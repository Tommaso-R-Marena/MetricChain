#!/usr/bin/env python3
"""Referee's own library for the review of docs/workstreams/Z_ADDENDUM.md.

Written from the definitions in R_REPORT.md / Z_ADDENDUM.md; it does NOT import rlib.py or zetalib.py.
Floating point throughout: nothing here is a certified bound.

Objects
  Pair            theta (direct definition), J, dJ, d2J; a, h, L, vartheta = theta_hint''(0), cstar2;
                  the slope map  Sigma(B, s) = sup_{e>0} [B - (1 - s) theta(e)]/e  in two independent ways:
                    sigma()/sigma_grad()/sigma_vec():  Sigma = t'(1 - s)/(1 - t'),  J(t')/(1 - t') = B/(1 - s)   (derived by
                                                       the referee: sigma' = (1-s) r is the least number with
                                                       inf_e [theta(e) + r e] >= B/(1-s), and inf_e[theta + r e] = J(t)/(1-t),
                                                       r = t/(1-t));
                    sigma_direct():                    the supremum over e computed from theta itself (grid + golden section).
  lower_hull()    lower convex envelope of grid values (monotone chain) and a brute-force O(N^2) version for testing it
  EnvSeq          the envelope sequence in "structural" form: W_{j+1} = Sigma(., W_j(.)) up to the tangency point B_t(j+1),
                  then the tangent line through (b_{j+1}, 1).  (This uses the description of the envelope in the proof of
                  Lemma A10; GridEnv below does not.)
  GridEnv         the envelope sequence from the definition on grids: W_{j+1} = lower convex envelope of the grid values
                  of min(1, Sigma(B, W_j(B))) on [0, b_{j+1}],  b_{j+1} = sup{B <= b_j : Sigma(B, W_j(B)) < infinity}.
Both pairs used here (cube, Gaussian) have infinite slope of theta at zero, so (B, s) is regular iff s < 1, B < (1 - s) a.
"""
import math

import numpy as np

LN2 = math.log(2.0)
GOLD = 0.5 * (math.sqrt(5.0) - 1.0)


def kl(x, y):
    """KL(Bernoulli(x) || Bernoulli(y))"""
    out = 0.0
    if x > 0.0:
        out += x * math.log(x / y)
    if x < 1.0:
        out += (1.0 - x) * math.log((1.0 - x) / (1.0 - y))
    return out


