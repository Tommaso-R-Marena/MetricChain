# Ensemble report — what an ensemble is determined by

**Ensemble Identifiability and Certified Inference Division.**  Branch
`research/ensemble-identifiability`.  Version 1 (first checkpoint, 2026-11-26).

Labels: **[V]** machine-checked in Lean 4 + Mathlib (declaration named; axioms `propext`,
`Classical.choice`, `Quot.sound` only) · **[P]** paper proof given here · **[K]** known, cited
(the prior-art register `PRIOR_ART.md` says how each source was read) · **[N]** numerical
evidence only (script named) · **[C]** conjecture.  None of the paper proofs has been read by
anyone outside this division yet; an internal adversarial review is commissioned and its
findings will be applied as linked corrections.  "New" below always means "not found in the
search documented in `PRIOR_ART.md`".

---

## 0. Summary

An unknown probability measure `μ` (an *ensemble*) on a configuration space `X` is seen
through means of observables, `y_i = ∫ φ_i dμ + ε_i`.  This report answers, for three kinds
of data, the first question of that model: **which ensembles are determined by the data,
how stably, and with what certificate.**

| # | statement | label | novelty class |
|---|---|---|---|
| E1 | `μ` is determined by the means of `Φ` among *all* ensembles iff its support is exactly the zero set of a non-negative function in `span{1, Φ}` and the features are affinely independent on it (finite `X`; for compact `X`: iff the minimal face of the moment body through the data is a simplex with one configuration over each vertex).  A certificate bounds the mass off the support linearly in the data error.  On continua an identified ensemble can be only Hölder-stable (example with exponent `½`) | P; sufficiency and the mass bound V (`eq_of_exposing_certificate`, `mass_off_support_le`) | known in substance (uniqueness of representing measures; dual certificates of sparse recovery); formulation |
| E2 | **One conformation.**  `ω(τ) = sup{E_ν ρ : ‖E_νΦ − Φ(x⋆)‖ ≤ τ}` equals `min_λ {τ‖λ‖_* + max_y[ρ(y) − λ·(Φ(y) − Φ(x⋆))]}`; the best linear modulus is `κ = min{‖λ‖_* : λ·(Φ(y) − Φ(x⋆)) ≥ ρ(y) ∀y}`.  For `ρ = d(x⋆,·)` the constraint is the **sharp-minimum condition of theory report Theorem 2.4**: *a certificate that `x⋆` minimises `λ·Φ + g` for every admissible residual is a certificate that the data of `Φ` identify the conformation `x⋆`, with transport modulus `‖λ‖_*·τ`* | P (duality, exactness of `κ`); the inequality and the bridge V (`transport_le_of_sharp`, `identification_of_robust_certificate`, `residual_advantage_le`) | formulation (linear-programming duality; the dictionary with robust optimality not found in print) |
| E3 | **Finite ensembles, first order.**  For an identified `μ` on a finite metric space, `sup{W₁(ν, μ) : ‖E_νΦ − E_μΦ‖ ≤ τ} = κ_μ·τ` exactly for small `τ`, with `κ_μ = max_{g 1-Lipschitz} min{‖λ‖_* : c + λ·Φ ≥ g on X, = g on supp μ}`; `κ_μ` depends on the support only, not on the weights | P | new (not found); elementary |
| E4 | **Rényi–Heppes for arbitrary observables.**  If two configurations agree on fewer than `r` of `m` features and `m ≥ K(r−1) + 1`, every ensemble with at most `K` conformers is determined by the `m` *laws* of the features among all ensembles; the bound is sharp for every `K ≥ 2`, `r ≥ 2` | V for finite `X` (`renyi_heppes`), P in general | generalisation of a known theorem (Rényi 1952, Heppes 1956: linear projections) |
| E5 | **Splices on a variety.**  For a polynomial feature map `F : ℝ^D → ℝ^m` without constant coordinates: for generic `K`-tuples no vector assembled coordinate-wise from the feature vectors of *different* points lies on the feature variety — for every `K` — **iff the algebraic matroid of the coordinates of `F` is connected**; if it is not, splices are realisable on an open set of pairs | P | new (not found); closest: unlabeled PCA (linear, unknown subspace) and the product lemma of Garamvölgyi–Gortler–Jordán |
| E6–E8 | **Ensemble rigidity.**  For a graph on at least `d+2` vertices the following are equivalent: `G` is generically globally rigid in `ℝ^d`; every generic finite ensemble of frameworks, *with any number of conformers*, is determined modulo congruence, among all ensembles, by the laws of its edge lengths.  Then `2K` moments of each squared edge length suffice for `K` conformers — `2K|E|` scalar means — with the explicit certificate `Σ_e Π_i (ℓ_e² − ℓ_e(x_i)²)²`.  Mean squared distances alone determine no ensemble at all | P, given two cited theorems (global rigidity is generic; globally rigid ⇒ connected rigidity matroid, 2022) | new (not found) |
| E9 | Pair correlations on `{±1}ⁿ`: every ensemble with at most three conformers is determined; four conformers need not be (explicit) | K (the cut polytope is 3-neighbourly); the example N/P | known |
| E10 | **Typical supports.**  For `K ≤ n − 10n/ln n` independent uniform conformers, with probability `1 − O(K³(¾)ⁿ)` *every* ensemble supported on them is determined by its pair correlations among all ensembles, with the explicit certificate `‖P^⊥x‖²` | P given K (Odlyzko 1988); self-contained proof for `K < 0.2933 n` | synthesis |
| E11 | For `K/n → α > 6.338` the uniform ensemble on `K` random conformers is **not** determined: its pair correlations are also those of an ensemble with full support | P given K (Bai–Yin; Sheppard's formula) | new (not found); elementary |
| E12 | **Adaptivity.**  A fixed set of pairs that determines every two-conformer ensemble must contain *all* `n(n−1)/2` pairs; adaptively, `rn − r(r+1)/2` pair correlations determine the whole correlation matrix of any ensemble of correlation rank `r ≤ K` (certified, no assumption); for typical supports every certificate needs `Ω(Kn/ln(en/K))` pairs | P; K (Cover's counting) | formulation / synthesis |

The thread through the three parts is one sentence: **an ensemble is determined by a family
of observables exactly when it is *exposed* by a non-negative function in their span, the
stability of the identification is the sharpness of that exposure, and the certificates are
objects that the programme's kernels already check** — minima of energies in the span.

What is *not* in this report: noise models beyond a tolerance; finite temperature (soft
basins, identification inside an envelope class); anything about real instruments.  §8 lists
the limitations, §9 the open problems.

---

## 1. Setting and notation

`X` is a compact metric space (often finite) of configurations, `P(X)` its Borel probability
measures (*ensembles*).  `Φ = (φ_1, …, φ_m) : X → ℝ^m` is a continuous family of observables
and `Aν = ∫ Φ dν ∈ ℝ^m` the *data* of `ν`.  The *moment body* is `𝒦 = A(P(X)) = conv Φ(X)`,
compact and convex.  `‖·‖` is a norm on `ℝ^m` in which data errors are measured, `‖·‖_*` its
dual.  For `λ ∈ ℝ^m` the function `E_λ = λ·Φ` is called an *energy in the span of the
observables*.

`μ` is **identified** (by `Φ`) if `Aν = Aμ` implies `ν = μ` for every `ν ∈ P(X)`: no prior
on `ν` — no sparsity, no model, no class.  A *conformer* is an atom of a finitely supported
ensemble; a *conformation* is an ensemble `δ_x`.

An *envelope* is a function `d ≥ 0` on `X × X` with `d(x,x) = 0` and the triangle inequality,
not necessarily symmetric; `g` is *admissible* if `g(x) − g(y) ≤ d(x,y)` (theory report §1;
`IsEnvelope`, `Admissible`).  For a symmetric `d`, `W₁` is the transport distance with cost
`d` and `‖h‖_KR = sup{∫ g dh : g admissible}` the Kantorovich–Rubinstein norm of a signed
measure of total mass zero, so that `W₁(μ, ν) = ‖ν − μ‖_KR` **[K]**.

---

## 2. Part I — Observability as exposedness

### 2.1 Which ensembles are identified

**Theorem E1 (identified = exposed simplex).**
(a) *Finite `X`.*  Let `μ ∈ P(X)` have support `S`.  Then `μ` is identified by `Φ` iff
 (i) the vectors `(1, Φ(x))`, `x ∈ S`, are linearly independent, and
 (ii) there are `c ∈ ℝ`, `λ ∈ ℝ^m` with `f := c + λ·Φ ≥ 0` on `X` and `{f = 0} = S`.
(b) *Compact `X`.*  Let `G` be the minimal face of `𝒦` containing `Aμ`.  Then `μ` is
identified iff `X_G := Φ^{-1}(G)` is finite and the vectors `(1, Φ(x))`, `x ∈ X_G`, are
linearly independent; in that case `supp μ = X_G`.  In particular an identified ensemble has
at most `m + 1` conformers.

Condition (ii) says: `S` is exactly the set of ground states of the energy `E_λ` — in the
language of the programme, `S` is the contact set of a *frustration-free* energy in the span
of the observables.  **[P]**; (a) "if" is **[V]** `Ensemble.eq_of_exposing_certificate`
(non-vacuity witness `ensemble_exposing_certificate_witness`).

*Proof of (a).*  `μ` is identified iff the cone
`T = {h ∈ ℝ^X : h ⊥ span{1, Φ}, h(x) ≥ 0 for x ∉ S}` is `{0}`: if `ν ≠ μ` has the data of `μ`
then `ν − μ ∈ T ∖ {0}`; conversely for `h ∈ T ∖ {0}` the vector `μ + εh` is, for small `ε > 0`,
another ensemble with the same data (`μ > 0` on `S`; `Σ h = 0` because `h ⊥ 1`).
*If.*  Let `h ∈ T`.  Then `0 = Σ_x h(x) f(x) = Σ_{x ∉ S} h(x) f(x)`, a sum of non-negative
terms with `f > 0`, so `h = 0` off `S`; then `Σ_{x∈S} h(x)(1, Φ(x)) = 0` and (i) gives `h = 0`.
*Only if.*  (i): a non-zero `h` supported on `S` with `h ⊥ span{1,Φ}` is in `T`.  (ii): let
`F = span{1, Φ}` (functions on `X`) and `F_S = {f ∈ F : f|_S = 0}`.  By Stiemke's theorem of
the alternative applied to the subspace `F_S|_{X∖S}` of `ℝ^{X∖S}`, either some `f ∈ F_S` is
positive on `X ∖ S` — which is (ii) — or there is a non-zero `g ≥ 0` on `X ∖ S` with
`Σ_{x∉S} g(x) f(x) = 0` for all `f ∈ F_S`.  In the second case the functional `f ↦ ⟨g, f⟩` on
`F` vanishes on the kernel `F_S` of the restriction map `F → ℝ^S`, hence factors through it:
`⟨g, f⟩ = Σ_{x∈S} a(x) f(x)` for some `a ∈ ℝ^S` and all `f ∈ F`.  Then `h = g − a` is orthogonal
to `F`, equals `g ≥ 0` off `S`, and is not zero: `h ∈ T ∖ {0}`, a contradiction.  ∎

*Proof of (b).*  *Every ensemble with data `y = Aμ` is carried by `X_G`.*  If `y` is in the
relative interior of `𝒦` there is nothing to prove.  Otherwise there is an affine `ℓ ≥ 0` on
`𝒦`, not identically zero on `𝒦`, with `ℓ(y) = 0`; for `ν` with `Aν = y`,
`∫ ℓ∘Φ dν = ℓ(y) = 0` and `ℓ∘Φ ≥ 0`, so `ν` is carried by `X₁ = {ℓ∘Φ = 0}`, a compact set with
`conv Φ(X₁) = 𝒦 ∩ {ℓ = 0}`, a proper face containing `y`.  Repeat with `(X₁, 𝒦 ∩ {ℓ = 0})`; the
dimension drops, and the process ends at the face that contains `y` in its relative
interior, which is `G`.
*If.*  Then `G` is a simplex with vertices `Φ(x)`, `x ∈ X_G`, and barycentric coordinates
are unique.  *Only if.*  Let `μ` be the only ensemble with data `y`, and `x₀ ∈ X_G`.  As `y`
is in the relative interior of `G = conv Φ(X_G)`, for small `ε > 0` the point
`z = y + ε(y − Φ(x₀))` is in `G`, so `y = (z + εΦ(x₀))/(1+ε)` is the data of an ensemble that
charges `x₀`; hence `μ({x₀}) > 0` for every `x₀ ∈ X_G`.  If `X_G` had `m + 2` points, or if
the vectors `(1, Φ(x))` were dependent on `X_G`, a non-trivial `Σ_j c_j (1, Φ(x_j)) = 0`
would give the second ensemble `μ + ε Σ_j c_j δ_{x_j}`.  ∎

**Remarks.**  (1) *Known in substance.*  E1 is the statement that a point of a compact
convex set has a unique representing measure on a generating set iff it lies in a
simplicial face over which the generating map is injective; for moment problems on an
interval it is the theory of principal representations, and (ii) is the *dual certificate*
of non-negative sparse recovery.  What is specific here is the reading (ii) ↔ ground states.
(2) *Faces need not be exposed on continua.*  In (a), `G` is exposed by one `f`.  In (b) the
iteration is needed: there are identified ensembles with no single certificate, and their
identification is not Lipschitz-stable (Example E1.2).
(3) *Numerical check* **[N]** (`experiments/ensemble/exposedness_checks.py`, T1): on 1 500
random instances (5–9 configurations, 1–4 integer-valued observables) the certificate
criterion (two linear programmes) and the direct test (the fibre is a point, by `2|X|`
linear programmes) agree in all cases; 965 of the instances are identified.

**Proposition E1.1 (what a certificate gives quantitatively) [V, P].**  Let `X` be finite,
`μ` supported on `S`, `f = c + λ·Φ` with `f = 0` on `S` and `f ≥ γ > 0` off `S`.  For every
ensemble `ν`:

    ν(X ∖ S)  ≤  ‖λ‖_* · ‖Aν − Aμ‖ / γ .

(**[V]** `Ensemble.mass_off_support_le`, in the form with `Σ_i |λ_i|·|Δdata_i|`.)  If moreover
`σ > 0` is such that `‖(Σ_{x∈S} h(x), Σ_{x∈S} h(x)Φ(x))‖_{1 ⊕ ‖·‖} ≥ σ‖h‖₁` for all `h ∈ ℝ^S`, then

    ‖ν − μ‖₁  ≤  [ (1 + (1 + R)/σ)·‖λ‖_*/γ + 1/σ ] · ‖Aν − Aμ‖ ,     R = max_x ‖Φ(x)‖ .

*Proof.*  `γ·ν(X∖S) ≤ ∫ f dν = ∫ f dν − ∫ f dμ = λ·(Aν − Aμ)`.  For the second bound put
`p = ν(X ∖ S)` and `h = (ν − μ)|_S`; then `|Σ_S h| = p` and
`‖Σ_S h Φ‖ ≤ ‖Aν − Aμ‖ + pR`, so `‖h‖₁ ≤ (p + ‖Aν − Aμ‖ + pR)/σ`, and `‖ν − μ‖₁ = p + ‖h‖₁`.  ∎

So an identification certificate is a triple `(λ, γ, σ)`: an energy in the span, its gap
above the ground states, and the conditioning of the features on the ground states.
Certifying `γ` is certifying a lower bound on a minimum over `X ∖ S` of `c + E_λ` — for
pairwise `Φ` on a product space, a task of the verified `(min,+)` kernel.

**Example E1.2 (identified but only Hölder-stable) [P].**  `X = [−1, π/2]`,
`Φ(t) = (1, t)` for `t ≤ 0` and `Φ(t) = (cos t, sin t)` for `t ≥ 0` (a `C¹` curve: a segment
continued by a circular arc).  The conformation `δ₀` is identified: an ensemble with data
`(1, 0)` is carried by `{φ₁ = 1} = [−1, 0]` and has `∫ t dν = 0` there.  But `(1,0)` is a
non-exposed extreme point of `𝒦`, there is no single certificate, and for small `t > 0` the
ensemble `ν_t = p·δ_t + (1−p)·δ_{−1}` with `p = 1/(1 + sin t)` has data
`(1 − p(1 − cos t), 0)`, at distance `τ ≈ t²/2` from the data of `δ₀`, while
`W₁(ν_t, δ₀) = p·t + (1 − p) ≈ 2t ≈ 2√(2τ)`.  On a finite `X` this cannot happen: every
identified ensemble has a certificate, hence a linear modulus (E1.1).

**Corollary E1.3 (observables that are quadratic in the coordinates) [P].**
(a) On `ℝ^D`, an ensemble with finite second moments is determined by its first and second
moments among such ensembles iff it is a conformation.  (b) Let `G` be any graph on `N`
points in `ℝ^d` — the complete graph included.  No ensemble of frameworks with a
non-degenerate conformer is determined modulo congruence by its mean squared edge lengths:
if `μ` does not give probability one to "all edges have length zero", and `R ≥ 0` is
independent of the configuration `p` with `R² ∈ {0, 2}` with probability `½` each, then the
law `ν` of `R·p` has the same mean squared length of every pair and is not congruent to `μ`.

*Proof.*  (a) "If": the covariance vanishes.  "Only if": with covariance `Σ ≠ 0` the
Gaussian law with the same mean and covariance, or — if `μ` is that Gaussian — any other law
with them, is a second ensemble.  (b) `E|Rp_u − Rp_v|² = E R²·E|p_u − p_v|²`.  With
`Q = Σ_{uv}|p_u − p_v|²`, `P_ν(Q = 0) = ½ + ½P_μ(Q = 0) > P_μ(Q = 0)` unless `P_μ(Q = 0) = 1`,
and `Q` is invariant under congruence.  ∎

Mean squared distances carry the mean *Gram* structure and nothing about fluctuations;
they cannot even certify that the ensemble is a single conformation.  The first data that
can are two different moments of the same distance (equality in Jensen's inequality), and
§3 shows what `2K` moments do.

### 2.2 One conformation: the exact modulus, and the bridge to robust optimality

Let `x⋆ ∈ X` and let `ρ : X → [0, ∞)` be continuous with `ρ(x⋆) = 0` (a loss: how far an
ensemble is from the conformation `x⋆`).  The *identification modulus* is

    ω(τ) = sup{ ∫ ρ dν : ν ∈ P(X), ‖Aν − Φ(x⋆)‖ ≤ τ } ,      τ ≥ 0 .

**Theorem E2 (duality; the identification constant; the bridge).**
(a) For every `τ ≥ 0`:

    ω(τ) = inf_{λ ∈ ℝ^m} { τ‖λ‖_* + max_{y ∈ X} [ ρ(y) − λ·(Φ(y) − Φ(x⋆)) ] } ,

and the infimum is attained for `τ > 0`.
(b) `ω` is concave and non-decreasing.  Put

    κ = inf{ ‖λ‖_* : λ·(Φ(y) − Φ(x⋆)) ≥ ρ(y) for all y ∈ X }     (inf ∅ = ∞).

Then `ω(τ) ≤ κτ` for all `τ`, the infimum is attained when finite, and
`κ = sup_{τ>0} ω(τ)/τ = lim_{τ↓0} ω(τ)/τ`: **`κ` is the best constant in a linear bound.**
(c) *The bridge.*  Let `d` be an envelope and `ρ = d(x⋆, ·)`.  The constraint in `κ` reads

    d(x⋆, y) ≤ E_λ(y) − E_λ(x⋆)        for all y,

which is the sharp-minimum condition of theory report Theorem 2.4.  Hence, by that theorem:
**`κ < ∞` iff some energy `E_λ` in the span of the observables has `x⋆` as its minimiser for
every admissible residual `g` (`x⋆ ∈ argmin(E_λ + g)` for all `g` with `g(x) − g(y) ≤ d(x,y)`),
and `κ` is the least dual norm of such an energy.**  For every ensemble `ν` and every
admissible `g`:

    E_ν g  ≥  g(x⋆) − ∫ d(x⋆, y) dν(y)  ≥  g(x⋆) − κ·‖Aν − Φ(x⋆)‖ .

**[P]** for (a), (b); in (c) the two inequalities and the passage through Theorem 2.4 are
**[V]**: `Ensemble.transport_le_of_sharp` (with a modulus `s`),
`Ensemble.identification_of_robust_certificate` (hypothesis: the left-hand side of
`robust_certified_iff`; conclusion: `∫ d(x⋆,·) dν ≤ Σ_i |λ_i|·|E_νφ_i − φ_i(x⋆)|`),
`Ensemble.robust_certificate_of_sharp`, `Ensemble.residual_advantage_le`.

*Proof.*  (a) For `v ∈ ℝ^m`, `inf_λ [τ‖λ‖_* − λ·v]` is `0` if `‖v‖ ≤ τ` and `−∞` otherwise.
Hence `ω(τ) = sup_ν inf_λ L(ν, λ)` with
`L(ν, λ) = ∫ ρ dν − λ·(Aν − Φ(x⋆)) + τ‖λ‖_*`, which is affine and weak-* continuous in `ν` on the
convex compact `P(X)` and convex in `λ`.  By Sion's minimax theorem
`sup_ν inf_λ L = inf_λ sup_ν L`, and `sup_ν` of an affine functional of `ν` is the maximum
over point masses.  The bracket is `≥ 0` (take `y = x⋆`), so the objective is at least
`τ‖λ‖_*`: coercive for `τ > 0`.
(b) `ω` is the value of a linear programme in `ν` as a function of the right-hand side:
concave; monotone because the feasible set grows.  `ω(τ) ≤ κτ`: insert a feasible `λ` in (a).
Conversely let `κ' = sup_τ ω(τ)/τ < ∞`.  Then `ω(0) = 0`, and for each `τ > 0` a minimiser
`λ_τ` of (a) satisfies `τ‖λ_τ‖_* + M(λ_τ) ≤ κ'τ` with
`M(λ) = max_y[ρ(y) − λ·(Φ(y) − Φ(x⋆))] ≥ 0`; so `‖λ_τ‖_* ≤ κ'` and `M(λ_τ) ≤ κ'τ → 0`.  A limit
point `λ₀` has `‖λ₀‖_* ≤ κ'` and `M(λ₀) = 0`, i.e. it is feasible for `κ`: `κ ≤ κ'`.  The ratio
`ω(τ)/τ` is non-increasing by concavity and `ω(0) = 0`.
(c) is a reading of (b) together with `robust_certified_iff`; the first inequality of the
display is `g(x⋆) − g(y) ≤ d(x⋆, y)` integrated.  ∎

**Reading.**  Theorem 2.4 of the theory report says when a configuration is *certifiably
optimal without evaluating the residual anywhere*: when the known energy grows away from it
at least as fast as the envelope.  Theorem E2 says that the same inequality, for an energy
built from *measured observables*, is exactly what makes averaged data pin an ensemble to
that configuration, and that the best constant is a norm of the certificate.  The two
uncertainty models are dual to each other — an unknown residual in a Lipschitz class
against an unknown ensemble in a transport ball — and the pointwise form of that duality is
the sharp minimum.  (For a general reference ensemble the duality is the known formula for
distributionally robust expectations over transport balls; `PRIOR_ART.md` §2.)

*Numerical check* **[N]** (`exposedness_checks.py`, T2): 400 random instances with the `ℓ^∞`
data norm; primal and dual values agree to `3·10⁻¹⁵` at four tolerances; where `κ` is finite
(301 instances) `ω(10⁻⁴)/10⁻⁴ = κ` to `4·10⁻¹⁵` and `ω(τ) ≤ κτ` throughout.

**Example E2.1 (the cube, one-body data).**  `X = {0,1}ⁿ`, `d` the Hamming distance,
`Φ(x) = x`, `x⋆ = 0`, data errors in `ℓ^∞`.  The constraint `Σ λ_i y_i ≥ |y|` forces `λ_i ≥ 1`,
so `κ = n`: `E_ν d_H(·, 0) ≤ nτ`, with equality when every site is flipped with probability `τ`.  With errors in `ℓ¹`
the constant is `1`.  The constant is extensive exactly when the errors are per-observable.

### 2.3 Finite ensembles: the first-order constant

Let `X` be finite with a metric `d`, `μ` identified with support `S`, and

    ω_μ(τ) = sup{ W₁(ν, μ) : ν ∈ P(X), ‖Aν − Aμ‖ ≤ τ } .

**Theorem E3 (the first-order identification constant).**  Let
`T₁ = {h ∈ ℝ^X : Σ h = 0, h ≥ 0 off S, ‖Ah‖ ≤ 1}` (compact, because `μ` is identified) and

    κ_μ = max_{h ∈ T₁} ‖h‖_KR .

(a) `ω_μ(τ) ≤ κ_μ τ` for all `τ ≥ 0`, with equality for
`τ ≤ τ₀ = min_{x∈S} μ(x) / max_{h∈T₁} ‖h‖_∞`.
(b) `κ_μ = max_{g 1-Lipschitz} κ(g)`, where `κ(g)` is the least coefficient norm of an
*interpolating majorant* of `g` in the span:

    κ(g) = min{ ‖λ‖_* : c + λ·Φ ≥ g on X,  c + λ·Φ = g on S } .

(c) `κ_μ` depends on `S` only — not on the weights of `μ`, which enter through `τ₀` alone.
For `S = {x⋆}`, `κ_μ` is the constant `κ` of Theorem E2 with `ρ = d(x⋆, ·)`.

**[P]**.

*Proof.*  For `ν ∈ P(X)` put `h = ν − μ`: `Σ h = 0`, `h ≥ −μ`, in particular `h ≥ 0` off `S`,
and `W₁(ν, μ) = ‖h‖_KR`.  So the feasible `h` form `H_τ = {h ∈ τT₁ : h ≥ −μ}`, which gives
`ω_μ(τ) ≤ κ_μτ`, and `H_τ = τT₁` as soon as `τ‖h‖_∞ ≤ min_S μ` on `T₁`: (a).  For (b),
`κ_μ = max_g max_{h∈T₁} ⟨g, h⟩`, and for fixed `g` the inner problem is a linear programme
whose dual — multipliers `c` for `Σh = 0` and `λ` for `‖Ah‖ ≤ 1`; `h` free on `S`, `h ≥ 0`
off `S` — is `κ(g)`.  (c): `T₁` is defined by `S`.  For `S = {x⋆}` the constraint is
`λ·(Φ(y) − Φ(x⋆)) ≥ g(y) − g(x⋆)`, and the largest right-hand side over 1-Lipschitz `g` is
`d(x⋆, y)`, attained simultaneously in `y` by `g = d(x⋆, ·)`.  ∎

**Reading.**  To first order, how well data pin an identified ensemble does not depend on
its populations, only on *where* its conformers are; the populations decide how small the
data error must be before the first-order regime starts.  Computing `κ_μ` is a maximisation
of a convex function over the Lipschitz polytope and is not a linear programme; `κ(g)` for a
given test function is.  *Numerical check* **[N]** (`exposedness_checks.py`, T3): on 60
random instances `κ_μ` computed by enumerating the vertices of `T₁` equals `κ(g⋆)` for the
Kantorovich potential `g⋆` of the maximiser to `7·10⁻¹⁵`, no sampled `g` exceeds it, and
`ω_μ(τ)/τ = κ_μ` at `τ = τ₀/2` for two random weightings of each support to `5·10⁻¹⁶`.

---

## 3. Part II — Laws of observables: chimeras, and ensemble rigidity

Some measurements return more than a mean: the whole distribution of a scalar feature (a
distance distribution).  The law of a feature `T` is still linear information about the
ensemble — the means of all functions `h∘T` — so the model of §1 covers it.  What is lost is
the *joint* law of different features: averaging destroys correlations between observables.

### 3.1 A Rényi–Heppes theorem for arbitrary observables

Rényi (1952): a distribution with `K` atoms in the plane is determined by its projections on
`K + 1` distinct lines; Heppes (1956): the same in `ℝ^d` **[K]**.  The proof uses one property
of projections — two of them determine the point — and nothing else.

Let `X` be a set and `T_j : X → Y_j`, `j = 1, …, m`, maps (measurable, between standard Borel
spaces).  The family is **`r`-determining** if two distinct points of `X` agree on fewer than
`r` of the features.

**Theorem E4 (Rényi–Heppes for arbitrary features).**  Let `(T_j)_{j≤m}` be `r`-determining,
`μ` a probability measure on `X` with at most `K` atoms and no other mass, and `ν` *any*
probability measure on `X` with `(T_j)_# ν = (T_j)_# μ` for all `j`.  If `m ≥ K(r − 1) + 1`, then
`ν = μ`.  The bound is sharp for every `K ≥ 2` and `r ≥ 2`: there are `r`-determining families
of `K(r−1)` linear functionals on `ℝ^r` and two different ensembles of `K` conformers with
the same `K(r−1)` laws.

**[V]** for finite `X`: `Ensemble.renyi_heppes` (stated for weight vectors: `ν ≥ 0` arbitrary,
`μ` supported on at most `K` points; non-vacuity witness `ensemble_renyi_heppes_grid`: a weight
vector on the `3 × 3` grid with at most two atoms is determined by its row, column and
diagonal sums).  **[P]** in general.

*Proof.*  Let `S = supp μ`, `|S| ≤ K`.  The law of `T_j` under `ν` is carried by the finite set
`T_j(S)`, so `ν(B) = 1` for `B = ∩_j T_j^{-1}(T_j(S))`.  Let `y ∈ B`: for each `j` choose
`a_j ∈ S` with `T_j(y) = T_j(a_j)`.  Some `a ∈ S` is chosen for at least `⌈m/K⌉ ≥ r` indices, so
`y` agrees with `a` on `r` features and `y = a`.  Hence `ν` is carried by `S`.  Weights: fix
`a ∈ S`.  Every other `b ∈ S` agrees with `a` on at most `r − 1` features, so at most
`(K−1)(r−1) < m` features fail to separate `a` from the rest of `S`; for a `j` that does,
`ν({a}) = (T_j)_#ν({T_j(a)}) = (T_j)_#μ({T_j(a)}) = μ({a})`.
*Sharpness.*  In a plane `Π ⊂ ℝ^r` take the vertices of a regular `2K`-gon, coloured
alternately, and let `μ`, `ν` be uniform on the two colour classes; the `K` directions
`θ_1, …, θ_K ∈ Π` normal to the `K` classes of parallel edges project both classes onto the
same multisets (each edge joins the two colours).  For each `k` choose `r − 1` vectors
`θ_k + v_{k,1}, …, θ_k + v_{k,r−1}` with `v_{k,i} ∈ Π^⊥` in general position.  Each of these
`K(r−1)` functionals restricts to `Π` as `⟨θ_k, ·⟩`, so `μ` and `ν` have the same laws; and
any `r` of them are linearly independent — they cannot all belong to one `k`, so their
`Π`-components span `Π`, and the `Π^⊥`-components are generic — so the family is
`r`-determining.  ∎

*Numerical check* **[N]**: the witness in Lean; the square `K = 2` (`{(1,1), (−1,−1)}` and
`{(1,−1), (−1,1)}` have the same two coordinate laws).

For frameworks the theorem is weak: a set of edge lengths determines a configuration only
if it is globally rigid, so `r` is almost the whole edge set and `K(r−1) + 1 ≤ |E|` forces
`K = 1`.  Worst-case counting is the wrong tool there; the next theorem is the right one.

### 3.2 Splices on a variety

Let `F = (F_1, …, F_m) : ℝ^D → ℝ^m` be a polynomial map (the *feature map*).  Its **algebraic
matroid** `𝓜(F)` on `[m]` has as independent sets the algebraically independent subsets of
`{F_e}`; its rank function is `r(J) =` the generic rank of the Jacobian of `F_J = (F_e)_{e∈J}`
`=` the dimension of the Zariski closure of `F_J(ℝ^D)` **[K]** (Jacobian criterion,
characteristic zero).  `V` denotes the Zariski closure of `F(ℝ^D)`, the *feature variety*; it
is irreducible of dimension `r([m])`.  A matroid is *connected* if `r(J) + r([m]∖J) > r([m])`
for every proper non-empty `J` **[K]**.

For points `x_1, …, x_K ∈ ℝ^D` and a map `a : [m] → [K]` (a *colouring* of the features by the
points) the **splice** is the vector `q^a = (F_e(x_{a(e)}))_{e∈[m]}`.  It has, coordinate by
coordinate, a feature value of one of the points.  A splice with a non-constant colouring
that is the feature vector of an actual configuration is a **chimera**.

**Theorem E5 (splices and the algebraic matroid).**  Assume no `F_e` is constant.
(a) If `𝓜(F)` is connected then for every `K ≥ 2` there is a proper algebraic subset
`B_K ⊂ (ℝ^D)^K`, defined over the field of the coefficients of `F`, such that for every
`(x_1, …, x_K) ∉ B_K` and every non-constant colouring `a`: `q^a ∉ V`.  In particular there is no
chimera.
(b) If `𝓜(F)` is not connected, let `J` be a proper non-empty set with
`r(J) + r(J^c) = r([m])`.  Then `V = V_J × V_{J^c}` (the closures of the two coordinate
projections), every splice of two points along `(J, J^c)` lies in `V`, and there is a
non-empty open set of pairs `(x, x') ∈ (ℝ^D)²` for which both splices along `(J, J^c)` are
chimeras: `(F_J(x), F_{J^c}(x')) = F(y)`, `(F_J(x'), F_{J^c}(x)) = F(y')`.

**[P]**.

*Proof.*  (a) Fix a non-constant `a` with non-empty classes `J_1, …, J_k`, `k ≥ 2`, and the
polynomial map `s_a : (ℝ^D)^K → ℝ^m`, `s_a(x_1, …, x_K) = q^a`.  Its coordinates are polynomials
in disjoint groups of variables for different classes, so its Jacobian is block diagonal
and its generic rank is `Σ_i r(J_i)`; the Zariski closure `W_a` of its image is irreducible
of that dimension.  By connectedness and subadditivity of the rank,
`Σ_i r(J_i) ≥ r(J_1) + r([m] ∖ J_1) > r([m]) = dim V`, so `W_a ⊄ V`: some polynomial `P_a` of
the ideal of `V` does not vanish identically on the image of `s_a`.  Then
`B_a = {P_a ∘ s_a = 0}` is a proper algebraic subset of `(ℝ^D)^K`, and `B_K = ∪_a B_a` is a
finite union.  For a tuple outside `B_K`, `P_a(q^a) ≠ 0`, so `q^a ∉ V`.  (The ideal of `V` is the
kernel of `y_e ↦ F_e`, generated over the coefficient field of `F`.)
(b) `V ⊆ V_J × V_{J^c}`; the product is the closure of the image of
`(x, x') ↦ (F_J(x), F_{J^c}(x'))`, hence irreducible, of dimension `r(J) + r(J^c) = dim V`; two
irreducible varieties of the same dimension, one inside the other, coincide.  For the
realisability take `x₀` at which the Jacobians of `F`, `F_J`, `F_{J^c}` have their generic
ranks.  By the constant-rank theorem `F`, `F_J`, `F_{J^c}` map a neighbourhood `U` of `x₀` onto
embedded submanifolds `N`, `N_J`, `N_{J^c}` of dimensions `r([m])`, `r(J)`, `r(J^c)`, and
`N ⊆ N_J × N_{J^c}`, a manifold of the same dimension; so `N` is open in `N_J × N_{J^c}` and
contains `(F_J(x), F_{J^c}(x'))` for all `x, x'` near `x₀`.  ∎

*Remark (closest prior art).*  The product structure in (b) is Lemma 3.1 of
Garamvölgyi–Gortler–Jordán (2022) for measurement varieties of graphs.  Recovering a matrix
from the entries of its columns in unknown order is *unlabeled principal component analysis*
(Yao–Peng–Tsakiris 2021/2024): there the rows lie on an unknown generic linear subspace and
uniqueness up to row permutation is proved for rank `r < min(m, n)`; here the variety is
known and arbitrary, and the criterion is matroid connectivity.  We have not found (a).

**Corollary E6 (identification from the laws of the coordinates).**  Let `𝓜(F)` be connected
and no `F_e` constant.  There is a proper algebraic subset `B'_K ⊂ (ℝ^D)^K` such that for
`(x_1, …, x_K) ∉ B'_K`, weights `w_i > 0`, `μ = Σ_i w_i δ_{x_i}`, and **any** Borel probability
measure `ν` on `ℝ^D` with `(F_e)_#ν = (F_e)_#μ` for every `e`:

    F_# ν = F_# μ      (the ensembles of feature vectors coincide),

i.e. `ν` is carried by `∪_i F^{-1}(F(x_i))` and `ν(F^{-1}(F(x_i))) = w_i`.  **[P]**.

*Proof.*  `B'_K = B_K ∪ ⋃_{e, i<j} {F_e(x_i) = F_e(x_j)}`, proper because no `F_e` is constant.
`ν`-almost every `y` has `F_e(y) ∈ {F_e(x_i)}_i` for all `e`; the index `a(e)` with
`F_e(y) = F_e(x_{a(e)})` is unique, and `F(y) = q^a ∈ V`, so `a` is constant by E5(a):
`F(y) = F(x_i)` for some `i`.  The weights: `ν(F^{-1}F(x_i)) = (F_e)_#ν({F_e(x_i)}) = w_i` for any
`e`.  ∎

So for marginal laws the picture is: **identification of finite ensembles = absence of
chimeras = connectivity of the algebraic matroid**, plus injectivity of `F` on single
configurations, which is a question about one conformation at a time.

### 3.3 Ensemble rigidity

Let `G = (V, E)` be a graph on `N` vertices, `d ≥ 1`, and
`F = m_{d,G} : (ℝ^d)^N → ℝ^E`, `p ↦ (|p_u − p_v|²)_{uv∈E}`, the squared-edge-length map.  The
Jacobian of `F` is twice the rigidity matrix, so `𝓜(F)` is the generic `d`-dimensional
rigidity matroid `R_d(G)`.  `G` is *generically globally rigid* in `ℝ^d` if for generic `p`
every `q` with `F(q) = F(p)` is congruent to `p`.  Two cited theorems:

* **[K]** (Gortler–Healy–Thurston 2010) global rigidity is a generic property: either every
  generic framework of `G` is globally rigid or none is.
* **[K]** (Garamvölgyi–Gortler–Jordán 2022, Theorem 3.5; `d ≤ 2`: Jackson–Jordán 2005) if `G` is
  globally rigid in `ℝ^d` on at least `d + 2` vertices, then `R_d(G)` is connected.

Here "generic" for a tuple of configurations means: its `dNK` coordinates are algebraically
independent over `ℚ` (in particular outside every proper algebraic subset defined over `ℚ`,
and true for Lebesgue-almost every tuple).

**Theorem E7 (ensemble rigidity = global rigidity).**  Let `N ≥ d + 2`.  The following are
equivalent.
(a) `G` is generically globally rigid in `ℝ^d`.
(b) For every `K ≥ 1`, every generic `(x_1, …, x_K) ∈ ((ℝ^d)^N)^K` and all weights `w_i > 0`: if
`ν` is a Borel probability measure on `(ℝ^d)^N` such that, for every edge `e`, the law of the
length of `e` under `ν` equals its law under `μ = Σ_i w_i δ_{x_i}`, then `ν = μ` modulo
congruence: `ν` is carried by the congruence classes `[x_i]` and `ν([x_i]) = w_i`.

**[P]**, given the two cited theorems.

*Proof.*  (b) ⇒ (a) is `K = 1`.  (a) ⇒ (b): `R_d(G)` is connected and no edge length is
constant, so Corollary E6 applies (its exceptional set is defined over `ℚ`, hence avoided by
generic tuples): `ν` is carried by `∪_i F^{-1}(F(x_i))` with the right masses; each `x_i` is
generic, so `F^{-1}(F(x_i)) = [x_i]`.  ∎

**Reading.**  Global rigidity is a statement about one configuration.  The theorem says it
is automatically a statement about *mixtures of any number of them*: a graph whose edge
lengths determine a generic conformation has edge-length **distributions** — one
one-dimensional law per edge, no joint information — that determine a generic finite
ensemble.  The mechanism is that a globally rigid graph has no way to borrow some lengths
from one conformer and the rest from another.  The hypothesis `N ≥ d + 2` matters: the
triangle in the plane is globally rigid, its rigidity matroid is free, and the ensembles
`½δ_{(3,4,5)} + ½δ_{(4,5,6)}` and `½δ_{(3,5,6)} + ½δ_{(4,4,5)}` (side lengths) have the same three
edge-length laws.

**Corollary E8 (finitely many means; an explicit certificate).**  In the situation of
Theorem E7(a), let `μ = Σ_{i≤K} w_i δ_{x_i}` be generic.  If `ν` is a Borel probability
measure on `(ℝ^d)^N` with

    ∫ ℓ_e^{2j} dν = ∫ ℓ_e^{2j} dμ        for every edge e and j = 1, …, 2K

(`ℓ_e` the length of `e`), then `ν = μ` modulo congruence.  These are `2K|E|` scalar means of
polynomial observables.  The function

    f(p) = Σ_{e∈E} Π_{i=1}^{K} ( ℓ_e(p)² − ℓ_e(x_i)² )²

is a certificate in the sense of Theorem E1: it is non-negative, lies in the span of
`{1, ℓ_e^{2j}}`, and its zero set is `∪_i [x_i]`.  **[P]**.

*Proof.*  `∫ f dν = ∫ f dμ = 0`, so `ν`-almost every `p` has every `ℓ_e(p)²` among the
`ℓ_e(x_i)²`: the law of each `ℓ_e²` under `ν` is carried by the `K` atoms of its law under `μ`
and has the same moments of orders `0, …, K − 1`, hence the same weights (Vandermonde).  So
all edge-length laws agree and Theorem E7 applies.  The zero set of `f` is the set of
configurations all of whose squared edge lengths occur among the conformers', which by
E5(a) and global rigidity is `∪_i [x_i]`.  ∎

The certificate ties Parts I and II together: for marginal-law data the exposing function
is always "sum over features of the product of squared deviations from the conformers'
values", its zero set is the set of all splices that are realisable, and the ensemble is
identified exactly when that set contains nothing but the conformers.  By Corollary E1.3,
`j = 1` alone (mean squared lengths) identifies nothing; `j ≤ 2` certifies a single
conformation (`E ℓ⁴ = (E ℓ²)²` forces every measured length to be constant); `j ≤ 2K` resolves
`K` conformers.

*Numerical checks* **[N]** (`experiments/ensemble/rigidity_checks.py`).  R1: rank and
connectivity of the rigidity matroids of `K₄`, `K₅`, the wheel `W₅` in the plane and `K₅`, `K₆`
in space (connected), and of the triangle, `K₄` minus an edge and `K₄` plus a vertex of
degree two in the plane (not connected), by brute force over all subsets.  R2: for `K₄` in
the plane and `K₅` in space, with two and three random conformers, the Cayley–Menger
determinant of every non-constant splice examined (1 240; 2 904; 20 440; 79 998) is at
least `1.6·10⁻³` in absolute value, against `10⁻¹²` at the conformers.  R3: for the wheel,
least squares from 25 starts leaves a residual of at least `6·10⁻⁴` on 180 random splices
(`3·10⁻¹⁵` at a conformer).  R4: the triangle example; for `K₄` plus a vertex of degree two
the splice along the separator is realised exactly when two circles meet (40 of 40
agreements, 31 realised).  R5: all 22 zeros of the certificate `f` found from 400 starts for
`K₄` with two conformers have the edge lengths of one of the conformers.

### 3.4 Continuous ensembles: an obstruction

**Proposition E8.1 [K, with a two-line corollary].**  Let `D ⊂ ℝ^n`, `n ≥ 2`, be a bounded
connected open set and `q_1, …, q_m` continuously differentiable on `D̄`.  There are two
different Borel probability measures on `D̄` with the same law of every `q_i`.

*Proof.*  By the theorem of Vitushkin and Henkin (1967) the sums `Σ_i g_i ∘ q_i` with
continuous `g_i` are nowhere dense in `C(D̄)`; a subspace that is not dense is annihilated by
a non-zero signed measure `σ` (Hahn–Banach, Riesz), i.e. `(q_i)_#σ = 0` for all `i`, and
`σ(D̄) = 0`.  Normalise the positive and negative parts of `σ`.  ∎

So no finite family of smooth scalar observables — however large — determines every
ensemble on a configuration space of dimension at least two through the laws of the
observables, let alone through their means.  Identification from laws is a property of
*classes*: finite ensembles (E4–E8), or exponential families generated by the functions
`g∘q_i` themselves (for pair distances: pair-additive energies; theory report §11.17, the
science division's Proposition 6).  Whether every ensemble with a continuous positive
density is unidentified — a bounded `g ≢ 0` with `E_μ[g | q_i] = 0` for all `i` — is
Conjecture C1 (§9), with a proof strategy.

---

## 4. Part III — Pair data on the cube: how many conformers, how many observables

`X = {±1}ⁿ`; the observables are the `n(n−1)/2` pair products `x_i x_j`; the data of an
ensemble are its pair-correlation matrix `C = E[xxᵀ]` (unit diagonal).  The observables are
even, so everything is modulo the global flip `x ↦ −x`: an *ensemble* in this part is a
probability measure on `X̄ = {±1}ⁿ/±`.  The moment body is the cut polytope `CUT_n`
(in `±1` form), whose vertices are the matrices `xxᵀ`.  By Theorem E1 an ensemble with
support `S ⊂ X̄` is identified iff `conv{xxᵀ : x ∈ S}` is a simplicial face of `CUT_n` — iff
`S` is exactly the set of ground states of some Ising energy `Σ_{i<j} Q_ij x_i x_j` and the
matrices `xxᵀ`, `x ∈ S`, are affinely independent.

### 4.1 The worst case

**Proposition E9 [K; the example P/N].**  (a) Every ensemble with at most three conformers
is determined by its pair correlations among all ensembles.  (b) Four conformers need not
be: on `n = 4` sites the uniform ensemble on `(+,+,+,+)`, `(+,−,−,+)`, `(+,−,+,−)`, `(+,+,−,−)`
has `C = I`, the pair correlations of the uniform ensemble on the cube.

(a) is the theorem that the cut polytope is 3-neighbourly (Deza–Laurent–Poljak 1992;
Deza–Laurent, *Geometry of Cuts and Metrics*) — three distinct vertices of a polytope are
affinely independent — together with Theorem E1.  (b): the four vectors are the rows of a
Hadamard matrix, so its columns are orthogonal.  *Numerical check* **[N]**
(`experiments/ensemble/pair_capacity_checks.py`, C4): by linear programming, all triples of
vertices containing a fixed one are faces for `n = 5, 6` (105 and 465 triples); 10 of 455
four-sets (`n = 5`) and 22 of 1 500 sampled four-sets (`n = 6`) are not.

### 4.2 Typical supports: capacity of order `n`

**Theorem E10 (random conformers are exactly the ground states of an explicit energy).**
Let `x¹, …, x^K` be independent uniform points of `{±1}ⁿ`, `S` the `n × K` matrix with these
columns, `P` the orthogonal projector on its column space, and

    f(x) = ‖x − Px‖² = (n − tr P) − Σ_{i≠j} P_ij x_i x_j ,

a non-negative function in the span of the pair observables.
(a) On the event `𝓔` = {the `x^a` are linearly independent and the only sign vectors in
their span are `±x^a`}, **every** ensemble supported on `{x^a}` — whatever its weights — is
determined by its pair correlations among all ensembles on `X̄`; `f` is a certificate.
(b) `P(𝓔^c) ≤ 2^{−t} + 2^{K+t}(¾)^{n−K−t}` for every integer `t ≥ 0`.  In particular, for
`K ≤ αn` with `α < α₀ := ln(4/3)/ln(8/3) = 0.2933…`, `P(𝓔^c)` is exponentially small in `n`.
(c) **[K]** (Odlyzko 1988) for `K ≤ n − 10n/ln n`, `P(𝓔^c) = (1 + o(1))·4·C(K,3)·(¾)ⁿ`.

**[P]** for (a), (b); (c) is cited (read at the level of a search summary and of a later
paper that restates it; the leading term is confirmed by our enumeration, below).

*Proof.*  (a) The zero set of `f` on the cube is the set of sign vectors in the span, `±S` on
`𝓔`.  If `Σ_a h_a = 0` and `Σ_a h_a x^a_i x^a_j = 0` for `i ≠ j`, then `Σ_a h_a x^a x^{aᵀ} = 0`
(the diagonal is `Σ_a h_a`), and applying this matrix to a vector `y` with `y·x^a = δ_{ab}`
gives `h_b x^b = 0`.  So the features are affinely independent on `S` and Theorem E1(a)
applies on `X̄`.
(b) *Lemma 1 (Littlewood–Offord).*  For `c ∈ ℝ^K` not of the form `±e_a` and `s` uniform on
`{±1}^K`: `P(|⟨c, s⟩| = 1) ≤ ¾`.  Let `t` be the number of non-zero entries of `c`.  `t = 0`:
the probability is `0`.  `t = 1`: `c = γe_a`, `|γ| ≠ 1`: `0`.  `t = 2`: the value is
`±(c_a + c_b)` or `±(c_a − c_b)`, each with probability `½`, and `|c_a + c_b| = |c_a − c_b| = 1`
would give `c_a c_b = 0`: at most `½`.  `t ≥ 3`: condition on all coordinates of `s` but three
in the support; the value is `u + c_aσ_a + c_bσ_b + c_eσ_e`.  For each of the two targets the
sign triples that reach it form an antichain (after changing signs so that the three
coefficients are positive, a larger triple gives a strictly larger sum), so there are at
most `C(3,1) = 3` of them (Sperner): at most `6` of `8`.
*Lemma 2 (Odlyzko).*  The first `K' = K + t` rows of `S` have rank `K` with probability at
least `1 − 2^{−t}`: a subspace of `ℝ^{K'}` of dimension `j − 1` contains at most `2^{j−1}` sign
vectors (its points are determined by `j − 1` coordinates), so the `j`-th column, restricted
to these rows, lies in the span of the earlier ones with probability at most
`2^{j−1−K'}`; sum over `j ≤ K`.
*Union bound.*  On the event of Lemma 2, every `c` with `Sc ∈ {±1}ⁿ` satisfies
`S_{[K']} c = ε` for some `ε ∈ {±1}^{K'}`, and `c` is determined by `ε`: there are at most
`2^{K'}` candidates, and they are functions of the first `K'` rows.  The remaining `n − K'`
rows are independent of them, so by Lemma 1 a candidate that is not `±e_a` survives with
probability at most `(¾)^{n−K'}`.  With `K = αn`, `t = δn` the bound is exponentially small
iff `(α + δ) ln 2 < (1 − α − δ) ln(4/3)`.  ∎

*Numerical checks* **[N]** (`pair_capacity_checks.py`).  C1: Lemma 1 exhaustively on 7 296
rational coefficient vectors (largest probability `¾`, at `(1,1,1)` up to signs).  C2: exact
enumeration of the sign vectors in random spans; frequency of a spurious one against
`4·C(K,3)(¾)ⁿ`: `0.079` against `0.086` (`n = 30`, `K = 10`), `0.027` against `0.028` (`n = 36`,
`K = 12`).  C3: on `n = 9`, 198 random supports with `K = 2, …, 6`: whenever the zero set of
`f` is `±S` the fibre linear programme confirms identification; the smallest gap
`min_{x ∉ ±S} f(x)` observed is `0.43`.

**Reading.**  A typical set of up to almost `n` conformers is *exactly* the set of ground
states of an explicit pairwise energy — the storage problem of associative memories with
zero error, which is where Odlyzko's question came from — and that is the same thing as
being resolved by pair-averaged data, with any populations.  The certificate is a positive
semidefinite form; finding the conformers from `C` means finding the sign vectors in its
range, and *verifying* the certificate means certifying `min_{x ∉ ±S} f(x) > 0`, a
minimisation of a dense pairwise energy.  The known efficient recovery through the standard
semidefinite relaxation is guaranteed under the much stronger *Schur independence* of the
conformers, which requires `K(K−1)/2 + 1 ≤ n` (Kueng–Tropp 2021): between `√(2n)` and `n`
conformers the ensemble is identified by Theorem E10 but that guarantee is not available.

**Theorem E11 (beyond `6.34 n` conformers nothing is identified).**  Let `n → ∞`,
`n/K → y ∈ (0, y₁)` with `y₁ = (1 − √(1 − 2/π))² = 0.1578…` (i.e. `K/n → 1/y > 6.338`), and let `μ` be
the uniform ensemble on `K` independent uniform conformers.  With probability tending to
one there is an ensemble with full support on the cube that has the pair correlations of
`μ`.  **[P]**, given **[K]**: Bai–Yin's theorem on the smallest singular value, and
Sheppard's formula `E[sign g_i · sign g_j] = (2/π) arcsin R_ij` for a centred Gaussian vector
with correlation matrix `R`.

*Proof.*  `C = SSᵀ/K`.  Let `R_ij = sin(πC_ij/2)` for `i ≠ j`, `R_ii = 1`.  If `R` is positive
definite, the signs of `g ∼ N(0, R)` have full support and pair correlations
`(2/π) arcsin R_ij = C_ij`.  Write `E = C − I` and `R = I + (π/2)E − H` with
`|H_ij| ≤ (π/2)³|E_ij|³/6`.  (i) `λ_min(C) → (1 − √y)²` almost surely (Bai–Yin), so
`λ_min(I + (π/2)E) → 1 − (π/2)(2√y − y)`, positive iff `√y < 1 − √(1 − 2/π)`.  (ii) For `i ≠ j`,
`E_ij` is the mean of `K` independent signs, so `E[E_ij⁶] ≤ 15/K³`, and
`‖H‖_op² ≤ ‖H‖_F² ≤ (π³/48)² Σ_{i≠j} E_ij⁶`, whose expectation is at most
`(π³/48)²·15 n²/K³ → 0`.  ∎

*Numerical check* **[N]** (C5, `n = 300`): the smallest eigenvalue of `R` is `−0.057` at
`K = 5.5n`, `+0.012` at `6.34n`, `+0.040` at `7n`.

So the number of typical conformers that pair data resolve is `Θ(n)`: at least
`n − 10n/ln n`, fewer than `6.34n` (for equal populations).  The exact threshold — for which
`α` is a random set of `αn` vertices of the cut polytope a face — is Problem O1.

### 4.3 Which pairs must be measured: adaptivity

A *design* is a set `H` of pairs; the `H`-data of an ensemble are its correlations on `H`.

**Theorem E12 (measurement complexity of pair data).**
(a) *Fixed designs.*  If the `H`-data determine the correlation of the pair `{i, j}` for
every ensemble with at most two conformers, then `{i, j} ∈ H`.  Hence a design chosen in
advance that identifies every two-conformer ensemble consists of **all** `n(n−1)/2` pairs.
(b) *Adaptive designs.*  For **every** ensemble on the cube, with correlation matrix of rank
`r`, pivoted Cholesky factorisation — read the column of a site whose residual variance is
positive, update, repeat — reads `rn − r(r+1)/2` pair correlations and determines all of
`C`; the conclusion needs no assumption on the ensemble, because the residual matrix is
positive semidefinite with zero diagonal.  `r` is at most the number of conformers.
(c) *Any certificate.*  Let `x¹, …, x^K` be independent uniform, `K = γn`, `γ ∈ (0, 1]` fixed.
There is `β(γ) > 0` such that, with probability tending to one, every design `H` that
admits a certificate `c + Σ_{H} Q_ij x_i x_j ≥ 0` with zero set `±S` has minimum degree at
least `β(γ)K`, hence at least `β(γ)Kn/2` pairs (`β(¼) ≥ 0.08`); for general
`C ln n ≤ K ≤ n`, `Ω(Kn/ln(en/K))` pairs.

**[P]**; (c) uses **[K]** Cover's count of linearly separable dichotomies.

*Proof.*  (a) Fix `s ∈ {±1}^{n−2}` on the other sites.  `μ_+` is uniform on
`(+,+,s), (−,−,s)` and `μ_−` on `(+,−,s), (−,+,s)` (sites `i, j` first).  Both have
`E x_i x_k = E x_j x_k = 0` and `E x_k x_l = s_k s_l` for `k, l ∉ {i, j}`, and
`E x_i x_j = ±1`.
(b) Let `d` be the residual diagonal (initially all ones) and `L` the factor found so far.
A pivot `p` with `d_p > 0` needs column `p` of `C`: `n − t` new entries at step `t`.  The
residual `C − LLᵀ` is a Schur complement of a positive semidefinite matrix, hence positive
semidefinite; when its diagonal vanishes it vanishes.  Each step lowers the rank by one.
(c) Write `f(x) = (terms without x_v) + x_v·⟨Q_v, x_{N(v)}⟩` with `N(v)` the
neighbourhood of `v` in `H`.  Each `x^a` minimises `f`, so flipping site `v` gives
`−2x^a_v⟨Q_v, x^a_{N(v)}⟩ ≥ 0`, with equality only if the flipped vector is again in `±S`.
With probability at least `1 − 2K²n2^{−n}` no two elements of `±S` are at Hamming distance
one; then the labels `−x^a_v` of the `K` points `x^a_{N(v)} ∈ ℝ^{N(v)}` are strictly linearly
separable through the origin.  `K` points in `ℝ^D` have at most `2Σ_{i<D} C(K−1, i)` such
dichotomies (Cover 1965; equality in general position), and for a fixed neighbourhood the
labels are uniform and independent of the points.  A union bound over the sites and over
the `C(n−1, D)` neighbourhoods of size `D = βK` gives a probability at most
`2n·exp(K[β ln(en/(βK)) + H(β) − ln 2])` (`H` the entropy in nats), which tends to zero when
the bracket is negative.  ∎

*Numerical check* **[N]** (C6): on `n = 60` sites pivoted Cholesky reads exactly
`rn − r(r+1)/2` entries (59, 117, 174, 285, 444 for 1, 2, 3, 5, 8 conformers, against 1 770
pairs) and reconstructs `C` to `10⁻¹⁵`; the two ensembles of (a) differ in one entry.

**Reading.**  For exact data the cost of *certified* identification from pair observables
is `Θ(Kn)` up to a logarithm — the number of parameters of `K` conformers — if the pairs may
be chosen adaptively, and `Θ(n²)` in the worst case if they may not.  The adaptive
procedure is not specific to finite ensembles: it is stopped by the data (a vanishing
residual diagonal), and for a "soft" ensemble with decaying spectrum the same question
becomes one of low-rank approximation from adaptively chosen columns (Problem O6).

---

## 5. What this says inside the programme

1. **One certificate, two readings.**  The inequality `d(x⋆, y) ≤ E(y) − E(x⋆)` certifies, for
   a known energy `E`, that `x⋆` is optimal whatever admissible residual is added (theory
   report Theorem 2.4) — and, for an energy `E = λ·Φ` in the span of measured observables,
   that averaged data pin every compatible ensemble to `x⋆` within `‖λ‖_*·τ` in transport
   cost (Theorem E2; machine-checked in both directions of use).  Certificates produced
   for equilibrium problems are identification certificates; the gap that the `(min,+)`
   kernel certifies is the stability constant (Proposition E1.1).
2. **Identified ensembles are the frustration-free ones.**  With no prior at all, what
   averaged data can determine is exactly the ensembles carried by the ground states of an
   energy in the span of the observables (Theorem E1).  Everything else is partially
   identified, and the science division's certificate formats
   (`INFERENCE_LIMITS.md` §8) are the tools for it.  Our results are the uniqueness side of
   its model-free format.
3. **Compatibility with the science division's Theorems 2 and 3.**  There, `k`-body data
   that look uniform bound every basin population by about `n^{−⌊k/2⌋}` and cannot exclude a
   mixture of that many basins.  Here, pair data resolve up to about `n` *point* conformers
   in typical position, and fail beyond `6.34n`.  The two statements meet: an identified
   `K`-conformer ensemble has correlation rank `K`, the uniform-looking datum `C = I` has
   rank `n`, and Proposition E9(b) is the smallest case of their code construction.
4. **Geometry enters through one matroid.**  For distance distributions, the ensemble-level
   question reduces to connectivity of the rigidity matroid (Theorem E5), which for
   globally rigid graphs is a theorem of 2022.  Any rigidity result of the Geometric
   Inference Division that controls the matroid of a measurement map — for torsion angles,
   for orientational restraints, for bodies and hinges — is an ensemble theorem by
   Corollary E6.

## 6. Verification status

| item | status |
|---|---|
| Lean | `proofs/Ensemble/Exposedness.lean`, `proofs/Ensemble/RenyiHeppes.lean`: seven headline theorems, two non-vacuity witnesses in `proofs/AxiomAudit.lean`; standard axioms only; no warning |
| numerics | `experiments/ensemble/run_all.py` runs the three scripts quoted above; output in `experiments/ensemble/output.txt` |
| review | internal adversarial review commissioned at this checkpoint; not yet applied.  No review by another division yet.  No external peer review |
| prior art | `PRIOR_ART.md`: eleven searches, four sources read in part through a fetch tool, the rest at the level of search summaries or from memory (marked) |

## 7. Corrections

None yet (first version).  Corrections will be listed here and in `DEAD_ENDS.md`, and sent
as linked messages.

## 8. Limitations

* **Exact data.**  Parts II and III are about exact data.  Part I has tolerances, but no
  statistical noise model; the minimax theory (modulus of continuity) is not written.
* **Point conformers.**  Finite ensembles are an idealisation.  At finite temperature every
  basin is a distribution; Proposition E8.1 shows that without a class nothing is
  identified from finitely many smooth observables.  Identification *inside* an envelope
  class or an exponential family with a remainder is not treated here.
* **Genericity.**  Theorems E5–E8 are for generic tuples of conformers.  Conformers that
  share rigid parts — the typical case in applications — have coincident edge lengths and
  are not generic; the relevant matroid is then a contraction (Problem O3).
* **No algorithm with a complexity guarantee.**  Certificates are exhibited; finding them
  (sign vectors in a subspace; the conformers behind `2K` moments per edge) is not
  analysed.  Verifying the gap of the certificate of Theorem E10 is a hard minimisation in
  general.
* **Asymptotics.**  Theorem E11 is asymptotic, and for equal populations only.
* **Sources.**  Odlyzko's theorem, the 3-neighbourliness of the cut polytope, Bai–Yin,
  Cover, Vitushkin–Henkin and Gortler–Healy–Thurston are cited without a full reading of
  the original texts (see `PRIOR_ART.md`).

## 9. Open problems and conjectures

* **O1 (the capacity of pair data).**  For which `α` is a random set of `αn` vertices of the
  cut polytope a simplicial face, with high probability?  Known now: yes for
  `α < 1` (E10(c)); no for `α > 6.338` with equal weights (E11).
* **O2 (`k`-body data).**  The same for all correlations of order at most `k = 2t`: is the
  capacity of order `n^t`?  (Certificate: the projector on the span of the lifted
  conformers; needed: an analogue of Odlyzko's theorem for tensor powers.)
* **O3 (conformers with common rigid parts).**  If the conformers agree on a set `J₀` of
  features and are generic otherwise, is the ensemble identified from the laws of the
  remaining features iff the contraction `𝓜/J₀` is connected (and the fibres are
  irreducible)?  For two rigid bodies joined by a hinge this is a statement about the
  inter-body edges.
* **O4 (quantitative ensemble rigidity).**  Define the *chimera gap* of a tuple as the least
  distance of a non-constant splice from the measurement variety.  Stability of Theorem E7
  when the edge-length laws are known up to a transport error `τ`, in terms of the chimera
  gap and the rigidity eigenvalues.
* **O5 (fewer moments).**  Theorem E8 uses `2K` moments per edge, `2K|E|` numbers, for
  `K(dN − d(d+1)/2) + K − 1` unknowns.  How many moments per edge suffice among ensembles
  with at most `K` conformers (generic identifiability of a secant variety)?
* **O6 (soft ensembles and adaptivity).**  For an ensemble whose correlation matrix has
  eigenvalues `λ_1 ≥ λ_2 ≥ …`, how many adaptively chosen pair correlations determine `C` to
  a prescribed accuracy, and what do they certify about other observables?
* **O7 (finite temperature).**  Which members of an envelope class are identified inside
  the class by `k`-body data?  (The class is a polytope in the weights; the identified
  members are exposed points relative to the observable span.)  Is there a general
  relation between "hard for evaluations" and "easy for ensemble data"?
* **C1 (conjecture; the obstruction for densities).**  Under the hypotheses of E8.1 with
  smooth `q_i`, every probability measure with a continuous positive density on `D` shares
  the laws of all `q_i` with a different one of the form `(1 + εg)μ`, `g` bounded.
  *Strategy:* the operator `g ↦ (E_μ[g | q_i])_i` composed with its adjoint is the identity
  plus integral operators that are compact for pairwise transversal foliations, so the
  range of the adjoint is closed; if the kernel were trivial the operator would be bounded
  below, which high-frequency wave packets transversal to all the foliations contradict.
* **O8 (noise).**  The minimax risk of a linear target over a convex class of ensembles
  under Gaussian noise is, up to a constant, a modulus of continuity (Donoho 1994).
  Compute it for the classes of this report; decide what adaptivity gains under noise.
