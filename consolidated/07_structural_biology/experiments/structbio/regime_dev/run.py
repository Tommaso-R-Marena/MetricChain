#!/usr/bin/env python3
"""Experiment SB-X-008 — which regime are the development instances in?  (exploratory measurement)

Asked for by the Complexity division (COMPLEXITY-RES-0010): "The quantity that decides the regime of
an instance is max_i beta c_i, not beta sum_e o_e; your table gives the second."  For the weighted
library-only tables of model v2 (the object of capability C2), after thermal dead-end elimination
with margin TAU, every pair is fitted by a row-plus-column sum and the oscillation `o_e` of the rest
is computed; a pair is "weak" at threshold theta if `o_e <= theta`.  Reported per structure and theta:

  beta * sum_e o_e          the first-order width our relaxation loses (nats),
  max_i beta * c_i          with c_i = sum of o_e over the weak pairs that contain site i,
  (beta^2 / 8) sum_i c_i^2  what a site-wise second-order bound would give AT BEST (product reference,
                            unit influence) — an indicator only: no such bound is implemented or certified here,
  the pairs kept exact and the largest table of the elimination order found for them.

Nothing here is certified; these are properties of the integer tables computed in floating point.

    python experiments/structbio/regime_dev/run.py
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from fractions import Fraction

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "structbio" / "gmec_dev"))

import run as dev  # noqa: E402
from metricchain_sb.partition import _node_steps, _State, _to_int, plan_order, weighted_model  # noqa: E402

BETA = Fraction(1000, 593)
TAU = 12.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=list(dev.DEV_SET))
    ap.add_argument("--model", default="v2-lib")
    ap.add_argument("--thetas", type=float, nargs="*", default=[1.0, 0.1, 0.01])
    args = ap.parse_args()
    with open(HERE / "results.jsonl", "a") as out:
        for pdb_id in args.ids:
            base, _, tmeta = dev.build_model(pdb_id, args.model)
            model = weighted_model(base, [s["state_shares"] for s in tmeta["sites"]], BETA)
            scale = 2 ** model.scale_bits
            for theta in args.thetas:
                st = _State(model, model.full_domains())
                steps = _node_steps(st, None, _to_int(TAU, scale), _to_int(theta, scale))
                replay = _State(model, model.full_domains())
                c = np.zeros(model.n)
                total, weak = 0.0, 0
                for step in steps:
                    if step["op"] == "prune":
                        replay.D[step["site"]].remove(step["remove"])
                    else:
                        i, j = step["pair"]
                        table = replay.J.pop((i, j))
                        f, g = np.asarray(step["f"], dtype=np.int64), np.asarray(step["g"], dtype=np.int64)
                        rest = table[np.ix_(replay.D[i], replay.D[j])] - f[replay.D[i]][:, None] - g[replay.D[j]][None, :]
                        o = float(rest.max() - rest.min()) / scale
                        c[i] += o
                        c[j] += o
                        total += o
                        weak += 1
                sizes = {i: len(st.D[i]) for i in range(st.n)}
                _, largest = plan_order(sizes, set(st.J), None)
                beta = float(BETA)
                row = {"experiment": "SB-X-008", "kind": "exploratory", "split": "development", "pdb_id": pdb_id,
                       "model": args.model, "weighted_by_state_share": True, "commit": dev.git_commit(),
                       "beta_per_kcal": str(BETA), "tau_kcal": TAU, "theta_kcal": theta, "sites": model.n,
                       "states_after_pruning": int(sum(sizes.values())), "states_before": int(sum(model.sizes)),
                       "pairs": len(model.pair), "weak_pairs": weak, "exact_pairs": len(st.J),
                       "beta_sum_o": beta * total, "max_beta_c": beta * float(c.max()),
                       "median_beta_c": beta * float(np.median(c)),
                       "site_wise_second_order_indicator": beta * beta * float((c ** 2).sum()) / 8.0,
                       "largest_table_log10": math.log10(largest) if largest > 0 else None}
                out.write(json.dumps(row, sort_keys=True) + "\n")
                out.flush()
                print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()
                                  if k in ("pdb_id", "theta_kcal", "states_after_pruning", "weak_pairs", "exact_pairs",
                                           "beta_sum_o", "max_beta_c", "median_beta_c",
                                           "site_wise_second_order_indicator", "largest_table_log10")}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
