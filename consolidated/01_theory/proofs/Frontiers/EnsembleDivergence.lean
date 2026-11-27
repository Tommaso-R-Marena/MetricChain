import Mathlib
import proofs.Frontiers.FreeEnergySandwich
import proofs.Frontiers.EnvelopeDuality

/-!
# The sandwich gap is a relative entropy: certified error of a reference sampler

Let `w` be the reference ensemble (a probability vector, `w ∝ exp(-β E₀)`) and let
`tilt w Δ β ∝ w · exp(-β Δ)` be the target ensemble of the corrected energy `E₀ + Δ`.

* `kl_reference_target_eq_gap` — the Jensen gap of the free-energy sandwich,
  `log (∑ w exp(-βΔ)) + β ⟨Δ⟩_w`, **is exactly** the relative entropy `KL(w ‖ tilt)` of the target
  ensemble with respect to the reference ensemble.
* `kl_reference_target_le_hoeffding`, `kl_reference_target_le_bounded_differences` — hence
  `0 ≤ KL(reference ‖ target) ≤ β² (b - a)² / 8` for a residual with values in `[a, b]`, and
  `≤ β² ∑ c_i² / 8` for a product reference and a residual with bounded differences `c`.
* `bounded_differences_sandwich_any_reference`, `kl_reference_target_le_any_reference` — for an
  *arbitrary* reference on a product space (no independence) the width is `β² (∑ c_i)² / 8`:
  bounded differences give oscillation at most `∑ c_i` (`osc_le_sum_of_bounded_differences`).
* `correlated_reference_counterexample` — the sum-of-squares width is *false* without the product
  hypothesis: two perfectly correlated binary sites violate it.

Consequence for samplers: any sampler of the reference ensemble is a certified approximate sampler
of the target ensemble, with relative entropy controlled by the envelope constants of the
residual.  Which constants depends on the reference: for an *arbitrary* reference (a
transfer-matrix sampler for a tree-structured `E₀`, a generative model trained on `E₀`) only the
oscillation bound `β² (b - a)² / 8` is available, with `b - a ≤ ∑ c_i`; the bounded-difference
bound `β² ∑ c_i² / 8` requires a *product* reference (independent sites) and is false for
correlated ones (two perfectly correlated binary sites, `Δ = x₁ + x₂`, `β = 1`: gap
`log cosh 1 > 1/4`).  For product references it is sharp (`mcdiarmid_no_better_constant`).
-/

namespace MetricChain

open Finset

variable {Ω : Type*} [Fintype Ω]

/-- Relative entropy of weight vectors on a finite type (terms with `p x = 0` vanish). -/
noncomputable def klFin (p q : Ω → ℝ) : ℝ := ∑ x, p x * (Real.log (p x) - Real.log (q x))

/-- The target ensemble: the reference weights tilted by the Boltzmann factor of the residual. -/
noncomputable def tilt (w Δ : Ω → ℝ) (β : ℝ) (x : Ω) : ℝ :=
  w x * Real.exp (-β * Δ x) / ∑ y, w y * Real.exp (-β * Δ y)

