"""Validations (numerics before theory).
(a) the Markov-recursion (DP) inequality  sum_x pi_phi(x)^t Q(x)^(1-t) >= prod_i c_i  on random inhomogeneous binary chains with
    random members phi of the class (not only vertices) and random Markov Q;
(b) exact sub-additivity of F+ (free-b.c. law, slack K at both ends), super-additivity of F- (envelope reduced by K), the sandwich
    F- <= F <= F+, the gap F+ - F- <= t*Delta, and sub-additivity of the DP block function, at fixed t;
(c) Step 5: class-wise quantiles are admissible for type classes of the cube (group orbits) and NOT for Markov (pair) type classes;
(d) convergence of exact increments of ln E[Xi^r] to the transfer-operator value."""
import sys, time, math, itertools
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *
from ylyap import *

rng = np.random.default_rng(7); t0 = time.time()

# ------------------------------------------------------------------ (a)
print("(a) DP inequality on random inhomogeneous binary chains")
worst = 1e9; ncase = 0; tight = 1e9
for case in range(60):
    n = int(rng.integers(5, 9)); X = np.array(list(itertools.product((0, 1), repeat=n)))
    us = rng.uniform(0.3, 1.5, n)                                         # site slopes (Hamming envelopes u_i)
    Ps = [None] + [None] * (n - 1)
    p1 = rng.dirichlet([2, 2])
    Ps = [rng.dirichlet([1.5, 1.5], size=2) for _ in range(n - 1)]        # P_i(b, a), i = 2..n
    pi = p1[X[:, 0]].copy()
    for i in range(1, n): pi *= Ps[i - 1][X[:, i - 1], X[:, i]]
    D = np.zeros((2 ** n, 2 ** n))
    for i in range(n): D += us[i] * (X[:, i][:, None] != X[:, i][None, :])
    # d*_i: backward recursion with G_i = max over ordered pairs (a,a') and extreme rays w of K_{i+1}
    dst = np.zeros(n); dst[n - 1] = us[n - 1]
    for i in range(n - 2, -1, -1):
        Pn = Ps[i]; G = -1e9
        for (a, a2) in ((0, 1), (1, 0)):
            for lam in (dst[i + 1], -dst[i + 1]):
                w = np.array([math.exp(lam / 2), math.exp(-lam / 2)])
                G = max(G, math.log((Pn[a2] @ w) / (Pn[a] @ w)))
        dst[i] = us[i] + G
    for rep in range(5):
        c = rng.uniform(0, rng.choice([1.0, 4.0]) * D.max(), 2 ** n)
        if rng.random() < 0.5: c[rng.random(2 ** n) < 0.85] = np.inf; c[rng.integers(2 ** n)] = 0.0
        phi = (c[None, :] + D).min(axis=1)
        if rep == 4: phi = D[:, rng.integers(2 ** n)] * rng.choice([1.0, -1.0])   # a cone or an anti-cone
        assert (phi[:, None] - phi[None, :] - D).max() < 1e-9
        t = float(rng.uniform(0.1, 0.9))
        q1 = rng.dirichlet([2, 2]); qs = [rng.dirichlet([1.5, 1.5], size=2) for _ in range(n - 1)]
        Q = q1[X[:, 0]].copy()
        for i in range(1, n): Q *= qs[i - 1][X[:, i - 1], X[:, i]]
        piphi = pi * np.exp(-phi); piphi /= piphi.sum()
        lhs = float((piphi ** t * Q ** (1 - t)).sum())
        lam = np.linspace(-1, 1, 801)
        def cmin(prow, qrow, dd):
            v = np.exp(np.outer(lam * dd, [0.5, -0.5]))                        # tilts within [-dd, dd]
            tl = prow[None, :] * v; tl /= tl.sum(axis=1, keepdims=True)
            return float(((tl ** t) * (qrow[None, :] ** (1 - t))).sum(axis=1).min())
        rhs = cmin(p1, q1, dst[0])
        for i in range(1, n): rhs *= min(cmin(Ps[i - 1][b], qs[i - 1][b], dst[i]) for b in (0, 1))
        worst = min(worst, lhs / rhs); ncase += 1
print("   %d cases: min of [sum pi_phi^t Q^(1-t)] / [prod c_i] = %.6f  (must be >= 1)" % (ncase, worst))

# ------------------------------------------------------------------ (b)
print("(b) F+, F-, DP at fixed t, binary symmetric chain, u = 1")
u = 1.0
for p in (0.4, 0.3):
    K = math.log((1 - p) / p); us = ustar(u, p)
    for t in (0.3, 0.45, 0.7):
        F = lambda law, w: renyi_F(gibbs_rows(law, lip_vertices(w)), t, tol=1e-11)
        Fp = {1: F(bsc_block_law(1, p), [u + 2 * K]), 2: F(bsc_block_law(2, p), [u + K, u + K]), 3: F(bsc_block_law(3, p), [u + K, u, u + K])}
        Fpl = {L: F(bsc_block_law(L, p), [u] * L) for L in (1, 2, 3)}
        Fd = {L: F(bsc_block_law_cond(L, p, 0), [u] * (L - 1) + [us]) for L in (1, 2, 3)}
        s = "   p=%.1f t=%.2f: F+_1,2,3 = %.6f %.6f %.6f  sub-add: F+_2 - 2F+_1 = %+.6f, F+_3 - F+_1 - F+_2 = %+.6f (<= 0) | DP: FD_2 - 2FD_1 = %+.6f, FD_3 - FD_1 - FD_2 = %+.6f (<= 0)" % (
            p, t, Fp[1][0], Fp[2][0], Fp[3][0], Fp[2][0] - 2 * Fp[1][0], Fp[3][0] - Fp[1][0] - Fp[2][0], Fd[2][0] - 2 * Fd[1][0], Fd[3][0] - Fd[1][0] - Fd[2][0])
        if u > 2 * K:
            Fm = {1: F(bsc_block_law(1, p), [u - 2 * K]), 2: F(bsc_block_law(2, p), [u - K, u - K]), 3: F(bsc_block_law(3, p), [u - K, u, u - K])}
            s += " | F-_1,2,3 = %.6f %.6f %.6f  super-add: %+.6f, %+.6f (>= 0) | sandwich F- <= F <= F+: %s | (F+_3 - F-_3)/(t*2(u+K)) = %.3f (<= 1)" % (
                Fm[1][0], Fm[2][0], Fm[3][0], Fm[2][0] - 2 * Fm[1][0], Fm[3][0] - Fm[1][0] - Fm[2][0],
                all(Fm[L][0] <= Fpl[L][0] + 1e-9 <= Fp[L][0] + 2e-9 for L in (1, 2, 3)), (Fp[3][0] - Fm[3][0]) / (t * 2 * (u + K)))
        else:
            s += " | plain <= F+: %s | plain <= DP*L-type bound: F_L <= L*FD_1: %s" % (all(Fpl[L][0] <= Fp[L][0] + 1e-9 for L in (1, 2, 3)), all(Fpl[L][0] <= L * Fd[1][0] + 1e-9 for L in (1, 2, 3)))
        print(s)

