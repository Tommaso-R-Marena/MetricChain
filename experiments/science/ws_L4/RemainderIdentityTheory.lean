import Mathlib
import proofs.Frontiers.HigherOrderEnvelope

/-!
# The remainder identity of the anchored expansion — stated for the theory division's declarations

Science division, workstream L4, Part A.  This file is **generated** by `assemble.py`: it is
Parts 1–6 of `RemainderIdentity.lean` (same directory), verbatim, on top of
`import proofs.Frontiers.HigherOrderEnvelope` (read-only; the theory division's compiled file)
instead of the copies of Part 0 of that file.  With `open MetricChain`, the names `mixConfig`,
`mixedDiff`, `HigherDiffBound`, `supp`, `anchoredInterp` and the basic lemmas used in the proofs
are here the theory division's own declarations `MetricChain.mixConfig`, `MetricChain.mixedDiff`,
`MetricChain.HigherDiffBound`, `MetricChain.supp`, `MetricChain.anchoredInterp`, …  So the
theorems of this file are statements about the objects of the theory report's Theorem 11.18
(`MetricChain.higherOrder_remainder`), which `ScienceL4.abs_remainder_le_of_class` re-derives from
the identity.  Item 1 of Part A of the brief is `MetricChain.anchored_decomposition` (reused, not
re-proved here).  See `RemainderIdentity.lean` for the description of the contents.
-/

set_option autoImplicit false

namespace ScienceL4

open Finset MetricChain

variable {ι : Type*} {σ : ι → Type*}

/-! # Parts 1–6: repeated verbatim from `RemainderIdentity.lean` -/

/-! ## Part 1: the remainder identity (Proposition 1 of the P3 report, §2.1) -/

/-- The sites of `S` that lie strictly before every site of `T`.  For `T ≠ ∅` these are the
sites `i ∈ S` with `i < min T`; for `T = ∅` it is `S`. -/
def below [LinearOrder ι] (S T : Finset ι) : Finset ι :=
  S.filter fun i => ∀ t ∈ T, i < t

/-- Membership in `below`. -/
theorem mem_below [LinearOrder ι] {S T : Finset ι} {i : ι} :
    i ∈ below S T ↔ i ∈ S ∧ ∀ t ∈ T, i < t := by
  simp [below]

/-- Before the empty set: everything. -/
theorem below_empty [LinearOrder ι] (S : Finset ι) : below S ∅ = S := by
  ext i
  simp [mem_below]

/-- For a nonempty `T`, "before every site of `T`" is "before `min T`". -/
theorem mem_below_iff_lt_min' [LinearOrder ι] {S T : Finset ι} (hT : T.Nonempty) {i : ι} :
    i ∈ below S T ↔ i ∈ S ∧ i < T.min' hT := by
  rw [mem_below, Finset.lt_min'_iff]

/-- A new largest site `j` is not before a nonempty set of earlier sites. -/
theorem below_insert_of_nonempty [LinearOrder ι] [DecidableEq ι] {j : ι} {S T : Finset ι}
    (hj : ∀ i ∈ S, i < j) (hTS : T ⊆ S) (hT : T.Nonempty) :
    below (insert j S) T = below S T := by
  obtain ⟨t, ht⟩ := hT
  ext i
  rw [mem_below, mem_below, Finset.mem_insert]
  constructor
  · rintro ⟨hi | hi, h⟩
    · exact absurd (h t ht) (by rw [hi]; exact not_lt.mpr (hj t (hTS ht)).le)
    · exact ⟨hi, h⟩
  · rintro ⟨hi, h⟩
    exact ⟨Or.inr hi, h⟩

/-- The sites of `insert j S` before `insert j T`, for a new largest site `j`, are the sites of
`S` before `T`. -/
theorem below_insert_insert [LinearOrder ι] [DecidableEq ι] {j : ι} {S : Finset ι}
    (hj : ∀ i ∈ S, i < j) (T : Finset ι) :
    below (insert j S) (insert j T) = below S T := by
  ext i
  rw [mem_below, mem_below, Finset.mem_insert]
  constructor
  · rintro ⟨hi | hi, h⟩
    · exact absurd (h j (Finset.mem_insert_self j T)) (by rw [hi]; exact lt_irrefl j)
    · exact ⟨hi, fun t ht => h t (Finset.mem_insert_of_mem ht)⟩
  · rintro ⟨hi, h⟩
    refine ⟨Or.inr hi, fun t ht => ?_⟩
    rcases Finset.mem_insert.mp ht with rfl | ht
    · exact hj i hi
    · exact h t ht

/-- The truncated sum of mixed differences over the subsets of `insert j S` (`j ∉ S`): the
subsets of `S`, plus the mixed differences of the single-site difference `D_j g` over the subsets
of `S` with one site less. -/
theorem sum_mixedDiff_filter_insert [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x b : ∀ i, σ i)
    {j : ι} {S : Finset ι} (hjS : j ∉ S) (m : ℕ) :
    ∑ T ∈ (insert j S).powerset.filter (fun T => T.card < m + 1), mixedDiff g x T b =
      ∑ T ∈ S.powerset.filter (fun T => T.card < m + 1), mixedDiff g x T b +
        ∑ T ∈ S.powerset.filter (fun T => T.card < m),
          mixedDiff (fun z => g (Function.update z j (b j)) - g z) x T b := by
  rw [sum_powerset_insert_filter_card (fun n => n < m + 1) _ hjS]
  simp only [Nat.add_lt_add_iff_right]
  congr 1
  refine Finset.sum_congr rfl fun T hT => ?_
  exact mixedDiff_insert_siteDiff g x b fun hmem =>
    hjS (Finset.mem_powerset.mp (Finset.mem_filter.mp hT).1 hmem)

/-- **Remainder identity, general form.**  For every base point `x`, target states `b`, set `S`
of switched sites and order `m`: the value at the configuration with the sites of `S` switched,
minus the mixed differences at `x` over the subsets of `S` with fewer than `m` sites, is the sum
over the `m`-subsets `T` of `S` of the mixed difference over `T` at the base point in which the
sites of `S` before `T` are already switched.

Proof: induction on `S`, adding a largest site `j`.  With `D_j g z = g (z[j ↦ b j]) − g z`,
`R_{m+1}(g, insert j S) = R_{m+1}(g, S) + R_m(D_j g, S)`; the first term gives the `(m+1)`-subsets
without `j`, the second those that contain `j`, because
`mixedDiff (D_j g) z T b = mixedDiff g z (insert j T) b`; and adding the largest site changes
neither set of sites "before `T`". -/
theorem remainder_identity_mixConfig [LinearOrder ι] [DecidableEq ι] (b : ∀ i, σ i)
    (S : Finset ι) :
    ∀ (m : ℕ) (g : (∀ i, σ i) → ℝ) (x : ∀ i, σ i),
      g (mixConfig x b S) - ∑ T ∈ S.powerset.filter (fun T => T.card < m), mixedDiff g x T b =
        ∑ T ∈ S.powersetCard m, mixedDiff g (mixConfig x b (below S T)) T b := by
  induction S using Finset.induction_on_max with
  | empty =>
    intro m g x
    cases m with
    | zero => simp [mixedDiff_empty, mixConfig_empty, below_empty]
    | succ m =>
      have hfilter : (∅ : Finset ι).powerset.filter (fun T => T.card < m + 1) = {∅} := by
        rw [Finset.powerset_empty, Finset.filter_true_of_mem]
        intro T hT
        rw [Finset.mem_singleton.mp hT]
        simp
      have hcard : (∅ : Finset ι).powersetCard (m + 1) = ∅ :=
        Finset.powersetCard_eq_empty.mpr (by simp)
      rw [hfilter, hcard, Finset.sum_singleton, Finset.sum_empty, mixedDiff_empty,
        mixConfig_empty, sub_self]
  | insert j S hj ih =>
    intro m g x
    cases m with
    | zero => simp [mixedDiff_empty, below_empty]
    | succ m =>
      have hjS : j ∉ S := fun h => lt_irrefl j (hj j h)
      have hsum := sum_mixedDiff_filter_insert g x b hjS m
      have hR : ∑ T ∈ (insert j S).powersetCard (m + 1),
            mixedDiff g (mixConfig x b (below (insert j S) T)) T b =
          ∑ T ∈ S.powersetCard (m + 1), mixedDiff g (mixConfig x b (below S T)) T b +
            ∑ T ∈ S.powersetCard m,
              mixedDiff (fun z => g (Function.update z j (b j)) - g z)
                (mixConfig x b (below S T)) T b := by
        rw [sum_powersetCard_succ_insert
          (fun T => mixedDiff g (mixConfig x b (below (insert j S) T)) T b) m hjS]
        congr 1
        · refine Finset.sum_congr rfl fun T hT => ?_
          rw [Finset.mem_powersetCard] at hT
          have hne : T.Nonempty := Finset.card_pos.mp (by omega)
          rw [below_insert_of_nonempty hj hT.1 hne]
        · refine Finset.sum_congr rfl fun T hT => ?_
          rw [Finset.mem_powersetCard] at hT
          have hjT : j ∉ T := fun h => hjS (hT.1 h)
          rw [below_insert_insert hj, mixedDiff_insert_siteDiff g _ b hjT]
      have ih1 := ih (m + 1) g x
      have ih2 := ih m (fun z => g (Function.update z j (b j)) - g z) x
      rw [hsum, hR, mixConfig_insert]
      linarith

/-- **The base point of the `m`-subset `T` in Proposition 1**: the configuration `z^{T,y}` equal
to `y` at the sites before every site of `T` and to the anchor `x₀` at all other sites. -/
def switchedBase [LinearOrder ι] (x₀ y : ∀ i, σ i) (T : Finset ι) : ∀ i, σ i :=
  fun i => if ∀ t ∈ T, i < t then y i else x₀ i

/-- The paper's description of the base point: `z_i = y_i` for `i < min T`, `x₀_i` otherwise. -/
theorem switchedBase_apply [LinearOrder ι] (x₀ y : ∀ i, σ i) {T : Finset ι} (hT : T.Nonempty)
    (i : ι) : switchedBase x₀ y T i = if i < T.min' hT then y i else x₀ i := by
  simp only [switchedBase, Finset.lt_min'_iff]

/-- For `T = ∅` (order `0`) the base point is `y` itself. -/
theorem switchedBase_empty [LinearOrder ι] (x₀ y : ∀ i, σ i) : switchedBase x₀ y ∅ = y := by
  funext i
  simp [switchedBase]

/-- The base point agrees with the anchor at every site that is not before all of `T` — in
particular from `min T` on. -/
theorem switchedBase_of_exists_le [LinearOrder ι] (x₀ y : ∀ i, σ i) {T : Finset ι} {i : ι}
    (h : ∃ t ∈ T, t ≤ i) : switchedBase x₀ y T i = x₀ i := by
  obtain ⟨t, ht, hti⟩ := h
  have hn : ¬ ∀ t ∈ T, i < t := fun hall => absurd (hall t ht) (not_lt.mpr hti)
  simp [switchedBase, hn]

/-- The base point agrees with the anchor on `T`. -/
theorem switchedBase_of_mem [LinearOrder ι] (x₀ y : ∀ i, σ i) {T : Finset ι} {i : ι}
    (h : i ∈ T) : switchedBase x₀ y T i = x₀ i :=
  switchedBase_of_exists_le x₀ y ⟨i, h, le_rfl⟩

/-- At every site the base point has the state of the anchor or the state of `y`. -/
theorem switchedBase_eq_or [LinearOrder ι] (x₀ y : ∀ i, σ i) (T : Finset ι) (i : ι) :
    switchedBase x₀ y T i = x₀ i ∨ switchedBase x₀ y T i = y i := by
  unfold switchedBase
  split_ifs
  · exact Or.inr rfl
  · exact Or.inl rfl

/-- Switching the changed sites before `T` gives the base point of `T`. -/
theorem mixConfig_below_supp [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (x₀ y : ∀ i, σ i) (T : Finset ι) :
    mixConfig x₀ y (below (supp x₀ y) T) = switchedBase x₀ y T := by
  funext i
  by_cases hy : y i = x₀ i
  · simp [mixConfig, switchedBase, mem_below, mem_supp, hy]
  · simp [mixConfig, switchedBase, mem_below, mem_supp, hy]

/-- **Proposition 1 (remainder identity of the anchored expansion).**  For every `g`, anchor
`x₀`, configuration `y` and order `m`: the remainder of the anchored interpolant of order `m − 1`
is the sum, over the `m`-subsets `T` of the changed sites, of the mixed difference of `g` over
`T` with target `y`, at the base point equal to `y` before `min T` and to the anchor elsewhere. -/
theorem remainder_identity [Fintype ι] [LinearOrder ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    g y - anchoredInterp m g x₀ y =
      ∑ T ∈ (supp x₀ y).powersetCard m, mixedDiff g (switchedBase x₀ y T) T y := by
  have h := remainder_identity_mixConfig y (supp x₀ y) m g x₀
  rw [mixConfig_supp] at h
  unfold anchoredInterp
  rw [h]
  exact Finset.sum_congr rfl fun T _ => by rw [mixConfig_below_supp]

/-- Check: the exact decomposition `g y = ∑_{T ⊆ supp} Δ_T g(x₀; y_T)` (the theory division's
`anchored_decomposition`) is the remainder identity at an order above the number of changed
sites. -/
theorem anchored_decomposition_of_identity [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    g y = ∑ T ∈ (supp x₀ y).powerset, mixedDiff g x₀ T y := by
  have h := remainder_identity ((supp x₀ y).card + 1) g x₀ y
  rw [Finset.powersetCard_eq_empty.mpr (Nat.lt_succ_self _), Finset.sum_empty] at h
  unfold anchoredInterp at h
  rw [Finset.filter_true_of_mem] at h
  · linarith
  · intro T hT
    exact Nat.lt_succ_of_le (Finset.card_le_card (Finset.mem_powerset.mp hT))

/-- **Context expansion** (step (a) of the paper proof of Proposition 1).  If `V` is disjoint
from `T`, the mixed difference over `T` at the base point with the sites of `V` switched is the
sum over `U ⊆ V` of the mixed differences over `T ∪ U` at the original base point. -/
theorem mixedDiff_mixConfig_eq_sum [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (z b : ∀ i, σ i)
    (V : Finset ι) :
    ∀ T : Finset ι, Disjoint T V →
      mixedDiff g (mixConfig z b V) T b = ∑ U ∈ V.powerset, mixedDiff g z (T ∪ U) b := by
  induction V using Finset.induction_on with
  | empty =>
    intro T _
    simp [mixConfig_empty]
  | insert v V hv ih =>
    intro T hT
    have hvT : v ∉ T := fun h => (Finset.disjoint_left.mp hT h) (Finset.mem_insert_self v V)
    have hTV : Disjoint T V := Finset.disjoint_of_subset_right (Finset.subset_insert v V) hT
    have hTV' : Disjoint (insert v T) V := Finset.disjoint_insert_left.mpr ⟨hv, hTV⟩
    have h1 := mixedDiff_insert g (mixConfig z b V) b hvT
    have h2 : ∑ U ∈ V.powerset, mixedDiff g z (T ∪ insert v U) b =
        ∑ U ∈ V.powerset, mixedDiff g z (insert v T ∪ U) b := by
      refine Finset.sum_congr rfl fun U _ => ?_
      rw [Finset.union_insert, Finset.insert_union]
    rw [mixConfig_insert, Finset.sum_powerset_insert hv, h2, ← ih T hTV, ← ih (insert v T) hTV']
    linarith

/-- No site of `T` is before every site of `T`. -/
theorem disjoint_below [LinearOrder ι] (S T : Finset ι) : Disjoint T (below S T) := by
  rw [Finset.disjoint_left]
  intro i hiT hi
  exact lt_irrefl i ((mem_below.mp hi).2 i hiT)

/-- **Each summand of Proposition 1 in anchored terms** (step (b) of the paper proof): the mixed
difference over `T` at the base point of `T` is the sum of the anchored terms `d_{T ∪ U}` over
the sets `U` of changed sites before `T`. -/
theorem mixedDiff_switchedBase_eq_sum [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) (T : Finset ι) :
    mixedDiff g (switchedBase x₀ y T) T y =
      ∑ U ∈ (below (supp x₀ y) T).powerset, mixedDiff g x₀ (T ∪ U) y := by
  rw [← mixConfig_below_supp, mixedDiff_mixConfig_eq_sum g x₀ y _ T (disjoint_below _ T)]

/-- **The tail of the anchored decomposition, regrouped** (the identity behind step (b) of the
paper proof: "send each `U` with `|U| ≥ m` to the set `T` of its `m` largest elements").  The sum
of the anchored terms `d_U` over the sets `U` of at least `m` changed sites is the double sum over
the `m`-subsets `T` and the sets `U'` of changed sites before `T` of `d_{T ∪ U'}`.  (Obtained here
from the remainder identity, not from the bijection.) -/
theorem sum_mixedDiff_card_ge [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    ∑ U ∈ (supp x₀ y).powerset.filter (fun U => m ≤ U.card), mixedDiff g x₀ U y =
      ∑ T ∈ (supp x₀ y).powersetCard m,
        ∑ U ∈ (below (supp x₀ y) T).powerset, mixedDiff g x₀ (T ∪ U) y := by
  have h1 := remainder_identity m g x₀ y
  have h2 := anchored_decomposition g x₀ y
  have h3 := Finset.sum_filter_add_sum_filter_not (supp x₀ y).powerset (fun U => U.card < m)
    (fun U => mixedDiff g x₀ U y)
  have h4 : (supp x₀ y).powerset.filter (fun U => ¬ U.card < m) =
      (supp x₀ y).powerset.filter (fun U => m ≤ U.card) :=
    Finset.filter_congr fun U _ => not_lt
  rw [h4] at h3
  have h5 : ∑ T ∈ (supp x₀ y).powersetCard m, mixedDiff g (switchedBase x₀ y T) T y =
      ∑ T ∈ (supp x₀ y).powersetCard m,
        ∑ U ∈ (below (supp x₀ y) T).powerset, mixedDiff g x₀ (T ∪ U) y :=
    Finset.sum_congr rfl fun T _ => mixedDiff_switchedBase_eq_sum g x₀ y T
  unfold anchoredInterp at h1
  linarith

/-! ## Part 2: the corollary with anchored constants -/

/-- **Anchored envelope of order `m`** (the constants `c_T^anch` of the P3 report, §2.0): every
mixed difference of `g` over a set `T` of `m` sites, at a base point that agrees with the anchor
`x₀` on `T`, with any target states, is bounded by `c T`. -/
def AnchoredDiffBound [DecidableEq ι] (m : ℕ) (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i)
    (c : Finset ι → ℝ) : Prop :=
  ∀ (z b : ∀ i, σ i) (T : Finset ι), T.card = m → (∀ i ∈ T, z i = x₀ i) → |mixedDiff g z T b| ≤ c T

/-- **Ordered anchored envelope of order `m`**: the same with base points that agree with the
anchor at every site from the first site of `T` on (contexts differ from the anchor only before
`min T`).  This is all that Proposition 1 uses. -/
def OrderedAnchoredDiffBound [LinearOrder ι] [DecidableEq ι] (m : ℕ) (g : (∀ i, σ i) → ℝ)
    (x₀ : ∀ i, σ i) (c : Finset ι → ℝ) : Prop :=
  ∀ (z b : ∀ i, σ i) (T : Finset ι), T.card = m → (∀ i, (∃ t ∈ T, t ≤ i) → z i = x₀ i) →
    |mixedDiff g z T b| ≤ c T

/-- Class constants are anchored constants. -/
theorem anchoredDiffBound_of_class [DecidableEq ι] {m : ℕ} {g : (∀ i, σ i) → ℝ}
    {c : Finset ι → ℝ} (h : HigherDiffBound m g c) (x₀ : ∀ i, σ i) :
    AnchoredDiffBound m g x₀ c :=
  fun z b T hT _ => h z b T hT

/-- Anchored constants are ordered anchored constants. -/
theorem AnchoredDiffBound.ordered [LinearOrder ι] [DecidableEq ι] {m : ℕ}
    {g : (∀ i, σ i) → ℝ} {x₀ : ∀ i, σ i} {c : Finset ι → ℝ} (h : AnchoredDiffBound m g x₀ c) :
    OrderedAnchoredDiffBound m g x₀ c :=
  fun z b T hT hz => h z b T hT fun i hi => hz i ⟨i, hi, le_rfl⟩

/-- Anchored constants of order `m` are nonnegative on the `m`-subsets. -/
theorem AnchoredDiffBound.nonneg [DecidableEq ι] {m : ℕ} {g : (∀ i, σ i) → ℝ}
    {x₀ : ∀ i, σ i} {c : Finset ι → ℝ} (h : AnchoredDiffBound m g x₀ c) {T : Finset ι}
    (hT : T.card = m) : 0 ≤ c T :=
  (abs_nonneg _).trans (h x₀ x₀ T hT fun _ _ => rfl)

/-- Non-vacuity: on finite state spaces every function has class constants — hence anchored and
ordered anchored constants — of every order. -/
theorem exists_higherDiffBound [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)] (m : ℕ)
    (g : (∀ i, σ i) → ℝ) : ∃ c : Finset ι → ℝ, HigherDiffBound m g c := by
  refine ⟨fun T => ∑ x : (∀ i, σ i), ∑ b : (∀ i, σ i), |mixedDiff g x T b|, fun x b T _ => ?_⟩
  calc |mixedDiff g x T b| ≤ ∑ b' : (∀ i, σ i), |mixedDiff g x T b'| :=
        Finset.single_le_sum (f := fun b' => |mixedDiff g x T b'|) (fun _ _ => abs_nonneg _)
          (Finset.mem_univ b)
    _ ≤ ∑ x' : (∀ i, σ i), ∑ b' : (∀ i, σ i), |mixedDiff g x' T b'| :=
        Finset.single_le_sum (f := fun x' => ∑ b' : (∀ i, σ i), |mixedDiff g x' T b'|)
          (fun _ _ => Finset.sum_nonneg fun _ _ => abs_nonneg _) (Finset.mem_univ x)

/-- **Remainder bound, local form**: only the `m`-th order differences that occur in
Proposition 1 at the configuration `y` need to be bounded. -/
theorem abs_remainder_le_of_local [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ y : ∀ i, σ i)
    (h : ∀ T ∈ (supp x₀ y).powersetCard m, |mixedDiff g (switchedBase x₀ y T) T y| ≤ c T) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ T ∈ (supp x₀ y).powersetCard m, c T := by
  rw [remainder_identity]
  exact (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum h)

/-- **Remainder bound with ordered anchored constants.** -/
theorem abs_remainder_le_of_ordered [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : OrderedAnchoredDiffBound m g x₀ c) (y : ∀ i, σ i) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ T ∈ (supp x₀ y).powersetCard m, c T :=
  abs_remainder_le_of_local m g c x₀ y fun T hT =>
    hg _ y T (Finset.mem_powersetCard.mp hT).2 fun _ hi => switchedBase_of_exists_le x₀ y hi

/-- **Corollary of Proposition 1 (anchored constants).**  If `|Δ_T g(z; b_T)| ≤ c T` for all
`m`-subsets `T`, all base points `z` with `z_T = x₀_T` and all targets, then
`|g y − I_{m−1} g y| ≤ ∑_{T ⊆ supp x₀ y, |T| = m} c T`. -/
theorem abs_remainder_le_of_anchored [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : AnchoredDiffBound m g x₀ c) (y : ∀ i, σ i) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ T ∈ (supp x₀ y).powersetCard m, c T :=
  abs_remainder_le_of_ordered m g c x₀ hg.ordered y

/-- **The remainder theorem with class constants** (the theory division's Theorem 11.18,
`higherOrder_remainder`), re-derived from the identity.  The order on the sites is used only in
the proof. -/
theorem abs_remainder_le_of_class [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ)
    (hg : HigherDiffBound m g c) (x₀ y : ∀ i, σ i) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ T ∈ (supp x₀ y).powersetCard m, c T :=
  abs_remainder_le_of_anchored m g c x₀ (anchoredDiffBound_of_class hg x₀) y

/-! ## Part 3: the allocation lemma at order `m` -/

/-- **Site shares cover the `m`-subsets** (order-`m` version of the theory division's
`cover_of_site_shares`, which is the case `m = 3`; same proof).  If every `m`-subset `T` has
nonnegative shares `lam T i` on its sites that add up to at least `c T`, then for every set `S`
of sites the sum of `c` over the `m`-subsets of `S` is at most the sum over the sites `i ∈ S` of
all the shares charged to `i`. -/
theorem cover_of_site_shares_order [Fintype ι] [DecidableEq ι] (m : ℕ) (c : Finset ι → ℝ)
    (lam : Finset ι → ι → ℝ) (hlam : ∀ T : Finset ι, T.card = m → ∀ i ∈ T, 0 ≤ lam T i)
    (hshare : ∀ T : Finset ι, T.card = m → c T ≤ ∑ i ∈ T, lam T i) (S : Finset ι) :
    ∑ T ∈ S.powersetCard m, c T ≤
      ∑ i ∈ S, ∑ T ∈ (univ : Finset ι).powersetCard m, (if i ∈ T then lam T i else 0) := by
  calc ∑ T ∈ S.powersetCard m, c T
      ≤ ∑ T ∈ S.powersetCard m, ∑ i ∈ T, lam T i :=
        Finset.sum_le_sum fun T hT => hshare T (Finset.mem_powersetCard.mp hT).2
    _ = ∑ T ∈ S.powersetCard m, ∑ i ∈ S, (if i ∈ T then lam T i else 0) := by
        refine Finset.sum_congr rfl fun T hT => ?_
        have hTS : T ⊆ S := (Finset.mem_powersetCard.mp hT).1
        rw [← Finset.sum_filter]
        congr 1
        ext i
        simp only [Finset.mem_filter]
        exact ⟨fun h => ⟨hTS h, h⟩, fun h => h.2⟩
    _ = ∑ i ∈ S, ∑ T ∈ S.powersetCard m, (if i ∈ T then lam T i else 0) := Finset.sum_comm
    _ ≤ ∑ i ∈ S, ∑ T ∈ (univ : Finset ι).powersetCard m, (if i ∈ T then lam T i else 0) := by
        refine Finset.sum_le_sum fun i _ => ?_
        refine Finset.sum_le_sum_of_subset_of_nonneg
          (Finset.powersetCard_mono (Finset.subset_univ S)) fun T hT _ => ?_
        split_ifs with hi
        · exact hlam T (Finset.mem_powersetCard.mp hT).2 i hi
        · exact le_rfl

/-- **Site penalties** `γ_i = (1/m) ∑_{T ∋ i, |T| = m} c_T` (P3 report, §2.4). -/
noncomputable def sitePenalty [Fintype ι] [DecidableEq ι] (m : ℕ) (c : Finset ι → ℝ) (i : ι) : ℝ :=
  (1 / (m : ℝ)) * ∑ T ∈ ((univ : Finset ι).powersetCard m).filter (fun T => i ∈ T), c T

/-- The site penalty as the sum of the equal shares `c T / m` charged to the site. -/
theorem sitePenalty_eq_sum_ite [Fintype ι] [DecidableEq ι] (m : ℕ) (c : Finset ι → ℝ) (i : ι) :
    sitePenalty m c i =
      ∑ T ∈ (univ : Finset ι).powersetCard m, (if i ∈ T then c T / (m : ℝ) else 0) := by
  unfold sitePenalty
  rw [Finset.sum_filter, Finset.mul_sum]
  refine Finset.sum_congr rfl fun T _ => ?_
  split_ifs
  · ring
  · ring

/-- **Allocation lemma at order `m ≥ 1`.**  For constants that are nonnegative on the
`m`-subsets and `γ_i = (1/m) ∑_{T ∋ i, |T| = m} c_T`:
`∑_{T ⊆ S, |T| = m} c_T ≤ ∑_{i ∈ S} γ_i` for every set `S` of sites. -/
theorem allocation_lemma [Fintype ι] [DecidableEq ι] {m : ℕ} (hm : 1 ≤ m) (c : Finset ι → ℝ)
    (hc : ∀ T : Finset ι, T.card = m → 0 ≤ c T) (S : Finset ι) :
    ∑ T ∈ S.powersetCard m, c T ≤ ∑ i ∈ S, sitePenalty m c i := by
  have hm0 : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm
  have h := cover_of_site_shares_order m c (fun T _ => c T / (m : ℝ))
    (fun T hT _ _ => div_nonneg (hc T hT) hm0.le)
    (fun T hT => by
      rw [Finset.sum_const, hT, nsmul_eq_mul]
      exact le_of_eq (by field_simp)) S
  refine h.trans (le_of_eq ?_)
  exact Finset.sum_congr rfl fun i _ => (sitePenalty_eq_sum_ite m c i).symm

/-- The site penalty from two totals (P3 report, §2.4): `m · γ_i = Γ_m − Γ_m^{(−i)}`, the sum of
the constants over all `m`-subsets minus the sum over the `m`-subsets that avoid the site. -/
theorem sitePenalty_eq_total_sub [Fintype ι] [DecidableEq ι] {m : ℕ} (hm : 1 ≤ m)
    (c : Finset ι → ℝ) (i : ι) :
    (m : ℝ) * sitePenalty m c i =
      ∑ T ∈ (univ : Finset ι).powersetCard m, c T -
        ∑ T ∈ ((univ : Finset ι).erase i).powersetCard m, c T := by
  have hm0 : (m : ℝ) ≠ 0 := by
    have : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm
    exact this.ne'
  have hsplit := Finset.sum_filter_add_sum_filter_not ((univ : Finset ι).powersetCard m)
    (fun T => i ∈ T) c
  have hErase : ((univ : Finset ι).powersetCard m).filter (fun T => ¬ i ∈ T) =
      ((univ : Finset ι).erase i).powersetCard m := by
    ext T
    simp only [Finset.mem_filter, Finset.mem_powersetCard, Finset.subset_univ, true_and]
    constructor
    · rintro ⟨hc, hi⟩
      exact ⟨fun t ht => Finset.mem_erase.mpr ⟨fun h => hi (h ▸ ht), Finset.mem_univ t⟩, hc⟩
    · rintro ⟨hsub, hc⟩
      exact ⟨hc, fun hi => Finset.notMem_erase i _ (hsub hi)⟩
  rw [hErase] at hsplit
  unfold sitePenalty
  rw [← hsplit]
  field_simp
  ring

/-! ## Part 4: the sandwich -/

/-- **The sandwich, general shares.**  With anchored constants `c` of order `m` and nonnegative
shares `lam T i` of each `m`-subset among its sites that add up to at least `c T`, the anchored
interpolant of order `m − 1` minus / plus the penalties of the changed sites brackets `g`. -/
theorem anchored_sandwich_shares [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : AnchoredDiffBound m g x₀ c) (lam : Finset ι → ι → ℝ)
    (hlam : ∀ T : Finset ι, T.card = m → ∀ i ∈ T, 0 ≤ lam T i)
    (hshare : ∀ T : Finset ι, T.card = m → c T ≤ ∑ i ∈ T, lam T i) (y : ∀ i, σ i) :
    anchoredInterp m g x₀ y -
        ∑ i ∈ supp x₀ y, ∑ T ∈ (univ : Finset ι).powersetCard m, (if i ∈ T then lam T i else 0) ≤
        g y ∧
      g y ≤ anchoredInterp m g x₀ y +
        ∑ i ∈ supp x₀ y, ∑ T ∈ (univ : Finset ι).powersetCard m, (if i ∈ T then lam T i else 0) := by
  have h1 := abs_le.mp (abs_remainder_le_of_anchored m g c x₀ hg y)
  have h2 := cover_of_site_shares_order m c lam hlam hshare (supp x₀ y)
  exact ⟨by linarith [h1.1], by linarith [h1.2]⟩

/-- **The sandwich** (item 5 of Part A of the brief).  With anchored constants `c` of order
`m ≥ 1` and the site penalties `γ_i = (1/m) ∑_{T ∋ i, |T| = m} c_T`:
`I_{m−1} g(y) − ∑_{i ∈ S(y)} γ_i ≤ g(y) ≤ I_{m−1} g(y) + ∑_{i ∈ S(y)} γ_i`.
Nonnegativity of the constants is not a hypothesis: it follows from the bound at the anchor. -/
theorem anchored_sandwich [Fintype ι] [LinearOrder ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    {m : ℕ} (hm : 1 ≤ m) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : AnchoredDiffBound m g x₀ c) (y : ∀ i, σ i) :
    anchoredInterp m g x₀ y - ∑ i ∈ supp x₀ y, sitePenalty m c i ≤ g y ∧
      g y ≤ anchoredInterp m g x₀ y + ∑ i ∈ supp x₀ y, sitePenalty m c i := by
  have h1 := abs_le.mp (abs_remainder_le_of_anchored m g c x₀ hg y)
  have h2 := allocation_lemma hm c (fun T hT => hg.nonneg hT) (supp x₀ y)
  exact ⟨by linarith [h1.1], by linarith [h1.2]⟩

/-- **The sandwich with the constant** `Γ_m = ∑_{|T| = m} c_T` (the sum over all `m`-subsets of the
sites), any `m`. -/
theorem anchored_sandwich_total [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : AnchoredDiffBound m g x₀ c) (y : ∀ i, σ i) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ T ∈ (univ : Finset ι).powersetCard m, c T :=
  (abs_remainder_le_of_anchored m g c x₀ hg y).trans
    (Finset.sum_le_sum_of_subset_of_nonneg (Finset.powersetCard_mono (Finset.subset_univ _))
      fun _ hT _ => hg.nonneg (Finset.mem_powersetCard.mp hT).2)

/-- The penalty of the changed sites is a one-body term: `∑_{i ∈ S(y)} γ_i = ∑_i γ_i [y_i ≠ x₀_i]`. -/
theorem sum_supp_eq_sum_ite [Fintype ι] [∀ i, DecidableEq (σ i)] (x₀ y : ∀ i, σ i) (γ : ι → ℝ) :
    ∑ i ∈ supp x₀ y, γ i = ∑ i, (if y i ≠ x₀ i then γ i else 0) := by
  unfold supp
  rw [Finset.sum_filter]

/-! ## Part 5: one-site oscillation of the remainder (P3 report, §3.7) -/

/-- A mixed difference over `T` depends on the target states only through the sites of `T`. -/
theorem mixedDiff_congr_target [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x : ∀ i, σ i)
    {T : Finset ι} {b b' : ∀ i, σ i} (h : ∀ j ∈ T, b j = b' j) :
    mixedDiff g x T b = mixedDiff g x T b' := by
  unfold mixedDiff
  refine Finset.sum_congr rfl fun U hU => ?_
  have hUT := Finset.mem_powerset.mp hU
  have e : mixConfig x b U = mixConfig x b' U := by
    funext j
    by_cases hj : j ∈ U
    · simp [mixConfig, hj, h j (hUT hj)]
    · simp [mixConfig, hj]
  rw [e]

/-- Switching all changed sites except `i` gives `y` with the site `i` reset to the anchor. -/
theorem mixConfig_erase_supp [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (x₀ y : ∀ i, σ i) (i : ι) :
    mixConfig x₀ y ((supp x₀ y).erase i) = Function.update y i (x₀ i) := by
  funext j
  by_cases hj : j = i
  · subst hj
    simp [mixConfig]
  · by_cases hy : y j = x₀ j
    · simp [mixConfig, mem_supp, hj, hy]
    · simp [mixConfig, mem_supp, hj, hy]

/-- Resetting the site `i` to the anchor removes it from the changed sites. -/
theorem supp_update_anchor [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (x₀ y : ∀ i, σ i) (i : ι) :
    supp x₀ (Function.update y i (x₀ i)) = (supp x₀ y).erase i := by
  ext j
  by_cases hj : j = i
  · subst hj
    simp [mem_supp]
  · simp [mem_supp, hj]

/-- The interpolant at `y` with the site `i` reset to the anchor, in terms of the mixed
differences with target `y`. -/
theorem anchoredInterp_update_anchor [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) (i : ι) :
    anchoredInterp m g x₀ (Function.update y i (x₀ i)) =
      ∑ T ∈ ((supp x₀ y).erase i).powerset.filter (fun T => T.card < m), mixedDiff g x₀ T y := by
  unfold anchoredInterp
  rw [supp_update_anchor]
  refine Finset.sum_congr rfl fun T hT => ?_
  have hTS := Finset.mem_powerset.mp (Finset.mem_filter.mp hT).1
  exact mixedDiff_congr_target g x₀ fun j hj =>
    Function.update_of_ne (Finset.ne_of_mem_erase (hTS hj)) _ _

/-- **Switching one more site changes the remainder by a sum of `m`-th order differences that
contain that site.**  For `j ∉ S` (any site, not necessarily the last), the remainder of order
`m + 1` after switching `insert j S` minus the remainder after switching `S` is, in absolute
value, at most the sum of the bounds of the differences over the sets `insert j T`, `T` an
`m`-subset of `S`.  (The difference is the remainder of order `m` of the single-site difference
`D_j g`, to which the remainder identity applies.) -/
theorem abs_remainder_insert_sub_le [LinearOrder ι] [DecidableEq ι] (g : (∀ i, σ i) → ℝ)
    (c : Finset ι → ℝ) (x b : ∀ i, σ i) {j : ι} {S : Finset ι} (hjS : j ∉ S) (m : ℕ)
    (hc : ∀ T ∈ S.powersetCard m,
      |mixedDiff g (mixConfig x b (below S T)) (insert j T) b| ≤ c (insert j T)) :
    |(g (mixConfig x b (insert j S)) -
          ∑ T ∈ (insert j S).powerset.filter (fun T => T.card < m + 1), mixedDiff g x T b) -
        (g (mixConfig x b S) -
          ∑ T ∈ S.powerset.filter (fun T => T.card < m + 1), mixedDiff g x T b)| ≤
      ∑ T ∈ S.powersetCard m, c (insert j T) := by
  have h := remainder_identity_mixConfig b S m (fun z => g (Function.update z j (b j)) - g z) x
  have e : (g (mixConfig x b (insert j S)) -
        ∑ T ∈ (insert j S).powerset.filter (fun T => T.card < m + 1), mixedDiff g x T b) -
      (g (mixConfig x b S) -
        ∑ T ∈ S.powerset.filter (fun T => T.card < m + 1), mixedDiff g x T b) =
      ∑ T ∈ S.powersetCard m,
        mixedDiff (fun z => g (Function.update z j (b j)) - g z) (mixConfig x b (below S T)) T b := by
    rw [sum_mixedDiff_filter_insert g x b hjS m, mixConfig_insert, ← h]
    ring
  rw [e]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun T hT => ?_)
  have hjT : j ∉ T := fun hmem => hjS ((Finset.mem_powersetCard.mp hT).1 hmem)
  rw [← mixedDiff_insert_siteDiff g _ b hjT]
  exact hc T hT

/-- The constants of the `(m + 1)`-subsets `insert i T`, `T ⊆ S`, `i ∉ S`, are among those of the
`(m + 1)`-subsets that contain `i`. -/
theorem sum_insert_le_sum_filter [Fintype ι] [DecidableEq ι] (c : Finset ι → ℝ) (m : ℕ)
    (hc : ∀ T : Finset ι, T.card = m + 1 → 0 ≤ c T) {i : ι} {S : Finset ι} (hiS : i ∉ S) :
    ∑ T ∈ S.powersetCard m, c (insert i T) ≤
      ∑ T ∈ ((univ : Finset ι).powersetCard (m + 1)).filter (fun T => i ∈ T), c T := by
  have h := sum_powersetCard_succ_insert (fun T => if i ∈ T then c T else 0) m hiS
  have h1 : ∑ T ∈ S.powersetCard (m + 1), (if i ∈ T then c T else 0) = 0 :=
    Finset.sum_eq_zero fun T hT => if_neg fun hi => hiS ((Finset.mem_powersetCard.mp hT).1 hi)
  have h2 : ∑ T ∈ S.powersetCard m, (if i ∈ insert i T then c (insert i T) else 0) =
      ∑ T ∈ S.powersetCard m, c (insert i T) :=
    Finset.sum_congr rfl fun T _ => if_pos (Finset.mem_insert_self i T)
  rw [h1, h2, zero_add] at h
  rw [← h, Finset.sum_filter]
  refine Finset.sum_le_sum_of_subset_of_nonneg
    (Finset.powersetCard_mono (Finset.subset_univ _)) fun T hT _ => ?_
  split_ifs
  · exact hc T (Finset.mem_powersetCard.mp hT).2
  · exact le_rfl

/-- **Resetting one site to the anchor changes the remainder by at most the constants of the
`m`-subsets through that site**: with anchored constants of order `m ≥ 1` and
`R = g − I_{m−1} g`, `|R(y) − R(y[i ↦ x₀ i])| ≤ ∑_{T ∋ i, |T| = m} c_T`. -/
theorem abs_remainder_sub_reset_le [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] {m : ℕ} (hm : 1 ≤ m) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ)
    (x₀ : ∀ i, σ i) (hg : AnchoredDiffBound m g x₀ c) (y : ∀ i, σ i) (i : ι) :
    |(g y - anchoredInterp m g x₀ y) -
        (g (Function.update y i (x₀ i)) -
          anchoredInterp m g x₀ (Function.update y i (x₀ i)))| ≤
      ∑ T ∈ ((univ : Finset ι).powersetCard m).filter (fun T => i ∈ T), c T := by
  by_cases hi : y i = x₀ i
  · have e : Function.update y i (x₀ i) = y := by
      rw [← hi]
      exact Function.update_eq_self i y
    rw [e, sub_self, abs_zero]
    exact Finset.sum_nonneg fun T hT =>
      hg.nonneg (Finset.mem_powersetCard.mp (Finset.mem_filter.mp hT).1).2
  · obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
    have hiS : i ∉ (supp x₀ y).erase i := Finset.notMem_erase i _
    have hins : insert i ((supp x₀ y).erase i) = supp x₀ y :=
      Finset.insert_erase (mem_supp.mpr hi)
    have hbound := abs_remainder_insert_sub_le g c x₀ y hiS m' (fun T hT => by
      have hT' := Finset.mem_powersetCard.mp hT
      have hiT : i ∉ T := fun hmem => hiS (hT'.1 hmem)
      refine hg _ y (insert i T) (by rw [Finset.card_insert_of_notMem hiT, hT'.2]) ?_
      intro j hj
      have hnot : j ∉ below ((supp x₀ y).erase i) T := by
        intro hmem
        rcases Finset.mem_insert.mp hj with rfl | hjT
        · exact hiS (mem_below.mp hmem).1
        · exact lt_irrefl j ((mem_below.mp hmem).2 j hjT)
      show (if j ∈ below ((supp x₀ y).erase i) T then y j else x₀ j) = x₀ j
      rw [if_neg hnot])
    rw [hins, mixConfig_supp, mixConfig_erase_supp, ← anchoredInterp_update_anchor] at hbound
    exact hbound.trans (sum_insert_le_sum_filter c m' (fun T hT => hg.nonneg hT) hiS)

/-- The sum of the constants of the `m`-subsets through a site is `m` times its site penalty. -/
theorem mul_sitePenalty [Fintype ι] [DecidableEq ι] {m : ℕ} (hm : 1 ≤ m) (c : Finset ι → ℝ)
    (i : ι) :
    (m : ℝ) * sitePenalty m c i =
      ∑ T ∈ ((univ : Finset ι).powersetCard m).filter (fun T => i ∈ T), c T := by
  have hm0 : (m : ℝ) ≠ 0 := by
    have : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm
    exact this.ne'
  unfold sitePenalty
  field_simp

/-- **Certified one-site oscillation of the remainder** (P3 report, §3.7: `c_i(R) ≤ 2 m γ_i`).
With anchored constants of order `m ≥ 1`: if `y` and `y'` differ at the site `i` only, the
remainders `R = g − I_{m−1} g` at `y` and `y'` differ by at most
`2 ∑_{T ∋ i, |T| = m} c_T = 2 m γ_i`. -/
theorem remainder_oscillation_le [Fintype ι] [LinearOrder ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] {m : ℕ} (hm : 1 ≤ m) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ)
    (x₀ : ∀ i, σ i) (hg : AnchoredDiffBound m g x₀ c) (y y' : ∀ i, σ i) (i : ι)
    (hyy' : ∀ j, j ≠ i → y j = y' j) :
    |(g y - anchoredInterp m g x₀ y) - (g y' - anchoredInterp m g x₀ y')| ≤
      2 * ((m : ℝ) * sitePenalty m c i) := by
  have h1 := abs_le.mp (abs_remainder_sub_reset_le hm g c x₀ hg y i)
  have h2 := abs_le.mp (abs_remainder_sub_reset_le hm g c x₀ hg y' i)
  have e : Function.update y i (x₀ i) = Function.update y' i (x₀ i) := by
    funext j
    by_cases hj : j = i
    · subst hj
      simp
    · rw [Function.update_of_ne hj, Function.update_of_ne hj, hyy' j hj]
  rw [e] at h1
  rw [mul_sitePenalty hm c i, abs_le]
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

/-! ## Part 6: the corollary, the sandwich and the oscillation bound without an order on the sites

The hypotheses and conclusions of these statements do not mention the order of the sites; the
order was an instance argument above only because the proofs use Proposition 1.  Here a linear
order on the finite type of sites is chosen inside the proof. -/

/-- A finite type has a linear order (transported from `Fin n`). -/
@[reducible] noncomputable def linearOrderOfFintype (α : Type*) [Fintype α] : LinearOrder α :=
  LinearOrder.lift' (Fintype.equivFin α) (Fintype.equivFin α).injective

/-- **Corollary of Proposition 1 (anchored constants), no order on the sites.** -/
theorem abs_remainder_le_of_anchored_unordered [Fintype ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : AnchoredDiffBound m g x₀ c) (y : ∀ i, σ i) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ T ∈ (supp x₀ y).powersetCard m, c T := by
  letI : LinearOrder ι := linearOrderOfFintype ι
  exact abs_remainder_le_of_anchored m g c x₀ hg y

/-- **The sandwich, no order on the sites.** -/
theorem anchored_sandwich_unordered [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    {m : ℕ} (hm : 1 ≤ m) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : AnchoredDiffBound m g x₀ c) (y : ∀ i, σ i) :
    anchoredInterp m g x₀ y - ∑ i ∈ supp x₀ y, sitePenalty m c i ≤ g y ∧
      g y ≤ anchoredInterp m g x₀ y + ∑ i ∈ supp x₀ y, sitePenalty m c i := by
  letI : LinearOrder ι := linearOrderOfFintype ι
  exact anchored_sandwich hm g c x₀ hg y

/-- **The sandwich with general shares, no order on the sites.** -/
theorem anchored_sandwich_shares_unordered [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : AnchoredDiffBound m g x₀ c) (lam : Finset ι → ι → ℝ)
    (hlam : ∀ T : Finset ι, T.card = m → ∀ i ∈ T, 0 ≤ lam T i)
    (hshare : ∀ T : Finset ι, T.card = m → c T ≤ ∑ i ∈ T, lam T i) (y : ∀ i, σ i) :
    anchoredInterp m g x₀ y -
        ∑ i ∈ supp x₀ y, ∑ T ∈ (univ : Finset ι).powersetCard m, (if i ∈ T then lam T i else 0) ≤
        g y ∧
      g y ≤ anchoredInterp m g x₀ y +
        ∑ i ∈ supp x₀ y, ∑ T ∈ (univ : Finset ι).powersetCard m, (if i ∈ T then lam T i else 0) := by
  letI : LinearOrder ι := linearOrderOfFintype ι
  exact anchored_sandwich_shares m g c x₀ hg lam hlam hshare y

/-- **Certified one-site oscillation of the remainder, no order on the sites.** -/
theorem remainder_oscillation_le_unordered [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    {m : ℕ} (hm : 1 ≤ m) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : AnchoredDiffBound m g x₀ c) (y y' : ∀ i, σ i) (i : ι)
    (hyy' : ∀ j, j ≠ i → y j = y' j) :
    |(g y - anchoredInterp m g x₀ y) - (g y' - anchoredInterp m g x₀ y')| ≤
      2 * ((m : ℝ) * sitePenalty m c i) := by
  letI : LinearOrder ι := linearOrderOfFintype ι
  exact remainder_oscillation_le hm g c x₀ hg y y' i hyy'

end ScienceL4

/-! ## The headline theorems with every name of the theory division written out

Each statement below is closed by the corresponding theorem of Parts 1–6 as it stands, so the
kernel has checked that those theorems are statements about `MetricChain.mixedDiff`,
`MetricChain.supp`, `MetricChain.anchoredInterp` and `MetricChain.HigherDiffBound`. -/

namespace ScienceL4

open Finset

/-- **Proposition 1** for the theory division's `mixedDiff` and `anchoredInterp`
(`ScienceL4.switchedBase x₀ y T i = if ∀ t ∈ T, i < t then y i else x₀ i`). -/
theorem remainder_identity_theory {ι : Type*} {σ : ι → Type*} [Fintype ι] [LinearOrder ι]
    [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    g y - MetricChain.anchoredInterp m g x₀ y =
      ∑ T ∈ (MetricChain.supp x₀ y).powersetCard m,
        MetricChain.mixedDiff g (ScienceL4.switchedBase x₀ y T) T y :=
  remainder_identity m g x₀ y

/-- The theory division's Theorem 11.18 — literally the statement of
`MetricChain.higherOrder_remainder`, with no order on the sites — obtained from the identity. -/
theorem higherOrder_remainder_of_identity {ι : Type*} {σ : ι → Type*} [Fintype ι]
    [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ)
    (c : Finset ι → ℝ) (hg : MetricChain.HigherDiffBound m g c) (x₀ y : ∀ i, σ i) :
    |g y - MetricChain.anchoredInterp m g x₀ y| ≤
      ∑ T ∈ (MetricChain.supp x₀ y).powersetCard m, c T :=
  abs_remainder_le_of_anchored_unordered m g c x₀ (anchoredDiffBound_of_class hg x₀) y

/-- **The sandwich** for the theory division's declarations, with the anchored hypothesis and the
site penalties written out; no order on the sites. -/
theorem anchored_sandwich_theory {ι : Type*} {σ : ι → Type*} [Fintype ι]
    [DecidableEq ι] [∀ i, DecidableEq (σ i)] {m : ℕ} (hm : 1 ≤ m) (g : (∀ i, σ i) → ℝ)
    (c : Finset ι → ℝ) (x₀ : ∀ i, σ i)
    (hg : ∀ (z b : ∀ i, σ i) (T : Finset ι), T.card = m → (∀ i ∈ T, z i = x₀ i) →
      |MetricChain.mixedDiff g z T b| ≤ c T) (y : ∀ i, σ i) :
    MetricChain.anchoredInterp m g x₀ y - ∑ i ∈ MetricChain.supp x₀ y,
        (1 / (m : ℝ)) * ∑ T ∈ ((univ : Finset ι).powersetCard m).filter (fun T => i ∈ T), c T ≤
        g y ∧
      g y ≤ MetricChain.anchoredInterp m g x₀ y + ∑ i ∈ MetricChain.supp x₀ y,
        (1 / (m : ℝ)) * ∑ T ∈ ((univ : Finset ι).powersetCard m).filter (fun T => i ∈ T), c T :=
  anchored_sandwich_unordered hm g c x₀ hg y

end ScienceL4

/-! ## Axioms -/

#print axioms MetricChain.anchored_decomposition
#print axioms ScienceL4.remainder_identity_mixConfig
#print axioms ScienceL4.switchedBase_apply
#print axioms ScienceL4.switchedBase_of_mem
#print axioms ScienceL4.remainder_identity
#print axioms ScienceL4.anchored_decomposition_of_identity
#print axioms ScienceL4.mixedDiff_mixConfig_eq_sum
#print axioms ScienceL4.mixedDiff_switchedBase_eq_sum
#print axioms ScienceL4.sum_mixedDiff_card_ge
#print axioms ScienceL4.exists_higherDiffBound
#print axioms ScienceL4.abs_remainder_le_of_local
#print axioms ScienceL4.abs_remainder_le_of_ordered
#print axioms ScienceL4.abs_remainder_le_of_anchored
#print axioms ScienceL4.abs_remainder_le_of_class
#print axioms ScienceL4.cover_of_site_shares_order
#print axioms ScienceL4.allocation_lemma
#print axioms ScienceL4.sitePenalty_eq_total_sub
#print axioms ScienceL4.anchored_sandwich_shares
#print axioms ScienceL4.anchored_sandwich
#print axioms ScienceL4.anchored_sandwich_total
#print axioms ScienceL4.sum_supp_eq_sum_ite
#print axioms ScienceL4.abs_remainder_insert_sub_le
#print axioms ScienceL4.abs_remainder_sub_reset_le
#print axioms ScienceL4.remainder_oscillation_le
#print axioms ScienceL4.abs_remainder_le_of_anchored_unordered
#print axioms ScienceL4.anchored_sandwich_unordered
#print axioms ScienceL4.anchored_sandwich_shares_unordered
#print axioms ScienceL4.remainder_oscillation_le_unordered
#print axioms ScienceL4.remainder_identity_theory
#print axioms ScienceL4.higherOrder_remainder_of_identity
#print axioms ScienceL4.anchored_sandwich_theory
