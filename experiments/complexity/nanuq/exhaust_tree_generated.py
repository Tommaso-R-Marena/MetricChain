"""Exhaustive test restricted to 'tree-generated' circular split systems:
Sigma = union of the split systems of binary trees compatible with the circular order
(equivalently: every split of Sigma lies in a compatible subfamily of Sigma with n-3 nontrivial splits)."""
import sys
from itertools import combinations
from splitsys import *

def compatible(n, m1, m2):
    full = (1 << n) - 1
    a, b = m1, m2
    return (a & b) == 0 or (a & ~b & full) == 0 or (~a & b & full) == 0 or ((~a) & (~b) & full) == 0

def tree_generated(n, sub):
    """sub: list of nontrivial canonical masks. True iff every split lies in a clique (pairwise
    compatible) of size n-3 inside sub."""
    need = n - 3
    sub = list(sub)
    if not sub:
        return False
    comp = {m: [k for k in sub if k != m and compatible(n, m, k)] for m in sub}
    def extend(clique, cands):
        if len(clique) == need:
            return True
        if len(clique) + len(cands) < need:
            return False
        for idx, c in enumerate(cands):
            if extend(clique + [c], [k for k in cands[idx + 1:] if k in comp[c]]):
                return True
        return False
    for m in sub:
        if not extend([m], comp[m]):
            return False
    return True

def run(n, maxshow=6):
    allsp = all_circular_splits(n)
    triv = [m for m in allsp if is_trivial(n, m)]
    nontriv = [m for m in allsp if not is_trivial(n, m)]
    counts = {"invalid": 0, "ok": 0, "neg": 0, "support": 0}
    examples = {"neg": [], "support": [], "invalid": []}
    ntg = 0
    for r in range(n - 3, len(nontriv) + 1):
        for sub in combinations(nontriv, r):
            if not tree_generated(n, sub):
                continue
            ntg += 1
            sigma = set(triv) | set(sub)
            st, det = check(n, sigma)
            counts[st] += 1
            if st in examples and len(examples[st]) < maxshow:
                examples[st].append(([allsp[m] for m in sub], det))
    print("n =", n, "tree-generated systems:", ntg, counts)
    for st in examples:
        for ex in examples[st]:
            print("  ", st, "nontrivial splits (gap pairs):", ex[0], "->", ex[1])

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        run(n)
