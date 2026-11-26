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
* **Affine flexes give mixtures** (`sqdist_midpoint_of_conic`, Theorem A (iii)⇒(ii)): if a symmetric
  matrix `S` vanishes on a set of edge vectors and `1 ± S` are positive semidefinite, there are
  linear maps `A₊, A₋` preserving the lengths of the edge vectors with
  `‖A₊ v‖² + ‖A₋ v‖² = 2 ‖v‖²` for every `v`, and `‖A₊ v‖² - ‖v‖² = v ⬝ᵥ S *ᵥ v`.
* **The hierarchy** (Theorem E, for finite mixtures): `secondMomentRigid_of_universal` (universal
  rigidity of the measured-plus-constrained framework reduces averaged data on a set of pairs to
  averaged data on all pairs) and `globallyRigid_of_secondMomentRigid`.  The notion is called
  *second-moment rigidity* (rigidity under ensemble-averaged squared distances); "ensemble
  rigidity" is the Ensemble Identifiability Division's name for determination by the *laws* of
  the edge lengths, a different and weaker requirement on the framework (its Theorem E7).
* **Non-vacuity** (`fourAtom_virtual_value_witness`): the midpoint of two distinct values of a
  squared distance is attained by a two-state mixture — the four-atom obstruction in its simplest
  algebraic form — and `block_rigidity_nonvacuous`.
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

/-! ### 5. The hierarchy: universal ⇒ ensemble ⇒ global rigidity (finite mixtures) -/

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

end MetricChain.Geometry
