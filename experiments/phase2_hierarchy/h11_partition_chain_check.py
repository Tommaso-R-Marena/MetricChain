"""
Phase II (adaptive hierarchy) -- the relaxation principle for arbitrary nested hidden partitions
(report section 7.3, Theorem P): two independent checks.

Setting.  Fine classes c with weights phi_c; a type is z in [0,1]^C (density of ones per class);
r(z) = sum phi_c f(z_c), f = KL(.||1/2); ||z - z'|| = sum phi_c |z_c - z'_c|.  Partitions G1 <= G2 of the
classes (G2 refines G1).  avg_k = averaging over the cells of G_k, cost_k(z) = r(z) - r(avg_k z).
   V0 = { r <= theta }            what a blind batch sees
   V1 = { cost_1 <= theta }       what a batch that knows G1 sees
   V2 = { cost_2 <= theta }       what a batch that knows G2 sees
Hypotheses on a u-Lipschitz F:  F = F o avg_1 on V0,  F = F o avg_2 on V1.   nu0 = sup_{V0} (-F - r).
Theorem P:  theta >= h  ==>  -F(y) - r(y) <= nu0 + h - theta  for every y outside V2.

PART A (the chain of the proof, random instances, no grid).  For a random instance and a random y outside V2
the script builds the three points of the proof,
   e  = clip_l(y)  (two-sided clipping at the level l = s*kappa, s chosen with T(e) + Q(m') = theta),
   m' = clip_kappa(avg_2 e),
   e' = e with the lowest (highest) classes of every deep cell raised (lowered) until the cell mean is m',
and checks from the definitions only:
   (a) e' in V1                      [so F(e') = F(avg_2 e') = F(m')]
   (b) avg_2 e' = m', m' in V0       [so F(m') = F(avg_1 m') and the cap applies at avg_1 m']
   (c) B := r(avg_1 m') - r(y) + u ||y - e'||  <=  h - theta        (the bound of the theorem)
   (d) the per-cell price inequality  price(y_g -> e_g) + price(m_g -> m'_g) <= phi_g h.

PART B (exact, finite n, brute force).  Classes of sizes n_c, exact binomial probabilities.  The pointwise
largest U = -F on the grid of types with |U(k +- e_c) - U(k)| <= u, U <= R = -ln P on V0, U invariant under
exchanges between classes of the same G1-cell inside V0 and of the same G2-cell inside V1 (connected
components of the exchange graph, so nothing is assumed about the shape of the regions).  Reported:
   gain = max over types outside V2 of [U - R]      (theorem:  <= n h - Theta + O(#classes u) in entropy form,
                                                      + O(#classes log n) with exact binomial probabilities).
"""
import sys, itertools
import numpy as np
from scipy.special import gammaln
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

LN2 = np.log(2.0)
def f(r):
    r = np.clip(r, 1e-300, 1 - 1e-16); return LN2 + r * np.log(r) + (1 - r) * np.log1p(-r)
def consts(u):
    pu = 1 / (1 + np.exp(u)); L1 = np.log(2 / (1 + np.exp(-u))); return pu, L1, f(pu), f(L1 / u), L1 / u

# ---------------------------------------------------------------- PART A
def avg(z, w, cells):
    out = np.empty_like(z)
    for g in cells: out[g] = np.dot(w[g], z[g]) / w[g].sum()
    return out
def rate(z, w): return float(np.dot(w, f(z)))
def fill(e, w, cells, target):
    """raise the lowest (lower the highest) classes of each cell until its mean equals target"""
    out = e.copy()
    for g in cells:
        wg = w[g]; eg = e[g]; mg = np.dot(wg, eg) / wg.sum(); tg = target[g[0]]
        if abs(tg - mg) < 1e-15: continue
        # the mean of max(eg, lam) (resp. min(eg, lam)) is nondecreasing in lam
        lo, hi = (eg.min(), max(eg.max(), tg)) if tg > mg else (min(eg.min(), tg), eg.max())
        for _ in range(200):
            lam = 0.5 * (lo + hi)
            cand = np.maximum(eg, lam) if tg > mg else np.minimum(eg, lam)
            mean = np.dot(wg, cand) / wg.sum()
            if mean < tg: lo = lam
            else: hi = lam
        lam = 0.5 * (lo + hi)
        out[g] = np.maximum(eg, lam) if tg > mg else np.minimum(eg, lam)
    return out
