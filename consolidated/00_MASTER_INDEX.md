# MetricChain — unified research archive: master index

*Assembled on 2026-11-27 by the Computational Research Division (engineering) as a bounded administrative
task of the research owner.  This index and the files under `09_…`, `10_…`, `11_…` were written for the
archive; **everything under `01_…` – `08_…` (except each `00_DIVISION_INDEX.md`) is a byte-for-byte copy
of a division's own files at a pinned commit.**  Nothing was edited, redacted, merged or re-derived.*

**Status of this version.**
<!-- GEN:status -->
INTERIM (built 2026-11-27): two bounded Modal runs of the engineering division (compute-ledger jobs M-016 and M-021) were still running when this version was built, and their results are not in it.  The engineering section is refreshed once after they have been collected; the other seven divisions are pinned at the heads they pushed under the consolidation directive.
<!-- /GEN:status -->

**Read this before anything else.**

* Every document in this archive was written by AI sessions.  "Reviewed" means reviewed by another AI
  session — a subagent of the same division or another division of the programme.  **No statement here
  has been read by an external human expert, and none has been compared with an experiment.**
* The assessments quoted below are the divisions' *own* (their consolidation reports, sections A–G).
  This index locates them; it does not re-assess, rank across divisions, or reconcile.  Where two
  divisions disagree, or one never read the other's last message, §9 says so and leaves it open.
* No new mathematical synthesis was attempted here.  §10 and §11 list only connections that some
  division already wrote down.
* "Originality" in every division's report means *not found in a bounded search by AI sessions*,
  mostly at the level of abstracts.  Several claims of novelty were withdrawn during the programme (§6).

## 0. Orientation

### 0.1 The eight divisions and their pinned commits

Repository: <https://github.com/Tommaso-R-Marena/MetricChain>.  Each division worked on one branch;
the commit below is the head of that branch when the archive was built.

<!-- GEN:pins -->
| # | division | branch | pinned commit | commit date (UTC) | merge-base with theory | files | MiB |
|---|---|---|---|---|---|---:|---:|
| 01 | Theoretical Research Division | `claude/determined-ride-og1u7j` | `b3c5d6115df06bb160d6490a95d9ec6e1a108d02` | 2026-11-27 01:26:54 | — | 1864 | 18.46 |
| 02 | Computational Research Division (engineering) | `research/ubuntu-engineering` | `846e58caab20daac26c4da9b02c3093916d5adfc` | 2026-11-27 01:27:57 | `d81eb8aba138` | 719 | 36.68 |
| 03 | Scientific Discovery, Translation & Independent Validation Division | `research/scientific-translation` | `340081afba8841a4093b3df9b18387e8a36f20b1` | 2026-11-27 01:17:37 | `5ed407282d89` | 4281 | 60.43 |
| 04 | Ensemble Identifiability and Certified Inference Division | `research/ensemble-identifiability` | `a089a0ce2427c7f3797b838837d16659c8b0a1e4` | 2026-11-27 01:24:04 | `a844b5a8f374` | 181 | 2.20 |
| 05 | Geometric Inference, Rigidity and Inverse Problems Division | `research/geometric-inference` | `229527e37bbd53428f31718339b7ceb61bc1e942` | 2026-11-27 01:08:57 | `a844b5a8f374` | 189 | 1.88 |
| 06 | Mathematical Biology and Computational Complexity Division | `research/biological-complexity` | `4a09627d3560dc86cf162bce6c93f030ae84efb9` | 2026-11-27 01:27:10 | `a844b5a8f374` | 437 | 2.95 |
| 07 | Structural & Computational Biology, Software Development and Applications Division | `research/structural-biology` | `a5cc106dd59d984237dff483716360cae5306538` | 2026-11-27 02:49:58 | `b2caab689155` | 127 | 9.58 |
| 08 | Frontier Benchmarking, Experimental Evidence and Scientific Evaluation Division | `research/frontier-benchmarks` | `14254f33bee9cc33f7e015f5ec5c58976f7efcb5` | 2026-11-27 01:25:04 | `b2caab689155` | 98 | 1.15 |
| | **all eight** | | | | | **7896** | **133.32** |
<!-- /GEN:pins -->

<!-- GEN:totals -->
7896 files (133.32 MiB) imported from the eight branches; 3 files (24.74 MiB) left out by reference; heads pinned at 2026-11-27T04:58:54Z.
<!-- /GEN:totals -->
All divisions share one history (root `897242c`, 2026-11-24); every branch other than theory forked from
the theory branch at the merge-base shown, so its tree also contains an older copy of the theory files.
The archive copies those only once, from the theory head (`11_reproducibility/README.md` §2).

### 0.2 Layout

| directory | content |
|---|---|
| [`01_theory/`](01_theory/00_DIVISION_INDEX.md) … [`08_frontier_benchmarking/`](08_frontier_benchmarking/00_DIVISION_INDEX.md) | one directory per division: its files at their original repository paths, plus a generated `00_DIVISION_INDEX.md` (provenance, every document with its title, Lean files, code and result directories, what was left out) |
| [`09_cross_divisional_dependencies/`](09_cross_divisional_dependencies/README.md) | documented relationships between the divisions; index of all mailbox items with dates and titles; who cites whom; open disagreements |
| [`10_benchmark_status/`](10_benchmark_status/README.md) | completed, negative, running, frozen and proposed benchmarks; compute and Modal record; everything unfinished or unreviewed |
| [`11_reproducibility/`](11_reproducibility/README.md) | how the archive was built and how to verify it; pinned commits; excluded artifacts with retrieval instructions; Lean files; the build, verification and scan scripts |
| [`MANIFEST.json`](MANIFEST.json) | one record per artifact: original path, branch, pinned commit, last-change commit, git object id, SHA-256, size, class, evidence class |

### 0.3 How evidence is labelled

The divisions label statements inside their documents; the common labels are **[V]** machine-checked in
Lean, **[P]** paper proof, **[N]** numerical evidence, **[K]** cited from the literature, **[C]**
conjecture, **[M]** measured by another division.  The manifest adds a coarse *evidence class per file*
(Lean source / paper proofs and statements / internal AI review / prior-art assessment / computational
evidence / external public data / administrative record) and never assigns a status of its own.

What "machine-checked" covers, in the divisions' own words:

| division | what its audit established (quoted) | source |
|---|---|---|
| theory | "92 Lean files, 49 334 lines, 5068 declarations and 696 headline theorems on the three standard axioms; 192 harness tests; 618 mutations, 617 caught and one expected pass" — lower bounds, recursions and certificate kernels are [V]; "the upper bounds are not machine-checked" | [`theory.md`](01_theory/docs/collaboration/consolidation/theory.md) header, §B1 |
| engineering | one theorem of its own, `verifyM_eq`, "checked by Lean (a four-case induction).  The runs: executions by Lean's interpreter, not proof terms" | [`engineering.md`](02_engineering/docs/collaboration/consolidation/engineering.md) §B1 |
| science | "Short cores machine-checked (Lemma 1; Theorem 3 in Markov form; Theorems 4, 4′, 5, 7 in Pinsker form; Propositions 6, 9; the algebraic core of Lemma A16.5)"; for its certified brackets "nothing else is machine-checked" | [`science.md`](03_scientific_translation/docs/collaboration/consolidation/science.md) §B1, §B2 |
| ensemble | "build without warning, 5151 declarations on the three standard axioms"; "five Lean modules (1 093 lines; 26 headline statements and 10 non-vacuity witnesses…)" | [`ensemble.md`](04_ensemble_identifiability/docs/collaboration/consolidation/ensemble.md) §A, §G |
| geometry | "1 Lean file (59 declarations of ours in an audit of 5110, standard axioms only…)"; "Machine-checking covers the linear-algebra core only" | [`geometry.md`](05_geometric_inference/docs/collaboration/consolidation/geometry.md) §A, §F |
| complexity | "CX-V1–V6: finite or arithmetic cores only; no model of structures or of networks is formalised" | [`complexity.md`](06_biological_complexity/docs/collaboration/consolidation/complexity.md) §G |
| structural biology | "19 Lean 4 theorems … Checked by Lean; not reviewed by the theory division; not in its audited tree"; the software is "tested, not verified" | [`structural-biology.md`](07_structural_biology/docs/collaboration/consolidation/structural-biology.md) §B4, "State at the halt" |
| frontier | none claimed ("This division proves nothing and builds no method") | [`frontier-benchmarks.md`](08_frontier_benchmarking/docs/collaboration/consolidation/frontier-benchmarks.md) |

