# What noisy averaged distances and inexact local geometry still determine — with every constant computable

**Geometric Inference division — fifth note** (thirteenth checkpoint).  Labels as in
`ENSEMBLE_RIGIDITY.md`: [P] proof on paper, [N] numerical, [K] known.  **Unreviewed.**
Written for three open items: our obligation O-5 (the constant of Theorem G was a global
infimum that nobody could compute), the Ensemble division's remark that our stability
theorem did not have computable constants, and items G-1 and G-3 of the Frontier
Benchmarking division's `MATHEMATICAL_FEEDBACK.md` ("demixing has no noise statement";
"does Theorem B survive bond constraints known only within `±δ`").

**What this note gives, and what it does not.**  It gives inequalities, valid for *every*
competing ensemble, in which every constant is a finite computation on the data or on a
fitted mixture; the first-order constants of the demixing problem, which are small
(between `0.7` and `4.5` in the instances computed) and attained; and an exact description
of what a tolerance on the bond geometry costs.  It does **not** give a guarantee at
realistic accuracy: the ranges in which the inequalities are certified end at relative
errors between `10⁻¹²` and `10⁻⁴` of the data (§8).  Outside those ranges the first-order
constants are predictions, not theorems.

## 0. Summary

Data: the centred matrix `G̃ ≈ G(μ) = −½ J M(μ) J` of a `K`-state ensemble `μ` of chains, known
up to an error `ε` in Frobenius norm; the statewise constraints (bond lengths, 1–3
distances) known up to a tolerance `δ`.

1. **A lemma about one matrix (Lemma N0).**  A positive semidefinite matrix of rank at
   most 3 that satisfies the conic equations up to a residual `ρ` is within
   `c·ρ/σ` of one of the `K` reference projectors — where `σ` is the smallest non-trivial
   singular value of the conic system, a number the demixing algorithm already computes.
   The proof is three lines of eigenvalue interlacing.  This is the quantitative form of
   "the only chains that are linear images of the stack are the states" (Theorem B).
2. **All ensembles, square-root law, explicit (Theorem N1).**  For every ensemble `ν` of
   chains — any number of states, continuous or not — whose data are within `ε` of `G̃`:
   all of its mass except a fraction `√(n−1−3K)·ε/φ₁` lies within an explicit radius
   `r(φ₁)` of the `K` reference states.  As a corollary the constant `κ` of Theorem G has
   a **computable lower bound** (O-5 closed in this sense).  The rate `distance² ≲ ε` is
   the true one (Theorem G(e)).
3. **`K`-state mixtures, linear law, explicit (Theorem N2).**  Every `K`-state mixture
   within `ε` of the data has its states within `C·ε` of the reference states and its
   inverse weights within `C′·ε`, for `ε` below an explicit threshold; `C` is large
   (`10²`–`10⁶`).
4. **The right constants, in a certified range (Theorem N3).**  Linearising at an exact
   mixture gives the first-order constants `C_state`, `C_w` (block norms of a
   pseudo-inverse).  By iterating a second-order inequality from the crude bound of item 3
   they are proved for every `K`-state competitor in a smaller range, and they are
   **attained** to first order.  In the instances: `C_state` between `0.7` and `4.5` —
   demixing is well conditioned to first order, also at the thresholds.
5. **From the data alone (§6).**  DEMIX, then a least-squares polish to an exact mixture
   `μ₀` with residual `ε₀`: every competitor within `ε` of the data is within `ε + ε₀` of
   `G(μ₀)`, and items 2–4 apply at `μ₀`.  The number of states: the eigenvalues above `ε`
   count `3K` whenever `ε < λ_{3K}/2`; no noisy data bound `K` from above.
6. **Inexact local geometry (§7).**  With exact data and constraints known within `δ`,
   identifiability in the exact sense is **lost for every `δ > 0`**: the mixtures with the
   same data form an explicit family of dimension `9K(K−1)/2 + K − 1` (rotations of the
   stack).  Its size is linear in `δ` with an exactly computable first-order constant
   `c_tol` (between `0.7` and `1.8` in the instances, attained), and Theorem N3 certifies a
   constant within a factor 6 of it.  So Theorem B survives a tolerance as a stability
   statement, not as a uniqueness statement.

Evidence: `experiments/geometry/robust_demix.py` checks every inequality of every proof on
competitors that are not chosen to be favourable (chains near the states, random chains,
chains that are nearly affine images of the stack and far from every state; split states
and spurious states of small weight; mixtures along the extremal directions).  No
violation; §8.

## 1. Setting and notation

