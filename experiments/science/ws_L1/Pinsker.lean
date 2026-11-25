import Mathlib

/-!
# Pinsker's inequality on a finite type

Science division, workstream L1.  Mathlib `v4.31.0` has no Pinsker inequality (no file of the
library mentions it).  None of the division's statements needs it — Theorem 7 uses only the
symmetrised inequality proved in `MaxEntStability.lean` — but the note quotes it, so it is
proved here for completeness and for reuse.

* `kemperman_scalar` — for `a ≥ 0`, `b > 0`:
  `3 (a - b)² ≤ (2a + 4b) · (a (log a - log b) - a + b)`.
* `pinsker` — for a probability vector `p ≥ 0` and a positive probability vector `q` on a finite
  type: `2 · TV(p,q)² ≤ KL(p‖q)`, with `TV = ½ ∑ |p - q|` and `KL = ∑ p (log p - log q)`.
* `pinsker_tv_le` — `TV(p,q) ≤ √(KL(p‖q) / 2)`.

Proof (Kemperman): the function `G(t) = (2t² + 4t) log t - (5t² - 4t - 1)` vanishes at `1` and
has derivative `4 ((t + 1) log t - 2 (t - 1))`, which has the sign of `t - 1`
(`two_mul_sub_div_add_le_log_sub`); so `G ≥ 0` on `(0, ∞)`, which is the scalar inequality.
Cauchy–Schwarz with the weights `(2p + 4q)/3` finishes.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL1

open Finset

/-! ### The scalar inequality -/

/-- `2 (a - b) / (a + b) ≤ log a - log b` for `0 < b ≤ a` (repeated from
`MaxEntStability.lean`). -/
theorem two_mul_sub_div_add_le_log_sub {a b : ℝ} (hb : 0 < b) (hab : b ≤ a) :
    2 * (a - b) / (a + b) ≤ Real.log a - Real.log b := by
  have ha : 0 < a := lt_of_lt_of_le hb hab
  have hsum : 0 < a + b := add_pos ha hb
  have hsum' : a + b ≠ 0 := hsum.ne'
  obtain ⟨x, hx⟩ : ∃ x : ℝ, x = (a - b) / (a + b) := ⟨_, rfl⟩
  have hx0 : 0 ≤ x := by
    rw [hx]
    exact div_nonneg (sub_nonneg.mpr hab) hsum.le
  have hx1 : x < 1 := by
    rw [hx, div_lt_one hsum]
    linarith
  have habs : |x| < 1 := by
    rw [abs_of_nonneg hx0]
    exact hx1
  have hs := Real.hasSum_log_sub_log_of_abs_lt_one habs
  have h0 : 2 * (1 / (2 * ((0 : ℕ) : ℝ) + 1)) * x ^ (2 * 0 + 1) ≤
      Real.log (1 + x) - Real.log (1 - x) :=
    le_hasSum hs 0 fun j _ =>
      mul_nonneg (mul_nonneg zero_le_two (one_div_nonneg.mpr (by positivity)))
        (pow_nonneg hx0 _)
  have h1 : 2 * x ≤ Real.log (1 + x) - Real.log (1 - x) := by simpa using h0
  have e1 : 1 + x = 2 * a / (a + b) := by
    rw [hx]
    field_simp
    ring
  have e2 : 1 - x = 2 * b / (a + b) := by
    rw [hx]
    field_simp
    ring
  have e3 : Real.log (1 + x) - Real.log (1 - x) = Real.log a - Real.log b := by
    rw [e1, e2, Real.log_div (mul_pos two_pos ha).ne' hsum',
      Real.log_div (mul_pos two_pos hb).ne' hsum',
      Real.log_mul two_ne_zero ha.ne', Real.log_mul two_ne_zero hb.ne']
    ring
  have e4 : 2 * (a - b) / (a + b) = 2 * x := by
    rw [hx]
    ring
  rw [e4, ← e3]
  exact h1

/-- Kemperman's auxiliary function `G(t) = (2t² + 4t) log t - (5t² - 4t - 1)`. -/
def kempG (t : ℝ) : ℝ := (2 * t ^ 2 + 4 * t) * Real.log t - (5 * t ^ 2 - 4 * t - 1)

