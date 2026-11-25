/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# Robust ratios of macrostate weights (theory report §11.28)

For a finite configuration space with weights `w = e^{-f}`, an envelope `d` and residuals `g` that are admissible
(`g x - g y ≤ d x y`), the *observable* free energies are differences `-ln [Z_g(A)/Z_g(B)]` of two macrostates,
`Z_g(S) = ∑_{x ∈ S} w x · e^{-g x}`.  This file contains the certificate side of the theory:

* `macro_le_of_plan` — weak duality: a transport plan with gains from `B` to `A` certifies `Z_g(A) ≤ λ · Z_g(B)`
  for every residual that is admissible from `B` to `A` (only these constraints are used);
* `macro_single_le` — the plan for a single state (Theorem 11.12 in odds form);
* `macro_le_card_mul` — the plan "every state of `A` is served by one state of `B`": the upper half of the max–min sandwich;
* `cone_admissible`, `macro_cone_ge` — the cone around a state of `A`: the lower half of the sandwich;
* `closed_pair_within_A`, `closed_pair_within_B`, `closed_pair_cross` — a pair that is closed under the two extensions
  (lowest on `A` given `B`, highest on `B` given `A`) is admissible in all four directions: only the constraints from
  `B` to `A` matter.
-/
import Mathlib

namespace MetricChain.MacroRatio

open Finset

variable {X : Type*}

/-- **Weak duality for the robust ratio of two macrostates.**  If `ψ ≥ 0` on `B × A` ships to every `y ∈ A` at least its
weight and spends at every `z ∈ B`, with the gain `e^{d z y}` per unit shipped, at most `lam` times its weight, then
`Z_g(A) ≤ lam · Z_g(B)` for every residual with `g z - g y ≤ d z y` (`z ∈ B`, `y ∈ A`). -/
theorem macro_le_of_plan (A B : Finset X) (w g : X → ℝ) (d ψ : X → X → ℝ) (lam : ℝ)
    (hψ : ∀ z ∈ B, ∀ y ∈ A, 0 ≤ ψ z y)
    (hg : ∀ z ∈ B, ∀ y ∈ A, g z - g y ≤ d z y)
    (hcap : ∀ z ∈ B, ∑ y ∈ A, Real.exp (d z y) * ψ z y ≤ lam * w z)
    (hdem : ∀ y ∈ A, w y ≤ ∑ z ∈ B, ψ z y) :
    ∑ y ∈ A, w y * Real.exp (-g y) ≤ lam * ∑ z ∈ B, w z * Real.exp (-g z) := by
  calc ∑ y ∈ A, w y * Real.exp (-g y)
      ≤ ∑ y ∈ A, (∑ z ∈ B, ψ z y) * Real.exp (-g y) := by
        apply Finset.sum_le_sum
        intro y hy
        exact mul_le_mul_of_nonneg_right (hdem y hy) (Real.exp_pos _).le
    _ = ∑ z ∈ B, ∑ y ∈ A, ψ z y * Real.exp (-g y) := by
        simp_rw [Finset.sum_mul]
        exact Finset.sum_comm
    _ ≤ ∑ z ∈ B, ∑ y ∈ A, (Real.exp (d z y) * ψ z y) * Real.exp (-g z) := by
        apply Finset.sum_le_sum
        intro z hz
        apply Finset.sum_le_sum
        intro y hy
        have h1 : Real.exp (-g y) ≤ Real.exp (d z y) * Real.exp (-g z) := by
          rw [← Real.exp_add]
          apply Real.exp_le_exp.mpr
          linarith [hg z hz y hy]
        calc ψ z y * Real.exp (-g y) ≤ ψ z y * (Real.exp (d z y) * Real.exp (-g z)) :=
              mul_le_mul_of_nonneg_left h1 (hψ z hz y hy)
          _ = Real.exp (d z y) * ψ z y * Real.exp (-g z) := by ring
    _ = ∑ z ∈ B, (∑ y ∈ A, Real.exp (d z y) * ψ z y) * Real.exp (-g z) := by
        apply Finset.sum_congr rfl
        intro z _
        rw [Finset.sum_mul]
    _ ≤ ∑ z ∈ B, (lam * w z) * Real.exp (-g z) := by
        apply Finset.sum_le_sum
        intro z hz
        exact mul_le_mul_of_nonneg_right (hcap z hz) (Real.exp_pos _).le
    _ = lam * ∑ z ∈ B, w z * Real.exp (-g z) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro z _
        ring

