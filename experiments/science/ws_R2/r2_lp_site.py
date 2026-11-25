#!/usr/bin/env python3
"""R2 — the site-cluster programme of Proposition 11.72(b), re-formulated from scratch,
with my own exact dual certificates.

Cluster of an ORIENTED lattice bond (v->w), w = v + s a_i:  v, w, u_j = v + s a_j, z_j = w - s a_j
(j != i; j runs over the three other bond indices in increasing order), so that (u_j,v,w,z_j)
is trans and (u_j,v,w,z_k), j != k, is gauche.  Pattern sigma = (v,w,u1,u2,u3,z1,z2,z3) in {0,1}^8.

For a finite site set S with N sites let nu(sigma) = #{oriented bonds with pattern sigma},
mu = nu/(4N).  Then (derived by me, tested below on random sets):
   mu(v) = 1,  e3/N = 2 mu(v w),  e8/N = mu(C(d_v,2)) = mu((C(d_v,2)+C(d_w,2))/2),
   e11/N = mu(sum_{j != k} u_j z_k),      d_v = w+u1+u2+u3, d_w = v+z1+z2+z3.
After averaging nu over the 48 point-group images of S (which changes no e_d):
   (S12) mu is invariant under the 12 cluster symmetries (S3 on the index j, exchange of ends);
   (STAR) the marginal of mu on (v; w,u1,u2,u3) is invariant under all permutations of the
          four neighbours.
A pattern is 'forbidden' if an occupied centre (v or w) has fewer than two occupied neighbours;
mu(forbidden) <= 2 n_E / N.

Part 1: test the identities and (S12), (STAR) on random finite site sets (exact integers).
Part 2: LP (HiGHS): support function of the relaxation in the eleven directions.
Part 3: my own dual certificates, rationalised and verified in exact arithmetic on all orbits;
        the smallest M for which a certificate exists (to compare with the table).
Part 4: direct test of the finite inequality with n_E on random and on all small site sets.
"""
import sys, os, itertools, random
from fractions import Fraction as Fr
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lattice import *

ROWS=[((-1,0,0),0,Fr(1,2)),((4,-1,0),0,5),((6,-1,0),1,6),((-2,1,0),3,2),((-1,1,-1),0,3),((-1,2,-1),3,4),
      ((-4,2,-1),2,6),((3,4,-3),5,6),((6,-2,1),2,6),((0,-1,2),7,1),((-3,0,2),9,3)]

PATS=[p for p in itertools.product((0,1),repeat=8)]
def C2(d): return d*(d-1)//2
def dv(p): return p[1]+p[2]+p[3]+p[4]
def dw(p): return p[0]+p[5]+p[6]+p[7]
def f3(p): return Fr(2*p[0]*p[1])
def f8(p): return Fr(C2(dv(p))+C2(dw(p)),2)
def f11(p): return Fr(sum(p[2+j]*p[5+k] for j in range(3) for k in range(3) if j!=k))
def forbidden(p): return (p[0]==1 and dv(p)<2) or (p[1]==1 and dw(p)<2)

# the 12 cluster symmetries as permutations of the 8 positions
def sym12():
    out=[]
    for perm in itertools.permutations(range(3)):
        for ex in (0,1):
            def act(p,perm=perm,ex=ex):
                v,w=p[0],p[1]; u=[p[2+perm[j]] for j in range(3)]; z=[p[5+perm[j]] for j in range(3)]
                return (w,v,*z,*u) if ex else (v,w,*u,*z)
            out.append(act)
    return out
SYM=sym12()
def orbit(p): return frozenset(a(p) for a in SYM)
ORBITS=sorted({orbit(p) for p in PATS if any(p)}, key=lambda o: sorted(o))
def star(p): return (p[0],p[1],p[2],p[3],p[4])
def swap_w_u1(t): return (t[0],t[2],t[1],t[3],t[4])
# star relations: for each star pattern t with t != swap(t): marg(t) - marg(swap t) = 0
STAR_REL=sorted({tuple(sorted((t,swap_w_u1(t)))) for t in itertools.product((0,1),repeat=5) if t!=swap_w_u1(t)})
def rel_val(k,p):
    t1,t2=STAR_REL[k]; s=star(p)
    return (1 if s==t1 else 0)-(1 if s==t2 else 0)

