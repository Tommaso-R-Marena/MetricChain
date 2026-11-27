#!/usr/bin/env python3
"""R2 — lower bounds of Theorem 11.71(c).

Part A (limit): packings in the triangle T0 = conv{(0,0,0),(1/2,2,3/2),(1,5,6)} (where gamma = 0
        given Prop 11.72(d) and convexity of K^br): points with pairwise ||.||_c > 2 eps1/L.
        Grid points with rational barycentric coordinates; several greedy sweeps; the final packing
        is re-verified pairwise in exact rational arithmetic.
Part B (finite N): explicit bridges = my lamellae (r2_lamella.py) prolonged by an all-trans tail
        to exactly N beads; exact (h,g) from coordinates; a subset with
        L||h_i-h_j||_c > g_i+g_j+2 eps1 N pairwise (exact integer arithmetic for L=1; rational for 1/5).
usage: r2_packing.py A | B N1 N2 ...
"""
import sys, os, random, itertools
from fractions import Fraction as Fr
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lattice import norm_c
CASES=[("(1,1/2)",Fr(1),Fr(1,2)),("(1,1/4)",Fr(1),Fr(1,4)),("(1/5,1/2)",Fr(1,5),Fr(1,2)),("(1/5,1/4)",Fr(1,5),Fr(1,4))]
V1=(Fr(1,2),Fr(2),Fr(3,2)); V2=(Fr(1),Fr(5),Fr(6))

def greedy(points,dist_ok,orders):
    best=[]
    for order in orders:
        chosen=[]
        for i in order:
            if all(dist_ok(i,j) for j in chosen): chosen.append(i)
        if len(chosen)>len(best): best=chosen
    return best

def partA():
    print("Part A: packings in T0 (pairwise ||p_i-p_j||_c > 2 eps1/L), exact verification")
    for name,L,eps in CASES:
        dmin=2*eps/L
        best=None
        for G in (24,30,36,40,48,60,72,84,96,120):
            pts=[(a,b) for a in range(G+1) for b in range(G+1-a)]
            # float coordinates in u for speed
            U=np.array([[float(5*(a*V1[0]+b*V2[0])/G), float(3*((a*V1[0]+b*V2[0])+(a*V1[1]+b*V2[1]))/G),
                         float(((a*V1[0]+b*V2[0])+(a*V1[1]+b*V2[1])+(a*V1[2]+b*V2[2]))/G)] for a,b in pts])
            n=len(pts)
            if n>8000: continue
            D=np.abs(U[:,None,:]-U[None,:,:]).sum(2)
            ok=D>float(dmin)*(1+1e-9)
            rng=random.Random(1)
            orders=[list(range(n)), list(range(n-1,-1,-1)),
                    sorted(range(n),key=lambda i:(pts[i][0]+pts[i][1],pts[i][0])),
                    sorted(range(n),key=lambda i:(-(pts[i][0]+pts[i][1]),pts[i][0])),
                    sorted(range(n),key=lambda i:(pts[i][1],pts[i][0])),
                    sorted(range(n),key=lambda i:(U[i].sum(),U[i][0])),
                    sorted(range(n),key=lambda i:(-U[i].sum(),U[i][0]))]
            for t in range(6):
                o=list(range(n)); rng.shuffle(o); orders.append(o)
            ch=greedy(pts,lambda i,j:ok[i,j],orders)
            if best is None or len(ch)>len(best[1]): best=(G,[pts[i] for i in ch])
        G,ch=best
        P=[tuple((a*V1[i]+b*V2[i])/G for i in range(3)) for a,b in ch]
        exact=all(norm_c(tuple(P[i][k]-P[j][k] for k in range(3)))>dmin for i in range(len(P)) for j in range(i))
        print(f"  {name}: {len(P)} points (grid G={G}); pairwise > {dmin} verified exactly: {exact}")
    return

def partB(Ns):
    from r2_lamella import lamella_np, measure_np
    print("Part B: packings among explicit bridges with exactly N beads (lamellae + all-trans tail)")
    for N in Ns:
        cand={}
        for M in range(1,400,2):
            for Q in range(1,400,2):
                if 2*M*Q*2>N+8: break
                for l in range(2,N):
                    x=lamella_np(M,Q,l,N)
                    if x is None: break
                    hg=measure_np(x)          # asserts: bonded, injective, 1-4 distances in {11,19}
                    # bridge and lattice checks from coordinates (vectorised)
                    assert len(x)==N and x[1:,1].min()>x[0,1] and x[:,1].max()==x[-1,1]
                    par=x%2; assert np.all((par[:,0]==par[:,1])&(par[:,1]==par[:,2])) and np.all(((x-par).sum(1))%4==0)
                    cand[hg]=(M,Q,l)
        pts=sorted(cand)
        H=np.array(pts,dtype=np.int64); n=len(pts)
        # cumulative coordinates: ||dh||_c = 5|d1| + 3|d2| + |d3| with (d1,d2,d3) differences of (h3, h3+h8, h3+h8+h11)
        Cc=np.stack([H[:,0],H[:,0]+H[:,1],H[:,0]+H[:,1]+H[:,2]],axis=1); Wt=np.array([5,3,1],dtype=np.int64)
        res=[]
        for name,L,eps in CASES:
            # exact integers:  L*D > g_i+g_j+2 eps N   <=>   4*L.num*D > (4(g_i+g_j) + 8 eps N)*L.den
            add=int(8*eps*N)
            rng=random.Random(N)
            nrm=9*H[:,0]+4*H[:,1]+H[:,2]
            orders=[np.lexsort((H[:,0],H[:,3])), np.lexsort((H[:,3],nrm)), np.lexsort((H[:,3],-nrm)), np.lexsort((H[:,3],H[:,0]))]
            for t in range(40):
                orders.append(np.argsort(H[:,3]+np.array([rng.random() for _ in range(n)])*N*0.02*t,kind="stable"))
            best=[]
            for o in orders:
                ch=[]; CC=np.empty((0,3),dtype=np.int64); GG=np.empty(0,dtype=np.int64)
                for i in o:
                    if len(ch)==0 or np.all(4*L.numerator*(np.abs(CC-Cc[i])@Wt) > (4*(GG+H[i,3])+add)*L.denominator):
                        ch.append(i); CC=np.vstack([CC,Cc[i]]); GG=np.append(GG,H[i,3])
                if len(ch)>len(best): best=ch
            # exact re-verification of the best packing
            for a in range(len(best)):
                for b in range(a):
                    i,j=best[a],best[b]
                    D=int(5*abs(H[i,0]-H[j,0])+3*abs(H[i,0]+H[i,1]-H[j,0]-H[j,1])+abs(int(H[i,:3].sum())-int(H[j,:3].sum())))
                    assert L*D > int(H[i,3])+int(H[j,3])+2*eps*N
            res.append(len(best))
        print(f"  N={N}: {len(pts)} distinct (h,g) among lamellae+tail; pairwise-uncoverable subsets found: " + ", ".join(f"{c[0]}: {r}" for c,r in zip(CASES,res)),flush=True)

if __name__=="__main__":
    if sys.argv[1]=="A": partA()
    else: partB([int(a) for a in sys.argv[2:]])
