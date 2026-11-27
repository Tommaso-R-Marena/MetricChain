import Mathlib
import proofs.Frontiers.HigherOrderEnvelope

/-!
# The remainder of the anchored expansion as an identity, and site penalties of every order

`HigherOrderEnvelope.lean` bounds the remainder of the anchored expansion of order `m - 1` by the
sum of the order-`m` envelope constants over the `m`-subsets of the changed sites
(`higherOrder_remainder`), with constants that are uniform in the base point.  This file proves
the statement behind it as an **identity** and draws the two consequences that a certificate
needs.  The identity, the observation that only anchored base points occur, and the request to
machine-check both are the Scientific Discovery Division's (its workstream P3, Proposition 1 and
the allocation lemma; message SCI-MSG-0020, request P3-T1); the proofs here are ours and follow
the induction of `higherOrder_remainder_mixConfig`.

Sites are linearly ordered.  For sets of sites `T ⊆ S` let `sitesBefore S T` be the sites of `S`
that precede every site of `T` (all of `S` if `T` is empty).

* `anchored_remainder_identity_mixConfig`, `anchored_remainder_identity` — for every function
  `g`, reference `x₀`, configuration `y` and order `m`,
  `g y - anchoredInterp m g x₀ y = ∑_{T ⊆ supp x₀ y, |T| = m} mixedDiff g z_T T y`,
  where the base point `z_T` equals `y` at the changed sites before every site of `T` and the
  reference `x₀` everywhere else (`remainderBase_of_before`, `remainderBase_of_not_before`); in
  particular it equals the reference on `T` and at every site after the first site of `T`.
* `anchored_remainder_bound` — hence the remainder is bounded by the sum of *anchored* constants:
  it suffices to bound the mixed differences over `T` at base points that agree with the
  reference on `T`.  (`higherOrder_remainder` asks for all base points.)
* `cover_of_site_shares_order`, `cover_of_equal_shares` — the allocation lemma at order `m`: if
  every constant `c T` is split among the sites of `T`, the sum of the constants over the
  `m`-subsets of any set `S` is at most the sum over `i ∈ S` of the shares that `i` carries; with
  equal shares the site penalty is `γ i = (1/m) ∑_{T ∋ i} c T`.
* `anchored_remainder_site_penalties` — the two together: `|g y - anchoredInterp m g x₀ y|` is at
  most the sum of the site penalties over the changed sites, so that
  `anchoredInterp m g x₀ ∓ ∑_{i changed} γ i` is a sandwich of `g` by two functions that use the
  values of `g` on the Hamming ball of radius `m - 1` only.
* `anchored_remainder_witness` — on three binary sites the remainder of order three of the triple
  coupling at the configuration `(1,1,1)` is the single mixed difference over all three sites at
  the reference, and equals `1`.
-/

namespace MetricChain

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-! ### The sites before a set -/

/-- The sites of `S` that precede every site of `T`. -/
def sitesBefore [LinearOrder ι] (S T : Finset ι) : Finset ι := S.filter fun i => ∀ t ∈ T, i < t

theorem mem_sitesBefore [LinearOrder ι] {S T : Finset ι} {i : ι} :
    i ∈ sitesBefore S T ↔ i ∈ S ∧ ∀ t ∈ T, i < t := by
  unfold sitesBefore
  exact Finset.mem_filter

/-- Every site precedes every site of the empty set. -/
theorem sitesBefore_empty [LinearOrder ι] (S : Finset ι) : sitesBefore S ∅ = S := by
  ext i
  rw [mem_sitesBefore]
  exact ⟨fun h => h.1, fun h => ⟨h, fun t ht => absurd ht (Finset.notMem_empty t)⟩⟩

/-- A new last site does not precede anything. -/
theorem sitesBefore_insert_of_subset [DecidableEq ι] [LinearOrder ι] {S T : Finset ι} {j : ι}
    (hj : ∀ i ∈ S, i < j) (hTS : T ⊆ S) (hT : T.Nonempty) :
    sitesBefore (insert j S) T = sitesBefore S T := by
  ext i
  rw [mem_sitesBefore, mem_sitesBefore, Finset.mem_insert]
  constructor
  · rintro ⟨hi | hi, h⟩
    · exfalso
      obtain ⟨t, ht⟩ := hT
      subst hi
      exact lt_asymm (h t ht) (hj t (hTS ht))
    · exact ⟨hi, h⟩
  · rintro ⟨hi, h⟩
    exact ⟨Or.inr hi, h⟩

