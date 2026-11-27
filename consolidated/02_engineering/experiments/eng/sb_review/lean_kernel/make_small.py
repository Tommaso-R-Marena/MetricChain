"""Small instances with certificates from the structural-biology division's producer, for the run of the
machine-checked kernel (``RunKernel.lean``): chains whose certificates are one chain of eliminations of a chosen
length (to time the kernel against the number of eliminations), and frustrated dense instances whose certificates
branch and carry messages.

Run with the structural-biology division's interpreter and a copy of its tree:

    <their python> experiments/eng/sb_review/lean_kernel/make_small.py --sb <copy of their tree> --out DIR
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sb", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    sys.path.insert(0, str(args.sb.expanduser() / "src"))
    from metricchain_sb import mincert
    from metricchain_sb.gmec import certify_gmec
    from metricchain_sb.mincheck import check_min_certificate
    from metricchain_sb.model import PairModel
    args.out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(17)
    cases = []
    for n in (3, 4, 5, 6, 7, 8, 9, 10, 12):                      # chains: n sites of 4 states, one cheap state each
        k = 4
        unary = [np.array([0] + [rng.randint(50, 90) for _ in range(k - 1)]) for _ in range(n)]
        pair = {(i, i + 1): np.array([[rng.randint(-3, 3) for _ in range(k)] for _ in range(k)]) for i in range(n - 1)}
        cases.append((f"chain{n:02d}", unary, pair))
    for idx, (n, k) in enumerate(((5, 3), (6, 3), (6, 4), (7, 3))):   # dense, frustrated: every pair penalises agreement and near-agreement
        unary = [np.array([rng.randint(0, 2) for _ in range(k)]) for _ in range(n)]
        pair = {(i, j): np.array([[rng.randint(5, 9) if a == b else rng.randint(0, 4) for b in range(k)] for a in range(k)])
                for i in range(n) for j in range(i + 1, n)}
        cases.append((f"dense{idx}", unary, pair))
    rows = []
    for name, unary, pair in cases:
        model = PairModel(unary=unary, pair=pair)
        cert = certify_gmec(model)
        res = check_min_certificate(cert)
        counts = mincert.count_nodes(cert.root)
        (args.out / f"{name}.mincert.json").write_text(mincert.dumps(cert, include_model=False))
        arrays = {"scale_bits": np.array(model.scale_bits, dtype=np.int64), "n": np.array(model.n, dtype=np.int64),
                  "pairs": np.array(sorted(model.pair), dtype=np.int64).reshape(-1, 2)}
        for i, u in enumerate(model.unary):
            arrays[f"u{i}"] = np.asarray(u, dtype=np.int64)
        for (i, j), t in model.pair.items():
            arrays[f"p{i}_{j}"] = np.asarray(t, dtype=np.int64)
        np.savez_compressed(args.out / f"{name}.npz", **arrays)
        row = dict(name=name, sites=model.n, states=max(model.sizes), pairs=len(model.pair), accepted=bool(res.accepted),
                   full_box=bool(res.full_box), lower_bound=str(res.lower_bound), leaf=counts["leaf"], branch=counts["branch"], prune=counts["prune"])
        rows.append(row)
        print(json.dumps(row), flush=True)
    (args.out / "small_summary.json").write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
