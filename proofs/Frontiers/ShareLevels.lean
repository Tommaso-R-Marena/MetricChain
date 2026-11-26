import Mathlib
import proofs.Frontiers.AnchoredRemainder

/-!
# Shares of the anchored constants at every level

`AnchoredRemainder.lean` bounds the remainder of the anchored expansion of order `m - 1` by the
sum of the anchored constants `c T` over the `m`-subsets `T` of the changed sites
(`anchored_remainder_bound`) and divides every constant equally among the sites of `T`
(`sitePenalty`, `cover_of_equal_shares`).  This file divides the constants among the `k`-subsets
of `T`, for every level `k ≤ m`, and compares the levels.  Everything is elementary counting.

The pair form at `m = 3` is `cover_of_pair_thirds` (`ThirdOrderModel.lean`); the pair and triple forms at
order `m` with a band or window are Lemmas A, A′ and B of the Scientific Discovery Division's workstream P6
(message SCI-MSG-0025), which asked for this machine check (request P6-T1).  The general level `k`, the
comparison of consecutive levels and the window of arbitrary shape are stated here in one form; the proofs
were written by an assistant of the Theoretical Research Division from the coordinator's statements and
reviewed by the coordinator, who added the last section (arbitrary allocations).

The share of a `k`-subset `K` at level `k` is
`levelShare k m c K = ∑_{T ⊇ K, |T| = m} c T / (m choose k)`.
Level `1` at `K = {i}` is the site penalty (`levelShare_one_eq_sitePenalty`, and
`sum_levelShare_one` for the sum over the sites of a set), level `0` at `K = ∅` is the sum of all
constants (`levelShare_zero_empty`), and level `m` at an `m`-subset `T` is `c T`
(`levelShare_self`).

* `sum_levelShare_eq` — counting form: the shares of the `k`-subsets of a set `S` add up to
  `∑_{|T| = m} c T · (|T ∩ S| choose k) / (m choose k)`.
* `cover_of_level_shares` — for `k ≤ m` and constants that are nonnegative on the `m`-subsets the
  level-`k` shares cover the `m`-subsets of every set `S`:
  `∑_{T ⊆ S, |T| = m} c T ≤ ∑_{K ⊆ S, |K| = k} levelShare k m c K`.
* `level_shares_antitone` — for constants that are nonnegative on the `m`-subsets the bound of
  level `k + 1` is at most the bound of level `k`, on every set `S`; the arithmetic is
  `choose_succ_mul_choose_le`:
  `(t choose k + 1) · (m choose k) ≤ (t choose k) · (m choose k + 1)` for `t ≤ m`.
* `sum_superset_levelShare_succ` — double counting: for `k + 1 ≤ m` the level-`(k + 1)` shares of
  the `(k + 1)`-sets that contain a `k`-set `K` add up to `k + 1` times the level-`k` share of `K`.
* `level_window_cover`, `level_window_le` — window push-down.  Let `W` be any decidable set of
  `(k + 1)`-sets (the window).  Keep the level-`(k + 1)` shares inside the window and push the
  share of every `(k + 1)`-set outside the window down to its `k`-subsets in equal parts
  (`pushedShare`).  The result covers the bound of level `k + 1` and is at most the bound of
  level `k`; so for every window and `k + 1 ≤ m` (`cover_of_window_shares` is the first step)
  `∑_{T ⊆ S} c T ≤ (level k + 1 inside the window) + (pushed level k) ≤ (level k)`.
* `anchored_remainder_level_shares`, `anchored_remainder_window_shares` — with anchored constants
  of order `m` the remainder of the anchored expansion is bounded by the level-`k` shares of the
  `k`-subsets of the changed sites (`k ≤ m`), and by the window form (`k + 1 ≤ m`).
* `cover_of_subset_shares`, `anchored_remainder_subset_shares` — the shares need not be equal: any
  nonnegative shares of the `k`-subsets of `T` that add up to at least `c T` cover, so the allocation can
  be chosen for the ensemble at hand.
* `level_shares_witness`, `level_window_witness` — on three sites, with the constant `1` on the
  triple and two changed sites, the bounds of the levels `1`, `2`, `3` are `2/3`, `1/3`, `0`, and
  the window of the pairs that contain the first site gives `1/2`: the levels differ, and a
  window form can lie strictly between two of them.
-/

namespace MetricChain

open Finset

variable {ι : Type*}

/-! ### Level shares -/

/-- The share of a `k`-subset `K` at level `k`: every constant `c T` of an `m`-subset `T ⊇ K` is
divided equally among the `m.choose k` subsets of `T` with `k` elements. -/
noncomputable def levelShare [Fintype ι] [DecidableEq ι] (k m : ℕ) (c : Finset ι → ℝ)
    (K : Finset ι) : ℝ :=
  ∑ T ∈ (univ : Finset ι).powersetCard m, (if K ⊆ T then c T / (m.choose k : ℝ) else 0)

