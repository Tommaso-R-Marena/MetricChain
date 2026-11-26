# Implementation guide — what of this division's mathematics can be turned into software, and what must not be

**Geometric Inference, Rigidity and Inverse Problems Division**, for the Structural Biology
division (which writes the software), the Engineering division (which verifies and runs
it) and the Frontier Benchmarks division (which evaluates it).  Written at the eleventh
checkpoint in answer to the research owner's supplementary directive of 2026-11-26.  This
division writes no production software; the scripts named here are research code that
defines the semantics and serves as a reference for tests.

Source commit for every statement below: the commit that adds this file, on
`research/geometric-inference` (the mathematics is in `docs/geometry/ENSEMBLE_RIGIDITY.md`,
`HINGE_ENSEMBLES.md`, `LOCAL_DATA_STABILITY.md`; one row per statement in
`THEOREM_REGISTER.md`).  Labels: **[V]** machine-checked in Lean, **[P]** proof on paper,
**[P-exact]** proof on paper whose finite part is an exact computation, **[K]** known,
**[N]** numerical, **[C]** conjecture.  "Reviewed" always means an internal review by an AI
session of this or another division — never external peer review.

---

## 0. Four notions that are not interchangeable

For an ensemble `μ` (a probability distribution over conformations of one chain) and data
`M(μ)`:

| notion | definition used here | how it is decided | example where it holds and the next one fails |
|---|---|---|---|
| **global identifiability** | no other ensemble — with any number of states, or a continuous one — has the same data | a theorem, or a certificate (below) | two generic states with 9 points: holds numerically, no certificate known |
| **local identifiability** | no *nearby* ensemble *with the same number of states* has the same data | the rank of a Jacobian | two states with 8 points: holds, and a 9-state ensemble has the same data (instance C1) |
| **algorithmic recoverability** | a stated algorithm returns `μ` from `M(μ)` | run it; its output is correct only together with a certificate | DEMIX below the conic threshold with `K` supplied returns something; it is not `μ` |
| **efficient certification** | a polynomial-size computation whose success *proves* global identifiability for the instance | a rank in exact arithmetic (or with a reported gap) | linear certificate from 12 points for two states; quartic from 11 (10 modulo a known point) |

A tool must say which of the four it has established.  "The optimiser converged to the
truth on synthetic data" establishes none of them.

Thresholds for chains with fixed bond lengths and bond angles, generic states (number of
points `n`):

| states `K` | locally identifiable | globally identifiable | certified: quartic | certified: linear (conic condition) |
|---|---|---|---|---|
| 1 | 4 | 5 [P] | — | 5 [P] |
| 2 | 7 [P-exact] | 10 [P-exact]; 9 [N]; **not** at 7, 8 [N, explicit second solutions] | 10 (modulo the structural point), 11 [P-exact] | 12 [P-exact] |
| 3 | 9 [P-exact] | 16 [P-exact]; 14, 15 [N] | 16, 17 [P-exact] | 23 [P-exact] |
| 4 | 11 [P-exact] | 30 [P-exact]; conjectured 19 | 30 [P-exact]; conjectured 24 | 39 [P-exact] |
| `K` | `2K + 3` (`K ≤ 8` exact) | conjectured `⌊9K/2⌋ + 1` | at least `6K − 1` and about `0.89K²` | `⌈(9K² + K + 8)/4⌉` (`K ≤ 20` exact; a weaker bound for all `K`) |

"Generic" means outside a proper algebraic subset that is not described; **an
instance-specific guarantee comes only from running the certificate on the instance.**

---

## 1. The observable, and its distance from measurements

Everything in §§2–5 takes as data the matrix `M_ij = ⟨|x_i − x_j|²⟩` of ensemble-averaged
**squared** distances between **labelled** points, for **all** pairs, **exactly**.  This is
an idealised observable.  We know of no measurement that returns it, and we have not
justified substituting it for any.  The gaps, as mathematics:

