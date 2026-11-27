"""X-005: re-evaluate every stored maximiser with the current code.

Job M-008 ("cost") ran at a commit earlier than the one that introduced the exact tie rule
(``meanrun.py``, "Ties"); jobs M-009 and M-010 ran with it.  This script decodes the stored best point of every search, evaluates it again
locally -- with the tie rule and without it -- and reports the largest change of ln(cost) and whether any
claim of Theorem 11.56 is violated under either convention.  It also re-evaluates the flat instance.

    python experiments/eng/twolevel/recheck.py [--jobs cost claims converge] [--nmax 16000]
"""
from __future__ import annotations

import argparse
import json
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
from metricchain_eng.twolevel.meanrun import Instance, Law  # noqa: E402
from metricchain_eng.twolevel.tables import TIE  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", nargs="*", default=["cost", "claims", "converge"])
    ap.add_argument("--nmax", type=int, default=10 ** 9)
    args = ap.parse_args()
    t0 = time.time()
    report = {}
    for job in args.jobs:
        path = Path(__file__).resolve().parent / "results" / f"x005_{job}.jsonl"
        if not path.exists():
            continue
        out = report[job] = dict(searches=0, flat=0, max_abs_change_no_tie=0.0, max_abs_change_tie=0.0, max_rel_change_tie=0.0,
                                 violations_no_tie=0, violations_tie=0, worst=None)
        for line in path.read_text().splitlines():
            c = json.loads(line)
            if c["n"] > args.nmax:
                continue
            P, _ = run_search.design_params(c["n"], c["u"], c["phi"], c["design"])
            evs = {tie: Evaluator(P, tie=tie) for tie in (0.0, TIE)}
            flat = Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=c["u"] * P.n_i)
            na = c["n"] * c["a"]
            for orc in ("bottom", "top"):
                stored = c["flat"][orc]["lcost"]
                for tie, ev in evs.items():
                    R = ev.run(flat, orc)
                    d = abs(R.lcost - stored)
                    key = "max_abs_change_tie" if tie else "max_abs_change_no_tie"
                    out[key] = max(out[key], d)
                    if tie:
                        out["max_rel_change_tie"] = max(out["max_rel_change_tie"], d / na)
                    out["violations_tie" if tie else "violations_no_tie"] += bool(R.violations())
                out["flat"] += 1
            for s in c["searches"]:
                for tie, ev in evs.items():
                    fam = Family(ev, k=c["k"], monotone=(s["family"] == "monotone"))
                    F, d0, c_in = fam.decode(np.array(s["best_x"]))
                    R = ev.run(fam.instance(F, d0, c_in), s["oracle"])
                    val = objective_value(R, s["objective"])
                    d = abs(val - s["best_value"])
                    key = "max_abs_change_tie" if tie else "max_abs_change_no_tie"
                    if d > out[key]:
                        out[key] = d
                        if tie:
                            out["worst"] = dict(u=c["u"], n=c["n"], phi=c["phi"], objective=s["objective"], family=s["family"],
                                                oracle=s["oracle"], stored=s["best_value"], now=val)
                    if tie and s["objective"] == "cost":
                        out["max_rel_change_tie"] = max(out["max_rel_change_tie"], d / na)
                    out["violations_tie" if tie else "violations_no_tie"] += bool(R.violations())
                out["searches"] += 1
    report["seconds"] = time.time() - t0
    print(json.dumps(report, indent=1))
    (Path(__file__).resolve().parent / "results" / "x005_recheck.json").write_text(json.dumps(report, indent=1))
    return 0 if all(v["violations_tie"] == 0 and v["violations_no_tie"] == 0 for v in report.values() if isinstance(v, dict)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
