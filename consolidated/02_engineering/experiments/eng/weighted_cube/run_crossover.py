"""Where does the block bound of the Markov recursion cross the cube?  (For R10-T2.)

For L in {3, 4} and every p of the grid, and for both exponents (a: capacity per site; h: sup_t F* per site):

* the sign of (block bound - cube) is tabulated on a grid of slopes; every sign change is located by bisection
  in floating point (a NUMERICAL value of the crossing slope of the L-site bound);
* the two slopes with two decimals on either side of the crossing are then CERTIFIED: at the larger one the
  upper bound is below the cube (so the chain's exponent is below the cube's there), at the smaller one the
  certified LOWER end of the block quantity is above the cube (so this block length does not decide there).

Nothing here says that the block bound is monotone in the slope: "below" is certified at the listed slopes only
(and at the grid slopes of run_bounds.py).

Usage (repository root):
    python experiments/eng/weighted_cube/run_crossover.py            # about 20 minutes
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from metricchain_eng.weighted_cube import exponents as EX  # noqa: E402
from run_bounds import P_GRID, compute_cell, load_chambers  # noqa: E402

RES = Path(__file__).resolve().parent / "results"


def block_value(L, chambers, p, u, kind):
    us = EX.ustar(p, u)
    c = next(c for c in chambers if c.contains(Fraction(us / u)))
    prob = EX.BlockProblem(c, p, u)
    if kind == "a":
        return EX.capacity_bound(prob)["upper"] / L
    return EX.h_bound(prob, rel_tol=2e-4)["upper"] / L


def cube_value(u, kind):
    hc, _, ac, _ = EX.cube_exponents(u)
    return ac if kind == "a" else hc


def crossings(L, chambers, p, kind, slopes, tol):
    diff = lambda u: block_value(L, chambers, p, u, kind) - cube_value(u, kind)
    vals = [(u, diff(u)) for u in slopes]
    out = []
    for (u1, d1), (u2, d2) in zip(vals[:-1], vals[1:]):
        if d1 > 0 >= d2 or d1 <= 0 < d2:
            lo, hi, dlo = u1, u2, d1
            while hi - lo > tol:
                mid = 0.5 * (lo + hi)
                dm = diff(mid)
                if (dm > 0) == (dlo > 0):
                    lo, dlo = mid, dm
                else:
                    hi = mid
            out.append(dict(between=[u1, u2], crossing=0.5 * (lo + hi), direction="down" if d1 > 0 else "up"))
    return out, vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, nargs="+", default=[3, 4])
    ap.add_argument("--p", type=str, nargs="*", default=P_GRID)
    ap.add_argument("--kinds", type=str, nargs="*", default=["a", "h"])
    args = ap.parse_args()
    slopes = {"a": [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0],
              "h": [1.0, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0]}
    out = dict(note="crossing = floating-point bisection (numerical); certified = interval arithmetic at the two "
                    "neighbouring slopes with two decimals", rows=[])
    t_all = time.time()
    for L in args.L:
        chambers, _ = load_chambers(L)
        expanded = {}
        for p_str in args.p:
            p = float(Fraction(p_str))
            for kind in args.kinds:
                t0 = time.time()
                cr, vals = crossings(L, chambers, p, kind, slopes[kind], 2e-4 if kind == "a" else 2e-3)
                row = dict(L=L, p=p_str, kind=kind, sign_table=[[u, "above" if d > 0 else "below"] for u, d in vals],
                           crossings=[])
                for c in cr:
                    u_c = c["crossing"]
                    if c["direction"] == "down":
                        u_minus, u_plus = math.floor(u_c * 100) / 100, math.ceil(u_c * 100) / 100
                    else:
                        u_minus, u_plus = math.ceil(u_c * 100) / 100, math.floor(u_c * 100) / 100
                    cert = {}
                    for name, uu in (("not_decided_at", u_minus), ("below_at", u_plus)):
                        cell = compute_cell(L, chambers, p_str, f"{uu:.2f}", expanded, do_h=(kind == "h"))
                        q = cell[kind]
                        cert[name] = dict(u=f"{uu:.2f}", lower=q["lower"], upper=q["upper"], cube_lo=cell["cube"][kind + "_lo"],
                                          cube_hi=cell["cube"][kind + "_hi"], below_cube=q["below_cube"],
                                          lower_end_above_cube=bool(float(q["lower"]) > float(cell["cube"][kind + "_hi"])))
                    row["crossings"].append(dict(numerical_crossing=round(u_c, 4), direction=c["direction"], **cert))
                row["seconds"] = round(time.time() - t0, 1)
                out["rows"].append(row)
                print(json.dumps(row), flush=True)
    out["seconds_total"] = round(time.time() - t_all, 1)
    (RES / "crossover.json").write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", (RES / "crossover.json").relative_to(ROOT))


if __name__ == "__main__":
    main()
