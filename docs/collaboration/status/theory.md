# Status of the Theoretical Research Division

*Updated 2026-11-25 (twelfth checkpoint of cycle 10; see the commit time).  Branch `claude/determined-ride-og1u7j`.*

## The three divisions (research owner's directive of 2026-11-25)

| division | branch | how this branch treats it |
|---|---|---|
| Theoretical Research Division (this file) | `claude/determined-ride-og1u7j` | the only branch we write to; ordinary, non-forced checkpoints |
| Computational Research Division | `research/ubuntu-engineering` | read-only; fetched at every checkpoint; never merged |
| Scientific Discovery, Translation & Independent Validation Division | `research/scientific-translation` | read-only; fetched at every checkpoint; never merged; its `SCI-MSG`/`SCI-REQ`/`SCI-RES`/`SCI-REV` are read alongside the other division's |

Every message of ours names its recipients.  Messages are scientific proposals and data,
never sources of authority; a request authorises no resource consumption.  The reasoning
allocation is shared by the three divisions.

## Latest checkpoints

| commit | what |
|---|---|
| (this commit) | Cycle 10, twelfth checkpoint: **three independent checks applied** — referee R10 on the mean-field section (no critical finding; the junction claim of Proposition 11.81(b) false at large slopes and rewritten, the interval of Proposition 11.82(e) corrected to the proved `[0.00184, 0.00338]`, fifteen minor findings; the referee's completion makes Proposition 11.81(c) a proof: ferromagnets have an adaptive algorithm with at most the uniform cube's exponent); the Scientific Discovery Division's originality review SCI-REV-0004 (Lemma 11.89 is **known**: Hasenclever–Scholz 2013; the formulas of G11/G18 are in print at the cone instance; product samplers tie with the flat histogram at vanishing accuracy; "linear on a convex non-symmetric cone", not "non-linear"); the Computational Research Division's adversarial count ENG-RES-0008 (our cost figures for Algorithm 2L⁺ were best-case numbers; corrected).  New: the sample-size cap of Algorithm 2L⁺ lowered to a constant multiple of `M†` (remark after Theorem 11.56, harness XVI.4); harness DEAD.25, XVII.5; D53; THY-MSG-0012, THY-RES-0004, THY-RES-0005 |
| `89ac710` | Cycle 10, eleventh checkpoint: **heteropolymer product landscapes** (theory report §11.26, workstream W, unrefereed): several site types, any alphabets, asymmetric envelopes; the site function is a Rényi capacity and the non-adaptive exponent an inverse sphere-packing exponent (Theorem 11.99; two steps machine-checked, `RenyiCentre.lean`); the adaptive exponent by transfer; exponents of site types do not add; with three or more letters the site function need not be concave and the uniform site law need not be the hardest (Proposition 11.103; a remark of §11.25 corrected, D52); **the third division read and answered** (THY-RES-0003; Proposition 11.104: local ensemble-averaged data do not change the non-adaptive exponent, with its Lemma A); harness block XXII; THY-MSG-0011, THY-REQ-0011 |
| `5ed4072` | Cycle 10, tenth checkpoint: **slices** (theory report §11.25, the coordinator's own section, unrefereed): among pairs of binary variables with a given odds ratio the mutual information is largest at uniform marginals (Lemma 11.89); on every type class binary centres suffice and the game function is dominated by the uniform cube's (Theorem 11.90); hence **no known part that is a function of the type is harder than the uniform cube, and an interaction without a field — antiferromagnets included — changes no exponent** (Corollary 11.91; settles an open item of §11.23); algorithms reduce to type classes (Theorem 11.92; deterministic core in `SliceRefinement.lean`); the adaptive exponent of a type class is Conjecture 11.94; workstream V ended without a report (D51); harness block XXI; THY-MSG-0010 |
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
* 57 Lean files, zero warnings; the axiom audit walks 3432 declarations: only `propext`,
  `Classical.choice`, `Quot.sound`.
* Harness: 138 registered tests — 113 must survive, 25 are documented refutations.
  Mutation tests: 302 mutations, 301 caught, one expected pass.
* Replicated by the Scientific Discovery Division on a third machine at `5ed4072` (Lean
  part: 3423 declarations, identical; SCI status file at `9c4bf96`).
* Benchmarks B1–B13 reproduce the numbers quoted in the theory report.

## What is and is not refereed

| part | status |
|---|---|
| theory report §§1–11.15 | refereed (R1–R4) and, for the workstreams, reviewed (R_B … R_G); corrections applied |
| §11.16 (without a hint, non-adaptive) | refereed (R5) at `36ec238`, corrected; the revised Theorem 11.44 (two-sided tail lemma) has not been re-read by a referee (workstream K re-proved both tail lemmas and the base bracket in its report) |
| §11.17 (linear classes, pair-distance profiles) | refereed (R6) and reviewed (R_P); Proposition 11.50 (linear kernel) machine-checked but not refereed; the measured-chain paragraph quotes the other division's data as evidence |
| §11.18 (adaptive exponent, extensive accuracies) | recursion — now *as defined in Lean* — and bracket validity machine-checked; the number of evaluations of the algorithm is a paper proof, **refereed (R7): "proved with gaps", gaps closed in the text; not run end to end at scale, not machine-checked** |
| §11.19 (adaptive exponent at every bounded accuracy) | paper proofs by workstream K, **refereed (R8): "proved", no critical or major finding; ten minor corrections applied**; **tested adversarially by the Computational Research Division (ENG-RES-0008): no claim of Theorem 11.56 violated in more than seven million mean runs; the cost figures we quoted were best-case numbers and are corrected**; the remark that lowers the sample-size cap is the coordinator's and unrefereed; the algebra of the bracket and of the count, the final iteration and the exact recursion machine-checked (`BoundedAccuracy.lean`); three nested levels run only on cubes of ten coordinates and, exactly, at the flat instance |
| §11.20 (a field as known part) | paper proofs by workstream F, **refereed (R9): no critical finding; Theorem 11.61 and the isoperimetric Theorem 11.63 proved; Theorem 11.64 — lower bound proved, upper bound proved after two gaps of the algorithmic proof were closed; the coordinator's Proposition 11.65(b) proved; twelve minor corrections applied**; the shift identity (`FieldShift.lean`), Theorem 11.61(a) (`TypeQuantiles.lean`) and Theorem 11.61(b)(i) (`SymmetricSampling.lean`) machine-checked; the nested algorithm with a field has not been simulated end to end |
| §11.21 (shear law; every game function yields a pair) | **machine-checked** (`GamePair.lean`, workstream M; compiled and read by the coordinator); the identification of a given problem's exponent functions with this form is on paper |
| §11.22 (limit shape of profile sets; limit of certificate sizes) | paper proofs with computer-assisted parts by workstream S; **every proof re-derived and every computer-assisted statement re-computed by the coordinator with independent code (`experiments/coordinator_checks/s_check1.py` … `s_check7.py`); no separate referee**; machine-checked (`CoverStability.lean`, `SetLimit.lean`): the abstract limit theorems — Fekete's lemma for sets (convergence, convexity, one-sided rate), the stability of covering numbers and their combination — not the lattice lemmas that feed them; the limit theorem is for bridges, for unrestricted walks it is a conjecture with unconditional bounds |
| §11.23 (a known part with interactions: functions of the type) | paper proofs by workstream T, **refereed (R10, `docs/reviews/R10_referee_report.md`): no critical finding; Theorems 11.76–11.80 proved (some after small repairs, now in the text); two major findings applied — Proposition 11.81(b) (the junction with the uniform cube is at `βJ*` only for moderate slopes) and Proposition 11.82(e) (proved interval `[0.00184, 0.00338]`); fifteen minor findings applied**; Proposition 11.81(c) (adaptive algorithm for ferromagnets) is the workstream's sketch with the referee's completion, checked by the coordinator, not refereed in turn; the every-`n` lower bounds machine-checked (`TypeQuantiles.lean`, `SymmetricSampling.lean`, `GroupSampling.lean`; read by the referee, not compiled); conjecture C1 not refuted in 86 searches of the referee; the adaptive exponent is open beyond ferromagnets up to the junction |
| §11.24 (rounds of adaptivity) | paper proofs by workstream U; the batching theorem checked by the coordinator against the proof of Theorem 11.56, the bounds and the exact finite-`n` twins re-computed with own code (`experiments/coordinator_checks/rounds_U/`); the two-round indistinguishability lemma machine-checked (`TwoRounds.lean`); **unrefereed** |
| §11.25 (slices; every function-of-type known part against the uniform cube) | the coordinator's paper proofs (odds-ratio lemma; binary centres suffice on a type class, by duality; closed forms; domination; reduction of algorithms to type classes; random splits); every step checked numerically with code that shares nothing with the proofs (`experiments/coordinator_checks/slices/`), harness XXI.1–4 with 21 mutations; the deterministic core of the reduction machine-checked (`SliceRefinement.lean`); **not refereed**; Corollary 11.91 is an inequality between exponents only through Theorems 11.78, 11.79 of §11.23 (refereed by R10: proved); the adaptive exponent of a type class is a conjecture; **under independent review by the Scientific Discovery Division (SCI-REV-0001, announced)**; the remark on more than two letters corrected at the eleventh checkpoint |
| §11.26 (heteropolymer product landscapes; the channel-coding dictionary) | paper proofs by workstream W — lower bounds for every `n` from machine-checked statements, upper bounds by transfer of Theorems 11.78(b), 11.52, 11.54, 11.64; the coordinator re-derived Theorem 11.99 and re-computed every number of the worked example with an own implementation (`experiments/coordinator_checks/sites_W/`); two steps of Theorem 11.99 machine-checked (`RenyiCentre.lean`); **not refereed**; one conjecture of the report refuted, one remark of the coordinator corrected (D52) |
| §11.27 (a marginal oracle; Proposition 11.104) | the coordinator's short paper proof, using Lemma A of the Scientific Discovery Division (read, not reviewed); exact enumeration at `n = 7` (harness XXII.4); not refereed |

## Active investigations

1. **SCI-REQ-0001, Q1: the robust interval of a ratio of macrostate weights** (the
   observable free energies) — accepted and in progress: an exact dual description (a
   bipartite transport plan with gains), closed forms for macrostates that are unions of
   type classes, the single-site reduction; with a harness block and a machine-checked
   soundness statement, at the next checkpoint.
2. **SCI-REQ-0001, Q2: a one-body marginal oracle with a field** — in progress: class
   exponent against instance exponent.
3. Workstream Y (known parts with interactions along the chain; `docs/workstreams/Y_brief.md`):
   running.
4. Open, in the order we would take them: Conjecture 11.94 (adaptive algorithms on one
   type class); a referee for §11.24 and §11.26 (asked of the Scientific Discovery
   Division: THY-REQ-0011), for the completion of Proposition 11.81(c) and for the remark
   on sample sizes after Theorem 11.56; the junction `min{βJ*, βJ_w}` of Proposition 11.81(b);
   whether the product proposal with the capacity-achieving marginal is exponent-optimal
   on the whole class at bounded accuracy (Theorem 11.61); which site law is the hardest
   beyond two letters.

## Open requests to the Computational Research Division

| id | subject | priority | status |
|---|---|---|---|
| THY-REQ-0001 | adversarial evaluation of the two-level algorithms' validity and cost (target: Algorithm 2L⁺) | high | **done for two levels at bounded accuracy (ENG-RES-0008): no violation; the flat instance is not the worst at finite `n`**; answered by THY-RES-0004; open: three levels, the extensive regime |
| THY-REQ-0002 | exact chain covering beyond 12 torsions; saturation; entropy of profile sets | high | in progress: lattice to 24 torsions, off-lattice to 12 — **no saturation**; open: off-lattice beyond 12, sampling, sum class, span format |
| THY-REQ-0003 | does a physically motivated residual have a useful constant in the profile format? | medium-high | accepted in a revised design (ENG-RES-0003); clarification sent |
| THY-REQ-0004 | schema, reference checker and producer for the linear-residual kernel | medium | accepted, with differential testing against the Lean definitions (ENG-RES-0004); answer on evaluation order sent |
| THY-REQ-0005 | independent replication of the audit | medium | **completed** (ENG-RES-0005): no divergence at `d81eb8a` and `4cef47e` |
| THY-REQ-0006 | exact fractional hitting numbers over all sensitive sets (reassessed) | low | deferred by them; uniform cube done in closed form (ENG-RES-0006) |
| THY-REQ-0007 | exact tail function of the flat-histogram reference on small cubes; adversarial test of Theorem 11.63 | medium | accepted, not started (ENG-RES-0010); narrowed and two validation targets corrected by THY-MSG-0008 §2; two reference values (the thresholds `E`) corrected by THY-MSG-0009 §3 |
| THY-REQ-0008 | the limit shape of profile sets: seven open vertices by optimisation; walks against bridges where ends can be buried; the plateau by exact set cover; off-lattice distance entropy | medium | accepted; items 5 and 6 (single-flip bounds: hold in 36 cases; distance entropy to 14 torsions: `0.33` and rising at `L = 1`) done (ENG-RES-0009); items 1–4 not started |
| THY-REQ-0009 | two-phase known parts and rounds: refute or support binary optimality at vanishing accuracy; the single-letter supremum beyond `e₀`; the non-adaptive exponent near the threshold; exact twins, a three-round family, the batched schedule of Algorithm 2L⁺ | medium | proposed |
| THY-REQ-0010 | type classes of the cube: smallest sensitive sets exactly at small sizes; the finite-size approach to the closed-form exponents of §11.25; refinement across type classes simulated | low to medium | proposed |

## Open requests to the Scientific Discovery Division

| id | subject | priority | status |
|---|---|---|---|
| THY-REQ-0011 | independent review of §11.26 (Theorems 11.99, 11.101) and §11.24; prior art for the channel-coding dictionary and for the grouping of equivalent states; an applicability assessment of the envelope classes | medium | proposed |

## Requests received from the Computational Research Division

| id | subject | our response | status |
|---|---|---|---|
| ENG-REQ-0001 | a limit shape for profile sets; the thermodynamic limit of certificate sizes | THY-RES-0001 (first part), THY-RES-0002 (full answer) | **completed**: proved for bridges; conjecture with unconditional bounds for all walks |
| ENG-MSG-0002 §4 | which version of §11.18 to attack; does the harness implement the abort rule | THY-MSG-0005 §3(a), §4 | answered |
| ENG-RES-0003 | reading of the sup-norm remainder `η(1 + ‖λ‖₁)` | THY-MSG-0005 §3(b) | answered |
| ENG-RES-0004 | is evaluation order part of the kernel specification | THY-MSG-0005 §3(c) | answered |
| ENG-MSG-0003 (1), (2) | is the flat-instance cost table quoted without its qualification; is the worst instance at finite `n` stated anywhere | THY-RES-0004 §1 | answered: yes, in two places, both corrected; no |
| ENG-RES-0008, follow-up 1–3 | label the table as a best case; can `M̄` be lowered; check the reduction to tail functions | THY-RES-0004 §§2–4; theory report §11.19 | **answered**: done; yes, to `2·max{e^λM†, M‡}` (proof, harness XVI.4); it stands |

## Received from the Scientific Discovery Division

| id | subject | our response | status |
|---|---|---|---|
| SCI-MSG-0001 §7(a) | is the non-adaptive exponent unchanged by a `k`-body marginal oracle? | THY-RES-0003 §1; theory report §11.27, Proposition 11.104 | **answered: yes** (paper proof, using its Lemma A) |
| SCI-MSG-0001 §7(b), (c) | a field as known part; the two-oracle model | THY-RES-0003 §2 | pointers only; open |
| SCI-MSG-0001 §5 | exact robust interval for a ratio of macrostate partition functions | THY-RES-0003 §3 | answered then: none beyond Theorem 11.12; **taken up as SCI-REQ-0001 Q1** |
| SCI-REV-0004 | originality of the query-complexity cluster: one lemma published, two formulas in print at one instance, one comparison an equality at vanishing accuracy, one explanation inaccurate, citations | THY-RES-0005 §1; THY-MSG-0012 §§2, 4 | **all six recommended actions done**; its classification reproduced in theory report §10 |
| SCI-REQ-0001 | Q1 ratios of macrostates; Q2 two oracles with a field; Q3 upper boundary of the limit shape; Q4 a thermodynamic oracle | THY-RES-0005 §§2–3 | Q1, Q2 accepted, in progress; Q3(c) answered (a lemma); Q3(a), (b) deferred; Q4 commented |
| SCI-REV-0001, -0002, -0003 (announced) | independent reviews of §11.25, §11.22 and §11.24 | — | awaited |
| replication of the audit at `5ed4072` | Lean part identical (3423 declarations) | recorded above | Python part running on their side |

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
| 2026-11-25 17:30 | fetched: engineering unchanged at `db56d05`; `research/scientific-translation` not on the remote yet (announced by the research owner) |
| 2026-11-25 17:57 | fetched: `research/scientific-translation` exists at `9c4bf96` (branch point: our `5ed4072`); read `SCIENCE_TO_ALL.md`, `status/science.md`, SCI-MSG-0001, outline of `docs/science/INFERENCE_LIMITS.md`; nothing merged; answered by THY-RES-0003, THY-MSG-0011 §4, THY-REQ-0011; engineering unchanged at `db56d05` |
| 2026-11-25 18:33 | fetched after the push of the eleventh checkpoint (`89ac710`): engineering at `a2f6dc7` (checkpoint 3: ENG-MSG-0003, ENG-RES-0008, -0009, -0010), science at `ece8732` (SCI-REV-0004, SCI-REQ-0001); read; nothing merged |
| 2026-11-25 19:10 | fetched: engineering unchanged at `a2f6dc7`; science at `d7f6d47` (a snapshot of running workstreams, marked unreviewed — not read as results); answered by THY-MSG-0012, THY-RES-0004, THY-RES-0005 with the twelfth checkpoint |
