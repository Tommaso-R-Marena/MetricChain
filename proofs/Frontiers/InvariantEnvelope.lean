import Mathlib
import proofs.Frontiers.TorsionRMSD
import proofs.Frontiers.EnvelopeDuality
import proofs.CertificateAlgebra

/-!
# From rigid-motion invariance and a Lipschitz certificate to a torsion-space envelope

A learned residual is usable by the certificate kernels only through an envelope
(`EnvelopeDuality.lean`).  This file shows how an *invariant architecture* produces one.

Invariance is parametrised by a submonoid `G` of isometries of the ambient space
(`RigidInvariantIn G`).  Taking `G` to be the proper rigid motions gives `SE(3)`-invariance, which
leaves room for chirality-sensitive residuals; `RigidInvariant` is the special case of the full
isometry group (`E(3)`: reflections included).

* if a residual `Δ` on configurations is `G`-invariant and `Λ`-Lipschitz for the `ℓ²`
  configuration distance, then `|Δ x - Δ y| ≤ Λ · c` whenever `x` and `y` can be superposed within
  `c` by a motion of `G` (`invariant_lipschitz_of_rigidWithinIn`): the superposition distance —
  not the raw coordinate distance — controls the residual;
* consequently a single torsion move by `δ` changes the residual by at most
  `Λ · 2 √(2 I_red) |sin(δ/2)|`, with `I_red` the reduced moment of inertia of the internal
  rotation at the current configuration, provided `G` contains the rotations about the torsion
  axis (`residual_torsion_move_in`; automatically true for the full isometry group,
  `residual_torsion_move`; sharper `min`-inertia form `residual_torsion_move_min_in`), and a
  sequence of torsion moves by the sum of these (`residual_torsion_chain_in`,
  `residual_torsion_chain`);
* with a configuration-independent bound `Ibar` on the reduced inertia the constant becomes the
  uniform `c = Λ · 2 √(2 Ibar)` (`residual_torsion_move_uniform`), and
  `residualLowerClass_of_invariant_lipschitz` packages this as membership of `Δ ∘ emb` in the
  residual class of the certificate kernel, so that `verifyR_sound_invariant` certifies
  `L ≤ E + Δ ∘ emb` on the box; `residualIntervalClass_of_rigidWithinIn` and
  `verifyITop_sound_invariant` are the versions for interval anchor data and the top-level
  kernel.
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

/-- The residual is invariant under every motion of the submonoid `G` of isometries (for the
proper rigid motions: `SE(3)`-invariance, compatible with chirality-sensitive residuals). -/
def RigidInvariantIn (G : Submonoid (P ≃ᵢ P)) (Δ : (ι → P) → ℝ) : Prop :=
  ∀ g ∈ G, ∀ y : ι → P, Δ (fun i => g (y i)) = Δ y

omit [Fintype ι] in
/-- Invariance under all isometries implies invariance under any subgroup. -/
theorem RigidInvariant.rigidInvariantIn {Δ : (ι → P) → ℝ} (h : RigidInvariant Δ)
    (G : Submonoid (P ≃ᵢ P)) : RigidInvariantIn G Δ :=
  fun g _ y => h g y

omit [Fintype ι] in
/-- `RigidInvariant` is `RigidInvariantIn` for the full isometry group. -/
theorem rigidInvariantIn_top {Δ : (ι → P) → ℝ} :
    RigidInvariantIn (⊤ : Submonoid (P ≃ᵢ P)) Δ ↔ RigidInvariant Δ :=
  ⟨fun h g y => h g (Submonoid.mem_top g) y, fun h => h.rigidInvariantIn ⊤⟩

