#!/usr/bin/env python3
"""Problem O1 (docs/ensemble/ENSEMBLE_REPORT.md §9): for which K do K random vertices of the cut polytope
CUT_n form a simplicial face?  Equivalently: when are K random conformers on {-1,1}^n (modulo the global
flip) exactly the ground states of some Ising energy sum_{i<j} Q_ij x_i x_j, with affinely independent
pair features — i.e. when is every ensemble supported on them determined by its pair correlations among
all ensembles (Theorem E1)?

Exact test by linear programming over the whole cube (2^{n-1} points modulo flip):
    find (c, Q):  c + Q.phi(x) = 0 for x in S,   c + Q.phi(y) >= 1 for y not in S.
Also reported: whether the PSD ("projector") certificate of Theorem E10 works (only sign vectors in the
span are +-S; needs K < n), to see how far general certificates reach beyond it.

Usage: python3 capacity_threshold.py [n ...]      default: 8 10 12
Numerical evidence only [N].  Output: table of face frequencies.
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261129)


def cube_mod_flip(n):
    X = np.array(list(itertools.product((-1, 1), repeat=n - 1)), dtype=np.int8)
    return np.hstack([np.ones((X.shape[0], 1), dtype=np.int8), X])


def pair_features(X):
    n = X.shape[1]
    iu = np.triu_indices(n, 1)
    return (X[:, iu[0]] * X[:, iu[1]]).astype(float)          # N x C(n,2)


def is_simplicial_face(F, idx):
    N, m = F.shape
    G = np.hstack([np.ones((N, 1)), F])                       # rows (1, phi(x))
    if np.linalg.matrix_rank(G[idx]) < len(idx):
        return False, False
    mask = np.ones(N, dtype=bool); mask[idx] = False
    res = linprog(np.zeros(m + 1), A_ub=-G[mask], b_ub=-np.ones(mask.sum()),
                  A_eq=G[idx], b_eq=np.zeros(len(idx)), bounds=[(None, None)] * (m + 1), method="highs")
    return True, res.status == 0


def psd_certificate(X, idx):
    S = X[idx].T.astype(float)
    if np.linalg.matrix_rank(S) < len(idx):
        return False
    P = S @ np.linalg.pinv(S)
    Xf = X.astype(float)
    f = np.sum((Xf - Xf @ P) ** 2, axis=1)
    zero = np.nonzero(f < 1e-9)[0]
    return set(zero.tolist()) == set(idx.tolist())


def run(n, trials):
    X = cube_mod_flip(n); F = pair_features(X); N = X.shape[0]
    m = F.shape[1]
    rows = []
    Ks = sorted(set([max(2, int(round(a * n))) for a in (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0)]))
    for K in Ks:
        if K > min(N, m + 1):
            continue
        face = psd = indep = 0
        t0 = time.time()
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            ind, fc = is_simplicial_face(F, idx)
            indep += ind; face += fc
            if K < n:
                psd += psd_certificate(X, idx)
        rows.append((K, K / n, indep / trials, face / trials, psd / trials if K < n else float("nan"),
                     time.time() - t0))
    return rows


def main():
    ns = [int(a) for a in sys.argv[1:]] or [8, 10, 12]
    for n in ns:
        trials = {8: 200, 10: 200, 12: 120, 14: 40, 16: 12}.get(n, 20)
        print(f"n = {n}: {2 ** (n - 1)} points modulo flip, {n * (n - 1) // 2} pair observables, {trials} trials per K")
        print("    K    K/n   indep.   simplicial face   PSD certificate   seconds")
        for K, a, ind, fc, ps, sec in run(n, trials):
            print(f"  {K:4d}  {a:5.2f}   {ind:5.2f}        {fc:5.2f}            {ps:5.2f}        {sec:6.1f}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
