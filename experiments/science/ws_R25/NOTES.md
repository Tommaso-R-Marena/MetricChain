# R25 — working notes (second look at Theorem 1c, regime |x| >= |sigma|, and Lemma A1)

Internal review by an AI agent; not external peer review.
Every time below is read from the clock with `date -u` at the moment of writing.

## 2026-11-26T21:02:47Z — start

* Read `docs/science/workstreams/COMMON.md` (115 lines) and `docs/science/workstreams/R25_brief.md` (92 lines).
* Created `experiments/science/ws_R25/`.
* Object: `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/cx_ro_89114ea/STRANDS_NN_HARDNESS.md`
  (their commit `89114ea`, read-only copy).  Next: read §0, §1, §2, §3 to end of proof of Thm 1c, App. A (Lemma A1).
* Rules I hold myself to: write only here and in `docs/science/workstreams/R25_REPORT.md`; no state-changing git;
  no subagents; `OMP_NUM_THREADS=1`, at most 2 processes, < 2 GB, < 10 min per run, peak memory in last line of
  every script, `python3 -B`; fresh log names; a log is cited only if its run reached its last line.

## 2026-11-26T21:12:20Z — the note has been read (review, by hand; no code yet)

Object: 720 lines, sha256 `3df75bc9f4b11b5a98579b33924ec127bd0e7f3c26fefc25da6410b95e115fc7`.
Read in full: l.1–446 (§0–§3 incl. Thm 1d/1e text, which I do not review), l.647–721 (App. A).  Skimmed l.447–646
(§4–§9) only to see how the two places are used (Cor. 5 uses `|T| ≤ 21m`; §6 describes their tests).

### Item 1 (Theorem 1c, regime |x| >= |sigma|), first pass by hand — all steps re-derived

Notation of the note: template `G^B A G^B … G^B` (m blocks), items `C^{a_i}`, `Σa_i = mB`, `M = mB − n`,
chords nested `(t_1,c_1)…(t_K,c_K)`, faces `F_0…F_K`; `F_0`, `F_K` hold the two template-end nicks.
`d = |x| − |σ|`.

1. Counting identities l.320–322: template GG bonds number `m(B−1) = M + n − m`; each lies on exactly one face;
   stack and flush faces carry exactly one each ⇒ `st + fl + L = M + n − m`.  The `n−1` inter-item nicks lie on
   inner faces only (F_0/F_K already hold a nick; connected ⇒ ≤ 1 nick per face) ⇒ `fl = n − 1 − z`.  OK.
2. Eq. (2): `E − E_0 = σ st + x fl + P − σM − x(n−m)` with `st = M − (m−1) − L + z`, `fl = n−1−z` gives
   `(x−σ)(m−1−z) + |σ|L + P`, and `x − σ = −d`.  OK — and this is pure algebra, valid for either sign of `d`.
3. Separator count l.328–341: for an inner face `f ∈ 𝔉` with `k_f` separators: `k_f − 1` whole blocks unpaired,
   `(k_f−1)(B−1) ≥ k_f − 1` loose bonds [B ≥ 2 used, first time], plus 1 for "bulge/interior (r)" or
   "non-flush inter-item nick (z)".  For `F_0`/`F_K ∈ 𝔉`: `k_f` whole blocks, `k_f(B−1) ≥ k_f` loose bonds
   [B ≥ 2 again].  Different faces ⇒ different bonds/nicks ⇒ `m − 1 ≤ L + r + z`.  OK.
4. Conclusion l.343–351: with `P ≥ γ r + P''`: `E − E_0 ≥ (|σ|−d)L + (γ−d) r + P''`; each coefficient > 0 because
   `d < min(|σ|,γ)` [the hypothesis `|x| < |σ| + min(|σ|,γ)` used here, with the right sign]; `≥ min(|σ|,γ) − d`
   as soon as `L ≥ 1` or a bulge/interior loop exists.  OK.
5. Last step l.352–356: `L = 0` and no bulge/interior ⇒ all template GG bonds have both ends paired ⇒ (B ≥ 2,
   third use: every G is an end of a GG bond) all G paired ⇒ (`Σ a_i = mB`, implicit) all C paired ⇒ the face
   of an item bond has that bond as item side, no nick ⇒ stack (no bulge allowed) ⇒ step (d) ⇒ tiling.  OK.

No error found by hand.  Observations to be tested by enumeration:

* **O1 (B ≥ 2 is redundant in the statement).**  If `B = 1` then `Σ a_i = m` with `a_i ≥ 1` forces `n = m`, all
  `a_i = 1`, `M = 0`, `n − m = 0`; every connected structure pairs each one-base item with its own `G`: it is a
  tiling structure and has no stack and no flush face, energy `nΔG_assoc = E*_x` for every `x`.  So for `B = 1`
  the conclusion holds vacuously for every `x`; the brief's "control B = 1" cannot produce a violation.
* **O2 (the hypothesis is sharp only at B = 2).**  The count of step 3 gives more: with `h` = number of
  separators "absorbed" by wholly unpaired blocks, `m − 1 − z ≤ h + r` and `L ≥ h(B−1)`, hence
  `E − E_0 ≥ |σ|(L − h(B−1)) + h((B−1)|σ| − d) + r(γ − d) + P''`.  Conjecture to test: for `B ≥ 2` the exact
  condition is `|x| < min(B|σ|, |σ| + γ)` and the exact gap `min(|σ|, |σ| + γ − |x|, B|σ| − |x|)` (all `x ≤ 0`).
  For `B = 2` this is the note's `ε_x` in the regime `|x| ≥ |σ|`.
