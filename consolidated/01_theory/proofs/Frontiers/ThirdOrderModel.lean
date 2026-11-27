/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# Third-order residual classes reduce to pairwise lower models (theory report §11.7, Theorem 11.18a)

`HigherOrderEnvelope.lean` bounds a residual `g` whose mixed differences of order three over a triple `T` of sites are
at most `c T` by its interpolant of order two around a reference configuration `x₀` — which uses the values of `g` on
the Hamming ball of radius two only — up to the sum of the constants over the triples of changed sites
(`higherOrder_remainder`).  That bound is a *three-body* function of the configuration.  This file turns it into
**pairwise** lower models, which the tropical kernel can certify:

* `anchoredInterp_three` — the interpolant of order two is pairwise: the star part plus the second mixed differences
  at the reference (`pairIncrement`) over the pairs of sites;
* `thirdOrderLowerModel`, `thirdOrderLowerModel_energy` — the pairwise model with one-body penalties `γ i` on changed
  sites and pair penalties `γ₂ i j` on changed pairs, and its energy;
* `thirdOrder_pairwise_lower` — if the penalties *cover* the triples, `∑_{T ⊆ S, |T| = 3} c T ≤ ∑_{i ∈ S} γ i + pairSum γ₂ S`
  for every set `S` of sites, the model is a lower bound of the true energy at every configuration;
* `cover_of_site_shares`, `thirdOrder_pairwise_lower_thirds` — site form: `γ i = ⅓ ∑_{T ∋ i} c T` covers (more
  generally any nonnegative shares of the triples among their sites);
* `cover_of_pair_thirds`, `thirdOrder_pairwise_lower_pair_thirds` — pair form: `γ₂ i k = ⅓ ∑_{T ⊇ {i,k}} c T` covers; it
  is the tighter of the two (a triple with only one or two changed sites costs less or nothing);
* `verify_sound_thirdOrder` — kernel soundness: a certificate accepted by the pairwise kernel for an instance that
  lies termwise below the model bounds the true energy `M.energy x + g x`;
* `thirdOrder_witness` — non-vacuity on three binary sites: both forms have exactly the penalty `c T` at a single
  triple.

The statement was requested by the Scientific Discovery Division (its message SCI-MSG-0015, request P2-T1, with the site
form), after it measured third-order constants of a solvent term in rotamer variables on a fixed backbone that are two
orders of magnitude below the single-site excitation energies.  The measured constants are not certified constants;
nothing here says how to obtain certified ones.
-/
import Mathlib
import proofs.Frontiers.HigherOrderEnvelope

namespace MetricChain

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-- Second mixed difference of `g` at the reference `x₀`, sites `i`, `j`, target states `a`, `b`. -/
def pairIncrement [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i) (i j : ι) (a : σ i)
    (b : σ j) : ℝ :=
  g (Function.update (Function.update x₀ i a) j b) - g (Function.update x₀ i a) -
    g (Function.update x₀ j b) + g x₀

theorem pairIncrement_comm [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i) {i j : ι}
    (hij : i ≠ j) (a : σ i) (b : σ j) :
    pairIncrement g x₀ j i b a = pairIncrement g x₀ i j a b := by
  unfold pairIncrement
  rw [Function.update_comm hij.symm]
  ring

theorem pairIncrement_left_ref [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i) (i j : ι)
    (b : σ j) : pairIncrement g x₀ i j (x₀ i) b = 0 := by
  unfold pairIncrement
  rw [Function.update_eq_self]
  ring

theorem pairIncrement_right_ref [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i) (i j : ι)
    (a : σ i) (hij : i ≠ j) : pairIncrement g x₀ i j a (x₀ j) = 0 := by
  unfold pairIncrement
  have h : Function.update (Function.update x₀ i a) j (x₀ j) = Function.update x₀ i a := by
    funext k
    by_cases hk : k = j
    · subst hk
      rw [Function.update_self, Function.update_of_ne hij.symm]
    · rw [Function.update_of_ne hk]
  rw [h, Function.update_eq_self]
  ring

