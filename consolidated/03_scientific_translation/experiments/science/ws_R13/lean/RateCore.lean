/-
Workstream R13 (science division) — the real-number core of the rate `τ_k − h ≤ c₁/(k + c₂)` for the level recursion
(theory report at 63e36f7, remark after Theorem 11.53; proof in the docstring of
`experiments/coordinator_checks/nested_review_R6/t4_rate.py`, paragraphs "Epoch" and "Closed form").

What is formalised here (Mathlib only; nothing about algorithms, nothing about the functions of the cube):

* `epoch_gain` — one epoch of the recursion `d ↦ d (J a + h)/(J a − h d)` with `d ≤ J < d + 1` raises `d` by at least
  `(J + 1) κ`, `κ = h² a/((a − h)(a + h)(2a − h))`, as soon as `d ≥ h/(a − h)`;
* `closed_form` — for the sequences `d_m`, `k_m` of statement (a) (`d_0 = h/(a − h)`, `k_0 = 1`, `d_m ≤ J_m < d_m + 1`,
  `d_{m+1} = d_m (J_m a + h)/(J_m a − h d_m)`, `k_{m+1} = k_m + J_m + 1`) and every level `n` with `k_m ≤ n < k_{m+1}`:
  `h/d_m ≤ c₁/(n + c₂)`, `c₁ = h (1 + κ)/κ`, `c₂ = (a + h)(2a − h)/(h a) − 2`;
* `rate_of_epochs` — the passage from the epoch property to the rate, for an abstract family of statements
  `P n b` ("`b` is an upper bound at level `n`"): if `P 1 a`, bounds persist to the next level and may be weakened,
  and the epoch property holds (`P n b`, `h < b`, `J = ⌈h/(b − h)⌉` imply `P (n + J + 1) (b J a/(J a + h))`), then
  `P n (h + c₁/(n + c₂))` for every `n ≥ 1`.

Not formalised in this file: that the level recursion has the epoch property (Lemma 1 and Lemma 2 of the proof, which
use `StepLE.of_limit` and `StepLE.of_macro`) — see `RateTop.lean` next to this file if it exists.
-/
import Mathlib

namespace ScienceR13

/-- `κ = h² a/((a − h)(a + h)(2a − h))`. -/
noncomputable def kappa (a h : ℝ) : ℝ := h ^ 2 * a / ((a - h) * (a + h) * (2 * a - h))

/-- `c₁ = h (1 + κ)/κ`. -/
noncomputable def c1 (a h : ℝ) : ℝ := h * (1 + kappa a h) / kappa a h

/-- `c₂ = (a + h)(2a − h)/(h a) − 2`. -/
noncomputable def c2 (a h : ℝ) : ℝ := (a + h) * (2 * a - h) / (h * a) - 2

theorem kappa_pos {a h : ℝ} (hh : 0 < h) (hah : h < a) : 0 < kappa a h := by
  unfold kappa
  have h1 : 0 < a - h := by linarith
  have h2 : 0 < a + h := by linarith
  have h3 : 0 < 2 * a - h := by linarith
  have ha : 0 < a := by linarith
  positivity

/-- `κ < d₀ = h/(a − h)`; equivalently `c₂ + 1 > 0`. -/
theorem kappa_lt_d0 {a h : ℝ} (hh : 0 < h) (hah : h < a) : kappa a h < h / (a - h) := by
  unfold kappa
  have h1 : 0 < a - h := by linarith
  have h2 : 0 < a + h := by linarith
  have h3 : 0 < 2 * a - h := by linarith
  have ha : 0 < a := by linarith
  rw [div_lt_div_iff₀ (by positivity) h1]
  nlinarith [mul_pos hh h1, mul_pos (mul_pos hh h1) (mul_pos ha ha), mul_pos (mul_pos hh h1) (mul_pos hh hh),
    mul_pos (mul_pos hh h1) (mul_pos ha (sub_pos.mpr hah))]

