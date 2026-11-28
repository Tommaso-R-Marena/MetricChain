import Mathlib

/-!
# The relaxation lemma: arithmetic core

Phase II (adaptive hierarchy), `docs/phase2_hierarchy/HIERARCHY_REPORT.md` §3 (Lemma B).

A block-radial energy has a profile `F` on types `d = (d_j)`; `t_j` is the cost of a block distance
relative to the typical one.  In the proof of Lemma B a hidden type `y` is compared with an *anchor* `e`
obtained by relaxing the blocks of `y` towards typical distances.  The blocks have one of four roles:
`P` (revealed in the first round, relaxed to the hinted radius), `Q` (revealed in the second round,
relaxed to the hinted radius), `Trel` (never revealed, relaxed to a deeper radius), `Tun` (never revealed,
not moved).  Per block the proof establishes four elementary inequalities about binomial costs (facts
(F1)–(F4), (R) of the report); the value of the profile at the anchor is bounded by the largest mass a
blind batch sees; and the profile is Lipschitz.  This file checks that these inputs give the conclusion —
i.e. the bookkeeping of the proof, with its signs and constants — and nothing more.

Notation: `a j = t_j(e_j)`, `b j = t_j(y_j)`, `s j = u·|e_j − y_j|`, `H j = n_j·h`, `c` the per-block
logarithmic allowance, `Fy = F(y)`, `Fe = F(e)`, `nu0` the blind-visible maximum of `−F − t`.

* `relaxation_core` — the bound `−F(y) − t(y) ≤ ν₀ + cap + Σ_P H + Σ_Trel H − t_T(e) + c·(#blocks moved)`.
* `relaxation_exhausted` — case (ii) of the lemma: if the anchor exhausts the budget of the second round
  (`t_T(e) ≥ Θ − Σ_Q H − slack`) and the blocks carry at most the total weight `Htot`, then
  `−F(y) − t(y) ≤ ν₀ − (Θ − Htot) + (allowances)`: the hidden type is lighter than the blind-visible
  maximum by the excess of the budget over `n·h`.
* `relaxation_unmoved` — case (i): if no block of `T` is moved, `−F(y) − t(y) ≤ ν₀ + Σ_P H − t_T(y) + …`.
* `relax_step` — the per-block inequality (R) from its two ingredients.
* `choose_mul_pow_le`, `choose_step` — the binomial facts (F2) and (F3) in exact form.
-/

namespace MetricChain.RelaxationCore

open Finset

variable {ι : Type*}

/-- The per-block inequality (R): if `γ(e) ≤ Λ + H + c₁` (the anchor radius is at most the hinted one)
and `γ(y) ≥ Λ − c₂` (the bound from the moment generating function), then `γ(e) ≤ γ(y) + H + c₁ + c₂`. -/
theorem relax_step {γe γy Λ H c₁ c₂ : ℝ} (h₁ : γe ≤ Λ + H + c₁) (h₂ : Λ - c₂ ≤ γy) :
    γe ≤ γy + H + c₁ + c₂ := by linarith

