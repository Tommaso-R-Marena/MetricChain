/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# State-dependent share certificates (theory report §11.7, Proposition 11.18b (d), (e))

`ShareCertificates.lean` certifies the second-order sharp-minimum condition for an *additive* known part by shares
`s i k` of the pair constants that do not depend on the state.  This file removes both restrictions:

* `energy_sub_eq_excitations_add_secondDiff` — a pairwise model is its own expansion of order two: the energy of a
  configuration exceeds that of the reference by the single-site excitation energies plus the second differences
  `pairSecondDiff` of the pair tables at the reference;
* `secondOrder_certified_of_state_shares` — **soundness of state-dependent shares for a pairwise known part**: if
  every site `i` in every changed state `a` takes a share `s i k a ≥ 0` of each pair `{i, k}`, the two shares of a
  pair of changed states cover the pair constant minus the second difference of the known pair term, and the shares
  of a state add up to at most its measured single-site excitation energy, then the reference minimises
  `M.energy + g'` for every residual `g'` of the second-order class;
* `secondOrder_certified_of_deficit_shares` — the special case of constant shares of the *deficits* (Proposition
  11.18b(d), on paper since the sixteenth checkpoint);
* `stateShare_witness` — non-vacuity and strictness: an instance with two sites and three states on which the
  state-dependent shares exist and no deficits with constant shares do.

The statement was proposed by the Scientific Discovery Division (its workstream P4, review SCI-REV-0012, §4 and
request P4-T3(iii)), which also observed that such shares exist exactly when the reference solves the pairwise
linear relaxation of the minimisation of the lower model — they are a dual solution, a reparametrisation in which
every one-body and every pair term is minimised at the reference.  That equivalence is linear-programming duality
and is not formalised here; this file is the direction a checker needs.
-/
import Mathlib
import proofs.Frontiers.ShareCertificates

