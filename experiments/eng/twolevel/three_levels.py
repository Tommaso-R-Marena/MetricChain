"""X-010: three nested levels of Algorithm 2L+ with the engineering evaluator.

Step 1 (this file): the flat instance psi = 0, to be held against the referee's exact three-level numbers
(theory branch, ``experiments/reviews/R8/r8_flat3.py`` and ``out/flat3_a.txt``; design copied from its docstring,
code written here on top of ``metricchain_eng.twolevel``).  The outer algorithm is Algorithm 2L+ with a
geometric ladder of 40 rungs; each rung is served by the cheaper of

  * the base bracket of Proposition K0 in the inner dimension, and
  * Algorithm 2L+ itself in the inner dimension (the "middle" level, 30 rungs, base brackets inside), designed
    for the accuracy of the rung:
        x >= 8 :  lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, b = x/4, theta = e^{x-b} - (3e+1) - (2 p_u)^d e^{-b},
                  outer fraction phi_2 = g/(g + theta_hint(g)), g = x/d, clipped to [0.05, 0.7], and 1.5 times that;
        x <  8 :  lam = eta = eta' = theta = min(x/12, 1/3), b = x/2, nu_1 = 2 e^u n_o/theta, phi_2 = 0.55.

At the flat instance every run is deterministic: the bracket a procedure returns for a flat fibre, and its
cost, are numbers.  The outer run needs, per rung, the cost and *where the fibre average sits in the returned
bracket* (``meanrun.rung_positions``, ``positions``).

    python experiments/eng/twolevel/three_levels.py --check          # against the referee's published values
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel.alg2l import Params, constants, hinted_lower_bound  # noqa: E402
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, Law  # noqa: E402
from metricchain_eng.twolevel.tables import LN2, CubeTables, cube_constants, theta_hint  # noqa: E402

_tables: dict = {}


def tables(d: int, u: float) -> CubeTables:
    if (d, u) not in _tables:
        _tables[(d, u)] = CubeTables(d, u)
    return _tables[(d, u)]


def k0_flat(d: int, u: float, x: float, l_inv_delta: float) -> tuple[float, float, float, str]:
    """Proposition K0 in dimension d at accuracy x on a flat fibre: (ln cost, alpha, beta, kind) with the returned
    bracket [W e^-alpha, W e^beta].  Enumeration (exact, alpha = beta = 0) if no radius qualifies or if it is cheaper."""
    t = tables(d, u)
    eta = min(0.5, math.tanh(x / 4))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) + l_inv_delta))
    budget = x - math.log((1 + eta) / (1 - eta))
    ok = np.logaddexp(0.0, t.lG2(eta)[:d]) <= budget
    if not ok[0]:
        return d * LN2, 0.0, 0.0, "enum"
    bad = np.flatnonzero(~ok)
    rstar = (int(bad[0]) - 1) if bad.size else d - 1
    lM = max(math.log(K) + d * LN2 - math.log(1 - eta) - float(t.lball[rstar]), math.log(K / (1 - eta)))
    lcost = LN2 + lM
    if lcost >= d * LN2:
        return d * LN2, 0.0, 0.0, "enum"
    lq = math.log(K) - math.log(1 - eta) - lM
    if d * LN2 + lq < -1e-12:
        ltail = -math.inf
    else:
        ltail = float(t.lE[min(t.radius(lq), rstar)]) - d * LN2
    alpha = math.log(1 + eta)
    beta = float(np.logaddexp(-math.log(1 - eta), ltail))
    assert alpha + beta <= x + 1e-9
    return lcost, alpha, beta, "K0"


def k0_cone(d: int, u: float, x: float, l_inv_delta: float, slope: float) -> tuple[float, float, float, str]:
    """Proposition K0 on the cone psi(z) = slope u |z| of dimension d, at the level of expectations: the answer the
    two-sample bracket itself gives, not an assumed placement.  K0 draws two samples of size M; t_hat is the K-th
    largest weight of the first, A_hat the mean of min(w, t_hat) over the second, and it returns
    [A_hat/(1 + eta), A_hat/(1 - eta) + t_hat 2^-d E_rhat(d)].  With every count at its mean, t_hat is the weight
    e^{-slope u r_t} of the shell r_t that holds the quantile K/M, and A_hat = E min(w, t_hat).  Returns
    (ln cost, alpha, beta, kind) with the bracket [A e^-alpha, A e^beta]; ``slope = 0`` is ``k0_flat``."""
    if slope == 0.0:
        return k0_flat(d, u, x, l_inv_delta)
    t = tables(d, u)
    eta = min(0.5, math.tanh(x / 4))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) + l_inv_delta))
    budget = x - math.log((1 + eta) / (1 - eta))
    ok = np.logaddexp(0.0, t.lG2(eta)[:d]) <= budget
    if not ok[0]:
        return d * LN2, 0.0, 0.0, "enum"
    bad = np.flatnonzero(~ok)
    rstar = (int(bad[0]) - 1) if bad.size else d - 1
    lM = max(math.log(K) + d * LN2 - math.log(1 - eta) - float(t.lball[rstar]), math.log(K / (1 - eta)))
    lcost = LN2 + lM
    if lcost >= d * LN2:
        return d * LN2, 0.0, 0.0, "enum"
    r = np.arange(d + 1, dtype=float)
    lw = -slope * u * r
    lp = t.lbinom - d * LN2
    # the K-th largest of M weights: the shell r_t with P(|z| <= r_t) >= K/M > P(|z| <= r_t - 1)
    r_t = int(np.searchsorted(t.lball - d * LN2, math.log(K) - lM - 1e-12, side="left"))
    lt = -slope * u * min(r_t, d)
    lEmin = float(np.logaddexp.reduce(lp + np.minimum(lw, lt)))
    lA = float(np.logaddexp.reduce(lp + lw))
    lq = math.log(K) - math.log(1 - eta) - lM
    if d * LN2 + lq < -1e-12:
        ltail = -math.inf
    else:
        ltail = lt + float(t.lE[min(t.radius(lq), rstar)]) - d * LN2
    lL = lEmin - math.log(1 + eta)
    lU = float(np.logaddexp(lEmin - math.log(1 - eta), ltail))
    alpha, beta = lA - lL, lU - lA
    assert alpha >= -1e-12 and beta >= -1e-12 and alpha + beta <= x + 1e-9, (alpha, beta, x)
    return lcost, max(alpha, 0.0), max(beta, 0.0), "K0"


def flat_run(u: float, n: int, phi: float, *, lam: float = 0.2, eta: float = 0.05, etap: float = 0.05, theta: float = 0.05,
             ltheta: float | None = None, b: float = 0.5, Lr: int = 40, bounded: bool = True, l_inv_delta: float = math.log(20.0),
             inner=None) -> dict:
    """Algorithm 2L+ at psi = 0 in dimension n with outer fraction phi and a geometric ladder of Lr rungs; ``inner(d, x,
    l_inv_delta')`` returns (ln cost, alpha, beta, kind) of the procedure that serves a rung (default: ``k0_flat``)."""
    n_o = min(max(int(math.floor(phi * n)), 1), n - 1)
    n_i = n - n_o
    x0 = 2 * u * n_i
    xs = [x0 * (b / x0) ** (l / Lr) for l in range(Lr + 1)]
    xs[-1] = b
    lth = math.log(theta) if ltheta is None else ltheta
    nu1 = max(1.0, 2 * math.exp(u) * n_o / math.exp(lth)) if bounded else 1.0
    P = Params(n=n, n_o=n_o, u=u, lam=lam, eta=eta, etap=etap, theta=math.inf, nu1=nu1, b=b, delta=1.0, xs=tuple(xs),
               ltheta=lth, ldelta=-l_inv_delta)
    outer = tables(n_o, u)
    C = constants(P, outer)
    lC, alphas, betas, kinds = [-math.inf], [], [], ["triv"]
    for l in range(1, Lr + 1):
        c, a_, b_, kind = (k0_flat if inner is None else inner)(n_i, u, xs[l], C.l_inv_delta_p)
        lC.append(c)
        alphas.append(a_)
        betas.append(b_)
        kinds.append(kind)
    ev = Evaluator(P, outer, lC=np.array(lC))
    R = ev.run(Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=u * n_i), "bottom", positions=(alphas, betas))
    assert R.closed and not R.violations(), (R.status, R.violations())
    return dict(lcost=R.lcost, lL=R.lL, lU=R.lU, width=R.lU - R.lL, xout=C.x_out, lCmax=R.lCmax, kinds=kinds, xs=xs, n_o=n_o, n_i=n_i,
                K=C.K, r_dag=C.r_dag)


