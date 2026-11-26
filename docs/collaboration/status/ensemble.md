# Status of the Ensemble Identifiability and Certified Inference Division

*Updated 2026-11-26, about 22:45 UTC (fifth checkpoint; see the commit time).  Branch `research/ensemble-identifiability`.*

## State

**Fifth checkpoint** (ENSEMBLE-MSG-0007, ENSEMBLE-RES-0006; report §7 items 14, 15):

* *The internal review of Part VI (ER3) applied.*  No numbered statement was false.  A
  count of conditions on the torus was false (its conclusion true for another reason);
  thresholds were hand interpolations; a published theorem (Kahle 2010) contains E9(a)
  and supersedes E21 on finite product spaces; E18 is restated with the finite problem
  on the zero set (also asked for by the Geometric Inference Division); the transfer of
  E20′ to chains is withdrawn in the text.  Added from the review: **three states on a
  torus of two angles are never determined by bilinear data** (E22); **five generic
  states on a torus of three angles are** (E20a); a second growth constant and a linear
  weight bound in E20″.  Every Part of the report has now had one review.
* *A sentence we had quoted from the Science division and that it withdrew is out of
  Part IV* (SCI-RES-0037): "only bang-bang members are pinned by averaged data".
* *Proposition E15U* (the exact condition for the thermal union bound): its main
  statement was re-derived and replicated by the Science division (SCI-RES-0038).
* *The checking problem for lifted certificates has a literature*
  (Johnston–Lovitz–Vijayaraghavan 2023; pointed out by the Geometric Inference Division):
  certificates by linear algebra for generic instances, NP-hard for given ones — cited.

**Supplementary directive of the research owner (2026-11-26, received about 22:00 UTC):** a
seventh division (Structural & Computational Biology, Software Development and
Applications; branch `research/structural-biology`) and, for us, constructive forms of the
results, wider observation models, partial identification, software translation and
benchmark design.  Done so far: the initial technical orientation ENSEMBLE-MSG-0006;
`docs/ensemble/SOFTWARE_INTERFACE.md` (a card per result: inputs, outputs, cost, what must
be checked, when to abstain, readiness R3–R0); `docs/ensemble/BENCHMARK_CONTROLS.md` with
eighteen reference instances whose verdicts are verified in exact arithmetic
(`experiments/ensemble/benchmarks/controls_v1.json`) — a specification; execution is the
engineering division's; Proposition E17.1 (correlated noise; an observation function
known up to a uniform error is exactly an enlarged tolerance; a parametric family gives
a certified outer bound).  **The new division's branch was created at about 22:16 UTC at the
theory division's commit `b2caab6`; at 22:27 UTC it still had no commit of its own and no
digest.**

**Fourth checkpoint** (ENSEMBLE-MSG-0005; ENSEMBLE-RES-0004, -0005):

* *Corrections after the second internal review* (`docs/ensemble/reviews/ER2_internal_review.md`;
  report §7 item 10): **Theorem E15T had claimed a false converse** ("the bound holds
  without frustration, and only then") — a violated bond can break the thermal union
  bound and need not; the theorem is restated for positively associated polarised
  members; E15 and E15T are classed "formulation" (a union bound over a monotone
  coupling); the polarised member is defined by the cost into the centre (one-sided
  envelopes); E17's lower constant is `0.335`; E7′ excludes planar bodies; E2.2 says "at
  best a square root".
* *New: the exact condition for the thermal union bound* (Proposition E15U): for binary
  sites and any known part the bound holds for every member iff
  `E[N | U] − E[N | U^c] ≥ 1` under the polarised member for every up-set `U` of the
  disagreement order.  Necessary: each site's disagreement non-negatively correlated
  with the number of the others; sufficient at weak coupling (frustration tolerated if
  every site's bonds are satisfied on balance); not sufficient in general (a three-body
  example in closed form, a four-site pair model).
* *The Science division's independent review of Part II applied* (SCI-REV-0020; report §7
  item 9): joint genericity, two obstruction examples of theirs, a stability statement
  of theirs, novelty classes lowered.  Its SCI-RES-0032 on E15 applied (item 11).
* *The Complexity division's results recorded in §4.2* (COMPLEXITY-RES-0003, -0007, -0008),
  with a table: at `n = 12` almost every identified support beyond `K ≈ n/2` has no
  certificate of degree 2.
* *A mechanical check of quoted numbers* (`experiments/ensemble/check_quotes.py`, run last
  by `run_all.py`).
* **Not yet done:** the corrections inside Part VI that GEOMETRY-RES-0005 and
  COMPLEXITY-RES-0007 require (obligation OB20) wait for the internal review of that
  Part, which is running.  The conditional transfer of E20′ to chains is withdrawn
  (ENSEMBLE-RES-0004 §3); the report's paragraph still carries it.

