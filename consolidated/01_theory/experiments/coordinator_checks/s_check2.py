#!/usr/bin/env python3
"""Coordinator spot checks of workstream S, part 2: the concatenation lemma for bridges (Lemma 3.1) and the
one-more-bead lemma (Lemma 3.2), with an own implementation.

For bridges x1, x2: P = last bead of x1, b = last bond vector of x1, b' = the bond before; c1 = b' if b' is an
up-bond, otherwise an up-bond out of P; linker l1 = P+c1, l2 = l1+b, l3 = l2+c1, Q = l3+b.  The copy of x2 is found by
brute force over the 48 signed permutation matrices R (x -> R(x - x2[0]) + Q): it must be a lattice walk, keep the
y-coordinate order (R fixes the y-axis), and start with the bonds (c1, b).  Claim: exactly one such copy exists; the
result is a bridge with N1+N2+3 beads and
   0 <= d3 <= 1, 0 <= d8 <= 9, 0 <= d11 <= 14, dg = [b' is a down-bond]."""
import sys, itertools, random
from s_lat import *

SIGNED_PERMS = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        SIGNED_PERMS.append((perm, sg))


def apply(R, v):
    perm, sg = R
    return (sg[0] * v[perm[0]], sg[1] * v[perm[1]], sg[2] * v[perm[2]])


def vsub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def vadd(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def concat(x1, x2, which=0):
    P = x1[-1]
    b = vsub(x1[-1], x1[-2])
    bp = vsub(x1[-2], x1[-3])
    assert b[1] == 1
    down = (bp[1] == -1)
    if not down:
        c1 = bp
    else:
        ups = [vsub(q, P) for q in nbrs(P) if q[1] == P[1] + 1]
        assert len(ups) == 2
        c1 = ups[which]
    l1 = vadd(P, c1); l2 = vadd(l1, b); l3 = vadd(l2, c1); Q = vadd(l3, b)
    copies = []
    for R in SIGNED_PERMS:
        if apply(R, (0, 1, 0)) != (0, 1, 0):
            continue
        img = [vadd(apply(R, vsub(p, x2[0])), Q) for p in x2]
        if vsub(img[1], img[0]) != c1 or vsub(img[2], img[1]) != b:
            continue
        if valid_walk(img):
            copies.append(img)
    assert len(copies) == 1, len(copies)
    x = x1 + [l1, l2, l3] + copies[0]
    assert valid_walk(x) and is_bridge(x) and len(x) == len(x1) + len(x2) + 3
    return x, down


def check_pair(x1, x2, p1, p2, stats):
    P = x1[-1]
    bp = vsub(x1[-2], x1[-3])
    for which in ((0, 1) if bp[1] == -1 else (0,)):
        x, down = concat(x1, x2, which)
        p = profile(x)
        d = tuple(p[i] - p1[i] - p2[i] for i in range(4))
        assert 0 <= d[0] <= 1 and 0 <= d[1] <= 9 and 0 <= d[2] <= 14, d
        assert d[3] == (1 if down else 0), d
        for i in range(4):
            stats[i] = max(stats[i], d[i])
        stats[4] += 1


def one_more(x1, p1):
    P = x1[-1]
    b = vsub(x1[-1], x1[-2]); bp = vsub(x1[-2], x1[-3])
    cs = [bp] if bp[1] == 1 else [vsub(q, P) for q in nbrs(P) if q[1] == P[1] + 1]
    for c1 in cs:
        x = x1 + [vadd(P, c1)]
        assert valid_walk(x) and is_bridge(x)
        p = profile(x)
        d = tuple(p[i] - p1[i] for i in range(4))
        assert 0 <= d[0] <= 1 and 0 <= d[1] <= 3 and 0 <= d[2] <= 6 and d[3] == (0 if bp[1] == 1 else 1), d


def main():
    nfull = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    nsamp = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    nrand = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    br = {N: enum_walks(N, bridge=True) for N in range(3, nsamp + 1)}
    pr = {N: [profile(w) for w in br[N]] for N in br}
    print("bridges from an A site:", {N: len(br[N]) for N in br})
    for N in br:
        for w, p in zip(br[N], pr[N]):
            one_more(w, p)
    print("Lemma 3.2 (one more bead): increments in [0,1]x[0,3]x[0,6], gauche increment = [b' down]: OK for all bridges listed")
    stats = [0, 0, 0, 0, 0]
    for N1 in range(3, nfull + 1):
        for N2 in range(3, nfull + 1):
            for i, x1 in enumerate(br[N1]):
                for j, x2 in enumerate(br[N2]):
                    check_pair(x1, x2, pr[N1][i], pr[N2][j], stats)
    print(f"Lemma 3.1: all pairs with 3 <= N1, N2 <= {nfull}: {stats[4]} concatenations, max (d3, d8, d11, dg) = {tuple(stats[:4])}: OK")
    rng = random.Random(20261125)
    stats = [0, 0, 0, 0, 0]
    for _ in range(nrand):
        N1 = rng.randint(3, nsamp); N2 = rng.randint(3, nsamp)
        i = rng.randrange(len(br[N1])); j = rng.randrange(len(br[N2]))
        check_pair(br[N1][i], br[N2][j], pr[N1][i], pr[N2][j], stats)
    print(f"Lemma 3.1: {nrand} random pairs with N1, N2 <= {nsamp}: {stats[4]} concatenations, max (d3, d8, d11, dg) = {tuple(stats[:4])}: OK")
    print("PART 2 OK")


if __name__ == "__main__":
    main()
