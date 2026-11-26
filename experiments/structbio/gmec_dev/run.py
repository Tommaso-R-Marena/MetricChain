#!/usr/bin/env python3
"""Experiment SB-X-001 — certified GMEC on the development set of public structures.

DEVELOPMENT EVIDENCE (benchmark level 3, development split): these structures were used while the
software was written.  Nothing here is a held-out result.

For every structure of `DEV_SET`:
  1. build the fixed-backbone rotamer model of `metricchain_sb.molecular` (ff14SB torsions and
     Lennard-Jones, distance-dependent-dielectric Coulomb with eps0 = 4, in vacuo, idealised
     staggered rotamers plus the native state, tables clipped at 1000 kcal/mol);
  2. round the float tables to the nearest multiple of 2**-20 kcal/mol — this integer instance
     *is* the model from here on (label [M]); record its sha256;
  3. baseline: toulbar2 on the identical integer instance (no certificate);
  4. produce a zero-gap `min` certificate (`metricchain_sb.gmec`), write it detached
     (`certs/<id>.mincert.json`), check it with the independent checker (`metricchain_sb.mincheck`);
  5. append one JSON row to `results.jsonl`.

    python experiments/structbio/gmec_dev/run.py                 # all structures
    python experiments/structbio/gmec_dev/run.py 1CRN 5PTI       # a subset
    python experiments/structbio/gmec_dev/run.py --check         # rebuild every instance, verify the
                                                                 # stored checksums and re-check the stored certificates

Timings are of this machine (label [E]); they are not benchmark results.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import platform
import subprocess
import sys
import time
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_sb import mincert  # noqa: E402
from metricchain_sb.baselines.toulbar2 import solve_gmec  # noqa: E402
from metricchain_sb.gmec import certify_gmec  # noqa: E402
from metricchain_sb.mincheck import check_min_certificate  # noqa: E402
from metricchain_sb.model import PairModel  # noqa: E402

DEV_SET = ["1CRN", "5PTI", "1BPI", "1PGA", "2IGD", "1UBQ"]
SCALE_BITS = 20
MODEL_PARAMS = dict(eps0=4.0, e_clip=1000.0, max_states_per_site=None, include_native=True, seed=0)
PDB_DIR = ROOT / "benchmarks" / "structbio" / "pdb"


def git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True)
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "src"], cwd=ROOT, capture_output=True, text=True)
        return out.stdout.strip() + ("+dirty" if dirty.stdout.strip() else "")
    except Exception:  # noqa: BLE001
        return "unknown"


def build_model(pdb_id: str):
    from metricchain_sb.molecular import build_energy_tables
    t0 = time.perf_counter()
    tables = build_energy_tables(str(PDB_DIR / f"{pdb_id}.pdb"), **MODEL_PARAMS)
    seconds = time.perf_counter() - t0
    meta = {"source": tables.meta.get("source"), "model_params": MODEL_PARAMS, "scale_bits": SCALE_BITS,
            "units": "kcal/mol", "sites": [{k: s.get(k) for k in ("chain", "resnum", "resname", "n_states")}
                                            for s in tables.meta.get("sites", [])]}
    model = PairModel.from_float(tables.unary, tables.pair, scale_bits=SCALE_BITS, meta=meta)
    return model, seconds, tables.meta


def run_one(pdb_id: str) -> dict:
    model, t_build, tmeta = build_model(pdb_id)
    sha = mincert.model_sha256(model)
    unit = Fraction(1, 2 ** SCALE_BITS)
    tb = solve_gmec(model)
    t0 = time.perf_counter()
    cert = certify_gmec(model, eps=Fraction(0), time_limit=3600)
    t_produce = time.perf_counter() - t0
    text = mincert.dumps(cert, include_model=False)
    (HERE / "certs").mkdir(exist_ok=True)
    cert_path = HERE / "certs" / f"{pdb_id}.mincert.json"
    cert_path.write_text(text)
    t0 = time.perf_counter()
    result = check_min_certificate(mincert.loads(text, model=model))
    t_check = time.perf_counter() - t0
    if not (result.accepted and result.full_box and result.certified_gap == 0):
        raise SystemExit(f"{pdb_id}: no zero-gap certificate over the full state set ({result.reason})")
    counts = mincert.count_nodes(cert.root)
    native = tuple(0 for _ in range(model.n))
    row = {
        "experiment": "SB-X-001", "split": "development", "pdb_id": pdb_id, "commit": git_commit(),
        "model_sha256": sha, "pdb_sha256": hashlib.sha256((PDB_DIR / f"{pdb_id}.pdb").read_bytes()).hexdigest(),
        "sites": model.n, "states_min": min(model.sizes), "states_max": max(model.sizes),
        "states_total": sum(model.sizes), "pairs": len(model.pair),
        "certificate_accepted": bool(result.accepted),
        "box_is_full": bool(result.full_box),      # only then is the bound a bound on the global minimum
        "certified_lower_bound_kcal": str(result.lower_bound), "witness_energy_kcal": str(result.witness_energy),
        "certified_gap_kcal": str(result.certified_gap),
        "certified_lower_bound_float": float(result.lower_bound),
        "toulbar2_energy_kcal": str(tb.energy_int * unit), "agrees_with_toulbar2": tb.energy_int * unit == result.witness_energy,
        "native_state_energy_float": float(model.energy(native)),
        "witness_sites_differing_from_native": sum(1 for a in cert.witness if a != 0),
        "seconds_build_tables": round(t_build, 2), "seconds_toulbar2": round(tb.seconds, 3),
        "seconds_produce_certificate": round(t_produce, 2), "seconds_check_certificate": round(t_check, 3),
        "toulbar2_nodes": tb.nodes, "bnb_nodes": cert.meta["bnb_nodes"], "cert_leaves": counts["leaf"],
        "cert_branches": counts["branch"], "cert_prunes": counts["prune"],
        "cert_message_integers": counts["message_integers"], "cert_bytes": len(text),
        "cert_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "platform": f"{platform.python_implementation()} {platform.python_version()} on {platform.machine()}",
        "versions": tmeta.get("software"),
    }
    return row


def check_all() -> int:
    rows = [json.loads(line) for line in (HERE / "results.jsonl").read_text().splitlines() if line.strip()]
    latest = {r["pdb_id"]: r for r in rows}
    failures = 0
    for pdb_id, row in latest.items():
        model, _, _ = build_model(pdb_id)
        sha = mincert.model_sha256(model)
        text = (HERE / "certs" / f"{pdb_id}.mincert.json").read_text()
        ok_sha = sha == row["model_sha256"]
        ok_cert = hashlib.sha256(text.encode()).hexdigest() == row["cert_sha256"]
        verdict = "instance checksum differs: the instance was not reproduced bit for bit on this machine"
        if ok_sha:
            res = check_min_certificate(mincert.loads(text, model=model))
            verdict = f"accepted={res.accepted} full_box={res.full_box} lower={res.lower_bound} gap={res.certified_gap}"
            ok_sha = res.accepted and res.full_box and str(res.lower_bound) == row["certified_lower_bound_kcal"]
        print(f"{pdb_id}: instance {'ok' if sha == row['model_sha256'] else 'DIFFERS'}; "
              f"certificate file {'ok' if ok_cert else 'DIFFERS'}; {verdict}")
        failures += 0 if (ok_sha and ok_cert) else 1
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", default=DEV_SET)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return 1 if check_all() else 0
    with open(HERE / "results.jsonl", "a") as out:
        for pdb_id in args.ids:
            row = run_one(pdb_id)
            out.write(json.dumps(row, sort_keys=True) + "\n")
            out.flush()
            print(f"{pdb_id}: accepted={row['certificate_accepted']} E*={row['certified_lower_bound_float']:.6f} kcal/mol "
                  f"gap={row['certified_gap_kcal']} toulbar2 agrees={row['agrees_with_toulbar2']} "
                  f"produce {row['seconds_produce_certificate']} s, check {row['seconds_check_certificate']} s, "
                  f"toulbar2 {row['seconds_toulbar2']} s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
