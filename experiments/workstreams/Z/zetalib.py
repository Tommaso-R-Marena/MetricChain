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


# ---------------------------------------------------------------------------------------------------------------
#  families for exact nests (the framework of q2lib: objects with costs(d, xs, ld), Ebound(d, x, Lam), B, sigma, xmin)
# ---------------------------------------------------------------------------------------------------------------
import numpy as np     # noqa: E402

LN2 = math.log(2.0)


def theta_vec(u, e):
    """theta_na of the cube at an array of rates (vectorised bisection)"""
    e = np.asarray(e, dtype=float)
    pu = 1.0 / (1.0 + math.exp(u))

    def kl(x, y):
        return x * np.log(x / y) + (1 - x) * np.log((1 - x) / (1 - y))

    lo = np.full(e.shape, pu)
    hi = np.full(e.shape, 0.5)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        ok = kl(mid, pu) <= e
        lo = np.where(ok, mid, lo)
        hi = np.where(ok, hi, mid)
    out = kl(0.5 * (lo + hi), 0.5)
    return np.where(e >= kl(0.5, pu), 0.0, out)


class SatFlat(Q2.FamBase):
    """a family whose certified cost is exactly d B at every accuracy >= xmin (it saturates the flat type; error 0)"""
    name = 'saturating flat base'

    def __init__(self, B, xmin=1.0):
        self.B, self.xmin = B, xmin

    def Ebound(self, d, x, Lam):
        return 0.0

    def costs(self, d, xs, ld):
        return np.full(np.asarray(xs, dtype=float).shape, d * self.B)


class ZLevelFam(Q2.FamBase):
    """Z_j[inner] of Z_REPORT section 4: one level of Lemma Z2 over `inner` (type: the lines `lines`, least accuracy
    <= 1), the outer block chosen by the proxy Pi_j; enumeration for d <= d_min.  Flat majorant: B = bnext."""
    name = 'Z level'

    def __init__(self, ev, inner, lines, lines_next, bnext, N, st):
        self.ev, self.cu, self.inner, self.N, self.st = ev, ev.cu, inner, N, st
        self.u = ev.u
        self.LB = np.array([B for (B, s) in lines])
        self.Ls = np.array([s for (B, s) in lines])
        self.NB = np.array([B for (B, s) in lines_next])
        self.Ns = np.array([s for (B, s) in lines_next])
        self.B = bnext
        self.dm = dmin(self.u)
        self.xmin = X0(self.u, N) + 1.0
        self.nlev = 0
        self.loss = []                 # (d, xhat, ln C_max - type of the next curve): the measured loss of a level

    def Ebound(self, d, x, Lam):
        return (self.inner.Ebound(d, 1.0, Lam + Q2.qSb(self.cu, d, Lam)) + Q2.ell0(self.cu, d, Lam) + X0(self.u, d)
                + self.dm * LN2 + 2.0)

    def type_major(self, d, x):
        return float(np.max(d * self.NB - self.Ns * x))

    def design(self, d, y):
        """the outer block: a minimiser of Pi_j(n_o) = max_lines [(d - n_o) B + (1 - s) n_o theta(y/n_o)] (a scan over all n_o
        for d <= 1500, over about 1200 candidates beyond: any n_o gives a valid level)"""
        hi = d - self.dm + 1
        if hi <= 1500:
            cand = np.arange(1, hi + 1)
        else:
            cand = np.unique(np.concatenate((np.arange(1, 200), np.linspace(1, hi, 1000).astype(int), [hi])))
        th = theta_vec(self.u, y / cand)
        pi = np.max((d - cand)[:, None] * self.LB[None, :] + (1 - self.Ls)[None, :] * (cand * th)[:, None], axis=1)
        k = int(np.argmin(pi))
        return int(cand[k]), float(th[k]), float(pi[k])

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        assert d <= self.N and np.all(xs >= self.xmin - 1e-12)
        out = np.empty(xs.shape)
        Lam = -ld + d * LN2
        for i, xh in enumerate(xs):
            if d <= self.dm:
                out[i] = d * LN2
            else:
                y = xh - X0(self.u, d)
                n_o, th, pi = self.design(d, y)
                lth = math.log(3.0 * (n_o + 1)) + 2 * self.u + math.exp(self.u) + y
                r = Q2.level_U(self.ev, d, n_o, lth, n_o * th, ld, self.inner)
                self.nlev += 1
                self.st.add('Z3: accuracy', r['c']['xout'], xh + 1e-9, (d, xh))
                self.st.add('Z3: (U-infinity)', r['lC'], pi + Q2.ell0(self.cu, d, Lam) + self.inner.Ebound(d, 1.0, Lam + Q2.qSb(self.cu, d, Lam)),
                            (d, xh, n_o))
                out[i] = r['lC']
                self.loss.append((d, float(xh), r['lC'] - self.type_major(d, float(xh))))
            self.st.add('Z3: the type', out[i], self.type_major(d, float(xh)) + self.Ebound(d, float(xh), Lam), (d, float(xh), ld))
        return out