`n` points in `ℝ³`, `K` states, `m = 3K`.  `E₀` is the set of statewise-constrained pairs with
nominal lengths `ℓ_e` (for chains: separations 1 and 2).  For a tolerance vector `δ = (δ_e) ≥ 0`
let `𝒞_δ` be the set of configurations `Y` with `| |y_i − y_j|² − ℓ_e² | ≤ δ_e` for `e = (i, j) ∈ E₀`;
`𝒞 = 𝒞_0`.  Nothing else about chains is used, except in the automatic weight bound of
Theorem N2, which needs the bonds to be in `E₀`.  `L₀` is the Laplacian of the graph `E₀`,
`Λ₀` its largest eigenvalue (at most `6.25` for chains), `ℓ₊ = max_e √(ℓ_e² + δ_e)`,
`D_n² = ℓ_b² n(n² − 1)/12` with `ℓ_b` the largest bond length (the squared Frobenius norm of a
centred chain is at most `D_n²`).

For an ensemble `ν` on `𝒞_δ`: `G(ν) = ∫ Y_c Y_cᵀ dν = −½ J M(ν) J` (`Y_c` the centred configuration), so
`‖G(ν) − G(ν′)‖_F ≤ ½‖M(ν) − M(ν′)‖_F`.

**The symmetry group.**  `d_P(X, Y) = min ‖Y − XR − 𝟙tᵀ‖_F` over **all** isometries, reflections
included.  Every statement of this note — and of the report — identifies each state up to
its own isometry, independently of the other states: averaged squared distances cannot
see the handedness of any state.  (Item G-4 of the Frontier division; the convention is
now stated in the report, §1, and in the implementation guide, §0.)

**A reference** is a triple `(Z, Q, v)`: `Z ∈ ℝ^{n×m}` with centred columns and rank `m`;
`Q = [Q_1 … Q_K] ∈ O(m)` cut into blocks of three columns; `v_k > 0`.  It defines reference states
`X̂_k = ZQ_k/√v_k` and reference projectors `P̂_k = Q_kQ_kᵀ/v_k`, with `Σ_k v_k P̂_k = I` and
`Σ_k v_k X̂_k X̂_kᵀ = ZZᵀ`.  Two cases are used:

* *cut from the data*: `Z` from the top `m` eigenpairs of `G̃`, `Q` and `v` as DEMIX computes them;
* *exact*: `Z` the centred stack of a mixture `μ₀ = Σ w_k δ_{X_k}` of chains in `𝒞`, `Q` the
  coordinate blocks, `v = w`; then `X̂_k = X_k`.

From a reference the following numbers are computed (`robust_demix.py`, `numbers`):

    𝒞_Z : Sym(m) → ℝ^{E₀},  S ↦ (e_Zᵀ S e_Z)_e          (e_Z the E₀-edge vectors of Z)
    τ_k = ‖𝒞_Z(P̂_k) − ℓ²‖₂ = ‖( |e_{X̂_k}|² − ℓ_e² )_e‖₂ ,   τ_max = max_k τ_k      (violations of the reference states)
    𝒯′ = span{P̂_k − P̂_1} ,    σ_⊥ = min{ ‖𝒞_Z N‖₂ : N ⊥ 𝒯′, ‖N‖_F = 1 }
    V = Σ v_k ,   σ′ = σ_⊥ − 2τ_max V ,   c_k = 1 + √(3(K − 1 + (V/v_k − 1)²))
    a = κ_P ‖Z‖_op max_k √v_k c_k ,   κ_P = 1/√(2(√2 − 1)) < 1.099 ,   λ_m = σ_m(Z)² .

For an exact reference `τ = 0`, `V = 1`, and `σ_⊥ > 0` **iff the conic condition (CC) holds**
(`ker 𝒞_z = 𝒩(z)` contains `𝒯 = 𝒯′`, with equality iff (CC)); it is the "smallest non-trivial
singular value" that §6.1 of the report already reports.  Finally, for `φ ≥ 0`,

    ρ(φ) = ‖δ‖₂ + 2ℓ₊√(Λ₀φ) + Λ₀φ ,    ν̄(φ) = (ρ(φ) + τ_max)/σ′ ,    r(φ) = √φ + a ν̄(φ) .

Lemma P is the Procrustes–Gram inequality of `LOCAL_DATA_STABILITY.md` §3 [K]:
`min_{R ∈ O(r)} ‖U − XR‖_F ≤ κ_P ‖UUᵀ − XXᵀ‖_F / σ_r(X)`.

## 2. The lemma

