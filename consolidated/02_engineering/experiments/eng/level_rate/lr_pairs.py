"""Pairs of exponent functions for the level recursion (independent check of "Theorem R").

Everything here is written from the mathematical statements of the theory division's reports
(docs/workstreams/R_REPORT.md and docs/THEORY_REPORT.md, sections 11.16, 11.18, 11.20, 11.21, 11.26, read at
the pinned commit named in results/*.json), not from its code.

A *pair* is given by a game function ``F`` on [0, 1] (THEORY_REPORT 11.21, Theorem 11.66): continuous,
``F(0) = F(1) = 0``.  From it

    hinted exponent        R(e)      = max_{0<=t<=1} [F(t) - t e]
    shear                  S(e)      = e + R(e)
    non-adaptive exponent  theta_na  = R o S^{-1}

and, when F is concave and differentiable, the graph of ``theta_na`` is the curve

    t in (0, 1)  |->  ( x(t), theta(t) ) = ( F(t) + (1 - t) F'(t),  F(t) - t F'(t) ),

traversed from (E, 0) at t = 0 to (0, a) at t = 1 (put e = F'(t): R(e) = F(t) - t e, x = e + R(e)); the slope of
``theta_na`` at x(t) is -t/(1 - t).  Constants:

    a = theta_na(0+) = -F'(1),   E = F'(0) (threshold),   h = max F = F(L) (the fixed point theta_na(h) = h),
    vartheta = -1/F''(L) = theta_hint''(0) = theta_na''(h)/(1 + |theta_na'(h)|)^3,
    predicted constant of Theorem R:  lim k^2 (tau_k - h) = 2 pi^2 h^2 vartheta.

The dual function of R_REPORT section 1, J(t) = inf_{e>0} [(1 - t) theta_na(e) + t e], equals F for concave F
(``dual_J_from_theta`` evaluates the infimum itself, for the numerical check of hypothesis (H1)).

Pairs implemented:

* ``GaussPair``            F = t(1 - t):  theta_na = (1 - sqrt x)^2, theta_hint = (1 - e)^2/4   (11.21(d));
* ``SitePair``             products of binary sites, F = sum_j lambda_j F_j (Theorem 11.98(b)):
    - symmetric site of slope u:  F_j(t) = (1 - t) ln 2 - ln(p^t + q^t),  p = 1/(1 + e^u)   (the cube: one site);
    - biased site (site law (1 - p, p), slope u): F_j(t) = (1 - t) C_t, the Renyi capacity of order t of the
      two-input channel of the vertex Gibbs laws (Theorem 11.99), in closed form (see ``_biased_terms``);
      cross-checked in the tests against the cosh form of Theorem 11.59(b) maximised over the residual field;
* ``CubeKL``               the cube through the formulas of 11.16 (Kullback-Leibler form), independent of F;
* ``KinkedPair``, ``PowerTopPair``   pairs that violate hypothesis (H1) (R_REPORT section 9), for negative controls.

No absolute paths, no I/O.
"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np

LN2 = math.log(2.0)


# ----------------------------------------------------------------------------------------------------------------
# site functions, double precision (vectorised in t) -- written so that nothing cancels near t = 0 and t = 1
# ----------------------------------------------------------------------------------------------------------------
def _sym_terms(u: float, t):
    """F, F', F'' of the symmetric binary site of slope u:  F(t) = Lambda(tu) - t Lambda(u),
    Lambda(v) = ln(2/(1 + e^{-v}))  (= (1 - t) ln 2 - ln(p^t + q^t), p = 1/(1 + e^u))."""
    t = np.asarray(t, dtype=float)
    w = 1.0 - t
    pu = 1.0 / (1.0 + math.exp(u))
    lam_u = LN2 - math.log1p(math.exp(-u))
    # Lambda(tu) - Lambda(u) = -log1p(p_u * expm1(u w))
    f = w * lam_u - np.log1p(pu * np.expm1(u * w))
    ptu = 1.0 / (1.0 + np.exp(t * u))            # 1/(1 + e^{tu})
    d1 = -lam_u + u * ptu
    d2 = -u * u * ptu * (1.0 - ptu)
    return f, d1, d2


def _biased_laws(p: float, u: float):
    """The two vertex Gibbs laws of a two-letter site with site law (1 - p, p) and slope u: the Lipschitz
    polytope is {gamma(1) - gamma(0) in [-u, u]}, its vertices are gamma = +-u on the letter 1, and
    pi_gamma is proportional to pi * exp(-gamma)."""
    q = 1.0 - p
    zp = q + p * math.exp(-u)
    zm = q + p * math.exp(u)
    return (q / zp, p * math.exp(-u) / zp), (q / zm, p * math.exp(u) / zm)


def _biased_terms(p: float, u: float, t):
    """F and F' of the biased binary site: F(t) = -t ln min_M sum_a (M P+(a)^t + (1 - M) P-(a)^t)^{1/t}
    (Theorem 11.99; the programme is convex in M).  Stationarity in M gives, with A_a = P+(a)^t, B_a = P-(a)^t,
    m_a = M A_a + (1 - M) B_a:  (m_0/m_1)^{(1-t)/t} = (B_1 - A_1)/(A_0 - B_0) =: ratio, hence
    M = (kap B_1 - B_0)/((A_0 - B_0) + kap (B_1 - A_1)), kap = ratio^{t/(1-t)}.  F' by the envelope theorem.
    Written with expm1/log1p so that the forms 1^infinity (t -> 1) and 0/0 (t -> 0) lose no digits:
    the absolute errors of F and F' are of the order of the rounding unit for 0 < t < 1."""
    t = np.asarray(t, dtype=float)
    w = 1.0 - t
    (a0, a1), (b0, b1) = _biased_laws(p, u)
    la0, la1, lb0, lb1 = math.log(a0), math.log(a1), math.log(b0), math.log(b1)
    ea0, ea1, eb0, eb1 = np.expm1(t * la0), np.expm1(t * la1), np.expm1(t * lb0), np.expm1(t * lb1)   # A - 1, B - 1
    D0 = ea0 - eb0                                   # A_0 - B_0 > 0
    D1 = ea1 - eb1                                   # A_1 - B_1 < 0
    # ratio - 1 = -(D0 + D1)/D0 and D0 + D1 = sum_a A_a - sum_a B_a, with sum_a A_a - 1 = sum_a a_a (a_a^{-w} - 1)
    SA1 = a0 * np.expm1(-w * la0) + a1 * np.expm1(-w * la1)
    SB1 = b0 * np.expm1(-w * lb0) + b1 * np.expm1(-w * lb1)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        logratio = np.where(t > 0.5, np.log1p(-(SA1 - SB1) / D0), np.log(-D1 / D0))
        kap1 = np.expm1(t / w * logratio)            # kap - 1
        num = kap1 * (1.0 + eb1) + (eb1 - eb0)       # kap B_1 - B_0
        den = (D0 - D1) - kap1 * D1
        M = num / den
        mm0 = M * ea0 + (1.0 - M) * eb0              # m_0 - 1
        mm1 = M * ea1 + (1.0 - M) * eb1
        l0, l1 = np.log1p(mm0), np.log1p(mm1)
        g0, g1 = np.exp(l0 / t), np.exp(l1 / t)
        G = g0 + g1
        # G - 1 = [sum_a m_a - 1] + sum_a m_a (m_a^{w/t} - 1), and sum_a m_a - 1 = M (sum A - 1) + (1 - M)(sum B - 1)
        G1 = M * SA1 + (1.0 - M) * SB1 + (1.0 + mm0) * np.expm1(w / t * l0) + (1.0 + mm1) * np.expm1(w / t * l1)
        lnG = np.where(t > 0.5, np.log1p(G1), np.log(G))
        f = -t * lnG
        dm0 = M * (1.0 + ea0) * la0 + (1.0 - M) * (1.0 + eb0) * lb0
        dm1 = M * (1.0 + ea1) * la1 + (1.0 - M) * (1.0 + eb1) * lb1
        dG = g0 * (-l0 / t**2 + dm0 / (t * (1.0 + mm0))) + g1 * (-l1 / t**2 + dm1 / (t * (1.0 + mm1)))
        d1 = -lnG - t * dG / G
    return f, d1


