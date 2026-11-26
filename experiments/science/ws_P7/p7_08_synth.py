"""
P7 item 4, second half: synthetic families -- how deep must the tree be?

 A. THE RING WITH REPULSIVE CHORDS (binary sites, reference = all sites unchanged):
        F(S) = |S| - w * #{ring edges inside S} + R * #{non-adjacent pairs inside S}     (S = set of changed sites)
    i.e. A_i = 1, M_ij = -w for ring neighbours, M_ij = +R otherwise.  For 0 < w < 2 and R large the
    reference is the unique minimiser.  Claims of the report (Proposition P7.5), tested here:
      * shares exist                      iff  w <= 1;
      * a set B of branching sites makes the leaf "all of B unchanged" certifiable iff every arc of the ring
        left by B, with q edges, has w <= (q + 1)/q;  for 3/2 < w < 2 arcs may have at most two sites, so
        the tree needs depth >= ceil(n/3) -- depth TWO for four sites;
      * the other leaves are certified at once, so depth d costs d + 1 leaves.
    Run in exact integer arithmetic (tables are multiples of 1/4): n = 4 at w = 3/4, 5/4, 7/4 (depths 0, 1, 2),
    then n = 4 ... 9 at w = 7/4, R = 10; every leaf compared with brute force over its 2^(free sites) states;
    for n = 4 also which sets of triplet constraints close the gap.
 B. THREE SITES NEVER NEED DEPTH TWO (Proposition P7.4): random three-site models, 2 to 4 states per site.
 C. RANDOM FOUR-SITE MODELS (2 or 3 states): how often a gap, how often depth two.
    B, C: random tables (uniform reals), reference = the minimiser found by brute force.

usage: python3 -B p7_08_synth.py > logs/p7_08_synth.log   (writes out/p7_08_synth.json; last line "DONE p7_08_synth")
"""
import sys, os, json, time, itertools, math
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM

t00 = time.time()
print(f"p7_08_synth  started {L7.now()}")
STAT = dict(leaf_cert=0, leaf_viol=0, leaf_truth=0, leaves=0)
OUT = {}


def ring(n, w, R):
    A = [np.array([0.0, 1.0]) for _ in range(n)]
    M = {}
    for i in range(n):
        for j in range(i + 1, n):
            T = np.zeros((2, 2))
            T[1, 1] = -w if (j - i == 1 or (i == 0 and j == n - 1)) else R
            M[(i, j)] = T
    return PM((2,) * n, (0,) * n, A, M)


class Tree:
    """leaf certification with a cache and brute-force comparison for one model."""

    def __init__(self, pm):
        self.pm = pm; self.ipm = IPM(pm); self.IG = self.ipm.grid(); self.cache = {}
        assert int(self.IG.min()) == 0 and int(self.IG[pm.r]) == 0

    def leaf(self, D):
        key = tuple(tuple(int(v) for v in d) for d in D)
        if key not in self.cache:
            c = L7.certify_leaf(self.pm, self.ipm, D)
            b = int(L7.box_min(self.IG, D))
            STAT["leaves"] += 1
            if b < 0:
                STAT["leaf_truth"] += 1
            if c["ok"]:
                STAT["leaf_cert"] += 1
                if c["LB"] > b:
                    STAT["leaf_viol"] += 1
            self.cache[key] = dict(ok=c["ok"], lp=c["lp"], kind=c["kind"], bf=b)
        return self.cache[key]

    def depth_needed(self, maxdepth):
        """least depth of a tree all of whose leaves are certified (None if > maxdepth), and its least number of leaves."""
        pm = self.pm

        def best(D, depth):
            if self.leaf(D)["ok"]:
                return (0, 1)
            if depth == 0:
                return None
            res = None
            for i in range(pm.n):
                if len(D[i]) < 2:
                    continue
                subs = [best(L7.fix(D, i, a), depth - 1) for a in D[i]]
                if any(s is None for s in subs):
                    continue
                cand = (1 + max(s[0] for s in subs), sum(s[1] for s in subs))
                if res is None or cand < res:
                    res = cand
            return res
        for d in range(maxdepth + 1):
            r = best(pm.full_domain(), d)
            if r is not None:
                return r
        return None


# ------------------------------------------------------------------------------------------------ 0
# the theory division's explicit integrality gap (theory report, Proposition 11.18b(e)): three binary sites,
# A = (1, 1, 1), c_12 = c_13 = 2, a known pair term T_23 = 10  ->  M_01 = M_02 = -2, M_12 = +10 (sites renumbered 0, 1, 2)
def _t(v):
    T = np.zeros((2, 2)); T[1, 1] = v
    return T
