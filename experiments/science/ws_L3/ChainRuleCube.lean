import Mathlib

/-!
# Proposition A1.1, item 2: the chain-rule bound on the biased cube

Science division, workstream L3.  Source: `docs/science/workstreams/A1_REPORT.md` §2.5
(Proposition A1.1).  This file imports **Mathlib only**.

Item 1 of the proposition (conditional laws lie in `[a₀, a₁]`) is `condMarg_mem_window` in
`Compensation.lean` of this directory.  Item 2 is proved here:

    KL(ν_ψ ‖ Bern(r)ⁿ) ≤ n · max{KL(a₀‖r), KL(a₁‖r)}    for every ψ ∈ L_u and every r ∈ (0,1),

with equality at the two cones `u·d_H(·, 0ⁿ)` (value `n·KL(a₀‖r)`) and `u·d_H(·, 1ⁿ)` (value
`n·KL(a₁‖r)`), so that the right side is the greatest value over the class.
Here `a₀ = p₋ = pe^{−u}/(q + pe^{−u})`, `a₁ = p₊ = pe^{u}/(q + pe^{u})`.

**Part 0** repeats, verbatim, the general chain rule of workstream L2
(`experiments/science/ws_L2/Window.lean`: `gibbsLaw`, `klDivFin`, `KLBound`, `kl_gibbs_prod_eq`,
`klBound_prod`, `klBound_pi`, `kl_additive_pi`, … — credited to L2; the files of
`experiments/science/` cannot import each other; the namespace here is `ScienceL3.Chain`).
**Part 1 is new:** the two-letter site bound (`klB_le_max`, `klDivFin_bern`, `klBound_bool`) and
the statements on `Fin n → Bool` (`a1_item2`, `a1_item2_lip`, `a1_item2_cone`,
`a1_item2_isGreatest`).
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL3

namespace Chain

open Finset

/-! ## Part 0: repeated from `experiments/science/ws_L2/Window.lean` (workstream L2) -/

section OneSite

variable {α : Type*} [Fintype α]

/-- The Gibbs law `π_γ ∝ π e^{-γ}`. -/
def gibbsLaw (π γ : α → ℝ) (a : α) : ℝ := π a * Real.exp (-γ a) / ∑ b, π b * Real.exp (-γ b)

/-- `γ` is in the class of the envelope `d`: `γ a - γ b ≤ d a b`. -/
def Admissible (d : α → α → ℝ) (γ : α → ℝ) : Prop := ∀ a b, γ a - γ b ≤ d a b


