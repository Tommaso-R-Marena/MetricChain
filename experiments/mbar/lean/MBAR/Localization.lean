import Mathlib

/-!
# Deterministic localisation (handoff B1/C1) and sound composition of error bounds (E3)

Division 9, `docs/mbar/MATHEMATICS.md` part B (audit of B1, C1) and E3.

`Softmax`: for nonnegative weights `a_j` (not all zero) and a direction `h`, with
`S p t = Σ_j a_j h_j^p e^{t h_j}`, the tilted mean `m t = S 1 t / S 0 t` and tilted variance
`Vr t = S 2 t / S 0 t − (m t)²`:

* `hasDerivAt_m`  : `m' = Vr`;
* `hasDerivAt_Vr` : `Vr' = κ₃` (third central moment);
* `kappa_ge`      : `κ₃ ≥ −ρ · Vr` whenever `h_i − h_j ≤ ρ` for all `i, j`
                    (the self-concordance-type bound with the sharp constant 1);
* `Vr_ge`         : `Vr t ≥ e^{−ρ t} Vr 0` for `t ≥ 0`;
* `curvature_integrated` : `m 1 − m 0 ≥ Vr 0 · (1 − e^{−ρ})/ρ`.

With `a_j = s_j e^{f_j} q_j(x_n)` this is, sample by sample, the inequality
`(g(f+h) − g(f))·h ≥ h·H_N(f)·h (1 − e^{−osc h})/osc h` of handoff B1 (`curvature_sum`).

* `pairing_le`       : `|Σ y_i h_i| ≤ (ρ/2) Σ|y_i|` for zero-sum `y` (cut norm against oscillation);
* `cut_localization` : the scalar inversion `ρ ≤ −log(1 − R ε)` of handoff C1;
* `free_energy_envelope`, `contrast_composition` : a uniform energy envelope `|ũ − u| ≤ ε` moves a
  free energy by at most `ε`; a statistical radius and envelope radii add (handoff E3).

Not formalised: the Hoeffding bound over cuts used by C1 — external, [X].
-/

open Finset

namespace MBAR

namespace Softmax

variable {ι : Type*} [Fintype ι] (a h : ι → ℝ)

/-- `S p t = Σ_j a_j h_j^p e^{t h_j}`. -/
noncomputable def S (p : ℕ) (t : ℝ) : ℝ := ∑ j, a j * h j ^ p * Real.exp (t * h j)

/-- Tilted mean of `h`. -/
noncomputable def m (t : ℝ) : ℝ := S a h 1 t / S a h 0 t

/-- Tilted variance of `h`. -/
noncomputable def Vr (t : ℝ) : ℝ := S a h 2 t / S a h 0 t - m a h t ^ 2

/-- Tilted third central moment of `h`. -/
noncomputable def kappa (t : ℝ) : ℝ :=
  S a h 3 t / S a h 0 t - 3 * m a h t * (S a h 2 t / S a h 0 t) + 2 * m a h t ^ 3

lemma hasDerivAt_S (p : ℕ) (t : ℝ) : HasDerivAt (S a h p) (S a h (p + 1) t) t := by
  have h1 : ∀ j ∈ (Finset.univ : Finset ι),
      HasDerivAt (fun y : ℝ => a j * h j ^ p * Real.exp (y * h j))
        (a j * h j ^ (p + 1) * Real.exp (t * h j)) t := by
    intro j _
    have h2 : HasDerivAt (fun y : ℝ => y * h j) (h j) t := by
      simpa using (hasDerivAt_id t).mul_const (h j)
    have h3 : HasDerivAt (fun y : ℝ => a j * h j ^ p * Real.exp (y * h j))
        (a j * h j ^ p * (Real.exp (t * h j) * h j)) t := (h2.exp).const_mul (a j * h j ^ p)
    have e : a j * h j ^ p * (Real.exp (t * h j) * h j)
        = a j * h j ^ (p + 1) * Real.exp (t * h j) := by ring
    rw [e] at h3
    exact h3
  have h4 := HasDerivAt.fun_sum h1
  exact h4

