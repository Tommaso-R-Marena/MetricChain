/-
  MetricChain — Ensemble division.  The permanent certificate (report §4c.4, Proposition E21).

  `K` states of a product configuration space with `r` coordinates; `a i k ≥ 0` vanishes exactly
  when coordinate `k` of the configuration equals coordinate `k` of state `i`.  The certificate is
  the permanent of the `K × r` matrix `a`: the sum, over injective assignments of coordinates to
  states, of the products `∏ i, a i (κ i)`.  By Hall's marriage theorem it vanishes iff some set
  of states "sees" fewer coordinates than it has members (`permCert_eq_zero_iff`); if every set
  `I` of at least two states has at least `card I` coordinates at which its states do not all
  coincide (the Hall condition), it vanishes exactly at the states (`permCert_zero_set`).
  For two states this is the certificate of `TwoStateCertificate.lean`.

  On paper: that the certificate lies in the span of the multilinear observables, and the passage
  from "non-negative function in the span with zero set = support" to identification
  (Theorem E1; for finite spaces `eq_of_exposing_certificate`).
-/
import Mathlib

namespace MetricChain.Ensemble

open Finset

variable {ι α : Type*} [Fintype ι] [DecidableEq ι] [Fintype α] [DecidableEq α]

/-- The permanent certificate of `K = card ι` states on a product of `card α` coordinates:
the sum over injective assignments `κ` of coordinates to states of `∏ i, a i (κ i)`, where
`a i k ≥ 0` measures how far coordinate `k` of the configuration is from coordinate `k` of state `i`. -/
noncomputable def permCert (a : ι → α → ℝ) : ℝ :=
  ∑ κ ∈ (univ : Finset (ι → α)).filter Function.Injective, ∏ i, a i (κ i)

/-- The coordinates at which the configuration differs from state `i`. -/
noncomputable def offSet (a : ι → α → ℝ) (i : ι) : Finset α := univ.filter (fun k => a i k ≠ 0)

theorem permCert_nonneg (a : ι → α → ℝ) (ha : ∀ i k, 0 ≤ a i k) : 0 ≤ permCert a :=
  Finset.sum_nonneg (fun κ _ => Finset.prod_nonneg (fun i _ => ha i (κ i)))

/-- **Zero set of the permanent certificate (Hall).**  For non-negative entries the certificate
vanishes iff some set `s` of states sees fewer than `card s` coordinates at which the
configuration differs from one of its states. -/
theorem permCert_eq_zero_iff (a : ι → α → ℝ) (ha : ∀ i k, 0 ≤ a i k) :
    permCert a = 0 ↔ ∃ s : Finset ι, (s.biUnion (offSet a)).card < s.card := by
  have hterm : ∀ κ ∈ (univ : Finset (ι → α)).filter Function.Injective, 0 ≤ ∏ i, a i (κ i) :=
    fun κ _ => Finset.prod_nonneg (fun i _ => ha i (κ i))
  have hhall := Finset.all_card_le_biUnion_card_iff_exists_injective (offSet a)
  constructor
  · intro h
    by_contra hno
    push Not at hno
    obtain ⟨κ, hκinj, hκ⟩ := hhall.mp hno
    have hzero := (Finset.sum_eq_zero_iff_of_nonneg hterm).mp h κ
      (Finset.mem_filter.mpr ⟨Finset.mem_univ κ, hκinj⟩)
    obtain ⟨i, _, hi⟩ := Finset.prod_eq_zero_iff.mp hzero
    have := hκ i
    simp only [offSet, Finset.mem_filter, Finset.mem_univ, true_and] at this
    exact this hi
  · rintro ⟨s, hs⟩
    unfold permCert
    refine Finset.sum_eq_zero (fun κ hκ => ?_)
    have hκinj : Function.Injective κ := (Finset.mem_filter.mp hκ).2
    by_contra hne
    have hall_i : ∀ i, a i (κ i) ≠ 0 := by
      intro i hi
      exact hne (Finset.prod_eq_zero (Finset.mem_univ i) hi)
    have hmem : ∀ i, κ i ∈ offSet a i := by
      intro i
      simp only [offSet, Finset.mem_filter, Finset.mem_univ, true_and]
      exact hall_i i
    have := (hhall.mpr ⟨κ, hκinj, hmem⟩) s
    exact absurd this (not_le.mpr hs)