/-- Bookkeeping of Lemma B. -/
theorem relaxation_core (P Q Trel Tun : Finset ι) (a b s H : ι → ℝ) (c Fy Fe nu0 cap : ℝ)
    (hP : ∀ j ∈ P, a j - b j + s j ≤ H j + c)
    (hQ : ∀ j ∈ Q, s j - b j ≤ c)
    (hT : ∀ j ∈ Trel, s j - b j ≤ H j + c - a j)
    (hU : ∀ j ∈ Tun, s j = 0 ∧ a j = b j)
    (hcap : -Fe ≤ nu0 + ∑ j ∈ P, a j + cap)
    (hLip : -Fy ≤ -Fe + (∑ j ∈ P, s j + ∑ j ∈ Q, s j + ∑ j ∈ Trel, s j + ∑ j ∈ Tun, s j)) :
    -Fy - (∑ j ∈ P, b j + ∑ j ∈ Q, b j + ∑ j ∈ Trel, b j + ∑ j ∈ Tun, b j)
      ≤ nu0 + cap + ∑ j ∈ P, H j + ∑ j ∈ Trel, H j - (∑ j ∈ Trel, a j + ∑ j ∈ Tun, a j)
        + c * ((P.card : ℝ) + Q.card + Trel.card) := by
  have h1 : ∑ j ∈ P, (a j - b j + s j) ≤ ∑ j ∈ P, (H j + c) := Finset.sum_le_sum hP
  have h2 : ∑ j ∈ Q, (s j - b j) ≤ ∑ j ∈ Q, c := Finset.sum_le_sum hQ
  have h3 : ∑ j ∈ Trel, (s j - b j) ≤ ∑ j ∈ Trel, (H j + c - a j) := Finset.sum_le_sum hT
  have h4 : ∑ j ∈ Tun, s j = 0 := Finset.sum_eq_zero (fun j hj => (hU j hj).1)
  have h5 : ∑ j ∈ Tun, a j = ∑ j ∈ Tun, b j := Finset.sum_congr rfl (fun j hj => (hU j hj).2)
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul] at h1 h2 h3
  linarith

/-- Case (ii) of Lemma B: the anchor exhausts the budget `Θ` of the batch that knows `P`. -/
theorem relaxation_exhausted (P Q Trel Tun : Finset ι) (a b s H : ι → ℝ)
    (c Fy Fe nu0 cap Θ slack Htot : ℝ)
    (hP : ∀ j ∈ P, a j - b j + s j ≤ H j + c)
    (hQ : ∀ j ∈ Q, s j - b j ≤ c)
    (hT : ∀ j ∈ Trel, s j - b j ≤ H j + c - a j)
    (hU : ∀ j ∈ Tun, s j = 0 ∧ a j = b j)
    (hcap : -Fe ≤ nu0 + ∑ j ∈ P, a j + cap)
    (hLip : -Fy ≤ -Fe + (∑ j ∈ P, s j + ∑ j ∈ Q, s j + ∑ j ∈ Trel, s j + ∑ j ∈ Tun, s j))
    (hbudget : Θ - ∑ j ∈ Q, H j - slack ≤ ∑ j ∈ Trel, a j + ∑ j ∈ Tun, a j)
    (hweight : ∑ j ∈ P, H j + ∑ j ∈ Q, H j + ∑ j ∈ Trel, H j ≤ Htot) :
    -Fy - (∑ j ∈ P, b j + ∑ j ∈ Q, b j + ∑ j ∈ Trel, b j + ∑ j ∈ Tun, b j)
      ≤ nu0 - (Θ - Htot) + cap + slack + c * ((P.card : ℝ) + Q.card + Trel.card) := by
  have h := relaxation_core P Q Trel Tun a b s H c Fy Fe nu0 cap hP hQ hT hU hcap hLip
  linarith

/-- Case (i) of Lemma B: no block of `T` is moved (`Trel = ∅`). -/
theorem relaxation_unmoved (P Q Tun : Finset ι) (a b s H : ι → ℝ) (c Fy Fe nu0 cap : ℝ)
    (hP : ∀ j ∈ P, a j - b j + s j ≤ H j + c)
    (hQ : ∀ j ∈ Q, s j - b j ≤ c)
    (hU : ∀ j ∈ Tun, s j = 0 ∧ a j = b j)
    (hcap : -Fe ≤ nu0 + ∑ j ∈ P, a j + cap)
    (hLip : -Fy ≤ -Fe + (∑ j ∈ P, s j + ∑ j ∈ Q, s j + ∑ j ∈ Tun, s j)) :
    -Fy - (∑ j ∈ P, b j + ∑ j ∈ Q, b j + ∑ j ∈ Tun, b j)
      ≤ nu0 + cap + ∑ j ∈ P, H j - ∑ j ∈ Tun, b j + c * ((P.card : ℝ) + Q.card) := by
  have h := relaxation_core P Q (∅ : Finset ι) Tun a b s H c Fy Fe nu0 cap hP hQ
    (by intro j hj; simp at hj) hU hcap (by simpa using hLip)
  have h5 : ∑ j ∈ Tun, a j = ∑ j ∈ Tun, b j := Finset.sum_congr rfl (fun j hj => (hU j hj).2)
  simp at h
  linarith

