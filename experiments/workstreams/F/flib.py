"""Workstream F -- single-letter formulas for binary sites with a field (own code; numpy only).

Conventions (beta absorbed):  reference measure pi = Bernoulli(p)^n on {0,1}^n, p = P(x_i = 1), q = 1 - p
(field theta = ln(q/p));  class = {psi : u-Lipschitz for the Hamming distance};  target ln E_pi e^{-psi}.
A "centre" s has type m = |s|/n.  A point x has, relative to s, the profile (a, b):
    a = #{i : s_i = 1, x_i = 0}/n   in [0, m],        b = #{i : s_i = 0, x_i = 1}/n   in [0, 1-m],
so  d(x,s)/n = a + b,  type of x:  kappa = m - a + b.   In relative units  x = a/m, y = b/(1-m).
"""
import math
import numpy as np

LN2 = math.log(2.0)


def h(x):
    """binary entropy (nats), vectorised, 0 at the ends"""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    m = (x > 0) & (x < 1)
    xm = x[m]
    out[m] = -xm * np.log(xm) - (1 - xm) * np.log(1 - xm)
    return out


def hs(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log(x) - (1 - x) * math.log(1 - x)


def kl(a, b):
    """binary relative entropy KL(a||b), vectorised in a (and b)"""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float) + 0 * a
    out = np.zeros_like(a)
    m1 = a > 0
    out[m1] += a[m1] * np.log(a[m1] / b[m1])
    m2 = a < 1
    out[m2] += (1 - a[m2]) * np.log((1 - a[m2]) / (1 - b[m2]))
    return out


def kls(a, b):
    r = 0.0
    if a > 0:
        r += a * math.log(a / b)
    if a < 1:
        r += (1 - a) * math.log((1 - a) / (1 - b))
    return r


# ---------------------------------------------------------------------------------------------
# the site
# ---------------------------------------------------------------------------------------------
class Site:
    """binary site with P(1) = p and envelope constant u (zero residual g = 0)"""

    def __init__(self, p, u):
        self.p, self.q, self.u = p, 1 - p, u
        q = 1 - p
        # soft gaps of one site at the zero residual: Lambda(b) = -ln sum_a pi(a) e^{-u [a != b]}
        self.L0 = -math.log(q + p * math.exp(-u))
        self.L1 = -math.log(p + q * math.exp(-u))
        # cone Gibbs law pi_s(x | s = b)  propto  pi(x) e^{-u [x != b]}: flip probabilities
        self.eta1 = q * math.exp(-u) / (p + q * math.exp(-u))      # P(x = 0 | s = 1)
        self.eta0 = p * math.exp(-u) / (q + p * math.exp(-u))      # P(x = 1 | s = 0)
        # the window of types: Gibbs means of the additive instances gamma = +u and gamma = -u
        self.kmin = p * math.exp(-u) / (q + p * math.exp(-u))
        self.kmax = p * math.exp(u) / (q + p * math.exp(u))

    def Lam(self, m):
        return (1 - m) * self.L0 + m * self.L1

    def v(self, kappa):
        """regularised KL(kappa || p): the largest function below KL(.||p) with slope in [-u, u]
        ( = max_{|lam| <= u} [lam kappa - ln(q + p e^lam)] ) = (1/n) ln w_H at type kappa"""
        kappa = np.asarray(kappa, dtype=float)
        out = kl(np.clip(kappa, self.kmin, self.kmax), self.p)
        out = out + self.u * np.maximum(kappa - self.kmax, 0) + self.u * np.maximum(self.kmin - kappa, 0)
        return out

    # profile functions; x = a/m, y = b/(1-m)
    def kappa(self, m, x, y):
        return m * (1 - x) + (1 - m) * y

    def I(self, m, x, y):
        """mutual information between the centre letter and the point letter"""
        return h(self.kappa(m, x, y)) - m * h(x) - (1 - m) * h(y)

    def Icone(self, m, x, y):
        """rate function of the cone Gibbs measure pi_s at the profile (x, y)"""
        return m * kl(x, self.eta1) + (1 - m) * kl(y, self.eta0)

    def J(self, m, x, y):
        """-(1/n) ln pi(sphere of profile (x,y) around s)"""
        return m * kl(x, self.q) + (1 - m) * kl(y, self.p)


