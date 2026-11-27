#!/usr/bin/env python3
"""DIAGNOSTIC evaluation (class A-EXP, development instances): why does the structural-biology
division's certified minimum-energy producer abstain, and where does its time go?

Nothing here modifies the evaluated software; it is imported from a detached copy of a pinned
commit and some of its internal functions are called to *measure* intermediate quantities.

Three measurements per instance:

  root      after its own dead-end elimination at the root: remaining search space; its dual
            (message-passing) bound after 50 / 300 / 1000 / 3000 sweeps, as a float and after its
            own rounding of the messages to integers ("exact" bound, the one a certificate may
            use); seconds per sweep; all gaps are against the best known value (toulbar2's
            optimum where toulbar2 claimed one), in units of the instance's integer costs.

  eps       the producer run as shipped but asked for a gap just under ONE COST UNIT
            (eps = 4095/4096) instead of zero.  The public instances have integer costs, so a
            lower bound above U - 1 already proves that U is optimal - by a one-line integrality
            argument that is NOT part of the certificate kernel.  If this run certifies quickly
            where the zero-gap run abstains, the abstention is caused by the missing integrality
            step, not by the search.

  oracle    as shipped (zero gap), but handed toulbar2's solution as the witness: does a better
            incumbent remove the abstention?  (written, not run: see RESULTS)

  profile   cProfile of the as-shipped zero-gap run for a fixed time: where the time goes.

  nodes     the as-shipped zero-gap run with a longer budget and two counters wrapped around the
            producer's own functions (calls of its dead-end elimination = search nodes entered;
            calls of its message-passing sweep): how large a search does it need, or - if it
            still abstains - how many nodes did it get through?

usage: diagnose_gmec.py INSTANCE_DIR SB_SRC_DIR PILOT_JSONL OUT_JSON [--mode root|eps|oracle|profile|nodes]
                        [--jobs N] [--budget S] [--only ...]
"""
from __future__ import annotations

import argparse
import cProfile
import io
import json
import multiprocessing as mp
import pstats
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploratory_gmec"))
from run_scp_exploratory import read_wcsp  # noqa: E402


def load(inst_path, sb_src):
    sys.path.insert(0, sb_src)
    import numpy as np
    from metricchain_sb.model import PairModel
    inst = read_wcsp(Path(inst_path))
    model = PairModel(unary=[np.array(u, dtype=np.int64) for u in inst["unary"]],
                      pair={k: np.array(t, dtype=np.int64) for k, t in inst["pair"].items()}, scale_bits=0)
    return inst, model


