import Mathlib

/-!
# Two blocks with a coupling: the two exact reductions behind Theorem 11.116(a), (b)

Theory report §11.32 treats a known part with nearest-neighbour interactions along the chain by cutting the chain
into blocks.  Both reductions are algebra on a product of two blocks; this file machine-checks that algebra in its
abstract two-block form (the chain statement iterates it over the cuts, on paper).

* `cut_coupling_admissible`, `cut_coupling_partition`, `cut_coupling_normalised` — **upper reduction (U).**  A coupling
  `J` between two blocks can be moved from the known part into the residual: if `ψ` is admissible for the envelopes
  `d₁ + d₂`, then `ψ + J` is admissible for the envelopes enlarged by the slacks
  `δm(x₁, y₁) ≥ max_{x₂} [J(x₁, x₂) - J(y₁, x₂)]` and `δp(x₂, y₂) ≥ max_{x₁} [J(x₁, x₂) - J(x₁, y₂)]`, and the
  partition sum of the coupled model with residual `ψ` is that of the product model with residual `ψ + J`.
* `gap_embedding_admissible`, `gap_embedding_partition` — **exact embedding (L′).**  If the law on two blocks is the
  product of the block marginals times a positive correction `ρ`, then for every `ψ'` admissible for the envelopes
  reduced by the slacks of `log ρ`, the function `ψ' + log ρ` is admissible for the full envelopes and its partition
  sum under the corrected law is that of `ψ'` under the product — with no loss of accuracy.
* `cut_coupling_witness` — non-vacuity: for two binary blocks coupled by the indicator of disagreement the slack
  "one if the state changes" satisfies the hypothesis, and without a slack the conclusion fails (the coupling itself,
  the image of the zero residual, changes by one).
-/

namespace MetricChain

open Finset

section BlockReductions

variable {X₁ X₂ : Type*}

/-- **Upper reduction, class membership (theory report Theorem 11.116(a)).**  Two blocks `X₁`, `X₂` with envelopes
`d₁`, `d₂`, coupled by any function `J`.  If `ψ` is admissible for `d₁ + d₂`, then `ψ + J` is admissible for the
envelopes enlarged by any slacks `δm ≥ max_{x₂}[J(x₁, x₂) - J(y₁, x₂)]` on the first block and
`δp ≥ max_{x₁}[J(x₁, x₂) - J(x₁, y₂)]` on the second. -/
theorem cut_coupling_admissible {d₁ : X₁ → X₁ → ℝ} {d₂ : X₂ → X₂ → ℝ} (J : X₁ → X₂ → ℝ)
    {δm : X₁ → X₁ → ℝ} {δp : X₂ → X₂ → ℝ}
    (hm : ∀ x₁ y₁ x₂, J x₁ x₂ - J y₁ x₂ ≤ δm x₁ y₁)
    (hp : ∀ y₁ x₂ y₂, J y₁ x₂ - J y₁ y₂ ≤ δp x₂ y₂)
    {ψ : X₁ × X₂ → ℝ} (hψ : ∀ x y, ψ x - ψ y ≤ d₁ x.1 y.1 + d₂ x.2 y.2) (x y : X₁ × X₂) :
    (ψ x + J x.1 x.2) - (ψ y + J y.1 y.2) ≤
      (d₁ x.1 y.1 + δm x.1 y.1) + (d₂ x.2 y.2 + δp x.2 y.2) := by
  have h1 := hψ x y
  have h2 := hm x.1 y.1 x.2
  have h3 := hp y.1 x.2 y.2
  linarith

variable [Fintype X₁] [Fintype X₂]

/-- **Upper reduction, the partition sum.**  With block weights `a`, `b` and the coupling `J`, the weights of the
coupled model times `e^{-ψ}` are the product weights times `e^{-(ψ + J)}`: the coupling has moved into the
residual. -/
theorem cut_coupling_partition (a : X₁ → ℝ) (b : X₂ → ℝ) (J : X₁ → X₂ → ℝ) (ψ : X₁ × X₂ → ℝ) :
    ∑ x : X₁ × X₂, a x.1 * b x.2 * Real.exp (-J x.1 x.2) * Real.exp (-ψ x) =
      ∑ x : X₁ × X₂, a x.1 * b x.2 * Real.exp (-(ψ x + J x.1 x.2)) := by
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [mul_assoc, ← Real.exp_add]
  congr 2
  ring

