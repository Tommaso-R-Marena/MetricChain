/-
Copyright (c) 2026 MetricChain contributors. Released under the Apache 2.0 license.
-/
import Mathlib

/-!
# Reduction of algorithms to type classes: the deterministic core

Theory report §11.25, Theorem 11.92.  For an exchangeable reference measure the quantity to be
estimated is `A = ∑ t, p t * A t`, where `t` runs over the type classes, `p t` is the known weight of
the class and `A t` the unknown mean of `e^{-ψ}` over it.  An algorithm keeps a bracket
`L t ≤ A t ≤ U t` for every class and always refines the class `k` with the largest `p t * U t`
("optimistic refinement").  This file contains the statements about that procedure that involve no
probability:

* `sum_mem_bracket`, `bracket_width` — the output `[p k * L k, card · p k * U k]` contains `A`, and its
  width is at most `card` times the width of the bracket of the maximising class;
* `argmax_deficit_le` — the maximising class is within its own bracket width of the largest term:
  a class is refined only if its deficit is at most the width of its bracket;
* `deficit_ge` — if the class means are Lipschitz across classes (`A t ≤ r t j * A j`), the largest
  term is at least `p j * A t / r t j` for every `j`: the deficits are bounded below by the gap between
  the weights and their Lipschitz minorant;
* `mean_le_of_biregular` — the double counting behind the Lipschitz property of the class means: in a
  biregular bipartite graph, a weight that grows by at most the factor `c` along every edge has means
  that differ by at most the factor `c`.

Paper statements that are *not* formalised here: that adjacent type classes of the cube are joined by
such a biregular graph (one switched coordinate), the probabilistic validity of the brackets, and the
count of evaluations.
-/

namespace MetricChain.SliceRefinement

open Finset

variable {ι : Type*} [Fintype ι]

/-- **Validity of the output of optimistic refinement.**  If `L t ≤ A t ≤ U t` for every class and `k`
maximises `p t * U t`, then `p k * L k ≤ ∑ t, p t * A t ≤ card ι * (p k * U k)`. -/
theorem sum_mem_bracket (p A L U : ι → ℝ) (hp : ∀ t, 0 ≤ p t) (hA : ∀ t, 0 ≤ A t)
    (hL : ∀ t, L t ≤ A t) (hU : ∀ t, A t ≤ U t) (k : ι) (hk : ∀ t, p t * U t ≤ p k * U k) :
    p k * L k ≤ ∑ t, p t * A t ∧ ∑ t, p t * A t ≤ Fintype.card ι * (p k * U k) := by
  constructor
  · calc p k * L k ≤ p k * A k := mul_le_mul_of_nonneg_left (hL k) (hp k)
      _ ≤ ∑ t, p t * A t :=
        single_le_sum (f := fun t => p t * A t) (fun t _ => mul_nonneg (hp t) (hA t)) (mem_univ k)
  · calc ∑ t, p t * A t ≤ ∑ _t : ι, p k * U k :=
        sum_le_sum fun t _ => (mul_le_mul_of_nonneg_left (hU t) (hp t)).trans (hk t)
      _ = Fintype.card ι * (p k * U k) := by
        simp [Finset.sum_const, nsmul_eq_mul, Finset.card_univ]

/-- **Width of the output.**  If the bracket of the maximising class has ratio at most `c`, the output
bracket has ratio at most `card ι * c`. -/
theorem bracket_width (p L U : ι → ℝ) (c : ℝ) (k : ι) (hp : 0 ≤ p k) (hc : U k ≤ c * L k) :
    Fintype.card ι * (p k * U k) ≤ Fintype.card ι * c * (p k * L k) := by
  have h : p k * U k ≤ c * (p k * L k) := by
    calc p k * U k ≤ p k * (c * L k) := mul_le_mul_of_nonneg_left hc hp
      _ = c * (p k * L k) := by ring
  calc (Fintype.card ι : ℝ) * (p k * U k) ≤ Fintype.card ι * (c * (p k * L k)) :=
        mul_le_mul_of_nonneg_left h (Nat.cast_nonneg _)
    _ = Fintype.card ι * c * (p k * L k) := by ring