def root_worker(args):
    inst_path, sb_src, best_known = args
    import math
    import numpy as np
    inst, model = load(inst_path, sb_src)
    from metricchain_sb import gmec
    out = {"instance": Path(inst_path).name.split(".")[0], "n": inst["n"], "best_known": best_known}
    mb = 12
    P = gmec._Problem(model, mb)
    unit = 2 ** mb                                   # fine units per cost unit
    D = [np.arange(k, dtype=np.int64) for k in P.sizes]
    out["log10_space_before"] = round(sum(math.log10(len(d)) for d in D), 1)
    t0 = time.perf_counter()
    prunes = gmec.dead_end_elimination(P, D)
    out["dee_seconds"] = round(time.perf_counter() - t0, 2)
    out["dee_eliminations"] = len(prunes)
    out["log10_space_after_dee"] = round(sum(math.log10(len(d)) for d in D), 1)
    out["sites_still_free"] = int(sum(len(d) > 1 for d in D))
    out["max_domain_after_dee"] = int(max(len(d) for d in D))
    out["edges"] = len(P.edges)
    dual = gmec._Dual(P, D, None)
    done = 0
    traj = []
    t_sweeps = 0.0
    for target_sweeps in (50, 300, 1000, 3000):
        t1 = time.perf_counter()
        for _ in range(target_sweeps - done):
            dual.sweep()
        t_sweeps += time.perf_counter() - t1
        done = target_sweeps
        fb = dual.bound()
        mint = {key: np.rint(vec).astype(np.int64) for key, vec in dual.full_messages().items()}
        eb = gmec._exact_bound(P, D, mint)
        x = gmec.icm(P, D, dual.decode())
        u = P.energy(x)
        const = inst["constant"]
        traj.append({"sweeps": done, "float_bound": round(fb / unit + const, 4), "exact_bound": round(eb / unit + const, 4),
                     "decoded_energy": int(u // unit + const) if u % unit == 0 else u / unit + const,
                     "gap_float_to_best": None if best_known is None else round(best_known - (fb / unit + const), 4),
                     "gap_exact_to_best": None if best_known is None else round(best_known - (eb / unit + const), 4)})
        if t_sweeps > 240:
            break
    out["seconds_per_sweep"] = round(t_sweeps / done, 4)
    out["trajectory"] = traj
    return out


def _eps_child(inst_path, sb_src, eps_num, eps_den, budget, queue, use_oracle=False):
    inst, model = load(inst_path, sb_src)
    from metricchain_sb import gmec, mincheck
    witness = None
    if use_oracle:
        import lzma
        import tempfile
        import pytoulbar2
        with tempfile.NamedTemporaryFile(suffix=".wcsp", delete=False) as fh:
            fh.write(lzma.open(inst_path).read())
        cfn = pytoulbar2.CFN(verbose=-1)
        cfn.Read(fh.name)
        res = cfn.Solve(showSolutions=0, timeLimit=int(budget))
        if res and res[0]:
            witness = [int(v) for v in res[0]]
    t0 = time.perf_counter()
    try:
        cert = gmec.certify_gmec(model, eps=Fraction(eps_num, eps_den), time_limit=budget, max_nodes=10_000_000,
                                 witness=witness)
    except gmec.CertificationBudgetExceeded as exc:
        queue.put({"status": "abstained_budget", "seconds": round(time.perf_counter() - t0, 1)})
        return
    t1 = time.perf_counter()
    res = mincheck.check_min_certificate(cert)
    from metricchain_sb import mincert
    queue.put({"status": "certificate_accepted" if res.accepted else "certificate_rejected",
               "seconds": round(t1 - t0, 1), "check_seconds": round(time.perf_counter() - t1, 2),
               "witness_energy": int(res.witness_energy) + inst["constant"],
               "lower_bound": str(res.lower_bound + inst["constant"]), "certified_gap": str(res.certified_gap),
               "nodes": mincert.count_nodes(cert.root), "bnb_nodes": cert.meta.get("bnb_nodes")})


def eps_worker(args):
    inst_path, sb_src, best_known, budget = args[:4]
    oracle = len(args) > 4 and args[4]
    out = {"instance": Path(inst_path).name.split(".")[0], "best_known": best_known,
           "eps": "0 (witness = toulbar2's solution)" if oracle else "4095/4096", "budget": budget}
    queue = mp.Queue()
    proc = mp.Process(target=_eps_child, args=(inst_path, sb_src, 0 if oracle else 4095, 1 if oracle else 4096, budget, queue, oracle))
    proc.start()
    try:
        out.update(queue.get(timeout=budget * 1.3 + 60))
    except Exception:
        out["status"] = "killed_at_wall_limit"
    proc.join(timeout=5)
    if proc.is_alive():
        proc.kill()
    if out.get("witness_energy") is not None and best_known is not None:
        out["witness_equals_best_known"] = out["witness_energy"] == best_known
    return out


def _nodes_child(inst_path, sb_src, budget, queue):
    inst, model = load(inst_path, sb_src)
    from metricchain_sb import gmec, mincheck, mincert
    count = {"nodes": 0, "sweeps": 0}
    dee, sweep = gmec.dead_end_elimination, gmec._Dual.sweep

    def counted_dee(*a, **k):
        count["nodes"] += 1
        return dee(*a, **k)

    def counted_sweep(self, *a, **k):
        count["sweeps"] += 1
        return sweep(self, *a, **k)

    gmec.dead_end_elimination = counted_dee          # looked up as a module global at call time
    gmec._Dual.sweep = counted_sweep
    t0 = time.perf_counter()
    try:
        cert = gmec.certify_gmec(model, eps=Fraction(0), time_limit=budget, max_nodes=10_000_000)
    except gmec.CertificationBudgetExceeded:
        queue.put({"status": "abstained_budget", "seconds": round(time.perf_counter() - t0, 1),
                   "nodes_entered": count["nodes"], "sweeps": count["sweeps"]})
        return
    t1 = time.perf_counter()
    res = mincheck.check_min_certificate(cert)
    queue.put({"status": "certificate_accepted" if res.accepted else "certificate_rejected",
               "seconds": round(t1 - t0, 1), "check_seconds": round(time.perf_counter() - t1, 2),
               "witness_energy": int(res.witness_energy) + inst["constant"],
               "nodes_entered": count["nodes"], "sweeps": count["sweeps"],
               "certificate_nodes": mincert.count_nodes(cert.root), "bnb_nodes": cert.meta.get("bnb_nodes")})


def nodes_worker(args):
    inst_path, sb_src, best_known, budget = args[:4]
    out = {"instance": Path(inst_path).name.split(".")[0], "best_known": best_known, "budget": budget}
    queue = mp.Queue()
    proc = mp.Process(target=_nodes_child, args=(inst_path, sb_src, budget, queue))
    proc.start()
    try:
        out.update(queue.get(timeout=budget * 1.3 + 120))
    except Exception:
        out["status"] = "killed_at_wall_limit"
    proc.join(timeout=5)
    if proc.is_alive():
        proc.kill()
    if out.get("witness_energy") is not None and best_known is not None:
        out["witness_equals_best_known"] = out["witness_energy"] == best_known
    return out


def profile_worker(args):
    inst_path, sb_src, budget = args
    inst, model = load(inst_path, sb_src)
    from metricchain_sb import gmec
    prof = cProfile.Profile()
    prof.enable()
    status = "finished"
    try:
        gmec.certify_gmec(model, eps=Fraction(0), time_limit=budget, max_nodes=10_000_000)
    except gmec.CertificationBudgetExceeded:
        status = "abstained_budget"
    prof.disable()
    stats = pstats.Stats(prof, stream=io.StringIO())
    total = sum(v[2] for v in stats.stats.values())      # total "tottime"
    rows = sorted(((v[2], v[3], v[0], f"{Path(k[0]).name}:{k[2]}") for k, v in stats.stats.items()), reverse=True)[:12]
    calls = {name: nc for (tt, ct, nc, name) in rows}
    return {"instance": Path(inst_path).name.split(".")[0], "status": status, "budget": budget,
            "top_by_own_time": [{"function": name, "own_seconds": round(tt, 1), "share": round(tt / total, 3),
                                 "calls": nc} for (tt, ct, nc, name) in rows],
            "cumulative": {name: round(ct, 1) for (tt, ct, nc, name) in
                           sorted(((v[2], v[3], v[0], f"{Path(k[0]).name}:{k[2]}") for k, v in stats.stats.items()),
                                  key=lambda r: -r[1])[:10]}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("instance_dir")
    ap.add_argument("sb_src")
    ap.add_argument("pilot_jsonl")
    ap.add_argument("out_json")
    ap.add_argument("--mode", choices=("root", "eps", "oracle", "profile", "nodes"), default="root")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--budget", type=float, default=300.0)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    best = {}
    for line in Path(args.pilot_jsonl).read_text().splitlines():
        r = json.loads(line)
        tb = r["toulbar2"]
        best[r["instance"]] = (tb.get("cost"), tb.get("status") == "optimum_claimed_by_solver")
    paths = sorted(Path(args.instance_dir).glob("pdb*.wcsp.xz"), key=lambda p: p.stat().st_size)
    if args.only:
        paths = [p for p in paths if p.name.split(".")[0] in args.only]
    names = [p.name.split(".")[0] for p in paths]
    if args.mode == "root":
        jobs = [(str(p), args.sb_src, best[n][0]) for p, n in zip(paths, names)]
        worker = root_worker
    elif args.mode in ("eps", "oracle"):
        jobs = [(str(p), args.sb_src, best[n][0], args.budget, args.mode == "oracle") for p, n in zip(paths, names)]
        worker = eps_worker
    elif args.mode == "nodes":
        jobs = [(str(p), args.sb_src, best[n][0], args.budget) for p, n in zip(paths, names)]
        worker = nodes_worker
    else:
        jobs = [(str(p), args.sb_src, args.budget) for p in paths]
        worker = profile_worker
    rows = []
    if args.mode in ("eps", "oracle", "nodes"):
        # each job starts its own (killable) child process, so the scheduler must be threads
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            iterator = pool.map(worker, jobs)
            for row in iterator:
                row["toulbar2_proved"] = best[row["instance"]][1]
                rows.append(row)
                print(json.dumps(row, sort_keys=True)[:900], flush=True)
    else:
        with mp.get_context("spawn").Pool(args.jobs) as pool:
            for row in pool.imap_unordered(worker, jobs):
                row["toulbar2_proved"] = best[row["instance"]][1]
                rows.append(row)
                print(json.dumps(row, sort_keys=True)[:900], flush=True)
    rows.sort(key=lambda r: names.index(r["instance"]))
    json.dump(rows, open(args.out_json, "w"), indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
