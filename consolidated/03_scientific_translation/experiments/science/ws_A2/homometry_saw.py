#!/usr/bin/env python3
"""Workstream A2 — identifiability of lattice chain conformations from pair-distance data.

For self-avoiding walks (SAWs) with N beads on Z^2 or Z^3 we count, up to the point group of the lattice
(8 resp. 48 isometries, reflections included) and translations:

  W_N  walks (labelled conformations; reversal of the chain is NOT identified),
  S_N  distinct site sets traced by them (unlabelled point sets),
  D_N  distinct multisets of ALL squared pair distances of these site sets   (the "full distance distribution",
       the object of Boutin-Kemper / Patterson homometry),
  P_N  distinct truncated profiles: numbers of pairs at each squared distance d < S_c (two conventions: all pairs,
       or only pairs with chain separation >= 3 as in THEORY_REPORT 11.22).

D_N < S_N  <=>  there are non-congruent ("homometric") site sets of chains with the same distance distribution.
The first homometric pair found is printed.

Usage:  python3 homometry_saw.py DIM NMAX [SC [NMIN]]
"""
import sys
import itertools
from collections import defaultdict

DIM = int(sys.argv[1]) if len(sys.argv) > 1 else 2
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 12
SC = int(sys.argv[3]) if len(sys.argv) > 3 else 5
NMIN = int(sys.argv[4]) if len(sys.argv) > 4 else 4

if DIM == 2:
    STEPS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
else:
    STEPS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def point_group(dim):
    """All signed permutation matrices, as functions on tuples."""
    ops = []
    for perm in itertools.permutations(range(dim)):
        for signs in itertools.product((1, -1), repeat=dim):
            ops.append((perm, signs))
    return ops


OPS = point_group(DIM)


def apply(op, p):
    perm, signs = op
    return tuple(signs[i] * p[perm[i]] for i in range(DIM))


def canon_set(points):
    """Canonical form of an unlabelled point set under the point group and translations."""
    best = None
    for op in OPS:
        img = [apply(op, p) for p in points]
        mins = tuple(min(q[i] for q in img) for i in range(DIM))
        img = tuple(sorted(tuple(q[i] - mins[i] for i in range(DIM)) for q in img))
        if best is None or img < best:
            best = img
    return best


def canon_walk(walk):
    """Canonical form of a labelled walk (sequence) under the point group and translations (no reversal)."""
    best = None
    o = walk[0]
    for op in OPS:
        img = tuple(apply(op, tuple(p[i] - o[i] for i in range(DIM))) for p in walk)
        if best is None or img < best:
            best = img
    return best


def sqd(p, q):
    return sum((a - b) ** 2 for a, b in zip(p, q))


def enumerate_walks(n_beads):
    """All SAWs with n_beads beads starting at the origin whose first step is STEPS[0]
    (every symmetry class has such a representative; classes are identified later by canon_walk)."""
    origin = (0,) * DIM
    first = STEPS[0]
    walk = [origin, first]
    occ = {origin, first}
    out = []

    def rec():
        if len(walk) == n_beads:
            out.append(tuple(walk))
            return
        last = walk[-1]
        for s in STEPS:
            nxt = tuple(a + b for a, b in zip(last, s))
            if nxt in occ:
                continue
            walk.append(nxt)
            occ.add(nxt)
            rec()
            walk.pop()
            occ.remove(nxt)

    if n_beads == 1:
        return [(origin,)]
    rec()
    return out


def main():
    print(f"# lattice Z^{DIM}, point group of order {len(OPS)}, cutoff S_c = {SC} (squared distances < S_c)")
    print("# N  c_{N-1}/|first step|  W_N  S_N  D_N  homometric_groups  P_all  P_sep3")
    for n in range(NMIN, NMAX + 1):
        walks = enumerate_walks(n)
        walk_classes = set()
        set_to_multiset = {}
        prof_all = set()
        prof_sep = set()
        for w in walks:
            cw = canon_walk(w)
            if cw in walk_classes:
                continue
            walk_classes.add(cw)
            # truncated profiles (functions of the labelled walk)
            cnt_all = defaultdict(int)
            cnt_sep = defaultdict(int)
            for i in range(n):
                pi = w[i]
                for j in range(i + 1, n):
                    d = sqd(pi, w[j])
                    if d < SC:
                        cnt_all[d] += 1
                        if j - i >= 3:
                            cnt_sep[d] += 1
            prof_all.add(tuple(sorted(cnt_all.items())))
            prof_sep.add(tuple(sorted(cnt_sep.items())))
            cs = canon_set(w)
            if cs not in set_to_multiset:
                ms = defaultdict(int)
                for i in range(n):
                    for j in range(i + 1, n):
                        ms[sqd(cs[i], cs[j])] += 1
                set_to_multiset[cs] = tuple(sorted(ms.items()))
        groups = defaultdict(list)
        for cs, ms in set_to_multiset.items():
            groups[ms].append(cs)
        homo = [g for g in groups.values() if len(g) > 1]
        print(n, len(walks), len(walk_classes), len(set_to_multiset), len(groups), len(homo),
              len(prof_all), len(prof_sep), flush=True)
        if homo:
            g = min(homo, key=lambda g: g)
            print(f"#   example of non-congruent site sets with equal distance multisets (N={n}):")
            for cs in g[:3]:
                print("#     ", cs)
            sizes = sorted((len(g) for g in homo), reverse=True)
            print(f"#   sizes of the largest homometric groups: {sizes[:10]}; site sets in groups: {sum(sizes)}")


if __name__ == "__main__":
    main()
