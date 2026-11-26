import Mathlib

/-!
# Second-moment rigidity of conformational ensembles: the machine-checked core

Geometric Inference, Rigidity and Inverse Problems Division (branch `research/geometric-inference`).
Paper statements and proofs: `docs/geometry/ENSEMBLE_RIGIDITY.md`.  This file checks the algebraic and
linear-algebraic steps on which those proofs rest; it does **not** formalise measure-theoretic
ensembles, genericity, or the thresholds (which are exact computations, see `experiments/geometry/`).

## Contents

* **Stacking** (`stacked_sqdist`, Lemma 2.1): for a finite mixture with weights `w k ≥ 0` and states
  `x k : ι → E`, the stacked configuration `z i = (√(w k) • x k i)_k` in the `ℓ²` product satisfies
  `‖z i - z j‖² = ∑ k, w k * ‖x k i - x k j‖²`: an ensemble average of squared distances is a
  squared distance of one configuration in a higher dimension.
* **Stress energy** (`stress_energy_eq`): for a symmetric matrix `Ω` with zero row sums,
  `y ⬝ᵥ Ω *ᵥ y = -(1/2) ∑ i j, Ω i j * (y i - y j)²`, so the energy of a configuration is a linear
  function of its squared distances on the support of `Ω`.
* **Stress certificate** (`stress_certificate`, the core of Theorem F): if `Ω ⪰ 0` has zero row
  sums and annihilates every coordinate of every state of a reference mixture, then every
  coordinate of every state (of positive weight) of any mixture with the same averaged squared
  distances on the support of `Ω` lies in the kernel of `Ω`.
* **Block rigidity** (`block_rigidity`, the core of Theorem B): if a linear map `A` into a space of
  dimension at most `d` has `‖A (u + u')‖² = c k ‖u‖² + c l ‖u'‖²` on two orthogonal blocks of
  dimension `d ≥ 1`, then `c k = 0` or `c l = 0`; and `c k ≥ 0` (`block_coeff_nonneg`).  Hence a
  positive semidefinite block-scalar form of rank at most `d` is supported on a single block.
* **Theorem B, algebraic core end to end** (`mixture_state_of_conic`): under the conic condition —
  every symmetric bilinear form vanishing on the edge vectors is block-scalar — a linear map into
  a space of dimension at most `d` that preserves the lengths of the edge vectors is a scaled
  isometry on one block and vanishes on the others.
* **Lemma 2.2, finite form** (`exists_linearMap_of_gram_eq`, `state_is_linear_image`): families
  with the same Gram matrix are related by a linear isometry; hence every state of positive
  weight of a finite mixture with the averaged squared distances of a spanning configuration
  `z` is a linear image of `z`.
* **Theorem B for finite mixtures, end to end** (`finite_mixture_identifiable`): under the conic
  condition, every state of positive weight of a finite mixture with the averaged squared
  distances of `z` (all pairs) and the statewise edge lengths of `z` satisfies
  `‖Y i - Y i'‖² = c ‖comp k₀ (z i - z i')‖²` for one block `k₀`: it is similar to one of the
  states (blocks are abstract: pairwise orthogonal subspaces of dimension `d` with component maps).
* **Theorem B for finite mixtures, in coordinates** (`mixture_identifiable_stacked`): the same
  with the coordinate blocks of the `ℓ²` product and the stacked configuration of states `X k`
  with weights `w k > 0`, `∑ w = 1`, and common edge lengths on the constrained pairs: every
  state of positive weight of a competing finite mixture has the distance matrix of one of the
  `X k` (`SameShape`).  The conic condition and the spanning condition are hypotheses (they are
  the exact computations of `experiments/geometry/`); the weights of the competing mixture are
  not treated.  Non-vacuity with two different states, used end to end: `line_mixture_example`
  (`line_conic`, `line_span`, `line_states_differ`).
* **Affine flexes give mixtures** (`sqdist_midpoint_of_conic`, Theorem A (iii)⇒(ii)): if a symmetric
  matrix `S` vanishes on a set of edge vectors and `1 ± S` are positive semidefinite, there are
  linear maps `A₊, A₋` preserving the lengths of the edge vectors with
  `‖A₊ v‖² + ‖A₋ v‖² = 2 ‖v‖²` for every `v`, and `‖A₊ v‖² - ‖v‖² = v ⬝ᵥ S *ᵥ v`.
* **The hierarchy** (Theorem E, for finite mixtures): `secondMomentRigid_of_universal` (universal
  rigidity of the measured-plus-constrained framework reduces averaged data on a set of pairs to
  averaged data on all pairs — it does **not** by itself give second-moment rigidity:
  `universal_not_secondMomentRigid`, a counterexample found by the internal referee) and
  `globallyRigid_of_secondMomentRigid`.  The notion is called
  *second-moment rigidity* (rigidity under ensemble-averaged squared distances); "ensemble
  rigidity" is the Ensemble Identifiability Division's name for determination by the *laws* of
  the edge lengths, a different and weaker requirement on the framework (its Theorem E7).
* **Elementary identities** (`fourAtom_virtual_value_witness`, `block_rigidity_nonvacuous`): a
  number between two values is a convex combination of them (the four-atom obstruction in its
  simplest algebraic form), and the shape of the conclusion of `block_rigidity`.  They do not
  instantiate the hypotheses of a theorem of this file; the instance that does is
  `line_mixture_example` (section 7).
-/

namespace MetricChain.Geometry

open scoped BigOperators
open Finset Matrix

/-! ### 1. Stacking -/

section Stacking

