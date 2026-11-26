#!/usr/bin/env python3
"""
r16_validate.py -- workstream R16: cross-check of r16lib.py (float64 logarithms) against the science division's
EXACT-arithmetic implementation of workstream R6 (experiments/science/ws_R6/r6lib.py: exact integers, Fractions,
40-digit mpmath; everyn.py: Proposition K0), which was written from the statements before any code of the theory
division was read (R6_REPORT.md section 3.1).  Read-only import (run with python3 -B: no bytecode is written).

Checks, at n = 4000, u = 1:
  (1) tables ln|B|, ln E_r, ln T_k on Q_m, m in {300, 1500, 2500}: largest absolute difference of logarithms;
  (2) every constant of the OUTER level (phi_1 = 0.375 and 0.5): J, nu_0, r-dagger, m_max, K, ln Mbar, ln delta', x_out;
  (3) the cost of the base bracket at the 40 rungs (R6 rounds eta down to a multiple of 1e-6: differences of the order
      1e-5 in ln(cost) are expected);
  (4) two MIDDLE designs in dimension 2500 (the bounded one at x = 0.5, b = max, phi_2 = 0.5; the extensive one at
      x = 50, phi_2 as chosen by the rule): constants, the cost of the base bracket at their 30 rungs, and ln C_max;
  (5) ln C_max of the outer level at phi_1 = 0.5 (two levels).
"""
import os
import sys
import time
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_R6"))
import mpmath as mp          # noqa: E402
import r6lib as X            # noqa: E402   (science division, workstream R6: exact)
import everyn as EV          # noqa: E402   (science division, workstream R6: Proposition K0, exact tables)
sys.path.pop(0)
import r16lib as R           # noqa: E402

mp.mp.dps = 40
u = 1.0
t0 = time.time()
nbad = 0


def flag(ok):
    global nbad
    if not ok:
        nbad += 1
    return "ok" if ok else "DIFFER"


