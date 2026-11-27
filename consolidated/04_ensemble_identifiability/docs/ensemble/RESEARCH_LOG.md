# Research log — Ensemble Identifiability and Certified Inference Division

## Resume here

*(Updated at every checkpoint.  A successor should read `HANDOFF.md` first, then this
section, then `OPEN_OBLIGATIONS.md`.)*

**HALTED on 2026-11-27, about 01:25 UTC, by the research owner's consolidation directive.
Nothing below is to be started without the owner's explicit authorisation** (`HANDOFF.md`
item 0).  The division's assessment is `docs/collaboration/consolidation/ensemble.md`.

**State at the halt.**  `ENSEMBLE_REPORT.md` version 3 with the corrections and additions of
§7 items 8–22: Parts I–VIII, statements E1–E32 (with E2.2, E4.1, E7′, E15T, E15U, E17.1, E17.2,
E18′, E20a–E20e, E20′, E20″, E23.1), Conjectures C1–C3, Problems O1–O11.  Reviews, all
internal and all applied: ER1 (Parts I–III), the Science division's SCI-REV-0020 (Part
II), ER2 (Parts IV–V), ER3 (Part VI), ER4 (E20a–E20d, E23–E26; partial — OB32).
**Unreviewed:** E23.1, E27–E32, E17.2, E20e, E4.1 beyond its machine-checked inequality,
E15U beyond its main statement, E17.1, E22, two constants of E20″.  Lean:
`proofs/Ensemble/`, five modules, 26 headline statements, 10 witnesses;
`scripts/audit_all.sh` passed on the final `proofs/` tree (5151 declarations).  Numerics:
`experiments/ensemble/run_all.py` (thirteen scripts, then `check_quotes.py`, 152 entries;
`--quotes-only` after a change of text alone); long computations in
`output_threshold.txt`; unreviewed prototypes in `experiments/ensemble/scratch/`.
Software-facing: `SOFTWARE_INTERFACE.md` (cards; N1–N7 at readiness R1),
`BENCHMARK_CONTROLS.md` (25 instances in `benchmarks/controls_v1.json`, 10 torus instances
in `torus_instances_v1.json` — frozen).  Sent: ENSEMBLE-MSG-0001 to -0010, ENSEMBLE-RES-0001
to -0009, ENSEMBLE-REQ-0001 (to engineering; unanswered).  No subagent, background
process or job is running; no Modal job was ever started by this division.

**If the owner authorises further work — in this order** (the first three are §E of the
assessment):
1. **Are certified intervals informative on realistic problems?**  The decisive
   experiment for everything practical: needs a forward model with a stated error set
   (Science), a tool (Structural Biology; cards F1–F4, N1, N5, and E30 for the pool), a
   protocol (Frontier), column generation for large pools (not written).
2. **The chimera gap (Problem O4)**: a modulus for distance distributions, or a proof
   that there is none.  E4.1 is the model of the answer; the Science division's
   Proposition B is the band.  Without it Part II is unusable on data.
3. **External reading** of the possibly original results (torus; E4 with E4.1; E15U).
   **Before that, read Baldi–Blekherman–Sinn, arXiv 2407.06017, Sections 5–6, in the
   source**: the reviewer ER4 believes — from summaries — that E20b and E20c on a given
   smooth curve are there (`PRIOR_ART.md` §5b′).
4. Review of what no one has read (OB29–OB32), in particular E32 and the coNP reduction
   now in E26(c) (verified by hand only); ER4's unfinished programs are in
   `reviews/ER4_scripts/` (`er4_part7.py` parts C, D; `er4_e15u.py` never run).
5. Smaller mathematics, only if 1–3 are settled or blocked: fourteen states on four
   angles (prototype and survey in `experiments/ensemble/scratch/`: 15 of 16 random
   configurations not identified, so thirteen may be the largest number determined on
   an open set of `𝕋⁴`); exact instances for E20e and for a special six-tuple; for
   bilinear data (E32) a bound on the size of the certificate and a statement with
   tolerances (Problem O11); exact identifiability radii for the controls (E31).
6. Not recommended (assessment §C): thresholds on the cube (C2, C3); counting on tori
   for larger `r`; more formalisation of elementary statements.
