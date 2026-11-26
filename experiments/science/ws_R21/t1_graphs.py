"""T1 — the graphs used in R21 (plane, d = 2): rank, rigidity, redundant rigidity, vertex
connectivity, stress-matrix rank (generic global rigidity), and connectivity of the generic
rigidity matroid by brute force over all bipartitions of the edge set.  Own code.

Expected (theory): GGR in the plane  <=>  K_n (n <= 3)  or  3-connected and redundantly rigid
(Jackson-Jordan 2005)  <=>  (n >= 4) stress matrix of rank n - 3 at a generic point
(Connelly 2005; Gortler-Healy-Thurston 2010).  For n >= d + 2: GGR  =>  matroid connected
(the cited 2022 theorem).  The converse fails: 2K4_2sum, 2K4_edge.
"""
import sys
import numpy as np
from r21_common import *

rng = np.random.default_rng(2101)
G = graph_table()
print("T1 graphs  start", now())
print(f"{'graph':10s} {'N':>2s} {'m':>3s} {'rank':>4s} {'2N-3':>4s} {'rigid':>5s} {'redund':>6s} {'kappa':>5s} "
      f"{'stress_rk':>9s} {'N-3':>3s} {'GGR(stress)':>11s} {'GGR(JJ)':>7s} {'#separators':>11s} {'connected':>9s}")
viol = 0
for name, (N, E) in G.items():
    res = []
    for trial in range(3):  # three random points: the generic quantities must agree
        P = rng.standard_normal((N, 2))
        rk, seps = matroid_separators(P, E)
        sr, sdim = stress_rank(P, E, rng)
        rr = redundantly_rigid(P, E)
        res.append((rk, len(seps), sr, rr))
    if len(set(res)) != 1:
        print("   !! non-generic disagreement between random points for", name, res)
        viol += 1
    rk, nsep, sr, rr = res[0]
    kap = vertex_connectivity(N, E)
    rigid = rk == 2 * N - 3
    ggr_stress = (N <= 3 and len(E) == N * (N - 1) // 2) or (N >= 4 and sr == N - 3)
    ggr_jj = (N <= 3 and len(E) == N * (N - 1) // 2) or (N >= 4 and kap >= 3 and rr)
    connected = nsep == 0
    print(f"{name:10s} {N:2d} {len(E):3d} {rk:4d} {2*N-3:4d} {str(rigid):>5s} {str(rr):>6s} {kap:5d} "
          f"{sr:9d} {N-3:3d} {str(ggr_stress):>11s} {str(ggr_jj):>7s} {nsep:11d} {str(connected):>9s}")
    if ggr_stress != ggr_jj:
        print("   !! stress test and Jackson-Jordan criterion disagree for", name)
        viol += 1
    if ggr_stress and N >= 4 and not connected:
        print("   !! GGR on >= d+2 vertices but matroid not connected (would contradict the cited theorem):", name)
        viol += 1
print("violations of the consistency checks:", viol)
print("DONE t1_graphs", now())
