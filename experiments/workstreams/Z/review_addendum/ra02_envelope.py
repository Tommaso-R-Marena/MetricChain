#!/usr/bin/env python3
"""RA02 -- the envelope sequence of A3, computed by the referee in two ways:
  (S) structural (EnvSeq): W_{j+1} = Sigma(., W_j) up to the tangency point, then the tangent line through (b_{j+1}, 1);
      double precision root finding, no grid;
  (G) from the definition on grids (GridEnv): lower convex envelope of the grid values of min(1, Sigma(B, W_j(B))),
      two grid designs and two resolutions.
Prints the tops b_j, j^2 (b_j - h)/c_*^2, the difference between (S) and (G), the table of A6 (cube u = 1), the exact
values for the Gaussian pair (b_2 = 1/2, b_3 = 5/14, derived by hand) and the lower bound 1/(4 cos^2(pi/(2j+1))).
Usage: python3 -B ra02_envelope.py [pair] [J]      pair in {cube1, cube2, cube0.5, gauss}; default cube1 120
"""
import math
import sys
import time

import numpy as np

import ra_lib as R

which = sys.argv[1] if len(sys.argv) > 1 else "cube1"
J = int(sys.argv[2]) if len(sys.argv) > 2 else 120
P = (R.Gauss() if which == "gauss" else R.Cube(float(which[4:]))).setup()
a, h, c2 = P.a, P.h, P.cstar2
print("# %s: a = %.8f, h = %.8f (h/a = %.5f), L = %.6f, c_*^2 = %.8f" % (P.name, a, h, h / a, P.L, c2))

t0 = time.time()
S = R.EnvSeq(P, J)
print("# structural sequence to level %d: %.1f s;  largest relative mismatch between the chord slope and H'(B_t): %.1e"
      % (J, time.time() - t0, max(S.tan_err)))
JG = min(J, 80)
t0 = time.time()
G1 = R.GridEnv(P, JG, 4000, "uniform")
G2 = R.GridEnv(P, JG, 16000, "uniform")
G3 = R.GridEnv(P, JG, 8000, "quad")
print("# grid sequences (uniform 4000, uniform 16000, quadratic 8000) to level %d: %.1f s" % (JG, time.time() - t0))

print("#   j     b_j/a (S)      j^2(b_j-h)/c_*^2    B_t(j)/a     W_j(B_t)    slope m_j |  (G)-(S) in units of a: uni4000   uni16000   quad8000")
rows = list(range(0, 13)) + [k for k in (15, 20, 30, 40, 60, 80, 100, 120, 160, 200, 300, 400, 600, 800, 1000) if 12 < k <= J]
for j in rows:
    if j > J:
        continue
    d = ["%9.1e" % ((G.b[j] - S.b[j]) / a) if j <= JG else "    -    " for G in (G1, G2, G3)]
    if j >= 1:
        print("  %4d  %.8f   %10.5f        %.6f    %.5f   %9.3f  |  %s  %s  %s"
              % (j, S.b[j] / a, j * j * (S.b[j] - h) / c2, S.Bt[j] / a, S.wt[j], S.m[j], d[0], d[1], d[2]))
    else:
        print("  %4d  %.8f   %10.5f" % (j, S.b[j] / a, 0.0))

mono = all(S.b[j + 1] <= S.b[j] for j in range(J))
print("tops nonincreasing: %s;  all above h: %s;  b_1 = a: %s" % (mono, min(S.b) > h, S.b[1] == a))

# the curves: (S) against (G) on the common domain, and the family properties of the structural curves
print("\n# curves: max |W_j(S) - W_j(G quad8000)| on the grid of (G);  convex / nondecreasing / in [0,1] (S, 2001 points)")
for j in [k for k in (1, 2, 3, 5, 10, 20, 40, 80) if k <= JG]:
    x, W = G3.curves[j]
    msk = x <= S.b[j]
    diff = float(np.max(np.abs(S.Wvec(j, x[msk]) - W[msk])))
    xs = np.linspace(0.0, S.b[j], 2001)
    Ws = S.Wvec(j, xs)
    d1 = np.diff(Ws)
    d2 = np.diff(Ws, 2)
    print("  j = %3d: max difference %.2e;   min increment %.2e, min second difference %.2e (rel. to max %.2e), range [%.3g, %.6f]"
          % (j, diff, float(d1.min()), float(d2.min()), float(np.abs(d2).max()), float(Ws.min()), float(Ws.max())))