**Third checkpoint** (`docs/ensemble/ENSEMBLE_REPORT.md` version 3, Part VI; ENSEMBLE-MSG-0004):

* *Lifted certificates* (E18): one construction behind our cube certificate, flat
  extensions and the geometry division's chain certificate; identification also when the
  certificate's zero set exceeds the support.  Three conformers on the cube now have a
  proof without a citation.
* *A prior on the number of conformers* (E18′, E19(c)): with pair data, `(1−ε)n²/2` random
  conformers are determined among ensembles with at most as many conformers (generic
  weights); among all ensembles nothing is beyond `2n`.
* *Data of even order `≤ 2d` on the cube* (E19): `(1−ε)n^d/d!` random conformers are exactly
  the ground states of an explicit energy (the probabilistic core is Baldi–Vershynin 2019,
  **which we re-derived before finding it — cited, not claimed**); nothing beyond
  `2n^{2d−1}/(2d−1)!`; numerically the four-body threshold is 2.6–3.5 times the
  sum-of-squares range (Conjecture C3).
* *Tori of torsion angles* (E20, E20′): generic `K ≤ 2^r − r − 1` atoms are determined by
  multilinear trigonometric data; two states iff they differ in two angles, with an
  explicit certificate (an answer, on the torus model, to SCI-RES-0029 §3 (b)).
* *After the checkpoint* (E20″): the two-state certificate has quadratic growth with an
  explicit constant (`min(1, β_min/4)` for three or more differing angles), which gives a
  stability bound `∫ min(d_p², d_q²) dν ≤ Λτ/c*` and the weights within `O(√τ)`, every
  constant computable; the growth inequality is machine-checked.  And (E21) for `K` states
  that satisfy a Hall condition — for instance pairwise at least `K` differing angles — the
  permanent of the coordinate-wise distances is a certificate; its zero set is
  machine-checked through Mathlib's Hall theorem.

**Second checkpoint** (`docs/ensemble/ENSEMBLE_REPORT.md` version 2).  Added to the first
checkpoint (Theorems E1–E12: identified = exposed; the bridge to theory report Theorem 2.4;
distributional ensemble rigidity = global rigidity; pair data on the cube):

* *Finite temperature* (Part IV): a first-order class is a polytope (E13); **a thermal union
  bound** — `TV(μ, μ*_a) ≤ Σ_i [μ*_{a,i}(a_i) − μ(x_i = a_i)]` for every member, dimension-free,
  core machine-checked (E15); its extension, with the same constant, to every known part
  that is log-supermodular in the disagreement variables (any graph, any range, every
  bond satisfied by the centre), and its failure under frustration (E15T); a bimodal
  ensemble identified by one pair observable (E16).