def make_inner(stats: list | None = None):
    """The rung server of the three-level run: the cheaper of K0 and a two-level run designed for the rung."""

    def inner(d: int, u: float, x: float, l_inv_delta: float):
        est = cube_constants(u).eps_star
        c0, a0, b0, k0 = k0_flat(d, u, x, l_inv_delta)
        best = (c0, a0, b0, k0)
        g = x / d
        if g >= 0.9 * est or d < 50:
            if stats is not None:
                stats.append((x, k0, c0, None))
            return best
        cands = []
        if x >= 8:
            bm = x / 4
            lth = (x - bm) + math.log1p(-(3 * math.e + 1 + (2 / (1 + math.exp(u))) ** d * math.exp(-bm)) * math.exp(-(x - bm)))
            p0 = min(0.7, max(0.05, g / (g + theta_hint(u, g))))
            for p2 in (p0, min(0.8, 1.5 * p0)):
                if 2 * u * (d - int(p2 * d)) <= bm * 1.5:
                    continue
                cands.append(flat_run(u, d, p2, lam=1.0, eta=0.5, etap=1.0, ltheta=lth, b=bm, Lr=30, bounded=False, l_inv_delta=l_inv_delta))
        else:
            c = min(x / 12, 1 / 3)
            cands.append(flat_run(u, d, 0.55, lam=c, eta=c, etap=c, theta=c, b=x / 2, Lr=30, bounded=True, l_inv_delta=l_inv_delta))
        cm = None
        for r in cands:
            assert r["xout"] <= x + 1e-9, (r["xout"], x)
            if cm is None or r["lcost"] < cm["lcost"]:
                cm = r
        if cm is not None and cm["lcost"] < best[0]:
            best = (cm["lcost"], -cm["lL"], cm["lU"], "2L+")          # the flat fibre has W = 1: bracket [e^lL, e^lU]
        if stats is not None:
            stats.append((x, best[3], c0, cm["lcost"] if cm is not None else None))
        return best

    return inner


