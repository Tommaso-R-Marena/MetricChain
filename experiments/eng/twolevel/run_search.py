"""X-005: adversarial search for the worst instance of Algorithm 2L+ (THY-REQ-0001, Part B).

One *cell* is (u, n, phi) with the design parameters of the theory division's own cost table
(K_REPORT §6.4: b = 0.5, lambda = 0.2, eta = eta' = theta = 0.05, nu_1 = 2 e^u n_o / theta,
delta = 0.05, geometric ladder of inner rates eps* 0.85^i).  For a cell this script computes

  * the constants of Theorem 11.56 and the cap C_max;
  * the number of evaluations at the flat instance (both inner oracles);
  * the largest number of evaluations found by a search over radial instances
    (monotone and general profiles, both oracles), with the extremes of every claim of the
    theorem over all instances evaluated;
  * optionally searches that maximise a claim's slack instead of the cost.

    python experiments/eng/twolevel/run_search.py --u 1 --n 1000 --phi 0.5 0.8 --budget 4000
    python experiments/eng/twolevel/run_search.py --grid small --out results/x.json

The Modal app ``modal_jobs/twolevel_app.py`` maps ``cell`` over the full grid.
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
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel.adversary import Family, Search, describe_profile  # noqa: E402
from metricchain_eng.twolevel.alg2l import (Params, base_family, claimed_exponent, hinted_lower_bound,  # noqa: E402
                                            tau2)
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, Law  # noqa: E402
from metricchain_eng.twolevel.tables import CubeTables, cube_constants  # noqa: E402

PHIS = (0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85)
NS = (250, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000)
US = (0.5, 1.0, 2.0)
DESIGN = dict(b=0.5, lam=0.2, eta=0.05, etap=0.05, theta=0.05, delta=0.05, ladder_ratio=0.85, ladder_len=40)


def design_params(n: int, u: float, phi: float, design: dict = DESIGN) -> tuple[Params, tuple]:
    """Parameters of the theory division's cost table for (n, u, phi); also the inner rates used."""
    c = cube_constants(u)
    n_o = max(1, min(n - 1, int(math.floor(phi * n))))
    n_i = n - n_o
    b = design["b"]
    rates = [c.eps_star * design["ladder_ratio"] ** i for i in range(design["ladder_len"])]
    used = [r for r in rates if b < r * n_i < 2 * u * n_i]
    xs = [2 * u * n_i] + [r * n_i for r in used] + [b]
    P = Params(n=n, n_o=n_o, u=u, lam=design["lam"], eta=design["eta"], etap=design["etap"], theta=design["theta"],
               nu1=max(1.0, 2 * math.exp(u) * n_o / design["theta"]), b=b, delta=design["delta"], xs=tuple(xs))
    return P, tuple(used)


def _run_summary(R, n: int) -> dict:
    return dict(status=R.status, lcost=R.lcost, lM_max=R.lM_max, lM_last=R.lM_last, r_close=R.r_close, j_stop=R.j_stop,
                npop=R.npop, nneg=R.nneg, width=R.width, cost_over_cap=R.lcost - R.lCmax,
                slack_v=R.slack_v, slack_vi=R.slack_vi, slack_iv_Mneg=R.slack_iv_Mneg, slack_iv_Mbar=R.slack_iv_Mbar,
                margin_iii=R.margin_iii, violations=R.violations())


def cell(u: float, n: int, phi: float, budget: int = 4000, budget_general: int = 2000, seed: int = 1, k: int = 8,
         objectives: tuple = ("cost",), design: dict = DESIGN) -> dict:
    """Everything for one (u, n, phi); see the module docstring."""
    t_start = time.time()
    c = cube_constants(u)
    P, rates = design_params(n, u, phi, design)
    ev = Evaluator(P)
    C = ev.C
    out = dict(u=u, n=n, phi=phi, n_o=P.n_o, n_i=P.n_i, design=design, budget=budget, budget_general=budget_general,
               seed=seed, k=k, a=c.a, h=c.h,
               constants=dict(J=C.J, K=C.K, nu0=C.nu0, r_dag=C.r_dag, lpi_dag=C.lpi_dag, m_max=C.m_max, L=P.L,
                              lM_dag=C.lM_dag, lM_bar=C.lM_bar, x_out=C.x_out, lCmax=ev.lCmax,
                              lC_finest=float(ev.lC[-1]), lC_first=float(ev.lC[1])),
               claimed_exponent=claimed_exponent(u, P.n_o / n, rates))
    flat = Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=u * P.n_i)
    out["flat"] = {orc: _run_summary(ev.run(flat, orc), n) for orc in ("bottom", "top")}
    searches = []
    for objective in objectives:
        for monotone, bud in ((True, budget), (False, budget_general)):
            if bud <= 0:
                continue
            fam = Family(ev, k=k, monotone=monotone)
            for orc in ("bottom", "top"):
                t0 = time.time()
                S = Search(fam, orc, objective)
                for x in S.seeds():
                    S.evaluate(x)
                seeds_best = S.res.best_value
                res = S.run(bud, seed=seed)
                F, d0, c_in = fam.decode(res.best_x)
                searches.append(dict(
                    objective=objective, family="monotone" if monotone else "general", oracle=orc, n_eval=res.n_eval,
                    best_value=res.best_value, seeds_best=seeds_best, best_x=res.best_x.tolist(), d0=d0, c_in=c_in,
                    profile=describe_profile(F, u, n_seg_max=40), best_run=_run_summary(res.best_run, n),
                    extremes=res.extremes, n_violations=len(res.violations), violations=res.violations[:3],
                    seconds=time.time() - t0))
    out["searches"] = searches
    out["seconds"] = time.time() - t_start
    return out


