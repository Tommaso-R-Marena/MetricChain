/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# A lower bound for every algorithm from any law on labels, for any reference measure
# (theory report §11.32, Theorem 11.116(c); workstream Y, Lemma A)

The exponents of §§11.9–11.26 are proved for known parts that are product measures.  The step that does not need a
product is this one.  On a finite set `X` with a known part `f` (any function) and an envelope `d`, take admissible
labels `φ j`, normalise them so that their Gibbs weights `e^{-(f + φ̃_j)}` add up to one, and let

    γ* = -(1/t) log ∑_j M_j e^{-t φ̃_j}

be their soft minimum for a probability vector `M` and `t > 0`.  Then

* `softMinLabel_admissible` — `γ*` belongs to the class (the class is closed under soft minima);
* `exp_softMinLabel` — `e^{-t γ*} = ∑_j M_j e^{-t φ̃_j}`, so the exponential weights of the centre functions
  `φ̃_j - γ* - log Z(f + γ*)` add up to the same constant at every configuration;
* `renyiG_eq` — `-t · log Z(f + γ*)` is the Rényi functional `G_t(M) = -t log ∑_x (∑_j M_j π_j(x)^t)^{1/t}`;
* `softMin_expected_queries_ge` — **every randomised algorithm that is `(ε/2, δ)`-correct on the class makes at
  least `(1 - 2δ) · exp(G_t(M) - t r)` evaluations at `γ*` in expectation, for every `r > ε`**: an application of
  `genDip_expected_queries_ge_exp_weights` (theory report Theorem 11.27(b)) with those centre functions;
* `renyiG_le_log_card` — non-vacuity and consistency: the hypotheses are met by exhaustive evaluation, and the
  bound never exceeds the number of configurations.

For a chain of `n` sites with a nearest-neighbour reference measure `X` is the whole configuration space: the
lower bounds of Theorem 11.116 and Proposition 11.117 are instances.  The supremum of `G_t(M)` over `M` is the site
function `F*_X(t)` of the report (a Rényi capacity); that identification, and every evaluation of it, is on paper.
The statement and its proof are workstream Y's (Lemma A), re-derived by referee R11 and by the Scientific
Discovery Division (SCI-REV-0010).
-/
import Mathlib
import proofs.Frontiers.GeneralisedDips

namespace MetricChain

open Finset

section SoftMin

variable {X : Type*} [Fintype X] [Nonempty X] {J : Type*} [Fintype J]

/-- `log Z` of the known part `f` plus a residual `g`, at unit temperature. -/
noncomputable def logZ1 (f g : X → ℝ) : ℝ := Real.log (∑ x, Real.exp (-1 * (f x + g x)))

/-- A label shifted by a constant so that its Gibbs weights `e^{-(f + φ̃)}` add up to one. -/
noncomputable def normLabel (f φ : X → ℝ) : X → ℝ := fun x => φ x + logZ1 f φ

/-- The **soft minimum** of the normalised labels with weights `M` at the parameter `t`:
`γ*(x) = -(1/t) log ∑_j M_j e^{-t φ̃_j(x)}`. -/
noncomputable def softMinLabel (f : X → ℝ) (φ : J → X → ℝ) (M : J → ℝ) (t : ℝ) : X → ℝ :=
  fun x => -(1 / t) * Real.log (∑ j, M j * Real.exp (-t * normLabel f (φ j) x))

/-- The Rényi functional `G_t(M) = -t log ∑_x (∑_j M_j π_j(x)^t)^{1/t}` of the label law `M`, with the normalised
Gibbs laws `π_j = e^{-(f + φ̃_j)}`; powers are written with `exp` and `log`. -/
noncomputable def renyiG (f : X → ℝ) (φ : J → X → ℝ) (M : J → ℝ) (t : ℝ) : ℝ :=
  -t * Real.log (∑ x, Real.exp ((1 / t) *
    Real.log (∑ j, M j * Real.exp (-t * (f x + normLabel f (φ j) x)))))

