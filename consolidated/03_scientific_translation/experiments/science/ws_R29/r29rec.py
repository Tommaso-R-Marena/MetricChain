#!/usr/bin/env python3
"""r29rec.py -- own routines of workstream R29, third part: one step of the level recursion on T = theta_na.

    R[theta](g) = inf_{0<phi<1, 0<=beta<=g} F(phi, beta; g),      mu = phi theta((g - beta)/phi),  S(y) = y + theta(y),
    F = (1 - phi) max( S(beta/(1-phi)), S(mu/(1-phi)) )   if beta <= mu      (S is convex, so the supremum over gamma in
    F = mu + (1 - phi) theta(beta/(1 - phi))               if beta >  mu       [beta, mu] is at an end point).

Every (phi, beta) gives an upper bound of R[theta](g); a minimiser can only err upwards.  The minimiser here:
a scan on a nonuniform grid (dense near phi -> 1 and near beta -> 0) with a tabulated theta, then, from the lowest
local minima of the scan and from the edge beta = 0, a *moving zoom* in the coordinates (logit phi, logit beta/g) with
the exact theta: an 11 x 11 box that moves when its minimum is on the boundary and shrinks when it is interior.
"""
import math

import numpy as np

GR = (math.sqrt(5.0) - 1) / 2


class Rec:
    def __init__(self, P, ntab=200001):
        self.P = P
        self.a, self.es = P.a, P.estar
        self._S = np.linspace(0.0, 1.0, ntab)
        self._TH = P.theta_vec(self.es * self._S ** 2)
        self._TH[0], self._TH[-1] = self.a, 0.0
        # scan grids
        ph = np.concatenate([np.linspace(0.002, 0.998, 250), 1 - np.geomspace(1e-6, 0.1, 120), np.geomspace(1e-5, 0.01, 40)])
        self.PHI = np.unique(ph)
        q = np.concatenate([np.linspace(0.0, 1.0, 161), np.geomspace(1e-7, 0.05, 120), 1 - np.geomspace(1e-5, 0.05, 40)])
        self.Q = np.unique(q)

    def theta_tab(self, e):
        e = np.asarray(e, dtype=float)
        s_ = np.sqrt(np.clip(e, 0.0, self.es) / self.es)
        return np.where(e >= self.es, 0.0, np.interp(s_, self._S, self._TH))

    def F_vec(self, phi, beta, g, theta=None):
        theta = theta or self.P.theta_vec
        phi, beta = np.broadcast_arrays(np.asarray(phi, float), np.asarray(beta, float))
        mu = phi * theta((g - beta) / phi)
        y1 = beta / (1 - phi)
        t1 = theta(y1)
        y2 = mu / (1 - phi)
        A = (1 - phi) * (y1 + t1)
        Bv = (1 - phi) * (y2 + theta(y2))
        return np.where(beta <= mu, np.maximum(A, Bv), mu + (1 - phi) * t1)

    def F_s(self, phi, beta, g):
        th = self.P.theta
        mu = phi * th((g - beta) / phi)
        y1 = beta / (1 - phi)
        t1 = th(y1)
        if beta <= mu:
            y2 = mu / (1 - phi)
            return (1 - phi) * max(y1 + t1, y2 + th(y2))
        return mu + (1 - phi) * t1

    def _zoom(self, g, x0, y0, wx, wy, rounds=70, n=11):
        """moving zoom in x = logit(phi), y = logit(beta/g) with the exact theta"""
        lin = np.linspace(-1.0, 1.0, n)
        best = (math.inf, None, None)
        for _ in range(rounds):
            xs = x0 + wx * lin
            ys = y0 + wy * lin
            phi = 1.0 / (1.0 + np.exp(-xs))
            q = 1.0 / (1.0 + np.exp(-ys))
            phi = np.clip(phi, 1e-12, 1 - 1e-12)
            V = self.F_vec(phi[:, None], (g * q)[None, :], g)
            i, j = np.unravel_index(np.argmin(V), V.shape)
            if V[i, j] < best[0]:
                best = (float(V[i, j]), float(phi[i]), float(g * q[j]))
            x0, y0 = xs[i], ys[j]
            if 0 < i < n - 1:
                wx *= 0.4
            if 0 < j < n - 1:
                wy *= 0.4
            if wx < 1e-13 and wy < 1e-13:
                break
        return best

    def _edge0(self, g):
        """the edge beta = 0: a 1-d minimisation over phi (scan, then golden section)"""
        f = lambda p: self.F_s(p, 0.0, g)
        v = self.F_vec(self.PHI, np.zeros(len(self.PHI)), g, self.theta_tab)
        k = int(np.argmin(v))
        lo, hi = self.PHI[max(k - 2, 0)], self.PHI[min(k + 2, len(self.PHI) - 1)]
        x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
        f1, f2 = f(x1), f(x2)
        for _ in range(70):
            if f1 < f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - GR * (hi - lo)
                f1 = f(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + GR * (hi - lo)
                f2 = f(x2)
        pm = 0.5 * (lo + hi)
        return (f(pm), pm, 0.0)

    def R_theta(self, g, starts=4, full=False):
        """(value, phi, beta) of the smallest F found; with full=True also the scan minimum"""
        PH, Q = self.PHI, self.Q
        val = self.F_vec(PH[:, None], (g * Q)[None, :], g, self.theta_tab)
        pad = np.pad(val, 1, constant_values=np.inf)
        c = pad[1:-1, 1:-1]
        loc = np.ones(val.shape, dtype=bool)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di or dj:
                    loc &= c <= pad[1 + di:pad.shape[0] - 1 + di, 1 + dj:pad.shape[1] - 1 + dj]
        idx = np.argwhere(loc)
        order = np.argsort(val[loc])
        cands = [tuple(idx[k]) for k in order[:starts]]
        scan = float(val.min())
        best = (scan,) + tuple(float(z) for z in (PH[np.unravel_index(np.argmin(val), val.shape)[0]], g * Q[np.unravel_index(np.argmin(val), val.shape)[1]]))
        lx = lambda p: math.log(p / (1 - p))
        for (i, j) in cands:
            p0 = float(PH[i])
            q0 = min(max(float(Q[j]), 1e-9), 1 - 1e-9)
            wx = 2.0 * max(abs(lx(float(PH[min(i + 1, len(PH) - 1)])) - lx(p0)), abs(lx(p0) - lx(float(PH[max(i - 1, 0)]))), 1e-3)
            qn = [min(max(float(Q[k]), 1e-9), 1 - 1e-9) for k in (max(j - 1, 0), min(j + 1, len(Q) - 1))]
            wy = 2.0 * max(abs(lx(qn[1]) - lx(q0)), abs(lx(q0) - lx(qn[0])), 1e-3)
            r = self._zoom(g, lx(p0), lx(q0), wx, wy)
            if r[0] < best[0]:
                best = r
        e0 = self._edge0(g)
        if e0[0] < best[0]:
            best = e0
        return best + (scan,) if full else best

    def T2(self, g):
        if g >= self.es:
            return 0.0
        return min(self.P.theta(g), self.R_theta(g)[0])


class Rec2:
    """The same operator in the coordinates (y1, e):  y1 = beta/(1 - phi) the finest inner rate, e = (g - beta)/phi the
    outer rate; then phi = (g - y1)/(e - y1), y2 = mu/(1 - phi) = theta(e)(g - y1)/(e - g), and
        F = ((e - g)/(e - y1)) * [ max(S(y1), S(y2))  if y1 <= y2  else  y2 + theta(y1) ],      0 <= y1 < g < e <= eps*
    (beyond eps* the bracket is a (e - g)/(e - y1), increasing in e).  Minimiser: an exact 2-d scan, then from the
    lowest local minima of the scan nested golden-section searches (inner: e, outer: y1) on windows of +-3 cells."""

    def __init__(self, P, ny=140, ne=420):
        self.P = P
        self.a, self.es = P.a, P.estar
        self.ny, self.ne = ny, ne

    def F_vec(self, y1, e, g):
        th = self.P.theta_vec
        y1, e = np.broadcast_arrays(np.asarray(y1, float), np.asarray(e, float))
        y2 = th(e) * (g - y1) / (e - g)
        t1 = th(y1)
        inner = np.where(y1 <= y2, np.maximum(y1 + t1, y2 + th(y2)), y2 + t1)
        return (e - g) / (e - y1) * inner

    def F_s(self, y1, e, g):
        th = self.P.theta
        y2 = th(e) * (g - y1) / (e - g)
        t1 = th(y1)
        inner = max(y1 + t1, y2 + th(y2)) if y1 <= y2 else y2 + t1
        return (e - g) / (e - y1) * inner

    @staticmethod
    def _gold(f, lo, hi, iters=60):
        x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
        f1, f2 = f(x1), f(x2)
        for _ in range(iters):
            if f1 < f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - GR * (hi - lo)
                f1 = f(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + GR * (hi - lo)
                f2 = f(x2)
            if hi - lo <= 1e-15 * max(abs(hi), 1e-300):
                break
        xm = 0.5 * (lo + hi)
        return xm, f(xm)

    def K(self, y1, g, ee):
        """K(y1) = min over the outer rate e of F(y1, e; g): a full 1-d scan over the grid ee with the exact theta, then a
        golden-section search on +-2 cells around the grid minimum.  Returns (value, e)."""
        v = self.F_vec(np.full(len(ee), y1), ee, g)
        j = int(np.argmin(v))
        lo, hi = float(ee[max(j - 2, 0)]), float(ee[min(j + 2, len(ee) - 1)])
        em, fm = self._gold(lambda e_: self.F_s(y1, e_, g), lo, hi)
        if v[j] < fm:
            return float(v[j]), float(ee[j])
        return fm, em

    def R_theta(self, g, starts=2, full=False):
        """nested one-dimensional minimisations: outer over y1 (scan of K, then golden section around its lowest local
        minima), inner K(y1) with a FULL scan over e every time (no window carried over from a 2-d scan)."""
        es = self.es
        if g >= es:
            return (0.0, 1.0, 0.0) + ((0.0,) if full else ())
        ys = np.unique(np.concatenate([[0.0], np.geomspace(1e-9, 1.0, self.ny // 2) * g * 0.999999, np.linspace(0.0, 0.999999, self.ny // 2) * g]))
        de = np.unique(np.concatenate([np.geomspace(1e-9, 1.0, self.ne // 2), np.linspace(1e-6, 1.0, self.ne // 2)])) * (es - g)
        ee = g + de
        memo = {}

        def Kv(y1):
            if y1 not in memo:
                memo[y1] = self.K(y1, g, ee)
            return memo[y1][0]
        kv = np.array([Kv(float(y)) for y in ys])
        scan = float(kv.min())
        n = len(ys)
        locs = [i for i in range(n) if (i == 0 or kv[i] <= kv[i - 1]) and (i == n - 1 or kv[i] <= kv[i + 1])]
        locs.sort(key=lambda i: kv[i])
        best = (math.inf, None)
        for i in locs[:starts]:
            lo, hi = float(ys[max(i - 2, 0)]), float(ys[min(i + 2, n - 1)])
            ym, fm = self._gold(Kv, lo, hi, iters=45)
            if kv[i] < fm:
                ym, fm = float(ys[i]), float(kv[i])
            if fm < best[0]:
                best = (fm, ym)
        v, y1 = best
        e = memo[y1][1]
        phi = (g - y1) / (e - y1)
        out = (v, phi, y1 * (1 - phi))
        return out + (scan,) if full else out

    def T2(self, g):
        if g >= self.es:
            return 0.0
        return min(self.P.theta(g), self.R_theta(g)[0])