def chain(u, w, G1, G2, y, theta):
    pu, L1, a, h, kap = consts(u)
    clipk = lambda z, l: np.minimum(np.maximum(z, l), 1 - l)
    def build(s):
        e = clipk(y, s * kap); m = avg(e, w, G2); mp = clipk(m, kap)
        T = rate(e, w) - rate(m, w); Q = rate(mp, w) - rate(avg(mp, w, G1), w)
        return e, m, mp, T, Q
    lo, hi = 0.0, 1.0                       # Phi(0) > theta >= Phi(1)
    for _ in range(100):
        s = 0.5 * (lo + hi); e, m, mp, T, Q = build(s)
        if T + Q > theta: lo = s
        else: hi = s
    e, m, mp, T, Q = build(hi)
    ep = fill(e, w, G2, mp)
    gam = lambda t: f(t) + u * np.minimum(t, 1 - t)
    res = {}
    res['a_cost1_eprime'] = rate(ep, w) - rate(avg(ep, w, G1), w) - theta               # <= 0
    res['b_mean_err'] = float(np.abs(avg(ep, w, G2) - mp).max())                        # = 0
    res['b_rate_mprime'] = rate(mp, w) - theta                                          # <= 0
    res['c_bound'] = rate(avg(mp, w, G1), w) - rate(y, w) + u * float(np.dot(w, np.abs(y - ep))) - (h - theta)   # <= 0
    worst = -1e9
    for g in G2:
        pr = float(np.dot(w[g], gam(e[g]) - gam(y[g]))) + w[g].sum() * float(gam(mp[g[0]]) - gam(m[g[0]]))
        worst = max(worst, pr - w[g].sum() * h)
    res['d_cell_price'] = worst                                                         # <= 0
    res['T_fill'] = (rate(ep, w) - rate(avg(ep, w, G2), w)) - T                         # <= 0
    return res

def random_instance(rng):
    nc = int(rng.integers(2, 9))
    w = rng.dirichlet(np.ones(nc) * rng.choice([0.3, 1.0, 3.0]))
    w = np.maximum(w, 1e-3); w /= w.sum()
    lab1 = rng.integers(0, rng.integers(1, nc + 1), nc)                 # cells of G1
    lab2 = lab1 * 100 + rng.integers(0, rng.integers(1, nc + 1), nc)    # G2 refines G1
    cells = lambda lab: [np.flatnonzero(lab == v) for v in np.unique(lab)]
    return w, cells(lab1), cells(lab2)
def random_type(rng, nc, u):
    pu, L1, a, h, kap = consts(u)
    mode = rng.integers(0, 6)
    if mode == 0: y = rng.random(nc)
    elif mode == 1: y = rng.beta(0.4, 0.4, nc)
    elif mode == 2: y = np.where(rng.random(nc) < 0.5, pu, 1 - pu) + 0.02 * rng.standard_normal(nc)
    elif mode == 3: y = np.where(rng.random(nc) < 0.6, pu * rng.random(), 0.5) + 0.01 * rng.standard_normal(nc)
    elif mode == 4: y = np.where(rng.random(nc) < 0.5, kap, 1 - kap) + 0.05 * rng.standard_normal(nc)
    else: y = rng.choice([0.0, pu, kap, 0.5, 1 - kap, 1 - pu, 1.0], nc)
    return np.clip(y, 0.0, 1.0)

