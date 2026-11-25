import Mathlib

/-!
# Soundness of the identified-set certificates and of the falsification certificate

Science division, workstream L1.  Source statements: `docs/science/INFERENCE_LIMITS.md` §8
("Certified identified sets") and §9, Theorem 8 ("falsification certificates").

Setting: `X` a finite configuration space, `K` a finite index set of features `φ k : X → ℝ`,
data in the form of a box `lo k ≤ E_μ φ_k ≤ hi k`, a target `ψ : X → ℝ`.

## What is proved (all on a finite type, real-valued functions)

* `modelFree_certificate_sound_support` — §8, first bullet, in the note's own form: for every
  `λ`, every upper bound `h` of the support function of the data set `D` at `λ` and every upper
  bound `M` of `max_x (ψ x - λ·Φ x)`: `E_μ ψ ≤ h + M` for every probability vector `μ` with
  `E_μ Φ ∈ D`.  (`D` is an arbitrary set; no convexity or compactness is used for soundness.)
* `modelFree_certificate_sound` — the same for a box, with multipliers `λ⁺, λ⁻ ≥ 0`.
* `envelope_flow_sound_weights` — §8, third bullet ("flow with gains"), in the weights `w`:
  the cone `w y ≤ κ x y * w x`, data constraints in homogeneous form, a non-negative flow `F`
  with `(ψ z - t - Λ z) * μ₀ z ≤ ∑ x, F x z - ∑ y, κ z y * F z y` for all `z` imply
  `(∑ μ₀ w ψ) / (∑ μ₀ w) ≤ t`.
* `envelope_flow_sound_normalised`, `envelope_flow_sound_gibbs` — the same for the normalised
  ensemble `μ₀ w / ∑ μ₀ w`, and in the note's form: for every residual `g` with
  `g x - g y ≤ d x y` whose ensemble `μ_g ∝ μ₀ exp (-β g)` satisfies the data, `E_{μ_g} ψ ≤ t`
  (with `κ = exp (β d)`, `β ≥ 0`).
* `falsification_sound_weights`, `falsification_sound_ensemble`, `falsification_sound_gibbs`,
  `theorem8c_falsification` — Theorem 8(c): the same certificate with `ψ ≡ 1`, `t = 0` is
  contradictory: no member of the class is consistent with the data.
* `gibbs_variational` — the Gibbs variational (Donsker–Varadhan) inequality on a finite type,
  `E_μ G ≤ KL(μ‖μ₀) + log ∑ μ₀ exp G`, proved directly from `log t ≤ t - 1`
  (Mathlib `v4.31.0` has no Donsker–Varadhan statement).  The reference `μ₀` need not be
  normalised.
* `divergenceBall_certificate_sound` — §8, second bullet.
* `kl_lower_bound_certificate_sound` — Theorem 8(b), the inequality (not the equality at the
  supremum, which is maximum-entropy duality and is not formalised).
* `envelope_flow_certificate_witness`, `falsification_certificate_witness` — non-vacuity: on a
  two-state system the hypotheses of the flow certificate are satisfiable and the certified
  bound is attained; a falsification certificate exists for data that some ensemble satisfies.

## Not proved here

Completeness (the "equality at the infimum over `λ`" of §8, i.e. linear-programming duality),
and the strict inequality `b_min(D) > b` of Theorem 8(c) as a statement about an infimum (it
needs attainment of the infimum on a compact set); what is proved is that *no* ensemble in the
class of constant `b` is consistent with the data.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL1

open Finset

variable {X K : Type*} [Fintype X] [Fintype K]

/-! ### The Lagrangian term of the data constraints -/

/-- `Λ z = ∑ k, (λ⁺_k (φ_k z - hi_k) - λ⁻_k (φ_k z - lo_k))`: the Lagrangian term of the box
constraints `lo k ≤ E φ_k ≤ hi k` with multipliers `lp = λ⁺`, `lm = λ⁻`. -/
def dataLagrangian (φ : K → X → ℝ) (lo hi lp lm : K → ℝ) (z : X) : ℝ :=
  ∑ k, (lp k * (φ k z - hi k) - lm k * (φ k z - lo k))

/-- For non-negative multipliers, data constraints in homogeneous form
(`∑ v (φ_k - hi_k) ≤ 0 ≤ ∑ v (φ_k - lo_k)`) make the `v`-weighted Lagrangian term
non-positive.  No sign condition on `v` is needed. -/
theorem sum_mul_dataLagrangian_nonpos (v : X → ℝ) (φ : K → X → ℝ) (lo hi lp lm : K → ℝ)
    (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k)
    (hhi : ∀ k, ∑ x, v x * (φ k x - hi k) ≤ 0) (hlo : ∀ k, 0 ≤ ∑ x, v x * (φ k x - lo k)) :
    ∑ x, v x * dataLagrangian φ lo hi lp lm x ≤ 0 := by
  have e : ∑ x, v x * dataLagrangian φ lo hi lp lm x =
      ∑ k, (lp k * ∑ x, v x * (φ k x - hi k) - lm k * ∑ x, v x * (φ k x - lo k)) := by
    calc ∑ x, v x * dataLagrangian φ lo hi lp lm x
        = ∑ x, ∑ k, v x * (lp k * (φ k x - hi k) - lm k * (φ k x - lo k)) := by
          simp only [dataLagrangian, Finset.mul_sum]
      _ = ∑ k, ∑ x, v x * (lp k * (φ k x - hi k) - lm k * (φ k x - lo k)) := Finset.sum_comm
      _ = ∑ k, (lp k * ∑ x, v x * (φ k x - hi k) - lm k * ∑ x, v x * (φ k x - lo k)) := by
          refine Finset.sum_congr rfl fun k _ => ?_
          rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
          exact Finset.sum_congr rfl fun x _ => by ring
  rw [e]
  refine Finset.sum_nonpos fun k _ => ?_
  have h1 := mul_nonpos_of_nonneg_of_nonpos (hlp k) (hhi k)
  have h2 := mul_nonneg (hlm k) (hlo k)
  linarith