# ---------------------------------------------------------------------------------------------
# hinted exponent of an additive instance gamma |x| (game formula of Theorem 11.27 / workstream A)
# ---------------------------------------------------------------------------------------------
def game_value_2x2(K):
    """min over column mixtures M of max over rows a of (K M)_a, K positive 2x2"""
    # f(M0) = max(K00 M0 + K01 (1-M0), K10 M0 + K11 (1-M0)), convex piecewise linear
    cands = [0.0, 1.0]
    den = (K[0, 0] - K[0, 1]) - (K[1, 0] - K[1, 1])
    if abs(den) > 1e-300:
        M0 = (K[1, 1] - K[0, 1]) / den
        if 0 < M0 < 1:
            cands.append(M0)
    best = math.inf
    for M0 in cands:
        val = max(K[0, 0] * M0 + K[0, 1] * (1 - M0), K[1, 0] * M0 + K[1, 1] * (1 - M0))
        best = min(best, val)
    return best


def additive_site(p, u, gamma):
    """site data of the additive instance gamma|x| in the class with field p:
    Gibbs law pi_g, slack s[a, b] = u [a != b] - gamma a + gamma b  (a = evaluated letter, b = centre letter),
    soft gaps Lam[b] = -ln sum_a pi_g(a) e^{-s(a,b)}"""
    q = 1 - p
    pg1 = p * math.exp(-gamma) / (q + p * math.exp(-gamma))
    pig = np.array([1 - pg1, pg1])
    s = np.array([[0.0, u + gamma], [u - gamma, 0.0]])
    Lam = np.array([-math.log(pig[0] * math.exp(-s[0, b]) + pig[1] * math.exp(-s[1, b])) for b in (0, 1)])
    return pig, s, Lam


def minus_log_val(p, u, gamma, t):
    pig, s, Lam = additive_site(p, u, gamma)
    K = np.exp(-t * (s - Lam[None, :]))
    return -math.log(game_value_2x2(K))