/-- Level `1` is the site penalty of equal shares. -/
theorem levelShare_one_eq_sitePenalty [Fintype ι] [DecidableEq ι] (m : ℕ) (c : Finset ι → ℝ)
    (i : ι) : levelShare 1 m c {i} = sitePenalty m c i := by
  unfold levelShare sitePenalty
  simp only [Finset.singleton_subset_iff, Nat.choose_one_right]

/-- The bound of level `1` on a set `S` is the sum of the site penalties over `S`. -/
theorem sum_levelShare_one [Fintype ι] [DecidableEq ι] (m : ℕ) (c : Finset ι → ℝ)
    (S : Finset ι) :
    ∑ K ∈ S.powersetCard 1, levelShare 1 m c K = ∑ i ∈ S, sitePenalty m c i := by
  rw [Finset.powersetCard_one, Finset.sum_map]
  exact Finset.sum_congr rfl fun i _ => levelShare_one_eq_sitePenalty m c i

/-- Level `0`: the share of the empty set is the sum of the constants of all `m`-subsets. -/
theorem levelShare_zero_empty [Fintype ι] [DecidableEq ι] (m : ℕ) (c : Finset ι → ℝ) :
    levelShare 0 m c ∅ = ∑ T ∈ (univ : Finset ι).powersetCard m, c T := by
  unfold levelShare
  simp