def _mp_sym(u, t):
    u = mp.mpf(u)
    t = mp.mpf(t)
    return (mp.log(2) - mp.log1p(mp.exp(-t * u))) - t * (mp.log(2) - mp.log1p(mp.exp(-u)))


def _mp_biased(p, u, t):
    p, u, t = mp.mpf(p), mp.mpf(u), mp.mpf(t)
    if t <= 0 or t >= 1:
        return mp.mpf(0)
    q = 1 - p
    zp, zm = q + p * mp.exp(-u), q + p * mp.exp(u)
    a0, a1, b0, b1 = q / zp, p * mp.exp(-u) / zp, q / zm, p * mp.exp(u) / zm
    A0, A1, B0, B1 = a0**t, a1**t, b0**t, b1**t
    kap = ((B1 - A1) / (A0 - B0)) ** (t / (1 - t))
    M = (kap * B1 - B0) / ((A0 - B0) + kap * (B1 - A1))
    m0, m1 = M * A0 + (1 - M) * B0, M * A1 + (1 - M) * B1
    return -t * mp.log(m0 ** (1 / t) + m1 ** (1 / t))


# ----------------------------------------------------------------------------------------------------------------
# the pair
# ----------------------------------------------------------------------------------------------------------------
class GamePair:
    """A pair defined by a concave, differentiable game function.  Subclasses give F, dF (double precision,
    vectorised) and F_mp (mpmath, scalar)."""

    name = "pair"
    smooth = True
    _const = None

    # --- to be supplied -----------------------------------------------------------------------------------
    def F(self, t):
        raise NotImplementedError

    def dF(self, t):
        raise NotImplementedError

    def F_mp(self, t):
        raise NotImplementedError

    # --- derived, high precision ----------------------------------------------------------------------------
    def _a_mp(self):
        """a = -F'(1) (one-sided numerical derivative in mpmath unless a subclass has a closed form)."""
        return -mp.diff(self.F_mp, 1, 1, direction=-1)

    def _E_mp(self):
        return mp.diff(self.F_mp, 0, 1, direction=1)

    def _L_float(self) -> float:
        lo, hi = 1e-12, 1.0 - 1e-12                  # F' decreases from E > 0 to -a < 0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if float(self.dF(np.array(mid))) > 0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def constants(self, dps: int = 40) -> dict:
        """a, E, L, h, vartheta = -1/F''(L), the predicted constant 2 pi^2 h^2 vartheta, and F'''(L) --
        from F in mpmath (derivatives by mpmath.diff; L by Newton's method on F')."""
        if self._const is not None and self._const["dps"] == dps:
            return self._const
        old = mp.mp.dps
        mp.mp.dps = dps
        try:
            a = self._a_mp()
            E = self._E_mp()
            L = mp.mpf(self._L_float())
            for _ in range(8):
                L = L - mp.diff(self.F_mp, L, 1) / mp.diff(self.F_mp, L, 2)
            h = self.F_mp(L)
            d2 = mp.diff(self.F_mp, L, 2)
            d3 = mp.diff(self.F_mp, L, 3)
            vth = -1 / d2
            self._const = dict(dps=dps, a=a, E=E, L=L, h=h, d2=d2, d3=d3, vartheta=vth,
                               constant=2 * mp.pi**2 * h**2 * vth)
        finally:
            mp.mp.dps = old
        return self._const

    @property
    def a(self) -> float:
        return float(self.constants()["a"])

    @property
    def E(self) -> float:
        return float(self.constants()["E"])

    @property
    def L(self) -> float:
        return float(self.constants()["L"])

    @property
    def h(self) -> float:
        return float(self.constants()["h"])

    @property
    def vartheta(self) -> float:
        return float(self.constants()["vartheta"])

    @property
    def constant(self) -> float:
        """2 pi^2 h^2 vartheta, the limit of k^2 (tau_k - h) claimed by Theorem R."""
        return float(self.constants()["constant"])

    # --- the dual function (for the line dynamics) --------------------------------------------------------------
    def J(self, t):
        """The dual function of R_REPORT section 1; equal to F because F is concave."""
        return self.F(t)

    # --- the curve of theta_na --------------------------------------------------------------------------------
    def curve(self, t):
        """(x(t), theta_na(x(t))) for t in [0, 1]."""
        t = np.asarray(t, dtype=float)
        f, d = self.F(t), self.dF(t)
        return f + (1.0 - t) * d, f - t * d

    def t_of_x(self, x, iters: int = 64):
        """The parameter t with x(t) = x (bisection; x(t) decreases from E at t = 0 to 0 at t = 1)."""
        x = np.asarray(x, dtype=float)
        lo = np.zeros(x.shape)
        hi = np.ones(x.shape)
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            big = self.curve(mid)[0] > x          # x(mid) too large -> t must grow
            lo = np.where(big, mid, lo)
            hi = np.where(big, hi, mid)
        return 0.5 * (lo + hi)

    def theta_na(self, x):
        """theta_na(x), by inversion of the curve (accurate; slow) -- 0 from E on, a at 0."""
        x = np.asarray(x, dtype=float)
        t = self.t_of_x(np.clip(x, 0.0, self.E))
        th = self.curve(t)[1]
        return np.where(x >= self.E, 0.0, np.where(x <= 0, self.a, th))

    def theta_hint(self, e):
        """R(e) = max_t [F(t) - t e] for 0 <= e (zero from E on)."""
        e = np.asarray(e, dtype=float)
        lo = np.zeros(e.shape)
        hi = np.ones(e.shape)
        for _ in range(64):                       # F' decreasing: solve F'(t) = e
            mid = 0.5 * (lo + hi)
            big = self.dF(mid) > e
            lo = np.where(big, mid, lo)
            hi = np.where(big, hi, mid)
        t = 0.5 * (lo + hi)
        return np.where(e >= self.E, 0.0, self.F(t) - t * e)

    def theta_table(self, n: int = 400_000):
        """Points (x_j, theta_j) of the graph of theta_na, x increasing from 0 to E, graded like x ~ j^4 near 0
        (theta_na has a square-root singularity at 0).  The piecewise-linear interpolant through exact points
        of a convex function lies ABOVE it: used as a majorant of theta_na in the upper-bound scheme."""
        j = np.arange(n + 1) / n
        w = j * j * (2.0 - j)                      # w = 1 - t, increasing from 0 to 1, w ~ 2 j^2 near 0
        x, th = self.curve(1.0 - w)
        x[0], th[0] = 0.0, self.a
        x[-1], th[-1] = self.E, 0.0
        if not (np.all(np.diff(x) > 0) and np.all(np.diff(th) <= 0)):
            raise ValueError("theta table is not monotone: the game function is not strictly concave?")
        return x, th

    # --- the dual function from theta_na itself ----------------------------------------------------------------
    def dual_J_from_theta(self, t: float, n: int = 20001) -> float:
        """J(t) = inf_{e>0} [(1 - t) theta_na(e) + t e] evaluated from theta_na (not from F): a scan over the
        curve followed by golden-section refinement in the curve parameter."""
        ts = np.linspace(1e-9, 1 - 1e-9, n)
        x, th = self.curve(ts)
        val = (1 - t) * th + t * x
        k = int(np.argmin(val))
        lo, hi = ts[max(k - 1, 0)], ts[min(k + 1, n - 1)]
        gr = (math.sqrt(5) - 1) / 2

        def f(tt):
            xx, tth = self.curve(np.array(tt))
            return float((1 - t) * tth + t * xx)

        c, d = hi - gr * (hi - lo), lo + gr * (hi - lo)
        fc, fd = f(c), f(d)
        for _ in range(80):
            if fc <= fd:
                hi, d, fd = d, c, fc
                c = hi - gr * (hi - lo)
                fc = f(c)
            else:
                lo, c, fc = c, d, fd
                d = lo + gr * (hi - lo)
                fd = f(d)
        return min(fc, fd, float(val[k]))

    def describe(self) -> dict:
        c = self.constants()
        return {k: float(c[k]) for k in ("a", "E", "L", "h", "vartheta", "constant", "d2", "d3")}


