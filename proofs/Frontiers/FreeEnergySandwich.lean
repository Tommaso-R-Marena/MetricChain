import Mathlib

/-!
# The free-energy sandwich: Gibbs–Bogoliubov below, Hoeffding–McDiarmid above

A reference Gibbs ensemble on a finite configuration space `Ω` is a probability weight vector
`w : Ω → ℝ` (`0 ≤ w x`, `∑ x, w x = 1`; think `w = exp (-β E₀) / Z₀`).  A residual energy
`Δ : Ω → ℝ` perturbs it, and the partition-function ratio is

`Z / Z₀ = ∑ x, w x * exp (-β * Δ x)`.

This file proves rigorous two-sided bounds on `log (Z / Z₀)` which use only the reference mean
`⟨Δ⟩₀ = ∑ x, w x * Δ x` and oscillation / bounded-difference information about `Δ`.  Nothing is
assumed about the structure of `Δ` (it may be a non-decomposable many-body term).  We call
`log (Z / Z₀) + β ⟨Δ⟩₀ ≥ 0` the *Jensen gap*.

## Main results

* **T1** `gibbs_bogoliubov` — Jensen lower bound `-β ⟨Δ⟩₀ ≤ log (Z / Z₀)`.
* **T2** `hoeffding_core`, `hoeffding_upper` — Hoeffding's lemma for finite weighted sums:
  if `a ≤ g ≤ b` then `∑ x, w x * exp (g x - ⟨g⟩) ≤ exp ((b - a)² / 8)`, hence
  `log (Z / Z₀) ≤ -β ⟨Δ⟩₀ + β² (b - a)² / 8`.
* **T3** `free_energy_sandwich`, `partition_ratio_sandwich`, `free_energy_difference_sandwich` —
  the two bounds combined: for abstract weights, for `Z / Z₀` with Boltzmann weights
  `w x = exp (-β E₀ x) / Z₀`, and for the free-energy difference `F - F₀` with
  `F = -(1/β) log Z`:  `⟨Δ⟩₀ - β (b - a)² / 8 ≤ F - F₀ ≤ ⟨Δ⟩₀`.
* **T4** `mcdiarmid_mgf`, `mcdiarmid_log_upper`, `bounded_differences_sandwich` — McDiarmid
  tensorization.  For a *product* reference `W x = ∏ i, p i (x i)` on `Fin n → α` and a residual
  with bounded differences `|g (update x i a) - g x| ≤ c i`,
  `∑ x, W x * exp (g x - ⟨g⟩) ≤ exp ((∑ i, (c i)²) / 8)`, hence
  `-β ⟨Δ⟩ ≤ log (∑ x, W x * exp (-β Δ x)) ≤ -β ⟨Δ⟩ + β² (∑ i, (c i)²) / 8`.
  The engine is `bounded_differences_tensorization`: *any* family of single-site bounds on the
  centred moment generating function tensorizes over the sites.
  `mcdiarmid_mgf_pi`, `bounded_differences_sandwich_pi` are the same statements for an
  arbitrary finite site index type `ι` and site-dependent alphabets `σ i` (configurations
  `x : ∀ i, σ i`; a heteropolymer, where every site has its own state space).
* **T5** sharpness — the worst residual is *additive* (fully decomposable) and *two-level*:
  * `additive_gap_eq` — for an additive residual `Δ x = ∑ i, δ i (x i)` the Jensen gap is
    exactly the sum of the single-site gaps;
  * `additive_extremal`, `exists_two_level_additive_extremal`,
    `exists_two_level_worst_residual` — for **every** product reference, every `β` and all
    constants `c i ≥ 0` there are subsets of site states such that the additive two-level
    residual `Δ⋆ x = ∑ i, c i * [x i ∈ A i]` has the largest Jensen gap among all residuals with
    bounded differences `c`; its gap is given in closed form by `two_level_additive_gap`;
  * `balanced_additive_gap`, `balanced_additive_extremal` — for the balanced two-level
    reference (`α = Bool`, `p i b = 1/2`) the worst case is `Δ x = ∑ i, c i * [x i]`, with gap
    exactly `∑ i, log (cosh (β * c i / 2))`;
  * `log_cosh_bounds`, `tendsto_log_cosh_div_sq`, `balanced_additive_gap_bounds` —
    `u² / (2 + u²) ≤ log (cosh u) ≤ u² / 2` and `log (cosh u) / u² → 1/2`, so this gap agrees
    with the bound of T4 to leading order;
  * `hoeffding_constant_sharp`, `mcdiarmid_constant_optimal`, `mcdiarmid_no_better_constant` —
    for every `K < 1/8` the bound of T4 with `K` in place of `1/8` fails, already for `n = 1`,
    the balanced two-level reference and an additive residual.

## Proof outline

* T1 is Jensen's inequality for `exp` (`ConvexOn.map_sum_le`).
* T2 transfers Mathlib's Hoeffding lemma
  (`ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc`) to finite weighted sums: the weights define
  the probability measure `∑ x, w x • δ_x` on `Ω` (discrete σ-algebra), with respect to which
  every integral is the corresponding finite weighted sum.
* T4 is the martingale (tensorization) argument, by induction on the number of sites using
  `(∀ i : Fin (n + 1), σ i) ≃ σ 0 × (∀ i : Fin n, σ i.succ)`: one single-site step in the first
  coordinate (`two_factor_step`, `two_factor_tensorization`), and the site-0 average of `g`
  again has bounded differences.  The general index type is reduced to `Fin n` by transport
  along an enumeration of the sites.
* T5 uses `∏ i, ∑ a, f i a = ∑ x, ∏ i, f i (x i)` (`Fintype.prod_sum`) to factor sums of
  products of site terms; the tensorization engine of T4 with the *exact* single-site suprema
  in place of Hoeffding's bound; convexity of the centred moment generating function (its
  maximum over a cube is attained at a vertex, i.e. at a two-level function); and elementary
  bounds on `cosh`.

No measure theory appears in any statement: everything is a finite sum over a `Fintype`.

## Conventions used in the docstrings

`W x = ∏ i, p i (x i)` is the product weight of a configuration `x : Fin n → α`;
`⟨g⟩ = ∑ x, W x * g x` is the reference mean; `[P]` is the indicator `if P then 1 else 0`;
"bounded differences `c`" means `∀ x i a, |g (Function.update x i a) - g x| ≤ c i`.
-/

namespace MetricChain

/-! ## T1. Gibbs–Bogoliubov (Jensen) lower bound -/

section Jensen

variable {Ω : Type*} [Fintype Ω]

/-- **Jensen's inequality for `exp`** with respect to a finite probability weight vector. -/
theorem jensen_exp_weighted (w g : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1) :
    Real.exp (∑ x, w x * g x) ≤ ∑ x, w x * Real.exp (g x) := by
  have h := convexOn_exp.map_sum_le (t := Finset.univ) (w := w) (p := g)
    (fun x _ => hw x) hsum (fun x _ => Set.mem_univ _)
  simpa [smul_eq_mul] using h

/-- A weighted exponential sum over a probability weight vector is strictly positive. -/
theorem weighted_exp_sum_pos (w g : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1) :
    0 < ∑ x, w x * Real.exp (g x) :=
  lt_of_lt_of_le (Real.exp_pos _) (jensen_exp_weighted w g hw hsum)

/-- The reference mean of `-β Δ` is `-β` times the reference mean of `Δ`. -/
theorem weighted_sum_neg_mul (w Δ : Ω → ℝ) (β : ℝ) :
    ∑ x, w x * (-β * Δ x) = -β * ∑ x, w x * Δ x := by
  rw [Finset.mul_sum]
  exact Finset.sum_congr rfl fun x _ => by ring

/-- **T1 (Gibbs–Bogoliubov / Jensen lower bound).**  For a probability weight vector `w` and any
residual `Δ`, `-β ⟨Δ⟩₀ ≤ log (∑ x, w x * exp (-β Δ x)) = log (Z / Z₀)`. -/
theorem gibbs_bogoliubov (w Δ : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1) (β : ℝ) :
    -β * ∑ x, w x * Δ x ≤ Real.log (∑ x, w x * Real.exp (-β * Δ x)) := by
  have hJ := jensen_exp_weighted w (fun x => -β * Δ x) hw hsum
  have hpos := weighted_exp_sum_pos w (fun x => -β * Δ x) hw hsum
  rw [← weighted_sum_neg_mul]
  exact (Real.le_log_iff_exp_le hpos).mpr hJ

end Jensen

/-! ## T2. Hoeffding upper bound -/

section Hoeffding

variable {Ω : Type*} [Fintype Ω]

/-- **Hoeffding's lemma for finite weighted sums (core form).**  If `g` takes values in `[a, b]`
then its centred moment generating function at `1` is at most `exp ((b - a)² / 8)`.

The proof transfers `ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc` to the probability measure
`∑ x, w x • δ_x` on `Ω` equipped with the discrete σ-algebra. -/
theorem hoeffding_core (w g : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1) (a b : ℝ)
    (hg : ∀ x, a ≤ g x ∧ g x ≤ b) :
    ∑ x, w x * Real.exp (g x - ∑ y, w y * g y) ≤ Real.exp ((b - a) ^ 2 / 8) := by
  classical
  letI : MeasurableSpace Ω := ⊤
  haveI : MeasurableSingletonClass Ω := ⟨fun _ => MeasurableSpace.measurableSet_top⟩
  let μ : MeasureTheory.Measure Ω :=
    ∑ x, ENNReal.ofReal (w x) • MeasureTheory.Measure.dirac x
  -- integrals against `μ` are finite weighted sums
  have hint : ∀ f : Ω → ℝ, ∫ ω, f ω ∂μ = ∑ x, w x * f x := by
    intro f
    simp only [μ]
    rw [MeasureTheory.integral_finsetSum_measure]
    · refine Finset.sum_congr rfl fun x _ => ?_
      rw [MeasureTheory.integral_smul_measure, MeasureTheory.integral_dirac,
        ENNReal.toReal_ofReal (hw x), smul_eq_mul]
    · intro x _
      haveI := MeasureTheory.Measure.smul_finite (MeasureTheory.Measure.dirac x)
        (ENNReal.ofReal_ne_top (r := w x))
      exact MeasureTheory.Integrable.of_finite
  haveI : MeasureTheory.IsProbabilityMeasure μ := ⟨by
    simp only [μ, MeasureTheory.Measure.coe_finsetSum, Finset.sum_apply,
      MeasureTheory.Measure.smul_apply, MeasureTheory.measure_univ, smul_eq_mul, mul_one]
    rw [← ENNReal.ofReal_sum_of_nonneg (fun x _ => hw x), hsum, ENNReal.ofReal_one]⟩
  have hsub := ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc (μ := μ) (X := g) (a := a) (b := b)
    (measurable_of_finite g).aemeasurable
    (Filter.Eventually.of_forall fun x => ⟨(hg x).1, (hg x).2⟩)
  have h := hsub.mgf_le 1
  rw [ProbabilityTheory.mgf, hint, hint] at h
  simp only [one_mul] at h
  refine h.trans (le_of_eq ?_)
  congr 1
  simp only [NNReal.coe_pow, NNReal.coe_div, coe_nnnorm, Real.norm_eq_abs, NNReal.coe_ofNat]
  rw [div_pow, sq_abs]
  ring

/-- **Hoeffding's lemma, oscillation form.**  If any two values of `g` differ by at most `c`, the
centred moment generating function is at most `exp (c² / 8)`. -/
theorem hoeffding_core_osc (w g : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1) (c : ℝ)
    (hg : ∀ x x', |g x - g x'| ≤ c) :
    ∑ x, w x * Real.exp (g x - ∑ y, w y * g y) ≤ Real.exp (c ^ 2 / 8) := by
  have hne : Nonempty Ω := by
    by_contra h
    rw [not_nonempty_iff] at h
    rw [Finset.univ_eq_empty, Finset.sum_empty] at hsum
    exact zero_ne_one hsum
  obtain ⟨x₀, hx₀⟩ := Finite.exists_max g
  have h := hoeffding_core w g hw hsum (g x₀ - c) (g x₀)
    (fun x => ⟨by have := (abs_le.mp (hg x₀ x)).2; linarith, hx₀ x⟩)
  have e : (g x₀ - (g x₀ - c)) ^ 2 / 8 = c ^ 2 / 8 := by ring
  rwa [e] at h

/-- Centring a weighted exponential sum pulls out the factor `exp (-m)`. -/
theorem weighted_exp_centered_eq (w g : Ω → ℝ) (m : ℝ) :
    ∑ x, w x * Real.exp (g x - m) = Real.exp (-m) * ∑ x, w x * Real.exp (g x) := by
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [sub_eq_add_neg, Real.exp_add]
  ring

