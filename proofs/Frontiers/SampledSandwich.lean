import Mathlib
import proofs.Frontiers.FreeEnergySandwich

/-!
# The sampled free-energy sandwich: random samples pin `ln (Z / Z₀)`

Setting of `FreeEnergySandwich.lean`: a product reference `W x = ∏ i, p i (x i)` on the
configurations `x : Fin n → α` (`0 ≤ p i a`, `∑ a, p i a = 1`) and a residual `Δ` with bounded
differences `|Δ (update x i a) - Δ x| ≤ c i`.  Write

* `m = ⟨Δ⟩ = ∑ x, W x * Δ x` for the reference mean of the residual,
* `C = ∑ i, (c i)²`,
* `L = log (∑ x, W x * exp (-β Δ x)) = ln (Z / Z₀)` for the free-energy difference between the
  target (reference plus residual) and the reference.

The bounded-differences sandwich (`bounded_differences_sandwich`) reads
`-β m ≤ L ≤ -β m + β² C / 8`.  It pins `L` once `m` is known, but `m` is a sum over all
`|α| ^ n` configurations, and elsewhere in the project it is proved that *deterministic*
certification of a free energy from pointwise evaluations of the residual needs exponentially
many evaluations.  This file proves the constructive counterpart for *random* evaluations: the
empirical mean of `Δ` over `N` independent samples from the reference pins `L` with high
probability, and the number of samples needed depends only on `C`, on the accuracy and on the
confidence level, not on the size of the configuration space.

## The sample space

A sample is a tuple `ω : Fin N → (Fin n → α)` of `N` configurations.  Independent sampling from
the reference gives it the weight `P ω = sampleWeight p N ω = ∏ k, W (ω k)`; these weights are
nonnegative and sum to one.  The *weight of an event* `E` (a predicate on samples) is the finite
sum `∑ ω ∈ univ.filter E, P ω`, i.e. its probability.  The empirical mean of the residual is
`empMean Δ ω = (∑ k, Δ (ω k)) / N`.  No measure theory appears in any statement: everything is
a finite sum over the `Fintype` of sample tuples.

## Main results

* **S0** `sampleWeight_nonneg`, `sampleWeight_sum_one` — the sample weights form a probability
  vector; `sample_weight_mono`, `sample_weight_union_le`, `sample_weight_ge_of_compl_le` are
  monotonicity, the union bound and the complement rule for weights of events.
* **S1** `sample_mgf` (`sample_mgf_eq`, `sample_mgf_le`) — moment generating function of the
  centred sample sum: for every real `t`,
  `∑ ω, P ω * exp (t * ∑ k, (Δ (ω k) - m)) = (∑ x, W x * exp (t * (Δ x - m))) ^ N`
  and this is at most `exp (N * t² * C / 8)`.
* **S2** `sample_chernoff`, `sample_mean_upper_tail`, `sample_mean_lower_tail` — the Chernoff
  bound and the one-sided deviation inequalities: for `η ≥ 0` each of the events
  `m + η ≤ empMean Δ ω` and `empMean Δ ω ≤ m - η` has weight at most `exp (-2 * N * η² / C)`.
* **S3** `sample_mean_two_sided` — the event `η ≤ |empMean Δ ω - m|` has weight at most
  `2 * exp (-2 * N * η² / C)`.
* **S4** `sampled_free_energy_sandwich` — **the sampled free-energy sandwich**: the samples `ω`
  for which the interval
  `[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² * C / 8]`
  does *not* contain `L` have total weight at most `2 * exp (-2 * N * η² / C)`; equivalently
  (`sampled_free_energy_sandwich_good`) the interval contains `L` with probability at least
  `1 - 2 * exp (-2 * N * η² / C)`.  The deterministic half is `sandwich_of_mean_estimate`: *any*
  estimate `e` of the reference mean with `|e - m| ≤ η` yields such an interval.
* **S5** `sample_size_bound`, `sampled_free_energy_sandwich_of_sample_size`,
  `sampled_free_energy_sandwich_good_of_sample_size` — sample-size form: if
  `C * log (2 / δ) ≤ N * (2 * η²)` then the failure probability is at most `δ`.
  `sampled_sandwich_sample_complexity`, `exists_sampled_sandwich_sample_size` — the explicit
  sample size `max 1 ⌈C₀ * log (2 / δ) / (2 * η²)⌉₊` works simultaneously for all alphabets, all
  numbers of sites, all product references, all residuals with `C ≤ C₀` and all `β`.  (If
  `|c i| ≤ c₀` at every site one can take `C₀ = n * c₀²`: the sample size then grows linearly
  with the number of sites, whereas the configuration space has `|α| ^ n` points.)
* **S6** `sampled_sandwich_check_1` … `sampled_sandwich_check_4` — non-vacuity on a concrete
  two-site instance with a non-constant residual.

## Proof outline

* S1: the exponential of a sum over the samples is a product over the samples, and a sum over
  tuples of a product of single-sample terms is the `N`-th power of the single-sample sum
  (`Fintype.sum_pow`, i.e. independence).  The single-sample factor is bounded by McDiarmid's
  inequality `mcdiarmid_mgf` applied to `t * Δ`, whose bounded differences are `|t| * c i`.
* S2: exponential Markov inequality.  If `a ≤ t * ∑ k, (Δ (ω k) - m)` on an event, then
  `1 ≤ exp (t * ∑ k, (Δ (ω k) - m) - a)` there, so by S1 the event has weight at most
  `exp (N * t² * C / 8 - a)`.  The two tails are `t = ± 4 η / C` and `a = 4 N η² / C`.
* S3 is the union bound, and S4 follows because outside the event of S3 the empirical mean is an
  estimate of `m` with error at most `η`.
* S5 is algebra, together with the degenerate case below.

## Degenerate cases

No positivity assumption on `N` or `C` is needed in S1–S4.  For `N = 0` the empirical mean is
`0` (convention `0 / 0 = 0`) and the bounds of S2–S4 read `≤ 1` and `≤ 2`.  For `C = 0` the
right-hand sides of S2–S4 are again `1` and `2`, by the convention `x / 0 = 0`: the statements
are true but carry no information.  The sharp statement in that case is
`sampled_sandwich_of_sq_sum_eq_zero`: a residual with `C = 0` is constant
(`const_of_bounded_differences_sq_sum_eq_zero`), and then the interval of S4 contains `L` for
*every* sample with `N ≥ 1`.  Consequently the sample-size form S5 only assumes `0 < N`.

## Conventions used in the docstrings

`W`, `m`, `C`, `L`, `P` are as above; "bounded differences `c`" means
`∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i`; the "weight" of an event is the sum of the
sample weights `P ω` over the sample tuples `ω` in the event.
-/

