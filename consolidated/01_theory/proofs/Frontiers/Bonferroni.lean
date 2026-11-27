import Mathlib

/-!
# The second Bonferroni inequality for a product of numbers in `[0, 1]`

For numbers `c i ∈ [0, 1]` indexed by a finite set `s`,

`1 - ∑ c i  ≤  ∏ (1 - c i)  ≤  1 - ∑ c i + ∑_{pairs} c i * c j`,

where the sum over unordered pairs is written without an order on the index type as
`((∑ c i)² - ∑ (c i)²) / 2` (`pairSum`), and also as half the sum over the off-diagonal ordered
pairs (`pairSum_eq_offDiag`).

The upper bound is inequality (c) of Proposition A17.23 of the Scientific Discovery Division
(message SCI-RES-0035 §2, 2026-11-26): with `c h = 1 - exp (-β S⁻_h)` it turns the exact identity
`Z(m₋ + s₋) = Z(m₋) ⟨∏_h (1 - c h)⟩_floor` into an upper end for `Z(E)` that needs the laws of single
held sites and of pairs of held sites under the floor only.  The statement and the induction
("multiplying by `1 - c n` loses `c n` times the pair sum, which is nonnegative") are that
division's; this file is their machine check, written by the coordinator of the Theoretical
Research Division.  The lower bound is the first Bonferroni (Weierstrass) inequality, included
for the sandwich.

## Results

* `sum_sq_le_sq_sum` — for nonnegative numbers, `∑ (c i)² ≤ (∑ c i)²`; hence `pairSum_nonneg`.
* `prod_one_sub_le` — the second Bonferroni inequality.
* `one_sub_sum_le_prod` — the first.
* `prod_one_sub_mem` — both, as a sandwich.
* `pairSum_eq_offDiag` — the pair sum as half the sum of `c i * c j` over the ordered pairs `i ≠ j`.
* `prod_one_sub_le_witness` — the hypotheses can be met (two numbers `1/2`, `1/3`).
-/

namespace MetricChain.Bonferroni

open Finset

variable {ι : Type*} [DecidableEq ι]

/-- The sum of `c i * c j` over the unordered pairs `{i, j}`, `i ≠ j`, of `s`. -/
noncomputable def pairSum (s : Finset ι) (c : ι → ℝ) : ℝ :=
  ((∑ i ∈ s, c i) ^ 2 - ∑ i ∈ s, c i ^ 2) / 2

/-- For nonnegative numbers the sum of the squares is at most the square of the sum. -/
theorem sum_sq_le_sq_sum (s : Finset ι) (c : ι → ℝ) (h0 : ∀ i ∈ s, 0 ≤ c i) :
    ∑ i ∈ s, c i ^ 2 ≤ (∑ i ∈ s, c i) ^ 2 := by
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih =>
    rw [Finset.sum_insert ha, Finset.sum_insert ha]
    have hca : 0 ≤ c a := h0 a (Finset.mem_insert_self a s)
    have hs : ∀ i ∈ s, 0 ≤ c i := fun i hi => h0 i (Finset.mem_insert_of_mem hi)
    have hS : 0 ≤ ∑ i ∈ s, c i := Finset.sum_nonneg hs
    have := ih hs
    nlinarith [mul_nonneg hca hS]

/-- The pair sum of nonnegative numbers is nonnegative. -/
theorem pairSum_nonneg (s : Finset ι) (c : ι → ℝ) (h0 : ∀ i ∈ s, 0 ≤ c i) :
    0 ≤ pairSum s c := by
  unfold pairSum
  have := sum_sq_le_sq_sum s c h0
  linarith

/-- Adding an index: the pair sum grows by `c a` times the old sum. -/
theorem pairSum_insert {a : ι} {s : Finset ι} (ha : a ∉ s) (c : ι → ℝ) :
    pairSum (insert a s) c = pairSum s c + c a * ∑ i ∈ s, c i := by
  unfold pairSum
  rw [Finset.sum_insert ha, Finset.sum_insert ha]
  ring

/-- **The second Bonferroni inequality** for numbers in `[0, 1]`:
`∏ (1 - c i) ≤ 1 - ∑ c i + ∑_{pairs} c i * c j`. -/
theorem prod_one_sub_le (s : Finset ι) (c : ι → ℝ) (h0 : ∀ i ∈ s, 0 ≤ c i)
    (h1 : ∀ i ∈ s, c i ≤ 1) :
    ∏ i ∈ s, (1 - c i) ≤ 1 - ∑ i ∈ s, c i + pairSum s c := by
  induction s using Finset.induction_on with
  | empty => simp [pairSum]
  | insert a s ha ih =>
    rw [Finset.prod_insert ha, Finset.sum_insert ha, pairSum_insert ha]
    have hca : 0 ≤ c a := h0 a (Finset.mem_insert_self a s)
    have hca1 : c a ≤ 1 := h1 a (Finset.mem_insert_self a s)
    have hs0 : ∀ i ∈ s, 0 ≤ c i := fun i hi => h0 i (Finset.mem_insert_of_mem hi)
    have hs1 : ∀ i ∈ s, c i ≤ 1 := fun i hi => h1 i (Finset.mem_insert_of_mem hi)
    have hP := ih hs0 hs1
    have hpair : 0 ≤ pairSum s c := pairSum_nonneg s c hs0
    have h1a : 0 ≤ 1 - c a := by linarith
    have step : (1 - c a) * ∏ i ∈ s, (1 - c i)
        ≤ (1 - c a) * (1 - ∑ i ∈ s, c i + pairSum s c) :=
      mul_le_mul_of_nonneg_left hP h1a
    nlinarith [mul_nonneg hca hpair]

