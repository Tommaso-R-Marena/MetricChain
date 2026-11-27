# Referee R9 -- own single-letter library (nothing imported from ws/F).
# Conventions of the report under review: cube Q_n, pi = Bernoulli(p)^n, q = 1-p, u > 0,
# Lam(0) = -ln(q + p e^-u), Lam(1) = -ln(p + q e^-u); additive instance gamma|x|, Z_gamma = q + p e^-gamma.
import numpy as np
from math import log, exp, sqrt, lgamma
from scipy.optimize import brentq, minimize_scalar, linprog

EPS = 1e-300


def h(x):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    m = (x > 0) & (x < 1)
    xm = x[m]
    out[m] = -xm * np.log(xm) - (1 - xm) * np.log1p(-xm)
    return out if out.ndim else float(out)


def kl(a, b):
    """binary KL(a||b), a in [0,1], b in (0,1); vectorised"""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a, b = np.broadcast_arrays(a, b)
    out = np.zeros(a.shape)
    m1 = a > 0
    out[m1] += a[m1] * np.log(a[m1] / b[m1])
    m0 = a < 1
    out[m0] += (1 - a[m0]) * np.log((1 - a[m0]) / (1 - b[m0]))
    return out if out.ndim else float(out)


class Par:
    def __init__(self, p, u):
        self.p = p
        self.u = u
        self.q = q = 1 - p
        self.theta = log(q / p)
        self.Lam0 = -log(q + p * exp(-u))
        self.Lam1 = -log(p + q * exp(-u))
        self.eta1 = q * exp(-u) / (p + q * exp(-u))   # flip prob of a coordinate with s_i = 1
        self.eta0 = p * exp(-u) / (q + p * exp(-u))   # flip prob of a coordinate with s_i = 0
        self.kminus = p * exp(-u) / (q + p * exp(-u))
        self.kplus = p * exp(u) / (q + p * exp(u))
        self._tab = None

    # ---------- one-site quantities
    def lnZ(self, g):
        return np.log(self.q + self.p * np.exp(-np.asarray(g, dtype=float)))

    def v(self, kap):
        """regularised KL(kap||p): KL on the window, slopes +-u outside (closed form)"""
        kap = np.asarray(kap, dtype=float)
        kc = np.clip(kap, self.kminus, self.kplus)
        return kl(kc, self.p) + self.u * np.abs(kap - kc)

    def v_bymax(self, kap, ng=40001):
        g = np.linspace(-self.u, self.u, ng)
        return float(np.max(-g * kap - self.lnZ(g)))

    # ---------- the game function
    def F(self, g, t):
        """closed form of Theorem F2(b); vectorised; F(g,0)=0"""
        g = np.asarray(g, dtype=float)
        t = np.asarray(t, dtype=float)
        u = self.u
        with np.errstate(divide='ignore', invalid='ignore'):
            num = (-np.expm1(-t * (u + g))) * np.exp(-t * self.Lam0) + (-np.expm1(-t * (u - g))) * np.exp(-t * (self.Lam1 + g))
            val = -t * self.lnZ(g) + np.log(num) - np.log(-np.expm1(-2 * t * u))
        val = np.where(t == 0, 0.0, val)
        return val

    def F_cosh(self, g, t):
        u = self.u
        th = self.theta
        lam = th + g
        lp, lm = th + u, th - u
        C = lambda x: 2 * np.cosh(x / 2)
        return np.log((np.sinh(t * (lp - lam) / 2) * C(lm) ** t + np.sinh(t * (lam - lm) / 2) * C(lp) ** t) / np.sinh(t * u)) - t * np.log(C(lam))

    def Kmat(self, g, t):
        """K[a,b] = exp(-t[u 1[a!=b] - Lam(b) - g a - ln Z_g])"""
        Lam = [self.Lam0, self.Lam1]
        lz = float(self.lnZ(g))
        K = np.zeros((2, 2))
        for a in (0, 1):
            for b in (0, 1):
                K[a, b] = exp(-t * (self.u * (a != b) - Lam[b] - g * a - lz))
        return K

    def F_game(self, g, t):
        """-ln val, val = min_M max_a sum_b M(b) K(a,b), by linear programming"""
        K = self.Kmat(g, t)
        # variables (M0, M1, w): minimise w s.t. K M <= w, M >= 0, sum M = 1
        res = linprog(c=[0, 0, 1], A_ub=np.hstack([K, -np.ones((2, 1))]), b_ub=[0, 0],
                      A_eq=[[1, 1, 0]], b_eq=[1], bounds=[(0, None), (0, None), (None, None)], method='highs')
        return -log(res.x[2])

    # ---------- F*(t) = max_g F(g,t)
    def Fstar(self, t, return_g=False):
        t = float(t)
        if t <= 0:
            return (0.0, 0.0) if return_g else 0.0
        u = self.u
        gs = np.linspace(-u, u, 2001)
        vals = self.F(gs, t)
        i = int(np.argmax(vals))
        lo, hi = gs[max(i - 1, 0)], gs[min(i + 1, len(gs) - 1)]
        r = minimize_scalar(lambda g: -float(self.F(g, t)), bounds=(lo, hi), method='bounded', options={'xatol': 1e-13})
        best = max(-r.fun, float(vals[i]))
        gbest = r.x if -r.fun >= vals[i] else gs[i]
        return (best, gbest) if return_g else best

    def table(self, nt=4001, ng=1601):
        """F*(t) on a grid of t in [0,1], gamma-maximisation by grid + vectorised golden section"""
        if self._tab is not None and self._tab[0].size == nt:
            return self._tab
        u = self.u
        ts = np.linspace(0, 1, nt)
        gs = np.linspace(-u, u, ng)
        Fs = np.zeros(nt)
        Gs = np.zeros(nt)
        step = gs[1] - gs[0]
        for blk in range(1, nt, 500):
            tt = ts[blk:blk + 500]
            vals = self.F(gs[None, :], tt[:, None])
            idx = np.argmax(vals, axis=1)
            lo = np.clip(gs[idx] - step, -u, u)
            hi = np.clip(gs[idx] + step, -u, u)
            gr = (sqrt(5) - 1) / 2
            for _ in range(60):
                x1 = hi - gr * (hi - lo)
                x2 = lo + gr * (hi - lo)
                f1 = self.F(x1, tt)
                f2 = self.F(x2, tt)
                m = f1 > f2
                hi = np.where(m, x2, hi)
                lo = np.where(m, lo, x1)
            gm = 0.5 * (lo + hi)
            fm = self.F(gm, tt)
            best = np.maximum(fm, vals[np.arange(len(tt)), idx])
            Fs[blk:blk + 500] = best
            Gs[blk:blk + 500] = np.where(fm >= vals[np.arange(len(tt)), idx], gm, gs[idx])
        self._tab = (ts, Fs, Gs)
        return self._tab

    # ---------- exponents from F*
    def Rmax(self, e, return_arg=False):
        """max_{0<=t<=1} [F*(t) - t e]"""
        ts, Fs, Gs = self.table()
        obj = Fs - ts * e
        i = int(np.argmax(obj))
        lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)]
        if hi > lo:
            r = minimize_scalar(lambda t: -(self.Fstar(t) - t * e), bounds=(lo, hi), method='bounded', options={'xatol': 1e-12})
            val, tb = (-r.fun, r.x) if -r.fun > obj[i] else (obj[i], ts[i])
        else:
            val, tb = obj[i], ts[i]
        val = max(val, 0.0, -e)   # t = 0 and t = 1 (F*(0) = F*(1) = 0)
        if return_arg:
            return val, tb, self.Fstar(tb, True)[1]
        return val

    def Rg(self, g, e, return_arg=False):
        """R_gamma(e) = max_{0<=t<=1} [F(g,t) - t e]"""
        ts = np.linspace(0, 1, 4001)
        obj = self.F(g, ts) - ts * e
        i = int(np.argmax(obj))
        lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)]
        r = minimize_scalar(lambda t: -(float(self.F(g, t)) - t * e), bounds=(lo, hi), method='bounded', options={'xatol': 1e-13})
        val, tb = (-r.fun, r.x) if -r.fun > obj[i] else (obj[i], ts[i])
        val = max(val, 0.0, -e)
        return (val, tb) if return_arg else val

    def R0(self, e):
        return self.Rg(0.0, e)

    def E(self):
        """class threshold sup_t F*(t)/t = max_g lim_{t->0} F(g,t)/t (chord gap of ln C)"""
        th, u = self.theta, self.u
        lnC = lambda x: np.log(2 * np.cosh(x / 2))
        G = lambda g: ((u - g) * lnC(th - u) + (u + g) * lnC(th + u)) / (2 * u) - lnC(th + g)
        r = minimize_scalar(lambda g: -G(g), bounds=(-u, u), method='bounded', options={'xatol': 1e-14})
        return -r.fun, r.x, float(G(0.0))

    def S(self, e):
        return e + self.Rmax(e)

    def ec(self):
        """e_c = -a,  a = sup_{t<1} F*(t)/(1-t)  (the supremum may be the limit t -> 1, i.e. -dF*/dt(1))"""
        if getattr(self, '_ec', None) is not None:
            return self._ec
        ts, Fs, Gs = self.table()
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = Fs[:-1] / (1 - ts[:-1])
        i = int(np.argmax(ratio))
        lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 2)]
        r = minimize_scalar(lambda t: -self.Fstar(t) / (1 - t), bounds=(lo, hi), method='bounded', options={'xatol': 1e-12})
        a = max(-r.fun, ratio[i])
        # limit t -> 1: Richardson extrapolation of F*(1-d)/d
        d = 1e-4
        l1 = self.Fstar(1 - d) / d
        l2 = self.Fstar(1 - d / 2) / (d / 2)
        a = max(a, 2 * l2 - l1, l2)
        self._ec = -a
        return -a

    def Sinv(self, x):
        """inverse of S on (e_c, inf), x > 0"""
        a = -self.ec()
        lo = -a
        hi = max(x, 1.0) + 1.0
        f = lambda e: self.S(e) - x
        return brentq(f, lo, hi, xtol=1e-13, rtol=1e-13)

    def theta_na(self, x):
        return self.Rmax(self.Sinv(x))

    def theta_na_tau(self, x):
        """max_{0<=tau<1} (F*(tau) - tau x)/(1 - tau)"""
        ts, Fs, Gs = self.table()
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = (Fs[:-1] - ts[:-1] * x) / (1 - ts[:-1])
        i = int(np.argmax(ratio))
        lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 2)]
        if hi > lo:
            r = minimize_scalar(lambda t: -(self.Fstar(t) - t * x) / (1 - t), bounds=(lo, hi), method='bounded', options={'xatol': 1e-12})
            return max(-r.fun, ratio[i])
        return ratio[i]

    def Rmax_inv(self, th):
        """inverse of R^max on (-inf, E): th > 0"""
        a = -self.ec()
        if th >= a:
            return -th
        E = self.E()[0]
        return brentq(lambda e: self.Rmax(e) - th, -a, E, xtol=1e-13, rtol=1e-13)

    # ---------- profile functionals z = (m; a, b):  a = P(S=1,X=0), b = P(S=0,X=1)
    def prof(self, m, al, be):
        """al = a/m, be = b/(1-m) (conditional flip probabilities); returns dict of arrays"""
        kap = m * (1 - al) + (1 - m) * be
        rho = m * al + (1 - m) * be
        I = h(kap) - m * h(al) - (1 - m) * h(be)
        Icone = m * kl(al, self.eta1) + (1 - m) * kl(be, self.eta0)
        J = m * kl(al, self.q) + (1 - m) * kl(be, self.p)
        Lam_m = (1 - m) * self.Lam0 + m * self.Lam1
        return dict(kap=kap, rho=rho, I=I, Icone=Icone, J=J, Lam_m=Lam_m)

    def cons(self, kind, m, al, be, g=0.0):
        d = self.prof(m, al, be)
        if kind == 'R0':      # u rho - Lam_m
            c = self.u * d['rho'] - d['Lam_m']
        elif kind == 'Rg':    # u rho - Lam_m + v_g(kap)
            c = self.u * d['rho'] - d['Lam_m'] - g * d['kap'] - float(self.lnZ(g))
        elif kind == 'Rmax':  # u rho - Lam_m + v(kap)
            c = self.u * d['rho'] - d['Lam_m'] + self.v(d['kap'])
        elif kind == 'na':    # I^cone
            c = d['Icone']
        elif kind == 'na2':   # I + u rho - Lam_m + v(kap)
            c = d['I'] + self.u * d['rho'] - d['Lam_m'] + self.v(d['kap'])
        else:
            raise ValueError(kind)
        return d['I'], c

    def minI(self, kind, m, level, g=0.0, N=401, zooms=7):
        """min{ I(z) : c(z) <= level } over profiles with centre type m, by grid + zoom (no duality)."""
        lo = np.array([0.0, 0.0])
        hi = np.array([1.0, 1.0])
        best = (np.inf, None)
        for z in range(zooms):
            al = np.linspace(lo[0], hi[0], N)[:, None]
            be = np.linspace(lo[1], hi[1], N)[None, :]
            I, c = self.cons(kind, m, al, be, g)
            I = np.where(c <= level, I, np.inf)
            k = int(np.argmin(I))
            i, j = divmod(k, N)
            if not np.isfinite(I[i, j]):
                # no feasible grid point in this window
                break
            if I[i, j] < best[0]:
                best = (float(I[i, j]), (float(al[i, 0]), float(be[0, j])))
            w = (hi - lo) / (N - 1) * 6
            c0 = np.array([al[i, 0], be[0, j]])
            lo = np.clip(c0 - w, 0, 1)
            hi = np.clip(c0 + w, 0, 1)
        return best

    def maxmin(self, kind, level, g=0.0, mgrid=None, N=301, zooms=7):
        """max_m min{I : c <= level}"""
        if mgrid is None:
            mgrid = np.linspace(0.02, 0.98, 49)
        vals = np.array([self.minI(kind, m, level, g, N, zooms)[0] for m in mgrid])
        vals = np.where(np.isfinite(vals), vals, -np.inf)
        i = int(np.argmax(vals))
        lo, hi = mgrid[max(i - 1, 0)], mgrid[min(i + 1, len(mgrid) - 1)]
        f = lambda m: -self.minI(kind, m, level, g, N, zooms)[0]
        r = minimize_scalar(f, bounds=(lo, hi), method='bounded', options={'xatol': 1e-7})
        if -r.fun > vals[i]:
            return -r.fun, r.x
        return float(vals[i]), float(mgrid[i])

    def a_cone(self):
        """max_m I(z_c(m)), z_c = cone-law profile"""
        f = lambda m: -float(self.prof(m, self.eta1, self.eta0)['I'])
        r = minimize_scalar(f, bounds=(1e-6, 1 - 1e-6), method='bounded', options={'xatol': 1e-12})
        return -r.fun, r.x


def logbinom(n, k):
    n = np.asarray(n, dtype=float)
    k = np.asarray(k, dtype=float)
    from scipy.special import gammaln
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def logsumexp(a):
    a = np.asarray(a, dtype=float)
    m = np.max(a)
    if not np.isfinite(m):
        return m
    return m + log(np.sum(np.exp(a - m)))