**Lemma N0 (near a vertex) [P].**  Let `(Q, v)` be as above, `𝒞 : Sym(m) → ℝ^E` any linear map and
`ℓ² ∈ ℝ^E`, with `τ_k, τ_max, σ_⊥, σ′ > 0, V, c_k` defined as in §1.  Let `P ∈ Sym(m)` be positive
semidefinite of rank at most 3 with `‖𝒞(P) − ℓ²‖₂ ≤ ρ`, and put `ν̄ = (ρ + τ_max)/σ′`.  If `ν̄V < 1`
there is an index `k₀` with

    ‖P − P̂_{k₀}‖_F ≤ c_{k₀} ν̄ .

*Proof.*  Write `P − P̂_1 = T + N` with `T ∈ 𝒯′` and `N ⊥ 𝒯′`; then `P = Σ_k t_k P̂_k + N` with
`Σ t_k = 1`, and `𝒞(N) = (𝒞(P) − ℓ²) − Σ_k t_k(𝒞(P̂_k) − ℓ²)`, so

    σ_⊥ ‖N‖_F ≤ ρ + τ_max Σ_k |t_k| .                                             (∗)

`B = Σ t_k P̂_k` has the eigenvalues `b_k = t_k/v_k`, each of multiplicity 3.  Let `ν = ‖N‖_op`.
`P = B + N` is positive semidefinite with at most three non-zero eigenvalues, so by Weyl's
inequality every eigenvalue of `B` is at least `−ν` and all but the three largest are at
most `ν`: `b_k ≥ −ν` for all `k`, and at most one `k` has `b_k > ν`.
*If no `k` has `b_k > ν`:* `|t_k| ≤ v_kν`, so `1 = Σ t_k ≤ νV` and, by (∗),
`‖N‖_F ≤ ρ/(σ_⊥ − τ_maxV) ≤ ν̄`, whence `νV ≤ ν̄V < 1` — a contradiction.
*So exactly one `k₀` has `b_{k₀} > ν`.*  Then `|t_k| ≤ v_kν` for `k ≠ k₀`, `|t_{k₀} − 1| ≤ ν(V − v_{k₀})`,
`Σ|t_k| ≤ 1 + 2νV`, and (∗) gives `‖N‖_F ≤ (ρ + τ_max)/(σ_⊥ − 2τ_maxV) = ν̄`.  Finally
`‖B − P̂_{k₀}‖_F² = 3[Σ_{k≠k₀} b_k² + ((t_{k₀} − 1)/v_{k₀})²] ≤ 3ν²[(K − 1) + (V/v_{k₀} − 1)²]`.  ∎

For an exact reference the lemma says: *a positive semidefinite matrix of rank at most 3
that solves the conic system up to `ρ < σ_c` is within `c_kρ/σ_c` of one of the `K` projectors* —
Theorem B′ with a modulus.

## 3. All ensembles

For a configuration `Y` let `A_Yᵀ = Z⁺Y_c` (so `ΠY_c = ZA_Yᵀ`, `Π` the projection onto the columns
of `Z`), `R_Y = Π^⊥Y_c` and `φ(Y) = ‖R_Y‖_F²` — the squared distance from `Y` to the affine images of
the stack; `φ` is the certificate function of Theorem G.

**Theorem N1 [P].**  Let `(Z, Q, v)` be a reference with `σ′ > 0` and `G̃` a symmetric centred
matrix.  Let `ν` be any ensemble on `𝒞_δ` and `ε = ‖G(ν) − G̃‖_F`.
(a) `∫ φ dν ≤ Φ := √(n − 1 − m)·ε + tr(Π^⊥ G̃)`.
(b) For every `Y ∈ 𝒞_δ` with `ν̄(φ(Y))V < 1`: `min_k d_P(Y, X̂_k) ≤ r(φ(Y))`.
(c) For every `φ₁` with `ν̄(φ₁)V < 1`: `ν{ Y : min_k d_P(Y, X̂_k) > r(φ₁) } ≤ Φ/φ₁`.

*Proof.*  (a) `∫ φ dν = tr(Π^⊥G(ν)) = ⟨Π^⊥, G(ν) − G̃⟩ + tr(Π^⊥G̃)` and `‖Π^⊥‖_F = √(n − 1 − m)`.
(b) For `e = (i, j) ∈ E₀` the edge of `Y` is `e_Y = A_Ye_Z + r_e`, `r_e` the edge of `R_Y`.  `P_Y = A_YᵀA_Y` is
positive semidefinite of rank at most 3 and
`e_ZᵀP_Ye_Z − ℓ_e² = (|e_Y|² − ℓ_e²) − 2⟨e_Y, r_e⟩ + |r_e|²`; since `Σ_e |r_e|² = tr(R_YᵀL₀R_Y) ≤ Λ₀φ`, the
residual has norm at most `ρ(φ)`.  Lemma N0 gives `k₀` with `‖P_Y − P̂_{k₀}‖_F ≤ c_{k₀}ν̄(φ)`.  Lemma P
with `U = A_Yᵀ` and `X = Q_{k₀}/√v_{k₀}` (`XXᵀ = P̂_{k₀}`, `σ_3(X) = 1/√v_{k₀}`) gives `R ∈ O(3)` with
`‖A_Yᵀ − XR‖_F ≤ κ_P√v_{k₀} c_{k₀} ν̄(φ)`, and `Y_c − X̂_{k₀}R = Z(A_Yᵀ − XR) + R_Y`.
(c) `r` is increasing, so by (b) the set is contained in `{φ > φ₁}`; Markov and (a).  ∎

