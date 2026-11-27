#!/usr/bin/env python3
"""a6_03_own_certified.py [u] [levels] [K] [refine]  --  an INDEPENDENT certified multi-rate sequence, and the comparison
of its tops with the coordinator's certified tops (stored outputs of z6_certified_tops.py) and with floating-point
envelope tops computed by the referee in two ways that err in opposite directions.

Own construction (a6exact.py; nothing shared with z6_certified_tops.py):
  * the pairs (E, TH), TH >= theta(E): enclosures of KL(rho || p_u), KL(rho || 1/2) by the referee's interval
    arithmetic on integers (series for exp and log with explicit remainders, 200 bits) -- no mpmath intervals;
  * the rate at a sample point is chosen from the closed form of the slope map through J (the script: golden section);
  * line coefficients rounded to doubles EXACTLY in the valid direction (Fractions; the script: four ulps);
  * own sample points, with a second pass around the point where the cap line leaves the curve;
  * exact hull, exact cap, exact top with the referee's own upper bound abar of a.
By Proposition A13 + Lemma A1 + the base case of Proposition A8, its tops are upper bounds of tau_j as well.

Floating point (a6lib.py), for the comparison only:
  * 'grid'  -- the envelope sequence on grids; its tops err DOWNWARDS (lower hull of grid values >= envelope);
  * 'lines' -- the multi-rate sequence in floating point with many sample points; its tops err UPWARDS.
  So  grid <= b_j <= lines  up to rounding: a two-sided floating-point bracket of the envelope tops.
Required by Corollary A4: every certified top >= b_j.  Required by Proposition A8: >= tau_j (tau_2 in closed form).
"""
import math
import os
import re
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a6exact as X                                             # noqa: E402
import a6lib as L                                               # noqa: E402

u_str = sys.argv[1] if len(sys.argv) > 1 else "1"
JLEV = int(sys.argv[2]) if len(sys.argv) > 2 else 40
KS = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
REF = int(sys.argv[4]) if len(sys.argv) > 4 else 400
KF = 20000

t00 = time.time()
PX = X.CubeX(u_str)
Pf = L.Cube(float(u_str))
abar = X.fl_up(PX.a_hi)
FAIL = []