/-- **`G`-invariance upgrades a Lipschitz certificate to the `G`-superposition distance.** -/
theorem invariant_lipschitz_of_rigidWithinIn {G : Submonoid (P ≃ᵢ P)} {Δ : (ι → P) → ℝ} {Λ : ℝ}
    (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ) (hlip : ConfigLipschitz Λ Δ) {x y : ι → P}
    {c : ℝ} (hc : 0 ≤ c) (h : RigidWithinIn G x y c) : |Δ x - Δ y| ≤ Λ * c := by
  obtain ⟨g, hgG, hg⟩ := h
  have h1 := hlip x (fun i => g (y i))
  rw [hinv g hgG y] at h1
  have h2 : Real.sqrt (∑ i, dist (x i) (g (y i)) ^ 2) ≤ c := by
    calc Real.sqrt (∑ i, dist (x i) (g (y i)) ^ 2) ≤ Real.sqrt (c ^ 2) := Real.sqrt_le_sqrt hg
      _ = c := Real.sqrt_sq hc
  calc |Δ x - Δ y| ≤ Λ * Real.sqrt (∑ i, dist (x i) (g (y i)) ^ 2) := h1
    _ ≤ Λ * c := mul_le_mul_of_nonneg_left h2 hΛ

variable [DecidableEq ι]

/-- **Bounded difference under one torsion move, `G`-invariant residuals.**  `G` must contain the
rotations about the torsion axis (true for the proper rigid motions). -/
theorem residual_torsion_move_in {G : Submonoid (P ≃ᵢ P)} {Δ : (ι → P) → ℝ} {Λ : ℝ} (hΛ : 0 ≤ Λ)
    (hinv : RigidInvariantIn G Δ) (hlip : ConfigLipschitz Λ Δ) {u : P ≃ᵢ AxisSpace}
    {B : Finset ι} {δ : ℝ} {X Y : ι → P}
    (hG : ∀ ψ : ℝ, u.trans ((axisRot ψ).trans u.symm) ∈ G) (h : IsTorsionMove u B δ X Y) :
    |Δ X - Δ Y| ≤ Λ * (2 * Real.sqrt (2 * reducedInertia u B X) * |Real.sin (δ / 2)|) :=
  invariant_lipschitz_of_rigidWithinIn hΛ hinv hlip (by positivity) (h.rigidWithinIn G hG)

/-- **Bounded difference under one torsion move, `min`-inertia form** (never worse than the
reduced-inertia form): `Λ · 2 √(min(I_A, I_B)) |sin(δ/2)|`. -/
theorem residual_torsion_move_min_in {G : Submonoid (P ≃ᵢ P)} {Δ : (ι → P) → ℝ} {Λ : ℝ}
    (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ) (hlip : ConfigLipschitz Λ Δ)
    {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ} {X Y : ι → P}
    (hG : ∀ ψ : ℝ, u.trans ((axisRot ψ).trans u.symm) ∈ G) (h : IsTorsionMove u B δ X Y) :
    |Δ X - Δ Y| ≤
      Λ * (2 * Real.sqrt (min (axialInertia u Bᶜ X) (axialInertia u B X)) *
        |Real.sin (δ / 2)|) :=
  invariant_lipschitz_of_rigidWithinIn hΛ hinv hlip (by positivity) (h.rigidWithinIn_min G hG)

/-- **Torsion-space envelope along a path of torsion moves, `G`-invariant residuals.** -/
theorem residual_torsion_chain_in {G : Submonoid (P ≃ᵢ P)} {Δ : (ι → P) → ℝ} {Λ : ℝ}
    (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ) (hlip : ConfigLipschitz Λ Δ) (X : ℕ → ι → P)
    (u : ℕ → P ≃ᵢ AxisSpace) (B : ℕ → Finset ι) (δ : ℕ → ℝ) (m : ℕ)
    (hG : ∀ k < m, ∀ ψ : ℝ, (u k).trans ((axisRot ψ).trans (u k).symm) ∈ G)
    (h : ∀ k < m, IsTorsionMove (u k) (B k) (δ k) (X k) (X (k + 1))) :
    |Δ (X 0) - Δ (X m)| ≤
      Λ * ∑ k ∈ range m, 2 * Real.sqrt (2 * reducedInertia (u k) (B k) (X k)) *
        |Real.sin (δ k / 2)| :=
  invariant_lipschitz_of_rigidWithinIn hΛ hinv hlip (Finset.sum_nonneg fun _ _ => by positivity)
    (rigidWithinIn_torsion_chain G X u B δ m hG h)

