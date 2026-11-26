# Research intake of the Structural & Computational Biology division

Living document of the Structural & Computational Biology, Software Development and Applications
division (STRUCTBIO), branch `research/structural-biology`. It answers §4 of the founding
directive (`OWNER_DIRECTIVES.md`, SB-D-1): what the other six divisions have built, at what
status, and what this division takes from it. Per-result records are in
`THEOREM_TO_SOFTWARE_REGISTER.md`.

## 0. Header

- **Date:** 2026-11-26 (first synchronisation).
- **Branch point:** theory commit `b2caab6` ("Cycle 10, twenty-third checkpoint …"). The Lean
  sources, reference checker, conformance vectors, audit scripts, toolchain pins and
  `docs/BLUEPRINT.md` are identical at `b2caab6` and at the theory head `eb88823`
  (`docs/collaboration/STRUCTBIO_UPSTREAM_SYNC.md`).

**Heads inspected** (copied from `STRUCTBIO_UPSTREAM_SYNC.md`):

| division | branch | head commit | head date (git) | intake report(s) |
|---|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `eb88823c931953d6455f79c9d8089063abfb442b` | 2026-11-26 21:37 UTC | T1, T2 |
| engineering | `research/ubuntu-engineering` | `96c4fd22258646fd7500cbe50eb6450ae011afcf` | 2026-11-26 21:55 UTC | E |
| science | `research/scientific-translation` | `71bc661903cc40b0044bdc109f2f07963ba8f357` | 2026-11-26 21:49 UTC | S1, S2 |
| ensemble | `research/ensemble-identifiability` | `8d42f609b8bd16a308275cf68856f3cf0460a6e1` | 2026-11-26 20:25 UTC | N |
| geometry | `research/geometric-inference` | `288b2def39ae1bba0afabad0151e275b3a5cdbbc` | 2026-11-26 20:10 UTC | G |
| complexity | `research/biological-complexity` | `25bcd61d362ee860bf02845f062b150314aa916b` | 2026-11-26 21:50 UTC | C |

**Method.** Eight read-only reviewers (subagents of this division) each read one slice in a
confined read-only worktree and wrote one intake report (`intake/`). This document was written
from those reports. **An intake report is a reading, not a verification.** Everything below is
"per intake reviewer, not re-verified" unless it appears in the following list.

**Checked by the coordinator in person:**
- the reference checker's (`experiments/reference_checker.py`) semantics for the `min` and
  `partition` kinds, read in full; this division's checker agrees with it on 288 mutated
  certificates;
- `docs/BLUEPRINT.md` §§1–6.5a and 8–11, read;
- the definitions `ZCert2`, `zverify2`, `Elim1OK`, `Elim2OK`, `CutOK` and the statement of
  `zverify2Top_sound` in `proofs/Frontiers/PartitionProduct.lean`, read;
- the statements `free_energy_sandwich` and `partition_ratio_sandwich` in
  `proofs/Frontiers/FreeEnergySandwich.lean`, read;
- `lake build proofs.CertificateAlgebra proofs.Frontiers.PartitionProduct` succeeds at `b2caab6`
  on this division's machine (Lean 4.31.0, Mathlib v4.31.0; 8563 jobs).

The full `scripts/audit_all.sh` has not been run by this division.

**Labels.** Status labels are copied from the repositories: [V] machine-checked, [P] paper proof,
[K] known/cited, [N] numerical, [C] conjecture; science adds [M] (measured on a named model) and
[H] (heuristic); engineering adds [X], [X\*], [R], [S], [E]; geometry uses "P-exact". Every review
named below is an **internal review by an AI session or subagent, not external academic peer
review**. That holds whether the reviewer was the same division (REV-, ER1, R-series) or another
one (SCI-REV-).

## 1. The six divisions

### 1.1 Theory (T1, T2)

**What exists.** A small verified core of computable Lean kernels with soundness theorems
(T1 §1):
- K1, `verify` / `verify_sound`: a lower bound on the minimum energy of a pairwise rational
  instance on a box. Its rules are leaf (LP dual), branch, Goldstein prune and sum.
- K2, `verifyITop_sound`: the same bound under an unknown residual in an envelope class.
- K3, `zverifyTop_sound`, and K3′, `zverify2Top_sound` with cut/elim1/elim2: two-sided bounds on a
  partition sum.

