# Workstream R18 — running notes (referee of ENG-RES-0014 §1 and §4)

Internal review, not external peer review.  Times are read from the clock (`date -u`) at the moment of writing.

Object: engineering branch at `1cc4e1c`, read-only export
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro_1cc4e1c/` (= `<ENG>`).
Write only here (`experiments/science/ws_R18/`) and `docs/science/workstreams/R18_REPORT.md`.

## Log

* 2026-11-26T16:02Z — started.  Read `COMMON.md` and `R18_brief.md`.  `git status --short` (read-only) shows only
  the two untracked briefs R18, R19.  Directory `ws_R18/` created, this file opened.
  Plan: (1) read ENG-RES-0014 §0/§1/§4/limitations, ENG-RES-0008, ENG-MSG-0003 §5, R6/R16 reports, r6lib.py,
  r16lib.py, their `meanrun.py`, `alg2l.py`, `simulate.py`, the two check scripts, the tests;
  (2) re-derive §1 line by line; (3) own literal loop vs closed rule + failing control; (4) re-derive §4;
  (5) own non-product instances + failing control; (6) re-run their two checks from `rerun_copy/`;
  (7) assumption table; (8) report.

## Tool actions declined

(none so far — kept current at the end of this file as well)

## Own errors (kept as they happen)

* E1 (16:10Z): the entry below was first stamped "16:30Z", a time I had guessed before reading the clock; the clock
  said 16:10:32Z.  Corrected here.  Rule from now on: `date -u` is run first and its output is pasted.
  **Repeated at 16:19Z** (the re-run plan was first stamped "16:21Z"; clock: 16:19:36Z; corrected).  From now on the
  stamp is produced by `$(date -u ...)` inside the command that appends the entry, never typed.

* E2 (16:17Z): a planning run of their Python reference at n = 16 000 without a memory guard peaked at 6 457.5 MB
  (limit 2 GB); details in the log entry of 16:17Z.  Since then every run of their code is under a 2 GB
  address-space limit.
* E3 (16:50Z): `r18_corner.py part1`, first version: mean run fed `Fr(float)` where the instance has an exact tie;
  details in the log entry of 16:52Z.  No number of that version is used.
* E4 (16:54Z): **three** compute processes for about 25 s (limit: two): `r18_corner.py part1` and the chunk
  `cost_n8000_u0.5` of sequence B were running in the background when I started `r18_diag_n1400.py` in the foreground
  (20 s, 257 MB); the 1-second `r18_compare_rerun.py` at 16:53:14Z also overlapped.  Nothing failed.  From now on
  `ps` is read before every start.

## Log (continued)

* 2026-11-26T16:10Z — READ so far: ENG-RES-0014 (all), ENG-RES-0008 (all), `meanrun.py`, `ckernel.py`,
  `alg2l.py`, `simulate.py`, `adversary.py`, `run_search.py`, the two check scripts, K_REPORT §2.2–2.4 (the algorithm
  text: step 1 "while U_i > s_j and L_i ≤ s_j e^{−b} move to the next rung ... then low if U_i ≤ s_j and high otherwise"),
  theory report Thm 11.56, our `ws_R6/r6lib.py` (literal engine with per-class anchor offset `kap = u n_i − t0` and
  per-class strategy: usable for non-product places).

  First derivations (paper, mine; to be tested numerically before being believed):
  - Notation w = ln W − ln s.  At rung l: unclassified iff −B_l < w ≤ A_l − b; LOW iff w ≤ −B_l; HIGH iff
    w > max(A_l − b, −B_l) =: h_l.  B_l nonincreasing (intersection).  Exit rung l*.
    HIGH ⇒ w > h_{l*} ≥ min_l h_l = −c.  LOW ⇒ w ≤ −B_{l*} ≤ −B_l ≤ h_l for l ≥ l*; for rungs passed at this level
    w ≤ A_l − b ≤ h_l; for rungs passed at EARLIER levels s' < s: w' ≤ A_l − b and w < w' (levels increase) ⇒ same.
    So LOW ⇒ w ≤ −c.  Rule holds per point, any admissible positions, with persistent rungs, ties included
    (W = s e^{−c} is LOW).  Needs: B_l nonincreasing (automatic), A_L + B_L ≤ x_L ≤ b (exit by rung L),
    levels visited in increasing order, bracket of (point, rung) independent of the level at which it is asked.
    A_l monotone is NOT needed.  0 ≤ c ≤ b needs A_l ≥ 0, B_L ≥ 0, α_L ≤ x_L ≤ b.
  - "bottom ⇒ c = b": c = max(min(b − t0, x0 − t0), min(b, x0 − t0, x_1)); equals b iff x0 − t0 ≥ b AND x_1 ≥ b
    (or t0 = 0).  The message omits "x_1 ≥ b"; true in X-005 because `design_params` ends every ladder with x_L = b
    exactly.  With L = 1, x_1 < b: c = x_1 < b.  CANDIDATE FINDING (minor, condition to add).
  - "top ⇒ c = 0": c = max(0, min(b − t0, x0 − t0)); zero iff t0 ≥ b (or t0 = x0).  x0 − t0 ≥ b not needed for top.
  - range of t0: from |ψ(a,b) − ψ(a,0)| ≤ u|b|: W ∈ e^{−ψ(a,0)}[((1+e^{−u})/2)^{n_i}, ((1+e^{u})/2)^{n_i}],
    so t0 ∈ [n_i(u − Λ1), n_i(2u − Λ1)], both ends attained (cones ±u|b|).  OK.
  - window of rung l: L ≤ s e^{−b} and U > s ⇔ W e^{b−A_l} ≤ s < W e^{B_l}: exact, non-strict left, strict right.
    calls_{l+1} = #{i : ∃ j ≤ j_stop, j ∈ win_l(i), i ≤ M_j} by nestedness in l (per point).
  - §4: c(t0) constant on the feasible range iff lo ≥ b (top) / x0 − hi ≥ b and x_1 ≥ b (bottom): needs
    n_i·min(u − Λ1, Λ1) ≥ b.  To be checked on all 468 cells (min n_i = 38 ⇒ 38·0.219 = 8.3 ≥ 0.5 expected).
    The evaluator's pair mode computes c from (A0, B0) = (hi, x0 − lo): outside the range this is not the shift of any
    fibre — no guard in `rung_positions`.  CANDIDATE FINDING (to test with a design having lo < b ≤ hi).
  - In the X-005 designs x_1 = ε* n_i ≤ min(lo, x0 − hi), so windows of rungs l ≥ 1 do not depend on the place at all:
    the union changes calls_1 only (the cheapest inner procedure).  To be confirmed numerically.
  - Both check scripts import `ckernel.Evaluator` (C kernel, compiled on first use).  The brief forbids building it:
    plan = an adapter in `rerun_copy/` that provides `Evaluator.run` through their Python reference `meanrun.mean_run`.

* 2026-11-26T16:17Z — scratch copy `rerun_copy/` made (their files by `cp -p`, sha256 identical to `<ENG>`; the C
  kernel source is NOT copied; their `ckernel.py` kept as `ckernel_THEIRS_not_used.py.txt`; my adapter installed as
  `rerun_copy/src/metricchain_eng/twolevel/ckernel.py`, source of truth `r18_ckernel_adapter.py`).  `.gitignore` in
  `ws_R18/` excludes `rerun_copy/`.
* 16:17Z — planning run `r18_time_reference.py 1000 16000` (their Python reference on six stored maximisers,
  phi = 0.5): values reproduced to the 6 decimals printed, BUT **peak RSS 6457.5 MB** (limit of the brief: 2 GB).
  **Own error E2**: I started a run of their reference at n = 16 000 without a memory guard.  It lasted under a
  minute and finished; nothing else on the machine was disturbed as far as I can see (another workstream's job at
  1.4 GB kept running).  Candidate causes and their sizes: (a) `_range_max` in their `meanrun.py` caches one array
  of length j_stop+1 per distinct window length, and the windows clipped at j_stop have one length per atom:
  8001 atoms × 99 579 levels × 8 B = 6.37 GB at u = 1, n = 16 000 — matches the peak; (b) the cube tables and the
  law: 3 arrays of 8001 floats — 0.2 MB; (c) numpy/scipy import — about 60 MB.  So (a).  Consequence: their
  Python reference cannot evaluate the large cells within 2 GB (the need grows like n_o·j_stop: ×64 from 16 000 to
  128 000).  From now on every run of their code is started under `ulimit -v`.
  Timing of their reference per mean run (phi = 0.5): n = 1000: 0.05–0.28 s; n = 16 000: 10–29 s.

* 2026-11-26T16:19Z — RE-RUN PLAN (written before the runs, as the brief asks for runs above five minutes).
  What: their `recheck_classification.py` and `nonproduct_bound.py`, verbatim (runpy), from `rerun_copy/chunks/<key>/`,
  `python3 -I -B`, their Python reference `meanrun.mean_run` through the R18 adapter, address space limited to 2 GB
  in-process (`RLIMIT_AS`), one chunk at a time in one background process.
  Cost per step: one mean run of their reference took 0.02 s at n = 250 (5.9 s for the 288 runs of chunk cost_n250,
  83 MB) and 0.05–0.28 s at n = 1000; it grows roughly like n² (atoms × levels), so about 3 s at n = 4000.
  Steps: per chunk 2 runs per stored search: 288 runs for a whole-n chunk (n ≤ 1400), 96 for an (n, u) chunk.
  Expected: n = 350: 12 s; 500: 25 s; 700: 50 s; 1000: 100 s; 1400: 190 s; 2000: 3 × 130 s; 4000: 3 × 510 s
  (each chunk under 10 min); `claims_n1000` 160 s; `converge_n1000` 10 s; the same again for `nonproduct_bound`
  (job cost only).  Total about 80 min of one core.
  Not attempted: n ≥ 8000 — memory of their reference ≈ (n_o+1)(j_stop+1)·8 B (measured 6.46 GB at n = 16 000,
  about 1.6 GB expected at n = 8000, u = 1, phi = 0.5, more at larger phi and u) and about 12 s per run.
  Compared with: (i) their stored per-cell values in `<ENG>/experiments/eng/twolevel/results/
  x005_recheck_classification.json` (`stored_worst`, `exact_worst`) and `x005_nonproduct_bound.json`
  (`worst_product`, `worst_bound`, `max_gap`) cell by cell; (ii) the counts of the tables `recheck_classification`
  and `nonproduct` of ENG-RES-0014 restricted to the cells re-run.
  Stale directories `rerun_copy/chunks/{cost,claims,converge,converge2}_n<n>` for n ≥ 2000 without the `_u` suffix are
  from the first version of `r18_make_chunks.py`; unused, left in place (no wildcard deletion).

* 2026-11-26T16:24:27Z — ITEM 1 REPLICATION DONE (`r18_rule.py`, own literal loop from the text of step 1, exact integer
  arithmetic in units of 1/4 and 1/64; log `logs/rule_seed18_n100000.log`, 39.5 s, 12 MB).
  Rule and window: 15 191 163 literal decisions (156 789 exactly on the threshold W = s e^{-c}; U = s met 138 328 times,
  L = s e^{-b} met 320 930 times — sums of the columns ties_U, ties_L), 4 behaviours (bottom, top, centre, any admissible pair
  incl. narrower than x_l) × 2 grids, places over the whole of [0, x0] with the two corners over-sampled, the point
  present at an arbitrary subset of increasing levels with its bracket kept:
  **rule violations 0; unclassified 0; c outside [0, b] 0; 2 400 374 window checks (first level at which rung l+1 is
  called = first present level in W e^{b−A_l} ≤ s < W e^{B_l}), violations 0.**
  Controls, all fail as they must: min/max exchanged 50 105 decisions wrong; tie given to HIGH 156 789 (= every
  tie); no intersection 174 447 (0 for "top", where the running minimum changes nothing); window strictness
  exchanged 360 035; old convention (c = b / c = 0) outside its range 210 177 of 6 220 655 decisions; ladder with
  x_L > b: 21 951 points left unclassified at the last rung.
  **Finding F1 confirmed by the literal loop (block D):** "bottom" with t0 ≥ b and x0 − t0 ≥ b but x_1 < b (allowed
  by Theorem 11.56: only x_L ≤ b is asked): c = x_1 < b in 100 000 of 100 000 cases, c = b in none; 139 144 of
  3 396 825 literal decisions contradict the convention c = b, none contradicts the exact rule.  With x_L = b
  (every X-005 design: `design_params` appends b to the ladder) c = b in the range: 0 exceptions.
  My closed forms c_bottom = max(min(b−t0, x0−t0), min(b, x0−t0, x_1)), c_top = max(0, min(b−t0, x0−t0)): wrong in 0
  of 400 000.

* 2026-11-26T16:32:07Z — OWN MEAN RUN (`r18_mean.py`: exact integers for probabilities / populated test / radii, Fractions
  for every logarithm compared with a level, mpmath 50 digits for magnitudes; per-atom place, positions and shift)
  AGAINST THEIR PYTHON REFERENCE (`r18_xcheck.py`, log `logs/xcheck_seed1_150.log`, 104 s, 77 MB; their code under
  `ulimit -v 2 GB`): 150 random designs (u ∈ {½,1,2}, n ≤ 240, λ ∈ {1/5,¼,½,1}, η ∈ {1/20,¼,½}, ladders ending at b or
  below it), 2 profiles each.  Runs compared 2 700 (bottom 300, top 300, explicit positions 300, corner places 600,
  old convention 600, their pair mode 600), 1 057 582 levels: status, stopping level, closing radius, the sample
  size of EVERY level, ln calls of every rung, ln cost, ln C_max, constants (J, K, r†, m_max): **0 mismatches** —
  once ONE convention of theirs is reproduced (next item).
  Controls: old convention at a corner place where the exact shift differs: their reference's run changes in 257 of
  301; lo/hi exchanged: calls of some rung fall below the product instance's in 243 of 600 runs (union: 0 of 600).
* same time — **Mismatch found first, and its cause (sizes of the candidates):** before the convention was reproduced, 36 of 108
  runs of the first 6 designs differed in the sample size of 1–2 levels each (status, stopping level, cost within
  1e-8 unaffected).  Candidates: (a) their test "populated at pass m" is `m ≥ −log2 P(HIGH) − 1e-12`, i.e.
  2^m·P(HIGH) ≥ 2^(−1e-12) = 1 − 6.93e-13, where the mean count gives N = M·P(HIGH) ≥ K only for 2^m·P(HIGH) ≥ 1;
  with n_o ≥ 41 the extreme shell has probability 2^(−n_o) < 6.93e-13, so at the levels where only that shell is LOW
  theirs is populated at M = K and the exact mean count is not (K(1 − 2^-43) < K).  With this tolerance
  put into my run (`pop_tol`) all 36 vanish, and all 2 700 runs agree: (a) explains every mismatch.
  (b) a bug in my loop — would not vanish by a change of one threshold.  (c) rounding of ln s_j — I use exact
  Fractions and they use a 1e-9 tie rule; the instances are on rational grids: no mismatch left to explain.
  Size of the convention's effect, my run with and without it, 600 runs: sample sizes change in 154 runs (4 513 levels);
  largest |Δ ln cost| = 0.0345; smallest n_o with a change 43, as predicted (2^-41 < 6.93e-13 < 2^-40).
  Reading: "N ≥ K" at P(HIGH) = 1 − ε is itself an artefact of taking means (a literal run has N = K with
  probability (1−ε)^K); their tolerance removes it for ε < 6.9e-13 only.  Candidate observation, not an error.

* 2026-11-26T16:40:27Z — ITEM 2, MEAN-RUN LEVEL (`r18_nonproduct.py main 120 5`, own evaluator; log
  `logs/nonproduct_main_seed5_120.log`, 139.6 s, 22 MB): 120 designs (every fourth the X-005 design at n ∈ {60,100,150,250},
  the others random), radial laws, both uniform behaviours, 7 placement patterns each (two places and three places
  correlated with W in both directions; shells split 1:2; a random place per shell; for every atom the dearest place
  of a grid of 17).  **1 680 instances that are not products, 946 694 levels: sample size of a level different from
  the product instance with the same law: 0.  14 168 rung checks: calls above the bound (A0 = hi, B0 = x0 − lo): 0;
  cost above the bound's: 0; bound below the product instance: 0.**  Control lo/hi exchanged: exceeded in 1 661 rung
  checks, in 678 of the 1 680 instances.  Every pattern attains the bound exactly in some case (share 1.000000): the
  bound is the exact maximum over joint laws of place and average there, not only a bound.  The union changes the
  calls of a rung beyond the first in 16 of 240 (design, behaviour) pairs (all in random designs).
  With my toy inner costs (ln C_l = 2 + 3l — inputs, not theirs) the largest ln(bound/product) is 8.92.
* same — ITEM 2, AN ACTUAL ψ (`r18_nonproduct.py explicit`, log `logs/nonproduct_explicit.log`): ψ(a,b) = F(|a|) + σ(|a|)·u·|b|,
  σ from +1 to −1 by 1/(2 n_i) per outer shell, F = 0 or F = u·|a|; u-Lipschitz on every edge (checked on all
  (|a|,|b|) transitions); places sweep the whole of [lo, hi]; F = 0 gives "high W at hi", F = u·d gives "high W at lo".
  12 (instance, behaviour) cases: one shift for all fibres; sample sizes equal to the product instance's (reference
  fibre's place) in 12 of 12; bound holds in 12; control violated in 12.  The instance costs MORE than the product
  instance with its law in 6 cases (calls of I_1 up to ×4.1: 7.30e7 against 1.78e7 at u = 2, n_o = 24, n_i = 4,
  F = u·d, bottom) and attains the bound to 4 digits in 3 (u = 2, F = 0, bottom and top; u = 2, F = ud, top:
  2.510e8 of 2.513e8).  So "an amount that is a bound and not the cost of an instance" (ENG-RES-0014 §4, Reading)
  is not generally so: the bound is attained by instances, at least at these sizes and with these inner costs.
* same — LITERAL RUNS, first pass (`r18_literal.py 3 18`): 54 runs, identity (literal calls = own-window count with the
  realised sample sizes) violated 0, union window violated 0, control exceeded in 54, sample sizes identical to the
  product instance on the same outer sample in 54; single runs above the MEAN-RUN bound: 32 (largest ratio seen
  1.01) — the mean-run bound is a statement about mean runs, not about samples.
  PLAN for the full run (more than five minutes): `r18_literal.py 100 18`: 18 cases × 100 literal runs + 100 product
  runs on the same sample; cost per (literal + product) run 0.34 s measured ⇒ about 10 min, 50 MB; compared with:
  the identity and the union inequality (must be 0 violations), the control (must be > 0), and the mean-run calls of
  `r18_mean.py` (means over runs expected within about 1 %).

* 2026-11-26T16:53:12Z — RE-RUN, sequence A finished 16:48:17Z: 26 chunk logs, every one ends with "R18-RUNNER done … exit=0"
  (recheck: cost n = 250…4000 (14 chunks incl. the u-splits), claims n = 1000, converge n = 1000; nonproduct: cost
  n = 250…4000).  Largest peak RSS 1 691.9 MB (nonproduct, n = 4000, u = 2), longest chunk 390.9 s.
  PLAN sequence B (runs above five minutes possible): the three chunks with n = 8000, u = 0.5 — recheck cost, nonproduct
  cost, recheck claims.  Cost per step: at n = 4000, u = 0.5 one mean run of their reference took 0.48 s and the
  chunk 357–374 MB; expected ×4 in time and memory at n = 8000: about 190 s per cost chunk (96 runs), 320 s for the
  claims chunk (160 runs), about 1.5 GB — under the 2 GB address-space limit, which stops the run otherwise
  (then the log goes to `not_cited/`).  Compared with: their stored per-cell values, as for sequence A.
  n = 8000 with u = 1, 2 and every n ≥ 16 000 are NOT attempted: their reference would need about 3.3 GB and more.
* same — LITERAL RUNS, full (`logs/literal_seed18_100.log`, 435.6 s, 47 MB): 18 cases (3 sizes × {ψ+ actual, ψ− actual, two
  places simulated} × {bottom, top}), 1 800 literal runs of r6lib at the theorem's K (855–927), all closed.
  **identity (literal calls of every rung = count over the point's own windows with the realised sample sizes): 0
  violations; union window: 0 violations; control lo/hi exchanged: exceeded in 1 800 of 1 800 runs; sample sizes and
  counts of every level identical to the product instance on the same outer sample: 1 800 of 1 800.**
  Against the mean run: stopping level and largest sample equal to the mean run's in 100/100 runs of 17 cases and
  in 68/100 of one (ψ+, u = 2, top); means of literal calls within 2 % of the mean run in 12 cases, but off by up to
  28 % at u = 2 (ψ−, bottom: 9.31e7 literal against 7.30e7; ψ−, top: 3.16e8 against 2.51e8; ψ+, top: 7.00e8 against
  9.72e8).  **Single literal runs above the MEAN-RUN bound at some rung: 1 130 of 1 800, by up to ×1.50; in the case
  ψ−, u = 2, top the MEAN of the literal calls of I_1 (3.1585e8) is above the mean-run bound (2.5128e8).**  So the
  number of §4 bounds mean runs; for literal runs the inequality holds with the realised sample sizes.
* same — `r18_cells.py` (`logs/cells.log`): all 468 cells: lo ≥ b (smallest lo − b = 10.18 at u = ½, n = 250, φ = 0.85,
  n_i = 38), x0 − hi ≥ b (7.82, same cell), x_L = b, x_1 ≤ min(lo, x0 − hi) (smallest margin 5.03 at u = 2, n = 250,
  φ = 0.85); exact shifts at lo, mid, hi equal b / 0 in 1 404 of 1 404.  Consequence of the last inequality: in EVERY
  X-005 cell the windows of the rungs l ≥ 1 do not depend on the place; the union of §4 changes the calls of I_1 only.
* same — `r18_rule.py` re-run with block E (`logs/rule_seed18_n100000_v2.log`, blocks A–D identical to the first log): the rule
  and the window also hold (0 violations in 2.0 M decisions each) when intermediate rungs are wider than x_l and when
  positions have either sign (invalid brackets; then c leaves [0, b] in 82 294 of 100 000 points); an algorithm that
  does not intersect violates the rule written with raw positions in 11 865 of 2 029 533 decisions (control).
* same — `r18_corner.py part1` first pass (5 literal runs per case): (A) their kind of test input (flat law, ψ0 = 0,
  place given independently, "top", t0 < b): ln cost exact − old convention = +4.1744 at all three sizes and both λ —
  the "e^{4.2}" of the message; my two runs equal their reference's two runs in every case.  Note: such a triple is
  not an instance (a flat ψ has ψ(a,0) = ψ0, so ln W = t0 − u n_i − ψ0).  (B) on consistent flat instances where the
  two mean runs differ, the literal run has every level's sample size as the exact rule's mean run (never the old
  convention's).  **Own error E3:** in the first version of part 1 the mean run was fed `Fr(float(kap))` while the
  literal engine saw the same number as a float that reproduces an exact tie (L = s e^{-b}); the "exact" mean run
  then stopped one level later than the literal runs.  Cause computed: float(2.9) is 8.9e-17 below 2.9, which
  turns the tie W = s e^{-c} into W > s e^{-c}.  Corrected by building the mean run's inputs from the same rationals
  as the instance (`kapq = u n_i − t0`), before any number of that first version was used.

* 2026-11-26T16:55:28Z — RE-RUN COMPARED after sequence A (`r18_compare_rerun.py`, `logs/compare_rerun_after_A.log`):
  recheck_classification: 1 408 of the table's 2 624 searches re-run (cost n ≤ 4000: 1 152; claims n = 1000: 240;
  converge n = 1000: 16): in a corner 0; changed by the exact rule 0; claims violated 0; old convention reproduces
  the stored value in 1 407 of 1 408.  292 cells against their stored per-cell values: |stored_worst − theirs| = 0,
  |exact_worst − theirs| ≤ 4.3e-14.  The one not reproduced: u = 0.5, n = 1400, φ = 0.3, general/top, c_in = 0.0
  (flat fibre): +1.539e-05 with the tie rule, **0 with tie = 0** (`logs/diag_cost_n1400.log`) — a tie-rule change as
  the message says, not the cell's worst search.  So 1 of their 9 is at n ≤ 4000 and 8 are at sizes I could not
  re-run.
  nonproduct_bound: 288 of 468 cells re-run (n ≤ 4000): worst_product, worst_bound within 4.3e-14 of their stored
  values, max_gap within 2.8e-14, bounds above C_max 0 = theirs.  Table rows u = 0.5 and u = 1 reproduced in full
  (their maxima are at n = 250, 350); row u = 2: "2.3e-13; 1.7e-16" reproduced (n = 4000, φ = 0.75), "0.026 (n a)"
  reproduced (n = 350, φ = 0.85), "13 (ln)" is at n = 8000, φ = 0.85 — NOT re-run (their reference needs more than 2 GB there).
  **Stored file against script default (candidate finding):** the four result files hold 2 672 searches; the stored
  `x005_recheck_classification.json` has the jobs cost, claims, converge only (2 624); the script's default job list
  includes converge2 (48 searches), so the command of "Evidence and reproduction" gives 2 672 at 1cc4e1c, not the
  table's 2 624 — unless `--jobs cost claims converge` is passed.

* 2026-11-26T17:00:07Z — CORNER, part 1 full (`logs/corner_part1_seed18_30.log`, 211.7 s, 71 MB; their code under ulimit): 54 cases
  = 3 sizes × λ ∈ {½, 1/5} × {top t0 = ⅛, top t0 = ¼, bottom t0 = x0 − ¼}.
  (A) their kind of input: largest |ln cost(exact) − ln cost(old convention)| = 4.174 ("e^{4.2}" confirmed, by my
  code and by their reference; the two agree in all 18 (A) rows).
  (B) 36 consistent instances (flat; outer cone u/2), 30 literal r6lib runs each: on 26 the two mean runs differ;
  where they stop at different levels (25 instances, 750 literal runs) the literal run stops at the exact rule's
  level in 750 and at the old convention's in 0; where the mean-run costs differ by more than 0.05 (13 instances)
  the mean literal ln(queries) is closer to the exact rule's in 13.  (Every level's sample size equal to the exact
  rule's mean run: 360 of 780 — the flat ones; on cones individual levels fluctuate.)
* same — CORNER, part 2 (`logs/corner_part2b_seed18_300.log`, 17 s; THEIR reference): 300 designs with lo < b or x0 − hi < b
  (n_i ∈ 2..8, b ∈ {½,…,3}), radial laws, product instances of their family at 9 feasible places each (c_in = t0 − u n_i).
  The shift depends on the place in 482 of 600 (design, law, behaviour) cases.  **A product instance costs MORE than
  the pair mode (`t0_range = (lo, hi)`) returns for its own law in 16 cases (39 of 5 400 runs): bottom 7 (largest
  ln excess 0.693), top 9 (largest 6.834).**  Worst: u = 1, n = 44 (n_o = 42, n_i = 2), λ = 0.2, η = ¼, η′ = 0.1, θ = 2,
  ν1 = 1, b = 2.5, ladder (4, 2.875, 2.5), cone of slope u to radius 35 then flat, reference at d0 with F = 2, "top",
  every fibre at t0 = lo = 1.2402: ln cost 16.5121 (shift 1.2598) against 9.6776 from the pair mode (shift 0):
  the "upper bound" is below the instance by a factor e^{6.83}.  My code reproduces both numbers to 6 decimals
  (16.512084, 9.677630); the union of windows with the fibres' own shift gives 16.513467 ≥ the instance, as it must.
  Example stored in `data_corner_example_their_reference.json`.
  A first version of part 2 varied the place with the law held fixed (not a product instance of their family: the
  reference fibre's place is tied to ψ0); its log and example are in `not_cited/` (…SUPERSEDED…).  A run of
  `r18_nonproduct.py corner 150 5` was stopped by its 110 s timeout: log in `not_cited/`; restarted with 40 designs.

* 2026-11-26T17:08:15Z — sequence B finished 17:05:42Z (three chunks n = 8000, u = 0.5, all exit=0; peak 1 265 MB, longest 276.5 s).
  FINAL RE-RUN COMPARISON (`logs/compare_rerun_final.log`): recheck_classification 1 536 of 2 624 searches (cost 1 200,
  claims 320, converge 16): in a corner 0, changed 0, violated 0, reproduced 1 535 (the one exception as above);
  304 cells against their stored per-cell values: 0 and ≤ 4.3e-14.  nonproduct_bound: 300 of 468 cells (n ≤ 4000 all
  slopes; n = 8000 for u = 0.5): ≤ 4.3e-14 on worst_product and worst_bound, ≤ 2.8e-14 on max_gap, same counts of
  bounds above C_max (0).  Not re-run: n = 8000 (u = 1, 2), n ≥ 16 000 — 1 088 searches of the first table, 168 cells
  of the second, among them the cell of the entry "13" (n = 8000, u = 2, φ = 0.85).
* same — **A CELL OF THEIRS (`r18_cell.py 2 250 0.85`; first pass)**: the cell with the largest excess of their table
  `anyplacement` (+0.02005 n a).  Their files: worst product instance found (M-008) ln cost 125.373236; bound
  searched (M-014) 127.016745, monotone/top, reference shell d0 = 189, c_in = −4.294.
  (1) my mean run at that law: bound = 127.016745, their stored value to 2.8e-14 (first comparison of my evaluator
  with a published number at a published size); product instance at that law 116.223.
  (2) the dearest place per shell: every shell at lo = 54.484 (the reference shell at its own place 71.706): cost =
  the bound exactly.
  (3) an ACTUAL ψ (cone fibres, σ following (2) under the Lipschitz constraint, every edge checked, ln W recomputed
  from ψ to 2.8e-14, ψ0 unchanged): mean-run cost 127.016745 = the bound; calls of I_1: 1.809e50 against 1.373e41
  for the product instance with its law.
  (4) a PRODUCT instance: every fibre at lo (c_in = −21.5163), the maximiser's profile with a ramp of slope u
  below the reference shell (shells 176..212 changed, ln of their probability −52.8; u-Lipschitz, monotone): cost
  127.016745, **by my code and by their reference (violations of the theorem's claims: none)**.
  So in this cell: the "excess" is the cost of an instance — and of a product instance: the product search of job
  M-008 stopped 1.6435 in ln cost (0.02005 n a, a factor 5.2) below a product instance that exists.  The profile
  of (4) has 19 runs of constant slope; their family (8 knots) gives at most 17, so as built it is outside their
  search family, inside the class of product instances.  The table `anyplacement` therefore measures, here, the
  shortfall of the product search, not a difference between products and non-products.  Candidate MAJOR finding.
  Other cells with excess > 0.001 n a (5): running now (`r18_cell_sequence.sh`).  Also: 18 of 360 cells have the
  bound-search BELOW the product search by more than 1e-4 n a (down to −0.0054): the two searches differ by ±0.005 n a
  at the small sizes in both directions.
  PLAN `r18_mixed.py --costs theirs` (may exceed five minutes in total; each case capped at 240 s of search): 3 cases at
  n = 100–250; per mean run 0.1–0.5 s; compared with: max of the two uniform placement-free bounds of the same law.

* 2026-11-26T17:15:26Z — **THE SIX CELLS** (`r18_cell.py`, second version: `logs/cell_v2_*.log`, each a few seconds, 89 MB, their code
  under ulimit; the first version's logs `logs/cell_u*.log` reached their last lines too and differ only in step (4),
  which there kept the reference shell; its data files are in `not_cited/`).  In every one of the six cells where their
  searched bound exceeds their searched product worst case by more than 0.001 n a, **a PRODUCT instance has a
  mean-run cost equal to the searched bound, by THEIR reference evaluator, with no claim of the theorem violated**:
    (u, n, φ)        worst product found   bound searched   product instance
    (2, 250, 0.85)   125.373236            127.016745       127.016745: every fibre at lo, the M-014 law, reference point in
                                                            shell d1 = 212 (one shell changed, probability 2^-212), monotone
    (2, 350, 0.85)   161.175052            161.951637       161.951637: same construction, d1 = 297 (54 shells, e^-69.1)
    (0.5, 250, 0.50)  37.751829             37.797269        37.797269: the stored M-014 maximiser ITSELF, decoded by their
    (0.5, 350, 0.50)  40.706118             40.735971        40.735971   `Family.decode` as a product instance of their own
    (0.5, 350, 0.55)  40.083311             40.099500        40.099500   8-knot monotone family
    (0.5, 500, 0.35)  46.909303             46.929972        46.929972
  My evaluator gives the same six numbers to the 6 decimals printed, and reproduces their stored bound in each cell
  (differences 0 to 2.8e-14).  In the first cell an ACTUAL ψ that is not a product (cone fibres, σ(d) varying, every
  edge ≤ u(1 − 1e-9) where the slope changes) also costs 127.016745.
  Reading: (i) "by an amount that is a bound and not the cost of an instance" is false in all six cells; (ii) "no
  such instance costs more than the worst product instance found" is false as worded (even product instances do);
  (iii) the column measures the shortfall of the product search M-008 (up to 1.6435 in ln = 0.02005 n a), not a
  difference between products and the rest: with the stored M-008 values at n = 250, 350, 500 reproduced by the
  present code (my re-run: 144/144 each), this is not the tie rule.  (iv) The mechanism in the u = 2 cells: the bound
  search frees the reference value from the place of the fibres; a product instance does the same with a ramp of
  slope u to a reference point in a shell of negligible probability.
* same — MIXED BEHAVIOUR (`r18_mixed.py --costs theirs`, `logs/mixed_theirs_a.log`, 264 s): X-005 design with their inner costs;
  the same law, behaviour "bottom" on some shells and "top" on others.  n = 100, u = 1, φ = 0.5, flat law: uniform
  bottom 44.483875 (= its placement-free bound), uniform top 36.906359; best shell-dependent behaviour found
  45.044595 ("top" on 7 of 51 shells; largest sample K·2^10 instead of K·2^9): **+0.5607 above the larger of the two
  bounds**.  Dip law: +0.0001; n = 150, u = 2: 0 (within 1e-6; the log's word "EXCEEDED" there is a printing
  threshold of 1e-9, corrected in the script for the next run `mixed_theirs_b.log`).
  PLAN `r18_cell0.py` (possibly above five minutes in all): every stored M-014 maximiser as a product instance, their
  reference; n ≤ 2000 in one run (about 1 000 mean runs of their reference at 0.02–1 s each: 3–4 min), n = 4000 in a
  second (144 runs at 0.5–4 s: about 5 min, below 1.7 GB); compared with the stored worst product value of each cell.

* 2026-11-26T17:29:39Z — LATER RESULTS (all logs complete):
  - `r18_cell0.py` (their decoder + their reference on every stored M-014 maximiser as a product instance):
    `logs/cell0_n250_to_2000.log` (200.3 s, 602 MB), `logs/cell0_n4000.log` (287.1 s, 1 659 MB),
    `logs/cell0_n8000_u0.5.log` (102.8 s, 1 195 MB): 300 cells; a product instance above M-008's "worst found" in 33
    cells (13 by > 1e-4 n a, 4 by > 1e-3 n a, largest +0.00600 n a); violations 0.  The table has 15 cells with the
    bound above the product search by > 1e-4 n a (their files, all 360 cells); all 15 are among the 300; 13 explained
    to 1e-6 n a by the stored maximiser as a product instance, 2 (u = 2, φ = 0.85, n = 250, 350) by the ramp.
  - `r18_mixed.py --costs theirs`, second run (`logs/mixed_theirs_b.log`, 98.9 s): excess over the larger uniform
    bound +0.5607 (u = 1, flat), +0.4702 (u = ½, flat), +0.000011 (u = 1, cone), 0 (u = 2 flat; plateau).
  - `r18_rule.py` v3 (`logs/rule_seed18_n100000_v3.log`, 78.7 s): control "levels in decreasing order": 30 017 of
    2 016 504 decisions wrong; other blocks as v2.
  - data of the product instances: `data_cell_u2_n250_phi0.85.json`, `data_cell_u2_n350_phi0.85.json` (profile F with
    increments in [0, u], max increment − u = 0; reference shell d1; ψ0 = F[d1] = 0).
  - REPORT written: `docs/science/workstreams/R18_REPORT.md` (sections 0–7).  One correction while writing: the
    memory of their reference is "about (n_o+1)(j_stop+1)·8 B" (one array per distinct window length; at u = 2,
    n = 16 000 the same planning run needed less than that formula gives, so it is an estimate, not a law).

* 2026-11-26T17:35:30Z — TIES AT PUBLISHED SIZES (`r18_ties_large.py 1000 2000 4000`, `logs/ties_large_n1000_2000_4000.log`, 87.5 s,
  357 MB): X-005 design, u = 1, flat fibres (c_in = 0), profiles on the level grid (flat; cone to 0.3 n_o / 0.4 n_o then
  flat): every atom lies exactly on a level, so "top" has U = s at every rung and W = s at the threshold.  My exact
  mean run against their reference: 18 runs, 220 463 levels, 0 mismatches (levels, sample sizes, calls of every
  rung, cost).  So their tie tolerances are sufficient up to n = 4000.  (The column "atoms with the rung-0 window
  ending exactly on a level ≤ j_stop" of that log is 0 everywhere — that end lies above the stopping level; the
  ties exercised are the ones just named.)
  PLAN `r18_flat_large.py 8000` then `… 16000` restricted to φ = 0.5 (more than five minutes in all): my exact
  evaluator on the flat instance (one atom) against the flat-instance costs STORED in x005_cost.jsonl (their
  kernel, job M-008).  Measured at n = 8000: 9–16 s per run for u = ½, 54 s for u = 1 (a first foreground try was
  cut by its 110 s timeout after three rows, all three with difference 0 — no log kept); expected 150 s for u = 2;
  6 runs ≈ 7 min at n = 8000.  Compared with: stored ln cost, stopping level, ln M_max.  A difference would not
  by itself be an error (the stored values predate the tie rule); agreement is a replication of the kernel at a
  size their Python reference cannot reach within 2 GB.

* 2026-11-26T17:55:45Z — `r18_flat_large.py 8000` was STOPPED by its own time limit (1150 s) during the sixth row (u = 2, top); its log is
  `not_cited/flat_large_n8000_STOPPED_by_time_limit_1150s_after_5_rows.log`.  The five rows it printed all agree
  with the stored flat-instance values (difference 0, 0, 0, −1.1e-13, 0; the fifth, u = 2 bottom, took 600 s — my
  estimate of 150 s for u = 2 was wrong by a factor 4: the pass loop at u = 2 goes to K·2^m with m in the thousands).
  Restarted with `--umax 1` (four rows, about 200 s expected from the measured 10 + 19 + 55 + 111 s) to have a log
  that reaches its last line: `logs/flat_large_n8000_umax1.log`.  The u = 2 rows are not cited.
* same — read-through of the report against the logs: corrected (i) "lo − b ≥ 10.18" → 10.17 (the value is 10.1753) and "at
  least 10.2" → 10.1; (ii) §3.4: the explicit ψ makes more calls than the product instance in 7 cases (not 6) and
  attains the bound in 2 (within 0.2 % in a third), not "to four digits in 3" — the same slip is in the notes entry
  of 16:40Z above; (iii) "a shell nobody samples" → "of negligible probability" (the changed shells are sampled, e.g.
  e^{82} points at (2, 350, 0.85); they carry a negligible share); (iv) corner part 1 (A): the difference 4.1744 is in
  the 12 "top" rows, 0 in the 6 "bottom" rows.

* 2026-11-26T17:59:16Z — `logs/flat_large_n8000_umax1.log` complete (124.4 s, 98 MB): my exact mean run on the flat instance against the
  flat-instance costs stored in x005_cost.jsonl (their kernel) at n = 8000, φ = 0.5, u = ½ and 1, both behaviours:
  4 of 4 agree (stopping level, largest sample, ln cost; largest difference 1.1e-13); constants J, K, r†, m_max
  equal in mine, theirs and the stored record.
* same — FINAL CHECKS: 15 copied files identical by sha256 to <ENG>; their `ckernel.py` kept unchanged as `….py.txt`; adapter
  in `rerun_copy` identical to `r18_ckernel_adapter.py` (71 lines); 29 of 29 chunk logs end with exit=0; no `.c`,
  no `.so`, no `build/` anywhere under `rerun_copy/`.  `git status --short` (read-only) shows of mine only
  `docs/science/workstreams/R18_REPORT.md` and `experiments/science/ws_R18/`.
  State at hand-back: report complete (sections 0–7).  **Tool actions declined: none.**  (One foreground command
  was moved to the background by the tool after 120 s — not a refusal; three runs were ended by time limits I had
  set myself: logs in `not_cited/`.)
