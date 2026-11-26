#!/usr/bin/env python3
"""A scan in the penalty strength: when does a floor leave the anchor?  (For the theory division, THY-RES-0016 section 5 (i):
"a first-order transition in the penalty strength"; promised in SCI-RES-0024 section 3 (c).)

The floor of a certificate is  m_-(x) = (model without penalty)(x) - pen(x),  pen the sum of workstream P9's resolved
tables in the window form (every subset T charged in full to one in-window sub-tuple K(T); addendum A17 (19), item 67).
Here the penalty is multiplied by lambda:

        m_lambda(x) = (model without penalty)(x) - lambda * pen(x),         lambda = 1 is the certificate's floor,

and for every lambda are printed: ln Z(m_lambda) (transfer matrix, exact), the slope d ln Z / d lambda = beta <pen>_lambda
(central difference of exact values), the first-order number lambda * beta <pen>_0, and, from N exact samples of
m_lambda: the mean number of sites off the anchor, the largest, and the share of samples with at least half the sites off.
ln Z(m_lambda) is convex in lambda; a first-order transition shows as a jump of the slope and of the occupancy at a
lambda_c that the first-order number does not see.  After the coarse grid, lambda_c (the lambda at which the mean number
of sites off the anchor crosses half the chain) is located by bisection.
The model, the tables and the choice K(T) are built exactly as in first_order_recovery.py (the lines are copied from
its main(), commit 0930440, up to the two models; the allowance is attached to each evaluated term); nothing here is a
certificate.  Control printed: at lambda = 1 the value must equal the floor of the committed log of the same case.

Run: python3 -B floor_transition.py K12 4 7 > floor_transition_K12_m4_w7.log
     python3 -B floor_transition.py LKSE:12 3 7 --grid 0,0.05,0.1,0.2,0.3,0.5,0.75,1 > floor_transition_LKSEc12_m3_w7.log
"""
import os, sys, copy, math, time, glob, itertools, functools, resource
import numpy as np
import nested_sampler as NS
from window_model_occ import build_window_models_occ, gibbs_sample
L, pw = NS.L, NS.pw
BETA, RND = L.BETA, 1.0 + 1e-9
HERE = os.path.dirname(os.path.abspath(__file__)); SCI = os.path.normpath(os.path.join(HERE, ".."))
P8, P9, MYT = os.path.join(SCI, "ws_P8"), os.path.join(SCI, "ws_P9"), os.path.join(SCI, "p9_verification", "cache")


def log(s): print(s, flush=True)


def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def maximal_windows(U, w):
    sets = []
    for a in range(len(U)):
        V = tuple(p for p in range(len(U)) if U[a] <= U[p] <= U[a] + w)
        if not any(set(V) <= set(V2) for V2 in sets):
            sets = [V2 for V2 in sets if not set(V2) <= set(V)] + [V]
    return sets


