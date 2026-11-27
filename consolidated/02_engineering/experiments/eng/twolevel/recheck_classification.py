"""X-005: the stored maximisers under the exact classification rule.

The mean runs of X-005 (jobs M-008, M-009, M-010, M-013) counted a sample point HIGH at the level s iff
W > s e^{-b} ("bottom") or W > s ("top").  The algorithm classifies by the brackets it holds, and the
trivial bracket of rung 0 changes the rule in two corners (``meanrun.rung_positions``): "top" with
t0 < b and "bottom" with x_0 - t0 < b.  This script re-evaluates every stored best point with both
rules and reports how many lie in a corner, by how much ln(cost) changes, whether any claim of
Theorem 11.56 is violated under the exact rule, and what the worst instance of each cell becomes.

    python experiments/eng/twolevel/recheck_classification.py --out experiments/eng/twolevel/results/x005_recheck_classification.json
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
from metricchain_eng.twolevel.adversary import Family, objective_value  # noqa: E402
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    # the table of ENG-RES-0014 §1 and the stored x005_recheck_classification.json are these three jobs (2 624 stored
    # maximisers); "converge2" (48 more) can be added on the command line (SCI-REV-0018, finding m6)
    ap.add_argument("--jobs", nargs="*", default=["cost", "claims", "converge"])
    ap.add_argument("--nmax", type=int, default=10 ** 9)
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    t0 = time.time()
    report = dict(jobs={}, cells=[])
    for job in args.jobs:
        path = Path(__file__).resolve().parent / "results" / f"x005_{job}.jsonl"
        if not path.exists():
            continue
        out = report["jobs"][job] = dict(searches=0, in_corner=0, legacy_reproduces_stored=0, max_abs_legacy_minus_stored=0.0,
                                          changed=0, max_increase=0.0, max_decrease=0.0, max_increase_over_na=0.0, max_decrease_over_na=0.0,
                                          violations_exact=0, violation_examples=[])
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            c = json.loads(line)
            if c["n"] > args.nmax:
                continue
            P, _ = run_search.design_params(c["n"], c["u"], c["phi"], c["design"])
            ev = Evaluator(P)
            na = c["n"] * c["a"]
            x0, b = P.xs[0], P.b
            cell = dict(job=job, u=c["u"], n=c["n"], phi=c["phi"], seed=c.get("seed", 1), stored_worst=-math.inf, exact_worst=-math.inf, na=na)
            for s in c["searches"]:
                fam = Family(ev, k=c["k"], monotone=(s["family"] == "monotone"))
                F, d0, c_in = fam.decode(np.array(s["best_x"]))
                inst = fam.instance(F, d0, c_in)
                corner = (s["oracle"] == "top" and inst.t0 < b) or (s["oracle"] == "bottom" and x0 - inst.t0 < b)
                Rl = ev.run(inst, s["oracle"], legacy_classification=True)
                Re = ev.run(inst, s["oracle"])
                vl, ve = objective_value(Rl, s["objective"]), objective_value(Re, s["objective"])
                out["searches"] += 1
                out["in_corner"] += int(bool(corner))
                d_legacy = abs(vl - s["best_value"])
                out["legacy_reproduces_stored"] += int(d_legacy < 1e-6)
                out["max_abs_legacy_minus_stored"] = max(out["max_abs_legacy_minus_stored"], d_legacy)
                if Re.violations():
                    out["violations_exact"] += 1
                    if len(out["violation_examples"]) < 5:
                        out["violation_examples"].append(dict(u=c["u"], n=c["n"], phi=c["phi"], objective=s["objective"], oracle=s["oracle"], violations=Re.violations()))
                if s["objective"] == "cost":
                    d = Re.lcost - Rl.lcost
                    out["changed"] += int(abs(d) > 1e-9)
                    out["max_increase"] = max(out["max_increase"], d)
                    out["max_decrease"] = min(out["max_decrease"], d)
                    out["max_increase_over_na"] = max(out["max_increase_over_na"], d / na)
                    out["max_decrease_over_na"] = min(out["max_decrease_over_na"], d / na)
                    cell["stored_worst"] = max(cell["stored_worst"], s["best_value"])
                    cell["exact_worst"] = max(cell["exact_worst"], Re.lcost)
            if cell["stored_worst"] > -math.inf:
                report["cells"].append(cell)
        print(job, json.dumps(out), flush=True)
    cells = [c for c in report["cells"] if c["job"] == "cost"]
    if cells:
        d = [(c["exact_worst"] - c["stored_worst"]) / c["na"] for c in cells]
        report["cost_cells"] = dict(cells=len(cells), changed=int(sum(abs(x) > 1e-9 for x in d)), max_increase_over_na=float(max(d)), max_decrease_over_na=float(min(d)))
        print("cells of the cost job: the worst stored instance under the exact rule:", json.dumps(report["cost_cells"]), flush=True)
    report["seconds"] = time.time() - t0
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
