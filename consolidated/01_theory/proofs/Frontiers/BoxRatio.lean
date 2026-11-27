/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# A ratio of two macrostate weights in a box class (theory report §11.30, Corollary 11.114)

The observable of an experiment is a free-energy *difference* between two macrostates `A`, `B` of one system,
`-log (Z_A / Z_B)` with `Z_M = ∑_{x ∈ M} w(x) e^{-r(x)}`.  In a box class (`BoxClass.lean`) the lemmas for `log Z` hold
for arbitrary non-negative weights, hence for the weights restricted to a macrostate, and give for the ratio:

* `ratio_detect_ge` — every member of the box whose log-ratio differs from that of `r` by more than `η` differs from
  `r` on a set of probability at least `½ min (p_A(η), p_B(η))` under the mixture of the samplers of the two
  macrostates, `p_M` the detection bound of `detect_ge` for the weights restricted to `M` at the *same* level `η`
  (the worst case is a change of one macrostate alone: `ratio_core`);
* `ratio_spotCheck_correct` — so the spot check with that mixture certifies the log-ratio on every class inside the box;
* `logRatio_dipAlt_gt` — a set inside one macrostate, disjoint from the other, whose dip weight exceeds `(e^ε - 1)` times
  the weight of its macrostate changes the log-ratio by more than `ε` when lowered to the floor;
* `ratio_expected_queries_ge` — hence pairwise disjoint such sets, in either macrostate, force `(1 - 2δ)` evaluations
  each of every randomised algorithm that is correct for the log-ratio on the box.

So the cost of certifying a free-energy difference in a box class is, up to constants, the *larger* of the two
macrostates' own costs, each computed inside its macrostate, whatever the weights of the macrostates in the whole
system: the Boltzmann factor of the distance to the floor, `Z_M(lo)/Z_M(r) - 1`, plus a term from the ceiling,
`1 - Z_M(hi)/Z_M(r)`, both divided by the accuracy.  The statements of this file use the dips (the first term);
the bump alternatives and the lower bound with both kinds of sets are in `BoxAdditions.lean`.  (The first version
of this header named the first term alone and called the result "Corollary 11.113"; both were pointed out by the
Scientific Discovery Division's review SCI-REV-0013.)  `ratio_detect_ge` and `ratio_spotCheck_correct` do not need
the two macrostates to be disjoint; they need positive total dip and bump weights in each.
-/
import proofs.Frontiers.BoxClass

namespace MetricChain.BoxClass

open Finset

variable {X : Type*} [Fintype X]

open Classical in
/-- Weights restricted to a macrostate. -/
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

/-- The logarithm of the ratio of the weights of two macrostates. -/
noncomputable def logRatio (w : X → ℝ) (A B : Finset X) (r : X → ℝ) : ℝ :=
  Real.log (Zw (restr w A) r) - Real.log (Zw (restr w B) r)

/-- The sampler for a ratio: half of the samples from the sampler of each macrostate. -/
noncomputable def ratioSampler (w lo hi : X → ℝ) (A B : Finset X) (r : X → ℝ) (x : X) : ℝ :=
  1 / 2 * sampler (restr w A) lo hi r x + 1 / 2 * sampler (restr w B) lo hi r x

theorem ratioSampler_nonneg {w lo hi r : X → ℝ} (hw : ∀ x, 0 ≤ w x) (hr : Box lo hi r) (A B : Finset X) (x : X) :
    0 ≤ ratioSampler w lo hi A B r x := by
  unfold ratioSampler
  have h1 := sampler_nonneg (restr_nonneg hw A) hr x
  have h2 := sampler_nonneg (restr_nonneg hw B) hr x
  linarith

theorem ratioSampler_sum {w lo hi r : X → ℝ} {A B : Finset X}
    (hUA : 0 < ∑ y, dip (restr w A) lo r y) (hVA : 0 < ∑ y, bump (restr w A) hi r y)
    (hUB : 0 < ∑ y, dip (restr w B) lo r y) (hVB : 0 < ∑ y, bump (restr w B) hi r y) :
    ∑ x, ratioSampler w lo hi A B r x = 1 := by
  unfold ratioSampler
  rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, sampler_sum hUA hVA, sampler_sum hUB hVB]
  norm_num

