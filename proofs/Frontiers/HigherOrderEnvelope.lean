import Mathlib
import proofs.Frontiers.SecondOrderEnvelope

/-!
# Higher-order envelopes: the anchored expansion of order `m` with a sharp remainder

`SecondOrderEnvelope.lean` treats residuals with bounded *second* mixed differences.  This file
proves the statement for mixed differences of every order `m`: the anchored (cut-HDMR, many-body)
expansion of order `m - 1` around a reference configuration `x₀` approximates a residual `g` up
to the sum of the order-`m` envelope constants over the `m`-subsets of the changed sites, and
this bound cannot be improved.

## Objects

Sites `ι`, state spaces `σ i`, configurations `x : ∀ i, σ i`; `mixConfig x b U` is the
configuration equal to `b` on `U` and to `x` elsewhere.

* `mixedDiff g x T b = ∑_{U ⊆ T} (-1)^(|T| - |U|) · g (mixConfig x b U)` — the mixed difference
  of `g` at the base point `x` over the sites of `T`, with target states `b`.  The orders `0`,
  `1`, `2` are `mixedDiff_empty`, `mixedDiff_singleton`, `mixedDiff_pair`; the recursion over the
  sites is `mixedDiff_insert`.
* `HigherDiffBound m g c` — every mixed difference of `g` over a set `T` of `m` sites is bounded
  by `c T`, uniformly in the base point and in the target states.  For `m = 0` this is a uniform
  bound on `g`, for `m = 1` bounded single-site differences, and for `m = 2` the second-order
  envelope of `SecondOrderEnvelope.lean` (`higherDiffBound_two_of_mixedDiffBound`).
* `supp x₀ y` — the set of sites at which `y` differs from the reference `x₀`.
* `anchoredInterp m g x₀ y = ∑_{T ⊆ supp x₀ y, |T| < m} mixedDiff g x₀ T y` — the anchored
  interpolant of order `m - 1`.  It only uses the values of `g` at configurations with fewer than
  `m` changed sites.
* `higherRemainder m c x₀ y = ∑_{T ⊆ supp x₀ y, |T| = m} c T` — the remainder bound, read as a
  function of the configuration.

## Results

* `anchored_decomposition` — Möbius inversion: `g y = ∑_{T ⊆ supp x₀ y} mixedDiff g x₀ T y`.
  Hence the interpolant is exact at configurations with fewer than `m` changed sites
  (`anchoredInterp_eq_of_card_lt`).
* `higherOrder_remainder` — if `HigherDiffBound m g c`, then for every configuration `y`
  `|g y - anchoredInterp m g x₀ y| ≤ ∑_{T ⊆ supp x₀ y, |T| = m} c T`.
  `higherOrder_remainder_of_vanish` is the same bound for a function that vanishes at all
  configurations with fewer than `m` changed sites.
* `higherOrder_remainder_sharp` — for `c ≥ 0` the bound `higherRemainder m c x₀` itself vanishes
  at the configurations with fewer than `m` changed sites, has the order-`m` envelope `c`
  (`higherRemainder_higherDiffBound`) and attains the remainder bound with equality at every
  configuration.
* `higherOrder_remainder_one`, `secondOrder_remainder_of_higherOrder` — consistency with the
  lower orders: for `m = 1` the theorem is the bounded-differences estimate
  `|g y - g x₀| ≤ ∑_{j ∈ supp x₀ y} c {j}`; for `m = 2` the interpolant is the star part
  (`anchoredInterp_two`), the bound is the pairwise remainder (`sum_pairSum_powersetCard_two`,
  `pairSum_supp`), and the theorem is `secondOrder_remainder` of `SecondOrderEnvelope.lean`.
* `higherOrder_witness` — non-vacuity for `m = 3`: the three-body coupling on three binary sites.

## Proof of the remainder bound

`higherOrder_remainder_mixConfig`, by induction on `m` and, inside, on the set `S` of switched
sites.  Write `R m g S = g (mixConfig x b S) - ∑_{T ⊆ S, |T| < m} mixedDiff g x T b` and
`D_j g z = g (z[j ↦ b j]) - g z`.  For `j ∉ S`,
`R (m + 1) g (insert j S) = R (m + 1) g S + R m (D_j g) S`: the subsets of `insert j S` are the
subsets `T` of `S` and the sets `insert j T`, and
`mixedDiff g x (insert j T) b = mixedDiff (D_j g) x T b` (`mixedDiff_insert_siteDiff`).  The first
term is bounded by the inner induction hypothesis, the second by the outer one applied to `D_j g`
with the constants `T ↦ c (insert j T)`, and the two bounds add up to the sum of `c` over the
`(m + 1)`-subsets of `insert j S` (`sum_powersetCard_succ_insert`).

## Proof of sharpness

`higherRemainder_higherDiffBound`, by induction on `m`: changing the state of the site `j`
changes `higherRemainder (m + 1) c x₀` by a difference of two indicators times the order-`m`
remainder function with the constants `T ↦ c (insert j T)` on the sets `T ∌ j`
(`higherRemainder_update_sub`), and the indicator factor does not depend on the other sites
(`mixedDiff_mul_left`).
-/

namespace MetricChain

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-! ### Mixed differences, envelopes of order `m`, the anchored interpolant -/

/-- **Mixed difference** of `g` at the base point `x` over the sites of `T` with target states
`b`: the alternating sum of the values of `g` at the configurations obtained from `x` by
switching the sites of a subset `U ⊆ T` to their target states. -/
def mixedDiff [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x : ∀ i, σ i) (T : Finset ι)
    (b : ∀ i, σ i) : ℝ :=
  ∑ U ∈ T.powerset, (-1 : ℝ) ^ (T.card - U.card) * g (mixConfig x b U)