/-- **Upper reduction, normalised**: `A_π(ψ) = A_ρ(ψ + J) / A_ρ(J)` for `π ∝ ρ e^{-J}`, `ρ ∝ a ⊗ b`. -/
theorem cut_coupling_normalised (a : X₁ → ℝ) (b : X₂ → ℝ) (J : X₁ → X₂ → ℝ) (ψ : X₁ × X₂ → ℝ)
    (hW : ∑ x : X₁ × X₂, a x.1 * b x.2 ≠ 0) :
    (∑ x : X₁ × X₂, a x.1 * b x.2 * Real.exp (-J x.1 x.2) * Real.exp (-ψ x)) /
        (∑ x : X₁ × X₂, a x.1 * b x.2 * Real.exp (-J x.1 x.2)) =
      ((∑ x : X₁ × X₂, a x.1 * b x.2 * Real.exp (-(ψ x + J x.1 x.2))) / ∑ x : X₁ × X₂, a x.1 * b x.2) /
        ((∑ x : X₁ × X₂, a x.1 * b x.2 * Real.exp (-J x.1 x.2)) / ∑ x : X₁ × X₂, a x.1 * b x.2) := by
  rw [cut_coupling_partition, div_div_div_cancel_right₀ hW]

omit [Fintype X₁] [Fintype X₂] in
/-- **Exact embedding, class membership (theory report Theorem 11.116(b)).**  Let the law on two blocks be the
product of the block marginals times a positive correction `ρ`.  If `ψ'` is admissible for the envelopes reduced
by slacks `εm ≥ max_{x₂}[log ρ(x₁, x₂) - log ρ(y₁, x₂)]` and `εp ≥ max_{x₁}[log ρ(x₁, x₂) - log ρ(x₁, y₂)]`, then
`ψ' + log ρ` is admissible for the full envelopes. -/
theorem gap_embedding_admissible {d₁ : X₁ → X₁ → ℝ} {d₂ : X₂ → X₂ → ℝ} (ρ : X₁ → X₂ → ℝ)
    {εm : X₁ → X₁ → ℝ} {εp : X₂ → X₂ → ℝ}
    (hm : ∀ x₁ y₁ x₂, Real.log (ρ x₁ x₂) - Real.log (ρ y₁ x₂) ≤ εm x₁ y₁)
    (hp : ∀ y₁ x₂ y₂, Real.log (ρ y₁ x₂) - Real.log (ρ y₁ y₂) ≤ εp x₂ y₂)
    {ψ' : X₁ × X₂ → ℝ}
    (hψ : ∀ x y, ψ' x - ψ' y ≤ (d₁ x.1 y.1 - εm x.1 y.1) + (d₂ x.2 y.2 - εp x.2 y.2)) (x y : X₁ × X₂) :
    (ψ' x + Real.log (ρ x.1 x.2)) - (ψ' y + Real.log (ρ y.1 y.2)) ≤ d₁ x.1 y.1 + d₂ x.2 y.2 := by
  have h1 := hψ x y
  have h2 := hm x.1 y.1 x.2
  have h3 := hp y.1 x.2 y.2
  linarith

/-- **Exact embedding, the partition sum**: `A_π(ψ' + log ρ) = A_{π₁ ⊗ π₂}(ψ')`, with no loss of accuracy. -/
theorem gap_embedding_partition (a : X₁ → ℝ) (b : X₂ → ℝ) (ρ : X₁ → X₂ → ℝ) (hρ : ∀ x₁ x₂, 0 < ρ x₁ x₂)
    (ψ' : X₁ × X₂ → ℝ) :
    ∑ x : X₁ × X₂, a x.1 * b x.2 * ρ x.1 x.2 * Real.exp (-(ψ' x + Real.log (ρ x.1 x.2))) =
      ∑ x : X₁ × X₂, a x.1 * b x.2 * Real.exp (-ψ' x) := by
  refine Finset.sum_congr rfl fun x _ => ?_
  have h : Real.exp (-(ψ' x + Real.log (ρ x.1 x.2))) = Real.exp (-ψ' x) * (ρ x.1 x.2)⁻¹ := by
    rw [neg_add, Real.exp_add, Real.exp_neg (Real.log _), Real.exp_log (hρ x.1 x.2)]
  rw [h]
  have hne := (hρ x.1 x.2).ne'
  field_simp

/-- **Non-vacuity.**  Two binary blocks coupled by `J(x₁, x₂) = [x₁ ≠ x₂]`: the slack `[x₁ ≠ y₁]` satisfies the
hypothesis of `cut_coupling_admissible`, and with no slack the conclusion fails for the zero residual. -/
theorem cut_coupling_witness :
    (∀ x₁ y₁ x₂ : Bool, (if x₁ = x₂ then (0 : ℝ) else 1) - (if y₁ = x₂ then 0 else 1) ≤
        (if x₁ = y₁ then 0 else 1)) ∧
      ¬ ∀ x y : Bool × Bool, ((0 : ℝ) + (if x.1 = x.2 then 0 else 1)) -
          (0 + (if y.1 = y.2 then 0 else 1)) ≤ 0 := by
  constructor
  · intro x₁ y₁ x₂
    cases x₁ <;> cases y₁ <;> cases x₂ <;> norm_num
  · intro h
    have h1 := h (true, false) (true, true)
    norm_num at h1

end BlockReductions

end MetricChain