def reference_columns(u: float, n: int, x_out: float, delta: float = 0.05) -> dict:
    """The comparison columns of the theory division's table: the plain two-sample bracket in dimension n at the
    certified accuracy, and the hinted lower bound at that accuracy."""
    fam = base_family(n, u)
    return dict(plain=fam.lcost(x_out, math.log(1 / delta)), lower=hinted_lower_bound(n, u, x_out, delta, fam.tables))


NS_COST = (250, 350, 500, 700, 1000, 1400, 2000, 4000, 8000, 16000, 32000, 64000, 128000)


def tasks(job: str) -> list[dict]:
    """Task lists of the Modal jobs (keyword arguments of ``cell``).

    cost      every (u, n, phi) of the table, objective "cost"; the search budget is reduced at the two
              largest sizes so that a task stays near a quarter of an hour of one core
    claims    searches that maximise the slack of a claim of Theorem 11.56 instead of the cost
    converge  larger budgets and other seeds on a few cells (is the search budget the limitation?)
    converge2 the same question at the two largest sizes, phi = 0.5, all three slopes
    """
    out = []
    if job == "cost":
        for u in US:
            for n in NS_COST:
                bud = {128000: (1500, 750), 64000: (2500, 1250)}.get(n, (4000, 2000))
                for phi in PHIS:
                    out.append(dict(u=u, n=n, phi=phi, budget=bud[0], budget_general=bud[1], seed=1, objectives=("cost",)))
    elif job == "claims":
        for u in US:
            for n in (1000, 8000, 64000):
                for phi in (0.35, 0.5, 0.65, 0.8):
                    for obj in ("cost_minus_cap", "count", "Mneg", "sample", "vi"):
                        out.append(dict(u=u, n=n, phi=phi, budget=3000, budget_general=1500, seed=1, objectives=(obj,)))
    elif job == "converge":
        for n in (1000, 16000):
            for phi in (0.5, 0.65):
                for seed in (2, 3):
                    bud = (20000, 10000) if n <= 1000 else (12000, 6000)
                    out.append(dict(u=1.0, n=n, phi=phi, budget=bud[0], budget_general=bud[1], seed=seed, objectives=("cost",)))
    elif job == "converge2":
        # the two largest sizes had the smallest budgets in job M-008 (SCI-REV-0008, R7-ENG-4): three times those
        # budgets and two other seeds, at the outer fraction that is best against the worst instance there
        for u in US:
            for n, bud in ((64000, (7500, 3750)), (128000, (4500, 2250))):
                for seed in (2, 3):
                    out.append(dict(u=u, n=n, phi=0.5, budget=bud[0], budget_general=bud[1], seed=seed, objectives=("cost",)))
    elif job == "smoke":
        out.append(dict(u=1.0, n=250, phi=0.5, budget=300, budget_general=150, seed=1, objectives=("cost",)))
        out.append(dict(u=2.0, n=500, phi=0.65, budget=300, budget_general=150, seed=1, objectives=("count",)))
    else:
        raise ValueError(job)
    return out


def estimated_core_seconds(task: dict) -> float:
    """One mean run takes about 1.33 microseconds per unit of n on the development machine and about twice
    that on a Modal core (measured by the smoke test of job M-008); the figure returned is for Modal."""
    n_obj = len(task["objectives"])
    return n_obj * 2 * (task["budget"] + task["budget_general"] + 126) * 2.66e-6 * task["n"]


def grid(name: str) -> list[tuple]:
    if name == "small":
        return [(u, n, phi) for u in (1.0,) for n in (250, 1000) for phi in (0.4, 0.5, 0.65, 0.8)]
    if name == "full":
        return [(u, n, phi) for u in US for n in NS for phi in PHIS]
    raise ValueError(name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--u", type=float)
    ap.add_argument("--n", type=int)
    ap.add_argument("--phi", type=float, nargs="*")
    ap.add_argument("--grid", choices=("small", "full"))
    ap.add_argument("--budget", type=int, default=4000)
    ap.add_argument("--budget-general", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--objectives", nargs="*", default=["cost"])
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    cells = grid(args.grid) if args.grid else [(args.u, args.n, phi) for phi in (args.phi or PHIS)]
    rows = []
    for u, n, phi in cells:
        r = cell(u, n, phi, args.budget, args.budget_general, args.seed, objectives=tuple(args.objectives))
        rows.append(r)
        a = r["a"]
        best = max(s["best_value"] for s in r["searches"] if s["objective"] == "cost") if "cost" in args.objectives else float("nan")
        nviol = sum(s["n_violations"] for s in r["searches"])
        print(f"u={u} n={n} phi={phi:.2f}: flat {max(r['flat'][o]['lcost'] for o in r['flat']) / (n * a):.4f}  worst found {best / (n * a):.4f}"
              f"  C_max {r['constants']['lCmax'] / (n * a):.4f}  claimed limit {r['claimed_exponent'] / a:.4f}  violations {nviol}"
              f"  ({r['seconds']:.0f} s)", flush=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
