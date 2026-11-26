#!/usr/bin/env python3
"""R22 own library, written from the definitions of <GEO>/docs/geometry/ENSEMBLE_RIGIDITY.md (d84a43b) BEFORE opening
the Geometry division's code.  Nothing here is copied from experiments/geometry/ or from the coordinator's
hinge_pair.py (a transfer-frame construction is used instead of NeRF).

Objects
  chain(tors, cosang)        n = len(tors)+3 atoms in R^3, unit bonds, bond angle with cosine `cosang`
  chain_exact(tans, ca, sa)  the same in exact rational arithmetic (torsions by half-angle tangents; cos/sin of the
                             supplement of the bond angle rational, e.g. bond-angle cosine -5/13 -> ca=5/13, sa=12/13)
  E0(n)                      constrained pairs: bonds (i,i+1) and 1-3 pairs (i,i+2)
  stack(states, w)           stacked configuration z (n x 3K), blocks sqrt(w_k) X_k
  conic_matrix(z, n)         rows  e (x) e  for the E0-edge vectors of z, in the basis of Sym(m) (m = 3K)
  conic_nullity(z)           dim N(z) by SVD, with the two singular values at the gap
  rank_exact(rows)           rank over Q of a matrix of Fractions/ints (fraction-free Bareiss elimination)
  sqdist(X)                  D(X)
  procrustes2(X, Y)          d_P(X,Y)^2 = min over isometries (reflections included) of ||X - gY||_F^2
  torsion_tangents(tors,...) the n-3 torsion derivatives dX/dphi_j (analytic)
  iso_basis(X)               orthonormal basis of the infinitesimal isometries at X (6-dim for non-collinear X)
"""
from fractions import Fraction
import numpy as np


# ----------------------------------------------------------------------------------------------- chains
def _Rx(c, s, one, zero):
    return [[one, zero, zero], [zero, c, -s], [zero, s, c]]


def _Rz(c, s, one, zero):
    return [[c, -s, zero], [s, c, zero], [zero, zero, one]]


def _mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def chain(tors, cosang=-1.0 / 3.0, bond=1.0):
    """Transfer-frame construction.  Atom 0 at the origin; bond j (atom j-1 -> j) has direction F_j e_x;
    F_1 = I, F_2 = F_1 Rz(alpha), F_{j+2} = F_{j+1} Rx(phi_j) Rz(alpha), alpha = pi - bond angle."""
    tors = np.asarray(tors, float)
    ca, sa = -cosang, np.sqrt(1.0 - cosang * cosang)
    Rz = np.array([[ca, -sa, 0.0], [sa, ca, 0.0], [0.0, 0.0, 1.0]])
    n = len(tors) + 3
    X = np.zeros((n, 3))
    F = np.eye(3)
    X[1] = X[0] + bond * F[:, 0]
    F = F @ Rz
    X[2] = X[1] + bond * F[:, 0]
    for j, phi in enumerate(tors):
        c, s = np.cos(phi), np.sin(phi)
        Rx = np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])
        F = F @ Rx @ Rz
        X[j + 3] = X[j + 2] + bond * F[:, 0]
    return X


def chain_exact(tans, ca=Fraction(5, 13), sa=Fraction(12, 13)):
    """Exact chain: torsion j has half-angle tangent tans[j] (a Fraction); ca, sa = cos, sin of pi - bond angle."""
    one, zero = Fraction(1), Fraction(0)
    assert ca * ca + sa * sa == 1
    Rz = _Rz(ca, sa, one, zero)
    F = [[one, zero, zero], [zero, one, zero], [zero, zero, one]]
    X = [[zero, zero, zero]]
    X.append([X[-1][i] + F[i][0] for i in range(3)])
    F = _mm(F, Rz)
    X.append([X[-1][i] + F[i][0] for i in range(3)])
    for t in tans:
        t = Fraction(t)
        c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        F = _mm(_mm(F, _Rx(c, s, one, zero)), Rz)
        X.append([X[-1][i] + F[i][0] for i in range(3)])
    return X


def E0(n):
    return [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]


def sqdist(X):
    X = np.asarray(X, float)
    return ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)


def stack(states, w):
    return np.concatenate([np.sqrt(wk) * np.asarray(Xk, float) for Xk, wk in zip(states, w)], axis=1)


# ----------------------------------------------------------------------------------------------- conic system
def sym_index(m):
    return [(a, b) for a in range(m) for b in range(a, m)]