lemma S0_pos (ha : ∀ j, 0 ≤ a j) (hpos : ∃ j, 0 < a j) (t : ℝ) : 0 < S a h 0 t := by
  obtain ⟨j0, hj0⟩ := hpos
  unfold S
  refine Finset.sum_pos' (fun j _ => ?_) ⟨j0, Finset.mem_univ j0, ?_⟩
  · simp only [pow_zero, mul_one]; exact mul_nonneg (ha j) (Real.exp_pos _).le
  · simp only [pow_zero, mul_one]; exact mul_pos hj0 (Real.exp_pos _)

variable {a h}

lemma hasDerivAt_m (hZ : ∀ t, 0 < S a h 0 t) (t : ℝ) : HasDerivAt (m a h) (Vr a h t) t := by
  have h0 : HasDerivAt (S a h 0) (S a h 1 t) t := hasDerivAt_S a h 0 t
  have h1 : HasDerivAt (S a h 1) (S a h 2 t) t := hasDerivAt_S a h 1 t
  have hZt := (hZ t).ne'
  have h2 : HasDerivAt (m a h)
      ((S a h 2 t * S a h 0 t - S a h 1 t * S a h 1 t) / S a h 0 t ^ 2) t := h1.div h0 hZt
  convert h2 using 1
  simp only [Vr, m]
  field_simp

lemma hasDerivAt_Vr (hZ : ∀ t, 0 < S a h 0 t) (t : ℝ) :
    HasDerivAt (Vr a h) (kappa a h t) t := by
  have h0 : HasDerivAt (S a h 0) (S a h 1 t) t := hasDerivAt_S a h 0 t
  have h2 : HasDerivAt (S a h 2) (S a h 3 t) t := hasDerivAt_S a h 2 t
  have hZt := (hZ t).ne'
  have h3 : HasDerivAt (Vr a h)
      ((S a h 3 t * S a h 0 t - S a h 2 t * S a h 1 t) / S a h 0 t ^ 2
        - ((2 : ℕ) : ℝ) * m a h t ^ (2 - 1) * Vr a h t) t :=
    (h2.div h0 hZt).sub ((hasDerivAt_m hZ t).pow 2)
  convert h3 using 1
  simp only [kappa, Vr, m, Nat.reduceSub, pow_one, Nat.cast_ofNat]
  field_simp
  ring

