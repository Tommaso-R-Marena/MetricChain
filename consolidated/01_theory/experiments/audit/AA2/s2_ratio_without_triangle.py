#!/usr/bin/env python3
"""AA2 audit, script S2 -- Theorem 11.105(a),(d) (robust ratio of two macrostate weights) and the
triangle inequality of the envelope.

Theorem 11.105(a): R+(A,B) = sup_g Z_g(A)/Z_g(B) over admissible g equals the value of the programme that
keeps ONLY the constraints from B to A.  The Setting assumes that the envelope d satisfies the triangle
inequality.  What if it does not (raw differential tables, DEAD_ENDS D3)?

Exact computation by a linear programme in t = e^{-g} (Charnes-Cooper normalisation sum_B w t = 1):
  full class:        t(x) <= e^{d(y,x)} t(y)  for all ordered pairs   (g(y) - g(x) <= d(y,x))
  bipartite relax.:  only the pairs (z in B, y in A).

Run:  python3 experiments/audit/AA2/s2_ratio_without_triangle.py > experiments/audit/AA2/out_s2.txt
"""
import itertools
import math
import numpy as np
from scipy.optimize import linprog


def rplus(w, d, A, B, pairs):
    """max sum_A w t / sum_B w t  s.t.  t(y) <= exp(d[z][y]) t(z) for (z, y) in pairs, t > 0."""
    N = len(w)
    c = np.zeros(N)
    for y in A:
        c[y] = -w[y]
    A_ub, b_ub = [], []
    for (z, y) in pairs:
        row = np.zeros(N)
        row[y] = 1.0
        row[z] = -math.exp(d[z][y])
        A_ub.append(row)
        b_ub.append(0.0)
    A_eq = np.zeros((1, N))
    for z in B:
        A_eq[0, z] = w[z]
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), A_eq=A_eq, b_eq=[1.0],
                  bounds=[(0, None)] * N, method="highs")
    if res.status == 3:
        return math.inf
    assert res.status == 0, res.message
    return -res.fun


def closure(d):
    d = np.array(d, dtype=float)
    N = len(d)
    for k in range(N):
        for i in range(N):
            for j in range(N):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def all_pairs(N):
    return [(z, y) for z in range(N) for y in range(N) if z != y]


print("AA2 / S2: Theorem 11.105(a) needs the triangle inequality (or the shortest-path closure)")
print()
# states a = 0 (macrostate A), b = 1 (macrostate B), c = 2 (outside); orientation: g(x) - g(y) <= d[x][y]
# the direct constraint from b to a is loose, the path b -> c -> a is tight
d = [[0.0, 10.0, 1.0],      # d(a, .)
     [10.0, 0.0, 1.0],      # d(b, .)
     [1.0, 1.0, 0.0]]       # d(c, .)
w = np.ones(3)
A, B = [0], [1]
tri_ok = all(d[i][j] <= d[i][k] + d[k][j] + 1e-12 for i in range(3) for j in range(3) for k in range(3))
full = rplus(w, d, A, B, all_pairs(3))
bip = rplus(w, d, A, B, [(z, y) for z in B for y in A])
dc = closure(d)
full_c = rplus(w, dc, A, B, all_pairs(3))
bip_c = rplus(w, dc, A, B, [(z, y) for z in B for y in A])
print("three states: A = {a}, B = {b}, c outside;  d(b,a) = d(a,b) = 10, d(b,c) = d(c,a) = d(a,c) = d(c,b) = 1")
print(f"  triangle inequality holds: {tri_ok}")
print(f"  ln R+ over the full class (all constraints)            = {math.log(full):.6f}")
print(f"  ln of the bipartite programme of Theorem 11.105(a)     = {math.log(bip):.6f}   (formula (d): d(b,a) = 10)")
print(f"  after the shortest-path closure: full = {math.log(full_c):.6f}, bipartite = {math.log(bip_c):.6f}")
print(f"  => without the triangle inequality part (a) overestimates the range by a factor e^{math.log(bip) - math.log(full):.3f};")
print("     with the closed envelope the two agree (the class is unchanged by the closure)")
print()

# random check of both directions: (i) with a closed envelope the two programmes agree; (ii) with a raw table they
# disagree in a positive fraction of instances, always in the direction bipartite >= full
rng = np.random.default_rng(20261126)
agree_closed, disagree_raw, bad_dir, trials = 0, 0, 0, 300
worst = 0.0
for _ in range(trials):
    N = int(rng.integers(4, 7))
    d = rng.uniform(0.2, 3.0, size=(N, N))
    np.fill_diagonal(d, 0.0)
    w = rng.uniform(0.2, 2.0, size=N)
    k = int(rng.integers(1, N - 1))
    perm = rng.permutation(N)
    A, B = list(perm[:k]), list(perm[k:k + int(rng.integers(1, N - k + 1))])
    pairs_b = [(z, y) for z in B for y in A]
    f_raw, b_raw = rplus(w, d, A, B, all_pairs(N)), rplus(w, d, A, B, pairs_b)
    dc = closure(d)
    f_cl, b_cl = rplus(w, dc, A, B, all_pairs(N)), rplus(w, dc, A, B, pairs_b)
    agree_closed += abs(math.log(f_cl) - math.log(b_cl)) < 1e-7
    gap = math.log(b_raw) - math.log(f_raw)
    disagree_raw += gap > 1e-7
    bad_dir += gap < -1e-7
    worst = max(worst, gap)
    assert abs(math.log(f_raw) - math.log(f_cl)) < 1e-7      # the class does not change under the closure
print(f"random instances ({trials}, 4-6 states, raw tables uniform in [0.2, 3]):")
print(f"  closed envelope: bipartite programme = full programme in {agree_closed} of {trials}")
print(f"  raw table:       bipartite programme > full programme in {disagree_raw} of {trials} (never smaller: {bad_dir} violations);"
      f" largest overestimate of ln R+: {worst:.4f}")
