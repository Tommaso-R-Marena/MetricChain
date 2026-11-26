"""The level-2 outer-labeled planar bloblets that are NOT galled, as a three-parameter family N[kB, k1, k2].

Skeleton (rooted partner): a theta graph with branch vertices h1 (hybrid; two incoming paths A, B, one outgoing path C)
and t; the second hybrid h2 lies inside C.  Outer-labeled planarity forces the middle path (A, say) to carry no leaf.
    kB leaves b_1..b_kB on B (b_1 nearest to h1),   k1 leaves x_1..x_k1 on C between h1 and h2 (x_1 nearest to h1),
    one leaf y below h2,                             k2 leaves c_1..c_k2 on C between h2 and t (c_1 nearest to h2).
Circular order:  b_1, ..., b_kB, c_k2, ..., c_1, y, x_k1, ..., x_1.      N* of counterexample7.py is N[4, 1, 1].

Four displayed trees (keep the B-edge or the A-edge at h1; keep the x-side or the c-side edge at h2):
    T1 (B, x-side): caterpillar  c_1 .. c_k2 | b_kB .. b_1 | x_1 .. x_k1 | y
    T2 (A, x-side): three arms at t:  (b_1 .. b_kB),  (c_1 .. c_k2),  (y, x_k1 .. x_1)
    T3 (B, c-side): caterpillar  y | c_1 .. c_k2 | b_kB .. b_1 | x_1 .. x_k1
    T4 (A, c-side): three arms at t:  (b_1 .. b_kB),  (y, c_1 .. c_k2),  (x_k1 .. x_1)

Usage:  python3 level2_nongalled.py [max_leaves]      (default 11)
"""
import sys
from itertools import combinations
from splitsys import *


def leaves(kB, k1, k2):
    """names in circular order, and index maps"""
    names = [("b", i) for i in range(1, kB + 1)] + [("c", i) for i in range(k2, 0, -1)] + [("y", 0)] + \
            [("x", i) for i in range(k1, 0, -1)]
    return names, {nm: i for i, nm in enumerate(names)}


def caterpillar_splits(n, seq):
    out = set()
    m = 0
    for i, l in enumerate(seq[:-1]):
        m |= 1 << l
        out.add(canon(n, m))
    return out


def arms_splits(n, arms):
    out = set()
    for arm in arms:                       # from the far end to the centre
        m = 0
        for l in arm:
            m |= 1 << l
            if m != (1 << n) - 1:
                out.add(canon(n, m))
    return out


def system(kB, k1, k2):
    names, ix = leaves(kB, k1, k2)
    n = len(names)
    b = [ix[("b", i)] for i in range(1, kB + 1)]
    x = [ix[("x", i)] for i in range(1, k1 + 1)]
    c = [ix[("c", i)] for i in range(1, k2 + 1)]
    y = ix[("y", 0)]
    trees = [
        caterpillar_splits(n, c + b[::-1] + x + [y]),
        arms_splits(n, [b, c, [y] + x[::-1]]),
        caterpillar_splits(n, [y] + c + b[::-1] + x),
        arms_splits(n, [b, [y] + c, x[::-1]]),
    ]
    sigma = set()
    for t in trees:
        sigma |= t
    for l in range(n):
        sigma.add(canon(n, 1 << l))
    return n, names, sigma, trees


def pattern_restrictions(n, sigma):
    """six-subsets whose restriction contains the three 3-splits and misses a 2-split"""
    out = []
    for Y in combinations(range(n), 6):
        idx = {yv: k for k, yv in enumerate(Y)}
        rest = set()
        for m in sigma:
            mm = 0
            for yv in Y:
                if (m >> yv) & 1:
                    mm |= 1 << idx[yv]
            if mm != 0 and mm != 63:
                rest.add(canon(6, mm))
        three = {canon(6, 0b000111), canon(6, 0b001110), canon(6, 0b011100)}
        two = [canon(6, 0b000011 << k) if k < 5 else canon(6, 0b100001) for k in range(6)]
        if three <= rest and not all(t in rest for t in two):
            out.append(Y)
    return out


def status(kB, k1, k2):
    n, names, sigma, trees = system(kB, k1, k2)
    D = nanuq_2d(n, sigma)
    al = alphas_2(n, D)
    neg = [(g, v) for g, v in al.items() if v < 0]
    wrong = []
    for (i, j), v in al.items():
        m = 0
        for q in range(i + 1, j + 1):
            m |= 1 << q
        insys = canon(n, m) in sigma
        if (v > 0) != insys and v >= 0:
            wrong.append(((i, j), v))
    return n, names, sigma, al, neg, wrong


if __name__ == "__main__":
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    # anchor: N* = N[4,1,1] has the metric printed in the note (order a1,a2,b,x,y,c,d)
    n, names, sigma, trees = system(4, 1, 1)
    D = nanuq_2d(n, sigma)
    ix = {nm: i for i, nm in enumerate(names)}
    order = [("b", 3), ("b", 2), ("b", 1), ("x", 1), ("y", 0), ("c", 1), ("b", 4)]      # a1, a2, b, x, y, c, d
    M = [[D[ix[p]][ix[q]] // 2 for q in order] for p in order]
    target = [[0, 21, 23, 26, 26, 23, 21], [21, 0, 17, 24, 26, 27, 25], [23, 17, 0, 20, 24, 29, 27],
              [26, 24, 20, 0, 20, 24, 26], [26, 26, 24, 20, 0, 20, 24], [23, 27, 29, 24, 20, 0, 17],
              [21, 25, 27, 26, 24, 17, 0]]
    print("anchor: N[4,1,1] reproduces the metric of N* printed in the note:", M == target)
    print()
    print(" kB k1 k2   n | pattern-free | Kalmanson (planar order) | exact support | negative weights (min)")
    for tot in range(3, maxn):
        for kB in range(0, tot + 1):
            for k1 in range(0, tot - kB + 1):
                k2 = tot - kB - k1
                n, names, sigma, al, neg, wrong = status(kB, k1, k2)
                if n < 4:
                    continue
                pat = pattern_restrictions(n, sigma) if n >= 6 else []
                print(f" {kB:2d} {k1:2d} {k2:2d}  {n:2d} | {'yes' if not pat else 'NO ':>12} | {'yes' if not neg else 'NO ':>24} |"
                      f" {'yes' if not neg and not wrong else 'no ':>13} | {min(v for _, v in neg) // 2 if neg else ''}"
                      f"{'   wrong support: ' + str(len(wrong)) if wrong and not neg else ''}")
