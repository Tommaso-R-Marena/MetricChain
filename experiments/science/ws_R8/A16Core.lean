import Mathlib

/-!
# The algebraic core of Lemma A16.5 (isoperimetry with an energy constraint)

Science division, workstream R8 (adversarial referee of addendum A16 of
`docs/science/INFERENCE_LIMITS_ADDENDA.md`).  Optional machine check; the mathematics and the
numerics are in `docs/science/workstreams/R8_REPORT.md`.

Units `β = 1`.  A member `g` of the class is described by its weights `t = e^{-g}`; `U₀` is the
bound on the mean energy, `η ≥ 0` the multiplier, and

  `f η U₀ t = (1 - η U₀) t - η t ln t`,     `F η U₀ u ρ = sup { f η U₀ t : e^{-uρ} ≤ t ≤ e^{uρ} }`.

## What is proved here

* `constraint_iff`    : `U₀ ≤ (Σ t (-ln t)) / Σ t  ↔  Σ t ln t + U₀ Σ t ≤ 0`
                        (the constraint "mean energy `≥ U₀`" in the weights);
* `sum_le_sum_f`      : under the constraint, `Σ t ≤ Σ f η U₀ t` for every `η ≥ 0`
                        (the direction of the Lagrangian inequality);
* `f_le_max`, `f_at_max` : `f η U₀ t ≤ η t* = f η U₀ t*` for `ln t* = 1/η - 1 - U₀`;
* `f_mono_below`, `f_anti_above` : `f η U₀` is nondecreasing on `(0, t*]`, nonincreasing on `[t*, ∞)`;
* `F_mono`            : `F η U₀ u ρ` is nondecreasing in `ρ ≥ 0` (a supremum over a growing interval);
* `F_eq_plateau`      : if `t* ≥ 1`, the supremum is attained at the clipped level `min t* e^{uρ}`;
* `sum_le_sum_F`      : `Σ t ≤ Σ F η U₀ u (ρ i)` whenever `e^{-uρ i} ≤ t i ≤ e^{uρ i}` and the
                        constraint holds;
* `plateau_optimal`   : for a fixed profile `ρ`, if the plateau `min t* e^{uρ}` meets the constraint
                        with equality, every admissible `t` has `Σ t ≤ Σ min t* e^{uρ i}`.

## What is NOT proved here

The isoperimetric step (Harper's theorem: `#{ρ ≥ k}` is largest, for all `k` at once, for the
ball), i.e. the comparison of `Σ F(ρ(x))` between different supports; the existence and the
uniqueness of the level; that the plateau is a member of the class.
-/

open Finset

namespace R8

/-- the Lagrangian integrand of Lemma A16.5 -/
noncomputable def f (η U₀ t : ℝ) : ℝ := (1 - η * U₀) * t - η * (t * Real.log t)

/-- its supremum over the interval allowed at distance `ρ` from the complement of the support -/
noncomputable def F (η U₀ u ρ : ℝ) : ℝ :=
  sSup (f η U₀ '' Set.Icc (Real.exp (-(u * ρ))) (Real.exp (u * ρ)))

/-- "mean energy at least `U₀`" written in the weights -/
theorem constraint_iff {ι : Type*} (s : Finset ι) (t : ι → ℝ) (U₀ : ℝ)
    (hZ : 0 < ∑ i ∈ s, t i) :
    U₀ ≤ (∑ i ∈ s, t i * (-Real.log (t i))) / (∑ i ∈ s, t i) ↔
      ∑ i ∈ s, t i * Real.log (t i) + U₀ * ∑ i ∈ s, t i ≤ 0 := by
  rw [le_div_iff₀ hZ]
  simp only [mul_neg, Finset.sum_neg_distrib]
  constructor <;> intro h <;> linarith

theorem sum_f_eq {ι : Type*} (s : Finset ι) (t : ι → ℝ) (η U₀ : ℝ) :
    ∑ i ∈ s, f η U₀ (t i) =
      ∑ i ∈ s, t i - η * (∑ i ∈ s, t i * Real.log (t i) + U₀ * ∑ i ∈ s, t i) := by
  simp only [f, Finset.sum_sub_distrib, ← Finset.mul_sum]
  ring

/-- the direction of the Lagrangian inequality: the constraint is `φ ≤ 0` and `η ≥ 0` -/
theorem sum_le_sum_f {ι : Type*} (s : Finset ι) (t : ι → ℝ) (η U₀ : ℝ) (hη : 0 ≤ η)
    (hφ : ∑ i ∈ s, t i * Real.log (t i) + U₀ * ∑ i ∈ s, t i ≤ 0) :
    ∑ i ∈ s, t i ≤ ∑ i ∈ s, f η U₀ (t i) := by
  rw [sum_f_eq]
  nlinarith [mul_nonneg hη (neg_nonneg.mpr hφ)]

