"""Print the numbers of the report from the stored result files (``results/*.json``); nothing is recomputed.

    python report_numbers.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

RES = Path(__file__).resolve().parent / "results"


def main() -> int:
    fz = json.loads((RES / "freeze.json").read_text())
    print(f"FREEZE  {fz['frozen_utc']}  sha256 {fz['indep_zcheck_sha256_at_freeze'][:16]}...  "
          f"{fz['indep_zcheck_lines_at_freeze']} lines; gaps recorded: {len(fz['specification_gaps_recorded_before_freeze'])}")

    runs = sorted(RES.glob("z12_seed*.json"))
    tot, rel, flt, dis = (collections.Counter() for _ in range(4))
    by = collections.defaultdict(collections.Counter)
    findings, seconds, instances = 0, 0.0, 0
    worst = {"excess_lo_relative": 0.0, "excess_hi_relative_without_prunes": 0.0, "excess_hi_relative": 0.0,
             "float_inside_exact_gap_relative": 0.0}
    for path in runs:
        d = json.loads(path.read_text())
        seconds += d["seconds"]
        instances += d["instances"]
        findings += len(d["findings"])
        for src, c in d["by_source"].items():
            group = "variants" if src.startswith("variant") else src
            by[group].update(c)
            tot.update(c)
        rel.update(d["relation"])
        flt.update(d["float_tier"])
        dis.update(d["disagreements"])
        for k in worst:
            if d[k].get("n"):
                worst[k] = max(worst[k], d[k]["max"])
    print(f"\nZ12  runs {[p.name for p in runs]}  instances {instances}  certificates {tot['cases']}  "
          f"seconds {seconds:.0f}  findings stored {findings}")
    cols = ["cases", "their_not_run_hazard", "their_accept", "their_reject", "mine_accept", "mine_reject",
            "agree_accept", "agree_reject", "only_theirs_accepts", "only_mine_accepts", "their_truth_yes",
            "their_unsound_lnz", "their_pop_yes", "their_unsound_pop", "their_exception", "their_loader_exception",
            "their_timeout", "mine_truth_yes", "mine_pop_yes", "mine_internal", "mine_accept_rounded_mode",
            "accepted_without_a_box"]
    for group in sorted(by):
        print(f"  {group}:")
        print("     " + ", ".join(f"{c}={by[group].get(c, 0)}" for c in cols))
    print("  all sources: " + ", ".join(f"{c}={tot.get(c, 0)}" for c in cols))
    print("  their truth verdicts other than yes:",
          {k: v for k, v in tot.items() if k.startswith(("their_truth_", "their_pop_")) and not k.endswith("_yes")})
    print("  mine  truth verdicts other than yes:",
          {k: v for k, v in tot.items() if k.startswith(("mine_truth_", "mine_pop_")) and not k.endswith("_yes")})
    print("  relation (both accept):", {k: rel[k] for k in sorted(rel)})
    print("  largest relative distance of their bounds from the ideal interval: lower",
          f"{worst['excess_lo_relative']:.3e}, upper without prunes {worst['excess_hi_relative_without_prunes']:.3e},"
          f" upper with prunes {worst['excess_hi_relative']:.3e}   (2**-40 = {2 ** -40:.3e})")
    print("  float tier:", {k: flt[k] for k in sorted(flt)})
    print(f"  largest relative amount by which a float-tier bound lies inside the exact-tier interval: "
          f"{worst['float_inside_exact_gap_relative']:.3e}")
    print("  disagreements by class:")
    for k, v in dis.most_common():
        print(f"     {v:6d}  {k}")

    z4 = json.loads((RES / "z4.json").read_text())
    e, lg = z4["exp"], z4["log"]
    print(f"\nZ4   cases {z4['cases']}  seconds {z4['seconds']}  lower confirmed {e.get('lower_confirmed', 0)}  "
          f"upper confirmed {e.get('upper_confirmed', 0)}  violated {e.get('lower_VIOLATED', 0) + e.get('upper_VIOLATED', 0)}"
          f"  undecided {e.get('lower_undecided', 0) + e.get('upper_undecided', 0)}  exceptions {z4['exp_exceptions']}")
    print(f"     exp_bounds equal to the mantissa/exponent form: {e.get('exp_bounds_equals_me_form', 0)}, "
          f"different: {e.get('exp_bounds_differs_from_me_form', 0)}; lower bound zero: {e.get('lower_bound_zero', 0)}")
    for k, v in z4["exp_log2_relative_width"].items():
        if "bits=64" in k and v.get("n"):
            print(f"     log2 relative width, {k:30s} n={v['n']:4d}  median {v['median']:.4g}  max {v['max']:.4g}")
    print("     microseconds per call at bits=64:", z4["exp_microseconds_per_call_bits64"])
    print(f"     log_bounds: cases {lg['cases']}, lower confirmed {lg.get('lower_confirmed', 0)}, upper confirmed "
          f"{lg.get('upper_confirmed', 0)}, violated {lg.get('lower_VIOLATED', 0) + lg.get('upper_VIOLATED', 0)}; "
          f"width in units of 2**-40: {z4['log_width_in_units_of_2^-40']}")
    print(f"     log_bounds monotonicity: {z4['log_monotonicity']}, worst relative inversion "
          f"{z4['log_worst_inversion_relative']:.3e}")

    fd = json.loads((RES / "findings.json").read_text())
    f1 = fd["F1_float_tier_unsound_for_large_exp_bits"]
    print(f"\nF1   tables {f1['tables']}  truth ln Z {f1['truth_ln_z']}")
    print(f"     certificate {f1['certificate']}")
    print(f"     indep_zcheck {f1['indep_zcheck']}")
    print(f"     float tier unsound at exp_bits {f1['unsound_exp_bits']}; sound or rejected at "
          f"{f1['sound_or_rejected_exp_bits']}")
    for row in f1["by_exp_bits"]:
        if row["exp_bits"] in (64, 985, 990, 991, 992, 993):
            print(f"     exp_bits {row['exp_bits']}: float {row['float']} | exact {row['exact']}")
    f3 = fd["F3_prune_with_negative_margin"]
    print("\nF3   re-run:")
    for row in f3["re_run_here"]:
        print("    ", row)
    print("     ad-hoc probe, not re-run:", f3["observed_in_an_ad_hoc_probe_not_re_run"])
    f4 = fd["F4_file_loader"]
    print(f"\nF4   loader cases {len(f4['cases'])}")
    print("     raised something else than MalformedZCertificate:",
          f4["their_loader_raised_something_else_than_MalformedZCertificate"])
    print("     loaded by theirs, refused by indep_zcheck:", f4["loaded_by_theirs_and_refused_by_indep_zcheck"])
    for row in f4["cases"]:
        if "nested" in row["case"] or "meta" in row["case"]:
            print("    ", row)
    print("\nF6  ", fd["F6_model_without_sites"])
    print("\nCOST (small dense instances, certificate of their producer without steps)")
    for row in fd["cost_small_dense"]:
        print("    ", json.dumps(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
