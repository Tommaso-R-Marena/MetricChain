"""Log-domain tables of the Hamming cube for the two-level algorithm (theory report §11.19).

Written from the definitions in ``docs/workstreams/K_REPORT.md`` §§0, 2.1 of the theory branch
(commit 63efc69), not from the workstream's code:

    |B(m, r)|   Hamming ball, |B(m, -1)| = 0
    E_r(m)    = sum_{j <= r} C(m, j) (e^{u (r + 1 - j)} - 1)
    T_m(k)    = sum_j C(m, j) e^{-u (j - k)_+}
    Gt(0)     = e^u - 1,      Gt(r) = E_r(m) / |B(m, r - 1)|   (r >= 1)        "one-sided ratio"
    kappa(r)  = the largest k >= 0 with |B(m, k)| <= max{1, c_eta |B(m, r - 1)|},  c_eta = (1 - eta)/(1 + eta)
    G2(r)     = E_r(m) / T_m(kappa(r))                                       "two-sided ratio"

Everything is stored as natural logarithms, so that cubes of 10^5 coordinates are harmless.
``brute_tables`` evaluates the same definitions with exact integers and ``math.fsum`` for
small ``m``; the unit tests compare the two.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np
from scipy.special import gammaln

LN2 = math.log(2.0)
TOL = 1e-10  # absolute tolerance when logarithms of counts are compared (rounding of sums of ~1e5 terms is ~1e-11)
TIE = 1e-9   # two logarithms of weights or levels closer than this are treated as equal (see meanrun.py, "Ties")


def _logcumsumexp(a: np.ndarray) -> np.ndarray:
    return np.logaddexp.accumulate(a)


@dataclass
class CubeTables:
    """Tables of the ``m``-cube for slope ``u``.  Index ``r`` runs over ``0..m``."""

    m: int
    u: float
    lbinom: np.ndarray = field(init=False, repr=False)   # ln C(m, j)
    lball: np.ndarray = field(init=False, repr=False)    # ln |B(m, r)|
    lE: np.ndarray = field(init=False, repr=False)       # ln E_r(m)
    lT: np.ndarray = field(init=False, repr=False)       # ln T_m(k)
    lGt: np.ndarray = field(init=False, repr=False)      # ln Gt(r)

    def __post_init__(self) -> None:
        m, u = self.m, self.u
        if m < 1 or u <= 0:
            raise ValueError("need m >= 1 and u > 0")
        j = np.arange(m + 1, dtype=float)
        self.lbinom = gammaln(m + 1.0) - gammaln(j + 1.0) - gammaln(m - j + 1.0)
        self.lball = _logcumsumexp(self.lbinom)
        # E_r = e^{u(r+1)} S_r - |B(r)|,  S_r = sum_{j<=r} C(m,j) e^{-uj};  |B(r)| / (e^{u(r+1)} S_r) <= e^{-u} < 1
        lS = _logcumsumexp(self.lbinom - u * j)
        lead = u * (j + 1.0) + lS
        self.lE = lead + np.log1p(-np.exp(self.lball - lead))
        # T_m(k) = |B(k)| + e^{uk} sum_{j>k} C(m,j) e^{-uj}
        suffix = _logcumsumexp((self.lbinom - u * j)[::-1])[::-1]          # ln sum_{j>=i} C(m,j) e^{-uj}
        above = np.concatenate([suffix[1:], [-np.inf]])                    # ln sum_{j>k}  ...
        self.lT = np.logaddexp(self.lball, u * j + above)
        self.lGt = np.concatenate([[math.log(math.expm1(u))], self.lE[1:] - self.lball[:-1]])

    # ------------------------------------------------------------------ balls
    def lball_at(self, r: int) -> float:
        """ln |B(m, r)| with the convention |B(m, -1)| = 0."""
        return -math.inf if r < 0 else float(self.lball[min(r, self.m)])

    def kball(self, logcount: float) -> int:
        """The largest k >= 0 with |B(m, k)| <= max{1, count}; ``logcount`` = ln(count).

        Reliable only for ``count <= c 2^m`` with ``c`` bounded away from 1 (consecutive balls
        near the top of the cube differ by less than rounding error in the log domain).  Every
        caller satisfies this: the counts are ``2^m p/(1 + eta)`` or ``c_eta |B(r-1)|``."""
        t = max(0.0, logcount) + TOL
        return max(int(np.searchsorted(self.lball, t, side="right")) - 1, 0)

    def radius(self, lq: float, l1mq: float | None = None) -> int:
        """The least r in 0..m with |B(m, r)| >= 2^m q, for ``lq`` = ln q <= 0.

        ``q = 1`` gives ``m`` exactly.  Near q = 1 the comparison is made on the complement,
        ``2^m - |B(m, r)| = |B(m, m - r - 1)| <= 2^m (1 - q)``, because ln|B(m, r)| is
        indistinguishable from m ln 2 long before r = m (the numerical form of the closure
        gap of DEAD_ENDS D45, item 4).  ``l1mq`` = ln(1 - q) may be supplied when it is known
        more accurately than log1p(-e^lq).
        """
        if lq < -LN2:
            return int(np.searchsorted(self.lball, self.m * LN2 + lq - TOL, side="left"))
        if l1mq is None:
            l1mq = math.log(-math.expm1(lq)) if lq < 0.0 else -math.inf
        if l1mq == -math.inf:
            return self.m
        # least r with |B(m, m-r-1)| <= 2^m (1-q): the largest admissible complement radius c = m-r-1
        c = int(np.searchsorted(self.lball, self.m * LN2 + l1mq + TOL, side="right")) - 1   # largest c with |B(c)| <= ...
        return self.m - c - 1 if c >= 0 else self.m

    # ------------------------------------------------------------------ ratios
    def kappa(self, eta: float) -> np.ndarray:
        """kappa(r) for r = 0..m."""
        lc = math.log((1.0 - eta) / (1.0 + eta))
        prev = np.concatenate([[-np.inf], self.lball[:-1]])                # ln |B(r-1)|
        t = np.maximum(0.0, lc + prev) + TOL
        return np.maximum(np.searchsorted(self.lball, t, side="right") - 1, 0)

    def lG2(self, eta: float) -> np.ndarray:
        """ln G2(r) for r = 0..m."""
        return self.lE - self.lT[self.kappa(eta)]

    def r_dagger(self, eta: float, theta: float, nu0: float) -> int:
        """The largest r in 0..m-1 such that for every r' <= r

            [N]  Gt(r') <= theta (1 - eta) nu0     and     [P]  min{ Gt(r')/c_eta, G2(r') } <= theta ;

        -1 if this fails at r' = 0."""
        lth = math.log(theta)
        lceta = math.log((1.0 - eta) / (1.0 + eta))
        okN = self.lGt <= lth + math.log((1.0 - eta) * nu0)
        okP = np.minimum(self.lGt - lceta, self.lG2(eta)) <= lth
        ok = (okN & okP)[: self.m]
        bad = np.flatnonzero(~ok)
        return (int(bad[0]) - 1) if bad.size else self.m - 1

    def lpi_dagger(self, r_dag: int) -> float:
        """ln pi_dagger = ln(|B(m, r_dagger)| / 2^m), and ln 2^{-m-1} if r_dagger = -1."""
        return (self.lball_at(r_dag) if r_dag >= 0 else -LN2) - self.m * LN2

    def log_binomial_tails(self, p: float) -> tuple[np.ndarray, np.ndarray]:
        """(ln P(Bin(m, p) <= r), ln P(Bin(m, p) >= r)) for r = 0..m."""
        j = np.arange(self.m + 1, dtype=float)
        lp = self.lbinom + j * math.log(p) + (self.m - j) * math.log1p(-p)
        return _logcumsumexp(lp), _logcumsumexp(lp[::-1])[::-1]


# ---------------------------------------------------------------------------------------------
# Constants of the cube class (theory report §11.16)
# ---------------------------------------------------------------------------------------------
def kl(a: float, b: float) -> float:
    """Binary relative entropy KL(a || b)."""
    out = 0.0
    if a > 0.0:
        out += a * math.log(a / b)
    if a < 1.0:
        out += (1.0 - a) * math.log((1.0 - a) / (1.0 - b))
    return out


@dataclass(frozen=True)
class CubeConstants:
    u: float
    p_u: float       # 1/(1 + e^u)
    Lambda1: float   # ln(2/(1 + e^-u))
    eps_star: float  # ln cosh(u/2)
    a: float         # KL(p_u || 1/2)            non-adaptive exponent at bounded accuracy
    h: float         # KL(Lambda1/u || 1/2)      hinted exponent at bounded accuracy


def cube_constants(u: float) -> CubeConstants:
    p_u = 1.0 / (1.0 + math.exp(u))
    lam1 = math.log(2.0 / (1.0 + math.exp(-u)))
    return CubeConstants(u, p_u, lam1, math.log(math.cosh(u / 2.0)), kl(p_u, 0.5), kl(lam1 / u, 0.5))


def theta_na(u: float, e: float) -> float:
    """min{KL(rho || 1/2) : KL(rho || p_u) <= e}; equals ``a`` at e = 0 and 0 from eps* on."""
    c = cube_constants(u)
    if e <= 0.0:
        return c.a
    if e >= c.eps_star:
        return 0.0
    lo, hi = c.p_u, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if kl(mid, c.p_u) <= e:
            lo = mid
        else:
            hi = mid
    return kl(lo, 0.5)


def theta_hint(u: float, e: float) -> float:
    """KL((Lambda1 + e)/u || 1/2), 0 from eps* on."""
    c = cube_constants(u)
    rho = (c.Lambda1 + e) / u
    return kl(rho, 0.5) if rho < 0.5 else 0.0


# ---------------------------------------------------------------------------------------------
# The same definitions by brute force (exact integers; used by the tests)
# ---------------------------------------------------------------------------------------------
def brute_tables(m: int, u: float, eta: float) -> dict[str, list]:
    """ball sizes (exact integers), E_r, T_m(k), Gt, kappa, G2 straight from the definitions."""
    binom = [math.comb(m, j) for j in range(m + 1)]
    ball = [sum(binom[: r + 1]) for r in range(m + 1)]
    E = [math.fsum(binom[j] * math.expm1(u * (r + 1 - j)) for j in range(r + 1)) for r in range(m + 1)]
    T = [math.fsum(binom[j] * math.exp(-u * max(j - k, 0)) for j in range(m + 1)) for k in range(m + 1)]
    Gt = [math.expm1(u)] + [E[r] / ball[r - 1] for r in range(1, m + 1)]
    c_eta = Fraction(str(eta))
    c_eta = (1 - c_eta) / (1 + c_eta)
    kappa = []
    for r in range(m + 1):
        bound = max(Fraction(1), c_eta * (ball[r - 1] if r >= 1 else 0))
        kappa.append(max(k for k in range(m + 1) if ball[k] <= bound))
    G2 = [E[r] / T[kappa[r]] for r in range(m + 1)]
    return dict(ball=ball, E=E, T=T, Gt=Gt, kappa=kappa, G2=G2)
