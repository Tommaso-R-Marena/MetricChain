#!/usr/bin/env python3
"""EXPLORATORY comparison (assessment class A-EXP, stage "development"; protocol FB-P-01 §pilot).

The structural-biology division's certified minimum-energy producer (`metricchain_sb.gmec`,
pinned commit) against toulbar2 on public FIXED-SEQUENCE side-chain-positioning instances
(the ten `pdb*` instances of the PIC-2011 "ProteinFolding" category as hosted in the EvalGM
repository; the eleven instances of that category with domains above 81 are consistent with
design instances and are excluded as outside the research charter).

What this script measures, per instance and per method, under one wall-clock budget:
  * did the method return a claimed optimum / an accepted certificate / an abstention;
  * the optimum value (the two must agree whenever both claim one);
  * wall time; for the certified route also certificate size and checking time.

What it does NOT measure: anything about proteins.  The instances are integer cost tables
published in 2011; "optimum" means optimum of those tables.  Wall-time ratios compare a
mature C++ solver with a Python prototype written in a few hours and are reported as
engineering observations only.  Nothing was tuned on these instances by us: both methods run
with their defaults.

usage: run_scp_exploratory.py INSTANCE_DIR SB_SRC_DIR OUT_JSONL [--budget SECONDS] [--only NAME ...]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import math
import multiprocessing as mp
import os
import sys
import time
from fractions import Fraction
from pathlib import Path


def read_wcsp(path: Path):
    """Parse a WCSP file (arity <= 2) into (n, sizes, constant, unary, pair) with exact integers.

    unary[i] is a list of ints; pair[(i, j)] (i < j) a list of rows.  Several cost functions on
    one scope are summed.  Returns also the declared upper bound.
    """
    opener = lzma.open if path.suffix == ".xz" else open
    with opener(path, "rt") as fh:
        tokens = fh.read().split()
    pos = 0

    def nxt():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    name, n, maxdom, ncost, ub = nxt(), int(nxt()), int(nxt()), int(nxt()), int(nxt())
    sizes = [int(nxt()) for _ in range(n)]
    unary = [[0] * k for k in sizes]
    pair: dict = {}
    constant = 0
    for _ in range(ncost):
        arity = int(nxt())
        scope = [int(nxt()) for _ in range(arity)]
        default = int(nxt())
        ntuples = int(nxt())
        if arity == 0:
            constant += default
            for _ in range(ntuples):
                constant += int(nxt())
        elif arity == 1:
            (i,) = scope
            tab = [default] * sizes[i]
            for _ in range(ntuples):
                a, c = int(nxt()), int(nxt())
                tab[a] = c
            for a in range(sizes[i]):
                unary[i][a] += tab[a]
        elif arity == 2:
            i, j = scope
            tab = [[default] * sizes[j] for _ in range(sizes[i])]
            for _ in range(ntuples):
                a, b, c = int(nxt()), int(nxt()), int(nxt())
                tab[a][b] = c
            if i > j:
                i, j = j, i
                tab = [list(col) for col in zip(*tab)]
            if (i, j) in pair:
                old = pair[(i, j)]
                tab = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(old, tab)]
            pair[(i, j)] = tab
        else:
            raise ValueError(f"{path.name}: arity {arity} not supported (pairwise instances only)")
    if pos != len(tokens):
        raise ValueError(f"{path.name}: {len(tokens) - pos} trailing tokens")
    return {"name": name, "n": n, "sizes": sizes, "constant": constant, "unary": unary, "pair": pair, "ub": ub}


def _toulbar2_worker(wcsp_plain: str, budget: float, queue):
    import pytoulbar2
    t0 = time.perf_counter()
    try:
        cfn = pytoulbar2.CFN(verbose=-1)
        cfn.Read(wcsp_plain)
        res = cfn.Solve(showSolutions=0, timeLimit=int(budget))
        elapsed = time.perf_counter() - t0
        if res and res[0]:
            queue.put({"status": "optimum_claimed", "cost": int(round(res[1])), "seconds": elapsed,
                       "solution": [int(v) for v in res[0]]})
        else:
            queue.put({"status": "no_solution_within_budget", "seconds": elapsed})
    except Exception as exc:  # noqa: BLE001
        queue.put({"status": f"error: {type(exc).__name__}: {exc}"[:300], "seconds": time.perf_counter() - t0})


def _sb_worker(inst_path: str, sb_src: str, budget: float, queue):
    sys.path.insert(0, sb_src)
    import numpy as np
    from metricchain_sb import gmec, mincert, mincheck
    from metricchain_sb.model import PairModel
    inst = read_wcsp(Path(inst_path))
    model = PairModel(unary=[np.array(u, dtype=np.int64) for u in inst["unary"]],
                      pair={k: np.array(t, dtype=np.int64) for k, t in inst["pair"].items()}, scale_bits=0)
    out = {"model_sha256": mincert.model_sha256(model)}
    t0 = time.perf_counter()
    try:
        cert = gmec.certify_gmec(model, eps=Fraction(0), time_limit=budget, max_nodes=10_000_000)
    except gmec.CertificationBudgetExceeded as exc:
        out.update({"status": "abstained_budget", "seconds": time.perf_counter() - t0, "detail": str(exc)[:200]})
        queue.put(out)
        return
    except Exception as exc:  # noqa: BLE001
        out.update({"status": f"error: {type(exc).__name__}: {exc}"[:300], "seconds": time.perf_counter() - t0})
        queue.put(out)
        return
    t1 = time.perf_counter()
    out.update({"status": "certificate_produced", "seconds": t1 - t0})
    queue.put(dict(out, partial=True))          # the producer's result survives whatever happens next

    def check_and_serialise():
        t_a = time.perf_counter()
        result = mincheck.check_min_certificate(cert)
        t_b = time.perf_counter()
        info = {"accepted": bool(result.accepted), "reason": result.reason, "check_seconds": t_b - t_a,
                "witness_energy": None if result.witness_energy is None else int(result.witness_energy) + inst["constant"],
                "lower_bound": None if result.lower_bound is None else str(result.lower_bound + inst["constant"]),
                "certified_gap": None if result.certified_gap is None else str(result.certified_gap)}
        try:
            info["nodes"] = mincert.count_nodes(cert.root)
            text = mincert.dumps(cert)
            info["certificate_bytes"] = len(text.encode())
            info["certificate_sha256"] = hashlib.sha256(text.encode()).hexdigest()
        except RecursionError:
            info["serialise_error"] = "RecursionError"
        except Exception as exc:  # noqa: BLE001
            info["serialise_error"] = f"{type(exc).__name__}: {exc}"[:200]
        return info

    # (1) exactly as shipped: default interpreter recursion limit
    out["as_shipped"] = check_and_serialise()
    # (2) evaluator-side workaround, recorded as such: the same code in a thread with a large
    #     stack and a raised recursion limit.  This changes no line of the evaluated software.
    if not out["as_shipped"]["accepted"] or "serialise_error" in out["as_shipped"]:
        import threading
        box = {}
        sys.setrecursionlimit(3_000_000)
        threading.stack_size(1 << 30)
        th = threading.Thread(target=lambda: box.update(r=check_and_serialise()))
        th.start()
        th.join()
        out["with_raised_recursion_limit"] = box.get("r", {"accepted": False, "reason": "thread died"})
    best = out.get("with_raised_recursion_limit", out["as_shipped"])
    out["status"] = "certificate_accepted" if out["as_shipped"]["accepted"] else (
        "certificate_accepted_only_with_raised_recursion_limit" if best.get("accepted") else "certificate_rejected")
    out["witness_energy"] = best.get("witness_energy")
    queue.put(out)


def run_with_wall_limit(target, args, wall: float):
    queue = mp.Queue()
    proc = mp.Process(target=target, args=(*args, queue))
    t0 = time.perf_counter()
    proc.start()
    result = None
    while True:
        remaining = wall - (time.perf_counter() - t0)
        if remaining <= 0:
            break
        try:
            msg = queue.get(timeout=min(remaining, 1.0))
        except Exception:  # queue.Empty
            if not proc.is_alive() and queue.empty():
                break
            continue
        result = msg
        if not msg.get("partial"):
            break
    if result is None:
        result = {"status": "killed_at_wall_limit" if proc.is_alive() else "worker_died", "seconds": time.perf_counter() - t0}
    elif result.get("partial"):
        result["after_production"] = "killed_at_wall_limit" if proc.is_alive() else "worker_died"
    proc.join(timeout=5)
    if proc.is_alive():
        proc.kill()
        proc.join()
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("instance_dir")
    ap.add_argument("sb_src")
    ap.add_argument("out_jsonl")
    ap.add_argument("--budget", type=float, default=300.0)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    paths = sorted(Path(args.instance_dir).glob("pdb*.wcsp.xz"))
    if args.only:
        paths = [p for p in paths if p.name.split(".")[0] in args.only]
    tmp = Path(args.out_jsonl).parent / "_plain"
    tmp.mkdir(parents=True, exist_ok=True)
    with open(args.out_jsonl, "a") as out:
        for p in paths:
            inst = read_wcsp(p)
            plain = tmp / p.name[:-3]
            plain.write_bytes(lzma.open(p).read())
            row = {
                "instance": p.name.split(".")[0], "file_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                "n": inst["n"], "max_domain": max(inst["sizes"]), "pairs": len(inst["pair"]),
                "log10_configurations": round(sum(math.log10(k) for k in inst["sizes"]), 1),
                "budget_seconds": args.budget,
            }
            row["toulbar2"] = run_with_wall_limit(_toulbar2_worker, (str(plain), args.budget), args.budget + 60)
            row["toulbar2"].pop("solution", None)
            row["sb_certified"] = run_with_wall_limit(_sb_worker, (str(p), args.sb_src, args.budget), args.budget * 1.5 + 60)
            tb, sb = row["toulbar2"], row["sb_certified"]
            if tb.get("status") == "optimum_claimed" and sb.get("witness_energy") is not None:
                row["optima_agree"] = (tb["cost"] == sb["witness_energy"])
            out.write(json.dumps(row, sort_keys=True) + "\n")
            out.flush()
            print(json.dumps(row, sort_keys=True)[:600], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
