"""
fill_report.py -- workstream R6: write the campaign sections of the report (3.2, 3.4, 3.6, 3.7) from data/summary_all.json,
so that every run count in the report is generated from the data files.  Run make_section3.py first.
usage: python3 fill_report.py            (replaces the markers <!--SECTION3B-->, <!--SECTION3C-->, <!--SECTION3D--> in the report)
"""
import json, os, io, contextlib, subprocess, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "..", "..", "..", "docs", "science", "workstreams", "R6_REPORT.md")

out = subprocess.run([sys.executable, os.path.join(HERE, "make_section3.py")], capture_output=True, text=True).stdout
table = "\n".join(l for l in out.splitlines() if l.startswith("|"))
S = json.load(open(os.path.join(HERE, "data", "summary_all.json")))


def g(name, key, default=0):
    return S.get(name, {}).get("S", {}).get(key, default)


def mx(name, key):
    return S.get(name, {}).get("max", {}).get(key, 0.0)


A = ["A_small", "A_ties", "A_medium"]
valid_2lp = sum(g(n, "runs") for n in A)
valid_2l = g("D_2L", "runs")
neg_A = sum(g(n, "neg") for n in A)
pop_A = sum(g(n, "pop") for n in A)
close_pop_A = sum(g(n, "close_pop") for n in A)
close_unpop_A = sum(g(n, "close_unpop") for n in A)
close_tail0_A = sum(g(n, "close_tail0") for n in A)
close_le_A = sum(g(n, "close_r_le_rdag") for n in A)
disc_A = sum(g(n, "discarded") for n in A)
maxA = lambda k: max(mx(n, k) for n in A)
all_names = ["A_small", "A_ties", "A_medium", "D_2L", "B_reducedK", "B_invalid", "B_lazy", "D_2L_off"]
total_runs = sum(g(n, "runs") for n in all_names)
total_det = sum(g(n, "det_viol") for n in all_names)
total_good = sum(g(n, "good_viol") for n in all_names)
inv_runs = g("B_invalid", "runs") + g("B_lazy", "runs")
LZ = S.get("B_lazy_split", {})
byK = S.get("B_reducedK_byK", {})
byK2 = S.get("D_2L_off_byK", {})


def bk(d, key, field):
    return d.get(key, {}).get(field, 0)


e1 = S.get("e2e_K1", {})
e16 = S.get("e2e_K16", {})
th = S.get("three", {})
cc = S.get("capcorner", {})
adv = S.get("adversarial", [])

for _n in A + ["D_2L"]:
    assert g(_n, "closed") == g(_n, "runs"), ("not every valid run closed", _n)
    assert g(_n, "G_failed") == 0 and g(_n, "invalid_final") == 0 and g(_n, "det_viol") == 0 and g(_n, "good_viol") == 0, _n
