import Mathlib

/-!
# Lemma A16.5 (isoperimetry with an energy constraint), conditional on Harper's theorem

Science division, workstream L3.  Source: `docs/science/INFERENCE_LIMITS_ADDENDA.md`, addendum
A16, Lemma A16.5.  This file imports **Mathlib only**.

Workstream R8 (the referee of A16) machine-checked the algebraic core of the lemma in
`experiments/science/ws_R8/A16Core.lean`: the Lagrangian inequality, the maximum and the
monotonicity of `f_η`, the monotonicity of `F_η`, the plateau as maximiser for `t* ≥ 1`, and the
assembly `Σ t ≤ Σ F_η(ρ(x))`.  Its report (R8_REPORT §7, T-R8-1) names what is missing for a
full machine check: *the rearrangement step, with Harper's theorem as a hypothesis*.

**Part 0** repeats the declarations of `A16Core.lean` that are needed (verbatim, credited to
workstream R8; the files of `experiments/science/` cannot import each other).
**Part 1 is new:**

* `sum_comp_le_of_card_le` — the rearrangement step: if `H : ℕ → ℝ` is nondecreasing and
  `#{x : ρ x > k} ≤ #{x : ρ' x > k}` for all `k`, then `Σ_x H (ρ x) ≤ Σ_x H (ρ' x)`;
* `lemmaA16_5_of_harper` — **Lemma A16.5 for the multiplier `η > 0`, conditional on Harper's
  inequality between the level-set counts and on the level**: every weight vector within the
  pointwise bounds of a distance profile `ρ` and with `φ(t) ≤ 0` has `Σ t ≤ Σ_x min(t*, e^{uρ'(x)})`,
  the partition sum of the plateau on the comparison profile `ρ'`, provided the plateau has
  `φ ≥ 0` (in the addendum: `= 0`, the level `c*`);
* `tail_of_harper` — the case `η = 0` (the full cone; the tail lemma);
* `lemmaA16_5_of_harper_ge` — the same with Harper's hypothesis in the form
  `#{ρ ≥ k} ≤ #{ρ' ≥ k}` for `k ≥ 1`;
* `f_concaveOn` — `f_η` is concave on `[0, ∞)` for `η ≥ 0`;
* `sum_eq_sum_f_add` — `Σ t = Σ f_η(t) + η·φ(t)`;
* `F_eq_clip` — for **every** level `t* > 0` the maximiser of `f_η` on `[e^{−uρ}, e^{uρ}]` is the
  clipped level `max(e^{−uρ}, min(t*, e^{uρ}))` (a hill when `t* < 1`); `F_zero`: `F_0(ρ) = e^{uρ}`.

**Not proved here:** Harper's theorem itself (it is the hypothesis `hharper`), the existence
and uniqueness of the level `c*`, and that the plateau is a member of the class.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL3

namespace A16

open Finset

/-! ## Part 0: repeated from `experiments/science/ws_R8/A16Core.lean` (workstream R8) -/

/-- the Lagrangian integrand of Lemma A16.5 -/
def f (η U₀ t : ℝ) : ℝ := (1 - η * U₀) * t - η * (t * Real.log t)

/-- its supremum over the interval allowed at distance `ρ` from the complement of the support -/
def F (η U₀ u ρ : ℝ) : ℝ :=
  sSup (f η U₀ '' Set.Icc (Real.exp (-(u * ρ))) (Real.exp (u * ρ)))

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

/-! ## Part 1 (new): the rearrangement step and the lemma conditional on Harper's theorem -/

/-- **(a) of the brief, as an identity:** `Σ t = Σ f_η(t) + η·φ(t)`,
`φ(t) = Σ t ln t + U₀ Σ t`. -/
theorem sum_eq_sum_f_add {ι : Type*} (s : Finset ι) (t : ι → ℝ) (η U₀ : ℝ) :
    ∑ i ∈ s, t i =
      ∑ i ∈ s, f η U₀ (t i) + η * (∑ i ∈ s, t i * Real.log (t i) + U₀ * ∑ i ∈ s, t i) := by
  rw [sum_f_eq]
  ring

/-- **(b) of the brief:** `f_η` is concave on `[0, ∞)` for `η ≥ 0` (a linear function minus
`η` times the convex function `t ln t`). -/
theorem f_concaveOn {η : ℝ} (hη : 0 ≤ η) (U₀ : ℝ) : ConcaveOn ℝ (Set.Ici 0) (f η U₀) := by
  refine ⟨convex_Ici 0, fun x hx y hy a b ha hb hab => ?_⟩
  have h := Real.convexOn_mul_log.2 hx hy ha hb hab
  simp only [smul_eq_mul] at h ⊢
  unfold f
  nlinarith [mul_le_mul_of_nonneg_left h hη]

