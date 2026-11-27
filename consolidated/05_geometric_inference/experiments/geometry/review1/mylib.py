"""Referee's independent helpers (written from the mathematical definitions; nothing is
imported from the authors' experiments/geometry).

Chain convention (differs on purpose from the authors' NeRF construction):
  a chain with n atoms is built by frame propagation.  F_1 = I, bond vector a (atom a -> a+1)
  is  b_a * F_a e_x,   F_a = F_{a-1} Rx(tau_a) Rz(alpha_a),
  alpha = exterior angle (= pi - bond angle) between consecutive bond vectors,
  tau = torsion.  So |x_{a+1}-x_a| = b_a and
  |x_{a+2}-x_a|^2 = b_a^2 + b_{a+1}^2 + 2 b_a b_{a+1} cos(alpha_a) are fixed.
"""
import numpy as np


def Rx(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[1.0, 0, 0], [0, c, -s], [0, s, c]])


def Rz(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def build_chain(tors, bonds, alphas):
    """tors: n-3 torsions; bonds: n-1 bond lengths; alphas: n-2 exterior angles."""
    bonds = np.asarray(bonds, float)
    n = len(bonds) + 1
    assert len(alphas) == n - 2 and len(tors) == n - 3
    X = np.zeros((n, 3))
    F = np.eye(3)
    X[1] = bonds[0] * F[:, 0]
    for a in range(1, n - 1):          # bond a goes from atom a to atom a+1
        tau = tors[a - 2] if a >= 2 else 0.0
        F = F @ Rx(tau) @ Rz(alphas[a - 1])
        X[a + 1] = X[a] + bonds[a] * F[:, 0]
    return X


def geometry(n, bond_angle_deg=None, bonds=None, alphas=None, rng=None, hetero=False):
    """Return (bonds, alphas) for a chain with n atoms."""
    if bonds is None:
        bonds = np.ones(n - 1)
    if alphas is None:
        alphas = np.full(n - 2, np.pi - np.deg2rad(bond_angle_deg))
    return np.asarray(bonds, float), np.asarray(alphas, float)


def sqdist(X):
    """Matrix of squared distances of the rows of X."""
    g = X @ X.T
    d = np.diag(g)
    return d[:, None] + d[None, :] - 2 * g


def stack(Xs, w):
    return np.concatenate([np.sqrt(wk) * X for wk, X in zip(w, Xs)], axis=1)


def e0_pairs(n, angles=True):
    P = [(i, i + 1) for i in range(n - 1)]
    if angles:
        P += [(i, i + 2) for i in range(n - 2)]
    return P


def free_pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 3, n)]


def vech_quadratic(v):
    """Row r(v) with r(v).vech(S) = v^T S v, vech = (S_ii ; S_ij i<j)."""
    m = len(v)
    iu = np.triu_indices(m, 1)
    return np.concatenate([v * v, 2 * v[iu[0]] * v[iu[1]]])


def unvech(s, m):
    S = np.zeros((m, m))
    S[np.arange(m), np.arange(m)] = s[:m]
    iu = np.triu_indices(m, 1)
    S[iu] = s[m:]
    S[(iu[1], iu[0])] = s[m:]
    return S


def conic_system(Z, pairs):
    return np.array([vech_quadratic(Z[j] - Z[i]) for (i, j) in pairs])


def nullspace(A, ncols, rtol=1e-9):
    """Orthonormal basis (rows) of the null space of A (as vech vectors) and singular values."""
    U, s, Vt = np.linalg.svd(A, full_matrices=True)
    sfull = np.concatenate([s, np.zeros(ncols - len(s))])
    rank = int((sfull > rtol * sfull[0]).sum())
    return Vt[rank:], sfull, rank


def congruent(X, Y, tol=1e-7):
    return np.abs(sqdist(X) - sqdist(Y)).max() < tol


def procrustes_dist(X, Y):
    """d_P(X,Y) = min over isometries (reflections included) of ||X - gY||_F."""
    Xc = X - X.mean(0)
    Yc = Y - Y.mean(0)
    s = np.linalg.svd(Xc.T @ Yc, compute_uv=False)
    v = (Xc ** 2).sum() + (Yc ** 2).sum() - 2 * s.sum()
    return np.sqrt(max(v, 0.0))
