import proofs.Frontiers.BoundedAccuracy

/-!
# The level recursion acts on lines: minorant lines (Lemma L) and majorant lines (Lemma M)

Theory report §11.18 (the remark "a rate for the recursion") and §11.19; workstream R,
`docs/workstreams/R_brief.md` §2.2 and §2.6 (this file: Lean task LD,
`docs/workstreams/LD_brief.md`).  The level recursion on exponent functions is

  `R[T](g) = inf_{0<φ<1, 0<β<g} sup_{γ≥β} [ min(γ, φ θ_na((g−β)/φ)) + (1−φ) T(γ/(1−φ)) ]`,
  `T₁ = θ_na`,   `T_{k+1} = min(T_k, R[T_k])`

(`BoundedAccuracy.Rstep` and `BoundedAccuracy.exactRec`; `exactRec θna k` is `T_{k+1}`).  This
file proves what one step of the recursion does to a *line* `B − σ x`, from below and from
above, and the first consequences.  Like `HintRecursion.lean` it is analysis of the recursion
and nothing about algorithms.

**Lemma L (minorant lines), R_brief §2.2.**

* (L1, L2) `line_le_Rstep`: if `θna ≥ 0`, `0 ≤ σ ≤ σ'`, `B − σ x ≤ T x` for all `x > 0`, and
  `B − (1 − σ) θna e ≤ σ' e` for all `e > 0`, then `B − σ' g ≤ R[T](g)` for all `g > 0` (`T`
  bounded above, so that the infimum in `Rstep` is over a nonempty set); `line_le_min_Rstep`:
  the same for `min(T, R[T])`, the step of the recursion.
* (L3) `lines_le_exactRec`: iteration.  A minorant line `(B, s 0)` of `θna` and slopes with
  `s j ≤ s (j+1)`, `B − (1 − s j) θna e ≤ s (j+1) e` for `j < K` give
  `B − s k x ≤ exactRec θna k x` for `k ≤ K`.  Hence `exists_sub_le_exactRec` (for every `η > 0`
  some `x > 0` has `B − η ≤ exactRec θna K x`) and `le_sSup_exactRec`
  (`B ≤ sup exactRec θna K`): the exponent `τ_{K+1} = sup T_{K+1}` of level `K + 1` at accuracy
  zero is at least `B`.
* (L4) The Gaussian pair, `gaussNa x = (1 − √(min x 1))²`: the least admissible new slope is
  the Möbius map `σ' = B (1 − σ)/(1 − σ − B)` (`gauss_slope_map`, `gauss_slope_map_least`;
  `σ + B < 1` is needed with strict inequality), the tangent lines of `gaussNa` are
  `B − (B/(1 − B)) x` (`gauss_tangent_line`, the image of the flat line `σ = 0`), and for
  `B ≥ 1/4` the map moves no slope downwards (`gauss_slope_le`); so the orbit of the tangent
  slope gives minorant lines of the exact recursion for as long as it stays below `1 − B`
  (`gauss_lines_le_exactRec`).
* (L5) Witnesses (the hypotheses are not vacuous): `B = 3/8` with the slopes `3/5, 6` gives
  `3/8 − 6 x ≤ exactRec gaussNa 1 x` (`gauss_level_two_minorant`, `gauss_level_two_ge`: the
  second level has exponent at least `3/8 > 1/4 = h` at accuracy zero), and `B = 3/10` with the
  slopes `3/7, 12/19, 21/13` gives `3/10 − (21/13) x ≤ exactRec gaussNa 2 x`
  (`gauss_level_three_minorant`, `gauss_level_three_ge`).

**Lemma M (majorant lines on a range, one step), R_brief §2.6.**

* (M1) `StepLE.monotoneS_step`: if `T` is nonincreasing, `T ≤ M` on `(0, R]`, `x + M x` is
  nondecreasing on `(0, R]`, `θna` is continuous at `g/φ`, `μ = φ θna(g/φ) > 0` and
  `X = μ/(1 − φ) ≤ R`, then every `T'` with `StepLE θna T T'` has `T' g ≤ (1 − φ)(X + M X)`.
  (`stepLE_Rstep`: `T' = R[T]` is such a function when `θna, T ≥ 0`.)
* (M2) `StepLE.line_step`, `StepLE.line_step_slope`: for the line `M x = B − σ x`, `σ ≤ 1`, this
  is `T' g ≤ (1 − φ) B + (1 − σ) φ θna(g/φ) = B − σ' g` with `σ' = (B − (1 − σ) θna e)/e`,
  `e = g/φ`; `StepLE.line_step_rate`: at a fixed outer rate `e` the majorant line `(B, σ)` on
  `(0, R]` becomes the majorant line `(B, σ')` on `(0, R e/(θna e + R)]`; `exactRec_line_step`:
  the same along the exact recursion.
