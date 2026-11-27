#!/usr/bin/env python3
"""Consistency check of the outer bounds against all enumerated periodic structures:
 (1) every periodic site set with all degrees >= 2 (code/periodic, index <= 12) satisfies the eleven inequalities of Theorem 4.2;
 (2) every periodic chain system (code/pchain, index <= 12) lies in the profile polytope of the path-cluster LP, and its
     gauche density is >= gamma_LP at its profile (checked on the hull vertices and a sample)."""
import sys, os, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
out = sys.argv[1]
F = [((-4, 2, -1), 2), ((-3, 0, 2), 9), ((-2, 1, 0), 3), ((-1, 0, 0), 0), ((-1, 1, -1), 0), ((-1, 2, -1), 3),
     ((0, -1, 2), 7), ((3, 4, -3), 5), ((4, -1, 0), 0), ((6, -2, 1), 2), ((6, -1, 0), 1)]
n1 = 0; worst = Fr(-10**9)
for K in range(1, 13):
    for line in open(f"{out}/periodic_K{K}.txt"):
        if line.startswith('#'): continue
        n, e3, e8, e11 = map(int, line.split())
        p = (Fr(e3, 2 * n) - 1, Fr(e8, 2 * n) - 1, Fr(e11, 2 * n))
        for c, b in F:
            v = c[0] * p[0] + c[1] * p[1] + c[2] * p[2] - b
            assert v <= 0, (K, n, e3, e8, e11, c)
            worst = max(worst, v)
        n1 += 1
print(f"(1) {n1} periodic site-set keys (index <= 12): all eleven inequalities hold exactly; largest value of c.p - b: {worst}")
V = np.load(f"{out}/lp4_vertices3.npy"); h = ConvexHull(V)
pts = {}
for K in range(1, 13):
    for line in open(f"{out}/pchain_K{K}.txt"):
        if line.startswith('#'): continue
        n, e3, e8, e11, g0, g1 = map(int, line.split())
        k = (e3 / n - 1, e8 / n - 1, e11 / n)
        pts[k] = min(pts.get(k, 9), g0 / n)
P = np.array(list(pts)); G = np.array([pts[tuple(k)] for k in P])
viol = (P @ h.equations[:, :3].T + h.equations[:, 3]).max()
print(f"(2) {len(P)} chain-system densities: largest violation of a facet of the path-cluster LP polytope: {viol:.2e}")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cluster_lp4 import build
CF, f3, f8, f11, fg, Aeq, beq = build()
A2 = np.vstack([Aeq.toarray(), 2 * f3, f8, f11])
rng = np.random.default_rng(0)
idx = rng.choice(len(P), size=400, replace=False)
mn = 9
for i in idx:
    b2 = np.concatenate([beq, [P[i][0] + 1, P[i][1] + 1, P[i][2]]])
    res = linprog(2 * fg, A_eq=A2, b_eq=b2, bounds=(0, None), method="highs")
    assert res.status == 0
    mn = min(mn, G[i] - res.fun)
print(f"    on 400 random chain systems: min (gauche density - gamma_LP) = {mn:.2e}  (must be >= 0 up to rounding)")
