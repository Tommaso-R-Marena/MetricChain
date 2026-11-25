#!/usr/bin/env python3
"""Explicit rung-folded lamellae (Proposition 5.2): bridges whose site set is an M x Q block of parallel all-trans
stems (rods along (0,1,1)) and whose folds are single lattice bonds ("rungs") -- no linker sites.

Rod (m,q):  A_k = m(2,2,0) + q(2,0,2) + k(0,2,2),  B_k = A_k + (1,1,1);   position t = 2k (A_k) or 2k+1 (B_k).
Bonds inside a rod: t ~ t+1.  Rungs:  B^{(m,q)}_k ~ A^{(m+1,q)}_k  and  B^{(m,q)}_k ~ A^{(m,q+1)}_k.
Snake: rows q = 0..Q-1 (Q odd), row q traversed in direction +m (q even) or -m (q odd), M odd; stems alternately
up and down; the first stem starts one period lower, the last one ends one period higher.

usage: lamella.py   (prints a table of sizes, exact counts and densities)
"""
import sys
from lat import *

def site(m, q, t):
    k, r = divmod(t, 2)
    p = (2 * m + 2 * q, 2 * m + 2 * k, 2 * q + 2 * k)
    return add(p, (1, 1, 1)) if r else p

def lamella(M, Q, ell):
    rods = []
    for q in range(Q):
        ms = range(M) if q % 2 == 0 else range(M - 1, -1, -1)
        rods += [(m, q) for m in ms]
    walk = []
    t_in = -2                      # A_{-1}: the first stem starts one period lower
    up = True
    for i, (m, q) in enumerate(rods):
        last = (i == len(rods) - 1)
        if last:
            assert up
            t_out = 2 * ell + 1    # B_ell: one period higher
        else:
            m2, q2 = rods[i + 1]
            plus = (m2, q2) in ((m + 1, q), (m, q + 1))        # rung B^{r}_k ~ A^{r'}_k
            k = ell - 1 if up else 0
            t_out = 2 * k + 1 if plus else 2 * k               # leave from B_k ("+") or from A_k ("-")
        step = 1 if up else -1
        assert (t_out - t_in) * step >= 0, "stem too short"
        walk += [site(m, q, t) for t in range(t_in, t_out + step, step)]
        if not last:
            t_in = 2 * k if plus else 2 * k + 1                # arrive at A_k ("+") or at B_k ("-")
            up = not up
    return walk

def main():
    print("# M Q ell |   N    (h3, h8, h11, g)    | h3/N    h8/N   h11/N    g/N   | ideal (0.5,2,1.5) for Q=1, (1,5,6) for M,Q large")
    for (M, Q, ell) in [(3, 1, 4), (5, 1, 8), (9, 1, 16), (17, 1, 32), (33, 1, 64), (65, 1, 128),
                        (3, 3, 4), (5, 5, 6), (7, 7, 8), (9, 9, 10), (13, 13, 14), (17, 17, 18), (21, 21, 22), (25, 25, 26)]:
        w = lamella(M, Q, ell)
        assert is_walk(w) and is_bridge(w)
        N = len(w); p = profile(w)
        print(f"  {M:2d} {Q:2d} {ell:3d} | {N:6d} {str(p):>26} | {p[0]/N:6.4f} {p[1]/N:7.4f} {p[2]/N:7.4f} {p[3]/N:7.4f}"
              f" | N^(-1/3) = {N**(-1/3):.4f}, (1 - h3/N) N^(1/3) = {(1 - p[0]/N) * N**(1/3):.3f}")

if __name__ == "__main__":
    main()
