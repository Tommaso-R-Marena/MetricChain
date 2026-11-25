import Mathlib

/-!
# The stochastic sandwich for robust macrostate ratios (addendum A11)

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
  inequalities, for a lower set `A` and an upper set `B`.

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
* `cube_sandwich_strict_witness` — a two-site instance with a non-additive submodular known
  part in which all hypotheses hold and both inequalities are strict.

Not proved here: Corollaries A11.2 (width formula; it has an integral) and A11.3, the
necessity of the hypotheses (numerical in the note), Remark (1) for ordered alphabets beyond
what the abstract part gives, Remark (2).
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
  cases x i <;> cases y i <;> simp <;> linarith

/-- The field `-h↓` is admissible as soon as `0 ≤ c↑_i + c↓_i` for every site. -/
theorem neg_field_admissible {cup cdn : ι → ℝ} (hc : ∀ i, 0 ≤ cup i + cdn i) :
    Admissible (envDist cup cdn) (fun x => -field cdn x) := by
  intro x y
  have key : field cdn y - field cdn x ≤ envDist cup cdn x y := by
    unfold envDist field
    rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum (fun i _ => ?_)
    have := hc i
    cases x i <;> cases y i <;> simp <;> linarith
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

/-- **Holley condition of Theorem A11, lower end, written out.** -/
theorem cube_holley_lower {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ} {cup cdn : ι → ℝ}
    (hf : Submodular f) (hg : Admissible (envDist cup cdn) g) (x y : ι → Bool) :
    Real.exp (-(β * (f x + field cup x))) * Real.exp (-(β * (f y + g y))) ≤
      Real.exp (-(β * (f (x ⊓ y) + field cup (x ⊓ y)))) *
        Real.exp (-(β * (f (x ⊔ y) + g (x ⊔ y)))) :=
  holley_condition_lower_of_saturation hβ hf hg
    (fun a b => (envDist_sup_right cup cdn a b).le) x y

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

/-- **Corollary A11.1, upper end, cross-multiplied** (lower set `A`, upper set `B`):
`Z_{f+g}(A) * Z_{f+h↑}(B) ≤ Z_{f+h↑}(A) * Z_{f+g}(B)`. -/
theorem cube_macrostate_cross_upper {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ}
    {cup cdn : ι → ℝ} (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    (A B : Finset (ι → Bool)) (hA : IsLowerSet (A : Set (ι → Bool)))
    (hB : IsUpperSet (B : Set (ι → Bool))) :
    (∑ x ∈ A, Real.exp (-(β * (f x + g x)))) * (∑ x ∈ B, Real.exp (-(β * (f x + field cup x)))) ≤
      (∑ x ∈ A, Real.exp (-(β * (f x + field cup x)))) * (∑ x ∈ B, Real.exp (-(β * (f x + g x)))) :=
  macrostate_cross_upper hβ hf hg (fun a b => (envDist_sup_right cup cdn a b).le) A B hA hB

/-- **Corollary A11.1, lower end, cross-multiplied** (lower set `A`, upper set `B`):
`Z_{f-h↓}(A) * Z_{f+g}(B) ≤ Z_{f+g}(A) * Z_{f-h↓}(B)`. -/
theorem cube_macrostate_cross_lower {β : ℝ} (hβ : 0 ≤ β) {f g : (ι → Bool) → ℝ}
    {cup cdn : ι → ℝ} (hf : Submodular f) (hg : Admissible (envDist cup cdn) g)
    (A B : Finset (ι → Bool)) (hA : IsLowerSet (A : Set (ι → Bool)))
    (hB : IsUpperSet (B : Set (ι → Bool))) :
    (∑ x ∈ A, Real.exp (-(β * (f x - field cdn x)))) * (∑ x ∈ B, Real.exp (-(β * (f x + g x)))) ≤
      (∑ x ∈ A, Real.exp (-(β * (f x + g x)))) * (∑ x ∈ B, Real.exp (-(β * (f x - field cdn x)))) :=
  macrostate_cross_lower hβ hf hg (fun a b => (envDist_inf_left cup cdn a b).le) A B hA hB

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

end Cube

end ScienceL2

end

#print axioms ScienceL2.holley_cross_nonneg
#print axioms ScienceL2.holley_cross
#print axioms ScienceL2.updown_cross
#print axioms ScienceL2.holley_condition_lower_of_saturation
#print axioms ScienceL2.holley_condition_upper_of_saturation
#print axioms ScienceL2.sandwich_cross_lower
#print axioms ScienceL2.sandwich_cross_upper
#print axioms ScienceL2.sandwich_mean
#print axioms ScienceL2.macrostate_cross_upper
#print axioms ScienceL2.macrostate_cross_lower
#print axioms ScienceL2.macrostate_ratio
#print axioms ScienceL2.envDist_sup_right
#print axioms ScienceL2.envDist_inf_left
#print axioms ScienceL2.field_admissible
#print axioms ScienceL2.neg_field_admissible
#print axioms ScienceL2.add_nonneg_of_admissible
#print axioms ScienceL2.cube_holley_lower
#print axioms ScienceL2.cube_holley_upper
#print axioms ScienceL2.cube_sandwich_cross_lower
#print axioms ScienceL2.cube_sandwich_cross_upper
#print axioms ScienceL2.cube_sandwich_mean
#print axioms ScienceL2.cube_macrostate_cross_upper
#print axioms ScienceL2.cube_macrostate_cross_lower
#print axioms ScienceL2.cube_macrostate_ratio
#print axioms ScienceL2.cube_macrostate_ratio_compl
