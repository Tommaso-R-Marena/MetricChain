# Status of the Ensemble Identifiability and Certified Inference Division

*Updated 2026-11-27, about 00:47 UTC (after the fifth checkpoint: Part VII; the torus of three angles settled; Part VIII; the answers to the Frontier Benchmarking division; see the commit time).  Branch `research/ensemble-identifiability`.*

## State

**The Frontier Benchmarking division's mathematical feedback answered** (ENSEMBLE-RES-0008;
report §7 item 19; **unreviewed**, obligation OB30).  Its five items for us, read from its
`MATHEMATICAL_FEEDBACK.md` at the fetch of 00:18 UTC: *E-1* (data known up to scale and
offset) is Proposition E23.1, now also with tolerances — linear in
`(ν, 1/gain, offset/gain)`; *E-2* (verdicts that survive enlarging the pool): Proposition
E30 — intervals and mass bounds survive at the tolerance `τ + Lh` for a pool that is a
net, verdicts do not; *E-3* (an identifiability radius "as a linear programme"):
Proposition E31 — the radius is the largest width of a population interval over all
subsets, it is **not** a linear programme (NP-complete to decide whether it is one), and
it has certified bounds from `2|X|` programmes; *E-4* (a modulus for distance
distributions): open — Problem O4 — with a sharp modulus in the neighbouring case of
separating features (Proposition E4.1); *E-5* (error sets that are not boxes):
Proposition E17.2 — the tolerance term of a certificate is the support function of the
error set.  **New finding** (Proposition E20e, numerical): thirteen states on a torus of
four angles are determined in 26 of 40 random instances and not determined in 10, each
with a margin — *there is no generic answer over the reals*.  **First request to
engineering** (ENSEMBLE-REQ-0001, taking up its offer): independent re-implementation of
three finite checks, local computation only.  Answered in the same message:
GEOMETRY-MSG-0010 (for distributions of distances among sparse labels our E7/E8 apply,
without stability) and COMPLEXITY-MSG-0006 §1 (applied).  **Received and not yet
answered:** SCI-RES-0040, the Science division's answer to our question E-S5 (how the
ensemble enters the standard observables); **nine of our controls were replicated** by
the Frontier Benchmarking division's independent code (FRONTIER-MSG-0002 §4).

**Incomplete models: Part VIII, and the answer to the Structural Biology division**
(ENSEMBLE-RES-0007; report §4e, §4d.1, §7 item 18; **unreviewed**, obligation OB29).  Four
statements against the ways in which the model of Parts I–VII can be wrong: several
unknown gains and offsets are linear, each costing one direction of the certificate
(E23.1); a datum averaged on two time scales is convex in the ensemble and bracketed by
its two limits — a convex outer bound valid for every separation of time scales (E27);
an incomplete library is a tolerance, and data that falsify a library give a certified
lower bound on the weight it misses, from bounds on the observables alone (E28); the
number of conformers is partially identified — the largest number is the size of the
zero set of a certificate, the smallest is NP-hard with rank lower bounds, and the
ensemble is identified iff they agree (E29).  Software cards N4–N6; controls B9-01 to
B9-03 (25 reference instances, 38 exact verifications).  ENSEMBLE-RES-0007 tells the
Structural Biology division what has changed in the statements its register quotes
from our `8d42f60`, checks its table of data types as mathematics, and confirms its
prior-art observation.  **An internal review (ER4) of Part VII, E20a–E20d and the other
unreviewed statements is running** (a subagent of this division; it examines `b654396`,
so Part VIII and E23.1 are not covered).

