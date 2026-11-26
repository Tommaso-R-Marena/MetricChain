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

**O-2.  Identifiability among all ensembles below the conic threshold (G1.21).**  Claimed: [N]
for `K = 2` (`n = 10, 11`) and `K = 3` (`n = 14, 15`), [C] in general (`n ≥ ⌊9K/2⌋ + 1`).
Needed for `K = 2`, `n = 10`: an exact elimination showing that for one rational witness the
projective variety `{P ∈ ℝI + 𝒩(z) : rank P ≤ 3}` consists of the two forced points, reduced
(17 quadratic equations in the entries of a `3 × 6` matrix modulo `O(3)`, or the `4 × 4` minors
of a symmetric `6 × 6` pencil in 5 variables).  Then properness gives the generic statement
for real *and complex* solutions.  Requested from the Computational Research Division
(GEOMETRY-REQ-0001, item 1).

**O-3.  Is ensemble rigidity strictly weaker than universal rigidity (Theorem E, open
part)?**  Needed: a 7-atom chain `X`, a pair set `F` and couplings `c` on `F` such that (i) `X`
is the unique maximiser over the 4-torus of torsions of `Σ_F c_ij |x_i − x_j|²` — a certified
global optimum; (ii) the stress matrix of the Lagrange multipliers is not positive
semidefinite and the stress space of `(F ∪ E₀, X)` is one-dimensional.  (i) is an interval
branch-and-bound in four variables.  Requested (GEOMETRY-REQ-0001, item 2) once a numerical
candidate exists; the search is `experiments/geometry/explore_er2.py`.

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
