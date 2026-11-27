#!/usr/bin/env python3
"""ER4 (internal AI review) -- shared numerical tools for the torus of three angles, written from the definitions
of the report (section 4c.4, commit b654396).  Nothing here is imported or copied from experiments/ensemble/.

Conventions.
  * lift          w(phi) = (cos(phi_1/2), sin(phi_1/2)) x (cos(phi_2/2), sin(phi_2/2)) x (cos(phi_3/2), sin(phi_3/2))
  * data span V   27 products of {1, cos phi_k, sin phi_k}; a function of V is a coefficient vector c in R^27,
                  f(phi) = Fvec(phi) . c
  * products      w_a w_b are converted to coefficient vectors EXACTLY (half-angle formulas), not by a fit
  * the curve     Z = {N w = 0} for a 2 x 8 matrix N with orthonormal rows.  It is computed WITHOUT continuation:
                  for fixed phi_3 the two conditions are x^T A_j y = 0 (j = 1, 2) with 2 x 2 matrices A_j(phi_3) and
                  unit vectors x, y for the angles 1, 2; so det[A_1 y, A_2 y] = 0, a binary quadratic in y: zero or
                  two real points over every phi_3 (the curve is a double cover of the circle of phi_3).
"""
import itertools

import numpy as np

IDX27 = list(itertools.product(range(3), repeat=3))
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])
# per-angle conversion of h_a h_b (h = (cos(phi/2), sin(phi/2))) into coefficients of (1, cos phi, sin phi)
T_HALF = np.zeros((2, 2, 3))
T_HALF[0, 0] = [0.5, 0.5, 0.0]
T_HALF[0, 1] = T_HALF[1, 0] = [0.0, 0.0, 0.5]
T_HALF[1, 1] = [0.5, -0.5, 0.0]


def wrap(d):
    return (np.asarray(d) + np.pi) % (2 * np.pi) - np.pi


def hvec(p):
    return np.array([np.cos(p / 2), np.sin(p / 2)])


def dhvec(p):
    return 0.5 * np.array([-np.sin(p / 2), np.cos(p / 2)])


def ddhvec(p):
    return -0.25 * np.array([np.cos(p / 2), np.sin(p / 2)])


def lift(phi):
    return np.einsum("a,b,c->abc", hvec(phi[0]), hvec(phi[1]), hvec(phi[2])).ravel()


def dlift(phi):
    """3 x 8: derivatives of the lift"""
    h = [hvec(p) for p in phi]
    d = [dhvec(p) for p in phi]
    return np.array([
        np.einsum("a,b,c->abc", d[0], h[1], h[2]).ravel(),
        np.einsum("a,b,c->abc", h[0], d[1], h[2]).ravel(),
        np.einsum("a,b,c->abc", h[0], h[1], d[2]).ravel()])


def ddlift(phi):
    """3 x 3 x 8: second derivatives of the lift"""
    h = [hvec(p) for p in phi]
    d = [dhvec(p) for p in phi]
    dd = [ddhvec(p) for p in phi]
    out = np.zeros((3, 3, 8))
    for a in range(3):
        for b in range(3):
            fac = []
            for k in range(3):
                if k == a and k == b:
                    fac.append(dd[k])
                elif k == a or k == b:
                    fac.append(d[k])
                else:
                    fac.append(h[k])
            out[a, b] = np.einsum("a,b,c->abc", *fac).ravel()
    return out


def _trig(X):
    """X: (..., 3) -> values, first and second derivatives of (1, cos, sin) per angle: arrays (..., 3 angles, 3)"""
    X = np.asarray(X, dtype=float)
    c, s = np.cos(X), np.sin(X)
    one, zero = np.ones_like(X), np.zeros_like(X)
    v = np.stack([one, c, s], axis=-1)
    d = np.stack([zero, -s, c], axis=-1)
    dd = np.stack([zero, -c, -s], axis=-1)
    return v, d, dd


def Fmat(X):
    """X: (n, 3) -> (n, 27) matrix of the 27 trigonometric products"""
    X = np.atleast_2d(X)
    v, _, _ = _trig(X)
    return np.einsum("ni,nj,nk->nijk", v[:, 0], v[:, 1], v[:, 2]).reshape(len(X), 27)


def Fvec(phi):
    return Fmat(np.asarray(phi)[None, :])[0]


