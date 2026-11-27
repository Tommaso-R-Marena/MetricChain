"""Referee A, test 8: Corollary E (section 8b of the report as revised at commit 9626e4f, added after my brief):
for theta with |theta'(0+)| <= 1,   T_k(x) = sup{B - p_k(B) x : p_k(B) < infinity}   for all k and x.

The recursion itself on a grid (same method as a4b_recursion_fine.py: exact sup over gamma for the piecewise-linear
interpolant using only monotonicity of T_k; inf over (phi, beta) by mesh + row-wise zoom + 2-d zoom), for
theta = a exp(-e/c).  Beyond the grid, T_k(x) is replaced by min(T_k(x_max), theta(x)) (an upper bound).
Compared with the Legendre transform of the orbit curve p_k (own slope map, smooth.py).
Usage: python3 a8_corollaryE.py a c [levels]      (slope at zero = a/c)
"""
import sys, math, time
import numpy as np
from smooth import make

A = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
C = float(sys.argv[2]) if len(sys.argv) > 2 else 1.25
KL = int(sys.argv[3]) if len(sys.argv) > 3 else 6
P = make("expo:%g:%g:0" % (A, C))
theta = lambda e: A * np.exp(-np.asarray(e, dtype=float) / C)
XMAX = 14 * C
gs = np.unique(np.concatenate([np.exp(np.linspace(math.log(1e-8), math.log(1e-2), 110)), np.linspace(1e-2, XMAX, 700)]))
NG = len(gs)


class PLT:
    def __init__(self, vals):
        self.v = np.minimum.accumulate(np.asarray(vals, dtype=float))
        self.S = gs + self.v
        tab = [self.S]; k = 1
        while 2 * k <= NG:
            prev = tab[-1]
            tab.append(np.maximum(prev[:NG - 2 * k + 1], prev[k:NG - k + 1])); k *= 2
        self.tab = tab

    def T(self, x):
        x = np.asarray(x, dtype=float)
        return np.where(x > XMAX, np.minimum(self.v[-1], theta(x)), np.interp(x, gs, self.v))

    def rangemaxS(self, lo, hi):
        out = np.maximum(lo + self.T(lo), hi + self.T(hi))
        i0 = np.searchsorted(gs, lo, side="left"); i1 = np.searchsorted(gs, hi, side="right") - 1
        ok = i1 >= i0
        if np.any(ok):
            a0, a1 = i0[ok], i1[ok]
            k = np.floor(np.log2(a1 - a0 + 1)).astype(int)
            res = np.empty(len(a0))
            for kk in np.unique(k):
                sel = k == kk
                t = self.tab[kk]
                res[sel] = np.maximum(t[a0[sel]], t[a1[sel] - (1 << kk) + 1])
            out[ok] = np.maximum(out[ok], res)
        return out


def V(T, g, phi, beta):
    mu = phi * theta((g - beta) / phi)
    one = 1.0 - phi
    lo = beta / one; hi = np.maximum(beta, mu) / one
    return np.where(beta <= mu, one * T.rangemaxS(lo, hi), mu + one * T.T(lo))


def R_fine(T, g, nz=600, nl=64, zooms=5):
    z = np.linspace(-16, 16, nz); l = np.concatenate([np.linspace(math.log(1e-13), math.log(0.5), nl - 20), np.log(np.linspace(0.52, 0.999999, 20))])
    Z, Lg = np.meshgrid(z, l, indexing="ij")
    val = V(T, g, 1 / (1 + np.exp(-Z)), np.exp(Lg) * g)
    best = float(val.min())
    bi, bj = np.unravel_index(int(np.argmin(val)), val.shape)
    bz, bl = z[bi], l[bj]
    zc = z[np.argmin(val, axis=0)]; hz = z[1] - z[0]; u = np.linspace(-1, 1, 33)
    beta_row = (np.exp(l) * g)[:, None]
    for _ in range(zooms):
        zz = zc[:, None] + hz * u[None, :]
        v2 = V(T, g, 1 / (1 + np.exp(-zz)), np.broadcast_to(beta_row, zz.shape))
        k = np.argmin(v2, axis=1); zc = zz[np.arange(len(l)), k]; hz /= 6.0
        m = float(v2.min())
        if m < best:
            best = m; r = int(np.argmin(v2.min(axis=1))); bz, bl = zc[r], l[r]
    hz, hl = (z[1] - z[0]), 0.5
    for _ in range(zooms):
        zz = np.linspace(bz - hz, bz + hz, 33); ll = np.minimum(np.linspace(bl - hl, bl + hl, 33), math.log(0.9999999))
        Z2, L2 = np.meshgrid(zz, ll, indexing="ij")
        v2 = V(T, g, 1 / (1 + np.exp(-Z2)), np.exp(L2) * g)
        i2, j2 = np.unravel_index(int(np.argmin(v2)), v2.shape)
        best = min(best, float(v2[i2, j2]))
        bz, bl, hz, hl = zz[i2], ll[j2], hz / 6, hl / 6
    return best


def legendre(k, x):
    """sup{B - p_k(B) x : p_k(B) < inf} on a B-grid of [0, a] (vectorised orbit), refined near the end of the finite range."""
    Bs = np.linspace(0, A, 20001)
    for rnd in range(3):
        p = np.zeros_like(Bs)
        for _ in range(k):
            fin = np.isfinite(p)
            S = P.sig3(Bs, np.where(fin, p, 2.0))[0]
            p = np.where(fin, S, np.inf)
        fin = np.isfinite(p)
        bmax = Bs[fin].max()
        if rnd < 2:
            Bs = np.unique(np.concatenate([Bs, np.linspace(max(0, bmax - 2 * A / 20000 / (50 ** rnd)), min(A, bmax + 2 * A / 20000 / (50 ** rnd)), 2001)]))
    out = np.array([float(np.max(Bs[fin] - p[fin] * xx)) for xx in np.atleast_1d(x)])
    return out, bmax


print("# theta = %g exp(-e/%g): a = %g, slope at zero = %g, h = %.6f ; g-grid %d points in [1e-8, %g]" % (A, C, A, A / C, P.h, NG, XMAX))
vals = theta(gs)
t0 = time.time()
sel = [np.argmin(np.abs(gs - x)) for x in [1e-8, 1e-4, 1e-2, 0.1, 0.3, 0.7, 1.5, 3.0]]
for k in range(2, KL + 1):
    T = PLT(vals)
    new = np.array([min(T.v[i], R_fine(T, float(g))) for i, g in enumerate(gs)])
    vals = np.minimum.accumulate(new)
    Lk, bmax = legendre(k, gs)
    d = vals - Lk
    i = int(np.argmax(np.abs(d)))
    print("# level %d (%.0f s): B_inf(k) = %.6f ; T_k(1e-8) = %.6f ; max_g |T_k - Legendre(p_k)| = %.2e (signed %+.2e at g = %.3g, T = %.6f) ; min_g (T_k - Legendre) = %+.2e"
          % (k, time.time() - t0, bmax, vals[0], abs(d[i]), d[i], gs[i], vals[i], float(d.min())))
    print("    g:        " + "  ".join("%.2e" % gs[q] for q in sel))
    print("    Legendre: " + "  ".join("%.6f" % Lk[q] for q in sel))
    print("    T_k:      " + "  ".join("%.6f" % vals[q] for q in sel))
    sys.stdout.flush()
