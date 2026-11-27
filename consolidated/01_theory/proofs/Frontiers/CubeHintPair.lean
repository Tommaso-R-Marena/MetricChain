import Mathlib
import proofs.Frontiers.HintRecursion

/-!
# The exponent functions of the Hamming cube satisfy `HintPair`

Theory report §11.18, Theorem 11.53.  `HintRecursion.lean` analyses the level recursion for an
abstract pair of functions `θna`, `θh` with the properties collected in `HintPair`, and proves
`superSolution_le_hint` and `iterates_lt_hint_add` for such a pair.  This file proves that the
exponent functions of the cube are such a pair.  For a slope `u > 0`, writing
`KL(ρ ‖ q) = klBin ρ q`:

* `cubeP u = 1/(1 + e^u)` (`p_u`), `cubeLam u = log (2/(1 + e^{-u}))` (`Λ₁`),
  `cubeEstar u = KL(1/2 ‖ p_u)` (`ε*`), `cubeA u = KL(p_u ‖ 1/2)` (`a`),
  `cubeH u = KL(Λ₁/u ‖ 1/2)` (`h`); by `cubeEstar_eq`, `cubeEstar_eq_log_cosh` and `cubeA_eq`,
  `ε* = u/2 - Λ₁ = log cosh (u/2)` and `a = Λ₁ - u p_u`;
* `cubeHint u e = KL((Λ₁ + e)/u ‖ 1/2)`, the hinted exponent `θ_hint`;
* `cubeNa u x = KL(cubeRadius u x ‖ 1/2)`, the exponent `θ_na` of non-adaptive sampling, where
  `cubeRadius u x` is the largest `ρ ∈ [p_u, 1/2]` with `KL(ρ ‖ p_u) ≤ x`.  `cubeNa_isLeast`: for
  `x ≥ 0` it is the least element of `{KL(ρ ‖ 1/2) : p_u ≤ ρ ≤ 1/2, KL(ρ ‖ p_u) ≤ x}`, and
  (`cubeNa_isLeast_allRadii`) also of `{KL(ρ ‖ 1/2) : 0 ≤ ρ ≤ 1, KL(ρ ‖ p_u) ≤ x}`, which is the
  definition of the theory report (Theorem 11.44).  `klBin_cubeRadius`: for `0 ≤ x ≤ ε*` the
  radius is the root of `KL(ρ ‖ p_u) = x`; `cubeNa_of_cubeEstar_le`: `θ_na = 0` from `ε*` on;
* `cubePair`: `HintPair (cubeNa u) (cubeHint u) (cubeA u) (cubeH u) (cubeEstar u)`;
* `cube_superSolution_le_hint`, `cube_iterates_lt_hint_add`: the two theorems of
  `HintRecursion.lean` for the cube; `cube_zero_superSolution`, `cubeNa_antitoneOn`,
  `cubeNa_le_cubeA`, `cubeNa_nonneg`: their hypotheses are consistent, and `θ_na` itself is
  nonincreasing, bounded and nonnegative;
* `cubeHint_lt_cubeNa`: `θ_hint < θ_na` on `[0, ε*)`;
* `cubeHintClip`, `cubePairClip`, `cube_step_from_hint_le`, `cube_hint_superSolution`: the
  hinted exponent is a fixed point of the recursion (Theorem 11.53(b)).  `step_from_hint_le` asks
  for a hinted exponent that is nonincreasing on all of `(0, ∞)`, which `cubeHint u` is only up to
  `ε*`; continued by zero from `ε*` on (`cubeHintClip`) it is, the pair is still a `HintPair`, one
  step of the recursion from it stays below `θ_hint` ("`≤`"), and no step goes below it ("`≥`":
  the convexity argument of the theory report, the analogue of `gauss_hint_superSolution`).
  `cube_hintRecursion_witness`: hence the hypotheses of the two theorems are satisfied by a
  positive function, and the bound `T ≤ θ_hint` is attained.

The proof is calculus.  `KL(· ‖ 1/2) = log 2 - binEntropy` is continuous, and strictly decreasing
on `[0, 1/2]`.  By `klBin_shift`, `KL(ρ ‖ p_u) = KL(ρ ‖ 1/2) + u ρ - Λ₁` on `(0, 1)`; the derivative
`log (ρ/(1 - ρ)) + u` of the right-hand side is positive for `p_u < ρ < 1`, so the accuracy
`KL(· ‖ p_u)` is strictly increasing on `[p_u, 1)`, from `0` at `p_u` to `ε*` at `1/2`.  The largest
feasible radius is therefore the generalised inverse of the accuracy: it is continuous at every
`x > 0` (`sSup_sublevel_continuousAt`, which uses only that the accuracy is strictly increasing)
and it returns `ρ` at the accuracy of `ρ` (`sSup_sublevel_apply`).  At the radius
`(Λ₁ + e)/u ∈ (p_u, 1/2]` of the hinted exponent the accuracy is `e + θ_hint(e)`
(`klBin_cubeHintRadius`); this gives the identity `θ_na(e + θ_hint(e)) = θ_hint(e)`, the
monotonicity of `e + θ_hint(e)`, and `θ_hint(e) ≥ h - e`.

**Not formalised here:** anything about algorithms — that `cubeNa` and `cubeHint` are the
exponents of non-adaptive sampling and of sampling with a hint are paper theorems of the theory
report (11.44–11.45 and 11.25) — and the two-level bound `R[T]` as a function: as in
`HintRecursion.lean`, statements about it are expressed through `StepLE`, and the sequence
`T₁ = θ_na`, `T_{k+1} = min(T_k, R[T_k])` of Theorem 11.53(d) is not defined.
-/

namespace MetricChain
namespace HintRecursion

open Set

/-! ### Relative entropy with respect to the uniform two-point distribution -/

