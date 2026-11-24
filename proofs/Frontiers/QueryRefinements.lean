import Mathlib
import proofs.Frontiers.QueryLowerBound

/-!
# Refinements of the query bounds (third referee)

The third independent referee (`docs/reviews/R3_referee_report.md`, Appendix A) found that one
paper statement of theory report §11.10 was false for exponentially small accuracies, that the
converse (spot-check) of Theorem 11.22 was not tight, and that the model of algorithms is
strictly larger than decision trees.  The machine-checked lemmas of that report are collected
here (the proofs are the referee's), together with the hedged spot-check for the minimum that
they make possible.

* `exists_query_ne_pair`, `prob_query_ne_pair` — **pair version of the detection principle**: for
  any two members `g₁, g₂` of the class with `|Φ g₁ - Φ g₂| > ε`, the run on an arbitrary `g` must
  query a point where `g₁` or `g₂` differs from `g` (with probability `1 - 2δ` for randomised
  algorithms).  This is strictly stronger than `exists_query_ne` / `prob_query_ne_ge` (the case
  `g₂ = g`) and is the fractional relaxation of a value certificate.
* `hedgedSpotCheck`, `hedgedSpotCheck_correct`, `hedged_window_up` — **hedged spot-check**: the
  spot-check may return any number `o` instead of `Φ g₀`; it is correct as soon as every
  alternative with `|Φ g - o| > ε / 2` is detected.  With `o = Φ g₀ + ε/2 - η` only alternatives
  that raise `Φ` by more than `ε - η` or lower it by more than `η` have to be detected, which
  removes the loss between the levels `ε` (lower bound) and `ε / 2` (unhedged spot-check).
* `min_hedgedSpotCheck_correct` — for the minimum: with the output `min (f + g₀) - ε/2 + η` it
  suffices that the samples hit every closed slack ball of radius `gap y + ε - η` and the set of
  `η`-minimisers.  With `η → 0` this is the covering relation of the lower bound
  `expected_queries_ge`: at zero temperature randomisation gains the integrality gap of the
  covering problem, up to the factor `log (1/δ)`.
* `cube_one_point_dip`, `cube_small_accuracy_randomized`, `cube_exact_randomized` — **tiny
  accuracies on the cube**: if `ε` is below the effect of a dip supported on one point, every
  randomised algorithm makes at least `(1 - 2δ) 2^n` evaluations on the zero residual.  So the
  soft-gap exponent of `cube_thermal_randomized_bound` is *not* attained for exponentially small
  accuracies: the soft gap is a relaxation of the exact dip criterion.
* `thermal_exact_dip_randomized`, `cube_exact_dip_randomized` — **the exact-dip bound**: the
  packing bound with the exact effect `log E_π exp (β (r - s)₊)` of a dip in place of its
  soft-gap relaxation `β r - softGap`.  On the cube it reduces the lower bounds of the whole
  accuracy diagram (extensive, sub-extensive and exponentially small accuracies) to two finite
  sums: the effect of the dip of radius `r` and the size of a Hamming ball.
* `Referee3.pathoAlg`, `Referee3.pathoAlg_not_a_tree` — a `QueryAlgorithm` whose query sets form a
  subcube partition that no decision tree realises: the abstract model is strictly more general
  than decision trees (which only strengthens the lower bounds).
* `Referee3.packing_factor_attained` — a genuinely randomised algorithm for which
  `expected_queries_ge_packing` holds with equality: the factor `1 - 2δ` is attained.
-/

namespace MetricChain

open Finset

/-! ### Pair version of the detection principle -/

section PairDetection

variable {X : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}

/-- deterministic pair detection -/
theorem exists_query_ne_pair (alg : QueryAlgorithm X) {ε : ℝ}
    (hcorr : ∀ g, G g → |alg.output g - Φ g| ≤ ε / 2) (g : X → ℝ) {g₁ g₂ : X → ℝ}
    (h₁ : G g₁) (h₂ : G g₂) (hΦ : ε < |Φ g₁ - Φ g₂|) :
    ∃ a ∈ alg.queries g, g₁ a ≠ g a ∨ g₂ a ≠ g a := by
  by_contra hno
  have hall₁ : ∀ a ∈ alg.queries g, g₁ a = g a := by
    intro a ha
    by_contra hne
    exact hno ⟨a, ha, Or.inl hne⟩
  have hall₂ : ∀ a ∈ alg.queries g, g₂ a = g a := by
    intro a ha
    by_contra hne
    exact hno ⟨a, ha, Or.inr hne⟩
  have ho₁ := (alg.consistent g g₁ hall₁).2
  have ho₂ := (alg.consistent g g₂ hall₂).2
  have c1 := abs_le.mp (hcorr g₁ h₁)
  have c2 := abs_le.mp (hcorr g₂ h₂)
  rw [ho₁] at c1
  rw [ho₂] at c2
  have h3 : |Φ g₁ - Φ g₂| ≤ ε := abs_le.mpr ⟨by linarith [c1.2, c2.1], by linarith [c1.1, c2.2]⟩
  linarith

variable {Ω : Type*} [Fintype Ω]

open Classical in
/-- randomised pair detection -/
theorem prob_query_ne_pair (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    (g : X → ℝ) {g₁ g₂ : X → ℝ} (h₁ : G g₁) (h₂ : G g₂) (hΦ : ε < |Φ g₁ - Φ g₂|) :
    1 - 2 * δ ≤ ∑ ω ∈ univ.filter
      (fun ω => ∃ a ∈ (alg ω).queries g, g₁ a ≠ g a ∨ g₂ a ≠ g a), P ω := by
  have hsub : univ.filter (fun ω => |(alg ω).output g₁ - Φ g₁| ≤ ε / 2) ∩
      univ.filter (fun ω => |(alg ω).output g₂ - Φ g₂| ≤ ε / 2) ⊆
        univ.filter (fun ω => ∃ a ∈ (alg ω).queries g, g₁ a ≠ g a ∨ g₂ a ≠ g a) := by
    intro ω hω
    obtain ⟨hc1, hc2⟩ := Finset.mem_inter.mp hω
    refine Finset.mem_filter.mpr ⟨mem_univ ω, ?_⟩
    by_contra hno
    have hall₁ : ∀ a ∈ (alg ω).queries g, g₁ a = g a := by
      intro a ha
      by_contra hne
      exact hno ⟨a, ha, Or.inl hne⟩
    have hall₂ : ∀ a ∈ (alg ω).queries g, g₂ a = g a := by
      intro a ha
      by_contra hne
      exact hno ⟨a, ha, Or.inr hne⟩
    have ho₁ := ((alg ω).consistent g g₁ hall₁).2
    have ho₂ := ((alg ω).consistent g g₂ hall₂).2
    have c1 := abs_le.mp (Finset.mem_filter.mp hc1).2
    have c2 := abs_le.mp (Finset.mem_filter.mp hc2).2
    rw [ho₁] at c1
    rw [ho₂] at c2
    have h3 : |Φ g₁ - Φ g₂| ≤ ε :=
      abs_le.mpr ⟨by linarith [c1.2, c2.1], by linarith [c1.1, c2.2]⟩
    linarith
  have hui := Finset.sum_union_inter
    (s₁ := univ.filter (fun ω => |(alg ω).output g₁ - Φ g₁| ≤ ε / 2))
    (s₂ := univ.filter (fun ω => |(alg ω).output g₂ - Φ g₂| ≤ ε / 2)) (f := P)
  have hunion : ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g₁ - Φ g₁| ≤ ε / 2) ∪
      univ.filter (fun ω => |(alg ω).output g₂ - Φ g₂| ≤ ε / 2), P ω ≤ 1 := by
    rw [← hP1]
    exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) fun ω _ _ => hP ω
  have e1 := hcorr g₁ h₁
  have e2 := hcorr g₂ h₂
  have hinter : 1 - 2 * δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g₁ - Φ g₁| ≤ ε / 2) ∩
      univ.filter (fun ω => |(alg ω).output g₂ - Φ g₂| ≤ ε / 2), P ω := by linarith
  exact hinter.trans (Finset.sum_le_sum_of_subset_of_nonneg hsub fun ω _ _ => hP ω)