/-- `c₂ = d₀/κ − 2`. -/
theorem c2_eq {a h : ℝ} (hh : 0 < h) (hah : h < a) : c2 a h = h / (a - h) / kappa a h - 2 := by
  unfold c2 kappa
  have h1 : a - h ≠ 0 := by linarith
  have h2 : a + h ≠ 0 := by linarith
  have h3 : 2 * a - h ≠ 0 := by linarith
  have ha : a ≠ 0 := by linarith
  have hh' : h ≠ 0 := hh.ne'
  field_simp

/-- The polynomial inequality behind "the gain per level is at least `κ`": `h f(d) ≥ h f(d₀)` for `d ≥ d₀`. -/
theorem gain_poly {a h d : ℝ} (hh : 0 < h) (hah : h < a) (hd : h ≤ d * (a - h)) :
    (d + 2) * (d * (a - h) + a) * (h * a) ≤ d * (1 + d) * ((a - h) * (a + h) * (2 * a - h)) := by
  have h1 : 0 < a - h := by linarith
  have ha : 0 < a := by linarith
  have hd0 : 0 < d := by
    by_contra hcon
    rw [not_lt] at hcon
    nlinarith
  have hid : (a - h) * (d * (1 + d) * ((a - h) * (a + h) * (2 * a - h)) - (d + 2) * (d * (a - h) + a) * (h * a))
      = (d * (a - h) - h) * ((2 * a ^ 2 - h ^ 2) * d * (a - h) + 2 * (a - h) * a ^ 2) := by ring
  have hA : 0 < 2 * a ^ 2 - h ^ 2 := by nlinarith
  have hrhs : 0 ≤ (d * (a - h) - h) * ((2 * a ^ 2 - h ^ 2) * d * (a - h) + 2 * (a - h) * a ^ 2) := by
    apply mul_nonneg (by linarith)
    have : 0 < (2 * a ^ 2 - h ^ 2) * d * (a - h) := by positivity
    have : 0 < 2 * (a - h) * a ^ 2 := by positivity
    linarith
  rw [← hid] at hrhs
  have := nonneg_of_mul_nonneg_right hrhs h1
  linarith

/-- **One epoch.**  With `d ≥ d₀ = h/(a − h)` and `d ≤ J < d + 1`: the denominator is positive and
`d' − d ≥ (J + 1) κ` for `d' = d (J a + h)/(J a − h d)`. -/
theorem epoch_gain {a h d J : ℝ} (hh : 0 < h) (hah : h < a) (hd : h / (a - h) ≤ d) (hJ1 : d ≤ J) (hJ2 : J < d + 1) :
    0 < J * a - h * d ∧ (J + 1) * kappa a h ≤ d * (J * a + h) / (J * a - h * d) - d := by
  have h1 : 0 < a - h := by linarith
  have h2 : 0 < a + h := by linarith
  have h3 : 0 < 2 * a - h := by linarith
  have ha : 0 < a := by linarith
  have hd' : h ≤ d * (a - h) := by
    rw [div_le_iff₀ h1] at hd
    exact hd
  have hd0 : 0 < d := lt_of_lt_of_le (div_pos hh h1) hd
  have hden : 0 < J * a - h * d := by nlinarith
  refine ⟨hden, ?_⟩
  have hgain : d * (J * a + h) / (J * a - h * d) - d = d * h * (1 + d) / (J * a - h * d) := by
    have hne : J * a - h * d ≠ 0 := hden.ne'
    rw [eq_div_iff hne, sub_mul, div_mul_cancel₀ _ hne]
    ring
  rw [hgain, le_div_iff₀ hden]
  have hκ := kappa_pos hh hah
  have hD : 0 < (a - h) * (a + h) * (2 * a - h) := by positivity
  -- (J + 1) (J a − h d) ≤ (d + 2) (d (a − h) + a)
  have hprod : (J + 1) * (J * a - h * d) ≤ (d + 2) * (d * (a - h) + a) := by
    have e1 : J + 1 ≤ d + 2 := by linarith
    have e2 : J * a - h * d ≤ d * (a - h) + a := by nlinarith
    have e3 : 0 ≤ J + 1 := by linarith
    have e4 : 0 ≤ d * (a - h) + a := by positivity
    calc (J + 1) * (J * a - h * d) ≤ (J + 1) * (d * (a - h) + a) := mul_le_mul_of_nonneg_left e2 e3
      _ ≤ (d + 2) * (d * (a - h) + a) := mul_le_mul_of_nonneg_right e1 e4
  have hpoly := gain_poly hh hah hd'
  -- κ (d + 2)(d (a − h) + a) ≤ d h (1 + d)
  have hκle : kappa a h * ((d + 2) * (d * (a - h) + a)) ≤ d * h * (1 + d) := by
    unfold kappa
    rw [div_mul_eq_mul_div, div_le_iff₀ hD]
    nlinarith
  calc (J + 1) * kappa a h * (J * a - h * d) = kappa a h * ((J + 1) * (J * a - h * d)) := by ring
    _ ≤ kappa a h * ((d + 2) * (d * (a - h) + a)) := mul_le_mul_of_nonneg_left hprod hκ.le
    _ ≤ d * h * (1 + d) := hκle

