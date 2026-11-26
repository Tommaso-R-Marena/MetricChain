"""Certified cost bounds of nested runs of Algorithm 2L+ (theory report §11.19, Theorem 11.56 and remark (1b)).

The cost bound of one level,

    C_max = 1 + 2 M_bar + sum_{l=1}^{L} min{ 2 M_bar, (J + 1) cnt(x_{l-1}) } C_l ,

depends on the level's own design and on the cost bounds ``C_l`` of whatever serves its rungs — not on the instance,
and not on where the servers' brackets fall.  It holds in every run on every instance (the algorithm aborts with the
trivial bracket before a query would exceed it).  A run of Algorithm 2L+ in the fibre dimension, designed for a
certified accuracy at most the rung's and for the failure probability the level above hands down, is therefore an
admissible server with ``C_l`` its own ``C_max``; and ``C_max`` is nondecreasing in every ``C_l``.  So the rule

    every rung is served by the candidate with the smallest certified cost

gives, by induction on the depth, a certified bound for any number of nested levels that is nonincreasing in the
depth and in the set of candidate designs (THY-RES-0013 §4; the rule is the theory division's, reviewed by the
science division in SCI-REV-0016).  This module evaluates that recursion: no instance, no evaluator run, only the
constants of Theorem 11.56 (``alg2l.constants``) and the cost of the base bracket of Proposition K0.

Everything is a natural logarithm.  Written from the theorem's formulas in ``alg2l.py`` and from the description of
the rule in THY-RES-0013 §4; the candidate designs "referee" and "bounded" are those of the theory branch's
``experiments/coordinator_checks/three_levels_certified/cert3.py`` (read as text, not run, not imported), so that the
published table can be reproduced; "wide" is this module's own, larger family.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

import numpy as np

from .alg2l import Params, constants
from .meanrun import lC_max
from .tables import LN2, CubeTables, cube_constants, theta_hint

_tables: dict = {}          # (d, u) -> CubeTables, least recently used first; bounded by the total of the dimensions
_tables_total = 0
TABLES_BUDGET = 4_000_000   # sum of d over the cached tables (each table holds about ten arrays of d + 1 doubles: 320 MB)


def tables(d: int, u: float) -> CubeTables:
    """Tables of the d-cube, cached with a bound on memory (a deep search visits thousands of dimensions)."""
    global _tables_total
    key = (d, u)
    t = _tables.pop(key, None)
    if t is None:
        t = CubeTables(d, u)
        _tables_total += d
        while _tables_total > TABLES_BUDGET and _tables:
            old_key = next(iter(_tables))
            _tables.pop(old_key)
            _k0cache.pop(old_key, None)
            _tables_total -= old_key[0]
    _tables[key] = t
    return t


# ---------------------------------------------------------------------------------------------
# The base bracket (Proposition K0): its cost is fixed by its design and is its own bound
# ---------------------------------------------------------------------------------------------
def k0_lcost(d: int, u: float, x: float, l_inv_delta: float) -> tuple[float, str]:
    """(ln cost, kind) of the base bracket in dimension d at accuracy x and failure probability e^-l_inv_delta:
    two samples of the prescribed size, or enumeration of the 2^d points where that is cheaper or no radius qualifies."""
    t = tables(d, u)
    eta = min(0.5, math.tanh(x / 4))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) + l_inv_delta))
    budget = x - math.log((1 + eta) / (1 - eta))
    ok = np.logaddexp(0.0, t.lG2(eta)[:d]) <= budget
    if not ok[0]:
        return d * LN2, "enum"
    bad = np.flatnonzero(~ok)
    rstar = (int(bad[0]) - 1) if bad.size else d - 1
    lM = max(math.log(K) + d * LN2 - math.log(1 - eta) - float(t.lball[rstar]), math.log(K / (1 - eta)))
    lcost = LN2 + lM
    if lcost >= d * LN2:
        return d * LN2, "enum"
    return lcost, "K0"


_k0cache: dict = {}


def _k0_half(d: int, u: float):
    """For eta = 1/2 (every accuracy x >= 4 artanh(1/2) = 2.197): the running maximum of ln(1 + G2(r)), r = 0..d-1,
    so that the first radius that fails the budget is found by bisection."""
    key = (d, u)
    t = tables(d, u)                    # touches the table (and may evict others together with their entries here)
    hit = _k0cache.get(key)
    if hit is None:
        hit = np.maximum.accumulate(np.logaddexp(0.0, t.lG2(0.5)[:d]))
        _k0cache[key] = hit
    return hit


def k0_lcost_vec(d: int, u: float, xs, l_inv_delta: float) -> np.ndarray:
    """``k0_lcost`` for an array of accuracies (the costs only)."""
    xs = np.asarray(xs, dtype=float)
    out = np.empty(xs.size)
    half = xs / 4 >= math.atanh(0.5)
    if half.any():
        t = tables(d, u)
        gmax = _k0_half(d, u)
        eta = 0.5
        K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) + l_inv_delta))
        budget = xs[half] - math.log((1 + eta) / (1 - eta))
        first_bad = np.searchsorted(gmax, budget, side="right")          # first r with ln(1 + G2(r)) > budget
        rstar = np.minimum(first_bad, d) - 1
        lball = np.where(rstar >= 0, t.lball[np.maximum(rstar, 0)], 0.0)
        lM = np.maximum(math.log(K) + d * LN2 - math.log(1 - eta) - lball, math.log(K / (1 - eta)))
        lcost = LN2 + lM
        out[half] = np.where((rstar < 0) | (lcost >= d * LN2), d * LN2, lcost)
    for i in np.flatnonzero(~half):
        out[i] = k0_lcost(d, u, float(xs[i]), l_inv_delta)[0]
    return out


# ---------------------------------------------------------------------------------------------
# One level
# ---------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Design:
    """The design of one level of Algorithm 2L+ in dimension d (everything but the servers of its rungs)."""

    phi: float              # outer fraction: n_o = clip(floor(phi d), 1, d - 1)
    lam: float
    eta: float
    etap: float
    b: float                # tolerance
    Lr: int                 # rungs of the geometric ladder x_l = x_0 (b/x_0)^{l/Lr}
    theta: float | None = None
    ltheta: float | None = None
    bounded: bool = True    # nu_1 = 2 e^u n_o / theta (the bounded-accuracy choice) or nu_1 = 1
    name: str = ""

    def lth(self) -> float:
        return math.log(self.theta) if self.ltheta is None else self.ltheta


def split(d: int, phi: float) -> tuple[int, int]:
    n_o = min(max(int(math.floor(phi * d)), 1), d - 1)
    return n_o, d - n_o


def level_params(u: float, d: int, D: Design, l_inv_delta: float) -> Params | None:
    """The parameters of the level, or None if the ladder does not exist (x_0 = 2 u n_i must exceed b)."""
    n_o, n_i = split(d, D.phi)
    x0 = 2 * u * n_i
    if not (D.b > 0 and x0 > D.b):
        return None
    xs = [x0 * (D.b / x0) ** (l / D.Lr) for l in range(D.Lr + 1)]
    xs[-1] = D.b
    lth = D.lth()
    nu1 = max(1.0, math.exp(math.log(2 * n_o) + u - lth)) if D.bounded else 1.0
    return Params(n=d, n_o=n_o, u=u, lam=D.lam, eta=D.eta, etap=D.etap, theta=math.inf, nu1=nu1, b=D.b, delta=1.0, xs=tuple(xs),
                  ltheta=lth, ldelta=-l_inv_delta)


@dataclass
class LevelBound:
    lCmax: float
    xout: float
    design: Design
    n_o: int
    n_i: int
    lM_bar: float
    l_inv_delta_p: float
    xs: tuple
    lC: np.ndarray                                   # ln C_l, l = 0..L (index 0 unused)
    servers: list = field(default_factory=list)      # per rung l = 1..L: the server's description (kind or LevelBound)
    lterm: np.ndarray | None = None                  # ln of the l-th term of C_max, l = 1..L

    def depth(self) -> int:
        """Number of nested levels of Algorithm 2L+ in this procedure, itself included."""
        return 1 + max([s.depth() for s in self.servers if isinstance(s, LevelBound)], default=0)


def level_bound(u: float, d: int, D: Design, l_inv_delta: float, server, cutoff: float = math.inf) -> LevelBound | None:
    """C_max of one level in dimension d.  ``server(d_i, x, l_inv_delta')`` returns ``(ln C, description)`` for a rung.
    Returns None if the design is infeasible, or as soon as the bound is known to be at least ``cutoff`` (the outer
    sample alone, 2 M_bar, is below C_max)."""
    P = level_params(u, d, D, l_inv_delta)
    if P is None:
        return None
    C = constants(P, tables(P.n_o, u))
    if LN2 + C.lM_bar >= cutoff:
        return None
    lC = np.full(P.L + 1, -np.inf)
    servers = []
    for l in range(1, P.L + 1):
        c, desc = server(P.n_i, P.xs[l], C.l_inv_delta_p)
        lC[l] = c
        servers.append(desc)
    lmult = np.array([min(LN2 + C.lM_bar, math.log(C.J + 1) + C.lcnt(P.xs[l - 1], P)) for l in range(1, P.L + 1)])
    lterm = lmult + lC[1:]
    lCmax = lC_max(P, C, lC)
    return LevelBound(lCmax=lCmax, xout=C.x_out, design=D, n_o=P.n_o, n_i=P.n_i, lM_bar=C.lM_bar,
                      l_inv_delta_p=C.l_inv_delta_p, xs=P.xs, lC=lC, servers=servers, lterm=lterm)


# ---------------------------------------------------------------------------------------------
# Candidate designs of a level that must reach a certified accuracy x in dimension d
# ---------------------------------------------------------------------------------------------
def acc_const(c: float) -> float:
    """What a level adds to its tolerance at lam = eta = eta' = theta = c: ln(e^lam (1 + eta)/(1 - eta) + eta' + theta)."""
    return math.log(math.exp(c) * (1 + c) / (1 - c) + 2 * c)


def extensive_design(u: float, d: int, x: float, phi: float, Lr: int = 30, bfrac: float = 0.25) -> Design:
    """The referee's design for large accuracies: lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, b = x/4 and the largest
    theta the accuracy allows, theta = e^{x-b} - (3e + 1) - (2 p_u)^d e^{-b}."""
    bm = bfrac * x
    lth = (x - bm) + math.log1p(-(3 * math.e + 1 + (2 / (1 + math.exp(u))) ** d * math.exp(-bm)) * math.exp(-(x - bm)))
    return Design(phi=phi, lam=1.0, eta=0.5, etap=1.0, b=bm, Lr=Lr, ltheta=lth, bounded=False,
                  name=f"extensive(b={bfrac:g}x,phi={phi:.3f})")


def bounded_design(x: float, phi: float, b: float, Lr: int = 30, c: float | None = None, tag: str = "") -> Design:
    c = min(x / 12, 1 / 3) if c is None else c
    return Design(phi=phi, lam=c, eta=c, etap=c, b=b, Lr=Lr, theta=c, bounded=True, name=f"bounded(c={c:.3f},b={tag or f'{b:.3g}'},phi={phi:.3f})")


def referee_candidates(u: float, d: int, x: float):
    """The middle designs of the theory branch's referee (r8_flat3.py): one list of designs to try in full."""
    g = x / d
    out = []
    if x >= 8:
        p0 = min(0.7, max(0.05, g / (g + theta_hint(u, g))))
        for p2 in (p0, min(0.8, 1.5 * p0)):
            if 2 * u * (d - int(p2 * d)) <= (x / 4) * 1.5:
                continue
            out.append(extensive_design(u, d, x, p2))
    else:
        out.append(bounded_design(x, 0.55, x / 2, tag="x/2"))
    return out


