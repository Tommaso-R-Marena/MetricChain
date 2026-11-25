#!/usr/bin/env python3
"""R2 — consistency of the outer bounds of Prop 11.72(b),(c) with large explicit walks (the verified
bridges, my lamellae, the helix): slack of every row of K2 and of the three gauche bounds, per bead.
A negative slack that does not vanish with N would contradict Prop 11.72(c)."""
import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lamella import lamella, measure_np
from r2_lattice import nb
ROWS=[((-1,0,0),0),((4,-1,0),0),((6,-1,0),1),((-2,1,0),3),((-1,1,-1),0),((-1,2,-1),3),((-3,2,-1),2),((-3,4,-3),2),((3,4,-3),5),((6,-2,1),2),((0,-1,2),7),((-3,0,2),9)]
G=[((-5,0,2),8),((0,-1,2),7),((-4,1,1),7)]
items=[(n,N,tuple(q)) for n,N,q in json.load(open(f"{HERE}/out/witness_points_W64.json"))]
items.append(("gauche-rich box 128",166199,(1717,376013,687789,131710)))
for M,Q,l in [(151,1,160),(31,31,32)]:
    x=lamella(M,Q,l); items.append((f"lamella {M}x{Q}x{l}",len(x),measure_np(x)))
x=[(0,0,0)]
for i in range(3000): x.append(nb(x[-1],i%4))
items.append(("4_1 helix",len(x),measure_np(x)))
worst=1e9
for name,N,q in items:
    p=[q[0]/N,q[1]/N,q[2]/N]; g=q[3]/N
    s1=min(b-sum(c[i]*p[i] for i in range(3)) for c,b in ROWS)
    s2=min(g-(sum(c[i]*p[i] for i in range(3))-b) for c,b in G)
    worst=min(worst,s1,s2)
    print(f"{name:34s} N={N:6d}: smallest slack over the 12 rows of K2: {s1:8.4f};  smallest slack of the gauche bounds q - (c.p - b): {s2:8.4f}")
print("smallest slack overall:",round(worst,5),"(>= 0: no row violated by any of these walks)")