namespace MetricChain

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-- Exchanging the two indices in a sum over ordered pairs of distinct sites. -/
theorem sum_erase_swap_real [Fintype ι] [DecidableEq ι] (F : ι → ι → ℝ) :
    ∑ i, ∑ k ∈ (univ : Finset ι).erase i, F k i = ∑ i, ∑ k ∈ (univ : Finset ι).erase i, F i k := by
  have e : ∀ f : ι → ι → ℝ, ∑ i, ∑ k ∈ (univ : Finset ι).erase i, f i k =
      ∑ i, ∑ k, (if k ≠ i then f i k else 0) := by
    intro f
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [← Finset.sum_filter]
    congr 1
    ext k
    simp [Finset.mem_erase]
  rw [e (fun i k => F k i), e (fun i k => F i k), Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun k _ => ?_
  by_cases h : i = k
  · subst h
    simp
  · rw [if_pos h, if_pos (Ne.symm h)]

/-- **Second difference of a pair table at the reference**: what the ordered pair `(i, k)` of a pairwise model
contributes to the energy beyond the single-site excitations when site `i` is in state `a` and site `k` in state `b`.
It vanishes when either state is the reference state. -/
def pairSecondDiff (M : PairModel ℝ ι σ) (x₀ : ∀ i, σ i) (i k : ι) (a : σ i) (b : σ k) : ℝ :=
  M.J i k a b - M.J i k a (x₀ k) - M.J i k (x₀ i) b + M.J i k (x₀ i) (x₀ k)

theorem pairSecondDiff_of_left_eq (M : PairModel ℝ ι σ) (x₀ : ∀ i, σ i) (i k : ι) {a : σ i} (h : a = x₀ i)
    (b : σ k) : pairSecondDiff M x₀ i k a b = 0 := by
  subst h
  unfold pairSecondDiff
  ring

theorem pairSecondDiff_of_right_eq (M : PairModel ℝ ι σ) (x₀ : ∀ i, σ i) (i k : ι) (a : σ i) {b : σ k}
    (h : b = x₀ k) : pairSecondDiff M x₀ i k a b = 0 := by
  subst h
  unfold pairSecondDiff
  ring

/-- **A pairwise model is its own expansion of order two.**  The energy of `y` exceeds that of the reference by the
single-site excitation energies plus the second differences of the pair tables over the ordered pairs of sites. -/
theorem energy_sub_eq_excitations_add_secondDiff [Fintype ι] [DecidableEq ι] (M : PairModel ℝ ι σ)
    (x₀ y : ∀ i, σ i) :
    M.energy y - M.energy x₀ =
      ∑ i, (M.energy (Function.update x₀ i (y i)) - M.energy x₀) +
        ∑ i, ∑ k ∈ (univ : Finset ι).erase i, pairSecondDiff M x₀ i k (y i) (y k) := by
  have hexc : ∀ i, M.energy (Function.update x₀ i (y i)) - M.energy x₀ =
      M.localE i (y i) x₀ - M.localE i (x₀ i) x₀ := by
    intro i
    have h1 := M.energy_update x₀ i (y i)
    have h2 := M.energy_update x₀ i (x₀ i)
    rw [Function.update_eq_self] at h2
    linarith
  have s1 : ∑ i, ∑ k ∈ (univ : Finset ι).erase i, M.J k i (x₀ k) (y i) =
      ∑ i, ∑ k ∈ (univ : Finset ι).erase i, M.J i k (x₀ i) (y k) :=
    sum_erase_swap_real (fun i k => M.J i k (x₀ i) (y k))
  have s2 : ∑ i, ∑ k ∈ (univ : Finset ι).erase i, M.J k i (x₀ k) (x₀ i) =
      ∑ i, ∑ k ∈ (univ : Finset ι).erase i, M.J i k (x₀ i) (x₀ k) :=
    sum_erase_swap_real (fun i k => M.J i k (x₀ i) (x₀ k))
  simp only [hexc]
  unfold PairModel.energy PairModel.localE pairSecondDiff
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  linarith

/-- **State-dependent share certificate for the second-order sharp-minimum condition, pairwise known part.**
Let the residual lie in the second-order class with pair constants `c`.  Let every site `i` in every changed state `a`
take a share `s i k a ≥ 0` of each pair `{i, k}` such that (cover) for all changed states `a` of `i` and `b` of `k` the
two shares cover the pair constant minus the second difference of the known pair term,
`c i k − T_ik(a, b) ≤ s i k a + s k i b`, and (load) the shares of a state add up to at most its measured single-site
excitation energy.  Then the reference minimises `M.energy + g'` for every residual `g'` of the class.  Constant
shares and an additive known part give `secondOrder_certified_of_shares`. -/
theorem secondOrder_certified_of_state_shares [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ)
    (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (x₀ : ∀ i, σ i) (s : ∀ i, ι → σ i → ℝ)
    (hs : ∀ i k a, 0 ≤ s i k a)
    (hcs : ∀ i k, i ≠ k → ∀ (a : σ i) (b : σ k), a ≠ x₀ i → b ≠ x₀ k →
      c i k - (pairSecondDiff M x₀ i k a b + pairSecondDiff M x₀ k i b a) ≤ s i k a + s k i b)
    (hload : ∀ i (a : σ i), a ≠ x₀ i → ∑ k ∈ (univ : Finset ι).erase i, s i k a ≤
      (M.energy (Function.update x₀ i a) + g (Function.update x₀ i a)) - (M.energy x₀ + g x₀))
    (g' : (∀ i, σ i) → ℝ) (hg' : SecondOrderClass g c x₀ g') (x : ∀ i, σ i) :
    M.energy x₀ + g' x₀ ≤ M.energy x + g' x := by
  refine secondOrder_certified_minimizer M g c hc x₀ (fun y => ?_) g' hg' x
  have e1 := lowerModel_energy M g c x₀ y
  have e2 := lowerModel_energy M g c x₀ x₀
  rw [starPart_self, pairRemainder_self] at e2
  -- constants and shares evaluated at the configuration `y`
  set C : ι → ι → ℝ := fun i k =>
    c i k * changed x₀ y i * changed x₀ y k -
      (pairSecondDiff M x₀ i k (y i) (y k) + pairSecondDiff M x₀ k i (y k) (y i)) with hCdef
  set Sh : ι → ι → ℝ := fun i k => if y i = x₀ i then 0 else s i k (y i) with hShdef
  have hSh : ∀ i k, 0 ≤ Sh i k := by
    intro i k
    show 0 ≤ (if y i = x₀ i then 0 else s i k (y i))
    by_cases hi : y i = x₀ i
    · rw [if_pos hi]
    · rw [if_neg hi]
      exact hs i k (y i)
  have hC : ∀ i k, i ≠ k → C i k ≤ Sh i k + Sh k i := by
    intro i k hik
    have hCik : C i k = c i k * changed x₀ y i * changed x₀ y k -
        (pairSecondDiff M x₀ i k (y i) (y k) + pairSecondDiff M x₀ k i (y k) (y i)) := rfl
    by_cases hi : y i = x₀ i
    · have z : C i k = 0 := by
        rw [hCik, changed_of_eq hi, pairSecondDiff_of_left_eq M x₀ i k hi, pairSecondDiff_of_right_eq M x₀ k i (y k) hi]
        ring
      rw [z]
      exact add_nonneg (hSh i k) (hSh k i)
    · by_cases hk : y k = x₀ k
      · have z : C i k = 0 := by
          rw [hCik, changed_of_eq hk, pairSecondDiff_of_right_eq M x₀ i k (y i) hk, pairSecondDiff_of_left_eq M x₀ k i hk]
          ring
        rw [z]
        exact add_nonneg (hSh i k) (hSh k i)
      · have h := hcs i k hik (y i) (y k) hi hk
        have e : C i k = c i k - (pairSecondDiff M x₀ i k (y i) (y k) + pairSecondDiff M x₀ k i (y k) (y i)) := by
          rw [hCik, changed_of_ne hi, changed_of_ne hk]
          ring
        have e' : Sh i k + Sh k i = s i k (y i) + s k i (y k) := by
          show (if y i = x₀ i then 0 else s i k (y i)) + (if y k = x₀ k then 0 else s k i (y k)) = _
          rw [if_neg hi, if_neg hk]
        rw [e, e']
        exact h
  have hcover := pairSum_le_of_shares C Sh hSh hC univ
  -- the pair constant of `C` is the pairwise remainder minus the second differences of the known part
  have hswap : ∑ i, ∑ k ∈ (univ : Finset ι).erase i, pairSecondDiff M x₀ k i (y k) (y i) =
      ∑ i, ∑ k ∈ (univ : Finset ι).erase i, pairSecondDiff M x₀ i k (y i) (y k) :=
    sum_erase_swap_real (fun i k => pairSecondDiff M x₀ i k (y i) (y k))
  have hCsum : pairSum C univ = pairRemainder c x₀ y -
      ∑ i, ∑ k ∈ (univ : Finset ι).erase i, pairSecondDiff M x₀ i k (y i) (y k) := by
    have h1 : ∑ i, ∑ k ∈ (univ : Finset ι).erase i, C i k =
        ∑ i, ∑ k ∈ (univ : Finset ι).erase i, c i k * changed x₀ y i * changed x₀ y k -
          (∑ i, ∑ k ∈ (univ : Finset ι).erase i, pairSecondDiff M x₀ i k (y i) (y k) +
            ∑ i, ∑ k ∈ (univ : Finset ι).erase i, pairSecondDiff M x₀ k i (y k) (y i)) := by
      rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl fun i _ => ?_
      rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    unfold pairSum pairRemainder
    rw [h1, hswap]
    ring
  -- the loads are at most the excitation energies
  have hloads : ∑ i, ∑ k ∈ (univ : Finset ι).erase i, Sh i k ≤
      ∑ i, ((M.energy (Function.update x₀ i (y i)) + g (Function.update x₀ i (y i))) - (M.energy x₀ + g x₀)) := by
    refine Finset.sum_le_sum fun i _ => ?_
    by_cases hi : y i = x₀ i
    · have z : ∑ k ∈ (univ : Finset ι).erase i, Sh i k = 0 := by
        refine Finset.sum_eq_zero fun k _ => ?_
        show (if y i = x₀ i then 0 else s i k (y i)) = 0
        rw [if_pos hi]
      rw [z, hi, Function.update_eq_self]
      linarith
    · have z : ∑ k ∈ (univ : Finset ι).erase i, Sh i k = ∑ k ∈ (univ : Finset ι).erase i, s i k (y i) := by
        refine Finset.sum_congr rfl fun k _ => ?_
        show (if y i = x₀ i then 0 else s i k (y i)) = s i k (y i)
        rw [if_neg hi]
      rw [z]
      exact hload i (y i) hi
  have hen := energy_sub_eq_excitations_add_secondDiff M x₀ y
  have hstar : starPart g x₀ y = g x₀ + ∑ i, (g (Function.update x₀ i (y i)) - g x₀) := rfl
  have hsplit : ∑ i, ((M.energy (Function.update x₀ i (y i)) + g (Function.update x₀ i (y i))) - (M.energy x₀ + g x₀)) =
      ∑ i, (M.energy (Function.update x₀ i (y i)) - M.energy x₀) +
        ∑ i, (g (Function.update x₀ i (y i)) - g x₀) := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun i _ => ?_
    ring
  linarith

/-- **Share certificate with a pairwise known part (deficits).**  If `w i k` bounds the deficits
`c i k − T_ik(a, b)` over all changed states, shares of the `w i k` between the two sites with loads at most the least
excitation energies certify the reference: the case of `secondOrder_certified_of_state_shares` in which the shares do
not depend on the state (theory report, Proposition 11.18b(d)). -/
theorem secondOrder_certified_of_deficit_shares [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ)
    (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (x₀ : ∀ i, σ i) (w s : ι → ι → ℝ)
    (hw : ∀ i k, i ≠ k → ∀ (a : σ i) (b : σ k), a ≠ x₀ i → b ≠ x₀ k →
      c i k - (pairSecondDiff M x₀ i k a b + pairSecondDiff M x₀ k i b a) ≤ w i k)
    (hs : ∀ i k, 0 ≤ s i k) (hws : ∀ i k, i ≠ k → w i k ≤ s i k + s k i)
    (hload : ∀ i (a : σ i), a ≠ x₀ i → ∑ k ∈ (univ : Finset ι).erase i, s i k ≤
      (M.energy (Function.update x₀ i a) + g (Function.update x₀ i a)) - (M.energy x₀ + g x₀))
    (g' : (∀ i, σ i) → ℝ) (hg' : SecondOrderClass g c x₀ g') (x : ∀ i, σ i) :
    M.energy x₀ + g' x₀ ≤ M.energy x + g' x :=
  secondOrder_certified_of_state_shares M g c hc x₀ (fun i k _ => s i k) (fun i k _ => hs i k)
    (fun i k hik a b ha hb => le_trans (hw i k hik a b ha hb) (hws i k hik)) hload g' hg' x

/-! ### A witness: state-dependent shares certify an instance on which no constant shares exist -/

/-- Two sites with three states each: excitation energies `1` and `10` at both sites, and a known pair term that
raises the pair of states `(1, 1)` by `2`. -/
def stateShareModel : PairModel ℝ (Fin 2) (fun _ => Fin 3) where
  h _ a := if a = 0 then 0 else if a = 1 then 1 else 10
  J i k a b := if i = 0 ∧ k = 1 ∧ a = 1 ∧ b = 1 then 2 else 0

/-- The shares of the witness: a site in its cheap state takes `1/2` of the pair, in its expensive state `5/2`. -/
noncomputable def stateShareWitness : ∀ _ : Fin 2, Fin 2 → Fin 3 → ℝ := fun _ _ a => if a = 1 then 1 / 2 else 5 / 2

private theorem stateShareModel_excitation (i : Fin 2) (a : Fin 3) :
    stateShareModel.energy (Function.update (fun _ => (0 : Fin 3)) i a) - stateShareModel.energy (fun _ => (0 : Fin 3)) =
      if a = 0 then 0 else if a = 1 then 1 else 10 := by
  have h1 := stateShareModel.energy_update (fun _ => (0 : Fin 3)) i a
  have h2 := stateShareModel.energy_update (fun _ => (0 : Fin 3)) i 0
  rw [Function.update_eq_self] at h2
  have l1 : stateShareModel.localE i a (fun _ => (0 : Fin 3)) = if a = 0 then 0 else if a = 1 then 1 else 10 := by
    unfold PairModel.localE stateShareModel
    simp
  have l2 : stateShareModel.localE i 0 (fun _ => (0 : Fin 3)) = 0 := by
    unfold PairModel.localE stateShareModel
    simp
  linarith

/-- **Non-vacuity and strictness.**  On the witness — pair constant `3`, zero residual on the star — the
state-dependent shares satisfy the hypotheses of `secondOrder_certified_of_state_shares`, while the hypotheses of
`secondOrder_certified_of_deficit_shares` cannot be met by any deficits and constant shares: the pair of states `(1, 2)`
has the deficit `3`, and the cheapest states of the two sites can carry `1` each. -/
theorem stateShare_witness :
    (∀ i k a, 0 ≤ stateShareWitness i k a) ∧
    (∀ i k : Fin 2, i ≠ k → ∀ a b : Fin 3, a ≠ 0 → b ≠ 0 →
      3 - (pairSecondDiff stateShareModel (fun _ => 0) i k a b + pairSecondDiff stateShareModel (fun _ => 0) k i b a) ≤
        stateShareWitness i k a + stateShareWitness k i b) ∧
    (∀ (i : Fin 2) (a : Fin 3), a ≠ 0 → ∑ k ∈ (univ : Finset (Fin 2)).erase i, stateShareWitness i k a ≤
      (stateShareModel.energy (Function.update (fun _ => (0 : Fin 3)) i a) + 0) -
        (stateShareModel.energy (fun _ => (0 : Fin 3)) + 0)) ∧
    ¬ ∃ w s : Fin 2 → Fin 2 → ℝ,
      (∀ i k : Fin 2, i ≠ k → ∀ a b : Fin 3, a ≠ 0 → b ≠ 0 →
        3 - (pairSecondDiff stateShareModel (fun _ => 0) i k a b +
          pairSecondDiff stateShareModel (fun _ => 0) k i b a) ≤ w i k) ∧
      (∀ i k, i ≠ k → w i k ≤ s i k + s k i) ∧
      (∀ (i : Fin 2) (a : Fin 3), a ≠ 0 → ∑ k ∈ (univ : Finset (Fin 2)).erase i, s i k ≤
        (stateShareModel.energy (Function.update (fun _ => (0 : Fin 3)) i a) + 0) -
          (stateShareModel.energy (fun _ => (0 : Fin 3)) + 0)) := by
  have e0 : (univ : Finset (Fin 2)).erase 0 = {1} := by decide
  have e1 : (univ : Finset (Fin 2)).erase 1 = {0} := by decide
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro i k a
    unfold stateShareWitness
    split_ifs <;> norm_num
  · intro i k hik a b ha hb
    unfold pairSecondDiff stateShareModel stateShareWitness
    fin_cases i <;> fin_cases k <;> fin_cases a <;> fin_cases b <;> simp at hik ha hb ⊢ <;> norm_num
  · intro i a ha
    have hx := stateShareModel_excitation i a
    have hsum : ∑ k ∈ (univ : Finset (Fin 2)).erase i, stateShareWitness i k a = if a = 1 then 1 / 2 else 5 / 2 := by
      fin_cases i
      · simp [e0, stateShareWitness]
      · simp [e1, stateShareWitness]
    rw [hsum]
    fin_cases a <;> simp at ha hx ⊢ <;> linarith
  · rintro ⟨w, s, hw, hws, hload⟩
    have a1 := hw 0 1 (by decide) 1 2 (by decide) (by decide)
    have a2 := hws 0 1 (by decide)
    have a3 := hload 0 1 (by decide)
    have a4 := hload 1 1 (by decide)
    have x0 := stateShareModel_excitation 0 1
    have x1 := stateShareModel_excitation 1 1
    rw [e0, Finset.sum_singleton] at a3
    rw [e1, Finset.sum_singleton] at a4
    have d : pairSecondDiff stateShareModel (fun _ => 0) 0 1 (1 : Fin 3) (2 : Fin 3) +
        pairSecondDiff stateShareModel (fun _ => 0) 1 0 (2 : Fin 3) (1 : Fin 3) = 0 := by
      unfold pairSecondDiff stateShareModel
      simp
    rw [d] at a1
    simp at x0 x1
    linarith

end MetricChain
