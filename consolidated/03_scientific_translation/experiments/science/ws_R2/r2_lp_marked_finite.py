#!/usr/bin/env python3
"""R2 — finite-N constants for the marked programme (listed as "not done" in §11.22).

For a walk with N >= 2 beads let nu be the count of oriented bonds per configuration (regular
configurations: every occupied centre has two marks; irregular: a centre is a chain END, one mark).
With a certificate (y0, y_k) of r2_lp_marked.py and
     F(config) = c.f(sigma) + c_g fg(config) - y0 [v] - sum_k y_k r_k(star_v(config)),
the orbit average of F is <= 0 on regular configurations, sum over the symmetrised measure of r_k is 0
exactly (the marginal on the star of v is S4-invariant whatever w is), sum nu [v] = 4N, and at most 16
oriented bonds have an end as a centre.  Hence, for EVERY walk,
     c.e + c_g g  <=  y0 N + 4 C,      C = max over irregular configurations of F,
i.e.   c.h + c_g g <= b N + 4C + c3 + 2 c8.
This script computes C for the twelve rows of K2 and the three gauche bounds from my own certificates and
tests the resulting finite inequalities on all class tables (N <= 27), on random walks and on the large
verified bridges.
"""
import sys, os, itertools, json, random
from fractions import Fraction as Fr
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import r2_lp_marked as LP
from r2_lp_marked import f3,f8,f11,fg,fv,star,REL,rel_val,certificate,ROWS,GROWS,PAIRS
from cmp_tables import load_eng

def extended_configs():
    """all configurations in which a centre may be an end (exactly one mark); returns the irregular ones"""
    out=[]
    SING=[frozenset([i]) for i in range(4)]
    for s in itertools.product((0,1),repeat=8):
        v,w=s[0],s[1]; nv=(w,s[2],s[3],s[4]); nw=(v,s[5],s[6],s[7])
        mvs=[m for m in PAIRS+SING if all(nv[i] for i in m)] if v else [None]
        mws=[m for m in PAIRS+SING if all(nw[i] for i in m)] if w else [None]
        for mv in mvs:
            for mw in mws:
                if v and w and ((0 in mv)!=(0 in mw)): continue
                irregular=(mv is not None and len(mv)==1) or (mw is not None and len(mw)==1)
                if irregular: out.append((s,mv,mw))
    return out
IRR=extended_configs()
def F(conf,c,cg,y0,y):
    s,mv,mw=conf
    val=c[0]*f3(conf)+c[1]*f8(conf)+c[2]*f11(conf)-y0*s[0]
    # gauche term only if both centres are regular and vw is a chain bond
    if cg and mv is not None and mw is not None and len(mv)==2 and len(mw)==2: val+=cg*fg(conf)
    st=star(conf)
    if mv is None or len(mv)==2:      # regular (or empty) star of v
        val-=sum(y[k]*((1 if st==REL[k][0] else 0)-(1 if st==REL[k][1] else 0)) for k in range(len(y)) if y[k]!=0)
    return val
def constant(c,cg,b):
    y0=Fr(b+c[0]+c[1]); r=certificate(c,cg,y0)
    assert r is not None
    y,den=r
    C=max(F(conf,c,cg,y0,y) for conf in IRR)
    return max(C,Fr(0))
if __name__=="__main__":
    print(f"{len(IRR)} irregular configurations (a centre is a chain end)")
    res=[]
    for c,b in ROWS:
        C=constant(c,0,b); K=4*C+c[0]+2*c[1]; res.append((c,0,b,K))
        print(f"  row {str(c):>12s} b={b}: C = {C};  finite form: c.h <= {b} N + {K}")
    for name,c,b in GROWS:
        C=constant(c,-1,b); K=4*C+c[0]+2*c[1]; res.append((c,-1,b,K))
        print(f"  {name:>20s}: C = {C};  finite form: g >= c.h - {b} N - {K}   (c = {c})")
    # tests
    worst={i:None for i in range(len(res))}
    for N in range(4,28):
        tab,_=load_eng(N-3)
        for h,v in tab.items():
            for i,(c,cg,b,K) in enumerate(res):
                val=c[0]*h[0]+c[1]*h[1]+c[2]*h[2]+cg*(v[1] if cg else 0)-b*N-K
                assert val<=0, ("VIOLATION",N,h,c)
                worst[i]=val if worst[i] is None else max(worst[i],val)
    print("class tables N = 4..27: all fifteen finite inequalities hold; largest [lhs - rhs] per statement:", [str(worst[i]) for i in range(len(res))])
    from r2_lattice import nbrs, measure
    rng=random.Random(3); nt=0
    for t in range(400):
        N=rng.randint(4,200); x=[(0,0,0)]; occ={(0,0,0)}
        while len(x)<N:
            cc=[q for q in nbrs(x[-1]) if q not in occ]
            if not cc: break
            q=rng.choice(cc); x.append(q); occ.add(q)
        if len(x)<4: continue
        N=len(x); h=measure(x); nt+=1
        for c,cg,b,K in res:
            assert c[0]*h[0]+c[1]*h[1]+c[2]*h[2]+cg*h[3]-b*N-K<=0
    print(f"{nt} random self-avoiding walks (4..200 beads): hold")
    items=[(n,N,tuple(q)) for n,N,q in json.load(open(f"{HERE}/out/witness_points_W64.json"))]+[("big",166199,(1717,376013,687789,131710))]
    for n,N,h in items:
        for c,cg,b,K in res:
            assert c[0]*h[0]+c[1]*h[1]+c[2]*h[2]+cg*h[3]-b*N-K<=0
    print("ten verified bridges (12 041 .. 166 199 beads): hold")
