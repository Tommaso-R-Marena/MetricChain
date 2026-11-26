import Mathlib
import proofs.Frontiers.BoxRatio

/-!
# Box classes: detection at the floor and at the ceiling, weighted samplers, and bumps for ratios

Additions to `BoxClass.lean` and `BoxRatio.lean` (theory report §11.30, Theorem 11.110(c) and Corollary 11.114).

**Provenance.**  Everything in this file up to and including `logRatio_bumpAlt_gt` was written and machine-checked by
the Scientific Discovery Division in its independent review of the seventeenth checkpoint (workstream R12, message
SCI-REV-0013, findings m1, m3, m5; its file `experiments/science/ws_R12/lean/R12Additions.lean` on the branch
`research/scientific-translation`).  That file restated our definitions in a namespace of its own, because our
modules are not modules of its tree; here the statements and proofs are taken over unchanged and refer to the
definitions of `BoxClass.lean` and `BoxRatio.lean` themselves.  The last theorem,
`ratio_expected_queries_ge_mixed`, is ours and follows `box_expected_queries_ge_mixed`.

* `detect_ge_at_floor`, `detect_ge_at_ceiling` — the detection lemma in the two cases that `detect_ge` excludes by its
  hypotheses `0 < U`, `0 < V`: at the floor of the box (total dip weight zero) every far member differs from `r` on a
  set of probability at least `(1 - e^{-η}) Z / V` under the bump sampler, without the factor one half; at the
  ceiling the same with dips.
* `samplerW`, `detect_ge_weighted`, `weighted_opt` — the sampler `λ dip/U + (1 - λ) bump/V` detects with probability at
  least `min (λ (e^η - 1) Z / U, (1 - λ)(1 - e^{-η}) Z / V)`; with `λ = A/(A + B)`, `A = U/((e^η - 1) Z)`,
  `B = V/((1 - e^{-η}) Z)`, this is `1/(A + B)`: the sample size is the sum of the two terms, not twice the larger.
* `logRatio_bumpAlt_lt`, `logRatio_bumpAlt_gt` — raising the remainder to the ceiling on a set that avoids one
  macrostate and whose bump weight inside the other exceeds `(1 - e^{-ε})` times that macrostate's weight changes
  the log-ratio by more than `ε`.
* `ratio_expected_queries_ge_mixed` — hence the lower bound for every randomised algorithm that certifies a ratio
  counts sets that are heavy by their dips **or** by their bumps, in either macrostate: near the floor of a
  macrostate the bumps carry the bound (`ratio_expected_queries_ge` is the case of dips alone).
-/

namespace MetricChain.BoxClass

open Finset

variable {X : Type*} [Fintype X]

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

/-! ### The lower bound for a ratio with dips and bumps (ours) -/