* **O3 (candidates for smallest counterexamples beyond the range)**, by hand: `a = (3,1), m = 2, B = 2`
  (a no-instance): straddle structure `E − E_0 = γ − d`; block-1-unpaired structure `E − E_0 = 2|σ| − |x|`.
  Also `a = (4), m = 2, B = 2` (n < m).  Yes-instances: `(2,1,1), 2, 2` (straddle), `(2,2), 2, 2` (unpaired block).
* **O4** the stated `ε_x` jumps at `|x| = |σ|` from `0+` to `min(|σ|,γ)`: both bounds are valid, the case-1 gap
  is not sharp for `γ > 0`, `B ≥ 2` (conjecture: `min(|σ|, |σ| − |x| + γ)`).

Implicit hypotheses (Item 1) collected: `a_i ≥ 1`, `Σ a_i = mB` (used in "then all mB item bases are paired");
flush faces exist only on inner faces, between two *items*, on a template GG bond inside a block — never at a
separator (the `A` is unpaired), never on `F_0`/`F_K` (template ends, one chord); every other exterior loop,
including helix–A–helix across a separator and exterior loops with dangling bases, has energy exactly 0; `x`
and `σ` are constants (same for every flush face / GG-CC stack); `γ` bounds *every* bulge and interior loop
(also the one-nucleotide `A` bulge over a separator); energies are sums over faces only.

### Item 2 (Lemma A1), first pass by hand — both directions re-derived

* Sizes: `|W| = 2L`; `|X| = |Y| = L + m + Σ_C(ℓ_C − 1) = 2L` **only if every clause has ℓ_C ≥ 1** (an empty
  clause would give "−1 garbage pairs"; with 0 pairs `|X| = 2L + #empty > |W|`, and `c¹_C` lies in no triple,
  which also violates the hypothesis of Lemma A2 "every element lying in at least one triple").  Candidate
  minor finding.
* `|T| = 2L + L + Σ_C 2ℓ_C(ℓ_C−1)`; per clause 3, 10, 21 for ℓ_C = 1, 2, 3.  OK, `≤ 21m`.  No duplicate triples.
* (⇒) `b_{v,j}` lies only in `T_j, F_j`; `a_{v,j}` only in `T_j, F_{j−1}`; propagation round the cycle gives all
  true or all false; `d_v = 1` degenerates correctly (`T_1`, `F_1` share `a`, `b`).  `c¹_C` lies only in the ℓ_C
  clause triples, the tip of the chosen one is not covered by a variable triple ⇒ literal true.  Garbage
  triples play no role in this direction.  OK.
* (⇐) after the variable triples every slot has exactly one free tip; clause C: ℓ_C free tips, one to the
  clause triple (a true slot), ℓ_C − 1 to its ℓ_C − 1 garbage pairs (each garbage pair is joined to all 2ℓ_C
  tips of the clause).  Every element exactly once.  OK.
* Why linear: tips exist per *occurrence* (slot), not per (variable, clause) pair; so the free tips of a clause
  are exactly ℓ_C, and garbage is collected clause by clause with ℓ_C − 1 pairs.  (Garey–Johnson's gadget, from
  my memory and unverified: every variable has 2m tips, `m(n−1)` global garbage pairs joined to all `2mn`
  tips, `Θ(m²n²)` triples.)
* Stronger identity to test by code: `#perfect matchings = Σ_{α satisfying, over occurring variables}
  Π_C (number of true slots of C under α)·(ℓ_C − 1)!`.
* Special cases by hand: repeated literal in a clause (slots are occurrences: fine), `x ∨ ¬x` in one clause
  (fine), unit clauses (no garbage, clause triple forced), variable occurring once (`d_v = 1`, fine), only
  positively (fine), variables not occurring (no elements), empty clause (see above), `m = 0` (empty instance).

### Plan for the code (own code, from the statements)
* `nn_model.py`: circle, generic crossing predicate, faces as orbits of links, loop types from §1, energy
  signature, tiling by the definition of §2.  Enumerators: L0 (all partial matchings, all labelled orders, tiny),
  LA (backtracking over non-crossing pair sets, generic faces), LB (transfer-matrix DP over nested chords).
* `a1_3dm.py`: construction of Lemma A1, exact cover counting, brute-force SAT, controls (triple removed/added).

## 2026-11-26T21:17:39Z — code written; first runs; **my observation O1 was wrong** (own error no. 1)

* Wrote `nn_model.py` (model, enumerators L0/LA/LB) and `t1c_levelA.py` (part1: L0 vs LA; part2: LA on all
  compositions of mB, structural checks of the proof, LA vs LB).
* Trial runs (scratch logs `logs_tmp_part1.txt`, `logs_tmp_part2_q6.txt`, output `tmp_trial_q6.json`; these are
  trials, NOT cited as evidence; the cited runs get fresh names below).