omit [Fintype J] in
theorem sum_exp_normLabel (f φ : X → ℝ) : ∑ x, Real.exp (-1 * (f x + normLabel f φ x)) = 1 := by
  have hpos : 0 < ∑ x, Real.exp (-1 * (f x + φ x)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have h : ∀ x, Real.exp (-1 * (f x + normLabel f φ x)) =
      Real.exp (-1 * (f x + φ x)) * (∑ y, Real.exp (-1 * (f y + φ y)))⁻¹ := by
    intro x
    unfold normLabel logZ1
    rw [← Real.exp_log (inv_pos.mpr hpos), ← Real.exp_add, Real.log_inv]
    congr 1
    ring
  simp only [h]
  rw [← Finset.sum_mul]
  exact mul_inv_cancel₀ hpos.ne'

omit [Nonempty X] in
theorem softMin_sum_pos (f : X → ℝ) (φ : J → X → ℝ) {M : J → ℝ} (hM : ∀ j, 0 ≤ M j) (hM1 : ∑ j, M j = 1)
    (t : ℝ) (x : X) : 0 < ∑ j, M j * Real.exp (-t * normLabel f (φ j) x) := by
  have hex : ∃ j ∈ (univ : Finset J), (0 : ℝ) < M j := by
    apply Finset.exists_lt_of_sum_lt
    simp [hM1]
  obtain ⟨j, _, hj⟩ := hex
  exact Finset.sum_pos' (fun j _ => mul_nonneg (hM j) (Real.exp_pos _).le)
    ⟨j, mem_univ j, mul_pos hj (Real.exp_pos _)⟩

omit [Nonempty X] in
/-- The defining property of the soft minimum: `e^{-t γ*} = ∑_j M_j e^{-t φ̃_j}`. -/
theorem exp_softMinLabel (f : X → ℝ) (φ : J → X → ℝ) {M : J → ℝ} (hM : ∀ j, 0 ≤ M j) (hM1 : ∑ j, M j = 1)
    {t : ℝ} (ht : t ≠ 0) (x : X) :
    Real.exp (-t * softMinLabel f φ M t x) = ∑ j, M j * Real.exp (-t * normLabel f (φ j) x) := by
  have hpos := softMin_sum_pos f φ hM hM1 t x
  unfold softMinLabel
  have e : -t * (-(1 / t) * Real.log (∑ j, M j * Real.exp (-t * normLabel f (φ j) x))) =
      Real.log (∑ j, M j * Real.exp (-t * normLabel f (φ j) x)) := by
    field_simp
  rw [e, Real.exp_log hpos]

omit [Nonempty X] in
/-- **The class is closed under soft minima**: if every label is admissible for the envelope `d`, so is `γ*`. -/
theorem softMinLabel_admissible {d : X → X → ℝ} (f : X → ℝ) (φ : J → X → ℝ) (hφ : ∀ j, Admissible d (φ j))
    {M : J → ℝ} (hM : ∀ j, 0 ≤ M j) (hM1 : ∑ j, M j = 1) {t : ℝ} (ht : 0 < t) :
    Admissible d (softMinLabel f φ M t) := by
  intro x y
  have hx := softMin_sum_pos f φ hM hM1 t x
  have hy := softMin_sum_pos f φ hM hM1 t y
  -- S(x) ≥ S(y) e^{-t d(x, y)}
  have hS : (∑ j, M j * Real.exp (-t * normLabel f (φ j) y)) * Real.exp (-t * d x y) ≤
      ∑ j, M j * Real.exp (-t * normLabel f (φ j) x) := by
    rw [Finset.sum_mul]
    refine Finset.sum_le_sum fun j _ => ?_
    rw [mul_assoc, ← Real.exp_add]
    refine mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr ?_) (hM j)
    have h := hφ j x y
    unfold normLabel
    nlinarith
  have hlog := Real.log_le_log (mul_pos hy (Real.exp_pos _)) hS
  rw [Real.log_mul hy.ne' (Real.exp_pos _).ne', Real.log_exp] at hlog
  unfold softMinLabel
  have ht' : (0 : ℝ) < 1 / t := by positivity
  have key : -(1 / t) * Real.log (∑ j, M j * Real.exp (-t * normLabel f (φ j) x)) -
      -(1 / t) * Real.log (∑ j, M j * Real.exp (-t * normLabel f (φ j) y)) ≤ (1 / t) * (t * d x y) := by
    have := mul_le_mul_of_nonneg_left hlog ht'.le
    linarith
  have e : (1 / t) * (t * d x y) = d x y := by field_simp
  linarith

