"""X-010: two and three levels of Algorithm 2L+ on adversarial outer landscapes (THY-RES-0004 §7, first proposal).

For u = 1 and n in {1000, 4000, 16000}, on a grid of outer fractions: ``three_levels.worst_case`` (the flat costs,
the worst outer landscape with flat fibres, the bound with the middle level at its cap).  Local process pool;
the file is appended per cell, so a rerun resumes.

    python experiments/eng/twolevel/run_three_levels.py --n 1000 4000 --workers 4
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import three_levels  # noqa: E402

OUT = Path(__file__).resolve().parent / "results" / "x010_three_levels.jsonl"
PHIS = (0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80)
BUDGETS = {1000: (4000, 2000), 4000: (4000, 2000), 16000: (2500, 1250)}


def tasks(ns, u=1.0, seed=1) -> list[dict]:
    return [dict(u=u, n=n, phi=phi, budget=BUDGETS[n][0], budget_general=BUDGETS[n][1], seed=seed) for n in ns for phi in PHIS]


def work(task: dict) -> dict:
    t0 = time.time()
    r = three_levels.worst_case(**task)
    r["seconds"] = time.time() - t0
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="*", default=[1000, 4000])
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    done = set()
    if OUT.exists():
        for line in OUT.read_text().splitlines():
            r = json.loads(line)
            done.add((r["u"], r["n"], r["phi"]))
    todo = [t for t in tasks(args.n) if (t["u"], t["n"], t["phi"]) not in done]
    print(f"{len(todo)} cells to do ({len(done)} stored)", flush=True)
    with mp.Pool(args.workers) as pool, OUT.open("a") as fh:
        for k, r in enumerate(pool.imap_unordered(work, todo), 1):
            r.update(commit=commit, job="local")
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            print(f"[{k}/{len(todo)}] n={r['n']} phi={r['phi']:.2f}: flat2 {r['flat2']:.4f} worst2 {r['worst2']:.4f} | flat3 {r['flat3']:.4f} "
                  f"worst3(flat fibres) {r['worst3_flat_fibres']:.4f} worst3(capped) {r['worst3_capped_middle']:.4f}  ({r['seconds']:.0f} s)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
