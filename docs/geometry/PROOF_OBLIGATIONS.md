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
(`DEAD_ENDS.md` DG-9).  Still open: (a) `K ≥ 3` — the scheme at infinity is
positive-dimensional at the conjectured threshold `⌊9K/2⌋ + 1`, and a direct Gröbner basis
(the `4 × 4` minors of a `9 × 9` pencil in 21 variables for `K = 3`) is out of reach as posed;
a reduction that removes the structural part is needed; (b) `K = 2`, `n = 9`: identifiable in
six instances although further chains exist — is it generic, and is there a proof?
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

**O-5.  The constant of Theorem G.**  `κ` is a global infimum over the conformation space.
Needed for a certified constant: a rigorous lower bound of `φ(X)/min_k d_P(X, X_k)²` on the
torus of torsions (local part: an eigenvalue; global part: branch-and-bound).  Also: `C_μ` is
not explicit in the smoothness constant of the conformation space.

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