open Classical in
/-- **Lower bound for every randomised algorithm that certifies a ratio on a box class, floor and ceiling.**  Let
`D j` be pairwise disjoint sets, each of one of four kinds: avoiding `B` with dip weight inside `A` above
`(e^ε - 1) Z_A(r)`; avoiding `A` with dip weight inside `B` above `(e^ε - 1) Z_B(r)`; avoiding `B` with bump weight
inside `A` above `(1 - e^{-ε}) Z_A(r)`; avoiding `A` with bump weight inside `B` above `(1 - e^{-ε}) Z_B(r)`.  Every
mixture of algorithms that returns the log-ratio within `ε/2` with probability at least `1 - δ` on every member of
the box makes, on `r`, at least `(1 - 2δ)` evaluations per set in expectation. -/
theorem ratio_expected_queries_ge_mixed {Ω : Type*} [Fintype Ω] {ι : Type*} [Fintype ι] {w lo hi : X → ℝ}
    (hw : ∀ x, 0 ≤ w x) {A B : Finset X} {a b : X} (ha : a ∈ A) (hwa : 0 < w a) (hb : b ∈ B) (hwb : 0 < w b)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ r, Box lo hi r →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output r - logRatio w A B r| ≤ ε / 2), P ω)
    {r : X → ℝ} (hr : Box lo hi r) (D : ι → Finset X)
    (hdisj : ∀ i j, i ≠ j → Disjoint (D i) (D j))
    (hD : ∀ j,
      (((∀ x ∈ D j, x ∉ B) ∧ (Real.exp ε - 1) * Zw (restr w A) r < ∑ x ∈ D j, dip (restr w A) lo r x) ∨
        ((∀ x ∈ D j, x ∉ A) ∧ (Real.exp ε - 1) * Zw (restr w B) r < ∑ x ∈ D j, dip (restr w B) lo r x)) ∨
      (((∀ x ∈ D j, x ∉ B) ∧
          (1 - Real.exp (-ε)) * Zw (restr w A) r < ∑ x ∈ D j, bump (restr w A) hi r x) ∨
        ((∀ x ∈ D j, x ∉ A) ∧
          (1 - Real.exp (-ε)) * Zw (restr w B) r < ∑ x ∈ D j, bump (restr w B) hi r x))) :
    (1 - 2 * δ) * (Fintype.card ι : ℝ) ≤ ∑ ω, P ω * ((alg ω).queries r).card := by
  -- the alternative of the set `j`: the floor if its dips are heavy in a macrostate, the ceiling otherwise
  have hex : ∀ j, ∃ f : X → ℝ, Box lo hi f ∧ ε < |logRatio w A B f - logRatio w A B r| ∧
      ∀ x, f x ≠ r x → x ∈ D j := by
    intro j
    rcases hD j with (⟨h1, h2⟩ | ⟨h1, h2⟩) | (⟨h1, h2⟩ | ⟨h1, h2⟩)
    · exact ⟨dipAlt lo r (D j), dipAlt_mem hr (D j),
        lt_of_lt_of_le (logRatio_dipAlt_gt hw ha hwa h1 h2) (le_abs_self _), fun _ => dipAlt_ne⟩
    · refine ⟨dipAlt lo r (D j), dipAlt_mem hr (D j), ?_, fun _ => dipAlt_ne⟩
      have h3 := logRatio_dipAlt_lt hw (A := A) hb hwb h1 h2
      have h4 := neg_le_abs (logRatio w A B (dipAlt lo r (D j)) - logRatio w A B r)
      linarith
    · refine ⟨bumpAlt hi r (D j), bumpAlt_mem hr (D j), ?_, fun _ => bumpAlt_ne⟩
      have h3 := logRatio_bumpAlt_lt hw (B := B) ha hwa h1 h2
      have h4 := neg_le_abs (logRatio w A B (bumpAlt hi r (D j)) - logRatio w A B r)
      linarith
    · exact ⟨bumpAlt hi r (D j), bumpAlt_mem hr (D j),
        lt_of_lt_of_le (logRatio_bumpAlt_gt hw (A := A) hb hwb h1 h2) (le_abs_self _), fun _ => bumpAlt_ne⟩
  choose alt halt_mem halt_sens halt_ne using hex
  have key := expected_queries_ge_packing (G := Box lo hi) (Φ := logRatio w A B) alg P hP hP1
    hcorr hr alt halt_mem halt_sens (fun _ => (1 : ℝ)) (fun _ => zero_le_one) (B := 1) ?_
  · simpa using key
  · intro x
    have hsub : (univ.filter (fun j => alt j x ≠ r x)).card ≤ 1 := by
      rw [Finset.card_le_one]
      intro i hi j hj
      by_contra hij
      have hai : x ∈ D i := halt_ne i x (Finset.mem_filter.mp hi).2
      have haj : x ∈ D j := halt_ne j x (Finset.mem_filter.mp hj).2
      exact (Finset.disjoint_left.mp (hdisj i j hij)) hai haj
    have : ∑ j ∈ univ.filter (fun j => alt j x ≠ r x), (1 : ℝ)
        = ((univ.filter (fun j => alt j x ≠ r x)).card : ℝ) := by simp
    rw [this]
    exact_mod_cast hsub

end MetricChain.BoxClass