theorem f_eq (η U₀ ts : ℝ) (hη : 0 < η) (hstar : Real.log ts = 1 / η - 1 - U₀) (x : ℝ) :
    f η U₀ x = η * (x * (1 + Real.log ts - Real.log x)) := by
  unfold f
  rw [hstar]
  field_simp
  ring

theorem f_at_max (η U₀ ts : ℝ) (hη : 0 < η) (hstar : Real.log ts = 1 / η - 1 - U₀) :
    f η U₀ ts = η * ts := by
  rw [f_eq η U₀ ts hη hstar]
  ring

/-- the tangent-line inequality `t (ln b - ln t) ≤ b - t` -/
theorem tangent (t b : ℝ) (ht : 0 < t) (hb : 0 < b) :
    t * (Real.log b - Real.log t) ≤ b - t := by
  have h1 : Real.log (b / t) ≤ b / t - 1 := Real.log_le_sub_one_of_pos (div_pos hb ht)
  rw [Real.log_div hb.ne' ht.ne'] at h1
  have h2 := mul_le_mul_of_nonneg_left h1 ht.le
  have h4 : t * (b / t - 1) = b - t := by field_simp
  linarith

/-- `t*` maximises `f` -/
theorem f_le_max (η U₀ t ts : ℝ) (hη : 0 < η) (ht : 0 < t) (hts : 0 < ts)
    (hstar : Real.log ts = 1 / η - 1 - U₀) : f η U₀ t ≤ η * ts := by
  rw [f_eq η U₀ ts hη hstar]
  apply mul_le_mul_of_nonneg_left _ hη.le
  have := tangent t ts ht hts
  nlinarith

/-- `f` is nondecreasing below `t*` -/
theorem f_mono_below (η U₀ t b ts : ℝ) (hη : 0 < η) (ht : 0 < t) (htb : t ≤ b) (hbs : b ≤ ts)
    (hstar : Real.log ts = 1 / η - 1 - U₀) : f η U₀ t ≤ f η U₀ b := by
  have hb : 0 < b := lt_of_lt_of_le ht htb
  have h2 := tangent t b ht hb
  have h3 : Real.log b ≤ Real.log ts := Real.log_le_log hb hbs
  rw [f_eq η U₀ ts hη hstar t, f_eq η U₀ ts hη hstar b]
  apply mul_le_mul_of_nonneg_left _ hη.le
  nlinarith [mul_nonneg (sub_nonneg.mpr htb) (sub_nonneg.mpr h3)]

/-- `f` is nonincreasing above `t*` -/
theorem f_anti_above (η U₀ a t ts : ℝ) (hη : 0 < η) (hts : 0 < ts) (hsa : ts ≤ a) (hat : a ≤ t)
    (hstar : Real.log ts = 1 / η - 1 - U₀) : f η U₀ t ≤ f η U₀ a := by
  have ha : 0 < a := lt_of_lt_of_le hts hsa
  have ht : 0 < t := lt_of_lt_of_le ha hat
  have h2 := tangent t a ht ha
  have h3 : Real.log ts ≤ Real.log a := Real.log_le_log hts hsa
  rw [f_eq η U₀ ts hη hstar t, f_eq η U₀ ts hη hstar a]
  apply mul_le_mul_of_nonneg_left _ hη.le
  nlinarith [mul_nonneg (sub_nonneg.mpr hat) (sub_nonneg.mpr h3)]

theorem f_continuous (η U₀ : ℝ) : Continuous (f η U₀) := by
  unfold f
  exact (continuous_const.mul continuous_id).sub (continuous_const.mul Real.continuous_mul_log)

theorem F_bddAbove (η U₀ u ρ : ℝ) :
    BddAbove (f η U₀ '' Set.Icc (Real.exp (-(u * ρ))) (Real.exp (u * ρ))) :=
  (isCompact_Icc.image (f_continuous η U₀)).bddAbove

