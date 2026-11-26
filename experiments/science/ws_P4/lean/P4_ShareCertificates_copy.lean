/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# Share certificates for the second-order sharp-minimum condition (theory report §11.7, Proposition 11.18b)

Theorem 11.17 (`secondOrder_certified_minimizer_iff`) says that a reference configuration `x₀` minimises the true energy
for every residual of a second-order class iff it minimises its own pairwise lower model.  For an additive known part
that condition reads: no set `S` of sites is *over-dense*, `∑_{i<j ∈ S} c i j ≤ ∑_{i ∈ S} (excitation energy of site i)`.
This file gives a certificate for it that is checked by additions:

* `pairSum_le_of_shares` — if every pair constant is split between its two sites, `c i k ≤ s i k + s k i` with
  nonnegative shares, the pair constant of any set of sites is at most the sum of the loads `∑_{k ≠ i} s i k` of its sites;
* `secondOrder_certified_of_shares` — hence, for an additive explicit part: if every site's load is at most each of its
  measured single-site excitation energies, `x₀` minimises `M.energy + g'` for every residual `g'` of the class;
* `secondOrder_certified_of_rowSum` — the split in halves: the **row-sum condition** `½ ∑_{k ≠ i} c i k ≤` excitation
  energy (stated on paper since cycle 7; machine-checked here).

The converse — whenever no set of sites is over-dense, shares exist — is the max-flow min-cut theorem for the network
source → pairs → sites → sink and is not formalised (theory report, Proposition 11.18b(b); harness XI.17 compares the two
conditions with brute force).  The analogue for triples is `cover_of_site_shares` in `ThirdOrderModel.lean`.