Lean-only layers sit on top: split, linear residual and barriers. There is also a numeric layer
(`exp_enclosure`, `QInterval`) and theorems over ℝ (share certificates, voxel bridge, macro
ratios). All of these are [V] by the repository's label. T1 could not build them; the coordinator
built two modules (§0).

**What runs.** Only the Python reference checker runs on external certificates, for
`min`/`residual`/`partition`. It is declared untrusted (BP:1280) and is related to Lean "by tests,
not by proof" (T1 §3). Lean has no executable target, `native_decide` is forbidden, and kernel
evaluation of `verify` exhausted 11.9 GB at 512 table entries (T1 §3; T2 A1). **No certificate
producer exists** (T1 §2.12). The JSON schema has no `split`, `cut`/`elim`, linear or barrier
nodes (T1 §2.11). T1 found that no conformance vector or fuzz case contains a `sum` node (T1 §3).

**What has run on what.** "Nothing in the theory branch has been run on a real PDB structure." Its
most realistic data are the science division's [M] measurements on synthetic peptides
(T2, framing fact).

**Review.**
- Referee R1 read the statements and did not check the build or the reference checker (T1 R1).
- R2 refereed §§11.1–11.9, with reservation M4 (D33).
- Many later sections are "not refereed" (T2 F.14).
- Novelty was reviewed by science in SCI-REV-0006 (§1.3).

**Decision-relevant negative results** (T2 §C, §D):
- D42 / Thms 11.36–11.37: per-torsion constants cannot certify long chains. Certify side chains on
  a fixed backbone.
- D28: first-order classes have an exponential price for every algorithm.
- Thms 11.31–11.32, D32, D40: dense second-order classes cost `2^{n−o(n)}`.
- "Measured constants are not certified ones" (T2 C4).
- D56 item 3: sampling statistics are not certificates.
- D22, D33: partition-kernel limits, `2ⁿ` leaves on a chain without cut/elim.
- D15, D16: soundness hygiene; only the `…Top` entry points are safe.
- AA1 E8: voxel enclosures are "vacuous beyond a handful of coupled continuous coordinates".

**Open items that overlap our mandate** (T2 §F):
- a producer and a scalable checker with a refinement proof (§12 item 7);
- a measured comparison with pseudo-Boolean proof logging (§6.4);
- interval evaluation of force-field terms;
- certified envelope constants for any real energy term;
- non-product (clash-pruned) domains.

### 1.2 Engineering ("Ubuntu") (E)

**What exists.**
- X-012 `leafcert` (Q-04, campaign BM-2): an exact two-engine (C and Python) checker for the
  science division's "shares at the leaves" format, the leaf/branch rules of `verify`. Code
  `0e5103b`.
- Validation [X] on nine science files; fuzzing found 0 unsound acceptances in 246,842
  certificates (E C.2).
- The format is dense and full-product. The reviewer estimates that a 300-residue protein is
  above its C limits.
- No producer is on the branch. A producer job (`leafprod`) was "in flight", untracked, and is
  absent from `96c4fd2` (E C.2).
- Other packages (`twolevel`, `chains`, `weighted_cube`) are of low reuse value for side chains.
  The exception is `sampling.binomial_exact` (E C.3–C.5).

**What has run on what.** Only toy peptide certificates made by the science division (E C.2,
F.1). The reviewer reproduced the leafcert tests in a sandbox without SciPy: 176 passed, 4 failed
and 2 errors, all `ModuleNotFoundError: scipy` (E G).

**Process and budget.**
- Requests go through the mailbox and are judged against readiness criteria R1–R9 and stages A–F
  (E A).
- The owner authorised up to $1,750 of Modal spending under D-5 (E B.1).
- There is **no allocation, mention, queue row or readiness row for a seventh division** (E B.6).
- The hard stop is 2026-11-30 15:00 US Eastern (E B.5).

**Dead ends and pitfalls** (E F):
- ED-8: numpy's binomial sampler is biased from about 10¹⁵ trials.
- ED-5: floating-point ties.
- 64-bit wrap-around would have accepted false bounds in the leafcert edge tests.
- Five corrections of its own record, including solver bounds that had been reported as
  certified.

**Open items overlapping ours** (E D):
- E-1, "what is actually trusted", planned;
- E-2, "what a native `min` certificate costs at realistic sizes", planned and not started;
- Q-14 / BM-2 stages C–E, "not ready: needs a producer and a written baseline specification";
- SCI-RES-0014 P7-E1, a producer, open;
- Q-08 (science P3-E1/P6-E1), a sandwich-certificate checker, "not ready for an independent
  checker";