/-- `KL(ρ ‖ 1/2) = log 2 - H(ρ)` for every real `ρ`, with `H` the binary entropy of Mathlib. -/
theorem klBin_half_eq (ρ : ℝ) : klBin ρ (1 / 2) = Real.log 2 - Real.binEntropy ρ := by
  unfold klBin Real.binEntropy
  have h2 : (1 : ℝ) - 1 / 2 = 1 / 2 := by norm_num
  have hl : Real.log (1 / 2) = -Real.log 2 := by rw [one_div, Real.log_inv]
  rw [h2]
  rcases eq_or_ne ρ 0 with rfl | h0
  · simp
  rcases eq_or_ne ρ 1 with rfl | h1
  · simp
  have h1' : 1 - ρ ≠ 0 := sub_ne_zero.mpr (Ne.symm h1)
  rw [Real.log_div h0 (by norm_num), Real.log_div h1' (by norm_num), Real.log_inv, Real.log_inv, hl]
  ring

theorem klBin_half_continuous : Continuous fun ρ : ℝ => klBin ρ (1 / 2) := by
  have h : (fun ρ : ℝ => klBin ρ (1 / 2)) = fun ρ => Real.log 2 - Real.binEntropy ρ :=
    funext klBin_half_eq
  rw [h]
  exact continuous_const.sub Real.binEntropy_continuous

theorem klBin_half_half : klBin (1 / 2) (1 / 2) = 0 := by
  rw [klBin_half_eq, one_div, Real.binEntropy_two_inv, sub_self]

theorem klBin_half_nonneg (ρ : ℝ) : 0 ≤ klBin ρ (1 / 2) := by
  rw [klBin_half_eq]
  linarith [Real.binEntropy_le_log_two (p := ρ)]

/-- `KL(· ‖ 1/2)` is strictly decreasing on `[0, 1/2]`. -/
theorem klBin_half_strictAntiOn : StrictAntiOn (fun ρ : ℝ => klBin ρ (1 / 2)) (Icc 0 (1 / 2)) := by
  have h2 : (2 : ℝ)⁻¹ = 1 / 2 := by norm_num
  have hm := Real.binEntropy_strictMonoOn
  rw [h2] at hm
  intro x hx y hy hxy
  have := hm hx hy hxy
  simp only [klBin_half_eq]
  linarith

theorem klBin_half_pos {ρ : ℝ} (h0 : 0 ≤ ρ) (h1 : ρ < 1 / 2) : 0 < klBin ρ (1 / 2) := by
  have h : klBin (1 / 2) (1 / 2) < klBin ρ (1 / 2) :=
    klBin_half_strictAntiOn ⟨h0, h1.le⟩ ⟨by norm_num, le_rfl⟩ h1
  rwa [klBin_half_half] at h

theorem klBin_self (ρ : ℝ) : klBin ρ ρ = 0 := by
  unfold klBin
  rcases eq_or_ne ρ 0 with rfl | h0
  · simp
  rcases eq_or_ne ρ 1 with rfl | h1
  · simp
  have h1' : 1 - ρ ≠ 0 := sub_ne_zero.mpr (Ne.symm h1)
  rw [div_self h0, div_self h1', Real.log_one, mul_zero, mul_zero, add_zero]

/-- `ρ ↦ KL(ρ ‖ 1/2) + u ρ - c` is strictly increasing on `[1/(1 + e^u), 1]`: its derivative
`log (ρ/(1 - ρ)) + u` is positive for `1/(1 + e^u) < ρ < 1`. -/
theorem klBin_half_add_strictMonoOn (u c : ℝ) :
    StrictMonoOn (fun ρ : ℝ => klBin ρ (1 / 2) + u * ρ - c) (Icc (1 / (1 + Real.exp u)) 1) := by
  have hfun : (fun ρ : ℝ => klBin ρ (1 / 2) + u * ρ - c)
      = fun ρ => Real.log 2 - Real.binEntropy ρ + u * ρ - c := by
    funext ρ
    rw [klBin_half_eq]
  rw [hfun]
  apply strictMonoOn_of_deriv_pos (convex_Icc _ _)
  · fun_prop
  · intro x hx
    rw [interior_Icc] at hx
    have he : 0 < Real.exp u := Real.exp_pos u
    have hp : 0 < 1 / (1 + Real.exp u) := by positivity
    have hx0 : 0 < x := lt_trans hp hx.1
    have hx1 : x < 1 := hx.2
    have hd : HasDerivAt (fun ρ => Real.log 2 - Real.binEntropy ρ + u * ρ - c)
        (0 - (Real.log (1 - x) - Real.log x) + u * 1 - 0) x :=
      (((hasDerivAt_const x (Real.log 2)).sub (Real.hasDerivAt_binEntropy hx0.ne' hx1.ne)).add
        ((hasDerivAt_id x).const_mul u)).sub (hasDerivAt_const x c)
    rw [hd.deriv]
    have hlt : 1 - x < Real.exp u * x := by
      have h3 := hx.1
      rw [div_lt_iff₀ (by positivity)] at h3
      nlinarith
    have hlog : Real.log (1 - x) < u + Real.log x := by
      have h4 := Real.log_lt_log (by linarith) hlt
      rwa [Real.log_mul he.ne' hx0.ne', Real.log_exp] at h4
    linarith

/-! ### The generalised inverse of a strictly increasing function on an interval -/

/-- The largest point of the sublevel set of a strictly increasing function at one of its own
values is the point itself. -/
theorem sSup_sublevel_apply {f : ℝ → ℝ} {a b : ℝ} (hf : StrictMonoOn f (Icc a b)) {ρ : ℝ}
    (hρ : ρ ∈ Icc a b) : sSup {r | a ≤ r ∧ r ≤ b ∧ f r ≤ f ρ} = ρ := by
  apply le_antisymm
  · refine csSup_le ⟨ρ, hρ.1, hρ.2, le_rfl⟩ ?_
    rintro r ⟨hr1, hr2, hr3⟩
    exact (hf.le_iff_le ⟨hr1, hr2⟩ hρ).mp hr3
  · exact le_csSup ⟨b, fun r hr => hr.2.1⟩ ⟨hρ.1, hρ.2, le_rfl⟩

/-- The supremum of a sublevel set of a continuous function on `[a, b]` belongs to it. -/
theorem sSup_sublevel_mem {f : ℝ → ℝ} {a b : ℝ} (hab : a ≤ b) (hf : ContinuousOn f (Icc a b))
    {x : ℝ} (hx : f a ≤ x) :
    sSup {r | a ≤ r ∧ r ≤ b ∧ f r ≤ x} ∈ {r | a ≤ r ∧ r ≤ b ∧ f r ≤ x} := by
  have hset : {r | a ≤ r ∧ r ≤ b ∧ f r ≤ x} = Icc a b ∩ f ⁻¹' Iic x := by
    ext r
    simp [and_assoc]
  have hcl : IsClosed {r | a ≤ r ∧ r ≤ b ∧ f r ≤ x} := by
    rw [hset]
    exact hf.preimage_isClosed_of_isClosed isClosed_Icc isClosed_Iic
  exact hcl.csSup_mem ⟨a, le_rfl, hab, hx⟩ ⟨b, fun r hr => hr.2.1⟩

/-- The generalised inverse `x ↦ sup {r ∈ [a, b] : f r ≤ x}` of a strictly increasing function
is continuous at every `x > f a` (no continuity of `f` is needed). -/
theorem sSup_sublevel_continuousAt {f : ℝ → ℝ} {a b : ℝ} (hab : a ≤ b)
    (hf : StrictMonoOn f (Icc a b)) {x₀ : ℝ} (hx₀ : f a < x₀) :
    ContinuousAt (fun x => sSup {r | a ≤ r ∧ r ≤ b ∧ f r ≤ x}) x₀ := by
  have hbdd : ∀ x, BddAbove {r | a ≤ r ∧ r ≤ b ∧ f r ≤ x} := fun x => ⟨b, fun r hr => hr.2.1⟩
  have hne : ∀ x, f a ≤ x → ({r | a ≤ r ∧ r ≤ b ∧ f r ≤ x}).Nonempty :=
    fun x hx => ⟨a, le_rfl, hab, hx⟩
  rw [ContinuousAt, tendsto_order]
  constructor
  · -- values below the limit: a feasible radius `ρ₁ > c` stays feasible near `x₀`
    intro c hc
    obtain ⟨ρ', ⟨h1, h2, h3⟩, hcρ'⟩ := exists_lt_of_lt_csSup (hne x₀ hx₀.le) hc
    obtain ⟨ρ₁, hc1, ha1, hb1, hf1⟩ : ∃ ρ₁, c < ρ₁ ∧ a ≤ ρ₁ ∧ ρ₁ ≤ b ∧ f ρ₁ < x₀ := by
      rcases eq_or_lt_of_le h1 with h | h
      · exact ⟨a, by rw [h]; exact hcρ', le_rfl, hab, hx₀⟩
      · have hlt : max a ((c + ρ') / 2) < ρ' := max_lt h (by linarith)
        exact ⟨max a ((c + ρ') / 2), lt_max_of_lt_right (by linarith), le_max_left _ _,
          hlt.le.trans h2,
          lt_of_lt_of_le (hf ⟨le_max_left _ _, hlt.le.trans h2⟩ ⟨h1, h2⟩ hlt) h3⟩
    filter_upwards [lt_mem_nhds hf1] with x hx
    exact lt_of_lt_of_le hc1 (le_csSup (hbdd x) ⟨ha1, hb1, hx.le⟩)
  · -- values above the limit: a radius `ρ₂` between the limit and `c` is infeasible near `x₀`
    intro c hc
    rcases lt_or_ge b c with hbc | hcb
    · filter_upwards [lt_mem_nhds hx₀] with x hx
      exact lt_of_le_of_lt (csSup_le (hne x hx.le) fun r hr => hr.2.1) hbc
    · obtain ⟨R₀, hR₀c, haR, hup⟩ : ∃ R₀, R₀ < c ∧ a ≤ R₀ ∧
          ∀ r, a ≤ r → r ≤ b → f r ≤ x₀ → r ≤ R₀ :=
        ⟨_, hc, le_csSup (hbdd x₀) ⟨le_rfl, hab, hx₀.le⟩,
          fun r h1 h2 h3 => le_csSup (hbdd x₀) ⟨h1, h2, h3⟩⟩
      have h2a : a ≤ (R₀ + c) / 2 := by linarith
      have h2b : (R₀ + c) / 2 ≤ b := by linarith
      have hf2 : x₀ < f ((R₀ + c) / 2) := by
        by_contra hcon
        rw [not_lt] at hcon
        have h5 := hup _ h2a h2b hcon
        linarith
      filter_upwards [lt_mem_nhds hx₀, gt_mem_nhds hf2] with x hx hx2
      refine lt_of_le_of_lt (csSup_le (hne x hx.le) ?_) (show (R₀ + c) / 2 < c by linarith)
      rintro r ⟨hr1, hr2, hr3⟩
      by_contra hcon
      rw [not_le] at hcon
      have h6 := hf ⟨h2a, h2b⟩ ⟨hr1, hr2⟩ hcon
      linarith

/-! ### The functions of the cube -/

/-- `p_u = 1/(1 + e^u)`, the radius at which the accuracy `KL(· ‖ p_u)` vanishes. -/
noncomputable def cubeP (u : ℝ) : ℝ := 1 / (1 + Real.exp u)

/-- `Λ₁ = log (2/(1 + e^{-u}))`, the soft gap of one site. -/
noncomputable def cubeLam (u : ℝ) : ℝ := Real.log (2 / (1 + Real.exp (-u)))

/-- The threshold `ε* = KL(1/2 ‖ p_u)` (`= u/2 - Λ₁ = log cosh (u/2)`). -/
noncomputable def cubeEstar (u : ℝ) : ℝ := klBin (1 / 2) (cubeP u)

/-- `a = KL(p_u ‖ 1/2)`, the largest value of the non-adaptive exponent. -/
noncomputable def cubeA (u : ℝ) : ℝ := klBin (cubeP u) (1 / 2)

/-- `h = KL(Λ₁/u ‖ 1/2)`, the value of the hinted exponent at `0`. -/
noncomputable def cubeH (u : ℝ) : ℝ := klBin (cubeLam u / u) (1 / 2)

/-- The hinted exponent `θ_hint(e) = KL((Λ₁ + e)/u ‖ 1/2)`. -/
noncomputable def cubeHint (u e : ℝ) : ℝ := klBin ((cubeLam u + e) / u) (1 / 2)

/-- The largest radius `ρ ∈ [p_u, 1/2]` whose accuracy `KL(ρ ‖ p_u)` is at most `x`. -/
noncomputable def cubeRadius (u x : ℝ) : ℝ :=
  sSup {ρ | cubeP u ≤ ρ ∧ ρ ≤ 1 / 2 ∧ klBin ρ (cubeP u) ≤ x}

/-- The exponent of non-adaptive sampling,
`θ_na(x) = min {KL(ρ ‖ 1/2) : p_u ≤ ρ ≤ 1/2, KL(ρ ‖ p_u) ≤ x}`, defined as the value at the
largest feasible radius; `cubeNa_isLeast` says that it is that minimum for `x ≥ 0`.  (For `x < 0`
no radius is feasible and the value is of no significance.) -/
noncomputable def cubeNa (u x : ℝ) : ℝ := klBin (cubeRadius u x) (1 / 2)

theorem cubeP_pos (u : ℝ) : 0 < cubeP u := by
  unfold cubeP
  positivity

theorem cubeP_lt_one (u : ℝ) : cubeP u < 1 := by
  unfold cubeP
  rw [div_lt_one (by positivity)]
  linarith [Real.exp_pos u]

theorem cubeP_lt_half {u : ℝ} (hu : 0 < u) : cubeP u < 1 / 2 := by
  unfold cubeP
  have h1 : 1 < Real.exp u := Real.one_lt_exp_iff.mpr hu
  rw [div_lt_div_iff₀ (by positivity) (by norm_num)]
  linarith

/-- `klBin_shift` in the notation of this file. -/
theorem klBin_cubeP {u ρ : ℝ} (h0 : 0 < ρ) (h1 : ρ < 1) :
    klBin ρ (cubeP u) = klBin ρ (1 / 2) + u * ρ - cubeLam u :=
  klBin_shift h0 h1

/-- The accuracy `KL(· ‖ p_u)` is strictly increasing on `[p_u, 1)`. -/
theorem klBin_cubeP_strictMonoOn_Ico (u : ℝ) :
    StrictMonoOn (fun ρ : ℝ => klBin ρ (cubeP u)) (Ico (cubeP u) 1) := by
  refine ((klBin_half_add_strictMonoOn u (cubeLam u)).mono Ico_subset_Icc_self).congr ?_
  intro ρ hρ
  exact (klBin_cubeP (lt_of_lt_of_le (cubeP_pos u) hρ.1) hρ.2).symm

/-- The accuracy `KL(· ‖ p_u)` is strictly increasing on `[p_u, 1/2]`. -/
theorem klBin_cubeP_strictMonoOn (u : ℝ) :
    StrictMonoOn (fun ρ : ℝ => klBin ρ (cubeP u)) (Icc (cubeP u) (1 / 2)) :=
  (klBin_cubeP_strictMonoOn_Ico u).mono (Icc_subset_Ico_right (by norm_num))

theorem klBin_cubeP_continuousOn (u : ℝ) :
    ContinuousOn (fun ρ : ℝ => klBin ρ (cubeP u)) (Icc (cubeP u) (1 / 2)) := by
  have hc : Continuous fun ρ : ℝ => klBin ρ (1 / 2) + u * ρ - cubeLam u :=
    (klBin_half_continuous.add (continuous_const.mul continuous_id)).sub continuous_const
  refine hc.continuousOn.congr ?_
  intro ρ hρ
  exact klBin_cubeP (lt_of_lt_of_le (cubeP_pos u) hρ.1) (by linarith [hρ.2])

/-- `ε* = u/2 - Λ₁`. -/
theorem cubeEstar_eq (u : ℝ) : cubeEstar u = u / 2 - cubeLam u := by
  unfold cubeEstar
  rw [klBin_cubeP (by norm_num) (by norm_num), klBin_half_half]
  ring

/-- `ε* = log cosh (u/2)`. -/
theorem cubeEstar_eq_log_cosh (u : ℝ) : cubeEstar u = Real.log (Real.cosh (u / 2)) := by
  rw [cubeEstar_eq, Real.cosh_eq]
  unfold cubeLam
  have h1 : (Real.exp (u / 2) + Real.exp (-(u / 2))) / 2
      = Real.exp (u / 2) * ((1 + Real.exp (-u)) / 2) := by
    have h2 : Real.exp (-(u / 2)) = Real.exp (u / 2) * Real.exp (-u) := by
      rw [← Real.exp_add]
      congr 1
      ring
    rw [h2]
    ring
  rw [h1, Real.log_mul (Real.exp_pos _).ne' (by positivity), Real.log_exp,
    Real.log_div (by norm_num) (by positivity), Real.log_div (by positivity) (by norm_num)]
  ring

/-- `a = Λ₁ - u p_u`. -/
theorem cubeA_eq (u : ℝ) : cubeA u = cubeLam u - u * cubeP u := by
  have h := klBin_cubeP (u := u) (cubeP_pos u) (cubeP_lt_one u)
  rw [klBin_self] at h
  unfold cubeA
  linarith

theorem cubeA_pos {u : ℝ} (hu : 0 < u) : 0 < cubeA u :=
  klBin_half_pos (cubeP_pos u).le (cubeP_lt_half hu)

theorem cubeEstar_pos {u : ℝ} (hu : 0 < u) : 0 < cubeEstar u := by
  have h : klBin (cubeP u) (cubeP u) < klBin (1 / 2) (cubeP u) :=
    klBin_cubeP_strictMonoOn u ⟨le_rfl, (cubeP_lt_half hu).le⟩ ⟨(cubeP_lt_half hu).le, le_rfl⟩
      (cubeP_lt_half hu)
  rw [klBin_self] at h
  exact h

theorem cubeHint_zero (u : ℝ) : cubeHint u 0 = cubeH u := by
  unfold cubeHint cubeH
  rw [add_zero]

/-- The radius `(Λ₁ + e)/u` of the hinted exponent lies in `(p_u, 1/2]` for `0 ≤ e ≤ ε*`. -/
theorem cubeHintRadius_mem {u : ℝ} (hu : 0 < u) {e : ℝ} (he0 : 0 ≤ e) (heE : e ≤ cubeEstar u) :
    (cubeLam u + e) / u ∈ Ioc (cubeP u) (1 / 2) := by
  have ha := cubeA_pos hu
  rw [cubeA_eq] at ha
  rw [cubeEstar_eq] at heE
  constructor
  · rw [lt_div_iff₀ hu]
    linarith
  · rw [div_le_iff₀ hu]
    linarith

theorem cubeHintRadius_lt_half {u : ℝ} (hu : 0 < u) {e : ℝ} (heE : e < cubeEstar u) :
    (cubeLam u + e) / u < 1 / 2 := by
  rw [cubeEstar_eq] at heE
  rw [div_lt_iff₀ hu]
  linarith

/-- By `klBin_shift`, the accuracy at the radius of the hinted exponent is `e + θ_hint(e)`. -/
theorem klBin_cubeHintRadius {u : ℝ} (hu : 0 < u) {e : ℝ} (he0 : 0 ≤ e)
    (heE : e ≤ cubeEstar u) :
    klBin ((cubeLam u + e) / u) (cubeP u) = e + cubeHint u e := by
  obtain ⟨h1, h2⟩ := cubeHintRadius_mem hu he0 heE
  rw [klBin_cubeP (lt_trans (cubeP_pos u) h1) (by linarith)]
  unfold cubeHint
  have h3 : u * ((cubeLam u + e) / u) = cubeLam u + e := by field_simp
  rw [h3]
  ring

theorem cubeHint_pos {u : ℝ} (hu : 0 < u) {e : ℝ} (he0 : 0 ≤ e) (heE : e < cubeEstar u) :
    0 < cubeHint u e :=
  klBin_half_pos ((cubeP_pos u).le.trans (cubeHintRadius_mem hu he0 heE.le).1.le)
    (cubeHintRadius_lt_half hu heE)

/-- `e + θ_hint(e)` is nondecreasing on `[0, ε*]`: it is the accuracy `KL(· ‖ p_u)` at the radius
`(Λ₁ + e)/u`. -/
theorem cubeHint_add_mono {u : ℝ} (hu : 0 < u) {e e' : ℝ} (he0 : 0 ≤ e) (hee' : e ≤ e')
    (he'E : e' ≤ cubeEstar u) : e + cubeHint u e ≤ e' + cubeHint u e' := by
  have h1 := cubeHintRadius_mem hu he0 (hee'.trans he'E)
  have h2 := cubeHintRadius_mem hu (he0.trans hee') he'E
  rw [← klBin_cubeHintRadius hu he0 (hee'.trans he'E),
    ← klBin_cubeHintRadius hu (he0.trans hee') he'E]
  exact (klBin_cubeP_strictMonoOn u).monotoneOn ⟨h1.1.le, h1.2⟩ ⟨h2.1.le, h2.2⟩
    (div_le_div_of_nonneg_right (by linarith) hu.le)

/-! ### The largest feasible radius and the non-adaptive exponent -/

/-- At the accuracy of a radius `ρ ∈ [p_u, 1/2]` the largest feasible radius is `ρ`. -/
theorem cubeRadius_klBin {u ρ : ℝ} (hρ : ρ ∈ Icc (cubeP u) (1 / 2)) :
    cubeRadius u (klBin ρ (cubeP u)) = ρ :=
  sSup_sublevel_apply (klBin_cubeP_strictMonoOn u) hρ

theorem cubeRadius_mem_Icc {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 ≤ x) :
    cubeRadius u x ∈ Icc (cubeP u) (1 / 2) := by
  have hmem : cubeP u ∈ {ρ | cubeP u ≤ ρ ∧ ρ ≤ 1 / 2 ∧ klBin ρ (cubeP u) ≤ x} :=
    ⟨le_rfl, (cubeP_lt_half hu).le, by rw [klBin_self]; exact hx⟩
  exact ⟨le_csSup ⟨1 / 2, fun r hr => hr.2.1⟩ hmem, csSup_le ⟨_, hmem⟩ fun r hr => hr.2.1⟩

/-- The largest feasible radius is feasible. -/
theorem cubeRadius_mem {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 ≤ x) :
    cubeRadius u x ∈ {ρ | cubeP u ≤ ρ ∧ ρ ≤ 1 / 2 ∧ klBin ρ (cubeP u) ≤ x} := by
  have h0 : klBin (cubeP u) (cubeP u) ≤ x := by rw [klBin_self]; exact hx
  exact sSup_sublevel_mem (cubeP_lt_half hu).le (klBin_cubeP_continuousOn u) h0

/-- For `0 ≤ x ≤ ε*` the largest feasible radius is the root of `KL(ρ ‖ p_u) = x`. -/
theorem klBin_cubeRadius {u : ℝ} (hu : 0 < u) {x : ℝ} (hx0 : 0 ≤ x) (hxE : x ≤ cubeEstar u) :
    klBin (cubeRadius u x) (cubeP u) = x := by
  have h0 : klBin (cubeP u) (cubeP u) ≤ x := by rw [klBin_self]; exact hx0
  obtain ⟨ρ, hρ, hρx⟩ := intermediate_value_Icc (cubeP_lt_half hu).le (klBin_cubeP_continuousOn u)
    (show x ∈ Icc (klBin (cubeP u) (cubeP u)) (klBin (1 / 2) (cubeP u)) from ⟨h0, hxE⟩)
  have hρx' : klBin ρ (cubeP u) = x := hρx
  rw [← hρx', cubeRadius_klBin hρ]

theorem cubeRadius_continuousAt {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 < x) :
    ContinuousAt (cubeRadius u) x := by
  have h0 : klBin (cubeP u) (cubeP u) < x := by rw [klBin_self]; exact hx
  exact sSup_sublevel_continuousAt (cubeP_lt_half hu).le (klBin_cubeP_strictMonoOn u) h0

/-- **The non-adaptive exponent is the minimum** of `KL(ρ ‖ 1/2)` over the radii
`ρ ∈ [p_u, 1/2]` with accuracy `KL(ρ ‖ p_u) ≤ x`. -/
theorem cubeNa_isLeast {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 ≤ x) :
    IsLeast ((fun ρ => klBin ρ (1 / 2)) ''
      {ρ | cubeP u ≤ ρ ∧ ρ ≤ 1 / 2 ∧ klBin ρ (cubeP u) ≤ x}) (cubeNa u x) := by
  refine ⟨⟨cubeRadius u x, cubeRadius_mem hu hx, rfl⟩, ?_⟩
  rintro _ ⟨ρ, hρ, rfl⟩
  have hle : ρ ≤ cubeRadius u x := le_csSup ⟨1 / 2, fun r hr => hr.2.1⟩ hρ
  exact klBin_half_strictAntiOn.antitoneOn ⟨(cubeP_pos u).le.trans hρ.1, hρ.2.1⟩
    ⟨(cubeP_pos u).le.trans (cubeRadius_mem_Icc hu hx).1, (cubeRadius_mem_Icc hu hx).2⟩ hle

/-- At the accuracy of a radius `ρ ∈ [p_u, 1/2]` the non-adaptive exponent is `KL(ρ ‖ 1/2)`. -/
theorem cubeNa_klBin {u ρ : ℝ} (hρ : ρ ∈ Icc (cubeP u) (1 / 2)) :
    cubeNa u (klBin ρ (cubeP u)) = klBin ρ (1 / 2) := by
  unfold cubeNa
  rw [cubeRadius_klBin hρ]

theorem cubeNa_zero {u : ℝ} (hu : 0 < u) : cubeNa u 0 = cubeA u := by
  have h := cubeNa_klBin (u := u) (ρ := cubeP u) ⟨le_rfl, (cubeP_lt_half hu).le⟩
  rw [klBin_self] at h
  exact h

/-- From the threshold `ε*` on, the non-adaptive exponent is zero. -/
theorem cubeNa_of_cubeEstar_le {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : cubeEstar u ≤ x) :
    cubeNa u x = 0 := by
  have hmem : (1 / 2 : ℝ) ∈ {ρ | cubeP u ≤ ρ ∧ ρ ≤ 1 / 2 ∧ klBin ρ (cubeP u) ≤ x} :=
    ⟨(cubeP_lt_half hu).le, le_rfl, hx⟩
  have hr : cubeRadius u x = 1 / 2 :=
    le_antisymm (csSup_le ⟨_, hmem⟩ fun r hr => hr.2.1)
      (le_csSup ⟨1 / 2, fun r hr => hr.2.1⟩ hmem)
  unfold cubeNa
  rw [hr, klBin_half_half]

theorem cubeNa_nonneg (u x : ℝ) : 0 ≤ cubeNa u x :=
  klBin_half_nonneg _

/-- The non-adaptive exponent is at most `a = KL(p_u ‖ 1/2)`. -/
theorem cubeNa_le_cubeA {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 ≤ x) : cubeNa u x ≤ cubeA u := by
  have hr := cubeRadius_mem_Icc hu hx
  exact klBin_half_strictAntiOn.antitoneOn ⟨(cubeP_pos u).le, (cubeP_lt_half hu).le⟩
    ⟨(cubeP_pos u).le.trans hr.1, hr.2⟩ hr.1

/-- The non-adaptive exponent is nonincreasing on `[0, ∞)`. -/
theorem cubeNa_antitoneOn {u : ℝ} (hu : 0 < u) : AntitoneOn (cubeNa u) (Ici 0) := by
  intro x hx y hy hxy
  have hrx := cubeRadius_mem_Icc hu hx
  have hry := cubeRadius_mem_Icc hu hy
  have hle : cubeRadius u x ≤ cubeRadius u y :=
    csSup_le_csSup ⟨1 / 2, fun r hr => hr.2.1⟩
      ⟨cubeP u, le_rfl, (cubeP_lt_half hu).le, by rw [klBin_self]; exact hx⟩
      (fun r hr => ⟨hr.1, hr.2.1, hr.2.2.trans hxy⟩)
  exact klBin_half_strictAntiOn.antitoneOn ⟨(cubeP_pos u).le.trans hrx.1, hrx.2⟩
    ⟨(cubeP_pos u).le.trans hry.1, hry.2⟩ hle

/-- The non-adaptive exponent is continuous on `(0, ∞)`. -/
theorem cubeNa_continuousAt {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 < x) :
    ContinuousAt (cubeNa u) x :=
  klBin_half_continuous.continuousAt.comp (cubeRadius_continuousAt hu hx)

/-- The restriction to radii in `[p_u, 1/2]` is immaterial: the non-adaptive exponent is the
minimum of `KL(ρ ‖ 1/2)` over all `ρ ∈ [0, 1]` with `KL(ρ ‖ p_u) ≤ x`. -/
theorem cubeNa_isLeast_allRadii {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 ≤ x) :
    IsLeast ((fun ρ => klBin ρ (1 / 2)) '' {ρ | 0 ≤ ρ ∧ ρ ≤ 1 ∧ klBin ρ (cubeP u) ≤ x})
      (cubeNa u x) := by
  obtain ⟨hr1, hr2, hr3⟩ := cubeRadius_mem hu hx
  refine ⟨⟨cubeRadius u x, ⟨(cubeP_pos u).le.trans hr1, by linarith, hr3⟩, rfl⟩, ?_⟩
  rintro _ ⟨ρ, ⟨hρ0, hρ1, hρx⟩, rfl⟩
  show cubeNa u x ≤ klBin ρ (1 / 2)
  rcases lt_or_ge ρ (cubeP u) with hlt | hge
  · -- below `p_u`: `KL(ρ ‖ 1/2) ≥ a`
    have h1 : klBin (cubeP u) (1 / 2) ≤ klBin ρ (1 / 2) :=
      klBin_half_strictAntiOn.antitoneOn ⟨hρ0, by linarith [cubeP_lt_half hu]⟩
        ⟨(cubeP_pos u).le, (cubeP_lt_half hu).le⟩ hlt.le
    exact (cubeNa_le_cubeA hu hx).trans h1
  rcases le_or_gt ρ (1 / 2) with hle | hgt
  · exact (cubeNa_isLeast hu hx).2 ⟨ρ, ⟨hge, hle, hρx⟩, rfl⟩
  rcases eq_or_lt_of_le hρ1 with h1 | h1
  · -- `ρ = 1`: `KL(1 ‖ 1/2) = log 2 ≥ a`
    have h2 : cubeA u ≤ klBin ρ (1 / 2) := by
      unfold cubeA
      rw [h1, klBin_half_eq, klBin_half_eq, Real.binEntropy_one]
      linarith [Real.binEntropy_nonneg (cubeP_pos u).le (cubeP_lt_one u).le]
    exact (cubeNa_le_cubeA hu hx).trans h2
  · -- `1/2 < ρ < 1`: the accuracy exceeds `ε*`, where the exponent is zero
    have hE : cubeEstar u < klBin ρ (cubeP u) :=
      klBin_cubeP_strictMonoOn_Ico u ⟨(cubeP_lt_half hu).le, by norm_num⟩ ⟨hge, h1⟩ hgt
    rw [cubeNa_of_cubeEstar_le hu (hE.le.trans hρx)]
    exact klBin_half_nonneg ρ

/-- The identity `θ_na(e + θ_hint(e)) = θ_hint(e)` on `[0, ε*]`. -/
theorem cubeNa_add_cubeHint {u : ℝ} (hu : 0 < u) {e : ℝ} (he0 : 0 ≤ e) (heE : e ≤ cubeEstar u) :
    cubeNa u (e + cubeHint u e) = cubeHint u e := by
  have hmem := cubeHintRadius_mem hu he0 heE
  rw [← klBin_cubeHintRadius hu he0 heE, cubeNa_klBin ⟨hmem.1.le, hmem.2⟩]
  rfl

/-- Below the threshold the hinted exponent is strictly smaller than the non-adaptive one. -/
theorem cubeHint_lt_cubeNa {u : ℝ} (hu : 0 < u) {e : ℝ} (he0 : 0 ≤ e) (heE : e < cubeEstar u) :
    cubeHint u e < cubeNa u e := by
  have hmem := cubeHintRadius_mem hu he0 heE.le
  have hpos := cubeHint_pos hu he0 heE
  have hr := cubeRadius_mem_Icc hu he0
  have hfeas : klBin (cubeRadius u e) (cubeP u) ≤ e := (cubeRadius_mem hu he0).2.2
  have hF := klBin_cubeHintRadius hu he0 heE.le
  have hlt : cubeRadius u e < (cubeLam u + e) / u := by
    by_contra hcon
    rw [not_lt] at hcon
    have h1 : klBin ((cubeLam u + e) / u) (cubeP u) ≤ klBin (cubeRadius u e) (cubeP u) :=
      (klBin_cubeP_strictMonoOn u).monotoneOn ⟨hmem.1.le, hmem.2⟩ hr hcon
    linarith
  exact klBin_half_strictAntiOn ⟨(cubeP_pos u).le.trans hr.1, hr.2⟩
    ⟨(cubeP_pos u).le.trans hmem.1.le, hmem.2⟩ hlt

/-! ### The pair of the cube -/

/-- **The exponent functions of the Hamming cube satisfy `HintPair`**, with `a = KL(p_u ‖ 1/2)`,
`h = KL(Λ₁/u ‖ 1/2)` and `E = ε* = KL(1/2 ‖ p_u)`; the constant of `hint_lower` is `L = 1`. -/
theorem cubePair {u : ℝ} (hu : 0 < u) :
    HintPair (cubeNa u) (cubeHint u) (cubeA u) (cubeH u) (cubeEstar u) where
  h_pos := by
    rw [← cubeHint_zero]
    exact cubeHint_pos hu le_rfl (cubeEstar_pos hu)
  a_pos := cubeA_pos hu
  na_le := fun _ hx => cubeNa_le_cubeA hu hx.le
  na_cont := fun _ hx => cubeNa_continuousAt hu hx
  na_h := by
    have h := cubeNa_add_cubeHint hu le_rfl (cubeEstar_pos hu).le
    rw [zero_add, cubeHint_zero] at h
    exact h
  ident := fun _ he0 heE => cubeNa_add_cubeHint hu he0.le heE.le
  hint_pos := fun _ he0 heE => cubeHint_pos hu he0.le heE
  hint_mono := fun _ _ he hee' he' => cubeHint_add_mono hu he.le hee' he'.le
  hint_lower := ⟨1, by
    intro e he0 heE
    have h := cubeHint_add_mono hu le_rfl he0.le heE.le
    rw [zero_add, cubeHint_zero] at h
    linarith⟩

/-- No super-solution of the level recursion of the cube lies above the hinted exponent
(`superSolution_le_hint` for the pair of the cube). -/
theorem cube_superSolution_le_hint {u : ℝ} (hu : 0 < u) {T : ℝ → ℝ}
    (hs : StepLE (cubeNa u) T T) (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x)
    (hbdd : ∃ C, ∀ x, 0 < x → T x ≤ C) :
    ∀ g, 0 < g → g < cubeEstar u → T g ≤ cubeHint u g :=
  superSolution_le_hint (cubePair hu) hs hanti hbdd

/-- The level recursion of the cube converges to the hinted exponent
(`iterates_lt_hint_add` for the pair of the cube). -/
theorem cube_iterates_lt_hint_add {u : ℝ} (hu : 0 < u) (T : ℕ → ℝ → ℝ)
    (hstep : ∀ k, StepLE (cubeNa u) (T k) (T (k + 1)))
    (hmono : ∀ k x, 0 < x → T (k + 1) x ≤ T k x)
    (hanti : ∀ k x y, 0 < x → x ≤ y → T k y ≤ T k x)
    (hbdd : ∃ C, ∀ x, 0 < x → T 0 x ≤ C) (hnn : ∀ k x, 0 < x → 0 ≤ T k x)
    {g : ℝ} (hg : 0 < g) (hgE : g < cubeEstar u) {η : ℝ} (hη : 0 < η) :
    ∃ k, T k g < cubeHint u g + η :=
  iterates_lt_hint_add (cubePair hu) T hstep hmono hanti hbdd hnn hg hgE hη

/-- The zero function satisfies the hypotheses of `cube_superSolution_le_hint`, so they are
consistent. -/
theorem cube_zero_superSolution (u : ℝ) : StepLE (cubeNa u) (fun _ => 0) (fun _ => 0) := by
  intro g φ β B hβ _ hφ0 _ hB
  have h1 := hB β le_rfl
  have h2 : 0 ≤ min β (φ * cubeNa u ((g - β) / φ)) :=
    le_min hβ.le (mul_nonneg hφ0.le (cubeNa_nonneg _ _))
  simp only [mul_zero, add_zero] at h1
  show (0 : ℝ) ≤ B
  linarith

/-! ### The hinted exponent is a fixed point of the recursion

`step_from_hint_le` asks for a hinted exponent that is nonincreasing on all of `(0, ∞)`.  The
function `cubeHint u` is nonincreasing up to `ε*` only (beyond it the radius `(Λ₁ + e)/u` exceeds
`1/2`); continued by zero from `ε*` on it is nonincreasing, and since the fields of `HintPair`
concern `(0, ε*)` only, the pair is still a `HintPair`. -/

/-- The hinted exponent of the cube, continued by zero from `ε*` on. -/
noncomputable def cubeHintClip (u e : ℝ) : ℝ := cubeHint u (min e (cubeEstar u))

theorem cubeHintClip_eq {u e : ℝ} (he : e ≤ cubeEstar u) : cubeHintClip u e = cubeHint u e := by
  unfold cubeHintClip
  rw [min_eq_left he]

/-- At the threshold the radius of the hinted exponent is `1/2` and the exponent vanishes. -/
theorem cubeHint_cubeEstar {u : ℝ} (hu : 0 < u) : cubeHint u (cubeEstar u) = 0 := by
  unfold cubeHint
  have h : (cubeLam u + cubeEstar u) / u = 1 / 2 := by
    rw [cubeEstar_eq, div_eq_iff hu.ne']
    ring
  rw [h, klBin_half_half]

theorem cubeHintClip_of_cubeEstar_le {u : ℝ} (hu : 0 < u) {e : ℝ} (he : cubeEstar u ≤ e) :
    cubeHintClip u e = 0 := by
  unfold cubeHintClip
  rw [min_eq_right he, cubeHint_cubeEstar hu]

/-- The hinted exponent is nonincreasing on `[0, ε*]`. -/
theorem cubeHint_antitoneOn {u : ℝ} (hu : 0 < u) :
    AntitoneOn (cubeHint u) (Icc 0 (cubeEstar u)) := by
  intro e he e' he' hee'
  have h1 := cubeHintRadius_mem hu he.1 he.2
  have h2 := cubeHintRadius_mem hu he'.1 he'.2
  exact klBin_half_strictAntiOn.antitoneOn ⟨(cubeP_pos u).le.trans h1.1.le, h1.2⟩
    ⟨(cubeP_pos u).le.trans h2.1.le, h2.2⟩ (div_le_div_of_nonneg_right (by linarith) hu.le)

/-- The clipped hinted exponent is nonincreasing on `(0, ∞)`. -/
theorem cubeHintClip_anti {u : ℝ} (hu : 0 < u) {x y : ℝ} (hx : 0 < x) (hxy : x ≤ y) :
    cubeHintClip u y ≤ cubeHintClip u x := by
  have hE := (cubeEstar_pos hu).le
  exact cubeHint_antitoneOn hu ⟨le_min hx.le hE, min_le_right _ _⟩
    ⟨le_min (hx.le.trans hxy) hE, min_le_right _ _⟩ (min_le_min_right _ hxy)

/-- The pair of the cube with the clipped hinted exponent. -/
theorem cubePairClip {u : ℝ} (hu : 0 < u) :
    HintPair (cubeNa u) (cubeHintClip u) (cubeA u) (cubeH u) (cubeEstar u) where
  h_pos := (cubePair hu).h_pos
  a_pos := (cubePair hu).a_pos
  na_le := (cubePair hu).na_le
  na_cont := (cubePair hu).na_cont
  na_h := (cubePair hu).na_h
  ident := fun e he0 heE => by
    rw [cubeHintClip_eq heE.le]
    exact (cubePair hu).ident e he0 heE
  hint_pos := fun e he0 heE => by
    rw [cubeHintClip_eq heE.le]
    exact (cubePair hu).hint_pos e he0 heE
  hint_mono := fun e e' he hee' he' => by
    rw [cubeHintClip_eq (hee'.trans he'.le), cubeHintClip_eq he'.le]
    exact (cubePair hu).hint_mono e e' he hee' he'
  hint_lower := ⟨1, fun e he0 heE => by
    rw [cubeHintClip_eq heE.le]
    have h := cubeHint_add_mono hu le_rfl he0.le heE.le
    rw [zero_add, cubeHint_zero] at h
    linarith⟩

/-- One step of the level recursion from the hinted exponent of the cube does not leave it:
`R[θ_hint] ≤ θ_hint` on `(0, ε*)` (`step_from_hint_le` for the pair of the cube). -/
theorem cube_step_from_hint_le {u : ℝ} (hu : 0 < u) {T' : ℝ → ℝ}
    (hs : StepLE (cubeNa u) (cubeHintClip u) T') {g : ℝ} (hg : 0 < g) (hgE : g < cubeEstar u) :
    T' g ≤ cubeHint u g := by
  have h := step_from_hint_le (cubePairClip hu) hs
    (fun _ _ hx hxy => cubeHintClip_anti hu hx hxy) hg hgE
  rwa [cubeHintClip_eq hgE.le] at h

theorem cubeHintClip_nonneg (u e : ℝ) : 0 ≤ cubeHintClip u e :=
  klBin_half_nonneg _

theorem cubeHintClip_le_cubeH {u : ℝ} (hu : 0 < u) {x : ℝ} (hx : 0 ≤ x) :
    cubeHintClip u x ≤ cubeH u := by
  have hE := (cubeEstar_pos hu).le
  rw [← cubeHint_zero]
  exact cubeHint_antitoneOn hu ⟨le_rfl, hE⟩ ⟨le_min hx hE, min_le_right _ _⟩ (le_min hx hE)

/-- **The hinted exponent of the cube is a super-solution** of the level recursion: one step from
it does not go below it (Theorem 11.53(b), "`≥`").  With `cube_step_from_hint_le` the hinted
exponent is a fixed point of the recursion on `(0, ε*)`, and it is a positive function to which
`cube_superSolution_le_hint` applies, so the bound of that theorem is attained.  The proof is the
convexity argument of the theory report: at `γ = max(β, μ)` the bracket is a convex combination
`φ KL(ρo ‖ 1/2) + (1 - φ) KL(ρi ‖ 1/2)` of the outer and the inner term, by `klBin_shift` the mean
radius `φ ρo + (1 - φ) ρi` is at most the radius of the hinted exponent at the target accuracy,
and `KL(· ‖ 1/2)` is convex on `[0, 1]` and nonincreasing on `[0, 1/2]`. -/
theorem cube_hint_superSolution {u : ℝ} (hu : 0 < u) :
    StepLE (cubeNa u) (cubeHintClip u) (cubeHintClip u) := by
  intro g φ β B hβ hβg hφ0 hφ1 hB
  show cubeHintClip u g ≤ B
  have h1 : 0 < 1 - φ := by linarith
  have hE := cubeEstar_pos hu
  -- the outer radius `ρo` and the outer exponent `μ = φ KL(ρo ‖ 1/2)`
  have hr := cubeRadius_mem hu (div_nonneg (by linarith) hφ0.le : 0 ≤ (g - β) / φ)
  obtain ⟨ρo, hρo1, hρo2, hρo3, hna⟩ : ∃ ρo, cubeP u ≤ ρo ∧ ρo ≤ 1 / 2 ∧
      klBin ρo (cubeP u) ≤ (g - β) / φ ∧ cubeNa u ((g - β) / φ) = klBin ρo (1 / 2) :=
    ⟨cubeRadius u ((g - β) / φ), hr.1, hr.2.1, hr.2.2, rfl⟩
  have hρo0 : 0 < ρo := lt_of_lt_of_le (cubeP_pos u) hρo1
  rw [klBin_cubeP hρo0 (by linarith), le_div_iff₀ hφ0] at hρo3
  obtain ⟨μ, hμ, hμ0⟩ : ∃ μ, μ = φ * klBin ρo (1 / 2) ∧ 0 ≤ μ :=
    ⟨_, rfl, mul_nonneg hφ0.le (klBin_half_nonneg _)⟩
  have hkey := hB (max β μ) (le_max_left _ _)
  rw [hna, ← hμ, min_eq_right (le_max_right _ _)] at hkey
  have hmax : max β μ ≤ β + μ := max_le (by linarith) (by linarith)
  -- the inner accuracy `m` (capped at `ε*`) and the inner radius `ρi`
  obtain ⟨m, hm0, hmE, hmy, hclip⟩ : ∃ m, 0 ≤ m ∧ m ≤ cubeEstar u ∧ (1 - φ) * m ≤ max β μ ∧
      cubeHintClip u (max β μ / (1 - φ)) = cubeHint u m := by
    refine ⟨min (max β μ / (1 - φ)) (cubeEstar u),
      le_min (div_nonneg (hβ.le.trans (le_max_left _ _)) h1.le) hE.le, min_le_right _ _, ?_, rfl⟩
    have h2 := mul_le_mul_of_nonneg_left
      (min_le_left (max β μ / (1 - φ)) (cubeEstar u)) h1.le
    have h3 : (1 - φ) * (max β μ / (1 - φ)) = max β μ := by field_simp
    linarith
  have hmi := cubeHintRadius_mem hu hm0 hmE
  obtain ⟨ρi, hρi1, hρi2, hρi, hhint⟩ : ∃ ρi, cubeP u < ρi ∧ ρi ≤ 1 / 2 ∧
      u * ρi = cubeLam u + m ∧ cubeHint u m = klBin ρi (1 / 2) :=
    ⟨(cubeLam u + m) / u, hmi.1, hmi.2, by field_simp, rfl⟩
  rw [hclip, hhint] at hkey
  -- the radius `ρg` of the hinted exponent at the target accuracy
  have hgi := cubeHintRadius_mem hu
    (le_min (hβ.le.trans hβg.le) hE.le : 0 ≤ min g (cubeEstar u)) (min_le_right _ _)
  obtain ⟨ρg, hρg1, hρg2, hρg, hgoal⟩ : ∃ ρg, cubeP u < ρg ∧ ρg ≤ 1 / 2 ∧
      u * ρg = cubeLam u + min g (cubeEstar u) ∧ cubeHintClip u g = klBin ρg (1 / 2) :=
    ⟨(cubeLam u + min g (cubeEstar u)) / u, hgi.1, hgi.2, by field_simp, rfl⟩
  rw [hgoal]
  have hρi0 : 0 ≤ ρi := (cubeP_pos u).le.trans hρi1.le
  -- convexity of `KL(· ‖ 1/2)`
  have hconv : klBin (φ * ρo + (1 - φ) * ρi) (1 / 2)
      ≤ φ * klBin ρo (1 / 2) + (1 - φ) * klBin ρi (1 / 2) := by
    have hc := Real.strictConcave_binEntropy.concaveOn.2
      (show ρo ∈ Icc (0 : ℝ) 1 from ⟨hρo0.le, by linarith⟩)
      (show ρi ∈ Icc (0 : ℝ) 1 from ⟨hρi0, by linarith⟩) hφ0.le h1.le (by ring)
    simp only [smul_eq_mul] at hc
    simp only [klBin_half_eq]
    linarith
  -- the mean radius is at most `ρg`
  have hmean : φ * ρo + (1 - φ) * ρi ≤ ρg := by
    have hb : (1 - φ) * (u * ρi) = (1 - φ) * cubeLam u + (1 - φ) * m := by
      rw [hρi]
      ring
    have hmul : u * (φ * ρo + (1 - φ) * ρi) ≤ u * ρg := by
      rw [hρg]
      rcases le_total g (cubeEstar u) with hgE | hgE
      · rw [min_eq_left hgE]
        linarith
      · rw [min_eq_right hgE, cubeEstar_eq]
        have h4 := mul_le_mul_of_nonneg_left hρo2 hφ0.le
        have h5 := mul_le_mul_of_nonneg_left hρi2 h1.le
        have h6 := mul_le_mul_of_nonneg_left (add_le_add h4 h5) hu.le
        linarith
    exact le_of_mul_le_mul_left hmul hu
  have hanti : klBin ρg (1 / 2) ≤ klBin (φ * ρo + (1 - φ) * ρi) (1 / 2) :=
    klBin_half_strictAntiOn.antitoneOn
      ⟨add_nonneg (mul_nonneg hφ0.le hρo0.le) (mul_nonneg h1.le hρi0), hmean.trans hρg2⟩
      ⟨(cubeP_pos u).le.trans hρg1.le, hρg2⟩ hmean
  linarith

/-- **Witness for `cube_superSolution_le_hint` and `cube_iterates_lt_hint_add`.**  The hinted
exponent of the cube, continued by zero, is a nonincreasing bounded function with `T ≤ R[T]`
(`cube_hint_superSolution`) that is positive on `(0, ε*)`; so the hypotheses of both theorems are
satisfied by something other than zero, and the conclusion `T ≤ θ_hint` holds with equality. -/
theorem cube_hintRecursion_witness {u : ℝ} (hu : 0 < u) {g : ℝ} (hg : 0 < g)
    (hgE : g < cubeEstar u) :
    cubeHintClip u g ≤ cubeHint u g ∧ cubeHintClip u g = cubeHint u g ∧ 0 < cubeHintClip u g ∧
      ∀ η : ℝ, 0 < η → ∃ k : ℕ, (fun (_ : ℕ) => cubeHintClip u) k g < cubeHint u g + η := by
  have hanti : ∀ x y : ℝ, 0 < x → x ≤ y → cubeHintClip u y ≤ cubeHintClip u x :=
    fun _ _ hx hxy => cubeHintClip_anti hu hx hxy
  have hbdd : ∃ C, ∀ x : ℝ, 0 < x → cubeHintClip u x ≤ C :=
    ⟨cubeH u, fun _ hx => cubeHintClip_le_cubeH hu hx.le⟩
  refine ⟨cube_superSolution_le_hint hu (cube_hint_superSolution hu) hanti hbdd g hg hgE,
    cubeHintClip_eq hgE.le, ?_, ?_⟩
  · rw [cubeHintClip_eq hgE.le]
    exact cubeHint_pos hu hg.le hgE
  · intro η hη
    exact cube_iterates_lt_hint_add hu (fun _ => cubeHintClip u)
      (fun _ => cube_hint_superSolution hu) (fun _ _ _ => le_rfl) (fun _ => hanti) hbdd
      (fun _ _ _ => cubeHintClip_nonneg _ _) hg hgE hη

end HintRecursion
end MetricChain
