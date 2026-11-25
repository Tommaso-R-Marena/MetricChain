"""Q1, second half: with one site per chi angle (chi2 moves with chi1) the known part is NOT
pairwise.  Demonstration on Ace-(Ser)3-NMe (all 9 states of every residue are clash-free at 0.70,
so the full grid is the domain): the stored grid (9,9,9) is re-indexed as (3,3,3,3,3,3) with
axes (chi1_1, chi2_1, chi1_2, chi2_2, chi1_3, chi2_3) and mixed differences of orders 3, 4, 5 of
the vacuum energy f are computed for every subset of chi-sites.
usage: python3 -B an_perchi.py [BB]"""
import sys, itertools
import numpy as np
from anlib import *

bb = sys.argv[1] if len(sys.argv) > 1 else "E"
d = load_fb(f"fb_S3_{bb}_R3_t0.60")
assert d["shape"] == (9, 9, 9) and all(len(x) == 9 for x in d["dom"])
f = (d["tors"] + d["lj"] + d["coul"])
X = np.ones(f.shape, dtype=bool)
T = third_order(f, X)
print(f"Ser3 on {bb}: residue sites (9 states each): max |third-order mixed difference| of f = {max(v[0] for v in T.values()):.2e} kcal/mol (range of f {f.max()-f.min():.1f})")
f6 = f.reshape((3,) * 6); X6 = np.ones(f6.shape, dtype=bool)
res_of = [0, 0, 1, 1, 2, 2]
for order in (2, 3, 4, 5):
    by = {}
    for S in itertools.combinations(range(6), order):
        mx, _, _ = mixed(f6, X6, S)
        key = tuple(sorted([res_of[s] for s in S].count(r) for r in set(res_of[s] for s in S)))[::-1]
        by[key] = max(by.get(key, 0.0), mx)
    print(f"   chi sites (3 states each), order {order}: max |mixed difference| by pattern (number of chi's taken from each residue involved): "
          + "; ".join(f"{k}: {v:.3e}" for k, v in sorted(by.items())))
