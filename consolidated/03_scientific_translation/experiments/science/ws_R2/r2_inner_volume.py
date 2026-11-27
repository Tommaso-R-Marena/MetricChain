#!/usr/bin/env python3
"""R2 — a RIGOROUS inner bound for the volume of the profile body 𝒦 = proj K^br, from
(i) points proved to lie in K^br exactly: rod (0,0,0), one row of stems (1/2,2,3/2), crystal (1,5,6)
    [Prop 11.72(d)], all-gauche 4_1 helix (0,0,1) [this review];
(ii) explicit finite bridges (authors' generator, verified by my code: out/witness_points_W64.json and
    the 166 199-bead bridge): each has a point of 𝒦 within delta_i = 168/(N_i+3) in ||.||_c.
With C = conv(all measured points) and delta = max delta_i:   𝒦 ⊇ C ⊖ delta*B_c  (erosion; support functions).
The eroded polytope is { x : n.x <= b - delta*h(n) for every facet (n,b) of C },  h(n) = |U^{-T} n|_inf,
U = [[5,0,0],[3,3,0],[1,1,1]]  (||x||_c = |Ux|_1).
"""
import json, os, sys
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
HERE=os.path.dirname(os.path.abspath(__file__))
U=np.array([[5,0,0],[3,3,0],[1,1,1]],float); UinvT=np.linalg.inv(U).T
exact=[(0,0,0),(0.5,2,1.5),(1,5,6),(0,0,1)]
J=json.load(open(f"{HERE}/out/witness_points_W64.json"))
approx=[(n,N,np.array(q[:3])/N,168/(N+3)) for n,N,q in J]
approx.append(("gauche-rich (0,12/5,22/5) box 128",166199,np.array([1717,376013,687789])/166199,168/166202))
def eroded_volume(P,delta):
    hull=ConvexHull(P)
    A=hull.equations[:,:3]; b=-hull.equations[:,3]
    h=np.abs(A@UinvT.T).max(1)          # dual norm of each (unit) facet normal
    b2=b-delta*h
    cen=P.mean(0)
    if not np.all(A@cen<b2-1e-9): return hull.volume,None
    hs=HalfspaceIntersection(np.hstack([A,-b2[:,None]]),cen)
    return hull.volume,ConvexHull(hs.intersections).volume
P_exact=np.array(exact,float)
print(f"exact points only (T0 and the helix point): volume of the hull = {ConvexHull(P_exact).volume:.5f}  (= 1/12)")
allP=np.vstack([P_exact]+[p for _,_,p,_ in approx]); delta=max(d for *_,d in approx)
v,ve=eroded_volume(allP,delta)
print(f"exact points + {len(approx)} verified finite bridges: hull volume {v:.4f}; delta = {delta:.5f}; eroded hull volume (rigorous inner bound for vol 𝒦) = {ve:.4f}")
print(f"   = {100*ve/30:.2f} % of the bulk box; outer bound 3.125 (10.42 %).  [Authors' estimate from periodic systems: 2.22, resting on the routing sketch]")
for name,N,p,d in approx: print(f"   {name:36s} N={N:6d} p=({p[0]:.4f},{p[1]:.4f},{p[2]:.4f}) delta={d:.5f}")
