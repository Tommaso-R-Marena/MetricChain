#!/usr/bin/env python3
"""Experiment SB-X-007 — the null method: does the dual bound alone certify the minimum?

DEVELOPMENT EVIDENCE.  Baseline asked for by the Frontier division (FRONTIER-MSG-0001 section 4 (a))
and the science division (SCI-REV-0026 section 7.2): the exact dual bound of the pairwise
relaxation with no dead-end elimination and no search — in our format a certificate that is a
single leaf on the full box, checked by the same checker.  Yanover, Schueler-Furman and Weiss
(2008) report a relaxation finding the global optimum for about 85 % of a standard side-chain
benchmark; if the leaf alone certifies most of our instances, eliminations and the tree are
rarely needed.

For every development structure and model variant: one-leaf certificates are attempted at
eps = 0 and then at increasing eps (kcal/mol); the row records the smallest eps of the list at
which one leaf suffices, i.e. an upper bound on the gap the dual bound leaves.

EXPECTATION WRITTEN BEFORE THE FIRST RUN (2026-11-27): the leaf alone certifies exact
optimality (eps = 0) for at least four of the six structures in each of the variants v2 and
v2-lib.  (Reason for the guess: our certificates on these structures consist of eliminations
and a single leaf — but the leaf was computed after the eliminations had shrunk the box.)

    python experiments/structbio/nullmethod_dev/run.py
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
from metricchain_sb.gmec import CertificationBudgetExceeded, certify_gmec  # noqa: E402
from metricchain_sb.mincheck import check_min_certificate  # noqa: E402

EPS_LADDER = ("0", "1/1000", "1/100", "1/10", "1", "10", "100")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=list(dev.DEV_SET))
    ap.add_argument("--models", nargs="*", default=["v2", "v2-lib"])
    ap.add_argument("--max-sweeps", type=int, default=3000)
    args = ap.parse_args()
    with open(HERE / "results.jsonl", "a") as out:
        for model_name in args.models:
            for pdb_id in args.ids:
                model, _, _ = dev.build_model(pdb_id, model_name)
                stored = mincert.loads(dev.cert_path(pdb_id, model_name).read_text(), model=model)
                e_min = model.energy(stored.witness)            # the certified minimum (SB-X-001)
                row = {"experiment": "SB-X-007", "split": "development", "pdb_id": pdb_id, "model": model_name,
                       "commit": dev.git_commit(), "model_sha256": mincert.model_sha256(model), "sites": model.n,
                       "max_sweeps": args.max_sweeps, "eps_ladder_kcal": list(EPS_LADDER),
                       "certified_minimum_kcal": str(e_min)}
                t0 = time.perf_counter()
                for eps in EPS_LADDER:
                    try:
                        cert = certify_gmec(model, eps=Fraction(eps), witness=stored.witness, eliminate=False,
                                            max_nodes=1, max_sweeps=args.max_sweeps)
                    except CertificationBudgetExceeded:
                        continue
                    res = check_min_certificate(cert)
                    counts = mincert.count_nodes(cert.root)
                    ok = bool(res.accepted and res.full_box and counts["prune"] == 0 and counts["branch"] == 0
                              and counts["leaf"] == 1 and res.witness_energy == e_min)
                    row.update(outcome="one-leaf" if ok else "REJECTED", smallest_eps_kcal=eps,
                               certified_gap_kcal=str(res.certified_gap), certified_gap_float=float(res.certified_gap),
                               exact_by_leaf_alone=bool(ok and res.certified_gap == 0))
                    break
                else:
                    row.update(outcome="abstained", smallest_eps_kcal=None, exact_by_leaf_alone=False)
                row["seconds"] = round(time.perf_counter() - t0, 2)
                out.write(json.dumps(row, sort_keys=True) + "\n")
                out.flush()
                print(json.dumps({k: row.get(k) for k in ("pdb_id", "model", "outcome", "smallest_eps_kcal",
                                                           "certified_gap_float", "exact_by_leaf_alone", "seconds")}),
                      flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
