#!/usr/bin/env python3
"""zrev.py -- the referee's own exponent-level library for the review of Z_REPORT.md.

Written from the definitions (R_REPORT.md sections 1-6, Z_REPORT.md sections 1-2); nothing is imported from the
workstream's libraries (experiments/workstreams/R/rlib.py, Z/zetalib.py, Q2/q2lib.py).

  Cube(u)            p_u, a, h, eps*, L, vartheta, c_*^2;  theta_na(e) and its derivative, through the parameter rho
  sigma_direct       Sigma(B, s) = sup_e [B - (1-s) theta_na(e)]/e  by DIRECT maximisation over e (golden section on a
                     unimodal function, after a coarse scan) -- slow, used for validation
  sigma              the same through the first-order condition (1-s)(theta - e theta') = B  (vectorised bisection)
  Chain              the cut orbit curves W_j (cut level s_t, restart b_0), B_t(j), m_j, b_j  (R_REPORT section 6)
"""
import math
import sys

import numpy as np

sys.dont_write_bytecode = True
LN2 = math.log(2.0)
INF = float('inf')


def kl(x, y):
    s = 0.0
    if x > 0:
        s += x * math.log(x / y)
    if x < 1:
        s += (1 - x) * math.log((1 - x) / (1 - y))
    return s


