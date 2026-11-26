#!/usr/bin/env python3
"""Workstream Z -- shared routines (docs/workstreams/Z_REPORT.md).

The exponent-level objects come from experiments/workstreams/R/rlib.py (slope map, orbit curves), the exact
one-level evaluator and the formulas of Lemma U and of the chain from experiments/workstreams/Q2/q2lib.py
(which imports the two independent evaluators of Q and of referee R12).  Nothing of either is modified.

  ChainZ      the cut orbit curves W_j, their top values b_j  (R_REPORT.md section 6; Proposition Z1)
  Psi         the bracket of one level in exponent form, Psi_g(phi; B, s) = (1 - phi) B + (1 - s) phi theta_na(g / phi)
  X0, dmin    the accuracy offset and the least inner dimension of Proposition Z3
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, '..', 'R'))
sys.path.insert(0, os.path.join(HERE, '..', 'Q2'))
import rlib            # noqa: E402
import q2lib as Q2     # noqa: E402


def dmin(u):
    return int(math.floor(1.0 / (2 * u))) + 2


def X0(u, d):
    return 2.0 + math.log(3.0 * (d + 1)) + 2 * u + math.exp(u)


class ChainZ:
    """W_j and b_j for the cube of slope u, cut level s_t = L + dst, restart height b_0 = h + eps1."""

    def __init__(self, u, dst, eps1, J):
        self.u = u
        self.P = rlib.Cube(u).setup()
        P = self.P
        self.h, self.L, self.a = P.h, P.L, P.a
        self.s_t = P.L + dst
        self.b0 = P.h + eps1
        assert self.s_t < 1 - P.h / P.a and self.b0 < (1 - self.s_t) * P.a
        self.cut = [self._cut(j) for j in range(J + 2)]      # None (case A) or (B_t(j), m_j)
        self.b = [self.b0]
        self.range_ok = True
        self.worstW = 0.0
        for j in range(J + 1):
            c = self.cut[j]
            if c is None:
                bn = self.b[j]
            else:
                Bt, m = c
                bn = min(self.b[j], Bt + (1 - self.s_t - Bt / P.a) / (m + 1 / P.a))
            self.b.append(bn)
            w = self.W(j + 1, bn)
            self.worstW = max(self.worstW, w)
            if w > 1 + 1e-12:
                self.range_ok = False
        self._theta_cache = {}

    def _cut(self, j):
        P = self.P
        if P.orbit_with_slope(self.b0, j)[0] <= self.s_t:
            return None
        lo, hi = P.h, self.b0
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if P.orbit_with_slope(mid, j)[0] <= self.s_t:
                lo = mid
            else:
                hi = mid
        return lo, P.orbit_with_slope(lo, j)[1]

    def W(self, j, B):
        c = self.cut[j]
        if c is None or B <= c[0]:
            return self.P.orbit_with_slope(B, j)[0]
        return self.s_t + c[1] * (B - c[0])

    def grid(self, j, N):
        """the grid family of W_j: lines (B, W_j(B)), B a multiple of 1/N in [0, b_j], and B = b_j"""
        Bs = [i / N for i in range(int(math.floor(N * self.b[j] + 1e-12)) + 1)]
        if Bs[-1] < self.b[j]:
            Bs.append(self.b[j])
        return [(B, min(1.0, max(0.0, self.W(j, B)))) for B in Bs]

    def theta(self, e):
        return self.P.theta_na(e)


def Psi(theta, g, phi, lines):
    """max over the lines of (1 - phi) B + (1 - s) phi theta(g / phi)"""
    th = theta(g / phi)
    return max((1 - phi) * B + (1 - s) * phi * th for (B, s) in lines)


def Mval(lines, g):
    return max(B - s * g for (B, s) in lines)
