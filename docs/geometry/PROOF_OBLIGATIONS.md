# Unresolved proof obligations — Geometric Inference division

Each item: what is claimed, at which label, what would discharge it, who could do it.

**O-1.  Sharp conic threshold for every `K` (Theorem C(d)).**  Claimed: [C].  Have: exact
witnesses for `K ≤ 20` (cos −5/13) and `K ≤ 12` (tetrahedral angle, and both constraint sets);
a complete proof for freely jointed chains; and, for every `K` and every bond angle
(Theorem C(c), sixth checkpoint): the generic rank `r_N` is **concave** in the number of bonds
`N`, strictly increasing until it reaches `D_K`, and equal to `2N − 1` for `N ≤ 3K`; hence the
threshold `(9K² − 5K + 6)/2`, twice the sharp one for large `K`.  By concavity the conjecture
is equivalent to one statement: **the last increment before saturation is 2**, i.e.
`r_N = 2N − 1` at `N = ⌊(D_K + 1)/2⌋`.
What is known beyond the report (working notes, not checked by anyone else):
(1) *Monotonicity in `K`*: if the conditions of `K − 1` chains are independent, so are those of
`K` chains; with (b), `r_N = 2N − 1` for `N ≤ 906` for every `K ≥ 20` at the rational geometry.
(2) *Structure at the first defect.*  Let `N` be the first length with increment `≤ 1` and
`dim 𝒩/𝒯 ≥ 2`, `p = p_N` the last point, `q = γp + σu(φ)` on the torus `A(p)`.  For
`S ∈ 𝒩(π)`: `pᵀSq = σ g_S(φ)`, `qᵀSq = 2γσ g_S(φ) + σ² h_S(φ)` with
`g_S = Σ_k G_S^{(k)}·u_k(φ_k)` (`G_S` = the components of `(Sp)^{(k)}` orthogonal to `p^{(k)}`) and
`h_S = uᵀQ_Su` (`Q_S` = the compression of `S` to `V(p)`).  Increment `≤ 1` means that the
pairs `(g_S, h_S)`, `S ∈ 𝒩(π)`, are pairwise proportional as functions on the torus, which
leaves three types for the generic path: (A) `G_S = 0` on `𝒩(π)` — equivalently every quadric
through the path is, modulo trivial ones, singular at the last point (`Sp_N = 0`);
(B) `h_S ≡ 0` on `𝒩(π)` — modulo trivial quadrics `V(p_N)` is totally isotropic;
(C) `h_S = (c·u) g_S` for one vector `c ∈ V(p_N)` (after a coprimality argument in the ring
of Laurent polynomials; linear forms `Σ_k(A_kz_k + Ā_k/z_k)` in two variables factor only if
`|A_1| = |A_2|`).  By shift invariance each type propagates along longer paths: under (A)
the surviving quadric at the last unsaturated length is singular, modulo `𝒯`, at about
`D_K − 2N` consecutive points at each end, which a parameter count allows only if
`D_K − 2N ≲ 2.25K`.  So a defect, if it exists, appears only within `O(K)` conditions of
the sharp threshold; types (B), (C) not worked out.
(3) *Reformulations* (report, remark after Theorem C): Jacobi matrices with a totally
isotropic chain subspace; Schur squares of chain codes.
(4) The quadrics invisible from `p` (`G_S = 0`, `Q_S` trivial) form a space of dimension
`(5K + 2)(K − 1)/2` modulo trivial ones, so a one-step argument is not enough.
Needed: either the exclusion of the three types at the last step, or a degeneration with a
triangular structure (candidates: complex chains running to isotropic directions; nearly
straight chains expanded in the bending angle).  Could be attempted by a workstream with a
distinct approach.