def bounded_chains(u: float, d: int, x: float, phis=(0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20)):
    """The theory division's added candidates: the bounded-accuracy design at every accuracy, tolerance x/2 or the
    largest the accuracy allows; per tolerance a *chain* of outer fractions to descend while the bound decreases."""
    c = min(x / 12, 1 / 3)
    bmax = x - acc_const(c) - 1e-6
    chains = []
    for bm, tag in ((x / 2, "x/2"), (bmax, "max")):
        if bm <= 0 or bm > bmax:
            continue
        chain = []
        for p2 in phis:
            if 2 * u * (d - int(p2 * d)) <= bm * 1.5:
                break
            chain.append(bounded_design(x, p2, bm, tag=tag))
        if chain:
            chains.append(chain)
    return chains


# ---------------------------------------------------------------------------------------------
# The recursion
# ---------------------------------------------------------------------------------------------
class Recursion:
    """Servers chosen by certified cost, to a given depth.

    ``family``:
      "referee"  the referee's middle designs only (THY-RES-0013 §4, column "servers by certified cost");
      "searched" those and the bounded design at every accuracy, as in cert3.py (column "more middle designs");
      "wide"     this module's family (``wide_candidates``).
    ``best(d, x, l_inv_delta, depth)`` returns ``(ln C, description)`` of the cheapest certified procedure with at
    most ``depth`` nested levels of Algorithm 2L+ above base brackets (depth 0: the base bracket alone).
    """

    def __init__(self, u: float, family: str = "searched", prefilter: bool = True):
        if family not in ("referee", "searched", "wide"):
            raise ValueError(family)
        self.u = u
        self.family = family
        self.prefilter = prefilter
        self.cc = cube_constants(u)
        self.calls = 0

    # -- one rung ------------------------------------------------------------------------------
    def best(self, d: int, x: float, lid: float, depth: int):
        c0, kind0 = k0_lcost(d, self.u, x, lid)
        out = (c0, kind0)
        if depth > 0 and not (x / d >= 0.9 * self.cc.eps_star or d < 50):
            bestlb = self._best_level(d, x, lid, depth, cutoff=c0)
            if bestlb is not None and bestlb.lCmax < c0:
                out = (bestlb.lCmax, bestlb)
        return out

    def _server(self, depth: int):
        return lambda d_i, x, lidp: self.best(d_i, x, lidp, depth)

    def _try(self, d: int, x: float, lid: float, depth: int, D: Design, cutoff: float):
        self.calls += 1
        lb = level_bound(self.u, d, D, lid, self._server(depth - 1), cutoff=cutoff)
        if lb is None or lb.xout > x + 1e-9:
            return None
        return lb

    def _best_level(self, d: int, x: float, lid: float, depth: int, cutoff: float):
        """The level design with the smallest certified bound among the family's candidates (None if none exists or
        none can be below ``cutoff``; candidates that cannot beat ``cutoff`` by their outer sample alone are skipped
        without evaluating their rungs, which changes nothing in the minimum reported below the cutoff)."""
        best = None

        def consider(lb):
            nonlocal best
            if lb is not None and (best is None or lb.lCmax < best.lCmax):
                best = lb

        if self.family in ("referee", "searched"):
            # cert3.py evaluates the referee's candidates in full; the pruning by the outer sample is exact for the
            # question "is the minimum below the base bracket's cost, and what is it then"
            for D in referee_candidates(self.u, d, x):
                consider(self._try(d, x, lid, depth, D, math.inf))
            if self.family == "searched" and (not self.prefilter or cutoff > 0.2 * d * self.cc.a):
                for chain in bounded_chains(self.u, d, x):
                    prev = None
                    for D in chain:
                        lb = level_bound(self.u, d, D, lid, self._server(depth - 1))
                        self.calls += 1
                        if lb is None or lb.xout > x + 1e-9:
                            break
                        if prev is not None and lb.lCmax >= prev:
                            break
                        consider(lb)
                        prev = lb.lCmax
        else:
            for D in wide_candidates(self.u, d, x):
                bound = cutoff if best is None else min(cutoff, best.lCmax)
                consider(self._try(d, x, lid, depth, D, bound))
        return best

    # -- the top level ---------------------------------------------------------------------------
    def top(self, n: int, D: Design, l_inv_delta: float, depth: int) -> LevelBound | None:
        """The certified bound of ``depth`` nested levels: the top level has design ``D``, its rungs are served by the
        cheapest certified procedures with at most ``depth - 1`` levels."""
        if depth < 1:
            raise ValueError("at least one level")
        return level_bound(self.u, n, D, l_inv_delta, self._server(depth - 1))


