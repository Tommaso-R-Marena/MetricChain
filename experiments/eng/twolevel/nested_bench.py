"""X-011: nested runs of Algorithm 2L+ designed by certified cost — the bound, the best case and the worst case found.

Two kinds of cell (each one task of ``modal_jobs/bench_app.py``, or of the local driver at the end of this file):

``certified_cell``   the certified cost bound of at most k nested levels, minimised over a grid of outer fractions of
                     the top level and over a family of designs for every level below it (``certified.Search``: an
                     exact minimisation with pruning; no instance is evaluated);
``instance_cell``    the design tree that ``certified_cell`` selects at one outer fraction, *run* in the mean-run
                     model: at the flat instance (its best case), and on the worst outer landscape an adversarial
                     search finds, with fibres that are flat, or cones on which every base bracket gives its own
                     answer (reading (B) of ENG-RES-0014: the algorithm as built), or cones with every base bracket
                     placed at the bottom or at the top of what it promised (reading (A): the theorem as stated).

The top level is the design of ENG-RES-0014 §2 and of the theory report's remark (1b): b = 0.5, lambda = 0.2,
eta = eta' = theta = 0.05, delta = 0.05, the ladder x_l = x_0 (b/x_0)^{l/40}; certified accuracy 0.8715.

    python experiments/eng/twolevel/nested_bench.py --check        # against published numbers (theory branch, ENG-RES-0014)
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
sys.path.insert(0, str(Path(__file__).resolve().parent))

from metricchain_eng.twolevel.alg2l import constants, hinted_lower_bound  # noqa: E402
from metricchain_eng.twolevel.certified import (LevelBound, Search, k0_lcost, level_params, tables,  # noqa: E402
                                                top_design)
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, Law, radial_law  # noqa: E402
from metricchain_eng.twolevel.tables import LN2, cube_constants  # noqa: E402

LID = math.log(20.0)            # delta = 0.05 at the top level
PHIS = (0.60, 0.55, 0.50, 0.45, 0.425, 0.40, 0.375, 0.35, 0.325, 0.30, 0.275, 0.25, 0.225, 0.20, 0.175, 0.15, 0.125, 0.10)


# ---------------------------------------------------------------------------------------------
# Certified bounds
# ---------------------------------------------------------------------------------------------
def tree_summary(lb: LevelBound, na: float, max_depth: int = 3) -> dict:
    """What serves the rungs of a level, recursively along the rung that carries the largest term."""
    kinds = ["2L+" if isinstance(s, LevelBound) else str(s) for s in lb.servers]
    top = int(np.argmax(lb.lterm))
    out = dict(design=lb.design.name, n_o=lb.n_o, n_i=lb.n_i, bound=lb.lCmax / na, accuracy=lb.xout,
               outer_sample=(LN2 + lb.lM_bar) / na, levels=lb.depth(),
               rungs_by_server={k: kinds.count(k) for k in sorted(set(kinds))},
               largest_term=dict(rung=top + 1, accuracy=lb.xs[top + 1], term=float(lb.lterm[top]) / na, server_cost=float(lb.lC[top + 1]) / na))
    nested = [s for s in lb.servers if isinstance(s, LevelBound)]
    if nested:
        acc = [lb.xs[i + 1] for i, s in enumerate(lb.servers) if isinstance(s, LevelBound)]
        out["nested_accuracies"] = [min(acc), max(acc)]
        out["nested_designs"] = sorted({s.design.name.split("(")[0] for s in nested})
    s = lb.servers[top]
    if isinstance(s, LevelBound) and max_depth > 1:
        out["largest_term"]["server"] = tree_summary(s, na, max_depth - 1)
    return out


def certified_cell(u: float, n: int, family: str, max_levels: int, phis=PHIS, time_limit: float = math.inf) -> dict:
    """ln(C_max)/(n a) of at most k = 1..max_levels nested levels of Algorithm 2L+ above base brackets (k nested levels
    are "k + 1 levels" in the reports, which count the base brackets), per outer fraction of the top level and at the
    best one.  For k >= 2 a fraction whose bound is not below the best bound already found (with fewer levels, or at
    an earlier fraction with as many) is reported as None: the search proves that it is not better and stops there.
    ``time_limit`` (seconds): what is unfinished when it is reached is reported as such; finished rows are kept."""
    cc = cube_constants(u)
    na = n * cc.a
    S = Search(u, family)
    t0 = time.time()
    S.deadline = t0 + time_limit if math.isfinite(time_limit) else None
    rows = []
    best_prev = math.inf
    order = list(phis)
    for k in range(1, max_levels + 1):
        per_phi, best, best_lb, timed_out = {}, math.inf, None, False
        for phi in order:
            cutoff = min(best, best_prev + 1e-9 * na) if k > 1 else math.inf
            try:
                lb = S.top(n, top_design(phi), LID, k, cutoff=cutoff)
            except TimeoutError:
                timed_out = True
                break
            if lb is None:
                per_phi[phi] = None
                continue
            per_phi[phi] = lb.lCmax / na
            if lb.lCmax < best:
                best, best_lb = lb.lCmax, (phi, lb)
        row = dict(nested_levels=k, per_phi={f"{p:g}": per_phi.get(p, "not computed (time limit)") for p in phis}, complete=not timed_out,
                   seconds=time.time() - t0, nodes=S.nodes, level_evaluations=S.levels)
        if best_lb is not None:
            row.update(best=best / na, best_phi=best_lb[0], tree=tree_summary(best_lb[1], na), improved=bool(best < best_prev - 1e-9 * na))
        else:
            row.update(best=None, best_phi=None, improved=False)     # no fraction (of those finished) is below the bound with fewer levels
        rows.append(row)
        if timed_out:
            break
        best_prev = min(best_prev, best)
        # next depth: the fractions in the order of their bound at this depth (a good cutoff early), unevaluated ones last
        order = sorted(phis, key=lambda p: (per_phi.get(p) is None, per_phi.get(p) if per_phi.get(p) is not None else -p))
    x_out = top_bound_accuracy(u, n)
    return dict(kind="certified", u=u, n=n, family=family, a=cc.a, h_over_a=cc.h / cc.a, x_out=x_out,
                lower_bound=hinted_lower_bound(n, u, x_out, 0.05) / na, base_bracket=k0_lcost(n, u, x_out, LID)[0] / na,
                enumeration=n * LN2 / na, rows=rows, seconds=time.time() - t0)


def top_bound_accuracy(u: float, n: int, phi: float = 0.5) -> float:
    P = level_params(u, n, top_design(phi), LID)
    return constants(P, tables(P.n_o, u)).x_out


# ---------------------------------------------------------------------------------------------
# A design tree run in the mean-run model
# ---------------------------------------------------------------------------------------------
def k0_answer(d: int, u: float, x: float, lid: float, slope: float):
    """(ln cost, alpha, beta) of the base bracket on the cone of slope ``slope`` u (0: flat) — its own answer."""
    from three_levels import k0_cone

    c, a_, b_, _ = k0_cone(d, u, x, lid, slope)
    return c, a_, b_


def server_on_cone(server, d: int, x: float, lid: float, u: float, slope: float, oracle: str):
    """(ln cost, alpha, beta, ok): cost of a rung's server on the cone fibre of dimension d and where the fibre
    average sits in the bracket it returns, [A e^-alpha, A e^beta].  ``oracle``: "k0" (base brackets give their own
    answers), "bottom" or "top" (base brackets place the average at an end of a bracket of the full promised width)."""
    if isinstance(server, LevelBound):
        return level_on_cone(server, u, slope, oracle, lid)
    if oracle == "k0":
        c, a_, b_ = k0_answer(d, u, x, lid, slope)
        return c, a_, b_, True
    c0, _ = k0_lcost(d, u, x, lid)
    return c0, (0.0 if oracle == "bottom" else x), (x if oracle == "bottom" else 0.0), True


def level_setup(lb: LevelBound, u: float, lid: float, slope: float, oracle: str):
    """Evaluator of the level ``lb`` when its fibres are cones of slope ``slope`` u: per-rung costs and positions."""
    d = lb.n_o + lb.n_i
    P = level_params(u, d, lb.design, lid)
    outer = tables(P.n_o, u)
    C = constants(P, outer)
    lC, alphas, betas, ok = [-math.inf], [], [], True
    for l in range(1, P.L + 1):
        c, a_, b_, good = server_on_cone(lb.servers[l - 1], P.n_i, P.xs[l], C.l_inv_delta_p, u, slope, oracle)
        assert a_ >= -1e-9 and b_ >= -1e-9 and a_ + b_ <= P.xs[l] + 1e-9, (a_, b_, P.xs[l])
        lC.append(c)
        alphas.append(max(a_, 0.0))
        betas.append(max(b_, 0.0))
        ok = ok and good
    c_in = P.n_i * math.log((1 + math.exp(-slope * u)) / 2)
    return P, outer, C, Evaluator(P, outer, lC=np.array(lC)), (alphas, betas), c_in, ok


def level_on_cone(lb: LevelBound, u: float, slope: float, oracle: str, lid: float):
    """The mean run of the nested procedure ``lb`` on the cone of slope ``slope`` u in its own dimension (the cone is
    additive, hence a product instance for every split): (ln cost, alpha, beta, ok)."""
    P, outer, C, ev, pos, c_in, ok = level_setup(lb, u, lid, slope, oracle)
    F = slope * u * np.arange(P.n_o + 1, dtype=float)
    inst = Instance(radial_law(F, outer, shift=c_in), psi0=0.0, t0=u * P.n_i + c_in)
    R = ev.run(inst, "bottom", positions=pos)
    good = ok and R.closed and not R.violations()
    return R.lcost, R.lA - R.lL, R.lU - R.lA, good


def instance_cell(u: float, n: int, phi: float, family: str, nested_levels: int, readings=("flat", "B", "A"), slope: float = 1.0,
                  budget: int = 4000, budget_general: int = 2000, seed: int = 1, k: int = 8) -> dict:
    """The design that the certified-cost rule selects at outer fraction ``phi`` (``family``, at most ``nested_levels``
    nested levels of Algorithm 2L+), run in the mean-run model:

      flat_instance   every landscape flat (the best case);
      "flat"          worst outer landscape found, flat fibres (base brackets' own answers);
      "B"             worst outer landscape found, cone fibres of slope ``slope`` u, base brackets' own answers;
      "A"             the larger of two searches: cone fibres (nested_levels >= 2) or any fibre with the inner offset
                      searched (nested_levels = 1), every base bracket placing the average at the bottom, or at the top,
                      of a bracket of its full promised width.
    Every searched value is the cost of one instance: a lower bound on the worst case of the design.
    """
    from metricchain_eng.twolevel.adversary import Family
    from metricchain_eng.twolevel.adversary import Search as AdvSearch

    cc = cube_constants(u)
    na = n * cc.a
    t0 = time.time()
    lb = Search(u, family).top(n, top_design(phi), LID, nested_levels)
    out = dict(kind="instance", u=u, n=n, phi=phi, family=family, nested_levels=nested_levels, slope=slope, budget=budget,
               budget_general=budget_general, seed=seed, a=cc.a, certified=lb.lCmax / na, levels_used=lb.depth(),
               tree=tree_summary(lb, na), searches=[], design_seconds=time.time() - t0)
    P, outer, C, ev, pos, c_in, ok = level_setup(lb, u, LID, 0.0, "k0")
    flat = Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=u * P.n_i)
    R = ev.run(flat, "bottom", positions=pos)
    out.update(x_out=C.x_out, flat_instance=R.lcost / na, flat_ok=bool(ok and R.closed and not R.violations()),
               lower_bound=hinted_lower_bound(n, u, C.x_out, 0.05) / na)

    def search(name, ev, orc, positions, fixed, good):
        best = -math.inf
        for monotone, bud in ((True, budget), (False, budget_general)):
            S = AdvSearch(Family(ev, k=k, monotone=monotone), orc, "cost", positions=positions, fixed_c_in=fixed)
            res = S.run(bud, seed=seed)
            out["searches"].append(dict(name=name, family="monotone" if monotone else "general", best=res.best_value / na, n_eval=res.n_eval,
                                        violations=len(res.violations), status=res.best_run.status, servers_ok=bool(good),
                                        best_x=res.best_x.tolist()))
            best = max(best, res.best_value)
        return best / na

    for reading in readings:
        if reading == "flat":
            out["worst_flat_fibres"] = search("flat fibres", ev, "bottom", pos, 0.0, ok)
        elif reading == "B":
            _, _, _, evB, posB, cB, okB = level_setup(lb, u, LID, slope, "k0")
            out["worst_B"] = search(f"cone fibres slope {slope:g}, own answers", evB, "bottom", posB, cB, okB)
        elif reading == "A":
            vals = []
            for orc in ("bottom", "top"):
                if nested_levels == 1:
                    lC = np.array([-math.inf] + [k0_lcost(P.n_i, u, P.xs[l], C.l_inv_delta_p)[0] for l in range(1, P.L + 1)])
                    vals.append(search(f"any fibre, base brackets at the {orc}", Evaluator(P, outer, lC=lC), orc, None, None, True))
                else:
                    _, _, _, evA, posA, cA, okA = level_setup(lb, u, LID, slope, orc)
                    vals.append(search(f"cone fibres slope {slope:g}, base brackets at the {orc}", evA, "bottom", posA, cA, okA))
            out["worst_A"] = max(vals)
        else:
            raise ValueError(reading)
    out["seconds"] = time.time() - t0
    return out


# ---------------------------------------------------------------------------------------------
# Job lists (shared by the Modal app and the local driver)
# ---------------------------------------------------------------------------------------------
SIZES = (1000, 1400, 2000, 4000, 8000, 16000, 32000, 64000, 128000)
BUDGETS = {1000: (4000, 2000), 4000: (4000, 2000)}          # evaluations of the monotone and of the general family
BUDGET_LARGE = (2500, 1250)                                 # n >= 8000 (as in X-010)
INSTANCE_PHIS = (0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15)


def tasks(job: str) -> list[dict]:
    """Task lists.  Every task has a unique id and a tier (run-time bound of ``modal_jobs/bench_app.py``)."""
    out = []
    if job == "smoke":
        out.append(dict(func="certified_cell", tier="s", kwargs=dict(u=1.0, n=1000, family="theory", max_levels=3, time_limit=900)))
        out.append(dict(func="instance_cell", tier="s", kwargs=dict(u=1.0, n=1000, phi=0.5, family="theory", nested_levels=2, budget=150, budget_general=80)))
    elif job == "certified1":
        # stage 1 of Q-01: u = 1, nine sizes, two design families, up to five nested levels
        for n in SIZES:
            for fam in ("theory", "wide"):
                tier = "l" if n <= 8000 else "xl" if n <= 16000 else "xxl"
                limit = {"l": 10800, "xl": 21600, "xxl": 43200}[tier] - 900
                out.append(dict(func="certified_cell", tier=tier, kwargs=dict(u=1.0, n=n, family=fam, max_levels=5, time_limit=limit)))
    elif job == "instances1":
        # stage 1 of Q-02 and Q-03: the designs selected by certified cost (theory's candidate family), run
        for n in (1000, 4000, 16000):
            b, bg = BUDGETS.get(n, BUDGET_LARGE)
            for k in (1, 2, 3):
                for phi in INSTANCE_PHIS:
                    out.append(dict(func="instance_cell", tier="m" if n <= 4000 else "l",
                                    kwargs=dict(u=1.0, n=n, phi=phi, family="theory", nested_levels=k, budget=b, budget_general=bg)))
        for n in (8000, 32000, 64000):                       # Q-03 (R16-THY-1(b)): two levels at three more sizes
            b, bg = BUDGET_LARGE
            for phi in (0.65, 0.60, 0.55, 0.50, 0.45, 0.40):
                out.append(dict(func="instance_cell", tier="l" if n <= 32000 else "xl",
                                kwargs=dict(u=1.0, n=n, phi=phi, family="theory", nested_levels=1, readings=("B", "A"), budget=b, budget_general=bg)))
    else:
        raise ValueError(job)
    for t_ in out:
        kw = t_["kwargs"]
        t_["id"] = t_["func"] + ":" + ",".join(f"{k}={kw[k]}" for k in sorted(kw) if k not in ("time_limit",))
    return out


def run_task(task: dict) -> dict:
    fn = {"certified_cell": certified_cell, "instance_cell": instance_cell}[task["func"]]
    return fn(**task["kwargs"])


# ---------------------------------------------------------------------------------------------
# Checks against published numbers
# ---------------------------------------------------------------------------------------------
PUBLISHED_CERTIFIED = {  # theory branch, experiments/coordinator_checks/three_levels_certified/README.md (u = 1):
    # n: (two levels, three levels with "more middle designs", its outer fraction)
    1000: (1.1384, 1.1384, 0.5), 4000: (0.7262, 0.6106, 0.375), 16000: (0.5899, 0.4782, 0.3)}


def check() -> int:
    bad = 0
    for n, (two, three, phi3) in PUBLISHED_CERTIFIED.items():
        na = n * cube_constants(1.0).a
        S = Search(1.0, "theory")
        v2 = S.top(n, top_design(0.5), LID, 1).lCmax / na
        v3 = S.top(n, top_design(phi3), LID, 2).lCmax / na
        ok = abs(v2 - two) < 5e-5 and v3 <= three + 5e-5
        bad += not ok
        print(f"n={n}: two levels {v2:.4f} (published {two}); three levels at phi={phi3}: {v3:.4f} (published {three}; the exhaustive "
              f"minimum over the same candidates may be lower) {'ok' if ok else 'DIFFERS'}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--job", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if args.check:
        return check()
    if args.job:
        out = Path(args.out) if args.out else ROOT / "experiments" / "eng" / "twolevel" / "results" / f"x011_{args.job}.jsonl"
        with out.open("a") as fh:
            for t in tasks(args.job):
                r = run_task(t)
                fh.write(json.dumps(r) + "\n")
                fh.flush()
                print(json.dumps({k: v for k, v in r.items() if k not in ("rows", "searches", "tree")})[:400], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
