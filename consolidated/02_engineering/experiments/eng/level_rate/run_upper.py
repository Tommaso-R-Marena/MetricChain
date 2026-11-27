"""Method (a2): rigorous upper bounds of tau_k from convex majorants of the level recursion.

    python experiments/eng/level_rate/run_upper.py <case> [--N 16000] [--K 160]

writes results/upper_<case>_N<N>.json: for k = 1..K the value M_k(0) >= tau_k, with the diagnostics of every
level (number of nodes at which the new majorant is not below the old one -- zero means R1[M_k] <= M_k on the
grid --, number of hull vertices, seconds).  One process, one thread; about 1 to 2 seconds per level.

What is an upper bound and why: see the docstring of lr_recursion.py.  The numbers are floating-point
evaluations of a quantity that is an upper bound in exact arithmetic; a margin of 1e-13 a per level is added
for rounding (no interval arithmetic).
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


def run(case: str, N: int, K: int, eps0: float = 0.02, n_theta: int = 1_000_000, profile_ks=()) -> dict:
    t0 = time.time()
    pair = C.make(case)
    ub = R.ConvexUpperBound(pair, N=N, eps0=eps0, n_theta=n_theta)
    h = float(pair.h)
    prof = {}
    while ub.k < K:
        old = ub.M.copy()
        rec = ub.step()
        # nodes at which the level changed nothing (the recursion has reached its fixed point there)
        rec["n_unchanged"] = int(np.sum(ub.M[:-1] >= old[:-1] - 1e-13 * ub.a))
        rec["x_first_unchanged_over_E"] = float(ub.x[int(np.argmax(ub.M >= old - 1e-13 * ub.a))] / ub.E)
        if ub.k in profile_ks:
            # the majorant at a few accuracies, for the comparison with the lines
            prof[str(ub.k)] = dict(x=[float(v) for v in ub.x[:: max(1, N // 40)]],
                                   M=[float(v) for v in ub.M[:: max(1, N // 40)]])
    out = dict(case=case, name=pair.name, pinned_theory_commit=C.PINNED, N=N, K=K, eps0=eps0, n_theta=n_theta,
               fp_margin_per_level=ub.fp_margin, a=ub.a, E=ub.E, h=h,
               tau_upper={str(r["k"]): repr(r["tau"]) for r in ub.history},
               levels=[{k: v for k, v in r.items() if k != "tau"} for r in ub.history[1:]],
               n_above_total=int(sum(r.get("n_above", 0) for r in ub.history)),
               profiles=prof, seconds=time.time() - t0,
               status="upper bound of tau_k (exact arithmetic); floating point with a margin, not interval arithmetic")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("--N", type=int, default=16000)
    ap.add_argument("--K", type=int, default=160)
    ap.add_argument("--eps0", type=float, default=0.02)
    args = ap.parse_args(argv)
    res = run(args.case, args.N, args.K, args.eps0, profile_ks=(3, 10, 40))
    path = C.dump(f"upper_{args.case}_N{args.N}.json", res)
    k = str(args.K)
    print(f"{args.case} N={args.N}: tau_{k} <= {res['tau_upper'][k]}  n_above={res['n_above_total']} "
          f"({res['seconds']:.0f} s) -> {path.name}", flush=True)


if __name__ == "__main__":
    main()
