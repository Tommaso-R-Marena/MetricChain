#!/usr/bin/env python3
"""R22 prior art, a check of the dictionary used in finding F3: for d = 1 and unit-diagonal ("star") constraints the
states are sign vectors c_k in {+-1}^n, the stacked rows are z_i = (sqrt(w_k) c_k(i))_k, the constrained edge vectors
are the z_i themselves (centre at 0), and
     dim N(z) = r(r+1)/2 - rank Z,   Z = [1 | c_i o c_j (i<j)]   (Tropp 2018, Fact 3.1 = Laurent-Poljak 1996, Thm 4.2),
so that (CC) [dim N = r - 1]  <=>  Z has full column rank 1 + r(r-1)/2.
Run: python3 -B t6_d1_dictionary.py > t6_d1_dictionary.log
"""
import itertools
import numpy as np
rng = np.random.default_rng(2340); viol = 0
print("| r | n | rank Z | 1 + r(r-1)/2 | dim N(z) from the conic system | r(r+1)/2 - rank Z | (CC) | Z full column rank |")
print("|---|---|---|---|---|---|---|---|")
for r, n in ((2, 2), (2, 3), (3, 4), (3, 6), (4, 7), (4, 12), (5, 11), (5, 30), (6, 16), (6, 60)):
    for rep in range(2):
        C = rng.choice([-1.0, 1.0], size=(n, r)); w = rng.dirichlet(np.ones(r) * 3)
        z = C * np.sqrt(w)[None, :]
        idx = [(a, b) for a in range(r) for b in range(a, r)]
        R = np.array([[zi[a] * zi[b] * (1 if a == b else 2) for a, b in idx] for zi in z])
        s = np.linalg.svd(R, compute_uv=False); dimN = len(idx) - int((s > 1e-10 * s[0]).sum())
        Z = np.column_stack([np.ones(n)] + [C[:, i] * C[:, j] for i, j in itertools.combinations(range(r), 2)])
        rz = np.linalg.matrix_rank(Z)
        ok = dimN == len(idx) - rz and ((dimN == r - 1) == (rz == 1 + r * (r - 1) // 2))
        viol += int(not ok)
        print(f"| {r} | {n} | {rz} | {1 + r * (r - 1) // 2} | {dimN} | {len(idx) - rz} | {dimN == r - 1} | {rz == 1 + r * (r - 1) // 2} |" + ("" if ok else "  <-- mismatch"))
print(f"violations: {viol}")
print("ALL DONE")