class Cube:
    def __init__(self, u):
        self.u = u
        self.p = 1.0 / (1.0 + math.exp(u))
        self.a = kl(self.p, 0.5)
        self.eps_star = kl(0.5, self.p)                      # = ln cosh(u/2)
        self.rho_h = 1.0 - math.log((1 + math.exp(u)) / 2.0) / u
        self.h = kl(self.rho_h, 0.5)
        assert abs(kl(self.rho_h, self.p) - self.h) < 1e-12
        # dual function J(t) = inf_e [(1-t) theta(e) + t e]; maximiser L:  theta'(h) = -L/(1-L)
        lam = math.log(self.rho_h / (1 - self.rho_h))        # theta' = lam/(lam + u) at rho
        r = -lam / (lam + u)
        self.L = r / (1 + r)
        # theta''(h): d/de [lam/(lam+u)] = u/(lam+u)^2 * dlam/drho * drho/de,  dlam/drho = 1/(rho(1-rho)), de/drho = lam + u
        th2 = u / (lam + u) ** 3 / (self.rho_h * (1 - self.rho_h))
        self.vartheta = th2 / (1 + r) ** 3
        self.cstar2 = 2 * math.pi ** 2 * self.h ** 2 * self.vartheta

    # ---- scalar theta_na ----
    def rho_of(self, e):
        if e <= 0:
            return self.p
        if e >= self.eps_star:
            return 0.5
        lo, hi = self.p, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if kl(mid, self.p) < e:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def theta(self, e):
        return kl(self.rho_of(e), 0.5)

    # ---- vectorised ----
    def e_of_rho(self, rho):
        p = self.p
        return rho * np.log(rho / p) + (1 - rho) * np.log((1 - rho) / (1 - p))

    def th_of_rho(self, rho):
        return LN2 + rho * np.log(rho) + (1 - rho) * np.log(1 - rho)

    def theta_v(self, e):
        """theta_na on an array of rates e >= 0."""
        e = np.asarray(e, dtype=np.float64)
        lo = np.full(e.shape, self.p)
        hi = np.full(e.shape, 0.5)
        ee = np.minimum(e, self.eps_star)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            less = self.e_of_rho(mid) < ee
            lo = np.where(less, mid, lo)
            hi = np.where(less, hi, mid)
        out = self.th_of_rho(0.5 * (lo + hi))
        out = np.where(e >= self.eps_star, 0.0, out)
        out = np.where(e <= 0, self.a, out)
        return np.maximum(out, 0.0)

    # ---- the slope map ----
    def sigma_direct(self, B, s, ngrid=4000):
        """sup_{e>0} [B - (1-s) theta(e)]/e by direct maximisation (scalar; coarse scan in rho + golden section).
        inf if B >= (1-s) a (infinite slope of theta at 0), 0 if B <= 0."""
        if s >= 1.0:
            return INF if B > 0 else 0.0
        if B >= (1 - s) * self.a:
            return INF
        if B <= 0:
            return 0.0
        p = self.p

        def f(rho):
            e = rho * math.log(rho / p) + (1 - rho) * math.log((1 - rho) / (1 - p))
            th = LN2 + rho * math.log(rho) + (1 - rho) * math.log(1 - rho)
            return (B - (1 - s) * th) / e
        # scan rho in (p, 1/2] on a grid that is fine near p (where e is small)
        ts = np.linspace(0.0, 1.0, ngrid + 1)[1:]
        rhos = p + (0.5 - p) * ts ** 2
        vals = [f(r) for r in rhos]
        i = int(np.argmax(vals))
        lo = rhos[max(i - 1, 0)] if i > 0 else p + (0.5 - p) * 1e-14
        hi = rhos[min(i + 1, ngrid - 1)]
        gr = (math.sqrt(5) - 1) / 2
        c, d = hi - gr * (hi - lo), lo + gr * (hi - lo)
        fc, fd = f(c), f(d)
        for _ in range(120):
            if fc < fd:
                lo, c, fc = c, d, fd
                d = lo + gr * (hi - lo)
                fd = f(d)
            else:
                hi, d, fd = d, c, fc
                c = hi - gr * (hi - lo)
                fc = f(c)
        best = max(fc, fd, vals[i])
        return max(best, B / self.eps_star, 0.0)             # e >= eps*: theta = 0, the ratio B/e is largest at eps*

    def _icpt(self, rho):
        """the intercept at zero of the tangent line of theta at e(rho):  theta - e theta',  theta' = lam/(lam+u)."""
        lam = np.log(rho / (1 - rho))
        return self.th_of_rho(rho) - self.e_of_rho(rho) * lam / (lam + self.u)

    def sigma_grad(self, B, s):
        """vectorised: (Sigma, dSigma/dB, dSigma/ds) with inf where B >= (1-s)a; for B <= 0: (0, 1/eps*, 0).
        First-order condition: the tangent line of (1-s) theta with intercept B, i.e. icpt(rho) = B/(1-s)."""
        B = np.asarray(B, dtype=np.float64)
        s = np.asarray(s, dtype=np.float64)
        B, s = np.broadcast_arrays(B, s)
        one = np.maximum(1.0 - s, 1e-300)
        tgt = B / one
        reg = (s < 1.0) & (B < (1.0 - s) * self.a)
        lo = np.full(B.shape, self.p)
        hi = np.full(B.shape, 0.5)
        for _ in range(64):
            mid = 0.5 * (lo + hi)
            with np.errstate(divide='ignore', invalid='ignore'):
                big = self._icpt(mid) > tgt                  # icpt decreases from a (rho = p) to 0 (rho = 1/2)
            lo = np.where(big, mid, lo)
            hi = np.where(big, hi, mid)
        rho = 0.5 * (lo + hi)
        lam = np.log(rho / (1 - rho))
        e = self.e_of_rho(rho)
        th = self.th_of_rho(rho)
        with np.errstate(divide='ignore', invalid='ignore'):
            sig = one * (-lam / (lam + self.u))
            dB = 1.0 / e
            ds = th / e
        pos = B > 0
        sig = np.where(reg, np.where(pos, sig, 0.0), INF)
        dB = np.where(reg, np.where(pos, dB, 1.0 / self.eps_star), INF)
        ds = np.where(reg, np.where(pos, ds, 0.0), INF)
        return sig, dB, ds

    def sig1(self, B, s):
        """scalar (Sigma, dSigma/dB, dSigma/ds) through the first-order condition, safeguarded Newton in rho."""
        if s >= 1.0 or B >= (1.0 - s) * self.a:
            return INF, INF, INF
        if B <= 0.0:
            return 0.0, 1.0 / self.eps_star, 0.0
        t = B / (1.0 - s)
        p, u = self.p, self.u
        lo, hi = p, 0.5
        rho = 0.5 * (lo + hi)
        log = math.log
        for _ in range(200):
            lam = log(rho / (1 - rho))
            e = rho * log(rho / p) + (1 - rho) * log((1 - rho) / (1 - p))
            th = LN2 + rho * log(rho) + (1 - rho) * log(1 - rho)
            f = th - e * lam / (lam + u) - t                 # decreasing in rho
            if f > 0:
                lo = rho
            else:
                hi = rho
            if hi - lo < 4e-16 * hi:
                break
            df = -e * u / ((lam + u) ** 2 * rho * (1 - rho))
            new = rho - f / df if df != 0 else 0.5 * (lo + hi)
            if not (lo < new < hi):
                new = 0.5 * (lo + hi)
            if abs(new - rho) < 1e-17:
                rho = new
                break
            rho = new
        lam = log(rho / (1 - rho))
        e = rho * log(rho / p) + (1 - rho) * log((1 - rho) / (1 - p))
        th = LN2 + rho * log(rho) + (1 - rho) * log(1 - rho)
        return (1.0 - s) * (-lam / (lam + u)), 1.0 / e, th / e

    def orbit1(self, B, j):
        """scalar (p_j(B), p_j'(B)) by the chain rule; (inf, inf) once irregular."""
        pp, dp = 0.0, 0.0
        for _ in range(j):
            sg, gB, gs = self.sig1(B, pp)
            if sg == INF:
                return INF, INF
            dp = gB + gs * dp
            pp = sg
        return pp, dp

    def sigma(self, B, s):
        return self.sigma_grad(B, s)[0]

    def J(self, t):
        lam = lambda v: math.log(2.0 / (1.0 + math.exp(-v)))
        return lam(t * self.u) - t * lam(self.u)