pm0 = PM((2, 2, 2), (0, 0, 0), [np.array([0.0, 1.0])] * 3, {(0, 1): _t(-2.0), (0, 2): _t(-2.0), (1, 2): _t(10.0)})
ipm0 = IPM(pm0)
p0 = L7.primal_lp(pm0)
rp0 = L7.rationalise_point(pm0, ipm0, p0["mu1"], p0["mu2"])
tr0 = Tree(pm0)
d0 = tr0.depth_needed(2)
print(f"\n0. the theory division's example of Proposition 11.18b(e): share LP t = {L7.shares_lp(pm0)['t']:+.4f}; relaxation value {p0['val']:+.4f} "
      f"(exact: {rp0['value']} with denominator {rp0['den']}; the report says -1/2); least depth of a certified tree {d0[0]}, leaves {d0[1]} "
      f"(this instance has ties: two pairs of changed sites have the value 0 of the reference)")
assert rp0["value"] == -L7.Fraction(1, 2)
OUT["theory_example"] = dict(t=L7.shares_lp(pm0)["t"], relaxation=p0["val"], depth=d0[0], leaves=d0[1])

# ------------------------------------------------------------------------------------------------ A
print("\nA. the ring with repulsive chords (exact integer arithmetic; R = 10)")
A_rows = []
for n, w in [(4, 0.75), (4, 1.25), (4, 1.75), (5, 1.75), (6, 1.75), (7, 1.75), (8, 1.75), (9, 1.75)]:
    pm = ring(n, w, 10.0)
    tr = Tree(pm)
    Dfull = pm.full_domain()
    root = L7.shares_lp(pm)["t"]
    relax = L7.dual_lp(pm, Dfull)["val"]
    # sets B of sites kept at the reference: is the leaf "B unchanged" certified?  least |B|
    least = None
    for d in range(0, n + 1):
        good = []
        for B in itertools.combinations(range(n), d):
            D = [np.array([0]) if i in B else Dfull[i] for i in range(n)]
            if tr.leaf(D)["ok"]:
                good.append(B)
        if good:
            least = (d, good)
            break
    d, good = least
    # the caterpillar tree along the first good B: branch on its sites in order; every "changed" leaf must be certified at once
    B = good[0]
    D = Dfull; ok_tree = True; nleaves = 0
    for i in B:
        ch = tr.leaf(L7.fix(D, i, 1))
        ok_tree = ok_tree and ch["ok"]; nleaves += 1
        D = L7.fix(D, i, 0)
    ok_tree = ok_tree and tr.leaf(D)["ok"]; nleaves += 1
    full = tr.depth_needed(3) if n <= 6 else None
    A_rows.append(dict(n=n, w=w, t_root=root, relaxation=relax, least_B=d, n_good_B=len(good), example_B=list(B), caterpillar_ok=ok_tree, caterpillar_leaves=nleaves,
                       search_depth_leaves=full, predicted=(0 if w <= 1 else math.ceil(n / 3) if w > 1.5 else math.ceil(n / 4))))
    print(f"  n = {n}, w = {w}: share LP t = {root:+.4f}, relaxation value {relax:+.4f} (minimum 0); least number of branching sites on the reference path {d} "
          f"(predicted {A_rows[-1]['predicted']}; {len(good)} such sets, e.g. {list(B)}); caterpillar tree with {nleaves} leaves certified: {ok_tree}"
          + (f"; exhaustive tree search (depth <= 3): least depth {full[0]}, least leaves {full[1]}" if full else ""))
    assert d == A_rows[-1]["predicted"] and ok_tree
# thresholds for n = 4 by a sweep of w (floating point; R = 10)
sweep = []
for w in np.round(np.arange(0.05, 2.0, 0.05), 2):
    pm = ring(4, float(w), 10.0)
    tr = Tree(pm)
    r_ = tr.depth_needed(2)
    sweep.append((float(w), r_[0] if r_ else None))
ch = [(sweep[i][0], sweep[i + 1][0], sweep[i][1], sweep[i + 1][1]) for i in range(len(sweep) - 1) if sweep[i][1] != sweep[i + 1][1]]
print(f"  n = 4, sweep of w in steps of 0.05: depth needed changes between {[(a, b) for a, b, _, _ in ch]} (depths {[(c, d_) for _, _, c, d_ in ch]}); predicted thresholds 1 and 3/2")
# triplets for n = 4, w = 7/4
pm = ring(4, 1.75, 10.0); ipm = IPM(pm)
T4 = list(itertools.combinations(range(4), 3))
trip = {}
for m_ in range(1, 5):
    for Ts in itertools.combinations(T4, m_):
        res = L7.multi_triple_lp(pm, list(Ts))
        ok = False
        if res["t"] is not None and res["t"] > 1e-9:
            mI, lamI = L7.multi_triple_to_int(ipm, pm.full_domain(), res["s"], res["lam"], list(Ts))
            ok = L7.multi_triple_bound(ipm, pm.full_domain(), mI, lamI, list(Ts))[0] >= 0
        trip[Ts] = (res["t"], ok)