class GaussPair(GamePair):
    """The small-slope limit: F = t(1 - t); theta_na(x) = (1 - sqrt x)^2, theta_hint(e) = (1 - e)^2/4."""

    name = "gauss"

    def F(self, t):
        t = np.asarray(t, dtype=float)
        return t * (1.0 - t)

    def dF(self, t):
        t = np.asarray(t, dtype=float)
        return 1.0 - 2.0 * t

    def F_mp(self, t):
        t = mp.mpf(t)
        return t * (1 - t)

    def _a_mp(self):
        return mp.mpf(1)

    def _E_mp(self):
        return mp.mpf(1)

    def theta_na(self, x):
        x = np.asarray(x, dtype=float)
        return np.where(x >= 1, 0.0, (1 - np.sqrt(np.clip(x, 0, 1))) ** 2)

    def theta_hint(self, e):
        e = np.asarray(e, dtype=float)
        return np.where(e >= 1, 0.0, (1 - np.clip(e, 0, 1)) ** 2 / 4)


class SitePair(GamePair):
    """A product of binary sites: ``sites`` is a list of (fraction, slope u, site law p) with p = P(letter 1);
    p = 0.5 is the symmetric site.  F = sum_j fraction_j F_j (Theorem 11.98(b): one common slope t)."""

    def __init__(self, sites, name: str | None = None):
        tot = sum(s[0] for s in sites)
        if abs(tot - 1.0) > 1e-12:
            raise ValueError("fractions must sum to one")
        self.sites = [(float(lam), float(u), float(p)) for lam, u, p in sites]
        self.name = name or "sites " + ", ".join(f"({lam:g},{u:g},{p:g})" for lam, u, p in self.sites)
        self._const = None

    def _terms(self, t):
        t = np.asarray(t, dtype=float)
        f = np.zeros(t.shape)
        d = np.zeros(t.shape)
        for lam, u, p in self.sites:
            if p == 0.5:
                fj, dj, _ = _sym_terms(u, t)
            else:
                fj, dj = _biased_terms(p, u, np.clip(t, 1e-13, 1 - 1e-13))
            f = f + lam * fj
            d = d + lam * dj
        return f, d

    def F(self, t):
        return self._terms(t)[0]

    def dF(self, t):
        return self._terms(t)[1]

    def d2F(self, t):
        """Second derivative (symmetric sites only: closed form)."""
        t = np.asarray(t, dtype=float)
        out = np.zeros(t.shape)
        for lam, u, p in self.sites:
            if p != 0.5:
                raise NotImplementedError("closed-form F'' is implemented for symmetric sites only")
            out = out + lam * _sym_terms(u, t)[2]
        return out

    def F_mp(self, t):
        tot = mp.mpf(0)
        for lam, u, p in self.sites:
            tot += mp.mpf(lam) * (_mp_sym(u, t) if p == 0.5 else _mp_biased(p, u, t))
        return tot

    def _symmetric(self) -> bool:
        return all(p == 0.5 for _, _, p in self.sites)

    def _a_mp(self):
        # symmetric sites: a_j = KL(p_u || 1/2) = Lambda(u) - u p_u (closed form); otherwise numerical
        if not self._symmetric():
            return super()._a_mp()
        tot = mp.mpf(0)
        for lam, u, _ in self.sites:
            u = mp.mpf(u)
            tot += mp.mpf(lam) * (mp.log(2) - mp.log1p(mp.exp(-u)) - u / (1 + mp.exp(u)))
        return tot

    def _E_mp(self):
        # symmetric sites: E_j = ln cosh(u/2) (closed form); otherwise numerical
        if not self._symmetric():
            return super()._E_mp()
        return sum(mp.mpf(lam) * mp.log(mp.cosh(mp.mpf(u) / 2)) for lam, u, _ in self.sites)


