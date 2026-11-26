import Mathlib
import proofs.Frontiers.AnchoredRemainder

/-!
# The remainder of an anchored expansion over a down-closed family of sets of sites

`AnchoredRemainder.lean` writes the error of the anchored expansion of order `m - 1` — the sum of
the mixed differences at the reference over the sets of fewer than `m` changed sites — as a sum of
mixed differences over the sets of exactly `m` changed sites (`anchored_remainder_identity`).
"Fewer than `m` sites" is one down-closed family of sets of sites.  This file proves the identity
for **every down-closed family** `D` (every subset of a member is a member): the sets of `m` sites
are replaced by the *threshold sets* of `D`.

The identity for a down-closed family and the bound of Part B are Propositions 10 and 11 of the Scientific
Discovery Division's workstream P5 (message SCI-MSG-0024), with paper proofs there and the request to
machine-check them (P5-T2).  The proofs here were written by an assistant of the Theoretical Research
Division from the coordinator's statements and plan, and reviewed by the coordinator.

Sites are linearly ordered.  A set `T` is a threshold set of `D` (`IsThreshold D T`) if `T ∉ D`
and `T` without its first site is in `D` (`isThreshold_iff_of_nonempty`); the empty set is a
threshold set iff `∅ ∉ D` (`isThreshold_empty_iff`), which for a down-closed family means that
the family has no members at all.

## Part A: the remainder identity

* `downClosed_remainder_identity_mixConfig`, `downClosed_remainder_identity` — for every function
  `g`, down-closed family `D`, reference `x₀` and configuration `y`,
  `g y - ∑_{U ⊆ supp x₀ y, U ∈ D} mixedDiff g x₀ U y
    = ∑_{T ⊆ supp x₀ y, T threshold set of D} mixedDiff g z_T T y`,
  where the base point `z_T = remainderBase x₀ y T` equals `y` at the changed sites before every
  site of `T` and the reference `x₀` everywhere else.
* `downClosed_remainder_bound` — hence the error of the expansion over `D` is bounded by a sum of
  *anchored* constants over the threshold sets: it suffices to bound the mixed differences over a
  threshold set `T` at base points that agree with the reference on `T`.
* `isThreshold_card_lt_iff`, `downClosed_remainder_card_lt` — for the family "fewer than `m`
  sites" the threshold sets are the sets of exactly `m` sites, and the general identity is the
  statement of `anchored_remainder_identity_mixConfig`, derived here a second time.
* `downClosed_remainder_witness`, `downClosed_remainder_witness_family`,
  `downClosed_remainder_witness_identity` — on three sites the family of all subsets of `{0, 1}`
  is down-closed, is not of the form "fewer than `m` sites", and has the single threshold set
  `{2}`; on three binary sites the identity then reads
  `g (1,1,1) - ∑_{U ⊆ {0,1}} mixedDiff g (0,0,0) U (1,1,1) = g (1,1,1) - g (1,1,0)`.

Proof of the identity (`downClosed_remainder_identity_mixConfig`): induction over the set `S` of
switched sites in increasing order of the sites, for all functions and all down-closed families
at once.  Let `j` be a site after all sites of `S` and `D_j g z = g (z[j ↦ b j]) - g z`.  The
subsets of `insert j S` are the subsets `U` of `S` and the sets `insert j U`, and
`mixedDiff g x (insert j U) b = mixedDiff (D_j g) x U b` (`mixedDiff_insert_siteDiff`).  So the
left side for `(g, D, insert j S)` is the sum of the left sides for `(g, D, S)` and for
`(D_j g, D', S)` with the family `D' U = D (insert j U)`, which is down-closed again.  On the
right side, if `∅ ∈ D`, the threshold sets of `D` without `j` are nonempty, so their base points
do not change (`sitesBefore_insert_of_subset`), and `insert j T` is a threshold set of `D` iff
`T` is a threshold set of `D'` (`isThreshold_insert_iff`), with the same base point
(`sitesBefore_insert_insert`).  A family without members — the case `∅ ∉ D` — is treated
directly (`downClosed_remainder_of_forall_not`): nothing is subtracted and the only threshold set
is `∅`.

