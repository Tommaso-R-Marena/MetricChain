import Mathlib
import proofs.Core.Basic

/-!
# Dual decomposition at finite temperature (Hölder / weighted mini-bucket form)

At zero temperature the `sum` rule of the certificate kernel is `min (E₁ + E₂) ≥ min E₁ + min E₂`.
Its finite-temperature deformation is Hölder's inequality: the free energy of `E₁ + E₂` at inverse
temperature `β` is bounded below by the free energies of the parts at the *colder* inverse
temperatures `β / ρ` and `β / (1 - ρ)`:

  `Z_β(E₁ + E₂) ≤ Z_{β/ρ}(E₁)^ρ · Z_{β/(1-ρ)}(E₂)^{1-ρ}`,
  `F_β(E₁ + E₂) ≥ F_{β/ρ}(E₁) + F_{β/(1-ρ)}(E₂)`.

This is the weighted mini-bucket / tree-reweighted bound (Liu–Ihler 2011; Wainwright–Jaakkola–
Willsky 2005) in the vocabulary of this project; it is recorded here, machine-checked, because it
is the sum-product counterpart of the kernel's `sum` rule and tends to it as `β → ∞`.
-/

namespace MetricChain

open Finset

variable {Ω : Type*}

/-- **Hölder decomposition of the partition function.** -/
theorem partitionFn_holder (S : Finset Ω) (E₁ E₂ : Ω → ℝ) {β ρ : ℝ} (hρ0 : 0 < ρ) (hρ1 : ρ < 1) :
    partitionFn β (fun x => E₁ x + E₂ x) S ≤
      partitionFn (β / ρ) E₁ S ^ ρ * partitionFn (β / (1 - ρ)) E₂ S ^ (1 - ρ) := by
  have h1ρ : 0 < 1 - ρ := by linarith
  have hpq : (1 / ρ).HolderConjugate (1 / (1 - ρ)) := by
    rw [Real.holderConjugate_iff]
    refine ⟨by rw [lt_div_iff₀ hρ0]; linarith, ?_⟩
    field_simp
    ring
  have key := Real.inner_le_Lp_mul_Lq S (fun x => Real.exp (-β * E₁ x))
    (fun x => Real.exp (-β * E₂ x)) hpq
  have hf : ∀ x, |Real.exp (-β * E₁ x)| ^ (1 / ρ) = Real.exp (-(β / ρ) * E₁ x) := by
    intro x
    rw [abs_of_pos (Real.exp_pos _), ← Real.exp_mul]
    congr 1
    field_simp
  have hg : ∀ x, |Real.exp (-β * E₂ x)| ^ (1 / (1 - ρ)) = Real.exp (-(β / (1 - ρ)) * E₂ x) := by
    intro x
    rw [abs_of_pos (Real.exp_pos _), ← Real.exp_mul]
    congr 1
    field_simp
  simp only [hf, hg] at key
  simp only [one_div, inv_inv] at key
  unfold partitionFn
  calc ∑ x ∈ S, Real.exp (-β * (E₁ x + E₂ x))
      = ∑ x ∈ S, Real.exp (-β * E₁ x) * Real.exp (-β * E₂ x) := by
        apply Finset.sum_congr rfl
        intro x _
        rw [← Real.exp_add]
        ring_nf
    _ ≤ _ := key

/-- **Free-energy form: dual decomposition with temperature rescaling.** -/
theorem freeEnergy_holder {S : Finset Ω} (hS : S.Nonempty) (E₁ E₂ : Ω → ℝ) {β ρ : ℝ}
    (hβ : 0 < β) (hρ0 : 0 < ρ) (hρ1 : ρ < 1) :
    freeEnergy (β / ρ) E₁ S + freeEnergy (β / (1 - ρ)) E₂ S ≤
      freeEnergy β (fun x => E₁ x + E₂ x) S := by
  have h1ρ : 0 < 1 - ρ := by linarith
  have hZ := partitionFn_pos β (fun x => E₁ x + E₂ x) hS
  have hZ1 := partitionFn_pos (β / ρ) E₁ hS
  have hZ2 := partitionFn_pos (β / (1 - ρ)) E₂ hS
  have hlog := Real.log_le_log hZ (partitionFn_holder S E₁ E₂ hρ0 hρ1)
  rw [Real.log_mul (Real.rpow_pos_of_pos hZ1 ρ).ne' (Real.rpow_pos_of_pos hZ2 (1 - ρ)).ne',
    Real.log_rpow hZ1, Real.log_rpow hZ2] at hlog
  unfold freeEnergy
  have e1 : -(1 / (β / ρ)) * Real.log (partitionFn (β / ρ) E₁ S) =
      -(1 / β) * (ρ * Real.log (partitionFn (β / ρ) E₁ S)) := by
    field_simp
  have e2 : -(1 / (β / (1 - ρ))) * Real.log (partitionFn (β / (1 - ρ)) E₂ S) =
      -(1 / β) * ((1 - ρ) * Real.log (partitionFn (β / (1 - ρ)) E₂ S)) := by
    field_simp
  rw [e1, e2]
  have hinv : 0 < 1 / β := by positivity
  nlinarith

end MetricChain