/-- A bound on the centred sum is the same as a bound on the uncentred sum. -/
theorem weighted_exp_centered_le_iff (w g : Ω → ℝ) (m K : ℝ) :
    ∑ x, w x * Real.exp (g x - m) ≤ Real.exp K ↔
      ∑ x, w x * Real.exp (g x) ≤ Real.exp (m + K) := by
  rw [weighted_exp_centered_eq, Real.exp_add, Real.exp_neg, inv_mul_le_iff₀ (Real.exp_pos m)]

/-- From a bound `exp K` on the centred moment generating function to the bound
`log (∑ x, w x * exp (g x)) ≤ ⟨g⟩ + K` on the log-partition ratio. -/
theorem log_weighted_exp_le_of_centered_le (w g : Ω → ℝ) (hw : ∀ x, 0 ≤ w x)
    (hsum : ∑ x, w x = 1) (K : ℝ)
    (h : ∑ x, w x * Real.exp (g x - ∑ y, w y * g y) ≤ Real.exp K) :
    Real.log (∑ x, w x * Real.exp (g x)) ≤ ∑ x, w x * g x + K := by
  rw [weighted_exp_centered_le_iff] at h
  have hpos := weighted_exp_sum_pos w g hw hsum
  calc Real.log (∑ x, w x * Real.exp (g x))
      ≤ Real.log (Real.exp (∑ x, w x * g x + K)) := Real.log_le_log hpos h
    _ = ∑ x, w x * g x + K := Real.log_exp _

/-- **T2 (Hoeffding upper bound).**  If the residual `Δ` takes values in `[a, b]` then
`log (Z / Z₀) ≤ -β ⟨Δ⟩₀ + β² (b - a)² / 8`, for every real `β`. -/
theorem hoeffding_upper (w Δ : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1) (a b : ℝ)
    (hΔ : ∀ x, a ≤ Δ x ∧ Δ x ≤ b) (β : ℝ) :
    Real.log (∑ x, w x * Real.exp (-β * Δ x)) ≤
      -β * ∑ x, w x * Δ x + β ^ 2 * (b - a) ^ 2 / 8 := by
  have hosc : ∀ x x', |(-β * Δ x) - (-β * Δ x')| ≤ |β| * (b - a) := by
    intro x x'
    have e : (-β * Δ x) - (-β * Δ x') = β * (Δ x' - Δ x) := by ring
    rw [e, abs_mul]
    refine mul_le_mul_of_nonneg_left ?_ (abs_nonneg β)
    rw [abs_le]
    constructor <;> linarith [(hΔ x).1, (hΔ x).2, (hΔ x').1, (hΔ x').2]
  have h := log_weighted_exp_le_of_centered_le w (fun x => -β * Δ x) hw hsum _
    (hoeffding_core_osc w (fun x => -β * Δ x) hw hsum (|β| * (b - a)) hosc)
  rw [weighted_sum_neg_mul] at h
  have e : (|β| * (b - a)) ^ 2 / 8 = β ^ 2 * (b - a) ^ 2 / 8 := by
    rw [mul_pow, sq_abs]
  rwa [e] at h

end Hoeffding

/-! ### General facts about the centred moment generating function -/

section CentredMGF

/-- The Jensen gap `log (∑ x, w x * exp (-β Δ x)) + β ⟨Δ⟩` is the logarithm of the centred
moment generating function of `-β Δ`. -/
theorem jensen_gap_eq_log_centered {Ω : Type*} [Fintype Ω] (w Δ : Ω → ℝ) (hw : ∀ x, 0 ≤ w x)
    (hsum : ∑ x, w x = 1) (β : ℝ) :
    Real.log (∑ x, w x * Real.exp (-β * Δ x)) + β * ∑ x, w x * Δ x =
      Real.log (∑ x, w x * Real.exp (-β * Δ x - ∑ y, w y * (-β * Δ y))) := by
  have h := weighted_exp_centered_eq w (fun x => -β * Δ x) (∑ y, w y * (-β * Δ y))
  rw [h, Real.log_mul (Real.exp_pos _).ne'
    (weighted_exp_sum_pos w (fun x => -β * Δ x) hw hsum).ne', Real.log_exp,
    weighted_sum_neg_mul]
  ring

/-- The centred moment generating function does not change when a constant is added. -/
theorem centered_mgf_shift {Ω : Type*} [Fintype Ω] (w : Ω → ℝ) (hsum : ∑ x, w x = 1)
    (g : Ω → ℝ) (k : ℝ) :
    ∑ x, w x * Real.exp ((g x - k) - ∑ y, w y * (g y - k)) =
      ∑ x, w x * Real.exp (g x - ∑ y, w y * g y) := by
  have e : ∑ y, w y * (g y - k) = ∑ y, w y * g y - k := by
    simp_rw [mul_sub]
    rw [Finset.sum_sub_distrib, ← Finset.sum_mul, hsum, one_mul]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [e]
  congr 2
  ring

