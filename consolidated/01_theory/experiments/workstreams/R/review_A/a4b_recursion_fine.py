"""Referee A, test 4b: the recursion itself on a fine grid, with the supremum over gamma evaluated EXACTLY for the
piecewise-linear interpolant of T_k, against the majorants M_{S_k, tau_k} of the exact dynamics of convex majorants
(Proposition U + Corollary U' iterated from T_1 = theta) and against the minorant lines of Proposition A.

Only the proved monotonicity of T_k is used for the supremum over gamma (not the shortcut 'sup at max(beta, mu)'):
for nonincreasing T,   sup_{gamma >= beta} [min(gamma, mu) + (1-phi) T(gamma/(1-phi))]
    = (1-phi) max_{beta/(1-phi) <= y <= mu/(1-phi)} (y + T(y))          if beta <= mu      (range maximum of S = y + T)
    = mu + (1-phi) T(beta/(1-phi))                                        if beta >  mu.
The infimum over (phi, beta): a (phi, beta) mesh (logit(phi) x log(beta/g)), then repeated zooms around the best cells.
T_k is the piecewise-linear (in g) interpolant of its grid values (constant below the grid, 0 from e = 1 on), made
nonincreasing by a running minimum.  Result: an estimate of T_k with errors from the g-grid only; the size of the
error is visible in the comparison with the (machine-checked) lower bound from lines.
Usage: python3 a4b_recursion_fine.py [levels] [check]
"""
import math, sys, time
import numpy as np
from ralib import Gauss, bracket_sup_gamma
from dual_dyn import DualDyn, gauss_sig3

KL = int(sys.argv[1]) if len(sys.argv) > 1 else 6
NU = int(sys.argv[3]) if len(sys.argv) > 3 else 161            # number of uniform points in [1e-2, 1]
NGEO = int(sys.argv[4]) if len(sys.argv) > 4 else 140          # number of geometric points in [1e-8, 1e-2]
G = Gauss()
gs = np.unique(np.concatenate([np.exp(np.linspace(math.log(1e-8), math.log(1e-2), NGEO)), np.linspace(1e-2, 1.0, NU)]))
NG = len(gs)


class PLT:
    """nonincreasing piecewise-linear T on the grid gs, with range maxima of S(y) = y + T(y)."""
    def __init__(self, vals):
        self.v = np.minimum.accumulate(np.asarray(vals, dtype=float))
        self.S = gs + self.v
        tab = [self.S]
        k = 1
        while 2 * k <= NG:
            prev = tab[-1]
            tab.append(np.maximum(prev[:NG - 2 * k + 1], prev[k:NG - k + 1]))
            k *= 2
        self.tab = tab

    def T(self, x):
        x = np.asarray(x, dtype=float)
        return np.where(x >= 1.0, 0.0, np.interp(x, gs, self.v))

    __call__ = T

    def rangemaxS(self, lo, hi):
        """max_{lo <= y <= hi} (y + T(y)) for arrays lo <= hi."""
        out = np.maximum(lo + self.T(lo), hi + self.T(hi))
        # beyond 1: S(y) = y increasing -> endpoints suffice; nodes strictly inside [lo, hi]
        i0 = np.searchsorted(gs, lo, side="left")
        i1 = np.searchsorted(gs, hi, side="right") - 1
        ok = i1 >= i0
        if np.any(ok):
            a0, a1 = i0[ok], i1[ok]
            ln = a1 - a0 + 1
            k = np.floor(np.log2(ln)).astype(int)
            res = np.empty(len(a0))
            for kk in np.unique(k):
                sel = k == kk
                t = self.tab[kk]
                res[sel] = np.maximum(t[a0[sel]], t[a1[sel] - (1 << kk) + 1])
            tmp = out[ok]
            out[ok] = np.maximum(tmp, res)
        return out


def V(T, g, phi, beta):
    mu = phi * G((g - beta) / phi)
    one = 1.0 - phi
    lo = beta / one
    hi = np.maximum(beta, mu) / one
    v1 = one * T.rangemaxS(lo, hi)                      # used when beta <= mu
    v2 = mu + one * T.T(lo)                              # used when beta > mu
    return np.where(beta <= mu, v1, v2)


def R_fine(T, g, nz=700, nl=72, zooms=5):
    """min over a (logit phi) x (ln beta/g) mesh; then, FOR EVERY beta of the mesh, a 1-d zoom in phi around the best
    phi of that row (narrow valleys in phi at fixed beta -- e.g. the family beta -> 0, phi = g/e -- are otherwise missed
    when a broad, slightly higher plateau such as 'phi -> 0, beta -> g' (value T(g)) wins on the mesh); then a 2-d zoom
    around the best point found."""
    z = np.linspace(-16, 16, nz); l = np.concatenate([np.linspace(math.log(1e-13), math.log(0.5), nl - 24), np.log(np.linspace(0.52, 0.999999, 24))])
    Z, Lg = np.meshgrid(z, l, indexing="ij")
    val = V(T, g, 1 / (1 + np.exp(-Z)), np.exp(Lg) * g)
    best = float(val.min())
    bi, bj = np.unravel_index(int(np.argmin(val)), val.shape)
    bz, bl = z[bi], l[bj]
    # row-wise zoom (all beta rows at once)
    zc = z[np.argmin(val, axis=0)]                     # best z per beta
    hz = z[1] - z[0]
    u = np.linspace(-1, 1, 33)
    beta_row = (np.exp(l) * g)[:, None]
    for _ in range(zooms):
        zz = zc[:, None] + hz * u[None, :]
        v2 = V(T, g, 1 / (1 + np.exp(-zz)), np.broadcast_to(beta_row, zz.shape))
        k = np.argmin(v2, axis=1)
        zc = zz[np.arange(len(l)), k]
        hz /= 6.0
        m = float(v2.min())
        if m < best:
            best = m
            r = int(np.argmin(v2.min(axis=1)))
            bz, bl = zc[r], l[r]
    # 2-d zoom around the best point
    hz, hl = (z[1] - z[0]), 0.5
    for _ in range(zooms):
        zz = np.linspace(bz - hz, bz + hz, 33); ll = np.minimum(np.linspace(bl - hl, bl + hl, 33), math.log(0.9999999))
        Z2, L2 = np.meshgrid(zz, ll, indexing="ij")
        v2 = V(T, g, 1 / (1 + np.exp(-Z2)), np.exp(L2) * g)
        i2, j2 = np.unravel_index(int(np.argmin(v2)), v2.shape)
        if float(v2[i2, j2]) < best:
            best = float(v2[i2, j2])
        bz, bl, hz, hl = zz[i2], ll[j2], hz / 6, hl / 6
    return best


