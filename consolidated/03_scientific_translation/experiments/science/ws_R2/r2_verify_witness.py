#!/usr/bin/env python3
"""R2 — explicit bridges built by the AUTHORS' generator (experiments/workstreams/S/code/build.py,
imported read-only, no bytecode written), verified by MY code: lattice walk, injective, bridge,
(h,g) by r2_lamella.measure_np (site-set counts + 1-4 distances).

A witness is data: once its coordinates are verified independently it does not matter how it
was produced.  For each bridge with N beads Theorem 11.69 gives a point of K^br within
168/(N+3) (norm ||p||_c+|g|).

usage: r2_verify_witness.py big      -> the 166 199-bead bridge of Proposition 11.72(e)
       r2_verify_witness.py nine W   -> the nine periodic systems of S_REPORT §4.2 in a box of side W,
                                       and a RIGOROUS inner volume for the profile body
"""
import sys, os, itertools, json
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
SCODE="/home/user/MetricChain/experiments/workstreams/S/code"
sys.path.append(SCODE)
import numpy as np
from fractions import Fraction as Fr
import build as B                      # authors' generator
from r2_lattice import lat, is_bridge, norm_c
from r2_lamella import measure_np

WIT={
 "W3 woodpile (0,3,4;0)": "hnf rows (1 0 0) (0 1 2) (0 0 3); path bonds A(n)-type: A(0,0,1):a2,a3 A(0,0,2):a0,a1",
 "checkerboard (0,1,3;0)": "hnf rows (1 0 0) (0 1 1) (0 0 2); path bonds A(n)-type: A(0,0,1):a0,a1",
 "coplanar sheets (0,0,1;0)": "hnf rows (1 0 0) (0 1 1) (0 0 3); path bonds A(n)-type: A(0,0,2):a0,a1",
 "rods (1/2,2,5/2;0)": "hnf rows (1 0 0) (0 1 1) (0 0 4); path bonds A(n)-type: A(0,0,2):a0,a1 A(0,0,3):a0,a1",
 "crossed rods (1/2,4,9/2;0)": "hnf rows (1 0 0) (0 1 4) (0 0 5); path bonds A(n)-type: A(0,0,1):a2,a3 A(0,0,2):a2,a3 A(0,0,3):a0,a1 A(0,0,4):a0,a1",
 "crystal (1,5,6;0)": "hnf rows (1 0 0) (0 1 0) (0 0 1); path bonds A(n)-type: A(0,0,0):a0,a1",
 "gauche-rich (0,12/5,22/5;4/5)": "hnf rows (1 0 1) (0 1 4) (0 0 8); path bonds A(n)-type: A(0,0,2):a0,a3 A(0,0,4):a0,a2 A(0,0,5):a2,a3 A(0,0,6):a1,a2 A(0,0,7):a0,a1",
 "gauche-rich (1/3,5/3,3;2/3)": "hnf rows (1 0 2) (0 1 3) (0 0 6); path bonds A(n)-type: A(0,0,2):a0,a1 A(0,0,4):a0,a2 A(0,0,5):a1,a2",
 "all-gauche (0,1/2,9/4;1)": "hnf rows (1 0 4) (0 1 5) (0 0 10); path bonds A(n)-type: A(0,0,4):a0,a1 A(0,0,6):a0,a2 A(0,0,7):a1,a3 A(0,0,9):a2,a3",
}
def build_bridge(w,W):
    hnf,ch=B.parse(w)
    strands=B.strands_in_box(hnf,ch,(W,W,W))
    walk,nlink,dropped,ns=B.link(strands)
    return B.make_bridge(walk)
def verify(b):
    """my verification, nothing of the authors' used"""
    assert all(lat(s) for s in b), "non-lattice site"
    assert is_bridge(b), "not a bridge"
    return measure_np(b)            # asserts bonded + injective + 1-4 distances in {11,19}

if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="big":
        b=build_bridge(WIT["gauche-rich (0,12/5,22/5;4/5)"],128)
        N=len(b); h3,h8,h11,g=verify(b)
        print(f"bridge from the system (0,12/5,22/5;4/5), box 128: N = {N}; verified by my code: self-avoiding lattice walk, bridge; (h3,h8,h11,g) = ({h3},{h8},{h11},{g})")
        print(f"   report: N = 166199, (1717, 376013, 687789, 131710): match = {(N,h3,h8,h11,g)==(166199,1717,376013,687789,131710)}")
        val=2*h11-5*h3-8*N
        print(f"   2h11-5h3-8N = {val} = {val/N:.5f} N   (report: 37401 = 0.225N);  168/(N+3) = {168/(N+3):.6f}")
        print(f"   => a point (p*,g*) of K^br with 2p11*-5p3*-8 >= {val/N:.5f} - 2*{168/(N+3):.5f} = {val/N-2*168/(N+3):.5f}; by the gauche bound of Prop 11.72(c), gamma(p*) >= that  (report: >= 0.22)")
        print(f"   g/N = {g/N:.5f}")
    else:
        Wd=int(sys.argv[2]); pts=[]; dmax=0
        for name,w in WIT.items():
            b=build_bridge(w,Wd)
            if b is None: print(f"  {name}: builder failed"); continue
            N=len(b); h3,h8,h11,g=verify(b)
            d=168/(N+3); dmax=max(dmax,d)
            pts.append((name,N,(h3,h8,h11,g)))
            print(f"  {name:32s} box {Wd}: N = {N:6d}  (h,g)/N = ({h3/N:.4f}, {h8/N:.4f}, {h11/N:.4f}; {g/N:.4f})  exact ({h3},{h8},{h11},{g})   168/(N+3) = {d:.5f}",flush=True)
        json.dump([(n,N,list(q)) for n,N,q in pts],open(f"{HERE}/out/witness_points_W{Wd}.json","w"))