* Witness: `gauss_level_two_majorant`, `exactRec gaussNa 1 g ≤ 1 − 4 g` for `0 < g ≤ 1/5`, from
  the majorant line `1 − x` of `gaussNa` on `(0, 1]` at the outer rate `e = 1/4`.

**Not formalised.**  The analysis of the slope map — how many levels a line needs before its
slope leaves the range in which the map is finite, hence the rate of `τ_k − h` and its constant
— is a paper argument (workstream R), as are the slope map and the tangent lines of the cube,
and the monotonicity of the orbit for `B < 1/4`.  On the side of the upper bound only the single
step is here: the monotone hull, the rule at accuracy zero and the families of lines that an
upper bound for `τ_k` needs are on paper.  The identification of the recursion with algorithms
is on paper (theory report §11.18–§11.19).
-/

namespace MetricChain
namespace LineDynamics

open MetricChain.HintRecursion MetricChain.BoundedAccuracy Set

/-! ### Lemma L: minorant lines -/

private theorem scale_line {p B σ γ : ℝ} (hp : p ≠ 0) :
    p * (B - σ * (γ / p)) = p * B - σ * γ := by
  field_simp

/-- **Lemma L: a minorant line survives one step, with a new slope.**  Let `θna ≥ 0`,
`0 ≤ σ ≤ σ'`, and let the line `B − σ x` lie below `T` on `(0, ∞)`.  If
`B − (1 − σ) θna e ≤ σ' e` for every outer rate `e > 0`, then the line `B − σ' g` lies below
`R[T]`.  (The bound `T ≤ C` only makes the infimum in `Rstep` an infimum over a nonempty set.)
Proof: for parameters `(φ, β)` put `μ = φ θna((g − β)/φ)` and evaluate the bracket at
`γ₀ = max β μ`; it is at least `μ + (1 − φ) B − σ γ₀`, and the hypothesis at `e = (g − β)/φ`,
multiplied by `φ`, reads `φ B − (1 − σ) μ ≤ σ' (g − β)`. -/
theorem line_le_Rstep {θna T : ℝ → ℝ} {B σ σ' C : ℝ}
    (hθ : ∀ x, 0 < x → 0 ≤ θna x) (hσ : 0 ≤ σ) (hσσ' : σ ≤ σ')
    (hT : ∀ x, 0 < x → B - σ * x ≤ T x) (hTC : ∀ x, 0 < x → T x ≤ C)
    (hmap : ∀ e, 0 < e → B - (1 - σ) * θna e ≤ σ' * e)
    {g : ℝ} (hg : 0 < g) : B - σ' * g ≤ Rstep θna T g := by
  apply le_csInf (admissible_nonempty hTC hg)
  rintro B₀ ⟨φ, β, hβ, hβg, hφ0, hφ1, h⟩
  have h1 : 0 < 1 - φ := by linarith
  have he : 0 < (g - β) / φ := div_pos (by linarith) hφ0
  -- the outer exponent `μ`, and the slope map at the outer rate multiplied by `φ`
  obtain ⟨μ, hμ⟩ : ∃ μ, μ = φ * θna ((g - β) / φ) := ⟨_, rfl⟩
  have hμ0 : 0 ≤ μ := by rw [hμ]; exact mul_nonneg hφ0.le (hθ _ he)
  have hm : φ * B - (1 - σ) * μ ≤ σ' * (g - β) := by
    have h2 := mul_le_mul_of_nonneg_left (hmap _ he) hφ0.le
    have h3 : φ * (σ' * ((g - β) / φ)) = σ' * (g - β) := by field_simp
    rw [h3] at h2
    rw [hμ]
    linarith
  rw [← hμ] at h
  -- the bracket at `γ₀ = max β μ`
  have hγ0 : 0 < max β μ := lt_of_lt_of_le hβ (le_max_left _ _)
  have hkey := h (max β μ) (le_max_left _ _)
  rw [min_eq_right (le_max_right _ _)] at hkey
  have hTl : (1 - φ) * B - σ * max β μ ≤ (1 - φ) * T (max β μ / (1 - φ)) := by
    have h2 := mul_le_mul_of_nonneg_left (hT _ (div_pos hγ0 h1)) h1.le
    rwa [scale_line h1.ne'] at h2
  rcases le_total β μ with hc | hc
  · -- `β ≤ μ`: `B₀ ≥ (1 − φ) B + (1 − σ) μ ≥ B − σ' (g − β)`
    rw [max_eq_right hc] at hTl hkey
    nlinarith [mul_nonneg (hσ.trans hσσ') hβ.le]
  · -- `μ ≤ β`: `B₀ ≥ μ + (1 − φ) B − σ β ≥ (1 − σ) μ + (1 − φ) B − σ β ≥ B − σ' g + (σ' − σ) β`
    rw [max_eq_left hc] at hTl hkey
    nlinarith [mul_nonneg hσ hμ0, mul_nonneg (sub_nonneg.mpr hσσ') hβ.le]

/-- **The step of the recursion keeps the line**: under the hypotheses of `line_le_Rstep` the
line `B − σ' g` lies below `min(T, R[T])`. -/
theorem line_le_min_Rstep {θna T : ℝ → ℝ} {B σ σ' C : ℝ}
    (hθ : ∀ x, 0 < x → 0 ≤ θna x) (hσ : 0 ≤ σ) (hσσ' : σ ≤ σ')
    (hT : ∀ x, 0 < x → B - σ * x ≤ T x) (hTC : ∀ x, 0 < x → T x ≤ C)
    (hmap : ∀ e, 0 < e → B - (1 - σ) * θna e ≤ σ' * e)
    {g : ℝ} (hg : 0 < g) : B - σ' * g ≤ min (T g) (Rstep θna T g) := by
  refine le_min ?_ (line_le_Rstep hθ hσ hσσ' hT hTC hmap hg)
  have h1 := hT g hg
  have h2 : σ * g ≤ σ' * g := mul_le_mul_of_nonneg_right hσσ' hg.le
  linarith

/-- Slopes that start nonnegative and do not decrease for `K` steps are nonnegative. -/
theorem slopes_nonneg (s : ℕ → ℝ) (K : ℕ) (hs0 : 0 ≤ s 0)
    (hmono : ∀ j, j < K → s j ≤ s (j + 1)) : ∀ k, k ≤ K → 0 ≤ s k := by
  intro k
  induction k with
  | zero => exact fun _ => hs0
  | succ k ih => exact fun hk => (ih (by omega)).trans (hmono k (by omega))

/-- **Lemma L iterated along the exact recursion.**  Let `θna` be nonnegative, nonincreasing
and bounded, let `B − s 0 · x` be a minorant line of `θna`, and let the slopes satisfy
`s j ≤ s (j+1)` and the slope-map inequality `B − (1 − s j) θna e ≤ s (j+1) e` for `j < K`.  Then
`B − s k · x` is a minorant line of level `k` of the exact recursion, for every `k ≤ K`. -/
theorem lines_le_exactRec {θna : ℝ → ℝ} {B C : ℝ} (s : ℕ → ℝ) (K : ℕ)
    (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hθanti : ∀ x y, 0 < x → x ≤ y → θna y ≤ θna x) (hθC : ∀ x, 0 < x → θna x ≤ C)
    (hs0 : 0 ≤ s 0) (hmono : ∀ j, j < K → s j ≤ s (j + 1))
    (h0 : ∀ x, 0 < x → B - s 0 * x ≤ θna x)
    (hmap : ∀ j, j < K → ∀ e, 0 < e → B - (1 - s j) * θna e ≤ s (j + 1) * e) :
    ∀ k, k ≤ K → ∀ x, 0 < x → B - s k * x ≤ exactRec θna k x := by
  intro k
  induction k with
  | zero => exact fun _ => h0
  | succ k ih =>
    intro hk x hx
    have hk' : k < K := by omega
    show B - s (k + 1) * x ≤ min (exactRec θna k x) (Rstep θna (exactRec θna k) x)
    exact line_le_min_Rstep hθ (slopes_nonneg s K hs0 hmono k hk'.le) (hmono k hk') (ih hk'.le)
      (exactRec_props hθ hθanti hθC k).2.1 (hmap k hk') hx

/-- A function above a line `B − σ x` on `(0, ∞)` comes within any `η > 0` of `B` near zero. -/
theorem exists_sub_le_of_line {T : ℝ → ℝ} {B σ : ℝ} (hT : ∀ x, 0 < x → B - σ * x ≤ T x)
    {η : ℝ} (hη : 0 < η) : ∃ x, 0 < x ∧ B - η ≤ T x := by
  have hpos : 0 < |σ| + 1 := by positivity
  have hx : 0 < η / (|σ| + 1) := div_pos hη hpos
  refine ⟨η / (|σ| + 1), hx, ?_⟩
  have h1 := hT _ hx
  have h2 : σ * (η / (|σ| + 1)) ≤ |σ| * (η / (|σ| + 1)) :=
    mul_le_mul_of_nonneg_right (le_abs_self σ) hx.le
  have h3 : |σ| * (η / (|σ| + 1)) ≤ η := by
    rw [← mul_div_assoc, div_le_iff₀ hpos]
    nlinarith [abs_nonneg σ]
  linarith

/-- **The consequence at accuracy zero.**  Under the hypotheses of `lines_le_exactRec`, level
`K` of the exact recursion comes within any `η > 0` of `B`: for every `η > 0` there is an
accuracy `x > 0` with `B − η ≤ exactRec θna K x`. -/
theorem exists_sub_le_exactRec {θna : ℝ → ℝ} {B C : ℝ} (s : ℕ → ℝ) (K : ℕ)
    (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hθanti : ∀ x y, 0 < x → x ≤ y → θna y ≤ θna x) (hθC : ∀ x, 0 < x → θna x ≤ C)
    (hs0 : 0 ≤ s 0) (hmono : ∀ j, j < K → s j ≤ s (j + 1))
    (h0 : ∀ x, 0 < x → B - s 0 * x ≤ θna x)
    (hmap : ∀ j, j < K → ∀ e, 0 < e → B - (1 - s j) * θna e ≤ s (j + 1) * e)
    {η : ℝ} (hη : 0 < η) : ∃ x, 0 < x ∧ B - η ≤ exactRec θna K x :=
  exists_sub_le_of_line (lines_le_exactRec s K hθ hθanti hθC hs0 hmono h0 hmap K le_rfl) hη

/-- **The exponent at accuracy zero is at least `B`.**  Under the hypotheses of
`lines_le_exactRec`, `B ≤ sup_{x > 0} exactRec θna K x`; in the notation of the theory report,
`τ_{K+1} ≥ B`. -/
theorem le_sSup_exactRec {θna : ℝ → ℝ} {B C : ℝ} (s : ℕ → ℝ) (K : ℕ)
    (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hθanti : ∀ x y, 0 < x → x ≤ y → θna y ≤ θna x) (hθC : ∀ x, 0 < x → θna x ≤ C)
    (hs0 : 0 ≤ s 0) (hmono : ∀ j, j < K → s j ≤ s (j + 1))
    (h0 : ∀ x, 0 < x → B - s 0 * x ≤ θna x)
    (hmap : ∀ j, j < K → ∀ e, 0 < e → B - (1 - s j) * θna e ≤ s (j + 1) * e) :
    B ≤ sSup (exactRec θna K '' Ioi 0) := by
  have hbdd : BddAbove (exactRec θna K '' Ioi 0) :=
    ⟨C, by rintro _ ⟨x, hx, rfl⟩; exact (exactRec_props hθ hθanti hθC K).2.1 x hx⟩
  refine le_of_forall_pos_le_add fun η hη => ?_
  obtain ⟨x, hx, hxB⟩ := exists_sub_le_exactRec s K hθ hθanti hθC hs0 hmono h0 hmap hη
  have h1 : exactRec θna K x ≤ sSup (exactRec θna K '' Ioi 0) := le_csSup hbdd ⟨x, hx, rfl⟩
  linarith

/-! ### The Gaussian pair: the slope map is a Möbius map -/

theorem gaussNa_nonneg (x : ℝ) : 0 ≤ gaussNa x := by
  unfold gaussNa
  positivity

theorem gaussNa_anti {x y : ℝ} (hxy : x ≤ y) : gaussNa y ≤ gaussNa x := by
  unfold gaussNa
  have h1 : Real.sqrt (min x 1) ≤ Real.sqrt (min y 1) :=
    Real.sqrt_le_sqrt (min_le_min hxy le_rfl)
  have h2 : Real.sqrt (min y 1) ≤ 1 := by
    calc Real.sqrt (min y 1) ≤ Real.sqrt 1 := Real.sqrt_le_sqrt (min_le_right _ _)
      _ = 1 := Real.sqrt_one
  exact pow_le_pow_left₀ (by linarith) (by linarith) 2

/-- `gaussNa` in the variable `w = √x ∈ [0, 1]`. -/
theorem gaussNa_sq {w : ℝ} (hw0 : 0 ≤ w) (hw1 : w ≤ 1) : gaussNa (w ^ 2) = (1 - w) ^ 2 := by
  unfold gaussNa
  rw [min_eq_left (by nlinarith), Real.sqrt_sq hw0]

theorem gaussNa_of_one_le {x : ℝ} (hx : 1 ≤ x) : gaussNa x = 0 := by
  unfold gaussNa
  rw [min_eq_right hx, Real.sqrt_one]
  norm_num

private theorem exists_sq_eq {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x ≤ 1) :
    ∃ w : ℝ, 0 ≤ w ∧ w ≤ 1 ∧ w ^ 2 = x := by
  refine ⟨Real.sqrt x, Real.sqrt_nonneg x, ?_, Real.sq_sqrt hx0⟩
  calc Real.sqrt x ≤ Real.sqrt 1 := Real.sqrt_le_sqrt hx1
    _ = 1 := Real.sqrt_one

/-- **The slope map of the Gaussian pair is a Möbius map.**  For `0 ≤ B` and `σ + B < 1` the new
slope `σ' = B (1 − σ)/(1 − σ − B)` satisfies the hypothesis of Lemma L:
`B − (1 − σ) gaussNa e ≤ σ' e` for all `e > 0`.  For `e ≤ 1`, with `w = √e` and `p = 1 − σ`:
`σ' w² + p (1 − w)² − B = (p w − (p − B))²/(p − B)`; for `e ≥ 1`: `gaussNa e = 0` and
`B ≤ σ' ≤ σ' e`. -/
theorem gauss_slope_map {B σ : ℝ} (hB : 0 ≤ B) (hσB : σ + B < 1) :
    ∀ e, 0 < e → B - (1 - σ) * gaussNa e ≤ B * (1 - σ) / (1 - σ - B) * e := by
  intro e he
  have hd : 0 < 1 - σ - B := by linarith
  rcases le_total e 1 with h1 | h1
  · obtain ⟨w, hw0, hw1, rfl⟩ := exists_sq_eq he.le h1
    rw [gaussNa_sq hw0 hw1, div_mul_eq_mul_div, le_div_iff₀ hd]
    nlinarith [sq_nonneg ((1 - σ) * w - (1 - σ - B))]
  · rw [gaussNa_of_one_le h1, mul_zero, sub_zero]
    have h2 : B ≤ B * (1 - σ) / (1 - σ - B) := by
      rw [le_div_iff₀ hd]
      nlinarith [mul_nonneg hB hB]
    nlinarith [mul_nonneg (hB.trans h2) (sub_nonneg.mpr h1)]

/-- The Möbius value is the *least* admissible new slope: every `σ'` that satisfies the
hypothesis of Lemma L for the Gaussian pair is at least `B (1 − σ)/(1 − σ − B)` (there is
equality in `gauss_slope_map` at `e = (1 − B/(1 − σ))²`). -/
theorem gauss_slope_map_least {B σ σ' : ℝ} (hB : 0 ≤ B) (hσB : σ + B < 1)
    (h : ∀ e, 0 < e → B - (1 - σ) * gaussNa e ≤ σ' * e) :
    B * (1 - σ) / (1 - σ - B) ≤ σ' := by
  have hp : 0 < 1 - σ := by linarith
  have hd : 0 < 1 - σ - B := by linarith
  have hw0 : 0 < (1 - σ - B) / (1 - σ) := div_pos hd hp
  have hw1 : (1 - σ - B) / (1 - σ) ≤ 1 := by rw [div_le_one hp]; linarith
  have h1 := h _ (pow_pos hw0 2)
  rw [gaussNa_sq hw0.le hw1] at h1
  have e1 : B - (1 - σ) * (1 - (1 - σ - B) / (1 - σ)) ^ 2 = B * (1 - σ - B) / (1 - σ) := by
    field_simp
    ring
  have e2 : σ' * ((1 - σ - B) / (1 - σ)) ^ 2 = σ' * (1 - σ - B) ^ 2 / (1 - σ) ^ 2 := by
    field_simp
  rw [e1, e2, div_le_div_iff₀ hp (by positivity)] at h1
  rw [div_le_iff₀ hd]
  nlinarith [mul_pos hd hp]

/-- **The tangent lines of `gaussNa`**: `B − (B/(1 − B)) x ≤ (1 − √x)²` (with equality at
`x = (1 − B)²`).  This is `gauss_slope_map` at `σ = 0`: the tangent slope is the image of the
flat line. -/
theorem gauss_tangent_line {B : ℝ} (hB0 : 0 ≤ B) (hB1 : B < 1) :
    ∀ x, 0 < x → B - B / (1 - B) * x ≤ gaussNa x := by
  intro x hx
  have h := gauss_slope_map (σ := 0) hB0 (by linarith) x hx
  simp only [sub_zero, one_mul, mul_one] at h
  linarith

/-- For `B ≥ 1/4` (`1/4` is the value `h` of the hinted exponent at accuracy zero) the Möbius map
moves no slope downwards: `σ' − σ = ((σ − 1/2)² + B − 1/4)/(1 − σ − B) ≥ 0`. -/
theorem gauss_slope_le {B σ : ℝ} (hB : 1 / 4 ≤ B) (hσB : σ + B < 1) :
    σ ≤ B * (1 - σ) / (1 - σ - B) := by
  have hd : 0 < 1 - σ - B := by linarith
  rw [le_div_iff₀ hd]
  nlinarith [sq_nonneg (σ - 1 / 2)]

/-- **The Möbius orbit of a tangent line gives minorant lines of the Gaussian recursion.**
For `1/4 ≤ B < 1` let `s 0 = B/(1 − B)` and `s (j+1) = B (1 − s j)/(1 − s j − B)` for `j < K`, the
slopes `s j`, `j < K`, staying below `1 − B`.  Then `B − s k · x ≤ exactRec gaussNa k x` for all
`k ≤ K`. -/
theorem gauss_lines_le_exactRec {B : ℝ} (hB : 1 / 4 ≤ B) (hB1 : B < 1) (s : ℕ → ℝ) (K : ℕ)
    (hs0 : s 0 = B / (1 - B)) (hreg : ∀ j, j < K → s j + B < 1)
    (hstep : ∀ j, j < K → s (j + 1) = B * (1 - s j) / (1 - s j - B)) :
    ∀ k, k ≤ K → ∀ x, 0 < x → B - s k * x ≤ exactRec gaussNa k x := by
  have hB0 : 0 ≤ B := by linarith
  refine lines_le_exactRec s K (fun x _ => gaussNa_nonneg x) (fun x y _ hxy => gaussNa_anti hxy)
    gaussPair.na_le ?_ ?_ ?_ ?_
  · rw [hs0]
    exact div_nonneg hB0 (by linarith)
  · intro j hj
    rw [hstep j hj]
    exact gauss_slope_le hB (hreg j hj)
  · intro x hx
    rw [hs0]
    exact gauss_tangent_line hB0 hB1 x hx
  · intro j hj e he
    rw [hstep j hj]
    exact gauss_slope_map hB0 (hreg j hj) e he

/-- **Witness, one step.**  `B = 3/8`, slopes `3/5` (tangent line) and `6`: the line
`3/8 − 6 x` lies below the second level `T₂ = exactRec gaussNa 1` of the Gaussian recursion. -/
theorem gauss_level_two_minorant : ∀ x, 0 < x → 3 / 8 - 6 * x ≤ exactRec gaussNa 1 x := by
  have h := gauss_lines_le_exactRec (B := 3 / 8) (by norm_num) (by norm_num)
    (fun j => if j = 0 then 3 / 5 else 6) 1 (by norm_num)
    (by intro j hj; interval_cases j; norm_num)
    (by intro j hj; interval_cases j; norm_num) 1 le_rfl
  simpa using h

/-- **The second level of the Gaussian recursion has exponent at least `3/8` at accuracy
zero** (and `3/8 > 1/4 = h`, the limit of the levels). -/
theorem gauss_level_two_ge :
    ∀ η : ℝ, 0 < η → ∃ x, 0 < x ∧ 3 / 8 - η ≤ exactRec gaussNa 1 x :=
  fun _ hη => exists_sub_le_of_line gauss_level_two_minorant hη

/-- **Witness, two steps.**  `B = 3/10`, slopes `3/7`, `12/19`, `21/13`: the line
`3/10 − (21/13) x` lies below the third level `T₃ = exactRec gaussNa 2`. -/
theorem gauss_level_three_minorant :
    ∀ x, 0 < x → 3 / 10 - 21 / 13 * x ≤ exactRec gaussNa 2 x := by
  have h := gauss_lines_le_exactRec (B := 3 / 10) (by norm_num) (by norm_num)
    (fun j => if j = 0 then 3 / 7 else if j = 1 then 12 / 19 else 21 / 13) 2 (by norm_num)
    (by intro j hj; interval_cases j <;> norm_num)
    (by intro j hj; interval_cases j <;> norm_num) 2 le_rfl
  simpa using h

/-- **The third level of the Gaussian recursion has exponent at least `3/10` at accuracy
zero.** -/
theorem gauss_level_three_ge :
    ∀ η : ℝ, 0 < η → ∃ x, 0 < x ∧ 3 / 10 - η ≤ exactRec gaussNa 2 x :=
  fun _ hη => exists_sub_le_of_line gauss_level_three_minorant hη

/-! ### Lemma M: majorant lines on a range -/

/-- **Lemma M: one step for a majorant with nondecreasing `x + M x` on a range.**  Let `T` be
nonincreasing with `T ≤ M` on `(0, R]`, where `x + M x` is nondecreasing on `(0, R]`.  Let
`g > 0`, `0 < φ < 1`, `θna` continuous at the outer rate `g/φ`, `μ = φ θna(g/φ) > 0` and
`X = μ/(1 − φ) ≤ R`.  Then `T' g ≤ (1 − φ)(X + M X)` for every `T'` below the two-level bound
built on `T`.  (From `StepLE.of_limit`: for `0 < γ ≤ μ` the bracket `γ + (1 − φ) T(γ/(1 − φ))`
is at most `(1 − φ)(y + M y)` with `y = γ/(1 − φ) ≤ X`.) -/
theorem StepLE.monotoneS_step {θna T T' M : ℝ → ℝ} (hs : StepLE θna T T')
    (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x) {R g φ : ℝ}
    (hg : 0 < g) (hφ0 : 0 < φ) (hφ1 : φ < 1)
    (hc : ContinuousAt θna (g / φ)) (hμ : 0 < φ * θna (g / φ))
    (hX : φ * θna (g / φ) / (1 - φ) ≤ R)
    (hTM : ∀ x, 0 < x → x ≤ R → T x ≤ M x)
    (hS : ∀ x y, 0 < x → x ≤ y → y ≤ R → x + M x ≤ y + M y) :
    T' g ≤ (1 - φ) * (φ * θna (g / φ) / (1 - φ) + M (φ * θna (g / φ) / (1 - φ))) := by
  have h1 : 0 < 1 - φ := by linarith
  apply StepLE.of_limit hs hanti hg hφ0 hφ1 hc hμ
  intro γ hγ0 hγ
  have hy0 : 0 < γ / (1 - φ) := div_pos hγ0 h1
  have hyX : γ / (1 - φ) ≤ φ * θna (g / φ) / (1 - φ) := div_le_div_of_nonneg_right hγ h1.le
  have h2 := hTM _ hy0 (hyX.trans hX)
  have h3 := hS _ _ hy0 hyX hX
  have h4 : γ = (1 - φ) * (γ / (1 - φ)) := by field_simp
  have h5 := mul_le_mul_of_nonneg_left h2 h1.le
  have h6 := mul_le_mul_of_nonneg_left h3 h1.le
  linarith

/-- **The line step at a general outer rate.**  If `T x ≤ B − σ x` on `(0, R]` with `σ ≤ 1`, then
under the hypotheses of Lemma M, `T' g ≤ (1 − φ) B + (1 − σ) φ θna(g/φ)`. -/
theorem StepLE.line_step {θna T T' : ℝ → ℝ} (hs : StepLE θna T T')
    (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x) {B σ R g φ : ℝ}
    (hg : 0 < g) (hφ0 : 0 < φ) (hφ1 : φ < 1)
    (hc : ContinuousAt θna (g / φ)) (hμ : 0 < φ * θna (g / φ))
    (hX : φ * θna (g / φ) / (1 - φ) ≤ R)
    (hT : ∀ x, 0 < x → x ≤ R → T x ≤ B - σ * x) (hσ : σ ≤ 1) :
    T' g ≤ (1 - φ) * B + (1 - σ) * (φ * θna (g / φ)) := by
  have h1 : 0 < 1 - φ := by linarith
  have h : T' g ≤ (1 - φ) * (φ * θna (g / φ) / (1 - φ)
      + (B - σ * (φ * θna (g / φ) / (1 - φ)))) :=
    StepLE.monotoneS_step (M := fun x => B - σ * x) hs hanti hg hφ0 hφ1 hc hμ hX hT
      (fun x y _ hxy _ => by
        show x + (B - σ * x) ≤ y + (B - σ * y)
        nlinarith [mul_nonneg (sub_nonneg.mpr hσ) (sub_nonneg.mpr hxy)])
  have e : (1 - φ) * (φ * θna (g / φ) / (1 - φ) + (B - σ * (φ * θna (g / φ) / (1 - φ))))
      = (1 - φ) * B + (1 - σ) * (φ * θna (g / φ)) := by
    field_simp
    ring
  rwa [e] at h

/-- **The line step as a slope map.**  The bound of `StepLE.line_step` written with the outer
rate `e = g/φ`: `T' g ≤ B − σ' g` with the new slope `σ' = (B − (1 − σ) θna e)/e`. -/
theorem StepLE.line_step_slope {θna T T' : ℝ → ℝ} (hs : StepLE θna T T')
    (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x) {B σ R g φ : ℝ}
    (hg : 0 < g) (hφ0 : 0 < φ) (hφ1 : φ < 1)
    (hc : ContinuousAt θna (g / φ)) (hμ : 0 < φ * θna (g / φ))
    (hX : φ * θna (g / φ) / (1 - φ) ≤ R)
    (hT : ∀ x, 0 < x → x ≤ R → T x ≤ B - σ * x) (hσ : σ ≤ 1) :
    T' g ≤ B - ((B - (1 - σ) * θna (g / φ)) / (g / φ)) * g := by
  have h := StepLE.line_step hs hanti hg hφ0 hφ1 hc hμ hX hT hσ
  have e : B - ((B - (1 - σ) * θna (g / φ)) / (g / φ)) * g
      = (1 - φ) * B + (1 - σ) * (φ * θna (g / φ)) := by
    field_simp
    ring
  rwa [e]

/-- **A majorant line on a range becomes a majorant line on a range.**  Fix an outer rate `e`
at which `θna` is continuous and positive.  If `T x ≤ B − σ x` on `(0, R]` with `σ ≤ 1`, then
`T' g ≤ B − σ' g` on `(0, R']` with `σ' = (B − (1 − σ) θna e)/e` and `R' = R e/(θna e + R)`
(the accuracies `g` whose outer fraction `φ = g/e` has `X = g θna e/(e − g) ≤ R`). -/
theorem StepLE.line_step_rate {θna T T' : ℝ → ℝ} (hs : StepLE θna T T')
    (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x) {B σ R e : ℝ}
    (hc : ContinuousAt θna e) (hθe : 0 < θna e) (hR : 0 < R)
    (hT : ∀ x, 0 < x → x ≤ R → T x ≤ B - σ * x) (hσ : σ ≤ 1) :
    ∀ g, 0 < g → g ≤ R * e / (θna e + R) →
      T' g ≤ B - ((B - (1 - σ) * θna e) / e) * g := by
  intro g hg hgR
  have hsum : 0 < θna e + R := by linarith
  have he : 0 < e := by
    by_contra hcon
    have h1 : R * e / (θna e + R) ≤ 0 :=
      div_nonpos_of_nonpos_of_nonneg
        (mul_nonpos_of_nonneg_of_nonpos hR.le (not_lt.mp hcon)) hsum.le
    linarith
  have hgs : g * (θna e + R) ≤ R * e := (le_div_iff₀ hsum).mp hgR
  have hge : g < e := by nlinarith [mul_pos hg hθe]
  have hφ0 : 0 < g / e := div_pos hg he
  have hφ1 : g / e < 1 := (div_lt_one he).mpr hge
  have hgφ : g / (g / e) = e := by field_simp
  have hX : g / e * θna (g / (g / e)) / (1 - g / e) ≤ R := by
    have h1 : 0 < 1 - g / e := by linarith
    rw [hgφ, div_le_iff₀ h1]
    have h2 : g / e * θna e = g * θna e / e := by ring
    have h3 : R * (1 - g / e) = (R * e - R * g) / e := by field_simp
    rw [h2, h3]
    exact div_le_div_of_nonneg_right (by linarith) he.le
  have h := StepLE.line_step_slope hs hanti hg hφ0 hφ1 (by rw [hgφ]; exact hc)
    (by rw [hgφ]; exact mul_pos hφ0 hθe) hX hT hσ
  rwa [hgφ] at h

/-- `R[T]` itself is below the two-level bound built on `T` (for nonnegative `θna` and `T`), so
Lemma M and the line steps apply to `T' = Rstep θna T`. -/
theorem stepLE_Rstep {θna T : ℝ → ℝ} (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hT : ∀ x, 0 < x → 0 ≤ T x) : StepLE θna T (Rstep θna T) := by
  intro g φ β B hβ hβg hφ0 hφ1 hB
  exact csInf_le ⟨0, fun x hx => admissible_nonneg hθ hT hx⟩ ⟨φ, β, hβ, hβg, hφ0, hφ1, hB⟩

/-- **The line step along the exact recursion.**  A majorant line `(B, σ)`, `σ ≤ 1`, of level
`k` on `(0, R]` gives the majorant line `(B, (B − (1 − σ) θna e)/e)` of level `k + 1` on
`(0, R e/(θna e + R)]`, for every outer rate `e` at which `θna` is continuous and positive. -/
theorem exactRec_line_step {θna : ℝ → ℝ} {C : ℝ} (hθ : ∀ x, 0 < x → 0 ≤ θna x)
    (hθanti : ∀ x y, 0 < x → x ≤ y → θna y ≤ θna x) (hθC : ∀ x, 0 < x → θna x ≤ C) (k : ℕ)
    {B σ R e : ℝ} (hc : ContinuousAt θna e) (hθe : 0 < θna e) (hR : 0 < R)
    (hT : ∀ x, 0 < x → x ≤ R → exactRec θna k x ≤ B - σ * x) (hσ : σ ≤ 1) :
    ∀ g, 0 < g → g ≤ R * e / (θna e + R) →
      exactRec θna (k + 1) g ≤ B - ((B - (1 - σ) * θna e) / e) * g := by
  have P := exactRec_props hθ hθanti hθC k
  exact StepLE.line_step_rate (T' := exactRec θna (k + 1)) (stepLE_exact hθ P.1) P.2.2 hc hθe
    hR hT hσ

/-- The chord `1 − x` is a majorant of `gaussNa` on `(0, 1]`. -/
theorem gaussNa_le_one_sub {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x ≤ 1) : gaussNa x ≤ 1 - x := by
  obtain ⟨w, hw0, hw1, rfl⟩ := exists_sq_eq hx0 hx1
  rw [gaussNa_sq hw0 hw1]
  nlinarith [mul_nonneg hw0 (sub_nonneg.mpr hw1)]

/-- **Witness for Lemma M.**  The majorant line `1 − x` of `gaussNa` on `(0, 1]`, at the outer
rate `e = 1/4` (where `gaussNa e = 1/4`), becomes the majorant line `1 − 4 g` of the second level
of the Gaussian recursion on `(0, 1/5]`. -/
theorem gauss_level_two_majorant :
    ∀ g, 0 < g → g ≤ 1 / 5 → exactRec gaussNa 1 g ≤ 1 - 4 * g := by
  intro g hg hg5
  have hline : ∀ x, 0 < x → x ≤ 1 → exactRec gaussNa 0 x ≤ 1 - 1 * x := by
    intro x hx hx1
    show gaussNa x ≤ 1 - 1 * x
    rw [one_mul]
    exact gaussNa_le_one_sub hx.le hx1
  have h := exactRec_line_step (fun x _ => gaussNa_nonneg x) (fun x y _ hxy => gaussNa_anti hxy)
    gaussPair.na_le 0 (gaussPair.na_cont (1 / 4) (by norm_num))
    (by rw [gaussPair.na_h]; norm_num) one_pos hline le_rfl g hg
    (by rw [gaussPair.na_h]; norm_num; linarith)
  rw [gaussPair.na_h] at h
  norm_num at h
  linarith

end LineDynamics
end MetricChain