/-- **Uniform bounded-difference constant.**  If the reduced moment of inertia of the torsion is
at most `Ibar` at the configuration `X`, then *any* change of that torsion angle changes the
residual by at most `Λ · 2 √(2 Ibar)`, independently of the angle increment. -/
theorem residual_torsion_move_uniform {G : Submonoid (P ≃ᵢ P)} {Δ : (ι → P) → ℝ} {Λ : ℝ}
    (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ) (hlip : ConfigLipschitz Λ Δ)
    {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ} {X Y : ι → P}
    (hG : ∀ ψ : ℝ, u.trans ((axisRot ψ).trans u.symm) ∈ G) (h : IsTorsionMove u B δ X Y)
    {Ibar : ℝ} (hI : reducedInertia u B X ≤ Ibar) :
    |Δ X - Δ Y| ≤ Λ * (2 * Real.sqrt (2 * Ibar)) := by
  have h1 := residual_torsion_move_in hΛ hinv hlip hG h
  have h2 : Real.sqrt (2 * reducedInertia u B X) ≤ Real.sqrt (2 * Ibar) :=
    Real.sqrt_le_sqrt (by linarith)
  have h3 : |Real.sin (δ / 2)| ≤ 1 := Real.abs_sin_le_one _
  have h4 : 0 ≤ Real.sqrt (2 * reducedInertia u B X) := Real.sqrt_nonneg _
  have h5 : 2 * Real.sqrt (2 * reducedInertia u B X) * |Real.sin (δ / 2)| ≤
      2 * Real.sqrt (2 * Ibar) := by
    nlinarith [abs_nonneg (Real.sin (δ / 2)), Real.sqrt_nonneg (2 * Ibar)]
  exact le_trans h1 (mul_le_mul_of_nonneg_left h5 hΛ)

omit [DecidableEq ι] in
/-- **From superposition radii to the residual class of the certificate kernel.**  Let `emb`
embed discrete states into configurations so that changing site `i` moves the configuration, up
to a motion of `G`, by at most `ρ i`.  If the published constants satisfy `Λ · ρ i ≤ c i` and the
published anchor values are lower bounds on the residual, then `Δ ∘ emb` belongs to
`ResidualLowerClass`.  (The torsion lemmas above supply `ρ i = 2 √(Ī_i)` with
`Ī_i ≥ min(I_A, I_B)`, or `2 √(2 Ī_i)` with `Ī_i ≥ I_red`.) -/
theorem residualLowerClass_of_rigidWithinIn {n k : ℕ} {G : Submonoid (P ≃ᵢ P)}
    {Δ : (ι → P) → ℝ} {Λ : ℝ} (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ)
    (hlip : ConfigLipschitz Λ Δ) (emb : Config n k → ι → P) (ρ : Fin n → ℝ) (hρ : ∀ i, 0 ≤ ρ i)
    (hmove : ∀ (x : Config n k) (i : Fin n) (s : Fin k),
      RigidWithinIn G (emb x) (emb (Function.update x i s)) (ρ i))
    (R : RProblem n k) (hc : ∀ i, Λ * ρ i ≤ (R.c i : ℝ))
    (hanch : ∀ p ∈ R.anchors, (p.2 : ℝ) ≤ Δ (emb p.1)) :
    ResidualLowerClass R (fun x => Δ (emb x)) := by
  refine ⟨fun x i s => ?_, hanch⟩
  have h1 := invariant_lipschitz_of_rigidWithinIn hΛ hinv hlip (hρ i) (hmove x i s)
  have h2 := neg_abs_le (Δ (emb x) - Δ (emb (Function.update x i s)))
  have h3 := hc i
  show Δ (emb (Function.update x i s)) - Δ (emb x) ≤ (R.c i : ℝ)
  linarith

