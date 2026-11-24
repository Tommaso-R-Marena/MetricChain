import Mathlib

/-!
# MetricChain — exact-rational verification semantics with outward rounding

This file is the numerical trust base of the project.  Every quantity that a certificate checker
has to *evaluate* is a computable function on `ℚ` (it can be run by the interpreter, by kernel
evaluation `decide +kernel` and by `norm_num`), and every such function comes with a soundness
theorem relating it to the *real* number it is meant to bound.  No floating point number and no
transcendental function is ever evaluated.

## Part 1 — dyadic outward rounding
* `roundDown p q`, `roundUp p q` : directed rounding of `q : ℚ` to the fixed-point grid `2⁻ᵖ ℤ`.
* `roundDown_le`, `le_roundUp`, `roundUp_sub_roundDown_le`, `roundDown_mono`, `roundUp_mono`.
* `dyadic_le_roundDown_iff`, `roundUp_le_dyadic_iff` : `roundDown p q` is the largest grid point
  below `q` and `roundUp p q` the smallest grid point above `q`; `roundDown_den_dvd`,
  `roundUp_den_dvd` : the results have denominators dividing `2ᵖ`.  So the model of
  fixed-precision directed rounding is faithful.

## Part 2 — rational intervals enclosing reals
* `QInterval` (two rational endpoints) and `QInterval.Contains I x` for `x : ℝ`.
* Computable operations `point`, `add`, `neg`, `sub`, `mul`, `scale`, `sq`, `inv`, `div`,
  `outward`, `hull`, `inter`, `sum`, `lowerBound`, `upperBound`.
* Soundness theorems `contains_point`, `contains_add`, `contains_neg`, `contains_sub`,
  `contains_mul`, `contains_scale`, `contains_sq`, `contains_inv`, `contains_div`,
  `contains_outward`, `contains_hull_left`, `contains_hull_right`, `contains_inter`,
  `contains_sum`, the width bound `outward_width_le`, and tightness of the square
  (`sq_lo_attained`, `sq_hi_attained`).

## Part 3 — certified rational enclosure of `exp`
* `expTaylor`, `expErr`, `expLo`, `expHi` : Taylor polynomial with explicit remainder, combined
  with the argument reduction `exp q = (exp (q / 2ᵏ)) ^ 2ᵏ`.
* `exp_enclosure` : `expLo n k q ≤ exp q ≤ expHi n k q` whenever `0 < n` and `|q| ≤ 2ᵏ`.
* Certificate forms `le_exp_of_le_expLo`, `exp_le_of_expHi_le`, `le_log_of_expHi_le`,
  `log_le_of_le_expLo` (a claimed bound on `exp` or `log` is reduced to a rational comparison),
  and positivity `expLo_pos`.
* `QInterval.exp`, `QInterval.contains_exp`, the Boltzmann-factor corollary
  `QInterval.contains_boltzmann` and its finite-sum (partition function) form
  `QInterval.contains_boltzmann_sum`.

## Part 4 — rational atlas of the circle
* `circParam t = ((1 - t²)/(1 + t²), 2t/(1 + t²))` and `quarterTurn q` (rotation by `q · 90°`).
* `circParam_on_circle`, and `circle_rational_atlas` : every point of the unit circle equals
  `quarterTurn q (circParam t)` for some `q : Fin 4` and some `|t| ≤ 1/2`
  (`torsion_rational_atlas` for the point `(cos θ, sin θ)`).  A torsion angle can therefore be
  replaced by the coordinates `(q, t)`, in which `cos` and `sin` are rational functions.
* `circParamQ` (computable rational points of the circle), `QInterval.circParam`,
  `QInterval.quarterTurn`, `QInterval.circChart` : rational-interval enclosures of the charts,
  with soundness theorems `QInterval.contains_circParam`, `QInterval.contains_quarterTurn`,
  `QInterval.contains_circChart`.

## Part 5 — executability
Concrete evaluations checked by `norm_num`, by kernel evaluation (`decide +kernel`) and by plain
`decide`, together with instances of the soundness theorems, e.g. `2.7182 ≤ exp 1 ≤ 2.7183`
obtained from `exp_enclosure` and two rational comparisons.
-/

namespace MetricChain

/-! ## Part 1 — dyadic outward rounding -/

/-- `roundDown p q` is `q` rounded towards `-∞` on the dyadic grid `2⁻ᵖ ℤ` (fixed-point arithmetic
with `p` fractional bits).  It is the largest grid point `≤ q`, see `dyadic_le_roundDown_iff`. -/
def roundDown (p : ℕ) (q : ℚ) : ℚ := ⌊q * 2 ^ p⌋ / 2 ^ p

/-- `roundUp p q` is `q` rounded towards `+∞` on the dyadic grid `2⁻ᵖ ℤ`.
It is the smallest grid point `≥ q`, see `roundUp_le_dyadic_iff`. -/
def roundUp (p : ℕ) (q : ℚ) : ℚ := ⌈q * 2 ^ p⌉ / 2 ^ p

theorem roundDown_le (p : ℕ) (q : ℚ) : roundDown p q ≤ q := by
  unfold roundDown
  rw [div_le_iff₀ (by positivity)]
  exact Int.floor_le _

theorem le_roundUp (p : ℕ) (q : ℚ) : q ≤ roundUp p q := by
  unfold roundUp
  rw [le_div_iff₀ (by positivity)]
  exact Int.le_ceil _

theorem roundDown_le_roundUp (p : ℕ) (q : ℚ) : roundDown p q ≤ roundUp p q :=
  (roundDown_le p q).trans (le_roundUp p q)

/-- Rounding up and rounding down differ by at most one grid step. -/
theorem roundUp_sub_roundDown_le (p : ℕ) (q : ℚ) : roundUp p q - roundDown p q ≤ 1 / 2 ^ p := by
  unfold roundUp roundDown
  rw [← sub_div]
  have h : ((⌈q * 2 ^ p⌉ : ℤ) : ℚ) ≤ ((⌊q * 2 ^ p⌋ + 1 : ℤ) : ℚ) := by
    exact_mod_cast Int.ceil_le_floor_add_one (q * 2 ^ p)
  push_cast at h
  gcongr
  linarith

/-- Rounding down loses strictly less than one grid step. -/
theorem sub_lt_roundDown (p : ℕ) (q : ℚ) : q - 1 / 2 ^ p < roundDown p q := by
  unfold roundDown
  have h2 : (0 : ℚ) < 2 ^ p := by positivity
  have h : (q - 1 / 2 ^ p) * 2 ^ p = q * 2 ^ p - 1 := by field_simp
  rw [lt_div_iff₀ h2, h]
  exact Int.sub_one_lt_floor _

/-- Rounding up gains strictly less than one grid step. -/
theorem roundUp_lt_add (p : ℕ) (q : ℚ) : roundUp p q < q + 1 / 2 ^ p := by
  unfold roundUp
  have h2 : (0 : ℚ) < 2 ^ p := by positivity
  have h : (q + 1 / 2 ^ p) * 2 ^ p = q * 2 ^ p + 1 := by field_simp
  rw [div_lt_iff₀ h2, h]
  exact Int.ceil_lt_add_one _

/-- `roundDown p` is monotone in the rounded number. -/
theorem roundDown_mono (p : ℕ) : Monotone (roundDown p) := by
  intro a b h
  unfold roundDown
  have : ⌊a * 2 ^ p⌋ ≤ ⌊b * 2 ^ p⌋ := Int.floor_le_floor (by gcongr)
  gcongr

/-- `roundUp p` is monotone in the rounded number. -/
theorem roundUp_mono (p : ℕ) : Monotone (roundUp p) := by
  intro a b h
  unfold roundUp
  have : ⌈a * 2 ^ p⌉ ≤ ⌈b * 2 ^ p⌉ := Int.ceil_le_ceil (by gcongr)
  gcongr

/-- `roundDown p q` is the **largest** point of the grid `2⁻ᵖ ℤ` below `q`. -/
theorem dyadic_le_roundDown_iff (p : ℕ) (z : ℤ) (q : ℚ) :
    (z : ℚ) / 2 ^ p ≤ roundDown p q ↔ (z : ℚ) / 2 ^ p ≤ q := by
  unfold roundDown
  have h2 : (0 : ℚ) < 2 ^ p := by positivity
  rw [div_le_div_iff_of_pos_right h2, Int.cast_le, Int.le_floor, div_le_iff₀ h2]

