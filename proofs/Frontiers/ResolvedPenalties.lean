import Mathlib
import proofs.Frontiers.TermOrders

/-!
# Resolved penalties: state-dependent remainder bounds charged to sub-tuples

`AnchoredRemainder.lean` and `TermOrders.lean` bound the remainder of the anchored expansion of
order `m - 1` at a configuration `x` by a sum of constants over the `m`-subsets `T` of the changed
sites `supp x₀ x` (the sites at which `x` differs from the anchor `x₀`).  The constant of `T` may
depend on the states that `x` has on `T`; the bound is then a sum
`∑_{T ⊆ supp x₀ x, |T| = m} Φ T x` over `m`-tuples of sites.  This file proves that such a sum is
dominated by tables `γ U x` indexed by the non-empty sub-tuples `U` of the changed sites, as soon
as every `Φ T` is distributed over the sub-tuples of `T` with weights that add up to one.

The statements are the Scientific Discovery Division's (message SCI-MSG-0028 §7, workstream P9:
its Proposition P and its Theorem R; requests P9-T1 and P9-T3).  The paper proofs were re-derived
by the coordinator from that message; this file is their machine check.  Added in the
formalisation: `order_pos_of_weights`, `maxTable_congr`, `maxTable_le`,
`anchored_remainder_bound_orders_off_anchor` and `resolved_remainder_bound`.

## Setting

Sites `ι` (a finite type), state spaces `σ i`, states `x : ∀ i, σ i`, the anchor `x₀`, and
`supp x₀ x` of `HigherOrderEnvelope.lean`.  A state is *off the anchor on `T`* if `T ⊆ supp x₀ x`.
All tables are functions of the whole state; that a table `γ U` reads the states of the sites of
`U` only is a property of the tables one inserts and is not used.

## Results

* `resolved_allocation` — **Proposition P.**  Weights `w T U ≥ 0` on the non-empty `U ⊆ T` with
  sum one, tables `c T U x ≥ 0` that dominate `Φ T x` at the states off the anchor on `T`, and
  `γ U x ≥ ∑_{T ⊇ U, |T| = m} w T U * c T U x` at the states off the anchor on `U`.  Then
  `∑_{T ⊆ supp x₀ x, |T| = m} Φ T x ≤ ∑_{∅ ≠ U ⊆ supp x₀ x} γ U x` for every state `x`.
  `resolved_allocation_univ`: for `γ ≥ 0` the right-hand side may be taken over all non-empty
  `U`.  `order_pos_of_weights`: the hypothesis on the weights forces `0 < m`, so no side
  condition on `m` is needed.
* `fibreOff`, `maxTable`, `resolved_allocation_max` — the same with the least tables: `c T U x`
  is the maximum of `Φ T` over the states that agree with `x` on `U` and are off the anchor on
  `T` (`le_maxTable`, `maxTable_nonneg`); it depends on the states of `U` only (`maxTable_congr`)
  and is below every other non-negative bound of that kind (`maxTable_le`).
* `reduction_step` — **the reduction step.**  For non-empty `V ⊆ U` the table of `U` may be given
  up for a non-negative table `γ'` at the index `V` that is at least `γ U y` for all states `y`
  that agree with `x` on `V` (and are off the anchor on `U`): the right-hand side of
  `resolved_allocation` does not decrease.
* `anchored_remainder_bound_orders_state` — **the remainder bound with constants that depend on
  the actual state** (request P9-T3): `anchored_remainder_bound_orders` of `TermOrders.lean` needs
  its hypothesis on the constants at the configuration `y` at hand only, so the constants may be
  functions `c τ T y` of that configuration.  `anchored_remainder_bound_orders_off_anchor`: its
  proof uses that hypothesis for the `m`-subsets `T` of the changed sites only, so the constants
  are needed at the configurations off the anchor on `T` only.
* `resolved_remainder_bound` — the two statements combined: the remainder of the anchored
  expansion at `y` is at most `∑_{∅ ≠ U ⊆ supp x₀ y} γ U y`.

## Proof of Proposition P

For `T ⊆ supp x₀ x` with `|T| = m`: `Φ T x = ∑_U w T U * Φ T x ≤ ∑_{∅ ≠ U ⊆ T} w T U * c T U x`.
Sum over `T` and exchange the two sums (`U ⊆ T ⊆ supp x₀ x` gives `U ⊆ supp x₀ x`); enlarge the
inner sum from the `m`-sets `T` with `U ⊆ T ⊆ supp x₀ x` to all `m`-sets `T ⊇ U` (the terms are
non-negative); use the hypothesis on `γ`.