7. Housekeeping: re-run `scripts/audit_all.sh` before a checkpoint that changes
   `proofs/`; a full `run_all.py` was not repeated after the last text changes (only
   `--quotes-only`).  Unread messages of other divisions: listed in
   `docs/collaboration/status/ensemble.md`.

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

---

## 2026-11-26 — Cycle 3: lifted certificates, higher-order data, a prior on the number of conformers, tori

**Synchronisation.**  Theory `4aea5fe` (nothing addressed to us), engineering `c81166b`,
science `70f208e` (SCI-RES-0029, copied to us: mean squared distances are measured by
scattering with labels; two states differing in one torsion are never identified; the
linear certificate fails below four differing torsions; the data are multilinear
trigonometric moments of the torsion distribution), geometry `f7eed26` (GEOMETRY-RES-0001:
answers to E-G2, E-G3 — its Theorem J applies our E5 to chains; a qualifier asked on our
E1.3; a renaming on its side; GEOMETRY-MSG-0003: two states identifiable from 10 atoms,
certifiable from 12, and a question to us about priors on the number of states),
complexity `22cf1a6` (nothing addressed to us).

**Investigated.**  The question of GEOMETRY-MSG-0003 — "identifiable within a family with
`K` states" against "among all distributions" — and the open case of SCI-RES-0029 (two or
three differing torsions).

**Proved / assembled.**
* E18: the projector certificate for any lift; identification also when its zero set
  exceeds the support.  By-product: E9(a) without a citation.
* E18′: on finite spaces, flat isolation gives identification among ensembles with at
  most `K` atoms for generic weights.
* E19: the cube with data of even order `≤ 2d`.  The core — no other lifted vertex in the
  span of `(1−ε)n^d/d!` lifted random conformers — we proved for `d = 2` and then found in
  print (Baldi–Vershynin 2019, Theorem 4.2; `DEAD_ENDS.md` ED15).  Built on it: explicit
  `2d`-body energies with prescribed ground states; pair data with a prior on the number of
  conformers reach `n²/2` against `2n` without; a Cover-type upper bound `2n^{2d−1}/(2d−1)!`.
* E20, E20′: generic conformers on a variety (trisecant lemma); tori; two states on a
  torus are identified iff they differ in two angles, with an explicit product
  certificate.

**Computed.**  Exact face decisions for two- and four-body data (`kbody_capacity.py`):
the threshold is at 2.6, 3.3, 3.5 times the sum-of-squares range for `n = 8, 10, 12` —
identification extends far beyond what the natural certificate certifies (Conjecture C3).
The first formulation of the linear programme (equalities kept) was too slow at `n = 14`;
eliminating them through a null-space basis made each solve about fifty times faster.
`n = 22` for pair data: `1.00, 0.58, 0.08, 0, 0` at `K/n = 1.0, …, 1.4`.

**Refuted / withdrawn / rediscovered.**  ED15 (a theorem derived, then found in print);
ED16 (two failures of the new checks that were bookkeeping and tolerance, not
mathematics; grid linear programmes on the torus prove nothing when they find no twin).

**Communicated.**  ENSEMBLE-RES-0003 (geometry, science), ENSEMBLE-MSG-0004 (all).

**Reassessment.**  The most useful new statement for the programme is the table of §4c.5:
in every setting where both are known, *identified* is strictly more than *certified by
the natural sum of squares*, and for four-body data the gap may be of order `n`.  That is
a question about certificates — what a kernel must check beyond a square — and it is put
to the theory and complexity divisions.  The weakest points: Part VI is unreviewed; E19
depends on a theorem whose proof we have not read; C3 rests on three sizes.

---

## 2026-11-26 — Cycle 4 (begun): a certified modulus on the torus; the audit; a Gaussian control

**Proved.**  Proposition E20″: the two-state certificate on a torus grows at least like
`c*·min(d_p², d_q²)` with `c* = min(1, β_min/4)` (three or more differing angles) or
`min(1, β_kβ_l/(4(β_k + β_l)))` (two); hence `∫ min(d_p², d_q²) dν ≤ Λτ/c*` for every measure
whose pairwise product means are within `τ`, and the weights are recovered within
`O(√τ)`.  The growth inequality is machine-checked (`twoStateCert_growth_three`,
`twoStateCert_growth_two`); the kernel rejected the first statement of the two-angle case
(`DEAD_ENDS.md` ED17).  This is the first statement of the report on a continuous
configuration space whose constants are all computable — the science division's
criterion for a non-vacuous guarantee.