assert g("B_invalid", "det_viol") == 0 and g("B_lazy", "det_viol") == 0 and g("D_2L_off", "det_viol") == 0 and g("B_reducedK", "det_viol") == 0
assert g("B_reducedK", "good_viol") == 0 and g("B_lazy", "q_gt_Cmax") == 0
sec_b = f"""### 3.2 Literal runs with a simulated inner oracle (`campaign.py`; data `data/<campaign>_<seed>.jsonl`)

{table}

Reading.

* **With the constants of the theorems and valid inner answers** ({valid_2lp} runs of Algorithm 2L⁺, {valid_2l} of
  Algorithm 2L; {disc_A} further runs of 2L⁺ were discarded because a block would have exceeded `2^83` points): every run
  closed; the events of the proof held at every pass of every run; no claim was violated; every final bracket
  contains `A`.  Branches exercised in the 2L⁺ runs: {pop_A} levels left as populated and {neg_A} as negligible;
  closures at a populated pass {close_pop_A}, at an unpopulated one {close_unpop_A} ({close_tail0_A} with an empty tail,
  {close_le_A} at a radius `≤ r†`); largest sample `e^{{{max(mx(n, 'lnM') for n in A):.1f}}}` points.  In the 2L runs: {g('D_2L', 'pop')}
  populated and {g('D_2L', 'neg')} negligible levels, largest sample `e^{{{mx('D_2L', 'lnM'):.1f}}}`.
* **How close the bounds come** (valid runs, 2L⁺): the count inequality `M_j^neg p(s_je^{{−x}}) ≤ c_η⁻¹e^λνe^x` reaches
  `{maxA('count_ineq'):.3f}` of its right-hand side; the sampled count `{maxA('used_over_cnt'):.3f}` of `cnt(x)`; the calls per level and
  rung `{maxA('calls_over_bound'):.3f}` of `min{{M̄, cnt}}`; the largest sample is `{maxA('M_over_Mdag'):.2f}·M†`, i.e. `{maxA('M_over_capnew'):.3f}` of the cap of
  `40c5bd7` and `{maxA('M_over_Mbar'):.4f}` of `M̄`; `ln(queries)/ln(C_max) ≤ {maxA('lnq_over_lnCmax'):.3f}`.  For 2L: largest sample
  `{mx('D_2L', 'M_over_Mdag'):.2f}·M†` (`{mx('D_2L', 'M_over_capnew'):.3g}` of `2eM†`), sampled count `{mx('D_2L', 'used_over_cnt'):.3g}` of `32KJe²e^x + 4K`,
  `2M_j^neg p(s_je^{{−x}})` at most `{mx('D_2L', 'count_ineq'):.3g}` of `16KJe²e^x`.
  The count is the tight claim, as R7, R8 and the engineering division found; the cap `M̄` is loose by the factor `ν₀`.
* **`K` reduced** (`B_reducedK`: `K` replaced by 8, 20 or 50 — the theorem's values are in the hundreds or thousands): the
  events of the proof failed in
  {bk(byK, "(8, 'valid')", 'Gfail')} of {bk(byK, "(8, 'valid')", 'runs')} runs at `K = 8`, {bk(byK, "(20, 'valid')", 'Gfail')} of {bk(byK, "(20, 'valid')", 'runs')} at `K = 20`, {bk(byK, "(50, 'valid')", 'Gfail')} of {bk(byK, "(50, 'valid')", 'runs')} at `K = 50`;
  **on every run on which they hold no claim is violated**; the every-run claims hold in all {g('B_reducedK', 'runs')} runs;
  {g('B_reducedK', 'invalid_final')} final brackets were invalid ({g('B_reducedK', 'invalid_final_on_G')} on a run on which the events hold).
* **Invalid inner answers** (`B_invalid`, `B_lazy`: {inv_runs} runs; nobody had tested this — in every earlier harness
  (V1) holds by construction).  The statements that Theorem 11.56 makes "for every run, on or off the
  good event" — closing radius above `r†` at every level left, `M ≤ max(K, 2M_j^neg)`, `M_j^neg ≤ (1+η)e^λν₀M†`,
  `M ≤ M̄`, the cap of `40c5bd7`, the width of every pair returned through the closure test, queries
  `≤ C_max` — **held in all {inv_runs} runs**.  As allowed off the good event, {g('B_invalid', 'invalid_final')} final brackets were
  invalid, {g('B_invalid', 'closed_LgtU')} returned pairs had `L > U` (erratum m1 of `K_REPORT.md`: return the trivial bracket), and
  {g('B_invalid', 'abort_unclassified')} runs aborted with a point unclassified at the last rung.
* **The abort rule is not decorative.**  With the behaviour LAZY and rung costs `10^l` ({LZ.get('cheap_runs', 0)} runs) no run
  needs it ({LZ.get('cheap_abort_cost', 0)} aborts; queries at most `{LZ.get('cheap_max_q_over_Cvi', 0):.3f}` of the bound of claim (vi)); with rung costs
  `e^{{80l}}` — the regime of the theorems, where the last rung dominates — **{LZ.get('steep_abort_cost', 0)} of {LZ.get('steep_runs', 0)} runs stop on the
  query budget**: without the rule their cost would exceed `C_max`.  With the test made *before* the inner
  call the number of queries is `≤ C_max` in every run (runs above `C_max`: {LZ.get('steep_q_gt_Cmax', 0)}; largest
  `ln(queries) − ln(C_max) = {LZ.get('steep_max_lnq_minus_lnCmax', 0):.3f}`).  This is the first execution of the branch that
  makes "the cost bound holds always" true (R7's M1).
* **Algorithm 2L off the good event** (`D_2L_off`, {g('D_2L_off', 'runs')} runs with reduced `K` and/or invalid answers): the
  every-run statements of Theorem 11.52 (`r > r†` at every level left, `M ≤ 8Je²M†`, `M < 2eM†`, the width,
  the completed cost display) held in all runs; {g('D_2L_off', 'invalid_final')} final brackets were invalid, {g('D_2L_off', 'invalid_final_on_G')} of them on a
  run on which the events hold; {g('D_2L_off', 'good_viol')} violations of a good-event claim on such runs.
* **The cap remark of `40c5bd7` in its degenerate branch** (`capcorner.py`, {cc.get('runs', 0)} runs, `n_o ∈ 3..12`, `λ = 1 > u`,
  `η = ½`): the cap was never reached (largest sample `{cc.get('max_M_over_cap', 0):.2f}` of it); for `r† ≥ 1` all
  {cc.get('rge1_unpop_at_Mdd', 0)} unpopulated passes with `M = M‡` exactly closed; for `r† ∈ {{0, −1}}` that pass failed to
  close {cc.get('pass_at_Mdd_unpop_notclosed', 0)} times and the sample reached exactly `2M‡` in {cc.get('sample_eq_2Mdd', 0)} runs (§2.8).

In total: **{total_runs} literal runs in the campaigns of the table, {total_det} violations of an every-run claim, {total_good}
violations of a good-event claim on a run where the events hold.**
"""

