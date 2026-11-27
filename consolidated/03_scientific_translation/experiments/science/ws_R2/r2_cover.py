#!/usr/bin/env python3
"""R2 — exact covering numbers N^P_cov (profile format, known part #gauche, zero residual, e=1)
by integer programming (scipy.optimize.milp / HiGHS) on class tables.

A centre class a covers a client class c  iff  L*||h_a - h_c|| <= gmin(c) + eps.
usage: r2_cover.py walk|bridge|eng N Lnum Lden EPSnum EPSden [c|w] [timelimit]
   eps = EPSnum/EPSden * N;  norm c = cumulative (Theorem 11.48(b)), w = weighted 9,4,1 (the wrong one, D48)
   'eng' = engineering table (needed for N >= 24)
"""
import sys, os, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cmp_tables import load_eng
def load(kind,N):
    if kind=="eng":
        d,_=load_eng(N-3); return {h:v[1] for h,v in d.items()}
    d={}
    for line in open(f"{HERE}/out/{kind}_N{N}.txt"):
        f=line.split(); d[tuple(map(int,f[:3]))]=int(f[4])
    return d
def cover_number(kind,N,L,eps1,norm="c",tl=600,verbose=False):
    tab=load(kind,N); H=np.array(sorted(tab),dtype=np.int64); gm=np.array([tab[tuple(h)] for h in H],dtype=np.int64)
    n=len(H)
    d=H[:,None,:]-H[None,:,:]
    if norm=="c": D=5*np.abs(d[:,:,0])+3*np.abs(d[:,:,0]+d[:,:,1])+np.abs(d[:,:,0]+d[:,:,1]+d[:,:,2])
    else: D=9*np.abs(d[:,:,0])+4*np.abs(d[:,:,1])+np.abs(d[:,:,2])
    eps=eps1*N
    # exact: L.num*D*den(eps)*... <= (gm+eps)  -> integers
    q=L.denominator*eps.denominator
    lhs=D*L.numerator*eps.denominator                      # = L*D*q
    rhs=(gm*eps.denominator+eps.numerator)*L.denominator   # = (gm+eps)*q
    cov=lhs<=rhs[None,:]          # cov[a,c]: centre a covers client c
    # reductions are left to the solver; build sparse constraint matrix: for each client c, sum_{a covers c} x_a >= 1
    A=csr_matrix(cov.T.astype(np.float64))
    t0=time.time()
    res=milp(c=np.ones(n),constraints=LinearConstraint(A,lb=np.ones(n),ub=np.inf),integrality=np.ones(n),bounds=Bounds(0,1),options={"time_limit":tl,"disp":False})
    x=np.round(res.x).astype(int) if res.x is not None else None
    ub=int(x.sum()) if x is not None else None
    if x is not None: assert np.all(cov[x==1].any(axis=0)), "not a cover"
    lb=int(np.ceil(res.mip_dual_bound-1e-6)) if getattr(res,"mip_dual_bound",None) is not None else None
    return n,lb,ub,res.status,time.time()-t0
if __name__=="__main__":
    kind=sys.argv[1]; N=int(sys.argv[2]); L=Fr(int(sys.argv[3]),int(sys.argv[4])); e1=Fr(int(sys.argv[5]),int(sys.argv[6]))
    norm=sys.argv[7] if len(sys.argv)>7 else "c"; tl=float(sys.argv[8]) if len(sys.argv)>8 else 600
    n,lb,ub,st,t=cover_number(kind,N,L,e1,norm,tl)
    print(f"{kind} N={N} L={L} eps={e1}*N norm={norm}: classes={n}  cover number in [{lb},{ub}]  (status {st}; {t:.1f}s)",flush=True)