**O-2.  Identifiability among all ensembles below the conic threshold.**  **Discharged for
two states** (Theorem I, G1.25): exact elimination with Singular, installed in our own
environment after GEOMETRY-REQ-0001 was written; the answer is not the one the request
expected — the scheme has degree 7, not 2, because of a structural rank-2 point at infinity
(`DEAD_ENDS.md` DG-9).  **Partly discharged for three and four states** (Theorem I′, G1.31,
ninth checkpoint): identifiable from 16 atoms (three states) and from 30 (four), by a
linear-algebra certificate on quartic forms with exact witnesses; the same method re-proves
two states at 10 atoms.  Still open: (a) `K = 3` at 14 and 15 atoms, `K = 4` at 19 to 29,
`K ≥ 5` below the conic threshold — at the conjectured threshold `⌊9K/2⌋ + 1` the scheme at
infinity is positive-dimensional and the certificate needs a higher level (O-15);
(b) `K = 2`, `n = 9`: identifiable in
six instances although further chains exist — is it generic, and is there a proof?
[**Independent replication, received at the thirteenth checkpoint** (Engineering,
ENG-MSG-0007 §5; its report `experiments/eng/geometry_req1/REPORT.md` on its branch, not
opened by us): by a session that had not seen our result, two states at ten atoms have
exactly the two solutions, each reduced, and one point at infinity of multiplicity 5 —
degree 7; the 120 minors span 63 of 70 dimensions; eleven atoms: degree 2; every exact
rank of ours confirmed over ℚ on eight witnesses; and for (b): at nine atoms exactly 46
further affine complex solutions, of which 2 to 8 are real and positive semidefinite on
six witnesses.  Its remark that "63" is an open condition (the span is at most 63 a
priori) is the genericity argument of Theorem I′.]
(c) `K = 2`, `n = 7, 8`: non-identifiability is numerical (explicit competing ensembles to
`10⁻¹⁴`); a proof would show that the identity is interior to the convex hull of `𝒫(z)`.
(d) An independent replication of the degree-7 computation with another system
(GEOMETRY-REQ-0001, item 1, as amended by GEOMETRY-MSG-0003).

**O-3.  Second-moment rigidity is strictly weaker than universal rigidity: a certificate.**
Numerical instances exist (`er_not_ur_instance.py`, candidates A and B; report §8.2).
Needed for a theorem: (i) a certified statement that instance A is the unique maximiser, up
to the mirror image, of `H_c` over the 4-torus of torsions — interval branch-and-bound with a
second-order exclusion test near the maximiser (margin to the next local maximum `0.015`,
smallest Hessian eigenvalue `0.0064` in normalised units, so the certified neighbourhood is
small and the cost is in the shells around it); (ii) a certified four-dimensional realisation
(an interval Newton step on the 16 length equations).  Requested from the Computational
Research Division: GEOMETRY-REQ-0006.  An instance with a larger margin and curvature would
be cheaper to certify; `explore_er3.py` produces candidates at a rate of about one per
thousand random instances.

**O-4.  Sequence-local data among all ensembles.**  Proved: separation `3K + 1` suffices
(Theorem F′); `K + 3` is necessary and locally sufficient within `K`-state ensembles (Theorem
H).  Open: the smallest separation that identifies a generic `K`-mixture among all ensembles,
for long chains.  Heuristic: the statewise constraints over-determine the block structure, so
the answer may be much smaller than `3K + 1`.

**O-5.  The constant of Theorem G.**  *Closed at the thirteenth checkpoint in the sense
"computable":* `ROBUST_DEMIXING.md` Corollary N1.1 gives `κ ≥ min(φ₁/r(φ₁)², φ₁/(2D_n²))` with
every quantity a finite computation (unreviewed).  *Still open:* (i) the bound is four to
eight orders of magnitude smaller than the values found by search in two-state instances — a certified constant of the right
order needs a global optimisation over the torus of torsions outside the basin, or a
sharper version of Lemma N0 that uses positive semidefiniteness beyond eigenvalue counts;
(ii) `C_μ` of Theorem G(d) (the weights of an arbitrary competing ensemble to first order
in the error) is still not explicit — the mechanism is known (the mean out-of-stack
displacement of each cell is of the order of the error, not of its square root) and the
bookkeeping was not done.

**O-6.  Theorem H for every `K`.**  Base cases are exact computations for `K ≤ 8`; the
extension in `n` is proved.  Needed: an induction on `K`, or a structural reason why the
Jacobian is generically of full rank exactly from the parameter count on.

**O-7.  Lean.**  Done: Lemma 2.2 for finite mixtures (`exists_linearMap_of_gram_eq`,
`state_is_linear_image`); Theorem B against finite competing mixtures with abstract blocks
(`finite_mixture_identifiable`) and in coordinates, with the stacked configuration of states
`X_k` and weights `w_k` and the conclusion "every state of positive weight has the distance
matrix of some `X_{k₀}`" (`mixture_identifiable_stacked`); a two-state instance on the line in
which all hypotheses hold, used end to end (`line_mixture_example`).  Not formalised: (b) the
weights of the competing mixture; (c) competing ensembles that are not finitely supported;
(d) Theorem B′; (e) Theorem G; (f) the conic and spanning conditions for an actual
three-dimensional chain (they are exact rank computations of size `D_K × D_K` — `20 × 20`
for two states — and could be checked by `decide`-free rational linear algebra in Lean; not
attempted).

