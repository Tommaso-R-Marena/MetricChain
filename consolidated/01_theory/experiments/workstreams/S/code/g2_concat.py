#!/usr/bin/env python3
"""G2 check: the concatenation lemma for y-bridges, with its constants.

For every ordered pair (x1, x2) of bridges with N1, N2 beads (all pairs if few, otherwise a random sample),
build the concatenation of Lemma 2.1:   x1,  three linker beads at heights H+1, H+2, H+3 above the top bead of x1
(linker bonds c1,c2,c3,c4 all "up", c2 = c4 = last bond of x1, c3 = c1, c1 = the bond before the last bond of x1
if that bond is "up"),  then an image of x2 under a lattice symmetry that preserves y.
Recount the profile and the gauche number of the result from scratch and record
    delta = (h, g)(x) - (h, g)(x1) - (h, g)(x2).
Checks: x is a self-avoiding lattice walk, a bridge, has N1+N2+3 beads; delta within the bounds of the lemma;
delta_g = [second-to-last bond of x1 is down] + [second bond of x2 is down].

usage: g2_concat.py NMAX [SAMPLE] [SEED]
"""
import sys, random
from lat import *

def concat(x1, x2):
    """return the list of all valid concatenations (one per admissible symmetry and choice of c1)"""
    P = x1[-1]
    b = sub(x1[-1], x1[-2])                       # last bond, up
    assert b[1] == 1
    ups_P = [sub(q, P) for q in nbrs(P) if q[1] > P[1]]      # the two up bonds from P
    res = []
    for c1 in ups_P:
        l1 = add(P, c1); l2 = add(l1, b); l3 = add(l2, c1); Q = add(l3, b)
        bonds2 = [sub(x2[i + 1], x2[i]) for i in range(len(x2) - 1)]
        for M in YMAPS:
            pos = [Q]
            for v in bonds2:
                pos.append(add(pos[-1], M(v)))
            x = list(x1) + [l1, l2, l3] + pos
            if is_walk(x):
                res.append(x)
    return res

def main():
    nmax = int(sys.argv[1]); sample = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    B = {N: bridges(N) for N in range(3, nmax + 1)}
    prof = {N: [profile(x) for x in B[N]] for N in B}
    print("bridges starting at an A site:", {N: len(B[N]) for N in B})
    lo = [10**9] * 4; hi = [-10**9] * 4
    npairs = 0
    worst = {}
    for N1 in B:
        for N2 in B:
            n1, n2 = len(B[N1]), len(B[N2])
            if n1 * n2 > sample:
                pairs = [(rng.randrange(n1), rng.randrange(n2)) for _ in range(sample)]
            else:
                pairs = [(i, j) for i in range(n1) for j in range(n2)]
            for (i, j) in pairs:
                x1, x2 = B[N1][i], B[N2][j]
                p1, p2 = prof[N1][i], prof[N2][j]
                cands = concat(x1, x2)
                assert cands, "no valid concatenation"
                # expected gauche excess
                b_prev = sub(x1[-2], x1[-3]); u2 = sub(x2[2], x2[1])
                expect = (1 if b_prev[1] < 0 else 0) + (1 if u2[1] < 0 else 0)
                best = None
                for x in cands:
                    assert len(x) == N1 + N2 + 3 and is_bridge(x)
                    p = profile(x)
                    assert p == profile_def(x)
                    dl = tuple(p[k] - p1[k] - p2[k] for k in range(4))
                    if best is None or dl[3] < best[3] or (dl[3] == best[3] and dl < best):
                        best = dl
                # the prescribed choice (c1 = b_prev if up; second bond of the image of x2 = b if up) attains `expect`
                assert best[3] == expect, (best, expect)
                # bounds must hold for EVERY candidate with minimal gauche excess; record extremes over those
                for x in cands:
                    p = profile(x)
                    dl = tuple(p[k] - p1[k] - p2[k] for k in range(4))
                    if dl[3] != expect:
                        continue
                    for k in range(4):
                        lo[k] = min(lo[k], dl[k]); hi[k] = max(hi[k], dl[k])
                    assert 0 <= dl[0] <= 1 and 0 <= dl[1] <= 9 and 0 <= dl[2] <= 14 and 0 <= dl[3] <= 1, dl
                npairs += 1
    print(f"pairs checked: {npairs}")
    print("delta (h3, h8, h11, g): observed min", lo, " observed max", hi, "  proved bounds: [0,1] [0,9] [0,14] [0,1]")

if __name__ == "__main__":
    main()
