"""Proposition 9.2 (docs/geometry/ENSEMBLE_RIGIDITY.md): labelled configurations observed after a
Haar-random proper rotation.  The third moment of the data determines the mean triple
products  tau_ijl = sum_k w_k det(x_i^k, x_j^k, x_l^k).  In the stacked space R^{3K} this is the
alternating 3-form  T = sum_k w_k^{-1/2} vol_k  evaluated on the stacked points, and the
coordinate blocks are exactly the vectors v for which the contraction i_v T has rank <= 2
(rank 4 or 6 for vectors with components in two or three blocks).  So second and third
moments together determine a generic K-mixture WITHOUT statewise constraints, while the second
moment alone never does (Proposition 3.1).

Check: build T from the triple products in an unknown orthonormal basis of the stacked space
(as the data give it), and compare the ranks of contractions with block vectors and with
generic vectors."""
import itertools
import sys
import numpy as np


def run(K=2, n=None, seed=0):
    rng = np.random.default_rng(seed)
    m = 3 * K
    n = n or m + 3
    w = rng.dirichlet(np.ones(K) * 3)
    Xs = [rng.normal(size=(n, 3)) for _ in range(K)]
    tau = {t: sum(wk * np.linalg.det(X[list(t)]) for wk, X in zip(w, Xs)) for t in itertools.combinations(range(n), 3)}
    z = np.hstack([np.sqrt(wk) * X for wk, X in zip(w, Xs)])
    Q, _ = np.linalg.qr(rng.normal(size=(m, m)))
    Z = z @ Q                                           # what the second moment gives: z up to O(3K)
    # solve for the 3-form T (coefficients on basis 3-vectors) from T(Z_i, Z_j, Z_l) = tau_ijl
    basis = list(itertools.combinations(range(m), 3))
    A = np.array([[np.linalg.det(Z[list(t)][:, list(b)]) for b in basis] for t in tau])
    coef, res, rk, sv = np.linalg.lstsq(A, np.array(list(tau.values())), rcond=None)
    fit = np.abs(A @ coef - np.array(list(tau.values()))).max()
    T = np.zeros((m, m, m))
    for c, b in zip(coef, basis):
        for perm in itertools.permutations(range(3)):
            sgn = np.linalg.det(np.eye(3)[list(perm)])
            T[b[perm[0]], b[perm[1]], b[perm[2]]] = sgn * c
    def contraction_rank(v):
        return np.linalg.matrix_rank(np.einsum("a,abc->bc", v, T), tol=1e-8)
    block_ranks = []
    for k in range(K):
        for _ in range(3):
            u = np.zeros(m)
            u[3 * k:3 * k + 3] = rng.normal(size=3)
            block_ranks.append(contraction_rank(u @ Q))       # block vector, in the unknown basis
    generic_ranks = [contraction_rank(rng.normal(size=m)) for _ in range(6)]
    two_block = []
    if K >= 2:
        u = np.zeros(m)
        u[:6] = rng.normal(size=6)
        two_block.append(contraction_rank(u @ Q))
    return dict(K=K, n=n, fit_residual=float(fit), rank_of_system=int(rk), block_ranks=block_ranks,
                two_block_ranks=two_block, generic_ranks=generic_ranks)


if __name__ == "__main__":
    for K in (2, 3):
        print(run(K))
