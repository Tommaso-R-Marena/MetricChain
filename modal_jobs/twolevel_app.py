"""Modal job: adversarial search over instances for Algorithm 2L+ (experiment X-005, THY-REQ-0001 Part B).

Ephemeral app (``modal run`` only; nothing is deployed).  Each task is one call of
``experiments/eng/twolevel/run_search.py::cell`` -- the function the local driver uses -- on one
core.  Results are appended, as they arrive, to
``experiments/eng/twolevel/results/x005_<job>.jsonl`` (one JSON object per line), so an
interrupted run loses nothing that finished.

    modal run modal_jobs/twolevel_app.py --job smoke
    modal run modal_jobs/twolevel_app.py --job cost
    modal run modal_jobs/twolevel_app.py --job claims
    modal run modal_jobs/twolevel_app.py --job converge

Resource bounds: one core and 1 GiB per task, at most ``MAX_CONTAINERS`` containers,
``TIMEOUT_S`` seconds per task, no retries.  The task lists and their expected core-seconds
are in ``run_search.tasks`` / ``run_search.estimated_core_seconds``; the entry point prints
the expected and the worst-case cost before it starts anything.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
MAX_CONTAINERS = 100
TIMEOUT_S = 3600
USD_PER_CORE_HOUR = 0.0473 + 1.0 * 0.0080        # one core + 1 GiB (rates of 2026-11-25, docs/engineering/COMPUTE_LEDGER.md)

app = modal.App("metricchain-eng-twolevel")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("gcc", "libc6-dev")
    .pip_install("numpy==2.5.5", "scipy==1.18.1")
    .env({"METRICCHAIN_ENG_BUILD": "/tmp/metricchain_build"})
    .add_local_dir(ROOT / "src" / "metricchain_eng" / "twolevel", "/root/src/metricchain_eng/twolevel",
                   ignore=["**/__pycache__/**"])
    .add_local_file(ROOT / "src" / "metricchain_eng" / "__init__.py", "/root/src/metricchain_eng/__init__.py")
    .add_local_file(ROOT / "experiments" / "eng" / "twolevel" / "run_search.py", "/root/experiments/eng/twolevel/run_search.py")
)


@app.function(image=image, cpu=1.0, memory=1024, timeout=TIMEOUT_S, max_containers=MAX_CONTAINERS, retries=0)
def search_task(task: dict) -> dict:
    sys.path.insert(0, "/root/src")
    sys.path.insert(0, "/root/experiments/eng/twolevel")
    import run_search

    kw = dict(task)
    kw["objectives"] = tuple(kw["objectives"])
    return run_search.cell(**kw)


@app.local_entrypoint()
def main(job: str = "smoke"):
    sys.path.insert(0, str(ROOT / "src"))
    sys.path.insert(0, str(ROOT / "experiments" / "eng" / "twolevel"))
    import run_search

    todo = run_search.tasks(job)
    out = ROOT / "experiments" / "eng" / "twolevel" / "results" / f"x005_{job}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():                                   # resume: skip tasks whose result is already stored
        for line in out.read_text().splitlines():
            r = json.loads(line)
            done.add((r["u"], r["n"], r["phi"], r["seed"], tuple(s for s in sorted({x["objective"] for x in r["searches"]}))))
    todo = [t for t in todo if (t["u"], t["n"], t["phi"], t["seed"], tuple(sorted(t["objectives"]))) not in done]
    expected = sum(run_search.estimated_core_seconds(t) for t in todo) / 3600.0
    print(f"job {job}: {len(todo)} tasks ({len(done)} already stored); expected {expected:.1f} core-hours = ${expected * USD_PER_CORE_HOUR:.2f}; "
          f"worst case (every task to its timeout) ${len(todo) * TIMEOUT_S / 3600.0 * USD_PER_CORE_HOUR:.2f}", flush=True)
    if not todo:
        return
    todo.sort(key=run_search.estimated_core_seconds, reverse=True)      # longest first
    n_done = 0
    with out.open("a") as fh:
        for r in search_task.map(todo, order_outputs=False):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            n_done += 1
            worst = max((s["best_value"] for s in r["searches"]), default=float("nan"))
            nviol = sum(s["n_violations"] for s in r["searches"])
            print(f"[{n_done}/{len(todo)}] u={r['u']} n={r['n']} phi={r['phi']:.2f} {r['searches'][0]['objective']}: best {worst:.3f}"
                  f"  violations {nviol}  ({r['seconds']:.0f} s)", flush=True)