# the referee's published values (theory branch at 9408e33, experiments/reviews/R8/out/flat3_a.txt), ln(cost)/(n a):
# (u, n, phi_1) -> (two levels, three levels, C_max of three levels, rungs served by the middle algorithm)
REFEREE = {(1.0, 1000, 0.30): (1.2054, 0.9842, 1.1309, 20), (1.0, 1000, 0.50): (0.9839, 0.8645, 1.1213, 18),
           (1.0, 1000, 0.70): (0.7510, 0.7323, 1.3781, 16), (1.0, 1000, 0.80): (0.7123, 0.7123, 1.4948, 6),
           (1.0, 4000, 0.30): (0.8800, 0.5279, 0.5868, 25), (1.0, 4000, 0.40): (0.7724, 0.4780, 0.6331, 24),
           (1.0, 4000, 0.50): (0.6670, 0.4602, 0.7261, 24), (1.0, 4000, 0.65): (0.5519, 0.5519, 0.8934, 22),
           (1.0, 16000, 0.25): (0.8226, 0.4094, 0.4397, 28), (1.0, 16000, 0.35): (0.7201, 0.4053, 0.4791, 28),
           (1.0, 16000, 0.45): (0.6167, 0.4345, 0.5500, 28), (1.0, 16000, 0.55): (0.5126, 0.4959, 0.6428, 27)}


