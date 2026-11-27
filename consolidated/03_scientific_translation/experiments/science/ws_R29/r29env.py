#!/usr/bin/env python3
"""r29env.py -- own routines of workstream R29, second part (nothing imported from the theory division's code).

  CubeF     the cube pair in doubles: theta_na (scalar and vectorised), J, Q, Sigma
  EnvSA     the envelope sequence of Z_ADDENDUM A2/A3, computed WITHOUT a grid ("semi-analytic"), in doubles or in
            mpmath multiprecision:  by Lemma A10's description of the envelope,
                W_j = H_j := Sigma(., W_{j-1}(.))   on [0, Bt_j],        W_j(B) = 1 - m_j (b_j - B)   on [Bt_j, b_j],
            where m_j = max_B (1 - H_j(B))/(b_j - B) (the tangent from (b_j, 1); H_j is convex, so the ratio is
            quasi-concave and a golden-section search finds it), Bt_j the maximiser, and b_{j+1} the root of
            W_j(B) = 1 - B/a.  Evaluating W_j(B) costs j evaluations of the slope map.  Not rigorous: an independent
            high-accuracy value of the true envelope tops b_j, against which certified tops must not fall
            (Corollary A4: every admissible sequence from the same start has tops >= b_j).
"""
import math

import numpy as np


class CubeF:
    def __init__(self, u):
        self.u = float(u)
        self.pu = 1.0 / (1.0 + math.exp(self.u))
        self.a = self.kl(self.pu, 0.5)
        self.lam1 = math.log(2.0 / (1.0 + math.exp(-self.u)))
        self.estar = math.log(math.cosh(self.u / 2.0))
        self.rho_h = self.lam1 / self.u
        self.h = self.kl(self.rho_h, 0.5)
        self.L = math.log((1 - self.rho_h) / self.rho_h) / self.u
        self.thpp = 1.0 / (self.u ** 2 * self.rho_h * (1 - self.rho_h))
        self.cs2 = 2 * math.pi ** 2 * self.h ** 2 * self.thpp

    @staticmethod
    def kl(r, p):
        out = 0.0
        if r > 0:
            out += r * math.log(r / p)
        if r < 1:
            out += (1 - r) * math.log((1 - r) / (1 - p))
        return out

    def rho_of_e(self, e):
        if e <= 0:
            return self.pu
        if e >= self.estar:
            return 0.5
        lo, hi = self.pu, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if mid == lo or mid == hi:
                break
            if self.kl(mid, self.pu) > e:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)

    def theta(self, e):
        if e >= self.estar:
            return 0.0
        if e <= 0:
            return self.a
        return self.kl(self.rho_of_e(e), 0.5)

    def theta_vec(self, e):
        """vectorised theta_na: bisection in rho to the last bit, then one evaluation"""
        e = np.asarray(e, dtype=float)
        pu = self.pu
        lo = np.full(e.shape, pu)
        hi = np.full(e.shape, 0.5)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            with np.errstate(divide="ignore", invalid="ignore"):
                kl = mid * np.log(mid / pu) + (1 - mid) * np.log((1 - mid) / (1 - pu))
            big = kl > e
            hi = np.where(big, mid, hi)
            lo = np.where(big, lo, mid)
        r = 0.5 * (lo + hi)
        out = r * np.log(2 * r) + (1 - r) * np.log(2 * (1 - r))
        return np.where(e >= self.estar, 0.0, np.where(e <= 0, self.a, out))

    def J(self, t):
        return math.log(2.0 / (1.0 + math.exp(-t * self.u))) - t * self.lam1

    def Sigma_bisect(self, B, s):
        """the slope map by plain bisection on Q(t') = B/(1 - s) (kept as a cross-check of Sigma)"""
        if B <= 0:
            return 0.0
        if s >= 1.0 or B >= (1.0 - s) * self.a:
            return math.inf
        tgt = B / (1.0 - s)
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if mid == lo or mid == hi:
                break
            if self.J(mid) <= tgt * (1.0 - mid):
                lo = mid
            else:
                hi = mid
        tp = 0.5 * (lo + hi)
        return tp * (1.0 - s) / (1.0 - tp)

    def Sigma(self, B, s):
        """the slope map: Newton from the left on f(t) = J(t) - tgt (1 - t), which is concave with f(0) < 0, so the
        iterates increase monotonically to the smallest root t' (the root t = 1 of f is never reached)"""
        if B <= 0:
            return 0.0
        if s >= 1.0 or B >= (1.0 - s) * self.a:
            return math.inf
        tgt = B / (1.0 - s)
        u, lam1 = self.u, self.lam1
        t = 0.0
        for _ in range(100):
            ex = math.exp(-t * u)
            f = math.log(2.0 / (1.0 + ex)) - t * lam1 - tgt * (1.0 - t)
            fp = u * ex / (1.0 + ex) - lam1 + tgt
            if f >= 0.0 or fp <= 0.0:
                break
            tn = t - f / fp
            if tn <= t:
                break
            if tn >= 1.0:                      # rounding at a nearly irregular point: the map is infinite to working accuracy
                return math.inf
            t = tn
        if not (0.0 <= t < 1.0):
            return math.inf
        return t * (1.0 - s) / (1.0 - t)