end PairDetection

/-! ### Hedged spot-check -/

section Hedged

variable {X : Type*} [Fintype X] {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}

open Classical in
/-- Spot check of the hint `g₀` with a hedged output `o`. -/
noncomputable def hedgedSpotCheck (Φ : (X → ℝ) → ℝ) (g₀ : X → ℝ) (o : ℝ) {N : ℕ} (a : Fin N → X) :
    QueryAlgorithm X where
  queries := fun g => if ∀ k, g (a k) = g₀ (a k) then univ.image a else univ
  output := fun g => if ∀ k, g (a k) = g₀ (a k) then o else Φ g
  consistent := by
    intro g g' h
    by_cases hg : ∀ k, g (a k) = g₀ (a k)
    · simp only [if_pos hg] at h
      have hg' : ∀ k, g' (a k) = g₀ (a k) := fun k =>
        (h (a k) (Finset.mem_image_of_mem a (mem_univ k))).trans (hg k)
      simp only [if_pos hg, if_pos hg']
      exact ⟨trivial, trivial⟩
    · simp only [if_neg hg] at h
      have hgg : g' = g := funext fun x => h x (mem_univ x)
      rw [hgg]
      exact ⟨rfl, rfl⟩

open Classical in
theorem hedgedSpotCheck_card_le (Φ : (X → ℝ) → ℝ) (g₀ : X → ℝ) (o : ℝ) {N : ℕ} (a : Fin N → X) :
    ((hedgedSpotCheck Φ g₀ o a).queries g₀).card ≤ N := by
  have hq : (hedgedSpotCheck Φ g₀ o a).queries g₀ = univ.image a := by
    unfold hedgedSpotCheck
    exact if_pos fun _ => rfl
  rw [hq]
  exact Finset.card_image_le.trans (by simp)

open Classical in
/-- **The hedged spot check is sound.**  If every member `g` of the class with
`|Φ g - o| > ε / 2` differs from the hint on a set of `q`-probability at least `p`, and
`(1 - p)^N ≤ δ`, then the hedged spot check is within `ε / 2` of `Φ` with probability at least
`1 - δ` on every member of the class. -/
theorem hedgedSpotCheck_correct (g₀ : X → ℝ) (o : ℝ) (N : ℕ) (q : X → ℝ) (hq : ∀ x, 0 ≤ q x)
    (hq1 : ∑ x, q x = 1) {ε δ p : ℝ} (hε : 0 ≤ ε) (hp1 : p ≤ 1)
    (hp : ∀ g, G g → ε / 2 < |Φ g - o| → p ≤ ∑ x ∈ univ.filter (fun x => g x ≠ g₀ x), q x)
    (hN : (1 - p) ^ N ≤ δ) (g : X → ℝ) (hg : G g) :
    1 - δ ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
      |(hedgedSpotCheck Φ g₀ o a).output g - Φ g| ≤ ε / 2), ∏ k, q (a k) := by
  have hδ : 0 ≤ δ := le_trans (pow_nonneg (by linarith) N) hN
  have htot : ∑ a : Fin N → X, ∏ k, q (a k) = 1 := by
    have h := Finset.sum_pow' (univ : Finset X) q N
    rw [hq1, one_pow] at h
    rw [h]
    refine Finset.sum_congr ?_ fun _ _ => rfl
    ext a
    simp
  have hnn : ∀ a : Fin N → X, 0 ≤ ∏ k, q (a k) := fun a => Finset.prod_nonneg fun k _ => hq (a k)
  by_cases hclose : |Φ g - o| ≤ ε / 2
  · have hall : univ.filter (fun a : Fin N → X =>
        |(hedgedSpotCheck Φ g₀ o a).output g - Φ g| ≤ ε / 2) = univ := by
      apply Finset.filter_true_of_mem
      intro a _
      by_cases hag : ∀ k, g (a k) = g₀ (a k)
      · have hout : (hedgedSpotCheck Φ g₀ o a).output g = o := by
          unfold hedgedSpotCheck
          exact if_pos hag
        rw [hout, abs_sub_comm]
        exact hclose
      · have hout : (hedgedSpotCheck Φ g₀ o a).output g = Φ g := by
          unfold hedgedSpotCheck
          exact if_neg hag
        rw [hout, sub_self, abs_zero]
        linarith
    rw [hall, htot]
    linarith
  · have hfar : ε / 2 < |Φ g - o| := not_le.mp hclose
    have hpD := hp g hg hfar
    have hsplit : ∑ x ∈ univ.filter (fun x => g x ≠ g₀ x), q x +
        ∑ x ∈ univ.filter (fun x => ¬ g x ≠ g₀ x), q x = 1 := by
      rw [Finset.sum_filter_add_sum_filter_not, hq1]
    have hS0 : 0 ≤ ∑ x ∈ univ.filter (fun x => ¬ g x ≠ g₀ x), q x :=
      Finset.sum_nonneg fun x _ => hq x
    have hbad : ∑ a ∈ univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)),
        ∏ k, q (a k) = (∑ x ∈ univ.filter (fun x => ¬ g x ≠ g₀ x), q x) ^ N := by
      rw [Finset.sum_pow']
      refine Finset.sum_congr ?_ fun _ _ => rfl
      ext a
      simp
    have hbadle : ∑ a ∈ univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)),
        ∏ k, q (a k) ≤ δ := by
      rw [hbad]
      exact le_trans (pow_le_pow_left₀ hS0 (by linarith) N) hN
    have hcover : (univ : Finset (Fin N → X)) ⊆
        univ.filter (fun a : Fin N → X => |(hedgedSpotCheck Φ g₀ o a).output g - Φ g| ≤ ε / 2) ∪
          univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)) := by
      intro a _
      by_cases hag : ∀ k, g (a k) = g₀ (a k)
      · exact Finset.mem_union_right _
          (Finset.mem_filter.mpr ⟨mem_univ a, fun k => not_not.mpr (hag k)⟩)
      · refine Finset.mem_union_left _ (Finset.mem_filter.mpr ⟨mem_univ a, ?_⟩)
        have hout : (hedgedSpotCheck Φ g₀ o a).output g = Φ g := by
          unfold hedgedSpotCheck
          exact if_neg hag
        rw [hout, sub_self, abs_zero]
        linarith
    have h1 : (1 : ℝ) ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
        |(hedgedSpotCheck Φ g₀ o a).output g - Φ g| ≤ ε / 2) ∪
          univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)), ∏ k, q (a k) := by
      rw [← htot]
      exact Finset.sum_le_sum_of_subset_of_nonneg hcover fun a _ _ => hnn a
    have h2 := Finset.sum_union_inter
      (s₁ := univ.filter (fun a : Fin N → X =>
        |(hedgedSpotCheck Φ g₀ o a).output g - Φ g| ≤ ε / 2))
      (s₂ := univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)))
      (f := fun a => ∏ k, q (a k))
    have h3 : 0 ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
        |(hedgedSpotCheck Φ g₀ o a).output g - Φ g| ≤ ε / 2) ∩
          univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)), ∏ k, q (a k) :=
      Finset.sum_nonneg fun a _ => hnn a
    linarith