## Not proved here

That the weights and the tables of an actual certificate satisfy the hypotheses (sum one,
domination, the inequality for `γ`): these are finite checks on the numbers of the certificate
and are not part of this file.  Nothing is proved about the transfer matrices, and nothing about
floating-point arithmetic.
-/

namespace MetricChain.ResolvedPenalties

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-! ### Proposition P -/

/-- **Proposition P (state-dependent bounds charged to sub-tuples).**  For every set `T` of `m`
sites let `Φ T x` be a number that depends on the state `x`.  Let `w T U ≥ 0` be weights on the
non-empty subsets `U` of `T` that add up to one, let the tables `c T U x ≥ 0` dominate `Φ T x`
at the states `x` that are off the anchor on `T`, and let `γ U x` be at least
`∑_{T ⊇ U, |T| = m} w T U * c T U x` at the states that are off the anchor on `U`.  Then at every
state `x` the numbers `Φ T x` of the `m`-subsets `T` of the changed sites add up to at most the
tables of the non-empty subsets of the changed sites:

`∑_{T ⊆ supp x₀ x, |T| = m} Φ T x ≤ ∑_{∅ ≠ U ⊆ supp x₀ x} γ U x`.

The hypotheses on `w` and `c` are needed for `|T| = m` and non-empty `U ⊆ T` only; nothing is
assumed about the signs of `Φ` and `γ`, and nothing about `m` (`order_pos_of_weights`). -/
theorem resolved_allocation [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ)
    (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ) (w : Finset ι → Finset ι → ℝ)
    (c : Finset ι → Finset ι → (∀ i, σ i) → ℝ) (γ : Finset ι → (∀ i, σ i) → ℝ)
    (hw0 : ∀ T U, T.card = m → U.Nonempty → U ⊆ T → 0 ≤ w T U)
    (hw1 : ∀ T, T.card = m → ∑ U ∈ T.powerset.filter (·.Nonempty), w T U = 1)
    (hc : ∀ T U x, T.card = m → U.Nonempty → U ⊆ T → T ⊆ supp x₀ x → Φ T x ≤ c T U x)
    (hc0 : ∀ T U x, T.card = m → U.Nonempty → U ⊆ T → 0 ≤ c T U x)
    (hγ : ∀ U x, U.Nonempty → U ⊆ supp x₀ x →
      ∑ T ∈ (univ.powersetCard m).filter (U ⊆ ·), w T U * c T U x ≤ γ U x)
    (x : ∀ i, σ i) :
    ∑ T ∈ (supp x₀ x).powersetCard m, Φ T x ≤
      ∑ U ∈ (supp x₀ x).powerset.filter (·.Nonempty), γ U x := by
  calc ∑ T ∈ (supp x₀ x).powersetCard m, Φ T x
      ≤ ∑ T ∈ (supp x₀ x).powersetCard m,
          ∑ U ∈ T.powerset.filter (·.Nonempty), w T U * c T U x := by
        refine Finset.sum_le_sum fun T hT => ?_
        obtain ⟨hTS, hTm⟩ := Finset.mem_powersetCard.mp hT
        calc Φ T x = (∑ U ∈ T.powerset.filter (·.Nonempty), w T U) * Φ T x := by
              rw [hw1 T hTm, one_mul]
          _ = ∑ U ∈ T.powerset.filter (·.Nonempty), w T U * Φ T x := Finset.sum_mul _ _ _
          _ ≤ ∑ U ∈ T.powerset.filter (·.Nonempty), w T U * c T U x := by
              refine Finset.sum_le_sum fun U hU => ?_
              obtain ⟨hUT, hUne⟩ := Finset.mem_filter.mp hU
              have hUT' : U ⊆ T := Finset.mem_powerset.mp hUT
              exact mul_le_mul_of_nonneg_left (hc T U x hTm hUne hUT' hTS)
                (hw0 T U hTm hUne hUT')
    _ = ∑ U ∈ (supp x₀ x).powerset.filter (·.Nonempty),
          ∑ T ∈ ((supp x₀ x).powersetCard m).filter (U ⊆ ·), w T U * c T U x := by
        refine Finset.sum_comm' fun T U => ?_
        simp only [Finset.mem_powersetCard, Finset.mem_filter, Finset.mem_powerset]
        constructor
        · rintro ⟨⟨hTS, hTm⟩, hUT, hU⟩
          exact ⟨⟨⟨hTS, hTm⟩, hUT⟩, hUT.trans hTS, hU⟩
        · rintro ⟨⟨⟨hTS, hTm⟩, hUT⟩, _, hU⟩
          exact ⟨⟨hTS, hTm⟩, hUT, hU⟩
    _ ≤ ∑ U ∈ (supp x₀ x).powerset.filter (·.Nonempty),
          ∑ T ∈ (univ.powersetCard m).filter (U ⊆ ·), w T U * c T U x := by
        refine Finset.sum_le_sum fun U hU => ?_
        have hUne : U.Nonempty := (Finset.mem_filter.mp hU).2
        refine Finset.sum_le_sum_of_subset_of_nonneg
          (Finset.filter_subset_filter _ (Finset.powersetCard_mono (Finset.subset_univ _)))
          fun T hT _ => ?_
        obtain ⟨hT1, hUT⟩ := Finset.mem_filter.mp hT
        have hTm : T.card = m := (Finset.mem_powersetCard.mp hT1).2
        exact mul_nonneg (hw0 T U hTm hUne hUT) (hc0 T U x hTm hUne hUT)
    _ ≤ ∑ U ∈ (supp x₀ x).powerset.filter (·.Nonempty), γ U x := by
        refine Finset.sum_le_sum fun U hU => ?_
        obtain ⟨hUS, hUne⟩ := Finset.mem_filter.mp hU
        exact hγ U x hUne (Finset.mem_powerset.mp hUS)

/-- **Proposition P, sum over all non-empty sub-tuples.**  For non-negative tables `γ` the
right-hand side of `resolved_allocation` may be extended to all non-empty sets `U` of sites:
`∑_{T ⊆ supp x₀ x, |T| = m} Φ T x ≤ ∑_{U ≠ ∅} γ U x`. -/
theorem resolved_allocation_univ [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ)
    (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ) (w : Finset ι → Finset ι → ℝ)
    (c : Finset ι → Finset ι → (∀ i, σ i) → ℝ) (γ : Finset ι → (∀ i, σ i) → ℝ)
    (hw0 : ∀ T U, T.card = m → U.Nonempty → U ⊆ T → 0 ≤ w T U)
    (hw1 : ∀ T, T.card = m → ∑ U ∈ T.powerset.filter (·.Nonempty), w T U = 1)
    (hc : ∀ T U x, T.card = m → U.Nonempty → U ⊆ T → T ⊆ supp x₀ x → Φ T x ≤ c T U x)
    (hc0 : ∀ T U x, T.card = m → U.Nonempty → U ⊆ T → 0 ≤ c T U x)
    (hγ : ∀ U x, U.Nonempty → U ⊆ supp x₀ x →
      ∑ T ∈ (univ.powersetCard m).filter (U ⊆ ·), w T U * c T U x ≤ γ U x)
    (hγ0 : ∀ U x, 0 ≤ γ U x) (x : ∀ i, σ i) :
    ∑ T ∈ (supp x₀ x).powersetCard m, Φ T x ≤
      ∑ U ∈ (univ : Finset ι).powerset.filter (·.Nonempty), γ U x :=
  (resolved_allocation m x₀ Φ w c γ hw0 hw1 hc hc0 hγ x).trans
    (Finset.sum_le_sum_of_subset_of_nonneg
      (Finset.filter_subset_filter _ (Finset.powerset_mono.mpr (Finset.subset_univ _)))
      fun U _ _ => hγ0 U x)

/-- Weights with sum one on the non-empty subsets of every `m`-set exist for `m ≥ 1` only: the
empty set has no non-empty subset.  So `resolved_allocation` needs no side condition on `m`. -/
theorem order_pos_of_weights (m : ℕ) (w : Finset ι → Finset ι → ℝ)
    (hw1 : ∀ T : Finset ι, T.card = m → ∑ U ∈ T.powerset.filter (·.Nonempty), w T U = 1) :
    0 < m := by
  rcases Nat.eq_zero_or_pos m with h | h
  · have h1 := hw1 ∅ (by rw [Finset.card_empty, h])
    rw [Finset.powerset_empty, Finset.filter_singleton, if_neg Finset.not_nonempty_empty,
      Finset.sum_empty] at h1
    exact absurd h1 zero_ne_one
  · exact h

/-! ### The least tables: maxima over the states that agree on the sub-tuple -/

/-- The states `y` that agree with `x` on `U` and are off the anchor at every site of `T`. -/
def fibreOff [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)] [∀ i, DecidableEq (σ i)]
    (x₀ : ∀ i, σ i) (T U : Finset ι) (x : ∀ i, σ i) : Finset (∀ i, σ i) :=
  univ.filter fun y => (∀ i ∈ U, y i = x i) ∧ T ⊆ supp x₀ y

/-- Membership in `fibreOff`. -/
theorem mem_fibreOff [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)] [∀ i, DecidableEq (σ i)]
    {x₀ : ∀ i, σ i} {T U : Finset ι} {x y : ∀ i, σ i} :
    y ∈ fibreOff x₀ T U x ↔ (∀ i ∈ U, y i = x i) ∧ T ⊆ supp x₀ y := by
  simp [fibreOff]