/-- **From an invariant Lipschitz residual to the residual class of the certificate kernel.**
Let `emb` embed discrete torsion states into configurations in such a way that changing site `i`
is a torsion move (about some axis whose rotations lie in `G`) with reduced inertia at most
`Ibar i`.  If the published constants satisfy `Λ · 2 √(2 Ibar i) ≤ c i` (rounded up) and the
published anchor values are lower bounds on the residual (rounded down), then `Δ ∘ emb` belongs
to `ResidualLowerClass`. -/
theorem residualLowerClass_of_invariant_lipschitz {n k : ℕ} {G : Submonoid (P ≃ᵢ P)}
    {Δ : (ι → P) → ℝ} {Λ : ℝ} (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ)
    (hlip : ConfigLipschitz Λ Δ) (emb : Config n k → ι → P) (Ibar : Fin n → ℝ)
    (hmove : ∀ (x : Config n k) (i : Fin n) (s : Fin k),
      ∃ (u : P ≃ᵢ AxisSpace) (B : Finset ι) (δ : ℝ),
        (∀ ψ : ℝ, u.trans ((axisRot ψ).trans u.symm) ∈ G) ∧
          IsTorsionMove u B δ (emb x) (emb (Function.update x i s)) ∧
            reducedInertia u B (emb x) ≤ Ibar i)
    (R : RProblem n k) (hc : ∀ i, Λ * (2 * Real.sqrt (2 * Ibar i)) ≤ (R.c i : ℝ))
    (hanch : ∀ p ∈ R.anchors, (p.2 : ℝ) ≤ Δ (emb p.1)) :
    ResidualLowerClass R (fun x => Δ (emb x)) := by
  refine ⟨fun x i s => ?_, hanch⟩
  obtain ⟨u, B, δ, hG, hmv, hI⟩ := hmove x i s
  have h1 := residual_torsion_move_uniform hΛ hinv hlip hG hmv hI
  have h2 := neg_abs_le (Δ (emb x) - Δ (emb (Function.update x i s)))
  have h3 := hc i
  show Δ (emb (Function.update x i s)) - Δ (emb x) ≤ (R.c i : ℝ)
  linarith

/-- **Certified bound for a pairwise energy plus an invariant Lipschitz residual.**  Under the
hypotheses of `residualLowerClass_of_invariant_lipschitz`, an accepted residual certificate bounds
the full energy `E + Δ ∘ emb` on the box. -/
theorem verifyR_sound_invariant {n k : ℕ} {G : Submonoid (P ≃ᵢ P)} {Δ : (ι → P) → ℝ} {Λ : ℝ}
    (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ) (hlip : ConfigLipschitz Λ Δ)
    (emb : Config n k → ι → P) (Ibar : Fin n → ℝ)
    (hmove : ∀ (x : Config n k) (i : Fin n) (s : Fin k),
      ∃ (u : P ≃ᵢ AxisSpace) (B : Finset ι) (δ : ℝ),
        (∀ ψ : ℝ, u.trans ((axisRot ψ).trans u.symm) ∈ G) ∧
          IsTorsionMove u B δ (emb x) (emb (Function.update x i s)) ∧
            reducedInertia u B (emb x) ≤ Ibar i)
    (R : RProblem n k) (hc : ∀ i, Λ * (2 * Real.sqrt (2 * Ibar i)) ≤ (R.c i : ℝ))
    (hanch : ∀ p ∈ R.anchors, (p.2 : ℝ) ≤ Δ (emb p.1)) (c : RCert n k) (D : Dom n k) (L : ℚ)
    (hv : verifyR c R D L = true) (x : Config n k) (hx : InBox D x) :
    (L : ℝ) ≤ (R.base.energy x : ℝ) + Δ (emb x) :=
  verifyR_sound_lower c R D L hv _
    (residualLowerClass_of_invariant_lipschitz hΛ hinv hlip emb Ibar hmove R hc hanch) x hx

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

