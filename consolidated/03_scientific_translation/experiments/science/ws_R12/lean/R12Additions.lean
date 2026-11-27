/-
Workstream R12 of the Scientific Discovery Division (review of the theory division's seventeenth
checkpoint, branch at 9408e33).  NOT part of the `MetricChain` library.

Statements that the review proposes to the theory division (R12_REPORT §1: M1, m1, m3, m5):

* `detect_ge_at_floor`, `detect_ge_at_ceiling` — the detection lemma of Theorem 11.110(c) in the two cases
  that `BoxClass.detect_ge` excludes by its hypotheses `hU`, `hV`: at the floor of the box (total dip weight
  zero) every far member differs from `r` on a set of bump-probability at least `(1 - e^{-η}) Z / V`, without
  the factor one half; at the ceiling the same with dips.
* `detect_ge_weighted`, `weighted_opt` — the sampler `λ dip/U + (1 - λ) bump/V` detects with probability at
  least `min (λ (e^η - 1) Z / U, (1 - λ)(1 - e^{-η}) Z / V)`; with `λ = A/(A + B)`, `A = U/((e^η - 1) Z)`,
  `B = V/((1 - e^{-η}) Z)`, this is `1/(A + B)`: the sample size is the SUM of the two terms, not twice the
  larger one.
* `logRatio_bumpAlt_lt`, `logRatio_bumpAlt_gt` — the alternative missing from `BoxRatio.lean`: raising the
  remainder to the ceiling on a set that avoids one macrostate and whose bump weight inside the other
  exceeds `(1 - e^{-ε})` times that macrostate's weight changes the log-ratio by more than `ε`.
* `affine_half_large` — the core of the counter-algorithm to Proposition 11.18e(b) on the cube for order
  below two: an affine function on `{-1, 1}^n` is at least `1/(n + 1)` of its maximum in absolute value on
  at least half of the points (so `q` uniformly random evaluations miss its scale with probability at most
  `2^{-q}`, whatever `n`).

The definitions `Box`, `Zw`, `dip`, `bump`, `bumpAlt`, `restr`, `logRatio` and the lemmas `dip_nonneg`,
`bump_nonneg`, `Zw_pos`, `Zw_sub_le_dip`, `Zw_sub_le_bump`, `Zw_bumpAlt`, `restr_*` are COPIED from the
theory division's `proofs/Frontiers/BoxClass.lean` and `BoxRatio.lean` (their statements and proofs), in a
namespace of our own, because those files are not modules of our tree.  New here: the seven theorems above
(and their auxiliary lemmas).

Check with:  lake env lean experiments/science/ws_R12/lean/R12Additions.lean
-/
import Mathlib

namespace ScienceR12

open Finset

variable {X : Type*} [Fintype X]

/-! ### Copied definitions and lemmas (theory division, `BoxClass.lean`, `BoxRatio.lean`) -/

def Box (lo hi : X → ℝ) (r : X → ℝ) : Prop := ∀ x, lo x ≤ r x ∧ r x ≤ hi x

noncomputable def Zw (w r : X → ℝ) : ℝ := ∑ x, w x * Real.exp (-r x)

noncomputable def dip (w lo r : X → ℝ) (x : X) : ℝ := w x * (Real.exp (-lo x) - Real.exp (-r x))

noncomputable def bump (w hi r : X → ℝ) (x : X) : ℝ := w x * (Real.exp (-r x) - Real.exp (-hi x))

omit [Fintype X] in
theorem dip_nonneg {w lo hi r : X → ℝ} (hw : ∀ x, 0 ≤ w x) (hr : Box lo hi r) (x : X) : 0 ≤ dip w lo r x := by
  unfold dip
  exact mul_nonneg (hw x) (sub_nonneg.mpr (Real.exp_le_exp.mpr (by linarith [(hr x).1])))

omit [Fintype X] in
theorem bump_nonneg {w lo hi r : X → ℝ} (hw : ∀ x, 0 ≤ w x) (hr : Box lo hi r) (x : X) : 0 ≤ bump w hi r x := by
  unfold bump
  exact mul_nonneg (hw x) (sub_nonneg.mpr (Real.exp_le_exp.mpr (by linarith [(hr x).2])))

