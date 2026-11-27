"""Referee A, test 4: the recursion itself (brute force on R, level by level, on a grid of accuracies) against the
majorants M_{S_k, tau_k} of the exact dynamics of convex majorants (Proposition U + Corollary U', iterated from T_1).

Gaussian pair.  T_1 = theta exactly; T_{k+1}(g) = min(T_k(g), R_bf[T_k](g)) on a geometric g-grid, T_k interpolated
linearly in ln g (constant below the grid, 0 above e = 1).  R_bf = min over a (phi, beta)-grid (+ refinement) of the
brute-force sup over gamma: an UPPER estimate of R[T_k](g) (up to interpolation), so 'T_k^bf <= M + tol' is a
conservative test of  T_k <= M_{S_k, tau_k}.  Also printed: the lower bound from minorant lines, sup_B (B - p_k(B) g).
Usage: python3 a4_recursion_vs_majorant.py [levels] [ngrid]
"""
import math, sys, time
import numpy as np
from ralib import Gauss, R_bruteforce
from dual_dyn import DualDyn, gauss_sig3

KL = int(sys.argv[1]) if len(sys.argv) > 1 else 5
NG = int(sys.argv[2]) if len(sys.argv) > 2 else 36
G = Gauss()
gs = np.exp(np.linspace(math.log(1e-6), math.log(0.9), NG))
lg = np.log(gs)


def interp_T(vals):
    def T(x):
        x = np.asarray(x, dtype=float)
        out = np.interp(np.log(np.maximum(x, 1e-300)), lg, vals)
        return np.where(x >= 1.0, 0.0, out)
    return T


dd = DualDyn(gauss_sig3, 1.0)
dd.step()                                   # S_1, tau_1 = 1


def majorant(k, x):
    """M_{S_k, tau_k}(x) = max_B (B - S_k(B) x): B-grid on [0, tau_k], then golden section (concave in B)."""
    tau = dd.cuts[k - 1][3]
    Bs = np.concatenate([np.linspace(0, tau, 1501), tau - tau * 10.0 ** np.linspace(-9, -1, 200)])
    Bs = np.unique(Bs)
    Sv = np.array([dd.S(k, float(B))[0] for B in Bs])
    out = []
    GR = (math.sqrt(5) - 1) / 2
    for xx in np.atleast_1d(x):
        v = Bs - Sv * xx
        i = int(np.argmax(v))
        lo, hi = Bs[max(i - 1, 0)], Bs[min(i + 1, len(Bs) - 1)]
        f = lambda B: B - dd.S(k, B)[0] * xx
        x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
        f1, f2 = f(x1), f(x2)
        for _ in range(50):
            if f1 >= f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - GR * (hi - lo); f1 = f(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + GR * (hi - lo); f2 = f(x2)
        out.append(max(float(v[i]), f1, f2))
    return np.array(out)


def lines_lb(k, x):
    """sup_B (B - p_k(B) x): orbit of the flat line, k steps of the Moebius map (Proposition A)."""
    Bs = np.linspace(0, 0.999, 20000)
    p = np.zeros_like(Bs); ok = np.ones_like(Bs, dtype=bool)
    for _ in range(k):
        d = 1 - p - Bs
        ok &= d > 0
        p = np.where(ok, Bs * (1 - p) / np.where(ok, d, 1.0), np.inf)
    return np.array([float(np.max(np.where(ok, Bs - np.where(ok, p, 0) * xx, -np.inf))) for xx in np.atleast_1d(x)])


Tvals = G(gs)                               # T_1 = theta
M1 = majorant(1, gs)
print("# Gaussian pair; g-grid %d points in [1e-6, 0.9]" % NG)
print("# level 1: max (T_1 - M_{S_1})  = %+.2e   (T_1 = theta <= (1 - x)_+)" % float(np.max(Tvals - M1)))
t0 = time.time()
for k in range(2, KL + 1):
    T = interp_T(Tvals)
    new = np.array([min(Tvals[i], R_bruteforce(G, T, float(g), nphi=110, nbeta=18, ngam=140)) for i, g in enumerate(gs)])
    Tvals = new
    dd.step()
    Mk = majorant(k, gs)
    Lk = lines_lb(k, gs)
    i = int(np.argmax(Tvals - Mk))
    print("# level %d (%.0f s): tau_k^UB = %.6f ; T_k^bf(1e-6) = %.6f ; lines LB at 1e-6 = %.6f ; max_g (T_k^bf - M_{S_k,tau_k}) = %+.3e at g = %.2e ; "
          "min_g (M - T_k^bf) / max = %.3e / %.3e ; min_g (T_k^bf - LB) = %+.3e"
          % (k, time.time() - t0, dd.cuts[k - 1][3], Tvals[0], Lk[0], float((Tvals - Mk)[i]), gs[i], float(np.min(Mk - Tvals)),
             float(np.max(Mk - Tvals)), float(np.min(Tvals - Lk))))
    sel = [0, NG // 6, NG // 3, NG // 2, 2 * NG // 3, 5 * NG // 6, NG - 1]
    print("    g:        " + "  ".join("%.3e" % gs[j] for j in sel))
    print("    LB lines: " + "  ".join("%.6f " % Lk[j] for j in sel))
    print("    T_k^bf:   " + "  ".join("%.6f " % Tvals[j] for j in sel))
    print("    M_{S_k}:  " + "  ".join("%.6f " % Mk[j] for j in sel))
    sys.stdout.flush()