**The torus of three angles is settled** (ENSEMBLE-MSG-0009; report §4c.4, §7 item 17;
**unreviewed**, obligation OB28).  *Theorem E20b:* six states in general position on `𝕋³`
are never determined by the multilinear data — twelve first-order conditions along the
curve where the lifted certificate vanishes have rank 12 (exactly, at rational
instances), so every candidate certificate vanishes on the whole curve; with E20a
(whose numerical input is now an exact computation): five, not six.  *Proposition
E20c:* on a hypersurface of special six-tuples they **are** determined, by a certificate
that is provably not a sum of squares of lifted forms (existence numerical); near such
a six-tuple the verdict "identified" is discontinuous in the configuration while the
stability bound of the certificate is not.  *Proposition E20d:* for `r ≥ 4` no
`K ≥ 3^r/(r + 1)` states in general position are determined (17 on four angles), by a
published theorem on double points of `(ℙ¹)^r`; the range for four angles is 11 to 16.
**Machine-checked since the last commit:** `Ensemble.eq_of_homogeneous_certificate` (the
sufficiency half of Proposition E23(b): data known up to one calibration factor), with a
witness; the audit passed on the tree that contains it.  New question E-T5 to Theory
and Complexity (is the certificate of E20c a sum of squares at the next level?).
Acknowledged: THY-MSG-0019 §5 (E-T4 answered: no such format), COMPLEXITY-REV-0005 (the
propositions we quote in §4.2 reviewed), GEOMETRY-MSG-0009.  The Structural Biology
division's intake report on our work is answered in ENSEMBLE-RES-0007.
**Prior art found** (`PRIOR_ART.md` §1, §5b′, §6 item 20; prompted by that report): our
Theorem E1(b) *is* Theorem 18 of di Dio and Schmüdgen (J. Funct. Anal. 2018) on the
determinacy of truncated moment functionals, and the chain of its proof is Fialkow's
core variety — now cited as known; the upper end of our interval for the weight of a
conformer is the "maximum occurrence" of the structural-biology literature; the
mechanism of E20b, E20c on the curve is in Baldi, Blekherman and Sinn (2024).
**Finished:** the four-body threshold run at `n = 14` (half-point between 320 and 340
conformers; 3.5 to 3.7 times the lift dimension; 8 to 15 % above a Gaussian cloud).

**After the fifth checkpoint — data that are not linear in the ensemble** (ENSEMBLE-MSG-0008;
report §4d = Part VII, §7 item 16; **unreviewed**, obligation OB27).  For data that are
functions of finitely many means: ratios of means and one unknown calibration factor are
linear problems (E23: the factor costs exactly the constant in the certificate; an
ensemble identified with the factor known can cease to be when it is unknown); in
general the loss is the fibre of the function in the moment body, and the values of a
target form a union of intervals (E24); the length of a mean vector identifies only at
its least or largest possible value, with a linear modulus for the support and a
square-root modulus for the weights, both attained (E25); squared means are `2^m` linear
problems, and deciding whether such data are consistent with any ensemble is
NP-complete, also in the strong sense (E26).  A sentence of ENSEMBLE-MSG-0006 and of
`SOFTWARE_INTERFACE.md` ("ratios … are covered by nothing") was wrong and is corrected
(`DEAD_ENDS.md` ED25).  Software cards N1–N3 (readiness R1); control family B8
(twenty-two reference instances, thirty-three exact verifications at that commit).

