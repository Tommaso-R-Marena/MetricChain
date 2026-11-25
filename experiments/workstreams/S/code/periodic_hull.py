#!/usr/bin/env python3
"""Convex hull of the densities (p3, p8, p11) of all periodic site sets found by code/periodic (deg >= 2),
compared with the vertices of the bond-cluster LP outer bound.
usage: periodic_hull.py OUT_DIR KMAX LP_VERTICES.npy
"""
import sys, os
import numpy as np
from fractions import Fraction
from scipy.spatial import ConvexHull

out, kmax, lpv = sys.argv[1], int(sys.argv[2]), np.load(sys.argv[3])
pts = {}
for K in range(1, kmax + 1):
    p = f"{out}/periodic_K{K}.txt"
    if not os.path.exists(p): continue
    for line in open(p):
        if line.startswith('#'): continue
        n, e3, e8, e11 = map(int, line.split())
        key = (Fraction(e3, 2 * n) - 1, Fraction(e8, 2 * n) - 1, Fraction(e11, 2 * n))
        if key not in pts:
            pts[key] = (K, n, e3, e8, e11)
P = np.array([[float(x) for x in k] for k in pts])
keys = list(pts)
hull = ConvexHull(P)
print(f"# periodic site sets with every occupied site of degree >= 2, cell index <= {kmax}: {len(P)} distinct density points")
print(f"# hull: {len(hull.vertices)} vertices, volume {hull.volume:.6f} (p-coordinates), x36 = {36*hull.volume:.4f} (weighted coordinates)")
print("# vertices: (p3, p8, p11)   first witness (index K, n per cell, E3, E8, E11)")
for i in sorted(hull.vertices, key=lambda i: tuple(P[i])):
    k = keys[i]
    print(f"  ({str(k[0]):>6}, {str(k[1]):>6}, {str(k[2]):>6})   K={pts[k][0]} n={pts[k][1]} E3={pts[k][2]} E8={pts[k][3]} E11={pts[k][4]}")
print("# LP vertices: inside the periodic hull?  (max facet violation; <= 1e-9 means inside)")
for v in sorted(map(tuple, lpv)):
    viol = (hull.equations[:, :3] @ np.array(v) + hull.equations[:, 3]).max()
    print(f"  ({v[0]:8.5f}, {v[1]:8.5f}, {v[2]:8.5f})   violation {viol:9.5f}   {'attained' if viol < 1e-9 else 'NOT attained by these periodic sets'}")
np.save(f"{out}/periodic_hull_vertices.npy", P[hull.vertices])