- the real-peptide requests, blocked on R5 ("an evaluator of the energy").

### 1.3 Science (S1, S2)

**What exists.** A research pipeline for certified brackets of `ln Z` of ff14SB + GBn2 rotamer
models on chains, using banded transfer matrices (S1 §0):
- P3 Theorem 3: certified sandwich.
- P6: shares.
- P8/P9: state-wise and state-resolved tables.
- A17.19 / A17.23: recovery.

Its logical skeleton is machine-checked: `remainder_identity`, `anchored_sandwich`,
`GibbsRecovery.lean`, `ResolvedPenalties.lean`. Its constants, tables, evaluator and arithmetic are
[P] or [M], in "unreviewed research code" (S1 A.6–A.7).

There is **no free-energy certificate file and no independent checker** (S1 A.7, B). The
division's obligation G-3 (tree decompositions) is "not written, not built" (S1 G.7). Its only
GMEC-type artefact is P7 "shares at the leaves": integer certificates in units of 2⁻⁴⁰ kcal/mol
whose instances rest on measured class constants (S1 A.7, H5).

**What has run on what.** **No division has used a real protein structure.** Science's
real-force-field work is ff14SB + GBn2 (OpenMM 8.6.1, GBn2 polarisation only) on **synthetic capped
homopeptides**, `Ace-Xₙ-NMe` and one patterned peptide `LKSE:n`, on uniform ideal backbones with a
three-state grid per dihedral. In the division's words: "no structure file, no rotamer library
from a database, no sequence varied or optimised" (S1 §0, A.2). "PDB" occurs nowhere in its docs
(S1 D). The largest headline result is the Val₂₀/PPII bracket
`ln Z(E) ∈ [518.2332, 518.2937]` (S1 A.6).

**Review.**
- R3, R8, R19 and R24 are internal reviews of the division's own work.
- R14 was "terminated by a platform safeguard".
- Addenda A17 (13)–(18) and (24) are unrefereed (S1 A.7, S2 C).
- Science reviews other divisions on request: SCI-REV-0006 (novelty of the kernels), -0019,
  -0020/-0021, -0022 and -0023 (S2 E).

**Decision-relevant negative results.**
- SD45 / SCI-REV-0012 §5: on pruned non-product domains the certified minimum missed the
  clash-free minimum in 14 of 40 analyses (S1 A.3; S2 A).
- SD19: no pairwise known part in backbone torsions.
- SD47 / P5: sign-blind bounds lose 16–153×.
- Floor delocalisation: (LKSE)₃ at order 3 has "no certificate (658.9 nats)".
- The gap between certified and measured constants is 33–1,400× (S1 A.5, A.8).
- Model error is larger than certified width by "four or more orders" (S1 C; reviewer's
  inference).

**Benchmarks.** B2 (certificate cost on public side-chain networks) and B5 (is the certified
minimum meaningful?) are designed and show "nothing yet" (S1 D; S2 §0).

**Prior-art verdicts** (S2 A):
- min kernel: class (7) narrow, "every rule is known; no proof logging for cost-function
  networks / MAP found";
- residual kernel: (7), "found to have none" (SCI-REV-0006 M1);
- partition kernel: (5) new combination.

No file in the repository mentions SCWRL, FASPR, Rosetta's packer or an ML packer (S2 §0;
T2 E for theory).

**Open requests overlapping ours** (S1 F):
- P3-E1 = P6-E1, a sandwich checker;
- P3-E2, a GBn2 evaluator with a proved rounding bound;
- P2-E1, a buried environment on a public structure;
- P7-E1, a producer;
- E-1 of SCI-REV-0006 §7, native kernel against pseudo-Boolean proof logging, "accepted", not
  done.

### 1.4 Ensemble identifiability (N)

**What exists.** An exact, finite-dimensional, linear-information theory of identifiability
(N §0, B):
- E1/E1.1: identified iff the support is the full zero set of a non-negative function in the data
  span. The "if" direction is [V] (`eq_of_exposing_certificate`), as is the mass bound
  (`mass_off_support_le`).
- E2/E2.3: one conformation; forward-model error enters as a supremum.
- E13: flow certificate in a first-order class, [P].
- E17: modulus = dual certificate = near-minimax estimator, [P].
- Torus results E20′/E20″/E21, with Lean cores.

