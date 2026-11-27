# Consolidation assessment — Geometric Inference, Rigidity and Inverse Problems Division

*Branch `research/geometric-inference`.  Written 2026-11-27 under the research owner's
directive "Controlled Consolidation and Temporary Research Halt".  State of the branch
assessed: commit `a1622d7` (thirteenth checkpoint) plus the commit that adds this file.
Everything below was produced in one working day by AI sessions; "reviewed" always means
reviewed by another AI session of this collaboration, never external peer review.*

## A. Executive assessment

The division studied one idealised inverse problem and two neighbours of it.

*The problem.*  A chain of `n` points has `K` conformations ("states") with weights; one
observes the matrix `M` of **ensemble-averaged squared distances** between all labelled
points, and knows that every state has the same bond lengths and bond angles.  Which
ensembles are determined by `M`?

*What was established.*

1. A clean theory for that problem: an ensemble is one configuration in `ℝ^{3K}` (stacking);
   it is determined among **all** ensembles — any number of states, continuous ones
   included — exactly when the constrained edge directions of that configuration lie on no
   non-trivial quadric (the conic condition); for generic chains this holds from
   `⌈(9K² + K + 8)/4⌉` points on (12, 23, 39 for two, three, four states), and then the
   states are recovered by linear algebra with a rank certificate (DEMIX).  Below that
   threshold a quartic linear-algebra certificate proves identifiability from 10, 16, 30
   points.  Core statements are machine-checked or reviewed; thresholds are exact
   computations.
2. Its boundaries, as theorems or explicit counterexamples: without statewise constraints
   nothing is determined; a continuous part is never determined; one differing torsion is
   never resolved; sparse labels determine nothing; a tolerance on the bond geometry
   destroys uniqueness; "parameter count" thresholds give only local identifiability.
3. For single conformations from sequence-local distances: the stability constant grows
   like `n²` — a global bound with no threshold (reviewed with replication), matching lower
   bounds — and, by the Science division's finding which we replicated, distances known to
   a few tenths of an ångström do not determine a fold in the worst case.
4. Quantitative versions with computable constants: correct, and **empty at realistic
   accuracy** (certified ranges of `10⁻⁵` ångström for local distances; relative errors
   `10⁻¹²`–`10⁻⁴` for demixing).

*What was not established.*  No statement about any measured quantity: the observable is
measured by no instrument (labelled scattering gives block sums; FRET, DEER, NOE and PRE
data are not averaged squared distances).  No software beyond reference scripts.  No
realistic validation.  The mathematics of items 1–2 is, in our assessment, a modest but
real contribution to rigidity theory (identifiability of mixtures of frameworks from
second-moment data), built from known tools; parts of it are rediscoveries (section C).
Its value for computational structural biology is at present **negative-control value**:
it says precisely what such data cannot determine.

Counts at the head of the branch: 5 notes, 58 register rows, 1 Lean file (59 declarations
of ours in an audit of 5110, standard axioms only; unchanged since the sixth checkpoint),
57 harness tests and 44 planted errors (all caught), exact computations behind 12 rows,
19 numbered proof obligations (some partly discharged, one — O-19 — planned and not started), 27 recorded dead ends and
corrections, 12 messages (with the consolidation message), 10 responses, 6 requests,
1 internal review; no shared compute used.

## B. The strongest contributions, ranked

### B1. Second-moment rigidity of ensembles: the conic criterion, exact thresholds, demixing

* **Contribution.**  (i) Lemma 2.1–2.2: `M(μ)` is the squared-distance matrix of the stacked
  configuration `z ∈ ℝ^{3K}`; every state of every ensemble with the same `M` is a linear
  image of `z`.  (ii) Theorems A, B, B′: `μ` is identifiable among all ensembles if the only
  quadrics through the `E₀`-edge directions of `z` are the trivial ones (CC); exact
  criterion B′ (unique barycentric representation on rank-3 points).  (iii) Theorem C: for
  generic chains (CC) holds iff `n ≥ ⌈(9K² + K + 8)/4⌉` — exact witnesses for `K ≤ 20`, a
  weaker bound for all `K`, concavity of the generic rank along the chain.  (iv) DEMIX
  (Proposition 6.1): recovery by two eigen-decompositions and one linear system, with a
  certificate that is sound for every realizable input.  (v) Theorem H: local
  identifiability within `K`-state ensembles from `2K + 3` points (exact for `K ≤ 8`).
  (vi) Theorems F, G: stress certificates for incomplete data; a global `W₂² ≤ C·‖ΔM‖` bound,
  sharp in the exponent.
