/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# Sup-norm (box) classes around a known function (theory report §11.30)

The energy is `f̂ + r` with `f̂` known and tractable — weights `w = e^{-f̂}` — and a remainder `r` of which only pointwise
bounds `lo ≤ r ≤ hi` are known (a *box class*; `lo = -ρ₋`, `hi = ρ₊` constant is a one-sided sup-norm ball).  The file
contains what makes `log Z` certifiable in such a class by sampling from the known part, and why nothing cheaper works:

* `Zw_sub_le_dip`, `Zw_sub_le_bump` — a member of the box that differs from `r` only on `D` raises the partition sum by
  at most the *dip weight* of `D`, `∑_D w (e^{-lo} - e^{-r})`, and lowers it by at most the *bump weight*
  `∑_D w (e^{-r} - e^{-hi})`;
* `detect_ge` — hence every member whose `log Z` differs from that of `r` by more than `η` differs from `r` on a set of
  probability at least `p = ½ min ((e^η - 1) Z / U, (1 - e^{-η}) Z / V)` under the sampler `q = ½ dip/U + ½ bump/V`;
* `box_spotCheck_correct` — so the spot check of a hint with `N` samples of `q`, `(1 - p)^N ≤ δ`, is correct on **every
  class contained in the box** (in particular on the intersection of the box with a first-order class);
* `dipAlt_mem`, `logZ_dipAlt_gt` — the alternative "lowered to the floor on `D`" is in the box and changes `log Z` by
  more than `ε` as soon as the dip weight of `D` exceeds `(e^ε - 1) Z`;
* `box_expected_queries_ge` — therefore every randomised algorithm that is correct on the box makes, on `r`, at least
  `(1 - 2δ) k` evaluations in expectation whenever there are `k` pairwise disjoint sets with that much dip weight;
* `jensen_bracket` — `-E_π r ≤ log Z - log Z₀ = log E_π e^{-r}`: the lower end of the bracket is a mean.

For a constant box at the centre (`r = 0`, the known function is right) the two bounds read
`(1 - 2δ) ⌊(e^{ρ₋} - 1)/(2 (e^ε - 1))⌋ ≤ cost ≤ ⌈2 log (1/δ) · max ((e^{ρ₋} - 1)/(e^{ε/2} - 1), 1/(1 - e^{-ε/2}))⌉`:
the number of evaluations is governed by how far *below* the known function the truth may lie, in units of `k_B T`, and
by nothing else — not by the size of the system.
-/
import Mathlib
import proofs.Frontiers.QueryLowerBound

namespace MetricChain.BoxClass

open Finset

variable {X : Type*} [Fintype X]

/-- The box class: pointwise bounds on the remainder. -/
def Box (lo hi : X → ℝ) (r : X → ℝ) : Prop := ∀ x, lo x ≤ r x ∧ r x ≤ hi x

/-- The partition sum with weights `w` (the Gibbs weights of the known function) and remainder `r`. -/
noncomputable def Zw (w r : X → ℝ) : ℝ := ∑ x, w x * Real.exp (-r x)

/-- The dip weight of a point: how much the partition sum can gain there. -/
noncomputable def dip (w lo r : X → ℝ) (x : X) : ℝ := w x * (Real.exp (-lo x) - Real.exp (-r x))

/-- The bump weight of a point: how much the partition sum can lose there. -/
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
/-- A member of the box raises the partition sum by at most the dip weight of the set where it differs. -/
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
/-- A member of the box lowers the partition sum by at most the bump weight of the set where it differs. -/
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

/-- The total dip weight is the gain of the floor: `∑ dip = Z(lo) - Z(r)`. -/
theorem sum_dip_eq (w lo r : X → ℝ) : ∑ x, dip w lo r x = Zw w lo - Zw w r := by
  unfold dip Zw
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun x _ => by ring

/-- The total bump weight is the loss at the ceiling: `∑ bump = Z(r) - Z(hi)`. -/
theorem sum_bump_eq (w hi r : X → ℝ) : ∑ x, bump w hi r x = Zw w r - Zw w hi := by
  unfold bump Zw
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun x _ => by ring

