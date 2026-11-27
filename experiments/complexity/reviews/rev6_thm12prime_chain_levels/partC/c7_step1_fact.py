# c7_step1_fact.py -- REVIEW 6: the finite fact behind Theorem A(a) (Step 1 of the proof of Theorem 12, level-free):
# every six-point system that is a substitution of two tree-generated systems with at least three leaves each is
# 6-locally good.  Own code: tree-generated systems on 3, 4, 5, 6 points as unions of planar trees; the definition of
# "6-locally good" (twelve dihedral labellings, Phi6 >= 0 with equality when y1 y4 | y5 y6 is not displayed) from
# section 3 of NANUQ_LOCAL_CRITERION.md.  Also recounts 150 / 127 and the number of systems with the pattern (17).
import itertools
from fractions import Fraction


def circ_splits(n):
    out = set()
    for i in range(n):
        for ln in range(2, n - 1):
            m = 0
            for t in range(ln):
                m |= 1 << ((i + t) % n)
            out.add(min(m, ((1 << n) - 1) ^ m))
    return sorted(out)


def tree_generated(n):
    full = (1 << n) - 1
    S = circ_splits(n)

    def compat(a, b):
        return any((x & y) == 0 for x in (a, full ^ a) for y in (b, full ^ b))
    trees = [frozenset(c) for c in itertools.combinations(S, n - 3) if all(compat(a, b) for a, b in itertools.combinations(c, 2))]
    systems = set()
    for r in range(1, len(trees) + 1):
        if n == 6 and r > 14:
            break
        for comb in itertools.combinations(trees, r):
            systems.add(frozenset().union(*comb))
    return trees, systems


def displayed(S, n, A, B):
    full = (1 << n) - 1
    for m in S:
        for side in (m, full ^ m):
            if side & A == A and side & B == 0:
                return True
    return False


def w(S, a, b, c, d):
    """weight of ab|cd for a,b,c,d in circular order: 1, 1/2, 0"""
    x = displayed(S, 6, (1 << a) | (1 << b), (1 << c) | (1 << d))
    y = displayed(S, 6, (1 << a) | (1 << d), (1 << b) | (1 << c))
    assert x or y
    return Fraction(1) if (x and not y) else Fraction(1, 2) if (x and y) else Fraction(0)


def locally_good(S):
    for r in range(6):
        for refl in (0, 1):
            y = [((-q) % 6 if refl else q) for q in range(6)]
            y = [(v + r) % 6 for v in y]
            u1, z, ww, up, v1, vq = y
            # orientation: w() needs its four arguments in circular order (either direction works for a pairing)
            phi = w(S, z, ww, v1, vq) + w(S, z, ww, up, u1) - w(S, z, ww, up, vq) - w(S, z, ww, v1, u1)
            disp = displayed(S, 6, (1 << u1) | (1 << up), (1 << v1) | (1 << vq))
            if phi < 0 or (not disp and phi != 0):
                return False
    return True


trees6, sys6 = tree_generated(6)
good = {S for S in sys6 if locally_good(S)}
three = [m for m in circ_splits(6) if bin(m).count("1") == 3]
two = [m for m in circ_splits(6) if bin(m).count("1") in (2, 4)]
pattern = {S for S in sys6 if all(t in S for t in three) and not all(t in S for t in two)}
print(f"six points: {len(trees6)} planar trees, {len(sys6)} tree-generated systems, {len(good)} six-locally good, "
      f"{len(pattern)} with the pattern (three 3-splits, a 2-split missing); pattern systems that are locally good: {len(pattern & good)}")

# substitutions: an interval A of size a (2 <= a <= 4) of the six points plays the role of X2 minus r
quad = 0
subs = set()
for a in (2, 3, 4):
    n1, n2 = 6 - a + 1, a + 1
    _, S1s = tree_generated(n1) if n1 >= 4 else (None, {frozenset()})
    _, S2s = tree_generated(n2) if n2 >= 4 else (None, {frozenset()})
    for start in range(6):
        A = [(start + t) % 6 for t in range(a)]
        rest = [(start + a + t) % 6 for t in range(6 - a)]
        # X1 in circular order: p, rest...   (p stands for A);   X2 in circular order: A..., r
        X1 = ["p"] + rest
        X2 = A + ["r"]
        for S1 in S1s:
            for S2 in S2s:
                quad += 1
                out = set()
                for m in S1:
                    side = [X1[i] for i in range(n1) if (m >> i) & 1]
                    mm = 0
                    for x in side:
                        for q in (A if x == "p" else [x]):
                            mm |= 1 << q
                    out.add(min(mm, 63 ^ mm))
                for m in S2:
                    side = [X2[i] for i in range(n2) if (m >> i) & 1]
                    mm = 0
                    for x in side:
                        for q in (rest if x == "r" else [x]):
                            mm |= 1 << q
                    out.add(min(mm, 63 ^ mm))
                mA = sum(1 << q for q in A)
                out.add(min(mA, 63 ^ mA))           # the split A | rest itself (trivial in both factors, non-trivial here)
                subs.add(frozenset(out))
print(f"substitutions of two tree-generated systems with >= 3 leaves each: {quad} placements (factor pairs x positions), "
      f"{len(subs)} distinct six-point systems; all tree-generated: {subs <= sys6}; all six-locally good: {subs <= good}")
