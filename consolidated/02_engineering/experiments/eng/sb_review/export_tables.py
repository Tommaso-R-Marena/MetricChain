"""Export the integer instances of the structural-biology division's development set, so that they can be checked by
code that shares nothing with theirs.

This script runs THEIR builder (``metricchain_sb.molecular.build_energy_tables`` and ``PairModel.from_float``, with the
parameters of their driver ``experiments/structbio/gmec_dev/run.py``) from a copy of their tree, in an environment with
their pinned dependencies, and writes one numpy archive per structure: ``scale_bits``, ``n``, ``pairs``, ``u<i>``,
``p<i>_<j>`` (int64).  Whether those tables are the stated energy function is their claim K5 and is not tested here;
what is tested downstream is everything that is claimed *about* the tables.

    <their python> experiments/eng/sb_review/export_tables.py --sb <copy of their tree> --out <directory> [IDS ...]

It also solves each instance with toulbar2 through a wrapper of ours (not theirs) and stores the optimum.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

DEV_SET = ["1CRN", "5PTI", "1BPI", "1PGA", "2IGD", "1UBQ"]
SCALE_BITS = 20
MODEL_PARAMS = dict(eps0=4.0, e_clip=1000.0, max_states_per_site=None, include_native=True, seed=0)   # as in their driver


def toulbar2_optimum(unary, pair, ub: int):
    """Our own call of pytoulbar2 on the integer instance (costs shifted to be nonnegative, as the solver needs)."""
    import pytoulbar2
    n = len(unary)
    shift_u = [int(min(u)) for u in unary]
    shift_p = {k: int(t.min()) for k, t in pair.items()}
    top = int(sum(int(max(u)) - s for u, s in zip(unary, shift_u)) + sum(int(t.max()) - shift_p[k] for k, t in pair.items())) + 1
    cfn = pytoulbar2.CFN(top)
    for i, u in enumerate(unary):
        cfn.AddVariable(f"x{i}", range(len(u)))
    for i, u in enumerate(unary):
        cfn.AddFunction([i], [int(v) - shift_u[i] for v in u])
    for (i, j), t in pair.items():
        cfn.AddFunction([i, j], [int(v) - shift_p[(i, j)] for v in t.reshape(-1)])
    t0 = time.perf_counter()
    res = cfn.Solve(showSolutions=0)
    dt = time.perf_counter() - t0
    if not res:
        return None, None, dt
    sol = [int(a) for a in res[0]]
    return int(res[1]) + sum(shift_u) + sum(shift_p.values()), sol, dt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sb", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("ids", nargs="*", default=DEV_SET)
    args = ap.parse_args()
    sys.path.insert(0, str(args.sb / "src"))
    from metricchain_sb.model import PairModel
    from metricchain_sb.molecular import build_energy_tables
    args.out.mkdir(parents=True, exist_ok=True)
    summary = []
    for pdb_id in args.ids:
        t0 = time.perf_counter()
        tables = build_energy_tables(str(args.sb / "benchmarks" / "structbio" / "pdb" / f"{pdb_id}.pdb"), **MODEL_PARAMS)
        model = PairModel.from_float(tables.unary, tables.pair, scale_bits=SCALE_BITS)
        t_build = time.perf_counter() - t0
        arrays = {"scale_bits": np.array(model.scale_bits, dtype=np.int64), "n": np.array(model.n, dtype=np.int64),
                  "pairs": np.array(sorted(model.pair), dtype=np.int64).reshape(-1, 2)}
        for i, u in enumerate(model.unary):
            arrays[f"u{i}"] = np.asarray(u, dtype=np.int64)
        for (i, j), t in model.pair.items():
            arrays[f"p{i}_{j}"] = np.asarray(t, dtype=np.int64)
        np.savez_compressed(args.out / f"{pdb_id}.npz", **arrays)
        opt, sol, t_tb = toulbar2_optimum([np.asarray(u, dtype=np.int64) for u in model.unary],
                                         {k: np.asarray(t, dtype=np.int64) for k, t in model.pair.items()}, 0)
        row = dict(pdb_id=pdb_id, sites=model.n, states_total=sum(model.sizes), states_max=max(model.sizes), pairs=len(model.pair),
                   seconds_build=round(t_build, 2), toulbar2_optimum_int=opt, toulbar2_solution=sol, toulbar2_seconds=round(t_tb, 3))
        summary.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != "toulbar2_solution"}), flush=True)
    (args.out / "export_summary.json").write_text(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
