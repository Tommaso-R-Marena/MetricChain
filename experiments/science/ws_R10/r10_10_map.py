"""r10_10: for which (p,u) is each direction of the headline PROVED?  Own code.

For every (p,u): cube values; lower bounds for the chain that hold for every n and every
algorithm (families of site-wise labels: Proposition H = tilted Markov labels; block fields =
Proposition I with the two uniform fields on blocks of any length); the cheap rigorous upper
bound of Proposition F with L = 1 (closed site problem).  "RAISED" is printed when a lower
bound exceeds the cube's value; an upper bound below the cube would print "LOWERED".

Numerical safeguards: the operator for the moment Lyapunov exponents is evaluated with N = 48
and N = 96 nodes; a pair is used only if both agree to 1e-7.
usage: python3 r10_10_map.py [h] [a]
"""
import sys
import time
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from r10lib import *
from r10_lyap import G_inf
from r10_blockfield import joint_first_last_m, blockfield_bound
from r10_06_markov_recursion import ustar

t0 = time.time()
ps = [0.45, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01]
us = [0.05, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0]


def G_checked(t, c, p, u):
    a = G_inf(t, c, p, u, N=48)
    b = G_inf(t, c, p, u, N=96)
    return a if abs(a - b) < 1e-7 else -np.inf


def lowerH(p, u):
    """max over (t,c) of Prop. H."""
    best = (-np.inf, None, None)
    for tstart in (0.45, 0.3, 0.15):
        for cstart in (0.0, 0.5, 1.0):
            r = minimize(lambda v: -G_inf(min(max(v[0], 0.02), 0.98), max(v[1], 0.0), p, u), (tstart, cstart),
                         method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-11))
            tt, cc = min(max(r.x[0], 0.02), 0.98), max(r.x[1], 0.0)
            v = G_checked(tt, cc, p, u)
            if v > best[0]:
                best = (v, tt, cc)
    return best


def lowerB(p, u, Lmax=40):
    best = (-np.inf, None, None)
    for L in range(1, Lmax + 1):
        f = joint_first_last_m(L, p)
        tb, vb = golden_max(lambda t: blockfield_bound(p, u, L, t, f)[0], 0.03, 0.97, tol=1e-4)
        # check the operator with more nodes
        v2 = blockfield_bound(p, u, L, tb, f, N=96)[0]
        if abs(v2 - vb) < 1e-7 and vb > best[0]:
            best = (vb, L, tb)
        if best[1] is not None and L > best[1] + 8:
            break
    return best


def upperDP1(p, u):
    us_ = ustar(p, u)
    hh = us_ / 2
    # two-letter site with law (1-p, p) and slope u*: vertices +-hh; closed solver
    W, _ = gibbs(np.array([1 - p, p]), np.array([[0.0, us_], [0.0, -us_]]))
    low = lambda t: renyi_bracket(W, t, tol=1e-12)["upper"]
    tb, vb = golden_max(low, 0.02, 0.98, tol=1e-6)
    return vb, capacity_bracket(W, tol=1e-12)["upper"], threshold_bracket(W, tol=1e-12)["upper"]


print("columns: cube | lower bounds (Prop. H: tilted Markov labels; block fields) | upper bound (Prop. F, L=1) | verdict")
print("%-5s %-5s | %-9s %-9s %-9s | %-32s %-28s | %-9s | %-10s | %-8s %-9s" % (
    "p", "u", "h_cube", "a_cube", "E_cube", "h >= (Prop. H; t, c)", "h >= (block field; L, t)", "h <= DP1", "h verdict", "E_F/E_c", "E<=DP1/E_c"))
rows = []
for p in ps:
    for u in us:
        hc, tc, ac, Ec = cube_exponents(u)
        H = lowerH(p, u)
        B = lowerB(p, u)
        hu, au, eu = upperDP1(p, u)
        lo = max(H[0], B[0])
        verdict = "RAISED" if lo > hc * (1 + 1e-6) else ("LOWERED" if hu < hc * (1 - 1e-6) else "undecided")
        rows.append((p, u, hc, lo, hu, verdict))
        print("%-5g %-5g | %.6f  %.6f  %.6f  | %.6f (%.3f, %.3f) x%.3f   %.6f (%2d, %.3f) x%.3f | %.6f x%.3f | %-10s | %.3f    %.3f   (%.0fs)" % (
            p, u, hc, ac, Ec, H[0], H[1], H[2], H[0] / hc, B[0], B[1], B[2], B[0] / hc, hu, hu / hc, verdict,
            E_F(p, u) / Ec, eu / Ec, time.time() - t0), flush=True)
print("\nverdict matrix for h (rows p, columns u = %s):" % us)
for p in ps:
    print("  p=%-5g " % p + "  ".join("%-9s" % r[5] for r in rows if r[0] == p))
print("ratio (best lower bound)/cube for h:")
for p in ps:
    print("  p=%-5g " % p + "  ".join("%-9.3f" % (r[3] / r[2]) for r in rows if r[0] == p))
print("ratio (upper bound DP L=1)/cube for h:")
for p in ps:
    print("  p=%-5g " % p + "  ".join("%-9.3f" % (r[4] / r[2]) for r in rows if r[0] == p))
print("time %.0fs" % (time.time() - t0))