A text scan of every Lean file in the archive (not a build): [`11_reproducibility/LEAN_FILES.md`](11_reproducibility/LEAN_FILES.md).

<!-- GEN:lean -->
| division | Lean files | lines | `theorem`/`lemma` | files containing `sorry` | `axiom` declarations |
|---|---:|---:|---:|---:|---:|
| theory | 120 | 52944 | 2399 | 0 | 0 |
| engineering | 1 | 334 | 3 | 0 | 0 |
| science | 54 | 24765 | 1050 | 0 | 0 |
| ensemble | 8 | 3560 | 100 | 0 | 0 |
| geometry | 6 | 4861 | 134 | 0 | 0 |
| complexity | 7 | 1210 | 87 | 0 | 0 |
| structbio | 2 | 492 | 19 | 0 | 0 |
| frontier | 0 | 0 | 0 | 0 | 0 |
<!-- /GEN:lean -->

### 0.4 Suggested reading order

1. The eight consolidation reports (20–33 kB each; sections A executive assessment, B strongest
   contributions, C negative results, D practical opportunities, E next actions, F publication
   readiness, G state at the halt): linked in §1.
2. §2 below for the mathematics-paper candidate.
3. [`09_cross_divisional_dependencies/README.md`](09_cross_divisional_dependencies/README.md) for how the pieces relate.
4. Then the registers of statements (§3) and the reports they point to.

---

## 1. The strongest potentially original mathematical results

As ranked *by each division itself* in section B of its consolidation report.  The column "claim of
originality" is the division's own; "none" means the division explicitly claims none.

### 1.1 Theory — [`01_theory/docs/collaboration/consolidation/theory.md`](01_theory/docs/collaboration/consolidation/theory.md)

| | contribution | status (theirs) | claim of originality (theirs) | main text |
|---|---|---|---|---|
| B1 | **Adaptive query complexity of a certified partition function on the cube class**: exact exponents for fixed sampling (`a`), for hinted verification and for adaptive algorithms (`h`), a nested-level recursion with the sharp `1/k²` law, `ln N ≤ n·h + O(n^{1/3}(ln n)^{2/3})` | lower bounds and recursion [V]; algorithms, sharp rate, finite-`n` bound [P], refereed internally and by science | "the only candidate for a mathematics paper"; exponents not found in two sweeps; "every ingredient is classical" | §2 below |
| B2 | Machine-checked certificate kernels for a class of residuals (`verify_sound`, `verifyITop_sound`, `zverifyTop_sound`, barrier certificates, the sharp-minimum theorem) | [V] | "plausibly new, narrow": the class-robust form and machine-checked semantics; "the rules are classical" | [`THEORY_REPORT.md`](01_theory/docs/THEORY_REPORT.md) §§2–6, 11.8, 11.31; [`BLUEPRINT.md`](01_theory/docs/BLUEPRINT.md); [`proofs/CertificateAlgebra.lean`](01_theory/proofs/CertificateAlgebra.lean), `proofs/Frontiers/Partition*.lean`, `BarrierCertificate.lean`, `FactorElimination.lean` |
| B3 | Share certificates, sandwiches and the envelope sampler (Theorems 11.18, 11.18a–f; Propositions 11.113, 11.113a; Theorems 11.110–11.115) | share lemmas [V]; sampler bounds [P], reviewed by science | "a component of the science division's result, not a standalone one" | `THEORY_REPORT.md` §§11.6, 11.7, 11.30, 11.31; `HigherOrderEnvelope.lean`, `ShareLevels.lean`, `StateShares.lean`, `DownClosedRemainder.lean`, `BoxRatio.lean` |
| B4 | The abstract level theorem and its boundary: what nesting needs (11.118), dependence under influence (11.119), no gain on Gauss space (11.120), **false certificates** under uncertified influence (11.121); fields, site types, chains, two rounds (11.61–11.65, 11.95–11.101, 11.116–11.117, 11.86) | [P], refereed; parts [V] | prior art named (Ahlswede–Zhang, Yu, Gaussian isoperimetry, channel coding) | `THEORY_REPORT.md` §§11.20, 11.24, 11.26, 11.32, 11.33; workstreams [`N`](01_theory/docs/workstreams/N_REPORT.md), [`F`](01_theory/docs/workstreams/F_REPORT.md), [`U`](01_theory/docs/workstreams/U_REPORT.md), [`W`](01_theory/docs/workstreams/W_REPORT.md), [`Y`](01_theory/docs/workstreams/Y_REPORT.md); `TwoRounds.lean` |
| B5 | Tail functions beyond the uniform cube by induction over the sites (Proposition 11.124; Conjecture I6) | [P], "**unrefereed**, one day old" | none for the methods | [`I_REPORT.md`](01_theory/docs/workstreams/I_REPORT.md); `experiments/workstreams/I/` |

### 1.2 Science — [`03_scientific_translation/docs/collaboration/consolidation/science.md`](03_scientific_translation/docs/collaboration/consolidation/science.md)

| | contribution | status (theirs) | claim of originality (theirs) | main text |
|---|---|---|---|---|
| B1 | Certified two-sided free-energy brackets for a force field with a many-body (generalized-Born) solvent term, with a checkable certificate; brackets of `10⁻²`–`10⁻⁴` nats at up to `5·10¹⁷` states | paper proofs with floating-point allowances; parts (13)–(18), (23)–(24) **unrefereed**; Stage 1 checker | "not found" in six queries; "Not found is not new" | [`P3_REPORT.md`](03_scientific_translation/docs/science/workstreams/P3_REPORT.md), `P6`, `P8`, `P9`; [`INFERENCE_LIMITS_ADDENDA.md`](03_scientific_translation/docs/science/INFERENCE_LIMITS_ADDENDA.md) A17; [`SANDWICH_CERTIFICATE_FORMAT.md`](03_scientific_translation/docs/science/SANDWICH_CERTIFICATE_FORMAT.md); `experiments/science/sandwich_cert/` |
| B2 | What averaged and thermodynamic data are worth to a certified free-energy computation (marginals of bounded order change no exponent; Theorems 2–8; addendum A16) | short cores [V]; referees R3, R8 | oracle-invariance statements "not found"; "the mechanism is classical coding theory" | [`INFERENCE_LIMITS.md`](03_scientific_translation/docs/science/INFERENCE_LIMITS.md); addenda A12, A16; `experiments/science/ws_L1` … `ws_L3` (Lean) |
| B3 | Measurements of what the programme's objects cost on a real force field (class constants, certified reweighting, coverage of uncertified error bars, the rotamer discretisation) | exact enumeration on grids; partly replicated | "no originality in the mathematics is claimed" | [`PHYSICAL_APPLICABILITY.md`](03_scientific_translation/docs/science/PHYSICAL_APPLICABILITY.md); `SP_REPORT.md`, `P2_REPORT.md` |
| B4 | The validation record: thirty reviews with replication; prior-art determinations | internal AI review | a method, not mathematics | [`INDEPENDENT_VALIDATION.md`](03_scientific_translation/docs/science/INDEPENDENT_VALIDATION.md); `SCI-REV-0001` … `-0030`; [`PRIOR_ART_MATRIX.md`](03_scientific_translation/docs/science/PRIOR_ART_MATRIX.md) |
| B5 | A closed-form robust range for free-energy differences between monotone macrostates | [V] since its checkpoint 29 | "Two lines from Holley's inequality.  The statement was not found" | `INFERENCE_LIMITS_ADDENDA.md` A11, A13, A14; `experiments/science/ws_L2/Sandwich.lean` |

