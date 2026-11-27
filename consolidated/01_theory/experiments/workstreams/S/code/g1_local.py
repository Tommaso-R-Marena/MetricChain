#!/usr/bin/env python3
"""Check of the local counting identities (Lemma 1.3) and of the proved inequalities on real walks.

For every bridge with N <= NMAX beads (and a sample of lamellae):
   e8  = sum over ALL lattice sites m of C(d(m), 2),            d(m) = number of occupied neighbours of m,
   e11 = (1/2) * sum over all lattice bonds (v,w) of #{(u, z): u ~ v, z ~ w, u,z occupied, u != w, z != v, |u-z|^2 = 11},
and the 11 facet inequalities of the cluster LP in their finite form  c.h <= b N + 4 M + c3 + 2 c8,
and the hand-proved ones  4 h3 - 2 <= h8,  6 h3 - N - 4 <= h8 <= 2 h3 + 3 N + 3.
usage: g1_local.py NMAX
"""
import sys
from lat import *
import lamella as lam

F = [((-4, 2, -1), 2, 6), ((-3, 0, 2), 9, 3), ((-2, 1, 0), 3, 2), ((-1, 0, 0), 0, 0.5), ((-1, 1, -1), 0, 3), ((-1, 2, -1), 3, 4),
     ((0, -1, 2), 7, 1), ((3, 4, -3), 5, 6), ((4, -1, 0), 0, 5), ((6, -2, 1), 2, 6), ((6, -1, 0), 1, 6)]

def local_counts(pos):
    S = set(pos)
    cand = set()
    for p in S:
        cand.update(nbrs(p))
    cand |= S
    e8 = 0
    for m in cand:
        d = sum(1 for q in nbrs(m) if q in S)
        e8 += d * (d - 1) // 2
    # bonds (v,w) with v of type A: all bonds having at least one endpoint adjacent to S
    bonds = set()
    for m in cand:
        for q in nbrs(m):
            bonds.add((m, q) if is_A(m) else (q, m))
    g2 = 0
    for (v, w) in bonds:
        us = [u for u in nbrs(v) if u != w and u in S]
        zs = [z for z in nbrs(w) if z != v and z in S]
        g2 += sum(1 for u in us for z in zs if d2(u, z) == 11)
        assert all(d2(u, z) in (11, 19) for u in us for z in zs)
    assert g2 % 2 == 0
    return e8, g2 // 2

def check(pos, slack):
    N = len(pos)
    h3, h8, h11, g = profile(pos)
    e8, e11 = local_counts(pos)
    assert e8 == h8 + N - 2 and e11 == h11, (e8, h8, e11, h11)
    assert 4 * h3 - 2 <= h8 and 6 * h3 - N - 4 <= h8 <= 2 * h3 + 3 * N + 3
    for c, b, M in F:
        lhs = c[0] * h3 + c[1] * h8 + c[2] * h11
        rhs = b * N + 4 * M + c[0] + 2 * c[1]
        assert lhs <= rhs, (c, lhs, rhs)
        slack[c] = min(slack.get(c, 10**9), rhs - lhs)

def main():
    nmax = int(sys.argv[1])
    slack = {}
    n = 0
    for N in range(3, nmax + 1):
        for x in bridges(N):
            check(x, slack); n += 1
    for (M, Q, ell) in [(3, 1, 4), (5, 1, 8), (3, 3, 4), (5, 5, 6), (7, 7, 8), (9, 9, 10)]:
        check(lam.lamella(M, Q, ell), slack); n += 1
    print(f"walks checked: {n} (all bridges with N <= {nmax}, six lamellae); local identities and all inequalities hold")
    print("smallest slack of each facet inequality (finite form):", {str(k): v for k, v in slack.items()})

if __name__ == "__main__":
    main()
