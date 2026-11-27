#!/usr/bin/env python3
"""ER2 review helpers (own code; nothing imported from experiments/ensemble).

Conventions.  X is a finite set of N states, pi > 0 a reference, d an N x N envelope (d >= 0, zero diagonal,
triangle inequality, not necessarily symmetric).  The first-order class is

    P(pi, d) = { mu in simplex : mu(y) pi(x) <= exp(d(x,y)) mu(x) pi(y)  for all x != y } .

In the weights w = mu / pi the constraint (x, y) reads  w(y) - exp(d(x,y)) w(x) <= 0.
"""
import itertools, os, pathlib
import numpy as np
from scipy.optimize import linprog


def repo_root():
    """Root of the MetricChain checkout: the first parent of this file that contains experiments/ensemble,
    else the environment variable METRICCHAIN, else /home/user/MetricChain."""
    for q in pathlib.Path(__file__).resolve().parents:
        if (q / "experiments" / "ensemble").is_dir():
            return str(q)
    return os.environ.get("METRICCHAIN", "/home/user/MetricChain")


def lp(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if res.status != 0:
        raise RuntimeError(f"LP status {res.status}: {res.message}")
    return res


def shortest_path_closure(D):
    D = D.copy(); N = len(D)
    for k in range(N):
        D = np.minimum(D, D[:, [k]] + D[[k], :])
    np.fill_diagonal(D, 0.0)
    return D


def class_rows_mu(pi, d, pairs=None):
    """Rows R with R @ mu <= 0 describing the class in the variable mu (scaled by 1/pi)."""
    N = len(pi)
    if pairs is None:
        pairs = [(x, y) for x in range(N) for y in range(N) if x != y and np.isfinite(d[x, y])]
    R = np.zeros((len(pairs), N))
    for k, (x, y) in enumerate(pairs):
        R[k, y] = 1.0 / pi[y]
        R[k, x] = -np.exp(d[x, y]) / pi[x]
    return R, pairs


def is_member(mu, pi, d, tol=1e-10):
    w = mu / pi
    N = len(pi)
    for x in range(N):
        for y in range(N):
            if x != y and np.isfinite(d[x, y]) and w[y] > np.exp(d[x, y]) * w[x] * (1 + tol) + tol:
                return False
    return abs(mu.sum() - 1) < 1e-9 and mu.min() >= -1e-12


def tight_graph_components(mu, pi, d, tol=1e-9):
    """Connected components of the tight graph: edge {x,y} iff one of the two constraints is an equality
    (relative tolerance tol)."""
    N = len(pi); w = mu / pi
    parent = list(range(N))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for x in range(N):
        for y in range(N):
            if x != y and np.isfinite(d[x, y]):
                if abs(w[y] - np.exp(d[x, y]) * w[x]) <= tol * max(w[y], np.exp(d[x, y]) * w[x], 1e-300):
                    parent[find(x)] = find(y)
    return len({find(a) for a in range(N)})


def vertices_bruteforce(pi, d, pairs=None, tol=1e-9):
    """All vertices of the class polytope by brute force over (N-1)-subsets of the constraints
    (independent of Theorem E13(a)).  Returns an array of distinct vertices (rows mu)."""
    N = len(pi)
    R, pairs = class_rows_mu(pi, d, pairs)
    ones = np.ones((1, N))
    found = []
    idx = list(range(len(pairs)))
    for comb in itertools.combinations(idx, N - 1):
        M = np.vstack([R[list(comb)], ones])
        if abs(np.linalg.det(M)) < 1e-9 * np.prod(np.linalg.norm(M, axis=1)):      # relative: singular bases
            continue
        rhs = np.zeros(N); rhs[-1] = 1.0
        mu = np.linalg.solve(M, rhs)
        if mu.min() < -tol or (R @ mu).max() > tol:
            continue
        if not any(np.abs(mu - v).max() < 1e-8 for v in found):
            found.append(mu)
    return np.array(found)


def vertices_bruteforce_fast(pi, d, pairs=None, tol=1e-9, chunk=20000):
    """Same as vertices_bruteforce, vectorised (for N = 8 with 24 constraints: C(24,7) = 346104 bases)."""
    N = len(pi)
    R, pairs = class_rows_mu(pi, d, pairs)
    combs = itertools.combinations(range(len(pairs)), N - 1)
    found = {}
    rhs = np.zeros(N); rhs[-1] = 1.0
    while True:
        block = list(itertools.islice(combs, chunk))
        if not block:
            break
        B = np.array(block)
        M = np.empty((len(B), N, N))
        M[:, :N - 1, :] = R[B]
        M[:, N - 1, :] = 1.0
        det = np.linalg.det(M)
        ok = np.abs(det) > 1e-9 * np.prod(np.linalg.norm(M, axis=2), axis=1)       # relative: singular bases
        if not ok.any():
            continue
        sol = np.linalg.solve(M[ok], np.broadcast_to(rhs, (int(ok.sum()), N))[..., None])[..., 0]
        feas = (sol.min(axis=1) > -tol) & ((sol @ R.T).max(axis=1) < tol)
        for mu in sol[feas]:
            key = tuple(np.round(mu, 6))
            found.setdefault(key, mu)
    # merge keys that differ only by rounding at a boundary
    out = []
    for mu in found.values():
        if not any(np.abs(mu - v).max() < 1e-7 for v in out):
            out.append(mu)
    return np.array(out)


def product_states(sizes):
    return list(itertools.product(*[range(q) for q in sizes]))


def max_tv_minus_linear(R, mustar, lin, const, N):
    """max over {mu >= 0, sum mu = 1, R mu <= 0} of  TV(mu, mustar) - (const - lin . mu)
    computed exactly as max over subsets S of X of an LP (TV = max_S mu(S) - mustar(S)).
    Returns (value, best subset mask, argmax mu)."""
    best = (-np.inf, None, None)
    A_eq = np.ones((1, N)); b_eq = [1.0]
    b_ub = np.zeros(len(R))
    bounds = [(0, None)] * N
    for mask in range(1 << N):
        ind = np.array([(mask >> k) & 1 for k in range(N)], dtype=float)
        res = linprog(-(ind + lin), A_ub=R, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if res.status != 0:
            raise RuntimeError("LP failed")
        val = -res.fun - ind @ mustar - const
        if val > best[0]:
            best = (val, mask, res.x.copy())
    return best


def face_maxmargin(F, idx, tol=1e-6, return_margin=False):
    """Is {x_k : k in idx} a simplicial face of conv{F[k]} (rows of F = feature vectors of all states)?
    Affine independence, then  max t :  Q.F[k] = c on idx,  Q.F[y] >= c + t off idx,  |Q_j| <= 1  (float64, all states).
    Face <=> t* > 0 (decided as t* > tol)."""
    N, D = F.shape; K = len(idx)
    if np.linalg.matrix_rank(np.hstack([np.ones((K, 1)), F[idx]])) < K:
        return (False, 0.0) if return_margin else False
    mask = np.ones(N, dtype=bool); mask[idx] = False
    M = int(mask.sum())
    c = np.zeros(D + 2); c[-1] = -1.0
    res = linprog(c, A_ub=np.hstack([-F[mask], np.ones((M, 1)), np.ones((M, 1))]), b_ub=np.zeros(M),
                  A_eq=np.hstack([F[idx], -np.ones((K, 1)), np.zeros((K, 1))]), b_eq=np.zeros(K),
                  bounds=[(-1, 1)] * D + [(None, None), (None, 10.0)], method="highs")
    if res.status != 0:
        raise RuntimeError("LP failed")
    return (res.x[-1] > tol, res.x[-1]) if return_margin else res.x[-1] > tol
