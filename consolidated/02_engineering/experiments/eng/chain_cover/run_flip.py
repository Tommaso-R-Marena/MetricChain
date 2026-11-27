#!/usr/bin/env python3
"""THY-REQ-0002 question 3(b): single-flip constants of the profile distance on lattice chains,
and the exhaustive test whether they are a valid torsion-Hamming envelope.

For every chain length with a class table (``data/dia_Sc12_n<n>.txt``) and a mode-A output of
``build/dia_flip`` (``data/flip/dia_Sc12_flipA_n<n>.txt``; created with ``--run``):

* ``c_sf[j]`` = largest ``||N^x - N^x'||_1`` over pairs of self-avoiding conformations that
  differ in torsion ``j`` only;
* ``Dmax`` = largest profile distance between any two conformations (from the class table);
* mode B of ``dia_flip``: all pairs of conformations differing exactly on a set ``T`` of torsions
  with ``sum_{j in T} c_sf[j] < Dmax`` are enumerated (every other pair satisfies the envelope
  inequality trivially), and ``||N^x - N^y||_1 <= sum_{j in T} c_sf[j]`` is tested for each.

Published value used as a check (P_REPORT section 3.3, n = 12):
``c/L = (52, 85, 92, 108, 114, 114, 114, 114, 108, 92, 85, 52)``.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.chains.profile_cover import parse_enum_output  # noqa: E402

PUBLISHED_C12 = [52, 85, 92, 108, 114, 114, 114, 114, 108, 92, 85, 52]
BIN = ROOT / "build" / "dia_flip"


def read_mode_a(path: Path):
    rows = [[int(t) for t in ln.split()] for ln in path.read_text().splitlines() if ln and not ln.startswith("#")]
    c = [r[1] for r in rows]
    inside = [r[2] for r in rows]
    outside = [r[3] for r in rows]
    return c, inside, outside


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nmin", type=int, default=3)
    ap.add_argument("--nmax", type=int, default=14)
    ap.add_argument("--run", action="store_true", help="run build/dia_flip for missing mode-A outputs")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    (HERE / "data" / "flip").mkdir(parents=True, exist_ok=True)
    (HERE / "results").mkdir(exist_ok=True)
    rows, bad = [], []
    for n in range(args.nmin, args.nmax + 1):
        a_path = HERE / "data" / "flip" / f"dia_Sc12_flipA_n{n}.txt"
        t_path = HERE / "data" / f"dia_Sc12_n{n}.txt"
        if not t_path.exists():
            continue
        if not a_path.exists():
            if not args.run:
                continue
            a_path.write_text(subprocess.run([str(BIN), "-n", str(n)], check=True, capture_output=True, text=True).stdout)
        c, inside, outside = read_mode_a(a_path)
        tab = parse_enum_output(t_path.read_text())
        dmax = int(tab.l1_matrix().max())
        out = subprocess.run([str(BIN), "-n", str(n), "-c", ",".join(map(str, c)), "-D", str(dmax)],
                             check=True, capture_output=True, text=True).stdout
        stats = dict(tok.split("=") for tok in [ln for ln in out.splitlines() if ln.startswith("# sets=")][0][2:].split())
        m = (n + 1) // 2                                        # distance from the nearer end: 1 .. m
        dist_end = np.array([min(j + 1, n - j) for j in range(n)])
        slope, intercept = np.polyfit(dist_end, np.array(c, dtype=float), 1) if n >= 4 else (float("nan"), float("nan"))
        row = {"n_torsions": n, "n_beads": n + 3, "c_sf": c, "symmetric": c == c[::-1],
               "monotone_to_centre": all(c[j] <= c[j + 1] for j in range(m - 1)),
               "end_constant": c[0], "centre_constant": c[(n - 1) // 2],
               "linear_fit_slope_per_torsion": round(float(slope), 3), "linear_fit_intercept": round(float(intercept), 3),
               "fraction_of_flips_leaving_domain": [round(o / (i + o), 4) for i, o in zip(inside, outside)],
               "Dmax": dmax, "sets_with_budget_below_Dmax": int(stats["sets"]),
               "pairs_checked": int(stats["pairs_checked"]), "pairs_violating": int(stats["pairs_violating"]),
               "worst_excess": int(stats["worst_excess"]),
               "valid_hamming_envelope": int(stats["pairs_violating"]) == 0}
        rows.append(row)
        print(f"n={n:2d} c_sf={c}  Dmax={dmax}  sets={row['sets_with_budget_below_Dmax']} pairs={row['pairs_checked']} "
              f"violations={row['pairs_violating']} worst_excess={row['worst_excess']}  valid_envelope={row['valid_hamming_envelope']}",
              flush=True)
        if n == 12 and c != PUBLISHED_C12:
            bad.append((n, "c_sf", c, PUBLISHED_C12))
        if not row["symmetric"]:
            bad.append((n, "c_sf not symmetric under chain reversal", c, None))
    if not args.check:
        out_path = HERE / "results" / "lattice_Sc12_flip.json"
        out_path.write_text(json.dumps({"model": "diamond lattice, self-avoiding, homopolymer", "s_cut": 12,
                                        "rows": rows}, indent=1) + "\n")
        print(f"wrote {out_path.relative_to(ROOT)}")
    for b in bad:
        print("MISMATCH:", b)
    if args.check:
        print("CHECK", "FAILED" if bad else "PASSED")
    return 1 if (bad and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