def rung_table(u: float, n: int, phi: float, *, lam: float = 0.2, eta: float = 0.05, etap: float = 0.05, theta: float = 0.05,
               b: float = 0.5, Lr: int = 40, l_inv_delta: float = math.log(20.0)) -> dict:
    """The outer design of ``flat_run`` and, per rung, both servers: K0 (cost; its bracket of a flat fibre) and the
    cheapest middle 2L+ at the flat fibre (flat cost, bracket of the flat fibre, and its own cost bound C_max)."""
    n_o = min(max(int(math.floor(phi * n)), 1), n - 1)
    n_i = n - n_o
    x0 = 2 * u * n_i
    xs = [x0 * (b / x0) ** (l / Lr) for l in range(Lr + 1)]
    xs[-1] = b
    P = Params(n=n, n_o=n_o, u=u, lam=lam, eta=eta, etap=etap, theta=theta, nu1=max(1.0, 2 * math.exp(u) * n_o / theta), b=b, delta=1.0,
               xs=tuple(xs), ldelta=-l_inv_delta)
    outer = tables(n_o, u)
    C = constants(P, outer)
    rows = []
    for l in range(1, Lr + 1):
        x = xs[l]
        c0, a0, b0, k0 = k0_flat(n_i, u, x, C.l_inv_delta_p)
        row = dict(l=l, x=x, k0=(c0, a0, b0, k0), middle=None)
        cands = [(kw, flat_run(u, n_i, l_inv_delta=C.l_inv_delta_p, **kw)) for kw in middle_designs(u, n_i, x)]
        if cands:
            kw, cm = min(cands, key=lambda t: t[1]["lcost"])
            assert cm["xout"] <= x + 1e-9
            row["middle"] = (cm["lcost"], -cm["lL"], cm["lU"], cm["lCmax"])
            row["design"] = kw
        rows.append(row)
    return dict(P=P, outer=outer, C=C, rows=rows, n_o=n_o, n_i=n_i)


def worst_case(u: float, n: int, phi: float, budget: int = 4000, budget_general: int = 2000, seed: int = 1, k: int = 8) -> dict:
    """Two and three levels on adversarial *outer* landscapes (the families of X-005), at the level of expectations.

    two levels           every rung served by K0; inner behaviours "bottom" and "top"; inner offset searched
    three levels, L      rungs served as at the flat instance (the cheaper of K0 and the middle 2L+ there), **flat fibres**:
                         costs and brackets of the servers are those of a flat fibre.  A real instance (psi depends on
                         the outer block only), hence a lower bound on the worst case of three levels
    three levels, U      the same choice of servers, but every middle run charged its own cost bound C_max, inner
                         behaviours "bottom" and "top", inner offset searched: an upper bound for product instances
                         under those two behaviours
    """
    from metricchain_eng.twolevel.adversary import Family, Search
    from metricchain_eng.twolevel.alg2l import lC_max

    a = cube_constants(u).a
    T = rung_table(u, n, phi)
    P, outer, C, rows = T["P"], T["outer"], T["C"], T["rows"]
    na = n * a
    flat = Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=u * P.n_i)
    use_mid = [r["middle"] is not None and r["middle"][0] < r["k0"][0] for r in rows]
    lC2 = np.array([-math.inf] + [r["k0"][0] for r in rows])
    pos2 = ([r["k0"][1] for r in rows], [r["k0"][2] for r in rows])
    lC3 = np.array([-math.inf] + [r["middle"][0] if m else r["k0"][0] for r, m in zip(rows, use_mid)])
    pos3 = ([r["middle"][1] if m else r["k0"][1] for r, m in zip(rows, use_mid)], [r["middle"][2] if m else r["k0"][2] for r, m in zip(rows, use_mid)])
    lC3u = np.array([-math.inf] + [r["middle"][3] if m else r["k0"][0] for r, m in zip(rows, use_mid)])
    ev2, ev3, ev3u = Evaluator(P, outer, lC=lC2), Evaluator(P, outer, lC=lC3), Evaluator(P, outer, lC=lC3u)
    out = dict(u=u, n=n, phi=phi, n_o=P.n_o, n_i=P.n_i, a=a, budget=budget, budget_general=budget_general, seed=seed, x_out=C.x_out,
               served_by_middle=int(sum(use_mid)),
               flat2=ev2.run(flat, "bottom", positions=pos2).lcost / na, flat3=ev3.run(flat, "bottom", positions=pos3).lcost / na,
               cmax2=lC_max(P, C, lC2) / na, cmax3_flat_costs=lC_max(P, C, lC3) / na, cmax3_certified=lC_max(P, C, lC3u) / na,
               lower=hinted_lower_bound(n, u, C.x_out, 0.05) / na, searches=[])

    def search(name, ev, orc, positions, fixed):
        best = -math.inf
        for monotone, bud in ((True, budget), (False, budget_general)):
            S = Search(Family(ev, k=k, monotone=monotone), orc, "cost", positions=positions, fixed_c_in=fixed)
            res = S.run(bud, seed=seed)
            out["searches"].append(dict(name=name, oracle=orc, family="monotone" if monotone else "general", best=res.best_value / na,
                                        n_eval=res.n_eval, violations=len(res.violations), status=res.best_run.status,
                                        best_x=res.best_x.tolist()))
            best = max(best, res.best_value)
        return best / na

    out["worst2"] = max(search("two levels", ev2, orc, None, None) for orc in ("bottom", "top"))
    out["worst3_flat_fibres"] = search("three levels, flat fibres", ev3, "bottom", pos3, 0.0)
    out["worst3_capped_middle"] = max(search("three levels, middle at its cap", ev3u, orc, None, None) for orc in ("bottom", "top"))
    return out


