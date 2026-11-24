import Mathlib
import proofs.Frontiers.FreeEnergySandwich

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

Consequence for samplers: any sampler of the reference ensemble (a transfer-matrix sampler for a
tree-structured `E₀`, a generative model trained on `E₀`) is a certified approximate sampler of the
target ensemble, with relative entropy controlled by the envelope constants of the residual — and
the bound is sharp (`mcdiarmid_no_better_constant`).
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

end MetricChain
