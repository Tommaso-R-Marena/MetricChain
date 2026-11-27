#!/usr/bin/env python3
"""zlev.py -- finite-n side of the review of Z_REPORT.md.

The exact one-level evaluator is the one of the referee of Q2 (experiments/workstreams/Q2/review/rlib.py, imported
read-only under the name RL: tables of the outer cube, r_dagger, pi_dagger and the constants of Theorem 11.56).  It is
independent of the libraries the coordinator used for Z (q2lib/qlib/r12lib).  Everything else here is written from the
text of Z_REPORT.md (sections 3-6) and Q2_REPORT.md (sections 2, 4): the functions ell_0, q, the level L(d; n_o, e) of
Lemma Z2, the design of Proposition Z3, the families of Proposition Z4.
"""
import importlib.util
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("q2review_rlib", os.path.join(HERE, '..', '..', 'Q2', 'review', 'rlib.py'))
RL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RL)

LN2 = math.log(2.0)
E1 = math.e
C3 = 3 * E1 + 1
C12 = 12 * E1 * (E1 - 1)
C18 = math.log(18 * E1 * (E1 - 1))
C24 = math.log(24 * E1 * (E1 - 1))
INF = float('inf')


# ---- the functions of Lemma U at tolerance b = 1 (Q2_REPORT section 2), from the text
def A_n(u, n):
    return (2 * u + LN2) * n + 3.0


def mbar(u, n):
    return n + 2 + math.log2(C12 * A_n(u, n))


def Kbar(u, n, Lam):
    return 18 * (Lam + math.log(2 * A_n(u, n) * mbar(u, n) * (n + 3))) + 1


def q(u, n, Lam):
    return math.log(4.0 * (n + 1)) + math.log(A_n(u, n)) + C24 + math.log(Kbar(u, n, Lam))


def ell0(u, n, Lam):
    return 1 + 2 * math.log(A_n(u, n)) + C18 + math.log(Kbar(u, n, Lam)) + math.log(n + 3.0)


# ---- Z_REPORT section 4
def dmin(u):
    return int(math.floor(1.0 / (2 * u))) + 2


def X0(u, d):
    return 2.0 + math.log(3.0 * (d + 1)) + 2 * u + math.exp(u)