/-- **The sandwich gap is the relative entropy of the target w.r.t. the reference ensemble.** -/
theorem kl_reference_target_eq_gap (w Δ : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1)
    (β : ℝ) :
    klFin w (tilt w Δ β) =
      β * ∑ x, w x * Δ x + Real.log (∑ x, w x * Real.exp (-β * Δ x)) := by
  have hZ : 0 < ∑ y, w y * Real.exp (-β * Δ y) :=
    weighted_exp_sum_pos w (fun y => -β * Δ y) hw hsum
  have hterm : ∀ x, w x * (Real.log (w x) - Real.log (tilt w Δ β x)) =
      w x * (β * Δ x + Real.log (∑ y, w y * Real.exp (-β * Δ y))) := by
    intro x
    rcases (hw x).eq_or_lt with h0 | hpos
    · rw [← h0, zero_mul, zero_mul]
    · congr 1
      unfold tilt
      rw [Real.log_div (mul_pos hpos (Real.exp_pos _)).ne' hZ.ne',
        Real.log_mul hpos.ne' (Real.exp_pos _).ne', Real.log_exp]
      ring
  unfold klFin
  rw [Finset.sum_congr rfl fun x _ => hterm x]
  simp only [mul_add, Finset.sum_add_distrib]
  rw [← Finset.sum_mul, hsum, one_mul, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro x _
  ring

/-- The reference-to-target relative entropy is nonnegative (Gibbs–Bogoliubov). -/
theorem kl_reference_target_nonneg (w Δ : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1)
    (β : ℝ) : 0 ≤ klFin w (tilt w Δ β) := by
  rw [kl_reference_target_eq_gap w Δ hw hsum β]
  have := gibbs_bogoliubov w Δ hw hsum β
  linarith

/-- **Certified sampler error, global oscillation.**  For a residual with values in `[a, b]`,
`KL(reference ‖ target) ≤ β² (b - a)² / 8`. -/
theorem kl_reference_target_le_hoeffding (w Δ : Ω → ℝ) (hw : ∀ x, 0 ≤ w x)
    (hsum : ∑ x, w x = 1) (a b : ℝ) (hΔ : ∀ x, a ≤ Δ x ∧ Δ x ≤ b) (β : ℝ) :
    klFin w (tilt w Δ β) ≤ β ^ 2 * (b - a) ^ 2 / 8 := by
  rw [kl_reference_target_eq_gap w Δ hw hsum β]
  have := hoeffding_upper w Δ hw hsum a b hΔ β
  linarith

/-- **Certified sampler error, bounded differences.**  For a product reference on `n` sites and a
residual with bounded differences `c`, `KL(reference ‖ target) ≤ β² ∑ c_i² / 8`. -/
theorem kl_reference_target_le_bounded_differences {α : Type*} [Fintype α] {n : ℕ}
    (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1)
    (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β : ℝ) :
    klFin (fun x : Fin n → α => ∏ i, p i (x i)) (tilt (fun x => ∏ i, p i (x i)) Δ β) ≤
      β ^ 2 * (∑ i, c i ^ 2) / 8 := by
  rw [kl_reference_target_eq_gap _ Δ (prod_weight_nonneg p hp) (prod_weight_sum_one p hp1) β]
  have := mcdiarmid_log_upper p hp hp1 Δ c hΔ β
  linarith

/-! ### Arbitrary (correlated) references: the Hoeffding width `(∑ c_i)²` -/

section AnyReference

variable {ι : Type*} [Fintype ι] [DecidableEq ι] {σ : ι → Type*} [∀ i, Fintype (σ i)]
  [∀ i, DecidableEq (σ i)]

omit [∀ i, Fintype (σ i)] in
/-- A residual with single-site bounded differences `c` has global oscillation at most
`∑ i, c i`. -/
theorem osc_le_sum_of_bounded_differences (Δ : (∀ i, σ i) → ℝ) (c : ι → ℝ)
    (hΔ : ∀ x i a, Δ (Function.update x i a) - Δ x ≤ c i) (x y : ∀ i, σ i) :
    Δ x - Δ y ≤ ∑ i, c i := by
  have hc : ∀ i, 0 ≤ c i := fun i => by
    have h := hΔ x i (x i)
    rwa [Function.update_eq_self, sub_self] at h
  have hadm : Admissible
      (siteEnvelope fun i (s s' : σ i) => if s = s' then (0 : ℝ) else c i) Δ := by
    apply admissible_of_single_site
    intro z i a
    by_cases h : a = z i
    · subst h
      simp
    · simp only [h, if_false]
      exact hΔ z i a
  have h := hadm x y
  unfold siteEnvelope at h
  refine h.trans (Finset.sum_le_sum fun i _ => ?_)
  show (if x i = y i then (0 : ℝ) else c i) ≤ c i
  split_ifs
  · exact hc i
  · exact le_rfl

/-- **Free-energy sandwich for an arbitrary reference.**  For any probability weights `w` on a
product space — no independence between sites is assumed — and a residual with single-site
bounded differences `c`:
`-β ⟨Δ⟩ ≤ log (∑ x, w x * exp (-β Δ x)) ≤ -β ⟨Δ⟩ + β² (∑ i, c i)² / 8`.
Without a product structure the *square of the sum* replaces the sum of squares of
`bounded_differences_sandwich`, and this cannot be improved to the sum of squares (two perfectly
correlated sites). -/
theorem bounded_differences_sandwich_any_reference (w : (∀ i, σ i) → ℝ) (hw : ∀ x, 0 ≤ w x)
    (hsum : ∑ x, w x = 1) (Δ : (∀ i, σ i) → ℝ) (c : ι → ℝ)
    (hΔ : ∀ x i a, Δ (Function.update x i a) - Δ x ≤ c i) (β : ℝ) :
    -β * ∑ x, w x * Δ x ≤ Real.log (∑ x, w x * Real.exp (-β * Δ x)) ∧
      Real.log (∑ x, w x * Real.exp (-β * Δ x)) ≤
        -β * ∑ x, w x * Δ x + β ^ 2 * (∑ i, c i) ^ 2 / 8 := by
  refine ⟨gibbs_bogoliubov w Δ hw hsum β, ?_⟩
  have hne : (Finset.univ : Finset (∀ i, σ i)).Nonempty := by
    by_contra h
    rw [Finset.not_nonempty_iff_eq_empty] at h
    rw [h, Finset.sum_empty] at hsum
    exact zero_ne_one hsum
  obtain ⟨xmax, -, hmax⟩ := Finset.exists_max_image Finset.univ Δ hne
  obtain ⟨xmin, -, hmin⟩ := Finset.exists_min_image Finset.univ Δ hne
  have hosc := osc_le_sum_of_bounded_differences Δ c hΔ xmax xmin
  have h := hoeffding_upper w Δ hw hsum (Δ xmin) (Δ xmax)
    (fun x => ⟨hmin x (Finset.mem_univ x), hmax x (Finset.mem_univ x)⟩) β
  have h0 : 0 ≤ Δ xmax - Δ xmin := sub_nonneg.mpr (hmin xmax (Finset.mem_univ _))
  have hsq : (Δ xmax - Δ xmin) ^ 2 ≤ (∑ i, c i) ^ 2 := pow_le_pow_left₀ h0 hosc 2
  nlinarith [sq_nonneg β]

/-- **Certified sampler error for an arbitrary reference**: `KL(reference ‖ target) ≤ β² (∑ c_i)² / 8`. -/
theorem kl_reference_target_le_any_reference (w : (∀ i, σ i) → ℝ) (hw : ∀ x, 0 ≤ w x)
    (hsum : ∑ x, w x = 1) (Δ : (∀ i, σ i) → ℝ) (c : ι → ℝ)
    (hΔ : ∀ x i a, Δ (Function.update x i a) - Δ x ≤ c i) (β : ℝ) :
    klFin w (tilt w Δ β) ≤ β ^ 2 * (∑ i, c i) ^ 2 / 8 := by
  rw [kl_reference_target_eq_gap w Δ hw hsum β]
  have := (bounded_differences_sandwich_any_reference w hw hsum Δ c hΔ β).2
  linarith

end AnyReference

/-! ### The product hypothesis cannot be dropped -/

/-- Sum over the four configurations of two binary sites. -/
theorem sum_fin_two_fn (f : (Fin 2 → Fin 2) → ℝ) :
    ∑ x, f x = f ![0, 0] + f ![0, 1] + f ![1, 0] + f ![1, 1] := by
  rw [← (piFinTwoEquiv fun _ => Fin 2).symm.sum_comp f, Fintype.sum_prod_type]
  simp only [Fin.sum_univ_two]
  have e : ∀ a b : Fin 2, (piFinTwoEquiv fun _ => Fin 2).symm (a, b) = ![a, b] := fun a b => rfl
  rw [e, e, e, e]
  ring

theorem fin_two_cast_bounds (a : Fin 2) : (0 : ℝ) ≤ ((a : ℕ) : ℝ) ∧ ((a : ℕ) : ℝ) ≤ 1 := by
  fin_cases a <;> simp

/-- **The sum-of-squares width fails for correlated references.**  Two perfectly correlated binary
sites (`w` uniform on `{(0,0), (1,1)}`), residual `Δ x = x₀ + x₁` with bounded differences
`c = (1, 1)`, at `β = 1`: the Jensen gap `log (∑ w e^{-Δ}) + ⟨Δ⟩ = log cosh 1` exceeds
`β² ∑ c_i² / 8 = 1/4`.  Hence the product hypothesis of `bounded_differences_sandwich` cannot be
dropped. -/
theorem correlated_reference_counterexample :
    ∃ (w Δ : (Fin 2 → Fin 2) → ℝ), (∀ x, 0 ≤ w x) ∧ ∑ x, w x = 1 ∧
      (∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ 1) ∧
        (1 : ℝ) ^ 2 * (∑ _i : Fin 2, (1 : ℝ) ^ 2) / 8 <
          Real.log (∑ x, w x * Real.exp (-1 * Δ x)) + 1 * ∑ x, w x * Δ x := by
  refine ⟨fun x => if x 0 = x 1 then 1 / 2 else 0, fun x => ((x 0 : ℕ) : ℝ) + ((x 1 : ℕ) : ℝ),
    fun x => by dsimp only; split_ifs <;> norm_num, ?_, ?_, ?_⟩
  · rw [sum_fin_two_fn]
    norm_num
  · intro x i a
    have ha := fin_two_cast_bounds a
    have h0 := fin_two_cast_bounds (x 0)
    have h1 := fin_two_cast_bounds (x 1)
    fin_cases i
    · have e1 : Function.update x 0 a 0 = a := Function.update_self 0 a x
      have e2 : Function.update x 0 a 1 = x 1 :=
        Function.update_of_ne (by decide : (1 : Fin 2) ≠ 0) a x
      show |((Function.update x 0 a 0 : ℕ) : ℝ) + ((Function.update x 0 a 1 : ℕ) : ℝ) -
        (((x 0 : ℕ) : ℝ) + ((x 1 : ℕ) : ℝ))| ≤ 1
      rw [e1, e2, abs_le]
      constructor <;> linarith [ha.1, ha.2, h0.1, h0.2]
    · have e1 : Function.update x 1 a 1 = a := Function.update_self 1 a x
      have e2 : Function.update x 1 a 0 = x 0 :=
        Function.update_of_ne (by decide : (0 : Fin 2) ≠ 1) a x
      show |((Function.update x 1 a 0 : ℕ) : ℝ) + ((Function.update x 1 a 1 : ℕ) : ℝ) -
        (((x 0 : ℕ) : ℝ) + ((x 1 : ℕ) : ℝ))| ≤ 1
      rw [e1, e2, abs_le]
      constructor <;> linarith [ha.1, ha.2, h1.1, h1.2]
  · rw [sum_fin_two_fn, sum_fin_two_fn]
    have hsum : (∑ _i : Fin 2, (1 : ℝ) ^ 2) = 2 := by simp
    rw [hsum]
    norm_num
    -- goal: 1/4 < log (1/2 + 1/2 * exp (-2)) + 1   (up to normalisation)
    have hlog2 : Real.log 2 < 3 / 4 := lt_trans Real.log_two_lt_d9 (by norm_num)
    have hexp : Real.exp (-(3 / 4 : ℝ)) < 1 / 2 := by
      rw [← Real.exp_log (by norm_num : (0 : ℝ) < 1 / 2)]
      apply Real.exp_lt_exp.mpr
      rw [one_div, Real.log_inv]
      linarith
    have hpos : (0 : ℝ) < Real.exp (-2) := Real.exp_pos _
    have key : -(3 / 4 : ℝ) < Real.log (1 / 2 + 1 / 2 * Real.exp (-2)) := by
      rw [Real.lt_log_iff_exp_lt (by positivity)]
      linarith
    linarith

end MetricChain