/-- **The closed form dominates the epoch recursion.** -/
theorem closed_form {a h : ℝ} (hh : 0 < h) (hah : h < a) (d : ℕ → ℝ) (k J : ℕ → ℕ)
    (hd0 : d 0 = h / (a - h)) (hk0 : k 0 = 1)
    (hJ : ∀ m, d m ≤ J m ∧ (J m : ℝ) < d m + 1)
    (hd : ∀ m, d (m + 1) = d m * (J m * a + h) / (J m * a - h * d m))
    (hk : ∀ m, k (m + 1) = k m + J m + 1) :
    ∀ m n : ℕ, k m ≤ n → n < k (m + 1) → h / d m ≤ c1 a h / (n + c2 a h) := by
  have h1 : 0 < a - h := by linarith
  have hκ := kappa_pos hh hah
  have hκd := kappa_lt_d0 hh hah
  have hd0pos : 0 < h / (a - h) := div_pos hh h1
  -- d_m ≥ d_0 + κ (k_m − 1)
  have hlin : ∀ m, h / (a - h) ≤ d m ∧ h / (a - h) + kappa a h * ((k m : ℝ) - 1) ≤ d m := by
    intro m
    induction m with
    | zero =>
      rw [hd0, hk0]
      constructor
      · exact le_rfl
      · simp
    | succ m ih =>
      obtain ⟨ih1, ih2⟩ := ih
      obtain ⟨_, hg⟩ := epoch_gain hh hah ih1 (hJ m).1 (hJ m).2
      rw [← hd m] at hg
      have hJ0 : (0 : ℝ) ≤ J m := Nat.cast_nonneg _
      have hk' : ((k (m + 1) : ℕ) : ℝ) = (k m : ℝ) + (J m : ℝ) + 1 := by
        rw [hk m]; push_cast; ring
      constructor
      · nlinarith [mul_nonneg (by linarith : (0 : ℝ) ≤ (J m : ℝ) + 1) hκ.le]
      · rw [hk']
        nlinarith
  intro m n hmn hnk
  obtain ⟨hm1, hm2⟩ := hlin m
  have hdm : 0 < d m := lt_of_lt_of_le hd0pos hm1
  -- n ≤ k_m + J_m < k_m + d_m + 1
  have hn1 : (n : ℝ) ≤ (k m : ℝ) + (J m : ℝ) := by
    have : n ≤ k m + J m := by
      rw [hk m] at hnk
      omega
    exact_mod_cast this
  have hn2 : (n : ℝ) - (k m : ℝ) - 1 < d m := by linarith [(hJ m).2]
  have hkey : kappa a h * ((n : ℝ) - 2) + h / (a - h) ≤ (1 + kappa a h) * d m := by
    nlinarith
  -- positivity of the denominator: n ≥ 1
  have hk1 : ∀ m, 1 ≤ k m := by
    intro m
    induction m with
    | zero => rw [hk0]
    | succ m ih => rw [hk m]; omega
  have hn0 : (1 : ℝ) ≤ n := by
    have : 1 ≤ n := le_trans (hk1 m) hmn
    exact_mod_cast this
  have hpos : 0 < kappa a h * ((n : ℝ) - 2) + h / (a - h) := by nlinarith
  have hden : (n : ℝ) + c2 a h = (kappa a h * ((n : ℝ) - 2) + h / (a - h)) / kappa a h := by
    rw [c2_eq hh hah]
    field_simp
    ring
  have hrw : c1 a h / ((n : ℝ) + c2 a h) = h * (1 + kappa a h) / (kappa a h * ((n : ℝ) - 2) + h / (a - h)) := by
    rw [hden]
    unfold c1
    field_simp
  rw [hrw, div_le_div_iff₀ hdm hpos]
  nlinarith

/-- The sequences of statement (a), built with `J = ⌈d⌉`. -/
noncomputable def epochSeq (a h : ℝ) : ℕ → ℝ × ℕ
  | 0 => (h / (a - h), 1)
  | m + 1 =>
    let p := epochSeq a h m
    (p.1 * ((⌈p.1⌉₊ : ℝ) * a + h) / ((⌈p.1⌉₊ : ℝ) * a - h * p.1), p.2 + ⌈p.1⌉₊ + 1)

/-- **From the epoch property to the rate.**  `P n b` is read "`b` is an upper bound at level `n`". -/
theorem rate_of_epochs {a h : ℝ} (hh : 0 < h) (hah : h < a) (P : ℕ → ℝ → Prop)
    (hstep : ∀ n b, 1 ≤ n → P n b → P (n + 1) b)
    (hweak : ∀ n b b', P n b → b ≤ b' → P n b')
    (hP1 : P 1 a)
    (hep : ∀ (n : ℕ) (b : ℝ), 1 ≤ n → P n b → h < b →
      P (n + ⌈h / (b - h)⌉₊ + 1) (b * ((⌈h / (b - h)⌉₊ : ℝ) * a) / ((⌈h / (b - h)⌉₊ : ℝ) * a + h))) :
    ∀ n : ℕ, 1 ≤ n → P n (h + c1 a h / (n + c2 a h)) := by
  have h1 : 0 < a - h := by linarith
  have ha : 0 < a := by linarith
  set d : ℕ → ℝ := fun m => (epochSeq a h m).1 with hddef
  set k : ℕ → ℕ := fun m => (epochSeq a h m).2 with hkdef
  set J : ℕ → ℕ := fun m => ⌈d m⌉₊ with hJdef
  have hd0 : d 0 = h / (a - h) := rfl
  have hk0 : k 0 = 1 := rfl
  have hdS : ∀ m, d (m + 1) = d m * (J m * a + h) / (J m * a - h * d m) := fun m => rfl
  have hkS : ∀ m, k (m + 1) = k m + J m + 1 := fun m => rfl
  -- d_m ≥ d_0 > 0, hence the ceiling property
  have hdge : ∀ m, h / (a - h) ≤ d m := by
    intro m
    induction m with
    | zero => exact le_of_eq hd0.symm
    | succ m ih =>
      have hd0pos : 0 < h / (a - h) := div_pos hh h1
      have hJm : d m ≤ J m ∧ (J m : ℝ) < d m + 1 :=
        ⟨Nat.le_ceil _, Nat.ceil_lt_add_one (le_trans hd0pos.le ih)⟩
      obtain ⟨_, hg⟩ := epoch_gain hh hah ih hJm.1 hJm.2
      rw [← hdS m] at hg
      have hκ := kappa_pos hh hah
      have hJ0 : (0 : ℝ) ≤ J m := Nat.cast_nonneg _
      nlinarith [mul_nonneg (by linarith : (0 : ℝ) ≤ (J m : ℝ) + 1) hκ.le]
  have hd0pos : 0 < h / (a - h) := div_pos hh h1
  have hJ : ∀ m, d m ≤ J m ∧ (J m : ℝ) < d m + 1 := fun m =>
    ⟨Nat.le_ceil _, Nat.ceil_lt_add_one (le_trans hd0pos.le (hdge m))⟩
  have hk1 : ∀ m, 1 ≤ k m := by
    intro m
    induction m with
    | zero => rw [hk0]
    | succ m ih => rw [hkS m]; omega
  -- the bound at the beginning of every epoch
  have hPk : ∀ m, P (k m) (h * (1 + 1 / d m)) := by
    intro m
    induction m with
    | zero =>
      rw [hk0, hd0]
      have e : h * (1 + 1 / (h / (a - h))) = a := by
        field_simp
        ring
      rw [e]
      exact hP1
    | succ m ih =>
      have hdm : 0 < d m := lt_of_lt_of_le hd0pos (hdge m)
      have hb : h < h * (1 + 1 / d m) := by
        have : 0 < 1 / d m := by positivity
        nlinarith
      have hceil : h / (h * (1 + 1 / d m) - h) = d m := by
        field_simp
        ring
      have key := hep (k m) (h * (1 + 1 / d m)) (hk1 m) ih hb
      rw [hceil] at key
      obtain ⟨hden, _⟩ := epoch_gain hh hah (hdge m) (hJ m).1 (hJ m).2
      have hJpos : (0 : ℝ) < J m := lt_of_lt_of_le hdm (hJ m).1
      have e : h * (1 + 1 / d m) * ((J m : ℝ) * a) / ((J m : ℝ) * a + h) = h * (1 + 1 / d (m + 1)) := by
        rw [hdS m]
        have hne1 : (J m : ℝ) * a - h * d m ≠ 0 := hden.ne'
        have hne2 : (J m : ℝ) * a + h ≠ 0 := by positivity
        have hne3 : d m ≠ 0 := hdm.ne'
        field_simp
        ring
      rw [hkS m]
      rw [← e]
      exact key
  -- persistence along levels
  have hpers : ∀ n n' b, 1 ≤ n → n ≤ n' → P n b → P n' b := by
    intro n n' b hn hnn' hP
    induction hnn' with
    | refl => exact hP
    | step hle ih => exact hstep _ b (le_trans hn hle) ih
  -- every level lies in an epoch
  have hkmono : ∀ m, m + 1 ≤ k m := by
    intro m
    induction m with
    | zero => rw [hk0]
    | succ m ih => rw [hkS m]; omega
  intro n hn
  have hex : ∃ m, n < k (m + 1) := ⟨n, by have := hkmono (n + 1); omega⟩
  classical
  set m := Nat.find hex with hmdef
  have hm : n < k (m + 1) := Nat.find_spec hex
  have hm' : k m ≤ n := by
    by_cases hm0 : m = 0
    · rw [hm0, hk0]; exact hn
    · obtain ⟨m', hm'⟩ := Nat.exists_eq_succ_of_ne_zero hm0
      have := Nat.find_min hex (m := m') (by omega)
      rw [not_lt] at this
      rw [hm']
      exact this
  have hdm : 0 < d m := lt_of_lt_of_le hd0pos (hdge m)
  have hcf := closed_form hh hah d k J hd0 hk0 hJ hdS hkS m n hm' hm
  refine hweak n _ _ (hpers (k m) n _ (hk1 m) hm' (hPk m)) ?_
  have e : h * (1 + 1 / d m) = h + h / d m := by
    field_simp
  rw [e]
  linarith

end ScienceR13

#print axioms ScienceR13.epoch_gain
#print axioms ScienceR13.closed_form
#print axioms ScienceR13.rate_of_epochs