**Corollary N1.1 (a computable constant for Theorem G) [P].**  Let `μ₀` satisfy (CC), take the
exact reference, `δ = 0`, and any `φ₁` with `ν̄(φ₁) < 1`.  Then the constant
`κ = inf_{Y ∈ 𝒞} φ(Y)/min_k d_P(Y, X_k)²` of Theorem G satisfies

    κ ≥ min( φ₁/r(φ₁)² ,  φ₁/(2D_n²) ) ,

so `∫ min_k d_P(·, X_k)² dν ≤ (√(n − 1 − 3K)/(2κ)) ‖M(ν) − M(μ₀)‖_F` for every ensemble `ν` on `𝒞`, with
a constant that is a finite computation.

*Proof.*  `r(φ)²/φ` is increasing; for `φ(Y) ≤ φ₁` use (b); for `φ(Y) > φ₁` use
`min_R ‖Y_c − X_cR‖_F² ≤ ‖Y_c‖² + ‖X_c‖² ≤ 2D_n²`.  ∎

*What it is worth.*  The bound is correct and small: `10⁻¹³` to `10⁻⁷` in the table of §8,
against values of `κ` between `2·10⁻³` and `3·10⁻²` found by global search in comparable
instances (report, §7.2).  The loss has two sources: the product of four worst cases in
`r` (edge alignment, `1/σ_c`, the interlacing constant, `‖Z‖_op`) and the trivial bound `2D_n²`
outside the basin `φ ≤ φ₁`.  The basin itself is certified up to `φ₁ ≈ (σ_c/(2ℓ₊√Λ₀))²`;
chains that are nearly affine images of the stack and far from every state exist at
`φ` 70 to 1 100 times larger [N; §8], so the true basin is at most that much larger.
The rate — squared distance proportional to the error of the data — cannot be improved
(Theorem G(e): splitting a state changes the data at second order).

## 4. Mixtures with `K` states: a linear law

**Theorem N2 [P].**  Let the reference be cut from `G̃` (factor `f = 2`) or exact with `G̃ = ZZᵀ`
(`f = 1`), with `σ′ > 0`.  Let `μ′ = Σ_{j=1}^K u_j δ_{Y_j}` be a mixture of `K` configurations of `𝒞_δ` with
`‖G(μ′) − G̃‖_F ≤ ε < λ_m`, and put `ε_Z = f κ_P ε/√λ_m`, `ν̄_j = ν̄(ε_Z²/u_j)`.  If

    max_j ν̄_j · V < 1    and    2 max_k c_k · max_j ν̄_j < √6 ,

then after renumbering the states of `μ′`

    d_P(Y_k, X̂_k) ≤ ε_Z/√u_k + κ_P ‖Z‖_op √v_k c_k ν̄_k ,      |1/u_k − 1/v_k| ≤ c_k ν̄_k .

For chains, `u_j ≥ (λ_m − ε)/D_n²` always; and whenever the hypotheses hold with lower
bounds `u̲_k ≤ u_k`, they hold with the better bounds `1/(1/v_k + c_kν̄(ε_Z²/u̲_k))`.