**O-8.  Measure theory in Lemma 2.2 and Theorem B′.**  The proofs use: representatives of
`L²` classes chosen simultaneously for finitely many indices (fine); Tchakaloff's theorem for
a compactly supported measure restricted to a ball and to its complement (standard); the
measurability of `x ↦ A(x)ᵀA(x)` and of the index `κ(x)` (immediate from the construction).
Checked by the internal review only.

**O-9.  Corollary 9.1** rests on a cited sample-complexity theorem that was not re-derived
(and whose hypotheses for mixtures should be checked by the Ensemble Identifiability
Division: GEOMETRY-REQ-0002).

**O-10.  Heterogeneous bond geometry in Theorem C(c).**  Lemma R is proved for one bond
angle; for position-dependent angles the reachability bound `m₀` changes and the statement is
"for some `m₀` depending on the angles".  Not written.

**O-11.  Genericity sets.**  All generic statements exclude an unspecified proper analytic
subset.  Which conformations violate (CC) — beyond planar ones and those with coinciding
states — is not described.

**O-12.  Hinge ensembles with more than two states** (`HINGE_ENSEMBLES.md` §6).  Identifiability
is the determinacy of the interval-moment problem on `O(2)^s`.  Known: two states — never for
one hinge, always from two on (Theorem M); three states at two hinges — can fail (one
explicit instance, numerical).  Open: the threshold in `s` for `K` states; whether three states
at two hinges are ever identifiable; a proof for three states at four hinges (numerically
only the states are linear images of the stack).  Tools: flat extensions of moment matrices,
on a group with several components and for non-commuting products.

**O-13.  A dual certificate for hinge pairs.**  Theorem M (b) is proved by listing the eight
candidates.  Is the face `conv{D(X_1), D(X_2)}` exposed — is there `c_0 + ⟨C, D(·)⟩ ≥ 0` on all
conformations vanishing exactly on the two states?  It would give a stability statement.
Also open: torsion changes that are multiples of `π`; hinges closer than three torsions
(segments with a conic).

**O-14.  Theorem F″ (block sums) has no instance.**  A semidefinite programme for a labelling
scheme of the kind the Science division describes (SCI-RES-0029 §2) has not been run.


**O-15.  The ladder below the conic threshold (§6.2).**  Proved: Proposition 6.2 (what the
certificates `h_D = K` and `h_D = K + dim Λ_D` imply; the count; the structural point) —
elementary, the mechanism being Johnston–Lovitz–Vijayaraghavan's — and Theorem I′ (exact
witnesses: two states from 10 atoms, three from 16, four from 30).  Not proved:
(i) **Conjecture 6.3** — for chains in general position `h_4 = K` from `max(count, 6K − 1)`
atoms on.  Open cases: four states at 24 to 29 atoms.  `exact_demix4.py 4 28` is feasible
locally (about 3 hours, 4.5 GB); 26 and 24 need the echelon form stored in 16-bit integers
and many hours — a candidate for a request to Engineering, not sent.  A proof for all `K`
would need the restriction of the Schur module of the `4 × 2` rectangle to forms on `L` to
have maximal rank; the method of Dastidar–Weich–Wein for rank one (zero out variables, a
block triangular square matrix with distinct monomials on the diagonal blocks) is the place
to start.
(ii) The thresholds of the higher levels: the table of `minrank_prediction.py` is a
heuristic (maximal rank for non-generic linear forms), checked only at `D = 4`.
(iii) **Three states at 15 and 14 atoms.**  At 15 atoms the structural locus is two lines
and seven points, the count excludes `D = 4`, and the natural statement is
`h_5 = K + dim Λ_5` (33 649 quintic forms; `exact_demix4.py` handles `D = 4` only).  At 14
atoms — the information threshold — the level predicted for generic sections is 10, out of
reach.  Whether the first-order jets along a positive-dimensional structural locus account
for the whole defect, as they do for an isolated point, is not known.
(iv) All statements are for generic chains at two bond angles and at all but finitely
many others; no statement for a given other angle, none for position-dependent angles.
(v) DEMIX-4 at `n = 6K − 2` (extraction through `c²g`) is described, not implemented.
(vi) Noise: nothing.  The certificate is a rank; its stability constant is the smallest
singular value of a matrix of size `C(m + 3, 4)` and was not studied.