/-- With the output `Φ g₀ + ε/2 - η` (`0 ≤ η ≤ ε`), only alternatives that raise `Φ` by more than
`ε - η` or lower it by more than `η` have to be detected. -/
theorem hedged_window_up {ε η Φg Φg₀ : ℝ} (h : ε / 2 < |Φg - (Φg₀ + ε / 2 - η)|) :
    ε - η < Φg - Φg₀ ∨ η < Φg₀ - Φg := by
  rcases lt_abs.mp h with h1 | h1
  · left
    linarith
  · right
    linarith

end Hedged

/-! ### Hedged spot-check of the minimum -/

section MinHedged

variable {X : Type*} [Fintype X] [Nonempty X]

open Classical in
/-- **Hedged spot-check of the minimum.**  Let `g₀` be the hint, `0 ≤ η`, and `q` a probability
vector that gives probability at least `p` to every closed slack ball
`{a : s(a, y) ≤ gap y + ε - η}` and to the set of `η`-minimisers.  If `(1 - p)^N ≤ δ`, the
spot-check with `N` independent samples of `q` that returns `min (f + g₀) - ε/2 + η` when all
values agree is within `ε / 2` of `min (f + g)` with probability at least `1 - δ` on every
admissible residual: an undetected alternative has its minimum in the window
`[min (f + g₀) - (ε - η), min (f + g₀) + η]`, which lies within `ε / 2` of the output. -/
theorem min_hedgedSpotCheck_correct {d : X → X → ℝ} (f g₀ : X → ℝ) (N : ℕ) (q : X → ℝ)
    (hq : ∀ x, 0 ≤ q x) (hq1 : ∑ x, q x = 1) {ε η δ p : ℝ} (hε : 0 ≤ ε) (hp1 : p ≤ 1)
    (hball : ∀ y, p ≤ ∑ a ∈ univ.filter (fun a => slack d g₀ a y ≤
      f y + g₀ y - (univ.inf' univ_nonempty fun x => f x + g₀ x) + (ε - η)), q a)
    (hmin : p ≤ ∑ x ∈ univ.filter (fun x =>
      f x + g₀ x - (univ.inf' univ_nonempty fun x => f x + g₀ x) ≤ η), q x)
    (hN : (1 - p) ^ N ≤ δ) (g : X → ℝ) (hg : Admissible d g) :
    1 - δ ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
      |(hedgedSpotCheck (fun g => univ.inf' univ_nonempty fun x => f x + g x) g₀
          ((univ.inf' univ_nonempty fun x => f x + g₀ x) - ε / 2 + η) a).output g -
        univ.inf' univ_nonempty fun x => f x + g x| ≤ ε / 2), ∏ k, q (a k) := by
  refine hedgedSpotCheck_correct (G := Admissible d)
    (Φ := fun g => univ.inf' univ_nonempty fun x => f x + g x) g₀
    ((univ.inf' univ_nonempty fun x => f x + g₀ x) - ε / 2 + η) N q hq hq1 hε hp1
    (fun g hg hfar => ?_) hN g hg
  rcases lt_abs.mp hfar with hup | hdown
  · -- the minimum of the alternative is higher by more than `η`
    refine le_trans hmin (Finset.sum_le_sum_of_subset_of_nonneg ?_ fun x _ _ => hq x)
    intro x hx
    refine Finset.mem_filter.mpr ⟨mem_univ x, ?_⟩
    have h := higher_alternative_differs_on_minimisers f (g := g₀) (g' := g) (η := η)
      (by linarith) x (Finset.mem_filter.mp hx).2
    exact ne_of_gt h
  · -- the minimum of the alternative is lower by more than `ε - η`
    obtain ⟨y, hy⟩ := lower_alternative_differs_on_ball (d := d) f (g := g₀) (g' := g) hg
      (η := ε - η) (by linarith)
    refine le_trans (hball y) (Finset.sum_le_sum_of_subset_of_nonneg ?_ fun x _ _ => hq x)
    intro a ha
    exact Finset.mem_filter.mpr ⟨mem_univ a, ne_of_lt (hy a (Finset.mem_filter.mp ha).2)⟩

end MinHedged

/-! ### Tiny accuracies on the cube -/

section CubeSmallAccuracy

/-- distinct configurations are at Hamming-envelope distance at least `c` -/
theorem hamEnv_ge_of_ne {n : ℕ} {c : ℝ} (hc : 0 ≤ c) {x y : Fin n → Bool} (h : x ≠ y) :
    c ≤ hamEnv (fun _ : Fin n => c) x y := by
  obtain ⟨i, hi⟩ := Function.ne_iff.mp h
  unfold hamEnv
  have hnn : ∀ j ∈ (univ : Finset (Fin n)), 0 ≤ (if x j = y j then (0 : ℝ) else c) := by
    intro j _
    split_ifs
    · exact le_rfl
    · exact hc
  have hsingle := Finset.single_le_sum hnn (mem_univ i)
  rw [if_neg hi] at hsingle
  exact hsingle

/-- partition function of the zero residual with a one-point dip of depth `c` -/
theorem cube_one_point_dip (n : ℕ) {β c : ℝ} (hc : 0 ≤ c) (y : Fin n → Bool) :
    ∑ x, Real.exp (-β * ((0 : ℝ) + dip (hamEnv fun _ : Fin n => c) (fun _ => 0) y c x)) =
      2 ^ n - 1 + Real.exp (β * c) := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc
  have hterm : ∀ x : Fin n → Bool,
      Real.exp (-β * ((0 : ℝ) + 0)) *
        Real.exp (β * max 0 (c - slack (hamEnv fun _ : Fin n => c) (fun _ => 0) x y)) =
          1 + (if x = y then Real.exp (β * c) - 1 else 0) := by
    intro x
    have hs : slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) x y =
        hamEnv (fun _ : Fin n => c) x y := by
      unfold slack
      ring
    rw [hs]
    by_cases hxy : x = y
    · subst hxy
      rw [hd.self x, sub_zero, max_eq_right hc, if_pos rfl]
      simp
    · have hge := hamEnv_ge_of_ne hc hxy
      rw [if_neg hxy, max_eq_left (by linarith)]
      simp
  have h := sum_exp_dip β (hamEnv fun _ : Fin n => c) (fun _ : Fin n → Bool => (0 : ℝ))
    (fun _ => (0 : ℝ)) y c
  refine h.trans ?_
  rw [Finset.sum_congr rfl fun x _ => hterm x, Finset.sum_add_distrib, Finset.sum_ite_eq']
  simp
  ring

open Classical in
/-- **Below the effect of a one-point dip every randomised algorithm evaluates almost
everything on the zero residual of the cube class.** -/
theorem cube_small_accuracy_randomized (n : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {β c ε δ : ℝ} (hc : 0 < c)
    (hε : ε < Real.log (2 ^ n - 1 + Real.exp (β * c)) - Real.log (2 ^ n))
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ ε / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ ∑ ω, P ω * ((alg ω).queries fun _ => 0).card := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc.le
  have hadm := admissible_zero_hamEnv (n := n) (c := c) hc.le
  have hZ0 : ∑ _x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)) = (2 : ℝ) ^ n := by
    simp
  have key := expected_queries_ge_of_radius
    (Φ := fun g : (Fin n → Bool) → ℝ => Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x))))
    hd alg P hP hP1 hcorr hadm (fun _ => c)
    (fun y => by
      show ε < |Real.log (∑ x, Real.exp (-β * ((0 : ℝ) +
          dip (hamEnv fun _ : Fin n => c) (fun _ => 0) y c x))) -
        Real.log (∑ _x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)))|
      rw [cube_one_point_dip n hc.le y, hZ0]
      exact lt_of_lt_of_le hε (le_abs_self _))
    (fun _ => (1 : ℝ)) (fun _ => zero_le_one) (B := 1)
    (fun a => by
      have hsub : univ.filter (fun y : Fin n → Bool =>
          slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) a y < c) ⊆ {a} := by
        intro y hy
        have hlt := (Finset.mem_filter.mp hy).2
        have hs : slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) a y =
            hamEnv (fun _ : Fin n => c) a y := by
          unfold slack
          ring
        rw [hs] at hlt
        by_contra hne
        have hne' : a ≠ y := fun h => hne (by rw [Finset.mem_singleton]; exact h.symm)
        have := hamEnv_ge_of_ne hc.le hne'
        linarith
      calc ∑ y ∈ univ.filter (fun y : Fin n → Bool =>
            slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) a y < c), (1 : ℝ)
          ≤ ∑ y ∈ ({a} : Finset (Fin n → Bool)), (1 : ℝ) :=
            Finset.sum_le_sum_of_subset_of_nonneg hsub fun _ _ _ => zero_le_one
        _ = 1 := by simp)
  have hcard : ∑ _y : Fin n → Bool, (1 : ℝ) = (2 : ℝ) ^ n := by
    simp
  rw [hcard, mul_one] at key
  exact key

/-- In particular exact computation (`ε = 0`) needs `(1 - 2δ) 2^n` evaluations for `β, c > 0`. -/
theorem cube_exact_randomized (n : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {β c δ : ℝ} (hβ : 0 < β) (hc : 0 < c)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ (0 : ℝ) / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ ∑ ω, P ω * ((alg ω).queries fun _ => 0).card := by
  refine cube_small_accuracy_randomized n alg P hP hP1 hc ?_ hcorr
  have h1 : (1 : ℝ) < Real.exp (β * c) := Real.one_lt_exp_iff.mpr (mul_pos hβ hc)
  have h2 : (0 : ℝ) < 2 ^ n := by positivity
  have := Real.log_lt_log h2 (show (2 : ℝ) ^ n < 2 ^ n - 1 + Real.exp (β * c) by linarith)
  linarith

end CubeSmallAccuracy

/-! ### The exact-dip bound -/

section ExactDip

variable {X : Type*} [Fintype X] {Ω : Type*} [Fintype Ω]

open Classical in
/-- **Exact-dip bound for the free energy.**  A dip of depth `r y` at `y` multiplies the
partition function by `E_π exp (β (r y - s(·, y))₊)` (`sum_exp_dip`).  If the logarithm of this
factor exceeds `ε` for every `y`, a randomised algorithm that returns `log Z(f + g)` within
`ε / 2` with probability at least `1 - δ` on every admissible residual satisfies the packing bound
for the open slack balls of radii `r y`.  The soft-gap bound `thermal_expected_queries_ge` is the
relaxation `(r - s)₊ ≥ r - s` of this statement and is far from it when `exp ε - 1` is small. -/
theorem thermal_exact_dip_randomized {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {β ε δ : ℝ}
    (hcorr : ∀ g, Admissible d g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) (r : X → ℝ)
    (hr : ∀ y, ε < Real.log (∑ x, Real.exp (-β * (f x + g x)) *
        Real.exp (β * max 0 (r y - slack d g x y))) -
      Real.log (∑ x, Real.exp (-β * (f x + g x))))
    (w : X → ℝ) (hw : ∀ y, 0 ≤ w y) {B : ℝ}
    (hcap : ∀ a, ∑ y ∈ univ.filter (fun y => slack d g a y < r y), w y ≤ B) :
    (1 - 2 * δ) * ∑ y, w y ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B := by
  refine expected_queries_ge_of_radius
    (Φ := fun g => Real.log (∑ x, Real.exp (-β * (f x + g x)))) hd alg P hP hP1 hcorr hg r
    (fun y => ?_) w hw hcap
  show ε < |Real.log (∑ x, Real.exp (-β * (f x + dip d g y (r y) x))) -
      Real.log (∑ x, Real.exp (-β * (f x + g x)))|
  rw [sum_exp_dip]
  exact lt_of_lt_of_le (hr y) (le_abs_self _)

open Classical in
/-- **Exact-dip bound on the cube.**  Zero known part, envelope `c ·` Hamming distance, zero
residual.  If the dip of depth `r` changes `log Z` by more than `ε`, i.e.
`ε < log (∑_x exp (β (r - c · dist (x, y))₊)) - log 2^n`, and every open Hamming ball
`{y : c · dist (a, y) < r}` has at most `B` points, then every randomised algorithm that is
`(ε/2, δ)`-correct on the class makes at least `(1 - 2δ) 2^n / B` evaluations on the zero
residual in expectation.  With `r = c (k + 1)` the two sums are
`∑_{j ≤ k} C(n, j) (exp (β c (k + 1 - j)) - 1) + 2^n` and `|B(k)|`; all lower bounds of the accuracy
diagram of theory report §11.10 are instances. -/
theorem cube_exact_dip_randomized (n : ℕ) (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ)
    (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {β c ε δ r : ℝ} (hc : 0 ≤ c)
    (hr : ∀ y : Fin n → Bool, ε < Real.log (∑ x : Fin n → Bool,
        Real.exp (β * max 0 (r - hamEnv (fun _ : Fin n => c) x y))) - Real.log (2 ^ n))
    {B : ℝ} (hB : ∀ a : Fin n → Bool,
      ((univ.filter fun y : Fin n → Bool => hamEnv (fun _ : Fin n => c) a y < r).card : ℝ) ≤ B)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ ε / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ (∑ ω, P ω * ((alg ω).queries fun _ => 0).card) * B := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc
  have hadm := admissible_zero_hamEnv (n := n) (c := c) hc
  have hs : ∀ x y : Fin n → Bool,
      slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) x y =
        hamEnv (fun _ : Fin n => c) x y := by
    intro x y
    unfold slack
    ring
  have hZ0 : ∑ _x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)) = (2 : ℝ) ^ n := by
    simp
  have key := thermal_exact_dip_randomized hd (fun _ => (0 : ℝ)) alg P hP hP1 (β := β) hcorr
    hadm (fun _ => r)
    (fun y => by
      have hnum : ∑ x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)) *
          Real.exp (β * max 0 (r - slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) x y)) =
          ∑ x : Fin n → Bool, Real.exp (β * max 0 (r - hamEnv (fun _ : Fin n => c) x y)) := by
        refine Finset.sum_congr rfl fun x _ => ?_
        rw [hs]
        simp
      show ε < Real.log (∑ x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)) *
          Real.exp (β * max 0 (r - slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) x y))) -
        Real.log (∑ _x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)))
      rw [hnum, hZ0]
      exact hr y)
    (fun _ => (1 : ℝ)) (fun _ => zero_le_one) (B := B)
    (fun a => by
      have hcongr : (univ.filter fun y : Fin n → Bool =>
          slack (hamEnv fun _ : Fin n => c) (fun _ => (0 : ℝ)) a y < r) =
          univ.filter fun y : Fin n → Bool => hamEnv (fun _ : Fin n => c) a y < r := by
        refine Finset.filter_congr fun y _ => ?_
        rw [hs]
      rw [hcongr, Finset.sum_const, nsmul_eq_mul, mul_one]
      exact hB a)
  have hcard : ∑ _y : Fin n → Bool, (1 : ℝ) = (2 : ℝ) ^ n := by
    simp
  rw [hcard] at key
  exact key