*Proof.*  Let `z′` be the centred stack of `μ′`, `G(μ′) = z′z′ᵀ` of rank at most `m`.  *Cut from the
data:* by Weyl the eigenvalues of `G̃` beyond the `m`-th are at most `ε` in absolute value and
the `m`-th exceeds `ε`, so `ZZᵀ` is a best approximation of `G̃` of rank `m` and
`‖ZZᵀ − z′z′ᵀ‖_F ≤ 2ε`; *exact:* `≤ ε`.  Lemma P gives `Q₀ ∈ O(m)` with `z′ = ZQ₀ + E`, `‖E‖_F ≤ ε_Z`.
With `Π_j` the `j`-th coordinate block, `Y_j = ZA_jᵀ + E_j` where `A_jᵀ = Q₀Π_jᵀ/√u_j` and
`‖E_j‖_F ≤ ε_Z/√u_j`.  `P′_j = A_jᵀA_j` is positive semidefinite of rank 3 with the single non-zero
eigenvalue `1/u_j`, and as in Theorem N1(b) — with `E_j` in the place of `R_Y` — its conic
residual is at most `ρ(ε_Z²/u_j)`.  Lemma N0 gives `k(j)` with `‖P′_j − P̂_{k(j)}‖_F ≤ c_{k(j)}ν̄_j`; the
bound on the states follows as before, the bound on the weights from Weyl applied to the
largest eigenvalues `1/u_j` and `1/v_k`.  `j ↦ k(j)` is injective: `P′_jP′_{j′} = 0` for `j ≠ j′`, so
`‖P′_j − P′_{j′}‖_F² = 3/u_j² + 3/u_{j′}² ≥ 6`, which exceeds `(2 max c · max ν̄)²`.
The automatic bound: `λ_m(G(μ′)) ≥ λ_m − ε` (Weyl), and `λ_m(G(μ′)) ≤ u_jλ_1(Y_{j,c}Y_{j,c}ᵀ) ≤ u_jD_n²`
because the other states contribute rank at most `m − 3`.  The improvement of the lower
bounds: the index `k₀` of Lemma N0 depends on `P′_j` only, so the conclusion `|1/u_k − 1/v_k| ≤ c_kν̄_k`
may be fed back.  ∎

The constant of this theorem — the limit of the bound divided by `ε` — is the product of
the same worst cases and is large (`C_crude` in §8).  Its use is to place every competitor
in the neighbourhood where the next theorem applies.

## 5. The first-order constants, certified

Let the reference be exact, `μ₀ = Σ w_k δ_{X_k}` with `X_k ∈ 𝒞` centred.  For each `k` let `Rig_k` be the
rigidity operator of `(E₀, X_k)` (`Δ ↦ (⟨e_{X_k}, Δ_e⟩)_e`), `s_k` its smallest non-zero singular value,
and `𝒯_k` the space of its flexes that are orthogonal to the infinitesimal isometries of
`X_k`.  Let

    𝓛(a, τ) = Σ_k [ a_k X_kX_kᵀ + w_k (X_kτ_kᵀ + τ_kX_kᵀ) ]      on   { Σ a_k = 0 } × ∏_k 𝒯_k .

**Hypothesis (J):** `𝓛` is injective (infinitesimal identifiability; it follows from (CC) —
bracketed step of Theorem G(d) — and is checked numerically for each instance).  Define

    C_state,k = ‖(τ_k-block of 𝓛⁺)‖_op ,     C_w = ‖(a-block of 𝓛⁺)‖_op ,
    T_k = ‖ viol ↦ ν⁰_k − (τ_k-block of 𝓛⁺𝓛(0, ν⁰)) ‖_op ,    ν⁰_j = Rig_j⁺(viol_j/2) ,

`T_w` likewise for the weights; `viol = (viol_{j,e})` ranges over all vectors indexed by states
and constrained pairs.  All are norms of explicit matrices (`first_order` in the script).

**Theorem N3 [P].**  Assume (J).  Let `μ′ = Σ u_kδ_{Y_k}` be a mixture of `K` configurations of `𝒞_δ`
with `‖G(μ′) − G(μ₀)‖_F ≤ η`, numbered and aligned so that `Δ_k = Y_kR_k − X_k` has minimal norm.
If `‖Δ_k‖_F ≤ B_k` and `|u_k − w_k| ≤ A_k` for all `k`, then, with `‖viol‖ ≤ √K‖δ‖₂`,

    ‖Δ_k‖_F ≤ T_k‖viol‖ + C_state,k · 𝓔(B, A) + Λ₀B_k²/(2s_k) ,
    ‖u − w‖₂ ≤ T_w‖viol‖ + C_w · 𝓔(B, A) ,
    𝓔(B, A) = η + Σ_k [ w_k‖X_k‖_op Λ₀B_k²/s_k + 2A_k‖X_k‖_opB_k + (w_k + A_k)B_k² ] .

In particular, starting from the bounds of Theorem N2 (`A_k = w_kc_kν̄_k`) and iterating, one
obtains bounds that tend to `C_state,k η + T_k‖viol‖` and `C_w η + T_w‖viol‖` as `η, δ → 0`.
**The constant `C_state,k` cannot be improved:** there are mixtures `μ_t → μ₀` of `K` chains with
`d_P(Y_k(t), X_k)/‖G(μ_t) − G(μ₀)‖_F → C_state,k`.