/-- `fibreOff x₀ T U x` depends on the states of `x` on `U` only. -/
theorem fibreOff_congr [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)]
    [∀ i, DecidableEq (σ i)] (x₀ : ∀ i, σ i) (T : Finset ι) {U : Finset ι} {x x' : ∀ i, σ i}
    (h : ∀ i ∈ U, x i = x' i) : fibreOff x₀ T U x = fibreOff x₀ T U x' := by
  ext y
  simp only [mem_fibreOff]
  constructor
  · rintro ⟨h1, h2⟩
    exact ⟨fun i hi => (h1 i hi).trans (h i hi), h2⟩
  · rintro ⟨h1, h2⟩
    exact ⟨fun i hi => (h1 i hi).trans (h i hi).symm, h2⟩

/-- **The table of maxima** `c T U x = max {Φ T y : y agrees with x on U, y off the anchor on T}`,
and `0` if there is no such state (then `x` itself is not off the anchor on `T`). -/
noncomputable def maxTable [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)]
    [∀ i, DecidableEq (σ i)] (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ) (T U : Finset ι)
    (x : ∀ i, σ i) : ℝ :=
  if h : (fibreOff x₀ T U x).Nonempty then (fibreOff x₀ T U x).sup' h (Φ T) else 0

/-- The table of maxima depends on the states of `x` on `U` only. -/
theorem maxTable_congr [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)]
    [∀ i, DecidableEq (σ i)] (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ) (T : Finset ι)
    {U : Finset ι} {x x' : ∀ i, σ i} (h : ∀ i ∈ U, x i = x' i) :
    maxTable x₀ Φ T U x = maxTable x₀ Φ T U x' := by
  unfold maxTable
  simp only [fibreOff_congr x₀ T h]

