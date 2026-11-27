"""Referee A: smooth pairs (theta with its derivative), the slope map through the tangency condition

    Sigma(B, s) = -(1 - s) theta'(e*),   theta(e*) - e* theta'(e*) = B/(1 - s)     (kappa(e) = theta - e theta' decreases from a),
    dSigma/dB = 1/e*,   dSigma/ds = theta(e*)/e*                                    (envelope theorem; (Sigma 4) of the report),

vectorised (bisection in ln e).  Cross-checked against the direct maximisation over e of ralib.Theta.sigma in a5_chain.py.
"""
import math
import numpy as np


class Smooth:
    name = "abstract"
    lo_e, hi_e = 1e-14, 1e6

    def f(self, e): raise NotImplementedError
    def df(self, e): raise NotImplementedError
    def d2f(self, e, d=1e-5):
        return (self.f(e * (1 + d)) - 2 * self.f(e) + self.f(e * (1 - d))) / (e * d) ** 2

    def kappa(self, e):
        return self.f(e) - e * self.df(e)

    def sig3(self, B, s):
        """vectorised (Sigma, dB, ds); inf where B >= (1 - s) a ; (0, 0, 0) where B/(1-s) <= theta(inf)."""
        B = np.atleast_1d(np.asarray(B, dtype=float)); s = np.atleast_1d(np.asarray(s, dtype=float))
        B, s = np.broadcast_arrays(B, s)
        y = 1.0 - s
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(y > 0, B / np.where(y > 0, y, 1.0), np.inf)
        bad = ~(t < self.a)                       # also catches s >= 1 and nan
        zero = t <= self.finf
        lo = np.full(B.shape, math.log(self.lo_e)); hi = np.full(B.shape, math.log(self.hi_e))
        tt = np.where(bad | zero, 0.5 * (self.a + self.finf), t)
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            k = self.kappa(np.exp(mid))
            up = k > tt                           # kappa decreasing: root is to the right
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        e = np.exp(0.5 * (lo + hi))
        th = self.f(e)
        Sig = -y * self.df(e)
        dB = 1.0 / e
        ds = th / e
        Sig = np.where(zero, 0.0, Sig); dB = np.where(zero, 0.0, dB); ds = np.where(zero, 0.0, ds)
        Sig = np.where(bad, np.inf, Sig); dB = np.where(bad, np.inf, dB); ds = np.where(bad, np.inf, ds)
        return Sig, dB, ds

    def sig3s(self, B, s):
        S, dB, ds = self.sig3(np.array([B]), np.array([s]))
        return float(S[0]), float(dB[0]), float(ds[0])

    def setup(self):
        lo, hi = 0.0, self.a
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if float(self.f(np.array(mid))) > mid:
                lo = mid
            else:
                hi = mid
        self.h = h = 0.5 * (lo + hi)
        r = -float(self.df(np.array(h)))
        self.r = r
        self.L = r / (1 + r)
        self.vartheta = float(self.d2f(np.array(h))) / (1 + r) ** 3
        self.const = 2 * math.pi ** 2 * h * h * self.vartheta
        return self

    # orbit p_j(B) and its derivative at a scalar B
    def orbit(self, B, n):
        p, dp = 0.0, 0.0
        for _ in range(n):
            S, dB, ds = self.sig3s(B, p)
            if not math.isfinite(S):
                return math.inf, math.inf
            p, dp = S, dB + ds * dp
        return p, dp


class SGauss(Smooth):
    name = "Gaussian (1 - sqrt e)^2"
    a, finf = 1.0, 0.0
    hi_e = 1.0

    def f(self, e):
        return np.where(e < 1, (1 - np.sqrt(np.minimum(e, 1.0))) ** 2, 0.0)

    def df(self, e):
        r = np.sqrt(np.minimum(e, 1.0))
        return np.where(e < 1, -(1 - r) / r, 0.0)


class SExpo(Smooth):
    def __init__(self, a=1.0, c=0.3, d=0.0):
        self.a, self.c, self.d, self.finf = a, c, d, d
        self.name = "expo: theta = %g + %g exp(-e/%g)" % (d, a - d, c)
        self.hi_e = 60 * c

    def f(self, e):
        return self.d + (self.a - self.d) * np.exp(-e / self.c)

    def df(self, e):
        return -(self.a - self.d) / self.c * np.exp(-e / self.c)


