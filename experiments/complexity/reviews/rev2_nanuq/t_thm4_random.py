"""Theorem 4 on random tree-generated systems with 8 and 9 points (unions of random binary circular trees):
whenever the literal hypothesis (locally NANUQ-positive) holds, is the metric Kalmanson with exact support?"""
import random
from collections import Counter
from css import *
rng = random.Random(123)
res = Counter()
for n in (8, 9):
    trees = binary_trees(n)
    for trial in range(1500):
        k = rng.choice([1, 2, 2, 3, 3, 4, 5, 6])
        # bias towards 'close' trees so that the hypothesis holds reasonably often
        base = rng.choice(trees)
        fam = [base]
        for _ in range(k - 1):
            cand = [t for t in rng.sample(trees, 40) if len(t & base) >= n - 5]
            fam.append(rng.choice(cand) if cand else rng.choice(trees))
        s = with_trivial(n, frozenset().union(*fam))
        hyp = locally_nanuq_positive(n, s)
        ok = check(n, s)[0] == "ok"
        res[(n, "hypothesis" if hyp else "no hypothesis", "ok" if ok else "FAIL")] += 1
for k, v in sorted(res.items()):
    print(k, v)
