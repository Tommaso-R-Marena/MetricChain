"""The chain model of GEOMETRY-REQ-0006, written by the Computational Research Division from the
definitions of the Geometric Inference division (their commit 288b2de: `geomlib.chain`, read as
text; nothing of theirs is imported or executed).

TRUSTED (this file defines the function that the certificate is about).

The chain.  n atoms x_0..x_{n-1} in R^3, unit bonds u_k = x_k - x_{k-1} (k = 1..n-1), bond angle
111 degrees = 37 pi / 60 at every interior atom, torsions theta_0..theta_{n-4} (theta_m is the
dihedral of the atoms m, m+1, m+2, m+3).  With

    C = cos(111 deg),  S = sin(111 deg),
    A = [[-C, -S, 0], [S, -C, 0], [0, 0, 1]],      Rx(t) = [[1, 0, 0], [0, cos t, -sin t], [0, sin t, cos t]],
    T_j = Rx(theta_j) A  (j >= 0),   T_{-1} = A,

the NeRF construction of `geomlib.chain` is: frame Phi_k = A T_0 ... T_{k-3} (Phi_1 = I, Phi_2 = A)
whose columns are (bond direction, in-plane normal, binormal), and u_k = Phi_k e_1.  [Derivation:
with the frame (bc, m, nrm) of the three previous atoms the new bond is
-C bc + S cos t m + S sin t nrm and the new frame is the old one times Rx(t) A.  Checked against a
literal transcription of the NeRF recursion in `nerf_chain` below and in the tests.]

Consequently, for 1 <= k < l <= n-1 (the orthogonal prefix Phi_k cancels):

    u_k . u_l = e_1^T T_{k-2} T_{k-1} ... T_{l-3} e_1 ,

and  |x_j - x_i|^2 = (j - i) + 2 sum_{i < k < l <= j} u_k . u_l .

Forms.  Every entry of every T_j is affine in (cos theta_j, sin theta_j) and each product above
contains each T_j at most once, so every squared distance is a *multi-affine form*

    D(theta) = sum_alpha  d_alpha  prod_m  phi_{alpha_m}(theta_m),   phi_0 = 1, phi_1 = cos, phi_2 = sin,

represented here as a dict {alpha: coefficient} with alpha in {0,1,2}^(n-3) and coefficients that
are Arb balls (python-flint), rigorous enclosures of the exact real coefficients (which are
polynomials in C and S with integer coefficients, times the rational couplings).  Entries of A and
Rx that are exactly zero are represented by the empty form and never enter a product; this makes
two structural facts visible in the *support* of the forms (and they are asserted where used):

  (S1) mirror symmetry: no monomial has an odd number of sine factors, i.e. D(-theta) = D(theta)
       [A and the constant and cosine parts of Rx commute with J = diag(1, 1, -1), the sine part
       anticommutes, and e_1^T M e_1 vanishes for a matrix M that anticommutes with J];
  (S2) |x_j - x_i|^2 depends only on theta_i .. theta_{j-3}.
"""
from __future__ import annotations

from fractions import Fraction as Fr

from flint import arb, fmpq

BOND_ANGLE = Fr(37, 60)           # 111 degrees, in units of pi


def bond_angle_cos_sin():
    """(C, S): enclosures of cos and sin of the bond angle (exact rational multiple of pi)."""
    s, c = arb.sin_cos_pi_fmpq(fmpq(BOND_ANGLE.numerator, BOND_ANGLE.denominator))
    return c, s


def statewise_pairs(n):
    """E0: the n-1 bonds followed by the n-2 one-three pairs (0-based atom indices)."""
    return [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]


# ------------------------------------------------------------------ multi-affine forms
def f_add(p, q):
    r = dict(p)
    for alpha, v in q.items():
        r[alpha] = r[alpha] + v if alpha in r else v
    return r


def f_scale(p, s):
    return {alpha: v * s for alpha, v in p.items()}


def f_mul(p, q):
    """Product of two forms in disjoint sets of variables (asserted: the result is multi-affine)."""
    r = {}
    for a, x in p.items():
        for b, y in q.items():
            assert all(i == 0 or j == 0 for i, j in zip(a, b)), "a variable occurs twice: not multi-affine"
            alpha = tuple(i + j for i, j in zip(a, b))
            r[alpha] = r[alpha] + x * y if alpha in r else x * y
    return r