adv_lines = []
for r in adv:
    c = r["cell"]
    adv_lines.append("| `n = %d`, `n_o = %d`, `u = %g`, `λ = %.3g` | %s | %d | %.3f | %d |" % (
        c["n"], c["n_o"], c["u"], float(c["lam"]),
        {"ineq": "count inequality (v)", "count": "sampled count / `cnt`", "calls": "calls per level / bound (vi)", "cap": "sample / cap of `40c5bd7`",
         "mbar": "sample / `M†`", "cost": "`ln q/ln C_max`"}[r["objective"]], r["evaluations"], r["best"], r["violations"]))
adv_table = "\n".join(adv_lines)
adv_total = sum(r["evaluations"] for r in adv)

sec_c = f"""### 3.4 Real inner brackets: two levels and three levels (`e2e.py`, `three.py`)

*Two levels.*  Explicit `u`-Lipschitz functions on `Q_{{n_o}} × Q_{{n_i}}`, `(n_o, n_i) ∈ {{(6,6), (7,6), (6,7), (7,5), (8,5), (5,7)}}`
(five random constructions: McShane envelopes of random data, additive, radial walks, inf-convolutions of
noise), `u ∈ {{½, 1, 2}}`; every outer point is individual; the inner procedure of every rung is the two-sample
bracket of Proposition 11.57(a) on the fibre with fresh randomness (two samples drawn as exact
multinomial counts over the fibre) and the constants of the proposition for `δ′ = δ/(4LM̄)`; all constants
of Theorem 11.56 from the formulas; `L ∈ {{1, 2, 3}}`.
**{e1.get('runs', 0)} runs, {e1.get('real_brackets', 0):,} real inner brackets** ({e1.get('rungs_real', 0)} of {e1.get('rungs', 0)} rungs by a two-sample bracket,
the rest by enumeration): {e1.get('invalid_inner', 0)} inner brackets invalid or wider than promised; {e1.get('invalid_final', 0)} final brackets
invalid; {e1.get('too_wide_final', 0)} wider than `x_out`; {e1.get('abort', 0)} aborts; violations of every-run / good-event claims:
{e1.get('det_viol', 0)} / {e1.get('good_viol', 0)}; queries at most `{e1.get('max_q_over_Cmax', 0):.2g}·C_max`.
With `K` (outer and inner) divided by 16 — off the theorems, an attempt to provoke real failures of (V1): {e16.get('runs', 0)} runs,
{e16.get('real_brackets', 0):,} real brackets, {e16.get('invalid_inner', 0)} of them invalid or too wide (in {e16.get('runs_with_invalid_inner', 0)} runs); the events of
the proof failed in {e16.get('G_failed', 0)} runs; {e16.get('invalid_final', 0)} invalid final brackets, {e16.get('invalid_final_on_G', 0)} of them on a run where the
events hold; violations of every-run / good-event claims: {e16.get('det_viol', 0)} / {e16.get('good_viol', 0)}.

*Three levels.*  `Q_n = Q_{{n_o}} × (Q_{{n_o′}} × Q_{{n_i′}})`, `(n_o, n_o′, n_i′) ∈ {sorted(tuple(x) for x in th.get('sizes', []))}`, `u ∈ {{½, 1}}`:
outer Algorithm 2L⁺; on every fibre a middle Algorithm 2L⁺ whose *certified* accuracy is at most the
outer rung's and whose failure probability is the outer `δ′`; at the bottom real two-sample brackets;
all constants from the theorems; the declared cost of a middle call is the middle `C_max`.  (For run
time an outer point draws its bracket from a pool of independent middle runs on its fibre, as in
R8.)  **{th.get('outer_runs', 0)} outer runs, {th.get('middle_runs', 0)} middle runs, {th.get('bottom_brackets', 0):,} bottom brackets:**
invalid or too wide at the bottom {th.get('bottom_invalid', 0)}, in the middle {th.get('middle_invalid', 0)} / {th.get('middle_too_wide', 0)}, at the top
{th.get('outer_invalid', 0)} / {th.get('outer_too_wide', 0)}; violations of a claim of Theorem 11.56 at the middle level {th.get('middle_det', 0)} + {th.get('middle_good', 0)}, at
the outer level {th.get('outer_det', 0)} + {th.get('outer_good', 0)}; the outer number of queries stays a factor `e^{{{-th.get('max_lnq_minus_lnCmax', 0):.1f}}}` below its `C_max`.

*What these runs are worth.*  The cubes have 12–13 (two levels) and 9–10 (three levels) coordinates;
at these sizes an inner bracket costs more than enumerating its fibre, and the runs test the logic of
the nesting and the interface "bracket procedure" with real, independent randomness — not the cost.
"""