def part_A(ntrials=20000, seed=20261128):
    rng = np.random.default_rng(seed)
    worst = {}; done = 0; tried = 0
    while done < ntrials:
        tried += 1
        u = float(rng.choice([0.25, 0.5, 1.0, 2.0, 4.0, 6.0]))
        pu, L1, a, h, kap = consts(u)
        w, G1, G2 = random_instance(rng)
        y = random_type(rng, len(w), u)
        theta = h * float(rng.choice([1.0, 1.0, 1.05, 1.3, 2.0, 3.0]))
        T_y = rate(y, w) - rate(avg(y, w, G2), w)
        if T_y <= theta * (1 + 1e-9): continue
        res = chain(u, w, G1, G2, y, theta)
        for k, v in res.items():
            v_rel = v / h if k not in ('b_mean_err',) else v
            if k not in worst or v_rel > worst[k][0]: worst[k] = (v_rel, u, theta / h, len(w), len(G1), len(G2))
        done += 1
    print("PART A: %d hidden types in random instances (%d draws); largest value of each quantity (all must be <= 0 up to rounding)" % (done, tried))
    names = {'a_cost1_eprime': "(a) cost_1(e') - theta, units of h", 'b_mean_err': "(b) |avg_2 e' - m'|",
             'b_rate_mprime': "(b) r(m') - theta, units of h", 'c_bound': "(c) B - (h - theta), units of h",
             'd_cell_price': "(d) cell price - phi_g h, units of h", 'T_fill': "    T(e') - T(e), units of h"}
    ok = True
    for k in ('a_cost1_eprime', 'b_mean_err', 'b_rate_mprime', 'c_bound', 'd_cell_price', 'T_fill'):
        v = worst[k]; ok &= v[0] <= 1e-7
        print("   %-40s max %+.3e   (at u=%g, theta=%.2fh, %d classes, |G1|=%d, |G2|=%d)" % ((names[k],) + v))
    print("   all checks passed:", ok)
    return ok

# ---------------------------------------------------------------- PART B
def components(mask, shape, cell_pairs):
    """connected components of the exchange graph k -> k + e_c - e_c' (c, c' in the same cell) inside mask"""
    idx = np.arange(mask.size).reshape(shape)
    rows = []; cols = []
    for c, d in cell_pairs:
        sl_a = [slice(None)] * len(shape); sl_b = [slice(None)] * len(shape)
        sl_a[c] = slice(0, shape[c] - 1); sl_b[c] = slice(1, shape[c])          # k_c -> k_c + 1
        sl_a[d] = slice(1, shape[d]); sl_b[d] = slice(0, shape[d] - 1)          # k_d -> k_d - 1
        A = idx[tuple(sl_a)]; B = idx[tuple(sl_b)]
        both = mask[tuple(sl_a)] & mask[tuple(sl_b)]
        rows.append(A[both]); cols.append(B[both])
    rows = np.concatenate(rows) if rows else np.zeros(0, int); cols = np.concatenate(cols) if cols else np.zeros(0, int)
    g = coo_matrix((np.ones(len(rows), np.int8), (rows, cols)), shape=(mask.size, mask.size))
    ncomp, lab = connected_components(g, directed=False)
    return lab.reshape(shape)
def comp_min(U, mask, lab):
    k = lab[mask]; v = U[mask]
    order = np.argsort(k, kind='stable'); ks = k[order]; vs = v[order]
    starts = np.r_[0, np.flatnonzero(np.diff(ks)) + 1]
    mins = np.minimum.reduceat(vs, starts)
    out = np.empty_like(vs); out[order] = np.repeat(mins, np.diff(np.r_[starts, len(ks)]))
    U2 = U.copy(); U2[mask] = out
    return U2
def lip_pass(U, u):
    for ax in range(U.ndim):
        U = np.moveaxis(U, ax, 0)
        for i in range(1, U.shape[0]): np.minimum(U[i], U[i - 1] + u, out=U[i])
        for i in range(U.shape[0] - 2, -1, -1): np.minimum(U[i], U[i + 1] + u, out=U[i])
        U = np.moveaxis(U, 0, ax)
    return U
def extremal(u, ns, G1, G2, Theta, form="entropy", iters=400):
    """form = "entropy":  R = sum n_c f(k_c/n_c) and cost_G = R - sum_g n_g f(a_g/n_g)   (no polynomial prefactors)
       form = "binomial": R = -ln P(type), cost_G = -ln P(type | its G-shell)             (exact probabilities)"""
    shape = tuple(n + 1 for n in ns)
    grids = np.meshgrid(*[np.arange(n + 1) for n in ns], indexing='ij')
    if form == "binomial":
        R = -sum(gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1) - n * LN2 for n, k in zip(ns, grids))
        shell = lambda ng, ag: -(gammaln(ng + 1) - gammaln(ag + 1) - gammaln(ng - ag + 1) - ng * LN2)
    else:
        R = sum(n * f(k / n) for n, k in zip(ns, grids))
        shell = lambda ng, ag: ng * f(ag / ng)
    def cost(G):
        c = R.copy()
        for g in G:
            ng = sum(ns[i] for i in g); ag = sum(grids[i] for i in g)
            c -= shell(ng, ag)
        return c
    V0 = R <= Theta; V1 = cost(G1) <= Theta; V2 = cost(G2) <= Theta
    pairs = lambda G: [(c, d) for g in G for c in g for d in g if c < d]
    lab0 = components(V0, shape, pairs(G1)); lab1 = components(V1, shape, pairs(G2))
    INF = 1e18
    U = np.where(V0, R, INF)
    for it in range(iters):
        Uold = U.copy()
        U = lip_pass(U, u)
        U = comp_min(U, V0, lab0)
        U = comp_min(U, V1, lab1)
        if it > 2 and np.max(np.abs(U - Uold)) < 1e-10: break
    hidden = ~V2
    gain = float((U - R)[hidden].max()) if hidden.any() else float('-inf')
    j = np.unravel_index(np.argmax(np.where(hidden, U - R, -INF)), shape)
    return gain, tuple(int(x) for x in j), it

