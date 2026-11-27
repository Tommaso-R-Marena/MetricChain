"""X-005b: how much can instances that are not products cost?  (SCI-REV-0008 §4, point (1).)

The search family of X-005 consists of product instances: every fibre sits at the same place t0 of
its trivial bracket.  An instance in which t0 varies from fibre to fibre is in the class and outside
that family.  For such an instance the sample sizes of the outer loop depend only on the law of the
fibre averages (and on the inner behaviour through the classification shift c); the fibres' places
enter through the refinement windows alone.  Replacing every window by its union over all feasible
places t0 in [n_i (u - Lambda_1), n_i (2u - Lambda_1)] gives an upper bound on the number of
evaluations of **every** instance with that law (``meanrun.rung_positions``, ``t0`` as a pair).

This script evaluates that bound at every stored maximiser of X-005 and at the flat laws, and
reports how far it lies above the stored (product) cost.

    python experiments/eng/twolevel/nonproduct_bound.py --out experiments/eng/twolevel/results/x005_nonproduct_bound.json
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

import run_search  # noqa: E402
from metricchain_eng.twolevel.adversary import Family  # noqa: E402
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.tables import cube_constants  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", nargs="*", default=["cost"])
    ap.add_argument("--nmax", type=int, default=10 ** 9)
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    t_start = time.time()
    cells = []
    for job in args.jobs:
        path = Path(__file__).resolve().parent / "results" / f"x005_{job}.jsonl"
        for line in path.read_text().splitlines():
            c = json.loads(line)
            if c["n"] > args.nmax:
                continue
            P, _ = run_search.design_params(c["n"], c["u"], c["phi"], c["design"])
            ev = Evaluator(P)
            cc = cube_constants(c["u"])
            rng = (P.n_i * (c["u"] - cc.Lambda1), P.n_i * (2 * c["u"] - cc.Lambda1))
            na = c["n"] * c["a"]
            cell = dict(job=job, u=c["u"], n=c["n"], phi=c["phi"], na=na, worst_product=-math.inf, worst_bound=-math.inf, max_gap=0.0, violations=0,
                        calls_gap=[])
            for s in c["searches"]:
                if s["objective"] != "cost":
                    continue
                fam = Family(ev, k=c["k"], monotone=(s["family"] == "monotone"))
                F, d0, c_in = fam.decode(np.array(s["best_x"]))
                inst = fam.instance(F, d0, c_in)
                R = ev.run(inst, s["oracle"])
                Rb = ev.run(inst, s["oracle"], t0_range=rng)
                assert Rb.j_stop == R.j_stop and abs(Rb.lM_max - R.lM_max) < 1e-12        # the sample is the same
                assert Rb.lcost >= R.lcost - 1e-9
                cell["worst_product"] = max(cell["worst_product"], R.lcost)
                cell["worst_bound"] = max(cell["worst_bound"], Rb.lcost)
                cell["max_gap"] = max(cell["max_gap"], Rb.lcost - R.lcost)
                cell["violations"] += int(Rb.lcost > Rb.lCmax + 1e-9)
            cells.append(cell)
    by = {}
    for c in cells:
        k = f"{c['u']:g}"
        by.setdefault(k, dict(cells=0, max_gap=0.0, max_gap_over_na=0.0, max_worst_increase_over_na=0.0, worst_increase_at=None))
        b = by[k]
        b["cells"] += 1
        b["max_gap"] = max(b["max_gap"], c["max_gap"])
        b["max_gap_over_na"] = max(b["max_gap_over_na"], c["max_gap"] / c["na"])
        inc = (c["worst_bound"] - c["worst_product"]) / c["na"]
        if inc > b["max_worst_increase_over_na"]:
            b["max_worst_increase_over_na"] = inc
            b["worst_increase_at"] = dict(n=c["n"], phi=c["phi"], increase=c["worst_bound"] - c["worst_product"])
    report = dict(cells=cells, by_u=by, above_Cmax=sum(c["violations"] for c in cells), seconds=time.time() - t_start)
    print(json.dumps(dict(by_u=by, above_Cmax=report["above_Cmax"]), indent=1))
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