class SRecip(Smooth):
    def __init__(self, a=1.0, c=0.5, r=2.0):
        self.a, self.c, self.rr, self.finf = a, c, r, 0.0
        self.name = "recip: theta = %g/(1 + e/%g)^%g" % (a, c, r)
        self.hi_e = 1e9 * c

    def f(self, e):
        return self.a / (1 + e / self.c) ** self.rr

    def df(self, e):
        return -self.a * self.rr / self.c / (1 + e / self.c) ** (self.rr + 1)


class SPower(Smooth):
    """theta = a (1 - (e/c)^q)^r on e < c, 0 beyond; 0 < q <= 1, r > 1."""
    def __init__(self, a=1.0, c=0.7, q=0.35, r=1.5):
        self.a, self.c, self.q, self.rr, self.finf = a, c, q, r, 0.0
        self.name = "power: theta = %g (1 - (e/%g)^%g)^%g" % (a, c, q, r)
        self.hi_e = c

    def f(self, e):
        z = np.minimum(e / self.c, 1.0)
        return self.a * (1 - z ** self.q) ** self.rr

    def df(self, e):
        z = np.minimum(e / self.c, 1.0)
        return np.where(e < self.c, -self.a * self.rr * self.q / self.c * z ** (self.q - 1) * (1 - z ** self.q) ** (self.rr - 1), 0.0)


def make(name):
    if name == "gauss":
        return SGauss().setup()
    kind, *args = name.split(":")
    args = [float(x) for x in args]
    return {"expo": SExpo, "recip": SRecip, "power": SPower}[kind](*args).setup()


# ---- scalar (pure python) versions, for long orbits -------------------------------------------------------------
def _scalarise(P):
    """attach fs, dfs (scalar theta, theta') and a fast scalar sig3f(B, s) to the pair P."""
    if isinstance(P, SGauss):
        P.fs = lambda e: (1 - math.sqrt(e)) ** 2 if e < 1 else 0.0
        P.dfs = lambda e: -(1 - math.sqrt(e)) / math.sqrt(e) if e < 1 else 0.0
    elif isinstance(P, SExpo):
        a, c, d = P.a, P.c, P.d
        P.fs = lambda e: d + (a - d) * math.exp(-e / c)
        P.dfs = lambda e: -(a - d) / c * math.exp(-e / c)
    elif isinstance(P, SRecip):
        a, c, r = P.a, P.c, P.rr
        P.fs = lambda e: a / (1 + e / c) ** r
        P.dfs = lambda e: -a * r / c / (1 + e / c) ** (r + 1)
    elif isinstance(P, SPower):
        a, c, q, r = P.a, P.c, P.q, P.rr
        P.fs = lambda e: a * (1 - (e / c) ** q) ** r if e < c else 0.0
        P.dfs = lambda e: -a * r * q / c * (e / c) ** (q - 1) * (1 - (e / c) ** q) ** (r - 1) if e < c else 0.0
    llo, lhi = math.log(P.lo_e), math.log(P.hi_e)
    fs, dfs, A, finf = P.fs, P.dfs, P.a, P.finf

    def sig3f(B, s):
        y = 1.0 - s
        if y <= 0 or B >= y * A:
            return math.inf, math.inf, math.inf
        t = B / y
        if t <= finf:
            return 0.0, 0.0, 0.0
        lo, hi = llo, lhi
        for _ in range(64):
            mid = 0.5 * (lo + hi)
            e = math.exp(mid)
            if fs(e) - e * dfs(e) > t:
                lo = mid
            else:
                hi = mid
        e = math.exp(0.5 * (lo + hi))
        return -y * dfs(e), 1.0 / e, fs(e) / e, e
    P.sig3f = sig3f

    def orbitf(B, n):
        p, dp = 0.0, 0.0
        for _ in range(n):
            r_ = sig3f(B, p)
            if not math.isfinite(r_[0]):
                return math.inf, math.inf
            p, dp = r_[0], r_[1] + r_[2] * dp
        return p, dp
    P.orbitf = orbitf
    return P


_make0 = make


def make(name):
    return _scalarise(_make0(name))


