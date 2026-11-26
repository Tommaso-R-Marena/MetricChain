"""Adversarial search over instances for Algorithm 2L+ (THY-REQ-0001, Part B).

What is searched.  The outer loop of the algorithm sees an instance only through the law of
the fibre averages W(a), a in Q_{n_o}; that law is the law of exp(-g) for a u-Lipschitz g on
the outer cube, and (Harper) its level sets can be taken to be initial segments of the
simplicial order.  When the level sets are *balls* this is a radial profile

    W(a) = exp(c_in - F(d(a, centre))),      F(0) = 0,   0 <= F(r) - F(r-1) <= u,

and that is the family searched here ("monotone"); profiles with slopes in [-u, u]
("general") are searched too, as a control on the reduction.  Besides F the instance has two
scalars: the distance d0 of the reference point's outer part from the centre (psi_0 = F(d0))
and the inner offset c_in = ln A_in + F_i(reference) in [-n_i Lambda_1, n_i (u - Lambda_1)],
which fixes where W sits in the trivial bracket (t0 = u n_i + c_in).

Parametrisation: F has piecewise-constant slope on k + 1 segments; the k knots are free.  A
point x of [0, 1]^(2k + 3) is decoded as (knots, slopes, d0, c_in); the knot coordinate is
warped so that half of the range resolves the neighbourhoods of r_dagger, p_u n_o,
Lambda_1 n_o / u and n_o / 2 on the scale sqrt(n_o).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import differential_evolution

from .alg2l import Params
from .ckernel import Evaluator
from .meanrun import Instance, Run, radial_law
from .tables import cube_constants

OBJECTIVES = ("cost", "cost_minus_cap", "count", "Mneg", "sample", "vi", "cost_any_placement")


def _stretch(x: float) -> float:
    """[0,1] -> [0,1] with flat ends, so that the extreme values are reached on sets of positive measure."""
    return min(1.0, max(0.0, 1.2 * x - 0.1))


@dataclass
class Family:
    """The decoder from [0,1]^D to instances, for fixed algorithm parameters."""

    ev: Evaluator
    k: int = 8
    monotone: bool = True
    anchors: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        P, C = self.ev.P, self.ev.C
        c = cube_constants(P.u)
        n_o = P.n_o
        s = 4.0 * math.sqrt(n_o)
        raw = [0.0, C.r_dag - s, C.r_dag, C.r_dag + s, c.p_u * n_o + s, c.Lambda1 * n_o / P.u - s,
               c.Lambda1 * n_o / P.u + s, n_o / 2 - s, n_o / 2 + s, float(n_o)]
        a = np.clip(np.array(raw), 0.0, n_o)
        a = np.maximum.accumulate(a)
        keep = np.concatenate([[True], np.diff(a) > 0.5])
        self.anchors = a[keep]
        if self.anchors[-1] < n_o:
            self.anchors = np.append(self.anchors, float(n_o))

    @property
    def dim(self) -> int:
        return 2 * self.k + 3

    def warp(self, z: np.ndarray) -> np.ndarray:
        """Knot coordinate in [0,1] -> radius in [0, n_o]."""
        grid = np.linspace(0.0, 1.0, len(self.anchors))
        return np.interp(z, grid, self.anchors)

    def unwarp(self, r: float) -> float:
        grid = np.linspace(0.0, 1.0, len(self.anchors))
        return float(np.interp(r, self.anchors, grid))

    def profile(self, knots_r: np.ndarray, slopes: np.ndarray) -> np.ndarray:
        """F on 0..n_o with slope slopes[i] between consecutive knots (radii, ascending)."""
        n_o = self.ev.P.n_o
        edges = np.concatenate([[0.0], np.clip(np.sort(knots_r), 0.0, n_o), [float(n_o)]])
        d = np.arange(n_o + 1, dtype=float)
        # F(r) = integral_0^r of the slope function
        cum = np.concatenate([[0.0], np.cumsum(np.diff(edges) * slopes)])
        return np.interp(d, edges, cum)

    def decode(self, x: np.ndarray) -> tuple[np.ndarray, int, float]:
        P = self.ev.P
        k = self.k
        c = cube_constants(P.u)
        knots = self.warp(np.sort(np.asarray(x[:k])))
        st = np.array([_stretch(v) for v in x[k:2 * k + 1]])
        slopes = P.u * st if self.monotone else P.u * (2.0 * st - 1.0)
        F = self.profile(knots, slopes)
        d0 = int(round(_stretch(x[2 * k + 1]) * P.n_o))
        lo, hi = -P.n_i * c.Lambda1, P.n_i * (P.u - c.Lambda1)
        c_in = lo + _stretch(x[2 * k + 2]) * (hi - lo)
        return F, d0, c_in

    def instance(self, F: np.ndarray, d0: int, c_in: float) -> Instance:
        P = self.ev.P
        # psi(a, b) = F(d(a)) + F_i(b);  psi_0 = F(d0) + F_i(ref);  W(a) = exp(-F(d(a))) A_in.  Shift psi so that
        # F_i(ref) = 0:  ln W = -F + c_in  with  c_in = ln A_in + F_i(ref),  t0 = u n_i + c_in.
        return Instance(radial_law(F, self.ev.outer, shift=c_in), psi0=float(F[d0]), t0=P.u * P.n_i + c_in)

    def encode_two_slope(self, R: float, s_in: float, s_out: float, d0_frac: float = 0.5, c_in_frac: float | None = None) -> np.ndarray:
        """x for the profile with slope s_in*u below radius R and s_out*u above (both in [0,1] for the
        monotone family; in [-1,1] for the general one)."""
        P = self.ev.P
        c = cube_constants(P.u)
        k = self.k
        z = self.unwarp(R)
        x = np.empty(self.dim)
        x[:k] = z
        def enc(v):      # inverse of the slope map
            st = v if self.monotone else (v + 1.0) / 2.0
            return (st + 0.1) / 1.2
        x[k] = enc(s_in)
        x[k + 1:2 * k + 1] = enc(s_out)
        x[2 * k + 1] = (d0_frac + 0.1) / 1.2
        if c_in_frac is None:                       # flat fibre: c_in = 0
            lo, hi = -P.n_i * c.Lambda1, P.n_i * (P.u - c.Lambda1)
            c_in_frac = (0.0 - lo) / (hi - lo) if hi > lo else 0.5
        x[2 * k + 2] = (c_in_frac + 0.1) / 1.2
        return np.clip(x, 0.0, 1.0)


@dataclass
class SearchResult:
    objective: str
    oracle: str
    best_value: float = -math.inf
    best_x: np.ndarray | None = None
    best_run: Run | None = None
    n_eval: int = 0
    # extremes of every claim over ALL evaluated instances (the claims under optimisation pressure)
    extremes: dict = field(default_factory=dict)
    violations: list = field(default_factory=list)


_SLACKS = ("slack_valid_lower", "slack_valid_upper", "slack_width", "slack_iv_M", "slack_iv_Mneg", "slack_iv_Mbar",
           "slack_v", "slack_vi")


def objective_value(R: Run, objective: str) -> float:
    if objective in ("cost", "cost_any_placement"):
        return R.lcost
    if objective == "cost_minus_cap":
        return R.lcost - R.lCmax
    if objective == "count":
        return R.slack_v
    if objective == "Mneg":
        return R.slack_iv_Mneg
    if objective == "sample":
        return R.slack_iv_Mbar
    if objective == "vi":
        return R.slack_vi
    raise ValueError(objective)


class Search:
    """Maximise an objective of the mean run over the instance family, recording every claim on the way."""

    def __init__(self, fam: Family, oracle: str, objective: str = "cost", positions: tuple | None = None,
                 fixed_c_in: float | None = None):
        self.fam, self.oracle, self.objective = fam, oracle, objective
        # ``positions``: fixed rung brackets (alpha, beta) instead of an oracle (meanrun.rung_positions);
        # ``fixed_c_in``: the inner offset is not searched (0.0 = flat fibres).  Both are used by the three-level runs.
        self.positions, self.fixed_c_in = positions, fixed_c_in
        # "cost_any_placement": the upper bound on the evaluations of every instance with the same law of fibre
        # averages, whatever the places of its fibres in their trivial brackets (meanrun.rung_positions); the
        # run so evaluated is not the run of one instance, and its claims are not those of the theorem
        P = fam.ev.P
        c = cube_constants(P.u)
        self.t0_range = (P.n_i * (P.u - c.Lambda1), P.n_i * (2 * P.u - c.Lambda1)) if objective == "cost_any_placement" else None
        self.res = SearchResult(objective, oracle)
        self.res.extremes = {k: -math.inf for k in _SLACKS}
        self.res.extremes.update(margin_iii=math.inf, cost_over_cap=-math.inf, lcost=-math.inf, lM_max=-math.inf, not_closed=0)

    def evaluate(self, x: np.ndarray) -> float:
        F, d0, c_in = self.fam.decode(x)
        if self.fixed_c_in is not None:
            c_in = self.fixed_c_in
        R = self.fam.ev.run(self.fam.instance(F, d0, c_in), self.oracle, t0_range=self.t0_range, positions=self.positions)
        res = self.res
        res.n_eval += 1
        ex = res.extremes
        for k in _SLACKS:
            v = getattr(R, k)
            if v > ex[k]:
                ex[k] = v
        ex["margin_iii"] = min(ex["margin_iii"], R.margin_iii)
        ex["cost_over_cap"] = max(ex["cost_over_cap"], R.lcost - R.lCmax)
        ex["lcost"] = max(ex["lcost"], R.lcost)
        ex["lM_max"] = max(ex["lM_max"], R.lM_max)
        if not R.closed:
            ex["not_closed"] += 1
        viol = R.violations()
        if viol and len(res.violations) < 20:
            res.violations.append(dict(x=np.asarray(x).tolist(), violations=viol))
        val = objective_value(R, self.objective)
        if not math.isfinite(val):
            val = -1e300
        if val > res.best_value:
            res.best_value, res.best_x, res.best_run = val, np.array(x, dtype=float), R
        return val

    def seeds(self) -> list[np.ndarray]:
        """Structured starting points: flat, cones, plateau-then-cone and cone-then-flat ("dip") at the radii that
        matter, with the reference point at the centre, at the median and at the far side."""
        fam = self.fam
        P, C = fam.ev.P, fam.ev.C
        c = cube_constants(P.u)
        n_o = P.n_o
        s = math.sqrt(n_o)
        radii = sorted(set(float(min(max(r, 0.0), n_o)) for r in
                           [C.r_dag + 1, C.r_dag + s, c.p_u * n_o, c.p_u * n_o + s, 0.9 * c.Lambda1 * n_o / P.u,
                            c.Lambda1 * n_o / P.u, 1.1 * c.Lambda1 * n_o / P.u, 1.3 * c.Lambda1 * n_o / P.u, n_o / 2]))
        out = []
        for d0f in (0.5, 0.0, 1.0):
            out.append(fam.encode_two_slope(n_o / 2, 0.0, 0.0, d0f))            # flat
            out.append(fam.encode_two_slope(n_o / 2, 1.0, 1.0, d0f))            # cone
            out.append(fam.encode_two_slope(n_o / 2, 0.5, 0.5, d0f))            # cone of slope u/2
            for R in radii:
                out.append(fam.encode_two_slope(R, 0.0, 1.0, d0f))              # plateau below R, cone above
                out.append(fam.encode_two_slope(R, 1.0, 0.0, d0f))              # cone below R, flat above ("dip")
        return out

    def run(self, budget: int, seed: int, popsize: int = 12) -> SearchResult:
        fam = self.fam
        rng = np.random.default_rng(seed)
        seeds = self.seeds()
        for x in seeds:
            self.evaluate(x)
        if budget <= len(seeds):
            return self.res
        D = fam.dim
        npop = max(popsize * D, len(seeds) + 8)
        init = rng.random((npop, D))
        init[:len(seeds)] = np.array(seeds)
        # jittered copies of the structured points
        for i in range(len(seeds), min(npop, 2 * len(seeds))):
            init[i] = np.clip(np.array(seeds[i - len(seeds)]) + rng.normal(0.0, 0.03, size=D), 0.0, 1.0)
        maxiter = max(1, (budget - len(seeds)) // npop - 1)
        differential_evolution(lambda x: -self.evaluate(x), bounds=[(0.0, 1.0)] * D, init=init, maxiter=maxiter,
                               popsize=popsize, tol=0.0, atol=0.0, mutation=(0.4, 1.0), recombination=0.8,
                               seed=int(rng.integers(0, 2 ** 31 - 1)), polish=False, updating="immediate")
        return self.res


def describe_profile(F: np.ndarray, u: float, n_seg_max: int = 12) -> list[tuple[int, int, float]]:
    """Run-length description of a profile: (first radius, last radius, slope/u) per segment of constant slope."""
    dF = np.round(np.diff(F) / u, 6)
    out = []
    start = 0
    for r in range(1, len(dF) + 1):
        if r == len(dF) or dF[r] != dF[start]:
            out.append((start, r, float(dF[start])))
            start = r
    return out[:n_seg_max] if len(out) > n_seg_max else out