omit [Fintype ι] in
/-- **A class is refined only if its deficit is at most its bracket.**  If `k` maximises `p t * U t`
and its bracket has ratio at most `c` (`U k ≤ c * A k`), then every term `p j * A j` is at most
`c * (p k * A k)`. -/
theorem argmax_deficit_le (p A U : ι → ℝ) (c : ℝ) (hp : ∀ t, 0 ≤ p t) (hU : ∀ t, A t ≤ U t) (k : ι)
    (hk : ∀ t, p t * U t ≤ p k * U k) (hc : U k ≤ c * A k) (j : ι) :
    p j * A j ≤ c * (p k * A k) := by
  calc p j * A j ≤ p j * U j := mul_le_mul_of_nonneg_left (hU j) (hp j)
    _ ≤ p k * U k := hk j
    _ ≤ p k * (c * A k) := mul_le_mul_of_nonneg_left hc (hp k)
    _ = c * (p k * A k) := by ring

omit [Fintype ι] in
/-- **Deficits are bounded below by the gap to the Lipschitz minorant of the weights.**  If the class
means satisfy `A t ≤ r t j * A j` (for the cube: `r t j = e^{u|t-j|}`) and `M` bounds all terms
`p j * A j`, then `p j * A t ≤ r t j * M` for all `t`, `j`: in logarithms,
`ln M - ln (p t * A t) ≥ max_j [ln p j - u|t - j|] - ln p t`. -/
theorem deficit_ge (p A : ι → ℝ) (r : ι → ι → ℝ) (hp : ∀ t, 0 ≤ p t) (hr : ∀ t j, 0 ≤ r t j)
    (hA : ∀ t j, A t ≤ r t j * A j) (M : ℝ) (hM : ∀ j, p j * A j ≤ M) (t j : ι) :
    p j * A t ≤ r t j * M := by
  calc p j * A t ≤ p j * (r t j * A j) := mul_le_mul_of_nonneg_left (hA t j) (hp j)
    _ = r t j * (p j * A j) := by ring
    _ ≤ r t j * M := mul_le_mul_of_nonneg_left (hM j) (hr t j)