**Second supplementary directive of the research owner (received about 22:40 UTC):** an
eighth division — Frontier Benchmarking, Experimental Evidence and Scientific Evaluation,
branch `research/frontier-benchmarks`, digest `FRONTIER_BENCHMARKS_TO_ALL.md`.  Our protocol
copy recognises all eight divisions (`docs/collaboration/README.md`, third addendum, with
the rules that bind us: read its findings, answer within our responsibilities, turn an
exposed limitation into a theorem, an algorithm or an obstruction, do not duplicate its
evaluation mandate, leave substantial computation to engineering, respect blind /
pre-leaderboard / retrospective distinctions and held-out data).  The branch was founded
at 22:54 UTC; at 23:07 UTC (`626fd13`) its digest said that nothing had been sent yet.  Our
benchmark controls are marked as public development material, not held-out evidence.

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
| structural biology | `research/structural-biology` | `aec72df` | its first checkpoint (23:07 UTC).  Read in full: `STRUCTURAL_BIOLOGY_TO_ALL.md`; STRUCTBIO-MSG-0002 (its maturity statement to the Frontier division); **its intake report on our work** (`docs/structural_biology/intake/N_ensemble.md`, written at our `8d42f60` — before our fourth and fifth checkpoints, the reviews ER2 and ER3 and ENSEMBLE-MSG-0006) and the entries A15, A16 of its theorem-to-software register (capability C3, "ensemble partial identification", planned, not started).  STRUCTBIO-MSG-0001 only where it names us; STRUCTBIO-REQ-0001 to -0003 (to engineering, science, theory) by their subjects in the digest.  **Answered** in ENSEMBLE-RES-0007 (what has changed in the statements it registered, its table of data types, its prior-art observation) |
| frontier benchmarks | `research/frontier-benchmarks` | `097b4c7` | founded at 22:54 UTC on 2026-11-26.  Read in full at the fetch of 00:18 UTC on 2026-11-27: **FRONTIER-MSG-0001** (its introduction, its determination that nothing of MetricChain is a CASP17 participant, its evaluation standards and the freeze tooling); the section "To the ensemble division" of its `MATHEMATICAL_FEEDBACK.md` (**five items E-1 … E-5**: data known up to scale and offset; verdicts that survive enlarging the candidate pool; a graded "identifiability radius"; a modulus for distance distributions; error sets that are not boxes — proposals to be sent in its FRONTIER-MSG-0002); the row C5 of its `RESEARCH_INTAKE.md` about our work (at our `2d2054d`) and §6 of its `CASP17_ASSESSMENT.md` (retrospective question R-1, "what could the ensemble data decide?", gated on prerequisites that do not exist).  Not read: its protocols, registers, literature assessments, code.  Also read: the section on us of its `intake/INTAKE_ensemble_geometry_complexity.md` and the cross-cutting part with five questions for us.  **Answered** in ENSEMBLE-RES-0008 |
| *all five older branches moved between 22:27 and 23:07 UTC* | | theory `07cde81`, engineering `640cd9c`, science `169c6b1`, geometry `d3375f7`, complexity `48412d8` | read since: THY-MSG-0019 §5 (to us) in full; COMPLEXITY-REV-0005 (summary, findings 7, 8, 10, disposition table); GEOMETRY-MSG-0009 in full; headers only: THY-MSG-0020, SCI-REV-0024, GEOMETRY-RES-0007; the engineering protocol copy not read.  The rows above describe what was read at the earlier heads |
| *all seven branches moved again by 00:18 UTC on 2026-11-27* | | theory `37ce6d3`, engineering `8df6e5e`, science `5e1c350`, geometry `a82b1cd`, complexity `d920323`, structural biology `41fa668` | read since: GEOMETRY-MSG-0010 in full (answered in ENSEMBLE-RES-0008 §3); COMPLEXITY-MSG-0006 §1 in full (applied; §4 of the same response); ENG-MSG-0007 §2 (how to make a request), §6 (its offer to us), §7; STRUCTBIO-MSG-0003 where it names us (it does not address us); headers only: SCI-MSG-0035, GEOMETRY-RES-0008, COMPLEXITY-RES-0009, -0010.  Not addressed to us and not read: STRUCTBIO-REQ-0004, STRUCTBIO-RES-0001, -0002, SCI-RES-0039, SCI-REV-0025 to -0028, ENG-RES-0015 to -0018 |
| *fetch of 00:45 UTC on 2026-11-27* | | frontier benchmarks `3c6446b`, science `92d334d`, structural biology `d61fc53`, theory `61461f3`; engineering, geometry, complexity unchanged | read: **SCI-RES-0040 in full** (the Science division's answer to our question E-S5: a table of how the ensemble enters fourteen standard observables, from memory — most are means in one motional regime; scattering and DEER have a factor *and* an offset; order parameters and fast-regime Overhauser rates are squared lengths of mean vectors; Bragg intensities are squared means; dipolar couplings with a fitted alignment tensor are bilinear; images and kinetics are outside); FRONTIER-MSG-0002 §1, §4 (**nine of our controls replicated by its independent code**), §6 (its questions to us: E-3, E-1 with factor and offset, E-2 — answered in ENSEMBLE-RES-0008); FRONTIER-MSG-0003 where it names us.  **To be answered** (ENSEMBLE-RES-0009): SCI-RES-0040 — which of our statements covers which row of its table.  Not read: FRONTIER-REQ-0001, -0002, SCI-RES-0041, -0042, THY-MSG-0021, the new files of structural biology (none addresses us) |

## Verified state at the head of the branch

* Lean: `proofs/Ensemble/Exposedness.lean`, `RenyiHeppes.lean`, `ThermalUnionBound.lean`,
  `TwoStateCertificate.lean`, `PermanentCertificate.lean`; twenty-five headline theorems
  and nine non-vacuity witnesses listed in `proofs/AxiomAudit.lean` (the eighth, for the
  density form of the thermal inequality, was asked for by the review ER2; the
  twenty-fifth theorem and ninth witness are the homogeneous certificate of E23(b)).
* **The programme's full audit** (`scripts/audit_all.sh`: self-tests with planted
  violations, `lake build` (8653 jobs, no warning), token scan, axiom walk — 5147
  declarations, standard axioms only —, falsification harness, 552 mutation tests,
  separation benchmarks, reference checker, documentation references) **passed on the
  `proofs/` tree of this commit** ("AUDIT PASSED", run of 23:01–23:34 UTC on 2026-11-26,
  started after the two new declarations were inserted).  The documentation-reference
  stage was re-run after the last edits of the documents.  Files of other divisions changed here:
  only `proofs/AxiomAudit.lean` (imports, `#print axioms` lines and witnesses appended) and
  `docs/collaboration/README.md` (an addendum).
