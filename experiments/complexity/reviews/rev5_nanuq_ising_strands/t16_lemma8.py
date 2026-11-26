# t16_lemma8.py -- REVIEWER'S OWN CODE: Lemma 8 of the note (used by Theorem 7 and by Step 1 of Theorem 12):
# the class A_n of planar trees with twin leaves for n = 4, 5, 6, its closure C_6 under substitution with
# factors of at least three leaves, and "every system of C_6 is 6-locally good".
import itertools, sys, time
from functools import lru_cache
from mysplits import norm, six_locally_good_6, substitute, tree_generated, trivial_splits, globally_good

sys.setrecursionlimit(10000)

@lru_cache(None)
def triangulations(a, b):
    """all triangulations of the polygon with vertices a..b (a<b), as tuples of diagonals (i,j), the side (a,b) excluded"""
    if b - a < 2:
        return ((),)
    out = []
    for k in range(a + 1, b):
        left = triangulations(a, k); right = triangulations(k, b)
        extra = tuple(d for d in ((a, k), (k, b)) if d[1] - d[0] >= 2)
        for l in left:
            for r in right:
                out.append(extra + l + r)
    return tuple(out)

def systems_A(n):
    """all A-systems on n leaves: trees on P = n + k positions, k twin pairs"""
    res = set()
    triv = trivial_splits(n)
    for pattern in itertools.product((1, 2), repeat=n):
        P = sum(pattern)
        # positions of each leaf
        pos = []; c = 0
        for i, m in enumerate(pattern):
            pos.append(list(range(c, c + m))); c += m
        leaf_of = {}
        for i, ps in enumerate(pos):
            for p in ps: leaf_of[p] = i
        choices = list(itertools.product(*[range(m) for m in pattern]))
        for tri in triangulations(0, P - 1):
            # splits of the tree on positions 0..P-1: diagonal (i,j) <-> positions i..j-1 ; position P-1 is the side (P-1,0)
            S = set(triv)
            sides = [frozenset(range(i, j)) for (i, j) in tri]
            for ch in choices:
                kept = {pos[i][ch[i]]: i for i in range(n)}
                for side in sides:
                    m = 0
                    for p in side:
                        if p in kept: m |= 1 << kept[p]
                    if m and m != (1 << n) - 1:
                        S.add(norm(m, n))
            res.add(frozenset(S))
    return res

t0 = time.time()
A = {n: systems_A(n) for n in (3, 4, 5, 6)}
print("|A_3|, |A_4|, |A_5|, |A_6| =", [len(A[n]) for n in (3, 4, 5, 6)], " (note: 1, 3, 16, 102)   %.0fs" % (time.time() - t0))
TG = {n: set(tree_generated(n)) for n in (3, 4, 5, 6)}
print("A_n subset of tree-generated:", all(A[n] <= TG[n] for n in (3, 4, 5, 6)), "; A_4 = all, A_5 = all:", A[4] == TG[4], A[5] == TG[5])
# closure C_m (m <= 6) under substitution, all intermediate systems with at most 6 leaves, factors with >= 3 leaves
C = {n: set(A[n]) for n in (3, 4, 5, 6)}
changed = True
while changed:
    changed = False
    for n1 in (3, 4, 5):
        for n2 in (3, 4, 5):
            n = n1 + n2 - 2
            if n > 6: continue
            for S1 in list(C[n1]):
                for S2 in list(C[n2]):
                    for p in range(n1):
                        for r in range(n2):
                            S, nn = substitute(S1, n1, p, S2, n2, r)
                            if S not in C[nn]:
                                C[nn].add(S); changed = True
print("|C_4|, |C_5|, |C_6| =", [len(C[n]) for n in (4, 5, 6)], " (note: 3, 16, 108)")
print("every system of C_6 is 6-locally good:", all(six_locally_good_6(S) for S in C[6]),
      "; globally good:", all(globally_good(S, 6) for S in C[6]))
lg = [S for S in TG[6] if six_locally_good_6(S)]
print("6-locally good systems not in C_6:", len([S for S in lg if S not in C[6]]), " (note: 19)")
print("time %.0fs" % (time.time() - t0))
