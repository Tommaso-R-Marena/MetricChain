# Ensemble report — what an ensemble is determined by

**Ensemble Identifiability and Certified Inference Division.**  Branch
`research/ensemble-identifiability`.  Version 3 (third checkpoint, 2026-11-26: Part VI added;
version 2 was the second checkpoint, commit `1a067b5`; version 1 the first, commit `a570520`;
§7 lists what changed).

Labels: **[V]** machine-checked in Lean 4 + Mathlib (declaration named; axioms `propext`,
`Classical.choice`, `Quot.sound` only) · **[P]** paper proof given here · **[K]** known, cited
(the prior-art register `PRIOR_ART.md` says how each source was read) · **[N]** numerical
evidence only (script named) · **[C]** conjecture.  Review status: Parts I–III (version 1)
have had one internal adversarial review by a subagent of this division
(`reviews/ER1_internal_review.md`; an AI review, not academic peer review), whose findings
are applied here (§7); the science division has contributed one proposition and has a
review of Part II in progress; Parts IV and V are under a second internal review that has
not yet reported; Part VI has been read by nobody but its author.
"New" below always means "not found in the search documented in `PRIOR_ART.md`".

---

## 0. Summary

An unknown probability measure `μ` (an *ensemble*) on a configuration space `X` is seen
through means of observables, `y_i = ∫ φ_i dμ + ε_i`.  This report answers, for several kinds
of data, the first question of that model: **which ensembles are determined by the data,
how stably, and with what certificate.**

