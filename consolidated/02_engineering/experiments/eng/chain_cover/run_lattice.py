#!/usr/bin/env python3
"""THY-REQ-0002, lattice part: covering numbers and entropy of profile sets of diamond-lattice chains.

Reads the class tables written by ``build/dia_enum`` (``data/dia_Sc<cut>_n<n>.txt``; regenerate
with ``--enumerate``), and computes for every chain length

* ``N^P_cov(L, eps)`` -- exact minimum cover in the profile format (known part ``#gauche``,
  zero residual), for ``L in {1, 1/5}`` and ``eps in {0, 1, eps1*N : eps1 in {1/20, 1/10, 1/4, 1/2}}``;
* the entropy numbers of the profile set in the normalised metric ``||N^x - N^y||_1 / N``:
  ``m(delta)`` of a farthest-point traversal started at the all-trans class (the quantity of
  P_REPORT section 3.2) and a bracket [LP bound, verified cover] of the internal covering number
  at closed radius ``delta*N`` (exact when the two ends coincide).

``--check`` re-derives the published values of P_REPORT section 3.3 (n = 5..12) and fails if any
differs.  Results are written to ``results/lattice_Sc<cut>.json``.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.chains.lattice_analysis import (  # noqa: E402
    DELTAS, analyse_table, format_row, merge_rows)
from metricchain_eng.chains.profile_cover import parse_enum_output  # noqa: E402

# P_REPORT section 3.3 (diamond lattice, S_c = 12, homopolymer, zero residual), columns
# (L=1, eps=0), (L=1, eps=N/2), (L=1/5, eps=0); section 3.2 for the class counts.
PUBLISHED_COVER = {5: (5, 3, 2), 6: (6, 5, 2), 7: (10, 5, 2), 8: (10, 5, 2), 9: (13, 5, 3),
                   10: (16, 7, 3), 11: (19, 7, 4), 12: (21, 8, 4)}
PUBLISHED_CONFS = {5: 233, 6: 683, 7: 2005, 8: 5849, 9: 17107, 10: 49833, 11: 145379, 12: 422825,
                   13: 1231221}
PUBLISHED_CLASSES = {5: 22, 6: 37, 7: 57, 8: 90, 9: 129, 10: 190, 11: 258, 12: 356, 13: 479}
# P_REPORT section 3.2: m(4), m(2), m(1), m(0.5), m(0.25) of a farthest-point traversal
PUBLISHED_M = {8: (2, 3, 7, 14, 31), 10: (3, 5, 11, 25, 55), 11: (3, 5, 11, 26, 73),
               12: (3, 5, 10, 34, 96), 13: (3, 5, 12, 34, 88)}



def load(n: int, s_cut: int):
    path = HERE / "data" / f"dia_Sc{s_cut}_n{n}.txt"
    return parse_enum_output(path.read_text()) if path.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cut", type=int, default=12, help="squared-distance cutoff S_c (default 12)")
    ap.add_argument("--nmin", type=int, default=5)
    ap.add_argument("--nmax", type=int, default=18)
    ap.add_argument("--enumerate", action="store_true", help="(re)run build/dia_enum for missing class tables")
    ap.add_argument("--solvers", default="highs,cpsat")
    ap.add_argument("--no-exact-nets", action="store_true")
    ap.add_argument("--net-time-limit", type=float, default=30.0, help="seconds of HiGHS per net (default 30)")
    ap.add_argument("--check", action="store_true", help="re-derive the published values and exit non-zero on a mismatch")
    args = ap.parse_args()
    solvers = tuple(args.solvers.split(","))
    (HERE / "data").mkdir(exist_ok=True)
    (HERE / "results").mkdir(exist_ok=True)

    rows, bad, notes = [], [], []
    for n in range(args.nmin, args.nmax + 1):
        if load(n, args.cut) is None:
            if not args.enumerate:
                print(f"n={n}: no class table (run with --enumerate)", file=sys.stderr)
                continue
            out = subprocess.run([str(ROOT / "build" / "dia_enum"), "-n", str(n), "-c", str(args.cut)],
                                 check=True, capture_output=True, text=True).stdout
            (HERE / "data" / f"dia_Sc{args.cut}_n{n}.txt").write_text(out)
        row = analyse_table(load(n, args.cut), solvers, exact_nets=not args.no_exact_nets,
                            net_time_limit=args.net_time_limit)
        rows.append(row)
        c = row["cover"]
        print(format_row(row), flush=True)
        c = row["cover"]
        if args.cut == 12:
            if n in PUBLISHED_CONFS and row["conformations"] != PUBLISHED_CONFS[n]:
                bad.append((n, "conformations", row["conformations"], PUBLISHED_CONFS[n]))
            if n in PUBLISHED_CLASSES and row["classes"] != PUBLISHED_CLASSES[n]:
                bad.append((n, "classes", row["classes"], PUBLISHED_CLASSES[n]))
            if n in PUBLISHED_COVER:
                got = (c["L=1,eps=0"]["N_cov"], c["L=1,eps=1/2*N"]["N_cov"], c["L=1/5,eps=0"]["N_cov"])
                if got != PUBLISHED_COVER[n]:
                    bad.append((n, "cover", got, PUBLISHED_COVER[n]))
            if n in PUBLISHED_M:
                # m(delta) depends on the start and on the tie-breaking of the traversal, which the
                # workstream report does not specify: a difference here is reported, not counted
                got = tuple(row["entropy"][f"delta={d}"]["m_fpt"] for d in DELTAS)
                if got != PUBLISHED_M[n]:
                    notes.append((n, "m(delta) of the farthest-point traversal (start/tie-break dependent)",
                                  got, PUBLISHED_M[n]))
        if not all(v["proved_optimal"] for v in c.values()):
            bad.append((n, "optimality not proved by all solvers", None, None))
    out = HERE / "results" / f"lattice_Sc{args.cut}.json"
    if not args.check:
        merge_rows(out, rows, args.cut)
        print(f"wrote {out.relative_to(ROOT)}")
    for b in bad:
        print("MISMATCH:", b)
    for b in notes:
        print("NOTE:", b)
    if args.check:
        print("CHECK", "FAILED" if bad else "PASSED")
    return 1 if (bad and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
