"""The upper-bound dynamics of the level recursion in dual variables, Gaussian pair (coordinator's check; an
approximation on a grid, NOT one-sided - workstream R is asked for the certified version).

A convex majorant M of T_k with slopes in [-1, 0] is described by S(B) = the least slope of a line with intercept B
below M (convex, increasing, S(tau) <= 1 at the top intercept tau = M(0+)).  One level (duality for convex
majorants, Sion; then slopes capped at one; then the monotone hull = lower convex envelope in the (B, s) plane):
    tau' = root of S(B) = 1 - B/a          (the line that can just be dropped at accuracy zero),
    S~(B) = min(1, Sigma_B(S(B)))  for B < tau',   S~(tau') = 1,       S' = lower convex envelope of S~ on [0, tau'].
Gaussian pair: a = 1, h = 1/4, Sigma_B(s) = B (1 - s)/(1 - s - B).  Start: M_1 = hull(theta_na) = (1 - x)_+, S_1(B) = B.
Only intercepts B = h + delta > h are tracked (lines below h converge to the tangents of theta_hint and never
reach the dropping slope); the point delta = 0 is kept at the fixed slope 1/2.

Output: k, tau_k (upper-bound dynamics), k^2 (tau_k - h)/(pi^2/16), and the same for the lower bound from lines and
the grid recursion where stored.
"""
import math, os, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
a, h = 1.0, 0.25
CONST = math.pi ** 2 / 16


def lower_convex_envelope(x, y):
    """lower convex hull of the points (x_i, y_i), x increasing; returns the envelope evaluated at x."""
    hull = []
    for i in range(len(x)):
        while len(hull) >= 2:
            i1, i2 = hull[-2], hull[-1]
            if (y[i2] - y[i1]) * (x[i] - x[i1]) >= (y[i] - y[i1]) * (x[i2] - x[i1]):
                hull.pop()
            else:
                break
        hull.append(i)
    return np.interp(x, x[hull], y[hull])


def run(K, npts=40001):
    # delta-grid: geometric from 1e-10 to 0.75 (B up to a = 1), plus delta = 0
    d = np.concatenate([[0.0], np.exp(np.linspace(math.log(1e-10), math.log(0.75), npts))])
    B = h + d
    S = B.copy()                      # S_1(B) = B  (lines (s, s) of (1 - x)_+); at B = h the slope 1/4 < 1/2: it moves to 1/2
    tau = 1.0
    out = {1: tau}
    for k in range(2, K + 1):
        # top: root of S(B) = 1 - B/a on the current domain [h, tau]
        f = S - (1 - B / a)
        dom = B <= tau + 1e-15
        idx = np.where(dom & (f >= 0))[0]
        if len(idx) == 0:
            tau_new = tau
        else:
            j = idx[0]
            if j == 0:
                tau_new = B[0]
            else:
                t = f[j - 1] / (f[j - 1] - f[j])
                tau_new = B[j - 1] + t * (B[j] - B[j - 1])
        out[k] = tau_new
        # propagate the regular lines (B < tau_new), cap at one, add the point (tau_new, 1), convexify
        reg = B < tau_new
        Bn = np.concatenate([B[reg], [tau_new]])
        Sreg = S[reg]
        den = 1 - Sreg - B[reg]
        Sn = np.where(den > 1e-300, B[reg] * (1 - Sreg) / np.maximum(den, 1e-300), 1.0)
        Sn = np.minimum(1.0, np.maximum(Sn, Sreg))
        Sn = np.concatenate([Sn, [1.0]])
        env = lower_convex_envelope(Bn, Sn)
        # back to the fixed grid (beyond tau_new the values are irrelevant)
        S = np.interp(B, Bn, env, right=1.0)
        tau = tau_new
    return out


def grid_values(fname):
    o = {}
    p = os.path.join(HERE, fname)
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r"^(\d+) (\d\.\d+) ", line)
            if m:
                o[int(m.group(1))] = float(m.group(2))
    return o


def lb(k):
    def angle(Bv):
        rt = math.sqrt(4 * Bv - 1)
        return (k - 1) * math.atan2(rt, 1 - 2 * Bv) + math.atan2((1 - Bv) * rt, 1 - 3 * Bv)
    lo, hi = 0.25 + 1e-15, 0.5 - 1e-12
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if angle(mid) < math.pi else (lo, mid)
    return lo


K = 320
ub = run(K)
gv = grid_values("out_iterate_gauss_160.txt")
print("# Gaussian pair; constant pi^2/16 = %.6f" % CONST)
print("#   k   tau^LB (lines)   tau (grid recursion)   tau^UB (dual dynamics)   k^2(.-h)/const:  LB      grid     UB")
for k in list(range(2, 13)) + [15, 20, 30, 40, 55, 80, 100, 120, 160, 240, 320]:
    g = gv.get(k)
    print("  %4d   %.10f   %s   %.10f     %.5f  %s  %.5f" % (
        k, lb(k), ("%.10f" % g) if g else "     -      ", ub[k], k * k * (lb(k) - h) / CONST,
        ("%.5f" % (k * k * (g - h) / CONST)) if g else "   -   ", k * k * (ub[k] - h) / CONST))