### 1.3 Ensemble — [`04_ensemble_identifiability/docs/collaboration/consolidation/ensemble.md`](04_ensemble_identifiability/docs/collaboration/consolidation/ensemble.md)

| | contribution | status (theirs) | claim of originality (theirs) | main text |
|---|---|---|---|---|
| B1 | Finite ensembles on a torus from multilinear trigonometric means: exact thresholds (two states; five, not six, on `𝕋³`; `K ≤ 2^r − r − 1` generic; a non-SOS certificate) | parts [V]; rest [P] with exact computer algebra; ER3, ER4 | counts "not found"; mechanisms known (di Dio–Schmüdgen Thm 40; probably Baldi–Blekherman–Sinn) | [`ENSEMBLE_REPORT.md`](04_ensemble_identifiability/docs/ensemble/ENSEMBLE_REPORT.md) §4c.4; `proofs/Ensemble/TwoStateCertificate.lean`, `PermanentCertificate.lean` |
| B2 | Ensembles of frameworks from laws of edge lengths; a sharp quantitative Rényi–Heppes theorem (E4, E4.1, E5–E8) | E4 and the first bound of E4.1 [V]; ER1; SCI-REV-0020 | "not found"; "a combinatorialist may call E4 folklore" | report §3; `proofs/Ensemble/RenyiHeppes.lean` |
| B3 | Certified partial identification under realistic observation models (E1.1, E17–E17.2, E23–E32) | core [V]; E17.1, E17.2, E23.1, E27–E32 **unreviewed** | "Little is claimed"; "elementary convex analysis" | report §4b, §4d, §4e; [`SOFTWARE_INTERFACE.md`](04_ensemble_identifiability/docs/ensemble/SOFTWARE_INTERFACE.md); `proofs/Ensemble/Exposedness.lean` |
| B4 | An exact criterion for the thermal union bound (E15U) | core of E15(c) [V]; ER2; re-derived by science (SCI-RES-0038) | "not found" in two searches | report §4a; `proofs/Ensemble/ThermalUnionBound.lean` |
| B5 | How many random conformers pair data on the cube can identify (E10–E12, E19) | synthesis of known theorems; thresholds are conjectures | E19(a), E19(g) found in print | report §4, §4c |

### 1.4 Geometry — [`05_geometric_inference/docs/collaboration/consolidation/geometry.md`](05_geometric_inference/docs/collaboration/consolidation/geometry.md)