class EnvSA:
    """semi-analytic envelope sequence; P is a CubeF (doubles) or an r29lib.CubeMP (mpmath)"""

    def __init__(self, P, J, verbose=False):
        self.P = P
        self.mpmode = hasattr(P, "mpmath")
        self.num = (lambda x: P.mpmath.mpf(x)) if self.mpmode else float
        self.inf = P.mpmath.inf if self.mpmode else math.inf
        self.a = P.a
        self.b = [P.a, P.a]                         # b_0 = a, b_1 = b^+(W_0, a) = a
        self.Bt = [None]
        self.m = [None]
        self.linear_root = [None]                   # whether b_{j+1} lies on the linear part of W_j
        self.gold_iters = 110 if self.mpmode else 90
        for j in range(1, J + 1):
            Bt, m = self._tangent(j)
            self.Bt.append(Bt)
            self.m.append(m)
            bj = self.b[j]
            Blin = self.a * m * bj / (self.a * m + 1)
            if Blin >= Bt:
                self.b.append(Blin)
                self.linear_root.append(True)
            else:                                   # the root of W_j(B) = 1 - B/a is on the curved part
                lo, hi = self.num(0), Bt
                for _ in range(int(P.mp.prec) + 8 if self.mpmode else 100):
                    mid = (lo + hi) / 2
                    if self.W(j, mid) + mid / self.a - 1 < 0:
                        lo = mid
                    else:
                        hi = mid
                self.b.append((lo + hi) / 2)
                self.linear_root.append(False)
            if verbose:
                print("   EnvSA level %d: Bt = %s  m = %s  b_%d = %s" % (j, Bt, m, j + 1, self.b[-1]), flush=True)

    def H(self, j, B):
        """H_j(B) = Sigma(B, W_{j-1}(B))"""
        return self.P.Sigma(B, self.W(j - 1, B))

    def W(self, j, B):
        if j == 0:
            return self.num(0)
        if B <= self.Bt[j]:
            return self.H(j, B)
        return 1 - self.m[j] * (self.b[j] - B)

    def _tangent(self, j):
        bj = self.b[j]

        def r(B):
            Hv = self.H(j, B)
            if Hv == self.inf:
                return -self.inf
            return (1 - Hv) / (bj - B)
        # H_j is convex, so r is quasi-concave on [0, b_j): golden section for its maximum
        gr = (math.sqrt(5.0) - 1) / 2 if not self.mpmode else (self.P.mpmath.sqrt(5) - 1) / 2
        lo, hi = self.num(0), bj * (1 - self.num(1) / 10 ** 12)
        x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        f1, f2 = r(x1), r(x2)
        for _ in range(self.gold_iters):
            if f1 > f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - gr * (hi - lo)
                f1 = r(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + gr * (hi - lo)
                f2 = r(x2)
        Bt = (lo + hi) / 2
        m = r(Bt)
        m0 = 1 / bj                                  # the value at B = 0 (the chord from the origin)
        if m0 >= m:
            return self.num(0), m0
        return Bt, m

    def M(self, j, g, n=4000):
        """max_B (B - W_j(B) g) by a scan plus a golden-section refinement (the function is concave in B)"""
        bj = self.b[j]

        def f(B):
            return B - self.W(j, B) * g
        gr = (math.sqrt(5.0) - 1) / 2 if not self.mpmode else (self.P.mpmath.sqrt(5) - 1) / 2
        lo, hi = self.num(0), bj
        x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        f1, f2 = f(x1), f(x2)
        for _ in range(self.gold_iters):
            if f1 > f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - gr * (hi - lo)
                f1 = f(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + gr * (hi - lo)
                f2 = f(x2)
        return max(f((lo + hi) / 2), f(bj), f(self.num(0)))
