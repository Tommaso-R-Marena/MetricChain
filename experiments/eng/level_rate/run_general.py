"""Method (a1): the level recursion on a grid with no structural assumption (a plain numerical approximation).

    python experiments/eng/level_rate/run_general.py <case> [--N 1000] [--K 40]

writes results/general_<case>_N<N>.json: tau_k for k = 1..K and, level by level, the diagnostics that say
whether the structure used by the upper-bound scheme (run_upper.py) is seen in the unconstrained computation:
* is S(x) = x + T_k(x) quasi-convex at the nodes, is T_k convex at the nodes (largest concave corner);
* among the nodes that improved, the fraction whose best point lies in "regime 2" (x_lo > x_hi);
* the structure-free search (dense grid in (logit phi, logit beta/g) + refinement) against the search along
  the balance curve: how much lower the former ever gets (it should never be lower by more than the
  interpolation error), and how much it misses (narrow valleys).
When ``--compare`` is given the convex upper bound is run on the same grid and the largest and smallest
difference of the nodal values is recorded level by level.

About 7 s per level at N = 1000, 14 s at N = 2000 (one thread).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lr_cases as C  # noqa: E402
import lr_recursion as R  # noqa: E402
import numpy as np  # noqa: E402


def run(case: str, N: int, K: int, compare: bool, n_theta: int = 1_000_000) -> dict:
    t0 = time.time()
    pair = C.make(case)
    th = R.build_theta(pair, n_theta)
    gen = R.GeneralRecursion(pair, N=N, theta=th)
    ub = R.ConvexUpperBound(pair, N=N, theta=th) if compare else None
    cmp_rows = []
    while gen.k < K:
        gen.step()
        if ub is not None:
            ub.step()
            d = (gen.T - ub.M) / gen.a
            cmp_rows.append(dict(k=gen.k, general_minus_upper_min_over_a=float(d.min()),
                                 general_minus_upper_max_over_a=float(d.max()),
                                 tau_general=repr(float(gen.T[0])), tau_upper=repr(float(ub.M[0]))))
    out = dict(case=case, name=pair.name, pinned_theory_commit=C.PINNED, N=N, K=K, n_theta=n_theta,
               a=gen.a, E=gen.E, h=float(pair.h),
               tau={str(r["k"]): repr(r["tau"]) for r in gen.history},
               levels=[{k: v for k, v in r.items() if k != "tau"} for r in gen.history[1:]],
               comparison_with_upper_bound_same_grid=cmp_rows, seconds=time.time() - t0,
               status="plain numerical approximation (linear interpolation in sqrt(x)); not a bound")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("--N", type=int, default=1000)
    ap.add_argument("--K", type=int, default=40)
    ap.add_argument("--compare", action="store_true")
    args = ap.parse_args(argv)
    res = run(args.case, args.N, args.K, args.compare)
    path = C.dump(f"general_{args.case}_N{args.N}.json", res)
    print(f"{args.case} N={args.N}: tau_{args.K} ~ {res['tau'][str(args.K)]} ({res['seconds']:.0f} s) -> {path.name}",
          flush=True)


if __name__ == "__main__":
    main()