if len(sys.argv) > 2 and sys.argv[2] == "check":
    # consistency check of V against the brute-force sup over gamma of ralib (no shortcut), random (g, phi, beta)
    rng = np.random.default_rng(5)
    T = PLT(G(gs))
    worst = 0.0
    for _ in range(300):
        g = 10 ** rng.uniform(-5, -0.05); phi = 1 / (1 + math.exp(-rng.uniform(-6, 6))); beta = g * 10 ** rng.uniform(-8, -0.001)
        a_ = float(V(T, g, np.array([phi]), np.array([beta]))[0])
        b_ = bracket_sup_gamma(G, T, g, phi, beta, ngam=4000)[0]
        worst = max(worst, abs(a_ - b_))
    print("# check: max |V (range-max form) - brute-force sup over gamma| over 300 random (g, phi, beta) = %.2e" % worst)

dd = DualDyn(gauss_sig3, 1.0)
dd.step()
GR = (math.sqrt(5) - 1) / 2


def majorant(k, x):
    tau = dd.cuts[k - 1][3]
    Bs = np.unique(np.concatenate([np.linspace(0, tau, 1201), tau - tau * 10.0 ** np.linspace(-9, -1, 200)]))
    Sv = np.array([dd.S(k, float(B))[0] for B in Bs])
    out = []
    for xx in np.atleast_1d(x):
        v = Bs - Sv * xx
        i = int(np.argmax(v))
        lo, hi = Bs[max(i - 1, 0)], Bs[min(i + 1, len(Bs) - 1)]
        f = lambda B: B - dd.S(k, B)[0] * xx
        x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
        f1, f2 = f(x1), f(x2)
        for _ in range(45):
            if f1 >= f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - GR * (hi - lo); f1 = f(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + GR * (hi - lo); f2 = f(x2)
        out.append(max(float(v[i]), f1, f2))
    return np.array(out)


def lines_lb(k, x):
    Bs = np.linspace(0, 0.9999, 200001)
    p = np.zeros_like(Bs); ok = np.ones_like(Bs, dtype=bool)
    for _ in range(k):
        d = 1 - p - Bs
        ok &= d > 0
        p = np.where(ok, Bs * (1 - p) / np.where(ok, d, 1.0), np.inf)
    return np.array([float(np.max(np.where(ok, Bs - np.where(ok, p, 0) * xx, -np.inf))) for xx in np.atleast_1d(x)])


vals = G(gs)
print("# Gaussian pair; g-grid: %d points (%d geometric in [1e-8, 1e-2], %d uniform in [1e-2, 1])" % (NG, NGEO, NU))
t0 = time.time()
sel = [np.argmin(np.abs(gs - x)) for x in [1e-8, 5e-7, 3e-5, 5e-4, 1e-2, 7e-2, 0.2, 0.38, 0.63, 0.88]]
for k in range(2, KL + 1):
    T = PLT(vals)
    new = np.array([min(T.v[i], R_fine(T, float(g))) for i, g in enumerate(gs[:-1])] + [0.0])
    vals = np.minimum.accumulate(new)
    dd.step()
    Mk = majorant(k, gs); Lk = lines_lb(k, gs)
    d_up = vals - Mk; d_lo = vals - Lk
    i = int(np.argmax(d_up)); j = int(np.argmin(d_lo))
    print("# level %d (%.0f s): tau_k^UB = %.6f ; T_k(1e-8) = %.6f ; LB(1e-8) = %.6f | max_g (T_k - M_{S_k,tau_k}) = %+.2e at g = %.3g | min_g (T_k - LB_lines) = %+.2e at g = %.3g | max_g (M - T_k) = %.3e"
          % (k, time.time() - t0, dd.cuts[k - 1][3], vals[0], Lk[0], d_up[i], gs[i], d_lo[j], gs[j], float(np.max(Mk - vals))))
    print("    g:        " + "  ".join("%.2e" % gs[q] for q in sel))
    print("    LB lines: " + "  ".join("%.6f" % Lk[q] for q in sel))
    print("    T_k:      " + "  ".join("%.6f" % vals[q] for q in sel))
    print("    M_{S_k}:  " + "  ".join("%.6f" % Mk[q] for q in sel))
    sys.stdout.flush()