| # | statement | label | novelty class |
|---|---|---|---|
| E1 | `μ` is determined by the means of `Φ` among *all* ensembles iff its support is exactly the zero set of a non-negative function in `span{1, Φ}` and the features are affinely independent on it (finite `X`; for compact `X`: iff the preimage of the minimal face of the moment body through the data is a finite set with affinely independent features).  A certificate bounds the mass off the support linearly in the data error.  On continua an identified ensemble can be only Hölder-stable (example with exponent `½`) | P; sufficiency and the mass bound V (`eq_of_exposing_certificate`, `mass_off_support_le`) | known in substance (uniqueness of representing measures; dual certificates of sparse recovery); formulation |
| E2 | **One conformation.**  `ω(τ) = sup{E_ν ρ : ‖E_νΦ − Φ(x⋆)‖ ≤ τ}` equals `min_λ {τ‖λ‖_* + max_y[ρ(y) − λ·(Φ(y) − Φ(x⋆))]}`; the best linear modulus is `κ = min{‖λ‖_* : λ·(Φ(y) − Φ(x⋆)) ≥ ρ(y) ∀y}`.  For `ρ = d(x⋆,·)` the constraint is the **sharp-minimum condition of theory report Theorem 2.4**: *a certificate that `x⋆` minimises `λ·Φ + g` for every admissible residual is a certificate that the data of `Φ` identify the conformation `x⋆`, with transport modulus `‖λ‖_*·τ`* | P (duality, exactness of `κ`); the inequality and the bridge V for finite `X`, in the form `Σ_i |λ_i|·|Δdata_i|` (`transport_le_of_sharp`, `identification_of_robust_certificate`, `residual_advantage_le`) | formulation (linear-programming duality; the dictionary with robust optimality, two lines given Theorem 2.4, was not found in print) |
| E3 | **Finite ensembles, first order.**  For an identified `μ` on a finite metric space, `sup{W₁(ν, μ) : ‖E_νΦ − E_μΦ‖ ≤ τ} = κ_μ·τ` exactly for small `τ`, with `κ_μ = max_{g 1-Lipschitz} min{‖λ‖_* : c + λ·Φ ≥ g on X, = g on supp μ}`; `κ_μ` depends on the support only, not on the weights | P | formulation (`1/κ_μ` is a minimum conic gain on a tangent cone / a Hoffman constant; ER1 F11) |
| E4 | **Rényi–Heppes for arbitrary observables.**  If two configurations agree on fewer than `r` of `m` features and `m ≥ K(r−1) + 1`, every ensemble with at most `K` conformers is determined by the `m` *laws* of the features among all ensembles; the bound is sharp for every `K ≥ 2`, `r ≥ 2` | V for finite `X` (`renyi_heppes`), P in general | generalisation of a known theorem (Rényi 1952, Heppes 1956); the support step is the frameproof-code lemma of Boneh–Shaw 1998 |
| E5 | **Splices on a variety.**  For a polynomial feature map `F : ℝ^D → ℝ^m` without constant coordinates: for generic `K`-tuples no vector assembled coordinate-wise from the feature vectors of *different* points lies on the feature variety — for every `K` — **iff the algebraic matroid of the coordinates of `F` is connected**; if it is not, splices are realisable on an open set of pairs | P | new (not found); closest: unlabeled PCA (linear, unknown subspace) and the product lemma of Garamvölgyi–Gortler–Jordán |
| E6–E8 | **Distributional ensemble rigidity.**  For a graph on at least `d+2` vertices the following are equivalent: `G` is generically globally rigid in `ℝ^d`; every generic finite ensemble of frameworks, *with any number of conformers*, is determined modulo congruence, among all ensembles, by the laws of its edge lengths.  Then `2K` moments of each squared edge length suffice for `K` conformers — `2K|E|` scalar means — with the explicit certificate `Σ_e Π_i (ℓ_e² − ℓ_e(x_i)²)²`.  Mean squared distances alone determine no ensemble at all | P, given two cited theorems (global rigidity is generic; globally rigid ⇒ connected rigidity matroid, 2022) | new (not found) |
| E7′ | **Conformers that share rigid parts, smallest case.**  Two rigid bodies joined by `m` generic legs: for generic attachment points and poses the leg-length laws determine every finite ensemble of relative poses when `m ≥ dim SE(d) + 1` (seven in space, four in the plane), and fail to on an open set when `2 ≤ m ≤ dim SE(d)` — one leg more than rigidity | P, given a K fact on generic lines | new (not found) |
| E9 | Pair correlations on `{±1}ⁿ`: every ensemble with at most three conformers is determined (explicit certificate, §4c.1); four conformers need not be (explicit) | P (also K: the cut polytope is 3-neighbourly); the example N/P | known; the certificate proof is ours |
| E10 | **Typical supports.**  For `K ≤ n − 10n/ln n` independent uniform conformers, with probability `1 − O(K³(¾)ⁿ + K²2^{−n})` *every* ensemble supported on them is determined by its pair correlations among all ensembles, with the explicit certificate `‖P^⊥x‖²` | P given K (Odlyzko 1988); self-contained proof for `K < 0.2933 n` | synthesis |
| E11 | For `K ≥ (2+ε)n` random conformers, with high probability **no** ensemble supported on all of them is determined by pair correlations (any weights); for `K/n → α > 6.338` the pair correlations of every ensemble with positive weights on them are those of a full-support ensemble (explicit for equal weights) | P given K (Cover; Bai–Yin, Sheppard) | (a) synthesis: the classical capacity bound of pair-interaction associative memories read through E1; (b) not found, elementary |
| E12 | **Adaptivity.**  A fixed set of pairs that determines every two-conformer ensemble must contain *all* `n(n−1)/2` pairs; adaptively, `rn − r(r+1)/2` pair correlations determine the whole correlation matrix of any ensemble of correlation rank `r ≤ K` (certified, no assumption); for typical supports every certificate needs `Ω(Kn/ln(en/K))` pairs | P; K (Cover's counting) | formulation / synthesis |
| E13 | **Inside a first-order class** (a polytope in the normalised weights): a member is extreme iff its tight graph is connected; it is determined by data *among the members* iff a face exposed by an observable in the span contains it and carries injective data; exact flow certificates | P | formulation (polyhedral geometry; the flow format is the science division's) |
| E15 | **A thermal union bound.**  For a product reference and a symmetric site-additive envelope, any alphabets, heterogeneous sites: `TV(μ, μ*_a) ≤ Σ_i [1 − μ(x_i = a_i)/μ*_{a,i}(a_i)]` for every member `μ`, `μ*_a` the member most polarised towards `a`; for binary sites `TV(μ, μ*_a) ≤ Σ_i [μ*_{a,i}(a_i) − μ(x_i = a_i)]`, with equality cases — dimension-free, constant one.  On the cube a member is identified by one-body data inside the class iff at most one marginal is unsaturated | P | new (not found) |
| E15T | **The same with an interacting known part.**  The thermal union bound holds with the same constant for *every* reference that is log-supermodular in the disagreement variables — any Ising-type known part, on any graph and of any range, all of whose bonds are satisfied by the centre; if the centre violates a bond the bound is false (exact counterexamples on chains).  Frustration is the obstruction | P given K (FKG; marginals of log-supermodular measures); the obstruction N | new (not found) |
| E16 | **A bimodal ensemble identified by one pair observable.**  For even `n` the double cone `∝ exp((b/2)|M_a|)` is the unique maximiser of `E[M_a²]` over the cube class; for odd `n` the maximisers are a segment parametrised by the population difference of the two basins | P | new (not found); elementary |
| E17 | **Noise.**  For a convex class and Gaussian noise `σ` the minimax root-mean-square error of a mean `E_μψ` is between `0.199·ω(2σ)` and `0.5·ω(2σ)`, with `ω(ε) = min_λ{ε‖λ‖₂ + range over the class of ψ − λ·Φ}`: the dual certificate of the identified interval is the near-minimax linear estimator | P (elementary); K (Donoho 1994: factor 1.25) | formulation of a known theory |
| E18 | **Lifted certificates.**  For a lift `v` with the entries of `vv^*` in the span of the data, `‖P^⊥v(x)‖²` is a non-negative function in the span; if its zero set is finite with linearly independent `v(x)v(x)^*`, every ensemble on the conformers is determined among all ensembles — also when the zero set is larger than the support.  Three conformers on the cube: a self-contained proof of E9(a).  **With a prior on the number of atoms** (finite `X`): flat-isolated supports are determined among ensembles with at most `K` atoms for all weights outside a null set (E18′) | P | elementary; formulation (flat extensions, E10 and the geometry division's certificate are instances) |
| E19 | **Data of even order `≤ 2d` on the cube.**  `K ≤ (1−ε)n^d/d!` random conformers are the ground states of the explicit energy `‖P^⊥ξ_d(x)‖²` and every ensemble on them is determined among all ensembles; pair data determine up to `(1−ε)n²/2` conformers among ensembles **with at most `K` conformers** (generic weights) but nothing beyond `2n` among all; without a prior nothing is determined beyond `(2+ε)·n^{2d−1}/(2d−1)!`; for four-body data the threshold is numerically 2.6–3.5 times the sum-of-squares range, about that of a Gaussian cloud of the same size | (a) K (Baldi–Vershynin 2019), which we re-derived before finding it; (b)–(d) P given K; (e) N | synthesis; the probabilistic core is a published theorem (rediscovery on our side) |
| E20 | **Generic conformers on a variety; torsion angles.**  For a lift into `ℂ^N` whose image has projective codimension `c`, generic ensembles of `K ≤ c` conformers are determined among all ensembles; on the torus `𝕋^r` with multilinear trigonometric data: `K ≤ 2^r − r − 1`.  **Two states on a torus** are determined iff they differ in at least two angles, with an explicit product certificate using pairs of angles only (E20′) | P given K (generalised trisecant lemma); E20′ P, its combinatorial core V (`twoStateCert_eq_zero_iff`) | synthesis; E20′ elementary (not searched) |

The thread through the report is one sentence, stated with its two conditions: **on a
finite configuration space an ensemble is determined by a family of observables exactly
when its support is the *whole* zero set of a non-negative function in their span and the
features are affinely independent on it; the stability of the identification is the
sharpness of that exposure; and the certificates are objects that the programme's kernels
already check** — minima of energies in the span.  On a compact space the zero set is
replaced by the minimal face of the moment body, reached by iterated exposure, and the
stability is linear only in the exposed case (Example E1.2, Proposition E2.2).  (Version 1
stated the sentence without the two conditions; the internal review ER1 showed it false in
both directions as written — §7.)

Parts IV and V (added at the second checkpoint) carry the same sentence to finite
temperature — inside a first-order class the identified ensembles are the exposed members
of a polytope, with a dimension-free "thermal union bound" for the most polarised member —
and to noise, where the dual certificate is a near-minimax estimator.

What is *not* in this report: anything about real instruments; algorithms with complexity
guarantees; identification inside classes other than first-order ones.  §8 lists the
limitations, §9 the open problems.

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
`W₁(ν_t, δ₀) = p·t + (1 − p) ≈ 2t ≈ 2√(2τ)`.  The exponent `½` is exact: with errors in
`ℓ^∞`, `1 − cos t ≥ (4/π²)t²` gives `∫_{t>0} t² dν ≤ π²τ/4`, hence `∫_{t>0} t dν ≤ (π/2)√τ`, and
the second datum gives `∫_{t≤0} |t| dν ≤ τ + ∫_{t>0} sin t dν`; so `ω(τ) ≤ τ + π√τ` (ER1 F9).
On a finite `X` this cannot happen: every identified ensemble has a certificate, hence a
linear modulus (E1.1).

**Corollary E1.3 (observables that are quadratic in the coordinates) [P].**
(a) On `ℝ^D`, an ensemble with finite second moments is determined by its first and second
moments among such ensembles iff it is a conformation.  (b) Let `G` be any graph on `N`
points in `ℝ^d` — the complete graph included — and let the configuration space be all of
`(ℝ^d)^N`, with no statewise constraint.  No ensemble of frameworks with a
non-degenerate conformer is determined modulo congruence by its mean squared edge lengths:
if `μ` does not give probability one to "all edges have length zero", and `R ≥ 0` is
independent of the configuration `p` with `R² ∈ {0, 2}` with probability `½` each, then the
law `ν` of `R·p` has the same mean squared length of every pair and is not congruent to `μ`.

*Proof.*  (a) "If": the covariance vanishes.  "Only if": with covariance `Σ ≠ 0` the
Gaussian law with the same mean and covariance, or — if `μ` is that Gaussian — any other law
with them, is a second ensemble.  (b) `E|Rp_u − Rp_v|² = E R²·E|p_u − p_v|²`.  With
`Q = Σ_{uv}|p_u − p_v|²`, `P_ν(Q = 0) = ½ + ½P_μ(Q = 0) > P_μ(Q = 0)` unless `P_μ(Q = 0) = 1`,
and `Q` is invariant under congruence.  ∎

("Modulo congruence" means equality of the push-forwards to `(ℝ^d)^N/E(d)`.  The one
exception is in the statement: the ensemble with all edge lengths zero almost surely,
which for a connected graph *is* determined.  The twin above contains the collapsed
framework; if degenerate frameworks are to be excluded take `R² ∈ {½, 3/2}` instead, which
changes `E Q²` by the factor `1.25` and needs `0 < E_μ Q² < ∞`.  ER1 F8.)

Mean squared distances carry the mean *Gram* structure and nothing about fluctuations;
they cannot even certify that the ensemble is a single conformation.  This is a statement
about *unconstrained* configurations.  The Geometric Inference Division reached the same
obstruction independently (every structure has the mean squared distances of a mixture of
collinear ones; its `ENSEMBLE_RIGIDITY.md`, Proposition 3.1) and showed what removes it:
if every state obeys the same bond constraints — the ensemble lives on the configuration
space of a chain, not on `(ℝ^d)^N` — mean squared distances do determine mixtures, from an
exactly known chain length on (its Theorems B and C; two generic states from ten atoms
on, its Theorem I).  The qualifier "no statewise constraint" in (b) was asked for by that
division (GEOMETRY-RES-0001 §0) and is accepted: the random rescaling of the proof leaves
a constrained configuration space.  That division now calls determination of a
conformation by the means of the squared lengths *second-moment rigidity*; it lies
between global and universal rigidity, whereas determination by the laws (Theorem E7) is
global rigidity.  In the language of Theorem E1 the
constraints shrink the configuration space until the zero set of a non-negative quadratic
form, an affine subspace of `(ℝ^d)^N`, meets it in finitely many points.  The first data that
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
(c) *The bridge.*  Let `d` be an envelope with `d(x⋆, ·)` continuous (automatic on a finite
`X`) and `ρ = d(x⋆, ·)`; "identifies the conformation" below presupposes `d(x⋆, y) > 0` for
`y ≠ x⋆`, otherwise the conclusion is identification modulo `{d(x⋆, ·) = 0}`.  The constraint in `κ` reads

    d(x⋆, y) ≤ E_λ(y) − E_λ(x⋆)        for all y,

which is the sharp-minimum condition of theory report Theorem 2.4.  Hence, by that theorem:
**`κ < ∞` iff some energy `E_λ` in the span of the observables has `x⋆` as its minimiser for
every admissible residual `g` (`x⋆ ∈ argmin(E_λ + g)` for all `g` with `g(x) − g(y) ≤ d(x,y)`),
and `κ` is the least dual norm of such an energy.**  For every ensemble `ν` and every
admissible `g`:

    E_ν g  ≥  g(x⋆) − ∫ d(x⋆, y) dν(y)  ≥  g(x⋆) − κ·‖Aν − Φ(x⋆)‖ .

**[P]** for (a), (b); in (c) the two inequalities and the passage through Theorem 2.4 are
**[V]** for finite `X` and with the pairing `Σ_i |λ_i|·|Δdata_i|` (which gives `‖λ‖_*‖Δ‖` for
every absolute norm, the `ℓ^p` norms included; for a general norm the proof is the same
line, on paper): `Ensemble.transport_le_of_sharp` (with a modulus `s`),
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

**Proposition E2.2 (on a continuum the modulus is a square root and the certificate is a
curvature) [P; (a) and the reading are the science division's: SCI-RES-0026 §2(c),
SCI-RES-0028 §2(b)].**  Let `X` contain an open subset of a Riemannian manifold around `x⋆`,
`d` the geodesic distance, and `Φ` of class `C¹` near `x⋆`.
(a) No energy in the span satisfies the sharp-minimum inequality at `x⋆`: the constant `κ`
of Theorem E2 for `ρ = d(x⋆, ·)` is `+∞`, **whatever the observables and however many**.  If
`Φ` is `C²`, then `ω(τ) ≥ c√τ` for small `τ`.
(b) Theorem E2 with `ρ = d(x⋆, ·)²` gives the statement that survives:
`κ₂ = min{‖λ‖_* : E_λ(y) − E_λ(x⋆) ≥ d(x⋆, y)² for all y}` is the best constant in
`∫ d(x⋆, y)² dν(y) ≤ κ₂·‖Aν − Φ(x⋆)‖`, so that `W₁(ν, δ_{x⋆}) ≤ W₂(ν, δ_{x⋆}) ≤ √(κ₂ τ)`.

*Proof.*  (a) The inequality forces `x⋆` to minimise the `C¹` function `E_λ`, so its
differential vanishes there and `E_λ(y) − E_λ(x⋆) = o(d(x⋆, y))`.  For `C²` observables the
ensemble `½δ_{y₊} + ½δ_{y₋}`, `y_± = exp_{x⋆}(±tv)`, has data within `Ct²` of `Φ(x⋆)` (the
first-order terms cancel) and transport cost `t|v|`.  (b) is Theorem E2(b).  ∎

So Example E1.2 is the rule, not an exception: on a finite configuration space
identification of a conformation is Lipschitz in the data and certified by a *gap*; on a
continuous one it is Hölder of exponent `½` and certified by *quadratic growth* of an energy
in the span — a certified lower bound on a curvature near `x⋆` together with a gap away
from it.  The Geometric Inference Division's bound `W₂(ν, μ)² ≤ C‖M(ν) − M(μ)‖` for mean
squared distances (its GEOMETRY-MSG-0002, item 6, with the same remark on the exponent) is
an instance with a finite ensemble in place of `δ_{x⋆}`.

*Remark E2.3 (uncertain measurement operators are a tolerance) [P, immediate].*  If the true
observables `Φ̃` are known only through a model `Φ` with `sup_x ‖Φ̃(x) − Φ(x)‖ ≤ η`, then
`‖∫Φ̃ dν − ∫Φ dν‖ ≤ η` for every ensemble, so every statement of this part holds for data
generated by `Φ̃` with `τ` replaced by `τ + η`, the certificates being computed for the model
`Φ`.  The error of the forward model enters through its supremum over the configuration
space, not through its typical size: a certificate cannot use that the ensemble avoids
the configurations where the model of the measurement is poor, because it does not know
the ensemble.

### 2.3 Finite ensembles: the first-order constant

Let `X` be finite with a metric `d`, `μ` identified with support `S`, and

    ω_μ(τ) = sup{ W₁(ν, μ) : ν ∈ P(X), ‖Aν − Aμ‖ ≤ τ } .

**Theorem E3 (the first-order identification constant).**  Let
`T₁ = {h ∈ ℝ^X : Σ h = 0, h ≥ 0 off S, ‖Ah‖ ≤ 1}` (compact, because `μ` is identified) and

    κ_μ = max_{h ∈ T₁} ‖h‖_KR .

(a) `ω_μ(τ) ≤ κ_μ τ` for all `τ ≥ 0`, with equality for
`τ ≤ τ₀ = min_{x∈S} μ(x) / max_{h∈T₁} ‖h‖_∞` (`τ₀ = ∞` if `T₁ = {0}`).
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

(In the vocabulary of convex recovery `1/κ_μ` is the *minimum conic gain* of the data map
on the tangent cone of the simplex at `μ`, equivalently a Hoffman constant of a polyhedral
system; that it depends on the active set only is standard there — Chandrasekaran, Recht,
Parrilo and Willsky 2012, cited from memory by the review ER1 F11.  The theorem is a
formulation in the transport norm, not a new principle.)

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
`K + 1` distinct lines; Heppes (1956): in `ℝ^d`, by its projections on `K + 1` subspaces any
two of which determine the point **[K; as quoted by Fraiman–Moreno–Ransford 2022, the
transversality condition from the review's memory]**.  The proof uses that one property of
the projections and nothing else.

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

*A neighbour in coding theory (pointed out by the review ER1).*  The support step is the
standard lemma on *frameproof codes*: a code of length `ℓ` and minimum distance
`d > ℓ − ℓ/c` is `c`-frameproof — no coalition of `c` codewords can produce, coordinate by
coordinate from its own symbols, another codeword (Boneh–Shaw 1998; Staddon–Stinson–Wei
2001; **[K, from the review's search]**).  With `d = m − r + 1` and `c = K` this is exactly
`m > K(r − 1)`.  A splice is a *descendant* of a coalition, and "no chimera" is
*frameproof*.  The statement about weights and arbitrary measures is, as far as the review
and we know, not in that literature.

For frameworks the theorem gives nothing: modulo congruence there are always (non-generic)
pairs of non-congruent configurations that agree on *every* edge, so the edge lengths are
not `r`-determining for any `r ≤ |E|`.  Worst-case counting is the wrong tool there; the
next theorem — in the vocabulary above: generic point sets of a variety with a connected
algebraic matroid are frameproof for every coalition size — is the right one.

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
ranks.  By the constant-rank theorem there are neighbourhoods `U₁`, `U₂` of `x₀` that `F_J`,
`F_{J^c}` map onto embedded submanifolds `N_J`, `N_{J^c}` of dimensions `r(J)`, `r(J^c)`, and a
neighbourhood `U ⊆ U₁ ∩ U₂` that `F` maps onto an embedded submanifold `N` of dimension
`r([m])`.  Then `N ⊆ N_J × N_{J^c}`, a manifold of the same dimension, so `N` is open in it;
and `(x, x') ↦ (F_J(x), F_{J^c}(x'))` is continuous with value `F(x₀) ∈ N` at `(x₀, x₀)`, so it
takes values in `N = F(U)` for all `x, x'` near `x₀`.  ∎

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

So for marginal laws: **no chimera ⇒ identified** (at the level of feature vectors), and
for generic tuples the absence of splices on the variety is the connectivity of the
algebraic matroid (Theorem E5); injectivity of `F` on single configurations is a separate
question about one conformation at a time.
*The converse is false* (review ER1, F2, with both examples).  A chimera breaks
identification only if chimeras can be combined into a non-negative table with the right
one-dimensional marginals — for instance two complementary ones, as in E5(b).  The exact
criterion, when the conformers have distinct values of every feature: `μ` is identified at
the level of feature vectors iff the only `v ≥ 0` on the realisable colourings whose
marginal on every feature is `(w_i)` is the diagonal one.
*Example 1:* three configurations with two features, `F(x₁) = (0,0)`, `F(x₂) = (1,1)`,
`F(y) = (0,1)`: `y` is a chimera, yet every `ν` with the laws of `w₁δ_{x₁} + w₂δ_{x₂}` has
`ν(x₂) = w₂` (first feature) and `ν(x₂) + ν(y) = w₂` (second), so `ν(y) = 0`.  *Example 2*
(frameworks, an open set of pairs): `K₄` plus a vertex joined to two of its vertices `0, 1`,
in the plane, the first conformer with `|x₀x₁| = 2` and pendant lengths `(1.5, 1.5)`, the
second with `|x₀x₁| = 5` and pendant lengths `(3, 2.5)`.  The three chimeras that carry the
`K₄` of the first conformer and at least one pendant length of the second are realisable
(the two circles meet); no splice carrying the `K₄` of the second conformer and a pendant
length of the first is (`1.5 + 1.5`, `1.5 + 2.5`, `3 + 1.5 < 5`), and no mixed `K₄` is.  The
law of the `K₄` block gives mass `w₂` to the second conformer, and the laws of the two
pendant edges then force zero mass on the three chimeras: identified, for all weights, on
an open set of pairs (check R7).  So for a disconnected matroid identification fails on a
non-empty open set of pairs (E5(b)) and can hold on another.

*Remark (rational feature maps; other parameter spaces).*  Theorem E5 and Corollary E6 hold,
with the same proofs, for a *rational* map `F : ℝ^D ⇢ ℝ^m` defined off a proper algebraic
subset, tuples being taken in its domain: the closure of the image is still irreducible of
dimension the generic rank of the Jacobian, and the splice maps are rational.  This covers
every parameter space with a rational parametrisation: tori of torsion angles in half-angle
coordinates (the rational atlas of the circle of theory report §5), rotation groups
(Cayley transform), and products of these — in particular the relative poses of rigid
bodies (Theorem E7′ below).

### 3.3 Distributional ensemble rigidity

*Terminology.*  The Geometric Inference Division uses "ensemble rigidity" for a property of
one conformation under *mean* squared-distance data with statewise constraints (no
ensemble of other conformations reproduces its averaged data).  The property of this
section is about *laws* of edge lengths and about finite ensembles; to keep the two apart
we call it distributional ensemble rigidity.

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

**Theorem E7 (distributional ensemble rigidity = global rigidity).**  Let `N ≥ d + 2`.  The following are
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
edge-length laws.  Genericity matters as well, and the exceptional set is not only "shared
lengths": on the line, the 4-cycle with conformers `x = (8, 0, 3, 5)` and `x' = (8, 3, 5, 0)`
has edge lengths `(8, 3, 2, 3)` and `(5, 2, 5, 8)`, both splices `(8, 2, 2, 8)` and `(5, 3, 5, 3)`
close up, and the two chimeras form a twin ensemble (found by the review ER1, F14:
conformers related by arithmetic coincidences; check R8).

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
and has the same moments of orders `0, …, K − 1`, hence the same weights (Vandermonde; that
a measure with `K` atoms on the line is the only non-negative measure with its moments up
to order `2K` is classical — Gauss quadrature, Karlin–Studden).  So
all edge-length laws agree and Theorem E7 applies.  The zero set of `f` is the set of
configurations all of whose squared edge lengths occur among the conformers', which by
E5(a) and global rigidity is `∪_i [x_i]`.  ∎

The certificate ties Parts I and II together: the function "sum over features of the
product of squared deviations from the conformers' values" is non-negative, lies in the
span, and its zero set is the set of all realisable splices; when that set contains
nothing but the conformers — as it does for a connected matroid and generic tuples — it is
an exposing function and the ensemble is identified.  (When realisable chimeras exist the
ensemble may still be identified, by a different exposing function: Example 2 of §3.2.
Version 1 said "exactly when"; ER1 F2.)  By Corollary E1.3,
`j = 1` alone (mean squared lengths) identifies nothing; `j ≤ 2` certifies a single
conformation (`E ℓ⁴ = (E ℓ²)²` forces every measured length to be constant); `j ≤ 2K` resolves
`K` conformers.

**Theorem E7′ (conformers that differ by a rigid-body motion: a platform with `m` legs).**
Generic tuples exclude the most common situation: conformers that share rigid parts.  The
smallest case is two rigid bodies.  Let `d ∈ {2, 3}`, `D_d = d(d+1)/2` the dimension of the
group `SE(d)` of proper rigid motions; the first body carries points `u_1, …, u_m`, the
second `v_1, …, v_m`, and a relative pose `g ∈ SE(d)` has *leg lengths* `ℓ_e(g) = |u_e − g·v_e|`.
For generic attachment points:
(a) the algebraic matroid of `(ℓ_e²)_{e≤m}` on `SE(d)` is the uniform matroid of rank
`min(m, D_d)`; for `m ≥ 2` it is connected iff `m ≥ D_d + 1`;
(b) if `m ≥ D_d + 1` (seven legs in space, four in the plane): for generic `K`-tuples of poses
and all weights, every Borel probability measure on `SE(d)` with the `m` leg-length laws of
`μ = Σ_i w_i δ_{g_i}` equals `μ` — for every `K`;
(c) if `2 ≤ m ≤ D_d` there is an open set of pairs of poses whose two-conformer ensembles
are not determined by the leg-length laws (for `m = 1` not even one pose is determined).

**[P]**, given **[K]**: the line vectors of generic lines are in general linear position
(any `D_d` of them are independent).

*Proof.*  (a) The differential of `ℓ_e²` at `g` along a twist is the pairing of the twist with
the line through `u_e` and `g·v_e`, so the Jacobian has the line (Plücker) vectors of the
legs as rows; for generic attachment points and pose the legs are `m` generic lines, any
`D_d` of their vectors are independent, and a uniform matroid `U_{r,m}` with `0 < r < m` is
connected.  (b) By the remark after Corollary E6 (`SE(d)` has a rational parametrisation)
the feature-space ensemble is determined; it remains to see that, for generic attachment
points, a generic pose is the only pose with its `m` leg lengths.  Let `B` be the set of
pairs (attachment points, pose `g`) for which some pose `g' ≠ g` has the same `m` leg
lengths; it is semialgebraic.  For generic first `D_d` legs and generic `g`, these legs have
a Jacobian of full rank at `g`, so the fibre through `g` is finite; for each of its other
points `g'`, the attachment points `(u, v)` of a further leg with `|u − g v| = |u − g' v|` form
a proper algebraic subset (take `v` with `gv ≠ g'v` and `u = gv`).  So the fibres of `B` over
generic (first `D_d` legs, pose) have positive codimension, hence so has `B`, hence for
attachment points outside a proper algebraic subset the poses `g` with (points, `g`) `∈ B`
form a set of positive codimension in `SE(d)`.  (The review ER1 pointed out that version 2
exchanged the two quantifiers without this argument.)
(c) For `2 ≤ m ≤ D_d` the matroid is free on at least two elements, hence disconnected, and
E5(b) applies.  ∎

Six legs determine finitely many poses of a parallel platform; a seventh leg generically
determines the pose (this is the generic global rigidity of body–bar frameworks:
redundant rigidity; Connelly–Jordán–Whiteley 2013 **[K]**).  The theorem says that the same
seventh leg makes the *distributions* of the leg lengths determine a generic finite
ensemble of poses, with any number of conformers.  For more than two bodies the criterion
is the connectivity of the body–bar matroid (Problem O3).  *Numerical check* **[N]**
(`experiments/ensemble/platform_checks.py`): rank and connectivity of the leg matroid for
`d = 2` (`m = 3, 4, 5`) and `d = 3` (`m = 6, 7, 8`); no splice of two random poses is realised
with four or five legs in the plane (264 splices, least-squares residual at least `1.9·10⁻³`
against `10⁻¹⁴` at a pose) or seven legs in space (80 splices, at least `2.4·10⁻³`); with
three, respectively six, legs the splices of nearby poses are realised in 20 of 20 cases.

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
agreements, 31 realised).  R5: all 203 zeros of the certificate `f` found from 400 starts
(100 near each conformer, 200 random) for `K₄` with two conformers have the edge lengths of
one of the conformers (63 and 140).  R7: the example of §3.2 with realisable chimeras and
20 perturbations of it — the realisable splices are the two conformers and three chimeras
in all 21 pairs (smallest Cayley–Menger determinant of a mixed block `5.9`, against `10⁻¹³`
at a conformer; chimeras realised to `4·10⁻¹⁵`), and the largest chimera mass compatible
with the eight laws is zero.  R8: the 4-cycle on the line.  (Version 1 quoted "22 zeros"
for R5, a number the script did not print; ER1 F6.)

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

**Proposition E9 [P; also K].**  (a) Every ensemble with at most three conformers
is determined by its pair correlations among all ensembles.  (b) Four conformers need not
be: on `n = 4` sites the uniform ensemble on `(+,+,+,+)`, `(+,−,−,+)`, `(+,−,+,−)`, `(+,+,−,−)`
has `C = I`, the pair correlations of the uniform ensemble on the cube.

(a) is proved in §4c.1 (Remark 1 to Theorem E18), with the explicit certificate `‖P^⊥x‖²`:
the sign vectors in the span of three conformers are the conformers and at most one more
vertex.  It is also the theorem that the cut polytope is 3-neighbourly (stated, as best
possible, in Ziegler's *Lectures on 0/1-polytopes* for the correlation polytope
`COR(n) ≅ CUT(n+1)`; Deza–Laurent, *Geometry of Cuts and Metrics*; neither read in the
original) together with Theorem E1; our proof does not use the citation.  (b): the four vectors are the rows of a
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
(c) **[K + two lines]** for `3 ≤ K ≤ n − 10n/ln n`, `P(𝓔^c) = (1 + o(1))·4·C(K,3)·(¾)ⁿ`; for
`K = 2`, `P(𝓔^c) = 2^{1−n}`, and for `K = 1` the event `𝓔` is certain.

**[P]** for (a), (b).  (c): Odlyzko's theorem (1988; read as restated by Irmatov 2024,
Theorem 1.1 — the original was not obtained) says that for `p ≤ n − 10n/ln n` the
probability that the span of `p` random sign vectors contains a sign vector other than `±`
the given ones is `4C(p,3)(¾)ⁿ + O(p⁴(5/8)ⁿ) + O((7/10)ⁿ)`.  The event `𝓔^c` also contains linear
dependence, which is not in that event.  The two lines that were missing (review ER1,
F5): let `j` be the first index with `x^j` in the span of the earlier conformers; either
`x^j = ±x^i` for some `i < j` (total probability at most `K²2^{−n}`), or `x^j` is one of the at
most `2^{j−1}` other sign vectors of that span, which has probability at most
`2^{j−1−n}·P(the span has such a vector) ≤ 2^{−10n/ln n}·O(K³(¾)ⁿ)`.  Summed over `j` this is
`o(K³(¾)ⁿ)`, and so is `K²2^{−n}`.  The leading term is confirmed by our enumeration, below.

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

*Relation to the Geometric Inference Division's Theorem B.*  The cube is a configuration
space with statewise constraints `x_i² = 1`, pair correlations are second moments, and
`‖P^⊥x‖²` is the cube's form of that division's certificate `‖Π^⊥X‖²` for mean squared
distances of chains with fixed bond lengths: a positive semidefinite form that vanishes on
the stacked conformers.  There the form certifies up to about `(2/3)√n` states (its
Theorem C) and identifiability appears numerically up to about `2n/9` states (its
GEOMETRY-MSG-0002, item 10); here it certifies up to almost `n`
conformers and identifiability extends beyond `n` (§4.4) — in both cases the range between
the two is where the exposing function is non-negative on the constrained space without
being a positive semidefinite form plus multipliers of the constraints.

**Reading.**  A typical set of up to almost `n` conformers is *exactly* the set of ground
states of an explicit pairwise energy — the storage problem of associative memories with
zero error, which is where Odlyzko's question came from; `f` is the energy of the
*projection rule* (Personnaz–Guyon–Dreyfus 1985; Kanter–Sompolinsky 1987; cited from the
review's memory) — and that is the same thing as
being resolved by pair-averaged data, with any populations.  The certificate is a positive
semidefinite form; finding the conformers from `C` means finding the sign vectors in its
range, and *verifying* the certificate means certifying `min_{x ∉ ±S} f(x) > 0`, a
minimisation of a dense pairwise energy.  The known efficient recovery through the standard
semidefinite relaxation is guaranteed under the much stronger *Schur independence* of the
conformers, which requires `K(K−1)/2 + 1 ≤ n` (Kueng–Tropp 2021): between `√(2n)` and `n`
conformers the ensemble is identified by Theorem E10 but that guarantee is not available.

**Theorem E11 (beyond `2n` conformers nothing is identified).**
(a) Let `ε > 0` and `K ≥ (2 + ε)n`.  With probability at least
`1 − e^{−c(ε)n} − K²(n+1)2^{1−n}` the `K` independent uniform conformers are **not** the zero
set of any non-negative function in the span of the pair observables; hence, by Theorem
E1, no ensemble whose support is the set of all `K` conformers — whatever its weights — is
determined by its pair correlations.  (For `K > n(n−1)/2 + 1` the pair features are affinely
dependent and the conclusion is immediate; the probability bound is meant for smaller `K`.)
(b) (*An explicit twin.*)  Let `n → ∞`, `n/K → y ∈ (0, y₁)` with
`y₁ = (1 − √(1 − 2/π))² = 0.1578…` (i.e. `K/n → 1/y > 6.338`).  With probability tending to one,
every ensemble with positive weights on the `K` conformers has the pair correlations of an
ensemble with full support on the cube; for the uniform ensemble the twin is explicit
(the signs of a Gaussian vector).

**[P]**; (a) uses **[K]** Cover's count of linearly separable dichotomies, (b) uses **[K]**
Bai–Yin's theorem on the smallest singular value and Sheppard's formula
`E[sign g_i · sign g_j] = (2/π) arcsin R_ij` for a centred Gaussian vector with correlation
matrix `R`.

*Proof.*  (a) With probability at least `1 − K²(n+1)2^{1−n}` no two elements of `±S` are equal
or at Hamming distance one.  Suppose `f = c + Σ_{i<j} Q_ij x_i x_j ≥ 0` has zero set `±S`.
Flipping site `1` of a conformer `x^a` gives a state outside `±S`, so
`f(x^{a,1}) − f(x^a) = −2x^a_1 Σ_{j≥2} Q_1j x^a_j > 0`: the labels `−x^a_1` of the `K` points
`(x^a_2, …, x^a_n) ∈ ℝ^{n−1}` are realised by the linear threshold function with weights
`(Q_1j)_j`, through the origin.
`K` points in `ℝ^{n−1}` have at most `2Σ_{i≤n−2} C(K−1, i)` such dichotomies (Cover 1965), and
the labels are uniform and independent of the points; so the probability is at most
`2^{1−K} Σ_{i≤n−2} C(K−1, i) = P(Bin(K−1, ½) ≤ n − 2)`, exponentially small for
`K − 1 ≥ (2+ε)(n−2)`.  If `S` is not the zero set of such an `f`, Theorem E1(a) shows that no
ensemble with support `S` is identified.
(b) `C = SSᵀ/K`.  Let `R_ij = sin(πC_ij/2)` for `i ≠ j`, `R_ii = 1`.  If `R` is positive
definite, the signs of `g ∼ N(0, R)` have full support and pair correlations
`(2/π) arcsin R_ij = C_ij`.  Write `E = C − I` and `R = I + (π/2)E − H` with
`|H_ij| ≤ (π/2)³|E_ij|³/6`.  (i) `λ_min(C) → (1 − √y)²` almost surely (Bai–Yin), so
`λ_min(I + (π/2)E) → 1 − (π/2)(2√y − y)`, positive iff `√y < 1 − √(1 − 2/π)`.  (ii) For `i ≠ j`,
`E_ij` is the mean of `K` independent signs, so `E[E_ij⁶] ≤ 15/K³`, and
`‖H‖_op² ≤ ‖H‖_F² ≤ (π³/48)² Σ_{i≠j} E_ij⁶`, whose expectation is at most
`(π³/48)²·15 n²/K³ → 0`.  So the uniform ensemble `μ_u` on the conformers has a twin `ν_u` with
full support.  If `μ = Σ_a w_a δ_{x^a}` has all `w_a > 0`, put `t = K·min_a w_a ∈ (0, 1]`; then
`μ = tμ_u + (1 − t)μ'` with `μ'` an ensemble on the conformers, and `tν_u + (1 − t)μ'` has the
pair correlations of `μ` and full support (review ER1, F4: version 1 was stated for equal
populations only).  ∎

(a) is the classical capacity bound `α ≤ 2` of associative memories with pair interactions
(Cover 1965; Gardner 1988) read through Theorem E1: a synthesis, not a new bound.

*Numerical check* **[N]** (C5, `n = 300`): the smallest eigenvalue of `R` is `−0.057` at
`K = 5.5n`, `+0.012` at `6.34n`, `+0.040` at `7n`.

So the number of typical conformers that pair data resolve is `Θ(n)`: at least
`n − 10n/ln n`, at most `2n`.  The exact threshold — for which `α` is a random set of `αn`
vertices of the cut polytope a simplicial face — is Problem O1; §4.4 reports where it
appears to be.

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
the `C(n−1, D)` neighbourhoods of size `D = ⌊βK⌋` (a smaller neighbourhood is contained in one
of that size) gives a probability at most
`2n·exp(K[β ln(en/(βK)) + H(β) − ln 2])` (`H` the entropy in nats), which tends to zero when
the bracket is negative.  ∎

*Numerical check* **[N]** (C6): on `n = 60` sites pivoted Cholesky reads exactly
`rn − r(r+1)/2` entries (59, 117, 174, 285, 444 for 1, 2, 3, 5, 8 conformers, against 1 770
pairs) and reconstructs `C` to `10⁻¹⁵`; the two ensembles of (a) differ in one entry.

**Reading.**  For exact data the cost of *certified* identification from pair observables
is `Θ(Kn)` up to a logarithm — the number of parameters of `K` conformers — if the pairs may
be chosen adaptively, and `Θ(n²)` in the worst case if they may not.  (The step that joins
(b) and (c): the pairs read by pivoted Cholesky determine `C` among all positive
semidefinite matrices with unit diagonal, so on the event `𝓔` of E10 their data identify
`μ`, and by Theorem E1(a), "only if", a certificate supported on those pairs exists; the
review ER1 found one by linear programming in 73 of 73 supports.  The constant
`β(¼) ≥ 0.08` is tight for this union bound: the bracket changes sign at `0.0834`.)  The
adaptive procedure is not specific to finite ensembles: it is stopped by the data (a vanishing
residual diagonal), and for a "soft" ensemble with decaying spectrum the same question
becomes one of low-rank approximation from adaptively chosen columns (Problem O6).

### 4.4 Where the threshold appears to be [N]

Theorems E10 and E11 leave the interval `[1, 2]` for the threshold `α*` of Problem O1.  Two
exact computations narrow it numerically; neither is a proof.

*Faces, exactly, on small cubes* (`experiments/ensemble/capacity_threshold.py`: one linear
programme over all `2^{n−1}` states; `capacity_cutting_plane.py`: the same decision by
cutting planes with a full enumeration of the energies after every solve, validated against
the first at `n = 12`).  Frequency with which `K` random conformers (distinct modulo the
flip) form a simplicial face of the cut polytope:

| `n` (trials) | `K/n ≈ 0.9` | `1.0` | `1.1` | `1.2` | `1.3` | `1.4` |
|---|---|---|---|---|---|---|
| 10 (400) | 0.79 | 0.61 | 0.38 | 0.25 | 0.07 | 0.02 |
| 12 (300) | 0.77 | 0.68 | 0.54 | 0.32 | 0.06 | 0.02 |
| 14 (120) | 0.86 | 0.79 | 0.77 | 0.18 | 0.06 | — |
| 16 (100) | 0.99 | 0.94 | 0.66 | 0.26 | 0.07 | 0.01 |
| 18 (60) | 1.00 | 0.93 | 0.62 | 0.20 | 0.02 | 0.00 |
| 20 (40) | — | 1.00 | 0.63 | 0.10 | 0.00 | 0.00 |

(The columns are the nearest integer `K`; exact ratios are in the stored output.)  At
`K = n` the frequency rises towards one with `n`; the point of frequency one half moves
from about `1.05n` (`n = 10`) to `1.12n`–`1.15n` (`n = 14, …, 20`), and the transition
sharpens (at `K ≈ 1.3n`: `0.07, 0.06, 0.06, 0.07, 0.02, 0.00`).  So faces persist beyond `n`,
where no positive semidefinite certificate can exist, and the threshold is **not** `1`.

*A necessary condition at larger sizes* (`symmetric_stability.py`): if the conformers are
the ground states of `xᵀQx` they are strict local minima under single flips, a linear
feasibility problem in the symmetric `Q`.  Frequency of feasibility: `n = 20`: `0.93, 0.80,
0.17, 0` at `K/n = 1.2, 1.3, 1.5, 1.75`; `n = 30`: `1.0, 0.55, 0` at `1.3, 1.5, 1.73`; `n = 40`:
`1.0, 0.8, 0.2, 0` at `1.3, 1.5, 1.6, 1.7`; `n = 60` (6 trials): `1.0, 1.0, 0.33, 0` at the same
ratios.  So single-flip stability with symmetric couplings fails near `1.6n` at these sizes — below the `2n` of independent couplings (Cover),
above the face threshold.

**Conjecture C2.**  There is a constant `α* ∈ (1, 2)` such that `αn` random conformers are a
simplicial face of the cut polytope with probability tending to one for `α < α*` and to
zero for `α > α*`; the computations suggest `α*` between `1.1` and `1.2`, with single-flip
stability lost only near `1.6`.  We have no argument for the value.  (A dimension count of Wendel type —
`Kn` constraints against `n(n−1)/2` unknowns — predicts `α* = 1` and is wrong: the
constraint vectors are not in general position, all of them correlate positively with the
anti-Hebbian direction; `DEAD_ENDS.md` ED7.)

---

## 4a. Part IV — Finite temperature: identification inside a first-order class

Parts I–III put no prior on the ensemble.  At finite temperature every basin is a
distribution, and by E8.1 nothing with a density is identified without a class.  The
programme's class is the *first-order* (envelope) class: on a finite `X`, for a reference
ensemble `π > 0` and an envelope `d`,

    𝒫 = 𝒫(π, d) = { μ ∈ P(X) : μ(y)π(x) ≤ e^{d(x,y)} μ(x)π(y) for all x, y } ,

the Gibbs ensembles `μ_g ∝ π e^{−g}` of the admissible residuals (`β` absorbed in `d`).  The
constraints are linear in `μ`: **the class is a polytope.**  Its *tight graph* at `μ` has an
edge `{x, y}` when one of the two constraints of the pair holds with equality.

### 4a.1 Extreme members, and what "identified inside the class" means

**Theorem E13 (the polytope of the class).**
(a) For a finite envelope, `μ ∈ 𝒫` is an extreme point iff its tight graph is connected.
(b) `μ ∈ 𝒫` is determined by the data of `Φ` *among the members of `𝒫`* iff some
`f ∈ span{1, Φ}` has a set of maximisers `F_f = argmax_{ν∈𝒫} E_ν f` that contains `μ` and on
which the data map `A` is injective.  In particular an extreme member is identified inside
the class iff it is the unique maximiser over the class of the mean of an observable in
the span.
(c) (*Certificate; the bound is the science division's format, the exactness is
linear-programming duality.*)  `E_ν f ≤ t` for all `ν ∈ 𝒫` iff there is a flow `Ψ ≥ 0` on
`X × X` with `(f(z) − t)π(z) ≤ Σ_x Ψ(x, z) − Σ_y e^{d(z,y)} Ψ(z, y)` for all `z`.

**[P]**.  For `d ≡ ∞` off the diagonal, `𝒫` is the simplex and (b) is Theorem E1(a); (a) is
for finite envelopes only (in the simplex `δ_x` is extreme and its tight graph has no
edge — remark of the review ER1).

*Proof.*  (a) In the weights `w = μ/π` a tight edge reads `w(y) = e^{d(x,y)} w(x)`.  If the
tight graph is connected, `w` is determined up to a factor, so `μ` is the only point of `𝒫`
with these tight constraints: a vertex.  If it is not, multiply `w` by `1 + ε` on one
component: for small `|ε|` the finitely many slack constraints stay satisfied, so `μ` is the
midpoint of a segment in `𝒫`.
(b) *If:* `ν ∈ 𝒫` with `Aν = Aμ` has `E_ν f = E_μ f`, so `ν ∈ F_f`, so `ν = μ`.  *Only if:* let
`N = {h : Σh = 0, Ah = 0}`, `T` the tangent cone of `𝒫` at `μ` and `L` its lineality space (the
directions of the minimal face `G` through `μ`).  Identification is `N ∩ T = {0}`.  Then
`(N + L) ∩ T = L`: if `n + l = t` then `n = t − l ∈ T`, so `n = 0`.  The image of `T` in the
quotient by `L` is a pointed polyhedral cone that meets the image of `N + L` only in `0`, so
there is a linear functional vanishing on `N + L` and negative on `T ∖ L`; it is given by
some `f ∈ N^⊥ = span{1, Φ}`, whose maximisers on `𝒫` are exactly `G`, and `A` is injective on
`G` because `N ∩ L = {0}`.
(c) Multiply the inequality by `w(z) ≥ 0` and sum: the right-hand side becomes
`Σ_{x,y} Ψ(x,y)(w(y) − e^{d(x,y)}w(x)) ≤ 0`.  Conversely the bound is the value of a linear
programme in `w` (after normalising `Σ π w = 1`) and `Ψ` is its dual solution.  ∎

### 4a.2 One-body data: a thermal union bound

Let `X = Π_i A_i` (finite alphabets, not necessarily equal), `π = ⊗_i π_i` a product reference
and `d(x, y) = Σ_i δ_i(x_i, y_i)` with every `δ_i` a metric on `A_i` (symmetric).  For `a ∈ X` let

    μ*_a = ⊗_i μ*_{a,i} ,        μ*_{a,i}(s) ∝ π_i(s) e^{−δ_i(a_i, s)} ,

the Gibbs ensemble of the residual `d(a, ·)`: the member *most polarised towards `a`*.

**Theorem E15 (one-body populations pin the most polarised member, dimension-free).**
(a) `μ*_a ∈ 𝒫`, and for every `μ ∈ 𝒫` and every site `i`:  `μ(x_i = a_i) ≤ μ*_{a,i}(a_i)`.
(b) For every `μ ∈ 𝒫`:

    TV(μ, μ*_a)  ≤  Σ_i [ 1 − μ(x_i = a_i) / μ*_{a,i}(a_i) ] .

(c) If all sites are binary:

    TV(μ, μ*_a)  ≤  Σ_i [ μ*_{a,i}(a_i) − μ(x_i = a_i) ] ,

with equality for `μ = μ*_{a'}` whenever `a'` differs from `a` in exactly one site.
(d) On the cube with uniform reference and `d = b·d_H`, `n ≥ 2`: a member is determined
inside the class by its one-body marginals iff at most one of them is unsaturated
(`|E x_i| < tanh(b/2)`); it is then a product measure.

**[P]**; the analytic core of (c) is **[V]**: `Ensemble.thermal_union_bound_density` — for
independent binary sites and a density `r` (`E r = 1`) that does not decrease when a site is
switched to its excited state, `E|r − 1| ≤ 2 Σ_i (E[r·1{x_i excited}] − p_i)` — with
`Ensemble.thermal_union_bound` (the same for any monotone `r`) and
`Ensemble.thermal_union_bound_sharp` (equality on one site).  The Lean statements use a
product expectation defined by iteration over the sites; that the density of a class
member with respect to `μ*_a` is monotone (the first lines of the proof below) is on paper.
As `b → ∞` the member `μ*_a` becomes the conformation `δ_a` and (c) becomes the union
bound `1 − μ({a}) ≤ Σ_i μ(x_i ≠ a_i)`; (c) is its finite-temperature form, with the same
constant one and no dependence on the number of sites, on the reference, or on the
strengths `b_i` of the individual sites.

*Proof.*  Write `w = μ/π`, `w* = μ*_a/π ∝ e^{−d(a,·)}`.
(a) `d(a, x) − d(a, y) ≤ d(x, y)` by the triangle inequality and symmetry, so `μ*_a ∈ 𝒫`.  For
`μ ∈ 𝒫` and a state `s` of site `i`: `w(s, x_{−i}) ≥ e^{−δ_i(a_i, s)} w(a_i, x_{−i})`, so
`μ(x_i = s) ≥ (π_i(s)/π_i(a_i)) e^{−δ_i(a_i,s)} μ(x_i = a_i)`; sum over `s`.
(b) Let `r = μ/μ*_a`.  The same inequality gives *star-monotonicity*:
`r(s, x_{−i}) ≥ r(a_i, x_{−i})` for all `i`, `s`, `x_{−i}`.  Under `μ*_a` the sites are independent.
With `d_i = E[r | x_1 … x_i] − E[r | x_1 … x_{i−1}]` (expectations under `μ*_a`), `r − 1 = Σ_i d_i`
and, `x'` denoting `x` with site `i` resampled independently,

    E|d_i| ≤ E|r(x) − r(x')| ≤ 2·E[ r(x) − r(a_i, x_{−i}) ] = 2·[ 1 − μ(x_i = a_i)/μ*_{a,i}(a_i) ] ,

because `r(x)` and `r(x')` both dominate `r(a_i, x_{−i})`, and
`E_{μ*} r(a_i, x_{−i}) = μ(x_i = a_i)/μ*_{a,i}(a_i)`.  Finally `TV = ½ E_{μ*}|r − 1|`.
(c) For a binary site with `σ_i = μ*_{a,i}(a_i)`, `x_i' ≠ x_i` has probability `2σ_i(1−σ_i)`,
and then `|r(x) − r(x')| = D_i r := r(ā_i, x_{−i}) − r(a_i, x_{−i}) ≥ 0`; so
`E|d_i| ≤ 2σ_i(1−σ_i) E[D_i r] = 2 Cov(r, 1[x_i ≠ a_i]) = 2[σ_i − μ(x_i = a_i)]`.  Equality: for
`μ = μ*_{a'}` both sides equal the total variation of the two laws of the one site that
differs.
(d) If the marginal of site `i` is saturated towards `a_i`, then by the proof of (a) every
inequality `μ(ā_i, x_{−i}) ≥ e^{−b} μ(a_i, x_{−i})` is an equality, so `μ` is the product of the
saturated law of site `i` and its marginal on the other sites, which is a member of the
class there.  So `μ = μ*_{a_T} ⊗ m` with `T` the saturated sites and `m` a member on `T^c` with
no saturated marginal, and `μ` is identified iff `m` is.  If `|T^c| ≤ 1`, `m` is determined
by its marginal.  If `|T^c| ≥ 2`: by E13(b) there would be a one-body `f = c_0 + Σ c_i x_i`
with `m ∈ F_f`; if some `c_i ≠ 0`, every maximiser is saturated at `i` (the bounds of (a) are
attained simultaneously by a product member), which `m` is not; so `f` is constant,
`F_f` is the whole class on `T^c`, and one-body data are not injective there (the uniform
ensemble and a weakly correlated one).  ∎

*Numerical check* **[N]** (`experiments/ensemble/finite_temperature_checks.py`).  F1: for
`n = 3` and `b ∈ {0.5, 1, 2}` the maximum of `TV(μ, P_a) − Σ_i τ_i` over the whole class
polytope, computed exactly by one linear programme per sign pattern, is `0` to `10⁻¹⁵`; 360
sampled (member, centre) pairs for `n = 4, 5, 6` satisfy (c).  F2: (b) on 96 cases with
three-letter sites, random site metrics and non-uniform product references.  F3: (d) on 60
members for `n = 3` by the fibre linear programme.

**Theorem E15T (an interacting known part: the bound holds without frustration, and only
then).**  Binary sites; the envelope is `d(x, y) = Σ_i b_i [x_i ≠ y_i]`; the reference `π` is
any positive measure on the configurations; `μ*_a ∝ π e^{−d(a,·)}` is the member most
polarised towards `a`.  Write `e_i = 1[x_i ≠ a_i]`.  Call `π` **unfrustrated at `a`** if it is
log-supermodular in the variables `e` (`π(e ∨ e')π(e ∧ e') ≥ π(e)π(e')`).  A Gibbs measure
`π ∝ exp(Σ_{i<j} J_ij x_i x_j + Σ_i h_i x_i)` on **any graph, with interactions of any range
and any fields,** is unfrustrated at `a` iff `a` satisfies every bond, `J_ij a_i a_j ≥ 0`;
many-body terms are allowed as long as the product stays log-supermodular.
(a) If `π` is unfrustrated at `a`, then for every member `μ` of the class and every site,
`μ(x_i = a_i) ≤ μ*_a(x_i = a_i)`, and for every ordering of the sites

    TV(μ, μ*_a)  ≤  Σ_i [ E_μ h_i(x_1, …, x_{i−1}) − μ(x_i = a_i) ]  ≤  Σ_i [ μ*_a(x_i = a_i) − μ(x_i = a_i) ] ,

with `h_i(x_{<i}) = μ*_a(x_i = a_i | x_1, …, x_{i−1})`.  For a nearest-neighbour reference on a
tree (a chain) ordered with parents first, `h_i` depends on the parent of `i` only, and the
first bound is linear in the one-body populations.
(b) If `a` violates a bond, both statements of (a) can fail.

**[P]** for (a), given **[K]**: the FKG inequality, and the fact that marginals of
log-supermodular measures are log-supermodular (Karlin–Rinott 1980; a consequence of the
four-functions theorem).  (b) is **[N]**, by exact maximisation over the class polytope.

*Proof of (a).*  `μ*_a` is `π` times a product function of `e`, hence log-supermodular in
`e`, and so are its marginals `ν_i` on the first `i` sites.  As in E15, `r = μ/μ*_a` is
non-decreasing in every `e_i` — the reference cancels in the ratio.  By the FKG inequality
`μ(e_i = 1) = E_{μ*}[r e_i] ≥ E_{μ*}[r]·μ*(e_i = 1)`: the first claim.  Let `n` be the last
site and `q(e_{<n}) = μ*(e_n = 1 | e_{<n})`; the lattice condition applied to `(e', 0)` and
`(e, 1)` with `e ≤ e'` says that `q` is non-decreasing.  Then
`r̄ := E_{μ*}[r | x_{<n}] = (1 − q)·r(·, a_n) + q·r(·, ā_n)` is the ratio of the marginals of
`μ` and `μ*_a` on the first `n − 1` sites; it is non-decreasing in every `e_j` (the two values
of `r` increase, `q` increases, and `r(·, ā_n) ≥ r(·, a_n)`); and

    E_{μ*}|r − r̄| = E[ 2q(1−q)(r(·, ā_n) − r(·, a_n)) ] = 2( E_{μ*}[r e_n] − E_{μ*}[q r̄] )
                  = 2( E_μ h_n(x_{<n}) − μ(x_n = a_n) ) .

Since `E|r − 1| ≤ E|r − r̄| + E_{ν_{n−1}}|r̄ − 1|`, induction on the number of sites gives the
first bound.  For the second: `h_i = 1 − q_i` is non-increasing in `e_{<i}`, and the marginal
of `μ` on the first `i − 1` sites has a non-decreasing density with respect to the
log-supermodular `ν_{i−1}`, so by FKG `E_μ h_i ≤ E_{μ*} h_i = μ*_a(x_i = a_i)`.  ∎

So the thermal union bound is not a statement about independent sites.  It holds with
the same constant for every known part that is ferromagnetic after the gauge
transformation by the centre — nearest-neighbour chains (the regime of theory report
§11.32), lattices in any dimension, mean-field and long-range couplings, attractive
many-body terms — **and frustration is a real obstruction, not an artefact of the proof.**
For non-binary alphabets the induction needs the conditional law of the last site, when an
earlier site leaves its centre state, to put more mass on every non-centre state; we have
not looked for the right hypothesis (Problem O7).  *Numerical check* **[N]** (F6): chains and
triangles of three sites with random couplings satisfied by `a`, random fields and slopes:
the maximum over the class polytope of `TV(μ, μ*_a) − Σ_j [μ*_a(x_j = a_j) − μ(x_j = a_j)]`,
computed exactly, is `0` to `10⁻¹⁵` (six cases); complete graphs on four to seven sites,
1 200 vertices and mixtures of the class polytope: `≤ 3·10⁻¹⁵`; chains of three sites with
one violated bond: `+0.23` to `+0.47`, and there the population bound fails as well.

### 4a.3 Pair data: a bimodal ensemble that one observable identifies

On the cube class (uniform reference, `d = b·d_H`), for `a ∈ {±1}ⁿ` let `M_a(x) = Σ_i a_i x_i` and

    D_a ∝ exp( (b/2)·|M_a| ) ,

the *double cone*: two basins, around `a` and `−a`, each as steep as the class allows,
separated by a barrier of height `nb/2`.

**Theorem E16.**  (a) For even `n`, `D_a` is an extreme member and the **unique** maximiser
over the class of `E_μ[M_a²] = n + 2 E_μ[Σ_{i<j} a_i a_j x_i x_j]`; hence it is determined
inside the class by one mean of one pair-additive observable.
(b) For odd `n` the maximisers are exactly the members
`D_{a,θ} ∝ exp((b/2)|M_a|)·(1 + θ·sign M_a)`, `|θ| ≤ tanh(b/2)`: the pair observable identifies
the two basins and leaves the difference of their populations, `θ`, free within the bound
of the class; `θ = E[sign M_a]` is then identified by one odd observable.

**[P]**.

*Proof.*  Take `a = (1, …, 1)` (a gauge transformation maps the class to itself).  The class
and the functional `μ ↦ E_μ M²` are invariant under permutations of the sites and under the
global flip, and the class is convex, so the average `μ̄` of a member over this group is a
member with the same `E M²` and has the form `μ̄(x) = m(|M(x)|)`.  With `N_l` the number of
states with `|M| = l`, the law of `L = |M|` under `μ̄` is `p(l) ∝ N_l m(l)`, and the class
constraints are `m(l+2)/m(l) ∈ [e^{−b}, e^{b}]`.  For `m*(l) = e^{bl/2}` the ratio `m*/m` is
non-decreasing, so `p*` dominates `p` stochastically (monotone likelihood ratio), and
`E*[L²] ≥ E[L²]` with equality only if `p = p*`.  So every maximiser `μ` has `μ̄ = D`.
(a) For even `n` every edge of the cube changes `|M|` by exactly `2`, so every edge is tight
for `D`: `D` is extreme by E13(a), and an extreme point that is an average of members equals
each of them.  (b) For odd `n` the edges between `M = 1` and `M = −1` are not tight, the tight
graph has the two components `{M > 0}`, `{M < 0}`, and the minimal face through `D` consists
of the members obtained by rescaling the two components, `D_θ`; the cross edges give
`(1+θ)/(1−θ) ∈ [e^{−b}, e^{b}]`.  A maximiser `μ` has `D` as an average of its orbit, so the
orbit lies in the minimal face through `D`.  ∎

*Numerical check* **[N]** (F4): the linear programme `max E[M²]` over the class polytope
returns the value of the double cone for `n = 4, 6, 5`; on the optimal face the weights have
spread `10⁻¹⁶` for even `n` and exactly the predicted spread `0.1102` for `n = 5`, `b = 1`.

**Reading of Part IV.**  Inside a first-order class the ensembles that averaged data can
identify are again the *exposed* ones, and at finite temperature these are the members
whose residual is as steep as the envelope allows along a connected set of pairs: the
polarised basin (one-body data, with a dimension-free constant), the two-basin double cone
(one pair observable).  Bimodality as such is not an obstacle; what cannot be identified
are members in the interior of the class.  The science division's Theorem 2 exhibits such
members (mixtures of polarised basins over a code) and the uniform ensemble — the zero
residual, the hardest instance of the theory division's diagram for algorithms with a hint
— is the most interior of all.  We state this as an observation, not as a theorem relating
the two complexities (Problem O7).

---

## 4b. Part V — Noise: the certificate is the estimator

Let `𝒫 ⊆ P(X)` be convex and compact (all ensembles; an envelope class; a divergence ball),
and let the data be `y = Aμ + σξ` with `ξ` standard Gaussian in `ℝ^m`.  The target is a mean
`T(μ) = E_μ ψ`.  For `f` on `X` let `R_𝒫(f) = sup_{𝒫} E f − inf_{𝒫} E f` (for `𝒫 = P(X)`: the
oscillation of `f`), and

    ω(ε) = sup{ T(μ₁) − T(μ₀) : μ₀, μ₁ ∈ 𝒫, ‖A(μ₁ − μ₀)‖₂ ≤ ε } .

**Theorem E17 (modulus = dual certificate = estimator).**
(a) `ω(ε) = min_{λ∈ℝ^m} { ε‖λ‖₂ + R_𝒫(ψ − λ·Φ) }` for `ε > 0`.
(b) Let `λ` attain the minimum for `ε = 2σ` and `c` be the midpoint of the range of
`E(ψ − λ·Φ)` over `𝒫`.  The affine estimator `T̂ = λ·y + c` has
`sup_{μ∈𝒫} E(T̂ − T(μ))² ≤ σ²‖λ‖² + R_𝒫(ψ − λ·Φ)²/4 ≤ ω(2σ)²/4`.
(c) Every estimator has `sup_{μ∈𝒫} E(T̂ − T(μ))² ≥ Φ_N(−1)·ω(2σ)²/4 ≥ ω(2σ)²/25.3`
(`Φ_N` the standard normal distribution function).

So the minimax root-mean-square error lies between `0.199·ω(2σ)` and `0.5·ω(2σ)`.  **[P]**
(elementary); **[K]** (Donoho 1994): for convex classes the best affine estimator is within
a factor `1.25` of the minimax risk, which is determined by the modulus.

*Proof.*  (a) As in E2(a): `ω(ε) = sup_{μ₀,μ₁} inf_λ [T(μ₁) − T(μ₀) − λ·A(μ₁ − μ₀) + ε‖λ‖₂]`, and
Sion's theorem on the convex compact `𝒫 × 𝒫`.  (b) The bias is
`c − E_μ(ψ − λ·Φ)`, at most `R/2` in absolute value; the variance is `σ²‖λ‖²`; and
`σ²‖λ‖² + R²/4 ≤ (σ‖λ‖ + R/2)²`.  (c) Let `μ₀, μ₁` attain `ω(2σ) =: Δ`.  The events
`{|T̂ − T(μ_j)| < Δ/2}`, `j = 0, 1`, are disjoint, so the two error probabilities sum to at
least one minus the total variation of the two Gaussian laws of `y`, which is
`2Φ_N(‖A(μ₁−μ₀)‖/(2σ)) − 1 ≤ 2Φ_N(1) − 1`.  ∎

**Reading.**  The multiplier `λ` of the dual problem is three things at once: the
certificate of the identified interval at tolerance `ε` (its second term is a range of
`ψ − λ·Φ` over the class, which is what the kernels bound: a maximum and a minimum over `X`
for the model-free class, two flows with gains for an envelope class, two tilted partition
functions for a divergence ball); the weights of a linear estimator; and, by (b)–(c), a
proof that no estimator does better than a constant factor.  The trade-off inside the
minimum is noise amplification `‖λ‖` against the part of the target that the measured
observables do not explain.  *Numerical check* **[N]** (F5): the duality with the `ℓ^∞` data
norm on 200 random instances, gap `5·10⁻¹⁵`.

## 4c. Part VI — Lifted supports: what sum-of-squares certificates reach, and what knowing the number of conformers buys

The certificate of Theorem E10 is a positive semidefinite form in the configuration.  The
same construction with other *lifts* of the configuration gives: the capacity of
higher-order data on the cube; a theorem for generic conformers on any irreducible variety,
torsion angles included; a certificate form of "identified but not exposed"; and an exact
statement of what a prior on the number of conformers adds.  Epistemic status in one
sentence: the principle (E18) is elementary, the two probabilistic and geometric inputs
(E19(a), E20) are published theorems — the first of which we re-derived before finding it
(`PRIOR_ART.md` §5b, `DEAD_ENDS.md` ED15) — and what is ours is the synthesis and the
readings (b)–(e) of E19, E18′ and E20′.

### 4c.1 The principle

A *lift* is a map `v : X → 𝕂^{N×q}` (`𝕂 = ℝ` or `ℂ`; `q = 1` is a vector lift) such that every
entry of `v(x)v(x)^*` is a combination of `1` and the observables, with coefficients in `𝕂`.
For a finite `S ⊂ X` put `U = Σ_{x∈S} col v(x)`, let `P` be the orthogonal projector on `U`, and

    f_S(x) = ‖(I − P) v(x)‖_F² ,        Z_S = { x ∈ X : col v(x) ⊆ U }  ⊇ S .

**Theorem E18 (lifted certificates).**  `f_S` is a non-negative function in the real span of
`{1, Φ}` with zero set `Z_S`.  If `Z_S` is finite and the Hermitian matrices `v(x)v(x)^*`,
`x ∈ Z_S`, are linearly independent over `ℝ`, then every ensemble supported in `Z_S` — in
particular every ensemble supported in `S`, whatever its weights — is determined by the
means of `Φ` among all Borel probability measures on `X`.  Two cases:
(i) `Z_S = S` (*`S` is lift-isolated*) and the subspaces `col v(x)`, `x ∈ S`, are linearly
independent: then the matrices are independent automatically and `f_S` exposes `S` in the
sense of Theorem E1;
(ii) `Z_S ⊋ S`: the ensemble is identified although `f_S` does not expose `S` — the
certificate form of the non-exposed case of Theorem E1(b).

**[P]**; elementary.

*Proof.*  `f_S(x) = tr((I − P) v(x)v(x)^*)` is real and is a combination of entries of
`vv^*`, hence of `1` and `Φ`; it vanishes iff `(I − P)v(x) = 0`.  If `ν` has the data of `μ` and
`μ` is carried by `Z_S`, then `∫f_S dν = ∫f_S dμ = 0`, so `ν(X ∖ Z_S) = 0`, and
`Σ_{x∈Z_S} (ν(x) − μ(x)) v(x)v(x)^* = 0` because every entry is an affine function of the
data and the total masses agree; independence gives `ν = μ`.  In case (i), if
`Σ_x h_x v(x)v(x)^* = 0`, compress with a projection onto `col v(x₀)` along the sum of the
other column spaces: `h_{x₀} v(x₀)v(x₀)^* = 0`.  ∎

| configuration space and data | lift `v` | `Z_S = S` means | where |
|---|---|---|---|
| cube, pair correlations | `x` | the only sign vectors in the span of the conformers are `±` the conformers | Theorem E10 (Odlyzko) |
| cube, correlations of even order `≤ 2d` | `z^{≤d}`: all monomials of degree `≤ d` in `z_j = x_1x_j` | no other lifted vertex in the span of the lifted conformers | Theorem E19 (Baldi–Vershynin) |
| torus `𝕋^r`, Fourier coefficients with indices in `{−1,0,1}^r` | `⊗_k (1, e^{iφ_k})` | the secant span meets the Segre variety only in the atoms | Theorem E20 (trisecant lemma) |
| `ℝ^D`, moments of degree `≤ 2t` | monomials of degree `≤ t` | — | classical: flat extensions (Curto–Fialkow) **[K, memory]** |
| chains with fixed bond geometry, mean squared distances | centred coordinate matrix (`q = 3`) | the chains that are linear images of the stacked conformers are the conformers | the Geometric Inference Division's Theorems B, G(a), I (its GEOMETRY-RES-0001 §0: "your E1 is the principle, our Theorem G(a) an instance") |

*Remarks.*  1. **Three conformers, constructively** (this replaces the citation in
Proposition E9(a)).  Let `x¹, x², x³` be sign vectors, pairwise different modulo sign; they
are linearly independent (a dependency `ax¹ + bx² + cx³ = 0` with `|a| ≥ |b| ≥ |c| > 0` forces
`|a| = |b| + |c|` and then `x² = ±x³`).  Up to a global sign every coordinate shows one of the
four patterns `(+,+,+), (+,+,−), (+,−,+), (−,+,+)`, and at least three of them occur (if only
two did, two of the vectors would agree up to sign).  A sign vector `ax¹ + bx² + cx³` needs
`|a+b+c| = |a+b−c| = |a−b+c| = |−a+b+c| = 1` on the patterns that occur: with all four,
`(a,b,c) = ±e_i` only; with three, also `±(s₁, s₂, s₃)` for one choice of signs.  So `Z_S` is
`S` or `S` and one more vertex `y = s₁x¹ + s₂x² + s₃x³`, and `yyᵀ` is not a combination of
the `x^i x^{iᵀ}` because the six matrices `x^i x^{jᵀ} + x^j x^{iᵀ}` are independent.  By
Theorem E18, every ensemble on three conformers is determined by its pair correlations,
with the certificate `‖P^⊥x‖²` — for two conformers `Z_S = S` — **[P]**; exhaustive check
for `n = 6` (L5: 4 960 triples; a fourth vertex in 2 880 of them).
2. *A sum-of-squares certificate cannot reach beyond the dimension of the lift:* if the
column spaces fill `𝕂^N`, `f_S ≡ 0`.
3. *Stability.*  On a finite `X`, Proposition E1.1 applies with the gap
`γ = min_{X∖Z_S} f_S`; on a continuum `f_S` has at best quadratic growth and the modulus is
that of Proposition E2.2.

### 4c.2 What knowing the number of conformers buys (finite spaces)

**Proposition E18′ (a prior on the number of atoms).**  Let `X` be finite, `S ⊂ X` with `K`
elements, `Φ` affinely independent on `S`, and suppose `S` is *flat-isolated*: no `y ∉ S` has
`Φ(y)` in the affine hull of `Φ(S)`.  Then there is a finite union `H` of proper affine
subspaces of `{w : Σ_a w_a = 1}` such that for every weight vector `w ∉ H` the ensemble
`μ_w = Σ_a w_a δ_{x_a}` is the only ensemble **with at most `K` atoms** that has the data of
`μ_w`.  **[P]**; elementary.

*Proof.*  Let `L = aff Φ(S)`, of dimension `K − 1`, and let `ν` have support `S'`, `|S'| ≤ K`, and
the data `b` of `μ_w`; `L' = aff Φ(S')`.  Then `b ∈ L ∩ L'`.  If `L ⊄ L'`, the weights `w` with
`Aμ_w ∈ L'` form a proper affine subspace `H_{S'}`.  If `L ⊆ L'`, then `L' = L` by dimension, so
`Φ(S') ⊂ L`, so `S' ⊆ S` by flat isolation, and `ν = μ_w` by affine independence.  Take
`H = ∪ H_{S'}` over the finitely many `S'` of the first kind.  ∎

So with the number of conformers known, what is needed is a condition on *one* extra
point at a time (no other vertex on the flat); without it, the whole face must be exposed
(Theorem E1).  Theorem E19(c) shows how far apart the two are.  The restriction to
weights outside `H` cannot simply be dropped: on the cube with five sites, for every
flat-isolated support of 6 or 7 conformers that is not a face there are *some* weights for
which another ensemble with as many conformers has the same pair data (L3) — at that size
`K` is more than half the number of observables; whether exceptional weights exist for
`n < K ≪ n²/4` at large `n` is Problem O9.

### 4c.3 The cube: data of higher order

For a conformer `x` (modulo the flip) let `z_j = x_1x_j`, `j = 2, …, n`, and `ξ_d(x) = z^{≤d}`, the
vector of all monomials of degree at most `d` in `z` (the constant included), of dimension
`L_d = C(n−1, ≤d) = Σ_{j≤d} C(n−1, j)`.  The entries of `ξ_dξ_dᵀ` are the monomials of degree at
most `2d` in `z`, i.e. exactly the correlations `x_A`, `|A|` even, `|A| ≤ 2d`.

**Theorem E19 (data of even order at most `2d`; `d` fixed, random conformers).**
(a) **[K]** (Baldi–Vershynin 2019, Theorems 4.1 and 4.2; the first is Abbe–Shpilka–Wigderson
2015, Theorem 4.5.)  There is an absolute constant `C` such that for `d(n−1)^{0.02} ≤ t ≤
0.001(n−1)` and `K < C(n − 1 − C(n−1)/log(n−1) − t, ≤d)`, with probability at least
`1 − 2^{−t/4} − 2^{−t}` the vectors `ξ_d(x^a)` are linearly independent and their span contains
no `ξ_d(y)`, `y` a vertex of the cube, other than themselves.  In particular this holds with
probability tending to one for `K ≤ (1 − ε)L_d ~ (1−ε) n^d/d!`.
(b) **[P given (a)]**  On that event every ensemble supported on the `K` conformers —
whatever its weights — is determined among all ensembles on the cube by its correlations
of even order at most `2d`, and the conformers are exactly the ground states of the
explicit energy `‖P^⊥ξ_d(x)‖²`, with interactions of even order at most `2d`.  (`d = 1` is
Theorem E10.)
(c) **[P given (a)]**  (*Pair data and a prior on the number of conformers.*)  On the event
of (a) with `d = 2` — so for `K ≤ (1−ε)n²/2` — and for all weights outside a finite union of
proper affine subspaces, the ensemble is the only ensemble **with at most `K` conformers**
that has its pair correlations.  By Theorem E11(a), for `K ≥ (2+ε)n` it is not the only
ensemble with them.  So for `2n < K < n²/2` the number of conformers is exactly the prior
that restores identifiability, and not knowing it costs a factor of order `n` in capacity.
(d) **[P given K: Cover]**  (*An upper bound without a prior.*)  Let
`D_odd = Σ_{j odd, j ≤ 2d−1} C(n−1, j) ~ n^{2d−1}/(2d−1)!`.  If `K ≥ (2+ε)D_odd`, then with
probability at least `1 − e^{−c(ε)D_odd} − K²(n+1)2^{1−n}` the conformers are not the zero set of
any non-negative function with interactions of even order at most `2d`, and no ensemble
supported on all of them is determined by its correlations of even order at most `2d`.
(e) **[N]**  For `d = 2` (two- and four-body data) the truth is far above (b): by exact
linear programming over all states, the number of random conformers that form a face
with frequency one half is about `76`, `152`, `233` for `n = 8, 10, 12` — against the lift
dimensions `29, 46, 67`, beyond which no certificate of the form (b) exists, and the bounds
`84, 186, 352` of (d).
(f) **[N]**  (*A Gaussian control.*)  If the feature vectors of the `2^{n−1}` states are
replaced by independent Gaussian vectors of the same dimension, the same computation
gives thresholds of about `78` and `142` for the sizes of `n = 8, 10`: for four-body data the
cube behaves like a generic cloud of as many points in as many dimensions (and is slightly
more neighbourly).  For pair data it does not: at `n = 12` the Gaussian cloud stops near
`K = 11` and the cube near `13`, at `n = 14` near `11.5` against `16`, and asymptotically the
Gaussian value is `n/(4 ln 2) ≈ 0.36n`
(the weak-neighbourliness threshold of Donoho and Tanner, `K ≈ D/(2 ln(N/D))` for `N` points
in dimension `D ≪ N`; **[K, memory]**) against `1.1n`–`1.2n` for the cube.

*Proof.*  (a) is the cited theorem applied to the independent uniform vectors
`z^a ∈ {±1}^{n−1}` (their Theorem 4.2 excludes vectors `u^{≤d}` "different from `±x_i^{≤d}`"; the
constant coordinate rules out the minus sign, and `u^{≤d} = (z^a)^{≤d}` forces `u = z^a`);
linear independence is their Theorem 4.1 with the same `t`, whose range of `K` is larger.
(b) is Theorem E18(i) with the lift `ξ_d`.  (c) For `d = 2` the vector `ξ_2(x)` is `(1, Φ(x))`
with `Φ` the pair observables, so linear independence of the `ξ_2(x^a)` is affine independence
of `Φ` on `S`, and "no other `ξ_2(y)` in the span" is flat isolation (the constant coordinate
makes the coefficients sum to one); apply Proposition E18′.  (d) As in Theorem E11(a): if
`f = Σ_{|A| even ≤ 2d} c_A x_A ≥ 0` has zero set `±S`, flipping site `v` of a conformer gives
`−2x^a_v g_v(x^a) > 0` with `g_v = Σ_{A∋v} c_A x_{A∖v}`, a combination of the `D_odd` odd monomials
of degree at most `2d − 1` in the other sites; so the labels `−x^a_v` of `K` points of `ℝ^{D_odd}`
are realised by a linear threshold function through the origin; there are at most
`2Σ_{i<D_odd} C(K−1, i)` such labellings (Cover), and the labels are uniform and independent
of the points.  ∎

*Numerical checks* **[N]** (`lifted_checks.py`; `kbody_capacity.py` for (e), stored in
`output_threshold.txt`).  L1: lift isolation for `d = 2` at `n = 12` (66 pair observables):
frequency `1.000, 1.000, 1.000, 0.995, 0.955` at `K = 24, 33, 49, 54, 66` — far beyond `2n = 24`.
L2: `n = 8`, four-body data: 38 lift-isolated supports with 12 to 24 conformers, identification
confirmed by a linear programme over all states in all 38.  L3: `n = 5`, exhaustive over all
supports of the same size: flat-isolated non-faces, random weights — no twin with at most
`K` atoms.

**Reading.**  Three numbers describe what data of order `2d` can do for random conformers:
`n^d/d!` are certified by a sum of squares of degree `d`; at most `2n^{2d−1}/(2d−1)!` can be
identified at all; with a prior on the number of conformers and generic weights, data of
order `d` already reach `n^d/d!`.  For pair data the first two differ by a factor two and
the truth is near `1.1n`–`1.2n` (§4.4).  For four-body data they differ by a factor of order
`n`, and at the sizes we can compute the truth is 2.6 to 3.5 times the sum-of-squares
range, growing with `n`, and equal within a few per cent to the threshold of a Gaussian
cloud of the same size — whose asymptotic value, `D/(2 ln(N/D)) ≈ n³/(48 ln 2)`, is of order
`n³` (Problem O2, Conjecture C3).  This is a gap between *identifiable* and *certifiable by
the natural certificate* that is not a constant, the cube's version of the gap the
Geometric Inference Division found on chains (identifiable from 10 atoms, linearly
certifiable from 12).

**Conjecture C3.**  For fixed `d ≥ 2` the largest `K` for which `K` random conformers are, with
probability tending to one, the ground states of an energy of even order at most `2d` is of
order `n^{2d−1}`; in particular sums of squares of degree `d` certify a vanishing fraction of
the identified supports.  (Evidence: (d), (e), and the Gaussian control (f), whose
asymptotic value is `n^{2d−1}/(2 ln 2·(2d)!)`; for `d = 1` the cube exceeds that value
threefold.  We have no proof of any lower bound above `L_d`.)

### 4c.4 Generic conformers on a variety; torsion angles

**Theorem E20 (generic conformers: the certified capacity is the codimension of the lifted
variety).**  Let `𝒳` be an irreducible complex variety, `v : 𝒳 → ℂ^N` a regular map whose image
spans `ℂ^N`, `𝒱 ⊂ ℙ^{N−1}` the closure of the image of `[v]`, and `c = N − 1 − dim 𝒱`.  Let the
configuration space `X ⊂ 𝒳` be Zariski dense, with `[v]` injective on `X`, and let the
observables span the entries of `vv^*` on `X`.  Then for every `K ≤ c` and all
`(x_1, …, x_K) ∈ X^K` outside a proper Zariski-closed subset, the support `{x_i}` is
lift-isolated with independent `v(x_i)`; hence every ensemble supported on it is determined
by the means of the observables among all Borel probability measures on `X`.
**[P given K]**: the generalised trisecant lemma (Chiantini–Coppens, Corollary 1.3: for an
integral non-degenerate `𝒱 ⊂ ℙ^{N−1}` over `ℂ` and `K − 1 < c`, the span of `K` general points of
`𝒱` meets `𝒱` in exactly those points).

*Proof.*  The exceptional set of the lemma is a proper closed subset of `𝒱^K`; its preimage
in `𝒳^K` is closed and proper because `[v]^K` has dense image, and `X^K` is Zariski dense in
`𝒳^K`.  For a tuple outside it, a point `y ∈ X` with `v(y)` in the span has `[v(y)]` among the
`[v(x_i)]`, so `y` is one of the `x_i`.  General points of a non-degenerate variety are
linearly independent as long as their number is at most `N`.  Theorem E18(i).  ∎

At `K = c + 1` the secant span meets `𝒱` in `deg 𝒱` points when the intersection is finite, and
Theorem E18(ii) still applies whenever the rank-one matrices on the finitely many zeros in
`X` are independent.

**Corollary (torsion angles: the torus `𝕋^r` with multilinear data).**  Let the data be the
Fourier coefficients `∫ e^{i a·φ} dμ`, `a ∈ {−1, 0, 1}^r` — the means of all products of
`1, cos φ_k, sin φ_k` over the angles.  With `v(φ) = ⊗_k (1, e^{iφ_k})` the variety `𝒱` is the Segre
embedding of `(ℙ¹)^r` in `ℙ^{2^r − 1}`, of dimension `r` and degree `r!`, and `𝕋^r` is Zariski dense
in it.  So **every generic ensemble of `K ≤ 2^r − r − 1` points of `𝕋^r` is determined by these
data among all probability measures on the torus**, with a certificate that is a sum of
squared moduli of multilinear polynomials: `K ≤ 4` for three angles, `11` for four, `26` for
five.  For `r = 3` and `K = 5` the certificate has six zeros on the torus (the sixth point
of the secant 4-plane; it is fixed by the antiholomorphic involution `z ↦ 1/z̄`, so it lies
on the torus), and in the instances computed the six rank-one matrices are independent,
so those ensembles are identified as well (**[N]**, L4).

**Proposition E20′ (two states on a torus; an explicit certificate).**  Let `p, q ∈ 𝕋^r`
differ in the angles `k ∈ D` and agree in the others (`k ∈ E`).  With
`a_k = 2 − 2cos(φ_k − p_k)`, `b_k = 2 − 2cos(φ_k − q_k)`,

    f(φ) = Σ_{k∈E} a_k + Σ_{k≠l, k,l∈D} a_k b_l

is a non-negative trigonometric polynomial that uses only frequencies supported on at
most two angles.  If `|D| ≥ 2` its zero set is `{p, q}`, and **every two-state ensemble on
`p, q` is determined among all probability measures on the torus by the means of the
products of `1, cos, sin` of at most two angles**.  If `|D| = 1` no two-state ensemble on
`p, q` is determined by the multilinear data of any order.  **[P]**; elementary.  The
combinatorial core is **[V]**: `Ensemble.twoStateCert_eq_zero_iff` — for non-negative `a`,
`b` that never vanish together on an index set in which every element has another one,
`Σ_{k≠l} a_k b_l = 0` iff all `a_k` vanish or all `b_k` vanish — with
`Ensemble.twoStateCert_nonneg` and `Ensemble.twoStateCert_unique_eq_zero` (one differing
angle: the certificate is identically zero).  That `a_k = 2 − 2cos(φ_k − p_k)` is
non-negative and vanishes only at `p_k`, the terms over `E`, and the passage from the zero
set to identification (Theorem E1) are on paper.

*Proof.*  `f(φ) = 0` iff `φ_k = p_k` on `E` and, for all `k ≠ l` in `D`, `φ_k = p_k` or `φ_l = q_l`.  Let
`A = {k ∈ D : φ_k = p_k}`.  If `A = D`, `φ = p`.  Otherwise take `k ∈ D ∖ A`: then `φ_l = q_l ≠ p_l` for
all `l ≠ k` in `D`, so each such `l` is outside `A`, and applying the same to `l` gives `φ_k = q_k`:
`φ = q`.  The data separate `p` from `q`; Theorem E1.  If `D = {k}`: on the circle where the
other angles are fixed every multilinear observable is affine in `(cos φ_k, sin φ_k)`, and
the first Fourier coefficient of `(1−w)δ_{p_k} + wδ_{q_k}`, a point of the open disc, is that of
infinitely many other measures on the circle.  ∎

*Relation to the science division's SCI-RES-0029 §3.*  Its (a) — two states that differ in
one torsion are never identified from mean squared distances — is the case `|D| = 1`; its
(c) — mean squared distances of a chain are a linear image of the Fourier coefficients
with indices in `{−1,0,1}` of the torsion distribution — is what makes the torus the right
model; and it leaves open whether two states that differ in two or three torsions are
identified, since the Geometric Inference Division's linear certificate (its condition
(CC)) fails there.  Proposition E20′ answers the question *on the torus*: yes, with an
explicit certificate, as soon as two torsions differ.  For chains this becomes a theorem
under two statements that are not ours and that we have not checked: that every
competing state keeps the shared segments rigid (the Geometric Inference Division's
Lemma 2.2, as used in SCI-RES-0029), and that the mean squared distances span the
products of `1, cos, sin` of at most two of the differing torsions (rank 9 of 9 for two
torsions in the science division's computation; not reported for three).

### 4c.5 Identified, certified, and the gap between them

| setting | certified by the natural sum of squares up to | identified up to | not identified beyond |
|---|---|---|---|
| cube, pair data, random conformers | `n − 10n/ln n` (E10) | about `1.1n`–`1.2n` **[N]** (§4.4) | `2n` (E11(a)) |
| cube, two- and four-body data, random conformers | `(1−o(1))n²/2` (E19(b)) | 2.6 to 3.5 times the lift dimension for `n = 8, 10, 12`, about the threshold of a Gaussian cloud **[N]** | `n³/3` (E19(d)) |
| cube, pair data, at most `K` conformers assumed, generic weights | — | `(1−o(1))n²/2` (E19(c)) | `n²/2` (dimension) |
| torus `𝕋^r`, multilinear data, generic atoms | `2^r − r − 1` (E20); `2^r − r` for `r = 2` (E20′) and, in computed instances, `r = 3` | not known | not known (a count of double-point conditions suggests `(3^r − 1)/(r+1)`) |
| chains, mean squared distances, two generic states (Geometric Inference Division) | 12 atoms (its Theorem C) | 10 atoms (its Theorem I) | 8 atoms (its numerics) |

In every row where both are known, the identified range is strictly larger than the range
of the natural certificate; in the second row the two may differ in order.  What a kernel
would have to check beyond the sum of squares — a non-negativity that is not a square, on
a finite space — is the question we put to the theory and complexity divisions
(ENSEMBLE-MSG-0004).

---

## 5. What this says inside the programme

1. **One certificate, two readings.**  The inequality `d(x⋆, y) ≤ E(y) − E(x⋆)` certifies, for
   a known energy `E`, that `x⋆` is optimal whatever admissible residual is added (theory
   report Theorem 2.4) — and, for an energy `E = λ·Φ` in the span of measured observables,
   that averaged data pin every compatible ensemble to `x⋆` within `‖λ‖_*·τ` in transport
   cost (Theorem E2; machine-checked in both directions of use).  On *finite* configuration
   spaces — the rotamer problems on which the kernels run — certificates produced for
   equilibrium problems are identification certificates, and the gap that the `(min,+)`
   kernel certifies is one of the four constants of the stability bound (Proposition E1.1:
   the gap `γ`, the coefficient norm, the conditioning `σ` of the features on the support,
   and the range `R`).  On continuous
   coordinates the inequality cannot hold for smooth observables; the certificate that
   plays its role is a lower bound of a second-order quantity, with a square-root modulus
   (Proposition E2.2), which — on the science division's reading of the theory report, to
   be confirmed by the theory division — no existing kernel checks.
2. **Identified ensembles are the frustration-free ones.**  With no prior at all, on a
   finite configuration space, what averaged data can determine is exactly the ensembles
   whose support is the *whole* ground-state set of an energy in the span of the
   observables, with affinely independent features on it (Theorem E1).  Everything else is partially
   identified, and the science division's certificate formats
   (`INFERENCE_LIMITS.md` §8) are the tools for it.  Our results are the uniqueness side of
   its model-free format.
3. **Compatibility with the science division's Theorems 2 and 3.**  There, `k`-body data
   that look uniform bound every basin population by about `n^{−⌊k/2⌋}` and cannot exclude a
   mixture of that many basins.  Here, pair data resolve up to about `n` *point* conformers
   in typical position, and fail beyond `2n`.  The two statements are compatible: on the
   event of Theorem E10 an identified `K`-conformer ensemble has correlation rank `K < n`,
   while the uniform-looking datum `C = I` has rank `n`; and Proposition E9(b) is the
   smallest case of their code construction.  (In general an identified `K`-conformer
   ensemble has rank at most `min(K, n)` only: the cut polytope on three sites is a simplex,
   so the uniform ensemble on its four vertices is identified, with rank three.  Version 1
   said "rank `K`"; ER1 F3.)
4. **Geometry enters through one matroid.**  For distance distributions, the ensemble-level
   question reduces to connectivity of the rigidity matroid (Theorem E5), which for
   globally rigid graphs is a theorem of 2022.  A rigidity result of the Geometric
   Inference Division that controls the matroid of a measurement map — for torsion angles,
   for orientational restraints, for bodies and hinges — becomes an ensemble statement
   through Corollary E6 within its hypotheses: a rational parametrisation, generic
   conformers (no shared feature values), and a conclusion about the ensemble of feature
   vectors only.

## 6. Verification status

| item | status |
|---|---|
| Lean | `proofs/Ensemble/Exposedness.lean`, `RenyiHeppes.lean`, `ThermalUnionBound.lean`, `TwoStateCertificate.lean`: sixteen headline theorems and four non-vacuity witnesses listed in `proofs/AxiomAudit.lean`; standard axioms only; no warning; the Lean stages of the programme's `scripts/audit_all.sh` pass on this branch (the status file records the Python stages).  What is machine-checked is named at each theorem; everything else is a paper proof.  Of Part VI only the combinatorial core of E20′ is machine-checked; for finite `X` the last step of E18 is `eq_of_exposing_certificate` applied to the zero set |
| numerics | `experiments/ensemble/run_all.py` runs the six scripts whose numbers are quoted (output in `experiments/ensemble/output.txt`); the threshold computations of §4.4 and §4c.3 are separate (`capacity_threshold.py`, `capacity_cutting_plane.py`, `symmetric_stability.py`, `kbody_capacity.py`; output in `output_threshold.txt`) |
| review | an internal adversarial review of version 1 (Parts I–III; `reviews/ER1_internal_review.md`, by a subagent of this division — an AI review, not peer review) found no false numbered statement, five major and thirteen minor defects of wording, citation and scope; all are applied and listed in §7.  The science division has accepted a review of E5, E7, E8, E1.3 and §5 (its workstream R21; SCI-RES-0028) and has already contributed Proposition E2.2.  Parts IV and V, Theorem E7′ and §4.4 (version 2) are under a second internal review, commissioned at the third checkpoint and not yet reported; Part VI (version 3) has been read by nobody but its author.  No external peer review |
| prior art | `PRIOR_ART.md`: the searches of the first checkpoint and those of the internal review; for Parts IV and V and E7′ two searches (obligation OB10); for Part VI the two cited theorems were read in the sources (§5b), E18′, E20′ and C3 were not searched (OB16) |

## 7. Corrections and changes since version 1 (commit `a570520`)

*(Items 1–6: version 2, commit `1a067b5`.  Item 7: version 3.)*

1. **Theorem E11 strengthened and restated** (linked correction of ENSEMBLE-MSG-0002 §1,
   in ENSEMBLE-MSG-0003).  Version 1: "beyond `6.34n` random conformers (equal populations)
   the pair correlations are those of a full-support ensemble".  That statement stands as
   E11(b), but the constant was not the right bound: by Cover's count at one site, beyond
   `(2+ε)n` conformers *no* ensemble supported on all of them is identified, whatever the
   weights (E11(a)).  `DEAD_ENDS.md` ED9.
2. **Proposition E2.2 added** — on a continuous configuration space the sharp-minimum
   inequality cannot hold for smooth observables and the modulus is a square root.  This
   is the science division's observation (SCI-RES-0026, SCI-RES-0028); Example E1.2 was
   presented in version 1 as an example where it is the rule.  §5 item 1 is restricted
   accordingly.
3. **Terminology.**  "Ensemble rigidity" (version 1, Theorem E7) is now "distributional
   ensemble rigidity", because the Geometric Inference Division uses the shorter name for
   a different property.  Corollary E1.3 now cites that division's independent
   Proposition 3.1 and its Theorems B, C (statewise constraints restore identifiability).
4. **Added:** the remark that E5 and E6 hold for rational feature maps; Theorem E7′ (two
   rigid bodies); §4.4 (numerical location of the capacity threshold; Conjecture C2); Part
   IV (E13, E15, E16); Part V (E17).  The limitation "what a law of a distance is
   physically" is quoted from the science division.
5. Prior art: Donoho–Tanner (2005) and Bruckstein–Elad–Zibulevsky (2008) for E1 (found by
   the science division).
6. **Internal review ER1 applied** (`reviews/ER1_internal_review.md`; linked correction of
   ENSEMBLE-MSG-0002 in ENSEMBLE-MSG-0003 §1a).  No numbered statement of version 1 was
   found false; the following sentences *around* them were, and are withdrawn:
   * *F1.*  "An ensemble is determined exactly when it is exposed by a non-negative function
     in the span" (summary; §5 item 2).  False both ways: `X = {a, b, c}` with one feature
     `(0, 0, 1)` is exposed and not identified; Example E1.2 is identified and not exposed.
     Now stated with the two conditions of Theorem E1.
   * *F2.*  "Identification = absence of chimeras" (§3.2) and "identified exactly when the
     zero set of `f` contains nothing but the conformers" (§3.3).  Only "no chimera ⇒
     identified" is true; two counterexamples, one on an open set of frameworks, are now in
     §3.2 (check R7).
   * *F3.*  "An identified `K`-conformer ensemble has correlation rank `K`" (§5 item 3): only
     on the event of Theorem E10.
   * *F4.*  E11(b) restricted to equal populations without need; E11(a) classed as new
     although it is the classical capacity bound read through E1; a sign in its proof.
   * *F5.*  E10(c) attributed to Odlyzko a statement about a larger event and without the
     hypothesis `K ≥ 3`; the two missing lines are supplied.
   * *Minor (F6–F18).*  A number quoted for check R5 that the script did not print (22
     for 82; the check now starts near both conformers); the compact case in the summary
     row of E1; exception and definition in E1.3(b); the upper bound in Example E1.2;
     hypotheses of E2(c) and what exactly is machine-checked there; the degenerate case and
     the novelty class of E3; Heppes' theorem misquoted; the closing remark of §3.1; three
     neighbourhoods in the proof of E5(b); a non-generic counterexample on the line and a
     classical citation for E8; the source for 3-neighbourliness; three remarks on E12;
     §5 items 1 and 4; three checks that tested less than they said (T2, C2, R5).
   * *Novelty classes lowered:* E2(c), E3 to "formulation"; E11(a) to "synthesis"; E4 gains
     a neighbour (frameproof codes) and E10 two (projection-rule memories).
   * *Remarks of the review on version-2 material:* E7′(a) was false for one leg and
     E7′(b) exchanged two quantifiers without an argument; E13(a) needs a finite envelope.
     All three are corrected.
7. **Version 3 (third checkpoint): Part VI added** (§4c: Theorems E18, E18′, E19, E20,
   Proposition E20′, Conjecture C3; Problems O9, O10; O2 answered in part).  Proposition
   E9(a) has its own proof now (§4c.1) and no longer rests on a citation.  Corollary
   E1.3(b) carries the qualifier "no statewise constraint" asked for by the Geometric
   Inference Division.  The probabilistic core of E19 is a published theorem that we
   re-derived before finding it; it is cited, not claimed (`DEAD_ENDS.md` ED15).

## 8. Limitations

* **Exact data.**  Parts II and III are about exact data.  Part I has tolerances and Part V
  Gaussian noise on means; there is no noise model for laws.
* **What a law of a distance is, physically** (the science division, SCI-RES-0026 §3, from
  general knowledge of the experiments): each measured distance distribution is the
  solution of an ill-posed deconvolution and comes with a band, not as a law; the distance
  is between labels on flexible linkers; different pairs are measured on different
  samples; scattering gives one pooled distribution and averaged couplings give moments.
  Theorems E7, E7′, E8 are statements about exact laws of exact distances and reach no
  datum before a stability modulus under a band exists (Problem O4).
* **Point conformers.**  Finite ensembles are an idealisation.  At finite temperature every
  basin is a distribution; Proposition E8.1 shows that without a class nothing is
  identified from finitely many smooth observables.  Identification *inside* the
  first-order class is treated in Part IV for one-body data and, in one extremal case, for
  pair data; inside an exponential family with a remainder it is not treated.
* **Genericity.**  Theorems E5–E8 are for generic tuples of conformers.  Conformers that
  share rigid parts — the typical case in applications — have coincident edge lengths and
  are not generic; Theorem E7′ treats two rigid bodies, and the general case is a
  contraction of the rigidity matroid (Problem O3).
* **No algorithm with a complexity guarantee.**  Certificates are exhibited; finding them
  (sign vectors in a subspace; the conformers behind `2K` moments per edge) is not
  analysed.  Verifying the gap of the certificate of Theorem E10 is a hard minimisation in
  general.
* **Asymptotics.**  Theorem E11(b) is asymptotic; E10 and E11(a) leave the constant of the
  capacity between `1` and `2`.
* **Sources.**  Odlyzko's theorem, the 3-neighbourliness of the cut polytope, Bai–Yin,
  Cover, Vitushkin–Henkin and Gortler–Healy–Thurston are cited without a full reading of
  the original texts (see `PRIOR_ART.md`).

## 9. Open problems and conjectures

* **O1 (the capacity of pair data).**  For which `α` is a random set of `αn` vertices of the
  cut polytope a simplicial face, with high probability?  Proved: yes for `α < 1` (E10(c));
  no for `α > 2` (E11(a)).  Numerically the threshold is between `1.1` and `1.2` (§4.4,
  Conjecture C2).
  A proof would need certificates that are not positive semidefinite forms (lower bound)
  and an obstruction finer than single-site stability (upper bound).
* **O2 (`k`-body data).**  Answered in part by Theorem E19: for data of even order at most
  `2d`, `(1−ε)n^d/d!` random conformers are certified by the projector on the lifted
  conformers (the analogue of Odlyzko's theorem for tensor lifts is Baldi–Vershynin 2019),
  and nothing is identified beyond `(2+ε)n^{2d−1}/(2d−1)!`.  Open: the true order for
  `d ≥ 2` (Conjecture C3: `n^{2d−1}`); any certificate that is not a sum of squares of
  degree `d`; the constant for `d = 1` (Problem O1).
* **O3 (conformers with common rigid parts).**  If the conformers agree on a set `J₀` of
  features and are generic otherwise, is the ensemble identified from the laws of the
  remaining features iff the contraction `𝓜/J₀` is connected?  Settled for two rigid
  bodies (Theorem E7′: `dim SE(d) + 1` legs).  Open: several bodies (connectivity of the
  body–bar matroid, in terms of the multigraph of bars); hinges and other joints; fibres
  with several components when the common part is given by distances only.
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
* **O7 (finite temperature).**  Answered in part by E13–E16 and E15T.  Open: the thermal
  union bound for non-binary alphabets with an interacting reference; what replaces it
  at a frustrated centre (a constant larger than one? a different centre member?);
  which members are identified by `k`-body data for `k ≥ 2` beyond the double cone; the
  exact constant in total variation for non-binary sites; and whether there is a theorem
  relating "hard for evaluations" to "interior for ensemble data".
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
* **O9 (a prior on the number of conformers, all weights).**  Proposition E18′ excludes a
  null set of weights.  For random conformers on the cube with `n ≪ K ≪ n²/4`, is every
  ensemble on them — all weights — the only one with at most `K` conformers and its pair
  correlations?  Equivalently: is the span of the lifted conformers disjoint from the
  span of any `K` other lifted vertices?  (Resilience against one vertex is the theorem
  of Baldi and Vershynin; at `n = 5`, where `K > m/2`, exceptional weights exist.)
* **O10 (the torus beyond sums of squares).**  For generic atoms on `𝕋^r` with multilinear
  data: is the largest identified `K` equal to `2^r − r`, to the count `⌊(3^r − 1)/(r+1)⌋`, or
  in between?  For chains: do mean squared distances span the pairwise products needed
  by Proposition E20′ when three or more torsions differ (a question to the science and
  geometry divisions)?