def derivative(form, k):
    """d/d theta_k of a form:  d(a + b cos + c sin) = c cos - b sin  in the k-th variable."""
    r = {}
    for alpha, v in form.items():
        if alpha[k] == 0:
            continue
        beta = alpha[:k] + (3 - alpha[k],) + alpha[k + 1:]
        w = -v if alpha[k] == 1 else v
        r[beta] = r[beta] + w if beta in r else w
    return r


def _mat_mul(M, N):
    out = [[{} for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            acc = {}
            for m in range(3):
                if M[i][m] and N[m][j]:
                    acc = f_add(acc, f_mul(M[i][m], N[m][j]))
            out[i][j] = acc
    return out


class Chain:
    """Squared-distance forms of the n-atom chain.

    By default the bond angle is BOND_ANGLE and the coefficients are Arb balls.  For tests of the
    construction an exact point (C, S) of the unit circle may be given as `cos_sin` (e.g. two
    Fractions with C^2 + S^2 = 1): the same code then computes with exact numbers."""

    def __init__(self, n, cos_sin=None):
        self.n = n
        self.nv = n - 3
        self.exact = cos_sin is not None
        self.C, self.S = cos_sin if self.exact else bond_angle_cos_sin()
        zero = (0,) * self.nv
        C, S = self.C, self.S
        self._zero = zero
        self._one = C * 0 + 1
        self._A = [[{zero: -C}, {zero: -S}, {}], [{zero: S}, {zero: -C}, {}], [{}, {}, {zero: self._one}]]
        self._dots = {}

    def _T(self, j):
        if j < 0:
            return self._A
        cos = {self._zero[:j] + (1,) + self._zero[j + 1:]: self._one}
        sin = {self._zero[:j] + (2,) + self._zero[j + 1:]: self._one}
        rx = [[{self._zero: self._one}, {}, {}], [{}, cos, f_scale(sin, -1)], [{}, sin, cos]]
        return _mat_mul(rx, self._A)

    def bond_dot(self, k, l):
        """The form of u_k . u_l  (1 <= k < l <= n-1):  e_1^T T_{k-2} ... T_{l-3} e_1."""
        assert 1 <= k < l <= self.n - 1
        if (k, l) not in self._dots:
            M = self._T(k - 2)
            for j in range(k - 1, l - 2):
                M = _mat_mul(M, self._T(j))
            self._dots[(k, l)] = M[0][0]
        return self._dots[(k, l)]

    def sqdist(self, i, j):
        """The form of |x_j - x_i|^2  (0 <= i < j <= n-1)."""
        assert 0 <= i < j <= self.n - 1
        form = {self._zero: self._one * (j - i)}
        for k in range(i + 1, j + 1):
            for l in range(k + 1, j + 1):
                form = f_add(form, f_scale(self.bond_dot(k, l), 2))
        return form

    def energy(self, pairs, couplings):
        """The form of H_c = sum_{(i,j) in pairs} c_ij |x_i - x_j|^2, couplings exact rationals."""
        form = {}
        for (i, j), c in zip(pairs, couplings):
            c = Fr(c)
            form = f_add(form, f_scale(self.sqdist(i, j), c if self.exact else fmpq(c.numerator, c.denominator)))
        return form


def odd_sine_monomials(form):
    """Monomials with an odd number of sine factors (empty iff the form is even: (S1))."""
    return [alpha for alpha in form if sum(a == 2 for a in alpha) % 2]


# ------------------------------------------------------------------ floating point reference
def nerf_chain(tors, bond_angle_deg=111.0):
    """Literal transcription (numpy, floating point; NOT part of the certificate) of the NeRF
    recursion of `geomlib.chain` of the requesting division, used to test the forms."""
    import numpy as np

    th = np.deg2rad(bond_angle_deg)
    n = len(tors) + 3
    X = np.zeros((n, 3))
    X[1] = [1.0, 0.0, 0.0]
    X[2] = X[1] + np.array([-np.cos(th), np.sin(th), 0.0])
    for i in range(3, n):
        a, b, c = X[i - 3], X[i - 2], X[i - 1]
        bc = (c - b) / np.linalg.norm(c - b)
        nrm = np.cross(b - a, bc)
        nrm /= np.linalg.norm(nrm)
        m = np.cross(nrm, bc)
        t = tors[i - 3]
        X[i] = c - np.cos(th) * bc + np.sin(th) * (np.cos(t) * m + np.sin(t) * nrm)
    return X
