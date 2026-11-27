"""r10_13: in which range of (p,u) is "the interaction raises the exponent" proved, and where is
the OPPOSITE proved?  Own code.

Upper bounds: Proposition F of Y (Markov recursion) with blocks of L = 3 sites,
    F_inf(t) <= F^DP_3(t)/3,  F^DP_3 = F*[P^(3)(.|+); slopes (u,u,u*)]  (all 72-96 vertices, duality
    brackets), hence  a_inf <= capacity/3,  E_inf <= threshold/3,  and
    h_inf = sup_t F_inf(t) <= rigorous sup over t from a grid of step 0.005 by the interval rule
    (F*/t nonincreasing, F*/(1-t) nondecreasing for every finite site) with the tails
    t*E and (1-t)*a.
Lower bounds (every n, every algorithm): Proposition H (tilted Markov labels) and block fields
    (Proposition I with the two uniform fields on blocks of any length); for a: the same
    families divided by (1-t) at t = 0.99 and 0.999.
usage: python3 r10_13_reversal.py [p ...]
"""
import sys
import time
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from r10lib import *
from r10_lyap import G_inf
from r10_blockfield import joint_first_last_m, blockfield_bound
from r10_06_markov_recursion import ustar, dp_block

t0 = time.time()
ps = [float(a) for a in sys.argv[1:]] or [0.45, 0.4, 0.3, 0.2, 0.1, 0.05]
us = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0]
TG = np.round(np.arange(0.05, 0.9501, 0.005), 4)


def dp_upper(p, u, L=3):
    W, nv = dp_block(p, u, L)
    B = np.array([renyi_bracket(W, float(t), tol=1e-11, iters=40000)["upper"] for t in TG]) / L
    a_up = capacity_bracket(W, tol=1e-11)["upper"] / L
    e_up = threshold_bracket(W, tol=1e-11)["upper"] / L
    iv = np.minimum(B[:-1] * TG[1:] / TG[:-1], B[1:] * (1 - TG[:-1]) / (1 - TG[1:]))
    h_up = max(iv.max(), TG[0] * e_up, (1 - TG[-1]) * a_up)
    return h_up, B.max(), float(TG[int(np.argmax(B))]), a_up, e_up, nv


def G_checked(t, c, p, u):
    a = G_inf(t, c, p, u, N=48)
    b = G_inf(t, c, p, u, N=96)
    return a if abs(a - b) < 1e-8 * max(1.0, abs(a)) + 1e-9 else -np.inf


def lower_h(p, u):
    best = (-np.inf, "none")
    for ts in (0.45, 0.3, 0.15):
        for cs in (0.0, 0.5, 1.0):
            r = minimize(lambda v: -G_inf(min(max(v[0], 0.02), 0.98), max(v[1], 0.0), p, u), (ts, cs),
                         method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-11))
            tt, cc = min(max(r.x[0], 0.02), 0.98), max(r.x[1], 0.0)
            v = G_checked(tt, cc, p, u)
            if v > best[0]:
                best = (v, "H t=%.3f c=%.3f" % (tt, cc))
    for L in range(1, 41):
        f = joint_first_last_m(L, p)
        tb, vb = golden_max(lambda t: blockfield_bound(p, u, L, t, f)[0], 0.03, 0.97, tol=1e-4)
        if abs(blockfield_bound(p, u, L, tb, f, N=96)[0] - vb) < 1e-8 and vb > best[0]:
            best = (vb, "B L=%d t=%.3f" % (L, tb))
    return best


def lower_a(p, u):
    best = (-np.inf, "none")
    for t in (0.99, 0.999):
        r = minimize_scalar(lambda c: -G_inf(t, c, p, u, N=64), bounds=(0.0, 3.0), method="bounded")
        v = G_checked(t, r.x, p, u) / (1 - t)
        if v > best[0]:
            best = (v, "H t=%.3f c=%.3f" % (t, r.x))
        for L in range(1, 25):
            f = joint_first_last_m(L, p)
            v1 = blockfield_bound(p, u, L, t, f)[0]
            v2 = blockfield_bound(p, u, L, t, f, N=96)[0]
            if abs(v1 - v2) < 1e-10 and v1 / (1 - t) > best[0]:
                best = (v1 / (1 - t), "B L=%d t=%.3f" % (L, t))
    return best


def verdict(lo, up, cube):
    if lo > cube * (1 + 1e-5):
        return "RAISED"
    if up < cube * (1 - 1e-5):
        return "LOWERED"
    return "undecided"


res = {}
for p in ps:
    for u in us:
        hc, tc, ac, Ec = cube_exponents(u)
        h_up, Bmax, tB, a_up, e_up, nv = dp_upper(p, u)
        lh = lower_h(p, u)
        la = lower_a(p, u)
        vh = verdict(lh[0], h_up, hc)
        va = verdict(la[0], a_up, ac)
        res[(p, u)] = (vh, va, lh[0] / hc, h_up / hc, la[0] / ac, a_up / ac)
        print("p=%-5g u=%-4g | h: cube %.6f  lower %.6f [%s]  upper(DP,L=3) %.6f (grid max %.6f at t=%.3f)  -> %-9s | a: cube %.6f  lower %.6f [%s]  upper %.6f -> %-9s | E: cube %.6f  E_F %.6f  upper %.6f  (%.0fs)"
              % (p, u, hc, lh[0], lh[1], h_up, Bmax, tB, vh, ac, la[0], la[1], a_up, va, Ec, E_F(p, u), e_up, time.time() - t0), flush=True)
print("\nverdicts for h (rows p, columns u = %s)" % us)
for p in ps:
    print("  p=%-5g " % p + " ".join("%-10s" % res[(p, u)][0] for u in us))
print("verdicts for a")
for p in ps:
    print("  p=%-5g " % p + " ".join("%-10s" % res[(p, u)][1] for u in us))
print("brackets [lower, upper]/cube for h")
for p in ps:
    print("  p=%-5g " % p + " ".join("[%.3f,%.3f]" % res[(p, u)][2:4] for u in us))
print("brackets [lower, upper]/cube for a")
for p in ps:
    print("  p=%-5g " % p + " ".join("[%.3f,%.3f]" % res[(p, u)][4:6] for u in us))
print("time %.0fs" % (time.time() - t0))