def cube(u: float) -> SitePair:
    return SitePair([(1.0, u, 0.5)], name=f"cube u={u:g}")


def product2(u1: float, u2: float, lam1: float) -> SitePair:
    return SitePair([(lam1, u1, 0.5), (1.0 - lam1, u2, 0.5)], name=f"product u=({u1:g},{u2:g}) lambda1={lam1:g}")


def biased_cube(p: float, u: float) -> SitePair:
    return SitePair([(1.0, u, p)], name=f"biased cube p={p:g} u={u:g}")


# ----------------------------------------------------------------------------------------------------------------
# the cube through section 11.16 (no game function): for cross-checks
# ----------------------------------------------------------------------------------------------------------------
def kl_bin(x, y):
    """KL(x || y) for Bernoulli laws, natural logarithms."""
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = np.where(x > 0, x * np.log(x / y), 0.0)
        t2 = np.where(x < 1, (1 - x) * np.log((1 - x) / (1 - y)), 0.0)
    return t1 + t2


class CubeKL:
    """theta_na(e) = min{KL(rho || 1/2) : KL(rho || p_u) <= e},  theta_hint(e) = KL((Lambda_1 + e)/u || 1/2),
    a = KL(p_u || 1/2), h = KL(Lambda_1/u || 1/2), Lambda_1 = ln(2/(1 + e^{-u})), eps* = ln cosh(u/2)."""

    def __init__(self, u: float):
        self.u = u
        self.pu = 1 / (1 + math.exp(u))
        self.lam1 = math.log(2 / (1 + math.exp(-u)))
        self.E = math.log(math.cosh(u / 2))
        self.a = float(kl_bin(self.pu, 0.5))
        self.rho_h = self.lam1 / u
        self.h = float(kl_bin(self.rho_h, 0.5))
        # d^2/de^2 KL((Lambda_1 + e)/u || 1/2) at e = 0
        self.hint2 = 1 / (u * u * self.rho_h * (1 - self.rho_h))
        self.constant = 2 * math.pi**2 * self.h**2 * self.hint2

    def theta_hint(self, e):
        e = np.asarray(e, dtype=float)
        rho = (self.lam1 + e) / self.u
        return np.where(rho < 0.5, kl_bin(np.minimum(rho, 0.5), 0.5), 0.0)

    def theta_na(self, x):
        """The minimum is at the largest rho in [p_u, 1/2] with KL(rho || p_u) <= x (KL(. || 1/2) decreases
        on [0, 1/2], KL(. || p_u) increases on [p_u, 1/2])."""
        x = np.asarray(x, dtype=float)
        lo = np.full(x.shape, self.pu)
        hi = np.full(x.shape, 0.5)
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            ok = kl_bin(mid, self.pu) <= x
            lo = np.where(ok, mid, lo)
            hi = np.where(ok, hi, mid)
        out = kl_bin(0.5 * (lo + hi), 0.5)
        return np.where(x >= self.E, 0.0, np.where(x <= 0, self.a, out))