* Numerics: `python3 experiments/ensemble/run_all.py` — twelve scripts (`torus_six_states.py`,
  with exact rational and modular computations, `torus_four_angles.py`,
  `nonlinear_data_checks.py`, `misspecification_checks.py` and `robustness_checks.py` are the
  new ones; the last regenerates and verifies the benchmark controls), then
  `check_quotes.py` (every number quoted in a "Numerical check" passage of the report is
  the one in the stored output; 137 entries): all pass
  (`experiments/ensemble/output.txt`).  Threshold computations and the degree-2 table:
  `output_threshold.txt`.

## What is and is not reviewed

| part | status |
|---|---|
| Lean statements | kernel-checked; the statements of `ThermalUnionBound.lean` were compared with the report by the review ER2 (they match); the others were read by the author only |
| Parts I–III (version 1) | internal adversarial review ER1 (a subagent of this division; AI review, not peer review): every numbered statement confirmed, five major and thirteen minor corrections, **all applied**.  Part II also reviewed independently by the Science division (SCI-REV-0020: every step re-derived, no gap; four major and ten minor findings on what the statements may be read as, **all applied**) |
| Parts IV, V, E7′, E2.2, E2.3, §4.4 (version 2) | internal adversarial review ER2 (same kind): no critical defect; four major findings — among them a false converse in E15T — and twelve minor, **all applied**; E15 replicated by the Science division with its own code (SCI-RES-0032) |
| Proposition E15U | main statement re-derived and replicated by the Science division (SCI-RES-0038); the other three characterisations and the consequences **read by nobody but the author** |
| Proposition E17.1 (observation models) | immediate; **read by nobody but the author** |
| Part VII (E23–E26; data not linear in the ensemble) | paper proofs, elementary; numerical checks Q1–Q5; the sufficiency of E23(b) kernel-checked; **read by nobody but the author** (OB27); no prior-art search |
| Theorem E20b, Propositions E20c, E20d (the torus of three angles; double points) | paper proofs with exact computer algebra at rational instances (not kernel-checked); E20c's existence numerical; **read by nobody but the author** (OB28); under internal review (ER4, running) |
| Proposition E23.1 and Part VIII (E27–E29; incomplete models) | paper proofs, elementary; numerical checks M1–M4; **read by nobody but the author** (OB29); not covered by ER4; no prior-art search |
| E23.1(d), E17.2, E30, E31, E4.1 (replies to the Frontier division) and E20e (thirteen states on four angles) | paper proofs of a few lines; checks R1–R5; E20e(d) numerical (a stored survey of 40 instances, verified on grids and sampled curves, not exactly); **read by nobody but the author** (OB30); independent re-implementation asked of engineering (ENSEMBLE-REQ-0001) |
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
reviews by subagents of this division (ER1, ER2, ER3: all reported and applied).
