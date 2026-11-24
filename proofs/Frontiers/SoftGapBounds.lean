import Mathlib
import proofs.Frontiers.QueryLowerBound
import proofs.Frontiers.ExponentialWeights
import proofs.Frontiers.ProductRates

/-!
# Soft-gap bounds: randomised estimation of free energies from both sides

`QueryLowerBound.lean` shows that every algorithm for `log Z` must reach within slack
`(Λ(y) + ε)/β` of every point `y`, where `Λ` is the soft gap.  This file shows that the same
quantity gives an *upper* bound for randomised algorithms, proves the product forms, and
separates deterministic from randomised cost on the cube.

* `softGap_le_add_slack` — the soft gap is Lipschitz for `β` times the slack.
* `detection_weight_ge` — every admissible alternative with `Z' ≥ (1 + η) Z` differs from the
  instance on a set of weight at least `η Z`, for the weights
  `dipWeight z = exp (-β E z) ((1 + η) exp (Λ z) - 1)`; `gibbs_weight_ne_ge` is the companion
  for alternatives with a smaller partition function.
* `thermalSampler`, `thermal_spotCheck_correct`, `exists_thermal_spotCheck_sample_size` — the
  spot-check with samples from `½ Gibbs + ½ normalised dip weights` returns `log Z` within
  `ε / 2` with probability `1 - δ` on every admissible residual, with
  `N ≈ 2 log (1/δ) E_π[exp Λ] / (1 - exp (-ε/2))` evaluations on the hint
  (`sum_dipWeight_eq`).
* `cube_deterministic_lower_bound`, `cube_dipWeight_sum` — on the cube every deterministic
  algorithm needs almost `2^n` evaluations, the spot-check about `(2 / (1 + e^{-βc}))^n`.
* `softGap_hamEnv_additive`, `thermal_product_randomized` — on product landscapes the soft gap
  is a sum over the sites and the randomised lower bound of `thermal_expected_queries_ge`
  factorises: the counterpart, with the soft gap as distortion budget, of `product_exp_weights`
  (energy gap) and `thermal_product_exp_weights` (free-energy gap).
-/

namespace MetricChain

open Finset

section SoftGapSampling

variable {X : Type*} [Fintype X] [Nonempty X]

