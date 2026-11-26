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

*A limitation of the mutation count at `5ed4072`, reported by the theory division at its
fourteenth checkpoint (its `DEAD_ENDS.md` D55 item 12; THY-RES-0007 §7).*  The mutation
runner of that commit ran mutants in quick mode and counted any failing run as
"caught", without first running the *unmutated* harness on the same selection in the
same mode; a test that misbehaves in quick mode without any mutation would have had
all its mutations counted as caught.  In our run the full quick harness passed in the
same audit ("ALL TESTS BEHAVE AS EXPECTED"), which excludes the failure they found for
tests that the quick harness and the runner's selections exercise identically, but we
did not check that they do.  So "266 caught" at `5ed4072` is the runner's count, with
that caveat; the runner at `658b77f` checks a baseline per selection (§1.4).  We did not
copy the runner into any file of ours.

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
(0.5265).  Beyond `n = 12` the coordinator has used their tables without replicating them.

**Extended by workstreams** (independent enumerators each): R2 — walk class tables for
4–23 beads; **R7 — the class tables for 1–22 torsions at `a2f6dc7`, identical** (21 and 22
were computed remotely only on the engineering side); for 23–24 torsions the total
numbers of conformations equal the published series of self-avoiding walks on the
diamond lattice, the class decomposition was not examined.  See §1.3.

### 1.3 The engineering division's results at `a2f6dc7` — replication by workstream R7 (SCI-REV-0008)

| item | what was done | result |
|---|---|---|
| off-lattice ("generic") chain: conformations and profile classes, 5–14 torsions | own enumerator from the model definition | identical |
| off-lattice covers: 72 cells at 5–10 torsions, the 6 exact cells at 11; tie analysis; 60 entropy numbers | own cover code | identical; at 12 torsions and for the open brackets: consistency of own bounds only |
| lattice class tables, 1–22 torsions | own enumerator (C) | identical |
| the 288 published lattice covers | verified as covers on the unreduced instances | all valid |
| the 263 lattice cells published as optima | own lower bounds with exact certificates | **254 certified without any solver's search** (241 by an exact LP-duality certificate, 13 by a branch and bound with an exact certificate at every pruned node); 9 rest on HiGHS's search |
| Harper closed form for the uniform-cube hitting numbers | re-derived; own code; exhaustive over all subsets for `n ≤ 4`, including the programme over all minimal sensitive sets | all 52 stored rows identical |
| single-flip constants up to 14 torsions | own code | identical; 15–16 not examined |
| adversarial test of Algorithm 2L⁺ (X-005) | the engineering code re-run at reduced size (a re-run, not a replication); the reduction to tail functions re-derived and checked exhaustively on small cubes | two cells bit-identical; maximisers for `n ≤ 2000`; reduction correct as stated |

