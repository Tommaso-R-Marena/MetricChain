"""Theorem K (docs/geometry/LOCAL_DATA_STABILITY.md): lower bounds on the stability constant of
chain reconstruction from sequence-local distances, checked on instances.

(a) any n points in R^3, any graph with |i - j| <= K on every edge:
        s_7(R)^2 <= (5 pi^2 / 3) K (K+1) (2K+1) / n^2      (R: unit-direction rigidity matrix).
(b) torsion-distance duality (global): for a chain with bonds of length <= b and its image Y
    under one torsion move by delta,
        || d_F(X) - d_F(Y) ||_2 <= 2 sin(delta/2) b sqrt(T_K),
        T_K = sum_{s=3}^{K} sum_{t=1}^{s-2} min(t, s-1-t)^2   (~ K^4/48),
    so the global stability constant of any range-K distance data is at least
        d_P(X, Y) / (2 sin(delta/2) b sqrt(T_K)).
(c) helices: s_7 ~ c / n^2 (numerical).
"""
import sys
import numpy as np
from geomlib import chain
from torsion_sharpness import procrustes


def T(K):
    return sum(min(t, s - 1 - t) ** 2 for s in range(3, K + 1) for t in range(1, s - 1))


def rigidity_matrix(X, edges):
    n = len(X)
    R = np.zeros((len(edges), 3 * n))
    for e, (i, j) in enumerate(edges):
        d = (X[i] - X[j]) / np.linalg.norm(X[i] - X[j])
        R[e, 3 * i:3 * i + 3] = d
        R[e, 3 * j:3 * j + 3] = -d
    return R


def check_a(trials=60, seed=0):
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(trials):
        n = int(rng.integers(12, 60))
        K = int(rng.integers(1, 8))
        X = rng.normal(size=(n, 3)) * rng.uniform(0.2, 5) if rng.random() < 0.5 else chain(n, rng.uniform(-np.pi, np.pi, n - 3))
        allp = [(i, j) for i in range(n) for j in range(i + 1, min(n, i + K + 1))]
        keep = rng.random(len(allp)) < rng.uniform(0.5, 1.0)
        edges = [e for e, k in zip(allp, keep) if k] or allp
        s = np.sort(np.linalg.svd(rigidity_matrix(X, edges), compute_uv=False)) if len(edges) >= 3 * n else None
        # with fewer rows than columns pad with zeros: singular values of the 3n-column matrix
        if s is None:
            sv = np.linalg.svd(rigidity_matrix(X, edges), compute_uv=False)
            s = np.sort(np.concatenate([sv, np.zeros(3 * n - len(sv))]))
        bound = np.sqrt(5 * np.pi ** 2 / 3 * K * (K + 1) * (2 * K + 1)) / n
        worst = max(worst, s[6] / bound)
    return worst


def check_b(trials=200, seed=1):
    rng = np.random.default_rng(seed)
    worst = 0.0
    examples = []
    for _ in range(trials):
        n = int(rng.integers(10, 50))
        K = int(rng.integers(3, 9))
        tors = rng.uniform(-np.pi, np.pi, n - 3)
        X = chain(n, tors)
        m = int(rng.integers(0, n - 3))
        delta = rng.uniform(0.05, np.pi)
        t2 = tors.copy()
        t2[m] += delta
        Y = chain(n, t2)
        pairs = [(i, j) for i in range(n) for j in range(i + 1, min(n, i + K + 1))]
        dd = np.array([np.linalg.norm(X[i] - X[j]) - np.linalg.norm(Y[i] - Y[j]) for (i, j) in pairs])
        lhs = np.linalg.norm(dd)
        rhs = 2 * np.sin(delta / 2) * 1.0 * np.sqrt(T(K))
        worst = max(worst, lhs / rhs)
        examples.append(procrustes(X, Y) / max(lhs, 1e-300))
    return worst, float(np.max(examples))


def helix_exponent(K=4, deg=60.0):
    ns, s7 = [], []
    for n in (40, 80, 160):
        X = chain(n, np.full(n - 3, np.deg2rad(deg)))
        edges = [(i, j) for i in range(n) for j in range(i + 1, min(n, i + K + 1))]
        s = np.sort(np.linalg.svd(rigidity_matrix(X, edges), compute_uv=False))
        ns.append(n)
        s7.append(s[6])
    return np.polyfit(np.log(ns), np.log(s7), 1)[0], s7[-1] * ns[-1] ** 2


if __name__ == "__main__":
    print("T_K for K = 3..8:", [T(K) for K in range(3, 9)], " K^4/48:", [round(K ** 4 / 48, 1) for K in range(3, 9)])
    print("(a) max of s_7 / bound over random instances (must be <= 1):", round(check_a(), 4))
    w, ex = check_b()
    print("(b) max of ||delta d||_2 / (2 sin(delta/2) b sqrt(T_K)) over random torsion moves (must be <= 1):", round(w, 4),
          "; largest d_P / ||delta d|| seen:", round(ex, 1))
    e, c = helix_exponent()
    print(f"(c) helix (60 degrees, K = 4): exponent of s_7 in n = {e:.3f}; s_7 n^2 = {c:.2f}")