WIDE_PHIS = (0.70, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10)


def wide_candidates(u: float, d: int, x: float):
    """A larger family: both kinds of design at every accuracy, a finer grid of outer fractions, three tolerances for
    the bounded kind and three for the extensive kind."""
    out = []
    c = min(x / 12, 1 / 3)
    bmax = x - acc_const(c) - 1e-6
    for bm, tag in ((x / 2, "x/2"), (bmax, "max"), (0.75 * bmax, "0.75max")):
        if bm <= 0 or bm > bmax:
            continue
        for p2 in WIDE_PHIS:
            if 2 * u * (d - int(p2 * d)) <= bm * 1.5:
                continue
            out.append(bounded_design(x, p2, bm, tag=tag))
    if x >= 8:
        for bfrac in (0.25, 0.5, 0.125):
            for p2 in WIDE_PHIS:
                if 2 * u * (d - int(p2 * d)) <= (bfrac * x) * 1.5:
                    continue
                out.append(extensive_design(u, d, x, p2, bfrac=bfrac))
    return out


def top_design(phi: float, b: float = 0.5, lam: float = 0.2, eta: float = 0.05, etap: float = 0.05, theta: float = 0.05,
               Lr: int = 40) -> Design:
    """The outer design of ENG-RES-0014 §2 and of the theory report's remark (1b): certified accuracy 0.8715."""
    return Design(phi=phi, lam=lam, eta=eta, etap=etap, b=b, Lr=Lr, theta=theta, bounded=True, name=f"top(phi={phi:.3f})")