*Proof.*  Optimal alignment makes `Δ_k` centred and orthogonal to the infinitesimal rotations
of `X_k` (`X_kᵀ(Y_kR_k)` is symmetric), so `Δ_k = τ_k + ν_k` with `τ_k ∈ 𝒯_k` and `ν_k ⊥ ker Rig_k`.  The
constraints give `2 Rig_k(Δ_k) = viol_k − q_k`, where `viol_{k,e} = |e_{Y_k}|² − ℓ_e²` and `q_{k,e} = |Δ_{k,e}|²`,
`‖q_k‖₂ ≤ Λ₀‖Δ_k‖²`; hence `ν_k = ν⁰_k + ν¹_k` with `‖ν¹_k‖ ≤ Λ₀‖Δ_k‖²/(2s_k)`.  With `a_k = u_k − w_k`,
exactly,

    G(μ′) − G(μ₀) = 𝓛(a, τ) + 𝓛(0, ν) + Σ_k [ a_k(X_kΔ_kᵀ + Δ_kX_kᵀ) + w_kΔ_kΔ_kᵀ ] + Σ_k a_kΔ_kΔ_kᵀ .

Apply `𝓛⁺` (a left inverse on the tangent space): `(a, τ) = −𝓛⁺𝓛(0, ν⁰) + 𝓛⁺[…]`, where the
bracket has norm at most `𝓔(B, A)` (`‖𝓛(0, ν¹)‖ ≤ Σ 2w_k‖X_k‖_op‖ν¹_k‖`).  Then
`Δ_k = [ν⁰_k − (𝓛⁺𝓛(0, ν⁰))_k] + (𝓛⁺[…])_k + ν¹_k`.  Each iteration is an implication for the same
competitor, and the right-hand sides are increasing in `(B, A)`, so taking minima is
legitimate.  Sharpness: generic chains are smooth points of `𝒞` with tangent space
`𝒯_k ⊕` isometries, so the curve of mixtures with velocity `𝓛⁺y`, `y` the direction that
attains the norm, has the stated limit.  ∎

## 6. From the data alone

**Corollary N4 (a posteriori) [P].**  Given `G̃` and an error level `ε`: compute any exact
`K`-mixture `μ₀` of chains (in practice: DEMIX, then least squares over weights and torsions)
and its residual `ε₀ = ‖G(μ₀) − G̃‖_F`.  Every ensemble whose data are within `ε` of `G̃` is within
`η = ε + ε₀` of `G(μ₀)`; Theorems N1–N3 at `μ₀` with this `η` bound every such ensemble, the true
one included, by numbers computed from `G̃`, `ε` and `δ`.  If the hypotheses fail the procedure
reports that nothing is certified.

**Proposition N5 (the number of states) [P].**  (i) If `‖G̃ − G(μ)‖_op ≤ ε` for a `K`-mixture with
`λ_{3K}(G(μ)) > 2ε`, exactly `3K` eigenvalues of `G̃` exceed `ε`.  (ii) For any ensemble `ν` with
`‖G̃ − G(ν)‖_op ≤ ε`, `rank G(ν)` is at least the number of eigenvalues of `G̃` above `ε`: `ν` has at
least a third of that many states.  (iii) No bound from above: adding a state of weight
`t` to any ensemble changes `G` by at most `2tD_n²`.  *Proof.*  Weyl.  ∎

A rule with a fixed tolerance relative to the largest eigenvalue — the default of
`experiments/geometry/demix.py`, `10⁻⁸` — is the wrong rule for noisy data: this is our own
dead end DG-7 ("automatic detection of the number of states failed at noise `10⁻⁴`"), which
the Frontier division's intake quotes.  The threshold must be the error level; with it,
detection is correct up to half the smallest non-zero eigenvalue of `G` (`λ_m` in the table
of §8: between `0.09` and `5`), by (i).  [N: `robust_demix.py`, part "number of states".]

## 7. Inexact local geometry

**Proposition N6 [P; the constants N].**  Let `μ₀ = Σ w_kδ_{X_k}` be a `K`-mixture on `𝒞` with (CC),
`z` its centred stack, and let the data be exact.
(i) The mixtures of `K` configurations with `G(μ′) = G(μ₀)` are exactly those with states
`Y_j = zQΠ_jᵀ/√u_j`, `Q ∈ O(3K)`, `u` in the simplex: a family of dimension `9K(K − 1)/2 + K − 1`
modulo isometries of the states.  For `δ = 0` only `μ₀` is on `𝒞` (Theorem B); **for every
tolerance with all `δ_e > 0` a full neighbourhood of `μ₀` in the family is on `𝒞_δ`.**
(ii) To first order (`Q = exp(tΞ)`, `u = w + ta`) the displacement of state `k` and the vector of
all constraint violations are linear in `(Ξ, a)`; the largest ratio `c_tol,k` of their norms is
finite and is attained along a curve of the family.
(iii) Theorem N3 with `η = 0` certifies `d_P(Y_k, X_k) ≤ T_k‖viol‖ + O(‖viol‖²)` in its range, and
`c_tol,k ≤ T_k`.