CASES = [
    ("one merged cell, two hidden classes; nothing learned",        (120, 120),      [[0, 1]],          [[0, 1]]),
    ("one merged cell, unequal hidden classes",                      (60, 180),       [[0, 1]],          [[0, 1]]),
    ("merged cell split in round 2 into {1}, {2,3}",                 (60, 80, 100),   [[0, 1, 2]],       [[0], [1, 2]]),
    ("merged pair revealed first; third class never",                (80, 80, 80),    [[0, 1], [2]],     [[0, 1], [2]]),
    ("pair split in round 2; hidden pair never split",               (40, 40, 40, 40),[[0, 1, 2, 3]],    [[0, 1], [2, 3]]),
    ("two cells in round 1, each with a hidden pair",                (40, 60, 50, 30),[[0, 1], [2, 3]],  [[0, 1], [2, 3]]),
    ("nothing in round 1; round 2 splits {1,2} from {3,4}",          (30, 50, 40, 40),[[0, 1, 2, 3]],    [[0, 1], [2, 3]]),
]
def part_B():
    print("PART B1: extremal profiles on the lattice of types, entropy form (no polynomial prefactors).")
    print("         excess = [max over types hidden from the third batch of (U - R)] - (n h - Theta), nats;  blind-visible maximum 0;")
    print("         theorem:  excess <= O(#classes * u)  for Theta >= n h   (for Theta < n h a plain dip is hidden and the excess is positive).")
    worst = -1e9
    for u in (1.0, 2.0, 4.0):
        pu, L1, a, h, kap = consts(u)
        for name, ns, G1, G2 in CASES:
            n = sum(ns); row = []
            for th in (0.7, 1.0, 1.2, 1.5, 2.5):
                gain, at, it = extremal(u, ns, G1, G2, th * n * h)
                ex = gain - (n * h - th * n * h); row.append("%.1f: %+7.2f" % (th, ex))
                if th >= 1.0: worst = max(worst, ex / u)
            print("  u=%g n=%d sizes %-17s G1=%-17s G2=%-17s excess at Theta/nh = %s" % (u, n, ns, G1, G2, " | ".join(row)))
            sys.stdout.flush()
    print("  largest excess over all cases with Theta >= n h: %.2f u" % worst)
    print("PART B2: growth with n (same proportions; Theta = 1.2 n h).  excess as above, entropy form / exact binomial form.")
    for u in (2.0, 4.0):
        pu, L1, a, h, kap = consts(u)
        for name, base, G1, G2 in (("merged cell, two hidden classes", (1, 3), [[0, 1]], [[0, 1]]),
                                   ("merged cell split in round 2", (3, 4, 5), [[0, 1, 2]], [[0], [1, 2]]),
                                   ("merged pair first; third class never", (1, 1, 1), [[0, 1], [2]], [[0, 1], [2]])):
            row = []
            for scale in ((60, 120, 240, 480) if len(base) == 2 else (20, 40, 60)):
                ns = tuple(b * scale for b in base); n = sum(ns)
                ex = []
                for form in ("entropy", "binomial"):
                    gain, at, it = extremal(u, ns, G1, G2, 1.2 * n * h, form=form)
                    ex.append(gain - (n * h - 1.2 * n * h))
                row.append("n=%d: %+.2f / %+.2f" % (n, ex[0], ex[1]))
            print("  u=%g %-38s %s" % (u, name, " | ".join(row))); sys.stdout.flush()

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "AB"
    if "A" in which: part_A()
    if "B" in which: part_B()