/-! ### Two of the binomial facts, in exact form

Fact (F2) of the report: `P_j(d) e^{-ud} ≤ ((1 + e^{-u})/2)^{n_j}`, i.e. `t_j(d) + u d ≥ n_j Λ₁ − L`.
Fact (F3): `γ_j(d) ≥ γ_j(d+1)` as long as `(d+1) e^u ≤ n_j − d`, i.e. `P_j(d+1) ≥ e^u P_j(d)`. -/

/-- (F2), exact form: one term of the binomial expansion is at most the whole sum. -/
theorem choose_mul_pow_le (n d : ℕ) (hd : d ≤ n) (x : ℝ) (hx : 0 ≤ x) :
    (n.choose d : ℝ) * x ^ d ≤ (1 + x) ^ n := by
  have h := add_pow x 1 n
  have hterm : ∀ m ∈ Finset.range (n + 1), 0 ≤ x ^ m * 1 ^ (n - m) * (n.choose m : ℝ) := by
    intro m _
    positivity
  have hle := Finset.single_le_sum hterm (Finset.mem_range.mpr (Nat.lt_succ_of_le hd))
  calc (n.choose d : ℝ) * x ^ d = x ^ d * 1 ^ (n - d) * (n.choose d : ℝ) := by ring
    _ ≤ ∑ m ∈ Finset.range (n + 1), x ^ m * 1 ^ (n - m) * (n.choose m : ℝ) := hle
    _ = (x + 1) ^ n := h.symm
    _ = (1 + x) ^ n := by ring

/-- (F3), exact form: if `(d+1)·w ≤ n − d` then `w·C(n,d) ≤ C(n,d+1)`
(with `w = e^u`: moving one step towards the centre gains at least the slope). -/
theorem choose_step (n d : ℕ) (w : ℝ) (hw : ((d : ℝ) + 1) * w ≤ (n : ℝ) - d) (hd : d ≤ n) :
    w * (n.choose d : ℝ) ≤ (n.choose (d + 1) : ℝ) := by
  have key : (n.choose (d + 1) : ℝ) * ((d : ℝ) + 1) = (n.choose d : ℝ) * ((n : ℝ) - d) := by
    have h := Nat.choose_succ_right_eq n d
    have h' : ((n.choose (d + 1) * (d + 1) : ℕ) : ℝ) = ((n.choose d * (n - d) : ℕ) : ℝ) := by
      exact_mod_cast h
    push_cast [Nat.cast_sub hd] at h'
    linarith
  have hpos : (0 : ℝ) < (d : ℝ) + 1 := by positivity
  have hc : (0 : ℝ) ≤ (n.choose d : ℝ) := by positivity
  have h1 : w * (n.choose d : ℝ) * ((d : ℝ) + 1) ≤ (n.choose (d + 1) : ℝ) * ((d : ℝ) + 1) := by
    calc w * (n.choose d : ℝ) * ((d : ℝ) + 1) = (n.choose d : ℝ) * (((d : ℝ) + 1) * w) := by ring
      _ ≤ (n.choose d : ℝ) * ((n : ℝ) - d) := by
          exact mul_le_mul_of_nonneg_left hw hc
      _ = (n.choose (d + 1) : ℝ) * ((d : ℝ) + 1) := key.symm
  exact le_of_mul_le_mul_right h1 hpos

end MetricChain.RelaxationCore