omit [Nonempty X] in
/-- The Gibbs weight of the soft minimum is the `1/t`-power of the `M`-mixture of the `t`-th powers of the label
weights; hence `G_t(M) = -t · log Z(f + γ*)`. -/
theorem renyiG_eq (f : X → ℝ) (φ : J → X → ℝ) {M : J → ℝ} (hM : ∀ j, 0 ≤ M j) (hM1 : ∑ j, M j = 1)
    {t : ℝ} (ht : t ≠ 0) : renyiG f φ M t = -t * logZ1 f (softMinLabel f φ M t) := by
  unfold renyiG logZ1
  congr 2
  refine Finset.sum_congr rfl fun x _ => ?_
  have hpos := softMin_sum_pos f φ hM hM1 t x
  have h1 : ∑ j, M j * Real.exp (-t * (f x + normLabel f (φ j) x)) =
      Real.exp (-t * f x) * ∑ j, M j * Real.exp (-t * normLabel f (φ j) x) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [mul_left_comm, ← Real.exp_add]
    congr 2
    ring
  rw [h1, Real.log_mul (Real.exp_pos _).ne' hpos.ne', Real.log_exp]
  congr 1
  unfold softMinLabel
  field_simp
  ring

variable {Ω : Type*} [Fintype Ω]

