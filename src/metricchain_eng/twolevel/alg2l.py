"""Algorithm 2L+ (theory report §11.19, Theorem 11.56 = workstream K's Theorem K1): parameters,
the constants that the theorem derives from them, the base bracket family of Proposition
11.57(a) (= K0), and the asymptotic exponent the theory claims for the cost.

Written from the text of ``docs/workstreams/K_REPORT.md`` §§2.1-2.3, 3.2, 3.4 at theory commit
63efc69 (with the errata of referee report R8 listed at the head of that file), not from the
workstream's scripts.  All large numbers are natural logarithms.

Notation of the report:

    J     = ceil((2 u n + b + n_o ln 2)/lambda)
    nu0   = max{(J + 1)(e^lambda - 1)/eta', nu1} / (1 - eta)
    m_max = ceil(log2( 2 (1 + eta) e^lambda nu0 / ((1 - eta) pi_dagger) ))
    K     = ceil( 3 (1 + eta) eta^-2 ln( 2 (J + 1)(m_max + 1)(L + 2)/delta ) )
    nu    = K nu0,   M_dagger = K/((1 - eta) pi_dagger),   M_bar = 2 (1 + eta) e^lambda nu0 M_dagger
    delta' = delta/(4 L M_bar)
    cnt(x) = max{ K, 2 (1 + eta)^2 (1 - eta)^-1 e^lambda nu e^x }
    C_max  = 1 + 2 M_bar + sum_{l=1}^{L} min{ 2 M_bar, (J + 1) cnt(x_{l-1}) } C_l
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np

from .tables import LN2, CubeTables, cube_constants, theta_na


def logsumexp(values) -> float:
    arr = np.asarray(list(values), dtype=float)
    if arr.size == 0:
        return -math.inf
    mx = float(arr.max())
    if mx == -math.inf:
        return -math.inf
    return mx + math.log(float(np.exp(arr - mx).sum()))


@dataclass(frozen=True)
class Params:
    """Parameters of Algorithm 2L+.  ``xs`` is the ladder x_0 = 2 u n_i > x_1 > ... > x_L, x_L <= b.

    ``n_o = n`` (no inner block) is accepted for studies of the outer loop alone; the ladder
    then only supplies the number of rungs ``L`` that enters ``K``."""

    n: int
    n_o: int
    u: float
    lam: float      # ladder ratio e^lambda of the levels, 0 < lambda <= 1
    eta: float      # Chernoff factor, 0 < eta <= 1/2
    etap: float     # share of the negligible levels, 0 < eta' <= 1
    theta: float    # share of the tail, theta > 0
    nu1: float      # nu_1 >= 1
    b: float        # tolerance (= accuracy of the finest inner brackets), b > 0
    delta: float    # failure probability
    xs: tuple       # inner accuracies x_0 > x_1 > ... > x_L
    ltheta: float | None = None     # ln(theta), for designs whose theta overflows a double (the extensive regime of
                                    # theory report §11.18: theta = e^{x-b} - ...); then pass theta=math.inf

    @property
    def lth(self) -> float:
        """ln(theta); every computation uses this, never ``theta`` itself."""
        return math.log(self.theta) if self.ltheta is None else self.ltheta

    def __post_init__(self) -> None:
        if not (self.n >= 1 and 1 <= self.n_o <= self.n):
            raise ValueError("need 1 <= n_o <= n")
        if not (0 < self.lam <= 1 and 0 < self.eta <= 0.5 and 0 < self.etap <= 1 and self.theta > 0 and self.nu1 >= 1):
            raise ValueError("parameter outside the range of Theorem 11.56")
        xs = self.xs
        if len(xs) < 2:
            raise ValueError("the ladder needs at least one rung")
        if self.n_i == 0:
            return      # outer loop alone (controls): the ladder only supplies the number of rungs L
        if any(xs[i] <= xs[i + 1] for i in range(len(xs) - 1)):
            raise ValueError("the ladder must be strictly decreasing")
        if abs(xs[0] - 2 * self.u * self.n_i) > 1e-9 * max(1.0, xs[0]) or xs[-1] > self.b + 1e-12:
            raise ValueError("the ladder must start at 2 u n_i and end at or below b")

    @property
    def n_i(self) -> int:
        return self.n - self.n_o

    @property
    def L(self) -> int:
        return len(self.xs) - 1


@dataclass(frozen=True)
class Constants:
    """Everything Theorem 11.56 computes from the parameters (logarithms where the name starts with l)."""

    J: int
    nu0: float
    r_dag: int
    lpi_dag: float
    m_max: int
    K: int
    lK: float
    lnu: float
    lM_dag: float
    lM_bar: float
    l_inv_delta_p: float     # ln(1/delta')
    x_out: float             # certified accuracy ln[(2 p_u)^n + e^b (e^lam (1+eta)/(1-eta) + eta' + theta)]
    lMneg_cap: float         # ln((1 + eta) e^lam nu0 M_dagger): the bound of claim (iv) on M_j^neg
    lcount_factor: float     # ln((1 + eta)/(1 - eta) e^lam nu): claim (v) is  M_j^neg p(s_j e^-x) <= this * e^x

    def lcnt(self, x: float, P: Params) -> float:
        """ln cnt(x)."""
        return max(self.lK, math.log(2 * (1 + P.eta) ** 2 / (1 - P.eta)) + P.lam + self.lnu + x)


def constants(P: Params, outer: CubeTables) -> Constants:
    if outer.m != P.n_o or outer.u != P.u:
        raise ValueError("outer tables do not match the parameters")
    J = math.ceil((2 * P.u * P.n + P.b + P.n_o * LN2) / P.lam)
    nu0 = max((J + 1) * math.expm1(P.lam) / P.etap, P.nu1) / (1 - P.eta)
    r_dag = outer.r_dagger(P.eta, None, nu0, lth=P.lth)
    lpi = outer.lpi_dagger(r_dag)
    m_max = math.ceil((math.log(2 * (1 + P.eta) * nu0 / (1 - P.eta)) + P.lam - lpi) / LN2)
    K = math.ceil(3 * (1 + P.eta) / P.eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * (P.L + 2) / P.delta))
    lK = math.log(K)
    lnu = lK + math.log(nu0)
    lM_dag = lK - math.log(1 - P.eta) - lpi
    lM_bar = math.log(2 * (1 + P.eta) * nu0) + P.lam + lM_dag
    c = cube_constants(P.u)
    x_out = logsumexp([P.n * math.log(2 * c.p_u),
                       P.b + logsumexp([P.lam + math.log((1 + P.eta) / (1 - P.eta)), math.log(P.etap), P.lth])])
    return Constants(
        J=J, nu0=nu0, r_dag=r_dag, lpi_dag=lpi, m_max=m_max, K=K, lK=lK, lnu=lnu, lM_dag=lM_dag, lM_bar=lM_bar,
        l_inv_delta_p=math.log(4 * P.L / P.delta) + lM_bar, x_out=x_out,
        lMneg_cap=math.log((1 + P.eta) * nu0) + P.lam + lM_dag,
        lcount_factor=math.log((1 + P.eta) / (1 - P.eta)) + P.lam + lnu,
    )


def lowered_sample_cap(P: Params, outer: CubeTables, C: Constants, lK: float | None = None) -> float:
    """ln of the sample cap ``2 max{e^lam M_dagger, M_ddagger}`` of THY-RES-0004 §3 (the theory division's remark after
    Theorem 11.56; the corner ``r_dagger < Delta`` as closed in SCI-REV-0007 §2).  Claim: in every run of Algorithm
    2L+, on or off the good event, every sample is ``K`` or has fewer points than this.

    ``Delta = ceil(lam/u)``, ``pi_ddagger = 2^{-n_o} |B(n_o, r_dagger - Delta)|``, ``M_ddagger = K/((1 - eta) pi_ddagger)``,
    and ``M_ddagger = K 2^{n_o}/(1 - eta)`` if ``r_dagger < Delta``.  ``lK`` replaces ``ln K`` (runs with K scaled down).
    The constants ``m_max``, ``K`` and ``C_max`` of this module still use the theorem's ``M_bar``; this function is
    what the stored runs are tested against (``experiments/eng/twolevel/lowered_cap.py``)."""
    lK = C.lK if lK is None else lK
    lM_dag = lK - math.log(1 - P.eta) - C.lpi_dag
    delta = math.ceil(P.lam / P.u - 1e-12)
    if C.r_dag >= delta:
        lM_dd = lK - math.log(1 - P.eta) - (outer.lball_at(C.r_dag - delta) - P.n_o * LN2)
    else:
        lM_dd = lK + P.n_o * LN2 - math.log(1 - P.eta)
    return LN2 + max(P.lam + lM_dag, lM_dd)


# ---------------------------------------------------------------------------------------------
# The base family (Proposition 11.57(a) = K0): the two-sample bracket with a certified width
# ---------------------------------------------------------------------------------------------
@dataclass
class BaseFamily:
    """ln(number of evaluations) of the base bracket in dimension ``d`` for slope ``u``.

    eta = min(1/2, tanh(x/4));  K = ceil(3 (1 + eta) eta^-2 ln(4/delta'));  r* = the largest radius
    <= d - 1 with ln(1 + G2_d(r')) <= x - ln((1 + eta)/(1 - eta)) for all r' <= r*;
    M = ceil(K 2^d / ((1 - eta) |B(d, r*)|)); two samples, so 2M evaluations; enumeration of the
    cube (2^d evaluations) if no radius qualifies or if it is cheaper.
    """

    d: int
    u: float
    tables: CubeTables = field(init=False, repr=False)
    _g2: dict = field(init=False, repr=False, default_factory=dict)
    _cache: dict = field(init=False, repr=False, default_factory=dict)

    def __post_init__(self) -> None:
        self.tables = CubeTables(self.d, self.u)

    def _prefix_max_g2(self, eta: float) -> np.ndarray:
        key = round(eta, 12)
        if key not in self._g2:
            self._g2[key] = np.maximum.accumulate(self.tables.lG2(eta)[: self.d])
        return self._g2[key]

    def lcost(self, x: float, l_inv_delta: float) -> float:
        key = (round(x, 10), round(l_inv_delta, 8))
        if key in self._cache:
            return self._cache[key]
        d = self.d
        full = d * LN2
        eta = min(0.5, math.tanh(x / 4.0))
        budget = x - math.log((1 + eta) / (1 - eta))
        val = full
        if budget > 0.0:
            lim = math.log(math.expm1(budget)) if budget < 30.0 else budget     # ln(e^budget - 1)
            pm = self._prefix_max_g2(eta)
            r_star = int(np.searchsorted(pm, lim, side="right")) - 1           # all r' <= r* satisfy lG2 <= lim
            if r_star >= 0:
                K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4.0) + l_inv_delta))
                lM = math.log(K) + full - math.log(1 - eta) - self.tables.lball_at(r_star)
                lM = max(lM, math.log(K / (1 - eta)))
                val = min(full, LN2 + lM)
        self._cache[key] = val
        return val


@lru_cache(maxsize=64)
def base_family(d: int, u: float) -> BaseFamily:
    return BaseFamily(d, u)


def inner_costs(P: Params, C: Constants) -> np.ndarray:
    """ln C_l for l = 0..L with the base family inside; index 0 is the trivial bracket (one evaluation,
    already counted with the sampled point, so its entry is -inf)."""
    fam = base_family(P.n_i, P.u)
    return np.array([-math.inf] + [fam.lcost(x, C.l_inv_delta_p) for x in P.xs[1:]])


def lC_max(P: Params, C: Constants, lC: np.ndarray) -> float:
    """ln C_max of Theorem 11.56."""
    terms = [0.0, LN2 + C.lM_bar]
    for l in range(1, P.L + 1):
        terms.append(min(LN2 + C.lM_bar, math.log(C.J + 1) + C.lcnt(P.xs[l - 1], P)) + float(lC[l]))
    return logsumexp(terms)


# ---------------------------------------------------------------------------------------------
# What the theory claims asymptotically (K_REPORT (3.1), with T = theta_na, T(0) = a)
# ---------------------------------------------------------------------------------------------
def claimed_exponent(u: float, phi: float, rates: tuple) -> float:
    """max{ phi a, max_{1<=l<=L-1}[min(phi a, (1-phi) xi_{l-1}) + (1-phi) theta_na(xi_l)],
            min(phi a, (1-phi) xi_{L-1}) + (1-phi) a }      for the rates 2u = xi_0 > xi_1 > ... > xi_{L-1} > 0."""
    c = cube_constants(u)
    xi = (2.0 * u,) + tuple(rates)
    best = phi * c.a
    for l in range(1, len(xi)):
        best = max(best, min(phi * c.a, (1 - phi) * xi[l - 1]) + (1 - phi) * theta_na(u, xi[l]))
    return max(best, min(phi * c.a, (1 - phi) * xi[-1]) + (1 - phi) * c.a)


def tau2(u: float) -> tuple[float, float]:
    """(tau_2, minimising phi):  min_phi max((1-phi) a, phi a + (1-phi) theta_na(phi a/(1-phi)))."""
    c = cube_constants(u)
    best = (math.inf, 0.5)
    for i in range(1, 2000):
        phi = i / 2000.0
        v = max((1 - phi) * c.a, phi * c.a + (1 - phi) * theta_na(u, phi * c.a / (1 - phi)))
        if v < best[0]:
            best = (v, phi)
    return best


def hinted_lower_bound(n: int, u: float, eps: float, delta: float, tables: CubeTables | None = None) -> float:
    """ln[(1 - 2 delta) 2^n / |B(n, k*(eps))|], k*(eps) the least k with 2^-n E_k(n) > e^eps - 1
    (theory report Theorem 11.25(a))."""
    t = tables if tables is not None else CubeTables(n, u)
    target = n * LN2 + math.log(math.expm1(eps))
    k = int(np.searchsorted(t.lE, target, side="right"))
    k = min(k, n)
    return math.log(1 - 2 * delta) + n * LN2 - t.lball_at(k)
