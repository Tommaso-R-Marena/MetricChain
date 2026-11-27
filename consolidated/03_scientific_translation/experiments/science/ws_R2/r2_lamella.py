#!/usr/bin/env python3
"""R2 — rung-folded lamellae (Proposition 11.72(d)), own construction, everything verified from
coordinates.

Rod R_{m,q}: sites site(m,q,t) = m(2,2,0)+q(2,0,2)+k(0,2,2) (+(1,1,1) if t odd), k = floor(t/2);
height y = 2m+t.  Rungs: site(m,q,2k+1) ~ site(m+1,q,2k) and site(m,q,2k+1) ~ site(m,q+1,2k).
Snake order over an M x Q block (M,Q odd), stems alternately up and down over l periods;
first bead at t=-2 on rod (0,0), last bead at t=2l+1 on rod (M-1,Q-1); optional all-trans tail
(continuation of the last stem upwards) to reach exactly N beads.
"""
import sys, os
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lattice import *

def site(m,q,t):
    k=t//2
    s=(2*m+2*q, 2*m+2*k, 2*q+2*k)
    return s if t%2==0 else (s[0]+1,s[1]+1,s[2]+1)

def lamella(M,Q,l,N=None):
    assert M%2==1 and Q%2==1 and l>=2
    rods=[]
    for q in range(Q):
        ms=range(M) if q%2==0 else range(M-1,-1,-1)
        rods+=[(m,q) for m in ms]
    x=[]; t=-2; up=True
    for s,(m,q) in enumerate(rods):
        last=(s==len(rods)-1)
        if last:
            assert up
            tend=2*l+1
        else:
            m2,q2=rods[s+1]
            forward=(m2==m+1 and q2==q) or (m2==m and q2==q+1)
            backward=(m2==m-1 and q2==q)
            assert forward or backward
            if up: tend=2*l-1 if forward else 2*l-2
            else:  tend=1 if forward else 0
        rng=range(t,tend+1) if up else range(t,tend-1,-1)
        x+= [site(m,q,tt) for tt in rng]
        if not last:
            t = tend-1 if forward else tend+1
            up = not up
    if N is not None:
        if len(x)>N: return None
        m,q=rods[-1]; tt=2*l+2
        while len(x)<N:
            x.append(site(m,q,tt)); tt+=1
    return x

def lamella_np(M,Q,l,N=None):
    """the same walk as lamella(), as an (n,3) int64 array, built stem by stem with numpy (fast)"""
    assert M%2==1 and Q%2==1 and l>=2
    rods=[]
    for q in range(Q):
        ms=range(M) if q%2==0 else range(M-1,-1,-1)
        rods+=[(m,q) for m in ms]
    parts=[]; t=-2; up=True; n=0
    for s_,(m,q) in enumerate(rods):
        last=(s_==len(rods)-1)
        if last: tend=2*l+1
        else:
            m2,q2=rods[s_+1]
            forward=(m2==m+1 and q2==q) or (m2==m and q2==q+1)
            if up: tend=2*l-1 if forward else 2*l-2
            else:  tend=1 if forward else 0
        if last and N is not None:
            tend=tend+(N-(n+(tend-t+1)))
            if tend<2*l+1: return None
        tt=np.arange(t,tend+1,dtype=np.int64) if up else np.arange(t,tend-1,-1,dtype=np.int64)
        k=tt//2; odd=tt%2
        parts.append(np.stack([2*m+2*q+odd, 2*m+2*k+odd, 2*q+2*k+odd],axis=1)); n+=len(tt)
        if not last:
            t = tend-1 if forward else tend+1
            up = not up
    return np.concatenate(parts)

OFF=1<<10; KK=1<<11
def key(a): return ((a[:,0]+OFF)*KK+(a[:,1]+OFF))*KK+(a[:,2]+OFF)
_VEC={3:np.array(V3),8:np.array(V8),11:np.array(V11)}
def measure_np(x):
    """(h3,h8,h11,g) via site-set counts (Lemma 11.67, verified in r2_lemma67.py) and the 1-4 distance;
    checks: lattice walk (consecutive distance^2 = 3), injective."""
    a=np.asarray(x,dtype=np.int64); N=len(a)
    d=np.diff(a,axis=0); assert np.all((d*d).sum(1)==3), "not bonded"
    k=key(a); assert len(np.unique(k))==N, "not injective"
    ks=np.sort(k); e={}
    for dd,vecs in _VEC.items():
        c=0
        for v in vecs:
            kv=key(a+v)
            pos=np.searchsorted(ks,kv); pos[pos>=N]=N-1
            c+=int((ks[pos]==kv).sum())
        e[dd]=c//2
    d14=((a[3:]-a[:-3])**2).sum(1); assert np.all((d14==11)|(d14==19))
    return (e[3]-(N-1), e[8]-(N-2), e[11], int((d14==11).sum()))

if __name__=="__main__":
    # self-test of measure_np and measure_fast against the O(N^2) definition
    for (M,Q,l) in [(1,1,2),(3,1,2),(3,3,2),(5,3,3),(3,5,4)]:
        x=lamella(M,Q,l)
        assert all(lat(s) for s in x) and is_bridge(x)
        assert measure(x)==measure_fast(x)==measure_np(x), (M,Q,l)
    print("self-test: lamellae are self-avoiding lattice bridges; O(N^2) definition == look-up == numpy site-set count")
    print("\none row of stems (Q=1): density -> (1/2, 2, 3/2; 0)")
    for M,l in [(3,4),(9,10),(21,24),(45,50),(91,91),(151,160)]:
        x=lamella(M,1,l); N=len(x); h=measure_np(x); assert is_bridge(x)
        pred=tuple(l*(M-1)*c for c in (1,4,3))
        print(f"  M={M:3d} l={l:3d} N={N:6d}: (h,g)/N = ({h[0]/N:.4f},{h[1]/N:.4f},{h[2]/N:.4f};{h[3]/N:.4f})   g={h[3]} <= 3(MQ-1)={3*(M-1)}: {h[3]<=3*(M-1)}   h - l(M-1)(1,4,3) = {tuple(h[i]-pred[i] for i in range(3))}")
    print("\ncrystal (M=Q~l): density -> (1, 5, 6; 0);  k = (1 - ||N^x||_1/(35N)) N^(1/3)")
    for M,Q,l in [(3,3,3),(5,5,5),(7,7,8),(11,11,12),(15,15,16),(21,21,22),(25,25,26),(31,31,32)]:
        x=lamella(M,Q,l); N=len(x); h=measure_np(x); assert is_bridge(x)
        pred=tuple(l*((2*M*Q-M-Q)*a+(M-1)*(Q-1)*b) for a,b in zip((1,4,3),(0,2,6)))
        nrm=9*h[0]+4*h[1]+h[2]
        print(f"  {M}x{Q}x{l} N={N:6d}: (h,g)/N = ({h[0]/N:.4f},{h[1]/N:.4f},{h[2]/N:.4f};{h[3]/N:.4f})  g={h[3]} <= {3*(M*Q-1)}: {h[3]<=3*(M*Q-1)}  |h - formula|/(MQ) = {tuple(round(abs(h[i]-pred[i])/(M*Q),2) for i in range(3))}  (1-h3/N)N^(1/3)={(1-h[0]/N)*N**(1/3):.3f}  k={(1-nrm/(35*N))*N**(1/3):.3f}  dist to (1,5,6;0) = {35-nrm/N+h[3]/N:.4f} = {(35-nrm/N+h[3]/N)*N**(1/3):.2f} N^(-1/3)")