*Kind of check:* an independent replication with code written before the corresponding
engineering implementation was read, on one core, no computation above 15 minutes; no
remote job was re-run.  *By the coordinator:* finding M1 verified on the engineering
branch (`git show a2f6dc7:…`: the keys of the stored rows 1–18 against 19–24; the loop
over solvers in `covering_number_P` stops at the first proof of optimality); the
reviewer's `own_harper.py table 14` re-run and compared row by row with the stored
`harper_fc_table.json` (52 rows, no difference); Propositions G1, G2 of the report
(squared distances of the off-lattice chain are polynomials in `c = −cos θ` with rational
coefficients of degree at most `q − p − 1`; `cos 69°` has degree 16, so for at most 14
torsions an equality is an identity) re-derived — conjugation by `diag(1, −1, −1)` removes
odd powers of `sin θ`, the mirror image removes `√3`; the examples `5 + 4c` (trans) and
`2 + 4c + 3c²` (gauche) for the 1–4 pair checked by hand.  **Not examined by anyone here:** the class
decomposition at 23–24 torsions; CP-SAT's proofs; nine HiGHS-only optima; single-flip
constants at 15–16 torsions and the envelope test; X-001; ENG-RES-0006 §2; the
correctness of the mean-run evaluator (the algorithm's cost proof is SCI-REV-0007).

### 1.4 The theory division's audit at its head `658b77f` (fourteenth checkpoint) — passes on this machine

| item | value |
|---|---|
| command | `bash scripts/audit_all.sh` (unmodified), default mode |
| tree | `git archive 658b77f`, extracted outside the repository (no science files in it; nothing of the theory branch modified); Lean packages shared with our tree by a symbolic link (same `lean-toolchain`, `lake-manifest.json`, `lakefile.lean` as at `5ed4072` — checked with `git diff`) |
| machine | the same cloud container as §1.1, 4 cores shared with six workstreams |
| start / end (UTC) | 2026-11-25 23:23:53 / 23:53:36 (29 min 43 s wall clock) |
| result | **`AUDIT PASSED`**, exit code 0 |
| self-test | planted violations detected; axiom-walk self-test ok |
| Lean | **60 files, 32 393 lines; `Build completed successfully (8618 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 3474 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 412 headline theorems checked |
| harness (quick mode) | **`ALL TESTS BEHAVE AS EXPECTED`** |
| mutation tests | **342 mutations: 341 caught, 1 expected pass, 0 not as expected**; 115 baseline runs of the unmutated harness (one per selection): all behave as expected — the check added by the theory division at this commit (its D55 item 12) |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 028 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_658b77f.log` |

All numbers are those the theory division reports for this head in its status file
(60 files; 3474 declarations; 342 mutations, 341 caught, one expected pass).  (Checkpoint
34 was committed while the mutation stage was still running; this table was completed
at checkpoint 35.)  New since our replication at `5ed4072`: four Lean files
(among them `TwoRoundsExpected.lean`, which is our workstream R4's file adopted by them,
and `Scattering.lean`, their machine-check of our Proposition A2.1) and the harness
blocks XXII–XXIII, XIV.5, XX.5, XXI.6, DEAD.25–27.  *Kind of check:* a re-run of their
script on a third machine — a replication of the computation, not a review of what the
statements say (workstream R9 reads two of the new Lean files against the prose).

### 1.5 The theory division's audit at its head `b2d3e9c` (fifteenth checkpoint) — passes on this machine

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive b2d3e9c` extracted outside the repository; the build directory of the run at `658b77f` re-used |
| start / end (UTC) | 2026-11-26 00:09:02 / 01:04:13 (55 min wall clock on a machine with a load average of 12–14; 31 min of CPU) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | **62 files, 34 078 lines; `Build completed successfully (8620 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 3603 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 434 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` |
| mutation tests | **374 mutations: 373 caught, 1 expected pass, 0 not as expected**; 124 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 142 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_b2d3e9c.log` |

The numbers are those of the theory division's status file at this head (62 files; 3603
declarations; 374 mutations, 373 caught, one expected pass).  New at this commit:
`proofs/Frontiers/BoxClass.lean` (their §11.30) and `MonotoneSandwich.lean` — the latter is
our `experiments/science/ws_L2/Sandwich.lean` as published at `9a0865f`: compared with `diff` by
the coordinator, the only differences are their provenance paragraph (8 lines) and the
removal of our closing `#print axioms` block (71 lines).  So the audit now walks, and this
replication re-checks, two Lean files written by this division.  *Kind of check:* a
re-run of their script on a third machine.  (Checkpoint 36 was committed while this run
was in progress; the table was completed at checkpoint 39.)

**A caveat on the mutation stage of §1.1, §1.4 and §1.5, added at checkpoint 42.**  The
theory division reported (THY-RES-0009 §6, `DEAD_ENDS.md` D57 on its branch at `24a3c27`)
a second hole in its mutation runner: a mutant that *crashes* inside a test was counted
as caught, and one old mutation had been "caught" in this way for eleven checkpoints.
Our three replications ran that runner as committed, so their counts of caught
mutations (266 of 267; 341 of 342; 373 of 374) include mutants that may have crashed
rather than been detected.  The replication at `24a3c27` (§1.6) uses the repaired runner.

### 1.6 The theory division's audit at its head `24a3c27` (sixteenth checkpoint) — passes on this machine, with the repaired mutation runner

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive 24a3c27` extracted outside the repository; the build directory of the run at `b2d3e9c` re-used |
| start / end (UTC) | 2026-11-26 01:50:05 / 02:21:46 (32 min wall clock, on a machine shared with three workstreams) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | **65 files, 34 791 lines; `Build completed successfully (8623 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 3655 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 452 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` |
| mutation tests | **411 mutations: 410 caught, 1 expected pass, 0 not as expected**; 131 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 180 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_24a3c27.log` |

The numbers are those of the theory division's status file at this head (65 files; 3655
declarations; 411 mutations, 410 caught, one expected pass).  New at this commit and
therefore re-checked here for the first time outside their machine:
`proofs/Frontiers/ThirdOrderModel.lean`, `ShareCertificates.lean`, `HilbertBall.lean`
(present in the built tree; their statements are being read by our workstreams P4 and
L4, not by this run).  **The mutation runner at this head is the repaired one** — read
by the coordinator: `experiments/mutation_tests.py` lines 74–79 classify a mutant whose
test ends with an exception as "NOT AS EXPECTED (the mutant crashed)", and line 8 of its
header states the rule — so "410 caught" here means detected, not crashed, which the
counts of §1.1, §1.4, §1.5 could not claim.  *Kind of check:* a re-run of their script on
a third machine; one function of the runner read.  Not done: reading the 37 mutations
added since `b2d3e9c`; running the harness in its full (non-quick) mode.


## 2. Reviews

| id | object | by | state |
|---|---|---|---|
| SCI-REV-0001 | theory report §11.25 (slices) | workstream R1 | **published.**  No critical finding; four major (headline covers two of three exponents; a missing proof step at negative accuracies, supplied; two false statements in a remark at `5ed4072`, already corrected by the theory division; Lemma 11.89 in print), twelve minor.  Replicated with own code: Lemma 11.89 on `10⁷` tables and at 60 digits; Theorem 11.90(a) with 3–5 blocks incl. negative accuracies; (b) by brute force; (c) on 270 400 grid points; the table; Corollary 11.91's numbers; Theorem 11.92 and Lemma 11.93 by enumeration; `SliceRefinement.lean` compiled.  Not reviewed: Theorems 11.78(b), 11.79(c).  One statement attributed to referee R10 not reproduced |
| SCI-REV-0002 | theory report §11.22 (limit shape) | workstream R2 | **published.**  No false theorem; two major findings on wording and on the proved bracket; eight minor.  Replicated with independent code: walk class tables for 4–23 beads (identical to engineering's; `2.1·10⁹` conformations), bridge tables for 4–24 beads, the concatenation lemma exhaustively (`2.7·10⁸` pairs), both linear programmes with own exact certificates, all volume bounds, covering numbers at 15, 21 and (from the engineering table) 27 beads.  Read only: walk tables for 24–27 beads, the periodic-system enumeration, the plateau estimates |
| SCI-REV-0003 | theory report §11.24 (rounds of adaptivity) | workstream R4 | **published.**  No critical finding; one major (Theorem 11.84(ii) false as stated: cost bounded on the good event only; one-line repair), nine minor.  Replicated with code written before the authors' code was opened: `θ₂*`, `T^{(2)}(0)`, `h` at nine slopes; the exact twins table in every printed digit and one more row; the asymptotic gap; Lemma 11.85 end to end on whole cubes.  Own harness for Claims A/B (350 runs).  Read only: Theorems 11.56, 11.58, 11.51; the recursion for `r ≥ 3`; not examined: Proposition 11.88(e) |
| SCI-REV-0005 | theory report §11.26, Theorems 11.99, 11.101 | workstream R5 | **published.**  Theorem 11.99 proved (three independent numerical routes on 56 site/slope pairs to `10⁻¹²`); 11.101(a) proved; 11.101(b) proved with two gaps in the written proof, closed.  All reference numbers replicated to the published rounding (one slope jump differs in its second digit); `RenyiCentre.lean` compiled.  Read, not re-derived: Theorem 11.52's accounting.  Not replicated: exact joint-type sums for `n ≤ 480`.  Nothing simulated by anyone |
| SCI-REV-0007 | theory report §§11.18–11.19 (the cost of the nested adaptive algorithm) | workstream R6 | **published.**  No critical or major finding; Theorems 11.52, 11.54, 11.56, Proposition 11.57, Theorem 11.58 proved (an accounting written before reading the authors' reproduces theirs constant by constant); the sample-cap remark of `40c5bd7` proved with one uncovered pass closed; eight minor points.  Replicated: an own implementation, 4 075 literal runs (847 with invalid inner answers), the engineering division's published costs to every digit.  New: an every-`n` two-level cost and a certified finite-`n` separation; numpy's binomial bias.  Coordinator's checks: see the re-runs below. |
| SCI-REV-0008 | the engineering division's experiments X-002 … X-006 and their record at `a2f6dc7` | workstream R7 | **published.**  No wrong number; two major findings (the two-solver validation cannot be regenerated; floating point at its limit at 13 torsions of the off-lattice chain — exact arithmetic over `ℚ[cos θ]` proposed), minor findings on the wording of "certified", of the `1/√n` decay and of the count of mean runs, and on provenance.  Replication: §1.3. |
| SCI-REV-0009 | the theory report as revised at `658b77f` against our five reviews (second round); the theory division's exact-semigroup sketch | workstream R9 | **published.**  All major findings applied correctly; their four points back right; three corrections of our own texts; one new false sentence, eight minor defects; statements written while revising (the `χ²` bound, Proposition 11.69a, `Scattering.lean`) refereed.  New: Theorem R9.1 (coboundary; Newton–Okounkov body; counting).  Replicated with own code: all bridges to 22 beads; `1.6·10⁸` + `3.5·10⁸` ordered pairs to 13 beads; the four packings and the volumes in exact rationals; site functions to nine digits; `E′ − E` with R4's code (a re-run).  *By the coordinator:* Theorem R9.1(a) re-derived; `r9_cobound.c` recompiled in a scratch copy and run on all 6 869 641 pairs with at most 11 beads (no failure); `r9_certificate.py` re-run (determinants `1`, `−1`; all checks passed).  Not re-run by the coordinator: everything else. |
| SCI-REV-0010 | the theory division's workstream Y at `658b77f` (`docs/workstreams/Y_REPORT.md`, 612 lines; a two-state nearest-neighbour chain as known part), delivered there unverified | workstream R10 | **published.**  No critical finding; **one major** (the headline "an interaction raises all three exponents" holds at the stated slope `u = 1` and is false as a general statement: `a` and `h` are lowered at large slopes, proved with their own Proposition F and blocks of three sites); twelve minor (one wrong sentence at `p = 0.4`; a negative result proved for the level function instead of the truncated residual, example supplied; two brackets that close; unconverged or truncated scans).  *Reviewed (re-derived):* the reductions (U), (L), (L′), Lemmas A–C, Propositions D, F, G, H, I, J(a), Theorem E(a).  *Replicated with own code written before theirs was opened:* controls and vertex counts, every lower end and the Markov recursion to every printed digit, the tilt-state upper ends with a differently built safe discretisation (all slightly below theirs), tables 6.1–6.2 (55 entries), the small-`n` enumerations, the quantile counter-example.  *Re-run of their functions at new parameters:* the reversal cells.  *By the coordinator:* Propositions R10.1 (both expansions; a sign corrected) and R10.2 re-derived; the example of m2 by hand; their `ylib` functions re-run at two cells (`0.495806`, `0.467509` against `0.502282`); the exact capacities of chains of one to four sites with a third code (`pi_inference/r10_reversal_check.py`: vertex counts, `a_4`, the increments of the report's §3.5 to all digits).  **Not checked by anyone here:** Theorem E(d), (e); §6.4; the LP ascent for `n = 8–12`; §8.1, §8.4, §9; the Lean files; Theorems 11.95, 11.97, 11.98, 11.99, 11.101 themselves (hence no algorithmic upper bound); floating-point rounding.  Not re-run by the coordinator: the scripts of `ws_R10/` |
| SCI-REV-0011 | the theory division's Proposition 11.69b at `24a3c27` (theory report lines 5553–5648; two scripts; harness test XVIII.7), requested by them | follow-up of workstream R9 (`workstreams/R9_ADDENDUM.md`) | **published.**  Nothing false; four minor (a constant `168` where the cost is exactly `A + B ≤ 60`; an interior estimate stated with a threshold it does not need; a remark that fails from 12 beads on; a clause of a harness text true for some pairs only) and the false parenthesis C1 of SCI-REV-0009, still there.  *Reviewed (re-derived):* the equivalence of the two definitions of clean, (a), (b), the estimate of (c).  *Replicated with own code (first-round code, written before their scripts existed):* the counts of clean bridges for 3–12 beads against their membership test on the same enumeration (24 484 bridges, no disagreement); exact additivity on all 176 400 ordered pairs with at most 8 beads in their normalisation; heads and tails for 3–12 beads; the lattice by own row reduction, two minors and five classes with determinant 1.  *Their code re-run:* `t4_head_tail.py`, `t4_lattice_index.py`, outputs byte-identical.  *By the coordinator:* the proposition and Lemma 11.68 read in full at `24a3c27`; the 12-bead counter-example checked from its coordinates with independent arithmetic (a valid self-avoiding bridge; the pair at squared distance 11 after a tail of two; none after a tail of three); the determinant; `r9b_check.py` re-run from a clean copy (identical apart from three timing lines).  **Not checked:** Kaveh–Khovanskii, Theorem 1.6; the harness helpers; anything beyond 13 beads (pairs) and 20 beads (cleaning) |
| SCI-REV-0012 | the theory division's Theorem 11.18a, Propositions 11.18b, 11.18c at `24a3c27` (theory report §11.7; `ThirdOrderModel.lean`, `ShareCertificates.lean`; harness XI.16–XI.18), requested by them; and their share certificate on our instances | workstream P4 (`workstreams/P4_REPORT.md`) | **published.**  No critical finding; **one major**: Proposition 11.18c(a) claims Proposition 11.18b on reset-closed domains and its completeness part is false there (two-site counter-example, checked by enumeration, flow and LP; re-checked by the coordinator by brute force); minor: its sentence about our pruned domains is wrong as a description; three rewordings.  *Reviewed (re-derived):* every part of 11.18a, 11.18b, 11.18c; the Lean statements read against the report's wording.  *Replicated with own code:* second- and third-order constants by another algorithm (identical to the stored ones in 908 analyses); the share certificate by exact rational max-flow with exact verification of every certificate and of an over-dense witness for every refusal (908 analyses); soundness `m ≤ E` at every state of 1 023 (instance, model) pairs; the remainder bounds on 60 random and 114 real non-product domains.  *Re-run of their code:* harness blocks XI.16–XI.18 (their frequencies reproduced); copies of their two Lean files compiled against our tree (one import line changed in one copy).  *By the coordinator:* Propositions 11.18b, 11.18c read in full; the counter-example and the pruned-domain finding recomputed (`pi_inference/p4_adoption_check.py`); `p4_00`, `p4_01`, `p4_01b`, `p4_03`, `p4_04` re-run from a clean copy (identical apart from run times); both Lean copies re-compiled and compared with the originals by `diff`.  **Also a negative finding about our own workstream P2** (linked correction of SCI-MSG-0015).  **Not checked:** the citations of 11.18b(b); share certificates on non-product domains; LP rejections are floating-point statements; nothing fed to their kernel; not re-run by the coordinator: `p4_02`, `p4_06`, `p4_07`, `p4_08` |
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

* **Theory report §11.29 as rewritten at `b2d3e9c` (their Theorem 11.109a, Proposition
  11.109b — our workstream F's results in their words) — reviewed by the coordinator
  against `SF_REPORT.md` at their request** (SCI-RES-0008 §1): the statements coincide
  item by item (compensation lemma, the excess on the cone law, Theorems A and B with
  their constants, the tilt inequality, the bracket).  Their `U_γ(e) = inf_λ R̄_γ(e − c_γ(λ); θ − λ)`
  with `R̄ = max(R, −e)` is the statement our code computed: the game form with `t ≤ 1`
  vanishes at `t = 1` for every additive base (nine cases), equals the plain-dip profile
  form for `−a_γ ≤ e ≤ 0` (15 cases, to `10⁻¹²`), equals `−e` below, and equals the closed form
  from balls on the uniform cube (`experiments/science/pi_inference/tilt_negative_argument_check.py`,
  which imports the workstream's single-letter code).  *Kind of check:* a reading against
  our own report and one numerical check; not a re-proof.  **Not verified:** that their
  `R_λ` of Theorem 11.78(b) equals the plain-dip profile form at an additive base with a
  field; Theorem 11.78(b) itself.
* **Theory report §11.30 (box classes; their Theorem 11.110, Corollary 11.111) — read in
  full by the coordinator** (SCI-RES-0008 §3), after an independent re-derivation of the
  same statements from their preview (addendum A17 (0); three numbers re-computed): no
  error found.  Not read: `BoxClass.lean`, harness block XXIV.

### Originality reviews (prior art; not reviews of correctness)

| id | object | by | state |
|---|---|---|---|
| SCI-REV-0004 | theory report rows G11, G18, G20–G23, G25–G27 | workstream A1 | published; follow-up on THY-REQ-0011 B1, B2 running |
| SCI-REV-0006 | theory report rows E1, D3, D4, C4, G1, G4, G7, G13, G16, G19, G24 | workstream A2 | published |
| SCI-MSG-0002 | our own `INFERENCE_LIMITS.md` | workstream M | published; follow-up on Theorems 7, 8 running |
| SCI-RES-0009 | theory report §11.30 (box classes), statements (a)–(e), and our own addendum A17 (A17.1–A17.8) | workstream A3 | published (checkpoint 39): 47 sources read in the relevant passages, about 93 located; classification statement by statement; **20 quoted passages re-read by the coordinator in the downloaded sources — all agree** (list in SCI-RES-0009 §4); what could not be accessed is listed there and in `A3_REPORT.md`.  *Kind of check:* an originality review with full-text reading; the workstream compared statements and did not referee proofs |

### Replications made by workstreams, read by the coordinator

* A1: the table of theory report §11.20 at `u = 2`; `h`, `a` at four slopes; `0.0293` at
  `n = 6400`; Lemma 11.89 on 400 000 random tables.
* A2: the lever-arm exponent `3/2` and its constant (**not** a sharper one, as this line said until checkpoint 34: the same formula as in the theory division's workstream G report at other parameters — corrected in SCI-RES-0007 §2, `DEAD_ENDS.md` SD38); C4 on 20 000 instances; the
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

* **Own statements (addendum A16) — the author's checks (refereed since: see the next item):** entropy bracket — 400 random members of
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
  exact cases (`energy_isoperimetry_check.py`).  ~~No second reader.~~
* **Addendum A16, refereed by workstream R8 (checkpoint 35; SCI-MSG-0016).**  Every step
  re-derived by the referee; its own numerics with nothing imported from ours: 576
  members and an adversarial entropy minimisation for A16.1; twelve own plateau twins
  and our ten reproduced; **Lemma A16.5 over general members** (a convex programme with
  rigorous LP bounds on every support of `Q_3`, `Q_4`, 650 random supports of `Q_5`, `Q_6`; an
  exhaustive grid of `1.15·10⁷` + `2.77·10⁸` Lipschitz functions) — no violation; the
  algebraic core in Lean (`ws_R8/A16Core.lean`).  Findings: Theorem A16.6 (ii)–(iii)
  over-claimed and is repaired (R8.2–R8.5); one printed algorithm wrong without its
  gauge; one script of ours aborted before its cited output.  *By the coordinator:* R8.2
  (quantile form), R8.3 (`G(r₂−1) − (U″−U₀)₊ ≤ gap ≤ G(r₂)`: the three steps and the
  derivative `d ln Z^{pl}/dU₀ = −1/(1+c*+U₀)`) and the counterexample to the printed bracket
  re-derived; `A16Core.lean` compiled (exit 0, standard axioms, no `sorry`) and
  `plateau_optimal` read against the lemma; `r8_07_deepend.py`, `r8_08_matching.py` re-run
  from a scratch copy (output identical to the committed logs); our repaired
  `plateau_twin_check.py` re-run to its end — the regenerated data identical to the
  committed file in all 260 entries.  **Not re-run by the coordinator:** the referee's
  brute force over general members (5 min), its conjecture families, its non-adaptive
  bracket (29 min).  *Kind of check:* an independent review with independent numerics by
  one referee inside this division — not an external review.
* **L1, statements against the note (owed since checkpoint 18; done at checkpoint 26 for
  the headline statements):** the Lean statements `theorem4_adaptive_marginal_oracle`,
  `theorem4'_nonadaptive_marginal_oracle`, `theorem4'_binary_cube_closed_form`,
  `theorem4'_one_body_closed_form`, `lemma1_uniform_marginals` and `theorem7` were read line
  by line against Theorems 4, 4′ (addendum A1), Lemma 1 and Theorem 7 of the note: they
  say what the note says, with the conventions listed in the file headers (accuracy
  `ε/2` and gap `> ε`; the bound without division; the expectation at the uniform oracle
  answer; the oracle-indexed model of an algorithm; Theorem 7 in its Pinsker form).
  Not read line by line: the remaining declarations of the eight files.
* **A3 (prior art; checkpoint 39):** besides the 20 passages, the three statements of the
  workstream's own that addendum A17 adopts were re-derived by the coordinator and
  checked with a script written independently of the workstream's
  (`experiments/science/pi_inference/a3_adoption_check.py`, half a minute: A3.2 on 898
  random members and product measures in 50-digit arithmetic, largest ratio `0.993`; the
  second-order sandwich of the Jensen gap on 29 107 random laws; the unhinted rule at the
  centre of a constant box — `545` evaluations, exact failure probability `0.031 ≤ 0.05`
  over three-level members).  The workstream's `check_math.py` was re-run from a clean
  state to its last line; output identical to `check_math.out` up to timings.
* **L3 (Lean; checkpoint 39):** the four files of `experiments/science/ws_L3/` re-compiled
  by the coordinator one at a time with `lake env lean <absolute path>` (Lean 4.31.0;
  20, 38, 7 and 9 seconds): **four exit codes 0, no error, no warning; no `sorry`, `admit`,
  `native_decide`, `axiom`, `unsafe` in any file; 91 `#print axioms` lines, 90 with exactly
  `[propext, Classical.choice, Quot.sound]` and one with `[propext, Quot.sound]`.**
  Checksums of the compiled files are in SCI-MSG-0019 §3.  Read in the files against
  `SF_REPORT.md` §2.0–§2.2 and addendum A16: the definitions (`refW`, `tiltW`, `baseW`, `coneW`,
  `dipW`, `Hkr`, `barW`, `omegaM`, `kappaA`, `betaA`, `oracle1`, `logA`, `LipH`, `InCone`) and the
  statements `theoremA_fin`, `theoremA_group_sharp`, `theoremA_fin_Cm`, `lemma1a`,
  `lemma0_window_lipH`, `lemma2_mass`, `lemma2_dens`, `densW_coneW`,
  `exists_correct_oracle_algorithm`, `A16.lemmaA16_5_of_harper` — they say what the report
  says, with the differences listed in SCI-MSG-0019 §2.  The theory division's two
  imported files were used as compiled in our tree (built on `5ed4072`).  Not read line
  by line: the other declarations; `ChainRuleCube.lean`.  *Kind of check:* machine
  verification plus a reading of the statements by one person.
* **L4 (Lean; after checkpoint 43):** the three files of `experiments/science/ws_L4/` re-compiled
  by the coordinator one at a time with `lake env lean` (23, 11 and 27 seconds): **three exit
  codes 0, no error, no warning; no `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`; 96
  `#print axioms` lines, 94 with exactly `propext, Classical.choice, Quot.sound`, two with
  `propext, Quot.sound`** — the counts of the workstream's own last run.  Read against the
  paper statements: 15 theorems and 7 definitions (`remainder_identity`, `switchedBase_apply`,
  `abs_remainder_le_of_anchored`, `allocation_lemma`, `cover_of_site_shares_order`,
  `anchored_sandwich`; `key_exp_ineq`, `mgf_le_bennettB`, `integral_exp_le_bennettB`,
  `remainder_bracket`, `deterministic_bracket`, `bennettW_sub_antitone`,
  `deterministic_bracket_sharp`, `ceiling_lower_bound`, `iid_certificate_delta`).  The one new
  statement (the sharper upper end) re-derived by hand and checked with independent lines
  on `2·10⁵` random triples and 19 823 random finite laws.  `HigherOrderEnvelope.lean`, which
  the companion file imports, compared with `cmp`: identical in our tree and at `24a3c27`.
  **The theory division's own `AnchoredRemainder.lean` (their seventeenth checkpoint,
  `9408e33`; sha256 `976f2168…c78376`)**, which proves the same identity, allocation and
  sandwich: every statement read by the coordinator next to ours (they agree; table in
  SCI-MSG-0023 §2), and a copy with four `#print axioms` lines compiled against our tree
  (exit 0; `propext, Classical.choice, Quot.sound`).
  Not done: reading the proofs; compiling `bennett_bracket_weights` against the theory
  division's `BoxClass.lean` (not in our tree).  *The workstream's script-generated report
  was not adopted; `workstreams/L4_REPORT.md` is the coordinator's (process note at its head).*
* **P3 (a floor by analysis; checkpoint 40) — review, re-runs, and an independent
  replication of the headline number.**  *Re-derived by the coordinator:* the remainder
  identity (Proposition 1), the chain rule for mixed differences with its first
  corollary (Lemma 2, L1), the allocation lemma at order `m`, the sample-range bound
  (Lemma R), Proposition 6.  *Own script, written independently*
  (`experiments/science/pi_inference/p3_adoption_check.py`, two seconds): the identity on
  2 520 cases (`3·10⁻¹⁵`), the allocation lemma on 24 288 pairs, coverage of the
  sample-range bracket on four laws (miss rate at most `0.0075` at `δ = 0.05`), the corollary
  on 6 000 cases.  *Re-run in a scratch copy of the workstream's directory:*
  `t05_identity.py` (`1.8·10⁻¹³`, as reported); `t01_validate.py gbn2` — its evaluator against
  OpenMM's Reference platform on 14 systems: largest deviation `1.8·10⁻¹¹` kcal/mol, its
  pruned domains equal to P2's in 26 of 26 comparisons (as reported); `run_floor.py V8 P2
  0.70 5 --N 20000 --siteres --w 2` — the row of the report's table reproduced digit for
  digit, 0 violations of the sandwich over 6 561 states, the exact `ln Z = 245.947014`
  inside `[245.913695, 245.967703]` and inside the sampled brackets.  ***Independent
  replication* (different method, different code, P2's evaluator instead of P3's):** the
  coordinator's chain model with exact sampling gives, for Ace-Val₂₀-NMe on PPII,
  `518.2618 ± 0.0007` at first order with anchored tables and `518.2626 ± 0.0001` with
  fitted tables; P3's certified deterministic bracket is `[518.2332, 518.2937]` and the
  intersection of its twelve intervals `[518.2608, 518.2648]`.  At ten residues both
  pipelines enumerate 59 049 states: `291.3352` and `291.335178`.  *Not checked:* Theorem 3
  and Proposition 4 beyond reading; the interval enclosures; 159 of the 160 enumerated
  runs; the twenty-residue certificate itself was not re-run (447 s for the ball) — its
  *value* is what was replicated.  *Kind of check:* independent review of the
  combinatorial core, re-runs of the workstream's scripts, and an independent
  replication of one number; the certificate's validity rests on paper proofs and
  unreviewed code (SCI-MSG-0020 §4).

## 3. Not validated by us

Everything not listed above.  In particular the paper proofs of theory report §§11.16–11.17,
11.20–11.21 and 11.23 (refereed by the theory division's own referees R5–R10) have not
been reviewed by this division; statements of ours that lean on them say so
(`docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`, "Dependencies").
