#!/usr/bin/env python3
"""R2 — bridge class tables: (1) mine vs the authors' stored tables (experiments/workstreams/S/out);
(2) set-level form of conditions (C) and (E) of Theorem 11.69 on the complete sets
P_N = {(h,g) of bridges with N beads}:  for q1 in P_N1, q2 in P_N2 there is q in P_{N1+N2+3} with
q-q1-q2 in [0,1]x[0,9]x[0,14]x{0,1};  for q in P_N there is q' in P_{N+1} with q'-q in [0,1]x[0,3]x[0,6]x{0,1};
(3) one-sided consequence of the rate (i) of the abstract lemma, on data:
    every point of Q_m/m is within beta/m + m(beta'+R)/M of Q_M/M (Q_M = P_{M-3});
(4) R = 36: max of (9h3+4h8+h11+g)/N.
"""
import os, sys, itertools
HERE=os.path.dirname(os.path.abspath(__file__))
SOUT="/home/user/MetricChain/experiments/workstreams/S/out"
def load(path, cols):
    P=set(); tab={}
    for line in open(path):
        if line.startswith("#"): continue
        f=line.split(); h=tuple(map(int,f[:3])); mask=int(f[cols["mask"]],16 if cols.get("hex") else 10)
        tab[h]=(int(f[3]),int(f[cols["gmin"]]),int(f[cols["gmax"]]),mask)
        g=0
        while mask:
            if mask&1: P.add(h+(g,))
            mask>>=1; g+=1
    return P,tab
mine={}; theirs={}
for N in range(3,30):
    f=f"{HERE}/out/bridge_N{N}.txt"
    if os.path.exists(f) and os.path.getsize(f)>0: mine[N]=load(f,{"gmin":4,"gmax":6,"mask":7,"hex":True})
    f=f"{SOUT}/bridge_N{N}.txt"
    if os.path.exists(f): theirs[N]=load(f,{"gmin":4,"gmax":5,"mask":6,"hex":True})
print("(1) own bridge tables vs the authors' stored tables")
for N in sorted(mine):
    if N in theirs:
        Pm,tm=mine[N]; Pt,tt=theirs[N]
        ratio={tt[h][0]/tm[h][0] for h in tm if h in tt}
        same_cls=set(tm)==set(tt); same_g=all(tm[h][1:]==tt[h][1:] for h in tm if h in tt)
        print(f"  N={N:2d}: classes mine {len(tm)} theirs {len(tt)} same classes={same_cls}; gmin,gmax,gmask identical={same_g}; (h,g) sets identical={Pm==Pt}; count ratio theirs/mine={sorted(ratio)}")
    else:
        print(f"  N={N:2d}: classes mine {len(mine[N][1])}, |P_N|={len(mine[N][0])} (no stored table of the authors)")
P={N:mine[N][0] for N in mine}
print("\n(2) set-level (C): for all N1<=N2 with N1+N2+3 available")
Nmax=max(P); worst_fail=0; tested=0
for N1 in sorted(P):
    for N2 in sorted(P):
        if N2<N1 or N1+N2+3>Nmax: continue
        T=P[N1+N2+3]; bad=0
        for q1 in P[N1]:
            for q2 in P[N2]:
                tested+=1
                s=tuple(a+b for a,b in zip(q1,q2))
                ok=False
                for d3 in (0,1):
                    for dg in (0,1):
                        for d8 in range(10):
                            for d11 in range(15):
                                if (s[0]+d3,s[1]+d8,s[2]+d11,s[3]+dg) in T: ok=True;break
                            if ok:break
                        if ok:break
                    if ok:break
                bad+=(not ok)
        worst_fail+=bad
        if bad: print(f"   FAIL N1={N1} N2={N2}: {bad}")
print(f"   pairs of points tested: {tested}; failures: {worst_fail}")
print("(2') set-level (E):")
bad=0;tested=0
for N in sorted(P):
    if N+1 not in P: continue
    for q in P[N]:
        tested+=1
        if not any((q[0]+a,q[1]+b,q[2]+c,q[3]+d) in P[N+1] for a in (0,1) for b in range(4) for c in range(7) for d in (0,1)): bad+=1
print(f"   points tested: {tested}; failures: {bad}")
print("\n(3) approximate nestedness on data: sup over q in Q_m/m of dist(q, Q_M/M) vs beta/m + m(beta'+R)/M  (norm ||.||_c+|g|; Q_M=P_{M-3})")
def nc(d): return 5*abs(d[0])+3*abs(d[0]+d[1])+abs(d[0]+d[1]+d[2])+abs(d[3])
for m in (6,8,10):
    for M in (2*m,3*m, Nmax+3):
        if m-3 not in P or M-3 not in P or M<m: continue
        sup=0.0
        for q in P[m-3]:
            best=min(nc(tuple(a/M-b/m for a,b in zip(r,q))) for r in P[M-3])
            sup=max(sup,best)
        print(f"   m={m} (N={m-3}) M={M} (N={M-3}): sup dist = {sup:.4f}   bound = {60/m+m*(28+36)/M:.3f}")
print("\n(4) max over bridges of (9h3+4h8+h11+g)/N (R=36):", {N:round(max((9*q[0]+4*q[1]+q[2]+q[3])/N for q in P[N]),3) for N in sorted(P)})