*Proof.*  (i) Two `n × m` matrices of rank `m` with the same Gram matrix differ by an
orthogonal map on the right; `u_jY_jY_jᵀ` is the `j`-th block of `zQ` whatever `u_j` is; violations
are continuous and vanish at `(I, w)`.  (ii) Finiteness is the injectivity of the violation
map on `{Ξ` with zero diagonal blocks`} × {Σa = 0}`, the infinitesimal form of Theorem B.
(iii) The first-order identity of the proof of Theorem N3.  ∎

In the instances `c_tol` is between `0.7` and `1.8` and `T_k` between `3.6` and `8.2` (§8).  Example:
two states, 24 points, every squared constrained distance of every state off by one per
cent: `‖viol‖ = 0.19` squared bond lengths, so a state moves by at most `1.38 × 0.19 = 0.27` bond
lengths in Frobenius norm over the chain, `0.054` bond lengths in RMSD — to first order.  This
answers the second half of the Frontier division's G-3: the theorem survives as a
Lipschitz statement with a moderate constant, and it does not survive as uniqueness.

## 8. Numbers

`python3 experiments/geometry/robust_demix.py --table` (unit bonds, bond angle 111°, one random
mixture per row, seed 7; `η` is a Frobenius norm of an `n × n` matrix whose norm is `‖G‖`):

| `K` | `n` | `σ_c` | `λ_m` | `‖G‖` | `C_state` | `C_w` | `C_crude` | N2 holds up to `η =` | (weights `≥ w_min/2`) | N3 within 1.5 of first order up to | basin `φ₁` | `κ ≥` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 12 | `6.6·10⁻³` | `0.088` | 35 | 4.53 | 0.347 | `1.1·10⁵` | `1.8·10⁻⁶` | `3.6·10⁻⁵` | `1.6·10⁻⁸` | `6.6·10⁻⁷` | `5.8·10⁻¹⁰` |
| 2 | 16 | `0.11` | `0.54` | 49 | 1.47 | 0.091 | `3.1·10³` | `1.2·10⁻⁴` | `1.4·10⁻³` | `7.6·10⁻⁷` | `1.7·10⁻⁴` | `6.3·10⁻⁸` |
| 2 | 24 | `0.32` | `0.98` | 89 | 1.35 | 0.061 | `1.0·10³` | `3.4·10⁻⁴` | `5.7·10⁻³` | `2.6·10⁻⁶` | `1.5·10⁻³` | `1.6·10⁻⁷` |
| 2 | 40 | `1.3` | `5.3` | 276 | 0.68 | 0.018 | `2.0·10²` | `3.3·10⁻³` | `5.0·10⁻²` | `1.3·10⁻⁵` | `1.9·10⁻²` | `4.9·10⁻⁷` |
| 3 | 23 | `0.014` | `0.30` | 102 | 2.58 | 0.104 | `7.3·10⁴` | `3.1·10⁻⁶` | `7.0·10⁻⁵` | `1.9·10⁻⁸` | `3.1·10⁻⁶` | `3.8·10⁻¹⁰` |
| 3 | 30 | `0.15` | `0.64` | 141 | 2.16 | 0.040 | `5.4·10³` | `4.7·10⁻⁵` | `1.1·10⁻³` | `2.8·10⁻⁷` | `3.2·10⁻⁴` | `1.8·10⁻⁸` |
| 3 | 45 | `0.29` | `1.4` | 318 | 1.73 | 0.020 | `2.9·10³` | `1.1·10⁻⁴` | `3.0·10⁻³` | `4.6·10⁻⁷` | `1.2·10⁻³` | `2.0·10⁻⁸` |
| 4 | 39 | `1.2·10⁻³` | `0.51` | 254 | 4.06 | 0.043 | `1.4·10⁶` | `1.5·10⁻⁷` | `4.7·10⁻⁶` | `4.4·10⁻¹⁰` | `2.2·10⁻⁸` | `5.5·10⁻¹³` |
| 4 | 48 | `0.071` | `1.3` | 541 | 3.91 | 0.029 | `2.3·10⁴` | `1.6·10⁻⁵` | `4.3·10⁻⁴` | `2.1·10⁻⁸` | `7.3·10⁻⁵` | `1.0·10⁻⁹` |

(`C_state`: the largest over the states.  `C_crude`: the constant of Theorem N2 for small `η`.
Rows 1, 5 and 8 are at the conic thresholds `n₀(K) = 12, 23, 39`.)

**Reading.**
* *The problem is well conditioned to first order* — `C_state` is of order one, at the
  thresholds as well, and it decreases with the number of points.  `σ_c`, the number that
  the algorithm reports as its certificate, is small at the thresholds, and it governs the
  *certified range*, not the conditioning.  The two must not be confused: a small `σ_c` does
  not mean that the answer is inaccurate.
