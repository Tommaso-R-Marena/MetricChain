#!/usr/bin/env python3
"""Experiment SB-X-006 — leaving a rotamer well, and optimality under entrywise table error.

DEVELOPMENT EVIDENCE on model v2 (hydrogens by the deterministic rule).  Two constructions the
science division proposed in SCI-REV-0026 (section 0 point 1; section 4), each a certified
minimisation of the kind SB-X-001 already does:

  state gap_i   min { E(x) : x_i != x*_i } - E(x*)                      (as SB-X-003)
  well gap_i    min { E(x) : x_i in another rotamer well than x*_i } - E(x*)
  at error b    the same two gaps in the *shifted* table (entries x* uses raised by b, all others
                lowered by b).  A positive well gap of the shifted table certifies: in every table
                whose entries lie within b of ours, every minimiser has site i in the well of x*_i.
  necessary optimality at b: does x* minimise every table within b?  (one minimisation)

b runs over one table unit (2^-20 kcal/mol: covers the rounding, at most half a unit, and the
observed evaluation error 4e-11 kcal/mol, which has no bound) and 0.001, 0.01, 0.1 kcal/mol.

EXPECTATIONS, WRITTEN BEFORE THE FIRST RUN (2026-11-27, 00:2x UTC; this file is committed before
`results.jsonl` exists):
  H6a  at b = one unit, x* is necessarily optimal on all six structures;
  H6b  at b = 0.01 kcal/mol, x* is necessarily optimal on none (the science division's expectation);
  H6c  at b = 0.01 kcal/mol at least half of the sites of every structure keep their well in every
       scenario; at b = 0.1 kcal/mol fewer than half do;
  H6d  the median well gap exceeds RT = 0.593 kcal/mol in every structure, while the median state
       gap is below it.
What would refute the reading "the model determines wells, not states": well gaps as small as
state gaps (H6d false).

    python experiments/structbio/wellgaps_dev/run.py                    # six structures, model v2
    python experiments/structbio/wellgaps_dev/run.py 1CRN --b-kcal 0.01
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import pathlib
import statistics
import sys
import time
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "structbio" / "gmec_dev"))

import run as dev  # noqa: E402
from metricchain_sb import mincert  # noqa: E402
from metricchain_sb.gmec import CertificationBudgetExceeded  # noqa: E402
from metricchain_sb.mincheck import check_min_certificate  # noqa: E402
from metricchain_sb.stability import certify_exclusion_gaps, certify_necessary_optimality, shifted_model  # noqa: E402

RT = 0.593
_STATE = {}


def _one(task):
    site, mode, b_units = task
    model, x_star, wells = _STATE["models"][b_units], _STATE["x_star"], _STATE["wells"][site]
    exclude = {x_star[site]} if mode == "state" else {a for a, w in enumerate(wells) if w == wells[x_star[site]]}
    row = {"experiment": "SB-X-006", "kind": "gap", "split": "development", "pdb_id": _STATE["pdb_id"],
           "model": _STATE["model_name"], "commit": dev.git_commit(), "site": site, "mode": mode,
           "b_units": b_units, "b_kcal": b_units / 2 ** dev.SCALE_BITS, "states_excluded": len(exclude),
           "n_states": model.sizes[site], "resname": _STATE["sites"][site]["resname"],
           "resnum": _STATE["sites"][site]["resnum"]}
    t0 = time.perf_counter()
    try:
        (gap,) = certify_exclusion_gaps(model, x_star, {site: exclude}, time_limit=_STATE["time_limit"])
    except CertificationBudgetExceeded as exc:
        row.update(outcome="abstained", reason=str(exc))
    else:
        if gap.gap is None:
            row.update(outcome="no-alternative")
        else:
            res = check_min_certificate(gap.certificate)
            row.update(outcome="certified" if res.accepted and res.certified_gap == 0 else "REJECTED",
                       gap_kcal=str(gap.gap), gap_float=float(gap.gap),
                       alternative_state=int(gap.alternative[site]),
                       sites_changed_in_alternative=sum(1 for a, c in zip(gap.alternative, x_star) if a != c))
    row["seconds"] = round(time.perf_counter() - t0, 2)
    return row


def run_structure(pdb_id, model_name, b_list, processes, time_limit, out):
    model, _, tmeta = dev.build_model(pdb_id, model_name)
    cert = mincert.loads(dev.cert_path(pdb_id, model_name).read_text(), model=model)
    res = check_min_certificate(cert)
    if not (res.accepted and res.full_box and res.certified_gap == 0):
        raise SystemExit(f"{pdb_id} [{model_name}]: the stored certificate is not a zero-gap certificate of this instance")
    x_star = tuple(cert.witness)
    sites = tmeta["sites"]
    _STATE.update(pdb_id=pdb_id, model_name=model_name, x_star=x_star, sites=sites, time_limit=time_limit,
                  wells=[[tuple(w) for w in s["wells"]] for s in sites],
                  models={0: model, **{b: shifted_model(model, x_star, b) for b in b_list}})
    for b in b_list:                                  # necessary optimality: one minimisation per b
        t0 = time.perf_counter()
        row = {"experiment": "SB-X-006", "kind": "necessary-optimality", "split": "development", "pdb_id": pdb_id,
               "model": model_name, "commit": dev.git_commit(), "b_units": b, "b_kcal": b / 2 ** dev.SCALE_BITS,
               "model_sha256": mincert.model_sha256(model)}
        try:
            verdict = certify_necessary_optimality(model, x_star, b, time_limit=time_limit)
        except CertificationBudgetExceeded as exc:
            row.update(outcome="abstained", reason=str(exc))
        else:
            ok = check_min_certificate(verdict.certificate)
            row.update(outcome="certified" if ok.accepted and ok.full_box and ok.certified_gap == 0 else "REJECTED",
                       holds=bool(verdict.holds), margin_kcal=str(verdict.margin), margin_float=float(verdict.margin))
            if not verdict.holds:
                cx = verdict.counterexample
                row.update(counterexample_sites_changed=sum(1 for a, c in zip(cx, x_star) if a != c),
                           counterexample_wells_changed=sum(1 for i, (a, c) in enumerate(zip(cx, x_star))
                                                            if _STATE["wells"][i][a] != _STATE["wells"][i][c]))
        row["seconds"] = round(time.perf_counter() - t0, 2)
        out.write(json.dumps(row, sort_keys=True) + "\n")
        out.flush()
        print(json.dumps({k: row.get(k) for k in ("pdb_id", "kind", "b_kcal", "outcome", "holds", "margin_float",
                                                   "counterexample_wells_changed", "seconds")}), flush=True)
    tasks = [(i, mode, b) for b in [0] + list(b_list) for mode in ("state", "well") for i in range(model.n)
             if not (mode == "state" and b != 0)]     # state gaps only in the unshifted table
    with mp.get_context("fork").Pool(processes) as pool:
        rows = pool.map(_one, tasks, chunksize=1)
    for row in rows:
        out.write(json.dumps(row, sort_keys=True) + "\n")
    for b in [0] + list(b_list):
        for mode in ("state", "well"):
            sel = [r for r in rows if r["b_units"] == b and r["mode"] == mode]
            if not sel:
                continue
            gaps = [r["gap_float"] for r in sel if r["outcome"] == "certified"]
            summary = {"experiment": "SB-X-006", "kind": "summary", "split": "development", "pdb_id": pdb_id,
                       "model": model_name, "commit": dev.git_commit(), "mode": mode, "b_units": b,
                       "b_kcal": b / 2 ** dev.SCALE_BITS, "sites": len(sel), "certified": len(gaps),
                       "abstained": sum(1 for r in sel if r["outcome"] == "abstained"),
                       "rejected": sum(1 for r in sel if r["outcome"] == "REJECTED"),
                       "positive": sum(1 for g in gaps if g > 0),
                       "min_gap": min(gaps, default=None), "median_gap": statistics.median(gaps) if gaps else None,
                       "below_RT": sum(1 for g in gaps if g < RT), "below_3RT": sum(1 for g in gaps if g < 3 * RT),
                       "seconds_total": round(sum(r["seconds"] for r in sel), 1)}
            out.write(json.dumps(summary, sort_keys=True) + "\n")
            print(json.dumps({k: summary[k] for k in ("pdb_id", "mode", "b_kcal", "sites", "certified", "abstained",
                                                      "positive", "min_gap", "median_gap", "below_RT", "below_3RT")}),
                  flush=True)
    out.flush()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=list(dev.DEV_SET))
    ap.add_argument("--model", choices=sorted(dev.MODELS), default="v2")
    ap.add_argument("--b-kcal", type=float, nargs="*", default=[0.001, 0.01, 0.1])
    ap.add_argument("--no-unit", action="store_true", help="do not add b = one table unit")
    ap.add_argument("--processes", type=int, default=4)
    ap.add_argument("--time-limit", type=float, default=600.0)
    args = ap.parse_args()
    b_list = sorted({round(b * 2 ** dev.SCALE_BITS) for b in args.b_kcal} | (set() if args.no_unit else {1}))
    with open(HERE / "results.jsonl", "a") as out:
        for pdb_id in args.ids:
            run_structure(pdb_id, args.model, b_list, args.processes, args.time_limit, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
