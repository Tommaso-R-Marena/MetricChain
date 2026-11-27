#!/usr/bin/env python3
"""RA07b -- tau_3 again, more carefully (the author's z7_exactness.py, written while this review was in progress,
reports tau_3 = 0.361296 a at u = 1; ra07_tau3.py gave 0.361184 a: the two differ in the fourth digit).

tau_3 = inf_phi sup_gamma [min(gamma, phi a) + (1 - phi) T_2(gamma/(1 - phi))]
      = inf_{x > 0} a S(x)/(a + x),      S(x) := sup_{0 <= y <= x} (y + T_2(y))            (x = phi a/(1 - phi), y = gamma/(1 - phi)).
S(0+) = tau_2, and S(x) = tau_2 as long as y + T_2(y) <= tau_2 on (0, x]; so the candidates for the infimum are the first
point x* with x* + T_2(x*) = tau_2 (value a tau_2/(a + x*)) and interior minima beyond it.
T_2(x) = min(theta(x), R[theta](x)) is computed at single rates by a careful minimisation over (phi, beta): a two-ended
first mesh (phi linear and 1 - phi logarithmic; beta/x linear and logarithmic, 400 x 300 points) and 10 zooms of 81 x 81.
Every (phi, beta) is an upper bound of R[theta](x), so the computed T_2 is >= T_2; the root x* is then too large and
the value a tau_2/(a + x*) too SMALL if the minimisation is incomplete -- so the larger of two honest computations is
the more complete one only if ... (see the output: the script also prints how T_2(x) moves with the effort).
Usage: python3 -B ra07b_tau3_precise.py [pair]      pair in {cube1, gauss}; default cube1
"""
import math
import sys

import numpy as np

import ra_lib as R

which = sys.argv[1] if len(sys.argv) > 1 else "cube1"
P = (R.Gauss() if which == "gauss" else R.Cube(float(which[4:]))).setup()
a, h, es = P.a, P.h, P.epsstar
S = R.EnvSeq(P, 4)
tau2 = S.b[2]

if which == "gauss":
    def theta(e):
        e = np.asarray(e, dtype=float)
        return np.where(e < 1.0, (1.0 - np.sqrt(np.clip(e, 0.0, 1.0))) ** 2, 0.0)
else:
    pu = P.pu

    def klv(x, y):
        return x * np.log(x / y) + (1 - x) * np.log((1 - x) / (1 - y))

    def theta(e):
        e = np.asarray(e, dtype=float)
        lo = np.full(e.shape, pu)
        hi = np.full(e.shape, 0.5)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            ok = klv(mid, pu) <= e
            lo = np.where(ok, mid, lo)
            hi = np.where(ok, hi, mid)
        return np.where(e >= es, 0.0, klv(0.5 * (lo + hi), 0.5))


def bracket(g, ps, bfs):
    """the bracket of R at (phi, beta = bf g) for T = theta, on the mesh ps x bfs"""
    ps = ps[:, None]
    bs = (bfs * g)[None, :]
    om = 1.0 - ps
    mu = ps * theta((g - bs) / ps)
    vb = bs + om * theta(bs / om)
    vm = mu + om * theta(mu / om)
    return np.where(bs >= mu, mu + om * theta(bs / om), np.maximum(vb, vm))