**Computed.**  The Gaussian control of E19(f): replacing the lifted vertices of the cube
by a Gaussian cloud of the same size gives face thresholds 78, 142, 214 against the
cube's 76, 152, 233 (four-body data, `n = 8, 10, 12`), and 11, 11.5 against 13, 16 for pair
data (`n = 12, 14`).  So the cube is at least as neighbourly as a generic cloud, with a
ratio that grows with `n`; the asymptotic Gaussian value `D/(2 ln(N/D))` is of order
`n^{2d−1}`, which is the content of Conjecture C3.

**Verified.**  `scripts/audit_all.sh`: AUDIT PASSED (OB9 closed).  Lean: 5125 declarations.

**Proved (continued).**  Proposition E21: for `K` states of a product space, the permanent
of the matrix of coordinate-wise distances to the states is non-negative and, by Hall's
marriage theorem, vanishes exactly at the states when every set `I` of at least two states
has at least `|I|` coordinates at which its members do not all coincide.  On a torus this
identifies the ensemble from multilinear data of order `K`; for `K = 2` it is E20′.  The
zero set is machine-checked (`permCert_eq_zero_iff`, `permCert_zero_set`) with Mathlib's
Hall theorem.  A check that expected the converse on binary sites failed and was
corrected (`DEAD_ENDS.md` ED18).  Lean: 5142 declarations, no warning.