/-- **The first Bonferroni (Weierstrass) inequality** for numbers in `[0, 1]`:
`1 - ∑ c i ≤ ∏ (1 - c i)`. -/
theorem one_sub_sum_le_prod (s : Finset ι) (c : ι → ℝ) (h0 : ∀ i ∈ s, 0 ≤ c i)
    (h1 : ∀ i ∈ s, c i ≤ 1) :
    1 - ∑ i ∈ s, c i ≤ ∏ i ∈ s, (1 - c i) := by
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih =>
    rw [Finset.prod_insert ha, Finset.sum_insert ha]
    have hca : 0 ≤ c a := h0 a (Finset.mem_insert_self a s)
    have hca1 : c a ≤ 1 := h1 a (Finset.mem_insert_self a s)
    have hs0 : ∀ i ∈ s, 0 ≤ c i := fun i hi => h0 i (Finset.mem_insert_of_mem hi)
    have hs1 : ∀ i ∈ s, c i ≤ 1 := fun i hi => h1 i (Finset.mem_insert_of_mem hi)
    have hP := ih hs0 hs1
    have hS : 0 ≤ ∑ i ∈ s, c i := Finset.sum_nonneg hs0
    have h1a : 0 ≤ 1 - c a := by linarith
    have step : (1 - c a) * (1 - ∑ i ∈ s, c i) ≤ (1 - c a) * ∏ i ∈ s, (1 - c i) :=
      mul_le_mul_of_nonneg_left hP h1a
    nlinarith [mul_nonneg hca hS]

/-- The sandwich: the product of the `1 - c i` lies between the first and the second
Bonferroni sum. -/
theorem prod_one_sub_mem (s : Finset ι) (c : ι → ℝ) (h0 : ∀ i ∈ s, 0 ≤ c i)
    (h1 : ∀ i ∈ s, c i ≤ 1) :
    1 - ∑ i ∈ s, c i ≤ ∏ i ∈ s, (1 - c i) ∧
      ∏ i ∈ s, (1 - c i) ≤ 1 - ∑ i ∈ s, c i + pairSum s c :=
  ⟨one_sub_sum_le_prod s c h0 h1, prod_one_sub_le s c h0 h1⟩

/-- The pair sum is half the sum of `c i * c j` over the ordered pairs `i ≠ j` of `s`. -/
theorem pairSum_eq_offDiag (s : Finset ι) (c : ι → ℝ) :
    pairSum s c = (∑ p ∈ s.offDiag, c p.1 * c p.2) / 2 := by
  unfold pairSum
  have h : (∑ i ∈ s, c i) ^ 2 = ∑ p ∈ s ×ˢ s, c p.1 * c p.2 := by
    rw [sq, Finset.sum_mul_sum, Finset.sum_product]
  have hd : ∑ i ∈ s, c i ^ 2 = ∑ p ∈ s.diag, c p.1 * c p.2 := by
    rw [Finset.sum_diag]
    exact Finset.sum_congr rfl fun i _ => by ring
  have hsplit : ∑ p ∈ s ×ˢ s, c p.1 * c p.2
      = ∑ p ∈ s.diag, c p.1 * c p.2 + ∑ p ∈ s.offDiag, c p.1 * c p.2 := by
    rw [← Finset.sum_union (Finset.disjoint_diag_offDiag s), Finset.diag_union_offDiag]
  rw [h, hd, hsplit]
  ring

/-- Non-vacuity: for `c = (1/2, 1/3)` the product is `1/3`, the first Bonferroni sum `1/6`, the
second `1/3` (with two numbers the second inequality is an equality). -/
theorem prod_one_sub_le_witness : ∏ i ∈ (Finset.univ : Finset (Fin 2)), (1 - ![(1 / 2 : ℝ), 1 / 3] i)
    ≤ 1 - ∑ i ∈ (Finset.univ : Finset (Fin 2)), ![(1 / 2 : ℝ), 1 / 3] i
      + pairSum (Finset.univ : Finset (Fin 2)) ![(1 / 2 : ℝ), 1 / 3] := by
  apply prod_one_sub_le
  · intro i _; fin_cases i <;> norm_num
  · intro i _; fin_cases i <;> norm_num

end MetricChain.Bonferroni
