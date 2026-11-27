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

### 1.7 The theory division's audit at its head `9408e33` (seventeenth checkpoint) — passes on this machine

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive 9408e33` extracted outside the repository; the build directory of the run at `24a3c27` re-used |
| start / end (UTC) | 2026-11-26 03:04:28 / 03:49:57 (45 min wall clock, on a machine shared with three workstreams and two runs of the coordinator) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | **69 files, 37 543 lines; `Build completed successfully (8627 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 4015 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 504 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` (the script prints the last 80 lines of the harness output: 59 tests "survived", 19 "REFUTED (as documented)" are visible in the log; the status file states 170 registered tests) |
| mutation tests | **435 mutations: 434 caught, 1 expected pass, 0 not as expected**; 136 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 377 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_9408e33.log` |

The numbers are those of the theory division's status file at this head (69 Lean files;
4015 declarations; 435 mutations, 434 caught, one expected pass).  New at this commit
and therefore built and axiom-checked here for the first time outside their machine:
`proofs/Frontiers/AnchoredRemainder.lean`, `BarrierCertificate.lean`, `BoxRatio.lean`,
and their adopted copy of our `KineticsCertificates.lean`; the extended `BoxClass.lean`.
(A copy of `AnchoredRemainder.lean` had been compiled separately and its statements
read by the coordinator — SCI-MSG-0023 §2; the statements of the other files are being
read by our review workstream R12, not by this run.)  The classification rule of the
mutation runner (`experiments/mutation_tests.py`, the block read in §1.6) is unchanged
from `24a3c27` (`diff` of lines 60–95: empty).  One stale number seen in passing: the
harness text of test XXIV.8 says "theory report Corollary 11.113" for what the report
numbers Corollary 11.114 (11.113 is the sandwich sampler); nothing depends on it.
*Kind of check:* a re-run of their script on a third machine.  Not done: reading the 24
mutations added since `24a3c27`; running the harness in its full (non-quick) mode.


