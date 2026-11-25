#!/usr/bin/env python3
"""Referee R8 -- the level recursion with the point g = 0 (item 13 of the brief; Proposition K5).  Own code.

  T_1 = theta_na on (0, inf), tau_1 = a;
  T_{k+1}(g) = min(T_k(g), R[T_k](g)),
       R[T](g) = inf_{0<phi<1, 0<beta<g} sup_{gamma>=beta} [ min(gamma, phi theta_na((g-beta)/phi)) + (1-phi) T(gamma/(1-phi)) ],
  tau_{k+1}  = min(tau_k, inf_phi max( (1-phi) tau_k , (1-phi) sup_{0<x<=phi a/(1-phi)} (x + T_k(x)) )).

Discretisation: T_k on a geometric grid of (gmin, eps*] (0 beyond eps*); the supremum over gamma is exact for the
interpolant; the infimum over (phi, beta) is a grid search (so every value is an upper estimate of the
infimum for the interpolant).  Two interpolants:
  'step'   T(y) := value at the grid point to the left (tau_k below gmin): an upper bound of T_k, so that all
           numbers are upper bounds of the exact recursion (up to rounding);
  'linear' piecewise linear: an estimate.
Checked at every level: nonincreasing in k and g, T_k >= theta_hint on the grid, tau_k >= h, tau_k >= T_k(gmin).
tau_2 is compared with the closed form min_phi max((1-phi)a, phi a + (1-phi) theta_na(phi a/(1-phi))).

usage: python3 r8_recursion.py [u ...]
"""
import sys, math, time
import numpy as np


def kl(r, q):
    out = 0.0
    if r > 0:
        out += r * math.log(r / q)
    if r < 1:
        out += (1 - r) * math.log((1 - r) / (1 - q))
    return out


class Cube:
    def __init__(self, u):
        self.u = u
        self.pu = 1 / (1 + math.exp(u))
        self.lam1 = math.log(2 / (1 + math.exp(-u)))
        self.estar = math.log(math.cosh(u / 2))
        self.a = kl(self.pu, 0.5)
        self.h = kl(self.lam1 / u, 0.5)
        # table of theta_na by radius
        self.rho = np.linspace(self.pu, 0.5, 20001)
        self.acc = np.array([kl(r, self.pu) for r in self.rho])      # increasing from 0 to eps*
        self.val = np.array([kl(r, 0.5) for r in self.rho])

    def theta_na(self, x):
        x = np.asarray(x, dtype=float)
        r = np.interp(np.clip(x, 0.0, self.estar), self.acc, self.rho)
        v = np.log(2.0) + r * np.log(r) + (1 - r) * np.log(1 - r)
        return np.where(x >= self.estar, 0.0, np.maximum(v, 0.0))

    def theta_na_exact(self, x):
        if x >= self.estar:
            return 0.0
        lo, hi = self.pu, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if kl(mid, self.pu) <= x:
                lo = mid
            else:
                hi = mid
        return kl(lo, 0.5)

    def theta_hint(self, e):
        e = np.asarray(e, dtype=float)
        r = np.clip((self.lam1 + e) / self.u, 1e-300, 0.5)
        v = np.log(2.0) + r * np.log(r) + (1 - r) * np.log(1 - r)
        return np.where(e >= self.estar, 0.0, np.maximum(v, 0.0))


def tau2_closed(c):
    best = 1e9
    arg = None
    for phi in np.linspace(0.30, 0.70, 400001):
        v = max((1 - phi) * c.a, phi * c.a + (1 - phi) * c.theta_na_exact(phi * c.a / (1 - phi)))
        if v < best:
            best, arg = v, phi
    return best, arg


