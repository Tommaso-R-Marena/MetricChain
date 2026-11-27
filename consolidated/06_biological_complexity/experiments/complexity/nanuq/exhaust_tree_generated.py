"""Exhaustive test restricted to tree-generated circular split systems (unions of split systems of binary
trees compatible with the circular order): is the NANUQ metric Kalmanson with support exactly Sigma?"""
import sys
from splitsys import *
from localcrit import tree_generated_systems, describe

def run(n, maxshow=6):
    counts = {"invalid": 0, "ok": 0, "neg": 0, "support": 0}
    examples = []
    tg = tree_generated_systems(n)
    for sigma in tg:
        st, det = check(n, set(sigma))
        counts[st] += 1
        if st != "ok" and len(examples) < maxshow:
            examples.append((st, describe(n, sigma), det))
    print("n =", n, "tree-generated systems:", len(tg), counts)
    for ex in examples:
        print("   ", ex[0], "missing splits:", ex[1], "->", ex[2])

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        run(n)
