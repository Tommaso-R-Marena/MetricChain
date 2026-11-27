#!/usr/bin/env python3
"""a6_07_pairs.py  --  the two places where z6_certified_tops.py relies on mpmath's interval arithmetic, checked against
the referee's own enclosures (integers, series with remainders; a6exact.py):

 (1) abar = up(KL(p_u || 1/2)) >= a   and   ALOW <= a,   for several slopes (the module is re-imported per slope);
 (2) certified_pair(rho) = (e', thbar):  e' >= KL(rho || p_u)  and  thbar >= KL(rho || 1/2)  (hence thbar >=
     theta(e'), theta being nonincreasing) for random doubles rho in (p_u, 1/2) and for rho next to both ends;
     and how tight the pairs are (in ulps).
 (3) at u = 5: the second certified top of the coordinator's script and of the referee's own sequence against the
     closed form a^2/(a + x*) of A6a -- a certified refutation of the closed form at that slope.

Why this matters: mpmath's `iv.log` rounds an APPROXIMATION of the logarithm (computed with 20 guard bits) in the
directed way -- it is not a proved enclosure in the last bit of the working precision.  At 30 digits that last bit
is 14 orders of magnitude below a double ulp, and the script's outward rounding to doubles leaves a slack that is
positive but can be arbitrarily small; so "rigorous" holds with overwhelming probability, not by proof, unless the
values are checked -- which is what this script does for the values it samples.
"""
import importlib
import math
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import a6exact as X                                             # noqa: E402

t00 = time.time()
FAIL = []
rng = np.random.default_rng(7)


def check(name, ok, info=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", name, info))
    if not ok:
        FAIL.append(name)


z6 = None
for u_str in ("1", "2", "0.5", "0.25", "3", "5"):
    _argv = sys.argv
    sys.argv = ["z6_certified_tops.py", u_str, "1", "10", "nocompare"]
    if z6 is None:
        import z6_certified_tops as z6                          # noqa: E402
    else:
        z6 = importlib.reload(z6)
    sys.argv = _argv
    PX = X.CubeX(u_str)
    abar, alow = float(z6.ABAR), float(z6.ALOW)
    ulp = math.ulp(abar)
    print("u = %s:  a in [%.20g, %.20g] (referee);  script: ALOW = %.20g, abar = %.20g" % (u_str, float(PX.a_lo), float(PX.a_hi), alow, abar))
    check("u = %s: abar >= a and ALOW <= a (proved with the referee's enclosure)" % u_str, Fr(abar) >= PX.a_hi and Fr(alow) <= PX.a_lo,
          "| slack (abar - a)/ulp = %.3f, (a - ALOW)/ulp = %.3f" % (float((Fr(abar) - PX.a_hi) / Fr(ulp)), float((PX.a_lo - Fr(alow)) / Fr(ulp))))
    pu_hi = PX.pu.upper()
    pu = float(pu_hi)
    n = 1500 if u_str in ("1", "2") else 600
    rhos = list(pu + (0.5 - pu) * rng.random(n) ** 2)
    rhos += [pu + (0.5 - pu) * w * w for w in (1e-6, 3e-6, 1e-5, 1e-4, 1e-3, 1e-2)]      # the script's lower end is w = 1e-6
    rhos += [0.5 - d for d in (1e-3, 1e-6, 1e-9, 1e-12, 1e-15, 2 ** -53)] + [0.5]
    bad = 0
    min_e = min_t = math.inf
    max_e = max_t = 0.0
    for r in rhos:
        r = float(r)
        if not (Fr(r) > pu_hi and r <= 0.5):
            continue
        e_s, th_s = z6.certified_pair(r)
        if r >= 0.5:
            ok = Fr(e_s) >= PX.eps_hi and th_s == 0.0
            bad += (not ok)
            continue
        e_iv = X.kl(r, PX.pu)
        t_iv = X.kl(r, PX.half)
        ok = Fr(e_s) >= e_iv.upper() and Fr(th_s) >= t_iv.upper() and e_s > 0
        bad += (not ok)
        se = float((Fr(e_s) - e_iv.upper()) / Fr(math.ulp(e_s)))
        st = float((Fr(th_s) - t_iv.upper()) / Fr(math.ulp(th_s)))
        min_e, max_e, min_t, max_t = min(min_e, se), max(max_e, se), min(min_t, st), max(max_t, st)
    check("u = %s: %d pairs (random rho, both ends, rho = 1/2): e' >= KL(rho||p_u) and thbar >= KL(rho||1/2), proved" % (u_str, len(rhos)), bad == 0,
          "| slack in ulps: e' %.1e .. %.1e, thbar %.1e .. %.1e" % (min_e, max_e, min_t, max_t))

# ---- (3) at u = 5 (z6 is still loaded for u = 5): the certified second top against the closed form a^2/(a + x*)
print("(3) u = 5: certified upper bounds of tau_2 against the closed form a^2/(a + x*) of A6a")
import a6lib as L                                               # noqa: E402
Pf = L.Cube(5.0)
PX = X.CubeX("5")
closed = 0.604053203153265 * Pf.a                               # a^2/(a + x*) (a6_01 part D, a6_08)
tau2 = 0.602893471993203 * Pf.a                                 # min_x a max(a, x + theta(x))/(a + x)  (the same scripts)
z6.K = 2000                                                     # the module's number of sample points (a global read by step)
V = z6.Curve([], [], z6.ABAR)
V = z6.step(V)
V = z6.step(V)
c2_script = float(V.c)
abar = X.fl_up(PX.a_hi)
W = X.XCurve([], abar)
W = X.own_step(PX, Pf, W, abar, 1500, L.sample_points, refine=400)
W = X.own_step(PX, Pf, W, abar, 1500, L.sample_points, refine=400)
c2_own = float(W.c)
print("    closed form a^2/(a + x*) = %.12f = 0.604053203 a;   tau_2 = min_x a max(a, x + theta)/(a + x) = %.12f = 0.602893472 a" % (closed, tau2))
print("    certified c_2: the coordinator's script (K = 2000): %.15g = %.9f a;   the referee's sequence: %.15g = %.9f a" % (
    c2_script, c2_script / Pf.a, c2_own, c2_own / Pf.a))
check("u = 5: both certified second tops are below the closed form by more than 1e-3 a (so tau_2 < a^2/(a + x*), given the statements the certificate rests on)",
      c2_script < closed - 1e-3 * Pf.a and c2_own < closed - 1e-3 * Pf.a)
check("u = 5: both certified second tops are above tau_2 and within 1e-6 a of it", tau2 - 1e-12 <= c2_own <= tau2 + 1e-6 * Pf.a and tau2 - 1e-12 <= c2_script <= tau2 + 1e-6 * Pf.a,
      "| (c_2 - tau_2)/a: script %.1e, referee %.1e" % ((c2_script - tau2) / Pf.a, (c2_own - tau2) / Pf.a))

print()
print("time %.0f s" % (time.time() - t00))
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