def describe(lb: LevelBound, na: float, indent: int = 0, max_depth: int = 2) -> list[str]:
    """Human-readable summary of which procedure serves which rung."""
    pad = "  " * indent
    lines = [f"{pad}{lb.design.name}: n_o={lb.n_o}, n_i={lb.n_i}, ln C_max/(n a) = {lb.lCmax / na:.4f}, accuracy {lb.xout:.4g}, "
             f"outer sample {(LN2 + lb.lM_bar) / na:.4f}"]
    if indent >= max_depth:
        return lines
    kinds = ["2L+" if isinstance(s, LevelBound) else str(s) for s in lb.servers]
    lines.append(f"{pad}  rungs by server: " + ", ".join(f"{k}:{kinds.count(k)}" for k in sorted(set(kinds))))
    top = int(np.argmax(lb.lterm))
    s = lb.servers[top]
    lines.append(f"{pad}  largest term: rung {top + 1} (accuracy {lb.xs[top + 1]:.4g}), {lb.lterm[top] / na:.4f}, served by "
                 f"{'2L+' if isinstance(s, LevelBound) else s} at {lb.lC[top + 1] / na:.4f}")
    if isinstance(s, LevelBound):
        lines += describe(s, na, indent + 2, max_depth)
    return lines


# ---------------------------------------------------------------------------------------------
# The same recursion as an exact search with pruning (any depth, any candidate family)
# ---------------------------------------------------------------------------------------------
def theory_candidates(u: float, d: int, x: float):
    """Every design ``cert3.py`` can try for a rung, as one flat list: the referee's and the bounded design with
    tolerance x/2 or maximal at the outer fractions 0.50, 0.45, ..., 0.20.  (``cert3.py`` walks the fractions
    downwards and stops at the first that does not improve; the minimum over the whole list can only be lower.)"""
    out = list(referee_candidates(u, d, x))
    for chain in bounded_chains(u, d, x):
        out += chain
    return out


