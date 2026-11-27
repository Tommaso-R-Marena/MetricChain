"""
summarise_all.py -- workstream R6: one table over all campaign files in data/ (simulated-oracle campaigns, end-to-end runs, adversarial search).
usage: python3 summarise_all.py
"""
import json, glob, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))

def load(pat):
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "data", pat))):
        for l in open(f):
            l = l.strip()
            if l:
                out.append(json.loads(l))
    return out

rows = []
tot = collections.Counter()
for name in ["A_small", "A_ties", "A_medium", "B_reducedK", "B_invalid", "B_lazy", "D_2L", "D_2L_off"]:
    recs = load(name + "_[0-9]*.jsonl")
    if not recs:
        continue
    ok = [r for r in recs if "harness_limit" not in r]
    S = collections.Counter()
    S["runs"] = len(ok); S["discarded"] = len(recs) - len(ok)
    mx = collections.defaultdict(float)
    for r in ok:
        S["closed"] += r["status"] == "closed"
        S["closed_LgtU"] += r["status"] == "closed_L>U"
        S["abort"] += r["status"] == "abort"
        S["abort_cost"] += r.get("abort") == "query budget C_max"
        S["abort_unclassified"] += r.get("abort") == "unclassified at the last rung"
        S["G_failed"] += (not r["G"])
        S["det_viol"] += bool(r["det"])
        S["good_viol"] += bool(r["good"])
        S["pop"] += r["pop"]; S["neg"] += r["neg"]; S["runs_neg"] += r["neg"] > 0
        if r["status"] == "closed":
            S["close_pop"] += r["close_pop"]; S["close_unpop"] += not r["close_pop"]; S["close_tail0"] += r["close_tail0"]
            inval = (r["lo"] > 1e-9 or r["up"] < -1e-9)
            S["invalid_final"] += inval
            S["invalid_final_on_G"] += inval and r["G"]
            S["close_r_le_rdag"] += (r["close_r"] <= r["rdag"])
        if "q_le_Cmax" in r:
            S["q_gt_Cmax"] += not r["q_le_Cmax"]
        for k, v in r["ratios"].items():
            mx[k] = max(mx[k], v)
        mx["lnM"] = max(mx["lnM"], r["lnM"])
    rows.append((name, dict(S), dict(mx)))
    for k, v in S.items():
        tot[k] += v
for name, S, mx in rows:
    print("==", name)
    print("  ", {k: S[k] for k in sorted(S)})
    print("  ", {k: round(v, 4) for k, v in sorted(mx.items())})
print("== TOTAL simulated-oracle runs:", {k: tot[k] for k in sorted(tot)})

e2e = load("e2e_*.jsonl")
if e2e:
    for Kdiv in sorted(set(r["Kdiv"] for r in e2e)):
        rr = [r for r in e2e if r["Kdiv"] == Kdiv]
        print("== e2e (real two-sample inner brackets), K divided by", Kdiv, ":", dict(
            runs=len(rr), closed=sum(r["status"] == "closed" for r in rr), abort=sum(r["status"] == "abort" for r in rr),
            real_brackets=sum(r["real_brackets"] for r in rr), inner_calls=sum(r["inner_calls"] for r in rr),
            rungs_real=sum(r["rungs_real"] for r in rr), rungs=sum(r["rungs"] for r in rr),
            invalid_inner=sum(r["invalid_inner"] for r in rr), runs_with_invalid_inner=sum(r["invalid_inner"] > 0 for r in rr),
            G_failed=sum(not r["G"] for r in rr), det_viol=sum(bool(r["det"]) for r in rr), good_viol=sum(bool(r["good"]) for r in rr),
            invalid_final=sum(1 for r in rr if r["status"] == "closed" and (r["lo"] > 1e-9 or r["up"] < -1e-9)),
            invalid_final_on_G=sum(1 for r in rr if r["status"] == "closed" and (r["lo"] > 1e-9 or r["up"] < -1e-9) and r["G"]),
            too_wide_final=sum(1 for r in rr if r["status"] == "closed" and r["width"] > r["x_out"] + 1e-9),
            max_q_over_Cmax=max(r["q_over_Cmax"] for r in rr), neg=sum(r["neg"] for r in rr), points=sum(r["points"] for r in rr)))
adv = load("adversarial.jsonl")
for r in adv:
    c = json.loads(r["cell"])
    print("== adversarial: n=%d n_o=%d u=%g objective=%s evaluations=%d best=%.4f violations=%d" % (c["n"], c["n_o"], c["u"], r["objective"], r["evaluations"], r["best"], r["violations"]))