* part1 trial: 29 tiny labelled instances, 126 621 pair sets, 84 924 connected, 16 654 connected and
  unpseudoknotted; uniqueness of the ordering: 0 violations; LA ≠ L0: 0; mutant enumerator detected on 29/29.
* part2 trial (mB ≤ 6) showed `B1_nontiling_structures: 8922`.  **So O1 above is false**: for `B = 1`,
  `Σ a_i = m` does NOT force `a_i = 1` — I confused `n ≤ m` with `n = m`.  Items longer than one base exist
  (`a = (2), m = 2, B = 1`), they are no-instances, and they have non-tiling structures.  By hand:
  template `GAG`, item `CC`: the structure with ONE pair has energy 0, while `E_0 = σM + x(n−m) = σ − x = d ≥ 0`
  for `|x| ≥ |σ|`.  So at `B = 1`, `x = σ`: a non-tiling structure of a no-instance has energy exactly `E*_x`
  (and MFE = E*_x): **the hypothesis B ≥ 2 is necessary**, and the brief's control B = 1 can fail, as the
  coordinator expected.  (The numerics came before the theory here, as COMMON.md rule 3 asks; the error was
  caught by the enumeration about five minutes after it was written into these notes — 21:12 → 21:17 by the
  clock — before any report text.  An earlier wording of this line said "20 minutes": that was a guess, not a
  clock reading, and is corrected here.)
* Consequence for O2: the conjectured unified condition `|x| < min(B|σ|, |σ| + γ)` gives `|x| < |σ|` at `B = 1`,
  i.e. exactly the note's exclusion.  To be tested for all B ≥ 1.
* Fixes to `t1c_levelA.py`: dropped-term controls are now tallied only for B ≥ 2 (at B = 1 the full
  inequality fails anyway); all tally keys are initialised so that zeros are printed.

## 2026-11-26T21:32:30Z — cited runs 01–03 (Item 1, enumeration) and 10–11 (Item 2); all reached their last line

All logs start with a `start <UTC>` line written by `date -u` and end with the script's `peak memory` line.

* `run01_part1.log` (4.4 s, 34.0 MB): L0 (every partial G–C matching × every labelled order, pairwise crossing
  test, union-find) against LA (backtracking) on 29 tiny labelled instances: 126 621 pair sets, 84 924 connected,
  16 654 connected and unpseudoknotted.  Violations: uniqueness of the ordering 0; LA ≠ L0 0.
  Control (mutant enumerator that never pairs the last base): detected on 29/29.
* `run02_levelA_q8.log` (176.0 s, 16.7 MB) → `sig_levelA_q8.json`: LA on all 837 compositions of the 20 families
  with mB ≤ 8: 7 156 938 non-crossing pair sets, 1 309 291 connected structures (957 901 with B ≥ 2), 370 tilings.
  Violations: Fact 1: 0; bond count `st+fl+L = m(B−1)`: 0; nick count `fl = n−1−z`: 0;
  separator inequality `m−1 ≤ L+r+z` for B ≥ 2: 0 (**for B = 1: 351 135 violations of 351 382 non-tiling
  structures** — so the inequality really needs B ≥ 2); tiling ⇔ all item bonds stacked: 0; tiling ⇔ (L = 0 and no
  bulge/interior) for B ≥ 2: 0; tiling signature `(M, n−m, 0, 0, m−1, 0)`: 0; DP LB ≠ LA: 0 of 837.
  Controls (B ≥ 2): inequality without r fails 7 196 times, without L 111 848, without z 14 988; mutant DP
  (flush test ignoring the template side) detected on 810/837 compositions.
* `run03_levelA_3x3.log` (314.0 s, 16.5 MB) → `sig_levelA_3x3.json`: the same for the family (3,3): 256
  compositions, 12 446 720 non-crossing pair sets, 1 883 167 connected structures, 64 tilings; all violations 0;
  controls: 960 / 85 170 / 1 344; mutant DP detected on 255/256.
* `run10_a1_special.log` (13.8 MB): 15 special formulas (unit, repeated literal, tautological clause, variable
  once, only positive/negative, duplicate clauses, three unsatisfiable ones): 0 violations; exact-cover counter
  vs naive subset enumeration: 0 disagreements on 112 instances (control: a naive count ignoring W differs on 14);
  empty clause `[(1,2),()]`: |W| = 4, |X| = |Y| = 5, c¹/c² of the empty clause in no triple.
* `run11_a1_exh_nv3_m3.log` (241.7 s, 15.9 MB): **all 102 339 formulas on 3 variables with ≤ 3 clauses**
  (clauses = non-empty multisets of ≤ 3 literals; 99 477 satisfiable, 2 862 unsatisfiable; largest instance
  q = 18, |T| = 63): sizes 0 violations; satisfiable-but-no-matching 0; unsatisfiable-but-matching 0; counting
  identity 0 (9 280 618 matchings counted); recipe of the proof 0 of 344 430 (every satisfying assignment);
  decoding 0 of 3 731 374 matchings (cap 50 per formula).
  Controls: drop true triple → 22 172 disagreements; drop false → 22 172; drop clause → 21 093; drop
  garbage (p tip) → 926; drop garbage (n tip) → 2 226; wrong clause triple added → 2 477 (unsat but matching);
  unlinked variable gadget → 2 862 (every unsatisfiable formula gets a matching); identity without (ℓ−1)! fails
  on 95 814 formulas.