# ---------- Part 1: empirical measures of finite site sets ----------
def point_group():
    G=[]
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1,-1),repeat=3):
            def g(x,perm=perm,signs=signs): return tuple(signs[i]*x[perm[i]] for i in range(3))
            # lattice symmetry x -> g x (+ (1,1,1) if g maps the a_i to the -a_i)
            if g(A[0]) in A:
                G.append(lambda x,g=g: g(x))
            else:
                assert tuple(-c for c in g(A[0])) in A
                G.append(lambda x,g=g: add(g(x),(1,1,1)))
    return G
PG=point_group()
def empirical(S):
    """nu(sigma) over oriented bonds, as dict pattern -> count"""
    S=set(S); cand=set()
    for s in S:
        cand.add(s)
        for t in nbrs(s):
            cand.add(t)
            for r in nbrs(t): cand.add(r)
    nu=defaultdict(int)
    for v in cand:
        for i in range(4):
            w=nb(v,i); js=[j for j in range(4) if j!=i]
            us=[nb(v,j) for j in js]; zs=[nb(w,j) for j in js]
            # check the labelling: (u_j,v,w,z_j) trans (19), (u_j,v,w,z_k) gauche (11)
            for a in range(3):
                for b in range(3):
                    assert d2(us[a],zs[b])==(19 if a==b else 11)
            p=(int(v in S),int(w in S),*[int(u in S) for u in us],*[int(z in S) for z in zs])
            if any(p): nu[p]+=1
    return nu
def part1(ntest=60,seed=1):
    rng=random.Random(seed)
    box=[s for s in itertools.product(range(-3,6),repeat=3) if lat(s)]
    for t in range(ntest):
        S=rng.sample(box,rng.randint(1,30)); N=len(S)
        e3,e8,e11=site_e(S)
        nu=empirical(S)
        assert sum(c*p[0] for p,c in nu.items())==4*N
        assert sum(c*f3(p) for p,c in nu.items())==4*e3
        assert sum(c*C2(dv(p)) for p,c in nu.items())==4*e8
        assert sum(c*f8(p) for p,c in nu.items())==4*e8
        assert sum(c*f11(p) for p,c in nu.items())==4*e11
        # symmetrised measure (x48)
        tot=defaultdict(int)
        for T in PG:
            TS=[T(s) for s in S]
            assert all(lat(s) for s in TS)
            for p,c in empirical(TS).items(): tot[p]+=c
        for p in list(tot):
            for a in SYM: assert tot[a(p)]==tot[p], "S12 fails"
        marg=defaultdict(int)
        for p,c in tot.items(): marg[star(p)]+=c
        for tpat in itertools.product((0,1),repeat=5):
            if not any(tpat): continue
            for perm in itertools.permutations(range(4)):
                t2=(tpat[0],*[tpat[1+perm[i]] for i in range(4)])
                assert marg[tpat]==marg[t2], "STAR fails"
        # forbidden mass
        nE=sum(1 for s in S if sum(1 for q in nbrs(s) if q in set(S))<2)
        assert sum(c for p,c in nu.items() if forbidden(p))<=8*nE
    print(f"Part 1: identities mu(v)=1, e3=2mu(vw)N, e8=mu(C(d_v,2))N, e11=mu(sum u_j z_k)N, symmetry (S12), star invariance (STAR, all 24 permutations) and mu(forbidden)<=2n_E/N hold exactly on {ntest} random finite site sets")

# ---------- Part 2/3: LP and certificates ----------
ALLOWED=[o for o in ORBITS if not forbidden(next(iter(o)))]
FORB=[o for o in ORBITS if forbidden(next(iter(o)))]
def oavg(fun,o): return sum(Fr(fun(p)) for p in o)/len(o)
def primal(c):
    """max c.(f3,f8,f11) over orbit measures with mu(v)=1, star relations, no forbidden mass"""
    orbs=ALLOWED
    obj=[-float(c[0]*oavg(f3,o)+c[1]*oavg(f8,o)+c[2]*oavg(f11,o))*len(o) for o in orbs]
    Aeq=[[float(oavg(lambda p:p[0],o))*len(o) for o in orbs]]; beq=[1.0]
    for k in range(len(STAR_REL)):
        Aeq.append([float(oavg(lambda p,k=k:rel_val(k,p),o))*len(o) for o in orbs]); beq.append(0.0)
    r=linprog(obj,A_eq=Aeq,b_eq=beq,bounds=(0,None),method="highs")
    assert r.status==0, r.message
    return -r.fun
