#!/usr/bin/env python3
"""Direct test of Theorem 4.2 on arbitrary finite site sets (any degrees): for random sets S check
     c3 (e3 - N) + c8 (e8 - N) + c11 e11  <=  b N + 2 M n_E      (n_E = number of occupied sites with < 2 occupied neighbours)
for the eleven rows.  Random sets: Bernoulli subsets of boxes at several densities, and unions of random walks."""
import random, itertools
from lat import *
F = [((-4, 2, -1), 2, 6), ((-3, 0, 2), 9, 3), ((-2, 1, 0), 3, 2), ((-1, 0, 0), 0, 0.5), ((-1, 1, -1), 0, 3), ((-1, 2, -1), 3, 4),
     ((0, -1, 2), 7, 1), ((3, 4, -3), 5, 6), ((4, -1, 0), 0, 5), ((6, -2, 1), 2, 6), ((6, -1, 0), 1, 6)]
rng = random.Random(5)
def counts(S):
    e = []
    for d in (3, 8, 11):
        e.append(sum(1 for p in S for v in DISP[d] if add(p, v) in S) // 2)
    nE = sum(1 for p in S if sum(1 for q in nbrs(p) if q in S) < 2)
    return len(S), e, nE
box = [p for p in itertools.product(range(0, 9), repeat=3) if is_site(p)]
ntest = 0; minslack = {}
def test(S):
    global ntest
    if not S: return
    N, e, nE = counts(S)
    for c, b, M in F:
        lhs = c[0] * (e[0] - N) + c[1] * (e[1] - N) + c[2] * e[2]
        rhs = b * N + 2 * M * nE
        assert lhs <= rhs, (c, N, e, nE)
        minslack[c] = min(minslack.get(c, 1e9), rhs - lhs)
    ntest += 1
for dens in (0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 0.97, 1.0):
    for _ in range(150):
        test({p for p in box if rng.random() < dens})
for _ in range(600):
    S = set()
    for w in range(rng.randint(1, 6)):
        p = rng.choice(box); path = [p]
        for _ in range(rng.randint(3, 60)):
            q = rng.choice(nbrs(path[-1]))
            if q in S or q in path: break
            path.append(q)
        S |= set(path)
    test(S)
print(f"{ntest} random finite site sets: all eleven inequalities of Theorem 4.2 hold; smallest slack per row:", {str(k): v for k, v in minslack.items()})