/-- **The Hall condition gives exactly the states.**  If every set of at least two states sees at
least as many coordinates as it has members (whatever the configuration — this is what the
Hall condition on the states provides), the certificate vanishes iff the configuration coincides
with one of the states in every coordinate. -/
theorem permCert_eq_zero_iff_of_hall (a : ι → α → ℝ) (ha : ∀ i k, 0 ≤ a i k)
    (hall : ∀ s : Finset ι, 2 ≤ s.card → s.card ≤ (s.biUnion (offSet a)).card) :
    permCert a = 0 ↔ ∃ i, ∀ k, a i k = 0 := by
  rw [permCert_eq_zero_iff a ha]
  constructor
  · rintro ⟨s, hs⟩
    have hcard : s.card < 2 := by
      by_contra h
      push Not at h
      exact absurd (hall s h) (not_le.mpr hs)
    have hpos : 0 < s.card := lt_of_le_of_lt (Nat.zero_le _) hs
    have hone : s.card = 1 := by omega
    obtain ⟨i, rfl⟩ := Finset.card_eq_one.mp hone
    refine ⟨i, fun k => ?_⟩
    have hempty : (offSet a i).card = 0 := by
      have : (({i} : Finset ι).biUnion (offSet a)).card < 1 := by simpa using hs
      simpa using this
    have hk : k ∉ offSet a i := by
      rw [Finset.card_eq_zero.mp hempty]; simp
    simp only [offSet, Finset.mem_filter, Finset.mem_univ, true_and, not_not] at hk
    exact hk
  · rintro ⟨i, hi⟩
    refine ⟨{i}, ?_⟩
    have : offSet a i = ∅ := by
      ext k
      simp [offSet, hi k]
    simp [this]

/-- **Proposition E21 (a), (b): the permanent certificate vanishes exactly at the states.**
States `s i : α → β` and a configuration `x : α → β` of a product space with coordinates in `α`;
`a i k ≥ 0` vanishes exactly when `x k = s i k`.  *Hall condition on the states:* every set `I` of at
least two states has at least `card I` coordinates at which its states do not all coincide.  Then
the certificate vanishes iff the configuration is one of the states. -/
theorem permCert_zero_set {β : Type*} [DecidableEq β] (s : ι → α → β) (x : α → β) (a : ι → α → ℝ)
    (ha : ∀ i k, 0 ≤ a i k) (hzero : ∀ i k, a i k = 0 ↔ x k = s i k)
    (hallS : ∀ I : Finset ι, 2 ≤ I.card →
      I.card ≤ (univ.filter (fun k => ∃ i ∈ I, ∃ j ∈ I, s i k ≠ s j k)).card) :
    permCert a = 0 ↔ ∃ i, x = s i := by
  have hall : ∀ I : Finset ι, 2 ≤ I.card → I.card ≤ (I.biUnion (offSet a)).card := by
    intro I hI
    refine le_trans (hallS I hI) (Finset.card_le_card ?_)
    intro k hk
    obtain ⟨i, hi, j, hj, hne⟩ := (Finset.mem_filter.mp hk).2
    rw [Finset.mem_biUnion]
    by_cases hxi : x k = s i k
    · refine ⟨j, hj, ?_⟩
      simp only [offSet, Finset.mem_filter, Finset.mem_univ, true_and]
      intro h0
      exact hne (hxi.symm.trans ((hzero j k).mp h0))
    · refine ⟨i, hi, ?_⟩
      simp only [offSet, Finset.mem_filter, Finset.mem_univ, true_and]
      intro h0
      exact hxi ((hzero i k).mp h0)
  rw [permCert_eq_zero_iff_of_hall a ha hall]
  constructor
  · rintro ⟨i, hi⟩
    exact ⟨i, funext (fun k => (hzero i k).mp (hi k))⟩
  · rintro ⟨i, hi⟩
    exact ⟨i, fun k => (hzero i k).mpr (congrFun hi k)⟩

end MetricChain.Ensemble