/-- **(c) of the brief, for every level:** for every `t* > 0` (with `ln t* = 1/η − 1 − U₀`,
`η > 0`) the maximiser of `f_η` on `[e^{−uρ}, e^{uρ}]` is the level clipped to the interval,
`max(e^{−uρ}, min(t*, e^{uρ}))` — the plateau `min(t*, e^{uρ})` when `t* ≥ 1`, a hill
`max(t*, e^{−uρ})` when `t* < 1`. -/
theorem F_eq_clip (η U₀ u ρ ts : ℝ) (hη : 0 < η) (hu : 0 ≤ u) (hρ : 0 ≤ ρ) (hts : 0 < ts)
    (hstar : Real.log ts = 1 / η - 1 - U₀) :
    F η U₀ u ρ = f η U₀ (max (Real.exp (-(u * ρ))) (min ts (Real.exp (u * ρ)))) := by
  unfold F
  have huρ : 0 ≤ u * ρ := mul_nonneg hu hρ
  have hlohi : Real.exp (-(u * ρ)) ≤ Real.exp (u * ρ) := Real.exp_le_exp.mpr (by linarith)
  apply IsGreatest.csSup_eq
  constructor
  · exact ⟨_, ⟨le_max_left _ _, max_le hlohi (min_le_right _ _)⟩, rfl⟩
  · rintro _ ⟨t, ⟨hta, htb⟩, rfl⟩
    have ht : 0 < t := lt_of_lt_of_le (Real.exp_pos _) hta
    rcases le_total ts (Real.exp (-(u * ρ))) with h | h
    · -- the level is below the interval: the maximiser is the lower end
      rw [min_eq_left (h.trans hlohi), max_eq_left h]
      exact f_anti_above η U₀ _ t ts hη hts h hta hstar
    · rcases le_total ts (Real.exp (u * ρ)) with h' | h'
      · rw [min_eq_left h', max_eq_right h, f_at_max η U₀ ts hη hstar]
        exact f_le_max η U₀ t ts hη ht hts hstar
      · rw [min_eq_right h', max_eq_right hlohi]
        exact f_mono_below η U₀ t _ ts hη ht htb h' hstar

/-- For `η = 0` (no constraint): `F_0(ρ) = e^{uρ}`, the full cone. -/
theorem F_zero (U₀ u ρ : ℝ) (hu : 0 ≤ u) (hρ : 0 ≤ ρ) : F 0 U₀ u ρ = Real.exp (u * ρ) := by
  unfold F
  have hf : f 0 U₀ = id := by
    funext t
    unfold f
    simp
  have hlohi : Real.exp (-(u * ρ)) ≤ Real.exp (u * ρ) :=
    Real.exp_le_exp.mpr (by nlinarith [mul_nonneg hu hρ])
  rw [hf, Set.image_id, csSup_Icc hlohi]

/-- **The rearrangement step (Harper's theorem enters as the hypothesis `hcard`).**  If
`H : ℕ → ℝ` is nondecreasing and the level sets of `ρ` are no larger than those of `ρ'`,
`#{x : ρ x > k} ≤ #{x : ρ' x > k}` for every `k`, then `Σ_x H (ρ x) ≤ Σ_x H (ρ' x)`. -/
theorem sum_comp_le_of_card_le {X : Type*} [Fintype X] {H : ℕ → ℝ} (hH : Monotone H)
    (ρ ρ' : X → ℕ)
    (hcard : ∀ k : ℕ, (univ.filter fun x => k < ρ x).card ≤ (univ.filter fun x => k < ρ' x).card) :
    ∑ x, H (ρ x) ≤ ∑ x, H (ρ' x) := by
  obtain ⟨K, hK⟩ : ∃ K : ℕ, ∀ x, ρ x ≤ K ∧ ρ' x ≤ K :=
    ⟨univ.sup ρ ⊔ univ.sup ρ', fun x =>
      ⟨(Finset.le_sup (f := ρ) (Finset.mem_univ x)).trans le_sup_left,
        (Finset.le_sup (f := ρ') (Finset.mem_univ x)).trans le_sup_right⟩⟩
  have key : ∀ σ : X → ℕ, (∀ x, σ x ≤ K) →
      ∑ x, H (σ x) = (Fintype.card X : ℝ) * H 0 +
        ∑ k ∈ Finset.range K, (H (k + 1) - H k) * ((univ.filter fun x => k < σ x).card : ℝ) := by
    intro σ hσ
    have h1 : ∀ x, H (σ x) =
        H 0 + ∑ k ∈ Finset.range K, if k < σ x then (H (k + 1) - H k) else 0 := by
      intro x
      have hfil : (Finset.range K).filter (fun k => k < σ x) = Finset.range (σ x) := by
        ext k
        simp only [Finset.mem_filter, Finset.mem_range]
        exact ⟨fun h => h.2, fun h => ⟨lt_of_lt_of_le h (hσ x), h⟩⟩
      rw [← Finset.sum_filter, hfil, Finset.sum_range_sub]
      ring
    rw [Finset.sum_congr rfl fun x _ => h1 x, Finset.sum_add_distrib, Finset.sum_const,
      Finset.card_univ, nsmul_eq_mul, Finset.sum_comm]
    congr 1
    refine Finset.sum_congr rfl fun k _ => ?_
    rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, mul_comm]
  rw [key ρ fun x => (hK x).1, key ρ' fun x => (hK x).2]
  have hsum : ∑ k ∈ Finset.range K,
        (H (k + 1) - H k) * ((univ.filter fun x => k < ρ x).card : ℝ) ≤
      ∑ k ∈ Finset.range K,
        (H (k + 1) - H k) * ((univ.filter fun x => k < ρ' x).card : ℝ) := by
    refine Finset.sum_le_sum fun k _ => ?_
    refine mul_le_mul_of_nonneg_left ?_ (sub_nonneg.mpr (hH (Nat.le_succ k)))
    exact_mod_cast hcard k
  linarith

/-- **Lemma A16.5 for the multiplier `η > 0`, conditional on Harper's theorem and on the
level.**  `X` a finite set (the cube); `t : X → ℝ` the weights `e^{−g}` of a member; `ρ x ∈ ℕ` the
distance from `x` to the complement of its support, so that `e^{−uρ(x)} ≤ t(x) ≤ e^{uρ(x)}`;
energy constraint `φ(t) = Σ t ln t + U₀ Σ t ≤ 0` (mean energy `≥ U₀`); `ρ'` the distance profile
of the comparison set (the ball), with **Harper's inequality `#{ρ > k} ≤ #{ρ' > k}` for all `k`
as a hypothesis**; a level `t* ≥ 1` with `ln t* = 1/η − 1 − U₀` at which the plateau
`t_pl(x) = min(t*, e^{uρ'(x)})` has `φ(t_pl) ≥ 0` (in the addendum `= 0`: the level `c* = ln t*`
with `U_{g_pl} = U₀`).  Then `Z_g = Σ t ≤ Σ t_pl = Z^{pl}`. -/
theorem lemmaA16_5_of_harper {X : Type*} [Fintype X] (t : X → ℝ) (ρ ρ' : X → ℕ)
    (η U₀ u ts : ℝ) (hη : 0 < η) (hu : 0 ≤ u) (h1 : 1 ≤ ts)
    (hstar : Real.log ts = 1 / η - 1 - U₀)
    (hφ : ∑ x, t x * Real.log (t x) + U₀ * ∑ x, t x ≤ 0)
    (hmem : ∀ x, t x ∈ Set.Icc (Real.exp (-(u * (ρ x : ℝ)))) (Real.exp (u * (ρ x : ℝ))))
    (hharper : ∀ k : ℕ,
      (univ.filter fun x => k < ρ x).card ≤ (univ.filter fun x => k < ρ' x).card)
    (hpl : 0 ≤ ∑ x, min ts (Real.exp (u * (ρ' x : ℝ))) *
        Real.log (min ts (Real.exp (u * (ρ' x : ℝ)))) +
      U₀ * ∑ x, min ts (Real.exp (u * (ρ' x : ℝ)))) :
    ∑ x, t x ≤ ∑ x, min ts (Real.exp (u * (ρ' x : ℝ))) := by
  have h2 := sum_le_sum_F univ t (fun x => (ρ x : ℝ)) η U₀ u hη.le hφ fun x _ => hmem x
  have hmono : Monotone fun k : ℕ => F η U₀ u (k : ℝ) := fun a b hab =>
    F_mono η U₀ u hu (Nat.cast_nonneg a) (Nat.cast_le.mpr hab)
  have h3 := sum_comp_le_of_card_le hmono ρ ρ' hharper
  have h4 : ∑ x, F η U₀ u (ρ' x : ℝ) = ∑ x, f η U₀ (min ts (Real.exp (u * (ρ' x : ℝ)))) :=
    Finset.sum_congr rfl fun x _ =>
      F_eq_plateau η U₀ u (ρ' x : ℝ) ts hη hu (Nat.cast_nonneg _) h1 hstar
  have h5 := sum_f_eq univ (fun x => min ts (Real.exp (u * (ρ' x : ℝ)))) η U₀
  have h6 := mul_nonneg hη.le hpl
  linarith

/-- **Lemma A16.5 for `η = 0` (the full cone is feasible; the tail lemma), conditional on
Harper's theorem**: weights with `t(x) ≤ e^{uρ(x)}` have `Σ t ≤ Σ_x e^{uρ'(x)}`. -/
theorem tail_of_harper {X : Type*} [Fintype X] (t : X → ℝ) (ρ ρ' : X → ℕ) (u : ℝ)
    (hu : 0 ≤ u) (hmem : ∀ x, t x ≤ Real.exp (u * (ρ x : ℝ)))
    (hharper : ∀ k : ℕ,
      (univ.filter fun x => k < ρ x).card ≤ (univ.filter fun x => k < ρ' x).card) :
    ∑ x, t x ≤ ∑ x, Real.exp (u * (ρ' x : ℝ)) := by
  have hmono : Monotone fun k : ℕ => Real.exp (u * (k : ℝ)) := fun a b hab =>
    Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left (Nat.cast_le.mpr hab) hu)
  exact (Finset.sum_le_sum fun x _ => hmem x).trans
    (sum_comp_le_of_card_le hmono ρ ρ' hharper)

/-- `#{x : ρ x ≥ k} ≤ #{x : ρ' x ≥ k}` for all `k ≥ 1` is the hypothesis `hharper` above. -/
theorem harper_gt_of_ge {X : Type*} [Fintype X] (ρ ρ' : X → ℕ)
    (h : ∀ k : ℕ, 1 ≤ k →
      (univ.filter fun x => k ≤ ρ x).card ≤ (univ.filter fun x => k ≤ ρ' x).card) (k : ℕ) :
    (univ.filter fun x => k < ρ x).card ≤ (univ.filter fun x => k < ρ' x).card :=
  h (k + 1) (Nat.succ_le_succ (Nat.zero_le k))

/-- Lemma A16.5 conditional on Harper's theorem in the form of the addendum,
`#{x : ρ(x) ≥ k} ≤ #{x : ρ*(x) ≥ k}` for every `k ≥ 1`. -/
theorem lemmaA16_5_of_harper_ge {X : Type*} [Fintype X] (t : X → ℝ) (ρ ρ' : X → ℕ)
    (η U₀ u ts : ℝ) (hη : 0 < η) (hu : 0 ≤ u) (h1 : 1 ≤ ts)
    (hstar : Real.log ts = 1 / η - 1 - U₀)
    (hφ : ∑ x, t x * Real.log (t x) + U₀ * ∑ x, t x ≤ 0)
    (hmem : ∀ x, t x ∈ Set.Icc (Real.exp (-(u * (ρ x : ℝ)))) (Real.exp (u * (ρ x : ℝ))))
    (hharper : ∀ k : ℕ, 1 ≤ k →
      (univ.filter fun x => k ≤ ρ x).card ≤ (univ.filter fun x => k ≤ ρ' x).card)
    (hpl : 0 ≤ ∑ x, min ts (Real.exp (u * (ρ' x : ℝ))) *
        Real.log (min ts (Real.exp (u * (ρ' x : ℝ)))) +
      U₀ * ∑ x, min ts (Real.exp (u * (ρ' x : ℝ)))) :
    ∑ x, t x ≤ ∑ x, min ts (Real.exp (u * (ρ' x : ℝ))) :=
  lemmaA16_5_of_harper t ρ ρ' η U₀ u ts hη hu h1 hstar hφ hmem
    (harper_gt_of_ge ρ ρ' hharper) hpl

end A16

end ScienceL3

/-! ## Axioms -/

#print axioms ScienceL3.A16.sum_eq_sum_f_add
#print axioms ScienceL3.A16.f_concaveOn
#print axioms ScienceL3.A16.F_eq_clip
#print axioms ScienceL3.A16.F_zero
#print axioms ScienceL3.A16.sum_comp_le_of_card_le
#print axioms ScienceL3.A16.lemmaA16_5_of_harper
#print axioms ScienceL3.A16.tail_of_harper
#print axioms ScienceL3.A16.lemmaA16_5_of_harper_ge
