"""Shared functions for the local criterion: dihedral images, the local termwise conditions on 6 points,
clade blow-ups, and the list of tree-generated circular split systems."""
from itertools import combinations
from splitsys import *
from local_terms import phi5, phi6, displayed, weight2


def rotate(n, mask, r):
    full = (1 << n) - 1
    return ((mask << r) | (mask >> (n - r))) & full if r else mask


def reflect(n, mask):
    out = 0
    for p in range(n):
        if (mask >> p) & 1:
            out |= 1 << ((-p) % n)
    return out


def dihedral_images(n, sigma):
    out = set()
    for r in range(n):
        s1 = frozenset(canon(n, rotate(n, m, r)) for m in sigma)
        out.add(s1)
        out.add(frozenset(canon(n, reflect(n, m)) for m in s1))
    return out


def psi2(sigma, n, a, u, b, z, w):
    """2 * Psi(a;u;b;z,w) = 2 - 2w(au|zw) - 2w(ub|zw) + 2w(ab|zw)"""
    return 2 - weight2(sigma, n, a, u, z, w) - weight2(sigma, n, u, b, z, w) + weight2(sigma, n, a, b, z, w)


def local_ok(n, sigma):
    """All termwise conditions of the local criterion for a system on n = 6 points, in every dihedral placement:
       Phi6 >= 0;  Phi6 = 0 if the split quartet is not displayed;  and on every 5-subset: Phi5 >= 0,
       Phi5 = 0 if the split quartet is not displayed, Psi >= 0.   Returns (ok, sorted list of failure kinds)."""
    assert n == 6
    reasons = set()
    for img in dihedral_images(n, sigma):
        s = set(img)
        v = phi6(s, n, 0, 1, 2, 3, 4, 5)
        if v < 0:
            reasons.add("Phi6<0")
        if not displayed(s, 0, 3, 4, 5) and v != 0:
            reasons.add("Phi6!=0 undisplayed")
        for sub in combinations(range(n), 5):
            for r in range(5):
                u1, z, up, v1, vq = [sub[(r + t) % 5] for t in range(5)]
                v5 = phi5(s, n, u1, z, up, v1, vq)
                if v5 < 0:
                    reasons.add("Phi5<0")
                if not displayed(s, u1, up, v1, vq) and v5 != 0:
                    reasons.add("Phi5!=0 undisplayed")
                if psi2(s, n, u1, z, up, v1, vq) < 0:
                    reasons.add("Psi<0")
    return (not reasons), sorted(reasons)


def compatible(n, m1, m2):
    full = (1 << n) - 1
    a, b = m1, m2
    return (a & b) == 0 or (a & ~b & full) == 0 or (~a & b & full) == 0 or ((~a) & (~b) & full) == 0


def tree_generated(n, sub):
    """sub: nontrivial canonical masks.  True iff every split lies in a pairwise compatible subfamily of sub of
    size n-3 (i.e. the system is a union of split systems of binary trees compatible with the circular order)."""
    need = n - 3
    sub = list(sub)
    if not sub:
        return False
    comp = {m: [k for k in sub if k != m and compatible(n, m, k)] for m in sub}

    def extend(size, cands):
        if size == need:
            return True
        if size + len(cands) < need:
            return False
        for idx, c in enumerate(cands):
            if extend(size + 1, [k for k in cands[idx + 1:] if k in comp[c]]):
                return True
        return False
    return all(extend(1, comp[m]) for m in sub)


def tree_generated_systems(n):
    """list of frozensets of canonical masks (trivial splits included)"""
    allsp = all_circular_splits(n)
    triv = [m for m in allsp if is_trivial(n, m)]
    nontriv = [m for m in allsp if not is_trivial(n, m)]
    out = []
    for r in range(n - 3, len(nontriv) + 1):
        for sub in combinations(nontriv, r):
            if tree_generated(n, sub):
                out.append(frozenset(set(triv) | set(sub)))
    return out


def blowup(n, sigma, mult):
    """Replace leaf p by a caterpillar clade with mult[p] leaves (mult 2 = cherry).  Returns (n', sigma')."""
    start, tot = [0] * n, 0
    for p in range(n):
        start[p] = tot
        tot += mult[p]
    n2 = tot
    full = (1 << n2) - 1
    out = set()
    for m in sigma:
        mm = 0
        for p in range(n):
            if (m >> p) & 1:
                for q in range(start[p], start[p] + mult[p]):
                    mm |= 1 << q
        if mm != 0 and mm != full:
            out.add(canon(n2, mm))
    for p in range(n):
        for size in range(2, mult[p] + 1):
            mm = 0
            for q in range(start[p], start[p] + size):
                mm |= 1 << q
            if mm != full:
                out.add(canon(n2, mm))
        for q in range(start[p], start[p] + mult[p]):
            out.add(canon(n2, 1 << q))
    return n2, out


def describe(n, sigma):
    """sorted list of the missing nontrivial splits as leaf sets (the side not containing leaf 0)"""
    allsp = all_circular_splits(n)
    miss = []
    for m in allsp:
        if not is_trivial(n, m) and m not in sigma:
            miss.append(tuple(p for p in range(n) if (m >> p) & 1))
    return sorted(miss)
