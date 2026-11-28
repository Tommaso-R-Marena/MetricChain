# Certified inference over classes of Boltzmann weights: theorem S3 verified, improved, and replaced

*Computational Research Division, branch `research/phase2-certified-inference`, Phase II (research
owner's directive D-11).  Written 2026-11-28.  Status of every statement: **[P]** paper proof given
here; **[N]** checked numerically by the prototype (`src/metricchain_eng/certinf/`, tests
`tests/eng/test_certinf.py`, `tests/eng/test_certinf_review.py`); nothing here is machine-checked.
**Second version.**  The first version was reviewed adversarially by a subagent (`REVIEW_A.md`: three
critical and eight major findings).  Every finding is answered here; §13 lists what changed.  Two claims
of the first version were wrong and are withdrawn: that the cost in the envelope ratio is a property of
the class (it is a property of the sampling law — Theorem 5.4), and that the sequential bound is exact
for monotone targets on sites with more than two states.  The corrected statements and Theorem 5.4 have
not been refereed again.*

## 0. Verdict

1. **S3 is correct**, with the constant it states, once five assumptions it leaves out are added (§2).
   Its proof is a covering-net argument and is routine.
2. **Its sample bound can be improved when there are many observables or `ε` is small.**  The dimension
   enters as `log d` instead of `d·log(1/ε)` (Theorem 3.1).  For `d ≤ 6` and large `ε` S3's own bound is
   the smaller one, and both are loose by a factor 4 to 7 against simulation.
3. **Compressing the whole moment body is the wrong tool for the stated purpose.**  A sound outer
   interval needs one expectation of one explicit function to be certified non-positive (Theorems 4.1,
   5.1).  The validity of that certificate does not depend on the number of observables or on the
   sample size; it adapts to the variance, needs none of `b`, `G`, `Z_l`, needs no union bound over
   thresholds, and handles `G = 0`.  Its *width* does depend on the number of observables, through the
   fitted multipliers (the referee measured an excess of 0.09 to 0.26 at a thousand draws as `m` goes
   from 1 to 60).
4. **The cost in the envelope ratio `Γ = sup u/l` belongs to the sampling law, not to the problem.**
   With draws from the reference, or from S3's gap distribution, no procedure avoids a number of draws
   proportional to `Γ` in the worst case over instances (Theorem 6.1).  With draws from the extremal
   ensemble of the class — a Boltzmann weight with a modified energy — the same certificate costs what
   a bounded average costs: no `Γ`, and no bound on `u` to declare (Theorem 5.4, pointed out by the
   referee).  The first version of this note said the cost was "a property of the class, not of the
   method"; that was wrong.  What *is* a property of the class, whatever is sampled: for an energy
   envelope of half-width `ρ`, `Γ = e^{2ρ}`, and with an extensive residual the identified sets of the
   rectangular class of S3 are nearly vacuous (§9.4).
5. **The class that repairs this is in the archive**: the theory division's bounded-influence
   (Lipschitz) energies, for which it already has the linear structure and a transport duality with
   gains (its Theorems 11.12 and 11.105; Theorem 9.1 here is that duality applied to a tilted score).
   What is added here: for product references the class is closed under marginalisation; for additive
   observables the identified set — with observations — is computed exactly at any system size
   without sampling (Proposition 9.2, Corollary 9.3); for functions of a few additive statistics a
   sound outer interval is computed by dynamic programming (Proposition 9.6; 1.13 to 1.40 times the
   exact width in the twenty cases of one experiment, up to 1.84 and 3.97 in the referee's — these are
   cases, not a bound on the looseness); for references that are not products the computation for
   additive observables gives a sound outer interval with enlarged constants (Proposition 9.7, on an
   inequality of the theory division).  Every rectangular class containing the same class gives an
   interval within `e^{−un}` of the trivial one (§9.4).
6. **Novelty is low, and much of the exact theory was already in the archive.**  The exact dual of §4
   for exact data is the science division's item 89(d); its form with regions is the ensemble
   division's E17.2 for the model-free case; S3's sampler is the theory division's Proposition 11.113
   (for another question).  Outside the archive the ingredients are classical (§10).  What was found
   neither in the archive nor in a bounded search: the sampled certificate for an interval with data
   (Theorem 5.1), the lower bound for reference and gap draws (Theorem 6.1), and the closure statements
   of §9.  Theorem 5.4 is importance sampling from a least-favourable member of the class; no search
   was made for it.  All are short, and a specialist may know them.

## 1. Setting, and the proposal under review

`X` is a finite set of configurations.  An **envelope** is a pair `l, u : X → [0, ∞)` with `l ≤ u` and
`Σ_x u(x) > 0`.  The **box class** is `W(l,u) = {w : l ≤ w ≤ u, Σ w > 0}`, and `P(l,u) = {w/Σw : w ∈
W(l,u)}`.  It is invariant under a common rescaling of `l` and `u`.  With energies, `l = e^{−E_max}`,
`u = e^{−E_min}`; with a reference model, `l = w₀ e^{−ρ}`, `u = w₀ e^{ρ}`.  Write `g = u − l`,
`G = Σ g`, `Z_l = Σ l`, and `Γ = sup_x u(x)/l(x) ∈ [1, ∞]` (with `0/0 = 1`).  `P(l,u)` is convex and
compact for every envelope; for `l ≡ 0` it is the set of all probabilities on `supp u`.

`φ : X → ℝ^m` are the measured observables, `f : X → ℝ` the target, `v = (1, φ, f) ∈ ℝ^d`, `d = m + 2`.
The **observation region** `R ⊂ ℝ^m` is closed and convex, with support function
`h_R(η) = sup_{y∈R} η·y`.  For a box with centre `y⁰` and half-widths `e`, `h_R(η) = η·y⁰ + Σ|η_i|e_i`;
for an ellipsoid `{y : (y−y⁰)ᵀΣ⁻¹(y−y⁰) ≤ χ²}` (correlated errors), `h_R(η) = η·y⁰ + χ·(ηᵀΣη)^{1/2}`.
The **identified set** of the target is

    I = { E_p f : p ∈ P(l,u), E_p φ ∈ R },      V⁺ = sup I,   V⁻ = inf I.

It is a compact interval (the image of a compact convex set of ensembles under a linear map), possibly
empty.

**The proposal ("S3"), as given to this division.**  "Suppose rigorously justified energy envelopes give
Boltzmann-weight bounds l(x) ≤ w(x) ≤ u(x).  For bounded measured observables φ(x) and bounded target
observable f(x), define v(x) = (1, φ(x), f(x)), b = Σ_x l(x)v(x), G = Σ_x [u(x)−l(x)], Z_l = Σ_x l(x).
The set of compatible unnormalized ensemble moments is the zonotope K = b + Σ_x [u(x)−l(x)] [0,v(x)].
For G>0, sample independent configurations from q(x) = [u(x)−l(x)]/G.  Construct
K_hat = b + (G/L) Σ_j [0,v(X_j)].  The proposed concentration theorem is d_H,infinity(K,K_hat) ≤ εG with
probability at least 1−δ, provided L ≥ (2/ε²)[d log(1+8/ε)+log(2/δ)], where d is the dimension of the
moment vectors. … After normalization by total weight, the corresponding coordinatewise approximation
error is at most κ = 2εG/Z_l.  Consequently, enlarging the experimental observation region by κ, solving
the compressed linear-fractional optimization problem, and expanding the resulting target interval by κ
gives a probabilistically sound outer identified interval.  Infeasibility after the appropriate
expansion can certify inconsistency between the observation region and the assumed energy class."

## 2. S3 re-derived

**Proposition 2.1 (the moment body) [P].**  `K := {Σ_x w(x)v(x) : l ≤ w ≤ u} = b + Σ_x g(x)[0, v(x)]`, a
zonotope, with support function

    h_K(λ) = λ·b + Σ_x g(x)(λ·v(x))₊ = Σ_x [ u(x)(λ·v(x))₊ − l(x)(λ·v(x))₋ ],

and `I = {M_f/M_0 : M ∈ K, M_0 > 0, M_φ/M_0 ∈ R}`.

*Proof.*  Write `w = l + t·g` with `t(x) ∈ [0,1]`.  The supremum of `λ·M` over `K` takes `t(x) = 1`
exactly where `λ·v(x) > 0`.  ∎

**Theorem 2.2 (S3, concentration) [P].**  Assume **(H1)** `‖v(x)‖_∞ ≤ 1` for all `x`, **(H2)** `b` and
`G` are known exactly, **(H3)** `X_1, …, X_L` are independent with law exactly `q = g/G`, **(H4)** `G > 0`.
If `L ≥ (2/ε²)[d·ln(1 + 8/ε) + ln(2/δ)]`, then with probability at least `1 − δ`,
`d_{H,∞}(K, K̂) ≤ εG`.

*Proof.*  For convex compact sets the Hausdorff distance in a norm is the supremum over the dual unit
ball of the difference of the support functions; the dual of `ℓ∞` is `ℓ1`.  By Proposition 2.1,
`h_K(λ) − h_{K̂}(λ) = G·[E_q ψ_λ − (1/L)Σ_j ψ_λ(X_j)]` with `ψ_λ(x) = (λ·v(x))₊`.  For `‖λ‖₁ ≤ 1`, (H1)
gives `ψ_λ ∈ [0,1]`, and `λ ↦ ψ_λ(x)` is 1-Lipschitz in `ℓ1`.  Hoeffding for one `λ`:
`P(|dev| > ε/2) ≤ 2e^{−Lε²/2}`.  An `ε/4`-net of the `ℓ1` unit ball in its own norm has at most
`(1 + 8/ε)^d` points, and both the mean and the empirical mean are 1-Lipschitz, so the deviation at any
`λ` exceeds that at the nearest net point by at most `ε/2`.  A union bound gives the claim.  ∎

**Proposition 2.3 (normalisation) [P].**  Assume (H1) and **(H5)** `Z_l > 0`.  If `M ∈ K`, `M̂ ∈ K̂` and
`‖M − M̂‖_∞ ≤ εG`, then `|M_i/M_0 − M̂_i/M̂_0| ≤ 2εG/Z_l =: κ` for every coordinate `i`.

*Proof.*  `|M_i M̂_0 − M̂_i M_0| ≤ |M_i|·|M̂_0 − M_0| + M_0·|M_i − M̂_i| ≤ 2 M_0 εG` because `|M_i| ≤ M_0`
by (H1); and `M̂_0 ≥ b_0 = Z_l` for every point of `K̂`.  ∎

**Corollary 2.4 (outer interval, inconsistency) [P].**  On the event of Theorem 2.2, with
`Î_κ = {M̂_f/M̂_0 : M̂ ∈ K̂, M̂_φ/M̂_0 ∈ R ⊕ κB_∞}`: `I ⊂ Î_κ + [−κ, κ]`; and if `Î_κ = ∅` then `I = ∅`.
(Convexity of `R` is not used for this statement, only for computing `Î_κ`.)

**What S3 leaves out.**

| | assumption | what happens without it |
|---|---|---|
| H1 | all observables scaled to `[−1, 1]` | the bound is `εG·sup‖v‖_∞`; an unscaled observable silently breaks `κ` |
| H2 | `b`, `G` (hence `Z_l`) exact | these are sums over all of `X` — partition-function-type quantities, in general as hard as the problem itself; §7 |
| H3 | exact independent draws from `q` | with a Markov chain sampler the Hoeffding step fails; §7 |
| H4 | `G > 0` | `q` is undefined; §7.5 |
| H5 | `Z_l > 0` | `κ = ∞`: no statement in the model-free case `l ≡ 0` |
| — | (not an assumption: the *width*) | soundness holds under H1–H5, but the excess width is not `O(κ)` in general: with `φ = ε'·f` and exact data the enlargement of the region alone costs `κ/ε'` |

(The first version counted the last row as a sixth assumption; it is not one.)

**Proposition 2.5 (conditioning of the enlarged problem) [P].**  For every `τ, η` with `Ψ(τ, η) ≤ 0` in
the notation of §4, `sup I(R ⊕ κB_∞) ≤ τ + κ‖η‖₁`.  Hence, when an optimal multiplier `η⁺` exists
(`Ψ(V⁺, η⁺) ≤ 0`), the enlargement of the region costs at most `κ‖η⁺‖₁`: the size of the Lagrange
multipliers of the observation constraints, unbounded over instances.

*Proof.*  `h_{R⊕κB_∞}(η) = h_R(η) + κ‖η‖₁`, so the score of §4 for the enlarged region at `τ + κ‖η‖₁`
equals the score for `R` at `τ`.  ∎

*What this gives for S3, and what it does not* (corrected after the review, finding m2).  On the event
of Theorem 2.2 a point of `K̂` whose normalised observables lie in `R ⊕ κB_∞` corresponds to a point of
`K` with observables in `R ⊕ 2κB_∞` and a target within `κ`.  So each end of S3's interval exceeds the
corresponding end of `I` by at most `2κ(1 + ‖η^±‖₁)`, and the excess width is at most
`2κ(2 + ‖η⁺‖₁ + ‖η⁻‖₁)`, not `2κ` — when optimal multipliers exist.  They need not: for a region tangent
to the reachable set the infimum of Theorem 4.1(b) is not attained and the enlargement costs of the
order of `√κ` (the referee's example: `0.134·√κ` for `κ = 10⁻³ … 10⁻⁵`).

## 3. The concentration bound improved

**Theorem 3.1 (dimension enters logarithmically) [P].**  Under (H1)–(H4), with probability at least
`1 − δ`,

    d_{H,∞}(K, K̂) ≤ G·[ 2·√(2 ln(2d)/L) + √(ln(2/δ)/(2L)) ].

So `L ≥ ε⁻²·(2√(2 ln 2d) + √(ln(2/δ)/2))²` suffices, against `2ε⁻²[d ln(1+8/ε) + ln(2/δ)]` in S3.  Not
uniformly better: at `δ = 0.05` S3's own bound asks for fewer draws when `d = 2` and `ε > 0.21`, `d = 3`
and `ε > 0.35`, `d = 4` and `ε > 0.53`, `d = 6` and `ε > 0.99` (the referee's computation).  The smaller
of the two may be used, each being a deterministic bound on the same quantile.

*Proof.*  Let `F = {ψ_λ : ‖λ‖₁ ≤ 1}`, `D⁺ = sup_F (E_q ψ − P_L ψ)`, `D⁻ = sup_F (P_L ψ − E_q ψ)`.  Changing
one `X_j` changes `D^±` by at most `1/L`; McDiarmid gives `D^± ≤ E D^± + √(ln(2/δ)/(2L))` with
probability `1 − δ/2` each.  By symmetrisation `E D^± ≤ 2·E sup_F (1/L)Σ σ_j ψ(X_j)`.  The positive part
is 1-Lipschitz, so by the contraction lemma (Ledoux–Talagrand) the Rademacher average of `F` is at most
that of the linear class, `E‖(1/L)Σ σ_j v(X_j)‖_∞`, and by Massart's finite-class lemma applied to the
`2d` vectors `±(v_i(X_1), …, v_i(X_L))` of Euclidean norm at most `√L` this is at most `√(2 ln(2d)/L)`.  ∎

*Remark 3.2 (multiplicative approximation, coresets).*  The literature on approximating zonoids by
zonotopes (Bourgain–Lindenstrauss–Milman; Talagrand; `ℓ1` Lewis-weight sampling, Cohen–Peng) proves more
than Theorems 2.2 and 3.1: a `(1 ± ε)` approximation of the symmetric part `Σ g(x)|λ·v(x)|` in *every*
direction with about `d log d/ε²` generators — but drawn from the Lewis distribution, which depends on
the whole generator matrix, not from `q`.  This matters here: at an optimum the gap term in the
relevant direction is of order `Z_l`, not `G` (§5.3), so a multiplicative guarantee would remove the
factor `G/Z_l`.  Theorem 6.1(b) shows that draws from `q` cannot achieve this.  Lewis sampling needs a
pass over all of `X`, after which the exact problem is solvable too; its use is a *coreset* — a
compressed body, of size independent of `|X|`, answering every region `R` for fixed `(φ, f)`.  Not
implemented.

## 4. The exact problem: a dual with one multiplier per observable

For `τ ∈ ℝ` and `η ∈ ℝ^m` with `h_R(η) < ∞` define the **score** and its **certificate value**

    s_{τ,η}(x) = f(x) − τ − η·φ(x) + h_R(η),
    Ψ(τ, η)   = Σ_x [ u(x)·s₊(x) − l(x)·s₋(x) ] = Σ_x [ l(x)s(x) + g(x)s₊(x) ].

`Ψ` is jointly convex and non-increasing in `τ`, with `Ψ(τ', η) ≤ Ψ(τ, η) − (τ' − τ)Z_l` for `τ' > τ`.

**Theorem 4.1 (identified interval; consistency) [P].**
(a) *Soundness, with no assumption.*  If `Ψ(τ, η) ≤ 0` for some `η`, then `E_p f ≤ τ` for every
`p ∈ P(l,u)` with `E_p φ ∈ R`.
(b) *Completeness, for every envelope.*  Put `T(η) := h_R(η) + max_{p∈P(l,u)} E_p[f − η·φ]`.  Then
`Ψ(τ, η) ≤ 0` if and only if `τ ≥ T(η)`, and `inf_η T(η) = V⁺` (`−∞` if `I = ∅`).  So
`V⁺ = inf{τ : ∃η, Ψ(τ, η) ≤ 0}` whenever `I ≠ ∅`, also for `l ≡ 0`.  The infimum over `η` need not be
attained (a region tangent to the reachable set).
(c) *Extremal weights.*  Let `τ = T(η)` and `p = w/Σw ∈ P(l,u)`.  Then `E_pφ ∈ R` and `E_p f = τ` if and
only if `w = u` on `{s > 0}`, `w = l` on `{s < 0}`, `E_pφ ∈ R` and `η·E_pφ = h_R(η)`.  Such a `p` exists if
and only if `τ = V⁺`, i.e. `η` is an optimal multiplier; the weights on `{s = 0}` are then fixed by the
last two conditions, not free.
(d) *Lower endpoint.*  Apply (a)–(c) to `−f`.
(e) *Inconsistency.*  With `t = η·φ − h_R(η)`: `I = ∅` if and only if there is `η` with
`min_{p∈P(l,u)} E_p t > 0`.  For `Z_l > 0` this is `Φ(η) := Σ_x [ l(x)t₊(x) − u(x)t₋(x) ] > 0`.  For
`l ≡ 0`, where `Φ ≤ 0` identically, it is `t > 0` on `supp u`.
(f) *Model-free limit.*  For `l ≡ 0`, `Ψ(τ,η) ≤ 0` reads `f − η·φ + h_R(η) ≤ τ` on `supp u`: the
classical dual of the generalised moment problem.

*Proof.*  (a) Let `p = w/Σw` be feasible.  Then `Σ w(f − τ) = Σ w s + Σw·(η·E_pφ − h_R(η)) ≤ Σ w s ≤
Σ[u s₊ − l s₋] ≤ 0`.  (b) `Ψ(τ, η) = max_{l≤w≤u} Σ w s_{τ,η}`, so `Ψ(τ, η) ≤ 0` if and only if
`E_p s_{τ,η} ≤ 0` for every `p ∈ P(l,u)`, i.e. `τ ≥ T(η)`; the maximum in `T` exists because `P(l,u)` is
compact.  The function `(p, η) ↦ E_p f − η·E_pφ + h_R(η)` is linear in `p` on the compact convex set
`P(l,u)`, and convex and lower semicontinuous in `η` on the convex cone `{h_R < ∞}`.  Sion's minimax
theorem gives `inf_η T(η) = max_{p∈P} inf_η[E_p f − η·E_pφ + h_R(η)]`, and `inf_η[h_R(η) − η·y]` is `0` if
`y ∈ R` and `−∞` otherwise (`R` closed and convex): the right-hand side is
`max{E_p f : p ∈ P, E_pφ ∈ R}`.  No hypothesis on `Z_l` and no monotonicity in `τ` is used.  (The first
version argued through the moment body and strict monotonicity in `τ`, which fails for `Z_l = 0`; this
argument is the referee's repair.)  (c) If `p` is feasible with `E_p f = τ = T(η)`, then
`0 = E_p(f − τ) = E_p s + (η·E_pφ − h_R(η)) ≤ E_p s ≤ 0`, so both inequalities are equalities:
`η·E_pφ = h_R(η)`, and `Σ w s = 0 = Ψ(τ, η)` is the maximum over the box, which forces `w = u` on
`{s > 0}` and `w = l` on `{s < 0}`.  The converse is the same computation read backwards.  If such a `p`
exists, `V⁺ ≥ E_p f = T(η) ≥ V⁺`; conversely, if `T(η) = V⁺`, a maximiser of `E_p f` over the compact
feasible set qualifies.  (e) The function `(p, η) ↦ η·E_pφ − h_R(η)` is linear in `p`, and concave and
upper semicontinuous in `η`; by Sion's theorem `min_p sup_η = sup_η min_p`, and `sup_η[η·y − h_R(η)]` is
`0` if `y ∈ R` and `+∞` otherwise.  So `I = ∅` if and only if `sup_η min_p E_p t = +∞`, which by positive
homogeneity in `η` means `min_p E_p t > 0` for some `η`.  For `Z_l > 0` every `w` in the box has positive
total and `min_w Σ w t = Φ(η)`; for `l ≡ 0`, `P(l,u)` is the set of probabilities on `supp u`.  (f) is
immediate.  ∎

*Counterexamples to the first version's (c) and (e), kept* (the referee's;
`experiments/eng/phase2_review/check_thm41.py`).  For (e): `X = {0,1}`, `l ≡ 0`, `u ≡ 1`, `φ = (0,1)`,
`R = [2,3]` — `I = ∅` although `Φ ≤ 0` everywhere.  For (c), which said that any weights on `{s = 0}`
attain the bound: `l ≡ 1`, `u ≡ 3` on three states, `f = (0, ½, 1)`, `φ = (0, 0, 1)`, `R = [0, ¼]`,
`V⁺ = 0.53125`; at the optimal pair `η = 0.625`, `τ = V⁺` the scores are `(−0.375, 0.125, 0)`, the third
state sits on `{s = 0}`, and exactly one value of its weight attains `V⁺` (the weight `l` gives
`E_p f = 0.5`; the weight `u` gives `E_pφ = 0.4286 ∉ R`).

*Remarks.*  (i) **This theorem is not new in the programme.**  With `m = 0` it is the threshold rule of
DeRobertis and Hartigan for intervals of measures, which the ensemble division gave to the science
division (ENSEMBLE-RES-0002 §4).  For exact data (`R` a point) parts (a)–(b) are the science division's
item 89(d) (`INFERENCE_LIMITS_ADDENDA.md` §(22): "`E_μψ ≤ t` whenever some `λ` has
`Σ u(ψ − t − λ·(Φ − m))₊ ≤ Σ l(ψ − t − λ·(Φ − m))₋`, with equality at the best `λ`").  The support
function of a convex error set and the Farkas certificate of infeasibility are the ensemble division's
E17.2 and F3 for the model-free case, which is (f).  What this statement adds is their union — regions
and the inconsistency certificate (e) for the box class — and a proof by one minimax argument.
Outside the programme it is classical in substance (§10).  (ii) The problem has `m + 1` unknowns whatever
`|X|` is; `X` enters only through sums of explicit functions.  (iii) `T` is convex, and its
subgradients at `η` are `∇h_R(η) − E_pφ` for the maximisers `p` of `E_p[f − η·φ]` over `P(l,u)` (weights
`u` on `{s_{T(η),η} > 0}`, `l` on `{s < 0}`, anything in between on the ties): at an optimal `η`, when one
exists, some maximiser has its measured averages at the boundary point of `R` exposed by `η`.
(iv) If certified bounds cross — an upper bound below a lower bound — then `I = ∅`.

## 5. Certification from samples: one function, no union bound

Let `π` be a probability on `X` from which one can sample, and let `L, U : X → [0, ∞)` be computable
with `l = c·π·L`, `u = c·π·U` for an unknown constant `c > 0` (so `u(x) > 0 ⇒ π(x) > 0`).  Then
`Ψ(τ, η) = c·E_π ψ_{τ,η}` with

    ψ_{τ,η}(x) = U(x)s₊(x) − L(x)s₋(x).

*Reference sampling*: `π ∝ w₀`, `L = e^{−ρ}`, `U = e^{ρ}`.  No normalising constant appears.
*Gap sampling* (S3's access model): `Ψ(τ, η) = λ·b + G·E_q[s₊]` with `λ = (h_R(η) − τ, −η, 1)`; the
certificate is `E_q[s₊ − c₀] ≤ 0` with the known constant `c₀ = −λ·b/G`.  Both are instances of "an
exactly known part plus one expectation".

(The gap distribution `q ∝ u − l` is the sampler of the theory division's Proposition 11.113, where it
serves another purpose: there the true energy is *evaluated* at every draw, and the output is a bracket
for the partition sum of that one known energy.  Here the energy is never evaluated — it is unknown —
and the output is a statement about every energy in the class.)

**Theorem 5.1 (sampled certificate) [P].**  Let `η`, a level `τ_min` and numbers
`0 ≤ λ_1, …, λ_J < 1/B` be fixed, where `B > 0` and `B ≥ sup_x ψ_{τ_min,η}(x)`; let `Y_1, …, Y_n` be independent
draws from `π`, independent of those choices.  Define

    W_n(τ) = (1/J) Σ_k Π_{j=1}^n (1 − λ_k·ψ_{τ,η}(Y_j)),      τ̂ = inf{τ ≥ τ_min : W_n(τ) ≥ 1/δ}.

Then `P(τ̂ < V⁺) ≤ δ`.  That is, `τ̂` is an upper bound for the whole identified set with probability
at least `1 − δ` — for every `n`, every dimension `m`, every choice of `η` and of the `λ_k`.

*Proof.*  `ψ_{τ,η}(x)` is non-increasing in `τ`, so every factor is positive for `τ ≥ τ_min` and
`W_n` is non-decreasing and continuous in `τ`.  Let `τ° = inf{τ ≥ τ_min : E_π ψ_{τ,η} ≤ 0}`; the set is
closed, so `E_π ψ_{τ°,η} ≤ 0` and `τ° ≥ V⁺` by Theorem 4.1(a).  If `τ° = τ_min`, every `τ̂ ≥ τ_min` is
valid.  Otherwise `E_π ψ_{τ°,η} = 0` by continuity, each product has expectation `Π(1 − λ_k·0) = 1`, so
`E W_n(τ°) = 1` and `P(W_n(τ°) ≥ 1/δ) ≤ δ` by Markov.  On the complement, monotonicity gives
`W_n(τ) < 1/δ` for all `τ ≤ τ°`, hence `τ̂ ≥ τ° ≥ V⁺`.  ∎

Only an **upper** bound `B` on `ψ` is needed; it comes from an a-priori bound on `U` (the envelope) and
on the ranges of `f` and `φ`.  If no such bound exists the procedure must abstain.  The same statement
with `−ψ` and Theorem 4.1(e) certifies inconsistency when `Z_l > 0`: fix `η`, test
`E_π[L t₊ − U t₋] > 0`.  For `l ≡ 0` no sample can certify inconsistency (an unsampled configuration may
have any `φ`); only the declared range of `φ` can, deterministically.

*The level is attained, so nothing may be chosen on the certification sample* (the referee's
experiments).  With `τ_min` just below `V⁺` and one bet near `1/B` the failure rate is 0.046 to 0.049 at
`δ = 0.05`; with `B` taken from the certification sample it is 0.37 to 0.98.  `η`, `τ_min`, the bets and
`B` must all be fixed before, or independently of, the draws that certify.

**Procedure.**  Split the sample.  On the first part solve the dual of §4 with the empirical measure
(any optimiser; only the quality of `η`, not soundness, depends on it).  The bets are fixed in advance
(the prototype: `0.9·2^{−k}/B`, `k = 0, …, 15`, with `τ_min` the lower end of the declared range of `f` —
simple and wasteful: a `τ_min` taken from the training part would shrink `B`).  On the second part
compute `τ̂` by bisection.  Do the same for the lower endpoint with `δ/2` each.

**Proposition 5.2 (what it costs: a first-order estimate, not a theorem).**  Let `μ = E_πψ < 0` and
`v = E_π ψ²` at the tested `(τ, η)`.  To first order a bet `λ ≤ 1/B` gives `ln W_n ≈ n(λ|μ| − λ²v/2)`.
*Free bet* (`|μ|/v ≤ 1/B`): `ln W_n ≈ nμ²/(2v)`, and the certificate fires at `n ≈ 2v·ln(1/δ)/μ²`.
*Capped bet* (`|μ|/v > 1/B`): the cost is `n ≈ B·ln(1/δ)/|μ|` up to a factor 2, which can exceed the
first formula by orders of magnitude.  For a uniform envelope (`L ≡ 1`, `U ≡ Γ`), scores bounded by `S`,
and an excess `α` over the root `T(η)` of the multiplier in use (which is `V⁺` only for an optimal `η`):
`|μ| ≥ α`, `v ≤ (Γ + 1)S²` and `B ≤ ΓS`, so

    n ≲ ln(1/δ)·max{ 2(Γ + 1)S²/α² ,  2ΓS/α }.

Both entries are upper estimates.  The prototype's mixture of 16 bets adds `ln 16` to `ln(1/δ)`.

*Derivation.*  `ln(1 − λz) = −λz − λ²z²/2 + O(λ³)`; maximise `λ|μ| − λ²v/2` over `λ ≤ 1/B`.  Whenever
`E_πψ ≤ 0`, `Γ E s₊ ≤ E s₋ ≤ S`, so `E ψ² ≤ ΓS·ΓE s₊ + S·E s₋ ≤ (Γ + 1)S²`; and `∂Ψ/∂τ ≤ −E_π L = −1`.  ∎
*Checked by the referee* in one family of instances: simulated over predicted cost 1.04 and 1.13 when
the bet is free; the free-bet formula alone is too optimistic by factors 2.8, 22, 254 and 267 when the
bet is capped (the first version presented the cap as a correction term).

**5.3 Comparison with S3 at equal certified accuracy.**  S3 needs `L = 8(Γ−1)²κ⁻²[d ln(1 +
16(Γ−1)/κ) + ln(2/δ)]` draws for an allowance `κ` — quadratic in `Γ`, linear in `d` — and then widens
the region as well (Proposition 2.5).  Theorem 5.1 needs at most about `2(Γ+1)S² ln(1/δ)/α²` for a given
multiplier: linear in `Γ`, with no `d` in the formula — but `α` is measured from the root `T(η)` of the
fitted multiplier, whose distance to `V⁺` grows with `m` at a fixed training size, and the comparison
is between a sufficient condition and a first-order estimate.  The reason for the factor `Γ`: S3
controls the body to `εG` in every direction, whereas
at the optimum the gap term satisfies `G·E_q s₊ = −λ·b ≤ Z_l·S`, i.e. it is of the order of `Z_l`, and a
variance-sensitive test of that one direction sees a variance of order `E_q s₊`, not 1.  Measured:
`RESULTS.md` (hypotheses H-A, H-B).

**5.4 Draws from the extremal ensemble: the envelope ratio does not enter.**  (Observed by the referee,
`REVIEW_A.md` finding M1(a); stated and proved here; implemented as `certify_upper_tilted`.)

Fix `η` and a pilot level `τ₀`.  The **extremal ensemble at the pilot** is `p₀ ∝ ω₀` with `ω₀ = u` on
`{s_{τ₀,η} > 0}` and `ω₀ = l` elsewhere: a member of `P(l,u)` (if `Σω₀ > 0`); with energies, the Boltzmann
weight of `E_min` on `{s_{τ₀,η} > 0}` and of `E_max` elsewhere.  For `τ ≥ τ₀` put

    ψ̃_τ(x) = s_{τ,η}(x)                 if s_{τ,η}(x) > 0  or  s_{τ₀,η}(x) ≤ 0,
    ψ̃_τ(x) = (l(x)/u(x))·s_{τ,η}(x)     if s_{τ,η}(x) ≤ 0 < s_{τ₀,η}(x).

**Theorem 5.4 [P].**  (i) `Ψ(τ, η) = (Σω₀)·E_{p₀}ψ̃_τ` for every `τ ≥ τ₀`.  (ii) `ψ̃_τ(x)` is non-increasing
in `τ`, and `ψ̃_τ ≤ (s_{τ₀,η})₊`.  Hence Theorem 5.1 holds verbatim with draws `Y_j` from `p₀`, `ψ̃` in
place of `ψ`, `τ_min = τ₀` and any `B ≥ sup_x (s_{τ₀,η}(x))₊`, `B > 0`: `τ̂ = inf{τ ≥ τ₀ : W_n(τ) ≥ 1/δ}`
satisfies `P(τ̂ < V⁺) ≤ δ`, whatever the pilot.  (iii) If `Z_l > 0`, then for `τ ≥ max(τ₀, T(η))`,
`E_{p₀}ψ̃_τ ≤ −(τ − T(η))·Σω_τ/Σω₀`, with `ω_τ` the extremal weight at level `τ`; in particular
`E_{p₀}ψ̃_{τ₀} ≤ −(τ₀ − T(η))` when the pilot is above the root.

*Proof.*  (i) On `{s_{τ₀} > 0}`, `ω₀ψ̃_τ` is `u·s_τ` where `s_τ > 0` and `l·s_τ` where `s_τ ≤ 0`; on
`{s_{τ₀} ≤ 0}`, `s_τ ≤ 0` and `ω₀ψ̃_τ = l·s_τ`.  In every case it is `u(s_τ)₊ − l(s_τ)₋`.  (ii) Both
branches are non-increasing in `τ` and agree at `s_τ = 0`; and `ψ̃_τ ≤ (s_τ)₊ ≤ (s_{τ₀})₊`.  The proof of
Theorem 5.1 uses only that the tested variable is non-increasing in `τ`, bounded above by `B` at
`τ_min`, and has an expectation of the sign of `Ψ`.  (iii) `Ψ(·, η)` is convex, vanishes at `T(η)`, and
`−Σω_τ` is a subgradient at `τ`; so `0 = Ψ(T(η)) ≥ Ψ(τ) + (τ − T(η))·Σω_τ`.  ∎

*What it buys.*  The tested variable is bounded by the range `S` of the score — no bound on `U` is
declared — and has variance at most `S²`; with a pilot at an excess `α` above the root its mean is at
most `−α`.  To first order the certificate fires at the pilot with `n ≈ 2S²·ln(1/δ)/α²` draws: **no
`Γ`**.  On the hard instance of Theorem 6.1(a) the referee measured the least `n` with a median excess
below 0.05: 2 240, 19 456, 221 184, 2 031 616 draws from `π` for `Γ = 10, 10², 10³, 10⁴`, against 896,
928, 928, 896 draws from `p₀`.  Theorem 6.1 is not contradicted: its procedures draw from `π` or `q`.

*What it costs.*  (1) **A sampler for `p₀`.**  It is a Boltzmann weight, so any sampler for the
reference applies to the modified energy; but the energy jumps by `ln(u/l)` across the surface
`{s_{τ₀,η} = 0}`, an exact sampler built by rejection from `π` costs up to `Γ` proposals per draw (in
agreement with Theorem 6.1), and for dependent draws nothing is certified (§7.3).  (2) **A pilot.**  The
bound cannot be below `τ₀`, and above a pilot that is too low the drift is diluted by `Σω_τ/Σω₀`.  A
pilot from reference draws has an error of the order of Theorem 5.1's own, so the gain needs the pilot
to be refined with draws from the extremal ensemble itself (the estimate `tilted_root`); every choice
must be made on draws other than those that certify.  (3) For `l ≡ 0` the test has no power: under `p₀`
the tested variable is non-negative.  Measured on the validation families with exact samplers:
`RESULTS.md`, supplementary experiment S1 (not pre-registered).

## 6. With reference or gap draws, a cost proportional to the envelope ratio is unavoidable

**Theorem 6.1 (lower bound for a prescribed sampling law) [P].**  Let `Γ ≥ 4`, `δ < 1/4`.  Consider
procedures whose only information about the instance, beyond what is named below, is `n` independent
draws from a prescribed law together with the values of `f`, `L` and `U` at the drawn configurations —
they cannot evaluate weights at configurations of their choice, enumerate, or draw from another law —
and which output `τ̂` with `P(V⁺ ≤ τ̂ ≤ V⁺ + α) ≥ 1 − δ` on every instance with envelope ratio `Γ`, no
observations, and a target with values in `[0,1]`.
(a) If the procedure knows `f` and `Γ` and the law is the reference `π`, then
`n ≥ Γ·ln(1/(4δ))/(72α²)` for `α < 1/6`.
(b) If in addition it is given `b`, `G` and `Z_l` exactly and the law is the gap distribution — S3's
access model — then `n ≥ Γ·ln(1/(4δ))/(2304α²)` for `α < 1/48`.

*Proof.*  (a) `X = {0,1}`, `f(x) = x`, `π(1) = a`, `L ≡ 1`, `U ≡ Γ`: `V⁺(a) = Γa/(1 + (Γ−1)a)`.  With
`a₀ = 1/Γ`, `a₁ = (1+θ)/Γ`, `θ ∈ (0,1]`: `V⁺(a₁) − V⁺(a₀) = Γ²θ/[(2Γ−1)(2Γ−1+θ(Γ−1))] ≥ θ/6`.  If
`θ > 6α`, the event `{τ̂ ≥ V⁺(a₁)}` has probability at least `1 − δ` under `a₁` and at most `δ` under
`a₀`.  By the Bretagnolle–Huber inequality, `2δ ≥ ½·exp(−n·KL(Bern(a₀)‖Bern(a₁)))`, and
`KL ≤ χ² = (θ/Γ)²/(a₁(1−a₁)) ≤ 2θ²/Γ`.  Let `θ ↓ 6α`.
(b) `X = {0,1,2}`, `f = (0, ½, 1)`, `m = 1/Γ`, `π_t = (1 − 2m + t, 2(m − t), t)` for `t ∈ [0, m/2]`.
`E_{π_t} f = m` for every `t`, so `b ∝ (1, m)`, `G` and `Z_l` do not depend on `t`, and `q = π_t`.  For
`t ≤ (Γ−2)/(Γ(Γ−1))`, which contains `[0, m/2]`, the optimal threshold up-weights `{½, 1}` and
`V⁺(t) = 1/(1 + (Γ−1)(2/Γ − t))`.  With `t₀ = 1/(4Γ)`, `t₁ = (1+θ)t₀`:
`V⁺(t₁) − V⁺(t₀) ≥ (Γ−1)θt₀/9 ≥ θ/48`, and `χ²(π_{t₀}‖π_{t₁}) ≤ θ²t₀(2 + 2t₀) ≤ θ²/Γ`.  Conclude as in
(a) with `θ ↓ 48α`.  ∎

*The access model matters* (the referee's findings M1 and M2).  On these two- and three-point instances
one evaluation of `l`, or two of the unnormalised reference, reveals the parameter: the theorem is about
what draws from `π` or `q` alone can certify.  (The atoms stand for cells of many configurations of
equal weight whose cardinalities carry the parameter; then evaluations at the drawn configurations tell
nothing more, and `b`, `G`, `Z_l` are unchanged.  That version is not written out.)  And the theorem is a
worst case over instances for one sampling law: it says nothing about a given instance, and nothing
about draws from another law — Theorem 5.4 certifies these very instances with no `Γ`.

**Consequences.**  (0) This is the counterpart, for an interval of an average under an unknown energy,
of the theory division's lower bounds for the partition sum of a known one (its Proposition 11.113(d):
order `sinh²(Δ/2)/ε²`, which is `Γ/(4ε²)` for an envelope of width `Δ = 2ρ`; Theorem 11.110(d)).
(i) For reference draws the linear dependence on `Γ` in Proposition 5.2 is optimal up to constants.
(ii) Exact knowledge of `b`, `G`, `Z_l` does not change the rate of gap sampling.  (iii) For an energy
envelope of half-width `ρ`, `Γ = e^{2ρ}`.  If the residual is extensive, `ρ = n·ρ₁`, certification *from
reference draws* costs `e^{2nρ₁}` in the worst case, more than enumerating a space of `q^n` states as
soon as `ρ₁ > ½ ln q` (0.35 kT per binary site).  This is not a statement about every instance: on the
instance of §9.4 two hundred reference draws certify the box's bound for `Γ` up to `10¹³` (the referee's
computation) — a bound that is useless because it is nearly trivial, not because it is expensive.
(iv) In the model-free case `Γ = ∞`: **no finite sample, from any law, certifies anything about
unsampled configurations.**  A linear programme over a sampled pool is a statement about that pool only.  The
ensemble division's E30 says the same from the other side — its verdicts are not stable when the pool
is refined, and its outer interval on a net needs a Lipschitz constant of the observables in
configuration space; its E28 bounds the weight an incomplete library can be missing.  An energy
envelope with finite `Γ` is the assumption that turns a pool into a statement about the population.

## 7. Propagating uncertainty in the inputs

**7.1 Envelopes.**  `P(l,u) ⊂ P(l',u')` whenever `l' ≤ l` and `u ≤ u'`.  If only enclosures
`l ∈ [l⁻, l⁺]`, `u ∈ [u⁻, u⁺]` are known, run every certificate with `(l⁻, u⁺)`.  Rounding is handled the
same way in principle: evaluate the certificate sums in interval arithmetic and decide on the upper end.
*What the prototype does:* its population sums (`psi`, `tau_root`, `interval`, the lumped and the
site-wise computations) are plain floating point — so the "exact" intervals of the validation are
floating-point values — and its one rigorous-arithmetic step is the optional confirmation of the
validation wealth (`rigorous=True`), which decides on a rigorous lower bound of the wealth.  (The first
version said "ball arithmetic" without this qualification.)

**7.2 `b`, `G`, `Z_l` (gap sampling only).**  With `b ∈ [b⁻, b⁺]` componentwise and `G ≤ G⁺`,
`Ψ ≤ Σ_i max(λ_i b_i⁻, λ_i b_i⁺) + G⁺·E_q s₊`; certify the right-hand side.  If `b` itself is estimated
from a sample of `p_l ∝ l`, a second test and a split of `δ` are needed.  Reference sampling needs
neither — the reason to prefer it whenever a reference exists.  (Implemented after the review for a
componentwise enclosure of `b` and an upper bound of `G` — the arguments `b_hi`, `G_hi` of the gap
certificate, which tests `s₊ + sup_b λ·b / G⁺`; the second test for a `b` estimated from a sample is not
implemented.)

**7.3 Approximate sampling.**  If the sampler's law `π'` satisfies `π'/π ∈ [1/β, β]`, replace `(L, U)`
by `(L/β, βU)`.  If only `‖π' − π‖_TV ≤ ε_TV` is known, then
`E_πψ_τ ≤ E_{π'}ψ_τ + ε_TV·(sup_x ψ_τ − inf_x ψ_τ)`; because Theorem 5.1 needs the tested function to be
non-increasing in `τ`, the allowance must be *one constant*: fix a bracket `[τ_min, τ_max]` in advance,
add to `ψ_τ` a bound of `ε_TV·(sup ψ_τ − inf ψ_τ)` valid on the whole bracket, and restrict `τ̂` to the
bracket (the prototype: the declared range of `f`).  The first version added the range at each `τ`,
which is neither monotone nor bounded (finding M6).  If the draws are dependent (Markov chain Monte Carlo) and no certified mixing bound is
available, Theorem 5.1 does not apply and the prototype **abstains**; exact samplers exist for product,
chain and tree references.

**7.4 Observables.**  An evaluation error `|φ̃ − φ| ≤ e_φ` enlarges `R` by `e_φ`; an error on `f` is
added to the interval.  Ranges of `f`, `φ` and a bound on `U` must be declared: they define `B`.  A
sampled value outside the declared bounds voids the certificate (reported, not ignored).

**7.5 `G = 0` and partial degeneracy.**  If `l = u` the class is one ensemble, `K = {b}`, `q` is
undefined and S3 has no content.  In §5, `ψ = L·s` and the certificate is an ordinary one-sided test of
`E_{p_l} s ≤ 0`: a confidence interval for one ensemble average, with the observations acting as
control variates through `η`.  If `g = 0` only on part of `X`, gap sampling never visits that part and
relies on `b` for it; reference sampling treats all configurations alike.  (The prototype's gap
certificate returns the exact value `b_f/b_0` for `G = 0`; its S3 routine abstains.)

**7.6 The gap distribution.**  Its limitations, collected: it needs (H2); its worst-case rate is the
same as the reference's (Theorem 6.1(b)), and both lose to draws from the extremal ensemble (Theorem
5.4); when `u/l` varies it concentrates on the most uncertain configurations,
which need not be those that decide the query; and it does not exist for `G = 0`.  Its one advantage:
the exactly known linear part `λ·b` acts as a control variate, so only `s₊` is sampled.

## 8. Deterministic alternatives and structure

**Proposition 8.1 (lumping) [P].**  If `(φ, f)` takes the same value on each cell of a partition
`X = ⊔_c X_c`, then `K = b + Σ_c g(X_c)·[0, v_c]`: the problem on `X` is the problem on the cells, with
`l` and `u` summed over each cell.  Hence, whenever cell sums of `l` and `u` are computable — level
counts of additive, lattice-valued observables for product, chain or tree references, by convolution
or transfer matrices — the identified interval is computed **exactly**, without sampling, in time
polynomial in the number of cells.  (Implemented for product references.)

*Proof.*  Generators with equal direction add.  ∎

*Limits.*  Counting configurations by the value of a sum with arbitrary real coefficients is
`#P`-hard (it contains counting knapsack solutions); the proposition is useful for lattice-valued
observables with polynomially many levels, and it does not apply to observables that are not sums over
the tractable structure (distances, scattering intensities), for which §5 is the tool.

**Other directions examined.**  *Adaptive sampling*: the variance of `ψ` is minimised by a proposal
proportional to `|u s₊ − l s₋|`; the two-stage scheme — a pilot, then draws from the extremal ensemble
at the pilot — is Theorem 5.4 (sound by §5 itself with the tilted law as reference; implemented).  *Low rank*: the dependence on `X` is through the law of
the `(m+3)`-vector `(L, U, φ, f)` under `π`; nothing else is used.  *Parametric envelopes*
(`E = E₀ + Σ_k θ_k h_k`, `θ` in a box) are not rectangular; their box hull is sound and can be very
loose; §9 treats the most important structured case.

## 9. Beyond boxes: ratio-constrained classes and bounded influence

The box class lets `w(x)` vary independently at every `x`.  Energies of physical models do not: a
residual that changes by at most `u₁` when one site changes (the theory division's class `L_u` of
`u`-Lipschitz residuals on the cube; bounded influence) forces `w(x)/w₀(x) ≤ e^{u₁}·w(y)/w₀(y)` for
neighbours `x, y`.  These constraints are **linear in the weights**.

**All of this structure is the theory division's.**  Its Theorem 11.12 (machine-checked) states that in
the weights the class is the polyhedral cone `w(y) ≤ e^{d(x,y)}w(x)`, "so robust Boltzmann averages of
any observable are linear-fractional programs"; its Theorem 11.105 gives, for the largest ratio
`Z(A)/Z(B)` of two set weights over an envelope class with the triangle inequality, the "transport
with gains" dual, with weak duality machine-checked, and names flows with gains (Jewell 1962) and the
metric form of differential privacy as the known neighbours.  The science division's item 89(a) notes
that the box is the class of a "hub" metric.  Theorem 9.1 below is Theorem 11.105 applied to the
measure `π·|s|` with `A = {s > 0}`, `B = {s < 0}` — it is stated for a general graph and for a signed
score because that is the form the multipliers of §4 need.  Proposition 9.5 is the science division's
machine-checked stochastic sandwich.  Proposition 9.7 rests on an inequality the theory division sent
during Phase II (THY-MSG-0023).  Propositions 9.2, 9.4, 9.6 and Corollary 9.3 were not found in
the archive; the theory report says of closed forms that they are "special to single states".

**Definition.**  Let `π > 0` on `X`, `E` a set of ordered pairs, `C_{xy} > 0` for `(x,y) ∈ E`.  The
**ratio-constrained class** is `𝒞 = {r ≥ 0 : r(x) ≤ C_{xy}·r(y) for (x,y) ∈ E}`, a polyhedral cone, with
ensembles `p ∝ π·r`.  With `C_{xy} = e^{c(x,y)}` this says that the residual energy `−ln r` is
`c`-Lipschitz.  The box class is the star: one extra node `*` with `r(x) ≤ U(x)r(*)` and
`r(*) ≤ r(x)/L(x)`.  Intersections of classes are unions of edge sets.

**Theorem 9.1 (flow duality) [P].**  Let `a : X → ℝ`.  Then `Σ_x a(x)r(x) ≤ 0` for all `r ∈ 𝒞` if and
only if there is a flow `θ : E → [0, ∞)` with

    a(x) ≤ Σ_{y:(x,y)∈E} θ_{xy} − Σ_{y:(y,x)∈E} C_{yx}·θ_{yx}        for every x.

Consequently, with `a = π·s_{τ,η}`: `E_p f ≤ τ` for every `p` in the class with `E_pφ ∈ R` as soon as
such a flow exists for some `η`; and if `I ≠ ∅`, `V⁺` is the infimum of the `τ` for which one exists.
(The normalised class `{r ∈ 𝒞 : Σπr = 1}` is compact because `π > 0`, whatever `E` is; a hypothesis is
needed only for the star, whose extra node has reference weight zero.)

*Proof.*  `𝒞 = {r : −r ≤ 0, Ar ≤ 0}` with rows `e_x − C_{xy}e_y`.  By Farkas' lemma the cone of vectors
`a` with `a·r ≤ 0` on `𝒞` is `{Aᵀθ − ν : θ, ν ≥ 0}`, and `(Aᵀθ)(x)` is the right-hand side.  The
second part is Theorem 4.1 with `K` replaced by `{Σ_x π(x)r(x)v(x) : r ∈ 𝒞}`; Sion's theorem applies on
the compact convex set `{r ∈ 𝒞 : Σπr = 1}`.  ∎

*Reading.*  Positive mass `a₊` must be shipped to where `a` is negative; a unit shipped along `(x,y)`
arrives as `C_{xy}` units.  For the star this is `Σ[U a₊ − L a₋] ≤ 0`: Theorem 4.1.  For a metric
class it is a transport problem with multiplicative cost `e^{c(x,y)}`.

**Proposition 9.2 (closure under marginalisation) [P].**  Let `X = Π_i X_i`, `π = ⊗π_i`, and let `𝒞_u` be
the class of `r` with `r(x) ≤ e^{u_i}r(x')` whenever `x, x'` differ only at site `i` (`u_i ≥ 0`).  For every set
`B` of sites, the set of `B`-marginals of the ensembles of `𝒞_u` is exactly the class of the same kind
on `Π_{i∈B} X_i` with reference `⊗_{i∈B}π_i`.

*Proof.*  The `B`-marginal of `π r` is `π_B·r̄` with `r̄(x_B) = Σ_z π_{B^c}(z)r(x_B, z)`, and averaging
the inequalities `r(x_B, z) ≤ e^{u_i}r(x'_B, z)` over `z` preserves them.  Conversely a function of
`x_B` in the small class is in `𝒞_u`.  ∎

(For a reference that is not a product the averaging uses different conditional laws for `x_B` and
`x'_B`, and the statement fails; §12.)

**Corollary 9.3 (additive observables: exact at any size) [P].**  In the setting of Proposition 9.2
let `φ(x) = Σ_i φ_i(x_i)` and `f(x) = Σ_i f_i(x_i)`.  Then

    V⁺ = inf_η [ h_R(η) + Σ_i D_i⁺(f_i − η·φ_i) ],     D_i⁺(g) = max{E_{p_i} g : p_i ∝ π_i r_i, max r_i/min r_i ≤ e^{u_i}},

and each `D_i⁺` is a threshold rule on `|X_i|` states.  For binary sites the achievable one-site
marginals are `p_i(1) ∈ [σ(θ_i − u_i), σ(θ_i + u_i)]`, `θ_i = logit π_i(1)`, independently over `i`.

*Proof.*  The averages depend on the one-site marginals only.  By Proposition 9.2 each lies in the
one-site class, which is a box class with ratio `e^{u_i}` (on one site all states are neighbours); and
every tuple of such marginals is realised by the product `r(x) = Π r_i(x_i)`, which is in `𝒞_u`.  So the
problem is a convex programme over a product of one-site polytopes; its Lagrangian separates, and
Sion's theorem gives the formula.  ∎

**Proposition 9.5 (monotone targets: the science division's stochastic sandwich) [in the archive,
machine-checked].**  For binary sites, every ensemble of the class lies, in the stochastic order,
between the two product measures `ν_−`, `ν_+` with one-site odds `e^{θ_i − u_i}` and `e^{θ_i + u_i}`,
both of which belong to the class.  Hence for every target `g` that is monotone in each coordinate the
identified interval without data is exactly `[E_{ν_−}g, E_{ν_+}g]`; relabelling the two states of a
site covers targets that increase in some coordinates and decrease in others.  This is the science
division's Theorem A11 (theory report Theorem 11.106a; `proofs/Frontiers/MonotoneSandwich.lean`,
`cube_sandwich_mean`, `cube_mean_range_eq_Icc`), proved there by Holley's inequality for a submodular
known part; for a product reference it also follows from the one-site bound
`p(x_i = 1 | x_{−i}) ≤ σ(θ_i + u_i)` and a sequential coupling.
**Consequence for certification.**  For a monotone score the certificate `sup_p E_p s ≤ 0` is one
expectation under a product measure, estimated by ordinary Monte Carlo: no envelope ratio enters, at
any system size.  A score with active multipliers is in general not monotone (it is a difference of
monotone functions), so this settles the first open problem of §12 for monotone scores only.

**Proposition 9.6 (sequential bound; functions of a few additive statistics) [P; N].**  In the setting
of Proposition 9.2, for every `g`,

    sup_{p ∈ 𝒞_u} E_p g  ≤  SEQ(g) := T_1 T_2 ⋯ T_n g,        (T_i g)(x_{<i}) = D_i⁺( g(x_{<i}, ·) ),

with `D_i⁺` the one-site threshold rule of Corollary 9.3; hence `V⁺ ≤ inf_η [h_R(η) + SEQ(f − η·φ)]`.
If `g` depends on `x` through a vector of additive lattice-valued statistics, so does each
`T_i ⋯ T_n g` through the partial sums, and `SEQ(g)` is computed by dynamic programming in time
(sites × cells × states), at any number of sites, without sampling.  Equality holds for additive `g`,
and — on sites with two states — for coordinatewise monotone `g`.

*Proof.*  As in Proposition 9.2, the conditional law under `p` of `x_i` given `x_{<i}` is
`π_i·r̄` with `r̄(a) = Σ_z π_{>i}(z)·r(x_{<i}, a, z)`, whose ratio is at most `e^{u_i}`: it lies in the
one-site class.  So `E_p[g | x_{<n}] ≤ (T_n g)(x_{<n})`, and induction over the sites gives the bound.
For additive `g` every `T_i` acts on its own term; for monotone `g` on binary sites the maximising
thresholds are those of `ν_+`, whatever the earlier coordinates.  ∎

*Counterexample to the first version, which claimed equality for monotone `g` on any sites* (the
referee's, finding C3; kept as a test).  Two sites with three ordered states, site laws
`(0.0401, 0.5001, 0.4598)` and `(0.3815, 0.4694, 0.1491)`, slopes `(1.0038, 1.0722)`,
`g = 1{x₁ + x₂ ≥ 3}`: the supremum over the class is `0.632638`, `SEQ(g) = 0.671526`, and `0.634084` with
the sites in the other order.  With three states the maximising one-site threshold (up-weight the top
state, or the top two) depends on the earlier coordinates, and the extremal sequential ensemble leaves
the class.

The bound is the exact value for a larger class — all ensembles whose one-step conditionals lie in the
one-site classes — and is therefore not tight in general.  Measured against the exact programme on a
cube of ten sites, two slopes, five targets, with and without one measured average
(`experiments/eng/phase2_seq/`, twenty cases): exact for the monotone, the additive and the
bi-monotone target without data; in the other cases an interval 1.13 to 1.40 times as wide as the
exact one; sound in every case.  These factors describe the cases tried, not the bound: the referee
found 1.44 for parity on eight sites, 1.84 for a random function of one statistic on six, and 3.97 for
a random target on at most five.

**9.4 Exponential separation from the box class [P].**  Uniform cube, `π_i = ½`, slope `u` at every
site, target `f = x_1`, no observations.  Bounded-influence class: `V⁺ = σ(u)`, for every `n`.  Every
box class containing it has ratio at least `e^{un}` (a box needs `U(x) ≥ e^{un}L(x̄)` for antipodal
`x, x̄`, so `U(x)U(x̄) ≥ e^{2un}L(x)L(x̄)`), and for the uniform box of that ratio — as for the box
centred at a configuration — `V⁺ = e^{un}/(1 + e^{un})`: within `e^{−un}` of the trivial bound 1.  More is true (the referee's observation): **every** box class containing the
bounded-influence class has `V⁺ ≥ e^{un}/(1 + e^{un})`.  Indeed containment forces
`U(x) ≥ e^{u·d(x,y)}L(y)` for all `x, y` (test with `r = e^{−u·d(x,·)}`); with `A = {x₁ = 1}` and the
antipode `x̄ ∈ A^c` of `x ∈ A`, `Σ_{x∈A}U(x) ≥ e^{un}Σ_{x∈A}L(x̄) = e^{un}Σ_{y∈A^c}L(y)`, and
`V⁺ = u(A)/(u(A) + l(A^c))`.  S3 applied to envelopes derived from a bounded-influence class therefore
discards essentially all the information in the class — whatever is sampled.  (The first version added
that a sampled certificate over that box "needs `e^{un}` draws".  That was false: on this instance
`π(f = 1) = ½`, and reference draws certify the nearly trivial bound cheaply.)

**Proposition 9.4 (local transport plus a global remainder) [P].**  Let `r` be in a ratio-constrained
class and also satisfy `max r/min r ≤ Γ_glob`.  Let `Q(x, ·)` be any kernel — a probability for every
`x` with `s(x) > 0` — that moves such a configuration along edges, with path constant
`C(x,y) ≥ r(x)/r(y)`, and put

    β(y) = Σ_x π(x)s₊(x)Q(x,y)C(x,y) − π(y)s₋(y).

Then `Σ π r s ≤ 0` whenever `Σ_y [Γ_glob·β₊(y) − β₋(y)] ≤ 0`.  If each `y` has enumerable preimages
under `Q`, `β(y)/π(y)` is computable at a sampled `y` and the condition is one expectation under `π`:
Theorem 5.1 applies.

*Proof.*  `Σ_x π r s₊ = Σ_{x,y} π(x)r(x)s₊(x)Q(x,y) ≤ Σ_y r(y)Σ_x π(x)s₊(x)Q(x,y)C(x,y)`, so
`Σ π r s ≤ Σ_y r(y)β(y) ≤ max r·Σβ₊ − min r·Σβ₋`.  ∎

*Limit of this proposition.*  The remainder pays `Γ_glob`.  For a pure bounded-influence class on `n`
sites `Γ_glob = e^{un}`, and with reference draws the remainder then costs `e^{un}` in the worst case
(Theorem 6.1): the transport must cancel all positive mass identically, which is an analytic statement
(as in Corollary 9.3), not a sampled one.  Draws from the extremal ensemble (Theorem 5.4) would avoid
the ratio, but for a metric class that ensemble is explicit only for monotone scores (Proposition 9.5);
in general it is the solution of the transport problem itself.  Sampled certificates for metric
classes are therefore available today only for monotone scores, or when a moderate global ratio is
also assumed.  This is the main open problem (§12).

**Proposition 9.7 (references that are not products: a sound outer bound) [P; the inequality is the
theory division's, THY-MSG-0023 §3(2)].**  Let `π` be any positive reference on `X = Π_i X_i`, and let
`κ_i ≥ 0` satisfy `π(z | x_i = a) ≤ e^{κ_i}·π(z | x_i = a')` for all states `a, a'` of site `i` and all
configurations `z` of the other sites.  Then for every `p ∝ π·r` with `r ∈ 𝒞_u` the one-site marginal is
`p_i = π_i·r̄_i` with `max r̄_i/min r̄_i ≤ e^{u_i + κ_i}`, where `π_i` is the one-site marginal of the
reference.  Hence, for additive `f` and `φ`,

    V⁺ ≤ inf_η [ h_R(η) + Σ_i D_i⁺(f_i − η·φ_i) ],     D_i⁺ over the one-site class of ratio e^{u_i + κ_i} around π_i:

a sound outer bound, computed as in Corollary 9.3 from the one-site marginals of the reference, which
are ordinary averages under the reference.  For a Gibbs reference `π ∝ e^{−E₀}`,
`κ_i ≤ max_{a,a'} osc_z [E₀(a, z) − E₀(a', z)]`.

*Proof.*  `r̄_i(a) = Σ_z π(z | x_i = a)·r(a, z) ≤ Σ_z e^{κ_i}π(z | x_i = a')·e^{u_i}r(a', z) = e^{u_i + κ_i}·r̄_i(a')`.
The bound follows as in Corollary 9.3, except that a tuple of one-site marginals need no longer be
realised jointly: it is an outer bound, not the identified end.  For the Gibbs form,
`π(z|a)/π(z|a') = e^{−D(z)}/E_{π(·|a')}e^{−D}` with `D(z) = E₀(a, z) − E₀(a', z)`.  ∎

The constant is a pointwise bound on the interaction across the cut, so the bound degrades quickly
with the coupling: for an Ising ring with coupling `J` it is `κ_i = 8|J|` in the worst case.  Measured
against the exact programme on rings of ten sites: `RESULTS.md`, supplementary experiment S2.

## 10. Relation to the literature

From a bounded search by a subagent (`experiments/eng/phase2_digest/PRIOR_ART_WEB.md`; 52 queries, about
12 pages opened, no full text read; entries marked there as opened / index-only / unverified).  None of
the references was read in full by this division.

| statement here | closest known | judgement |
|---|---|---|
| Proposition 2.1 (zonotope, support function) | lift zonoids (Koshevoy–Mosler); moments of bounded densities, the Markov `L`-problem (Akhiezer–Krein; Krein–Nudelman); Lyapunov's convexity theorem | classical |
| Theorems 2.2, 3.1 (random zonotope, additive `ℓ∞` error) | laws of large numbers and `√n` rates for averages of random sets through support functions (e.g. Beresteanu–Molinari); multiplicative approximation of zonoids (Bourgain–Lindenstrauss–Milman; Talagrand; Cohen–Peng) | routine empirical-process bounds; weaker than the multiplicative results, which need another sampling law |
| Theorem 4.1 (dual with moment constraints) | generalised Neyman–Pearson lemma (Dantzig–Wald); intervals of measures (DeRobertis–Hartigan); linearisation of ratios (Wasserman–Lavine–Wolpert); the marginal sensitivity model with balancing constraints (Zhao–Small–Bhattacharya; Dorn–Guo); CVaR | classical structure; the combined statement was not found verbatim and is a routine corollary |
| Theorem 5.1 (validation-sample certificate with a product test) | Monte Carlo bounding of stochastic programmes (Mak–Morton–Wood; Bayraksan–Morton), there with CLT intervals; betting confidence bounds (Waudby-Smith–Ramdas); inference for sharp sensitivity bounds is asymptotic | a known recipe applied to a new target; the monotonicity argument that removes the union bound over `τ` was not found |
| Theorem 6.1 (cost `∝ Γ` for reference or gap draws) | — | not found; a standard two-point argument |
| Theorem 5.4 (draws from the extremal ensemble) | least-favourable distributions in robust testing (Huber–Strassen); importance sampling with a tilted or umbrella law | the principle is classical; this use was not searched for (added after the review) |
| Theorem 9.1 (flow duality) | the theory division's Theorem 11.105 (in the archive; its own search found the general duality "not found in six searches at summary level"); generalised flows (Jewell); metric differential privacy | in the archive; a corollary |
| Proposition 9.2, Corollary 9.3 (closure; additive observables) | closure of metric differential privacy under post-processing is the same inequality | not found for partial identification; the proofs are two lines each |
| Proposition 9.5 (monotone targets) | the science division's Theorem A11 (Holley's inequality), machine-checked | in the archive |
| Proposition 9.6 (sequential bound) | nested one-step robust expectations are the dynamic programming of robust Markov decision processes with rectangular uncertainty | a known device applied here; not searched |
| Proposition 9.7 (references that are not products) | the theory division's marginalisation inequality (THY-MSG-0023, Phase II) | theirs; the use for additive observables is immediate |
| the application (energy envelope + averaged data → guaranteed interval or inconsistency) | "maximum occurrence" of a conformation given averaged data (Bertini et al.), without energies; bounds on Gibbs averages in a Kullback–Leibler ball (Katsoulakis, Rey-Bellet and co-authors), without data; maximum-entropy, BioEn, BME, metainference: one ensemble or a posterior, not a set | not found |

## 11. What is demonstrated, and what is not

* Demonstrated (proofs here, each checked numerically by the referee's independent code; the measured
  comparisons are in `RESULTS.md` and are not repeated here): S3 holds under (H1)–(H5); Theorem 5.1 gives
  a valid bound at every sample size, dimension and choice of multipliers; with reference or gap draws
  a cost proportional to `Γ` cannot be avoided in the worst case, and with draws from the extremal
  ensemble it is absent; for bounded-influence classes with product references and additive observables
  the identified interval is exact at any size.
* Demonstrated only on enumerable instances with exact samplers: everything statistical.  No certified
  statement is available for dependent draws (the prototype abstains), and the extremal ensemble of
  Theorem 5.4 has been sampled exactly, never by a Markov chain.
* Not demonstrated: any statement about a molecule.  An identified interval is exactly as good as its
  envelope, and no envelope between a force field and nature is known; the archive's own measurements
  put the residual of one implicit-solvent term at 12–53 kT per site, for which every interval here is
  vacuous.  The classes for which envelopes *are* rigorous are differences between two models (a
  truncated and a full energy; two parameter sets), i.e. statements about a model.

## 12. Open problems, in order of value

1. **Sampled certificates for bounded-influence classes without a global ratio.**  Settled for
   monotone scores by the stochastic sandwich (Proposition 9.5), and for functions of a few additive
   statistics there is the deterministic outer bound of Proposition 9.6.  Open for a general score
   with active multipliers.  Two routes: a tail certificate — a bound on the mass that local transport
   leaves (the theory division, asked, has nothing beyond the tail functions of its §11.33:
   THY-MSG-0023) — or a sampler for the extremal ensemble of the metric class, which would make
   Theorem 5.4 apply; or a way to tighten the sequential class.
2. **Samplers for the extremal ensemble of a box class** (new with Theorem 5.4).  It is a Boltzmann
   weight whose energy jumps by `ln(u/l)` across the surface `{s = 0}`.  Needed: exact or certified
   samplers for such weights (perfect simulation, or chains with certified mixing), and a rule for the
   pilot with a guarantee on the width.  Without them Theorem 5.4 is a statement about enumerable or
   exactly samplable models.
3. **References that are not products.**  Answered in part by the theory division (THY-MSG-0023): the
   class marginalises into the class with constants `u_i + κ_i`, `κ_i` the pointwise log-ratio of the
   conditional laws across the cut (Proposition 9.7) — an outer bound that degrades quickly with the
   coupling; with only an expected-distance bound on the conditionals there is no pointwise statement.
   Open: a bound that uses the typical, not the worst, interaction across the cut.
4. **Is additivity essential for exact intervals?**  Answered by the theory division (THY-MSG-0023; not
   checked here): for pair observables the upper end is NP-hard to compute once the slope is of order
   `ln n`, and for succinctly given observables at every slope; open at constant slope for pair
   observables.
5. **Coresets** (Remark 3.2) for repeated queries.

## 13. What changed after the review (`REVIEW_A.md`)

| finding | what it said | what was done |
|---|---|---|
| C1 | the gap-sampling certificate ignored the declaration | code: the guards and allowances of the reference path; tests |
| C2, K3 | Theorem 4.1(e) false for `l ≡ 0`; the inconsistency certificate blind there | (e) restated and proved for every envelope; code: the right criterion for populations, abstention for samples, a deterministic check from the declared range; tests |
| C3 | Proposition 9.6: equality for monotone targets false beyond binary sites | statement, proof and docstring corrected; the counterexample kept as a test |
| M1 | "a property of the class", "intrinsic", "needs `e^{un}` draws" do not follow from Theorem 6.1; draws from the extremal ensemble avoid `Γ` | claims withdrawn (§0, §6, §9.4, Proposition 9.4, §11); Theorem 5.4 added, implemented, tested and measured |
| M2 | Theorem 6.1 needs its access model | stated in the theorem; remark on evaluations |
| M3 | "removes the dimension" holds for validity only | §0 and §5.3 reworded |
| M4 | Theorem 4.1(c) ill-posed | restated with complementary slackness; counterexample kept |
| M5 | completeness for `l ≡ 0` used and unproved | one proof for every envelope (the referee's) |
| M6 | the total-variation rule of §7.3 not monotone in `τ` | §7.3 states the constant allowance that the code uses |
| M7 | claims without support (`RESULTS.md`, "ball arithmetic", §7.2) | §7.1, §7.2, §11 reworded; the enclosure rule of §7.2 implemented and tested; `RESULTS.md` written from the stored runs |
| M8 | Proposition 5.2 is an upper estimate; capped bets | restated with both regimes |
| K1 | non-finite draws reported as certified | code: void; tests |
| K2 | `G = 0` not handled | code: the exact value in the gap certificate, abstention in the S3 routine; tests |
| K4 | model-free problems on an ellipsoid not solved | code: a valid subgradient and cutting planes; test against an independent programme; the affected baseline recomputed |
| m1–m11 | wording, constants, hypotheses | applied: m1 (§0, Theorem 3.1), m2 (after Proposition 2.5), m3–m4 (table of §2), m5 (Theorem 5.1), m6 (Theorem 9.1), m7 (§9.4), m8 (§0, Proposition 9.6), m9 (Theorem 4.1(b)), m10 (§8), m11 (Propositions 9.2, 9.4) |
| m12 | efficiency of the bets; no lumping in the S3 routine | recorded in §5; not changed |

Not done: a second review of the corrected text; the version of Theorem 6.1 with cells; interval
arithmetic for the population sums.
