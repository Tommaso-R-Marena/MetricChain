"""Comparison script (run AFTER both codes existed): the author's four displayed trees of N(s,t)
(nongalled_formula.family, given by formula) against the displayed trees of the referee's explicit rooted
networks (nanuq_tests.family -> switchings)."""
import sys, os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, "author_copy/nanuq")
import nongalled_formula as A
from nanuq_tests import family as my_family

bad = 0
tot = 0
for version in ("bloblet", "clade"):
    for s in range(0, 7):
        for t in range(0, 7):
            n = s + t + 4
            net, order = my_family(s, t, version)
            idx = {x: i for i, x in enumerate(order)}
            mine = set()
            for tree in net.displayed_trees():
                ms = set()
                for sp in tree:
                    a, b = tuple(sp)
                    m = sum(1 << idx[x] for x in a)
                    ms.add(A.canon(n, m))
                mine.add(frozenset(ms))
            n2, sigma, _ = A.family(s, t, version)
            assert n2 == n
            mine_union = set().union(*mine)
            theirs = set(sigma)
            mine = mine_union
            tot += 1
            if mine != theirs:
                bad += 1
                print("DIFFERENT", version, s, t, len(mine), len(theirs))
print("N(s,t), 0<=s,t<=6, both versions: %d members, displayed split systems differing from the author's formula: %d" % (tot, bad))