The Lean code is 24 headline theorems plus 7 witnesses in 5 modules, on finite types only (N D).
The Python is LP scripts on SciPy/HiGHS (N D).

**What has run on what.** Synthetic instances only. The division states: "What is *not* in this
report: anything about real instruments" (N §0). It names no NOE, RDC, J-coupling, SAXS, DEER,
FRET or cryo-EM data (N A).

**Review.**
- ER1 (internal) covers Parts I–III: no numbered statement false.
- Parts IV–V, E2.2, E7′ and §4.4 are "ER2-pending".
- Part VI (E18–E21) "has been read by nobody but its author" (N §0).
- SCI-REV-0020 is accepted but unpublished.

**Dead ends.** ED12 ("identified ⇔ exposed" false in both directions), ED15 (Baldi–Vershynin
rediscovered), ED16 ("a grid LP … proves nothing when it does not [find a twin]") (N E).

**Open items.**
- No requests to engineering (N §0).
- Prior art not searched: MaxOcc / ensemble refinement, BME, EROS, Kruskal-type identifiability
  (N F).
- O4: no modulus under banded laws.

### 1.5 Geometric inference (G)

**What exists.**
- Identifiability of discrete-state ensembles from averaged squared distances under exact,
  state-independent bond geometry: Theorems A, B/B′, C (thresholds), F (stress certificates),
  G (W₂ stability, κ uncertified), H (local Jacobian rank), I, J (laws), M (hinges).
- Single-structure local-data bounds: Theorems K and L.

Lean covers cores only, for example `stress_certificate` and `mixture_identifiable_stacked`, which
do not treat weights (G B). The code is `geomlib.py` and exact mod-p rank scripts (G D).

**What has run on what.** Synthetic chains with homogeneous geometry. There is "no I/O for PDB"
(G D). The division's scope is "mathematics and synthetic systems only" (G A).

**Review.**
- REV-0001 (internal) covers work up to `e8e2582`. Theorems G′, K, L and M are not covered.
- SCI-REV-0021 reviewed B, B′ and G.
- SCI-REV-0023 is a prior-art and relevance review of Theorem L: "Nobody in this division reviewed
  the proof of Theorem L". It finds Theorem L's guarantee vacuous at physical noise. On an α-helix
  Cα trace, condition (S) needs distance errors ≈ 1.3·10⁻⁴ Å (G B12).

**Dead ends** (G E):
- DG-7: DEMIX auto-K fails at noise 10⁻⁴.
- DG-10: local ≠ global identifiability.
- DG-13: a false slogan.
- DG-19: an unproved exponent was published.
- DG-20: priority loss.

**Open items.**
- O-5: certified κ.
- GEOMETRY-REQ-0001 is Q-12 at engineering, "in progress".
- GEOMETRY-REQ-0006 has no response.
- No mention of FIRST/KINARI, the molecular conjecture, DMDGP or NMR structure calculation (G F).

### 1.6 Complexity (C)

**What exists.**
- Nucleic-acid strand hardness and algorithms (STRANDS).
- Phylogenetic-network metrics (NANUQ).
- Ising ground-set theorems: binary spins, complete graph; CX-T16–T19, T28/T29.
- Penalty-threshold brackets: CX-T21–T23, product reference.
- A certify-in-exact-rationals LP pattern (`span_algorithm.py`).

The labels are [P], [X] and partly [V] (C B, D).

**What has run on what.** "Abstract combinatorial models … synthetic instances only" (C A).

**Review.** COMPLEXITY-REV-0001…0004 are internal, and SCI-REV-0019 is from science. CX-T21–T23,
T25, T26–T29 and the T30 write-up are unreviewed (C E).

**Relevant negatives** (C E):
- The KP criterion is "void" on science's four floors.
- λ₀ is only 0.10–0.16 of the measured transition (SCI-RES-0034).
- Hard instances of the degree-2 reduction "are exposed", so they say nothing about the hardness
  of "exposed?".

**Open items.** No requests to engineering (C E). None of the open items addresses q-ary rotamer
models.

## 2. Cross-cutting findings

### 2.1 Gaps this division fills

- **Theory:** "No certificate producer exists in this worktree" (T1 §1.3). Our C1 producer is the
  first.
- **Engineering E-2:** "what a native `min` certificate costs at realistic sizes", planned and not
  started (E D). We build the producer and the structure pipeline. The split proposed by E is that
  engineering does the independent checking and benchmarking (stages A/B/D/F).