by = {m_: (sum(1 for Ts, v in trip.items() if len(Ts) == m_ and v[1]), sum(1 for Ts in trip if len(Ts) == m_)) for m_ in range(1, 5)}
print(f"  n = 4, w = 7/4: sets of triplet constraints that close the gap (exact), by number of triples: {by};  slack t with all four triples: {trip[tuple(T4)][0]:.4f}; "
      f"best t with one / two / three triples: {max(v[0] for Ts, v in trip.items() if len(Ts) == 1):.4f} / {max(v[0] for Ts, v in trip.items() if len(Ts) == 2):.4f} / {max(v[0] for Ts, v in trip.items() if len(Ts) == 3):.4f}")
OUT["ring"] = dict(rows=A_rows, sweep=sweep, triplets_n4={str(k_): v for k_, v in by.items()})

# ------------------------------------------------------------------------------------------------ B, C
def random_model(rng, shape, coupling):
    n = len(shape)
    G = np.zeros(shape)
    for i in range(n):
        sh = [1] * n; sh[i] = shape[i]
        G = G + rng.uniform(-1, 1, size=shape[i]).reshape(sh)
    for i in range(n):
        for j in range(i + 1, n):
            sh = [1] * n; sh[i] = shape[i]; sh[j] = shape[j]
            G = G + coupling * rng.uniform(-1, 1, size=(shape[i], shape[j])).reshape(sh)
    r = tuple(int(v) for v in np.unravel_index(int(np.argmin(G)), G.shape))
    return PM.from_grid(G, r)


rng = np.random.default_rng(20261126)
print("\nB, C. random models (uniform tables; reference = the minimiser; exact integer acceptance of every certificate)")
print(f"{'sites':>5s} {'states':>6s} {'coupling':>8s} {'models':>6s} | {'shares':>6s} {'gap':>5s} | {'depth 1':>7s} {'depth 2':>7s} {'deeper':>6s} | {'gap certified by EVERY site':>27s} {'by one triple':>13s}")
BC = []
for (n, kset, coupling, N) in [(3, (2,), 2.0, 1500), (3, (3,), 2.0, 1500), (3, (2, 3, 4), 2.0, 1500), (4, (2,), 2.0, 1500), (4, (3,), 2.0, 1000), (4, (2,), 0.5, 1000), (5, (2,), 2.0, 600)]:
    cnt = dict(models=0, shares=0, gap=0, d1=0, d2=0, deeper=0, every=0, triple=0, degenerate=0)
    for _ in range(N):
        shape = tuple(int(rng.choice(kset)) for _ in range(n))
        pm = random_model(rng, shape, coupling)
        tr = Tree(pm)
        cnt["models"] += 1
        Dfull = pm.full_domain()
        t = L7.shares_lp(pm)["t"]
        if tr.leaf(Dfull)["ok"]:
            cnt["shares"] += 1
            continue
        if t > -1e-9:
            cnt["degenerate"] += 1
            continue
        cnt["gap"] += 1
        r_ = tr.depth_needed(2 if n <= 4 else 3)
        if r_ is None:
            cnt["deeper"] += 1
        elif r_[0] == 1:
            cnt["d1"] += 1
        else:
            cnt["d2" if r_[0] == 2 else "deeper"] += 1
        if all(all(tr.leaf(L7.fix(Dfull, i, a))["ok"] for a in pm.dom[i]) for i in pm.active()):
            cnt["every"] += 1
        for T in itertools.combinations(pm.active(), 3):
            rs = L7.shares_lp(pm, triple=T)
            if rs["t"] is not None and rs["t"] > 1e-9:
                m = L7.shares_to_messages(tr.ipm, Dfull, rs["s"], triple=T)
                if L7.leaf_bound(tr.ipm, Dfull, m, triple=T)[0] >= 0:
                    cnt["triple"] += 1
                    break
    BC.append(dict(n=n, states=list(kset), coupling=coupling, **cnt))
    print(f"{n:5d} {str(kset):>6s} {coupling:8.1f} {cnt['models']:6d} | {cnt['shares']:6d} {cnt['gap']:5d} | {cnt['d1']:7d} {cnt['d2']:7d} {cnt['deeper']:6d} | {cnt['every']:27d} {cnt['triple']:13d}"
          + (f"   (degenerate: {cnt['degenerate']})" if cnt["degenerate"] else ""), flush=True)
    if n == 3:
        assert cnt["d2"] == 0 and cnt["deeper"] == 0 and cnt["every"] == cnt["gap"], "a three-site model that is not certified by one branching on every site: contradicts P7.4"
OUT["random"] = BC
OUT["stat"] = STAT
json.dump(OUT, open(os.path.join(L7.HERE, "out", "p7_08_synth.json"), "w"), indent=1, default=lambda o: int(o) if isinstance(o, np.integer) else float(o))
print(f"\nBRUTE FORCE: {STAT['leaves']} leaves enumerated; {STAT['leaf_cert']} leaf certificates compared with the exact leaf minimum: violations {STAT['leaf_viol']}; leaves with a negative minimum {STAT['leaf_truth']}")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_08_synth.json   finished {L7.now()}")
print("DONE p7_08_synth")
