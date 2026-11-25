#!/usr/bin/env python3
"""R2 — Proposition 11.74 (single-flip constants), own code.

 (1) lower bound: the hairpin  t^a (fold) t^b  and the same word with the middle fold torsion set
     to trans.  The fold word is read off my own lamella (two adjacent stems joined by a rung).
     D(a,b) = ||h(hairpin) - h(opened)||_c; torsion index j = a+2 (1-based), d_j = min(a+2, b+2);
     claim: c_j^sf >= D >= 14 d_j - 15.
 (2) the engineering division's exact constants (n <= 16) against 14 d - 15 <= c <= 70 (d+3) for d >= 5.
"""
import sys, os, glob
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lattice import *
from r2_lamella import lamella, measure_np
def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def word(x):
    """torsion states: 0 trans, +1/-1 gauche with the sign of det(b_k,b_{k+1},b_{k+2})"""
    b=[sub(x[i+1],x[i]) for i in range(len(x)-1)]
    out=[]
    for k in range(len(b)-2):
        dd=d2(x[k],x[k+3])
        if dd==19: out.append(0)
        else:
            assert dd==11
            s=det3(b[k],b[k+1],b[k+2]); assert s!=0
            out.append(1 if s>0 else -1)
    return out
def build(w):
    """lattice walk with torsion word w (first two bonds +a0, -a1); None if not self-avoiding"""
    x=[(0,0,0),(1,1,1),(0,2,2)]
    for s in w:
        b1=sub(x[-2],x[-3]); b2=sub(x[-1],x[-2]); cur=x[-1]
        cands=[sub(q,cur) for q in nbrs(cur) if q!=x[-2]]
        nxt=None
        for c in cands:
            if s==0 and c==b1: nxt=c
            elif s!=0 and c!=b1 and (det3(b1,b2,c)>0)==(s>0): nxt=c
        assert nxt is not None
        x.append(add(cur,nxt))
    return x if len(set(x))==len(x) else None

if __name__=="__main__":
    # fold word from the lamella with 3 stems: look at the first fold
    x=lamella(3,1,12); w=word(x)
    nz=[i for i,s in enumerate(w) if s!=0]
    fold=w[nz[0]:nz[0]+3]
    print("torsion word of my lamella(3,1,12):", "".join("t" if s==0 else ("+" if s>0 else "-") for s in w))
    print("fold word (first fold):", fold, " (S_REPORT: g+ g- g+ up to the sign convention)")
    assert build(w) is not None and measure(build(w))==measure(x), "word/build round trip"
    bad=0; lo=10**9; hi=-10**9; per=True; table={}
    AMAX=int(sys.argv[1]) if len(sys.argv)>1 else 40
    for a in range(3,AMAX+1):
        for b in range(3,AMAX+1):
            w1=[0]*a+fold+[0]*b; w2=[0]*a+[fold[0],0,fold[2]]+[0]*b
            x1=build(w1); x2=build(w2)
            if x1 is None or x2 is None: bad+=1; continue
            h1=measure_np(x1); h2=measure_np(x2)
            D=norm_c(tuple(h1[i]-h2[i] for i in range(3)))
            d=min(a+2,b+2); table[a,b]=(D,h1,h2)
            lo=min(lo,D-14*d); hi=max(hi,D-14*d)
    print(f"hairpins 3 <= a,b <= {AMAX}: {len(table)} pairs, not self-avoiding: {bad};  D - 14 d in [{lo}, {hi}]   (claim: >= -15; S_REPORT: [-15,-5])")
    ok1=all(table[a+2,b+2][0]==table[a,b][0]+28 for (a,b) in table if a>=5 and b>=5 and (a+2,b+2) in table)
    ok2=all(table[a,b+2][0]==table[a,b][0] for (a,b) in table if a>=5 and b>=a+6 and (a,b+2) in table)
    print(f"periodicity D(a+2,b+2)=D(a,b)+28 for a,b>=5: {ok1};  D(a,b+2)=D(a,b) for b>=a+6: {ok2}")
    a=b=10; D,h1,h2=table[a,b]; print(f"example a=b=10: hairpin (h,g)={h1}, opened (h,g)={h2}, D={D}, 14d-15={14*12-15}")
    # (2) engineering constants
    ENG="/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro/experiments/eng/chain_cover/results/lattice_Sc12_flip.json"
    import json
    try:
        J=json.load(open(ENG))
        print("\nengineering exact single-flip constants (keys):", list(J.keys())[:6] if isinstance(J,dict) else type(J))
    except Exception as e:
        print("could not read the engineering flip file:", e)
