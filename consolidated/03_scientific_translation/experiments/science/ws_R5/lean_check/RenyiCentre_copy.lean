/-
Copyright (c) 2026 MetricChain contributors. Released under the Apache 2.0 license.
-/
import Mathlib

/-!
# The hardest additive instance is a Rényi centre: the two elementary steps

Theory report §11.26, Theorem 11.99.  For a site with law `π`, Lipschitz polytope `L` and vertex
functions `φ`, the value of the game of an additive instance with Gibbs law `P` against a mixture
`M` of vertices is `min_a (P a / m a)^t` up to monotone transformations, where
`m a = (∑ φ, M φ · π_φ a ^ t)^(1/t)`.  The proof that the best instance is the one with `P ∝ m` (the
Rényi centre), and that this instance belongs to the class, rests on two elementary facts, which
are what this file contains:

* `exists_ratio_le`, `scale_le_inv_sum`, `eq_of_forall_ratio_ge` — for a probability vector `P` and a
  positive vector `m`, some ratio `P a / m a` is at most `1 / ∑ m`, with equality in all
  coordinates only for `P = m / ∑ m`;
* `softmin_admissible` — the class `{γ : γ a - γ b ≤ d a b}` is closed under soft minima
  `γ a = -(1/t) · log ∑ i, M i · exp (-t · φ i a)`; no symmetry of `d` is used.

Not formalised: the minimax theorem for the matrix game, the identification of
`-t · log ∑ a, m a` with `(1 - t)` times Sibson's information, and Csiszár's theorem that its
maximum over `M` is the Rényi radius.
-/

namespace MetricChain.RenyiCentre

open Finset

variable {ι : Type*} [Fintype ι]

/-- If `c • m ≤ P` pointwise for a probability vector `P` and a vector `m` of positive total mass,
then `c ≤ 1 / ∑ m`. -/
theorem scale_le_inv_sum (P m : ι → ℝ) (c : ℝ) (hP : ∑ a, P a = 1) (hs : 0 < ∑ a, m a)
    (h : ∀ a, c * m a ≤ P a) : c ≤ 1 / ∑ a, m a := by
  rw [le_div_iff₀ hs]
  calc c * ∑ a, m a = ∑ a, c * m a := by rw [mul_sum]
    _ ≤ ∑ a, P a := sum_le_sum fun a _ => h a
    _ = 1 := hP

