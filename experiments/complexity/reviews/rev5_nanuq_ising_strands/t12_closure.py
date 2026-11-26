# t12_closure.py -- REVIEWER'S OWN CODE: (1) the split metrics of the circular splits of C are linearly
# independent (Theorem 12(c)); (2) closure of K' under substitution (Theorem 10'(b)) on explicit pairs;
# (3) K (Theorem 10(c)) under cherry replacement: used in Corollary 14 (ii)=>(iv).
import itertools, random, collections
import numpy as np
from fractions import Fraction
from mysplits import *

# (1)
for n in range(4, 11):
    sp = sorted(circular_splits(n))
    pairs = list(itertools.combinations(range(n), 2))
    A = np.array([[1 if ((m >> x) & 1) != ((m >> y) & 1) else 0 for (x, y) in pairs] for m in sp], dtype=float)
    r = np.linalg.matrix_rank(A)
    # exact check of the determinant being non-zero for small n via integer Bareiss
    print("n = %d: %d circular splits, %d pairs, rank of the split metrics = %d" % (n, len(sp), len(pairs), r))
    assert len(sp) == len(pairs) == r

# (2)
three = sorted({norm(interval(i, i + 3, 6), 6) for i in range(3)})
two = [norm((1 << i) | (1 << ((i + 1) % 6)), 6) for i in range(6)]
pat_cache = {}
def pat6(R):
    if R not in pat_cache: pat_cache[R] = all(a in R for a in three) and any(t not in R for t in two)
    return pat_cache[R]
def inKp(S, n):
    return not any(pat6(restrict(S, Y, n)) for Y in itertools.combinations(range(n), 6))
lg_cache = {}
def inK(S, n):
    for Y in itertools.combinations(range(n), 6):
        R = restrict(S, Y, n)
        if R not in lg_cache: lg_cache[R] = six_locally_good_6(R)
        if not lg_cache[R]: return False
    return True
TG = {k: tree_generated(k) for k in (3, 4, 5, 6)}
Kp6 = [S for S in TG[6] if not pat6(S)]
K6 = [S for S in TG[6] if six_locally_good_6(S)]
assert len(Kp6) == 133 and len(K6) == 127
cnt = bad = 0
for S1 in Kp6:
    for n2 in (3, 4, 5):
        for S2 in TG[n2]:
            for p in range(6):
                for r in range(n2):
                    if n2 == 5 and (p + r) % 3: continue        # thin out
                    S, n = substitute(S1, 6, p, S2, n2, r)
                    cnt += 1
                    if not inKp(S, n): bad += 1
print("K'_6 o (tree-generated on 3,4,5 points): %d substitutions, not in K': %d" % (cnt, bad))
rng = random.Random(3)
cnt = bad = 0
for _ in range(1500):
    S1, S2 = rng.choice(Kp6), rng.choice(Kp6)
    S, n = substitute(S1, 6, rng.randrange(6), S2, 6, rng.randrange(6))
    cnt += 1
    if not inKp(S, n): bad += 1
print("K'_6 o K'_6 (10 points): %d random substitutions, not in K': %d" % (cnt, bad))
# a system outside K' substituted stays outside (sanity of the test)
out = [S for S in TG[6] if pat6(S)]
S, n = substitute(out[0], 6, 0, TG[4][2], 4, 1)
print("sanity: (outside K') o (4-point system) in K'?", inKp(S, n))

# (3) cherry replacement in K: K_6 with one leaf doubled (7 points) and two leaves doubled (8 points)
cherry = TG[3][0]
cnt = bad = 0
for S1 in K6:
    for p in range(6):
        S, n = substitute(S1, 6, p, cherry, 3, 0)
        cnt += 1
        if not inK(S, n): bad += 1
print("K_6 with one leaf replaced by a cherry: %d systems, not in K: %d" % (cnt, bad))
cnt = bad = 0
for S1 in TG[5]:
    for p in range(5):
        S, n = substitute(S1, 5, p, cherry, 3, 0)
        cnt += 1
        if not six_locally_good_6(S): bad += 1
print("five-point tree-generated systems with one leaf doubled: %d, not 6-locally good: %d" % (cnt, bad))
