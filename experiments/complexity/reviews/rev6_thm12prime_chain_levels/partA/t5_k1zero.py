# t5_k1zero.py -- REVIEW 6: nested blobs with k_1 = 0 (no position between the two hybrid nodes) and MANY middle
# b-positions.  Corollary C of NANUQ_HIGHER_LEVELS.md says "a blob with two hybrid nodes has Sigma(B) in K iff it is
# galled, or nested with at most one middle position"; Corollary 14(i) of the main note has the qualifier k_1 >= 1.
# Check: for N[kB, 0, k2] with clades of sizes 1..4 at the positions, every split weight is >= 0 and positive exactly
# on the displayed splits (so these blobs behave like members of K although they have several middle positions),
# and no six-leaf restriction of the bloblet has the forbidden pattern.
import random, itertools
import numpy as np
from rn import Net, alphas
from gen_l2 import Builder

rng = random.Random(9)
tested = 0
for kB in range(3, 7):
    for k2 in range(0, 3):
        positions = [("b", j) for j in range(1, kB + 1)] + [("c", e) for e in range(1, k2 + 1)] + [("y", 0)]
        # (1) the bloblet: pattern-free on all six-subsets
        B = Builder(rng)
        top, order = B.nested(kB, 0, k2, ("A",), len(positions), 0, sizes={p: 1 for p in positions})
        N = Net(B.net)
        n = N.n
        disp = N.displayed_splits(order)
        idx = {x: i for i, x in enumerate(order)}
        pat = 0
        for Y in itertools.combinations(range(n), 6):
            Yset = set(Y)
            restr = set()
            for sp in disp:
                A = next(iter(sp))
                a = frozenset(Y.index(idx[x]) for x in A if idx[x] in Yset)
                if 2 <= len(a) <= 4:
                    restr.add(min(tuple(sorted(a)), tuple(sorted(set(range(6)) - a))))
            three = {(0, 1, 2), (1, 2, 3), (0, 1, 5)}       # the three 3-splits {012|345}, {123|450}, {234|501} normalised
            three = {min(tuple(sorted(s)), tuple(sorted(set(range(6)) - set(s)))) for s in [(0, 1, 2), (1, 2, 3), (2, 3, 4)]}
            two = {min(tuple(sorted(s)), tuple(sorted(set(range(6)) - set(s)))) for s in [(i, (i + 1) % 6) for i in range(6)]}
            if three <= restr and not two <= restr:
                pat += 1
        assert pat == 0, (kB, k2, pat)
        # (2) clades at the positions
        for rep in range(6):
            B = Builder(rng)
            sizes = {p: rng.choice([1, 1, 2, 3, 4]) for p in positions}
            if sum(sizes.values()) > 15:
                continue
            top, order = B.nested(kB, 0, k2, ("A",), sum(sizes.values()), 0, sizes=sizes, kinds=["tree"])
            N = Net(B.net)
            D6 = N.nanuq6(order)
            al = alphas(D6, list(range(N.n)))
            disp = N.displayed_splits(order)
            full = frozenset(order)
            for (i, j), v in al.items():
                U = frozenset(order[q] for q in range(i + 1, j + 1))
                isd = frozenset((U, full - U)) in disp
                assert v >= 0 and ((v > 0) == isd), ("violation", kB, k2, sizes)
            tested += 1
print(f"N[kB,0,k2], kB = 3..6, k2 = 0..2: no six-leaf restriction of the bloblet has the pattern; with clades of sizes 1..4 "
      f"({tested} networks, up to 15 leaves) all split weights are >= 0 and positive exactly on the displayed splits")