def conic_matrix(z, edges=None):
    z = np.asarray(z, float)
    n, m = z.shape
    idx = sym_index(m)
    edges = E0(n) if edges is None else edges
    R = np.empty((len(edges), len(idx)))
    for r, (i, j) in enumerate(edges):
        e = z[j] - z[i]
        R[r] = [e[a] * e[b] * (1.0 if a == b else 2.0) for a, b in idx]
    return R


def conic_nullity(z, edges=None, rtol=1e-9):
    R = conic_matrix(z, edges)
    s = np.linalg.svd(R, compute_uv=False)
    rank = int((s > rtol * s[0]).sum())
    last = float(s[rank - 1] / s[0])
    nxt = float(s[rank] / s[0]) if rank < len(s) else 0.0
    return R.shape[1] - rank, last, nxt


def conic_nullspace(z, edges=None, rtol=1e-9):
    """orthonormal basis (as symmetric matrices) of N(z)"""
    z = np.asarray(z, float)
    m = z.shape[1]
    R = conic_matrix(z, edges)
    U, s, Vt = np.linalg.svd(R, full_matrices=True)
    rank = int((s > rtol * s[0]).sum())
    idx = sym_index(m)
    out = []
    for v in Vt[rank:]:
        S = np.zeros((m, m))
        for c, (a, b) in zip(v, idx):
            S[a, b] = S[b, a] = c
        out.append(S)
    return out


def conic_rows_exact(zrows, edges=None):
    """zrows: list of n lists of Fractions (length m).  Integer rows (denominators cleared rowwise)."""
    n, m = len(zrows), len(zrows[0])
    idx = sym_index(m)
    edges = E0(n) if edges is None else edges
    rows = []
    for (i, j) in edges:
        e = [zrows[j][a] - zrows[i][a] for a in range(m)]
        row = [e[a] * e[b] * (1 if a == b else 2) for a, b in idx]
        den = 1
        for x in row:
            den = den * x.denominator // _gcd(den, x.denominator)
        rows.append([int(x * den) for x in row])
    return rows


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def rank_exact(rows):
    """Rank over Q of an integer matrix by fraction-free (Bareiss) elimination with row and column search."""
    A = [list(r) for r in rows]
    nr, nc = len(A), len(A[0]) if A else 0
    rank, prev = 0, 1
    col = 0
    while rank < nr and col < nc:
        piv = None
        for r in range(rank, nr):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            col += 1
            continue
        A[rank], A[piv] = A[piv], A[rank]
        p = A[rank][col]
        for r in range(rank + 1, nr):
            f = A[r][col]
            for c in range(col + 1, nc):
                A[r][c] = (A[r][c] * p - f * A[rank][c]) // prev
            A[r][col] = 0
        prev = p
        rank += 1
        col += 1
    return rank


# ----------------------------------------------------------------------------------------------- shapes
def procrustes2(X, Y):
    """squared Procrustes distance with reflections allowed (min over O(3) and translations)"""
    X = np.asarray(X, float)
    Y = np.asarray(Y, float)
    Xc = X - X.mean(0)
    Yc = Y - Y.mean(0)
    s = np.linalg.svd(Xc.T @ Yc, compute_uv=False)
    return max(float((Xc ** 2).sum() + (Yc ** 2).sum() - 2.0 * s.sum()), 0.0)


def procrustes_align(X, Y):
    """return g(Y) = optimally aligned copy of Y onto X (reflections allowed)"""
    X = np.asarray(X, float)
    Y = np.asarray(Y, float)
    mx, my = X.mean(0), Y.mean(0)
    U, s, Vt = np.linalg.svd((X - mx).T @ (Y - my))
    R = U @ Vt                      # maps Y-frame rows:  (Y - my) @ R.T  ~ X - mx
    return (Y - my) @ R.T + mx


def torsion_tangents(tors, cosang=-1.0 / 3.0):
    """T[j] = dX/dphi_j (n x 3): atoms m >= j+3 rotate about the axis of bond j+2 (atoms j+1 -> j+2)."""
    X = chain(tors, cosang)
    n = len(X)
    T = np.zeros((len(tors), n, 3))
    for j in range(len(tors)):
        axis = X[j + 2] - X[j + 1]
        axis = axis / np.linalg.norm(axis)
        for m in range(j + 3, n):
            T[j, m] = np.cross(axis, X[m] - X[j + 2])
    return T


