/-
Science division, addendum A17 (17): the greedy vertex of the core minimises a linear cost.

Setting (see `docs/science/INFERENCE_LIMITS_ADDENDA.md`, A17 (17)).  Sites are numbered `0, …, n - 1` in the order in
which they are charged ("most frozen first").  `G j` stands for `Γ(R_j)`, the sum of the certified constants of the
subsets of `R_j = {j, …, n - 1}` (so `G n = 0`).  A vector of site penalties `γ` covers the envelope on the sets
`R_j` iff `G j ≤ ∑_{i ≥ j} γ i`.  The first-order cost of a penalty vector is `∑ p i * γ i`, `p i` the probability that
site `i` is off its anchor; "most frozen first" means that `p` is nondecreasing along the numbering, which is written
here as `p i = ∑_{j ≤ i} δ j` with increments `δ j ≥ 0`.

* `sum_mul_eq_sum_increments` — Abel summation: `∑ p i * γ i = ∑ δ j * ∑_{i ≥ j} γ i`.
* `greedy_cost_le` — every covering vector costs at least `∑ δ j * G j`.
* `marginal_tight` — the marginal vector `γ j = G j - G (j + 1)` covers every `R_j` with equality.
* `greedy_cost_eq`, `greedy_optimal` — so it attains the bound: among all covering vectors the marginal vector of
  the ordering by nondecreasing `p` has the least first-order cost.  (Edmonds' greedy rule on the base polytope of a
  supermodular function, in the one-line form that needs the covering property on the nested sets only; the theory
  division's Proposition 11.18f(c) is this statement for site penalties.)

Mathlib only; no project import.

**Provenance.**  Written and machine-checked by the Scientific Discovery Division (branch
`research/scientific-translation`, `experiments/science/pi_inference/lean/CoreGreedy.lean`, message SCI-RES-0017,
§3 (iii)) and adopted here with statements and proofs unchanged; only this paragraph was added and the `#print`
lines at the end were removed (the axiom check is in `proofs/AxiomAudit.lean`).  Theory report Proposition
11.18f(c′).
-/
import Mathlib

namespace ScienceA17

open Finset

/-- Abel summation: with `p i = ∑ j ∈ range (i + 1), δ j`,
`∑ i < n, p i * γ i = ∑ j < n, δ j * ∑ i ∈ Ico j n, γ i`. -/
theorem sum_mul_eq_sum_increments (n : ℕ) (δ γ : ℕ → ℝ) :
    ∑ i ∈ range n, (∑ j ∈ range (i + 1), δ j) * γ i
      = ∑ j ∈ range n, δ j * ∑ i ∈ Ico j n, γ i := by
  simp_rw [Finset.sum_mul, Finset.mul_sum]
  refine Finset.sum_comm' ?_
  intro i j
  simp only [mem_range, mem_Ico]
  omega

/-- Every vector that covers the nested sets costs at least `∑ δ j * G j`. -/
theorem greedy_cost_le (n : ℕ) (δ γ G : ℕ → ℝ) (hδ : ∀ j < n, 0 ≤ δ j)
    (hcov : ∀ j < n, G j ≤ ∑ i ∈ Ico j n, γ i) :
    ∑ j ∈ range n, δ j * G j ≤ ∑ i ∈ range n, (∑ j ∈ range (i + 1), δ j) * γ i := by
  rw [sum_mul_eq_sum_increments]
  exact Finset.sum_le_sum fun j hj =>
    mul_le_mul_of_nonneg_left (hcov j (mem_range.mp hj)) (hδ j (mem_range.mp hj))

/-- The marginal vector of the numbering, `γ j = G j - G (j + 1)`, covers every nested set with equality. -/
theorem marginal_tight (n : ℕ) (G : ℕ → ℝ) (hGn : G n = 0) :
    ∀ j ≤ n, ∑ i ∈ Ico j n, (G i - G (i + 1)) = G j := by
  intro j hj
  have tel : ∀ k, j ≤ k → ∑ i ∈ Ico j k, (G i - G (i + 1)) = G j - G k := by
    intro k hk
    induction k, hk using Nat.le_induction with
    | base => simp
    | succ k hjk ihk => rw [Finset.sum_Ico_succ_top hjk, ihk]; ring
  rw [tel n hj, hGn]; ring

/-- The marginal vector attains the bound of `greedy_cost_le`. -/
theorem greedy_cost_eq (n : ℕ) (δ G : ℕ → ℝ) (hGn : G n = 0) :
    ∑ i ∈ range n, (∑ j ∈ range (i + 1), δ j) * (G i - G (i + 1)) = ∑ j ∈ range n, δ j * G j := by
  rw [sum_mul_eq_sum_increments]
  refine Finset.sum_congr rfl fun j hj => ?_
  rw [marginal_tight n G hGn j (le_of_lt (mem_range.mp hj))]

/-- **The greedy vertex is optimal at first order.**  Number the sites so that the off-anchor probabilities are
nondecreasing (`p i = ∑ j ≤ i, δ j`, `δ ≥ 0`).  Then the marginal vector `γ⋆ j = G j - G (j + 1)` costs no more than
any vector `γ` that covers the nested sets `R_j`. -/
theorem greedy_optimal (n : ℕ) (δ γ G : ℕ → ℝ) (hδ : ∀ j < n, 0 ≤ δ j) (hGn : G n = 0)
    (hcov : ∀ j < n, G j ≤ ∑ i ∈ Ico j n, γ i) :
    ∑ i ∈ range n, (∑ j ∈ range (i + 1), δ j) * (G i - G (i + 1))
      ≤ ∑ i ∈ range n, (∑ j ∈ range (i + 1), δ j) * γ i := by
  rw [greedy_cost_eq n δ G hGn]
  exact greedy_cost_le n δ γ G hδ hcov

end ScienceA17