end ExactDip

end MetricChain

/-! ### Two examples about the model -/

namespace MetricChain.Referee3

open Finset MetricChain

/-! ### (1) A consistent "algorithm" that is not a decision tree -/

/-- Subcube partition of `{0,1}^3` into `01*`, `*01`, `1*0`, `000`, `111`. -/
def pat : Bool → Bool → Bool → Finset (Fin 3)
  | false, true, _ => {0, 1}
  | _, false, true => {1, 2}
  | true, _, false => {0, 2}
  | _, _, _ => {0, 1, 2}

theorem pat_stable : ∀ b0 b1 b2 c0 c1 c2 : Bool,
    ((0 : Fin 3) ∈ pat b0 b1 b2 → c0 = b0) → ((1 : Fin 3) ∈ pat b0 b1 b2 → c1 = b1) →
    ((2 : Fin 3) ∈ pat b0 b1 b2 → c2 = b2) → pat c0 c1 c2 = pat b0 b1 b2 := by
  decide

open Classical in
/-- sign bit of a real value -/
noncomputable def sgn (g : Fin 3 → ℝ) (i : Fin 3) : Bool := decide (0 < g i)

theorem sgn_congr {g g' : Fin 3 → ℝ} {i : Fin 3} (h : g' i = g i) : sgn g' i = sgn g i := by
  unfold sgn
  rw [h]