/-- **Envelope of order `m`.**  Every mixed difference of `g` over a set `T` of `m` sites is
bounded by `c T`, uniformly in the base point `x` and in the target states `b`. -/
def HigherDiffBound [DecidableEq ι] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) : Prop :=
  ∀ (x b : ∀ i, σ i) (T : Finset ι), T.card = m → |mixedDiff g x T b| ≤ c T

/-- The changed sites: the set of sites at which `y` differs from the reference `x₀`. -/
def supp [Fintype ι] [∀ i, DecidableEq (σ i)] (x₀ y : ∀ i, σ i) : Finset ι :=
  univ.filter fun i => y i ≠ x₀ i

/-- **Anchored interpolant of order `m - 1`**: the sum of the mixed differences of `g` at the
reference `x₀` over the sets of fewer than `m` changed sites.  Only the values of `g` at
configurations with fewer than `m` changed sites enter. -/
def anchoredInterp [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ)
    (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) : ℝ :=
  ∑ T ∈ (supp x₀ y).powerset.filter (fun T => T.card < m), mixedDiff g x₀ T y

/-- A site is changed iff its state differs from the reference state. -/
theorem mem_supp [Fintype ι] [∀ i, DecidableEq (σ i)] {x₀ y : ∀ i, σ i} {i : ι} :
    i ∈ supp x₀ y ↔ y i ≠ x₀ i := by
  simp [supp]

/-- Switching the base point at one site commutes with switching a set of sites. -/
theorem mixConfig_update_base [DecidableEq ι] (x b : ∀ i, σ i) (U : Finset ι) (j : ι) :
    mixConfig (Function.update x j (b j)) b U = Function.update (mixConfig x b U) j (b j) := by
  funext i
  by_cases hij : i = j
  · subst hij
    simp [mixConfig]
  · simp [mixConfig, hij]

/-- Outside the switched set the base point is kept. -/
theorem mixConfig_apply_of_notMem [DecidableEq ι] (x b : ∀ i, σ i) {U : Finset ι} {j : ι}
    (hj : j ∉ U) : mixConfig x b U j = x j := by
  simp [mixConfig, hj]