/-- `roundUp p q` is the **smallest** point of the grid `2⁻ᵖ ℤ` above `q`. -/
theorem roundUp_le_dyadic_iff (p : ℕ) (z : ℤ) (q : ℚ) :
    roundUp p q ≤ (z : ℚ) / 2 ^ p ↔ q ≤ (z : ℚ) / 2 ^ p := by
  unfold roundUp
  have h2 : (0 : ℚ) < 2 ^ p := by positivity
  rw [div_le_div_iff_of_pos_right h2, Int.cast_le, Int.ceil_le, le_div_iff₀ h2]

/-- Grid points are fixed by `roundDown`. -/
theorem roundDown_dyadic (p : ℕ) (z : ℤ) : roundDown p ((z : ℚ) / 2 ^ p) = (z : ℚ) / 2 ^ p := by
  unfold roundDown
  rw [div_mul_cancel₀ _ (by positivity : (2 : ℚ) ^ p ≠ 0), Int.floor_intCast]

/-- Grid points are fixed by `roundUp`. -/
theorem roundUp_dyadic (p : ℕ) (z : ℤ) : roundUp p ((z : ℚ) / 2 ^ p) = (z : ℚ) / 2 ^ p := by
  unfold roundUp
  rw [div_mul_cancel₀ _ (by positivity : (2 : ℚ) ^ p ≠ 0), Int.ceil_intCast]

theorem roundDown_neg (p : ℕ) (q : ℚ) : roundDown p (-q) = -roundUp p q := by
  unfold roundDown roundUp
  rw [neg_mul, Int.floor_neg, Int.cast_neg, neg_div]

theorem roundUp_neg (p : ℕ) (q : ℚ) : roundUp p (-q) = -roundDown p q := by
  unfold roundDown roundUp
  rw [neg_mul, Int.ceil_neg, Int.cast_neg, neg_div]

/-- Rounding down keeps nonnegative numbers nonnegative (rounded weights stay weights). -/
theorem roundDown_nonneg (p : ℕ) {q : ℚ} (h : 0 ≤ q) : 0 ≤ roundDown p q := by
  unfold roundDown
  have h0 : 0 ≤ ⌊q * 2 ^ p⌋ := Int.floor_nonneg.mpr (by positivity)
  exact div_nonneg (by exact_mod_cast h0) (by positivity)

theorem roundUp_nonneg (p : ℕ) {q : ℚ} (h : 0 ≤ q) : 0 ≤ roundUp p q :=
  h.trans (le_roundUp p q)

theorem roundUp_pos (p : ℕ) {q : ℚ} (h : 0 < q) : 0 < roundUp p q :=
  h.trans_le (le_roundUp p q)

/-- Fixed precision: `roundDown p q` is representable with `p` fractional bits. -/
theorem roundDown_den_dvd (p : ℕ) (q : ℚ) : (roundDown p q).den ∣ 2 ^ p := by
  unfold roundDown
  exact_mod_cast Rat.den_dvd ⌊q * 2 ^ p⌋ (2 ^ p)

/-- Fixed precision: `roundUp p q` is representable with `p` fractional bits. -/
theorem roundUp_den_dvd (p : ℕ) (q : ℚ) : (roundUp p q).den ∣ 2 ^ p := by
  unfold roundUp
  exact_mod_cast Rat.den_dvd ⌈q * 2 ^ p⌉ (2 ^ p)

/-- Real-number form of `roundDown_le`. -/
theorem roundDown_cast_le (p : ℕ) (q : ℚ) : ((roundDown p q : ℚ) : ℝ) ≤ (q : ℝ) :=
  Rat.cast_le.mpr (roundDown_le p q)

/-- Real-number form of `le_roundUp`. -/
theorem le_roundUp_cast (p : ℕ) (q : ℚ) : (q : ℝ) ≤ ((roundUp p q : ℚ) : ℝ) :=
  Rat.cast_le.mpr (le_roundUp p q)

/-! ## Part 2 — rational intervals enclosing reals -/

/-- A closed interval `[lo, hi]` with rational endpoints.  No ordering of the endpoints is
required: if `hi < lo` the interval contains no real number and every soundness statement
about it holds vacuously. -/
structure QInterval where
  /-- lower endpoint -/
  lo : ℚ
  /-- upper endpoint -/
  hi : ℚ
  deriving DecidableEq, Repr

namespace QInterval

/-- `I.Contains x`: the real number `x` lies in the closed interval `[I.lo, I.hi]`. -/
def Contains (I : QInterval) (x : ℝ) : Prop := (I.lo : ℝ) ≤ x ∧ x ≤ (I.hi : ℝ)

/-- The degenerate interval `[q, q]`. -/
def point (q : ℚ) : QInterval := ⟨q, q⟩

/-- Interval addition. -/
def add (I J : QInterval) : QInterval := ⟨I.lo + J.lo, I.hi + J.hi⟩

/-- Interval negation. -/
def neg (I : QInterval) : QInterval := ⟨-I.hi, -I.lo⟩

/-- Interval subtraction. -/
def sub (I J : QInterval) : QInterval := ⟨I.lo - J.hi, I.hi - J.lo⟩

/-- Interval multiplication: minimum and maximum of the four corner products. -/
def mul (I J : QInterval) : QInterval :=
  ⟨min (min (I.lo * J.lo) (I.lo * J.hi)) (min (I.hi * J.lo) (I.hi * J.hi)),
   max (max (I.lo * J.lo) (I.lo * J.hi)) (max (I.hi * J.lo) (I.hi * J.hi))⟩

/-- Multiplication of an interval by a rational constant (of either sign). -/
def scale (c : ℚ) (I : QInterval) : QInterval :=
  ⟨min (c * I.lo) (c * I.hi), max (c * I.lo) (c * I.hi)⟩

/-- Tight interval square: the lower endpoint is `0` when the interval straddles `0`
(see `sq_lo_attained`, `sq_hi_attained` for tightness). -/
def sq (I : QInterval) : QInterval :=
  ⟨if 0 ≤ I.lo then I.lo ^ 2 else if I.hi ≤ 0 then I.hi ^ 2 else 0, max (I.lo ^ 2) (I.hi ^ 2)⟩

/-- Interval reciprocal; sound when `0 < I.lo`, see `contains_inv`. -/
def inv (I : QInterval) : QInterval := ⟨I.hi⁻¹, I.lo⁻¹⟩

/-- Interval division `I / J`; sound when `0 < J.lo`, see `contains_div`. -/
def div (I J : QInterval) : QInterval := I.mul J.inv

/-- Outward rounding of both endpoints to the dyadic grid `2⁻ᵖ ℤ`. -/
def outward (p : ℕ) (I : QInterval) : QInterval := ⟨roundDown p I.lo, roundUp p I.hi⟩

/-- Convex hull (interval union) of two intervals. -/
def hull (I J : QInterval) : QInterval := ⟨min I.lo J.lo, max I.hi J.hi⟩

/-- Intersection of two intervals (combines two enclosures of the same quantity). -/
def inter (I J : QInterval) : QInterval := ⟨max I.lo J.lo, min I.hi J.hi⟩

/-- Interval sum over a finite index set. -/
def sum {ι : Type*} (s : Finset ι) (f : ι → QInterval) : QInterval :=
  ⟨∑ i ∈ s, (f i).lo, ∑ i ∈ s, (f i).hi⟩

/-- The certified lower bound carried by an interval. -/
def lowerBound (I : QInterval) : ℚ := I.lo

/-- The certified upper bound carried by an interval. -/
def upperBound (I : QInterval) : ℚ := I.hi

variable {I J : QInterval} {x y : ℝ}

theorem Contains.lo_le_hi (h : Contains I x) : I.lo ≤ I.hi := by
  have := h.1.trans h.2
  exact_mod_cast this

/-- Enlarging an interval preserves containment. -/
theorem Contains.mono (h : Contains I x) (hlo : J.lo ≤ I.lo) (hhi : I.hi ≤ J.hi) :
    Contains J x :=
  ⟨(Rat.cast_le.mpr hlo).trans h.1, h.2.trans (Rat.cast_le.mpr hhi)⟩