* **Artifacts.**  `docs/geometry/ENSEMBLE_RIGIDITY.md` §§2–7; register rows G1.1–G1.22;
  commits `d84a43b`, `7c2a3d1`, `f7eed26`, `cd4a2ec`; `experiments/geometry/exact_conic_rank.py`,
  `exact_jacobian_rank.py`, `demix.py`; `proofs/Geometry/EnsembleRigidity.lean`.
* **Verification and review.**  Machine-checked: `stacked_sqdist`, `state_is_linear_image`,
  `exists_linearMap_of_gram_eq`, `sqdist_midpoint_of_conic`, `mixture_state_of_conic`,
  `finite_mixture_identifiable`, `mixture_identifiable_stacked` (Theorem B against finite
  competing mixtures, in coordinates, with a worked instance), `stress_certificate`.
  Reviewed: internal referee (GEOMETRY-REV-0001: no false theorem, four overstatements
  corrected); Science division SCI-REV-0021 (Lemma 2.2, Theorems B, B′, Corollary 4.2,
  Theorem G proved as stated).  Exact ranks replicated over ℚ by Engineering
  (ENG-MSG-0007 §5).  Not machine-checked: competitors with continuous distributions;
  Theorem C (computer-assisted).
* **Assumptions.**  Exact data; all pairs; labelled points; identical bond lengths and
  bond angles in every state; states generic (in particular sharing no rigid segment);
  finitely many states.
* **Closest prior art.**  Schoenberg (sums of Euclidean distance matrices); Connelly, and
  Alfakih's dimensional rigidity (conic at infinity ⇔ affine flex; universal rigidity);
  Laurent–Poljak 1996 (faces of the elliptope) — **Theorem B in dimension one with
  unit-diagonal constraints is theirs** (found by the Science division, not by us);
  Barvinok–Pataki rank bounds; Kam's second-moment invariants in cryo-EM.
* **Distinction.**  States of dimension `d ≥ 2` with statewise *distance* constraints; the
  quantifier over all ensembles; the thresholds for chains; the algorithm with its
  certificate.
* **Evidence for originality.**  Not found by our logged searches (20 in all for the
  division, at the level of titles and abstracts) nor by the Science division's
  independent search for `d ≥ 2`.
* **Evidence against.**  The `d = 1` case is in print; the proof is the standard face
  argument for Gram matrices; every ingredient is classical; our searches opened almost
  no full texts; a specialist in universal rigidity may know the statement as folklore.
* **Validation.**  Exact witnesses (48 + 8 configurations, `K ≤ 20`); floating-point
  recovery at the thresholds; 23 labelled synthetic instances with second solutions where
  the answer is not unique (`BENCHMARKS.md`).
* **Limitations.**  The observable is idealised; (CC) is sufficient, not necessary; fails
  for states sharing rigid parts (B-hinges below); thresholds are generic statements —
  an instance is covered only by running its certificate.
* **Before publication / deployment.**  A literature check by a human specialist in
  rigidity theory and semidefinite geometry; a proof of the threshold for all `K` (now:
  exact to `K = 20`, weaker bound in general); a statement of relevance that does not
  claim an experiment.  Deployment: none warranted until an observable is matched.

### B2. Below the conic threshold: identifiability among all ensembles from 10, 16, 30 points

