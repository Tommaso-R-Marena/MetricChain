#!/usr/bin/env python3
"""R9 — own verification of the numbers behind M2 of SCI-REV-0002 as they stand in the theory report at 658b77f
(Theorem 11.71(c): 116 / 451 / 8 / 19;  Proposition 11.72: 1.56 <= vol K <= 3.125).

(1) packings: exact rationals.  Inputs: R2's weight files (ours), and a vertex list that I build here from the
    counts (N, h3, h8, h11, g) of the ten bridges as stored (a) by R2 (witness_points_W64.json, witness_big.txt)
    and (b) by the theory division (wit/verified.json in the export) -- the two lists must agree.
    Condition (re-derived in NOTES.md):  L*||p_k-p_l||_c > e*(g_k+g_l) + 2*eps1 + max(L,e)*(d_k+d_l).
(2) inner volume: floating point (Qhull), own formulation: erosion of the hull C of the 14 profile densities by
    delta*B_c = intersection over facets a.x <= b of the half-spaces a.x <= b - delta*||a||_c^* .
    The dual norm of ||v||_c = 5|v3| + 3|v3+v8| + |v3+v8+v11| is computed from the 6 vertices of the unit ball.
(3) outer volume 3.125: Qhull volume of the 12 vertices of K_2 printed in Proposition 11.72(c).
(4) small arithmetic of the revised text (N4, Bezdek's constants, the factor 31, ...).
"""
import json, os, sys, itertools, re
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection

sys.dont_write_bytecode = True
R2 = "/home/user/MetricChain/experiments/science/ws_R2/out"
EXP = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f"
THY = EXP + "/experiments/coordinator_checks/limit_shape_review"


def cnorm(d):
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2])


# ---- the ten bridges: two independent records of the counts
thy = json.load(open(THY + "/wit/verified.json"))
thy_set = sorted((r["N"], tuple(r["hg"])) for r in thy.values())
r2 = json.load(open(R2 + "/witness_points_W64.json"))
r2_set = [(n, tuple(hg)) for _, n, hg in r2]
big = open(R2 + "/witness_big.txt").read()
print("R2 witness_big.txt (first lines):")
print("   " + "\n   ".join(big.strip().splitlines()[:6]))
m = re.search(r"166199\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)", big)
nine_ok = all(x in thy_set for x in r2_set)
print("nine box-64 bridges: R2's counts are all in the theory division's verified list:", nine_ok)
print("theory division's verified list:", thy_set)

exact = [(Fr(0), Fr(0), Fr(0), Fr(0), Fr(0)), (Fr(1, 2), Fr(2), Fr(3, 2), Fr(0), Fr(0)),
         (Fr(1), Fr(5), Fr(6), Fr(0), Fr(0)), (Fr(0), Fr(0), Fr(1), Fr(1), Fr(0))]
mine = exact + [tuple(Fr(c, n) for c in hg) + (Fr(168, n + 3),) for n, hg in thy_set]
V = [tuple(Fr(t) for t in line.split()) for line in open(R2 + "/rigorous_packing_vertices.txt") if not line.startswith("#")]
assert sorted(V) == sorted(mine), "vertex list of the packings differs from the points built from the counts"
print("vertex list of the packings = 4 exact points + the 10 bridges with delta = 168/(N+3): True;  max delta =",
      max(v[4] for v in V), "=", float(max(v[4] for v in V)))

e = Fr(1)
for tag, L, e1 in (("L1_e12", Fr(1), Fr(1, 2)), ("L1_e14", Fr(1), Fr(1, 4)), ("L15_e12", Fr(1, 5), Fr(1, 2)), ("L15_e14", Fr(1, 5), Fr(1, 4))):
    P = []
    for line in open(R2 + f"/rigorous_packing_{tag}.txt"):
        if line.startswith("#") or not line.strip():
            continue
        lam = [Fr(t) for t in line.split()]
        assert len(lam) == 14 and min(lam) >= 0 and sum(lam) == 1
        P.append(tuple(sum(lam[i] * V[i][k] for i in range(14)) for k in range(5)))
    assert len(set(P)) == len(P)
    worst = min(L * cnorm([a[k] - b[k] for k in range(3)]) - (e * (a[3] + b[3]) + 2 * e1 + max(L, e) * (a[4] + b[4]))
                for a, b in itertools.combinations(P, 2))
    print(f"(L, eps1) = ({L}, {e1}): {len(P)} points; smallest margin = {worst} = {float(worst):.6f}; all pairs strict: {worst > 0}")

