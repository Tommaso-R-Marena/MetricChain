import Mathlib

/-!
# Theorem 5 and Proposition 9: the two-sided perturbation bracket and the caloric bracket

Science division, workstream L1.  Source: `docs/science/INFERENCE_LIMITS.md` §5, Theorem 5
(first display; "no class needed"):

    -β E_{μ₀} g  ≤  ln (Z_g / Z_0)  ≤  -β U,      U = E_{μ_g} g,
    width = β (E_{μ₀} g - E_{μ_g} g) = KL(μ₀‖μ_g) + KL(μ_g‖μ₀).

Here `μ₀` is a positive probability vector on a finite type (the model's Gibbs measure),
`zRatio μ₀ g β = ∑ μ₀ exp (-β g) = Z_g / Z_0` (`zRatio_eq_partition_ratio`) and
`tilt μ₀ g β ∝ μ₀ exp (-β g)` is the true ensemble `μ_g`.

## What is proved

* `kl_model_true` — `KL(μ₀‖μ_g) = β E_{μ₀} g + ln (Z_g/Z_0)`;
* `kl_true_model` — `KL(μ_g‖μ₀) = -β E_{μ_g} g - ln (Z_g/Z_0)`;
* `theorem5_bracket` — the two inequalities and the width identity, for every real `β` and
  every `g` (no class).

The lower end is the Gibbs–Bogoliubov inequality, which the theory division has as
`MetricChain.gibbs_bogoliubov`; the identity for `KL(μ₀‖μ_g)` is their
`kl_reference_target_eq_gap`.  The file is self-contained (imports only Mathlib).

* `logZ_step`, `meanEnergy_anti`, `caloric_bracket`, `caloric_bracket_width` —
  **Proposition 9** (§10): the mean energy `U(β)` is non-increasing, and for any
  `b 0, …, b m`:
  `-∑ (b_{j+1} - b_j) U(b_j) ≤ ln Z(b_m) - ln Z(b_0) ≤ -∑ (b_{j+1} - b_j) U(b_{j+1})`, of width at
  most `max_j (b_{j+1} - b_j) · (U(b_0) - U(b_m))` for increasing `b`.  These follow from
  Theorem 5 applied on each interval; no calculus is used, and the identity
  `ln Z(b_m) - ln Z(b_0) = -∫ U dβ` is not formalised.

Not formalised: the sampled form of Theorem 5 (McDiarmid), the Corollary at the zero residual,
Proposition 5b.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL1

open Finset

variable {X : Type*} [Fintype X]

/-- Relative entropy `KL(p‖q) = ∑ p (log p - log q)` on a finite type. -/
def klDivFin (p q : X → ℝ) : ℝ := ∑ x, p x * (Real.log (p x) - Real.log (q x))

/-- `Z_g / Z_0 = E_{μ₀} exp (-β g)`. -/
def zRatio (μ₀ g : X → ℝ) (β : ℝ) : ℝ := ∑ x, μ₀ x * Real.exp (-β * g x)

/-- The true ensemble `μ_g ∝ μ₀ exp (-β g)`. -/
def tilt (μ₀ g : X → ℝ) (β : ℝ) (x : X) : ℝ := μ₀ x * Real.exp (-β * g x) / zRatio μ₀ g β

/-- For `μ₀ = exp (-β f) / Z_0`, `zRatio` is the ratio of partition functions `Z_g / Z_0`. -/
theorem zRatio_eq_partition_ratio (f g : X → ℝ) (β : ℝ) :
    zRatio (fun x => Real.exp (-β * f x) / ∑ y, Real.exp (-β * f y)) g β =
      (∑ x, Real.exp (-β * (f x + g x))) / ∑ y, Real.exp (-β * f y) := by
  unfold zRatio
  rw [Finset.sum_div]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [div_mul_eq_mul_div, ← Real.exp_add]
  congr 2
  ring

/-- **Gibbs' inequality.**  `KL(p‖q) ≥ 0` for `p ≥ 0`, `q > 0`, `∑ q ≤ ∑ p`. -/
theorem klDivFin_nonneg (p q : X → ℝ) (hp : ∀ x, 0 ≤ p x) (hq : ∀ x, 0 < q x)
    (hsum : ∑ x, q x ≤ ∑ x, p x) : 0 ≤ klDivFin p q := by
  have hterm : ∀ x, p x - q x ≤ p x * (Real.log (p x) - Real.log (q x)) := by
    intro x
    rcases (hp x).eq_or_lt with h0 | hpos
    · rw [← h0, zero_mul]
      linarith [hq x]
    · have h1 := Real.log_le_sub_one_of_pos (div_pos (hq x) hpos)
      rw [Real.log_div (hq x).ne' hpos.ne'] at h1
      have h2 := mul_le_mul_of_nonneg_left h1 hpos.le
      have h3 : p x * (q x / p x - 1) = q x - p x := by field_simp
      linarith
  have h := Finset.sum_le_sum fun x (_ : x ∈ (Finset.univ : Finset X)) => hterm x
  rw [Finset.sum_sub_distrib] at h
  unfold klDivFin
  linarith

section Bracket

variable [Nonempty X]

theorem zRatio_pos (μ₀ g : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (β : ℝ) : 0 < zRatio μ₀ g β :=
  Finset.sum_pos (fun y _ => mul_pos (hμ₀ y) (Real.exp_pos _)) Finset.univ_nonempty

theorem tilt_pos (μ₀ g : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (β : ℝ) (x : X) : 0 < tilt μ₀ g β x :=
  div_pos (mul_pos (hμ₀ x) (Real.exp_pos _)) (zRatio_pos μ₀ g hμ₀ β)

theorem sum_tilt (μ₀ g : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (β : ℝ) : ∑ x, tilt μ₀ g β x = 1 := by
  unfold tilt
  rw [← Finset.sum_div]
  exact div_self (zRatio_pos μ₀ g hμ₀ β).ne'

theorem log_tilt (μ₀ g : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (β : ℝ) (x : X) :
    Real.log (tilt μ₀ g β x) = Real.log (μ₀ x) - β * g x - Real.log (zRatio μ₀ g β) := by
  unfold tilt
  rw [Real.log_div (mul_pos (hμ₀ x) (Real.exp_pos _)).ne' (zRatio_pos μ₀ g hμ₀ β).ne',
    Real.log_mul (hμ₀ x).ne' (Real.exp_pos _).ne', Real.log_exp]
  ring

/-- `KL(μ₀‖μ_g) = β E_{μ₀} g + ln (Z_g / Z_0)`. -/
theorem kl_model_true (μ₀ g : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (hμ₀1 : ∑ x, μ₀ x = 1) (β : ℝ) :
    klDivFin μ₀ (tilt μ₀ g β) = β * ∑ x, μ₀ x * g x + Real.log (zRatio μ₀ g β) := by
  have hterm : ∀ x, μ₀ x * (Real.log (μ₀ x) - Real.log (tilt μ₀ g β x)) =
      β * (μ₀ x * g x) + μ₀ x * Real.log (zRatio μ₀ g β) := by
    intro x
    rw [log_tilt μ₀ g hμ₀ β x]
    ring
  unfold klDivFin
  rw [Finset.sum_congr rfl fun x _ => hterm x, Finset.sum_add_distrib, ← Finset.mul_sum,
    ← Finset.sum_mul, hμ₀1, one_mul]

/-- `KL(μ_g‖μ₀) = -β E_{μ_g} g - ln (Z_g / Z_0)`. -/
theorem kl_true_model (μ₀ g : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (β : ℝ) :
    klDivFin (tilt μ₀ g β) μ₀ =
      -β * ∑ x, tilt μ₀ g β x * g x - Real.log (zRatio μ₀ g β) := by
  have hterm : ∀ x, tilt μ₀ g β x * (Real.log (tilt μ₀ g β x) - Real.log (μ₀ x)) =
      -β * (tilt μ₀ g β x * g x) - tilt μ₀ g β x * Real.log (zRatio μ₀ g β) := by
    intro x
    rw [log_tilt μ₀ g hμ₀ β x]
    ring
  unfold klDivFin
  rw [Finset.sum_congr rfl fun x _ => hterm x, Finset.sum_sub_distrib, ← Finset.mul_sum,
    ← Finset.sum_mul, sum_tilt μ₀ g hμ₀ β, one_mul]

/-- **Theorem 5 (two-sided perturbation bracket).**  For every `g` and every real `β`:
`-β E_{μ₀} g ≤ ln (Z_g/Z_0) ≤ -β E_{μ_g} g`, and the width of the bracket is the symmetrised
divergence `KL(μ₀‖μ_g) + KL(μ_g‖μ₀)`. -/
theorem theorem5_bracket (μ₀ g : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (hμ₀1 : ∑ x, μ₀ x = 1) (β : ℝ) :
    -β * ∑ x, μ₀ x * g x ≤ Real.log (zRatio μ₀ g β) ∧
    Real.log (zRatio μ₀ g β) ≤ -β * ∑ x, tilt μ₀ g β x * g x ∧
    (-β * ∑ x, tilt μ₀ g β x * g x) - (-β * ∑ x, μ₀ x * g x) =
      klDivFin μ₀ (tilt μ₀ g β) + klDivFin (tilt μ₀ g β) μ₀ := by
  have h1 := kl_model_true μ₀ g hμ₀ hμ₀1 β
  have h2 := kl_true_model μ₀ g hμ₀ β
  have hsum := sum_tilt μ₀ g hμ₀ β
  have n1 := klDivFin_nonneg μ₀ (tilt μ₀ g β) (fun x => (hμ₀ x).le) (tilt_pos μ₀ g hμ₀ β)
    (le_of_eq (hsum.trans hμ₀1.symm))
  have n2 := klDivFin_nonneg (tilt μ₀ g β) μ₀ (fun x => (tilt_pos μ₀ g hμ₀ β x).le) hμ₀
    (le_of_eq (hμ₀1.trans hsum.symm))
  refine ⟨by linarith, by linarith, by linarith⟩

/-! ### Proposition 9: a caloric curve brackets `ln Z` -/

/-- Partition function `Z(β) = ∑ x, exp (-β E x)` of the energy `E`. -/
def partitionAt (E : X → ℝ) (β : ℝ) : ℝ := ∑ x, Real.exp (-β * E x)

/-- Gibbs measure at inverse temperature `β`. -/
def gibbsAt (E : X → ℝ) (β : ℝ) (x : X) : ℝ := Real.exp (-β * E x) / partitionAt E β

/-- Mean energy `U(β) = E_{μ_β} E`. -/
def meanEnergy (E : X → ℝ) (β : ℝ) : ℝ := ∑ x, gibbsAt E β x * E x

theorem partitionAt_pos (E : X → ℝ) (β : ℝ) : 0 < partitionAt E β :=
  Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty

theorem gibbsAt_pos (E : X → ℝ) (β : ℝ) (x : X) : 0 < gibbsAt E β x :=
  div_pos (Real.exp_pos _) (partitionAt_pos E β)

theorem sum_gibbsAt (E : X → ℝ) (β : ℝ) : ∑ x, gibbsAt E β x = 1 := by
  unfold gibbsAt
  rw [← Finset.sum_div]
  exact div_self (partitionAt_pos E β).ne'

omit [Nonempty X] in
/-- `E_{μ_β} exp (-δ E) = Z(β + δ) / Z(β)`. -/
theorem zRatio_gibbsAt (E : X → ℝ) (β δ : ℝ) :
    zRatio (gibbsAt E β) E δ = partitionAt E (β + δ) / partitionAt E β := by
  unfold zRatio gibbsAt partitionAt
  rw [Finset.sum_div]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [div_mul_eq_mul_div, ← Real.exp_add]
  congr 2
  ring

/-- Tilting `μ_β` by `exp (-δ E)` gives `μ_{β + δ}`. -/
theorem tilt_gibbsAt (E : X → ℝ) (β δ : ℝ) (x : X) :
    tilt (gibbsAt E β) E δ x = gibbsAt E (β + δ) x := by
  have hZ := (partitionAt_pos E β).ne'
  have hZ' := (partitionAt_pos E (β + δ)).ne'
  unfold tilt
  rw [zRatio_gibbsAt]
  unfold gibbsAt
  have he : Real.exp (-(β + δ) * E x) = Real.exp (-β * E x) * Real.exp (-δ * E x) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [he]
  field_simp

/-- **Proposition 9, one step.**  For all real `β`, `δ`:
`-δ U(β) ≤ ln Z(β + δ) - ln Z(β) ≤ -δ U(β + δ)`. -/
theorem logZ_step (E : X → ℝ) (β δ : ℝ) :
    -δ * meanEnergy E β ≤ Real.log (partitionAt E (β + δ)) - Real.log (partitionAt E β) ∧
      Real.log (partitionAt E (β + δ)) - Real.log (partitionAt E β) ≤
        -δ * meanEnergy E (β + δ) := by
  have h := theorem5_bracket (gibbsAt E β) E (gibbsAt_pos E β) (sum_gibbsAt E β) δ
  rw [zRatio_gibbsAt, Real.log_div (partitionAt_pos E (β + δ)).ne' (partitionAt_pos E β).ne']
    at h
  have hU : ∑ x, tilt (gibbsAt E β) E δ x * E x = meanEnergy E (β + δ) := by
    unfold meanEnergy
    exact Finset.sum_congr rfl fun x _ => by rw [tilt_gibbsAt]
  rw [hU] at h
  exact ⟨h.1, h.2.1⟩

/-- **The mean energy is non-increasing in `β`.** -/
theorem meanEnergy_anti (E : X → ℝ) {β β' : ℝ} (h : β ≤ β') :
    meanEnergy E β' ≤ meanEnergy E β := by
  have hs := logZ_step E β (β' - β)
  rw [add_sub_cancel] at hs
  rcases h.eq_or_lt with heq | hlt
  · rw [heq]
  · have hpos : 0 < β' - β := sub_pos.mpr hlt
    have h1 : -(β' - β) * meanEnergy E β ≤ -(β' - β) * meanEnergy E β' := hs.1.trans hs.2
    nlinarith

/-- **Proposition 9 (a caloric curve determines `ln Z`).**  For any inverse temperatures
`b 0, b 1, …, b m`:
`-∑_j (b_{j+1} - b_j) U(b_j) ≤ ln Z(b_m) - ln Z(b_0) ≤ -∑_j (b_{j+1} - b_j) U(b_{j+1})`. -/
theorem caloric_bracket (E : X → ℝ) (b : ℕ → ℝ) (m : ℕ) :
    -∑ j ∈ Finset.range m, (b (j + 1) - b j) * meanEnergy E (b j) ≤
        Real.log (partitionAt E (b m)) - Real.log (partitionAt E (b 0)) ∧
      Real.log (partitionAt E (b m)) - Real.log (partitionAt E (b 0)) ≤
        -∑ j ∈ Finset.range m, (b (j + 1) - b j) * meanEnergy E (b (j + 1)) := by
  have htel : ∑ j ∈ Finset.range m,
      (Real.log (partitionAt E (b (j + 1))) - Real.log (partitionAt E (b j))) =
        Real.log (partitionAt E (b m)) - Real.log (partitionAt E (b 0)) :=
    Finset.sum_range_sub (fun j => Real.log (partitionAt E (b j))) m
  have hstep : ∀ j, -(b (j + 1) - b j) * meanEnergy E (b j) ≤
      Real.log (partitionAt E (b (j + 1))) - Real.log (partitionAt E (b j)) ∧
      Real.log (partitionAt E (b (j + 1))) - Real.log (partitionAt E (b j)) ≤
        -(b (j + 1) - b j) * meanEnergy E (b (j + 1)) := by
    intro j
    have h := logZ_step E (b j) (b (j + 1) - b j)
    rw [add_sub_cancel] at h
    exact h
  rw [← htel, ← Finset.sum_neg_distrib, ← Finset.sum_neg_distrib]
  constructor
  · refine Finset.sum_le_sum fun j _ => ?_
    have := (hstep j).1
    linarith
  · refine Finset.sum_le_sum fun j _ => ?_
    have := (hstep j).2
    linarith

/-- **Width of the caloric bracket.**  For increasing inverse temperatures with steps at most
`D`, the two ends of `caloric_bracket` differ by at most `D · (U(b_0) - U(b_m))`. -/
theorem caloric_bracket_width (E : X → ℝ) (b : ℕ → ℝ) (m : ℕ) {D : ℝ}
    (hmono : ∀ j, b j ≤ b (j + 1)) (hD : ∀ j, b (j + 1) - b j ≤ D) :
    (-∑ j ∈ Finset.range m, (b (j + 1) - b j) * meanEnergy E (b (j + 1))) -
        (-∑ j ∈ Finset.range m, (b (j + 1) - b j) * meanEnergy E (b j)) ≤
      D * (meanEnergy E (b 0) - meanEnergy E (b m)) := by
  have htel : ∑ j ∈ Finset.range m, (meanEnergy E (b j) - meanEnergy E (b (j + 1))) =
      meanEnergy E (b 0) - meanEnergy E (b m) :=
    Finset.sum_range_sub' (fun j => meanEnergy E (b j)) m
  have hsum : (-∑ j ∈ Finset.range m, (b (j + 1) - b j) * meanEnergy E (b (j + 1))) -
        (-∑ j ∈ Finset.range m, (b (j + 1) - b j) * meanEnergy E (b j)) =
      ∑ j ∈ Finset.range m,
        (b (j + 1) - b j) * (meanEnergy E (b j) - meanEnergy E (b (j + 1))) := by
    rw [← Finset.sum_neg_distrib, ← Finset.sum_neg_distrib, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun j _ => by ring
  rw [hsum, ← htel, Finset.mul_sum]
  refine Finset.sum_le_sum fun j _ => ?_
  have h1 : 0 ≤ meanEnergy E (b j) - meanEnergy E (b (j + 1)) :=
    sub_nonneg.mpr (meanEnergy_anti E (hmono j))
  exact mul_le_mul_of_nonneg_right (hD j) h1

end Bracket

end ScienceL1

end

#print axioms ScienceL1.zRatio_eq_partition_ratio
#print axioms ScienceL1.kl_model_true
#print axioms ScienceL1.kl_true_model
#print axioms ScienceL1.theorem5_bracket
#print axioms ScienceL1.logZ_step
#print axioms ScienceL1.meanEnergy_anti
#print axioms ScienceL1.caloric_bracket
#print axioms ScienceL1.caloric_bracket_width
