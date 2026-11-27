"""On 6 points: (i) tree-generated circular split systems, (ii) those whose NANUQ metric is Kalmanson with
exact support ("globally good"), (iii) those satisfying all local termwise conditions in every dihedral
placement ("locally good"), (iv) systems of class A and of its composition closure (= all galled
outer-labeled planar networks on 6 leaves, any level, any number of blobs).  Also: tightness (every excluded
system has a clade blow-up whose NANUQ metric fails) and closure of the locally good class under cherry
substitution."""
import sys
from collections import Counter
from itertools import product
from splitsys import *
from localcrit import *
from twin_trees import A_systems, closure_systems

def main():
    n = 6
    tg = tree_generated_systems(n)
    A, C = A_systems(n), closure_systems(n)
    good = [s for s in tg if check(n, set(s))[0] == "ok"]
    loc = {s: local_ok(n, s) for s in tg}
    locgood = [s for s in tg if loc[s][0]]
    print(f"tree-generated systems on 6 points: {len(tg)}")
    print(f"globally good (Kalmanson, exact support): {len(good)}")
    print(f"locally good (all termwise conditions):   {len(locgood)}   subset of globally good: {set(locgood) <= set(good)}")
    print(f"class A: {len(A)}   composition closure of A: {len(C)}   closure subset of locally good: {set(C) <= set(locgood)}")
    print("by number of nontrivial splits (tree-generated / locally good / closure):")
    for k in range(3, 10):
        print("   ", k, sum(1 for s in tg if len(s) - n == k), sum(1 for s in locgood if len(s) - n == k),
              sum(1 for s in C if len(s) - n == k))
    print("globally bad systems (missing splits as leaf sets):")
    for s in tg:
        if s not in set(good):
            print("    missing", describe(n, s), " local failures:", loc[s][1])
    print("locally bad but globally good systems, with a smallest failing clade blow-up:")
    for s in good:
        if loc[s][0]:
            continue
        found = None
        for mult in product((1, 2, 3), repeat=6):
            if sum(mult) > 10 or sum(mult) == 6:
                continue
            n2, s2 = blowup(6, s, mult)
            st, det = check(n2, s2)
            if st != "ok" and (found is None or sum(mult) < sum(found[0])):
                found = (mult, st)
        print("    missing", describe(n, s), " local failures:", loc[s][1], " blow-up:", found)
        assert found is not None
    # closure under cherry substitution
    ok = True
    for s in tree_generated_systems(5):
        for p in range(5):
            mult = [1] * 5
            mult[p] = 2
            n2, s2 = blowup(5, s, mult)
            ok &= local_ok(6, frozenset(s2))[0]
    print("every 5-point tree-generated system with one leaf doubled is locally good:", ok)

if __name__ == "__main__":
    main()