/-- Switching exactly the changed sites of `y` turns the reference into `y`. -/
theorem mixConfig_supp [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (x₀ y : ∀ i, σ i) : mixConfig x₀ y (supp x₀ y) = y := by
  funext i
  by_cases h : y i = x₀ i
  · simp [mixConfig, supp, h]
  · simp [mixConfig, supp, h]

/-- The changed sites of a partially switched configuration lie in the switched set. -/
theorem supp_mixConfig_subset [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (x₀ y : ∀ i, σ i) (U : Finset ι) : supp x₀ (mixConfig x₀ y U) ⊆ U := by
  intro i hi
  by_contra hiU
  exact mem_supp.mp hi (mixConfig_apply_of_notMem x₀ y hiU)

/-! ### The first orders and the recursion over the sites -/

/-- Sign bookkeeping: enlarging the outer set by one site flips the sign. -/
theorem neg_one_pow_succ_sub {a b : ℕ} (h : b ≤ a) :
    (-1 : ℝ) ^ (a + 1 - b) = -(-1 : ℝ) ^ (a - b) := by
  have e : a + 1 - b = (a - b) + 1 := by omega
  rw [e, pow_succ]
  ring

/-- Order `0`: the mixed difference over the empty set is the value at the base point. -/
theorem mixedDiff_empty [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x b : ∀ i, σ i) :
    mixedDiff g x ∅ b = g x := by
  simp [mixedDiff, mixConfig_empty]

/-- **Recursion over the sites.**  The mixed difference over `insert j T` is the difference of
the mixed differences over `T` at the base point with the site `j` switched and at the base
point itself. -/
theorem mixedDiff_insert [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x b : ∀ i, σ i) {j : ι}
    {T : Finset ι} (hj : j ∉ T) :
    mixedDiff g x (insert j T) b =
      mixedDiff g (Function.update x j (b j)) T b - mixedDiff g x T b := by
  unfold mixedDiff
  rw [Finset.sum_powerset_insert hj, Finset.card_insert_of_notMem hj]
  have h1 : ∑ U ∈ T.powerset, (-1 : ℝ) ^ (T.card + 1 - U.card) * g (mixConfig x b U) =
      -∑ U ∈ T.powerset, (-1 : ℝ) ^ (T.card - U.card) * g (mixConfig x b U) := by
    rw [← Finset.sum_neg_distrib]
    refine Finset.sum_congr rfl fun U hU => ?_
    rw [neg_one_pow_succ_sub (Finset.card_le_card (Finset.mem_powerset.mp hU))]
    ring
  have h2 : ∑ U ∈ T.powerset,
      (-1 : ℝ) ^ (T.card + 1 - (insert j U).card) * g (mixConfig x b (insert j U)) =
      ∑ U ∈ T.powerset,
        (-1 : ℝ) ^ (T.card - U.card) * g (mixConfig (Function.update x j (b j)) b U) := by
    refine Finset.sum_congr rfl fun U hU => ?_
    have hjU : j ∉ U := fun h => hj (Finset.mem_powerset.mp hU h)
    rw [Finset.card_insert_of_notMem hjU, Nat.add_sub_add_right, mixConfig_update_base,
      mixConfig_insert]
  rw [h1, h2]
  ring

/-- Order `1`: the mixed difference over one site is the single-site difference. -/
theorem mixedDiff_singleton [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x b : ∀ i, σ i) (j : ι) :
    mixedDiff g x {j} b = g (Function.update x j (b j)) - g x := by
  have h := mixedDiff_insert g x b (Finset.notMem_empty j)
  rw [mixedDiff_empty, mixedDiff_empty] at h
  simpa using h

/-- Order `2`: the mixed difference over two distinct sites is the mixed second difference of
`SecondOrderEnvelope.lean`. -/
theorem mixedDiff_pair [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x b : ∀ i, σ i) {i j : ι}
    (hij : i ≠ j) :
    mixedDiff g x {i, j} b =
      g (Function.update (Function.update x i (b i)) j (b j)) - g (Function.update x i (b i)) -
        g (Function.update x j (b j)) + g x := by
  rw [mixedDiff_insert g x b (Finset.notMem_singleton.mpr hij), mixedDiff_singleton,
    mixedDiff_singleton]
  ring

/-- The mixed difference of a single-site difference `z ↦ g (z[j ↦ b j]) - g z` is the difference
of the mixed differences of `g` at the two base points. -/
theorem mixedDiff_siteDiff [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x b : ∀ i, σ i) (j : ι)
    (T : Finset ι) :
    mixedDiff (fun z => g (Function.update z j (b j)) - g z) x T b =
      mixedDiff g (Function.update x j (b j)) T b - mixedDiff g x T b := by
  unfold mixedDiff
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun U _ => ?_
  rw [mixConfig_update_base]
  ring

/-- **Recursion, difference-operator form.**  The mixed difference of `g` over `insert j T` is
the mixed difference over `T` of the single-site difference of `g` at the site `j`. -/
theorem mixedDiff_insert_siteDiff [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x b : ∀ i, σ i)
    {j : ι} {T : Finset ι} (hj : j ∉ T) :
    mixedDiff g x (insert j T) b =
      mixedDiff (fun z => g (Function.update z j (b j)) - g z) x T b := by
  rw [mixedDiff_insert g x b hj, mixedDiff_siteDiff]

/-! ### Möbius inversion: the anchored decomposition is exact -/

/-- Möbius inversion at an arbitrary base point: the mixed differences over all subsets of `S`
add up to the value at the configuration with the sites of `S` switched. -/
theorem sum_mixedDiff_powerset [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (b : ∀ i, σ i)
    (S : Finset ι) : ∀ x, ∑ T ∈ S.powerset, mixedDiff g x T b = g (mixConfig x b S) := by
  induction S using Finset.induction_on with
  | empty =>
    intro x
    simp [mixedDiff_empty, mixConfig_empty]
  | insert j S hj ih =>
    intro x
    rw [Finset.sum_powerset_insert hj]
    have h : ∑ T ∈ S.powerset, mixedDiff g x (insert j T) b =
        ∑ T ∈ S.powerset,
          (mixedDiff g (Function.update x j (b j)) T b - mixedDiff g x T b) :=
      Finset.sum_congr rfl fun T hT =>
        mixedDiff_insert g x b fun h => hj (Finset.mem_powerset.mp hT h)
    rw [h, Finset.sum_sub_distrib, ih x, ih (Function.update x j (b j)), mixConfig_update_base,
      mixConfig_insert]
    ring

/-- **Möbius inversion (exactness of the anchored decomposition).**  Every function is the sum of
its mixed differences at the reference configuration over all sets of changed sites. -/
theorem anchored_decomposition [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    g y = ∑ T ∈ (supp x₀ y).powerset, mixedDiff g x₀ T y := by
  rw [sum_mixedDiff_powerset, mixConfig_supp]

/-- The anchored interpolant of order `m - 1` is exact at every configuration with fewer than
`m` changed sites. -/
theorem anchoredInterp_eq_of_card_lt [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) (h : (supp x₀ y).card < m) :
    anchoredInterp m g x₀ y = g y := by
  unfold anchoredInterp
  rw [Finset.filter_true_of_mem, ← anchored_decomposition]
  intro T hT
  exact lt_of_le_of_lt (Finset.card_le_card (Finset.mem_powerset.mp hT)) h

/-- The interpolant of a function that vanishes at all configurations with fewer than `m`
changed sites is zero. -/
theorem anchoredInterp_eq_zero_of_vanish [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (h : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i)
    (hv : ∀ z, (supp x₀ z).card < m → h z = 0) (y : ∀ i, σ i) :
    anchoredInterp m h x₀ y = 0 := by
  unfold anchoredInterp
  apply Finset.sum_eq_zero
  intro T hT
  rw [Finset.mem_filter] at hT
  unfold mixedDiff
  apply Finset.sum_eq_zero
  intro U hU
  have hlt : (supp x₀ (mixConfig x₀ y U)).card < m :=
    lt_of_le_of_lt (Finset.card_le_card
      ((supp_mixConfig_subset x₀ y U).trans (Finset.mem_powerset.mp hU))) hT.2
  rw [hv _ hlt, mul_zero]

/-! ### The remainder theorem of order `m` -/

/-- A sum over the subsets of `insert j S` whose cardinality has a property `p`: the subsets `T`
of `S`, and the sets `insert j T`. -/
theorem sum_powerset_insert_filter_card {α : Type*} [DecidableEq α] (p : ℕ → Prop)
    [DecidablePred p] (f : Finset α → ℝ) {j : α} {S : Finset α} (hj : j ∉ S) :
    ∑ T ∈ (insert j S).powerset.filter (fun T => p T.card), f T =
      ∑ T ∈ S.powerset.filter (fun T => p T.card), f T +
        ∑ T ∈ S.powerset.filter (fun T => p (T.card + 1)), f (insert j T) := by
  rw [Finset.sum_filter, Finset.sum_filter, Finset.sum_filter, Finset.sum_powerset_insert hj]
  congr 1
  refine Finset.sum_congr rfl fun T hT => ?_
  rw [Finset.card_insert_of_notMem fun h => hj (Finset.mem_powerset.mp hT h)]

/-- A sum over the `(m + 1)`-subsets of `insert j S`: the `(m + 1)`-subsets of `S`, and the sets
`insert j T` for the `m`-subsets `T` of `S`. -/
theorem sum_powersetCard_succ_insert {α : Type*} [DecidableEq α] (f : Finset α → ℝ) (m : ℕ)
    {j : α} {S : Finset α} (hj : j ∉ S) :
    ∑ T ∈ (insert j S).powersetCard (m + 1), f T =
      ∑ T ∈ S.powersetCard (m + 1), f T + ∑ T ∈ S.powersetCard m, f (insert j T) := by
  simp only [Finset.powersetCard_eq_filter]
  rw [sum_powerset_insert_filter_card (fun n => n = m + 1) f hj]
  simp only [Nat.add_right_cancel_iff]

/-- **Remainder bound after switching the sites of `S`.**  If the mixed differences of `g` with
target states `b` over the `m`-subsets `T` of `S` are bounded by `c T` at every base point, then
the sum of the mixed differences at `x` over the subsets of `S` with fewer than `m` sites
approximates `g (mixConfig x b S)` up to the sum of `c` over the `m`-subsets of `S`. -/
theorem higherOrder_remainder_mixConfig [DecidableEq ι] (b : ∀ i, σ i) :
    ∀ (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (S : Finset ι),
      (∀ T, T ⊆ S → T.card = m → ∀ x, |mixedDiff g x T b| ≤ c T) →
      ∀ x, |g (mixConfig x b S) -
          ∑ T ∈ S.powerset.filter (fun T => T.card < m), mixedDiff g x T b| ≤
        ∑ T ∈ S.powersetCard m, c T := by
  intro m
  induction m with
  | zero =>
    intro g c S h x
    have h0 := h ∅ (Finset.empty_subset S) rfl (mixConfig x b S)
    rw [mixedDiff_empty] at h0
    simpa using h0
  | succ m ih =>
    intro g c S
    induction S using Finset.induction_on with
    | empty =>
      intro _ x
      have hfilter : (∅ : Finset ι).powerset.filter (fun T => T.card < m + 1) = {∅} := by
        rw [Finset.powerset_empty, Finset.filter_true_of_mem]
        intro T hT
        rw [Finset.mem_singleton.mp hT]
        simp
      have hcard : (∅ : Finset ι).powersetCard (m + 1) = ∅ :=
        Finset.powersetCard_eq_empty.mpr (by simp)
      rw [hfilter, hcard, Finset.sum_singleton, Finset.sum_empty, mixedDiff_empty,
        mixConfig_empty, sub_self, abs_zero]
    | insert j S hj ihS =>
      intro h x
      have hS : ∀ T, T ⊆ S → T.card = m + 1 → ∀ x, |mixedDiff g x T b| ≤ c T :=
        fun T hT hc x => h T (hT.trans (Finset.subset_insert j S)) hc x
      have e1 := abs_le.mp (ihS hS x)
      have hk : ∀ T, T ⊆ S → T.card = m →
          ∀ x, |mixedDiff (fun z => g (Function.update z j (b j)) - g z) x T b| ≤
            c (insert j T) := by
        intro T hT hc x
        have hjT : j ∉ T := fun hmem => hj (hT hmem)
        rw [← mixedDiff_insert_siteDiff g x b hjT]
        exact h (insert j T) (Finset.insert_subset_insert j hT)
          (by rw [Finset.card_insert_of_notMem hjT, hc]) x
      have e2 := abs_le.mp (ih (fun z => g (Function.update z j (b j)) - g z)
        (fun T => c (insert j T)) S hk x)
      have hsum : ∑ T ∈ (insert j S).powerset.filter (fun T => T.card < m + 1),
          mixedDiff g x T b =
          ∑ T ∈ S.powerset.filter (fun T => T.card < m + 1), mixedDiff g x T b +
            ∑ T ∈ S.powerset.filter (fun T => T.card < m),
              mixedDiff (fun z => g (Function.update z j (b j)) - g z) x T b := by
        rw [sum_powerset_insert_filter_card (fun n => n < m + 1) _ hj]
        simp only [Nat.add_lt_add_iff_right]
        congr 1
        refine Finset.sum_congr rfl fun T hT => ?_
        exact mixedDiff_insert_siteDiff g x b fun hmem =>
          hj (Finset.mem_powerset.mp (Finset.mem_filter.mp hT).1 hmem)
      rw [hsum, sum_powersetCard_succ_insert c m hj, mixConfig_insert]
      exact abs_le.mpr ⟨by linarith [e1.1, e2.1], by linarith [e1.2, e2.2]⟩

/-- **Remainder theorem of order `m`.**  If every mixed difference of `g` over `m` sites is
bounded by the constant of its set of sites, the anchored interpolant of order `m - 1` around
any reference configuration `x₀` — which only uses the values of `g` at configurations with
fewer than `m` changed sites — approximates `g` at `y` up to the sum of the constants over the
`m`-subsets of the changed sites of `y`. -/
theorem higherOrder_remainder [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ)
    (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (hg : HigherDiffBound m g c) (x₀ y : ∀ i, σ i) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ T ∈ (supp x₀ y).powersetCard m, c T := by
  have h := higherOrder_remainder_mixConfig y m g c (supp x₀ y)
    (fun T _ hT x => hg x y T hT) x₀
  rw [mixConfig_supp] at h
  exact h

/-- **Remainder theorem, vanishing form.**  A function with the order-`m` envelope `c` that
vanishes at every configuration with fewer than `m` changed sites is bounded at `y` by the sum of
the constants over the `m`-subsets of the changed sites of `y`. -/
theorem higherOrder_remainder_of_vanish [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (h : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (hh : HigherDiffBound m h c)
    (x₀ : ∀ i, σ i) (hv : ∀ z, (supp x₀ z).card < m → h z = 0) (y : ∀ i, σ i) :
    |h y| ≤ ∑ T ∈ (supp x₀ y).powersetCard m, c T := by
  have e := higherOrder_remainder m h c hh x₀ y
  rwa [anchoredInterp_eq_zero_of_vanish m h x₀ hv y, sub_zero] at e

/-! ### Sharpness: the remainder bound has the envelope `c` and attains itself -/

/-- **The remainder bound as a function of the configuration**: the sum of the constants over
the `m`-subsets of the changed sites. -/
def higherRemainder [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ)
    (c : Finset ι → ℝ) (x₀ y : ∀ i, σ i) : ℝ :=
  ∑ T ∈ (supp x₀ y).powersetCard m, c T

/-- The remainder function vanishes at configurations with fewer than `m` changed sites. -/
theorem higherRemainder_eq_zero_of_card_lt [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (c : Finset ι → ℝ) (x₀ y : ∀ i, σ i) (h : (supp x₀ y).card < m) :
    higherRemainder m c x₀ y = 0 := by
  unfold higherRemainder
  rw [Finset.powersetCard_eq_empty.mpr h, Finset.sum_empty]

/-- A sum over the `(m + 1)`-subsets of `R`, split according to the membership of `j`. -/
theorem sum_powersetCard_succ_erase {α : Type*} [DecidableEq α] (f : Finset α → ℝ) (m : ℕ)
    (j : α) (R : Finset α) :
    ∑ T ∈ R.powersetCard (m + 1), f T = ∑ T ∈ (R.erase j).powersetCard (m + 1), f T +
      (if j ∈ R then 1 else 0) * ∑ T ∈ (R.erase j).powersetCard m, f (insert j T) := by
  by_cases h : j ∈ R
  · rw [if_pos h, one_mul, ← sum_powersetCard_succ_insert f m (Finset.notMem_erase j R),
      Finset.insert_erase h]
  · rw [if_neg h, zero_mul, add_zero, Finset.erase_eq_of_notMem h]

/-- The `m`-subsets of `R` that avoid `j` are the `m`-subsets of `R.erase j`: the other ones can
be removed from a sum by an indicator. -/
theorem sum_powersetCard_erase_insert {α : Type*} [DecidableEq α] (f : Finset α → ℝ) (m : ℕ)
    (j : α) (R : Finset α) :
    ∑ T ∈ (R.erase j).powersetCard m, f (insert j T) =
      ∑ T ∈ R.powersetCard m, (if j ∈ T then 0 else f (insert j T)) := by
  rw [← Finset.sum_subset (Finset.powersetCard_mono (Finset.erase_subset j R))]
  · refine Finset.sum_congr rfl fun T hT => ?_
    have hjT : j ∉ T := fun h => Finset.notMem_erase j R ((Finset.mem_powersetCard.mp hT).1 h)
    rw [if_neg hjT]
  · intro T hT hT'
    by_cases hjT : j ∈ T
    · rw [if_pos hjT]
    · exfalso
      apply hT'
      rw [Finset.mem_powersetCard] at hT ⊢
      exact ⟨fun i hi => Finset.mem_erase.mpr ⟨fun h => hjT (h ▸ hi), hT.1 hi⟩, hT.2⟩

/-- Updating the site `j` does not change the changed sites other than `j`. -/
theorem supp_update_erase [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (x₀ z : ∀ i, σ i) (j : ι) (s : σ j) :
    (supp x₀ (Function.update z j s)).erase j = (supp x₀ z).erase j := by
  ext i
  by_cases hij : i = j
  · simp [hij]
  · simp [mem_supp, hij]

/-- The indicator of a changed site is the function `changed` of `SecondOrderEnvelope.lean`. -/
theorem ite_mem_supp [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (x₀ z : ∀ i, σ i)
    (j : ι) : (if j ∈ supp x₀ z then (1 : ℝ) else 0) = changed x₀ z j := by
  simp [changed, mem_supp]

/-- **Single-site difference of the remainder function.**  Changing the state of the site `j`
changes the order-`(m + 1)` remainder function by the change of the indicator of `j` times the
order-`m` remainder function with the constants `T ↦ c (insert j T)` on the sets `T ∌ j`. -/
theorem higherRemainder_update_sub [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (c : Finset ι → ℝ) (x₀ z : ∀ i, σ i) (j : ι) (s : σ j) :
    higherRemainder (m + 1) c x₀ (Function.update z j s) - higherRemainder (m + 1) c x₀ z =
      (changed x₀ (Function.update z j s) j - changed x₀ z j) *
        higherRemainder m (fun T => if j ∈ T then 0 else c (insert j T)) x₀ z := by
  unfold higherRemainder
  rw [sum_powersetCard_succ_erase c m j (supp x₀ (Function.update z j s)),
    sum_powersetCard_succ_erase c m j (supp x₀ z), supp_update_erase, ite_mem_supp,
    ite_mem_supp, ← sum_powersetCard_erase_insert c m j (supp x₀ z)]
  ring

/-- A factor that takes the same value at all the configurations entering a mixed difference
can be pulled out of it. -/
theorem mixedDiff_mul_left [DecidableEq ι] (ψ f : (∀ i, σ i) → ℝ) (x b : ∀ i, σ i)
    (T : Finset ι) (hψ : ∀ U, U ⊆ T → ψ (mixConfig x b U) = ψ x) :
    mixedDiff (fun z => ψ z * f z) x T b = ψ x * mixedDiff f x T b := by
  unfold mixedDiff
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun U hU => ?_
  dsimp only
  rw [hψ U (Finset.mem_powerset.mp hU)]
  ring

/-- **The remainder function has the order-`m` envelope `c`** (for nonnegative constants): its
mixed difference over a set `T` of `m` sites is `c T` times a product of differences of
indicators. -/
theorem higherRemainder_higherDiffBound [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (x₀ : ∀ i, σ i) : ∀ (m : ℕ) (c : Finset ι → ℝ), (∀ T, 0 ≤ c T) →
      HigherDiffBound m (higherRemainder m c x₀) c := by
  intro m
  induction m with
  | zero =>
    intro c hc x b T hT
    rw [Finset.card_eq_zero.mp hT, mixedDiff_empty]
    simp [higherRemainder, abs_of_nonneg (hc ∅)]
  | succ m ih =>
    intro c hc x b T hT
    obtain ⟨j, hjT⟩ : T.Nonempty := Finset.card_pos.mp (by omega)
    have hjT₀ : j ∉ T.erase j := Finset.notMem_erase j T
    have hcard : (T.erase j).card = m := by
      rw [Finset.card_erase_of_mem hjT, hT]
      rfl
    have hc' : ∀ T', 0 ≤ (fun T' => if j ∈ T' then (0 : ℝ) else c (insert j T')) T' := by
      intro T'
      dsimp only
      split_ifs
      · exact le_rfl
      · exact hc _
    have hfun : (fun z => higherRemainder (m + 1) c x₀ (Function.update z j (b j)) -
        higherRemainder (m + 1) c x₀ z) = fun z => (changed x₀ b j - changed x₀ z j) *
        higherRemainder m (fun T' => if j ∈ T' then 0 else c (insert j T')) x₀ z := by
      funext z
      rw [higherRemainder_update_sub]
      simp [changed]
    have hψ : ∀ U, U ⊆ T.erase j →
        changed x₀ b j - changed x₀ (mixConfig x b U) j = changed x₀ b j - changed x₀ x j := by
      intro U hU
      have hjU : j ∉ U := fun h => hjT₀ (hU h)
      simp [changed, mixConfig_apply_of_notMem x b hjU]
    have hfac : |changed x₀ b j - changed x₀ x j| ≤ 1 := by
      unfold changed
      split_ifs <;> norm_num
    have hrec := ih _ hc' x b (T.erase j) hcard
    rw [if_neg hjT₀, Finset.insert_erase hjT] at hrec
    rw [← Finset.insert_erase hjT, mixedDiff_insert_siteDiff _ x b hjT₀, hfun,
      mixedDiff_mul_left (fun z => changed x₀ b j - changed x₀ z j) _ x b (T.erase j) hψ,
      abs_mul, Finset.insert_erase hjT]
    calc |changed x₀ b j - changed x₀ x j| *
          |mixedDiff (higherRemainder m (fun T' => if j ∈ T' then 0 else c (insert j T')) x₀)
            x (T.erase j) b| ≤ 1 * c T :=
          mul_le_mul hfac hrec (abs_nonneg _) zero_le_one
      _ = c T := one_mul _

/-- **Sharpness of the remainder theorem.**  For nonnegative constants the remainder bound
`higherRemainder m c x₀` (i) vanishes at every configuration with fewer than `m` changed sites,
(ii) has the order-`m` envelope `c`, and (iii) attains the bound of `higherOrder_remainder` with
equality at every configuration.  So the bound cannot be improved for any `m`, any constants and
any configuration. -/
theorem higherOrder_remainder_sharp [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (c : Finset ι → ℝ) (hc : ∀ T, 0 ≤ c T) (x₀ : ∀ i, σ i) :
    (∀ y, (supp x₀ y).card < m → higherRemainder m c x₀ y = 0) ∧
      HigherDiffBound m (higherRemainder m c x₀) c ∧
      ∀ y, |higherRemainder m c x₀ y - anchoredInterp m (higherRemainder m c x₀) x₀ y| =
        ∑ T ∈ (supp x₀ y).powersetCard m, c T := by
  refine ⟨fun y h => higherRemainder_eq_zero_of_card_lt m c x₀ y h,
    higherRemainder_higherDiffBound x₀ m c hc, fun y => ?_⟩
  rw [anchoredInterp_eq_zero_of_vanish m _ x₀
    (fun z h => higherRemainder_eq_zero_of_card_lt m c x₀ z h) y, sub_zero]
  exact abs_of_nonneg (Finset.sum_nonneg fun T _ => hc T)

/-! ### Consistency with the lower orders

For `m = 1` the interpolant is the reference value and the remainder theorem is the
bounded-differences estimate.  For `m = 2` the interpolant is the star part of
`SecondOrderEnvelope.lean`, the sum of the pair constants over the `2`-subsets of the changed
sites is the pairwise remainder, and `higherOrder_remainder` specialises to
`secondOrder_remainder`. -/

/-- Raising the order of the interpolant by one adds the mixed differences over the `m`-subsets
of the changed sites. -/
theorem anchoredInterp_succ [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ)
    (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    anchoredInterp (m + 1) g x₀ y =
      anchoredInterp m g x₀ y + ∑ T ∈ (supp x₀ y).powersetCard m, mixedDiff g x₀ T y := by
  unfold anchoredInterp
  rw [Finset.powersetCard_eq_filter, Finset.sum_filter, Finset.sum_filter, Finset.sum_filter,
    ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun T _ => ?_
  rcases Nat.lt_trichotomy T.card m with h | h | h
  · have h2 : T.card < m + 1 := by omega
    have h3 : ¬ T.card = m := by omega
    rw [if_pos h, if_pos h2, if_neg h3, add_zero]
  · have h1 : ¬ T.card < m := by omega
    have h2 : T.card < m + 1 := by omega
    rw [if_neg h1, if_pos h2, if_pos h, zero_add]
  · have h1 : ¬ T.card < m := by omega
    have h2 : ¬ T.card < m + 1 := by omega
    have h3 : ¬ T.card = m := by omega
    rw [if_neg h1, if_neg h2, if_neg h3, add_zero]

/-- With `m = 0` the interpolant has no terms. -/
theorem anchoredInterp_zero [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) : anchoredInterp 0 g x₀ y = 0 := by
  simp [anchoredInterp]

/-- With `m = 1` the interpolant is the reference value. -/
theorem anchoredInterp_one [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) : anchoredInterp 1 g x₀ y = g x₀ := by
  rw [anchoredInterp_succ, anchoredInterp_zero, Finset.powersetCard_zero, Finset.sum_singleton,
    mixedDiff_empty, zero_add]

/-- With `m = 2` the interpolant is the star part (order-one expansion) of
`SecondOrderEnvelope.lean`. -/
theorem anchoredInterp_two [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) : anchoredInterp 2 g x₀ y = starPart g x₀ y := by
  rw [anchoredInterp_succ, anchoredInterp_one, Finset.powersetCard_one, Finset.sum_map]
  unfold starPart
  congr 1
  rw [← Finset.sum_subset (Finset.subset_univ (supp x₀ y))]
  · exact Finset.sum_congr rfl fun i _ => mixedDiff_singleton g x₀ y i
  · intro i _ hi
    have hy : y i = x₀ i := by
      by_contra h
      exact hi (mem_supp.mpr h)
    rw [hy, Function.update_eq_self, sub_self]

/-- **Order one: bounded differences.**  If every single-site difference at a site `j` is
bounded by `c {j}`, the value of `g` at `y` differs from the reference value by at most the sum
of the constants of the changed sites. -/
theorem higherOrder_remainder_one [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (hg : HigherDiffBound 1 g c) (x₀ y : ∀ i, σ i) :
    |g y - g x₀| ≤ ∑ j ∈ supp x₀ y, c {j} := by
  have h := higherOrder_remainder 1 g c hg x₀ y
  rw [anchoredInterp_one, Finset.powersetCard_one, Finset.sum_map] at h
  exact h

/-- **Order two is the second-order envelope.**  A residual with the second-order envelope
`c : ι → ι → ℝ` of `SecondOrderEnvelope.lean` has the order-`2` envelope `c'` whenever
`c i j ≤ c' {i, j}` for all pairs of distinct sites (for symmetric `c`: `c' {i, j} = c i j`). -/
theorem higherDiffBound_two_of_mixedDiffBound [DecidableEq ι] (g : (∀ i, σ i) → ℝ)
    (c : ι → ι → ℝ) (c' : Finset ι → ℝ) (hc' : ∀ i j, i ≠ j → c i j ≤ c' {i, j})
    (hg : MixedDiffBound g c) : HigherDiffBound 2 g c' := by
  intro x b T hT
  obtain ⟨i, j, hij, rfl⟩ := Finset.card_eq_two.mp hT
  rw [mixedDiff_pair g x b hij]
  exact le_trans (hg x i j hij (b i) (b j)) (hc' i j hij)

/-- **Pair constant of a set of sites**: half the sum of `c i k` over the ordered pairs of
distinct sites of `T`.  For a pair `{i, j}` it is the mean of `c i j` and `c j i`. -/
noncomputable def pairSum [DecidableEq ι] (c : ι → ι → ℝ) (T : Finset ι) : ℝ :=
  (1 / 2) * ∑ i ∈ T, ∑ k ∈ T.erase i, c i k

/-- Adding a site `j` to a set adds the pair constants of the pairs `{j, i}`. -/
theorem pairSum_insert [DecidableEq ι] (c : ι → ι → ℝ) {j : ι} {S : Finset ι} (hj : j ∉ S) :
    pairSum c (insert j S) = pairSum c S + (1 / 2) * ∑ i ∈ S, (c j i + c i j) := by
  unfold pairSum
  rw [sum_insert_erase_pairs (fun i k => c i k) hj, Finset.sum_add_distrib]
  ring

/-- The pair constant of a pair of distinct sites is the mean of the two table entries. -/
theorem pairSum_pair [DecidableEq ι] (c : ι → ι → ℝ) {i j : ι} (hij : i ≠ j) :
    pairSum c {i, j} = (c i j + c j i) / 2 := by
  rw [pairSum_insert c (Finset.notMem_singleton.mpr hij)]
  simp [pairSum]
  ring

/-- The pair constants of the `2`-subsets of `S` add up to the pair constant of `S`. -/
theorem sum_pairSum_powersetCard_two [DecidableEq ι] (c : ι → ι → ℝ) (S : Finset ι) :
    ∑ T ∈ S.powersetCard 2, pairSum c T = pairSum c S := by
  induction S using Finset.induction_on with
  | empty =>
    have h0 : (∅ : Finset ι).powersetCard 2 = ∅ := Finset.powersetCard_eq_empty.mpr (by simp)
    rw [h0, Finset.sum_empty]
    simp [pairSum]
  | insert j S hj ih =>
    rw [sum_powersetCard_succ_insert (pairSum c) 1 hj, ih, pairSum_insert c hj,
      Finset.powersetCard_one, Finset.sum_map, Finset.mul_sum]
    congr 1
    refine Finset.sum_congr rfl fun i hi => ?_
    have hji : j ≠ i := fun h => hj (h ▸ hi)
    have h := pairSum_pair c hji
    rw [show (1 / 2 : ℝ) * (c j i + c i j) = (c j i + c i j) / 2 by ring, ← h]
    rfl

/-- The pair constant of the set of changed sites is the pairwise remainder of
`SecondOrderEnvelope.lean`. -/
theorem pairSum_supp [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (c : ι → ι → ℝ)
    (x₀ y : ∀ i, σ i) : pairSum c (supp x₀ y) = pairRemainder c x₀ y := by
  unfold pairSum pairRemainder
  congr 1
  rw [← Finset.sum_subset (Finset.subset_univ (supp x₀ y))]
  · refine Finset.sum_congr rfl fun i hi => ?_
    have hi1 : changed x₀ y i = 1 := changed_of_ne (mem_supp.mp hi)
    rw [← Finset.sum_subset (Finset.erase_subset_erase i (Finset.subset_univ (supp x₀ y)))]
    · refine Finset.sum_congr rfl fun k hk => ?_
      have hk1 : changed x₀ y k = 1 := changed_of_ne (mem_supp.mp (Finset.mem_of_mem_erase hk))
      rw [hi1, hk1, mul_one, mul_one]
    · intro k hk hk'
      have hki : k ≠ i := Finset.ne_of_mem_erase hk
      have hk0 : changed x₀ y k = 0 := by
        apply changed_of_eq
        by_contra h
        exact hk' (Finset.mem_erase.mpr ⟨hki, mem_supp.mpr h⟩)
      rw [hk0, mul_zero]
  · intro i _ hi
    have hi0 : changed x₀ y i = 0 := by
      apply changed_of_eq
      by_contra h
      exact hi (mem_supp.mpr h)
    apply Finset.sum_eq_zero
    intro k _
    rw [hi0, mul_zero, zero_mul]

/-- **The second-order remainder theorem is the case `m = 2`.**  With the pair constants
`pairSum c`, the order-`2` instance of `higherOrder_remainder` is literally the statement of
`secondOrder_remainder`: the interpolant is the star part and the bound is the pairwise
remainder. -/
theorem secondOrder_remainder_of_higherOrder [Fintype ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hg : MixedDiffBound g c)
    (hc : ∀ i j, c i j = c j i) (x₀ y : ∀ i, σ i) :
    |g y - starPart g x₀ y| ≤ pairRemainder c x₀ y := by
  have h2 : HigherDiffBound 2 g (pairSum c) :=
    higherDiffBound_two_of_mixedDiffBound g c (pairSum c)
      (fun i j hij => by rw [pairSum_pair c hij, ← hc i j]; linarith) hg
  have h := higherOrder_remainder 2 g (pairSum c) h2 x₀ y
  rwa [anchoredInterp_two, sum_pairSum_powersetCard_two, pairSum_supp] at h

/-! ### Non-vacuity for order three

Three binary sites, reference configuration `(0, 0, 0)` and the pure three-body coupling
`g y = [y 0 = 1] · [y 1 = 1] · [y 2 = 1]`.  It vanishes at every configuration with fewer than
three changed sites, its order-`3` mixed differences are bounded by `1`, and at `y = (1, 1, 1)`
the remainder bound of order `3` reads `1 ≤ 1`. -/

/-- Witness residual on three binary sites: the pure three-body coupling. -/
def tripleResidual (y : Config 3 2) : ℝ := if y 0 = 1 ∧ y 1 = 1 ∧ y 2 = 1 then 1 else 0

/-- The three-body coupling with rational values (evaluated by the kernel of Lean). -/
def tripleResidualQ (y : Config 3 2) : ℚ := if y 0 = 1 ∧ y 1 = 1 ∧ y 2 = 1 then 1 else 0

/-- The real three-body coupling is the cast of the rational one. -/
theorem tripleResidual_cast (y : Config 3 2) : tripleResidual y = (tripleResidualQ y : ℝ) := by
  unfold tripleResidual tripleResidualQ
  split_ifs <;> norm_num

/-- The rational three-body coupling vanishes at every configuration with fewer than three
changed sites (exhaustive evaluation). -/
theorem tripleResidualQ_vanish : ∀ y : Config 3 2,
    (supp (![0, 0, 0] : Config 3 2) y).card < 3 → tripleResidualQ y = 0 := by decide +kernel

/-- All order-`3` mixed differences of the rational three-body coupling are at most `1` in
absolute value (exhaustive evaluation in exact rational arithmetic). -/
theorem tripleResidualQ_mixed : ∀ (x b : Config 3 2) (T : Finset (Fin 3)), T.card = 3 →
    |∑ U ∈ T.powerset, (-1 : ℚ) ^ (T.card - U.card) * tripleResidualQ (mixConfig x b U)| ≤ 1 := by
  decide +kernel

/-- The three-body coupling has the order-`3` envelope `1`. -/
theorem tripleResidual_higherDiffBound : HigherDiffBound 3 tripleResidual (fun _ => 1) := by
  intro x b T hT
  have h : ((|∑ U ∈ T.powerset, (-1 : ℚ) ^ (T.card - U.card) *
      tripleResidualQ (mixConfig x b U)| : ℚ) : ℝ) ≤ ((1 : ℚ) : ℝ) :=
    Rat.cast_le.mpr (tripleResidualQ_mixed x b T hT)
  push_cast at h
  unfold mixedDiff
  simp only [tripleResidual_cast]
  exact h

/-- **Non-vacuity and sharpness for order three.**  The three-body coupling vanishes at every
configuration with fewer than three changed sites, has the order-`3` envelope `1`, and at
`y = (1, 1, 1)` both sides of the remainder bound of order `3` are equal to `1`. -/
theorem higherOrder_witness :
    (∀ y : Config 3 2, (supp (![0, 0, 0] : Config 3 2) y).card < 3 → tripleResidual y = 0) ∧
      HigherDiffBound 3 tripleResidual (fun _ => 1) ∧
      |tripleResidual ![1, 1, 1] -
        anchoredInterp 3 tripleResidual ![0, 0, 0] ![1, 1, 1]| = 1 ∧
      ∑ _T ∈ (supp (![0, 0, 0] : Config 3 2) ![1, 1, 1]).powersetCard 3, (1 : ℝ) = 1 := by
  have hv : ∀ y : Config 3 2, (supp (![0, 0, 0] : Config 3 2) y).card < 3 →
      tripleResidual y = 0 := by
    intro y hy
    rw [tripleResidual_cast, tripleResidualQ_vanish y hy, Rat.cast_zero]
  have hs : supp (![0, 0, 0] : Config 3 2) ![1, 1, 1] = Finset.univ := by decide
  refine ⟨hv, tripleResidual_higherDiffBound, ?_, ?_⟩
  · rw [anchoredInterp_eq_zero_of_vanish 3 tripleResidual ![0, 0, 0] hv, sub_zero]
    simp [tripleResidual]
  · rw [hs]
    simp

end MetricChain
