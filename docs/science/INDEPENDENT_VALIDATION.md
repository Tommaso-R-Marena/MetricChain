# Independent validation record — science division

What this division has independently **replicated** (re-computed with its own code or on
its own machine) and independently **reviewed** (read and re-derived) of the other
divisions' work.  The two are kept apart; nothing is claimed that was not done.  Reviews by
workstreams are entered here when the coordinator has read their reports.

---

## 1. Replications

### 1.1 The theory division's audit at its head `5ed4072` — passes on a third platform

| item | value |
|---|---|
| command | `bash scripts/audit_all.sh` (unmodified), default mode (quick falsification pass) |
| commit | `5ed407282d89af46d260d2dd1687059c8e3e7728` (the science branch point; tree identical to the theory head except for *untracked* science files under `docs/science/`, `docs/collaboration/` and `experiments/science/`) |
| machine | cloud container, Linux 6.18 x86_64, 4 cores (shared with eight workstreams during the run), Lean 4.31.0 from the release archive, Mathlib from `lake exe cache get`, Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1, mpmath 1.3.0 |
| start / end (UTC) | 2026-11-25 17:38:15 / 18:11:23 (33 min wall clock) |
| result | **`AUDIT PASSED`**, exit code 0 |
| self-test | planted violations detected; axiom-walk self-test ok |
| Lean | 56 files, 31 571 lines, build without incomplete-proof warnings; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 3423 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 386 headline theorems checked |
| harness | `ALL TESTS BEHAVE AS EXPECTED` (survivors and the 22 documented refutations) |
| mutation tests | **267 mutations: 266 caught, 1 expected pass, 0 not as expected** |
| benchmarks, reference checker, conformance vectors, doc references | pass |
| log | `experiments/science/audit_replication/audit_all_5ed4072.log` |

These numbers are the ones the theory division reports for its head in
`docs/collaboration/status/theory.md` (56 files; 3423 declarations; 267 mutations, 266
caught, one expected pass).

> **Correction (2026-11-25 18:35 UTC; the sentence as first published at `3593950` is kept
> below, struck through).**  When this record was written we had read the engineering
> branch at `db56d05`, where the audit had been replicated at `d81eb8a` and `4cef47e` (46
> files, 3101 declarations).  The engineering division's checkpoint 3 (`4b19048`, committed
> 18:09 UTC, two minutes before our run ended) reports a replication at **`63efc69`** (53
> files, 3369 declarations, 207 mutations; ENG-MSG-0003 §2).  So ours is the **first
> replication of the three Lean files added after `63efc69`** — `TwoRounds`, `GroupSampling`,
> `SliceRefinement` — and of the harness and mutation blocks added with them (128 tests, 267
> mutations), and an independent *second* replication, on a third platform, of the other
> seven.
>
> ~~The engineering division had replicated the audit at `d81eb8a` and `4cef47e` (46 files,
> 3101 declarations); this is the first replication of the ten Lean files and the harness
> blocks added since (`BoundedAccuracy`, `FieldShift`, `GamePair`, `CoverStability`,
> `SetLimit`, `TypeQuantiles`, `SymmetricSampling`, `TwoRounds`, `GroupSampling`,
> `SliceRefinement`).~~

*What a passing audit does and does not establish.*  It establishes that the statements
labelled **[V]** are consequences of the Lean kernel's axioms as stated in the Lean files,
and that the registered numerical tests behave as registered.  It does not establish that
a Lean statement says what the prose attributes to it (our reviews check this for the
sections they cover), nor anything about statements labelled **[P]**.

### 1.2 The engineering division's lattice-chain class tables, `n = 1 … 10` torsions — identical