class Interp:
    """T on the grid g (increasing), tau at 0, zero beyond eps*; S(x) = x + T(x)"""

    def __init__(self, g, T, tau, estar, mode):
        self.g, self.T, self.tau, self.estar, self.mode = g, T, tau, estar, mode
        n = g.shape[0]
        if mode == 'step':
            # cell 0: [0, g_0) value tau ; cell i (1..n-1): [g_{i-1}, g_i) value T_{i-1}; beyond g_{n-1}=eps*: 0
            self.edges = np.concatenate(([0.0], g))               # length n+1; cell i = [edges[i], edges[i+1])
            self.cval = np.concatenate(([tau], T[:-1]))            # value on cell i, i = 0..n-1
            self.cellsup = self.edges[1:] + self.cval              # sup of x + T on the whole cell
        else:
            self.xs = np.concatenate(([0.0], g))
            self.ys = np.concatenate(([tau], T))
            self.S = self.xs + self.ys
        # sparse table for range maxima
        arr = self.cellsup if mode == 'step' else self.S
        self.tab = [arr]
        k = 1
        while 2 * k <= arr.shape[0]:
            prev = self.tab[-1]
            self.tab.append(np.maximum(prev[:-k], prev[k:]))
            k *= 2

    def rmax(self, i, j):
        """max of arr[i..j] inclusive (arrays of indices, i <= j)"""
        ln = j - i + 1
        k = np.floor(np.log2(np.maximum(ln, 1))).astype(int)
        out = np.empty(i.shape[0])
        for kk in np.unique(k):
            sel = k == kk
            t = self.tab[kk]
            out[sel] = np.maximum(t[i[sel]], t[j[sel] - (1 << kk) + 1])
        return out

    def value(self, x):
        x = np.asarray(x, dtype=float)
        if self.mode == 'step':
            i = np.clip(np.searchsorted(self.edges, x, side='right') - 1, 0, self.cval.shape[0] - 1)
            return np.where(x >= self.estar, 0.0, self.cval[i])
        return np.where(x >= self.estar, 0.0, np.interp(x, self.xs, self.ys))

    def sup_S(self, x1, x2):
        """sup of x + T(x) over [x1, x2] (arrays, 0 <= x1 <= x2)"""
        x1 = np.asarray(x1, dtype=float)
        x2 = np.asarray(x2, dtype=float)
        est = self.estar
        # part beyond eps*: T = 0, sup = x2
        beyond = np.where(x2 >= est, x2, -np.inf)
        b2 = np.minimum(x2, est)
        b1 = np.minimum(x1, est)
        if self.mode == 'step':
            nc = self.cval.shape[0]
            i1 = np.clip(np.searchsorted(self.edges, b1, side='right') - 1, 0, nc - 1)
            i2 = np.clip(np.searchsorted(self.edges, b2, side='right') - 1, 0, nc - 1)
            # last cell cut at b2, full cells i1..i2-1
            last = b2 + self.cval[i2]
            full = np.where(i2 > i1, self.rmax(i1, np.maximum(i2 - 1, i1)), -np.inf)
            inside = np.maximum(last, full)
            inside = np.where(x1 >= est, -np.inf, inside)
        else:
            e1 = b1 + np.interp(b1, self.xs, self.ys)
            e2 = b2 + np.interp(b2, self.xs, self.ys)
            i1 = np.searchsorted(self.xs, b1, side='left')
            i2 = np.searchsorted(self.xs, b2, side='right') - 1
            mid = np.where(i2 >= i1, self.rmax(np.minimum(i1, self.xs.shape[0] - 1), np.maximum(i2, np.minimum(i1, self.xs.shape[0] - 1))), -np.inf)
            mid = np.where(i2 >= i1, mid, -np.inf)
            inside = np.maximum(np.maximum(e1, e2), mid)
            inside = np.where(x1 >= est, -np.inf, inside)
        return np.maximum(inside, beyond)


