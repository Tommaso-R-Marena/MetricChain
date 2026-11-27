"""R7: recount of the X-006 tables of ENG-RES-0008 section 6 from the stored file
(experiments/eng/twolevel/results/x006_sampled.jsonl at a2f6dc7), with my own code."""
import json, math
from collections import defaultdict
from pathlib import Path
P = Path(__file__).resolve().parent / "eng_copy" / "experiments" / "eng" / "twolevel" / "results" / "x006_sampled.jsonl"
rows = [json.loads(l) for l in open(P)]
agg = defaultdict(lambda: defaultdict(int))
for r in rows:
    k = (r["u"], r["n_o"], r["K"], r["k_scale"])
    for f in ("runs", "good_event_failed", "invalid", "invalid_on_good_event", "width_violations", "claim_violations_on_good_event", "aborted", "trivial_returned"):
        agg[k][f] += r[f]
    agg[k]["cases"] += 1
print("u n_o K scale | cases runs good_event_failed invalid invalid_on_good width claim aborted")
for k in sorted(agg, key=lambda t: (t[0], -t[3])):
    a = agg[k]
    print(k, a["cases"], a["runs"], a["good_event_failed"], a["invalid"], a["invalid_on_good_event"], a["width_violations"], a["claim_violations_on_good_event"], a["aborted"])
full = [r for r in rows if r["k_scale"] == 1.0]
tot = sum(r["runs"] for r in full)
fail = sum(r["good_event_failed"] + r["invalid"] + r["width_violations"] + r["claim_violations_on_good_event"] + r["aborted"] for r in full)
print(f"theorem's K: cases {len(full)}, runs {tot}, failures of any kind {fail}")
print(f"  95% upper bound, pooled: 1 - 0.05^(1/{tot}) = {1 - 0.05 ** (1 / tot):.3e};  per case ({full[0]['runs']} runs): {1 - 0.05 ** (1 / full[0]['runs']):.3e};"
      f"  Bonferroni over {len(full)} cases at overall 95%: {1 - (0.05 / len(full)) ** (1 / full[0]['runs']):.3e}")
print("  landscapes:", len({r['profile'] for r in full}), " oracles:", sorted({r['oracle'] for r in full}), " (u, n_o, n_i):", sorted({(r['u'], r['n_o'], r['n_i']) for r in full}))
d = [r["lqueries_mean"] - r["mean_run_lcost"] for r in full if r["oracle"] in ("bottom", "top")]
print(f"  mean ln(evaluations) minus mean-run ln(cost), oracles bottom/top at the theorem's K: min {min(d):+.4f} max {max(d):+.4f}")
d2 = [(r["lqueries_max"] - r["mean_run_lcost"], r["lqueries_min"] - r["mean_run_lcost"]) for r in full if r["oracle"] in ("bottom", "top")]
print(f"  spread of ln(evaluations) around the mean run within a case: max over cases of (max - meanrun) {max(x for x, y in d2):+.4f}, min of (min - meanrun) {min(y for x, y in d2):+.4f}")