variable {ι K E : Type*} [Fintype K] [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The stacked configuration of a finite mixture: `z i = (√(w k) • x k i)_k` in the `ℓ²` product. -/
noncomputable def stacked (w : K → ℝ) (x : K → ι → E) (i : ι) : PiLp 2 (fun _ : K => E) :=
  WithLp.toLp 2 (fun k => Real.sqrt (w k) • x k i)

/-- **Lemma 2.1 (stacking).**  The ensemble-averaged squared distance of a finite mixture is the
squared distance of the stacked configuration. -/
theorem stacked_sqdist (w : K → ℝ) (hw : ∀ k, 0 ≤ w k) (x : K → ι → E) (i j : ι) :
    ‖stacked w x i - stacked w x j‖ ^ 2 = ∑ k, w k * ‖x k i - x k j‖ ^ 2 := by
  rw [PiLp.norm_sq_eq_of_L2]
  refine Finset.sum_congr rfl fun k _ => ?_
  have h : (stacked w x i - stacked w x j) k = Real.sqrt (w k) • (x k i - x k j) := by
    simp [stacked, smul_sub]
  rw [h, norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt (hw k)]

end Stacking

/-! ### 2. Stress energy and the stress certificate -/

section Stress

variable {n : Type*} [Fintype n]

/-- For a symmetric matrix with zero row sums, the quadratic form is minus one half of the
`Ω`-weighted sum of squared differences. -/
theorem stress_energy_eq (Ω : Matrix n n ℝ) (hsymm : Ω.IsSymm) (hrow : ∀ i, ∑ j, Ω i j = 0)
    (y : n → ℝ) :
    y ⬝ᵥ Ω *ᵥ y = -(1 / 2) * ∑ i, ∑ j, Ω i j * (y i - y j) ^ 2 := by
  have hcol : ∀ j, ∑ i, Ω i j = 0 := by
    intro j
    rw [← hrow j]
    exact Finset.sum_congr rfl fun i _ => hsymm.apply j i
  have h1 : ∑ i, ∑ j, Ω i j * (y i) ^ 2 = 0 := by
    have : ∀ i, ∑ j, Ω i j * (y i) ^ 2 = (∑ j, Ω i j) * (y i) ^ 2 := fun i => by
      rw [Finset.sum_mul]
    simp [this, hrow]
  have h2 : ∑ i, ∑ j, Ω i j * (y j) ^ 2 = 0 := by
    rw [Finset.sum_comm]
    have : ∀ j, ∑ i, Ω i j * (y j) ^ 2 = (∑ i, Ω i j) * (y j) ^ 2 := fun j => by
      rw [Finset.sum_mul]
    simp [this, hcol]
  have h3 : y ⬝ᵥ Ω *ᵥ y = ∑ i, ∑ j, Ω i j * (y i * y j) := by
    simp only [dotProduct, mulVec, Finset.mul_sum]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => by ring
  have h4 : ∑ i, ∑ j, Ω i j * (y i - y j) ^ 2
      = ∑ i, ∑ j, Ω i j * (y i) ^ 2 + ∑ i, ∑ j, Ω i j * (y j) ^ 2
        - 2 * ∑ i, ∑ j, Ω i j * (y i * y j) := by
    rw [Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun j _ => by ring
  rw [h4, h1, h2, h3]
  ring

variable {J K C : Type*} [Fintype J] [Fintype K] [Fintype C]

/-- The `Ω`-energy of a finite mixture of configurations (coordinates `c : C`) is a linear function
of its averaged squared distances. -/
theorem mixture_energy_eq (Ω : Matrix n n ℝ) (hsymm : Ω.IsSymm) (hrow : ∀ i, ∑ j, Ω i j = 0)
    (v : J → ℝ) (Y : J → C → n → ℝ) :
    ∑ a, v a * ∑ c, (Y a c ⬝ᵥ Ω *ᵥ Y a c)
      = -(1 / 2) * ∑ i, ∑ j, Ω i j * ∑ a, v a * ∑ c, (Y a c i - Y a c j) ^ 2 := by
  have h : ∀ a, ∑ c, (Y a c ⬝ᵥ Ω *ᵥ Y a c)
      = -(1 / 2) * ∑ i, ∑ j, Ω i j * ∑ c, (Y a c i - Y a c j) ^ 2 := by
    intro a
    simp only [stress_energy_eq Ω hsymm hrow]
    rw [← Finset.mul_sum]
    congr 1
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Finset.mul_sum]
  simp only [h]
  rw [show ∑ a, v a * (-(1 / 2) * ∑ i, ∑ j, Ω i j * ∑ c, (Y a c i - Y a c j) ^ 2)
      = -(1 / 2) * ∑ a, ∑ i, ∑ j, Ω i j * (v a * ∑ c, (Y a c i - Y a c j) ^ 2) from by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun a _ => ?_
    rw [Finset.mul_sum, Finset.mul_sum, Finset.mul_sum]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [Finset.mul_sum, Finset.mul_sum, Finset.mul_sum]
    refine Finset.sum_congr rfl fun j _ => by ring]
  congr 1
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [Finset.mul_sum]

/-- **Stress certificate (core of Theorem F).**  Let `Ω` be positive semidefinite with zero row
sums.  Let a reference mixture (weights `w`, states `X`) have all coordinates of all states in the
kernel of `Ω`, and let a second mixture (weights `v ≥ 0`, states `Y`) have the same averaged squared
distances on every pair `i ≠ j` with `Ω i j ≠ 0`.  Then every coordinate of every state of positive
weight of the second mixture lies in the kernel of `Ω`: each such state is an affine image of the
kernel configuration. -/
theorem stress_certificate (Ω : Matrix n n ℝ) (hΩ : Ω.PosSemidef) (hrow : ∀ i, ∑ j, Ω i j = 0)
    (w : K → ℝ) (X : K → C → n → ℝ) (hX : ∀ k c, Ω *ᵥ X k c = 0)
    (v : J → ℝ) (hv : ∀ a, 0 ≤ v a) (Y : J → C → n → ℝ)
    (hdata : ∀ i j, Ω i j ≠ 0 →
      ∑ a, v a * ∑ c, (Y a c i - Y a c j) ^ 2 = ∑ k, w k * ∑ c, (X k c i - X k c j) ^ 2) :
    ∀ a, 0 < v a → ∀ c, Ω *ᵥ Y a c = 0 := by
  have hsymm : Ω.IsSymm := by
    have := hΩ.isHermitian
    simpa [Matrix.IsHermitian, Matrix.IsSymm, Matrix.conjTranspose_eq_transpose_of_trivial] using this
  have hnn : ∀ y : n → ℝ, 0 ≤ y ⬝ᵥ Ω *ᵥ y := fun y => by
    simpa using hΩ.dotProduct_mulVec_nonneg y
  -- the energies of the two mixtures agree
  have hE : ∑ a, v a * ∑ c, (Y a c ⬝ᵥ Ω *ᵥ Y a c) = ∑ k, w k * ∑ c, (X k c ⬝ᵥ Ω *ᵥ X k c) := by
    rw [mixture_energy_eq Ω hsymm hrow, mixture_energy_eq Ω hsymm hrow]
    congr 1
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    by_cases h : Ω i j = 0
    · simp [h]
    · rw [hdata i j h]
  have hX0 : ∑ k, w k * ∑ c, (X k c ⬝ᵥ Ω *ᵥ X k c) = 0 := by
    simp [hX]
  rw [hX0] at hE
  have hterm : ∀ a ∈ Finset.univ, 0 ≤ v a * ∑ c, (Y a c ⬝ᵥ Ω *ᵥ Y a c) := fun a _ =>
    mul_nonneg (hv a) (Finset.sum_nonneg fun c _ => hnn _)
  intro a ha c
  have h0 := (Finset.sum_eq_zero_iff_of_nonneg hterm).mp hE a (Finset.mem_univ a)
  have h1 : ∑ c, (Y a c ⬝ᵥ Ω *ᵥ Y a c) = 0 := by
    rcases mul_eq_zero.mp h0 with h | h
    · exact absurd h ha.ne'
    · exact h
  have h2 := (Finset.sum_eq_zero_iff_of_nonneg fun c _ => hnn (Y a c)).mp h1 c (Finset.mem_univ c)
  have := (hΩ.dotProduct_mulVec_zero_iff (Y a c)).mp (by simpa using h2)
  exact this

end Stress

/-! ### 3. Block rigidity -/

section Block

variable {V W : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
  [NormedAddCommGroup W] [InnerProductSpace ℝ W]

/-- A coefficient of a block-scalar form that is a squared norm is non-negative. -/
theorem block_coeff_nonneg (U : Submodule ℝ V) (hU : 0 < Module.finrank ℝ U)
    (A : V →ₗ[ℝ] W) (c : ℝ) (hA : ∀ u ∈ U, ‖A u‖ ^ 2 = c * ‖u‖ ^ 2) : 0 ≤ c := by
  haveI : Module.Finite ℝ U := Module.finite_of_finrank_pos hU
  haveI : Nontrivial U := Module.finrank_pos_iff.mp hU
  obtain ⟨u, hu⟩ := exists_ne (0 : U)
  have hu' : (u : V) ≠ 0 := fun h => hu (Subtype.ext h)
  have h := hA u u.2
  have hpos : 0 < ‖(u : V)‖ ^ 2 := by positivity
  by_contra hc
  have hc' : c < 0 := not_le.mp hc
  have : c * ‖(u : V)‖ ^ 2 < 0 := mul_neg_of_neg_of_pos hc' hpos
  nlinarith [sq_nonneg ‖A u‖]

/-- **Block rigidity (core of Theorem B).**  Let `U₁ ⟂ U₂` be two orthogonal subspaces of dimension
`d ≥ 1` and `A` a linear map into a space of dimension at most `d` such that
`‖A (u + u')‖² = c₁ ‖u‖² + c₂ ‖u'‖²` for `u ∈ U₁`, `u' ∈ U₂`.  Then `c₁ = 0` or `c₂ = 0`: a positive
semidefinite block-scalar quadratic form of rank at most `d` lives on one block. -/
theorem block_rigidity [FiniteDimensional ℝ W] (U₁ U₂ : Submodule ℝ V) (horth : U₁ ⟂ U₂) (d : ℕ) (hd : 0 < d)
    (h₁ : Module.finrank ℝ U₁ = d) (h₂ : Module.finrank ℝ U₂ = d)
    (hW : Module.finrank ℝ W ≤ d) (A : V →ₗ[ℝ] W) (c₁ c₂ : ℝ)
    (hA : ∀ u ∈ U₁, ∀ u' ∈ U₂, ‖A (u + u')‖ ^ 2 = c₁ * ‖u‖ ^ 2 + c₂ * ‖u'‖ ^ 2) :
    c₁ = 0 ∨ c₂ = 0 := by
  by_contra hne
  obtain ⟨hc₁, hc₂⟩ := not_or.mp hne
  have hpos₁ : 0 < Module.finrank ℝ U₁ := h₁ ▸ hd
  have hpos₂ : 0 < Module.finrank ℝ U₂ := h₂ ▸ hd
  haveI : FiniteDimensional ℝ U₁ := Module.finite_of_finrank_pos hpos₁
  haveI : FiniteDimensional ℝ U₂ := Module.finite_of_finrank_pos hpos₂
  have hn₁ : 0 ≤ c₁ := block_coeff_nonneg U₁ hpos₁ A c₁ fun u hu => by
    simpa using hA u hu 0 U₂.zero_mem
  have hn₂ : 0 ≤ c₂ := block_coeff_nonneg U₂ hpos₂ A c₂ fun u hu => by
    simpa using hA 0 U₁.zero_mem u hu
  have hp₁ : 0 < c₁ := lt_of_le_of_ne hn₁ (Ne.symm hc₁)
  have hp₂ : 0 < c₂ := lt_of_le_of_ne hn₂ (Ne.symm hc₂)
  -- `A` is injective on `U₁ ⊔ U₂`
  have hinj : Function.Injective (A.domRestrict (U₁ ⊔ U₂)) := by
    rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']
    intro x hx
    obtain ⟨u, hu, u', hu', hxu⟩ := Submodule.mem_sup.mp x.2
    have hAx : A (u + u') = 0 := by
      have : A (x : V) = 0 := by simpa [LinearMap.domRestrict_apply] using hx
      rwa [← hxu] at this
    have h := hA u hu u' hu'
    rw [hAx, norm_zero] at h
    have hu0 : ‖u‖ ^ 2 = 0 := by nlinarith [sq_nonneg ‖u‖, sq_nonneg ‖u'‖, mul_pos hp₁ hp₂]
    have hu'0 : ‖u'‖ ^ 2 = 0 := by nlinarith [sq_nonneg ‖u‖, sq_nonneg ‖u'‖, mul_pos hp₁ hp₂]
    have e1 : u = 0 := by simpa using hu0
    have e2 : u' = 0 := by simpa using hu'0
    apply Subtype.ext
    rw [← hxu, e1, e2]
    simp
  have hle : Module.finrank ℝ ↥(U₁ ⊔ U₂) ≤ Module.finrank ℝ W :=
    LinearMap.finrank_le_finrank_of_injective hinj
  have hsum := Submodule.finrank_sup_add_finrank_inf_eq U₁ U₂
  have hdisj : U₁ ⊓ U₂ = ⊥ := horth.disjoint.eq_bot
  rw [hdisj, finrank_bot, add_zero, h₁, h₂] at hsum
  omega

/-- **Theorem B, algebraic core end to end.**  Let `V` carry pairwise orthogonal blocks `U k` of
dimension `d ≥ 1` and let `Edges ⊆ V` satisfy the *conic condition*: every symmetric bilinear form
that vanishes on the edge vectors is block-scalar (`B u v = s k ⟪u, v⟫` on `U k × U k`, zero
between different blocks).  If a linear map `A` into a space of dimension at most `d` preserves
the lengths of the edge vectors (a competing state that is a linear image of the stacked
configuration and satisfies the statewise constraints), then `‖A u‖² = c k ‖u‖²` on every block
with `c k ≥ 0`, and at most one `c k` is non-zero: the state lives on a single block. -/
theorem mixture_state_of_conic [FiniteDimensional ℝ W] {K : Type*} [DecidableEq K]
    (U : K → Submodule ℝ V)
    (d : ℕ) (hd : 0 < d) (hdim : ∀ k, Module.finrank ℝ (U k) = d)
    (horth : ∀ k l, k ≠ l → U k ⟂ U l) (hW : Module.finrank ℝ W ≤ d) (Edges : Set V)
    (hCC : ∀ B : V →ₗ[ℝ] V →ₗ[ℝ] ℝ, (∀ u v, B u v = B v u) → (∀ e ∈ Edges, B e e = 0) →
      ∃ s : K → ℝ, ∀ k l, ∀ u ∈ U k, ∀ v ∈ U l,
        B u v = if k = l then s k * @inner ℝ V _ u v else 0)
    (A : V →ₗ[ℝ] W) (hA : ∀ e ∈ Edges, ‖A e‖ = ‖e‖) :
    ∃ c : K → ℝ, (∀ k, ∀ u ∈ U k, ‖A u‖ ^ 2 = c k * ‖u‖ ^ 2) ∧ (∀ k, 0 ≤ c k) ∧
      ∀ k l, k ≠ l → c k = 0 ∨ c l = 0 := by
  -- the symmetric bilinear form `⟪A u, A v⟫ - ⟪u, v⟫`
  let B : V →ₗ[ℝ] V →ₗ[ℝ] ℝ := (innerₗ W).compl₁₂ A A - innerₗ V
  have hB : ∀ u v, B u v = @inner ℝ W _ (A u) (A v) - @inner ℝ V _ u v := fun u v => by
    simp [B, LinearMap.sub_apply, LinearMap.compl₁₂_apply, innerₗ_apply_apply]
  have hsymm : ∀ u v, B u v = B v u := fun u v => by
    rw [hB, hB, real_inner_comm (A u), real_inner_comm u]
  have hedge : ∀ e ∈ Edges, B e e = 0 := fun e he => by
    rw [hB, real_inner_self_eq_norm_sq, real_inner_self_eq_norm_sq, hA e he, sub_self]
  obtain ⟨s, hs⟩ := hCC B hsymm hedge
  have hnorm : ∀ k, ∀ u ∈ U k, ‖A u‖ ^ 2 = (1 + s k) * ‖u‖ ^ 2 := by
    intro k u hu
    have h := hs k k u hu u hu
    rw [if_pos rfl, hB, real_inner_self_eq_norm_sq, real_inner_self_eq_norm_sq] at h
    linarith
  have hcross : ∀ k l, k ≠ l → ∀ u ∈ U k, ∀ u' ∈ U l, @inner ℝ W _ (A u) (A u') = 0 := by
    intro k l hkl u hu u' hu'
    have h := hs k l u hu u' hu'
    rw [if_neg hkl, hB] at h
    have horth' : @inner ℝ V _ u u' = 0 :=
      Submodule.isOrtho_iff_inner_eq.mp (horth k l hkl) u hu u' hu'
    linarith
  refine ⟨fun k => 1 + s k, hnorm, fun k => ?_, fun k l hkl => ?_⟩
  · exact block_coeff_nonneg (U k) (hdim k ▸ hd) A (1 + s k) (hnorm k)
  · refine block_rigidity (U k) (U l) (horth k l hkl) d hd (hdim k) (hdim l) hW A (1 + s k) (1 + s l) ?_
    intro u hu u' hu'
    rw [map_add, @norm_add_sq_real, hnorm k u hu, hnorm l u' hu', hcross k l hkl u hu u' hu']
    ring

end Block

/-! ### 3b. Lemma 2.2 for finite mixtures, and Theorem B end to end -/

section FiniteMixture

variable {ι V W : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
  [NormedAddCommGroup W] [InnerProductSpace ℝ W]

/-- Linear combinations of two families with the same Gram matrix have the same inner products. -/
theorem inner_linearCombination_eq_of_gram (z : ι → V) (y : ι → W)
    (hgram : ∀ i j, @inner ℝ V _ (z i) (z j) = @inner ℝ W _ (y i) (y j)) (c d : ι →₀ ℝ) :
    @inner ℝ V _ (Finsupp.linearCombination ℝ z c) (Finsupp.linearCombination ℝ z d)
      = @inner ℝ W _ (Finsupp.linearCombination ℝ y c) (Finsupp.linearCombination ℝ y d) := by
  simp only [Finsupp.linearCombination_apply, Finsupp.sum_inner, Finsupp.inner_sum,
    real_inner_smul_left, real_inner_smul_right, hgram]

/-- **Lemma 2.2, finite form.**  If a family `z` spans `V` and a family `y` in `W` has the same
Gram matrix, there is a linear map `A : V → W` with `A (z i) = y i` that preserves inner products
(a linear isometry onto its image). -/
theorem exists_linearMap_of_gram_eq (z : ι → V) (y : ι → W)
    (hspan : Submodule.span ℝ (Set.range z) = ⊤)
    (hgram : ∀ i j, @inner ℝ V _ (z i) (z j) = @inner ℝ W _ (y i) (y j)) :
    ∃ A : V →ₗ[ℝ] W, (∀ i, A (z i) = y i) ∧
      ∀ u v, @inner ℝ W _ (A u) (A v) = @inner ℝ V _ u v := by
  set Lz := Finsupp.linearCombination ℝ z with hLz
  set Ly := Finsupp.linearCombination ℝ y with hLy
  have hsurj : Function.Surjective Lz := by
    rw [← LinearMap.range_eq_top, hLz, Finsupp.range_linearCombination, hspan]
  have hker : LinearMap.ker Lz ≤ LinearMap.ker Ly := by
    intro c hc
    rw [LinearMap.mem_ker] at hc ⊢
    have h := inner_linearCombination_eq_of_gram z y hgram c c
    rw [← hLz, ← hLy, hc, inner_zero_left] at h
    exact inner_self_eq_zero.mp h.symm
  let e := Lz.quotKerEquivOfSurjective hsurj
  let A : V →ₗ[ℝ] W := ((LinearMap.ker Lz).liftQ Ly hker).comp e.symm.toLinearMap
  have hA : ∀ c : ι →₀ ℝ, A (Lz c) = Ly c := by
    intro c
    have : e.symm (Lz c) = Submodule.Quotient.mk c := by
      rw [LinearEquiv.symm_apply_eq]
      rfl
    simp [A, this]
  refine ⟨A, fun i => ?_, fun u v => ?_⟩
  · have := hA (Finsupp.single i 1)
    simpa [hLz, hLy] using this
  · obtain ⟨c, rfl⟩ := hsurj u
    obtain ⟨d, rfl⟩ := hsurj v
    rw [hA, hA]
    exact (inner_linearCombination_eq_of_gram z y hgram c d).symm

/-- Equal distances give equal Gram matrices of the differences from a base point. -/
theorem inner_sub_eq_of_dist_eq (z : ι → V) (y : ι → W)
    (h : ∀ i j, ‖z i - z j‖ ^ 2 = ‖y i - y j‖ ^ 2) (i₀ i j : ι) :
    @inner ℝ V _ (z i - z i₀) (z j - z i₀) = @inner ℝ W _ (y i - y i₀) (y j - y i₀) := by
  have e1 := @norm_sub_sq_real V _ _ (z i - z i₀) (z j - z i₀)
  have e2 := @norm_sub_sq_real W _ _ (y i - y i₀) (y j - y i₀)
  have hz : z i - z i₀ - (z j - z i₀) = z i - z j := by abel
  have hy : y i - y i₀ - (y j - y i₀) = y i - y j := by abel
  rw [hz] at e1
  rw [hy] at e2
  have a := h i j
  have b := h i i₀
  have c := h j i₀
  linarith

/-- **Lemma 2.2 for finite mixtures.**  If a finite mixture `(v, Y)` of configurations in `W` has
the averaged squared distances of a configuration `z` in `V` whose differences from a base point
span `V`, then every state of positive weight is a linear image of `z`:
`Y j i - Y j i' = A (z i - z i')`. -/
theorem state_is_linear_image {J : Type*} [Fintype J] (z : ι → V) (i₀ : ι)
    (hspan : Submodule.span ℝ (Set.range fun i => z i - z i₀) = ⊤)
    (v : J → ℝ) (hv : ∀ j, 0 ≤ v j) (Y : J → ι → W)
    (hdata : ∀ i i', ∑ j, v j * ‖Y j i - Y j i'‖ ^ 2 = ‖z i - z i'‖ ^ 2)
    (j : J) (hj : 0 < v j) :
    ∃ A : V →ₗ[ℝ] W, ∀ i i', Y j i - Y j i' = A (z i - z i') := by
  have hgram := inner_sub_eq_of_dist_eq z (stacked v Y)
    (fun i i' => by rw [stacked_sqdist v hv, hdata]) i₀
  obtain ⟨T, hT, -⟩ := exists_linearMap_of_gram_eq (fun i => z i - z i₀)
    (fun i => stacked v Y i - stacked v Y i₀) hspan hgram
  have hsq : Real.sqrt (v j) ≠ 0 := (Real.sqrt_pos.mpr hj).ne'
  let A : V →ₗ[ℝ] W := (Real.sqrt (v j))⁻¹ • ((PiLp.projₗ 2 (fun _ : J => W) j).comp T)
  have hA0 : ∀ i, A (z i - z i₀) = Y j i - Y j i₀ := by
    intro i
    have h1 : (stacked v Y i - stacked v Y i₀) j = Real.sqrt (v j) • (Y j i - Y j i₀) := by
      simp [stacked, smul_sub]
    simp only [A, LinearMap.smul_apply, LinearMap.comp_apply, hT]
    change (Real.sqrt (v j))⁻¹ • ((stacked v Y i - stacked v Y i₀) j) = _
    rw [h1, smul_smul, inv_mul_cancel₀ hsq, one_smul]
  refine ⟨A, fun i i' => ?_⟩
  have hz : z i - z i' = (z i - z i₀) - (z i' - z i₀) := by abel
  rw [hz, map_sub, hA0, hA0]
  abel

/-- **Theorem B for finite mixtures, end to end.**  Let `z : ι → V` be a configuration whose
differences from a base point span `V`; let `V` carry pairwise orthogonal blocks `U k` of
dimension `d ≥ 1` with block components `comp k` (`comp k v ∈ U k`, `∑ k, comp k v = v`); let
`E₀` be the set of statewise-constrained pairs and assume the **conic condition**: every
symmetric bilinear form on `V` that vanishes on the constrained edge vectors `z p.1 - z p.2`
(`p ∈ E₀`) is block-scalar.  Let `(v, Y)` be a finite mixture of configurations in a space `W`
of dimension at most `d` such that every state of positive weight has the edge lengths of `z`
on `E₀` (statewise constraints) and the mixture has the squared distances of `z` on average
(same averaged data, all pairs).  Then every state of positive weight lives on one block: there
are `k₀` and `c ≥ 0` with `‖Y j i - Y j i'‖² = c * ‖comp k₀ (z i - z i')‖²` for all `i, i'`.

In the stacked configuration of a mixture `∑ w_k δ_{X_k}`, `‖comp k (z i - z i')‖² =
w_k ‖X_k i - X_k i'‖²`, so the conclusion says that the state `Y j` is similar to the state
`X_{k₀}`, and congruent to it as soon as one constrained edge has non-zero length. -/
theorem finite_mixture_identifiable [FiniteDimensional ℝ W] {K J : Type*} [Fintype K]
    [DecidableEq K] [Nonempty K] [Fintype J]
    (U : K → Submodule ℝ V) (d : ℕ) (hd : 0 < d) (hdim : ∀ k, Module.finrank ℝ (U k) = d)
    (horth : ∀ k l, k ≠ l → U k ⟂ U l) (hW : Module.finrank ℝ W ≤ d)
    (comp : K → V →ₗ[ℝ] V) (hcomp_mem : ∀ k x, comp k x ∈ U k)
    (hcomp_sum : ∀ x, ∑ k, comp k x = x)
    (z : ι → V) (i₀ : ι) (hspan : Submodule.span ℝ (Set.range fun i => z i - z i₀) = ⊤)
    (E₀ : Set (ι × ι))
    (hCC : ∀ B : V →ₗ[ℝ] V →ₗ[ℝ] ℝ, (∀ u x, B u x = B x u) →
      (∀ p ∈ E₀, B (z p.1 - z p.2) (z p.1 - z p.2) = 0) →
      ∃ s : K → ℝ, ∀ k l, ∀ u ∈ U k, ∀ x ∈ U l,
        B u x = if k = l then s k * @inner ℝ V _ u x else 0)
    (v : J → ℝ) (hv : ∀ j, 0 ≤ v j) (Y : J → ι → W)
    (hstate : ∀ j, 0 < v j → ∀ p ∈ E₀, ‖Y j p.1 - Y j p.2‖ = ‖z p.1 - z p.2‖)
    (hdata : ∀ i i', ∑ j, v j * ‖Y j i - Y j i'‖ ^ 2 = ‖z i - z i'‖ ^ 2)
    (j : J) (hj : 0 < v j) :
    ∃ (k₀ : K) (c : ℝ), 0 ≤ c ∧
      ∀ i i', ‖Y j i - Y j i'‖ ^ 2 = c * ‖comp k₀ (z i - z i')‖ ^ 2 := by
  obtain ⟨A, hA⟩ := state_is_linear_image z i₀ hspan v hv Y hdata j hj
  -- the conic condition in the form needed by `mixture_state_of_conic`
  have hCC' : ∀ B : V →ₗ[ℝ] V →ₗ[ℝ] ℝ, (∀ u x, B u x = B x u) →
      (∀ e ∈ {e : V | ∃ p ∈ E₀, e = z p.1 - z p.2}, B e e = 0) →
      ∃ s : K → ℝ, ∀ k l, ∀ u ∈ U k, ∀ x ∈ U l,
        B u x = if k = l then s k * @inner ℝ V _ u x else 0 := by
    intro B hsym hedge
    exact hCC B hsym fun p hp => hedge _ ⟨p, hp, rfl⟩
  have hAedge : ∀ e ∈ {e : V | ∃ p ∈ E₀, e = z p.1 - z p.2}, ‖A e‖ = ‖e‖ := by
    rintro e ⟨p, hp, rfl⟩
    rw [← hA]
    exact hstate j hj p hp
  obtain ⟨c, hc, hc0, hcone⟩ :=
    mixture_state_of_conic U d hd hdim horth hW _ hCC' A hAedge
  -- a block with a non-zero coefficient, if there is one
  have hvanish : ∀ k, c k = 0 → ∀ x, A (comp k x) = 0 := by
    intro k hk x
    have h := hc k (comp k x) (hcomp_mem k x)
    rw [hk, zero_mul] at h
    exact norm_eq_zero.mp (by nlinarith [norm_nonneg (A (comp k x))])
  by_cases hex : ∃ k, c k ≠ 0
  · obtain ⟨k₀, hk₀⟩ := hex
    refine ⟨k₀, c k₀, hc0 k₀, fun i i' => ?_⟩
    have hAx : A (z i - z i') = A (comp k₀ (z i - z i')) := by
      conv_lhs => rw [← hcomp_sum (z i - z i'), map_sum]
      refine Finset.sum_eq_single k₀ (fun k _ hk => ?_) (fun h => absurd (Finset.mem_univ _) h)
      rcases hcone k k₀ hk with h | h
      · exact hvanish k h _
      · exact absurd h hk₀
    rw [hA, hAx, hc k₀ _ (hcomp_mem k₀ _)]
  · have hall : ∀ k, c k = 0 := fun k => by
      by_contra h
      exact hex ⟨k, h⟩
    obtain ⟨k₀⟩ := ‹Nonempty K›
    refine ⟨k₀, 0, le_refl 0, fun i i' => ?_⟩
    have hAx : A (z i - z i') = 0 := by
      rw [← hcomp_sum (z i - z i'), map_sum]
      exact Finset.sum_eq_zero fun k _ => hvanish k (hall k) _
    rw [hA, hAx, norm_zero]
    ring

end FiniteMixture

/-! ### 4. Affine flexes give mixtures -/

section Midpoint

open scoped MatrixOrder

variable {m : Type*} [Fintype m] [DecidableEq m]

/-- **Theorem A, (iii) ⇒ (ii).**  If a symmetric matrix `S` vanishes on the edge vectors
(`e ⬝ᵥ S *ᵥ e = 0`) and `1 + S`, `1 - S` are positive semidefinite, then there are linear maps
`A₊`, `A₋` that preserve the squared lengths of all edge vectors, with
`‖A₊ v‖² - ‖v‖² = v ⬝ᵥ S *ᵥ v` and `‖A₊ v‖² + ‖A₋ v‖² = 2 ‖v‖²` for every `v`: the configuration is
the midpoint, in squared distances, of its two affine images, which satisfy the same statewise
constraints. -/
theorem sqdist_midpoint_of_conic (S : Matrix m m ℝ)
    (hp : (1 + S).PosSemidef) (hm : (1 - S).PosSemidef)
    (edges : Set (m → ℝ)) (hconic : ∀ e ∈ edges, e ⬝ᵥ S *ᵥ e = 0) :
    ∃ Ap Am : Matrix m m ℝ,
      (∀ e ∈ edges, (Ap *ᵥ e) ⬝ᵥ (Ap *ᵥ e) = e ⬝ᵥ e ∧ (Am *ᵥ e) ⬝ᵥ (Am *ᵥ e) = e ⬝ᵥ e) ∧
      (∀ v, (Ap *ᵥ v) ⬝ᵥ (Ap *ᵥ v) - v ⬝ᵥ v = v ⬝ᵥ S *ᵥ v) ∧
      (∀ v, (Ap *ᵥ v) ⬝ᵥ (Ap *ᵥ v) + (Am *ᵥ v) ⬝ᵥ (Am *ᵥ v) = 2 * (v ⬝ᵥ v)) := by
  obtain ⟨Bp, hBp⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hp.nonneg
  obtain ⟨Bm, hBm⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hm.nonneg
  have key : ∀ (B P : Matrix m m ℝ), P = star B * B → ∀ v : m → ℝ,
      (B *ᵥ v) ⬝ᵥ (B *ᵥ v) = v ⬝ᵥ P *ᵥ v := by
    intro B P hP v
    rw [hP, ← Matrix.mulVec_mulVec, Matrix.dotProduct_mulVec _ _ (B *ᵥ v), star_eq_conjTranspose,
      Matrix.conjTranspose_eq_transpose_of_trivial, Matrix.vecMul_transpose]
  have hplus : ∀ v : m → ℝ, v ⬝ᵥ (1 + S) *ᵥ v = v ⬝ᵥ v + v ⬝ᵥ S *ᵥ v := fun v => by
    rw [Matrix.add_mulVec, Matrix.one_mulVec, dotProduct_add]
  have hminus : ∀ v : m → ℝ, v ⬝ᵥ (1 - S) *ᵥ v = v ⬝ᵥ v - v ⬝ᵥ S *ᵥ v := fun v => by
    rw [Matrix.sub_mulVec, Matrix.one_mulVec, dotProduct_sub]
  refine ⟨Bp, Bm, ?_, ?_, ?_⟩
  · intro e he
    rw [key Bp _ hBp, key Bm _ hBm, hplus, hminus, hconic e he]
    simp
  · intro v
    rw [key Bp _ hBp, hplus]
    ring
  · intro v
    rw [key Bp _ hBp, key Bm _ hBm, hplus, hminus]
    ring

end Midpoint

/-! ### 5. The hierarchy: (universal rigidity and the conic condition) ⇒ second-moment rigidity ⇒
global rigidity (finite mixtures) -/

section Hierarchy

universe u

variable {ι : Type*}

/-- Two configurations have the same lengths on a set of pairs. -/
def SameLengths {E E' : Type*} [NormedAddCommGroup E] [NormedAddCommGroup E']
    (G : Set (ι × ι)) (x : ι → E) (y : ι → E') : Prop :=
  ∀ p ∈ G, ‖x p.1 - x p.2‖ = ‖y p.1 - y p.2‖

/-- Two configurations have the same distance matrix (for point configurations in Euclidean
spaces this is congruence). -/
def SameShape {E E' : Type*} [NormedAddCommGroup E] [NormedAddCommGroup E']
    (x : ι → E) (y : ι → E') : Prop :=
  ∀ i j, ‖x i - x j‖ = ‖y i - y j‖

/-- Global rigidity of the framework `(G, x)` in its own ambient space. -/
def GloballyRigid {E : Type u} [NormedAddCommGroup E] (G : Set (ι × ι)) (x : ι → E) : Prop :=
  ∀ y : ι → E, SameLengths G x y → SameShape x y

/-- Universal rigidity of the framework `(G, x)`: rigidity among configurations in every real
inner product space (of the same universe). -/
def UniversallyRigid {E : Type u} [NormedAddCommGroup E] (G : Set (ι × ι)) (x : ι → E) : Prop :=
  ∀ (E' : Type u) [NormedAddCommGroup E'] [InnerProductSpace ℝ E'] (y : ι → E'),
    SameLengths G x y → SameShape x y

/-- `F`-second-moment rigidity for finite mixtures: every finite mixture of configurations of the same
ambient space that satisfy the statewise constraints `E₀` of `x` and reproduce the squared
distances of `x` on `F` *on average* consists of copies of `x`. -/
def SecondMomentRigid {E : Type u} [NormedAddCommGroup E] (E₀ F : Set (ι × ι)) (x : ι → E) : Prop :=
  ∀ (K : Type u) [Fintype K] (w : K → ℝ) (Y : K → ι → E),
    (∀ k, 0 ≤ w k) → ∑ k, w k = 1 → (∀ k, SameLengths E₀ x (Y k)) →
    (∀ p ∈ F, ∑ k, w k * ‖Y k p.1 - Y k p.2‖ ^ 2 = ‖x p.1 - x p.2‖ ^ 2) →
    ∀ k, 0 < w k → SameShape x (Y k)

variable {E : Type u} [NormedAddCommGroup E]

/-- **Theorem E(b), first half.**  Second-moment rigidity implies global rigidity of the framework on
the measured and the constrained pairs: a competing configuration is a one-state ensemble. -/
theorem globallyRigid_of_secondMomentRigid (E₀ F : Set (ι × ι)) (x : ι → E)
    (h : SecondMomentRigid E₀ F x) : GloballyRigid (F ∪ E₀) x := by
  intro y hy
  have := h PUnit (fun _ => 1) (fun _ => y) (fun _ => zero_le_one) (by simp)
    (fun _ p hp => hy p (Or.inr hp))
    (fun p hp => by simp [hy p (Or.inl hp)]) PUnit.unit zero_lt_one
  exact this

/-- **Theorem E(a), the reduction.**  If the framework on the measured and the constrained pairs
is universally rigid, averaged data on the measured pairs are as good as averaged data on all
pairs: second-moment rigidity with respect to all pairs implies second-moment rigidity with respect to `F`.
(The stacked configuration of a competing mixture has the lengths of `x` on `F ∪ E₀`, hence all its
distances; so the mixture reproduces all squared distances of `x` on average.) -/
theorem secondMomentRigid_of_universal [InnerProductSpace ℝ E] (E₀ F : Set (ι × ι)) (x : ι → E)
    (hU : UniversallyRigid (F ∪ E₀) x) (hfull : SecondMomentRigid E₀ Set.univ x) :
    SecondMomentRigid E₀ F x := by
  intro K _ w Y hw hsum hE₀ hF k hk
  refine hfull K w Y hw hsum hE₀ ?_ k hk
  intro p _
  -- the stacked configuration has the lengths of `x` on `F ∪ E₀`
  have hstack : SameLengths (F ∪ E₀) x (stacked w Y) := by
    intro q hq
    have hsq : ‖stacked w Y q.1 - stacked w Y q.2‖ ^ 2 = ‖x q.1 - x q.2‖ ^ 2 := by
      rw [stacked_sqdist w hw]
      rcases hq with hq | hq
      · exact hF q hq
      · have : ∀ k, w k * ‖Y k q.1 - Y k q.2‖ ^ 2 = w k * ‖x q.1 - x q.2‖ ^ 2 := fun k => by
          rw [hE₀ k q hq]
        simp only [this]
        rw [← Finset.sum_mul, hsum, one_mul]
    have h1 : 0 ≤ ‖stacked w Y q.1 - stacked w Y q.2‖ := norm_nonneg _
    have h2 : 0 ≤ ‖x q.1 - x q.2‖ := norm_nonneg _
    nlinarith [sq_nonneg (‖stacked w Y q.1 - stacked w Y q.2‖ - ‖x q.1 - x q.2‖)]
  have hshape := hU (PiLp 2 (fun _ : K => E)) (stacked w Y) hstack p.1 p.2
  rw [← stacked_sqdist w hw, hshape]

/-- **The conic hypothesis of `secondMomentRigid_of_universal` cannot be dropped.**  Three points
`x = (1, 0, i)` in `ℂ = ℝ²`, statewise constraints `E₀` = the path `0–1–2` (two unit bonds at a
right angle), measured pair `F = {(0, 2)}`.  `F ∪ E₀` is the complete graph, so the framework is
universally rigid; but the straight and the folded chain, `(1, 0, -1)` and `(1, 0, 1)`, with
weights `1/2`, have the same bond lengths and the same *average* squared distance
`2 = ‖1 - i‖²` on `F`.  So universal rigidity of `(F ∪ E₀, x)` does not imply `F`-second-moment
rigidity.  (Counterexample and proof by the referee of the internal review GEOMETRY-REV-0001,
finding M1; the summary of the report had claimed the implication.) -/
theorem universal_not_secondMomentRigid :
    ∃ (x : Fin 3 → ℂ) (E₀ F : Set (Fin 3 × Fin 3)),
      UniversallyRigid (F ∪ E₀) x ∧ ¬ SecondMomentRigid E₀ F x := by
  refine ⟨![1, 0, Complex.I], {(0, 1), (1, 2)}, {(0, 2)}, ?_, ?_⟩
  · intro E' _ _ y hy i j
    have h01 := hy (0, 1) (by simp)
    have h12 := hy (1, 2) (by simp)
    have h02 := hy (0, 2) (by simp)
    have h10 : ‖(![1, 0, Complex.I] : Fin 3 → ℂ) 1 - (![1, 0, Complex.I] : Fin 3 → ℂ) 0‖
        = ‖y 1 - y 0‖ := by
      rw [norm_sub_rev, norm_sub_rev (y 1)]; exact h01
    have h21 : ‖(![1, 0, Complex.I] : Fin 3 → ℂ) 2 - (![1, 0, Complex.I] : Fin 3 → ℂ) 1‖
        = ‖y 2 - y 1‖ := by
      rw [norm_sub_rev, norm_sub_rev (y 2)]; exact h12
    have h20 : ‖(![1, 0, Complex.I] : Fin 3 → ℂ) 2 - (![1, 0, Complex.I] : Fin 3 → ℂ) 0‖
        = ‖y 2 - y 0‖ := by
      rw [norm_sub_rev, norm_sub_rev (y 2)]; exact h02
    fin_cases i <;> fin_cases j
    · simp
    · exact h01
    · exact h02
    · exact h10
    · simp
    · exact h12
    · exact h20
    · exact h21
    · simp
  · intro h
    have key := h Bool (fun _ => (1 / 2 : ℝ))
      (fun b => if b then (![1, 0, -1] : Fin 3 → ℂ) else ![1, 0, 1])
      (fun _ => by norm_num) (by simp) ?_ ?_ false (by norm_num) 0 2
    · -- the folded state has ‖Y 0 - Y 2‖ = 0 but ‖x 0 - x 2‖ = ‖1 - i‖ ≠ 0
      simp at key
      have : (1 : ℂ) - Complex.I = 0 := by simpa using key
      have h1 := congrArg Complex.re this
      simp at h1
    · intro b p hp
      rcases hp with rfl | rfl <;> cases b <;> simp
    · intro p hp
      have hp' : p = (0, 2) := hp
      subst hp'
      have h2 : ‖(1 : ℂ) - Complex.I‖ ^ 2 = 2 := by
        rw [← Complex.normSq_eq_norm_sq]
        simp [Complex.normSq_apply]
        norm_num
      simp [h2]
      norm_num

end Hierarchy

/-! ### 6. Non-vacuity -/

/-- The four-atom obstruction in its simplest form: any value strictly between two attainable
squared distances is the average of the two with positive weights — a "virtual" value that no
single state need have. -/
theorem fourAtom_virtual_value_witness (a b t : ℝ) (ht : a < t ∧ t < b) :
    ∃ w₁ w₂ : ℝ, 0 < w₁ ∧ 0 < w₂ ∧ w₁ + w₂ = 1 ∧ w₁ * a + w₂ * b = t := by
  have hne : b - a ≠ 0 := by linarith
  refine ⟨(b - t) / (b - a), (t - a) / (b - a), ?_, ?_, ?_, ?_⟩
  · exact div_pos (by linarith) (by linarith)
  · exact div_pos (by linarith) (by linarith)
  · rw [← add_div, div_eq_iff hne]
    ring
  · rw [div_mul_eq_mul_div, div_mul_eq_mul_div, ← add_div, div_eq_iff hne]
    ring

/-- `block_rigidity` is not vacuous: on `ℝ × ℝ` with the two coordinate axes as blocks (`d = 1`),
the first projection into `ℝ` has block coefficients `(1, 0)`. -/
theorem block_rigidity_nonvacuous :
    ∃ (c₁ c₂ : ℝ), (c₁ = 0 ∨ c₂ = 0) ∧ c₁ ≠ 0 ∧
      ∀ u u' : ℝ, ‖(u : ℝ)‖ ^ 2 = c₁ * ‖u‖ ^ 2 + c₂ * ‖u'‖ ^ 2 :=
  ⟨1, 0, Or.inr rfl, one_ne_zero, fun u u' => by ring⟩

/-- The conic condition of `finite_mixture_identifiable` is satisfiable: on the line, with one
block and one constrained edge, every symmetric bilinear form that vanishes on the edge vector
vanishes identically (the one-state, one-dimensional instance). -/
theorem conic_condition_line (B : ℝ →ₗ[ℝ] ℝ →ₗ[ℝ] ℝ) (hB : B 1 1 = 0) :
    ∀ u x : ℝ, B u x = 0 * @inner ℝ ℝ _ u x := by
  intro u x
  have e1 : B u x = x * B u 1 := by
    have := (B u).map_smul x (1 : ℝ)
    simpa using this
  have e2 : B u 1 = u * B 1 1 := by
    have h2 := congrArg (fun f : ℝ →ₗ[ℝ] ℝ => f 1) (B.map_smul u (1 : ℝ))
    simpa using h2
  rw [e1, e2, hB]
  ring


/-! ### 7. Theorem B for finite mixtures in coordinates: the stacked configuration -/

section Concrete

variable {ι K E : Type*} [Fintype K] [DecidableEq K]
  [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The inclusion of the `k`-th coordinate block into the `ℓ²` product, as a linear map. -/
noncomputable def blockIncl (k : K) : E →ₗ[ℝ] PiLp 2 (fun _ : K => E) :=
  (WithLp.linearEquiv 2 ℝ (K → E)).symm.toLinearMap ∘ₗ LinearMap.single ℝ (fun _ : K => E) k

omit [Fintype K] in
theorem blockIncl_apply (k l : K) (a : E) :
    (blockIncl k a : PiLp 2 (fun _ : K => E)) l = if l = k then a else 0 := by
  simp only [blockIncl, LinearMap.comp_apply, LinearMap.single_apply]
  change (Pi.single k a : K → E) l = _
  rw [Pi.single_apply]

/-- The component of a vector of the `ℓ²` product in the `k`-th coordinate block. -/
noncomputable def blockComp (k : K) : PiLp 2 (fun _ : K => E) →ₗ[ℝ] PiLp 2 (fun _ : K => E) :=
  (blockIncl k).comp (PiLp.projₗ 2 (fun _ : K => E) k)

omit [Fintype K] in
theorem blockComp_apply (k l : K) (x : PiLp 2 (fun _ : K => E)) :
    blockComp k x l = if l = k then x k else 0 := by
  simp [blockComp, blockIncl_apply]

theorem blockComp_sum (x : PiLp 2 (fun _ : K => E)) : ∑ k, blockComp k x = x := by
  ext l
  simp [blockComp_apply]

theorem norm_blockComp (k : K) (x : PiLp 2 (fun _ : K => E)) : ‖blockComp k x‖ = ‖x k‖ := by
  have h : ‖blockComp k x‖ ^ 2 = ‖x k‖ ^ 2 := by
    rw [PiLp.norm_sq_eq_of_L2]
    rw [Finset.sum_eq_single k]
    · simp [blockComp_apply]
    · intro l _ hl
      simp [blockComp_apply, hl]
    · intro h
      exact absurd (Finset.mem_univ k) h
  have h1 : 0 ≤ ‖blockComp k x‖ := norm_nonneg _
  have h2 : 0 ≤ ‖x k‖ := norm_nonneg _
  nlinarith [sq_nonneg (‖blockComp k x‖ - ‖x k‖)]

omit [Fintype K] in
theorem blockIncl_injective (k : K) : Function.Injective (blockIncl (E := E) k) := by
  intro a b h
  have := congrArg (fun x : PiLp 2 (fun _ : K => E) => x k) h
  simpa [blockIncl_apply] using this

theorem blocks_ortho (k l : K) (h : k ≠ l) :
    LinearMap.range (blockIncl (E := E) k) ⟂ LinearMap.range (blockIncl (E := E) l) := by
  rw [Submodule.isOrtho_iff_inner_eq]
  rintro _ ⟨a, rfl⟩ _ ⟨b, rfl⟩
  rw [PiLp.inner_apply]
  refine Finset.sum_eq_zero fun m _ => ?_
  rw [blockIncl_apply, blockIncl_apply]
  by_cases hm : m = k
  · subst hm
    simp [h]
  · simp [hm]

/-- **Theorem B for finite mixtures, in coordinates.**  Let `X k : ι → E` (`k : K`) be states in
a space `E` of dimension `d ≥ 1` with positive weights `w k` summing to one, all with the same
edge lengths `ℓ p` on the constrained pairs `E₀`, and let `z = stacked w X` be their stacked
configuration.  Assume that the differences of `z` from a base point span the stacked space and
that the **conic condition** holds: every symmetric bilinear form on the stacked space that
vanishes on the constrained edge vectors of `z` is block-scalar.  If a finite mixture `(v, Y)` of
configurations in `E` has the same averaged squared distances on all pairs and each of its
states has the edge lengths `ℓ` on `E₀`, then every state of positive weight has the distance
matrix of one of the `X k`, provided some constrained edge has non-zero length. -/
theorem mixture_identifiable_stacked [FiniteDimensional ℝ E] [Nonempty K] {J : Type*} [Fintype J]
    (d : ℕ) (hd : 0 < d) (hE : Module.finrank ℝ E = d)
    (w : K → ℝ) (hw : ∀ k, 0 < w k) (hw1 : ∑ k, w k = 1) (X : K → ι → E)
    (E₀ : Set (ι × ι)) (ℓ : ι × ι → ℝ) (hX : ∀ k, ∀ p ∈ E₀, ‖X k p.1 - X k p.2‖ = ℓ p)
    (p₀ : ι × ι) (hp₀ : p₀ ∈ E₀) (hℓ : ℓ p₀ ≠ 0)
    (i₀ : ι)
    (hspan : Submodule.span ℝ (Set.range fun i => stacked w X i - stacked w X i₀) = ⊤)
    (hCC : ∀ B : PiLp 2 (fun _ : K => E) →ₗ[ℝ] PiLp 2 (fun _ : K => E) →ₗ[ℝ] ℝ,
      (∀ u x, B u x = B x u) →
      (∀ p ∈ E₀, B (stacked w X p.1 - stacked w X p.2) (stacked w X p.1 - stacked w X p.2) = 0) →
      ∃ s : K → ℝ, ∀ k l, ∀ u ∈ LinearMap.range (blockIncl (E := E) k),
        ∀ x ∈ LinearMap.range (blockIncl (E := E) l),
        B u x = if k = l then s k * @inner ℝ _ _ u x else 0)
    (v : J → ℝ) (hv : ∀ j, 0 ≤ v j) (Y : J → ι → E)
    (hY : ∀ j, 0 < v j → ∀ p ∈ E₀, ‖Y j p.1 - Y j p.2‖ = ℓ p)
    (hdata : ∀ i i', ∑ j, v j * ‖Y j i - Y j i'‖ ^ 2 = ∑ k, w k * ‖X k i - X k i'‖ ^ 2)
    (j : J) (hj : 0 < v j) :
    ∃ k₀, SameShape (Y j) (X k₀) := by
  have hw0 : ∀ k, 0 ≤ w k := fun k => (hw k).le
  -- the edge lengths of the stacked configuration on `E₀`
  have hzE : ∀ p ∈ E₀, ‖stacked w X p.1 - stacked w X p.2‖ = |ℓ p| := by
    intro p hp
    have h := stacked_sqdist w hw0 X p.1 p.2
    have h2 : ∑ k, w k * ‖X k p.1 - X k p.2‖ ^ 2 = ℓ p ^ 2 := by
      have : ∀ k, w k * ‖X k p.1 - X k p.2‖ ^ 2 = w k * ℓ p ^ 2 := fun k => by rw [hX k p hp]
      simp only [this]
      rw [← Finset.sum_mul, hw1, one_mul]
    rw [h2] at h
    rw [← Real.sqrt_sq (norm_nonneg _), h, Real.sqrt_sq_eq_abs]
  have hℓabs : ∀ j, 0 < v j → ∀ p ∈ E₀, ‖Y j p.1 - Y j p.2‖ = |ℓ p| := by
    intro j hj p hp
    have := hY j hj p hp
    rw [← this, abs_of_nonneg (norm_nonneg _)]
  have hdim : ∀ k : K, Module.finrank ℝ (LinearMap.range (blockIncl (E := E) k)) = d := by
    intro k
    rw [LinearMap.finrank_range_of_inj (blockIncl_injective k), hE]
  have hmem : ∀ (k : K) (x : PiLp 2 (fun _ : K => E)),
      blockComp k x ∈ LinearMap.range (blockIncl (E := E) k) := fun k x => ⟨_, rfl⟩
  have hstate : ∀ j, 0 < v j → ∀ p ∈ E₀,
      ‖Y j p.1 - Y j p.2‖ = ‖stacked w X p.1 - stacked w X p.2‖ := by
    intro j hj p hp
    rw [hℓabs j hj p hp, hzE p hp]
  have hdata' : ∀ i i', ∑ j, v j * ‖Y j i - Y j i'‖ ^ 2
      = ‖stacked w X i - stacked w X i'‖ ^ 2 := by
    intro i i'
    rw [hdata, stacked_sqdist w hw0]
  obtain ⟨k₀, c, hc0, hc⟩ := finite_mixture_identifiable
    (V := PiLp 2 (fun _ : K => E)) (W := E)
    (fun k => LinearMap.range (blockIncl (E := E) k)) d hd hdim
    blocks_ortho (le_of_eq hE) blockComp hmem blockComp_sum (stacked w X) i₀ hspan E₀ hCC
    v hv Y hstate hdata' j hj
  refine ⟨k₀, ?_⟩
  -- `‖comp k₀ (z i - z i')‖² = w k₀ ‖X k₀ i - X k₀ i'‖²`
  have hcomp : ∀ i i', ‖blockComp k₀ (stacked w X i - stacked w X i')‖ ^ 2
      = w k₀ * ‖X k₀ i - X k₀ i'‖ ^ 2 := by
    intro i i'
    rw [norm_blockComp]
    have h : (stacked w X i - stacked w X i') k₀ = Real.sqrt (w k₀) • (X k₀ i - X k₀ i') := by
      simp [stacked, smul_sub]
    rw [h, norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt (hw0 k₀)]
  -- the constant: one constrained edge of non-zero length
  have hcw : c * w k₀ = 1 := by
    have h := hc p₀.1 p₀.2
    rw [hcomp, hY j hj p₀ hp₀, hX k₀ p₀ hp₀] at h
    have hpos : ℓ p₀ ^ 2 ≠ 0 := pow_ne_zero 2 hℓ
    have : (c * w k₀ - 1) * ℓ p₀ ^ 2 = 0 := by linarith
    rcases mul_eq_zero.mp this with h' | h'
    · linarith
    · exact absurd h' hpos
  intro i i'
  have h := hc i i'
  rw [hcomp] at h
  have h2 : ‖Y j i - Y j i'‖ ^ 2 = ‖X k₀ i - X k₀ i'‖ ^ 2 := by
    rw [h, ← mul_assoc, hcw, one_mul]
  have a1 : 0 ≤ ‖Y j i - Y j i'‖ := norm_nonneg _
  have a2 : 0 ≤ ‖X k₀ i - X k₀ i'‖ := norm_nonneg _
  nlinarith [sq_nonneg (‖Y j i - Y j i'‖ - ‖X k₀ i - X k₀ i'‖)]

theorem norm_blockIncl (k : K) (a : E) : ‖(blockIncl k a : PiLp 2 (fun _ : K => E))‖ = ‖a‖ := by
  have h : blockComp k (blockIncl k a) = (blockIncl k a : PiLp 2 (fun _ : K => E)) := by
    ext l
    simp [blockComp_apply, blockIncl_apply]
  rw [← h, norm_blockComp, blockIncl_apply, if_pos rfl]

end Concrete

section LineWitness

/-- Two states of a three-point chain on the line with unit bonds: straight and folded. -/
noncomputable def lineStates : Fin 2 → Fin 3 → ℝ := ![![0, 1, 2], ![0, 1, 0]]

/-- Equal weights. -/
noncomputable def lineWeights : Fin 2 → ℝ := fun _ => 1 / 2

/-- The constrained pairs: the two bonds. -/
def lineBonds : Set (Fin 3 × Fin 3) := {((0 : Fin 3), (1 : Fin 3)), ((1 : Fin 3), (2 : Fin 3))}

theorem line_edge01 :
    stacked lineWeights lineStates 0 - stacked lineWeights lineStates 1
      = (-Real.sqrt (1 / 2)) • (blockIncl (0 : Fin 2) (1 : ℝ) + blockIncl (1 : Fin 2) (1 : ℝ)) := by
  ext l
  fin_cases l <;> simp [stacked, lineStates, lineWeights, blockIncl_apply]

theorem line_edge12 :
    stacked lineWeights lineStates 1 - stacked lineWeights lineStates 2
      = Real.sqrt (1 / 2) • (blockIncl (1 : Fin 2) (1 : ℝ) - blockIncl (0 : Fin 2) (1 : ℝ)) := by
  ext l
  fin_cases l
  · simp [stacked, lineStates, lineWeights, blockIncl_apply]
    ring
  · simp [stacked, lineStates, lineWeights, blockIncl_apply]

theorem line_sqrt_half : Real.sqrt (1 / 2) * Real.sqrt (1 / 2) = 1 / 2 :=
  Real.mul_self_sqrt (by norm_num)

theorem line_sqrt_half_pos : 0 < Real.sqrt (1 / 2) := Real.sqrt_pos.mpr (by norm_num)

/-- The conic condition holds for the stacked configuration of the two line states. -/
theorem line_conic (B : PiLp 2 (fun _ : Fin 2 => ℝ) →ₗ[ℝ] PiLp 2 (fun _ : Fin 2 => ℝ) →ₗ[ℝ] ℝ)
    (hsym : ∀ u x, B u x = B x u)
    (hedge : ∀ p ∈ lineBonds,
      B (stacked lineWeights lineStates p.1 - stacked lineWeights lineStates p.2)
        (stacked lineWeights lineStates p.1 - stacked lineWeights lineStates p.2) = 0) :
    ∃ s : Fin 2 → ℝ, ∀ k l, ∀ u ∈ LinearMap.range (blockIncl (E := ℝ) k),
      ∀ x ∈ LinearMap.range (blockIncl (E := ℝ) l),
      B u x = if k = l then s k * @inner ℝ _ _ u x else 0 := by
  set e0 : PiLp 2 (fun _ : Fin 2 => ℝ) := blockIncl (0 : Fin 2) (1 : ℝ) with he0
  set e1 : PiLp 2 (fun _ : Fin 2 => ℝ) := blockIncl (1 : Fin 2) (1 : ℝ) with he1
  have h01 := hedge ((0 : Fin 3), (1 : Fin 3)) (Or.inl rfl)
  have h12 := hedge ((1 : Fin 3), (2 : Fin 3)) (Or.inr rfl)
  simp only [line_edge01, line_edge12] at h01 h12
  rw [← he0, ← he1] at h01 h12
  simp only [map_smul, map_add, map_sub, LinearMap.smul_apply, LinearMap.add_apply,
    LinearMap.sub_apply, smul_eq_mul] at h01 h12
  have hs := hsym e1 e0
  have hr := line_sqrt_half
  have hcross : B e0 e1 = 0 := by
    have h : Real.sqrt (1 / 2) * Real.sqrt (1 / 2) * (4 * B e0 e1) = 0 := by
      rw [hs] at h01 h12
      linear_combination h01 - h12
    rw [hr] at h
    linarith
  -- every vector of a block is a multiple of its unit vector
  have hrep : ∀ (k : Fin 2) (a : ℝ),
      (blockIncl k a : PiLp 2 (fun _ : Fin 2 => ℝ)) = a • blockIncl k (1 : ℝ) := by
    intro k a
    rw [← map_smul, smul_eq_mul, mul_one]
  have hunit : ∀ k : Fin 2, @inner ℝ _ _ (blockIncl k (1 : ℝ) : PiLp 2 (fun _ : Fin 2 => ℝ))
      (blockIncl k (1 : ℝ)) = 1 := by
    intro k
    rw [real_inner_self_eq_norm_sq, norm_blockIncl, norm_one, one_pow]
  refine ⟨fun k => B (blockIncl k (1 : ℝ)) (blockIncl k (1 : ℝ)), ?_⟩
  rintro k l _ ⟨a, rfl⟩ _ ⟨b, rfl⟩
  rw [hrep k a, hrep l b]
  simp only [map_smul, LinearMap.smul_apply, smul_eq_mul]
  by_cases hkl : k = l
  · subst hkl
    rw [if_pos rfl, real_inner_smul_left, real_inner_smul_right, hunit]
    ring
  · rw [if_neg hkl]
    have h0 : B (blockIncl k (1 : ℝ)) (blockIncl l (1 : ℝ)) = 0 := by
      fin_cases k <;> fin_cases l
      · exact absurd rfl hkl
      · exact hcross
      · exact hs.trans hcross
      · exact absurd rfl hkl
    rw [h0, mul_zero, mul_zero]

theorem lineStates_values :
    lineStates 0 0 = 0 ∧ lineStates 0 1 = 1 ∧ lineStates 0 2 = 2 ∧
    lineStates 1 0 = 0 ∧ lineStates 1 1 = 1 ∧ lineStates 1 2 = 0 :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem line_bonds (k : Fin 2) :
    ∀ p ∈ lineBonds, ‖lineStates k p.1 - lineStates k p.2‖ = (fun _ : Fin 3 × Fin 3 => (1 : ℝ)) p := by
  obtain ⟨h00, h01, h02, h10, h11, h12⟩ := lineStates_values
  rintro p (rfl | rfl) <;> fin_cases k
  · change ‖lineStates 0 0 - lineStates 0 1‖ = 1
    rw [h00, h01]; norm_num
  · change ‖lineStates 1 0 - lineStates 1 1‖ = 1
    rw [h10, h11]; norm_num
  · change ‖lineStates 0 1 - lineStates 0 2‖ = 1
    rw [h01, h02]; norm_num
  · change ‖lineStates 1 1 - lineStates 1 2‖ = 1
    rw [h11, h12]; norm_num

theorem line_span :
    Submodule.span ℝ (Set.range fun i =>
      stacked lineWeights lineStates i - stacked lineWeights lineStates 0) = ⊤ := by
  rw [eq_top_iff]
  intro x _
  have h2 : Real.sqrt 2 ≠ 0 := by positivity
  have hx : x = (x 1 / Real.sqrt (1 / 2)) •
        (stacked lineWeights lineStates 1 - stacked lineWeights lineStates 0)
      + ((x 0 - x 1) / (2 * Real.sqrt (1 / 2))) •
        (stacked lineWeights lineStates 2 - stacked lineWeights lineStates 0) := by
    ext l
    fin_cases l
    · simp [stacked, lineStates, lineWeights]
      field_simp
      ring
    · simp [stacked, lineStates, lineWeights]
  rw [hx]
  exact Submodule.add_mem _ (Submodule.smul_mem _ _ (Submodule.subset_span ⟨1, rfl⟩))
    (Submodule.smul_mem _ _ (Submodule.subset_span ⟨2, rfl⟩))

theorem line_states_differ : ¬ SameShape (lineStates 0) (lineStates 1) := by
  obtain ⟨h00, -, h02, h10, -, h12⟩ := lineStates_values
  intro h
  have h' := h 0 2
  rw [h00, h02, h10, h12] at h'
  norm_num at h'

/-- **Non-vacuity of `mixture_identifiable_stacked` with two different states**, used end to
end: the equal mixture of the straight and the folded three-point unit chain on the line is the
only finite mixture of unit chains on the line with its averaged squared distances, in the
sense that every state of positive weight of such a mixture is straight or folded. -/
theorem line_mixture_example {J : Type*} [Fintype J] (v : J → ℝ) (hv : ∀ j, 0 ≤ v j)
    (Y : J → Fin 3 → ℝ)
    (hY : ∀ j, 0 < v j → ∀ p ∈ lineBonds, ‖Y j p.1 - Y j p.2‖ = 1)
    (hdata : ∀ i i', ∑ j, v j * ‖Y j i - Y j i'‖ ^ 2
      = ∑ k, lineWeights k * ‖lineStates k i - lineStates k i'‖ ^ 2)
    (j : J) (hj : 0 < v j) : ∃ k₀, SameShape (Y j) (lineStates k₀) :=
  mixture_identifiable_stacked 1 one_pos (Module.finrank_self ℝ) lineWeights
    (fun _ => by norm_num [lineWeights]) (by rw [Fin.sum_univ_two]; norm_num [lineWeights])
    lineStates lineBonds (fun _ => 1) line_bonds ((0 : Fin 3), (1 : Fin 3)) (Or.inl rfl)
    one_ne_zero 0 line_span line_conic v hv Y hY hdata j hj

end LineWitness

end MetricChain.Geometry