/-- The centred moment generating function is a convex function of the observable. -/
theorem convexOn_centered_mgf {Ω : Type*} [Fintype Ω] (w : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) :
    ConvexOn ℝ Set.univ (fun g : Ω → ℝ => ∑ x, w x * Real.exp (g x - ∑ y, w y * g y)) := by
  refine ⟨convex_univ, fun g _ g' _ a b ha hb hab => ?_⟩
  simp only [smul_eq_mul, Finset.mul_sum]
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_le_sum fun x _ => ?_
  have hlin : (a • g + b • g') x - ∑ y, w y * (a • g + b • g') y =
      a * (g x - ∑ y, w y * g y) + b * (g' x - ∑ y, w y * g' y) := by
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, mul_add, Finset.sum_add_distrib]
    have e1 : ∑ y, w y * (a * g y) = a * ∑ y, w y * g y := by
      rw [Finset.mul_sum]
      exact Finset.sum_congr rfl fun y _ => by ring
    have e2 : ∑ y, w y * (b * g' y) = b * ∑ y, w y * g' y := by
      rw [Finset.mul_sum]
      exact Finset.sum_congr rfl fun y _ => by ring
    rw [e1, e2]
    ring
  rw [hlin]
  have hexp := convexOn_exp.2 (Set.mem_univ (g x - ∑ y, w y * g y))
    (Set.mem_univ (g' x - ∑ y, w y * g' y)) ha hb hab
  simp only [smul_eq_mul] at hexp
  calc w x * Real.exp (a * (g x - ∑ y, w y * g y) + b * (g' x - ∑ y, w y * g' y))
      ≤ w x * (a * Real.exp (g x - ∑ y, w y * g y) +
          b * Real.exp (g' x - ∑ y, w y * g' y)) := mul_le_mul_of_nonneg_left hexp (hw x)
    _ = a * (w x * Real.exp (g x - ∑ y, w y * g y)) +
          b * (w x * Real.exp (g' x - ∑ y, w y * g' y)) := by ring

end CentredMGF

/-! ## T3. The two-sided sandwich -/

section Sandwich

variable {Ω : Type*} [Fintype Ω]

/-- **T3 (free-energy sandwich, abstract weights).**
`-β ⟨Δ⟩₀ ≤ log (∑ x, w x * exp (-β Δ x)) ≤ -β ⟨Δ⟩₀ + β² (b - a)² / 8`. -/
theorem free_energy_sandwich (w Δ : Ω → ℝ) (hw : ∀ x, 0 ≤ w x) (hsum : ∑ x, w x = 1) (a b : ℝ)
    (hΔ : ∀ x, a ≤ Δ x ∧ Δ x ≤ b) (β : ℝ) :
    -β * ∑ x, w x * Δ x ≤ Real.log (∑ x, w x * Real.exp (-β * Δ x)) ∧
      Real.log (∑ x, w x * Real.exp (-β * Δ x)) ≤
        -β * ∑ x, w x * Δ x + β ^ 2 * (b - a) ^ 2 / 8 :=
  ⟨gibbs_bogoliubov w Δ hw hsum β, hoeffding_upper w Δ hw hsum a b hΔ β⟩

/-- The Boltzmann sum over a nonempty finite configuration space is positive. -/
theorem boltzmann_sum_pos [Nonempty Ω] (E : Ω → ℝ) (β : ℝ) :
    0 < ∑ x, Real.exp (-β * E x) :=
  Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty

/-- Boltzmann weights are nonnegative. -/
theorem gibbs_weight_nonneg (E : Ω → ℝ) (β : ℝ) (x : Ω) :
    0 ≤ Real.exp (-β * E x) / ∑ y, Real.exp (-β * E y) :=
  div_nonneg (Real.exp_pos _).le (Finset.sum_nonneg fun _ _ => (Real.exp_pos _).le)

/-- Boltzmann weights sum to one. -/
theorem gibbs_weight_sum_one [Nonempty Ω] (E : Ω → ℝ) (β : ℝ) :
    ∑ x, Real.exp (-β * E x) / ∑ y, Real.exp (-β * E y) = 1 := by
  rw [← Finset.sum_div]
  exact div_self (boltzmann_sum_pos E β).ne'

/-- The partition-function ratio is the reference average of `exp (-β Δ)`:
`Z / Z₀ = ∑ x, w x * exp (-β Δ x)` with `w x = exp (-β E₀ x) / Z₀`. -/
theorem partition_ratio_eq (E₀ Δ : Ω → ℝ) (β : ℝ) :
    (∑ x, Real.exp (-β * (E₀ x + Δ x))) / (∑ x, Real.exp (-β * E₀ x)) =
      ∑ x, (Real.exp (-β * E₀ x) / ∑ y, Real.exp (-β * E₀ y)) * Real.exp (-β * Δ x) := by
  rw [Finset.sum_div]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [mul_add, Real.exp_add]
  ring

/-- **T3 (partition-function form).**  With `Z₀ = ∑ x, exp (-β E₀ x)`,
`Z = ∑ x, exp (-β (E₀ x + Δ x))` and the reference mean
`⟨Δ⟩₀ = ∑ x, (exp (-β E₀ x) / Z₀) * Δ x`, if `a ≤ Δ ≤ b` then
`-β ⟨Δ⟩₀ ≤ log (Z / Z₀) ≤ -β ⟨Δ⟩₀ + β² (b - a)² / 8`. -/
theorem partition_ratio_sandwich [Nonempty Ω] (E₀ Δ : Ω → ℝ) (a b : ℝ)
    (hΔ : ∀ x, a ≤ Δ x ∧ Δ x ≤ b) (β : ℝ) :
    -β * ∑ x, (Real.exp (-β * E₀ x) / ∑ y, Real.exp (-β * E₀ y)) * Δ x ≤
        Real.log ((∑ x, Real.exp (-β * (E₀ x + Δ x))) / (∑ x, Real.exp (-β * E₀ x))) ∧
      Real.log ((∑ x, Real.exp (-β * (E₀ x + Δ x))) / (∑ x, Real.exp (-β * E₀ x))) ≤
        -β * ∑ x, (Real.exp (-β * E₀ x) / ∑ y, Real.exp (-β * E₀ y)) * Δ x +
          β ^ 2 * (b - a) ^ 2 / 8 := by
  rw [partition_ratio_eq]
  exact free_energy_sandwich _ Δ (gibbs_weight_nonneg E₀ β) (gibbs_weight_sum_one E₀ β) a b hΔ β

/-- **T3 (free-energy form).**  For `β > 0` and `F = -(1/β) log Z`, `F₀ = -(1/β) log Z₀`:
`⟨Δ⟩₀ - β (b - a)² / 8 ≤ F - F₀ ≤ ⟨Δ⟩₀`.  The right-hand inequality is the classical
Gibbs–Bogoliubov inequality; the left-hand one is its Hoeffding converse. -/
theorem free_energy_difference_sandwich [Nonempty Ω] (E₀ Δ : Ω → ℝ) (a b : ℝ)
    (hΔ : ∀ x, a ≤ Δ x ∧ Δ x ≤ b) (β : ℝ) (hβ : 0 < β) :
    (∑ x, (Real.exp (-β * E₀ x) / ∑ y, Real.exp (-β * E₀ y)) * Δ x) - β * (b - a) ^ 2 / 8 ≤
        -(1 / β) * Real.log (∑ x, Real.exp (-β * (E₀ x + Δ x))) -
          -(1 / β) * Real.log (∑ x, Real.exp (-β * E₀ x)) ∧
      -(1 / β) * Real.log (∑ x, Real.exp (-β * (E₀ x + Δ x))) -
          -(1 / β) * Real.log (∑ x, Real.exp (-β * E₀ x)) ≤
        ∑ x, (Real.exp (-β * E₀ x) / ∑ y, Real.exp (-β * E₀ y)) * Δ x := by
  obtain ⟨h1, h2⟩ := partition_ratio_sandwich E₀ Δ a b hΔ β
  have hZ := boltzmann_sum_pos (fun x => E₀ x + Δ x) β
  have hZ₀ := boltzmann_sum_pos E₀ β
  rw [Real.log_div hZ.ne' hZ₀.ne'] at h1 h2
  set L := Real.log (∑ x, Real.exp (-β * (E₀ x + Δ x))) - Real.log (∑ x, Real.exp (-β * E₀ x))
    with hL
  set M := ∑ x, (Real.exp (-β * E₀ x) / ∑ y, Real.exp (-β * E₀ y)) * Δ x with hM
  have e : -(1 / β) * Real.log (∑ x, Real.exp (-β * (E₀ x + Δ x))) -
      -(1 / β) * Real.log (∑ x, Real.exp (-β * E₀ x)) = -(L / β) := by
    rw [hL]
    ring
  rw [e]
  constructor
  · rw [le_neg, div_le_iff₀ hβ]
    have e' : -(M - β * (b - a) ^ 2 / 8) * β = -β * M + β ^ 2 * (b - a) ^ 2 / 8 := by ring
    rw [e']
    exact h2
  · rw [neg_le, le_div_iff₀ hβ]
    have e' : -M * β = -β * M := by ring
    rw [e']
    exact h1

end Sandwich

/-! ## T4. McDiarmid tensorization for product references -/

section Tensorization

/-- **Abstract two-factor step.**  Let `p` be weights on `Ω₁`, `q ≥ 0` weights on `Ω₂`, and
suppose that for every fixed `y` the slice `g (·, y)` has centred moment generating function at
most `B` under `p`.  Then integrating out the first factor costs at most the factor `B`:
`∑ x y, p x * q y * exp (g x y - m) ≤ B * ∑ y, q y * exp (gbar y - m)` where
`gbar y = ∑ x, p x * g x y`. -/
theorem two_factor_step {Ω₁ Ω₂ : Type*} [Fintype Ω₁] [Fintype Ω₂] (p : Ω₁ → ℝ) (q : Ω₂ → ℝ)
    (hq : ∀ y, 0 ≤ q y) (g : Ω₁ → Ω₂ → ℝ) (B : ℝ)
    (hB : ∀ y, ∑ x, p x * Real.exp (g x y - ∑ x', p x' * g x' y) ≤ B) (m : ℝ) :
    ∑ x, ∑ y, p x * q y * Real.exp (g x y - m) ≤
      B * ∑ y, q y * Real.exp (∑ x, p x * g x y - m) := by
  rw [Finset.sum_comm, Finset.mul_sum]
  refine Finset.sum_le_sum fun y _ => ?_
  have key : ∑ x, p x * q y * Real.exp (g x y - m) =
      (q y * Real.exp (∑ x, p x * g x y - m)) *
        ∑ x, p x * Real.exp (g x y - ∑ x', p x' * g x' y) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun x _ => ?_
    have e : g x y - m = (∑ x, p x * g x y - m) + (g x y - ∑ x', p x' * g x' y) := by ring
    rw [e, Real.exp_add]
    ring
  rw [key]
  calc (q y * Real.exp (∑ x, p x * g x y - m)) *
        ∑ x, p x * Real.exp (g x y - ∑ x', p x' * g x' y)
      ≤ (q y * Real.exp (∑ x, p x * g x y - m)) * B :=
        mul_le_mul_of_nonneg_left (hB y) (mul_nonneg (hq y) (Real.exp_pos _).le)
    _ = B * (q y * Real.exp (∑ x, p x * g x y - m)) := by ring

/-- **Two-factor Hoeffding step.**  If `p` is a probability weight vector on `Ω₁`, `q ≥ 0` on
`Ω₂`, and `g` changes by at most `c₁` when its first argument changes, then for every real `m`
`∑ x y, p x * q y * exp (g x y - m) ≤ exp (c₁² / 8) * ∑ y, q y * exp (gbar y - m)`. -/
theorem two_factor_tensorization {Ω₁ Ω₂ : Type*} [Fintype Ω₁] [Fintype Ω₂] (p : Ω₁ → ℝ)
    (q : Ω₂ → ℝ) (hp : ∀ x, 0 ≤ p x) (hp1 : ∑ x, p x = 1) (hq : ∀ y, 0 ≤ q y)
    (g : Ω₁ → Ω₂ → ℝ) (c₁ : ℝ) (hg : ∀ x x' y, |g x y - g x' y| ≤ c₁) (m : ℝ) :
    ∑ x, ∑ y, p x * q y * Real.exp (g x y - m) ≤
      Real.exp (c₁ ^ 2 / 8) * ∑ y, q y * Real.exp (∑ x, p x * g x y - m) :=
  two_factor_step p q hq g _
    (fun y => hoeffding_core_osc p (fun x => g x y) hp hp1 c₁ (fun x x' => hg x x' y)) m

/-- Splitting a sum over configurations of `n + 1` sites into the first site and the rest. -/
theorem sum_config_succ {n : ℕ} {σ : Fin (n + 1) → Type*} [∀ i, Fintype (σ i)]
    (f : (∀ i, σ i) → ℝ) :
    ∑ x, f x = ∑ a : σ 0, ∑ y : ∀ i : Fin n, σ i.succ, f (Fin.cons a y) := by
  rw [← Fintype.sum_prod_type (fun z : σ 0 × (∀ i : Fin n, σ i.succ) => f (Fin.cons z.1 z.2))]
  exact (Equiv.sum_comp (Fin.consEquiv σ) f).symm

/-- The product weight of `Fin.cons a y` factors as (site `0`) × (remaining sites). -/
theorem prod_weight_cons {n : ℕ} {σ : Fin (n + 1) → Type*} (p : ∀ i, σ i → ℝ) (a : σ 0)
    (y : ∀ i : Fin n, σ i.succ) :
    ∏ i, p i ((Fin.cons a y : ∀ i, σ i) i) = p 0 a * ∏ i : Fin n, p i.succ (y i) := by
  rw [Fin.prod_univ_succ]
  simp only [Fin.cons_zero, Fin.cons_succ]

/-- Product weights are nonnegative. -/
theorem prod_weight_nonneg {α : Type*} {n : ℕ} (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (x : Fin n → α) : 0 ≤ ∏ i, p i (x i) :=
  Finset.prod_nonneg fun i _ => hp i (x i)

/-- Multiplying a residual by `-β` multiplies its bounded-difference constants by `|β|`. -/
theorem neg_mul_bounded_differences {α : Type*} {n : ℕ} (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β : ℝ) (x : Fin n → α)
    (i : Fin n) (a : α) :
    |(-β * Δ (Function.update x i a)) - (-β * Δ x)| ≤ |β| * c i := by
  have e : (-β * Δ (Function.update x i a)) - (-β * Δ x) =
      -β * (Δ (Function.update x i a) - Δ x) := by ring
  rw [e, abs_mul, abs_neg]
  exact mul_le_mul_of_nonneg_left (hΔ x i a) (abs_nonneg β)

/-- Induction engine for `bounded_differences_tensorization` and
`bounded_differences_tensorization_pi`, stated for site-dependent alphabets `σ i` so that the
induction hypothesis applies to the tail `fun i => σ i.succ`. -/
theorem bounded_differences_tensorization_aux :
    ∀ (n : ℕ) (σ : Fin n → Type*) [∀ i, Fintype (σ i)] (p : ∀ i, σ i → ℝ),
    (∀ i a, 0 ≤ p i a) → (∀ i, ∑ a, p i a = 1) →
    ∀ (c B : Fin n → ℝ), (∀ i, 0 ≤ B i) →
    (∀ i (h : σ i → ℝ), (∀ a a', |h a - h a'| ≤ c i) →
      ∑ a, p i a * Real.exp (h a - ∑ a', p i a' * h a') ≤ B i) →
    ∀ (g : (∀ i, σ i) → ℝ), (∀ x i a, |g (Function.update x i a) - g x| ≤ c i) → ∀ m : ℝ,
    ∑ x, (∏ i, p i (x i)) * Real.exp (g x - m) ≤
      (∏ i, B i) * Real.exp (∑ x, (∏ i, p i (x i)) * g x - m) := by
  intro n
  induction n with
  | zero =>
    intro σ _ p _ _ c B _ _ g _ m
    simp
  | succ n ih =>
    intro σ _ p hp hp1 c B hB0 hB g hg m
    have hq0 : ∀ y : ∀ i : Fin n, σ i.succ, 0 ≤ ∏ i : Fin n, p i.succ (y i) :=
      fun y => Finset.prod_nonneg fun i _ => hp i.succ (y i)
    -- the left-hand side as an iterated sum over the first site and the remaining sites
    have hL : ∑ x, (∏ i, p i (x i)) * Real.exp (g x - m) =
        ∑ a, ∑ y : ∀ i : Fin n, σ i.succ, p 0 a * (∏ i : Fin n, p i.succ (y i)) *
          Real.exp (g (Fin.cons a y) - m) := by
      rw [sum_config_succ]
      refine Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun y _ => ?_
      rw [prod_weight_cons]
    -- the mean of `g` is the mean of its site-0 average
    have hM : ∑ x, (∏ i, p i (x i)) * g x =
        ∑ y : ∀ i : Fin n, σ i.succ, (∏ i : Fin n, p i.succ (y i)) *
          ∑ a, p 0 a * g (Fin.cons a y) := by
      rw [sum_config_succ, Finset.sum_comm]
      refine Finset.sum_congr rfl fun y _ => ?_
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl fun a _ => ?_
      rw [prod_weight_cons]
      ring
    -- one single-site step in the first coordinate
    have h2 := two_factor_step (p 0)
      (fun y : ∀ i : Fin n, σ i.succ => ∏ i : Fin n, p i.succ (y i)) hq0
      (fun a y => g (Fin.cons a y)) (B 0)
      (fun y => hB 0 (fun a => g (Fin.cons a y)) (fun a a' => by
        have h := hg (Fin.cons a' y) 0 a
        rwa [Fin.update_cons_zero] at h)) m
    -- the site-0 average still has bounded differences
    have hgb : ∀ (y : ∀ i : Fin n, σ i.succ) (i : Fin n) (b : σ i.succ),
        |(∑ a, p 0 a * g (Fin.cons a (Function.update y i b))) -
          ∑ a, p 0 a * g (Fin.cons a y)| ≤ c i.succ := by
      intro y i b
      rw [← Finset.sum_sub_distrib]
      calc |∑ a, (p 0 a * g (Fin.cons a (Function.update y i b)) - p 0 a * g (Fin.cons a y))|
          ≤ ∑ a, |p 0 a * g (Fin.cons a (Function.update y i b)) - p 0 a * g (Fin.cons a y)| :=
            Finset.abs_sum_le_sum_abs _ _
        _ ≤ ∑ a, p 0 a * c i.succ := by
            refine Finset.sum_le_sum fun a _ => ?_
            rw [← mul_sub, abs_mul, abs_of_nonneg (hp 0 a)]
            refine mul_le_mul_of_nonneg_left ?_ (hp 0 a)
            have h := hg (Fin.cons a y) i.succ b
            rwa [← Fin.cons_update] at h
        _ = c i.succ := by rw [← Finset.sum_mul, hp1 0, one_mul]
    have hih := ih (fun i => σ i.succ) (fun i => p i.succ) (fun i a => hp i.succ a)
      (fun i => hp1 i.succ) (fun i => c i.succ) (fun i => B i.succ) (fun i => hB0 i.succ)
      (fun i => hB i.succ) (fun y => ∑ a, p 0 a * g (Fin.cons a y)) hgb m
    rw [hL, hM]
    calc ∑ a, ∑ y : ∀ i : Fin n, σ i.succ, p 0 a * (∏ i : Fin n, p i.succ (y i)) *
          Real.exp (g (Fin.cons a y) - m)
        ≤ B 0 * ∑ y : ∀ i : Fin n, σ i.succ, (∏ i : Fin n, p i.succ (y i)) *
            Real.exp (∑ a, p 0 a * g (Fin.cons a y) - m) := h2
      _ ≤ B 0 * ((∏ i : Fin n, B i.succ) *
            Real.exp (∑ y : ∀ i : Fin n, σ i.succ, (∏ i : Fin n, p i.succ (y i)) *
              ∑ a, p 0 a * g (Fin.cons a y) - m)) :=
          mul_le_mul_of_nonneg_left hih (hB0 0)
      _ = (∏ i, B i) *
            Real.exp (∑ y : ∀ i : Fin n, σ i.succ, (∏ i : Fin n, p i.succ (y i)) *
              ∑ a, p 0 a * g (Fin.cons a y) - m) := by
          rw [Fin.prod_univ_succ, mul_assoc]

variable {α : Type*} [Fintype α] {n : ℕ}

/-- **Tensorization of single-site bounds under bounded differences.**  Let
`W x = ∏ i, p i (x i)` be a product reference on `Fin n → α`.  Suppose that at each site `i`
every site function `h : α → ℝ` of oscillation at most `c i` has centred moment generating
function at most `B i` under `p i`.  Then every `g` with bounded differences `c` satisfies
`∑ x, W x * exp (g x - m) ≤ (∏ i, B i) * exp (⟨g⟩ - m)` for every real `m`. -/
theorem bounded_differences_tensorization (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (c B : Fin n → ℝ) (hB0 : ∀ i, 0 ≤ B i)
    (hB : ∀ i (h : α → ℝ), (∀ a a', |h a - h a'| ≤ c i) →
      ∑ a, p i a * Real.exp (h a - ∑ a', p i a' * h a') ≤ B i)
    (g : (Fin n → α) → ℝ) (hg : ∀ x i a, |g (Function.update x i a) - g x| ≤ c i) (m : ℝ) :
    ∑ x, (∏ i, p i (x i)) * Real.exp (g x - m) ≤
      (∏ i, B i) * Real.exp (∑ x, (∏ i, p i (x i)) * g x - m) :=
  bounded_differences_tensorization_aux n (fun _ => α) p hp hp1 c B hB0 hB g hg m

/-- Product weights of normalised site marginals sum to one. -/
theorem prod_weight_sum_one (p : Fin n → α → ℝ) (hp1 : ∀ i, ∑ a, p i a = 1) :
    ∑ x : Fin n → α, ∏ i, p i (x i) = 1 := by
  rw [← Fintype.prod_sum]
  exact Finset.prod_eq_one fun i _ => hp1 i

/-- McDiarmid tensorization with an arbitrary centring constant `m`. -/
theorem mcdiarmid_mgf_centered (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (g : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hg : ∀ x i a, |g (Function.update x i a) - g x| ≤ c i) (m : ℝ) :
    ∑ x, (∏ i, p i (x i)) * Real.exp (g x - m) ≤
      Real.exp ((∑ i, c i ^ 2) / 8) * Real.exp (∑ x, (∏ i, p i (x i)) * g x - m) := by
  have h := bounded_differences_tensorization p hp hp1 c (fun i => Real.exp (c i ^ 2 / 8))
    (fun i => (Real.exp_pos _).le)
    (fun i h hh => hoeffding_core_osc (p i) h (hp i) (hp1 i) (c i) hh) g hg m
  rwa [← Real.exp_sum, ← Finset.sum_div] at h

/-- **T4 (McDiarmid tensorization, the bounded-differences bound).**  For a product reference
`W x = ∏ i, p i (x i)` on `Fin n → α` and a residual `g` with bounded differences
`|g (update x i a) - g x| ≤ c i`, the centred moment generating function satisfies
`∑ x, W x * exp (g x - ⟨g⟩) ≤ exp ((∑ i, (c i)²) / 8)`. -/
theorem mcdiarmid_mgf (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1)
    (g : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hg : ∀ x i a, |g (Function.update x i a) - g x| ≤ c i) :
    ∑ x, (∏ i, p i (x i)) * Real.exp (g x - ∑ y, (∏ i, p i (y i)) * g y) ≤
      Real.exp ((∑ i, c i ^ 2) / 8) := by
  have h := mcdiarmid_mgf_centered p hp hp1 g c hg (∑ y, (∏ i, p i (y i)) * g y)
  rwa [sub_self, Real.exp_zero, mul_one] at h

/-- **T4 (`Δ`, `β` form).**  For a product reference and a residual `Δ` with bounded differences
`c`, `log (∑ x, W x * exp (-β Δ x)) ≤ -β ⟨Δ⟩ + β² (∑ i, (c i)²) / 8`. -/
theorem mcdiarmid_log_upper (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β : ℝ) :
    Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
      -β * ∑ x, (∏ i, p i (x i)) * Δ x + β ^ 2 * (∑ i, c i ^ 2) / 8 := by
  have h := log_weighted_exp_le_of_centered_le (fun x : Fin n → α => ∏ i, p i (x i))
    (fun x => -β * Δ x) (prod_weight_nonneg p hp) (prod_weight_sum_one p hp1) _
    (mcdiarmid_mgf p hp hp1 (fun x => -β * Δ x) (fun i => |β| * c i)
      (neg_mul_bounded_differences Δ c hΔ β))
  rw [weighted_sum_neg_mul] at h
  have e : (∑ i, (|β| * c i) ^ 2) / 8 = β ^ 2 * (∑ i, c i ^ 2) / 8 := by
    rw [Finset.mul_sum]
    congr 1
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [mul_pow, sq_abs]
  rwa [e] at h

/-- **T4 (bounded-differences sandwich).**  For a product reference and a residual with bounded
differences `c`:
`-β ⟨Δ⟩ ≤ log (∑ x, W x * exp (-β Δ x)) ≤ -β ⟨Δ⟩ + β² (∑ i, (c i)²) / 8`. -/
theorem bounded_differences_sandwich (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β : ℝ) :
    -β * ∑ x, (∏ i, p i (x i)) * Δ x ≤
        Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
      Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
        -β * ∑ x, (∏ i, p i (x i)) * Δ x + β ^ 2 * (∑ i, c i ^ 2) / 8 :=
  ⟨gibbs_bogoliubov (fun x : Fin n → α => ∏ i, p i (x i)) Δ (prod_weight_nonneg p hp)
      (prod_weight_sum_one p hp1) β,
    mcdiarmid_log_upper p hp hp1 Δ c hΔ β⟩

end Tensorization

/-! ## T4 for arbitrary site index types and heterogeneous site alphabets -/

section GeneralIndex

variable {ι : Type*} [Fintype ι] [DecidableEq ι] {σ : ι → Type*} [∀ i, Fintype (σ i)]

/-- **Tensorization of single-site bounds, general form.**  The statement of
`bounded_differences_tensorization` for configurations `x : ∀ i, σ i` with an arbitrary finite
site index type `ι` and site-dependent alphabets `σ i` (a heteropolymer: every site has its own
state space). -/
theorem bounded_differences_tensorization_pi (p : ∀ i, σ i → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (c B : ι → ℝ) (hB0 : ∀ i, 0 ≤ B i)
    (hB : ∀ i (h : σ i → ℝ), (∀ a a', |h a - h a'| ≤ c i) →
      ∑ a, p i a * Real.exp (h a - ∑ a', p i a' * h a') ≤ B i)
    (g : (∀ i, σ i) → ℝ) (hg : ∀ x i a, |g (Function.update x i a) - g x| ≤ c i) (m : ℝ) :
    ∑ x, (∏ i, p i (x i)) * Real.exp (g x - m) ≤
      (∏ i, B i) * Real.exp (∑ x, (∏ i, p i (x i)) * g x - m) := by
  -- transport everything along an enumeration `e` of the sites
  obtain ⟨e⟩ : Nonempty (ι ≃ Fin (Fintype.card ι)) := ⟨Fintype.equivFin ι⟩
  have hW : ∀ x : ∀ i, σ i, ∏ i, p i (x i) = ∏ k, p (e.symm k) (e.piCongrLeft' σ x k) :=
    fun x => (Equiv.prod_comp e.symm (fun i => p i (x i))).symm
  have hL : ∑ x, (∏ i, p i (x i)) * Real.exp (g x - m) =
      ∑ y : ∀ k, σ (e.symm k), (∏ k, p (e.symm k) (y k)) *
        Real.exp (g ((e.piCongrLeft' σ).symm y) - m) :=
    Fintype.sum_equiv (e.piCongrLeft' σ) _ _
      (fun x => by simp only [hW x, Equiv.symm_apply_apply])
  have hM : ∑ x, (∏ i, p i (x i)) * g x =
      ∑ y : ∀ k, σ (e.symm k), (∏ k, p (e.symm k) (y k)) * g ((e.piCongrLeft' σ).symm y) :=
    Fintype.sum_equiv (e.piCongrLeft' σ) _ _
      (fun x => by simp only [hW x, Equiv.symm_apply_apply])
  have hBprod : ∏ i, B i = ∏ k, B (e.symm k) := (Equiv.prod_comp e.symm B).symm
  have h := bounded_differences_tensorization_aux (Fintype.card ι) (fun k => σ (e.symm k))
    (fun k => p (e.symm k)) (fun k a => hp (e.symm k) a) (fun k => hp1 (e.symm k))
    (fun k => c (e.symm k)) (fun k => B (e.symm k)) (fun k => hB0 (e.symm k))
    (fun k h hh => hB (e.symm k) h hh) (fun y => g ((e.piCongrLeft' σ).symm y))
    (fun y k a => by
      have h1 := hg ((e.piCongrLeft' σ).symm y) (e.symm k) a
      rwa [← Function.piCongrLeft'_symm_update] at h1) m
  rw [hL, hM, hBprod]
  exact h

/-- Product weights of normalised site marginals sum to one (general index type). -/
theorem prod_weight_sum_one_pi (p : ∀ i, σ i → ℝ) (hp1 : ∀ i, ∑ a, p i a = 1) :
    ∑ x : ∀ i, σ i, ∏ i, p i (x i) = 1 := by
  rw [← Fintype.prod_sum]
  exact Finset.prod_eq_one fun i _ => hp1 i

/-- **T4, general form (McDiarmid tensorization).**  For an arbitrary finite site index type
`ι`, site-dependent alphabets `σ i`, a product reference `W x = ∏ i, p i (x i)` on `∀ i, σ i`
and a residual `g` with bounded differences `c`:
`∑ x, W x * exp (g x - ⟨g⟩) ≤ exp ((∑ i, (c i)²) / 8)`. -/
theorem mcdiarmid_mgf_pi (p : ∀ i, σ i → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (g : (∀ i, σ i) → ℝ) (c : ι → ℝ)
    (hg : ∀ x i a, |g (Function.update x i a) - g x| ≤ c i) :
    ∑ x, (∏ i, p i (x i)) * Real.exp (g x - ∑ y, (∏ i, p i (y i)) * g y) ≤
      Real.exp ((∑ i, c i ^ 2) / 8) := by
  have h := bounded_differences_tensorization_pi p hp hp1 c (fun i => Real.exp (c i ^ 2 / 8))
    (fun i => (Real.exp_pos _).le)
    (fun i h hh => hoeffding_core_osc (p i) h (hp i) (hp1 i) (c i) hh) g hg
    (∑ y, (∏ i, p i (y i)) * g y)
  rwa [sub_self, Real.exp_zero, mul_one, ← Real.exp_sum, ← Finset.sum_div] at h

/-- **T4, general form (bounded-differences sandwich).**  For an arbitrary finite site index
type `ι`, site-dependent alphabets `σ i`, a product reference `W x = ∏ i, p i (x i)` and a
residual `Δ` with bounded differences `c`:
`-β ⟨Δ⟩ ≤ log (∑ x, W x * exp (-β Δ x)) ≤ -β ⟨Δ⟩ + β² (∑ i, (c i)²) / 8`. -/
theorem bounded_differences_sandwich_pi (p : ∀ i, σ i → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (∀ i, σ i) → ℝ) (c : ι → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β : ℝ) :
    -β * ∑ x, (∏ i, p i (x i)) * Δ x ≤
        Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
      Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
        -β * ∑ x, (∏ i, p i (x i)) * Δ x + β ^ 2 * (∑ i, c i ^ 2) / 8 := by
  have hW0 : ∀ x : ∀ i, σ i, 0 ≤ ∏ i, p i (x i) :=
    fun x => Finset.prod_nonneg fun i _ => hp i (x i)
  have hW1 := prod_weight_sum_one_pi p hp1
  refine ⟨gibbs_bogoliubov (fun x : ∀ i, σ i => ∏ i, p i (x i)) Δ hW0 hW1 β, ?_⟩
  have hbd : ∀ (x : ∀ i, σ i) (i : ι) (a : σ i),
      |(-β * Δ (Function.update x i a)) - (-β * Δ x)| ≤ |β| * c i := by
    intro x i a
    have e : (-β * Δ (Function.update x i a)) - (-β * Δ x) =
        -β * (Δ (Function.update x i a) - Δ x) := by ring
    rw [e, abs_mul, abs_neg]
    exact mul_le_mul_of_nonneg_left (hΔ x i a) (abs_nonneg β)
  have h := log_weighted_exp_le_of_centered_le (fun x : ∀ i, σ i => ∏ i, p i (x i))
    (fun x => -β * Δ x) hW0 hW1 _
    (mcdiarmid_mgf_pi p hp hp1 (fun x => -β * Δ x) (fun i => |β| * c i) hbd)
  rw [weighted_sum_neg_mul] at h
  have e : (∑ i, (|β| * c i) ^ 2) / 8 = β ^ 2 * (∑ i, c i ^ 2) / 8 := by
    rw [Finset.mul_sum]
    congr 1
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [mul_pow, sq_abs]
  rwa [e] at h

end GeneralIndex

/-! ## T5. Sharpness: the worst residual is additive and two-level -/

section Sharpness

/-! ### Additive residuals factorise exactly -/

/-- The exponential moment of an additive function under a product weight is the product of the
single-site exponential moments. -/
theorem product_additive_mgf {α : Type*} [Fintype α] {n : ℕ} (p f : Fin n → α → ℝ) :
    ∑ x : Fin n → α, (∏ i, p i (x i)) * Real.exp (∑ i, f i (x i)) =
      ∏ i, ∑ a, p i a * Real.exp (f i a) := by
  rw [Fintype.prod_sum]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [Real.exp_sum, Finset.prod_mul_distrib]

/-- The mean of an additive function under a product of normalised site marginals is the sum of
the single-site means. -/
theorem product_additive_mean {α : Type*} [Fintype α] {n : ℕ} (p : Fin n → α → ℝ)
    (hp1 : ∀ i, ∑ a, p i a = 1) (f : Fin n → α → ℝ) :
    ∑ x : Fin n → α, (∏ i, p i (x i)) * ∑ i, f i (x i) = ∑ i, ∑ a, p i a * f i a := by
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => ?_
  have h1 : ∀ x : Fin n → α, (∏ j, p j (x j)) * f i (x i) =
      ∏ j, (p j (x j) * (if j = i then f i (x j) else 1)) := by
    intro x
    rw [Finset.prod_mul_distrib, Finset.prod_ite_eq' Finset.univ i (fun j => f i (x j))]
    simp
  simp_rw [h1]
  rw [← Fintype.prod_sum (fun j a => p j a * (if j = i then f i a else 1))]
  rw [Finset.prod_eq_single i]
  · simp
  · intro j _ hj
    simp [hj, hp1 j]
  · intro h
    exact absurd (Finset.mem_univ i) h

/-- For an additive residual `Δ x = ∑ i, δ i (x i)` and a product reference, the log-partition
ratio is the sum of the single-site log-partition ratios. -/
theorem additive_log_mgf {α : Type*} [Fintype α] {n : ℕ} (p : Fin n → α → ℝ)
    (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1) (δ : Fin n → α → ℝ) (β : ℝ) :
    Real.log (∑ x : Fin n → α, (∏ i, p i (x i)) * Real.exp (-β * ∑ i, δ i (x i))) =
      ∑ i, Real.log (∑ a, p i a * Real.exp (-β * δ i a)) := by
  have e : ∀ x : Fin n → α, -β * ∑ i, δ i (x i) = ∑ i, (-β * δ i (x i)) :=
    fun x => Finset.mul_sum _ _ _
  simp_rw [e]
  rw [product_additive_mgf p (fun i a => -β * δ i a), Real.log_prod]
  intro i _
  exact (weighted_exp_sum_pos (p i) (fun a => -β * δ i a) (hp i) (hp1 i)).ne'

/-- **T5 (additive residuals: the Jensen gap is additive).**  For `Δ x = ∑ i, δ i (x i)` and a
product reference, `log (∑ x, W x * exp (-β Δ x)) + β ⟨Δ⟩` is exactly the sum over the sites of
the single-site gaps `log (∑ a, p i a * exp (-β δ i a)) + β ∑ a, p i a * δ i a`. -/
theorem additive_gap_eq {α : Type*} [Fintype α] {n : ℕ} (p : Fin n → α → ℝ)
    (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1) (δ : Fin n → α → ℝ) (β : ℝ) :
    Real.log (∑ x : Fin n → α, (∏ i, p i (x i)) * Real.exp (-β * ∑ i, δ i (x i))) +
        β * ∑ x : Fin n → α, (∏ i, p i (x i)) * ∑ i, δ i (x i) =
      ∑ i, (Real.log (∑ a, p i a * Real.exp (-β * δ i a)) + β * ∑ a, p i a * δ i a) := by
  rw [additive_log_mgf p hp hp1, product_additive_mean p hp1, Finset.sum_add_distrib,
    Finset.mul_sum]

/-- An additive function whose site terms have oscillation at most `c i` has bounded
differences `c`: additive residuals belong to the bounded-difference class. -/
theorem additive_bounded_differences {α : Type*} {n : ℕ} (δ : Fin n → α → ℝ) (c : Fin n → ℝ)
    (hδ : ∀ i a b, |δ i a - δ i b| ≤ c i) (x : Fin n → α) (i : Fin n) (a : α) :
    |(∑ j, δ j (Function.update x i a j)) - ∑ j, δ j (x j)| ≤ c i := by
  rw [← Finset.sum_sub_distrib, Finset.sum_eq_single i]
  · rw [Function.update_self]
    exact hδ i a (x i)
  · intro j _ hj
    rw [Function.update_of_ne hj]
    exact sub_self _
  · intro h
    exact absurd (Finset.mem_univ i) h

/-- The constants of a bounded-difference hypothesis are automatically nonnegative. -/
theorem bounded_differences_nonneg {α : Type*} [Nonempty α] {n : ℕ} (g : (Fin n → α) → ℝ)
    (c : Fin n → ℝ) (hg : ∀ x i a, |g (Function.update x i a) - g x| ≤ c i) (i : Fin n) :
    0 ≤ c i :=
  (abs_nonneg _).trans (hg (fun _ => Classical.arbitrary α) i (Classical.arbitrary α))

/-- The centred moment generating function of an additive function under a product reference is
the product of the single-site centred moment generating functions. -/
theorem additive_centered_mgf {α : Type*} [Fintype α] {n : ℕ} (p : Fin n → α → ℝ)
    (hp1 : ∀ i, ∑ a, p i a = 1) (f : Fin n → α → ℝ) :
    ∑ x : Fin n → α, (∏ i, p i (x i)) *
        Real.exp ((∑ i, f i (x i)) - ∑ y : Fin n → α, (∏ i, p i (y i)) * ∑ i, f i (y i)) =
      ∏ i, ∑ a, p i a * Real.exp (f i a - ∑ a', p i a' * f i a') := by
  rw [product_additive_mean p hp1 f]
  have e : ∀ x : Fin n → α, (∑ i, f i (x i)) - ∑ i, ∑ a, p i a * f i a =
      ∑ i, (f i (x i) - ∑ a, p i a * f i a) := fun x => (Finset.sum_sub_distrib _ _).symm
  simp_rw [e]
  exact product_additive_mgf p (fun i a => f i a - ∑ a', p i a' * f i a')

/-- **T5 (the worst case is decomposable).**  Let `f i : α → ℝ` be, at every site `i`, a
worst-case site residual: it maximises the single-site centred moment generating function among
all site functions of oscillation at most `c i`.  Then the *additive* residual
`x ↦ ∑ i, f i (x i)` maximises the centred moment generating function among **all** residuals
with bounded differences `c`, decomposable or not. -/
theorem additive_extremal {α : Type*} [Fintype α] {n : ℕ} (p : Fin n → α → ℝ)
    (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1) (c : Fin n → ℝ) (f : Fin n → α → ℝ)
    (hf : ∀ i (h : α → ℝ), (∀ a a', |h a - h a'| ≤ c i) →
      ∑ a, p i a * Real.exp (h a - ∑ a', p i a' * h a') ≤
        ∑ a, p i a * Real.exp (f i a - ∑ a', p i a' * f i a'))
    (g : (Fin n → α) → ℝ) (hg : ∀ x i a, |g (Function.update x i a) - g x| ≤ c i) :
    ∑ x, (∏ i, p i (x i)) * Real.exp (g x - ∑ y, (∏ i, p i (y i)) * g y) ≤
      ∑ x : Fin n → α, (∏ i, p i (x i)) *
        Real.exp ((∑ i, f i (x i)) - ∑ y : Fin n → α, (∏ i, p i (y i)) * ∑ i, f i (y i)) := by
  rw [additive_centered_mgf p hp1 f]
  have h := bounded_differences_tensorization p hp hp1 c
    (fun i => ∑ a, p i a * Real.exp (f i a - ∑ a', p i a' * f i a'))
    (fun i => Finset.sum_nonneg fun a _ => mul_nonneg (hp i a) (Real.exp_pos _).le) hf g hg
    (∑ y, (∏ i, p i (y i)) * g y)
  rwa [sub_self, Real.exp_zero, mul_one] at h

/-! ### The worst case is additive and two-level, for every product reference -/

/-- **Two-level site extremality.**  For a probability weight vector `p` on a finite type and
`c ≥ 0` there is a subset of states (encoded by `s : α → Bool`) whose scaled indicator
`a ↦ c * [s a]` maximises the centred moment generating function among all site functions of
oscillation at most `c`.  (The functional is convex, so its maximum over the cube `[0, c]^α` is
attained at a vertex.) -/
theorem exists_two_level_site_extremal {α : Type*} [Fintype α] (p : α → ℝ) (hp : ∀ a, 0 ≤ p a)
    (hp1 : ∑ a, p a = 1) (c : ℝ) (hc : 0 ≤ c) :
    ∃ s : α → Bool, ∀ h : α → ℝ, (∀ a b, |h a - h b| ≤ c) →
      ∑ a, p a * Real.exp (h a - ∑ a', p a' * h a') ≤
        ∑ a, p a * Real.exp ((if s a then c else 0) - ∑ a', p a' * (if s a' then c else 0)) := by
  classical
  have hne : Nonempty α := by
    by_contra h
    rw [not_nonempty_iff] at h
    rw [Finset.univ_eq_empty, Finset.sum_empty] at hp1
    exact zero_ne_one hp1
  -- the best vertex of the cube
  obtain ⟨s, hs⟩ := Finite.exists_max (fun s : α → Bool =>
    ∑ a, p a * Real.exp ((if s a then c else 0) - ∑ a', p a' * (if s a' then c else 0)))
  refine ⟨s, fun h hh => ?_⟩
  -- shift `h` into the cube `[0, c]^α`, the convex hull of its vertices
  obtain ⟨a₁, ha₁⟩ := Finite.exists_min h
  have hhull : (fun a => h a - h a₁) ∈
      convexHull ℝ (Set.univ.pi fun _ : α => ({0, c} : Set ℝ)) := by
    rw [convexHull_pi]
    intro a _
    show h a - h a₁ ∈ convexHull ℝ {0, c}
    rw [convexHull_pair, segment_eq_Icc hc]
    exact ⟨sub_nonneg.mpr (ha₁ a), by have := (abs_le.mp (hh a a₁)).2; linarith⟩
  -- maximum principle for convex functions: some vertex `v` is at least as good
  obtain ⟨v, hv, hle⟩ := (convexOn_centered_mgf p hp).exists_ge_of_mem_convexHull
    (Set.subset_univ _) hhull
  have hv' : v = fun a => if decide (v a = c) then c else 0 := by
    funext a
    have h1 := hv a (Set.mem_univ a)
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at h1
    rcases h1 with h0 | hc'
    · simp [h0]
    · simp [hc']
  have h3 := hs (fun a => decide (v a = c))
  beta_reduce at hle h3
  rw [centered_mgf_shift p hp1 h (h a₁)] at hle
  rw [hv'] at hle
  exact hle.trans h3

/-- **T5 (the worst case is additive and two-level, moment generating function form).**  For
every product reference on `Fin n → α` and all constants `c i ≥ 0` there are subsets of site
states (encoded by `s i : α → Bool`) such that the additive two-level residual
`x ↦ ∑ i, c i * [s i (x i)]` maximises the centred moment generating function among **all**
residuals with bounded differences `c`. -/
theorem exists_two_level_additive_extremal {α : Type*} [Fintype α] {n : ℕ}
    (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1) (c : Fin n → ℝ)
    (hc : ∀ i, 0 ≤ c i) :
    ∃ s : Fin n → α → Bool,
      ∀ g : (Fin n → α) → ℝ, (∀ x i a, |g (Function.update x i a) - g x| ≤ c i) →
        ∑ x, (∏ i, p i (x i)) * Real.exp (g x - ∑ y, (∏ i, p i (y i)) * g y) ≤
          ∑ x : Fin n → α, (∏ i, p i (x i)) *
            Real.exp ((∑ i, (if s i (x i) then c i else 0)) -
              ∑ y : Fin n → α, (∏ i, p i (y i)) * ∑ i, (if s i (y i) then c i else 0)) := by
  choose s hs using fun i => exists_two_level_site_extremal (p i) (hp i) (hp1 i) (c i) (hc i)
  exact ⟨s, fun g hg =>
    additive_extremal p hp hp1 c (fun i a => if s i a then c i else 0) hs g hg⟩

/-- An additive two-level residual `x ↦ ∑ i, c i * [s i (x i)]` with `c i ≥ 0` has bounded
differences `c`. -/
theorem two_level_set_bounded_differences {α : Type*} {n : ℕ} (s : Fin n → α → Bool)
    (c : Fin n → ℝ) (hc : ∀ i, 0 ≤ c i) (x : Fin n → α) (i : Fin n) (a : α) :
    |(∑ j, c j * (if s j (Function.update x i a j) then 1 else 0)) -
      ∑ j, c j * (if s j (x j) then 1 else 0)| ≤ c i :=
  additive_bounded_differences (fun j b => c j * (if s j b then 1 else 0)) c
    (fun j a b => by
      have h := hc j
      cases s j a <;> cases s j b <;> simp [abs_of_nonneg h, h]) x i a

/-- **T5 (the worst case is additive and two-level, `Δ`, `β` form).**  For every product
reference on `Fin n → α`, every `β` and all constants `c i ≥ 0`, there are subsets of site
states (encoded by `s i : α → Bool`) such that the additive two-level residual
`Δ⋆ x = ∑ i, c i * [s i (x i)]` — which has bounded differences `c` — has the largest Jensen gap
`log (∑ x, W x * exp (-β Δ x)) + β ⟨Δ⟩` among **all** residuals with bounded differences `c`.
The worst case over the non-decomposable class is attained by a fully decomposable residual. -/
theorem exists_two_level_worst_residual {α : Type*} [Fintype α] {n : ℕ} (p : Fin n → α → ℝ)
    (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1) (c : Fin n → ℝ) (hc : ∀ i, 0 ≤ c i)
    (β : ℝ) :
    ∃ s : Fin n → α → Bool,
      (∀ x i a, |(∑ j, c j * (if s j (Function.update x i a j) then 1 else 0)) -
          ∑ j, c j * (if s j (x j) then 1 else 0)| ≤ c i) ∧
      ∀ Δ : (Fin n → α) → ℝ, (∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) →
        Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) +
            β * ∑ x, (∏ i, p i (x i)) * Δ x ≤
          Real.log (∑ x : Fin n → α, (∏ i, p i (x i)) *
              Real.exp (-β * ∑ i, c i * (if s i (x i) then 1 else 0))) +
            β * ∑ x : Fin n → α, (∏ i, p i (x i)) * ∑ i, c i * (if s i (x i) then 1 else 0) := by
  have hW0 := prod_weight_nonneg p hp
  have hW1 := prod_weight_sum_one p hp1
  obtain ⟨s', hs'⟩ := exists_two_level_additive_extremal p hp hp1 (fun i => |β| * c i)
    (fun i => mul_nonneg (abs_nonneg β) (hc i))
  rcases le_or_gt β 0 with hβ | hβ
  · -- `β ≤ 0`: `-β Δ⋆` is the extremal residual itself
    have habs : |β| = -β := abs_of_nonpos hβ
    refine ⟨s', two_level_set_bounded_differences s' c hc, fun Δ hΔ => ?_⟩
    have hδ : ∀ x : Fin n → α, -β * ∑ i, c i * (if s' i (x i) then 1 else 0) =
        ∑ i, (if s' i (x i) then |β| * c i else 0) := by
      intro x
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl fun i _ => ?_
      rw [habs]
      split_ifs <;> ring
    rw [jensen_gap_eq_log_centered (fun x : Fin n → α => ∏ i, p i (x i)) Δ hW0 hW1 β,
      jensen_gap_eq_log_centered (fun x : Fin n → α => ∏ i, p i (x i))
        (fun x : Fin n → α => ∑ i, c i * (if s' i (x i) then 1 else 0)) hW0 hW1 β]
    simp only [hδ]
    exact Real.log_le_log (weighted_exp_sum_pos _ _ hW0 hW1)
      (hs' (fun x => -β * Δ x) (neg_mul_bounded_differences Δ c hΔ β))
  · -- `β > 0`: pass to the complementary subsets; `-β Δ⋆` is the extremal residual up to a
    -- constant
    have habs : |β| = β := abs_of_pos hβ
    refine ⟨fun i a => !(s' i a),
      two_level_set_bounded_differences (fun i a => !(s' i a)) c hc, fun Δ hΔ => ?_⟩
    have hδ : ∀ x : Fin n → α, -β * ∑ i, c i * (if (!(s' i (x i))) then 1 else 0) =
        (∑ i, (if s' i (x i) then |β| * c i else 0)) - β * ∑ i, c i := by
      intro x
      rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl fun i _ => ?_
      rw [habs]
      cases s' i (x i) <;> simp
    rw [jensen_gap_eq_log_centered (fun x : Fin n → α => ∏ i, p i (x i)) Δ hW0 hW1 β,
      jensen_gap_eq_log_centered (fun x : Fin n → α => ∏ i, p i (x i))
        (fun x : Fin n → α => ∑ i, c i * (if (!(s' i (x i))) then 1 else 0)) hW0 hW1 β]
    simp only [hδ]
    rw [centered_mgf_shift (fun x : Fin n → α => ∏ i, p i (x i)) hW1
      (fun x : Fin n → α => ∑ i, (if s' i (x i) then |β| * c i else 0)) (β * ∑ i, c i)]
    exact Real.log_le_log (weighted_exp_sum_pos _ _ hW0 hW1)
      (hs' (fun x => -β * Δ x) (neg_mul_bounded_differences Δ c hΔ β))

/-- Single-site Jensen gap of a two-level residual `a ↦ c * [s a]` under a general site
marginal `p`: with `r = ∑ a, p a * [s a]` the reference probability of the level set, the gap is
`log (1 - r + r * exp (-β c)) + β c r`. -/
theorem two_level_site_gap_general {α : Type*} [Fintype α] (p : α → ℝ) (hp1 : ∑ a, p a = 1)
    (s : α → Bool) (c β : ℝ) :
    Real.log (∑ a, p a * Real.exp (-β * (c * if s a then 1 else 0))) +
        β * ∑ a, p a * (c * if s a then 1 else 0) =
      Real.log (1 - (∑ a, p a * if s a then 1 else 0) +
          (∑ a, p a * if s a then 1 else 0) * Real.exp (-β * c)) +
        β * c * ∑ a, p a * if s a then 1 else 0 := by
  have h1 : ∑ a, p a * Real.exp (-β * (c * if s a then 1 else 0)) =
      1 - (∑ a, p a * if s a then 1 else 0) +
        (∑ a, p a * if s a then 1 else 0) * Real.exp (-β * c) := by
    have e : ∀ a, p a * Real.exp (-β * (c * if s a then 1 else 0)) =
        p a - p a * (if s a then 1 else 0) +
          p a * (if s a then 1 else 0) * Real.exp (-β * c) := by
      intro a
      cases s a <;> simp
    simp_rw [e]
    rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, hp1, Finset.sum_mul]
  have h2 : ∑ a, p a * (c * if s a then 1 else 0) = c * ∑ a, p a * if s a then 1 else 0 := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun a _ => by ring
  rw [h1, h2]
  ring

/-- **T5 (closed form of the additive two-level gap).**  For a product reference and the
additive two-level residual `Δ x = ∑ i, c i * [s i (x i)]`, with `r i = ∑ a, p i a * [s i a]`
the reference probability of the `i`-th level set:
`log (∑ x, W x * exp (-β Δ x)) + β ⟨Δ⟩ = ∑ i, (log (1 - r i + r i * exp (-β c i)) + β c i r i)`. -/
theorem two_level_additive_gap {α : Type*} [Fintype α] {n : ℕ} (p : Fin n → α → ℝ)
    (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1) (s : Fin n → α → Bool)
    (c : Fin n → ℝ) (β : ℝ) :
    Real.log (∑ x : Fin n → α, (∏ i, p i (x i)) *
          Real.exp (-β * ∑ i, c i * (if s i (x i) then 1 else 0))) +
        β * ∑ x : Fin n → α, (∏ i, p i (x i)) * ∑ i, c i * (if s i (x i) then 1 else 0) =
      ∑ i, (Real.log (1 - (∑ a, p i a * if s i a then 1 else 0) +
          (∑ a, p i a * if s i a then 1 else 0) * Real.exp (-β * c i)) +
        β * c i * ∑ a, p i a * if s i a then 1 else 0) := by
  rw [additive_gap_eq p hp hp1 (fun i a => c i * (if s i a then 1 else 0)) β]
  exact Finset.sum_congr rfl fun i _ => two_level_site_gap_general (p i) (hp1 i) (s i) (c i) β

/-! ### The balanced two-level reference -/

/-- Single-site Jensen gap of the balanced two-level residual: `log (cosh (β c / 2))`. -/
theorem two_level_site_gap (c β : ℝ) :
    Real.log (∑ b : Bool, (1 / 2 : ℝ) * Real.exp (-β * (c * if b then 1 else 0))) +
        β * ∑ b : Bool, (1 / 2 : ℝ) * (c * if b then 1 else 0) =
      Real.log (Real.cosh (β * c / 2)) := by
  have hsum : ∑ b : Bool, (1 / 2 : ℝ) * Real.exp (-β * (c * if b then 1 else 0)) =
      Real.exp (-(β * c / 2)) * Real.cosh (β * c / 2) := by
    rw [Fintype.sum_bool, Real.cosh_eq]
    have e1 : Real.exp (-β * (c * 1)) = Real.exp (-(β * c / 2)) * Real.exp (-(β * c / 2)) := by
      rw [← Real.exp_add]
      congr 1
      ring
    have e2 : Real.exp (-(β * c / 2)) * Real.exp (β * c / 2) = 1 := by
      rw [← Real.exp_add]
      simp
    simp only [if_true, Bool.false_eq_true, if_false, mul_zero, Real.exp_zero]
    rw [e1]
    linear_combination (-1 / 2 : ℝ) * e2
  rw [hsum, Real.log_mul (Real.exp_pos _).ne' (Real.cosh_pos _).ne', Real.log_exp,
    Fintype.sum_bool]
  simp only [if_true, Bool.false_eq_true, if_false]
  ring

/-- **T5(a) (exact value for the balanced additive two-level residual).**  For `α = Bool`,
`p i true = p i false = 1/2` and `Δ x = ∑ i, c i * [x i]`:
`log (∑ x, W x * exp (-β Δ x)) + β ⟨Δ⟩ = ∑ i, log (cosh (β * c i / 2))`. -/
theorem balanced_additive_gap {n : ℕ} (p : Fin n → Bool → ℝ) (hp : ∀ i b, p i b = 1 / 2)
    (c : Fin n → ℝ) (β : ℝ) :
    Real.log (∑ x : Fin n → Bool, (∏ i, p i (x i)) *
          Real.exp (-β * ∑ i, c i * (if x i then 1 else 0))) +
        β * ∑ x : Fin n → Bool, (∏ i, p i (x i)) * ∑ i, c i * (if x i then 1 else 0) =
      ∑ i, Real.log (Real.cosh (β * c i / 2)) := by
  have hp0 : ∀ i b, 0 ≤ p i b := fun i b => by rw [hp]; norm_num
  have hp1 : ∀ i, ∑ b, p i b = 1 := fun i => by
    rw [Fintype.sum_bool, hp, hp]; norm_num
  rw [additive_gap_eq p hp0 hp1 (fun i b => c i * (if b then 1 else 0)) β]
  refine Finset.sum_congr rfl fun i _ => ?_
  simp_rw [hp]
  exact two_level_site_gap (c i) β

/-- The additive two-level residual `x ↦ ∑ i, c i * [x i]` has bounded differences `|c i|`. -/
theorem two_level_bounded_differences {n : ℕ} (c : Fin n → ℝ) (x : Fin n → Bool) (i : Fin n)
    (a : Bool) :
    |(∑ j, c j * (if Function.update x i a j then 1 else 0)) -
      ∑ j, c j * (if x j then 1 else 0)| ≤ |c i| :=
  additive_bounded_differences (fun j b => c j * (if b then 1 else 0)) (fun j => |c j|)
    (fun j a b => by cases a <;> cases b <;> simp) x i a

/-- Single-site extremality for the balanced two-level reference: a site function of oscillation
at most `c` has centred moment generating function at most `cosh (c / 2)`. -/
theorem balanced_site_mgf (h : Bool → ℝ) (c : ℝ) (hh : ∀ a a', |h a - h a'| ≤ c) :
    ∑ b : Bool, (1 / 2 : ℝ) * Real.exp (h b - ∑ b' : Bool, (1 / 2 : ℝ) * h b') ≤
      Real.cosh (c / 2) := by
  have hc : |(h true - h false) / 2| ≤ |c / 2| := by
    have h1 := hh true false
    have hc0 : 0 ≤ c := (abs_nonneg _).trans h1
    rw [abs_div, abs_div, abs_of_nonneg hc0]
    exact div_le_div_of_nonneg_right h1 (abs_nonneg 2)
  have e : ∑ b : Bool, (1 / 2 : ℝ) * Real.exp (h b - ∑ b' : Bool, (1 / 2 : ℝ) * h b') =
      Real.cosh ((h true - h false) / 2) := by
    rw [Fintype.sum_bool, Fintype.sum_bool, Real.cosh_eq]
    have e1 : h true - (1 / 2 * h true + 1 / 2 * h false) = (h true - h false) / 2 := by ring
    have e2 : h false - (1 / 2 * h true + 1 / 2 * h false) = -((h true - h false) / 2) := by
      ring
    rw [e1, e2]
    ring
  rw [e]
  exact Real.cosh_le_cosh.mpr hc

/-- For the balanced two-level reference, every residual with bounded differences `c` has
centred moment generating function at most `∏ i, cosh (c i / 2)`. -/
theorem balanced_mgf_le {n : ℕ} (p : Fin n → Bool → ℝ) (hp : ∀ i b, p i b = 1 / 2)
    (g : (Fin n → Bool) → ℝ) (c : Fin n → ℝ)
    (hg : ∀ x i a, |g (Function.update x i a) - g x| ≤ c i) :
    ∑ x, (∏ i, p i (x i)) * Real.exp (g x - ∑ y, (∏ i, p i (y i)) * g y) ≤
      ∏ i, Real.cosh (c i / 2) := by
  have hp0 : ∀ i b, 0 ≤ p i b := fun i b => by rw [hp]; norm_num
  have hp1 : ∀ i, ∑ b, p i b = 1 := fun i => by
    rw [Fintype.sum_bool, hp, hp]; norm_num
  have h := bounded_differences_tensorization p hp0 hp1 c (fun i => Real.cosh (c i / 2))
    (fun i => (Real.cosh_pos _).le)
    (fun i h hh => by
      simp_rw [hp]
      exact balanced_site_mgf h (c i) hh) g hg (∑ y, (∏ i, p i (y i)) * g y)
  rwa [sub_self, Real.exp_zero, mul_one] at h

/-- For the balanced two-level reference, the Jensen gap of every residual with bounded
differences `c` is at most `∑ i, log (cosh (β * c i / 2))`. -/
theorem balanced_gap_le {n : ℕ} (p : Fin n → Bool → ℝ) (hp : ∀ i b, p i b = 1 / 2)
    (Δ : (Fin n → Bool) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β : ℝ) :
    Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) +
        β * ∑ x, (∏ i, p i (x i)) * Δ x ≤
      ∑ i, Real.log (Real.cosh (β * c i / 2)) := by
  have hp0 : ∀ i b, 0 ≤ p i b := fun i b => by rw [hp]; norm_num
  have hp1 : ∀ i, ∑ b, p i b = 1 := fun i => by
    rw [Fintype.sum_bool, hp, hp]; norm_num
  have h := balanced_mgf_le p hp (fun x => -β * Δ x) (fun i => |β| * c i)
    (neg_mul_bounded_differences Δ c hΔ β)
  have hBpos : 0 < ∏ i, Real.cosh (|β| * c i / 2) :=
    Finset.prod_pos fun i _ => Real.cosh_pos _
  have h2 := log_weighted_exp_le_of_centered_le (fun x : Fin n → Bool => ∏ i, p i (x i))
    (fun x => -β * Δ x) (prod_weight_nonneg p hp0) (prod_weight_sum_one p hp1)
    (Real.log (∏ i, Real.cosh (|β| * c i / 2))) (by rw [Real.exp_log hBpos]; exact h)
  rw [weighted_sum_neg_mul, Real.log_prod (fun i _ => (Real.cosh_pos _).ne')] at h2
  have e : ∀ i, Real.cosh (|β| * c i / 2) = Real.cosh (β * c i / 2) := by
    intro i
    rcases abs_choice β with hβ | hβ
    · rw [hβ]
    · rw [hβ, neg_mul, neg_div, Real.cosh_neg]
  simp_rw [e] at h2
  linarith

/-- **T5 (exact extremality for the balanced reference).**  For the balanced two-level
reference, among all residuals `Δ` with bounded differences `c` (decomposable or not), the
Jensen gap `log (∑ x, W x * exp (-β Δ x)) + β ⟨Δ⟩` is maximised by the additive residual
`x ↦ ∑ i, c i * [x i]` (which belongs to the class, see `two_level_bounded_differences` and
`bounded_differences_nonneg`). -/
theorem balanced_additive_extremal {n : ℕ} (p : Fin n → Bool → ℝ) (hp : ∀ i b, p i b = 1 / 2)
    (Δ : (Fin n → Bool) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β : ℝ) :
    Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) +
        β * ∑ x, (∏ i, p i (x i)) * Δ x ≤
      Real.log (∑ x : Fin n → Bool, (∏ i, p i (x i)) *
          Real.exp (-β * ∑ i, c i * (if x i then 1 else 0))) +
        β * ∑ x : Fin n → Bool, (∏ i, p i (x i)) * ∑ i, c i * (if x i then 1 else 0) := by
  rw [balanced_additive_gap p hp c β]
  exact balanced_gap_le p hp Δ c hΔ β

/-! ### Scalar bounds on `log cosh` and optimality of the constant `1/8` -/

/-- `1 + u² / 2 ≤ cosh u` (first two terms of the power series). -/
theorem one_add_sq_div_two_le_cosh (u : ℝ) : 1 + u ^ 2 / 2 ≤ Real.cosh u := by
  have h := sum_le_hasSum (Finset.range 2)
    (fun i _ => div_nonneg (by rw [pow_mul]; positivity) (Nat.cast_nonneg _))
    (Real.hasSum_cosh u)
  simpa [Finset.sum_range_succ] using h

/-- `log (cosh u) ≤ u² / 2`. -/
theorem log_cosh_le_half_sq (u : ℝ) : Real.log (Real.cosh u) ≤ u ^ 2 / 2 :=
  (Real.log_le_iff_le_exp (Real.cosh_pos u)).mpr (Real.cosh_le_exp_half_sq u)

/-- `u² / (2 + u²) ≤ log (cosh u)`. -/
theorem sq_div_le_log_cosh (u : ℝ) : u ^ 2 / (2 + u ^ 2) ≤ Real.log (Real.cosh u) := by
  have h1 : 1 + u ^ 2 / 2 ≤ Real.cosh u := one_add_sq_div_two_le_cosh u
  have hpos : (0 : ℝ) < 1 + u ^ 2 / 2 := by positivity
  have h2 := Real.one_sub_inv_le_log_of_pos hpos
  have h3 := Real.log_le_log hpos h1
  have e : 1 - (1 + u ^ 2 / 2)⁻¹ = u ^ 2 / (2 + u ^ 2) := by
    have h4 : (2 + u ^ 2) ≠ 0 := by positivity
    have h5 : (1 + u ^ 2 / 2) ≠ 0 := hpos.ne'
    field_simp
    ring
  linarith

/-- **T5(b).**  `u² / (2 + u²) ≤ log (cosh u) ≤ u² / 2` for every real `u`. -/
theorem log_cosh_bounds (u : ℝ) :
    u ^ 2 / (2 + u ^ 2) ≤ Real.log (Real.cosh u) ∧ Real.log (Real.cosh u) ≤ u ^ 2 / 2 :=
  ⟨sq_div_le_log_cosh u, log_cosh_le_half_sq u⟩

/-- `log (cosh u) / u² → 1/2` as `u → 0`, `u ≠ 0`: the quadratic upper bound `u² / 2` is attained
to leading order.  With `u = β c / 2` this says that the exact gap `log (cosh (β c / 2))` of the
balanced two-level residual is asymptotic to the Hoeffding bound `β² c² / 8`. -/
theorem tendsto_log_cosh_div_sq :
    Filter.Tendsto (fun u : ℝ => Real.log (Real.cosh u) / u ^ 2) (nhdsWithin 0 {0}ᶜ)
      (nhds (1 / 2)) := by
  have hlow : Filter.Tendsto (fun u : ℝ => 1 / (2 + u ^ 2)) (nhdsWithin 0 {0}ᶜ)
      (nhds (1 / 2)) := by
    have hc : ContinuousAt (fun u : ℝ => 1 / (2 + u ^ 2)) 0 :=
      ContinuousAt.div continuousAt_const (by fun_prop) (by norm_num)
    have h := hc.tendsto
    simp only [ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, zero_pow, add_zero] at h
    exact h.mono_left nhdsWithin_le_nhds
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' hlow tendsto_const_nhds ?_ ?_
  · filter_upwards [self_mem_nhdsWithin] with u hu
    have hu0 : u ≠ 0 := hu
    have hu2 : (0 : ℝ) < u ^ 2 := by positivity
    have e : 1 / (2 + u ^ 2) = u ^ 2 / (2 + u ^ 2) / u ^ 2 := by
      have h4 : (2 + u ^ 2) ≠ 0 := by positivity
      field_simp
    rw [e]
    exact div_le_div_of_nonneg_right (sq_div_le_log_cosh u) hu2.le
  · filter_upwards [self_mem_nhdsWithin] with u hu
    have hu0 : u ≠ 0 := hu
    have hu2 : (0 : ℝ) < u ^ 2 := by positivity
    have e : (1 : ℝ) / 2 = u ^ 2 / 2 / u ^ 2 := by
      field_simp
    rw [e]
    exact div_le_div_of_nonneg_right (log_cosh_le_half_sq u) hu2.le

/-- Two-sided control of the exact gap of the balanced additive residual: it lies between
`∑ i, β² (c i)² / (8 + β² (c i)²)` and the McDiarmid bound `β² (∑ i, (c i)²) / 8`.  The two
agree to leading order as `β * c i → 0`, so the bound of T4 is attained to leading order. -/
theorem balanced_additive_gap_bounds {n : ℕ} (p : Fin n → Bool → ℝ) (hp : ∀ i b, p i b = 1 / 2)
    (c : Fin n → ℝ) (β : ℝ) :
    ∑ i, β ^ 2 * c i ^ 2 / (8 + β ^ 2 * c i ^ 2) ≤
        Real.log (∑ x : Fin n → Bool, (∏ i, p i (x i)) *
            Real.exp (-β * ∑ i, c i * (if x i then 1 else 0))) +
          β * ∑ x : Fin n → Bool, (∏ i, p i (x i)) * ∑ i, c i * (if x i then 1 else 0) ∧
      Real.log (∑ x : Fin n → Bool, (∏ i, p i (x i)) *
            Real.exp (-β * ∑ i, c i * (if x i then 1 else 0))) +
          β * ∑ x : Fin n → Bool, (∏ i, p i (x i)) * ∑ i, c i * (if x i then 1 else 0) ≤
        β ^ 2 * (∑ i, c i ^ 2) / 8 := by
  rw [balanced_additive_gap p hp c β]
  constructor
  · refine Finset.sum_le_sum fun i _ => ?_
    have h := sq_div_le_log_cosh (β * c i / 2)
    have e : (β * c i / 2) ^ 2 / (2 + (β * c i / 2) ^ 2) =
        β ^ 2 * c i ^ 2 / (8 + β ^ 2 * c i ^ 2) := by
      have h1 : (8 + β ^ 2 * c i ^ 2) ≠ 0 := by positivity
      have h2 : (2 + (β * c i / 2) ^ 2) ≠ 0 := by positivity
      field_simp
      ring
    rwa [e] at h
  · rw [Finset.mul_sum, Finset.sum_div]
    refine Finset.sum_le_sum fun i _ => ?_
    have h := log_cosh_le_half_sq (β * c i / 2)
    have e : (β * c i / 2) ^ 2 / 2 = β ^ 2 * c i ^ 2 / 8 := by ring
    rwa [e] at h

/-- Explicit witness for the optimality of `1/8`: `β = √(8 - 64 K)`, `c = 1`. -/
theorem hoeffding_constant_sharp_witness (K : ℝ) (hK : K < 1 / 8) :
    K * Real.sqrt (8 - 64 * K) ^ 2 * 1 ^ 2 <
      Real.log (Real.cosh (Real.sqrt (8 - 64 * K) * 1 / 2)) := by
  have ht : 0 < 8 - 64 * K := by linarith
  have hsq : Real.sqrt (8 - 64 * K) ^ 2 = 8 - 64 * K := Real.sq_sqrt ht.le
  refine lt_of_lt_of_le ?_ (sq_div_le_log_cosh (Real.sqrt (8 - 64 * K) * 1 / 2))
  have e : (Real.sqrt (8 - 64 * K) * 1 / 2) ^ 2 = (8 - 64 * K) / 4 := by
    rw [mul_one, div_pow, hsq]
    norm_num
  rw [e, hsq, lt_div_iff₀ (by positivity)]
  nlinarith [mul_pos ht (sq_pos_of_pos (by linarith : (0 : ℝ) < 1 - 8 * K))]

/-- **T5(c) (the constant `1/8` is optimal, scalar form).**  For every `K < 1/8` there are
`β`, `c` such that the exact gap `log (cosh (β c / 2))` of the one-site balanced additive
residual exceeds `K β² c²`. -/
theorem hoeffding_constant_sharp (K : ℝ) (hK : K < 1 / 8) :
    ∃ β c : ℝ, K * β ^ 2 * c ^ 2 < Real.log (Real.cosh (β * c / 2)) :=
  ⟨Real.sqrt (8 - 64 * K), 1, hoeffding_constant_sharp_witness K hK⟩

/-- **T5(c) (the constant `1/8` is optimal, explicit violating instance).**  For every
`K < 1/8` there are a single site (`n = 1`), the balanced two-level reference, an additive
residual `Δ` with bounded differences `c` and an inverse temperature `β` which violate the
upper bound of `mcdiarmid_log_upper` with `K` in place of `1/8`. -/
theorem mcdiarmid_constant_optimal (K : ℝ) (hK : K < 1 / 8) :
    ∃ (β : ℝ) (c : Fin 1 → ℝ) (Δ : (Fin 1 → Bool) → ℝ),
      (∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) ∧
        -β * ∑ x : Fin 1 → Bool, (∏ _i : Fin 1, (1 / 2 : ℝ)) * Δ x + K * β ^ 2 * ∑ i, c i ^ 2 <
          Real.log (∑ x : Fin 1 → Bool, (∏ _i : Fin 1, (1 / 2 : ℝ)) * Real.exp (-β * Δ x)) := by
  refine ⟨Real.sqrt (8 - 64 * K), fun _ => 1,
    fun x => ∑ i, (1 : ℝ) * (if x i then 1 else 0), ?_, ?_⟩
  · intro x i a
    exact additive_bounded_differences (fun _ b => (1 : ℝ) * (if b then 1 else 0))
      (fun _ => 1) (fun _ a b => by cases a <;> cases b <;> simp) x i a
  · have hgap := balanced_additive_gap (n := 1) (fun _ _ => 1 / 2) (fun _ _ => rfl)
      (fun _ => 1) (Real.sqrt (8 - 64 * K))
    have hw := hoeffding_constant_sharp_witness K hK
    simp only [Fin.sum_univ_one] at hgap ⊢
    linarith

/-- **T5(c) (no better constant).**  For `K < 1/8`, the statement of `mcdiarmid_log_upper` with
`K` in place of `1/8` is false. -/
theorem mcdiarmid_no_better_constant (K : ℝ) (hK : K < 1 / 8) :
    ¬ ∀ (n : ℕ) (p : Fin n → Bool → ℝ), (∀ i a, 0 ≤ p i a) → (∀ i, ∑ a, p i a = 1) →
        ∀ (Δ : (Fin n → Bool) → ℝ) (c : Fin n → ℝ),
          (∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) → ∀ β : ℝ,
            Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
              -β * ∑ x, (∏ i, p i (x i)) * Δ x + K * β ^ 2 * ∑ i, c i ^ 2 := by
  intro H
  obtain ⟨β, c, Δ, hΔ, hlt⟩ := mcdiarmid_constant_optimal K hK
  have h := H 1 (fun _ _ => 1 / 2) (fun _ _ => by norm_num)
    (fun _ => by rw [Fintype.sum_bool]; norm_num) Δ c hΔ β
  exact absurd h (not_le.mpr hlt)

end Sharpness

/-! ## Non-vacuity: concrete instances -/

section Examples

/-- Non-vacuity of T4 on a genuinely non-decomposable residual: two sites, `α = Bool`, uniform
site marginals, and the interaction `g x = [x 0 ∧ x 1]`, which has bounded differences
`c = (1, 1)`.  The hypotheses of `mcdiarmid_mgf` are jointly satisfiable and the conclusion is
the explicit bound `exp (1/4)`. -/
example :
    ∑ x : Fin 2 → Bool, (∏ _i : Fin 2, (1 / 2 : ℝ)) *
        Real.exp ((if x 0 && x 1 then (1 : ℝ) else 0) -
          ∑ y : Fin 2 → Bool, (∏ _i : Fin 2, (1 / 2 : ℝ)) *
            (if y 0 && y 1 then (1 : ℝ) else 0)) ≤
      Real.exp (1 / 4) := by
  have h01 : ∀ y : Fin 2 → Bool, (0 : ℝ) ≤ (if y 0 && y 1 then (1 : ℝ) else 0) ∧
      (if y 0 && y 1 then (1 : ℝ) else 0) ≤ 1 := fun y => by split_ifs <;> norm_num
  have h := mcdiarmid_mgf (α := Bool) (n := 2) (fun _ _ => 1 / 2) (fun _ _ => by norm_num)
    (fun _ => by rw [Fintype.sum_bool]; norm_num)
    (fun x => if x 0 && x 1 then (1 : ℝ) else 0) (fun _ => 1)
    (fun x i a => by
      rw [abs_le]
      constructor <;> linarith [(h01 x).1, (h01 x).2, (h01 (Function.update x i a)).1,
        (h01 (Function.update x i a)).2])
  have e : (∑ _i : Fin 2, (1 : ℝ) ^ 2) / 8 = 1 / 4 := by
    rw [Fin.sum_univ_two]
    norm_num
  rw [e] at h
  exact h

/-- The same instance in the `Δ`, `β` form: the two-sided bounded-differences sandwich. -/
example (β : ℝ) :
    -β * ∑ x : Fin 2 → Bool, (∏ _i : Fin 2, (1 / 2 : ℝ)) * (if x 0 && x 1 then (1 : ℝ) else 0) ≤
        Real.log (∑ x : Fin 2 → Bool, (∏ _i : Fin 2, (1 / 2 : ℝ)) *
          Real.exp (-β * (if x 0 && x 1 then (1 : ℝ) else 0))) ∧
      Real.log (∑ x : Fin 2 → Bool, (∏ _i : Fin 2, (1 / 2 : ℝ)) *
          Real.exp (-β * (if x 0 && x 1 then (1 : ℝ) else 0))) ≤
        -β * ∑ x : Fin 2 → Bool, (∏ _i : Fin 2, (1 / 2 : ℝ)) *
          (if x 0 && x 1 then (1 : ℝ) else 0) + β ^ 2 / 4 := by
  have h01 : ∀ y : Fin 2 → Bool, (0 : ℝ) ≤ (if y 0 && y 1 then (1 : ℝ) else 0) ∧
      (if y 0 && y 1 then (1 : ℝ) else 0) ≤ 1 := fun y => by split_ifs <;> norm_num
  have h := bounded_differences_sandwich (α := Bool) (n := 2) (fun _ _ => 1 / 2)
    (fun _ _ => by norm_num) (fun _ => by rw [Fintype.sum_bool]; norm_num)
    (fun x => if x 0 && x 1 then (1 : ℝ) else 0) (fun _ => 1)
    (fun x i a => by
      rw [abs_le]
      constructor <;> linarith [(h01 x).1, (h01 x).2, (h01 (Function.update x i a)).1,
        (h01 (Function.update x i a)).2]) β
  have e : β ^ 2 * (∑ _i : Fin 2, (1 : ℝ) ^ 2) / 8 = β ^ 2 / 4 := by
    rw [Fin.sum_univ_two]
    ring
  rw [e] at h
  exact h

/-- Non-vacuity of T3: the two-level system with uniform reference and `Δ ∈ {0, 1}`:
`-β/2 ≤ log ((1 + exp (-β)) / 2) ≤ -β/2 + β²/8`. -/
example (β : ℝ) :
    -β / 2 ≤ Real.log ((1 + Real.exp (-β)) / 2) ∧
      Real.log ((1 + Real.exp (-β)) / 2) ≤ -β / 2 + β ^ 2 / 8 := by
  have h := free_energy_sandwich (Ω := Bool) (fun _ => 1 / 2) (fun b => if b then 1 else 0)
    (fun _ => by norm_num) (by rw [Fintype.sum_bool]; norm_num) 0 1
    (fun b => by cases b <;> simp) β
  have e1 : ∑ b : Bool, (1 / 2 : ℝ) * (if b then 1 else 0) = 1 / 2 := by
    rw [Fintype.sum_bool]
    simp
  have e2 : ∑ b : Bool, (1 / 2 : ℝ) * Real.exp (-β * (if b then 1 else 0)) =
      (1 + Real.exp (-β)) / 2 := by
    rw [Fintype.sum_bool]
    simp only [if_true, Bool.false_eq_true, if_false, mul_one, mul_zero, Real.exp_zero]
    ring
  rw [e1, e2] at h
  constructor
  · linarith [h.1]
  · linarith [h.2]

/-- Non-vacuity of the general form of T4 on a *heterogeneous* system: two sites indexed by
`Bool`, the site `true` with `2` states and the site `false` with `3` states, uniform site
marginals, and the non-decomposable "equal labels" interaction
`g x = [(x true : ℕ) = (x false : ℕ)]`, which has bounded differences `c = (1, 1)`. -/
example (β : ℝ) :
    Real.log (∑ x : ∀ b : Bool, Fin (if b then 2 else 3),
        (∏ b : Bool, (1 / (if b then 2 else 3) : ℝ)) *
          Real.exp (-β * (if (x true : ℕ) = (x false : ℕ) then (1 : ℝ) else 0))) ≤
      -β * ∑ x : ∀ b : Bool, Fin (if b then 2 else 3),
        (∏ b : Bool, (1 / (if b then 2 else 3) : ℝ)) *
          (if (x true : ℕ) = (x false : ℕ) then (1 : ℝ) else 0) + β ^ 2 / 4 := by
  have h01 : ∀ y : ∀ b : Bool, Fin (if b then 2 else 3),
      (0 : ℝ) ≤ (if (y true : ℕ) = (y false : ℕ) then (1 : ℝ) else 0) ∧
        (if (y true : ℕ) = (y false : ℕ) then (1 : ℝ) else 0) ≤ 1 :=
    fun y => by by_cases h : (y true : ℕ) = (y false : ℕ) <;> simp [h]
  have h := (bounded_differences_sandwich_pi (ι := Bool) (σ := fun b => Fin (if b then 2 else 3))
    (fun b _ => 1 / (if b then 2 else 3)) (fun b _ => by positivity)
    (fun b => by
      cases b
      · show ∑ _a : Fin 3, (1 / 3 : ℝ) = 1
        simp
      · show ∑ _a : Fin 2, (1 / 2 : ℝ) = 1
        simp)
    (fun x => if (x true : ℕ) = (x false : ℕ) then (1 : ℝ) else 0) (fun _ => 1)
    (fun x i a => by
      rw [abs_le]
      constructor <;> linarith [(h01 x).1, (h01 x).2, (h01 (Function.update x i a)).1,
        (h01 (Function.update x i a)).2]) β).2
  have e : β ^ 2 * (∑ _i : Bool, (1 : ℝ) ^ 2) / 8 = β ^ 2 / 4 := by
    rw [Fintype.sum_bool]
    ring
  rw [e] at h
  exact h

end Examples

end MetricChain