class Chain:
    """The cut orbit curves of R_REPORT section 6 for the cube: cut level s_t = L + dst, restart height b_0 = h + eps1.

    p_0 = 0, p_{j+1}(B) = Sigma(B, p_j(B));  case A (p_j(b_0) <= s_t): W_j = p_j on [0, b_0];  case B: B_t(j) with
    p_j(B_t(j)) = s_t, m_j = p_j'(B_t(j)-), W_j = p_j on [0, B_t(j)], = s_t + m_j (B - B_t(j)) beyond.
    b_{j+1} = sup{B in [0, b_j] : Sigma(B, W_j(B)) < inf} = min(b_j, E_j), E_j the root of W_j(B) = 1 - B/a on the linear
    part (the cube has infinite slope at zero: Sigma(B, s) < inf iff B < (1-s) a).
    """

    def __init__(self, cu, dst, eps1, J):
        self.cu = cu
        self.s_t = cu.L + dst
        self.b0 = cu.h + eps1
        assert cu.L < self.s_t < 1 - cu.h / cu.a, "s_t must lie in (L, 1 - h/a)"
        assert cu.h < self.b0 < (1 - self.s_t) * cu.a, "b_0 must lie in (h, (1 - s_t) a)"
        self.J = J
        self.cut = []            # None (case A) or (B_t(j), m_j)
        for j in range(J + 1):
            self.cut.append(self._cut(j))
        self.b = [self.b0]
        self.E = [None]
        self.Wtop = [0.0]        # W_j(b_j)
        for j in range(J):
            c = self.cut[j]
            if c is None:
                bn = self.b[j]
                self.E.append(None)
            else:
                Bt, m = c
                Ej = Bt + (1 - self.s_t - Bt / cu.a) / (m + 1 / cu.a)
                self.E.append(Ej)
                bn = min(self.b[j], Ej)
            self.b.append(bn)
            self.Wtop.append(float(self.W(j + 1, np.array([bn]))[0]))
        self.range_ok = all(w <= 1 + 1e-12 for w in self.Wtop)

    def orbit(self, B, j):
        """(p_j(B), p_j'(B)) on an array B (inf once irregular)."""
        B = np.asarray(B, dtype=np.float64)
        p = np.zeros(B.shape)
        dp = np.zeros(B.shape)
        for _ in range(j):
            sig, gB, gs = self.cu.sigma_grad(B, np.where(np.isfinite(p), p, 2.0))
            with np.errstate(invalid='ignore'):
                dp = np.where(np.isfinite(sig), gB + gs * dp, INF)
            p = sig
        return p, dp

    def _cut(self, j):
        """case A: None; case B: (B_t(j), m_j).  Root of p_j(B) = s_t: Newton from the right (p_j is convex and
        increasing, so the iterates decrease to the root), started at the previous cut point (or b_0), then a
        bisection polish; m_j is the derivative of p_j at the root (chain rule)."""
        cu = self.cu
        if cu.orbit1(self.b0, j)[0] <= self.s_t:
            return None
        prev = self.cut[j - 1] if j >= 1 else None
        hi = prev[0] if prev is not None else self.b0
        lo = cu.h
        B = hi
        for _ in range(100):
            pv, dp = cu.orbit1(B, j)
            if pv == INF:
                B = 0.5 * (lo + B)
                continue
            if pv > self.s_t:
                hi = B
            else:
                lo = B
            new = B - (pv - self.s_t) / dp
            if not (lo < new < hi):
                new = 0.5 * (lo + hi)
            if abs(new - B) <= 2e-16 * B:
                B = new
                break
            B = new
        # polish: make sure p_j(lo) <= s_t < p_j(hi) with hi - lo at rounding level; take the left point (left derivative)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if mid <= lo or mid >= hi:
                break
            if cu.orbit1(mid, j)[0] <= self.s_t:
                lo = mid
            else:
                hi = mid
            if hi - lo < 1e-16 * hi:
                break
        pv, dp = cu.orbit1(lo, j)
        return lo, dp

    def W(self, j, B):
        """W_j on an array B in [0, b_0]."""
        B = np.asarray(B, dtype=np.float64)
        c = self.cut[j]
        if c is None:
            return self.orbit(B, j)[0]
        Bt, m = c
        inner = self.orbit(np.minimum(B, Bt), j)[0]
        return np.where(B <= Bt, inner, self.s_t + m * (B - Bt))

    def Wd(self, j, B):
        """(W_j, W_j') on an array B in [0, b_0] (W_j is C^1 at the cut point: the continuation is the tangent line)."""
        B = np.asarray(B, dtype=np.float64)
        c = self.cut[j]
        if c is None:
            return self.orbit(B, j)
        Bt, m = c
        w, dw = self.orbit(np.minimum(B, Bt), j)
        return np.where(B <= Bt, w, self.s_t + m * (B - Bt)), np.where(B <= Bt, dw, m)

    def grid(self, j, N):
        """the grid family of W_j (Z_REPORT section 4): lines (B, W_j(B)), B in {i/N : 0 <= i <= N b_j} and B = b_j."""
        nb = int(math.floor(N * self.b[j] + 1e-12))
        Bs = np.arange(nb + 1, dtype=np.float64) / N
        if Bs[-1] < self.b[j]:
            Bs = np.append(Bs, self.b[j])
        Ws = np.clip(self.W(j, Bs), 0.0, None)
        return Bs, Ws

    def fine(self, j, npts=4001):
        """a fine sample of W_j on [0, b_j] including the cut point (for maxima over the curve)."""
        Bs = np.linspace(0.0, self.b[j], npts)
        c = self.cut[j]
        if c is not None and c[0] < self.b[j]:
            Bs = np.sort(np.append(Bs, c[0]))
        return Bs, self.W(j, Bs)