namespace MetricChain

open Finset

section Sampling

variable {α : Type*} [Fintype α] {n : ℕ}

/-! ## S0. The sample space of `N` independent configurations -/

/-- **Sample weight.**  The weight of a tuple `ω` of `N` configurations under independent
sampling from the product reference `W x = ∏ i, p i (x i)`: `P ω = ∏ k, W (ω k)`.  For `N = 0`
there is exactly one (empty) tuple, of weight `1`. -/
noncomputable def sampleWeight (p : Fin n → α → ℝ) (N : ℕ) (ω : Fin N → Fin n → α) : ℝ :=
  ∏ k, ∏ i, p i (ω k i)

/-- **Empirical mean.**  The average `(∑ k, Δ (ω k)) / N` of the residual `Δ` over a tuple `ω`
of `N` sampled configurations.  For `N = 0` its value is `0` (convention `0 / 0 = 0`). -/
noncomputable def empMean {N : ℕ} (Δ : (Fin n → α) → ℝ) (ω : Fin N → Fin n → α) : ℝ :=
  (∑ k, Δ (ω k)) / N

omit [Fintype α] in
/-- **S0.**  Sample weights are nonnegative. -/
theorem sampleWeight_nonneg (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a) (N : ℕ)
    (ω : Fin N → Fin n → α) : 0 ≤ sampleWeight p N ω :=
  Finset.prod_nonneg fun k _ => prod_weight_nonneg p hp (ω k)

/-- **Independence.**  The sum over all sample tuples of a product of single-sample terms is the
`N`-th power of the single-sample sum. -/
theorem sum_sample_prod (f : (Fin n → α) → ℝ) (N : ℕ) :
    ∑ ω : Fin N → Fin n → α, ∏ k, f (ω k) = (∑ x, f x) ^ N :=
  (Fintype.sum_pow f N).symm

/-- **S0.**  Sample weights sum to one: together with `sampleWeight_nonneg`, they form a
probability vector on the sample tuples. -/
theorem sampleWeight_sum_one (p : Fin n → α → ℝ) (hp1 : ∀ i, ∑ a, p i a = 1) (N : ℕ) :
    ∑ ω : Fin N → Fin n → α, sampleWeight p N ω = 1 := by
  unfold sampleWeight
  rw [sum_sample_prod (fun x : Fin n → α => ∏ i, p i (x i)), prod_weight_sum_one p hp1, one_pow]

/-- The weight of any set of sample tuples is at most one. -/
theorem sample_event_weight_le_one (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (N : ℕ) (E : Finset (Fin N → Fin n → α)) :
    ∑ ω ∈ E, sampleWeight p N ω ≤ 1 := by
  rw [← sampleWeight_sum_one p hp1 N]
  exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ E)
    (fun ω _ _ => sampleWeight_nonneg p hp N ω)

