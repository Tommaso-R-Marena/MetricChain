#!/usr/bin/env python3
"""Z4: the ENVELOPE sequence -- the best convex sub-solution of the slope map, started from the flat family at the
non-adaptive exponent a (no restart near h, no range condition).

    W_0 = 0 on [0, b_0],  b_0 = a;      b_{j+1} = sup{B <= b_j : Sigma(B, W_j(B)) < infinity}  (the root of W_j(B) = 1 - B/a);
    W_{j+1} = the lower convex envelope of  min(1, Sigma(B, W_j(B)))  on [0, b_{j+1}]  (value at the right end: its limit).

Every (W_j, b_j) is convex, nondecreasing, continuous, with values in [0, 1] and W_j(0) = 0, and
W_{j+1} <= Sigma(., W_j) by construction: Corollary U' of R_REPORT applies at every step with no further condition,
so tau_{j+1} <= b_j at the exponent level, and Proposition Z3 of Z_REPORT applies to the grid families of these curves.
By monotonicity of the step this sequence is at least as good as any other sub-solution sequence that starts above
it (in particular the cut orbit curves restarted at a level k_1 with b_{k_1} <= h + eps_1).

FLOATING POINT, ON A GRID: the numbers are approximations [N], not certified bounds (the envelope of grid values
of a function is not a minorant of the function between grid points; the grid is refined to check stability).
Prints b_j/a, (b_j - h) j^2 / c_*^2, and the comparison with the exact recursion's tau_j where known
(tau_2 = 0.500 a, tau_3 = 0.361 a at u = 1: theory report 11.19).
Usage: python3 z4_env.py [u] [J] [grid]       (default 1.0 60 4000)
"""
import math
import sys

import numpy as np

import zetalib as Z

u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
J = int(sys.argv[2]) if len(sys.argv) > 2 else 60
NG = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
P = Z.rlib.Cube(u).setup()
a, h, cst = P.a, P.h, P.const
lamu = math.log(2 / (1 + math.exp(-u)))




def env_sequence(J, NG):
    C = Z.EnvZ(u, J - 2, NG)
    return C.curves, C.b


if __name__ == "__main__":
    curves, tops = env_sequence(J, NG)
    curves2, tops2 = env_sequence(min(J, 30), 2 * NG)
    print("# cube u = %g: a = %.6f, h = %.6f (h/a = %.4f), c_*^2 = %.6f;  grid %d (and %d for the first %d levels)" % (u, a, h, h / a, cst, NG, 2 * NG, min(J, 30)))
    print("#   j    b_j/a     (b_j - h)/h   j^2 (b_j - h)/c_*^2   change with the finer grid")
    for j in list(range(0, min(J, 12) + 1)) + [k for k in (15, 20, 30, 40, 60, 80, 100, 150, 200) if 12 < k <= J]:
        d = abs(tops2[j] - tops[j]) / a if j < len(tops2) else float("nan")
        print("  %4d  %.5f   %9.4f      %8.4f            %.1e" % (j, tops[j] / a, (tops[j] - h) / h, j * j * (tops[j] - h) / cst, d))
    ok = all(tops[j + 1] <= tops[j] + 1e-12 for j in range(J)) and tops[-1] > h
    print("monotone tops, all above h: %s" % ok)