Informally, by Möbius inversion (`sum_mixedDiff_powerset`) the left side is the sum of the mixed
differences over the sets `U ∉ D`; every such set has exactly one final segment, in the order of
the sites, that is a threshold set `T`, and the mixed differences over the sets with the final
segment `T` add up to the term of `T`.  This regrouping is not formalised here; the induction
above replaces it.

## Part B: a mixed difference in an arbitrary context

* `mixedDiff_congr_target`, `mixedDiff_update_sub`, `mixedDiff_mixedDiff_singleton` — a mixed
  difference over `T` depends on the target states on `T` only, and changing the base point at a
  site `j ∉ T` changes it by a mixed difference over `insert j T`.
* `mixedDiff_context_identity` — for a context `z` that agrees with the reference `x₀` on `T`,
  the mixed difference over `T` at `z` minus the one at `x₀` is the sum over the sites `j` at
  which `z` differs from `x₀` of a mixed difference over `insert j T` at a base point that agrees
  with `x₀` on `insert j T` (the order-one case of `anchored_remainder_identity`, applied to
  `u ↦ mixedDiff g u T y`).
* `mixedDiff_context_sub_bound`, `mixedDiff_context_bound` — hence, with anchored constants
  `c (insert j T)` for the mixed differences over the sets `insert j T`,
  `|mixedDiff g z T y - mixedDiff g x₀ T y| ≤ ∑_{j ∈ supp x₀ z} c (insert j T)`, and so
  `|mixedDiff g z T y| ≤ |mixedDiff g x₀ T y| + ∑_{j ∈ supp x₀ z} c (insert j T)`.
-/

namespace MetricChain

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-! ### Threshold sets of a family of sets of sites -/

/-- **Threshold sets** of a family `D` of sets of sites: `T` is not in `D`, and `T` without its
first site is in `D`.  For `T = ∅` the second clause is empty: `∅` is a threshold set iff
`∅ ∉ D`. -/
def IsThreshold [LinearOrder ι] [DecidableEq ι] (D : Finset ι → Prop) (T : Finset ι) : Prop :=
  ¬ D T ∧ ∀ t ∈ T, (∀ s ∈ T, t ≤ s) → D (T.erase t)

/-- Being a threshold set of a decidable family is decidable. -/
instance IsThreshold.decidablePred [LinearOrder ι] [DecidableEq ι] (D : Finset ι → Prop)
    [DecidablePred D] : DecidablePred (IsThreshold D) := fun T =>
  inferInstanceAs (Decidable (¬ D T ∧ ∀ t ∈ T, (∀ s ∈ T, t ≤ s) → D (T.erase t)))

/-- The empty set is a threshold set iff it does not belong to the family. -/
theorem isThreshold_empty_iff [DecidableEq ι] [LinearOrder ι] (D : Finset ι → Prop) :
    IsThreshold D ∅ ↔ ¬ D ∅ :=
  ⟨fun h => h.1, fun h => ⟨h, fun t ht => absurd ht (Finset.notMem_empty t)⟩⟩