/-- A `QueryAlgorithm` whose query sets form a subcube partition that no decision tree realises. -/
noncomputable def pathoAlg : QueryAlgorithm (Fin 3) where
  queries := fun g => pat (sgn g 0) (sgn g 1) (sgn g 2)
  output := fun _ => 0
  consistent := by
    intro g g' h
    refine ⟨?_, rfl⟩
    exact pat_stable _ _ _ _ _ _ (fun h0 => sgn_congr (h 0 h0)) (fun h1 => sgn_congr (h 1 h1))
      (fun h2 => sgn_congr (h 2 h2))

theorem pat_nonempty : ∀ b0 b1 b2 : Bool, (pat b0 b1 b2).Nonempty := by
  decide

/-- Every input is queried somewhere, but no point is queried on every input: there is no
"first query".  Hence `pathoAlg` is not the query map of any decision tree. -/
theorem pathoAlg_not_a_tree :
    (∀ g, (pathoAlg.queries g).Nonempty) ∧ ¬ ∃ a : Fin 3, ∀ g, a ∈ pathoAlg.queries g := by
  refine ⟨fun g => pat_nonempty _ _ _, ?_⟩
  rintro ⟨a, ha⟩
  have e001 : pathoAlg.queries (fun i : Fin 3 => if i = 2 then (1 : ℝ) else 0) = {1, 2} := by
    show pat (sgn _ 0) (sgn _ 1) (sgn _ 2) = _
    have s0 : sgn (fun i : Fin 3 => if i = 2 then (1 : ℝ) else 0) 0 = false := by simp [sgn]
    have s1 : sgn (fun i : Fin 3 => if i = 2 then (1 : ℝ) else 0) 1 = false := by simp [sgn]
    have s2 : sgn (fun i : Fin 3 => if i = 2 then (1 : ℝ) else 0) 2 = true := by simp [sgn]
    rw [s0, s1, s2]
    rfl
  have e100 : pathoAlg.queries (fun i : Fin 3 => if i = 0 then (1 : ℝ) else 0) = {0, 2} := by
    show pat (sgn _ 0) (sgn _ 1) (sgn _ 2) = _
    have s0 : sgn (fun i : Fin 3 => if i = 0 then (1 : ℝ) else 0) 0 = true := by simp [sgn]
    have s1 : sgn (fun i : Fin 3 => if i = 0 then (1 : ℝ) else 0) 1 = false := by simp [sgn]
    have s2 : sgn (fun i : Fin 3 => if i = 0 then (1 : ℝ) else 0) 2 = false := by simp [sgn]
    rw [s0, s1, s2]
    rfl
  have e010 : pathoAlg.queries (fun i : Fin 3 => if i = 1 then (1 : ℝ) else 0) = {0, 1} := by
    show pat (sgn _ 0) (sgn _ 1) (sgn _ 2) = _
    have s0 : sgn (fun i : Fin 3 => if i = 1 then (1 : ℝ) else 0) 0 = false := by simp [sgn]
    have s1 : sgn (fun i : Fin 3 => if i = 1 then (1 : ℝ) else 0) 1 = true := by simp [sgn]
    have s2 : sgn (fun i : Fin 3 => if i = 1 then (1 : ℝ) else 0) 2 = false := by simp [sgn]
    rw [s0, s1, s2]
    rfl
  have h1 := ha (fun i : Fin 3 => if i = 2 then (1 : ℝ) else 0)
  have h2 := ha (fun i : Fin 3 => if i = 0 then (1 : ℝ) else 0)
  have h3 := ha (fun i : Fin 3 => if i = 1 then (1 : ℝ) else 0)
  rw [e001] at h1
  rw [e100] at h2
  rw [e010] at h3
  fin_cases a <;> simp at h1 h2 h3