class Lines:
    """a finite family of lines (B_k, sigma_k) containing the zero line; majorant(d, x) = max_k [d B_k - sigma_k x].

    The maximum is evaluated exactly through the upper-left convex hull of the points (sigma_k, B_k): for x >= 0 only the
    vertices of the concave envelope between the point of least sigma and the point of largest B can be maximal; the
    vertex for a given t = x/d is found by bisection on the (decreasing) slopes of the hull.  major_brute is the direct
    maximum over all lines (used to validate)."""

    def __init__(self, Bs, Ss):
        self.B = np.asarray(Bs, dtype=np.float64)
        self.S = np.asarray(Ss, dtype=np.float64)
        assert self.B[0] == 0.0 and self.S[0] == 0.0, "the zero line must be in the family"
        assert np.all(self.B >= 0) and np.all(self.S >= 0) and np.all(self.S <= 1 + 1e-12)
        # hull
        order = np.lexsort((-self.B, self.S))             # by sigma, then by decreasing B
        pts = []
        lastS = None
        for i in order:
            sg, b = float(self.S[i]), float(self.B[i])
            if lastS is not None and sg == lastS:
                continue                                   # same slope, smaller B: dominated
            lastS = sg
            if pts and b <= pts[-1][1]:
                continue                                   # larger slope and not larger B: dominated for x >= 0
            while len(pts) >= 2:
                (s1, b1), (s2, b2) = pts[-2], pts[-1]
                # keep pts[-1] only if it lies strictly above the chord from pts[-2] to the new point
                if (b2 - b1) * (sg - s1) <= (b - b1) * (s2 - s1):
                    pts.pop()
                else:
                    break
            pts.append((sg, b))
        self.hS = np.array([p[0] for p in pts])
        self.hB = np.array([p[1] for p in pts])
        if len(pts) > 1:
            self.hslope = (self.hB[1:] - self.hB[:-1]) / (self.hS[1:] - self.hS[:-1])     # decreasing, > 0
            self._neg = -self.hslope                                                     # increasing
        else:
            self.hslope = np.zeros(0)
            self._neg = np.zeros(0)

    def _idx(self, t):
        """index of the hull vertex maximising B - t sigma: the number of hull slopes that exceed t."""
        return np.searchsorted(self._neg, -np.asarray(t, dtype=np.float64), side='left')

    def env(self, t):
        """M(t) = max_k [B_k - sigma_k t] for an array t >= 0."""
        t = np.atleast_1d(np.asarray(t, dtype=np.float64))
        i = self._idx(t)
        return self.hB[i] - self.hS[i] * t

    def major(self, d, x):
        """max_k [d B_k - sigma_k x] for scalar d > 0 and array x >= 0."""
        x = np.atleast_1d(np.asarray(x, dtype=np.float64))
        i = self._idx(x / d)
        return d * self.hB[i] - self.hS[i] * x

    def major_brute(self, d, x):
        x = np.atleast_1d(np.asarray(x, dtype=np.float64))
        out = np.empty(x.shape)
        step = max(1, int(4e6 // len(self.B)))
        for i in range(0, len(x), step):
            out[i:i + step] = (d * self.B[None, :] - self.S[None, :] * x[i:i + step, None]).max(axis=1)
        return out


class Sat:
    """a family that SATURATES the type H^infty(lines; E): certified ln-cost = max_k [d B_k - sigma_k x] + E(d, x; ln(1/delta) + d ln 2)
    (the zero line makes the majorant nonnegative).  Least accuracy xmin."""

    def __init__(self, lines, Efun=None, xmin=1.0):
        self.lines, self.Efun, self.xmin = lines, Efun, xmin

    def E(self, d, x, Lam):
        return 0.0 if self.Efun is None else self.Efun(d, x, Lam)

    def cost(self, d, xs, ld):
        xs = np.atleast_1d(np.asarray(xs, dtype=np.float64))
        assert xs.min() >= self.xmin - 1e-12
        Lam = -ld + d * LN2
        e = np.array([self.E(d, x, Lam) for x in xs]) if self.Efun is not None else 0.0
        return self.lines.major(d, xs) + e


def level_Z2(cu, d, n_o, y, ld, inner_cost, tab=None):
    """the level L(d; n_o, e = y/n_o) of Lemma Z2: Algorithm 2L+ in dimension d with lambda = 1, eta = 1/2, eta' = 1,
    nu_1 = 1, tolerance 1, threshold theta = 3 (n_o + 1) exp(2u + e^u + n_o e), the ladder of step one from
    x_1 = min{max(ceil(n_o theta_na(e)), 1), ceil(2 u n_i) - 1} down to 1, inner procedures I_l = F(n_i, x_l, delta').
    inner_cost(n_i, xs, ld') -> array of ln-costs.  Returns dict(lC, xout, ldp, L, x1, vth, lev)."""
    u = cu.u
    n_i = d - n_o
    assert 1 <= n_o <= d - 1 and 2 * u * n_i > 1
    e = y / n_o
    vth = cu.theta(e)
    lth = math.log(3.0 * (n_o + 1)) + 2 * u + math.exp(u) + y
    x1 = min(max(math.ceil(n_o * vth - 1e-12), 1), math.ceil(2 * u * n_i - 1e-12) - 1)
    xs = np.arange(x1, 0, -1, dtype=np.float64)
    L = len(xs)
    lev = RL.Level(u, d, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, ld, L, tab=tab)
    lcost = inner_cost(n_i, xs, lev.ldp)
    lC = lev.lcmax(list(xs), lcost)
    return dict(lC=lC, xout=float(lev.x_out), ldp=lev.ldp, L=L, x1=x1, vth=vth, lev=lev, e=e)


def proxy_all(cu, d, y, lines, no_max=None, brute=False):
    """Pi_j(n_o) = max_lines [(d - n_o) B + (1 - sigma) n_o theta_na(y/n_o)] for n_o = 1 .. d - d_min + 1 (array).
    = c + (d - n_o) M(c/(d - n_o)),  c = n_o theta_na(y/n_o),  M the envelope of the lines."""
    dm = dmin(cu.u)
    hi = d - dm + 1 if no_max is None else no_max
    nos = np.arange(1, hi + 1, dtype=np.float64)
    c = nos * cu.theta_v(y / nos)
    if not brute:
        ni = d - nos
        return nos.astype(int), c + ni * lines.env(c / ni)
    out = np.empty(nos.shape)
    B, S = lines.B, lines.S
    step = max(1, int(4e6 // len(B)))
    for i in range(0, len(nos), step):
        out[i:i + step] = ((d - nos[i:i + step])[:, None] * B[None, :] + c[i:i + step][:, None] * (1.0 - S)[None, :]).max(axis=1)
    return nos.astype(int), out
