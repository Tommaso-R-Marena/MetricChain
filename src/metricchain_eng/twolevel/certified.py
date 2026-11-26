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
from dataclasses import dataclass, field

import numpy as np

from .alg2l import Params, constants
from .meanrun import lC_max
from .tables import LN2, CubeTables, cube_constants, theta_hint

_tables: dict = {}


def tables(d: int, u: float) -> CubeTables:
    if (d, u) not in _tables:
        _tables[(d, u)] = CubeTables(d, u)
    return _tables[(d, u)]


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
        self.cache: dict = {}
        self.calls = 0

    # -- one rung ------------------------------------------------------------------------------
    def best(self, d: int, x: float, lid: float, depth: int):
        key = (d, round(x, 10), round(lid, 8), depth)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        c0, kind0 = k0_lcost(d, self.u, x, lid)
        out = (c0, kind0)
        if depth > 0 and not (x / d >= 0.9 * self.cc.eps_star or d < 50):
            bestlb = self._best_level(d, x, lid, depth, cutoff=c0)
            if bestlb is not None and bestlb.lCmax < c0:
                out = (bestlb.lCmax, bestlb)
        self.cache[key] = out
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