def main():
    a = sys.argv[1:]; seq, m, w = a[0], int(a[1]), int(a[2]); bb = "H"; M = m - 1; t0 = time.time()
    grid = [float(v) for v in a[a.index("--grid") + 1].split(",")] if "--grid" in a else [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 3, 4, 6, 8, 12, 16]
    NSAMP = int(a[a.index("--N") + 1]) if "--N" in a else 1000
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]; X0 = np.array(x0)
    subs = list(itertools.combinations(range(n), m)); non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
    # ---- P9's raw tables (as first_order_recovery.py)
    files = sorted(glob.glob(os.path.join(P9, "cache", f"theta2_{tag}_m{m}*.npz"))) or sorted(glob.glob(os.path.join(MYT, f"theta2_{tag}_m{m}*.npz")))
    tabs = [None] * len(subs)
    for fn in files:
        z = np.load(fn)
        for j in z["idx"]: tabs[int(j)] = np.array(z[f"t{int(j)}"], dtype=float)
    assert all(t is not None for t in tabs), "raw tables of P9 missing"
    log(f"=== {seq} on {bb}, tau {tau}: {n} sites, states per site {k}, anchor {x0}; order m = {m}, band {w}; {len(subs)} raw stage-2 tables of workstream P9 "
        f"(sum of their maxima {BETA * sum(float(t.max()) for t in tabs):.5g} kT)")

    def full(sites, red):
        out = np.zeros([k[i] for i in sites]); out[np.ix_(*[non[i] for i in sites])] = red
        return out
    # ---- the ball and the anchored terms (as first_order_recovery.py)
    blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0); vals = None
    for f in sorted(os.listdir(os.path.join(P8, "cache"))):
        if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f:
            z = np.load(os.path.join(P8, "cache", f))
            if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst): vals = np.array(z["vals"][:tot], dtype=float); break
    if vals is None: vals = np.concatenate([G.bulk_energy(allst[s:s + 256]) for s in range(0, tot, 256)])
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[p], c)
        return vals_s[p]
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None); assert nb == tot
    del allst, code, order
    XGo = gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(4242))
    log(f"(0) ball of radius {M}: {tot} values; guiding Gibbs sample (seed 4242): {float((XGo != X0[None]).sum(1).mean()):.2f} sites off the anchor on average [{time.time() - t0:.0f}s]")
    # ---- K(T) (as first_order_recovery.py)
    fst = os.path.join(P9, "out", f"tables_{tag}_m{m}_w{w}.npz"); keepK = None
    if os.path.exists(fst):
        ZS = np.load(fst)
        if [tuple(int(v) for v in T) for T in ZS["s2_subs"]] == subs and [int(v) for v in ZS["x0"]] == x0:
            keepK = [tuple(int(v) for v in str(s).split("_")) for s in ZS["s2_keep"]]; srck = "workstream P9's stored choice"
    if keepK is None:
        pm = [((np.bincount(XGo[:, i], minlength=k[i]) + 0.5) / (len(XGo) + 0.5 * k[i]))[non[i]] for i in range(n)]; keepK = []
        for T, tab in zip(subs, tabs):
            best = None
            for keep in ([tuple(range(m))] if T[-1] - T[0] <= w else maximal_windows(T, w)):
                other = tuple(p for p in range(m) if p not in keep); red = tab.max(axis=other) if other else tab; sc = red
                for p in reversed(keep): sc = sc @ pm[T[p]]
                if best is None or (float(sc), float(red.max())) < best[0]: best = ((float(sc), float(red.max())), tuple(T[p] for p in keep))
            keepK.append(best[1])
        srck = "the least mean of the reduced table under the product of the guiding sample's one-site marginals"
    W = {}
    for T, tab, K in zip(subs, tabs, keepK):
        other = tuple(p for p in range(m) if T[p] not in K); red = tab.max(axis=other) if other else tab
        W[K] = W.get(K, 0.0) + full(K, red)
    g1 = [W.get((i,), np.zeros(k[i])) for i in range(n)]; g2 = {K: v for K, v in W.items() if len(K) == 2}; g3 = {K: v for K, v in W.items() if len(K) >= 3}

    def pen(X):
        X = np.atleast_2d(X); out = np.zeros(len(X))
        for i in range(n): out += g1[i][X[:, i]]
        for K, v in list(g2.items()) + list(g3.items()): out += v[tuple(X[:, u] for u in K)]
        return out
    # ---- the floor without penalty: allowance attached to each evaluated term (as first_order_recovery.py, (1b))
    zn, znn = np.zeros(n), np.zeros((n, n)); offm = [np.ones(k[i]) for i in range(n)]
    for i in range(n): offm[i][x0[i]] = 0.0
    d_lo = {U: (arr if len(U) == 0 else arr - (2 ** len(U)) * L.EPS_G * functools.reduce(np.multiply.outer, [offm[u] for u in U])) for U, arr in d.items()}
    lo0, _, info = build_window_models_occ(NS.WindowModel, k, x0, c0, h, J, d_lo, w, L.EPS_G, M, zn, znn, None, XG=XGo, far_pairs="anchored"); del _
    penmax = float(sum(v.max() for v in g1) + sum(v.max() for v in g2.values()) + sum(v.max() for v in g3.values()))
    log(f"(1) floor without penalty built ({info['exact']} evaluated terms exact in a window, {info['reduced']} reduced, {info['far_pairs']} pairs beyond the band); K(T): {srck}; "
        f"penalty tables in the window form: {sum(1 for v in g1 if v.any())} on one site, {len(g2)} on pairs, {len(g3)} on larger sub-tuples; sum of their maxima {BETA * penmax:.5g} kT [{time.time() - t0:.0f}s, peak RSS {rss():.0f} MB]")

    def model(lam):
        mdl = copy.deepcopy(lo0)
        for i in range(n): mdl.one[i] = mdl.one[i] - lam * g1[i] * RND
        for (i, j), v in g2.items(): mdl.add_pair(i, j, -lam * v * RND)
        for U, v in g3.items(): mdl.add_multi(U, -lam * v * RND)
        return mdl
    cache = {}

    def lnz(lam):
        if lam not in cache: cache[lam] = model(lam).lnZ()
        return cache[lam]

    def row(lam, rng):
        mdl = model(lam); z = mdl.lnZ(); cache[lam] = z; dl = 1e-3 * max(lam, 1.0)
        slope = (lnz(lam + dl) - lnz(max(lam - dl, 0.0))) / (lam + dl - max(lam - dl, 0.0))
        X = mdl.sample(NSAMP, rng); off = (X != X0[None]).sum(1); p = pen(X)
        return dict(lam=lam, lnZ=z, slope=slope, off=float(off.mean()), offmax=int(off.max()), half=float((off >= (n + 1) // 2).mean()), penmean=BETA * float(p.mean()), mshare=float((off >= m).mean()))
    rng = np.random.default_rng(1234 + m); z0 = lnz(0.0); s0 = (lnz(1e-3) - z0) / 1e-3
    log(f"(2) ln Z(m_0) = {z0:.7f} (no penalty); slope at 0: beta <pen>_0 = {s0:.6g} nats per unit of lambda; {NSAMP} exact samples per lambda")
    log("| lambda | ln Z(m_lambda) | ln Z(m_lambda) - ln Z(m_0) | first order lambda beta <pen>_0 | slope beta <pen>_lambda (exact, by differences) | sampled beta <pen>_lambda | mean number of sites off the anchor | largest | share of samples with at least m sites off | share with at least half the chain off |")
    log("|---|---|---|---|---|---|---|---|---|---|")
    rows = []
    for lam in grid:
        r = row(lam, rng); rows.append(r)
        log(f"| {lam:g} | {r['lnZ']:.7f} | {r['lnZ'] - z0:.6g} | {lam * s0:.6g} | {r['slope']:.6g} | {r['penmean']:.6g} | {r['off']:.3f} | {r['offmax']} | {r['mshare']:.4f} | {r['half']:.4f} |")
    # ---- convexity of ln Z in lambda on the grid (a check of the numbers: second differences of a convex function are >= 0)
    lam_s = sorted(set(r["lam"] for r in rows)); zz = [cache[v] for v in lam_s]
    sl = [(zz[q + 1] - zz[q]) / (lam_s[q + 1] - lam_s[q]) for q in range(len(zz) - 1)]
    log(f"(3) ln Z(m_lambda) convex on the grid (slopes of successive chords nondecreasing): {all(sl[q + 1] >= sl[q] - 1e-9 for q in range(len(sl) - 1))}; "
        f"control, the same test on -ln Z (must fail unless the curve is a line): {all(-sl[q + 1] >= -sl[q] - 1e-9 for q in range(len(sl) - 1))}")
    # ---- locate lambda_c: the mean number of sites off the anchor crosses half the chain
    lo_l = max([r["lam"] for r in rows if r["off"] < n / 2], default=None); hi_l = min([r["lam"] for r in rows if r["off"] >= n / 2], default=None)
    if lo_l is None or hi_l is None or hi_l < lo_l:
        log(f"(4) the mean number of sites off the anchor does not cross n/2 = {n / 2:g} monotonically on the grid (below at lambda <= {lo_l}, above from {hi_l}): no lambda_c located")
    else:
        fine = []
        for it in range(9):
            mid = 0.5 * (lo_l + hi_l); r = row(mid, rng); fine.append(r)
            if r["off"] < n / 2: lo_l = mid
            else: hi_l = mid
        log("    bisection: " + "; ".join(f"lambda {r['lam']:.4f}: {r['off']:.2f} off, slope {r['slope']:.4g}" for r in fine))
        ra, rb = row(lo_l, rng), row(hi_l, rng)
        log(f"(4) lambda_c in [{lo_l:.4f}, {hi_l:.4f}] (ratio {hi_l / lo_l:.4f}): mean number of sites off the anchor {ra['off']:.2f} -> {rb['off']:.2f}, slope {ra['slope']:.5g} -> {rb['slope']:.5g}, "
            f"ln Z - ln Z(m_0) there {ra['lnZ'] - z0:.5g} against the first-order number {lo_l * s0:.5g}; at lambda = 1: ln Z(m_1) - ln Z(m_0) = {lnz(1.0) - z0:.6g}, first order {s0:.6g}")
        below = [r for r in rows + fine if r["lam"] <= lo_l]; width = None
        l2 = max([r["lam"] for r in rows + fine if r["off"] < 2.0], default=None); l8 = min([r["lam"] for r in rows + fine if r["off"] > 8.0], default=None)
        if l2 is not None and l8 is not None and l8 > l2 > 0:
            log(f"    sharpness: the mean number of sites off the anchor is below 2 up to lambda = {l2:.4f} and above 8 from lambda = {l8:.4f}: a factor {l8 / l2:.3f} in lambda")
    log(f"(5) at lambda = 1: ln Z(m_1) = {lnz(1.0):.7f} -- to be compared with the upper end of the sandwich in the committed log of the same case (first_order_recovery_{tag.split('_')[0]}_m{m}_w{w}.log)")
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {rss():.0f} MB")


if __name__ == "__main__":
    main()