**O-16.  Local distance data: the size of the best global constant** (`LOCAL_DATA_STABILITY.md`
§6; restated at the thirteenth checkpoint after the Science division's review
SCI-REV-0028).  Theorem L excludes distant configurations with a constant
`C_L ≈ 1.2 b n²/(s_*τ_*)`; Theorem L⁺ gives the first-order constant `1/(2μ)` when
`‖η‖₂ ≤ μ/(ΛC_L)`.  **Settled by that review (its F1; replicated by us, `distant_fits.py`):**
the gap between `C_L` and `1/(2μ)` is only partly an artefact — `C_glob(X) = sup_Y d_P/‖η‖₂`
is unbounded relative to `1/(2μ)` (a nearly coplanar interior window: `d_P/‖η‖₂ ∝ 1/τ` with
`1/(2μ)` bounded), so the factor `1/τ` is necessary in every global constant and the range
of Theorem L⁺ cannot be `μ²/Λ`; on the 20-point helix-like trace configurations at the
radius of gyration fit the local distances to `0.27` Å.  **Open:** (i) the size of `C_glob`
between the lower bounds and `C_L` — between `1.92` and `456` (or `88.7` with the local form)
on that trace: a factor 240 (46), and 55 on the worst pair found by search; is the true
constant of order `n²b/(s τ)` with a small absolute factor, and is the product `s_*τ_*`
or only `τ_*` necessary?  (ii) an instance-specific *computed* radius of injectivity
(interval arithmetic or a sum-of-squares certificate for one chain) — a computation to be
specified for Engineering, not requested; (iii) random noise: a statement in expectation —
the first-order expectation is now in the table of §6, but a guarantee needs (i);
(iv) incomplete windows: a missing interior pair of separation at most 3 (needed by the
proof, the conclusion not settled — the referee's conjecture); general lateration graphs;
(v) the stress route is excluded for long chains (`DEAD_ENDS.md` DG-26).  *Closed:* the
attribution of Lemma P (checked at the source by the Science division); an outside reading
of the proofs of Theorems L, L⁺ (SCI-REV-0028: proved as stated).

**O-17.  Label patterns (`LABEL_PATTERNS.md`).**  Proved: the transfer (Theorem P1); the
linear threshold for non-adjacent labelled bonds and for patterns with an anchor; the
obstruction given regularity.  Open: (i) **Conjecture P** — the generic conic rank is
`min(c(S), N_K)` for every pattern when `K ≥ 2` (exact on 100 random patterns and subsets,
`K ≤ 3`; the exception for one state shows that a proof must use `K ≥ 2`: the natural route
is the one of Theorem C (c), submodularity of the generic rank, now on the lattice of
patterns); (ii) regularity (R) as a theorem, with the size of the realisable neighbourhood
(small for labels at every third point); (iii) the quartic certificate on patterns for three
states; a description of the patterns with structural points (two hyperplanes covering
the labelled bond vectors) and of longer covers; (iv) the middle of the table of §6: what
happens between `c = 9K/2` and the information threshold, and at `c = 16` for two states;
(v) other statewise equalities (rigid labelled bodies); patterns combined with states that
share rigid parts; (vi) data that are not all pairs among the labelled sites (then a
stress certificate is needed: Theorem F; no producer); (vii) noise.

**O-18.  Robust demixing (`ROBUST_DEMIXING.md`).**  Proved (unreviewed): Lemma N0, Theorems
N1–N3, Corollary N4, Propositions N5, N6.  Not done: (i) **the certified ranges** end at
relative errors `10⁻¹²` to `10⁻⁴`; closing the gap to the scale at which the linearisation
really fails needs a better way into the basin than Theorem N2 (its constant is a product
of four worst cases); (ii) random noise — a statement in probability or in expectation,
and the first-order covariance of the estimate (the delta method is immediate; a
non-asymptotic statement is not); (iii) certificates in exact or interval arithmetic for
the constants (`σ_c`, the pseudo-inverse norms), so that the output is a certificate in the
sense of the theory division's kernels; (iv) the same analysis below the conic threshold
(for the quartic certificate — O-15) and for label patterns and block sums; (v) tolerances
that are not a box common to all states; (vi) hypothesis (J) as a consequence of (CC) with
a constant, instead of a numerical check per instance; (vii) the sharp first-order
tolerance constant `c_tol` in a certified range (the certified one, `T_k`, is 4 to 6 times
larger because it allows violation patterns that exact data exclude).
