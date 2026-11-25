#!/usr/bin/env python3
"""Inner approximation of the limit set from periodic chain systems (code/pchain): hull of the densities
(p3, p8, p11) and of (p3, p8, p11, gmin/n); gauche density on the 3D hull vertices.
usage: pchain_hull.py OUT_DIR KMAX [LP_VERTICES.npy]
"""
import sys, os
import numpy as np
from fractions import Fraction
from scipy.spatial import ConvexHull

out, kmax = sys.argv[1], int(sys.argv[2])
pts = {}
for K in range(1, kmax + 1):
    p = f"{out}/pchain_K{K}.txt"
    if not os.path.exists(p): continue
    for line in open(p):
        if line.startswith('#'): continue
        n, e3, e8, e11, gmin, gmax = map(int, line.split())
        key = (Fraction(e3, n) - 1, Fraction(e8, n) - 1, Fraction(e11, n))
        v = pts.get(key)
        g0, g1 = Fraction(gmin, n), Fraction(gmax, n)
        if v is None:
            pts[key] = [g0, g1, (K, n, e3, e8, e11, gmin)]
        else:
            if g0 < v[0]: v[0] = g0; v[2] = (K, n, e3, e8, e11, gmin)
            if g1 > v[1]: v[1] = g1
keys = list(pts)
P = np.array([[float(x) for x in k] for k in keys])
hull = ConvexHull(P)
print(f"# periodic chain systems (all components infinite), cell index <= {kmax}: {len(P)} distinct profile densities")
print(f"# 3D hull: {len(hull.vertices)} vertices, volume {hull.volume:.6f} (p-coordinates), x36 = {36*hull.volume:.4f} (weighted)")
print("# vertices (p3, p8, p11) | smallest and largest gauche density found | witness (K, n, e3, e8, e11, g)")
for i in sorted(hull.vertices, key=lambda i: tuple(P[i])):
    k = keys[i]; v = pts[k]
    print(f"  ({str(k[0]):>6}, {str(k[1]):>6}, {str(k[2]):>6})   gmin/n = {str(v[0]):>5}  gmax/n = {str(v[1]):>5}   {v[2]}")
np.save(f"{out}/pchain_hull_vertices_K{kmax}.npy", P[hull.vertices])
# zero-gauche systems only
Z = np.array([[float(x) for x in k] for k in keys if pts[k][0] == 0])
hz = ConvexHull(Z)
print(f"# zero-gauche (rod) systems only: {len(Z)} points, hull volume {hz.volume:.6f} ({len(hz.vertices)} vertices)")
# lower boundary: 4D hull of (p, gmin/n); value of the lower envelope at the 3D hull vertices and the largest gmin on any 3D-hull vertex
G = np.array([float(pts[k][0]) for k in keys])
print(f"# largest gmin/n over the 3D hull vertices: {max(float(pts[keys[i]][0]) for i in hull.vertices):.4f}")
P4 = np.column_stack([P, G])
h4 = ConvexHull(P4)
low = h4.equations[h4.equations[:, 3] < -1e-9]
def env(p):
    return ((low[:, :3] @ p + low[:, 4]) / (-low[:, 3])).max()
# maximise the lower envelope over the 3D hull: sample points of the hull (vertices, facet centroids, random convex combinations)
rng = np.random.default_rng(1)
V = P[hull.vertices]
samples = [v for v in V]
for s in hull.simplices:
    samples.append(P[s].mean(axis=0))
for _ in range(20000):
    w = rng.dirichlet(np.ones(len(V)) * 0.3)
    samples.append(w @ V)
vals = np.array([max(0.0, env(p)) for p in samples])
i = int(vals.argmax())
print(f"# lower envelope gamma of the 4D hull: max over {len(samples)} sample points of the 3D hull = {vals.max():.4f} at p = {np.round(samples[i], 4)}; "
      f"fraction of samples with gamma > 0.01: {(vals > 0.01).mean():.3f}; mean {vals.mean():.4f}")
if len(sys.argv) > 3:
    lpv = np.load(sys.argv[3])
    print("# LP vertices: max facet violation w.r.t. the chain-system hull (<= 1e-7: attained)")
    for v in sorted(map(tuple, lpv)):
        viol = (hull.equations[:, :3] @ np.array(v) + hull.equations[:, 3]).max()
        print(f"  ({v[0]:8.5f}, {v[1]:8.5f}, {v[2]:8.5f})   violation {viol:9.5f}   {'attained' if viol < 1e-7 else ''}")
