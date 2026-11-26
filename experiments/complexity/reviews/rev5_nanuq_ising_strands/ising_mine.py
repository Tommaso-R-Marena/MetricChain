# ising_mine.py -- REVIEWER'S OWN CODE for ISING_GROUND_SETS.md (Cor. 5a, Prop. 12, 13, 13', Thm 14).
# Nothing is imported from the repository under review.
import itertools, random, sys, math, collections
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog


def rref(rows):
    """exact reduced row echelon form of a list of integer/Fraction rows; returns (R, pivots)"""
    A = [[Fraction(x) for x in r] for r in rows]
    piv = []
    r = 0
    ncol = len(A[0]) if A else 0
    for c in range(ncol):
        p = None
        for i in range(r, len(A)):
            if A[i][c] != 0:
                p = i; break
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == len(A):
            break
    return A[:r], piv


def sign_vectors_in_span(states):
    """all sign vectors of the row space L, up to global sign (first non-determined entry +), exact.
    Method: L is determined by its entries at the pivot columns of the RREF."""
    R, piv = rref(states)
    n = len(states[0])
    out = set()
    for signs in itertools.product((1, -1), repeat=len(piv)):
        v = [sum(s * R[i][c] for i, s in enumerate(signs)) for c in range(n)]
        if all(x == 1 or x == -1 for x in v):
            v = tuple(int(x) for x in v)
            if v[0] < 0:
                v = tuple(-x for x in v)
            out.add(v)
    return out


def sign_vectors_in_span_bruteforce(states):
    """independent brute force: test every sign vector for membership by a rank computation"""
    R, piv = rref(states)
    n = len(states[0])
    r = len(piv)
    out = set()
    for tail in itertools.product((1, -1), repeat=n - 1):
        y = (1,) + tail
        # y in L iff y = sum_i y[piv_i] R_i
        ok = True
        for c in range(n):
            if sum(y[p] * R[i][c] for i, p in enumerate(piv)) != y[c]:
                ok = False; break
        if ok:
            out.add(y)
    return out


def canon(v):
    v = tuple(int(x) for x in v)
    return v if v[0] > 0 else tuple(-x for x in v)


def projector(states):
    """exact orthogonal projector onto the row space"""
    R, piv = rref(states)
    r = len(R); n = len(R[0])
    # G = R R^T, Pi = R^T G^{-1} R
    G = [[sum(a * b for a, b in zip(R[i], R[j])) for j in range(r)] for i in range(r)]
    # invert G exactly
    aug = [G[i] + [Fraction(int(i == j)) for j in range(r)] for i in range(r)]
    RR, pv = rref(aug)
    Ginv = [row[r:] for row in RR]
    Pi = [[sum(R[a][i] * Ginv[a][b] * R[b][j] for a in range(r) for b in range(r)) for j in range(n)] for i in range(n)]
    return Pi


def pair_matrix(states_all, n):
    """rows P(x) = (x_i x_j)_{i<j}"""
    idx = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return np.array([[x[i] * x[j] for (i, j) in idx] for x in states_all], dtype=float), idx


def exposed_lp(V, others, n):
    """max t s.t. <J,P(x)> - E0 = 0 (x in V), <J,P(y)> - E0 >= t (y in others), |J_ij| <= 1.
    returns the optimal margin t (exposed w.r.t. `others` iff t > 0)"""
    PV, idx = pair_matrix(V, n)
    if not others:
        return 1.0
    PO, _ = pair_matrix(others, n)
    d = len(idx)
    # variables: J (d), E0, t
    c = np.zeros(d + 2); c[-1] = -1
    Aeq = np.hstack([PV, -np.ones((len(V), 1)), np.zeros((len(V), 1))])
    beq = np.zeros(len(V))
    Aub = np.hstack([-PO, np.ones((len(others), 1)), np.ones((len(others), 1))])
    bub = np.zeros(len(others))
    bounds = [(-1, 1)] * d + [(None, None), (0, 1)]
    res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=bounds, method='highs')
    assert res.status == 0, res.message
    return -res.fun


def all_states(n):
    return [(1,) + t for t in itertools.product((1, -1), repeat=n - 1)]