/-- A new last site that is also added to `T` changes nothing: every site of `S` precedes it. -/
theorem sitesBefore_insert_insert [DecidableEq ι] [LinearOrder ι] {S T : Finset ι} {j : ι}
    (hj : ∀ i ∈ S, i < j) : sitesBefore (insert j S) (insert j T) = sitesBefore S T := by
  ext i
  rw [mem_sitesBefore, mem_sitesBefore, Finset.mem_insert]
  constructor
  · rintro ⟨hi | hi, h⟩
    · exfalso
      subst hi
      exact lt_irrefl i (h i (Finset.mem_insert_self i T))
    · exact ⟨hi, fun t ht => h t (Finset.mem_insert_of_mem ht)⟩
  · rintro ⟨hi, h⟩
    refine ⟨Or.inr hi, fun t ht => ?_⟩
    rcases Finset.mem_insert.mp ht with rfl | ht'
    · exact hj i hi
    · exact h t ht'

/-! ### The remainder identity -/

/-- **Remainder identity after switching the sites of `S`.**  The value at the configuration with
the sites of `S` switched, minus the mixed differences at `x` over the subsets of `S` with fewer
than `m` sites, is the sum over the `m`-subsets `T` of `S` of the mixed difference over `T` at
the base point in which the sites of `S` before every site of `T` are already switched. -/
theorem anchored_remainder_identity_mixConfig [DecidableEq ι] [LinearOrder ι] (b : ∀ i, σ i) :
    ∀ (m : ℕ) (g : (∀ i, σ i) → ℝ) (S : Finset ι) (x : ∀ i, σ i),
      g (mixConfig x b S) - ∑ T ∈ S.powerset.filter (fun T => T.card < m), mixedDiff g x T b =
        ∑ T ∈ S.powersetCard m, mixedDiff g (mixConfig x b (sitesBefore S T)) T b := by
  intro m
  induction m with
  | zero =>
    intro g S x
    have h1 : S.powerset.filter (fun T => T.card < 0) = ∅ :=
      Finset.filter_false_of_mem fun T _ => Nat.not_lt_zero _
    rw [h1, Finset.sum_empty, sub_zero, Finset.powersetCard_zero, Finset.sum_singleton,
      mixedDiff_empty, sitesBefore_empty]
  | succ m ih =>
    intro g S
    refine Finset.induction_on_max S ?_ ?_
    · intro x
      have hfilter : (∅ : Finset ι).powerset.filter (fun T => T.card < m + 1) = {∅} := by
        rw [Finset.powerset_empty, Finset.filter_true_of_mem]
        intro T hT
        rw [Finset.mem_singleton.mp hT]
        simp
      have hcard : (∅ : Finset ι).powersetCard (m + 1) = ∅ :=
        Finset.powersetCard_eq_empty.mpr (by simp)
      rw [hfilter, hcard, Finset.sum_singleton, Finset.sum_empty, mixedDiff_empty,
        mixConfig_empty, sub_self]
    · intro j S hj ihS x
      have hjS : j ∉ S := fun h => lt_irrefl j (hj j h)
      have e1 := ihS x
      have e2 := ih (fun z => g (Function.update z j (b j)) - g z) S x
      beta_reduce at e2
      have hsum : ∑ T ∈ (insert j S).powerset.filter (fun T => T.card < m + 1),
          mixedDiff g x T b =
          ∑ T ∈ S.powerset.filter (fun T => T.card < m + 1), mixedDiff g x T b +
            ∑ T ∈ S.powerset.filter (fun T => T.card < m),
              mixedDiff (fun z => g (Function.update z j (b j)) - g z) x T b := by
        rw [sum_powerset_insert_filter_card (fun n => n < m + 1) _ hjS]
        simp only [Nat.add_lt_add_iff_right]
        congr 1
        refine Finset.sum_congr rfl fun T hT => ?_
        exact mixedDiff_insert_siteDiff g x b fun hmem =>
          hjS (Finset.mem_powerset.mp (Finset.mem_filter.mp hT).1 hmem)
      have t1 : ∑ T ∈ S.powersetCard (m + 1),
          mixedDiff g (mixConfig x b (sitesBefore (insert j S) T)) T b =
          ∑ T ∈ S.powersetCard (m + 1), mixedDiff g (mixConfig x b (sitesBefore S T)) T b := by
        refine Finset.sum_congr rfl fun T hT => ?_
        obtain ⟨hTS, hTc⟩ := Finset.mem_powersetCard.mp hT
        have hne : T.Nonempty := Finset.card_pos.mp (by omega)
        rw [sitesBefore_insert_of_subset hj hTS hne]
      have t2 : ∑ T ∈ S.powersetCard m,
          mixedDiff g (mixConfig x b (sitesBefore (insert j S) (insert j T))) (insert j T) b =
          ∑ T ∈ S.powersetCard m,
            mixedDiff (fun z => g (Function.update z j (b j)) - g z)
              (mixConfig x b (sitesBefore S T)) T b := by
        refine Finset.sum_congr rfl fun T hT => ?_
        obtain ⟨hTS, _⟩ := Finset.mem_powersetCard.mp hT
        have hjT : j ∉ T := fun h => hjS (hTS h)
        rw [sitesBefore_insert_insert hj, mixedDiff_insert_siteDiff g _ b hjT]
      rw [hsum, sum_powersetCard_succ_insert _ m hjS, mixConfig_insert, t1, t2, ← e1, ← e2]
      ring