class Pair:
    name = "abstract"
    a = None

    # ---- to be supplied: theta(e), J(t), dJ(t), d2J(t), Jv(t) (numpy) -------------------------------------------
    def setup(self):
        lo, hi = 1e-14, 1.0 - 1e-14
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if self.dJ(mid) > 0:
                lo = mid
            else:
                hi = mid
        self.L = 0.5 * (lo + hi)
        self.h = self.J(self.L)
        self.vartheta = -1.0 / self.d2J(self.L)
        self.cstar2 = 2.0 * math.pi ** 2 * self.h ** 2 * self.vartheta
        return self

    def regular(self, B, s):
        return s < 1.0 and B < (1.0 - s) * self.a

    # ---- the slope map through J ---------------------------------------------------------------------------------
    def tprime(self, y):
        """the solution t in [0, 1) of J(t)/(1 - t) = y, 0 <= y < a  (safeguarded Newton)"""
        if y <= 0.0:
            return 0.0
        lo, hi = 0.0, 1.0
        t = 0.5
        for _ in range(200):
            om = 1.0 - t
            Jt = self.J(t)
            q = Jt / om - y
            if q > 0:
                hi = t
            else:
                lo = t
            dq = (self.dJ(t) * om + Jt) / (om * om)
            tn = t - q / dq if dq > 0 else 0.5 * (lo + hi)
            if not (lo < tn < hi):
                tn = 0.5 * (lo + hi)
            if abs(tn - t) < 2e-16 or hi - lo < 4e-16:
                t = tn
                break
            t = tn
        return t

    def sigma(self, B, s):
        if B <= 0.0 and s <= 1.0:
            return 0.0
        if not self.regular(B, s):
            return math.inf
        tp = self.tprime(B / (1.0 - s))
        return tp * (1.0 - s) / (1.0 - tp)

    def sigma_grad(self, B, s):
        """(Sigma, dSigma/dB, dSigma/ds) at a regular point: 1/e* and theta(e*)/e*, e* the maximiser"""
        tp = self.tprime(B / (1.0 - s))
        Jt, dJt = self.J(tp), self.dJ(tp)
        e = Jt + (1.0 - tp) * dJt
        th = Jt - tp * dJt
        return tp * (1.0 - s) / (1.0 - tp), 1.0 / e, th / e

    def sigma_vec(self, B, s):
        B = np.asarray(B, dtype=float)
        s = np.asarray(s, dtype=float)
        reg = (s < 1.0) & (B < (1.0 - s) * self.a)
        y = np.where(reg, B / np.where(reg, 1.0 - s, 1.0), 0.0)
        lo = np.zeros(y.shape)
        hi = np.ones(y.shape)
        for _ in range(62):
            mid = 0.5 * (lo + hi)
            ok = self.Jv(mid) / (1.0 - mid) <= y
            lo = np.where(ok, mid, lo)
            hi = np.where(ok, hi, mid)
        tp = 0.5 * (lo + hi)
        out = tp * (1.0 - s) / (1.0 - tp)
        return np.where(reg, out, np.inf)

    # ---- the slope map from theta itself -------------------------------------------------------------------------
    def sigma_direct(self, B, s, emax=None, n=4000):
        """sup_{e > 0} [B - (1 - s) theta(e)]/e by a logarithmic grid and golden-section refinement (>= 0: e -> infinity)"""
        if not self.regular(B, s):
            return math.inf
        emax = emax or self.e_zero * 4.0
        f = lambda e: (B - (1.0 - s) * self.theta(e)) / e
        es = np.exp(np.linspace(math.log(1e-12), math.log(emax), n))
        vals = np.array([f(e) for e in es])
        k = int(np.argmax(vals))
        lo, hi = es[max(k - 1, 0)], es[min(k + 1, n - 1)]
        for _ in range(100):
            m1 = hi - GOLD * (hi - lo)
            m2 = lo + GOLD * (hi - lo)
            if f(m1) < f(m2):
                lo = m1
            else:
                hi = m2
        return max(0.0, f(0.5 * (lo + hi)), float(vals[k]))

    def J_direct(self, t, n=4000):
        """inf_{e>0} [(1 - t) theta(e) + t e] from theta itself"""
        f = lambda e: (1.0 - t) * self.theta(e) + t * e
        es = np.exp(np.linspace(math.log(1e-12), math.log(self.e_zero * 4.0), n))
        vals = np.array([f(e) for e in es])
        k = int(np.argmin(vals))
        lo, hi = es[max(k - 1, 0)], es[min(k + 1, n - 1)]
        for _ in range(100):
            m1 = hi - GOLD * (hi - lo)
            m2 = lo + GOLD * (hi - lo)
            if f(m1) > f(m2):
                lo = m1
            else:
                hi = m2
        return min(f(0.5 * (lo + hi)), float(vals[k]))

    # ---- fixed points, hinted exponent ---------------------------------------------------------------------------
    def t1(self, B):
        """the solution t in [0, L] of J(t) = B, 0 <= B <= h"""
        lo, hi = 0.0, self.L
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if self.J(mid) < B:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def theta_hint_sup(self, g, n=200001):
        """sup_t [J(t) - t g] on a grid of [0, 1] with a parabolic refinement (independent of the closed form)"""
        t = np.linspace(0.0, 1.0 - 1e-12, n)
        v = self.Jv(t) - t * g
        k = int(np.argmax(v))
        if 0 < k < n - 1:
            lo, hi = t[k - 1], t[k + 1]
            for _ in range(100):
                m1 = hi - GOLD * (hi - lo)
                m2 = lo + GOLD * (hi - lo)
                if self.J(m1) - m1 * g < self.J(m2) - m2 * g:
                    lo = m1
                else:
                    hi = m2
            tm = 0.5 * (lo + hi)
            return max(float(v[k]), self.J(tm) - tm * g)
        return float(v[k])

    def orbit(self, B, n):
        """p_0 = 0, p_{i+1} = Sigma(B, p_i); list of length n + 1 (inf once irregular)"""
        out = [0.0]
        for _ in range(n):
            s = out[-1]
            out.append(self.sigma(B, s) if math.isfinite(s) else math.inf)
        return out

    def orbit_with_slope(self, B, n):
        p, dp = 0.0, 0.0
        for _ in range(n):
            if not self.regular(B, p):
                return math.inf, math.inf
            p, gB, gs = self.sigma_grad(B, p)
            dp = gB + gs * dp
        return p, dp