/-- The sampler of the spot check: half of the samples where the partition sum could gain, half where it could lose. -/
noncomputable def sampler (w lo hi r : X → ℝ) (x : X) : ℝ :=
  1 / 2 * (dip w lo r x / ∑ y, dip w lo r y) + 1 / 2 * (bump w hi r x / ∑ y, bump w hi r y)

theorem sampler_nonneg {w lo hi r : X → ℝ} (hw : ∀ x, 0 ≤ w x) (hr : Box lo hi r) (x : X) :
    0 ≤ sampler w lo hi r x := by
  unfold sampler
  have h1 : 0 ≤ dip w lo r x / ∑ y, dip w lo r y :=
    div_nonneg (dip_nonneg hw hr x) (Finset.sum_nonneg fun y _ => dip_nonneg hw hr y)
  have h2 : 0 ≤ bump w hi r x / ∑ y, bump w hi r y :=
    div_nonneg (bump_nonneg hw hr x) (Finset.sum_nonneg fun y _ => bump_nonneg hw hr y)
  linarith

theorem sampler_sum {w lo hi r : X → ℝ} (hU : 0 < ∑ y, dip w lo r y) (hV : 0 < ∑ y, bump w hi r y) :
    ∑ x, sampler w lo hi r x = 1 := by
  unfold sampler
  rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.sum_div, ← Finset.sum_div,
    div_self hU.ne', div_self hV.ne']
  norm_num

