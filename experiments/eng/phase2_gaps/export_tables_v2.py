"""Export the integer instances of the structural-biology division's models v2 and v2-lib.

A copy of ``experiments/eng/sb_review/export_tables.py`` (same archive layout, same toulbar2 call of ours) with one
change: the builder parameters are those of ``MODELS["v2"]`` / ``MODELS["v2-lib"]`` of their driver
``experiments/structbio/gmec_dev/run.py`` (identical at 41fa668 and a5cc106):

    v2      eps0=4.0, e_clip=1000.0, max_states_per_site=None, seed=0, include_native=True,  hydrogens="ideal"
    v2-lib  eps0=4.0, e_clip=1000.0, max_states_per_site=None, seed=0, include_native=False, hydrogens="ideal"

The tables are NOT stored by that division; they are regenerated here by THEIR builder
(``metricchain_sb.molecular.build_energy_tables`` and ``PairModel.from_float``), imported from the read-only worktree
given by ``--sb``.  Whether the tables are the stated energy function is their claim K5 and is not tested here.  The
checksum comparison with the certificate's ``model_sha256`` is done downstream by our own code (check_files.py).

    <their python> experiments/eng/phase2_gaps/export_tables_v2.py --sb <sb-worktree> --model v2 --out <dir> [IDS ...]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sb_review"))
from export_tables import toulbar2_optimum  # noqa: E402  (our own wrapper of pytoulbar2)

DEV_SET = ["1CRN", "5PTI", "1BPI", "1PGA", "2IGD", "1UBQ"]
SCALE_BITS = 20
_COMMON = dict(eps0=4.0, e_clip=1000.0, max_states_per_site=None, seed=0)
MODELS = {"v2": dict(_COMMON, include_native=True, hydrogens="ideal"),
          "v2-lib": dict(_COMMON, include_native=False, hydrogens="ideal")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sb", type=Path, required=True)
    ap.add_argument("--model", choices=sorted(MODELS), required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--no-toulbar2", action="store_true")
    ap.add_argument("ids", nargs="*", default=DEV_SET)
    args = ap.parse_args()
    sys.path.insert(0, str(args.sb / "src"))
    from metricchain_sb.model import PairModel
    from metricchain_sb.molecular import build_energy_tables
    args.out.mkdir(parents=True, exist_ok=True)
    summary = []
    for pdb_id in args.ids:
        t0 = time.perf_counter()
        tables = build_energy_tables(str(args.sb / "benchmarks" / "structbio" / "pdb" / f"{pdb_id}.pdb"), **MODELS[args.model])
        model = PairModel.from_float(tables.unary, tables.pair, scale_bits=SCALE_BITS)
        t_build = time.perf_counter() - t0
        arrays = {"scale_bits": np.array(model.scale_bits, dtype=np.int64), "n": np.array(model.n, dtype=np.int64),
                  "pairs": np.array(sorted(model.pair), dtype=np.int64).reshape(-1, 2)}
        for i, u in enumerate(model.unary):
            arrays[f"u{i}"] = np.asarray(u, dtype=np.int64)
        for (i, j), t in model.pair.items():
            arrays[f"p{i}_{j}"] = np.asarray(t, dtype=np.int64)
        np.savez_compressed(args.out / f"{pdb_id}.npz", **arrays)
        row = dict(pdb_id=pdb_id, model=args.model, sites=model.n, states_total=sum(model.sizes), states_max=max(model.sizes),
                   pairs=len(model.pair), seconds_build=round(t_build, 2))
        if not args.no_toulbar2:
            opt, sol, t_tb = toulbar2_optimum([np.asarray(u, dtype=np.int64) for u in model.unary],
                                             {k: np.asarray(t, dtype=np.int64) for k, t in model.pair.items()}, 0)
            row.update(toulbar2_optimum_int=opt, toulbar2_solution=sol, toulbar2_seconds=round(t_tb, 3))
        summary.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != "toulbar2_solution"}), flush=True)
    (args.out / "export_summary.json").write_text(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