/-- **Double counting in a biregular bipartite graph.**  Let `E ⊆ S × T` be a set of edges such that
every `s ∈ S` lies on exactly `a` edges and every `t ∈ T` on exactly `b` edges (`a, b > 0`).  If
`w s ≤ c * w' t` along every edge, then the mean of `w` over `S` is at most `c` times the mean of `w'`
over `T`.  (For two adjacent type classes of the cube, joined by switching one coordinate, `a = t + 1`
and `b = n - t`; with `w = w' = e^{-ψ}` and `c = e^u` this is Theorem 11.92(a).) -/
theorem mean_le_of_biregular {α β : Type*} [DecidableEq α] [DecidableEq β] (S : Finset α)
    (T : Finset β) (E : Finset (α × β)) (a b : ℕ) (ha : 0 < a) (hb : 0 < b)
    (hE : ∀ e ∈ E, e.1 ∈ S ∧ e.2 ∈ T)
    (hS : ∀ s ∈ S, #{e ∈ E | e.1 = s} = a) (hT : ∀ t ∈ T, #{e ∈ E | e.2 = t} = b)
    (w : α → ℝ) (w' : β → ℝ) (c : ℝ) (hw : ∀ e ∈ E, w e.1 ≤ c * w' e.2) :
    (∑ s ∈ S, w s) / #S ≤ c * ((∑ t ∈ T, w' t) / #T) := by
  -- sums over edges, fibred over either side
  have h1 : ∑ e ∈ E, w e.1 = a * ∑ s ∈ S, w s := by
    rw [← Finset.sum_fiberwise_of_maps_to (g := fun e : α × β => e.1) (fun e he => (hE e he).1),
      Finset.mul_sum]
    refine Finset.sum_congr rfl fun s hs => ?_
    rw [Finset.sum_congr rfl (fun e he => by rw [(Finset.mem_filter.mp he).2] : ∀ e ∈ E.filter
      (fun e => e.1 = s), w e.1 = w s), Finset.sum_const, hS s hs, nsmul_eq_mul]
  have h2 : ∑ e ∈ E, w' e.2 = b * ∑ t ∈ T, w' t := by
    rw [← Finset.sum_fiberwise_of_maps_to (g := fun e : α × β => e.2) (fun e he => (hE e he).2),
      Finset.mul_sum]
    refine Finset.sum_congr rfl fun t ht => ?_
    rw [Finset.sum_congr rfl (fun e he => by rw [(Finset.mem_filter.mp he).2] : ∀ e ∈ E.filter
      (fun e => e.2 = t), w' e.2 = w' t), Finset.sum_const, hT t ht, nsmul_eq_mul]
  have hc1 : (#E : ℝ) = a * #S := by
    have := Finset.card_eq_sum_card_fiberwise (f := fun e : α × β => e.1) (s := E) (t := S)
      (fun e he => (hE e he).1)
    rw [this, Finset.sum_congr rfl hS]
    simp [mul_comm]
  have hc2 : (#E : ℝ) = b * #T := by
    have := Finset.card_eq_sum_card_fiberwise (f := fun e : α × β => e.2) (s := E) (t := T)
      (fun e he => (hE e he).2)
    rw [this, Finset.sum_congr rfl hT]
    simp [mul_comm]
  have hmain : (a : ℝ) * ∑ s ∈ S, w s ≤ c * (b * ∑ t ∈ T, w' t) := by
    rw [← h1, ← h2, Finset.mul_sum]
    exact Finset.sum_le_sum hw
  have ha' : (0 : ℝ) < a := by exact_mod_cast ha
  have hb' : (0 : ℝ) < b := by exact_mod_cast hb
  by_cases hS0 : #S = 0
  · -- no points on the left: then there are no edges, hence no points on the right either
    have hS0' : (#S : ℝ) = 0 := by exact_mod_cast hS0
    have hT0 : (#T : ℝ) = 0 := by
      have h0 : (b : ℝ) * #T = 0 := by rw [← hc2, hc1, hS0', mul_zero]
      rcases mul_eq_zero.mp h0 with h | h
      · exact absurd h hb'.ne'
      · exact h
    rw [hS0', hT0, div_zero, div_zero, mul_zero]
  have hSpos : (0 : ℝ) < #S := by exact_mod_cast Nat.pos_of_ne_zero hS0
  have hTpos : (0 : ℝ) < #T := by
    have : (0 : ℝ) < b * #T := by rw [← hc2, hc1]; positivity
    exact (mul_pos_iff_of_pos_left hb').mp this
  have h3 : (a : ℝ) * #S = b * #T := by rw [← hc1, hc2]
  have h4 : (∑ t ∈ T, w' t) / #T * (b * #T) = b * ∑ t ∈ T, w' t := by
    rw [div_mul_eq_mul_div, div_eq_iff hTpos.ne']
    ring
  rw [div_le_iff₀ hSpos]
  have h5 : (a : ℝ) * (c * ((∑ t ∈ T, w' t) / #T) * #S) = c * (b * ∑ t ∈ T, w' t) := by
    calc (a : ℝ) * (c * ((∑ t ∈ T, w' t) / #T) * #S)
        = c * ((∑ t ∈ T, w' t) / #T * (a * #S)) := by ring
      _ = c * (b * ∑ t ∈ T, w' t) := by rw [h3, h4]
  have h6 : (a : ℝ) * ∑ s ∈ S, w s ≤ a * (c * ((∑ t ∈ T, w' t) / #T) * #S) := by
    rw [h5]
    exact hmain
  exact le_of_mul_le_mul_left h6 ha'

end MetricChain.SliceRefinement
