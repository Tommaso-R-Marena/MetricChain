#!/usr/bin/env python3
"""R2 — the numerical evidence quoted under Conjecture 11.75, from my own tables:
one-sided distance from the profile set of walks with N beads to that of bridges with N+k beads
(units of ||.||_c, not normalised), and the same for the lower boundaries {(h, gmin)} with ||dh||_c + max(0, gmin_bridge - gmin_walk);
max ||N^x||_1/N of walks and bridges."""
import os, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
def load(kind,N):
    f=f"{HERE}/out/{kind}_N{N}.txt"
    if not os.path.exists(f) or os.path.getsize(f)==0: return None
    d={}
    for line in open(f):
        t=line.split(); d[tuple(map(int,t[:3]))]=int(t[4])
    return d
def onesided(A,B,with_g):
    a=np.array([list(h)+[g] for h,g in A.items()]); b=np.array([list(h)+[g] for h,g in B.items()])
    best=0
    for i in range(0,len(a),256):
        d=a[i:i+256,None,:]-b[None,:,:]
        D=5*np.abs(d[:,:,0])+3*np.abs(d[:,:,0]+d[:,:,1])+np.abs(d[:,:,0]+d[:,:,1]+d[:,:,2])
        if with_g: D=D+np.maximum(0,-d[:,:,3])   # epigraph (one-sided) penalty max(0, gmin_bridge - gmin_walk), as in the authors' table
        best=max(best,int(D.min(1).max()))
    return best
print(" N | classes walks/bridges | max||N^x||_1/N walks/bridges | walks(N)->bridges(N+k), k=0..3 (profiles) | same for (h,gmin)")
for N in range(8,24):
    Wt=load("walk",N); Bt=load("bridge",N)
    if Wt is None or Bt is None: continue
    mw=max(9*h[0]+4*h[1]+h[2] for h in Wt)/N; mb=max(9*h[0]+4*h[1]+h[2] for h in Bt)/N
    d1=[];d2=[]
    for k in range(4):
        Bk=load("bridge",N+k)
        if Bk is None: d1.append("-"); d2.append("-"); continue
        d1.append(onesided(Wt,Bk,False)); d2.append(onesided(Wt,Bk,True))
    print(f" {N:2d} | {len(Wt):5d} / {len(Bt):5d} | {mw:.3f} / {mb:.3f} | {d1} | {d2}",flush=True)