class ZHatFam(Q2.FamBase):
    """Zhat[inner; alpha] of Z_REPORT section 5: the chain T[Z; alpha, m] below the accuracy X of the level family, the
    level family above.  Type: the lines of the next curve, error = chain error + X + 1."""
    name = 'Z hat'

    def __init__(self, zfam, chainfam, st):
        self.z, self.ch, self.st = zfam, chainfam, st
        self.B = zfam.B
        self.xmin = chainfam.xmin

    def Ebound(self, d, x, Lam):
        return self.ch.Ebound(d, x, Lam) + self.z.xmin + 1.0

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        out = np.empty(xs.shape)
        Lam = -ld + d * LN2
        for i, x in enumerate(xs):
            if x < self.z.xmin:
                out[i] = float(self.ch.costs(d, np.array([max(x, self.ch.xmin)]), ld)[0])
            else:
                out[i] = float(self.z.costs(d, np.array([x]), ld)[0])
            self.st.add('Z4: the type of the combined family', out[i], self.z.type_major(d, float(x)) + self.Ebound(d, float(x), Lam),
                        (d, float(x), ld))
        return out


# ---------------------------------------------------------------------------------------------------------------
#  the envelope sequence (Z_REPORT section 2): the best convex sub-solution of the slope map, started at b_0 = a
# ---------------------------------------------------------------------------------------------------------------
class EnvZ:
    """W_0 = 0 on [0, a];  b_{j+1} = the root of W_j(B) = 1 - B/a;  W_{j+1} = the lower convex envelope of
    min(1, Sigma(B, W_j(B))) on [0, b_{j+1}].  Floating point on a grid of NG + 1 points per curve (finer near the top):
    an approximation [N].  Same interface as ChainZ (b, W, grid, theta, h, a, P, range_ok)."""

    def __init__(self, u, J, NG=4000):
        self.u = u
        self.P = rlib.Cube(u).setup()
        self.h, self.L, self.a = self.P.h, self.P.L, self.P.a
        self.lamu = math.log(2 / (1 + math.exp(-u)))
        self.b0 = self.a
        self.curves, self.b = self._sequence(J + 2, NG)
        self.range_ok = all(float(np.max(W)) <= 1.0 + 1e-12 and float(np.min(np.diff(W))) >= -1e-12 for (_, W) in self.curves)
        self.worstW = max(float(np.max(W)) for (_, W) in self.curves)

    def _J(self, t):
        return np.log(2 / (1 + np.exp(-t * self.u))) - t * self.lamu

    def sigma_vec(self, B, s):
        """Sigma(B, s) = t'(1 - s)/(1 - t'),  Q(t') = B/(1 - s),  Q = J/(1 - t)  (vectorised bisection); inf where not regular"""
        B = np.asarray(B, dtype=float)
        s = np.asarray(s, dtype=float)
        reg = (s < 1.0) & (B < (1.0 - s) * self.a)
        tgt = np.where(reg, B / np.maximum(1.0 - s, 1e-300), 0.0)
        lo = np.zeros(B.shape)
        hi = np.full(B.shape, 1.0 - 1e-15)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            ok = self._J(mid) / (1.0 - mid) <= tgt
            lo = np.where(ok, mid, lo)
            hi = np.where(ok, hi, mid)
        tp = 0.5 * (lo + hi)
        return np.where(reg, tp * (1.0 - s) / (1.0 - tp), np.inf)

    @staticmethod
    def lower_convex_envelope(x, y):
        hull = []
        for i in range(len(x)):
            while len(hull) >= 2:
                i1, i2 = hull[-2], hull[-1]
                if (y[i2] - y[i1]) * (x[i] - x[i1]) >= (y[i] - y[i1]) * (x[i2] - x[i1]):
                    hull.pop()
                else:
                    break
            hull.append(i)
        return np.interp(x, x[hull], y[hull])

    def _sequence(self, J, NG):
        a = self.a
        b = a
        x = np.linspace(0.0, b, NG + 1)
        W = np.zeros(NG + 1)
        tops, curves = [b], [(x, W)]
        for _ in range(J):
            g = W - (1.0 - x / a)                       # increasing; its root is the next top
            if g[-1] <= 0:
                bn = x[-1]
            else:
                k = int(np.argmax(g > 0))
                x0, x1, g0, g1 = x[k - 1], x[k], g[k - 1], g[k]
                bn = x0 - g0 * (x1 - x0) / (g1 - g0)
            bn = min(bn, b)
            xn = bn * (1.0 - (1.0 - np.linspace(0.0, 1.0, NG + 1)) ** 2)           # finer near the top
            f = np.minimum(1.0, self.sigma_vec(xn, np.interp(xn, x, W)))
            f[-1] = 1.0
            e = self.lower_convex_envelope(xn, f)
            e[-1] = min(1.0, e[-2] + (e[-2] - e[-3]) * (xn[-1] - xn[-2]) / (xn[-2] - xn[-3]))   # the limit at the right end
            e = np.clip(e, 0.0, 1.0)
            b, x, W = bn, xn, e
            tops.append(b)
            curves.append((x, W))
        return curves, tops

    def W(self, j, B):
        x, W = self.curves[j]
        return float(np.interp(B, x, W))

    def grid(self, j, N):
        Bs = [i / N for i in range(int(math.floor(N * self.b[j] + 1e-12)) + 1)]
        if Bs[-1] < self.b[j]:
            Bs.append(self.b[j])
        x, W = self.curves[j]
        return [(B, float(min(1.0, max(0.0, np.interp(B, x, W))))) for B in Bs]

    def theta(self, e):
        return self.P.theta_na(e)


def make_chain(mode, u, J, eps1=0.003, dst=0.05, NG=4000):
    """'env': the envelope sequence from b_0 = a;  'cut': the cut orbit curves restarted at b_0 = h + eps1"""
    return EnvZ(u, J, NG) if mode == "env" else ChainZ(u, dst, eps1, J)
