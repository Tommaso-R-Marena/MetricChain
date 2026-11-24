import Mathlib
import proofs.Frontiers.TorsionRMSD
import proofs.Frontiers.EnvelopeDuality

/-!
# From SE(3)-invariance and a Lipschitz certificate to a torsion-space envelope

A learned residual is usable by the certificate kernels only through an envelope
(`EnvelopeDuality.lean`).  This file shows how an *equivariant architecture* produces one:

* if a residual `Δ` on configurations is invariant under rigid motions and `Λ`-Lipschitz for the
  `ℓ²` configuration distance, then `|Δ x - Δ y| ≤ Λ · c` whenever `x` and `y` can be superposed
  within `c` (`invariant_lipschitz_of_rigidWithin`): the superposition distance — not the raw
  coordinate distance — controls the residual;
* consequently a single torsion move by `δ` changes the residual by at most
  `Λ · 2 √(2 I_red) |sin(δ/2)|`, with `I_red` the reduced moment of inertia of the internal
  rotation (`residual_torsion_move`), and a sequence of torsion moves by the sum of these
  (`residual_torsion_chain`).

These are exactly the per-torsion bounded-difference constants `c_k = Λ · 2 √(2 Ī_k)` required by
`ResidualClass` in `CertificateAlgebra.lean`.
-/

namespace MetricChain

open Finset

variable {P : Type*} [PseudoMetricSpace P] {ι : Type*} [Fintype ι]

/-- The residual is invariant under every rigid motion of the ambient space. -/
def RigidInvariant (Δ : (ι → P) → ℝ) : Prop :=
  ∀ (g : P ≃ᵢ P) (y : ι → P), Δ (fun i => g (y i)) = Δ y

/-- The residual is `Λ`-Lipschitz for the `ℓ²` distance between configurations. -/
def ConfigLipschitz (Λ : ℝ) (Δ : (ι → P) → ℝ) : Prop :=
  ∀ x y : ι → P, |Δ x - Δ y| ≤ Λ * Real.sqrt (∑ i, dist (x i) (y i) ^ 2)

/-- **Invariance upgrades a Lipschitz certificate to the superposition distance.** -/
theorem invariant_lipschitz_of_rigidWithin {Δ : (ι → P) → ℝ} {Λ : ℝ} (hΛ : 0 ≤ Λ)
    (hinv : RigidInvariant Δ) (hlip : ConfigLipschitz Λ Δ) {x y : ι → P} {c : ℝ} (hc : 0 ≤ c)
    (h : RigidWithin x y c) : |Δ x - Δ y| ≤ Λ * c := by
  obtain ⟨g, hg⟩ := h
  have h1 := hlip x (fun i => g (y i))
  rw [hinv g y] at h1
  have h2 : Real.sqrt (∑ i, dist (x i) (g (y i)) ^ 2) ≤ c := by
    calc Real.sqrt (∑ i, dist (x i) (g (y i)) ^ 2) ≤ Real.sqrt (c ^ 2) := Real.sqrt_le_sqrt hg
      _ = c := Real.sqrt_sq hc
  calc |Δ x - Δ y| ≤ Λ * Real.sqrt (∑ i, dist (x i) (g (y i)) ^ 2) := h1
    _ ≤ Λ * c := mul_le_mul_of_nonneg_left h2 hΛ

variable [DecidableEq ι]

/-- **Bounded difference of an invariant Lipschitz residual under one torsion move.** -/
theorem residual_torsion_move {Δ : (ι → P) → ℝ} {Λ : ℝ} (hΛ : 0 ≤ Λ) (hinv : RigidInvariant Δ)
    (hlip : ConfigLipschitz Λ Δ) {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ} {X Y : ι → P}
    (h : IsTorsionMove u B δ X Y) :
    |Δ X - Δ Y| ≤ Λ * (2 * Real.sqrt (2 * reducedInertia u B X) * |Real.sin (δ / 2)|) :=
  invariant_lipschitz_of_rigidWithin hΛ hinv hlip (by positivity) h.rigidWithin

/-- **Torsion-space envelope of an invariant Lipschitz residual along a path of torsion moves.** -/
theorem residual_torsion_chain {Δ : (ι → P) → ℝ} {Λ : ℝ} (hΛ : 0 ≤ Λ) (hinv : RigidInvariant Δ)
    (hlip : ConfigLipschitz Λ Δ) (X : ℕ → ι → P) (u : ℕ → P ≃ᵢ AxisSpace) (B : ℕ → Finset ι)
    (δ : ℕ → ℝ) (m : ℕ) (h : ∀ k < m, IsTorsionMove (u k) (B k) (δ k) (X k) (X (k + 1))) :
    |Δ (X 0) - Δ (X m)| ≤
      Λ * ∑ k ∈ range m, 2 * Real.sqrt (2 * reducedInertia (u k) (B k) (X k)) *
        |Real.sin (δ k / 2)| :=
  invariant_lipschitz_of_rigidWithin hΛ hinv hlip (Finset.sum_nonneg fun _ _ => by positivity)
    (rigidWithin_torsion_chain X u B δ m h)

end MetricChain
