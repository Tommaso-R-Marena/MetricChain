"""Controls for the conservative tilt-state recursion (ydp3.DP3):
(1) p = 1/2 (uniform cube): the recursion must return the cube's F(t) = t ln cosh(u/2) - ln cosh(tu/2), E = ln cosh(u/2), and
    capacity a = ln 2 - h(1/(1+e^u));  safe values approach from above like the grid spacing, grid-restricted values are exact;
(2) finite chains: the stationary safe rate times n must dominate the exact F*_n(t) minus the proved boundary term (n = 4, all vertices);
(3) the two ends for the bracket at p = 0.3, t = 0.43 in dependence of G (safe decreasing, grid-restricted increasing)."""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *
from ydp3 import DP3
t0 = time.time(); u = 1.0
hc, ac, Ec = cube_numbers(u)
print("(1) p = 0.5: cube F(0.49) = %.7f, E = %.7f, a = %.7f" % (0.49 * math.log(math.cosh(0.5)) - math.log(math.cosh(0.245)), Ec, ac))
for G in (201, 801, 3201):
    s = DP3(0.5, u, G, +1); r = DP3(0.5, u, G, -1)
    print("   G=%4d: Renyi t=0.49: safe %.7f, grid-restricted %.7f | E: safe %.7f, restricted %.7f | a (Shannon): safe %.7f, restricted %.7f" % (
        G, s.renyi_rate(0.49, 0.5)[1], r.renyi_rate(0.49, 0.5)[1], s.kl_rate()[1], r.kl_rate()[1], s.shannon_rate(0.5)[1], r.shannon_rate(0.5)[1]))
print("(2) n = 4, all 990 vertices: exact max_phi (1-t)D_t(pi_phi||Q_qt) against n * (safe stationary rate, G=801)")
H = height_functions(4) * u
for p in (0.4, 0.3, 0.1):
    pi = bsc_block_law(4, p); P = gibbs_rows(pi, H); d = DP3(p, u, 801, +1); row = []
    for t in (0.3, 0.45, 0.7):
        for qt in (p, 0.8 * p):
            Q = bsc_block_law(4, qt)
            exact = float((-np.log((P ** t) @ (Q ** (1 - t)))).max())
            row.append("t=%.2f qt=%.2f: exact %.5f <= 4*rate %.5f %s" % (t, qt, exact, 4 * d.renyi_rate(t, qt)[1], "ok" if exact <= 4 * d.renyi_rate(t, qt)[1] + 1e-9 else "VIOLATED"))
    print("   p=%.1f: " % p + " | ".join(row))
print("(3) p = 0.3, t = 0.43, qt = 0.255: safe and grid-restricted rates")
for G in (201, 401, 801, 1601):
    s = DP3(0.3, u, G, +1).renyi_rate(0.43, 0.255); r = DP3(0.3, u, G, -1).renyi_rate(0.43, 0.255, iters=3000)
    print("   G=%4d: safe [%.7f, %.7f]   grid-restricted [%.7f, %.7f]   [%.0f s]" % (G, s[0], s[1], r[0], r[1], time.time() - t0), flush=True)
print("%.1f s" % (time.time() - t0))
