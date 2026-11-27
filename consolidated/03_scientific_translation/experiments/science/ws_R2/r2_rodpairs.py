#!/usr/bin/env python3
"""R2 — pairs per period between two parallel rods R_{0,0}, R_{dm,dq} (Prop 11.72(d) / S Prop 4.3),
and the all-gauche 4_1 helix as a bridge with (h,g) = (0,0,N-3; N-3)."""
import sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lattice import *
from r2_lamella import site
Lp=40
def rod(m,q,k0,k1): return [site(m,q,t) for t in range(2*k0,2*k1)]
core=rod(0,0,10,11)   # one period (2 sites) of rod (0,0)
print("pairs per period between rod (0,0) and rod (dm,dq) at squared distances (3,8,11); all other offsets: none")
tot={}
for dm in range(-4,5):
    for dq in range(-4,5):
        if (dm,dq)==(0,0): continue
        other=set(rod(dm,dq,0,Lp))
        c=[0,0,0]
        for s in core:
            for t in other:
                d=d2(s,t)
                if d==3: c[0]+=1
                elif d==8: c[1]+=1
                elif d==11: c[2]+=1
        if any(c): tot[dm,dq]=tuple(c)
for k,v in sorted(tot.items()): print("  offset",k,":",v)
# within one rod: pairs beyond chain separation 2 inside the cutoff?
r=rod(0,0,0,Lp); print("single rod: (h,g) =", measure(r), "(all-trans, no pairs)")
# all-gauche helix
x=[(0,0,0)]; 
for i in range(60): x.append(nb(x[-1], i%4))
print("4_1 helix, N =",len(x),": bridge:",is_bridge(x),"(h3,h8,h11,g) =",measure(x)," -> density (0,0,1;1)")