| | contribution | status (theirs) | claim of originality (theirs) | main text |
|---|---|---|---|---|
| B1 | Second-moment rigidity of ensembles: the conic criterion, exact thresholds `⌈(9K² + K + 8)/4⌉`, demixing with a certificate (Theorems A, B, B′, C, F, G, H; DEMIX) | core lemmas [V]; reviewed (GEOMETRY-REV-0001, SCI-REV-0021); Theorem C computer-assisted | not found for `d ≥ 2`; "the `d = 1` case is in print" (Laurent–Poljak) | [`ENSEMBLE_RIGIDITY.md`](05_geometric_inference/docs/geometry/ENSEMBLE_RIGIDITY.md) §§2–7; [`proofs/Geometry/EnsembleRigidity.lean`](05_geometric_inference/proofs/Geometry/EnsembleRigidity.lean) |
| B2 | Below the conic threshold: identifiability from 10, 16, 30 points by a quartic linear-algebra certificate (Theorems I, I′; Conjecture 6.3) | computer-assisted, exact; "§6.2 itself has had no outside reader" | "the method is published" (Johnston–Lovitz–Vijayaraghavan); thresholds not found | `ENSEMBLE_RIGIDITY.md` §5.5, §6.2 |
| B3 | Sequence-local distances: a global `n²` stability law (Theorems K, L, L⁺) | reviewed with replication (SCI-REV-0028) | "a discrete, explicit version of a known phenomenon"; "as a guarantee it is empty" | [`LOCAL_DATA_STABILITY.md`](05_geometric_inference/docs/geometry/LOCAL_DATA_STABILITY.md) |
| B4 | Partial observation: a counting rule and an obstruction for sparse labels (P1–P3) | **unreviewed** | count "not found (… a thin basis)" | [`LABEL_PATTERNS.md`](05_geometric_inference/docs/geometry/LABEL_PATTERNS.md) |
| B5 | Noise and inexact local geometry with computable constants (N0–N6) | **unreviewed, written last** | "Novelty of technique: none claimed" | [`ROBUST_DEMIXING.md`](05_geometric_inference/docs/geometry/ROBUST_DEMIXING.md) |
| — | Hinge ensembles (not ranked; main statement first obtained by science's referee, Proposition R22-1) | exact | joint | [`HINGE_ENSEMBLES.md`](05_geometric_inference/docs/geometry/HINGE_ENSEMBLES.md) |

### 1.5 Complexity — [`06_biological_complexity/docs/collaboration/consolidation/complexity.md`](06_biological_complexity/docs/collaboration/consolidation/complexity.md)

| | contribution | status (theirs) | claim of originality (theirs) | main text |
|---|---|---|---|---|
| B1 | Multi-strand folding in the nearest-neighbour model is strongly NP-hard for every fixed energy function in a class given by two sign conditions; the hard parameter is the number of species | paper proofs; three internal reviews (one by science, SCI-REV-0019); Lean for two arithmetic cores | answers a question two recent papers list as open, "for that class"; "the gadget is Lyngsø's"; "our record on novelty statements is poor" | [`STRANDS_NN_HARDNESS.md`](06_biological_complexity/docs/complexity/STRANDS_NN_HARDNESS.md) |
| B2 | The NANUQ metric of outer-labeled planar networks: local criterion, a seven-leaf counterexample, level 2 completely (Theorems 12, 12′) | paper proofs plus exact finite computations; four reviews | everything about non-galled networks "no source found"; the galled case a "probable rediscovery" of an unread third-party claim | [`NANUQ_LOCAL_CRITERION.md`](06_biological_complexity/docs/complexity/NANUQ_LOCAL_CRITERION.md) |
| B3 | Partition function, minimum free energy and level counts of interacting strands over all orderings, with symmetry | paper proofs; two reviews; agreement with enumeration | "the extension written out, proved and tested — not the idea" | [`STRANDS_ALGORITHM.md`](06_biological_complexity/docs/complexity/STRANDS_ALGORITHM.md); `experiments/complexity/strands/` |
| B4 | Recognising exact ground-state sets of pair energies (the ensemble division's question) | two reviews; "mostly known" | four statements "no source found"; the question for `K ≫ log n` open | [`ISING_GROUND_SETS.md`](06_biological_complexity/docs/complexity/ISING_GROUND_SETS.md) |

### 1.6 Structural biology, frontier benchmarking, engineering

None of the three claims a mathematically original result.

* **Structural biology** ([report](07_structural_biology/docs/collaboration/consolidation/structural-biology.md)): B1 checkable enclosures of `ln Z` and rotamer populations (C2) — "at most a new combination of existing techniques"; B2 quantified limits of certified side-chain computation; B3 certified minima with an independent checker (C1) — "in substance … an exact LP dual with an elimination trace — not new"; B4 machine-checked rule semantics (19 Lean theorems; "none as mathematics").
* **Frontier benchmarking** ([report](08_frontier_benchmarking/docs/collaboration/consolidation/frontier-benchmarks.md)): "None is mathematically original and none claims to be": B1 a head-to-head evaluation with a causal diagnosis; B2 evaluation-integrity procedures; B3 the CASP17 determination; B4 replication of nine identification controls.
* **Engineering** ([report](02_engineering/docs/collaboration/consolidation/engineering.md)): "This division proves nothing."  B1 independent verification of the certificate stack up to executing the theory kernel on six stored certificates of the structural-biology division's first model (`verifyM_eq`; the certificates of its later models were not covered — `09_cross_divisional_dependencies/README.md` §3.1); B2 the nested adaptive algorithm at finite size; B3 exact enumerations ("most likely a rediscovery in substance"); B4 corrections; B5 certified interval computations.

---

## 2. The mathematics-paper candidate: adaptive query complexity of a certified free energy on the cube class

The theory division names this (its B1) "the only candidate for a mathematics paper".  Everything it
rests on is in the archive.  Statement, in the division's words (consolidation report §B1): for
`A(ψ) = 2^{−n}Σ_x e^{−ψ(x)}` with `ψ` any `u`-Lipschitz function on the `n`-cube and randomised algorithms that
return a bracket of ratio `e^ε` with probability `1 − δ` from evaluations of `ψ`: (i) sampling fixed in
advance costs `exp(n·a + o(n))`, `a = KL(p_u‖½)`; (ii) no algorithm, adaptive or hinted, beats `exp(n·h)`;
(iii) an adaptive algorithm without a hint reaches `exp(n·h + o(n))` by nested levels; (iv)
`k²(τ_k − h) → 2π²h²θ_hint″(0)`; (v) at finite `n`, `ln N ≤ n·h + O(n^{1/3}(ln n)^{2/3})`.  At `u = 1`:
`a = 0.1109`, `h = 0.0291`.

### 2.1 Where each part is

All paths in this subsection are under [`01_theory/`](01_theory/00_DIVISION_INDEX.md) unless another directory is named.

| item | theorem (label in the report) | text and proof | formal verification | internal reviews |
|---|---|---|---|---|
| Hinted exponent and the lower bound for every algorithm | Theorem 11.25 ("[V lower bounds; P + K upper bounds]") | `docs/THEORY_REPORT.md` §11.10; `docs/workstreams/A_REPORT.md` | `proofs/Frontiers/QueryLowerBound.lean` (lower bounds); see `THEORY_REPORT.md` §9 for the full index | `docs/reviews/R3_referee_report.md`, `R4_referee_report.md` |
| Non-adaptive exponent: Monte Carlo is exponent-optimal among fixed samples | Theorems 11.44, 11.45 | `THEORY_REPORT.md` §11.16 | `proofs/Frontiers/NonAdaptive.lean` (`nonadaptive_expected_queries_ge`, `cube_nonadaptive_bound`) | `docs/reviews/R5_referee_report.md` |
| Adaptive exponent = hinted exponent; one more level; the recursion | Theorems 11.52, 11.53, 11.54 | `THEORY_REPORT.md` §11.18; `docs/workstreams/H_REPORT.md` | `proofs/Frontiers/HintRecursion.lean`, `CubeHintPair.lean` (recursion converges, [V]); `docs/workstreams/L_REPORT.md`, `M_REPORT.md`, `GamePair.lean` | `docs/reviews/R7_referee_report.md`; science [`SCI-REV-0007`](03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0007.md) (cost accounting re-derived; workstream [`R6`](03_scientific_translation/docs/science/workstreams/R6_REPORT.md)) |
| The slope map and the saddle-node; **the sharp `1/k²` law** | Theorems 11.53a, 11.53b | `THEORY_REPORT.md` §11.18; `docs/workstreams/R_REPORT.md` | `proofs/Frontiers/LineDynamics.lean` (parts of 11.53a); rate `O(1/k)`: `proofs/Frontiers/RateFull.lean` (written by science, adopted unchanged) | `docs/workstreams/R_REVIEW_A.md`, `R_REVIEW_B.md`; science [`SCI-REV-0014`](03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0014.md), workstream [`R13`](03_scientific_translation/docs/science/workstreams/R13_REPORT.md) |
| Every bounded accuracy | Lemma 11.55, Theorem 11.56, Proposition 11.57, Theorem 11.58 | `THEORY_REPORT.md` §11.19; `docs/workstreams/K_REPORT.md` | `proofs/Frontiers/BoundedAccuracy.lean` | `docs/reviews/R8_referee_report.md`; science [`SCI-REV-0016`](03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0016.md) (certified third level) |
| Explicit sub-exponential term `n·h + O(√(n ln n))` | Theorem 11.58a | `THEORY_REPORT.md` §11.19; `docs/workstreams/Q_REPORT.md`, `Q2_REPORT.md` | — | `docs/reviews/R12_referee_report.md`, `docs/workstreams/Q2_REVIEW.md`; science [`SCI-REV-0017`](03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0017.md) |
| **Finite size: `n·h + O(n^{1/3}(ln n)^{2/3})`**, certified exponents of `k` levels | Theorem 11.58e | `THEORY_REPORT.md` §11.19; `docs/workstreams/Z_REPORT.md`, `Z_ADDENDUM.md` | — (interval arithmetic in `experiments/workstreams/Z/`) | `docs/workstreams/Z_REVIEW.md`, `Z_ADDENDUM_REVIEW.md`, `Z_A6_REVIEW.md`; science [`SCI-REV-0030`](03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0030.md) — **published incomplete** (referee wound down at the halt; workstream [`R29`](03_scientific_translation/docs/science/workstreams/R29_REPORT.md)) |
| Two rounds of adaptivity lie strictly between | Theorem 11.86 | `THEORY_REPORT.md` §11.24; `docs/workstreams/U_REPORT.md` | `proofs/Frontiers/TwoRounds.lean`, `TwoRoundsExpected.lean` | science [`SCI-REV-0003`](03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0003.md) |

Also: the index of machine-checked statements, `docs/THEORY_REPORT.md` §9; the assumption audit of these
sections, `docs/audit/AA2_REPORT.md` (§§11.16–11.32) with `docs/audit/APPLIED_CORRECTIONS.md` and
`docs/ASSUMPTION_AUDIT.md`; science's sampled check of that audit, [`SCI-REV-0022`](03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0022.md);
errata on the way (D63, D66, D68) in `docs/DEAD_ENDS.md`; what a publication would need, `docs/THEORY_REPORT.md` §12
and the consolidation report §E1, §F.

### 2.2 Computational evidence

| what | where |
|---|---|
| Theory's own evaluations of the cost formulas; nests of two to seven levels; certified tops | `01_theory/experiments/workstreams/{K,Q,Q2,R,Z}/`; `01_theory/experiments/coordinator_checks/{nested_review_R6,level_rate,three_levels_certified}/`; `01_theory/experiments/reviews/R8/`, `R12/` |
| Engineering: the certified recursion of nested runs to six levels at `n ≤ 16 000`, designs run on searched instances, literal simulations on cubes of 8–16 sites; what a third, fourth, fifth level keeps of its asymptotic gain | `02_engineering/src/metricchain_eng/twolevel/`, `02_engineering/experiments/eng/twolevel/`; [`ENG-RES-0008`](02_engineering/docs/collaboration/responses/engineering/ENG-RES-0008.md), [`-0013`](02_engineering/docs/collaboration/responses/engineering/ENG-RES-0013.md), [`-0014`](02_engineering/docs/collaboration/responses/engineering/ENG-RES-0014.md), [`-0015`](02_engineering/docs/collaboration/responses/engineering/ENG-RES-0015.md), [`-0017`](02_engineering/docs/collaboration/responses/engineering/ENG-RES-0017.md); protocol with hypotheses written before collection: [`BM-1_X-011.md`](02_engineering/docs/engineering/benchmarks/protocols/BM-1_X-011.md) |
| Engineering: sites with different slopes (heterogeneous cubes), certified algorithm and 64 800 literal runs | [`ENG-RES-0016`](02_engineering/docs/collaboration/responses/engineering/ENG-RES-0016.md); `02_engineering/experiments/eng/review_x014/REPORT.md`; [`ENG-MSG-0008`](02_engineering/docs/collaboration/messages/engineering/ENG-MSG-0008.md) §2(c) |
| Engineering: numerical check of the rate theorem on new instances — **subagent's report, the coordinator's review not complete** (reports four numerical discrepancies in the theory report's tables and a site outside the binary family where hypothesis (H1) fails) | [`02_engineering/experiments/eng/level_rate/REPORT.md`](02_engineering/experiments/eng/level_rate/REPORT.md) |
| Science: replications (nested cost accounting; the rate; the third level; Theorem 11.58a) | `03_scientific_translation/experiments/science/ws_R6/`, `ws_R13/`, `ws_R16/`, `ws_R17/`, `ws_R29/` |

### 2.3 Closest prior art and unresolved novelty questions

* Theory's own list (consolidation report §B1): information-based complexity of integration (Bakhvalov;
  Novak), relative-error sequential Monte Carlo (Dagum–Karp–Luby–Ross), multilevel splitting / subset
  simulation / nested sampling, solvable integration problems (Kunsch–Novak–Rudolf 2019), Block and Shetty
  (arXiv 2602.23535), Harper's theorem.  Sweeps: `01_theory/docs/prior_art/L7_query_complexity.md`,
  `L6_transport_entropy_and_information_limits.md`, `L9_review_additions.md`; `01_theory/docs/THEORY_REPORT.md` §13.
* Science's independent determinations: [`SCI-REV-0004`](03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0004.md)
  ("What is in print, and what is not, in the query-complexity cluster"), workstream
  [`A1`](03_scientific_translation/docs/science/workstreams/A1_REPORT.md), [`PRIOR_ART_MATRIX.md`](03_scientific_translation/docs/science/PRIOR_ART_MATRIX.md).
  Its summary (consolidation report §B4): the odds-ratio lemma, the non-adaptive exponent formulas at the
  cone and the channel-coding dictionary's identities are **in print**; "adaptive = hinted" with exact
  exponents and a matching algorithm without log-concavity, and the two-round separation — **not found**.
* Open, in theory's words: "The literature was read by AI, mostly at the level of abstracts and
  introductions.  A specialist in information-based complexity may know the exponents as folklore."
  Sources science could not open are listed in its report §E3.

### 2.4 Generalisations, limitations and related results elsewhere in the archive

| what | who | where |
|---|---|---|
| The level theorem on an arbitrary probability space; where it works, where it cannot, where it returns false certificates | theory (B4); reviewed by science (SCI-REV-0027) | `01_theory/docs/THEORY_REPORT.md` §11.33; `01_theory/docs/workstreams/N_REPORT.md`, `N_REVIEW.md` |
| Fields, mean-field and chain known parts, several site types, slices | theory | `THEORY_REPORT.md` §§11.20, 11.23, 11.25, 11.26, 11.32; workstreams `F`, `T`, `W`, `Y` |
| Beyond the uniform cube: tail functions by induction over the sites (**unrefereed**) | theory (B5) | `01_theory/docs/workstreams/I_REPORT.md` |
| Averaged data added to energy evaluations change no exponent in the worst case | science (B2); theory Proposition 11.104, Theorem 11.109a | `03_scientific_translation/docs/science/INFERENCE_LIMITS.md`; `01_theory/docs/THEORY_REPORT.md` §§11.27, 11.29 |
| Finite size: "not competitive at any size at which it has been run"; worse than plain Monte Carlo up to about `2·10⁴` sites; a fifth level keeps at most a quarter of its asymptotic gain at `n ≤ 16 000` | theory §A, §B1; engineering B2, §C | `02_engineering/docs/collaboration/consolidation/engineering.md` |
| "the theory division's finite-size theorem beats non-adaptive cost only where it certifies `e^{890}` evaluations (their numbers, read by one referee)" | science §C | `03_scientific_translation/docs/collaboration/consolidation/science.md` |
| The constants of the finite-`n` theorem "are far from what the exact recursion shows (47–50 `ln n` per level in the proof, one to two and a half measured)" | theory §B1 | `01_theory/docs/collaboration/consolidation/theory.md` |
| Strongest unresolved problem: "is `n·h + Θ(n^{1/3})` the true second-order cost, or an artefact of block nesting" | theory, "State at the halt" | same |
| The real residuals measured so far lie outside the cheap classes for which the theory is sharp (class constants of 12 to 53 `kT` per site for an implicit-solvent term) | science B3; theory §A | `03_scientific_translation/docs/science/PHYSICAL_APPLICABILITY.md` |

---

## 3. Exact proofs and verification status: where the registers are

| division | register of statements with their status | proofs | proof obligations / open items |
|---|---|---|---|
| theory | [`docs/collaboration/status/theory.md`](01_theory/docs/collaboration/status/theory.md); `docs/THEORY_REPORT.md` §0.2–0.3 and §9 (index of machine-checked statements); [`docs/BLUEPRINT.md`](01_theory/docs/BLUEPRINT.md) | [`docs/THEORY_REPORT.md`](01_theory/docs/THEORY_REPORT.md) (1.2 MB), `docs/workstreams/*_REPORT.md`, `proofs/` (92 Lean files) | [`docs/ASSUMPTION_AUDIT.md`](01_theory/docs/ASSUMPTION_AUDIT.md), `docs/THEORY_REPORT.md` §12 |
| engineering | [`docs/engineering/EXPERIMENT_REGISTER.md`](02_engineering/docs/engineering/EXPERIMENT_REGISTER.md) (X-001 … X-019), [`docs/collaboration/status/engineering.md`](02_engineering/docs/collaboration/status/engineering.md) | the responses `ENG-RES-0001` … `-0019`; `experiments/eng/*/REPORT.md` | consolidation report §H |
| science | [`docs/collaboration/status/science.md`](03_scientific_translation/docs/collaboration/status/science.md), [`docs/science/INDEPENDENT_VALIDATION.md`](03_scientific_translation/docs/science/INDEPENDENT_VALIDATION.md) | `docs/science/INFERENCE_LIMITS.md`, `INFERENCE_LIMITS_ADDENDA.md`, `docs/science/workstreams/*_REPORT.md`, `experiments/science/ws_L*/*.lean` | [`docs/science/OPEN_PROBLEMS.md`](03_scientific_translation/docs/science/OPEN_PROBLEMS.md), [`RESEARCH_SYNTHESIS.md`](03_scientific_translation/docs/science/RESEARCH_SYNTHESIS.md) |
| ensemble | [`docs/ensemble/THEOREM_REGISTER.md`](04_ensemble_identifiability/docs/ensemble/THEOREM_REGISTER.md) (E1–E32) | [`docs/ensemble/ENSEMBLE_REPORT.md`](04_ensemble_identifiability/docs/ensemble/ENSEMBLE_REPORT.md), `proofs/Ensemble/` | [`OPEN_OBLIGATIONS.md`](04_ensemble_identifiability/docs/ensemble/OPEN_OBLIGATIONS.md) |
| geometry | [`docs/geometry/THEOREM_REGISTER.md`](05_geometric_inference/docs/geometry/THEOREM_REGISTER.md) (58 rows) | `docs/geometry/ENSEMBLE_RIGIDITY.md`, `LOCAL_DATA_STABILITY.md`, `LABEL_PATTERNS.md`, `ROBUST_DEMIXING.md`, `HINGE_ENSEMBLES.md`; `proofs/Geometry/EnsembleRigidity.lean` | [`PROOF_OBLIGATIONS.md`](05_geometric_inference/docs/geometry/PROOF_OBLIGATIONS.md) (O-1 … O-19) |
| complexity | [`docs/complexity/THEOREMS.md`](06_biological_complexity/docs/complexity/THEOREMS.md) (CX-T…, CX-V…) | the notes under `docs/complexity/`; `experiments/complexity/lean/` | [`OPEN_PROBLEMS.md`](06_biological_complexity/docs/complexity/OPEN_PROBLEMS.md) |
| structural biology | [`docs/structural_biology/RESULTS.md`](07_structural_biology/docs/structural_biology/RESULTS.md) (R-1 … R-13), [`THEOREM_TO_SOFTWARE_REGISTER.md`](07_structural_biology/docs/structural_biology/THEOREM_TO_SOFTWARE_REGISTER.md), [`VERIFICATION_REPORT.md`](07_structural_biology/docs/structural_biology/VERIFICATION_REPORT.md) | `proofs/StructBio/FactorElimination.lean` | [`OPEN_PROBLEMS.md`](07_structural_biology/docs/structural_biology/OPEN_PROBLEMS.md), `HANDOFF.md` |
| frontier | [`docs/frontier_benchmarks/RESULTS.md`](08_frontier_benchmarking/docs/frontier_benchmarks/RESULTS.md), [`BENCHMARK_REGISTRY.md`](08_frontier_benchmarking/docs/frontier_benchmarks/BENCHMARK_REGISTRY.md) | — | [`IMPROVEMENT_REGISTER.md`](08_frontier_benchmarking/docs/frontier_benchmarks/IMPROVEMENT_REGISTER.md) |

Internal referee reports and their corrections are listed per division in each `00_DIVISION_INDEX.md`
(classes `referee-report`, `mailbox-review`, `assumption-audit`).  Counts of files by class:

<!-- GEN:classes -->
| class | files | MiB | meaning |
|---|---:|---:|---|
| consolidation-report | 8 | 0.21 | the division's own critical assessment written under the consolidation directive |
| mathematical-report | 62 | 5.42 | theorem statements, definitions, proofs, workstream reports and research notes |
| lean-proof | 198 | 5.36 | Lean 4 source (formal statements and proofs) |
| theorem-register | 9 | 0.33 | registers of statements, proof obligations, experiments or improvements, with their status |
| referee-report | 61 | 3.10 | internal AI referee reports and reviews kept as documents |
| mailbox-review | 37 | 0.68 | reviews with replication sent through the collaboration mailbox |
| mailbox-message | 105 | 1.12 | messages between divisions |
| mailbox-request | 26 | 0.17 | requests between divisions |
| mailbox-response | 109 | 1.42 | responses between divisions |
| mailbox-other | 9 | 0.00 | other files of a mailbox directory (templates, placeholders, notes) |
| status-or-digest | 27 | 1.14 | status tables, digests to other divisions, synchronisation logs, mailbox rules |
| cross-division-intake | 15 | 0.55 | a division's written reading of the other divisions' work |
| prior-art | 23 | 1.24 | prior-art and literature assessments |
| assumption-audit | 7 | 0.45 | assumption audits and registers |
| negative-results | 8 | 0.33 | dead ends, withdrawn claims, negative results |
| open-problems | 5 | 0.17 | open problems, publication opportunities, frontier maps |
| handoff-or-log | 27 | 1.09 | research logs, handoff documents, plans, READMEs |
| owner-directives | 4 | 0.12 | the research owner's directives as recorded by a division |
| benchmark-or-evaluation-record | 28 | 0.51 | benchmark plans, protocols, registries, results, ledgers, verification reports |
| software-documentation | 4 | 0.11 | interfaces, formats and implementation guides |
| workstream-brief | 85 | 0.61 | briefs given to subagents (what a workstream or referee was asked to do) |
| source-code | 77 | 0.82 | packages, job drivers and repository scripts |
| test | 32 | 0.58 | test suites |
| experiment-script | 1854 | 13.81 | scripts of experiments, checks and reviews |
| experiment-report | 180 | 2.83 | reports and READMEs stored with experiments |
| certificate | 68 | 6.21 | certificate files and conformance vectors |
| stored-result | 4775 | 83.14 | stored outputs and raw results of computations |
| evaluation-freeze | 31 | 0.31 | frozen evaluation records: manifests, commitments, time-stamp tokens, frozen scores |
| input-data | 12 | 1.49 | public input structures and test data |
| build-config | 10 | 0.01 | toolchain and dependency pins, ignore files |
<!-- /GEN:classes -->

## 4. Closest known prior art

Each consolidation report gives, per contribution, "closest prior art", "evidence for originality" and
"evidence against".  The underlying assessments:

| division | prior-art documents |
|---|---|
| theory | the ten sweeps by topic under `01_theory/docs/prior_art/` (`L1_…` to `L10_…`); `docs/THEORY_REPORT.md` §13 |
| science | [`PRIOR_ART_MATRIX.md`](03_scientific_translation/docs/science/PRIOR_ART_MATRIX.md); workstreams `A1`–`A4`; `SM_REPORT.md`; `SCI-REV-0004`, `-0006`, `-0023` |
| ensemble | [`PRIOR_ART.md`](04_ensemble_identifiability/docs/ensemble/PRIOR_ART.md) |
| geometry | [`PRIOR_ART.md`](05_geometric_inference/docs/geometry/PRIOR_ART.md) |
| complexity | [`PRIOR_ART.md`](06_biological_complexity/docs/complexity/PRIOR_ART.md) |
| structural biology | [`PRIOR_ART.md`](07_structural_biology/docs/structural_biology/PRIOR_ART.md), [`BASELINE_REGISTER.md`](07_structural_biology/docs/structural_biology/BASELINE_REGISTER.md) |
| frontier | [`STATE_OF_THE_ART.md`](08_frontier_benchmarking/docs/frontier_benchmarks/STATE_OF_THE_ART.md); `docs/frontier_benchmarks/literature/LIT_*.md` (four) |
| engineering | none of its own (consolidation report §B: "general knowledge"; "this division did not search") |

## 5. Working implementations

| what | division | where | state (theirs) |
|---|---|---|---|
| Lean library of certificate kernels and exponent theory; audit script; reference checker with conformance vectors | theory | `01_theory/proofs/`, `scripts/audit_all.sh`, `experiments/reference_checker.py`, `experiments/certs/` | audit passed at its final tree |
| `metricchain_eng`: nested adaptive algorithm (two-level and nested designs, heterogeneous slopes), exact leaf-certificate checker and producer, weighted cubes, chain covers; Modal batch driver; independent checkers of the structural-biology formats; the kernel runner `RunKernel.lean` | engineering | `02_engineering/src/metricchain_eng/`, `tests/eng/`, `modal_jobs/`, `experiments/eng/sb_review/`, `experiments/eng/sb_zcheck/` | tested; subagent-written parts marked unreviewed |
| Sandwich certificate (format `metricchain-sandwich/1`) with a Stage 1 reference checker; research scripts for the certified brackets | science | `03_scientific_translation/experiments/science/sandwich_cert/`, `ws_P3`, `ws_P6`, `ws_P8`, `ws_P9`, `pi_inference/` | "research scripts with untracked caches" |
| Check scripts tied to the report's sentences; reference instances with ground truth | ensemble | `04_ensemble_identifiability/experiments/ensemble/` (`benchmark_controls.py`, `benchmarks/controls_v1.json`, `torus_instances_v1.json`) | "we wrote no software beyond check scripts" |
| DEMIX and exact rank computations; labelled benchmark instances | geometry | `05_geometric_inference/experiments/geometry/` (`demix.py`, `robust_demix.py`, `exact_*.py`, `benchmark_suite/`) | reference scripts, floating point where not exact |
| Exact partition function / minimum free energy / level counts for interacting strands; ground-set recognition | complexity | `06_biological_complexity/experiments/complexity/strands/`, `ising_faces/`, `nanuq/` | "unoptimised Python, validated for `N ≤ 16`" |
| `metricchain_sb`: rotamer tables from a structure, certified minima (C1, C1b), certified `ln Z` and populations (C2), checkers | structural biology | `07_structural_biology/src/metricchain_sb/`, `tests/structbio/`, `experiments/structbio/` | "tested, not verified"; repaired checkers not yet attacked again |
| `metricchain_fb`: freezes, RFC 3161 time-stamps, commitments, structure scores | frontier | `08_frontier_benchmarking/src/metricchain_fb/`, `tests/frontier/` | 64 tests |

## 6. Significant negative results

Each consolidation report has a section C; each division keeps a register of dead ends:
[theory `DEAD_ENDS.md`](01_theory/docs/DEAD_ENDS.md) (D1–D70),
[engineering](02_engineering/docs/engineering/DEAD_ENDS.md) (ED-1 … ED-14),
[science](03_scientific_translation/docs/science/DEAD_ENDS.md) (SD13–SD78),
[ensemble](04_ensemble_identifiability/docs/ensemble/DEAD_ENDS.md) (ED1–ED25),
[geometry](05_geometric_inference/docs/geometry/DEAD_ENDS.md) (DG-1 … DG-27),
[complexity](06_biological_complexity/docs/complexity/DEAD_ENDS.md),
[structural biology](07_structural_biology/docs/structural_biology/DEAD_ENDS.md),
[frontier `NEGATIVE_RESULTS.md`](08_frontier_benchmarking/docs/frontier_benchmarks/NEGATIVE_RESULTS.md) (N-1 … N-23).
The ones the divisions themselves call consequential:

* **No evidence about a molecule, and no demonstrated advantage.**  Frontier: "nothing in the programme
  has been compared with experiment by an independent party"; structural biology: "No improvement over
  established methods has been demonstrated on any dimension"; science: "Nothing here is evidence about a molecule."
* **Exactness is not the accuracy bottleneck.**  Published evidence (Yanover, Schueler-Furman, Weiss 2008,
  read at abstract level) says an exact optimum improves side-chain accuracy by less than 0.1 %; the
  guarantees are "two to four orders of magnitude more precise than the model they are about" (science §A).
  The recurring conclusion (theory §B2, science §A, frontier §C): *auditability, not accuracy*.
* **The certified route loses on speed.**  toulbar2 is 6–27 times faster on the development structures
  and 17–326 times on public instances; the certified route certified 4 of 10 public instances in 300 s
  (frontier B1; structural biology §C).  On every development instance the linear relaxation is tight, so
  the certificate is in substance an LP dual.
* **The nested adaptive algorithm is not competitive at any size at which it has been run** (theory §C;
  engineering §C).
* **The verified kernel as written cannot be executed at realistic size** — exponential in the length of
  an elimination chain; a proved-equal memoised version can (engineering B1(d); `ENG-MSG-0008` §2).
* **The cheap residual classes do not contain the physics measured so far** (science B3: class constants
  12–53 `kT`).
* **With realistic data no ensemble is identified**; verdicts are unstable under refinement of the pool
  (E30); distance-law results have no stability modulus (O4) (ensemble §A, §C).
* **Quantitative geometric guarantees are empty at realistic accuracy** (certified ranges of `10⁻⁵` Å);
  the idealised observable is measured by no instrument (geometry §A, §C).
* **A random seed inside the first structural-biology energy model** moved the certified minimum by
  13–25 kcal/mol (found by science, SCI-REV-0026; confirmed and removed).
* **Rediscoveries and withdrawn novelty claims**: theory D11, D12, D24 (certification geometry is
  polytrope and tropical geometry), the cost table of certified reweighting (Block–Shetty), Theorem I3
  (Marton); science's rediscoveries (§C); ensemble E1(b) = di Dio–Schmüdgen; geometry Theorem B for
  `d = 1` (Laurent–Poljak), the method of §6.2; complexity: "three times in one day … something we had
  called ours was known".
* **False statements found by review**, all recorded with their corrections: lists in every report's §C.

## 7. Benchmarks: completed, failed, running, proposed

See [`10_benchmark_status/README.md`](10_benchmark_status/README.md) (one table across divisions, with
sources), [`10_benchmark_status/COMPUTE_AND_MODAL.md`](10_benchmark_status/COMPUTE_AND_MODAL.md) (every
Modal job and what is still running) and
[`10_benchmark_status/INCOMPLETE_AND_UNREVIEWED.md`](10_benchmark_status/INCOMPLETE_AND_UNREVIEWED.md).
In one sentence: every evaluation so far is on development or synthetic instances; **no held-out
evaluation has been run by anyone**, the sealed held-out list is unopened, and no MetricChain entry
exists for CASP17.

## 8. The most promising unresolved research opportunities

Each division was asked for at most three next actions (section E of its report), with prerequisites,
baselines, success and failure criteria.  Titles as the divisions wrote them:

| division | E1 | E2 | E3 |
|---|---|---|---|
| theory | An external human review of the adaptive-complexity theorem, and a manuscript | One end-to-end certified `ln Z` on a small protein, with the chain of trust closed | Only if the theory line is continued: prove or refute Conjecture I6 |
| engineering | The held-out certified-optimum benchmark with the proof-logging comparison | Close the two gaps under every application claim: the energy tables and their rounding | Make the verified kernel a usable program |
| science | The error budget on real protein instances: does a certificate change any conclusion? | Stage 2 of the certificate and a referee for the unrefereed parts | An originality determination that would stand before an external expert, for B1 and B2 |
| ensemble | Are certified intervals informative on realistic problems? (the decisive experiment) | The chimera gap (Problem O4): can distance distributions be used at all? | External reading of the three possibly original results |
| geometry | Identifiability for the linear observables that exist: block sums | Make B1 + B2 (+ hinges, + B4) defensible before a human expert | Only if a quantitative theory is wanted: the two gaps |
| complexity | Make the strand results externally defensible and test the reference algorithm against established software | Settle the status of the NANUQ classification | Put the certification theory to work on the one piece of software that exists |
| structural biology | Frozen held-out evaluation of C1 and the null method | C2 as a certified oracle on an accepted model | What the certified number means: discretisation |
| frontier | Certified search at the speed of the solver it checks | Certified ensemble intervals on public experimental data, against maximum-entropy reweighting | The certified optimum against experiment: side-chain placement (protocol FB-P-02) |

Open mathematical problems named by the divisions: theory, "State at the halt" (four problems) and
`THEORY_REPORT.md` §12; science [`OPEN_PROBLEMS.md`](03_scientific_translation/docs/science/OPEN_PROBLEMS.md);
ensemble [`OPEN_OBLIGATIONS.md`](04_ensemble_identifiability/docs/ensemble/OPEN_OBLIGATIONS.md) (Problem O4, conjectures C2, C3);
geometry [`PROOF_OBLIGATIONS.md`](05_geometric_inference/docs/geometry/PROOF_OBLIGATIONS.md) (Conjecture 6.3, Conjecture P);
complexity [`OPEN_PROBLEMS.md`](06_biological_complexity/docs/complexity/OPEN_PROBLEMS.md) (E-C1 for `K ≫ log n`; #P-hardness at a fixed temperature);
structural biology [`OPEN_PROBLEMS.md`](07_structural_biology/docs/structural_biology/OPEN_PROBLEMS.md).
Incomplete arguments that the divisions consider promising are marked in those files and in the
"unreviewed" column of [`10_benchmark_status/INCOMPLETE_AND_UNREVIEWED.md`](10_benchmark_status/INCOMPLETE_AND_UNREVIEWED.md).

## 9. Dependencies between the divisions, and open disagreements

[`09_cross_divisional_dependencies/README.md`](09_cross_divisional_dependencies/README.md) lists the
documented relationships (who uses, reviewed, corrected or replicated what), the disagreements and the
messages that were never read by their addressee because both sides had halted;
[`MAILBOX_INDEX.md`](09_cross_divisional_dependencies/MAILBOX_INDEX.md) lists all
<!-- GEN:mail -->
277 mailbox items (theory 49, engineering 28, science 110, ensemble 20, geometry 29, complexity 23, structbio 12, frontier 6)
<!-- /GEN:mail -->
with dates and titles; `CROSS_REFERENCES.json` gives, for every mailbox identifier, the files that cite it.
Three divisions wrote their own reading of all the others, which is the nearest existing thing to a
synthesis: frontier ([`SCIENTIFIC_SYNTHESIS.md`](08_frontier_benchmarking/docs/frontier_benchmarks/SCIENTIFIC_SYNTHESIS.md),
[`MATHEMATICAL_FEEDBACK.md`](08_frontier_benchmarking/docs/frontier_benchmarks/MATHEMATICAL_FEEDBACK.md),
`docs/frontier_benchmarks/intake/INTAKE_*.md`), structural biology
([`RESEARCH_INTAKE.md`](07_structural_biology/docs/structural_biology/RESEARCH_INTAKE.md), `docs/structural_biology/intake/*.md`,
[`THEOREM_TO_SOFTWARE_REGISTER.md`](07_structural_biology/docs/structural_biology/THEOREM_TO_SOFTWARE_REGISTER.md))
and science ([`RESEARCH_SYNTHESIS.md`](03_scientific_translation/docs/science/RESEARCH_SYNTHESIS.md),
[`SCIENTIFIC_FRONTIER_MAP.md`](03_scientific_translation/docs/science/SCIENTIFIC_FRONTIER_MAP.md),
[`PUBLICATION_OPPORTUNITIES.md`](03_scientific_translation/docs/science/PUBLICATION_OPPORTUNITIES.md)).

## 10. Mathematical results that the divisions say may be useful beyond their original application

Only what a division wrote; no assessment was added.

| result | said by | where it says so |
|---|---|---|
| The validation method (independent re-derivation, own code, controls that can fail, predictions written before runs, linked corrections) — "the part of this programme most likely to be reused" | science | consolidation report §F (third text) |
| A guaranteed bracket for a reweighting or free-energy-perturbation estimate (a one-sided floor plus a variance; Hoeffding, Bennett) as a replacement for a standard error — "needs no new mathematics" | science | §D row 1 |
| Certified intervals as an oracle for approximate inference on rotamer models (how often does an uncertified marginal fall outside a certified interval?) | structural biology | §D row 1 |
| Negative controls for ensemble inference: count rules, sparse-label obstruction, tolerance radius — "a cheap, rigorous way to say what cannot be concluded" | geometry | §D |
| Control instances with ground truth for evaluating reweighting tools | ensemble | §D last row |
| A reference oracle for multi-strand thermodynamics, and stress-test instance families with a planted optimum | complexity | §D |
| Evaluation-integrity procedures (freezes with independent time-stamps, sealed lists, tests that fail if a frozen directory is edited) | frontier | §B2 |
| The level theorem needs "four facts about an outer integrand on a probability space and nothing else" (Theorem 11.118) | theory | §B4 |
| Share lemmas and sandwiches as the lemmas under certified free energies | theory | §B3 |
| A differential-testing harness and a ledgered batch driver for bounded cloud jobs | engineering | §D row 3 |

## 11. Existing ingredients that the divisions themselves propose to combine

Again only documented proposals; whether any combination yields a stronger result is the question of a
separate, explicitly authorised phase.

| proposed combination | ingredients named | proposed by |
|---|---|---|
| An end-to-end certified enclosure of `ln Z` for one small protein with every hypothesis checked by a program | theory: `zprune_sound`, `sum_boxFinset_elim`, `sum_boxFinset_relax`, `exp_enclosure`; structural biology: the C2 producer and `FactorElimination.lean`; engineering: independent checker, directed rounding (queue row Q-19); science: cells with their own free energy | theory E2; structural biology E2, E3; engineering E2; complexity E3 |
| A certified second-order bound for many weak pair terms that is actually tight | complexity CX-T35/T36 ([`CERTIFIED_BRACKETS.md`](06_biological_complexity/docs/complexity/CERTIFIED_BRACKETS.md), unreviewed) + a certified third-order remainder (theory's open problem 4) + exact elimination | complexity E3; structural biology E2; theory "State at the halt" (4) |
| "What local and thermodynamic data are worth", as one text | science B2 + theory Proposition 11.104 (the non-adaptive half was "proved independently three times") | science §F item 2 |
| Identifiability of mixtures of chain conformations, as one note | geometry B1 + B2 + hinges (jointly with science's Proposition R22-1) + the obstructions of B4, B5 | geometry §F, E2 |
| Second moments versus distributions of distances | geometry: Theorem F″, block sums; ensemble: E7/E8 (per-edge laws identify where second moments do not; ENSEMBLE-RES-0008 §3) | geometry E1, §B4 "Limitations" |
| The chimera gap: a stability modulus for distance laws | ensemble E4.1 + science's Proposition B + generic global rigidity (geometry) | ensemble E2 |
| Certified ensemble intervals on real averaged data | ensemble E17, E17.2, E23.1, E28, E30 + a forward model with a stated error set (science) + a tool (structural biology or engineering) + protocol and custody (frontier) | ensemble E1; frontier E2 |
| Certified search at solver speed | theory kernel (does it cover a split of a domain into two subsets? frontier's question D-1) + the structural-biology checker + an emitter from the uncertified solver's search | frontier E1; structural biology §D; engineering E1, E3 |
| The error budget on real instances | structural-biology tables (model v2) + science's necessary-optimality construction and referee R28's scripts + frontier's protocols | science E1 |
| Ground-set recognition for rotamer models | complexity B4 would need a `q`-state, sparse-graph analogue; it answers the ensemble division's question E-C1 | complexity §D |

## 12. What is not in the archive

<!-- GEN:excluded -->
| division | file | bytes | reason | git object | SHA-256 |
|---|---|---:|---|---|---|
| structbio | `experiments/structbio/gmec_dev/certs/v2-lib/1UBQ.mincert.json` | 10035244 | larger-than-5-MiB | `1ec678294f77494990a20ccc0f74b4ec48270b17` | `0c9dfbd9392ec930eeddf41ef53ff7a475d09237782e83ecd5f422c242a1ad79` |
| structbio | `experiments/structbio/gmec_dev/certs/v2/1UBQ.mincert.json` | 15901276 | larger-than-5-MiB | `f6c18f9d8192a0379985737fa2221ad3e7306267` | `f1250c338d0fc8342d6c2cf8995fdbde1f15f091064c1a6e6dc9d5b54a981954` |
| frontier | `experiments/frontier/freezes/FRONTIER-FRZ-0002_heldout_commitment_v1/sealed_list_v1.enc` | 2736 | sealed-evaluation-material | `562e85f0682b82616f81d6ab263a5eaaeeb87e84` | not computed (file not read) |
<!-- /GEN:excluded -->

* The **sealed held-out list** of the frontier division is left out and was not read, not even to hash
  it.  Its public commitment, selection rule, query and time-stamp tokens are included
  (`08_frontier_benchmarking/experiments/frontier/freezes/FRONTIER-FRZ-0002_heldout_commitment_v1/`).
  The passphrase and the commitment salt are, by that division's account, held by the research owner
  outside the repository; nothing in the archive contains them.
* Two certificates larger than 5 MiB are referenced, not copied.
* Not in any branch, hence not here: the divisions' untracked caches (regenerable by their account),
  logs of cloud jobs, tool installations.
* Files a division only inherited from the theory branch are not copied a second time.
* A scan of the whole archive found no credentials, no workspace or account names and no local user paths
  ([`11_reproducibility/README.md`](11_reproducibility/README.md) §5).

## 13. Download and verification

```
git clone --depth 1 --single-branch --branch research/consolidated-archive https://github.com/Tommaso-R-Marena/MetricChain.git
python3 MetricChain/consolidated/11_reproducibility/verify_manifest.py
```

or the branch as one compressed file:
<https://github.com/Tommaso-R-Marena/MetricChain/archive/refs/heads/research/consolidated-archive.zip>
(`.tar.gz` in place of `.zip` also works).  Details, and how to retrieve what was left out:
[`11_reproducibility/README.md`](11_reproducibility/README.md).
