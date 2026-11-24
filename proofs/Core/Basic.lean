import Mathlib

/-!
# MetricChain — core definitions

Finite-state statistical mechanics vocabulary shared by the `Frontiers` modules.

* `partitionFn β E S` — the Boltzmann sum `∑_{x ∈ S} exp(-β E x)` over a finite set of
  configurations `S`.  A fixed-sequence heteropolymer with discretised (or voxelised) internal
  coordinates is a finite configuration space; continuous torsion boxes are handled by the
  interval layer in `Core/Rounding.lean`.
* `freeEnergy β E S = -(1/β) log (partitionFn β E S)`.

Everything here is elementary; the content of the project lives in `proofs/Frontiers`.
-/

namespace MetricChain

open Finset

variable {Ω : Type*}

/-- Boltzmann sum of the energy `E` over the finite configuration set `S` at inverse temperature `β`. -/
noncomputable def partitionFn (β : ℝ) (E : Ω → ℝ) (S : Finset Ω) : ℝ :=
  ∑ x ∈ S, Real.exp (-β * E x)

/-- Helmholtz free energy `-(1/β) log Z`. -/
noncomputable def freeEnergy (β : ℝ) (E : Ω → ℝ) (S : Finset Ω) : ℝ :=
  -(1 / β) * Real.log (partitionFn β E S)

theorem partitionFn_nonneg (β : ℝ) (E : Ω → ℝ) (S : Finset Ω) : 0 ≤ partitionFn β E S :=
  Finset.sum_nonneg fun _ _ => (Real.exp_pos _).le

theorem partitionFn_pos (β : ℝ) (E : Ω → ℝ) {S : Finset Ω} (hS : S.Nonempty) :
    0 < partitionFn β E S :=
  Finset.sum_pos (fun _ _ => Real.exp_pos _) hS

/-- The partition function is antitone in the energy (for `β ≥ 0`). -/
theorem partitionFn_anti {β : ℝ} (hβ : 0 ≤ β) {E E' : Ω → ℝ} (S : Finset Ω)
    (h : ∀ x ∈ S, E x ≤ E' x) : partitionFn β E' S ≤ partitionFn β E S := by
  unfold partitionFn
  refine Finset.sum_le_sum fun x hx => Real.exp_le_exp.mpr ?_
  have := mul_le_mul_of_nonneg_left (h x hx) hβ
  linarith

/-- The partition function is monotone in the configuration set. -/
theorem partitionFn_mono_set (β : ℝ) (E : Ω → ℝ) {S T : Finset Ω} (h : S ⊆ T) :
    partitionFn β E S ≤ partitionFn β E T :=
  Finset.sum_le_sum_of_subset_of_nonneg h fun _ _ _ => (Real.exp_pos _).le

theorem partitionFn_union [DecidableEq Ω] (β : ℝ) (E : Ω → ℝ) {S T : Finset Ω}
    (h : Disjoint S T) : partitionFn β E (S ∪ T) = partitionFn β E S + partitionFn β E T :=
  Finset.sum_union h

/-- Free energy is monotone in the energy function (for `β > 0`). -/
theorem freeEnergy_mono {β : ℝ} (hβ : 0 < β) {E E' : Ω → ℝ} {S : Finset Ω} (hS : S.Nonempty)
    (h : ∀ x ∈ S, E x ≤ E' x) : freeEnergy β E S ≤ freeEnergy β E' S := by
  unfold freeEnergy
  have h1 := partitionFn_anti hβ.le S h
  have h2 := Real.log_le_log (partitionFn_pos β E' hS) h1
  have h3 : 0 ≤ 1 / β := by positivity
  nlinarith

end MetricChain
