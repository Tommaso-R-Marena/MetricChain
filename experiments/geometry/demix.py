"""Algorithm DEMIX (docs/geometry/ENSEMBLE_RIGIDITY.md, section 6).

Recover a K-state ensemble of chains from its matrix M of ensemble-averaged squared distances,
using only linear algebra: (1) classical scaling of M gives the stacked configuration Z in
R^{3K} up to an orthogonal map; (2) the quadrics through the statewise-constrained edge
directions of Z form a linear space, of dimension K-1 exactly when the conic condition (CC)
holds -- this is the certificate; (3) a generic quadric of that space has K eigenspaces of
dimension 3, the coordinate blocks of the states; (4) bond lengths give the weights.

Floating point; a demonstration on synthetic ensembles, not a certified solver.
"""
import itertools
import sys
import numpy as np
from geomlib import chain, edm, stack, sym_index, quad_row, sym_from_vec, kabsch_rmsd


def demix(M, edges, lengths, d=3, K=None, rank_tol=1e-8, null_tol=1e-6, rng=None):
    """edges: list of statewise-constrained pairs (i, j); lengths: their common lengths.
    If K is None the number of states is read off the rank of the centred matrix and the
    certificate (nullity = K - 1) is enforced: this is the exact-data mode of Proposition 6.1.
    If K is given (noisy data), the top dK eigenvectors and the bottom K - 1 singular vectors
    are used whatever the gaps; the certificate values are reported, not enforced.
    Returns dict with K, weights, states, certificate (nullity, singular values)."""
    rng = rng or np.random.default_rng(0)
    n = M.shape[0]
    J = np.eye(n) - np.ones((n, n)) / n
    G = -0.5 * J @ M @ J
    ev, V = np.linalg.eigh(G)
    order = np.argsort(ev)[::-1]
    ev, V = ev[order], V[:, order]
    enforce = K is None
    if enforce:
        r = int((ev > rank_tol * ev[0]).sum())
        if r % d:
            return dict(ok=False, reason=f"rank {r} of the centred matrix is not a multiple of {d}")
        K = r // d
    m = d * K
    Z = V[:, :m] * np.sqrt(np.maximum(ev[:m], 0.0))
    idx = sym_index(m)
    A = np.array([quad_row(Z[j] - Z[i], idx) for (i, j) in edges])
    sv = np.linalg.svd(A, compute_uv=False)
    sv_full = np.concatenate([sv, np.zeros(max(0, len(idx) - len(sv)))])
    nullity = int((sv_full <= null_tol * sv_full[0]).sum())
    cert = dict(K=K, nullity=nullity, expected=K - 1,
                smallest_nontrivial_sv=float(sv_full[len(idx) - K]) if len(idx) >= K else None,
                lambda_min=float(ev[m - 1]))
    if enforce and nullity != K - 1:
        return dict(ok=False, reason="conic condition fails: nullity %d, expected %d" % (nullity, K - 1),
                    certificate=cert)
    if K == 1:
        return dict(ok=True, K=1, weights=np.array([1.0]), states=[Z], certificate=cert)
    Vt = np.linalg.svd(A)[2]
    null = Vt[len(idx) - (K - 1):]
    T = sum(c * sym_from_vec(v, m, idx) for c, v in zip(rng.normal(size=K - 1), null))
    tv, Q = np.linalg.eigh(T)
    states, weights = [], []
    for k in range(K):
        Yk = Z @ Q[:, d * k:d * k + d]
        wk = float(np.mean([((Yk[j] - Yk[i]) ** 2).sum() / l ** 2 for (i, j), l in zip(edges, lengths)]))
        states.append(Yk / np.sqrt(wk))
        weights.append(wk)
    cert["eigen_gap"] = float(np.min(np.diff(tv[::d]))) if K > 1 else None
    return dict(ok=True, K=K, weights=np.array(weights), states=states, certificate=cert)


def chain_edges(n, b=1.0, theta=np.deg2rad(111.0)):
    c = np.sqrt(2 * b * b * (1 - np.cos(theta)))
    edges = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
    return edges, [b] * (n - 1) + [c] * (n - 2)


def match_error(Xs, w, out):
    K = len(Xs)
    best = (np.inf, np.inf)
    for perm in itertools.permutations(range(K)):
        e = max(kabsch_rmsd(Xs[k], out["states"][perm[k]]) for k in range(K))
        dw = max(abs(w[k] - out["weights"][perm[k]]) for k in range(K))
        best = min(best, (e, dw))
    return best


def demo(cases=((2, 12), (2, 16), (3, 23), (3, 30), (4, 39), (4, 48)), noises=(0.0, 1e-6, 1e-4), seed=7):
    rng = np.random.default_rng(seed)
    rows = []
    for K, n in cases:
        w = rng.dirichlet(np.ones(K) * 4)
        Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3)) for _ in range(K)]
        M = sum(wk * edm(X) for wk, X in zip(w, Xs))
        edges, lengths = chain_edges(n)
        for noise in noises:
            N = rng.normal(size=M.shape)
            N = (N + N.T) / 2
            np.fill_diagonal(N, 0)
            out = demix(M + noise * N, edges, lengths, K=None if noise == 0 else K)
            if out["ok"]:
                e, dw = match_error(Xs, w, out)
                rows.append((K, n, noise, e, dw, out["certificate"]["smallest_nontrivial_sv"]))
            else:
                rows.append((K, n, noise, None, None, out.get("reason")))
    return rows


if __name__ == "__main__":
    print(" K   n   noise     max state RMSD   max |dw|     s* (smallest non-trivial singular value)")
    for K, n, noise, e, dw, s in demo():
        if e is None:
            print(f"{K:2d} {n:3d}  {noise:7.0e}   -- {s}")
        else:
            print(f"{K:2d} {n:3d}  {noise:7.0e}   {e:12.3e}   {dw:10.3e}   {s:.3e}")
