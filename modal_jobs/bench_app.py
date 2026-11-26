"""Modal app of the benchmark campaigns (docs/engineering/benchmarks/): bounded, ephemeral, resumable.

    modal run modal_jobs/bench_app.py::main --driver nested_bench --job smoke --ledger M-0xx

A *driver* is a module under ``experiments/eng/`` (whitelisted in ``DRIVERS``) that exposes

    tasks(job) -> list of task dicts, each with a unique string ``"id"`` and, optionally, ``"tier"``
    run_task(task) -> JSON-serialisable dict

Every task runs on one core in its own container; nothing is deployed; no retries.  Results are appended as they
arrive to ``<driver directory>/results/<prefix>_<job>.jsonl`` with the task id, the commit of the code that ran and
the ledger number, so an interrupted job loses nothing that finished and a re-run skips what is stored.

Tiers bound a task's run time (and with the container cap the job's worst-case cost, which the entry point prints
before it starts anything and which must be in docs/engineering/COMPUTE_LEDGER.md *before* the launch):

    tier "s": 20 minutes, 1 GiB      tier "m": 1 hour, 2 GiB      tier "l": 3 hours, 2 GiB      tier "xl": 6 hours, 4 GiB
    tier "xxl": 12 hours, 4 GiB
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
MAX_CONTAINERS = 50      # half of the workspace limit of 100 concurrent containers (COMPUTE_LEDGER, policy rule 5)
CPU_USD_PER_HOUR = 0.0473
GIB_USD_PER_HOUR = 0.0080
TIERS = {"s": (1200, 1024), "m": (3600, 2048), "l": (10800, 2048), "xl": (21600, 4096), "xxl": (43200, 4096)}      # (timeout s, memory MiB)

# driver name -> (directory under experiments/eng, module, result prefix, packages of src/metricchain_eng it imports)
DRIVERS = {"nested_bench": ("twolevel", "nested_bench", "x011", ("twolevel",))}
PACKAGES = sorted({p for d in DRIVERS.values() for p in d[3]})
EXPERIMENT_DIRS = sorted({d[0] for d in DRIVERS.values()})

app = modal.App("metricchain-eng-bench")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("gcc", "libc6-dev")
    .pip_install("numpy==2.5.5", "scipy==1.18.1")
    .env({"METRICCHAIN_ENG_BUILD": "/tmp/metricchain_build"})
    .add_local_file(ROOT / "src" / "metricchain_eng" / "__init__.py", "/root/src/metricchain_eng/__init__.py")
)
for _p in PACKAGES:           # only the packages the whitelisted drivers import: what runs is what the provenance check covers
    image = image.add_local_dir(ROOT / "src" / "metricchain_eng" / _p, f"/root/src/metricchain_eng/{_p}", ignore=["**/__pycache__/**", "**/*.so"])
for _d in EXPERIMENT_DIRS:
    image = image.add_local_dir(ROOT / "experiments" / "eng" / _d, f"/root/experiments/eng/{_d}",
                                ignore=["**/__pycache__/**", "results/**", "**/*.jsonl", "**/*.log"])


def _run(driver: str, task: dict) -> dict:
    import importlib
    import time

    sub, module, _, _ = DRIVERS[driver]
    sys.path.insert(0, "/root/src")
    sys.path.insert(0, f"/root/experiments/eng/{sub}")
    t0 = time.time()
    out = importlib.import_module(module).run_task(task)
    out["task_id"] = task["id"]
    out["task_seconds"] = time.time() - t0
    return out


@app.function(image=image, cpu=1.0, memory=TIERS["s"][1], timeout=TIERS["s"][0], max_containers=MAX_CONTAINERS, retries=0)
def task_s(driver: str, task: dict) -> dict:
    return _run(driver, task)


@app.function(image=image, cpu=1.0, memory=TIERS["m"][1], timeout=TIERS["m"][0], max_containers=MAX_CONTAINERS, retries=0)
def task_m(driver: str, task: dict) -> dict:
    return _run(driver, task)


@app.function(image=image, cpu=1.0, memory=TIERS["l"][1], timeout=TIERS["l"][0], max_containers=MAX_CONTAINERS, retries=0)
def task_l(driver: str, task: dict) -> dict:
    return _run(driver, task)


@app.function(image=image, cpu=1.0, memory=TIERS["xl"][1], timeout=TIERS["xl"][0], max_containers=MAX_CONTAINERS, retries=0)
def task_xl(driver: str, task: dict) -> dict:
    return _run(driver, task)


@app.function(image=image, cpu=1.0, memory=TIERS["xxl"][1], timeout=TIERS["xxl"][0], max_containers=MAX_CONTAINERS, retries=0)
def task_xxl(driver: str, task: dict) -> dict:
    return _run(driver, task)


def tier_cost(tier: str) -> float:
    """Worst-case cost of one task of a tier in dollars (it runs to its timeout)."""
    timeout, mem = TIERS[tier]
    return timeout / 3600.0 * (CPU_USD_PER_HOUR + mem / 1024.0 * GIB_USD_PER_HOUR)


@app.local_entrypoint()
def main(driver: str = "nested_bench", job: str = "smoke", ledger: str = "", dry: bool = False, max_usd: float = 60.0):
    """``--dry`` prints the task list and the worst-case cost and starts nothing.  ``--max-usd`` refuses to start a job
    whose worst case exceeds it (default: the first-stage limit of the ledger's policy rule 3)."""
    import importlib
    import subprocess

    sub, module, prefix, packages = DRIVERS[driver]
    sys.path.insert(0, str(ROOT / "src"))
    sys.path.insert(0, str(ROOT / "experiments" / "eng" / sub))
    mod = importlib.import_module(module)
    todo = mod.tasks(job)
    ids = [t["id"] for t in todo]
    assert len(set(ids)) == len(ids), "task ids must be unique"
    out = ROOT / "experiments" / "eng" / sub / "results" / f"{prefix}_{job}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            done.add(json.loads(line).get("task_id"))
    todo = [t for t in todo if t["id"] not in done]
    worst = sum(tier_cost(t.get("tier", "m")) for t in todo)
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    # the code that runs: the driver's packages, its experiment directory (result files excluded: the job appends to them), this file
    paths = [f"src/metricchain_eng/{p}" for p in packages] + ["src/metricchain_eng/__init__.py", f"experiments/eng/{sub}",
                                                              f":(exclude)experiments/eng/{sub}/results", "modal_jobs/bench_app.py"]
    dirty = bool(subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *paths], capture_output=True, text=True).stdout.strip())
    by_tier = {k: sum(1 for t in todo if t.get("tier", "m") == k) for k in TIERS}
    print(f"job {driver}/{job} at {commit[:7]}{' (TREE DIFFERS FROM THE COMMIT)' if dirty else ''}: {len(todo)} tasks to run "
          f"({len(done)} already stored), by tier {by_tier}; worst case (every task to its timeout) ${worst:.2f}", flush=True)
    if dry or not todo:
        return
    if dirty:
        raise SystemExit("refusing to launch from a tree that differs from its commit: rows would store a commit that lacks their code")
    if worst > max_usd:
        raise SystemExit(f"worst case ${worst:.2f} exceeds --max-usd {max_usd:.2f}")
    if not ledger:
        raise SystemExit("--ledger M-0xx is required: the job must be entered in COMPUTE_LEDGER.md before launch")
    fns = {"s": task_s, "m": task_m, "l": task_l, "xl": task_xl, "xxl": task_xxl}
    n_done = 0
    with out.open("a") as fh:
        for tier in ("xxl", "xl", "l", "m", "s"):             # longest first
            batch = [t for t in todo if t.get("tier", "m") == tier]
            if not batch:
                continue
            for r in fns[tier].starmap([(driver, t) for t in batch], order_outputs=False, return_exceptions=True):
                n_done += 1
                if isinstance(r, Exception):
                    print(f"[{n_done}/{len(todo)}] FAILED: {type(r).__name__}: {str(r)[:300]}", flush=True)
                    continue
                r.update(commit=commit, job=ledger)
                fh.write(json.dumps(r) + "\n")
                fh.flush()
                print(f"[{n_done}/{len(todo)}] {r['task_id']} ({r['task_seconds']:.0f} s)", flush=True)
