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
#: Model variants (definition: docstring of metricchain_sb/molecular/tables.py).
#:   v1      hydrogens as left by OpenMM's addHydrogens from random starts with seed 0.  The rows of
#:           2026-11-26 are on this model.  Its tables depend on the seed by tens of kcal/mol
#:           (SB-X-005; SCI-REV-0026 F1): kept for reproduction only.
#:   v2      hydrogens by the deterministic rule of molecular/hydrogens.py; deposited state + library.
#:   v2-lib  as v2 without the deposited state (library states only; SCI-REV-0026 F2).
_COMMON = dict(eps0=4.0, e_clip=1000.0, max_states_per_site=None, seed=0)
MODELS = {
    "v1": dict(_COMMON, include_native=True, hydrogens="openmm-seeded"),
    "v2": dict(_COMMON, include_native=True, hydrogens="ideal"),
    "v2-lib": dict(_COMMON, include_native=False, hydrogens="ideal"),
}
DEFAULT_MODEL = "v2"
MODEL_PARAMS = MODELS["v1"]          # name used by SB-X-005 (the seed measurement is about v1)
PDB_DIR = ROOT / "benchmarks" / "structbio" / "pdb"


def _read_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True)
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "src"], cwd=ROOT, capture_output=True, text=True)
        return out.stdout.strip() + ("+dirty" if dirty.stdout.strip() else "")
    except Exception:  # noqa: BLE001
        return "unknown"


#: The commit of the code this process has in memory: read once, when the module is loaded, and
#: never again (SB-DEF-08 — a row must not record a head that moved while the process ran).
START_COMMIT = _read_commit()


def git_commit() -> str:
    return START_COMMIT


def cert_path(pdb_id: str, model: str = DEFAULT_MODEL) -> pathlib.Path:
    """Where the detached certificate of a structure lives (v1 files keep their original place)."""
    base = HERE / "certs" if model == "v1" else HERE / "certs" / model
    return base / f"{pdb_id}.mincert.json"


def build_tables(pdb_id: str, model: str = DEFAULT_MODEL):
    """(float tables, integer PairModel, seconds) of one structure under one model variant."""
    from metricchain_sb.molecular import build_energy_tables
    params = MODELS[model]
    t0 = time.perf_counter()
    tables = build_energy_tables(str(PDB_DIR / f"{pdb_id}.pdb"), **params)
    seconds = time.perf_counter() - t0
    meta = {"source": tables.meta.get("source"), "model": model, "model_params": params, "scale_bits": SCALE_BITS,
            "units": "kcal/mol",
            "sites": [{k: s.get(k) for k in ("chain", "resnum", "resname", "n_states", "wells", "deposited_well")}
                      for s in tables.meta.get("sites", [])]}
    pair_model = PairModel.from_float(tables.unary, tables.pair, scale_bits=SCALE_BITS, meta=meta)
    return tables, pair_model, seconds


def build_model(pdb_id: str, model: str = DEFAULT_MODEL):
    tables, pair_model, seconds = build_tables(pdb_id, model)
    return pair_model, seconds, tables.meta


def uses_clipped_entry(tables, x) -> bool:
    """Does configuration `x` use a table entry that was clipped?  If the certified minimiser uses
    none, it also minimises the unclipped integer table: clipping only lowers entries (and rounding
    is monotone), so E_unclipped(y) >= E_clipped(y) >= E_clipped(x) = E_unclipped(x) for every y.
    (The check the science division asked to see printed with each row, SCI-REV-0026 section 2.)"""
    clip = tables.meta["clipping"]["e_clip"]
    if clip is None:
        return False
    if any(tables.unary_unclipped[i][a] > clip for i, a in enumerate(x)):
        return True
    return any(p[x[i], x[j]] > clip for (i, j), p in tables.pair_unclipped.items())


