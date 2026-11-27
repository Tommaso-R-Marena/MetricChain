"""Rigorous primitives for GEOMETRY-REQ-0006 (ball arithmetic: Arb through python-flint).

TRUSTED.  Everything that concludes an inequality in the certificates goes through the functions
of this file; they use only Arb ball arithmetic (every ball contains the exact real number it
stands for), exact rational arithmetic (`fractions.Fraction`), and comparisons of balls, which
python-flint answers True only when the relation holds for all points of the balls.

Conventions.
* Angles are measured in units of pi: an angle is pi * tau, tau a `Fraction` (exact) or a ball.
* A *form* is a multi-affine trigonometric polynomial {alpha: ball} as in gr6_model.py;
  P = (P_0, .., P_{nv-1}) with P_m = (1, x_m, y_m) is a point of its multi-affine extension
  form^(P) = sum_alpha coef_alpha prod_m P_m[alpha_m], and form(theta) = form^((1, cos, sin)(theta_m)).
* `x.lower()` / `x.upper()` of a ball are exact numbers (balls of radius 0) below / above every
  point of the ball; comparing two exact numbers is an exact comparison.
"""
from __future__ import annotations

from fractions import Fraction as Fr
from itertools import product

from flint import arb, arb_mat, ctx, fmpq

PREC = 192                      # working precision in bits (set by set_precision)


def set_precision(bits=PREC):
    ctx.prec = bits


def to_fmpq(x):
    x = Fr(x)
    return fmpq(x.numerator, x.denominator)


def to_fraction(x):
    """Exact value of an exact ball (radius 0) as a Fraction."""
    assert x.is_exact()
    q = x.fmpq()
    return Fr(int(q.p), int(q.q))


def ball(x):
    """A ball containing the rational (or the float, exactly) x."""
    return arb(to_fmpq(x)) if isinstance(x, (Fr, int)) else arb(x)


# ------------------------------------------------------------------ points and arcs of the circle
def point(tau):
    """(1, cos(pi tau), sin(pi tau)) for an exact rational tau (Fraction) or for a ball tau; in the
    second case the result encloses the values for every real tau in the ball."""
    if isinstance(tau, (Fr, int)):
        s, c = arb.sin_cos_pi_fmpq(to_fmpq(tau))
    else:
        s, c = tau.sin_cos_pi()
    return (arb(1), c, s)


def arc_hull(lo, hi):
    """Vertices (1, x, y) of a triangle that contains the arc {(cos pi t, sin pi t): lo <= t <= hi},
    for exact rationals lo <= hi with hi - lo <= 1/2 (an arc of at most a quarter turn).

    Proof.  Let m = (lo + hi)/2 and w = pi (hi - lo)/2 <= pi/4.  In the frame where the midpoint
    of the arc is (1, 0) the arc is {(cos s, sin s): |s| <= w}, and the triangle with vertices
    (cos w, -sin w), (cos w, sin w), (1/cos w, 0) is {x >= cos w, x cos w + y sin w <= 1,
    x cos w - y sin w <= 1}; a point of the arc satisfies cos s >= cos w and cos(s -+ w) <= 1.
    The three vertices are the two end points and the point (cos pi m, sin pi m) / cos w.
    A degenerate arc (lo == hi) is returned as its single point."""
    lo, hi = Fr(lo), Fr(hi)
    assert 0 <= hi - lo <= Fr(1, 2)
    if lo == hi:
        return [point(lo)]
    sec = 1 / arb.cos_pi_fmpq(to_fmpq((hi - lo) / 2))
    _, cm, sm = point((lo + hi) / 2)
    return [point(lo), point(hi), (arb(1), cm * sec, sm * sec)]


# ------------------------------------------------------------------ multi-affine forms
def ma_eval(form, P):
    """Enclosure of form^(P).  P[m] may be None for a variable that the form does not contain."""
    total = arb(0)
    for alpha, coef in form.items():
        term = coef
        for m, a in enumerate(alpha):
            if a:
                term = term * P[m][a]
        total += term
    return total