# ---- the cube, parametrised by rho in (p_u, 1/2): e = KL(rho || p_u), theta = KL(rho || 1/2) -------------------
class SCube(Smooth):
    """theta'(e) = l/(l + u), l = ln(rho/(1 - rho)) < 0;  kappa = theta - e theta' decreases in rho from a to 0."""
    finf = 0.0

    def __init__(self, u):
        self.u = u
        self.pu = 1.0 / (1.0 + math.exp(u))
        pu = self.pu
        self.a = pu * math.log(2 * pu) + (1 - pu) * math.log(2 * (1 - pu))
        self.name = "cube u = %g (own parametrisation by rho)" % u

    def _par(self, rho):
        pu, u = self.pu, self.u
        l = np.log(rho / (1 - rho))
        e = rho * np.log(rho / pu) + (1 - rho) * np.log((1 - rho) / (1 - pu))
        th = rho * np.log(2 * rho) + (1 - rho) * np.log(2 * (1 - rho))
        dth = l / (l + u)
        return e, th, dth

    def f(self, e):
        # invert e -> rho by bisection (vectorised)
        e = np.atleast_1d(np.asarray(e, dtype=float))
        lo = np.full(e.shape, self.pu); hi = np.full(e.shape, 0.5)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            ee = self._par(mid)[0]
            up = ee < e
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        rho = 0.5 * (lo + hi)
        th = self._par(rho)[1]
        estar = self._par(np.array([0.5]))[0][0]
        return np.where(e >= estar, 0.0, th)

    def df(self, e):
        e = np.atleast_1d(np.asarray(e, dtype=float))
        lo = np.full(e.shape, self.pu); hi = np.full(e.shape, 0.5)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            ee = self._par(mid)[0]
            up = ee < e
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        return self._par(0.5 * (lo + hi))[2]

    def sig3(self, B, s):
        B = np.atleast_1d(np.asarray(B, dtype=float)); s = np.atleast_1d(np.asarray(s, dtype=float))
        B, s = np.broadcast_arrays(B, s)
        y = 1.0 - s
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(y > 0, B / np.where(y > 0, y, 1.0), np.inf)
        bad = ~(t < self.a)
        zero = t <= 0
        tt = np.where(bad | zero, 0.5 * self.a, t)
        lo = np.full(B.shape, self.pu); hi = np.full(B.shape, 0.5)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            e, th, dth = self._par(mid)
            up = th - e * dth > tt
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        e, th, dth = self._par(0.5 * (lo + hi))
        Sig, dB, ds = -y * dth, 1.0 / e, th / e
        Sig = np.where(zero, 0.0, Sig); dB = np.where(zero, 0.0, dB); ds = np.where(zero, 0.0, ds)
        return np.where(bad, np.inf, Sig), np.where(bad, np.inf, dB), np.where(bad, np.inf, ds)


def _scalarise_cube(P):
    pu, u, A = P.pu, P.u, P.a
    log = math.log

    def par(rho):
        l = log(rho / (1 - rho))
        e = rho * log(rho / pu) + (1 - rho) * log((1 - rho) / (1 - pu))
        th = rho * log(2 * rho) + (1 - rho) * log(2 * (1 - rho))
        return e, th, l / (l + u)

    def sig3f(B, s):
        y = 1.0 - s
        if y <= 0 or B >= y * A:
            return math.inf, math.inf, math.inf
        if B <= 0:
            return 0.0, 0.0, 0.0
        t = B / y
        lo, hi = pu, 0.5
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            e, th, dth = par(mid)
            if th - e * dth > t:
                lo = mid
            else:
                hi = mid
        e, th, dth = par(0.5 * (lo + hi))
        return -y * dth, 1.0 / e, th / e, e
    P.sig3f = sig3f

    def orbitf(B, n):
        p, dp = 0.0, 0.0
        for _ in range(n):
            r_ = sig3f(B, p)
            if not math.isfinite(r_[0]):
                return math.inf, math.inf
            p, dp = r_[0], r_[1] + r_[2] * dp
        return p, dp
    P.orbitf = orbitf
    return P


_make1 = make


def make(name):
    if name.startswith("cube:"):
        P = SCube(float(name.split(":")[1]))
        # fixed point etc. through the parametrisation: theta(h) = h
        lo, hi = P.pu, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            e, th, dth = P._par(np.array(mid))
            if float(th) > float(e):
                lo = mid
            else:
                hi = mid
        rho = 0.5 * (lo + hi)
        e, th, dth = [float(x) for x in P._par(np.array(rho))]
        P.h = e
        r = -dth
        P.r = r
        P.L = r / (1 + r)
        # theta'' = d(dth)/de = (d dth/d rho)/(de/d rho);  d dth/d rho = u/((l+u)^2 rho (1-rho)), de/d rho = l + u
        l = math.log(rho / (1 - rho))
        d2 = P.u / ((l + P.u) ** 3 * rho * (1 - rho))
        P.vartheta = d2 / (1 + r) ** 3
        P.const = 2 * math.pi ** 2 * P.h ** 2 * P.vartheta
        return _scalarise_cube(P)
    return _make1(name)