def R_theta(g, effort=2):
    n1, n2, nz, zooms = {0: (60, 40, 31, 5), 1: (150, 100, 41, 7), 2: (400, 300, 81, 10)}[effort]
    ps = np.unique(np.concatenate((np.linspace(0.002, 0.998, n1), 1.0 - np.exp(np.linspace(math.log(1e-5), math.log(0.2), n1 // 3)))))
    bfs = np.unique(np.concatenate((np.linspace(0.002, 0.999, n2), np.exp(np.linspace(math.log(1e-10), math.log(0.02), n2 // 2)))))
    val = bracket(g, ps, bfs)
    k = np.unravel_index(int(np.argmin(val)), val.shape)
    best = (float(val[k]), float(ps[k[0]]), float(bfs[k[1]]))
    wp, wb = 0.3, 3.0
    for _ in range(zooms):
        omb = 1.0 - best[1]
        ps = 1.0 - np.clip(omb * np.exp(np.linspace(-wp, wp, nz)), 1e-9, 1.0 - 1e-9)
        ps = np.unique(np.concatenate((ps, np.clip(best[1] * np.exp(np.linspace(-wp, wp, nz)), 1e-9, 1.0 - 1e-9))))
        bfs = np.unique(np.clip(best[2] * np.exp(np.linspace(-math.log(wb), math.log(wb), nz)), 1e-14, 1.0 - 1e-12))
        val = bracket(g, ps, bfs)
        k = np.unravel_index(int(np.argmin(val)), val.shape)
        if val[k] < best[0]:
            best = (float(val[k]), float(ps[k[0]]), float(bfs[k[1]]))
        wp, wb = wp / 2.2, wb ** (1 / 2.2)
    return best


def T2(x, effort=2):
    v, p, bf = R_theta(x, effort)
    return min(float(theta(x)), v), p, bf


print("# %s: a = %.10f, h = %.10f, tau_2 = b_2 = %.10f a" % (P.name, a, h, tau2 / a))
print("# how T_2 moves with the effort of the minimisation (three efforts) at a few rates:")
for xh in (0.3, 1.4, 1.5):
    vals = [T2(xh * h, e) for e in (0, 1, 2)]
    print("   x = %.2f h:  T_2/a = %.9f  %.9f  %.9f   (phi = %.5f, beta/x = %.3e at the highest effort);  (x + T_2(x))/a = %.9f"
          % (xh, vals[0][0] / a, vals[1][0] / a, vals[2][0] / a, vals[2][1], vals[2][2], (xh * h + vals[2][0]) / a))

# the first root of x + T_2(x) = tau_2   (scan at the lowest effort, bisection at the middle one, a check at the highest)
xs = np.linspace(0.02, 3.0, 75) * h
fv = np.array([x + T2(x, 0)[0] - tau2 for x in xs])
neg = fv < 0
i0 = int(np.argmax(~neg & (np.arange(len(xs)) > int(np.argmax(neg)))))      # first index after the first negative one where f >= 0
print("# y + T_2(y) - tau_2 on 75 rates in [0.02h, 3h]: negative on [%.3f h, %.3f h], first sign change to >= 0 at %.3f h; max of (y + T_2(y) - tau_2)/a before it: %.3e"
      % (xs[int(np.argmax(neg))] / h, xs[i0 - 1] / h, xs[i0] / h, float(np.max(fv[:i0])) / a))
lo, hi = xs[i0 - 1], xs[i0]
for _ in range(34):
    mid = 0.5 * (lo + hi)
    if mid + T2(mid, 1)[0] - tau2 < 0:
        lo = mid
    else:
        hi = mid
xstar = 0.5 * (lo + hi)
cand = a * tau2 / (a + xstar)
res2 = xstar + T2(xstar, 2)[0] - tau2
d = 1e-3 * h
slope = (T2(xstar + d, 1)[0] - T2(xstar - d, 1)[0]) / (2 * d)
print("x* = %.8f h = %.8f a;   a tau_2/(a + x*) = %.8f a;   residual of x + T_2(x) - tau_2 at x* with the highest effort: %.2e a;   T_2'(x*) = %.4f"
      % (xstar / h, xstar / a, cand / a, res2 / a, slope))
# beyond x*: S(x) = max over y <= x of (y + T_2(y)); the function a S(x)/(a + x) on a grid beyond x*
xs2 = np.linspace(xstar, 4.0 * h, 40)
Sx, best = tau2, cand
for x in xs2[1:]:
    Sx = max(Sx, x + T2(x, 0)[0])
    best = min(best, a * Sx / (a + x))
print("minimum of a S(x)/(a + x) over 40 rates in [x*, 4h]: %.8f a   (so the infimum is at x*: %s)" % (best / a, best >= cand - 1e-12))
print("tau_3 = %.6f a;   b_3 = %.6f a;   b_3 - tau_3 = %.3e a;   the optimal outer fraction phi = x*/(a + x*) = %.4f"
      % (cand / a, S.b[3] / a, (S.b[3] - cand) / a, xstar / (a + xstar)))
print("   (ra07_tau3.py, with T_2 interpolated from 1200 rates: 0.361184 a (cube), 0.355233 (Gaussian);  the author's z7_exactness.py: 0.361296 a (cube))")
if which != "gauss":
    print("   tau_3 = 0.361296 a would need x* = %.5f h, i.e. T_2 larger by %.2e a at that rate than computed here"
          % (a * (tau2 / (0.361296 * a) - 1.0) / h, (tau2 - a * (tau2 / (0.361296 * a) - 1.0) - T2(a * (tau2 / (0.361296 * a) - 1.0), 1)[0]) / a))
    print("   (1 - 0.278) tau_2 = %.6f a: the value on a phi-grid of step 0.001 at the grid point next to the kink phi* = %.5f"
          % ((1 - 0.278) * tau2 / a, xstar / (a + xstar)))
