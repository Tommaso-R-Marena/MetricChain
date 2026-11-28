import Mathlib

/-!
# Phase II: the overlap of a reference with an ensemble — the exact steps of the bridge note

Source: `docs/phase2/BRIDGE_NOTE.md` (Theorem F, Corollary F1, Proposition F3, Theorem J).

The note relates the query complexity of a certified free energy to quantities of bridge
sampling (the overlap of the reference measure with the ensemble, the conductance of the
two-state estimating equations).  Its proofs consist of an isoperimetric tail inequality of
the archive (theory report, Lemma 11.43, which rests on Harper's theorem and is not formalised),
concentration inequalities (cited), and the deterministic steps checked here:

* `bridge_identity` — `E_π[min(w, θ)] = A · E_μ[min(1, θ/w)]` for every threshold `θ`: the partition
  function is a ratio of two means of variables with values in `[0, 1]`, one under the reference
  and one under the ensemble.
* `overlap_ge_of_tail_bound` — the dichotomy behind Theorem F: if the mass above the level `s` is
  at most `s·M` whenever the super-level set has at most `V` points, and `s·M ≤ 1/2`, then
  `Σ_x min(g x, s) ≥ min(N/2, s (V + 1))`.
* `tv_ge_of_agree_off` — Proposition F3: two weights that agree off a set `D` have ensembles at
  total variation distance at least `μ₀(Dᶜ)(1 − A₀/A₁)`; a change of the partition function
  cannot be hidden from samples in a set of small probability.
* `one_two_dips_gap`, `mixture_mean_diff_le` — Theorem J: the laws of the energy under one dip and
  under two disjoint dips are mixtures of the same two components, with weights that differ by
  `(m + v)/((1 + m)(1 + 2m)) ≤ 1/(1 + 2m)`.
* `ratio_within` — the last step of Corollary F1: two means known within a factor `1 ± η` give
  their ratio within `(1 − η)/(1 + η)` and `(1 + η)/(1 − η)`.
* `harmonic_between_min` — `min(a,b)/2 ≤ ab/(a+b) ≤ min(a,b)`: the conductance of two states is
  between half the overlap and the overlap.
* `sq_sum_sqrt_mul_le` — `(Σ √(p q))² ≤ (Σ p q / m)(Σ m)`: an off-diagonal conductance of the
  multistate equations is at least the squared Bhattacharyya coefficient of the pair, whatever
  the other states are.

Nothing here is probability theory; the probabilistic and isoperimetric steps are paper
proofs, labelled as such in the note.
-/

namespace MetricChain

open Finset

section BridgeOverlap

variable {X : Type*} [Fintype X]

/-- The pointwise form of the bridge identity. -/
theorem mul_min_one_div (w θ : ℝ) (hw : 0 < w) : w * min 1 (θ / w) = min w θ := by
  rw [mul_min_of_nonneg _ _ hw.le, mul_one, mul_div_cancel₀ _ hw.ne']

/-- **The bridge identity.**  For a reference `p`, a positive weight `w` with partition function
`A = Σ p w ≠ 0` and any threshold `θ`: the reference mean of `min(w, θ)` is `A` times the ensemble
mean of `min(1, θ/w)`. -/
theorem bridge_identity (p w : X → ℝ) (hw : ∀ x, 0 < w x) (θ : ℝ)
    (hA : (∑ x, p x * w x) ≠ 0) :
    ∑ x, p x * min (w x) θ
      = (∑ x, p x * w x) * ∑ x, (p x * w x / ∑ y, p y * w y) * min 1 (θ / w x) := by
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [← mul_min_one_div (w x) θ (hw x)]
  field_simp

theorem min_eq_sub_max (g s : ℝ) : min g s = g - max (g - s) 0 := by
  rcases le_total g s with h | h
  · rw [min_eq_left h, max_eq_right (by linarith)]; ring
  · rw [min_eq_right h, max_eq_left (by linarith)]; ring

/-- The overlap is the total mass minus the mass above the level. -/
theorem sum_min_eq_sub_tail (g : X → ℝ) (s : ℝ) :
    ∑ x, min (g x) s = ∑ x, g x - ∑ x, max (g x - s) 0 := by
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun x _ => min_eq_sub_max _ _

/-- The overlap is at least the level times the size of the super-level set. -/
theorem card_superlevel_mul_le_sum_min (g : X → ℝ) (hg : ∀ x, 0 ≤ g x) (s : ℝ) (hs : 0 ≤ s) :
    s * ((univ.filter fun x => s < g x).card : ℝ) ≤ ∑ x, min (g x) s := by
  have h1 : ∑ x ∈ univ.filter (fun x => s < g x), min (g x) s
      = s * ((univ.filter fun x => s < g x).card : ℝ) := by
    rw [Finset.sum_congr rfl (fun x hx => min_eq_right (Finset.mem_filter.mp hx).2.le),
      Finset.sum_const, nsmul_eq_mul, mul_comm]
  rw [← h1]
  exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
    fun x _ _ => le_min (hg x) hs

/-- **The dichotomy behind Theorem F.**  `g ≥ 0` on a finite set of `N` points with `Σ g = N`
(mean one under the uniform measure), `s ≥ 0`.  Suppose the mass above the level `s` is at most
`s·M·N` whenever at most `V` points lie above it, and `s·M ≤ 1/2`.  Then
`Σ_x min(g x, s) ≥ min(N/2, s (V + 1))`: either few points lie above the level and half of the
mass is below it, or more than `V` points lie above it. -/
theorem overlap_ge_of_tail_bound (g : X → ℝ) (hg : ∀ x, 0 ≤ g x) (s M : ℝ) (V : ℕ) (hs : 0 ≤ s)
    (hmean : ∑ x, g x = (Fintype.card X : ℝ))
    (htail : (univ.filter fun x => s < g x).card ≤ V →
      ∑ x, max (g x - s) 0 ≤ s * M * (Fintype.card X : ℝ))
    (hM : s * M ≤ 1 / 2) :
    min ((Fintype.card X : ℝ) / 2) (s * ((V : ℝ) + 1)) ≤ ∑ x, min (g x) s := by
  have hN : (0 : ℝ) ≤ (Fintype.card X : ℝ) := Nat.cast_nonneg _
  by_cases hcard : (univ.filter fun x => s < g x).card ≤ V
  · have h := htail hcard
    have h2 : s * M * (Fintype.card X : ℝ) ≤ (Fintype.card X : ℝ) / 2 := by nlinarith
    refine (min_le_left _ _).trans ?_
    rw [sum_min_eq_sub_tail, hmean]
    linarith
  · have hcard' : (V : ℝ) + 1 ≤ ((univ.filter fun x => s < g x).card : ℝ) := by
      exact_mod_cast Nat.lt_of_not_le hcard
    refine (min_le_right _ _).trans ?_
    exact (mul_le_mul_of_nonneg_left hcard' hs).trans (card_superlevel_mul_le_sum_min g hg s hs)

/-- **Proposition F3 (a change of the partition function cannot be hidden from samples).**
Weights `w₀, w₁` that agree off `D`, with partition functions `A₀, A₁ > 0` under the reference
`p`: the total variation distance of the two ensembles is at least `μ₀(Dᶜ)·(1 − A₀/A₁)`. -/
theorem tv_ge_of_agree_off [DecidableEq X] (p w₀ w₁ : X → ℝ) (D : Finset X)
    (hagree : ∀ x, x ∉ D → w₀ x = w₁ x) (A₀ A₁ : ℝ)
    (hA₀ : A₀ = ∑ x, p x * w₀ x) (hA₁ : A₁ = ∑ x, p x * w₁ x) (h0 : 0 < A₀) (h1 : 0 < A₁) :
    (∑ x ∈ univ \ D, p x * w₀ x / A₀) * (1 - A₀ / A₁)
      ≤ (1 / 2) * ∑ x, |p x * w₀ x / A₀ - p x * w₁ x / A₁| := by
  set a : X → ℝ := fun x => p x * w₀ x / A₀ - p x * w₁ x / A₁ with ha
  have hsum : ∑ x, a x = 0 := by
    simp only [ha, Finset.sum_sub_distrib, ← Finset.sum_div, ← hA₀, ← hA₁]
    rw [div_self h0.ne', div_self h1.ne', sub_self]
  have hsplit : ∑ x ∈ univ \ D, a x + ∑ x ∈ D, a x = ∑ x, a x :=
    Finset.sum_sdiff (Finset.subset_univ D)
  have habs : ∑ x ∈ univ \ D, |a x| + ∑ x ∈ D, |a x| = ∑ x, |a x| :=
    Finset.sum_sdiff (Finset.subset_univ D)
  have hle1 : ∑ x ∈ univ \ D, a x ≤ ∑ x ∈ univ \ D, |a x| :=
    Finset.sum_le_sum fun x _ => le_abs_self _
  have hle2 : -(∑ x ∈ D, a x) ≤ ∑ x ∈ D, |a x| := by
    rw [← Finset.sum_neg_distrib]
    exact Finset.sum_le_sum fun x _ => neg_le_abs _
  have hkey : (∑ x ∈ univ \ D, p x * w₀ x / A₀) * (1 - A₀ / A₁) = ∑ x ∈ univ \ D, a x := by
    rw [Finset.sum_mul]
    refine Finset.sum_congr rfl fun x hx => ?_
    have hxD : x ∉ D := (Finset.mem_sdiff.mp hx).2
    simp only [ha, ← hagree x hxD]
    field_simp
  rw [hkey]
  linarith

/-- The weights of the floor in the laws of the energy under one dip and under two disjoint dips
(`m` the excess mass of a dip, `v` the measure of its ball). -/
theorem one_two_dips_gap (m v : ℝ) (hm : 0 ≤ m) (hv : v ≤ 1) :
    (1 - v) / (1 + m) - (1 - 2 * v) / (1 + 2 * m) = (m + v) / ((1 + m) * (1 + 2 * m)) ∧
      (m + v) / ((1 + m) * (1 + 2 * m)) ≤ 1 / (1 + 2 * m) := by
  have h1 : (0 : ℝ) < 1 + m := by linarith
  have h2 : (0 : ℝ) < 1 + 2 * m := by linarith
  refine ⟨by field_simp; ring, ?_⟩
  rw [div_le_div_iff₀ (mul_pos h1 h2) h2]
  nlinarith

/-- Two mixtures of the same two components: a function with values in `[−1, 1]` has means
that differ by at most twice the difference of the mixing weights. -/
theorem mixture_mean_diff_le (a₀ a₁ F G : ℝ) (hF : |F| ≤ 1) (hG : |G| ≤ 1) :
    |(a₀ * F + (1 - a₀) * G) - (a₁ * F + (1 - a₁) * G)| ≤ 2 * |a₀ - a₁| := by
  have h : (a₀ * F + (1 - a₀) * G) - (a₁ * F + (1 - a₁) * G) = (a₀ - a₁) * (F - G) := by ring
  rw [h, abs_mul, mul_comm 2]
  refine mul_le_mul_of_nonneg_left ?_ (abs_nonneg _)
  calc |F - G| ≤ |F| + |G| := abs_sub _ _
    _ ≤ 2 := by linarith

/-- Two positive means known within a factor `1 ± η` give their ratio within
`(1 − η)/(1 + η)` and `(1 + η)/(1 − η)`. -/
theorem ratio_within (a b α β η : ℝ) (hα : 0 < α) (hβ : 0 < β) (hη0 : 0 ≤ η) (hη : η < 1)
    (ha : (1 - η) * α ≤ a ∧ a ≤ (1 + η) * α) (hb : (1 - η) * β ≤ b ∧ b ≤ (1 + η) * β) :
    (1 - η) / (1 + η) * (α / β) ≤ a / b ∧ a / b ≤ (1 + η) / (1 - η) * (α / β) := by
  have h1 : (0 : ℝ) < 1 - η := by linarith
  have h2 : (0 : ℝ) < 1 + η := by linarith
  have hb0 : 0 < b := lt_of_lt_of_le (mul_pos h1 hβ) hb.1
  have ha0 : 0 < a := lt_of_lt_of_le (mul_pos h1 hα) ha.1
  constructor
  · rw [div_mul_div_comm, div_le_div_iff₀ (mul_pos h2 hβ) hb0]
    calc (1 - η) * α * b ≤ (1 - η) * α * ((1 + η) * β) :=
          mul_le_mul_of_nonneg_left hb.2 (mul_pos h1 hα).le
      _ ≤ a * ((1 + η) * β) := mul_le_mul_of_nonneg_right ha.1 (mul_pos h2 hβ).le
  · rw [div_mul_div_comm, div_le_div_iff₀ hb0 (mul_pos h1 hβ)]
    calc a * ((1 - η) * β) ≤ (1 + η) * α * ((1 - η) * β) :=
          mul_le_mul_of_nonneg_right ha.2 (mul_pos h1 hβ).le
      _ ≤ (1 + η) * α * b := mul_le_mul_of_nonneg_left hb.1 (mul_pos h2 hα).le

/-- `min(a,b)/2 ≤ ab/(a+b) ≤ min(a,b)` for positive `a, b`: the integrand of the conductance of
two states against the integrand of their overlap. -/
theorem harmonic_between_min (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    min a b / 2 ≤ a * b / (a + b) ∧ a * b / (a + b) ≤ min a b := by
  have hab : 0 < a + b := by linarith
  rcases le_total a b with h | h
  · rw [min_eq_left h]
    constructor
    · rw [div_le_div_iff₀ (by norm_num) hab]; nlinarith
    · rw [div_le_iff₀ hab]; nlinarith
  · rw [min_eq_right h]
    constructor
    · rw [div_le_div_iff₀ (by norm_num) hab]; nlinarith
    · rw [div_le_iff₀ hab]; nlinarith

/-- `(Σ √(p q))² ≤ (Σ p q / m)(Σ m)` for `p, q ≥ 0` and `m > 0`: with `m` the mixture of all states
(of total mass `Σ m`), an off-diagonal conductance `Σ p q / m` of the multistate equations is at
least the squared Bhattacharyya coefficient of the pair divided by the total mass. -/
theorem sq_sum_sqrt_mul_le (p q m : X → ℝ) (hp : ∀ x, 0 ≤ p x) (hq : ∀ x, 0 ≤ q x)
    (hm : ∀ x, 0 < m x) :
    (∑ x, Real.sqrt (p x * q x)) ^ 2 ≤ (∑ x, p x * q x / m x) * ∑ x, m x := by
  have hcs := Finset.sum_mul_sq_le_sq_mul_sq (univ : Finset X)
    (fun x => Real.sqrt (p x * q x / m x)) (fun x => Real.sqrt (m x))
  have h1 : ∀ x, Real.sqrt (p x * q x / m x) * Real.sqrt (m x) = Real.sqrt (p x * q x) := by
    intro x
    rw [← Real.sqrt_mul (div_nonneg (mul_nonneg (hp x) (hq x)) (hm x).le),
      div_mul_cancel₀ _ (hm x).ne']
  have h2 : ∀ x, Real.sqrt (p x * q x / m x) ^ 2 = p x * q x / m x := fun x =>
    Real.sq_sqrt (div_nonneg (mul_nonneg (hp x) (hq x)) (hm x).le)
  have h3 : ∀ x, Real.sqrt (m x) ^ 2 = m x := fun x => Real.sq_sqrt (hm x).le
  simp only [h1, h2, h3] at hcs
  exact hcs

end BridgeOverlap

end MetricChain