def middle_designs(u: float, d: int, x: float) -> list[dict]:
    """The referee's candidates for the middle level in dimension d at accuracy x (keyword arguments of ``flat_run`` /
    ``cone_run`` without the failure probability); empty where only K0 is tried."""
    est = cube_constants(u).eps_star
    g = x / d
    if g >= 0.9 * est or d < 50:
        return []
    out = []
    if x >= 8:
        bm = x / 4
        lth = (x - bm) + math.log1p(-(3 * math.e + 1 + (2 / (1 + math.exp(u))) ** d * math.exp(-bm)) * math.exp(-(x - bm)))
        p0 = min(0.7, max(0.05, g / (g + theta_hint(u, g))))
        for p2 in (p0, min(0.8, 1.5 * p0)):
            if 2 * u * (d - int(p2 * d)) > bm * 1.5:
                out.append(dict(phi=p2, lam=1.0, eta=0.5, etap=1.0, ltheta=lth, b=bm, Lr=30, bounded=False))
    else:
        c = min(x / 12, 1 / 3)
        out.append(dict(phi=0.55, lam=c, eta=c, etap=c, theta=c, b=x / 2, Lr=30, bounded=True))
    return out


def cone_run(u: float, n: int, phi: float, slope: float, oracle: str, *, lam: float = 0.2, eta: float = 0.05, etap: float = 0.05,
             theta: float = 0.05, ltheta: float | None = None, b: float = 0.5, Lr: int = 40, bounded: bool = True,
             l_inv_delta: float = math.log(20.0)) -> dict:
    """Algorithm 2L+ with base brackets inside, at the level of expectations, on the cone psi(z) = slope u |z| of
    dimension n (reference point at the apex).  The cone is additive over coordinates, so it is a product instance
    for *every* split into an outer and an inner block: the outer landscape is the cone on the outer block and every
    fibre is the cone on the inner block.  Inner behaviour ``oracle`` for the base brackets: "bottom", "top", or
    "k0" -- the answer Proposition K0 itself gives on the cone fibre (``k0_cone``), which makes the run that of
    the concrete algorithm on a concrete instance.
    Returns the cost and where the average sits in the returned bracket (alpha, beta)."""
    from metricchain_eng.twolevel.meanrun import radial_law

    n_o = min(max(int(math.floor(phi * n)), 1), n - 1)
    n_i = n - n_o
    x0 = 2 * u * n_i
    xs = [x0 * (b / x0) ** (l / Lr) for l in range(Lr + 1)]
    xs[-1] = b
    lth = math.log(theta) if ltheta is None else ltheta
    nu1 = max(1.0, 2 * math.exp(u) * n_o / math.exp(lth)) if bounded else 1.0
    P = Params(n=n, n_o=n_o, u=u, lam=lam, eta=eta, etap=etap, theta=math.inf, nu1=nu1, b=b, delta=1.0, xs=tuple(xs),
               ltheta=lth, ldelta=-l_inv_delta)
    outer = tables(n_o, u)
    C = constants(P, outer)
    lC = np.array([-math.inf] + [k0_flat(n_i, u, xs[l], C.l_inv_delta_p)[0] for l in range(1, Lr + 1)])     # the cost of K0 does not depend on the fibre
    ev = Evaluator(P, outer, lC=lC)
    c_in = n_i * math.log((1 + math.exp(-slope * u)) / 2)
    F = slope * u * np.arange(n_o + 1, dtype=float)
    inst = Instance(radial_law(F, outer, shift=c_in), psi0=0.0, t0=u * n_i + c_in)
    if oracle == "k0":
        ans = [k0_cone(n_i, u, xs[l], C.l_inv_delta_p, slope) for l in range(1, Lr + 1)]
        R = ev.run(inst, "bottom", positions=([a[1] for a in ans], [a[2] for a in ans]))
    else:
        R = ev.run(inst, oracle)
    return dict(lcost=R.lcost, alpha=R.lA - R.lL, beta=R.lU - R.lA, lA=R.lA, width=R.lU - R.lL, xout=C.x_out, lCmax=R.lCmax, closed=R.closed,
                violations=R.violations(), status=R.status)