def M_env(Bs, Ws, g):
    """max over the sample of (B - W g); g scalar or array."""
    g = np.atleast_1d(np.asarray(g, dtype=np.float64))
    return (Bs[None, :] - Ws[None, :] * g[:, None]).max(axis=1)


# ----------------------------------------------------------------------------- two-sided envelopes of a convex curve
def curve_points(Bs, Ws, dWs):
    """For a convex function W sampled with derivatives at the increasing points Bs: the points of the curve (a lower
    family: max over them of an affine function increasing in B and decreasing in s is a LOWER bound of the supremum over
    the curve) and the curve points together with the intersection points of consecutive tangent lines (an UPPER family:
    on [B_i, B_{i+1}] the curve lies above both tangents, so the supremum over the curve of such an affine function is at
    most its maximum over this family)."""
    Bs = np.asarray(Bs, dtype=np.float64)
    Ws = np.asarray(Ws, dtype=np.float64)
    dWs = np.asarray(dWs, dtype=np.float64)
    d = dWs[1:] - dWs[:-1]
    num = Ws[1:] - Ws[:-1] + dWs[:-1] * Bs[:-1] - dWs[1:] * Bs[1:]
    with np.errstate(divide='ignore', invalid='ignore'):
        Bx = np.where(np.abs(d) > 1e-300, -num / d, 0.5 * (Bs[1:] + Bs[:-1]))
    Bx = np.clip(Bx, Bs[:-1], Bs[1:])
    sx = np.minimum(Ws[:-1] + dWs[:-1] * (Bx - Bs[:-1]), Ws[1:] + dWs[1:] * (Bx - Bs[1:]))   # rounding-safe: the lower one
    sx = np.clip(sx, Ws[:-1], Ws[1:])          # the convex nondecreasing curve lies in [W_i, W_{i+1}] on the cell
    return (Bs, Ws), (np.concatenate([Bs, Bx]), np.concatenate([Ws, sx]))