- **Science B2 and B5:** designed, not run (S1 D). C1 and C1b supply the instances and the
  certificate side.
- **Q-14 / BM-2:** needs "a producer and a written baseline specification" (E D). We supply both
  as a request.
- **Real-peptide request blocker R5:** "an evaluator of the energy this division can run and
  check". Reviewer E's reading is that "STRUCTBIO is the natural owner" of structure ingestion and
  the evaluator (E D), coordinated with science, which owns the requests. This is a reviewer's
  suggestion, not a decision of this intake.

### 2.2 Overlaps to avoid duplicating

| item | owner | how we stay clear |
|---|---|---|
| E-1 "what is actually trusted" (Lean definitions run on certificates vs the reference checker; ENG-RES-0004) | engineering, planned | we supply certificate files and our format; engineering does the differential test |
| E-2 / Q-14 / BM-2 benchmarking | engineering | we produce; engineering checks, replicates and measures |
| Q-04 `leafcert` (X-012) | engineering | used as an external backstop, not rewritten; a sparse / restricted-domain extension would be requested, not built here |
| Q-08 sandwich checker (P3-E1 / P6-E1) | engineering for science | C2 needs a file-based format too; we write a specification for our kind and do not build a checker for science's sandwich |
| P7 shares-at-the-leaves certificates, P7-E1 producer | science / engineering | our `min` format differs (prune nodes, per-site domains); before claiming P7-E1 we ask whether `leafprod` will appear (E D) |
| B2 / B5 benchmark designs | science | we implement against science's designs and cite them |
| P3–P9 free-energy line | science | C2 is the general-graph counterpart and must not be presented as replacing its residual-class results |

### 2.3 Inconsistencies in other divisions' records

These are observations to send to their authors. They are not accusations, and the reviewer who
found each one is named.

- **Engineering:**
  - the ledger's "total authorised" row reads committed $0 and spent $0.07, stale against the first
    row (E B.3);
  - `status/engineering.md` says "153 tests", which predates leafcert's 182 (E C.1);
  - `DEPENDENCY_MAP.md` "Not yet connected" is stale relative to X-012 (E F.1);
  - `BENCHMARK_READINESS.md` says "ensemble / geometry / complexity — no request received" while
    GEOMETRY-REQ-0001 is registered as Q-12 "in progress" (E A.9; G E).
- **Ensemble:** the "Resume here" section of `RESEARCH_LOG.md` says "three modules, twelve headline
  theorems", while `status/ensemble.md` says five and 24 (N D). An `n = 22` row is in
  `output_threshold.txt` but not in the text (N B, C2).
- **Geometry:** `experiments/geometry/README.md` says "31 tests", "19 planted errors"; the current
  numbers are 41 and 29 (G D).
- **Complexity:**
  - `HANDOFF.md` calls items "Unreviewed" that `THEOREMS.md` records as reviewed;
  - `NANUQ_HIGHER_LEVELS.md` cites CX-T31 and CX-X3, which are absent from `THEOREMS.md`;
  - Q-CX1 is answered but not registered (C A).
- **Theory:**
  - no conformance vector or fuzz case contains a `sum` node, and no stored vector contains a
    partition `prune` (T1 §3);
  - benign differences between BLUEPRINT and the reference checker: lowest terms not enforced,
    full `h` required in `sum` parts, CBOR absent (T1 §2.11);
  - the checker accepts `lower_bound = 10⁶` on an empty domain (a true statement about an empty
    box) and ignores a witness outside the box (T1 §7.9);
  - SCI-REV-0022 found that the audit tag `{P}` cannot be trusted: 2 of 12 sampled are false
    without the assumption (S2 A).
- **Science:**
  - E reports that `p7_06_check.py` can return True for a false bound on malformed input; S1 records
    this as fixed at `70f208e`. **The two reports disagree** (§4);
  - `slack_recovery.bounds` "tests neither finiteness nor lower ≤ upper" (S1 B);
  - a reference-cycle leak in `p5lib.anch_walk` is "still present" (S1 B).
- **Identifier collision:** "E-1" names both engineering's trust item and SCI-REV-0006 §7's native
  vs pseudo-Boolean comparison. Science's `OPEN_PROBLEMS.md` calls the latter E2 (E D; S1 F;
  S2 D). Our messages will cite both by source.

### 2.4 Science's recorded directives and our founding directive

