#!/usr/bin/env python3
"""R2 — lattice packings in T0 (better than greedy): in barycentric coordinates (alpha,beta) of
T0 = {alpha V1 + beta V2 : alpha,beta >= 0, alpha+beta <= 1} the norm ||.||_c is
n(alpha,beta) = |5/2 a + 5 b| + |15/2 a + 18 b| + |4 a + 12 b|, whose unit ball is a centrally
symmetric hexagon H with vertices +-v1,+-v2,+-v3; the lattice (d/2)<v1+v2, v2+v3> is a packing
lattice with minimal distance exactly d.  Scan offsets; verify the result pairwise, exactly.
"""
import sys, itertools
from fractions import Fraction as Fr
L1=(Fr(5,2),Fr(5)); L2=(Fr(15,2),Fr(18)); L3=(Fr(4),Fr(12))
def n(a,b): return abs(L1[0]*a+L1[1]*b)+abs(L2[0]*a+L2[1]*b)+abs(L3[0]*a+L3[1]*b)
# vertices: kernels of the three forms
vs=[]
for l in (L1,L2,L3):
    p=(l[1],-l[0]); s=n(*p); vs.append((p[0]/s,p[1]/s))
# order cyclically by angle
import math
ang=lambda v: math.atan2(float(v[1]),float(v[0]))
cand=vs+[(-v[0],-v[1]) for v in vs]
cand.sort(key=ang)
v1,v2,v3=cand[0],cand[1],cand[2]
assert n(*v1)==1 and n(*v2)==1 and n(*v3)==1
w1=(v1[0]+v2[0],v1[1]+v2[1]); w2=(v2[0]+v3[0],v2[1]+v3[1])
assert n(*w1)==2 and n(*w2)==2 and n(w1[0]-w2[0],w1[1]-w2[1])==2
area_H=abs(float(v1[0]*v2[1]-v1[1]*v2[0])+float(v2[0]*v3[1]-v2[1]*v3[0])+float(v3[0]*(-v1[1])-v3[1]*(-v1[0])))
print(f"hexagon vertices v1={v1}, v2={v2}, v3={v3}; area(H) = {area_H:.6f} (in barycentric coordinates; T0 has area 1/2)")
def best_packing(d, steps=60, slack=Fr(1,2000)):
    s=d/2*(1+slack)
    g1=(w1[0]*s,w1[1]*s); g2=(w2[0]*s,w2[1]*s)
    det=g1[0]*g2[1]-g1[1]*g2[0]
    R=int(3/float(min(n(*g1),n(*g2)))*40)+5
    best=(0,None)
    f1=(float(g1[0]),float(g1[1])); f2=(float(g2[0]),float(g2[1]))
    # range of lattice indices needed: solve i,j from point in triangle
    import numpy as np
    inv=np.linalg.inv(np.array([[f1[0],f2[0]],[f1[1],f2[1]]]))
    corners=np.array([[0,0],[1,0],[0,1]],float)
    ij=corners@inv.T
    lo=np.floor(ij.min(0)).astype(int)-2; hi=np.ceil(ij.max(0)).astype(int)+2
    I,J=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1),indexing="ij")
    I=I.ravel(); J=J.ravel()
    for a in range(steps):
        for b in range(steps):
            oa=a/steps; ob=b/steps
            A=(I+oa)*f1[0]+(J+ob)*f2[0]; B=(I+oa)*f1[1]+(J+ob)*f2[1]
            c=int(((A>=-1e-12)&(B>=-1e-12)&(A+B<=1+1e-12)).sum())
            if c>best[0]: best=(c,(a,b))
    c,(a,b)=best
    oa=Fr(a,steps); ob=Fr(b,steps)
    pts=[]
    for i in range(int(lo[0]),int(hi[0])+1):
        for j in range(int(lo[1]),int(hi[1])+1):
            A=(i+oa)*g1[0]+(j+ob)*g2[0]; B=(i+oa)*g1[1]+(j+ob)*g2[1]
            if A>=0 and B>=0 and A+B<=1: pts.append((A,B))
    ok=all(n(p[0]-q[0],p[1]-q[1])>d for p,q in itertools.combinations(pts,2))
    return len(pts),ok
for name,L,eps in [("(1,1/2)",Fr(1),Fr(1,2)),("(1,1/4)",Fr(1),Fr(1,4)),("(1/5,1/2)",Fr(1,5),Fr(1,2)),("(1/5,1/4)",Fr(1,5),Fr(1,4))]:
    d=2*eps/L
    c,ok=best_packing(d)
    print(f"  {name}: lattice packing with {c} points of T0 at pairwise ||.||_c > {d} (exact check: {ok});  area count 0.5/((d/2)^2 area H) = {0.5/((float(d)/2)**2*area_H):.1f}")
