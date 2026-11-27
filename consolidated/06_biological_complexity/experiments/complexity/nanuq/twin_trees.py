"""Class A: planar binary trees with twin leaves.

An A-structure on n leaves with k twins is a binary tree T on N = n + k circularly ordered positions
together with k pairwise disjoint pairs of circularly adjacent positions.  Its displayed trees keep one
position of every pair; its split system is the union of their split systems.  (These are exactly the
outer-labeled planar galled networks all of whose hybrid nodes have a leaf child; no bloblet condition.)

A_systems(n) returns all split systems of A-structures on n leaves with circular order 0..n-1, k = 0..n."""
from functools import lru_cache
from itertools import product
from networks import unrooted_trees, adjacent_pair_choices, tree_splits
from splitsys import canon


def leafmap_for(N, pairs):
    second = {(p + 1) % N: p for p in pairs}
    start = N - 1 if 0 in second else 0
    leafmap = {}
    idx = 0
    for i in range(N):
        pos = (start + i) % N
        if pos in second:
            leafmap[pos] = leafmap[second[pos]]
        else:
            leafmap[pos] = idx
            idx += 1
    return leafmap, idx


def system_of(N, t, pairs):
    leafmap, n = leafmap_for(N, pairs)
    base = tree_splits(N, t)
    full = (1 << n) - 1
    out = set()
    for choice in product((0, 1), repeat=len(pairs)):
        deleted = set()
        for c, p in zip(choice, pairs):
            deleted.add(p if c else (p + 1) % N)
        for s in base:
            m = 0
            for pos in s:
                if pos not in deleted:
                    m |= 1 << leafmap[pos]
            if m == 0 or m == full:
                continue
            out.add(canon(n, m))
    # trivial splits
    for p in range(n):
        out.add(canon(n, 1 << p))
    return frozenset(out), n


@lru_cache(maxsize=None)
def A_systems(n, kmax=None):
    if kmax is None:
        kmax = n
    out = set()
    for k in range(0, kmax + 1):
        N = n + k
        if N < 3:
            continue
        pcs = adjacent_pair_choices(N, k)
        for t in unrooted_trees(N):
            for pairs in pcs:
                s, nn = system_of(N, t, pairs)
                assert nn == n
                out.add(s)
    return frozenset(out)


def compose(n1, s1, p, n2, s2, r):
    """substitute for leaf p of system s1 (n1 points) the system s2 (n2 points) rooted at its leaf r.
    New circular order: s1's leaves 0..p-1, then s2's leaves r+1,...,r-1 (cyclically), then s1's p+1..n1-1.
    Returns (n, frozenset of canonical masks)."""
    n = n1 + n2 - 2
    full = (1 << n) - 1
    def new1(q):          # new index of leaf q != p of system 1
        return q if q < p else q + n2 - 2
    def new2(q):          # new index of leaf q != r of system 2
        return p + ((q - r - 1) % n2)
    block = 0
    for q in range(n2):
        if q != r:
            block |= 1 << new2(q)
    out = set()
    for m in s1:
        mm = 0
        for q in range(n1):
            if (m >> q) & 1:
                mm |= block if q == p else (1 << new1(q))
        if mm != 0 and mm != full:
            out.add(canon(n, mm))
    rest = full ^ block
    for m in s2:
        mm = 0
        for q in range(n2):
            if (m >> q) & 1:
                mm |= rest if q == r else (1 << new2(q))
        if mm != 0 and mm != full:
            out.add(canon(n, mm))
    return n, frozenset(out)


@lru_cache(maxsize=None)
def closure_systems(n):
    """closure of the A-systems under (unrestricted) substitution, on n leaves, n >= 3"""
    out = set(A_systems(n))
    for n1 in range(3, n):
        n2 = n + 2 - n1
        if n2 < 3:
            continue
        for s1 in closure_systems(n1):
            for s2 in closure_systems(n2):
                for p in range(n1):
                    for r in range(n2):
                        nn, s = compose(n1, s1, p, n2, s2, r)
                        out.add(s)
    return frozenset(out)
