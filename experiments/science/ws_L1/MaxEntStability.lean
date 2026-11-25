import Mathlib

/-!
# Theorem 7: stability of maximum-entropy refinement

Science division, workstream L1.  Source: `docs/science/INFERENCE_LIMITS.md` §6, Theorem 7.

Setting of the note: `X` finite, `μ₀` of full support, features `Φ k`, true ensemble
`μ ∝ μ₀ exp (-β (λ·Φ + r))`, `ω = osc r`, and `ν` the I-projection of `μ₀` on
`{E Φ = E_μ Φ}`, which the note's proof uses in the form `ν ∝ μ₀ exp (-β λ'·Φ)` with
`E_ν Φ = E_μ Φ`.  Claims: (i) `KL(μ‖ν) + KL(ν‖μ) = β (E_ν r - E_μ r)`; (ii) `TV(μ,ν) ≤ βω/4`;
(iii) `KL(μ‖ν) + KL(ν‖μ) ≤ (βω)²/4`; (iv) `|E_μ ψ - E_ν ψ| ≤ osc ψ · βω/4`;
(v) `0 ≤ KL(μ‖μ₀) - KL(ν‖μ₀) = KL(μ‖ν) ≤ (βω)²/4`.

## What is proved

All five claims, with **no Pinsker hypothesis** (`theorem7`).  Mathlib `v4.31.0` has no
Pinsker inequality and no total-variation distance; but Theorem 7 only needs the
*symmetrised* inequality `4 TV² ≤ KL(p‖q) + KL(q‖p)`, which has a direct proof
(`symm_pinsker`): `(a - b)(log a - log b) ≥ 2 (a - b)² / (a + b)` pointwise
(`sq_div_add_le_mul_log`, from `log t ≥ 2 (t - 1) / (t + 1)` for `t ≥ 1`) and Cauchy–Schwarz.

* `symmKL_eq_of_logRatio` — the algebraic core of (i): if
  `log μ - log ν = a·Φ - β r + const` and the `Φ`-means agree, then
  `KL(μ‖ν) + KL(ν‖μ) = β (E_ν r - E_μ r)`.
* `symm_pinsker` — `4 TV² ≤ KL(p‖q) + KL(q‖p)` for positive probability vectors.
* `abs_sum_sub_le_osc_mul_tv` — `|E_p r - E_q r| ≤ (hi - lo) · TV(p,q)` for `lo ≤ r ≤ hi`.
* `pinsker_closing` — the closing step `4 T² ≤ J`, `J ≤ ω T`, **`0 ≤ ω`** ⟹ `T ≤ ω/4`,
  `J ≤ ω²/4`; `pinsker_closing_needs_nonneg` shows that `0 ≤ ω` cannot be dropped.
* `pythagoras_expFam` — `KL(μ‖μ₀) - KL(ν‖μ₀) = KL(μ‖ν)` for `ν ∝ μ₀ exp (-E)` and `E_μ E = E_ν E`.
* `theorem7_i_energies`, `theorem7_ii_iii_energies` — (i)–(iii) for two exponential tilts of
  `μ₀` whose energies differ by `b·Φ + β r`.
* `theorem7` — (i)–(v) in the note's form.
* `expFam_isIProjection` — the refined ensemble of exponential form with matching moments
  minimises `KL(·‖μ₀)` among all probability vectors with those moments (so it *is* the
  I-projection).
* `tv_bounded_perturbation` — the case without features, a non-vacuous instance:
  `TV(μ₀ exp (-β r)/Z, μ₀/Z₀) ≤ β (hi - lo)/4`.

## Differences from the note

* `ν` is *assumed* to be of exponential form with matching `Φ`-means (as the note's proof uses
  it).  That the I-projection has this form (Csiszár) is not formalised; the converse is
  (`expFam_isIProjection`).
* `ω` is any `hi - lo` with `lo ≤ r ≤ hi`; `β ≥ 0` is assumed (implicit in the note).
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL1

open Finset

variable {X K : Type*} [Fintype X] [Fintype K]

/-! ### Definitions -/

/-- Relative entropy `KL(p‖q) = ∑ p (log p - log q)` on a finite type. -/
def klDivFin (p q : X → ℝ) : ℝ := ∑ x, p x * (Real.log (p x) - Real.log (q x))

/-- Total variation distance `TV(p,q) = ½ ∑ |p - q|`. -/
def tvDist (p q : X → ℝ) : ℝ := 1 / 2 * ∑ x, |p x - q x|

/-- Normalising constant of the exponential tilt `μ₀ exp (-E)`. -/
def expFamZ (μ₀ E : X → ℝ) : ℝ := ∑ y, μ₀ y * Real.exp (-E y)

/-- The exponential tilt `x ↦ μ₀ x exp (-E x) / Z` of the reference `μ₀` by the energy `E`. -/
def expFam (μ₀ E : X → ℝ) (x : X) : ℝ := μ₀ x * Real.exp (-E x) / expFamZ μ₀ E

theorem tvDist_nonneg (p q : X → ℝ) : 0 ≤ tvDist p q :=
  mul_nonneg (by norm_num) (Finset.sum_nonneg fun _ _ => abs_nonneg _)

theorem tvDist_comm (p q : X → ℝ) : tvDist p q = tvDist q p := by
  unfold tvDist
  congr 1
  exact Finset.sum_congr rfl fun x _ => abs_sub_comm _ _

/-! ### Relative entropy: symmetrisation and Gibbs' inequality -/

/-- `KL(p‖q) + KL(q‖p) = ∑ (p - q)(log p - log q)`. -/
theorem klDivFin_add_symm (p q : X → ℝ) :
    klDivFin p q + klDivFin q p = ∑ x, (p x - q x) * (Real.log (p x) - Real.log (q x)) := by
  unfold klDivFin
  rw [← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl fun x _ => by ring

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

/-! ### (i) The identity for the symmetrised divergence -/

/-- **Algebraic core of Theorem 7(i).**  `μ`, `ν` of total mass `1` with equal `Φ`-means and
`log μ - log ν = ∑ k, a k * Φ k - β r + c`.  Then
`KL(μ‖ν) + KL(ν‖μ) = β (E_ν r - E_μ r)`. -/
theorem symmKL_eq_of_logRatio (μ ν : X → ℝ) (hμ1 : ∑ x, μ x = 1) (hν1 : ∑ x, ν x = 1)
    (Φ : K → X → ℝ) (hmom : ∀ k, ∑ x, μ x * Φ k x = ∑ x, ν x * Φ k x)
    (a : K → ℝ) (c β : ℝ) (r : X → ℝ)
    (hlog : ∀ x, Real.log (μ x) - Real.log (ν x) = ∑ k, a k * Φ k x - β * r x + c) :
    klDivFin μ ν + klDivFin ν μ = β * (∑ x, ν x * r x - ∑ x, μ x * r x) := by
  rw [klDivFin_add_symm]
  have h1 : ∑ x, (μ x - ν x) * ∑ k, a k * Φ k x = 0 := by
    calc ∑ x, (μ x - ν x) * ∑ k, a k * Φ k x
        = ∑ x, ∑ k, a k * (μ x * Φ k x - ν x * Φ k x) := by
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [Finset.mul_sum]
          exact Finset.sum_congr rfl fun k _ => by ring
      _ = ∑ k, ∑ x, a k * (μ x * Φ k x - ν x * Φ k x) := Finset.sum_comm
      _ = ∑ k, a k * (∑ x, μ x * Φ k x - ∑ x, ν x * Φ k x) := by
          refine Finset.sum_congr rfl fun k _ => ?_
          rw [← Finset.mul_sum, Finset.sum_sub_distrib]
      _ = 0 := by
          refine Finset.sum_eq_zero fun k _ => ?_
          rw [hmom k, sub_self, mul_zero]
  have h2 : ∑ x, (μ x - ν x) * r x = ∑ x, μ x * r x - ∑ x, ν x * r x := by
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun x _ => sub_mul _ _ _
  have h3 : ∑ x, (μ x - ν x) = 0 := by
    rw [Finset.sum_sub_distrib, hμ1, hν1, sub_self]
  have hsplit : ∑ x, ((μ x - ν x) * ∑ k, a k * Φ k x - β * ((μ x - ν x) * r x) +
        c * (μ x - ν x)) =
      ∑ x, (μ x - ν x) * ∑ k, a k * Φ k x - ∑ x, β * ((μ x - ν x) * r x) +
        ∑ x, c * (μ x - ν x) := by
    rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  calc ∑ x, (μ x - ν x) * (Real.log (μ x) - Real.log (ν x))
      = ∑ x, ((μ x - ν x) * ∑ k, a k * Φ k x - β * ((μ x - ν x) * r x) +
          c * (μ x - ν x)) := by
        refine Finset.sum_congr rfl fun x _ => ?_
        rw [hlog x]
        ring
    _ = ∑ x, (μ x - ν x) * ∑ k, a k * Φ k x - ∑ x, β * ((μ x - ν x) * r x) +
          ∑ x, c * (μ x - ν x) := hsplit
    _ = β * (∑ x, ν x * r x - ∑ x, μ x * r x) := by
        rw [← Finset.mul_sum, ← Finset.mul_sum, h1, h2, h3]
        ring

/-! ### The symmetrised Pinsker inequality -/

/-- `2 (a - b) / (a + b) ≤ log a - log b` for `0 < b ≤ a` (first term of the series of
`log ((1 + x) / (1 - x))`, `x = (a - b) / (a + b)`). -/
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
    rw [e1, e2, Real.log_div (mul_pos two_pos ha).ne' hsum', Real.log_div (mul_pos two_pos hb).ne' hsum',
      Real.log_mul two_ne_zero ha.ne', Real.log_mul two_ne_zero hb.ne']
    ring
  have e4 : 2 * (a - b) / (a + b) = 2 * x := by
    rw [hx]
    ring
  rw [e4, ← e3]
  exact h1

/-- `2 (a - b)² / (a + b) ≤ (a - b)(log a - log b)` for `a, b > 0`. -/
theorem sq_div_add_le_mul_log {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    2 * (a - b) ^ 2 / (a + b) ≤ (a - b) * (Real.log a - Real.log b) := by
  rcases le_total b a with h | h
  · have h1 := two_mul_sub_div_add_le_log_sub hb h
    have h2 := mul_le_mul_of_nonneg_left h1 (sub_nonneg.mpr h)
    have e : (a - b) * (2 * (a - b) / (a + b)) = 2 * (a - b) ^ 2 / (a + b) := by ring
    linarith
  · have h1 := two_mul_sub_div_add_le_log_sub ha h
    have h2 := mul_le_mul_of_nonneg_left h1 (sub_nonneg.mpr h)
    have e : (b - a) * (2 * (b - a) / (b + a)) = 2 * (a - b) ^ 2 / (a + b) := by ring
    have e' : (b - a) * (Real.log b - Real.log a) = (a - b) * (Real.log a - Real.log b) := by
      ring
    linarith

/-- **Symmetrised Pinsker inequality.**  For positive probability vectors on a finite type,
`4 TV(p,q)² ≤ KL(p‖q) + KL(q‖p)`.  (This is what two applications of Pinsker's inequality
would give; the direct proof needs no Pinsker.) -/
theorem symm_pinsker (p q : X → ℝ) (hp : ∀ x, 0 < p x) (hq : ∀ x, 0 < q x)
    (hp1 : ∑ x, p x = 1) (hq1 : ∑ x, q x = 1) :
    4 * tvDist p q ^ 2 ≤ klDivFin p q + klDivFin q p := by
  rw [klDivFin_add_symm]
  have hCS : (∑ x, |p x - q x|) ^ 2 ≤
      (∑ x, (p x - q x) ^ 2 / (p x + q x)) * ∑ x, (p x + q x) :=
    Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul Finset.univ
      (fun x _ => div_nonneg (sq_nonneg _) (add_pos (hp x) (hq x)).le)
      (fun x _ => (add_pos (hp x) (hq x)).le)
      (fun x _ => by
        show |p x - q x| ^ 2 ≤ (p x - q x) ^ 2 / (p x + q x) * (p x + q x)
        have hne := (add_pos (hp x) (hq x)).ne'
        rw [sq_abs]
        refine le_of_eq ?_
        field_simp)
  have hsum2 : ∑ x, (p x + q x) = 2 := by
    rw [Finset.sum_add_distrib, hp1, hq1]
    norm_num
  have hpt : ∑ x, 2 * (p x - q x) ^ 2 / (p x + q x) ≤
      ∑ x, (p x - q x) * (Real.log (p x) - Real.log (q x)) :=
    Finset.sum_le_sum fun x _ => sq_div_add_le_mul_log (hp x) (hq x)
  have e : ∑ x, 2 * (p x - q x) ^ 2 / (p x + q x) =
      2 * ∑ x, (p x - q x) ^ 2 / (p x + q x) := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun x _ => by ring
  have e' : 4 * tvDist p q ^ 2 = (∑ x, |p x - q x|) ^ 2 := by
    unfold tvDist
    ring
  rw [hsum2] at hCS
  linarith

/-! ### Means against total variation -/

/-- `|E_p r - E_q r| ≤ (hi - lo) · TV(p,q)` for `lo ≤ r ≤ hi` and `p`, `q` of equal total
mass `1`. -/
theorem abs_sum_sub_le_osc_mul_tv (p q : X → ℝ) (hp1 : ∑ x, p x = 1) (hq1 : ∑ x, q x = 1)
    (r : X → ℝ) {lo hi : ℝ} (hr : ∀ x, lo ≤ r x ∧ r x ≤ hi) :
    |∑ x, p x * r x - ∑ x, q x * r x| ≤ (hi - lo) * tvDist p q := by
  have e : ∑ x, p x * r x - ∑ x, q x * r x =
      ∑ x, (p x - q x) * (r x - (lo + hi) / 2) := by
    have h0 : ∑ x, (p x - q x) * ((lo + hi) / 2) = 0 := by
      rw [← Finset.sum_mul, Finset.sum_sub_distrib, hp1, hq1, sub_self, zero_mul]
    have h1 : ∑ x, (p x - q x) * (r x - (lo + hi) / 2) =
        ∑ x, p x * r x - ∑ x, q x * r x - ∑ x, (p x - q x) * ((lo + hi) / 2) := by
      rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun x _ => by ring
    rw [h1, h0, sub_zero]
  rw [e]
  calc |∑ x, (p x - q x) * (r x - (lo + hi) / 2)|
      ≤ ∑ x, |(p x - q x) * (r x - (lo + hi) / 2)| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ x, |p x - q x| * ((hi - lo) / 2) := by
        refine Finset.sum_le_sum fun x _ => ?_
        rw [abs_mul]
        refine mul_le_mul_of_nonneg_left ?_ (abs_nonneg _)
        rw [abs_le]
        constructor <;> linarith [(hr x).1, (hr x).2]
    _ = (hi - lo) * tvDist p q := by
        unfold tvDist
        rw [← Finset.sum_mul]
        ring

/-! ### The closing step -/

/-- **The closing step of Theorem 7.**  If `4 T² ≤ J`, `J ≤ ω T` and `0 ≤ ω`, then `T ≤ ω / 4`
and `J ≤ ω² / 4`. -/
theorem pinsker_closing {T J ω : ℝ} (hω : 0 ≤ ω) (h1 : 4 * T ^ 2 ≤ J) (h2 : J ≤ ω * T) :
    T ≤ ω / 4 ∧ J ≤ ω ^ 2 / 4 := by
  have hT : T ≤ ω / 4 := by
    by_contra hlt
    have hlt' : ω / 4 < T := not_le.mp hlt
    have hTpos : 0 < T := by linarith
    nlinarith [mul_pos hTpos (sub_pos.mpr hlt')]
  refine ⟨hT, ?_⟩
  nlinarith [mul_le_mul_of_nonneg_left hT hω]

/-- The hypothesis `0 ≤ ω` of `pinsker_closing` cannot be dropped (even with `0 ≤ T`):
`T = J = 0`, `ω = -1`. -/
theorem pinsker_closing_needs_nonneg :
    ∃ T J ω : ℝ, 0 ≤ T ∧ 4 * T ^ 2 ≤ J ∧ J ≤ ω * T ∧ ¬ T ≤ ω / 4 :=
  ⟨0, 0, -1, le_rfl, by norm_num, by norm_num, by norm_num⟩

/-! ### Exponential tilts -/

section Tilt

variable [Nonempty X]

theorem expFamZ_pos (μ₀ E : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) : 0 < expFamZ μ₀ E :=
  Finset.sum_pos (fun y _ => mul_pos (hμ₀ y) (Real.exp_pos _)) Finset.univ_nonempty

theorem expFam_pos (μ₀ E : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (x : X) : 0 < expFam μ₀ E x :=
  div_pos (mul_pos (hμ₀ x) (Real.exp_pos _)) (expFamZ_pos μ₀ E hμ₀)

theorem sum_expFam (μ₀ E : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) : ∑ x, expFam μ₀ E x = 1 := by
  unfold expFam
  rw [← Finset.sum_div]
  exact div_self (expFamZ_pos μ₀ E hμ₀).ne'

theorem log_expFam (μ₀ E : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (x : X) :
    Real.log (expFam μ₀ E x) = Real.log (μ₀ x) - E x - Real.log (expFamZ μ₀ E) := by
  unfold expFam
  rw [Real.log_div (mul_pos (hμ₀ x) (Real.exp_pos _)).ne' (expFamZ_pos μ₀ E hμ₀).ne',
    Real.log_mul (hμ₀ x).ne' (Real.exp_pos _).ne', Real.log_exp]
  ring

/-- **Pythagorean identity for an exponential tilt.**  For `ν = expFam μ₀ E` and any `μ` of
total mass `1` with `E_μ E = E_ν E`:  `KL(μ‖μ₀) - KL(ν‖μ₀) = KL(μ‖ν)`. -/
theorem pythagoras_expFam (μ₀ E : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (μ : X → ℝ)
    (hμ1 : ∑ x, μ x = 1) (hE : ∑ x, μ x * E x = ∑ x, expFam μ₀ E x * E x) :
    klDivFin μ μ₀ - klDivFin (expFam μ₀ E) μ₀ = klDivFin μ (expFam μ₀ E) := by
  have hν1 := sum_expFam μ₀ E hμ₀
  have hlog : ∀ x, Real.log (expFam μ₀ E x) - Real.log (μ₀ x) =
      -E x - Real.log (expFamZ μ₀ E) := fun x => by
    rw [log_expFam μ₀ E hμ₀ x]
    ring
  have h1 : klDivFin μ μ₀ - klDivFin μ (expFam μ₀ E) =
      ∑ x, μ x * (-E x - Real.log (expFamZ μ₀ E)) := by
    unfold klDivFin
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [← hlog x]
    ring
  have h2 : klDivFin (expFam μ₀ E) μ₀ =
      ∑ x, expFam μ₀ E x * (-E x - Real.log (expFamZ μ₀ E)) := by
    unfold klDivFin
    exact Finset.sum_congr rfl fun x _ => by rw [hlog x]
  have h3 : ∀ p : X → ℝ, ∑ x, p x * (-E x - Real.log (expFamZ μ₀ E)) =
      -∑ x, p x * E x - Real.log (expFamZ μ₀ E) * ∑ x, p x := by
    intro p
    rw [Finset.mul_sum, ← Finset.sum_neg_distrib, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun x _ => by ring
  rw [h3 μ, hμ1, hE] at h1
  rw [h3 (expFam μ₀ E), hν1] at h2
  linarith

/-! ### Theorem 7 for two exponential tilts -/

/-- **Theorem 7(i), energy form.**  Two tilts `μ = expFam μ₀ Eμ`, `ν = expFam μ₀ Eν` whose
energies differ by `∑ k, b k * Φ k + β r` and whose `Φ`-means agree satisfy
`KL(μ‖ν) + KL(ν‖μ) = β (E_ν r - E_μ r)`. -/
theorem theorem7_i_energies (μ₀ : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (Eμ Eν : X → ℝ)
    (Φ : K → X → ℝ) (b : K → ℝ) (β : ℝ) (r : X → ℝ)
    (hE : ∀ x, Eμ x - Eν x = ∑ k, b k * Φ k x + β * r x)
    (hmom : ∀ k, ∑ x, expFam μ₀ Eμ x * Φ k x = ∑ x, expFam μ₀ Eν x * Φ k x) :
    klDivFin (expFam μ₀ Eμ) (expFam μ₀ Eν) + klDivFin (expFam μ₀ Eν) (expFam μ₀ Eμ) =
      β * (∑ x, expFam μ₀ Eν x * r x - ∑ x, expFam μ₀ Eμ x * r x) := by
  refine symmKL_eq_of_logRatio _ _ (sum_expFam μ₀ Eμ hμ₀) (sum_expFam μ₀ Eν hμ₀) Φ hmom
    (fun k => -b k) (Real.log (expFamZ μ₀ Eν) - Real.log (expFamZ μ₀ Eμ)) β r ?_
  intro x
  have e : ∑ k, -b k * Φ k x = -∑ k, b k * Φ k x := by
    rw [← Finset.sum_neg_distrib]
    exact Finset.sum_congr rfl fun k _ => by ring
  show Real.log (expFam μ₀ Eμ x) - Real.log (expFam μ₀ Eν x) =
    ∑ k, -b k * Φ k x - β * r x + (Real.log (expFamZ μ₀ Eν) - Real.log (expFamZ μ₀ Eμ))
  rw [log_expFam μ₀ Eμ hμ₀ x, log_expFam μ₀ Eν hμ₀ x, e]
  linarith [hE x]

/-- **Theorem 7(ii)–(iii), energy form.**  If moreover `β ≥ 0` and `lo ≤ r ≤ hi`, then
`TV(μ,ν) ≤ β (hi - lo) / 4` and `KL(μ‖ν) + KL(ν‖μ) ≤ (β (hi - lo))² / 4`. -/
theorem theorem7_ii_iii_energies (μ₀ : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (Eμ Eν : X → ℝ)
    (Φ : K → X → ℝ) (b : K → ℝ) {β : ℝ} (hβ : 0 ≤ β) (r : X → ℝ) {lo hi : ℝ}
    (hr : ∀ x, lo ≤ r x ∧ r x ≤ hi)
    (hE : ∀ x, Eμ x - Eν x = ∑ k, b k * Φ k x + β * r x)
    (hmom : ∀ k, ∑ x, expFam μ₀ Eμ x * Φ k x = ∑ x, expFam μ₀ Eν x * Φ k x) :
    tvDist (expFam μ₀ Eμ) (expFam μ₀ Eν) ≤ β * (hi - lo) / 4 ∧
      klDivFin (expFam μ₀ Eμ) (expFam μ₀ Eν) + klDivFin (expFam μ₀ Eν) (expFam μ₀ Eμ) ≤
        (β * (hi - lo)) ^ 2 / 4 := by
  have hid := theorem7_i_energies μ₀ hμ₀ Eμ Eν Φ b β r hE hmom
  have hP := symm_pinsker (expFam μ₀ Eμ) (expFam μ₀ Eν) (expFam_pos μ₀ Eμ hμ₀)
    (expFam_pos μ₀ Eν hμ₀) (sum_expFam μ₀ Eμ hμ₀) (sum_expFam μ₀ Eν hμ₀)
  have hO := abs_sum_sub_le_osc_mul_tv (expFam μ₀ Eν) (expFam μ₀ Eμ) (sum_expFam μ₀ Eν hμ₀)
    (sum_expFam μ₀ Eμ hμ₀) r hr
  rw [tvDist_comm] at hO
  have hω : 0 ≤ hi - lo := by
    obtain ⟨x⟩ := ‹Nonempty X›
    linarith [(hr x).1, (hr x).2]
  have hJ : klDivFin (expFam μ₀ Eμ) (expFam μ₀ Eν) + klDivFin (expFam μ₀ Eν) (expFam μ₀ Eμ) ≤
      β * (hi - lo) * tvDist (expFam μ₀ Eμ) (expFam μ₀ Eν) := by
    rw [hid]
    have h3 := mul_le_mul_of_nonneg_left ((le_abs_self _).trans hO) hβ
    linarith
  exact pinsker_closing (mul_nonneg hβ hω) hP hJ

/-! ### Theorem 7 in the note's form -/

/-- **Theorem 7 (stability of maximum-entropy refinement).**  `X` finite, `μ₀ > 0`, features
`Φ`, `β ≥ 0`, remainder `r` with `lo ≤ r ≤ hi` (so `ω = osc r ≤ hi - lo`),
`μ ∝ μ₀ exp (-β (λ·Φ + r))` the true ensemble and `ν ∝ μ₀ exp (-β λ'·Φ)` a member of the
exponential family with the same `Φ`-means as `μ` (the maximum-entropy refinement).  Then
(i) `KL(μ‖ν) + KL(ν‖μ) = β (E_ν r - E_μ r)`;
(ii) `TV(μ,ν) ≤ β (hi - lo) / 4`;
(iii) `KL(μ‖ν) + KL(ν‖μ) ≤ (β (hi - lo))² / 4`;
(iv) `|E_μ ψ - E_ν ψ| ≤ (b - a) · β (hi - lo) / 4` for every `ψ` with `a ≤ ψ ≤ b`;
(v) `0 ≤ KL(μ‖μ₀) - KL(ν‖μ₀) = KL(μ‖ν) ≤ (β (hi - lo))² / 4`.
No hypothesis on `|X|`, on the features or on `μ₀` beyond positivity; no Pinsker hypothesis. -/
theorem theorem7 (μ₀ : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (Φ : K → X → ℝ) (lam lam' : K → ℝ)
    (r : X → ℝ) {β : ℝ} (hβ : 0 ≤ β) {lo hi : ℝ} (hr : ∀ x, lo ≤ r x ∧ r x ≤ hi)
    (μ ν : X → ℝ)
    (hμ : μ = expFam μ₀ (fun x => β * (∑ k, lam k * Φ k x + r x)))
    (hν : ν = expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x))
    (hmom : ∀ k, ∑ x, μ x * Φ k x = ∑ x, ν x * Φ k x) :
    (klDivFin μ ν + klDivFin ν μ = β * (∑ x, ν x * r x - ∑ x, μ x * r x)) ∧
    (tvDist μ ν ≤ β * (hi - lo) / 4) ∧
    (klDivFin μ ν + klDivFin ν μ ≤ (β * (hi - lo)) ^ 2 / 4) ∧
    (∀ (ψ : X → ℝ) (a b : ℝ), (∀ x, a ≤ ψ x ∧ ψ x ≤ b) →
      |∑ x, μ x * ψ x - ∑ x, ν x * ψ x| ≤ (b - a) * (β * (hi - lo) / 4)) ∧
    (0 ≤ klDivFin μ μ₀ - klDivFin ν μ₀) ∧
    (klDivFin μ μ₀ - klDivFin ν μ₀ = klDivFin μ ν) ∧
    (klDivFin μ ν ≤ (β * (hi - lo)) ^ 2 / 4) := by
  subst hμ hν
  have hE : ∀ x, β * (∑ k, lam k * Φ k x + r x) - β * ∑ k, lam' k * Φ k x =
      ∑ k, β * (lam k - lam' k) * Φ k x + β * r x := by
    intro x
    have e : ∑ k, β * (lam k - lam' k) * Φ k x =
        β * ∑ k, lam k * Φ k x - β * ∑ k, lam' k * Φ k x := by
      rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun k _ => by ring
    rw [e]
    ring
  have hi' := theorem7_i_energies μ₀ hμ₀ (fun x => β * (∑ k, lam k * Φ k x + r x))
    (fun x => β * ∑ k, lam' k * Φ k x) Φ (fun k => β * (lam k - lam' k)) β r hE hmom
  have hii := theorem7_ii_iii_energies μ₀ hμ₀ (fun x => β * (∑ k, lam k * Φ k x + r x))
    (fun x => β * ∑ k, lam' k * Φ k x) Φ (fun k => β * (lam k - lam' k)) hβ r hr hE hmom
  have hμpos := expFam_pos μ₀ (fun x => β * (∑ k, lam k * Φ k x + r x)) hμ₀
  have hνpos := expFam_pos μ₀ (fun x => β * ∑ k, lam' k * Φ k x) hμ₀
  have hμ1 := sum_expFam μ₀ (fun x => β * (∑ k, lam k * Φ k x + r x)) hμ₀
  have hν1 := sum_expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x) hμ₀
  -- the mean of the refined energy is determined by the feature means
  have hEmean : ∀ p : X → ℝ, ∑ x, p x * (β * ∑ k, lam' k * Φ k x) =
      β * ∑ k, lam' k * ∑ x, p x * Φ k x := by
    intro p
    calc ∑ x, p x * (β * ∑ k, lam' k * Φ k x)
        = ∑ x, ∑ k, β * (lam' k * (p x * Φ k x)) := by
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [Finset.mul_sum, Finset.mul_sum]
          exact Finset.sum_congr rfl fun k _ => by ring
      _ = ∑ k, ∑ x, β * (lam' k * (p x * Φ k x)) := Finset.sum_comm
      _ = β * ∑ k, lam' k * ∑ x, p x * Φ k x := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun k _ => ?_
          rw [Finset.mul_sum, Finset.mul_sum]
  have hEeq : ∑ x, expFam μ₀ (fun x => β * (∑ k, lam k * Φ k x + r x)) x *
        (β * ∑ k, lam' k * Φ k x) =
      ∑ x, expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x) x * (β * ∑ k, lam' k * Φ k x) := by
    rw [hEmean, hEmean]
    congr 1
    exact Finset.sum_congr rfl fun k _ => by rw [hmom k]
  have hpyth := pythagoras_expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x) hμ₀
    (expFam μ₀ (fun x => β * (∑ k, lam k * Φ k x + r x))) hμ1 hEeq
  have hKLμν := klDivFin_nonneg _ _ (fun x => (hμpos x).le) hνpos (le_of_eq (hν1.trans hμ1.symm))
  have hKLνμ := klDivFin_nonneg _ _ (fun x => (hνpos x).le) hμpos (le_of_eq (hμ1.trans hν1.symm))
  refine ⟨hi', hii.1, hii.2, ?_, ?_, hpyth, ?_⟩
  · intro ψ a b hψ
    have hO := abs_sum_sub_le_osc_mul_tv _ _ hμ1 hν1 ψ hψ
    have hba : 0 ≤ b - a := by
      obtain ⟨x⟩ := ‹Nonempty X›
      linarith [(hψ x).1, (hψ x).2]
    exact hO.trans (mul_le_mul_of_nonneg_left hii.1 hba)
  · rw [hpyth]
    exact hKLμν
  · linarith [hii.2]

/-- **The refined ensemble is the I-projection.**  A member `ν ∝ μ₀ exp (-β λ'·Φ)` of the
exponential family minimises `KL(·‖μ₀)` among all probability vectors with the same
`Φ`-means. -/
theorem expFam_isIProjection (μ₀ : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (Φ : K → X → ℝ) (lam' : K → ℝ)
    (β : ℝ) (μ' : X → ℝ) (hμ' : ∀ x, 0 ≤ μ' x) (hμ'1 : ∑ x, μ' x = 1)
    (hmom : ∀ k, ∑ x, μ' x * Φ k x =
      ∑ x, expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x) x * Φ k x) :
    klDivFin (expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x)) μ₀ ≤ klDivFin μ' μ₀ := by
  have hνpos := expFam_pos μ₀ (fun x => β * ∑ k, lam' k * Φ k x) hμ₀
  have hν1 := sum_expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x) hμ₀
  have hEmean : ∀ p : X → ℝ, ∑ x, p x * (β * ∑ k, lam' k * Φ k x) =
      β * ∑ k, lam' k * ∑ x, p x * Φ k x := by
    intro p
    calc ∑ x, p x * (β * ∑ k, lam' k * Φ k x)
        = ∑ x, ∑ k, β * (lam' k * (p x * Φ k x)) := by
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [Finset.mul_sum, Finset.mul_sum]
          exact Finset.sum_congr rfl fun k _ => by ring
      _ = ∑ k, ∑ x, β * (lam' k * (p x * Φ k x)) := Finset.sum_comm
      _ = β * ∑ k, lam' k * ∑ x, p x * Φ k x := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun k _ => ?_
          rw [Finset.mul_sum, Finset.mul_sum]
  have hEeq : ∑ x, μ' x * (β * ∑ k, lam' k * Φ k x) =
      ∑ x, expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x) x * (β * ∑ k, lam' k * Φ k x) := by
    rw [hEmean, hEmean]
    congr 1
    exact Finset.sum_congr rfl fun k _ => by rw [hmom k]
  have hpyth := pythagoras_expFam μ₀ (fun x => β * ∑ k, lam' k * Φ k x) hμ₀ μ' hμ'1 hEeq
  have hKL := klDivFin_nonneg μ' _ hμ' hνpos (le_of_eq (hν1.trans hμ'1.symm))
  linarith

/-- **No features: bounded perturbation of a Gibbs measure.**  A non-vacuous instance of
Theorem 7(ii): the ensembles `∝ μ₀ exp (-β r)` and `∝ μ₀` are within total variation
`β (hi - lo) / 4` when `lo ≤ r ≤ hi`. -/
theorem tv_bounded_perturbation (μ₀ : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (r : X → ℝ) {β : ℝ}
    (hβ : 0 ≤ β) {lo hi : ℝ} (hr : ∀ x, lo ≤ r x ∧ r x ≤ hi) :
    tvDist (expFam μ₀ (fun x => β * r x)) (expFam μ₀ (fun _ => 0)) ≤ β * (hi - lo) / 4 :=
  (theorem7_ii_iii_energies μ₀ hμ₀ (fun x => β * r x) (fun _ => 0)
    (fun (_ : Fin 0) (_ : X) => (0 : ℝ)) (fun _ => 0) hβ r hr (fun x => by simp)
    (fun k => k.elim0)).1

end Tilt

end ScienceL1

end

#print axioms ScienceL1.symmKL_eq_of_logRatio
#print axioms ScienceL1.symm_pinsker
#print axioms ScienceL1.abs_sum_sub_le_osc_mul_tv
#print axioms ScienceL1.pinsker_closing
#print axioms ScienceL1.pinsker_closing_needs_nonneg
#print axioms ScienceL1.pythagoras_expFam
#print axioms ScienceL1.theorem7_i_energies
#print axioms ScienceL1.theorem7_ii_iii_energies
#print axioms ScienceL1.theorem7
#print axioms ScienceL1.expFam_isIProjection
#print axioms ScienceL1.tv_bounded_perturbation