* **Contribution.**  Theorem I (two states: identifiable from 10 points, exact; at 7 and 8
  points explicit competing ensembles exist — numerical)
  and Theorem I′ (three states from 16, four from 30), by a certificate that is linear
  algebra on quartic forms: the `4 × 4` minors times forms have the maximal possible span.
  Proposition 6.2 (a)–(h), in particular the *structural point at infinity* (a rank-2
  quadric of two hyperplanes, present for `n ≤ 6K − 2`) and the certificate modulo it.
  Conjecture 6.3 and a table of predicted levels.
* **Artifacts.**  `ENSEMBLE_RIGIDITY.md` §5.5, §6.2; rows G1.25, G1.30–G1.32; commits `7c2a3d1`,
  `b0734aa`; `exact_demix4.py` (ranks modulo a prime at rational witnesses; only lower bounds
  on ranks are used), `exact_nonlinear_threshold.py` (Singular over ℚ), `minrank_prediction.py`.
* **Verification and review.**  Computer-assisted, exact.  The two-state case was computed
  independently by Engineering without sight of our result (degree `7 = 1 + 1 + 5`; 120
  minors spanning 63 of 70) and by our internal referee.  **§6.2 itself has had no outside
  reader.**  No Lean.
* **Assumptions.**  As B1, generic chains at the bond angles of the witnesses (and all but
  finitely many others).
* **Closest prior art.**  **The method is published**: Johnston–Lovitz–Vijayaraghavan 2023
  (linear sections of varieties), Derksen–Johnston–Lovitz 2024, Dastidar–Weich–Wein 2025.
* **Distinction.**  The reduction of the ensemble problem to a chain-structured linear
  section of the rank-3 locus; the structural point and the certificate modulo it; the
  exact thresholds.
* **For / against originality.**  For: thresholds for this structured family not found.
  Against: we drafted this section as new and found the literature only afterwards
  (`DEAD_ENDS.md` DG-21); what remains ours is an application of a known hierarchy.
* **Validation.**  Ten exact witnesses; a second prime; two planted errors caught.
* **Limitations.**  Four states between 19 and 29 points, three at 14–15, `K ≥ 5`: open;
  floating point is unreliable for these ranks (DG-23); no stability analysis.
* **Before publication.**  Fold into B1 as a section; one independent reading; either a
  proof of Conjecture 6.3 or a clear statement that the thresholds are computational.

### B3. Sequence-local distances: a global `n²` law — and what it does not give

* **Contribution.**  Theorem K (lower bounds: `n/K^{3/2}` always, `n²` on rod-like chains);
  Theorem L (for *every* configuration in `ℝ³`, no smallness condition:
  `min_g ‖Y − gX‖ ≤ 1.2 (b/(s_*τ_*)) (n + 2)² ‖η‖₂`, with a local form); Theorem L⁺ (the
  first-order constant in a certified range).  With the Science division's finding
  (SCI-REV-0028 F1, replicated by us): the first-order constant is not a global one, `1/τ`
  is necessary, and local distances known to `0.3` Å admit configurations farther away than
  the radius of gyration.
* **Artifacts.**  `docs/geometry/LOCAL_DATA_STABILITY.md`; rows G2.1–G2.7; commits `bdcca67`,
  `288b2de`, `9f164f9`, `a1622d7`; `local_data_upper.py`, `local_data_guarantees.py`,
  `distant_fits.py`.
* **Verification and review.**  **Reviewed with replication by the Science division
  (SCI-REV-0028): Lemmas P, Q, Theorem L, Corollaries L.1–L.3, Theorem L⁺ proved as
  stated**; Lemma P verified at its source; twelve findings applied.  Theorem K and
  Proposition L₀ not reviewed.  No Lean.
* **Assumptions.**  All distances of sequence separation at most 4; no four consecutive
  interior points coplanar; deterministic errors; `ℝ³`.
* **Closest prior art.**  Thin-rod geometric rigidity (Mora–Müller; Blanchard–Griso) —
  **mechanism and exponent**; lattice versions; Lew–Nevo–Peled–Raz (**Theorem K(a) is a
  corollary of theirs, with a better constant**); Arias-Castro–Vishwanath (the published
  global bound for this graph: with a threshold, exponential constant); Tu et al. (Lemma P).