class Cube(Pair):
    """theta_na(e) = KL(rho || 1/2) at the rho in [p_u, 1/2] with KL(rho || p_u) = e, p_u = 1/(1 + e^u); 0 for e >= eps*.
    J(t) = min_rho [(1 - t) KL(rho||1/2) + t KL(rho||p_u)] = -ln sum_x (1/2)^(1-t) p_u(x)^t
         = (1 - t) ln 2 - ln(1 + e^{t u}) + t ln(1 + e^u)        (referee's derivation; equals Lambda(tu) - t Lambda(u))."""

    def __init__(self, u):
        self.u = float(u)
        self.name = "cube u = %g" % u
        self.pu = 1.0 / (1.0 + math.exp(u))
        self.a = kl(self.pu, 0.5)
        self.epsstar = kl(0.5, self.pu)
        self.e_zero = self.epsstar
        self.lnc = math.log1p(math.exp(u))
        self.Lam_u = math.log(2.0 / (1.0 + math.exp(-u)))

    def theta(self, e):
        if e >= self.epsstar:
            return 0.0
        lo, hi = self.pu, 0.5
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if kl(mid, self.pu) <= e:
                lo = mid
            else:
                hi = mid
        return kl(0.5 * (lo + hi), 0.5)

    def J(self, t):
        return (1.0 - t) * LN2 - math.log1p(math.exp(t * self.u)) + t * self.lnc

    def Jv(self, t):
        return (1.0 - t) * LN2 - np.log1p(np.exp(t * self.u)) + t * self.lnc

    def dJ(self, t):
        z = math.exp(t * self.u)
        return -LN2 - self.u * z / (1.0 + z) + self.lnc

    def d2J(self, t):
        z = math.exp(t * self.u)
        return -self.u ** 2 * z / (1.0 + z) ** 2

    def theta_hint(self, g):
        rho = (self.Lam_u + g) / self.u
        return kl(rho, 0.5) if rho < 0.5 else 0.0


class Gauss(Pair):
    """theta(e) = (1 - sqrt e)^2 for e < 1, 0 beyond;  J(t) = t - t^2;  Sigma(B, s) = B (1 - s)/(1 - s - B)."""
    name = "Gaussian pair"
    a = 1.0
    e_zero = 1.0
    epsstar = 1.0

    def theta(self, e):
        return (1.0 - math.sqrt(e)) ** 2 if e < 1.0 else 0.0

    def J(self, t):
        return t - t * t

    def Jv(self, t):
        return t - t * t

    def dJ(self, t):
        return 1.0 - 2.0 * t

    def d2J(self, t):
        return -2.0

    def tprime(self, y):
        return y

    def sigma_vec(self, B, s):
        B = np.asarray(B, dtype=float)
        s = np.asarray(s, dtype=float)
        reg = (s < 1.0) & (B < (1.0 - s) * self.a)
        den = np.where(reg, 1.0 - s - B, 1.0)
        return np.where(reg, B * (1.0 - s) / den, np.inf)

    def theta_hint(self, g):
        return 0.25 * (1.0 - g) ** 2 if g < 1.0 else 0.0


