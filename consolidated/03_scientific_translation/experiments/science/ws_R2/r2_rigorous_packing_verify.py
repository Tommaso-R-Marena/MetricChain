#!/usr/bin/env python3
"""R2 — stand-alone verifier of the packings of r2_rigorous_packing.py (exact rational arithmetic).
Reads out/rigorous_packing_vertices.txt (the proved points q_i of K^br with their uncertainty delta_i)
and out/rigorous_packing_<tag>.txt (weights lambda per packing point); checks lambda >= 0, sum = 1, and
   L ||p_k - p_l||_c  >  e (g_k + g_l) + 2 eps1 + max(L,e) (d_k + d_l),   (p,g) = sum lambda_i q_i, d = sum lambda_i delta_i,
for all pairs (e = 1).  By convexity of K^br and Theorem 11.71(b) the number of points is then a lower
bound for liminf_N N^P_cov(eps1 N)."""
import os, sys, itertools
from fractions import Fraction as Fr
HERE=os.path.dirname(os.path.abspath(__file__))
def nc(d): return 5*abs(d[0])+3*abs(d[0]+d[1])+abs(d[0]+d[1]+d[2])
V=[[Fr(t) for t in line.split()] for line in open(f"{HERE}/out/rigorous_packing_vertices.txt") if not line.startswith("#")]
for tag,L,e1 in (("L1_e12",Fr(1),Fr(1,2)),("L1_e14",Fr(1),Fr(1,4)),("L15_e12",Fr(1,5),Fr(1,2)),("L15_e14",Fr(1,5),Fr(1,4))):
    f=f"{HERE}/out/rigorous_packing_{tag}.txt"
    if not os.path.exists(f): continue
    P=[]
    for line in open(f):
        if line.startswith("#"): continue
        lam=[Fr(t) for t in line.split()]
        assert len(lam)==len(V) and all(x>=0 for x in lam) and sum(lam)==1
        q=[sum(lam[i]*V[i][k] for i in range(len(V))) for k in range(5)]
        P.append(q)
    ok=all(L*nc([a[k]-b[k] for k in range(3)]) > (a[3]+b[3])+2*e1+max(L,Fr(1))*(a[4]+b[4]) for a,b in itertools.combinations(P,2))
    print(f"(L,eps1)=({L},{e1}): {len(P)} points; all weights valid; pairwise condition verified exactly: {ok}")
