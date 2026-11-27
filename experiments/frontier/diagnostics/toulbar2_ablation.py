#!/usr/bin/env python3
"""DIAGNOSTIC (class A-EXP, development instances): which ingredients of the uncertified exact
solver toulbar2 account for its speed on the public fixed-sequence instances?

The certified producer of the structural-biology division differs from toulbar2 in several ways
at once (bound, branching scheme, search order, variable-ordering heuristics, on-the-fly variable
elimination, implementation language).  This script switches toulbar2's ingredients off one at a
time, and all the ones the certified producer lacks together ("producer_like"), and records
search nodes, backtracks and seconds.  It also records toulbar2's lower bound at the root (after
its preprocessing, before any search) with and without virtual arc consistency, to compare with
the root bound of the certified producer (diagnose_gmec.py --mode root).

Two things learnt while writing it, kept here because they change how rows must be read:
  * in depth-first mode toulbar2's reported global dual bound stays at the root value even when
    the search has been completed, so "proved" is read from the solver's own flag `limited`
    (False = the search was completed), not from "dual bound >= cost";
  * with virtual arc consistency switched on (vac=1) the run did not return within the wall
    limit through this Python binding even on the smallest instance; those rows were dropped
    and nothing is concluded about virtual arc consistency.

Every run is a fresh process, because toulbar2's options are process-global.

usage: toulbar2_ablation.py INSTANCE_DIR OUT_JSONL [--budget S] [--only NAME ...] [--configs NAME ...]
"""
from __future__ import annotations

import argparse
import json
import lzma
import multiprocessing as mp
import sys
import tempfile
import time
from pathlib import Path

# option name -> value; "default" changes nothing.  Defaults of pytoulbar2 1.4.0.3 (read from the
# library, see RESULTS): DEE=1, binaryBranching=True, dichotomicBranching=1, elimDegree=3,
# elimDegree_preprocessing=-1, hbfs=1 (hbfsGlobalLimit=32768), lastConflict=True, vac=0,
# weightedDegree=1000000.
CONFIGS = {
    "default": {},
    "no_onthefly_variable_elimination": {"elimDegree": -1},
    "no_dead_end_elimination": {"DEE": 0},
    "depth_first_search": {"hbfs": 0, "hbfsGlobalLimit": 0},
    # toulbar2 refuses n-ary branching together with hybrid best-first search, so the effect of
    # the branching scheme is the difference between this row and "depth_first_search"
    "depth_first_nary_branching": {"binaryBranching": False, "hbfs": 0, "hbfsGlobalLimit": 0},
    "no_last_conflict": {"lastConflict": False},
    "no_weighted_degree": {"weightedDegree": 0},
    # everything the certified producer does not have, switched off together; dead-end
    # elimination stays, because the producer has it
    "producer_like": {"elimDegree": -1, "binaryBranching": False, "hbfs": 0, "hbfsGlobalLimit": 0,
                      "lastConflict": False, "weightedDegree": 0},
    # the same, but keeping binary branching: isolates the branching scheme
    "producer_like_but_binary": {"elimDegree": -1, "hbfs": 0, "hbfsGlobalLimit": 0,
                                 "lastConflict": False, "weightedDegree": 0},
}
ROOT_CONFIGS = {
    "root_default": {},
    "root_no_dee_no_elimination": {"DEE": 0, "elimDegree": -1},
}


def _child(plain_path: str, options: dict, budget: float, root_only: bool, queue):
    import pytoulbar2
    out = {}
    try:
        cfn = pytoulbar2.CFN(verbose=-1)
        for key, value in options.items():
            setattr(cfn.Option, key, value)
        cfn.Read(plain_path)
        t0 = time.perf_counter()
        if root_only:
            cfn.SolveFirst()
            out.update({"seconds": round(time.perf_counter() - t0, 3), "root_lower_bound": float(cfn.GetLB()),
                        "root_upper_bound": float(cfn.GetUB())})
        else:
            res = cfn.Solve(showSolutions=0, timeLimit=int(budget))
            dt = time.perf_counter() - t0
            dual = float(cfn.GetDDualBound())
            cost = float(res[1]) if res else None
            limited = bool(cfn.Option.limited)
            proved = cost is not None and not limited
            out.update({"seconds": round(dt, 3), "cost": cost, "dual_bound": dual, "limited": limited,
                        "status": "optimum_claimed_by_solver" if proved else "time_limit",
                        "nodes": int(cfn.GetNbNodes()), "backtracks": int(cfn.GetNbBacktracks())})
    except Exception as exc:  # recorded, never hidden
        out["error"] = f"{type(exc).__name__}: {exc}"[:300]
    queue.put(out)


def run(plain_path: str, options: dict, budget: float, root_only: bool) -> dict:
    ctx = mp.get_context("spawn")
    queue = ctx.Queue()
    proc = ctx.Process(target=_child, args=(plain_path, options, budget, root_only, queue))
    proc.start()
    try:
        out = queue.get(timeout=budget * 1.5 + 60)
    except Exception:
        out = {"status": "killed_at_wall_limit"}
    proc.join(timeout=5)
    if proc.is_alive():
        proc.kill()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("instance_dir")
    ap.add_argument("out_jsonl")
    ap.add_argument("--budget", type=float, default=60.0)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--configs", nargs="*")
    args = ap.parse_args()
    import pytoulbar2
    version = getattr(pytoulbar2, "__version__", None)
    paths = sorted(Path(args.instance_dir).glob("pdb*.wcsp.xz"), key=lambda p: p.stat().st_size)
    if args.only:
        paths = [p for p in paths if p.name.split(".")[0] in args.only]
    wanted = args.configs or (list(ROOT_CONFIGS) + list(CONFIGS))
    with open(args.out_jsonl, "a") as fh:
        for path in paths:
            name = path.name.split(".")[0]
            with tempfile.NamedTemporaryFile(suffix=".wcsp", delete=False) as tmp:
                tmp.write(lzma.open(path).read())
            for config in wanted:
                root_only = config in ROOT_CONFIGS
                options = ROOT_CONFIGS[config] if root_only else CONFIGS[config]
                row = {"instance": name, "config": config, "options": options, "budget": args.budget,
                       "pytoulbar2": version}
                row.update(run(tmp.name, options, args.budget, root_only))
                fh.write(json.dumps(row, sort_keys=True) + "\n")
                fh.flush()
                print(json.dumps(row, sort_keys=True), flush=True)
            Path(tmp.name).unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