/-- **Some ratio is small.**  For a probability vector `P` and a positive vector `m` there is a
letter with `P a / m a ≤ 1 / ∑ m`: against the mixture `M`, no instance has a game value above the
Rényi value. -/
theorem exists_ratio_le [Nonempty ι] (P m : ι → ℝ) (hP : ∑ a, P a = 1) (hm : ∀ a, 0 < m a) :
    ∃ a, P a / m a ≤ 1 / ∑ a, m a := by
  have hs : 0 < ∑ a, m a := sum_pos (fun a _ => hm a) univ_nonempty
  by_contra hcon
  simp only [not_exists, not_le] at hcon
  have hlt : ∑ a, m a / ∑ b, m b < ∑ a, P a := by
    apply sum_lt_sum_of_nonempty univ_nonempty
    intro a _
    have h1 := hcon a
    rw [lt_div_iff₀ (hm a)] at h1
    calc m a / ∑ b, m b = (1 / ∑ b, m b) * m a := by ring
      _ < P a := h1
  rw [← sum_div, div_self hs.ne', hP] at hlt
  exact lt_irrefl _ hlt

/-- **Equality case.**  If every ratio `P a / m a` is at least `1 / ∑ m`, then `P = m / ∑ m`: the
instance that attains the Rényi value is the one whose Gibbs law is the normalised power mean. -/
theorem eq_of_forall_ratio_ge (P m : ι → ℝ) (hP : ∑ a, P a = 1) (hm : ∀ a, 0 < m a)
    (h : ∀ a, 1 / ∑ b, m b ≤ P a / m a) (a : ι) : P a = m a / ∑ b, m b := by
  have hs : 0 < ∑ a, m a := sum_pos (fun a _ => hm a) ⟨a, mem_univ a⟩
  have hge : ∀ b, m b / ∑ c, m c ≤ P b := by
    intro b
    have h1 := h b
    rw [le_div_iff₀ (hm b)] at h1
    calc m b / ∑ c, m c = (1 / ∑ c, m c) * m b := by ring
      _ ≤ P b := h1
  have hsum : ∑ b, (P b - m b / ∑ c, m c) = 0 := by
    rw [sum_sub_distrib, ← sum_div, div_self hs.ne', hP, sub_self]
  have hzero := (sum_eq_zero_iff_of_nonneg (fun b _ => sub_nonneg.mpr (hge b))).mp hsum a (mem_univ a)
  linarith

omit [Fintype ι] in
/-- **The class is closed under soft minima.**  If every `φ i` satisfies `φ i a - φ i b ≤ d a b`,
then so does `γ a = -(1/t) · log ∑ i, M i · exp (-t · φ i a)` for nonnegative weights of positive
total mass and `t > 0`.  (With `M` an optimal mixture of vertices this `γ`, up to a constant, is the
hardest additive instance at slope `t`.) -/
theorem softmin_admissible {κ : Type*} [Fintype κ] (d : ι → ι → ℝ) (φ : κ → ι → ℝ) (M : κ → ℝ)
    (t : ℝ) (ht : 0 < t) (hM : ∀ i, 0 ≤ M i) (hM1 : 0 < ∑ i, M i)
    (hφ : ∀ i a b, φ i a - φ i b ≤ d a b) (a b : ι) :
    -(1 / t) * Real.log (∑ i, M i * Real.exp (-t * φ i a))
      - -(1 / t) * Real.log (∑ i, M i * Real.exp (-t * φ i b)) ≤ d a b := by
  set Sa := ∑ i, M i * Real.exp (-t * φ i a) with hSa
  set Sb := ∑ i, M i * Real.exp (-t * φ i b) with hSb
  have hpos : ∀ c : ι, 0 < ∑ i, M i * Real.exp (-t * φ i c) := by
    intro c
    obtain ⟨i, -, hi⟩ : ∃ i ∈ (univ : Finset κ), 0 < M i := by
      by_contra hcon
      simp only [not_exists, not_and, not_lt] at hcon
      have : ∑ i, M i ≤ 0 := sum_nonpos fun i hi => hcon i hi
      linarith
    exact sum_pos' (fun j _ => mul_nonneg (hM j) (Real.exp_pos _).le)
      ⟨i, mem_univ i, mul_pos hi (Real.exp_pos _)⟩
  have hle : Sb ≤ Real.exp (t * d a b) * Sa := by
    rw [hSa, hSb, mul_sum]
    refine sum_le_sum fun i _ => ?_
    have h1 : -t * φ i b ≤ t * d a b + -t * φ i a := by nlinarith [hφ i a b]
    calc M i * Real.exp (-t * φ i b) ≤ M i * Real.exp (t * d a b + -t * φ i a) :=
          mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr h1) (hM i)
      _ = Real.exp (t * d a b) * (M i * Real.exp (-t * φ i a)) := by rw [Real.exp_add]; ring
  have hlog : Real.log Sb ≤ t * d a b + Real.log Sa := by
    calc Real.log Sb ≤ Real.log (Real.exp (t * d a b) * Sa) := Real.log_le_log (hpos b) hle
      _ = t * d a b + Real.log Sa := by
          rw [Real.log_mul (Real.exp_pos _).ne' (hpos a).ne', Real.log_exp]
  have key : -(1 / t) * Real.log Sa - -(1 / t) * Real.log Sb = (Real.log Sb - Real.log Sa) / t := by
    field_simp
    ring
  rw [key, div_le_iff₀ ht]
  linarith

end MetricChain.RenyiCentre

-- appended by the referee (R5): print the axioms of the four theorems
#print axioms MetricChain.RenyiCentre.scale_le_inv_sum
#print axioms MetricChain.RenyiCentre.exists_ratio_le
#print axioms MetricChain.RenyiCentre.eq_of_forall_ratio_ge
#print axioms MetricChain.RenyiCentre.softmin_admissible
