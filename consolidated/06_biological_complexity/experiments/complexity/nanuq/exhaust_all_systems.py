"""Exhaustive test: for every circular split system Sigma on n points that contains all trivial
splits and displays at least one quartet on every 4-set, is the NANUQ metric d_Sigma Kalmanson
(alpha_ij >= 0) with support exactly Sigma?"""
import sys
from itertools import combinations
from splitsys import *

def run(n, maxshow=5):
    allsp = all_circular_splits(n)
    triv = [m for m in allsp if is_trivial(n, m)]
    nontriv = [m for m in allsp if not is_trivial(n, m)]
    counts = {"invalid": 0, "ok": 0, "neg": 0, "support": 0}
    examples = {"neg": [], "support": []}
    for r in range(len(nontriv) + 1):
        for sub in combinations(nontriv, r):
            sigma = set(triv) | set(sub)
            st, det = check(n, sigma)
            counts[st] += 1
            if st in examples and len(examples[st]) < maxshow:
                examples[st].append(([allsp[m] for m in sub], det))
    print("n =", n, counts)
    for st in examples:
        for ex in examples[st]:
            print("  ", st, "nontrivial splits (gap pairs):", ex[0], "->", ex[1])

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        run(n)