def R_additive(p, u, gamma, eps1, nt=2001, tmax=1.0):
    """R_gamma(eps1) = max_{0 <= t <= tmax} [ -ln val(K_t) - t eps1 ]  (tmax = 1 is beta)"""
    ts = np.linspace(0.0, tmax, nt)
    vals = np.array([minus_log_val(p, u, gamma, t) - t * eps1 for t in ts])
    i = int(np.argmax(vals))
    # golden-section polish around the best grid point
    lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, nt - 1)]
    f = lambda t: minus_log_val(p, u, gamma, t) - t * eps1
    gr = (math.sqrt(5) - 1) / 2
    c, d = hi - gr * (hi - lo), lo + gr * (hi - lo)
    fc, fd = f(c), f(d)
    for _ in range(60):
        if fc > fd:
            hi, d, fd = d, c, fc
            c = hi - gr * (hi - lo)
            fc = f(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + gr * (hi - lo)
            fd = f(d)
    tbest = (lo + hi) / 2
    return max(float(vals[i]), f(tbest)), tbest


def R_max(p, u, eps1, ngam=81, nt=801):
    """max over additive instances gamma in [-u, u] of R_gamma(eps1); returns (value, gamma*)"""
    gs = np.linspace(-u, u, ngam)
    vals = [R_additive(p, u, g, eps1, nt=nt)[0] for g in gs]
    i = int(np.argmax(vals))
    lo, hi = gs[max(i - 1, 0)], gs[min(i + 1, ngam - 1)]
    f = lambda g: R_additive(p, u, g, eps1, nt=nt)[0]
    gr = (math.sqrt(5) - 1) / 2
    c, d = hi - gr * (hi - lo), lo + gr * (hi - lo)
    fc, fd = f(c), f(d)
    for _ in range(40):
        if fc > fd:
            hi, d, fd = d, c, fc
            c = hi - gr * (hi - lo)
            fc = f(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + gr * (hi - lo)
            fd = f(d)
    g = (lo + hi) / 2
    return max(vals[i], f(g)), g


def thr_additive(p, u, gamma):
    """accuracy threshold of the additive instance: lim_{t -> 0} -ln val(K_t)/t"""
    t = 1e-6
    return minus_log_val(p, u, gamma, t) / t


# ---------------------------------------------------------------------------------------------
# profile (centre) formulas
# ---------------------------------------------------------------------------------------------
def hint0_rd(site, eps1, nm=20001):
    """hinted exponent at g = 0 in rate-distortion form: max_m [h(m) - h(rho_m)]_+,
    rho_m = (Lam(m) + eps1)/u, valid for rho_m <= min(m, 1-m).  Returns (value, m*, rho*)."""
    ms = np.linspace(1e-9, 1 - 1e-9, nm)
    rho = (site.Lam(ms) + eps1) / site.u
    ok = rho <= np.minimum(ms, 1 - ms)
    val = np.where(ok, h(ms) - h(np.clip(rho, 0, 1)), 0.0)
    i = int(np.argmax(val))
    return float(val[i]), float(ms[i]), float(rho[i])


class ProfileGrid:
    """grid of (m, x, y) with x + y < 1 (near side); evaluates the three max-min formulas

        theta_X(eps1) = max_m min { I(S;X) : c_X(m, x, y) <= eps1 },
        c_hint0 = u (m x + (1-m) y) - Lam(m)
        c_H     = c_hint0 + v(kappa)                 (regularised KL(P_X || pi))
        c_Hraw  = c_hint0 + KL(kappa || p)
        c_na    = Icone(m, x, y) = c_Hraw + I(S;X)
    """

    def __init__(self, site, nm=241, nx=321, ny=321, mlo=1e-4, mhi=1 - 1e-4):
        self.site = site
        self.ms = np.linspace(mlo, mhi, nm)
        xs = np.linspace(0.0, 1.0, nx)
        ys = np.linspace(0.0, 1.0, ny)
        self.X, self.Y = np.meshgrid(xs, ys, indexing="ij")
        self.near = (self.X + self.Y) < 1.0
        self.tables = []
        for m in self.ms:
            kap = site.kappa(m, self.X, self.Y)
            I = site.I(m, self.X, self.Y)
            c0 = site.u * (m * self.X + (1 - m) * self.Y) - site.Lam(m)
            cH = c0 + site.v(kap)
            cHraw = c0 + kl(kap, site.p)
            cna = site.Icone(m, self.X, self.Y)
            self.tables.append((I, c0, cH, cHraw, cna, kap))

    def maxmin(self, which, eps1):
        """returns (value, m*, x*, y*, kappa*)"""
        idx = dict(hint0=1, H=2, Hraw=3, na=4)[which]
        best = (-1.0, None, None, None, None)
        for m, tab in zip(self.ms, self.tables):
            I = tab[0]
            feas = self.near & (tab[idx] <= eps1)
            if not feas.any():
                val, ij = math.inf, None       # no exit: this centre type gives nothing (ball = everything)
                continue
            Im = np.where(feas, I, np.inf)
            k = int(np.argmin(Im))
            val = float(Im.flat[k])
            if val > best[0]:
                best = (val, float(m), float(self.X.flat[k]), float(self.Y.flat[k]), float(tab[5].flat[k]))
        return best


def kl_shift_identity_check(site, m, x, y):
    """Icone(m,x,y) - [ I + KL(kappa||p) + u (m x + (1-m) y) - Lam(m) ]   (should vanish)"""
    kap = site.kappa(m, x, y)
    return float(site.Icone(m, x, y) - (site.I(m, x, y) + kl(kap, site.p) + site.u * (m * x + (1 - m) * y) - site.Lam(m)))


# ---------------------------------------------------------------------------------------------
# precise max-min:  theta_X(eps1) = max_m min { I(m,x,y) : c_X(m,x,y) <= eps1 }
# ---------------------------------------------------------------------------------------------
from scipy.optimize import minimize, minimize_scalar


def _cfun(site, which):
    u = site.u
    if which == "hint0":
        return lambda m, x, y: u * (m * x + (1 - m) * y) - site.Lam(m)
    if which == "H":
        return lambda m, x, y: u * (m * x + (1 - m) * y) - site.Lam(m) + float(site.v(site.kappa(m, x, y)))
    if which == "Hraw":
        return lambda m, x, y: u * (m * x + (1 - m) * y) - site.Lam(m) + kls(site.kappa(m, x, y), site.p)
    if which == "na":
        return lambda m, x, y: m * kls(x, site.eta1) + (1 - m) * kls(y, site.eta0)
    raise ValueError(which)


def _I(m, x, y):
    kap = m * (1 - x) + (1 - m) * y
    return hs(kap) - m * hs(x) - (1 - m) * hs(y)


def inner_min(site, which, m, eps1, starts=None):
    """min { I(m,x,y) : c(m,x,y) <= eps1, 0 <= x,y <= 1 }; returns (value, x, y)"""
    c = _cfun(site, which)
    d = 1e-12
    cons = [{"type": "ineq", "fun": lambda z: eps1 - c(m, z[0], z[1])}]
    best = (math.inf, None, None)
    if starts is None:
        starts = []
        # feasible anchor: the cone point (na) or the origin (others); move towards independence
        if which == "na":
            x0, y0 = site.eta1, site.eta0
        else:
            x0, y0 = 1e-6, 1e-6
        # independence points: x + y = 1
        for w in (0.2, 0.5, 0.8):
            xi, yi = w, 1 - w
            # bisection along the segment from the anchor to the independence point for the boundary
            lo, hi = 0.0, 1.0
            if c(m, xi, yi) <= eps1:
                return 0.0, xi, yi
            for _ in range(60):
                mid = (lo + hi) / 2
                if c(m, x0 + mid * (xi - x0), y0 + mid * (yi - y0)) <= eps1:
                    lo = mid
                else:
                    hi = mid
            starts.append((x0 + lo * (xi - x0), y0 + lo * (yi - y0)))
    for (xs, ys) in starts:
        res = minimize(lambda z: _I(m, z[0], z[1]), x0=[xs, ys], method="SLSQP", constraints=cons,
                       bounds=[(d, 1 - d), (d, 1 - d)], options=dict(ftol=1e-15, maxiter=500))
        z = res.x
        if c(m, z[0], z[1]) <= eps1 + 1e-10:
            val = _I(m, z[0], z[1])
            if val < best[0]:
                best = (val, float(z[0]), float(z[1]))
        v0 = _I(m, xs, ys)
        if v0 < best[0]:
            best = (v0, xs, ys)
    return best


def maxmin_precise(site, which, eps1, mgrid=None):
    """max over m of inner_min; returns (value, m*, x*, y*, kappa*)"""
    if mgrid is None:
        mgrid = np.linspace(0.02, 0.98, 49)
    vals = [inner_min(site, which, m, eps1)[0] for m in mgrid]
    i = int(np.argmax(vals))
    lo, hi = mgrid[max(i - 1, 0)], mgrid[min(i + 1, len(mgrid) - 1)]
    res = minimize_scalar(lambda m: -inner_min(site, which, m, eps1)[0], bounds=(lo, hi), method="bounded",
                          options=dict(xatol=1e-10))
    m = float(res.x)
    val, x, y = inner_min(site, which, m, eps1)
    if vals[i] > val:
        m = float(mgrid[i])
        val, x, y = inner_min(site, which, m, eps1)
    return val, m, x, y, site.kappa(m, x, y)


# ---------------------------------------------------------------------------------------------
# closed form of the 2x2 game and the worst-case pair of exponent functions
# ---------------------------------------------------------------------------------------------
def F_game(p, u, gamma, t):
    """F(gamma, t) = -ln val(K_t) for the additive instance gamma|x| (closed form; vectorised):
       -t ln Z_g + ln[(1 - e^{-t(u+g)}) e^{-t L0} + (1 - e^{-t(u-g)}) e^{-t(L1+g)}] - ln(1 - e^{-2tu}),  F(.,0) = 0"""
    q = 1 - p
    L0 = -math.log(q + p * math.exp(-u))
    L1 = -math.log(p + q * math.exp(-u))
    gamma = np.asarray(gamma, dtype=float)
    t = np.asarray(t, dtype=float)
    tt = np.where(t > 0, t, 1.0)
    lnZ = np.log(q + p * np.exp(-gamma))
    val = (-tt * lnZ + np.log(-np.expm1(-tt * (u + gamma)) * np.exp(-tt * L0) - np.expm1(-tt * (u - gamma)) * np.exp(-tt * (L1 + gamma)))
           - np.log(-np.expm1(-2 * tt * u)))
    return np.where(t > 0, val, 0.0)


class WorstPair:
    """R^max(e) = max_{0<=t<=1} [F*(t) - t e],  F*(t) = max_{|gamma|<=u} F(gamma, t)   (all real e);
    S(e) = e + R^max(e);  theta_na(x) = R^max(S^{-1}(x));  h = R^max(0), a = theta_na(0+), E = F*'(0+)."""

    def __init__(self, p, u, nt=4001, ngam=801, gam_fixed=None):
        self.p, self.u = p, u
        self.ts = np.linspace(0.0, 1.0, nt)
        if gam_fixed is None:
            gs = np.linspace(-u, u, ngam)
            Fg = F_game(p, u, gs[:, None], self.ts[None, :])
            # parabolic refinement of the maximum over gamma
            i = np.argmax(Fg, axis=0)
            Fs = Fg[i, np.arange(nt)]
            ii = np.clip(i, 1, ngam - 2)
            f0, f1, f2 = Fg[ii - 1, np.arange(nt)], Fg[ii, np.arange(nt)], Fg[ii + 1, np.arange(nt)]
            den = f0 - 2 * f1 + f2
            with np.errstate(divide="ignore", invalid="ignore"):
                shift = np.where(den < 0, 0.5 * (f0 - f2) / den, 0.0)
            shift = np.clip(shift, -1, 1)
            gref = gs[ii] + shift * (gs[1] - gs[0])
            Fref = F_game(p, u, np.clip(gref, -u, u), self.ts)
            self.Fstar = np.maximum(Fs, Fref)
            self.gstar_t = np.where(Fref >= Fs, np.clip(gref, -u, u), gs[i])
        else:
            self.Fstar = F_game(p, u, gam_fixed, self.ts)
            self.gstar_t = np.full(nt, gam_fixed)
        self.Fstar[0] = 0.0
        self.E = float(self.Fstar[1] / self.ts[1])                 # slope at 0: the threshold
        self.h = self.R(0.0)
        # e_c: the largest e with R(e) = -e (slope -1):  e_c = (F*)'(1-) < 0;  a = theta_na(0+) = R(e_c) = -e_c
        self.ec = float((self.Fstar[-1] - self.Fstar[-2]) / (self.ts[-1] - self.ts[-2]))
        self.a = -self.ec

    def R(self, e):
        e = np.asarray(e, dtype=float)
        vals = self.Fstar[None, :] - np.atleast_1d(e)[:, None] * self.ts[None, :]
        i = np.argmax(vals, axis=1)
        out = vals[np.arange(len(i)), i]
        # parabolic refinement in t
        nt = len(self.ts)
        ii = np.clip(i, 1, nt - 2)
        r = np.arange(len(i))
        f0, f1, f2 = vals[r, ii - 1], vals[r, ii], vals[r, ii + 1]
        den = f0 - 2 * f1 + f2
        with np.errstate(divide="ignore", invalid="ignore"):
            corr = np.where(den < 0, -0.125 * (f2 - f0) ** 2 / den, 0.0)
        out = np.where((i > 0) & (i < nt - 1), np.maximum(out, f1 + corr), out)
        return out if e.ndim else float(out[0])

    def tstar(self, e):
        vals = self.Fstar - e * self.ts
        return float(self.ts[int(np.argmax(vals))])

    def S(self, e):
        return e + self.R(e)

    def Sinv(self, x):
        """the e with e + R(e) = x (x > 0)"""
        lo, hi = self.ec - 1.0, max(self.E, x) + 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if self.S(mid) < x:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    def theta_na(self, x):
        if x >= self.E:
            return 0.0
        return self.R(self.Sinv(x))


# ---------------------------------------------------------------------------------------------
# plain Monte Carlo from pi: the objective is J = I + KL(P_X || pi) = -(1/n) ln pi(sphere)
# ---------------------------------------------------------------------------------------------
def _J(site, m, x, y):
    return m * kls(x, site.q) + (1 - m) * kls(y, site.p)


def inner_min_J(site, which, m, eps1):
    """min { J(m,x,y) : c(m,x,y) <= eps1 }  (J is convex with minimum 0 at the pi-typical profile (q, p))"""
    c = _cfun(site, which)
    d = 1e-12
    cons = [{"type": "ineq", "fun": lambda z: eps1 - c(m, z[0], z[1])}]
    if c(m, site.q, site.p) <= eps1:
        return 0.0, site.q, site.p
    if which == "na":
        x0, y0 = site.eta1, site.eta0
    else:
        x0, y0 = 1e-6, 1e-6
    best = (math.inf, None, None)
    for w in (0.0, 0.5, 1.0):
        xi, yi = site.q, site.p
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if c(m, x0 + mid * (xi - x0), y0 + mid * (yi - y0)) <= eps1:
                lo = mid
            else:
                hi = mid
        xs, ys = x0 + lo * (xi - x0), y0 + lo * (yi - y0)
        xs = min(max(xs + (w - 0.5) * 0.02, d), 1 - d)
        res = minimize(lambda z: _J(site, m, z[0], z[1]), x0=[xs, ys], method="SLSQP", constraints=cons,
                       bounds=[(d, 1 - d), (d, 1 - d)], options=dict(ftol=1e-15, maxiter=500))
        z = res.x
        if c(m, z[0], z[1]) <= eps1 + 1e-10:
            val = _J(site, m, z[0], z[1])
            if val < best[0]:
                best = (val, float(z[0]), float(z[1]))
    return best


def maxmin_J(site, which, eps1, mgrid=None):
    if mgrid is None:
        mgrid = np.linspace(0.01, 0.99, 99)
    vals = [inner_min_J(site, which, m, eps1)[0] for m in mgrid]
    i = int(np.argmax(vals))
    lo, hi = mgrid[max(i - 1, 0)], mgrid[min(i + 1, len(mgrid) - 1)]
    res = minimize_scalar(lambda m: -inner_min_J(site, which, m, eps1)[0], bounds=(lo, hi), method="bounded",
                          options=dict(xatol=1e-10))
    m = float(res.x)
    val, x, y = inner_min_J(site, which, m, eps1)
    if vals[i] > val:
        m = float(mgrid[i]); val, x, y = inner_min_J(site, which, m, eps1)
    return val, m, x, y, site.kappa(m, x, y)