omit [DecidableEq ι] in
/-- **Interval form: membership in the class of the top-level residual kernel.**  As
`residualLowerClass_of_rigidWithinIn`, for interval anchor data: if the published intervals
contain the residual at the anchors, `Δ ∘ emb` belongs to `ResidualIntervalClass`. -/
theorem residualIntervalClass_of_rigidWithinIn {n k : ℕ} {G : Submonoid (P ≃ᵢ P)}
    {Δ : (ι → P) → ℝ} {Λ : ℝ} (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ)
    (hlip : ConfigLipschitz Λ Δ) (emb : Config n k → ι → P) (ρ : Fin n → ℝ) (hρ : ∀ i, 0 ≤ ρ i)
    (hmove : ∀ (x : Config n k) (i : Fin n) (s : Fin k),
      RigidWithinIn G (emb x) (emb (Function.update x i s)) (ρ i))
    (R : IProblem n k) (hc : ∀ i, Λ * ρ i ≤ (R.c i : ℝ))
    (hanch : ∀ p ∈ R.anchors, (p.lo : ℝ) ≤ Δ (emb p.x) ∧ ∀ h ∈ p.hi, Δ (emb p.x) ≤ (h : ℝ)) :
    ResidualIntervalClass R (fun x => Δ (emb x)) := by
  refine ⟨fun x i s => ?_, hanch⟩
  have h1 := invariant_lipschitz_of_rigidWithinIn hΛ hinv hlip (hρ i) (hmove x i s)
  have h2 := neg_abs_le (Δ (emb x) - Δ (emb (Function.update x i s)))
  have h3 := hc i
  show Δ (emb (Function.update x i s)) - Δ (emb x) ≤ (R.c i : ℝ)
  linarith

omit [DecidableEq ι] in
/-- **Certified two-sided statement for a pairwise energy plus an invariant Lipschitz residual,
through the top-level kernel.**  If `verifyITop` accepts interval data that contain the residual
at the anchors, then `L ≤ E + Δ ∘ emb` on the box, and at every anchor with an upper value the
true energy is at most `E + hi`. -/
theorem verifyITop_sound_invariant {n k : ℕ} {G : Submonoid (P ≃ᵢ P)} {Δ : (ι → P) → ℝ}
    {Λ : ℝ} (hΛ : 0 ≤ Λ) (hinv : RigidInvariantIn G Δ) (hlip : ConfigLipschitz Λ Δ)
    (emb : Config n k → ι → P) (ρ : Fin n → ℝ) (hρ : ∀ i, 0 ≤ ρ i)
    (hmove : ∀ (x : Config n k) (i : Fin n) (s : Fin k),
      RigidWithinIn G (emb x) (emb (Function.update x i s)) (ρ i))
    (R : IProblem n k) (hc : ∀ i, Λ * ρ i ≤ (R.c i : ℝ))
    (hanch : ∀ p ∈ R.anchors, (p.lo : ℝ) ≤ Δ (emb p.x) ∧ ∀ h ∈ p.hi, Δ (emb p.x) ≤ (h : ℝ))
    (c : RCert n k) (D : Dom n k) (L : ℚ) (hv : verifyITop c R D L = true) :
    (∀ x, InBox D x → (L : ℝ) ≤ (R.base.energy x : ℝ) + Δ (emb x)) ∧
      ∀ p ∈ R.anchors, ∀ h ∈ p.hi,
        (R.base.energy p.x : ℝ) + Δ (emb p.x) ≤ ((R.base.energy p.x + h : ℚ) : ℝ) :=
  (verifyITop_sound c R D L hv).2 _
    (residualIntervalClass_of_rigidWithinIn hΛ hinv hlip emb ρ hρ hmove R hc hanch)

end MetricChain
