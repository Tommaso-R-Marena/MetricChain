"""X-011e: are cone fibres of *intermediate* slope harder than those of full slope for the designs chosen by
certified cost?  The designs of X-011b at their selected outer fractions, the worst outer landscape searched as
there, fibres = cones of slope s u for s in (0.25, 0.5, 0.75); readings (B) and (A).

    python experiments/eng/twolevel/fibre_slopes.py [--procs 3]      # appends to results/x011_fibre_slopes.jsonl
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import nested_bench as nb  # noqa: E402

CELLS = [(4000, 2, 0.35), (4000, 3, 0.30), (16000, 2, 0.30)]        # (n, nested levels, outer fraction): the selected designs
SLOPES = (0.25, 0.5, 0.75)


def run(kw):
    b, bg = nb.BUDGETS.get(kw["n"], nb.BUDGET_LARGE)
    return nb.instance_cell(1.0, kw["n"], kw["phi"], "theory", kw["k"], readings=("B", "A"), slope=kw["slope"], budget=b, budget_general=bg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--procs", type=int, default=3)
    args = ap.parse_args()
    out = ROOT / "experiments" / "eng" / "twolevel" / "results" / "x011_fibre_slopes.jsonl"
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            done.add((r["n"], r["nested_levels"], r["phi"], r["slope"]))
    todo = [dict(n=n, k=k, phi=phi, slope=s) for (n, k, phi) in CELLS for s in SLOPES if (n, k, phi, s) not in done]
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    with Pool(args.procs) as pool, out.open("a") as fh:
        for r in pool.imap_unordered(run, todo):
            r["commit"] = commit
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            print(f"n={r['n']} levels={r['nested_levels'] + 1} phi={r['phi']} fibre slope {r['slope']}: (B, cone) {r['worst_B']:.4f}  (A) {r['worst_A']:.4f}  "
                  f"flat instance {r['flat_instance']:.4f} certified {r['certified']:.4f}  [{r['seconds']:.0f} s]", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