theorem kempG_hasDerivAt {x : ℝ} (hx : 0 < x) :
    HasDerivAt kempG (4 * ((x + 1) * Real.log x - 2 * (x - 1))) x := by
  have hne : x ≠ 0 := hx.ne'
  have a : HasDerivAt (fun t : ℝ => t ^ 2) (2 * x) x := by
    simpa using hasDerivAt_pow 2 x
  have b : HasDerivAt (fun t : ℝ => t) 1 x := hasDerivAt_id' x
  have hp : HasDerivAt (fun t : ℝ => 2 * t ^ 2 + 4 * t) (2 * (2 * x) + 4 * 1) x :=
    (a.const_mul 2).add (b.const_mul 4)
  have hq : HasDerivAt (fun t : ℝ => 5 * t ^ 2 - 4 * t - 1) (5 * (2 * x) - 4 * 1) x :=
    ((a.const_mul 5).sub (b.const_mul 4)).sub_const 1
  have h : HasDerivAt kempG
      ((2 * (2 * x) + 4 * 1) * Real.log x + (2 * x ^ 2 + 4 * x) * x⁻¹ -
        (5 * (2 * x) - 4 * 1)) x :=
    (hp.mul (Real.hasDerivAt_log hne)).sub hq
  refine h.congr_deriv ?_
  field_simp
  ring

theorem kempG_one : kempG 1 = 0 := by
  unfold kempG
  rw [Real.log_one]
  norm_num

/-- `G ≥ 0` on `(0, ∞)`. -/
theorem kempG_nonneg {t : ℝ} (ht : 0 < t) : 0 ≤ kempG t := by
  rcases le_total 1 t with h1 | h1
  · -- monotone on `[1, ∞)`
    have hmono : MonotoneOn kempG (Set.Ici 1) := by
      refine monotoneOn_of_deriv_nonneg (convex_Ici 1)
        (fun x hx => (kempG_hasDerivAt (lt_of_lt_of_le one_pos hx)).continuousAt.continuousWithinAt)
        (fun x hx => ?_) (fun x hx => ?_)
      · rw [interior_Ici] at hx
        exact (kempG_hasDerivAt (lt_trans one_pos hx)).differentiableAt.differentiableWithinAt
      · rw [interior_Ici] at hx
        have hx0 : 0 < x := lt_trans one_pos hx
        rw [(kempG_hasDerivAt hx0).deriv]
        have h := two_mul_sub_div_add_le_log_sub one_pos (le_of_lt hx)
        rw [Real.log_one, sub_zero, div_le_iff₀ (by linarith)] at h
        nlinarith
    have := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr h1) h1
    rw [kempG_one] at this
    exact this
  · -- antitone on `(0, 1]`
    have hanti : AntitoneOn kempG (Set.Ioc 0 1) := by
      refine antitoneOn_of_deriv_nonpos (convex_Ioc 0 1)
        (fun x hx => (kempG_hasDerivAt hx.1).continuousAt.continuousWithinAt)
        (fun x hx => ?_) (fun x hx => ?_)
      · rw [interior_Ioc] at hx
        exact (kempG_hasDerivAt hx.1).differentiableAt.differentiableWithinAt
      · rw [interior_Ioc] at hx
        rw [(kempG_hasDerivAt hx.1).deriv]
        have h := two_mul_sub_div_add_le_log_sub hx.1 (le_of_lt hx.2)
        rw [Real.log_one, zero_sub, div_le_iff₀ (by linarith [hx.1])] at h
        nlinarith
    have := hanti (Set.mem_Ioc.mpr ⟨ht, h1⟩) (Set.mem_Ioc.mpr ⟨one_pos, le_rfl⟩) h1
    rw [kempG_one] at this
    exact this

/-- **Kemperman's scalar inequality.**  For `a ≥ 0`, `b > 0`:
`3 (a - b)² ≤ (2a + 4b) (a (log a - log b) - a + b)`. -/
theorem kemperman_scalar {a b : ℝ} (ha : 0 ≤ a) (hb : 0 < b) :
    3 * (a - b) ^ 2 ≤ (2 * a + 4 * b) * (a * (Real.log a - Real.log b) - a + b) := by
  rcases ha.eq_or_lt with h0 | hpos
  · rw [← h0]
    nlinarith [sq_nonneg b]
  · have hG := kempG_nonneg (div_pos hpos hb)
    unfold kempG at hG
    rw [Real.log_div hpos.ne' hb.ne'] at hG
    have hbne : b ≠ 0 := hb.ne'
    have e : (2 * (a / b) ^ 2 + 4 * (a / b)) * (Real.log a - Real.log b) -
        (5 * (a / b) ^ 2 - 4 * (a / b) - 1) =
        ((2 * a ^ 2 + 4 * a * b) * (Real.log a - Real.log b) -
          (5 * a ^ 2 - 4 * a * b - b ^ 2)) / b ^ 2 := by
      field_simp
    rw [e, le_div_iff₀ (by positivity), zero_mul] at hG
    nlinarith