/-- The base point of the remainder term of `T`: the changed sites before every site of `T` carry
the states of `y`, all other sites those of the reference. -/
def remainderBase [Fintype ι] [DecidableEq ι] [LinearOrder ι] [∀ i, DecidableEq (σ i)]
    (x₀ y : ∀ i, σ i) (T : Finset ι) : ∀ i, σ i :=
  mixConfig x₀ y (sitesBefore (supp x₀ y) T)

/-- Before every site of `T` the base point is the configuration itself. -/
theorem remainderBase_of_before [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (x₀ y : ∀ i, σ i) (T : Finset ι) {i : ι} (hi : ∀ t ∈ T, i < t) :
    remainderBase x₀ y T i = y i := by
  unfold remainderBase
  by_cases hs : i ∈ supp x₀ y
  · have : i ∈ sitesBefore (supp x₀ y) T := mem_sitesBefore.mpr ⟨hs, hi⟩
    simp [mixConfig, this]
  · have hy : y i = x₀ i := by
      by_contra hne
      exact hs (mem_supp.mpr hne)
    rw [mixConfig_apply_of_notMem x₀ y (fun h => hs (mem_sitesBefore.mp h).1), hy]

/-- At every site that does not precede all of `T` — the sites of `T` and everything after the
first of them — the base point is the reference. -/
theorem remainderBase_of_not_before [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (x₀ y : ∀ i, σ i) (T : Finset ι) {i : ι} (hi : ¬ ∀ t ∈ T, i < t) :
    remainderBase x₀ y T i = x₀ i := by
  unfold remainderBase
  exact mixConfig_apply_of_notMem x₀ y fun h => hi (mem_sitesBefore.mp h).2

/-- On `T` itself the base point is the reference. -/
theorem remainderBase_on [Fintype ι] [DecidableEq ι] [LinearOrder ι] [∀ i, DecidableEq (σ i)]
    (x₀ y : ∀ i, σ i) (T : Finset ι) {t : ι} (ht : t ∈ T) : remainderBase x₀ y T t = x₀ t :=
  remainderBase_of_not_before x₀ y T fun h => lt_irrefl t (h t ht)

/-- **Remainder identity of the anchored expansion.**  For every function, reference and order:
the error of the anchored interpolant of order `m - 1` at `y` is the sum, over the `m`-subsets
`T` of the changed sites, of the mixed difference over `T` at the base point `remainderBase`. -/
theorem anchored_remainder_identity [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    g y - anchoredInterp m g x₀ y =
      ∑ T ∈ (supp x₀ y).powersetCard m, mixedDiff g (remainderBase x₀ y T) T y := by
  have h := anchored_remainder_identity_mixConfig y m g (supp x₀ y) x₀
  rw [mixConfig_supp] at h
  exact h

/-- **Remainder bound with anchored constants.**  It suffices to bound the mixed differences over
the `m`-subsets `T` at base points that agree with the reference on `T`. -/
theorem anchored_remainder_bound [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (x₀ y : ∀ i, σ i)
    (hc : ∀ T : Finset ι, T.card = m → ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) →
      |mixedDiff g z T y| ≤ c T) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ T ∈ (supp x₀ y).powersetCard m, c T := by
  rw [anchored_remainder_identity]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun T hT => ?_)
  exact hc T (Finset.mem_powersetCard.mp hT).2 _ fun t ht => remainderBase_on x₀ y T ht

/-! ### The allocation lemma at order `m` -/

/-- **Site shares cover the `m`-subsets.**  If every constant `c T` is at most the sum of
nonnegative shares `lam T i` of the sites of `T`, the constants of the `m`-subsets of any set `S`
add up to at most the shares carried by the sites of `S`. -/
theorem cover_of_site_shares_order [Fintype ι] [DecidableEq ι] (m : ℕ) (c : Finset ι → ℝ)
    (lam : Finset ι → ι → ℝ) (hlam : ∀ T : Finset ι, T.card = m → ∀ i, 0 ≤ lam T i)
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
        split_ifs
        · exact hlam T (Finset.mem_powersetCard.mp hT).2 i
        · exact le_rfl

/-- The site penalty of equal shares: `γ i = (1/m) ∑_{T ∋ i, |T| = m} c T`. -/
noncomputable def sitePenalty [Fintype ι] [DecidableEq ι] (m : ℕ) (c : Finset ι → ℝ) (i : ι) : ℝ :=
  ∑ T ∈ (univ : Finset ι).powersetCard m, (if i ∈ T then c T / m else 0)

/-- **Equal shares.**  For `m ≥ 1` and constants that are nonnegative on the `m`-subsets, the site
penalties `γ i = (1/m) ∑_{T ∋ i} c T` cover the `m`-subsets of every set of sites.  (Only the
constants of `m`-subsets enter; nonnegativity is asked of those alone — a remark of the Scientific
Discovery Division, SCI-MSG-0023.) -/
theorem cover_of_equal_shares [Fintype ι] [DecidableEq ι] {m : ℕ} (hm : 0 < m) (c : Finset ι → ℝ)
    (hc : ∀ T : Finset ι, T.card = m → 0 ≤ c T) (S : Finset ι) :
    ∑ T ∈ S.powersetCard m, c T ≤ ∑ i ∈ S, sitePenalty m c i := by
  unfold sitePenalty
  refine cover_of_site_shares_order m c (fun T _ => c T / m)
    (fun T hT _ => div_nonneg (hc T hT) (Nat.cast_nonneg m)) (fun T hT => ?_) S
  rw [Finset.sum_const, hT, nsmul_eq_mul, mul_div_cancel₀]
  exact_mod_cast hm.ne'

/-- **A sandwich from the Hamming ball.**  With anchored constants `c` of order `m ≥ 1` the
anchored interpolant of order `m - 1` — which uses the values of `g` at configurations with fewer
than `m` changed sites only — approximates `g` up to the sum of the site penalties over the
changed sites.  (No nonnegativity hypothesis: an anchored constant of an `m`-subset bounds an
absolute value, at the base point `x₀`, and no other constant enters the penalties.  The first
version asked `0 ≤ c T` for all `T`; the redundancy was found by the Scientific Discovery Division
when it compared this file with its own formalisation, SCI-MSG-0023.) -/
theorem anchored_remainder_site_penalties [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] {m : ℕ} (hm : 0 < m) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ)
    (x₀ y : ∀ i, σ i)
    (hc : ∀ T : Finset ι, T.card = m → ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) →
      |mixedDiff g z T y| ≤ c T) :
    |g y - anchoredInterp m g x₀ y| ≤ ∑ i ∈ supp x₀ y, sitePenalty m c i :=
  (anchored_remainder_bound m g c x₀ y hc).trans
    (cover_of_equal_shares hm c (fun T hT => (abs_nonneg _).trans (hc T hT x₀ fun _ _ => rfl)) _)

