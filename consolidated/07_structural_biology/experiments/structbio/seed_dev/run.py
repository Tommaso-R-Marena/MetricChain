#!/usr/bin/env python3
"""Experiment SB-X-005 — how much of the certified minimum survives another hydrogen-placement seed.

DEVELOPMENT MEASUREMENT (not a benchmark), asked for by the science division (SCI-REV-0026, finding
F1, request SB-6).  Model v1 places hydrogens with `openmm.app.Modeller.addHydrogens`: random start
positions (Python's `random`, seeded with `seed`) followed by at most 50 minimiser iterations.  Our
record SB-DEF-03 saw one-body entries of crambin differ by about 70 kcal/mol between two unseeded
builds.  `seed = 0` made the build reproducible; it did not make it less arbitrary.

For every development structure and every seed 0..9 this script builds the tables, certifies the
minimum of the integer table (checker must accept, full box, zero gap), compares with toulbar2 on
the identical instance, and records the minimiser.  Per structure it then records

  * the number of sites whose certified state differs from that of seed 0, per seed, and the
    number of sites whose certified state is not the same for all seeds;
  * the range of the certified minimum over seeds;
  * the energy, in the seed-0 table, of the minimisers of the other seeds (above the seed-0 minimum);
  * the spread (max - min over seeds) of every table entry: quantiles, for one-body and pair entries.

READING, WRITTEN BEFORE THE FIRST RUN (2026-11-26 23:58 UTC; the commit that first contains this
file precedes the commit that first contains `results.jsonl`):

  material     if in ANY structure some seed changes the certified state at more than 5 % of the
               sites, OR the certified minimum ranges over more than 1 kcal/mol.  Consequences we
               commit to: (i) every result on model v1 is a statement about the seed-0 tables and
               is labelled so next to R-1, R-6, R-7; (ii) no held-out run on v1; (iii) hydrogen
               placement becomes a deterministic function of the heavy atoms under a new model
               name, and development results and hypotheses are formed again on that model.
  immaterial   if in EVERY structure no site changes and the minimum ranges over less than
               0.01 kcal/mol.  Then `seed = 0` stays in the model definition with this evidence.
  intermediate otherwise: reported as measured; deterministic placement is still preferred.

PREDICTION OF THIS DIVISION, WRITTEN AT THE SAME TIME: material — in at least four of the six
structures more than 5 % of the sites change for some seed, and in at least four of six the
minimum ranges over more than 10 kcal/mol.

    python experiments/structbio/seed_dev/run.py                # six structures, seeds 0..9
    python experiments/structbio/seed_dev/run.py 1CRN --seeds 0 1 2
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from fractions import Fraction

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "structbio" / "gmec_dev"))

import run as dev  # noqa: E402
from metricchain_sb import mincert  # noqa: E402
from metricchain_sb.baselines.toulbar2 import solve_gmec  # noqa: E402
from metricchain_sb.gmec import CertificationBudgetExceeded, certify_gmec  # noqa: E402
from metricchain_sb.mincheck import check_min_certificate  # noqa: E402
from metricchain_sb.model import PairModel  # noqa: E402
from metricchain_sb.molecular import build_energy_tables  # noqa: E402

QUANTILES = (0.5, 0.9, 0.99, 1.0)


def build(pdb_id: str, seed: int):
    params = dict(dev.MODEL_PARAMS, seed=seed)
    tables = build_energy_tables(str(dev.PDB_DIR / f"{pdb_id}.pdb"), **params)
    model = PairModel.from_float(tables.unary, tables.pair, scale_bits=dev.SCALE_BITS, meta={"seed": seed})
    return tables, model


def uses_clipped_entry(tables, x) -> bool:
    clip = tables.meta["clipping"]["e_clip"]
    if clip is None:
        return False
    if any(tables.unary[i][a] >= clip for i, a in enumerate(x)):
        return True
    return any(p[x[i], x[j]] >= clip for (i, j), p in tables.pair.items())


def quantiles(values: np.ndarray) -> dict:
    return {str(q): float(np.quantile(values, q)) for q in QUANTILES} if values.size else {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=list(dev.DEV_SET))
    ap.add_argument("--seeds", type=int, nargs="*", default=list(range(10)))
    ap.add_argument("--time-limit", type=float, default=900.0)
    args = ap.parse_args()
    unit = Fraction(1, 2 ** dev.SCALE_BITS)
    with open(HERE / "results.jsonl", "a") as out:
        for pdb_id in args.ids:
            per_seed, models, lo_u, hi_u, lo_p, hi_p = {}, {}, None, None, None, None
            for seed in args.seeds:
                t0 = time.perf_counter()
                tables, model = build(pdb_id, seed)
                row = {"experiment": "SB-X-005", "kind": "seed", "split": "development", "pdb_id": pdb_id,
                       "seed": seed, "commit": dev.git_commit(), "model_sha256": mincert.model_sha256(model),
                       "sites": model.n, "sizes": list(model.sizes),
                       "clipped_entries": tables.meta["clipping"]["n_clipped_entries"]}
                try:
                    cert = certify_gmec(model, eps=Fraction(0), time_limit=args.time_limit)
                except CertificationBudgetExceeded as exc:
                    row.update(outcome="abstained", reason=str(exc))
                else:
                    res = check_min_certificate(cert)
                    ok = bool(res.accepted and res.full_box and res.certified_gap == 0)
                    tb = solve_gmec(model, time_limit=900)
                    row.update(outcome="certified" if ok else "REJECTED", minimum_kcal=str(res.witness_energy),
                               minimum_float=float(res.witness_energy), witness=list(cert.witness),
                               agrees_with_toulbar2=bool(tb.energy_int * unit == res.witness_energy),
                               witness_uses_clipped_entry=uses_clipped_entry(tables, cert.witness),
                               deposited_state_energy_float=float(model.energy(tuple(0 for _ in range(model.n)))),
                               sites_at_deposited_state=sum(1 for a in cert.witness if a == 0))
                    if ok:
                        per_seed[seed], models[seed] = cert.witness, model
                row["seconds"] = round(time.perf_counter() - t0, 2)
                out.write(json.dumps(row, sort_keys=True) + "\n")
                out.flush()
                print(json.dumps({k: row.get(k) for k in ("pdb_id", "seed", "outcome", "minimum_float",
                                                           "sites_at_deposited_state", "agrees_with_toulbar2",
                                                           "witness_uses_clipped_entry", "seconds")}), flush=True)
                u = np.concatenate([np.asarray(a, dtype=float).ravel() for a in tables.unary])
                p = np.concatenate([np.asarray(tables.pair[k], dtype=float).ravel() for k in sorted(tables.pair)])
                lo_u, hi_u = (u, u) if lo_u is None else (np.minimum(lo_u, u), np.maximum(hi_u, u))
                lo_p, hi_p = (p, p) if lo_p is None else (np.minimum(lo_p, p), np.maximum(hi_p, p))
            if not per_seed:
                continue
            ref_seed = min(per_seed)
            ref = per_seed[ref_seed]
            n = len(ref)
            changed = {str(s): sum(1 for a, b in zip(ref, x) if a != b) for s, x in per_seed.items() if s != ref_seed}
            not_constant = sum(1 for i in range(n) if len({x[i] for x in per_seed.values()}) > 1)
            minima = {s: models[s].energy(x) for s, x in per_seed.items()}
            cross = {str(s): float(models[ref_seed].energy(x) - minima[ref_seed]) for s, x in per_seed.items() if s != ref_seed}
            clip = dev.MODEL_PARAMS["e_clip"]
            unclipped_u, unclipped_p = hi_u < clip, hi_p < clip
            summary = {"experiment": "SB-X-005", "kind": "summary", "split": "development", "pdb_id": pdb_id,
                       "commit": dev.git_commit(), "seeds": sorted(per_seed), "reference_seed": ref_seed, "sites": n,
                       "sites_changed_vs_reference": changed, "max_sites_changed": max(changed.values(), default=0),
                       "max_fraction_changed": max(changed.values(), default=0) / n,
                       "sites_not_constant_over_seeds": not_constant,
                       "minimum_min_float": float(min(minima.values())), "minimum_max_float": float(max(minima.values())),
                       "minimum_range_kcal": float(max(minima.values()) - min(minima.values())),
                       "energy_in_reference_table_above_reference_minimum": cross,
                       "entry_spread_unary_all": quantiles(hi_u - lo_u), "entry_spread_pair_all": quantiles(hi_p - lo_p),
                       "entry_spread_unary_never_clipped": quantiles((hi_u - lo_u)[unclipped_u]),
                       "entry_spread_pair_never_clipped": quantiles((hi_p - lo_p)[unclipped_p]),
                       "entries_unary": int(hi_u.size), "entries_pair": int(hi_p.size)}
            out.write(json.dumps(summary, sort_keys=True) + "\n")
            out.flush()
            print(json.dumps({k: summary[k] for k in ("pdb_id", "sites", "sites_changed_vs_reference",
                                                      "sites_not_constant_over_seeds", "minimum_range_kcal",
                                                      "entry_spread_unary_never_clipped",
                                                      "entry_spread_pair_never_clipped")}), flush=True)
            if pdb_id == "1CRN":      # the per-entry spread of the smallest instance, kept for SB-13 (necessary optimality)
                np.savez_compressed(HERE / "1CRN_entry_spread.npz", unary=hi_u - lo_u, pair=hi_p - lo_p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
