#!/usr/bin/env python3
"""A necessary condition for Problem O1 at sizes where the cube cannot be enumerated.

If K conformers are exactly the ground states of an Ising energy x^T Q x (Q symmetric, zero diagonal),
then each is a local minimum under single flips, strictly so when no two of them differ in one site:
    x^a_v (Q x^a)_v < 0   for all conformers a and sites v .
This script estimates, for random conformers, the probability that such a symmetric Q exists
(a linear feasibility problem with n(n-1)/2 unknowns and K n constraints), optionally together with the
K - 1 equal-energy constraints.  It bounds the face probability of capacity_threshold.py from above.
For comparison: independent (asymmetric) couplings can stabilise 2n random patterns (Cover 1965).

Usage: python3 symmetric_stability.py [n ...]     default 10 14 20 30 40
Numerical evidence only [N].
"""
import sys, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix, csr_matrix

rng = np.random.default_rng(20261201)


def feasible(X, equal_energy):
    K, n = X.shape
    iu = np.triu_indices(n, 1); D = len(iu[0])
    pair = -np.ones((n, n), dtype=int); pair[iu] = np.arange(D); pair = np.maximum(pair, pair.T)
    A = lil_matrix((K * n, D))
    r = 0
    for a in range(K):
        for v in range(n):
            js = [j for j in range(n) if j != v]
            A[r, pair[v, js]] = X[a, v] * X[a, js]
            r += 1
    Aeq = beq = None
    if equal_energy and K > 1:
        F = (X[:, iu[0]] * X[:, iu[1]]).astype(float)
        Aeq = csr_matrix(F[1:] - F[0]); beq = np.zeros(K - 1)
    res = linprog(np.zeros(D), A_ub=csr_matrix(A), b_ub=-np.ones(K * n), A_eq=Aeq, b_eq=beq,
                  bounds=[(None, None)] * D, method="highs")
    return res.status == 0


def main():
    ns = [int(a) for a in sys.argv[1:]] or [10, 14, 20, 30, 40]
    for n in ns:
        trials = 40 if n <= 20 else (20 if n <= 30 else 12)
        print(f"n = {n} ({trials} trials per K): K/n, P(strict local stability, symmetric Q), P(... and equal energies)")
        for alpha in (0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.75, 2.0):
            K = int(round(alpha * n)); t0 = time.time(); f1 = f2 = 0
            for _ in range(trials):
                X = rng.choice((-1, 1), size=(K, n))
                a = feasible(X, False); f1 += a
                f2 += feasible(X, True) if a else 0
            print(f"   K = {K:3d}  K/n = {K / n:4.2f}   {f1 / trials:5.2f}   {f2 / trials:5.2f}   ({time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
