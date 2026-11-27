"""Nesting depth at the structural-biology division's later commits (the format writes chains of eliminations flat):
produce certificates with thousands of eliminations and serialise, convert and reload them in an interpreter with the
default recursion limit.

    python -B experiments/eng/sb_review/depth_head.py --sb <checkout> --out FILE
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
    rng = random.Random(3)
    rows = []
    for n, k in ((20, 20), (40, 30), (60, 30), (120, 40)):
        unary = [np.array([0] + [rng.randint(50, 90) for _ in range(k - 1)]) for _ in range(n)]
        pair = {(i, i + 1): np.array([[rng.randint(-3, 3) for _ in range(k)] for _ in range(k)]) for i in range(n - 1)}
        cert = certify_gmec(PairModel(unary=unary, pair=pair))
        counts = mincert.count_nodes(cert.root)
        row = dict(sites=n, states=k, accepted_in_memory=bool(check_min_certificate(cert).accepted), prune=counts["prune"], depth=counts["depth"])
        text = None
        for name, fn in (("dumps", lambda: mincert.dumps(cert)), ("to_metricchain_cert1", lambda: mincert.to_metricchain_cert1(cert))):
            try:
                v = fn()
                row[name] = "ok"
                text = v if name == "dumps" else text
            except Exception as exc:  # noqa: BLE001
                row[name] = type(exc).__name__
        if text is not None:
            try:
                row["loads"] = "ok, accepted" if check_min_certificate(mincert.loads(text)).accepted else "ok, rejected"
                row["bytes"] = len(text)
            except Exception as exc:  # noqa: BLE001
                row["loads"] = type(exc).__name__
        rows.append(row)
        print(json.dumps(row), flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(dict(recursion_limit=sys.getrecursionlimit(), rows=rows), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