theorem Zw_pos {w r : X → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀) : 0 < Zw w r := by
  unfold Zw
  refine Finset.sum_pos' (fun x _ => mul_nonneg (hw x) (Real.exp_pos _).le) ⟨x₀, mem_univ x₀, ?_⟩
  exact mul_pos hx₀ (Real.exp_pos _)

open Classical in
theorem Zw_sub_le_dip {w lo hi r r' : X → ℝ} (hw : ∀ x, 0 ≤ w x) (hr' : Box lo hi r') :
    Zw w r' - Zw w r ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x := by
  unfold Zw
  rw [← Finset.sum_sub_distrib, Finset.sum_filter]
  refine Finset.sum_le_sum fun x _ => ?_
  by_cases h : r' x = r x
  · simp [h]
  · rw [if_pos h]
    unfold dip
    have : Real.exp (-r' x) ≤ Real.exp (-lo x) := Real.exp_le_exp.mpr (by linarith [(hr' x).1])
    nlinarith [hw x]

open Classical in
theorem Zw_sub_le_bump {w lo hi r r' : X → ℝ} (hw : ∀ x, 0 ≤ w x) (hr' : Box lo hi r') :
    Zw w r - Zw w r' ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x := by
  unfold Zw
  rw [← Finset.sum_sub_distrib, Finset.sum_filter]
  refine Finset.sum_le_sum fun x _ => ?_
  by_cases h : r' x = r x
  · simp [h]
  · rw [if_pos h]
    unfold bump
    have : Real.exp (-hi x) ≤ Real.exp (-r' x) := Real.exp_le_exp.mpr (by linarith [(hr' x).2])
    nlinarith [hw x]

open Classical in
noncomputable def bumpAlt (hi r : X → ℝ) (D : Finset X) (x : X) : ℝ := if x ∈ D then hi x else r x

