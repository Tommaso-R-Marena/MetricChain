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

**Modulo what.**  In all four, "the ensemble" means the set of pairs (weight, state up to
an isometry of space, **reflections included, each state separately**).  The data cannot
see the handedness of any state.  A tool must not report a chirality, and an evaluation
must superpose each state separately with improper superpositions allowed — a
superposition-based score that sees chirality will penalise a correct answer, a
distance-based score will not (the Frontier Benchmarking division's item G-4).

**With noise there is a fifth thing to report: a radius.**  For data known up to `ε` the
question "identifiable?" has no yes/no answer; what can be established is an *enclosure* —
every ensemble consistent with the data lies within a stated distance of the output — and
whether that enclosure is certified or only first-order (§8b).

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
| every point observed | only a labelled subset `S` of the points, with all pairs among `S` | `LABEL_PATTERNS.md` (twelfth checkpoint): everything transfers to the labelled sites; what counts is the number `c(S)` of labelled pairs at chain separation 1 or 2 — linear certificate from `(9K² + K + 2)/2` (20, 43, 75), quartic from 17 for two states, **nothing from sparse labels** (S8 below) | a proof of the count for all patterns; three states below the linear threshold |
| all pairs among the observed points | only some pairs, or only linear functionals `⟨C_a, M⟩` (block sums — the Science division's analysis of labelled scattering, SCI-RES-0029) | Theorem F (a stress certificate for a subset of pairs; instances exist for scattered pairs), Theorem F″ (the same for linear functionals; **no instance**) | a certificate *producer* (a semidefinite programme) specified and tested; thresholds |
| squared distances | other averages of the distance (inverse powers, transfer efficiencies) are not quadratic in the coordinates | nothing: the stacking lemma fails | a theory |
| second moments | distance *distributions* (laws) carry more | Theorem J (laws at separations 3 and 4 determine generic finite ensembles), resting on the Ensemble division's E5/E6 | constructive version; noise |
| exact data | noise | `ROBUST_DEMIXING.md` (thirteenth checkpoint, unreviewed): for data known up to `ε`, explicit enclosures of **every** consistent ensemble (Theorem N1: all but a stated fraction of the mass within a stated radius of the output states; the constant of Theorem G is now computable), linear bounds for `K`-state competitors (Theorem N2), and the exact first-order constants `C_state`, `C_w` — of order one in the instances — certified in a small range and attained (Theorem N3); the count of states with the threshold at the error level (Proposition N5) (S9 below) | the certified ranges end at relative errors `10⁻¹²` to `10⁻⁴`: **no guarantee at realistic accuracy**; random noise; exact-arithmetic certificates; anything below the conic threshold |
| finitely many states | a continuous part | an obstruction: an ensemble with a continuous part is **never** determined (Corollary 4.2 (c)) | what *is* determined (moments), as a theorem with constants |
| the same bond lengths and bond angles in every state, exactly | fluctuating local geometry; coarse-grained traces whose virtual bond angle varies with the conformation | an obstruction for unconstrained states (Proposition 3.1); the certificates *refuse* when the supplied constraints are false (instance G1); **for a tolerance `δ` on the squared constrained distances** (`ROBUST_DEMIXING.md` Proposition N6): uniqueness is lost for every `δ > 0` — an explicit family of ensembles with the same data, of dimension `9K(K − 1)/2 + K − 1` — and the family has size `c_tol·‖violations‖` to first order, `c_tol` between `0.7` and `1.8` in the instances, with a certified constant within a factor 6 | tolerances that differ between states or are correlated; virtual bond angles that depend on the conformation (not a box) |
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

* **Statements.**  *Theorem L [P; **reviewed with replication by the Science division,
  SCI-REV-0028: proved as stated**; mechanism and scaling known — thin-rod rigidity,
  SCI-REV-0023].*  If no four consecutive *interior* points of `X` are coplanar, then for
  every configuration `Y` **in `ℝ³`**: `min_g‖Y − gX‖_F ≤ 1.2 (b/(s_*τ_*)) (n + 2)² ‖η‖₂`, `η` the errors of the
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
  for any estimate **in three dimensions** (false for an unprojected four-dimensional
  solution), with **every** pair of separation at most 4 measured and a bound on the
  errors of the *squared* distances — and **vacuous at realistic accuracy**: on a
  20-point helix-like trace `C_L = 456` against `1/(2μ) = 0.45`, and the range in which the
  first-order constant is certified is `3·10⁻⁶` ångström in root-mean-square distance error
  (`LOCAL_DATA_STABILITY.md` §6).  Printing it as an uncertainty would mislead.
* **Do not use the first-order number as an error bar either** (the Science division's
  review, SCI-REV-0028 §2 and §4; replicated by us, `distant_fits.py`).  `1/(2μ)` describes
  the limit of vanishing errors.  On the idealised 20-point helix-like trace configurations
  farther away than the radius of gyration fit all local distances to `0.27`–`0.30` Å, and on
  the strand-like trace to `0.2` Å; the first-order description ends near `0.2` Å and a few
  hundredths of an ångström respectively.  **In the worst case, sequence-local distances
  with errors of a few tenths of an ångström do not determine the fold of these traces,
  whatever the algorithm.**
* **What can be used** (same review, §4).  (1) *One window:* five consecutive points whose
  ten distances are known to within `0.1` Å are fixed, up to an isometry, to RMSD `≤ 0.32` Å
  on a helix-like window and `≤ 2.1` Å on a strand-like one (Lemma Q; no smallness
  condition; within a factor 2 to 3 of the worst case found).  (2) The first-order
  sensitivity as a *diagnostic of conditioning*, not as a bound.  Longer-range information
  is needed, and nearly planar stretches are where it is needed first.
* **Complexity.**  `O(n)` singular value problems of size 5 × 3 for the thicknesses; one sparse
  SVD of size `(4n) × (3n)` for `μ`.
* **Reference code.**  `local_data_upper.py` (`sharp_constants`, `theorem_L_bounds`,
  `theorem_Lplus_bound`), `local_data_guarantees.py`, `distant_fits.py`.

## 8a. Specification S8 — partial labelling (only a subset of the points is observed)

* **Statement.**  *`LABEL_PATTERNS.md`, Theorems P1, P2, Propositions P3, P4 [P; P-exact;
  **unreviewed**].*  Let `S` be the observed points, the data all averaged squared distances
  among `S`, and `c(S)` the number of pairs of `S` at chain separation 1 or 2.  S1–S3 apply to
  `(M_S, E₀(S))` unchanged and determine the ensemble of configurations **of the labelled
  sites**.  The linear certificate needs `c(S) ≥ (9K² + K + 2)/2` and, for patterns in general
  position, holds from there (proved for non-adjacent labelled bonds and for patterns with
  an anchor of `⌈(9K² + K + 8)/4⌉` consecutive points; exact on random patterns; conjectured
  in general for `K ≥ 2`; **false for one state** with two labelled triples).  Below
  `c(S) = 9K/2` the ensemble is not even locally identifiable; with no two labelled points at
  separation 1 or 2 nothing is determined.
* **Input.**  `M_S`; the positions of the labelled sites along the chain (to form `E₀(S)` and
  the lengths).  **Output.**  As S2, for the labelled sites only.  A tool must not output
  positions of unlabelled points as determined.
* **Computation and complexity.**  As S2 with `n` replaced by `|S|` and `2n − 3` by `c(S)`.
* **Pre-check that costs nothing.**  Count `c(S)`.  If `c(S) < 9K/2`: refuse, the answer is
  provably not unique.  If `c(S) < (9K² + K + 2)/2`: the linear certificate cannot hold.
* **Instances.**  A4 (an anchor of 12 with 7 isolated labels: certified, all 19 sites
  recovered), C6 (labels at every fourth point: a second solution supplied).
* **Reference code.**  `label_patterns.py` (`constrained_pairs`, `demix_pattern`,
  `second_solution`), `exact_label_patterns.py`.
* **Readiness.**  The pre-check and S2 on patterns: ready as a reference.  Everything
  between the two thresholds: exploratory.

## 8b. Specification S9 — demixing from noisy data, with an enclosure

* **Statement.**  *`ROBUST_DEMIXING.md`, Lemma N0, Theorems N1–N3, Corollary N4, Propositions
  N5, N6 [P; **unreviewed**; the tools are standard perturbation theory].*  Data: the centred
  matrix `G̃ = −½JM̃J` with `‖G̃ − G(truth)‖_F ≤ ε`; statewise constraints known within a
  tolerance `δ_e` on the squared distances.  For a reference mixture `μ₀` (below) and
  `η = ε + ‖G(μ₀) − G̃‖_F`: (a) every ensemble consistent with the data has all but a
  fraction `√(n−1−3K)·η/φ₁` of its mass within `r(φ₁)` of the states of `μ₀`; (b) every
  consistent mixture with `K` states has its states within `B_k` and its weights within
  `A` of those of `μ₀`, where `B_k → C_state,k·η + T_k‖violations‖` as `η, δ → 0`; (c) both
  only when the stated hypotheses hold — otherwise nothing is certified.
* **Input.**  `G̃` (or `M̃`), `ε`, `δ`, the constraint lengths, and `K` or the rule of
  Proposition N5 (count the eigenvalues of `G̃` above `ε`; correct when `ε < λ_{3K}/2`).
  **Output.**  The mixture `μ₀`; its residual; `C_state`, `C_w` (first-order condition
  numbers — always reported); the certified radii `B_k`, `A`, or the statement "not
  certified"; the enclosure of (a) with its mass fraction.
* **Computation.**  DEMIX on `G̃` with `K` given; least squares over weights and torsions
  started there (`polish`); at `μ₀`: one SVD of the conic system on the complement of the
  trivial quadrics (`σ_c`), the rigidity matrices of the states, the pseudo-inverse of the
  linearised map `(weights, tangent displacements) ↦ G` (size `n² × (K(n−3) + K − 1)`), a
  scalar fixed-point iteration.  `O(n²·(Kn)²)` operations for the pseudo-inverse.
* **Semantics of the two kinds of number.**  `C_state`, `C_w`, `c_tol` are *first-order*:
  true in a neighbourhood whose size is certified only up to the ranges of the table in
  §8 of the note (relative errors `10⁻¹²` to `10⁻⁴`).  `B_k`, `A` are *certified* when
  returned.  A tool must not present the former as the latter.  `σ_c` governs the
  certified range, **not** the accuracy: a small `σ_c` with a small `C_state` is a
  well-conditioned problem with a weak certificate.
* **Counterexamples and limits.**  With a tolerance, exact uniqueness never holds
  (Proposition N6).  The number of states is not bounded above by noisy data
  (Proposition N5 (iii)).  The hypothesis (J) (injective linearisation) is checked
  numerically.  Floating point; not a kernel-checked certificate.
* **Validation criteria.**  On synthetic mixtures with planted noise of known norm: the
  truth lies inside `B_k`, `A` whenever they are returned (never violated in our runs); along
  the extremal direction the ratio displacement/(`C_state η`) tends to 1; with the planted
  errors of `mutation_checks.py` (a constant 10 % too small, the residual claimed second
  order, the tolerance constant too small, the count threshold halved) the tests fail.
* **Reference code.**  `robust_demix.py` (`reference`, `numbers`, `theorem_N2`, `theorem_N3`,
  `first_order`, `polish`, `a_posteriori`, `tolerance_constant`, `count_states`).
* **Readiness.**  The first-order condition numbers and the count rule: ready as
  diagnostics.  The certified radii: correct, and empty at realistic accuracy.
  Exploratory until reviewed.

## 9. What a tool claiming more would have to contradict (obstructions)

| claim | obstruction | status |
|---|---|---|
| "the ensemble is recovered from averaged squared distances" with no statewise constraints | every configuration has the data of three collinear ones; a `K`-mixture sits in an `O(3K)`-orbit of others (Proposition 3.1; instance C4) | P |
| a continuous conformational distribution is recovered from second moments | never determined (Corollary 4.2 (c); instance G2) | P (Science division) |
| two states that differ in one torsion are resolved | only the mean of `(cos, sin)` is determined (instance C2) | P (Science division) |
| a unique fold from distances at sequence separation at most 3 | `2^{n−3}` mirror choices (instance C5) | P |
| an ensemble from averaged squared distances between sparse labels (no two at chain separation 1 or 2) | a family of other ensembles of dimension at least `9K(K − 1)/2`; even one conformation is not determined among ensembles (`LABEL_PATTERNS.md` Proposition P3; instance C6) | P given a regularity condition that holds numerically |
| an ensemble from fewer than `9K/2` statewise-constrained observed pairs | not even locally identifiable (the same proposition) | P given regularity |
| accuracy from local distances that does not degrade with length | first-order amplification at least of order `n`, and `n²` on rod-like chains (Theorem K; instance F3) | P |
| a fold from sequence-local distances (separation at most 4) known to a few tenths of an ångström | on idealised helix-like traces of 12 and 20 points, configurations farther away than the radius of gyration fit all local distances to `0.27`–`0.37` Å; on a strand-like trace to `0.2` Å (found by the Science division, SCI-REV-0028 F1; replicated by us) | N (explicit configurations by search) |
| identification at the "parameter count" threshold | local identifiability only (Theorem H; instance C1 at 8 points for two states) | P-exact / N |
| a certificate of uniqueness below 10, 16, 30 points for two, three, four generic states | none known to us; possible in principle down to the conjectured 10, 14, 19 | open |
| exact identification when the bond geometry is known only within a tolerance | for every tolerance `δ > 0` the rotated stacks give a family of ensembles with exactly the same data, of dimension `9K(K − 1)/2 + K − 1` (`ROBUST_DEMIXING.md` Proposition N6) | P |
| the number of states from noisy data, as an upper bound | a state of weight `t` changes the data by at most `2tD_n²`; only "at least `K`" can be established (Proposition N5) | P |
| a guarantee of accuracy for demixing at realistic noise | none exists in this collaboration: the certified ranges end at relative errors `10⁻¹²` to `10⁻⁴`; the first-order constants are of order one but are not certified there | open |

## 10. What must remain exploratory until independently reviewed

`ENSEMBLE_RIGIDITY.md` §6.2 (Proposition 6.2, Theorem I′, Conjecture 6.3) and
`LOCAL_DATA_STABILITY.md` §3 (Theorems L, L⁺) were written at the ninth and tenth
checkpoints and have been read by nobody outside the sessions that wrote them; the same
holds for `LABEL_PATTERNS.md` and `ROBUST_DEMIXING.md` (twelfth and thirteenth).  Theorem G's
constant now has a computable lower bound, which is very small (S9).  Theorem J rests on results of the Ensemble division that this
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
| S7 local-distance diagnostics | none | P; **reviewed with replication by the Science division (SCI-REV-0028)**; mechanism known | exact complete data of separation `≤ 4` | 420 arbitrary competitors | separation `≤ 3` | sparse SVD | as an error bar at realistic noise | diagnostics ready; guarantee vacuous |
| S8 partial labelling | (S2's declarations apply) | P, P-exact; **unreviewed**; one conjecture | all pairs among the labelled sites; exact common local geometry | exact ranks on 100 random patterns; second solutions | sparse labels (C6); one state with two triples | counting `c(S)`; then S2 | `c(S)` below the thresholds | pre-check and reference ready |
| S9 demixing from noisy data | none | P; **unreviewed**; standard perturbation theory | S2 + an error level `ε` in Frobenius norm + a box tolerance on the constraints | every inequality checked on competitors; constants attained; four planted errors caught | exact uniqueness with a tolerance; an upper bound on `K` | DEMIX, a least-squares polish, one pseudo-inverse | as a guarantee beyond relative errors `10⁻¹²`–`10⁻⁴` | condition numbers and count rule ready; certified radii empty at realistic accuracy |

(Originating division: Geometry, except where a row or the text names the Science
division.  Commit: the one that adds this file.  Physical interpretation, potential
application and competing methods are deliberately left to the Structural Biology and
Science divisions: we have not established any.)