* Trial analysis (scratch log `logs_tmp_analysis_trial.txt`, on trial data, not cited) agreed with the hand
  derivations of O2–O4; the cited analysis run comes after the DP runs.

## 2026-11-26T21:47:01Z — **own error no. 2: a trial run of mine exceeded the memory limit and was killed by the system**

* Runs 04, 05, 06 (DP) and 12, 13 (Lemma A1) completed and reached their last lines — details in the next entry.
* Then I started a TRIAL of the random larger-formula mode: `timeout 300 python3 -B a1_3dm.py rand 7 150`
  (scratch log `logs_tmp_a1_rand.txt`).  It was **killed by the kernel's memory-cgroup OOM killer** after
  1 min 56 s wall time; `dmesg` shows `Memory cgroup out of memory: Killed process 28803 (python3)
  total-vm:13593528kB, anon-rss:12050272kB`.  So one process of mine reached about **12 GB resident**, six
  times the 2 GB limit of the brief.  The kill was confined to my own cgroup (`CONSTRAINT_MEMCG`); the other
  job visible on the machine (`held_pair_exact.py`, pid 26657) was still running afterwards; my background run 06
  had already finished (its log has its last line, 246.3 s, 283.0 MB).
* Cause: the control "unlinked variable gadget" turns every slot into an independent binary choice, and my
  memoised exact-cover counter then has exponentially many distinct covered-sets (2^L, L up to 63 slots in that
  mode).  On the small exhaustive families (L ≤ 9) this is harmless; on larger formulas it is not.  I had not
  thought about the state space of the mutated instances before launching.
* Nothing is cited from that run (it produced no result line).
* Fixes (before any further run): (1) every script now sets a hard address-space limit of 2 GB on itself
  (`resource.setrlimit(RLIMIT_AS)`), so an over-allocation raises MemoryError instead of growing; (2) the
  counter aborts with an exception if its memo exceeds 2 000 000 states; (3) the random mode runs the controls
  without "unlinked" (that control is already exercised on 176 033 formulas in runs 11–13).
* Because the scripts change (only by these guards), **all cited runs will be repeated with the final scripts
  under fresh names (run2x/run3x)**, with the sha256 of each script recorded before the runs; the logs run01–run13
  stay in the directory as the first pass and are not overwritten.

## 2026-11-26T21:53:53Z — first-pass results of runs 04–06, 12–13; scripts frozen; second pass starts

First pass (scripts before the memory guards; logs kept, all reached their last line):
* `run04_dp_q9to12.log` (50.7 s, 115.9 MB) → `sig_dp_q9to12.json`: DP on the 14 families with 9 ≤ mB ≤ 12
  (16 896 compositions; 3 221 566 998 connected structures counted by signature, 2 627 562 093 with B ≥ 2):
  bond count 0, nick count 0, separator inequality for B ≥ 2: 0 violations (B = 1: 594 001 065), tiling
  signature 0, tiling ⇔ (L = 0, no bulge) 0.  Controls (B ≥ 2): without r 8 641 884; without L 273 170 612;
  without z 31 292 644.
* `run05_dp_2x7_7x2_3x5.log` (380.2 s, 485.8 MB) → `sig_dp_q14_15a.json`: families (2,7), (7,2), (3,5): 32 768
  compositions, 180 727 681 598 structures; all violations 0; controls 288 389 936 / 11 126 205 782 / 1 332 505 448.
* `run06_dp_5x3.log` (246.3 s, 283.0 MB) → `sig_dp_5x3.json`: family (5,3): 16 384 compositions,
  138 317 675 654 structures; all violations 0; controls 5 231 360 / 6 734 068 545 / 15 511 040.
* `run12_a1_exh_nv4_m2.log` (17.7 s, 14.4 MB): all 13 694 formulas on 4 variables with ≤ 2 clauses (36
  unsatisfiable): all violations 0; every control produces disagreements (24 … 1 512).
* `run13_a1_sample_nv4_m3.log` (184.2 s, 23.5 MB): 60 000 random 3-clause formulas on 4 variables, seed
  20261126 (653 unsatisfiable): all violations 0; every control produces disagreements (226 … 7 448).

Changes to the scripts since those runs (no change to the model code, the enumerators or the checks):
`limit_memory` (RLIMIT_AS 2 GB) in every script; `a1_3dm.py`: `make_counter`/`MEMO_CAP`, explicit matchings
enumerated with pruning by the counter, `CONTROLS_LARGE` for the random mode; `t1c_analysis.py`: labelled
counts, boundary points, control C2c, case-1 check C2d.

sha256 of the frozen scripts (taken at 2026-11-26T21:54:23Z, after one more addition to `t1c_analysis.py` — the tables C9 — and before the second pass):
    9648c4df0fc019355954fd3c5c117737486af0c24c3e1a2380333ea8f807e8f1  nn_model.py
    6c648399bfe26d5d65b1ea56c87f1f1ec4dc945e5627cd1434c0985df19f1383  t1c_levelA.py
    19063f4cbaba0e4759fc1fe05e3d7a39e56bf6e54521f6ded615a691b66839f3  t1c_dp.py
    72d5f1c041e56f63fe95787509cc0eec542a27dcc6c5cf639b889f722a272af8  t1c_analysis.py
    23f40823da5c0202073b901e6255b55f8c8809cb0d5bec5e4daf2296a08306e9  a1_3dm.py