def worst_case_cone_fibres(u: float, n: int, phi: float, slope: float, oracle: str, budget: int = 4000, budget_general: int = 2000,
                           seed: int = 1, k: int = 8) -> dict:
    """Three levels on a real instance with adversarial fibres: psi(a, z) = F_o(a) + slope u |z|, the outer landscape
    F_o searched (the families of X-005), every fibre the cone of slope ``slope`` u in the inner dimension.

    The servers of the rungs are those chosen at the flat fibre (the design does not know the instance).  A rung
    served by K0 costs what K0 costs and returns a bracket placed by ``oracle``; a rung served by the middle level
    costs the mean run of that two-level design *on the cone* (``cone_run``, same ``oracle`` for its base brackets)
    and returns the bracket that run returns.  Every value is the cost of one instance under one valid inner
    behaviour: a lower bound on the worst case of three levels."""
    from metricchain_eng.twolevel.adversary import Family, Search

    a = cube_constants(u).a
    T = rung_table(u, n, phi)
    P, outer, C, rows = T["P"], T["outer"], T["C"], T["rows"]
    n_i = P.n_i
    lC, alphas, betas, mid_cost_flat, mid_cost_cone, bad = [-math.inf], [], [], [], [], 0
    for r in rows:
        x = r["x"]
        use_mid = r["middle"] is not None and r["middle"][0] < r["k0"][0]
        if use_mid:
            m = cone_run(u, n_i, slope=slope, oracle=oracle, l_inv_delta=C.l_inv_delta_p, **r["design"])
            bad += int((not m["closed"]) or bool(m["violations"]))
            assert m["alpha"] >= -1e-9 and m["beta"] >= -1e-9 and m["alpha"] + m["beta"] <= x + 1e-9, (m, x)
            lC.append(m["lcost"])
            alphas.append(max(m["alpha"], 0.0))
            betas.append(max(m["beta"], 0.0))
            mid_cost_flat.append(r["middle"][0])
            mid_cost_cone.append(m["lcost"])
        elif oracle == "k0":
            c0, a0, b0, _ = k0_cone(n_i, u, x, C.l_inv_delta_p, slope)
            lC.append(c0)
            alphas.append(a0)
            betas.append(b0)
        else:
            lC.append(r["k0"][0])
            alphas.append(0.0 if oracle == "bottom" else x)
            betas.append(x if oracle == "bottom" else 0.0)
    ev = Evaluator(P, outer, lC=np.array(lC))
    c_in = n_i * math.log((1 + math.exp(-slope * u)) / 2)
    best, neval, nviol = -math.inf, 0, 0
    for monotone, bud in ((True, budget), (False, budget_general)):
        S = Search(Family(ev, k=k, monotone=monotone), "bottom", "cost", positions=(alphas, betas), fixed_c_in=c_in)
        res = S.run(bud, seed=seed)
        best, neval, nviol = max(best, res.best_value), neval + res.n_eval, nviol + len(res.violations)
    return dict(u=u, n=n, phi=phi, slope=slope, oracle=oracle, worst3_cone_fibres=best / (n * a), n_eval=neval, outer_violations=nviol,
                middle_runs_not_closed_or_violating=bad, served_by_middle=len(mid_cost_cone),
                largest_middle_cost_ratio=max((c - f for c, f in zip(mid_cost_cone, mid_cost_flat)), default=0.0))


