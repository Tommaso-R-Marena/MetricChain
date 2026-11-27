#!/usr/bin/env python3
"""RA07 -- Proposition A8 at the third level, on the operator R itself (approximate, floating point, grids).

  T_2 = min(theta, R[theta]) on a grid of rates (R[theta] minimised over (phi, beta) on meshes with zooms: every mesh
  point gives an upper bound, so the computed T_2 is an upper bound for T_2 up to rounding);
  T_3(g) = min(T_2, R[T_2])(g) at a few rates g > 0, and tau_3 = T_3(0+) = inf_phi sup_{gamma >= 0} [min(gamma, phi a) + (1 - phi) T_2(gamma/(1 - phi))]
  (the formula of the theory report, remark after 11.58), with T_2 interpolated between grid points (linearly in sqrt x:
  T_2 has a square-root singularity at 0) -- this interpolation is the uncontrolled part.
  Compared with M_{W_3, b_3}(g) and b_3 of the referee's envelope sequence (Proposition A8: T_3 <= M_{W_3, b_3}, tau_3 <= b_3).
Usage: python3 -B ra07_tau3.py [pair]      pair in {gauss, cube1}; default gauss
"""
import math
import sys

import numpy as np

import ra_lib as R

which = sys.argv[1] if len(sys.argv) > 1 else "gauss"
P = (R.Gauss() if which == "gauss" else R.Cube(float(which[4:]))).setup()
a, h, es = P.a, P.h, P.epsstar
S = R.EnvSeq(P, 4)
print("# %s: a = %.8f, h = %.8f;  b_2/a = %.8f, b_3/a = %.8f, b_4/a = %.8f" % (P.name, a, h, S.b[2] / a, S.b[3] / a, S.b[4] / a))

if which == "gauss":
    def theta(e):
        e = np.asarray(e, dtype=float)
        return np.where(e < 1.0, (1.0 - np.sqrt(np.minimum(e, 1.0))) ** 2, 0.0)
else:
    pu = P.pu

    def klv(x, y):
        return x * np.log(x / y) + (1 - x) * np.log((1 - x) / (1 - y))

    def theta(e):
        e = np.asarray(e, dtype=float)
        lo = np.full(e.shape, pu)
        hi = np.full(e.shape, 0.5)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            ok = klv(mid, pu) <= e
            lo = np.where(ok, mid, lo)
            hi = np.where(ok, hi, mid)
        return np.where(e >= es, 0.0, klv(0.5 * (lo + hi), 0.5))


def R_theta(g, nmesh=49, zooms=7):
    """upper bound for R[theta](g): mesh over (phi, beta/g) with zooms; theta convex: sup over gamma at gamma in {beta, mu}"""
    plo, phi_hi, blo, bhi = 1e-4, 1.0 - 1e-4, 1e-6, 1.0 - 1e-6
    best = (math.inf, 0.5, 0.5)
    for _ in range(zooms):
        ps = np.linspace(plo, phi_hi, nmesh)[:, None]
        bs = (np.linspace(blo, bhi, nmesh) * g)[None, :]
        om = 1.0 - ps
        mu = ps * theta((g - bs) / ps)
        vb = bs + om * theta(bs / om)
        vm = mu + om * theta(mu / om)
        val = np.where(bs >= mu, mu + om * theta(bs / om), np.maximum(vb, vm))
        k = np.unravel_index(int(np.argmin(val)), val.shape)
        if val[k] < best[0]:
            best = (float(val[k]), float(ps[k[0], 0]), float(bs[0, k[1]] / g))
        dp, db = (phi_hi - plo) / 8.0, (bhi - blo) / 8.0
        plo, phi_hi = max(1e-6, best[1] - dp), min(1.0 - 1e-6, best[1] + dp)
        blo, bhi = max(1e-9, best[2] - db), min(1.0 - 1e-9, best[2] + db)
    return best[0]


# T_2 on the grid x_i = es (i/N)^2
N = 1200
sq = np.linspace(0.0, 1.0, N + 1)
xg = es * sq ** 2
T2 = np.zeros(N + 1)
T2[0] = S.b[2]                      # tau_2 = b_2 (closed form of the theory report; checked in ra04)
th = theta(xg)
for i in range(1, N + 1):
    T2[i] = min(float(th[i]), R_theta(float(xg[i])))
T2 = np.minimum.accumulate(T2)     # nonincreasing (it is; this only removes search noise)
print("T_2 on %d rates;  T_2(0+)/a = %.6f, T_2 at the first grid point (x = %.2e h): %.6f a;  max over the grid of (T_2 - M_{W_2,b_2})/a = %.2e"
      % (N, T2[0] / a, xg[1] / h, T2[1] / a, max((T2[i] - S.M(2, float(xg[i]))[0]) / a for i in range(1, N + 1))))


