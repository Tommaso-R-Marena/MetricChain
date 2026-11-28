import Mathlib

/-!
# The flag inequality (small-slope limit)

Phase II (adaptive hierarchy), `docs/phase2_hierarchy/HIERARCHY_REPORT.md` §7.1, Proposition G.

In the small-slope limit a hidden type `Y*` of a flag of hidden directions is compared with an anchor in
the region that the penultimate batch sees.  With `Δ ≥ 0` the excess of the coordinate of `Y*` in the
last revealed direction over the anchor's and `ρ ≥ 1/2` the norm of its unrevealed part, the proof of
Proposition G reduces to

    2 √(Δ² + (ρ − 1/2)²) ≤ Δ² + Δ/(2ρ) + ρ²,

with equality at the plain dip (`Δ = 0`, `ρ = 1`) and at the bulk of a flat histogram (`Δ = ρ = 1/2`).
This file proves it:

* `cubic_nonpos` — `16ρ³ − 8ρ² − 6ρ − 1 ≤ 0` when `8ρ⁴ − 8ρ² + 1 < 0`, `ρ ≥ 1/2`;
* `quad_nonneg` — `16ρ⁴X² + (8ρ⁴ − 8ρ² + 1)X + (ρ−1)²(ρ² + 2ρ − 1) ≥ 0` for `X ≥ 0`, `ρ ≥ 1/2`
  (by the sign of the linear coefficient, or else by the discriminant, which factors as
  `−(2ρ−1)³(16ρ³ − 8ρ² − 6ρ − 1)`);
* `flag_sq` — the squared form in the variable `t = Δ/(2ρ)`;
* `flag_ineq` — the inequality as stated.

Not formalised: the limit model itself and the reduction of Proposition G to this inequality.
-/

namespace MetricChain.FlagInequality

/-- The cubic `16ρ³ − 8ρ² − 6ρ − 1` is nonpositive whenever `8ρ⁴ − 8ρ² + 1 < 0` and `ρ ≥ 1/2`. -/
theorem cubic_nonpos (ρ : ℝ) (hρ : 1 / 2 ≤ ρ) (hb : 8 * ρ ^ 4 - 8 * ρ ^ 2 + 1 < 0) :
    16 * ρ ^ 3 - 8 * ρ ^ 2 - 6 * ρ - 1 ≤ 0 := by
  have hρ1 : ρ ≤ 16 / 17 := by
    by_contra hcon
    push Not at hcon
    nlinarith [mul_pos (show (0:ℝ) < ρ by linarith) (show (0:ℝ) < ρ by linarith),
      mul_self_nonneg (ρ ^ 2 - 1 / 2), sq_nonneg (ρ - 16 / 17), mul_pos (show (0:ℝ) < ρ - 16/17 by linarith) (show (0:ℝ) < ρ by linarith)]
  -- 2ρ·q = 4·b + w,  w = −16ρ³ + 20ρ² − 2ρ − 4 = −(16ρ(ρ − 5/8)² + 4 − (17/4)ρ) ≤ 0 for ρ ≤ 16/17
  have hw : -16 * ρ ^ 3 + 20 * ρ ^ 2 - 2 * ρ - 4 ≤ 0 := by
    nlinarith [mul_nonneg (show (0:ℝ) ≤ ρ by linarith) (sq_nonneg (ρ - 5 / 8))]
  have h2 : 2 * ρ * (16 * ρ ^ 3 - 8 * ρ ^ 2 - 6 * ρ - 1) ≤ 0 := by nlinarith
  have hpos : (0:ℝ) < 2 * ρ := by linarith
  by_contra hcon
  push Not at hcon
  have := mul_pos hpos hcon
  linarith