def worst_two_levels_flat_fibres(u: float, n: int, phi: float, budget: int = 4000, budget_general: int = 2000, seed: int = 1, k: int = 8) -> dict:
    """Two levels (every rung served by K0) on adversarial outer landscapes with **flat fibres**: the like-for-like
    partner of "three levels, flat fibres" in ``worst_case`` -- the same instances, one level fewer."""
    from metricchain_eng.twolevel.adversary import Family, Search

    a = cube_constants(u).a
    T = rung_table(u, n, phi)
    P, outer, rows = T["P"], T["outer"], T["rows"]
    ev2 = Evaluator(P, outer, lC=np.array([-math.inf] + [r["k0"][0] for r in rows]))
    pos2 = ([r["k0"][1] for r in rows], [r["k0"][2] for r in rows])
    best, neval = -math.inf, 0
    for monotone, bud in ((True, budget), (False, budget_general)):
        S = Search(Family(ev2, k=k, monotone=monotone), "bottom", "cost", positions=pos2, fixed_c_in=0.0)
        res = S.run(bud, seed=seed)
        best, neval = max(best, res.best_value), neval + res.n_eval
    return dict(u=u, n=n, phi=phi, worst2_flat_fibres=best / (n * a), n_eval=neval)


def three_level_row(u: float, n: int, phi: float) -> dict:
    a = cube_constants(u).a
    r2 = flat_run(u, n, phi)
    stats: list = []
    r3 = flat_run(u, n, phi, inner=make_inner(stats))
    lb = hinted_lower_bound(n, u, r3["xout"], 0.05)
    return dict(u=u, n=n, phi=phi, two=r2["lcost"] / (n * a), three=r3["lcost"] / (n * a), cmax3=r3["lCmax"] / (n * a), lower=lb / (n * a),
                served=sum(1 for s in stats if s[1] == "2L+"), width=r3["width"], xout=r3["xout"], valid=bool(r3["lL"] <= 1e-12 and r3["lU"] >= -1e-12))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--nmax", type=int, default=16000)
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    rows, worst = [], 0.0
    for (u, n, phi), ref in REFEREE.items():
        if n > args.nmax:
            continue
        t0 = time.time()
        r = three_level_row(u, n, phi)
        r["referee"] = ref
        r["seconds"] = time.time() - t0
        d = max(abs(round(r["two"], 4) - ref[0]), abs(round(r["three"], 4) - ref[1]), abs(round(r["cmax3"], 4) - ref[2]))
        worst = max(worst, d)
        rows.append(r)
        print(f"u={u} n={n} phi={phi:.2f}: two {r['two']:.4f} ({ref[0]})  three {r['three']:.4f} ({ref[1]})  C_max3 {r['cmax3']:.4f} ({ref[2]})"
              f"  served {r['served']} ({ref[3]})  valid {r['valid']} width {r['width']:.3f} <= {r['xout']:.3f}   [{r['seconds']:.0f} s]", flush=True)
    print(f"largest difference to the referee's values: {worst:.4f}")
    if args.out:
        Path(args.out).write_text(json.dumps(dict(rows=rows, largest_difference=worst), indent=1) + "\n")
    return 0 if (not args.check or worst < 5e-5) else 1


if __name__ == "__main__":
    raise SystemExit(main())
