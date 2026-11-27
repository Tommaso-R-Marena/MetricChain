"""Shared helpers for the Geometric Inference division's experiments.

Floating-point helpers (numpy) for exploration and exact helpers (fractions / modular
arithmetic) for computer-assisted proofs.  Conventions:

* a chain with n atoms has bonds a = 0..n-2 (atom a -> a+1), torsions m = 0..n-4
  (torsion m is the dihedral of atoms m, m+1, m+2, m+3 about the bond m+1 -> m+2);
* `stack(Xs, w)` is the stacked configuration z_i = (sqrt(w_k) x_i^(k))_k in R^{3K};
* quadratic forms on R^m are coordinatised by the upper triangle (i <= j).
"""
from fractions import Fraction
import numpy as np


# ---------------------------------------------------------------- floating point
def chain(n, tors, b=1.0, theta=np.deg2rad(111.0)):
    """NeRF chain in R^3: bond length b, bond angle theta, torsions tors[0..n-4]."""
    X = np.zeros((n, 3))
    X[1] = [b, 0, 0]
    X[2] = X[1] + b * np.array([-np.cos(theta), np.sin(theta), 0.0])
    for i in range(3, n):
        a, bb, c = X[i - 3], X[i - 2], X[i - 1]
        bc = (c - bb) / np.linalg.norm(c - bb)
        nrm = np.cross(bb - a, bc)
        nrm /= np.linalg.norm(nrm)
        m = np.cross(nrm, bc)
        t = tors[i - 3]
        X[i] = c + (-b * np.cos(theta)) * bc + (b * np.sin(theta) * np.cos(t)) * m \
            + (b * np.sin(theta) * np.sin(t)) * nrm
    return X


def edm(X):
    G = X @ X.T
    d = np.diag(G)
    return d[:, None] + d[None, :] - 2 * G


def stack(Xs, w):
    return np.hstack([np.sqrt(wk) * X for wk, X in zip(w, Xs)])


def sym_index(m):
    return [(i, j) for i in range(m) for j in range(i, m)]


def quad_row(v, idx):
    """Coefficients of v^T S v in the coordinates S_ij (i <= j)."""
    return np.array([v[i] * v[j] if i == j else 2 * v[i] * v[j] for (i, j) in idx])


def sym_from_vec(vec, m, idx=None):
    idx = idx or sym_index(m)
    S = np.zeros((m, m))
    for t, (i, j) in enumerate(idx):
        S[i, j] = S[j, i] = vec[t]
    return S


def edge_vectors(Z, angles=True):
    """Statewise-constrained edge vectors of a (stacked) chain: bonds and, if `angles`,
    the 1-3 vectors."""
    E = [Z[i + 1] - Z[i] for i in range(len(Z) - 1)]
    if angles:
        E += [Z[i + 2] - Z[i] for i in range(len(Z) - 2)]
    return E


def conic_matrix(Z, angles=True):
    idx = sym_index(Z.shape[1])
    return np.array([quad_row(e, idx) for e in edge_vectors(Z, angles)])


def kabsch_rmsd(A, B, allow_reflection=True):
    A = A - A.mean(0)
    B = B - B.mean(0)
    U, s, Vt = np.linalg.svd(A.T @ B)
    if not allow_reflection and np.linalg.det(U @ Vt) < 0:
        s = s.copy()
        s[-1] = -s[-1]
    return float(np.sqrt(max(0.0, (A ** 2).sum() + (B ** 2).sum() - 2 * s.sum()) / len(A)))


# ---------------------------------------------------------------- exact arithmetic
def rat_circle(t):
    """Rational point (cos, sin) of the unit circle with half-angle tangent t."""
    t = Fraction(t)
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def chain_exact(n, tors_t, cth, sth, dim=3):
    """Exact chain with unit bonds, bond angle (cos, sin) = (cth, sth) in a field containing
    them, torsion half-angle tangents tors_t (rational).  Works over Fraction or any type
    supporting + - * / (e.g. the ModSqrt class below).  Returns a list of 3-vectors."""
    one = cth * 0 + 1
    zero = cth * 0
    X = [[zero, zero, zero], [one, zero, zero], [one - cth, sth, zero]]
    for i in range(3, n):
        a, bb, c = X[i - 3], X[i - 2], X[i - 1]
        bc = [c[j] - bb[j] for j in range(3)]                      # unit
        ab = [bb[j] - a[j] for j in range(3)]
        nr = cross(ab, bc)                                         # norm = sin(theta)
        nr = [x / sth for x in nr]
        m = cross(nr, bc)
        ct, st = rat_circle(tors_t[i - 3])
        ct, st = one * ct.numerator / ct.denominator, one * st.numerator / st.denominator
        X.append([c[j] - cth * bc[j] + sth * ct * m[j] + sth * st * nr[j] for j in range(3)])
    return X


class Mod:
    """Element of F_p (p prime), with field operations; used to bound ranks from below:
    rank over F_p of the reduction of a matrix is at most its rank over Q."""
    __slots__ = ("v",)
    p = 2147483629                                                   # prime below 2^31

    def __init__(self, v):
        if isinstance(v, Fraction):
            v = v.numerator * pow(v.denominator, -1, Mod.p)
        self.v = int(v) % Mod.p

    def _c(self, o):
        return o if isinstance(o, Mod) else Mod(o)

    def __add__(self, o): return Mod(self.v + self._c(o).v)
    __radd__ = __add__
    def __sub__(self, o): return Mod(self.v - self._c(o).v)
    def __rsub__(self, o): return Mod(self._c(o).v - self.v)
    def __mul__(self, o): return Mod(self.v * self._c(o).v)
    __rmul__ = __mul__
    def __truediv__(self, o): return Mod(self.v * pow(self._c(o).v, -1, Mod.p))
    def __neg__(self): return Mod(-self.v)
    def __eq__(self, o): return self.v == self._c(o).v
    def __repr__(self): return f"Mod({self.v})"


def rank_mod_p(rows, p=None):
    """Rank over F_p of an integer matrix given as a list of lists of ints (already reduced
    or not).  Plain Gaussian elimination with numpy int64 (p < 2^31)."""
    p = p or Mod.p
    A = np.array([[int(x) % p for x in r] for r in rows], dtype=np.int64)
    if A.size == 0:
        return 0
    nr, nc = A.shape
    r = 0
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if A[i, c] % p:
                piv = i
                break
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), -1, p)
        A[r] = (A[r] * inv) % p
        nzr = np.nonzero(A[:, c])[0]
        for i in nzr:
            if i != r:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
        if r == nr:
            break
    return r


def tonelli(a, p):
    """A square root of a modulo the odd prime p (a must be a quadratic residue)."""
    a %= p
    assert pow(a, (p - 1) // 2, p) == 1, "not a quadratic residue"
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r