/-- Containment of a rational point is the (decidable) rational statement. -/
theorem contains_ratCast_iff {q : ℚ} : Contains I (q : ℝ) ↔ I.lo ≤ q ∧ q ≤ I.hi := by
  simp [Contains]

theorem Contains.lowerBound_le (hx : Contains I x) : (I.lowerBound : ℝ) ≤ x := hx.1

theorem Contains.le_upperBound (hx : Contains I x) : x ≤ (I.upperBound : ℝ) := hx.2

/-- Certificate form of a lower bound: a rational comparison with the lower endpoint. -/
theorem Contains.cast_le_of_le_lo (hx : Contains I x) {a : ℚ} (ha : a ≤ I.lo) : (a : ℝ) ≤ x :=
  (Rat.cast_le.mpr ha).trans hx.1

/-- Certificate form of an upper bound: a rational comparison with the upper endpoint. -/
theorem Contains.le_cast_of_hi_le (hx : Contains I x) {b : ℚ} (hb : I.hi ≤ b) : x ≤ (b : ℝ) :=
  hx.2.trans (Rat.cast_le.mpr hb)

theorem contains_point (q : ℚ) : Contains (point q) (q : ℝ) := ⟨le_rfl, le_rfl⟩

/-- Variant of `contains_point` for a real number known to equal a rational. -/
theorem contains_point_of_eq {q : ℚ} (h : (q : ℝ) = x) : Contains (point q) x :=
  h ▸ contains_point q

theorem contains_add (hx : Contains I x) (hy : Contains J y) : Contains (add I J) (x + y) := by
  constructor
  · simp only [add, Rat.cast_add]; linarith [hx.1, hy.1]
  · simp only [add, Rat.cast_add]; linarith [hx.2, hy.2]

theorem contains_neg (hx : Contains I x) : Contains (neg I) (-x) := by
  constructor
  · simp only [neg, Rat.cast_neg]; linarith [hx.2]
  · simp only [neg, Rat.cast_neg]; linarith [hx.1]

theorem contains_sub (hx : Contains I x) (hy : Contains J y) : Contains (sub I J) (x - y) := by
  constructor
  · simp only [sub, Rat.cast_sub]; linarith [hx.1, hy.2]
  · simp only [sub, Rat.cast_sub]; linarith [hx.2, hy.1]

/-- A product `a * y` with `y ∈ [c, d]` lies between the two endpoint products. -/
theorem mul_between (a : ℝ) {c d y : ℝ} (h₁ : c ≤ y) (h₂ : y ≤ d) :
    min (a * c) (a * d) ≤ a * y ∧ a * y ≤ max (a * c) (a * d) := by
  rcases le_total 0 a with ha | ha
  · exact ⟨(min_le_left _ _).trans (mul_le_mul_of_nonneg_left h₁ ha),
      (mul_le_mul_of_nonneg_left h₂ ha).trans (le_max_right _ _)⟩
  · exact ⟨(min_le_right _ _).trans (mul_le_mul_of_nonpos_left h₂ ha),
      (mul_le_mul_of_nonpos_left h₁ ha).trans (le_max_left _ _)⟩

theorem contains_scale (c : ℚ) (hx : Contains I x) : Contains (scale c I) ((c : ℝ) * x) := by
  obtain ⟨h1, h2⟩ := mul_between (c : ℝ) hx.1 hx.2
  constructor
  · simpa only [scale, Rat.cast_min, Rat.cast_mul] using h1
  · simpa only [scale, Rat.cast_max, Rat.cast_mul] using h2

theorem contains_mul (hx : Contains I x) (hy : Contains J y) : Contains (mul I J) (x * y) := by
  obtain ⟨h1, h2⟩ := mul_between y hx.1 hx.2
  obtain ⟨h3, h4⟩ := mul_between (I.lo : ℝ) hy.1 hy.2
  obtain ⟨h5, h6⟩ := mul_between (I.hi : ℝ) hy.1 hy.2
  rw [mul_comm y x, mul_comm y, mul_comm y] at h1 h2
  constructor
  · simp only [mul, Rat.cast_min, Rat.cast_mul]
    exact (min_le_min h3 h5).trans h1
  · simp only [mul, Rat.cast_max, Rat.cast_mul]
    exact h2.trans (max_le_max h4 h6)

/-- The lower endpoint of a square is never negative. -/
theorem sq_lo_nonneg (I : QInterval) : 0 ≤ I.sq.lo := by
  unfold sq
  dsimp only
  split_ifs <;> positivity

theorem contains_sq (hx : Contains I x) : Contains (sq I) (x ^ 2) := by
  obtain ⟨h1, h2⟩ := hx
  constructor
  · unfold sq
    dsimp only
    split_ifs with h3 h4
    · have h3' : (0 : ℝ) ≤ (I.lo : ℝ) := by exact_mod_cast h3
      push_cast
      exact pow_le_pow_left₀ h3' h1 2
    · have h4' : (I.hi : ℝ) ≤ 0 := by exact_mod_cast h4
      push_cast
      nlinarith
    · push_cast
      positivity
  · simp only [sq, Rat.cast_max, Rat.cast_pow]
    rcases le_total 0 x with h | h
    · exact le_max_of_le_right (pow_le_pow_left₀ h h2 2)
    · exact le_max_of_le_left (by nlinarith)

/-- Tightness of `sq`, lower endpoint: it is the square of a rational point of the interval. -/
theorem sq_lo_attained (I : QInterval) (h : I.lo ≤ I.hi) :
    ∃ a : ℚ, I.lo ≤ a ∧ a ≤ I.hi ∧ a ^ 2 = I.sq.lo := by
  unfold sq
  dsimp only
  split_ifs with h1 h2
  · exact ⟨I.lo, le_rfl, h, rfl⟩
  · exact ⟨I.hi, h, le_rfl, rfl⟩
  · exact ⟨0, (not_le.mp h1).le, (not_le.mp h2).le, by norm_num⟩

/-- Tightness of `sq`, upper endpoint: it is the square of an endpoint of the interval. -/
theorem sq_hi_attained (I : QInterval) (h : I.lo ≤ I.hi) :
    ∃ a : ℚ, I.lo ≤ a ∧ a ≤ I.hi ∧ a ^ 2 = I.sq.hi := by
  rcases max_choice (I.lo ^ 2) (I.hi ^ 2) with h' | h'
  · exact ⟨I.lo, le_rfl, h, h'.symm⟩
  · exact ⟨I.hi, h, le_rfl, h'.symm⟩

theorem contains_inv (h : 0 < I.lo) (hx : Contains I x) : Contains (inv I) x⁻¹ := by
  have h0 : (0 : ℝ) < (I.lo : ℝ) := by exact_mod_cast h
  have hx0 : 0 < x := h0.trans_le hx.1
  constructor
  · simp only [inv, Rat.cast_inv]
    exact inv_anti₀ hx0 hx.2
  · simp only [inv, Rat.cast_inv]
    exact inv_anti₀ h0 hx.1

theorem contains_div (h : 0 < J.lo) (hx : Contains I x) (hy : Contains J y) :
    Contains (div I J) (x / y) := by
  rw [div_eq_mul_inv]
  exact contains_mul hx (contains_inv h hy)

/-- Outward rounding is sound: it only enlarges the interval. -/
theorem contains_outward (p : ℕ) (hx : Contains I x) : Contains (I.outward p) x :=
  hx.mono (roundDown_le p I.lo) (le_roundUp p I.hi)

/-- Outward rounding to `p` fractional bits widens an interval by at most two grid steps. -/
theorem outward_width_le (p : ℕ) (I : QInterval) :
    (I.outward p).hi - (I.outward p).lo ≤ I.hi - I.lo + 2 / 2 ^ p := by
  simp only [outward]
  have h1 := roundUp_lt_add p I.hi
  have h2 := sub_lt_roundDown p I.lo
  have h3 : (2 : ℚ) / 2 ^ p = 1 / 2 ^ p + 1 / 2 ^ p := by ring
  linarith

