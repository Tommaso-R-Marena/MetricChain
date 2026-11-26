"""K = 4: all 255 non-empty type sets, decided directly (full LP over all states + exact verification)."""
import itertools, sys
from fractions import Fraction
from ising_core import *

K = 4
types = [(1,) + t for t in itertools.product([1, -1], repeat=K - 1)]     # 8 types
deg = exp = nexp = 0
bad = []
rule_mismatch = 0
for mask in range(1, 1 << len(types)):
    ts = [types[i] for i in range(len(types)) if mask >> i & 1]
    V = states_from_types(ts)
    if not distinct_states(V):
        deg += 1
        continue
    res = decide(V)
    # the author's rule: not exposed iff product constant and four different types occur
    prod = set(t[0] * t[1] * t[2] * t[3] for t in ts)
    rule_not = (len(prod) == 1 and len(ts) == 4)
    if res.exposed:
        exp += 1
    else:
        nexp += 1
        bad.append(ts)
    if rule_not == res.exposed:
        rule_mismatch += 1
print("K=4: non-empty type sets:", (1 << len(types)) - 1, " degenerate:", deg, " exposed:", exp, " not exposed:", nexp)
print("mismatches with the rule of Theorem 3:", rule_mismatch)
for ts in bad:
    print("  not exposed:", ["".join("+" if v > 0 else "-" for v in t) for t in ts])

# orbits under signed permutations of the 4 states (order 2^3 * 4! = 192 on types mod sign)
def canon_t(t):
    return t if t[0] == 1 else tuple(-v for v in t)
idx = {t: i for i, t in enumerate(types)}
group = set()
for perm in itertools.permutations(range(K)):
    for sg in itertools.product([1, -1], repeat=K):
        group.add(tuple(idx[canon_t(tuple(sg[i] * t[perm[i]] for i in range(K)))] for t in types))
print("effective group order on types:", len(group))
seen = set()
orbits = 0
for mask in range(1, 1 << len(types)):
    if mask in seen:
        continue
    orbits += 1
    for g in group:
        im = 0
        for i in range(len(types)):
            if mask >> i & 1:
                im |= 1 << g[i]
        seen.add(im)
print("orbits of non-empty type sets:", orbits)