def dFmat(X):
    """X: (n, 3) -> (n, 3, 27): gradients of the 27 products"""
    X = np.atleast_2d(X)
    v, d, _ = _trig(X)
    n = len(X)
    out = np.empty((n, 3, 27))
    out[:, 0] = np.einsum("ni,nj,nk->nijk", d[:, 0], v[:, 1], v[:, 2]).reshape(n, 27)
    out[:, 1] = np.einsum("ni,nj,nk->nijk", v[:, 0], d[:, 1], v[:, 2]).reshape(n, 27)
    out[:, 2] = np.einsum("ni,nj,nk->nijk", v[:, 0], v[:, 1], d[:, 2]).reshape(n, 27)
    return out


def ddFvec(phi):
    """(3, 3, 27): Hessians of the 27 products at one point"""
    v, d, dd = _trig(np.asarray(phi, dtype=float))
    out = np.zeros((3, 3, 27))
    for a in range(3):
        for b in range(3):
            fac = []
            for k in range(3):
                if k == a and k == b:
                    fac.append(dd[k])
                elif k == a or k == b:
                    fac.append(d[k])
                else:
                    fac.append(v[k])
            out[a, b] = np.einsum("i,j,k->ijk", *fac).ravel()
    return out


def prod_coeffs(u, v):
    """coefficient vector in R^27 of the function (u . w)(v . w), exactly"""
    U = np.asarray(u).reshape(2, 2, 2)
    Vv = np.asarray(v).reshape(2, 2, 2)
    return np.einsum("abc,def,adi,bej,cfk->ijk", U, Vv, T_HALF, T_HALF, T_HALF).ravel()


def null2(P):
    """orthonormal basis (2 x 8) of the orthogonal complement of the lifts of the six states; also the singular values"""
    L = np.array([lift(p) for p in P])
    U, s, Vt = np.linalg.svd(L)
    return Vt[6:], s


def gval(N, phi):
    return N @ lift(phi)


def gjac(N, phi):
    return N @ dlift(phi).T          # 2 x 3


def tangent(N, phi):
    G = gjac(N, phi)
    t = np.cross(G[0], G[1])
    return t / np.linalg.norm(t), np.linalg.norm(t)


def I0_basis(N):
    """27 x 15 orthonormal basis of I_0 = {(l_1.w) g_1 + (l_2.w) g_2} and 27 x 12 orthonormal basis of its complement"""
    gens = []
    for j in range(2):
        for a in range(8):
            e = np.zeros(8)
            e[a] = 1.0
            gens.append(prod_coeffs(e, N[j]))
    G = np.array(gens).T                       # 27 x 16
    U, s, Vt = np.linalg.svd(G)
    return U[:, :15], U[:, 15:], s


def Rmatrix(N, P):
    """the twelve linear forms of (R): rows F(p_k) and (unit tangent at p_k) . dF(p_k)"""
    P = np.asarray(P)
    Fv = Fmat(P)
    dFv = dFmat(P)
    rows = []
    for k in range(len(P)):
        t, _ = tangent(N, P[k])
        rows.append(Fv[k])
        rows.append(t @ dFv[k])
    return np.array(rows)


# ----------------------------------------------------------------------------------- the real curve, by double cover
def _points_over(N3, phi3):
    """the (zero or two) real points of the curve over the value phi3.  N3 = N reshaped (2,2,2,2).
    Returns (disc, [phi_a, phi_b]) with the two points (or [] if disc < 0)."""
    h3 = hvec(phi3)
    A1 = N3[0] @ h3
    A2 = N3[1] @ h3
    Q = A1.T @ J2 @ A2
    Q = 0.5 * (Q + Q.T)
    disc = Q[0, 1] ** 2 - Q[0, 0] * Q[1, 1]
    if disc < 0:
        return disc, []
    r = np.sqrt(disc)
    ys = []
    if abs(Q[0, 0]) >= abs(Q[1, 1]):
        for sgn in (1.0, -1.0):
            ys.append(np.array([-Q[0, 1] + sgn * r, Q[0, 0]]))
    else:
        for sgn in (1.0, -1.0):
            ys.append(np.array([Q[1, 1], -Q[0, 1] + sgn * r]))
    pts = []
    for y in ys:
        y = y / np.linalg.norm(y)
        a1, a2 = A1 @ y, A2 @ y
        a = a1 if np.linalg.norm(a1) >= np.linalg.norm(a2) else a2
        x = J2 @ a
        x = x / np.linalg.norm(x)
        pts.append(np.array([wrap(2 * np.arctan2(x[1], x[0])), wrap(2 * np.arctan2(y[1], y[0])), wrap(phi3)]))
    return disc, pts