def T2f(x):
    """T_2 at arbitrary rates: linear interpolation in sqrt(x); 0 beyond eps*"""
    x = np.asarray(x, dtype=float)
    return np.where(x >= es, 0.0, np.interp(np.sqrt(np.minimum(x, es) / es), sq, T2))


# tau_3 = inf_phi sup_{0 <= gamma <= phi a} [gamma + (1 - phi) T_2(gamma/(1 - phi))]   (beyond phi a the bracket decreases)
def sup_gamma0(phi, ng=20001):
    gam = phi * a * np.linspace(0.0, 1.0, ng) ** 2
    return float(np.max(gam + (1.0 - phi) * T2f(gam / (1.0 - phi))))


phis = np.linspace(0.02, 0.98, 481)
vals = np.array([sup_gamma0(p) for p in phis])
k = int(np.argmin(vals))
lo, hi = phis[max(k - 1, 0)], phis[min(k + 1, len(phis) - 1)]
for _ in range(60):
    m1 = hi - R.GOLD * (hi - lo)
    m2 = lo + R.GOLD * (hi - lo)
    if sup_gamma0(m1) > sup_gamma0(m2):
        lo = m1
    else:
        hi = m2
tau3 = min(float(vals[k]), sup_gamma0(0.5 * (lo + hi)))
print("tau_3 (approximate) = %.6f a at phi = %.4f;   b_3 = %.6f a;   tau_3 - b_3 = %.2e a   (Proposition A8: <= 0)"
      % (tau3 / a, 0.5 * (lo + hi), S.b[3] / a, (tau3 - S.b[3]) / a))
if which == "gauss":
    print("   (Gaussian pair: b_3 = 5/14 = %.6f; lower bounds of R_REPORT: 1/(2 sqrt 2) = %.6f, B_inf(3) = %.6f)" % (5 / 14, 1 / (2 * math.sqrt(2)), 0.307978528))
else:
    print("   (cube u = 1: the theory report quotes tau_3 = 0.361 a)")


# T_3 at positive rates: R[T_2](g) over (phi, beta); sup over gamma in [beta, max(beta, mu)] on a grid.
# The minimiser can sit at phi close to 1 with beta/g tiny (large g) or at phi -> 0, beta -> g (the trivial R[T](g) <= T(g-)):
# the first pass uses a mesh that is fine at both ends (phi linear and 1 - phi logarithmic; beta/g linear and logarithmic).
def R_T2(g, ng=401):
    s = np.linspace(0.0, 1.0, ng)[None, :] ** 2

    def scan(ps, bfs):
        best = (math.inf, 0.5, 0.5)
        bs = (bfs * g)[:, None]
        for p in ps:
            om = 1.0 - p
            mu = p * theta((g - bs) / p)
            top = np.maximum(bs, mu)
            gam = bs + (top - bs) * s
            val = np.max(np.minimum(gam, mu) + om * T2f(gam / om), axis=1)
            k = int(np.argmin(val))
            if val[k] < best[0]:
                best = (float(val[k]), float(p), float(bfs[k]))
        return best

    ps = np.unique(np.concatenate((np.linspace(0.005, 0.995, 100), 1.0 - np.exp(np.linspace(math.log(1e-4), math.log(0.2), 60)))))
    bfs = np.unique(np.concatenate((np.linspace(0.01, 0.999, 50), np.exp(np.linspace(math.log(1e-9), math.log(0.05), 50)))))
    best = scan(ps, bfs)
    wp, wb = 0.02, 2.0                     # zoom: phi +- wp (in 1 - phi relative terms), beta/g within a factor wb
    for _ in range(6):
        omb = 1.0 - best[1]
        ps = 1.0 - np.clip(omb * np.exp(np.linspace(-wp * 10, wp * 10, 41)), 1e-6, 1.0 - 1e-6)
        bfs = np.clip(best[2] * np.exp(np.linspace(-math.log(wb), math.log(wb), 41)), 1e-12, 1.0 - 1e-9)
        cand = scan(ps, bfs)
        if cand[0] < best[0]:
            best = cand
        wp, wb = wp / 2.0, math.sqrt(wb)
    return best


print("#   g/h       T_2(g)/a     R[T_2](g)/a    T_3(g)/a     M_{W_3,b_3}(g)/a    (T_3 - M_3)/a     phi      beta/g")
worst = -math.inf
for gh in (0.001, 0.01, 0.03, 0.1, 0.3, 1.0, 2.0, 3.0):
    g = gh * h
    v, p, bf = R_T2(g)
    t2 = float(T2f(g))
    T3 = min(t2, v)
    M3 = S.M(3, g)[0]
    worst = max(worst, (T3 - M3) / a)
    print("  %7.3f    %.6f     %.6f      %.6f     %.6f          %10.3e      %.4f   %.3e" % (gh, t2 / a, v / a, T3 / a, M3 / a, (T3 - M3) / a, p, bf))
print("max of (T_3 - M_{W_3,b_3})/a at these rates: %.3e   (Proposition A8 at j = 3: <= 0 up to the accuracy of the grids)" % worst)
