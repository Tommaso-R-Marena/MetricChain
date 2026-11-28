"""Recompute B3 on F3 with the library as changed after the referee's findings (tau_grad no longer NaN for l = 0;
solve_upper('auto') polishes model-free problems on non-box regions with cutting planes).

The draws are regenerated from the same seeds as the grid (run_validation.one_rep, rng_ref), so the pools are
identical.  The pre-fix B3/F3 rows are moved from results/validation/*.jsonl to
results/superseded/B3_F3_pre_fix.jsonl (kept, marked superseded); the recomputed rows go to
results/validation/F3_B3_recomputed.jsonl.

    python experiments/eng/certinf/rerun_b3_f3.py
"""
from __future__ import annotations

import glob
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_validation as rv  # noqa: E402

VAL = HERE / "results" / "validation"
SUP = HERE / "results" / "superseded"


def job(args):
    tgt, env, rep = args
    rows = rv.one_rep("F3", tgt, env, 1000, rep, methods=["B3"])
    for r in rows:
        r["library"] = "post-fix"
    return rows


def main():
    t0 = time.perf_counter()
    SUP.mkdir(exist_ok=True)
    old = []
    for p in sorted(glob.glob(str(VAL / "F3_*.jsonl"))):
        if p.endswith("F3_B3_recomputed.jsonl"):
            continue
        rows = [json.loads(x) for x in open(p) if x.strip()]
        keep = [r for r in rows if r["method"] != "B3"]
        gone = [r for r in rows if r["method"] == "B3"]
        if gone:
            old += [dict(r, superseded="pre-fix library: tau_grad NaN for l = 0, descent without cutting planes") for r in gone]
            with open(p, "w") as fh:
                fh.write("".join(json.dumps(r) + "\n" for r in keep))
    if old:
        with open(SUP / "B3_F3_pre_fix.jsonl", "a") as fh:
            fh.write("".join(json.dumps(r) + "\n" for r in old))
    cells = sorted({(r["target"], r["env"], r["rep"]) for r in old} |
                   {(json.loads(x)["target"], json.loads(x)["env"], json.loads(x)["rep"]) for x in open(SUP / "B3_F3_pre_fix.jsonl")})
    jobs = [(t, float(e), rep) for t, e, rep in cells]
    out = []
    with Pool(3) as pool:
        for rows in pool.imap_unordered(job, jobs, chunksize=5):
            out += rows
    out.sort(key=lambda r: (r["target"], float(r["env"]), r["rep"]))
    (VAL / "F3_B3_recomputed.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
    (HERE / "results" / "rerun_b3_f3_wall.json").write_text(json.dumps(dict(wall=time.perf_counter() - t0, rows=len(out))))
    print(len(out), "rows", time.perf_counter() - t0)


if __name__ == "__main__":
    main()