sec_d = f"""### 3.6 Adversarial search (`adversarial.py`)

Hill climbing with restarts over the radial profile (one increment in `[−u, u]` per shell), the position
of the reference point, the inner offset and the inner behaviour, with literal runs, one objective at a
time; every run is also checked for every claim.

| cell | objective (a ratio that the theorem bounds by 1) | literal runs | largest value found | violations |
|---|---|---|---|---|
{adv_table}

{adv_total} runs, no violation.  The search does not get closer to any bound than the structured instances of the
campaigns do (count inequality `{maxA('count_ineq'):.3f}` there); the engineering division's much larger search in
expectation reports `0.95` for the count and `1.8·M†` for the sample.  K's own runs report samples up to
`4.5·M†`, the theory division's harness `3.7·M†` on a "plateau, then cone" (91 % of the cap).

### 3.7 Overlap with ENG-RES-0008

Read after my implementation was written; their code was neither run nor read.  *Same:* the algorithm
(K_REPORT §2.2 with errata m1, m10), radial product instances with a reference shell and one inner
offset, the inner behaviours "bottom", "top", "random", the reduced-`K` experiment, the checks (iii)–(vi).
*Their side only:* expectation-level ("mean") runs with a search over instances at `n` up to `128 000`
(7 095 840 runs) and the worst-instance cost tables; 585 000 literal runs at three sizes
(`(u, n_o) ∈ {{(½, 300), (1, 120), (2, 48)}}`) with one design.  *My side only:* invalid inner answers and the
abort rule; Algorithm 2L of Theorem 11.52 and the extensive regime (their "not started"); ties on the
level grid; the cap remark of `40c5bd7`, including its degenerate branch; behaviours mixed within a run and
the two adversaries; real inner brackets and three levels; the comparison of `C_max` with the
non-adaptive *lower* bound (§2.9).  *Where we overlap the numbers agree:* `C_max`, the plain bracket, the
hinted lower bound and the flat-instance trajectory (§3.3), to every published digit.  My literal runs
with their profile families (flat, cones, plateau-then-cone, dips around the critical radius, the
staircase, the 2-periodic profile, random walks) show, like theirs, no failure of the good event with
the theorem's `K` and no violation.

### 3.8 How to re-run (from `experiments/science/ws_R6/`; `OMP_NUM_THREADS=1`)

    python3 campaign.py A_small 1600 11 2        # likewise A_ties 500 12, A_medium 500 13, D_2L 240 16,
                                                 # B_reducedK 400 14, B_invalid 400 15, B_lazy 60 19, D_2L_off 300 17
    python3 campaign.py MUT_neg_tol 48 7 2       # mutations: MUT_noharper, MUT_maxform, MUT_close_at_no, MUT_q_no_eta
    python3 capcorner.py 1500 41                 # seeds 41, 42, 43
    python3 e2e.py 600 21 1 ; python3 e2e.py 400 22 16 ; python3 three.py 40 61 6
    python3 adversarial.py <cell 0..6> <ineq|count|calls|cap|mbar|cost> <evaluations> <seed>
    python3 everyn.py 1.0 0.5 4000,16000 ; python3 separation.py 1.0 250,...,8000 ; python3 flat_exact.py 1.0 1000 0.80
    python3 check_tail_lemmas.py ; python3 check_K4cd.py ; python3 tau2.py
    python3 make_section3.py                     # every number of section 3.2, 3.4, 3.6 from the data files
    cd /home/user/MetricChain && lake env lean /home/user/MetricChain/experiments/science/ws_R6/lean/R6Axioms.lean

Campaigns are stopped by a time limit when the machine is loaded; the run counts above are those of the
data files in `data/`.  `NOTES.md` records what was run in which order, including what was discarded.
"""

s = open(REPORT).read()
for marker, text in (("<!--SECTION3B-->", sec_b), ("<!--SECTION3C-->", sec_c), ("<!--SECTION3D-->", sec_d)):
    assert marker in s, marker
    s = s.replace(marker, text)
OUT = os.environ.get("R6_DRY_OUT", REPORT)       # set R6_DRY_OUT=<file> to write a preview instead of the report
open(OUT, "w").write(s)
print("report sections written to", OUT, ";", "total literal runs in the table:", total_runs, "| valid 2L+:", valid_2lp, "| valid 2L:", valid_2l,
      "| invalid-answer runs:", inv_runs, "| e2e:", e1.get("runs"), e16.get("runs"), "| three:", th.get("outer_runs"), "| capcorner:", cc.get("runs"),
      "| adversarial:", adv_total)
