#!/usr/bin/env python3
"""R2 — direct tests on finite site sets (not necessarily walks):
 (1) Prop 11.72(b): c3(e3-N)+c8(e8-N)+c11 e11 <= bN + 2M n_E for the eleven rows
     - on ALL subsets of a fixed 16-site lattice animal neighbourhood (65 535 sets),
     - on random subsets of a box (sparse and dense), random connected animals.
 (2) Prop 11.73: e3 <= 2N - 2^(-2/3) N^(2/3), e8 <= 6N - 3 N^(2/3) on the same sets and on
     compact sets (balls, cubes, octahedra of lattice sites) where it is closest to tight.
"""
import sys, os, itertools, random, math
from fractions import Fraction as Fr
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from r2_lattice import *
ROWS=[((-1,0,0),0,Fr(1,2)),((4,-1,0),0,5),((6,-1,0),1,6),((-2,1,0),3,2),((-1,1,-1),0,3),((-1,2,-1),3,4),
      ((-4,2,-1),2,6),((3,4,-3),5,6),((6,-2,1),2,6),((0,-1,2),7,1),((-3,0,2),9,3)]
def check(S,stats):
    S=set(S); N=len(S)
    if N==0: return
    e3,e8,e11=site_e(S)
    nE=sum(1 for s in S if sum(1 for q in nbrs(s) if q in S)<2)
    for i,(c,b,M) in enumerate(ROWS):
        lhs=c[0]*(e3-N)+c[1]*(e8-N)+c[2]*e11; rhs=b*N+2*M*nE
        assert lhs<=rhs, ("VIOLATION 11.72(b)",c,sorted(S))
        stats[i]=max(stats[i],lhs-b*N-2*M*nE)
    assert e3<=2*N-2**(-2/3)*N**(2/3)+1e-9 and e8<=6*N-3*N**(2/3)+1e-9, ("VIOLATION 11.73",sorted(S))
    stats["iso3"]=max(stats["iso3"],(2*N-e3)/N**(2/3) and -(2*N-e3)/N**(2/3))
    stats["iso8"]=max(stats["iso8"],-(6*N-e8)/N**(2/3))
if __name__=="__main__":
    rng=random.Random(5)
    stats={i:-10**9 for i in range(len(ROWS))}; stats["iso3"]=-1e9; stats["iso8"]=-1e9
    # (a) all subsets of a 16-site connected piece: a site, its neighbours, and more, grown breadth-first
    piece=[(0,0,0)]
    for s in piece:
        for t in nbrs(s):
            if t not in piece and len(piece)<16: piece.append(t)
    n=0
    for mask in range(1,1<<16):
        check([piece[i] for i in range(16) if mask>>i&1],stats); n+=1
    print(f"(a) all {n} non-empty subsets of a 16-site connected piece: no violation")
    # (b) random subsets of a box at various densities
    box=[s for s in itertools.product(range(-4,7),repeat=3) if lat(s)]
    for t in range(4000):
        dens=rng.random(); check([s for s in box if rng.random()<dens],stats)
    print(f"(b) 4000 random subsets of a box of {len(box)} sites (all densities): no violation")
    # (c) random connected animals
    for t in range(3000):
        S={(0,0,0)}; target=rng.randint(2,120)
        while len(S)<target:
            s=rng.choice(list(S)); S.add(rng.choice(nbrs(s)))
        check(S,stats)
    print("(c) 3000 random connected animals (2..120 sites): no violation")
    # (d) compact sets
    big=[s for s in itertools.product(range(-14,15),repeat=3) if lat(s)]
    best3=1e9; best8=1e9
    for R2 in range(3,180,4):
        for S in ([s for s in big if d2(s,(0,0,0))<=R2], [s for s in big if max(abs(c) for c in s)**2<=R2/3], [s for s in big if (abs(s[0])+abs(s[1])+abs(s[2]))**2<=R2*2]):
            if not S: continue
            check(S,stats); N=len(S); e3,e8,e11=site_e(S)
            best3=min(best3,(2*N-e3)/N**(2/3)); best8=min(best8,(6*N-e8)/N**(2/3))
    print(f"(d) balls / cubes / octahedra of lattice sites up to {len(big)} sites: no violation;  min (2N-e3)/N^(2/3) = {best3:.3f} (proved >= {2**(-2/3):.3f}),  min (6N-e8)/N^(2/3) = {best8:.3f} (proved >= 3)")
    print("largest value of [lhs - bN - 2M n_E] per row (must be <= 0):", [str(stats[i]) for i in range(len(ROWS))])
