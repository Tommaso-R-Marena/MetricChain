import Mathlib
import proofs.Frontiers.SoftGapBounds

/-!
# The spot-check constant does not depend on the residual

Found by an independent workstream (`docs/workstreams/G_REPORT.md`, Lemmas G9a, G9b) and checked
by its reviewer (`docs/reviews/R_G_review.md`).

The number of samples of the soft-gap sampler of `SoftGapBounds.lean`
(`thermal_spotCheck_correct`, `sum_dipWeight_eq`) is governed by `E_π[exp Λ]`.  This quantity is
the same for **every** residual:

  `E_π[exp Λ] = ∑_y exp (-β f y) / ∑_a exp (-β (f a + d a y))`

(`gibbs_mul_exp_softGap`, `sum_gibbs_exp_softGap_indep`, `sum_dipWeight_indep`): it is a property
of the known part and the envelope alone, so it can be computed before any evaluation, and the
upper bound of theory report Theorem 11.26 is uniform over the instances of a class.
`spotCheck_const_le_cover` bounds it by a metric entropy: if the space is partitioned into cells
of envelope diameter at most `r`, it is at most `exp (β r)` times the number of cells.
-/

namespace MetricChain

open Finset

variable {X : Type*} [Fintype X] [Nonempty X]

/-- Gibbs weight times `exp` of the soft gap: the residual enters only through `Z`. -/
theorem gibbs_mul_exp_softGap (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (y : X) :
    Real.exp (-β * (f y + g y)) * Real.exp (softGap β d f g y) =
      (∑ x, Real.exp (-β * (f x + g x))) *
        (Real.exp (-β * f y) / ∑ a, Real.exp (-β * (f a + d a y))) := by
  have hT : 0 < ∑ a, Real.exp (-β * (f a + d a y)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hT' : (∑ a, Real.exp (-β * (f a + d a y))) ≠ 0 := hT.ne'
  have hS : ∑ x, Real.exp (-β * (f x + g x + slack d g x y)) =
      Real.exp (-β * g y) * ∑ a, Real.exp (-β * (f a + d a y)) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [← Real.exp_add]
    congr 1
    unfold slack
    ring
  have h := exp_softGap_mul β d f g y
  rw [hS] at h
  have hg : Real.exp (-β * (f y + g y)) = Real.exp (-β * f y) * Real.exp (-β * g y) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [hg, ← h]
  field_simp

/-- **The spot-check exponent is the same for every residual**:
`E_π[exp Λ] = ∑_y exp (-β f y) / ∑_a exp (-β (f a + d a y))`. -/
theorem sum_gibbs_exp_softGap_indep (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) :
    (∑ y, Real.exp (-β * (f y + g y)) * Real.exp (softGap β d f g y)) /
        (∑ x, Real.exp (-β * (f x + g x))) =
      ∑ y, Real.exp (-β * f y) / ∑ a, Real.exp (-β * (f a + d a y)) := by
  have hZ : 0 < ∑ x, Real.exp (-β * (f x + g x)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  rw [div_eq_iff hZ.ne']
  rw [Finset.sum_congr rfl fun y _ => gibbs_mul_exp_softGap β d f g y]
  rw [← Finset.mul_sum]
  exact mul_comm _ _

/-- Total dip weight of the thermal sampler, with the residual-free constant. -/
theorem sum_dipWeight_indep (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (η : ℝ) :
    ∑ z, dipWeight β d f g η z =
      (∑ x, Real.exp (-β * (f x + g x))) *
        ((1 + η) * (∑ y, Real.exp (-β * f y) / ∑ a, Real.exp (-β * (f a + d a y))) - 1) := by
  rw [sum_dipWeight_eq]
  rw [Finset.sum_congr rfl fun y _ => gibbs_mul_exp_softGap β d f g y]
  rw [← Finset.mul_sum]
  ring

/-- **Metric-entropy bound for the spot-check constant.**  If the space is partitioned into cells
(`c : X → J`) such that `d a y ≤ r` inside every cell, then
`∑_y exp (-β f y) / ∑_a exp (-β (f a + d a y)) ≤ exp (β r) · |J|`. -/
theorem spotCheck_const_le_cover {J : Type*} [Fintype J] [DecidableEq J] (β : ℝ) (hβ : 0 ≤ β)
    (d : X → X → ℝ) (f : X → ℝ) (c : X → J) (r : ℝ)
    (hc : ∀ a y, c a = c y → d a y ≤ r) :
    ∑ y, Real.exp (-β * f y) / ∑ a, Real.exp (-β * (f a + d a y)) ≤
      Real.exp (β * r) * (Fintype.card J : ℝ) := by
  classical
  -- weight of the cell `j`
  let W : J → ℝ := fun j => ∑ a ∈ univ.filter (fun a => c a = j), Real.exp (-β * f a)
  have hWdef : ∀ j, W j = ∑ a ∈ univ.filter (fun a => c a = j), Real.exp (-β * f a) := fun _ => rfl
  have key : ∀ y, Real.exp (-β * f y) / ∑ a, Real.exp (-β * (f a + d a y)) ≤
      Real.exp (β * r) * (Real.exp (-β * f y) / W (c y)) := by
    intro y
    have hWpos : 0 < W (c y) := by
      rw [hWdef]
      refine Finset.sum_pos (fun _ _ => Real.exp_pos _) ⟨y, ?_⟩
      simp
    have hT : 0 < ∑ a, Real.exp (-β * (f a + d a y)) :=
      Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
    have hden : Real.exp (-(β * r)) * W (c y) ≤ ∑ a, Real.exp (-β * (f a + d a y)) := by
      rw [hWdef, Finset.mul_sum]
      calc ∑ a ∈ univ.filter (fun a => c a = c y), Real.exp (-(β * r)) * Real.exp (-β * f a)
          ≤ ∑ a ∈ univ.filter (fun a => c a = c y), Real.exp (-β * (f a + d a y)) := by
            refine Finset.sum_le_sum fun a ha => ?_
            rw [← Real.exp_add]
            apply Real.exp_le_exp.mpr
            have h1 : d a y ≤ r := hc a y (Finset.mem_filter.mp ha).2
            have h2 : β * d a y ≤ β * r := mul_le_mul_of_nonneg_left h1 hβ
            linarith
        _ ≤ ∑ a, Real.exp (-β * (f a + d a y)) := by
            refine Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _) ?_
            intro a _ _
            exact (Real.exp_pos _).le
    have hpos : 0 < Real.exp (-β * f y) := Real.exp_pos _
    -- 1 / T ≤ exp (β r) / W
    have hinv : 1 / (∑ a, Real.exp (-β * (f a + d a y))) ≤ Real.exp (β * r) / W (c y) := by
      rw [div_le_div_iff₀ hT hWpos]
      have h3 : Real.exp (β * r) * (Real.exp (-(β * r)) * W (c y)) = W (c y) := by
        rw [← mul_assoc, ← Real.exp_add]
        simp
      nlinarith [mul_le_mul_of_nonneg_left hden (Real.exp_pos (β * r)).le]
    calc Real.exp (-β * f y) / ∑ a, Real.exp (-β * (f a + d a y))
        = Real.exp (-β * f y) * (1 / ∑ a, Real.exp (-β * (f a + d a y))) := by ring
      _ ≤ Real.exp (-β * f y) * (Real.exp (β * r) / W (c y)) :=
          mul_le_mul_of_nonneg_left hinv hpos.le
      _ = Real.exp (β * r) * (Real.exp (-β * f y) / W (c y)) := by ring
  have hfib : ∀ j : J,
      ∑ y ∈ univ.filter (fun y => c y = j), Real.exp (-β * f y) / W (c y) ≤ 1 := by
    intro j
    have h1 : ∑ y ∈ univ.filter (fun y => c y = j), Real.exp (-β * f y) / W (c y) =
        ∑ y ∈ univ.filter (fun y => c y = j), Real.exp (-β * f y) / W j := by
      refine Finset.sum_congr rfl fun y hy => ?_
      rw [(Finset.mem_filter.mp hy).2]
    rw [h1, ← Finset.sum_div, hWdef]
    exact div_self_le_one _
  calc ∑ y, Real.exp (-β * f y) / ∑ a, Real.exp (-β * (f a + d a y))
      ≤ ∑ y, Real.exp (β * r) * (Real.exp (-β * f y) / W (c y)) :=
        Finset.sum_le_sum fun y _ => key y
    _ = Real.exp (β * r) * ∑ y, Real.exp (-β * f y) / W (c y) := by rw [Finset.mul_sum]
    _ = Real.exp (β * r) *
          ∑ j, ∑ y ∈ univ.filter (fun y => c y = j), Real.exp (-β * f y) / W (c y) := by
        rw [Finset.sum_fiberwise]
    _ ≤ Real.exp (β * r) * ∑ _j : J, (1 : ℝ) := by
        refine mul_le_mul_of_nonneg_left (Finset.sum_le_sum fun j _ => hfib j) (Real.exp_pos _).le
    _ = Real.exp (β * r) * (Fintype.card J : ℝ) := by simp

end MetricChain
