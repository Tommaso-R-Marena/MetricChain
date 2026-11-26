/-
  MetricChain — Ensemble division.  The zero set of the two-state certificate (report §4c.4,
  Proposition E20′).

  Two states `p`, `q` of a product configuration space differ in every coordinate of an index set
  `ι` with at least two elements.  For non-negative functions `a k` ("distance of coordinate `k`
  from `p k`") and `b k` ("distance of coordinate `k` from `q k`") that never vanish together, the
  certificate

      f = ∑_{k ≠ l} a k * b l

  vanishes exactly when all `a k` vanish (the configuration is `p`) or all `b k` vanish (it is
  `q`).  This is the combinatorial content of Proposition E20′; that `a k = 2 - 2 cos(φ_k - p_k)`
  is non-negative and vanishes only at `φ_k = p_k` is the trigonometric part, on paper.
-/
import Mathlib

namespace MetricChain.Ensemble

open Finset

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The two-state certificate `∑_{k ≠ l} a k * b l`. -/
def twoStateCert (a b : ι → ℝ) : ℝ :=
  ∑ k, ∑ l ∈ univ.filter (fun l => l ≠ k), a k * b l

/-- The purely logical core: if for all `k ≠ l` either coordinate `k` sits at `p` or coordinate
`l` sits at `q`, and no coordinate sits at both, then the configuration is `p` or it is `q`. -/
theorem all_left_or_all_right {A B : ι → Prop} (hne : ∀ k, ¬ (A k ∧ B k))
    (htwo : ∀ k : ι, ∃ l, l ≠ k) (h : ∀ k l, l ≠ k → A k ∨ B l) :
    (∀ k, A k) ∨ (∀ k, B k) := by
  by_cases hA : ∀ k, A k
  · exact Or.inl hA
  · right
    push Not at hA
    obtain ⟨k, hk⟩ := hA
    -- every other coordinate sits at `q`
    have hB : ∀ l, l ≠ k → B l := fun l hl => (h k l hl).resolve_left hk
    intro j
    by_cases hj : j = k
    · subst hj
      obtain ⟨l, hl⟩ := htwo j
      have hBl : B l := hB l hl
      have hAl : ¬ A l := fun hAl => hne l ⟨hAl, hBl⟩
      exact (h l j (fun e => hl e.symm)).resolve_left hAl
    · exact hB j hj

/-- **Zero set of the two-state certificate.**  For non-negative `a`, `b` that never vanish
together, on an index set in which every element has another one, the certificate vanishes iff
all `a k` vanish or all `b k` vanish. -/
theorem twoStateCert_eq_zero_iff (a b : ι → ℝ) (ha : ∀ k, 0 ≤ a k) (hb : ∀ k, 0 ≤ b k)
    (hne : ∀ k, ¬ (a k = 0 ∧ b k = 0)) (htwo : ∀ k : ι, ∃ l, l ≠ k) :
    twoStateCert a b = 0 ↔ (∀ k, a k = 0) ∨ (∀ k, b k = 0) := by
  constructor
  · intro h
    have hterm : ∀ k l, l ≠ k → a k * b l = 0 := by
      intro k l hl
      have h1 : ∀ k ∈ (univ : Finset ι), 0 ≤ ∑ l ∈ univ.filter (fun l => l ≠ k), a k * b l :=
        fun k _ => Finset.sum_nonneg (fun l _ => mul_nonneg (ha k) (hb l))
      have h2 := (Finset.sum_eq_zero_iff_of_nonneg h1).mp h k (Finset.mem_univ k)
      have h3 : ∀ l ∈ univ.filter (fun l => l ≠ k), 0 ≤ a k * b l :=
        fun l _ => mul_nonneg (ha k) (hb l)
      exact (Finset.sum_eq_zero_iff_of_nonneg h3).mp h2 l
        (Finset.mem_filter.mpr ⟨Finset.mem_univ l, hl⟩)
    exact all_left_or_all_right (A := fun k => a k = 0) (B := fun k => b k = 0) hne htwo
      (fun k l hl => mul_eq_zero.mp (hterm k l hl))
  · rintro (h | h)
    · simp [twoStateCert, h]
    · simp [twoStateCert, h]

/-- The certificate is non-negative. -/
theorem twoStateCert_nonneg (a b : ι → ℝ) (ha : ∀ k, 0 ≤ a k) (hb : ∀ k, 0 ≤ b k) :
    0 ≤ twoStateCert a b :=
  Finset.sum_nonneg (fun k _ => Finset.sum_nonneg (fun l _ => mul_nonneg (ha k) (hb l)))

/-- With a single coordinate the certificate is identically zero: two states that differ in one
coordinate only are not separated from the rest of that coordinate's fibre (the case `|D| = 1` of
Proposition E20′, in which no two-state ensemble is identified). -/
theorem twoStateCert_unique_eq_zero [Unique ι] (a b : ι → ℝ) : twoStateCert a b = 0 := by
  unfold twoStateCert
  refine Finset.sum_eq_zero (fun k _ => Finset.sum_eq_zero (fun l hl => ?_))
  exact absurd (Subsingleton.elim l k) (Finset.mem_filter.mp hl).2

end MetricChain.Ensemble
