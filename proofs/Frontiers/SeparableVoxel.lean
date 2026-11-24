import Mathlib
import proofs.Core.Basic

/-!
# Separable voxel envelopes: an `M`-dimensional Boltzmann integral from `M` one-dimensional ones

`VoxelEnclosure.lean` bounds the integral of `exp(-β E)` over a voxel by `vol · exp(-β E_lo/hi)`
(zeroth order).  This file provides the next order in certificate form.  If on a product voxel
`∏ s i ⊂ ℝ^ι` the energy is bracketed by **separable** functions,

  `∑ i, φ i (x i) ≤ E x ≤ ∑ i, ψ i (x i)`,

then by Fubini

  `∏ i, ∫_{s i} exp(-β ψ i) ≤ ∫_{∏ s i} exp(-β E) ≤ ∏ i, ∫_{s i} exp(-β φ i)`.

A second-order Taylor expansion with a diagonal Hessian enclosure
`E(c) + g·u + (m/2)|u|² ≤ E(c + u) ≤ E(c) + g·u + (M/2)|u|²` is of this form
(`φ i (t) = E(c)/|ι| + g i (t - c i) + (m/2)(t - c i)²`), so the integral over an
`M`-dimensional voxel is certified by `M` one-dimensional Gaussian-type integrals, each of which
can in turn be enclosed by one-dimensional voxel sums (`voxel_riemann_enclosure`).  The cost of a
second-order certificate is therefore `M ×` (one-dimensional resolution) per voxel instead of an
`M`-dimensional refinement.
-/

namespace MetricChain

open MeasureTheory Finset

variable {ι : Type*} [Fintype ι]

/-- **Fubini on a box for product integrands.** -/
theorem setIntegral_pi_prod (s : ι → Set ℝ) (f : ι → ℝ → ℝ) :
    ∫ x in Set.univ.pi s, ∏ i, f i (x i) = ∏ i, ∫ t in s i, f i t := by
  rw [volume_pi, Measure.restrict_pi_pi, integral_fintype_prod_eq_prod]

/-- A product of functions that are integrable on the factors is integrable on the box. -/
theorem integrableOn_pi_prod (s : ι → Set ℝ) (f : ι → ℝ → ℝ)
    (hf : ∀ i, IntegrableOn (f i) (s i)) :
    IntegrableOn (fun x : ι → ℝ => ∏ i, f i (x i)) (Set.univ.pi s) := by
  unfold IntegrableOn
  rw [volume_pi, Measure.restrict_pi_pi]
  exact Integrable.fintype_prod hf

/-- **Separable voxel envelope.**  Separable lower and upper envelopes of the energy on a product
voxel give two-sided bounds on the Boltzmann integral as products of one-dimensional integrals. -/
theorem separable_voxel_bounds (s : ι → Set ℝ) (hs : ∀ i, MeasurableSet (s i))
    (E : (ι → ℝ) → ℝ) (φ ψ : ι → ℝ → ℝ) {β : ℝ} (hβ : 0 ≤ β)
    (hlo : ∀ x ∈ Set.univ.pi s, ∑ i, φ i (x i) ≤ E x)
    (hhi : ∀ x ∈ Set.univ.pi s, E x ≤ ∑ i, ψ i (x i))
    (hint : IntegrableOn (fun x => Real.exp (-β * E x)) (Set.univ.pi s))
    (hφ : ∀ i, IntegrableOn (fun t => Real.exp (-β * φ i t)) (s i))
    (hψ : ∀ i, IntegrableOn (fun t => Real.exp (-β * ψ i t)) (s i)) :
    ∏ i, ∫ t in s i, Real.exp (-β * ψ i t) ≤ ∫ x in Set.univ.pi s, Real.exp (-β * E x) ∧
      ∫ x in Set.univ.pi s, Real.exp (-β * E x) ≤ ∏ i, ∫ t in s i, Real.exp (-β * φ i t) := by
  have hbox : MeasurableSet (Set.univ.pi s) := MeasurableSet.univ_pi hs
  have hexp : ∀ (χ : ι → ℝ → ℝ) (x : ι → ℝ),
      Real.exp (-β * ∑ i, χ i (x i)) = ∏ i, Real.exp (-β * χ i (x i)) := by
    intro χ x
    rw [Finset.mul_sum, Real.exp_sum]
  constructor
  · rw [← setIntegral_pi_prod s (fun i t => Real.exp (-β * ψ i t))]
    apply setIntegral_mono_on (integrableOn_pi_prod s _ hψ) hint hbox
    intro x hx
    rw [← hexp ψ x]
    apply Real.exp_le_exp.mpr
    have := mul_le_mul_of_nonneg_left (hhi x hx) hβ
    linarith
  · rw [← setIntegral_pi_prod s (fun i t => Real.exp (-β * φ i t))]
    apply setIntegral_mono_on hint (integrableOn_pi_prod s _ hφ) hbox
    intro x hx
    rw [← hexp φ x]
    apply Real.exp_le_exp.mpr
    have := mul_le_mul_of_nonneg_left (hlo x hx) hβ
    linarith

/-- **Relative width of the separable enclosure.**  If the two envelopes differ by at most `w i`
on the `i`-th factor, the upper product bound exceeds the lower one by at most the factor
`exp (β ∑ i, w i)`: for second-order envelopes `w i = (M - m)·(half-width i)²/2`, so the
enclosure is second order in the voxel size. -/
theorem separable_voxel_ratio (s : ι → Set ℝ) (hs : ∀ i, MeasurableSet (s i))
    (φ ψ : ι → ℝ → ℝ) (w : ι → ℝ) {β : ℝ} (hβ : 0 ≤ β)
    (hw : ∀ i, ∀ t ∈ s i, ψ i t ≤ φ i t + w i)
    (hφ : ∀ i, IntegrableOn (fun t => Real.exp (-β * φ i t)) (s i))
    (hψ : ∀ i, IntegrableOn (fun t => Real.exp (-β * ψ i t)) (s i)) :
    ∏ i, ∫ t in s i, Real.exp (-β * φ i t) ≤
      Real.exp (β * ∑ i, w i) * ∏ i, ∫ t in s i, Real.exp (-β * ψ i t) := by
  rw [Finset.mul_sum, Real.exp_sum, ← Finset.prod_mul_distrib]
  apply Finset.prod_le_prod
  · intro i _
    exact setIntegral_nonneg (hs i) fun t _ => (Real.exp_pos _).le
  · intro i _
    rw [← integral_const_mul]
    apply setIntegral_mono_on (hφ i) ((hψ i).const_mul _) (hs i)
    intro t ht
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    have := mul_le_mul_of_nonneg_left (hw i t ht) hβ
    linarith

end MetricChain
