#!/usr/bin/env python3
"""R2 — Lemma 11.67 (site-set reduction, local counting), tested from the definitions.

Independent of r2_enum.c: walks are enumerated here in pure Python; the profile is computed by
the O(N^2) loop over pairs p<q, q-p>=3; the gauche count by the bond-index rule AND by the
1-4 distance.  Then, for every walk:
  (1) h3 = e3(S)-(N-1), h8 = e8(S)-(N-2), h11 = e11(S)            [S = site set]
  (2) e3(S) = 1/2 sum_{m in S} d_S(m);  e8(S) = sum_{all lattice sites m} C(d_S(m),2);
      2 e11(S) = #{unoriented gauche 3-bond lattice paths u-v-w-z with u,z in S}
  (3) class table (count, gmin, count_gmin, gmax) == output of r2_enum.c  (if present)
usage: r2_lemma67.py Nmax [nrandom]
Also (2) on `nrandom` random finite site sets (not necessarily traceable).
"""
import sys, os, random, itertools
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
A = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
def is_A(s): return s[0]%2==0 and s[1]%2==0 and s[2]%2==0 and (s[0]+s[1]+s[2])%4==0
def is_B(s): return is_A((s[0]-1,s[1]-1,s[2]-1))
def nbrs(s):
    sg = 1 if is_A(s) else -1
    assert is_A(s) or is_B(s)
    return [(s[0]+sg*a[0], s[1]+sg*a[1], s[2]+sg*a[2]) for a in A]
def d2(a,b): return (a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2

def walks(N):
    """all walks with N beads, first two bonds fixed (+a0, then -a1); yields (sites, bondidx)"""
    x0=(0,0,0); x1=(1,1,1); x2=(0,2,2)
    path=[x0,x1,x2]; occ={x0,x1,x2}; bonds=[0,1]
    def rec():
        if len(path)==N:
            yield list(path), list(bonds); return
        s=path[-1]; sg = 1 if (len(path)-1)%2==0 else -1
        for b in range(4):
            if b==bonds[-1]: continue
            t=(s[0]+sg*A[b][0], s[1]+sg*A[b][1], s[2]+sg*A[b][2])
            if t in occ: continue
            path.append(t); occ.add(t); bonds.append(b)
            yield from rec()
            path.pop(); occ.discard(t); bonds.pop()
    yield from rec()

def profile_def(x):
    h={3:0,8:0,11:0}
    N=len(x)
    for p in range(N):
        for q in range(p+3,N):
            d=d2(x[p],x[q])
            if d in h: h[d]+=1
    return (h[3],h[8],h[11])

def site_counts(S):
    """e3,e8,e11 of a finite site set by brute force over pairs"""
    S=list(S); e={3:0,8:0,11:0}
    for i in range(len(S)):
        for j in range(i+1,len(S)):
            d=d2(S[i],S[j])
            if d in e: e[d]+=1
    return e[3],e[8],e[11]

def local_counts(S):
    """the local formulas of Lemma 11.67"""
    S=set(S)
    deg=defaultdict(int)             # d_S(m) for every lattice site m with an occupied neighbour
    for s in S:
        for t in nbrs(s): deg[t]+=1
    e3 = sum(deg[m] for m in S)      # = 2 e3
    e8 = sum(d*(d-1)//2 for d in deg.values())
    # gauche 3-bond paths u-v-w-z with u,z in S: enumerate from u, count each unoriented path once
    paths=0
    for u in S:
        for v in nbrs(u):
            for w in nbrs(v):
                if w==u: continue
                for z in nbrs(w):
                    if z==v: continue
                    if z in S and d2(u,z)==11:
                        paths+=1     # oriented; each unoriented path seen twice (from u and from z)
    assert paths%2==0
    return e3, e8, paths//2          # (2e3, e8, 2e11)

if __name__=="__main__":
    Nmax=int(sys.argv[1]); nrand=int(sys.argv[2]) if len(sys.argv)>2 else 0
    for N in range(4,Nmax+1):
        tab=defaultdict(lambda: defaultdict(int)); nw=0
        for x,b in walks(N):
            nw+=1
            h=profile_def(x)
            g_idx=sum(1 for i in range(N-3) if b[i+2]!=b[i])
            d14=[d2(x[i],x[i+3]) for i in range(N-3)]
            assert all(d in (11,19) for d in d14)
            g_dist=sum(1 for d in d14 if d==11)
            assert g_idx==g_dist
            assert all(d2(x[i],x[i+1])==3 for i in range(N-1)) and all(d2(x[i],x[i+2])==8 for i in range(N-2))
            e3,e8,e11=site_counts(x)
            assert h==(e3-(N-1), e8-(N-2), e11), (x,h,e3,e8,e11)
            l3,l8,l11=local_counts(x)
            assert (l3,l8,l11)==(2*e3,e8,2*e11), (x,(l3,l8,l11),(e3,e8,e11))
            tab[h][g_dist]+=1
        msg=""
        f=f"{HERE}/out/walk_N{N}.txt"
        if os.path.exists(f):
            mine={}
            for line in open(f):
                t=line.split(); mine[tuple(map(int,t[:3]))]=tuple(map(int,t[3:7]))
            py={h:(sum(c.values()),min(c),c[min(c)],max(c)) for h,c in tab.items()}
            msg=f" class table == r2_enum.c: {py==mine}"
        print(f"N={N}: {nw} walks, {len(tab)} classes: Lemma 11.67 (1),(2) hold for every walk; gauche rule (index==distance) holds;{msg}", flush=True)
    if nrand:
        rng=random.Random(20261125)
        # random finite site sets inside a small box
        box=[s for s in itertools.product(range(-4,7),repeat=3) if is_A(s) or is_B(s)]
        ok=0
        for t in range(nrand):
            k=rng.randint(1,min(40,len(box)))
            S=rng.sample(box,k)
            e3,e8,e11=site_counts(S); l3,l8,l11=local_counts(S)
            assert (l3,l8,l11)==(2*e3,e8,2*e11), (S,)
            ok+=1
        print(f"random finite site sets (box of {len(box)} sites, 1..40 sites): local formulas hold on {ok}/{nrand}")