def biased_F_cosh(p, u, t, dps: int = 30):
    """F*(t) = max_{|gamma| <= u} F(gamma, t) with the closed form of Theorem 11.59(b):
        F(gamma, t) = ln{ [sinh(t(l+ - l)/2) C(l-)^t + sinh(t(l - l-)/2) C(l+)^t] / sinh(tu) } - t ln C(l),
        l = theta + gamma, l+- = theta +- u, C(x) = 2 cosh(x/2), theta = ln((1 - p)/p).
    Independent of the Renyi form used in SitePair; mpmath, scalar."""
    old = mp.mp.dps
    mp.mp.dps = dps
    try:
        p, u, t = mp.mpf(p), mp.mpf(u), mp.mpf(t)
        th = mp.log((1 - p) / p)
        lp, lm = th + u, th - u

        def C(x):
            return 2 * mp.cosh(x / 2)

        def Fg(g):
            lam = th + g
            num = mp.sinh(t * (lp - lam) / 2) * C(lm) ** t + mp.sinh(t * (lam - lm) / 2) * C(lp) ** t
            return mp.log(num / mp.sinh(t * u)) - t * mp.log(C(lam))

        # F(., t) vanishes at both ends of the window and has exactly one critical point (Proposition 11.65)
        g = mp.findroot(lambda g: mp.diff(Fg, g), (-u / 2, u / 2), solver="anderson")
        if abs(g) > u:
            raise ValueError("maximiser outside the window")
        return Fg(g)
    finally:
        mp.mp.dps = old