# ------------------------------------------------------------------ (c)
print("(c) Step 5: are class-wise upper quantiles admissible?  (t_{class(y)} <= t_{class(x)} e^{d(x,y)} for all x, y)")
n = 9; X = np.array(list(itertools.product((0, 1), repeat=n))); N = len(X)
Dh = (X[:, None, :] != X[None, :, :]).sum(axis=2).astype(float)
typ = X.sum(axis=1)
pairs = X[:, :-1] * 2 + X[:, 1:]
mark = np.array([hash((int(x[0]),) + tuple(np.bincount(pr, minlength=4))) for x, pr in zip(X, pairs)])
_, mark = np.unique(mark, return_inverse=True); print("   n=%d: %d type classes, %d Markov (pair) type classes" % (n, len(set(typ)), mark.max() + 1))
def quantile_levels(w, cls, q):
    lev = np.zeros(cls.max() + 1)
    for c in range(cls.max() + 1):
        v = np.sort(w[cls == c])[::-1]                         # descending
        k = int(math.floor(q * len(v) + 1e-12))                # at most k points may lie strictly above the level
        lev[c] = v[k] if k < len(v) else v[-1]
        # smallest value tau of w on the class with dens{w > tau} <= q
        j = k
        while j < len(v) - 1 and v[j + 1] == v[j]: j += 1
        lev[c] = v[k]
    return lev
viol = {"type": 0, "markov": 0}; tot = 0; worst = {"type": -1e9, "markov": -1e9}
for rep in range(200):
    c = rng.uniform(0, rng.choice([2.0, 6.0]) * n, N)
    if rng.random() < 0.7: c[rng.random(N) < 0.97] = np.inf; c[rng.integers(N)] = 0.0
    psi = (c[None, :] + Dh).min(axis=1); w = np.exp(-psi)
    for q in (0.05, 0.2, 0.5):
        tot += 1
        for name, cls in (("type", typ), ("markov", mark)):
            lev = quantile_levels(w, cls, q)
            v = float((np.log(lev[cls])[None, :] - np.log(lev[cls])[:, None] - Dh).max())      # ln t_y - ln t_x - d(x,y) <= 0 ?
            worst[name] = max(worst[name], v); viol[name] += v > 1e-9
print("   %d (residual, q) cases, u = 1: violations for type classes: %d (largest excess %.2e);  for Markov type classes: %d (largest excess %.3f)" % (
    tot, viol["type"], worst["type"], viol["markov"], worst["markov"]))
# the explicit example of the report: n = 9, psi = d(., y*), y* = 000000010, q < 1/7
ystar = np.zeros(n, int); ystar[n - 2] = 1; iy = int((X == ystar).all(axis=1).argmax())
w = np.exp(-Dh[:, iy]); lev = quantile_levels(w, mark, 0.1)
x = np.zeros(n, int); x[0] = x[1] = 1; y = np.zeros(n, int); y[1] = 1
ix = int((X == x).all(axis=1).argmax()); iyy = int((X == y).all(axis=1).argmax())
print("   example: psi = d(., 000000010): level of the class of x = 110000000: %.4f (= e^-3); of y = 010000000: %.4f; d(x,y) = 1; admissibility needs t_y <= t_x e = %.4f: %s" % (
    lev[mark[ix]], lev[mark[iyy]], lev[mark[ix]] * math.e, "VIOLATED" if lev[mark[iyy]] > lev[mark[ix]] * math.e + 1e-12 else "ok"))

# ------------------------------------------------------------------ (d)
print("(d) exact increments of ln E[Xi^r] against the operator value (slow cases of y03)")
for (kappa, eta, q, r) in [(1.5, 0.1, 0.3, 5.0), (2.0, 0.3, 0.1, 3.0)]:
    Lop = moment_lyap(kappa, eta, q, r, 64)
    vals = [moment_exact(kappa, eta, q, r, n) for n in range(11, 22)]
    inc = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    gaps = [Lop - x for x in inc]
    print("   kappa=%.1f eta=%.1f q=%.1f r=%.0f: operator %.8f; increments n=12..21: %s; gap ratios %s" % (
        kappa, eta, q, r, Lop, " ".join("%.5f" % x for x in inc[::3]), " ".join("%.3f" % (gaps[i + 1] / gaps[i]) for i in range(0, len(gaps) - 1, 3))))
print("%.1f s" % (time.time() - t0))
