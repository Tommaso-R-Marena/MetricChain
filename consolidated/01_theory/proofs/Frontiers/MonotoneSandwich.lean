import Mathlib

/-!
# The stochastic sandwich for robust macrostate ratios (addendum A11)

*Provenance.*  This file was written by the Scientific Discovery Division (branch
`research/scientific-translation`, `experiments/science/ws_L2/Sandwich.lean`, as published with its
message SCI-MSG-0014 at its commit `9a0865f`) and is adopted here unchanged except for this
paragraph and the removal of its closing block of `#print axioms` commands (the axiom audit of
`proofs/AxiomAudit.lean` walks every declaration of this file and prints the headline ones).  It
was compiled by the theory division before adoption.  The paper statement is theory report
§11.28, Theorem 11.106a; the namespace `ScienceL2` is the division's and is kept.

Science division, workstream L2.  Source: `docs/science/INFERENCE_LIMITS_ADDENDA.md`, section A11
(Theorem A11, Corollary A11.1).

Setting of the note: `X = {0,1}ⁿ` with the coordinatewise order; envelope
`d(x,y) = ∑_{x_i=1,y_i=0} c↑_i + ∑_{x_i=0,y_i=1} c↓_i`; residual `g` admissible iff
`g x - g y ≤ d x y`; known part `f` submodular; `μ_e ∝ exp(-β e)`; fields
`h↑ x = ∑_i c↑_i x_i`, `h↓ x = ∑_i c↓_i x_i`.  Claim: `μ_{f+h↑} ≼ μ_{f+g} ≼ μ_{f-h↓}` in the
stochastic order, and for an up-set `B` with complement `A` the ratio `Z_{f+g}(A)/Z_{f+g}(B)`
fills exactly `[Z_{f-h↓}(A)/Z_{f-h↓}(B), Z_{f+h↑}(A)/Z_{f+h↑}(B)]`.

## What is proved

