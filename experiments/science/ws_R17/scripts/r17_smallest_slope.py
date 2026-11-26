#!/usr/bin/env python3
"""R17 spot check: the smallest slope-step level (theory report 11.58a, "What it is not" (v), the referee R12's
computation): "the smallest slope step exists at n = 187 (u = 2.5; at n = 202 for u = 2, 470 for u = 1), its
certified bound there is e^{142} (e^{125}, e^{101}), and a run of it that does not abort makes at least e^{49}
(e^{43}, e^{36}) evaluations".  Own code: r17_nest.py (families from Q_REPORT 4.1) on our r16lib.
The level: first slope step over the base family (R = infinity, R' = h), accuracy xhat = h n, delta = 0.05."""
import math, resource, sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r17_nest as N
import r17_formula as F
t0 = time.time()
for u, target in ((1.0, (470, 101, 36)), (2.0, (202, 125, 43)), (2.5, (187, 142, 49))):
    C = F.Cube(u)
    n = 2
    while not (1 + F.c_log(C, n) + C.h <= C.h * n):
        n += 1
    base = N.Base(C)
    S = N.Slope(C, base)
    xhat = C.h * n
    lcm, lev = S.level(n, xhat, math.log(0.05), 'proof')
    c1 = base.cost(lev.n_i, lev.xs[1], lev.ldeltap, 'proof')
    print("u=%g: smallest n with X_0(n) <= h n: %d (theirs %d);  X_0=%.4f, h n=%.4f, n_o=%d, n_i=%d, L=%d, K=%d, "
          "ln C_max = %.2f (theirs e^%d);  ln(K * C_1) = %.2f with C_1 the base bracket of rung 1 (x_1 = %g, ln C_1 = %.2f) "
          "(theirs e^%d);  base alone at (n, xhat): ln cost %.2f; enumeration n ln 2 = %.2f"
          % (u, n, target[0], 1 + F.c_log(C, n) + C.h, xhat, lev.n_o, lev.n_i, lev.L, lev.K, lcm, target[1],
             math.log(lev.K) + c1, lev.xs[1], c1, target[2], base.cost(n, xhat, math.log(0.05), 'proof'), n * math.log(2)))
print("violations recorded by the node checks: %d" % N.stats['viol'])
print("LAST LINE r17_smallest_slope.py: completed; wall %.1f s; peak RSS %.1f MB"
      % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