/-- `exp (softGap y) · ∑_a exp (-β (E a + s(a, y))) = Z`. -/
theorem exp_softGap_mul (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (y : X) :
    Real.exp (softGap β d f g y) * ∑ x, Real.exp (-β * (f x + g x + slack d g x y)) =
      ∑ x, Real.exp (-β * (f x + g x)) := by
  have hZ : 0 < ∑ x, Real.exp (-β * (f x + g x)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hS : 0 < ∑ x, Real.exp (-β * (f x + g x + slack d g x y)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  unfold softGap
  rw [Real.exp_sub, Real.exp_log hZ, Real.exp_log hS]
  field_simp

/-- **The soft gap is Lipschitz for `β` times the slack**: `Λ(x) ≤ Λ(z) + β s(z, x)`. -/
theorem softGap_le_add_slack {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ) {β : ℝ}
    (hβ : 0 ≤ β) (x z : X) :
    softGap β d f g x ≤ softGap β d f g z + β * slack d g z x := by
  have hSz : 0 < ∑ a, Real.exp (-β * (f a + g a + slack d g a z)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hle : Real.exp (-(β * slack d g z x)) * ∑ a, Real.exp (-β * (f a + g a + slack d g a z)) ≤
      ∑ a, Real.exp (-β * (f a + g a + slack d g a x)) := by
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum fun a _ => ?_
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    have htri := (slack_isEnvelope hd g).triangle a z x
    nlinarith
  have hlog := Real.log_le_log (mul_pos (Real.exp_pos _) hSz) hle
  rw [Real.log_mul (Real.exp_pos _).ne' hSz.ne', Real.log_exp] at hlog
  unfold softGap
  linarith

open Classical in
/-- **Detection weight of an alternative with a larger partition function.**  Let `g'` be
admissible with `Z(f + g') ≥ (1 + η) Z(f + g)`.  Then the points where `g'` differs from `g`
carry at least the weight `η Z` for the weights
`w z = exp (-β E z) · ((1 + η) exp (Λ z) - 1)`, `Λ` the soft gap.

Proof: let `h = g - g'`.  If `exp (β h) ≤ (1 + η) exp Λ` everywhere, compare term by term.
Otherwise some `x₀` has a deeper dip than its soft gap allows, `g'` then differs from `g` on the
whole slack ball of that depth around `x₀`, and on that ball the weights dominate
`exp (-β E z) · ((1 + η) exp (Λ x₀ - β s(z, x₀)) - 1)` because `Λ` is `β s`-Lipschitz; the sum
of these over all `z` is exactly `η Z`. -/
theorem detection_weight_ge {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) {g g' : X → ℝ}
    (hg : Admissible d g) (hg' : Admissible d g') {β η : ℝ} (hβ : 0 ≤ β) (hη : 0 ≤ η)
    (hsens : (1 + η) * ∑ x, Real.exp (-β * (f x + g x)) ≤ ∑ x, Real.exp (-β * (f x + g' x))) :
    η * ∑ x, Real.exp (-β * (f x + g x)) ≤
      ∑ z ∈ univ.filter (fun z => g' z ≠ g z),
        Real.exp (-β * (f z + g z)) * ((1 + η) * Real.exp (softGap β d f g z) - 1) := by
  have hΛ0 : ∀ z, 0 ≤ softGap β d f g z := fun z => softGap_nonneg hg f hβ z
  have hterm0 : ∀ z, 0 ≤ Real.exp (-β * (f z + g z)) *
      ((1 + η) * Real.exp (softGap β d f g z) - 1) := by
    intro z
    have h1 : (1 : ℝ) ≤ Real.exp (softGap β d f g z) := Real.one_le_exp (hΛ0 z)
    have h2 : (1 : ℝ) ≤ (1 + η) * Real.exp (softGap β d f g z) := by nlinarith
    exact mul_nonneg (Real.exp_pos _).le (by linarith)
  by_cases hA : ∀ x, Real.exp (β * (g x - g' x)) ≤ (1 + η) * Real.exp (softGap β d f g x)
  · -- Case A: compare term by term
    have hdiff : ∑ x, Real.exp (-β * (f x + g' x)) - ∑ x, Real.exp (-β * (f x + g x)) =
        ∑ x, Real.exp (-β * (f x + g x)) * (Real.exp (β * (g x - g' x)) - 1) := by
      rw [← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl fun x _ => ?_
      rw [mul_sub, mul_one, ← Real.exp_add]
      congr 2
      ring
    have hfilter : ∑ x, Real.exp (-β * (f x + g x)) * (Real.exp (β * (g x - g' x)) - 1) =
        ∑ x ∈ univ.filter (fun z => g' z ≠ g z),
          Real.exp (-β * (f x + g x)) * (Real.exp (β * (g x - g' x)) - 1) := by
      symm
      apply Finset.sum_subset (Finset.filter_subset _ _)
      intro x _ hx
      have hxe : g' x = g x := by
        by_contra hne
        exact hx (Finset.mem_filter.mpr ⟨mem_univ x, hne⟩)
      rw [hxe, sub_self, mul_zero, Real.exp_zero, sub_self, mul_zero]
    have hbound : ∑ x ∈ univ.filter (fun z => g' z ≠ g z),
        Real.exp (-β * (f x + g x)) * (Real.exp (β * (g x - g' x)) - 1) ≤
          ∑ z ∈ univ.filter (fun z => g' z ≠ g z),
            Real.exp (-β * (f z + g z)) * ((1 + η) * Real.exp (softGap β d f g z) - 1) := by
      refine Finset.sum_le_sum fun x _ => ?_
      exact mul_le_mul_of_nonneg_left (by linarith [hA x]) (Real.exp_pos _).le
    linarith
  · -- Case B: a dip deeper than the soft gap allows
    obtain ⟨x₀, hx₀⟩ := not_forall.mp hA
    have hx₀' : (1 + η) * Real.exp (softGap β d f g x₀) < Real.exp (β * (g x₀ - g' x₀)) :=
      not_le.mp hx₀
    -- the comparison terms
    have hT : ∑ z, Real.exp (-β * (f z + g z)) *
        ((1 + η) * Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀)) - 1) =
          η * ∑ x, Real.exp (-β * (f x + g x)) := by
      have h1 : ∀ z, Real.exp (-β * (f z + g z)) *
          ((1 + η) * Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀)) - 1) =
            (1 + η) * Real.exp (softGap β d f g x₀) *
              Real.exp (-β * (f z + g z + slack d g z x₀)) - Real.exp (-β * (f z + g z)) := by
        intro z
        have he : Real.exp (-β * (f z + g z + slack d g z x₀)) =
            Real.exp (-β * (f z + g z)) * Real.exp (-(β * slack d g z x₀)) := by
          rw [← Real.exp_add]
          congr 1
          ring
        rw [he]
        ring
      rw [Finset.sum_congr rfl fun z _ => h1 z, Finset.sum_sub_distrib, ← Finset.mul_sum,
        mul_assoc, exp_softGap_mul]
      ring
    have hsplit : ∑ z, Real.exp (-β * (f z + g z)) *
        ((1 + η) * Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀)) - 1) ≤
          ∑ z ∈ univ.filter (fun z => g' z ≠ g z), Real.exp (-β * (f z + g z)) *
            ((1 + η) * Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀)) - 1) := by
      rw [← Finset.sum_filter_add_sum_filter_not univ (fun z => g' z ≠ g z)]
      have hneg : ∑ z ∈ univ.filter (fun z => ¬ g' z ≠ g z), Real.exp (-β * (f z + g z)) *
          ((1 + η) * Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀)) - 1) ≤ 0 := by
        refine Finset.sum_nonpos fun z hz => ?_
        have hze : g' z = g z := not_not.mp (Finset.mem_filter.mp hz).2
        -- an undisturbed point is at slack at least the depth of the dip at `x₀`
        have hadm := hg' z x₀
        have hs : g x₀ - g' x₀ ≤ slack d g z x₀ := by
          have h' : slack d g z x₀ = d z x₀ - g z + g x₀ := rfl
          rw [hze] at hadm
          linarith
        have hexp : Real.exp (β * (g x₀ - g' x₀)) ≤ Real.exp (β * slack d g z x₀) :=
          Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left hs hβ)
        have hlt : (1 + η) * Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀)) ≤
            1 := by
          have h1 : (1 + η) * Real.exp (softGap β d f g x₀) ≤ Real.exp (β * slack d g z x₀) :=
            hx₀'.le.trans hexp
          calc (1 + η) * Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀))
              ≤ Real.exp (β * slack d g z x₀) * Real.exp (-(β * slack d g z x₀)) :=
                mul_le_mul_of_nonneg_right h1 (Real.exp_pos _).le
            _ = 1 := by rw [← Real.exp_add, add_neg_cancel, Real.exp_zero]
        exact mul_nonpos_of_nonneg_of_nonpos (Real.exp_pos _).le (by linarith)
      linarith
    have hdom : ∑ z ∈ univ.filter (fun z => g' z ≠ g z), Real.exp (-β * (f z + g z)) *
        ((1 + η) * Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀)) - 1) ≤
          ∑ z ∈ univ.filter (fun z => g' z ≠ g z),
            Real.exp (-β * (f z + g z)) * ((1 + η) * Real.exp (softGap β d f g z) - 1) := by
      refine Finset.sum_le_sum fun z _ => ?_
      refine mul_le_mul_of_nonneg_left ?_ (Real.exp_pos _).le
      have hlip := softGap_le_add_slack hd f g hβ x₀ z
      have h1 : Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀)) ≤
          Real.exp (softGap β d f g z) := by
        rw [← Real.exp_add]
        apply Real.exp_le_exp.mpr
        linarith
      have h2 : (1 + η) * (Real.exp (softGap β d f g x₀) * Real.exp (-(β * slack d g z x₀))) ≤
          (1 + η) * Real.exp (softGap β d f g z) :=
        mul_le_mul_of_nonneg_left h1 (by linarith)
      linarith [mul_assoc (1 + η) (Real.exp (softGap β d f g x₀))
        (Real.exp (-(β * slack d g z x₀)))]
    linarith

omit [Nonempty X] in
open Classical in
/-- **Detection weight of an alternative with a smaller partition function**: the points where
`g'` differs from `g` carry Gibbs weight at least `Z(f + g) - Z(f + g')`. -/
theorem gibbs_weight_ne_ge (f g g' : X → ℝ) (β : ℝ) :
    ∑ x, Real.exp (-β * (f x + g x)) - ∑ x, Real.exp (-β * (f x + g' x)) ≤
      ∑ z ∈ univ.filter (fun z => g' z ≠ g z), Real.exp (-β * (f z + g z)) := by
  have h1 := Finset.sum_filter_add_sum_filter_not univ (fun z => g' z ≠ g z)
    (fun z => Real.exp (-β * (f z + g z)))
  have h2 : ∑ z ∈ univ.filter (fun z => ¬ g' z ≠ g z), Real.exp (-β * (f z + g z)) ≤
      ∑ x, Real.exp (-β * (f x + g' x)) := by
    calc ∑ z ∈ univ.filter (fun z => ¬ g' z ≠ g z), Real.exp (-β * (f z + g z))
        = ∑ z ∈ univ.filter (fun z => ¬ g' z ≠ g z), Real.exp (-β * (f z + g' z)) := by
          refine Finset.sum_congr rfl fun z hz => ?_
          rw [not_not.mp (Finset.mem_filter.mp hz).2]
      _ ≤ ∑ x, Real.exp (-β * (f x + g' x)) :=
          Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
            fun z _ _ => (Real.exp_pos _).le
  linarith

/-- The unnormalised dip weights `exp (-β E z) · ((1 + η) exp (Λ z) - 1)`. -/
noncomputable def dipWeight (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (η : ℝ) (z : X) : ℝ :=
  Real.exp (-β * (f z + g z)) * ((1 + η) * Real.exp (softGap β d f g z) - 1)

/-- The sampling distribution of the thermal spot-check: half Gibbs measure of the hint (for
alternatives with a smaller partition function), half normalised dip weights (for alternatives
with a larger one). -/
noncomputable def thermalSampler (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (η : ℝ) (z : X) : ℝ :=
  1 / 2 * (Real.exp (-β * (f z + g z)) / ∑ x, Real.exp (-β * (f x + g x))) +
    1 / 2 * (dipWeight β d f g η z / ∑ x, dipWeight β d f g η x)

open Classical in
/-- **A randomised upper bound for the free energy in terms of soft gaps.**  Let `g₀` be an
admissible hint, `β ≥ 0`, `ε > 0`, `η = exp (ε/2) - 1`, and let

`p = ½ · min (η Z / W, 1 - exp (-ε/2))`,   `W = ∑_z exp (-β E z) ((1 + η) exp (Λ z) - 1)`.

If `(1 - p)^N ≤ δ`, the spot-check with `N` independent samples of `thermalSampler` returns
`log Z` within `ε / 2` with probability at least `1 - δ` on **every** admissible residual; on
the hint it makes at most `N` evaluations.  Since `W / Z ≤ (1 + η) E_π exp Λ`, about
`2 exp (ε/2) E_π[exp Λ] log (1/δ) / (exp (ε/2) - 1)` evaluations suffice: the same soft gaps
that give the lower bound `thermal_expected_queries_ge` give an upper bound. -/
theorem thermal_spotCheck_correct {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) {g₀ : X → ℝ}
    (hg₀ : Admissible d g₀) {β ε δ : ℝ} (hβ : 0 ≤ β) (hε : 0 < ε) (N : ℕ)
    (hN : (1 - 1 / 2 * min ((Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
        ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) (1 - Real.exp (-(ε / 2)))) ^ N ≤ δ)
    (g : X → ℝ) (hg : Admissible d g) :
    1 - δ ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
      |(spotCheck (fun g => Real.log (∑ x, Real.exp (-β * (f x + g x)))) g₀ a).output g -
        Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2),
      ∏ k, thermalSampler β d f g₀ (Real.exp (ε / 2) - 1) (a k) := by
  have hη : 0 < Real.exp (ε / 2) - 1 := by
    have := Real.add_one_lt_exp (show ε / 2 ≠ 0 by positivity)
    linarith
  have hZ : 0 < ∑ x, Real.exp (-β * (f x + g₀ x)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hw0 : ∀ z, 0 < dipWeight β d f g₀ (Real.exp (ε / 2) - 1) z := by
    intro z
    have h1 : (1 : ℝ) ≤ Real.exp (softGap β d f g₀ z) :=
      Real.one_le_exp (softGap_nonneg hg₀ f hβ z)
    unfold dipWeight
    exact mul_pos (Real.exp_pos _) (by nlinarith)
  have hW : 0 < ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x :=
    Finset.sum_pos (fun z _ => hw0 z) univ_nonempty
  have hb : 0 ≤ 1 - Real.exp (-(ε / 2)) := by
    have : Real.exp (-(ε / 2)) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
    linarith
  have hb1 : 1 - Real.exp (-(ε / 2)) ≤ 1 := by linarith [Real.exp_pos (-(ε / 2))]
  refine spotCheck_correct (G := Admissible d)
    (Φ := fun g => Real.log (∑ x, Real.exp (-β * (f x + g x)))) g₀ N
    (thermalSampler β d f g₀ (Real.exp (ε / 2) - 1)) (fun z => ?_) ?_ hε.le ?_
    (fun g hg hfar => ?_) hN g hg
  · unfold thermalSampler
    have h1 : 0 ≤ Real.exp (-β * (f z + g₀ z)) / ∑ x, Real.exp (-β * (f x + g₀ x)) :=
      div_nonneg (Real.exp_pos _).le hZ.le
    have h2 : 0 ≤ dipWeight β d f g₀ (Real.exp (ε / 2) - 1) z /
        ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x := div_nonneg (hw0 z).le hW.le
    linarith
  · unfold thermalSampler
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.sum_div,
      ← Finset.sum_div, div_self hZ.ne', div_self hW.ne']
    norm_num
  · have := min_le_right ((Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
      ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) (1 - Real.exp (-(ε / 2)))
    linarith
  · -- every distinguishable alternative differs from the hint on a set of probability ≥ p
    have hZg : 0 < ∑ x, Real.exp (-β * (f x + g x)) :=
      Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
    have hqsum : ∀ S : Finset X, ∑ x ∈ S, thermalSampler β d f g₀ (Real.exp (ε / 2) - 1) x =
        1 / 2 * ((∑ x ∈ S, Real.exp (-β * (f x + g₀ x))) / ∑ x, Real.exp (-β * (f x + g₀ x))) +
          1 / 2 * ((∑ x ∈ S, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) /
            ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) := by
      intro S
      unfold thermalSampler
      rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.sum_div,
        ← Finset.sum_div]
    rw [hqsum]
    have hpart1 : 0 ≤ (∑ x ∈ univ.filter (fun x => g x ≠ g₀ x), Real.exp (-β * (f x + g₀ x))) /
        ∑ x, Real.exp (-β * (f x + g₀ x)) :=
      div_nonneg (Finset.sum_nonneg fun x _ => (Real.exp_pos _).le) hZ.le
    have hpart2 : 0 ≤ (∑ x ∈ univ.filter (fun x => g x ≠ g₀ x),
        dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) /
          ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x :=
      div_nonneg (Finset.sum_nonneg fun x _ => (hw0 x).le) hW.le
    rcases lt_abs.mp hfar with hup | hdown
    · -- the alternative has a larger partition function: dip weights
      have hexp : Real.exp (ε / 2) * ∑ x, Real.exp (-β * (f x + g₀ x)) ≤
          ∑ x, Real.exp (-β * (f x + g x)) := by
        have h1 : ε / 2 + Real.log (∑ x, Real.exp (-β * (f x + g₀ x))) ≤
            Real.log (∑ x, Real.exp (-β * (f x + g x))) := by linarith
        have h2 := Real.exp_le_exp.mpr h1
        rwa [Real.exp_add, Real.exp_log hZ, Real.exp_log hZg] at h2
      have hdet := detection_weight_ge hd f hg₀ hg hβ hη.le (by
        rw [add_sub_cancel]
        exact hexp)
      have hfrac : (Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
          ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x ≤
            (∑ x ∈ univ.filter (fun x => g x ≠ g₀ x),
              dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) /
                ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x :=
        div_le_div_of_nonneg_right hdet hW.le
      have hmin := min_le_left ((Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
        ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) (1 - Real.exp (-(ε / 2)))
      linarith
    · -- the alternative has a smaller partition function: Gibbs weights
      have hexp : ∑ x, Real.exp (-β * (f x + g x)) ≤
          Real.exp (-(ε / 2)) * ∑ x, Real.exp (-β * (f x + g₀ x)) := by
        have h1 : Real.log (∑ x, Real.exp (-β * (f x + g x))) ≤
            -(ε / 2) + Real.log (∑ x, Real.exp (-β * (f x + g₀ x))) := by linarith
        have h2 := Real.exp_le_exp.mpr h1
        rwa [Real.exp_add, Real.exp_log hZ, Real.exp_log hZg] at h2
      have hdet := gibbs_weight_ne_ge f g₀ g β
      have hfrac : 1 - Real.exp (-(ε / 2)) ≤
          (∑ x ∈ univ.filter (fun x => g x ≠ g₀ x), Real.exp (-β * (f x + g₀ x))) /
            ∑ x, Real.exp (-β * (f x + g₀ x)) := by
        rw [le_div_iff₀ hZ]
        nlinarith
      have hmin := min_le_right ((Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
        ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) (1 - Real.exp (-(ε / 2)))
      linarith

omit [Nonempty X] in
/-- The normalising constant of the dip weights: `W = (1 + η) ∑_z exp (-β E z) exp (Λ z) - Z`. -/
theorem sum_dipWeight_eq (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (η : ℝ) :
    ∑ z, dipWeight β d f g η z =
      (1 + η) * ∑ z, Real.exp (-β * (f z + g z)) * Real.exp (softGap β d f g z) -
        ∑ z, Real.exp (-β * (f z + g z)) := by
  unfold dipWeight
  rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun z _ => by ring

/-- **A sample size always exists.**  For every `δ > 0` some `N` satisfies the hypothesis `hN`
of `thermal_spotCheck_correct`: the detection probability `p` is positive. -/
theorem exists_thermal_spotCheck_sample_size {d : X → X → ℝ} (f : X → ℝ) {g₀ : X → ℝ}
    (hg₀ : Admissible d g₀) {β ε δ : ℝ} (hβ : 0 ≤ β) (hε : 0 < ε) (hδ : 0 < δ) :
    ∃ N : ℕ, (1 - 1 / 2 * min ((Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
        ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) (1 - Real.exp (-(ε / 2)))) ^ N ≤ δ := by
  have hη : 0 < Real.exp (ε / 2) - 1 := by
    have := Real.add_one_lt_exp (show ε / 2 ≠ 0 by positivity)
    linarith
  have hZ : 0 < ∑ x, Real.exp (-β * (f x + g₀ x)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hw0 : ∀ z, 0 < dipWeight β d f g₀ (Real.exp (ε / 2) - 1) z := by
    intro z
    have h1 : (1 : ℝ) ≤ Real.exp (softGap β d f g₀ z) :=
      Real.one_le_exp (softGap_nonneg hg₀ f hβ z)
    unfold dipWeight
    exact mul_pos (Real.exp_pos _) (by nlinarith)
  have hW : 0 < ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x :=
    Finset.sum_pos (fun z _ => hw0 z) univ_nonempty
  have hb : 0 < 1 - Real.exp (-(ε / 2)) := by
    have h0 := Real.exp_lt_exp.mpr (show -(ε / 2) < 0 by linarith)
    rw [Real.exp_zero] at h0
    linarith
  have hb1 : 1 - Real.exp (-(ε / 2)) ≤ 1 := by linarith [Real.exp_pos (-(ε / 2))]
  have hmin : 0 < min ((Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
      ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) (1 - Real.exp (-(ε / 2))) :=
    lt_min (div_pos (mul_pos hη hZ) hW) hb
  have hmin1 := min_le_right ((Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
    ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) (1 - Real.exp (-(ε / 2)))
  obtain ⟨N, hN⟩ := exists_pow_lt_of_lt_one hδ (show 1 - 1 / 2 * min
    ((Real.exp (ε / 2) - 1) * (∑ x, Real.exp (-β * (f x + g₀ x))) /
      ∑ x, dipWeight β d f g₀ (Real.exp (ε / 2) - 1) x) (1 - Real.exp (-(ε / 2))) < 1 by linarith)
  exact ⟨N, hN.le⟩

end SoftGapSampling

/-! ### The cube: deterministic against randomised -/

section CubeSeparation

/-- **Every deterministic algorithm for the free energy of the cube evaluates almost
everything.**  `n` two-state sites, zero known part, Hamming envelope with constant `c ≥ 0`,
`β > 0`.  If a deterministic algorithm returns `log Z(g)` within `ε / 2` for every admissible
residual, then on the zero residual it makes at least `exp (-tε/β) · 2^n / (1 + e^{-tc})^n`
evaluations, for every `t ≥ 0` — for bounded `ε` and large `t`, almost `2^n`.

Proof: its queries form a free-energy certificate (`thermal_queries_bracket`), and the entropy
bound `card_ge_entropy` applies with the uniform Gibbs measure (entropy `n log 2`). -/
theorem cube_deterministic_lower_bound (n : ℕ) (alg : QueryAlgorithm (Fin n → Bool))
    {β c ε t : ℝ} (hβ : 0 < β) (hc : 0 ≤ c) (ht : 0 ≤ t)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      |alg.output g - Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ ε / 2) :
    Real.exp (-(t * ε / β)) * 2 ^ n ≤
      (alg.queries fun _ => 0).card * (1 + Real.exp (-t * c)) ^ n := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc
  have hadm := admissible_zero_hamEnv (n := n) (c := c) hc
  have hA := thermal_queries_nonempty (fun _ : Fin n → Bool => (0 : ℝ)) alg hβ hcorr hadm
  have hbr := thermal_queries_bracket hd (fun _ : Fin n → Bool => (0 : ℝ)) alg hβ hcorr hadm
  have hZhi := Zhi_le_of_bracket hadm (fun _ : Fin n → Bool => (0 : ℝ)) _ hA hβ.le hbr
  have hB : ∀ a ∈ alg.queries (fun _ : Fin n → Bool => (0 : ℝ)),
      ∑ y, Real.exp (-t * slack (hamEnv fun _ : Fin n => c) (fun _ => 0) a y) ≤
        (1 + Real.exp (-t * c)) ^ n := by
    intro a _
    have h := sum_exp_hamEnv (σ := fun _ : Fin n => Bool) (fun _ => c) t a
    rw [Finset.prod_const, Finset.card_univ, Fintype.card_fin, Fintype.card_bool] at h
    refine le_of_eq ?_
    rw [show (1 + Real.exp (-t * c)) ^ n = (1 + ((2 : ℕ) - 1 : ℝ) * Real.exp (-t * c)) ^ n by
      norm_num, ← h]
    refine Finset.sum_congr rfl fun y _ => ?_
    congr 1
    unfold slack
    ring
  have hent := card_ge_entropy (hamEnv fun _ : Fin n => c) (fun _ : Fin n → Bool => (0 : ℝ))
    (fun _ => 0) _ hA hβ ht hZhi hB
  -- the Gibbs measure of the zero energy is uniform, with entropy `n log 2`
  have hπ : ∀ y : Fin n → Bool,
      gibbsProb β (fun y : Fin n → Bool => (0 : ℝ) + 0) y = ((2 : ℝ) ^ n)⁻¹ := by
    intro y
    simp [gibbsProb]
  have hH : -∑ y : Fin n → Bool, gibbsProb β (fun y : Fin n → Bool => (0 : ℝ) + 0) y *
      Real.log (gibbsProb β (fun y : Fin n → Bool => (0 : ℝ) + 0) y) = Real.log ((2 : ℝ) ^ n) := by
    simp only [hπ]
    rw [Finset.sum_const, Finset.card_univ, Real.log_inv]
    simp
  rw [hH] at hent
  have hcard : (0 : ℝ) < (alg.queries fun _ => 0).card := by
    exact_mod_cast Finset.card_pos.mpr hA
  have hBpos : (0 : ℝ) < (1 + Real.exp (-t * c)) ^ n := by positivity
  have hprod : (0 : ℝ) < (alg.queries fun _ => 0).card * (1 + Real.exp (-t * c)) ^ n :=
    mul_pos hcard hBpos
  have h1 : Real.log ((2 : ℝ) ^ n) - t * ε / β ≤
      Real.log ((alg.queries fun _ => 0).card * (1 + Real.exp (-t * c)) ^ n) := by linarith
  have h2 := Real.exp_le_exp.mpr h1
  rw [Real.exp_sub, Real.exp_log (by positivity), Real.exp_log hprod] at h2
  rw [Real.exp_neg, mul_comm]
  exact h2

/-- The normalising constant of the dip weights on the cube with zero residual:
`W = 2^n ((1 + η) (2 / (1 + e^{-βc}))^n - 1)`.  With `Z = 2^n` the detection probability of
`thermal_spotCheck_correct` is `½ min (η / ((1 + η) K^n - 1), 1 - e^{-ε/2})`,
`K = 2 / (1 + e^{-βc}) < 2`: the spot-check needs about `K^n` evaluations where every
deterministic algorithm needs about `2^n` (`cube_deterministic_lower_bound`). -/
theorem cube_dipWeight_sum (n : ℕ) (β c η : ℝ) :
    ∑ z : Fin n → Bool, dipWeight β (hamEnv fun _ : Fin n => c) (fun _ => 0) (fun _ => 0) η z =
      2 ^ n * ((1 + η) * (2 / (1 + Real.exp (-β * c))) ^ n - 1) := by
  have hterm : ∀ z : Fin n → Bool,
      dipWeight β (hamEnv fun _ : Fin n => c) (fun _ => 0) (fun _ => 0) η z =
        (1 + η) * (2 / (1 + Real.exp (-β * c))) ^ n - 1 := by
    intro z
    have hpos : (0 : ℝ) < 2 / (1 + Real.exp (-β * c)) := by positivity
    unfold dipWeight
    rw [cube_softGap_general, ← Real.rpow_natCast, Real.rpow_def_of_pos hpos]
    simp [mul_comm]
  rw [Finset.sum_congr rfl fun z _ => hterm z, Finset.sum_const, Finset.card_univ]
  simp

end CubeSeparation

/-! ### Product landscapes -/

section ProductRandomized

variable {ι : Type*} [Fintype ι] [DecidableEq ι] {σ : ι → Type*} [∀ i, DecidableEq (σ i)]
  [∀ i, Fintype (σ i)] [∀ i, Nonempty (σ i)]

/-- **The soft gap of a product landscape is the sum of the site soft gaps.**  Known part
`∑ i, φ i (x i)`, residual `∑ i, γ i (x i)`, envelope `hamEnv c`: the soft gap of a configuration
`y` is the sum over the sites of the soft gaps of `y i` in the one-site problems with the
discrete envelopes `discreteEnvelope (c i)`. -/
theorem softGap_hamEnv_additive (β : ℝ) (c : ι → ℝ) (φ γ : ∀ i, σ i → ℝ) (y : ∀ i, σ i) :
    softGap β (hamEnv c) (fun x => ∑ i, φ i (x i)) (fun x => ∑ i, γ i (x i)) y =
      ∑ i, softGap β (discreteEnvelope (c i)) (φ i) (γ i) (y i) := by
  have hZ : ∑ x : ∀ i, σ i, Real.exp (-β * (∑ i, φ i (x i) + ∑ i, γ i (x i))) =
      ∏ i, ∑ s, Real.exp (-β * (φ i s + γ i s)) := by
    have h := sum_prod_mul_exp_sum (σ := σ) (fun _ _ => (1 : ℝ)) (fun i s => φ i s + γ i s) β
    simp only [Finset.prod_const_one, one_mul] at h
    rw [← h]
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [Finset.sum_add_distrib]
  have hS : ∑ x : ∀ i, σ i, Real.exp (-β * (∑ i, φ i (x i) + ∑ i, γ i (x i) +
      slack (hamEnv c) (fun x => ∑ i, γ i (x i)) x y)) =
        ∏ i, ∑ s, Real.exp (-β * (φ i s + γ i s +
          slack (discreteEnvelope (c i)) (γ i) s (y i))) := by
    have h := sum_prod_mul_exp_sum (σ := σ) (fun _ _ => (1 : ℝ))
      (fun i s => φ i s + γ i s + slack (discreteEnvelope (c i)) (γ i) s (y i)) β
    simp only [Finset.prod_const_one, one_mul] at h
    rw [← h]
    refine Finset.sum_congr rfl fun x _ => ?_
    congr 2
    rw [slack_hamEnv_additive, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun i _ => ?_
    unfold slack discreteEnvelope
    ring
  unfold softGap
  rw [hZ, hS, Real.log_prod, Real.log_prod, ← Finset.sum_sub_distrib]
  · intro i _
    exact (Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty).ne'
  · intro i _
    exact (Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty).ne'

variable {Ω : Type*} [Fintype Ω]

open Classical in
/-- **Randomised lower bound for the free energy on product landscapes.**  Known part
`∑ i, φ i (x i)`, admissible residual `∑ i, γ i (x i)`, envelope `hamEnv c` with `c ≥ 0`, and a
randomised algorithm that returns `log Z` within `ε / 2` with probability at least `1 - δ` on
every admissible residual.  Let `r i` be site radii with
`softGap y + ε < β ∑ i, r i (y i)` for every configuration `y` (by `softGap_hamEnv_additive` the
left-hand side is a sum of site soft gaps), let `v i ≥ 0` be site weights, `t ≥ 0`, and let
`B i` bound, for every state `a` of site `i`, the weighted site sum

  `∑ s, v i s * exp (-t * (s_i(a, s) - r i s))`,   `s_i(a, s) = (if a = s then 0 else c i) - γ i a + γ i s`.

Then on the additive instance the expected number of evaluations satisfies

  `(1 - 2δ) ∏ i, ∑ s, v i s ≤ E|Q| · ∏ i, B i`.

This is `thermal_expected_queries_ge` for product weights; slack and radii are sums over the
sites, so both sides factorise.  It is the finite-temperature, randomised counterpart of
`product_exp_weights` (minimum) and `thermal_product_exp_weights` (deterministic): the energy
gap of the first and the free-energy gap of the second are replaced by the soft gap. -/
theorem thermal_product_randomized (c : ι → ℝ) (hc : ∀ i, 0 ≤ c i) (φ γ : ∀ i, σ i → ℝ)
    (hγ : Admissible (hamEnv c) (fun x : ∀ i, σ i => ∑ i, γ i (x i)))
    (alg : Ω → QueryAlgorithm (∀ i, σ i)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {β ε δ : ℝ} (hβ : 0 ≤ β)
    (hcorr : ∀ g, Admissible (hamEnv c) g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - Real.log (∑ x : ∀ i, σ i,
        Real.exp (-β * (∑ i, φ i (x i) + g x)))| ≤ ε / 2), P ω)
    (r : ∀ i, σ i → ℝ)
    (hr : ∀ y : ∀ i, σ i, softGap β (hamEnv c) (fun x => ∑ i, φ i (x i))
      (fun x => ∑ i, γ i (x i)) y + ε < β * ∑ i, r i (y i))
    {t : ℝ} (ht : 0 ≤ t) (v : ∀ i, σ i → ℝ) (hv : ∀ i s, 0 ≤ v i s) (B : ι → ℝ)
    (hB : ∀ i (a : σ i), ∑ s, v i s * Real.exp (-t * ((if a = s then 0 else c i) - γ i a + γ i s -
      r i s)) ≤ B i) :
    (1 - 2 * δ) * ∏ i, ∑ s, v i s ≤
      (∑ ω, P ω * ((alg ω).queries fun x => ∑ i, γ i (x i)).card) * ∏ i, B i := by
  have hd : IsEnvelope (hamEnv (σ := σ) c) := hamEnv_isEnvelope hc
  have key := thermal_expected_queries_ge hd (fun x : ∀ i, σ i => ∑ i, φ i (x i)) alg P hP hP1 hβ
    hcorr hγ (fun y => ∑ i, r i (y i)) hr ht (fun y : ∀ i, σ i => ∏ i, v i (y i))
    (fun y => Finset.prod_nonneg fun i _ => hv i (y i)) (B := ∏ i, B i) (fun a => ?_)
  · rwa [← Fintype.prod_sum] at key
  · have hexp : ∀ y : ∀ i, σ i, slack (hamEnv c) (fun x => ∑ i, γ i (x i)) a y - ∑ i, r i (y i) =
        ∑ i, ((if a i = y i then 0 else c i) - γ i (a i) + γ i (y i) - r i (y i)) := by
      intro y
      rw [slack_hamEnv_additive, ← Finset.sum_sub_distrib]
    simp only [hexp]
    rw [sum_prod_mul_exp_sum v (fun i s => (if a i = s then 0 else c i) - γ i (a i) + γ i s -
      r i s) t]
    exact Finset.prod_le_prod
      (fun i _ => Finset.sum_nonneg fun s _ => mul_nonneg (hv i s) (Real.exp_pos _).le)
      (fun i _ => hB i (a i))

end ProductRandomized

end MetricChain