def run_one(pdb_id: str, model_name: str = DEFAULT_MODEL) -> dict:
    tables, model, t_build = build_tables(pdb_id, model_name)
    tmeta = tables.meta
    sha = mincert.model_sha256(model)
    unit = Fraction(1, 2 ** SCALE_BITS)
    tb = solve_gmec(model)
    t0 = time.perf_counter()
    cert = certify_gmec(model, eps=Fraction(0), time_limit=3600)
    t_produce = time.perf_counter() - t0
    text = mincert.dumps(cert, include_model=False)
    path = cert_path(pdb_id, model_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    t0 = time.perf_counter()
    result = check_min_certificate(mincert.loads(text, model=model))
    t_check = time.perf_counter() - t0
    if not (result.accepted and result.full_box and result.certified_gap == 0):
        raise SystemExit(f"{pdb_id}: no zero-gap certificate over the full state set ({result.reason})")
    counts = mincert.count_nodes(cert.root)
    native = tuple(0 for _ in range(model.n))
    has_deposited = MODELS[model_name]["include_native"]
    sites = tmeta["sites"]
    clipped = uses_clipped_entry(tables, cert.witness)
    row = {
        "experiment": "SB-X-001", "split": "development", "pdb_id": pdb_id, "commit": git_commit(),
        "model": model_name, "witness": list(cert.witness),
        # what the count below is: sites whose chosen STATE is a library state, not sites whose
        # conformation differs (a library state can lie a few degrees from the deposited one)
        "witness_sites_at_a_library_state": sum(1 for a in cert.witness if a != 0) if has_deposited else model.n,
        "witness_sites_in_another_well_than_deposited": sum(
            1 for s, a in zip(sites, cert.witness) if s["wells"][a] != s["deposited_well"]),
        "witness_uses_clipped_entry": clipped, "minimum_also_of_unclipped_integer_table": not clipped,
        "model_sha256": sha, "pdb_sha256": hashlib.sha256((PDB_DIR / f"{pdb_id}.pdb").read_bytes()).hexdigest(),
        "sites": model.n, "states_min": min(model.sizes), "states_max": max(model.sizes),
        "states_total": sum(model.sizes), "pairs": len(model.pair),
        "certificate_accepted": bool(result.accepted),
        "box_is_full": bool(result.full_box),      # only then is the bound a bound on the global minimum
        "certified_lower_bound_kcal": str(result.lower_bound), "witness_energy_kcal": str(result.witness_energy),
        "certified_gap_kcal": str(result.certified_gap),
        "certified_lower_bound_float": float(result.lower_bound),
        "toulbar2_energy_kcal": str(tb.energy_int * unit), "agrees_with_toulbar2": tb.energy_int * unit == result.witness_energy,
        "deposited_state_energy_float": float(model.energy(native)) if has_deposited else None,
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
    latest = {(r["pdb_id"], r.get("model", "v1")): r for r in rows}     # rows without the field are v1
    failures = 0
    for (pdb_id, model_name), row in latest.items():
        model, _, _ = build_model(pdb_id, model_name)
        sha = mincert.model_sha256(model)
        text = cert_path(pdb_id, model_name).read_text()
        ok_sha = sha == row["model_sha256"]
        ok_cert = hashlib.sha256(text.encode()).hexdigest() == row["cert_sha256"]
        verdict = "instance checksum differs: the instance was not reproduced bit for bit on this machine"
        if ok_sha:
            res = check_min_certificate(mincert.loads(text, model=model))
            verdict = f"accepted={res.accepted} full_box={res.full_box} lower={res.lower_bound} gap={res.certified_gap}"
            ok_sha = res.accepted and res.full_box and str(res.lower_bound) == row["certified_lower_bound_kcal"]
        print(f"{pdb_id} [{model_name}]: instance {'ok' if sha == row['model_sha256'] else 'DIFFERS'}; "
              f"certificate file {'ok' if ok_cert else 'DIFFERS'}; {verdict}")
        failures += 0 if (ok_sha and ok_cert) else 1
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", default=DEV_SET)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--model", choices=sorted(MODELS), default=DEFAULT_MODEL)
    args = ap.parse_args()
    if args.check:
        return 1 if check_all() else 0
    with open(HERE / "results.jsonl", "a") as out:
        for pdb_id in args.ids:
            row = run_one(pdb_id, args.model)
            out.write(json.dumps(row, sort_keys=True) + "\n")
            out.flush()
            print(f"{pdb_id} [{args.model}]: accepted={row['certificate_accepted']} "
                  f"E*={row['certified_lower_bound_float']:.6f} kcal/mol "
                  f"other-well sites={row['witness_sites_in_another_well_than_deposited']}/{row['sites']} "
                  f"clipped entry used={row['witness_uses_clipped_entry']} "
                  f"gap={row['certified_gap_kcal']} toulbar2 agrees={row['agrees_with_toulbar2']} "
                  f"produce {row['seconds_produce_certificate']} s, check {row['seconds_check_certificate']} s, "
                  f"toulbar2 {row['seconds_toulbar2']} s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