# ---- (2) inner volume by erosion (floating point)
pts = np.array([[float(v[0]), float(v[1]), float(v[2])] for v in V])
hull = ConvexHull(pts)
print(f"\nhull C of the 14 profile densities: vol = {hull.volume:.6f}; vertices used: {len(hull.vertices)}")
delta = float(max(v[4] for v in V))
# unit ball of ||.||_c: vertices +-e_a/5, +-e_b/3, +-e_c in cumulative coordinates (a,b,c)=(v3, v3+v8, v3+v8+v11)
ball = []
for a, b, c in ((1 / 5, 0, 0), (0, 1 / 3, 0), (0, 0, 1)):
    for s in (1, -1):
        ball.append((s * a, s * (b - a), s * (c - b)))          # back to (v3, v8, v11)
ball = np.array(ball)
assert np.allclose([cnorm(v) for v in ball], 1.0)
eqs = hull.equations.copy()                                      # a.x + b0 <= 0
dual = np.max(eqs[:, :3] @ ball.T, axis=1)                       # support function of the unit ball = dual norm of a
eqs[:, 3] += delta * dual
interior = pts[hull.vertices].mean(axis=0)
hs = HalfspaceIntersection(eqs, interior)
er = ConvexHull(hs.intersections)
print(f"erosion by delta = {delta:.6f} (dual norms of the facet normals between {dual.min():.3f} and {dual.max():.3f}): vol = {er.volume:.6f}")
print("   report: vol C = 1.6317, eroded 1.5632, '1.56 <= vol K'")

# ---- (3) outer polytope K_2 from its printed vertices
K2 = np.array([(0, 0, 0), (0, 0, 2), (0, 1, 4), (0, 2, 2), (0, 2, 4.5), (0, 3, 4), (0, 3, 4.5), (.5, 2, 1.5), (.5, 2, 3),
               (.5, 3.5, 3.5), (.5, 4, 4.5), (1, 5, 6)])
h2 = ConvexHull(K2)
print(f"\nK_2 from the 12 printed vertices: vol = {h2.volume:.6f} (report 3.125); all 12 are vertices: {len(h2.vertices) == 12}")
inside = all((h2.equations[:, :3] @ p + h2.equations[:, 3]).max() <= 1e-9 for p in pts)
print("the 14 proved profile densities lie in K_2 (necessary for consistency; bridges are finite, so up to O(1/N)):",
      inside, "; largest violation:", max((h2.equations[:, :3] @ p + h2.equations[:, 3]).max() for p in pts))

# ---- (4) arithmetic of the revised text
print("\narithmetic:")
print("  3627/116 =", 3627 / 116, "; 116/15 =", 116 / 15, "; 3627/15 =", 3627 / 15)
f = lambda N, k, c: k * N ** (-1 / 3) - c / N
N = 43512
print("  17.6 N^-1/3 - 17/N at N = 43512, 43513:", f(43512, 17.6, 17), f(43513, 17.6, 17))
lo, hi = 1, 10 ** 7
g = lambda N: f(N, 17.6, 17) >= 0.25
N = 300000
while g(N):
    N += 1
print("  largest N with 17.6 N^-1/3 - 17/N >= 1/4:", N - 1)
N = 100000
while f(N, 24.1, 29.4) >= 0.5:
    N += 1
print("  largest N with 24.1 N^-1/3 - 29.4/N >= 1/2:", N - 1)
bez = 3 * (18 * np.pi) ** (1 / 3) / np.pi
print("  Bezdek constant 3(18 pi)^(1/3)/pi =", bez, "; 2*bez*2^(-2/3) =", 2 * bez * 2 ** (-2 / 3))
print("  9*2^(-2/3) + 4*4.617 =", 9 * 2 ** (-2 / 3) + 4 * 4.617, "; 9*2^(-2/3)+4*3 =", 9 * 2 ** (-2 / 3) + 12)
print("  k >= (9*2^(-2/3)+12)/35 =", (9 * 2 ** (-2 / 3) + 12) / 35, "; with Bezdek:", (9 * 2 ** (-2 / 3) + 4 * 2 * bez * 2 ** (-2 / 3)) / 35)
print("  constant term: 17 + 4*3.1 =", 17 + 4 * 3.1)
print("  c = 2 sqrt(beta (d+1)(beta'+R)) =", 2 * np.sqrt(60 * 5 * 64))
print("  168/12044 =", 168 / 12044, "; 168/(166199+3) =", 168 / 166202, "; 2.4*168/22354 =", 2.4 * 168 / 22354)
for nm, n, hg in (("22351", 22351, (382, 60150, 83122, 2349)),):
    p = [c / n for c in hg]
    print("  g - 9p3 + 3p8 - p11 at the 22 351-bead bridge:", p[3] - 9 * p[0] + 3 * p[1] - p[2])
n, hg = 166199, (1717, 376013, 687789, 131710)
print("  2h11 - 5h3 - 8N at the 166 199-bead bridge:", 2 * hg[2] - 5 * hg[0] - 8 * n, "=", (2 * hg[2] - 5 * hg[0] - 8 * n) / n, "N")
n, hg = 12041, (67, 939, 12182, 1329)
print("  density of the 12 041-bead bridge:", [round(c / n, 3) for c in hg])
