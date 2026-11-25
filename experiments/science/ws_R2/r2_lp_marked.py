#!/usr/bin/env python3
"""R2 — the marked (path-cluster) programme of Proposition 11.72(c), re-formulated from scratch,
with my own exact dual certificates.

Configuration of an oriented lattice bond (v->w): the occupation pattern
sigma = (v,w,u1,u2,u3,z1,z2,z3) and, for each occupied centre, the set of its two chain
neighbours ("marks"): m_v a 2-subset of positions {0=w,1,2,3=u_j}, m_w a 2-subset of {0=v,1,2,3=z_j};
marked neighbours are occupied; 0 in m_v <=> 0 in m_w when both centres are occupied.
(340 configurations including the empty one; a walk produces only these, except for the O(1)
oriented bonds that have a chain END as a centre.)
  mu = nu/(4N);  p as in the site programme;  g/N = 2 mu(vw marked, m_v={w,u_j}, m_w={v,z_k}, j != k).
Constraints: mu(v)=1; invariance under the 12 cluster symmetries; the marginal on the marked
star of v, (v; w,u1,u2,u3; m_v), is invariant under all permutations of the four neighbours.

Part 1: the identities and the constraints are tested on the symmetrised measures of random
        walks (ends handled explicitly: stars with one mark are separate patterns).
Part 2: LP values (HiGHS) for the twelve rows of K2 and the three gauche bounds.
Part 3: own exact dual certificates on all orbits.
"""
import sys, os, itertools, random
from fractions import Fraction as Fr
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lattice import *

PAIRS=[frozenset(c) for c in itertools.combinations(range(4),2)]
def configs():
    out=[]
    for s in itertools.product((0,1),repeat=8):
        v,w=s[0],s[1]; nv=(w,s[2],s[3],s[4]); nw=(v,s[5],s[6],s[7])
        mvs=[m for m in PAIRS if all(nv[i] for i in m)] if v else [None]
        mws=[m for m in PAIRS if all(nw[i] for i in m)] if w else [None]
        for mv in mvs:
            for mw in mws:
                if v and w and ((0 in mv)!=(0 in mw)): continue
                out.append((s,mv,mw))
    return out
CONF=configs()
def C2(d): return d*(d-1)//2
def f3(c): s=c[0]; return Fr(2*s[0]*s[1])
def f8(c): s=c[0]; return Fr(C2(s[1]+s[2]+s[3]+s[4])+C2(s[0]+s[5]+s[6]+s[7]),2)
def f11(c): s=c[0]; return Fr(sum(s[2+j]*s[5+k] for j in range(3) for k in range(3) if j!=k))
def fv(c): return Fr(c[0][0])
def fg(c):
    s,mv,mw=c
    if not (s[0] and s[1]) or mv is None or mw is None or 0 not in mv or 0 not in mw: return Fr(0)
    j=[i for i in mv if i!=0][0]; k=[i for i in mw if i!=0][0]
    return Fr(2) if j!=k else Fr(0)
def act(perm,ex):
    def a(c):
        s,mv,mw=c
        # new index j carries old index perm[j]
        inv={0:0}; 
        for j in range(3): inv[perm[j]+1]=j+1
        u=[s[2+perm[j]] for j in range(3)]; z=[s[5+perm[j]] for j in range(3)]
        mv2=None if mv is None else frozenset(inv[i] for i in mv)
        mw2=None if mw is None else frozenset(inv[i] for i in mw)
        if ex: return ((s[1],s[0],*z,*u),mw2,mv2)
        return ((s[0],s[1],*u,*z),mv2,mw2)
    return a
SYM=[act(p,e) for p in itertools.permutations(range(3)) for e in (0,1)]
def orbit(c): return frozenset(a(c) for a in SYM)
def star(c): s,mv,mw=c; return (s[0],(s[1],s[2],s[3],s[4]),mv)
def perm_star(t,perm):
    v,nbh,mv=t
    # position i of the new star carries old position perm[i]
    inv={perm[i]:i for i in range(4)}
    return (v,tuple(nbh[perm[i]] for i in range(4)),None if mv is None else frozenset(inv[i] for i in mv))
SW=(1,0,2,3)

