#!/usr/bin/env python3
"""Experiment SB-X-004 — certified enclosures of ln Z on the development set (capability C2, first version).

DEVELOPMENT EVIDENCE.  For a structure of SB-X-001 and thresholds `theta` (kcal/mol): thermal
dead-end elimination with margin `TAU`, product-form relaxation of every pair whose non-additive
oscillation is at most `theta`, exact variable elimination of the rest (float tier: binary64 with
outward rounding, assumptions F1-F3 of `metricchain_sb.itables`), at `beta = 1000/593` per kcal/mol
(RT = 0.593 kcal/mol).  An abstention (table budget exceeded) is recorded as an outcome.

    python experiments/structbio/lnz_dev/run.py 1CRN
    python experiments/structbio/lnz_dev/run.py 1CRN --exact-check    # also the exact-rational tier at the coarsest threshold

The interval is the one the checker computes (`zcheck`).  Rule semantics: machine-checked in
`proofs/StructBio/FactorElimination.lean` (this division's file, 2026-11-27; before that: [V] for
chains and a paper argument in general); the checker implementation is tested.  A row records the
recipe (counts of steps) and is reproduced by re-running at the recorded commit; certificates can
be written with `zcert.dumps`.

MODELS (added 2026-11-27).  The rows of 2026-11-26 are on model v1 (seeded hydrogens, deposited
state among the states, every state with weight one): `--model v1 --unweighted` reproduces them.
The default is now `--model v2-lib` with state weights: library states only, each entering with
its share of the residue's torsion space (`molecular.rotamers.state_share`), so that the sum is
an average of exp(-beta E) over uniformly distributed torsions and `-ln Z_w / beta` is a free
energy relative to non-interacting free rotors (SCI-REV-0026 F2 (c): a sum over "the deposited
state plus a library" is not a quadrature of anything).

EXPECTATIONS FOR CRAMBIN ON v2-lib, WEIGHTED, WRITTEN BEFORE THE FIRST SUCH RUN (2026-11-27):
  H7a  with conditioning (table budget 3e6, up to 2e5 leaves) the width is below 1 nat at
       threshold 0.01 and below 0.3 nats at 0.003 kcal/mol (v1: 0.478 and 0.137);
  H7b  the exact tier's interval lies inside the float tier's at the coarsest threshold;
  H7c  (direction unknown) whether the strained library-only table prunes to fewer states than
       v1's did (v1: 233 eliminations at margin 12 kcal/mol without conditioning).
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
from metricchain_sb.partition import PartitionBudgetExceeded, certify_partition, weighted_model  # noqa: E402
from metricchain_sb.zcheck import check_partition_certificate  # noqa: E402

BETA = Fraction(1000, 593)
TAU = 12.0
THETAS = (1.0, 0.3, 0.1, 0.03, 0.01)
MAX_ENTRIES = 30_000_000


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=["1CRN"])
    ap.add_argument("--exact-check", action="store_true")
    ap.add_argument("--thetas", type=float, nargs="*", default=list(THETAS))
    ap.add_argument("--max-leaves", type=int, default=1,
                    help="allow conditioning (branch nodes) up to this many leaves; 1 = none")
    ap.add_argument("--max-entries", type=int, default=MAX_ENTRIES)
    ap.add_argument("--populations", action="store_true",
                    help="also certify population intervals of every residue at the last threshold")
    ap.add_argument("--model", choices=sorted(dev.MODELS), default="v2-lib")
    ap.add_argument("--unweighted", action="store_true",
                    help="every state with weight one (the only possibility when the deposited state is a state)")
    args = ap.parse_args()
    if dev.MODELS[args.model]["include_native"] and not args.unweighted:
        raise SystemExit("the deposited state stands for no share of torsion space: use a library-only model, "
                         "or --unweighted to sum over the states as they are")
    with open(HERE / "results.jsonl", "a") as out:
        for pdb_id in args.ids:
            base, _, tmeta = dev.build_model(pdb_id, args.model)
            model = base if args.unweighted else weighted_model(base, [s["state_shares"] for s in tmeta["sites"]], BETA)
            e_star = None
            cert_path = dev.cert_path(pdb_id, args.model)
            if cert_path.exists():             # the certified minimiser of the unweighted table, evaluated in this table
                e_star = model.energy(mincert.loads(cert_path.read_text(), model=base).witness)
            runs = [(theta, "float") for theta in args.thetas] + ([(args.thetas[0], "exact")] if args.exact_check else [])
            for theta, tier in runs:
                row = {"experiment": "SB-X-004", "split": "development", "pdb_id": pdb_id, "commit": dev.git_commit(),
                       "model": args.model, "weighted_by_state_share": not args.unweighted,
                       "model_sha256": mincert.model_sha256(model), "beta_per_kcal": str(BETA), "tau_kcal": TAU,
                       "theta_kcal": theta, "arithmetic": tier, "max_entries": args.max_entries,
                       "max_leaves": args.max_leaves}
                t0 = time.perf_counter()
                try:
                    cert = certify_partition(model, BETA, tau=TAU, theta=theta, arithmetic=tier,
                                             max_entries=args.max_entries, max_leaves=args.max_leaves)
                except PartitionBudgetExceeded as exc:
                    row.update(outcome="abstained", reason=str(exc), seconds=round(time.perf_counter() - t0, 2))
                else:
                    res = check_partition_certificate(cert, arithmetic=tier, max_entries=args.max_entries)
                    row.update(outcome="certified" if res.accepted else "REJECTED", full_box=bool(res.full_box),
                               ln_z_lo=str(res.ln_z_lo), ln_z_hi=str(res.ln_z_hi),
                               ln_z_lo_float=float(res.ln_z_lo), ln_z_hi_float=float(res.ln_z_hi),
                               width_nats=float(res.ln_z_hi - res.ln_z_lo),
                               leaves=res.stats["leaves"], prune_steps=res.stats["prune"], relax_steps=res.stats["relax"],
                               conditioned=cert.branch is not None,
                               largest_table=res.stats["largest_table"], seconds=round(time.perf_counter() - t0, 2))
                    if e_star is not None:
                        row["minus_beta_E_min"] = float(-BETA * e_star)
                out.write(json.dumps(row, sort_keys=True) + "\n")
                out.flush()
                print(json.dumps({k: row.get(k) for k in ("pdb_id", "theta_kcal", "arithmetic", "outcome", "ln_z_lo_float",
                                                           "ln_z_hi_float", "width_nats", "leaves", "largest_table",
                                                           "seconds", "reason")}), flush=True)
            if args.populations:
                theta = args.thetas[-1]
                for site in range(model.n):
                    row = {"experiment": "SB-X-004", "kind": "population", "split": "development", "pdb_id": pdb_id,
                           "model": args.model, "weighted_by_state_share": not args.unweighted,
                           "resname": tmeta["sites"][site]["resname"], "resnum": tmeta["sites"][site]["resnum"],
                           "wells": tmeta["sites"][site]["wells"], "deposited_well": tmeta["sites"][site]["deposited_well"],
                           "commit": dev.git_commit(), "model_sha256": mincert.model_sha256(model), "site": site,
                           "theta_kcal": theta, "tau_kcal": TAU, "beta_per_kcal": str(BETA), "arithmetic": "float",
                           "max_entries": args.max_entries, "max_leaves": args.max_leaves}
                    t0 = time.perf_counter()
                    try:
                        cert = certify_partition(model, BETA, keep=site, tau=TAU, theta=theta, arithmetic="float",
                                                 max_entries=args.max_entries, max_leaves=args.max_leaves)
                    except PartitionBudgetExceeded as exc:
                        row.update(outcome="abstained", reason=str(exc))
                    else:
                        res = check_partition_certificate(cert, arithmetic="float", max_entries=args.max_entries)
                        pops = {int(a): [float(lo), float(hi)] for a, (lo, hi) in sorted(res.populations.items())}
                        widths = [hi - lo for lo, hi in pops.values()]
                        row.update(outcome="certified" if res.accepted else "REJECTED", populations=pops,
                                   removed_states_upper=float(res.removed_upper), n_states=model.sizes[site],
                                   max_width=max(widths), leaves=res.stats["leaves"],
                                   most_populated_state=max(pops, key=lambda a: pops[a][0]),
                                   most_populated_lower=max(lo for lo, _ in pops.values()))
                    row["seconds"] = round(time.perf_counter() - t0, 2)
                    out.write(json.dumps(row, sort_keys=True) + "\n")
                    out.flush()
                    print(json.dumps({k: row.get(k) for k in ("pdb_id", "site", "outcome", "max_width", "most_populated_state",
                                                               "most_populated_lower", "leaves", "seconds", "reason")}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
