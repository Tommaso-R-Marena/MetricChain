#!/usr/bin/env python3
"""R9, item 4 (consequence): the numbers of Theorem 11.71(c) and Proposition 11.72 with EXACT points of K^br.
Vertex list: the four exact points and, for each explicit bridge, qhat/(N+3) = ((h,g) + A + B)/(N+3) (Theorem R9.1(d)),
with A, B from out/witness_ends_W64.json and out/witness_ends_W128_only.json (my code on regenerated coordinates).
(1) R2's four packings (same weights, same order of vertices) re-evaluated on the exact vertices, all radii zero:
    L ||p_k - p_l||_c > e (g_k + g_l) + 2 eps1   for all pairs, in exact rationals.
(2) inner volume = volume of the hull of the exact profile points (no erosion): exact rational volume by a fan
    triangulation of the Qhull facets (each facet's orientation fixed with an interior point)."""
import json, itertools, os, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull

R2 = "/home/user/MetricChain/experiments/science/ws_R2/out"
ends = json.load(open("out/witness_ends_W64.json"))
big = "out/witness_ends_W128_only.json"
if os.path.exists(big):
    ends += json.load(open(big))
byN = {N: (hg, a, b, q) for _, N, hg, a, b, q in ends}
print("bridges with end corrections:", sorted(byN))

def cnorm(d):
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2])

# R2's vertex list (order of the weight columns): rows p3 p8 p11 g delta, delta = 168/(N+3) identifies N
Vold = [tuple(Fr(t) for t in line.split()) for line in open(R2 + "/rigorous_packing_vertices.txt") if not line.startswith("#")]
Vnew = []
missing = []
for v in Vold:
    if v[4] == 0:
        Vnew.append(v[:4] + (Fr(0),)); continue
    N = int(Fr(168) / v[4]) - 3
    assert Fr(168, N + 3) == v[4]
    if N in byN:
        hg, a, b, q = byN[N]
        assert tuple(Fr(c, N) for c in hg) == v[:4]
        Vnew.append(tuple(Fr(c, N + 3) for c in q) + (Fr(0),))
    else:                                   # no coordinates: keep the density, with the improved radius 108/(N+3)
        missing.append(N)
        Vnew.append(v[:4] + (Fr(108, N + 3),))
print("vertices without end corrections (kept with radius 108/(N+3)):", missing)
e = Fr(1)
for tag, L, e1 in (("L1_e12", Fr(1), Fr(1, 2)), ("L1_e14", Fr(1), Fr(1, 4)), ("L15_e12", Fr(1, 5), Fr(1, 2)), ("L15_e14", Fr(1, 5), Fr(1, 4))):
    P = []
    for line in open(R2 + f"/rigorous_packing_{tag}.txt"):
        if line.startswith("#") or not line.strip():
            continue
        lam = [Fr(t) for t in line.split()]
        P.append(tuple(sum(lam[i] * Vnew[i][k] for i in range(14)) for k in range(5)))
    worst = min(L * cnorm([a[k] - b[k] for k in range(3)]) - (e * (a[3] + b[3]) + 2 * e1 + max(L, e) * (a[4] + b[4]))
                for a, b in itertools.combinations(P, 2))
    print(f"(L, eps1) = ({L}, {e1}): R2's {len(P)} weight vectors on the exact vertices: smallest margin {float(worst):+.6f}; all pairs strict: {worst > 0}")

# (2) exact volume of the hull of the exact profile points
pts = [v[:3] for v in Vnew if v[4] == 0]
F = np.array([[float(c) for c in p] for p in pts])
hull = ConvexHull(F)
c = [sum(p[i] for p in pts) / len(pts) for i in range(3)]     # an interior point (exact)
def det3(a, b, cc):
    return (a[0] * (b[1] * cc[2] - b[2] * cc[1]) - a[1] * (b[0] * cc[2] - b[2] * cc[0]) + a[2] * (b[0] * cc[1] - b[1] * cc[0]))
vol = Fr(0)
for simplex in hull.simplices:
    a, b, d = (pts[i] for i in simplex)
    vol += abs(det3([a[i] - c[i] for i in range(3)], [b[i] - c[i] for i in range(3)], [d[i] - c[i] for i in range(3)])) / 6
print(f"hull of the {len(pts)} exact profile points: Qhull volume {hull.volume:.6f}; exact rational sum over the cones of its {len(hull.simplices)} facets"
      f" from an interior point: {float(vol):.6f}  (a lower bound for vol K provided the facet list is that of the hull; the two agree)")