/-! ### Non-vacuity -/

/-- On three binary sites, for the triple coupling and the reference `(0,0,0)`: the remainder of
order three at `(1,1,1)` is the single mixed difference over all three sites at the reference
(the base point of the identity is the reference itself), and it equals `1`. -/
theorem anchored_remainder_witness :
    tripleResidual (fun _ => 1) - anchoredInterp 3 tripleResidual (fun _ => 0) (fun _ => 1) = 1 ∧
      remainderBase (σ := fun _ : Fin 3 => Fin 2) (fun _ => 0) (fun _ => 1) univ = fun _ => 0 := by
  constructor
  · have h : (supp (σ := fun _ : Fin 3 => Fin 2) (fun _ => 0) (fun _ => 1)).card < 3 → False := by
      intro hlt
      have : supp (σ := fun _ : Fin 3 => Fin 2) (fun _ => 0) (fun _ => 1) = univ := by
        ext i
        simp [mem_supp]
      rw [this] at hlt
      simp at hlt
    have hv : anchoredInterp 3 tripleResidual (fun _ => 0) (fun _ => 1) = 0 := by
      refine anchoredInterp_eq_zero_of_vanish 3 tripleResidual (fun _ => 0) (fun z hz => ?_) _
      rw [tripleResidual_cast]
      exact_mod_cast tripleResidualQ_vanish z hz
    rw [hv, sub_zero]
    simp [tripleResidual]
  · funext i
    exact remainderBase_on _ _ univ (Finset.mem_univ i)

end MetricChain