def run(u, ngrid=180, nphi=90, nbeta=26, kmax=10, mode='linear', gminfac=1e-6, verbose=True):
    c = Cube(u)
    a, h, est = c.a, c.h, c.estar
    g = est * np.exp(np.linspace(math.log(gminfac), 0.0, ngrid))
    T = c.theta_na(g)
    tau = a
    th = c.theta_hint(g)
    out = {'a': a, 'h': h, 'tau': [tau]}
    phis_base = np.unique(np.concatenate((np.linspace(0.004, 0.996, nphi), np.exp(np.linspace(math.log(1e-4), math.log(0.05), 30)),
                                          1 - np.exp(np.linspace(math.log(1e-3), math.log(0.05), 20)))))
    betafr = np.exp(np.linspace(math.log(1e-5), math.log(0.95), nbeta))
    ok_mono = ok_hint = True
    for k in range(2, kmax + 1):
        I = Interp(g, T, tau, est, mode)
        Tn = T.copy()
        for ig in range(ngrid):
            gg = g[ig]
            hg = float(c.theta_hint(gg))
            special = [gg / (gg + hg) if hg > 0 else 0.5, min(0.999, gg / h)]
            phis = np.unique(np.concatenate((phis_base, np.clip(np.array(special + [s * f for s in special for f in (0.8, 0.9, 1.1, 1.25)]), 1e-4, 0.999))))
            P, B = np.meshgrid(phis, betafr * gg, indexing='ij')
            P = P.ravel()
            B = B.ravel()
            mu = P * c.theta_na((gg - B) / P)
            # sup over gamma >= beta: if mu <= beta the value at gamma = beta, else (1-phi) sup_{[beta/(1-phi), mu/(1-phi)]} (x+T)
            v1 = mu + (1 - P) * I.value(B / (1 - P))
            hi = np.maximum(mu, B)
            v2 = (1 - P) * I.sup_S(B / (1 - P), hi / (1 - P))
            val = np.where(mu <= B, v1, v2)
            best = float(val.min())
            # one local refinement around the best pair
            ib = int(val.argmin())
            p0, b0 = P[ib], B[ib]
            pp = np.clip(p0 * np.exp(np.linspace(-0.06, 0.06, 25)), 1e-5, 0.9995)
            bb = np.clip(b0 * np.exp(np.linspace(-0.25, 0.25, 15)), gg * 1e-7, gg * 0.999)
            P2, B2 = np.meshgrid(pp, bb, indexing='ij')
            P2 = P2.ravel()
            B2 = B2.ravel()
            mu2 = P2 * c.theta_na((gg - B2) / P2)
            w1 = mu2 + (1 - P2) * I.value(B2 / (1 - P2))
            w2 = (1 - P2) * I.sup_S(B2 / (1 - P2), np.maximum(mu2, B2) / (1 - P2))
            best = min(best, float(np.where(mu2 <= B2, w1, w2).min()))
            Tn[ig] = min(T[ig], best)
        # make nonincreasing in g (R[T] is nonincreasing in g; the grid search need not be) -- only lowers values
        # that are above a value further left, which keeps upper bounds valid
        Tn = np.minimum.accumulate(Tn)
        # g = 0
        ph = np.unique(np.concatenate((np.linspace(0.0005, 0.9995, 4000), np.exp(np.linspace(math.log(1e-6), math.log(0.01), 400)))))
        v0 = np.maximum((1 - ph) * tau, (1 - ph) * I.sup_S(np.zeros_like(ph), ph * a / (1 - ph)))
        i0 = int(v0.argmin())
        taun = min(tau, float(v0[i0]))
        phibest = ph[i0]
        # checks
        if np.any(Tn > T + 1e-12) or taun > tau + 1e-12 or np.any(np.diff(Tn) > 1e-12):
            ok_mono = False
        if np.any(Tn < th - 1e-9) or taun < h - 1e-12:
            ok_hint = False
        T, tau = Tn, taun
        out['tau'].append(tau)
        if verbose:
            print("  u=%.2f %-6s k=%2d  tau_k/a = %.4f   (tau_k - h)/a = %.4f   tau_k - T_k(gmin) = %.2e a   min(T_k - theta_hint)/a = %+.2e  "
                  "max(T_k - theta_hint)/a = %.4f  minimising phi at 0: %.4f" % (u, mode, k, tau / a, (tau - h) / a, (tau - T[0]) / a,
                                                                       float((T - th).min()) / a, float((T - th).max()) / a, phibest))
            sys.stdout.flush()
    out['ok_mono'] = ok_mono
    out['ok_hint'] = ok_hint
    out['T'] = T
    out['g'] = g
    return out


if __name__ == '__main__':
    us = [float(x) for x in sys.argv[1:]] or [1.0]
    report = {0.5: [0.5001, 0.3568, 0.3037, 0.2814, 0.2711], 1.0: [0.5006, 0.3613, 0.3108, 0.2898, 0.2803],
              2.0: [0.5056, 0.3814, 0.3393, 0.3225, 0.3145]}
    for u in us:
        t0 = time.time()
        c = Cube(u)
        t2, phi2 = tau2_closed(c)
        print("u = %.2f: a = %.6f, h = %.6f, h/a = %.4f, eps* = %.6f" % (u, c.a, c.h, c.h / c.a, c.estar))
        print("  closed form: tau_2/a = min_phi max((1-phi)a, phi a + (1-phi) theta_na(phi a/(1-phi)))/a = %.5f at phi = %.4f" % (t2 / c.a, phi2))
        for mode in ('linear', 'step'):
            r = run(u, mode=mode, kmax=8)
            print("  %s: tau_k/a (k=2..8) = %s" % (mode, ' '.join('%.4f' % (t / c.a) for t in r['tau'][1:])))
            print("     report (linear), k=2..6: %s ;  nonincreasing in k and g: %s ;  never below theta_hint / h: %s   [%.0f s]"
                  % (report.get(u), r['ok_mono'], r['ok_hint'], time.time() - t0))
