"""Modal app of the benchmark campaigns (docs/engineering/benchmarks/): bounded, ephemeral, resumable.

    modal run modal_jobs/bench_app.py::main --driver nested_bench --job smoke --ledger M-0xx

A *driver* is a module under ``experiments/eng/`` (whitelisted in ``DRIVERS``) that exposes

    tasks(job) -> list of task dicts, each with a unique string ``"id"`` and, optionally, ``"tier"``
    run_task(task) -> JSON-serialisable dict

Every task runs on one core in its own container; nothing is deployed; no retries; at most 50 containers per run
(``CAPS``).  Results are appended as they
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
# Container caps per tier; their sum is 50, half of the workspace limit of 100 concurrent containers (COMPUTE_LEDGER,
# policy rule 5).  All tiers of a run are in flight together, so the sum is what bounds a run.
CAPS = {"s": 8, "m": 18, "l": 14, "xl": 4, "xxl": 6}
CPU_USD_PER_HOUR = 0.0473
GIB_USD_PER_HOUR = 0.0080
TIERS = {"s": (1200, 1024), "m": (3600, 2048), "l": (10800, 2048), "xl": (21600, 4096), "xxl": (43200, 4096)}      # (timeout s, memory MiB)

# driver name -> (directory under experiments/eng, module, result prefix, packages of src/metricchain_eng it imports)
DRIVERS = {"nested_bench": ("twolevel", "nested_bench", "x011", ("twolevel",)),
           "hetero_bench": ("twolevel", "hetero_bench", "x014", ("twolevel",)),
           "nested_literal": ("twolevel", "nested_literal", "x011f", ("twolevel",)),
           "r18_products": ("twolevel", "r18_products", "x005c", ("twolevel",))}
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


STORE = "metricchain-eng-bench-results"      # a modal.Dict: results of detached runs wait here until they are collected


def _run(driver: str, task: dict) -> dict:
    import importlib
    import time
    import traceback

    sub, module, _, _ = DRIVERS[driver]
    sys.path.insert(0, "/root/src")
    sys.path.insert(0, f"/root/experiments/eng/{sub}")
    t0 = time.time()
    store = task.get("_store")
    try:
        out = importlib.import_module(module).run_task({k: v for k, v in task.items() if not k.startswith("_")})
    except Exception as exc:                      # a detached run has nobody to raise to: record the failure
        if not store:
            raise
        out = dict(error=f"{type(exc).__name__}: {exc}", traceback=traceback.format_exc()[-2000:])
    out["task_id"] = task["id"]
    out["task_seconds"] = time.time() - t0
    if store:
        out.update(task.get("_meta", {}))
        modal.Dict.from_name(store, create_if_missing=True)[f"{task['_job']}|{task['id']}"] = out
    return out


@app.function(image=image, cpu=1.0, memory=TIERS["s"][1], timeout=TIERS["s"][0], max_containers=CAPS["s"], retries=0)
def task_s(driver: str, task: dict) -> dict:
    return _run(driver, task)


@app.function(image=image, cpu=1.0, memory=TIERS["m"][1], timeout=TIERS["m"][0], max_containers=CAPS["m"], retries=0)
def task_m(driver: str, task: dict) -> dict:
    return _run(driver, task)


@app.function(image=image, cpu=1.0, memory=TIERS["l"][1], timeout=TIERS["l"][0], max_containers=CAPS["l"], retries=0)
def task_l(driver: str, task: dict) -> dict:
    return _run(driver, task)


@app.function(image=image, cpu=1.0, memory=TIERS["xl"][1], timeout=TIERS["xl"][0], max_containers=CAPS["xl"], retries=0)
def task_xl(driver: str, task: dict) -> dict:
    return _run(driver, task)


@app.function(image=image, cpu=1.0, memory=TIERS["xxl"][1], timeout=TIERS["xxl"][0], max_containers=CAPS["xxl"], retries=0)
def task_xxl(driver: str, task: dict) -> dict:
    return _run(driver, task)


def tier_cost(tier: str) -> float:
    """Planning figure for the cost of one task of a tier in dollars: it runs to its timeout, and for the tiers of an
    hour or more it does so twice -- the platform pre-empts and restarts long tasks, and a job has cost more than
    one attempt per task (job M-022: $2.48 against $2.28; COMPUTE_LEDGER.md, policy rule 6).  Not a proof of a bound:
    a task can be restarted more than once."""
    timeout, mem = TIERS[tier]
    attempts = 2 if timeout >= 3600 else 1
    return attempts * timeout / 3600.0 * (CPU_USD_PER_HOUR + mem / 1024.0 * GIB_USD_PER_HOUR)


def _plan(driver: str, job: str, ledger: str):
    """Task lists of ``job`` (``a+b``: several lists), minus what is already stored locally; provenance of the tree."""
    import importlib
    import subprocess

    sub, module, prefix, packages = DRIVERS[driver]
    sys.path.insert(0, str(ROOT / "src"))
    sys.path.insert(0, str(ROOT / "experiments" / "eng" / sub))
    mod = importlib.import_module(module)
    jobs = job.split("+")
    ledgers = ledger.split("+") if ledger else []
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    # the code that runs: the driver's packages, its experiment directory (result files excluded: the job appends to them), this file
    paths = [f"src/metricchain_eng/{p}" for p in packages] + ["src/metricchain_eng/__init__.py", f"experiments/eng/{sub}",
                                                              f":(exclude)experiments/eng/{sub}/results", "modal_jobs/bench_app.py"]
    dirty = bool(subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *paths], capture_output=True, text=True).stdout.strip())
    todo, total_worst = [], 0.0            # (task, job name, output path, ledger number)
    for k, jb in enumerate(jobs):
        tasks = mod.tasks(jb)
        ids = [t["id"] for t in tasks]
        assert len(set(ids)) == len(ids), "task ids must be unique"
        out = result_path(driver, jb)
        out.parent.mkdir(parents=True, exist_ok=True)
        done = stored_ids(out)
        rest = [t for t in tasks if t["id"] not in done]
        worst = sum(tier_cost(t.get("tier", "m")) for t in rest)
        total_worst += worst
        by_tier = {name: sum(1 for t in rest if t.get("tier", "m") == name) for name in TIERS}
        print(f"job {driver}/{jb} at {commit[:7]}{' (TREE DIFFERS FROM THE COMMIT)' if dirty else ''}: {len(rest)} tasks to run "
              f"({len(done)} already stored), by tier {by_tier}; worst case (every task to its timeout, twice for tiers of an hour or more) ${worst:.2f}", flush=True)
        todo += [(t, jb, out, ledgers[k] if k < len(ledgers) else "") for t in rest]
    print(f"total worst case ${total_worst:.2f}; container caps by tier {CAPS} (sum {sum(CAPS.values())})", flush=True)
    return todo, total_worst, commit, dirty, jobs, ledgers


def result_path(driver: str, job: str) -> Path:
    sub, _, prefix, _ = DRIVERS[driver]
    return ROOT / "experiments" / "eng" / sub / "results" / f"{prefix}_{job}.jsonl"


def stored_ids(path: Path) -> set:
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            done.add(json.loads(line).get("task_id"))
    return done


def _refuse(todo, total_worst, dirty, jobs, ledgers, max_usd):
    if dirty:
        raise SystemExit("refusing to launch from a tree that differs from its commit: rows would store a commit that lacks their code")
    if total_worst > max_usd:
        raise SystemExit(f"worst case ${total_worst:.2f} exceeds --max-usd {max_usd:.2f}")
    if len(ledgers) != len(jobs):
        raise SystemExit("--ledger needs one number per job (M-0xx+M-0yy): every job must be in COMPUTE_LEDGER.md before launch")


@app.local_entrypoint()
def launch(driver: str = "nested_bench", job: str = "smoke", ledger: str = "", dry: bool = False, max_usd: float = 60.0, tiers: str = ""):
    """Detached mode, for jobs that outlive a session:

        modal run --detach modal_jobs/bench_app.py::launch --driver D --job a+b --ledger M-0xx+M-0yy
        python modal_jobs/bench_collect.py --driver D --job a+b            # any time later; appends finished rows

    Every task writes its result (or its failure) into the modal.Dict ``STORE``; the app ends by itself when the
    last task ends or reaches its timeout.  Tasks whose result is already in the Dict or in the local file are not
    started again.  ``--tiers m+l`` submits only the tasks of those tiers (to stay under the container cap while
    another job runs); the rest is submitted by a later call with the other tiers — never repeat a tier whose tasks
    may still be running, they would be started twice."""
    todo, total_worst, commit, dirty, jobs, ledgers = _plan(driver, job, ledger)
    if tiers:
        keep = set(tiers.split("+"))
        todo = [x for x in todo if x[0].get("tier", "m") in keep]
        total_worst = sum(tier_cost(x[0].get("tier", "m")) for x in todo)
        print(f"restricted to tiers {sorted(keep)}: {len(todo)} tasks, worst case ${total_worst:.2f}", flush=True)
    if dry or not todo:
        return
    _refuse(todo, total_worst, dirty, jobs, ledgers, max_usd)
    store = modal.Dict.from_name(STORE, create_if_missing=True)
    have = set(store.keys())
    fns = {"s": task_s, "m": task_m, "l": task_l, "xl": task_xl, "xxl": task_xxl}
    n = 0
    for tier in TIERS:
        batch = []
        for t, jb, _, led in todo:
            if t.get("tier", "m") != tier or f"{jb}|{t['id']}" in have:
                continue
            batch.append(dict(t, _store=STORE, _job=jb, _meta=dict(commit=commit, job=led)))
        if batch:
            fns[tier].spawn_map([driver] * len(batch), batch)
            n += len(batch)
            print(f"tier {tier}: {len(batch)} tasks submitted", flush=True)
    print(f"{n} tasks submitted at {commit[:7]}; collect with: python modal_jobs/bench_collect.py --driver {driver} --job {job}", flush=True)


@app.local_entrypoint()
async def main(driver: str = "nested_bench", job: str = "smoke", ledger: str = "", dry: bool = False, max_usd: float = 60.0):
    """Attached mode, for short jobs: results stream back and are appended to the result files; the app stops when
    this process ends.  ``--job a+b`` runs several job lists of one driver in one app (so that the container caps hold
    for their sum); ``--ledger`` then takes one number per job.  ``--dry`` prints the plan and starts nothing."""
    import asyncio

    todo, total_worst, commit, dirty, jobs, ledgers = _plan(driver, job, ledger)
    if dry or not todo:
        return
    _refuse(todo, total_worst, dirty, jobs, ledgers, max_usd)
    fns = {"s": task_s, "m": task_m, "l": task_l, "xl": task_xl, "xxl": task_xxl}
    n_done = 0
    lock = asyncio.Lock()

    async def run_tier(tier: str):
        nonlocal n_done
        batch = [x for x in todo if x[0].get("tier", "m") == tier]
        if not batch:
            return
        meta = {x[0]["id"]: x for x in batch}
        async for r in fns[tier].starmap.aio([(driver, x[0]) for x in batch], order_outputs=False, return_exceptions=True):
            async with lock:
                n_done += 1
                if isinstance(r, Exception):
                    print(f"[{n_done}/{len(todo)}] FAILED (tier {tier}): {type(r).__name__}: {str(r)[:300]}", flush=True)
                    continue
                _, _, out, led = meta[r["task_id"]]
                r.update(commit=commit, job=led)
                with out.open("a") as fh:
                    fh.write(json.dumps(r) + "\n")
                print(f"[{n_done}/{len(todo)}] {r['task_id']} ({r['task_seconds']:.0f} s)", flush=True)

    await asyncio.gather(*(run_tier(tier) for tier in TIERS))
