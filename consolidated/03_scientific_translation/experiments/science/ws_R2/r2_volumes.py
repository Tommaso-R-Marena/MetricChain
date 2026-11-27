#!/usr/bin/env python3
"""R2 — the polytopes K1, K2 of Proposition 11.72 and the volume bounds of Theorem 11.71(c).

 (1) vertices of K1 (eleven rows) and K2 (rows with (-4,2,-1;2) -> (-3,2,-1;2), plus (-3,4,-3;2)),
     in exact rational arithmetic (all triples of facets), volumes exactly (signed tetrahedra
     of the hull facets, rational).
 (2) the bounds  vol(u(X) + B1(r/2)) / vol B1(r/2),  r = eps1/L, B1 = l1-ball in u-coordinates
     u(p) = (5p3, 3(p3+p8), p3+p8+p11):   X = bulk box, K1, K2, and K1 with every facet moved out
     by (4M+c3+2c8)/N (N = 100, 1000).  Volume of the Minkowski sum = hull of vertex sums
     (scipy/Qhull), cross-checked by the Steiner polynomial (cubic in the radius, leading
     coefficients vol X and 4/3).
"""
import itertools, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull

ROWS_B=[((-1,0,0),0,Fr(1,2)),((4,-1,0),0,5),((6,-1,0),1,6),((-2,1,0),3,2),((-1,1,-1),0,3),((-1,2,-1),3,4),
        ((-4,2,-1),2,6),((3,4,-3),5,6),((6,-2,1),2,6),((0,-1,2),7,1),((-3,0,2),9,3)]
K1=[(c,Fr(b)) for c,b,M in ROWS_B]
K2=[(c,Fr(b)) for c,b,M in ROWS_B if c!=(-4,2,-1)]+[((-3,2,-1),Fr(2)),((-3,4,-3),Fr(2))]

def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
def solve3(m,b):
    D=det3(m)
    if D==0: return None
    out=[]
    for i in range(3):
        mm=[list(r) for r in m]
        for r in range(3): mm[r][i]=b[r]
        out.append(Fr(det3(mm))/D)
    return tuple(out)
def vertices(H):
    V=set()
    for (c1,b1),(c2,b2),(c3,b3) in itertools.combinations(H,3):
        x=solve3([c1,c2,c3],[b1,b2,b3])
        if x is None: continue
        if all(sum(Fr(c[i])*x[i] for i in range(3))<=b for c,b in H): V.add(x)
    return sorted(V)
def exact_volume(V):
    """exact volume of conv(V): Qhull gives the facet structure, the volume is recomputed in rationals"""
    P=np.array([[float(c) for c in v] for v in V]); hull=ConvexHull(P)
    cen=tuple(sum(v[i] for v in V)/len(V) for i in range(3))
    vol=Fr(0)
    for simp in hull.simplices:
        a,b,c=[V[i] for i in simp]
        m=[[a[i]-cen[i] for i in range(3)],[b[i]-cen[i] for i in range(3)],[c[i]-cen[i] for i in range(3)]]
        vol+=abs(det3(m))/6
    return vol, hull.volume
def u(p): return (5*p[0],3*(p[0]+p[1]),p[0]+p[1]+p[2])
def mink_volume(Vu,rho):
    oct_=[(s*rho if i==j else 0.0) for i in range(3) for s in (1,-1) for j in [0]]  # placeholder (unused)
    B=[]
    for i in range(3):
        for s in (1,-1):
            e=[0.0,0.0,0.0]; e[i]=s*rho; B.append(e)
    pts=np.array([[float(v[i])+b[i] for i in range(3)] for v in Vu for b in B])
    return ConvexHull(pts).volume
def bound(Vu,r):
    rho=r/2
    return mink_volume(Vu,rho)/(4*rho**3/3)

if __name__=="__main__":
    V1=vertices(K1); V2=vertices(K2)
    vol1,f1=exact_volume(V1); vol2,f2=exact_volume(V2)
    fmt=lambda V: " ".join("("+",".join(str(c) for c in v)+")" for v in V)
    print(f"K1: {len(V1)} vertices: {fmt(V1)}\n    volume = {vol1} = {float(vol1):.6f}  ({100*float(vol1)/30:.2f} % of the bulk box 1x5x6); in u-coordinates {float(15*vol1):.3f}")
    print(f"K2: {len(V2)} vertices: {fmt(V2)}\n    volume = {vol2} = {float(vol2):.6f}  ({100*float(vol2)/30:.2f} % of the bulk box); in u-coordinates {float(15*vol2):.3f}")
    print("    K2 subset of K1:", all(all(sum(Fr(c[i])*v[i] for i in range(3))<=b for c,b in K1) for v in V2))
    # redundancy: which rows are facets
    for name,H,V in (("K1",K1,V1),("K2",K2,V2)):
        fac=[(c,b) for c,b in H if sum(1 for v in V if sum(Fr(c[i])*v[i] for i in range(3))==b)>=3]
        print(f"    {name}: rows that are facets (>= 3 vertices on them): {len(fac)} of {len(H)}")
    box=[(a,b,c) for a in (0,1) for b in (0,5) for c in (0,6)]
    sets={"bulk box":[u(p) for p in box],"K1":[u(p) for p in V1],"K2":[u(p) for p in V2]}
    for N in (100,1000):
        H=[(c,Fr(b)+Fr(4*M+c[0]+2*c[1],N)) for c,b,M in ROWS_B]
        sets[f"K1^(N), N={N}"]=[u(p) for p in vertices(H)]
    # Steiner cross-check on K2
    Vu=sets["K2"]; rhos=[0.1,0.2,0.4,0.8]
    vols=[mink_volume(Vu,r) for r in rhos]
    coef=np.polyfit(rhos,vols,3)
    print(f"\nSteiner check (K2 in u-coordinates): vol(X+rho B1) = {coef[3]:.6f} + {coef[2]:.6f} rho + {coef[1]:.6f} rho^2 + {coef[0]:.6f} rho^3   (expect {float(15*vol2):.6f} ... {4/3:.6f})")
    print("\nbounds  vol(u(X)+B1(r/2))/vol B1(r/2)   [theory report table: bulk 26437/191833/392/2195; K1 limit 3719/23936/94/401; K2 3627/23272/93/393; K1 N>=100 4673/30526/111/488; N>=1000 3809/24555/96/409]")
    cases=[("(1,1/2)",0.5),("(1,1/4)",0.25),("(1/5,1/2)",2.5),("(1/5,1/4)",1.25)]
    print("  X".ljust(18)+"".join(f"{n:>16s}" for n,r in cases))
    for name,Vu in sets.items():
        print("  "+name.ljust(16)+"".join(f"{bound(Vu,r):16.2f}" for n,r in cases))
    print("\n(without the factor 2^3 for internal centres: vol(u(K2))*... /(4 r^3/3) at r=1/2: %.1f)"%(float(15*vol2)/(4*0.5**3/3)))