/-- Outward rounding keeps a nonnegative lower endpoint nonnegative. -/
theorem outward_lo_nonneg (p : ℕ) (h : 0 ≤ I.lo) : 0 ≤ (I.outward p).lo :=
  roundDown_nonneg p h

theorem contains_hull_left (J : QInterval) (hx : Contains I x) : Contains (hull I J) x :=
  hx.mono (min_le_left _ _) (le_max_left _ _)

theorem contains_hull_right (I : QInterval) (hx : Contains J x) : Contains (hull I J) x :=
  hx.mono (min_le_right _ _) (le_max_right _ _)

theorem contains_inter (hI : Contains I x) (hJ : Contains J x) : Contains (inter I J) x := by
  constructor
  · simp only [inter, Rat.cast_max]
    exact max_le hI.1 hJ.1
  · simp only [inter, Rat.cast_min]
    exact le_min hI.2 hJ.2

theorem contains_sum {ι : Type*} {s : Finset ι} {f : ι → QInterval} {g : ι → ℝ}
    (h : ∀ i ∈ s, Contains (f i) (g i)) : Contains (sum s f) (∑ i ∈ s, g i) := by
  constructor
  · simp only [sum, Rat.cast_sum]
    exact Finset.sum_le_sum fun i hi => (h i hi).1
  · simp only [sum, Rat.cast_sum]
    exact Finset.sum_le_sum fun i hi => (h i hi).2

end QInterval

/-! ## Part 3 — certified rational enclosure of `exp` -/

/-- Taylor polynomial of `exp` at `0` with `n` terms, evaluated at the rational `x`. -/
def expTaylor (n : ℕ) (x : ℚ) : ℚ := ∑ m ∈ Finset.range n, x ^ m / m.factorial

/-- Remainder bound for `expTaylor n x`, valid for `|x| ≤ 1` and `0 < n` (`Real.exp_bound`). -/
def expErr (n : ℕ) (x : ℚ) : ℚ := |x| ^ n * ((n + 1 : ℚ) / (n.factorial * n))

/-- Rational lower bound for `exp q`: Taylor polynomial minus remainder at the reduced argument
`q / 2ᵏ`, clipped at `0`, then raised to the power `2ᵏ`. -/
def expLo (n k : ℕ) (q : ℚ) : ℚ :=
  (max 0 (expTaylor n (q / 2 ^ k) - expErr n (q / 2 ^ k))) ^ (2 ^ k)

/-- Rational upper bound for `exp q`: Taylor polynomial plus remainder at the reduced argument
`q / 2ᵏ`, then raised to the power `2ᵏ`. -/
def expHi (n k : ℕ) (q : ℚ) : ℚ :=
  (expTaylor n (q / 2 ^ k) + expErr n (q / 2 ^ k)) ^ (2 ^ k)

theorem expTaylor_cast (n : ℕ) (x : ℚ) :
    ((expTaylor n x : ℚ) : ℝ) = ∑ m ∈ Finset.range n, (x : ℝ) ^ m / (m.factorial : ℝ) := by
  simp [expTaylor]

theorem expErr_cast (n : ℕ) (x : ℚ) :
    ((expErr n x : ℚ) : ℝ) =
      |(x : ℝ)| ^ n * ((n.succ : ℝ) / ((n.factorial : ℝ) * (n : ℝ))) := by
  simp [expErr]

theorem expErr_nonneg (n : ℕ) (x : ℚ) : 0 ≤ expErr n x := by
  unfold expErr
  positivity

theorem expLo_nonneg (n k : ℕ) (q : ℚ) : 0 ≤ expLo n k q :=
  pow_nonneg (le_max_left _ _) _

/-- Taylor remainder bound on the unit interval, with all data rational. -/
theorem abs_exp_sub_expTaylor_le {n : ℕ} (hn : 0 < n) {x : ℚ} (hx : |x| ≤ 1) :
    |Real.exp (x : ℝ) - ((expTaylor n x : ℚ) : ℝ)| ≤ ((expErr n x : ℚ) : ℝ) := by
  rw [expTaylor_cast, expErr_cast]
  exact Real.exp_bound (by exact_mod_cast hx) hn

/-- **Certified enclosure of `exp`** at a rational point: for every number `n > 0` of Taylor
terms and every number `k` of argument halvings with `|q| ≤ 2ᵏ`, the computable rationals
`expLo n k q` and `expHi n k q` bracket the real number `exp q`. -/
theorem exp_enclosure (n k : ℕ) (hn : 0 < n) (q : ℚ) (hq : |q| ≤ 2 ^ k) :
    ((expLo n k q : ℚ) : ℝ) ≤ Real.exp (q : ℝ) ∧ Real.exp (q : ℝ) ≤ ((expHi n k q : ℚ) : ℝ) := by
  have h2k : (0 : ℚ) < 2 ^ k := by positivity
  have hy1 : |q / 2 ^ k| ≤ 1 := by
    rw [abs_div, abs_of_pos h2k]
    exact (div_le_one h2k).mpr hq
  have hb := abs_le.mp (abs_exp_sub_expTaylor_le hn hy1)
  have hexp : Real.exp (q : ℝ) = Real.exp ((q / 2 ^ k : ℚ) : ℝ) ^ (2 ^ k) := by
    rw [← Real.exp_nat_mul]
    congr 1
    push_cast
    field_simp
  rw [hexp]
  constructor
  · simp only [expLo, Rat.cast_pow, Rat.cast_max, Rat.cast_zero, Rat.cast_sub]
    apply pow_le_pow_left₀ (le_max_left _ _)
    exact max_le (Real.exp_pos _).le (by linarith [hb.2])
  · simp only [expHi, Rat.cast_pow, Rat.cast_add]
    apply pow_le_pow_left₀ (Real.exp_pos _).le
    linarith [hb.1]

/-- The two bounds of `exp_enclosure` are consistently ordered. -/
theorem expLo_le_expHi (n k : ℕ) (hn : 0 < n) (q : ℚ) (hq : |q| ≤ 2 ^ k) :
    expLo n k q ≤ expHi n k q := by
  have h := exp_enclosure n k hn q hq
  exact_mod_cast h.1.trans h.2

/-- Certificate form of the lower bound: to prove `a ≤ exp q` it suffices to check the rational
inequality `a ≤ expLo n k q` (e.g. by `decide +kernel` or `norm_num`). -/
theorem le_exp_of_le_expLo {n k : ℕ} (hn : 0 < n) {q a : ℚ} (hq : |q| ≤ 2 ^ k)
    (h : a ≤ expLo n k q) : (a : ℝ) ≤ Real.exp (q : ℝ) :=
  (Rat.cast_le.mpr h).trans (exp_enclosure n k hn q hq).1

/-- Certificate form of the upper bound: to prove `exp q ≤ b` it suffices to check the rational
inequality `expHi n k q ≤ b`. -/
theorem exp_le_of_expHi_le {n k : ℕ} (hn : 0 < n) {q b : ℚ} (hq : |q| ≤ 2 ^ k)
    (h : expHi n k q ≤ b) : Real.exp (q : ℝ) ≤ (b : ℝ) :=
  (exp_enclosure n k hn q hq).2.trans (Rat.cast_le.mpr h)

/-- Certificate form of a lower bound for `log` (e.g. for free energies): `a ≤ log z` follows
from the comparison `expHi n k a ≤ z`. -/
theorem le_log_of_expHi_le {n k : ℕ} (hn : 0 < n) {a : ℚ} (ha : |a| ≤ 2 ^ k) {z : ℝ}
    (h : ((expHi n k a : ℚ) : ℝ) ≤ z) : (a : ℝ) ≤ Real.log z := by
  have h1 := (exp_enclosure n k hn a ha).2.trans h
  exact (Real.le_log_iff_exp_le ((Real.exp_pos _).trans_le h1)).mpr h1

/-- Certificate form of an upper bound for `log`: `log z ≤ b` follows from the comparison
`z ≤ expLo n k b`. -/
theorem log_le_of_le_expLo {n k : ℕ} (hn : 0 < n) {b : ℚ} (hb : |b| ≤ 2 ^ k) {z : ℝ}
    (hz : 0 < z) (h : z ≤ ((expLo n k b : ℚ) : ℝ)) : Real.log z ≤ (b : ℝ) :=
  (Real.log_le_iff_le_exp hz).mpr (h.trans (exp_enclosure n k hn b hb).1)

