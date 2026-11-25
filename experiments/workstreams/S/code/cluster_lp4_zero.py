#!/usr/bin/env python3
"""Path-cluster LP restricted to gauche density q <= Q0 (default 0): outer bound for the set of profile densities
that walks can reach with gauche density at most Q0, and the function gamma_LP on a grid (lower bound for gamma).
usage: cluster_lp4_zero.py NDIR OUT.npy [Q0]
"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import vstack, csr_matrix
from scipy.spatial import ConvexHull
from fractions import Fraction
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cluster_lp4 import build, fib_sphere

nd = int(sys.argv[1]); outp = sys.argv[2]; Q0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
CF, f3, f8, f11, fg, Aeq, beq = build()
pts = {}
dirs = [np.array(d, float) for d in itertools.product((-1, 0, 1), repeat=3) if any(d)]
for d in fib_sphere(nd):
    dirs.append(np.array([9 * d[0], 4 * d[1], d[2]]))
for c in dirs:
    obj = c[0] * 2 * f3 + c[1] * f8 + c[2] * f11
    res = linprog(-obj, A_eq=Aeq, b_eq=beq, A_ub=(2 * fg).reshape(1, -1), b_ub=[Q0], bounds=(0, None), method="highs")
    assert res.status == 0
    mu = res.x
    p = (2 * f3 @ mu - 1, f8 @ mu - 1, f11 @ mu)
    pts[tuple(np.round(p, 7))] = 1
P = np.array(sorted(pts))
h = ConvexHull(P)
print(f"# path-cluster LP with gauche density <= {Q0}: {len(h.vertices)} vertices, volume {h.volume:.6f} (p-coordinates), x36 = {36*h.volume:.4f}")
for i in sorted(h.vertices, key=lambda i: tuple(P[i])):
    fr = [str(Fraction(float(x)).limit_denominator(120)) for x in P[i]]
    print(f"  ({', '.join(f'{s:>7}' for s in fr)})")
np.save(outp, P[h.vertices])