FAMILIES = {"theory": theory_candidates, "wide": wide_candidates}


class Search:
    """min over a candidate family of the certified cost of at most ``depth`` nested levels above base brackets.

    The search is exact for the family: a candidate is discarded only when a lower bound of its cost — its outer
    sample ``2 M_bar``, or the terms of ``C_max`` accumulated so far over rungs whose servers are already known —
    is at least the best value found so far (or the cutoff the caller passes).  Candidates are tried in the order
    of their value with base brackets as servers, which is an upper bound of their value at any depth.
    """

    def __init__(self, u: float, family: str = "wide", coarse_rule: bool = True):
        self.u = u
        self.cands = FAMILIES[family]
        self.family = family
        self.cc = cube_constants(u)
        self.coarse_rule = coarse_rule      # the referee's rule: no nested run where x/d >= 0.9 eps* or d < 50
        self.nodes = 0
        self.levels = 0
        self.deadline: float | None = None  # time.time() after which ``best`` raises TimeoutError (the caller keeps what is finished)

    def _prepare(self, d: int, D: Design, lid: float):
        P = level_params(self.u, d, D, lid)
        if P is None:
            return None
        C = constants(P, tables(P.n_o, self.u))
        return P, C

    def _mult(self, P: Params, C) -> np.ndarray:
        return np.array([min(LN2 + C.lM_bar, math.log(C.J + 1) + C.lcnt(P.xs[l - 1], P)) for l in range(1, P.L + 1)])

    def best(self, d: int, x: float, lid: float, depth: int, cutoff: float = math.inf):
        """(ln C, description).  Exact whenever the value is below ``cutoff``; otherwise the base bracket's cost or
        some value >= cutoff is returned and only ">= cutoff" may be used."""
        self.nodes += 1
        if self.deadline is not None and (self.nodes & 255) == 0 and time.time() > self.deadline:
            raise TimeoutError("search deadline reached")
        c0, kind0 = k0_lcost(d, self.u, x, lid)
        if depth == 0 or (self.coarse_rule and (x / d >= 0.9 * self.cc.eps_star or d < 50)):
            return c0, kind0
        inc, desc = c0, kind0
        ranked = []
        bound = min(inc, cutoff)
        for D in self.cands(self.u, d, x):
            pc = self._prepare(d, D, lid)
            if pc is None:
                continue
            P, C = pc
            if C.x_out > x + 1e-9 or LN2 + C.lM_bar >= bound:
                continue
            lC0 = k0_lcost_vec(P.n_i, self.u, P.xs[1:], C.l_inv_delta_p)
            mult = self._mult(P, C)
            base = float(np.logaddexp(0.0, LN2 + C.lM_bar))
            shallow = float(np.logaddexp(base, np.logaddexp.reduce(mult + lC0)))
            ranked.append((shallow, len(ranked), D, P, C, lC0, mult, base))
        ranked.sort(key=lambda t: t[:2])
        for shallow, _, D, P, C, lC0, mult, base in ranked:
            bound = min(inc, cutoff)
            if base >= bound:
                continue
            self.levels += 1
            if depth == 1:
                val, lC, servers = shallow, lC0, None
            else:
                res = self._deep(P, C, lC0, mult, base, depth, bound)
                if res is None:
                    continue
                val, lC, servers = res
            if val < inc:
                inc = val
                desc = LevelBound(lCmax=val, xout=C.x_out, design=D, n_o=P.n_o, n_i=P.n_i, lM_bar=C.lM_bar,
                                  l_inv_delta_p=C.l_inv_delta_p, xs=P.xs, lC=np.concatenate([[-np.inf], lC]),
                                  servers=servers if servers is not None else ["K0/enum"] * P.L, lterm=mult + lC)
        return inc, desc

    def _deep(self, P: Params, C, lC0: np.ndarray, mult: np.ndarray, base: float, depth: int, bound: float):
        """C_max of the level with rungs served by the best procedures of depth - 1, or None if it is >= bound."""
        order = np.argsort(-(mult + lC0), kind="stable")
        lC = lC0.copy()
        servers = [None] * P.L
        acc = base
        for l in order:
            if acc >= bound:
                return None
            rem = bound + math.log(-math.expm1(acc - bound)) if math.isfinite(bound) else math.inf
            c, s = self.best(P.n_i, P.xs[l + 1], C.l_inv_delta_p, depth - 1, cutoff=rem - mult[l])
            acc = float(np.logaddexp(acc, mult[l] + c))
            lC[l] = c
            servers[l] = s
        if acc >= bound:
            return None
        return acc, lC, servers

    def top(self, n: int, D: Design, lid: float, depth: int, cutoff: float = math.inf) -> LevelBound | None:
        """The certified bound of ``depth`` nested levels with top design ``D`` (None if it is >= cutoff or the design
        is infeasible)."""
        pc = self._prepare(n, D, lid)
        if pc is None:
            return None
        P, C = pc
        lC0 = k0_lcost_vec(P.n_i, self.u, P.xs[1:], C.l_inv_delta_p)
        mult = self._mult(P, C)
        base = float(np.logaddexp(0.0, LN2 + C.lM_bar))
        if base >= cutoff:
            return None
        if depth == 1:
            val, lC, servers = float(np.logaddexp(base, np.logaddexp.reduce(mult + lC0))), lC0, None
            if val >= cutoff:
                return None
        else:
            res = self._deep(P, C, lC0, mult, base, depth, cutoff)
            if res is None:
                return None
            val, lC, servers = res
        return LevelBound(lCmax=val, xout=C.x_out, design=D, n_o=P.n_o, n_i=P.n_i, lM_bar=C.lM_bar,
                          l_inv_delta_p=C.l_inv_delta_p, xs=P.xs, lC=np.concatenate([[-np.inf], lC]),
                          servers=servers if servers is not None else ["K0/enum"] * P.L, lterm=mult + lC)