## 2026-11-26T22:13:43Z — second pass complete (these are the cited runs); all logs reached their last line

Every sig file of the second pass is byte-identical (`cmp`) to the one of the first pass.

Item 1 (Theorem 1c):
* `run21_part1.log` (4.0 s, 33.7 MB): as run01 — 29 instances, 126 621 pair sets, 16 654 connected and
  unpseudoknotted; uniqueness of the ordering 0 violations; LA ≠ L0 0; mutant detected 29/29.
* `run22_levelA_q8.log` (170.9 s, 16.6 MB) → `sig_levelA_q8_v2.json`: as run02 (837 compositions, 20 families,
  7 156 938 non-crossing pair sets, 1 309 291 connected structures; all violations 0 except the separator
  inequality at B = 1: 351 135; controls 7 196 / 111 848 / 14 988; LB ≠ LA 0; mutant DP 810/837).
* `run23_levelA_3x3.log` (305.3 s, 16.3 MB) → `sig_levelA_3x3_v2.json`: as run03 (256 compositions,
  12 446 720 pair sets, 1 883 167 structures; violations 0; controls 960 / 85 170 / 1 344; mutant DP 255/256).
* `run24_dp_q9to12.log` (49.9 s, 115.8 MB) → `sig_dp_q9to12_v2.json`; `run25_dp_2x7_7x2_3x5.log` (382.9 s,
  485.4 MB) → `sig_dp_q14_15a_v2.json`; `run26_dp_5x3.log` (239.7 s, 283.1 MB) → `sig_dp_5x3_v2.json`: as runs
  04–06.
* `run27_analysis.log` (19.8 s, **1449.2 MB** — under the limit, but the largest of my processes that finished):
  39 families (m,B), 1 656 instances (multisets), 67 141 ordered instances, 322 270 116 708 connected structures
  with equal items not distinguished (321 675 760 413 with B ≥ 2; 59 513 958 395 467 with all strands labelled),
  15 766 tiling structures.
  - C1 tilings have E = E_0 identically: 0 violations of 15 766.
  - C2 Theorem 1c as stated, regime |x| ≥ |σ|, B ≥ 2: 1050 grid points (X, γ ∈ (1/20)ℤ, γ also 5, 50) and 10
    boundary points (X = 1 + min(1,γ) − 10⁻⁶; X = 1): **0 violations**; least value of gap − ε_x is 0 (ε_x attained).
    C2c control (gap claimed 1/20 larger): fails at 9 293 (family, grid point) pairs.
  - C3 control B = 1: for every m = 2…12 the conclusion fails at all 1010 grid points of the regime
    (front triple (1,1,0): one pair, E − E_0 = |σ| − |x| ≤ 0).  m = 1, B = 1 has no non-tiling structure.
  - C4 control B = 2 outside the hypothesis: a non-tiling structure at or below E_0 at 435 of 435 grid points
    (m = 2…7).  ⇒ the hypothesis is exact at B = 2.
  - C5 the note's three control models: violating instances 1079, 1079, 280 of 1385 (B ≥ 2).
  - C6 exact region `|x| < min(B|σ|, |σ|+γ)`: 0 violations in all 39 families; for m ≥ 2 the triples (1,1,1)
    (straddle) and (B,1,0) (unpaired block) are present, so the region is exact for every family with m ≥ 2.
    C6b: for B ≥ 3 the conclusion holds at all grid points outside the stated hypothesis with
    `|x| < min(B|σ|, |σ|+γ)` (74 … 204 points per family).
  - C7 gap `min(|σ|, |σ|+γ−|x|, B|σ|−|x|)`: never undercut (0 of all grid points, all families); attained at every
    grid point for every family with m ≥ 2.
  - C8 smallest counterexamples: B = 1: `a = (2), m = 2` (template GAG, item CC; N = 5, 2 strands), one pair
    G3–C1: E − E_0 = |σ| − |x| (0 at x = σ).  B = 2, γ-branch: `a = (4), m = 2` (N = 9, 2 strands), all four
    pairs with the A bulged: E − E_0 = |σ| + γ − |x|; yes-instance `a = (1,1,2)`, order (1,2,1).  B = 2,
    σ-branch: `a = (4), m = 2`, pairs G4–C2, G5–C1 only: E − E_0 = 2|σ| − |x|; yes-instance `a = (2,2)`.
    B = 3: nothing at |x| = 2|σ|, γ = 2|σ|; first failure at |x| = 3|σ|: `a = (6), m = 2`; yes-instance (3,3).

Item 2 (Lemma A1):
* `run30_a1_special.log` (13.6 MB), `run31_a1_exh_nv3_m3.log` (252.0 s, 15.5 MB), `run32_a1_exh_nv4_m2.log`
  (19.2 s, 14.3 MB), `run33_a1_sample_nv4_m3.log` (189.1 s, 23.3 MB): the same numbers as runs 10–13.