/-- Level `m`: the share of an `m`-subset is its constant. -/
theorem levelShare_self [Fintype ι] [DecidableEq ι] {m : ℕ} (c : Finset ι → ℝ) {T : Finset ι}
    (hT : T.card = m) : levelShare m m c T = c T := by
  unfold levelShare
  rw [Finset.sum_eq_single_of_mem T (Finset.mem_powersetCard.mpr ⟨Finset.subset_univ T, hT⟩)]
  · rw [if_pos (Finset.Subset.refl T), Nat.choose_self, Nat.cast_one, div_one]
  · intro T' hT' hne
    refine if_neg fun hsub => hne ?_
    exact (Finset.eq_of_subset_of_card_le hsub
      ((Finset.mem_powersetCard.mp hT').2.trans hT.symm).le).symm

/-- Shares of constants that are nonnegative on the `m`-subsets are nonnegative. -/
theorem levelShare_nonneg [Fintype ι] [DecidableEq ι] (k : ℕ) {m : ℕ} {c : Finset ι → ℝ}
    (hc : ∀ T : Finset ι, T.card = m → 0 ≤ c T) (K : Finset ι) : 0 ≤ levelShare k m c K := by
  unfold levelShare
  refine Finset.sum_nonneg fun T hT => ?_
  split_ifs
  · exact div_nonneg (hc T (Finset.mem_powersetCard.mp hT).2) (Nat.cast_nonneg _)
  · exact le_rfl

/-- A set with more than `m` elements lies in no `m`-subset: its share vanishes. -/
theorem levelShare_eq_zero_of_lt_card [Fintype ι] [DecidableEq ι] (k : ℕ) {m : ℕ}
    (c : Finset ι → ℝ) {K : Finset ι} (hK : m < K.card) : levelShare k m c K = 0 := by
  unfold levelShare
  refine Finset.sum_eq_zero fun T hT => if_neg fun hKT => ?_
  have hle := Finset.card_le_card hKT
  rw [(Finset.mem_powersetCard.mp hT).2] at hle
  omega

/-! ### The counting form and the cover -/

/-- The `k`-subsets of `S` that lie in `T` are the `k`-subsets of `T ∩ S`. -/
theorem filter_subset_powersetCard [DecidableEq ι] (S T : Finset ι) (k : ℕ) :
    (S.powersetCard k).filter (fun K => K ⊆ T) = (T ∩ S).powersetCard k := by
  ext K
  simp only [Finset.mem_filter, Finset.mem_powersetCard, Finset.subset_inter_iff]
  tauto

/-- **Counting form.**  The level-`k` shares of the `k`-subsets of `S` add up to the constants
`c T` weighted by the fraction of the `k`-subsets of `T` that lie in `S`. -/
theorem sum_levelShare_eq [Fintype ι] [DecidableEq ι] (k m : ℕ) (c : Finset ι → ℝ)
    (S : Finset ι) :
    ∑ K ∈ S.powersetCard k, levelShare k m c K =
      ∑ T ∈ (univ : Finset ι).powersetCard m,
        c T * (((T ∩ S).card.choose k : ℝ) / (m.choose k : ℝ)) := by
  unfold levelShare
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun T _ => ?_
  rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, filter_subset_powersetCard,
    Finset.card_powersetCard]
  ring

/-- **Level shares cover the `m`-subsets.**  For `k ≤ m` and constants that are nonnegative on
the `m`-subsets, the constants of the `m`-subsets of any set `S` add up to at most the level-`k`
shares of the `k`-subsets of `S`. -/
theorem cover_of_level_shares [Fintype ι] [DecidableEq ι] {k m : ℕ} (hk : k ≤ m)
    (c : Finset ι → ℝ) (hc : ∀ T : Finset ι, T.card = m → 0 ≤ c T) (S : Finset ι) :
    ∑ T ∈ S.powersetCard m, c T ≤ ∑ K ∈ S.powersetCard k, levelShare k m c K := by
  have hpos : (0 : ℝ) < (m.choose k : ℝ) := by exact_mod_cast Nat.choose_pos hk
  rw [sum_levelShare_eq]
  calc ∑ T ∈ S.powersetCard m, c T
      = ∑ T ∈ S.powersetCard m, c T * (((T ∩ S).card.choose k : ℝ) / (m.choose k : ℝ)) := by
        refine Finset.sum_congr rfl fun T hT => ?_
        obtain ⟨hTS, hTc⟩ := Finset.mem_powersetCard.mp hT
        rw [Finset.inter_eq_left.mpr hTS, hTc, div_self hpos.ne', mul_one]
    _ ≤ ∑ T ∈ (univ : Finset ι).powersetCard m,
          c T * (((T ∩ S).card.choose k : ℝ) / (m.choose k : ℝ)) := by
        refine Finset.sum_le_sum_of_subset_of_nonneg
          (Finset.powersetCard_mono (Finset.subset_univ S)) fun T hT _ => ?_
        exact mul_nonneg (hc T (Finset.mem_powersetCard.mp hT).2)
          (div_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))

/-! ### The levels are ordered -/

/-- For `t ≤ m` the fraction `(t choose k) / (m choose k)` does not increase with `k`, in
cross-multiplied form. -/
theorem choose_succ_mul_choose_le {t m : ℕ} (htm : t ≤ m) (k : ℕ) :
    t.choose (k + 1) * m.choose k ≤ t.choose k * m.choose (k + 1) := by
  have h1 := Nat.choose_succ_right_eq t k
  have h2 := Nat.choose_succ_right_eq m k
  have h3 : t - k ≤ m - k := Nat.sub_le_sub_right htm k
  refine Nat.le_of_mul_le_mul_right ?_ (Nat.succ_pos k)
  calc t.choose (k + 1) * m.choose k * (k + 1)
      = t.choose (k + 1) * (k + 1) * m.choose k := by ring
    _ = t.choose k * (t - k) * m.choose k := by rw [h1]
    _ ≤ t.choose k * (m - k) * m.choose k := by gcongr
    _ = t.choose k * (m.choose k * (m - k)) := by ring
    _ = t.choose k * (m.choose (k + 1) * (k + 1)) := by rw [h2]
    _ = t.choose k * m.choose (k + 1) * (k + 1) := by ring

/-- **The levels are ordered.**  For constants that are nonnegative on the `m`-subsets the bound
of level `k + 1` is at most the bound of level `k`, on every set `S`.  (No hypothesis on `k`: for
`k ≥ m` the left side vanishes, since a set with `k + 1 > m` elements lies in no `m`-subset.) -/
theorem level_shares_antitone [Fintype ι] [DecidableEq ι] (k m : ℕ) (c : Finset ι → ℝ)
    (hc : ∀ T : Finset ι, T.card = m → 0 ≤ c T) (S : Finset ι) :
    ∑ K ∈ S.powersetCard (k + 1), levelShare (k + 1) m c K ≤
      ∑ K ∈ S.powersetCard k, levelShare k m c K := by
  rcases Nat.lt_or_ge m (k + 1) with hlt | hk
  · have hzero : ∑ K ∈ S.powersetCard (k + 1), levelShare (k + 1) m c K = 0 :=
      Finset.sum_eq_zero fun K hK => levelShare_eq_zero_of_lt_card (k + 1) c
        (by rw [(Finset.mem_powersetCard.mp hK).2]; exact hlt)
    rw [hzero]
    exact Finset.sum_nonneg fun K _ => levelShare_nonneg k hc K
  · have hpos1 : (0 : ℝ) < (m.choose (k + 1) : ℝ) := by exact_mod_cast Nat.choose_pos hk
    have hpos0 : (0 : ℝ) < (m.choose k : ℝ) := by
      exact_mod_cast Nat.choose_pos (Nat.le_of_succ_le hk)
    rw [sum_levelShare_eq, sum_levelShare_eq]
    refine Finset.sum_le_sum fun T hT => ?_
    have hTc : T.card = m := (Finset.mem_powersetCard.mp hT).2
    have hle : (T ∩ S).card ≤ m := hTc ▸ Finset.card_le_card Finset.inter_subset_left
    refine mul_le_mul_of_nonneg_left ?_ (hc T hTc)
    rw [div_le_div_iff₀ hpos1 hpos0]
    exact_mod_cast choose_succ_mul_choose_le hle k

/-! ### Double counting between consecutive levels -/

/-- Between a `k`-set `K` and an `m`-set `T ⊇ K` there are `m - k` sets with `k + 1` elements:
the sets `insert t K` with `t ∈ T \ K`. -/
theorem card_filter_powersetCard_succ_between [Fintype ι] [DecidableEq ι] {k m : ℕ}
    {K T : Finset ι} (hK : K.card = k) (hT : T.card = m) (hKT : K ⊆ T) :
    (((univ : Finset ι).powersetCard (k + 1)).filter (fun K' => K ⊆ K' ∧ K' ⊆ T)).card =
      m - k := by
  have himg : ((univ : Finset ι).powersetCard (k + 1)).filter (fun K' => K ⊆ K' ∧ K' ⊆ T) =
      (T \ K).image (fun t => insert t K) := by
    ext K'
    simp only [Finset.mem_filter, Finset.mem_powersetCard, Finset.subset_univ, true_and,
      Finset.mem_image, Finset.mem_sdiff]
    constructor
    · rintro ⟨hc, hKK', hK'T⟩
      obtain ⟨a, ha, rfl⟩ := Finset.exists_eq_insert_iff.mpr ⟨hKK', by rw [hK, hc]⟩
      exact ⟨a, ⟨hK'T (Finset.mem_insert_self a K), ha⟩, rfl⟩
    · rintro ⟨a, ⟨haT, haK⟩, rfl⟩
      exact ⟨by rw [Finset.card_insert_of_notMem haK, hK], Finset.subset_insert a K,
        Finset.insert_subset haT hKT⟩
  rw [himg, Finset.card_image_of_injOn, Finset.card_sdiff_of_subset hKT, hT, hK]
  intro a ha b _ hab
  exact (Finset.insert_inj (Finset.mem_sdiff.mp (Finset.mem_coe.mp ha)).2).mp hab

/-- **Double counting.**  For `k + 1 ≤ m` the level-`(k + 1)` shares of the `(k + 1)`-sets that
contain a `k`-set `K` add up to `k + 1` times the level-`k` share of `K`.  (No sign hypothesis.) -/
theorem sum_superset_levelShare_succ [Fintype ι] [DecidableEq ι] {k m : ℕ} (hk : k + 1 ≤ m)
    (c : Finset ι → ℝ) {K : Finset ι} (hK : K.card = k) :
    ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
        (if K ⊆ K' then levelShare (k + 1) m c K' else 0) =
      ((k : ℝ) + 1) * levelShare k m c K := by
  have hpos1 : (0 : ℝ) < (m.choose (k + 1) : ℝ) := by exact_mod_cast Nat.choose_pos hk
  have hpos0 : (0 : ℝ) < (m.choose k : ℝ) := by
    exact_mod_cast Nat.choose_pos (Nat.le_of_succ_le hk)
  have hchoose : ((m - k : ℕ) : ℝ) / (m.choose (k + 1) : ℝ) =
      ((k : ℝ) + 1) / (m.choose k : ℝ) := by
    have h : (m.choose (k + 1) : ℝ) * ((k : ℝ) + 1) = (m.choose k : ℝ) * ((m - k : ℕ) : ℝ) := by
      exact_mod_cast Nat.choose_succ_right_eq m k
    rw [div_eq_div_iff hpos1.ne' hpos0.ne']
    linear_combination (-1 : ℝ) * h
  calc ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
        (if K ⊆ K' then levelShare (k + 1) m c K' else 0)
      = ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
          ∑ T ∈ (univ : Finset ι).powersetCard m,
            (if K ⊆ K' ∧ K' ⊆ T then c T / (m.choose (k + 1) : ℝ) else 0) := by
        refine Finset.sum_congr rfl fun K' _ => ?_
        unfold levelShare
        by_cases h : K ⊆ K' <;> simp [h]
    _ = ∑ T ∈ (univ : Finset ι).powersetCard m,
          ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
            (if K ⊆ K' ∧ K' ⊆ T then c T / (m.choose (k + 1) : ℝ) else 0) := Finset.sum_comm
    _ = ∑ T ∈ (univ : Finset ι).powersetCard m,
          (if K ⊆ T then ((k : ℝ) + 1) * (c T / (m.choose k : ℝ)) else 0) := by
        refine Finset.sum_congr rfl fun T hT => ?_
        have hTc : T.card = m := (Finset.mem_powersetCard.mp hT).2
        rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
        by_cases hKT : K ⊆ T
        · rw [card_filter_powersetCard_succ_between hK hTc hKT, if_pos hKT]
          calc ((m - k : ℕ) : ℝ) * (c T / (m.choose (k + 1) : ℝ))
              = c T * (((m - k : ℕ) : ℝ) / (m.choose (k + 1) : ℝ)) := by ring
            _ = c T * (((k : ℝ) + 1) / (m.choose k : ℝ)) := by rw [hchoose]
            _ = ((k : ℝ) + 1) * (c T / (m.choose k : ℝ)) := by ring
        · have hempty : ((univ : Finset ι).powersetCard (k + 1)).filter
              (fun K' => K ⊆ K' ∧ K' ⊆ T) = ∅ :=
            Finset.filter_false_of_mem fun K' _ h => hKT (h.1.trans h.2)
          rw [hempty, if_neg hKT, Finset.card_empty, Nat.cast_zero, zero_mul]
    _ = ((k : ℝ) + 1) * levelShare k m c K := by
        unfold levelShare
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun T _ => ?_
        rw [mul_ite, mul_zero]

/-! ### Window push-down -/

/-- The pushed share of a `k`-set `K` for the window `W`: every `(k + 1)`-set `K' ⊇ K` outside
the window gives each of its `k + 1` subsets with `k` elements an equal part of its level-`(k + 1)`
share. -/
noncomputable def pushedShare [Fintype ι] [DecidableEq ι] (k m : ℕ) (c : Finset ι → ℝ)
    (W : Finset ι → Prop) [DecidablePred W] (K : Finset ι) : ℝ :=
  ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
    (if K ⊆ K' ∧ ¬ W K' then levelShare (k + 1) m c K' / ((k : ℝ) + 1) else 0)

/-- **Pushing down one level.**  For `f ≥ 0` on the `(k + 1)`-sets and a decidable property `P`:
the values of `f` on the `(k + 1)`-subsets of `S` with `P` add up to at most what the `k`-subsets
of `S` receive when every `(k + 1)`-set with `P` gives each of its `k`-subsets an equal part. -/
theorem sum_filter_powersetCard_succ_le [Fintype ι] [DecidableEq ι] (k : ℕ) (f : Finset ι → ℝ)
    (hf : ∀ K' : Finset ι, K'.card = k + 1 → 0 ≤ f K') (P : Finset ι → Prop) [DecidablePred P]
    (S : Finset ι) :
    ∑ K' ∈ (S.powersetCard (k + 1)).filter P, f K' ≤
      ∑ K ∈ S.powersetCard k, ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
        (if K ⊆ K' ∧ P K' then f K' / ((k : ℝ) + 1) else 0) := by
  have hk0 : ((k : ℝ) + 1) ≠ 0 := by positivity
  calc ∑ K' ∈ (S.powersetCard (k + 1)).filter P, f K'
      = ∑ K' ∈ S.powersetCard (k + 1), (if P K' then f K' else 0) := Finset.sum_filter _ _
    _ = ∑ K' ∈ S.powersetCard (k + 1), ∑ K ∈ S.powersetCard k,
          (if K ⊆ K' ∧ P K' then f K' / ((k : ℝ) + 1) else 0) := by
        refine Finset.sum_congr rfl fun K' hK' => ?_
        obtain ⟨hK'S, hK'c⟩ := Finset.mem_powersetCard.mp hK'
        by_cases hP : P K'
        · simp only [hP, and_true, ↓reduceIte]
          rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, filter_subset_powersetCard,
            Finset.inter_eq_left.mpr hK'S, Finset.card_powersetCard, hK'c,
            Nat.choose_succ_self_right, Nat.cast_add_one, mul_div_cancel₀ _ hk0]
        · simp [hP]
    _ ≤ ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1), ∑ K ∈ S.powersetCard k,
          (if K ⊆ K' ∧ P K' then f K' / ((k : ℝ) + 1) else 0) := by
        refine Finset.sum_le_sum_of_subset_of_nonneg
          (Finset.powersetCard_mono (Finset.subset_univ S)) fun K' hK' _ => ?_
        refine Finset.sum_nonneg fun K _ => ?_
        split_ifs
        · exact div_nonneg (hf K' (Finset.mem_powersetCard.mp hK').2) (by positivity)
        · exact le_rfl
    _ = ∑ K ∈ S.powersetCard k, ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
          (if K ⊆ K' ∧ P K' then f K' / ((k : ℝ) + 1) else 0) := Finset.sum_comm

/-- Above a `k`-set `K`, for `k + 1 ≤ m`: the equal parts of the level-`(k + 1)` shares inside
the window and the pushed share make up the level-`k` share of `K`. -/
theorem sum_superset_window_add_pushedShare [Fintype ι] [DecidableEq ι] {k m : ℕ}
    (hk : k + 1 ≤ m) (c : Finset ι → ℝ) (W : Finset ι → Prop) [DecidablePred W] {K : Finset ι}
    (hK : K.card = k) :
    ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
        (if K ⊆ K' ∧ W K' then levelShare (k + 1) m c K' / ((k : ℝ) + 1) else 0) +
      pushedShare k m c W K = levelShare k m c K := by
  have hk0 : ((k : ℝ) + 1) ≠ 0 := by positivity
  have hsplit : ∀ K' ∈ (univ : Finset ι).powersetCard (k + 1),
      (if K ⊆ K' ∧ W K' then levelShare (k + 1) m c K' / ((k : ℝ) + 1) else 0) +
        (if K ⊆ K' ∧ ¬ W K' then levelShare (k + 1) m c K' / ((k : ℝ) + 1) else 0) =
      (if K ⊆ K' then levelShare (k + 1) m c K' else 0) / ((k : ℝ) + 1) := by
    intro K' _
    by_cases h1 : K ⊆ K' <;> by_cases h2 : W K' <;> simp [h1, h2]
  unfold pushedShare
  rw [← Finset.sum_add_distrib, Finset.sum_congr rfl hsplit, ← Finset.sum_div,
    sum_superset_levelShare_succ hk c hK, mul_div_cancel_left₀ _ hk0]

/-- **The window form covers level `k + 1`.**  For constants that are nonnegative on the
`m`-subsets and every window `W`: the bound of level `k + 1` on `S` is at most the shares of
level `k + 1` inside the window plus the pushed shares of the `k`-subsets of `S`. -/
theorem level_window_cover [Fintype ι] [DecidableEq ι] (k m : ℕ) (c : Finset ι → ℝ)
    (hc : ∀ T : Finset ι, T.card = m → 0 ≤ c T) (W : Finset ι → Prop) [DecidablePred W]
    (S : Finset ι) :
    ∑ K' ∈ S.powersetCard (k + 1), levelShare (k + 1) m c K' ≤
      ∑ K' ∈ (S.powersetCard (k + 1)).filter W, levelShare (k + 1) m c K' +
        ∑ K ∈ S.powersetCard k, pushedShare k m c W K :=
  calc ∑ K' ∈ S.powersetCard (k + 1), levelShare (k + 1) m c K'
      = ∑ K' ∈ (S.powersetCard (k + 1)).filter W, levelShare (k + 1) m c K' +
          ∑ K' ∈ (S.powersetCard (k + 1)).filter (fun K' => ¬ W K'),
            levelShare (k + 1) m c K' :=
        (Finset.sum_filter_add_sum_filter_not _ _ _).symm
    _ ≤ ∑ K' ∈ (S.powersetCard (k + 1)).filter W, levelShare (k + 1) m c K' +
          ∑ K ∈ S.powersetCard k, pushedShare k m c W K :=
        add_le_add le_rfl (sum_filter_powersetCard_succ_le k _
          (fun K' _ => levelShare_nonneg (k + 1) hc K') (fun K' => ¬ W K') S)

/-- **The window form is at most level `k`.**  For constants that are nonnegative on the
`m`-subsets and every window `W`: the shares of level `k + 1` inside the window plus the pushed
shares of the `k`-subsets of `S` are at most the bound of level `k` on `S`.  (No hypothesis on
`k`: for `k ≥ m` the left side vanishes.) -/
theorem level_window_le [Fintype ι] [DecidableEq ι] (k m : ℕ) (c : Finset ι → ℝ)
    (hc : ∀ T : Finset ι, T.card = m → 0 ≤ c T) (W : Finset ι → Prop) [DecidablePred W]
    (S : Finset ι) :
    ∑ K' ∈ (S.powersetCard (k + 1)).filter W, levelShare (k + 1) m c K' +
        ∑ K ∈ S.powersetCard k, pushedShare k m c W K ≤
      ∑ K ∈ S.powersetCard k, levelShare k m c K := by
  rcases Nat.lt_or_ge m (k + 1) with hlt | hk
  · have hzero : ∀ K' ∈ (univ : Finset ι).powersetCard (k + 1),
        levelShare (k + 1) m c K' = 0 := fun K' hK' =>
      levelShare_eq_zero_of_lt_card (k + 1) c
        (by rw [(Finset.mem_powersetCard.mp hK').2]; exact hlt)
    have h1 : ∑ K' ∈ (S.powersetCard (k + 1)).filter W, levelShare (k + 1) m c K' = 0 :=
      Finset.sum_eq_zero fun K' hK' => hzero K'
        (Finset.powersetCard_mono (Finset.subset_univ S) (Finset.mem_filter.mp hK').1)
    have h2 : ∑ K ∈ S.powersetCard k, pushedShare k m c W K = 0 := by
      refine Finset.sum_eq_zero fun K _ => ?_
      unfold pushedShare
      refine Finset.sum_eq_zero fun K' hK' => ?_
      rw [hzero K' hK', zero_div, ite_self]
    rw [h1, h2, add_zero]
    exact Finset.sum_nonneg fun K _ => levelShare_nonneg k hc K
  · calc ∑ K' ∈ (S.powersetCard (k + 1)).filter W, levelShare (k + 1) m c K' +
          ∑ K ∈ S.powersetCard k, pushedShare k m c W K
        ≤ ∑ K ∈ S.powersetCard k, ∑ K' ∈ (univ : Finset ι).powersetCard (k + 1),
            (if K ⊆ K' ∧ W K' then levelShare (k + 1) m c K' / ((k : ℝ) + 1) else 0) +
          ∑ K ∈ S.powersetCard k, pushedShare k m c W K :=
          add_le_add (sum_filter_powersetCard_succ_le k _
            (fun K' _ => levelShare_nonneg (k + 1) hc K') W S) le_rfl
      _ = ∑ K ∈ S.powersetCard k, levelShare k m c K := by
          rw [← Finset.sum_add_distrib]
          exact Finset.sum_congr rfl fun K hK =>
            sum_superset_window_add_pushedShare hk c W (Finset.mem_powersetCard.mp hK).2

/-- **The window form covers the `m`-subsets.**  For `k + 1 ≤ m`, constants that are nonnegative
on the `m`-subsets and every window `W`: the constants of the `m`-subsets of `S` add up to at most
the shares of level `k + 1` inside the window plus the pushed shares of the `k`-subsets of `S`. -/
theorem cover_of_window_shares [Fintype ι] [DecidableEq ι] {k m : ℕ} (hk : k + 1 ≤ m)
    (c : Finset ι → ℝ) (hc : ∀ T : Finset ι, T.card = m → 0 ≤ c T) (W : Finset ι → Prop)
    [DecidablePred W] (S : Finset ι) :
    ∑ T ∈ S.powersetCard m, c T ≤
      ∑ K' ∈ (S.powersetCard (k + 1)).filter W, levelShare (k + 1) m c K' +
        ∑ K ∈ S.powersetCard k, pushedShare k m c W K :=
  (cover_of_level_shares hk c hc S).trans (level_window_cover k m c hc W S)

/-! ### The remainder of the anchored expansion -/

variable {σ : ι → Type*}

/-- **Remainder bound by level shares.**  With anchored constants `c` of order `m` and `k ≤ m`,
the anchored interpolant of order `m - 1` approximates `g` up to the level-`k` shares of the
`k`-subsets of the changed sites.  (No nonnegativity hypothesis: an anchored constant of an
`m`-subset bounds an absolute value.) -/
theorem anchored_remainder_level_shares [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] {k m : ℕ} (hk : k ≤ m) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ)
    (x₀ y : ∀ i, σ i)
    (hc : ∀ T : Finset ι, T.card = m → ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) →
      |mixedDiff g z T y| ≤ c T) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ K ∈ (supp x₀ y).powersetCard k, levelShare k m c K :=
  (anchored_remainder_bound m g c x₀ y hc).trans
    (cover_of_level_shares hk c (fun T hT => (abs_nonneg _).trans (hc T hT x₀ fun _ _ => rfl)) _)

/-- **Remainder bound in window form.**  With anchored constants `c` of order `m`, `k + 1 ≤ m`
and any window `W`: the remainder is at most the level-`(k + 1)` shares of the `(k + 1)`-subsets
of the changed sites inside the window plus the pushed shares of their `k`-subsets. -/
theorem anchored_remainder_window_shares [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] {k m : ℕ} (hk : k + 1 ≤ m) (g : (∀ i, σ i) → ℝ)
    (c : Finset ι → ℝ) (W : Finset ι → Prop) [DecidablePred W] (x₀ y : ∀ i, σ i)
    (hc : ∀ T : Finset ι, T.card = m → ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) →
      |mixedDiff g z T y| ≤ c T) :
    |g y - anchoredInterp m g x₀ y| ≤
      ∑ K' ∈ ((supp x₀ y).powersetCard (k + 1)).filter W, levelShare (k + 1) m c K' +
        ∑ K ∈ (supp x₀ y).powersetCard k, pushedShare k m c W K :=
  (anchored_remainder_bound m g c x₀ y hc).trans
    (cover_of_window_shares hk c (fun T hT => (abs_nonneg _).trans (hc T hT x₀ fun _ _ => rfl))
      W _)

/-! ### Non-vacuity -/

/-- **The levels differ.**  Three sites, the constant `1` on the triple and `0` elsewhere, and
the set `S = {0, 1}` of two changed sites: the bound of level `1` is `2/3`, of level `2` it is
`1/3`, and of level `3` it is `0` (the set `S` has no subset with three elements). -/
theorem level_shares_witness :
    ∑ K ∈ ({0, 1} : Finset (Fin 3)).powersetCard 1,
        levelShare 1 3 (fun T => if T = univ then 1 else 0) K = 2 / 3 ∧
      ∑ K ∈ ({0, 1} : Finset (Fin 3)).powersetCard 2,
        levelShare 2 3 (fun T => if T = univ then 1 else 0) K = 1 / 3 ∧
      ∑ K ∈ ({0, 1} : Finset (Fin 3)).powersetCard 3,
        levelShare 3 3 (fun T => if T = univ then 1 else 0) K = 0 := by
  have h3 : (univ : Finset (Fin 3)).powersetCard 3 = {univ} := by decide
  have hcard : (univ ∩ ({0, 1} : Finset (Fin 3))).card = 2 := by decide
  refine ⟨?_, ?_, ?_⟩ <;>
    rw [sum_levelShare_eq, h3, Finset.sum_singleton, hcard] <;> norm_num [Nat.choose]

/-- **A window form strictly between two levels.**  In the setting of `level_shares_witness`, with
the window of the pairs that contain the site `0`: the pair `{0, 1}` keeps its share `1/3`, the
pair `{1, 2}` lies outside the window and pushes half of its share `1/3` to the site `1`, and the
window form is `1/2` — strictly between `1/3` (level `2`) and `2/3` (level `1`). -/
theorem level_window_witness :
    ∑ K' ∈ (({0, 1} : Finset (Fin 3)).powersetCard 2).filter (fun K' => (0 : Fin 3) ∈ K'),
        levelShare 2 3 (fun T => if T = univ then 1 else 0) K' +
      ∑ K ∈ ({0, 1} : Finset (Fin 3)).powersetCard 1,
        pushedShare 1 3 (fun T => if T = univ then 1 else 0) (fun K' => (0 : Fin 3) ∈ K') K =
      1 / 2 := by
  have h3 : (univ : Finset (Fin 3)).powersetCard 3 = {univ} := by decide
  have hL : ∀ K : Finset (Fin 3),
      levelShare 2 3 (fun T => if T = univ then 1 else 0) K = 1 / 3 := by
    intro K
    unfold levelShare
    rw [h3, Finset.sum_singleton]
    norm_num [Nat.choose]
  have hin : ((({0, 1} : Finset (Fin 3)).powersetCard 2).filter
      (fun K' => (0 : Fin 3) ∈ K')).card = 1 := by decide
  have hpush : ∑ K ∈ ({0, 1} : Finset (Fin 3)).powersetCard 1,
      (((univ : Finset (Fin 3)).powersetCard 2).filter
        (fun K' => K ⊆ K' ∧ ¬ (0 : Fin 3) ∈ K')).card = 1 := by decide
  unfold pushedShare
  simp only [hL, ← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, ← Finset.sum_mul,
    ← Nat.cast_sum, hin, hpush]
  norm_num

/-! ### Arbitrary allocations (coordinator) -/

/-- **Arbitrary shares of level `k` cover the `m`-subsets.**  If every constant `c T` is at most the sum of
nonnegative shares `lam T K` of the `k`-subsets `K` of `T` — not necessarily equal ones — the constants of
the `m`-subsets of any set `S` add up to at most the shares carried by the `k`-subsets of `S`.  (For
`k = 1` this is `cover_of_site_shares_order`; `cover_of_level_shares` is the case of equal shares.) -/
theorem cover_of_subset_shares [Fintype ι] [DecidableEq ι] (k m : ℕ) (c : Finset ι → ℝ)
    (lam : Finset ι → Finset ι → ℝ) (hlam : ∀ T : Finset ι, T.card = m → ∀ K, 0 ≤ lam T K)
    (hshare : ∀ T : Finset ι, T.card = m → c T ≤ ∑ K ∈ T.powersetCard k, lam T K)
    (S : Finset ι) :
    ∑ T ∈ S.powersetCard m, c T ≤
      ∑ K ∈ S.powersetCard k, ∑ T ∈ (univ : Finset ι).powersetCard m,
        (if K ⊆ T then lam T K else 0) := by
  calc ∑ T ∈ S.powersetCard m, c T
      ≤ ∑ T ∈ S.powersetCard m, ∑ K ∈ T.powersetCard k, lam T K :=
        Finset.sum_le_sum fun T hT => hshare T (Finset.mem_powersetCard.mp hT).2
    _ = ∑ T ∈ S.powersetCard m, ∑ K ∈ S.powersetCard k, (if K ⊆ T then lam T K else 0) := by
        refine Finset.sum_congr rfl fun T hT => ?_
        have hTS : T ⊆ S := (Finset.mem_powersetCard.mp hT).1
        rw [← Finset.sum_filter]
        congr 1
        ext K
        simp only [Finset.mem_filter, Finset.mem_powersetCard]
        exact ⟨fun h => ⟨⟨h.1.trans hTS, h.2⟩, h.1⟩, fun h => ⟨h.2, h.1.2⟩⟩
    _ = ∑ K ∈ S.powersetCard k, ∑ T ∈ S.powersetCard m, (if K ⊆ T then lam T K else 0) :=
        Finset.sum_comm
    _ ≤ ∑ K ∈ S.powersetCard k, ∑ T ∈ (univ : Finset ι).powersetCard m,
          (if K ⊆ T then lam T K else 0) := by
        refine Finset.sum_le_sum fun K _ => ?_
        refine Finset.sum_le_sum_of_subset_of_nonneg
          (Finset.powersetCard_mono (Finset.subset_univ S)) fun T hT _ => ?_
        split_ifs
        · exact hlam T (Finset.mem_powersetCard.mp hT).2 K
        · exact le_rfl

/-- **Remainder bound by an arbitrary allocation.**  With anchored constants `c` of order `m` and any
nonnegative shares `lam T K` of the `k`-subsets of every `m`-subset `T` that add up to at least `c T`,
the remainder of the anchored expansion is at most the shares carried by the `k`-subsets of the changed
sites.  The allocation is free: it may be chosen for the ensemble at hand (theory report, Proposition
11.18f). -/
theorem anchored_remainder_subset_shares [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (k : ℕ) {m : ℕ} (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ)
    (lam : Finset ι → Finset ι → ℝ) (hlam : ∀ T : Finset ι, T.card = m → ∀ K, 0 ≤ lam T K)
    (hshare : ∀ T : Finset ι, T.card = m → c T ≤ ∑ K ∈ T.powersetCard k, lam T K)
    (x₀ y : ∀ i, σ i)
    (hc : ∀ T : Finset ι, T.card = m → ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) →
      |mixedDiff g z T y| ≤ c T) :
    |g y - anchoredInterp m g x₀ y| ≤
      ∑ K ∈ (supp x₀ y).powersetCard k, ∑ T ∈ (univ : Finset ι).powersetCard m,
        (if K ⊆ T then lam T K else 0) :=
  (anchored_remainder_bound m g c x₀ y hc).trans (cover_of_subset_shares k m c lam hlam hshare _)

end MetricChain
