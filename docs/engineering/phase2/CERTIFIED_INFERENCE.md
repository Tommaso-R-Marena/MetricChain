# Certified inference over classes of Boltzmann weights: theorem S3 verified, improved, and replaced

*Computational Research Division, branch `research/phase2-certified-inference`, Phase II (research
owner's directive D-11).  Written 2026-11-28.  Status of every statement: **[P]** paper proof given
here; **[N]** checked numerically by the prototype (`src/metricchain_eng/certinf/`, tests
`tests/eng/test_certinf.py`); nothing here is machine-checked.  An independent adversarial review by a
subagent is recorded in `REVIEW_A.md`; until it is, read every proof as unrefereed.*

## 0. Verdict

1. **S3 is correct**, with the constant it states, once six assumptions it leaves out are added (§2).
   Its proof is a covering-net argument and is routine.
2. **Its sample bound is not the right one.**  The dimension enters as `log d`, not `d·log(1/ε)`
   (Theorem 3.1).
3. **Compressing the whole moment body is the wrong tool for the stated purpose.**  A sound outer
   interval needs one expectation of one explicit function to be certified non-positive (Theorems 4.1,
   5.1).  That removes the dimension from the sample bound altogether, adapts to the variance, needs
   none of `b`, `G`, `Z_l`, needs no union bound over thresholds, and handles `G = 0`.
4. **No method can avoid a cost proportional to the envelope ratio `Γ = sup u/l`** (Theorem 6.1), in
   either access model.  For an energy envelope of half-width `ρ` this is `e^{2ρ}`: with an extensive
   residual, the rectangular class of S3 is exponentially expensive and its identified sets are
   nearly vacuous.  This is the main obstacle, and it is a property of the class, not of the method.
5. **The class that repairs this is in the archive**: the theory division's bounded-influence
   (Lipschitz) energies, for which it already has the linear structure and a transport duality with
   gains (its Theorems 11.12 and 11.105; Theorem 9.1 here is that duality applied to a tilted score).
   What is added here: for product references the class is closed under marginalisation, and for
   additive observables the identified set — with observations — is computed exactly at any system
   size without sampling (Proposition 9.2, Corollary 9.3), where the rectangular hull of the same class
   gives an interval that tends to the trivial one exponentially fast (§9.4).
6. **Novelty is low, and much of the exact theory was already in the archive.**  The exact dual of §4
   for exact data is the science division's item 89(d); its form with regions is the ensemble
   division's E17.2 for the model-free case; S3's sampler is the theory division's Proposition 11.113
   (for another question).  Outside the archive the ingredients are classical (§10).  What was found
   neither in the archive nor in a bounded search: the sampled certificate for an interval with data
   (Theorem 5.1), the lower bound for it (Theorem 6.1), and the closure statements of §9.  They are
   short, and a specialist may know them.

## 1. Setting, and the proposal under review

`X` is a finite set of configurations.  An **envelope** is a pair `l, u : X → [0, ∞)` with `l ≤ u` and
`Σ_x u(x) > 0`.  The **box class** is `W(l,u) = {w : l ≤ w ≤ u, Σ w > 0}`, and `P(l,u) = {w/Σw : w ∈
W(l,u)}`.  It is invariant under a common rescaling of `l` and `u`.  With energies, `l = e^{−E_max}`,
`u = e^{−E_min}`; with a reference model, `l = w₀ e^{−ρ}`, `u = w₀ e^{ρ}`.  Write `g = u − l`,
`G = Σ g`, `Z_l = Σ l`, and `Γ = sup_x u(x)/l(x) ∈ [1, ∞]`.

`φ : X → ℝ^m` are the measured observables, `f : X → ℝ` the target, `v = (1, φ, f) ∈ ℝ^d`, `d = m + 2`.
The **observation region** `R ⊂ ℝ^m` is closed and convex, with support function
`h_R(η) = sup_{y∈R} η·y`.  For a box with centre `y⁰` and half-widths `e`, `h_R(η) = η·y⁰ + Σ|η_i|e_i`;
for an ellipsoid `{y : (y−y⁰)ᵀΣ⁻¹(y−y⁰) ≤ χ²}` (correlated errors), `h_R(η) = η·y⁰ + χ·(ηᵀΣη)^{1/2}`.
The **identified set** of the target is

    I = { E_p f : p ∈ P(l,u), E_p φ ∈ R },      V⁺ = sup I,   V⁻ = inf I.

It is an interval (the image of a convex set under a linear-fractional map), possibly empty.

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
| H4 | `G > 0` | `q` is undefined; §7.4 |
| H5 | `Z_l > 0` | `κ = ∞`: no statement in the model-free case `l ≡ 0` |
| H6 | a regularity condition for the *width* | soundness holds, but the excess width is not `O(κ)` in general (next proposition) |

**Proposition 2.5 (conditioning of the enlarged problem) [P].**  For every `τ, η` with `Ψ(τ, η) ≤ 0` in
the notation of §4, `sup I(R ⊕ κB_∞) ≤ τ + κ‖η‖₁`.  Hence the enlargement of the region costs at most
`κ·inf‖η‖₁` over dual certificates, which is finite but unbounded over instances: it is the size of the
Lagrange multipliers of the observation constraints.

*Proof.*  `h_{R⊕κB_∞}(η) = h_R(η) + κ‖η‖₁`, so the score of §4 for the enlarged region at `τ + κ‖η‖₁`
equals the score for `R` at `τ`.  ∎

So the total excess width of S3's interval over `I` is up to `2κ(1 + ‖η⁺‖₁ ∨ ‖η⁻‖₁)`, not `2κ`.

## 3. The concentration bound improved

**Theorem 3.1 (dimension enters logarithmically) [P].**  Under (H1)–(H4), with probability at least
`1 − δ`,

    d_{H,∞}(K, K̂) ≤ G·[ 2·√(2 ln(2d)/L) + √(ln(2/δ)/(2L)) ].

So `L ≥ ε⁻²·(2√(2 ln 2d) + √(ln(2/δ)/2))²` suffices, against `2ε⁻²[d ln(1+8/ε) + ln(2/δ)]` in S3.

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
(b) *Completeness.*  For every `τ`, `inf_η Ψ(τ, η) = max{M_f − τM_0 : M ∈ K, M_φ ∈ M_0·R}` (`−∞` if the
set is empty).  Hence, if `I ≠ ∅` and `Z_l > 0`, `V⁺ = inf{τ : ∃η, Ψ(τ, η) ≤ 0}`.
(c) *Extremal weights.*  At a pair `(τ, η)` with `Ψ = 0`, the weights `w = u` on `{s > 0}`, `w = l` on
`{s < 0}` (anything in between on `{s = 0}`) attain it.
(d) *Lower endpoint.*  Apply (a)–(c) to `−f`.
(e) *Inconsistency.*  `I = ∅` if and only if there is `η` with
`Φ(η) := Σ_x [ l(x)t₊(x) − u(x)t₋(x) ] > 0`, where `t = η·φ − h_R(η)`.
(f) *Model-free limit.*  For `l ≡ 0`, `Ψ(τ,η) ≤ 0` reads `f − η·φ + h_R(η) ≤ τ` on `supp u`: the
classical dual of the generalised moment problem.

*Proof.*  (a) Let `p = w/Σw` be feasible.  Then `Σ w(f − τ) = Σ w s + Σw·(η·E_pφ − h_R(η)) ≤ Σ w s ≤
Σ[u s₊ − l s₋] ≤ 0`.  (b) `Ψ(τ, η) = max_{M∈K} γ(M, η)` with `γ(M, η) = M_f − τM_0 − η·M_φ +
h_R(η)M_0`, by Proposition 2.1.  `K` is compact and convex; `γ` is linear in `M`, and convex and lower
semicontinuous in `η` on the convex cone `{h_R < ∞}` because `M_0 ≥ 0`.  Sion's minimax theorem gives
`inf_η max_M γ = max_M inf_η γ`.  For `M_0 > 0`, `inf_η[−η·M_φ + h_R(η)M_0] = −M_0·sup_η[η·y − h_R(η)]`
with `y = M_φ/M_0`, and the supremum is `0` if `y ∈ R` and `+∞` otherwise (`R` closed convex).  The
last sentence follows from strict monotonicity in `τ`.  (c) is the case of equality in (a).  (e) "If" as
in (a).  "Only if": the set `Y = {M_φ/M_0 : M ∈ K}` is compact and convex and disjoint from the closed
convex `R`; a strictly separating `η` has `min_{M∈K}(η·M_φ − h_R(η)M_0) > 0`, which is `Φ(η) > 0` by
Proposition 2.1.  (f) is immediate.  ∎

*Remarks.*  (i) **This theorem is not new in the programme.**  With `m = 0` it is the threshold rule of
DeRobertis and Hartigan for intervals of measures, which the ensemble division gave to the science
division (ENSEMBLE-RES-0002 §4).  For exact data (`R` a point) parts (a)–(b) are the science division's
item 89(d) (`INFERENCE_LIMITS_ADDENDA.md` §(22): "`E_μψ ≤ t` whenever some `λ` has
`Σ u(ψ − t − λ·(Φ − m))₊ ≤ Σ l(ψ − t − λ·(Φ − m))₋`, with equality at the best `λ`").  The support
function of a convex error set and the Farkas certificate of infeasibility are the ensemble division's
E17.2 and F3 for the model-free case, which is (f).  What this statement adds is their union — regions
and the inconsistency certificate (e) for the box class — and a proof by one minimax argument.
Outside the programme it is classical in substance (§10).  (ii) The problem has `m + 1` unknowns whatever
`|X|` is; `X` enters only through sums of explicit functions.  (iii) The gradient of the root
`τ*(η) = inf{τ : Ψ(τ,η) ≤ 0}` is `∇h_R(η) − E_{p*}φ`, with `p*` the extremal ensemble of (c): at the
optimum the extremal ensemble's measured averages sit on the boundary point of `R` exposed by `η`.
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
`0 ≤ λ_1, …, λ_J < 1/B` be fixed, where `B ≥ sup_x ψ_{τ_min,η}(x)`; let `Y_1, …, Y_n` be independent
draws from `π`, independent of those choices.  Define

    W_n(τ) = (1/J) Σ_k Π_{j=1}^n (1 − λ_k·ψ_{τ,η}(Y_j)),      τ̂ = inf{τ ≥ τ_min : W_n(τ) ≥ 1/δ}.

Then `P(τ̂ < V⁺) ≤ δ`.  That is, `τ̂` is an upper bound for the whole identified set with probability
at least `1 − δ` — for every `n`, every dimension `m`, every choice of `η` and of the `λ_k`.

*Proof.*  `ψ_{τ,η}(x)` is non-increasing in `τ`, so every factor is positive for `τ ≥ τ_min` and
`W_n` is non-decreasing and continuous in `τ`.  Let `τ° = inf{τ ≥ τ_min : E_π ψ_{τ,η} ≤ 0}`; by Theorem
4.1(a), `τ° ≥ V⁺` or `τ° = τ_min`.  If `τ° = τ_min` and `E_π ψ_{τ_min,η} ≤ 0` every `τ̂ ≥ τ_min` is
valid.  Otherwise `E_π ψ_{τ°,η} = 0` by continuity, each product has expectation `Π(1 − λ_k·0) = 1`, so
`E W_n(τ°) = 1` and `P(W_n(τ°) ≥ 1/δ) ≤ δ` by Markov.  On the complement, monotonicity gives
`W_n(τ) < 1/δ` for all `τ ≤ τ°`, hence `τ̂ ≥ τ° ≥ V⁺`.  ∎

Only an **upper** bound `B` on `ψ` is needed; it comes from an a-priori bound on `U` (the envelope) and
on the ranges of `f` and `φ`.  If no such bound exists the procedure must abstain.  The same statement
with `−ψ` and Theorem 4.1(e) certifies inconsistency: fix `η`, test `E_π[L t₊ − U t₋] > 0`.

**Procedure.**  Split the sample.  On the first part solve the dual of §4 with the empirical measure
(any optimiser; only the quality of `η`, not soundness, depends on it) and choose the bets `λ_k` (a
geometric grid around the empirically log-optimal one).  On the second part compute `τ̂` by bisection.
Do the same for the lower endpoint with `δ/2` each.

**Proposition 5.2 (what it costs) [P, to first order].**  Let `μ = E_πψ < 0` and `σ² = Var_π ψ` at the
tested `(τ, η)`.  With the bet `λ = |μ|/(σ² + μ²)` (if below `1/B`),
`ln W_n ≈ nμ²/(2(σ²+μ²))`, so the certificate fires once `n ≳ 2(σ² + μ²)·ln(1/δ)/μ²`.  For a uniform
envelope (`L ≡ 1`, `U ≡ Γ`), scores bounded by `S`, and a target excess `α` over `V⁺`:
`|μ| ≥ α` and `σ² ≤ (Γ + 1)S²`, so

    n ≈ 2(Γ + 1)S²·ln(1/δ)/α²      (plus a term `ΓS ln(1/δ)/α` from the cap on the bet).

*Derivation.*  `ln(1 − λz) = −λz − λ²z²/2 + O(λ³)`; maximise `−λμ − λ²(σ²+μ²)/2`.  At the optimum
`Γ E s₊ = E s₋ ≤ S`, so `E[Γ²s₊²] ≤ ΓS·ΓE s₊ ≤ ΓS²`; and `∂Ψ/∂τ ≤ −E_π L = −1`.  ∎

**5.3 Comparison with S3 at equal certified accuracy.**  S3 needs `L = 8(Γ−1)²κ⁻²[d ln(1 +
16(Γ−1)/κ) + ln(2/δ)]` draws for an allowance `κ` — quadratic in `Γ`, linear in `d` — and then widens
the region as well (Proposition 2.5).  Theorem 5.1 needs about `2(Γ+1)S² ln(1/δ)/α²`: linear in `Γ`,
free of `d`.  The reason for the factor `Γ`: S3 controls the body to `εG` in every direction, whereas
at the optimum the gap term satisfies `G·E_q s₊ = −λ·b ≤ Z_l·S`, i.e. it is of the order of `Z_l`, and a
variance-sensitive test of that one direction sees a variance of order `E_q s₊`, not 1.  Measured:
`RESULTS.md`.

## 6. A cost proportional to the envelope ratio is unavoidable

**Theorem 6.1 (lower bound) [P].**  Let `Γ ≥ 4`, `δ < 1/4`.  Consider procedures that draw `n`
independent configurations and output `τ̂` with `P(V⁺ ≤ τ̂ ≤ V⁺ + α) ≥ 1 − δ` on every instance with
envelope ratio `Γ`, no observations, and a target with values in `[0,1]`.
(a) If the procedure knows `f` and `Γ` and samples from the reference `π`, then
`n ≥ Γ·ln(1/(4δ))/(72α²)` for `α < 1/6`.
(b) If in addition it is given `b`, `G` and `Z_l` exactly and samples from the gap distribution — S3's
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

**Consequences.**  (0) This is the counterpart, for an interval of an average under an unknown energy,
of the theory division's lower bounds for the partition sum of a known one (its Proposition 11.113(d):
order `sinh²(Δ/2)/ε²`, which is `Γ/(4ε²)` for an envelope of width `Δ = 2ρ`; Theorem 11.110(d)).
(i) The linear dependence on `Γ` in Proposition 5.2 is optimal up to constants.
(ii) Exact knowledge of `b`, `G`, `Z_l` does not change the rate.  (iii) For an energy envelope of
half-width `ρ`, `Γ = e^{2ρ}`.  If the residual is extensive, `ρ = n·ρ₁`, sampled certification costs
`e^{2nρ₁}`, more than enumerating a space of `q^n` states as soon as `ρ₁ > ½ ln q` (0.35 kT per binary
site).  (iv) In the model-free case `Γ = ∞`: **no finite sample certifies anything about unsampled
configurations.**  A linear programme over a sampled pool is a statement about that pool only.  The
ensemble division's E30 says the same from the other side — its verdicts are not stable when the pool
is refined, and its outer interval on a net needs a Lipschitz constant of the observables in
configuration space; its E28 bounds the weight an incomplete library can be missing.  An energy
envelope with finite `Γ` is the assumption that turns a pool into a statement about the population.

## 7. Propagating uncertainty in the inputs

**7.1 Envelopes.**  `P(l,u) ⊂ P(l',u')` whenever `l' ≤ l` and `u ≤ u'`.  If only enclosures
`l ∈ [l⁻, l⁺]`, `u ∈ [u⁻, u⁺]` are known, run every certificate with `(l⁻, u⁺)`.  Rounding is handled the
same way: the prototype evaluates certificate sums in ball arithmetic and decides on the upper end.

**7.2 `b`, `G`, `Z_l` (gap sampling only).**  With `b ∈ [b⁻, b⁺]` componentwise and `G ≤ G⁺`,
`Ψ ≤ Σ_i max(λ_i b_i⁻, λ_i b_i⁺) + G⁺·E_q s₊`; certify the right-hand side.  If `b` itself is estimated
from a sample of `p_l ∝ l`, a second test and a split of `δ` are needed.  Reference sampling needs
neither — the reason to prefer it whenever a reference exists.

**7.3 Approximate sampling.**  If the sampler's law `π'` satisfies `π'/π ∈ [1/β, β]`, replace `(L, U)`
by `(L/β, βU)`.  If only `‖π' − π‖_TV ≤ ε_TV` is known, add `ε_TV·(sup ψ − inf ψ)` to the tested
expectation.  If the draws are dependent (Markov chain Monte Carlo) and no certified mixing bound is
available, Theorem 5.1 does not apply and the prototype **abstains**; exact samplers exist for product,
chain and tree references.

**7.4 Observables.**  An evaluation error `|φ̃ − φ| ≤ e_φ` enlarges `R` by `e_φ`; an error on `f` is
added to the interval.  Ranges of `f`, `φ` and a bound on `U` must be declared: they define `B`.  A
sampled value outside the declared bounds voids the certificate (reported, not ignored).

**7.5 `G = 0` and partial degeneracy.**  If `l = u` the class is one ensemble, `K = {b}`, `q` is
undefined and S3 has no content.  In §5, `ψ = L·s` and the certificate is an ordinary one-sided test of
`E_{p_l} s ≤ 0`: a confidence interval for one ensemble average, with the observations acting as
control variates through `η`.  If `g = 0` only on part of `X`, gap sampling never visits that part and
relies on `b` for it; reference sampling treats all configurations alike.

**7.6 The gap distribution.**  Its limitations, collected: it needs (H2); its rate is the same as the
reference's (Theorem 6.1(b)); when `u/l` varies it concentrates on the most uncertain configurations,
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
proportional to `|u s₊ − l s₋|`; a two-stage scheme (pilot, then tilted proposal with known density
ratio) is sound by §7.3 and not implemented.  *Low rank*: the dependence on `X` is through the law of
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
score because that is the form the multipliers of §4 need.  Propositions 9.2 and 9.4 and Corollary 9.3
were not found in the archive; the theory report says of closed forms that they are "special to
single states".

**Definition.**  Let `π > 0` on `X`, `E` a set of ordered pairs, `C_{xy} > 0` for `(x,y) ∈ E`.  The
**ratio-constrained class** is `𝒞 = {r ≥ 0 : r(x) ≤ C_{xy}·r(y) for (x,y) ∈ E}`, a polyhedral cone, with
ensembles `p ∝ π·r`.  With `C_{xy} = e^{c(x,y)}` this says that the residual energy `−ln r` is
`c`-Lipschitz.  The box class is the star: one extra node `*` with `r(x) ≤ U(x)r(*)` and
`r(*) ≤ r(x)/L(x)`.  Intersections of classes are unions of edge sets.

**Theorem 9.1 (flow duality) [P].**  Let `a : X → ℝ`.  Then `Σ_x a(x)r(x) ≤ 0` for all `r ∈ 𝒞` if and
only if there is a flow `θ : E → [0, ∞)` with

    a(x) ≤ Σ_{y:(x,y)∈E} θ_{xy} − Σ_{y:(y,x)∈E} C_{yx}·θ_{yx}        for every x.

Consequently, with `a = π·s_{τ,η}`: `E_p f ≤ τ` for every `p` in the class with `E_pφ ∈ R` as soon as
such a flow exists for some `η`; and if the class is compact after normalisation (e.g. `E` strongly
connected) and `I ≠ ∅`, `V⁺` is the infimum of the `τ` for which one exists.

*Proof.*  `𝒞 = {r : −r ≤ 0, Ar ≤ 0}` with rows `e_x − C_{xy}e_y`.  By Farkas' lemma the cone of vectors
`a` with `a·r ≤ 0` on `𝒞` is `{Aᵀθ − ν : θ, ν ≥ 0}`, and `(Aᵀθ)(x)` is the right-hand side.  The
second part is Theorem 4.1 with `K` replaced by `{Σ_x π(x)r(x)v(x) : r ∈ 𝒞}`; Sion's theorem applies on
the compact convex set `{r ∈ 𝒞 : Σπr = 1}`.  ∎

*Reading.*  Positive mass `a₊` must be shipped to where `a` is negative; a unit shipped along `(x,y)`
arrives as `C_{xy}` units.  For the star this is `Σ[U a₊ − L a₋] ≤ 0`: Theorem 4.1.  For a metric
class it is a transport problem with multiplicative cost `e^{c(x,y)}`.

**Proposition 9.2 (closure under marginalisation) [P].**  Let `X = Π_i X_i`, `π = ⊗π_i`, and let `𝒞_u` be
the class of `r` with `r(x) ≤ e^{u_i}r(x')` whenever `x, x'` differ only at site `i`.  For every set
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

**9.4 Exponential separation from the box class [P].**  Uniform cube, `π_i = ½`, slope `u` at every
site, target `f = x_1`, no observations.  Bounded-influence class: `V⁺ = σ(u)`, for every `n`.  Every
box class containing it has ratio at least `e^{un}` (a box needs `U(x) ≥ e^{un}L(x̄)` for antipodal
`x, x̄`, so `U(x)U(x̄) ≥ e^{2un}L(x)L(x̄)`), and for the uniform box of that ratio — as for the box
centred at a configuration — `V⁺ = e^{un}/(1 + e^{un})`: within `e^{−un}` of the trivial bound 1.  And by Theorem 6.1 any sampled certificate over that box needs
`e^{un}` draws.  S3 applied to envelopes derived from a bounded-influence class therefore discards
essentially all the information in the class.

**Proposition 9.4 (local transport plus a global remainder) [P].**  Let `r` be in a ratio-constrained
class and also satisfy `max r/min r ≤ Γ_glob`.  Let `Q(x, ·)` be any kernel that moves a configuration
with `s(x) > 0` along edges, with path constant `C(x,y) ≥ r(x)/r(y)`, and put

    β(y) = Σ_x π(x)s₊(x)Q(x,y)C(x,y) − π(y)s₋(y).

Then `Σ π r s ≤ 0` whenever `Σ_y [Γ_glob·β₊(y) − β₋(y)] ≤ 0`.  If each `y` has enumerable preimages
under `Q`, `β(y)/π(y)` is computable at a sampled `y` and the condition is one expectation under `π`:
Theorem 5.1 applies.

*Proof.*  `Σ_x π r s₊ = Σ_{x,y} π(x)r(x)s₊(x)Q(x,y) ≤ Σ_y r(y)Σ_x π(x)s₊(x)Q(x,y)C(x,y)`, so
`Σ π r s ≤ Σ_y r(y)β(y) ≤ max r·Σβ₊ − min r·Σβ₋`.  ∎

*Limit of this proposition.*  The remainder pays `Γ_glob`.  For a pure bounded-influence class on `n`
sites `Γ_glob = e^{un}`, and by Theorem 6.1 no sample can certify the remainder: the transport must
then cancel all positive mass identically, which is an analytic statement (as in Corollary 9.3), not
a sampled one.  Sampled certificates for metric classes are therefore available today only when a
moderate global ratio is also assumed.  This is the main open problem (§12).

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
| Theorem 6.1 (cost `∝ Γ`) | — | not found; a standard two-point argument |
| Theorem 9.1 (flow duality) | the theory division's Theorem 11.105 (in the archive; its own search found the general duality "not found in six searches at summary level"); generalised flows (Jewell); metric differential privacy | in the archive; a corollary |
| Proposition 9.2, Corollary 9.3 (closure; additive observables) | closure of metric differential privacy under post-processing is the same inequality | not found for partial identification; the proofs are two lines each |
| the application (energy envelope + averaged data → guaranteed interval or inconsistency) | "maximum occurrence" of a conformation given averaged data (Bertini et al.), without energies; bounds on Gibbs averages in a Kullback–Leibler ball (Katsoulakis, Rey-Bellet and co-authors), without data; maximum-entropy, BioEn, BME, metainference: one ensemble or a posterior, not a set | not found |

## 11. What is demonstrated, and what is not

* Demonstrated (proofs here; numerics in `RESULTS.md`): S3 holds under (H1)–(H5); a sound interval is
  obtained with far fewer draws by Theorem 5.1; the cost in `Γ` is intrinsic; for bounded-influence
  classes with product references and additive observables the identified interval is exact at any
  size.
* Not demonstrated: any statement about a molecule.  An identified interval is exactly as good as its
  envelope, and no envelope between a force field and nature is known; the archive's own measurements
  put the residual of one implicit-solvent term at 12–53 kT per site, for which every interval here is
  vacuous.  The classes for which envelopes *are* rigorous are differences between two models (a
  truncated and a full energy; two parameter sets), i.e. statements about a model.

## 12. Open problems, in order of value

1. **Sampled certificates for bounded-influence classes without a global ratio.**  Needed: a tail
   certificate — a bound on the mass that local transport leaves — from the large-deviation exponents
   of the class (the theory division's exponents `a`, `h` are exactly of this kind), or an analytic
   transport for structured scores.
2. **References that are not products.**  Closure fails; under a Dobrushin-type smallness of the
   reference's own influences a perturbed closure should hold (the theory division's results on
   certified and uncertified influence, its Theorems 11.119 and 11.121, are the natural input).
3. **A lower bound for metric classes** matching Corollary 9.3: is the exact computation possible only
   because the observables are additive?
4. **Coresets** (Remark 3.2) for repeated queries.
