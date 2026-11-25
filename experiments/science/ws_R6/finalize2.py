"""
finalize2.py -- workstream R6: put the run counts of the SECOND pass (data/summary_all.json, written by make_section3.py) into
the passages of the report outside the generated blocks of section 3 (section 1, verdict table, m6, section 2.5, R6-E2, section 8).
Re-runnable: every passage is found by a regular expression on its words, not on its numbers, and must occur exactly once.
Run AFTER make_section3.py and fill_report.py.  Writes data/headline_counts.json.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.environ.get("R6_REPORT", os.path.join(HERE, "..", "..", "..", "docs", "science", "workstreams", "R6_REPORT.md"))
S = json.load(open(os.path.join(HERE, "data", "summary_all.json")))


def g(name, key):
    return S.get(name, {}).get("S", {}).get(key, 0)


def mx(name, key):
    return S.get(name, {}).get("max", {}).get(key, 0.0)


A = ["A_small", "A_ties", "A_medium"]
byK = S["D_2L_off_byK"]
off_thm_valid = sum(v["runs"] for k, v in byK.items() if k.startswith("(None") and "'valid'" in k)
off_redK = sum(v["runs"] for k, v in byK.items() if not k.startswith("(None") and "'valid'" in k)
off_invalid = sum(v["runs"] for k, v in byK.items() if "'invalid'" in k)
assert off_thm_valid + off_redK + off_invalid == g("D_2L_off", "runs")
for k, v in byK.items():                       # 2L, theorem constants, valid answers: events never failed, no invalid bracket
    if k.startswith("(None") and "'valid'" in k:
        assert v.get("Gfail", 0) == 0 and v.get("invalid_final", 0) == 0 and v.get("det", 0) == 0 and v.get("good", 0) == 0, v
v2lp = sum(g(n, "runs") for n in A)
v2l = g("D_2L", "runs")
thm_valid = v2lp + v2l + off_thm_valid
redK = g("B_reducedK", "runs") + off_redK
invalid = g("B_invalid", "runs") + g("B_lazy", "runs") + off_invalid
total = thm_valid + redK + invalid
assert total == sum(g(n, "runs") for n in A + ["D_2L", "B_reducedK", "B_invalid", "B_lazy", "D_2L_off"])
for n in A + ["D_2L"]:
    assert g(n, "G_failed") == 0 and g(n, "invalid_final") == 0 and g(n, "det_viol") == 0 and g(n, "good_viol") == 0 and g(n, "closed") == g(n, "runs"), n
for n in ["B_reducedK", "B_invalid", "B_lazy", "D_2L_off"]:
    assert g(n, "det_viol") == 0 and g(n, "good_viol") == 0, n
runs_2l = v2l + g("D_2L_off", "runs")
runs_2lp = v2lp + g("B_reducedK", "runs") + g("B_invalid", "runs") + g("B_lazy", "runs")
LZ = S["B_lazy_split"]
assert LZ["steep_q_gt_Cmax"] == 0
lazy_cost, lazy_runs = LZ["steep_abort_cost"], LZ["steep_runs"]
e2e_runs = S["e2e_K1"]["runs"] + S["e2e_K16"]["runs"]
adv_total = sum(r["completed"] for r in S["adversarial"])          # completed runs only
import glob
cs_runs = sum(json.load(open(f))["runs"] for f in glob.glob(os.path.join(HERE, "data", "capsearch_*.json")))
close_pop_A = sum(g(n, "close_pop") for n in A)
closed_A = sum(g(n, "closed") for n in A)
count_max = max(mx(n, "count_ineq") for n in A)
H = dict(total=total, theorem_constants_valid=thm_valid, of_which_2LP=v2lp, of_which_2L=v2l + off_thm_valid, reduced_K=redK, invalid_answers=invalid,
         runs_2L=runs_2l, runs_2LP=runs_2lp, lazy_steep_abort_cost=lazy_cost, lazy_steep_runs=lazy_runs, e2e_runs=e2e_runs, adversarial=adv_total,
         capsearch=cs_runs, close_pop_A=close_pop_A, closed_A=closed_A, count_ineq_max_A=count_max, D_2L_off=dict(theorem_valid=off_thm_valid, reduced_K=off_redK, invalid=off_invalid))
json.dump(H, open(os.path.join(HERE, "data", "headline_counts.json"), "w"), indent=1)

s = open(REPORT).read()
N = r"[\d,]+"


def sub(pattern, repl):
    global s
    found = re.findall(pattern, s)
    assert len(found) == 1, (pattern, len(found))
    s = re.sub(pattern, lambda m: repl, s)


sub(r"violated no claim in \*\*" + N + r" literal runs\*\*", f"violated no claim in **{total:,} literal runs**")
sub(r"simulated inner oracle — " + N + r" with the constants of the theorems", f"simulated inner oracle — {thm_valid:,} with the constants of the theorems")
sub(r"every bracket was valid\), " + N + r" with `K` reduced", f"every bracket was valid), {redK:,} with `K` reduced")
sub(r"for the first time, \*\*" + N + r" runs with invalid inner answers\*\*", f"for the first time, **{invalid:,} runs with invalid inner answers**")
sub(r"with a dear last rung " + N + r" of " + N + r" such", f"with a dear last rung {lazy_cost} of {lazy_runs} such")
sub(r"and " + N + r" runs of two searches for a counterexample", f"and {adv_total + cs_runs:,} runs of two searches for a counterexample")
sub(r"own derivation before reading; " + N + r" own runs of 2L \|", f"own derivation before reading; {runs_2l:,} own runs of 2L |")
sub(r"1–3, 8, 9 after; " + N + r" own simulated-oracle runs, " + N + r" with real inner brackets",
    f"1–3, 8, 9 after; {runs_2lp:,} own simulated-oracle runs, {e2e_runs} with real inner brackets")
sub(r"in the valid 2L⁺ campaigns " + N + r" of " + N + r" closures happen at a populated pass",
    f"in the valid 2L⁺ campaigns {close_pop_A} of {closed_A} closures happen at a populated pass")
sub(r"rung costs growing by `e\^\{80\}`, " + N + r" of my " + N + r" runs stop on the query", f"rung costs growing by `e^{{80}}`, {lazy_cost} of my {lazy_runs} runs stop on the query")
sub(r"unless it is stopped, in " + N + r" of " + N + r" runs\.", f"unless it is stopped, in {lazy_cost} of {lazy_runs} runs.")
sub(r"\(my runs reach `[\d.]+` of it, §3\.2;", f"(my runs reach `{count_max:.2f}` of it, §3.2;")
open(REPORT, "w").write(s)
print(json.dumps(H, indent=1))