* `run34_a1_random.log` (43.8 MB), new: seed 20261126.  (a) 3000 random formulas, 2–7 variables, 1…3·nv clauses
  of 1–3 literals with repetitions (2361 satisfiable, 639 not; largest q = 114, |T| = 379): all violations 0
  (counting identity on 8 337 082 939 matchings; recipe 0 of 13 321; decoding 0 of 92 193); six controls
  (without "unlinked") all produce disagreements (39 … 554).  (b) 3000 random pure 3-CNF formulas, 3–7 variables,
  3nv…6nv clauses (2287 satisfiable, 713 not; largest q = 252, |T| = 882): all violations 0 (recipe 0 of 6 174;
  decoding 0 of 114 350); identity without (ℓ−1)! fails on 2287.

Shell slip (no effect on any result): the background command for runs 22–23 ended with `tail -2 a b`, which
GNU tail rejects; the tool reported "exit code 1" although both runs had reached their last line.  Also I used
one foreground `sleep 100` to wait for run 25.

## 2026-11-26T22:13:53Z — housekeeping

Deleted, each by its explicit name (no wildcard), three first-pass files of my own that are byte-identical
duplicates of second-pass files (sha256 compared just before):
`sig_dp_q9to12.json` (= `sig_dp_q9to12_v2.json`, ac4f65e9…), `sig_dp_q14_15a.json` (= `sig_dp_q14_15a_v2.json`,
a5081491…), `sig_dp_5x3.json` (= `sig_dp_5x3_v2.json`, d1eeb688…) — 122 MB.  The first-pass logs run04–run06
that name them stay.  The small first-pass files `sig_levelA_q8.json`, `sig_levelA_3x3.json` stay.

## 2026-11-26T22:16:19Z — network use (textbook lookup only; generic queries; nothing of this project in a query)

Purpose: the brief asks whether the textbook garbage collection (Garey–Johnson, Theorem 3.2) is of quadratic size
and what makes the note's version linear.  I do not have the book.

Searches (tool: web search, 2 queries):
1. "Garey Johnson 3-dimensional matching NP-complete proof 3SAT truth-setting satisfaction testing garbage
   collection number of triples m(n-1)"
2. "standard reduction 3-SAT to 3-dimensional matching number of triples quadratic "m^2 n^2" Garey Johnson garbage
   collection linear size reduction ETH 3DM lower bound"