/-! ### (a) The model-free certificate -/

/-- **§8, model-free certificate, in the note's form.**  `μ` a probability vector whose feature
means lie in the data set `D`; `h` an upper bound of the support function of `D` at `λ`
(`∑ k, λ k * m k ≤ h` on `D`); `M` an upper bound of `ψ - λ·Φ` on `X`.  Then `E_μ ψ ≤ h + M`. -/
theorem modelFree_certificate_sound_support (μ : X → ℝ) (hμ : ∀ x, 0 ≤ μ x)
    (hμ1 : ∑ x, μ x = 1) (φ : K → X → ℝ) (D : Set (K → ℝ))
    (hD : (fun k => ∑ x, μ x * φ k x) ∈ D) (lam : K → ℝ) (h : ℝ)
    (hh : ∀ m ∈ D, ∑ k, lam k * m k ≤ h) (ψ : X → ℝ) (M : ℝ)
    (hM : ∀ x, ψ x - ∑ k, lam k * φ k x ≤ M) :
    ∑ x, μ x * ψ x ≤ h + M := by
  have h1 : ∑ x, μ x * (ψ x - ∑ k, lam k * φ k x) ≤ ∑ x, μ x * M :=
    Finset.sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (hM x) (hμ x)
  have h2 : ∑ x, μ x * M = M := by rw [← Finset.sum_mul, hμ1, one_mul]
  have h3 : ∑ x, μ x * ∑ k, lam k * φ k x = ∑ k, lam k * ∑ x, μ x * φ k x := by
    calc ∑ x, μ x * ∑ k, lam k * φ k x
        = ∑ x, ∑ k, lam k * (μ x * φ k x) := by
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [Finset.mul_sum]
          exact Finset.sum_congr rfl fun k _ => by ring
      _ = ∑ k, ∑ x, lam k * (μ x * φ k x) := Finset.sum_comm
      _ = ∑ k, lam k * ∑ x, μ x * φ k x :=
          Finset.sum_congr rfl fun k _ => (Finset.mul_sum _ _ _).symm
  have h4 : ∑ k, lam k * ∑ x, μ x * φ k x ≤ h := hh _ hD
  have h5 : ∑ x, μ x * ψ x =
      ∑ x, μ x * (ψ x - ∑ k, lam k * φ k x) + ∑ x, μ x * ∑ k, lam k * φ k x := by
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun x _ => by ring
  rw [h5, h3]
  linarith

