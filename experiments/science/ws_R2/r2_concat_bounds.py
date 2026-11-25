#!/usr/bin/env python3
"""R2 — the constants of Lemma 11.68, re-derived by counting lattice sites by height.

For each of the 8 ordered pairs (c1, b) = (up-bond out of P, up-bond out of P+c1):
  linker l1=P+c1, l2=l1+b, l3=l2+c1, Q=l3+b, H = height of P.
  S1 can only contain lattice sites of height <= H; S2 only Q (height H+4) and sites of
  height >= H+5.  Count the pairs (linker site, such site) at squared distance 3, 8, 11.
  These counts minus the chain neighbours across the junctions are upper bounds for
  (delta3, delta8, delta11).  Also: the facts F1, F2 (heights of the neighbour shells) and
  the distance l1-Q = 19, and the same count for appending 1..5 beads only (condition (E)
  and the extension of Q_M to M<6 needed to apply the Lean theorem).
"""
import itertools
A=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
def is_A(s): return all(c%2==0 for c in s) and sum(s)%4==0
def is_B(s): return is_A(tuple(c-1 for c in s))
def lat(s): return is_A(s) or is_B(s)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def d2(a,b): return sum((x-y)**2 for x,y in zip(a,b))
def bonds(s):
    sg=1 if is_A(s) else -1
    return [tuple(sg*c for c in a) for a in A]
R=range(-8,13)
SITES=[s for s in itertools.product(R,R,R) if lat(s)]
# F1, F2
for s0 in [(0,0,0),(1,1,1)]:
    for d in (3,8,11):
        hs={}
        for s in SITES:
            if d2(s,s0)==d: hs[s[1]-s0[1]]=hs.get(s[1]-s0[1],0)+1
        print(f"site {s0} ({'A' if is_A(s0) else 'B'}): shell d2={d}: {sum(hs.values())} sites, by relative height {dict(sorted(hs.items()))}")
    ups=[b for b in bonds(s0) if b[1]==1]; downs=[b for b in bonds(s0) if b[1]==-1]
    print(f"   up-bonds {ups}  down-bonds {downs}")
# all squared distances < 12 between lattice sites and their height differences
ds=sorted({d2(s,(0,0,0)) for s in SITES if 0<d2(s,(0,0,0))<20})
print("squared distances from an A site below 20:", ds)
mh=max(abs(s[1]) for s in SITES if 0<d2(s,(0,0,0))<12)
print("largest height difference at squared distance < 12:", mh)
print()
worst=None
for P in [(0,0,0),(1,1,1)]:
    for c1 in [b for b in bonds(P) if b[1]==1]:
        l1=add(P,c1)
        for b in [bb for bb in bonds(l1) if bb[1]==1]:
            H=P[1]
            l2=add(l1,b); l3=add(l2,c1); Q=add(l3,b)
            assert all(lat(s) for s in (l1,l2,l3,Q)) and d2(l1,l2)==3 and d2(l2,l3)==3 and d2(l3,Q)==3
            link=[l1,l2,l3]
            S1=[s for s in SITES if s[1]<=H]
            S2=[s for s in SITES if s[1]>=H+5]+[Q]
            cnt={}
            for name,S in (("S1",S1),("S2",S2)):
                for d in (3,8,11):
                    cnt[name,d]=sum(1 for l in link for s in S if d2(l,s)==d)
            # chain neighbours across the junctions (always present): (l1,P) d=3; (l1,P-b) d=8; (l2,P) d=8;
            # (l3,Q) d=3; (l2,Q) d=8; (l3,Q+c1) d=8
            d3=(cnt["S1",3]-1)+(cnt["S2",3]-1); d8=(cnt["S1",8]-2)+(cnt["S2",8]-2); d11=cnt["S1",11]+cnt["S2",11]
            # appending k beads only (zigzag l1,l2,l3,l4=l3+b,l5=l4+c1)
            l4=add(l3,b); l5=add(l4,c1)
            ext=[]
            for k in range(1,6):
                lk=[l1,l2,l3,l4,l5][:k]
                e3=sum(1 for l in lk for s in S1 if d2(l,s)==3)-1
                e8=sum(1 for l in lk for s in S1 if d2(l,s)==8)-(1 if k==1 else 2)
                e11=sum(1 for l in lk for s in S1 if d2(l,s)==11)
                ext.append((e3,e8,e11,9*e3+4*e8+e11+1))
            print(f"P={P} c1={c1} b={b}: pairs linker–S1 (d=3,8,11) = {cnt['S1',3]},{cnt['S1',8]},{cnt['S1',11]}; linker–S2 = {cnt['S2',3]},{cnt['S2',8]},{cnt['S2',11]};"
                  f" |l1-Q|^2={d2(l1,Q)}  => delta <= ({d3},{d8},{d11}), norm <= {9*d3+4*d8+d11+1}")
            print(f"     appending k=1..5 beads: (d3,d8,d11 bounds, norm incl. one gauche) = {ext}")
            worst=max(worst or (0,0,0),(d3,d8,d11))
print("\nworst case over the 8 pairs:", worst, " (lemma: (1, 9, 14), beta = 60; one bead: (1,3,6), beta' = 28)")