/-- The table of maxima dominates `Φ T` at the states that are off the anchor on `T`. -/
theorem le_maxTable [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)] [∀ i, DecidableEq (σ i)]
    (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ) {T : Finset ι} (U : Finset ι)
    {x : ∀ i, σ i} (hT : T ⊆ supp x₀ x) : Φ T x ≤ maxTable x₀ Φ T U x := by
  have hx : x ∈ fibreOff x₀ T U x := mem_fibreOff.mpr ⟨fun _ _ => rfl, hT⟩
  unfold maxTable
  rw [dif_pos ⟨x, hx⟩]
  exact Finset.le_sup' (Φ T) hx

/-- The table of maxima is non-negative if `Φ T` is non-negative at the states that are off the
anchor on `T`. -/
theorem maxTable_nonneg [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)]
    [∀ i, DecidableEq (σ i)] (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ) {T : Finset ι}
    (U : Finset ι) (x : ∀ i, σ i) (hΦ : ∀ y, T ⊆ supp x₀ y → 0 ≤ Φ T y) :
    0 ≤ maxTable x₀ Φ T U x := by
  unfold maxTable
  split_ifs with h
  · obtain ⟨y, hy⟩ := h
    exact (hΦ y (mem_fibreOff.mp hy).2).trans (Finset.le_sup' (Φ T) hy)
  · exact le_rfl

/-- The table of maxima is the least one: it is below every non-negative number that bounds
`Φ T` at all the states that agree with `x` on `U` and are off the anchor on `T`. -/
theorem maxTable_le [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)] [∀ i, DecidableEq (σ i)]
    (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ) (T U : Finset ι) (x : ∀ i, σ i) {b : ℝ}
    (hb : 0 ≤ b) (h : ∀ y, (∀ i ∈ U, y i = x i) → T ⊆ supp x₀ y → Φ T y ≤ b) :
    maxTable x₀ Φ T U x ≤ b := by
  unfold maxTable
  split_ifs with hne
  · exact (Finset.sup'_le_iff hne (Φ T)).mpr fun y hy =>
      h y (mem_fibreOff.mp hy).1 (mem_fibreOff.mp hy).2
  · exact hb

/-- **Proposition P with the tables of maxima.**  `resolved_allocation` for
`c T U x = max {Φ T y : y agrees with x on U, y off the anchor on T}`: if `Φ T x ≥ 0` at the
states off the anchor on the `m`-set `T`, the weights `w T U ≥ 0` add up to one, and
`γ U x ≥ ∑_{T ⊇ U, |T| = m} w T U * maxTable x₀ Φ T U x` at the states off the anchor on `U`, then
`∑_{T ⊆ supp x₀ x, |T| = m} Φ T x ≤ ∑_{∅ ≠ U ⊆ supp x₀ x} γ U x`. -/
theorem resolved_allocation_max [Fintype ι] [DecidableEq ι] [∀ i, Fintype (σ i)]
    [∀ i, DecidableEq (σ i)] (m : ℕ) (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ)
    (w : Finset ι → Finset ι → ℝ) (γ : Finset ι → (∀ i, σ i) → ℝ)
    (hΦ0 : ∀ T x, T.card = m → T ⊆ supp x₀ x → 0 ≤ Φ T x)
    (hw0 : ∀ T U, T.card = m → U.Nonempty → U ⊆ T → 0 ≤ w T U)
    (hw1 : ∀ T, T.card = m → ∑ U ∈ T.powerset.filter (·.Nonempty), w T U = 1)
    (hγ : ∀ U x, U.Nonempty → U ⊆ supp x₀ x →
      ∑ T ∈ (univ.powersetCard m).filter (U ⊆ ·), w T U * maxTable x₀ Φ T U x ≤ γ U x)
    (x : ∀ i, σ i) :
    ∑ T ∈ (supp x₀ x).powersetCard m, Φ T x ≤
      ∑ U ∈ (supp x₀ x).powerset.filter (·.Nonempty), γ U x :=
  resolved_allocation m x₀ Φ w (maxTable x₀ Φ) γ hw0 hw1
    (fun _ U _ _ _ _ hT => le_maxTable x₀ Φ U hT)
    (fun T U x hTm _ _ => maxTable_nonneg x₀ Φ U x fun y hy => hΦ0 T y hTm hy) hγ x

/-! ### The reduction step -/

/-- **The reduction step.**  A table may be given up for a table on a sub-tuple.  Let `V ⊆ U` be
non-empty and let `γ'` be a table with `γ' x ≥ γ U y` for every state `y` that agrees with `x` on
`V` and is off the anchor on `U` (for instance the maximum of `γ U` over the states of the sites
of `U` outside `V`), non-negative at the states off the anchor on `V`.  Then the right-hand side
of `resolved_allocation` does not decrease if the table of `U` is removed and `γ'` is added at
the index `V`; hence the new tables bound whatever the old ones bound.  (Of the states `y` only
`y = x` enters the proof; the hypothesis has the form that a table reading the states of `V`
only has to meet.  If `γ U ≥ 0` and `γ' x ≥ γ U y` for all `y` that agree with `x` on `V`, then
`γ' ≥ 0` and both hypotheses on `γ'` hold.) -/
theorem reduction_step [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (x₀ : ∀ i, σ i)
    (γ : Finset ι → (∀ i, σ i) → ℝ) (U V : Finset ι) (γ' : (∀ i, σ i) → ℝ)
    (hV : V.Nonempty) (hVU : V ⊆ U)
    (hγ' : ∀ x y, (∀ i ∈ V, y i = x i) → U ⊆ supp x₀ y → γ U y ≤ γ' x)
    (hγ'0 : ∀ x, V ⊆ supp x₀ x → 0 ≤ γ' x) (x : ∀ i, σ i) :
    ∑ W ∈ (supp x₀ x).powerset.filter (·.Nonempty), γ W x ≤
      ∑ W ∈ (supp x₀ x).powerset.filter (·.Nonempty),
        ((if W = U then 0 else γ W x) + if W = V then γ' x else 0) := by
  have hsplit : ∀ W : Finset ι,
      γ W x = (if W = U then 0 else γ W x) + if W = U then γ U x else 0 := by
    intro W
    by_cases h : W = U
    · simp [h]
    · simp [h]
  rw [Finset.sum_congr rfl fun W _ => hsplit W, Finset.sum_add_distrib, Finset.sum_add_distrib,
    Finset.sum_ite_eq' _ U fun _ => γ U x, Finset.sum_ite_eq' _ V fun _ => γ' x]
  refine add_le_add le_rfl ?_
  by_cases hU : U ∈ (supp x₀ x).powerset.filter (·.Nonempty)
  · have hUS : U ⊆ supp x₀ x := Finset.mem_powerset.mp (Finset.mem_filter.mp hU).1
    have hV' : V ∈ (supp x₀ x).powerset.filter (·.Nonempty) :=
      Finset.mem_filter.mpr ⟨Finset.mem_powerset.mpr (hVU.trans hUS), hV⟩
    rw [if_pos hU, if_pos hV']
    exact hγ' x x (fun _ _ => rfl) hUS
  · rw [if_neg hU]
    split_ifs with hV'
    · exact hγ'0 x (Finset.mem_powerset.mp (Finset.mem_filter.mp hV').1)
    · exact le_rfl

/-! ### The remainder bound with constants that depend on the actual state -/

/-- **Remainder bound with host-anchored constants that depend on the actual state.**
`anchored_remainder_bound_orders` is a statement about one configuration `y`, and its hypothesis
on the constants is a hypothesis on the mixed differences with target states `y`.  Hence the
constants may be functions `c τ T y` of the configuration: if for every `y` they bound the mixed
differences of `F τ` over the `m`-sets `T` with target states `y`, at the base points that agree
with the anchor on `T` and at the hosts of `τ` outside `T`, then for every `y` the remainder of
the anchored expansion of order `m - 1` is at most `∑_τ ∑_{T ⊆ supp x₀ y, |T| = m} c τ T y`. -/
theorem anchored_remainder_bound_orders_state [Fintype ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] {κ : Type*} (m : ℕ) (terms : Finset κ) (F : κ → (∀ i, σ i) → ℝ)
    (ord : κ → LinearOrder ι) (H : κ → Finset ι) (c : κ → Finset ι → (∀ i, σ i) → ℝ)
    (x₀ : ∀ i, σ i)
    (hH : ∀ τ ∈ terms, ∀ h ∈ H τ, (univ.filter fun i => (ord τ).lt h i).card < m)
    (hc : ∀ y : ∀ i, σ i, ∀ τ ∈ terms, ∀ T : Finset ι, T.card = m → ∀ z : ∀ i, σ i,
      (∀ t ∈ T, z t = x₀ t) → (∀ h ∈ H τ, h ∉ T → z h = x₀ h) →
      |mixedDiff (F τ) z T y| ≤ c τ T y) (y : ∀ i, σ i) :
    |(∑ τ ∈ terms, F τ y) - anchoredInterp m (fun x => ∑ τ ∈ terms, F τ x) x₀ y| ≤
      ∑ τ ∈ terms, ∑ T ∈ (supp x₀ y).powersetCard m, c τ T y :=
  anchored_remainder_bound_orders m terms F ord H (fun τ T => c τ T y) x₀ y hH (hc y)

/-- **The same bound from constants on the changed sites only.**  The proof of
`anchored_remainder_bound_orders` uses the hypothesis on the constants for the `m`-subsets `T`
of the changed sites `supp x₀ y` only (the remainder identity
`anchored_remainder_identity_orders` has no other terms).  So state-dependent constants
`c τ T y` have to bound the mixed differences over `T` with target states `y` only at the
configurations `y` that are off the anchor on `T`. -/
theorem anchored_remainder_bound_orders_off_anchor [Fintype ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] {κ : Type*} (m : ℕ) (terms : Finset κ) (F : κ → (∀ i, σ i) → ℝ)
    (ord : κ → LinearOrder ι) (H : κ → Finset ι) (c : κ → Finset ι → (∀ i, σ i) → ℝ)
    (x₀ : ∀ i, σ i)
    (hH : ∀ τ ∈ terms, ∀ h ∈ H τ, (univ.filter fun i => (ord τ).lt h i).card < m)
    (hc : ∀ y : ∀ i, σ i, ∀ τ ∈ terms, ∀ T : Finset ι, T.card = m → T ⊆ supp x₀ y →
      ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) → (∀ h ∈ H τ, h ∉ T → z h = x₀ h) →
      |mixedDiff (F τ) z T y| ≤ c τ T y) (y : ∀ i, σ i) :
    |(∑ τ ∈ terms, F τ y) - anchoredInterp m (fun x => ∑ τ ∈ terms, F τ x) x₀ y| ≤
      ∑ τ ∈ terms, ∑ T ∈ (supp x₀ y).powersetCard m, c τ T y := by
  rw [anchored_remainder_identity_orders m terms F ord x₀ y]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun τ hτ => ?_)
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun T hT => ?_)
  obtain ⟨hTS, hTm⟩ := Finset.mem_powersetCard.mp hT
  refine hc y τ hτ T hTm hTS _ (fun t ht => ?_) (fun h hh _ => ?_)
  · exact @remainderBase_on ι σ _ _ (ord τ) _ x₀ y T t ht
  · exact @remainderBase_host_anchor ι σ _ _ (ord τ) _ x₀ y T h
      (lt_of_lt_of_eq (hH τ hτ h hh) hTm.symm)

/-- **The remainder bound and Proposition P combined.**  With state-dependent host-anchored
constants `Θ τ T y` as in `anchored_remainder_bound_orders_off_anchor`, and weights `w` and tables
`c`, `γ` as in `resolved_allocation` for the bounds `Φ T y = ∑_τ Θ τ T y`, the remainder of the
anchored expansion of order `m - 1` at `y` is at most the sum of the tables of the non-empty
subsets of the changed sites:
`|∑_τ F τ y - anchoredInterp m (∑_τ F τ) x₀ y| ≤ ∑_{∅ ≠ U ⊆ supp x₀ y} γ U y`. -/
theorem resolved_remainder_bound [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    {κ : Type*} (m : ℕ) (terms : Finset κ) (F : κ → (∀ i, σ i) → ℝ) (ord : κ → LinearOrder ι)
    (H : κ → Finset ι) (Θ : κ → Finset ι → (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i)
    (w : Finset ι → Finset ι → ℝ) (c : Finset ι → Finset ι → (∀ i, σ i) → ℝ)
    (γ : Finset ι → (∀ i, σ i) → ℝ)
    (hH : ∀ τ ∈ terms, ∀ h ∈ H τ, (univ.filter fun i => (ord τ).lt h i).card < m)
    (hΘ : ∀ y : ∀ i, σ i, ∀ τ ∈ terms, ∀ T : Finset ι, T.card = m → T ⊆ supp x₀ y →
      ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) → (∀ h ∈ H τ, h ∉ T → z h = x₀ h) →
      |mixedDiff (F τ) z T y| ≤ Θ τ T y)
    (hw0 : ∀ T U, T.card = m → U.Nonempty → U ⊆ T → 0 ≤ w T U)
    (hw1 : ∀ T, T.card = m → ∑ U ∈ T.powerset.filter (·.Nonempty), w T U = 1)
    (hc : ∀ T U x, T.card = m → U.Nonempty → U ⊆ T → T ⊆ supp x₀ x →
      ∑ τ ∈ terms, Θ τ T x ≤ c T U x)
    (hc0 : ∀ T U x, T.card = m → U.Nonempty → U ⊆ T → 0 ≤ c T U x)
    (hγ : ∀ U x, U.Nonempty → U ⊆ supp x₀ x →
      ∑ T ∈ (univ.powersetCard m).filter (U ⊆ ·), w T U * c T U x ≤ γ U x)
    (y : ∀ i, σ i) :
    |(∑ τ ∈ terms, F τ y) - anchoredInterp m (fun x => ∑ τ ∈ terms, F τ x) x₀ y| ≤
      ∑ U ∈ (supp x₀ y).powerset.filter (·.Nonempty), γ U y := by
  refine (anchored_remainder_bound_orders_off_anchor m terms F ord H Θ x₀ hH hΘ y).trans ?_
  rw [Finset.sum_comm]
  exact resolved_allocation m x₀ (fun T x => ∑ τ ∈ terms, Θ τ T x) w c γ hw0 hw1 hc hc0 hγ y

end MetricChain.ResolvedPenalties