def iso_basis(X):
    """orthonormal basis (rows, flattened n*3) of the infinitesimal isometries at X"""
    X = np.asarray(X, float)
    n = len(X)
    vs = []
    for a in range(3):
        v = np.zeros((n, 3))
        v[:, a] = 1.0
        vs.append(v.ravel())
    for a in range(3):
        w = np.zeros(3)
        w[a] = 1.0
        vs.append(np.cross(w, X).ravel())
    Q, R = np.linalg.qr(np.array(vs).T)
    keep = np.abs(np.diag(R)) > 1e-10
    return Q[:, keep].T


def perp_projector(z):
    """orthogonal projector of R^n onto the complement of span(1, columns of z); also its rank"""
    z = np.asarray(z, float)
    n = len(z)
    B = np.concatenate([np.ones((n, 1)), z], axis=1)
    U, s, _ = np.linalg.svd(B, full_matrices=False)
    r = int((s > 1e-10 * s[0]).sum())
    U = U[:, :r]
    return np.eye(n) - U @ U.T, n - r


# ----------------------------------------------------------------------------------------------- self-test
if __name__ == "__main__":
    import time
    t0 = time.time()
    rng = np.random.default_rng(22)
    bad = 0
    print("r22lib self-test (controls of the library itself)")
    for cosang in (-1.0 / 3.0, -5.0 / 13.0, np.cos(np.deg2rad(111.0))):
        for n in (5, 9, 14):
            tors = rng.uniform(-np.pi, np.pi, n - 3)
            X = chain(tors, cosang)
            D = sqdist(X)
            b = max(abs(D[i, i + 1] - 1.0) for i in range(n - 1))
            c = max(abs(D[i, i + 2] - (2.0 - 2.0 * cosang)) for i in range(n - 2))
            # analytic torsion derivatives against central differences
            T = torsion_tangents(tors, cosang)
            h = 1e-6
            err = 0.0
            for j in range(n - 3):
                tp, tm = tors.copy(), tors.copy()
                tp[j] += h
                tm[j] -= h
                err = max(err, np.abs((chain(tp, cosang) - chain(tm, cosang)) / (2 * h) - T[j]).max())
            bad += int(b > 1e-12 or c > 1e-12 or err > 1e-7)
            print(f"  cos={cosang:+.4f} n={n}: bond err {b:.1e}, 1-3 err {c:.1e}, tangent err {err:.1e}")
    # exact chain against float chain
    tans = [Fraction(int(v), 7) for v in rng.integers(-20, 21, 9)]
    Xe = chain_exact(tans)
    Xf = chain([2 * np.arctan(float(t)) for t in tans], -5.0 / 13.0)
    d = np.abs(np.array([[float(v) for v in r] for r in Xe]) - Xf).max()
    exact_ok = all(sum((Xe[i + 1][a] - Xe[i][a]) ** 2 for a in range(3)) == 1 for i in range(len(Xe) - 1)) and \
        all(sum((Xe[i + 2][a] - Xe[i][a]) ** 2 for a in range(3)) == 2 + Fraction(10, 13) for i in range(len(Xe) - 2))
    bad += int(d > 1e-12 or not exact_ok)
    print(f"  exact chain vs float chain: max diff {d:.1e}; exact bond/1-3 identities hold: {exact_ok}")
    # rank_exact against numpy on random integer matrices of known rank
    for (r, c, k) in ((6, 9, 4), (12, 10, 7), (20, 21, 20)):
        A = rng.integers(-5, 6, (r, k)) @ rng.integers(-5, 6, (k, c))
        re_ = rank_exact([[int(v) for v in row] for row in A])
        rn = np.linalg.matrix_rank(A.astype(float))
        bad += int(re_ != rn)
        print(f"  rank_exact on a {r}x{c} integer matrix built with rank <= {k}: exact {re_}, numpy {rn}")
    # procrustes: invariant under an isometry with reflection, positive otherwise
    X = chain(rng.uniform(-np.pi, np.pi, 7))
    Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    if np.linalg.det(Q) > 0:
        Q[:, 0] *= -1
    p0 = procrustes2(X, X @ Q.T + rng.normal(size=3))
    p1 = procrustes2(X, chain(rng.uniform(-np.pi, np.pi, 7)))
    pa = np.abs(procrustes_align(X, X @ Q.T + 1.0) - X).max()
    bad += int(p0 > 1e-12 or p1 < 1e-3 or pa > 1e-12)
    print(f"  procrustes2 of a reflected, rotated, shifted copy: {p0:.1e}; of another chain: {p1:.3f}; align err {pa:.1e}")
    print(f"self-test violations: {bad}")
    print(f"ALL DONE {time.time() - t0:.1f} s")