Addresses opened (5):
* https://www.cs.toronto.edu/~vassos/teaching/c63/handouts/3DM.pdf — HTTP 403, **not read**.
* https://en.wikipedia.org/wiki/3-dimensional_matching — read through the fetch tool's summary only
  [summary of the page]: reduction from 3SAT with variable gadgets ("the number of triplets is twice the number
  of occurrences of x_i"), clause gadgets, a garbage-collection gadget; cites Garey–Johnson "Section 3.1 and
  problem SP1 in Appendix A.3.1".  No size bound stated.
* https://arxiv.org/abs/2411.05796 and https://arxiv.org/pdf/2411.05796 — F. Pfaue, bachelor's thesis (arXiv
  v1, 25 Oct 2024), §2.1.11 "3-SAT ≤SSP 3-Dimensional Matching" [full text of that section, read in the text
  extracted with pdftotext]: "The reduction is inspired by [GJ79], but changed slightly"; the sets are
  X = {x_i(j), x̄_i(j) | 1 ≤ i ≤ n, 1 ≤ j ≤ m}, helper elements a_i(j), b_i(j), clause elements s_1(j), s_2(j);
  true/false triples per (variable, clause) pair with a cyclic shift in one helper index; clause triples
  (ℓ_i(j), s_1(j), s_2(j)).  So in the Garey–Johnson-style gadget **every variable has 2m tips, one pair per
  clause, whether or not it occurs there**.  (This thesis avoids garbage collection by asking for a matching
  of size ≥ k; it does not show Garey–Johnson's garbage component.)
* https://arxiv.org/abs/2003.00336 — S. Kushagra, "Three-dimensional matching is NP-Hard" (29 Feb 2020)
  [abstract, through the fetch tool's summary; the tool did not return it verbatim]: the standard NP-hardness
  proof reduces 3SAT to 3DM with a power-4 blow-up; the note gives a linear-time reduction; under ETH the lower
  bound improves from 2^{o(m^{1/4})} to 2^{o(m)}.
* The search tool's own summaries (reading level [search snippet], sources not opened) said: "the standard
  reduction of 3-SAT to 3DM constructs a set with |M| in Θ(m²n²)".

What this settles, and at which level: that the textbook reduction is superlinear (Θ(m²n²) triples, "power 4")
is [search snippet] + [abstract]; that its variable gadget has 2m tips per variable is [full text of a secondary
source that says it follows GJ79 "changed slightly"]; Garey–Johnson's own garbage component (from my memory:
m(n−1) pairs, each joined to all 2mn tips) stays **[from memory — unverified]**.  Garey–Johnson's book itself was
not read by me.  A linear-size reduction 3SAT → 3DM exists in the literature (Kushagra 2020, [abstract]); I did
not compare its construction with Lemma A1.

## 2026-11-26T22:20:44Z — run 28: direct structure-by-structure test with explicit loop-energy functions

New script `t1c_direct.py` (sha256 2c5f7d18373d7e2433c4e6ccdb09b768a64144a9df5b89b529005b6b8c19c3c2; the frozen
scripts are untouched): energies computed face by face (exact rationals) from the generic face decomposition,
independent of the signature algebra of `t1c_analysis.py`; two loop-energy tables — extremal (every bulge/interior
loop exactly γ) and a seeded random table γ + {0, ¼, …, 2} depending on the numbers of unpaired template and
item bases.  Trial on mB ≤ 6 first (scratch log `logs_tmp_direct_q6.txt`).
* `run28_direct_q8.log` (116.9 s, 29.8 MB; reached its last line): 837 ordered instances, 957 901 connected
  structures with B ≥ 2 and 351 390 with B = 1.
  - 8 models in the regime (x = σ with γ = ½, 3, 1/1000; |x| = 5/4, γ = ½; |x| = 149/100, γ = ½; |x| = 7/4, γ = 2;
    |x| = 199/100, γ = 5; σ = −3, x = −4, γ = 2) × 2 tables: **0 violations** of "tiling ⇒ E = E_0" and of
    "non-tiling ⇒ E ≥ E_0 + ε_x"; with the extremal table the least value of E − E_0 − ε_x is 0 in all 8 models.
  - Control B = 1 (same 8 models): the gap claim fails for 68 199 … 351 135 structures in every model/table.
  - Controls outside the hypothesis, extremal table: (σ,0): 220 non-tiling structures at or below E_0;
    |x| = |σ|+γ = 3/2: 220; |x| = 2|σ|, γ = 2: 1 730; |x| = 9/4, γ = 3: 1 730.  (With the random table the first two
    have 0 — there the one-base A bulge costs γ + 1, so those models are inside the hypothesis with a larger γ.)

### Proof of the sharpened statement (to go into the report as replacement text) — checked again by hand
For every x ≤ 0 identity (2) holds: `E − E_0 = |σ|L + P − d(m − 1 − z)`, d = |x| − |σ| of either sign.
B ≥ 2, d ≥ 0: h := Σ_{inner f∈𝔉}(k_f − 1) + Σ_{f∈𝔉∩{F_0,F_K}} k_f wholly unpaired blocks ⇒ L ≥ h(B−1);
m − 1 = h + #(inner faces of 𝔉) ≤ h + r + z ⇒ E − E_0 ≥ |σ|(L − h(B−1)) + h((B−1)|σ| − d) + r(γ − d) + P''.
Non-tiling ⇒ bulge/interior loop (≥ γ − d) or L ≥ 1 (h ≥ 1: ≥ (B−1)|σ| − d; h = 0: ≥ |σ|).
B ≥ 2, d ≤ 0: case-1 identity; a bulge/interior loop gives ≥ γ + |σ| − |x|; otherwise an item bond off the stacks
and a loose GG bond both lie on non-flush exterior loops: ≥ (|σ| − |x|) + |x| = |σ|.
B = 1: case 1 of the note, gap |σ| − |x|.  Unified: hypothesis |x| < min(B|σ|, |σ|+γ), gap
min(|σ|, |σ|+γ−|x|, B|σ|−|x|).  Necessity for every m ≥ 2, B ≥ 1: the one-item instance a = (mB) (a no-instance):
all paired with m−1 bulged separators: E − E_0 = (m−1)(|σ| + g_A − |x|); paired with the last block only:
E − E_0 = (m−1)(B|σ| − |x|).  Both re-derived by hand; the m = 2, B = 2 and m = 2, B = 1 cases agree with C8/C9.

## 2026-11-26T22:22:32Z — run 29: controls for three checks that had none

`t1c_controls_extra.py` (sha256 02f19b08db3a20d54ae8f08ddac4445ea7fb2dca0f036837ca1a9430e57ccd08), log
`run29_controls_extra.log` (13.3 s, 13.9 MB, reached its last line):
* U′ uniqueness of the ordering with connectivity dropped: 4 520 of 27 538 pair sets (9 labelled instances with
  ≥ 2 items) are non-crossing for two or more orders — so the check U (0 violations among connected pair sets)
  could have failed.
* F′ Fact 1 with "three or more nicks": 296 372 violations among 567 498 non-crossing pair sets (mB ≤ 7).
* T′ "tiling iff every base paired": 164 violations; T″ "tiling iff no bulge and no interior loop": 46 243
  violations (126 571 connected structures, mB ≤ 7).

## 2026-11-26T22:28:09Z — run 35 (control for the counting identities); report drafted; totals recomputed

* `t1c_controls_ident.py` (sha256 4d062446b792d0f1bfc97b9388a37c575e40563cedd603f87218abb76b4eb1da), log
  `run35_controls_ident.log` (7.4 s, 13.0 MB, reached its last line): with the correct definitions both identities
  hold for 126 571 of 126 571 connected structures (mB ≤ 7); with a mis-defined flush face (template side ignored)
  each fails for 53 026 structures.
* Report drafted at `docs/science/workstreams/R25_REPORT.md`.
* **Own error no. 3:** in the first draft of the report I added three control totals by hand (the separator
  inequality without r / L / z over runs 22–26) and got all three wrong (302 270 372; 18 133 642 957; 1 379 325 164).
  Recomputed from the logs by a script: **302 271 336; 18 133 641 957; 1 379 325 464**.  All other sums in the
  report were then recomputed by script as well: 19 603 658 non-crossing pair sets; 3 192 458 structures visited one
  by one; 594 356 295 structures at B = 1 (594 356 283 non-tiling; 594 352 200 violating the separator inequality);
  182 033 formulas (4 903 unsatisfiable); 809 792 recipe matchings; 7 011 451 decoded matchings.

## 2026-11-26T22:31:28Z — run 36: the two structure counts quoted in the note are reproduced

`t1c_labelled_counts.py` (sha256 d95a632b97905395fc6ce5220465a398edb9741bb1c90660cacd307e7a43f61c), log
`run36_labelled_counts.log` (143.2 MB; reached its last line): number of connected unpseudoknotted structures per
instance with all strands labelled, from my signature files (Σ over orders of sizes × Π_s μ_s!).
* §6 of the note quotes "up to 1 887 888 structures per instance" (instances with 2 ≤ m ≤ 3, 3 ≤ B ≤ 5) and "up to
  762 294 structures" (generalised test).  My enumeration gives **exactly 1 887 888 for a = (2,2,3,3), m = 2, B = 5**
  and **exactly 762 294 for a = (2,4,4), m = 2, B = 5** (and for the families (1,10), (5,2), (10,1) with the same
  item multisets, since the count does not depend on where the separators are).  The note does not name the
  instances, so this is agreement of two seven-digit numbers, not a comparison instance by instance; these are
  the only numerical outputs of their enumerators visible to me (their code and logs were not available).

## 2026-11-26T22:33:29Z — sharpness of Theorem 1c′ for every m ≥ 2, by three explicit structures (hand + data)

For the replacement text I replaced the one-item instance a = (mB) (which shows necessity of the range but attains
the gap only for m = 2) by a = (2B, B, …, B) (m − 1 items, no packing; n − m = −1, M = m(B−1) + 1, E_0 = σM − x):
* S1: long item on blocks 1 and 2, separator bulged: m(B−1) stacks + one bulge ⇒ E − E_0 = |σ| + g_A − |x|.
* S2: long item paired with block 2 only (its 3′ half and block 1 on F_0): (m−1)(B−1) stacks ⇒ E − E_0 = B|σ| − |x|.
* S3: a = (B,…,B), B ≥ 2: tiling with the pair at the 5′ end of the template removed: M − 1 stacks ⇒ E − E_0 = |σ|.
Checked against the enumerated signatures (read from the sig files, not a new run): key "3,3|3,6" has
(st,fl,nb) = (6,0,1) ×1 and (4,0,0) ×12; "3,3|3,3,3" has (5,0,0) ×12 non-tiling; "4,3|3,3,6" has (8,0,1) ×1 and
(6,0,0) ×16; "3,4|4,8" has (9,0,1) ×1 and (6,0,0) ×15 — the predicted signatures in each case.

## 2026-11-26T22:35:16Z — closing entry

* Report: `docs/science/workstreams/R25_REPORT.md` (verdict: Theorem 1c, regime |x| ≥ |σ|: proved as stated;
  Lemma A1: proved with one degenerate gap — empty clauses — closed here; 0 critical, 0 major, 7 minor findings).
* Disclosures: (1) one temporary file of mine outside the two permitted places — the pdftotext output of the
  downloaded PDF, in the session scratchpad (`…/scratchpad/r25_web/ssp.txt`) — removed by explicit name
  (`rm` of the file, `rmdir` of the empty directory) at about 22:34; the fetch tool keeps the PDF itself in its own
  tool-results directory.  (2) A read-only `git status` shows an untracked `NOTES.md` at the repository root
  (22:31 UTC, 4 930 bytes, content about `r26_influence.py`): **not mine** — every entry of this workstream is in
  this file — and I did not touch it.  (3) No tool action was declined; one address returned HTTP 403.
* Final sha256 of the code (frozen scripts unchanged since 21:54; four small scripts added after the second pass):
    9648c4df0fc019355954fd3c5c117737486af0c24c3e1a2380333ea8f807e8f1  nn_model.py
    6c648399bfe26d5d65b1ea56c87f1f1ec4dc945e5627cd1434c0985df19f1383  t1c_levelA.py
    19063f4cbaba0e4759fc1fe05e3d7a39e56bf6e54521f6ded615a691b66839f3  t1c_dp.py
    72d5f1c041e56f63fe95787509cc0eec542a27dcc6c5cf639b889f722a272af8  t1c_analysis.py
    2c5f7d18373d7e2433c4e6ccdb09b768a64144a9df5b89b529005b6b8c19c3c2  t1c_direct.py
    02f19b08db3a20d54ae8f08ddac4445ea7fb2dca0f036837ca1a9430e57ccd08  t1c_controls_extra.py
    4d062446b792d0f1bfc97b9388a37c575e40563cedd603f87218abb76b4eb1da  t1c_controls_ident.py
    d95a632b97905395fc6ce5220465a398edb9741bb1c90660cacd307e7a43f61c  t1c_labelled_counts.py
    23f40823da5c0202073b901e6255b55f8c8809cb0d5bec5e4daf2296a08306e9  a1_3dm.py
* Cited logs (each starts with a clock line and ends with its `peak memory` line): run21–run29, run30–run36.
  First pass (same numbers; kept): run01–run06, run10–run13.  Scratch: `logs_tmp_*.txt`, `tmp_trial_*.json`.