def build():
    CS=set(CONF)
    assert all(a(c) in CS for c in CONF for a in SYM), "configurations not closed under the symmetries"
    orbs=sorted({orbit(c) for c in CONF if any(c[0])}, key=lambda o: sorted((x[0],sorted(x[1] or []),sorted(x[2] or [])) for x in o))
    stars=sorted({star(c) for c in CONF}, key=lambda t:(t[0],t[1],sorted(t[2] or [])))
    rel=[]; seen=set()
    for t in stars:
        t2=perm_star(t,SW)
        if t2==t or (t2,t) in seen or not any((t[0],)+t[1]): continue
        seen.add((t,t2)); rel.append((t,t2))
    return orbs,rel
ORBS,REL=build()
def rel_val(k,c):
    t1,t2=REL[k]; s=star(c)
    return (1 if s==t1 else 0)-(1 if s==t2 else 0)
def oavg(fun,o): return sum(Fr(fun(c)) for c in o)/len(o)
# precompute orbit averages
OA={name:[oavg(f,o) for o in ORBS] for name,f in (("f3",f3),("f8",f8),("f11",f11),("fg",fg),("fv",fv))}
OR=[[oavg(lambda c,k=k:rel_val(k,c),o) for o in ORBS] for k in range(len(REL))]

def primal(c,cg):
    obj=[-float(c[0]*OA["f3"][i]+c[1]*OA["f8"][i]+c[2]*OA["f11"][i]+cg*OA["fg"][i])*len(o) for i,o in enumerate(ORBS)]
    Aeq=[[float(OA["fv"][i])*len(o) for i,o in enumerate(ORBS)]]+[[float(OR[k][i])*len(o) for i,o in enumerate(ORBS)] for k in range(len(REL))]
    beq=[1.0]+[0.0]*len(REL)
    r=linprog(obj,A_eq=Aeq,b_eq=beq,bounds=(0,None),method="highs")
    assert r.status==0, r.message
    return -r.fun
def exact_max(c,cg,y0,y):
    return max(c[0]*OA["f3"][i]+c[1]*OA["f8"][i]+c[2]*OA["f11"][i]+cg*OA["fg"][i]-y0*OA["fv"][i]-sum(y[k]*OR[k][i] for k in range(len(y)) if y[k]!=0) for i in range(len(ORBS)))
def certificate(c,cg,y0):
    """multipliers y with  avg_O[c.f + cg fg - y0 [v] - sum y_k r_k] <= 0 on every orbit"""
    K=len(REL)
    Aub=[[-float(OR[k][i]) for k in range(K)] for i in range(len(ORBS))]
    bub=[-float(c[0]*OA["f3"][i]+c[1]*OA["f8"][i]+c[2]*OA["f11"][i]+cg*OA["fg"][i]-y0*OA["fv"][i]) for i in range(len(ORBS))]
    # feasibility with a little regularisation: minimise sum |y| (split variables)
    obj=[1.0]*(2*K)
    A2=[row+[-x for x in row] for row in Aub]
    r=linprog(obj,A_ub=A2,b_ub=bub,bounds=(0,None),method="highs")
    if r.status!=0: return None
    yf=[r.x[k]-r.x[K+k] for k in range(K)]
    for den in (1,2,3,4,6,8,12,24,48,96):
        y=[Fr(round(v*den),den) for v in yf]
        if exact_max(c,cg,Fr(y0),y)<=0: return y,den
    return None

# ---------- Part 1 ----------
def point_group():
    G=[]
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1,-1),repeat=3):
            def g(x,perm=perm,signs=signs): return tuple(signs[i]*x[perm[i]] for i in range(3))
            if g(A[0]) in A: G.append(lambda x,g=g: g(x))
            else: G.append(lambda x,g=g: add(g(x),(1,1,1)))
    return G
PG=point_group()
def empirical_marked(x):
    """extended configurations (ends have one mark) -> count, over oriented bonds"""
    idx={s:i for i,s in enumerate(x)}; S=set(x); N=len(x)
    def chain_nb(a,b): return a in idx and b in idx and abs(idx[a]-idx[b])==1
    cand=set()
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
            s=(int(v in S),int(w in S),*[int(u in S) for u in us],*[int(z in S) for z in zs])
            if not any(s): continue
            mv=frozenset(k for k,t in enumerate([w]+us) if chain_nb(v,t)) if v in S else None
            mw=frozenset(k for k,t in enumerate([v]+zs) if chain_nb(w,t)) if w in S else None
            nu[(s,mv,mw)]+=1
    return nu
