"""X-005 / X-006b against the lowered sample cap of THY-RES-0004 §3.

The theory division proved (unrefereed; reviewed since in SCI-REV-0007 §2) that every sample of
Algorithm 2L+ is ``K`` or has fewer than ``2 max{e^lam M_dagger, M_ddagger}`` points, where the theorem
has ``M_bar = 2 (1 + eta) e^lam nu0 M_dagger``.  They did not run it on the engineering instances.
This script re-evaluates every stored maximiser of X-005 (all objectives, among them the searches
that maximise the sample itself) and the flat instances, and reports the largest sample relative to
``M_dagger``, to the lowered cap and to ``M_bar``.

    python experiments/eng/twolevel/lowered_cap.py --out experiments/eng/twolevel/results/x005_lowered_cap.json
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
from metricchain_eng.twolevel.alg2l import lowered_sample_cap  # noqa: E402
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, Law  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", nargs="*", default=["cost", "claims", "converge"])
    ap.add_argument("--nmax", type=int, default=10 ** 9)
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    t0 = time.time()
    report = dict(jobs={}, by_u={})
    for job in args.jobs:
        path = Path(__file__).resolve().parent / "results" / f"x005_{job}.jsonl"
        if not path.exists():
            continue
        out = report["jobs"][job] = dict(runs=0, samples_above_K=0, above_M_dagger=0, above_lowered_cap=0,
                                          max_l_over_M_dagger=-math.inf, max_l_over_cap=-math.inf, min_l_cap_over_M_dagger=math.inf,
                                          max_l_cap_over_M_dagger=-math.inf, min_l_Mbar_over_cap=math.inf, worst=None)
        for line in path.read_text().splitlines():
            c = json.loads(line)
            if c["n"] > args.nmax:
                continue
            P, _ = run_search.design_params(c["n"], c["u"], c["phi"], c["design"])
            ev = Evaluator(P)
            lcap = lowered_sample_cap(P, ev.outer, ev.C)
            out["min_l_cap_over_M_dagger"] = min(out["min_l_cap_over_M_dagger"], lcap - ev.C.lM_dag)
            out["max_l_cap_over_M_dagger"] = max(out["max_l_cap_over_M_dagger"], lcap - ev.C.lM_dag)
            out["min_l_Mbar_over_cap"] = min(out["min_l_Mbar_over_cap"], ev.C.lM_bar - lcap)
            runs = [(dict(kind="flat", oracle=orc), ev.run(Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=c["u"] * P.n_i), orc))
                    for orc in ("bottom", "top")]
            for s in c["searches"]:
                fam = Family(ev, k=c["k"], monotone=(s["family"] == "monotone"))
                F, d0, c_in = fam.decode(np.array(s["best_x"]))
                runs.append((dict(kind=s["objective"], family=s["family"], oracle=s["oracle"]), ev.run(fam.instance(F, d0, c_in), s["oracle"])))
            bu = report["by_u"].setdefault(str(c["u"]), dict(max_l_over_M_dagger=-math.inf, max_l_over_cap=-math.inf))
            for tag, R in runs:
                out["runs"] += 1
                if R.lM_max <= ev.C.lK + 1e-9:
                    continue
                out["samples_above_K"] += 1
                a, b = R.lM_max - ev.C.lM_dag, R.lM_max - lcap
                out["above_M_dagger"] += a > 1e-9
                out["above_lowered_cap"] += b >= -1e-9                      # the claim is a strict inequality
                bu["max_l_over_M_dagger"] = max(bu["max_l_over_M_dagger"], a)
                bu["max_l_over_cap"] = max(bu["max_l_over_cap"], b)
                if b > out["max_l_over_cap"]:
                    out["max_l_over_cap"] = b
                    out["worst"] = dict(u=c["u"], n=c["n"], phi=c["phi"], **tag, sample_over_M_dagger=math.exp(a), sample_over_cap=math.exp(b),
                                        cap_over_M_dagger=math.exp(lcap - ev.C.lM_dag), r_dag=ev.C.r_dag)
                out["max_l_over_M_dagger"] = max(out["max_l_over_M_dagger"], a)
        print(job, json.dumps(out), flush=True)
    report["seconds"] = time.time() - t0
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