def check(name, ok, info=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", name, info))
    if not ok:
        FAIL.append(name)


# ---- the coordinator's stored certified tops (text files; read only)
def stored(fname):
    out = {}
    path = os.path.join(os.path.dirname(HERE), fname)
    if not os.path.exists(path):
        return out
    for line in open(path):
        m = re.match(r"\s*(\d+) \| ([0-9.]+) \| ([0-9.]+) \|\s*(\d+) \| (\S+) \| \s*(\S+) \|", line)
        if m:
            out[int(m.group(1))] = (float(m.group(2)), float(m.group(3)), m.group(5))
    return out


coord = stored("out_z6_certified_u%s.txt" % u_str)
coord400 = stored("out_z6_certified_u1_J400.txt") if u_str == "1" else {}

print("# cube, u = %s: referee's certified multi-rate sequence (K = %d sample points + %d around the cap tangency), %d levels" % (u_str, KS, REF, JLEV))
print("# a in [%.17g, %.17g] (referee's enclosure, width %.1e); abar = %.17g; h = %.12f (float)" % (float(PX.a_lo), float(PX.a_hi), float(PX.a.width()), abar, Pf.h))

# ---- floating-point brackets of the envelope tops
tg0 = time.time()
ltops, _ = L.lines_sequence(Pf, JLEV, KF, keep=set(), refine=500)
gtops, _ = L.grid_sequence(Pf, JLEV, KF, keep=set(), refine=500)
print("# floating-point bracket of the envelope tops (K = %d, refined): %.0f s" % (KF, time.time() - tg0))

# ---- the closed form of tau_2 (valid at this slope if |theta'(x*)| <= x*/(a + x*); see a6_01)
f = lambda t: float(2 * Pf.J(t) + (1 - 2 * t) * Pf.J1(t)) - Pf.a      # noqa: E731
lo, hi = 0.0, 0.5
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if f(mid) > 0:
        lo = mid
    else:
        hi = mid
ts = 0.5 * (lo + hi)
xs = float(Pf.e_of_t(ts))
tt = np.linspace(0, 1, 2000001)
tau2 = float(np.min(Pf.a * np.maximum(Pf.a, Pf.e_of_t(tt) + Pf.th_of_t(tt)) / (Pf.a + Pf.e_of_t(tt))))
tau2 = min(tau2, Pf.a ** 2 / (Pf.a + xs))
print("# tau_2 = %.12f = %.9f a (float; minimum of a max(a, x + theta(x))/(a + x))" % (tau2, tau2 / Pf.a))

def dec_up(fr, digits):
    """the decimal with `digits` places that is >= the rational fr (exact ceiling: a printed upper bound stays one)"""
    q = 10 ** digits
    n = -((-fr.numerator * q) // fr.denominator)
    return "%d.%0*d" % (n // q, digits, n % q)


print("# columns: j | own certified c_j (the double, 17 significant digits) | c_j/a, an upper bound printed with an exact ceiling | lines | float bracket of b_j/a: [grid, lines] | coordinator's certified c_j/a (as printed) | (own - b_j)/(b_j - h) | (coord - b_j)/(b_j - h) | j^2 (own - h)/c_*^2")
V = X.XCurve([], abar)
rows = []
for j in range(1, JLEV + 1):
    V = X.own_step(PX, Pf, V, abar, KS, L.sample_points, refine=REF)
    cj = V.c
    ratio_up = X.fl_up(Fr(cj) / PX.a_lo)
    bj_lo, bj_hi = gtops[j], ltops[j]
    cc = coord.get(j)
    c4 = coord400.get(j)
    rel_own = (cj - bj_lo) / (bj_lo - Pf.h) if j >= 2 else 0.0
    rel_co = ((cc[0] - bj_lo) / (bj_lo - Pf.h)) if (cc and j >= 2) else float("nan")
    rows.append((j, cj, ratio_up, bj_lo, bj_hi, cc, c4))
    print("%4d | %.17g | %s | %5d | [%.10f, %.10f] | %s | %9.2e | %9.2e | %.6f" % (
        j, cj, dec_up(Fr(cj) / PX.a_lo, 10), len(V.lines), bj_lo / Pf.a, bj_hi / Pf.a,
        ("%.9f" % cc[1]) if cc else "     -     ", rel_own, rel_co, j * j * (cj - Pf.h) / Pf.cs2), flush=True)

print()
tol = 5e-13 * Pf.a
check("own certified tops are nonincreasing and above h", all(rows[i][1] >= rows[i + 1][1] for i in range(len(rows) - 1)) and all(r[1] > Pf.h for r in rows))
check("own certified tops >= floating-point lower bracket of the envelope tops (Corollary A4)", all(r[1] >= r[3] - tol for r in rows),
      "| least (c_j - grid_j)/a: %.2e" % min((r[1] - r[3]) / Pf.a for r in rows))
have = [r for r in rows if r[5]]
if have:
    check("the coordinator's certified tops (as printed, 12 decimals) >= floating-point lower bracket, at all %d common levels" % len(have),
          all(r[5][0] >= r[3] - tol - 5e-13 for r in have), "| least (c_j - grid_j)/a: %.2e" % min((r[5][0] - r[3]) / Pf.a for r in have))
    worst = max(abs(r[5][0] - r[1]) / (r[3] - Pf.h) for r in have if r[0] >= 2)
    check("the two certified sequences agree to within 1e-2 of b_j - h at every common level (they need not agree further)", worst < 1e-2,
          "| largest |own - coordinator|/(b_j - h): %.2e; own is the smaller one at %d of %d levels" % (worst, sum(1 for r in have if r[1] < r[5][0]), len(have)))
have4 = [r for r in rows if r[6]]
if have4:
    check("the coordinator's run to 400 levels (K = 4000) >= floating-point lower bracket at the %d common levels" % len(have4), all(r[6][0] >= r[3] - tol - 5e-13 for r in have4))
check("the bracket [grid, lines] is consistent (grid <= lines up to rounding) and narrow", all(r[3] <= r[4] + 1e-13 for r in rows),
      "| largest width (lines - grid)/(b_j - h): %.2e" % max((r[4] - r[3]) / (r[3] - Pf.h) for r in rows if r[0] >= 2))
r2 = rows[1]
check("j = 2: own certified c_2 >= tau_2 (closed form), and within 1e-6 a of it", r2[1] >= tau2 - 1e-14 and r2[1] - tau2 < 1e-6 * Pf.a, "| (c_2 - tau_2)/a = %.2e" % ((r2[1] - tau2) / Pf.a))
if have:
    c2 = have[1][5][0] if have[1][0] == 2 else None
    if c2:
        check("j = 2: the coordinator's certified c_2 >= tau_2", c2 >= tau2 - 5e-13, "| (c_2 - tau_2)/a = %.2e" % ((c2 - tau2) / Pf.a))
# the certified majorant at three rates, against theta_hint (it must be above it) and against the coordinator's printed values
gs = [0.1 * Pf.h, 0.5 * Pf.h, Pf.h]
Mx = [float(X.fl_up(V.M_exact(g))) for g in gs]
print("  level %d, certified majorant M(g) at g = 0.1h, 0.5h, h:  %s   (theta_hint: %s)" % (
    JLEV, "  ".join("%.9f" % m for m in Mx), "  ".join("%.9f" % float(Pf.theta_hint(g)) for g in gs)))
check("own certified majorant >= theta_hint at the three rates", all(Mx[i] >= float(Pf.theta_hint(gs[i])) - 1e-15 for i in range(3)))
print()
print("time %.0f s" % (time.time() - t00))
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