**Applied (second internal review, ER2; the Science division's SCI-REV-0020 and
SCI-RES-0032; the Complexity division's COMPLEXITY-RES-0003, -0007, -0008).**  Report §7
items 9–11.  The one false statement: the title and summary of Theorem E15T claimed a
converse ("and only then") — refuted by a triangle with a violated bond on which the
bound holds (`DEAD_ENDS.md` ED19).  Novelty classes lowered: E5(a), E7, E8 (after
SCI-REV-0020), E15, E15T (after ER2: a union bound over a monotone coupling).  Withdrawn:
the conditional transfer of E20′ to chains (ED21), the thermal bound as a test of the
class (ED22).  A recurring defect — numbers quoted that no script printed — now has a
mechanical check (`check_quotes.py`, ED20).

**Proved (after the review).**  Proposition E15U, the exact condition the review had left
open: for binary sites and any known part, the thermal union bound holds for every
member of the class iff `Var_ν(1_U) ≤ Cov_ν(1_U, N)` for every up-set `U` of the disagreement
order, `ν` the polarised member and `N` the number of disagreements — equivalently
`E[N | U] − E[N | U^c] ≥ 1`.  The same principle (member densities are monotone; the class
contains `1 + t1_U`; "sublinear ≤ linear") characterises the population bound, stochastic
domination and the ordered bound.  Consequences: a necessary condition per site; its
sufficiency at weak coupling (the bound tolerates frustration if every site's bonds are
satisfied on balance); a three-body example in closed form where it is not sufficient.

**Refuted before being stated.**  "For pair-interaction known parts the per-site
condition is the whole condition": true on 17 000 random instances, false on a four-site
instance found by an adversarial search within twenty restarts (ED23).

**Computed.**  Identified against certified at degree 2 on small cubes (for the
Complexity division's Proposition 13): at `n = 12`, `K = 9`: 92 % faces, 0.5 % with a
degree-2 certificate.  Four-body data at `n = 14`: first row only (`K = 280`: all faces).

**Verified.**  `scripts/audit_all.sh`: AUDIT PASSED (5145 declarations).  `run_all.py` with
`check_quotes.py`: all pass.

**Communicated.**  ENSEMBLE-RES-0004 (science), -0005 (geometry, complexity, theory),
ENSEMBLE-MSG-0005 (all; a linked correction of ENSEMBLE-MSG-0003).

**Reassessment.**  Two of the division's headline statements have now been reduced by
review to their true size: Part II is a corollary of a published theorem with an
unpublished reading; the thermal union bound is a union bound.  What survives with
content of its own: the exposedness characterisation with its bridge to the theory
division's certificates (Part I), the capacity statements on the cube and the
identified-versus-certified table (Parts III, VI), the certified modulus on the torus
(E20″), and — new today — the exact condition E15U.  The honest ranking of what to do
next puts *unreviewed new statements* first (E15U, Part VI) and *threshold proofs*
second; volume is not the constraint, depth is.

---

## 2026-11-26 — After checkpoint 4: the supplementary directive; the review of Part VI arrives

**Directive.**  The research owner authorised a seventh division (software and
applications, branch `research/structural-biology`) and asked us for constructive forms of
our results, wider observation models, partial identification and impossibility results,
a software-facing account of what is implementable, and benchmark controls.

**Done.**  `SOFTWARE_INTERFACE.md`: one card per result with inputs, outputs, cost, what a
checker verifies, when a tool must abstain, and a readiness level (R3: identification
with certificate and stability on enumerable spaces, exact intervals, the bridge to
robust optimality, the thermal bound's evaluation, Kahle's worst-case theorem; R2: noise,
first-order classes, the projection certificate; R1: laws of distances, tori, E15U; R0:
thresholds).  The observation that organises it: on enumerable spaces checking a
certificate is easier than constructing it and needs no solver; on large product spaces
constructing is cheap and *checking* is NP-complete.  `BENCHMARK_CONTROLS.md` and
`benchmark_controls.py`: eighteen reference instances in seven families, every verdict
verified in exact arithmetic before it is written.  Proposition E17.1 (three reductions
for observation models).  ENSEMBLE-MSG-0006 to the new division.

**Received.**  The internal review of Part VI (ER3): no numbered statement false; two
major and nine minor findings; committed as received (`7eb9cae`), **not yet applied**
(OB24).  Its most consequential points: a remark of ours counted conditions wrongly (the
conclusion holds for another reason — no three states on a torus of two angles are
determined by bilinear data); a published theorem (Kahle 2010) gives the worst-case
capacity `2^t − 1` on product spaces and supersedes E21 there; five generic states on
`𝕋³` are identified (a two-line theorem), six are not (numerical).

**Next.**  Apply ER3 with OB20 (Part VI).  Then the research items of the directive:
certificate formats on product spaces; data that are not linear in the ensemble
(nothing covers them); certified lower bounds on the number of conformers; a review of
E15U and E17.1.

---

## 2026-11-26 — Checkpoint 5: the review of Part VI applied; crossings with the Science division

**Applied (ER3).**  Report §7 item 14.  The one false sentence was a count of conditions
that had never been computed (`DEAD_ENDS.md` ED24); the review replaced it by a theorem
(E22: no three states on a torus of two angles are determined by bilinear data) and
added a second (E20a: five generic states on three angles are).  We re-derived both and
the two new constants of E20″ before taking them in.  Kahle's theorem (2010) is the
worst-case capacity on product spaces; our E21 is weaker there.

**Crossing.**  Our fourth checkpoint printed in bold a sentence of the Science division
("only bang-bang members are pinned by averaged data") that it had withdrawn forty-seven
minutes earlier, in a message we had not yet fetched; removed (SCI-RES-0037).  The same
division re-derived and replicated the main statement of E15U (SCI-RES-0038) within
half an hour of our asking.

**Literature.**  Johnston–Lovitz–Vijayaraghavan (FOCS 2023), pointed out by the Geometric
Inference Division: the problem "does this span meet this variety in no other point" —
the checking problem of every lifted certificate — has an algorithm with certificates
for generic instances and is NP-hard in the worst case.  It is a published answer, for
generic instances, to the question we had put to the theory division (E-T4).

**Verified.**  `run_all.py` (seven scripts, then `check_quotes.py`): all pass.

**Communicated.**  ENSEMBLE-MSG-0007 (all; linked correction of ENSEMBLE-MSG-0004,
ENSEMBLE-RES-0003, ENSEMBLE-RES-0005 §2), ENSEMBLE-RES-0006 (science, geometry).

**Reassessment.**  After three internal reviews and two external ones the pattern is
stable: the numbered theorems survive; what fails are sentences that generalise from
them — a converse (E15T), a count (E21 Remark 3), a quoted reading (the sandwich) — and
numbers written from exploratory runs.  The remedies in place: `check_quotes.py` for the
numbers, adversarial search before any "in every instance tried", and reviews before a
statement is offered for implementation (`SOFTWARE_INTERFACE.md` readiness levels).  The
most valuable new mathematics of the day came out of the reviews themselves (E15U from
ER2's open question; E20a and E22 from ER3).  Next research should go where nothing we
have applies: data that are not linear in the ensemble.

---

## 2026-11-26 — After checkpoint 5: the eighth division; data that are not linear in the ensemble (Part VII)

**Directive.**  The research owner's second supplementary directive (about 22:40 UTC)
authorises an eighth division, Frontier Benchmarking (`research/frontier-benchmarks`).
Our protocol copy recognises eight divisions (`docs/collaboration/README.md`, third
addendum, with the six rules that bind us); the benchmark controls are marked as public
development material, not held-out evidence.  Its branch did not exist at 22:44 UTC; it
was founded at 22:54 UTC and had sent nothing at 23:07 UTC.

**Investigated.**  What remains of Parts I and V when a datum is not a mean.  We took
the largest class for which the answer is finite-dimensional: data that are functions
of finitely many means, `y = G(E_μΦ)`.

**Found** (report §4d; all [P], elementary, unreviewed).  E23: ratios and one unknown
calibration factor are linear; the factor costs exactly the constant in the
certificate.  E24: in general the loss is the fibre of `G` in the moment body; the
values of a target form a union of intervals.  E25: the length of a mean vector
identifies only at its least or largest possible value; at the least value the support
has a linear modulus and the weights a square-root modulus.  E26: squared means are `2^m`
linear problems; consistency is NP-complete.

**A mistake of ours, found while writing this.**  ENSEMBLE-MSG-0006 and
`SOFTWARE_INTERFACE.md` said that ratios of averages "are covered by nothing".  A ratio
with a positive denominator is a pair of linear constraints (`DEAD_ENDS.md` ED25).

**Self-review before the commit** (there was no reviewer).  Re-reading the Part against
its proofs found three sentences that said more or less than was proved, corrected
before publication: (i) "the range of a target is `[inf, sup]` over the fibre" — it is a
union of intervals and need not be an interval when the fibre is disconnected; (ii)
"the square-root bound is attained up to the term `τ²`" — it is attained exactly when the
nearest face is not a point, and the linear bound is attained when the nearest point
lies inside a facet (not otherwise in general: in a cloud in space whose nearest face
is an edge it is not); (iii) membership in NP of the consistency problem needs the data
as rational `√y_i`; and hardness holds in the strong sense, by exact cover by 3-sets
(scratch test: 60 of 60 instances agree with brute force; to be added to the script).

**Machine check, not yet committed.**  The sufficiency half of E23(b):

    theorem eq_of_homogeneous_certificate (Φ : ι → X → ℝ) (μ ν : X → ℝ)
        (hμ : IsEnsemble μ) (hν : IsEnsemble ν) (S : Finset X)
        (hsupp : ∀ x, x ∉ S → μ x = 0) (lam : ι → ℝ)
        (hzero : ∀ x ∈ S, energy lam Φ x = 0) (hpos : ∀ x, x ∉ S → 0 < energy lam Φ x)
        (hindep : ∀ h : X → ℝ, (∀ x, x ∉ S → h x = 0) → (∀ i, ∑ x, h x * Φ i x = 0) → ∀ x, h x = 0)
        (t : ℝ) (hdata : ∀ i, mean ν (Φ i) = t * mean μ (Φ i)) : ν = μ

type-checks with the standard axioms, with a witness on three configurations.  It
enters `proofs/` after the audit has passed on the tree that contains it.

**Verified.**  `run_all.py` (eight scripts, then `check_quotes.py` with 87 entries): all
pass; `benchmark_controls.py`: 22 instances, 33 exact verifications.

**Communicated.**  ENSEMBLE-MSG-0008 (all; linked correction of ENSEMBLE-MSG-0006 §5;
question E-S5 to Science and Structural Biology).

**Reassessment.**  The non-linear data that reduce to linear problems (ratios, a common
factor) are probably the ones that matter most in practice, and they cost nothing; what
costs — lengths, squares — costs a search whose size is exponential in the number of
such data, and for squares provably so.  The class "functions of finitely many means"
is exhausted as far as structure goes; the next uncovered ground is data that are not
of that class at all, and noise for non-convex compatible sets.  Part VII is the only
Part without a review: commission one before building on it.

---

## 2026-11-26 — The torus of three angles: a count that had been made wrongly, made where it belongs

**Trigger.**  Waiting for the audit of the homogeneous certificate, we returned to the one
statement of Part VI that was numerical on one side: "six generic states on `𝕋³` are not
determined" (review ER3: twins in 10 of 10 instances, and the remark that on the curve
the 27 products span 12 functions while six double zeros are 12 conditions).

**Idea.**  In real coordinates `t = tan(φ/2)` everything is polynomial with rational
coefficients.  A non-negative function of the data span that vanishes at the states has
a vanishing derivative along the curve `Z` where the lifted certificate vanishes: twelve
linear conditions on a 27-dimensional space that contains the 15-dimensional space of
functions vanishing on `Z`.  If the rank is 12, nothing else satisfies them, every
candidate certificate vanishes on the whole curve, and the chain of Theorem E1(b) never
leaves the curve.  No algebraic geometry is needed for the proof — only a rank, which
is exact at rational points.

**Proved.**  Theorem E20b (six states in general position: never), with exact ranks at
two rational six-tuples.  The numerical input of E20a replaced by a Gröbner-basis
computation in the eight charts plus semicontinuity; at the instance the sixth zero is
a rational point.

**Found while testing the rank.**  Moving the sixth state along the curve through the
other five, the determinant of the twelve conditions changes sign — at the "sixth zero"
of the five (dependent lifts; five states and their ghost are an identified six-state
ensemble) and at other points, where the lifts are independent and the rank is 11.
There the extra function `q_0` is semidefinite on the curve when the curve has one real
component, and a certificate `A(g_1² + g_2²) + q_0 + i` is non-negative on the whole torus
with exactly six zeros: **six states are determined on a hypersurface** (Proposition
E20c), by a certificate that cannot be a sum of squares of lifted forms.  With two real
components the signs of `q_0` on them may differ, and then there is a twin.  Explanation
(genus one, half-periods) recorded as an explanation.

**A sentence we wrote and withdrew before committing.**  "A test that answers
'identified' at such a configuration is right, and useless."  Wrong: the certificate
has quadratic growth, so every measure with nearly the same data is concentrated near
the six states, on both sides of the hypersurface.  What is discontinuous is the
verdict, not the information.  The paragraph now says that.

**The count for every `r`** (Proposition E20d).  The plain count of double points is an
upper bound — 17 states on four angles — because the conditions are independent for
`r ≥ 4` by a published theorem (Laface–Postinghel), whose only exceptions in these
degrees are three points on `(ℙ¹)²` and seven on `(ℙ¹)³`: exactly the two tori on which our
third checkpoint had read a threshold off the count (`DEAD_ENDS.md` ED24, with a sequel).
Sixteen random states on `𝕋⁴`: the unique function with sixteen double points is a saddle
at some state in every instance tried.

**Machine check.**  `Ensemble.eq_of_homogeneous_certificate` and its witness are in
`proofs/`; `scripts/audit_all.sh`: AUDIT PASSED (5147 declarations).

**Finished in the background.**  Four-body data at `n = 14`, ten supports per `K`, about
four hours on one core: face frequency `1.000` at `K = 320`, `0.200` at 340, `0.000` at 360.
The Gaussian cloud of that size has its threshold at `295.8` (new script
`gaussian_threshold.py`, the review's method): the ratio cube/Gaussian has grown at each
of the four sizes (`0.98, 1.04, 1.09`, then between `1.08` and `1.15`).

**Prior art found — and one of our theorems is in print.**  The Structural Biology
division's intake report lists what our prior-art register lacks.  A bounded search
(§6 item 20 of the register) found: (i) **Theorem E1(b) is Theorem 18 of di Dio and
Schmüdgen (2018)** on the determinacy of truncated moment functionals, and the chain of
our proof is Fialkow's core variety — we had it as "known in substance" from memory of
older sources; the first-checkpoint search never used the word "determinacy"; (ii) the
upper end of the interval of E2(a) for the weight of one conformer is the "maximum
occurrence" of Bertini, Luchinat, Parigi and co-workers; (iii) the mechanism of E20b and
E20c on the curve (faces ↔ totally real divisors, two-torsion, connectedness of the real
locus) is in Baldi, Blekherman and Sinn (2024), found an hour after we wrote the
explanation.  Recorded in the report and the register before the commit.  *Lesson: the
literature of a statement lives under the name its field gives it — "determinate
moment functional", not "identified ensemble".*

**Verified.**  `torus_six_states.py` (S1, S2, S5 exact; S3, S4, S4b, S6 numerical);
`run_all.py` (nine scripts, then `check_quotes.py`, 113 entries after the last edits of
the text — re-run with the new option `--quotes-only`): all pass.

**Communicated.**  ENSEMBLE-MSG-0009 (all; linked update of -0007 and -0008; question
E-T5; acknowledgements of THY-MSG-0019 §5, COMPLEXITY-REV-0005, GEOMETRY-MSG-0009).

**Reassessment.**  The dead end ED24 turned out to be a method applied in the wrong
place.  Two things follow for the open problem O10: for four angles the question
"thirteen to sixteen states" is now a finite-dimensional positivity question on a real
curve or surface that a linear programme can decide instance by instance; and "the
largest number of generic states" may not exist over the reals, because identification
beyond the lifted range is a semialgebraic condition that can hold on an open set and
fail on another.  The answer owed to the Structural Biology division comes first.

---

## 2026-11-27 — Incomplete models (Part VIII); the answer to the Structural Biology division; ER4 commissioned

**Trigger.**  The Structural Biology division's intake report on our work ends each of
its register entries with "becomes useless when": the truth is not in the library, the
forward-model error exceeds the data accuracy, the number of conformers is unknown.
The research owner's directive names the same things ("model misspecification",
"unknown ensemble complexity", "unknown or imperfect observation functions").

**Proved** (all elementary; checks M1–M4 passed at the first run, which after this
week's record we note without drawing a conclusion from it).
*E23.1:* several unknown gains and offsets keep the problem linear; identification is
Theorem E1(a) for the features projected off each group's data direction — one
direction of the certificate lost per gain.  *E27:* the perspective of a convex function
makes a two-time-scale average convex in the ensemble; with Jensen on both sides it is
bracketed by `g(E φ)` and `E g(φ)` for every partition, so the bracket is a convex
constraint that needs no knowledge of the time scales.  This is the first statement we
have for a datum that is *not* a function of finitely many means.  *E28:* an incomplete
library is a tolerance `εD`; a library that the data falsify comes with a certified
lower bound on the missing weight, computable from the library and bounds on the
observables; tight by duality; no upper bound exists.  *E29:* `K_max` is the size of the
zero set of a certificate, `K_min` is NP-hard with rank lower bounds, and identification
is `K_min = K_max`.

**Communicated.**  ENSEMBLE-RES-0007 to the Structural Biology division: the constants
and statements that its register quotes from our `8d42f60` and that have changed; its
table of data types as mathematics; its prior-art observation confirmed (E1(b) in
print; maximum occurrence).  Controls B9-01 to B9-03.

**Commissioned.**  The internal review ER4 of everything unreviewed up to `b654396`.

**Reassessment.**  Part VIII is the least deep and possibly the most useful thing
written this week: none of it needed more than convexity and duality, and each
statement turns a sentence of the form "the method is useless when …" into a test with
a certificate or a bound with a constant.  The deep open questions are where they
were: the capacity thresholds (C2, C3), the torus of four angles, a modulus for
distance distributions (O4).  The next mathematics should go to the torus of four
angles, where the method of E20b reduces an open question to a positivity problem on a
real curve.

---

## 2026-11-27 — The eighth division's feedback: five items, four answers, one correction of the question

**Synchronised (00:18 UTC).**  All seven other branches had moved.  The Frontier
Benchmarking division exists, has determined that nothing of MetricChain takes part in
CASP17, and has published `MATHEMATICAL_FEEDBACK.md`: for each division, the conclusions
an evaluation could not draw and the statement that would allow them.  Five items for
us.  The research owner's directive for this case: "investigate whether it motivates a
stronger theorem, a constructive algorithm, a generalization, or a rigorous
obstruction".

**E-1 (scale and offset).**  Already Proposition E23.1 of the previous commit; added the
version with tolerances.  The trick that makes it linear for any number of gains is to
divide the data by the gain (`t = 1/s`) instead of multiplying the ensemble by it.

**E-2 (pool refinement).**  Proposition E30: push an ensemble on the continuum forward
to the net; intervals and mass bounds survive with `τ → τ + Lh`.  Honest number: with
`Lh` 5 to 40 times `τ` the certified enclosure is 34 times too wide.

**E-3 (identifiability radius).**  The item proposed "a linear programme with a dual
certificate".  It is not one: the radius is the largest width of a population interval
over all subsets, a convex maximisation, and deciding whether it equals one is
NP-complete (a hyperplane section of a cube encodes the partition problem).  What can
be certified: `max_x w_x ≤ R ≤ ½Σ_x w_x`.  A rigorous obstruction and a constructive
substitute — the outcome the directive lists.

**E-4 (modulus for distance distributions).**  Our Problem O4; nothing.  But the
counting proof of Theorem E4 is quantitative as it stands: `mε/(m − K(r−1))`, and the
linear programme attains it.  Recorded as E4.1 with its limits.

**E-5 (error sets).**  Proposition E17.2: the support function.  A systematic direction
forces the certificate to be orthogonal to it — the same phenomenon as an offset in
E-1, which unifies the two.

**Thirteen states on four angles** (Proposition E20e).  The count of E20b on the curve
leaves ten candidates; a linear programme on the traced curve decides.  40 random
instances: 26 determined (certificates checked on the whole torus), 10 not (twins,
positive dual margins), 4 undecided.  Two bugs of the *verification* on the way, both
of the kind "threshold not scaled with the certificate's scale factor": the first
version rejected valid certificates; the dimensions 36, 26, 10 agreed with the count in
every instance.  Conclusion: no generic answer over the reals.

**Geometry (GEOMETRY-MSG-0010).**  It proved that averaged squared distances among
sparse labels determine nothing and left "distributions instead of means" to us: our
E7/E8 give identification from exact laws (or `2K` moments) of the distances among five
or more labelled sites, with no stability.

**Requested.**  ENSEMBLE-REQ-0001 to engineering: independent re-implementation of the
control instances, of the ranks behind E20b and of ten verdicts of E20e.

**Verified.**  `robustness_checks.py` (R1–R5), `torus_four_angles.py` (T1, T2; survey
stored); `run_all.py` (twelve scripts, then `check_quotes.py`): all pass.

**Reassessment.**  The Frontier division's feedback is the most useful input this
division has had from outside: each item named an assumption, and each answer is a
short proof — except the one it called a linear programme, which is a hardness result,
and the one that is our oldest open problem.  Today's statements are the least
reviewed part of the report (OB29, OB30); ER4 covers none of them.  Before more is
added, the review should catch up.

## 2026-11-27 — Consolidation and halt (research owner's directive, received about 01:00 UTC)

**What was in progress and was finished.**  (1) The answer to the Science division's
table of observables: report §4e.5; E27(c) for vectors; Proposition E32 for bilinear
data — begun as a remark that "no certificate of identification is known", it became a
proposition when the certificate turned out to be elementary: exclusion vectors on a
subdivision of the parameter box plus an explicit neighbourhood of the true parameter
(`bilinear_checks.py`: five planted instances certified exactly with 67 to 203 cells; a
twin; outer bounds; the Gaussian count is Wendel's formula).  ENSEMBLE-RES-0009.  (2) The
Lean statement of the counting inequality of E4.1; audit passed (5151 declarations).
(3) The internal review ER4: the reviewer was asked to stop and write up; report
committed as received (`87bb28a`), then applied (report §7 item 21; thirty edits in five
files).

**What the last review taught.**  As with ER1–ER3, no numbered statement was false and
several sentences about them were.  The most consequential finding is about originality,
not correctness: the mechanism of E20b and E20d is a theorem of the paper we had already
cited for E1(b) (di Dio–Schmüdgen, Theorem 40), which we had read only as far as its
Theorem 18.  A second paper we cite (Baldi–Blekherman–Sinn) probably contains E20b and
E20c on a given curve.  Reading cited papers to the end would have been cheaper than
re-deriving them.

**Not done, deliberately.**  No new literature search; no review of E32, E23.1, E27–E31,
E17.2, E20e; no full re-run of `run_all.py` after the last text changes (`--quotes-only`
passes); the other divisions' newest messages were read by header only.

**Assessment** (`docs/collaboration/consolidation/ensemble.md`).  The framework is known;
three narrow groups of results may be original; the useful output is elementary; the
decisive open question is empirical — whether certified intervals are informative on
realistic problems.  Halted.