/-- **Monotonicity.**  If the event `E` implies the event `E'`, the weight of `E` is at most
the weight of `E'`. -/
theorem sample_weight_mono (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a) (N : ℕ)
    (E E' : (Fin N → Fin n → α) → Prop) [DecidablePred E] [DecidablePred E']
    (h : ∀ ω, E ω → E' ω) :
    ∑ ω ∈ univ.filter E, sampleWeight p N ω ≤ ∑ ω ∈ univ.filter E', sampleWeight p N ω := by
  refine Finset.sum_le_sum_of_subset_of_nonneg (fun ω hω => ?_)
    (fun ω _ _ => sampleWeight_nonneg p hp N ω)
  rw [Finset.mem_filter] at hω ⊢
  exact ⟨hω.1, h ω hω.2⟩

/-- **Union bound.**  If the event `E` implies `E₁` or `E₂`, the weight of `E` is at most the
sum of the weights of `E₁` and `E₂`. -/
theorem sample_weight_union_le (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a) (N : ℕ)
    (E E₁ E₂ : (Fin N → Fin n → α) → Prop) [DecidablePred E] [DecidablePred E₁]
    [DecidablePred E₂] (h : ∀ ω, E ω → E₁ ω ∨ E₂ ω) :
    ∑ ω ∈ univ.filter E, sampleWeight p N ω ≤
      ∑ ω ∈ univ.filter E₁, sampleWeight p N ω + ∑ ω ∈ univ.filter E₂, sampleWeight p N ω := by
  rw [Finset.sum_filter, Finset.sum_filter, Finset.sum_filter, ← Finset.sum_add_distrib]
  refine Finset.sum_le_sum fun ω _ => ?_
  have h0 := sampleWeight_nonneg p hp N ω
  by_cases hE : E ω
  · rw [if_pos hE]
    rcases h ω hE with h1 | h2
    · rw [if_pos h1]
      split_ifs <;> linarith
    · rw [if_pos h2]
      split_ifs <;> linarith
  · rw [if_neg hE]
    split_ifs <;> linarith

/-- **Complement rule.**  If the complement of an event has weight at most `b`, the event has
weight at least `1 - b`. -/
theorem sample_weight_ge_of_compl_le (p : Fin n → α → ℝ) (hp1 : ∀ i, ∑ a, p i a = 1) (N : ℕ)
    (E : (Fin N → Fin n → α) → Prop) [DecidablePred E] (b : ℝ)
    (h : ∑ ω ∈ univ.filter (fun ω => ¬ E ω), sampleWeight p N ω ≤ b) :
    1 - b ≤ ∑ ω ∈ univ.filter E, sampleWeight p N ω := by
  have hsplit := Finset.sum_filter_add_sum_filter_not (univ : Finset (Fin N → Fin n → α)) E
    (sampleWeight p N)
  rw [sampleWeight_sum_one p hp1 N] at hsplit
  linarith

omit [Fintype α] in
/-- The centred sample sum is `N` times the centred empirical mean (also for `N = 0`, where
both sides vanish). -/
theorem sample_sum_centered_eq {N : ℕ} (Δ : (Fin n → α) → ℝ) (ω : Fin N → Fin n → α) (m : ℝ) :
    ∑ k, (Δ (ω k) - m) = N * (empMean Δ ω - m) := by
  rw [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  unfold empMean
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · simp
  · have hN' : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
    field_simp

/-! ## S1. The moment generating function of the sample sum -/

/-- **S1 (product structure).**  For every centring constant `m` and every real `t`, the moment
generating function of the centred sample sum is the `N`-th power of the single-sample one:
`∑ ω, P ω * exp (t * ∑ k, (Δ (ω k) - m)) = (∑ x, W x * exp (t * (Δ x - m))) ^ N`. -/
theorem sample_mgf_eq (p : Fin n → α → ℝ) (Δ : (Fin n → α) → ℝ) (m t : ℝ) (N : ℕ) :
    ∑ ω : Fin N → Fin n → α, sampleWeight p N ω * Real.exp (t * ∑ k, (Δ (ω k) - m)) =
      (∑ x, (∏ i, p i (x i)) * Real.exp (t * (Δ x - m))) ^ N := by
  rw [← sum_sample_prod]
  refine Finset.sum_congr rfl fun ω _ => ?_
  rw [Finset.mul_sum, Real.exp_sum, Finset.prod_mul_distrib]
  rfl

/-- **Single-sample bound.**  For a product reference and a residual `Δ` with bounded
differences `c`, `∑ x, W x * exp (t * (Δ x - ⟨Δ⟩)) ≤ exp (t² * C / 8)` for every real `t`
(McDiarmid's inequality `mcdiarmid_mgf` for `t * Δ`, whose bounded differences are
`|t| * c i`). -/
theorem single_sample_mgf_le (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (t : ℝ) :
    ∑ x, (∏ i, p i (x i)) * Real.exp (t * (Δ x - ∑ y, (∏ i, p i (y i)) * Δ y)) ≤
      Real.exp (t ^ 2 * (∑ i, c i ^ 2) / 8) := by
  have hbd : ∀ x i a, |t * Δ (Function.update x i a) - t * Δ x| ≤ |t| * c i := by
    intro x i a
    rw [← mul_sub, abs_mul]
    exact mul_le_mul_of_nonneg_left (hΔ x i a) (abs_nonneg t)
  have h := mcdiarmid_mgf p hp hp1 (fun x => t * Δ x) (fun i => |t| * c i) hbd
  have e1 : ∑ y, (∏ i, p i (y i)) * (t * Δ y) = t * ∑ y, (∏ i, p i (y i)) * Δ y := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun y _ => by ring
  have e2 : (∑ i, (|t| * c i) ^ 2) / 8 = t ^ 2 * (∑ i, c i ^ 2) / 8 := by
    rw [Finset.mul_sum]
    congr 1
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [mul_pow, sq_abs]
  rw [e1, e2] at h
  simpa only [mul_sub] using h

/-- **S1 (bound).**  For a product reference, a residual `Δ` with bounded differences `c` and
every real `t`: `∑ ω, P ω * exp (t * ∑ k, (Δ (ω k) - ⟨Δ⟩)) ≤ exp (N * t² * C / 8)`. -/
theorem sample_mgf_le (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (t : ℝ) (N : ℕ) :
    ∑ ω : Fin N → Fin n → α, sampleWeight p N ω *
        Real.exp (t * ∑ k, (Δ (ω k) - ∑ x, (∏ i, p i (x i)) * Δ x)) ≤
      Real.exp (N * t ^ 2 * (∑ i, c i ^ 2) / 8) := by
  rw [sample_mgf_eq]
  have h := single_sample_mgf_le p hp hp1 Δ c hΔ t
  have h0 : 0 ≤ ∑ x, (∏ i, p i (x i)) *
      Real.exp (t * (Δ x - ∑ y, (∏ i, p i (y i)) * Δ y)) :=
    Finset.sum_nonneg fun x _ => mul_nonneg (prod_weight_nonneg p hp x) (Real.exp_pos _).le
  calc (∑ x, (∏ i, p i (x i)) * Real.exp (t * (Δ x - ∑ y, (∏ i, p i (y i)) * Δ y))) ^ N
      ≤ Real.exp (t ^ 2 * (∑ i, c i ^ 2) / 8) ^ N := pow_le_pow_left₀ h0 h N
    _ = Real.exp (N * t ^ 2 * (∑ i, c i ^ 2) / 8) := by
        rw [← Real.exp_nat_mul]
        congr 1
        ring

/-- **S1 (moment generating function of the sample sum).**  For a product reference, a residual
`Δ` with bounded differences `c`, `m = ⟨Δ⟩` and every real `t`:
`∑ ω, P ω * exp (t * ∑ k, (Δ (ω k) - m)) = (∑ x, W x * exp (t * (Δ x - m))) ^ N` and
`(∑ x, W x * exp (t * (Δ x - m))) ^ N ≤ exp (N * t² * C / 8)`. -/
theorem sample_mgf (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (t : ℝ) (N : ℕ) :
    ∑ ω : Fin N → Fin n → α, sampleWeight p N ω *
          Real.exp (t * ∑ k, (Δ (ω k) - ∑ x, (∏ i, p i (x i)) * Δ x)) =
        (∑ x, (∏ i, p i (x i)) *
          Real.exp (t * (Δ x - ∑ y, (∏ i, p i (y i)) * Δ y))) ^ N ∧
      (∑ x, (∏ i, p i (x i)) * Real.exp (t * (Δ x - ∑ y, (∏ i, p i (y i)) * Δ y))) ^ N ≤
        Real.exp (N * t ^ 2 * (∑ i, c i ^ 2) / 8) := by
  refine ⟨sample_mgf_eq p Δ _ t N, ?_⟩
  rw [← sample_mgf_eq p Δ _ t N]
  exact sample_mgf_le p hp hp1 Δ c hΔ t N

/-! ## S2. Chernoff bound and one-sided deviations of the empirical mean -/

/-- **Chernoff bound (exponential Markov inequality) for the sample sum.**  Let `E` be a set of
sample tuples on which `a ≤ t * ∑ k, (Δ (ω k) - ⟨Δ⟩)`, for some real `t` and `a`.  Then the
weight of `E` is at most `exp (N * t² * C / 8 - a)`.  No division occurs, so this form is
meaningful also for `C = 0`. -/
theorem sample_chernoff (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (N : ℕ) (t a : ℝ)
    (E : Finset (Fin N → Fin n → α))
    (hE : ∀ ω ∈ E, a ≤ t * ∑ k, (Δ (ω k) - ∑ x, (∏ i, p i (x i)) * Δ x)) :
    ∑ ω ∈ E, sampleWeight p N ω ≤ Real.exp (N * t ^ 2 * (∑ i, c i ^ 2) / 8 - a) := by
  have hP := sampleWeight_nonneg p hp N
  calc ∑ ω ∈ E, sampleWeight p N ω
      ≤ ∑ ω ∈ E, sampleWeight p N ω *
          Real.exp (t * ∑ k, (Δ (ω k) - ∑ x, (∏ i, p i (x i)) * Δ x) - a) := by
        refine Finset.sum_le_sum fun ω hω => ?_
        exact le_mul_of_one_le_right (hP ω) (Real.one_le_exp (sub_nonneg.mpr (hE ω hω)))
    _ ≤ ∑ ω, sampleWeight p N ω *
          Real.exp (t * ∑ k, (Δ (ω k) - ∑ x, (∏ i, p i (x i)) * Δ x) - a) :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ E)
          (fun ω _ _ => mul_nonneg (hP ω) (Real.exp_pos _).le)
    _ = Real.exp (-a) * ∑ ω, sampleWeight p N ω *
          Real.exp (t * ∑ k, (Δ (ω k) - ∑ x, (∏ i, p i (x i)) * Δ x)) :=
        weighted_exp_centered_eq (sampleWeight p N)
          (fun ω => t * ∑ k, (Δ (ω k) - ∑ x, (∏ i, p i (x i)) * Δ x)) a
    _ ≤ Real.exp (-a) * Real.exp (N * t ^ 2 * (∑ i, c i ^ 2) / 8) :=
        mul_le_mul_of_nonneg_left (sample_mgf_le p hp hp1 Δ c hΔ t N) (Real.exp_pos _).le
    _ = Real.exp (N * t ^ 2 * (∑ i, c i ^ 2) / 8 - a) := by
        rw [← Real.exp_add]
        congr 1
        ring

/-- The Chernoff exponent `N * t² * C / 8 - t * (N * η)` at the optimal parameter
`t = 4 * η / C` equals `-2 * N * η² / C`. -/
theorem sample_chernoff_exponent_eq (N C η : ℝ) (hC : C ≠ 0) :
    N * (4 * η / C) ^ 2 * C / 8 - 4 * η / C * (N * η) = -2 * N * η ^ 2 / C := by
  field_simp
  ring

/-- **S2 (upper tail).**  For a product reference, a residual `Δ` with bounded differences `c`
and `η ≥ 0`, the samples whose empirical mean exceeds the reference mean `m = ⟨Δ⟩` by at least
`η` have weight at most `exp (-2 * N * η² / C)`.

No assumption `0 < C` or `0 < N` is needed: if `C = 0` or `N = 0` the right-hand side is
`exp 0 = 1` (for `C = 0` by the convention `x / 0 = 0`) and the statement is trivial. -/
theorem sample_mean_upper_tail (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (η : ℝ) (hη : 0 ≤ η) (N : ℕ) :
    ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
        ∑ x, (∏ i, p i (x i)) * Δ x + η ≤ empMean Δ ω), sampleWeight p N ω ≤
      Real.exp (-2 * N * η ^ 2 / ∑ i, c i ^ 2) := by
  have hC0 : 0 ≤ ∑ i, c i ^ 2 := Finset.sum_nonneg fun i _ => sq_nonneg (c i)
  rcases hC0.eq_or_lt with hC | hC
  · rw [← hC, div_zero, Real.exp_zero]
    exact sample_event_weight_le_one p hp hp1 N _
  · refine (sample_chernoff p hp hp1 Δ c hΔ N (4 * η / ∑ i, c i ^ 2)
      (4 * η / (∑ i, c i ^ 2) * (N * η)) _ (fun ω hω => ?_)).trans (le_of_eq ?_)
    · rw [Finset.mem_filter] at hω
      rw [sample_sum_centered_eq]
      refine mul_le_mul_of_nonneg_left ?_ (div_nonneg (mul_nonneg (by norm_num) hη) hC0)
      refine mul_le_mul_of_nonneg_left ?_ (Nat.cast_nonneg N)
      linarith [hω.2]
    · rw [sample_chernoff_exponent_eq _ _ _ hC.ne']

/-- **S2 (lower tail).**  For a product reference, a residual `Δ` with bounded differences `c`
and `η ≥ 0`, the samples whose empirical mean falls below the reference mean `m = ⟨Δ⟩` by at
least `η` have weight at most `exp (-2 * N * η² / C)`.  (Trivial if `C = 0` or `N = 0`, as in
`sample_mean_upper_tail`.) -/
theorem sample_mean_lower_tail (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (η : ℝ) (hη : 0 ≤ η) (N : ℕ) :
    ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
        empMean Δ ω ≤ ∑ x, (∏ i, p i (x i)) * Δ x - η), sampleWeight p N ω ≤
      Real.exp (-2 * N * η ^ 2 / ∑ i, c i ^ 2) := by
  have hC0 : 0 ≤ ∑ i, c i ^ 2 := Finset.sum_nonneg fun i _ => sq_nonneg (c i)
  rcases hC0.eq_or_lt with hC | hC
  · rw [← hC, div_zero, Real.exp_zero]
    exact sample_event_weight_le_one p hp hp1 N _
  · refine (sample_chernoff p hp hp1 Δ c hΔ N (-(4 * η / ∑ i, c i ^ 2))
      (4 * η / (∑ i, c i ^ 2) * (N * η)) _ (fun ω hω => ?_)).trans (le_of_eq ?_)
    · rw [Finset.mem_filter] at hω
      rw [sample_sum_centered_eq, neg_mul, ← mul_neg]
      refine mul_le_mul_of_nonneg_left ?_ (div_nonneg (mul_nonneg (by norm_num) hη) hC0)
      rw [← mul_neg]
      refine mul_le_mul_of_nonneg_left ?_ (Nat.cast_nonneg N)
      linarith [hω.2]
    · rw [neg_sq, sample_chernoff_exponent_eq _ _ _ hC.ne']

/-! ## S3. Two-sided deviation of the empirical mean -/

/-- **S3 (two-sided deviation).**  For a product reference, a residual `Δ` with bounded
differences `c` and `η ≥ 0`, the samples whose empirical mean deviates from the reference mean
`m = ⟨Δ⟩` by at least `η` have weight at most `2 * exp (-2 * N * η² / C)`.  (Trivial if `C = 0`
or `N = 0`, where the right-hand side is `2`.) -/
theorem sample_mean_two_sided (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (η : ℝ) (hη : 0 ≤ η) (N : ℕ) :
    ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
        η ≤ |empMean Δ ω - ∑ x, (∏ i, p i (x i)) * Δ x|), sampleWeight p N ω ≤
      2 * Real.exp (-2 * N * η ^ 2 / ∑ i, c i ^ 2) := by
  have hU := sample_mean_upper_tail p hp hp1 Δ c hΔ η hη N
  have hL := sample_mean_lower_tail p hp hp1 Δ c hΔ η hη N
  have h := sample_weight_union_le p hp N
    (fun ω : Fin N → Fin n → α => η ≤ |empMean Δ ω - ∑ x, (∏ i, p i (x i)) * Δ x|)
    (fun ω : Fin N → Fin n → α => ∑ x, (∏ i, p i (x i)) * Δ x + η ≤ empMean Δ ω)
    (fun ω : Fin N → Fin n → α => empMean Δ ω ≤ ∑ x, (∏ i, p i (x i)) * Δ x - η)
    (fun ω h => by
      rcases le_abs.mp h with h1 | h1
      · exact Or.inl (by linarith)
      · exact Or.inr (by linarith))
  linarith

/-! ## S4. The sampled free-energy sandwich -/

/-- **Deterministic transfer.**  For a product reference and a residual `Δ` with bounded
differences `c`, *any* estimate `e` of the reference mean `m = ⟨Δ⟩` with `|e - m| ≤ η` gives the
two-sided bound
`-β * e - |β| * η ≤ log (∑ x, W x * exp (-β Δ x)) ≤ -β * e + |β| * η + β² * C / 8`. -/
theorem sandwich_of_mean_estimate (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β η e : ℝ)
    (he : |e - ∑ x, (∏ i, p i (x i)) * Δ x| ≤ η) :
    -β * e - |β| * η ≤ Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
      Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
        -β * e + |β| * η + β ^ 2 * (∑ i, c i ^ 2) / 8 := by
  obtain ⟨h1, h2⟩ := bounded_differences_sandwich p hp hp1 Δ c hΔ β
  have h3 : |β * (e - ∑ x, (∏ i, p i (x i)) * Δ x)| ≤ |β| * η := by
    rw [abs_mul]
    exact mul_le_mul_of_nonneg_left he (abs_nonneg β)
  obtain ⟨h4, h5⟩ := abs_le.mp h3
  constructor <;> linarith

/-- **S4 (the sampled free-energy sandwich).**  For a product reference
`W x = ∏ i, p i (x i)`, a residual `Δ` with bounded differences `c`, every real `β`, every
`η ≥ 0` and every number `N` of independent samples, the total weight of the sample tuples `ω`
for which the interval

`[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² * C / 8]`

does **not** contain the free-energy difference `L = log (∑ x, W x * exp (-β Δ x))` is at most
`2 * exp (-2 * N * η² / C)`, where `C = ∑ i, (c i)²`.

No assumption `0 < C` or `0 < N` is needed: if `C = 0` (convention `x / 0 = 0`) or `N = 0` the
right-hand side is `2` and the statement is trivial; for `C = 0` and `N ≥ 1` the sharp statement
is `sampled_sandwich_of_sq_sum_eq_zero`. -/
theorem sampled_free_energy_sandwich (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β η : ℝ) (hη : 0 ≤ η) (N : ℕ) :
    ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
        ¬ (-β * empMean Δ ω - |β| * η ≤
              Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
            Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
              -β * empMean Δ ω + |β| * η + β ^ 2 * (∑ i, c i ^ 2) / 8)),
        sampleWeight p N ω ≤
      2 * Real.exp (-2 * N * η ^ 2 / ∑ i, c i ^ 2) := by
  refine (sample_weight_mono p hp N _ _ (fun ω hω => ?_)).trans
    (sample_mean_two_sided p hp hp1 Δ c hΔ η hη N)
  by_contra hlt
  exact hω (sandwich_of_mean_estimate p hp hp1 Δ c hΔ β η _ (not_le.mp hlt).le)

/-- **S4 (probability of success).**  In the setting of `sampled_free_energy_sandwich`, the
sample tuples `ω` for which the interval
`[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² * C / 8]` contains
`L = log (∑ x, W x * exp (-β Δ x))` have total weight at least
`1 - 2 * exp (-2 * N * η² / C)`. -/
theorem sampled_free_energy_sandwich_good (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β η : ℝ) (hη : 0 ≤ η) (N : ℕ) :
    1 - 2 * Real.exp (-2 * N * η ^ 2 / ∑ i, c i ^ 2) ≤
      ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
        -β * empMean Δ ω - |β| * η ≤
            Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
          Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
            -β * empMean Δ ω + |β| * η + β ^ 2 * (∑ i, c i ^ 2) / 8),
        sampleWeight p N ω :=
  sample_weight_ge_of_compl_le p hp1 N _ _
    (sampled_free_energy_sandwich p hp hp1 Δ c hΔ β η hη N)

/-! ## The degenerate case `C = 0` -/

omit [Fintype α] in
/-- A residual with bounded differences `c` and `∑ i, (c i)² = 0` is constant. -/
theorem const_of_bounded_differences_sq_sum_eq_zero (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (hC : ∑ i, c i ^ 2 = 0)
    (x y : Fin n → α) : Δ x = Δ y := by
  have hc : ∀ i, c i = 0 := fun i =>
    pow_eq_zero_iff two_ne_zero |>.mp
      ((Finset.sum_eq_zero_iff_of_nonneg (fun i _ => sq_nonneg (c i))).mp hC i (Finset.mem_univ i))
  have hupd : ∀ z i a, Δ (Function.update z i a) = Δ z := by
    intro z i a
    have h := hΔ z i a
    rw [hc i] at h
    exact sub_eq_zero.mp (abs_nonpos_iff.mp h)
  -- change the coordinates of `x` into those of `y` one at a time
  have key : ∀ s : Finset (Fin n), Δ (fun i => if i ∈ s then y i else x i) = Δ x := by
    intro s
    induction s using Finset.induction_on with
    | empty => simp
    | insert j s hj ih =>
      have e : (fun i => if i ∈ insert j s then y i else x i) =
          Function.update (fun i => if i ∈ s then y i else x i) j (y j) := by
        funext i
        by_cases hij : i = j
        · subst hij
          simp
        · simp [Finset.mem_insert, hij]
      rw [e, hupd, ih]
  have h := key Finset.univ
  simpa using h.symm

/-- **S4 for `C = 0`.**  If `∑ i, (c i)² = 0` (so that the residual is constant) and there is at
least one sample, then for *every* sample tuple `ω` the interval
`[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² * C / 8]` contains
`L = log (∑ x, W x * exp (-β Δ x))`: the set of bad samples of `sampled_free_energy_sandwich` is
empty. -/
theorem sampled_sandwich_of_sq_sum_eq_zero (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a)
    (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (hC : ∑ i, c i ^ 2 = 0)
    (β η : ℝ) (hη : 0 ≤ η) {N : ℕ} (hN : 0 < N) (ω : Fin N → Fin n → α) :
    -β * empMean Δ ω - |β| * η ≤ Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
      Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
        -β * empMean Δ ω + |β| * η + β ^ 2 * (∑ i, c i ^ 2) / 8 := by
  refine sandwich_of_mean_estimate p hp hp1 Δ c hΔ β η _ ?_
  have hconst := const_of_bounded_differences_sq_sum_eq_zero Δ c hΔ hC
  have hN' : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  have he : empMean Δ ω = Δ (ω ⟨0, hN⟩) := by
    unfold empMean
    rw [Finset.sum_congr rfl (fun k _ => hconst (ω k) (ω ⟨0, hN⟩)), Finset.sum_const,
      Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    field_simp
  have hm : ∑ x, (∏ i, p i (x i)) * Δ x = Δ (ω ⟨0, hN⟩) := by
    rw [Finset.sum_congr rfl (fun x _ => by rw [hconst x (ω ⟨0, hN⟩)]), ← Finset.sum_mul,
      prod_weight_sum_one p hp1, one_mul]
  rw [he, hm, sub_self, abs_zero]
  exact hη

/-! ## S5. Sample-size form -/

/-- **S5 (sample-size form of the bound).**  If `0 < C`, `0 < δ` and
`C * log (2 / δ) ≤ N * (2 * η²)`, then the bound `2 * exp (-2 * N * η² / C)` of S3 and S4 is at
most `δ`.  (Here `0 < C` cannot be dropped: for `C = 0` the left-hand side is `2` by the
convention `x / 0 = 0`.) -/
theorem sample_size_bound (C η δ : ℝ) (N : ℕ) (hC : 0 < C) (hδ : 0 < δ)
    (hN : C * Real.log (2 / δ) ≤ N * (2 * η ^ 2)) :
    2 * Real.exp (-2 * N * η ^ 2 / C) ≤ δ := by
  have h1 : Real.log (2 / δ) ≤ 2 * N * η ^ 2 / C := by
    rw [le_div_iff₀ hC]
    linarith
  have h2 : Real.exp (-2 * N * η ^ 2 / C) ≤ Real.exp (-Real.log (2 / δ)) := by
    refine Real.exp_le_exp.mpr ?_
    have e : -2 * N * η ^ 2 / C = -(2 * N * η ^ 2 / C) := by ring
    rw [e]
    linarith
  rw [Real.exp_neg, Real.exp_log (by positivity), inv_div] at h2
  linarith

/-- **S5 (sampled sandwich, sample-size form).**  For a product reference, a residual `Δ` with
bounded differences `c`, every real `β`, `η ≥ 0`, `δ > 0` and `N ≥ 1` samples with
`C * log (2 / δ) ≤ N * (2 * η²)`, the total weight of the sample tuples `ω` for which the
interval `[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² * C / 8]` does not
contain `L = log (∑ x, W x * exp (-β Δ x))` is at most `δ`.

The case `C = 0` is included (the bad set is then empty, by
`sampled_sandwich_of_sq_sum_eq_zero`); this is where `0 < N` is used. -/
theorem sampled_free_energy_sandwich_of_sample_size (p : Fin n → α → ℝ)
    (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ)
    (c : Fin n → ℝ) (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β η : ℝ)
    (hη : 0 ≤ η) {N : ℕ} (hN : 0 < N) (δ : ℝ) (hδ : 0 < δ)
    (hsize : (∑ i, c i ^ 2) * Real.log (2 / δ) ≤ N * (2 * η ^ 2)) :
    ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
        ¬ (-β * empMean Δ ω - |β| * η ≤
              Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
            Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
              -β * empMean Δ ω + |β| * η + β ^ 2 * (∑ i, c i ^ 2) / 8)),
        sampleWeight p N ω ≤ δ := by
  have hC0 : 0 ≤ ∑ i, c i ^ 2 := Finset.sum_nonneg fun i _ => sq_nonneg (c i)
  rcases hC0.eq_or_lt with hC | hC
  · rw [Finset.sum_eq_zero]
    · exact hδ.le
    · intro ω hω
      exact absurd (sampled_sandwich_of_sq_sum_eq_zero p hp hp1 Δ c hΔ hC.symm β η hη hN ω)
        (Finset.mem_filter.mp hω).2
  · exact (sampled_free_energy_sandwich p hp hp1 Δ c hΔ β η hη N).trans
      (sample_size_bound _ η δ N hC hδ hsize)

/-- **S5 (probability of success, sample-size form).**  In the setting of
`sampled_free_energy_sandwich_of_sample_size`, the sample tuples `ω` for which the interval
`[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² * C / 8]` contains
`L = log (∑ x, W x * exp (-β Δ x))` have total weight at least `1 - δ`. -/
theorem sampled_free_energy_sandwich_good_of_sample_size (p : Fin n → α → ℝ)
    (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1) (Δ : (Fin n → α) → ℝ)
    (c : Fin n → ℝ) (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (β η : ℝ)
    (hη : 0 ≤ η) {N : ℕ} (hN : 0 < N) (δ : ℝ) (hδ : 0 < δ)
    (hsize : (∑ i, c i ^ 2) * Real.log (2 / δ) ≤ N * (2 * η ^ 2)) :
    1 - δ ≤ ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
        -β * empMean Δ ω - |β| * η ≤
            Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
          Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
            -β * empMean Δ ω + |β| * η + β ^ 2 * (∑ i, c i ^ 2) / 8),
        sampleWeight p N ω :=
  sample_weight_ge_of_compl_le p hp1 N _ _
    (sampled_free_energy_sandwich_of_sample_size p hp hp1 Δ c hΔ β η hη hN δ hδ hsize)

/-- **S5 (explicit sample size).**  Let `C₀` bound the sum of squares `C = ∑ i, (c i)²` of the
bounded-difference constants, and let `η > 0`, `δ > 0`.  Every number of samples
`N ≥ max 1 ⌈C₀ * log (2 / δ) / (2 * η²)⌉₊` guarantees that the total weight of the sample tuples
`ω` for which the interval
`[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² * C / 8]` does not contain
`L = log (∑ x, W x * exp (-β Δ x))` is at most `δ`.  The threshold involves only `C₀`, `η` and
`δ`: neither the alphabet `α`, nor the number of sites `n`, nor the reference `p`, nor `β`. -/
theorem sampled_sandwich_sample_complexity (C₀ η δ : ℝ) (hη : 0 < η) (hδ : 0 < δ)
    (p : Fin n → α → ℝ) (hp : ∀ i a, 0 ≤ p i a) (hp1 : ∀ i, ∑ a, p i a = 1)
    (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ)
    (hΔ : ∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) (hC : ∑ i, c i ^ 2 ≤ C₀) (β : ℝ)
    (N : ℕ) (hN : max 1 ⌈C₀ * Real.log (2 / δ) / (2 * η ^ 2)⌉₊ ≤ N) :
    ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
        ¬ (-β * empMean Δ ω - |β| * η ≤
              Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
            Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
              -β * empMean Δ ω + |β| * η + β ^ 2 * (∑ i, c i ^ 2) / 8)),
        sampleWeight p N ω ≤ δ := by
  have hN1 : 0 < N := lt_of_lt_of_le Nat.one_pos ((le_max_left _ _).trans hN)
  have hN2 : C₀ * Real.log (2 / δ) / (2 * η ^ 2) ≤ N :=
    Nat.ceil_le.mp ((le_max_right _ _).trans hN)
  have hη2 : 0 < 2 * η ^ 2 := by positivity
  have hC0 : 0 ≤ ∑ i, c i ^ 2 := Finset.sum_nonneg fun i _ => sq_nonneg (c i)
  rw [div_le_iff₀ hη2] at hN2
  refine sampled_free_energy_sandwich_of_sample_size p hp hp1 Δ c hΔ β η hη.le hN1 δ hδ ?_
  rcases le_or_gt 0 (Real.log (2 / δ)) with hl | hl
  · exact (mul_le_mul_of_nonneg_right hC hl).trans hN2
  · have h1 : (∑ i, c i ^ 2) * Real.log (2 / δ) ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos hC0 hl.le
    have h2 : 0 ≤ (N : ℝ) * (2 * η ^ 2) := by positivity
    linarith

end Sampling

section SampleComplexity

/-- **S5 (the sample size does not depend on the configuration space).**  For every bound `C₀`
on `C = ∑ i, (c i)²`, every accuracy `η > 0` and every failure probability `δ > 0` there is a
number of samples `N₀` (explicitly `max 1 ⌈C₀ * log (2 / δ) / (2 * η²)⌉₊`, see
`sampled_sandwich_sample_complexity`) which works simultaneously for **all** finite alphabets
`α`, all numbers of sites `n`, all product references `p`, all residuals `Δ` with bounded
differences `c` such that `C ≤ C₀`, and all `β`: for `N ≥ N₀` samples, the sample tuples whose
interval `[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² * C / 8]` misses
`L = log (∑ x, W x * exp (-β Δ x))` have total weight at most `δ`. -/
theorem exists_sampled_sandwich_sample_size (C₀ η δ : ℝ) (hη : 0 < η) (hδ : 0 < δ) :
    ∃ N₀ : ℕ, ∀ (α : Type*) [Fintype α] (n : ℕ) (p : Fin n → α → ℝ), (∀ i a, 0 ≤ p i a) →
      (∀ i, ∑ a, p i a = 1) → ∀ (Δ : (Fin n → α) → ℝ) (c : Fin n → ℝ),
      (∀ x i a, |Δ (Function.update x i a) - Δ x| ≤ c i) → ∑ i, c i ^ 2 ≤ C₀ →
      ∀ (β : ℝ) (N : ℕ), N₀ ≤ N →
        ∑ ω ∈ univ.filter (fun ω : Fin N → Fin n → α =>
            ¬ (-β * empMean Δ ω - |β| * η ≤
                  Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ∧
                Real.log (∑ x, (∏ i, p i (x i)) * Real.exp (-β * Δ x)) ≤
                  -β * empMean Δ ω + |β| * η + β ^ 2 * (∑ i, c i ^ 2) / 8)),
            sampleWeight p N ω ≤ δ :=
  ⟨max 1 ⌈C₀ * Real.log (2 / δ) / (2 * η ^ 2)⌉₊, fun _ _ _ p hp hp1 Δ c hΔ hC β N hN =>
    sampled_sandwich_sample_complexity C₀ η δ hη hδ p hp hp1 Δ c hΔ hC β N hN⟩

end SampleComplexity

/-! ## S6. Non-vacuity: a concrete instance -/

section Examples

/-- The residual of the non-vacuity instance: the number of `true` sites of a two-site Boolean
configuration.  It takes the values `0`, `1`, `2` and has bounded differences `c = (1, 1)`. -/
noncomputable def sampledCheckResidual (x : Fin 2 → Bool) : ℝ :=
  (if x 0 then 1 else 0) + (if x 1 then 1 else 0)

/-- The residual of the non-vacuity instance is not constant. -/
theorem sampledCheckResidual_nonconstant :
    sampledCheckResidual (fun _ => false) ≠ sampledCheckResidual (fun _ => true) := by
  norm_num [sampledCheckResidual]

/-- The residual of the non-vacuity instance has bounded differences `c = (1, 1)`. -/
theorem sampledCheckResidual_bounded_differences (x : Fin 2 → Bool) (i : Fin 2) (a : Bool) :
    |sampledCheckResidual (Function.update x i a) - sampledCheckResidual x| ≤ 1 := by
  have h := additive_bounded_differences
    (fun (_ : Fin 2) (b : Bool) => if b then (1 : ℝ) else 0) (fun _ => 1)
    (fun _ a b => by cases a <;> cases b <;> simp) x i a
  simpa only [sampledCheckResidual, Fin.sum_univ_two] using h

/-- Closed form of the free-energy difference of the non-vacuity instance (two sites, uniform
reference on `Bool`, residual `sampledCheckResidual`):
`log (∑ x, W x * exp (-β Δ x)) = 2 * log ((1 + exp (-β)) / 2)`. -/
theorem sampledCheck_log_partition (β : ℝ) :
    Real.log (∑ x : Fin 2 → Bool, (∏ _i : Fin 2, (1 / 2 : ℝ)) *
        Real.exp (-β * sampledCheckResidual x)) = 2 * Real.log ((1 + Real.exp (-β)) / 2) := by
  have h := additive_log_mgf (α := Bool) (n := 2) (fun _ _ => 1 / 2) (fun _ _ => by norm_num)
    (fun _ => by rw [Fintype.sum_bool]; norm_num) (fun _ b => if b then 1 else 0) β
  have e : ∑ b : Bool, (1 / 2 : ℝ) * Real.exp (-β * (if b then 1 else 0)) =
      (1 + Real.exp (-β)) / 2 := by
    rw [Fintype.sum_bool]
    simp only [if_true, Bool.false_eq_true, if_false, mul_one, mul_zero, Real.exp_zero]
    ring
  rw [Fin.sum_univ_two, e] at h
  simp only [Fin.sum_univ_two] at h
  unfold sampledCheckResidual
  rw [h]
  ring

/-- Non-vacuity of S4 (`sampled_free_energy_sandwich`): two sites, `α = Bool`, uniform site
marginals, the non-constant residual `sampledCheckResidual` with bounded differences
`c = (1, 1)` (so `C = 2`), any number `N` of samples, any `β` and any `η ≥ 0`.  All hypotheses
are jointly satisfiable, and with the closed form `L = 2 * log ((1 + exp (-β)) / 2)` the
conclusion reads: the sample tuples whose interval
`[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² / 4]` misses `L` have total
weight at most `2 * exp (-(N * η²))`. -/
theorem sampled_sandwich_check_1 (N : ℕ) (β η : ℝ) (hη : 0 ≤ η) :
    ∑ ω ∈ univ.filter (fun ω : Fin N → Fin 2 → Bool =>
        ¬ (-β * empMean sampledCheckResidual ω - |β| * η ≤
              2 * Real.log ((1 + Real.exp (-β)) / 2) ∧
            2 * Real.log ((1 + Real.exp (-β)) / 2) ≤
              -β * empMean sampledCheckResidual ω + |β| * η + β ^ 2 / 4)),
        sampleWeight (fun (_ : Fin 2) (_ : Bool) => (1 / 2 : ℝ)) N ω ≤
      2 * Real.exp (-(N * η ^ 2)) := by
  have h := sampled_free_energy_sandwich (α := Bool) (n := 2) (fun _ _ => 1 / 2)
    (fun _ _ => by norm_num) (fun _ => by rw [Fintype.sum_bool]; norm_num)
    sampledCheckResidual (fun _ => 1) sampledCheckResidual_bounded_differences β η hη N
  have eC : ∑ _i : Fin 2, (1 : ℝ) ^ 2 = 2 := by
    rw [Fin.sum_univ_two]
    norm_num
  have e1 : β ^ 2 * 2 / 8 = β ^ 2 / 4 := by ring
  have e2 : -2 * (N : ℝ) * η ^ 2 / 2 = -(N * η ^ 2) := by ring
  rw [eC, sampledCheck_log_partition, e1, e2] at h
  exact h

/-- The sample weights of the non-vacuity instance sum to one, for every number `N` of samples.
Together with `sampled_sandwich_check_1` this shows that the complementary (good) event has
weight at least `1 - 2 * exp (-(N * η²))`, see `sampled_sandwich_check_3`. -/
theorem sampled_sandwich_check_2 (N : ℕ) :
    ∑ ω : Fin N → Fin 2 → Bool, sampleWeight (fun (_ : Fin 2) (_ : Bool) => (1 / 2 : ℝ)) N ω =
      1 :=
  sampleWeight_sum_one _ (fun _ => by rw [Fintype.sum_bool]; norm_num) N

/-- Non-vacuity of `sampled_free_energy_sandwich_good` on the instance of
`sampled_sandwich_check_1`: the sample tuples whose interval
`[-β * empMean Δ ω - |β| * η,  -β * empMean Δ ω + |β| * η + β² / 4]` contains
`L = 2 * log ((1 + exp (-β)) / 2)` have total weight at least `1 - 2 * exp (-(N * η²))`. -/
theorem sampled_sandwich_check_3 (N : ℕ) (β η : ℝ) (hη : 0 ≤ η) :
    1 - 2 * Real.exp (-(N * η ^ 2)) ≤
      ∑ ω ∈ univ.filter (fun ω : Fin N → Fin 2 → Bool =>
        -β * empMean sampledCheckResidual ω - |β| * η ≤
            2 * Real.log ((1 + Real.exp (-β)) / 2) ∧
          2 * Real.log ((1 + Real.exp (-β)) / 2) ≤
            -β * empMean sampledCheckResidual ω + |β| * η + β ^ 2 / 4),
        sampleWeight (fun (_ : Fin 2) (_ : Bool) => (1 / 2 : ℝ)) N ω :=
  sample_weight_ge_of_compl_le _ (fun _ => by rw [Fintype.sum_bool]; norm_num) N _ _
    (sampled_sandwich_check_1 N β η hη)

/-- Non-vacuity of the sample-size form S5 with explicit numbers: on the instance of
`sampled_sandwich_check_1` with `β = 1`, `η = 1/2`, `δ = 1/10` and `N = 16` samples the
hypothesis `C * log (2 / δ) ≤ N * (2 * η²)` holds (it reads `2 * log 20 ≤ 8`), and the
conclusion is: with probability at least `9/10` over the `16` samples,
`-empMean Δ ω - 1/2 ≤ 2 * log ((1 + exp (-1)) / 2) ≤ -empMean Δ ω + 3/4`. -/
theorem sampled_sandwich_check_4 :
    9 / 10 ≤ ∑ ω ∈ univ.filter (fun ω : Fin 16 → Fin 2 → Bool =>
        -empMean sampledCheckResidual ω - 1 / 2 ≤ 2 * Real.log ((1 + Real.exp (-1)) / 2) ∧
          2 * Real.log ((1 + Real.exp (-1)) / 2) ≤ -empMean sampledCheckResidual ω + 3 / 4),
        sampleWeight (fun (_ : Fin 2) (_ : Bool) => (1 / 2 : ℝ)) 16 ω := by
  have eC : ∑ _i : Fin 2, (1 : ℝ) ^ 2 = 2 := by
    rw [Fin.sum_univ_two]
    norm_num
  -- `20 ≤ exp 4`, from `2.7 < exp 1`
  have hexp : (20 : ℝ) ≤ Real.exp 4 := by
    have h1 : (2.7 : ℝ) < Real.exp 1 := lt_trans (by norm_num) Real.exp_one_gt_d9
    have h2 : Real.exp 4 = Real.exp 1 ^ 4 := by
      rw [← Real.exp_nat_mul]
      norm_num
    rw [h2]
    calc (20 : ℝ) ≤ 2.7 ^ 4 := by norm_num
      _ ≤ Real.exp 1 ^ 4 := pow_le_pow_left₀ (by norm_num) h1.le 4
  have hlog : Real.log 20 ≤ 4 := (Real.log_le_iff_le_exp (by norm_num)).mpr hexp
  have hsize : (∑ _i : Fin 2, (1 : ℝ) ^ 2) * Real.log (2 / (1 / 10)) ≤
      ((16 : ℕ) : ℝ) * (2 * (1 / 2) ^ 2) := by
    rw [eC]
    norm_num
    linarith
  have h := sampled_free_energy_sandwich_good_of_sample_size (α := Bool) (n := 2)
    (fun _ _ => 1 / 2) (fun _ _ => by norm_num) (fun _ => by rw [Fintype.sum_bool]; norm_num)
    sampledCheckResidual (fun _ => 1) sampledCheckResidual_bounded_differences 1 (1 / 2)
    (by norm_num) (N := 16) (by norm_num) (1 / 10) (by norm_num) hsize
  refine le_trans (by norm_num) (h.trans (le_of_eq ?_))
  congr 1
  refine Finset.filter_congr fun ω _ => ?_
  rw [eC, sampledCheck_log_partition, abs_one]
  constructor <;> rintro ⟨h1, h2⟩ <;> constructor <;> linarith

end Examples

end MetricChain
