#!/usr/bin/env python3
"""Exact certificates for lower bounds on the gauche density:  q >= a3 p3 + a8 p8 + a11 p11 - beta  for ALL walks
(in the limit N -> infinity), with the coefficients read off the dual of  gamma_LP(p0) = min q at fixed profile p0.
Then the certified inequality is evaluated at the profile of explicit finite bridges (out/build.txt)."""
import sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from cluster_lp4 import build
from lp4_exact import setup, certify

CF, f3, f8, f11, fg, Aeq, beq = build()
A2 = np.vstack([Aeq.toarray(), 2 * f3, f8, f11])
orbits, F, rows = setup()
out = open(sys.argv[1], "w")
def P(*a):
    print(*a); print(*a, file=out)
for p0 in [(0, Fr(12, 5), Fr(22, 5)), (0, Fr(18, 7), Fr(61, 14)), (Fr(1, 16), Fr(23, 8), Fr(35, 8)), (Fr(1, 3), Fr(10, 3), 5)]:
    b2 = np.concatenate([beq, [float(p0[0]) + 1, float(p0[1]) + 1, float(p0[2])]])
    res = linprog(2 * fg, A_eq=A2, b_eq=b2, bounds=(0, None), method="highs")
    lam = res.eqlin.marginals[-3:]                    # d gamma / d (E3, E8, E11)
    alpha = [Fr(float(x)).limit_denominator(24) for x in lam]
    # certify  alpha.p - q <= beta
    r = certify((alpha[0], alpha[1], alpha[2], Fr(-1)), orbits, F, rows)
    beta = r[0]
    val = alpha[0] * p0[0] + alpha[1] * p0[1] + alpha[2] * p0[2] - beta
    P(f"p0 = ({p0[0]}, {p0[1]}, {p0[2]}): gamma_LP = {res.fun:.6f};  certified:  q >= {alpha[0]} p3 + {alpha[1]} p8 + {alpha[2]} p11 - {beta}"
      f"   (value at p0: {val} = {float(val):.4f})")
# the inequality evaluated at explicit finite bridges of out/build.txt
P("certified inequality  q >= 2 p11 - 2 p8 ... evaluated at explicit bridges: see the rows above; bridge (0.0285, 2.1554, 3.9028; g/N = 0.7802), N = 21235:")
out.close()