def ma_range(form, hulls):
    """(lo, hi), exact numbers with lo <= form(theta) <= hi for all theta in the box whose m-th
    side is the arc with hull `hulls[m]` (`arc_hull`); hulls[m] = [None] for an absent variable.

    Proof.  form^ is affine in each (x_m, y_m) separately, the m-th arc lies in the convex hull of
    hulls[m], and a function that is affine in each block of variables attains its extrema over a
    product of polytopes at a tuple of vertices."""
    lo = hi = None
    for P in product(*hulls):
        v = ma_eval(form, P)
        l, u = v.lower(), v.upper()
        if lo is None or l < lo:
            lo = l
        if hi is None or hi < u:
            hi = u
    return lo, hi


# ------------------------------------------------------------------ symmetric interval matrices
def sym_eig_enclosure(M, Q):
    """Intervals that contain the spectrum of every real symmetric matrix S with S_ij in M_ij.

    M: n x n list of lists of balls; Q: n x n matrix of floats (any; approximate eigenvectors of
    the midpoint make the result sharp).  Returns [(lo_i, hi_i)], exact numbers, such that every
    eigenvalue of every such S lies in the union of the [lo_i, hi_i]; if these intervals are
    pairwise disjoint, each contains exactly one eigenvalue.  Raises ZeroDivisionError if Q is not
    certified to be invertible.

    Proof.  T = Q^-1 S Q has the (real) spectrum of S and lies in the ball matrix
    Qinv * M * Q computed below (Qinv encloses the exact inverse of the exact float matrix Q).
    Gershgorin: every eigenvalue lies in some disc |z - T_ii| <= sum_{j != i} |T_ij|, and a union
    of k discs disjoint from the others contains exactly k eigenvalues."""
    n = len(M)
    Qa = arb_mat(n, n, [arb(float(Q[i][j])) for i in range(n) for j in range(n)])
    T = Qa.inv() * arb_mat(n, n, [M[i][j] for i in range(n) for j in range(n)]) * Qa
    out = []
    for i in range(n):
        r = arb(0)
        for j in range(n):
            if j != i:
                r += T[i, j].abs_upper()
        out.append(((T[i, i] - r).lower(), (T[i, i] + r).upper()))
    return out


def pairwise_disjoint(intervals):
    """True iff the closed intervals [(lo, hi)] (exact numbers) are pairwise disjoint."""
    s = sorted(intervals, key=lambda iv: float(iv[0]))
    return all(s[i][1] < s[i + 1][0] for i in range(len(s) - 1)) and all(lo <= hi for lo, hi in s)


# ------------------------------------------------------------------ Krawczyk
def krawczyk(f, jac, centre, radius):
    """Krawczyk test for f: R^n -> R^n on the box Y = centre + [-radius, radius]^n.

    f(list of n balls) -> list of n balls enclosing f on the box given by the balls;
    jac(list of n balls) -> n x n list of lists of balls enclosing the Jacobian on that box;
    centre: list of n exact balls (radius 0); radius: positive float.

    Computes K = y0 - C f(y0) + (I - C J(Y)) (Y - y0) with C the midpoint of an enclosure of
    J(y0)^-1, and returns (True, K) iff K_i lies in the interior of Y_i for every i.  In that case
    f has exactly one zero in Y, it lies in K, and every matrix of J(Y) is nonsingular
    (Krawczyk 1969, Moore 1977, Rump 1983).  Returns (False, None) if the test fails, including
    the case where J(y0) is not certified to be invertible."""
    n = len(centre)
    assert all(c.is_exact() for c in centre) and radius > 0
    Y = [c + arb(0, radius) for c in centre]
    J0 = jac(centre)
    try:
        C = arb_mat(n, n, [J0[i][j] for i in range(n) for j in range(n)]).inv().mid()
    except ZeroDivisionError:
        return False, None
    JY = jac(Y)
    J = arb_mat(n, n, [JY[i][j] for i in range(n) for j in range(n)])
    eye = arb_mat(n, n, [int(i == j) for i in range(n) for j in range(n)])
    K = arb_mat(n, 1, list(centre)) - C * arb_mat(n, 1, list(f(centre))) \
        + (eye - C * J) * arb_mat(n, 1, [arb(0, radius)] * n)
    K = [K[i, 0] for i in range(n)]
    if all(Y[i].contains_interior(K[i]) for i in range(n)):
        return True, K
    return False, None
