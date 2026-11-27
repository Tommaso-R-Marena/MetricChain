"""Driver of the certificate benchmark (protocol: ``PROTOCOL.txt``; the same as data: ``config.py``).

    python experiments/eng/leafcert_bench/run_bench.py main       # every ladder, producer and baselines
    python experiments/eng/leafcert_bench/run_bench.py compare    # leaf-bound methods and branching rules
    python experiments/eng/leafcert_bench/run_bench.py long       # second pass with the 600 s limit

Options: ``--out DIR`` (default ``results`` next to this file), ``--master STRING`` (seeds; the default is
the test master of ``config.py``), ``--budget MINUTES``, ``--only FAMILY[,FAMILY...]``, ``--levels N`` (main:
only the first N sizes of every ladder), ``--resume`` (keep the cell files that exist), ``--time-limit S``
(to try the driver out with a shorter limit than the protocol's).

Two worker processes, each pinned to one logical CPU and limited to one thread, run one cell at a time.
A cell is written to ``DIR/<phase>/<family>__k<k>__n<n>.json`` when it is finished; ``DIR/<phase>/_run.json``
records the schedule, the cells that the budget rule did not start, and the software versions.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "src"))

import config  # noqa: E402


# ================================================================================================ inside a worker
def _status_kb(field):
    try:
        with open("/proc/self/status") as handle:
            for line in handle:
                if line.startswith(field + ":"):
                    return int(line.split()[1])
    except OSError:
        pass
    return None


def _reset_peak():
    try:
        with open("/proc/self/clear_refs", "w") as handle:
            handle.write("5")
    except OSError:
        pass


def _jsonable(obj):
    if isinstance(obj, dict):
        return {str(key): _jsonable(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(value) for value in obj]
    if hasattr(obj, "item") and not isinstance(obj, (str, bytes)):
        return obj.item()
    return obj


def run_producer(instance, model, options, caps, time_limit, measure=True):
    """One call of the producer with everything measured around it."""
    import hashlib

    from metricchain_eng.leafcert import ckernel as check_c
    from metricchain_eng.leafcert import loader
    from metricchain_eng.leafprod import formats, produce
    _reset_peak()
    before = _status_kb("VmRSS")
    t0 = time.perf_counter()
    res = produce(instance, time_limit=time_limit, partial=False, **options, **caps)
    seconds = time.perf_counter() - t0
    rec = {"status": res.status, "reason": res.reason, "L": res.L, "energy": res.energy, "optimal": res.optimal,
           "best_bound": res.best_bound, "seconds": seconds, "stats": _jsonable(res.stats),
           "rss_before_mb": None if before is None else before / 1024.0}
    peak = _status_kb("VmHWM")
    rec["peak_rss_mb"] = None if peak is None else peak / 1024.0
    if res.status == "certified" and measure:
        cert = res.certificate
        t0 = time.perf_counter()
        text = json.dumps(cert, separators=(",", ":"))
        rec["json_seconds"] = time.perf_counter() - t0
        rec["json_bytes"] = len(text)
        rec["cert_sha256"] = hashlib.sha256(text.encode()).hexdigest()
        del text
        data = loader.encode(loader.validate(cert))
        rec["encoded_bytes"] = len(data)
        times = []
        for _ in range(3):
            t0 = time.perf_counter()
            out = check_c.check_encoded(data)
            times.append(time.perf_counter() - t0)
        rec["c_kernel_seconds"] = min(times)
        rec["c_kernel_accepted"] = bool(out["accepted"])
        rec["formats"] = formats.costs(model, cert)
        rec["checker_counts"] = res.checks["c"]["counts"]
        peak = _status_kb("VmHWM")
        rec["peak_rss_mb_with_measurements"] = None if peak is None else peak / 1024.0
    return rec


def run_search(instance, bound, branching, time_limit, **extra):
    """A search without certificate (``certificate=False``): what the tree would be, and how long it takes."""
    from metricchain_eng.leafprod import produce
    t0 = time.perf_counter()
    res = produce(instance, time_limit=time_limit, certificate=False, bound=bound, branching=branching,
                  order=config.MAIN["order"], seed=config.MAIN["seed"], **extra)
    s = res.stats
    return {"status": "optimal" if res.status == "solved" else "limit", "value": res.L if res.status == "solved" else None,
            "seconds": time.perf_counter() - t0, "upper_bound": res.energy, "best_bound": res.best_bound,
            "stop": s["stop"], "nodes": s["nodes"], "branch_nodes": s["branch_nodes"], "leaf_boxes": s["leaf_boxes"],
            "leaf_certificates": s["leaf_certificates"], "depth": s["depth"], "cert_integers": s["cert_integers"],
            "check_ops": s["check_ops"], "ascents": s["ascents"], "sweeps": s["sweeps"], "lp_calls": s["lp_calls"],
            "lp_seconds": s["lp_seconds"], "lp_failures": s["lp_failures"], "root_value": s["root_value"],
            "root_lp_value": s["root_lp_value"], "lp_rounding_loss_root": s["lp_rounding_loss_root"],
            "ub_updates": s["ub_updates"], "initial_ub": s["initial_ub"], "anomalies": s["anomalies"],
            "shared_by_parent": s["shared_by_parent"], "shared_by_sibling": s["shared_by_sibling"]}


def _instance(task, index):
    from metricchain_eng.leafprod import families
    from metricchain_eng.leafprod.model import Model
    seed = families.seed_of(task["master"], task["family"], task["k"], task["n"], index)
    inst = families.make(task["family"], task["n"], task["k"], seed)
    model = Model(inst)
    import math
    from metricchain_eng.leafprod import formats
    states_log10 = float(sum(math.log10(int(v)) for v in model.k))
    dense_leaf, sparse_leaf = formats.per_leaf_integers(model)
    dense_inst, sparse_inst = formats.instance_integers(model)
    rec = {"index": index, "seed": seed, "digest": families.digest(inst), "sites": model.n, "edges": model.ne,
           "site_states": int(model.S), "alphabets": sorted(set(model.k.tolist())), "log10_states": states_log10,
           "dense_instance_integers": dense_inst, "sparse_instance_integers": sparse_inst,
           "dense_ints_per_leaf": dense_leaf, "sparse_ints_per_leaf": sparse_leaf}
    return inst, model, rec


def _agreement(rec):
    """Every exact value of the record must be the same number; every state found must not lie below it."""
    exact_values, uppers = {}, {}
    prod = rec.get("producer")
    if prod:
        if prod["status"] == "certified":
            exact_values["producer"] = prod["L"]
        if prod["energy"] is not None:
            uppers["producer"] = prod["energy"]
    for name in ("plain", "brute", "dp", "cpsat", "milp"):
        out = rec.get(name)
        if not out:
            continue
        if out["status"] == "optimal":
            exact_values[name] = out["value"]
        elif out.get("value") is not None:
            uppers[name] = out["value"]
        if out.get("upper_bound") is not None:
            uppers[name] = out["upper_bound"]
    values = set(exact_values.values())
    ok = len(values) <= 1
    optimum = values.pop() if len(values) == 1 else None
    if optimum is not None and any(v < optimum for v in uppers.values()):
        ok = False
    return {"consistent": ok, "exact_values": exact_values, "upper_bounds": uppers, "optimum": optimum}


def main_cell(task):
    """One cell of the main pass."""
    import baselines
    from metricchain_eng.leafprod.lpbound import LPBound
    run = task["run"]
    hits = {"plain": 0, "cpsat": 0, "milp": 0}
    records = []
    uncertified = 0
    for index in task["instances"]:
        inst, model, rec = _instance(task, index)
        t_inst = time.perf_counter()
        want_plain = run["plain"]
        if run["producer"]:
            rec["producer"] = run_producer(inst, model, config.MAIN, task["caps"], task["time_limit"])
            if rec["producer"]["status"] != "certified":
                uncertified += 1
                want_plain = want_plain and uncertified <= config.PLAIN_UNCERTIFIED
        if want_plain and hits["plain"] < config.HITS_TO_STOP:
            rec["plain"] = run_search(inst, config.MAIN["bound"], config.MAIN["branching"], task["time_limit"])
            hits["plain"] += rec["plain"]["status"] != "optimal"
        for name in ("cpsat", "milp"):
            if run[name] and index < config.GENERAL_INSTANCES and hits[name] < config.GENERAL_HITS_TO_STOP:
                rec[name] = getattr(baselines, name)(model, task["time_limit"])
                hits[name] += rec[name]["status"] != "optimal"
        rec["dp"] = baselines.dp(model, config.DP_MAX_TABLE)
        rec["brute"] = baselines.brute(model, config.BRUTE_MAX_STATES)
        t0 = time.perf_counter()
        sol = LPBound(model).solve(*model.box(), time_limit=config.ROOT_LP_TIME_LIMIT)
        rec["root_lp"] = {"value": None if sol is None else sol["value"], "seconds": time.perf_counter() - t0}
        rec["agreement"] = _agreement(rec)
        rec["seconds_instance"] = time.perf_counter() - t_inst
        records.append(rec)
    return records, hits


def compare_cell(task):
    """One cell of the comparison pass: the instances of the main pass under other branching rules (all
    instances of a rule cell) and other leaf bounds (the first instances of a bound cell)."""
    records = []
    hits = {}
    cell = (task["family"], task["k"], task["n"])
    rules, bounds = cell in config.COMPARE_RULE_CELLS, cell in config.COMPARE_LP_CELLS
    count = config.INSTANCES if rules else config.COMPARE_LP_INSTANCES
    for index in range(count):
        inst, model, rec = _instance(task, index)
        rec["searches"] = {}
        configs = []
        if rules:
            configs += [(b, r, {}) for b, r in config.COMPARE_RULES] + [("mp", "strong", {"share": False})]
        if bounds and index < config.COMPARE_LP_INSTANCES:
            configs += [(b, r, {}) for b, r in config.COMPARE_BOUNDS if not (rules and (b, r) == ("mp", "strong"))]
        for bound, branching, extra in configs:
            name = f"{bound}/{branching}" + ("/noshare" if extra else "")
            if hits.get(name, 0) >= config.HITS_TO_STOP:
                continue
            out = run_search(inst, bound, branching, task["time_limit"], **extra)
            hits[name] = hits.get(name, 0) + (out["status"] != "optimal")
            rec["searches"][name] = out
        rec["certified"] = {}
        if bounds and index < config.COMPARE_CERTIFIED_INSTANCES:
            for bound, branching in config.COMPARE_CERTIFIED:
                options = dict(config.MAIN, bound=bound, branching=branching)
                rec["certified"][f"{bound}/{branching}"] = run_producer(inst, model, options, task["caps"],
                                                                         task["time_limit"], measure=False)
        values = {out["value"] for out in rec["searches"].values() if out["status"] == "optimal"}
        values |= {out["L"] for out in rec["certified"].values() if out["status"] == "certified"}
        rec["consistent"] = len(values) <= 1
        records.append(rec)
    return records, hits


def long_cell(task):
    """One task of the second pass: one solver, one instance, the long time limit."""
    import baselines
    inst, model, rec = _instance(task, task["index"])
    solver = task["solver"]
    if solver == "producer":
        rec["producer"] = run_producer(inst, model, config.MAIN, task["caps"], task["time_limit"])
    elif solver == "plain":
        rec["plain"] = run_search(inst, config.MAIN["bound"], config.MAIN["branching"], task["time_limit"])
    else:
        rec[solver] = getattr(baselines, solver)(model, task["time_limit"])
    return [rec], {}


def worker(cpu, tasks, results):
    for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[var] = "1"
    try:
        os.sched_setaffinity(0, {cpu})
    except (AttributeError, OSError):
        pass
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_AS, (config.WORKER_ADDRESS_SPACE, config.WORKER_ADDRESS_SPACE))
    except (ImportError, ValueError, OSError):
        pass
    functions = {"main": main_cell, "compare": compare_cell, "long": long_cell}
    while True:
        task = tasks.get()
        if task is None:
            return
        t0 = time.perf_counter()
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        try:
            records, hits = functions[task["phase"]](task)
            out = {"task": task, "started_utc": started, "seconds": time.perf_counter() - t0, "cpu": cpu,
                   "instances": records, "limit_hits": hits, "error": None}
        except Exception as exc:                        # a failed cell is a result, not a missing file
            import traceback
            frames = [f"{Path(f.filename).name}:{f.lineno} in {f.name}" for f in traceback.extract_tb(exc.__traceback__)]
            out = {"task": task, "started_utc": started, "seconds": time.perf_counter() - t0, "cpu": cpu,
                   "instances": [], "limit_hits": {}, "error": f"{type(exc).__name__}: {str(exc)[:300]} | " + " < ".join(frames[-6:])}
        peak = _status_kb("VmHWM")
        out["worker_vm_peak_mb"] = None if _status_kb("VmPeak") is None else _status_kb("VmPeak") / 1024.0
        out["worker_rss_peak_mb"] = None if peak is None else peak / 1024.0
        results.put(out)


# ================================================================================================ the schedule
def versions():
    import platform
    out = {"python": platform.python_version(), "machine": platform.machine(), "system": platform.system()}
    for name in ("numpy", "scipy", "ortools"):
        try:
            out[name] = __import__(name).__version__
        except Exception:
            out[name] = None
    try:
        with open("/proc/cpuinfo") as handle:
            for line in handle:
                if line.startswith("model name"):
                    out["cpu"] = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    out["logical_cpus"] = os.cpu_count()
    try:
        out["load_average"] = list(os.getloadavg())
    except OSError:
        pass
    return out


class Pool:
    def __init__(self, cpus):
        self.ctx = mp.get_context("fork")
        self.results = self.ctx.Queue()
        self.slots = []
        for cpu in cpus:
            tasks = self.ctx.Queue()
            proc = self.ctx.Process(target=worker, args=(cpu, tasks, self.results), daemon=True)
            proc.start()
            self.slots.append({"cpu": cpu, "tasks": tasks, "proc": proc, "busy": None})

    def idle(self):
        return [slot for slot in self.slots if slot["busy"] is None]

    def submit(self, slot, task):
        slot["busy"] = task
        slot["tasks"].put(task)

    def wait(self):
        """The next finished task (blocking).  A worker that died gives an error result for its task."""
        while True:
            try:
                out = self.results.get(timeout=5.0)
            except Exception:
                for slot in self.slots:
                    if slot["busy"] is not None and not slot["proc"].is_alive():
                        task = slot["busy"]
                        tasks = self.ctx.Queue()
                        proc = self.ctx.Process(target=worker, args=(slot["cpu"], tasks, self.results), daemon=True)
                        proc.start()
                        slot.update(tasks=tasks, proc=proc, busy=None)
                        return {"task": task, "seconds": None, "cpu": slot["cpu"], "instances": [], "limit_hits": {},
                                "error": "the worker process died (killed or out of memory)"}
                continue
            for slot in self.slots:
                if slot["busy"] is not None and slot["busy"]["id"] == out["task"]["id"]:
                    slot["busy"] = None
            return out

    def close(self):
        for slot in self.slots:
            slot["tasks"].put(None)
        for slot in self.slots:
            slot["proc"].join(timeout=10)


def summarise_main(out):
    """Counts of a main cell, and which solvers go on to the next size of the ladder."""
    task, recs = out["task"], out["instances"]
    summary = {"instances": len(recs)}
    alive = {}
    prod = [r["producer"] for r in recs if "producer" in r]
    summary["producer_attempted"] = len(prod)
    summary["producer_certified"] = sum(p["status"] == "certified" for p in prod)
    alive["producer"] = bool(prod) and 2 * summary["producer_certified"] >= len(prod)
    for name in ("plain", "cpsat", "milp"):
        got = [r[name] for r in recs if name in r]
        summary[f"{name}_attempted"] = len(got)
        summary[f"{name}_solved"] = sum(g["status"] == "optimal" for g in got)
        hits = out["limit_hits"].get(name, 0)
        if name == "plain":
            alive[name] = bool(got) and hits < config.HITS_TO_STOP and 2 * summary["plain_solved"] >= len(got)
        else:
            alive[name] = bool(got) and hits < config.GENERAL_HITS_TO_STOP
    summary["inconsistent"] = sum(not r["agreement"]["consistent"] for r in recs)
    if out["error"]:
        alive = {name: False for name in ("producer", "plain", "cpsat", "milp")}
    return summary, alive


def write_cell(folder, out, extra):
    task = out["task"]
    doc = {"protocol_version": config.PROTOCOL_VERSION, "phase": task["phase"], "family": task["family"], "k": task["k"],
           "n": task["n"], "master": task["master"], **extra, **{key: out[key] for key in (
               "started_utc", "seconds", "cpu", "error", "limit_hits", "worker_vm_peak_mb", "worker_rss_peak_mb") if key in out},
           "task": task, "instances": out["instances"]}
    path = folder / (task["file"] + ".json")
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(_jsonable(doc), indent=1, sort_keys=True))
    os.replace(tmp, path)


def schedule_main(args, folder, pool, log):
    """Ladders are climbed level by level: among the ladders whose next cell can start, the one at the lowest
    level goes first (ties: the order of ``config.ladders()``), so that the budget rule cuts the largest sizes."""
    ladders = [lad for lad in config.ladders() if not args.only or lad[0] in args.only]
    state = []
    for family, k, sizes in ladders:
        general = config.general_ladder(family, k)
        state.append({"family": family, "k": k, "sizes": sizes[:args.levels] if args.levels else sizes, "level": 0,
                      "alive": {"producer": True, "plain": True, "cpsat": general, "milp": general}, "running": False,
                      "done": False})
    t_start = time.time()
    deadline = t_start + 60.0 * args.budget
    next_id = 0
    while True:
        for slot in pool.idle():
            ready = sorted((s for s in state if not s["done"] and not s["running"]),
                           key=lambda s: (s["level"], state.index(s)))
            if not ready:
                break
            if time.time() > deadline:
                for s in ready:
                    s["done"] = True
                    log["not_started_budget"].append([s["family"], s["k"], list(s["sizes"][s["level"]:])])
                break
            s = ready[0]
            n = s["sizes"][s["level"]]
            extension = not s["alive"]["producer"]
            count = config.EXTENSION_INSTANCES if extension else config.INSTANCES
            task = {"id": next_id, "phase": "main", "family": s["family"], "k": s["k"], "n": n, "master": args.master,
                    "file": config.cell_name(s["family"], s["k"], n), "instances": list(range(count)),
                    "run": dict(s["alive"]), "extension": extension, "time_limit": config.TIME_LIMIT, "caps": config.CAPS}
            next_id += 1
            path = folder / (task["file"] + ".json")
            if args.resume and path.exists():
                old = json.loads(path.read_text())
                finish_main(s, {"task": old["task"], "instances": old["instances"], "limit_hits": old["limit_hits"],
                                "error": old["error"], "seconds": old.get("seconds")}, folder, log, t_start, write=False)
                continue
            s["running"] = True
            pool.submit(slot, task)
        if not any(s["running"] for s in state):
            if all(s["done"] for s in state):
                break
            continue
        out = pool.wait()
        s = next(x for x in state if x["family"] == out["task"]["family"] and x["k"] == out["task"]["k"])
        s["running"] = False
        finish_main(s, out, folder, log, t_start)


def finish_main(s, out, folder, log, t_start, write=True):
    summary, alive = summarise_main(out)
    task = out["task"]
    if write:
        write_cell(folder, out, {"summary": summary, "alive_after": alive})
    line = (f"[{time.time() - t_start:7.1f}s] {task['file']:28s} "
            f"cert {summary['producer_certified']}/{summary['producer_attempted']} "
            f"plain {summary['plain_solved']}/{summary['plain_attempted']} cpsat {summary['cpsat_solved']}/{summary['cpsat_attempted']} "
            f"milp {summary['milp_solved']}/{summary['milp_attempted']} "
            f"{'EXT ' if task.get('extension') else ''}{'ERROR ' if out['error'] else ''}"
            f"{'INCONSISTENT ' if summary['inconsistent'] else ''}{(out.get('seconds') or 0):6.1f}s")
    print(line, flush=True)
    log["cells"].append({"file": task["file"], "summary": summary, "alive_after": alive, "seconds": out.get("seconds"),
                         "extension": task.get("extension", False), "error": bool(out["error"]),
                         "finished_after_seconds": time.time() - t_start})
    s["alive"] = alive
    s["level"] += 1
    if s["level"] >= len(s["sizes"]) or not (alive["producer"] or alive["plain"]):
        s["done"] = True
        if s["level"] < len(s["sizes"]):
            log["stopped_by_rule"].append([s["family"], s["k"], list(s["sizes"][s["level"]:])])


def run_tasks(args, folder, pool, log, tasks, describe):
    """A fixed list of independent tasks, in order, while the budget lasts."""
    t_start = time.time()
    deadline = t_start + 60.0 * args.budget
    todo = list(tasks)
    running = 0
    while todo or running:
        for slot in pool.idle():
            if not todo:
                break
            if time.time() > deadline:
                log["not_started_budget"] += [t["file"] for t in todo]
                todo = []
                break
            task = todo.pop(0)
            if args.resume and (folder / (task["file"] + ".json")).exists():
                continue
            pool.submit(slot, task)
            running += 1
        if not running:
            continue
        out = pool.wait()
        running -= 1
        write_cell(folder, out, {})
        print(f"[{time.time() - t_start:7.1f}s] {out['task']['file']:44s} {describe(out)} "
              f"{'ERROR ' if out['error'] else ''}{(out.get('seconds') or 0):6.1f}s", flush=True)
        log["cells"].append({"file": out["task"]["file"], "seconds": out.get("seconds"), "error": bool(out["error"]),
                             "finished_after_seconds": time.time() - t_start})


def compare_tasks(args):
    tasks = []
    for number, (family, k, n) in enumerate(config.COMPARE_CELLS):
        if args.only and family not in args.only:
            continue
        tasks.append({"id": number, "phase": "compare", "family": family, "k": k, "n": n, "master": args.master,
                      "file": config.cell_name(family, k, n), "instances": list(range(config.INSTANCES)),
                      "time_limit": config.TIME_LIMIT, "caps": config.CAPS})
    return tasks


def long_tasks(args, main_folder):
    """The second pass, from the files of the main pass, by the rule of the protocol."""
    def cells(family, k):
        out = []
        for n in config.SIZES[family]:
            path = main_folder / (config.cell_name(family, k, n) + ".json")
            if path.exists():
                out.append(json.loads(path.read_text()))
        return out

    tasks = []

    def add(family, k, doc, solver, indices):
        for index in indices:
            tasks.append({"id": len(tasks), "phase": "long", "family": family, "k": k, "n": doc["n"], "master": args.master,
                          "file": f"{config.cell_name(family, k, doc['n'])}__{solver}__r{index}", "index": index,
                          "solver": solver, "time_limit": config.LONG_TIME_LIMIT, "caps": config.LONG_CAPS})

    def first_failure(family, k, solver):
        """The first cell of the ladder in which ``solver`` missed instances, and those among 0, 1."""
        for doc in cells(family, k):
            missed = []
            for rec in doc["instances"]:
                got = rec.get(solver)
                if got is not None and got["status"] not in ("optimal", "certified"):
                    missed.append(rec["index"])
            if missed:
                return doc, missed[:2]
        return None, []

    for family, k, solver in config.LONG_ORDER:
        if args.only and family not in args.only:
            continue
        doc, missed = first_failure(family, k, solver)
        if doc is not None:
            add(family, k, doc, solver, missed)
    return tasks


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("phase", choices=("main", "compare", "long"))
    parser.add_argument("--out", default=str(HERE / "results"))
    parser.add_argument("--master", default=config.MASTER)
    parser.add_argument("--budget", type=float, default=None, help="minutes of wall time in which cells may start")
    parser.add_argument("--only", default="")
    parser.add_argument("--levels", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--time-limit", type=float, default=None,
                        help="override the time limit of the pass (for trying the driver out; not the protocol)")
    args = parser.parse_args(argv)
    if args.time_limit is not None:
        config.TIME_LIMIT = config.LONG_TIME_LIMIT = args.time_limit
    args.only = set(filter(None, args.only.split(",")))
    if args.budget is None:
        args.budget = config.BUDGET_MIN[args.phase]
    folder = Path(args.out) / args.phase
    folder.mkdir(parents=True, exist_ok=True)
    log = {"protocol_version": config.PROTOCOL_VERSION, "phase": args.phase, "master": args.master,
           "budget_minutes": args.budget, "time_limit_override": args.time_limit, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "versions": versions(), "cpus": list(config.CPUS), "cells": [], "not_started_budget": [],
           "stopped_by_rule": [], "only": sorted(args.only), "levels": args.levels}
    t0 = time.time()
    pool = Pool(config.CPUS)
    try:
        if args.phase == "main":
            schedule_main(args, folder, pool, log)
        elif args.phase == "compare":
            run_tasks(args, folder, pool, log, compare_tasks(args),
                      lambda out: "consistent" if all(r["consistent"] for r in out["instances"]) else "INCONSISTENT")
        else:
            tasks = long_tasks(args, Path(args.out) / "main")
            log["planned"] = [t["file"] for t in tasks]
            run_tasks(args, folder, pool, log, tasks, lambda out: " ".join(
                f"{name}:{rec[name]['status']}" for rec in out["instances"] for name in ("producer", "plain", "cpsat", "milp")
                if name in rec))
    finally:
        pool.close()
    log["wall_seconds"] = time.time() - t0
    try:
        log["load_average_end"] = list(os.getloadavg())
    except OSError:
        pass
    (folder / "_run.json").write_text(json.dumps(log, indent=1, sort_keys=True))
    print(f"{args.phase}: {len(log['cells'])} cells in {log['wall_seconds']:.0f} s; "
          f"{len(log['not_started_budget'])} not started (budget)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