Reviewer S1 notes a tension (S1 E). Science's D-1 says "Extensive application-specific
benchmarking will be undertaken during a subsequent research phase". Its D-2 says "Do not
independently consume the shared Modal budget through substantial new workloads without
authorization". Both pull against a benchmark campaign. Science's `OWNER_DIRECTIVES.md` records
six divisions, not seven.

Our founding directive (SB-D-1 §§11–17) commissions retrospective evaluation on public structural
data. It also says: "You may conduct inexpensive local unit tests and smoke tests. Substantial
shared computation must be requested through Ubuntu".

**Our reading:** this division designs and runs local unit, smoke and development-scale
experiments. Substantial computation is requested from engineering under its readiness rules, and
we do not launch it ourselves. We do not read SB-D-1 as changing science's directives for
science.

## 3. Capability decisions

The table records the decisions of this division (coordinator); the reasons are summarised.
Rows per result are in the register.

| id | capability | decision | reason |
|---|---|---|---|
| **C1** | certified GMEC on fixed-backbone rotamer models (K1 `verify`/`verify_sound`; leaf/branch/prune; kind `min`) | **taken forward; implemented at the first checkpoint**: producer (`gmec.py`: DEE + MPLP dual bound + branch and bound), compact format with exact conversion to `metricchain-cert/1` (`mincert.py`), independent integer checker (`mincheck.py`), differential tests (`tests/structbio/test_mincert.py`) | nearest implementable target (T1 §1.4); fills theory's missing producer, E-2 and B2/B5. **Novelty:** every rule is known (SCI-REV-0006); pseudo-Boolean proof logging (VeriPB) is the competing certificate technology; the comparison has never been measured (T2 A1; S2 A) |
| **C1b** | certified per-residue stability of the GMEC: certified gaps for changing one residue's state; the largest uniform bounded-difference perturbation under which the incumbent provably stays optimal | **planned next; design** | uses only K1: one `min` certificate on the anchored model (BLUEPRINT §6.6 step 1; `robust_certified_iff`, `single_evaluation_certificate_iff`); answers B5's "is the certified minimum meaningful" and S1's recommendation G.8 |
| **C2** | certified partition functions, free energies and rotamer populations on pairwise rotamer models (K3, K3′, numeric layer, `free_energy_sandwich` / `partition_ratio_sandwich`, `boltzmannAvg_prune_error`) | **taken forward; in progress** | see the obstruction below |
| **C3** | ensemble partial-identification certifier on finite conformer libraries (ensemble E1, E1.1, E2.3, E13, E17; science Theorem 8 and identified sets) | **priority 2** (next cycles) | exact-rational LP certificates for identified / not identified / range of a target; prior art MaxOcc, BME, EROS (novelty not established); a forward-model error budget is needed before any real data |
| **C4** | geometric observability analyser (geometry Theorems H, K, L, M; `geomlib`) | **priority 3** | flags what a pattern of distance data cannot determine; **not** a uniqueness certifier for experimental restraints (κ of Theorem G uncertified; Theorem L vacuous at physical noise per SCI-REV-0023) |
| **C5** | residual-class / robust certificates on real energy terms (K2 `verifyITop_sound`; `StateShares`, `ThirdOrderModel`; science P-series) | **blocked** | no certified constant exists for any real energy term; "measured constants are not certified ones" (T2 C4). Revisit only with interval evaluation of a force-field term |

**The C2 obstruction.**
- The verified exact rules stop at treewidth 2, because the instance type is pairwise. Eliminating
  a site with r ≥ 3 neighbours creates an r-body factor that `WInstance` cannot hold. Treewidth ≤ 2
  in general is [P]; every chain is [V] (T1 §4.5).
- Thermal pruning cannot precede a cut or an elimination in `ZCert2`.
- `cut` and `elim` are not in the JSON schema or the reference checker.
- The unrounded certified exponential yields rationals of 10⁴–10⁶ bits (T1 §4).

This division therefore specifies an extension with its own checker:
- general elimination on factor tables;
- a product-form relaxation of weak pairs;
- pruning before elimination;
- outward-rounded weights.

The extension goes to the theory division for review and, where practical, is machine-checked by
us in Lean.

Science's certified free-energy line (P3–P9) is chain- and band-only, on synthetic peptides, with no
file format and no independent checker, and its G-3 is "not written, not built". C2 is the
general-graph counterpart and does not replace science's residual-class results.

