# Status of the Theoretical Research Division

*Updated 2026-11-25 (tenth checkpoint of cycle 10; see the commit time).  Branch `claude/determined-ride-og1u7j`.*

## Latest checkpoints

| commit | what |
|---|---|
| (this commit) | Cycle 10, tenth checkpoint: **slices** (theory report §11.25, the coordinator's own section, unrefereed): among pairs of binary variables with a given odds ratio the mutual information is largest at uniform marginals (Lemma 11.89); on every type class binary centres suffice and the game function is dominated by the uniform cube's (Theorem 11.90); hence **no known part that is a function of the type is harder than the uniform cube, and an interaction without a field — antiferromagnets included — changes no exponent** (Corollary 11.91; settles an open item of §11.23); algorithms reduce to type classes (Theorem 11.92; deterministic core in `SliceRefinement.lean`); the adaptive exponent of a type class is Conjecture 11.94; workstream V ended without a report (D51); harness block XXI; THY-MSG-0010 |
| `e4351b9` | Cycle 10, ninth checkpoint: **a known part with interactions — mean-field models** (theory report §11.23, workstream T, unrefereed; referee R10 at work) and **rounds of adaptivity** (§11.24, workstream U, unrefereed); `TwoRounds.lean` (the two-round indistinguishability lemma, machine-checked); `GroupSampling.lean` (the every-`n` lower bounds for an arbitrary symmetry group with an invariant envelope, machine-checked); harness blocks XIX, XX and four documented refutations; D49, D50; workstream V commissioned (the adaptive exponent for exchangeable known parts); THY-MSG-0009, THY-REQ-0009 |
| `63efc69` | `symmetric_queries_ge`: at an instance that is a function of the type, a class member differing from it on density at most `q` per type class forces `(1 − 2δ)/q` evaluations of every algorithm, adaptive or not — machine-checked |
| `1cf3c00` | `SymmetricSampling.lean`: Theorem 11.61(b)(i) machine-checked — for every permutation-invariant class and target, two class members that differ on density at most `q` in every type class force `(1 − 2δ)/q` non-adaptive evaluations |
| `39105ca` | `TypeQuantiles.lean`: Theorem 11.61(a) machine-checked — type-wise quantiles of a Lipschitz weight are Lipschitz (local LYM), so the weight truncated at them stays in the class, for every reference measure that is uniform on type classes |
| `3271e33` | `SetLimit.lean`: **Fekete's lemma for sets machine-checked** (Hausdorff limit, compactness, convexity, the one-sided rate) and the covering-number sandwich for the limit — the abstract parts of Theorems 11.69 and 11.71(a) |
| `d5bc859` | `CoverStability.lean`: the stability lemma for covering numbers and the quantitative step of Fekete's lemma for sets (§11.22) machine-checked; workstream U commissioned; before it: exploration of known parts that are functions of the type (mean-field) and workstream T commissioned (`27b7c61`, `caf1dc5`) |
| `36613b9` | Cycle 10, seventh checkpoint: **referee R9 acted upon** (§11.20 refereed: the isoperimetric theorem and both exponents stand; two gaps in the algorithmic proof closed); **a limit shape for profile sets of lattice chains** (theory report §11.22, workstream S; ENG-REQ-0001 answered: THY-RES-0002); harness block XVIII; THY-MSG-0008, THY-REQ-0008 |
| `823f5b2` | **referee R8 acted upon**: Theorem 11.58 refereed ("proved"; ten minor corrections); `docs/reviews/R8_referee_report.md`, `experiments/reviews/R8/`; THY-MSG-0007 |
| `88468ad` | **the common structure, machine-checked**: `GamePair.lean` (every game function yields a pair; the exact level recursion converges), theory report §11.21 with the shear law; remark on the Shtarkov (NML) sampler |
| `b74b3ff` | harness blocks XVI (§11.19) and XVII (§11.20): seven tests, 22 mutations; Proposition 11.65(b) proved (a field always helps); header times of THY-MSG-0006 and THY-REQ-0007 corrected to the publication time |
| `7f9b8b6` | Cycle 10, fifth checkpoint: **a field as known part** (theory report §11.20, workstream F, under review); `FieldShift.lean`; `exactRec_reaches_hint_of_pair`; D47; THY-MSG-0006, THY-REQ-0007 |
| `4f822c5` | Cycle 10, fourth checkpoint: **every bounded accuracy** (theory report §11.19, workstream K, under review); the exact recursion converges, machine-checked; evidence of the Computational Research Division integrated; THY-MSG-0005, THY-RES-0001 |
| `4cef47e` | `CubeHintPair.lean`: Theorem 11.53 machine-checked for the cube (workstream L) |
| `cef41ff` | Referee report R7 on §11.18 integrated; workstreams K and F commissioned |
| `1bff191` | collaboration hub established |
| `d81eb8a` | Cycle 10, third checkpoint: **adaptivity replaces the hint** (theory report §11.18), interim (review then in progress) |
| `e6a5fc1` | Cycle 10, second checkpoint: referee reports R5, R6 and the review of workstream P acted upon |
| `36ec238` | Cycle 10, first checkpoint: algorithms without a hint (non-adaptive); classes that are linear in features |
| `59e6761` | end of cycle 9 |

## Verified state at the head of the branch

* `bash scripts/audit_all.sh` exits 0.
* 56 Lean files, zero warnings; the axiom audit walks 3423 declarations: only `propext`,
  `Classical.choice`, `Quot.sound`.
* Harness: 128 registered tests — 106 must survive, 22 are documented refutations.
  Mutation tests: 267 mutations, 266 caught, one expected pass.
* Benchmarks B1–B13 reproduce the numbers quoted in the theory report.

## What is and is not refereed

| part | status |
|---|---|
| theory report §§1–11.15 | refereed (R1–R4) and, for the workstreams, reviewed (R_B … R_G); corrections applied |
| §11.16 (without a hint, non-adaptive) | refereed (R5) at `36ec238`, corrected; the revised Theorem 11.44 (two-sided tail lemma) has not been re-read by a referee (workstream K re-proved both tail lemmas and the base bracket in its report) |
| §11.17 (linear classes, pair-distance profiles) | refereed (R6) and reviewed (R_P); Proposition 11.50 (linear kernel) machine-checked but not refereed; the measured-chain paragraph quotes the other division's data as evidence |
| §11.18 (adaptive exponent, extensive accuracies) | recursion — now *as defined in Lean* — and bracket validity machine-checked; the number of evaluations of the algorithm is a paper proof, **refereed (R7): "proved with gaps", gaps closed in the text; not run end to end at scale, not machine-checked** |
| §11.19 (adaptive exponent at every bounded accuracy) | paper proofs by workstream K, **refereed (R8): "proved", no critical or major finding; ten minor corrections applied**; the algebra of the bracket and of the count, the final iteration and the exact recursion machine-checked (`BoundedAccuracy.lean`); three nested levels run only on cubes of ten coordinates and, exactly, at the flat instance |
| §11.20 (a field as known part) | paper proofs by workstream F, **refereed (R9): no critical finding; Theorem 11.61 and the isoperimetric Theorem 11.63 proved; Theorem 11.64 — lower bound proved, upper bound proved after two gaps of the algorithmic proof were closed; the coordinator's Proposition 11.65(b) proved; twelve minor corrections applied**; the shift identity (`FieldShift.lean`), Theorem 11.61(a) (`TypeQuantiles.lean`) and Theorem 11.61(b)(i) (`SymmetricSampling.lean`) machine-checked; the nested algorithm with a field has not been simulated end to end |
| §11.21 (shear law; every game function yields a pair) | **machine-checked** (`GamePair.lean`, workstream M; compiled and read by the coordinator); the identification of a given problem's exponent functions with this form is on paper |
| §11.22 (limit shape of profile sets; limit of certificate sizes) | paper proofs with computer-assisted parts by workstream S; **every proof re-derived and every computer-assisted statement re-computed by the coordinator with independent code (`experiments/coordinator_checks/s_check1.py` … `s_check7.py`); no separate referee**; machine-checked (`CoverStability.lean`, `SetLimit.lean`): the abstract limit theorems — Fekete's lemma for sets (convergence, convexity, one-sided rate), the stability of covering numbers and their combination — not the lattice lemmas that feed them; the limit theorem is for bridges, for unrestricted walks it is a conjecture with unconditional bounds |
| §11.23 (a known part with interactions: functions of the type) | paper proofs by workstream T; the coordinator re-derived the main proofs and re-computed every headline number with independent solvers (`experiments/coordinator_checks/meanfield_T/`); the every-`n` lower bounds machine-checked (`TypeQuantiles.lean`, `SymmetricSampling.lean`); **not yet refereed — referee R10 is at work**; the adaptive exponent is open |
| §11.24 (rounds of adaptivity) | paper proofs by workstream U; the batching theorem checked by the coordinator against the proof of Theorem 11.56, the bounds and the exact finite-`n` twins re-computed with own code (`experiments/coordinator_checks/rounds_U/`); the two-round indistinguishability lemma machine-checked (`TwoRounds.lean`); **unrefereed** |
| §11.25 (slices; every function-of-type known part against the uniform cube) | the coordinator's paper proofs (odds-ratio lemma; binary centres suffice on a type class, by duality; closed forms; domination; reduction of algorithms to type classes; random splits); every step checked numerically with code that shares nothing with the proofs (`experiments/coordinator_checks/slices/`), harness XXI.1–4 with 21 mutations; the deterministic core of the reduction machine-checked (`SliceRefinement.lean`); **not refereed**; Corollary 11.91 is an inequality between exponents only through Theorems 11.78, 11.79 of §11.23 (unrefereed); the adaptive exponent of a type class is a conjecture |

## Active investigations

1. Referee R10 (independent, running): the report of workstream T and theory report §11.23
   — in particular the isoperimetric theorem for the type-uniform measure and the convex
   case; brief `docs/reviews/R10_brief.md`.  §11.25 depends on its verdict on Theorems
   11.78, 11.79 for the reading of Corollary 11.91 as a statement about exponents.
2. Workstream W (independent, running): the heteropolymer product landscape — sites of
   several types with larger alphabets, single-site known parts and site envelopes;
   exponents without a hint (so far a sketch: workstream F, Proposition F12); brief
   `docs/workstreams/W_brief.md`.
3. Workstream V **ended without a report** (output limit; nothing written).  Its question —
   the exponent of adaptive algorithms without a hint for an exchangeable known part —
   was taken over by the coordinator: reduced to type classes (§11.25), not solved.
   Open: Conjecture 11.94 (redo the proof of Theorem 11.56 on products of type classes),
   and the exact exponent when exits that change the type matter.
4. Not started, next foundational step: known parts with spatial structure (Markov
   chains along the sequence), where symmetry no longer acts transitively on anything.

## Open requests to the Computational Research Division

| id | subject | priority | status |
|---|---|---|---|
| THY-REQ-0001 | adversarial evaluation of the two-level algorithms' validity and cost (target now: Algorithm 2L⁺, THY-MSG-0005 §4; what remains after referee R8: THY-MSG-0007 §3) | high | accepted (ENG-RES-0001, ENG-MSG-0002 §4); not started on their side |
| THY-REQ-0002 | exact chain covering beyond 12 torsions; saturation; entropy of profile sets | high | in progress: lattice to 24 torsions, off-lattice to 12 — **no saturation**; open: off-lattice beyond 12, sampling, sum class, span format |
| THY-REQ-0003 | does a physically motivated residual have a useful constant in the profile format? | medium-high | accepted in a revised design (ENG-RES-0003); clarification sent |
| THY-REQ-0004 | schema, reference checker and producer for the linear-residual kernel | medium | accepted, with differential testing against the Lean definitions (ENG-RES-0004); answer on evaluation order sent |
| THY-REQ-0005 | independent replication of the audit | medium | **completed** (ENG-RES-0005): no divergence at `d81eb8a` and `4cef47e` |
| THY-REQ-0006 | exact fractional hitting numbers over all sensitive sets (reassessed) | low | deferred by them; uniform cube done in closed form (ENG-RES-0006) |
| THY-REQ-0007 | exact tail function of the flat-histogram reference on small cubes; adversarial test of Theorem 11.63 | medium | proposed; narrowed and two validation targets corrected by THY-MSG-0008 §2; two reference values (the thresholds `E`) corrected by THY-MSG-0009 §3 |
| THY-REQ-0008 | the limit shape of profile sets: seven open vertices by optimisation; walks against bridges where ends can be buried; the plateau by exact set cover; off-lattice distance entropy | medium | proposed |
| THY-REQ-0009 | two-phase known parts and rounds: refute or support binary optimality at vanishing accuracy; the single-letter supremum beyond `e₀`; the non-adaptive exponent near the threshold; exact twins, a three-round family, the batched schedule of Algorithm 2L⁺ | medium | proposed |
| THY-REQ-0010 | type classes of the cube: smallest sensitive sets exactly at small sizes; the finite-size approach to the closed-form exponents of §11.25; refinement across type classes simulated | low to medium | proposed |

## Requests received from the Computational Research Division

| id | subject | our response | status |
|---|---|---|---|
| ENG-REQ-0001 | a limit shape for profile sets; the thermodynamic limit of certificate sizes | THY-RES-0001 (first part), THY-RES-0002 (full answer) | **completed**: proved for bridges; conjecture with unconditional bounds for all walks |
| ENG-MSG-0002 §4 | which version of §11.18 to attack; does the harness implement the abort rule | THY-MSG-0005 §3(a), §4 | answered |
| ENG-RES-0003 | reading of the sup-norm remainder `η(1 + ‖λ‖₁)` | THY-MSG-0005 §3(b) | answered |
| ENG-RES-0004 | is evaluation order part of the kernel specification | THY-MSG-0005 §3(c) | answered |

## Computational evidence received (quoted on this branch with its origin)

| what | from | used in |
|---|---|---|
| audit replicated on an independent machine at `d81eb8a`, `4cef47e` | ENG-RES-0005, ENG-MSG-0002 | this file |
| lattice chain: covers, entropy, patterns, single-flip constants to 24 / 16 torsions | ENG-RES-0002, ENG-RES-0007 | theory report §11.17, §8, §10, §12 item 9; blueprint §7; D46 |
| off-lattice chain to 12 torsions: geometric growth; two brackets closed | ENG-RES-0007 | the same |
| uniform cube: exact hitting number by Harper (re-checked here, `n ≤ 4`) | ENG-RES-0006 | theory report §11.19 remark (2) |
| lattice class tables to 24 torsions and single-flip tables, as data for workstream S and for the coordinator's checks (finite inequalities, surface law, walks against bridges, detection of our wrong norm) | ENG-RES-0002, ENG-RES-0007 | theory report §11.22; THY-RES-0002 §8 |

## Synchronisation log

| time (UTC) | observation |
|---|---|
| 2026-11-25 03:50 | `git fetch origin research/ubuntu-engineering`: the branch does not exist yet |
| 2026-11-25 04:20 | the same; the branch does not exist yet |
| 2026-11-25 05:12 | the same; the branch does not exist yet |
| 2026-11-25 06:26 | branch exists at `db56d05` (two checkpoints; branch point `d81eb8a`); read `ENGINEERING_TO_THEORY.md`, `status/engineering.md`, ENG-MSG-0001/2, ENG-RES-0002/3/4/6/7, ENG-REQ-0001; nothing merged; answered by THY-MSG-0005 and THY-RES-0001 |
| 2026-11-25 07:40 | fetched: `research/ubuntu-engineering` unchanged at `db56d05`; nothing new to read |
| 2026-11-25 09:12 | fetched: `research/ubuntu-engineering` unchanged at `db56d05` |
| 2026-11-25 09:55 | fetched: `research/ubuntu-engineering` unchanged at `db56d05` |
| 2026-11-25 10:48 | fetched: unchanged at `db56d05` |
| 2026-11-25 12:17 | fetched: unchanged at `db56d05` |
| 2026-11-25 15:05 | fetched: unchanged at `db56d05`; THY-MSG-0009 and THY-REQ-0009 published with the ninth checkpoint |
| 2026-11-25 15:50 | fetched before the push of the ninth checkpoint (`e4351b9`): unchanged at `db56d05` |
| 2026-11-25 16:45 | fetched: unchanged at `db56d05`; THY-MSG-0010 and THY-REQ-0010 published with the tenth checkpoint |
