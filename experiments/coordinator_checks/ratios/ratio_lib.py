"""Robust range of a ratio of macrostate weights over a Lipschitz class (SCI-REQ-0001, Q1): exploration.

X finite, w = e^{-f} > 0, d an envelope (quasi-metric: d(x,x) = 0, triangle inequality, not necessarily symmetric),
admissible residuals g(x) - g(y) <= d(x,y), t = e^{-g}.  For disjoint non-empty A, B:
    R+(A,B) = sup_g Z_g(A)/Z_g(B),  Z_g(S) = sum_{x in S} w(x) t(x).
Three linear programmes:
  full      : max sum_A w t  s.t. sum_B w t = 1, t(y) <= e^{d(x,y)} t(x) for ALL ordered pairs x != y of X
  bipartite : the same with the constraints for x in B, y in A only (variables on A u B)
  dual      : min lam s.t. sum_{y in A} e^{d(z,y)} psi(z,y) <= lam w(z) (z in B), sum_{z in B} psi(z,y) >= w(y) (y in A), psi >= 0
"""
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def closure(D):
    """Shortest-path closure (triangle inequality)."""
    D = D.copy()
    n = len(D)
    for k in range(n):
        D = np.minimum(D, D[:, [k]] + D[[k], :])
    np.fill_diagonal(D, 0.0)
    return D


def lp_full(w, D, A, B):
    n = len(w)
    rows, cols, vals = [], [], []
    r = 0
    for x in range(n):
        for y in range(n):
            if x != y:
                rows += [r, r]; cols += [y, x]; vals += [1.0, -np.exp(D[x, y])]; r += 1
    Aub = coo_matrix((vals, (rows, cols)), shape=(r, n)).tocsr()
    c = np.zeros(n); c[A] = -w[A]
    Aeq = np.zeros((1, n)); Aeq[0, B] = w[B]
    res = linprog(c, A_ub=Aub, b_ub=np.zeros(r), A_eq=Aeq, b_eq=[1.0], bounds=[(0, None)] * n, method="highs")
    assert res.status == 0, res.message
    return -res.fun, res.x


def lp_bip(w, D, A, B):
    idx = list(B) + list(A)
    pos = {v: i for i, v in enumerate(idx)}
    m = len(idx)
    rows, cols, vals = [], [], []
    r = 0
    for z in B:
        for y in A:
            rows += [r, r]; cols += [pos[y], pos[z]]; vals += [1.0, -np.exp(D[z, y])]; r += 1
    Aub = coo_matrix((vals, (rows, cols)), shape=(r, m)).tocsr()
    c = np.zeros(m)
    for y in A: c[pos[y]] = -w[y]
    Aeq = np.zeros((1, m))
    for z in B: Aeq[0, pos[z]] = w[z]
    res = linprog(c, A_ub=Aub, b_ub=np.zeros(r), A_eq=Aeq, b_eq=[1.0], bounds=[(0, None)] * m, method="highs")
    assert res.status == 0, res.message
    t = np.full(len(w), np.nan); t[idx] = res.x
    return -res.fun, t


def lp_dual(w, D, A, B):
    """variables: psi(z,y) for z in B, y in A (row-major), then lam."""
    nb, na = len(B), len(A)
    nv = nb * na + 1
    c = np.zeros(nv); c[-1] = 1.0
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for i, z in enumerate(B):                     # sum_y e^{d(z,y)} psi(z,y) - lam w(z) <= 0
        for j, y in enumerate(A):
            rows.append(r); cols.append(i * na + j); vals.append(np.exp(D[z, y]))
        rows.append(r); cols.append(nv - 1); vals.append(-w[z]); rhs.append(0.0); r += 1
    for j, y in enumerate(A):                     # -sum_z psi(z,y) <= -w(y)
        for i, z in enumerate(B):
            rows.append(r); cols.append(i * na + j); vals.append(-1.0)
        rhs.append(-w[y]); r += 1
    Aub = coo_matrix((vals, (rows, cols)), shape=(r, nv)).tocsr()
    res = linprog(c, A_ub=Aub, b_ub=np.array(rhs), bounds=[(0, None)] * nv, method="highs")
    assert res.status == 0, res.message
    return res.fun, res.x[:-1].reshape(nb, na)


def lower_ext(g, D, A, B):
    """lowest admissible values on A given g on B: g(y) = max_z [g(z) - d(z,y)]"""
    out = g.copy()
    for y in A:
        out[y] = max(g[z] - D[z, y] for z in B)
    return out


def upper_ext(g, D, A, B):
    """highest admissible values on B given g on A: g(z) = min_y [g(y) + d(z,y)]"""
    out = g.copy()
    for z in B:
        out[z] = min(g[y] + D[z, y] for y in A)
    return out


def ratio(w, g, A, B):
    t = np.exp(-g)
    return float((w[A] * t[A]).sum() / (w[B] * t[B]).sum())
