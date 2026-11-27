"""Integrity check of the rows of jobs M-016 (``certified1``) and M-021 (``certified2``) after their collection.

    python experiments/eng/twolevel/check_late_rows.py                # structure only (seconds)
    python experiments/eng/twolevel/check_late_rows.py --recompute    # also recomputes the first two nested levels of every row (minutes, local)

Written for the collection of 2026-11-27 (the research owner's directive D-10: "Validate the completeness and
integrity of the retrieved artifacts").  It evaluates nothing new: it reads the stored rows and calls the function
that produced them.

Structure, per job: every row belongs to a task of the job, once; its parameters and its ledger number are those of
the task; the commit it names is in the history of the checkout; the nested levels are numbered 1, 2, ...; only the last level of a row
can be unfinished; a row with fewer levels than were asked for ends unfinished; the best bound found does not
increase with the number of levels; the two design families agree at a size on everything that does not depend on
the family (lower bound, base bracket, constants).  Tasks without a row are listed.

Recomputation: ``nested_bench.certified_cell(u, n, family, max_levels=2)`` with the code of the checkout must return
the stored lower bound, base bracket and constants, and the stored bounds with one and two nested levels at each of
the 18 outer fractions.  (``src/metricchain_eng/twolevel/certified.py`` is unchanged since the commits that ran the
jobs.)  The deeper levels took minutes to twelve hours each and are **not** recomputed; a level that ran into its
time limit holds the best bound found within that time on that machine and is not reproducible to the digit.

Exit status 1 if a stored row has a problem or differs (a task without a row is reported, not counted).
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULTS = HERE / "results"
sys.path.insert(0, str(HERE))

import nested_bench  # noqa: E402

JOBS = (("certified1", "M-016"), ("certified2", "M-021"))
SHARED = ("a", "h_over_a", "x_out", "lower_bound", "base_bracket", "enumeration")
TOL = 1e-9


def load(job: str) -> list[dict]:
    p = RESULTS / f"x011_{job}.jsonl"
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def in_history(commit: str):
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", commit, "HEAD"], capture_output=True)
    except OSError:
        return None
    return True if r.returncode == 0 else False if r.returncode == 1 else None      # None: not a git checkout


def structure(job: str, ledger: str) -> tuple[int, list[dict], int]:
    bad = 0
    tasks = {t["id"]: t for t in nested_bench.tasks(job)}
    rows = load(job)
    seen = {}
    for r in rows:
        tid = r.get("task_id")
        problems = []
        if tid not in tasks:
            problems.append("not a task of the job")
        else:
            kw = tasks[tid]["kwargs"]
            if (r["u"], r["n"], r["family"]) != (kw["u"], kw["n"], kw["family"]):
                problems.append("parameters differ from the task's")
            if r.get("job") != ledger:                       # a row carries the ledger number of its job
                problems.append(f"job field {r.get('job')!r}")
            levels = [x["nested_levels"] for x in r["rows"]]
            if levels != list(range(1, len(levels) + 1)):
                problems.append(f"levels numbered {levels}")
            if any(not x["complete"] for x in r["rows"][:-1]):
                problems.append("an unfinished level before the last")
            if len(levels) < kw["max_levels"] and r["rows"][-1]["complete"]:
                problems.append("fewer levels than asked for, and the last one finished")
            if r["seconds"] > kw["time_limit"] + 60:
                problems.append(f"{r['seconds']:.0f} s against a limit of {kw['time_limit']} s")
            best = math.inf
            for x in r["rows"]:
                if x["best"] is not None:
                    if x["best"] > best + TOL:
                        problems.append(f"bound increases at {x['nested_levels']} nested levels")
                    best = min(best, x["best"])
        if tid in seen:
            problems.append("task stored twice")
        seen[tid] = r
        anc = in_history(r.get("commit", ""))
        if anc is False:
            problems.append(f"commit {r.get('commit')} not in the history of the checkout")
        if problems:
            bad += 1
            print(f"  PROBLEM {tid}: {'; '.join(problems)}")
    by_size = {}
    for r in seen.values():
        by_size.setdefault((r["u"], r["n"]), []).append(r)
    for key, group in sorted(by_size.items()):
        for f in SHARED:
            vals = {round(g[f], 12) for g in group}
            if len(vals) > 1:
                bad += 1
                print(f"  PROBLEM u={key[0]} n={key[1]}: the families disagree on {f}: {sorted(vals)}")
    missing = [tid for tid in tasks if tid not in seen]
    unfinished = sum(1 for r in seen.values() if not r["rows"][-1]["complete"])
    commits = sorted({r.get("commit", "?")[:7] for r in seen.values()})
    print(f"{job} (job {ledger}): {len(seen)} of {len(tasks)} tasks stored, {len(missing)} missing; "
          f"{unfinished} rows end with an unfinished level (time limit); code commit(s) {', '.join(commits)}; "
          f"{bad} structural problems")
    for tid in missing:
        print(f"  MISSING {tid}")
    return bad, list(seen.values()), len(missing)


def _recompute(args):
    u, n, family = args
    r = nested_bench.certified_cell(u, n, family, 2)
    return (u, n, family), r


def recompute(rows: list[dict], workers: int) -> int:
    bad = 0
    stored = {(r["u"], r["n"], r["family"]): r for r in rows}
    with Pool(workers) as pool:
        for key, new in pool.imap_unordered(_recompute, sorted(stored)):
            old = stored[key]
            diffs = []
            for f in SHARED:
                if abs(old[f] - new[f]) > TOL * max(1.0, abs(old[f])):
                    diffs.append(f"{f}: stored {old[f]!r}, recomputed {new[f]!r}")
            n_cmp = 0
            for k in (0, 1):
                o, w = old["rows"][k], new["rows"][k]
                for phi, ov in o["per_phi"].items():
                    wv = w["per_phi"][phi]
                    n_cmp += 1
                    if (ov is None) != (wv is None) or (ov is not None and abs(ov - wv) > TOL):
                        diffs.append(f"{k + 1} nested level(s), fraction {phi}: stored {ov!r}, recomputed {wv!r}")
                if (o["best"] is None) != (w["best"] is None) or (o["best"] is not None and abs(o["best"] - w["best"]) > TOL) or o["best_phi"] != w["best_phi"]:
                    diffs.append(f"{k + 1} nested level(s), best: stored {o['best']!r} at {o['best_phi']}, recomputed {w['best']!r} at {w['best_phi']}")
            bad += bool(diffs)
            print(f"  u={key[0]:g} n={key[1]} {key[2]}: {n_cmp} bounds at one and two nested levels and {len(SHARED)} constants "
                  f"{'agree' if not diffs else 'DIFFER: ' + '; '.join(diffs[:4])} ({new['seconds']:.0f} s)", flush=True)
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--recompute", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    bad, rows, missing = 0, [], 0
    for job, ledger in JOBS:
        b, r, m = structure(job, ledger)
        bad += b
        rows += r
        missing += m
    if args.recompute:
        print(f"recomputation of the first two nested levels of {len(rows)} rows (tolerance {TOL:g}):", flush=True)
        b = recompute(rows, args.workers)
        bad += b
        print(f"recomputation: {len(rows) - b} of {len(rows)} rows agree")
    print("RESULT:", ("no difference in the stored rows" if not bad else f"{bad} problem(s) in the stored rows") + f"; {missing} task(s) without a row")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