/-- The detection bound of one macrostate at level `η` (not capped). -/
noncomputable def detectBound (w lo hi r : X → ℝ) (η : ℝ) : ℝ :=
  1 / 2 * min ((Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y) ((1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y)

/-- The arithmetic core of the detection bound for a ratio: if the weight of one macrostate can gain at most `dA` and
the weight of the other can lose at most `bB`, and the ratio nevertheless grows by more than the factor `E > 1`, then
`dA/U_A + bB/V_B` is at least the smaller of `(E - 1) Z_A/U_A` and `(1 - 1/E) Z_B/V_B`. -/
theorem ratio_core {E ZA ZB UA VB dA bB : ℝ} (hE : 1 < E) (hZA : 0 < ZA) (hZB : 0 < ZB) (hUA : 0 < UA)
    (hVB : 0 < VB) (hdA : 0 ≤ dA) (hbB : 0 ≤ bB) (hstar : (E - 1) * ZA * ZB < dA * ZB + E * ZA * bB) :
    min ((E - 1) * ZA / UA) ((1 - E⁻¹) * ZB / VB) ≤ dA / UA + bB / VB := by
  have hE0 : 0 < E := by linarith
  have hy : (1 - E⁻¹) * ZB / VB = (E - 1) * ZB / (E * VB) := by
    field_simp
  have hsum : dA / UA + bB / VB = (dA * VB + bB * UA) / (UA * VB) := by
    field_simp
  rcases le_total ((E - 1) * ZA / UA) ((1 - E⁻¹) * ZB / VB) with h | h
  · rw [min_eq_left h, hsum, div_le_div_iff₀ hUA (mul_pos hUA hVB)]
    -- from `x ≤ y`: `E ZA VB ≤ ZB UA`
    have h1 : E * ZA * VB ≤ ZB * UA := by
      rw [hy, div_le_div_iff₀ hUA (mul_pos hE0 hVB)] at h
      have h2 : (E - 1) * (E * ZA * VB) ≤ (E - 1) * (ZB * UA) := by nlinarith
      exact le_of_mul_le_mul_left h2 (by linarith)
    have h4 : E * ZA * VB * bB ≤ ZB * UA * bB := mul_le_mul_of_nonneg_right h1 hbB
    have h3 : ZB * ((E - 1) * ZA * VB) < ZB * (dA * VB + bB * UA) := by
      have h7 := mul_lt_mul_of_pos_right hstar hVB
      nlinarith
    have h5 := lt_of_mul_lt_mul_left h3 hZB.le
    have h6 := mul_lt_mul_of_pos_right h5 hUA
    nlinarith
  · rw [min_eq_right h, hsum, hy, div_le_div_iff₀ (mul_pos hE0 hVB) (mul_pos hUA hVB)]
    have h1 : ZB * UA ≤ E * ZA * VB := by
      rw [hy, div_le_div_iff₀ (mul_pos hE0 hVB) hUA] at h
      have h2 : (E - 1) * (ZB * UA) ≤ (E - 1) * (E * ZA * VB) := by nlinarith
      exact le_of_mul_le_mul_left h2 (by linarith)
    have h4 : ZB * UA * dA ≤ E * ZA * VB * dA := mul_le_mul_of_nonneg_right h1 hdA
    have h3 : ZA * ((E - 1) * ZB * UA) < ZA * (E * (dA * VB + bB * UA)) := by
      have h7 := mul_lt_mul_of_pos_right hstar hUA
      nlinarith
    have h5 := lt_of_mul_lt_mul_left h3 hZA.le
    have h6 := mul_lt_mul_of_pos_right h5 hVB
    nlinarith

open Classical in
/-- **Detection for a ratio.**  A member of the box whose log-ratio differs from that of `r` by more than `η > 0`
differs from `r` on a set of probability at least `½ min (p_A(η), p_B(η))` under the mixed sampler, `p_M` the
detection bound of the macrostate `M` at the same level `η`: the price of a ratio is one factor two. -/
theorem ratio_detect_ge {w lo hi r r' : X → ℝ} (hw : ∀ x, 0 ≤ w x) {A B : Finset X} {a b : X}
    (ha : a ∈ A) (hwa : 0 < w a) (hb : b ∈ B) (hwb : 0 < w b)
    (hr : Box lo hi r) (hr' : Box lo hi r')
    (hUA : 0 < ∑ y, dip (restr w A) lo r y) (hVA : 0 < ∑ y, bump (restr w A) hi r y)
    (hUB : 0 < ∑ y, dip (restr w B) lo r y) (hVB : 0 < ∑ y, bump (restr w B) hi r y) {η : ℝ} (hη : 0 < η)
    (hfar : η < |logRatio w A B r' - logRatio w A B r|) :
    1 / 2 * min (detectBound (restr w A) lo hi r η) (detectBound (restr w B) lo hi r η)
      ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), ratioSampler w lo hi A B r x := by
  set D := univ.filter (fun x => r' x ≠ r x) with hDdef
  have hwA := restr_nonneg hw A
  have hwB := restr_nonneg hw B
  have hZA : 0 < Zw (restr w A) r := Zw_pos hwA (restr_pos ha hwa)
  have hZA' : 0 < Zw (restr w A) r' := Zw_pos hwA (restr_pos ha hwa)
  have hZB : 0 < Zw (restr w B) r := Zw_pos hwB (restr_pos hb hwb)
  have hZB' : 0 < Zw (restr w B) r' := Zw_pos hwB (restr_pos hb hwb)
  have hE : 1 < Real.exp η := by
    have := Real.add_one_lt_exp (ne_of_gt hη)
    linarith
  -- the four partial sums over the set where the two remainders differ
  have hdA0 : 0 ≤ ∑ x ∈ D, dip (restr w A) lo r x := Finset.sum_nonneg fun y _ => dip_nonneg hwA hr y
  have hbA0 : 0 ≤ ∑ x ∈ D, bump (restr w A) hi r x := Finset.sum_nonneg fun y _ => bump_nonneg hwA hr y
  have hdB0 : 0 ≤ ∑ x ∈ D, dip (restr w B) lo r x := Finset.sum_nonneg fun y _ => dip_nonneg hwB hr y
  have hbB0 : 0 ≤ ∑ x ∈ D, bump (restr w B) hi r x := Finset.sum_nonneg fun y _ => bump_nonneg hwB hr y
  have hsum : ∑ x ∈ D, ratioSampler w lo hi A B r x
      = 1 / 4 * ((∑ x ∈ D, dip (restr w A) lo r x) / ∑ y, dip (restr w A) lo r y)
        + 1 / 4 * ((∑ x ∈ D, bump (restr w A) hi r x) / ∑ y, bump (restr w A) hi r y)
        + 1 / 4 * ((∑ x ∈ D, dip (restr w B) lo r x) / ∑ y, dip (restr w B) lo r y)
        + 1 / 4 * ((∑ x ∈ D, bump (restr w B) hi r x) / ∑ y, bump (restr w B) hi r y) := by
    unfold ratioSampler sampler
    simp only [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.sum_div]
    ring
  have q1 := div_nonneg hdA0 hUA.le
  have q2 := div_nonneg hbA0 hVA.le
  have q3 := div_nonneg hdB0 hUB.le
  have q4 := div_nonneg hbB0 hVB.le
  rw [hsum]
  have hexpneg : Real.exp (-η) = (Real.exp η)⁻¹ := Real.exp_neg η
  rcases lt_abs.mp hfar with h | h
  · -- the ratio went up: `Z_A` gained or `Z_B` lost
    have hprod : Real.exp η * Zw (restr w A) r * Zw (restr w B) r' < Zw (restr w A) r' * Zw (restr w B) r := by
      have h1 : η + (Real.log (Zw (restr w A) r) + Real.log (Zw (restr w B) r'))
          < Real.log (Zw (restr w A) r') + Real.log (Zw (restr w B) r) := by
        unfold logRatio at h; linarith
      have h2 := Real.exp_lt_exp.mpr h1
      rw [Real.exp_add, Real.exp_add, Real.exp_add, Real.exp_log hZA, Real.exp_log hZB', Real.exp_log hZA',
        Real.exp_log hZB] at h2
      linarith
    have hup := Zw_sub_le_dip (r := r) hwA hr'
    have hdown := Zw_sub_le_bump (r := r) hwB hr'
    have hstar : (Real.exp η - 1) * Zw (restr w A) r * Zw (restr w B) r
        < (∑ x ∈ D, dip (restr w A) lo r x) * Zw (restr w B) r
          + Real.exp η * Zw (restr w A) r * ∑ x ∈ D, bump (restr w B) hi r x := by
      have e1 : Zw (restr w A) r' * Zw (restr w B) r
          ≤ (Zw (restr w A) r + ∑ x ∈ D, dip (restr w A) lo r x) * Zw (restr w B) r :=
        mul_le_mul_of_nonneg_right (by linarith) hZB.le
      have e2 : Real.exp η * Zw (restr w A) r * (Zw (restr w B) r - ∑ x ∈ D, bump (restr w B) hi r x)
          ≤ Real.exp η * Zw (restr w A) r * Zw (restr w B) r' :=
        mul_le_mul_of_nonneg_left (by linarith) (mul_pos (Real.exp_pos η) hZA).le
      nlinarith
    have hcore := ratio_core hE hZA hZB hUA hVB hdA0 hbB0 hstar
    have hm : min (detectBound (restr w A) lo hi r η) (detectBound (restr w B) lo hi r η)
        ≤ 1 / 2 * min ((Real.exp η - 1) * Zw (restr w A) r / ∑ y, dip (restr w A) lo r y)
          ((1 - (Real.exp η)⁻¹) * Zw (restr w B) r / ∑ y, bump (restr w B) hi r y) := by
      unfold detectBound
      rw [hexpneg]
      rw [← mul_min_of_nonneg _ _ (by norm_num : (0 : ℝ) ≤ 1 / 2)]
      refine mul_le_mul_of_nonneg_left ?_ (by norm_num)
      exact le_min ((min_le_left _ _).trans (min_le_left _ _)) ((min_le_right _ _).trans (min_le_right _ _))
    linarith
  · -- the ratio went down: `Z_B` gained or `Z_A` lost
    have hprod : Real.exp η * Zw (restr w B) r * Zw (restr w A) r' < Zw (restr w B) r' * Zw (restr w A) r := by
      have h1 : η + (Real.log (Zw (restr w B) r) + Real.log (Zw (restr w A) r'))
          < Real.log (Zw (restr w B) r') + Real.log (Zw (restr w A) r) := by
        unfold logRatio at h; linarith
      have h2 := Real.exp_lt_exp.mpr h1
      rw [Real.exp_add, Real.exp_add, Real.exp_add, Real.exp_log hZB, Real.exp_log hZA', Real.exp_log hZB',
        Real.exp_log hZA] at h2
      linarith
    have hup := Zw_sub_le_dip (r := r) hwB hr'
    have hdown := Zw_sub_le_bump (r := r) hwA hr'
    have hstar : (Real.exp η - 1) * Zw (restr w B) r * Zw (restr w A) r
        < (∑ x ∈ D, dip (restr w B) lo r x) * Zw (restr w A) r
          + Real.exp η * Zw (restr w B) r * ∑ x ∈ D, bump (restr w A) hi r x := by
      have e1 : Zw (restr w B) r' * Zw (restr w A) r
          ≤ (Zw (restr w B) r + ∑ x ∈ D, dip (restr w B) lo r x) * Zw (restr w A) r :=
        mul_le_mul_of_nonneg_right (by linarith) hZA.le
      have e2 : Real.exp η * Zw (restr w B) r * (Zw (restr w A) r - ∑ x ∈ D, bump (restr w A) hi r x)
          ≤ Real.exp η * Zw (restr w B) r * Zw (restr w A) r' :=
        mul_le_mul_of_nonneg_left (by linarith) (mul_pos (Real.exp_pos η) hZB).le
      nlinarith
    have hcore := ratio_core hE hZB hZA hUB hVA hdB0 hbA0 hstar
    have hm : min (detectBound (restr w A) lo hi r η) (detectBound (restr w B) lo hi r η)
        ≤ 1 / 2 * min ((Real.exp η - 1) * Zw (restr w B) r / ∑ y, dip (restr w B) lo r y)
          ((1 - (Real.exp η)⁻¹) * Zw (restr w A) r / ∑ y, bump (restr w A) hi r y) := by
      unfold detectBound
      rw [hexpneg]
      rw [← mul_min_of_nonneg _ _ (by norm_num : (0 : ℝ) ≤ 1 / 2)]
      refine mul_le_mul_of_nonneg_left ?_ (by norm_num)
      exact le_min ((min_le_right _ _).trans (min_le_left _ _)) ((min_le_left _ _).trans (min_le_right _ _))
    linarith

/-- The detection probability of the spot check for a ratio at level `η`, capped at one. -/
noncomputable def ratioDetectProb (w lo hi : X → ℝ) (A B : Finset X) (r : X → ℝ) (η : ℝ) : ℝ :=
  min 1 (1 / 2 * min (detectBound (restr w A) lo hi r η) (detectBound (restr w B) lo hi r η))

open Classical in
/-- **Sampling certificate for a ratio of macrostate weights (upper bound).**  For any class `G` inside the box and a
hint `r₀` in the box: if `(1 - p)^N ≤ δ` with `p = ratioDetectProb … (ε/2)`, the spot check of the hint with `N`
independent samples of the mixed sampler returns the log-ratio within `ε/2` with probability at least `1 - δ` on
every member of `G`. -/
theorem ratio_spotCheck_correct {G : (X → ℝ) → Prop} {w lo hi r₀ : X → ℝ} (hw : ∀ x, 0 ≤ w x) {A B : Finset X}
    {a b : X} (ha : a ∈ A) (hwa : 0 < w a) (hb : b ∈ B) (hwb : 0 < w b)
    (hG : ∀ r, G r → Box lo hi r) (hr₀ : Box lo hi r₀)
    (hUA : 0 < ∑ y, dip (restr w A) lo r₀ y) (hVA : 0 < ∑ y, bump (restr w A) hi r₀ y)
    (hUB : 0 < ∑ y, dip (restr w B) lo r₀ y) (hVB : 0 < ∑ y, bump (restr w B) hi r₀ y)
    {ε δ : ℝ} (hε : 0 < ε) (N : ℕ)
    (hN : (1 - ratioDetectProb w lo hi A B r₀ (ε / 2)) ^ N ≤ δ) (r : X → ℝ) (hr : G r) :
    1 - δ ≤ ∑ s ∈ univ.filter (fun s : Fin N → X =>
      |(spotCheck (logRatio w A B) r₀ s).output r - logRatio w A B r| ≤ ε / 2),
      ∏ k, ratioSampler w lo hi A B r₀ (s k) := by
  refine spotCheck_correct (G := G) (Φ := logRatio w A B) r₀ N (ratioSampler w lo hi A B r₀)
    (ratioSampler_nonneg hw hr₀ A B) (ratioSampler_sum hUA hVA hUB hVB) hε.le (min_le_left _ _)
    (fun r' hr' hfar => ?_) hN r hr
  exact (min_le_right _ _).trans
    (ratio_detect_ge hw ha hwa hb hwb hr₀ (hG r' hr') hUA hVA hUB hVB (by linarith) hfar)

/-! ### The lower bound: disjoint dips inside either macrostate -/

/-- Lowering the remainder on a set that does not meet a macrostate does not change the weight of that macrostate. -/
theorem Zw_restr_dipAlt_of_disjoint (w lo r : X → ℝ) {M D : Finset X} (hD : ∀ x ∈ D, x ∉ M) :
    Zw (restr w M) (dipAlt lo r D) = Zw (restr w M) r := by
  rw [Zw_dipAlt]
  have : ∑ x ∈ D, dip (restr w M) lo r x = 0 := by
    refine Finset.sum_eq_zero fun x hx => ?_
    unfold dip
    rw [restr_eq_zero (hD x hx), zero_mul]
  rw [this, add_zero]

/-- A set that avoids `B` and whose dip weight inside `A` exceeds `(e^ε - 1) Z_A` raises the log-ratio by more than `ε`
when the remainder is lowered to the floor on it. -/
theorem logRatio_dipAlt_gt {w lo r : X → ℝ} (hw : ∀ x, 0 ≤ w x) {A B : Finset X} {a : X} (ha : a ∈ A)
    (hwa : 0 < w a) {D : Finset X} (hDB : ∀ x ∈ D, x ∉ B) {ε : ℝ}
    (hD : (Real.exp ε - 1) * Zw (restr w A) r < ∑ x ∈ D, dip (restr w A) lo r x) :
    ε < logRatio w A B (dipAlt lo r D) - logRatio w A B r := by
  have hZ : 0 < Zw (restr w A) r := Zw_pos (restr_nonneg hw A) (restr_pos ha hwa)
  have hgt : Real.exp ε * Zw (restr w A) r < Zw (restr w A) (dipAlt lo r D) := by rw [Zw_dipAlt]; nlinarith
  have hlog : ε + Real.log (Zw (restr w A) r) < Real.log (Zw (restr w A) (dipAlt lo r D)) := by
    have h := Real.log_lt_log (mul_pos (Real.exp_pos ε) hZ) hgt
    rwa [Real.log_mul (Real.exp_pos ε).ne' hZ.ne', Real.log_exp] at h
  unfold logRatio
  rw [Zw_restr_dipAlt_of_disjoint w lo r hDB]
  linarith

/-- The same in the other macrostate: the log-ratio falls by more than `ε`. -/
theorem logRatio_dipAlt_lt {w lo r : X → ℝ} (hw : ∀ x, 0 ≤ w x) {A B : Finset X} {b : X} (hb : b ∈ B)
    (hwb : 0 < w b) {D : Finset X} (hDA : ∀ x ∈ D, x ∉ A) {ε : ℝ}
    (hD : (Real.exp ε - 1) * Zw (restr w B) r < ∑ x ∈ D, dip (restr w B) lo r x) :
    ε < logRatio w A B r - logRatio w A B (dipAlt lo r D) := by
  have hZ : 0 < Zw (restr w B) r := Zw_pos (restr_nonneg hw B) (restr_pos hb hwb)
  have hgt : Real.exp ε * Zw (restr w B) r < Zw (restr w B) (dipAlt lo r D) := by rw [Zw_dipAlt]; nlinarith
  have hlog : ε + Real.log (Zw (restr w B) r) < Real.log (Zw (restr w B) (dipAlt lo r D)) := by
    have h := Real.log_lt_log (mul_pos (Real.exp_pos ε) hZ) hgt
    rwa [Real.log_mul (Real.exp_pos ε).ne' hZ.ne', Real.log_exp] at h
  unfold logRatio
  rw [Zw_restr_dipAlt_of_disjoint w lo r hDA]
  linarith

open Classical in
/-- **Lower bound for every randomised algorithm that certifies a ratio on a box class.**  Let `D j` be pairwise
disjoint sets, each either avoiding `B` with dip weight inside `A` above `(e^ε - 1) Z_A(r)`, or avoiding `A` with dip
weight inside `B` above `(e^ε - 1) Z_B(r)`.  Every mixture of algorithms that returns the log-ratio within `ε/2` with
probability at least `1 - δ` on every member of the box makes, on `r`, at least `(1 - 2δ)` evaluations per set in
expectation. -/
theorem ratio_expected_queries_ge {Ω : Type*} [Fintype Ω] {ι : Type*} [Fintype ι] {w lo hi : X → ℝ}
    (hw : ∀ x, 0 ≤ w x) {A B : Finset X} {a b : X} (ha : a ∈ A) (hwa : 0 < w a) (hb : b ∈ B) (hwb : 0 < w b)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ r, Box lo hi r →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output r - logRatio w A B r| ≤ ε / 2), P ω)
    {r : X → ℝ} (hr : Box lo hi r) (D : ι → Finset X)
    (hdisj : ∀ i j, i ≠ j → Disjoint (D i) (D j))
    (hD : ∀ j, ((∀ x ∈ D j, x ∉ B) ∧ (Real.exp ε - 1) * Zw (restr w A) r < ∑ x ∈ D j, dip (restr w A) lo r x) ∨
      ((∀ x ∈ D j, x ∉ A) ∧ (Real.exp ε - 1) * Zw (restr w B) r < ∑ x ∈ D j, dip (restr w B) lo r x)) :
    (1 - 2 * δ) * (Fintype.card ι : ℝ) ≤ ∑ ω, P ω * ((alg ω).queries r).card := by
  have hsens : ∀ j, ε < |logRatio w A B (dipAlt lo r (D j)) - logRatio w A B r| := by
    intro j
    rcases hD j with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact lt_of_lt_of_le (logRatio_dipAlt_gt hw ha hwa h1 h2) (le_abs_self _)
    · have h3 := logRatio_dipAlt_lt hw (A := A) hb hwb h1 h2
      have h4 := neg_le_abs (logRatio w A B (dipAlt lo r (D j)) - logRatio w A B r)
      linarith
  have key := expected_queries_ge_packing (G := Box lo hi) (Φ := logRatio w A B) alg P hP hP1
    hcorr hr (fun j => dipAlt lo r (D j)) (fun j => dipAlt_mem hr (D j))
    hsens (fun _ => (1 : ℝ)) (fun _ => zero_le_one) (B := 1) ?_
  · simpa using key
  · intro x
    have hsub : (univ.filter (fun j => dipAlt lo r (D j) x ≠ r x)).card ≤ 1 := by
      rw [Finset.card_le_one]
      intro i hi j hj
      by_contra hij
      have hai : x ∈ D i := dipAlt_ne (Finset.mem_filter.mp hi).2
      have haj : x ∈ D j := dipAlt_ne (Finset.mem_filter.mp hj).2
      exact (Finset.disjoint_left.mp (hdisj i j hij)) hai haj
    have : ∑ j ∈ univ.filter (fun j => dipAlt lo r (D j) x ≠ r x), (1 : ℝ)
        = ((univ.filter (fun j => dipAlt lo r (D j) x ≠ r x)).card : ℝ) := by simp
    rw [this]
    exact_mod_cast hsub

/-! ### Non-vacuity: two macrostates of two points each -/

/-- On four points with unit weights, the constant box `[-1, 1]` at the centre and macrostates `{0, 1}`, `{2, 3}`:
each macrostate has weight `2`, total dip weight `2(e - 1)` and total bump weight `2(1 - e^{-1})`, so its detection
bound at level `η` is `½ min ((e^η - 1)/(e - 1), (1 - e^{-η})/(1 - e^{-1}))`. -/
theorem ratio_witness :
    Zw (restr (fun _ : Fin 4 => (1 : ℝ)) {0, 1}) (fun _ => 0) = 2 ∧
    ∑ x, dip (restr (fun _ : Fin 4 => (1 : ℝ)) {0, 1}) (fun _ => -1) (fun _ => 0) x = 2 * (Real.exp 1 - 1) ∧
    logRatio (fun _ : Fin 4 => (1 : ℝ)) {0, 1} {2, 3} (fun _ => 0) = 0 := by
  have a0 : (0 : Fin 4) ∈ ({0, 1} : Finset (Fin 4)) := by decide
  have a1 : (1 : Fin 4) ∈ ({0, 1} : Finset (Fin 4)) := by decide
  have a2 : (2 : Fin 4) ∉ ({0, 1} : Finset (Fin 4)) := by decide
  have a3 : (3 : Fin 4) ∉ ({0, 1} : Finset (Fin 4)) := by decide
  have b0 : (0 : Fin 4) ∉ ({2, 3} : Finset (Fin 4)) := by decide
  have b1 : (1 : Fin 4) ∉ ({2, 3} : Finset (Fin 4)) := by decide
  have b2 : (2 : Fin 4) ∈ ({2, 3} : Finset (Fin 4)) := by decide
  have b3 : (3 : Fin 4) ∈ ({2, 3} : Finset (Fin 4)) := by decide
  have hZA : Zw (restr (fun _ : Fin 4 => (1 : ℝ)) {0, 1}) (fun _ => 0) = 2 := by
    simp only [Zw, restr, Fin.sum_univ_four, if_pos a0, if_pos a1, if_neg a2, if_neg a3, neg_zero, Real.exp_zero]
    norm_num
  have hZB : Zw (restr (fun _ : Fin 4 => (1 : ℝ)) {2, 3}) (fun _ => 0) = 2 := by
    simp only [Zw, restr, Fin.sum_univ_four, if_neg b0, if_neg b1, if_pos b2, if_pos b3, neg_zero, Real.exp_zero]
    norm_num
  refine ⟨hZA, ?_, ?_⟩
  · simp only [dip, restr, Fin.sum_univ_four, if_pos a0, if_pos a1, if_neg a2, if_neg a3, neg_zero, neg_neg,
      Real.exp_zero]
    ring
  · unfold logRatio
    rw [hZA, hZB, sub_self]

end MetricChain.BoxClass