open Classical in
/-- **A lower bound for every randomised algorithm from any law on labels, on any finite space (theory report,
Theorem 11.116(c)).**  Let `f` be the known part on a finite set `X` — any function: no product structure — and `d`
any envelope function.  For admissible labels `φ j`, a probability vector `M` on them and `t > 0`, let `γ*` be the
soft minimum of the normalised labels.  Then `γ*` is admissible (`softMinLabel_admissible`), and every randomised
algorithm that returns `log Z(f + g)` within `ε/2` with probability at least `1 - δ` on every admissible residual `g`
makes on `γ*`, in expectation, at least `(1 - 2δ) · exp (G_t(M) - t r)` evaluations, for every `r > ε`
(`G_t(M) = renyiG f φ M t`).  The alternatives are the generalised dips of `γ*` with the centre functions
`φ̃_j - γ* - log Z(f + γ*)`, whose exponential weights add up to a constant. -/
theorem softMin_expected_queries_ge {d : X → X → ℝ} (f : X → ℝ) (alg : Ω → QueryAlgorithm X)
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, Admissible d g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - Real.log (∑ x, Real.exp (-1 * (f x + g x)))| ≤ ε / 2), P ω)
    (φ : J → X → ℝ) (hφ : ∀ j, Admissible d (φ j)) {M : J → ℝ} (hM : ∀ j, 0 ≤ M j) (hM1 : ∑ j, M j = 1)
    {t : ℝ} (ht : 0 < t) {r : ℝ} (hr : ε < r) :
    (1 - 2 * δ) * Real.exp (renyiG f φ M t - t * r) ≤
      ∑ ω, P ω * ((alg ω).queries (softMinLabel f φ M t)).card := by
  set γ := softMinLabel f φ M t with hγ
  have hadm : Admissible d γ := softMinLabel_admissible f φ hφ hM hM1 ht
  set Φ : J → X → ℝ := fun j x => normLabel f (φ j) x - γ x - logZ1 f γ with hΦdef
  have hΦ : ∀ j x y, Φ j x - Φ j y ≤ slack d γ x y := by
    intro j x y
    have h := hφ j x y
    show (normLabel f (φ j) x - γ x - logZ1 f γ) - (normLabel f (φ j) y - γ y - logZ1 f γ) ≤ d x y - γ x + γ y
    unfold normLabel
    linarith
  have hZγ : 0 < ∑ x, Real.exp (-1 * (f x + γ x)) := Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hgap : ∀ j, softGapOf 1 f γ (Φ j) = 0 := by
    intro j
    unfold softGapOf
    have h : ∑ x, Real.exp (-1 * (f x + γ x + Φ j x)) = ∑ x, Real.exp (-1 * (f x + γ x)) := by
      have h2 : ∀ x, Real.exp (-1 * (f x + γ x + Φ j x)) =
          Real.exp (-1 * (f x + normLabel f (φ j) x)) * ∑ y, Real.exp (-1 * (f y + γ y)) := by
        intro x
        rw [← Real.exp_log hZγ, ← Real.exp_add]
        congr 1
        show -1 * (f x + γ x + (normLabel f (φ j) x - γ x - logZ1 f γ)) = _
        unfold logZ1
        ring
      simp only [h2]
      rw [← Finset.sum_mul, sum_exp_normLabel, one_mul]
    rw [h]
    ring
  have hr' : ∀ j, softGapOf 1 f γ (Φ j) + ε < 1 * (fun _ : J => r) j := by
    intro j
    rw [hgap j]
    simpa using hr
  have hB : ∀ a, ∑ j, M j * Real.exp (-t * (Φ j a - (fun _ : J => r) j)) ≤ Real.exp (t * (r + logZ1 f γ)) := by
    intro a
    have h1 : ∀ j, M j * Real.exp (-t * (Φ j a - r)) =
        (M j * Real.exp (-t * normLabel f (φ j) a)) * Real.exp (t * γ a + t * (r + logZ1 f γ)) := by
      intro j
      rw [mul_assoc, ← Real.exp_add]
      congr 2
      show -t * (normLabel f (φ j) a - γ a - logZ1 f γ - r) = _
      ring
    simp only [h1]
    rw [← Finset.sum_mul, ← exp_softMinLabel f φ hM hM1 ht.ne' a, ← Real.exp_add]
    apply le_of_eq
    congr 1
    rw [← hγ]
    ring
  have key := genDip_expected_queries_ge_exp_weights (d := d) f alg P hP hP1 (β := 1) zero_le_one hcorr hadm Φ hΦ
    (fun _ => r) hr' ht.le M hM hB
  rw [hM1, mul_one] at key
  have hG : renyiG f φ M t - t * r = -(t * (r + logZ1 f γ)) := by
    rw [renyiG_eq f φ hM hM1 ht.ne', ← hγ]
    ring
  rw [hG, Real.exp_neg]
  have hBpos : 0 < Real.exp (t * (r + logZ1 f γ)) := Real.exp_pos _
  rw [← div_eq_mul_inv, div_le_iff₀ hBpos]
  exact key

/-- **Non-vacuity and consistency.**  The algorithm that evaluates the residual everywhere is correct on every
class with `ε = δ = 0`, so the hypotheses of `softMin_expected_queries_ge` can be met — and its bound then says that
`G_t(M)` never exceeds the logarithm of the number of configurations (up to `t r` for every `r > 0`): the lower bound
is never larger than the cost of exhaustive evaluation. -/
theorem renyiG_le_log_card {d : X → X → ℝ} (f : X → ℝ) (φ : J → X → ℝ) (hφ : ∀ j, Admissible d (φ j))
    {M : J → ℝ} (hM : ∀ j, 0 ≤ M j) (hM1 : ∑ j, M j = 1) {t : ℝ} (ht : 0 < t) {r : ℝ} (hr : 0 < r) :
    renyiG f φ M t ≤ Real.log (Fintype.card X) + t * r := by
  have hcorr : ∀ g, Admissible d g → 1 - (0 : ℝ) ≤ ∑ ω ∈ (univ : Finset Unit).filter (fun _ =>
      |(fullQueryAlgorithm (fun g => Real.log (∑ x, Real.exp (-1 * (f x + g x))))).output g -
        Real.log (∑ x, Real.exp (-1 * (f x + g x)))| ≤ (0 : ℝ) / 2), (1 : ℝ) := by
    intro g _
    simp [fullQueryAlgorithm]
  have key := softMin_expected_queries_ge (Ω := Unit) (d := d) f
    (fun _ => fullQueryAlgorithm (fun g => Real.log (∑ x, Real.exp (-1 * (f x + g x)))))
    (fun _ => 1) (fun _ => zero_le_one) (by simp) (ε := 0) (δ := 0) hcorr φ hφ hM hM1 ht hr
  have hq : ∑ ω : Unit, (1 : ℝ) * (((fullQueryAlgorithm
      (fun g => Real.log (∑ x, Real.exp (-1 * (f x + g x))))).queries (softMinLabel f φ M t)).card : ℝ) =
      (Fintype.card X : ℝ) := by
    simp [fullQueryAlgorithm]
  rw [hq] at key
  have h1 : Real.exp (renyiG f φ M t - t * r) ≤ (Fintype.card X : ℝ) := by linarith
  have h2 := Real.log_le_log (Real.exp_pos _) h1
  rw [Real.log_exp] at h2
  linarith

end SoftMin

end MetricChain

-- R13: the lines below are the only difference from the theory division's file at 63e36f7 (appended by the reviewer)
#print axioms MetricChain.softMin_expected_queries_ge
#print axioms MetricChain.softMinLabel_admissible
#print axioms MetricChain.renyiG_eq
#print axioms MetricChain.renyiG_le_log_card
#check @MetricChain.softMin_expected_queries_ge
