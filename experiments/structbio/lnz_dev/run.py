#!/usr/bin/env python3
"""Experiment SB-X-004 — certified enclosures of ln Z on the development set (capability C2, first version).

DEVELOPMENT EVIDENCE.  For a structure of SB-X-001 and thresholds `theta` (kcal/mol): thermal
dead-end elimination with margin `TAU`, product-form relaxation of every pair whose non-additive
oscillation is at most `theta`, exact variable elimination of the rest (float tier: binary64 with
outward rounding, assumptions F1-F3 of `metricchain_sb.itables`), at `beta = 1000/593` per kcal/mol
(RT = 0.593 kcal/mol).  An abstention (table budget exceeded) is recorded as an outcome.

    python experiments/structbio/lnz_dev/run.py 1CRN
    python experiments/structbio/lnz_dev/run.py 1CRN --exact-check    # also the exact-rational tier at the coarsest threshold

The interval is the one the checker computes (`zcheck`); rule semantics are [V] for chains and [P]
in general, the checker implementation is tested — label [CP].  Z certificates have no file
format yet: a row records the recipe (counts of steps, order length) and is reproduced by
re-running at the recorded commit.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "structbio" / "gmec_dev"))

import run as dev  # noqa: E402
from metricchain_sb import mincert  # noqa: E402
from metricchain_sb.partition import PartitionBudgetExceeded, certify_partition  # noqa: E402
from metricchain_sb.zcheck import check_partition_certificate  # noqa: E402

BETA = Fraction(1000, 593)
TAU = 12.0
THETAS = (1.0, 0.3, 0.1, 0.03, 0.01)
MAX_ENTRIES = 30_000_000


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=["1CRN"])
    ap.add_argument("--exact-check", action="store_true")
    args = ap.parse_args()
    with open(HERE / "results.jsonl", "a") as out:
        for pdb_id in args.ids:
            model, _, _ = dev.build_model(pdb_id)
            e_star = None
            cert_path = ROOT / "experiments" / "structbio" / "gmec_dev" / "certs" / f"{pdb_id}.mincert.json"
            if cert_path.exists():
                e_star = model.energy(mincert.loads(cert_path.read_text(), model=model).witness)
            runs = [(theta, "float") for theta in THETAS] + ([(THETAS[0], "exact")] if args.exact_check else [])
            for theta, tier in runs:
                row = {"experiment": "SB-X-004", "split": "development", "pdb_id": pdb_id, "commit": dev.git_commit(),
                       "model_sha256": mincert.model_sha256(model), "beta_per_kcal": str(BETA), "tau_kcal": TAU,
                       "theta_kcal": theta, "arithmetic": tier, "max_entries": MAX_ENTRIES}
                t0 = time.perf_counter()
                try:
                    cert = certify_partition(model, BETA, tau=TAU, theta=theta, arithmetic=tier, max_entries=MAX_ENTRIES)
                except PartitionBudgetExceeded as exc:
                    row.update(outcome="abstained", reason=str(exc), seconds=round(time.perf_counter() - t0, 2))
                else:
                    res = check_partition_certificate(cert, arithmetic=tier, max_entries=MAX_ENTRIES)
                    prunes = sum(1 for s in cert.steps if s["op"] == "prune")
                    row.update(outcome="certified" if res.accepted else "REJECTED", full_box=bool(res.full_box),
                               ln_z_lo=str(res.ln_z_lo), ln_z_hi=str(res.ln_z_hi),
                               ln_z_lo_float=float(res.ln_z_lo), ln_z_hi_float=float(res.ln_z_hi),
                               width_nats=float(res.ln_z_hi - res.ln_z_lo),
                               step_slack_nats=float(res.slack_hi - res.slack_lo),
                               prunes=prunes, relaxed_pairs=len(cert.steps) - prunes,
                               exact_pairs=len(model.pair) - (len(cert.steps) - prunes),
                               largest_table=res.stats["largest_table"], seconds=round(time.perf_counter() - t0, 2))
                    if e_star is not None:
                        row["minus_beta_E_min"] = float(-BETA * e_star)
                out.write(json.dumps(row, sort_keys=True) + "\n")
                out.flush()
                print(json.dumps({k: row.get(k) for k in ("pdb_id", "theta_kcal", "arithmetic", "outcome", "ln_z_lo_float",
                                                           "ln_z_hi_float", "width_nats", "exact_pairs", "largest_table",
                                                           "seconds", "reason")}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
