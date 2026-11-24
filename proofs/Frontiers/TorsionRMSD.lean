import Mathlib

/-!
# Torsion-to-RMSD propagation via reduced moments of inertia

How far (in rigid-superposition `ℓ²` distance, i.e. `√N · RMSD`) can a sequence of single-torsion
moves carry an articulated chain?  This file gives a machine-checked answer in three layers.

## T1 — the rigid-superposition pseudo-metric (`RigidWithin`)

For configurations `x y : ι → P` of `ι`-labelled atoms in a pseudo-metric space `P`,

* `RigidWithin x y c` means `∃ g : P ≃ᵢ P, ∑ i, dist (x i) (g (y i)) ^ 2 ≤ c ^ 2`;
* `rigidWithin_refl`, `RigidWithin.symm`, `RigidWithin.mono`;
* `RigidWithin.trans` — triangle inequality (Minkowski in `ℓ²` + isometry invariance);
* `rigidWithin_chain` — along a path of configurations the costs add up;
* `rigidWithin_map_iff` — independence of the isometric chart of the ambient space;
* `RigidWithin.exists_rmsd_le` — translation into an honest RMSD bound `c / √N`.

`RigidWithinIn G` is the same notion with the superposing motion restricted to a submonoid `G` of
isometries (for instance the proper, chirality-preserving motions).  Reflexivity, the triangle
inequality and the chain rule are proved in that generality (`rigidWithinIn_refl`,
`RigidWithinIn.trans`, `rigidWithinIn_chain`); `RigidWithin` is the case `G = ⊤`
(`rigidWithinIn_top`).

## T2 — exact coaxial cost of one torsion move

In coordinates adapted to the torsion axis only the components perpendicular to the axis matter;
the perpendicular plane is identified with `ℂ`.  With static atoms `a : ιA → ℂ`, rotated atoms
`b : ιB → ℂ`, axial moments of inertia `I_A = ∑ ‖a i‖²`, `I_B = ∑ ‖b j‖²` and `S = I_A + I_B`:

* `coaxial_cost_eq` — the cost of the superposition by the angle `ψ` about the axis is
  `2 I_A (1 - cos ψ) + 2 I_B (1 - cos (φ - ψ))`;
* `exists_coaxial_angle` / `coaxial_cost_ge` — its minimum over `ψ` is attained and equals
  `2 S - 2 √(S² - 4 I_A I_B sin²(φ/2))`;
* `coaxial_cost_le_reduced` — this is at most `8 (I_A I_B / S) sin²(φ/2)` (reduced moment of
  inertia), sharp for `I_A = I_B`, `φ = π`;
* `reduced_le_coaxial_cost`, `coaxial_cost_le_min`, `min_inertia_le_two_reduced` — the sharper
  two-sided bounds `4 (I_A I_B / S) sin²(φ/2) ≤ … ≤ 4 min(I_A, I_B) sin²(φ/2)`, the right-hand
  side being at most `8 (I_A I_B / S) sin²(φ/2)`;
* `exists_coaxial_superposition` — the combined statement for finite families.

## T3 — packaging in the model space and the chain rule for torsion moves

* `AxisSpace = WithLp 2 (ℂ × ℝ)` is Euclidean 3-space in axis-adapted coordinates and
  `axisRot ψ : AxisSpace ≃ᵢ AxisSpace` is the rotation `(w, z) ↦ (e^{iψ} w, z)`;
* `rigidWithin_axis_torsion` — the configuration with the `B`-atoms rotated by `φ` is
  `RigidWithin` the original one at `c = √(8 (I_A I_B / S) sin²(φ/2))`;
* `IsTorsionMove u B δ X Y` — in the isometric chart `u : P ≃ᵢ AxisSpace` the atoms of `B` are
  rotated by `δ` about the axis and the others are fixed;
* `IsTorsionMove.rigidWithin` — one move costs at most `2 √(2 I_red) |sin (δ/2)|`
  (`IsTorsionMove.rigidWithin_exact` and `IsTorsionMove.rigidWithin_min` are the exact coaxial
  value and the bound `2 √(min(I_A, I_B)) |sin (δ/2)|`);
* `rigidWithin_torsion_chain` — a sequence of torsion moves (arbitrary axes, arbitrary moving
  sets) costs at most `∑ k, 2 √(2 I_k) |sin (δ_k/2)|`, hence (`rigidWithin_torsion_chain_abs`) at
  most `∑ k, √(2 I_k) |δ_k|`;
* `IsTorsionMove.rigidWithinIn`, `rigidWithinIn_torsion_chain` — the same with the superposition
  restricted to any submonoid of motions containing the rotations about the torsion axes.

All atoms carry unit mass.
-/

namespace MetricChain

open Finset

/-! ## T1. The rigid-superposition pseudo-metric -/

section Minkowski