# -----------------------------------------------------------------------------------------------------------------
#  lower convex envelopes of grid values
# -----------------------------------------------------------------------------------------------------------------
def lower_hull(x, y):
    """indices of the vertices of the lower convex hull of the points (x_i, y_i), x increasing (monotone chain)"""
    hull = []
    for i in range(len(x)):
        while len(hull) >= 2:
            i1, i2 = hull[-2], hull[-1]
            # i2 is dropped if it is on or above the chord from i1 to i
            if (y[i2] - y[i1]) * (x[i] - x[i1]) >= (y[i] - y[i1]) * (x[i2] - x[i1]):
                hull.pop()
            else:
                break
        hull.append(i)
    return hull


def lower_env(x, y):
    hull = lower_hull(x, y)
    return np.interp(x, x[hull], y[hull]), hull


def lower_env_bruteforce(x, y):
    """the largest convex minorant at the grid points, from the definition: min over chords spanning the point"""
    n = len(x)
    out = np.array(y, dtype=float)
    for i in range(n):
        best = y[i]
        for j in range(i):
            for k in range(i + 1, n):
                v = y[j] + (y[k] - y[j]) * (x[i] - x[j]) / (x[k] - x[j])
                if v < best:
                    best = v
        out[i] = best
    return out


# -----------------------------------------------------------------------------------------------------------------
#  the envelope sequence, structural form
# -----------------------------------------------------------------------------------------------------------------
class EnvSeq:
    """W_0 = 0 on [0, a].  Level j >= 1 is stored as (b_j, Bt_j, wt_j, m_j):
         W_j(B) = Sigma(B, W_{j-1}(B))  for B <= Bt_j,      W_j(B) = wt_j + m_j (B - Bt_j)  for Bt_j <= B <= b_j,   W_j(b_j) = 1,
       where b_j is the root of W_{j-1}(B) = 1 - B/a and Bt_j the last point at which the tangent line of
       H_{j-1} = Sigma(., W_{j-1}(.)) has a value <= 1 at b_j  (Bt_j = 0 and the chord from the origin if there is none)."""

    def __init__(self, pair, J, verbose=False):
        self.P = pair
        self.b = [pair.a]
        self.Bt = [None]
        self.wt = [None]
        self.m = [None]
        self.tan_err = [0.0]
        for _ in range(J):
            self._step()
            if verbose and len(self.b) % 50 == 0:
                print("   ... level", len(self.b) - 1, flush=True)

    def W(self, j, B):
        """(W_j(B), W_j'(B)) for 0 <= B <= b_j"""
        i = j
        while i >= 1 and B <= self.Bt[i]:
            i -= 1
        if i == 0:
            w, dw = 0.0, 0.0
        else:
            w, dw = self.wt[i] + self.m[i] * (B - self.Bt[i]), self.m[i]
        P = self.P
        for _ in range(i + 1, j + 1):
            S, SB, Ss = P.sigma_grad(B, w)
            w, dw = S, SB + Ss * dw
        return w, dw

    def H(self, j, B):
        """(H_j(B), H_j'(B)), H_j = Sigma(., W_j(.)); (inf, inf) where not regular"""
        w, dw = self.W(j, B)
        if not self.P.regular(B, w):
            return math.inf, math.inf
        S, SB, Ss = self.P.sigma_grad(B, w)
        return S, SB + Ss * dw

    def _step(self):
        P = self.P
        a = P.a
        j = len(self.b) - 1
        # the next top: the root of W_j(B) = 1 - B/a  (W_j(b_j) = 1 > 1 - b_j/a for j >= 1)
        if j == 0:
            bn = a
        elif self.wt[j] <= 1.0 - self.Bt[j] / a:
            bn = (1.0 - self.wt[j] + self.m[j] * self.Bt[j]) / (self.m[j] + 1.0 / a)
        else:
            lo, hi = 0.0, self.Bt[j]
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if mid <= lo or mid >= hi:
                    break
                if self.W(j, mid)[0] <= 1.0 - mid / a:
                    lo = mid
                else:
                    hi = mid
            bn = 0.5 * (lo + hi)
        bn = min(bn, self.b[j])
        # the tangency point: phi(B) = H_j(B) + H_j'(B) (bn - B) - 1 is nondecreasing; Bt = sup{phi <= 0}
        lo, hi = 0.0, bn
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if mid <= lo or mid >= hi:
                break
            Hm, dHm = self.H(j, mid)
            if math.isfinite(Hm) and Hm + dHm * (bn - mid) - 1.0 <= 0.0:
                lo = mid
            else:
                hi = mid
        Bt = lo
        if Bt > 0.0:
            wt, dH = self.H(j, Bt)
        else:
            wt, dH = 0.0, float("nan")
        m = (1.0 - wt) / (bn - Bt)
        self.b.append(bn)
        self.Bt.append(Bt)
        self.wt.append(wt)
        self.m.append(m)
        self.tan_err.append(abs(m - dH) / m if Bt > 0.0 else 0.0)

    def Wvec(self, j, B):
        """W_j on an array of points of [0, b_j]"""
        B = np.asarray(B, dtype=float)
        w = np.zeros(B.shape)
        for l in range(1, j + 1):
            mask = B <= self.Bt[l]
            lin = self.wt[l] + self.m[l] * (B - self.Bt[l])
            S = np.zeros(B.shape)
            if mask.any():
                S[mask] = self.P.sigma_vec(B[mask], w[mask])
            w = np.where(mask, S, lin)
        return w

    def M(self, k, g):
        """M_{W_k, b_k}(g) = max_{B <= b_k} [B - W_k(B) g]  (concave in B: bisection on W_k'(B) = 1/g), and the maximiser"""
        if k == 0:
            return self.b[0], self.b[0]
        if g <= 0.0 or self.m[k] * g <= 1.0:          # the slope never reaches 1/g: the maximum is at the top
            return self.b[k] - g, self.b[k]           # W_k(b_k) = 1
        lo, hi = 0.0, self.Bt[k]
        if hi <= 0.0:
            return 0.0, 0.0
        if self.W(k, hi)[1] * g <= 1.0:               # slope 1/g is reached at the junction with the linear part
            Bs = hi
        else:
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if mid <= lo or mid >= hi:
                    break
                if self.W(k, mid)[1] * g <= 1.0:
                    lo = mid
                else:
                    hi = mid
            Bs = 0.5 * (lo + hi)
        return max(0.0, Bs - self.W(k, Bs)[0] * g), Bs