* *Noise* (Part V): minimax risk = modulus = dual certificate (E17).
* *Laws of observables*: rigid-body ensembles — seven legs in space (E7′); the square-root
  modulus on continua (E2.2, the science division's).
* *Pair data*: nothing identified beyond `2n` conformers (E11(a)); the threshold is
  numerically between `1.1n` and `1.2n` (§4.4, Conjecture C2; exact decisions up to 20
  sites).

**Internal adversarial review of version 1 applied** (`docs/ensemble/reviews/ER1_internal_review.md`):
no numbered statement was found false; five sentences around the theorems were
(report §7 item 6), among them "identified exactly when exposed" and "identification =
absence of chimeras".  The linked correction of the first checkpoint is ENSEMBLE-MSG-0003
§2 and §2a.

## Synchronisation record (read-only)

| division | branch | last commit read | what was read |
|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `6ebcccd` | THY-MSG-0018 §3 in full (at `7f879d4`); since then commit titles and the list of changed files only — no new collaboration file |
| science | `research/scientific-translation` | `4661a03` | in full: SCI-REV-0020, SCI-RES-0032, SCI-RES-0036, SCI-RES-0037, SCI-RES-0038; SCI-MSG-0033 §§1, 2.2 in full, the rest by its headings; headers only: SCI-REV-0021, -0022, -0023, SCI-MSG-0031, -0032, -0034, SCI-RES-0033, -0034, -0035.  Its protocol for evaluating structural-biology software (checkpoint 65) not read |
| engineering | `research/ubuntu-engineering` | `c683fde` | the change of its protocol copy (seven divisions; how software benchmarks are reviewed before execution); its queue not read |
| geometry | `research/geometric-inference` | `b0734aa` | GEOMETRY-RES-0005 and GEOMETRY-MSG-0008 in full; GEOMETRY-MSG-0006 §1 and GEOMETRY-MSG-0007 §2 in full; GEOMETRY-RES-0006 header only; its report only through these messages |
| complexity | `research/biological-complexity` | `75266b2` | COMPLEXITY-RES-0003, -0007, -0008 in full; COMPLEXITY-MSG-0004 where it names us; COMPLEXITY-MSG-0005 (its orientation for the new division) header only |
| structural biology | `research/structural-biology` | `b2caab6` (the theory division's commit at which the branch was created) | absent at 22:00 UTC; present at 22:16 and 22:27 UTC with no commit of its own and no `STRUCTURAL_BIOLOGY_TO_ALL.md`; nothing to read yet |

## Verified state at the head of the branch

* Lean: `proofs/Ensemble/Exposedness.lean`, `RenyiHeppes.lean`, `ThermalUnionBound.lean`,
  `TwoStateCertificate.lean`, `PermanentCertificate.lean`; twenty-four headline theorems
  and eight non-vacuity witnesses listed in `proofs/AxiomAudit.lean` (the eighth, for the
  density form of the thermal inequality, was asked for by the review ER2).
* **The programme's full audit** (`scripts/audit_all.sh`: self-tests with planted
  violations, `lake build` (8653 jobs, no warning), token scan, axiom walk — 5145
  declarations, standard axioms only —, falsification harness, 552 mutation tests,
  separation benchmarks, reference checker, documentation references) **passed on the
  tree of this checkpoint** ("AUDIT PASSED").  The documentation-reference stage was
  re-run after the last edits of the documents.  Files of other divisions changed here:
  only `proofs/AxiomAudit.lean` (imports, `#print axioms` lines and witnesses appended) and
  `docs/collaboration/README.md` (an addendum).
* Numerics: `python3 experiments/ensemble/run_all.py` — seven scripts (the last regenerates
  and verifies the benchmark controls), then `check_quotes.py` (every number quoted in a
  "Numerical check" passage of the report is the one in the stored output): all pass
  (`experiments/ensemble/output.txt`).  Threshold computations and the degree-2 table:
  `output_threshold.txt`.  `proofs/` is unchanged since the audit of the fourth checkpoint.

## What is and is not reviewed

| part | status |
|---|---|
| Lean statements | kernel-checked; the statements of `ThermalUnionBound.lean` were compared with the report by the review ER2 (they match); the others were read by the author only |
| Parts I–III (version 1) | internal adversarial review ER1 (a subagent of this division; AI review, not peer review): every numbered statement confirmed, five major and thirteen minor corrections, **all applied**.  Part II also reviewed independently by the Science division (SCI-REV-0020: every step re-derived, no gap; four major and ten minor findings on what the statements may be read as, **all applied**) |
| Parts IV, V, E7′, E2.2, E2.3, §4.4 (version 2) | internal adversarial review ER2 (same kind): no critical defect; four major findings — among them a false converse in E15T — and twelve minor, **all applied**; E15 replicated by the Science division with its own code (SCI-RES-0032) |
| Proposition E15U | main statement re-derived and replicated by the Science division (SCI-RES-0038); the other three characterisations and the consequences **read by nobody but the author** |
| Proposition E17.1 (observation models) | immediate; **read by nobody but the author** |
| Part VI (version 3; E18–E21) | internal adversarial review ER3: no numbered statement false; two major and nine minor findings, **all applied**; five cited sources read in the original by the reviewer.  The statements taken from the review (E20a, E22, two constants of E20″) were re-derived by us and **read by nobody else** |
| prior art | `PRIOR_ART.md`: first-checkpoint searches; the sources of ER1 and ER2 with the level at which each was read; two searches for E15U; Part VI: two cited theorems read in the sources, the rest unsearched (OB16) |

No external peer review of anything.

## Open questions to others

Open: E-T1, E-T2 (answered in part by THY-MSG-0018), E-T4, E-G4 (no constant known),
E-C1 for `K ≫ log n` (open on the Complexity division's side too).  Closed since the third
checkpoint: E-S2 (SCI-REV-0020), E-S3 (withdrawn after SCI-RES-0032), E-S4 and E-G5
(GEOMETRY-RES-0005), E-G2′ (its body–bar count), E-T3 (THY-MSG-0018; the exact condition is
now our E15U), E-C1 for fixed `K` and `K = O(log n)`, E-C2 at the level of an interpolation
bound (COMPLEXITY-RES-0003, -0007, -0008).  See `ENSEMBLE_TO_ALL.md`.

## Resource use

No shared Modal computation requested or used.  Local computation only (several
CPU-hours in total, most of it the exact threshold decisions of §4.4 and §4c.3; one such
run, four-body data at `n = 14`, is still in progress on one core).  Three internal
reviews by subagents of this division (ER1, ER2 reported; ER3 running).
