"""Referee's own literal simulator of Algorithm 2L+ on cubes with site-dependent slopes (review of ENG-RES-0016 §2).

Written from the text of ``docs/workstreams/K_REPORT.md`` §§2.1-2.4 (theory branch, read with ``git show``) and the
table of substitutions of the draft's §2 — NOT from ``hetero.py`` / ``hetero_literal.py``, which are the objects under
review.  Nothing from the theory branch is executed.

Differences from the division's simulator, on purpose:
  * ball sizes, q, p_low, the Harper radius k and the closing radius r are exact (integers / Fractions);
  * the tables E_r, T_m, Gamma~, Gamma'' and r_dagger are computed here from the definitions (exact integers for the
    binomials, ``math.fsum`` in a log-shifted form for the sums);
  * every claim of Theorem K1 is checked in every run, pass by pass: (i) no abort / stop at a level <= J, (ii) L <= A <= U
    and the certificates p(s_j) <= q, p(s_j e^-b) >= p_low, l <= A at every update, (iii) q_j > pi_dagger at every level
    left, (iv) M_j^neg <= (1+eta) e^lam nu0 M_dagger and M <= M_bar, (v) the count, (vi) calls per level and rung and the
    total number of queries, the width and its four components;
  * the events (V2), (V3) that the proof uses on the run are evaluated on the realised sample, so that a violation can
    be attributed: "on the good event" (a counterexample to the proof) or "off it" (allowed, with probability <= delta);
  * adversarial inner oracles (always valid, ratio at most e^{x_l}) that see the level at which they are called.

Units: natural logarithms everywhere.
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

LN2 = math.log(2.0)


def limit_memory(gib: float) -> None:
    """A hard cap on the address space of this process (and of the workers it forks): an allocation beyond it raises
    MemoryError instead of exhausting the machine.  Every script of this review calls it first."""
    import resource

    lim = int(gib * 2 ** 30)
    resource.setrlimit(resource.RLIMIT_AS, (lim, lim))


TOL = 1e-9          # two logarithms closer than this are a tie; checks are made in the direction favourable to the claim
MARGIN = 1e-7       # the adversarial oracles keep this distance from the thresholds they aim at


# ---------------------------------------------------------------------------------------------
# Tables of the outer cube (K_REPORT §2.1), from the definitions
# ---------------------------------------------------------------------------------------------
def _lsum(terms):
    """ln of a sum of positive numbers given by their logarithms."""
    terms = [t for t in terms if t != -math.inf]
    if not terms:
        return -math.inf
    mx = max(terms)
    return mx + math.log(math.fsum(math.exp(t - mx) for t in terms))


def _lexpm1(z: float) -> float:
    """ln(e^z - 1) for z > 0."""
    return z + math.log(-math.expm1(-z)) if z > 30 else math.log(math.expm1(z))


class OuterTables:
    """ball sizes (exact), ln E_r, ln T_m(k), ln Gamma~, kappa, ln Gamma'' of Q_m with slope u; eta a Fraction."""

    def __init__(self, m: int, u: float, eta: Fraction, depth_cost=None):
        """``depth_cost(i)`` = U(i), the largest possible d(x, y) for two points at Hamming distance i (default u*i).
        With a non-default U the tables are the 'sorted slopes' tables for a mixed block (see mixed_outer.py)."""
        self.m, self.u, self.eta = m, u, Fraction(eta)
        U = (lambda i: u * i) if depth_cost is None else depth_cost
        self.binom = [math.comb(m, j) for j in range(m + 1)]
        self.ball = list(itertools.accumulate(self.binom))                      # |B(m, r)|, r = 0..m
        lbin = [math.log(c) for c in self.binom]
        lball = [math.log(c) for c in self.ball]
        # E_r = sum_{i>=1} (e^{U(i)} - e^{U(i-1)}) |B(m, r+1-i)|   (= sum_{j<=r} C(m,j)(e^{u(r+1-j)} - 1) for U(i) = u i)
        self.lE = []
        for r in range(m + 1):
            self.lE.append(_lsum(U(i - 1) + _lexpm1(U(i) - U(i - 1)) + lball[r + 1 - i] for i in range(1, r + 2)))
        # T_m(k) = sum_{i>=0} (e^{-U(i)} - e^{-U(i+1)}) |B(m, k+i)|  (= sum_j C(m,j) e^{-u (j-k)_+} for U(i) = u i); U(i) = +inf past m-k
        self.lT = []
        for k in range(m + 1):
            terms = []
            for i in range(0, m - k + 1):
                nxt = U(i + 1) if k + i + 1 <= m else math.inf
                w = -U(i) + (math.log(-math.expm1(-(nxt - U(i)))) if nxt != math.inf else 0.0)
                terms.append(w + lball[k + i])
            self.lT.append(_lsum(terms))
        self.lGt = [_lexpm1(U(1))] + [self.lE[r] - lball[r - 1] for r in range(1, m + 1)]
        c = (1 - self.eta) / (1 + self.eta)
        self.kappa = []
        for r in range(m + 1):
            bound = max(Fraction(1), c * (self.ball[r - 1] if r >= 1 else 0))
            self.kappa.append(max(k for k in range(m + 1) if self.ball[k] <= bound))
        self.lG2 = [self.lE[r] - self.lT[self.kappa[r]] for r in range(m + 1)]
        self.lbin = lbin

    def r_dagger(self, lth: float, nu0: float) -> int:
        lc = math.log(float((1 - self.eta) / (1 + self.eta)))
        lN = lth + math.log(float(1 - self.eta) * nu0)
        r = -1
        for rp in range(self.m):                                               # r' = 0..m-1
            if self.lGt[rp] <= lN and min(self.lGt[rp] - lc, self.lG2[rp]) <= lth:
                r = rp
            else:
                break
        return r

    def harper_k(self, count: Fraction) -> int:
        """the largest k >= 0 with |B(m, k)| <= max{1, count}."""
        bound = max(Fraction(1), count)
        k = 0
        while k + 1 <= self.m and self.ball[k + 1] <= bound:
            k += 1
        return k

    def closing_radius(self, count: Fraction) -> int:
        """the least r with |B(m, r)| >= count (count <= 2^m)."""
        r = 0
        while self.ball[r] < count:
            r += 1
        return r


def sorted_depth_cost(slopes):
    """U(i) = the sum of the i largest slopes (i <= m; continued linearly beyond m, where it is never used): the largest
    weighted distance between two points of the block at Hamming distance i."""
    srt = sorted((float(u) for u in slopes), reverse=True)
    cum = [0.0] + list(itertools.accumulate(srt))
    m = len(srt)
    return lambda i: cum[i] if i <= m else cum[m] + srt[0] * (i - m)


# ---------------------------------------------------------------------------------------------
# Parameters and constants (K_REPORT §2.2 with the substitutions of the draft's §2)
# ---------------------------------------------------------------------------------------------
@dataclass
class Design:
    us: tuple                 # slopes of all sites, the n_o outer ones first (one slope; several: the sorted-slope tables are used)
    n_o: int
    lam: float
    eta: Fraction
    etap: float
    lth: float                # ln theta
    nu1: float
    b: float
    xs: tuple                 # x_0 = 2 Omega_Y > x_1 > ... > x_L,  x_L <= b
    l_inv_delta: float = math.log(20.0)
    table_slope: float | None = None      # mutation / mixed outer block: the slope the outer tables are built for


@dataclass
class Consts:
    D: Design
    T: OuterTables
    Omega: float
    Omega_Y: float
    lPi: float                # ln prod_i 2 p_{u_i}
    J: int
    nu0: float
    r_dag: int
    lpi_dag: float
    m_max: int
    K: int
    x_out: float
    # the following depend on K and are recomputed when K is scaled down
    lnu: float = 0.0
    lM_dag: float = 0.0
    lM_bar: float = 0.0
    l_inv_delta_p: float = 0.0

    def set_K(self, K: int) -> None:
        D = self.D
        eta = float(D.eta)
        self.K = K
        self.lnu = math.log(K) + math.log(self.nu0)
        self.lM_dag = math.log(K) - math.log(1 - eta) - self.lpi_dag
        self.lM_bar = math.log(2 * (1 + eta) * self.nu0) + D.lam + self.lM_dag
        self.l_inv_delta_p = math.log(4 * (len(D.xs) - 1)) + D.l_inv_delta + self.lM_bar

    def lcnt(self, x: float) -> float:
        eta = float(self.D.eta)
        return max(math.log(self.K), math.log(2 * (1 + eta) ** 2 / (1 - eta)) + self.D.lam + self.lnu + x)

    def lCmax(self, lC=None) -> float:
        """ln C_max = ln[1 + 2 M_bar + sum_l min{2 M_bar, (J+1) cnt(x_{l-1})} C_l];  C_l = 1 by default."""
        xs = self.D.xs
        L = len(xs) - 1
        lC = [0.0] * L if lC is None else lC
        terms = [0.0, LN2 + self.lM_bar]
        for l in range(1, L + 1):
            terms.append(min(LN2 + self.lM_bar, math.log(self.J + 1) + self.lcnt(xs[l - 1])) + lC[l - 1])
        return _lsum(terms)

    def lcost_good(self) -> float:
        """ln[1 + M_bar + sum_l min{M_bar, (J+1) cnt(x_{l-1})}]: claim (vi), on the good event, C_l = 1."""
        xs = self.D.xs
        L = len(xs) - 1
        terms = [0.0, self.lM_bar]
        for l in range(1, L + 1):
            terms.append(min(self.lM_bar, math.log(self.J + 1) + self.lcnt(xs[l - 1])))
        return _lsum(terms)


def make_consts(D: Design, T: OuterTables | None = None, override: dict | None = None) -> Consts:
    """``override`` (cross-checks only): floats for Omega, Omega_Y, lPi computed elsewhere, so that two implementations
    resolve exact ties between brackets and levels in the same way (the sums differ in the last bit with the order)."""
    us = np.asarray(D.us, dtype=float)
    n_o = D.n_o
    u_o = float(us[:n_o].max())
    mixed = not np.all(us[:n_o] == u_o)
    eta = float(D.eta)
    Omega = float(us.sum())
    Omega_Y = float(us[n_o:].sum())
    lPi = float(np.sum(LN2 - np.log1p(np.exp(us))))
    if override:
        Omega, Omega_Y, lPi = override.get("Omega", Omega), override.get("Omega_Y", Omega_Y), override.get("lPi", lPi)
    L = len(D.xs) - 1
    if not (L >= 1 and abs(D.xs[0] - 2 * Omega_Y) < 1e-12 * max(1.0, D.xs[0]) and D.xs[-1] <= D.b + 1e-15
            and all(D.xs[i] > D.xs[i + 1] for i in range(L))):
        raise ValueError("ladder: x_0 = 2 Omega_Y > x_1 > ... > x_L, x_L <= b")
    J = math.ceil((2 * Omega + D.b + n_o * LN2) / D.lam)
    nu0 = max((J + 1) * math.expm1(D.lam) / D.etap, D.nu1) / (1 - eta)
    if T is None:
        if mixed:           # a mixed outer block: Lemma N14 (upper tail) and its mirror image (lower tail), slopes sorted along the depth
            T = OuterTables(n_o, u_o, D.eta, depth_cost=sorted_depth_cost(us[:n_o]))
        else:
            T = OuterTables(n_o, u_o if D.table_slope is None else D.table_slope, D.eta)
    r_dag = T.r_dagger(D.lth, nu0)
    lpi = (math.log(T.ball[r_dag]) if r_dag >= 0 else -LN2) - n_o * LN2
    m_max = math.ceil((math.log(2 * (1 + eta) * nu0 / (1 - eta)) + D.lam - lpi) / LN2)
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(2 * (J + 1) * (m_max + 1) * (L + 2)) + D.l_inv_delta))
    inside = _lsum([D.lam + math.log((1 + eta) / (1 - eta)), math.log(D.etap), D.lth])
    x_out = _lsum([lPi, D.b + inside])
    C = Consts(D=D, T=T, Omega=Omega, Omega_Y=Omega_Y, lPi=lPi, J=J, nu0=nu0, r_dag=r_dag, lpi_dag=lpi, m_max=m_max, K=K, x_out=x_out)
    C.set_K(K)
    return C


def geometric_ladder(x0: float, b: float, L: int) -> tuple:
    xs = [x0 * (b / x0) ** (l / L) for l in range(L + 1)]
    xs[-1] = b
    return tuple(xs)


# ---------------------------------------------------------------------------------------------
# Instances: psi on Q_n as a table, bit i of the index = coordinate i, outer coordinates first
# ---------------------------------------------------------------------------------------------
def all_points(n: int) -> np.ndarray:
    return ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)


def wdist(X, c, us):
    return np.abs(X - c[None, :]) @ us


def class_violation(psi: np.ndarray, us) -> float:
    n = len(us)
    idx = np.arange(2 ** n)
    return max(float(np.max(np.abs(psi - psi[idx ^ (1 << i)])) - us[i]) for i in range(n))


def lipschitz_minorant(v: np.ndarray, us) -> np.ndarray:
    """psi(x) = min_z [v(z) + d_u(x, z)]: the largest member of the class below v (one min-plus pass per coordinate)."""
    psi = v.copy()
    idx = np.arange(len(v))
    for i, u in enumerate(us):
        psi = np.minimum(psi, psi[idx ^ (1 << i)] + u)
    return psi


def instance(kind: str, us: np.ndarray, n_o: int, rng) -> np.ndarray:
    """A member of the class on Q_{n_o} x Q_{n_i}.  The kinds "outer_*" are products g(a) + F(y) whose outer landscape g
    is extremal for one step of the proof, with respect to the weighted metric of the outer block (for an outer block of
    one slope u_o: u_o times the Hamming distance)."""
    n = len(us)
    X = all_points(n)
    uo, ui = us[:n_o], us[n_o:]
    Xo, Xi = X[:, :n_o], X[:, n_o:]
    Om = float(us.sum())
    BIG = 1e6

    def rpt():
        return X[rng.integers(2 ** n)]

    def outer_parts():
        """points of the outer cube, a random centre, Hamming and weighted distances to it, the index of the outer point of every x."""
        Ao = all_points(n_o)
        c = Ao[rng.integers(2 ** n_o)]
        diff = np.abs(Ao - c[None, :])
        return Ao, diff.sum(axis=1), diff @ uo, Xo.astype(np.int64) @ (1 << np.arange(n_o))

    def some_inner():
        return inner_profile(rng.choice(["flat", "cone0", "anticone0", "linear", "rough"]), Xi, ui, rng)

    if kind == "flat":
        return np.zeros(2 ** n)
    if kind == "cone0":                      # l_initial = A exactly
        return wdist(X, X[0], us)
    if kind == "anticone0":                  # the reference point is the smallest weight; max W as far above s_0 as possible
        return -wdist(X, X[0], us)
    if kind == "cone":
        return wdist(X, rpt(), us)
    if kind == "anticone":
        return -wdist(X, rpt(), us)
    if kind == "dip":                        # the hard instance of the lower bound
        rho = rng.uniform(0.05, 1.0) * Om * 0.5
        return -np.maximum(rho - wdist(X, rpt(), us), 0.0)
    if kind in ("outer_dip", "outer_set"):
        # the largest outer landscape that is <= t outside a set D: W = t e^{dist(a, D^c)} on D — equality in the tail lemma
        # K.1(a) when D is a Hamming ball and the block has one slope.  D: a ball, or a ball plus part of the next shell.
        Ao, dH, dW, code = outer_parts()
        r = int(rng.integers(0, max(1, n_o // 2) + 1))
        inD = dH <= r
        if kind == "outer_set":
            inD = inD | ((dH == r + 1) & (rng.random(2 ** n_o) < rng.random()))
        if inD.all():
            inD[np.argmax(dH)] = False
        g = -lipschitz_minorant(np.where(inD, BIG, 0.0), uo)          # - (weighted distance to the complement of D)
        return g[code] + some_inner()
    if kind == "outer_cone":                 # fibre averages with the extreme outer slopes everywhere; extremal for Lemma K.1(b) at k = 0
        Ao, dH, dW, code = outer_parts()
        return rng.choice([-1.0, 1.0]) * dW[code] + some_inner()
    if kind == "outer_plateau":              # W = t on a ball S, t e^{-dist(a, S)} outside: equality in Lemma K.1(b) for one slope
        Ao, dH, dW, code = outer_parts()
        r = int(rng.integers(0, n_o))
        g = lipschitz_minorant(np.where(dH <= r, 0.0, BIG), uo)       # weighted distance to S
        return g[code] + some_inner()
    if kind == "linear":
        return X @ (us * rng.choice([-1.0, 1.0], size=n))
    if kind == "wells":
        f = np.full(2 ** n, np.inf)
        for _ in range(int(rng.integers(2, 6))):
            f = np.minimum(f, rng.uniform(0, Om) + wdist(X, rpt(), us))
        return f
    if kind == "ridges":
        f = np.full(2 ** n, -np.inf)
        for _ in range(int(rng.integers(2, 6))):
            f = np.maximum(f, rng.uniform(0, Om) - wdist(X, rpt(), us))
        return f
    if kind == "rough":                      # largest class member below noise of a random amplitude: generic, non-product
        amp = Om * 10 ** rng.uniform(-2, 0.3)
        return lipschitz_minorant(rng.uniform(0, amp, size=2 ** n), us)
    if kind == "rough_up":                   # smallest class member above noise
        amp = Om * 10 ** rng.uniform(-2, 0.3)
        return -lipschitz_minorant(rng.uniform(0, amp, size=2 ** n), us)
    if kind == "twofibre":                   # two fibre shapes glued: fibres differ from outer point to outer point, reference unrepresentative
        Ao, dH, dW, code = outer_parts()
        g1 = dW[code] * rng.choice([-1.0, 1.0])
        g2 = (Ao @ (uo * rng.choice([-1.0, 1.0], size=n_o)))[code]
        F1 = inner_profile("cone0", Xi, ui, rng)
        F2 = inner_profile("anticone0", Xi, ui, rng) + rng.uniform(-1, 1) * float(ui.sum())
        return np.minimum(g1 + F1, g2 + F2) if rng.random() < 0.5 else np.maximum(g1 + F1, g2 + F2)
    raise ValueError(kind)


def inner_profile(kind: str, Xi: np.ndarray, ui: np.ndarray, rng) -> np.ndarray:
    if kind == "flat":
        return np.zeros(len(Xi))
    if kind == "cone0":
        return Xi @ ui
    if kind == "anticone0":
        return -(Xi @ ui)
    if kind == "linear":
        return Xi @ (ui * rng.choice([-1.0, 1.0], size=len(ui)))
    if kind == "rough":
        n_i = len(ui)
        v = lipschitz_minorant(rng.uniform(0, float(ui.sum()) * 10 ** rng.uniform(-1.5, 0.3), size=2 ** n_i), ui)
        code = (Xi.astype(np.int64) @ (1 << np.arange(n_i)))
        return v[code]
    raise ValueError(kind)


INSTANCE_KINDS = ("flat", "cone0", "anticone0", "cone", "anticone", "dip", "outer_dip", "outer_set", "outer_cone", "outer_plateau", "linear", "wells",
                  "ridges", "rough", "rough_up", "twofibre")


# ---------------------------------------------------------------------------------------------
# Inner oracles: valid brackets [lo, hi] (logs) of the fibre average with hi - lo <= x
# ---------------------------------------------------------------------------------------------
def oracle(kind: str, lw: np.ndarray, x: np.ndarray, lsj: float, b: float, rng) -> tuple[np.ndarray, np.ndarray]:
    """delta in [0, x]: the bracket is [lw - delta, lw - delta + x]."""
    if kind == "bottom":
        d = np.zeros_like(lw)
    elif kind == "top":
        d = x.copy()
    elif kind == "mid":
        d = 0.5 * x
    elif kind == "random":
        d = rng.random(lw.size) * x
    elif kind in ("sticky_high", "sticky_low", "high", "low"):
        # unclassified iff hi > lsj and lo <= lsj - b  iff  lw - lsj + b <= delta < lw + x - lsj
        # Every choice is made with a margin MARGIN, so that the adversary never manufactures an exact tie U = s_j or
        # L = s_j e^-b (which exact arithmetic would classify and floating point may not: erratum m10).
        lo_d = np.maximum(0.0, lw - lsj + b + MARGIN)
        hi_d = np.minimum(x, lw + x - lsj - MARGIN)
        sticky = (lo_d < hi_d) if kind.startswith("sticky") else np.zeros(lw.size, dtype=bool)
        # high iff delta < lw - lsj + b and delta < lw + x - lsj (and delta >= 0)
        cap = np.minimum(lw - lsj + b, lw + x - lsj)
        can_high = cap > 4 * MARGIN
        d_high = np.minimum(x, 0.5 * np.maximum(cap, 0.0))
        # low iff lw - delta + x <= lsj iff delta >= lw + x - lsj (and delta <= x): possible iff lw <= lsj
        can_low = lw <= lsj - 2 * MARGIN
        d_low = np.clip(lw + x - lsj + MARGIN, 0.0, x)
        if kind.endswith("high"):
            d = np.where(can_high, d_high, np.where(can_low, d_low, 0.5 * x))
        else:
            d = np.where(can_low, d_low, np.where(can_high, d_high, 0.5 * x))
        d = np.where(sticky, lo_d, d)
    else:
        raise ValueError(kind)
    # [lw - d, lw + (x - d)]: valid by construction (0 <= d <= x), ratio x up to rounding; d = 0 and d = x are exact
    d = np.clip(d, 0.0, x)
    return lw - d, lw + (x - d)


ORACLES = ("bottom", "top", "mid", "random", "sticky_high", "sticky_low", "high", "low")


# ---------------------------------------------------------------------------------------------
# The algorithm, literal, with every claim checked
# ---------------------------------------------------------------------------------------------
@dataclass
class Report:
    status: str = ""
    level: int = -1
    M: int = 0
    lA: float = 0.0
    lL: float = -math.inf
    lU: float = math.inf
    width: float = math.inf
    queries: int = 0
    calls: list = field(default_factory=list)
    info_tie_abort: bool = False # an abort "unclassified at the last rung" that is a floating-point tie (erratum m10)
    good: bool = True            # the events (V2), (V3) the proof uses on this run hold (under every resolution of ties)
    ties: int = 0                # thresholds at which a fibre average lies within TOL
    viol: dict = field(default_factory=dict)      # claim -> number of violations
    info: dict = field(default_factory=dict)

    def add(self, claim: str, n: int = 1) -> None:
        self.viol[claim] = self.viol.get(claim, 0) + n


def run(psi: np.ndarray, C: Consts, orc: str, rng, mutation: str | None = None, trace: list | None = None) -> Report:
    """One literal run.  ``mutation`` (negative controls, wrong transfers):
        'omegaY_hom'  trivial fibre bracket with u_o n_i in place of Omega_Y
        'ell_hom'     first lower bound with the outer slope at every site
        'J_hom'       J with u_o n in place of Omega
        's0_hom'      s_0 with u_o n in place of Omega
        'no_harper'   no third term in step (b)
        'maxform'     lower end without the sum
    (wrong outer tables are a mutation of the constants: Design.table_slope)."""
    D, T = C.D, C.T
    us = np.asarray(D.us, dtype=float)
    n = len(us)
    n_o, n_i = D.n_o, n - D.n_o
    u_o = float(us[0])
    lam, b = D.lam, D.b
    eta = D.eta
    etaf = float(eta)
    xs = np.asarray(D.xs, dtype=float)
    L = len(xs) - 1
    K = C.K
    two_no = 2 ** n_o
    R = Report()

    tab = psi.reshape(2 ** n_i, two_no).T                         # tab[a, y]
    lW = np.logaddexp.reduce(-tab, axis=1) - n_i * LN2
    lA = float(np.logaddexp.reduce(lW) - n_o * LN2)
    R.lA = lA
    lWsorted = np.sort(lW)
    psi_ref = tab[:, 0]
    psi0 = float(psi[0])

    Omega = C.Omega if mutation != "s0_hom" else u_o * n
    ls0 = -psi0 - Omega
    lell = -psi0 - C.Omega - C.lPi                               # ln[e^-psi0 prod (1 + e^-u_i)/2]:  (1 + e^-u)/2 = e^-u/(2 p_u)
    if abs(lell - (-psi0 + float(np.sum(np.log((1 + np.exp(-us)) / 2))))) > 1e-9:
        raise AssertionError("first lower bound: the two forms disagree")
    if mutation == "ell_hom":
        lell = -psi0 + n * math.log((1 + math.exp(-u_o)) / 2)
    lell_init = lell
    J = C.J if mutation != "J_hom" else math.ceil((2 * u_o * n + b + n_o * LN2) / lam)
    half0 = C.Omega_Y if mutation != "omegaY_hom" else u_o * n_i

    def p_counts(lt):
        """(#{W > t} under 'ties are not above', under 'ties are above')."""
        lo = two_no - int(np.searchsorted(lWsorted, lt + TOL, side="right"))
        hi = two_no - int(np.searchsorted(lWsorted, lt - TOL, side="left"))
        return lo, hi

    queries = 1
    idx = np.empty(0, dtype=np.int64)
    wS = np.empty(0)                                             # ln W of the sample points (truth, for the checks)
    lo_ = np.empty(0)
    hi_ = np.empty(0)
    rung = np.empty(0, dtype=np.int16)
    calls = np.zeros(L + 1, dtype=np.int64)
    Mcap = K * 2 ** C.m_max
    lSigma = -math.inf
    upper = [ls0]
    lpop_part = -math.inf                                         # ln sum over populated levels left of (s_{i+1} - s_i) q_i
    lneg_part = -math.inf
    l1mel = math.log(-math.expm1(-lam))
    lel1 = math.log(math.expm1(lam))
    lceta = math.log(float((1 - eta) / (1 + eta)))
    lcount_factor = -lceta + lam + C.lnu                          # (1+eta)/(1-eta) e^lam nu
    lMneg_cap = math.log((1 + etaf) * C.nu0) + lam + C.lM_dag
    left = []                                                     # (level, kind, ln(s_i q_i))
    harper_ratio, tail_ratio = math.inf, None
    stopped = False
    status = ""
    j = 0

    def X_counts(M, lt):
        w = wS[:M]
        return int(np.count_nonzero(w > lt + TOL)), int(np.count_nonzero(w > lt - TOL))

    def event_V2(M, lt):
        ok = True
        for (X, pc) in zip(X_counts(M, lt), p_counts(lt)):
            p = Fraction(pc, two_no)
            ok &= (M * p <= Fraction(K) / (1 - eta)) or (X >= (1 - eta) * M * p)
        return ok

    def event_V3(M, lt):
        ok = True
        for (X, pc) in zip(X_counts(M, lt), p_counts(lt)):
            p = Fraction(pc, two_no)
            ok &= (X < K) or (X <= (1 + eta) * M * p)
        return ok

    for j in range(J + 1):
        lsj = ls0 + j * lam
        M = K
        lell_entry = lell
        lMneg = C.lnu + lsj - lell_entry - b
        if lMneg > lMneg_cap + 1e-9:
            R.add("(iv) M_j^neg <= (1+eta) e^lam nu0 M_dagger")
        calls_before = calls.copy()
        level_done = False
        while True:
            if M > Mcap:
                status = "abort: sample size"
                break
            if M > len(idx):
                new = rng.integers(0, two_no, size=M - len(idx))
                idx = np.concatenate([idx, new])
                wS = np.concatenate([wS, lW[new]])
                lo_ = np.concatenate([lo_, -psi_ref[new] - half0])
                hi_ = np.concatenate([hi_, -psi_ref[new] + half0])
                rung = np.concatenate([rung, np.zeros(len(new), dtype=np.int16)])
                queries += len(new)
            aborted = False
            while True:
                todo = np.flatnonzero((hi_[:M] > lsj) & (lo_[:M] <= lsj - b))
                if todo.size == 0:
                    break
                if np.any(rung[todo] >= L):
                    aborted = True
                    # K_REPORT erratum (m10): in exact arithmetic a valid bracket of ratio <= e^b cannot be unclassified; in floating
                    # point it can when U = s_j and L = s_j e^-b up to rounding.  Recorded so that such aborts are not counted
                    # against claim (i).
                    stuck = todo[rung[todo] >= L]
                    R.info_tie_abort = bool(np.all((np.abs(hi_[stuck] - lsj) < TOL) & (np.abs(lo_[stuck] - (lsj - b)) < TOL)))
                    break
                rung[todo] += 1
                x = xs[rung[todo]]
                nlo, nhi = oracle(orc, wS[todo], x, lsj, b, rng)
                lo_[todo] = np.maximum(lo_[todo], nlo)
                hi_[todo] = np.minimum(hi_[todo], nhi)
                np.add.at(calls, rung[todo], 1)
            if aborted:
                status = "abort: unclassified at the last rung"
                break
            N = int(np.count_nonzero(hi_[:M] > lsj))
            q = min(Fraction(1), Fraction(max(N, K)) / ((1 - eta) * M))
            lq = math.log(q)
            # (2.1): X_{s_j}(M) <= N <= X_{s_j e^-b}(M) — follows from the validity of the brackets alone
            if not (X_counts(M, lsj)[0] <= N <= X_counts(M, lsj - b)[1]):
                R.add("(2.1) X_{s_j} <= N <= X_{s_j e^-b}")
            # events the proof uses at this pass
            v2_here, v3_here = event_V2(M, lsj), event_V3(M, lsj - b)
            R.good &= v2_here and v3_here
            pc = p_counts(lsj)
            R.ties += pc[1] - pc[0]
            if Fraction(pc[0], two_no) > q:
                R.add("(ii) p(s_j) <= q")
                if v2_here:          # Step 2: (V2) at this very pass and (2.1) imply the certificate, whatever happened elsewhere
                    R.add(LOCAL_V2)
            lplow = None
            if N >= K:
                plow = Fraction(N) / ((1 + eta) * M)
                lplow = math.log(plow)
                if Fraction(p_counts(lsj - b)[1], two_no) < plow:
                    R.add("(ii) p(s_j e^-b) >= p_low")
                    if v3_here:      # Step 2: (V3) at this very pass and (2.1) imply the certificate
                        R.add(LOCAL_V3)
                k = T.harper_k(two_no * plow)
                # diagnostic: how close this pass comes to equality in the lower tail lemma (K.1(b)) as the algorithm uses it:
                # E min(W, t)/t against 2^-n_o T(k), t = s_j e^-b  (>= 1 when the lemma and the certificate hold)
                trunc_rel = float(np.mean(np.exp(np.minimum(lW - (lsj - b), 0.0))))
                harper_ratio = min(harper_ratio, trunc_rel / math.exp(T.lT[k] - n_o * LN2))
                lell = max(lell, lsj - b + lplow)
                if mutation != "no_harper":
                    lell = max(lell, lsj - b - n_o * LN2 + T.lT[k])
                if lell > lA + TOL:
                    R.add("(ii) l <= A")
            # closure test
            if two_no * q < 1:
                ltail = -math.inf
                r = -1
            else:
                r = T.closing_radius(two_no * q)
                ltail = lsj - n_o * LN2 + T.lE[r] if r <= n_o - 1 else math.inf
            if trace is not None:
                trace.append(dict(j=j, M=M, N=N, r=r, lq=lq, lell=lell, ltail=ltail))
            if ltail <= D.lth + b + lell:
                r_close, pop_close = r, N >= K
                if r >= 0:           # diagnostic: equality in the upper tail lemma (K.1(a)) as used: E(W - s_j)_+/s_j against 2^-n_o E_r  (<= 1)
                    excess_rel = float(np.mean(np.expm1(np.maximum(lW - lsj, 0.0))))
                    tail_ratio = excess_rel / math.exp(T.lE[r] - n_o * LN2)
                lLow = max(lell, lSigma)
                if N >= K and mutation != "maxform":
                    lLow = max(lLow, float(np.logaddexp(lSigma, l1mel - b + lsj + lplow)))
                if mutation == "maxform":
                    lLow = lell
                lUp = _lsum(upper + [ltail])
                stopped = True
                # width, term by term (Step 4; deterministic)
                if ls0 > C.lPi + lLow + TOL and mutation is None:
                    R.add("width: s_0 <= Pi L")
                if lpop_part > -lceta + lam + b + lLow + TOL:
                    R.add("width: populated part")
                if lneg_part > math.log(D.etap) + b + lLow + TOL:
                    R.add("width: negligible part")
                if ltail > D.lth + b + lLow + TOL:
                    R.add("width: tail")
                break
            # the level is left or the sample doubled: the test failed
            if N >= K or math.log(M) >= lMneg:
                # (iii) closing radius above r_dagger:  2^{n_o} q > |B(n_o, r_dagger)|
                if C.r_dag >= 0 and not (two_no * q > T.ball[C.r_dag]):
                    R.add("(iii) q_j > pi_dagger")
                term = lsj + lel1 + lq
                upper.append(term)
                if N >= K:
                    lpop_part = float(np.logaddexp(lpop_part, term))
                    lSigma = float(np.logaddexp(lSigma, l1mel - b + lsj + lplow))
                    left.append((j, "pop", lsj + lq))
                else:
                    lneg_part = float(np.logaddexp(lneg_part, term))
                    left.append((j, "neg", lsj + lq))
                    if not (q <= Fraction(K) / ((1 - eta) * M) and math.log(M) < C.lM_dag + 1e-12):
                        R.add("(iv) a negligible level has M < M_dagger")
                level_done = True
                break
            M *= 2
        # ---- checks at the end of the level (also when the run stops in it): sizes, the count, calls
        if not status:
            if math.log(M) > C.lM_bar + 1e-12:
                R.add("(iv) M <= M_bar")
            if not (M == K or math.log(M) < LN2 + lMneg + 1e-12):
                R.add("(iv) M <= max{K, 2 M_j^neg}")
            for l in range(0, L):
                lt = lsj - xs[l]
                good_here = event_V3(M, lt)
                R.good &= good_here
                pc_lo, pc_hi = p_counts(lt)
                R.ties += pc_hi - pc_lo
                # the count: M_j^neg p(s_j e^-x) <= c_eta^-1 e^lam nu e^x
                if pc_lo > 0 and lMneg + math.log(pc_lo) - n_o * LN2 > lcount_factor + xs[l] + TOL:
                    R.add("(v) the count")
                if X_counts(M, lt)[0] > math.exp(C.lcnt(xs[l])) * (1 + 1e-12):
                    R.add("(v) points above s_j e^-x <= cnt(x)")
                made = int(calls[l + 1] - calls_before[l + 1])
                if made > math.exp(min(C.lM_bar, C.lcnt(xs[l]))) * (1 + 1e-12):
                    R.add("(vi) calls of I_l in one level")
        if stopped or status:
            break
    else:
        status = "abort: level J left"

    R.queries = queries + int(calls.sum())
    R.calls = calls.tolist()
    R.level = j
    R.M = int(len(idx))
    if not stopped:
        R.status = status or "abort"
        if R.info_tie_abort:
            R.status = "abort: floating-point tie at the last rung (m10)"
        else:
            R.add("(i) abort")
        R.lL, R.lU = ls0, ls0 + 2 * Omega
        R.width = 2 * Omega
    else:
        R.status = "closed"
        R.lL, R.lU, R.width = lLow, lUp, lUp - lLow
        if lLow > lA + TOL:
            R.add("(ii) L <= A")
        if lUp < lA - TOL:
            R.add("(ii) A <= U")
        if R.width > C.x_out + TOL:
            R.add("width: U <= e^{x_out} L")
    if math.log(R.queries) > C.lcost_good() + 1e-12:
        R.add("(vi) queries <= 1 + M_bar + sum min{M_bar, (J+1) cnt}")
    if math.log(R.queries) > C.lCmax() + 1e-12:
        R.add("cost <= C_max")
    R.info = dict(lell_init=lell_init, lell=lell, n_left=len(left), n_neg=sum(1 for t in left if t[1] == "neg"))
    if stopped:              # how the run closed: with an empty tail (r = -1), or through the tail lemma at radius r, at a populated pass or not
        R.info.update(r_close=r_close, pop_close=bool(pop_close), harper_binding=bool(lell > lell_init + TOL), tail_ratio=tail_ratio)
    R.info["harper_ratio"] = harper_ratio if harper_ratio != math.inf else None
    return R


LOCAL_V2 = "local: (V2) holds at the pass, yet p(s_j) > q"
LOCAL_V3 = "local: (V3) holds at the pass, yet p(s_j e^-b) < p_low"
DETERMINISTIC = (LOCAL_V2, LOCAL_V3, "(2.1) X_{s_j} <= N <= X_{s_j e^-b}", "(iii) q_j > pi_dagger", "(iv) M_j^neg <= (1+eta) e^lam nu0 M_dagger", "(iv) M <= M_bar",
                 "(iv) M <= max{K, 2 M_j^neg}", "(iv) a negligible level has M < M_dagger", "width: s_0 <= Pi L", "width: populated part",
                 "width: negligible part", "width: tail", "width: U <= e^{x_out} L")
