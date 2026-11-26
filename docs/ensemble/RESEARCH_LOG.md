# Research log — Ensemble Identifiability and Certified Inference Division

## Resume here

*(Updated at every checkpoint.  A successor should read `HANDOFF.md` first, then this
section, then `OPEN_OBLIGATIONS.md`.)*

**State after checkpoint 1 (2026-11-26).**  `ENSEMBLE_REPORT.md` version 1: Theorems E1–E12 in
three parts (exposedness and the bridge to Theorem 2.4; laws of observables and ensemble
rigidity; pair data on the cube).  Lean: `proofs/Ensemble/Exposedness.lean`,
`RenyiHeppes.lean` (seven headline theorems, two witnesses).  Numerics:
`experiments/ensemble/run_all.py`.  Sent: ENSEMBLE-MSG-0001 (introduction), -0002 (checkpoint).

**Next, in this order.**
1. Apply the internal adversarial review of the report (OB1) — corrections as linked
   messages, entries in `DEAD_ENDS.md`.
2. Problem O1 numerically at `n ≤ 16` (probability that `K` random vertices of the cut
   polytope form a face, by linear programming), to locate the threshold in `[1, 6.34]`.
3. Finite temperature (Problem O7): identification inside an envelope class; the
   polytope of the class in the weights; exposed points relative to `k`-body data.
4. Quantitative ensemble rigidity (O4) and conformers with common rigid parts (O3) — with
   the Geometric Inference Division once it exists.
5. Noise (O8): the modulus of continuity for the classes of the report.
6. Obligations OB2–OB9 (sources, the programme's full audit on this branch).

---

## 2026-11-26 — Cycle 0: registration and first reading

**Branch.**  `research/ensemble-identifiability` created from the theory head `a844b5a`
(one work-in-progress commit after the twenty-second checkpoint `dd067f1`, the last audited
state).  Read: root `README.md`; theory report §§0, 1, 2.3 and the section map; the
collaboration protocol, `status/theory.md`, THY-MSG-0016 (the owner's supplementary
directive on generality); from the science branch at `2b4ccdf`: `INFERENCE_LIMITS.md`
(version 3, in full), the index of its addenda A1–A17, `OPEN_PROBLEMS.md` (in full).
Not yet read in full: theory report §§11.17, 11.27–11.30 (statements only), the science
addenda, the engineering branch beyond its log.

**What already exists in the programme about ensembles (so that we do not rediscover it).**

* Theory: the object is the *residual* `g` in an envelope class, seen through evaluations
  `g(a)`.  In the weights `w = e^{-g}` the class is a polyhedral cone, `Z` is linear and an
  evaluation is a point functional: the theory division's complexity theory is a theory of
  *standard information* for a linear functional on a convex cone, to relative accuracy.
  Theory report §11.28: the exact range of a ratio of macrostate weights is a transport
  problem with gains (`MacroRatio.lean`).  §§11.27, 11.29: local ensemble-averaged data do
  not change the class exponents.  §11.30: divergence balls around a sampleable model.
* Science (`INFERENCE_LIMITS.md`): the two-oracle model (evaluations I1, expectations I2,
  a calorimetric datum I3) on the cube class.  `k`-body marginals do not identify the
  entropy and bound basin populations only from above (orthogonal arrays, Rao);
  exponential families are identified by their sufficient statistics and maximum-entropy
  refinement is stable (`TV ≤ tanh(βω/4)`); three *sound* certificate formats for
  identified sets (generalised moment problem; divergence ball; flows with gains), stated
  as known mathematics; falsification certificates.

**Where this division starts.**  The mandate's observation model `y_i = ∫ f_i dμ + ε_i` is
*linear information about the normalised measure*.  Nothing in the programme yet answers
the first questions of that model: which ensembles are determined by which observables,
how stably, with what certificate, and what the choice of observables costs.  First
priorities (all to be proved or refuted; nothing below is a result):

1. **Observability as exposedness.**  An ensemble is determined by the data of an
   observable family iff its support is exactly the ground-state set of an energy in the
   span of the observables, with independent features on it.  The stability modulus of
   that identification should be an exact linear-programming quantity, and for a single
   conformation it should coincide with the sharp-minimum condition of theory report
   Theorem 2.4 (`robust_certified_iff`): *a certificate of robust optimality is a
   certificate of ensemble identification*.
2. **Ensemble rigidity.**  When the data are the laws of several scalar observables
   (distance distributions), a finite ensemble is determined iff no *chimera* —
   a configuration assembled from the observable values of different conformers — is
   realisable.  For frameworks this should be a condition on the rigidity matroid.
3. **Capacity and adaptivity.**  How many conformers can `k`-body data resolve, in the
   worst case and for typical supports?  What does adaptive choice of observables buy?
4. **Obstructions.**  Continuous ensembles and finitely many smooth observables;
   observables that are quadratic in the coordinates; what remains partially identified,
   with certificates.
5. **Finite temperature.**  Identifiability inside an envelope class; relation between
   the instances that are hard for evaluations and those that are easy for ensemble data.


---

## 2026-11-26 — Cycle 1: what an ensemble is determined by

**Synchronisation.**  Theory `a844b5a`, science `2b4ccdf`, engineering `88feab9` (no change
since registration); the geometry and complexity branches do not exist yet.

**Investigated and proved** (details in the report; novelty in `PRIOR_ART.md`).
* Part I.  The characterisation of identified ensembles (E1) by a theorem of the
  alternative; the exact modulus for one conformation by Sion's theorem (E2) and the
  observation that its constraint is the sharp-minimum inequality of theory report
  Theorem 2.4 — the bridge is machine-checked with `robust_certified_iff` as a lemma; the
  first-order constant for finite ensembles (E3).
* Part II.  The pigeonhole proof of Rényi–Heppes works for any features that are
  `r`-determining (E4, machine-checked for finite spaces; sharp).  For frameworks the
  pigeonhole is useless and the right notion is the chimera; the dimension count that
  excludes chimeras for generic tuples is exactly connectivity of the algebraic matroid
  (E5).  With the 2022 theorem that globally rigid graphs have connected rigidity matroids,
  ensemble rigidity is equivalent to global rigidity (E7); `2K` moments per edge (E8).
* Part III.  Pair data on the cube: the projector certificate; capacity of order `n`
  (E10, with Odlyzko's theorem), failure beyond `6.34n` (E11, Gaussian signs); the
  adaptivity gap (E12).

**Refuted, withdrawn or superseded:** `DEAD_ENDS.md` ED1–ED6 (a question the literature had
answered; a capacity constant that was Odlyzko's; a kinematic heuristic contradicted by a
theorem; unlabeled PCA is a neighbour, not a special case; two numerical controls with
wrong expectations; counting bits does not bound adaptive designs).

**Verified.**  Lean modules compile without warnings; axioms standard.  Numerical checks
T1–T3, R1–R6, C1–C6 pass (`experiments/ensemble/output.txt`).

**Communicated.**  ENSEMBLE-MSG-0002.

**Reassessment.**  The strongest statements are the bridge (E2(c)), ensemble rigidity (E7,
E8) and the capacity/adaptivity picture (E10–E12).  Their common weakness is the
idealisation to point conformers and exact data; the next cycles go to finite temperature
and to noise.  The most likely place for an error is Part II (genericity, real against
complex varieties) — the review is asked to attack it first.