/-- With at least four Taylor terms the lower bound `expLo` is strictly positive (a sufficient
condition; it makes Boltzmann-factor enclosures invertible, cf. `QInterval.contains_inv`). -/
theorem expLo_pos {n k : ℕ} (hn : 4 ≤ n) {q : ℚ} (hq : |q| ≤ 2 ^ k) : 0 < expLo n k q := by
  have h2k : (0 : ℚ) < 2 ^ k := by positivity
  have hy1 : |q / 2 ^ k| ≤ 1 := by
    rw [abs_div, abs_of_pos h2k]
    exact (div_le_one h2k).mpr hq
  have hn0 : 0 < n := by omega
  have hb := abs_le.mp (abs_exp_sub_expTaylor_le hn0 hy1)
  -- the remainder bound is at most `5/96`
  have hE : expErr n (q / 2 ^ k) ≤ 5 / 96 := by
    unfold expErr
    have h1 : |q / 2 ^ k| ^ n ≤ 1 := pow_le_one₀ (abs_nonneg _) hy1
    have hfac : (24 : ℚ) ≤ (n.factorial : ℚ) := by
      exact_mod_cast (Nat.factorial_le hn : Nat.factorial 4 ≤ n.factorial)
    have hn4 : (4 : ℚ) ≤ (n : ℚ) := by exact_mod_cast hn
    have h2 : ((n : ℚ) + 1) / ((n.factorial : ℚ) * (n : ℚ)) ≤ 5 / 96 := by
      rw [div_le_div_iff₀ (by positivity) (by norm_num)]
      nlinarith
    calc |q / 2 ^ k| ^ n * (((n : ℚ) + 1) / ((n.factorial : ℚ) * (n : ℚ)))
        ≤ 1 * (5 / 96) := mul_le_mul h1 h2 (by positivity) zero_le_one
      _ = 5 / 96 := one_mul _
  have hE' : ((expErr n (q / 2 ^ k) : ℚ) : ℝ) ≤ 5 / 96 :=
    (Rat.cast_le.mpr hE).trans (by norm_num)
  -- `exp y ≥ exp (-1) ≥ 0.36` on the unit interval
  have hy : (-1 : ℝ) ≤ ((q / 2 ^ k : ℚ) : ℝ) := by
    have := (abs_le.mp hy1).1
    exact_mod_cast this
  have hexp : (0.36 : ℝ) ≤ Real.exp ((q / 2 ^ k : ℚ) : ℝ) := by
    refine le_trans ?_ (Real.exp_le_exp.mpr hy)
    rw [Real.exp_neg, le_inv_comm₀ (by norm_num) (Real.exp_pos 1)]
    exact Real.exp_one_lt_d9.le.trans (by norm_num)
  have hpos : (0 : ℝ) < ((expTaylor n (q / 2 ^ k) - expErr n (q / 2 ^ k) : ℚ) : ℝ) := by
    push_cast
    linarith [hb.2]
  have hposQ : 0 < expTaylor n (q / 2 ^ k) - expErr n (q / 2 ^ k) := by exact_mod_cast hpos
  unfold expLo
  exact pow_pos (lt_max_of_lt_right hposQ) _

namespace QInterval

variable {I : QInterval} {x : ℝ}

/-- Interval extension of `exp` (`exp` is monotone, so only the endpoints are needed). -/
def exp (n k : ℕ) (I : QInterval) : QInterval := ⟨expLo n k I.lo, expHi n k I.hi⟩

theorem contains_exp {n k : ℕ} (hn : 0 < n) (hlo : |I.lo| ≤ 2 ^ k) (hhi : |I.hi| ≤ 2 ^ k)
    (hx : Contains I x) : Contains (I.exp n k) (Real.exp x) :=
  ⟨(exp_enclosure n k hn I.lo hlo).1.trans (Real.exp_le_exp.mpr hx.1),
    (Real.exp_le_exp.mpr hx.2).trans (exp_enclosure n k hn I.hi hhi).2⟩

/-- The lower endpoint of an `exp` enclosure is never negative. -/
theorem exp_lo_nonneg (n k : ℕ) (I : QInterval) : 0 ≤ (I.exp n k).lo :=
  expLo_nonneg n k I.lo

/-- The lower endpoint of an `exp` enclosure with at least four Taylor terms is positive. -/
theorem exp_lo_pos {n k : ℕ} (hn : 4 ≤ n) (hlo : |I.lo| ≤ 2 ^ k) : 0 < (I.exp n k).lo :=
  expLo_pos hn hlo

