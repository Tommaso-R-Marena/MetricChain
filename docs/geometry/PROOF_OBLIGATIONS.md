# Unresolved proof obligations — Geometric Inference division

Each item: what is claimed, at which label, what would discharge it, who could do it.

**O-1.  Sharp conic threshold for every `K` (Theorem C(d)).**  Claimed: [C].  Have: exact
witnesses for `K ≤ 12` at two bond geometries; a proof for every `K` with the weaker threshold
`m₀(D_K − 1) + 2`; a complete proof for freely jointed chains.  Needed: an induction on the
number of atoms showing that each new atom cuts the space of non-trivial quadrics by two
dimensions until none is left.  What we know (working notes, not in the report): in terms of
the invariants of a quadric `S` at the last bond `p` — its block gradient `G_S` (the
components of `(Sp)_k` orthogonal to the bond of state `k`) and its compression `Q_S` to the
planes orthogonal to the bonds — the two new conditions are `⟨G_S, e⟩ = 0` and `eᵀQ_Se = 0`
for a generic point `e` of a product of `K` circles; the quadrics invisible from `p` form a
space of dimension `(5K + 2)(K − 1)/2` modulo trivial ones, so a one-step argument is not
enough and the two-step freedom must be used.  Could be attempted by a workstream with a
distinct approach (e.g. a degeneration in which the states take turns).

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

**O-7.  Lean.**  Not formalised: Lemma 2.2 for finite mixtures (the linear isometry from equal
Gram matrices), hence the end-to-end statements of Theorems A and B; Theorem B′; Theorem G.
Formalising Lemma 2.2 and Theorem B for finite mixtures is the natural next step (the two
cores `block_rigidity` and `stress_certificate` are in place).

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