| idealisation | what a measurement differs in (as far as this collaboration has established) | what we have | what is missing |
|---|---|---|---|
| all pairs | only some pairs, or only linear functionals `⟨C_a, M⟩` (block sums — the Science division's analysis of labelled scattering, SCI-RES-0029) | Theorem F (a stress certificate for a subset of pairs; instances exist for scattered pairs), Theorem F″ (the same for linear functionals; **no instance**) | a certificate *producer* (a semidefinite programme) specified and tested; thresholds |
| squared distances | other averages of the distance (inverse powers, transfer efficiencies) are not quadratic in the coordinates | nothing: the stacking lemma fails | a theory |
| second moments | distance *distributions* (laws) carry more | Theorem J (laws at separations 3 and 4 determine generic finite ensembles), resting on the Ensemble division's E5/E6 | constructive version; noise |
| exact data | noise | Theorem G: `W₂² ≤ C·‖ΔM‖` with a constant `κ` that is **not computed** (a global infimum); numerical thresholds of one implementation | a certified `κ` (`PROOF_OBLIGATIONS.md` O-5) |
| finitely many states | a continuous part | an obstruction: an ensemble with a continuous part is **never** determined (Corollary 4.2 (c)) | what *is* determined (moments), as a theorem with constants |
| the same bond lengths and bond angles in every state, exactly | fluctuating local geometry; coarse-grained traces whose virtual bond angle varies with the conformation | an obstruction for unconstrained states (Proposition 3.1); the certificates *refuse* when the supplied constraints are false (instance G1) | a tolerance version |
| states in general position | states that share rigid parts (the common case of a hinge motion): the conic condition fails | `HINGE_ENSEMBLES.md`: a complete answer for two states (first by the Science division) | more than two states |
| labelled points | unassigned data | nothing | — |

So: **no statement in this guide is a statement about a real molecular system.**  The
software consequences that survive the idealisation are of two kinds — (i) *checkers* that
decide, for given synthetic or model data, whether a claimed identification is certified;
(ii) *obstructions* that a tool claiming more must contradict (§6).

---

## 2. Specification S1 — data model, stacking, and the first refusal

* **Statement [K/P].**  For `μ = Σ_k w_k δ_{X_k}`, `M(μ)` is the squared-distance matrix of the
  *stacked configuration* `z_i = (√w_k x_i^{(k)})_k ∈ ℝ^{3K}`; every ensemble with the same
  data consists of linear images of `z` (Lemma 2.2).  **Lean [V]:** `stacked_sqdist`,
  `exists_linearMap_of_gram_eq`, `state_is_linear_image` (finite mixtures;
  `proofs/Geometry/EnsembleRigidity.lean`, namespace `MetricChain.Geometry`).
* **Input.**  A real symmetric `n × n` matrix `M` with zero diagonal; the statewise
  constraints: a set `E₀` of pairs and their lengths `ℓ` (for chains: `|x_i − x_{i+1}|` and
  `|x_i − x_{i+2}|`), asserted to hold in every state.
* **Computation.**  `G = −½JMJ` (`J = I − 𝟙𝟙ᵀ/n`); eigen-decomposition; `r = rank G`; `Z = V_rΛ_r^{1/2}`.
* **Refuse** if `G` has a negative eigenvalue beyond tolerance (the data are not averaged
  squared distances of anything) or if `r` is not a multiple of 3.  `K := r/3`.
* **Semantics of `K`.**  For exact data of a `K`-mixture whose stack spans, `r = 3K`.  The
  converse is false: `r = 3K` does not make the data those of a `K`-mixture.
* **Complexity.**  `O(n³)`.
* **Conditioning.**  The smallest non-zero eigenvalue of `G` is of the order of
  (smallest weight) × (squared separation of the states in their least different direction);
  for nearly equal states the rank decision is ill-posed (instances F1a, F1b).  Report the
  eigenvalue gap; do not hide it in a tolerance.
* **Counterexamples to what one might assume.**  Mixtures of ideal helices and of planar
  states do not have rank `3K` (instance G3); a continuous ensemble can have a rank that is
  not a multiple of 3 (G2) — or one that is.
* **Reference code.**  `experiments/geometry/demix.py`, step 1.

## 3. Specification S2 — the linear certificate and DEMIX

* **Statement.**  *Theorem B [P; reviewed: Science division SCI-REV-0021 "proved as stated";
  internal review GEOMETRY-REV-0001; for `d = 1` known — Laurent–Poljak 1996].*  If the only
  quadrics `S ∈ Sym(3K)` with `eᵀSe = 0` on all `E₀`-edge vectors `e` of `z` are the `K − 1`
  trivial ones (the **conic condition**, CC), then `μ` is the only ensemble with its data.
  *Proposition 6.1 [P].*  If `M` is the data of *some* ensemble with the supplied constraints,
  `rank G = 3K`, and the solution space of the linear system below has dimension exactly
  `K − 1`, then that ensemble is a `K`-mixture, it is the only ensemble with these data, and
  DEMIX returns it.
* **Lean [V].**  `mixture_identifiable_stacked` (Theorem B in coordinates, against finite
  competing mixtures; with `∑ w = 1`), `finite_mixture_identifiable`, `block_rigidity`,
  `mixture_state_of_conic`; a two-state instance used end to end (`line_mixture_example`).
  The Lean statements are for finite mixtures; the measure-theoretic step is on paper.
* **Input.**  As S1.  **Output.**  Either `(K, states up to congruence — mirror images
  included —, weights, certificate)` or a refusal with its reason.
* **Computation.**  With `Z` from S1: the homogeneous linear system `eᵀSe = 0` for
  `S ∈ Sym(3K)`, one equation per constrained pair (`2n − 3` equations, `3K(3K + 1)/2`
  unknowns).  **Certificate: nullity `= K − 1`.**  A generic element of the null space has `K`
  eigenspaces of dimension 3 — the coordinate blocks of the states; the weights from one
  constrained length.
* **Complexity.**  `O(n³ + nK⁴)`; needs `n ≥ ⌈(9K² + K + 8)/4⌉` points.
* **Assumptions that the certificate checks by itself:** that the data are those of a
  `K`-mixture in general enough position.  **Assumptions it cannot check:** that `M` is the
  averaged squared-distance matrix of an ensemble *whose every state satisfies the supplied
  constraints*.  If that is false the output means nothing (and the certificate usually
  fails — instances G1, G4 — but this is not proved).
* **Conditioning.**  Two rank decisions (the rank of `G`; the nullity).  In floating point
  report the ratio of the last accepted to the first rejected singular value for both.  On
  synthetic data with noise our implementation loses the certificate at relative noise
  about `7·10⁻³` for two states with 12 points and `8·10⁻²` with 16 [N, one implementation].
  **No noise guarantee is proved with a computable constant.**
* **Known failures.**  Below the conic threshold (instances B1, B2, E1, E2); states that
  share rigid segments (hinges: CC fails for at most three differing torsions, although the
  ensemble may be identifiable — instance C3 is the non-identifiable case); nearly equal
  states.  In all of them the correct output is "not certified".
* **Validation criteria.**  On instances A1–A3: `K`, the states to RMSD `10⁻⁶` up to
  congruence and permutation, the weights to `10⁻⁶`, nullity `K − 1`.  On B, C, E, G
  instances: a refusal.  A tool that returns states on C1 without saying that they are not
  certified fails.
* **Reference code.**  `demix.py` (`demix(M, edges, lengths)`, exact-data mode when `K` is not
  supplied).  Exact arithmetic for the certificate on rational instances:
  `exact_conic_rank.py`.
* **Readiness.**  Ready as a checker and as a reference algorithm on exact synthetic data.

## 4. Specification S3 — the quartic certificate and DEMIX-4 (exploratory)

* **Statement.**  *Proposition 6.2 and Theorem I′ [P and P-exact; **unreviewed**; the mechanism
  is the published algorithm of Johnston–Lovitz–Vijayaraghavan 2023 for linear sections of
  varieties].*  Let `L` be the space of `(P, c)`, `P ∈ Sym(3K)`, with `eᵀPe = c·ℓ_e²` on the
  constrained edges, `m = dim L`.  If the `4 × 4` minors of `P`, as quartic forms on `L`, span a
  space of codimension exactly `K` (`h_4 = K`), then the only matrices of rank at most 3 in
  `L`, real or complex, are the multiples of the `K` state projectors; the ensemble is the
  only one with its data; the states are obtained by linear algebra.  If `n = 6K − 2` the
  same conclusion (without the recovery, which is described but not implemented) holds when
  the codimension is exactly `K + m`.
* **Lean.**  None.
* **Input / output.**  As S2.
* **Computation.**  Rank of a matrix with `C(m + 3, 4)` columns (`m = 3K(3K+1)/2 + 4 − 2n` below
  the conic threshold) and one row per `4 × 4` minor (**all** minors: a random subset does
  not span the same space); then a null-space contraction and one eigen-decomposition.
* **Complexity.**  Polynomial for fixed degree, impractical beyond a few states: 15 columns
  (`K = 2, n = 11`), 3 060 (`K = 3, n = 17`), 12 650 (`K = 4, n = 30`, 27 minutes in exact
  arithmetic), 66 045 (`K = 4, n = 24`, not attempted).
* **Conditioning — the main warning.**  **In floating point the rank defect is not reliable**
  (three states, 16 points: 21 and 24 in two runs, 20 exactly; `DEAD_ENDS.md` DG-23).  As a
  *certificate* this computation must be done in exact arithmetic on rational (or modular)
  data, where only lower bounds on ranks are used; in floating point it is a heuristic
  whose recovered states must be re-verified (the verification of Proposition 6.2 (c):
  `K` positive semidefinite matrices of rank 3 in `L` with orthogonal ranges and a positive
  combination equal to the identity).
* **Validation criteria.**  B1, B3: certificate and recovery; B2: defect `K + m`; A instances:
  consistent with S2; C, E instances: no certificate.
* **Reference code.**  `exact_demix4.py` (exact, certificate only), `demix4.py` (floating
  point, certificate and recovery).
* **Readiness.**  **Exploratory until independently reviewed.**  Do not ship as a guarantee.

## 5. Specification S4 — certificates for incomplete averaged data (checker only)

* **Statement.**  *Theorem F [P; core V: `stress_certificate`, `stress_energy_eq`,
  `mixture_energy_eq`; reviewed on paper].*  Let `μ` satisfy CC and let `F` be the measured
  pairs.  If there is a symmetric `Ω ⪰ 0` with `Ω𝟙 = 0`, supported on `F ∪ E₀` and the
  diagonal, with `ker Ω = span(𝟙, columns of z)`, and the vectors `(D(X_k)_ij)_{ij∈F}` are
  affinely independent, then `μ` is the only ensemble with its averaged squared distances
  on `F`.
* **What can be implemented now: the checker.**  Input: the candidate `μ` (states, weights),
  `F`, `Ω`.  Checks: symmetry and support of `Ω`; `Ω𝟙 = 0`; `Ωz = 0`; positive semidefiniteness
  with rank exactly `n − 1 − 3K` (an `LDLᵀ` factorisation — in exact arithmetic for a
  certificate; the Theory division's advice, THY-MSG-0018 §4, is a rational factor checked
  by one matrix identity); CC for `z` (S2); affine independence.  Complexity `O(n³)`.
* **What is not specified: the producer.**  Finding `Ω` is a semidefinite feasibility problem
  with a rank condition.  Instances were found by the internal referee's programme
  (`review1/k_stress.py`, needs `cvxpy`): for two states with 14 or 16 points such a stress
  exists for bands `3 ≤ |i − j| ≤ 7` and for 45 or 55 random pairs of 66, and **does not
  exist** for bands `≤ 6`.  No theorem says when it exists.
* **Readiness.**  Checker: ready.  Producer: exploratory.  Quantitative version (Theorem G):
  the constant `κ` is not computable at present — **do not print an error bar from it.**

## 6. Specification S5 — states that share rigid segments (hinges)

* **Statement.**  *Theorem M [P; count P-exact; the main statement is the Science
  division's Proposition R22-1, earlier; two independent derivations agree].*  Two states
  that differ in one torsion are never determined (only the mean of `(cos, sin)` of the
  hinge angle is).  Two states that differ in two torsions, with rigid segments on no
  conic: exactly eight chains are linear images of the stack (mirror assemblies), and the
  ensemble is determined iff at most one of the rotations `R_1`, `R_2`, `R_1R_2` is a
  half-turn.  More differing torsions: determined.
* **Computation.**  Detect the rigid segments: maximal runs of consecutive points whose
  principal submatrix of `M` has a centred Gram matrix of rank 3 (all states are congruent
  there; a run that contains a hinge has larger rank); the hinges are the bonds shared by
  consecutive runs.  For two hinges build the eight candidates; a linear programme over
  their squared-distance matrices decides uniqueness.  Small, and exact in principle.
* **Counterexamples supplied.**  Instances C2 (one hinge) and C3 (two half-turns) with
  explicit second solutions.
* **Readiness.**  Ready as a reference computation for two states
  (`hinge_pairs.py`, `hinge_halfturns.py`, `exact_hinge_candidates.py`); more than two
  states: open (three states at two hinges can fail).

## 7. Specification S6 — local identifiability (a diagnostic, not a certificate)

* **Statement.**  *Theorem H [P-exact for `K ≤ 8`].*  Generic `K`-state ensembles are locally
  identifiable among `K`-state ensembles from `n = 2K + 3` points (complete data) and from
  distances of sequence separation at most `K + 3`.
* **Computation.**  Rank of the Jacobian of (torsions of all states, weights) `↦ M` at the
  candidate; full rank = locally identifiable.  `O((Kn)³)`.
* **What it does not mean.**  Instance C1: full rank, and nine other chains with the same
  data.  A tool that fits a `K`-state model and reports a non-singular Hessian has
  established local identifiability within its model class and nothing else.

## 8. Specification S7 — one conformation from distances between points close along the chain

* **Statements.**  *Theorem L [P; unreviewed; mechanism and scaling known — thin-rod
  rigidity, SCI-REV-0023].*  If no four consecutive points of `X` are coplanar, then for
  every configuration `Y`: `min_g‖Y − gX‖_F ≤ 1.2 (b/(s_*τ_*)) (n + 2)² ‖η‖₂`, `η` the errors of the
  squared distances of sequence separation at most 4.  *Theorem L⁺ [P].*  For
  `‖η‖₂ ≤ μ/(ΛC_L)` the bound is `‖η‖₂/(μ + √(μ² − Λ‖η‖₂))`, tending to the first-order constant
  `1/(2μ)`.  *Theorem K [P; (a) known].*  The first-order constant is at least of order `n` for
  every configuration and of order `n²` on rod-like chains.  With separation at most 3 the
  conformation is **not** determined (one mirror choice per window; instance C5).
* **What to implement — diagnostics.**  (i) `μ`: the smallest non-zero singular value of the
  matrix with rows `(x_j − x_k)ᵀ(e_j − e_k)` over the measured pairs, and its singular
  vector (the softest deformation); `1/(2μ)` is the worst-case first-order amplification of
  squared-distance errors.  (ii) The window thicknesses `τ_i`, `s_i` (third singular values of
  centred windows of four and five points): a thin window marks where the handedness of
  the remainder is weakly determined (instance F2).  (iii) For separation at most 3: report
  non-uniqueness.
* **What not to implement as a guarantee.**  The global error bar of Corollary L.2 is valid
  for any estimate and any noise bound, and **vacuous at realistic accuracy**: on a
  20-point helix-like trace `C_L = 456` against `1/(2μ) = 0.45`, and the range in which the
  first-order constant is certified is `3·10⁻⁶` ångström in root-mean-square distance error
  (`LOCAL_DATA_STABILITY.md` §6).  Printing it as an uncertainty would mislead.
* **Complexity.**  `O(n)` singular value problems of size 5 × 3 for the thicknesses; one sparse
  SVD of size `(4n) × (3n)` for `μ`.
* **Reference code.**  `local_data_upper.py` (`sharp_constants`, `theorem_L_bounds`,
  `theorem_Lplus_bound`), `local_data_guarantees.py`.

## 9. What a tool claiming more would have to contradict (obstructions)

| claim | obstruction | status |
|---|---|---|
| "the ensemble is recovered from averaged squared distances" with no statewise constraints | every configuration has the data of three collinear ones; a `K`-mixture sits in an `O(3K)`-orbit of others (Proposition 3.1; instance C4) | P |
| a continuous conformational distribution is recovered from second moments | never determined (Corollary 4.2 (c); instance G2) | P (Science division) |
| two states that differ in one torsion are resolved | only the mean of `(cos, sin)` is determined (instance C2) | P (Science division) |
| a unique fold from distances at sequence separation at most 3 | `2^{n−3}` mirror choices (instance C5) | P |
| accuracy from local distances that does not degrade with length | first-order amplification at least of order `n`, and `n²` on rod-like chains (Theorem K; instance F3) | P |
| identification at the "parameter count" threshold | local identifiability only (Theorem H; instance C1 at 8 points for two states) | P-exact / N |
| a certificate of uniqueness below 10, 16, 30 points for two, three, four generic states | none known to us; possible in principle down to the conjectured 10, 14, 19 | open |

## 10. What must remain exploratory until independently reviewed

`ENSEMBLE_RIGIDITY.md` §6.2 (Proposition 6.2, Theorem I′, Conjecture 6.3) and
`LOCAL_DATA_STABILITY.md` §3 (Theorems L, L⁺) were written at the ninth and tenth
checkpoints and have been read by nobody outside the sessions that wrote them.  Theorem G's
constant is not computed.  Theorem J rests on results of the Ensemble division that this
division did not review.  Everything labelled [N] or [C] in the table of §0.  The
thresholds are for *generic* chains at specific bond angles (and all but finitely many
others); an instance is covered only by running its certificate.

## 11. Fifteen-field summary for the software register

| result | Lean | proof / review | assumptions | evidence | counterexamples | computational prerequisite | when it is useless | readiness |
|---|---|---|---|---|---|---|---|---|
| S1 stacking | `stacked_sqdist`, `exists_linearMap_of_gram_eq` | V + P; reviewed | exact second moments, labelled points | harness | G2, G3 | eigen-decomposition | data are not second moments | ready |
| S2 linear certificate, DEMIX | `mixture_identifiable_stacked`, `finite_mixture_identifiable` | V (finite mixtures) + P; reviewed by two internal reviews | S1 + exact common statewise constraints + enough points | exact ranks to `K = 20`; recovery on synthetic data | below threshold; hinges | two ranks | noise above about `10⁻²`; few points; shared segments | ready as checker / reference |
| S3 quartic certificate | none | P, P-exact; **unreviewed**; method known | as S2 | exact witnesses `K ≤ 4` | `n < 6K − 2`; four states below 30 points unknown | exact rank of size `C(m+3,4)` | `K ≥ 5`; floating point | exploratory |
| S4 stress certificate (checker) | `stress_certificate` | V (core) + P; reviewed | S2 + a stress supplied | instances by the referee's programme | bands of separation `≤ 6`: no stress exists | `LDLᵀ`, ranks | no producer; `κ` unknown | checker ready |
| S5 hinges | none | P, P-exact; two derivations | two states, rigid segments on no conic | exact degrees 8 / 2 | one hinge; two half-turns | eight candidates, a linear programme | more than two states | reference ready |
| S6 local identifiability | none | P-exact | generic | exact Jacobian ranks `K ≤ 8` | C1 | Jacobian rank | as evidence of identification | diagnostic only |
| S7 local-distance diagnostics | none | P; **unreviewed**; mechanism known | exact complete data of separation `≤ 4` | 420 arbitrary competitors | separation `≤ 3` | sparse SVD | as an error bar at realistic noise | diagnostics ready; guarantee vacuous |

(Originating division: Geometry, except where a row or the text names the Science
division.  Commit: the one that adds this file.  Physical interpretation, potential
application and competing methods are deliberately left to the Structural Biology and
Science divisions: we have not established any.)
