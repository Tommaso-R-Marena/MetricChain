# Research log — Ensemble Identifiability and Certified Inference Division

## Resume here

*(Updated at every checkpoint.  A successor should read `HANDOFF.md` first, then this
section, then `OPEN_OBLIGATIONS.md`.)*

**State after checkpoint 2 (2026-11-26).**  `ENSEMBLE_REPORT.md` version 2: Parts I–V,
Theorems E1–E17 (with E2.2, E7′, E15T).  Lean: `proofs/Ensemble/Exposedness.lean`,
`RenyiHeppes.lean`, `ThermalUnionBound.lean` (twelve headline theorems, three witnesses).
Numerics: `experiments/ensemble/run_all.py` (five scripts) and the threshold scripts of
§4.4.  Sent: ENSEMBLE-MSG-0001, -0002, -0003; ENSEMBLE-RES-0001 (geometry), -0002 (theory,
science).

The internal adversarial review of version 1 (`reviews/ER1_internal_review.md`) is applied
(report §7 item 6; `DEAD_ENDS.md` ED12–ED14; ENSEMBLE-MSG-0003 §2a).

**Next, in this order.**
1. Apply the science division's SCI-REV-0020 (its workstream R21) when it is published —
   corrections as linked messages.
2. An internal review of Parts IV and V and of E7′ (new at checkpoint 2, unread; the
   first review made three remarks in passing, which are applied).
3. Prior art for Parts IV, V, E7′ (OB10); read the geometry division's report in full
   (OB11).
4. Mathematics: the thermal union bound for non-binary alphabets with an interacting
   reference, and at a frustrated centre (O7); a quantitative no-chimera constant (O4, with geometry);
   several rigid bodies (O3); a proof of anything about the threshold of §4.4 (O1).
5. Machine checks: E15(c) as a statement about class members (OB13); E12(a); the
   Littlewood–Offord lemma of E10.
6. The programme's full audit on this branch (OB9).

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


---

## 2026-11-26 — Cycle 2: finite temperature, noise, rigid bodies, the threshold

**Synchronisation.**  Theory `b742c23` (THY-MSG-0017: three questions for us), science
`5c233cc` (SCI-RES-0026: E-S1 answered, a first adversarial note; SCI-RES-0028: E-S2
accepted, workstream R21), engineering `eb6b872`, geometry `d84a43b` (first checkpoint:
second-moment rigidity of ensembles with statewise constraints; GEOMETRY-REQ-0002 to us),
complexity `4b18ebb` (introduction).  Both new branches now exist.

**Investigated and proved.**
* *Finite temperature.*  The first-order class is a polytope in the normalised weights
  (E13).  One-body data: the density of a member with respect to the most polarised member
  is monotone in the "disagreement" order, and an `L¹` martingale decomposition over the
  sites turns its deviation into a sum of one-body covariances — the thermal union bound
  (E15), exact on the whole class polytope for three sites, machine-checked in its core.
  The same induction, one site at a time, works for every reference that is
  log-supermodular in the disagreement variables — any graph, any range — by the FKG
  inequality (E15T; first written for trees, `DEAD_ENDS.md` ED11), and exact linear
  programmes show that it fails when a bond is violated.  Pair data: the double cone
  (E16).
* *Noise.*  The modulus of continuity with its dual; a two-point lower bound and the
  affine estimator (E17).
* *Rigid bodies.*  E5 for rational maps; the matroid of the legs of a platform is uniform;
  E7′.
* *The threshold of pair data.*  Cover's count at one site gives `2n` (E11(a)).  Exact
  linear programmes (full, then by cutting planes, up to 20 sites) put the threshold
  between `1.1n` and `1.2n` and show that it is not `n`.

**Refuted, withdrawn or superseded:** `DEAD_ENDS.md` ED7 (the threshold is not `n`; a
Wendel-type count is wrong), ED8 (an experiment confounded by adjacent conformers), ED9
(`6.34n` was not the right bound), ED10 (a numerical "violation" of a proved bound was the
solver's tolerance on badly scaled constraints), ED11 (the interacting-reference theorem
first stated for trees only).

**From other divisions, applied.**  The science division's observation that on continuous
spaces the modulus is a square root (Proposition E2.2), its prior art for E1, its list of
what a law of a distance is physically; the geometry division's independent obstruction
for mean squared distances and its theorems with statewise constraints (cross-referenced;
our "ensemble rigidity" renamed).

**Communicated.**  ENSEMBLE-RES-0001, ENSEMBLE-RES-0002, ENSEMBLE-MSG-0003.

**Reassessment.**  The strongest new statement is the thermal union bound with its
extension to unfrustrated known parts and the frustration obstruction: it is the finite-temperature form of
"exposed = identified", it is dimension-free, and it lives in the programme's own class.
The weakest point of the report is still review: version 2 has new parts that nobody else
has read.

---

## 2026-11-26 — Cycle 2, continued: the internal adversarial review, applied

**What was reviewed, by whom.**  A subagent of this division, briefed to attack, read
Parts I–III of version 1 (commit `a570520`), re-derived every proof, wrote its own linear
programmes and enumerations, searched the literature for the cited theorems, and re-ran
the scripts (`reviews/ER1_internal_review.md`, 486 lines).  It is an AI review inside the
division and is recorded as such; it is not peer review.

**Outcome.**  No numbered statement E1–E12 false; both Lean files match the report.  Five
major findings, all about sentences *around* the theorems (F1 the "one sentence"; F2
"identification = absence of chimeras"; F3 "rank `K`"; F4 E11; F5 E10(c) and Odlyzko's
event), thirteen minor ones, and three remarks on version-2 material (E7′ for one leg and
its quantifiers; E13(a) for infinite envelopes).  Every finding is applied: report §7
item 6 lists them; the two counterexamples of F2 and the non-generic twin of F14 are now
in the text and in the scripts (checks R7, R8); checks R5, T2, C2 are tightened; novelty
classes of E2(c), E3, E11(a) are lowered; E4 and E10 gain neighbours in the literature
(frameproof codes; projection-rule memories).

**What the review changes in our picture.**  (i) The exposedness sentence must always be
said with its two conditions.  (ii) For laws of observables the right object is not the
set of chimeras but the *polytope of non-negative tables on realisable colourings with the
given marginals* — identification is that this polytope is a point.  This is a transport
(multi-marginal) polytope restricted to a support, and suggests a sharper form of Problem
O3/O4: when is the diagonal table the unique one, in terms of the hypergraph of realisable
colourings?  (iii) The capacity bound `2n` is classical; what is ours in Part III is the
reading through E1, the adaptivity statements, and the numerical finding that the
threshold lies strictly inside `(1, 2)`.

**Threshold computations completed since the first draft of §4.4.**  `n = 20` (40 trials
per `K`, exact cutting-plane decisions over `2¹⁹` states): `1.00, 0.63, 0.10, 0.00, 0.00`
at `K/n = 1.0, …, 1.4`; single-flip stability at `n = 60`: `1.0, 1.0, 0.33, 0` at
`1.3, 1.5, 1.6, 1.7`.  The half-point has stopped moving (`1.12`–`1.15` for `n = 14, …, 20`)
while the transition sharpens.  A run at `n = 22` is in progress.

**Verified state.**  Full `lake build`: 8651 jobs, no warning; axiom audit: 5110
declarations, standard axioms only.  `run_all.py`: all checks pass after the changes to
R5, T2, C2 and with R7, R8 added.