theorem Zw_bumpAlt (w hi r : X → ℝ) (D : Finset X) :
    Zw w (bumpAlt hi r D) = Zw w r - ∑ x ∈ D, bump w hi r x := by
  classical
  unfold Zw
  have h1 : ∑ x ∈ D, bump w hi r x = ∑ x, if x ∈ D then bump w hi r x else 0 := by
    rw [Finset.sum_ite_mem, Finset.univ_inter]
  rw [h1, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun x _ => ?_
  unfold bumpAlt bump
  by_cases h : x ∈ D
  · rw [if_pos h, if_pos h]; ring
  · rw [if_neg h, if_neg h]; ring

open Classical in
noncomputable def restr (w : X → ℝ) (M : Finset X) (x : X) : ℝ := if x ∈ M then w x else 0

omit [Fintype X] in
theorem restr_nonneg {w : X → ℝ} (hw : ∀ x, 0 ≤ w x) (M : Finset X) (x : X) : 0 ≤ restr w M x := by
  unfold restr
  split_ifs
  · exact hw x
  · exact le_rfl

omit [Fintype X] in
theorem restr_pos {w : X → ℝ} {M : Finset X} {a : X} (ha : a ∈ M) (hwa : 0 < w a) : 0 < restr w M a := by
  unfold restr
  rwa [if_pos ha]

omit [Fintype X] in
theorem restr_eq_zero {w : X → ℝ} {M : Finset X} {x : X} (hx : x ∉ M) : restr w M x = 0 := by
  unfold restr
  rw [if_neg hx]

noncomputable def logRatio (w : X → ℝ) (A B : Finset X) (r : X → ℝ) : ℝ :=
  Real.log (Zw (restr w A) r) - Real.log (Zw (restr w B) r)

/-! ### New (R12): detection at the floor and at the ceiling of the box -/

open Classical in
/-- **Detection at the floor.**  If the total dip weight at `r` is zero (the instance is at the floor of the
box wherever the known measure has mass), every member of the box whose `log Z` differs from that of `r` by
more than `η ≥ 0` differs from `r` on a set of probability at least `(1 - e^{-η}) Z / V` under the bump
sampler `bump / V` — the bound of `BoxClass.detect_ge` without the factor one half. -/
theorem detect_ge_at_floor {w lo hi r r' : X → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀)
    (hr : Box lo hi r) (hr' : Box lo hi r')
    (hU : ∑ y, dip w lo r y = 0) (hV : 0 < ∑ y, bump w hi r y) {η : ℝ} (hη : 0 ≤ η)
    (hfar : η < |Real.log (Zw w r') - Real.log (Zw w r)|) :
    (1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y
      ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x / ∑ y, bump w hi r y := by
  have hZ : 0 < Zw w r := Zw_pos hw hx₀
  have hZ' : 0 < Zw w r' := Zw_pos hw hx₀
  -- the partition sum cannot go up: the dips of the difference set are part of a total that is zero
  have hle : Zw w r' ≤ Zw w r := by
    have h1 := Zw_sub_le_dip (r := r) hw hr'
    have h2 : ∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x ≤ ∑ y, dip w lo r y :=
      Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _) fun y _ _ => dip_nonneg hw hr y
    linarith
  have hlogle : Real.log (Zw w r') ≤ Real.log (Zw w r) := Real.log_le_log hZ' hle
  rw [← Finset.sum_div]
  rcases lt_abs.mp hfar with h | h
  · exfalso; linarith
  · have h1' : Real.log (Zw w r') < Real.log (Zw w r) + -η := by linarith
    have h2 : Zw w r' < Zw w r * Real.exp (-η) := by
      have := Real.exp_lt_exp.mpr h1'
      rwa [Real.exp_add, Real.exp_log hZ, Real.exp_log hZ'] at this
    have h3 : (1 - Real.exp (-η)) * Zw w r ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x := by
      have := Zw_sub_le_bump (r := r) hw hr'
      nlinarith
    exact div_le_div_of_nonneg_right h3 hV.le

open Classical in
/-- **Detection at the ceiling.**  If the total bump weight at `r` is zero, every member of the box whose
`log Z` differs from that of `r` by more than `η ≥ 0` differs from `r` on a set of probability at least
`(e^η - 1) Z / U` under the dip sampler `dip / U`. -/
theorem detect_ge_at_ceiling {w lo hi r r' : X → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀)
    (hr : Box lo hi r) (hr' : Box lo hi r')
    (hU : 0 < ∑ y, dip w lo r y) (hV : ∑ y, bump w hi r y = 0) {η : ℝ} (hη : 0 ≤ η)
    (hfar : η < |Real.log (Zw w r') - Real.log (Zw w r)|) :
    (Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y
      ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x / ∑ y, dip w lo r y := by
  have hZ : 0 < Zw w r := Zw_pos hw hx₀
  have hZ' : 0 < Zw w r' := Zw_pos hw hx₀
  have hge : Zw w r ≤ Zw w r' := by
    have h1 := Zw_sub_le_bump (r := r) hw hr'
    have h2 : ∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x ≤ ∑ y, bump w hi r y :=
      Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _) fun y _ _ => bump_nonneg hw hr y
    linarith
  have hlogle : Real.log (Zw w r) ≤ Real.log (Zw w r') := Real.log_le_log hZ hge
  rw [← Finset.sum_div]
  rcases lt_abs.mp hfar with h | h
  · have h1 : Real.log (Zw w r) + η < Real.log (Zw w r') := by linarith
    have h2 : Zw w r * Real.exp η < Zw w r' := by
      have := Real.exp_lt_exp.mpr h1
      rwa [Real.exp_add, Real.exp_log hZ, Real.exp_log hZ'] at this
    have h3 : (Real.exp η - 1) * Zw w r ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x := by
      have := Zw_sub_le_dip (r := r) hw hr'
      nlinarith
    exact div_le_div_of_nonneg_right h3 hU.le
  · exfalso; linarith

/-! ### New (R12): a weighted mixture of the two samplers -/

/-- The sampler with weight `lam` on the dips and `1 - lam` on the bumps (`lam = 1/2` is `BoxClass.sampler`). -/
noncomputable def samplerW (lam : ℝ) (w lo hi r : X → ℝ) (x : X) : ℝ :=
  lam * (dip w lo r x / ∑ y, dip w lo r y) + (1 - lam) * (bump w hi r x / ∑ y, bump w hi r y)

theorem samplerW_nonneg {lam : ℝ} (h0 : 0 ≤ lam) (h1 : lam ≤ 1) {w lo hi r : X → ℝ} (hw : ∀ x, 0 ≤ w x)
    (hr : Box lo hi r) (x : X) : 0 ≤ samplerW lam w lo hi r x := by
  unfold samplerW
  have hd : 0 ≤ dip w lo r x / ∑ y, dip w lo r y :=
    div_nonneg (dip_nonneg hw hr x) (Finset.sum_nonneg fun y _ => dip_nonneg hw hr y)
  have hb : 0 ≤ bump w hi r x / ∑ y, bump w hi r y :=
    div_nonneg (bump_nonneg hw hr x) (Finset.sum_nonneg fun y _ => bump_nonneg hw hr y)
  have hl : 0 ≤ 1 - lam := by linarith
  have := mul_nonneg h0 hd
  have := mul_nonneg hl hb
  linarith

theorem samplerW_sum {lam : ℝ} {w lo hi r : X → ℝ} (hU : 0 < ∑ y, dip w lo r y)
    (hV : 0 < ∑ y, bump w hi r y) : ∑ x, samplerW lam w lo hi r x = 1 := by
  unfold samplerW
  rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.sum_div, ← Finset.sum_div,
    div_self hU.ne', div_self hV.ne']
  ring

open Classical in
/-- **Detection with a weighted mixture.**  Every member of the box whose `log Z` differs from that of `r` by
more than `η` differs from `r` on a set of probability at least
`min (lam (e^η - 1) Z / U, (1 - lam)(1 - e^{-η}) Z / V)` under `samplerW lam`. -/
theorem detect_ge_weighted {lam : ℝ} (h0 : 0 ≤ lam) (h1 : lam ≤ 1) {w lo hi r r' : X → ℝ}
    (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀) (hr : Box lo hi r) (hr' : Box lo hi r')
    (hU : 0 < ∑ y, dip w lo r y) (hV : 0 < ∑ y, bump w hi r y) {η : ℝ}
    (hfar : η < |Real.log (Zw w r') - Real.log (Zw w r)|) :
    min (lam * ((Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y))
        ((1 - lam) * ((1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y))
      ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), samplerW lam w lo hi r x := by
  have hZ : 0 < Zw w r := Zw_pos hw hx₀
  have hZ' : 0 < Zw w r' := Zw_pos hw hx₀
  have hl : 0 ≤ 1 - lam := by linarith
  have hsum : ∑ x ∈ univ.filter (fun x => r' x ≠ r x), samplerW lam w lo hi r x
      = lam * ((∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x) / ∑ y, dip w lo r y)
        + (1 - lam) * ((∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x) / ∑ y, bump w hi r y) := by
    unfold samplerW
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.sum_div, ← Finset.sum_div]
  have hd0 : 0 ≤ (∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x) / ∑ y, dip w lo r y :=
    div_nonneg (Finset.sum_nonneg fun y _ => dip_nonneg hw hr y) hU.le
  have hb0 : 0 ≤ (∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x) / ∑ y, bump w hi r y :=
    div_nonneg (Finset.sum_nonneg fun y _ => bump_nonneg hw hr y) hV.le
  rw [hsum]
  rcases lt_abs.mp hfar with h | h
  · have h1' : Real.log (Zw w r) + η < Real.log (Zw w r') := by linarith
    have h2 : Zw w r * Real.exp η < Zw w r' := by
      have := Real.exp_lt_exp.mpr h1'
      rwa [Real.exp_add, Real.exp_log hZ, Real.exp_log hZ'] at this
    have h3 : (Real.exp η - 1) * Zw w r ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x := by
      have := Zw_sub_le_dip (r := r) hw hr'
      nlinarith
    have h4 : (Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y
        ≤ (∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x) / ∑ y, dip w lo r y :=
      div_le_div_of_nonneg_right h3 hU.le
    have h5 := min_le_left (lam * ((Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y))
      ((1 - lam) * ((1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y))
    have h6 := mul_le_mul_of_nonneg_left h4 h0
    have h7 := mul_nonneg hl hb0
    linarith
  · have h1' : Real.log (Zw w r') < Real.log (Zw w r) + -η := by linarith
    have h2 : Zw w r' < Zw w r * Real.exp (-η) := by
      have := Real.exp_lt_exp.mpr h1'
      rwa [Real.exp_add, Real.exp_log hZ, Real.exp_log hZ'] at this
    have h3 : (1 - Real.exp (-η)) * Zw w r ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x := by
      have := Zw_sub_le_bump (r := r) hw hr'
      nlinarith
    have h4 : (1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y
        ≤ (∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x) / ∑ y, bump w hi r y :=
      div_le_div_of_nonneg_right h3 hV.le
    have h5 := min_le_right (lam * ((Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y))
      ((1 - lam) * ((1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y))
    have h6 := mul_le_mul_of_nonneg_left h4 hl
    have h7 := mul_nonneg h0 hd0
    linarith

/-- **The best weights.**  With `A = U/((e^η - 1) Z)` and `B = V/((1 - e^{-η}) Z)` the two terms of
`detect_ge_weighted` are `lam / A` and `(1 - lam) / B`; at `lam = A/(A + B)` both equal `1/(A + B)`. -/
theorem weighted_opt {A B : ℝ} (hA : 0 < A) (hB : 0 < B) :
    min (A / (A + B) * (1 / A)) ((1 - A / (A + B)) * (1 / B)) = 1 / (A + B) := by
  have hAB : 0 < A + B := by linarith
  have e1 : A / (A + B) * (1 / A) = 1 / (A + B) := by
    field_simp
  have e3 : 1 - A / (A + B) = B / (A + B) := by
    field_simp
    ring
  have e2 : (1 - A / (A + B)) * (1 / B) = 1 / (A + B) := by
    rw [e3]
    field_simp
  rw [e1, e2, min_self]

/-! ### New (R12): the bump alternative for a ratio of two macrostate weights -/

/-- Raising the remainder on a set that does not meet a macrostate does not change the weight of that
macrostate. -/
theorem Zw_restr_bumpAlt_of_disjoint (w hi r : X → ℝ) {M D : Finset X} (hD : ∀ x ∈ D, x ∉ M) :
    Zw (restr w M) (bumpAlt hi r D) = Zw (restr w M) r := by
  rw [Zw_bumpAlt]
  have : ∑ x ∈ D, bump (restr w M) hi r x = 0 := by
    refine Finset.sum_eq_zero fun x hx => ?_
    unfold bump
    rw [restr_eq_zero (hD x hx), zero_mul]
  rw [this, sub_zero]

/-- A set that avoids `B` and whose bump weight inside `A` exceeds `(1 - e^{-ε}) Z_A` lowers the log-ratio
`log (Z_A / Z_B)` by more than `ε` when the remainder is raised to the ceiling on it. -/
theorem logRatio_bumpAlt_lt {w hi r : X → ℝ} (hw : ∀ x, 0 ≤ w x) {A B : Finset X} {a : X} (ha : a ∈ A)
    (hwa : 0 < w a) {D : Finset X} (hDB : ∀ x ∈ D, x ∉ B) {ε : ℝ}
    (hD : (1 - Real.exp (-ε)) * Zw (restr w A) r < ∑ x ∈ D, bump (restr w A) hi r x) :
    ε < logRatio w A B r - logRatio w A B (bumpAlt hi r D) := by
  have hZ : 0 < Zw (restr w A) r := Zw_pos (restr_nonneg hw A) (restr_pos ha hwa)
  have hZ' : 0 < Zw (restr w A) (bumpAlt hi r D) := Zw_pos (restr_nonneg hw A) (restr_pos ha hwa)
  have hlt : Zw (restr w A) (bumpAlt hi r D) < Real.exp (-ε) * Zw (restr w A) r := by
    rw [Zw_bumpAlt]; nlinarith
  have hlog : Real.log (Zw (restr w A) (bumpAlt hi r D)) < -ε + Real.log (Zw (restr w A) r) := by
    have h := Real.log_lt_log hZ' hlt
    rwa [Real.log_mul (Real.exp_pos _).ne' hZ.ne', Real.log_exp] at h
  unfold logRatio
  rw [Zw_restr_bumpAlt_of_disjoint w hi r hDB]
  linarith

/-- The same in the other macrostate: the log-ratio rises by more than `ε`. -/
theorem logRatio_bumpAlt_gt {w hi r : X → ℝ} (hw : ∀ x, 0 ≤ w x) {A B : Finset X} {b : X} (hb : b ∈ B)
    (hwb : 0 < w b) {D : Finset X} (hDA : ∀ x ∈ D, x ∉ A) {ε : ℝ}
    (hD : (1 - Real.exp (-ε)) * Zw (restr w B) r < ∑ x ∈ D, bump (restr w B) hi r x) :
    ε < logRatio w A B (bumpAlt hi r D) - logRatio w A B r := by
  have hZ : 0 < Zw (restr w B) r := Zw_pos (restr_nonneg hw B) (restr_pos hb hwb)
  have hZ' : 0 < Zw (restr w B) (bumpAlt hi r D) := Zw_pos (restr_nonneg hw B) (restr_pos hb hwb)
  have hlt : Zw (restr w B) (bumpAlt hi r D) < Real.exp (-ε) * Zw (restr w B) r := by
    rw [Zw_bumpAlt]; nlinarith
  have hlog : Real.log (Zw (restr w B) (bumpAlt hi r D)) < -ε + Real.log (Zw (restr w B) r) := by
    have h := Real.log_lt_log hZ' hlt
    rwa [Real.log_mul (Real.exp_pos _).ne' hZ.ne', Real.log_exp] at h
  unfold logRatio
  rw [Zw_restr_bumpAlt_of_disjoint w hi r hDA]
  linarith

/-! ### New (R12): the core of the counter-algorithm to Proposition 11.18e(b), on the cube, order below two

An affine function `h(s) = α + ∑ β_i s_i` on the cube `{-1, 1}^n` has absolute value at least
`max |h| / (n + 1)` on at least half of the points.  Hence `q` uniformly random evaluations fail to
show the scale of `h` with probability at most `2^{-q}`, for every `h` — whatever `n`. -/

/-- The sign `±1` of a Boolean coordinate. -/
noncomputable def sgn (b : Bool) : ℝ := if b then 1 else -1

theorem sgn_true : sgn true = 1 := by simp [sgn]

theorem sgn_false : sgn false = -1 := by simp [sgn]

theorem sgn_not (b : Bool) : sgn (!b) = -sgn b := by
  cases b
  · rw [Bool.not_false, sgn_true, sgn_false]; ring
  · rw [Bool.not_true, sgn_true, sgn_false]

theorem abs_sgn (b : Bool) : |sgn b| = 1 := by
  cases b
  · rw [sgn_false]; norm_num
  · rw [sgn_true]; norm_num

theorem abs_two_mul_sgn (x : ℝ) (b : Bool) : |-2 * x * sgn b| = 2 * |x| := by
  cases b
  · rw [sgn_false, show (-2 * x * -1 : ℝ) = 2 * x by ring, abs_mul,
      abs_of_pos (by norm_num : (0 : ℝ) < 2)]
  · rw [sgn_true, show (-2 * x * 1 : ℝ) = -(2 * x) by ring, abs_neg, abs_mul,
      abs_of_pos (by norm_num : (0 : ℝ) < 2)]

/-- An affine function on the cube, in Boolean coordinates. -/
noncomputable def aff (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (s : Fin n → Bool) : ℝ :=
  α + ∑ i, β i * sgn (s i)

/-- Flip one coordinate. -/
def flipAt {n : ℕ} (j : Fin n) (s : Fin n → Bool) : Fin n → Bool := Function.update s j (!s j)

/-- Flip every coordinate. -/
def negAll {n : ℕ} (s : Fin n → Bool) : Fin n → Bool := fun i => !s i

theorem flipAt_involutive {n : ℕ} (j : Fin n) : Function.Involutive (flipAt (n := n) j) := by
  intro s
  funext i
  unfold flipAt
  by_cases h : i = j
  · subst h
    simp
  · rw [Function.update_of_ne h, Function.update_of_ne h]

theorem negAll_involutive {n : ℕ} : Function.Involutive (negAll (n := n)) := by
  intro s
  funext i
  simp [negAll]

theorem aff_flip (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (j : Fin n) (s : Fin n → Bool) :
    aff n α β (flipAt j s) - aff n α β s = -2 * β j * sgn (s j) := by
  unfold aff
  have e1 : ∑ i, β i * sgn (flipAt j s i)
      = β j * sgn (flipAt j s j) + ∑ i ∈ univ.erase j, β i * sgn (flipAt j s i) :=
    (Finset.add_sum_erase _ _ (mem_univ j)).symm
  have e2 : ∑ i, β i * sgn (s i) = β j * sgn (s j) + ∑ i ∈ univ.erase j, β i * sgn (s i) :=
    (Finset.add_sum_erase _ _ (mem_univ j)).symm
  have e3 : ∑ i ∈ univ.erase j, β i * sgn (flipAt j s i) = ∑ i ∈ univ.erase j, β i * sgn (s i) := by
    refine Finset.sum_congr rfl fun i hi => ?_
    have hij : i ≠ j := Finset.ne_of_mem_erase hi
    unfold flipAt
    rw [Function.update_of_ne hij]
  have e4 : flipAt j s j = !s j := by
    unfold flipAt
    simp
  rw [e1, e2, e3, e4, sgn_not]
  ring

theorem aff_negAll (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (s : Fin n → Bool) :
    aff n α β (negAll s) + aff n α β s = 2 * α := by
  unfold aff negAll
  have : ∑ i, β i * sgn (!s i) = -∑ i, β i * sgn (s i) := by
    rw [← Finset.sum_neg_distrib]
    exact Finset.sum_congr rfl fun i _ => by rw [sgn_not]; ring
  rw [this]
  ring

theorem tri_add (x y : ℝ) : |x + y| ≤ |x| + |y| :=
  abs_le.mpr ⟨by linarith [neg_abs_le x, neg_abs_le y], by linarith [le_abs_self x, le_abs_self y]⟩

theorem tri_sub (x y : ℝ) : |x - y| ≤ |x| + |y| :=
  abs_le.mpr ⟨by linarith [le_abs_self y, neg_abs_le x], by linarith [le_abs_self x, neg_abs_le y]⟩

theorem abs_aff_le (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (s : Fin n → Bool) :
    |aff n α β s| ≤ |α| + ∑ i, |β i| := by
  unfold aff
  have h1 := tri_add α (∑ i, β i * sgn (s i))
  have h2 := Finset.abs_sum_le_sum_abs (fun i => β i * sgn (s i)) univ
  have h3 : ∑ i, |β i * sgn (s i)| = ∑ i, |β i| :=
    Finset.sum_congr rfl fun i _ => by rw [abs_mul, abs_sgn, mul_one]
  linarith

/-- If an involution maps every point outside `G` into `G`, then `G` contains half of the points. -/
theorem card_le_two_mul_of_involution {S : Type*} [Fintype S] [DecidableEq S] (f : S → S)
    (hf : Function.Involutive f) (G : Finset S) (h : ∀ s, s ∈ G ∨ f s ∈ G) :
    Fintype.card S ≤ 2 * G.card := by
  have hsub : (univ : Finset S) ⊆ G ∪ G.image f := by
    intro s _
    rcases h s with hs | hs
    · exact Finset.mem_union_left _ hs
    · exact Finset.mem_union_right _ (Finset.mem_image.mpr ⟨f s, hs, hf s⟩)
  calc Fintype.card S = (univ : Finset S).card := Finset.card_univ.symm
    _ ≤ (G ∪ G.image f).card := Finset.card_le_card hsub
    _ ≤ G.card + (G.image f).card := Finset.card_union_le _ _
    _ ≤ G.card + G.card := Nat.add_le_add_left Finset.card_image_le _
    _ = 2 * G.card := by ring

open Classical in
/-- **Half of the cube sees the scale of an affine function.**  For every affine `h` on `{-1, 1}^n` and every
point `s₀` (in particular a maximiser of `|h|`), at least `2^{n-1}` points `s` have
`|h(s₀)| ≤ (n + 1) |h(s)|`. -/
theorem affine_half_large (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (s₀ : Fin n → Bool) :
    2 ^ n ≤ 2 * (univ.filter fun s : Fin n → Bool =>
      |aff n α β s₀| ≤ ((n : ℝ) + 1) * |aff n α β s|).card := by
  have hcard : Fintype.card (Fin n → Bool) = 2 ^ n := by simp
  have h0 := abs_aff_le n α β s₀
  have key : ∃ T : ℝ, |aff n α β s₀| ≤ ((n : ℝ) + 1) * T ∧
      ∃ f : (Fin n → Bool) → (Fin n → Bool), Function.Involutive f ∧
        ∀ s, T ≤ |aff n α β s| ∨ T ≤ |aff n α β (f s)| := by
    by_cases hα : ∀ i, |β i| ≤ |α|
    · refine ⟨|α|, ?_, negAll, negAll_involutive, ?_⟩
      · have hsum : ∑ i, |β i| ≤ ∑ _i : Fin n, |α| := Finset.sum_le_sum fun i _ => hα i
        rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hsum
        linarith
      · intro s
        by_contra hcon
        push Not at hcon
        have e := aff_negAll n α β s
        have t := tri_add (aff n α β (negAll s)) (aff n α β s)
        rw [e, abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 2)] at t
        linarith [hcon.1, hcon.2]
    · push Not at hα
      obtain ⟨i₀, hi₀⟩ := hα
      obtain ⟨j, -, hj⟩ := Finset.exists_max_image (univ : Finset (Fin n)) (fun i => |β i|)
        ⟨i₀, mem_univ i₀⟩
      have hαj : |α| ≤ |β j| := le_trans hi₀.le (hj i₀ (mem_univ _))
      refine ⟨|β j|, ?_, flipAt j, flipAt_involutive j, ?_⟩
      · have hsum : ∑ i, |β i| ≤ ∑ _i : Fin n, |β j| := Finset.sum_le_sum fun i _ => hj i (mem_univ _)
        rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hsum
        linarith
      · intro s
        by_contra hcon
        push Not at hcon
        have e := aff_flip n α β j s
        have t := tri_sub (aff n α β (flipAt j s)) (aff n α β s)
        rw [e, abs_two_mul_sgn] at t
        linarith [hcon.1, hcon.2]
  obtain ⟨T, hT, f, hf, hcov⟩ := key
  have hG := card_le_two_mul_of_involution f hf (univ.filter fun s => T ≤ |aff n α β s|)
    (fun s => by
      rcases hcov s with h | h
      · exact Or.inl (Finset.mem_filter.mpr ⟨mem_univ _, h⟩)
      · exact Or.inr (Finset.mem_filter.mpr ⟨mem_univ _, h⟩))
  rw [hcard] at hG
  refine hG.trans (Nat.mul_le_mul_left 2 (Finset.card_le_card ?_))
  intro s hs
  have hs' : T ≤ |aff n α β s| := (Finset.mem_filter.mp hs).2
  refine Finset.mem_filter.mpr ⟨mem_univ _, ?_⟩
  have hn : (0 : ℝ) ≤ (n : ℝ) + 1 := by positivity
  calc |aff n α β s₀| ≤ ((n : ℝ) + 1) * T := hT
    _ ≤ ((n : ℝ) + 1) * |aff n α β s| := mul_le_mul_of_nonneg_left hs' hn

end ScienceR12

#print axioms ScienceR12.detect_ge_at_floor
#print axioms ScienceR12.detect_ge_at_ceiling
#print axioms ScienceR12.detect_ge_weighted
#print axioms ScienceR12.weighted_opt
#print axioms ScienceR12.logRatio_bumpAlt_lt
#print axioms ScienceR12.logRatio_bumpAlt_gt
#print axioms ScienceR12.affine_half_large