* *The certified ranges are far below realistic accuracy.*  The sharp constants are
  certified for relative errors `η/‖G‖` between `2·10⁻¹²` (four states at the threshold) and
  `5·10⁻⁸`; the crude linear bound up to between `6·10⁻¹⁰` and `2·10⁻⁴` when the weights of the
  competitor are bounded below.  For a chain with bond length `3.8` ångström and 40 points
  the best case corresponds to errors of the averaged squared distances of the order of
  `10⁻⁵` Å² per entry for the sharp constant and `10⁻²` Å² for the crude one — against squared
  distances of tens to hundreds of Å².  **As guarantees for data of realistic accuracy the
  theorems are empty**, like Theorem L⁺; what they establish is that the first-order
  constants are the truth in a neighbourhood, and how to compute them.
* *How far the first-order description extends is not known.*  An honest extrapolation,
  not a theorem: with `C_state = 0.68` for two states and 40 points, an error of the data of
  `η = 1.4` (per-entry errors of about 1 Å² in the squared distances at bond length 3.8 Å)
  would move a state by about `0.95` bond lengths in Frobenius norm, `0.6` Å in RMSD; but
  that `η` is a quarter of `λ_m`, well outside any range in which we can show that the
  linearisation is valid.
* *The checks* (`robust_demix.py` without arguments, about two and a half minutes; all pass):
  Lemma N0 and Theorem N1 on 65 to 92 chains per instance for which the hypothesis holds
  (largest distance/bound `0.007`: the bound is loose by a factor of 150 or more), on random
  chains and on chains that are nearly affine images of the stack — the smallest `φ` of
  such a chain at distance more than one bond length from every state is `0.067`, `0.47`,
  `0.35`, `0.76` in four instances, 70 to 1 100 times the certified basin; Theorem N1(a), (c) on
  split states with a spurious state of small weight; Theorem N2 on perturbed mixtures
  (largest error/bound `2·10⁻³`); Theorem N3, every step with the actual quantities, on
  random competitors and along the extremal direction (error/bound `1.000`,
  displacement/(`C_state η`) `= 1.000`); the a-posteriori procedure at noise `10⁻⁹` to `10⁻⁴`
  (truth inside the certified bound, which is 7 to 20 times the actual error in the sharp
  range and `10⁴` times at `10⁻⁴`); the tolerance family (data unchanged to `10⁻¹⁰`; ratio to
  `c_tol` `= 1.0000` along the extremal curve; Theorem N3 with the tolerance, error/bound up to
  `0.17`).

## 9. Prior art and novelty

* **The mechanism is standard perturbation theory.**  Error bounds for moment and
  simultaneous-diagonalisation methods under noise are in print for latent-variable models
  (Anandkumar, Ge, Hsu, Kakade and Telgarsky, 2012; Hsu and Kakade, 2013), for noisy joint
  diagonalisation (Kuleshov, Chaganty and Liang, 2015), and for **joint block
  diagonalisation** — the algebraic step of DEMIX — by Cai and Li (arXiv 1703.00591: an
  error bound under an explicit size condition, a backward error, a condition number).
  The first three are cited from search summaries; of the last, the abstract and §§1–2 were
  read through a page-reading agent and §3 only through its summary.  Weyl's inequalities,
  Eckart–Young, the Procrustes–Gram inequality and quantitative inverse-function arguments
  are classical.
* **Not found** (two summary-level searches, one paper opened — a thin basis): the
  statements for this problem; Lemma N0 and the enclosure of *all* ensembles by eigenvalue
  interlacing (Theorem N1), which is not a statement about diagonalisation; the explicit
  family and the first-order constant for a tolerance on the constraints (Proposition N6).
  We claim these as ours at the level of "an application of standard tools that we did
  not find written down", not as new techniques.
* Corollary N1.1 makes Theorem G(c) effective; the Ensemble division's E20″ (a certified
  modulus on a torus of torsions) is the analogous statement in its setting, obtained
  differently.

## 10. Limits

Exact arithmetic is not used: the constants are floating-point evaluations of singular
values, adequate for the comparisons made here and not a certificate in the sense of the
theory division's kernels.  Hypothesis (J) is checked numerically per instance.  The
tolerance model is a box on the squared constrained distances, the same for every state.
The noise model is a deterministic bound in Frobenius norm on the centred matrix; nothing
is proved about random noise, about missing entries (for those the note on label patterns
gives exact-data statements only), or below the conic threshold (the quartic certificate
has no stability analysis; O-15).  The observable remains the idealised one.  Unreviewed.