/-- The quadratic in `X = t²` behind the flag inequality. -/
theorem quad_nonneg (ρ X : ℝ) (hρ : 1 / 2 ≤ ρ) (hX : 0 ≤ X) :
    0 ≤ 16 * ρ ^ 4 * X ^ 2 + (8 * ρ ^ 4 - 8 * ρ ^ 2 + 1) * X + (ρ - 1) ^ 2 * (ρ ^ 2 + 2 * ρ - 1) := by
  have hc : 0 ≤ (ρ - 1) ^ 2 * (ρ ^ 2 + 2 * ρ - 1) := by
    apply mul_nonneg (sq_nonneg _)
    nlinarith
  by_cases hb : 0 ≤ 8 * ρ ^ 4 - 8 * ρ ^ 2 + 1
  · have h1 : 0 ≤ 16 * ρ ^ 4 * X ^ 2 := by positivity
    have h2 : 0 ≤ (8 * ρ ^ 4 - 8 * ρ ^ 2 + 1) * X := mul_nonneg hb hX
    linarith
  · push Not at hb
    have hq := cubic_nonpos ρ hρ hb
    -- 64ρ⁴·c − b² = −(2ρ−1)³·q ≥ 0
    have hdisc : 0 ≤ 64 * ρ ^ 4 * ((ρ - 1) ^ 2 * (ρ ^ 2 + 2 * ρ - 1)) - (8 * ρ ^ 4 - 8 * ρ ^ 2 + 1) ^ 2 := by
      have hfac : 64 * ρ ^ 4 * ((ρ - 1) ^ 2 * (ρ ^ 2 + 2 * ρ - 1)) - (8 * ρ ^ 4 - 8 * ρ ^ 2 + 1) ^ 2
          = -((2 * ρ - 1) ^ 3 * (16 * ρ ^ 3 - 8 * ρ ^ 2 - 6 * ρ - 1)) := by ring
      rw [hfac]
      have h3 : 0 ≤ (2 * ρ - 1) ^ 3 := by
        apply pow_nonneg; linarith
      nlinarith [mul_nonneg h3 (neg_nonneg.mpr hq)]
    have hρ4 : (0:ℝ) < 64 * ρ ^ 4 := by positivity
    -- 64ρ⁴·(aX² + bX + c) = (32ρ⁴X + b)² + (64ρ⁴c − b²) ≥ 0  with a = 16ρ⁴
    have hmain : 0 ≤ 64 * ρ ^ 4 * (16 * ρ ^ 4 * X ^ 2 + (8 * ρ ^ 4 - 8 * ρ ^ 2 + 1) * X
        + (ρ - 1) ^ 2 * (ρ ^ 2 + 2 * ρ - 1)) := by
      nlinarith [sq_nonneg (32 * ρ ^ 4 * X + (8 * ρ ^ 4 - 8 * ρ ^ 2 + 1))]
    by_contra hcon
    push Not at hcon
    have := mul_neg_of_pos_of_neg hρ4 hcon
    linarith

/-- **The flag inequality** (Proposition G of the report, with `Δ = 2ρt`):
`4(Δ² + (ρ − 1/2)²) ≤ (Δ² + Δ/(2ρ) + ρ²)²` for `Δ ≥ 0`, `ρ ≥ 1/2`. -/
theorem flag_sq (ρ t : ℝ) (hρ : 1 / 2 ≤ ρ) (ht : 0 ≤ t) :
    4 * ((2 * ρ * t) ^ 2 + (ρ - 1 / 2) ^ 2) ≤ ((2 * ρ * t) ^ 2 + t + ρ ^ 2) ^ 2 := by
  have hq := quad_nonneg ρ (t ^ 2) hρ (sq_nonneg t)
  have hρ0 : (0:ℝ) ≤ ρ := by linarith
  have hcross : 0 ≤ 2 * ρ ^ 2 * t * (2 * t - 1) ^ 2 := by positivity
  nlinarith [hq, hcross]

/-- **The flag inequality.**  For `Δ ≥ 0` and `ρ ≥ 1/2`:
`2 √(Δ² + (ρ − 1/2)²) ≤ Δ² + Δ/(2ρ) + ρ²`. -/
theorem flag_ineq (Δ ρ : ℝ) (hΔ : 0 ≤ Δ) (hρ : 1 / 2 ≤ ρ) :
    2 * Real.sqrt (Δ ^ 2 + (ρ - 1 / 2) ^ 2) ≤ Δ ^ 2 + Δ / (2 * ρ) + ρ ^ 2 := by
  have hρ0 : (0:ℝ) < ρ := by linarith
  have ht : 0 ≤ Δ / (2 * ρ) := by positivity
  have h4 := flag_sq ρ (Δ / (2 * ρ)) hρ ht
  have hΔeq : 2 * ρ * (Δ / (2 * ρ)) = Δ := by field_simp
  rw [hΔeq] at h4
  have hR : 0 ≤ (Δ ^ 2 + Δ / (2 * ρ) + ρ ^ 2) / 2 := by positivity
  have hs : Real.sqrt (Δ ^ 2 + (ρ - 1 / 2) ^ 2) ≤ (Δ ^ 2 + Δ / (2 * ρ) + ρ ^ 2) / 2 := by
    apply Real.sqrt_le_iff.mpr
    constructor
    · exact hR
    · nlinarith [h4]
  linarith

end MetricChain.FlagInequality
