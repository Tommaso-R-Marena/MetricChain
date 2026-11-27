#!/usr/bin/env python3
"""R2 — finer greedy packings in T0 (on-the-fly distance checks, many sweep orders), exact check."""
import sys, os, random, itertools, math
from fractions import Fraction as Fr
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lattice import norm_c
V1=(Fr(1,2),Fr(2),Fr(3,2)); V2=(Fr(1),Fr(5),Fr(6))
U1=np.array([2.5,7.5,4.0]); U2=np.array([5.0,18.0,12.0])
def run(name,L,eps,Gs,nrand=30):
    dmin=float(2*eps/L); best=(0,None,None)
    for G in Gs:
        ab=np.array([(a,b) for a in range(G+1) for b in range(G+1-a)],dtype=np.int64)
        U=(ab[:,:1]*U1[None,:]+ab[:,1:]*U2[None,:])/G
        n=len(ab); rng=random.Random(G)
        keys=[ab[:,0]+ab[:,1], -(ab[:,0]+ab[:,1]), ab[:,0], ab[:,1], -ab[:,0], -ab[:,1], U.sum(1), -U.sum(1), U[:,0], U[:,1]-U[:,2]]
        orders=[np.lexsort((ab[:,0],k)) for k in keys]+[np.lexsort((ab[:,1],k)) for k in keys]+[np.lexsort((-ab[:,0],k)) for k in keys]
        for t in range(nrand):
            th=rng.random()*2*math.pi; k=np.cos(th)*ab[:,0]+np.sin(th)*ab[:,1]
            orders.append(np.argsort(k,kind="stable"))
        for o in orders:
            chosen=[]; C=np.empty((0,3))
            for i in o:
                if len(chosen)==0 or np.abs(C-U[i]).sum(1).min()>dmin*(1+1e-9):
                    chosen.append(i); C=np.vstack([C,U[i]])
            if len(chosen)>best[0]: best=(len(chosen),G,[tuple(ab[i]) for i in chosen])
    c,G,ch=best
    P=[tuple((int(a)*V1[i]+int(b)*V2[i])/G for i in range(3)) for a,b in ch]
    d=2*eps/L
    exact=all(norm_c(tuple(p[k]-q[k] for k in range(3)))>d for p,q in itertools.combinations(P,2))
    print(f"  {name}: {c} points (grid G={G}); pairwise ||.||_c > {d} verified exactly: {exact}",flush=True)
    return P
if __name__=="__main__":
    run("(1,1/2)",Fr(1),Fr(1,2),[70,72,90,96,105,108,120,140,144])
    run("(1,1/4)",Fr(1),Fr(1,4),[140,144,180,210,216,240],nrand=12)
    run("(1/5,1/2)",Fr(1,5),Fr(1,2),[14,24,28,36,42,70])
    run("(1/5,1/4)",Fr(1,5),Fr(1,4),[28,36,42,56,70,84,120])