open Classical in
/-- **Detection.**  Every member of the box whose `log Z` differs from that of `r` by more than `η` differs from `r`
on a set of sampler-probability at least `½ min ((e^η - 1) Z / U, (1 - e^{-η}) Z / V)`. -/
theorem detect_ge {w lo hi r r' : X → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀)
    (hr : Box lo hi r) (hr' : Box lo hi r')
    (hU : 0 < ∑ y, dip w lo r y) (hV : 0 < ∑ y, bump w hi r y) {η : ℝ}
    (hfar : η < |Real.log (Zw w r') - Real.log (Zw w r)|) :
    1 / 2 * min ((Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y)
        ((1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y)
      ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), sampler w lo hi r x := by
  have hZ : 0 < Zw w r := Zw_pos hw hx₀
  have hZ' : 0 < Zw w r' := Zw_pos hw hx₀
  have hsum : ∑ x ∈ univ.filter (fun x => r' x ≠ r x), sampler w lo hi r x
      = 1 / 2 * ((∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x) / ∑ y, dip w lo r y)
        + 1 / 2 * ((∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x) / ∑ y, bump w hi r y) := by
    unfold sampler
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.sum_div, ← Finset.sum_div]
  have hd0 : 0 ≤ (∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x) / ∑ y, dip w lo r y :=
    div_nonneg (Finset.sum_nonneg fun y _ => dip_nonneg hw hr y) hU.le
  have hb0 : 0 ≤ (∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x) / ∑ y, bump w hi r y :=
    div_nonneg (Finset.sum_nonneg fun y _ => bump_nonneg hw hr y) hV.le
  rw [hsum]
  rcases lt_abs.mp hfar with h | h
  · -- the partition sum went up
    have h1 : Real.log (Zw w r) + η < Real.log (Zw w r') := by linarith
    have h2 : Zw w r * Real.exp η < Zw w r' := by
      have := Real.exp_lt_exp.mpr h1
      rwa [Real.exp_add, Real.exp_log hZ, Real.exp_log hZ'] at this
    have h3 : (Real.exp η - 1) * Zw w r ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x := by
      have := Zw_sub_le_dip (r := r) hw hr'
      nlinarith
    have h4 : (Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y
        ≤ (∑ x ∈ univ.filter (fun x => r' x ≠ r x), dip w lo r x) / ∑ y, dip w lo r y :=
      div_le_div_of_nonneg_right h3 hU.le
    have h5 := min_le_left ((Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y)
      ((1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y)
    linarith
  · -- the partition sum went down
    have h1 : Real.log (Zw w r') + η < Real.log (Zw w r) := by linarith
    have h2 : Zw w r' < Zw w r * Real.exp (-η) := by
      have h1' : Real.log (Zw w r') < Real.log (Zw w r) + -η := by linarith
      have := Real.exp_lt_exp.mpr h1'
      rwa [Real.exp_add, Real.exp_log hZ, Real.exp_log hZ'] at this
    have h3 : (1 - Real.exp (-η)) * Zw w r ≤ ∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x := by
      have := Zw_sub_le_bump (r := r) hw hr'
      nlinarith
    have h4 : (1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y
        ≤ (∑ x ∈ univ.filter (fun x => r' x ≠ r x), bump w hi r x) / ∑ y, bump w hi r y :=
      div_le_div_of_nonneg_right h3 hV.le
    have h5 := min_le_right ((Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y)
      ((1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y)
    linarith

/-- The detection probability of the spot check at level `η`, capped at one. -/
noncomputable def detectProb (w lo hi r : X → ℝ) (η : ℝ) : ℝ :=
  min 1 (1 / 2 * min ((Real.exp η - 1) * Zw w r / ∑ y, dip w lo r y)
    ((1 - Real.exp (-η)) * Zw w r / ∑ y, bump w hi r y))

open Classical in
/-- **Sampling certificate for a box class (upper bound).**  Let `G` be any class of remainders inside the box, `r₀ ∈`
box the hint, and `p = min (1, ½ min ((e^{ε/2} - 1) Z / U, (1 - e^{-ε/2}) Z / V))` with `U`, `V` the total dip and bump
weights at `r₀`.  If `(1 - p)^N ≤ δ`, the spot check of the hint with `N` independent samples of `sampler` returns
`log Z` within `ε/2` with probability at least `1 - δ` on every member of `G`; on the hint it makes at most `N`
evaluations (`MetricChain.spotCheck_card_le`). -/
theorem box_spotCheck_correct {G : (X → ℝ) → Prop} {w lo hi r₀ : X → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : X}
    (hx₀ : 0 < w x₀) (hG : ∀ r, G r → Box lo hi r) (hr₀ : Box lo hi r₀)
    (hU : 0 < ∑ y, dip w lo r₀ y) (hV : 0 < ∑ y, bump w hi r₀ y) {ε δ : ℝ} (hε : 0 < ε) (N : ℕ)
    (hN : (1 - detectProb w lo hi r₀ (ε / 2)) ^ N ≤ δ) (r : X → ℝ) (hr : G r) :
    1 - δ ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
      |(spotCheck (fun r => Real.log (Zw w r)) r₀ a).output r - Real.log (Zw w r)| ≤ ε / 2),
      ∏ k, sampler w lo hi r₀ (a k) := by
  refine spotCheck_correct (G := G) (Φ := fun r => Real.log (Zw w r)) r₀ N (sampler w lo hi r₀)
    (sampler_nonneg hw hr₀) (sampler_sum hU hV) hε.le (min_le_left _ _) (fun r' hr' hfar => ?_) hN r hr
  exact (min_le_right _ _).trans (detect_ge hw hx₀ hr₀ (hG r' hr') hU hV hfar)

/-! ### The lower bound: disjoint dips -/

open Classical in
/-- The alternative that is lowered to the floor of the box on `D`. -/
noncomputable def dipAlt (lo r : X → ℝ) (D : Finset X) (x : X) : ℝ := if x ∈ D then lo x else r x

omit [Fintype X] in
theorem dipAlt_mem {lo hi r : X → ℝ} (hr : Box lo hi r) (D : Finset X) : Box lo hi (dipAlt lo r D) := by
  intro x
  unfold dipAlt
  by_cases h : x ∈ D
  · rw [if_pos h]; exact ⟨le_rfl, le_trans (hr x).1 (hr x).2⟩
  · rw [if_neg h]; exact hr x

omit [Fintype X] in
theorem dipAlt_ne {lo r : X → ℝ} {D : Finset X} {x : X} (h : dipAlt lo r D x ≠ r x) : x ∈ D := by
  by_contra hx
  exact h (by unfold dipAlt; rw [if_neg hx])

theorem Zw_dipAlt (w lo r : X → ℝ) (D : Finset X) :
    Zw w (dipAlt lo r D) = Zw w r + ∑ x ∈ D, dip w lo r x := by
  classical
  unfold Zw
  have h1 : ∑ x ∈ D, dip w lo r x = ∑ x, if x ∈ D then dip w lo r x else 0 := by
    rw [Finset.sum_ite_mem, Finset.univ_inter]
  rw [h1, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun x _ => ?_
  unfold dipAlt dip
  by_cases h : x ∈ D
  · rw [if_pos h, if_pos h]; ring
  · rw [if_neg h, if_neg h]; ring

/-- A dip set whose dip weight exceeds `(e^ε - 1) Z` changes `log Z` by more than `ε`. -/
theorem logZ_dipAlt_gt {w lo r : X → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀) {D : Finset X} {ε : ℝ}
    (hD : (Real.exp ε - 1) * Zw w r < ∑ x ∈ D, dip w lo r x) :
    ε < |Real.log (Zw w (dipAlt lo r D)) - Real.log (Zw w r)| := by
  have hZ : 0 < Zw w r := Zw_pos hw hx₀
  have hgt : Real.exp ε * Zw w r < Zw w (dipAlt lo r D) := by rw [Zw_dipAlt]; nlinarith
  have hlog : ε + Real.log (Zw w r) < Real.log (Zw w (dipAlt lo r D)) := by
    have h := Real.log_lt_log (mul_pos (Real.exp_pos ε) hZ) hgt
    rwa [Real.log_mul (Real.exp_pos ε).ne' hZ.ne', Real.log_exp] at h
  exact lt_of_lt_of_le (by linarith) (le_abs_self _)

open Classical in
/-- **Lower bound for every randomised algorithm on a box class.**  If the algorithms `alg ω`, mixed with the
probability vector `P`, return `log Z` within `ε/2` with probability at least `1 - δ` on every member of the box, and
`D j` are pairwise disjoint sets whose dip weights at `r` exceed `(e^ε - 1) Z(r)`, then the expected number of
evaluations on `r` is at least `(1 - 2δ)` times the number of these sets. -/
theorem box_expected_queries_ge {Ω : Type*} [Fintype Ω] {ι : Type*} [Fintype ι] {w lo hi : X → ℝ}
    (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀) (alg : Ω → QueryAlgorithm X)
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ r, Box lo hi r →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output r - Real.log (Zw w r)| ≤ ε / 2), P ω)
    {r : X → ℝ} (hr : Box lo hi r) (D : ι → Finset X)
    (hdisj : ∀ i j, i ≠ j → Disjoint (D i) (D j))
    (hD : ∀ j, (Real.exp ε - 1) * Zw w r < ∑ x ∈ D j, dip w lo r x) :
    (1 - 2 * δ) * (Fintype.card ι : ℝ) ≤ ∑ ω, P ω * ((alg ω).queries r).card := by
  have key := expected_queries_ge_packing (G := Box lo hi) (Φ := fun r => Real.log (Zw w r)) alg P hP hP1
    hcorr hr (fun j => dipAlt lo r (D j)) (fun j => dipAlt_mem hr (D j))
    (fun j => logZ_dipAlt_gt hw hx₀ (hD j)) (fun _ => (1 : ℝ)) (fun _ => zero_le_one) (B := 1) ?_
  · simpa using key
  · intro a
    have hsub : (univ.filter (fun j => dipAlt lo r (D j) a ≠ r a)).card ≤ 1 := by
      rw [Finset.card_le_one]
      intro i hi j hj
      by_contra hij
      have hai : a ∈ D i := dipAlt_ne (Finset.mem_filter.mp hi).2
      have haj : a ∈ D j := dipAlt_ne (Finset.mem_filter.mp hj).2
      exact (Finset.disjoint_left.mp (hdisj i j hij)) hai haj
    have : ∑ j ∈ univ.filter (fun j => dipAlt lo r (D j) a ≠ r a), (1 : ℝ)
        = ((univ.filter (fun j => dipAlt lo r (D j) a ≠ r a)).card : ℝ) := by simp
    rw [this]
    exact_mod_cast hsub

/-! ### The bracket of the estimate: the lower end is a mean -/

/-- **Gibbs–Bogoliubov / Jensen.**  With `W = ∑ w` and `m = (∑ w r)/W` the mean of the remainder under the Gibbs
measure of the known function: `log W - m ≤ log Z`. -/
theorem jensen_bracket {w r : X → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀) :
    Real.log (∑ x, w x) - (∑ x, w x * r x) / ∑ x, w x ≤ Real.log (Zw w r) := by
  have hW : 0 < ∑ x, w x :=
    Finset.sum_pos' (fun x _ => hw x) ⟨x₀, mem_univ x₀, hx₀⟩
  set m : ℝ := (∑ x, w x * r x) / ∑ x, w x with hm
  have hZ : 0 < Zw w r := Zw_pos hw hx₀
  -- `Z = e^{-m} ∑ w e^{-(r - m)} ≥ e^{-m} ∑ w (1 - (r - m)) = e^{-m} W`
  have h1 : Real.exp (-m) * ∑ x, w x ≤ Zw w r := by
    have h2 : ∀ x, w x * (1 - (r x - m)) ≤ w x * Real.exp (-(r x - m)) := fun x =>
      mul_le_mul_of_nonneg_left (by linarith [Real.add_one_le_exp (-(r x - m))]) (hw x)
    have h3 : ∑ x, w x * (1 - (r x - m)) = ∑ x, w x := by
      have : ∑ x, w x * (1 - (r x - m)) = (∑ x, w x) - (∑ x, w x * r x) + m * ∑ x, w x := by
        simp only [mul_sub, mul_one, Finset.sum_sub_distrib, Finset.mul_sum]
        have : ∑ x, w x * m = ∑ x, m * w x := Finset.sum_congr rfl fun x _ => mul_comm _ _
        linarith
      rw [this, hm, div_mul_cancel₀ _ hW.ne']
      ring
    have h4 : Zw w r = Real.exp (-m) * ∑ x, w x * Real.exp (-(r x - m)) := by
      unfold Zw
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl fun x _ => ?_
      rw [show -r x = -m + -(r x - m) by ring, Real.exp_add]
      ring
    rw [h4]
    refine mul_le_mul_of_nonneg_left ?_ (Real.exp_pos _).le
    calc ∑ x, w x = ∑ x, w x * (1 - (r x - m)) := h3.symm
      _ ≤ ∑ x, w x * Real.exp (-(r x - m)) := Finset.sum_le_sum fun x _ => h2 x
  have h5 := Real.log_le_log (mul_pos (Real.exp_pos (-m)) hW) h1
  rw [Real.log_mul (Real.exp_pos _).ne' hW.ne', Real.log_exp] at h5
  linarith

/-! ### Non-vacuity: the constant box at the centre -/

/-- For the constant box `[-ρ₋, ρ₊]` at the centre `r = 0` the total dip weight is `(e^{ρ₋} - 1) W` and the total bump
weight `(1 - e^{-ρ₊}) W`, `W = ∑ w = Z`. -/
theorem centre_weights (w : X → ℝ) (ρm ρp : ℝ) :
    Zw w (fun _ => 0) = ∑ x, w x ∧
    ∑ x, dip w (fun _ => -ρm) (fun _ => 0) x = (Real.exp ρm - 1) * ∑ x, w x ∧
    ∑ x, bump w (fun _ => ρp) (fun _ => 0) x = (1 - Real.exp (-ρp)) * ∑ x, w x := by
  refine ⟨?_, ?_, ?_⟩
  · unfold Zw; simp
  · unfold dip
    simp only [neg_neg, neg_zero, Real.exp_zero]
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun x _ => by ring
  · unfold bump
    simp only [neg_zero, Real.exp_zero]
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun x _ => by ring

end MetricChain.BoxClass
