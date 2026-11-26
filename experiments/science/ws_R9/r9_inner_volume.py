#!/usr/bin/env python3
"""R9, item 4 (consequence): what the exact semigroup does to the proved inner volume of the profile body K.
Inputs: the counts (N, h3, h8, h11, g) of the ten explicit bridges (theory division's wit/verified.json = R2's records).
(a) report (658b77f): every bridge density h/N is within 168/(N+3) of K  ->  erosion of the hull by 168/12044: 1.5632
(b) with the coboundary identity:  (h + A + B)/(N+3) is IN K, A + B in [0,1]x[0,9]x[0,14]  ->
      * h/N is within 108/(N+3) of K^br (norm ||.||_c + |g|; for the profile part alone 105/(N+3));
      * the point (h + (1/2, 9/2, 7))/(N+3) is within 29.5/(N+3) of K (profile part of the norm).
Floating point (Qhull); own formulation of the erosion (support functions)."""
import json
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection

EXP = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f"
ver = json.load(open(EXP + "/experiments/coordinator_checks/limit_shape_review/wit/verified.json"))
br = sorted((r["N"], tuple(r["hg"])) for r in ver.values())
exact = np.array([(0, 0, 0), (0.5, 2, 1.5), (1, 5, 6), (0, 0, 1)], float)

ball = []
for a, b, c in ((1 / 5, 0, 0), (0, 1 / 3, 0), (0, 0, 1)):
    for s in (1, -1):
        ball.append((s * a, s * (b - a), s * (c - b)))
ball = np.array(ball)

def eroded_volume(pts, delta):
    hull = ConvexHull(pts)
    if delta == 0:
        return hull.volume, hull.volume
    eqs = hull.equations.copy()
    eqs[:, 3] += delta * np.max(eqs[:, :3] @ ball.T, axis=1)
    hs = HalfspaceIntersection(eqs, pts[hull.vertices].mean(axis=0))
    return hull.volume, ConvexHull(hs.intersections).volume

Nmin = min(n for n, _ in br)
pts_a = np.vstack([exact, np.array([[c / n for c in hg[:3]] for n, hg in br])])
v, e = eroded_volume(pts_a, 168 / (Nmin + 3))
print(f"(a) hull of h/N: {v:.6f}; eroded by 168/{Nmin+3} = {168/(Nmin+3):.6f}: {e:.6f}   (report 1.6317, 1.5632)")
v, e = eroded_volume(pts_a, 105 / (Nmin + 3))
print(f"(b1) the same hull eroded by 105/{Nmin+3} = {105/(Nmin+3):.6f} (profile part of 3R = 108 without the gauche term): {e:.6f}")
pts_b = np.vstack([exact, np.array([[(hg[0] + 0.5) / (n + 3), (hg[1] + 4.5) / (n + 3), (hg[2] + 7) / (n + 3)] for n, hg in br])])
v, e = eroded_volume(pts_b, 29.5 / (Nmin + 3))
print(f"(b2) hull of (h + (1/2, 9/2, 7))/(N+3): {v:.6f}; eroded by 29.5/{Nmin+3} = {29.5/(Nmin+3):.6f}: {e:.6f}")
# if the ten bridges happened to be clean (A = B = 0), or after computing A + B from coordinates: exact points, no erosion
lo = ConvexHull(np.vstack([exact, np.array([[c / (n + 3) for c in hg[:3]] for n, hg in br])])).volume
hi = ConvexHull(np.vstack([exact, np.array([[(hg[0] + 1) / (n + 3), (hg[1] + 9) / (n + 3), (hg[2] + 14) / (n + 3)] for n, hg in br])])).volume
print(f"(c) with A + B known from coordinates the ten points are exact; the hull volume would lie between about {min(lo,hi):.6f} and {max(lo,hi):.6f}"
      f" (the two extreme cases A + B = 0 and A + B = (1, 9, 14))")
print("    outer bound (K_2): 3.125")
