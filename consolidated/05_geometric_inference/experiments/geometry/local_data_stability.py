"""Cycle 2, exploration: stability of chain reconstruction from sequence-local distances.

F_K = all pairs with sequence separation <= K.  R = normalised rigidity matrix (rows: unit
edge directions).  Its singular values s_1 <= s_2 <= ...: six vanish (rigid motions) when the
chain spans space; the stability constant of the infinitesimal reconstruction is C = 1/s_7.

Printed: s_7 for helices and random coils against n, the fitted exponent, and three upper
bounds on s_7:
 (a) translational modes (any configuration):  s_7^2 <= (5 pi^2/3) K(K+1)(2K+1) / n^2;
 (b) one torsion move (hinge): s_7^2 <= energy / |v_perp|^2 with the torsional velocity field
     of the central torsion (v_perp: component orthogonal to rigid motions);
 (c) coherent bending: the same with all torsional fields, signs chosen by a power iteration
     on the Gram matrix of the fields (the softest combination).
"""
import sys
import numpy as np
from geomlib import chain


def rigidity(X, K):
    n = len(X)
    rows = []
    for i in range(n):
        for j in range(i + 1, min(n, i + K + 1)):
            d = X[i] - X[j]
            d = d / np.linalg.norm(d)
            r = np.zeros(3 * n)
            r[3 * i:3 * i + 3] = d
            r[3 * j:3 * j + 3] = -d
            rows.append(r)
    return np.array(rows)


def rigid_basis(X):
    n = len(X)
    B = [np.tile(e, (n, 1)).flatten() for e in np.eye(3)] + [np.cross(e, X - X.mean(0)).flatten() for e in np.eye(3)]
    Q, _ = np.linalg.qr(np.array(B).T)
    return Q


def torsion_fields(X):
    n = len(X)
    T = []
    for m in range(n - 3):
        ax = X[m + 2] - X[m + 1]
        ax = ax / np.linalg.norm(ax)
        V = np.zeros((n, 3))
        V[m + 3:] = np.cross(ax, X[m + 3:] - X[m + 2])
        T.append(V.flatten())
    return np.array(T).T                     # 3n x (n-3)


def analyse(X, K):
    n = len(X)
    R = rigidity(X, K)
    s = np.linalg.svd(R, compute_uv=False)
    s = np.sort(s)
    # R has more rows than columns for K >= 4; singular values are of R (3n columns)
    s7 = s[6] if len(s) > 6 else 0.0
    bound_a = np.sqrt(5 * np.pi ** 2 / 3 * K * (K + 1) * (2 * K + 1)) / n
    Q = rigid_basis(X)
    T = torsion_fields(X)
    Tp = T - Q @ (Q.T @ T)
    c = (n - 3) // 2
    v = Tp[:, c]
    bound_b = np.linalg.norm(R @ T[:, c]) / np.linalg.norm(v)
    # softest combination of torsional fields: generalised eigenproblem  (R T)^T (R T) c = lam Tp^T Tp c
    A = (R @ T).T @ (R @ T)
    G = Tp.T @ Tp
    w = np.linalg.eigvalsh(np.linalg.solve(G + 1e-12 * np.trace(G) * np.eye(len(G)), A))
    bound_c = np.sqrt(max(w.real.min(), 0))
    return s7, bound_a, bound_b, bound_c


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    for K in (4, 6):
        for name, tors_fn in (("helix 60deg", lambda n: np.full(n - 3, np.deg2rad(60.0))),
                              ("helix 150deg", lambda n: np.full(n - 3, np.deg2rad(150.0))),
                              ("random coil", lambda n: rng.uniform(-np.pi, np.pi, n - 3))):
            print(f"K = {K}, {name}")
            ns, s7s = [], []
            for n in (20, 40, 80, 160):
                X = chain(n, tors_fn(n))
                s7, ba, bb, bc = analyse(X, K)
                rg = np.sqrt(((X - X.mean(0)) ** 2).sum() / n)
                ns.append(n); s7s.append(s7)
                print(f"   n={n:4d} Rg={rg:7.2f}  s7={s7:.3e}  C=1/s7={1/s7:10.1f}   bounds: (a) {ba:.3e}  (b) one torsion {bb:.3e}  (c) torsion space {bc:.3e}")
            slope = np.polyfit(np.log(ns[1:]), np.log(s7s[1:]), 1)[0]
            print(f"   fitted exponent of s7 in n: {slope:.2f}")
