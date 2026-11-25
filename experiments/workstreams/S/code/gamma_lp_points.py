#!/usr/bin/env python3
"""gamma_LP (smallest gauche density allowed by the path-cluster LP) at the gauche-rich vertices of the inner hull.
gamma_LP(p) > 0 at a profile density p that is attained by a chain system proves (up to floating-point LP and the
realisability of the chain system by walks) that gamma is not identically zero on the limit profile set."""
import numpy as np
from scipy.optimize import linprog
from cluster_lp4 import build
CF, f3, f8, f11, fg, Aeq, beq = build()
A2 = np.vstack([Aeq.toarray(), 2 * f3, f8, f11])
pts = [((0, 12/5, 22/5), 4/5), ((0, 18/7, 61/14), 5/7), ((0, 27/14, 4), 6/7), ((1/16, 23/8, 35/8), 3/4), ((1/3, 10/3, 5), 2/3),
       ((0, 0, 3/2), 1), ((0, 1/2, 9/4), 1), ((0, 1/4, 7/4), 1), ((1/3, 5/3, 3), 2/3), ((1/8, 5/4, 5/4), 1/2), ((0, 3, 4), 0), ((0, 1, 3), 0)]
print("# p = (p3, p8, p11) | gauche density of the best chain system found (index <= 12) | gamma_LP(p)")
for p, g in pts:
    b2 = np.concatenate([beq, [p[0] + 1, p[1] + 1, p[2]]])
    res = linprog(2 * fg, A_eq=A2, b_eq=b2, bounds=(0, None), method="highs")
    val = f"{res.fun:.4f}" if res.status == 0 else "infeasible (outside the LP polytope)"
    print(f"  ({p[0]:.4f}, {p[1]:.4f}, {p[2]:.4f}) | {g:.4f} | {val}")