theorem gibbsZ_pos [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (γ : α → ℝ) :
    0 < ∑ b, π b * Real.exp (-γ b) :=
  Finset.sum_pos (fun b _ => mul_pos (hπ b) (Real.exp_pos _)) Finset.univ_nonempty

theorem gibbsLaw_pos [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (γ : α → ℝ) (a : α) :
    0 < gibbsLaw π γ a :=
  div_pos (mul_pos (hπ a) (Real.exp_pos _)) (gibbsZ_pos hπ γ)

theorem sum_gibbsLaw [Nonempty α] {π : α → ℝ} (hπ : ∀ a, 0 < π a) (γ : α → ℝ) :
    ∑ a, gibbsLaw π γ a = 1 := by
  unfold gibbsLaw
  rw [← Finset.sum_div]
  exact div_self (gibbsZ_pos hπ γ).ne'

end OneSite

section ChainRule

universe u

/-- Relative entropy `∑ p (log p - log q)` of two positive vectors on a finite type. -/
def klDivFin {X : Type*} [Fintype X] (p q : X → ℝ) : ℝ :=
  ∑ x, p x * (Real.log (p x) - Real.log (q x))

/-- `KL(ν_ψ ‖ Q) ≤ M` for every member `ψ` of the class of the envelope `d`. -/
def KLBound {X : Type*} [Fintype X] (π : X → ℝ) (d : X → X → ℝ) (Q : X → ℝ) (M : ℝ) : Prop :=
  ∀ ψ, Admissible d ψ → klDivFin (gibbsLaw π ψ) Q ≤ M

/-- The soft minimum of `ψ` over the first coordinate, with weights `π₁`:
`r ↦ -log ∑_a π₁ a e^{-ψ (a, r)}`. -/
def softMin {α β : Type*} [Fintype α] (π₁ : α → ℝ) (ψ : α × β → ℝ) (r : β) : ℝ :=
  -Real.log (∑ a, π₁ a * Real.exp (-ψ (a, r)))

/-- Adding a constant to the energy does not change the Gibbs law. -/
theorem gibbsLaw_add_const {X : Type*} [Fintype X] (π γ : X → ℝ) (c : ℝ) :
    gibbsLaw π (fun x => γ x + c) = gibbsLaw π γ := by
  funext x
  unfold gibbsLaw
  have h : ∀ y, π y * Real.exp (-(γ y + c)) = π y * Real.exp (-γ y) * Real.exp (-c) := by
    intro y
    rw [neg_add, Real.exp_add]
    ring
  simp only [h]
  rw [← Finset.sum_mul, mul_div_mul_right _ _ (Real.exp_pos (-c)).ne']

section TwoFactors

variable {α β : Type*} [Fintype α] [Fintype β] [Nonempty α] [Nonempty β]

omit [Fintype β] [Nonempty β] in
theorem exp_neg_softMin {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) (ψ : α × β → ℝ) (r : β) :
    Real.exp (-softMin π₁ ψ r) = ∑ a, π₁ a * Real.exp (-ψ (a, r)) := by
  unfold softMin
  rw [neg_neg, Real.exp_log (gibbsZ_pos hπ₁ (fun a => ψ (a, r)))]

omit [Fintype β] [Nonempty β] in
/-- The soft minimum of a function that is `d₂`-Lipschitz in the second coordinate is
`d₂`-Lipschitz (the theory division's `softmin_admissible`). -/
theorem softMin_admissible {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {d₂ : β → β → ℝ}
    {ψ : α × β → ℝ} (hψ : ∀ a r r', ψ (a, r) - ψ (a, r') ≤ d₂ r r') :
    Admissible d₂ (softMin π₁ ψ) := by
  intro r r'
  have hm := gibbsZ_pos hπ₁ (fun a => ψ (a, r))
  have hm' := gibbsZ_pos hπ₁ (fun a => ψ (a, r'))
  have hle : ∑ a, π₁ a * Real.exp (-ψ (a, r')) ≤
      Real.exp (d₂ r r') * ∑ a, π₁ a * Real.exp (-ψ (a, r)) := by
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum (fun a _ => ?_)
    have hexp : Real.exp (-ψ (a, r')) ≤ Real.exp (d₂ r r') * Real.exp (-ψ (a, r)) := by
      rw [← Real.exp_add, Real.exp_le_exp]
      linarith [hψ a r r']
    have := mul_le_mul_of_nonneg_left hexp (hπ₁ a).le
    linarith
  have hlog := Real.log_le_log hm' hle
  rw [Real.log_mul (Real.exp_pos _).ne' hm.ne', Real.log_exp] at hlog
  unfold softMin
  linarith

/-- The Gibbs law on a product factorises: marginal of the second coordinate (the Gibbs law of
the soft minimum) times the conditional law of the first. -/
theorem gibbsLaw_prod_apply {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {π₂ : β → ℝ}
    (hπ₂ : ∀ r, 0 < π₂ r) (ψ : α × β → ℝ) (a : α) (r : β) :
    gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) ψ (a, r) =
      gibbsLaw π₂ (softMin π₁ ψ) r * gibbsLaw π₁ (fun a => ψ (a, r)) a := by
  have hm : 0 < ∑ a, π₁ a * Real.exp (-ψ (a, r)) := gibbsZ_pos hπ₁ (fun a => ψ (a, r))
  have hZ : ∑ z : α × β, π₁ z.1 * π₂ z.2 * Real.exp (-ψ z) =
      ∑ r, π₂ r * Real.exp (-softMin π₁ ψ r) := by
    rw [Fintype.sum_prod_type, Finset.sum_comm]
    refine Finset.sum_congr rfl (fun r _ => ?_)
    rw [exp_neg_softMin hπ₁, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun a _ => ?_)
    ring
  have hZpos : 0 < ∑ r, π₂ r * Real.exp (-softMin π₁ ψ r) := gibbsZ_pos hπ₂ _
  unfold gibbsLaw
  rw [hZ, exp_neg_softMin hπ₁]
  field_simp

/-- **Chain rule** for the relative entropy of a Gibbs law on `α × β` with respect to a product
vector `Q₁ ⊗ Q₂`: the divergence of the `β`-marginal plus the mean divergence of the
conditional laws on `α`. -/
theorem kl_gibbs_prod_eq {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {π₂ : β → ℝ}
    (hπ₂ : ∀ r, 0 < π₂ r) {Q₁ : α → ℝ} (hQ₁ : ∀ a, 0 < Q₁ a) {Q₂ : β → ℝ}
    (hQ₂ : ∀ r, 0 < Q₂ r) (ψ : α × β → ℝ) :
    klDivFin (gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) ψ) (fun z => Q₁ z.1 * Q₂ z.2) =
      klDivFin (gibbsLaw π₂ (softMin π₁ ψ)) Q₂ +
        ∑ r, gibbsLaw π₂ (softMin π₁ ψ) r *
          klDivFin (gibbsLaw π₁ (fun a => ψ (a, r))) Q₁ := by
  unfold klDivFin
  rw [Fintype.sum_prod_type, Finset.sum_comm, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun r _ => ?_)
  have hν : 0 < gibbsLaw π₂ (softMin π₁ ψ) r := gibbsLaw_pos hπ₂ _ r
  have hc : ∀ a, 0 < gibbsLaw π₁ (fun a => ψ (a, r)) a := fun a => gibbsLaw_pos hπ₁ _ a
  have hc1 : ∑ a, gibbsLaw π₁ (fun a => ψ (a, r)) a = 1 := sum_gibbsLaw hπ₁ _
  have hsum : ∑ a, gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) ψ (a, r) *
        (Real.log (gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) ψ (a, r)) -
          Real.log (Q₁ a * Q₂ r)) =
      ∑ a, (gibbsLaw π₁ (fun a => ψ (a, r)) a *
          (gibbsLaw π₂ (softMin π₁ ψ) r *
            (Real.log (gibbsLaw π₂ (softMin π₁ ψ) r) - Real.log (Q₂ r))) +
        gibbsLaw π₂ (softMin π₁ ψ) r *
          (gibbsLaw π₁ (fun a => ψ (a, r)) a *
            (Real.log (gibbsLaw π₁ (fun a => ψ (a, r)) a) - Real.log (Q₁ a)))) := by
    refine Finset.sum_congr rfl (fun a _ => ?_)
    rw [gibbsLaw_prod_apply hπ₁ hπ₂, Real.log_mul hν.ne' (hc a).ne',
      Real.log_mul (hQ₁ a).ne' (hQ₂ r).ne']
    ring
  refine hsum.trans ?_
  rw [Finset.sum_add_distrib, ← Finset.sum_mul, hc1, one_mul, ← Finset.mul_sum]

/-- **Tensorisation of the bound.**  If `KL(ν_γ ‖ Q₁) ≤ M₁` on the class of `d₁` and
`KL(ν_γ ‖ Q₂) ≤ M₂` on the class of `d₂`, then `KL(ν_ψ ‖ Q₁ ⊗ Q₂) ≤ M₁ + M₂` on the class of
`d₁ ⊕ d₂` on the product.  (The envelopes must vanish on the diagonal.) -/
theorem klBound_prod {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {π₂ : β → ℝ} (hπ₂ : ∀ r, 0 < π₂ r)
    {Q₁ : α → ℝ} (hQ₁ : ∀ a, 0 < Q₁ a) {Q₂ : β → ℝ} (hQ₂ : ∀ r, 0 < Q₂ r)
    {d₁ : α → α → ℝ} (hd₁ : ∀ a, d₁ a a ≤ 0) {d₂ : β → β → ℝ} (hd₂ : ∀ r, d₂ r r ≤ 0)
    {M₁ M₂ : ℝ} (h₁ : KLBound π₁ d₁ Q₁ M₁) (h₂ : KLBound π₂ d₂ Q₂ M₂) :
    KLBound (fun z : α × β => π₁ z.1 * π₂ z.2) (fun z z' => d₁ z.1 z'.1 + d₂ z.2 z'.2)
      (fun z => Q₁ z.1 * Q₂ z.2) (M₁ + M₂) := by
  intro ψ hψ
  rw [kl_gibbs_prod_eq hπ₁ hπ₂ hQ₁ hQ₂]
  have hA : Admissible d₂ (softMin π₁ ψ) := by
    refine softMin_admissible hπ₁ (fun a r r' => ?_)
    have := hψ (a, r) (a, r')
    simp only at this
    linarith [hd₁ a]
  have hB : ∀ r, Admissible d₁ (fun a => ψ (a, r)) := by
    intro r a a'
    have := hψ (a, r) (a', r)
    simp only at this
    linarith [hd₂ r]
  have h2 := h₂ _ hA
  have h1 : ∑ r, gibbsLaw π₂ (softMin π₁ ψ) r *
      klDivFin (gibbsLaw π₁ (fun a => ψ (a, r))) Q₁ ≤ M₁ := by
    calc ∑ r, gibbsLaw π₂ (softMin π₁ ψ) r * klDivFin (gibbsLaw π₁ (fun a => ψ (a, r))) Q₁
        ≤ ∑ r, gibbsLaw π₂ (softMin π₁ ψ) r * M₁ :=
          Finset.sum_le_sum (fun r _ =>
            mul_le_mul_of_nonneg_left (h₁ _ (hB r)) (gibbsLaw_pos hπ₂ _ r).le)
      _ = M₁ := by rw [← Finset.sum_mul, sum_gibbsLaw hπ₂, one_mul]
  linarith

/-- **Additivity at additive instances** (two factors):
`KL(ν_{γ₁ ⊕ γ₂} ‖ Q₁ ⊗ Q₂) = KL(ν_{γ₁} ‖ Q₁) + KL(ν_{γ₂} ‖ Q₂)`. -/
theorem kl_gibbs_prod_additive {π₁ : α → ℝ} (hπ₁ : ∀ a, 0 < π₁ a) {π₂ : β → ℝ}
    (hπ₂ : ∀ r, 0 < π₂ r) {Q₁ : α → ℝ} (hQ₁ : ∀ a, 0 < Q₁ a) {Q₂ : β → ℝ}
    (hQ₂ : ∀ r, 0 < Q₂ r) (γ₁ : α → ℝ) (γ₂ : β → ℝ) :
    klDivFin (gibbsLaw (fun z : α × β => π₁ z.1 * π₂ z.2) (fun z => γ₁ z.1 + γ₂ z.2))
        (fun z => Q₁ z.1 * Q₂ z.2) =
      klDivFin (gibbsLaw π₁ γ₁) Q₁ + klDivFin (gibbsLaw π₂ γ₂) Q₂ := by
  rw [kl_gibbs_prod_eq hπ₁ hπ₂ hQ₁ hQ₂]
  have hsoft : softMin π₁ (fun z : α × β => γ₁ z.1 + γ₂ z.2) =
      fun r => γ₂ r + (-Real.log (∑ a, π₁ a * Real.exp (-γ₁ a))) := by
    funext r
    unfold softMin
    have h : ∀ a, π₁ a * Real.exp (-(γ₁ a + γ₂ r)) =
        Real.exp (-γ₂ r) * (π₁ a * Real.exp (-γ₁ a)) := by
      intro a
      rw [neg_add, Real.exp_add]
      ring
    simp only [h]
    rw [← Finset.mul_sum, Real.log_mul (Real.exp_pos _).ne' (gibbsZ_pos hπ₁ γ₁).ne',
      Real.log_exp]
    ring
  have hcond : ∀ r, gibbsLaw π₁ (fun a => γ₁ a + γ₂ r) = gibbsLaw π₁ γ₁ :=
    fun r => gibbsLaw_add_const π₁ γ₁ (γ₂ r)
  rw [hsoft, gibbsLaw_add_const]
  simp only [hcond]
  rw [← Finset.sum_mul, sum_gibbsLaw hπ₂, one_mul]
  ring

end TwoFactors

/-- Transport of a Gibbs law along an equivalence. -/
theorem gibbsLaw_equiv {X Y : Type*} [Fintype X] [Fintype Y] (e : Y ≃ X) (π ψ : X → ℝ)
    (y : Y) : gibbsLaw (fun y => π (e y)) (fun y => ψ (e y)) y = gibbsLaw π ψ (e y) := by
  unfold gibbsLaw
  rw [Equiv.sum_comp e (fun x => π x * Real.exp (-ψ x))]

/-- Transport of the relative entropy of a Gibbs law along an equivalence. -/
theorem klDivFin_gibbs_equiv {X Y : Type*} [Fintype X] [Fintype Y] (e : Y ≃ X)
    (π ψ Q : X → ℝ) :
    klDivFin (gibbsLaw (fun y => π (e y)) (fun y => ψ (e y))) (fun y => Q (e y)) =
      klDivFin (gibbsLaw π ψ) Q := by
  unfold klDivFin
  simp only [gibbsLaw_equiv]
  exact Equiv.sum_comp e (fun x => gibbsLaw π ψ x * (Real.log (gibbsLaw π ψ x) - Real.log (Q x)))

/-- Transport of a bound along an equivalence. -/
theorem klBound_equiv {X Y : Type*} [Fintype X] [Fintype Y] (e : Y ≃ X) {π : X → ℝ}
    {d : X → X → ℝ} {Q : X → ℝ} {M : ℝ} (h : KLBound π d Q M) :
    KLBound (fun y => π (e y)) (fun y y' => d (e y) (e y')) (fun y => Q (e y)) M := by
  intro ψ hψ
  have hadm : Admissible d (fun x => ψ (e.symm x)) := by
    intro x x'
    have := hψ (e.symm x) (e.symm x')
    simpa using this
  have h1 := h _ hadm
  rw [← klDivFin_gibbs_equiv e] at h1
  simpa using h1

/-- **Item 3, the inequality.**  On a product `∀ i : Fin n, S i` of finite alphabets with
positive site weights `π i`, envelopes `d i` vanishing on the diagonal and positive site
vectors `Q i`: if `M i` bounds `KL(π_γ ‖ Q i)` over the site class `L i`, then
`KL(ν_ψ ‖ ⊗ Q i) ≤ ∑_i M i` for every `ψ` in the class of `∑_i d i`. -/
theorem klBound_pi {n : ℕ} : ∀ (S : Fin n → Type u) [∀ i, Fintype (S i)] [∀ i, Nonempty (S i)]
    (π : ∀ i, S i → ℝ) (d : ∀ i, S i → S i → ℝ) (Q : ∀ i, S i → ℝ) (M : Fin n → ℝ),
    (∀ i s, 0 < π i s) → (∀ i s, 0 < Q i s) → (∀ i s, d i s s ≤ 0) →
    (∀ i, KLBound (π i) (d i) (Q i) (M i)) →
    KLBound (fun x : ∀ i, S i => ∏ i, π i (x i)) (fun x y => ∑ i, d i (x i) (y i))
      (fun x => ∏ i, Q i (x i)) (∑ i, M i) := by
  induction n with
  | zero =>
    intro S _ _ π d Q M _ _ _ _ ψ _
    have hsum : ∀ F : (∀ i : Fin 0, S i) → ℝ, ∑ x, F x = F default :=
      fun F => Fintype.sum_unique F
    have hg : gibbsLaw (fun x : ∀ i : Fin 0, S i => ∏ i, π i (x i)) ψ default = 1 := by
      unfold gibbsLaw
      rw [hsum]
      exact div_self (by simp)
    unfold klDivFin
    rw [hsum, hg]
    simp
  | succ n ih =>
    intro S _ _ π d Q M hπ hQ hd h
    have ih' := ih (fun i => S i.succ) (fun i => π i.succ) (fun i => d i.succ)
      (fun i => Q i.succ) (fun i => M i.succ) (fun i s => hπ i.succ s) (fun i s => hQ i.succ s)
      (fun i s => hd i.succ s) (fun i => h i.succ)
    have h2 := klBound_prod (hπ 0)
      (fun r : ∀ i : Fin n, S i.succ => Finset.prod_pos (fun i _ => hπ i.succ (r i)))
      (hQ 0) (fun r : ∀ i : Fin n, S i.succ => Finset.prod_pos (fun i _ => hQ i.succ (r i)))
      (hd 0) (fun r : ∀ i : Fin n, S i.succ => Finset.sum_nonpos (fun i _ => hd i.succ (r i)))
      (h 0) ih'
    have h3 := klBound_equiv (Fin.consEquiv S).symm h2
    have e1 : (fun x : ∀ i, S i => ∏ i, π i (x i)) =
        fun x => π 0 ((Fin.consEquiv S).symm x).1 *
          ∏ i : Fin n, π i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.prod_univ_succ]
      rfl
    have e2 : (fun x y : ∀ i, S i => ∑ i, d i (x i) (y i)) =
        fun x y => d 0 ((Fin.consEquiv S).symm x).1 ((Fin.consEquiv S).symm y).1 +
          ∑ i : Fin n, d i.succ (((Fin.consEquiv S).symm x).2 i)
            (((Fin.consEquiv S).symm y).2 i) := by
      funext x y
      rw [Fin.sum_univ_succ]
      rfl
    have e3 : (fun x : ∀ i, S i => ∏ i, Q i (x i)) =
        fun x => Q 0 ((Fin.consEquiv S).symm x).1 *
          ∏ i : Fin n, Q i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.prod_univ_succ]
      rfl
    rw [e1, e2, e3, Fin.sum_univ_succ]
    exact h3

/-- **Item 3, additive instances.**  For `ψ x = ∑_i γ i (x i)` the Gibbs law is the product of
the site Gibbs laws and `KL(ν_ψ ‖ ⊗ Q i) = ∑_i KL(π_{γ i} ‖ Q i)`. -/
theorem kl_additive_pi {n : ℕ} : ∀ (S : Fin n → Type u) [∀ i, Fintype (S i)]
    [∀ i, Nonempty (S i)] (π : ∀ i, S i → ℝ) (Q : ∀ i, S i → ℝ) (γ : ∀ i, S i → ℝ),
    (∀ i s, 0 < π i s) → (∀ i s, 0 < Q i s) →
    klDivFin (gibbsLaw (fun x : ∀ i, S i => ∏ i, π i (x i)) (fun x => ∑ i, γ i (x i)))
        (fun x => ∏ i, Q i (x i)) =
      ∑ i, klDivFin (gibbsLaw (π i) (γ i)) (Q i) := by
  induction n with
  | zero =>
    intro S _ _ π Q γ _ _
    have hsum : ∀ F : (∀ i : Fin 0, S i) → ℝ, ∑ x, F x = F default :=
      fun F => Fintype.sum_unique F
    have hg : gibbsLaw (fun x : ∀ i : Fin 0, S i => ∏ i, π i (x i))
        (fun x => ∑ i, γ i (x i)) default = 1 := by
      unfold gibbsLaw
      rw [hsum]
      exact div_self (by simp)
    unfold klDivFin
    rw [hsum, hg]
    simp
  | succ n ih =>
    intro S _ _ π Q γ hπ hQ
    have ih' := ih (fun i => S i.succ) (fun i => π i.succ) (fun i => Q i.succ)
      (fun i => γ i.succ) (fun i s => hπ i.succ s) (fun i s => hQ i.succ s)
    have h2 := kl_gibbs_prod_additive (hπ 0)
      (π₂ := fun r : ∀ i : Fin n, S i.succ => ∏ i, π i.succ (r i))
      (fun r => Finset.prod_pos (fun i _ => hπ i.succ (r i)))
      (hQ 0) (Q₂ := fun r : ∀ i : Fin n, S i.succ => ∏ i, Q i.succ (r i))
      (fun r => Finset.prod_pos (fun i _ => hQ i.succ (r i)))
      (γ 0) (fun r : ∀ i : Fin n, S i.succ => ∑ i, γ i.succ (r i))
    have h3 := klDivFin_gibbs_equiv (Fin.consEquiv S).symm
      (fun z : S 0 × (∀ i : Fin n, S i.succ) => π 0 z.1 * ∏ i, π i.succ (z.2 i))
      (fun z => γ 0 z.1 + ∑ i, γ i.succ (z.2 i))
      (fun z => Q 0 z.1 * ∏ i, Q i.succ (z.2 i))
    have e1 : (fun x : ∀ i, S i => ∏ i, π i (x i)) =
        fun x => π 0 ((Fin.consEquiv S).symm x).1 *
          ∏ i : Fin n, π i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.prod_univ_succ]
      rfl
    have e2 : (fun x : ∀ i, S i => ∑ i, γ i (x i)) =
        fun x => γ 0 ((Fin.consEquiv S).symm x).1 +
          ∑ i : Fin n, γ i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.sum_univ_succ]
      rfl
    have e3 : (fun x : ∀ i, S i => ∏ i, Q i (x i)) =
        fun x => Q 0 ((Fin.consEquiv S).symm x).1 *
          ∏ i : Fin n, Q i.succ (((Fin.consEquiv S).symm x).2 i) := by
      funext x
      rw [Fin.prod_univ_succ]
      rfl
    rw [e1, e2, e3, h3, h2, ih', Fin.sum_univ_succ]

/-- **Item 3, as a maximum.**  If, for every site, `M i` is the greatest value of
`KL(π_γ ‖ Q i)` over the site class `L i`, then `∑_i M i` is the greatest value of
`KL(ν_ψ ‖ ⊗ Q i)` over the class `𝒞` of the product, and it is attained at an additive
instance. -/
theorem kl_pi_isGreatest {n : ℕ} (S : Fin n → Type u) [∀ i, Fintype (S i)]
    [∀ i, Nonempty (S i)] (π : ∀ i, S i → ℝ) (d : ∀ i, S i → S i → ℝ) (Q : ∀ i, S i → ℝ)
    (M : Fin n → ℝ) (hπ : ∀ i s, 0 < π i s) (hQ : ∀ i s, 0 < Q i s) (hd : ∀ i s, d i s s ≤ 0)
    (hM : ∀ i, IsGreatest
      {m | ∃ γ, Admissible (d i) γ ∧ klDivFin (gibbsLaw (π i) γ) (Q i) = m} (M i)) :
    IsGreatest {m | ∃ ψ, Admissible (fun x y : ∀ i, S i => ∑ i, d i (x i) (y i)) ψ ∧
        klDivFin (gibbsLaw (fun x : ∀ i, S i => ∏ i, π i (x i)) ψ) (fun x => ∏ i, Q i (x i)) = m}
      (∑ i, M i) := by
  constructor
  · choose γ hγ hγM using fun i => (hM i).1
    refine ⟨fun x => ∑ i, γ i (x i), ?_, ?_⟩
    · intro x y
      rw [← Finset.sum_sub_distrib]
      exact Finset.sum_le_sum (fun i _ => hγ i (x i) (y i))
    · rw [kl_additive_pi S π Q γ hπ hQ]
      exact Finset.sum_congr rfl (fun i _ => hγM i)
  · rintro m ⟨ψ, hψ, rfl⟩
    exact klBound_pi S π d Q M hπ hQ hd (fun i γ hγ => (hM i).2 ⟨γ, hγ, rfl⟩) ψ hψ

end ChainRule

/-! ## Part 1 (new): two letters — Proposition A1.1, item 2 -/

section TwoLetters

/-- The site law of the reference weight: `Bernoulli(p)` (as in `Compensation.lean`). -/
def bernW (p : ℝ) : Bool → ℝ
  | true => p
  | false => 1 - p

/-- `q + p e^{−γ}` (as in `Compensation.lean`). -/
def tiltZ (p γ : ℝ) : ℝ := (1 - p) + p * Real.exp (-γ)

/-- `p_γ = p e^{−γ}/(q + p e^{−γ})` (as in `Compensation.lean`); `a₀ = pTilt p u`,
`a₁ = pTilt p (−u)`. -/
def pTilt (p γ : ℝ) : ℝ := p * Real.exp (-γ) / tiltZ p γ

theorem bernW_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (a : Bool) : 0 < bernW p a := by
  cases a
  · show 0 < 1 - p
    linarith
  · exact hp0

theorem tiltZ_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) : 0 < tiltZ p γ :=
  add_pos (by linarith) (mul_pos hp0 (Real.exp_pos _))

theorem pTilt_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) : 0 < pTilt p γ :=
  div_pos (mul_pos hp0 (Real.exp_pos _)) (tiltZ_pos hp0 hp1 γ)

theorem pTilt_lt_one {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) : pTilt p γ < 1 := by
  unfold pTilt
  rw [div_lt_one (tiltZ_pos hp0 hp1 γ)]
  unfold tiltZ
  linarith

theorem pTilt_anti {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {γ γ' : ℝ} (h : γ ≤ γ') :
    pTilt p γ' ≤ pTilt p γ := by
  unfold pTilt
  rw [div_le_div_iff₀ (tiltZ_pos hp0 hp1 γ') (tiltZ_pos hp0 hp1 γ)]
  unfold tiltZ
  have he : Real.exp (-γ') ≤ Real.exp (-γ) := Real.exp_le_exp.mpr (by linarith)
  have h1 : 0 < p * (1 - p) := mul_pos hp0 (by linarith)
  nlinarith [mul_le_mul_of_nonneg_left he h1.le]

/-- The binary relative entropy `KL(Bern(a) ‖ Bern(r))`. -/
def klB (a r : ℝ) : ℝ :=
  a * (Real.log a - Real.log r) + (1 - a) * (Real.log (1 - a) - Real.log (1 - r))

/-- `a ↦ KL(Bern(a) ‖ Bern(r))` is convex on `[0, 1]` (two-point form). -/
theorem klB_convex_comb {x y r s t : ℝ} (hx0 : 0 ≤ x) (hx1 : x ≤ 1) (hy0 : 0 ≤ y)
    (hy1 : y ≤ 1) (hs : 0 ≤ s) (ht : 0 ≤ t) (hst : s + t = 1) :
    klB (s * x + t * y) r ≤ s * klB x r + t * klB y r := by
  have h1 := Real.convexOn_mul_log.2 (Set.mem_Ici.mpr hx0) (Set.mem_Ici.mpr hy0) hs ht hst
  have h2 := Real.convexOn_mul_log.2 (Set.mem_Ici.mpr (sub_nonneg.mpr hx1))
    (Set.mem_Ici.mpr (sub_nonneg.mpr hy1)) hs ht hst
  simp only [smul_eq_mul] at h1 h2
  have e : 1 - (s * x + t * y) = s * (1 - x) + t * (1 - y) := by
    linear_combination -hst
  unfold klB
  rw [e]
  linarith

/-- On an interval `[a₀, a₁] ⊆ [0, 1]` the binary relative entropy is largest at an end. -/
theorem klB_le_max {a₀ a₁ a r : ℝ} (h0 : 0 ≤ a₀) (h1 : a₁ ≤ 1) (ha0 : a₀ ≤ a) (ha1 : a ≤ a₁) :
    klB a r ≤ max (klB a₀ r) (klB a₁ r) := by
  rcases eq_or_lt_of_le (ha0.trans ha1) with heq | hlt
  · have ha : a = a₀ := le_antisymm (by rw [heq]; exact ha1) ha0
    rw [ha]
    exact le_max_left _ _
  · have hd : 0 < a₁ - a₀ := sub_pos.mpr hlt
    have hcomb : (a₁ - a) / (a₁ - a₀) * a₀ + (a - a₀) / (a₁ - a₀) * a₁ = a := by
      field_simp
      ring
    have hs : 0 ≤ (a₁ - a) / (a₁ - a₀) := div_nonneg (by linarith) hd.le
    have ht : 0 ≤ (a - a₀) / (a₁ - a₀) := div_nonneg (by linarith) hd.le
    have hst : (a₁ - a) / (a₁ - a₀) + (a - a₀) / (a₁ - a₀) = 1 := by
      field_simp
      ring
    have h := klB_convex_comb (r := r) h0 (by linarith) (by linarith) h1 hs ht hst
    rw [hcomb] at h
    calc klB a r ≤ (a₁ - a) / (a₁ - a₀) * klB a₀ r + (a - a₀) / (a₁ - a₀) * klB a₁ r := h
      _ ≤ (a₁ - a) / (a₁ - a₀) * max (klB a₀ r) (klB a₁ r) +
            (a - a₀) / (a₁ - a₀) * max (klB a₀ r) (klB a₁ r) :=
          add_le_add (mul_le_mul_of_nonneg_left (le_max_left _ _) hs)
            (mul_le_mul_of_nonneg_left (le_max_right _ _) ht)
      _ = max (klB a₀ r) (klB a₁ r) := by rw [← add_mul, hst, one_mul]

/-- The envelope of one site of the cube: `u·[a ≠ b]`. -/
def flipEnv (u : ℝ) (a b : Bool) : ℝ := if a = b then 0 else u

/-- The Gibbs law of a two-letter site is `Bern(p_γ)` with `γ = γ(1) − γ(0)`. -/
theorem gibbsLaw_bern_true {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : Bool → ℝ) :
    gibbsLaw (bernW p) γ true = pTilt p (γ true - γ false) := by
  have hrel : Real.exp (-(γ true - γ false)) * Real.exp (-γ false) = Real.exp (-γ true) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hden1 : 0 < p * Real.exp (-γ true) + (1 - p) * Real.exp (-γ false) :=
    add_pos (mul_pos hp0 (Real.exp_pos _)) (mul_pos (by linarith) (Real.exp_pos _))
  have hden2 : 0 < (1 - p) + p * Real.exp (-(γ true - γ false)) := tiltZ_pos hp0 hp1 _
  unfold gibbsLaw
  rw [Fintype.sum_bool]
  show p * Real.exp (-γ true) / (p * Real.exp (-γ true) + (1 - p) * Real.exp (-γ false)) =
    p * Real.exp (-(γ true - γ false)) / ((1 - p) + p * Real.exp (-(γ true - γ false)))
  rw [div_eq_div_iff hden1.ne' hden2.ne', ← hrel]
  ring

/-- `KL(π_γ ‖ Bern(r)) = KL(Bern(p_γ) ‖ Bern(r))` on a two-letter site. -/
theorem klDivFin_bern {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (r : ℝ) (γ : Bool → ℝ) :
    klDivFin (gibbsLaw (bernW p) γ) (bernW r) = klB (pTilt p (γ true - γ false)) r := by
  have ht := gibbsLaw_bern_true hp0 hp1 γ
  have hs := sum_gibbsLaw (π := bernW p) (bernW_pos hp0 hp1) γ
  rw [Fintype.sum_bool] at hs
  have hf : gibbsLaw (bernW p) γ false = 1 - pTilt p (γ true - γ false) := by linarith
  unfold klDivFin klB
  rw [Fintype.sum_bool, ht, hf]
  rfl

/-- **The site bound:** over the class of one site of the cube (`|γ(1) − γ(0)| ≤ u`),
`KL(π_γ ‖ Bern(r)) ≤ max{KL(a₀‖r), KL(a₁‖r)}`. -/
theorem klBound_bool {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u r : ℝ) :
    KLBound (bernW p) (flipEnv u) (bernW r)
      (max (klB (pTilt p u) r) (klB (pTilt p (-u)) r)) := by
  intro γ hγ
  rw [klDivFin_bern hp0 hp1]
  have h1 : γ true - γ false ≤ u := hγ true false
  have h2 : γ false - γ true ≤ u := hγ false true
  exact klB_le_max (pTilt_pos hp0 hp1 u).le (pTilt_lt_one hp0 hp1 (-u)).le
    (pTilt_anti hp0 hp1 h1) (pTilt_anti hp0 hp1 (by linarith))

/-- `Σ_i u·[x_i ≠ y_i] = u · d_H(x, y)`. -/
theorem sum_flipEnv {n : ℕ} (u : ℝ) (x y : Fin n → Bool) :
    ∑ i, flipEnv u (x i) (y i) = u * (hammingDist x y : ℝ) := by
  unfold hammingDist flipEnv
  rw [Finset.card_filter]
  push_cast
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  by_cases h : x i = y i <;> simp [h]

/-- **Proposition A1.1, item 2 (the chain-rule bound), envelope form.** -/
theorem a1_item2 {n : ℕ} {p r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr0 : 0 < r) (hr1 : r < 1)
    (u : ℝ) :
    KLBound (fun x : Fin n → Bool => ∏ i, bernW p (x i))
      (fun x y => ∑ i, flipEnv u (x i) (y i)) (fun x => ∏ i, bernW r (x i))
      ((n : ℝ) * max (klB (pTilt p u) r) (klB (pTilt p (-u)) r)) := by
  have h := klBound_pi (fun _ : Fin n => Bool) (fun _ => bernW p) (fun _ => flipEnv u)
    (fun _ => bernW r) (fun _ => max (klB (pTilt p u) r) (klB (pTilt p (-u)) r))
    (fun _ s => bernW_pos hp0 hp1 s) (fun _ s => bernW_pos hr0 hr1 s)
    (fun _ s => le_of_eq (if_pos rfl)) (fun _ => klBound_bool hp0 hp1 u r)
  rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at h
  exact h

/-- **Proposition A1.1, item 2.**  `π = Bern(p)ⁿ`, `ν_ψ ∝ π e^{−ψ}`.  For every `n`, every
`ψ` with `ψ x − ψ y ≤ u·d_H(x, y)` (the class `L_u`) and every `r ∈ (0, 1)`:

    KL(ν_ψ ‖ Bern(r)ⁿ) ≤ n · max{KL(a₀‖r), KL(a₁‖r)},   a₀ = p_u,  a₁ = p_{−u}. -/
theorem a1_item2_lip {n : ℕ} {p r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr0 : 0 < r)
    (hr1 : r < 1) {u : ℝ} (ψ : (Fin n → Bool) → ℝ)
    (hψ : ∀ x y, ψ x - ψ y ≤ u * (hammingDist x y : ℝ)) :
    klDivFin (gibbsLaw (fun x : Fin n → Bool => ∏ i, bernW p (x i)) ψ)
        (fun x => ∏ i, bernW r (x i)) ≤
      (n : ℝ) * max (klB (pTilt p u) r) (klB (pTilt p (-u)) r) :=
  a1_item2 hp0 hp1 hr0 hr1 u ψ fun x y => by
    show ψ x - ψ y ≤ ∑ i, flipEnv u (x i) (y i)
    rw [sum_flipEnv]
    exact hψ x y

/-- **Proposition A1.1, item 2, additive instances:** for `ψ(x) = Σ_i γ(x_i)`,
`KL(ν_ψ ‖ Bern(r)ⁿ) = n · KL(Bern(p_{γ(1)−γ(0)}) ‖ Bern(r))`. -/
theorem a1_item2_additive {n : ℕ} {p r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr0 : 0 < r)
    (hr1 : r < 1) (γ : Bool → ℝ) :
    klDivFin (gibbsLaw (fun x : Fin n → Bool => ∏ i, bernW p (x i)) (fun x => ∑ i, γ (x i)))
        (fun x => ∏ i, bernW r (x i)) =
      (n : ℝ) * klB (pTilt p (γ true - γ false)) r := by
  rw [kl_additive_pi (fun _ : Fin n => Bool) (fun _ => bernW p) (fun _ => bernW r)
    (fun _ => γ) (fun _ s => bernW_pos hp0 hp1 s) (fun _ s => bernW_pos hr0 hr1 s),
    Finset.sum_congr rfl fun i _ => klDivFin_bern hp0 hp1 r γ, Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]

/-- **Equality at the cone around `0ⁿ`:** for `ψ = u·|x| = u·d_H(x, 0ⁿ)`,
`KL(ν_ψ ‖ Bern(r)ⁿ) = n·KL(a₀‖r)`. -/
theorem a1_item2_cone0 {n : ℕ} {p r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr0 : 0 < r)
    (hr1 : r < 1) (u : ℝ) :
    klDivFin (gibbsLaw (fun x : Fin n → Bool => ∏ i, bernW p (x i))
        (fun x => ∑ i, if x i = true then u else 0)) (fun x => ∏ i, bernW r (x i)) =
      (n : ℝ) * klB (pTilt p u) r := by
  have h := a1_item2_additive (n := n) hp0 hp1 hr0 hr1 (fun b : Bool => if b = true then u else 0)
  have e : (if true = true then u else 0) - (if false = true then u else (0 : ℝ)) = u := by simp
  rw [e] at h
  exact h

/-- **Equality at the cone around `1ⁿ`:** for `ψ = u·(n − |x|) = u·d_H(x, 1ⁿ)`,
`KL(ν_ψ ‖ Bern(r)ⁿ) = n·KL(a₁‖r)`. -/
theorem a1_item2_cone1 {n : ℕ} {p r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr0 : 0 < r)
    (hr1 : r < 1) (u : ℝ) :
    klDivFin (gibbsLaw (fun x : Fin n → Bool => ∏ i, bernW p (x i))
        (fun x => ∑ i, if x i = true then 0 else u)) (fun x => ∏ i, bernW r (x i)) =
      (n : ℝ) * klB (pTilt p (-u)) r := by
  have h := a1_item2_additive (n := n) hp0 hp1 hr0 hr1 (fun b : Bool => if b = true then 0 else u)
  have e : (if true = true then (0 : ℝ) else u) - (if false = true then 0 else u) = -u := by simp
  rw [e] at h
  exact h

/-- An additive instance whose site function is in the site class is in the class `L_u`. -/
theorem cone_admissible {n : ℕ} {u : ℝ} (γ : Bool → ℝ)
    (hγ : ∀ a b, γ a - γ b ≤ flipEnv u a b) (x y : Fin n → Bool) :
    (∑ i, γ (x i)) - ∑ i, γ (y i) ≤ u * (hammingDist x y : ℝ) := by
  rw [← sum_flipEnv, ← Finset.sum_sub_distrib]
  exact Finset.sum_le_sum fun i _ => hγ (x i) (y i)

/-- **Proposition A1.1, item 2, as a maximum:** for `u ≥ 0` and `r ∈ (0, 1)`,
`n · max{KL(a₀‖r), KL(a₁‖r)}` is the greatest value of `KL(ν_ψ ‖ Bern(r)ⁿ)` over the class `L_u`;
it is attained at one of the two cones. -/
theorem a1_item2_isGreatest {n : ℕ} {p r u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr0 : 0 < r)
    (hr1 : r < 1) (hu : 0 ≤ u) :
    IsGreatest {m : ℝ | ∃ ψ : (Fin n → Bool) → ℝ,
        (∀ x y, ψ x - ψ y ≤ u * (hammingDist x y : ℝ)) ∧
        klDivFin (gibbsLaw (fun x : Fin n → Bool => ∏ i, bernW p (x i)) ψ)
          (fun x => ∏ i, bernW r (x i)) = m}
      ((n : ℝ) * max (klB (pTilt p u) r) (klB (pTilt p (-u)) r)) := by
  constructor
  · rcases le_total (klB (pTilt p (-u)) r) (klB (pTilt p u) r) with h | h
    · rw [max_eq_left h]
      refine ⟨fun x => ∑ i, if x i = true then u else 0, ?_, a1_item2_cone0 hp0 hp1 hr0 hr1 u⟩
      refine cone_admissible (fun b : Bool => if b = true then u else 0) (fun a b => ?_)
      cases a <;> cases b <;> simp [flipEnv, hu]
    · rw [max_eq_right h]
      refine ⟨fun x => ∑ i, if x i = true then 0 else u, ?_, a1_item2_cone1 hp0 hp1 hr0 hr1 u⟩
      refine cone_admissible (fun b : Bool => if b = true then 0 else u) (fun a b => ?_)
      cases a <;> cases b <;> simp [flipEnv, hu]
  · rintro m ⟨ψ, hψ, rfl⟩
    exact a1_item2_lip hp0 hp1 hr0 hr1 ψ hψ

end TwoLetters

end Chain

end ScienceL3

/-! ## Axioms -/

#print axioms ScienceL3.Chain.klBound_pi
#print axioms ScienceL3.Chain.kl_additive_pi
#print axioms ScienceL3.Chain.klB_le_max
#print axioms ScienceL3.Chain.klDivFin_bern
#print axioms ScienceL3.Chain.klBound_bool
#print axioms ScienceL3.Chain.a1_item2
#print axioms ScienceL3.Chain.a1_item2_lip
#print axioms ScienceL3.Chain.a1_item2_additive
#print axioms ScienceL3.Chain.a1_item2_cone0
#print axioms ScienceL3.Chain.a1_item2_cone1
#print axioms ScienceL3.Chain.a1_item2_isGreatest