# (S2): W_{j+1} <= Sigma(., W_j) on [0, b_{j+1}]
print("\n# (S2) for the structural curves: max of W_{j+1} - min(1, Sigma(., W_j)) on 2001 points of [0, b_{j+1}] (must be <= 0 up to rounding)")
for j in [k for k in (0, 1, 2, 4, 9, 19, 39, 79) if k < JG]:
    xs = np.linspace(0.0, S.b[j + 1], 2001)
    Wn = S.Wvec(j + 1, xs)
    Hj = np.minimum(1.0, P.sigma_vec(xs, S.Wvec(j, xs)))
    print("  j = %3d: %.2e   (W_{j+1}(b_{j+1}) = %.12f)" % (j, float(np.max(Wn - Hj)), float(Wn[-1])))

if which == "cube1":
    print("\n# the table of A6 (cube, u = 1)")
    tab = {1: (1.0, 1.15), 2: (0.5004, 1.48), 3: (0.3633, 1.41), 4: (0.3128, 1.25), 5: (0.2914, 1.12), 6: (0.2813, 1.05),
           8: (0.2728, 1.008), 10: (0.2691, 1.001), 20: (0.2642, 0.996), 40: (0.2631, 0.996)}
    for j, (ba, ratio) in tab.items():
        print("  j = %2d: addendum b_j/a = %-7g  mine %.5f   |  addendum j^2(b_j-h)/c_*^2 = %-6g  mine %.4f"
              % (j, ba, S.b[j] / a, ratio, j * j * (S.b[j] - h) / c2))
    print("  addendum (A8): ratio 0.9958, 0.9968, 0.9973 at k = 20, 40, 80;  mine: %s"
          % ", ".join("%.5f" % (k * k * (S.b[k] - h) / c2) for k in (20, 40, 80) if k <= J))
    print("  tau_2 = 0.500 a, tau_3 = 0.361 a (theory report, quoted in A6): b_2/a = %.5f, b_3/a = %.5f" % (S.b[2] / a, S.b[3] / a))

if which == "gauss":
    print("\n# Gaussian pair: exact values derived by hand: W_1(B) = B (B_t(1) = 0), b_2 = 1/2; B_t(2) = 1/4, W_2(1/4) = 3/8, slope 5/2, b_3 = 5/14")
    print("  b_2 - 1/2 = %.2e;  B_t(1) = %.2e;  B_t(2) - 1/4 = %.2e;  W_2(B_t) - 3/8 = %.2e;  m_2 - 5/2 = %.2e;  b_3 - 5/14 = %.2e"
          % (S.b[2] - 0.5, S.Bt[1], S.Bt[2] - 0.25, S.wt[2] - 0.375, S.m[2] - 2.5, S.b[3] - 5.0 / 14.0))
    print("# against the lower bound tau_j >= 1/(4 cos^2(pi/(2j+1)))  (Proposition G of R_REPORT)")
    okg = True
    for j in rows:
        if 1 <= j <= J:
            lb = 1.0 / (4.0 * math.cos(math.pi / (2 * j + 1)) ** 2)
            okg = okg and S.b[j] >= lb
            if j <= 12 or j in (20, 40, 80, 160, 400, 1000):
                print("  j = %4d: b_j = %.9f   lower bound %.9f   b_j - lb = %.3e   (b_j - h)/(lb - h) = %.5f"
                      % (j, S.b[j], lb, S.b[j] - lb, (S.b[j] - h) / (lb - h)))
    print("  b_j >= lower bound for all 1 <= j <= %d: %s" % (J, okg))
    print("  tau_3 >= 1/(2 sqrt 2) = %.6f (R_REPORT, remark (2) after Corollary U'):  b_3 = %.6f" % (1 / (2 * math.sqrt(2)), S.b[3]))
