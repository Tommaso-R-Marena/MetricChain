"""X-005b: the adversarial search of X-005 with the placement-free upper bound as objective.

For each (u, n, phi) of the grid with n <= --nmax: the same searches as job M-008 (two profile
families, two inner behaviours, the same budgets and seed), but maximising the upper bound on the
evaluations of *every* instance with a given law of fibre averages, whatever the places of its fibres
in their trivial brackets (``Search`` objective "cost_any_placement").  Run locally in a process pool.

    python experiments/eng/twolevel/run_anyplacement.py --nmax 4000 --workers 4
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

import run_search  # noqa: E402

OUT = Path(__file__).resolve().parent / "results" / "x005_anyplacement.jsonl"


def work(task: dict) -> dict:
    return run_search.cell(**task)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=4000)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    done = set()
    if OUT.exists():
        for line in OUT.read_text().splitlines():
            r = json.loads(line)
            done.add((r["u"], r["n"], r["phi"]))
    tasks = [dict(u=u, n=n, phi=phi, budget=4000, budget_general=2000, seed=1, objectives=("cost_any_placement",))
             for u in run_search.US for n in run_search.NS_COST if n <= args.nmax for phi in run_search.PHIS if (u, n, phi) not in done]
    tasks.sort(key=lambda t: -t["n"] * t["u"])
    print(f"{len(tasks)} cells to do ({len(done)} stored), commit {commit[:7]}", flush=True)
    t0 = time.time()
    with mp.Pool(args.workers) as pool, OUT.open("a") as fh:
        for k, r in enumerate(pool.imap_unordered(work, tasks), 1):
            r.update(commit=commit, job="local")
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            if k % 12 == 0 or k == len(tasks):
                print(f"[{k}/{len(tasks)}] {time.time() - t0:.0f} s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