/-- **Boltzmann factor.**  If the energy `e` lies in the rational interval `I` and `β` is a
rational inverse temperature with `|β · I.lo| ≤ 2ᵏ` and `|β · I.hi| ≤ 2ᵏ`, then the computable
interval `(I.scale (-β)).exp n k` encloses the Boltzmann factor `exp (-β e)`. -/
theorem contains_boltzmann {n k : ℕ} (hn : 0 < n) (β : ℚ) {e : ℝ}
    (hlo : |β * I.lo| ≤ 2 ^ k) (hhi : |β * I.hi| ≤ 2 ^ k) (he : Contains I e) :
    Contains ((I.scale (-β)).exp n k) (Real.exp (-(β : ℝ) * e)) := by
  have h := contains_scale (-β) he
  rw [Rat.cast_neg] at h
  have hlo' : |-β * I.lo| ≤ 2 ^ k := by rwa [neg_mul, abs_neg]
  have hhi' : |-β * I.hi| ≤ 2 ^ k := by rwa [neg_mul, abs_neg]
  refine contains_exp hn ?_ ?_ h
  · simp only [scale]
    rcases min_choice (-β * I.lo) (-β * I.hi) with h' | h' <;> rw [h'] <;> assumption
  · simp only [scale]
    rcases max_choice (-β * I.lo) (-β * I.hi) with h' | h' <;> rw [h'] <;> assumption

/-- **Partition-function enclosure.**  If each energy `E i` lies in the rational interval `I i`,
the computable interval sum of the Boltzmann enclosures contains the Boltzmann sum
`∑ i ∈ S, exp (-β · E i)` (the partition function of a finite configuration set). -/
theorem contains_boltzmann_sum {ι : Type*} {n k : ℕ} (hn : 0 < n) (β : ℚ) {S : Finset ι}
    {I : ι → QInterval} {E : ι → ℝ}
    (hlo : ∀ i ∈ S, |β * (I i).lo| ≤ 2 ^ k) (hhi : ∀ i ∈ S, |β * (I i).hi| ≤ 2 ^ k)
    (hE : ∀ i ∈ S, Contains (I i) (E i)) :
    Contains (sum S fun i => ((I i).scale (-β)).exp n k)
      (∑ i ∈ S, Real.exp (-(β : ℝ) * E i)) :=
  contains_sum fun i hi => contains_boltzmann hn β (hlo i hi) (hhi i hi) (hE i hi)

end QInterval

/-! ## Part 4 — rational atlas of the circle -/

/-- Rational parametrisation of the unit circle (half-angle substitution `t = tan (θ/2)`,
see `circParam_tan_half`). -/
noncomputable def circParam (t : ℝ) : ℝ × ℝ :=
  ((1 - t ^ 2) / (1 + t ^ 2), 2 * t / (1 + t ^ 2))

/-- Rotation of the plane by `q` quarter turns (`q · 90°`). -/
def quarterTurn : Fin 4 → ℝ × ℝ → ℝ × ℝ
  | 0, (a, b) => (a, b)
  | 1, (a, b) => (-b, a)
  | 2, (a, b) => (-a, -b)
  | 3, (a, b) => (b, -a)

@[simp] theorem quarterTurn_zero (p : ℝ × ℝ) : quarterTurn 0 p = p := rfl
@[simp] theorem quarterTurn_one (p : ℝ × ℝ) : quarterTurn 1 p = (-p.2, p.1) := rfl
@[simp] theorem quarterTurn_two (p : ℝ × ℝ) : quarterTurn 2 p = (-p.1, -p.2) := rfl
@[simp] theorem quarterTurn_three (p : ℝ × ℝ) : quarterTurn 3 p = (p.2, -p.1) := rfl

theorem circParam_on_circle (t : ℝ) : (circParam t).1 ^ 2 + (circParam t).2 ^ 2 = 1 := by
  have h : (1 + t ^ 2) ≠ 0 := by positivity
  simp only [circParam]
  field_simp
  ring

/-- Quarter turns preserve the squared norm, hence the unit circle. -/
theorem quarterTurn_norm_sq (q : Fin 4) (p : ℝ × ℝ) :
    (quarterTurn q p).1 ^ 2 + (quarterTurn q p).2 ^ 2 = p.1 ^ 2 + p.2 ^ 2 := by
  fin_cases q <;> simp <;> ring

/-- Every chart value lies on the unit circle. -/
theorem quarterTurn_circParam_on_circle (q : Fin 4) (t : ℝ) :
    (quarterTurn q (circParam t)).1 ^ 2 + (quarterTurn q (circParam t)).2 ^ 2 = 1 := by
  rw [quarterTurn_norm_sq, circParam_on_circle]

/-- The parameter is recovered from the point `(c, s) = circParam t` as `t = s / (1 + c)`. -/
theorem circParam_snd_div_one_add_fst (t : ℝ) :
    (circParam t).2 / (1 + (circParam t).1) = t := by
  have h : (1 + t ^ 2) ≠ 0 := by positivity
  simp only [circParam]
  field_simp
  ring

/-- Each chart is injective. -/
theorem circParam_injective : Function.Injective circParam := by
  intro t t' h
  rw [← circParam_snd_div_one_add_fst t, ← circParam_snd_div_one_add_fst t', h]

/-- Meaning of the parameter: `t = tan (θ/2)` gives the point `(cos θ, sin θ)`. -/
theorem circParam_tan_half {θ : ℝ} (h : Real.cos (θ / 2) ≠ 0) :
    circParam (Real.tan (θ / 2)) = (Real.cos θ, Real.sin θ) := by
  have h1 := Real.sin_sq_add_cos_sq (θ / 2)
  have hc : Real.cos θ = 2 * Real.cos (θ / 2) ^ 2 - 1 := by
    rw [← Real.cos_two_mul]; congr 1; ring
  have hs : Real.sin θ = 2 * Real.sin (θ / 2) * Real.cos (θ / 2) := by
    rw [← Real.sin_two_mul]; congr 1; ring
  have hne : Real.cos (θ / 2) ^ 2 + Real.sin (θ / 2) ^ 2 ≠ 0 := by
    rw [add_comm, h1]; exact one_ne_zero
  rw [hc, hs, Real.tan_eq_sin_div_cos]
  unfold circParam
  refine Prod.ext ?_ ?_
  · simp only
    field_simp
    linear_combination (-2 * Real.cos (θ / 2) ^ 2) * h1
  · simp only
    field_simp
    linear_combination (-Real.sin (θ / 2)) * h1

/-- Inverse of the chart on the arc `|s| ≤ c` (angles in `[-45°, 45°]`): the parameter
`t = s / (1 + c)` reproduces `(c, s)` and satisfies `|t| ≤ 1/2`. -/
theorem circParam_of_abs_le {c s : ℝ} (h : c ^ 2 + s ^ 2 = 1) (hs : |s| ≤ c) :
    |s / (1 + c)| ≤ 1 / 2 ∧ circParam (s / (1 + c)) = (c, s) := by
  have hc0 : 0 ≤ c := (abs_nonneg s).trans hs
  have hc : (0 : ℝ) < 1 + c := by linarith
  have hs2 : s ^ 2 ≤ c ^ 2 := sq_le_sq' (by linarith [neg_abs_le s]) (le_of_abs_le hs)
  have hc35 : 3 / 5 ≤ c := by nlinarith
  constructor
  · rw [abs_div, abs_of_pos hc, div_le_iff₀ hc]
    apply abs_le_of_sq_le_sq _ (by positivity)
    nlinarith
  · have hne : (1 + c) ≠ 0 := hc.ne'
    have hne2 : (1 + c) ^ 2 + s ^ 2 ≠ 0 := by positivity
    unfold circParam
    refine Prod.ext ?_ ?_
    · simp only
      field_simp
      linear_combination (-(1 + c)) * h
    · simp only
      field_simp
      linear_combination (-s) * h

/-- **Rational atlas of the circle.**  Every point `(c, s)` of the unit circle is the image of
some parameter `t ∈ [-1/2, 1/2]` under one of the four charts `quarterTurn q ∘ circParam`. -/
theorem circle_rational_atlas (c s : ℝ) (h : c ^ 2 + s ^ 2 = 1) :
    ∃ q : Fin 4, ∃ t : ℝ, |t| ≤ 1 / 2 ∧ quarterTurn q (circParam t) = (c, s) := by
  rcases le_total |s| |c| with h1 | h1
  · rcases le_total 0 c with h2 | h2
    · rw [abs_of_nonneg h2] at h1
      obtain ⟨ht, hp⟩ := circParam_of_abs_le h h1
      exact ⟨0, s / (1 + c), ht, by rw [hp]; rfl⟩
    · rw [abs_of_nonpos h2] at h1
      have h' : (-c) ^ 2 + (-s) ^ 2 = 1 := by nlinarith
      obtain ⟨ht, hp⟩ := circParam_of_abs_le h' (by rwa [abs_neg])
      exact ⟨2, -s / (1 + -c), ht, by rw [hp]; simp⟩
  · rcases le_total 0 s with h2 | h2
    · rw [abs_of_nonneg h2] at h1
      have h' : s ^ 2 + (-c) ^ 2 = 1 := by nlinarith
      obtain ⟨ht, hp⟩ := circParam_of_abs_le h' (by rwa [abs_neg])
      exact ⟨1, -c / (1 + s), ht, by rw [hp]; simp⟩
    · rw [abs_of_nonpos h2] at h1
      have h' : (-s) ^ 2 + c ^ 2 = 1 := by nlinarith
      obtain ⟨ht, hp⟩ := circParam_of_abs_le h' h1
      exact ⟨3, c / (1 + -s), ht, by rw [hp]; simp⟩

/-- Torsion-angle form of the atlas: every angle `θ` has transcendental-free coordinates
`(q, t)`, `|t| ≤ 1/2`, in which `(cos θ, sin θ)` is a rational function of `t`. -/
theorem torsion_rational_atlas (θ : ℝ) :
    ∃ q : Fin 4, ∃ t : ℝ, |t| ≤ 1 / 2 ∧
      quarterTurn q (circParam t) = (Real.cos θ, Real.sin θ) :=
  circle_rational_atlas _ _ (Real.cos_sq_add_sin_sq θ)

/-- Computable rational version of `circParam`: rational parameters give rational points. -/
def circParamQ (t : ℚ) : ℚ × ℚ := ((1 - t ^ 2) / (1 + t ^ 2), 2 * t / (1 + t ^ 2))

theorem circParam_ratCast (t : ℚ) :
    circParam (t : ℝ) = (((circParamQ t).1 : ℝ), ((circParamQ t).2 : ℝ)) := by
  simp [circParam, circParamQ]

theorem circParamQ_on_circle (t : ℚ) : (circParamQ t).1 ^ 2 + (circParamQ t).2 ^ 2 = 1 := by
  have h : (1 + t ^ 2) ≠ 0 := by positivity
  simp only [circParamQ]
  field_simp
  ring

/-- `t ↦ 2t / (1 + t²)` is monotone on `[-1, 1]`. -/
theorem two_mul_div_one_add_sq_mono {a b : ℝ} (ha : -1 ≤ a) (hab : a ≤ b) (hb : b ≤ 1) :
    2 * a / (1 + a ^ 2) ≤ 2 * b / (1 + b ^ 2) := by
  have h1 : a * b ≤ 1 := by nlinarith
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith [mul_nonneg (sub_nonneg.2 hab) (sub_nonneg.2 h1)]

/-- `2t / (1 + t²)` always lies in `[-1, 1]`. -/
theorem two_mul_div_one_add_sq_mem (t : ℝ) :
    -1 ≤ 2 * t / (1 + t ^ 2) ∧ 2 * t / (1 + t ^ 2) ≤ 1 := by
  have h : (0 : ℝ) < 1 + t ^ 2 := by positivity
  constructor
  · rw [le_div_iff₀ h]
    nlinarith [sq_nonneg (t + 1)]
  · rw [div_le_one h]
    nlinarith [sq_nonneg (t - 1)]

/-- Interval enclosure of `circParam t` for `t ∈ I`.

* The first component is evaluated through the dependency-free form `2 / (1 + t²) - 1`
  (the interval square is tight and `1 + t² ≥ 1 > 0`, so `inv` applies).
* The second component uses the monotonicity of `t ↦ 2t / (1 + t²)` on `[-1, 1]` when
  `I ⊆ [-1, 1]` (in particular on the chart domain `|t| ≤ 1/2`), and otherwise the generic
  product `(2 · I) · (1 + I²)⁻¹` intersected with `[-1, 1]`. -/
def QInterval.circParam (I : QInterval) : QInterval × QInterval :=
  let d : QInterval := ((point 1).add I.sq).inv
  ((d.scale 2).sub (point 1),
    if -1 ≤ I.lo ∧ I.hi ≤ 1 then ⟨2 * I.lo / (1 + I.lo ^ 2), 2 * I.hi / (1 + I.hi ^ 2)⟩
    else ((I.scale 2).mul d).inter ⟨-1, 1⟩)

/-- Soundness of `QInterval.circParam`: both coordinates of `circParam t` are enclosed. -/
theorem QInterval.contains_circParam {I : QInterval} {t : ℝ} (ht : I.Contains t) :
    I.circParam.1.Contains (MetricChain.circParam t).1 ∧
      I.circParam.2.Contains (MetricChain.circParam t).2 := by
  have h1 : (QInterval.point 1).Contains (1 : ℝ) := QInterval.contains_point_of_eq (by norm_num)
  have hden : ((QInterval.point 1).add I.sq).Contains (1 + t ^ 2) :=
    QInterval.contains_add h1 (QInterval.contains_sq ht)
  have hpos : 0 < ((QInterval.point 1).add I.sq).lo := by
    have := I.sq_lo_nonneg
    simp only [QInterval.add, QInterval.point]
    linarith
  have hinv := QInterval.contains_inv hpos hden
  have hne : (1 + t ^ 2) ≠ 0 := by positivity
  constructor
  · have h2 := QInterval.contains_sub (QInterval.contains_scale 2 hinv) h1
    have he : (MetricChain.circParam t).1 = ((2 : ℚ) : ℝ) * (1 + t ^ 2)⁻¹ - 1 := by
      simp only [MetricChain.circParam]
      push_cast
      field_simp
      ring
    rw [he]
    exact h2
  · by_cases hI : -1 ≤ I.lo ∧ I.hi ≤ 1
    · have hlo : (-1 : ℝ) ≤ (I.lo : ℝ) := by exact_mod_cast hI.1
      have hhi : (I.hi : ℝ) ≤ 1 := by exact_mod_cast hI.2
      simp only [QInterval.circParam, if_pos hI, MetricChain.circParam]
      constructor
      · push_cast
        exact two_mul_div_one_add_sq_mono hlo ht.1 (ht.2.trans hhi)
      · push_cast
        exact two_mul_div_one_add_sq_mono (hlo.trans ht.1) ht.2 hhi
    · have h2 : ((I.scale 2).mul ((QInterval.point 1).add I.sq).inv).Contains
          (2 * t / (1 + t ^ 2)) := by
        have h3 := QInterval.contains_mul (QInterval.contains_scale 2 ht) hinv
        rw [div_eq_mul_inv]
        simpa using h3
      have h4 : (⟨-1, 1⟩ : QInterval).Contains (2 * t / (1 + t ^ 2)) := by
        have h5 := two_mul_div_one_add_sq_mem t
        constructor
        · simpa using h5.1
        · simpa using h5.2
      simp only [QInterval.circParam, if_neg hI, MetricChain.circParam]
      exact QInterval.contains_inter h2 h4

/-- Quarter turn acting on a pair of intervals. -/
def QInterval.quarterTurn : Fin 4 → QInterval × QInterval → QInterval × QInterval
  | 0, (A, B) => (A, B)
  | 1, (A, B) => (B.neg, A)
  | 2, (A, B) => (A.neg, B.neg)
  | 3, (A, B) => (B, A.neg)

/-- Soundness of `QInterval.quarterTurn`. -/
theorem QInterval.contains_quarterTurn (q : Fin 4) {P : QInterval × QInterval} {p : ℝ × ℝ}
    (h1 : P.1.Contains p.1) (h2 : P.2.Contains p.2) :
    (QInterval.quarterTurn q P).1.Contains (MetricChain.quarterTurn q p).1 ∧
      (QInterval.quarterTurn q P).2.Contains (MetricChain.quarterTurn q p).2 := by
  obtain ⟨A, B⟩ := P
  obtain ⟨a, b⟩ := p
  fin_cases q
  · exact ⟨h1, h2⟩
  · exact ⟨QInterval.contains_neg h2, h1⟩
  · exact ⟨QInterval.contains_neg h1, QInterval.contains_neg h2⟩
  · exact ⟨h2, QInterval.contains_neg h1⟩

/-- Interval enclosure of the chart `quarterTurn q ∘ circParam` of the circle atlas: a pair of
rational intervals enclosing `(cos θ, sin θ)` for the torsion coordinate `(q, t)`, `t ∈ I`. -/
def QInterval.circChart (q : Fin 4) (I : QInterval) : QInterval × QInterval :=
  QInterval.quarterTurn q I.circParam

/-- Soundness of `QInterval.circChart`. -/
theorem QInterval.contains_circChart (q : Fin 4) {I : QInterval} {t : ℝ} (ht : I.Contains t) :
    (QInterval.circChart q I).1.Contains
        (MetricChain.quarterTurn q (MetricChain.circParam t)).1 ∧
      (QInterval.circChart q I).2.Contains
        (MetricChain.quarterTurn q (MetricChain.circParam t)).2 :=
  QInterval.contains_quarterTurn q (QInterval.contains_circParam ht).1
    (QInterval.contains_circParam ht).2

/-! ## Part 5 — non-vacuity and executability

All data-level definitions above (everything except the real-number specification objects
`QInterval.Contains`, `circParam` and `quarterTurn`) are computable functions on `ℚ`.  The
examples below evaluate them with `norm_num` and with `decide +kernel`, i.e. `decide` whose
`Decidable` instance is evaluated by the kernel's own reduction (no compiled code is involved).
Plain `decide` gets stuck on *any* rational product because core Lean marks `Rat.mul`,
`Rat.add`, `Rat.sub`, `Rat.inv` as irreducible; it succeeds once these four are unsealed, as the
first examples of each group show. -/

section Examples

/-! ### Rounding -/

unseal Rat.mul Rat.inv Rat.add Rat.sub in
example : roundDown 4 (1 / 3) = 5 / 16 := by decide

unseal Rat.mul Rat.inv Rat.add Rat.sub in
example : roundUp 4 (1 / 3) = 3 / 8 := by decide

example : roundDown 4 (1 / 3) = 5 / 16 := by norm_num [roundDown]
example : roundUp 4 (1 / 3) = 3 / 8 := by norm_num [roundUp]
example : roundDown 4 (-1 / 3) = -3 / 8 := by decide +kernel
example : roundUp 4 (-1 / 3) = -5 / 16 := by decide +kernel

/-- The one-grid-step bound `roundUp_sub_roundDown_le` is attained. -/
example : roundUp 10 (1 / 3) - roundDown 10 (1 / 3) = 1 / 2 ^ 10 := by decide +kernel

/-! ### Interval arithmetic -/

unseal Rat.mul Rat.inv Rat.add Rat.sub in
example : QInterval.mul ⟨-1, 2⟩ ⟨3, 4⟩ = ⟨-4, 8⟩ := by decide

example : QInterval.mul ⟨-1, 2⟩ ⟨3, 4⟩ = ⟨-4, 8⟩ := by norm_num [QInterval.mul]
example : QInterval.sq ⟨-1 / 3, 2⟩ = ⟨0, 4⟩ := by decide +kernel
example : QInterval.inv ⟨1 / 3, 2⟩ = ⟨1 / 2, 3⟩ := by norm_num [QInterval.inv]
example : (QInterval.mul ⟨-1 / 3, 2⟩ ⟨4 / 7, 3⟩).outward 5 = ⟨-1, 6⟩ := by decide +kernel
example : QInterval.outward 4 ⟨1 / 3, 2 / 3⟩ = ⟨5 / 16, 11 / 16⟩ := by
  norm_num [QInterval.outward, roundDown, roundUp]
example : QInterval.sum (Finset.range 4) (fun i => ⟨i, i + 1 / 2⟩) = ⟨6, 8⟩ := by decide +kernel

/-- Soundness used on genuinely irrational data: `3 ≤ √2 · π ≤ 8`. -/
example : (QInterval.mul ⟨1, 2⟩ ⟨3, 4⟩).Contains (Real.sqrt 2 * Real.pi) :=
  QInterval.contains_mul (I := ⟨1, 2⟩) (J := ⟨3, 4⟩)
    ⟨by norm_num, by norm_num [Real.sqrt_le_iff]⟩
    ⟨by simpa using Real.pi_gt_three.le, by simpa using Real.pi_le_four⟩

/-! ### Exponential -/

example : expLo 8 1 1 = 1681189712449 / 618475290624 := by decide +kernel
example : expHi 8 1 1 = 2059457942325001 / 757632231014400 := by decide +kernel

example : (expLo 8 1 1 : ℚ) ≤ 2718281828 / 1000000000 ∧
    2718281829 / 1000000000 ≤ expHi 8 1 1 := by decide +kernel

example : (expLo 8 1 1 : ℚ) ≤ 2718281828 / 1000000000 ∧
    2718281829 / 1000000000 ≤ expHi 8 1 1 := by
  norm_num [expLo, expHi, expTaylor, expErr, Finset.sum_range_succ, Nat.factorial]

/-- Eight Taylor terms and one halving already enclose `e` to within `10⁻⁶`. -/
example : expHi 8 1 1 - expLo 8 1 1 ≤ 1 / 10 ^ 6 := by decide +kernel

/-- An instance of `exp_enclosure`. -/
example : ((expLo 8 1 1 : ℚ) : ℝ) ≤ Real.exp 1 ∧ Real.exp 1 ≤ ((expHi 8 1 1 : ℚ) : ℝ) := by
  simpa using exp_enclosure 8 1 (by norm_num) 1 (by norm_num)

/-- A numerical statement about the real number `e`, proved from `exp_enclosure` and two rational
comparisons checked by the kernel. -/
example : (2.7182 : ℝ) ≤ Real.exp 1 ∧ Real.exp 1 ≤ 2.7183 := by
  have hlo := le_exp_of_le_expLo (n := 8) (k := 1) (q := 1) (a := 27182 / 10000)
    (by norm_num) (by norm_num) (by decide +kernel)
  have hhi := exp_le_of_expHi_le (n := 8) (k := 1) (q := 1) (b := 27183 / 10000)
    (by norm_num) (by norm_num) (by decide +kernel)
  norm_num at hlo hhi ⊢
  exact ⟨hlo, hhi⟩

/-- Twelve Taylor terms, one halving and outward rounding to 30 fractional bits: the enclosure
of `e` is a single grid cell of width `2⁻³⁰`. -/
example : ((QInterval.point 1).exp 12 1).outward 30
    = ⟨2918732888 / 2 ^ 30, 2918732889 / 2 ^ 30⟩ := by decide +kernel

/-- A certified enclosure of `log 2`, checked through the rational `exp` bounds. -/
example : (0.693 : ℝ) ≤ Real.log 2 ∧ Real.log 2 ≤ 0.694 := by
  have hlo := le_log_of_expHi_le (n := 8) (k := 0) (a := 693 / 1000) (z := 2)
    (by norm_num) (by norm_num)
    (by exact_mod_cast (by decide +kernel : expHi 8 0 (693 / 1000) ≤ 2))
  have hhi := log_le_of_le_expLo (n := 8) (k := 0) (b := 694 / 1000) (z := 2)
    (by norm_num) (by norm_num) (by norm_num)
    (by exact_mod_cast (by decide +kernel : (2 : ℚ) ≤ expLo 8 0 (694 / 1000)))
  norm_num at hlo hhi ⊢
  exact ⟨hlo, hhi⟩

/-- A Boltzmann factor: for an energy `e ∈ [1, 3/2]` and `β = 2`, `exp (-β e) ∈ [0.0497, 0.1354]`
(the true range is `[exp (-3), exp (-2)] ≈ [0.04979, 0.13534]`). -/
example (e : ℝ) (he : (⟨1, 3 / 2⟩ : QInterval).Contains e) :
    (0.0497 : ℝ) ≤ Real.exp (-2 * e) ∧ Real.exp (-2 * e) ≤ 0.1354 := by
  have h := QInterval.contains_boltzmann (n := 12) (k := 2) (by norm_num) 2
    (by norm_num) (by norm_num) he
  have hlo := h.cast_le_of_le_lo (a := 497 / 10000) (by decide +kernel)
  have hhi := h.le_cast_of_hi_le (b := 1354 / 10000) (by decide +kernel)
  norm_num at hlo hhi ⊢
  exact ⟨hlo, hhi⟩

/-- A two-level partition function `Z = ∑ᵢ exp (-β Eᵢ)` with `β = 2`, `E₀ = 0` and an
interval-valued energy `E₁ ∈ [1, 3/2]`: `1.0497 ≤ Z ≤ 1.1354`. -/
example (E : Fin 2 → ℝ) (h0 : (QInterval.point 0).Contains (E 0))
    (h1 : (⟨1, 3 / 2⟩ : QInterval).Contains (E 1)) :
    (1.0497 : ℝ) ≤ ∑ i, Real.exp (-2 * E i) ∧ ∑ i, Real.exp (-2 * E i) ≤ 1.1354 := by
  have h := QInterval.contains_boltzmann_sum (n := 12) (k := 2) (by norm_num) 2
    (S := Finset.univ) (I := ![QInterval.point 0, ⟨1, 3 / 2⟩]) (E := E)
    (by intro i _; fin_cases i <;> norm_num [QInterval.point])
    (by intro i _; fin_cases i <;> norm_num [QInterval.point])
    (by intro i _; fin_cases i <;> assumption)
  have hlo := h.cast_le_of_le_lo (a := 10497 / 10000) (by decide +kernel)
  have hhi := h.le_cast_of_hi_le (b := 11354 / 10000) (by decide +kernel)
  norm_num at hlo hhi ⊢
  exact ⟨hlo, hhi⟩

/-- The same Boltzmann enclosure, outward-rounded to 20 fractional bits. -/
example : (((⟨1, 3 / 2⟩ : QInterval).scale (-2)).exp 12 2).outward 20
    = ⟨52205 / 1048576, 70955 / 524288⟩ := by decide +kernel

/-! ### Circle atlas -/

example : circParamQ (1 / 2) = (3 / 5, 4 / 5) := by norm_num [circParamQ]

example : (⟨1 / 4, 1 / 2⟩ : QInterval).circParam = (⟨3 / 5, 15 / 17⟩, ⟨8 / 17, 4 / 5⟩) := by
  decide +kernel

example : QInterval.circChart 1 ⟨1 / 4, 1 / 2⟩ = (⟨-4 / 5, -8 / 17⟩, ⟨3 / 5, 15 / 17⟩) := by
  decide +kernel

/-- Outside `[-1, 1]` the generic branch is used; the result still lies in `[-1, 1]²`. -/
example : (⟨-2, 3⟩ : QInterval).circParam = (⟨-4 / 5, 1⟩, ⟨-1, 1⟩) := by decide +kernel

example : quarterTurn 1 (circParam (1 / 3)) = (-3 / 5, 4 / 5) := by norm_num [circParam]

/-- An instance of `circle_rational_atlas`. -/
example : ∃ q : Fin 4, ∃ t : ℝ, |t| ≤ 1 / 2 ∧ quarterTurn q (circParam t) = (-4 / 5, 3 / 5) :=
  circle_rational_atlas _ _ (by norm_num)

end Examples

end MetricChain