**Not translatable now:**
- query-complexity and exponent theory (idealised classes, asymptotic);
- voxel and continuous-rotamer enclosures (no interval evaluation of force-field terms);
- barrier and macro-ratio certificates (no kernel or checker entry point; certificate sizes);
- the linear/profile kernel (class too small, constants vacuous);
- STRANDS and NANUQ (nucleic acids, phylogenetics);
- the Ising ground-set theorems (binary, complete graph), except as design heuristics;
- the ensemble and geometry positive identifiability theorems that assume exact idealised
  observables.

Reasons and the conditions that would change each verdict are in Part B of the register.

## 4. Limits of this intake

The reports disclose these limits themselves:

- **T1:** no `lake build` and no audit, because no Lean toolchain was installed; every [V] is the
  repository's label. Definitions and main statements were read, not proof bodies, outside the
  files listed in T1's "Done". T1 ran the reference checker's self-test, all 16 vectors and six
  probes of its own.
- **T2:** confined to the results table, audit, dead ends and prior art; kernel code was left to
  T1. Line numbers refer to `eb88823`.
- **E:** ran leafcert outside the tree without SciPy, so the LP producer, mutation and broken-copy
  tests did not run (176 passed, 4 failed, 2 errors). E did not run Lean.
- **S1:** read about 40 % of the P-series reports (`SP_REPORT.md`, `P2`–`P9`). For `SK`, `SF`, `SM`
  and `SX` it read verdicts only, and for several messages digest entries only. **No script was
  run**: OpenMM, numexpr, SciPy and mpmath were absent. S1 did not verify the citations.
- **S2:** its list of missed competitors is from the reviewer's memory, "unverified here, no network
  used".
- **N:** no `lake build`, and the Python could not be re-run (no SciPy). Every number comes from
  recorded outputs.
- **G:** nothing was built and Lean was not rebuilt. The one script run was `demix.py`.
- **C:** ran no Lean and no Python.
- **All:** no network. Every prior-art statement is the originating division's or the reviewer's
  recollection, and nothing was re-searched.

**Contradictions between reports that remain open:**
- (a) Seven or nine P7 certificates. E says "Nine files are seven certificates"; S1 says "Nine
  certificates accepted".
- (b) The label of P7's instances: T1 and T2 cite TR as **[M]**; S1 cites science as "[P]".
- (c) Whether the `p7_06_check.py` malformed-input defect is fixed: E describes it in the present
  tense, S1 says it was fixed at `70f208e`.
- (d) S2 §0 lists the partition kernel among two capabilities with no counterpart, while S2's own
  table and T2 A3 class it (5), "new combination".
- (e) C2 uses `free_energy_sandwich` / `partition_ratio_sandwich` for weak pairs "under an
  arbitrary reference". The reviewers place limits on that sandwich:
  - T2 B lists Thm 3.1 (`β²Σc_i²/8`) as not translatable: "Product reference only (D14); for any
    reference, vacuous once `βΣc_i>8`";
  - T1 §6 quotes BP:460: "Do not use the `Σ c_i²` width with a correlated reference: it is false
    there".

  **Resolved by the coordinator on 2026-11-26** (register row A11, field 12): C2 uses only the
  *range form* `partition_ratio_sandwich` — any reference, `a ≤ Δ ≤ b` pointwise, width
  `β²(b−a)²/8` — and never the `Σc_i²` width.  The reviewers' limits stand: the range form is
  vacuous once `β(b−a)` is large, which is what we measured on ubiquitin (RESULTS R-3).

## 5. Pointers

- Intake reports, all dated 2026-11-26:
  - `docs/structural_biology/intake/T1_theory_kernels.md`
  - `T2_theory_results.md`
  - `E_engineering.md`
  - `S1_science_forcefield.md`
  - `S2_science_priorart.md`
  - `N_ensemble.md`
  - `G_geometry.md`
  - `C_complexity.md`

  The same folder also holds `MOLECULAR_LAYER_REPORT.md`. That is this division's own
  implementation report, not an intake report.
- Register: `docs/structural_biology/THEOREM_TO_SOFTWARE_REGISTER.md`.
- Upstream pins: `docs/collaboration/STRUCTBIO_UPSTREAM_SYNC.md`.
- Founding directive: `docs/structural_biology/OWNER_DIRECTIVES.md`.

This document is updated at each synchronisation. A changed status gets a dated line here and in
the register; nothing is rewritten silently.