* **Distinction.**  A global bound without threshold, polynomial, by stitching complete
  five-point windows — not found by two searches of the Science division.
* **For / against originality.**  For: those searches.  Against: scaling and mechanism are
  classical; the result is a discrete, explicit version of a known phenomenon.
* **Validation.**  Every step of the proof on 420 arbitrary competitors (ours) and 23 360
  pairs (the referee's); the distant configurations replicated to the digit.
* **Limitations.**  As a guarantee it is empty: certified range `3·10⁻⁶` Å on a 20-point
  helix-like trace; the best global constant is unknown between `1.92` and `456` there.
* **Before publication.**  At most a short note, jointly with the Science division, whose
  finding is the scientifically interesting half.

### B4. Partial observation: a counting rule, and an obstruction for sparse labels

* **Contribution.**  If only a subset `S` of the points is observed (all averaged squared
  distances among `S`): everything transfers to `S` (Theorem P1); the linear certificate
  needs `c(S) ≥ (9K² + K + 2)/2` observed pairs at chain separation 1 or 2 and that suffices
  for two families of patterns and on 100 random ones (Theorem P2, Conjecture P); below
  `9K/2` no local identifiability, and **with no two labels at separation 1 or 2 nothing is
  determined** — explicit second solutions (Proposition P3).
* **Artifacts.**  `docs/geometry/LABEL_PATTERNS.md`; rows G4.1–G4.5; commit `a82b1cd`;
  `label_patterns.py`, `exact_label_patterns.py`; benchmark instances A4, C6.
* **Status.**  Paper proofs and exact computations; **unreviewed**; the obstruction rests
  on a regularity condition checked numerically; no Lean.
* **Prior art and distinction.**  The mechanism of the obstruction is the classical
  rotation indeterminacy of second-moment data; the count was not found (two searches,
  one paper opened — a thin basis).
* **Limitations.**  Second moments only: for *distributions* of the same distances the
  Ensemble division's theorems give identifiability (ENSEMBLE-RES-0008 §3).
* **Before use.**  A review; a proof of Conjecture P; then it is a zero-cost pre-check for
  any tool that fits ensembles to such data.

### B5. Noise and inexact local geometry with computable constants

* **Contribution.**  Lemma N0 (a rank-3 positive semidefinite solution of the conic system
  up to `ρ` is within `cρ/σ` of a projector — by eigenvalue interlacing); enclosures of every
  consistent ensemble (Theorem N1; the constant of Theorem G becomes computable); the
  exact first-order constants of demixing, certified in a range and attained (Theorem N3:
  `0.7`–`4.5` in the instances); the tolerance family (Proposition N6: uniqueness is lost for
  every tolerance; first-order size `c_tol·‖violations‖`).
* **Artifacts.**  `docs/geometry/ROBUST_DEMIXING.md`; rows G5.1–G5.6; commit `a1622d7`;
  `robust_demix.py`.
* **Status.**  Paper proofs, every inequality checked numerically on unfavourable
  competitors; **unreviewed, written last**; floating point; no Lean.
* **Prior art and distinction.**  Standard perturbation theory; joint block
  diagonalisation has a published perturbation theory (Cai–Li 2017).  Ours: the
  application, the all-ensemble enclosure, the tolerance family.  Novelty of technique:
  none claimed.
* **Limitations.**  Certified ranges end at relative errors `10⁻¹²`–`10⁻⁴`.
* **Before use.**  A review; an exact or interval evaluation of the constants.  The
  first-order condition numbers are usable now as diagnostics, labelled as first-order.

*Not ranked: hinge ensembles* (`HINGE_ENSEMBLES.md`; two states that share rigid segments
are identifiable from two differing torsions on, unless two of three rotations are
half-turns).  Correct and exact, but **its main statement was obtained first by the
Science division's referee** (Proposition R22-1); ours was independent and adds the sharp
half-turn criterion and the exact count.  It belongs in any joint write-up of B1.

## C. Negative results, rediscoveries, and what to deprioritise

* **Rediscoveries.**  Theorem B for `d = 1` (Laurent–Poljak 1996); Theorem K(a)
  (Lew–Nevo–Peled–Raz 2023, better constant); the method of §6.2 (Johnston–Lovitz–
  Vijayaraghavan 2023); the mechanism and exponent of Theorem L (thin-rod rigidity); the
  hinge theorem (Science division, hours earlier).  Three of these were pointed out by
  the Science division, not found by us.
* **Our own errors, all corrected on the record** (`DEAD_ENDS.md` DG-1 … DG-27): "universal
  rigidity ⇒ second-moment rigidity" was false as written; an expected degree 2 was 7; a
  threshold in the first Theorem L was an artefact of the proof; a published ratio was
  wrong by a factor 7 (round-off); floating-point ranks were wrong at the certificate
  thresholds; header times were guesses; one attribution to another division was wrong.
* **Guarantees that are empty.**  Theorem L/L⁺ (`10⁻⁵` Å); robust demixing (`10⁻¹²`–`10⁻⁴`
  relative); the computable constant of Theorem G is four to eight orders below the
  values found by search.
* **Impossibility at realistic accuracy** (Science division; replicated): sequence-local
  distances with errors of a few tenths of an ångström do not determine a fold.
* **The observable.**  Complete labelled averaged squared distances are measured by no
  instrument.  Every "identifiable" above is modulo all isometries of each state.
* **A route computed and excluded.**  Stress matrices of maximal rank for the gap of
  Theorem L: the factor grows faster than `n⁴` (DG-26).
* **Deprioritise or abandon.**  (1) Better constants for Theorem L by refining the
  chaining argument — the gap is partly real.  (2) Conjecture 6.3 and the certificate
  ladder for `K ≥ 5` by exact computation — hours per case, and DEMIX-4 is impractical
  beyond four states.  (3) Any use of these results as a proxy for FRET, DEER, NOE or
  scattering data without a forward model stated by the Science division.  (4) More Lean
  for the present statements — the machine-checked core is the part that matters.

## D. Practical opportunities, by level of evidence

| opportunity | mathematical possibility | implemented | synthetic validation | realistic computational validation | experimental evidence |
|---|---|---|---|---|---|
| **Negative controls for ensemble inference**: before fitting an ensemble to averaged pair data, decide whether such data can identify it at all (count rules; sparse-label obstruction; tolerance radius; "no upper bound on the number of states") | proved (B1, B4, B5; parts unreviewed) | reference scripts only (`label_patterns.py`, `robust_demix.py`) | yes: 23 labelled instances with explicit second solutions | none | none |
| **Demixing with a certificate and a radius** for data that *are* second moments | proved for the idealised observable | reference scripts (`demix.py`, `robust_demix.py`), floating point | recovery at thresholds; enclosures never violated | none; no instrument delivers the observable | none |
| **Conditioning diagnostics for local-distance reconstruction** (window thickness; nearly planar stretches are where long-range data are needed first; Lemma Q as a per-window bound) | proved; the usable part identified by the Science division | reference scripts | idealised traces only | none (deposited traces not touched; the Frontier division's FB-P-07 expects a negative outcome, as we do) | none |

The honest summary: the nearest thing to a "useful capability" is the first row — a
cheap, rigorous way to say **what cannot be concluded** — and it is useful only to the
extent that some real data are, or reduce to, second moments.  Whether they do is a
question for the Science division (its analysis of labelled scattering gives block sums,
which we have not treated).

## E. Recommended next actions (at most three)

**E1. Identifiability for the linear observables that exist: block sums, with the
Ensemble division's laws as the alternative.**
* Objective: thresholds, certificates and obstructions when the data are block sums
  `⟨C_a, M⟩` under a labelling scheme stated by the Science division; a clear statement of
  when second moments suffice and when distributions are needed.
* Prerequisites: Theorem F″ (checker for linear-functional data, no producer); the count
  `B ≳ √(2Kn)`; the Ensemble division's E7/E8.
* Missing: Jacobian ranks for block patterns (local identifiability); a certificate
  producer; an obstruction of the sparse-label kind for block sums.
* Baselines: maximum-entropy and Bayesian reweighting on a candidate pool; maximum
  occurrence.  Benchmark: planted synthetic ensembles under the stated scheme, with the
  Frontier division's protocol FB-P-04/-06 deciding the metric.
* Success: a proved threshold or obstruction and a pre-check that a baseline tool cannot
  contradict.  Failure: no identifiability at any realistic number of blocks — which is
  itself the result to publish to the collaboration.
* Reasoning: the numerical part is comparable to our twelfth checkpoint (one focused
  session); the proofs are not estimable.  Compute: local, minutes; **no Modal**.
* Dependencies: Science (forward model and scheme), Ensemble, Structural Biology.
* Model: the exploration can run on Opus; the proofs and the adversarial self-review
  benefited from the stronger model throughout this session.

**E2. Make B1 + B2 (+ hinges, + B4) defensible before a human expert.**
* Objective: one manuscript-grade note with complete proofs, an honest novelty statement,
  and a reproducibility package.
* Prerequisites: all present.  Missing: a specialist's literature check (rigidity,
  semidefinite geometry, algebraic statistics of mixtures); an independent reading of
  §6.2, `LABEL_PATTERNS.md` and `ROBUST_DEMIXING.md`; a proof of the threshold for all `K`
  or a clear computational statement.
* Baselines and benchmark: not applicable (mathematics).  Success: an external reader
  finds no false statement and confirms or refutes novelty for `d ≥ 2`.  Failure: the
  statement is folklore — then the note is a survey with exact thresholds.
* Reasoning: one review session plus writing; compute: the harness (two minutes) and the
  exact runs (under an hour); no Modal.  Dependencies: Science (review).  Model: writing
  can be done on Opus; the review should not be done by the model that wrote the proofs.

**E3. Only if the collaboration wants a quantitative theory: the two gaps.**
* Objective: the best global constant for local distances (between `1.92` and `456` on the
  test trace) and a way into the demixing basin better than Theorem N2; or statements for
  random noise.
* Prerequisites: Theorems L, L⁺, N2, N3; the Science division's worst cases.  Missing: the
  idea.  Success: a constant within a moderate factor of the lower bound, or a proof that
  none exists.  Risk: high; no cost estimate is possible.  No Modal.  We rank this last
  and would not start it before E1 and E2.

## F. Publication readiness

* **Candidate.**  "Identifiability of mixtures of chain conformations from averaged squared
  distances" — B1 with B2, the hinge theorem (jointly with the Science division) and the
  obstructions of B4 and B5.  It is a self-contained piece of rigidity theory with exact
  thresholds, an algorithm, machine-checked core lemmas and independent replications.
* **What it still needs before an external expert.**  (1) A literature search by someone
  who knows the field, with full texts — ours were at the level of abstracts, and three
  rediscoveries were found by others; (2) the one-dimensional case credited to
  Laurent–Poljak and the method of §6.2 to Johnston–Lovitz–Vijayaraghavan from the first
  page; (3) proofs in one notation, with the computer-assisted steps separated and their
  scripts archived; (4) an independent reading of the unreviewed parts; (5) a relevance
  paragraph that says the observable is idealised.
* **Not candidates on their own.**  Theorem L (known mechanism; empty guarantee; the
  interesting finding is the Science division's); robust demixing (standard tools).
* Machine-checking covers the linear-algebra core only and says nothing about novelty.

## Handoff

`docs/geometry/HANDOFF.md` (commands, environment), `docs/geometry/RESEARCH_LOG.md`
("Resume here"), `docs/geometry/PROOF_OBLIGATIONS.md` (O-1 … O-19),
`docs/collaboration/status/geometry.md` (verified state, messages, what was and was not
read of other branches).  Nothing of ours is running: no subagent, no background
process, no scheduled session, no Modal job; no shared compute was ever used.  The
division does not resume without the research owner's explicit authorisation.