# ----------------------------------------------------------------------------------------------------------------
# pairs that violate (H1): negative controls (R_REPORT section 9)
# ----------------------------------------------------------------------------------------------------------------
class KinkedPair:
    """theta(e) = max(1 - 3e, 1/2 - e, 0) (R_REPORT, Proposition K): a = 1, h = 1/4, a kink at h;
    J(t) = min(1 - t, 1/4, t/2) is flat on [1/2, 3/4].  Not a smooth game function: only ``theta_table``,
    ``J`` and the constants are provided."""

    name = "kinked"
    smooth = False
    a, h, E = 1.0, 0.25, 0.5
    L1, L2 = 0.5, 0.75

    def theta_na(self, x):
        x = np.asarray(x, dtype=float)
        return np.maximum(np.maximum(1 - 3 * x, 0.5 - x), 0.0)

    def J(self, t):
        t = np.asarray(t, dtype=float)
        return np.minimum(np.minimum(1 - t, 0.25), t / 2)

    def theta_table(self, n: int = 0):
        x = np.array([0.0, 0.25, 0.5])
        return x, self.theta_na(x)


class PowerTopPair(GamePair):
    """F(t) = h (1 - |2t - 1|^p) with p > 2: a game function whose maximum is flatter than quadratic
    (h - J(t) ~ |t - L|^p), so (H1) fails (J''(L) = 0, vartheta = infinity).  R_REPORT section 9 expects
    tau_k - h ~ k^{-p/(p-1)} [labelled a heuristic there].  a = E = 2 p h."""

    def __init__(self, p: float = 4.0, h: float = 0.125):
        self.p, self.hh = float(p), float(h)
        self.name = f"power top p={p:g}"
        self._const = None

    def F(self, t):
        t = np.asarray(t, dtype=float)
        return self.hh * (1.0 - np.abs(2 * t - 1) ** self.p)

    def dF(self, t):
        t = np.asarray(t, dtype=float)
        z = 2 * t - 1
        return -2 * self.p * self.hh * np.sign(z) * np.abs(z) ** (self.p - 1)

    def F_mp(self, t):
        t = mp.mpf(t)
        return mp.mpf(self.hh) * (1 - abs(2 * t - 1) ** mp.mpf(self.p))

    def constants(self, dps: int = 40) -> dict:
        ph = self.p * self.hh
        return dict(dps=dps, a=mp.mpf(2 * ph), E=mp.mpf(2 * ph), L=mp.mpf("0.5"), h=mp.mpf(self.hh),
                    d2=mp.mpf(0), d3=mp.mpf(0), vartheta=mp.inf, constant=mp.inf)