Abstract part (any finite distributive lattice `α`; tool: Mathlib's four functions theorem):

* `holley_cross_nonneg`, `holley_cross` — Holley's inequality in cross-multiplied form for
  *unnormalised* non-negative weights: if `w₁ x * w₂ y ≤ w₁ (x ⊓ y) * w₂ (x ⊔ y)` then
  `(∑ φ w₁) (∑ w₂) ≤ (∑ w₁) (∑ φ w₂)` for every monotone `φ` (of any sign);
* `updown_cross` — for a lower set `A` and an upper set `B` (not necessarily complementary):
  `w₁(B) * w₂(A) ≤ w₁(A) * w₂(B)`;
* `holley_condition_lower_of_saturation`, `holley_condition_upper_of_saturation` — the two
  Holley conditions of the note from: `f` submodular, `g` admissible for an *arbitrary*
  `d : α → α → ℝ`, `0 ≤ β`, and the "saturation" inequalities
  `d (x ⊔ y) y ≤ h↑ x - h↑ (x ⊓ y)`, `d (x ⊓ y) x ≤ h↓ (x ⊔ y) - h↓ y`;
* `sandwich_cross_lower`, `sandwich_cross_upper`, `sandwich_mean` — Theorem A11 on such a lattice;
* `macrostate_cross_lower`, `macrostate_cross_upper`, `macrostate_ratio` — Corollary A11.1,
  inequalities, for a lower set `A` and an upper set `B`;
* `mean_range_eq_Icc`, `ratio_range_eq_Icc` — if moreover `h↑` and `-h↓` are admissible and
  `0 < β`, the set of values over the class *is* the closed interval ("fills exactly").

No lattice (`Mixture` section; any type, any envelope):

* `mixRes_admissible` — the class is convex in the weights `e^{-β g}`;
* `exists_admissible_ratio` — a ratio of two linear functionals of the weights takes every value
  between its values at two admissible residuals.

The cube `ι → Bool` (`ι` any finite type, e.g. `Fin n`):

* `envDist`, `field`, `envDist_sup_right`, `envDist_inf_left` (the saturation *identities*);
* `field_admissible`, `neg_field_admissible` — the two fields are admissible as soon as
  `0 ≤ c↑_i + c↓_i` for all `i`; `add_nonneg_of_admissible` — and this is necessary for the class
  to be non-empty;
* `cube_holley_lower`, `cube_holley_upper` — the Holley conditions, written out with `Real.exp`;
* `cube_sandwich_cross_lower`, `cube_sandwich_cross_upper`, `cube_sandwich_mean` — Theorem A11;
* `cube_macrostate_cross_lower`, `cube_macrostate_cross_upper`, `cube_macrostate_ratio`,
  `cube_macrostate_ratio_compl` — Corollary A11.1 (inequalities);
* `cube_mean_isLeast`, `cube_mean_isGreatest` — both ends are attained in the class;
* `cube_mean_range_eq_Icc`, `cube_ratio_range_eq_Icc` — for `0 < β` the set of values over the
  class *is* the closed interval ("fills exactly");
* `field_submodular`, `pairTerm_submodular`, `pairwise_submodular` — additive known parts and
  pairwise known parts with all couplings `J_ij ≤ 0` are submodular;
* `cube_sandwich_strict_witness` — a two-site instance with a non-additive submodular known
  part in which all hypotheses hold and both inequalities are strict;
  `cube_sandwich_fails_negative_beta` — in the same instance at `β = -1` the lower inequality
  fails (so `0 ≤ β` is needed).

A product of finite chains `∀ i, Fin (k i)` (Remark (1) of A11):

* `chainDist`, `chainField`, `chainDist_sup_right`, `chainDist_inf_left`,
  `chainField_admissible`, `neg_chainField_admissible`;
* `chain_sandwich_mean`, `chain_mean_range_eq_Icc`, `chain_ratio_range_eq_Icc`.

Addendum A13 (arbitrary site quasi-metrics, step fields):

* `siteDist_sup_right_le`, `siteDist_inf_left_le` (the triangle inequality telescoped along the
  order), `stepField_sandwich_mean`, `stepField_macrostate_ratio`.

Corollary A11.2, the sign only:

* `updown_inter_cross`, `cube_occupation_cross`, `cube_occupation_mono` — for a lower set `A`
  and an upper set `B`, `⟨x_i⟩_{A,t} ≤ ⟨x_i⟩_{B,t}` in `μ_{f+th}` (every summand of the width
  formula is non-negative when `c_i ≥ 0`).

Not proved here: the width formula of Corollary A11.2 itself (an integral), Corollary A11.3,
the necessity of the hypotheses (numerical in the note), Remark (2).
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL2

open Finset
open scoped FinsetFamily

/-! ### Abstract part: a finite distributive lattice -/

section Lattice

variable {α : Type*}

/-- Unnormalised Boltzmann weight `exp (-(β * e x))` of the energy `e`. -/
def boltz (β : ℝ) (e : α → ℝ) (x : α) : ℝ := Real.exp (-(β * e x))

theorem boltz_pos (β : ℝ) (e : α → ℝ) (x : α) : 0 < boltz β e x := Real.exp_pos _

/-- `g` is admissible for the envelope `d`: `g x - g y ≤ d x y`. -/
def Admissible (d : α → α → ℝ) (g : α → ℝ) : Prop := ∀ x y, g x - g y ≤ d x y

/-- `f (x ⊔ y) + f (x ⊓ y) ≤ f x + f y`. -/
def Submodular [Lattice α] (f : α → ℝ) : Prop := ∀ x y, f (x ⊔ y) + f (x ⊓ y) ≤ f x + f y

/-- The mean of `φ` in the Gibbs measure `∝ exp (-β e)`. -/
def gibbsMean [Fintype α] (β : ℝ) (e φ : α → ℝ) : ℝ :=
  (∑ x, φ x * boltz β e x) / ∑ x, boltz β e x

/-- The partition sum of `e` restricted to the set `S`. -/
def zOn (β : ℝ) (e : α → ℝ) (S : Finset α) : ℝ := ∑ x ∈ S, boltz β e x

theorem zOn_nonneg (β : ℝ) (e : α → ℝ) (S : Finset α) : 0 ≤ zOn β e S :=
  Finset.sum_nonneg (fun x _ => (boltz_pos β e x).le)

theorem zOn_pos (β : ℝ) (e : α → ℝ) {S : Finset α} (hS : S.Nonempty) : 0 < zOn β e S :=
  Finset.sum_pos (fun x _ => boltz_pos β e x) hS

theorem sum_boltz_pos [Fintype α] [Nonempty α] (β : ℝ) (e : α → ℝ) : 0 < ∑ x, boltz β e x :=
  Finset.sum_pos (fun x _ => boltz_pos β e x) Finset.univ_nonempty

variable [DistribLattice α] [Fintype α]

/-- **Holley's inequality, cross-multiplied, unnormalised weights, `φ ≥ 0`.**  A direct
instance of the four functions theorem. -/
theorem holley_cross_nonneg (w₁ w₂ φ : α → ℝ) (hw₁ : ∀ x, 0 ≤ w₁ x) (hw₂ : ∀ x, 0 ≤ w₂ x)
    (hφ₀ : ∀ x, 0 ≤ φ x) (hφ : Monotone φ)
    (h : ∀ x y, w₁ x * w₂ y ≤ w₁ (x ⊓ y) * w₂ (x ⊔ y)) :
    (∑ x, φ x * w₁ x) * (∑ x, w₂ x) ≤ (∑ x, w₁ x) * (∑ x, φ x * w₂ x) := by
  refine four_functions_theorem_univ (fun x => φ x * w₁ x) w₂ w₁ (fun x => φ x * w₂ x)
    (fun x => mul_nonneg (hφ₀ x) (hw₁ x)) hw₂ hw₁ (fun x => mul_nonneg (hφ₀ x) (hw₂ x)) ?_
  intro a b
  have h1 : φ a ≤ φ (a ⊔ b) := hφ le_sup_left
  calc φ a * w₁ a * w₂ b = φ a * (w₁ a * w₂ b) := by ring
    _ ≤ φ (a ⊔ b) * (w₁ (a ⊓ b) * w₂ (a ⊔ b)) :=
        mul_le_mul h1 (h a b) (mul_nonneg (hw₁ a) (hw₂ b)) (hφ₀ _)
    _ = w₁ (a ⊓ b) * (φ (a ⊔ b) * w₂ (a ⊔ b)) := by ring

/-- **Holley's inequality, cross-multiplied, unnormalised weights, any monotone `φ`.**
The inequality is invariant under adding a constant to `φ`, so `φ ≥ 0` is not needed. -/
theorem holley_cross (w₁ w₂ φ : α → ℝ) (hw₁ : ∀ x, 0 ≤ w₁ x) (hw₂ : ∀ x, 0 ≤ w₂ x)
    (hφ : Monotone φ) (h : ∀ x y, w₁ x * w₂ y ≤ w₁ (x ⊓ y) * w₂ (x ⊔ y)) :
    (∑ x, φ x * w₁ x) * (∑ x, w₂ x) ≤ (∑ x, w₁ x) * (∑ x, φ x * w₂ x) := by
  set c : ℝ := ∑ x, |φ x| with hc
  have hc0 : ∀ x, 0 ≤ φ x + c := by
    intro x
    have h1 : |φ x| ≤ c :=
      Finset.single_le_sum (f := fun y => |φ y|) (fun y _ => abs_nonneg (φ y)) (Finset.mem_univ x)
    have h2 := neg_abs_le (φ x)
    linarith
  have hmono : Monotone (fun x => φ x + c) := fun x y hxy => by
    have := hφ hxy
    simp only
    linarith
  have key := holley_cross_nonneg w₁ w₂ (fun x => φ x + c) hw₁ hw₂ hc0 hmono h
  have e1 : ∑ x, (φ x + c) * w₁ x = ∑ x, φ x * w₁ x + c * ∑ x, w₁ x := by
    simp only [add_mul, Finset.sum_add_distrib, Finset.mul_sum]
  have e2 : ∑ x, (φ x + c) * w₂ x = ∑ x, φ x * w₂ x + c * ∑ x, w₂ x := by
    simp only [add_mul, Finset.sum_add_distrib, Finset.mul_sum]
  rw [e1, e2] at key
  linarith

omit [Fintype α] in
/-- For a lower set `A` and an upper set `B`: `w₁(B) * w₂(A) ≤ w₁(A) * w₂(B)`.  (The sets need
not be complementary.) -/
theorem updown_cross [DecidableEq α] (w₁ w₂ : α → ℝ) (hw₁ : ∀ x, 0 ≤ w₁ x)
    (hw₂ : ∀ x, 0 ≤ w₂ x) (h : ∀ x y, w₁ x * w₂ y ≤ w₁ (x ⊓ y) * w₂ (x ⊔ y))
    (A B : Finset α) (hA : IsLowerSet (A : Set α)) (hB : IsUpperSet (B : Set α)) :
    (∑ x ∈ B, w₁ x) * (∑ x ∈ A, w₂ x) ≤ (∑ x ∈ A, w₁ x) * (∑ x ∈ B, w₂ x) := by
  have key := four_functions_theorem w₁ w₂ w₁ w₂ hw₁ hw₂ hw₁ hw₂ h B A
  have hsub1 : B ⊼ A ⊆ A := by
    intro z hz
    obtain ⟨a, _, b, hb, rfl⟩ := Finset.mem_infs.1 hz
    exact Finset.mem_coe.1 (hA inf_le_right (Finset.mem_coe.2 hb))
  have hsub2 : B ⊻ A ⊆ B := by
    intro z hz
    obtain ⟨a, ha, b, _, rfl⟩ := Finset.mem_sups.1 hz
    exact Finset.mem_coe.1 (hB le_sup_left (Finset.mem_coe.2 ha))
  calc (∑ x ∈ B, w₁ x) * (∑ x ∈ A, w₂ x)
      ≤ (∑ a ∈ B ⊼ A, w₁ a) * ∑ a ∈ B ⊻ A, w₂ a := key
    _ ≤ (∑ x ∈ A, w₁ x) * (∑ x ∈ B, w₂ x) := by
        apply mul_le_mul
        · exact Finset.sum_le_sum_of_subset_of_nonneg hsub1 (fun x _ _ => hw₁ x)
        · exact Finset.sum_le_sum_of_subset_of_nonneg hsub2 (fun x _ _ => hw₂ x)
        · exact Finset.sum_nonneg (fun x _ => hw₂ x)
        · exact Finset.sum_nonneg (fun x _ => hw₁ x)

omit [Fintype α] in
/-- **Holley condition, lower end** (`μ₁ = μ_{f+h↑}`, `μ₂ = μ_{f+g}`), on any lattice, from
submodularity of `f`, admissibility of `g` for `d`, `0 ≤ β` and
`d (x ⊔ y) y ≤ h↑ x - h↑ (x ⊓ y)`. -/
theorem holley_condition_lower_of_saturation {β : ℝ} (hβ : 0 ≤ β) {f g hup : α → ℝ}
    {d : α → α → ℝ} (hf : Submodular f) (hg : Admissible d g)
    (hsat : ∀ x y, d (x ⊔ y) y ≤ hup x - hup (x ⊓ y)) (x y : α) :
    boltz β (fun z => f z + hup z) x * boltz β (fun z => f z + g z) y ≤
      boltz β (fun z => f z + hup z) (x ⊓ y) * boltz β (fun z => f z + g z) (x ⊔ y) := by
  unfold boltz
  rw [← Real.exp_add, ← Real.exp_add, Real.exp_le_exp]
  have h1 := hf x y
  have h2 := hg (x ⊔ y) y
  have h3 := hsat x y
  have h4 : f (x ⊓ y) + hup (x ⊓ y) + (f (x ⊔ y) + g (x ⊔ y)) ≤ f x + hup x + (f y + g y) := by
    linarith
  have h5 := mul_le_mul_of_nonneg_left h4 hβ
  simp only
  linarith

omit [Fintype α] in
/-- **Holley condition, upper end** (`μ₁ = μ_{f+g}`, `μ₂ = μ_{f-h↓}`), on any lattice, from
submodularity of `f`, admissibility of `g` for `d`, `0 ≤ β` and
`d (x ⊓ y) x ≤ h↓ (x ⊔ y) - h↓ y`. -/
theorem holley_condition_upper_of_saturation {β : ℝ} (hβ : 0 ≤ β) {f g hdn : α → ℝ}
    {d : α → α → ℝ} (hf : Submodular f) (hg : Admissible d g)
    (hsat : ∀ x y, d (x ⊓ y) x ≤ hdn (x ⊔ y) - hdn y) (x y : α) :
    boltz β (fun z => f z + g z) x * boltz β (fun z => f z - hdn z) y ≤
      boltz β (fun z => f z + g z) (x ⊓ y) * boltz β (fun z => f z - hdn z) (x ⊔ y) := by
  unfold boltz
  rw [← Real.exp_add, ← Real.exp_add, Real.exp_le_exp]
  have h1 := hf x y
  have h2 := hg (x ⊓ y) x
  have h3 := hsat x y
  have h4 : f (x ⊓ y) + g (x ⊓ y) + (f (x ⊔ y) - hdn (x ⊔ y)) ≤ f x + g x + (f y - hdn y) := by
    linarith
  have h5 := mul_le_mul_of_nonneg_left h4 hβ
  simp only
  linarith

/-- **Theorem A11, lower end, cross-multiplied.**  For every monotone `φ`:
`(∑ φ w_{f+h↑}) (∑ w_{f+g}) ≤ (∑ w_{f+h↑}) (∑ φ w_{f+g})`. -/
theorem sandwich_cross_lower {β : ℝ} (hβ : 0 ≤ β) {f g hup : α → ℝ} {d : α → α → ℝ}
    (hf : Submodular f) (hg : Admissible d g)
    (hsat : ∀ x y, d (x ⊔ y) y ≤ hup x - hup (x ⊓ y)) {φ : α → ℝ} (hφ : Monotone φ) :
    (∑ x, φ x * boltz β (fun z => f z + hup z) x) * (∑ x, boltz β (fun z => f z + g z) x) ≤
      (∑ x, boltz β (fun z => f z + hup z) x) * (∑ x, φ x * boltz β (fun z => f z + g z) x) :=
  holley_cross _ _ φ (fun x => (boltz_pos _ _ x).le) (fun x => (boltz_pos _ _ x).le) hφ
    (holley_condition_lower_of_saturation hβ hf hg hsat)

/-- **Theorem A11, upper end, cross-multiplied.**  For every monotone `φ`:
`(∑ φ w_{f+g}) (∑ w_{f-h↓}) ≤ (∑ w_{f+g}) (∑ φ w_{f-h↓})`. -/
theorem sandwich_cross_upper {β : ℝ} (hβ : 0 ≤ β) {f g hdn : α → ℝ} {d : α → α → ℝ}
    (hf : Submodular f) (hg : Admissible d g)
    (hsat : ∀ x y, d (x ⊓ y) x ≤ hdn (x ⊔ y) - hdn y) {φ : α → ℝ} (hφ : Monotone φ) :
    (∑ x, φ x * boltz β (fun z => f z + g z) x) * (∑ x, boltz β (fun z => f z - hdn z) x) ≤
      (∑ x, boltz β (fun z => f z + g z) x) * (∑ x, φ x * boltz β (fun z => f z - hdn z) x) :=
  holley_cross _ _ φ (fun x => (boltz_pos _ _ x).le) (fun x => (boltz_pos _ _ x).le) hφ
    (holley_condition_upper_of_saturation hβ hf hg hsat)

/-- **Theorem A11 (sandwich in stochastic order), as inequalities between Gibbs means.**
`E_{f+h↑} φ ≤ E_{f+g} φ ≤ E_{f-h↓} φ` for every monotone `φ`. -/
theorem sandwich_mean [Nonempty α] {β : ℝ} (hβ : 0 ≤ β) {f g hup hdn : α → ℝ} {d : α → α → ℝ}
    (hf : Submodular f) (hg : Admissible d g)
    (hsatU : ∀ x y, d (x ⊔ y) y ≤ hup x - hup (x ⊓ y))
    (hsatD : ∀ x y, d (x ⊓ y) x ≤ hdn (x ⊔ y) - hdn y) {φ : α → ℝ} (hφ : Monotone φ) :
    gibbsMean β (fun z => f z + hup z) φ ≤ gibbsMean β (fun z => f z + g z) φ ∧
      gibbsMean β (fun z => f z + g z) φ ≤ gibbsMean β (fun z => f z - hdn z) φ := by
  unfold gibbsMean
  constructor
  · rw [div_le_div_iff₀ (sum_boltz_pos _ _) (sum_boltz_pos _ _)]
    have := sandwich_cross_lower hβ hf hg hsatU hφ
    linarith
  · rw [div_le_div_iff₀ (sum_boltz_pos _ _) (sum_boltz_pos _ _)]
    have := sandwich_cross_upper hβ hf hg hsatD hφ
    linarith

omit [Fintype α] in
/-- **Corollary A11.1, upper end, cross-multiplied**: for a lower set `A` and an upper set `B`,
`Z_{f+g}(A) * Z_{f+h↑}(B) ≤ Z_{f+h↑}(A) * Z_{f+g}(B)`. -/
theorem macrostate_cross_upper [DecidableEq α] {β : ℝ} (hβ : 0 ≤ β) {f g hup : α → ℝ}
    {d : α → α → ℝ} (hf : Submodular f) (hg : Admissible d g)
    (hsat : ∀ x y, d (x ⊔ y) y ≤ hup x - hup (x ⊓ y))
    (A B : Finset α) (hA : IsLowerSet (A : Set α)) (hB : IsUpperSet (B : Set α)) :
    zOn β (fun z => f z + g z) A * zOn β (fun z => f z + hup z) B ≤
      zOn β (fun z => f z + hup z) A * zOn β (fun z => f z + g z) B := by
  have := updown_cross _ _ (fun x => (boltz_pos β (fun z => f z + hup z) x).le)
    (fun x => (boltz_pos β (fun z => f z + g z) x).le)
    (holley_condition_lower_of_saturation hβ hf hg hsat) A B hA hB
  unfold zOn
  linarith

omit [Fintype α] in
/-- **Corollary A11.1, lower end, cross-multiplied**: for a lower set `A` and an upper set `B`,
`Z_{f-h↓}(A) * Z_{f+g}(B) ≤ Z_{f+g}(A) * Z_{f-h↓}(B)`. -/
theorem macrostate_cross_lower [DecidableEq α] {β : ℝ} (hβ : 0 ≤ β) {f g hdn : α → ℝ}
    {d : α → α → ℝ} (hf : Submodular f) (hg : Admissible d g)
    (hsat : ∀ x y, d (x ⊓ y) x ≤ hdn (x ⊔ y) - hdn y)
    (A B : Finset α) (hA : IsLowerSet (A : Set α)) (hB : IsUpperSet (B : Set α)) :
    zOn β (fun z => f z - hdn z) A * zOn β (fun z => f z + g z) B ≤
      zOn β (fun z => f z + g z) A * zOn β (fun z => f z - hdn z) B := by
  have := updown_cross _ _ (fun x => (boltz_pos β (fun z => f z + g z) x).le)
    (fun x => (boltz_pos β (fun z => f z - hdn z) x).le)
    (holley_condition_upper_of_saturation hβ hf hg hsat) A B hA hB
  unfold zOn
  linarith

omit [Fintype α] in
/-- **Corollary A11.1 (inequalities), as ratios**: for a lower set `A` and a non-empty upper
set `B`, `Z_{f-h↓}(A)/Z_{f-h↓}(B) ≤ Z_{f+g}(A)/Z_{f+g}(B) ≤ Z_{f+h↑}(A)/Z_{f+h↑}(B)`. -/
theorem macrostate_ratio [DecidableEq α] {β : ℝ} (hβ : 0 ≤ β) {f g hup hdn : α → ℝ}
    {d : α → α → ℝ} (hf : Submodular f) (hg : Admissible d g)
    (hsatU : ∀ x y, d (x ⊔ y) y ≤ hup x - hup (x ⊓ y))
    (hsatD : ∀ x y, d (x ⊓ y) x ≤ hdn (x ⊔ y) - hdn y)
    (A B : Finset α) (hA : IsLowerSet (A : Set α)) (hB : IsUpperSet (B : Set α))
    (hBne : B.Nonempty) :
    zOn β (fun z => f z - hdn z) A / zOn β (fun z => f z - hdn z) B ≤
        zOn β (fun z => f z + g z) A / zOn β (fun z => f z + g z) B ∧
      zOn β (fun z => f z + g z) A / zOn β (fun z => f z + g z) B ≤
        zOn β (fun z => f z + hup z) A / zOn β (fun z => f z + hup z) B := by
  constructor
  · rw [div_le_div_iff₀ (zOn_pos _ _ hBne) (zOn_pos _ _ hBne)]
    exact macrostate_cross_lower hβ hf hg hsatD A B hA hB
  · rw [div_le_div_iff₀ (zOn_pos _ _ hBne) (zOn_pos _ _ hBne)]
    exact macrostate_cross_upper hβ hf hg hsatU A B hA hB

end Lattice

/-! ### The class is convex in the weights: every value in between is attained

No lattice structure is used in this section: `α` is any type, `d` any envelope. -/

section Mixture

variable {α : Type*}

/-- Real-arithmetic core: a linear-fractional function on a segment takes every value between
its values at the end points. -/
theorem exists_convex_ratio {n₀ n₁ d₀ d₁ r : ℝ} (hd₀ : 0 < d₀) (hd₁ : 0 < d₁)
    (h₀ : n₀ / d₀ ≤ r) (h₁ : r ≤ n₁ / d₁) :
    ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧ ((1 - t) * n₀ + t * n₁) / ((1 - t) * d₀ + t * d₁) = r := by
  rw [div_le_iff₀ hd₀] at h₀
  rw [le_div_iff₀ hd₁] at h₁
  by_cases hz : (r * d₀ - n₀) + (n₁ - r * d₁) = 0
  · refine ⟨0, le_refl 0, zero_le_one, ?_⟩
    simp only [sub_zero, one_mul, zero_mul, add_zero]
    rw [div_eq_iff hd₀.ne']
    linarith
  · have hpos : 0 < (r * d₀ - n₀) + (n₁ - r * d₁) :=
      lt_of_le_of_ne (by linarith) (Ne.symm hz)
    set t : ℝ := (r * d₀ - n₀) / ((r * d₀ - n₀) + (n₁ - r * d₁)) with ht
    have ht0 : 0 ≤ t := div_nonneg (by linarith) hpos.le
    have ht1 : t ≤ 1 := by
      rw [ht, div_le_one hpos]
      linarith
    have hden : 0 < (1 - t) * d₀ + t * d₁ := by
      rcases eq_or_lt_of_le ht0 with h | h
      · rw [← h]
        simpa using hd₀
      · have h1 := mul_pos h hd₁
        have h2 := mul_nonneg (sub_nonneg.2 ht1) hd₀.le
        linarith
    refine ⟨t, ht0, ht1, ?_⟩
    rw [div_eq_iff hden.ne']
    have key : t * ((r * d₀ - n₀) + (n₁ - r * d₁)) = r * d₀ - n₀ := by
      rw [ht]
      field_simp
    linear_combination key

/-- The residual whose weight `exp (-β g)` is the convex combination
`(1 - t) exp (-β g₀) + t exp (-β g₁)` of the weights of `g₀` and `g₁`. -/
def mixRes (β : ℝ) (g₀ g₁ : α → ℝ) (t : ℝ) (x : α) : ℝ :=
  -(Real.log ((1 - t) * Real.exp (-(β * g₀ x)) + t * Real.exp (-(β * g₁ x)))) / β

theorem mix_pos (β : ℝ) (g₀ g₁ : α → ℝ) {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) (x : α) :
    0 < (1 - t) * Real.exp (-(β * g₀ x)) + t * Real.exp (-(β * g₁ x)) := by
  rcases eq_or_lt_of_le ht0 with h | h
  · rw [← h]
    simpa using Real.exp_pos (-(β * g₀ x))
  · have h1 := mul_pos h (Real.exp_pos (-(β * g₁ x)))
    have h2 := mul_nonneg (sub_nonneg.2 ht1) (Real.exp_pos (-(β * g₀ x))).le
    linarith

/-- The Boltzmann weight of `f + mixRes` is the convex combination of the two weights. -/
theorem boltz_mixRes {β : ℝ} (hβ : β ≠ 0) (f g₀ g₁ : α → ℝ) {t : ℝ} (ht0 : 0 ≤ t)
    (ht1 : t ≤ 1) (x : α) :
    boltz β (fun z => f z + mixRes β g₀ g₁ t z) x =
      (1 - t) * boltz β (fun z => f z + g₀ z) x + t * boltz β (fun z => f z + g₁ z) x := by
  have hV := mix_pos β g₀ g₁ ht0 ht1 x
  unfold boltz mixRes
  simp only
  have e : -(β * (f x +
        -Real.log ((1 - t) * Real.exp (-(β * g₀ x)) + t * Real.exp (-(β * g₁ x))) / β)) =
      -(β * f x) +
        Real.log ((1 - t) * Real.exp (-(β * g₀ x)) + t * Real.exp (-(β * g₁ x))) := by
    field_simp
    ring
  rw [e, Real.exp_add, Real.exp_log hV]
  have e0 : Real.exp (-(β * (f x + g₀ x))) =
      Real.exp (-(β * f x)) * Real.exp (-(β * g₀ x)) := by
    rw [← Real.exp_add]
    ring_nf
  have e1 : Real.exp (-(β * (f x + g₁ x))) =
      Real.exp (-(β * f x)) * Real.exp (-(β * g₁ x)) := by
    rw [← Real.exp_add]
    ring_nf
  rw [e0, e1]
  ring

/-- **The class is convex in the weights**: for `0 < β` the mixture residual of two admissible
residuals is admissible (for any envelope `d`). -/
theorem mixRes_admissible {β : ℝ} (hβ : 0 < β) {d : α → α → ℝ} {g₀ g₁ : α → ℝ}
    (h₀ : Admissible d g₀) (h₁ : Admissible d g₁) {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    Admissible d (mixRes β g₀ g₁ t) := by
  intro x y
  have hVx := mix_pos β g₀ g₁ ht0 ht1 x
  have hVy := mix_pos β g₀ g₁ ht0 ht1 y
  have k₀ : Real.exp (-(β * g₀ y)) ≤ Real.exp (β * d x y) * Real.exp (-(β * g₀ x)) := by
    rw [← Real.exp_add, Real.exp_le_exp]
    have := mul_le_mul_of_nonneg_left (h₀ x y) hβ.le
    linarith
  have k₁ : Real.exp (-(β * g₁ y)) ≤ Real.exp (β * d x y) * Real.exp (-(β * g₁ x)) := by
    rw [← Real.exp_add, Real.exp_le_exp]
    have := mul_le_mul_of_nonneg_left (h₁ x y) hβ.le
    linarith
  have hV : (1 - t) * Real.exp (-(β * g₀ y)) + t * Real.exp (-(β * g₁ y)) ≤
      Real.exp (β * d x y) *
        ((1 - t) * Real.exp (-(β * g₀ x)) + t * Real.exp (-(β * g₁ x))) := by
    have a := mul_le_mul_of_nonneg_left k₀ (sub_nonneg.2 ht1)
    have b := mul_le_mul_of_nonneg_left k₁ ht0
    linarith
  have hlog : Real.log ((1 - t) * Real.exp (-(β * g₀ y)) + t * Real.exp (-(β * g₁ y))) ≤
      β * d x y +
        Real.log ((1 - t) * Real.exp (-(β * g₀ x)) + t * Real.exp (-(β * g₁ x))) := by
    have := Real.log_le_log hVy hV
    rwa [Real.log_mul (Real.exp_pos _).ne' hVx.ne', Real.log_exp] at this
  unfold mixRes
  rw [div_sub_div_same, div_le_iff₀ hβ]
  linarith

/-- **Every value in between is attained.**  Let `g₀, g₁` be admissible, `0 < β`, and let
`N(g) = ∑_{x ∈ S} a x e^{-β(f+g)(x)}`, `D(g) = ∑_{x ∈ T} b x e^{-β(f+g)(x)}` with
`D(g₀), D(g₁) > 0`.  Then every `r` with `N(g₀)/D(g₀) ≤ r ≤ N(g₁)/D(g₁)` equals `N(g)/D(g)` for
some admissible `g`. -/
theorem exists_admissible_ratio {β : ℝ} (hβ : 0 < β) {d : α → α → ℝ} {f g₀ g₁ : α → ℝ}
    (h₀ : Admissible d g₀) (h₁ : Admissible d g₁) (S T : Finset α) (a b : α → ℝ)
    (hD₀ : 0 < ∑ x ∈ T, b x * boltz β (fun z => f z + g₀ z) x)
    (hD₁ : 0 < ∑ x ∈ T, b x * boltz β (fun z => f z + g₁ z) x) {r : ℝ}
    (hr₀ : (∑ x ∈ S, a x * boltz β (fun z => f z + g₀ z) x) /
        (∑ x ∈ T, b x * boltz β (fun z => f z + g₀ z) x) ≤ r)
    (hr₁ : r ≤ (∑ x ∈ S, a x * boltz β (fun z => f z + g₁ z) x) /
        (∑ x ∈ T, b x * boltz β (fun z => f z + g₁ z) x)) :
    ∃ g, Admissible d g ∧ (∑ x ∈ S, a x * boltz β (fun z => f z + g z) x) /
        (∑ x ∈ T, b x * boltz β (fun z => f z + g z) x) = r := by
  obtain ⟨t, ht0, ht1, ht⟩ := exists_convex_ratio hD₀ hD₁ hr₀ hr₁
  refine ⟨mixRes β g₀ g₁ t, mixRes_admissible hβ h₀ h₁ ht0 ht1, ?_⟩
  have eS : ∑ x ∈ S, a x * boltz β (fun z => f z + mixRes β g₀ g₁ t z) x =
      (1 - t) * ∑ x ∈ S, a x * boltz β (fun z => f z + g₀ z) x +
        t * ∑ x ∈ S, a x * boltz β (fun z => f z + g₁ z) x := by
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl (fun x _ => ?_)
    rw [boltz_mixRes hβ.ne' f g₀ g₁ ht0 ht1 x]
    ring
  have eT : ∑ x ∈ T, b x * boltz β (fun z => f z + mixRes β g₀ g₁ t z) x =
      (1 - t) * ∑ x ∈ T, b x * boltz β (fun z => f z + g₀ z) x +
        t * ∑ x ∈ T, b x * boltz β (fun z => f z + g₁ z) x := by
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl (fun x _ => ?_)
    rw [boltz_mixRes hβ.ne' f g₀ g₁ ht0 ht1 x]
    ring
  rw [eS, eT]
  exact ht

end Mixture

/-! ### The exact range on a lattice with a saturated envelope -/

section LatticeRange

variable {α : Type*} [DistribLattice α] [Fintype α]

/-- **Theorem A11, "every value in between is attained", abstract form**: on a finite
distributive lattice with an envelope `d` saturated by `h↑` and `h↓`, both admissible, and
`0 < β`: the set of values of `E_{f+g} φ` over the admissible class is exactly the closed interval
between the values at the two extremal residuals. -/
theorem mean_range_eq_Icc [Nonempty α] {β : ℝ} (hβ : 0 < β) {f hup hdn : α → ℝ}
    {d : α → α → ℝ} (hf : Submodular f)
    (hsatU : ∀ x y, d (x ⊔ y) y ≤ hup x - hup (x ⊓ y))
    (hsatD : ∀ x y, d (x ⊓ y) x ≤ hdn (x ⊔ y) - hdn y)
    (hUadm : Admissible d hup) (hDadm : Admissible d (fun x => -hdn x))
    {φ : α → ℝ} (hφ : Monotone φ) :
    {r | ∃ g, Admissible d g ∧ gibbsMean β (fun z => f z + g z) φ = r} =
      Set.Icc (gibbsMean β (fun z => f z + hup z) φ) (gibbsMean β (fun z => f z - hdn z) φ) := by
  ext r
  constructor
  · rintro ⟨g, hg, rfl⟩
    exact sandwich_mean hβ.le hf hg hsatU hsatD hφ
  · rintro ⟨h1, h2⟩
    have hsub : (fun z => f z - hdn z) = (fun z => f z + (fun y => -hdn y) z) := by
      funext z
      ring
    rw [hsub] at h2
    unfold gibbsMean at h1 h2
    obtain ⟨g, hg, hgr⟩ := exists_admissible_ratio hβ hUadm hDadm (f := f) Finset.univ
      Finset.univ φ (fun _ => 1) (by simpa using sum_boltz_pos _ _)
      (by simpa using sum_boltz_pos _ _) (r := r) (by simpa using h1) (by simpa using h2)
    refine ⟨g, hg, ?_⟩
    unfold gibbsMean
    simpa using hgr

omit [Fintype α] in
/-- **Corollary A11.1, "fills exactly the interval", abstract form**: for a lower set `A` and a
non-empty upper set `B`, the set of values of `Z_{f+g}(A)/Z_{f+g}(B)` over the admissible class
is exactly `[Z_{f-h↓}(A)/Z_{f-h↓}(B), Z_{f+h↑}(A)/Z_{f+h↑}(B)]`. -/
theorem ratio_range_eq_Icc [DecidableEq α] {β : ℝ} (hβ : 0 < β) {f hup hdn : α → ℝ}
    {d : α → α → ℝ} (hf : Submodular f)
    (hsatU : ∀ x y, d (x ⊔ y) y ≤ hup x - hup (x ⊓ y))
    (hsatD : ∀ x y, d (x ⊓ y) x ≤ hdn (x ⊔ y) - hdn y)
    (hUadm : Admissible d hup) (hDadm : Admissible d (fun x => -hdn x))
    (A B : Finset α) (hA : IsLowerSet (A : Set α)) (hB : IsUpperSet (B : Set α))
    (hBne : B.Nonempty) :
    {r | ∃ g, Admissible d g ∧
        zOn β (fun z => f z + g z) A / zOn β (fun z => f z + g z) B = r} =
      Set.Icc (zOn β (fun z => f z - hdn z) A / zOn β (fun z => f z - hdn z) B)
        (zOn β (fun z => f z + hup z) A / zOn β (fun z => f z + hup z) B) := by
  ext r
  constructor
  · rintro ⟨g, hg, rfl⟩
    exact macrostate_ratio hβ.le hf hg hsatU hsatD A B hA hB hBne
  · rintro ⟨h1, h2⟩
    have hsub : (fun z => f z - hdn z) = (fun z => f z + (fun y => -hdn y) z) := by
      funext z
      ring
    rw [hsub] at h1
    unfold zOn at h1 h2
    obtain ⟨g, hg, hgr⟩ := exists_admissible_ratio hβ hDadm hUadm (f := f) A B (fun _ => 1)
      (fun _ => 1) (by simpa [zOn] using zOn_pos β _ hBne)
      (by simpa [zOn] using zOn_pos β _ hBne) (r := r) (by simpa using h1) (by simpa using h2)
    refine ⟨g, hg, ?_⟩
    unfold zOn
    simpa using hgr

end LatticeRange

/-! ### The cube `ι → Bool` -/

section Cube

variable {ι : Type*} [Fintype ι]

/-- The envelope of the note, with separate constants for raising and lowering a site:
`d x y = ∑_{i : x_i = 1, y_i = 0} c↑_i + ∑_{i : x_i = 0, y_i = 1} c↓_i`. -/
def envDist (cup cdn : ι → ℝ) (x y : ι → Bool) : ℝ :=
  (∑ i, if x i && !y i then cup i else 0) + ∑ i, if !x i && y i then cdn i else 0

/-- The field `h x = ∑_i c_i x_i`. -/
def field (c : ι → ℝ) (x : ι → Bool) : ℝ := ∑ i, if x i then c i else 0

/-- `d (x ∨ y, y) = h↑ x - h↑ (x ∧ y)`. -/
theorem envDist_sup_right (cup cdn : ι → ℝ) (x y : ι → Bool) :
    envDist cup cdn (x ⊔ y) y = field cup x - field cup (x ⊓ y) := by
  unfold envDist field
  rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  show (if (x i || y i) && !y i then cup i else 0) + (if !(x i || y i) && y i then cdn i else 0)
      = (if x i then cup i else 0) - (if (x i && y i) then cup i else 0)
  cases x i <;> cases y i <;> simp

/-- `d (x ∧ y, x) = h↓ (x ∨ y) - h↓ y`. -/
theorem envDist_inf_left (cup cdn : ι → ℝ) (x y : ι → Bool) :
    envDist cup cdn (x ⊓ y) x = field cdn (x ⊔ y) - field cdn y := by
  unfold envDist field
  rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  show (if (x i && y i) && !x i then cup i else 0) + (if !(x i && y i) && x i then cdn i else 0)
      = (if (x i || y i) then cdn i else 0) - (if y i then cdn i else 0)
  cases x i <;> cases y i <;> simp

/-- The field `h↑` is admissible as soon as `0 ≤ c↑_i + c↓_i` for every site. -/
theorem field_admissible {cup cdn : ι → ℝ} (hc : ∀ i, 0 ≤ cup i + cdn i) :
    Admissible (envDist cup cdn) (field cup) := by
  intro x y
  unfold envDist field
  rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum (fun i _ => ?_)
  have := hc i
  cases x i <;> cases y i <;> simp
  linarith

/-- The field `-h↓` is admissible as soon as `0 ≤ c↑_i + c↓_i` for every site. -/
theorem neg_field_admissible {cup cdn : ι → ℝ} (hc : ∀ i, 0 ≤ cup i + cdn i) :
    Admissible (envDist cup cdn) (fun x => -field cdn x) := by
  intro x y
  have key : field cdn y - field cdn x ≤ envDist cup cdn x y := by
    unfold envDist field
    rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum (fun i _ => ?_)
    have := hc i
    cases x i <;> cases y i <;> simp
    linarith
  linarith

variable [DecidableEq ι]

/-- If the class is non-empty then `0 ≤ c↑_i + c↓_i` for every site (so the hypothesis of
`field_admissible` costs nothing). -/
theorem add_nonneg_of_admissible {cup cdn : ι → ℝ} {g : (ι → Bool) → ℝ}
    (hg : Admissible (envDist cup cdn) g) (i : ι) : 0 ≤ cup i + cdn i := by
  set x : ι → Bool := fun j => decide (j = i) with hx
  set y : ι → Bool := fun _ => false with hy
  have h1 := hg x y
  have h2 := hg y x
  have e1 : envDist cup cdn x y = cup i := by
    unfold envDist
    simp [hx, hy]
  have e2 : envDist cup cdn y x = cdn i := by
    unfold envDist
    simp [hx, hy]
  rw [e1] at h1
  rw [e2] at h2
  linarith

omit [DecidableEq ι] in
/-- **Holley condition of Theorem A11, lower end, written out.** -/
theorem cube_holley_lower {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hf : Submodular f) (hg : Admissible (envDist cup cdn) g) (x y : ι → Bool) :
    Real.exp (-(β * (f x + field cup x))) * Real.exp (-(β * (f y + g y))) ≤
      Real.exp (-(β * (f (x ⊓ y) + field cup (x ⊓ y)))) *
        Real.exp (-(β * (f (x ⊔ y) + g (x ⊔ y)))) :=
  holley_condition_lower_of_saturation hβ hf hg
    (fun a b => (envDist_sup_right cup cdn a b).le) x y

omit [DecidableEq ι] in
/-- **Holley condition of Theorem A11, upper end, written out.** -/
theorem cube_holley_upper {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hf : Submodular f) (hg : Admissible (envDist cup cdn) g) (x y : ι → Bool) :
    Real.exp (-(β * (f x + g x))) * Real.exp (-(β * (f y - field cdn y))) ≤
      Real.exp (-(β * (f (x ⊓ y) + g (x ⊓ y)))) *
        Real.exp (-(β * (f (x ⊔ y) - field cdn (x ⊔ y)))) :=
  holley_condition_upper_of_saturation hβ hf hg
    (fun a b => (envDist_inf_left cup cdn a b).le) x y

/-- **Theorem A11, lower end, cross-multiplied, written out**: for every monotone `φ`,
`(∑ φ e^{-β(f+h↑)}) (∑ e^{-β(f+g)}) ≤ (∑ e^{-β(f+h↑)}) (∑ φ e^{-β(f+g)})`. -/
theorem cube_sandwich_cross_lower {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ}
    {cup cdn : ι → ℝ} (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    {φ : (ι → Bool) → ℝ} (hφ : Monotone φ) :
    (∑ x, φ x * Real.exp (-(β * (f x + field cup x)))) * (∑ x, Real.exp (-(β * (f x + g x)))) ≤
      (∑ x, Real.exp (-(β * (f x + field cup x)))) * (∑ x, φ x * Real.exp (-(β * (f x + g x)))) :=
  sandwich_cross_lower hβ hf hg (fun a b => (envDist_sup_right cup cdn a b).le) hφ

/-- **Theorem A11, upper end, cross-multiplied, written out**: for every monotone `φ`,
`(∑ φ e^{-β(f+g)}) (∑ e^{-β(f-h↓)}) ≤ (∑ e^{-β(f+g)}) (∑ φ e^{-β(f-h↓)})`. -/
theorem cube_sandwich_cross_upper {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ}
    {cup cdn : ι → ℝ} (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    {φ : (ι → Bool) → ℝ} (hφ : Monotone φ) :
    (∑ x, φ x * Real.exp (-(β * (f x + g x)))) * (∑ x, Real.exp (-(β * (f x - field cdn x)))) ≤
      (∑ x, Real.exp (-(β * (f x + g x)))) * (∑ x, φ x * Real.exp (-(β * (f x - field cdn x)))) :=
  sandwich_cross_upper hβ hf hg (fun a b => (envDist_inf_left cup cdn a b).le) hφ

/-- **Theorem A11 on the cube**: `E_{f+h↑} φ ≤ E_{f+g} φ ≤ E_{f-h↓} φ` for every monotone `φ`,
every submodular `f`, every admissible `g`, every `β ≥ 0`. -/
theorem cube_sandwich_mean {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    {φ : (ι → Bool) → ℝ} (hφ : Monotone φ) :
    gibbsMean β (fun x => f x + field cup x) φ ≤ gibbsMean β (fun x => f x + g x) φ ∧
      gibbsMean β (fun x => f x + g x) φ ≤ gibbsMean β (fun x => f x - field cdn x) φ :=
  sandwich_mean hβ hf hg (fun a b => (envDist_sup_right cup cdn a b).le)
    (fun a b => (envDist_inf_left cup cdn a b).le) hφ

omit [DecidableEq ι] in
/-- **Corollary A11.1, upper end, cross-multiplied** (lower set `A`, upper set `B`):
`Z_{f+g}(A) * Z_{f+h↑}(B) ≤ Z_{f+h↑}(A) * Z_{f+g}(B)`. -/
theorem cube_macrostate_cross_upper {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ}
    {cup cdn : ι → ℝ} (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    (A B : Finset (ι → Bool)) (hA : IsLowerSet (A : Set (ι → Bool)))
    (hB : IsUpperSet (B : Set (ι → Bool))) :
    (∑ x ∈ A, Real.exp (-(β * (f x + g x)))) * (∑ x ∈ B, Real.exp (-(β * (f x + field cup x)))) ≤
      (∑ x ∈ A, Real.exp (-(β * (f x + field cup x)))) * (∑ x ∈ B, Real.exp (-(β * (f x + g x)))) :=
  macrostate_cross_upper hβ hf hg (fun a b => (envDist_sup_right cup cdn a b).le) A B hA hB

omit [DecidableEq ι] in
/-- **Corollary A11.1, lower end, cross-multiplied** (lower set `A`, upper set `B`):
`Z_{f-h↓}(A) * Z_{f+g}(B) ≤ Z_{f+g}(A) * Z_{f-h↓}(B)`. -/
theorem cube_macrostate_cross_lower {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ}
    {cup cdn : ι → ℝ} (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    (A B : Finset (ι → Bool)) (hA : IsLowerSet (A : Set (ι → Bool)))
    (hB : IsUpperSet (B : Set (ι → Bool))) :
    (∑ x ∈ A, Real.exp (-(β * (f x - field cdn x)))) * (∑ x ∈ B, Real.exp (-(β * (f x + g x)))) ≤
      (∑ x ∈ A, Real.exp (-(β * (f x + g x)))) * (∑ x ∈ B, Real.exp (-(β * (f x - field cdn x)))) :=
  macrostate_cross_lower hβ hf hg (fun a b => (envDist_inf_left cup cdn a b).le) A B hA hB

omit [DecidableEq ι] in
/-- **Corollary A11.1 (inequalities)** for a lower set `A` and a non-empty upper set `B`:
`Z_{f-h↓}(A)/Z_{f-h↓}(B) ≤ Z_{f+g}(A)/Z_{f+g}(B) ≤ Z_{f+h↑}(A)/Z_{f+h↑}(B)`. -/
theorem cube_macrostate_ratio {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    (A B : Finset (ι → Bool)) (hA : IsLowerSet (A : Set (ι → Bool)))
    (hB : IsUpperSet (B : Set (ι → Bool))) (hBne : B.Nonempty) :
    zOn β (fun x => f x - field cdn x) A / zOn β (fun x => f x - field cdn x) B ≤
        zOn β (fun x => f x + g x) A / zOn β (fun x => f x + g x) B ∧
      zOn β (fun x => f x + g x) A / zOn β (fun x => f x + g x) B ≤
        zOn β (fun x => f x + field cup x) A / zOn β (fun x => f x + field cup x) B :=
  macrostate_ratio hβ hf hg (fun a b => (envDist_sup_right cup cdn a b).le)
    (fun a b => (envDist_inf_left cup cdn a b).le) A B hA hB hBne

/-- The complement of an upper set is a lower set (as finsets). -/
theorem isLowerSet_compl_finset {γ : Type*} [Preorder γ] [Fintype γ] [DecidableEq γ]
    {B : Finset γ} (hB : IsUpperSet (B : Set γ)) : IsLowerSet ((Bᶜ : Finset γ) : Set γ) := by
  intro a b hba ha
  simp only [Finset.coe_compl, Set.mem_compl_iff, Finset.mem_coe] at ha ⊢
  exact fun hb => ha (Finset.mem_coe.1 (hB hba (Finset.mem_coe.2 hb)))

/-- **Corollary A11.1 (inequalities), in the note's form**: `B` a non-empty up-set and
`A = X ∖ B`. -/
theorem cube_macrostate_ratio_compl {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ}
    {cup cdn : ι → ℝ} (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    (B : Finset (ι → Bool)) (hB : IsUpperSet (B : Set (ι → Bool))) (hBne : B.Nonempty) :
    zOn β (fun x => f x - field cdn x) Bᶜ / zOn β (fun x => f x - field cdn x) B ≤
        zOn β (fun x => f x + g x) Bᶜ / zOn β (fun x => f x + g x) B ∧
      zOn β (fun x => f x + g x) Bᶜ / zOn β (fun x => f x + g x) B ≤
        zOn β (fun x => f x + field cup x) Bᶜ / zOn β (fun x => f x + field cup x) B :=
  cube_macrostate_ratio hβ hf hg Bᶜ B (isLowerSet_compl_finset hB) hB hBne

/-- **Both ends of Theorem A11 are attained, lower end**: the least value of `E_{f+g} φ` over the
class is the value at the field `g = h↑`. -/
theorem cube_mean_isLeast {β : ℝ} (hβ : 0 ≤ β) {f : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hc : ∀ i, 0 ≤ cup i + cdn i) (hf : Submodular f) {φ : (ι → Bool) → ℝ} (hφ : Monotone φ) :
    IsLeast {r | ∃ g, Admissible (envDist cup cdn) g ∧ gibbsMean β (fun x => f x + g x) φ = r}
      (gibbsMean β (fun x => f x + field cup x) φ) := by
  refine ⟨⟨field cup, field_admissible hc, rfl⟩, ?_⟩
  rintro r ⟨g, hg, rfl⟩
  exact (cube_sandwich_mean hβ hf hg hφ).1

/-- **Both ends of Theorem A11 are attained, upper end**: the greatest value of `E_{f+g} φ` over
the class is the value at the field `g = -h↓`. -/
theorem cube_mean_isGreatest {β : ℝ} (hβ : 0 ≤ β) {f : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hc : ∀ i, 0 ≤ cup i + cdn i) (hf : Submodular f) {φ : (ι → Bool) → ℝ} (hφ : Monotone φ) :
    IsGreatest {r | ∃ g, Admissible (envDist cup cdn) g ∧ gibbsMean β (fun x => f x + g x) φ = r}
      (gibbsMean β (fun x => f x - field cdn x) φ) := by
  refine ⟨⟨fun x => -field cdn x, neg_field_admissible hc, ?_⟩, ?_⟩
  · simp only [sub_eq_add_neg]
  · rintro r ⟨g, hg, rfl⟩
    exact (cube_sandwich_mean hβ hf hg hφ).2

/-- **Theorem A11, "every value in between is attained"**: for `0 < β` the set of values of
`E_{f+g} φ` over the admissible class is exactly the closed interval between the values at the
two fields. -/
theorem cube_mean_range_eq_Icc {β : ℝ} (hβ : 0 < β) {f : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hc : ∀ i, 0 ≤ cup i + cdn i) (hf : Submodular f) {φ : (ι → Bool) → ℝ} (hφ : Monotone φ) :
    {r | ∃ g, Admissible (envDist cup cdn) g ∧ gibbsMean β (fun x => f x + g x) φ = r} =
      Set.Icc (gibbsMean β (fun x => f x + field cup x) φ)
        (gibbsMean β (fun x => f x - field cdn x) φ) :=
  mean_range_eq_Icc hβ hf (fun a b => (envDist_sup_right cup cdn a b).le)
    (fun a b => (envDist_inf_left cup cdn a b).le) (field_admissible hc)
    (neg_field_admissible hc) hφ

omit [DecidableEq ι] in
/-- **Corollary A11.1, "fills exactly the interval"**: for `0 < β`, a lower set `A` and a
non-empty upper set `B`, the set of values of `Z_{f+g}(A)/Z_{f+g}(B)` over the admissible class
is exactly `[Z_{f-h↓}(A)/Z_{f-h↓}(B), Z_{f+h↑}(A)/Z_{f+h↑}(B)]`. -/
theorem cube_ratio_range_eq_Icc {β : ℝ} (hβ : 0 < β) {f : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hc : ∀ i, 0 ≤ cup i + cdn i) (hf : Submodular f)
    (A B : Finset (ι → Bool)) (hA : IsLowerSet (A : Set (ι → Bool)))
    (hB : IsUpperSet (B : Set (ι → Bool))) (hBne : B.Nonempty) :
    {r | ∃ g, Admissible (envDist cup cdn) g ∧
        zOn β (fun x => f x + g x) A / zOn β (fun x => f x + g x) B = r} =
      Set.Icc (zOn β (fun x => f x - field cdn x) A / zOn β (fun x => f x - field cdn x) B)
        (zOn β (fun x => f x + field cup x) A / zOn β (fun x => f x + field cup x) B) :=
  ratio_range_eq_Icc hβ hf (fun a b => (envDist_sup_right cup cdn a b).le)
    (fun a b => (envDist_inf_left cup cdn a b).le) (field_admissible hc)
    (neg_field_admissible hc) A B hA hB hBne

omit [DecidableEq ι] in
/-- Additive known parts are submodular (with equality). -/
theorem field_submodular (c : ι → ℝ) : Submodular (field c) := by
  intro x y
  unfold field
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  refine Finset.sum_le_sum (fun i _ => ?_)
  show (if (x i || y i) then c i else 0) + (if (x i && y i) then c i else 0) ≤
    (if x i then c i else 0) + (if y i then c i else 0)
  cases x i <;> cases y i <;> simp

omit [Fintype ι] [DecidableEq ι] in
/-- A pair term `J [x_i ∧ x_j]` with `J ≤ 0` (no frustration) is submodular. -/
theorem pairTerm_submodular (i j : ι) {J : ℝ} (hJ : J ≤ 0) :
    Submodular (fun x : ι → Bool => if x i && x j then J else 0) := by
  intro x y
  show (if (x i || y i) && (x j || y j) then J else 0) +
      (if (x i && y i) && (x j && y j) then J else 0) ≤
    (if x i && x j then J else 0) + (if y i && y j then J else 0)
  cases x i <;> cases x j <;> cases y i <;> cases y j <;> simp <;> linarith

omit [Fintype ι] [DecidableEq ι] in
/-- Finite sums of submodular functions are submodular. -/
theorem submodular_sum {κ : Type*} (s : Finset κ) (F : κ → (ι → Bool) → ℝ)
    (hF : ∀ k ∈ s, Submodular (F k)) : Submodular (fun x => ∑ k ∈ s, F k x) := by
  intro x y
  simp only
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  exact Finset.sum_le_sum (fun k hk => hF k hk x y)

omit [DecidableEq ι] in
/-- **Every pairwise known part without frustration is submodular**:
`f x = ∑_i a_i x_i + ∑_{i,j} J_ij x_i x_j` with all `J_ij ≤ 0`. -/
theorem pairwise_submodular (a : ι → ℝ) (J : ι → ι → ℝ) (hJ : ∀ i j, J i j ≤ 0) :
    Submodular (fun x : ι → Bool =>
      field a x + ∑ i, ∑ j, if x i && x j then J i j else 0) := by
  intro x y
  have h1 := field_submodular a x y
  have h2 := submodular_sum Finset.univ
    (fun i (x : ι → Bool) => ∑ j, if x i && x j then J i j else 0)
    (fun i _ => submodular_sum Finset.univ
      (fun j (x : ι → Bool) => if x i && x j then J i j else 0)
      (fun j _ => pairTerm_submodular i j (hJ i j))) x y
  simp only at h2 ⊢
  linarith

end Cube

/-! ### The sign of the summands in Corollary A11.2 (FKG)

Corollary A11.2 writes the width of the robust interval as an integral of
`∑_i c_i (⟨x_i⟩_{B,t} - ⟨x_i⟩_{A,t})`, `⟨·⟩_{S,t}` the mean in `μ_{f + t h}(· | S)`, and says
that every summand is non-negative.  The integral is not formalised; the sign is: for a lower
set `A` and an upper set `B`, the conditional occupation of a site is larger on `B`. -/

section Occupation

/-- For a log-supermodular weight on a distributive lattice, a lower set `A` and upper sets
`B, U`: `w(A ∩ U) w(B) ≤ w(A) w(B ∩ U)`. -/
theorem updown_inter_cross {α : Type*} [DistribLattice α] [DecidableEq α] (w : α → ℝ)
    (hw : ∀ x, 0 ≤ w x) (h : ∀ x y, w x * w y ≤ w (x ⊓ y) * w (x ⊔ y))
    (A B U : Finset α) (hA : IsLowerSet (A : Set α)) (hB : IsUpperSet (B : Set α))
    (hU : IsUpperSet (U : Set α)) :
    (∑ x ∈ A ∩ U, w x) * (∑ x ∈ B, w x) ≤ (∑ x ∈ A, w x) * (∑ x ∈ B ∩ U, w x) := by
  have key := four_functions_theorem w w w w hw hw hw hw h (A ∩ U) B
  have hsub1 : (A ∩ U) ⊼ B ⊆ A := by
    intro z hz
    obtain ⟨a, ha, b, _, rfl⟩ := Finset.mem_infs.1 hz
    exact Finset.mem_coe.1 (hA inf_le_left (Finset.mem_coe.2 (Finset.mem_inter.1 ha).1))
  have hsub2 : (A ∩ U) ⊻ B ⊆ B ∩ U := by
    intro z hz
    obtain ⟨a, ha, b, hb, rfl⟩ := Finset.mem_sups.1 hz
    exact Finset.mem_inter.2 ⟨Finset.mem_coe.1 (hB le_sup_right (Finset.mem_coe.2 hb)),
      Finset.mem_coe.1 (hU le_sup_left (Finset.mem_coe.2 (Finset.mem_inter.1 ha).2))⟩
  calc (∑ x ∈ A ∩ U, w x) * (∑ x ∈ B, w x)
      ≤ (∑ a ∈ (A ∩ U) ⊼ B, w a) * ∑ a ∈ (A ∩ U) ⊻ B, w a := key
    _ ≤ (∑ x ∈ A, w x) * (∑ x ∈ B ∩ U, w x) := by
        apply mul_le_mul
        · exact Finset.sum_le_sum_of_subset_of_nonneg hsub1 (fun x _ _ => hw x)
        · exact Finset.sum_le_sum_of_subset_of_nonneg hsub2 (fun x _ _ => hw x)
        · exact Finset.sum_nonneg (fun x _ => hw x)
        · exact Finset.sum_nonneg (fun x _ => hw x)

/-- The Boltzmann weight of a submodular energy is log-supermodular (`β ≥ 0`). -/
theorem boltz_logSupermodular {α : Type*} [Lattice α] {β : ℝ} (hβ : 0 ≤ β) {e : α → ℝ}
    (he : Submodular e) (x y : α) :
    boltz β e x * boltz β e y ≤ boltz β e (x ⊓ y) * boltz β e (x ⊔ y) := by
  unfold boltz
  rw [← Real.exp_add, ← Real.exp_add, Real.exp_le_exp]
  have h := mul_le_mul_of_nonneg_left (he x y) hβ
  linarith

variable {ι : Type*} [Fintype ι]

/-- Fields are modular. -/
theorem field_modular (c : ι → ℝ) (x y : ι → Bool) :
    field c (x ⊔ y) + field c (x ⊓ y) = field c x + field c y := by
  unfold field
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  show (if (x i || y i) then c i else 0) + (if (x i && y i) then c i else 0) =
    (if x i then c i else 0) + (if y i then c i else 0)
  cases x i <;> cases y i <;> simp

/-- **Sign of the summands of Corollary A11.2.**  For submodular `f`, any field `h = ∑ c_i x_i`,
any real `t`, `β ≥ 0`, a lower set `A` and an upper set `B`, and any site `i`:
`Z_{f+th}(A ∩ {x_i = 1}) · Z_{f+th}(B) ≤ Z_{f+th}(A) · Z_{f+th}(B ∩ {x_i = 1})`,
i.e. `⟨x_i⟩_{A,t} ≤ ⟨x_i⟩_{B,t}`. -/
theorem cube_occupation_cross {β : ℝ} (hβ : 0 ≤ β) {f : (ι → Bool) → ℝ} (hf : Submodular f)
    (c : ι → ℝ) (t : ℝ) (i : ι) (A B : Finset (ι → Bool))
    (hA : IsLowerSet (A : Set (ι → Bool))) (hB : IsUpperSet (B : Set (ι → Bool))) :
    zOn β (fun x => f x + t * field c x) (A.filter (fun x => x i = true)) *
        zOn β (fun x => f x + t * field c x) B ≤
      zOn β (fun x => f x + t * field c x) A *
        zOn β (fun x => f x + t * field c x) (B.filter (fun x => x i = true)) := by
  classical
  have he : Submodular (fun x : ι → Bool => f x + t * field c x) := by
    intro x y
    have h1 := hf x y
    have h2 := field_modular c x y
    have h3 : t * (field c (x ⊔ y) + field c (x ⊓ y)) = t * (field c x + field c y) := by
      rw [h2]
    simp only
    linarith
  have hU : IsUpperSet (((Finset.univ : Finset (ι → Bool)).filter (fun x => x i = true) :
      Finset (ι → Bool)) : Set (ι → Bool)) := by
    intro x y hxy hx
    simp only [Finset.coe_filter, Finset.mem_univ, true_and, Set.mem_setOf_eq] at hx ⊢
    have h := hxy i
    rw [hx] at h
    exact le_antisymm le_top h
  have key := updown_inter_cross (boltz β (fun x => f x + t * field c x))
    (fun x => (boltz_pos _ _ x).le) (boltz_logSupermodular hβ he) A B
    ((Finset.univ : Finset (ι → Bool)).filter (fun x => x i = true)) hA hB hU
  have eA : A ∩ (Finset.univ : Finset (ι → Bool)).filter (fun x => x i = true) =
      A.filter (fun x => x i = true) := by
    ext x
    simp
  have eB : B ∩ (Finset.univ : Finset (ι → Bool)).filter (fun x => x i = true) =
      B.filter (fun x => x i = true) := by
    ext x
    simp
  rw [eA, eB] at key
  exact key

/-- The same as an inequality between conditional occupations, for non-empty `A` and `B`:
`⟨x_i⟩_{A,t} ≤ ⟨x_i⟩_{B,t}`. -/
theorem cube_occupation_mono {β : ℝ} (hβ : 0 ≤ β) {f : (ι → Bool) → ℝ} (hf : Submodular f)
    (c : ι → ℝ) (t : ℝ) (i : ι) (A B : Finset (ι → Bool))
    (hA : IsLowerSet (A : Set (ι → Bool))) (hB : IsUpperSet (B : Set (ι → Bool)))
    (hAne : A.Nonempty) (hBne : B.Nonempty) :
    zOn β (fun x => f x + t * field c x) (A.filter (fun x => x i = true)) /
        zOn β (fun x => f x + t * field c x) A ≤
      zOn β (fun x => f x + t * field c x) (B.filter (fun x => x i = true)) /
        zOn β (fun x => f x + t * field c x) B := by
  rw [div_le_div_iff₀ (zOn_pos _ _ hAne) (zOn_pos _ _ hBne)]
  have := cube_occupation_cross hβ hf c t i A B hA hB
  linarith

end Occupation

/-! ### Ordered alphabets (Remark (1) of A11): a product of finite chains

Sites `i : ι` with levels `0, …, k i - 1` (the alphabet `Fin (k i)`), coordinatewise order.
Raising site `i` from level `r` to `r + 1` costs `c↑ i r`, lowering it from `r + 1` to `r` costs
`c↓ i r`; the envelope is additive along each chain:
`d x y = ∑_i (∑_{y_i ≤ r < x_i} c↑ i r + ∑_{x_i ≤ r < y_i} c↓ i r)`.  The additive functions
`h↑ x = ∑_i ∑_{r < x_i} c↑ i r` and `h↓ x = ∑_i ∑_{r < x_i} c↓ i r` saturate it, so the sandwich
holds verbatim.  The cube is the case `k i = 2`. -/

section Chains

variable {ι : Type*} [Fintype ι] {k : ι → ℕ}

/-- The envelope that is additive along each chain. -/
def chainDist (cup cdn : ι → ℕ → ℝ) (x y : ∀ i, Fin (k i)) : ℝ :=
  ∑ i, ((∑ r ∈ Finset.Ico (y i : ℕ) (x i : ℕ), cup i r) +
    ∑ r ∈ Finset.Ico (x i : ℕ) (y i : ℕ), cdn i r)

/-- The additive function `x ↦ ∑_i ∑_{r < x_i} c i r`. -/
def chainField (c : ι → ℕ → ℝ) (x : ∀ i, Fin (k i)) : ℝ :=
  ∑ i, ∑ r ∈ Finset.range (x i : ℕ), c i r

/-- `d (x ∨ y, y) = h↑ x - h↑ (x ∧ y)` on a product of chains. -/
theorem chainDist_sup_right (cup cdn : ι → ℕ → ℝ) (x y : ∀ i, Fin (k i)) :
    chainDist cup cdn (x ⊔ y) y = chainField cup x - chainField cup (x ⊓ y) := by
  unfold chainDist chainField
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rcases le_total (x i) (y i) with h | h
  · have e1 : (x ⊔ y) i = y i := by
      rw [Pi.sup_apply]
      exact sup_of_le_right h
    have e2 : (x ⊓ y) i = x i := by
      rw [Pi.inf_apply]
      exact inf_of_le_left h
    rw [e1, e2]
    simp
  · have e1 : (x ⊔ y) i = x i := by
      rw [Pi.sup_apply]
      exact sup_of_le_left h
    have e2 : (x ⊓ y) i = y i := by
      rw [Pi.inf_apply]
      exact inf_of_le_right h
    have hle : (y i : ℕ) ≤ (x i : ℕ) := h
    rw [e1, e2, Finset.sum_Ico_eq_sub _ hle, Finset.Ico_eq_empty_of_le hle, Finset.sum_empty,
      add_zero]

/-- `d (x ∧ y, x) = h↓ (x ∨ y) - h↓ y` on a product of chains. -/
theorem chainDist_inf_left (cup cdn : ι → ℕ → ℝ) (x y : ∀ i, Fin (k i)) :
    chainDist cup cdn (x ⊓ y) x = chainField cdn (x ⊔ y) - chainField cdn y := by
  unfold chainDist chainField
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rcases le_total (x i) (y i) with h | h
  · have e1 : (x ⊔ y) i = y i := by
      rw [Pi.sup_apply]
      exact sup_of_le_right h
    have e2 : (x ⊓ y) i = x i := by
      rw [Pi.inf_apply]
      exact inf_of_le_left h
    rw [e1, e2]
    simp
  · have e1 : (x ⊔ y) i = x i := by
      rw [Pi.sup_apply]
      exact sup_of_le_left h
    have e2 : (x ⊓ y) i = y i := by
      rw [Pi.inf_apply]
      exact inf_of_le_right h
    have hle : (y i : ℕ) ≤ (x i : ℕ) := h
    rw [e1, e2, Finset.sum_Ico_eq_sub _ hle, Finset.Ico_eq_empty_of_le hle, Finset.sum_empty,
      zero_add]

/-- `h↑` is admissible when `0 ≤ c↑ i r + c↓ i r` for every site and level. -/
theorem chainField_admissible {cup cdn : ι → ℕ → ℝ} (hc : ∀ i r, 0 ≤ cup i r + cdn i r) :
    Admissible (chainDist (k := k) cup cdn) (chainField cup) := by
  intro x y
  unfold chainDist chainField
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum (fun i _ => ?_)
  rcases le_total (x i : ℕ) (y i : ℕ) with h | h
  · have h0 : 0 ≤ ∑ r ∈ Finset.Ico (x i : ℕ) (y i : ℕ), (cup i r + cdn i r) :=
      Finset.sum_nonneg (fun r _ => hc i r)
    rw [Finset.sum_add_distrib, Finset.sum_Ico_eq_sub _ h] at h0
    rw [Finset.Ico_eq_empty_of_le h, Finset.sum_empty, zero_add]
    linarith
  · rw [Finset.sum_Ico_eq_sub _ h, Finset.Ico_eq_empty_of_le h, Finset.sum_empty, add_zero]

/-- `-h↓` is admissible when `0 ≤ c↑ i r + c↓ i r` for every site and level. -/
theorem neg_chainField_admissible {cup cdn : ι → ℕ → ℝ} (hc : ∀ i r, 0 ≤ cup i r + cdn i r) :
    Admissible (chainDist (k := k) cup cdn) (fun x => -chainField cdn x) := by
  intro x y
  have key : chainField cdn y - chainField cdn x ≤ chainDist cup cdn x y := by
    unfold chainDist chainField
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum (fun i _ => ?_)
    rcases le_total (x i : ℕ) (y i : ℕ) with h | h
    · rw [Finset.sum_Ico_eq_sub (cdn i) h, Finset.Ico_eq_empty_of_le h, Finset.sum_empty,
        zero_add]
    · have h0 : 0 ≤ ∑ r ∈ Finset.Ico (y i : ℕ) (x i : ℕ), (cup i r + cdn i r) :=
        Finset.sum_nonneg (fun r _ => hc i r)
      rw [Finset.sum_add_distrib, Finset.sum_Ico_eq_sub (cdn i) h] at h0
      rw [Finset.Ico_eq_empty_of_le h, Finset.sum_empty, add_zero]
      linarith
  linarith

variable [DecidableEq ι]

/-- **Theorem A11 on a product of finite chains** (Remark (1)):
`E_{f+h↑} φ ≤ E_{f+g} φ ≤ E_{f-h↓} φ` for every monotone `φ`, submodular `f`, admissible `g`. -/
theorem chain_sandwich_mean [∀ i, NeZero (k i)] {β : ℝ} (hβ : 0 ≤ β)
    {f g : (∀ i, Fin (k i)) → ℝ} {cup cdn : ι → ℕ → ℝ} (hf : Submodular f)
    (hg : Admissible (chainDist cup cdn) g) {φ : (∀ i, Fin (k i)) → ℝ} (hφ : Monotone φ) :
    gibbsMean β (fun x => f x + chainField cup x) φ ≤ gibbsMean β (fun x => f x + g x) φ ∧
      gibbsMean β (fun x => f x + g x) φ ≤ gibbsMean β (fun x => f x - chainField cdn x) φ :=
  sandwich_mean hβ hf hg (fun a b => (chainDist_sup_right cup cdn a b).le)
    (fun a b => (chainDist_inf_left cup cdn a b).le) hφ

/-- **Theorem A11 on a product of finite chains, exact range**: for `0 < β` the values of
`E_{f+g} φ` over the class fill exactly the interval between the two additive extremal
residuals. -/
theorem chain_mean_range_eq_Icc [∀ i, NeZero (k i)] {β : ℝ} (hβ : 0 < β)
    {f : (∀ i, Fin (k i)) → ℝ} {cup cdn : ι → ℕ → ℝ} (hc : ∀ i r, 0 ≤ cup i r + cdn i r)
    (hf : Submodular f) {φ : (∀ i, Fin (k i)) → ℝ} (hφ : Monotone φ) :
    {r | ∃ g, Admissible (chainDist cup cdn) g ∧ gibbsMean β (fun x => f x + g x) φ = r} =
      Set.Icc (gibbsMean β (fun x => f x + chainField cup x) φ)
        (gibbsMean β (fun x => f x - chainField cdn x) φ) :=
  mean_range_eq_Icc hβ hf (fun a b => (chainDist_sup_right cup cdn a b).le)
    (fun a b => (chainDist_inf_left cup cdn a b).le) (chainField_admissible hc)
    (neg_chainField_admissible hc) hφ

omit [DecidableEq ι] in
/-- **Corollary A11.1 on a product of finite chains, exact range** of the macrostate ratio for
a lower set `A` and a non-empty upper set `B`. -/
theorem chain_ratio_range_eq_Icc {β : ℝ} (hβ : 0 < β)
    {f : (∀ i, Fin (k i)) → ℝ} {cup cdn : ι → ℕ → ℝ} (hc : ∀ i r, 0 ≤ cup i r + cdn i r)
    (hf : Submodular f) (A B : Finset (∀ i, Fin (k i)))
    (hA : IsLowerSet (A : Set (∀ i, Fin (k i)))) (hB : IsUpperSet (B : Set (∀ i, Fin (k i))))
    (hBne : B.Nonempty) :
    {r | ∃ g, Admissible (chainDist cup cdn) g ∧
        zOn β (fun x => f x + g x) A / zOn β (fun x => f x + g x) B = r} =
      Set.Icc
        (zOn β (fun x => f x - chainField cdn x) A / zOn β (fun x => f x - chainField cdn x) B)
        (zOn β (fun x => f x + chainField cup x) A / zOn β (fun x => f x + chainField cup x) B) :=
  ratio_range_eq_Icc hβ hf (fun a b => (chainDist_sup_right cup cdn a b).le)
    (fun a b => (chainDist_inf_left cup cdn a b).le) (chainField_admissible hc)
    (neg_chainField_admissible hc) A B hA hB hBne

end Chains

/-! ### Addendum A13: arbitrary site quasi-metrics and the step fields

Sites with levels `0, …, k i - 1`; `ds i s t` a function of two levels with `ds i s s ≤ 0` and
the triangle inequality on the levels below `k i` (a quasi-metric on the site alphabet);
`d x y = ∑_i ds i (x i) (y i)`.  Step fields `Γ↑ x = ∑_i ∑_{r < x_i} ds i (r+1) r` and
`Γ↓ x = ∑_i ∑_{r < x_i} ds i r (r+1)`.  The triangle inequality telescoped along the order gives
the saturation *inequalities*, hence the sandwich (the bounds are sound; they are attained when
the envelope is additive along the order, which is the `Chains` section). -/

section StepFields

variable {ι : Type*} [Fintype ι] {k : ι → ℕ}

/-- `d x y = ∑_i ds i (x i) (y i)`. -/
def siteDist (ds : ι → ℕ → ℕ → ℝ) (x y : ∀ i, Fin (k i)) : ℝ :=
  ∑ i, ds i (x i : ℕ) (y i : ℕ)

/-- The step field `Γ↑ x = ∑_i ∑_{r < x_i} ds i (r+1) r`. -/
def stepUp (ds : ι → ℕ → ℕ → ℝ) (x : ∀ i, Fin (k i)) : ℝ :=
  ∑ i, ∑ r ∈ Finset.range (x i : ℕ), ds i (r + 1) r

/-- The step field `Γ↓ x = ∑_i ∑_{r < x_i} ds i r (r+1)`. -/
def stepDn (ds : ι → ℕ → ℕ → ℝ) (x : ∀ i, Fin (k i)) : ℝ :=
  ∑ i, ∑ r ∈ Finset.range (x i : ℕ), ds i r (r + 1)

/-- Triangle inequality telescoped upwards: `dd s t ≤ ∑_{t ≤ r < s} dd (r+1) r`. -/
theorem le_sum_steps_up {K : ℕ} (dd : ℕ → ℕ → ℝ) (h0 : ∀ s, s < K → dd s s ≤ 0)
    (htri : ∀ a b c, a < K → b < K → c < K → dd a c ≤ dd a b + dd b c) {t s : ℕ}
    (hts : t ≤ s) (hs : s < K) : dd s t ≤ ∑ r ∈ Finset.Ico t s, dd (r + 1) r := by
  induction s, hts using Nat.le_induction with
  | base => simpa using h0 t hs
  | succ s hts' ih =>
    rw [Finset.sum_Ico_succ_top hts']
    have h1 := ih (by omega)
    have h2 := htri (s + 1) s t hs (by omega) (by omega)
    linarith

/-- Triangle inequality telescoped downwards: `dd t s ≤ ∑_{t ≤ r < s} dd r (r+1)`. -/
theorem le_sum_steps_dn {K : ℕ} (dd : ℕ → ℕ → ℝ) (h0 : ∀ s, s < K → dd s s ≤ 0)
    (htri : ∀ a b c, a < K → b < K → c < K → dd a c ≤ dd a b + dd b c) {t s : ℕ}
    (hts : t ≤ s) (hs : s < K) : dd t s ≤ ∑ r ∈ Finset.Ico t s, dd r (r + 1) := by
  induction s, hts using Nat.le_induction with
  | base => simpa using h0 t hs
  | succ s hts' ih =>
    rw [Finset.sum_Ico_succ_top hts']
    have h1 := ih (by omega)
    have h2 := htri t s (s + 1) (by omega) (by omega) hs
    linarith

/-- `d (x ∨ y, y) ≤ Γ↑ x - Γ↑ (x ∧ y)` for site quasi-metrics. -/
theorem siteDist_sup_right_le (ds : ι → ℕ → ℕ → ℝ) (h0 : ∀ i s, s < k i → ds i s s ≤ 0)
    (htri : ∀ i a b c, a < k i → b < k i → c < k i → ds i a c ≤ ds i a b + ds i b c)
    (x y : ∀ i, Fin (k i)) :
    siteDist ds (x ⊔ y) y ≤ stepUp ds x - stepUp ds (x ⊓ y) := by
  unfold siteDist stepUp
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum (fun i _ => ?_)
  rcases le_total (x i) (y i) with h | h
  · have e1 : (x ⊔ y) i = y i := by
      rw [Pi.sup_apply]
      exact sup_of_le_right h
    have e2 : (x ⊓ y) i = x i := by
      rw [Pi.inf_apply]
      exact inf_of_le_left h
    rw [e1, e2, sub_self]
    exact h0 i _ (y i).isLt
  · have e1 : (x ⊔ y) i = x i := by
      rw [Pi.sup_apply]
      exact sup_of_le_left h
    have e2 : (x ⊓ y) i = y i := by
      rw [Pi.inf_apply]
      exact inf_of_le_right h
    have hle : (y i : ℕ) ≤ (x i : ℕ) := h
    rw [e1, e2, ← Finset.sum_Ico_eq_sub _ hle]
    exact le_sum_steps_up (ds i) (h0 i) (htri i) hle (x i).isLt

/-- `d (x ∧ y, x) ≤ Γ↓ (x ∨ y) - Γ↓ y` for site quasi-metrics. -/
theorem siteDist_inf_left_le (ds : ι → ℕ → ℕ → ℝ) (h0 : ∀ i s, s < k i → ds i s s ≤ 0)
    (htri : ∀ i a b c, a < k i → b < k i → c < k i → ds i a c ≤ ds i a b + ds i b c)
    (x y : ∀ i, Fin (k i)) :
    siteDist ds (x ⊓ y) x ≤ stepDn ds (x ⊔ y) - stepDn ds y := by
  unfold siteDist stepDn
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum (fun i _ => ?_)
  rcases le_total (x i) (y i) with h | h
  · have e1 : (x ⊔ y) i = y i := by
      rw [Pi.sup_apply]
      exact sup_of_le_right h
    have e2 : (x ⊓ y) i = x i := by
      rw [Pi.inf_apply]
      exact inf_of_le_left h
    rw [e1, e2, sub_self]
    exact h0 i _ (x i).isLt
  · have e1 : (x ⊔ y) i = x i := by
      rw [Pi.sup_apply]
      exact sup_of_le_left h
    have e2 : (x ⊓ y) i = y i := by
      rw [Pi.inf_apply]
      exact inf_of_le_right h
    have hle : (y i : ℕ) ≤ (x i : ℕ) := h
    rw [e1, e2, ← Finset.sum_Ico_eq_sub _ hle]
    exact le_sum_steps_dn (ds i) (h0 i) (htri i) hle (x i).isLt

variable [DecidableEq ι]

/-- **Theorem A13** (sandwich on ordered alphabets, arbitrary site quasi-metrics):
`E_{f+Γ↑} φ ≤ E_{f+g} φ ≤ E_{f-Γ↓} φ` for every monotone `φ`. -/
theorem stepField_sandwich_mean [∀ i, NeZero (k i)] {β : ℝ} (hβ : 0 ≤ β)
    {f g : (∀ i, Fin (k i)) → ℝ} {ds : ι → ℕ → ℕ → ℝ} (h0 : ∀ i s, s < k i → ds i s s ≤ 0)
    (htri : ∀ i a b c, a < k i → b < k i → c < k i → ds i a c ≤ ds i a b + ds i b c)
    (hf : Submodular f) (hg : Admissible (siteDist ds) g) {φ : (∀ i, Fin (k i)) → ℝ}
    (hφ : Monotone φ) :
    gibbsMean β (fun x => f x + stepUp ds x) φ ≤ gibbsMean β (fun x => f x + g x) φ ∧
      gibbsMean β (fun x => f x + g x) φ ≤ gibbsMean β (fun x => f x - stepDn ds x) φ :=
  sandwich_mean hβ hf hg (siteDist_sup_right_le ds h0 htri) (siteDist_inf_left_le ds h0 htri) hφ

omit [DecidableEq ι] in
/-- **Theorem A13, macrostates**: for a lower set `A` and a non-empty upper set `B`,
`Z_{f-Γ↓}(A)/Z_{f-Γ↓}(B) ≤ Z_{f+g}(A)/Z_{f+g}(B) ≤ Z_{f+Γ↑}(A)/Z_{f+Γ↑}(B)`. -/
theorem stepField_macrostate_ratio {β : ℝ} (hβ : 0 ≤ β)
    {f g : (∀ i, Fin (k i)) → ℝ} {ds : ι → ℕ → ℕ → ℝ} (h0 : ∀ i s, s < k i → ds i s s ≤ 0)
    (htri : ∀ i a b c, a < k i → b < k i → c < k i → ds i a c ≤ ds i a b + ds i b c)
    (hf : Submodular f) (hg : Admissible (siteDist ds) g) (A B : Finset (∀ i, Fin (k i)))
    (hA : IsLowerSet (A : Set (∀ i, Fin (k i)))) (hB : IsUpperSet (B : Set (∀ i, Fin (k i))))
    (hBne : B.Nonempty) :
    zOn β (fun x => f x - stepDn ds x) A / zOn β (fun x => f x - stepDn ds x) B ≤
        zOn β (fun x => f x + g x) A / zOn β (fun x => f x + g x) B ∧
      zOn β (fun x => f x + g x) A / zOn β (fun x => f x + g x) B ≤
        zOn β (fun x => f x + stepUp ds x) A / zOn β (fun x => f x + stepUp ds x) B :=
  macrostate_ratio hβ hf hg (siteDist_sup_right_le ds h0 htri)
    (siteDist_inf_left_le ds h0 htri) A B hA hB hBne

end StepFields

/-! ### Non-vacuity: a two-site instance with strict inequalities

Two sites, known part `f x = -[x₀ ∧ x₁]` (submodular, not additive), `c↑ = c↓ = 1`, residual
`g = 0`, `β = 1`, observable `φ = [x₀]`.  Then
`E_{f+h↑} φ = 2e⁻¹/(1+3e⁻¹) < E_f φ = (1+e)/(3+e) < E_{f-h↓} φ = (e+e³)/(1+2e+e³)`. -/

section Witness

/-- Sum over the four points of `Fin 2 → Bool`. -/
theorem sum_fin_two_bool (F : (Fin 2 → Bool) → ℝ) :
    ∑ x, F x = F ![false, false] + F ![false, true] + F ![true, false] + F ![true, true] := by
  have h := Fintype.sum_equiv (finTwoArrowEquiv Bool) F (fun p => F ![p.1, p.2]) (fun x => by
    congr 1
    funext i
    fin_cases i <;> rfl)
  rw [h, Fintype.sum_prod_type]
  simp only [Fintype.sum_bool]
  ring

/-- The field on two sites, written out. -/
theorem field_fin_two (c : Fin 2 → ℝ) (x : Fin 2 → Bool) :
    field c x = (if x 0 then c 0 else 0) + (if x 1 then c 1 else 0) := by
  unfold field
  rw [Fin.sum_univ_two]

/-- The known part of the witness: `-1` if both sites are occupied, `0` otherwise. -/
def wF (x : Fin 2 → Bool) : ℝ := if x 0 && x 1 then -1 else 0

/-- The observable of the witness: occupation of site `0`. -/
def wPhi (x : Fin 2 → Bool) : ℝ := if x 0 then 1 else 0

theorem wF_submodular : Submodular wF := by
  intro x y
  show (if (x 0 || y 0) && (x 1 || y 1) then (-1 : ℝ) else 0) +
      (if (x 0 && y 0) && (x 1 && y 1) then (-1 : ℝ) else 0) ≤
    (if x 0 && x 1 then (-1 : ℝ) else 0) + (if y 0 && y 1 then (-1 : ℝ) else 0)
  cases x 0 <;> cases x 1 <;> cases y 0 <;> cases y 1 <;> norm_num

theorem wPhi_monotone : Monotone wPhi := by
  intro x y hxy
  have h0 : x 0 ≤ y 0 := hxy 0
  unfold wPhi
  revert h0
  cases x 0 <;> cases y 0 <;> simp

theorem zero_admissible_one : Admissible (envDist (fun _ : Fin 2 => (1 : ℝ)) (fun _ => 1))
    (fun _ => (0 : ℝ)) := by
  intro x y
  unfold envDist
  have h1 : 0 ≤ ∑ i : Fin 2, if x i && !y i then (1 : ℝ) else 0 :=
    Finset.sum_nonneg (fun i _ => by split_ifs <;> norm_num)
  have h2 : 0 ≤ ∑ i : Fin 2, if !x i && y i then (1 : ℝ) else 0 :=
    Finset.sum_nonneg (fun i _ => by split_ifs <;> norm_num)
  linarith

/-- **Non-vacuity with strict inequalities.**  In the two-site instance all hypotheses of
`cube_sandwich_mean` hold and both inequalities are strict. -/
theorem cube_sandwich_strict_witness :
    Submodular wF ∧ Monotone wPhi ∧
      Admissible (envDist (fun _ : Fin 2 => (1 : ℝ)) (fun _ => 1)) (fun _ => (0 : ℝ)) ∧
      gibbsMean 1 (fun x => wF x + field (fun _ : Fin 2 => (1 : ℝ)) x) wPhi <
        gibbsMean 1 (fun x => wF x + (fun _ => (0 : ℝ)) x) wPhi ∧
      gibbsMean 1 (fun x => wF x + (fun _ => (0 : ℝ)) x) wPhi <
        gibbsMean 1 (fun x => wF x - field (fun _ : Fin 2 => (1 : ℝ)) x) wPhi := by
  have ha : 0 < Real.exp (-1) := Real.exp_pos _
  have hb : 1 < Real.exp 1 := by
    have := Real.add_one_lt_exp (show (1 : ℝ) ≠ 0 by norm_num)
    linarith
  have hab : Real.exp (-1) * Real.exp 1 = 1 := by
    rw [← Real.exp_add]
    norm_num
  have ha1 : Real.exp (-1) < 1 := by nlinarith [mul_pos ha (sub_pos.2 hb)]
  have hc : Real.exp (1 + 1 + 1) = Real.exp 1 * Real.exp 1 * Real.exp 1 := by
    rw [Real.exp_add, Real.exp_add]
  have hbb : 1 < Real.exp 1 * Real.exp 1 := by nlinarith
  have hbbb : Real.exp 1 * Real.exp 1 < Real.exp 1 * Real.exp 1 * Real.exp 1 := by nlinarith
  refine ⟨wF_submodular, wPhi_monotone, zero_admissible_one, ?_, ?_⟩
  · unfold gibbsMean
    rw [sum_fin_two_bool, sum_fin_two_bool, sum_fin_two_bool, sum_fin_two_bool]
    simp [boltz, wF, wPhi, field_fin_two]
    rw [div_lt_div_iff₀ (by positivity) (by positivity)]
    nlinarith
  · unfold gibbsMean
    rw [sum_fin_two_bool, sum_fin_two_bool, sum_fin_two_bool, sum_fin_two_bool]
    simp [boltz, wF, wPhi, field_fin_two]
    rw [hc, div_lt_div_iff₀ (by positivity) (by positivity)]
    nlinarith

/-- **`β ≥ 0` is needed.**  In the same two-site instance at `β = -1` the lower inequality of
Theorem A11 fails: `E_{f+h↑} φ > E_{f+g} φ`. -/
theorem cube_sandwich_fails_negative_beta :
    Submodular wF ∧ Monotone wPhi ∧
      Admissible (envDist (fun _ : Fin 2 => (1 : ℝ)) (fun _ => 1)) (fun _ => (0 : ℝ)) ∧
      gibbsMean (-1) (fun x => wF x + (fun _ => (0 : ℝ)) x) wPhi <
        gibbsMean (-1) (fun x => wF x + field (fun _ : Fin 2 => (1 : ℝ)) x) wPhi := by
  have ha : 0 < Real.exp (-1) := Real.exp_pos _
  have hb : 1 < Real.exp 1 := by
    have := Real.add_one_lt_exp (show (1 : ℝ) ≠ 0 by norm_num)
    linarith
  have hab : Real.exp (-1) * Real.exp 1 = 1 := by
    rw [← Real.exp_add]
    norm_num
  have ha1 : Real.exp (-1) < 1 := by nlinarith [mul_pos ha (sub_pos.2 hb)]
  refine ⟨wF_submodular, wPhi_monotone, zero_admissible_one, ?_⟩
  unfold gibbsMean
  rw [sum_fin_two_bool, sum_fin_two_bool, sum_fin_two_bool, sum_fin_two_bool]
  simp [boltz, wF, wPhi, field_fin_two]
  rw [div_lt_div_iff₀ (by positivity) (by positivity)]
  nlinarith

end Witness

end ScienceL2

end