/-! ### (2) The factor `1 - 2δ` of the general packing bound is attained on a two-element class -/

/-- constant-output algorithm that queries nothing -/
def blind (X : Type*) (c : ℝ) : QueryAlgorithm X where
  queries := fun _ => ∅
  output := fun _ => c
  consistent := fun _ _ _ => ⟨rfl, rfl⟩

/-- the three-point mixture: full evaluation, blind guess `0`, blind guess `1` -/
noncomputable def mix3 : Fin 3 → QueryAlgorithm Unit
  | 0 => fullQueryAlgorithm (fun g => g ())
  | 1 => blind Unit 0
  | 2 => blind Unit 1

def P3 (δ : ℝ) : Fin 3 → ℝ
  | 0 => 1 - 2 * δ
  | 1 => δ
  | 2 => δ

/-- the two-element class `{0, 1}` of functions on a one-point space -/
def G2 (g : Unit → ℝ) : Prop := g = (fun _ => 0) ∨ g = (fun _ => 1)

open Classical in
/-- On the class `{0, 1}` with `Φ g = g ()` and `ε = 1/2` the mixture is correct with probability
`1 - δ` on both members, the alternative `1` is `ε`-distinguishable from `0`, and the expected
number of evaluations on `0` is exactly `1 - 2δ`: equality in `expected_queries_ge_packing`
(one alternative, weight `1`, capacity `B = 1`). -/
theorem packing_factor_attained {δ : ℝ} (hδ0 : 0 ≤ δ) (hδ : δ ≤ 1 / 2) :
    (∀ ω, 0 ≤ P3 δ ω) ∧ ∑ ω, P3 δ ω = 1 ∧
    (∀ g, G2 g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(mix3 ω).output g - g ()| ≤ (1 / 2 : ℝ) / 2),
      P3 δ ω) ∧
    (1 / 2 : ℝ) < |(fun _ : Unit => (1 : ℝ)) () - (fun _ : Unit => (0 : ℝ)) ()| ∧
    ∑ ω, P3 δ ω * ((mix3 ω).queries (fun _ => 0)).card = 1 - 2 * δ := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro ω
    fin_cases ω <;> simp [P3] <;> linarith
  · simp [Fin.sum_univ_three, P3]
    ring
  · intro g hg
    rcases hg with rfl | rfl
    · have hsub : ({0, 1} : Finset (Fin 3)) ⊆
          univ.filter (fun ω => |(mix3 ω).output (fun _ => (0 : ℝ)) - (fun _ : Unit => (0 : ℝ)) ()| ≤
            (1 / 2 : ℝ) / 2) := by
        intro ω hω
        simp only [mem_insert, mem_singleton] at hω
        rcases hω with rfl | rfl <;> simp [mix3, fullQueryAlgorithm, blind] <;> norm_num
      have hnn : ∀ ω : Fin 3, 0 ≤ P3 δ ω := by
        intro ω
        fin_cases ω <;> simp [P3] <;> linarith
      have := Finset.sum_le_sum_of_subset_of_nonneg hsub (fun ω _ _ => hnn ω)
      have e : ∑ ω ∈ ({0, 1} : Finset (Fin 3)), P3 δ ω = 1 - δ := by
        rw [Finset.sum_pair (by decide)]
        simp [P3]
        ring
      linarith
    · have hsub : ({0, 2} : Finset (Fin 3)) ⊆
          univ.filter (fun ω => |(mix3 ω).output (fun _ => (1 : ℝ)) - (fun _ : Unit => (1 : ℝ)) ()| ≤
            (1 / 2 : ℝ) / 2) := by
        intro ω hω
        simp only [mem_insert, mem_singleton] at hω
        rcases hω with rfl | rfl <;> simp [mix3, fullQueryAlgorithm, blind] <;> norm_num
      have hnn : ∀ ω : Fin 3, 0 ≤ P3 δ ω := by
        intro ω
        fin_cases ω <;> simp [P3] <;> linarith
      have := Finset.sum_le_sum_of_subset_of_nonneg hsub (fun ω _ _ => hnn ω)
      have e : ∑ ω ∈ ({0, 2} : Finset (Fin 3)), P3 δ ω = 1 - δ := by
        rw [Finset.sum_pair (by decide)]
        simp [P3]
        ring
      linarith
  · norm_num
  · simp [Fin.sum_univ_three, P3, mix3, fullQueryAlgorithm, blind]

end MetricChain.Referee3