/-- A nonempty set is a threshold set iff it does not belong to the family and the set without
its first site does. -/
theorem isThreshold_iff_of_nonempty [DecidableEq ι] [LinearOrder ι] (D : Finset ι → Prop)
    {T : Finset ι} (hT : T.Nonempty) :
    IsThreshold D T ↔ ¬ D T ∧ D (T.erase (T.min' hT)) := by
  unfold IsThreshold
  refine and_congr Iff.rfl
    ⟨fun h => h _ (T.min'_mem hT) fun s hs => T.min'_le s hs, fun h t ht hmin => ?_⟩
  have ht' : t = T.min' hT := le_antisymm (hmin _ (T.min'_mem hT)) (T.min'_le t ht)
  rw [ht']
  exact h

/-- A family without members has the single threshold set `∅`. -/
theorem isThreshold_iff_eq_empty [DecidableEq ι] [LinearOrder ι] {D : Finset ι → Prop}
    (hD : ∀ U, ¬ D U) (T : Finset ι) : IsThreshold D T ↔ T = ∅ := by
  constructor
  · intro h
    by_contra hne
    exact hD _ ((isThreshold_iff_of_nonempty D (Finset.nonempty_iff_ne_empty.mpr hne)).mp h).2
  · intro hT
    rw [hT]
    exact (isThreshold_empty_iff D).mpr (hD ∅)

/-- **Threshold sets that contain a new last site.**  Let `j` be a site after all sites of `S` and
let `D` contain the empty set.  For `T ⊆ S` the set `insert j T` is a threshold set of `D` iff
`T` is a threshold set of the family `U ↦ D (insert j U)`. -/
theorem isThreshold_insert_iff [DecidableEq ι] [LinearOrder ι] {D : Finset ι → Prop} (h0 : D ∅)
    {S T : Finset ι} {j : ι} (hj : ∀ i ∈ S, i < j) (hTS : T ⊆ S) :
    IsThreshold D (insert j T) ↔ IsThreshold (fun U => D (insert j U)) T := by
  have hjT : j ∉ T := fun h => lt_irrefl j (hj j (hTS h))
  unfold IsThreshold
  refine and_congr Iff.rfl ⟨fun h t ht hmin => ?_, fun h t ht hmin => ?_⟩
  · -- a first site `t` of `T` is the first site of `insert j T`
    have htj : t < j := hj t (hTS ht)
    have h' := h t (Finset.mem_insert_of_mem ht) fun s hs => by
      rcases Finset.mem_insert.mp hs with hsj | hsT
      · rw [hsj]
        exact htj.le
      · exact hmin s hsT
    rwa [Finset.erase_insert_of_ne htj.ne'] at h'
  · rcases Finset.mem_insert.mp ht with htj | htT
    · -- `j` is the first site of `insert j T` only if `T = ∅`; then `∅ ∈ D` is needed
      have hT : T = ∅ := by
        by_contra hne
        obtain ⟨s, hs⟩ := Finset.nonempty_iff_ne_empty.mpr hne
        have hle := hmin s (Finset.mem_insert_of_mem hs)
        rw [htj] at hle
        exact absurd hle (not_le.mpr (hj s (hTS hs)))
      rw [htj, Finset.erase_insert hjT, hT]
      exact h0
    · have htj : t < j := hj t (hTS htT)
      rw [Finset.erase_insert_of_ne htj.ne']
      exact h t htT fun s hs => hmin s (Finset.mem_insert_of_mem hs)

/-- For the family "fewer than `m` sites" the threshold sets are the sets of exactly `m` sites. -/
theorem isThreshold_card_lt_iff [DecidableEq ι] [LinearOrder ι] (m : ℕ) (T : Finset ι) :
    IsThreshold (fun U : Finset ι => U.card < m) T ↔ T.card = m := by
  unfold IsThreshold
  beta_reduce
  constructor
  · rintro ⟨h1, h2⟩
    rcases T.eq_empty_or_nonempty with hT | hne
    · rw [hT, Finset.card_empty] at h1 ⊢
      omega
    · have h3 := h2 (T.min' hne) (Finset.min'_mem T hne) fun s hs => Finset.min'_le T s hs
      rw [Finset.card_erase_of_mem (Finset.min'_mem T hne)] at h3
      have hpos : 0 < T.card := Finset.card_pos.mpr hne
      omega
  · intro h
    refine ⟨by omega, fun t ht _ => ?_⟩
    rw [Finset.card_erase_of_mem ht]
    have hpos : 0 < T.card := Finset.card_pos.mpr ⟨t, ht⟩
    omega

/-! ### Part A: the remainder identity -/

/-- A sum over the subsets of `insert j S` with a property `p`: the subsets `T` of `S` with `p T`,
and the sets `insert j T` with `p (insert j T)`. -/
theorem sum_powerset_insert_filter {α : Type*} [DecidableEq α] (p : Finset α → Prop)
    [DecidablePred p] (f : Finset α → ℝ) {j : α} {S : Finset α} (hj : j ∉ S) :
    ∑ T ∈ (insert j S).powerset.filter p, f T =
      ∑ T ∈ S.powerset.filter p, f T +
        ∑ T ∈ S.powerset.filter (fun T => p (insert j T)), f (insert j T) := by
  rw [Finset.sum_filter, Finset.sum_filter, Finset.sum_filter, Finset.sum_powerset_insert hj]

/-- **The identity for a family without members.**  Nothing is subtracted, the only threshold set
is `∅`, and its term is the value at the configuration with all sites of `S` switched. -/
theorem downClosed_remainder_of_forall_not [DecidableEq ι] [LinearOrder ι] (b : ∀ i, σ i)
    (S : Finset ι) (g : (∀ i, σ i) → ℝ) (D : Finset ι → Prop) [DecidablePred D]
    (hD : ∀ U, ¬ D U) (x : ∀ i, σ i) :
    g (mixConfig x b S) - ∑ U ∈ S.powerset.filter D, mixedDiff g x U b =
      ∑ T ∈ S.powerset.filter (IsThreshold D),
        mixedDiff g (mixConfig x b (sitesBefore S T)) T b := by
  have h1 : S.powerset.filter D = ∅ := Finset.filter_false_of_mem fun U _ => hD U
  have h2 : S.powerset.filter (IsThreshold D) = {∅} := by
    ext T
    rw [Finset.mem_filter, Finset.mem_powerset, Finset.mem_singleton,
      isThreshold_iff_eq_empty hD]
    exact ⟨fun h => h.2, fun h => ⟨h ▸ Finset.empty_subset S, h⟩⟩
  rw [h1, h2, Finset.sum_empty, sub_zero, Finset.sum_singleton, mixedDiff_empty,
    sitesBefore_empty]

/-- **Remainder identity for a down-closed family, after switching the sites of `S`.**  Let `D` be
a down-closed family of sets of sites.  The value at the configuration with the sites of `S`
switched, minus the mixed differences at `x` over the subsets of `S` that belong to `D`, is the
sum over the threshold sets `T ⊆ S` of `D` of the mixed difference over `T` at the base point in
which the sites of `S` before every site of `T` are already switched. -/
theorem downClosed_remainder_identity_mixConfig [DecidableEq ι] [LinearOrder ι] (b : ∀ i, σ i)
    (S : Finset ι) :
    ∀ (g : (∀ i, σ i) → ℝ) (D : Finset ι → Prop) [DecidablePred D],
      (∀ U V, V ⊆ U → D U → D V) → ∀ x : ∀ i, σ i,
      g (mixConfig x b S) - ∑ U ∈ S.powerset.filter D, mixedDiff g x U b =
        ∑ T ∈ S.powerset.filter (IsThreshold D),
          mixedDiff g (mixConfig x b (sitesBefore S T)) T b := by
  refine Finset.induction_on_max S ?_ ?_
  · intro g D _ hD x
    by_cases h0 : D ∅
    · -- no site: the member `∅` gives `g x`, and there is no threshold set
      have h1 : (∅ : Finset ι).powerset.filter D = {∅} := by
        rw [Finset.powerset_empty, Finset.filter_true_of_mem]
        intro T hT
        rw [Finset.mem_singleton.mp hT]
        exact h0
      have h2 : (∅ : Finset ι).powerset.filter (IsThreshold D) = ∅ := by
        rw [Finset.powerset_empty]
        refine Finset.filter_false_of_mem fun T hT hthr => ?_
        rw [Finset.mem_singleton.mp hT] at hthr
        exact hthr.1 h0
      rw [h1, h2, Finset.sum_singleton, Finset.sum_empty, mixedDiff_empty, mixConfig_empty,
        sub_self]
    · exact downClosed_remainder_of_forall_not b ∅ g D
        (fun U hU => h0 (hD U ∅ (Finset.empty_subset U) hU)) x
  · intro j S hj ihS g D _ hD x
    by_cases h0 : D ∅
    · have hjS : j ∉ S := fun h => lt_irrefl j (hj j h)
      -- the induction hypothesis for `(g, D)` and for the site difference with `U ↦ D (insert j U)`
      have e1 := ihS g D hD x
      have e2 := ihS (fun z => g (Function.update z j (b j)) - g z) (fun U => D (insert j U))
        (fun U V hVU hU => hD (insert j U) (insert j V) (Finset.insert_subset_insert j hVU) hU) x
      beta_reduce at e2
      -- the members of `D` among the subsets of `insert j S`
      have hsum : ∑ U ∈ (insert j S).powerset.filter D, mixedDiff g x U b =
          ∑ U ∈ S.powerset.filter D, mixedDiff g x U b +
            ∑ U ∈ S.powerset.filter (fun U => D (insert j U)),
              mixedDiff (fun z => g (Function.update z j (b j)) - g z) x U b := by
        rw [sum_powerset_insert_filter D _ hjS]
        congr 1
        refine Finset.sum_congr rfl fun U hU => ?_
        exact mixedDiff_insert_siteDiff g x b fun hmem =>
          hjS (Finset.mem_powerset.mp (Finset.mem_filter.mp hU).1 hmem)
      -- the threshold sets of `D` among the subsets of `insert j S`
      have hthr : ∑ T ∈ (insert j S).powerset.filter (IsThreshold D),
          mixedDiff g (mixConfig x b (sitesBefore (insert j S) T)) T b =
          ∑ T ∈ S.powerset.filter (IsThreshold D),
              mixedDiff g (mixConfig x b (sitesBefore S T)) T b +
            ∑ T ∈ S.powerset.filter (IsThreshold fun U => D (insert j U)),
              mixedDiff (fun z => g (Function.update z j (b j)) - g z)
                (mixConfig x b (sitesBefore S T)) T b := by
        rw [sum_powerset_insert_filter (IsThreshold D) _ hjS]
        congr 1
        · refine Finset.sum_congr rfl fun T hT => ?_
          obtain ⟨hTS, hTthr⟩ := Finset.mem_filter.mp hT
          have hne : T.Nonempty := by
            rw [Finset.nonempty_iff_ne_empty]
            intro hT0
            rw [hT0] at hTthr
            exact hTthr.1 h0
          rw [sitesBefore_insert_of_subset hj (Finset.mem_powerset.mp hTS) hne]
        · have hfilter : S.powerset.filter (fun T => IsThreshold D (insert j T)) =
              S.powerset.filter (IsThreshold fun U => D (insert j U)) :=
            Finset.filter_congr fun T hT =>
              isThreshold_insert_iff h0 hj (Finset.mem_powerset.mp hT)
          rw [hfilter]
          refine Finset.sum_congr rfl fun T hT => ?_
          have hjT : j ∉ T := fun h =>
            hjS (Finset.mem_powerset.mp (Finset.mem_filter.mp hT).1 h)
          rw [sitesBefore_insert_insert hj, mixedDiff_insert_siteDiff g _ b hjT]
      rw [hsum, hthr, mixConfig_insert, ← e1, ← e2]
      ring
    · exact downClosed_remainder_of_forall_not b (insert j S) g D
        (fun U hU => h0 (hD U ∅ (Finset.empty_subset U) hU)) x

/-- **Remainder identity for a down-closed family.**  For every function, reference `x₀`,
configuration `y` and down-closed family `D` of sets of sites: the value at `y` minus the mixed
differences at the reference over the sets of changed sites in `D` is the sum, over the threshold
sets `T` of `D` among the changed sites, of the mixed difference over `T` at the base point
`remainderBase x₀ y T`. -/
theorem downClosed_remainder_identity [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ) (D : Finset ι → Prop) [DecidablePred D]
    (hD : ∀ U V, V ⊆ U → D U → D V) (x₀ y : ∀ i, σ i) :
    g y - ∑ U ∈ (supp x₀ y).powerset.filter D, mixedDiff g x₀ U y =
      ∑ T ∈ (supp x₀ y).powerset.filter (IsThreshold D),
        mixedDiff g (remainderBase x₀ y T) T y := by
  have h := downClosed_remainder_identity_mixConfig y (supp x₀ y) g D hD x₀
  rw [mixConfig_supp] at h
  exact h

/-- **Remainder bound for a down-closed family, with anchored constants.**  It suffices to bound
the mixed differences over the threshold sets `T` at base points that agree with the reference on
`T`. -/
theorem downClosed_remainder_bound [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ) (D : Finset ι → Prop) [DecidablePred D]
    (hD : ∀ U V, V ⊆ U → D U → D V) (c : Finset ι → ℝ) (x₀ y : ∀ i, σ i)
    (hc : ∀ T : Finset ι, IsThreshold D T → ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) →
      |mixedDiff g z T y| ≤ c T) :
    |g y - ∑ U ∈ (supp x₀ y).powerset.filter D, mixedDiff g x₀ U y| ≤
      ∑ T ∈ (supp x₀ y).powerset.filter (IsThreshold D), c T := by
  rw [downClosed_remainder_identity g D hD]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun T hT => ?_)
  exact hc T (Finset.mem_filter.mp hT).2 _ fun t ht => remainderBase_on x₀ y T ht

/-- **Consistency with the order-`m` identity.**  For the family "fewer than `m` sites" the
threshold sets are the subsets of `m` sites, and the general identity is the statement of
`anchored_remainder_identity_mixConfig`. -/
theorem downClosed_remainder_card_lt [DecidableEq ι] [LinearOrder ι] (b : ∀ i, σ i) (m : ℕ)
    (g : (∀ i, σ i) → ℝ) (S : Finset ι) (x : ∀ i, σ i) :
    g (mixConfig x b S) - ∑ T ∈ S.powerset.filter (fun T => T.card < m), mixedDiff g x T b =
      ∑ T ∈ S.powersetCard m, mixedDiff g (mixConfig x b (sitesBefore S T)) T b := by
  have h := downClosed_remainder_identity_mixConfig b S g (fun U => U.card < m)
    (fun U V hVU hU => lt_of_le_of_lt (Finset.card_le_card hVU) hU) x
  have hfilter : S.powerset.filter (IsThreshold fun U : Finset ι => U.card < m) =
      S.powersetCard m := by
    rw [Finset.powersetCard_eq_filter]
    exact Finset.filter_congr fun T _ => isThreshold_card_lt_iff m T
  rw [hfilter] at h
  exact h

/-! ### Non-vacuity: a family that is not given by the number of sites

Three sites `0 < 1 < 2` and the family of all subsets of `{0, 1}`. -/

/-- **Witness.**  On three sites, for the family of all subsets of `{0, 1}`: the only threshold
set is `{2}`. -/
theorem downClosed_remainder_witness :
    (univ : Finset (Fin 3)).powerset.filter
      (IsThreshold fun U : Finset (Fin 3) => U ⊆ {0, 1}) = {{2}} := by
  decide

/-- The witness family is down-closed and is not of the form "fewer than `m` sites": it contains
the set `{0, 1}` of two sites and does not contain the set `{2}` of one site. -/
theorem downClosed_remainder_witness_family :
    (∀ U V : Finset (Fin 3), V ⊆ U → U ⊆ {0, 1} → V ⊆ {0, 1}) ∧
      ¬ ∃ m : ℕ, ∀ U : Finset (Fin 3), U ⊆ {0, 1} ↔ U.card < m := by
  refine ⟨fun U V hVU hU => hVU.trans hU, ?_⟩
  rintro ⟨m, hm⟩
  have h1 : ({0, 1} : Finset (Fin 3)).card < m := (hm {0, 1}).mp (Finset.Subset.refl _)
  have h2 : ¬ ({2} : Finset (Fin 3)).card < m := fun h => absurd ((hm {2}).mpr h) (by decide)
  have e1 : ({0, 1} : Finset (Fin 3)).card = 2 := by decide
  have e2 : ({2} : Finset (Fin 3)).card = 1 := by decide
  omega

/-- **The identity at the witness.**  On three binary sites, with the reference `(0,0,0)` and the
configuration `(1,1,1)`: the value minus the mixed differences over the subsets of `{0, 1}` is the
single-site difference at the site `2` at the base point `(1,1,0)`. -/
theorem downClosed_remainder_witness_identity (g : (Fin 3 → Fin 2) → ℝ) :
    g (fun _ => 1) - ∑ U ∈ (univ : Finset (Fin 3)).powerset.filter (fun U => U ⊆ {0, 1}),
        mixedDiff g (fun _ => 0) U (fun _ => 1) = g (fun _ => 1) - g ![1, 1, 0] := by
  have hs : supp (σ := fun _ : Fin 3 => Fin 2) (fun _ => 0) (fun _ => 1) = univ := by
    ext i
    simp [mem_supp]
  have hbase : remainderBase (σ := fun _ : Fin 3 => Fin 2) (fun _ => 0) (fun _ => 1) {2} =
      ![1, 1, 0] := by decide
  have hupd : Function.update (![1, 1, 0] : Fin 3 → Fin 2) 2 1 = fun _ => 1 := by decide
  have h := downClosed_remainder_identity g (fun U : Finset (Fin 3) => U ⊆ {0, 1})
    (fun U V hVU hU => hVU.trans hU) (fun _ => 0) (fun _ => 1)
  rw [hs, downClosed_remainder_witness, Finset.sum_singleton, mixedDiff_singleton, hbase,
    hupd] at h
  exact h

/-! ### Part B: a mixed difference in an arbitrary context -/

/-- A mixed difference over `T` depends on the target states only through their values on `T`. -/
theorem mixedDiff_congr_target [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x : ∀ i, σ i)
    {T : Finset ι} {b b' : ∀ i, σ i} (h : ∀ t ∈ T, b t = b' t) :
    mixedDiff g x T b = mixedDiff g x T b' := by
  unfold mixedDiff
  refine Finset.sum_congr rfl fun U hU => ?_
  have hmix : mixConfig x b U = mixConfig x b' U := by
    funext i
    by_cases hi : i ∈ U
    · simp [mixConfig, hi, h i (Finset.mem_powerset.mp hU hi)]
    · simp [mixConfig, hi]
  rw [hmix]

/-- **A site update commutes with a mixed difference.**  For `j ∉ T`, changing the base point at
the site `j` to the state `v` changes the mixed difference over `T` by the mixed difference over
`insert j T` towards any target `b'` with `b' j = v` that agrees with `y` on `T`. -/
theorem mixedDiff_update_sub [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (u y b' : ∀ i, σ i) {j : ι}
    {T : Finset ι} (hj : j ∉ T) (v : σ j) (hv : b' j = v) (hb : ∀ t ∈ T, b' t = y t) :
    mixedDiff g (Function.update u j v) T y - mixedDiff g u T y =
      mixedDiff g u (insert j T) b' := by
  rw [mixedDiff_insert g u b' hj, hv, mixedDiff_congr_target g _ hb,
    mixedDiff_congr_target g u hb]

/-- **A single-site difference of a mixed difference.**  For `j ∉ T`, the mixed difference over
`{j}` towards `z` of the function `w ↦ mixedDiff g w T y` is the mixed difference of `g` over
`insert j T` towards the target with the state of `z` at `j` and the states of `y` elsewhere. -/
theorem mixedDiff_mixedDiff_singleton [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (u y z : ∀ i, σ i)
    {j : ι} {T : Finset ι} (hj : j ∉ T) :
    mixedDiff (fun w => mixedDiff g w T y) u {j} z =
      mixedDiff g u (insert j T) (Function.update y j (z j)) := by
  have hne : ∀ t ∈ T, t ≠ j := fun t ht h => hj (h ▸ ht)
  rw [mixedDiff_singleton]
  exact mixedDiff_update_sub g u y _ hj (z j) (Function.update_self j (z j) y) fun t ht =>
    Function.update_of_ne (hne t ht) (z j) y

/-- **A mixed difference in an arbitrary context, as an identity.**  Let the context `z` agree
with the reference `x₀` on `T`.  The mixed difference over `T` at `z` minus the one at `x₀` is the
sum, over the sites `j` at which `z` differs from `x₀`, of the mixed difference over `insert j T`
at the base point `remainderBase x₀ z {j}` — the states of `z` at the changed sites before `j`,
the reference elsewhere — towards the state of `z` at `j` and the states of `y` on `T`. -/
theorem mixedDiff_context_identity [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i) (T : Finset ι)
    (z : ∀ i, σ i) (hz : ∀ t ∈ T, z t = x₀ t) (y : ∀ i, σ i) :
    mixedDiff g z T y - mixedDiff g x₀ T y =
      ∑ j ∈ supp x₀ z,
        mixedDiff g (remainderBase x₀ z {j}) (insert j T) (Function.update y j (z j)) := by
  have h := anchored_remainder_identity 1 (fun u => mixedDiff g u T y) x₀ z
  rw [anchoredInterp_one, Finset.powersetCard_one, Finset.sum_map] at h
  refine h.trans (Finset.sum_congr rfl fun j hj => ?_)
  exact mixedDiff_mixedDiff_singleton g _ y z fun hjT => mem_supp.mp hj (hz j hjT)

/-- **A mixed difference in an arbitrary context, difference form.**  Suppose that for every site
`j ∉ T` the mixed differences over `insert j T` are bounded by `c (insert j T)` at the base points
that agree with the reference `x₀` on `insert j T`.  Then the mixed differences over `T` at a
context `z` that agrees with the reference on `T` and at the reference itself differ by at most
the sum of `c (insert j T)` over the sites `j` at which `z` differs from the reference. -/
theorem mixedDiff_context_sub_bound [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i) (T : Finset ι)
    (c : Finset ι → ℝ)
    (hc : ∀ j, j ∉ T → ∀ z b : ∀ i, σ i, (∀ t ∈ insert j T, z t = x₀ t) →
      |mixedDiff g z (insert j T) b| ≤ c (insert j T))
    (z : ∀ i, σ i) (hz : ∀ t ∈ T, z t = x₀ t) (y : ∀ i, σ i) :
    |mixedDiff g z T y - mixedDiff g x₀ T y| ≤ ∑ j ∈ supp x₀ z, c (insert j T) := by
  rw [mixedDiff_context_identity g x₀ T z hz y]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun j hj => ?_)
  refine hc j (fun hjT => mem_supp.mp hj (hz j hjT)) _ _ fun t ht => ?_
  -- the base point is the reference at `j` and at the sites of `T`
  rcases Finset.mem_insert.mp ht with htj | htT
  · rw [htj]
    exact remainderBase_on x₀ z {j} (Finset.mem_singleton_self j)
  · by_cases hlt : ∀ s ∈ ({j} : Finset ι), t < s
    · rw [remainderBase_of_before x₀ z {j} hlt, hz t htT]
    · exact remainderBase_of_not_before x₀ z {j} hlt

/-- **A mixed difference in an arbitrary context.**  Suppose that for every site `j ∉ T` the mixed
differences over `insert j T` are bounded by `c (insert j T)` at the base points that agree with
the reference `x₀` on `insert j T`.  Then at a context `z` that agrees with the reference on `T`
the absolute value of the mixed difference over `T` is at most the absolute value of the one at
the reference plus the sum of `c (insert j T)` over the sites `j` at which `z` differs from the
reference. -/
theorem mixedDiff_context_bound [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i) (T : Finset ι)
    (c : Finset ι → ℝ)
    (hc : ∀ j, j ∉ T → ∀ z b : ∀ i, σ i, (∀ t ∈ insert j T, z t = x₀ t) →
      |mixedDiff g z (insert j T) b| ≤ c (insert j T))
    (z : ∀ i, σ i) (hz : ∀ t ∈ T, z t = x₀ t) (y : ∀ i, σ i) :
    |mixedDiff g z T y| ≤ |mixedDiff g x₀ T y| + ∑ j ∈ supp x₀ z, c (insert j T) := by
  have h := abs_le.mp (mixedDiff_context_sub_bound g x₀ T c hc z hz y)
  exact abs_le.mpr ⟨by linarith [h.1, neg_abs_le (mixedDiff g x₀ T y)],
    by linarith [h.2, le_abs_self (mixedDiff g x₀ T y)]⟩

end MetricChain