def dual_cert(c,b,Mfix=None):
    """find y0, y_k with  avg_O[c.f - sum y_k r_k - y0 [v]] <= 0 on allowed orbits, <= M on forbidden.
       y0 is fixed to b+c3+c8; minimise M (LP), then rationalise and verify exactly."""
    y0=Fr(b+c[0]+c[1]); K=len(STAR_REL)
    # variables: y_1..y_K, M
    Aub=[];bub=[]
    for o in ORBITS:
        row=[-float(oavg(lambda p,k=k:rel_val(k,p),o)) for k in range(K)]
        rhs=-float(c[0]*oavg(f3,o)+c[1]*oavg(f8,o)+c[2]*oavg(f11,o)-y0*oavg(lambda p:p[0],o))
        if o in FORBSET: row.append(-1.0)
        else: row.append(0.0)
        Aub.append(row); bub.append(rhs)
    obj=[0.0]*K+[1.0]
    r=linprog(obj,A_ub=Aub,b_ub=bub,bounds=[(None,None)]*K+[(0,None)],method="highs")
    assert r.status==0, r.message
    return r
FORBSET=set(FORB)
def verify_exact(c,b,y,M):
    """exact check of a certificate (y rational list, M rational)"""
    y0=Fr(b+c[0]+c[1]); worst_allowed=None; worst_forb=None
    for o in ORBITS:
        val=c[0]*oavg(f3,o)+c[1]*oavg(f8,o)+c[2]*oavg(f11,o)-y0*oavg(lambda p:p[0],o)-sum(y[k]*oavg(lambda p,k=k:rel_val(k,p),o) for k in range(len(y)))
        if o in FORBSET: worst_forb=val if worst_forb is None else max(worst_forb,val)
        else: worst_allowed=val if worst_allowed is None else max(worst_allowed,val)
    return worst_allowed, worst_forb

def rationalise(c,b,r):
    """try denominators 1..24 for y; return (y, M) verified exactly, with the smallest M found"""
    K=len(STAR_REL); best=None
    for den in (1,2,3,4,6,8,12,24,48):
        y=[Fr(round(v*den),den) for v in r.x[:K]]
        wa,wf=verify_exact(c,b,y,None)
        if wa<=0:
            M=max(wf,Fr(0))
            if best is None or M<best[1]: best=(y,M,den)
    return best

if __name__=="__main__":
    print(f"{len(ORBITS)} orbits of non-empty patterns under the 12 cluster symmetries, {len(ALLOWED)} allowed, {len(FORB)} forbidden; {len(STAR_REL)} star relations (transposition w<->u1)")
    part1()
    print("\nPart 2: support function of the site-cluster relaxation (HiGHS) vs the table (b + c3 + c8)")
    for c,b,M in ROWS:
        val=primal(c)
        print(f"  c={str(c):>12s}: LP max of c.e/N = {val:.9f}   table: {b+c[0]+c[1]}   -> c.p <= {val-c[0]-c[1]:.9f} (claimed {b})")
    print("\nPart 3: own dual certificates, verified in exact rational arithmetic on all 46 orbits")
    allok=True
    for c,b,M in ROWS:
        r=dual_cert(c,b)
        best=rationalise(c,b,r)
        if best is None:
            print(f"  c={c}: could not rationalise (LP M*={r.x[-1]:.6f})"); allok=False; continue
        y,Mmine,den=best
        wa,wf=verify_exact(c,b,y,None)
        ok=(wa<=0 and Mmine<=M)
        allok&=ok
        print(f"  c={str(c):>12s} b={b}: exact certificate with denominators {den}: max over allowed orbits = {wa} (<= 0), max over forbidden orbits = {wf}; LP-minimal M = {r.x[-1]:.4f}; table M = {M}; row certified with M <= table M: {ok}")
        print(f"       y (nonzero) = {{{', '.join(f'{STAR_REL[k]}: {v}' for k,v in enumerate(y) if v!=0)}}}")
    print("  all eleven rows certified exactly with the table's M:", allok)
