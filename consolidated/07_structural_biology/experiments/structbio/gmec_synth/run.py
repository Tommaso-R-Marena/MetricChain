#!/usr/bin/env python3
"""Experiment SB-X-002 — certified GMEC on synthetic instances (benchmark SB-BM-2, levels 1–2).

VALIDATION EVIDENCE on synthetic models (no energy function is modelled).  For every cell
`(generator, n, kmax, seed)` and accuracy `eps` the row records: whether a certificate was
produced within the budget (an abstention is an outcome), whether the independent checker
accepted it, agreement of the witness energy with toulbar2 on the identical instance, times,
nodes and certificate size.

    python experiments/structbio/gmec_synth/run.py --quick          # a small grid (about 10 minutes)
    python experiments/structbio/gmec_synth/run.py                  # the grid of SB-BM-2 (hours; one core)
    python experiments/structbio/gmec_synth/run.py --time-limit 120

Rows are appended to `results.jsonl` as they are produced.  Timings are observations [E].
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_sb import mincert  # noqa: E402
from metricchain_sb.baselines.toulbar2 import solve_gmec  # noqa: E402
from metricchain_sb.gmec import CertificationBudgetExceeded, certify_gmec  # noqa: E402
from metricchain_sb.mincheck import check_min_certificate  # noqa: E402
from metricchain_sb.synthetic import random_contact_model, random_pair_model  # noqa: E402


def commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def cells(quick: bool):
    if quick:
        for n, kmax in [(15, 6), (25, 8), (40, 8), (60, 10)]:
            for seed in range(3):
                yield "contact", n, kmax, seed
        for n in (10, 14):
            for seed in range(2):
                yield "dense", n, 4, seed
        return
    for n in (15, 25, 40, 60, 100, 150):
        for kmax in (6, 12, 24):
            for seed in range(10):
                yield "contact", n, kmax, seed
    for n in (10, 15, 20):
        for seed in range(10):
            yield "dense", n, 4, seed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--time-limit", type=float, default=600.0)
    ap.add_argument("--max-nodes", type=int, default=200_000)
    ap.add_argument("--baseline-time-limit", type=float, default=900.0,
                    help="seconds allowed to toulbar2 per instance (the first quick run had no limit and was stopped "
                         "by hand while toulbar2 worked on a 60-site instance)")
    ap.add_argument("--out", default=str(HERE / "results.jsonl"))
    args = ap.parse_args()
    sha = commit()
    with open(args.out, "a") as out:
        for gen, n, kmax, seed in cells(args.quick):
            model = (random_contact_model(seed=seed, n=n, kmax=kmax) if gen == "contact"
                     else random_pair_model(seed, n=n, kmax=kmax, density=1.0, scale_bits=3, kmin=2))
            unit = Fraction(1, 2 ** model.scale_bits)
            try:
                tb = solve_gmec(model, time_limit=int(args.baseline_time_limit))
            except RuntimeError as exc:           # toulbar2 gave no proven optimum within its limit: an outcome, recorded
                out.write(json.dumps({"experiment": "SB-X-002", "kind": "validation-synthetic", "generator": gen, "n": n,
                                      "kmax": kmax, "seed": seed, "commit": sha, "outcome": "baseline-timeout",
                                      "reason": str(exc)}, sort_keys=True) + "\n")
                out.flush()
                continue
            for eps in (Fraction(0), Fraction(1, 1000)):
                row = {"experiment": "SB-X-002", "kind": "validation-synthetic", "generator": gen, "n": n,
                       "kmax": kmax, "seed": seed, "eps": str(eps), "commit": sha, "pairs": len(model.pair),
                       "states_total": sum(model.sizes), "model_sha256": mincert.model_sha256(model),
                       "toulbar2_energy": str(tb.energy_int * unit), "seconds_toulbar2": round(tb.seconds, 4),
                       "toulbar2_nodes": tb.nodes, "time_limit": args.time_limit}
                t0 = time.perf_counter()
                try:
                    cert = certify_gmec(model, eps=eps, max_nodes=args.max_nodes, time_limit=args.time_limit)
                except CertificationBudgetExceeded as exc:
                    row.update(outcome="abstained", reason=str(exc), seconds_produce=round(time.perf_counter() - t0, 2))
                else:
                    t_produce = time.perf_counter() - t0
                    t0 = time.perf_counter()
                    res = check_min_certificate(cert)
                    counts = mincert.count_nodes(cert.root)
                    row.update(outcome="certified" if res.accepted else "REJECTED",
                               seconds_produce=round(t_produce, 2), seconds_check=round(time.perf_counter() - t0, 3),
                               certified_gap=str(res.certified_gap), witness_energy=str(res.witness_energy),
                               agrees_with_toulbar2=(res.witness_energy == tb.energy_int * unit) if eps == 0
                               else (res.lower_bound <= tb.energy_int * unit <= res.witness_energy),
                               bnb_nodes=cert.meta["bnb_nodes"], leaves=counts["leaf"], branches=counts["branch"],
                               prunes=counts["prune"], cert_bytes=len(mincert.dumps(cert, include_model=False)))
                out.write(json.dumps(row, sort_keys=True) + "\n")
                out.flush()
                print(json.dumps({k: row.get(k) for k in ("generator", "n", "kmax", "seed", "eps", "outcome",
                                                           "seconds_produce", "seconds_toulbar2", "bnb_nodes",
                                                           "agrees_with_toulbar2")}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