The question was asked by the Scientific Discovery Division (SCI-MSG-0015, request P2-T2: "is there a condition of
maximum-density type?").
-/
import Mathlib
import proofs.Frontiers.HigherOrderEnvelope

namespace MetricChain

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-- **Pair shares cover the pairs.**  If every pair constant is covered by the two shares charged to
its sites, `c i k ≤ s i k + s k i`, then the pair constant of any set of sites is at most the sum of
the loads `∑_{k ≠ i} s i k` of its sites. -/
theorem pairSum_le_of_shares [Fintype ι] [DecidableEq ι] (c s : ι → ι → ℝ)
    (hs : ∀ i k, 0 ≤ s i k) (hcs : ∀ i k, i ≠ k → c i k ≤ s i k + s k i) (S : Finset ι) :
    pairSum c S ≤ ∑ i ∈ S, ∑ k ∈ (univ : Finset ι).erase i, s i k := by
  unfold pairSum
  have h1 : ∑ i ∈ S, ∑ k ∈ S.erase i, c i k ≤ ∑ i ∈ S, ∑ k ∈ S.erase i, (s i k + s k i) :=
    Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun k hk =>
      hcs i k (Finset.ne_of_mem_erase hk).symm
  have h2 : ∑ i ∈ S, ∑ k ∈ S.erase i, s k i = ∑ i ∈ S, ∑ k ∈ S.erase i, s i k := by
    have e : ∀ f : ι → ι → ℝ, ∑ i ∈ S, ∑ k ∈ S.erase i, f i k =
        ∑ i ∈ S, ∑ k ∈ S, (if k ≠ i then f i k else 0) := by
      intro f
      refine Finset.sum_congr rfl fun i _ => ?_
      rw [← Finset.sum_filter]
      congr 1
      ext k
      simp [Finset.mem_erase, and_comm]
    rw [e (fun i k => s k i), e (fun i k => s i k), Finset.sum_comm]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun k _ => ?_
    by_cases h : i = k
    · subst h
      simp
    · rw [if_pos h, if_pos (Ne.symm h)]
  have h3 : ∑ i ∈ S, ∑ k ∈ S.erase i, (s i k + s k i) = 2 * ∑ i ∈ S, ∑ k ∈ S.erase i, s i k := by
    simp only [Finset.sum_add_distrib]
    rw [h2]
    ring
  have h4 : ∑ i ∈ S, ∑ k ∈ S.erase i, s i k ≤ ∑ i ∈ S, ∑ k ∈ (univ : Finset ι).erase i, s i k :=
    Finset.sum_le_sum fun i _ => Finset.sum_le_sum_of_subset_of_nonneg
      (Finset.erase_subset_erase i (Finset.subset_univ S)) fun k _ _ => hs i k
  linarith

/-- **Share certificate for the second-order sharp-minimum condition (additive known part).** -/
theorem secondOrder_certified_of_shares [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (hJ : ∀ i j a b, M.J i j a b = 0) (g : (∀ i, σ i) → ℝ)
    (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (x₀ : ∀ i, σ i) (s : ι → ι → ℝ)
    (hs : ∀ i k, 0 ≤ s i k) (hcs : ∀ i k, i ≠ k → c i k ≤ s i k + s k i)
    (hload : ∀ i (a : σ i), a ≠ x₀ i → ∑ k ∈ (univ : Finset ι).erase i, s i k ≤
      M.h i a - M.h i (x₀ i) + (g (Function.update x₀ i a) - g x₀))
    (g' : (∀ i, σ i) → ℝ) (hg' : SecondOrderClass g c x₀ g') (x : ∀ i, σ i) :
    M.energy x₀ + g' x₀ ≤ M.energy x + g' x := by
  refine secondOrder_certified_minimizer M g c hc x₀ (fun y => ?_) g' hg' x
  have e1 := lowerModel_energy M g c x₀ y
  have e2 := lowerModel_energy M g c x₀ x₀
  rw [starPart_self, pairRemainder_self] at e2
  have hE : ∀ z : ∀ i, σ i, M.energy z = ∑ i, M.h i (z i) := by
    intro z
    unfold PairModel.energy
    simp [hJ]
  have hcover := pairSum_le_of_shares c s hs hcs (supp x₀ y)
  rw [pairSum_supp] at hcover
  have hsum : ∑ i ∈ supp x₀ y, ∑ k ∈ (univ : Finset ι).erase i, s i k ≤
      ∑ i, (M.h i (y i) - M.h i (x₀ i) + (g (Function.update x₀ i (y i)) - g x₀)) := by
    rw [← Finset.sum_subset (Finset.subset_univ (supp x₀ y))]
    · exact Finset.sum_le_sum fun i hi => hload i (y i) (mem_supp.mp hi)
    · intro i _ hi
      have hy : y i = x₀ i := by
        by_contra hne
        exact hi (mem_supp.mpr hne)
      rw [hy, Function.update_eq_self]
      ring
  have hstar : starPart g x₀ y = g x₀ + ∑ i, (g (Function.update x₀ i (y i)) - g x₀) := rfl
  rw [hE y] at e1
  rw [hE x₀] at e2
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib] at hsum
  linarith

/-- **The row-sum condition** is the share certificate with equal shares. -/
theorem secondOrder_certified_of_rowSum [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (hJ : ∀ i j a b, M.J i j a b = 0) (g : (∀ i, σ i) → ℝ)
    (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j) (x₀ : ∀ i, σ i)
    (hrow : ∀ i (a : σ i), a ≠ x₀ i → (1 / 2) * ∑ k ∈ (univ : Finset ι).erase i, c i k ≤
      M.h i a - M.h i (x₀ i) + (g (Function.update x₀ i a) - g x₀))
    (g' : (∀ i, σ i) → ℝ) (hg' : SecondOrderClass g c x₀ g') (x : ∀ i, σ i) :
    M.energy x₀ + g' x₀ ≤ M.energy x + g' x := by
  refine secondOrder_certified_of_shares M hJ g c hc x₀ (fun i k => c i k / 2)
    (fun i k => by have := hc0 i k; positivity)
    (fun i k _ => by rw [hc k i]; linarith) (fun i a ha => ?_) g' hg' x
  have h := hrow i a ha
  rw [Finset.mul_sum] at h
  refine le_trans (le_of_eq ?_) h
  refine Finset.sum_congr rfl fun k _ => ?_
  ring

end MetricChain

-- appended by workstream P4 (science division): axioms of the headline statements of this copy
#print axioms MetricChain.pairSum_le_of_shares
#print axioms MetricChain.secondOrder_certified_of_shares
#print axioms MetricChain.secondOrder_certified_of_rowSum
