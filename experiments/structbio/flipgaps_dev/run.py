#!/usr/bin/env python3
"""Experiment SB-X-003 — certified per-residue flip gaps on the development set (capability C1b).

DEVELOPMENT EVIDENCE.  For every structure of SB-X-001 and every flexible site `i`, one zero-gap
`min` certificate on the box in which the state `x*_i` of the certified minimiser is removed
from site `i`:

    gap_i = min { E(x) : x_i != x*_i } - E(x*)      (certified; attained by a witness)

The smallest gap is the certified gap to the second-best configuration.  If it exceeds twice
the rounding margin `(n + pairs) * 2**-(scale_bits+1)`, the minimiser of the integer tables is
also the unique minimiser of the float tables they were rounded from.

    python experiments/structbio/flipgaps_dev/run.py            # all development structures
    python experiments/structbio/flipgaps_dev/run.py 1CRN       # a subset
    python experiments/structbio/flipgaps_dev/run.py --check 1CRN   # recompute and compare with the stored rows

Certificates are regenerated on demand and not stored (one per site); every row records the
sha256 of its certificate file as produced.  Numbers are properties of the published integer
tables ([M]); timings are observations ([E]).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import pathlib
import sys
import time
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "structbio" / "gmec_dev"))

import run as dev  # noqa: E402  (SB-X-001: model construction and parameters)
from metricchain_sb import mincert  # noqa: E402
from metricchain_sb.mincheck import check_min_certificate  # noqa: E402
from metricchain_sb.stability import certify_flip_gaps, rounding_margin  # noqa: E402

_STATE = {}


def _init(pdb_id):
    model, _, tmeta = dev.build_model(pdb_id, "v1")        # SB-X-003 is an experiment on model v1 (see SB-X-006 for v2)
    text = dev.cert_path(pdb_id, "v1").read_text()
    cert = mincert.loads(text, model=model)
    _STATE.update(model=model, x_star=cert.witness, sites=tmeta["sites"], pdb_id=pdb_id)


def _one(site):
    model, x_star = _STATE["model"], _STATE["x_star"]
    t0 = time.perf_counter()
    (gap,) = certify_flip_gaps(model, x_star, sites=[site], time_limit=3600)
    seconds = time.perf_counter() - t0
    text = mincert.dumps(gap.certificate, include_model=False)
    res = check_min_certificate(mincert.loads(text, model=model))
    meta = _STATE["sites"][site]
    return {"experiment": "SB-X-003", "split": "development", "pdb_id": _STATE["pdb_id"], "site": site,
            "resname": meta["resname"], "resnum": meta["resnum"], "chain": meta["chain"],
            "n_states": model.sizes[site], "state_in_minimiser": int(x_star[site]),
            "minimiser_state_is_deposited": int(x_star[site]) == 0,
            "best_alternative_state": int(gap.alternative[site]),
            "flip_gap_kcal": str(gap.gap), "flip_gap_float": float(gap.gap),
            "certificate_accepted": bool(res.accepted), "bnb_nodes": gap.certificate.meta["bnb_nodes"],
            "seconds": round(seconds, 2), "cert_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "model_sha256": mincert.model_sha256(model)}


def run_structure(pdb_id: str, processes: int):
    _init(pdb_id)
    model = _STATE["model"]
    sites = [i for i, k in enumerate(model.sizes) if k > 1]
    t0 = time.perf_counter()
    with mp.get_context("fork").Pool(processes) as pool:
        rows = pool.map(_one, sites, chunksize=1)
    wall = time.perf_counter() - t0
    margin = rounding_margin(model)
    second = min(Fraction(r["flip_gap_kcal"]) for r in rows)
    summary = {"experiment": "SB-X-003", "split": "development", "pdb_id": pdb_id, "summary": True,
               "commit": dev.git_commit(), "sites": len(rows), "all_accepted": all(r["certificate_accepted"] for r in rows),
               "second_best_gap_kcal": str(second), "second_best_gap_float": float(second),
               "rounding_margin_kcal": str(margin), "rounding_margin_float": float(margin),
               "minimiser_unique": second > 0, "minimiser_of_float_tables_too": second > 2 * margin,
               "sites_with_gap_below_RT_0.593": sum(1 for r in rows if r["flip_gap_float"] < 0.593),
               "sites_with_gap_below_3RT": sum(1 for r in rows if r["flip_gap_float"] < 3 * 0.593),
               "wall_seconds": round(wall, 1), "processes": processes, "model_sha256": mincert.model_sha256(model)}
    return rows, summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=dev.DEV_SET)
    ap.add_argument("--processes", type=int, default=4)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    path = HERE / "results.jsonl"
    if args.check:
        stored = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        bad = 0
        for pdb_id in args.ids:
            rows, _ = run_structure(pdb_id, args.processes)
            old = {r["site"]: r for r in stored if r.get("pdb_id") == pdb_id and not r.get("summary")}
            for r in rows:
                same = r["site"] in old and old[r["site"]]["flip_gap_kcal"] == r["flip_gap_kcal"] and r["certificate_accepted"]
                bad += 0 if same else 1
            print(f"{pdb_id}: {len(rows)} gaps recomputed, {'all equal to the stored rows' if not bad else 'DIFFERENCES'}")
        return 1 if bad else 0
    with open(path, "a") as out:
        for pdb_id in args.ids:
            rows, summary = run_structure(pdb_id, args.processes)
            for r in rows:
                out.write(json.dumps(r, sort_keys=True) + "\n")
            out.write(json.dumps(summary, sort_keys=True) + "\n")
            out.flush()
            print(json.dumps({k: summary[k] for k in ("pdb_id", "sites", "all_accepted", "second_best_gap_float",
                                                       "rounding_margin_float", "minimiser_of_float_tables_too",
                                                       "sites_with_gap_below_RT_0.593", "sites_with_gap_below_3RT",
                                                       "wall_seconds")}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