# -----------------------------------------------------------------------------------------------------------------
#  the envelope sequence from the definition, on grids
# -----------------------------------------------------------------------------------------------------------------
class GridEnv:
    """curves[j] = (x, W) with x a grid of [0, b_j].  grid: 'uniform' or 'quad' (finer near the top)."""

    def __init__(self, pair, J, NG=4000, grid="uniform"):
        self.P = pair
        self.NG = NG
        self.grid = grid
        a = pair.a
        x = self._grid(a)
        self.curves = [(x, np.zeros(NG + 1))]
        self.b = [a]
        self.hull_sizes = [2]
        for _ in range(J):
            self._step()

    def _grid(self, b):
        s = np.linspace(0.0, 1.0, self.NG + 1)
        if self.grid == "quad":
            s = 1.0 - (1.0 - s) ** 2
        return b * s

    def _step(self):
        P = self.P
        a = P.a
        x, W = self.curves[-1]
        g = W - (1.0 - x / a)                      # nondecreasing; Sigma(B, W(B)) < infinity iff g < 0
        if g[-1] < 0:
            bn = x[-1]
        else:
            k = int(np.argmax(g >= 0))
            if k == 0:
                bn = x[0]
            else:
                bn = x[k - 1] - g[k - 1] * (x[k] - x[k - 1]) / (g[k] - g[k - 1])
        bn = min(bn, self.b[-1])
        xn = self._grid(bn)
        Wi = np.interp(xn, x, W)
        f = np.minimum(1.0, P.sigma_vec(xn, Wi))  # = 1 where Sigma = infinity
        f[0] = 0.0
        f[-1] = 1.0                                # infinite slope at zero: Sigma = infinity at the top
        e, hull = lower_env(xn, f)
        # the value at the right end is the left limit of the envelope: the last hull edge is a line ending at (bn, 1)
        self.curves.append((xn, e))
        self.b.append(bn)
        self.hull_sizes.append(len(hull))

    def W(self, j, B):
        x, W = self.curves[j]
        return np.interp(B, x, W)