def random_walk(N,rng):
    while True:
        x=[(0,0,0)]; occ={(0,0,0)}
        while len(x)<N:
            c=[t for t in nbrs(x[-1]) if t not in occ]
            if not c: break
            t=rng.choice(c); x.append(t); occ.add(t)
        if len(x)==N: return x
def part1(ntest=25,seed=7):
    rng=random.Random(seed); CS=set(CONF)
    for t in range(ntest):
        N=rng.randint(8,60); x=random_walk(N,rng)
        h3,h8,h11,g=measure(x); e3,e8,e11=site_e(x)
        nu=empirical_marked(x)
        irregular=sum(cnt for c,cnt in nu.items() if c not in CS)
        assert irregular<=16
        assert sum(cnt*c[0][0] for c,cnt in nu.items())==4*N
        assert sum(cnt*f3(c) for c,cnt in nu.items())==4*e3 and sum(cnt*f8(c) for c,cnt in nu.items())==4*e8 and sum(cnt*f11(c) for c,cnt in nu.items())==4*e11
        assert sum(cnt*fg(c) for c,cnt in nu.items() if c in CS)==4*g, "gauche identity"
        tot=defaultdict(int)
        for T in PG:
            for c,cnt in empirical_marked([T(s) for s in x]).items(): tot[c]+=cnt
        for c in list(tot):
            for a in SYM: assert tot[a(c)]==tot[c], "S12 fails"
        marg=defaultdict(int)
        for c,cnt in tot.items(): marg[star(c)]+=cnt
        for tpat in list(marg):
            for perm in itertools.permutations(range(4)):
                assert marg[perm_star(tpat,perm)]==marg[tpat], "STAR fails"
    print(f"Part 1: on {ntest} random self-avoiding walks (8..60 beads): at most 16 oriented bonds have a chain end as a centre; mu(v)=1 and the formulas for e3,e8,e11 and g/N = 2mu(...) hold exactly; the symmetrised measure is invariant under the 12 cluster symmetries and its marked-star marginal under all 24 permutations")

ROWS=[((-1,0,0),0),((4,-1,0),0),((6,-1,0),1),((-2,1,0),3),((-1,1,-1),0),((-1,2,-1),3),((-3,2,-1),2),((-3,4,-3),2),
      ((3,4,-3),5),((6,-2,1),2),((0,-1,2),7),((-3,0,2),9)]
GROWS=[("q >= 2p11-5p3-8",(-5,0,2),8),("q >= 2p11-p8-7",(0,-1,2),7),("q >= p11+p8-4p3-7",(-4,1,1),7)]
if __name__=="__main__":
    print(f"{len(CONF)} configurations (incl. the empty one), {len(ORBS)} orbits of non-empty configurations, {len(REL)} star relations (transposition w<->u1)")
    part1()
    print("\nPart 2: LP values (HiGHS): max of c.p over the marked relaxation (claimed b), and the old row (-4,2,-1)")
    for c,b in ROWS+[((-4,2,-1),2)]:
        val=primal(c,0)-c[0]-c[1]
        print(f"  c={str(c):>12s}: max c.p = {val:.9f}   claimed {b}")
    for name,c,b in GROWS:
        val=primal(c,-1)-c[0]-c[1]
        print(f"  {name:>20s}: max of (c.p - q) = {val:.9f}   claimed {b}")
    print("\nPart 3: own exact certificates (all orbits, rational arithmetic)")
    ok=True
    for c,b in ROWS:
        r=certificate(c,0,b+c[0]+c[1])
        if r is None: print(f"  c={c}: NO exact certificate found"); ok=False; continue
        y,den=r
        print(f"  c={str(c):>12s} b={b}: certified exactly (denominator {den}; {sum(1 for v in y if v!=0)} nonzero multipliers; max over orbits = {exact_max(c,0,Fr(b+c[0]+c[1]),y)})")
    for name,c,b in GROWS:
        r=certificate(c,-1,b+c[0]+c[1])
        if r is None: print(f"  {name}: NO exact certificate found"); ok=False; continue
        y,den=r
        print(f"  {name:>20s}: certified exactly (denominator {den}; {sum(1 for v in y if v!=0)} nonzero multipliers; max over orbits = {exact_max(c,-1,Fr(b+c[0]+c[1]),y)})")
    print("  all certified:",ok)
