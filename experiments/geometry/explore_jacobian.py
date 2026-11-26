"""Exploration (floating point): generic rank of the Jacobian of
   (torsions of K states, weights)  ->  mean squared distances on a pair set F.
Full column rank = generic local identifiability of the K-state ensemble from F-averaged
data (bond lengths and bond angles fixed statewise)."""
import sys
import numpy as np
from geomlib import chain

rng = np.random.default_rng(3)


def dchain(X):
    """Derivatives of atom positions w.r.t. each torsion: dX[m] is n x 3 (torsion m rotates
    atoms m+3.. about the axis through atoms m+1, m+2)."""
    n = len(X)
    out = []
    for m in range(n - 3):
        ax = X[m + 2] - X[m + 1]
        ax = ax / np.linalg.norm(ax)
        D = np.zeros((n, 3))
        for j in range(m + 3, n):
            D[j] = np.cross(ax, X[j] - X[m + 2])
        out.append(D)
    return out


def jac(K, n, pairs, seed=None):
    r = np.random.default_rng(seed) if seed is not None else rng
    w = r.dirichlet(np.ones(K) * 3)
    Xs = [chain(n, r.uniform(-np.pi, np.pi, n - 3)) for _ in range(K)]
    cols = []
    for k in range(K):
        dX = dchain(Xs[k])
        for m in range(n - 3):
            cols.append([w[k] * 2 * (Xs[k][j] - Xs[k][i]) @ (dX[m][j] - dX[m][i]) for (i, j) in pairs])
    for k in range(K - 1):
        cols.append([((Xs[k][j] - Xs[k][i]) ** 2).sum() - ((Xs[K - 1][j] - Xs[K - 1][i]) ** 2).sum()
                     for (i, j) in pairs])
    return np.array(cols).T


def rank(A, tol=1e-8):
    if A.size == 0:
        return 0
    s = np.linalg.svd(A, compute_uv=False)
    return int((s > tol * s[0]).sum())


def band_pairs(n, w):
    return [(i, j) for i in range(n) for j in range(i + 3, min(n, i + w + 1))]


if __name__ == "__main__":
    print("complete averaged data: smallest n with full column rank (local identifiability)")
    for K in range(1, 6):
        for n in range(4, 40):
            pairs = band_pairs(n, n)
            P = K * (n - 3) + K - 1
            if len(pairs) < P:
                continue
            r = rank(jac(K, n, pairs))
            if r == P:
                print(f"  K={K}: n={n}  params={P} data={len(pairs)} rank={r}   (count bound n>=2K+3 -> {2*K+3};  3K+1={3*K+1})")
                break
            else:
                print(f"     K={K} n={n} params={P} data={len(pairs)} rank={r}  (deficient)")
    print("band-limited averaged data |i-j|<=w: smallest n with full column rank, for each w")
    for K in range(1, 6):
        for w in range(K + 2, K + 6):
            found = None
            for n in range(w + 1, 60):
                pairs = band_pairs(n, w)
                P = K * (n - 3) + K - 1
                if len(pairs) < P:
                    continue
                r = rank(jac(K, n, pairs))
                if r == P:
                    found = (n, P, len(pairs))
                    break
            print(f"  K={K} w={w}: {'n=%d params=%d data=%d' % found if found else 'never (n<60)'}"
                  f"   [count: (K^2+3K+4)/2 = {(K*K+3*K+4)/2} at w=K+3]")