Own enumerator (`experiments/science/pi_chain/dia_chain.py`; written from the model
definition, not from their code): for every `n = 1 … 10` the number of self-avoiding
conformations, the number of profile classes, and the full table (profile → number of
conformations, least gauche count, its multiplicity, largest gauche count) are **identical**
to `experiments/eng/chain_cover/data/dia_Sc12_n{n}.txt` at `db56d05`
(3, 9, 27, 79, 233, 683, 2 005, 5 849, 17 107, 49 833 conformations; 2, 4, 7, 13, 22, 37, 57,
90, 129, 190 classes).  At `n = 12` a derived quantity agrees: the identified interval of
§11.2 of `INFERENCE_LIMITS.md` computed from our enumeration (width 0.527) and from their table
(0.5265).  Beyond `n = 12` we have used their tables without replicating them.

## 2. Reviews

| id | object | by | state |
|---|---|---|---|
| SCI-REV-0001 | theory report §11.25 (slices) | workstream R1 | **published.**  No critical finding; four major (headline covers two of three exponents; a missing proof step at negative accuracies, supplied; two false statements in a remark at `5ed4072`, already corrected by the theory division; Lemma 11.89 in print), twelve minor.  Replicated with own code: Lemma 11.89 on `10⁷` tables and at 60 digits; Theorem 11.90(a) with 3–5 blocks incl. negative accuracies; (b) by brute force; (c) on 270 400 grid points; the table; Corollary 11.91's numbers; Theorem 11.92 and Lemma 11.93 by enumeration; `SliceRefinement.lean` compiled.  Not reviewed: Theorems 11.78(b), 11.79(c).  One statement attributed to referee R10 not reproduced |
| SCI-REV-0002 | theory report §11.22 (limit shape) | workstream R2 | **published.**  No false theorem; two major findings on wording and on the proved bracket; eight minor.  Replicated with independent code: walk class tables for 4–23 beads (identical to engineering's; `2.1·10⁹` conformations), bridge tables for 4–24 beads, the concatenation lemma exhaustively (`2.7·10⁸` pairs), both linear programmes with own exact certificates, all volume bounds, covering numbers at 15, 21 and (from the engineering table) 27 beads.  Read only: walk tables for 24–27 beads, the periodic-system enumeration, the plateau estimates |
| SCI-REV-0003 | theory report §11.24 (rounds of adaptivity) | workstream R4 | **published.**  No critical finding; one major (Theorem 11.84(ii) false as stated: cost bounded on the good event only; one-line repair), nine minor.  Replicated with code written before the authors' code was opened: `θ₂*`, `T^{(2)}(0)`, `h` at nine slopes; the exact twins table in every printed digit and one more row; the asymptotic gap; Lemma 11.85 end to end on whole cubes.  Own harness for Claims A/B (350 runs).  Read only: Theorems 11.56, 11.58, 11.51; the recursion for `r ≥ 3`; not examined: Proposition 11.88(e) |
| SCI-REV-0005 | theory report §11.26, Theorems 11.99, 11.101 | workstream R5 | **published.**  Theorem 11.99 proved (three independent numerical routes on 56 site/slope pairs to `10⁻¹²`); 11.101(a) proved; 11.101(b) proved with two gaps in the written proof, closed.  All reference numbers replicated to the published rounding (one slope jump differs in its second digit); `RenyiCentre.lean` compiled.  Read, not re-derived: Theorem 11.52's accounting.  Not replicated: exact joint-type sums for `n ≤ 480`.  Nothing simulated by anyone |
| — | our own `INFERENCE_LIMITS.md` v2 (adversarial referee) | workstream R3 | **done; corrections published as SCI-MSG-0008; the note is now version 3.**  No numbered statement false, no proof broken; eight major findings (two false sentences, the rest overstatements), thirteen minor.  Replicated with the referee's own code: Theorem 2 on three further codes (extended Golay on the full `2²⁴` cube), Theorem 3 on five codes with the exact optimum as a linear programme, Proposition 5b's numbers, Theorem 7 on random and adversarial instances, the tables of §9 (12/12), §11.1 (27/27), §11.2 (22/22), §11.4 (16/16), the engineering class tables for `n ≤ 9`.  Not re-run: the author's own scripts; the compact-decile row of §11.4.  The referee's own statements R1–R6 are **[P]**, unrefereed |

* **Theory report §11.28 (ratios of macrostate weights; at `dcdfea6`) — independent review
  by the coordinator and independent replication of Theorems 11.105 and 11.106**
  (SCI-RES-0005).  Re-derived: 11.105 (a)–(e), 11.106, 11.107.  Replicated with own code
  (`experiments/science/pi_inference/ratio_duality_replication.py`; nothing of the theory
  division imported): 400 random instances (4–12 states, asymmetric envelopes, `A ∪ B ≠ X`)
  — full programme = `B → A` programme = bipartite dual to `3·10⁻¹⁵`; a control without
  the triangle inequality (243 of 400 strictly different); 396 one-state closed forms;
  400 sandwiches; 24 threshold cases on the cube (uniform and non-monotone exchangeable
  weights) to `7·10⁻¹⁵`.  `MacroRatio.lean` compiled here from a scratch copy (exit 0;
  nine statements; standard axioms).  **Not replicated:** Theorem 11.107's numbers,
  Theorem 11.108 (limit and numbers).  §11.29: with workstream F.

### Originality reviews (prior art; not reviews of correctness)

| id | object | by | state |
|---|---|---|---|
| SCI-REV-0004 | theory report rows G11, G18, G20–G23, G25–G27 | workstream A1 | published; follow-up on THY-REQ-0011 B1, B2 running |
| SCI-REV-0006 | theory report rows E1, D3, D4, C4, G1, G4, G7, G13, G16, G19, G24 | workstream A2 | published |
| SCI-MSG-0002 | our own `INFERENCE_LIMITS.md` | workstream M | published; follow-up on Theorems 7, 8 running |

### Replications made by workstreams, read by the coordinator

* A1: the table of theory report §11.20 at `u = 2`; `h`, `a` at four slopes; `0.0293` at
  `n = 6400`; Lemma 11.89 on 400 000 random tables.
* A2: the lever-arm exponent `3/2` (and a sharper constant); C4 on 20 000 instances; the
  referee's count 802 075 walks / 541 profiles on the square lattice.
* Coordinator: the theory division's reference value `a = 0.294791` for the three-letter
  site of THY-MSG-0011 §1(c), by an own Blahut–Arimoto computation of the capacity of the
  vertex channel (`experiments/science/pi_inference/vertex_channel_chain_rule_check.py`); the
  smallest homometric pair of lattice chains of A2.

### Re-runs by the coordinator of workstream results (same machine; the workstream's own scripts — a re-run, not a second implementation)

* **P (force-field pilot):** `verify_openmm_direct.py` — 508 clash-free conformations of the
  tripeptide grid and `c_i(g_GB) = 16.09 12.41 18.63 16.43 15.14 11.19 kcal/mol`, computed from
  OpenMM 8.6.1's own force objects without the workstream's fast evaluator;
  `an9_torsion_refits.py` — range 1.1147 kcal/mol of ff99SB − ff14SB along φ, independent of ψ
  to `3·10⁻⁷`; ff19SB − ff14SB: 5.0 kcal/mol on the clash-free part of a 5° map (`c_φ = 3.7`,
  `c_ψ = 4.4`).  Everything else of `SP_REPORT.md` is the workstream's own measurement, read
  but not re-run.
* **K (kinetics):** `KineticsCertificates.lean` compiled with `lake env lean` (exit 0; 32
  theorems; axioms `propext`, `Classical.choice`, `Quot.sound` for 31, none for one; no
  `sorry`); the statements of `box_cut_barrier`, `box_cut_barrier_residual`,
  `certified_trap_height`, `trap_survival`, `trap_certificate`, `box_trap_certificate` read
  against the report; scripts `t1_cut_duality.py`, `t3_cover.py`, `t9_trap_stationary.py`
  re-run with output identical to the committed files.  The workstream's enumeration
  reproduces the engineering division's conformation counts 683, 2 005, 5 849 for 6, 7, 8
  torsions (as does our own enumerator, §1.2).
* **R4 (review of §11.24):** `TwoRoundsExpected.lean` compiled (exit 0; four theorems;
  standard axioms; no `sorry`); `m1_demo.py` re-run with identical output (the run violating
  Claim B); `exponents.py` re-run in full (13 minutes): all values at the five slopes of
  the theory report reproduced; the wording of Theorem 11.84(ii) read in the theory report.
* **A1 (addendum):** `addendum_checks.py` re-run (15 checks passed, 0 failures); items 1–3 of
  Proposition A1.2 and the two formulas of the `e^{u/2}` rule re-derived by hand; two of the
  workstream's citations checked earlier (SCI-REV-0004), none of the addendum's new ones
  re-opened by the coordinator.
* **R1 (review of §11.25):** the reviewer's four-line proof of Lemma 11.89 re-derived by
  hand; `ceiling_check.py` and `thm_1190a_blocks.py` re-run (all pass; the latter reports a
  value `6·10⁻⁹` at the cusp `X = 0`, within its tolerance — the reviewer's m11).
* **R5 (review of §11.26):** `t06_bruteforce_orientation.py` and `t09_lemma_Tprime.py` re-run
  (zero violations; the negative control of the first produces 8 602).
* **X (alternative frameworks):** `n1_coset_formula.py` re-run ("N1 OK": aliasing formulas
  to `3·10⁻¹⁴`; spectra of exact order `m` recovered with zero posterior variance on dual BCH
  designs; `sup P_A² ≤ 4·NL` in every printed case); the arguments of Theorem 3(a),(b),
  Proposition 5′(a) and Proposition 8(c) re-derived by hand.  The comparison tables and
  every other statement of `SX_REPORT.md` were read, not re-run.
* **L1 (Lean formalisation of our note):** all eight files compiled by the coordinator with
  `lake env lean` (exit 0 each; 78 `#print axioms` lines, every one
  `[propext, Classical.choice, Quot.sound]`; no `sorry`, `admit` or `native_decide` in the
  sources; no error or warning line).  Statements read against the note: not yet done line
  by line by the coordinator — the workstream's own discrepancy list (four items) is in
  `L1_REPORT.md`.
* **R6 (review of the cost of the nested adaptive algorithm, theory report §§11.18–11.19):**
  by the coordinator — `separation.py 1.0 1000,1350,1400` re-run (identical: `ln C_max` =
  126.3, 150.8, 154.0 against `ln LB_na` = 110.9, 149.0, 155.0); **the two lower-bound
  columns of the separation table recomputed with independent code**
  (`experiments/science/pi_inference/nonadaptive_lb_crosscheck.py`: ten numbers at five
  `(u, n)`, identical to the report's); the central count re-derived (`M·p(s_je^{−x}) ≤
  [4KJe·s_j/(ℓe^b)]·[4e^{b+1}ℓ/s_{i+1}] = 16KJe²e^{j−i−1} < 16KJe²e^x` — the two factors `e^b`
  cancel) and the corner inequality `E_1 ≥ (n_o+2)E_0` of the cap remark; the reviewer's
  two Lean files compiled (they print the axioms of eleven statements of the theory
  division: all `[propext, Classical.choice, Quot.sound]`); **the sampler bias confirmed
  independently** (`numpy_binomial_bias_check.py`: mean 91.26 for 92 at `n = 2⁶¹`, `z = −47`;
  a Poisson control is unbiased).  **Not done by the coordinator:** the re-derivation of
  the whole proof (the reviewer's), the 4 075 literal runs and the campaigns (not
  re-run), the `C_max` column (it reproduces the engineering division's published
  values according to the reviewer).  *Kind of check:* an independent review with an
  independent derivation, and an independent replication of the numerics, by one
  reviewer.
* **P2 (class constants in rotamer variables on a fixed backbone):**
  `verify_openmm_direct_sc.py` re-run by the coordinator (9 s, OpenMM 8.6.1; Ser₃ on the
  strand, 729 assignments, OpenMM's own `CustomGBForce` and force groups, explicit loops,
  none of the workstream's evaluators): `c_i(g_GB) = 4.81 4.12 4.32`,
  `c_12, c_13, c_23 = 1.306 2.426 1.308`, `c_123(g_GB) = 4.03·10⁻³`, `c_123(f) = 5.86·10⁻¹³` kcal/mol
  — identical to the committed log.  Three citations checked against the PubMed records
  (Gaillard and Simonson 2014, doi:10.1002/jcc.23637; Marshall, Vizcarra and Mayo 2005,
  doi:10.1110/ps.041259105; Villa et al. 2017, doi:10.1002/jcc.24898): bibliographic data
  and the quoted abstract sentences are as the report gives them.  **Not re-run:** the
  140 enumerations (2.4 h), the analyses, the covers; the 584 MB of grids are not under
  version control.  A measurement by one workstream, not independently replicated.
* **F (local data with a field; also a review of theory report §11.29 at `dcdfea6`):**
  re-derived by the coordinator — Lemma 0 (window), Lemma 1 (indistinguishability with an
  oracle), Lemma 2 (the excess of a dip is the cone law, within `1/(e^r − 1)`), Lemma 3
  (compensation), every step of the proof of Theorem A, the algebra of Theorem B, and
  the tilt inequality of Proposition C(a).  Re-run: `t16_exact_rational.py` in a scratch
  copy — output identical to the committed file (base and alternative have identical
  one-body marginals as fractions).  Own check, nothing imported from the workstream:
  `experiments/science/pi_inference/compensation_lemma_check.py` — twelve random cases,
  `n ≤ 10`: both members in the class, all marginals equal to `3·10⁻¹⁵`, the gap formula
  exact, and without the compensator the marginals differ by `0.03 … 0.37`.  **Not checked
  by the coordinator:** the identification with the theory division's `R^max`, `θ_na`
  (read); Propositions C(b), D, E; Theorem τ; all tables, including the corrections of
  the theory division's numbers.  This is an *independent derivation* of the theory
  division's Proposition 11.109 (a)–(d) and a proof of its conjecture (f); it is not a
  replication of their numerics (their scripts were not run).
* **L2 (second Lean wave: A11, A13, R6.1, R6.2, R5(2), A1.2 items 1–3):** all three files
  compiled by the coordinator with `lake env lean` (exit 0 each; 65 + 70 + 43 = 178
  `#print axioms` lines, every one `[propext, Classical.choice, Quot.sound]`; no error or
  warning line; no `sorry`, `admit`, `native_decide`).  Statements and definitions read
  against the paper for: `cube_sandwich_mean`, `cube_ratio_range_eq_Icc`,
  `stepField_sandwich_mean`, `cube_sandwich_fails_negative_beta`, `excess_identity`,
  `r6_2_binary_cube`, `r6_2_cosets` (with `partSum`, `meanEn`, `twinMin`, `excessMass`,
  `excessEnergy`, `basin`, `basinW`, `overlapW`, `cosetDist`), `condLaw_mem_window`,
  `klBound_pi_of_vertices`, `extremePoints_window_eq` — they say what the paper says, with
  the corrections listed in SCI-MSG-0014.  Not read line by line: the other 160-odd
  declarations; the proofs (the kernel checks those).
* **R3 (referee of our note):** R6.1, R6.2, R6.3 and their assembly into Theorem R6
  re-derived line by line by the coordinator (checkpoint 21; notes in addendum A12): no
  gap; the gain is slightly better than stated (`1 − 3/(4r₁)` in place of `1 − 1/r₁`).
  Corollary R6′ (both oracles) written out and re-derived at checkpoint 25 (addendum A12).
* **Own statement A11 (robust macrostate ratios):** exact linear programmes over the weight
  cone, 900 instances with the hypotheses (field optimal to `5·10⁻¹⁴`), 300 + 298 control
  instances with one hypothesis dropped (field not optimal in most);
  `experiments/science/pi_inference/monotone_ratio_check.py`.  A numerical trap is
  recorded there: default solver tolerances gave three spurious deviations of `10⁻⁶ … 10⁻⁵`.
* **Own statements (addenda A10):** the attenuation lemma checked with exact rational
  Krawtchouk values and 60-digit sums for `n = 100 … 800`, `u = 1, 2`
  (`experiments/science/pi_inference/dip_attenuation_check.py`): identity A10.1 to `10⁻⁵⁹`;
  the bound of A10.2 holds with a margin of five to ten.

* **Own statements (addenda A13–A15):** A13 — 360 exact linear programmes over ordered
  alphabets (`ordered_alphabet_ratio_check.py`); A14 — exact transfer matrices
  (`helix_coil_robust_range.py`); A15 — exact linear programmes for 11, 13 and 15 beads
  (`pi_chain/scattering_identified.py`, `scattering_fixed_instrument.py`); the 13-bead table
  of SCI-MSG-0011 compared entry by entry with the stored results at checkpoint 25 (one
  rounding corrected), and the class counts quoted in request S-E1 (1 346, 11 328, 95 673)
  with the logs of `identified_sets.py`.  Author's computations; no second implementation.
* **A1 (Proposition A1.1), second time:** the four steps re-derived by the coordinator at
  checkpoint 25 (conditional laws in the window; chain rule and information radius;
  Azuma; the truncation inequality `E|Â/A − 1| ≤ √(τ/M) + 2ν(dν/dQ > τ)`) before repeating
  the claim to the theory division in SCI-MSG-0011 §4.

* **Own statements (addendum A16), author only:** entropy bracket — 400 random members of
  the class by enumeration (`n ≤ 11`), equality at the cone and at the zero residual to ten
  digits; the two relative entropies and their series to `10⁻⁹`; plateau twins — exact
  sums over the joint law of the two distances (overlapping supports), ten cases,
  `n = 600 … 2000`: root above `κ_lo`, gap above the proved bound, radii against the
  asymptotic formula (`experiments/science/pi_inference/plateau_twin_check.py`).  One
  numerical trap met and recorded (`DEAD_ENDS.md` SD31).  Lemma A16.5: the best
  energy-feasible modification on *every* support of `Q_4` (65 534 supports × 9 parameter
  pairs) and on 8 000 random supports of `Q_5`, `Q_6` against the plateau on the initial
  segment of the same size — no violation (largest `3·10⁻¹⁴`); 1 398 random members with
  dips and hills, `n ≤ 10`; Theorem A16.6(iii): `G(r₂−2) <` gap `= G(r₂−1) < G(r₂)` in eight
  exact cases (`energy_isoperimetry_check.py`).  **No second reader.**
* **L1, statements against the note (owed since checkpoint 18; done at checkpoint 26 for
  the headline statements):** the Lean statements `theorem4_adaptive_marginal_oracle`,
  `theorem4'_nonadaptive_marginal_oracle`, `theorem4'_binary_cube_closed_form`,
  `theorem4'_one_body_closed_form`, `lemma1_uniform_marginals` and `theorem7` were read line
  by line against Theorems 4, 4′ (addendum A1), Lemma 1 and Theorem 7 of the note: they
  say what the note says, with the conventions listed in the file headers (accuracy
  `ε/2` and gap `> ε`; the bound without division; the expectation at the uniform oracle
  answer; the oracle-indexed model of an algorithm; Theorem 7 in its Pinsker form).
  Not read line by line: the remaining declarations of the eight files.

## 3. Not validated by us

Everything not listed above.  In particular the paper proofs of theory report §§11.16–11.17,
11.20–11.21 and 11.23 (refereed by the theory division's own referees R5–R10) have not
been reviewed by this division; statements of ours that lean on them say so
(`docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`, "Dependencies").