### 1.8 The theory division's audit at its head `63e36f7` (eighteenth checkpoint) — passes on this machine

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive 63e36f7` extracted outside the repository; the build directory of the run at `9408e33` re-used |
| start / end (UTC) | 2026-11-26 04:42:44 / 05:16:55 (34 min wall clock, on a machine shared with two workstreams and runs of the coordinator) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | **76 files, 43 498 lines; `Build completed successfully (8634 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 4527 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 574 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` (the script prints the last 80 lines of the harness output: 59 tests "survived" and 19 "REFUTED (as documented)" are visible in the log; the status file states 175 registered tests) |
| mutation tests | **464 mutations: 463 caught, 1 expected pass, 0 not as expected**; 141 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 728 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_63e36f7.log` |

The numbers are those of the theory division's status file at this head (76 Lean files;
4527 declarations; 464 mutations, 463 caught, one expected pass; 141 baseline runs).
Seven files are new since `9408e33` and were built and axiom-checked here for the first
time outside their machine: `StateShares.lean`, `SoftMinLowerBound.lean`, `BoxBennett.lean`
(theirs; the first and third build on results of ours and say so in their headers) and
`OracleCompensation.lean`, `OracleLowerBound.lean`, `ProductSamplerChainRule.lean`,
`BennettTwoPoint.lean` (their adopted copies of files written by our workstreams L3, R6
and L4; each header says so).  *Read here:* the file list and the header comments;
the statements of the new files are being read by our review workstream R13, not by
this run, and whether the adopted copies are declaration-for-declaration ours has not
been diffed by the coordinator (their response says "declarations unchanged").  The
classification rule of the mutation runner (`experiments/mutation_tests.py`, the block
read in §1.6) is unchanged from `9408e33` (`diff` of lines 60–95: empty).  The stale
number noted in §1.7 is still there (the harness text of test XXIV.8 says "Corollary
11.113" for what the report numbers Corollary 11.114); nothing depends on it.
*Kind of check:* a re-run of their script on a third machine.  Not done: reading the 29
mutations added since `9408e33`; running the harness in its full (non-quick) mode.


### 1.9 The theory division's audit at its head `f7df44f` (nineteenth checkpoint) — passes on this machine

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive f7df44f` extracted outside the repository; the build directory of the run at `63e36f7` copied in; `lake-manifest.json`, `lean-toolchain`, `lakefile.lean` unchanged since `63e36f7` (`git diff`: empty) |
| start / end (UTC) | 2026-11-26 07:44:22 / 08:25:24 (41 min wall clock, at low priority on a machine shared with two workstreams and runs of the coordinator) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | **81 files, 45 172 lines; `Build completed successfully (8639 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 4642 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 617 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` |
| mutation tests | **492 mutations: 491 caught, 1 expected pass, 0 not as expected**; 145 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 811 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_f7df44f.log` |

The numbers are those of the theory division's status file at this head (81 Lean files;
4642 declarations; 492 mutations, 491 caught, one expected pass; 145 baseline runs).
Five files are new since `63e36f7` and were built and axiom-checked here for the first
time outside their machine: `ShareLevels.lean`, `DownClosedRemainder.lean`,
`BoxAdditions.lean`, `AffineHalf.lean`, `BlockReductions.lean` (two of them adopted from
our review workstream R12, by their headers as quoted in THY-RES-0012).  *Read here:*
the list of files and, by our review workstream R15, `BoxAdditions.lean`,
`BoxRatio.lean` and `BoxClass.lean` in full (statements against the wording of
Corollary 11.114; SCI-REV-0015) — not `ShareLevels.lean`, `DownClosedRemainder.lean`,
`AffineHalf.lean`, `BlockReductions.lean`, whose statements nobody on our side has
read.  *Kind of check:* a re-run of their script on a third machine.  Not done:
reading the 28 mutations added since `63e36f7`; the harness in its full mode.


### 1.10 The theory division's head `9befefd` (twentieth checkpoint) — nothing that the audit builds or runs has changed; the one input that changed passes

Between `f7df44f` and `9befefd` the theory division changed documents and added one
directory of coordinator checks (`experiments/coordinator_checks/three_levels_certified/`,
the subject of our review workstream R16).  Checked here on 2026-11-26, 09:24 UTC:

| item | value |
|---|---|
| files changed under `proofs/`, `scripts/`, `lake-manifest.json`, `lean-toolchain`, `lakefile.lean` | **0** (`git diff --name-only f7df44f 9befefd -- …`; the listings `git ls-tree -r <head> -- proofs scripts` of the two heads are identical, 81 Lean files) |
| files changed under `experiments/` outside the new directory | **0** — the falsification harness, the mutation tests, the benchmarks and the reference checker are the files audited in §1.9 |
| the audited input that did change: the documents, through `scripts/check_doc_refs.py` | run on `git archive 9befefd`, extracted outside the repository: **`doc references OK (2811 declarations indexed)`**, exit code 0 |
| log | `experiments/science/audit_replication/docrefs_9befefd.log` |

*Kind of check:* identity of inputs plus a re-run of the one step whose input changed —
**not** a re-run of `audit_all.sh` at this head.  The build, the axiom audit, the
harness and the mutation tests were not repeated: their inputs are byte-identical to
those of §1.9, which passed on this machine 07:44–08:25 UTC the same day.  The new
directory is not part of the audit script; it is being reviewed (R16), including one
replication with code that does not import the theory division's.

### 1.11 The theory division's audit at its head `628d3e2` (twenty-first checkpoint) — passes on this machine

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive 628d3e2` extracted outside the repository; the build directory of the run at `f7df44f` copied in; `lake-manifest.json`, `lean-toolchain`, `lakefile.lean` unchanged since `f7df44f` (`git diff`: empty) |
| start / end (UTC) | 2026-11-26 10:47:36 / 11:22:03 (34 min wall clock, at low priority on a machine shared with one workstream) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | **85 files, 47 197 lines; `Build completed successfully (8643 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 4899 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 646 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` |
| mutation tests | **503 mutations: 502 caught, 1 expected pass, 0 not as expected**; 146 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 911 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_628d3e2.log` |

Their status file at this head says 85 Lean files, 180 tests, 503 mutations.  Four files
are new since `f7df44f` / `9befefd`: `RateFull.lean` and `SandwichCost.lean` — **ours, adopted**
(written by workstream R13 and by the coordinator; compared here with our originals:
identical except for a provenance paragraph and the removal of the `#print axioms` and
`#check` commands, as THY-RES-0014 says) — and `SplitRule.lean`,
`SymmetricPairHypothesis.lean`, theirs, built and axiom-checked here for the first time
outside their machine; their statements were not read by us.  *A first attempt of this
run stopped in the build step* (`failed to create thread`, exit 134, while building
`SplitRule.lean`): the coordinator had set a virtual-memory limit of 16 GB for the shell,
under which Lean could not start a thread; the three other new files had built.  The
run was repeated without the limit; its log is the one named above, and the log of the
first attempt is not kept in the repository.  *Kind of check:* a re-run of their script
on a third machine.  Not done: reading the 11 mutations added since `f7df44f`; the
harness in its full mode; the kernel-evaluation experiment of their §4 (not part of the
audit script).

### 1.12 The theory division's audit at its head `dd067f1` (twenty-second checkpoint) — passes on this machine

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive dd067f1` extracted outside the repository; the build directory of the run at `628d3e2` (§1.11) copied in; `lake-manifest.json`, `lean-toolchain`, `lakefile.lean` unchanged since `628d3e2` (`git diff`: empty) |
| start / end (UTC) | 2026-11-26 14:03:44 / 14:45:11 (41 min wall clock, on a machine shared with our own computations and one workstream) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | **87 files, 47 657 lines; `Build completed successfully (8645 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 4937 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 659 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` |
| mutation tests | **538 mutations: 537 caught, 1 expected pass, 0 not as expected**; 149 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (2 940 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_dd067f1.log` |

Their status file at this head says 87 Lean files, 4 937 declarations, 183 tests, 538
mutations.  Two Lean files are new since `628d3e2`: `CoreGreedy.lean` — **ours, adopted**
(compared here with our original, `experiments/science/pi_inference/lean/CoreGreedy.lean`:
statements and proofs identical; a provenance paragraph replaces one clause of the header
comment and the two `#print axioms` lines at the end are gone, as THY-RES-0015 says) — and
`TermOrders.lean` (364 lines), theirs: the remainder identity with one order per term, the
hypothesis "at most `m` hosts" with its sharpness, and the split around the anchor (our
requests P8-T1 and A18-T1), built and axiom-checked here for the first time outside their
machine; **its statements were not read by us**.  `AxiomAudit.lean` gained the two imports and
thirteen `#print axioms` lines.  One input of the audit that is neither a proof nor a test
changed: the list of tokens that `scripts/check_doc_refs.py` does not treat as references to
declarations is longer by eleven mathematical symbols (`T_j`, `t_f`, `ρ_h`, `B_m`, `H_τ`,
`J_m`, `c_l`, `g_τ`, `h_a`, `pen_λ`, `ρ_e`); none of the eleven is the name of a declaration in
`proofs/` (searched here).  *Kind of check:* a re-run of their script on a third machine.
Not done: reading `TermOrders.lean`; reading the 35 mutations and the three tests added
since `628d3e2`; the harness in its full mode.

### 1.13 The theory division's audit at its head `3cf14b9` (work in progress after the twenty-second checkpoint) — passes on this machine; the first full audit of that head

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive 3cf14b9` extracted outside the repository; the build directory of the run at `dd067f1` (§1.12) moved in; `lake-manifest.json`, `lean-toolchain`, `lakefile.lean` and `scripts/` unchanged since `dd067f1` (`git diff`: empty); `PATH=$HOME/.lean/lean-4.31.0-linux/bin:$PATH`, `nice -n 5` |
| start / end (UTC) | 2026-11-26 15:31:28 / 16:07:42 (36 min wall clock, on a machine shared with our own computations and two workstreams) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | **90 files, 49 057 lines; `Build completed successfully (8648 jobs)`**; forbidden-token scan: none |
| axiom audit | **`AXIOM AUDIT OK: 5051 declarations`** use only `propext`, `Classical.choice`, `Quot.sound`; 685 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` |
| mutation tests | **552 mutations: 551 caught, 1 expected pass, 0 not as expected**; 151 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (3 018 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_3cf14b9.log` |

This head is not a checkpoint of theirs: THY-RES-0016 says "single-file checks and the axiom audit file pass at this
commit, the full audit will be run at the next checkpoint" — so this run is, as far as their messages say, the
first full run of their audit at a commit that contains the three new files.  Their THY-MSG-0017 (at `07b1a70`)
gives the same counts: 90 Lean files, 5 051 declarations.  New since `dd067f1`: **`GibbsRecovery.lean` (494 lines:
our Proposition A17.19) and `ResolvedPenalties.lean` (378 lines: workstream P9's Proposition P, the reduction step,
the remainder bound with constants that depend on the state)** — the statements are ours, the Lean is theirs; we
read the module docstrings and the statements of the four inequalities and of the two iterations
(`lower_jensen`, `lower_product`, `upper_jensen`, `upper_product`, `log_Z_le_ueStep_iterate`,
`log_Z_le_upStep_iterate`) and the theorem list of the second file, not the proofs — and `LineDynamics.lean` (491
lines, theirs: two lemmas on the rate of their level recursion; **not read**).  `AxiomAudit.lean` gained the three
imports and its `#print axioms` lines; the harness gained items XVI.6, XVI.7 with 14 mutations and two baseline
selections.  *Kind of check:* a re-run of their script on a third machine.  **What it adds for our own results:**
the four inequalities behind every corrected bracket of addenda A17 (19)–(20), and the allocation step behind
every penalty table, compile on a machine that is not theirs and use the three standard axioms only.  Not done:
reading the proofs; the harness in its full mode; `LineDynamics.lean`.

### 1.14 The engineering division's exact checker for "shares at the leaves" certificates (X-012, their answer to our request P7-E2) — re-run here; and what it found in our own checker

*Object:* `src/metricchain_eng/leafcert/`, `experiments/eng/leafcert/run_vectors.py`, `tests/eng/test_leafcert.py` at
`research/ubuntu-engineering` `eb6b872` (the checker entered at `0e5103b`); their report
`experiments/eng/leafcert/REPORT.md` read in full.  *Kind of check:* a **re-run of their code** from a scratch copy
(`python3 -I -B`, gcc 13.3 where they used 15.2), reading our nine certificate files from commit `2b4ccdf` as their
script does; not a review of their code.

| what | result |
|---|---|
| `run_vectors.py` (4.0 s) | both engines (C with 128-bit sums, Python integers) accept all nine files, reject the three controls of each (27), reproduce every count of our table (P7 report §5.2), brute-force minimum 0 over 18 270 to 531 441 states; the `vectors.json` written here equals theirs after removing keys that name times and the platform |
| `pytest tests/eng/test_leafcert.py` | 182 passed in 61 s |
| not run | their long fuzz configuration (`LEAFCERT_FUZZ=10`); the C source was not read line by line |

*What their report found in ours* (its §9, item 1; confirmed): our reference checker `ws_P7/p7_06_check.py` did not
validate its input and summed everything in `U` and `P2` while bounding only the entries of the format — on a
malformed file it could accept a false bound.  None of the nine files is malformed; no verdict or count changes.
Corrected (strict loading, a well-formedness test before any arithmetic, the total over the format's entries only;
two new controls — their example, and an extra key in every leaf: 9 of 9 rejected where the old rule accepts 9 of
9; `ws_P7/logs/p7_06_check_v2.log`); linked correction SCI-RES-0030; coordinator's note at the end of
`workstreams/P7_REPORT.md`.

### 1.15 The engineering division's exact vertex enumeration of the weighted cubes (X-013, their answer to our request R10-E1) — tests re-run here; 48 certified cells reproduced by an independent computation

*Object:* `experiments/eng/weighted_cube/REPORT.md` (613 lines, read in full), `tests/eng/test_weighted_cube.py` and the
package `src/metricchain_eng/weighted_cube/` at `research/ubuntu-engineering` `c81166b`.  *Kinds of check:* a **re-run of
their tests** from a scratch copy (gcc 13.3), and a **replication** of part of their numbers with code of our own written
from §1 of their report (`experiments/science/r10_verification/x013_sitewise_check.py`).  Not a review of their code.

| what | result |
|---|---|
| `pytest tests/eng/test_weighted_cube.py` | 38 passed, 5 skipped in 4 s; with `WCUBE_SLOW=1` 39 passed, 4 skipped in 62 s (the skipped tests compare with the Parma Polyhedra Library, which is not installed here and which we did not install) |
| the capacity of the channel with the `2^L` site-wise labels only, by our own Blahut–Arimoto (lower and upper end meet to `10⁻¹³`), against their certified capacities | 48 cells (`p = 0.45, 0.4, 0.3`; three and four sites): largest difference `9.9·10⁻⁷`, their sixth decimal; the validation value `0.495805524595` per site lies in their interval |
| the five cells where they report that site-wise labels are not optimal (three sites) | ours below theirs, by their printed ratios to `5·10⁻⁶` |
| control | with `u*` on the first site of the block instead of the last, 24 of 24 cells disagree with their table |
| not checked | the upper side (that no vertex does better): their four enumeration methods and the Parma library; anything with five sites; the tables for `h`; their drivers were not run |

*What it found in ours:* the expectation written into our request (SCI-REV-0010 §6 R10-T2, §7 R10-E1: "blocks of four and
five decide …") was a guess stated as a fact, and is wrong for five of the six cells it names; linked correction
SCI-RES-0033 §3.  *What we added:* the weak-coupling limit of the crossover their increments indicate, in closed form
(addendum A17 (23), item 91).

### 1.16 The theory division's audit at its head `b2caab6` (twenty-third checkpoint) — passes on this machine

| item | value |
|---|---|
| command, tree | as §1.4: `bash scripts/audit_all.sh`, unmodified, on `git archive b2caab6` extracted outside the repository; the build directory of the run at `3cf14b9` (§1.13) moved in; the listings `git ls-tree -r` of `proofs/`, `scripts/`, `lake-manifest.json`, `lean-toolchain`, `lakefile.lean` at the two commits are identical (90 Lean files); `PATH=$HOME/.lean/lean-4.31.0-linux/bin:$PATH`, `nice -n 10` |
| start / end (UTC) | 2026-11-26 20:39:56 / 21:13:32 (34 min wall clock, on a machine shared with our own computations and two referees) |
| result | **`AUDIT PASSED`**, exit code 0 |
| Lean | 90 files, 49 057 lines; `Build completed successfully (8648 jobs)`; forbidden-token scan: none |
| axiom audit | `AXIOM AUDIT OK: 5051 declarations` use only `propext`, `Classical.choice`, `Quot.sound`; 685 headline theorems checked |
| harness (quick mode) | `ALL TESTS BEHAVE AS EXPECTED` |
| mutation tests | **575 mutations: 574 caught, 1 expected pass, 0 not as expected**; 153 baseline runs of the unmutated harness, all as expected |
| benchmarks, reference checker, conformance vectors, doc references | pass (3 018 declarations indexed) |
| log | `experiments/science/audit_replication/audit_all_b2caab6.log` |

What changed since `3cf14b9`: no Lean file, no script; `experiments/falsify_conjectures.py` (+449 lines) and
`experiments/mutation_tests.py` (+56) — the harness items for their report §11.33 (the nested algorithm on general
spaces) and 23 more mutations; documents; workstream directories that the audit does not run.  *Kind of check:* a
re-run of their script on another machine.  Not done: reading the new harness items; the harness in its full mode;
their report §11.33 and the rate theorem (Theorems 11.53a, b), which they offer for attack (THY-MSG-0018).

## 2. Reviews

| id | object | by | state |
|---|---|---|---|
| SCI-REV-0027 (workstream R26) | the theory division's §11.33 at `4692f59` (unchanged at `07cde81`): Theorems N1, N1′, N4, N9, N10, Proposition N12; the influence between blocks computed for band models | an AI referee of this division that had not seen the section nor their internal review; offered by them (THY-MSG-0018) | published (checkpoint 69): theorems stand; two major corrections to Proposition N12 and one to the band-model sentence of Theorem N4; the referee's replication uses a simulated inner oracle; **the coordinator replicated the hub finding independently** (`r26_verification/hub_tail_check.py`: the upper-end inequality fails by `1.75·10⁴`–`2.58·10⁴` against the exact product-class tail function) and re-ran five scripts with identical output |
| SCI-REV-0026 | the Structural Biology division's first checkpoint (`aec72df`): the model definition, the claims of their first capability, their prior art, baselines and held-out rule | the coordinator, at their request (STRUCTBIO-REQ-0002); **read only** — their code was not read and nothing was run — plus own checks (eight PubMed records, two documents searched by term, one brute-force script of ours) | published (checkpoint 68): the claim supported as a statement about the model; one major finding on the model (a random seed), one on the state set, four replacement texts; a linked correction of our own prior art.  Not a test of their implementation |
| SCI-REV-0025 | the Structural Biology division's founding commit (`720e0ec`): a certified minimum of an exact pairwise model | the coordinator, under the owner's directive D-3; **read only** (commit message, sync note, module docstrings) | published (checkpoint 67); its §3 corrected by SCI-REV-0026 §6 (prior art) |
| SCI-MSG-0033 (workstream R24) | **our own** results of the evening of 26 November: addendum items 86–90, SCI-MSG-0031, SCI-RES-0032, SCI-MSG-0032 | an AI referee of this division that had not seen them, briefed by their author to attack | **done**: 182 numbers agree with the logs; no critical finding; three major (a wrong reading of the loss between groups; a criterion that lost a clause; a hardness claim that does not follow), thirteen minor — all accepted, the major ones re-checked by the coordinator with own code; linked corrections published.  An internal review, not external peer review |
| SCI-REV-0024 (workstream R25) | the Complexity division's hardness note at `89114ea`: the proof of Theorem 1c for `abs(x) ≥ abs(σ)`, and Lemma A1 | an AI referee of this division that had seen neither the note nor their own review; asked for by them | published (checkpoint 66): both proved (A1 with the proviso of non-empty clauses); seven minor findings, one of them a wider hypothesis with a proof; **review** of every line of the two places, **replication** by enumeration (39 families; 182 033 formulas) with failing controls, **no re-run** (their scripts unavailable).  Coordinator: read in full; three instances by hand; two of the referee's scripts re-run with identical output; one citation verified at record level; compared with COMPLEXITY-REV-0003 (agreement where they overlap) |
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
| SCI-REV-0013 | the theory division's seventeenth checkpoint at `9408e33`, requested by them (THY-RES-0010 §9.2): the corrected Theorem 11.110(e); Propositions 11.18e, 11.113; Corollary 11.114; Theorem 11.18d as written; `BarrierCertificate.lean` and Theorem 11.115 against our formats; harness XI.19, XI.20, XXIV.6–XXIV.10 | workstream R12 (`workstreams/R12_REPORT.md`) | **published.**  No critical finding; **two major** (Proposition 11.18e(b) false as written — a counter-algorithm; the necessary order of Proposition 11.113(d) too large by `e^Δ`); eleven minor with replacement texts.  *Reviewed (re-derived):* both ends of 11.110(e); the dimension, closure and unisolvence of 11.18e; the support lemma (a proof by induction); 11.113(a)–(c); 11.114 (a two-vertex linear programme).  *Replicated with own code:* exact optimal packings on 720 + 1 425 small boxes; the support lemma exhaustively in 128 grid × order cases; 200 exact sandwiches and 400 000 simulated runs; 252 ratio cases; the barrier instances in exact rationals; the adjacency lemma over all box pairs on nine grids.  *Their code re-run:* seven harness blocks; 41 + 56 mutations (all caught); a copy of `BoxClass.lean` compiled against our tree.  *Machine-checked by the workstream:* seven statements (`R12Additions.lean`).  *By the coordinator:* the two sentences read at `9408e33`; M1 re-derived and recomputed with separate code (least good fraction exactly `0.5` over 3 834 affine functions; failure `2⁻⁵` on the extremal member); M2 derived independently before the report was read and its exact binomial failure computed; `R12Additions.lean` compiled (exit 0, standard axioms); `r12_03`, `r12_04` re-run from a clean copy (identical apart from the timing line).  **Not checked by the coordinator:** the other replications and re-runs; `BoxRatio.lean`, `BarrierCertificate.lean` (built by the audit of §1.7, statements read by the workstream only) |
| SCI-REV-0014 | the theory division's eighteenth checkpoint at `63e36f7`, requested by them (THY-RES-0011 §9(a)): the rate of the level recursion (remark after Theorem 11.53; `t4_rate.py`); how five of our reviews were applied (§11.32; Propositions 11.18b, 11.18c; 11.69b; §§11.18–11.19; 11.110(f)) | workstream R13 | **published.**  No critical finding.  The rate is correct and machine-checked by the workstream on top of their lemmas (`RateFull.lean`, standard axioms; compiled again by the coordinator).  One major: Proposition 11.117(b) without "symmetric" is false (counter-example computed by the workstream and by the coordinator).  Twelve minor in their texts, five in ours (linked corrections).  *Kind:* review + replication (own one-sided recursion, block recursions, brute force of share instances) + re-runs of their harness blocks and of `t4_rate.py` + a machine check.  Not checked: their Lean proofs; Theorem 11.116 beyond (c) |
| SCI-REV-0015 | theory report at `f7df44f`: Proposition 11.18e(b′)(i), Proposition 11.18f, Proposition 11.113a, `ratio_expected_queries_ge_mixed` against Corollary 11.114, the necessity argument of Proposition 11.113(d), the outline of the conjecture (b′)(ii) — requested by the theory division (THY-RES-0012) | workstream R15 | **published.**  Nothing false; no critical or major finding; twelve minor (conditions to add: the sampling scheme and the constant of the nested sampler's bound; a linear order and a range of validity for the first-order allocation rule; the conditions on "attained"; four precisions of the necessity argument; two sentences of Corollary 11.114), each with a replacement text; six additions (the bound with `t_f` for `2t_f`; the `f ∓ γ` criterion; ordering vertices; a finite-depth one-site count; a necessity bound that grows with `ln(1/δ)`; `S` is one interval).  Replicated with own code on synthetic instances (168 000 coverage runs; exact linear programmes; all 59 049 vertices of small instances); their harness blocks and `pairing_check.py` re-run.  The coordinator re-derived the main statements and re-ran all seven scripts (logs identical) |
| SCI-REV-0016 | theory report at `9befefd`, §11.19 remark (1b), THY-RES-0013 §4 and `coordinator_checks/three_levels_certified/`: the certified third level — offered by the theory division (THY-RES-0013 §6), accepted in SCI-RES-0018 | workstream R16 (`workstreams/R16_REPORT.md`) | **published.**  No critical finding, no error in the mathematics; the rule (a two-level run of Theorem 11.56 designed for the fibre dimension, a certified accuracy at most the rung's and the failure probability `δ′` of the level above is an admissible inner procedure; the bound is monotone in the servers' costs with the outer design fixed) holds.  **One major** (M1: the two-level worst cases at five of eight sizes belong to a design with another ladder — ENG-RES-0008's `ε*·0.85^i` — than the outer design they are compared with); three minor (the abort rule of Theorem 11.56 as worded proves `C_max + M̄`; the tolerance formula is a supremum; "at the level of expectations" is the mean-run model).  *Replication* (own code, nothing of theirs imported, no instance evaluated): **159 of 159 certified numbers** of their stored outputs to four digits, 1 950 of 1 950 per-rung fields; cross-checked against our R6 exact arithmetic.  *Re-run:* their `summary.py` (byte-identical), one line of `cert3.py`, their `flat_run` on grids.  *New in the review:* without a search and without the mean-run model the comparison "three levels certified below two levels" is true at every outer fraction scanned from `n = 16 000` on and false at `4 000` and `8 000` (exact two-level cost at the flat instance: `0.5336, 0.5110, 0.5027, 0.4998, 0.4961` against `0.6106, 0.5262, 0.4782, 0.4439, 0.4381`).  *Checked by the coordinator:* the report read in full; the quoted lines of the theory report, of `r8_flat.py`, `cert3.py`, ENG-RES-0008 and ENG-RES-0014 re-read; six scripts re-run with output identical to the workstream's logs (the ladder comparison behind M1, the replication at `n = 4 000`, the validation, the 159-number comparison, the flat instance at `n = 4 000` with our engine and with theirs).  *Not checked by the coordinator:* the per-rung comparison; sizes above `4 000` beyond the stored logs; Steps 2–9 of the proof. |
| SCI-REV-0017 | theory report at `dd067f1`, Theorem 11.58a (the adaptive cost without a hint is `exp(n·h + O(√(n ln n)))`), with `Q_REPORT.md` and their referee's report — offered by the theory division (THY-RES-0015 §7), accepted in SCI-RES-0020 | workstream R17 (`workstreams/R17_REPORT.md`, with the coordinator's note; `experiments/science/ws_R17/`; the coordinator's check `experiments/science/r17_verification/`) | **published.**  **The theorem is proved as stated, given Theorem 11.56 with the abort test before every query**; no critical and no major finding; nine minor (an attribution; the prose on the slope step says more than the lemma; an `O(1)` that is `O_{u,δ}(1)` — 31 to 178 nats; `k_M − 1` levels, not `k_M`; a column head; the class of randomised algorithms; a check that samples base nodes — reproduced to five printed numbers).  *Review:* Lemma Q4, Propositions Q6, Q7, Theorems Q8, Q9 line by line against the contract C1–C8 of workstream R16; the lower bound (also by the coordinator, by hand).  *Replication:* formula (5.2) typed from the text alone (`0.7072, 0.3713, 0.2731, 0.2637`; no ambiguity resolved by reading their code); the exact nest with our cost code (`1568.21 / 1728.68 / 1969.97` at `n = 16 000`, theirs to the digit); 9 054 one-level checks with saturating families; **the outer loop of a slope step run for the first time (27 designs, 530 runs) and of a drop (6 designs, 64 runs): no violation of any claim of Theorem 11.56**; the lower bound on 19 136 cases (the coordinator: 2 844 with other code, least slack 0.684 nats, a control that fails).  *Re-run:* their `q1`–`q4` (the 25-minute full `q3` not).  *Not covered:* Theorem 11.56 itself beyond a re-reading; depth `M ≥ 5`; the literature inputs; Lean; prior art |
| — | our own `INFERENCE_LIMITS.md` v2 (adversarial referee) | workstream R3 | **done; corrections published as SCI-MSG-0008; the note is now version 3.**  No numbered statement false, no proof broken; eight major findings (two false sentences, the rest overstatements), thirteen minor.  Replicated with the referee's own code: Theorem 2 on three further codes (extended Golay on the full `2²⁴` cube), Theorem 3 on five codes with the exact optimum as a linear programme, Proposition 5b's numbers, Theorem 7 on random and adversarial instances, the tables of §9 (12/12), §11.1 (27/27), §11.2 (22/22), §11.4 (16/16), the engineering class tables for `n ≤ 9`.  Not re-run: the author's own scripts; the compact-decile row of §11.4.  The referee's own statements R1–R6 are **[P]**, unrefereed |
| SCI-REV-0018 | the engineering division's ENG-RES-0014 §1 (the classification rule of its mean-run evaluator of the theory division's nested algorithm) and §4 (a bound for instances that are not products), at `1cc4e1c` — offered by us, accepted by them | workstream R18 | **published.**  §1 proved as stated (a complete proof; 15.2 million literal decisions in exact arithmetic, 0 violations, eight controls failing); §4 proved at the level it is computed (mean runs, uniform inner behaviour, the range condition).  No critical finding; **one major: the conclusion "no such instance costs more than the worst product instance found" is false as worded — in every cell where their searched bound exceeds their product search, a product instance costs the bound by their own reference evaluator; the excess (up to `0.020·na`) is the shortfall of the first search**; ten minor.  Replicated with a literal loop and a mean run written from the statements (agreement with their reference on 2 700 runs and with their stored bound to `3·10⁻¹⁴`); re-run: two of their scripts where their Python reference fits in 2 GB.  Checked by the coordinator: the major finding in its largest cell with their evaluator (127.016745 against 125.373236), the rule check with another seed, the proof of the rule |
| SCI-REV-0019 | the Complexity division's `STRANDS_NN_HARDNESS.md` at `fc4b238`, Theorems 1 and 3 (minimum-free-energy folding of unboundedly many strands is strongly NP-hard in a nearest-neighbour model with exterior loops 0; counting is #P-hard) — asked for by them | workstream R20 | **published.**  Both theorems proved as stated (every step re-derived); no critical finding; two major — the gadget is a published one (Lyngsø 2004, in the form of Ducloz–Shalaby–Woods) and the note does not say so; "(H2) is the sign pattern of every physical parameter set" is false (a published rule set has a bulge of −0.13 kcal/mol), and a weaker hypothesis (H2\*) suffices with a five-line proof — and ten minor.  Replicated with an enumerator written before theirs was opened: 0 violations on 74 instances (19.5 million structures), every control violated (a stack across a nick rewarded: wrong on 23 of 32 non-solvable instances); their numbers equal ours on thirteen shared instances.  Re-run: their small test passes; their big test cannot finish within 2 GB.  Checked by the coordinator: the bulge rule at the source (a second reading of the database page), the proof under (H2\*), the enumerator's validation with another seed and the required control |
| SCI-REV-0020 | the Ensemble division's `ENSEMBLE_REPORT.md` at `a570520` (version 1), Theorems E5–E8, Corollary E1.3, §5 — asked for by them; compared with their version 2 at `1a067b5` | workstream R21 | **published.**  Proved as stated with their definition of generic; four major findings on reading and hypotheses (the free space; jointly generic — Examples D1, D2; no stability modulus; novelty classes), ten minor  *Review:* every step re-derived; the two cited theorems opened through a page fetch.  *Replication:* 549 908 splices on seven globally rigid planar graphs by an exhaustive method, no chimera; controls that must find one find it (160 of 160; 320 of 320).  *Re-run:* their `run_all.py` reproduces their output; one of their checks fails with 3 of 20 other seeds.  *Checked by the coordinator:* Examples D1 (exact) and D2 with own code, Propositions B and C re-derived, three gap computations with another seed (same orders; medians uncertain by a factor up to four) |
| SCI-REV-0021 | the Geometry division's `ENSEMBLE_RIGIDITY.md` at `d84a43b`, Lemma 2.2, Theorems B, B′, Corollary 4.2, Theorem G — asked for by them; reviewed sections compared with their head `e8e2582` | workstream R22 | **published.**  Proved as stated; three major findings (what the conic condition is, with a proposition for two differing torsions and its half-turn exception; Theorem G (c)–(d) as existence statements; Theorem B at `d = 1` is Laurent–Poljak 1996), seven minor  *Review:* every step re-derived.  *Replication:* the conic condition in exact rational arithmetic (22 of 22 cases); Theorem G's identities and exponents; linear images and linear programmes for states that share segments, by two routes.  *Re-run:* their harness (23 of 23; 11 of 11 mutations).  *Checked by the coordinator:* the two-hinge proposition with own code (`geometry_checks/two_hinges.py`: the eight images and no other zero in 6 of 6; both identities; the programme) |
| SCI-REV-0022 | the theory division's assumption audit at `fc3f5d9` (`docs/ASSUMPTION_AUDIT.md`, `docs/audit/AA1_REPORT.md`, `AA2_REPORT.md`) — promised by us | workstream R23 | **published.**  A sample of 32 of 513 tags by a rule fixed in advance: `{F}` 8 of 10, `{P}` 6 of 12 (two false when removed), `{Q}` 4 of 6, `{?}` 3 of 4; five major findings, nineteen minor  *Review:* the sampled entries against the theory report.  *Replication:* the three counterexamples of their §6 with independent code before theirs was opened; two sampled `{F}` rebuilt; a linear programme for the counterexample to a tag.  *Re-run:* all fifteen audit scripts, byte-identical.  *Checked by the coordinator:* the counterexample of F1 by hand, two proofs, one number, F1 and F4 against their text |
| — | our own addendum A17, parts (19)–(20) (the recovery of the band's slack; held-site passes; thirteen regression runs; Lys₂₀) and Part A of `ASSUMPTION_AUDIT.md` (adversarial referee) | workstream R19 | **done; corrections published as SCI-MSG-0030; the addendum has a part (21), the audit marks "[R19 …]" and a change table.**  No critical finding and no bracket in doubt; four major findings — a formula called a measurement (the loss between groups: measured 0.06 to 2.2 times `D²/4`, two thirds of the Lys₁₂ bracket at band 4), a wrong wording about ceilings, a proposition presented as general that excluded our own instance (terms with hosts), a growth comparison labelled as proved on a false premise — and fifteen minor.  Replicated with the referee's own code: the accounting as an identity to `10⁻⁹` kcal/mol at every state of four enumerated instances and 5 380 states of Lys₁₂; 65 670 held-site statistics on 3 000 random band models to `6·10⁻¹³`; the Lys₁₂ bracket at band 4 by a variable elimination without windows; Corollary AA.2 on 300 synthetic energies with three controls; level H2′.  Re-run: six of our logs, identical.  Checked by the coordinator: the loss measurement repeated with another seed (2.084 against 2.085); the audit tests re-run, identical |

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
| SCI-REV-0023 | the Geometry division's Theorem L, Corollary L.1, the `Θ(n²)` statement and Theorem K(a) (`LOCAL_DATA_STABILITY.md` at `288b2de`) | workstream A4 | published (checkpoint 62): 123 logged queries and addresses, 33 texts opened, the paper they cite read in full; classification statement by statement; **five deciding sources downloaded again by the coordinator — the checksums of the text extractions equal the agent's, and every quotation and formula taken from the passages read is there as quoted** (list in the coordinator's note of `A4_REPORT.md`); what was not reached is in its §5.2.  *Kind of check:* an originality review with full-text reading of public texts; no proof of the reviewed statements was read |

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
* **P5 (the compact case; before SCI-MSG-0024) — a recomputation with independent lines, not
  a re-run** (`experiments/science/pi_inference/p5_adoption_check.py`, 7 s).  (1) Ace-Leu₆-NMe on
  the helix, 64 states: the kernel matrices from workstream P3's table-free path
  (`energy_direct`'s formulas; the workstream used the tables; the two energies agree to
  `5·10⁻¹²` kcal/mol), the coordinator's own inclusion–exclusion for the anchored
  interpolation, and the coordinator's own sign search (1-flip ascent at every state, both
  signs, six starts; the twelve best candidates evaluated at all states).  True remainder
  `0.056866, 0.030119, 0.002221` and all-charges-positive `3.600712, 0.573930, 0.004578` kcal/mol at
  orders 3, 4, 5: the workstream's values to `10⁻⁹`.  **Sign patterns found here give
  remainders `8.6845, 0.6848, 0.0367` — the workstream's values — so every sign-blind bound
  exceeds the truth by at least 152.7, 22.7, 16.5**, and P3's `Γ_m` (131.7, 12.9, 0.776) bounds
  all of them.  (2) The Leu₁₂ helix certificate at order 6 with site penalties, rebuilt
  through workstream P6's `make_models`: `ln Z(m₋) = 374.5276673543`, `ln Z(m₊) = 374.2090967932`,
  exact `ln Z(E) = 374.345343432`, no violation of the sandwich at 4 096 states, cost number
  `0.200003` — identical to the workstream's run of P3's pipeline.  (3) `diff`:
  `ws_P5/floor_p3copy.py` is `ws_P3/run_floor.py` plus four lines.  Re-derived by hand:
  Proposition 7, Theorem 9 (i)–(iv), Propositions 10, 11 (one slip in the statement of
  Theorem 9(i), noted at the end of the report).  **Not checked by the coordinator:** the
  sign searches for Leu₈, Leu₁₂, serine; the family script; the locality and
  reference-term scripts; the certificates at 16, 20, 30 residues (the last two contain
  the coordinator's earlier fitted-chain values — a check of the value only).
* **P6 (pair and triple shares; before SCI-MSG-0025) — recomputations with independent
  lines, a re-run from a copy, and tests of the samplers.**  (1) `p6_adoption_check.py`
  (4 s): the chain `envelope ≤ triples ≤ triples in a window ≤ pairs ≤ banded pairs ≤ sites`
  on random non-negative constants, exhaustively over `{0,1}^n` (`n = 6 … 10`, orders 3–5):
  86 400 inequalities, no violation; the inclusion–exclusion formula and both
  double-counting identities.  The triple form on Ace-Val₈-NMe/PPII at order 4 with the
  coordinator's own inclusion–exclusion and brute-force models (inputs: P3's 70 constants,
  the enumerated energy): no state with `|remainder| > penalty`; widths 0.4235, 0.0704,
  0.0110 nats (site, pair, triple) against the workstream's 0.425, 0.0717, 0.0123 — a
  common difference of 0.0013–0.0015, the slack of P3's reduction of the evaluated
  three-site terms, which the coordinator's models do not have; the envelope alone
  0.0016.  (2) `certified_populations.py` (3 min; it rebuilds the workstream's models by
  calling its functions): **1 542 exact single-site populations inside their intervals**
  on ten enumerated instances (site, pair and triple sandwiches), the sandwich re-checked
  at every state, and the brackets `[518.255189, 518.271430]`, `[518.238327, 518.292897]`,
  `[518.258807, 518.267767]`, `[743.165709, 743.167411]` reproduced.  (3) **Re-run from a
  copy of the workstream's directory** (its own files untouched):
  `p6_09_triple.py V20 P2 0.70 --m 4 --bands 8 --noenum` and
  `p6_02_sandwich.py V20 P2 0.70 --m 4,5 --bands 8 --noenum` — identical digits (widths
  1.735567, 0.305644, 0.054570; 0.060494, 0.016241).  (4) The sampler: the 50 000 stored
  points against models rebuilt here (identical energies), `W` and the bracket
  `[518.262315, 518.262513]` recomputed, the site-state frequencies against the exact
  marginals of `q` (largest `|z| = 2.5`, rms 1.15); `sampler_precision_check.py` (25 s): at
  twelve residues against exact enumeration, the coordinator's chain sampler (four
  million samples: estimate off by `(+1.5 ± 1.8)·10⁻⁶`) and P3's band sampler with the
  rejection step on a banded model (six million proposals: acceptance rate `z = +0.5`,
  mean `W` `z = +0.3`, estimate off by `(+0.9 ± 3.4)·10⁻⁶`).  **Not checked by the
  coordinator:** thirty residues on PPII (triple form) and its sampled bracket; the
  extreme-member checks; the helix control; the sampler's coverage runs; the closed-form
  sums against explicit enumeration.  **Open at the level of two standard errors:** the
  coordinator's pooled chain estimate at twenty residues (`518.262430 ± 0.000006`, 684 000
  samples) against the sandwich sampler's point estimates (`518.262415 ± 0.000004`).

* **R13 (before SCI-REV-0014) — a re-derivation, two compilations and a recomputation.**
  `r13_adoption_check.py` (seconds; written from the statements): statement (a) of the
  rate re-derived on paper from the three Lean statements (every line agrees with the
  report); the constants at `u = 1` and the epoch recursion against the closed form in
  exact rationals to level `2·10⁵` (largest ratio `0.9591`); `RateCore.lean` and
  `RateFull.lean` compiled by the coordinator (`lake env lean`, exit 0, thirteen theorems
  on the three standard axioms; the three imported theory files byte-identical in our
  tree and at `63e36f7`); the counter-example to Proposition 11.117(b) recomputed in
  40-digit arithmetic (the report's table to every digit); m1, m3, m9 checked against
  the theory division's text and stored output.  **Not checked by the coordinator:**
  the one-sided recursion; the harness re-runs; the block recursions; the share
  instances; the first sizes.
* **P7 (before SCI-RES-0014) — an independent checker and brute force.**
  `p7_adoption_check.py` (seconds; written from the report's description of the format):
  all nine tree certificates accepted by a checker that shares no code with the
  workstream's; two controls rejected for each; the minimum of each published instance
  by brute force (0, at the reference only); the four gaps by an own linear programme
  (the report's numbers); Proposition P7.5 at four sites.  **Not checked by the
  coordinator:** the exact proofs of the gaps and failures; the survey; the triplet
  certificates; the thirteen `#eval` runs of the theory division's `verify`.

* **The coordinator's own addenda A17 (15), (16) (before SCI-MSG-0026) — what was checked,
  and by whom: by their author only.**  (1) `window_model_check.py` (40 s): the new model
  class against exhaustive enumeration on 189 sandwiches (serine, helix and strand,
  orders 3–5, three windows, three penalty forms, three rules for the terms that do not
  fit a window): model energies against a direct evaluation that shares no code with
  the class (`1.9·10⁻¹³` kcal/mol at every state), `m₋ ≤ E ≤ m₊` at every state, transfer
  matrix against the sum over states (`6·10⁻¹⁴`), the full window against the
  enumerated brackets of `serine_helix_shares.py` (`4·10⁻⁵` nats: the floating-point
  allowances); Lemma A17.16 exactly on 378 sandwiches; the two-window triple form on 11.
  (2) The driver `serine_helix_reach.py` against enumeration on Ser₆ (the brackets of
  A17 (15) in every digit) and on Leu₁₂ (the exact `ln Z` inside every bracket; P5's
  order-6 certificate and P6's order-5 pair-form number reproduced).  (3) At twelve
  residues, where nothing can be enumerated: the sandwich at 3 200 Gibbs states of the
  true ensemble, 4 000 exact samples of the floor and 2 000 states of the theory
  division's sampler per run — no violation in any run; two estimates inside every
  bracket; `P3`'s constants against the true remainder on seven small instances
  (`reach_side_checks.py`: `|remainder| ≤ Γ_m` at every state and order).  **Three
  wrong statements were caught by these checks before publication** (`DEAD_ENDS.md`
  SD50, SD51, and the "pointwise tighter" claim in item 41 of the addendum).  (4) **Lemma
  A17.16 machine-checked** by the coordinator (`pi_inference/lean/SandwichCost.lean`:
  `sandwich_cost`, `floor_side`, `ceiling_side`, `Z_ratio`; `lake env lean`, exit 0, the
  three standard axioms, no `sorry`; log next to the file).  **Not checked by anyone
  else:** everything but the lemma's proof — the validity of the allowances for the
  window models, the code, the runs, the reading.  A referee workstream (R14: proofs, an
  independent implementation, an attack on the sandwich by optimisation) was launched
  and terminated at once by a platform safeguard; it reviewed nothing and has not
  been replaced.  **These parts are unrefereed.**

* **Addendum A17 (17) (before SCI-RES-0017) — the theory division's nested sampler and
  allocation rule run by the coordinator: what was checked, and how.**  *Kind of check:*
  their two propositions are **used**, not reviewed, here (their review is workstream
  R15); the runs are a **replication on real instances** of statements they had tested
  on small synthetic ones.  (1) Sampler, `nested_sampler.py --enum`, two enumerated
  serine instances (17 496 and 104 976 states): both sandwiches at every state; the
  three identities of their Proposition 11.113a(a), (b) to `3·10⁻¹⁴`; the envelope three
  ways (a table of all constants, one closed form per changed set, workstream P3's
  per-subset routine) to `3·10⁻¹⁶` kcal/mol; coverage 100 of 100 for six kinds of
  bracket at three proposal budgets.  Beyond enumeration (twenty-residue valine,
  twelve-residue serine helix): no evaluated energy outside the inner sandwich in
  2 400 evaluations, clipping never active, the outer sandwich of SCI-MSG-0025
  reproduced (`[518.238327, 518.292897]`), the plain sampler's width of SCI-MSG-0025
  reproduced (`0.0043`), the point estimate of the serine helix equal to the
  uncertified estimate of A17 (16) to `8·10⁻⁶`.  The validation logs were produced
  again with the final script (identical numbers).  (2) Allocation,
  `allocation_core_test.py`, one enumerated instance (Leu₁₂ on the helix, 4 096
  states) at orders 3–6: supermodularity of `Γ` on all sets; every penalty vector used
  is in the core and covers the envelope at every state (asserted); the exact `ln Z`
  inside every bracket; the greedy vertex from `n + 1` closed-form sums against the
  direct assignment of every constant (`3·10⁻¹³` kcal/mol); the water-filling bound
  against a numerical optimiser on random instances and below the Frank–Wolfe
  optimum on the real one.  `site_allocation_fw.py` (transfer matrices) reproduces the
  site form of A17 (16) digit for digit on the same instance and its Frank–Wolfe
  bracket contains the exact value.  (3) `ScienceA17.greedy_optimal` **machine-checked**
  (`pi_inference/lean/CoreGreedy.lean`, exit 0, standard axioms).  (4) Sources: the
  empirical Bernstein inequality read in the ar5iv rendering of arXiv:0907.3740 by a
  fetch subagent (Theorem 4, one-sided, i.i.d. variables in `[0, 1]`); Shapley (1971),
  Wainwright–Jaakkola–Willsky (2002/2005) and Liu–Ihler (2011) confirmed
  bibliographically by web search, not opened; Edmonds (1970) and Ichiishi (1981) from
  memory.  **Not checked by anyone else:** the inner sandwich as built (the allowance
  `a(t)`, the treatment of ball states), the one-known-mean bound (workstream R15 is
  asked to check it), the convex-game reading, the code, the runs.  One instance per
  regime.  **Unrefereed.**

* **P8 (the charged case; before SCI-MSG-0027) and addendum A17 (18) — a review of the
  theorem, necessary conditions with independent code, and a re-run with another
  driver; the constants themselves were recomputed by nobody.**  *Kinds of check, kept
  apart.*  (1) **Review:** Theorem AH re-derived by the coordinator (the remainder
  identity for an arbitrary order of the sites; hosts last); its hypothesis sharpened
  to "at most `m` hosts"; Lemma T re-read against P3's Lemma 2 and Corollary L1.
  (2) **Own code, a family built to break the theorem**
  (`p8_verification/ah_synthetic_test.py`): exact restricted maxima on two grids;
  9 900 structured functions, `1.17·10⁶` (function, state) checks, no violation, ratio
  1 attained; three wrong versions of the statement all violated.  *The first version
  of this test used i.i.d. Gaussian tables only, on which eleven wrong versions are
  not violated* (`DEAD_ENDS.md` SD59).  (3) **Own code for the left side, P8's
  constants on the right** (`lys_enum_check.py`): `|g − I_{m−1}g| ≤ Σ_{T⊆S(x)} ĉ_T` at every
  state of Lys₄, Lys₅, LKSE:5, orders 3 to `n`, variants 'Sb' and 'SAb' — no violation.
  (4) **Another driver** (`lys12_rerun.py`): the nine certified brackets of P8's table
  T10 for Lys₁₂ to every printed digit; P8's per-subset decomposition of P3's closed
  form against closed-form sums over exclusion sets (`3·10⁻¹⁴`); the ball from P8's
  cache after a row-by-row comparison of its states and a re-evaluation of 3 000
  values; 4 250 uniformly random states with 4–12 side chains off the anchor — no
  violation.  The three logs were produced twice (the script changed one sentence in
  between): identical numbers.  (5) **Re-run** of P8's validation chain for Lys₄ in a
  scratch copy: five logs equal line by line, timings apart (one check ran on two
  charge systems instead of four).  (6) **A17 (18), the split around the anchor**
  (`window_model_occ.py`, `occ_reduction_test.py`): on Lys₅ at bands 2 and 3 the
  sandwich at all 115 248 states and the exact `ln Z` inside every bracket, for four
  reduction rules and three share forms; beyond enumeration the sandwich at 960 Gibbs
  states of a second sample (not the one that guides the rule) and 2 000 exact samples
  of each floor — no violation in any run.  (7) **The sampler on the charged peptides**
  (`nested_sampler_ext.py`): the driver validated end to end on Lys₅ (exact
  `ln Z = 251.348445` inside all six brackets); the cached floor sampler gives output
  identical to workstream P3's; no evaluated energy outside either sandwich in 13 279
  evaluations (19 + 60 + 1 200 + 12 000); two predictions written before the runs —
  one confirmed (Lys₁₂), one wrong by a factor four in the width and twelve in the
  envelope bracket ((LKSE)₃), a third confirmed ((LKSE)₃, second run).  **Not checked
  by anyone:** P8's implementation of the per-state ingredients (the constants);
  workstream P3's interval enclosures; §1, §2 and most tables of P8's report
  (read only); the (LKSE)₃ bracket of table T10 was reproduced by my test script
  (`[654.863818, 659.350547]`), not by the re-run driver.  **Unrefereed.**

* **P9 (penalties resolved by rotamer state; before SCI-MSG-0028) and addendum A17 (19) —
  a review of the statements, per-entry checks with independent code, a re-derivation
  of every bracket with another driver, a replication of one sampler run; the stage-2
  tables themselves were computed by nobody but P9.**  *Kinds of check, kept apart.*
  (1) **Review:** Lemma T′, Theorem R, Corollary J, Proposition P, Corollary S re-derived
  by the coordinator; no gap found.  (2) **Own code for the left side, P9's raw tables on
  the right** (`p9_verification/resolved_enum_check.py`, `resolved_check12.py`): every
  state of Lys₄, Lys₅, LKSE:5 at every order (`R ≤ B₂ ≤ B₁ ≤ B_SAb`, no violation); at
  twelve residues every state with exactly `m` side chains off the anchor against the
  exact anchored term — 92 525 and 1 524 690 states of Lys₁₂ (orders 3, 4), 175 185 and
  3 290 515 of (LKSE)₃ — no violation, smallest ratio 8.25–15.05, two controls that fail
  (14 334 – 1 853 296 and 438 – 170 176 violations); at order 5, 2 000 random states per
  peptide (necessary condition only: no ball of radius 5 exists).  (3) **Another
  driver, tables re-built from the raw ones** (`resolved_brackets.py`): the window-form
  tables and triple sums equal P9's stored ones exactly; "envelope ≤ tables" at
  32 000 – 40 000 random states per case with equality where the envelope is one entry,
  two wrong allocations fail; **twelve brackets (six cases, two forms) digit for
  digit**; produced twice (the model builder gained an optional output in between):
  identical.  (4) **The sandwich at 6 980 states of mine per case and form** — no
  violation; *its control:* with the tables left out it fails at 829–929, 18, 92 states
  (Lys₁₂ orders 3, 4; (LKSE)₃ order 4) and at none at order 5 or for serine; with tables
  ten times smaller never (`DEAD_ENDS.md` SD62) — the checks with teeth are (2) and (3).
  (5) **Replication of a sampler run** (`nested_resolved.py`, my driver, another seed):
  (LKSE)₃ from the order-4 ball `[655.612563, 655.612815]` / `[655.612658, 655.612720]`
  against P9's `[655.612562, 655.612814]` / `[655.612657, 655.612719]`; and one run P9 did
  not make (Lys₁₂ from the order-3 ball, predicted before).  (6) **A17 (19), the
  recovery** (`slack_recovery.py`, `first_order_recovery.py`): on Lys₅ (three order/band
  combinations) and LKSE:5 the two hypotheses at every state (margin exactly the
  constant allowance), two controls that fail at up to 229 329 states, the group means
  from the held-site passes against enumeration (`10⁻¹²`), the exact `ln Z` inside every
  corrected bracket; at twelve residues the hypotheses at 5 380 states per case with
  new energies (nine cases: no violation, both controls fail), the means against
  20 000 exact samples of the ceiling (within 1.6 standard errors; the Lys₁₂ rows share
  a seed), and every corrected bracket against the sampled interval of the same `ln Z`
  (contains it, or — Lys₁₂ at order 5 — overlaps it and is the narrower).  Four versions
  of the code; the logs of the first three are not kept (`DEAD_ENDS.md` SD64).  **Not
  checked by anyone:** P9's implementation of the stage-2 evaluation beyond (2); the
  stage-1 tables; the forms S and B; P3's interval enclosures; the evaluation
  tolerance `ε_g` of the solvent term (unproved for the evaluator: workstream P3's own
  statement).  **Unrefereed.**

### Checks of our statements made by other divisions (recorded here so that a reader finds them; none was repeated by us)

* **Inequality (c) of Proposition A17.23** (the second Bonferroni inequality for numbers in `[0, 1]`, addendum item 94) — **machine-checked by the theory division** at their commit `07cde81`: `proofs/Frontiers/Bonferroni.lean`, `MetricChain.Bonferroni.prod_one_sub_le`, with the first Bonferroni inequality and the sandwich (THY-MSG-0019 §2).  The step from it to the bound on the partition function — the identity `Z(m₋ + s₋) = Z(m₋)⟨Π_h(1 − c_h)⟩` and the averaging — is **not** formalised.  The file was not built or opened here.
* **The weak-coupling coefficient `F*` of SCI-RES-0033** — confirmed by the theory division by a brute-force capacity computation written from our statement (agreement `3·10⁻⁵` at five values of `u`; one sign change, at 1.505534; THY-MSG-0019 §2).
* **Finding F1 of SCI-REV-0022** (their Theorem 11.32 with a non-additive true residual) — replicated by the theory division by a linear programme over the whole class before they changed anything (THY-MSG-0019 §2).
* **Our reference checker's defect** (`ws_P7/p7_06_check.py`) — found by the engineering division, confirmed and corrected by us (§1.14); the Structural Biology division's intake noticed two descriptions of the nine certificate files — both are true: nine files, seven distinct certificates (the two Ser₆ files at clash threshold 0.70 are integer for integer those at 0.60; checked on 26 November by hashing the files without their labels).

## 3. Not validated by us

Everything not listed above.  In particular the paper proofs of theory report §§11.16–11.17,
11.20–11.21 and 11.23 (refereed by the theory division's own referees R5–R10) have not
been reviewed by this division; statements of ours that lean on them say so
(`docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`, "Dependencies").
