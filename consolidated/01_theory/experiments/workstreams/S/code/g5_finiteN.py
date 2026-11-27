#!/usr/bin/env python3
"""(a) Finite-N version of the proved outer polytope and the resulting upper bounds for N^P_cov(eps1 N), N >= N0.
    Facets (exact certificates, out/lp_exact.txt):  c.p <= b  in the limit;  for a walk with N beads
        c.(h/N) <= b + (4 M_c + c3 + 2 c8)/N       (two end beads; h = e - (N-1, N-2, 0)).
(b) Surface law of the extreme profile:  max ||N^x||_1 / N  against 35 (1 - k N^(-1/3)).
usage: g5_finiteN.py OUT_DIR ENG_DATA_DIR
"""
import sys, os, itertools
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from g5_bounds import to_u, vol_bound, bcc_count

out, eng = sys.argv[1], sys.argv[2]
# facets (c3, c8, c11), b, M from the exact certificates
F = [((-4, 2, -1), 2, 6), ((-3, 0, 2), 9, 3), ((-2, 1, 0), 3, 2), ((-1, 0, 0), 0, 0.5), ((-1, 1, -1), 0, 3), ((-1, 2, -1), 3, 4),
     ((0, -1, 2), 7, 1), ((3, 4, -3), 5, 6), ((4, -1, 0), 0, 5), ((6, -2, 1), 2, 6), ((6, -1, 0), 1, 6)]
def poly(N0):
    hs = []
    for c, b, M in F:
        add = 0.0 if N0 is None else (4 * M + c[0] + 2 * c[1]) / N0
        hs.append([c[0], c[1], c[2], -(b + add)])
    hs = np.array(hs, float)
    hi = HalfspaceIntersection(hs, np.array([0.3, 2.5, 3.0]))
    V = hi.intersections
    return V[ConvexHull(V).vertices]
print("# (a) volumetric upper bounds  Pack <= vol(X + B(r/2))/vol(B(r/2))  for the proved outer polytope enlarged for N >= N0")
print("#   N0      volume(p)   | L=1,eps1=1/2   L=1,eps1=1/4   L=1/5,eps1=1/2   L=1/5,eps1=1/4")
for N0 in (27, 100, 300, 1000, 10000, None):
    V = poly(N0)
    vol = ConvexHull(V).volume
    row = f"  {str(N0):>6}   {vol:9.4f}   |"
    for L, e1 in ((1.0, 0.5), (1.0, 0.25), (0.2, 0.5), (0.2, 0.25)):
        row += f" {vol_bound(to_u(V), e1 / L):12.0f}  "
    print(row)

print("\n# (b) extreme profile norm per bead (walks: the other division's class tables; bridges: own enumeration)")
print("#   N   max||N||_1/N walks   k = (1 - max/35) N^(1/3)   | bridges   k")
for N in range(8, 28):
    H = []
    for line in open(f"{eng}/dia_Sc12_n{N-3}.txt"):
        if line.startswith('#'): continue
        a = list(map(int, line.split())); H.append(9 * a[0] + 4 * a[1] + a[2])
    m = max(H) / N
    row = f"  {N:3d}   {m:8.4f}             {(1 - m / 35) * N ** (1/3):6.3f}"
    p = f"{out}/bridge_N{N}.txt"
    if os.path.exists(p):
        Hb = []
        for line in open(p):
            if line.startswith('#'): continue
            a = line.split(); Hb.append(9 * int(a[0]) + 4 * int(a[1]) + int(a[2]))
        mb = max(Hb) / N
        row += f"                  | {mb:8.4f}  {(1 - mb / 35) * N ** (1/3):6.3f}"
    print(row)