/-- `F` is nondecreasing in the distance: a supremum over a growing interval -/
theorem F_mono (η U₀ u : ℝ) (hu : 0 ≤ u) {ρ ρ' : ℝ} (hρ : 0 ≤ ρ) (h : ρ ≤ ρ') :
    F η U₀ u ρ ≤ F η U₀ u ρ' := by
  unfold F
  have hle : u * ρ ≤ u * ρ' := mul_le_mul_of_nonneg_left h hu
  apply csSup_le_csSup (F_bddAbove η U₀ u ρ')
  · refine (Set.nonempty_Icc.mpr (Real.exp_le_exp.mpr ?_)).image _
    nlinarith [mul_nonneg hu hρ]
  · apply Set.image_mono
    apply Set.Icc_subset_Icc
    · exact Real.exp_le_exp.mpr (by linarith)
    · exact Real.exp_le_exp.mpr hle

/-- for a level `t* ≥ 1` the supremum is attained at the clipped level -/
theorem F_eq_plateau (η U₀ u ρ ts : ℝ) (hη : 0 < η) (hu : 0 ≤ u) (hρ : 0 ≤ ρ) (h1 : 1 ≤ ts)
    (hstar : Real.log ts = 1 / η - 1 - U₀) :
    F η U₀ u ρ = f η U₀ (min ts (Real.exp (u * ρ))) := by
  unfold F
  have huρ : 0 ≤ u * ρ := mul_nonneg hu hρ
  have hts : 0 < ts := lt_of_lt_of_le one_pos h1
  apply IsGreatest.csSup_eq
  constructor
  · refine ⟨min ts (Real.exp (u * ρ)), ⟨?_, min_le_right _ _⟩, rfl⟩
    have hlow : Real.exp (-(u * ρ)) ≤ 1 := by
      rw [← Real.exp_zero]
      exact Real.exp_le_exp.mpr (by linarith)
    exact le_min (hlow.trans h1) (hlow.trans (Real.one_le_exp huρ))
  · rintro _ ⟨t, ⟨hta, htb⟩, rfl⟩
    have ht : 0 < t := lt_of_lt_of_le (Real.exp_pos _) hta
    rcases le_total ts (Real.exp (u * ρ)) with h | h
    · rw [min_eq_left h, f_at_max η U₀ ts hη hstar]
      exact f_le_max η U₀ t ts hη ht hts hstar
    · rw [min_eq_right h]
      exact f_mono_below η U₀ t _ ts hη ht htb h hstar

/-- weak duality with the pointwise bounds: `Z ≤ Σ_x F(ρ(x))` -/
theorem sum_le_sum_F {ι : Type*} (s : Finset ι) (t ρ : ι → ℝ) (η U₀ u : ℝ) (hη : 0 ≤ η)
    (hφ : ∑ i ∈ s, t i * Real.log (t i) + U₀ * ∑ i ∈ s, t i ≤ 0)
    (hmem : ∀ i ∈ s, t i ∈ Set.Icc (Real.exp (-(u * ρ i))) (Real.exp (u * ρ i))) :
    ∑ i ∈ s, t i ≤ ∑ i ∈ s, F η U₀ u (ρ i) := by
  refine (sum_le_sum_f s t η U₀ hη hφ).trans (Finset.sum_le_sum fun i hi => ?_)
  unfold F
  exact le_csSup (F_bddAbove η U₀ u (ρ i)) (Set.mem_image_of_mem _ (hmem i hi))

/-- For a fixed distance profile `ρ`: if the plateau at the level `t* ≥ 1` meets the energy
constraint with equality, it has the largest `Z` among all weight vectors that satisfy the
pointwise bounds and the constraint.  (Strong duality at the plateau; no Lipschitz condition on
`t` is needed.) -/
theorem plateau_optimal {ι : Type*} (s : Finset ι) (t ρ : ι → ℝ) (η U₀ u ts : ℝ)
    (hη : 0 < η) (hu : 0 ≤ u) (hρ : ∀ i ∈ s, 0 ≤ ρ i) (h1 : 1 ≤ ts)
    (hstar : Real.log ts = 1 / η - 1 - U₀)
    (hφ : ∑ i ∈ s, t i * Real.log (t i) + U₀ * ∑ i ∈ s, t i ≤ 0)
    (hmem : ∀ i ∈ s, t i ∈ Set.Icc (Real.exp (-(u * ρ i))) (Real.exp (u * ρ i)))
    (hpl : ∑ i ∈ s, min ts (Real.exp (u * ρ i)) * Real.log (min ts (Real.exp (u * ρ i)))
        + U₀ * ∑ i ∈ s, min ts (Real.exp (u * ρ i)) = 0) :
    ∑ i ∈ s, t i ≤ ∑ i ∈ s, min ts (Real.exp (u * ρ i)) := by
  have h := sum_le_sum_F s t ρ η U₀ u hη.le hφ hmem
  have e : ∑ i ∈ s, F η U₀ u (ρ i) = ∑ i ∈ s, f η U₀ (min ts (Real.exp (u * ρ i))) :=
    Finset.sum_congr rfl fun i hi => F_eq_plateau η U₀ u (ρ i) ts hη hu (hρ i hi) h1 hstar
  rw [e, sum_f_eq, hpl] at h
  simpa using h

end R8

#print axioms R8.constraint_iff
#print axioms R8.sum_le_sum_f
#print axioms R8.F_mono
#print axioms R8.F_eq_plateau
#print axioms R8.sum_le_sum_F
#print axioms R8.plateau_optimal
