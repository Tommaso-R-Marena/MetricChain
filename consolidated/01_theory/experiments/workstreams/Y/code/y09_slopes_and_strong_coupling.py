"""Two scans around the main table (binary symmetric chain).
(1) slope dependence at p = 0.3: Lyapunov lower bound (tilted Markov labels) for h and E_F for E against the cube, and the
    one-site Markov-recursion (DP, L = 1) upper bound; small-slope prediction: ratio -> chi = (1-p)/p.
(2) strong coupling at u = 1: p -> 0: the DP (L = 1) upper bounds on h, a, E; Lyapunov lower bound on h; E_F -> u/2."""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *
from ylyap import *

t0 = time.time()
def lyap_h(p, u, cmax=3.0):
    def best_c(t):
        grid = np.linspace(0.0, cmax, 31); vals = [G_inf(t, c, p, u) for c in grid]; i = int(np.argmax(vals))
        c, v = golden_max(lambda c: G_inf(t, c, p, u), grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)], it=25)
        return v, c
    ts = np.linspace(0.1, 0.9, 17); vals = [best_c(t)[0] for t in ts]; i = int(np.argmax(vals))
    tst, hlow = golden_max(lambda t: best_c(t)[0], ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)], it=20)
    return hlow, tst, best_c(tst)[1]
def dp1(p, u):
    us = ustar(u, p); P = gibbs_rows([1 - p, p], [[0.0, us], [0.0, -us]])
    h = h_mult(P); a = capacity(P, tol=1e-12); E = E_threshold(P, tol=1e-12)
    return us, h[1], a[1], E[1]

p = 0.3
print("(1) p = 0.3 (chi = (1-p)/p = %.4f): slope dependence" % ((1 - p) / p))
print("    u     | h_cube     h >= (Lyap)  ratio  (t*, c*)       h <= (DP1)  | E_cube     E_F        ratio   E <= (DP1) | a_cube    a <= (DP1)")
for u in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0):
    hc, ac, Ec = cube_numbers(u)
    hl, tst, cst = lyap_h(p, u, cmax=4.0 if u < 0.3 else 3.0)
    us, hu, au, Eu = dp1(p, u)
    print("    %-5.2f | %.6f   %.6f     %.3f  (%.3f, %.2f)   %.6f   | %.6f   %.6f   %.3f   %.6f   | %.6f  %.6f" % (
        u, hc, hl, hl / hc, tst, cst, hu, Ec, E_F(p, u), E_F(p, u) / Ec, Eu, ac, au))

u = 1.0; hc, ac, Ec = cube_numbers(u)
print("\n(2) u = 1: strong coupling (cube: h = %.6f, a = %.6f, E = %.6f; u/2 = 0.5)" % (hc, ac, Ec))
print("    p      K       u*      | h >= (Lyap)  h <= (DP1)  | a <= (DP1)   H(p)      | E_F        E <= (DP1)")
for p in (0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.003, 0.001):
    us, hu, au, Eu = dp1(p, u)
    hl = lyap_h(p, u)[0] if p >= 0.02 else float("nan")
    Hp = -p * math.log(p) - (1 - p) * math.log(1 - p)
    print("    %-6.3f %.4f  %.4f  | %.6f     %.6f    | %.6f     %.6f  | %.6f   %.6f" % (p, math.log((1 - p) / p), us, hl, hu, au, Hp, E_F(p, u), Eu))
print("%.1f s" % (time.time() - t0))
