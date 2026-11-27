# Workstream R16 — notes (kept from the first minute)

Object: theory tree at commit 9befefd, read-only export
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_9befefd/` (= `<EXP>`).
I write only here (`experiments/science/ws_R16/`) and `docs/science/workstreams/R16_REPORT.md`.

Kinds of checking used below: **review** (re-derived), **replication** (own code from the
statement), **re-run** (their code), **read only**.

## Log

* 2026-11-26T08:43:51Z (clock: `date -u`) — started. Read `COMMON.md` and `R16_brief.md` in
  full. Created this directory (it did not exist before my `mkdir -p`; `R16_REPORT.md` did not
  exist). Machine: 4 cores, 15 GB total, load average 1.92 at start (other jobs running).
  `git status` shows untracked files of other workstreams (P8, pi_inference) — not mine, not
  touched.
* 2026-11-26T08:48:36Z — read in full: THY-RES-0013; theory report (export) §11.18 Theorem 11.52
  (lines 4556–4693), §11.19 Lemma 11.55, Theorem 11.56 + proof + two remarks (5008–5146),
  Prop. 11.57, Thm 11.58, remarks (1), (1a), (1b) (5216–5410); K_REPORT §§1.2–3.4 (algorithm
  2L+ text §2.2, statement §2.3, proof §2.4 nine steps, Prop. K0 §3.2, Thm K2 §3.4);
  three_levels_certified/README.md, cert3.py; reviews/R8/r8_flat.py.
  First reading (to be re-derived, not yet verdicts):
  - contract of an inner procedure = "bracket procedure" (§11.18 l.4544 / K_REPORT §1.3):
    for dimension d, accuracy x, failure prob δ′, cost C: at most C queries on ANY ψ∈L_u(Q_d)
    ALWAYS; returns L≤U with L≤A≤U and U≤e^x L except with prob δ′.
  - union bound over calls: (V1) of K_REPORT §2.4: potential calls (i,l), i≤K2^{m_max}, 1≤l≤L,
    each fails w.p. ≤δ′=δ/(4L M̄); L·K2^{m_max}·δ′ < 2L M̄ δ′ = δ/2.  So δ′ is per call and the
    union over all calls of all rungs is already inside the outer budget.
  - cert3 designs every two-level candidate with ldelta=ldeltap (outer δ′) and asserts
    xout ≤ x+1e-9.
  - message's b = x − ln(e^c(1+c)/(1−c)+2c) drops the (2p_u)^d term of the accuracy formula;
    code uses bmax = x − acc_const(c) − 1e-6 (cert3.py l.92) and breaks if xout > x+1e-9.
  - Thm 11.56's statement (l.5033–5037) puts the abort test "before every inner call";
    Thm 11.52's rule (l.4602–4606) puts it before every query incl. the one query of a new
    outer point.  To check: is the cost bound of 11.56 "always" with the test before inner
    calls only?  (points ≤ M̄ always? statement l.5039–5041 says so "for every run").
* 2026-11-26T08:57:18Z — own code written: `r16lib.py` (tables with exact integer binomials/balls,
  E_r and T_k by positive prefix/suffix sums; `Level` = constants of Thm 11.56; `k0` = Prop. K0 family;
  candidates and the choice rule), `r16_cert.py` (driver), `r16_validate.py` (cross-check against our
  R6 exact-arithmetic code, read-only import with `python3 -B`).
  Design ambiguities resolved by READING their code (marked [RESOLVED-BY-READING] in r16lib.py):
  (1) outer/middle ladder geometric x_l = x_0 (b/x_0)^{l/L} (r8_flat.py l.106) — NOT the ladder
  "ε*·0.85^i" of K_REPORT §6.4 / theory report l.5303–5304 that our R6 used; (2) n_o = floor(φ n) in
  floating point, clipped; (3) second extensive fraction clipped to 0.8, skip rule 2u(d−n_o) ≤ 1.5 b;
  (4) added candidates: b_max = x − ln(e^c(1+c)/(1−c)+2c) − 1e-6, descent 0.50…0.20 with three stop
  rules; (5) gates: no candidate when x/d ≥ 0.9 ε* or d < 50; added candidates only where the base
  bracket costs more than e^{0.2 d a}; (6) K0: M without the ceiling in theirs (I keep the ceiling
  below e^40 — invisible), enumeration when cheaper.
* RESULT (replication, logs/rep_4000.log, run reached its last line "peak RSS MB 38.2"; 2 s):
  n = 4000, u = 1, all 7 outer fractions × {two levels, tuned, searched}: 21 of 21 numbers equal to
  theirs (out_4000.txt) to the four digits given. Best: two 0.7262 (0.5), tuned 0.6331 (0.4),
  searched 0.6106 (0.375). Rungs served by two-level runs: φ=0.375 tuned 20-21, 28-40 (15); searched
  20-21, 24-40 (19); φ=0.40 tuned 21, 28-40 (14); searched 21, 24-40 (18) — as in out_terms_4000.txt.
* RESULT (logs/validate.log, reached last line; 1 s): r16lib vs R6 exact arithmetic: tables agree to
  7e-13 in ln; outer level (φ=0.375, 0.5) and two middle designs (bounded x=0.5 b=max φ₂=0.5;
  extensive x=50 φ₂=0.7466) in dimension 2500: J, r†, m_max, K identical; ln ν₀, ln M̄, ln δ′, x_out to
  1e-8; base-bracket costs to 1.1e-4 in ln (R6 rounds η to 1e-6); ln C_max to 1.7e-5. 0 checks differ.
* 2026-11-26T09:03:23Z — RE-RUN of their code from the export (python3 -I -B, nothing written into <EXP>:
  1240 files before and after, no __pycache__, none newer than my files):
  - summary.py → logs/rerun_summary.log: byte-identical to their stored out_summary.txt (diff empty).
  - cert3.py 4000 0.375 tuned,searched (through runpy so that the peak RSS is printed) →
    logs/rerun_cert3_4000_0375.log: two levels C_max 0.8553, tuned 0.6387, searched 0.6106; 30 s;
    peak RSS 36.6 MB; equal to their stored line and to my replication.
  - own error: my first attempt used /usr/bin/time, which does not exist here (exit 127, nothing ran,
    the log was overwritten by the second attempt).
* REPLICATION extended (own code is fast: no flat-instance simulation, only bounds):
  - per-rung tables: r16_compare_terms.py: n=4000 φ₁=0.375 and 0.40, modes tuned and searched: 1300
    fields (accuracy, multiplier kind/value, base cost, best candidate's certified bound and design
    string, server, term), 0 differ (logs/compare_terms_4000.log); n=16000 φ₁=0.30: 650 fields, 0
    differ (logs/compare_terms_16000.log).
  - all sizes of their table: logs/rep_{1000,1400,2000,4000,8000,16000,32000,64000}.log; every
    certified number of their out_*.txt (two-level C_max, tuned, searched, every (n, φ₁)): 159 of 159
    equal to four digits (logs/compare_all.log). Peak RSS at most 136 MB (n=64000, 67 s).
  - after the first runs I changed Tab to stream the exact integers instead of keeping lists (memory
    at n=64000); all logs listed here were produced AFTER that change (re-run 08:59–09:02Z).
* 2026-11-26T09:07:34Z — further replication facts:
  - (1b)'s example (n=4000, φ₁=0.40, rung 27, x=9.845, d=2400): base bracket 0.5122 ✓; the referee's
    first extensive design (φ₂ = g/(g+θ_hint(g)) = 0.1312, n_o′=314) certified 0.7041 ✓ (flat cost
    0.2233: theirs, NOT replicated — I have no flat-instance evaluator); the second design
    (1.5× → 0.1968) is certified 0.6638, still above the base bracket.
  - ordering searched ≤ tuned ≤ two holds at all 54 (n, φ₁) of my logs (as printed).
  - extra fractions at n=4000 (logs/rep_4000_extra_fractions.log): two levels 0.7829/0.8369/0.8934
    at φ₁=0.55/0.60/0.65 (so the two-level minimum 0.7262 at 0.50 is the minimum of the wider grid;
    these three equal the engineering division's certified column at those fractions as copied in
    their summary.py); searched 0.6180, 0.6120, 0.6106, 0.6140, 0.6248 at φ₁ = 0.36, 0.37, 0.375, 0.38,
    0.39: the grid value 0.6106 is not improved by a finer grid.
  - read ENG-RES-0014 (copy in scratchpad eng_ce71724/, full text) and the passages of ENG-RES-0008
    (scratchpad copy) on mean runs / literal runs: "Everything is at the level of expectations (every
    count replaced by its mean)"; literal runs only at n_o ∈ {300, 120, 48}, n_i = 6; "On the flat
    instance the run is deterministic and the number of evaluations is exact".
    ⇒ for Item 4: the two-level "worst instance found" is a MEAN-RUN cost (model), except the flat
    instance, where the run is deterministic and the cost exact.  Two-level flat costs per fraction
    (their table three_worst): n=4000 min 0.5519 at φ=0.65 (< certified three-level 0.6106!);
    n=16000 min 0.5126 at φ=0.55 (> certified three-level 0.4782).
* 2026-11-26T09:18:29Z — ITEM 4, two facts found:
  (F-a) RE-RUN of their r8_flat.flat_run on a fine grid of the outer fraction (step 0.01, 0.30…0.85;
  driver r16_rerun_flat2.py; logs/rerun_flat2_a.log reached its last line, 131 s, 68 MB;
  logs/rerun_flat2_b.log for n=32000, 64000 still running when this line was written).
  Exact (deterministic) two-level cost at the flat instance, minimum over φ, against my certified
  three-level bound ('searched'):
     n=2000: 0.5818 (φ=0.68) vs 0.8118 → three-level bound NOT below at 38 of 56 fractions
     n=4000: 0.5336 (φ=0.63) vs 0.6106 → NOT below at 16 of 56 fractions (φ 0.56…0.71)
     n=8000: 0.5110 (φ=0.59) vs 0.5262 → NOT below at 3 of 56 fractions (φ 0.58…0.60)
     n=16000: 0.5027 (φ=0.56) vs 0.4782 → below at every fraction (+43 nats)
     n=32000: 0.4998 (φ=0.54) vs 0.4439 → below at every fraction (+198 nats)
  ⇒ "three levels beat two levels" WITHOUT search and WITHOUT the mean-run model holds from
  n = 16000 on (flat instance as witness, every φ of the fine grid); at n = 4000 and 8000 the claim
  needs non-flat instances evaluated as mean runs for φ in [0.56,0.71] resp. [0.58,0.60].
  Side observation: the flat-tuned two-level cost at n=32000 (0.4998) is below τ₂/a = 0.5004; the
  flat-tuned figures of remark (1) (0.55, 0.52, 0.51) are grid-limited (their grid 0.3,0.4,0.5,0.55,…).
  (F-b) The two-level worst cases at n = 1400, 2000, 8000, 32000, 64000 are from ENG-RES-0008, whose
  design has the ladder "inner rates ε*·0.85^i (i<40)" (its §1, line 84), NOT the geometric 40-rung
  ladder of the table's outer design (ENG-RES-0014 §2 uses the latter: n = 1000, 4000, 16000).
  Check with own code (r16_ladders.py → logs/ladders.log, reached last line): with the ε*·0.85^i ladder
  the two-level certified C_max at φ=0.50 is 0.9913, 0.8700, 0.7228, 0.6387, 0.5887, 0.5596, 0.5419 at
  n = 1400 … 64000 and 1.1720 at (1000, 0.55) — exactly ENG-RES-0008's column "cap C_max at that φ"
  (0.991, 0.870, 0.723, 0.639, 0.589, 0.560, 0.542; 1.172); with the geometric ladder it is 0.9933,
  0.8721, 0.7262, 0.6415, 0.5899, 0.5646, 0.5407 (the table's two-level column).  So (β)'s "the
  two-level algorithm of the same outer design" is not what was computed at n = 8000, 32000, 64000.
  Size of the effect where both ladders were searched (reading (A)): 1.040 (φ=0.55) vs 1.0461 at
  n=1000; 0.694 vs 0.6940 at 4000; 0.576 vs 0.5753 at 16000 — at most 0.006, against margins ≥ 0.09.
* 2026-11-26T09:24:54Z — TOOL DECLINED AN ACTION (recorded as the brief requires): the Bash tool blocked a
  foreground command of the form "sleep 60; cat <my log>" (a wait for my own background job; the
  message said to use a background run or a monitor instead of a foreground sleep).  I did not retry
  it and did not chain shorter sleeps; the background job's completion notice arrived by itself and I
  then read the log.  Nothing was lost.  (Two earlier commands "sleep 45; grep …" and "sleep 100;
  grep …" had been accepted and had run.)
* 2026-11-26T09:25:06Z — more results:
  - logs/rerun_flat2_b.log (reached last line; 453 s; peak 162 MB): n=64000: exact flat two-level min
    0.4961 at φ=0.53 vs certified three-level 0.4381 → below at every fraction (+412 nats).
    Note 0.4998 (32000) and 0.4961 (64000) are BELOW τ₂/a = 0.5004: τ₂/a·na is not a finite-n lower
    bound on what the two-level algorithm as built pays (flat instance, base brackets' own answers).
  - logs/rerun_flat2_local_16000.log (reached last line; 145 s): every second n_o in [8880, 9120] at
    n=16000: minimum 0.4991 at n_o=9024 — so the minimum over the outer dimension is 0.499, not the
    grid value 0.5027; still 0.021 n a = 37 nats above the certified three-level bound 0.4782.
  - own code, extra outer fractions (not in their outputs; logs/rep_*_extra_fractions.log):
    n=64000: searched 0.4772/0.4364/0.4341/0.4559/0.4558/0.4768 at φ₁=0.15/0.225/0.275/0.30/0.35/0.40
    → 0.4341 at φ₁=0.275 is below their 0.4381 (0.25);  n=32000: 0.4575 (0.225), 0.4629 (0.275) → their
    0.4439 (0.25) stands;  n=8000: 0.5259 (0.325) vs their 0.5262 (0.30).
  - K_REPORT §6.4 (l.843–844) says "geometric ladder of 40 inner rates"; remark (1a) (l.5303–5304) and
    ENG-RES-0008 say "inner rates ε*·0.85^i"; the referee's flat_run uses x_l = x₀(b/x₀)^{l/40}.  Both
    are "geometric ladders of 40 rungs" — that is how the two designs came to be treated as one.
* 2026-11-26T09:34:16Z — REPLICATION of the two-level flat cost with OUR OWN engine (R6's literal engine,
  exact arithmetic, + an oracle returning the base bracket's deterministic answer on the zero fibre;
  r16_flat_own.py; the memory-light copy of the engine loop r16_flat_own_light.py for n=16000):
  (1000, 0.50): 0.9839 [both variants of the tail radius: r* and the integer-M r^]  — theirs 0.9839
  (4000, 0.50): 0.6670, levels 20765 (20002 populated, 762 negligible), closing radius 603 — theirs 0.6670
  (4000, 0.63) variant int: 0.5336 — theirs (fine grid minimum) 0.5336
  light engine at (4000, 0.50): identical to the unmodified engine (0.6670, 20765 levels, 118885 passes,
  radius 603, width 0.7830), 69 MB instead of 198 MB.
  (8000, 0.59) and (16000, n_o=9024): see the lines above this entry in the terminal / the logs.
  Own error recorded: I first asserted r^ = r* for the base bracket; false with the integer M of
  Prop. K0 at the coarsest rungs (12 of 40 at n=1000); both conventions give the same cost to 4 digits.
* REPORT first full draft written to docs/science/workstreams/R16_REPORT.md (placeholders FLAT8000,
  FLAT16000 to be filled from the two logs).
* 2026-11-26T09:37:15Z — (8000, 0.59), own engine (logs/flat_own_8000_059_rstar.log, reached last line, 172 s,
  peak 888 MB): 0.5110 — theirs 0.5110.  (16000, n_o=9024) with the light engine: started 09:29:55Z,
  still running; it will be stopped by me if it approaches 20 minutes (the limit of the brief).
  - sensitivity check for Item 1(ii) (own code): the server of the finest rung at n=4000, φ₁=0.375
    (bounded, b=max, φ₂=0.5): designed for the outer δ′ (ln δ′ = −253.9): K′ = 496086, certified
    0.5291; designed for δ = 0.05: K′ = 44461, certified 0.5219.  So the digits do show which failure
    probability the candidates are designed for — it is δ′.
  - max(x_out − x_l) over all chosen servers in all logs/rep_*.log: values 0, −7.11e-15, −1e-06, −0.054.
  - two-level certified bound at n=32000 on a finer grid (own code, logs/rep_32000_two_fine.log):
    0.5725 (0.48), 0.5622 (0.49), 0.5646 (0.50), 0.5748 (0.51): the table's 0.5646 is grid-limited.
  - K's script flat_cost_bounded.py l.66: rates = estar*0.85**i — KR §6.4's "geometric ladder of 40
    inner rates" is the ε*·0.85^i ladder (read only, one line).
  - (β) at n=4000 on the division's grid: the exact flat two-level cost exceeds the certified
    three-level bound 0.6106 at 9 of its 12 fractions (0.25…0.55: 0.9299…0.6133; 0.75: 0.6378; 0.80:
    0.6841) and not at 0.60, 0.65, 0.70 (0.5592, 0.5519, 0.5973), where the mean-run worst cases are
    0.7936, 0.8466, 0.9027 (margins 81, 105, 130 nats).
* 2026-11-26T09:39:39Z — I STOPPED my own job r16_flat_own_light.py 16000 n_o=9024 (PID 28137, kill of that one
  PID) after about 10 minutes: from their evaluator's summary of the same cell (npop 80002, nneg 4234,
  last sample K·2^1243) the pass-by-pass engine needs about 2.6 million passes, i.e. more than the
  20-minute limit.  Its log did not reach the last line (a line saying so was appended) and is not
  cited.  Plan: an exact shortcut for the levels at which no point can be high (closure and
  negligibility are monotone in the sample size there, so the last pass can be found by bisection),
  validated against the unmodified engine at n=4000 and 8000.
* 2026-11-26T09:43:06Z — r16_flat_own_fast.py (copy of R6's engine loop with the exact shortcut at levels where
  no point can be high) VALIDATED against the unmodified engine: (4000, 0.5): 0.6670, 20765 levels
  (20002/762), K·2^239, radius 603, width 0.7830 — identical, 6 s instead of 20 s; (8000, 0.59):
  0.5110, 42082 levels (40002/2079), K·2^620, radius 1373, width 0.7869 — identical, 18 s instead of
  172 s.  Then (16000, n_o=9024): 0.4991, 84237 levels (80002/4234), K·2^1243, radius 2577 (r† 2309),
  width 0.7860; 79 s, 187 MB (logs/flat_own_fast_16000_no9024_rstar.log, reached last line) — theirs:
  0.4991, npop 80002, nneg 4234, last m 1243.  So the two-level flat cost is now REPLICATED at five
  cells: (1000, .50) 0.9839; (4000, .50) 0.6670; (4000, .63) 0.5336; (8000, .59) 0.5110; (16000,
  n_o=9024) 0.4991.  Running: (32000, 0.54) in the background (their value 0.4998).
  - m1: in the 2648 stored runs of our R6 harness (rule "before every inner call"; 142 budget
    aborts) no run has more than C_max queries (field q_le_Cmax; read from ws_R6/data/*.jsonl).  I did
    not construct a run that exceeds C_max; the finding is about what the stated rule proves.
* 2026-11-26T09:45:51Z — housekeeping: every log cited in the report ends with "peak RSS MB".  Their summary.py
  prints none, so I re-ran it through runpy (logs/rerun_summary_runpy.log, identical output, diff
  empty).  Logs NOT cited because their runs did not reach the last line: flat_own_1000_050.log (my
  wrong assertion), flat_own_light_16000_no9024_rstar.log (stopped by me), rerun_cert3_time.txt
  (/usr/bin/time missing).  Export still 1240 files, no __pycache__.
* 2026-11-26T09:49:16Z — V-shape check (from the re-run logs): on the grid of step 0.01 the exact two-level flat
  cost is strictly decreasing to the left of its minimum and strictly increasing to the right, at
  n = 4000, 8000, 16000, 32000, 64000 (at n = 2000 not strictly on the right).  Ends of the grid at
  n = 16000: 0.7718 (0.30), 0.7657 (0.85); 32000: 0.7467, 0.7851; 64000: 0.7297, 0.8006.

## File inventory (experiments/science/ws_R16/)

* r16lib.py — own library (tables, constants of Thm 11.56, Prop. K0, candidates, the rule).
* r16_cert.py — driver (certified bounds; --terms for per-rung tables).
* r16_validate.py — cross-check against our R6 exact arithmetic.
* r16_compare_all.py, r16_compare_terms.py — comparisons with their stored outputs (read only).
* r16_ladders.py — M1: the two ladders.
* r16_rerun_flat2.py, r16_rerun_flat2_local.py — RE-RUN drivers of their r8_flat.flat_run (python3 -I -B).
* r16_flat_own.py — own replication of the two-level flat cost with R6's engine (unmodified).
* r16_flat_own_light.py — the same with a copy of the engine loop that keeps one pass record per level.
* r16_flat_own_fast.py — the same with the exact shortcut (validated at n = 4000, 8000).
* logs/ — every log; the three that did not reach their last line are named above and not cited.
* 2026-11-26T09:51:38Z — own engine with the exact shortcut: (16000, 0.56): 0.5027 (theirs 0.5027), 84220
  levels (80002/4217), K·2^1238, radius 2556, 76 s; (32000, 0.54): 0.4998 (theirs 0.4998), 168528
  levels (160002/8525), K·2^2482, radius 4855 (r† 4484), width 0.7808, 430 s, peak 387 MB.  Both logs
  reached their last line.  Two-level flat cost now replicated at SEVEN cells: (1000,.50) 0.9839;
  (4000,.50) 0.6670; (4000,.63) 0.5336; (8000,.59) 0.5110; (16000,.56) 0.5027; (16000,n_o=9024)
  0.4991; (32000,.54) 0.4998.  64000: re-run only (0.4961 at 0.53).
* Report completed (no placeholder left).  Final state: findings M1 (major), m1, m2, m3 (minor),
  o1–o3 (observations); requests R16-THY-1 … 6.
* 2026-11-26T09:52:07Z — final proofreading of the report done; hand-back follows.  No process of mine is
  running (checked with ps).  Nothing was written outside experiments/science/ws_R16/ and
  docs/science/workstreams/R16_REPORT.md; nothing in <EXP> (1240 files, no __pycache__) or in ws_R6.
* 2026-11-26T09:52:59Z — after that line two wordings in report §6 were updated (R16-THY-4: the flat costs are
  now also replicated by our own engine up to n=32000; R16-THY-6: below τ₂/a at 32000 AND 64000).
  Report: 706 lines.  Handing back.