/-- **§8, model-free certificate, box form.**  For a probability vector `μ` with
`lo k ≤ E_μ φ_k ≤ hi k` and multipliers `λ⁺, λ⁻ ≥ 0`: if `ψ x ≤ t + Λ x` for all `x`, then
`E_μ ψ ≤ t`.  No energy model appears. -/
theorem modelFree_certificate_sound (μ : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hμ1 : ∑ x, μ x = 1)
    (φ : K → X → ℝ) (lo hi : K → ℝ)
    (hlo : ∀ k, lo k ≤ ∑ x, μ x * φ k x) (hhi : ∀ k, ∑ x, μ x * φ k x ≤ hi k)
    (lp lm : K → ℝ) (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k) (ψ : X → ℝ) (t : ℝ)
    (hcert : ∀ x, ψ x ≤ t + dataLagrangian φ lo hi lp lm x) :
    ∑ x, μ x * ψ x ≤ t := by
  have hsub : ∀ (c : ℝ) (k : K), ∑ x, μ x * (φ k x - c) = ∑ x, μ x * φ k x - c := by
    intro c k
    have e : ∑ x, μ x * (φ k x - c) = ∑ x, μ x * φ k x - ∑ x, μ x * c := by
      rw [← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun x _ => mul_sub _ _ _
    rw [e, ← Finset.sum_mul, hμ1, one_mul]
  have hL : ∑ x, μ x * dataLagrangian φ lo hi lp lm x ≤ 0 :=
    sum_mul_dataLagrangian_nonpos μ φ lo hi lp lm hlp hlm
      (fun k => by rw [hsub (hi k) k]; linarith [hhi k])
      (fun k => by rw [hsub (lo k) k]; linarith [hlo k])
  have h1 : ∑ x, μ x * ψ x ≤ ∑ x, μ x * (t + dataLagrangian φ lo hi lp lm x) :=
    Finset.sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (hcert x) (hμ x)
  have h2 : ∑ x, μ x * (t + dataLagrangian φ lo hi lp lm x) =
      t + ∑ x, μ x * dataLagrangian φ lo hi lp lm x := by
    have e : ∑ x, μ x * (t + dataLagrangian φ lo hi lp lm x) =
        ∑ x, μ x * t + ∑ x, μ x * dataLagrangian φ lo hi lp lm x := by
      rw [← Finset.sum_add_distrib]
      exact Finset.sum_congr rfl fun x _ => mul_add _ _ _
    rw [e, ← Finset.sum_mul, hμ1, one_mul]
  linarith

/-! ### (b) The envelope class: flows with gains -/

/-- **The flow term is non-positive on the cone.**  For weights `w` in the cone
`w y ≤ κ x y * w x` and a non-negative flow `F`,
`∑ z, w z * (∑ x, F x z - ∑ y, κ z y * F z y) = ∑ x y, F x y * (w y - κ x y * w x) ≤ 0`. -/
theorem flow_term_nonpos (w : X → ℝ) (κ F : X → X → ℝ) (hF : ∀ x y, 0 ≤ F x y)
    (hcone : ∀ x y, w y ≤ κ x y * w x) :
    ∑ z, w z * (∑ x, F x z - ∑ y, κ z y * F z y) ≤ 0 := by
  have e1 : ∑ z, w z * ∑ x, F x z = ∑ x, ∑ y, F x y * w y := by
    calc ∑ z, w z * ∑ x, F x z = ∑ z, ∑ x, F x z * w z := by
          refine Finset.sum_congr rfl fun z _ => ?_
          rw [Finset.mul_sum]
          exact Finset.sum_congr rfl fun x _ => mul_comm _ _
      _ = ∑ x, ∑ y, F x y * w y := Finset.sum_comm
  have e2 : ∑ z, w z * ∑ y, κ z y * F z y = ∑ x, ∑ y, κ x y * F x y * w x := by
    refine Finset.sum_congr rfl fun z _ => ?_
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun y _ => by ring
  have e : ∑ z, w z * (∑ x, F x z - ∑ y, κ z y * F z y) =
      ∑ x, ∑ y, F x y * (w y - κ x y * w x) := by
    calc ∑ z, w z * (∑ x, F x z - ∑ y, κ z y * F z y)
        = ∑ z, w z * ∑ x, F x z - ∑ z, w z * ∑ y, κ z y * F z y := by
          rw [← Finset.sum_sub_distrib]
          exact Finset.sum_congr rfl fun z _ => mul_sub _ _ _
      _ = ∑ x, ∑ y, F x y * w y - ∑ x, ∑ y, κ x y * F x y * w x := by rw [e1, e2]
      _ = ∑ x, ∑ y, F x y * (w y - κ x y * w x) := by
          rw [← Finset.sum_sub_distrib]
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [← Finset.sum_sub_distrib]
          exact Finset.sum_congr rfl fun y _ => by ring
  rw [e]
  refine Finset.sum_nonpos fun x _ => Finset.sum_nonpos fun y _ => ?_
  exact mul_nonpos_of_nonneg_of_nonpos (hF x y) (by linarith [hcone x y])

/-- **§8, envelope-class certificate ("flow with gains"), in the weights.**
`w ≥ 0` in the cone `w y ≤ κ x y * w x`, `∑ μ₀ w > 0`, data constraints in homogeneous form,
multipliers `λ⁺, λ⁻ ≥ 0`, a non-negative flow `F` with
`(ψ z - t - Λ z) * μ₀ z ≤ ∑ x, F x z - ∑ y, κ z y * F z y` for every `z`.
Then `(∑ μ₀ w ψ) / (∑ μ₀ w) ≤ t`.  (No sign condition on `μ₀` or `κ` is needed.) -/
theorem envelope_flow_sound_weights (μ₀ w : X → ℝ) (hw : ∀ x, 0 ≤ w x)
    (hpos : 0 < ∑ x, μ₀ x * w x) (κ : X → X → ℝ) (hcone : ∀ x y, w y ≤ κ x y * w x)
    (φ : K → X → ℝ) (lo hi lp lm : K → ℝ) (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k)
    (hhi : ∀ k, ∑ x, μ₀ x * w x * (φ k x - hi k) ≤ 0)
    (hlo : ∀ k, 0 ≤ ∑ x, μ₀ x * w x * (φ k x - lo k))
    (ψ : X → ℝ) (t : ℝ) (F : X → X → ℝ) (hF : ∀ x y, 0 ≤ F x y)
    (hcert : ∀ z, (ψ z - t - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤
      ∑ x, F x z - ∑ y, κ z y * F z y) :
    (∑ x, μ₀ x * w x * ψ x) / (∑ x, μ₀ x * w x) ≤ t := by
  have h1 : ∑ z, w z * ((ψ z - t - dataLagrangian φ lo hi lp lm z) * μ₀ z) ≤
      ∑ z, w z * (∑ x, F x z - ∑ y, κ z y * F z y) :=
    Finset.sum_le_sum fun z _ => mul_le_mul_of_nonneg_left (hcert z) (hw z)
  have h2 := flow_term_nonpos w κ F hF hcone
  have h3 : ∑ x, μ₀ x * w x * dataLagrangian φ lo hi lp lm x ≤ 0 :=
    sum_mul_dataLagrangian_nonpos (fun x => μ₀ x * w x) φ lo hi lp lm hlp hlm hhi hlo
  have h4 : ∑ z, w z * ((ψ z - t - dataLagrangian φ lo hi lp lm z) * μ₀ z) =
      ∑ x, μ₀ x * w x * ψ x - t * ∑ x, μ₀ x * w x -
        ∑ x, μ₀ x * w x * dataLagrangian φ lo hi lp lm x := by
    rw [Finset.mul_sum, ← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun z _ => by ring
  rw [div_le_iff₀ hpos]
  linarith

/-- The same certificate for the normalised ensemble `μ = μ₀ w / ∑ μ₀ w`, with the data
constraints in their natural form `lo k ≤ E_μ φ_k ≤ hi k`. -/
theorem envelope_flow_sound_normalised (μ₀ w : X → ℝ) (hw : ∀ x, 0 ≤ w x)
    (hpos : 0 < ∑ x, μ₀ x * w x) (κ : X → X → ℝ) (hcone : ∀ x y, w y ≤ κ x y * w x)
    (φ : K → X → ℝ) (lo hi lp lm : K → ℝ) (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k)
    (hlo : ∀ k, lo k ≤ ∑ x, μ₀ x * w x / (∑ y, μ₀ y * w y) * φ k x)
    (hhi : ∀ k, ∑ x, μ₀ x * w x / (∑ y, μ₀ y * w y) * φ k x ≤ hi k)
    (ψ : X → ℝ) (t : ℝ) (F : X → X → ℝ) (hF : ∀ x y, 0 ≤ F x y)
    (hcert : ∀ z, (ψ z - t - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤
      ∑ x, F x z - ∑ y, κ z y * F z y) :
    ∑ x, μ₀ x * w x / (∑ y, μ₀ y * w y) * ψ x ≤ t := by
  have hnorm : ∀ q : X → ℝ, ∑ x, μ₀ x * w x / (∑ y, μ₀ y * w y) * q x =
      (∑ x, μ₀ x * w x * q x) / ∑ y, μ₀ y * w y := by
    intro q
    rw [Finset.sum_div]
    exact Finset.sum_congr rfl fun x _ => by ring
  have hhom : ∀ (c : ℝ) (k : K), ∑ x, μ₀ x * w x * (φ k x - c) =
      ∑ x, μ₀ x * w x * φ k x - c * ∑ x, μ₀ x * w x := by
    intro c k
    rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun x _ => by ring
  rw [hnorm ψ]
  refine envelope_flow_sound_weights μ₀ w hw hpos κ hcone φ lo hi lp lm hlp hlm ?_ ?_ ψ t F hF
    hcert
  · intro k
    have h := hhi k
    rw [hnorm (φ k), div_le_iff₀ hpos] at h
    rw [hhom (hi k) k]
    linarith
  · intro k
    have h := hlo k
    rw [hnorm (φ k), le_div_iff₀ hpos] at h
    rw [hhom (lo k) k]
    linarith

/-- The ensemble `μ_g ∝ μ₀ · exp (-β g)` of the residual `g` (the theory division's `tilt`). -/
def gibbsTilt (μ₀ g : X → ℝ) (β : ℝ) (x : X) : ℝ :=
  μ₀ x * Real.exp (-β * g x) / ∑ y, μ₀ y * Real.exp (-β * g y)

/-- The normalising sum of `gibbsTilt` is positive for non-negative `μ₀` of positive mass. -/
theorem gibbsTilt_norm_pos (μ₀ g : X → ℝ) (β : ℝ) (hμ₀ : ∀ x, 0 ≤ μ₀ x)
    (hμ₀pos : 0 < ∑ x, μ₀ x) : 0 < ∑ x, μ₀ x * Real.exp (-β * g x) := by
  obtain ⟨x, hx⟩ : ∃ x, 0 < μ₀ x := by
    by_contra hno
    have : ∑ x, μ₀ x ≤ 0 := Finset.sum_nonpos fun x _ => not_lt.mp fun hx => hno ⟨x, hx⟩
    linarith
  exact Finset.sum_pos' (fun y _ => mul_nonneg (hμ₀ y) (Real.exp_pos _).le)
    ⟨x, Finset.mem_univ x, mul_pos hx (Real.exp_pos _)⟩

/-- `gibbsTilt` is a probability vector. -/
theorem sum_gibbsTilt (μ₀ g : X → ℝ) (β : ℝ) (hμ₀ : ∀ x, 0 ≤ μ₀ x) (hμ₀pos : 0 < ∑ x, μ₀ x) :
    ∑ x, gibbsTilt μ₀ g β x = 1 := by
  unfold gibbsTilt
  rw [← Finset.sum_div]
  exact div_self (gibbsTilt_norm_pos μ₀ g β hμ₀ hμ₀pos).ne'

/-- **§8, envelope-class certificate, in the note's form.**  Model `μ₀` (non-negative, positive
mass), envelope `d`, `β ≥ 0`, `κ = exp (β d)`.  If a flow certificate holds, then
`E_{μ_g} ψ ≤ t` for every admissible residual `g` (`g x - g y ≤ d x y`) whose ensemble
`μ_g ∝ μ₀ exp (-β g)` is consistent with the data. -/
theorem envelope_flow_sound_gibbs {β : ℝ} (hβ : 0 ≤ β) (d : X → X → ℝ) (g : X → ℝ)
    (hg : ∀ x y, g x - g y ≤ d x y) (μ₀ : X → ℝ) (hμ₀ : ∀ x, 0 ≤ μ₀ x)
    (hμ₀pos : 0 < ∑ x, μ₀ x)
    (φ : K → X → ℝ) (lo hi lp lm : K → ℝ) (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k)
    (hlo : ∀ k, lo k ≤ ∑ x, gibbsTilt μ₀ g β x * φ k x)
    (hhi : ∀ k, ∑ x, gibbsTilt μ₀ g β x * φ k x ≤ hi k)
    (ψ : X → ℝ) (t : ℝ) (F : X → X → ℝ) (hF : ∀ x y, 0 ≤ F x y)
    (hcert : ∀ z, (ψ z - t - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤
      ∑ x, F x z - ∑ y, Real.exp (β * d z y) * F z y) :
    ∑ x, gibbsTilt μ₀ g β x * ψ x ≤ t := by
  have hpos := gibbsTilt_norm_pos μ₀ g β hμ₀ hμ₀pos
  have hcone : ∀ x y, Real.exp (-β * g y) ≤ Real.exp (β * d x y) * Real.exp (-β * g x) := by
    intro x y
    rw [← Real.exp_add, Real.exp_le_exp]
    have := mul_le_mul_of_nonneg_left (hg x y) hβ
    linarith
  exact envelope_flow_sound_normalised μ₀ (fun x => Real.exp (-β * g x))
    (fun x => (Real.exp_pos _).le) hpos (fun x y => Real.exp (β * d x y)) hcone
    φ lo hi lp lm hlp hlm hlo hhi ψ t F hF hcert

/-! ### (c) Falsification (Theorem 8(c)) -/

/-- **Theorem 8(c), in the weights.**  A flow certificate with `ψ ≡ 1`, `t = 0` is
contradictory: no weight vector of the cone with positive mass satisfies the data. -/
theorem falsification_sound_weights (μ₀ w : X → ℝ) (hw : ∀ x, 0 ≤ w x)
    (hpos : 0 < ∑ x, μ₀ x * w x) (κ : X → X → ℝ) (hcone : ∀ x y, w y ≤ κ x y * w x)
    (φ : K → X → ℝ) (lo hi lp lm : K → ℝ) (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k)
    (hhi : ∀ k, ∑ x, μ₀ x * w x * (φ k x - hi k) ≤ 0)
    (hlo : ∀ k, 0 ≤ ∑ x, μ₀ x * w x * (φ k x - lo k))
    (F : X → X → ℝ) (hF : ∀ x y, 0 ≤ F x y)
    (hcert : ∀ z, (1 - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤
      ∑ x, F x z - ∑ y, κ z y * F z y) : False := by
  have h := envelope_flow_sound_weights μ₀ w hw hpos κ hcone φ lo hi lp lm hlp hlm hhi hlo
    (fun _ => 1) 0 F hF (fun z => by rw [sub_zero]; exact hcert z)
  simp only [mul_one] at h
  rw [div_self hpos.ne'] at h
  linarith

/-- **Theorem 8(c), in the ensemble.**  Model `μ₀ > 0`.  If a falsification certificate exists
for the gains `κ`, then no probability vector `μ` in the ball
`μ y * μ₀ x ≤ κ x y * (μ x * μ₀ y)` (for `κ = exp (b d)`: Lipschitz divergence
`D_d(μ‖μ₀) ≤ b`) satisfies the data `lo k ≤ E_μ φ_k ≤ hi k`. -/
theorem falsification_sound_ensemble (μ₀ μ : X → ℝ) (hμ₀ : ∀ x, 0 < μ₀ x) (hμ : ∀ x, 0 ≤ μ x)
    (hμ1 : ∑ x, μ x = 1) (κ : X → X → ℝ)
    (hball : ∀ x y, μ y * μ₀ x ≤ κ x y * (μ x * μ₀ y))
    (φ : K → X → ℝ) (lo hi lp lm : K → ℝ) (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k)
    (hlo : ∀ k, lo k ≤ ∑ x, μ x * φ k x) (hhi : ∀ k, ∑ x, μ x * φ k x ≤ hi k)
    (F : X → X → ℝ) (hF : ∀ x y, 0 ≤ F x y)
    (hcert : ∀ z, (1 - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤
      ∑ x, F x z - ∑ y, κ z y * F z y) : False := by
  have hw_eq : ∀ x, μ₀ x * (μ x / μ₀ x) = μ x := by
    intro x
    have := (hμ₀ x).ne'
    field_simp
  have hsub : ∀ (c : ℝ) (k : K), ∑ x, μ x * (φ k x - c) = ∑ x, μ x * φ k x - c := by
    intro c k
    have e : ∑ x, μ x * (φ k x - c) = ∑ x, μ x * φ k x - ∑ x, μ x * c := by
      rw [← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun x _ => mul_sub _ _ _
    rw [e, ← Finset.sum_mul, hμ1, one_mul]
  refine falsification_sound_weights μ₀ (fun x => μ x / μ₀ x)
    (fun x => div_nonneg (hμ x) (hμ₀ x).le) ?_ κ ?_ φ lo hi lp lm hlp hlm ?_ ?_ F hF hcert
  · simp only [hw_eq]
    rw [hμ1]
    exact one_pos
  · intro x y
    have h := hball x y
    show μ y / μ₀ y ≤ κ x y * (μ x / μ₀ x)
    rw [div_le_iff₀ (hμ₀ y)]
    have e : κ x y * (μ x / μ₀ x) * μ₀ y = κ x y * (μ x * μ₀ y) / μ₀ x := by ring
    rw [e, le_div_iff₀ (hμ₀ x)]
    exact h
  · intro k
    simp only [hw_eq]
    rw [hsub (hi k) k]
    linarith [hhi k]
  · intro k
    simp only [hw_eq]
    rw [hsub (lo k) k]
    linarith [hlo k]

/-- **Theorem 8(c), for residuals.**  If a falsification certificate exists for
`κ = exp (β d)`, then no residual `g` with `g x - g y ≤ d x y` has an ensemble
`μ_g ∝ μ₀ exp (-β g)` consistent with the data. -/
theorem falsification_sound_gibbs {β : ℝ} (hβ : 0 ≤ β) (d : X → X → ℝ) (μ₀ : X → ℝ)
    (hμ₀ : ∀ x, 0 ≤ μ₀ x) (hμ₀pos : 0 < ∑ x, μ₀ x)
    (φ : K → X → ℝ) (lo hi lp lm : K → ℝ) (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k)
    (F : X → X → ℝ) (hF : ∀ x y, 0 ≤ F x y)
    (hcert : ∀ z, (1 - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤
      ∑ x, F x z - ∑ y, Real.exp (β * d z y) * F z y)
    (g : X → ℝ) (hg : ∀ x y, g x - g y ≤ d x y)
    (hlo : ∀ k, lo k ≤ ∑ x, gibbsTilt μ₀ g β x * φ k x)
    (hhi : ∀ k, ∑ x, gibbsTilt μ₀ g β x * φ k x ≤ hi k) : False := by
  have h := envelope_flow_sound_gibbs hβ d g hg μ₀ hμ₀ hμ₀pos φ lo hi lp lm hlp hlm hlo hhi
    (fun _ => 1) 0 F hF (fun z => by rw [sub_zero]; exact hcert z)
  simp only [mul_one] at h
  rw [sum_gibbsTilt μ₀ g β hμ₀ hμ₀pos] at h
  linarith

/-- **Theorem 8(c) as stated in the note.**  Inverse temperature `β > 0`, envelope `d`, class of
constant `b`: residuals with `g x - g y ≤ (b / β) * d x y`.  If there are multipliers
`λ⁺, λ⁻ ≥ 0` and a flow `F ≥ 0` with
`(1 - Λ z) * μ₀ z ≤ ∑ x, F x z - ∑ y, exp (b * d z y) * F z y` for all `z`, then the data are
inconsistent with the class: no residual of the class has an ensemble satisfying the data. -/
theorem theorem8c_falsification {β b : ℝ} (hβ : 0 < β) (d : X → X → ℝ) (μ₀ : X → ℝ)
    (hμ₀ : ∀ x, 0 ≤ μ₀ x) (hμ₀pos : 0 < ∑ x, μ₀ x)
    (φ : K → X → ℝ) (lo hi lp lm : K → ℝ) (hlp : ∀ k, 0 ≤ lp k) (hlm : ∀ k, 0 ≤ lm k)
    (F : X → X → ℝ) (hF : ∀ x y, 0 ≤ F x y)
    (hcert : ∀ z, (1 - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤
      ∑ x, F x z - ∑ y, Real.exp (b * d z y) * F z y) :
    ¬ ∃ g : X → ℝ, (∀ x y, g x - g y ≤ b / β * d x y) ∧
      (∀ k, lo k ≤ ∑ x, gibbsTilt μ₀ g β x * φ k x) ∧
      (∀ k, ∑ x, gibbsTilt μ₀ g β x * φ k x ≤ hi k) := by
  rintro ⟨g, hg, hlo, hhi⟩
  have hcert' : ∀ z, (1 - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤
      ∑ x, F x z - ∑ y, Real.exp (β * (b / β * d z y)) * F z y := by
    intro z
    have e : ∀ y, β * (b / β * d z y) = b * d z y := by
      intro y
      field_simp
    simp only [e]
    exact hcert z
  exact falsification_sound_gibbs hβ.le (fun x y => b / β * d x y) μ₀ hμ₀ hμ₀pos φ lo hi lp lm
    hlp hlm F hF hcert' g hg hlo hhi

/-! ### (d) The divergence ball: Gibbs variational inequality -/

/-- Relative entropy `KL(p‖q) = ∑ p (log p - log q)` on a finite type (terms with `p x = 0`
vanish; meaningful when `p` vanishes wherever `q` does).  Same expression as the theory
division's `klFin`. -/
def klDivFin (p q : X → ℝ) : ℝ := ∑ x, p x * (Real.log (p x) - Real.log (q x))

/-- **Gibbs variational (Donsker–Varadhan) inequality on a finite type.**  For a probability
vector `μ`, non-negative reference weights `μ₀` (not necessarily normalised) with `μ ≪ μ₀`, and
any `G : X → ℝ`:  `E_μ G ≤ KL(μ‖μ₀) + log ∑ μ₀ exp G`. -/
theorem gibbs_variational (μ μ₀ : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hμ1 : ∑ x, μ x = 1)
    (hμ₀ : ∀ x, 0 ≤ μ₀ x) (hac : ∀ x, μ₀ x = 0 → μ x = 0) (G : X → ℝ) :
    ∑ x, μ x * G x ≤ klDivFin μ μ₀ + Real.log (∑ x, μ₀ x * Real.exp (G x)) := by
  obtain ⟨Z, hZ⟩ : ∃ Z : ℝ, Z = ∑ x, μ₀ x * Real.exp (G x) := ⟨_, rfl⟩
  have hZpos : 0 < Z := by
    obtain ⟨x, hx⟩ : ∃ x, 0 < μ x := by
      by_contra hno
      have : ∑ x, μ x ≤ 0 := Finset.sum_nonpos fun x _ => not_lt.mp fun hx => hno ⟨x, hx⟩
      linarith
    have hx0 : 0 < μ₀ x := lt_of_le_of_ne (hμ₀ x) fun h => hx.ne' (hac x h.symm)
    rw [hZ]
    exact Finset.sum_pos' (fun y _ => mul_nonneg (hμ₀ y) (Real.exp_pos _).le)
      ⟨x, Finset.mem_univ x, mul_pos hx0 (Real.exp_pos _)⟩
  have hterm : ∀ x, μ x * G x ≤
      μ x * (Real.log (μ x) - Real.log (μ₀ x)) + μ x * Real.log Z +
        (μ₀ x * Real.exp (G x) / Z - μ x) := by
    intro x
    rcases (hμ x).eq_or_lt with h0 | hpos
    · have hν : 0 ≤ μ₀ x * Real.exp (G x) / Z :=
        div_nonneg (mul_nonneg (hμ₀ x) (Real.exp_pos _).le) hZpos.le
      rw [← h0]
      linarith
    · have hx0 : 0 < μ₀ x := lt_of_le_of_ne (hμ₀ x) fun h => hpos.ne' (hac x h.symm)
      have hν : 0 < μ₀ x * Real.exp (G x) / Z := div_pos (mul_pos hx0 (Real.exp_pos _)) hZpos
      have h1 := Real.log_le_sub_one_of_pos (div_pos hν hpos)
      rw [Real.log_div hν.ne' hpos.ne', Real.log_div (mul_pos hx0 (Real.exp_pos _)).ne' hZpos.ne',
        Real.log_mul hx0.ne' (Real.exp_pos _).ne', Real.log_exp] at h1
      have h2 := mul_le_mul_of_nonneg_left h1 hpos.le
      have h3 : μ x * (μ₀ x * Real.exp (G x) / Z / μ x - 1) =
          μ₀ x * Real.exp (G x) / Z - μ x := by
        field_simp
      linarith
  have hsum := Finset.sum_le_sum fun x (_ : x ∈ (Finset.univ : Finset X)) => hterm x
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib] at hsum
  have e1 : ∑ x, μ x * Real.log Z = Real.log Z := by rw [← Finset.sum_mul, hμ1, one_mul]
  have e2 : ∑ x, μ₀ x * Real.exp (G x) / Z = 1 := by
    rw [← Finset.sum_div, ← hZ]
    exact div_self hZpos.ne'
  rw [← hZ]
  unfold klDivFin
  linarith

/-- **§8, divergence-ball certificate.**  `μ` a probability vector with `μ ≪ μ₀`,
`KL(μ‖μ₀) ≤ ρ`, feature means in `D`; `h` an upper bound of the support function of `D` at
`λ`; `η > 0`.  Then
`E_μ ψ ≤ h + η ρ + η log ∑ μ₀ exp ((ψ - λ·Φ) / η)`. -/
theorem divergenceBall_certificate_sound (μ μ₀ : X → ℝ) (hμ : ∀ x, 0 ≤ μ x)
    (hμ1 : ∑ x, μ x = 1) (hμ₀ : ∀ x, 0 ≤ μ₀ x) (hac : ∀ x, μ₀ x = 0 → μ x = 0)
    (φ : K → X → ℝ) (D : Set (K → ℝ)) (hD : (fun k => ∑ x, μ x * φ k x) ∈ D)
    (lam : K → ℝ) (h : ℝ) (hh : ∀ m ∈ D, ∑ k, lam k * m k ≤ h)
    {ρ : ℝ} (hρ : klDivFin μ μ₀ ≤ ρ) {η : ℝ} (hη : 0 < η) (ψ : X → ℝ) :
    ∑ x, μ x * ψ x ≤ h + η * ρ +
      η * Real.log (∑ x, μ₀ x * Real.exp ((ψ x - ∑ k, lam k * φ k x) / η)) := by
  have hDV := gibbs_variational μ μ₀ hμ hμ1 hμ₀ hac (fun x => (ψ x - ∑ k, lam k * φ k x) / η)
  have h3 : ∑ x, μ x * ∑ k, lam k * φ k x = ∑ k, lam k * ∑ x, μ x * φ k x := by
    calc ∑ x, μ x * ∑ k, lam k * φ k x
        = ∑ x, ∑ k, lam k * (μ x * φ k x) := by
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [Finset.mul_sum]
          exact Finset.sum_congr rfl fun k _ => by ring
      _ = ∑ k, ∑ x, lam k * (μ x * φ k x) := Finset.sum_comm
      _ = ∑ k, lam k * ∑ x, μ x * φ k x :=
          Finset.sum_congr rfl fun k _ => (Finset.mul_sum _ _ _).symm
  have h4 : ∑ k, lam k * ∑ x, μ x * φ k x ≤ h := hh _ hD
  have h5 : ∑ x, μ x * ψ x =
      η * ∑ x, μ x * ((ψ x - ∑ k, lam k * φ k x) / η) + ∑ x, μ x * ∑ k, lam k * φ k x := by
    rw [Finset.mul_sum, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun x _ => ?_
    field_simp
    ring
  have h6 : η * ∑ x, μ x * ((ψ x - ∑ k, lam k * φ k x) / η) ≤
      η * (klDivFin μ μ₀ +
        Real.log (∑ x, μ₀ x * Real.exp ((ψ x - ∑ k, lam k * φ k x) / η))) :=
    mul_le_mul_of_nonneg_left hDV hη.le
  have h7 : η * klDivFin μ μ₀ ≤ η * ρ := mul_le_mul_of_nonneg_left hρ hη.le
  rw [h5, h3]
  linarith

/-- **Theorem 8(b), the inequality.**  For every `λ` and every probability vector `μ ≪ μ₀` with
feature means in `D`:  `KL(μ‖μ₀) ≥ -h - log ∑ μ₀ exp (-λ·Φ)`, `h` an upper bound of the support
function of `D` at `λ`.  Hence `ρ_min(D) ≥ -h_D(λ) - log E_{μ₀} exp (-λ·Φ)`. -/
theorem kl_lower_bound_certificate_sound (μ μ₀ : X → ℝ) (hμ : ∀ x, 0 ≤ μ x)
    (hμ1 : ∑ x, μ x = 1) (hμ₀ : ∀ x, 0 ≤ μ₀ x) (hac : ∀ x, μ₀ x = 0 → μ x = 0)
    (φ : K → X → ℝ) (D : Set (K → ℝ)) (hD : (fun k => ∑ x, μ x * φ k x) ∈ D)
    (lam : K → ℝ) (h : ℝ) (hh : ∀ m ∈ D, ∑ k, lam k * m k ≤ h) :
    -h - Real.log (∑ x, μ₀ x * Real.exp (-∑ k, lam k * φ k x)) ≤ klDivFin μ μ₀ := by
  have hDV := gibbs_variational μ μ₀ hμ hμ1 hμ₀ hac (fun x => -∑ k, lam k * φ k x)
  have h3 : ∑ x, μ x * -∑ k, lam k * φ k x = -∑ k, lam k * ∑ x, μ x * φ k x := by
    calc ∑ x, μ x * -∑ k, lam k * φ k x
        = -∑ x, ∑ k, lam k * (μ x * φ k x) := by
          rw [← Finset.sum_neg_distrib]
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [mul_neg, Finset.mul_sum]
          congr 1
          exact Finset.sum_congr rfl fun k _ => by ring
      _ = -∑ k, ∑ x, lam k * (μ x * φ k x) := by rw [Finset.sum_comm]
      _ = -∑ k, lam k * ∑ x, μ x * φ k x := by
          congr 1
          exact Finset.sum_congr rfl fun k _ => (Finset.mul_sum _ _ _).symm
  have h4 : ∑ k, lam k * ∑ x, μ x * φ k x ≤ h := hh _ hD
  have hDV' : ∑ x, μ x * -∑ k, lam k * φ k x ≤
      klDivFin μ μ₀ + Real.log (∑ x, μ₀ x * Real.exp (-∑ k, lam k * φ k x)) := hDV
  rw [h3] at hDV'
  linarith

/-! ### Non-vacuity witnesses on a two-state system -/

/-- **The flow certificate is satisfiable and can be tight.**  Two states, uniform model, gains
`κ = 2` between distinct states (`b · d = log 2`), no data, target `ψ = 1_{true}`.  The flow
`F false true = 1/6` certifies `E ψ ≤ 2/3`, and the weights `w = (1, 2)` of the cone attain
`2/3`. -/
theorem envelope_flow_certificate_witness :
    ∃ (μ₀ w ψ : Bool → ℝ) (κ F : Bool → Bool → ℝ) (t : ℝ),
      (∀ x, 0 ≤ w x) ∧ (0 < ∑ x, μ₀ x * w x) ∧ (∀ x y, w y ≤ κ x y * w x) ∧
      (∀ x y, 0 ≤ F x y) ∧
      (∀ z, (ψ z - t - dataLagrangian (fun (_ : Fin 0) (_ : Bool) => (0 : ℝ)) (fun _ => 0)
          (fun _ => 0) (fun _ => 0) (fun _ => 0) z) * μ₀ z ≤
        ∑ x, F x z - ∑ y, κ z y * F z y) ∧
      (∑ x, μ₀ x * w x * ψ x) / (∑ x, μ₀ x * w x) = t := by
  refine ⟨fun _ => 1 / 2, fun x => if x then 2 else 1, fun x => if x then 1 else 0,
    fun x y => if x = y then 1 else 2, fun x y => if x = false ∧ y = true then 1 / 6 else 0,
    2 / 3, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro x
    cases x <;> norm_num
  · norm_num [Fintype.sum_bool]
  · intro x y
    cases x <;> cases y <;> norm_num
  · intro x y
    cases x <;> cases y <;> norm_num
  · intro z
    cases z <;> norm_num [Fintype.sum_bool, dataLagrangian]
  · norm_num [Fintype.sum_bool]

/-- **A falsification certificate exists for satisfiable data.**  Two states, uniform model,
gains `κ = 2` between distinct states, one feature `φ = 1_{true}` with data
`9/10 ≤ E φ ≤ 1` (satisfied by the ensemble `(1/20, 19/20)`).  Multipliers `λ⁺ = 0`, `λ⁻ = 5`
and the flow `F false true = 3/4` satisfy the hypothesis of `falsification_sound_weights`:
every ensemble of the class has `E φ ≤ 2/3 < 9/10`. -/
theorem falsification_certificate_witness :
    ∃ (μ₀ : Bool → ℝ) (κ F : Bool → Bool → ℝ) (φ : Unit → Bool → ℝ) (lo hi lp lm : Unit → ℝ),
      (∀ x, 0 < μ₀ x) ∧ ∑ x, μ₀ x = 1 ∧ (∀ k, 0 ≤ lp k) ∧ (∀ k, 0 ≤ lm k) ∧
      (∀ x y, 0 ≤ F x y) ∧
      (∀ z, (1 - dataLagrangian φ lo hi lp lm z) * μ₀ z ≤ ∑ x, F x z - ∑ y, κ z y * F z y) ∧
      ∃ μ : Bool → ℝ, (∀ x, 0 ≤ μ x) ∧ ∑ x, μ x = 1 ∧
        ∀ k, lo k ≤ ∑ x, μ x * φ k x ∧ ∑ x, μ x * φ k x ≤ hi k := by
  refine ⟨fun _ => 1 / 2, fun x y => if x = y then 1 else 2,
    fun x y => if x = false ∧ y = true then 3 / 4 else 0, fun _ x => if x then 1 else 0,
    fun _ => 9 / 10, fun _ => 1, fun _ => 0, fun _ => 5, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro x
    norm_num
  · norm_num [Fintype.sum_bool]
  · intro k
    norm_num
  · intro k
    norm_num
  · intro x y
    cases x <;> cases y <;> norm_num
  · intro z
    cases z <;> norm_num [Fintype.sum_bool, dataLagrangian]
  · refine ⟨fun x => if x then 19 / 20 else 1 / 20, ?_, ?_, ?_⟩
    · intro x
      cases x <;> norm_num
    · norm_num [Fintype.sum_bool]
    · intro k
      norm_num [Fintype.sum_bool]

end ScienceL1

end

#print axioms ScienceL1.modelFree_certificate_sound_support
#print axioms ScienceL1.modelFree_certificate_sound
#print axioms ScienceL1.envelope_flow_sound_weights
#print axioms ScienceL1.envelope_flow_sound_normalised
#print axioms ScienceL1.envelope_flow_sound_gibbs
#print axioms ScienceL1.falsification_sound_weights
#print axioms ScienceL1.falsification_sound_ensemble
#print axioms ScienceL1.falsification_sound_gibbs
#print axioms ScienceL1.theorem8c_falsification
#print axioms ScienceL1.gibbs_variational
#print axioms ScienceL1.divergenceBall_certificate_sound
#print axioms ScienceL1.kl_lower_bound_certificate_sound
#print axioms ScienceL1.envelope_flow_certificate_witness
#print axioms ScienceL1.falsification_certificate_witness
