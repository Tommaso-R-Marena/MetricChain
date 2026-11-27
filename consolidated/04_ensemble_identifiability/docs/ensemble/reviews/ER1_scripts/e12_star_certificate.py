#!/usr/bin/env python3
"""E12 'Reading': 'the cost of certified identification is Theta(Kn) if the pairs may be chosen adaptively'.
(b) only says that the pivot columns determine C; (c) is a lower bound for designs H admitting a certificate
supported on H.  The two meet only if the design H read by pivoted Cholesky itself admits a certificate.
By E1(a) (necessity) it must, whenever the full C identifies the ensemble.  Check by LP on small cubes."""
import itertools
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(2718)


def cube_mod_flip(n):
    X = np.array(list(itertools.product((-1, 1), repeat=n - 1)))
    return np.hstack([np.ones((X.shape[0], 1), dtype=int), X])


def pivots(C, tol=1e-9):
    n = len(C); d = np.ones(n); L = np.zeros((n, 0)); piv = []
    while d.max() > tol:
        p = int(np.argmax(d)); piv.append(p)
        new = (C[:, p] - L @ L[p]) / np.sqrt(d[p]); L = np.hstack([L, new[:, None]]); d = np.maximum(d - new ** 2, 0)
    return piv


def certificate_on(H, X, idx):
    """exists c, Q supported on H with c + sum_H Q_ij x_i x_j = 0 on idx and >= 1 elsewhere, and (1, phi_H)
    independent on idx?"""
    N = X.shape[0]
    G = np.hstack([np.ones((N, 1))] + [(X[:, i] * X[:, j])[:, None].astype(float) for (i, j) in H])
    if np.linalg.matrix_rank(G[idx], tol=1e-9) < len(idx):
        return False
    mask = np.ones(N, bool); mask[idx] = False
    res = linprog(np.zeros(G.shape[1]), A_ub=-G[mask], b_ub=-np.ones(mask.sum()), A_eq=G[idx],
                  b_eq=np.zeros(len(idx)), bounds=[(None, None)] * G.shape[1], method="highs")
    return res.status == 0


tot = good = full = 0; sizes = []
for n in (8, 9, 10):
    X = cube_mod_flip(n); N = X.shape[0]
    for _ in range(40):
        K = int(rng.integers(1, n - 2))
        S = rng.choice((-1.0, 1.0), size=(n, K))
        if np.linalg.matrix_rank(S) < K:
            continue
        P = S @ np.linalg.pinv(S)
        f = np.sum((X - X @ P) ** 2, axis=1)
        zero = set(np.nonzero(f < 1e-9)[0].tolist())
        idx = sorted(set(int(np.nonzero((X == (S[:, a] * S[0, a])).all(axis=1))[0][0]) for a in range(K)))
        if zero != set(idx) or len(idx) != K:
            continue                        # not on the event E
        w = rng.random(K) + 0.2; w /= w.sum()
        C = (S * w) @ S.T
        piv = pivots(C)
        H = sorted({(min(i, p), max(i, p)) for p in piv for i in range(n) if i != p})
        allpairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        tot += 1; good += certificate_on(H, X, idx); full += certificate_on(allpairs, X, idx)
        sizes.append((n, K, len(H), K * n - K * (K + 1) // 2, min(sum(1 for e in H if v in e) for v in range(n))))
print(f"supports on the event E: {tot}; certificate on ALL pairs exists: {full}; certificate supported on the "
      f"pairs read by pivoted Cholesky exists: {good}")
print("sample (n, K, |H|, Kn - K(K+1)/2, min degree of H):", sizes[:6])
# K = 1: a spanning tree suffices for a single conformation (fixed design)
n = 8; X = cube_mod_flip(n); x = int(rng.integers(X.shape[0]))
tree = [(i, i + 1) for i in range(n - 1)]
print("single conformation, fixed design = a path (n-1 pairs): certificate exists:", certificate_on(tree, X, [x]))