lemma expand2 (t μ : ℝ) :
    ∑ j, a j * Real.exp (t * h j) * (h j - μ) ^ 2
      = S a h 2 t - 2 * μ * S a h 1 t + μ ^ 2 * S a h 0 t := by
  simp only [S, Finset.mul_sum]
  rw [← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl (fun j _ => by ring)

lemma expand3 (t μ : ℝ) :
    ∑ j, a j * Real.exp (t * h j) * (h j - μ) ^ 3
      = S a h 3 t - 3 * μ * S a h 2 t + 3 * μ ^ 2 * S a h 1 t - μ ^ 3 * S a h 0 t := by
  simp only [S, Finset.mul_sum]
  rw [← Finset.sum_sub_distrib, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl (fun j _ => by ring)

/-- Centred form of the variance. -/
lemma S0_mul_Vr (hZ : ∀ t, 0 < S a h 0 t) (t : ℝ) :
    S a h 0 t * Vr a h t = ∑ j, a j * Real.exp (t * h j) * (h j - m a h t) ^ 2 := by
  have hZt := (hZ t).ne'
  rw [expand2]
  simp only [Vr, m]
  field_simp
  ring

/-- Centred form of the third moment. -/
lemma S0_mul_kappa (hZ : ∀ t, 0 < S a h 0 t) (t : ℝ) :
    S a h 0 t * kappa a h t = ∑ j, a j * Real.exp (t * h j) * (h j - m a h t) ^ 3 := by
  have hZt := (hZ t).ne'
  rw [expand3]
  simp only [kappa, m]
  field_simp
  ring

lemma Vr_nonneg (ha : ∀ j, 0 ≤ a j) (hZ : ∀ t, 0 < S a h 0 t) (t : ℝ) : 0 ≤ Vr a h t := by
  have h1 : 0 ≤ S a h 0 t * Vr a h t := by
    rw [S0_mul_Vr hZ t]
    exact Finset.sum_nonneg (fun j _ =>
      mul_nonneg (mul_nonneg (ha j) (Real.exp_pos _).le) (sq_nonneg _))
  exact nonneg_of_mul_nonneg_right h1 (hZ t)

/-- The tilted mean is within `ρ` of every value of `h`. -/
lemma m_le (ha : ∀ j, 0 ≤ a j) (hZ : ∀ t, 0 < S a h 0 t) {ρ : ℝ} (hρ : ∀ i j, h i - h j ≤ ρ)
    (t : ℝ) (j : ι) : m a h t ≤ h j + ρ := by
  rw [m, div_le_iff₀ (hZ t)]
  have e1 : S a h 1 t = ∑ i, a i * Real.exp (t * h i) * h i := by
    simp only [S]; exact Finset.sum_congr rfl (fun i _ => by ring)
  have e0 : (h j + ρ) * S a h 0 t = ∑ i, a i * Real.exp (t * h i) * (h j + ρ) := by
    simp only [S, Finset.mul_sum]; exact Finset.sum_congr rfl (fun i _ => by ring)
  rw [e1, e0]
  refine Finset.sum_le_sum (fun i _ => ?_)
  exact mul_le_mul_of_nonneg_left (by linarith [hρ i j])
    (mul_nonneg (ha i) (Real.exp_pos _).le)

/-- **Third-moment bound**: `κ₃ ≥ −ρ · Var` when the oscillation of `h` is at most `ρ`. -/
theorem kappa_ge (ha : ∀ j, 0 ≤ a j) (hZ : ∀ t, 0 < S a h 0 t) {ρ : ℝ}
    (hρ : ∀ i j, h i - h j ≤ ρ) (t : ℝ) : -ρ * Vr a h t ≤ kappa a h t := by
  have h1 : 0 ≤ S a h 0 t * (kappa a h t + ρ * Vr a h t) := by
    have e : S a h 0 t * (kappa a h t + ρ * Vr a h t)
        = ∑ j, a j * Real.exp (t * h j) * ((h j - m a h t) ^ 2 * (h j - m a h t + ρ)) := by
      rw [mul_add, S0_mul_kappa hZ t, ← mul_assoc, mul_comm (S a h 0 t) ρ, mul_assoc,
        S0_mul_Vr hZ t, Finset.mul_sum, ← Finset.sum_add_distrib]
      exact Finset.sum_congr rfl (fun j _ => by ring)
    rw [e]
    refine Finset.sum_nonneg (fun j _ => ?_)
    have h2 := m_le ha hZ hρ t j
    exact mul_nonneg (mul_nonneg (ha j) (Real.exp_pos _).le)
      (mul_nonneg (sq_nonneg _) (by linarith))
  have h3 := nonneg_of_mul_nonneg_right h1 (hZ t)
  linarith

/-- `t ↦ e^{ρ t} Vr t` is nondecreasing. -/
lemma monotone_exp_mul_Vr (ha : ∀ j, 0 ≤ a j) (hZ : ∀ t, 0 < S a h 0 t) {ρ : ℝ}
    (hρ : ∀ i j, h i - h j ≤ ρ) : Monotone (fun t => Real.exp (ρ * t) * Vr a h t) := by
  have hd : ∀ t, HasDerivAt (fun t => Real.exp (ρ * t) * Vr a h t)
      (Real.exp (ρ * t) * ρ * Vr a h t + Real.exp (ρ * t) * kappa a h t) t := by
    intro t
    have h1 : HasDerivAt (fun y : ℝ => ρ * y) ρ t := by
      simpa using (hasDerivAt_id t).const_mul ρ
    exact (h1.exp).mul (hasDerivAt_Vr hZ t)
  refine monotone_of_deriv_nonneg (fun t => (hd t).differentiableAt) (fun t => ?_)
  rw [(hd t).deriv]
  have h2 := kappa_ge ha hZ hρ t
  have h3 := (Real.exp_pos (ρ * t)).le
  nlinarith [mul_nonneg h3 (by linarith : 0 ≤ kappa a h t + ρ * Vr a h t)]

/-- **Variance comparison along a line**: `Vr t ≥ e^{−ρ t} Vr 0` for `t ≥ 0`. -/
theorem Vr_ge (ha : ∀ j, 0 ≤ a j) (hZ : ∀ t, 0 < S a h 0 t) {ρ : ℝ}
    (hρ : ∀ i j, h i - h j ≤ ρ) {t : ℝ} (ht : 0 ≤ t) :
    Real.exp (-ρ * t) * Vr a h 0 ≤ Vr a h t := by
  have h1 := monotone_exp_mul_Vr ha hZ hρ ht
  simp only [mul_zero, Real.exp_zero, one_mul] at h1
  have h2 : Real.exp (-ρ * t) * Vr a h 0
      ≤ Real.exp (-ρ * t) * (Real.exp (ρ * t) * Vr a h t) :=
    mul_le_mul_of_nonneg_left h1 (Real.exp_pos _).le
  have e : Real.exp (-ρ * t) * (Real.exp (ρ * t) * Vr a h t) = Vr a h t := by
    rw [← mul_assoc, ← Real.exp_add]
    have e0 : -ρ * t + ρ * t = 0 := by ring
    rw [e0, Real.exp_zero, one_mul]
  linarith

/-- **Integrated curvature** (handoff B1, one sample): the tilted mean increases along `h` by at
least `Var₀(h) · (1 − e^{−ρ})/ρ`. -/
theorem curvature_integrated (ha : ∀ j, 0 ≤ a j) (hZ : ∀ t, 0 < S a h 0 t) {ρ : ℝ}
    (hρ0 : 0 < ρ) (hρ : ∀ i j, h i - h j ≤ ρ) :
    Vr a h 0 * (1 - Real.exp (-ρ)) / ρ ≤ m a h 1 - m a h 0 := by
  -- G t = m t + Vr 0 · e^{-ρ t}/ρ is nondecreasing on [0, ∞)
  have hd : ∀ t, HasDerivAt (fun t => m a h t + Vr a h 0 * Real.exp (-ρ * t) / ρ)
      (Vr a h t + Vr a h 0 * (Real.exp (-ρ * t) * (-ρ)) / ρ) t := by
    intro t
    have h1 : HasDerivAt (fun y : ℝ => -ρ * y) (-ρ) t := by
      simpa using (hasDerivAt_id t).const_mul (-ρ)
    exact (hasDerivAt_m hZ t).add (((h1.exp).const_mul (Vr a h 0)).div_const ρ)
  have hmono : MonotoneOn (fun t => m a h t + Vr a h 0 * Real.exp (-ρ * t) / ρ) (Set.Ici 0) := by
    refine monotoneOn_of_deriv_nonneg (convex_Ici 0)
      (fun t _ => (hd t).continuousAt.continuousWithinAt)
      (fun t _ => (hd t).differentiableAt.differentiableWithinAt) (fun t ht => ?_)
    rw [interior_Ici] at ht
    rw [(hd t).deriv]
    have h2 := Vr_ge ha hZ hρ (le_of_lt ht)
    have e : Vr a h 0 * (Real.exp (-ρ * t) * (-ρ)) / ρ = -(Real.exp (-ρ * t) * Vr a h 0) := by
      field_simp
    rw [e]
    linarith
  have h3 := hmono (Set.mem_Ici.2 le_rfl) (Set.mem_Ici.2 zero_le_one) zero_le_one
  simp only [mul_zero, Real.exp_zero, mul_one] at h3
  have e2 : Vr a h 0 * (1 - Real.exp (-ρ)) / ρ
      = Vr a h 0 / ρ - Vr a h 0 * Real.exp (-ρ) / ρ := by ring
  rw [e2]
  linarith

end Softmax

/-- **Curvature of the multistate objective along a direction** (handoff B1): summing the one-sample
inequality over the samples `n` (weights `a n j = s_j e^{f_j} q_j(x_n)`), the directional change of
the score dominates the Hessian quadratic form times `(1 − e^{−ρ})/ρ`. -/
theorem curvature_sum {ν ι : Type*} [Fintype ν] [Fintype ι] {a : ν → ι → ℝ} {h : ι → ℝ}
    (ha : ∀ n j, 0 ≤ a n j) (hpos : ∀ n, ∃ j, 0 < a n j) {ρ : ℝ} (hρ0 : 0 < ρ)
    (hρ : ∀ i j, h i - h j ≤ ρ) :
    (∑ n, Softmax.Vr (a n) h 0) * (1 - Real.exp (-ρ)) / ρ
      ≤ ∑ n, (Softmax.m (a n) h 1 - Softmax.m (a n) h 0) := by
  rw [Finset.sum_mul, Finset.sum_div]
  exact Finset.sum_le_sum (fun n _ =>
    Softmax.curvature_integrated (ha n) (Softmax.S0_pos (a n) h (ha n) (hpos n)) hρ0 hρ)

/-- Pairing of a zero-sum vector with a function of small oscillation:
`|Σ y_i h_i| ≤ (ρ/2) Σ |y_i|` when `|h_i − c| ≤ ρ/2` for some centre `c`. -/
theorem pairing_le {ι : Type*} [Fintype ι] {y h : ι → ℝ} (hy : ∑ i, y i = 0) {c ρ : ℝ}
    (hc : ∀ i, |h i - c| ≤ ρ / 2) : |∑ i, y i * h i| ≤ ρ / 2 * ∑ i, |y i| := by
  have e : ∑ i, y i * h i = ∑ i, y i * (h i - c) := by
    have : ∑ i, y i * (h i - c) = ∑ i, y i * h i - (∑ i, y i) * c := by
      rw [Finset.sum_mul, ← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl (fun i _ => by ring)
    rw [this, hy]; ring
  rw [e, Finset.mul_sum]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum (fun i _ => ?_))
  rw [abs_mul, mul_comm]
  exact mul_le_mul_of_nonneg_right (hc i) (abs_nonneg _)

/-- **Scalar localisation of handoff C1**: from the resistance bound `ρ² ≤ R·Vh`, the integrated
curvature `Vh (1 − e^{−ρ})/ρ ≤ Δ` and the score bound `Δ ≤ ε ρ`, with `R ε < 1`:
`ρ ≤ −log(1 − R ε)`. -/
theorem cut_localization {ρ R ε Vh Δ : ℝ} (hρ : 0 ≤ ρ) (hR : 0 < R) (hε : 0 ≤ ε)
    (hres : ρ ^ 2 ≤ R * Vh) (hcurv : 0 < ρ → Vh * (1 - Real.exp (-ρ)) / ρ ≤ Δ)
    (hscore : Δ ≤ ε * ρ) (hq : R * ε < 1) : ρ ≤ -Real.log (1 - R * ε) := by
  have h1q : 0 < 1 - R * ε := by linarith
  rcases eq_or_lt_of_le hρ with h0 | hpos
  · rw [← h0]
    have := Real.log_nonpos h1q.le (by linarith [mul_nonneg hR.le hε])
    linarith
  · have h1 := (hcurv hpos).trans hscore
    rw [div_le_iff₀ hpos] at h1
    have hexp : 0 ≤ 1 - Real.exp (-ρ) := by
      have := Real.exp_le_one_iff.2 (by linarith : -ρ ≤ 0)
      linarith
    -- ρ² (1 − e^{−ρ}) ≤ R Vh (1 − e^{−ρ}) ≤ R ε ρ²
    have h2 : ρ ^ 2 * (1 - Real.exp (-ρ)) ≤ R * ε * ρ ^ 2 := by
      have a1 := mul_le_mul_of_nonneg_right hres hexp
      have a2 := mul_le_mul_of_nonneg_left h1 hR.le
      nlinarith [a1, a2]
    have hρ2 : 0 < ρ ^ 2 := pow_pos hpos 2
    have h3 : 1 - Real.exp (-ρ) ≤ R * ε := by
      have a3 : ρ ^ 2 * (1 - Real.exp (-ρ)) ≤ ρ ^ 2 * (R * ε) := by linarith [mul_comm (R * ε) (ρ ^ 2)]
      exact le_of_mul_le_mul_left a3 hρ2
    have h4 : 1 - R * ε ≤ Real.exp (-ρ) := by linarith
    have h5 := (Real.log_le_iff_le_exp h1q).2 h4
    linarith

/-! ### Sound composition of deterministic and statistical error bounds (handoff E3) -/

/-- A uniform envelope `|ũ − u| ≤ ε` on the energies moves the free energy `−log Z` by at most `ε`
(any nonnegative base weights `g`). -/
theorem free_energy_envelope {α : Type*} [Fintype α] {g u u' : α → ℝ} {ε : ℝ}
    (hg : ∀ x, 0 ≤ g x) (hZ : 0 < ∑ x, g x * Real.exp (-u x)) (hu : ∀ x, |u' x - u x| ≤ ε) :
    |(-Real.log (∑ x, g x * Real.exp (-u' x))) - (-Real.log (∑ x, g x * Real.exp (-u x)))|
      ≤ ε := by
  have hup : ∑ x, g x * Real.exp (-u' x) ≤ Real.exp ε * ∑ x, g x * Real.exp (-u x) := by
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum (fun x _ => ?_)
    have h1 : Real.exp (-u' x) ≤ Real.exp ε * Real.exp (-u x) := by
      rw [← Real.exp_add]
      apply Real.exp_le_exp.2
      have := abs_le.1 (hu x)
      linarith
    calc g x * Real.exp (-u' x) ≤ g x * (Real.exp ε * Real.exp (-u x)) :=
          mul_le_mul_of_nonneg_left h1 (hg x)
      _ = Real.exp ε * (g x * Real.exp (-u x)) := by ring
  have hlo : Real.exp (-ε) * ∑ x, g x * Real.exp (-u x) ≤ ∑ x, g x * Real.exp (-u' x) := by
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum (fun x _ => ?_)
    have h1 : Real.exp (-ε) * Real.exp (-u x) ≤ Real.exp (-u' x) := by
      rw [← Real.exp_add]
      apply Real.exp_le_exp.2
      have := abs_le.1 (hu x)
      linarith
    calc Real.exp (-ε) * (g x * Real.exp (-u x)) = g x * (Real.exp (-ε) * Real.exp (-u x)) := by
          ring
      _ ≤ g x * Real.exp (-u' x) := mul_le_mul_of_nonneg_left h1 (hg x)
  have hlow_pos : 0 < Real.exp (-ε) * ∑ x, g x * Real.exp (-u x) := mul_pos (Real.exp_pos _) hZ
  have hZ' : 0 < ∑ x, g x * Real.exp (-u' x) := lt_of_lt_of_le hlow_pos hlo
  have l1 := Real.log_le_log hZ' hup
  rw [Real.log_mul (Real.exp_pos ε).ne' hZ.ne', Real.log_exp] at l1
  have l2 := Real.log_le_log hlow_pos hlo
  rw [Real.log_mul (Real.exp_pos (-ε)).ne' hZ.ne', Real.log_exp] at l2
  rw [abs_le]
  constructor <;> linarith

/-- **Composition**: a statistical radius `r` for a contrast of the approximate system and envelope
radii `ε_k` add up to a radius for the same contrast of the true system. -/
theorem contrast_composition {ι : Type*} [Fintype ι] {c fhat ftil f ε : ι → ℝ} {r : ℝ}
    (hstat : |∑ k, c k * (fhat k - ftil k)| ≤ r) (henv : ∀ k, |ftil k - f k| ≤ ε k) :
    |∑ k, c k * (fhat k - f k)| ≤ r + ∑ k, |c k| * ε k := by
  have e : ∑ k, c k * (fhat k - f k)
      = ∑ k, c k * (fhat k - ftil k) + ∑ k, c k * (ftil k - f k) := by
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl (fun k _ => by ring)
  have h2 : |∑ k, c k * (ftil k - f k)| ≤ ∑ k, |c k| * ε k := by
    refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum (fun k _ => ?_))
    rw [abs_mul]
    exact mul_le_mul_of_nonneg_left (henv k) (abs_nonneg _)
  rw [e]
  exact (abs_add_le _ _).trans (add_le_add hstat h2)

end MBAR
