#!/usr/bin/env python3
"""Hand-check of one reduction used in the report (no project data, no project code):
for the band graph P_{n,K} (edges |i-j| <= K) the algebraic connectivity a(P_{n,K}) satisfies
    a(P_{n,K}) <= a(C_{n,K}) = 2K - 2 sum_{k<=K} cos(2 pi k / n) <= 2 pi^2 K(K+1)(2K+1) / (3 n^2)      (printed bound)
    a(P_{n,K}) <= a(C_{2n,K}) = sum_{k<=K} 2(1 - cos(pi k / n)) <= pi^2 K(K+1)(2K+1) / (6 n^2)          (2025 refinement)
and, for a random configuration in R^3, the 7th smallest eigenvalue of the stiffness matrix R^T R
(rows = unit edge directions) is <= a(P_{n,K})  (the inequality a_d(G) <= a(G))."""
import numpy as np
rng = np.random.default_rng(0)
def lap(n, K):
    L = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, min(n, i + K + 1)):
            L[i, i] += 1; L[j, j] += 1; L[i, j] -= 1; L[j, i] -= 1
    return L
def stiff7(n, K, X):
    rows = []
    for i in range(n):
        for j in range(i + 1, min(n, i + K + 1)):
            e = (X[i] - X[j]) / np.linalg.norm(X[i] - X[j]); r = np.zeros(3 * n)
            r[3 * i:3 * i + 3] = e; r[3 * j:3 * j + 3] = -e; rows.append(r)
    R = np.array(rows); w = np.linalg.eigvalsh(R.T @ R); return w[6]
ok = True
for n in (12, 20, 40, 80):
    for K in (3, 4, 6):
        a = np.linalg.eigvalsh(lap(n, K))[1]
        c1 = 2 * K - 2 * sum(np.cos(2 * np.pi * k / n) for k in range(1, K + 1))
        c2 = sum(2 * (1 - np.cos(np.pi * k / n)) for k in range(1, K + 1))
        b1 = 2 * np.pi ** 2 * K * (K + 1) * (2 * K + 1) / (3 * n ** 2)
        b2 = np.pi ** 2 * K * (K + 1) * (2 * K + 1) / (6 * n ** 2)
        s = max(stiff7(n, K, rng.normal(size=(n, 3))) for _ in range(3))
        good = (a <= c1 + 1e-12) and (c1 <= b1 + 1e-12) and (a <= c2 + 1e-12) and (c2 <= b2 + 1e-12) and (s <= a + 1e-9)
        ok &= good
        print(f"n={n:3d} K={K}: a(P)={a:.5f} <= a(C_n)={c1:.5f} <= {b1:.5f};  a(P) <= a(C_2n)={c2:.5f} <= {b2:.5f};  lambda_7(stiffness, random X)={s:.5f} <= a(P): {good}")
print("ALL OK" if ok else "SOME CHECK FAILED")