print("# r16_validate.py started %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
xt = {}


def xtab(m):
    if m not in xt:
        xt[m] = X.Tables(m, u)
    return xt[m]


# (1) tables
for m in (300, 1500, 2500):
    T = xtab(m)
    t = R.tab(m, u)
    dB = max(abs(float(mp.log(T.ball[r])) - t.lB[r]) for r in range(0, m + 1, max(1, m // 400)))
    dE = max(abs(float(mp.log(T.E[r])) - t.lE[r]) for r in range(0, m + 1, max(1, m // 400)))
    dT = max(abs(float(mp.log(T.T[r])) - t.lT[r]) for r in range(0, m + 1, max(1, m // 400)))
    print("(1) Q_%d: max |ln B - ln B_exact| = %.2e, ln E: %.2e, ln T: %.2e   %s" % (m, dB, dE, dT, flag(max(dB, dE, dT) < 1e-9)))


def compare_level(name, lev, theta, nu1, eta_frac):
    """constants of r16lib.Level against r6lib.Params2LP (exact)"""
    P = X.Params2LP(lev.n, lev.n_o, u, lev.lam, eta_frac, lev.etap, theta, nu1, lev.b, mp.e ** mp.mpf(lev.ldelta),
                    lev.xs, [1] * lev.L, tables=xtab(lev.n_o))
    ok = (P.J == lev.J and P.rdag == lev.rdag and P.m_max == lev.m_max and P.K == lev.K
          and abs(float(mp.log(P.nu0)) - math.log(lev.nu0)) < 1e-9
          and abs(float(mp.log(P.Mbar)) - lev.lMbar) < 1e-8
          and abs(float(mp.log(P.deltap)) - lev.ldeltap) < 1e-8
          and abs(float(P.x_out) - lev.xout) < 1e-10)
    print("(2/4) %s: J %d|%d, r-dagger %d|%d, m_max %d|%d, K %d|%d, ln nu0 %.9f|%.9f, ln Mbar %.8f|%.8f, ln delta' %.8f|%.8f,"
          " x_out %.12f|%.12f   %s" % (name, P.J, lev.J, P.rdag, lev.rdag, P.m_max, lev.m_max, P.K, lev.K,
                                       float(mp.log(P.nu0)), math.log(lev.nu0), float(mp.log(P.Mbar)), lev.lMbar,
                                       float(mp.log(P.deltap)), lev.ldeltap, float(P.x_out), lev.xout, flag(ok)))
    return P


def compare_k0_and_cmax(name, lev, P):
    """base-bracket costs at the rungs of lev, and ln C_max, against R6's exact routines"""
    d = lev.n_i
    lC = [None]
    lCx = [None]
    worst = 0.0
    kinds_differ = 0
    for l in range(1, lev.L + 1):
        c, kind = R.k0(u, d, lev.xs[l], lev.ldeltap)
        cx, info = EV.k0_cost(d, u, lev.xs[l], P.deltap, xtab(d))
        lC.append(c)
        lCx.append(cx)
        worst = max(worst, abs(float(cx) - c))
        kinds_differ += (kind == "enum") != (info["mode"] == "enum")
    lcm = lev.lCmax(lC)
    terms = [mp.log(2 * P.Mbar)]
    for l in range(1, lev.L + 1):
        terms.append(mp.log(min(2 * P.Mbar, (P.J + 1) * P.cnt(lev.xs[l - 1]))) + lCx[l])
    mx = max(terms)
    lcmx = float(mx + mp.log(mp.fsum(mp.e ** (t - mx) for t in terms) + mp.e ** (-mx)))
    print("(3/5) %s: base bracket at %d rungs in dimension %d: max |ln cost - ln cost_exact| = %.2e (enum/sample choices"
          " that differ: %d); ln C_max %.6f | exact %.6f, difference %.2e   %s"
          % (name, lev.L, d, worst, kinds_differ, lcm, lcmx, lcm - lcmx, flag(abs(lcm - lcmx) < 2e-3 and kinds_differ == 0)))
    return lcm, lcmx


from fractions import Fraction as Fr      # noqa: E402

a = R.a_of(u)
n = 4000
for phi in (0.375, 0.5):
    lev = R.outer_level(u, n, phi)
    P = compare_level("outer level n=%d phi_1=%.3f" % (n, phi), lev, 0.05, 2 * math.exp(u) * lev.n_o / 0.05, Fr(1, 20))
    lcm, lcmx = compare_k0_and_cmax("outer level n=%d phi_1=%.3f (two levels)" % (n, phi), lev, P)
    print("      two-level certified bound ln(C_max)/(na): %.4f | exact %.4f   [%.0f s]" % (lcm / (n * a), lcmx / (n * a), time.time() - t0))
    if phi == 0.375:
        ldp = lev.ldeltap
        d = lev.n_i

# (4) middle designs in dimension d = 2500 with the outer delta' of phi_1 = 0.375
x = 0.5
c = min(x / 12, 1 / 3)
bmax = x - R.acc_const(c) - 1e-6
mb = R.middle_bounded(u, d, x, 0.5, bmax, ldp)
Pb = compare_level("middle bounded d=%d x=0.5 b=max phi_2=0.5" % d, mb, c, 2 * math.exp(u) * mb.n_o / c, Fr(c).limit_denominator(10 ** 12))
compare_k0_and_cmax("middle bounded d=%d x=0.5 b=max phi_2=0.5" % d, mb, Pb)
x = 50.0
g = x / d
p0 = min(0.7, max(0.05, g / (g + R.theta_hint(u, g))))
p2 = min(0.8, 1.5 * p0)
me = R.middle_extensive(u, d, x, p2, ldp)
Pe = compare_level("middle extensive d=%d x=50 phi_2=%.4f" % (d, p2), me, mp.e ** mp.mpf(me.ltheta), 1.0, Fr(1, 2))
compare_k0_and_cmax("middle extensive d=%d x=50 phi_2=%.4f" % (d, p2), me, Pe)

print("# checks that differ: %d" % nbad)
print("# finished %s; elapsed %.0f s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), time.time() - t0))
print("peak RSS MB", R.peak_rss_mb())
