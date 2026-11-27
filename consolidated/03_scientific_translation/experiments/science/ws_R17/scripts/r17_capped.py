#!/usr/bin/env python3
"""R17: the two ends of the range of a slope step (item 1(i): "is the statement uniform ... including the smallest
and the largest slope step of an epoch?"), exact constants, own code (r17_nest.py on our r16lib).
 * smallest: xhat = X_0(n) exactly and just above (outer block of ONE coordinate);
 * largest:  xhat = R' n with R' = h (first slope step of an epoch): the inner block has only about (1 + c_log)/h
   coordinates, and for h n > 2u n_i the ladder is CAPPED at ceil(2 u n_i) - 1 < ceil(xhat) (case 2 of step (5)
   of the proof of Proposition Q6); also R' = h/2, h/3 (later steps of an epoch, saturating inner family of slope
   sigma on the range R - emulated here by the base family, whose cost is below every such majorant, so only the
   level's own inequalities (accuracy, Lemma Q4, (4.1), (2.1)) and the bound with (B, sigma, R) = (a, 0, inf) are
   checked).
Every level built is checked inside r17_nest.Slope.level: x_out = xhat, Lemma Q4, (4.1), (2.1), Proposition Q6."""
import math, os, resource, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r17_nest as N
import r17_formula as F
import r16lib as R
t0 = time.time()
print("# u n delta | xhat  n_o n_i  x_1  capped?  L  r_dag  ln(1/pi)  n_o h + ln(n_o+1) | ln C_max  Q6 bound  slack | (4.1) slack")
for u, sizes in ((1.0, (470, 2000, 34000, 40000, 64000)), (2.0, (202, 1000, 8300, 16000)), (0.5, (1678, 20000))):
    C = F.Cube(u)
    for n in sizes:
        for ld in (math.log(0.05), -float(n)):
            base = N.Base(C)
            S = N.Slope(C, base)
            X0 = 1 + F.c_log(C, n) + C.h
            # X0 + 1e-9: at xhat = X_0 exactly, floor((xhat - 1 - c_log)/h) = floor(h/h) is 0 in floating point (a tie;
            # the first version of this script failed there: not_cited/slope_ends_failed_*.log); in exact arithmetic n_o = 1
            for xhat in (X0 + 1e-9, X0 + 0.999 * C.h, 0.5 * (X0 + C.h * n), C.h * n):
                if xhat < X0 or xhat > C.h * n:
                    continue
                before = dict(N.stats)
                lcm, lev = S.level(n, xhat, ld, 'proof')
                Lam = -ld + n * math.log(2)
                bq6 = n * S.B - S.sigma * xhat + S.E(n, xhat, Lam)
                PM = math.log(lev.J + 1) + math.log(24 * math.e * (math.e - 1)) + lev.lK
                capped = lev.xs[1] < math.ceil(xhat)
                print("%g %d %s | %.4f %d %d %g %s %d %d %.3f %.3f | %.2f %.2f %.2f | %.2f"
                      % (u, n, "0.05" if ld > -10 else "e^-n", xhat, lev.n_o, lev.n_i, lev.xs[1], "CAPPED" if capped else "-",
                         lev.L, lev.rdag, -lev.lpidag, lev.n_o * C.h + math.log(lev.n_o + 1), lcm, bq6, bq6 - lcm,
                         xhat - 1 + PM - (math.log(2) + lev.lMbar)))
            R.clear_tabs(); N._pm.clear()
print("violations recorded by the level checks: %d  %s" % (N.stats['viol'], N.viol_log[:3]))
print("LAST LINE r17_capped.py: completed; wall %.1f s; peak RSS %.1f MB"
      % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
