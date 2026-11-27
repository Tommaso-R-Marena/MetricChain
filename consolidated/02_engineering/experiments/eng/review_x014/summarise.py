"""Print the numbers of the referee's report from the JSON files of this directory (nothing is computed here).

    python experiments/eng/review_x014/summarise.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    p = HERE / name
    return json.loads(p.read_text()) if p.exists() else None


def attack(name, label):
    d = load(name)
    if d is None:
        print(f"{label}: (not run)")
        return
    s = d["summary"]
    print(f"{label}: {s['configurations']} configurations ({s['skipped']} skipped), {s['runs']:,} runs, {s['closed']:,} closed, "
          f"{s['aborted']} aborted (+ {s['tie_aborts']} floating-point ties, m10), events used by the proof hold in {s['good']:,} runs")
    print(f"    invalid brackets: {s['invalid_on_good_event']} on the good event, {s['invalid_off_good_event']} off it")
    print(f"    violations on the good event: {s['violations_on_good_event'] or 'none'}")
    print(f"    violations off the good event: {s['violations_off_good_event'] or 'none'}")
    print(f"    violations of deterministic claims (any run): {s['deterministic_violations'] or 'none'}")
    print(f"    smallest x_out - width {s['min_slack_width']:.4f}; largest ln(cost) - ln(C_max) {s['max_lcost_minus_lCmax']:.2f}; levels left as negligible {s['negligible_levels']:,}; "
          f"closures: empty tail {s.get('closed_empty_tail', '?')}, radius 0 {s.get('closed_at_radius_0', '?')}, radius >= 1 {s.get('closed_at_radius_ge_1', '?')}, "
          f"at a populated pass {s.get('closed_at_populated_pass', '?')}; class violation {s['max_class_violation']:.1e}; memory errors {s.get('memory_errors', 0)}")
    if "max_tail_ratio" in s or "min_harper_ratio" in s:
        print(f"    closest approach to equality in the tail lemmas as used (all rows of this file, controls included where there are any): "
              f"true tail / bound <= {s.get('max_tail_ratio', float('nan')):.3f}, truncated mean / Harper bound >= {s.get('min_harper_ratio', float('nan')):.3f}")
    worst = None
    for r in d["rows"]:
        if "skipped" in r or not r["runs"]:
            continue
        frac = (r["invalid_good"] + r["invalid_bad"]) / r["runs"]
        if worst is None or frac > worst[0]:
            worst = (frac, r["invalid_good"] + r["invalid_bad"], r["runs"], r["shape"], r["design"], r.get("kdiv"))
    if worst:
        print(f"    largest invalid fraction in one configuration: {worst[1]}/{worst[2]} = {worst[0]:.4f}  {worst[3]} {worst[4]} K/{worst[5]}")
    if "by_mutation" in d:
        for k, m in d["by_mutation"].items():
            print(f"    mutation {k:48s}: caught in {m['configurations_caught']}/{m['configurations']} configurations, {m['runs_with_a_violation']}/{m['runs']} runs; "
                  f"invalid {m['invalid']}, aborted {m['aborted']}; largest true tail / bound {m.get('max_tail_ratio', float('nan')):.3f}")
            print(f"        claims violated: {m['claims']}")
        # per instance kind, for the wrong-table mutations: where does it show?
        kinds = {}
        for r in d["rows"]:
            if "skipped" in r or r["mutation"] is not None or r["table_factor"] is None:
                continue
            for k, v in r["by_kind"].items():
                a = kinds.setdefault((r["table_factor"], k), [0, 0])
                a[0] += v["invalid"]
                a[1] += v["runs"]
        for (tf, k), (bad, n) in sorted(kinds.items()):
            if n:
                print(f"        tables for {tf} of the outer slope, instances '{k}': {bad}/{n} invalid ({bad / n:.3f})")


def main() -> int:
    c = load("check_code.json")
    if c:
        k, r = c["constants"], c["runs"]
        print(f"check_code: constants {k['cases']} cases, {len(k['mismatches'])} mismatches; runs {r['runs']} compared, {r['agree']} agree, statuses {r['statuses']}, "
              f"tie aborts {r.get('tie_aborts_m10')}; max |dL| {r['max_abs_diff_L']:.1e}, max |dU| {r['max_abs_diff_U']:.1e}")
    attack("attack_theorem.json", "theorem's constants")
    attack("attack_radius.json", "theorem's constants, flat outer blocks")
    attack("attack_tuned.json", "instances tuned against the design (dip of the largest size the closure test lets pass)")
    attack("attack_kdiv.json", "K divided by 8 and 32")
    attack("attack_kdiv_local.json", "K divided by 8 and 32, second run with the per-pass implications checked")
    attack("attack_mutations.json", "negative controls")
    d = load("attack_their_sim.json")
    if d:
        print("division's simulator:", json.dumps(d["summary"], default=float))
    d = load("attack_nested.json")
    if d:
        print("nested (division's run_level):", json.dumps(d["summary"], default=float))
        for r in d["rows"]:
            if "skipped" in r:
                print("    skipped", r["sizes"], r["slopes"], r["skipped"])
            else:
                print(f"    {r['sizes']} {r['slopes']} b_top {r['b_top']}: runs {r['runs']}, invalid {r['invalid']}, too wide {r['too_wide']}, aborted {r['aborted']}, over budget {r['over_budget']}; "
                      f"middle runs {r['mid_runs']} (aborted {r['mid_aborts']}, invalid {r['mid_invalid']}, too wide {r['mid_too_wide']}, over their own bound {r['mid_over_budget']}); "
                      f"ln queries {r['max_lq_thm']:.1f} / bound {r['lCmax']:.1f}")
    d = load("check_lower_bound.json")
    if d:
        print("lower bound: dip", d["dip"])
        c = d["compare"]
        print(f"    module vs independent: {c['cases']} cases, max |diff| {c['max_abs_diff']:.1e}, mismatches {len(c['mismatches'])}, near-threshold {c['near_threshold_cases']}; "
              f"scan {c['scan_cases']} cases, max |diff| {c['scan_max_abs_diff']:.1e}, mismatches {len(c['scan_mismatches'])}")
        s = d["sub_blocks"]
        better = [x for x in s["cells"] if x["gain_nats"] > 1e-9]
        print(f"    sub-blocks: {len(better)} of {len(s['cells'])} cells have a sub-block with a larger bound; largest gain {s['largest_gain_nats']:.4f} nats")
        for x in sorted(better, key=lambda x: -x["gain_nats"])[:8]:
            print(f"        u=({x['uH']},{x['uL']}) n={x['n']} nH={x['nH']}: bound {x['lbound']:.4f}, sub-block {x['best_sub_block']} gives {x['best_sub_block_lbound']:.4f} (+{x['gain_nats']:.4f})")
        for p_ in d["exact_small"]["patterns"]:
            print(f"    Q_4 {p_['slopes']}: module = smallest ball with cone: {p_['module_agrees_with_balls_cone']}; smaller admissible set at eps {p_['accuracies_where_a_smaller_set_exists']}; "
                  f"largest factor {p_['largest_gain_factor']:.2f}")
    d = load("check_mixed.json")
    if d:
        ex = d["brute_force"]["exhaustive"]
        print(f"mixed tables, all proper subsets of Q_4, {len(ex)} slope patterns: upper violations {sum(x['upper_violations'] for x in ex)}, lower violations {sum(x['lower_violations'] for x in ex)}; "
              f"exact/bound upper in [{min(x['min_upper_ratio'] for x in ex):.4f}, {max(x['max_upper_ratio'] for x in ex):.4f}], bound/exact lower in "
              f"[{min(x['min_lower_ratio'] for x in ex):.4f}, {max(x['max_lower_ratio'] for x in ex):.4f}]")
        sa = d["brute_force"]["sampled"]
        print(f"    sampled/structured subsets of Q_5..Q_8: {sum(x['sets'] for x in sa):,} sets, upper violations {sum(x['upper_violations'] for x in sa)}, lower violations {sum(x['lower_violations'] for x in sa)}; "
              f"max upper ratio {max(x['max_upper_ratio'] for x in sa):.4f}, max lower ratio {max(x['max_lower_ratio'] for x in sa):.4f}")
        mo = d["module"]
        print(f"    module tables: {mo['table_cases']} compositions, max |d ln E| {mo['max_abs_diff_lE']:.1e}, |d ln T| {mo['max_abs_diff_lT']:.1e}; r_dagger mismatches {len(mo['r_dagger_mismatches'])}/{mo['r_dagger_cases']}; "
              f"constants mismatches {len(mo['constants_mismatches'])}/{mo['constants_cases']}; large blocks max |diff| {d['large_tables']['max_abs_diff']:.1e}")
        for k, s in d["literal"]["summary"].items():
            print(f"    literal, {k}: {json.dumps(s, default=float)}")
    d = load("check_tail_lemma.json")
    if d:
        print("Lemmas K.2 + K.1 at every threshold of the fibre-average tables:", json.dumps(d["summary"]))
    d = load("tie_abort_example.json")
    if d:
        for row in d:
            hits = [f"{x['instance'][:28]}.. / {x['oracle']}: {x['aborted']}/{x['runs']}" for x in row["instances"] if x["aborted"]]
            print(f"tie aborts of hetero_literal.run_2l: n_o={row['n_o']} u_o={row['u_o']} inner={row['inner']} lam={row['design']['lam']} b={row['design']['b']} "
                  f"(Omega/lam = {row['omega_over_lambda']:.6g}): {hits or 'none'}")
    d = load("nested_count_comparison.json")
    if d:
        for row in d:
            print("nested count:", row)
    d = load("check_k0_mixed.json")
    if d:
        for k, s in d["summary"].items():
            print(f"K0 on mixed blocks, {k}: {json.dumps(s, default=float)}")
    d = load("check_bounds_vs_lower.json")
    if d:
        print(f"certified bound vs lower bound: {d['searches']} searches, {d['single_levels']} single levels, {len(d['contradictions'])} contradictions; "
              f"smallest ratio search {d['smallest_ratio_search'] and round(d['smallest_ratio_search']['ratio'], 3)}, single {d['smallest_ratio_single'] and round(d['smallest_ratio_single']['ratio'], 3)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