/-- **One state against a macrostate** (Theorem 11.12 in odds form, for an arbitrary macrostate `B`): the weight of
`y₀` times `∑_{z ∈ B} w z e^{-d z y₀}` is at most `w y₀ · Z_g(B)/e^{-g y₀}`; division-free. -/
theorem macro_single_le (B : Finset X) (w g : X → ℝ) (d : X → X → ℝ) (y₀ : X)
    (hw : ∀ z ∈ B, 0 ≤ w z) (hg : ∀ z ∈ B, g z - g y₀ ≤ d z y₀) :
    Real.exp (-g y₀) * ∑ z ∈ B, w z * Real.exp (-d z y₀) ≤ ∑ z ∈ B, w z * Real.exp (-g z) := by
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro z hz
  have h1 : Real.exp (-g y₀) * Real.exp (-d z y₀) ≤ Real.exp (-g z) := by
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    linarith [hg z hz]
  calc Real.exp (-g y₀) * (w z * Real.exp (-d z y₀)) = w z * (Real.exp (-g y₀) * Real.exp (-d z y₀)) := by ring
    _ ≤ w z * Real.exp (-g z) := mul_le_mul_of_nonneg_left h1 (hw z hz)

/-- **Upper half of the max–min sandwich.**  If every `y ∈ A` has a source `z ∈ B` with `w y · e^{d z y} ≤ M · w z`, then
`Z_g(A) ≤ |A| · M · Z_g(B)`. -/
theorem macro_le_card_mul (A B : Finset X) (w g : X → ℝ) (d : X → X → ℝ) (M : ℝ)
    (hwA : ∀ y ∈ A, 0 ≤ w y) (hwB : ∀ z ∈ B, 0 ≤ w z) (hM : 0 ≤ M)
    (hg : ∀ z ∈ B, ∀ y ∈ A, g z - g y ≤ d z y)
    (hsrc : ∀ y ∈ A, ∃ z ∈ B, w y * Real.exp (d z y) ≤ M * w z) :
    ∑ y ∈ A, w y * Real.exp (-g y) ≤ (A.card : ℝ) * (M * ∑ z ∈ B, w z * Real.exp (-g z)) := by
  have hterm : ∀ y ∈ A, w y * Real.exp (-g y) ≤ M * ∑ z ∈ B, w z * Real.exp (-g z) := by
    intro y hy
    obtain ⟨z, hz, hzy⟩ := hsrc y hy
    have h1 : Real.exp (-g y) ≤ Real.exp (d z y) * Real.exp (-g z) := by
      rw [← Real.exp_add]
      apply Real.exp_le_exp.mpr
      linarith [hg z hz y hy]
    have h2 : w z * Real.exp (-g z) ≤ ∑ z' ∈ B, w z' * Real.exp (-g z') :=
      Finset.single_le_sum (f := fun z' => w z' * Real.exp (-g z'))
        (fun z' hz' => mul_nonneg (hwB z' hz') (Real.exp_pos _).le) hz
    calc w y * Real.exp (-g y) ≤ w y * (Real.exp (d z y) * Real.exp (-g z)) :=
          mul_le_mul_of_nonneg_left h1 (hwA y hy)
      _ = (w y * Real.exp (d z y)) * Real.exp (-g z) := by ring
      _ ≤ (M * w z) * Real.exp (-g z) := mul_le_mul_of_nonneg_right hzy (Real.exp_pos _).le
      _ = M * (w z * Real.exp (-g z)) := by ring
      _ ≤ M * ∑ z' ∈ B, w z' * Real.exp (-g z') := mul_le_mul_of_nonneg_left h2 hM
  calc ∑ y ∈ A, w y * Real.exp (-g y) ≤ ∑ _y ∈ A, M * ∑ z ∈ B, w z * Real.exp (-g z) :=
        Finset.sum_le_sum hterm
    _ = (A.card : ℝ) * (M * ∑ z ∈ B, w z * Real.exp (-g z)) := by
        rw [Finset.sum_const, nsmul_eq_mul]

/-- The cone around a state is an admissible residual (triangle inequality). -/
theorem cone_admissible (d : X → X → ℝ) (y₀ : X) (tri : ∀ a b c, d a c ≤ d a b + d b c) :
    ∀ x y, d x y₀ - d y y₀ ≤ d x y := by
  intro x y
  linarith [tri x y y₀]

/-- **Lower half of the max–min sandwich.**  For the cone `g = d · y₀` around a state `y₀ ∈ A`: if
`m · (w z · e^{-d z y₀}) ≤ w y₀` for every `z ∈ B`, then `m · Z_g(B) ≤ |B| · Z_g(A)`. -/
theorem macro_cone_ge (A B : Finset X) (w : X → ℝ) (d : X → X → ℝ) (y₀ : X) (m : ℝ)
    (hy₀ : y₀ ∈ A) (hd0 : d y₀ y₀ = 0) (hwA : ∀ y ∈ A, 0 ≤ w y)
    (hm : ∀ z ∈ B, m * (w z * Real.exp (-d z y₀)) ≤ w y₀) :
    m * ∑ z ∈ B, w z * Real.exp (-d z y₀) ≤ (B.card : ℝ) * ∑ y ∈ A, w y * Real.exp (-d y y₀) := by
  have h1 : w y₀ ≤ ∑ y ∈ A, w y * Real.exp (-d y y₀) := by
    have := Finset.single_le_sum (f := fun y => w y * Real.exp (-d y y₀))
      (fun y hy => mul_nonneg (hwA y hy) (Real.exp_pos _).le) hy₀
    simpa [hd0] using this
  calc m * ∑ z ∈ B, w z * Real.exp (-d z y₀) = ∑ z ∈ B, m * (w z * Real.exp (-d z y₀)) := by
        rw [Finset.mul_sum]
    _ ≤ ∑ _z ∈ B, w y₀ := Finset.sum_le_sum hm
    _ = (B.card : ℝ) * w y₀ := by rw [Finset.sum_const, nsmul_eq_mul]
    _ ≤ (B.card : ℝ) * ∑ y ∈ A, w y * Real.exp (-d y y₀) :=
        mul_le_mul_of_nonneg_left h1 (Nat.cast_nonneg _)

section ClosedPairs

variable (A B : Finset X) (g : X → ℝ) (d : X → X → ℝ)

/-- A pair that is closed under the lower extension to `A` is admissible inside `A`. -/
theorem closed_pair_within_A (tri : ∀ a b c, d a c ≤ d a b + d b c)
    (hBA : ∀ z ∈ B, ∀ y ∈ A, g z - g y ≤ d z y)
    (hlow : ∀ y ∈ A, ∃ z ∈ B, g y = g z - d z y) :
    ∀ y ∈ A, ∀ y' ∈ A, g y - g y' ≤ d y y' := by
  intro y hy y' hy'
  obtain ⟨z, hz, hzy⟩ := hlow y hy
  linarith [hBA z hz y' hy', tri z y y']

/-- A pair that is closed under the upper extension to `B` is admissible inside `B`. -/
theorem closed_pair_within_B (tri : ∀ a b c, d a c ≤ d a b + d b c)
    (hBA : ∀ z ∈ B, ∀ y ∈ A, g z - g y ≤ d z y)
    (hup : ∀ z ∈ B, ∃ y ∈ A, g z = g y + d z y) :
    ∀ z ∈ B, ∀ z' ∈ B, g z - g z' ≤ d z z' := by
  intro z hz z' hz'
  obtain ⟨y, hy, hzy⟩ := hup z' hz'
  linarith [hBA z hz y hy, tri z z' y]

/-- A closed pair is admissible from `A` to `B` as well: **only the constraints from `B` to `A` matter**. -/
theorem closed_pair_cross (tri : ∀ a b c, d a c ≤ d a b + d b c)
    (hBA : ∀ z ∈ B, ∀ y ∈ A, g z - g y ≤ d z y)
    (hlow : ∀ y ∈ A, ∃ z ∈ B, g y = g z - d z y)
    (hup : ∀ z ∈ B, ∃ y ∈ A, g z = g y + d z y) :
    ∀ y ∈ A, ∀ z ∈ B, g y - g z ≤ d y z := by
  intro y hy z hz
  obtain ⟨z', hz', hy_eq⟩ := hlow y hy
  obtain ⟨y', hy', hz_eq⟩ := hup z hz
  linarith [hBA z' hz' y' hy', tri z' y y', tri y z y']

end ClosedPairs

/-- Non-vacuity: two states at distance `c ≥ 0` with weights `1`; the plan `ψ = 1` certifies the ratio `e^c`, and the
residual `g = (c, 0)` attains it. -/
theorem two_point_witness (c : ℝ) :
    ∑ y ∈ ({true} : Finset Bool), (1 : ℝ) * Real.exp (-(fun b : Bool => if b then (0 : ℝ) else c) y)
      = Real.exp c * ∑ z ∈ ({false} : Finset Bool), (1 : ℝ) * Real.exp (-(fun b : Bool => if b then (0 : ℝ) else c) z) := by
  simp [← Real.exp_add]

end MetricChain.MacroRatio