/-! ### Pinsker's inequality -/

variable {X : Type*} [Fintype X]

/-- Relative entropy `KL(p‖q) = ∑ p (log p - log q)` on a finite type. -/
def klDivFin (p q : X → ℝ) : ℝ := ∑ x, p x * (Real.log (p x) - Real.log (q x))

/-- Total variation distance `TV(p,q) = ½ ∑ |p - q|`. -/
def tvDist (p q : X → ℝ) : ℝ := 1 / 2 * ∑ x, |p x - q x|

/-- **Pinsker's inequality on a finite type.**  For a probability vector `p ≥ 0` and a positive
probability vector `q`:  `2 · TV(p,q)² ≤ KL(p‖q)`. -/
theorem pinsker (p q : X → ℝ) (hp : ∀ x, 0 ≤ p x) (hq : ∀ x, 0 < q x)
    (hp1 : ∑ x, p x = 1) (hq1 : ∑ x, q x = 1) :
    2 * tvDist p q ^ 2 ≤ klDivFin p q := by
  have hw : ∀ x, 0 < 2 * p x + 4 * q x := fun x => by nlinarith [hp x, hq x]
  have hCS : (∑ x, |p x - q x|) ^ 2 ≤
      (∑ x, 3 * (p x - q x) ^ 2 / (2 * p x + 4 * q x)) * ∑ x, (2 * p x + 4 * q x) / 3 :=
    Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul Finset.univ
      (fun x _ => div_nonneg (mul_nonneg (by norm_num) (sq_nonneg _)) (hw x).le)
      (fun x _ => div_nonneg (hw x).le (by norm_num))
      (fun x _ => by
        show |p x - q x| ^ 2 ≤
          3 * (p x - q x) ^ 2 / (2 * p x + 4 * q x) * ((2 * p x + 4 * q x) / 3)
        have hne := (hw x).ne'
        rw [sq_abs]
        refine le_of_eq ?_
        field_simp)
  have hsum2 : ∑ x, (2 * p x + 4 * q x) / 3 = 2 := by
    rw [← Finset.sum_div, Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, hp1, hq1]
    norm_num
  have hpt : ∀ x, 3 * (p x - q x) ^ 2 / (2 * p x + 4 * q x) ≤
      p x * (Real.log (p x) - Real.log (q x)) - p x + q x := by
    intro x
    rw [div_le_iff₀ (hw x)]
    have h := kemperman_scalar (hp x) (hq x)
    linarith
  have hsum3 : ∑ x, 3 * (p x - q x) ^ 2 / (2 * p x + 4 * q x) ≤ klDivFin p q := by
    have h := Finset.sum_le_sum fun x (_ : x ∈ (Finset.univ : Finset X)) => hpt x
    rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, hp1, hq1] at h
    unfold klDivFin
    linarith
  have e' : 2 * tvDist p q ^ 2 = (∑ x, |p x - q x|) ^ 2 / 2 := by
    unfold tvDist
    ring
  rw [hsum2] at hCS
  rw [e']
  linarith

/-- Pinsker's inequality in the form `TV(p,q) ≤ √(KL(p‖q) / 2)`. -/
theorem pinsker_tv_le (p q : X → ℝ) (hp : ∀ x, 0 ≤ p x) (hq : ∀ x, 0 < q x)
    (hp1 : ∑ x, p x = 1) (hq1 : ∑ x, q x = 1) :
    tvDist p q ≤ Real.sqrt (klDivFin p q / 2) := by
  have h := pinsker p q hp hq hp1 hq1
  refine Real.le_sqrt_of_sq_le ?_
  linarith

end ScienceL1

end

#print axioms ScienceL1.kemperman_scalar
#print axioms ScienceL1.pinsker
#print axioms ScienceL1.pinsker_tv_le
