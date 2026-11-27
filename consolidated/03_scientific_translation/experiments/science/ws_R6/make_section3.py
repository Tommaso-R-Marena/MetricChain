"""
make_section3.py -- workstream R6: compute, from the data files only, every number quoted in section 3 of the report
(so that no number is transcribed by hand).  Prints markdown tables and a JSON summary (data/summary_all.json).
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


DESC = {
    "A_small": ("2L⁺", "theorem", "8 cells, `n_o ∈ {10,…,40}`: Theorem-K2 parameters at `x ∈ {1, 2, 4}`, two general cells, one Corollary-K1.b cell", "valid (10 behaviours)"),
    "A_ties": ("2L⁺", "theorem", "5 cells, `n_o ∈ {24, 32, 100, 120}`, dyadic `λ`, `un/λ ∈ ℕ`, flat fibres, profiles on the level grid", "valid (6 behaviours: ends of brackets exactly at `W`, mixtures, the two adversaries)"),
    "A_medium": ("2L⁺", "theorem", "12 cells, `n_o ∈ {60,…,1000}`, `u ∈ {½, 1, 2, 3}`: eight bounded-regime cells and four Corollary-K1.b (extensive) cells", "valid (10 behaviours)"),
    "B_reducedK": ("2L⁺", "`K ∈ {8, 20, 50}`", "5 cells (each with the three values of `K`), `n_o ∈ {40,…,400}`", "valid (10 behaviours)"),
    "B_invalid": ("2L⁺", "theorem (one cell `K = 20`)", "7 cells, `n_o ∈ {12,…,400}`", "**invalid** (9 behaviours: above `W`, below `W`, too wide, trivial, LAZY, mixtures)"),
    "B_lazy": ("2L⁺", "theorem", "6 cells, `n_o ∈ {40,…,400}`, two models of the rung costs (see below)", "**invalid** (LAZY: every refined point reaches the last rung)"),
    "D_2L": ("2L (Thm 11.52)", "theorem (`K = ⌈24 ln(2^{n+6}n³/δ)⌉`)", "8 cells, `n ∈ {40,…,3000}`, `n_o ∈ {12,…,1500}`", "valid (10 behaviours)"),
    "D_2L_off": ("2L (Thm 11.52)", "theorem and `K ∈ {10, 30}`", "5 cells, `n ∈ {60, 600, 1200}`", "valid and **invalid**"),
}

summary = {}
rows = []
tot = collections.Counter()
mx_all = collections.defaultdict(float)
for name in ["A_small", "A_ties", "A_medium", "D_2L", "B_reducedK", "B_invalid", "B_lazy", "D_2L_off"]:
    recs = load(name + "_[0-9]*.jsonl")
    if name == "B_lazy":
        recs += load("B_lazycheap_[0-9]*.jsonl")
    if not recs:
        continue
    ok = [r for r in recs if "harness_limit" not in r]
    S = collections.Counter()
    S["runs"] = len(ok)
    S["discarded"] = len(recs) - len(ok)
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
        S["pop"] += r["pop"]
        S["neg"] += r["neg"]
        S["runs_neg"] += r["neg"] > 0
        if r["status"] == "closed":
            S["close_pop"] += r["close_pop"]
            S["close_unpop"] += not r["close_pop"]
            S["close_tail0"] += r["close_tail0"]
            inval = (r["lo"] > 1e-9 or r["up"] < -1e-9)
            S["invalid_final"] += inval
            S["invalid_final_on_G"] += inval and r["G"]
            S["close_r_le_rdag"] += (r["close_r"] <= r["rdag"])
        if "q_le_Cmax" in r:
            S["q_gt_Cmax"] += not r["q_le_Cmax"]
        for k, v in r["ratios"].items():
            mx[k] = max(mx[k], v)
            mx_all[name[0] + ":" + k] = max(mx_all[name[0] + ":" + k], v)
        mx["lnM"] = max(mx["lnM"], r["lnM"])
        S["runs_big_blocks"] += r["lnM"] > 36.84           # a block of more than 1e16 points
    cells_seen = collections.Counter(r["cell"] for r in ok)
    cs = [json.loads(c) for c in cells_seen]
    census = dict(cells=len(cs), n=sorted(set(c["n"] for c in cs)), n_o=sorted(set(c["n_o"] for c in cs)), u=sorted(set(c["u"] for c in cs)),
                  Kov=sorted(set(str(c.get("Kov")) for c in cs)), runs_per_cell=sorted(cells_seen.values()),
                  behaviours=len(set(r["strat"] for r in ok)), profiles=len(set(r["prof"] for r in ok)))
    summary[name] = dict(S=dict(S), max=dict(mx), census=census)
    rows.append((name, S, mx))
    for k, v in S.items():
        tot[k] += v

print("| campaign | algorithm | `K` | cells | inner behaviour | runs completed (discarded) | closed / `L>U` / aborted | levels left populated / negligible | good event failed | **violations: every-run claims / good-event claims** | invalid final bracket (of these on the good event) |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for name, S, mx in rows:
    d = DESC[name]
    print("| `%s` | %s | %s | %s | %s | %d (%d) | %d / %d / %d | %d / %d | %d | **%d / %d** | %d (%d) |" % (
        name, d[0], d[1], d[2], d[3], S["runs"], S["discarded"], S["closed"], S["closed_LgtU"], S["abort"], S["pop"], S["neg"], S["G_failed"],
        S["det_viol"], S["good_viol"], S["invalid_final"], S["invalid_final_on_G"]))
print()
print("TOTAL:", {k: tot[k] for k in sorted(tot)})
valid_theorem = sum(summary[n]["S"]["runs"] for n in ("A_small", "A_ties", "A_medium", "D_2L") if n in summary)
off = sum(summary[n]["S"]["runs"] for n in ("B_reducedK", "B_invalid", "B_lazy", "D_2L_off") if n in summary)
inval_runs = sum(summary[n]["S"]["runs"] for n in ("B_invalid", "B_lazy") if n in summary)
print("runs with the constants of the theorems and a valid oracle:", valid_theorem, "| off the good event by design:", off, "| with invalid inner answers (B_invalid, B_lazy):", inval_runs)
print("largest ratios, campaigns A (valid, theorem constants):", {k[2:]: round(v, 4) for k, v in sorted(mx_all.items()) if k.startswith("A:")})
print("largest ratios, campaign D (2L):", {k[2:]: round(v, 4) for k, v in sorted(mx_all.items()) if k.startswith("D:")})
print("largest ratios, campaigns B:", {k[2:]: round(v, 4) for k, v in sorted(mx_all.items()) if k.startswith("B:")})
for name, S, mx in rows:
    print("  %-11s closures: at a populated pass %d, unpopulated %d, empty tail %d, at a radius <= r-dagger %d; runs with negligible levels %d; aborts: cost %d, unclassified %d; max ln M %.1f; q>C_max: %d"
          % (name, S["close_pop"], S["close_unpop"], S["close_tail0"], S["close_r_le_rdag"], S["runs_neg"], S["abort_cost"], S["abort_unclassified"], mx["lnM"], S["q_gt_Cmax"]))

print("census of the cells that have completed runs (to be compared with the descriptions in the table):")
for name in summary:
    if "census" in summary[name]:
        print("  %-11s" % name, summary[name]["census"])
# reduced K by value
for name in ("B_reducedK", "D_2L_off"):
    recs = [r for r in load(name + "_[0-9]*.jsonl") if "harness_limit" not in r]
    by = collections.defaultdict(collections.Counter)
    for r in recs:
        c = json.loads(r["cell"])
        k = c.get("Kov")
        valid_orc = r["strat"] in ("center", "top", "bottom", "adv_hi", "adv_lo", "exact", "random", "narrow", "mix3", "mix_tb")
        key = (k, "valid" if valid_orc else "invalid")
        by[key]["runs"] += 1
        by[key]["Gfail"] += (not r["G"])
        by[key]["det"] += bool(r["det"])
        by[key]["good"] += bool(r["good"])
        by[key]["abort"] += r["status"] == "abort"
        if r["status"] == "closed":
            inval = (r["lo"] > 1e-9 or r["up"] < -1e-9)
            by[key]["invalid_final"] += inval
            by[key]["invalid_final_on_G"] += inval and r["G"]
    print(name, "by (K override, oracle):")
    for key in sorted(by, key=lambda x: (str(x[0]), x[1])):
        print("   ", key, dict(by[key]))
    summary[name + "_byK"] = {str(k): dict(v) for k, v in by.items()}

# B_lazy split by the cost model of the cell
lz = [r for r in load("B_lazy_[0-9]*.jsonl") + load("B_lazycheap_[0-9]*.jsonl") if "harness_limit" not in r]
steep = [r for r in lz if json.loads(r["cell"]).get("costs") == "steep"]
cheap = [r for r in lz if json.loads(r["cell"]).get("costs") != "steep"]
summary["B_lazy_split"] = dict(steep_runs=len(steep), steep_abort_cost=sum(r.get("abort") == "query budget C_max" for r in steep),
                               steep_q_gt_Cmax=sum(not r["q_le_Cmax"] for r in steep),
                               steep_max_lnq_minus_lnCmax=max([r["lnq"] - r["lnCmax"] for r in steep], default=None),
                               cheap_runs=len(cheap), cheap_abort_cost=sum(r.get("abort") == "query budget C_max" for r in cheap),
                               cheap_max_q_over_Cvi=max([r["ratios"]["q_over_Cvi"] for r in cheap], default=None))
print("B_lazy split:", summary["B_lazy_split"])

e2e = load("e2e_*.jsonl")
for Kdiv in sorted(set(r["Kdiv"] for r in e2e)):
    rr = [r for r in e2e if r["Kdiv"] == Kdiv]
    d = dict(runs=len(rr), closed=sum(r["status"] == "closed" for r in rr), abort=sum(r["status"] == "abort" for r in rr),
             real_brackets=sum(r["real_brackets"] for r in rr), inner_calls=sum(r["inner_calls"] for r in rr),
             rungs_real=sum(r["rungs_real"] for r in rr), rungs=sum(r["rungs"] for r in rr),
             invalid_inner=sum(r["invalid_inner"] for r in rr), runs_with_invalid_inner=sum(r["invalid_inner"] > 0 for r in rr),
             G_failed=sum(not r["G"] for r in rr), det_viol=sum(bool(r["det"]) for r in rr), good_viol=sum(bool(r["good"]) for r in rr),
             invalid_final=sum(1 for r in rr if r["status"] == "closed" and (r["lo"] > 1e-9 or r["up"] < -1e-9)),
             invalid_final_on_G=sum(1 for r in rr if r["status"] == "closed" and (r["lo"] > 1e-9 or r["up"] < -1e-9) and r["G"]),
             too_wide_final=sum(1 for r in rr if r["status"] == "closed" and r["width"] > r["x_out"] + 1e-9),
             max_q_over_Cmax=max(r["q_over_Cmax"] for r in rr), neg=sum(r["neg"] for r in rr), points=sum(r["points"] for r in rr),
             max_width_excess=max(r["max_width_excess"] for r in rr))
    print("e2e, K divided by", Kdiv, ":", d)
    summary["e2e_K%d" % Kdiv] = d
th = [r for r in load("three_*.jsonl") if "skipped" not in r]
if th:
    d = dict(outer_runs=len(th), outer_closed=sum(r["status"] == "closed" for r in th), outer_invalid=sum(not r["outer_valid"] for r in th),
             outer_too_wide=sum(r["status"] == "closed" and r["width"] > r["x_out"] + 1e-9 for r in th), outer_det=sum(r["outer_det"] for r in th),
             outer_good=sum(r["outer_good"] for r in th), middle_runs=sum(r["middle_runs"] for r in th), middle_closed=sum(r["middle_closed"] for r in th),
             middle_invalid=sum(r["middle_invalid"] for r in th), middle_too_wide=sum(r["middle_too_wide"] for r in th),
             middle_det=sum(r["middle_det"] for r in th), middle_good=sum(r["middle_good"] for r in th), bottom_brackets=sum(r["bottom"] for r in th),
             bottom_invalid=sum(r["bottom_invalid"] for r in th), runs_with_real_bottom=sum(r["bottom_real"] for r in th),
             sizes=sorted(set(tuple(r["sizes"]) for r in th)), max_lnq_minus_lnCmax=max(r["lnq_outer"] - r["lnCmax_outer"] for r in th))
    print("three levels:", d)
    summary["three"] = d
adv = load("adversarial.jsonl")
adv.sort(key=lambda r: (json.loads(r["cell"])["n_o"], r["objective"]))
print("adversarial search:")
for r in adv:
    c = json.loads(r["cell"])
    print("   n=%d n_o=%d u=%g lam=%s | objective %-5s | %4d literal runs attempted, %s completed | best %.4f | violations %d" % (
        c["n"], c["n_o"], c["u"], c["lam"], r["objective"], r["evaluations"], r.get("completed", "all"), r["best"], r["violations"]))
# records written before the counter `completed` existed are from cells with n_o <= 40, where no run can reach the sampler limit
summary["adversarial"] = [dict(cell=json.loads(r["cell"]), objective=r["objective"], evaluations=r["evaluations"], completed=r.get("completed", r["evaluations"]),
                               seed=r["seed"], best=r["best"], violations=r["violations"]) for r in adv]
cc = [json.load(open(f))["summary"] for f in sorted(glob.glob(os.path.join(HERE, "data", "capcorner_*.json")))]
if cc:
    keys = [k for k in cc[0] if isinstance(cc[0][k], (int, float)) and k not in ("max_M_over_cap", "rge1_max_M_over_cap", "rle0_max_M_over_cap")]
    d = {k: sum(c[k] for c in cc) for k in keys}
    d["max_M_over_cap"] = max(c["max_M_over_cap"] for c in cc)
    print("capcorner:", d)
    summary["capcorner"] = d
json.dump(summary, open(os.path.join(HERE, "data", "summary_all.json"), "w"), indent=1, default=str)