def inf_phi(cu, g, PB, Ps, iters=75, lo0=1e-12, hi0=1.0 - 1e-12):
    """inf over phi in (0, 1) of  G(phi) = max_k [(1 - phi) B_k + (1 - s_k) phi theta(g/phi)],  for an ARRAY g.
    G is convex in phi (a maximum of convex functions, Lemma Z1a), so a golden-section search on [lo0, hi0] finds its
    minimum; by the Lipschitz bound of Lemma Z1a the infimum over (0, 1) is at most a * 1e-12 below it.
    Returns (values, phis) -- every value is G at an actual phi, hence an upper bound of the infimum of G."""
    g = np.atleast_1d(np.asarray(g, dtype=np.float64))
    one_s = 1.0 - Ps

    def G(ph):
        c = ph * cu.theta_v(g / ph)
        out = np.empty(g.shape)
        step = max(1, int(4e6 // max(len(PB), 1)))
        for i in range(0, len(g), step):
            out[i:i + step] = ((1.0 - ph[i:i + step])[:, None] * PB[None, :] + c[i:i + step][:, None] * one_s[None, :]).max(axis=1)
        return out
    lo = np.full(g.shape, lo0)
    hi = np.full(g.shape, hi0)
    gr = (math.sqrt(5) - 1) / 2
    c_ = hi - gr * (hi - lo)
    d_ = lo + gr * (hi - lo)
    fc, fd = G(c_), G(d_)
    best = np.minimum(fc, fd)
    bphi = np.where(fc < fd, c_, d_)
    for _ in range(iters):
        left = fc < fd
        hi = np.where(left, d_, hi)
        lo = np.where(left, lo, c_)
        nc = hi - gr * (hi - lo)
        nd = lo + gr * (hi - lo)
        # reuse one of the two inner points
        c_new = np.where(left, nc, d_)
        d_new = np.where(left, c_, nd)
        f_new = G(np.where(left, nc, nd))
        fc, fd = np.where(left, f_new, fd), np.where(left, fc, f_new)
        c_, d_ = c_new, d_new
        m = np.minimum(fc, fd)
        upd = m < best
        bphi = np.where(upd, np.where(fc < fd, c_, d_), bphi)
        best = np.where(upd, m, best)
    return best, bphi