/-- **The interpolant of order two is pairwise.** -/
theorem anchoredInterp_three [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    anchoredInterp 3 g x₀ y = starPart g x₀ y +
      (1 / 2) * ∑ i, ∑ j ∈ univ.erase i, pairIncrement g x₀ i j (y i) (y j) := by
  classical
  set f : ι → ι → ℝ := fun i j => pairIncrement g x₀ i j (y i) (y j) with hf
  rw [anchoredInterp_succ, anchoredInterp_two]
  congr 1
  have h1 : ∑ T ∈ (supp x₀ y).powersetCard 2, mixedDiff g x₀ T y =
      ∑ T ∈ (supp x₀ y).powersetCard 2, pairSum f T := by
    refine Finset.sum_congr rfl fun T hT => ?_
    obtain ⟨i, j, hij, rfl⟩ := Finset.card_eq_two.mp (Finset.mem_powersetCard.mp hT).2
    rw [mixedDiff_pair g x₀ y hij, pairSum_pair f hij]
    have hc : f j i = f i j := pairIncrement_comm g x₀ hij (y i) (y j)
    rw [hc]
    simp only [hf, pairIncrement]
    ring
  rw [h1, sum_pairSum_powersetCard_two, pairSum_supp]
  unfold pairRemainder
  congr 1
  refine Finset.sum_congr rfl fun i _ => ?_
  refine Finset.sum_congr rfl fun j hj => ?_
  have hji : j ≠ i := Finset.ne_of_mem_erase hj
  show pairIncrement g x₀ i j (y i) (y j) * changed x₀ y i * changed x₀ y j =
    pairIncrement g x₀ i j (y i) (y j)
  by_cases hi : y i = x₀ i
  · have hz : pairIncrement g x₀ i j (y i) (y j) = 0 := by
      rw [hi]
      exact pairIncrement_left_ref g x₀ i j (y j)
    rw [hz, zero_mul, zero_mul]
  · by_cases hj' : y j = x₀ j
    · have hz : pairIncrement g x₀ i j (y i) (y j) = 0 := by
        rw [hj']
        exact pairIncrement_right_ref g x₀ i j (y i) hji.symm
      rw [hz, zero_mul, zero_mul]
    · rw [changed_of_ne hi, changed_of_ne hj', mul_one, mul_one]

/-- **Pairwise lower model of third order.** -/
noncomputable def thirdOrderLowerModel [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (γ : ι → ℝ) (γ₂ : ι → ι → ℝ) (x₀ : ∀ i, σ i) :
    PairModel ℝ ι σ where
  h i s := M.h i s + (g (Function.update x₀ i s) - g x₀) - γ i * (if s = x₀ i then 0 else 1)
  J i j a b := M.J i j a b + pairIncrement g x₀ i j a b / 2 -
    γ₂ i j / 2 * (if a = x₀ i then 0 else 1) * (if b = x₀ j then 0 else 1)

theorem thirdOrderLowerModel_energy [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (γ : ι → ℝ) (γ₂ : ι → ι → ℝ) (x₀ x : ∀ i, σ i) :
    (thirdOrderLowerModel M g γ γ₂ x₀).energy x + g x₀ =
      M.energy x + anchoredInterp 3 g x₀ x - ∑ i, γ i * changed x₀ x i -
        pairRemainder γ₂ x₀ x := by
  rw [anchoredInterp_three, ← sum_half_changed_eq_pairRemainder]
  unfold PairModel.energy thirdOrderLowerModel starPart changed
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.mul_sum]
  have e : ∑ i, ∑ j ∈ univ.erase i, pairIncrement g x₀ i j (x i) (x j) / 2 =
      ∑ i, ∑ j ∈ univ.erase i, 1 / 2 * pairIncrement g x₀ i j (x i) (x j) := by
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    ring
  rw [e]
  ring

/-- **Third-order classes reduce to pairwise lower models.** -/
theorem thirdOrder_pairwise_lower [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (hg : HigherDiffBound 3 g c)
    (γ : ι → ℝ) (γ₂ : ι → ι → ℝ)
    (hcover : ∀ S : Finset ι, ∑ T ∈ S.powersetCard 3, c T ≤ ∑ i ∈ S, γ i + pairSum γ₂ S)
    (x₀ x : ∀ i, σ i) :
    (thirdOrderLowerModel M g γ γ₂ x₀).energy x + g x₀ ≤ M.energy x + g x := by
  have h := (abs_le.mp (higherOrder_remainder 3 g c hg x₀ x)).1
  have hc := hcover (supp x₀ x)
  rw [pairSum_supp] at hc
  have hs : ∑ i ∈ supp x₀ x, γ i = ∑ i, γ i * changed x₀ x i := by
    rw [← Finset.sum_subset (Finset.subset_univ (supp x₀ x))]
    · refine Finset.sum_congr rfl fun i hi => ?_
      rw [changed_of_ne (mem_supp.mp hi), mul_one]
    · intro i _ hi
      have : x i = x₀ i := by
        by_contra hne
        exact hi (mem_supp.mpr hne)
      rw [changed_of_eq this, mul_zero]
  rw [thirdOrderLowerModel_energy]
  linarith

/-- **Site shares cover the triples.** -/
theorem cover_of_site_shares [Fintype ι] [DecidableEq ι] (c : Finset ι → ℝ)
    (lam : Finset ι → ι → ℝ) (hlam : ∀ T i, 0 ≤ lam T i)
    (hshare : ∀ T : Finset ι, T.card = 3 → c T ≤ ∑ i ∈ T, lam T i) (S : Finset ι) :
    ∑ T ∈ S.powersetCard 3, c T ≤
      ∑ i ∈ S, ∑ T ∈ (univ : Finset ι).powersetCard 3, (if i ∈ T then lam T i else 0) := by
  calc ∑ T ∈ S.powersetCard 3, c T
      ≤ ∑ T ∈ S.powersetCard 3, ∑ i ∈ T, lam T i :=
        Finset.sum_le_sum fun T hT => hshare T (Finset.mem_powersetCard.mp hT).2
    _ = ∑ T ∈ S.powersetCard 3, ∑ i ∈ S, (if i ∈ T then lam T i else 0) := by
        refine Finset.sum_congr rfl fun T hT => ?_
        have hTS : T ⊆ S := (Finset.mem_powersetCard.mp hT).1
        rw [← Finset.sum_filter]
        congr 1
        ext i
        simp only [Finset.mem_filter]
        exact ⟨fun h => ⟨hTS h, h⟩, fun h => h.2⟩
    _ = ∑ i ∈ S, ∑ T ∈ S.powersetCard 3, (if i ∈ T then lam T i else 0) := Finset.sum_comm
    _ ≤ ∑ i ∈ S, ∑ T ∈ (univ : Finset ι).powersetCard 3, (if i ∈ T then lam T i else 0) := by
        refine Finset.sum_le_sum fun i _ => ?_
        refine Finset.sum_le_sum_of_subset_of_nonneg
          (Finset.powersetCard_mono (Finset.subset_univ S)) fun T _ _ => ?_
        split_ifs
        · exact hlam T i
        · exact le_rfl

/-- **The rule of thirds, site form.**  With `γ i = ⅓ ∑_{T ∋ i} c T` the site penalties cover every
triple of changed sites. -/
theorem thirdOrder_pairwise_lower_thirds [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ) (hc : ∀ T, 0 ≤ c T)
    (hg : HigherDiffBound 3 g c) (x₀ x : ∀ i, σ i) :
    (thirdOrderLowerModel M g
        (fun i => ∑ T ∈ (univ : Finset ι).powersetCard 3, (if i ∈ T then c T / 3 else 0))
        (fun _ _ => 0) x₀).energy x + g x₀ ≤ M.energy x + g x := by
  refine thirdOrder_pairwise_lower M g c hg _ _ (fun S => ?_) x₀ x
  have h0 : pairSum (fun _ _ : ι => (0 : ℝ)) S = 0 := by simp [pairSum]
  rw [h0, add_zero]
  refine cover_of_site_shares c (fun T _ => c T / 3) (fun T _ => by have := hc T; positivity)
    (fun T hT => ?_) S
  rw [Finset.sum_const, hT]
  simp only [nsmul_eq_mul, Nat.cast_ofNat]
  linarith

/-- **Pair shares cover the triples**: with `γ₂ i k = ⅓ ∑_{T ⊇ {i,k}} c T` the pair penalties over
the pairs of changed sites cover every triple of changed sites. -/
theorem cover_of_pair_thirds [Fintype ι] [DecidableEq ι] (c : Finset ι → ℝ) (hc : ∀ T, 0 ≤ c T)
    (S : Finset ι) :
    ∑ T ∈ S.powersetCard 3, c T ≤
      pairSum (fun i k => ∑ T ∈ (univ : Finset ι).powersetCard 3,
        (if i ∈ T ∧ k ∈ T then c T / 3 else 0)) S := by
  unfold pairSum
  have key : ∀ T ∈ S.powersetCard 3,
      ∑ i ∈ S, ∑ k ∈ S.erase i, (if i ∈ T ∧ k ∈ T then c T / 3 else 0) = 2 * c T := by
    intro T hT
    obtain ⟨hTS, hT3⟩ := Finset.mem_powersetCard.mp hT
    have h1 : ∀ i ∈ S, ∑ k ∈ S.erase i, (if i ∈ T ∧ k ∈ T then c T / 3 else 0) =
        if i ∈ T then 2 * (c T / 3) else 0 := by
      intro i _
      by_cases hi : i ∈ T
      · rw [if_pos hi]
        have h2 : ∀ k ∈ S.erase i, (if i ∈ T ∧ k ∈ T then c T / 3 else 0) =
            if k ∈ T then c T / 3 else 0 := by
          intro k _
          simp [hi]
        rw [Finset.sum_congr rfl h2, ← Finset.sum_filter]
        have h3 : (S.erase i).filter (fun k => k ∈ T) = T.erase i := by
          ext k
          simp only [Finset.mem_filter, Finset.mem_erase]
          exact ⟨fun h => ⟨h.1.1, h.2⟩, fun h => ⟨⟨h.1, hTS h.2⟩, h.2⟩⟩
        rw [h3, Finset.sum_const, Finset.card_erase_of_mem hi, hT3]
        simp
      · rw [if_neg hi]
        refine Finset.sum_eq_zero fun k _ => ?_
        simp [hi]
    rw [Finset.sum_congr rfl h1, ← Finset.sum_filter]
    have h4 : S.filter (fun i => i ∈ T) = T := by
      ext i
      simp only [Finset.mem_filter]
      exact ⟨fun h => h.2, fun h => ⟨hTS h, h⟩⟩
    rw [h4, Finset.sum_const, hT3]
    simp only [nsmul_eq_mul, Nat.cast_ofNat]
    ring
  have hsub : ∀ i ∈ S, ∀ k ∈ S.erase i,
      ∑ T ∈ S.powersetCard 3, (if i ∈ T ∧ k ∈ T then c T / 3 else 0) ≤
        ∑ T ∈ (univ : Finset ι).powersetCard 3, (if i ∈ T ∧ k ∈ T then c T / 3 else 0) := by
    intro i _ k _
    refine Finset.sum_le_sum_of_subset_of_nonneg
      (Finset.powersetCard_mono (Finset.subset_univ S)) fun T _ _ => ?_
    split_ifs
    · have := hc T
      positivity
    · exact le_rfl
  have hswap : ∑ i ∈ S, ∑ k ∈ S.erase i, ∑ T ∈ S.powersetCard 3,
      (if i ∈ T ∧ k ∈ T then c T / 3 else 0) = ∑ T ∈ S.powersetCard 3, 2 * c T := by
    rw [← Finset.sum_congr rfl key, Finset.sum_comm]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [Finset.sum_comm]
  have hle : ∑ T ∈ S.powersetCard 3, 2 * c T ≤
      ∑ i ∈ S, ∑ k ∈ S.erase i, ∑ T ∈ (univ : Finset ι).powersetCard 3,
        (if i ∈ T ∧ k ∈ T then c T / 3 else 0) := by
    rw [← hswap]
    exact Finset.sum_le_sum fun i hi => Finset.sum_le_sum fun k hk => hsub i hi k hk
  rw [← Finset.mul_sum] at hle
  linarith

/-- **The rule of thirds, pair form** (a tighter pairwise lower model than the site form). -/
theorem thirdOrder_pairwise_lower_pair_thirds [Fintype ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : Finset ι → ℝ)
    (hc : ∀ T, 0 ≤ c T) (hg : HigherDiffBound 3 g c) (x₀ x : ∀ i, σ i) :
    (thirdOrderLowerModel M g (fun _ => 0)
        (fun i k => ∑ T ∈ (univ : Finset ι).powersetCard 3,
          (if i ∈ T ∧ k ∈ T then c T / 3 else 0)) x₀).energy x + g x₀ ≤ M.energy x + g x := by
  refine thirdOrder_pairwise_lower M g c hg _ _ (fun S => ?_) x₀ x
  rw [Finset.sum_const_zero, zero_add]
  exact cover_of_pair_thirds c hc S

/-- **Kernel soundness with a third-order envelope.** -/
theorem verify_sound_thirdOrder {n k : ℕ} (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (g : Config n k → ℝ) (c : Finset (Fin n) → ℝ) (x₀ : Config n k)
    (hg : HigherDiffBound 3 g c) (γ : Fin n → ℝ) (γ₂ : Fin n → Fin n → ℝ)
    (hcover : ∀ S : Finset (Fin n), ∑ T ∈ S.powersetCard 3, c T ≤ ∑ i ∈ S, γ i + pairSum γ₂ S)
    (I : PairInstance n k)
    (hh : ∀ i a, (I.h i a : ℝ) ≤ (thirdOrderLowerModel M g γ γ₂ x₀).h i a)
    (hJ : ∀ i j a b, (I.J i j a b : ℝ) ≤ (thirdOrderLowerModel M g γ γ₂ x₀).J i j a b)
    (cert : Cert n k) (D : Dom n k) (L : ℚ) (hv : verify cert I D L = true)
    (x : Config n k) (hx : InBox D x) : (L : ℝ) + g x₀ ≤ M.energy x + g x := by
  have h1 := verify_sound_real cert I D L hv (thirdOrderLowerModel M g γ γ₂ x₀) hh hJ x hx
  have h2 := thirdOrder_pairwise_lower M g c hg γ γ₂ hcover x₀ x
  linarith

/-! ### Non-vacuity

Three binary sites, reference `(0, 0, 0)`, zero explicit part, and the pure three-body coupling of
`HigherOrderEnvelope.lean` (order-`3` envelope `1`).  At `(1, 1, 1)` the pairwise lower model has the
energy `-1` in the site form and in the pair form: the penalties of the three changed sites, and
of the three changed pairs, add up to the constant of the one triple — neither form loses
anything at a single triple. -/

/-- The zero pairwise model on three binary sites. -/
def zeroModel3 : PairModel ℝ (Fin 3) (fun _ => Fin 2) where
  h _ _ := 0
  J _ _ _ _ := 0

theorem powersetCard_three_fin_three :
    (univ : Finset (Fin 3)).powersetCard 3 = {univ} := by decide

/-- **Non-vacuity for the pairwise lower models of third order.** -/
theorem thirdOrder_witness :
    HigherDiffBound 3 tripleResidual (fun _ => 1) ∧
      (thirdOrderLowerModel zeroModel3 tripleResidual
          (fun i => ∑ T ∈ (univ : Finset (Fin 3)).powersetCard 3,
            (if i ∈ T then (1 : ℝ) / 3 else 0))
          (fun _ _ => 0) ![0, 0, 0]).energy ![1, 1, 1] + tripleResidual ![0, 0, 0] = -1 ∧
      (thirdOrderLowerModel zeroModel3 tripleResidual (fun _ => 0)
          (fun i k => ∑ T ∈ (univ : Finset (Fin 3)).powersetCard 3,
            (if i ∈ T ∧ k ∈ T then (1 : ℝ) / 3 else 0))
          ![0, 0, 0]).energy ![1, 1, 1] + tripleResidual ![0, 0, 0] = -1 ∧
      zeroModel3.energy ![1, 1, 1] + tripleResidual ![1, 1, 1] = 1 := by
  have hv : ∀ y : Config 3 2, (supp (![0, 0, 0] : Config 3 2) y).card < 3 →
      tripleResidual y = 0 := higherOrder_witness.1
  have hI : anchoredInterp 3 tripleResidual ![0, 0, 0] ![1, 1, 1] = 0 :=
    anchoredInterp_eq_zero_of_vanish 3 tripleResidual ![0, 0, 0] hv _
  have hE : zeroModel3.energy ![1, 1, 1] = 0 := by
    simp [PairModel.energy, zeroModel3]
  have hch : ∀ i : Fin 3, changed (![0, 0, 0] : Config 3 2) ![1, 1, 1] i = 1 := by
    intro i
    apply changed_of_ne
    fin_cases i <;> decide
  refine ⟨tripleResidual_higherDiffBound, ?_, ?_, ?_⟩
  · rw [thirdOrderLowerModel_energy, hE, hI]
    have h0 : pairRemainder (fun _ _ : Fin 3 => (0 : ℝ)) (![0, 0, 0] : Config 3 2) ![1, 1, 1] = 0 := by
      simp [pairRemainder]
    rw [h0, powersetCard_three_fin_three]
    simp [hch]
  · rw [thirdOrderLowerModel_energy, hE, hI]
    unfold pairRemainder
    rw [powersetCard_three_fin_three]
    simp [hch]
    norm_num
  · rw [hE]
    simp [tripleResidual]

end MetricChain
