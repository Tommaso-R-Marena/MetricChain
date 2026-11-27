#!/usr/bin/env python3
"""Write experiments/ensemble/benchmarks/torus_instances_v1.json: the instances behind Theorem E20b and Propositions
E20c, E20e of docs/ensemble/ENSEMBLE_REPORT.md, in a form that another implementation can read without this code
(for ENSEMBLE-REQ-0001: independent re-implementation by the engineering division).

  * two rational six-tuples on the torus of three angles (coordinates t = tan(phi/2)) with the exact ranks claimed;
  * ten 13-tuples on the torus of four angles (angles in radians, 17 significant digits) with the verdict of
    torus_four_angles.py for each.

Not part of run_all.py (about three minutes).  Public development material, not held-out evidence.
"""
import json
import pathlib

import numpy as np

import torus_four_angles as t4
import torus_six_states as t3

here = pathlib.Path(__file__).resolve().parent
six = [[list(map(str, s)) for s in t3.FIVE] + [list(map(str, t3.SIXTH))],
       [["4", "1", "-1/2"], ["0", "4/5", "-3"], ["0", "1/5", "4/5"], ["-1", "0", "6/5"], ["3/5", "-2", "-1/2"], ["2", "2/5", "2"]]]
out = {"version": 1, "generated_by": "experiments/ensemble/export_torus_instances.py",
       "conventions": {"three angles": "a state is (t1, t2, t3) with t_k = tan(phi_k/2), exact rationals as strings; the data "
                                       "span is { q(t)/prod(1+t_k^2) : q of degree <= 2 in each t_k } (27 functions); the lift is "
                                       "u(t) = (1,t1) x (1,t2) x (1,t3)",
                       "four angles": "a state is (phi1, ..., phi4) in radians; the data span is spanned by the 81 products of "
                                      "1, cos(phi_k), sin(phi_k), one factor per angle"},
       "six_states_three_angles": [{"states_t": inst,
                                    "claim": {"lifts_independent": True, "rank_of_the_twelve_tangential_conditions": 12,
                                              "dimension_of_span_functions_vanishing_on_the_curve": 15,
                                              "verdict": "NOT IDENTIFIED (Theorem E20b)"}} for inst in six],
       "thirteen_states_four_angles": []}
for seed in (0, 1, 2, 3, 10, 11, 12, 13, 14, 15):          # five of each verdict in the stored survey
    rng = np.random.default_rng(seed)
    P = rng.uniform(-np.pi, np.pi, size=(t4.K13, t4.R4))
    o = t4.analyse(seed)
    entry = {"seed": seed, "states_phi": [[repr(float(v)) for v in p] for p in P],
             "claim": {"functions_of_the_data_span_on_the_curve": o["dimR"], "rank_of_the_26_conditions": o["rank"],
                       "candidates": o["candidates"], "verdict": o["verdict"]}}
    if o["verdict"] == "NOT IDENTIFIED":
        entry["claim"]["dual_margin"] = round(o["dual_margin"], 6)
    if o["verdict"] == "IDENTIFIED":
        entry["claim"]["certificate_scale_A"] = o["certificate"]["A"]
        entry["claim"]["smallest_hessian_eigenvalue_at_the_states"] = round(o["certificate"]["hessian"], 6)
    out["thirteen_states_four_angles"].append(entry)
    print(f"seed {seed}: {o['verdict']}", flush=True)
(here / "benchmarks" / "torus_instances_v1.json").write_text(json.dumps(out, indent=1) + "\n")
print("written: experiments/ensemble/benchmarks/torus_instances_v1.json")