def project(N, phi, iters=50, tol=1e-15):
    """Newton projection onto the curve (least-norm steps)"""
    phi = np.array(phi, dtype=float)
    for _ in range(iters):
        r = gval(N, phi)
        if np.linalg.norm(r) < tol:
            break
        G = gjac(N, phi)
        phi = phi - np.linalg.lstsq(G, r, rcond=None)[0]
    return phi


def curve_components(N, M=4000):
    """All real components of Z = {N w = 0}, each as an ordered closed loop of points (array (n, 3)).
    Method: double cover over phi_3 on a grid of M values; branches matched by continuity; the two branches are
    joined where the discriminant changes sign."""
    N3 = N.reshape(2, 2, 2, 2)
    grid = -np.pi + 2 * np.pi * (np.arange(M) + 0.5) / M
    disc = np.empty(M)
    pts = [None] * M
    for i, p3 in enumerate(grid):
        disc[i], pts[i] = _points_over(N3, p3)
    real = disc >= 0
    if not real.any():
        return []
    comps = []
    if real.all():
        # two branches over the whole circle: follow them once around
        br = [[pts[0][0]], [pts[0][1]]]
        for i in range(1, M):
            a, b = pts[i]
            d_keep = np.linalg.norm(wrap(a - br[0][-1])) + np.linalg.norm(wrap(b - br[1][-1]))
            d_swap = np.linalg.norm(wrap(b - br[0][-1])) + np.linalg.norm(wrap(a - br[1][-1]))
            if d_keep <= d_swap:
                br[0].append(a)
                br[1].append(b)
            else:
                br[0].append(b)
                br[1].append(a)
        # closing: does branch 0 return to its start or to the start of branch 1?
        d_same = np.linalg.norm(wrap(br[0][-1] - br[0][0])) + np.linalg.norm(wrap(br[1][-1] - br[1][0]))
        d_cross = np.linalg.norm(wrap(br[0][-1] - br[1][0])) + np.linalg.norm(wrap(br[1][-1] - br[0][0]))
        if d_same <= d_cross:
            comps = [np.array(br[0]), np.array(br[1])]
        else:
            comps = [np.array(br[0] + br[1])]
        return comps
    # intervals of the grid on which the discriminant is non-negative (cyclically)
    start = next(i for i in range(M) if real[i] and not real[i - 1])
    i = start
    visited = 0
    while visited < M:
        if real[i % M] and not real[(i - 1) % M]:
            j = i
            br = [[pts[j % M][0]], [pts[j % M][1]]]
            while real[(j + 1) % M]:
                j += 1
                a, b = pts[j % M]
                d_keep = np.linalg.norm(wrap(a - br[0][-1])) + np.linalg.norm(wrap(b - br[1][-1]))
                d_swap = np.linalg.norm(wrap(b - br[0][-1])) + np.linalg.norm(wrap(a - br[1][-1]))
                if d_keep <= d_swap:
                    br[0].append(a)
                    br[1].append(b)
                else:
                    br[0].append(b)
                    br[1].append(a)
            # refine the two turning points (where the two branches meet) by projecting the midpoints
            first_mid = project(N, br[0][0] + 0.5 * wrap(br[1][0] - br[0][0]))
            last_mid = project(N, br[0][-1] + 0.5 * wrap(br[1][-1] - br[0][-1]))
            loop = [first_mid] + br[0] + [last_mid] + br[1][::-1]
            comps.append(np.array(loop))
            visited += (j - i + 1)
            i = j + 1
        else:
            i += 1
            visited += 1
    return comps


def refine_loop(N, loop, hmax=0.01):
    """insert projected midpoints until consecutive points of the closed loop are closer than hmax"""
    pts = [p for p in loop]
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        out.append(a)
        d = wrap(b - a)
        dist = np.linalg.norm(d)
        if dist > hmax:
            k = int(np.ceil(dist / hmax))
            for m in range(1, k):
                out.append(wrap(project(N, a + d * m / k)))
    return np.array(out)


def torus_dist(X, P):
    """X: (n,3), P: (K,3) -> (n,) distance to the nearest state (flat metric on the torus)"""
    X = np.atleast_2d(X)
    D = wrap(X[:, None, :] - np.asarray(P)[None, :, :])
    return np.sqrt((D ** 2).sum(-1)).min(1)