/-- Minkowski's inequality in `ℓ²`, in the squared form used below: if `∑ aᵢ² ≤ c₁²` and
`∑ bᵢ² ≤ c₂²` with `c₁, c₂ ≥ 0`, then `∑ (aᵢ + bᵢ)² ≤ (c₁ + c₂)²`. -/
theorem minkowski_l2_sq_le {ι : Type*} (s : Finset ι) (a b : ι → ℝ) {c₁ c₂ : ℝ}
    (hc₁ : 0 ≤ c₁) (hc₂ : 0 ≤ c₂)
    (ha : ∑ i ∈ s, a i ^ 2 ≤ c₁ ^ 2) (hb : ∑ i ∈ s, b i ^ 2 ≤ c₂ ^ 2) :
    ∑ i ∈ s, (a i + b i) ^ 2 ≤ (c₁ + c₂) ^ 2 := by
  have hcs : (∑ i ∈ s, a i * b i) ^ 2 ≤ (c₁ * c₂) ^ 2 := by
    calc (∑ i ∈ s, a i * b i) ^ 2 ≤ (∑ i ∈ s, a i ^ 2) * ∑ i ∈ s, b i ^ 2 :=
          sum_mul_sq_le_sq_mul_sq s a b
      _ ≤ c₁ ^ 2 * c₂ ^ 2 :=
          mul_le_mul ha hb (sum_nonneg fun i _ => sq_nonneg _) (sq_nonneg _)
      _ = (c₁ * c₂) ^ 2 := by ring
  have hab : ∑ i ∈ s, a i * b i ≤ c₁ * c₂ :=
    (abs_le_of_sq_le_sq' hcs (mul_nonneg hc₁ hc₂)).2
  have hexp : ∑ i ∈ s, (a i + b i) ^ 2 =
      ∑ i ∈ s, a i ^ 2 + 2 * ∑ i ∈ s, a i * b i + ∑ i ∈ s, b i ^ 2 := by
    rw [mul_sum, ← sum_add_distrib, ← sum_add_distrib]
    exact sum_congr rfl fun i _ => by ring
  rw [hexp]
  nlinarith

end Minkowski

section Rigid

variable {P : Type*} [PseudoMetricSpace P] {ι : Type*} [Fintype ι]

/-- `RigidWithinIn G x y c`: some rigid motion `g ∈ G` of the ambient space brings the
configuration `y` within `ℓ²` distance `c` of the configuration `x`.  Here `G` is a submonoid of the
isometry group of `P` (e.g. the proper motions), so that superpositions can be composed. -/
def RigidWithinIn (G : Submonoid (P ≃ᵢ P)) (x y : ι → P) (c : ℝ) : Prop :=
  ∃ g ∈ G, ∑ i, dist (x i) (g (y i)) ^ 2 ≤ c ^ 2

/-- `RigidWithin x y c`: some rigid motion (isometry) `g` of the ambient space brings the
configuration `y` within `ℓ²` distance `c` of the configuration `x`; for `c ≥ 0` the RMSD after
this superposition is then at most `c / √N` (`RigidWithin.exists_rmsd_le`). -/
def RigidWithin (x y : ι → P) (c : ℝ) : Prop :=
  ∃ g : P ≃ᵢ P, ∑ i, dist (x i) (g (y i)) ^ 2 ≤ c ^ 2

/-- `RigidWithin` is `RigidWithinIn` for the full isometry group. -/
theorem rigidWithinIn_top {x y : ι → P} {c : ℝ} :
    RigidWithinIn (⊤ : Submonoid (P ≃ᵢ P)) x y c ↔ RigidWithin x y c :=
  ⟨fun ⟨g, _, hg⟩ => ⟨g, hg⟩, fun ⟨g, hg⟩ => ⟨g, Submonoid.mem_top g, hg⟩⟩

/-- Forgetting the restriction on the superposing motion. -/
theorem RigidWithinIn.rigidWithin {G : Submonoid (P ≃ᵢ P)} {x y : ι → P} {c : ℝ}
    (h : RigidWithinIn G x y c) : RigidWithin x y c :=
  let ⟨g, _, hg⟩ := h
  ⟨g, hg⟩

/-- Enlarging the group of allowed superpositions. -/
theorem RigidWithinIn.mono_group {G H : Submonoid (P ≃ᵢ P)} (hGH : G ≤ H) {x y : ι → P} {c : ℝ}
    (h : RigidWithinIn G x y c) : RigidWithinIn H x y c :=
  let ⟨g, hgG, hg⟩ := h
  ⟨g, hGH hgG, hg⟩

/-- Reflexivity of restricted rigid superposition. -/
theorem rigidWithinIn_refl (G : Submonoid (P ≃ᵢ P)) (x : ι → P) : RigidWithinIn G x x 0 := by
  refine ⟨1, G.one_mem, ?_⟩
  show ∑ i, dist (x i) (x i) ^ 2 ≤ 0 ^ 2
  simp

/-- Monotonicity in the tolerance. -/
theorem RigidWithinIn.mono {G : Submonoid (P ≃ᵢ P)} {x y : ι → P} {c c' : ℝ}
    (h : RigidWithinIn G x y c) (hc : |c| ≤ |c'|) : RigidWithinIn G x y c' :=
  let ⟨g, hgG, hg⟩ := h
  ⟨g, hgG, hg.trans (sq_le_sq.mpr hc)⟩

/-- Triangle inequality for restricted rigid superposition. -/
theorem RigidWithinIn.trans {G : Submonoid (P ≃ᵢ P)} {x y z : ι → P} {c₁ c₂ : ℝ}
    (hc₁ : 0 ≤ c₁) (hc₂ : 0 ≤ c₂)
    (h₁ : RigidWithinIn G x y c₁) (h₂ : RigidWithinIn G y z c₂) :
    RigidWithinIn G x z (c₁ + c₂) := by
  obtain ⟨g, hgG, hg⟩ := h₁
  obtain ⟨h, hhG, hh⟩ := h₂
  refine ⟨g * h, G.mul_mem hgG hhG, ?_⟩
  have hh' : ∑ i, dist (g (y i)) (g (h (z i))) ^ 2 ≤ c₂ ^ 2 := by
    simpa only [g.dist_eq] using hh
  calc ∑ i, dist (x i) ((g * h) (z i)) ^ 2
      ≤ ∑ i, (dist (x i) (g (y i)) + dist (g (y i)) (g (h (z i)))) ^ 2 :=
        sum_le_sum fun i _ => pow_le_pow_left₀ dist_nonneg (dist_triangle _ _ _) 2
    _ ≤ (c₁ + c₂) ^ 2 := minkowski_l2_sq_le _ _ _ hc₁ hc₂ hg hh'

/-- Chain rule for restricted rigid superposition: costs add up along a path of
configurations. -/
theorem rigidWithinIn_chain (G : Submonoid (P ≃ᵢ P)) (X : ℕ → ι → P) (c : ℕ → ℝ) (m : ℕ)
    (hc : ∀ k < m, 0 ≤ c k) (h : ∀ k < m, RigidWithinIn G (X k) (X (k + 1)) (c k)) :
    RigidWithinIn G (X 0) (X m) (∑ k ∈ range m, c k) := by
  induction m with
  | zero => simpa using rigidWithinIn_refl G (X 0)
  | succ m ih =>
    rw [sum_range_succ]
    exact RigidWithinIn.trans
      (sum_nonneg fun k hk => hc k ((mem_range.mp hk).trans (Nat.lt_succ_self m)))
      (hc m (Nat.lt_succ_self m))
      (ih (fun k hk => hc k (hk.trans (Nat.lt_succ_self m)))
        (fun k hk => h k (hk.trans (Nat.lt_succ_self m))))
      (h m (Nat.lt_succ_self m))

/-- **(T1)** Every configuration is rigidly within `0` of itself. -/
theorem rigidWithin_refl (x : ι → P) : RigidWithin x x 0 :=
  (rigidWithinIn_refl ⊤ x).rigidWithin

/-- **(T1)** Symmetry of rigid superposition (use the inverse motion). -/
theorem RigidWithin.symm {x y : ι → P} {c : ℝ} (h : RigidWithin x y c) : RigidWithin y x c := by
  obtain ⟨g, hg⟩ := h
  refine ⟨g.symm, le_of_eq_of_le (sum_congr rfl fun i _ => ?_) hg⟩
  rw [dist_comm, ← g.dist_eq, g.apply_symm_apply]

/-- Monotonicity in the tolerance. -/
theorem RigidWithin.mono {x y : ι → P} {c c' : ℝ} (h : RigidWithin x y c) (hc : |c| ≤ |c'|) :
    RigidWithin x y c' :=
  let ⟨g, hg⟩ := h
  ⟨g, hg.trans (sq_le_sq.mpr hc)⟩

/-- **(T1)** Triangle inequality for the rigid-superposition pseudo-metric. -/
theorem RigidWithin.trans {x y z : ι → P} {c₁ c₂ : ℝ} (hc₁ : 0 ≤ c₁) (hc₂ : 0 ≤ c₂)
    (h₁ : RigidWithin x y c₁) (h₂ : RigidWithin y z c₂) : RigidWithin x z (c₁ + c₂) :=
  ((rigidWithinIn_top.mpr h₁).trans hc₁ hc₂ (rigidWithinIn_top.mpr h₂)).rigidWithin

/-- **(T1, chain form)** Along a path of configurations `X 0, …, X m` whose consecutive members
are rigidly within `c k ≥ 0`, the end configurations are rigidly within `∑ k < m, c k`. -/
theorem rigidWithin_chain (X : ℕ → ι → P) (c : ℕ → ℝ) (m : ℕ) (hc : ∀ k < m, 0 ≤ c k)
    (h : ∀ k < m, RigidWithin (X k) (X (k + 1)) (c k)) :
    RigidWithin (X 0) (X m) (∑ k ∈ range m, c k) :=
  (rigidWithinIn_chain ⊤ X c m hc fun k hk => rigidWithinIn_top.mpr (h k hk)).rigidWithin

/-- `RigidWithin` does not depend on the isometric chart used to describe the ambient space. -/
theorem rigidWithin_map_iff {Q : Type*} [PseudoMetricSpace Q] (u : P ≃ᵢ Q) {x y : ι → P}
    {c : ℝ} : RigidWithin (fun i => u (x i)) (fun i => u (y i)) c ↔ RigidWithin x y c := by
  constructor
  · rintro ⟨g, hg⟩
    refine ⟨u.trans (g.trans u.symm), le_of_eq_of_le (sum_congr rfl fun i _ => ?_) hg⟩
    rw [← u.dist_eq]
    simp
  · rintro ⟨g, hg⟩
    refine ⟨u.symm.trans (g.trans u), le_of_eq_of_le (sum_congr rfl fun i _ => ?_) hg⟩
    simp [u.dist_eq]

/-- `RigidWithin x y c` bounds the root-mean-square deviation after superposition by
`c / √N`, where `N` is the number of atoms. -/
theorem RigidWithin.exists_rmsd_le {x y : ι → P} {c : ℝ} (h : RigidWithin x y c) (hc : 0 ≤ c) :
    ∃ g : P ≃ᵢ P, Real.sqrt ((∑ i, dist (x i) (g (y i)) ^ 2) / Fintype.card ι) ≤
      c / Real.sqrt (Fintype.card ι) := by
  obtain ⟨g, hg⟩ := h
  refine ⟨g, ?_⟩
  rw [Real.sqrt_div (sum_nonneg fun i _ => sq_nonneg _)]
  refine div_le_div_of_nonneg_right ?_ (Real.sqrt_nonneg _)
  exact (Real.sqrt_le_sqrt hg).trans_eq (Real.sqrt_sq hc)

end Rigid

/-! ## T2. Exact coaxial cost of a single torsion move -/

section Coaxial

/-- Rotating a planar vector `w` by the angle `θ` displaces it by `2 ‖w‖² (1 - cos θ)`
(squared distance). -/
theorem planar_rotation_displacement_sq (θ : ℝ) (w : ℂ) :
    ‖Complex.exp (θ * Complex.I) * w - w‖ ^ 2 = 2 * ‖w‖ ^ 2 * (1 - Real.cos θ) := by
  have h : Complex.exp (θ * Complex.I) * w - w = (Complex.exp (θ * Complex.I) - 1) * w := by ring
  rw [h, norm_mul, mul_pow, Complex.sq_norm, Complex.normSq_apply]
  simp only [Complex.sub_re, Complex.sub_im, Complex.one_re, Complex.one_im,
    Complex.exp_ofReal_mul_I_re, Complex.exp_ofReal_mul_I_im, sub_zero]
  linear_combination (‖w‖ ^ 2) * Real.sin_sq_add_cos_sq θ

/-- Half-angle identity in the form used throughout: `cos φ = 1 - 2 sin²(φ/2)`. -/
theorem torsion_cos_half_angle (φ : ℝ) : Real.cos φ = 1 - 2 * Real.sin (φ / 2) ^ 2 := by
  have h := Real.cos_two_mul (φ / 2)
  rw [mul_div_cancel₀ φ (two_ne_zero)] at h
  rw [h, Real.cos_sq']
  ring

/-- **(T2-i)** Cost of the coaxial superposition by the angle `ψ`: the static atoms `a` are
displaced by the rotation `-ψ`, the atoms `b` (rotated by the torsion `φ`) by `φ - ψ`.  The total
squared displacement is `2 I_A (1 - cos ψ) + 2 I_B (1 - cos (φ - ψ))`. -/
theorem coaxial_cost_eq {ιA ιB : Type*} [Fintype ιA] [Fintype ιB] (a : ιA → ℂ) (b : ιB → ℂ)
    (φ ψ : ℝ) :
    ∑ i, ‖Complex.exp (-(ψ) * Complex.I) * a i - a i‖ ^ 2 +
        ∑ j, ‖Complex.exp ((φ - ψ) * Complex.I) * b j - b j‖ ^ 2 =
      2 * (∑ i, ‖a i‖ ^ 2) * (1 - Real.cos ψ) +
        2 * (∑ j, ‖b j‖ ^ 2) * (1 - Real.cos (φ - ψ)) := by
  rw [← Complex.ofReal_neg, ← Complex.ofReal_sub]
  simp only [planar_rotation_displacement_sq, Real.cos_neg]
  rw [← sum_mul, ← sum_mul, ← mul_sum, ← mul_sum]

/-- **(T2-ii)** The optimal coaxial superposition angle `ψ = arg (I_A + I_B e^{iφ})` realises the
cost `2 S - 2 √(S² - 4 I_A I_B sin²(φ/2))`, `S = I_A + I_B`.  (No sign condition is needed.) -/
theorem exists_coaxial_angle (IA IB φ : ℝ) :
    ∃ ψ : ℝ, 2 * IA * (1 - Real.cos ψ) + 2 * IB * (1 - Real.cos (φ - ψ)) =
      2 * (IA + IB) - 2 * Real.sqrt ((IA + IB) ^ 2 - 4 * IA * IB * Real.sin (φ / 2) ^ 2) := by
  set w : ℂ := (IA : ℂ) + (IB : ℂ) * Complex.exp (φ * Complex.I) with hw
  have hwre : w.re = IA + IB * Real.cos φ := by
    simp [hw, Complex.exp_ofReal_mul_I_re]
  have hwim : w.im = IB * Real.sin φ := by
    simp [hw, Complex.exp_ofReal_mul_I_im]
  have hre : ‖w‖ * Real.cos (Complex.arg w) = IA + IB * Real.cos φ := by
    rw [Complex.norm_mul_cos_arg, hwre]
  have him : ‖w‖ * Real.sin (Complex.arg w) = IB * Real.sin φ := by
    rw [Complex.norm_mul_sin_arg, hwim]
  have hnorm : ‖w‖ = Real.sqrt ((IA + IB) ^ 2 - 4 * IA * IB * Real.sin (φ / 2) ^ 2) := by
    rw [← Real.sqrt_sq (norm_nonneg w), Complex.sq_norm, Complex.normSq_apply, hwre, hwim]
    congr 1
    have h1 := Real.sin_sq_add_cos_sq φ
    have h2 := torsion_cos_half_angle φ
    rw [h2] at h1 ⊢
    linear_combination IB ^ 2 * h1
  refine ⟨Complex.arg w, ?_⟩
  rw [← hnorm, Real.cos_sub]
  have h1 := Real.sin_sq_add_cos_sq (Complex.arg w)
  linear_combination (2 * Real.cos (Complex.arg w)) * hre + (2 * Real.sin (Complex.arg w)) * him
    - (2 * ‖w‖) * h1

/-- **(T2-ii, optimality)** No coaxial superposition angle does better than the value of
`exists_coaxial_angle`: that value is the exact coaxial cost. -/
theorem coaxial_cost_ge (IA IB φ ψ : ℝ) :
    2 * (IA + IB) - 2 * Real.sqrt ((IA + IB) ^ 2 - 4 * IA * IB * Real.sin (φ / 2) ^ 2) ≤
      2 * IA * (1 - Real.cos ψ) + 2 * IB * (1 - Real.cos (φ - ψ)) := by
  have hsq : (IA * Real.cos ψ + IB * Real.cos (φ - ψ)) ^ 2 ≤
      (IA + IB) ^ 2 - 4 * IA * IB * Real.sin (φ / 2) ^ 2 := by
    rw [Real.cos_sub]
    have h1 := Real.sin_sq_add_cos_sq φ
    have h2 := Real.sin_sq_add_cos_sq ψ
    have h3 : Real.sin (φ / 2) ^ 2 = (1 - Real.cos φ) / 2 := by
      rw [torsion_cos_half_angle φ]; ring
    have key : (IA + IB) ^ 2 - 4 * IA * IB * Real.sin (φ / 2) ^ 2 -
        (IA * Real.cos ψ + IB * (Real.cos φ * Real.cos ψ + Real.sin φ * Real.sin ψ)) ^ 2 =
        ((IA + IB * Real.cos φ) * Real.sin ψ - IB * Real.sin φ * Real.cos ψ) ^ 2 := by
      rw [h3]
      linear_combination (-((IA + IB * Real.cos φ) ^ 2 + (IB * Real.sin φ) ^ 2)) * h2 -
        IB ^ 2 * h1
    nlinarith [sq_nonneg ((IA + IB * Real.cos φ) * Real.sin ψ - IB * Real.sin φ * Real.cos ψ)]
  have h := (le_abs_self _).trans (Real.abs_le_sqrt hsq)
  linarith

/-- **(T2-iii)** The exact coaxial cost is at most `8 I_red sin²(φ/2)` with the reduced moment of
inertia `I_red = I_A I_B / (I_A + I_B)`. -/
theorem coaxial_cost_le_reduced {IA IB : ℝ} (hA : 0 ≤ IA) (hB : 0 ≤ IB) (hS : 0 < IA + IB)
    (φ : ℝ) :
    2 * (IA + IB) - 2 * Real.sqrt ((IA + IB) ^ 2 - 4 * IA * IB * Real.sin (φ / 2) ^ 2) ≤
      8 * (IA * IB / (IA + IB)) * Real.sin (φ / 2) ^ 2 := by
  set s2 : ℝ := Real.sin (φ / 2) ^ 2 with hs2
  set t : ℝ := 4 * (IA * IB / (IA + IB)) * s2 with ht
  have hs2nn : 0 ≤ s2 := sq_nonneg _
  have htnn : 0 ≤ t := by positivity
  have hSt : (IA + IB) * t = 4 * IA * IB * s2 := by
    rw [ht]; field_simp
  have hgoal : (IA + IB) - t ≤ Real.sqrt ((IA + IB) ^ 2 - 4 * IA * IB * s2) := by
    by_cases hlt : (IA + IB) - t ≤ 0
    · exact hlt.trans (Real.sqrt_nonneg _)
    · have hpos : 0 < (IA + IB) - t := not_le.mp hlt
      rw [Real.le_sqrt' hpos]
      nlinarith
  linarith

/-- Complementary lower bound: the exact coaxial cost is at least `4 I_red sin²(φ/2)`; together
with `coaxial_cost_le_reduced` the reduced moment of inertia controls the cost up to a factor
`2`. -/
theorem reduced_le_coaxial_cost {IA IB : ℝ} (hA : 0 ≤ IA) (hB : 0 ≤ IB) (hS : 0 < IA + IB)
    (φ : ℝ) :
    4 * (IA * IB / (IA + IB)) * Real.sin (φ / 2) ^ 2 ≤
      2 * (IA + IB) - 2 * Real.sqrt ((IA + IB) ^ 2 - 4 * IA * IB * Real.sin (φ / 2) ^ 2) := by
  set s2 : ℝ := Real.sin (φ / 2) ^ 2 with hs2
  set t : ℝ := 2 * (IA * IB / (IA + IB)) * s2 with ht
  have hs2nn : 0 ≤ s2 := sq_nonneg _
  have hs2le : s2 ≤ 1 := by
    have := Real.sin_sq_le_one (φ / 2)
    simpa [hs2] using this
  have htnn : 0 ≤ t := by positivity
  have hSt : (IA + IB) * t = 2 * IA * IB * s2 := by
    rw [ht]; field_simp
  have hAB : 0 ≤ IA * IB := mul_nonneg hA hB
  have htS : t ≤ IA + IB := by
    by_contra hcon
    have hlt : IA + IB < t := not_le.mp hcon
    nlinarith [mul_nonneg hAB hs2nn, mul_nonneg hAB (sub_nonneg.mpr hs2le)]
  have hgoal : Real.sqrt ((IA + IB) ^ 2 - 4 * IA * IB * s2) ≤ (IA + IB) - t := by
    rw [Real.sqrt_le_left (sub_nonneg.mpr htS)]
    nlinarith [sq_nonneg t]
  linarith

/-- The exact coaxial cost is at most `4 min(I_A, I_B) sin²(φ/2)`: superposing either side exactly
is one possible coaxial choice (`ψ = 0` or `ψ = φ`). -/
theorem coaxial_cost_le_min (IA IB φ : ℝ) :
    2 * (IA + IB) - 2 * Real.sqrt ((IA + IB) ^ 2 - 4 * IA * IB * Real.sin (φ / 2) ^ 2) ≤
      4 * min IA IB * Real.sin (φ / 2) ^ 2 := by
  have h0 := coaxial_cost_ge IA IB φ 0
  have hφ := coaxial_cost_ge IA IB φ φ
  rw [sub_zero, Real.cos_zero, torsion_cos_half_angle φ] at h0
  rw [sub_self, Real.cos_zero, torsion_cos_half_angle φ] at hφ
  rcases min_cases IA IB with ⟨h, _⟩ | ⟨h, _⟩ <;> rw [h] <;> linarith

/-- The smaller moment of inertia is at most twice the reduced one, so the bound
`coaxial_cost_le_min` is never worse than `coaxial_cost_le_reduced`:
`4 min(I_A, I_B) sin²(φ/2) ≤ 8 I_red sin²(φ/2)`. -/
theorem min_inertia_le_two_reduced {IA IB : ℝ} (hA : 0 ≤ IA) (hB : 0 ≤ IB) (hS : 0 < IA + IB) :
    min IA IB ≤ 2 * (IA * IB / (IA + IB)) := by
  rw [← mul_div_assoc, le_div_iff₀ hS]
  rcases min_cases IA IB with ⟨h, hle⟩ | ⟨h, hlt⟩ <;> rw [h] <;> nlinarith

/-- Real-variable core of the combined statement: for nonnegative moments of inertia some coaxial
superposition angle costs at most `8 I_red sin²(φ/2)` (also when `I_A + I_B = 0`). -/
theorem exists_coaxial_angle_le {IA IB : ℝ} (hA : 0 ≤ IA) (hB : 0 ≤ IB) (φ : ℝ) :
    ∃ ψ : ℝ, 2 * IA * (1 - Real.cos ψ) + 2 * IB * (1 - Real.cos (φ - ψ)) ≤
      8 * (IA * IB / (IA + IB)) * Real.sin (φ / 2) ^ 2 := by
  rcases (add_nonneg hA hB).eq_or_lt with h0 | hpos
  · have hA0 : IA = 0 := by linarith
    have hB0 : IB = 0 := by linarith
    exact ⟨0, by simp [hA0, hB0]⟩
  · obtain ⟨ψ, hψ⟩ := exists_coaxial_angle IA IB φ
    exact ⟨ψ, hψ.le.trans (coaxial_cost_le_reduced hA hB hpos φ)⟩

/-- **(T2, combined)** For static atoms `a` and atoms `b` rotated by the torsion angle `φ` about
the axis, some coaxial superposition `ψ` has total squared displacement at most
`8 (I_A I_B / (I_A + I_B)) sin²(φ/2)`. -/
theorem exists_coaxial_superposition {ιA ιB : Type*} [Fintype ιA] [Fintype ιB] (a : ιA → ℂ)
    (b : ιB → ℂ) (φ : ℝ) :
    ∃ ψ : ℝ,
      ∑ i, ‖Complex.exp (-(ψ) * Complex.I) * a i - a i‖ ^ 2 +
          ∑ j, ‖Complex.exp ((φ - ψ) * Complex.I) * b j - b j‖ ^ 2 ≤
        8 * ((∑ i, ‖a i‖ ^ 2) * (∑ j, ‖b j‖ ^ 2) / (∑ i, ‖a i‖ ^ 2 + ∑ j, ‖b j‖ ^ 2)) *
          Real.sin (φ / 2) ^ 2 := by
  obtain ⟨ψ, hψ⟩ := exists_coaxial_angle_le (IA := ∑ i, ‖a i‖ ^ 2) (IB := ∑ j, ‖b j‖ ^ 2)
    (sum_nonneg fun i _ => sq_nonneg _) (sum_nonneg fun j _ => sq_nonneg _) φ
  exact ⟨ψ, (coaxial_cost_eq a b φ ψ).trans_le hψ⟩

end Coaxial

/-! ## T3. The model space, torsion moves and their chain rule -/

section Model

/-- Model Euclidean 3-space in coordinates adapted to an axis: the plane perpendicular to the axis
is `ℂ`, the axis is `ℝ`, and the metric is the `ℓ²` product metric. -/
abbrev AxisSpace : Type := WithLp 2 (ℂ × ℝ)

/-- Rotation by the angle `ψ` about the `z`-axis of `AxisSpace`: `(w, z) ↦ (e^{iψ} w, z)`,
as an isometry. -/
noncomputable def axisRot (ψ : ℝ) : AxisSpace ≃ᵢ AxisSpace where
  toFun p := WithLp.toLp 2 (Complex.exp (ψ * Complex.I) * p.fst, p.snd)
  invFun p := WithLp.toLp 2 (Complex.exp (-(ψ * Complex.I)) * p.fst, p.snd)
  left_inv p := by
    have h : Complex.exp (-(ψ * Complex.I)) * (Complex.exp (ψ * Complex.I) * p.fst) = p.fst := by
      rw [← mul_assoc, ← Complex.exp_add, neg_add_cancel, Complex.exp_zero, one_mul]
    show WithLp.toLp 2 (Complex.exp (-(ψ * Complex.I)) * (Complex.exp (ψ * Complex.I) * p.fst),
      p.snd) = p
    rw [h]
    rfl
  right_inv p := by
    have h : Complex.exp (ψ * Complex.I) * (Complex.exp (-(ψ * Complex.I)) * p.fst) = p.fst := by
      rw [← mul_assoc, ← Complex.exp_add, add_neg_cancel, Complex.exp_zero, one_mul]
    show WithLp.toLp 2 (Complex.exp (ψ * Complex.I) * (Complex.exp (-(ψ * Complex.I)) * p.fst),
      p.snd) = p
    rw [h]
    rfl
  isometry_toFun := by
    refine Isometry.of_dist_eq fun p q => ?_
    rw [WithLp.prod_dist_eq_of_L2, WithLp.prod_dist_eq_of_L2]
    simp only [WithLp.toLp_fst, WithLp.toLp_snd]
    rw [dist_eq_norm, ← mul_sub, norm_mul, Complex.norm_exp_ofReal_mul_I, one_mul, ← dist_eq_norm]

@[simp] theorem axisRot_fst (ψ : ℝ) (p : AxisSpace) :
    (axisRot ψ p).fst = Complex.exp (ψ * Complex.I) * p.fst := rfl

@[simp] theorem axisRot_snd (ψ : ℝ) (p : AxisSpace) : (axisRot ψ p).snd = p.snd := rfl

theorem axisRot_apply (ψ : ℝ) (p : AxisSpace) :
    axisRot ψ p = WithLp.toLp 2 (Complex.exp (ψ * Complex.I) * p.fst, p.snd) := rfl

/-- Rotations about the axis compose by adding angles. -/
theorem axisRot_axisRot (θ θ' : ℝ) (p : AxisSpace) :
    axisRot θ (axisRot θ' p) = axisRot (θ + θ') p := by
  rw [axisRot_apply, axisRot_apply (θ + θ'), axisRot_fst, axisRot_snd, ← mul_assoc,
    ← Complex.exp_add, ← add_mul, ← Complex.ofReal_add]

/-- A rotation by `θ` about the axis displaces a point by `2 r² (1 - cos θ)` (squared), where `r`
is its distance to the axis. -/
theorem dist_axisRot_sq (θ : ℝ) (p : AxisSpace) :
    dist p (axisRot θ p) ^ 2 = 2 * ‖p.fst‖ ^ 2 * (1 - Real.cos θ) := by
  rw [WithLp.prod_dist_eq_of_L2, Real.sq_sqrt (by positivity), axisRot_fst, axisRot_snd,
    dist_self, dist_comm, dist_eq_norm, planar_rotation_displacement_sq]
  ring

/-- **(T3, concrete form)** In the model space, the configuration in which the atoms
`(b j, zb j)` are rotated by `φ` about the axis while the atoms `(a i, za i)` stay put is rigidly
within `√(8 (I_A I_B / S) sin²(φ/2))` of the original configuration. -/
theorem rigidWithin_axis_torsion {ιA ιB : Type*} [Fintype ιA] [Fintype ιB]
    (a : ιA → ℂ) (za : ιA → ℝ) (b : ιB → ℂ) (zb : ιB → ℝ) (φ : ℝ) :
    RigidWithin
      (Sum.elim (fun i => WithLp.toLp 2 (a i, za i)) (fun j => WithLp.toLp 2 (b j, zb j)) :
        ιA ⊕ ιB → AxisSpace)
      (Sum.elim (fun i => WithLp.toLp 2 (a i, za i))
        (fun j => WithLp.toLp 2 (Complex.exp (φ * Complex.I) * b j, zb j)))
      (Real.sqrt (8 * ((∑ i, ‖a i‖ ^ 2) * (∑ j, ‖b j‖ ^ 2) /
        (∑ i, ‖a i‖ ^ 2 + ∑ j, ‖b j‖ ^ 2)) * Real.sin (φ / 2) ^ 2)) := by
  have hA : 0 ≤ ∑ i, ‖a i‖ ^ 2 := sum_nonneg fun i _ => sq_nonneg _
  have hB : 0 ≤ ∑ j, ‖b j‖ ^ 2 := sum_nonneg fun j _ => sq_nonneg _
  obtain ⟨ψ, hψ⟩ := exists_coaxial_angle_le hA hB φ
  refine ⟨axisRot (-ψ), ?_⟩
  rw [Real.sq_sqrt (by positivity), Fintype.sum_sum_type]
  refine le_of_eq_of_le ?_ hψ
  simp only [Sum.elim_inl, Sum.elim_inr]
  congr 1
  · rw [mul_sum, sum_mul]
    refine sum_congr rfl fun i _ => ?_
    rw [dist_axisRot_sq, Real.cos_neg, WithLp.toLp_fst]
  · rw [mul_sum, sum_mul]
    refine sum_congr rfl fun j _ => ?_
    have hrot : (WithLp.toLp 2 (Complex.exp (φ * Complex.I) * b j, zb j) : AxisSpace) =
        axisRot φ (WithLp.toLp 2 (b j, zb j)) := rfl
    rw [hrot, axisRot_axisRot, dist_axisRot_sq, neg_add_eq_sub, WithLp.toLp_fst]

end Model

section Torsion

variable {ι : Type*} {P : Type*} [PseudoMetricSpace P]

/-- Moment of inertia (unit masses) of the atoms in `s` about the axis which the chart `u` sends
to the `z`-axis of `AxisSpace`. -/
noncomputable def axialInertia (u : P ≃ᵢ AxisSpace) (s : Finset ι) (X : ι → P) : ℝ :=
  ∑ i ∈ s, ‖(u (X i)).fst‖ ^ 2

theorem axialInertia_nonneg (u : P ≃ᵢ AxisSpace) (s : Finset ι) (X : ι → P) :
    0 ≤ axialInertia u s X :=
  sum_nonneg fun _ _ => sq_nonneg _

variable [Fintype ι] [DecidableEq ι]

/-- Reduced moment of inertia `I_A I_B / (I_A + I_B)` of the two sides `Bᶜ`, `B` of a torsion
about the axis singled out by the chart `u`. -/
noncomputable def reducedInertia (u : P ≃ᵢ AxisSpace) (B : Finset ι) (X : ι → P) : ℝ :=
  axialInertia u Bᶜ X * axialInertia u B X / (axialInertia u Bᶜ X + axialInertia u B X)

theorem reducedInertia_nonneg (u : P ≃ᵢ AxisSpace) (B : Finset ι) (X : ι → P) :
    0 ≤ reducedInertia u B X :=
  div_nonneg (mul_nonneg (axialInertia_nonneg u _ X) (axialInertia_nonneg u _ X))
    (add_nonneg (axialInertia_nonneg u _ X) (axialInertia_nonneg u _ X))

/-- `IsTorsionMove u B δ X Y`: the configuration `Y` arises from `X` by a single torsion move.
In the isometric chart `u` (which sends the torsion axis to the `z`-axis of `AxisSpace`) the atoms
of `B` are rotated by the angle `δ` about the axis and all other atoms stay fixed. -/
structure IsTorsionMove (u : P ≃ᵢ AxisSpace) (B : Finset ι) (δ : ℝ) (X Y : ι → P) : Prop where
  /-- atoms outside `B` do not move -/
  fixed : ∀ i, i ∉ B → Y i = X i
  /-- atoms of `B` are rotated by `δ` about the axis -/
  moved : ∀ i, i ∈ B → u (Y i) = axisRot δ (u (X i))

/-- Cost of superposing a torsion move by the rotation `-ψ` about its own axis. -/
theorem IsTorsionMove.sum_dist_sq {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ} {X Y : ι → P}
    (h : IsTorsionMove u B δ X Y) (ψ : ℝ) :
    ∑ i, dist (u (X i)) (axisRot (-ψ) (u (Y i))) ^ 2 =
      2 * axialInertia u Bᶜ X * (1 - Real.cos ψ) +
        2 * axialInertia u B X * (1 - Real.cos (δ - ψ)) := by
  rw [← sum_compl_add_sum B]
  congr 1
  · rw [axialInertia, mul_sum, sum_mul]
    refine sum_congr rfl fun i hi => ?_
    rw [h.fixed i (mem_compl.mp hi), dist_axisRot_sq, Real.cos_neg]
  · rw [axialInertia, mul_sum, sum_mul]
    refine sum_congr rfl fun i hi => ?_
    rw [h.moved i hi, axisRot_axisRot, dist_axisRot_sq, neg_add_eq_sub]

omit [DecidableEq ι] in
/-- Superposing by the motion `r` of the model space, read in the chart `u`. -/
theorem sum_dist_sq_chart (u : P ≃ᵢ AxisSpace) (r : AxisSpace ≃ᵢ AxisSpace) (X Y : ι → P) :
    ∑ i, dist (X i) ((u.trans (r.trans u.symm)) (Y i)) ^ 2 =
      ∑ i, dist (u (X i)) (r (u (Y i))) ^ 2 := by
  refine sum_congr rfl fun i _ => ?_
  rw [← u.dist_eq]
  simp

/-- A torsion move can be superposed by a rotation about its own axis at squared cost at most
`8 I_red sin²(δ/2)`. -/
theorem IsTorsionMove.exists_axisRot {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ} {X Y : ι → P}
    (h : IsTorsionMove u B δ X Y) :
    ∃ ψ : ℝ, ∑ i, dist (X i) ((u.trans ((axisRot ψ).trans u.symm)) (Y i)) ^ 2 ≤
      (2 * Real.sqrt (2 * reducedInertia u B X) * |Real.sin (δ / 2)|) ^ 2 := by
  obtain ⟨ψ, hψ⟩ := exists_coaxial_angle_le (axialInertia_nonneg u Bᶜ X)
    (axialInertia_nonneg u B X) δ
  refine ⟨-ψ, ?_⟩
  have hc : (2 * Real.sqrt (2 * reducedInertia u B X) * |Real.sin (δ / 2)|) ^ 2 =
      8 * reducedInertia u B X * Real.sin (δ / 2) ^ 2 := by
    rw [mul_pow, mul_pow, Real.sq_sqrt (mul_nonneg zero_le_two (reducedInertia_nonneg u B X)),
      sq_abs]
    ring
  rw [hc, sum_dist_sq_chart]
  exact (h.sum_dist_sq ψ).trans_le hψ

/-- **(T3, exact coaxial form)** Superposing a torsion move by the optimal rotation about its own
axis costs exactly `√(2 S - 2 √(S² - 4 I_A I_B sin²(δ/2)))`, where `I_A`, `I_B` are the axial
moments of inertia of the fixed and of the moving atoms and `S = I_A + I_B`. -/
theorem IsTorsionMove.rigidWithin_exact {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ}
    {X Y : ι → P} (h : IsTorsionMove u B δ X Y) :
    RigidWithin X Y
      (Real.sqrt (2 * (axialInertia u Bᶜ X + axialInertia u B X) -
        2 * Real.sqrt ((axialInertia u Bᶜ X + axialInertia u B X) ^ 2 -
          4 * axialInertia u Bᶜ X * axialInertia u B X * Real.sin (δ / 2) ^ 2))) := by
  obtain ⟨ψ, hψ⟩ := exists_coaxial_angle (axialInertia u Bᶜ X) (axialInertia u B X) δ
  have hsum := (h.sum_dist_sq ψ).trans hψ
  refine ⟨u.trans ((axisRot (-ψ)).trans u.symm), ?_⟩
  have hnn : 0 ≤ 2 * (axialInertia u Bᶜ X + axialInertia u B X) -
      2 * Real.sqrt ((axialInertia u Bᶜ X + axialInertia u B X) ^ 2 -
        4 * axialInertia u Bᶜ X * axialInertia u B X * Real.sin (δ / 2) ^ 2) := by
    rw [← hsum]
    exact sum_nonneg fun i _ => sq_nonneg _
  rw [Real.sq_sqrt hnn, sum_dist_sq_chart, hsum]

/-- **(T3, `min` form)** A single torsion move costs at most `2 √(min(I_A, I_B)) |sin (δ/2)|`
(superpose the heavier side); this is never worse than the reduced-inertia bound
`IsTorsionMove.rigidWithin`, because `min(I_A, I_B) ≤ 2 I_A I_B / (I_A + I_B)`. -/
theorem IsTorsionMove.rigidWithin_min {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ}
    {X Y : ι → P} (h : IsTorsionMove u B δ X Y) :
    RigidWithin X Y
      (2 * Real.sqrt (min (axialInertia u Bᶜ X) (axialInertia u B X)) * |Real.sin (δ / 2)|) := by
  refine h.rigidWithin_exact.mono ?_
  have hmin : 0 ≤ min (axialInertia u Bᶜ X) (axialInertia u B X) :=
    le_min (axialInertia_nonneg u _ X) (axialInertia_nonneg u _ X)
  rw [abs_of_nonneg (Real.sqrt_nonneg _), abs_of_nonneg (by positivity)]
  calc Real.sqrt (2 * (axialInertia u Bᶜ X + axialInertia u B X) -
        2 * Real.sqrt ((axialInertia u Bᶜ X + axialInertia u B X) ^ 2 -
          4 * axialInertia u Bᶜ X * axialInertia u B X * Real.sin (δ / 2) ^ 2))
      ≤ Real.sqrt (4 * min (axialInertia u Bᶜ X) (axialInertia u B X) *
          Real.sin (δ / 2) ^ 2) := Real.sqrt_le_sqrt (coaxial_cost_le_min _ _ _)
    _ = 2 * Real.sqrt (min (axialInertia u Bᶜ X) (axialInertia u B X)) *
          |Real.sin (δ / 2)| := by
        have hrew : 4 * min (axialInertia u Bᶜ X) (axialInertia u B X) * Real.sin (δ / 2) ^ 2 =
            (2 * |Real.sin (δ / 2)|) ^ 2 * min (axialInertia u Bᶜ X) (axialInertia u B X) := by
          rw [mul_pow, sq_abs]; ring
        rw [hrew, Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (by positivity)]
        ring

/-- **(T3)** A single torsion move by the angle `δ` displaces the configuration, up to rigid
superposition, by at most `2 √(2 I_red) |sin (δ/2)|`. -/
theorem IsTorsionMove.rigidWithin {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ} {X Y : ι → P}
    (h : IsTorsionMove u B δ X Y) :
    RigidWithin X Y (2 * Real.sqrt (2 * reducedInertia u B X) * |Real.sin (δ / 2)|) :=
  let ⟨_, hψ⟩ := h.exists_axisRot
  ⟨_, hψ⟩

/-- Version of `IsTorsionMove.rigidWithin` with the superposition restricted to a submonoid `G`
of motions containing the rotations about the torsion axis. -/
theorem IsTorsionMove.rigidWithinIn {u : P ≃ᵢ AxisSpace} {B : Finset ι} {δ : ℝ} {X Y : ι → P}
    (h : IsTorsionMove u B δ X Y) (G : Submonoid (P ≃ᵢ P))
    (hG : ∀ ψ : ℝ, u.trans ((axisRot ψ).trans u.symm) ∈ G) :
    RigidWithinIn G X Y (2 * Real.sqrt (2 * reducedInertia u B X) * |Real.sin (δ / 2)|) :=
  let ⟨ψ, hψ⟩ := h.exists_axisRot
  ⟨_, hG ψ, hψ⟩

/-- **(T3, chain rule)** A sequence of single-torsion moves `X 0 → X 1 → ⋯ → X m` (move `k` about
the axis of the chart `u k`, rotating the atoms `B k` by `δ k`) displaces the configuration, up to
rigid superposition, by at most `∑ k < m, 2 √(2 I_k) |sin (δ_k / 2)|`, where `I_k` is the reduced
moment of inertia of move `k`. -/
theorem rigidWithin_torsion_chain (X : ℕ → ι → P) (u : ℕ → P ≃ᵢ AxisSpace) (B : ℕ → Finset ι)
    (δ : ℕ → ℝ) (m : ℕ) (h : ∀ k < m, IsTorsionMove (u k) (B k) (δ k) (X k) (X (k + 1))) :
    RigidWithin (X 0) (X m)
      (∑ k ∈ range m, 2 * Real.sqrt (2 * reducedInertia (u k) (B k) (X k)) *
        |Real.sin (δ k / 2)|) :=
  rigidWithin_chain X _ m (fun _ _ => by positivity) fun k hk => (h k hk).rigidWithin

/-- Restricted-group version of `rigidWithin_torsion_chain`. -/
theorem rigidWithinIn_torsion_chain (G : Submonoid (P ≃ᵢ P)) (X : ℕ → ι → P)
    (u : ℕ → P ≃ᵢ AxisSpace) (B : ℕ → Finset ι) (δ : ℕ → ℝ) (m : ℕ)
    (hG : ∀ k < m, ∀ ψ : ℝ, (u k).trans ((axisRot ψ).trans (u k).symm) ∈ G)
    (h : ∀ k < m, IsTorsionMove (u k) (B k) (δ k) (X k) (X (k + 1))) :
    RigidWithinIn G (X 0) (X m)
      (∑ k ∈ range m, 2 * Real.sqrt (2 * reducedInertia (u k) (B k) (X k)) *
        |Real.sin (δ k / 2)|) :=
  rigidWithinIn_chain G X _ m (fun _ _ => by positivity)
    fun k hk => (h k hk).rigidWithinIn G (hG k hk)

/-- Linearised chain rule: the displacement is at most `∑ k < m, √(2 I_k) |δ_k|`, i.e. the
rigid-superposition distance is Lipschitz in each torsion angle with constant `√(2 I_red)`. -/
theorem rigidWithin_torsion_chain_abs (X : ℕ → ι → P) (u : ℕ → P ≃ᵢ AxisSpace)
    (B : ℕ → Finset ι) (δ : ℕ → ℝ) (m : ℕ)
    (h : ∀ k < m, IsTorsionMove (u k) (B k) (δ k) (X k) (X (k + 1))) :
    RigidWithin (X 0) (X m)
      (∑ k ∈ range m, Real.sqrt (2 * reducedInertia (u k) (B k) (X k)) * |δ k|) := by
  refine (rigidWithin_torsion_chain X u B δ m h).mono ?_
  rw [abs_of_nonneg (sum_nonneg fun _ _ => by positivity),
    abs_of_nonneg (sum_nonneg fun _ _ => by positivity)]
  refine sum_le_sum fun k _ => ?_
  have h1 : |Real.sin (δ k / 2)| ≤ |δ k| / 2 := by
    have := Real.abs_sin_le_abs (x := δ k / 2)
    rwa [abs_div, abs_two] at this
  have h2 : 0 ≤ Real.sqrt (2 * reducedInertia (u k) (B k) (X k)) := Real.sqrt_nonneg _
  nlinarith [mul_le_mul_of_nonneg_left h1 h2]

end Torsion

/-! ## Non-vacuity checks -/

section Examples

/-- One static and one moving atom, both at unit distance from the axis, torsion angle `φ = π`:
`I_A = I_B = 1`, `S = 2`.  The exact coaxial cost `2 S - 2 √(S² - 4 I_A I_B sin²(φ/2))` is `4`. -/
example :
    2 * ((1 : ℝ) + 1) -
      2 * Real.sqrt (((1 : ℝ) + 1) ^ 2 - 4 * 1 * 1 * Real.sin (Real.pi / 2) ^ 2) = 4 := by
  rw [Real.sin_pi_div_two]
  norm_num

/-- … and the reduced-inertia bound `8 (I_A I_B / S) sin²(φ/2)` is also `4`: (T2-iii) is sharp. -/
example : 8 * ((1 : ℝ) * 1 / (1 + 1)) * Real.sin (Real.pi / 2) ^ 2 = 4 := by
  rw [Real.sin_pi_div_two]
  norm_num

/-- In that configuration every coaxial superposition angle costs exactly `4`. -/
example (ψ : ℝ) :
    2 * (1 : ℝ) * (1 - Real.cos ψ) + 2 * 1 * (1 - Real.cos (Real.pi - ψ)) = 4 := by
  rw [Real.cos_pi_sub]
  ring

/-- (T2) instantiated with concrete families: static atom at `1`, moving atom at `1`, `φ = π`. -/
example :
    ∃ ψ : ℝ,
      ∑ _i : Fin 1, ‖Complex.exp (-(ψ) * Complex.I) * (1 : ℂ) - 1‖ ^ 2 +
        ∑ _j : Fin 1, ‖Complex.exp ((Real.pi - ψ) * Complex.I) * (1 : ℂ) - 1‖ ^ 2 ≤ 4 := by
  obtain ⟨ψ, hψ⟩ :=
    exists_coaxial_superposition (fun _ : Fin 1 => (1 : ℂ)) (fun _ : Fin 1 => (1 : ℂ)) Real.pi
  refine ⟨ψ, hψ.trans (le_of_eq ?_)⟩
  rw [Real.sin_pi_div_two]
  norm_num

/-- (T3) instantiated: two atoms at unit distance from the axis, the second one rotated by `π`.
The hypotheses of `IsTorsionMove` are satisfiable and the conclusion reads `RigidWithin X Y 2`. -/
example :
    ∃ X Y : Fin 2 → AxisSpace,
      IsTorsionMove (IsometryEquiv.refl AxisSpace) {1} Real.pi X Y ∧ RigidWithin X Y 2 := by
  let X : Fin 2 → AxisSpace := fun _ => WithLp.toLp 2 ((1 : ℂ), (0 : ℝ))
  let Y : Fin 2 → AxisSpace := fun i => if i = 1 then axisRot Real.pi (X i) else X i
  have hmove : IsTorsionMove (IsometryEquiv.refl AxisSpace) {1} Real.pi X Y := by
    refine ⟨fun i hi => ?_, fun i hi => ?_⟩
    · have hi' : i ≠ 1 := by simpa using hi
      simp [Y, hi']
    · have hi' : i = 1 := by simpa using hi
      subst hi'
      rfl
  refine ⟨X, Y, hmove, ?_⟩
  have h := hmove.rigidWithin
  have hA : axialInertia (IsometryEquiv.refl AxisSpace) ({1} : Finset (Fin 2))ᶜ X = 1 := by
    have hc : ({1} : Finset (Fin 2))ᶜ = {0} := by decide
    rw [hc, axialInertia, sum_singleton]
    show ‖(1 : ℂ)‖ ^ 2 = 1
    simp
  have hB : axialInertia (IsometryEquiv.refl AxisSpace) ({1} : Finset (Fin 2)) X = 1 := by
    rw [axialInertia, sum_singleton]
    show ‖(1 : ℂ)‖ ^ 2 = 1
    simp
  have hred : reducedInertia (IsometryEquiv.refl AxisSpace) ({1} : Finset (Fin 2)) X = 1 / 2 := by
    rw [reducedInertia, hA, hB]
    norm_num
  rw [hred, Real.sin_pi_div_two] at h
  simpa using h

end Examples

end MetricChain
