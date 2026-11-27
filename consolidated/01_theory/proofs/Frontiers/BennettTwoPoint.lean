import Mathlib

/-!
# The two-point Bennett–Hoeffding bound on the moment generating function, and the bracket built on it

*Provenance.*  This file was written by the Scientific Discovery Division, its workstream L4
(branch `research/scientific-translation`, `experiments/science/ws_L4/BennettTwoPoint.lean`, as
published with its message SCI-MSG-0023 at its commit `d45ad56`; SHA-256 of the original
`3688efb683694da76b3b00b96213aa253a2887eb338d88724c03eaf40a00f2e0`).  It is adopted here with its
declarations unchanged; what was changed is this paragraph and the removal of its closing block
of axiom-printing commands, heading included (the audit of `proofs/AxiomAudit.lean` walks every
declaration of this file and prints the headline ones).  It was compiled by the theory division
before adoption.  It machine-checks Theorem 11.110(f) of the theory report (§11.30): the
two-point bound (`mgf_le_bennettB`, `integral_exp_le_bennettB`, attained: `bennettB_isGreatest`),
the bracket (`remainder_bracket`, `deterministic_bracket`, and the sharper
`deterministic_bracket_sharp`), the lower bound with a ceiling (`ceiling_lower_bound`) and the
certificate with its probability (`iid_certificate_delta`).  The namespace `ScienceL4.Bennett`
is the division's and is kept.

Science division, workstream L4, Part B.  Sources: `docs/science/INFERENCE_LIMITS_ADDENDA.md`,
addendum A17 part (7) (Proposition A17.7 with its Corollary and the "two additions");
`docs/science/workstreams/L4_brief.md` Part B; the theory division's request (THY-RES-0009 §7.4,
§9.5: "the two-point Bennett bound of Theorem 11.110(f) … needs the reduction to two-point laws,
which is the whole proof").  The inequality is Hoeffding's (1963, Theorem 3, inequality (2.8));
the weaker exponential form is Bennett's (1962, (8b)).  This file imports **Mathlib only**.

A "law" is a finite type `Ω` with weights `p : Ω → ℝ`, `p ≥ 0`, `∑ p = 1`; a random variable is a
function `Ω → ℝ`; `mean p f = ∑ ω, p ω * f ω`, `variance p r = mean p ((r − mean p r)²)`.

* Part 1 — the analytic core, `key_exp_ineq`: for all real `u ≤ c`,
  `c² (e^u − 1 − u) ≤ u² (e^c − 1 − c)`, i.e. `(e^u − 1 − u)/u²` is nondecreasing on the whole line
  (from `(e^u − 1 − u)/u² = ∫₀¹ (1 − t) e^{tu} dt`).  Hence the two parabolas: `exp_le_parabola`
  (`e^x ≤ 1 + x + ψ(c) x²` for `x ≤ c`) and `parabola_le_exp` (`e^x ≥ 1 + x + ψ(−a) x²` for `x ≥ −a`).
* Part 2 — the bounds on `E e^X` for `X ≤ b`, `E X ≤ 0`, `E X² ≤ v`: `mgf_le_one_add`
  (`≤ 1 + (v/b²)(e^b − 1 − b)`, Bennett's form) and **`mgf_le_bennettB`** (`≤ bennettB b v =
  (b² e^{−v/b} + v e^b)/(b² + v)`, the two-point bound), by integrating the parabola through
  the graph of `exp` that touches it at `−v/b` and meets it at `b`.
* Part 3 — the extremal two-point law (`twoPointP`, `twoPointX`): it satisfies the hypotheses
  and attains the bound (`twoPoint_mgf`); hence `bennettB_isGreatest`.
* Part 4 — consequences obtained from the theorem and the extremal law, with no calculus:
  `bennettB` is nondecreasing in both arguments (`bennettB_mono`), `1 ≤ bennettB`,
  `bennettB ≤ 1 + (v/b²)(e^b − 1 − b)`, and `bennettB b₂ v ≤ e^{b₂ − b₁} bennettB b₁ v` for `b₁ ≤ b₂`
  (`bennettB_le_exp_mul`: `b ↦ W(b, v) − b` is nonincreasing — not in the sources).
* Part 5 — `bennettW b v = ln (bennettB b v)`: monotone, nonnegative, the chain
  `W ≤ ln(1 + (v/b²)(e^b − 1 − b)) ≤ (v/b²)(e^b − 1 − b)`.
* Part 6 — the remainder: `remainder_bracket`
  (`0 ≤ ln E e^{−(r − E r)} ≤ W(b, v) ≤ ln(1 + …) ≤ (v/b²)(e^b − 1 − b)` if `r ≥ E r − b`, `Var r ≤ v`),
  `deterministic_bracket` (the deterministic part of the certificate),
  `deterministic_bracket_sharp` (the same with `W(r̄ − η − lo, v)` in place of `W(r̄ + η − lo, v)`),
  `ceiling_lower_bound` (`ln E e^{−(r − E r)} ≥ ln(1 + Var(r)(e^{−a} − 1 + a)/a²)` if `r ≤ E r + a`).
  `bracket_of_bounds`, `bracket_of_pointwise_bounds`, `bracket_of_midpoint` (Proposition 6 of the
  P3 report: a pointwise sandwich `0 ≤ r ≤ u` gives the inputs `b = E u`, `σ² = E u²`; the
  midpoint model gives `b = (E u + U)/2`, `σ² = E u²/4`).
* Part 7 — `bennett_bracket_weights`: the bracket for weights that are not normalised, in the
  vocabulary of the theory division's `MetricChain.BoxClass.jensen_bracket`.

* Part 8 — the certificate with its probability: `chebyshev_sum`, `certificate_of_mse` (any
  estimator of the mean with a known mean-square error), `iid_sample_mean_mse` (the mean of `N`
  independent samples has mean-square error `Var r / N`), `iid_certificate`,
  `iid_certificate_delta` (`η = √(v/(Nδ))`, probability at least `1 − δ`).

Also: `integral_exp_le_bennettB` (Part 2), the two-point bound on a general probability space.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL4

namespace Bennett

open Finset

/-! ## Part 1: the key inequality — `(e^u − 1 − u)/u²` is nondecreasing on the whole line -/

/-- `∫₀¹ (1 − t) e^{tu} dt = (e^u − 1 − u)/u²` for `u ≠ 0`. -/
theorem integral_one_sub_mul_exp {u : ℝ} (hu : u ≠ 0) :
    ∫ t in (0 : ℝ)..1, (1 - t) * Real.exp (t * u) = (Real.exp u - 1 - u) / u ^ 2 := by
  have hderiv : ∀ t ∈ Set.uIcc (0 : ℝ) 1,
      HasDerivAt (fun t : ℝ => ((1 - t) / u + 1 / u ^ 2) * Real.exp (t * u))
        ((1 - t) * Real.exp (t * u)) t := by
    intro t _
    have h1 : HasDerivAt (fun t : ℝ => (1 - t) / u + 1 / u ^ 2) (-1 / u) t :=
      (((hasDerivAt_id t).const_sub 1).div_const u).add_const (1 / u ^ 2)
    have h2 : HasDerivAt (fun t : ℝ => Real.exp (t * u)) (Real.exp (t * u) * u) t := by
      have h := ((hasDerivAt_id t).mul_const u).exp
      simpa using h
    have h4 : -1 / u * Real.exp (t * u) + ((1 - t) / u + 1 / u ^ 2) * (Real.exp (t * u) * u) =
        (1 - t) * Real.exp (t * u) := by
      field_simp
      ring
    exact (h1.mul h2).congr_deriv h4
  have hint : IntervalIntegrable (fun t : ℝ => (1 - t) * Real.exp (t * u))
      MeasureTheory.volume 0 1 :=
    (by fun_prop : Continuous fun t : ℝ => (1 - t) * Real.exp (t * u)).intervalIntegrable 0 1
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint]
  simp only [one_mul, zero_mul, Real.exp_zero, sub_self, sub_zero, zero_div, zero_add, mul_one]
  field_simp
  ring

/-- The integrand is nondecreasing in `u`, hence so is the integral. -/
theorem integral_one_sub_mul_exp_mono {u c : ℝ} (h : u ≤ c) :
    ∫ t in (0 : ℝ)..1, (1 - t) * Real.exp (t * u) ≤
      ∫ t in (0 : ℝ)..1, (1 - t) * Real.exp (t * c) := by
  refine intervalIntegral.integral_mono_on zero_le_one ?_ ?_ ?_
  · exact (by fun_prop : Continuous fun t : ℝ => (1 - t) * Real.exp (t * u)).intervalIntegrable 0 1
  · exact (by fun_prop : Continuous fun t : ℝ => (1 - t) * Real.exp (t * c)).intervalIntegrable 0 1
  · intro t ht
    exact mul_le_mul_of_nonneg_left
      (Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left h ht.1)) (by linarith [ht.2])

/-- **Key inequality.**  For all real `u ≤ c`: `c² (e^u − 1 − u) ≤ u² (e^c − 1 − c)`.  This is the
monotonicity of `u ↦ (e^u − 1 − u)/u²` (value `1/2` at `0`) on the whole line, in a form without
division. -/
theorem key_exp_ineq {u c : ℝ} (h : u ≤ c) :
    c ^ 2 * (Real.exp u - 1 - u) ≤ u ^ 2 * (Real.exp c - 1 - c) := by
  by_cases hu : u = 0
  · subst hu
    simp
  by_cases hc : c = 0
  · subst hc
    simp
  have h3 := integral_one_sub_mul_exp_mono h
  rw [integral_one_sub_mul_exp hu, integral_one_sub_mul_exp hc] at h3
  have hu2 : 0 < u ^ 2 := by positivity
  have hc2 : 0 < c ^ 2 := by positivity
  rw [div_le_div_iff₀ hu2 hc2] at h3
  linarith

/-- The coefficient `ψ(c) = (e^c − 1 − c)/c²` is nonnegative. -/
theorem psi_nonneg (c : ℝ) : 0 ≤ (Real.exp c - 1 - c) / c ^ 2 :=
  div_nonneg (by linarith [Real.add_one_le_exp c]) (sq_nonneg c)

/-- **The upper parabola.**  For `x ≤ c`, `c ≠ 0`: `e^x ≤ 1 + x + ψ(c) x²`, `ψ(c) = (e^c − 1 − c)/c²`:
the parabola that touches the graph of `exp` at `0` and meets it at `c` lies above it on
`(−∞, c]`. -/
theorem exp_le_parabola {x c : ℝ} (hc : c ≠ 0) (hx : x ≤ c) :
    Real.exp x ≤ 1 + x + (Real.exp c - 1 - c) / c ^ 2 * x ^ 2 := by
  have h := key_exp_ineq hx
  have hc2 : 0 < c ^ 2 := by positivity
  have h' : Real.exp x - 1 - x ≤ (Real.exp c - 1 - c) / c ^ 2 * x ^ 2 := by
    rw [div_mul_eq_mul_div, le_div_iff₀ hc2]
    linarith
  linarith

/-- **The lower parabola.**  For `x ≥ −a`, `a ≠ 0`: `e^x ≥ 1 + x + ψ(−a) x²`,
`ψ(−a) = (e^{−a} − 1 + a)/a²`. -/
theorem parabola_le_exp {x a : ℝ} (ha : a ≠ 0) (hx : -a ≤ x) :
    1 + x + (Real.exp (-a) - 1 + a) / a ^ 2 * x ^ 2 ≤ Real.exp x := by
  have h := key_exp_ineq hx
  have e : (-a) ^ 2 = a ^ 2 := by ring
  rw [e, sub_neg_eq_add] at h
  have ha2 : 0 < a ^ 2 := by positivity
  have h' : (Real.exp (-a) - 1 + a) / a ^ 2 * x ^ 2 ≤ Real.exp x - 1 - x := by
    rw [div_mul_eq_mul_div, div_le_iff₀ ha2]
    linarith
  linarith

/-- **The parabola of the two-point bound.**  For `x ≤ b` (and `a + b ≠ 0`):
`e^x ≤ e^{−a} (1 + (x + a) + ψ(a + b) (x + a)²)` — the parabola that touches the graph of `exp` at
`−a` and meets it at `b` lies above it on `(−∞, b]`. -/
theorem exp_le_tangent_parabola {a b x : ℝ} (hab : a + b ≠ 0) (hx : x ≤ b) :
    Real.exp x ≤ Real.exp (-a) *
      (1 + (x + a) + (Real.exp (a + b) - 1 - (a + b)) / (a + b) ^ 2 * (x + a) ^ 2) := by
  have h1 := exp_le_parabola hab (show x + a ≤ a + b by linarith)
  have h2 : Real.exp x = Real.exp (-a) * Real.exp (x + a) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [h2]
  exact mul_le_mul_of_nonneg_left h1 (Real.exp_pos _).le

/-! ## Part 2: bounds on the moment generating function of a finite law -/

variable {Ω : Type*} [Fintype Ω]

/-- The two-point bound `(b² e^{−v/b} + v e^b)/(b² + v)` (`v` plays `σ²`). -/
def bennettB (b v : ℝ) : ℝ :=
  (b ^ 2 * Real.exp (-(v / b)) + v * Real.exp b) / (b ^ 2 + v)

/-- `W(b, σ²) = ln[(b² e^{−σ²/b} + σ² e^b)/(b² + σ²)]`. -/
def bennettW (b v : ℝ) : ℝ := Real.log (bennettB b v)

/-- The expectation of the tangent parabola under mean `0` and second moment `v = a·b` is the
two-point bound: `e^{−a}(1 + a + ψ(a + b)(a² + ab)) = (b² e^{−a} + ab·e^b)/(b² + ab)`. -/
theorem tangent_parabola_value {a b : ℝ} (hb : 0 < b) (ha : 0 ≤ a) :
    Real.exp (-a) * (1 + a + (Real.exp (a + b) - 1 - (a + b)) / (a + b) ^ 2 * a ^ 2 +
      (Real.exp (a + b) - 1 - (a + b)) / (a + b) ^ 2 * (a * b)) = bennettB b (a * b) := by
  have hexp : Real.exp b = Real.exp (-a) * Real.exp (a + b) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hc' : a + b ≠ 0 := by positivity
  have hd : b ^ 2 + a * b ≠ 0 := by positivity
  unfold bennettB
  rw [mul_div_cancel_right₀ a hb.ne', hexp]
  field_simp
  ring

/-- The lower half (Jensen for `exp`, in the elementary form `e^x ≥ 1 + x`):
`∑ p + ∑ p X ≤ ∑ p e^X`. -/
theorem sum_add_sum_le_mgf {p X : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) :
    ∑ ω, p ω + ∑ ω, p ω * X ω ≤ ∑ ω, p ω * Real.exp (X ω) := by
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_le_sum fun ω _ => ?_
  have := mul_le_mul_of_nonneg_left (Real.add_one_le_exp (X ω)) (hp ω)
  linarith

/-- **Bennett's form of the bound** (his inequality (8b) at the level of the moment generating
function).  If `X ≤ b` on the support (`b ≠ 0` suffices for this form; `b > 0` in the
applications), `E X ≤ 0` and `E X² ≤ v`, then `E e^X ≤ 1 + (v/b²)(e^b − 1 − b)`. -/
theorem mgf_le_one_add {p X : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {b v : ℝ}
    (hb : b ≠ 0) (hXb : ∀ ω, p ω ≠ 0 → X ω ≤ b) (hmean : ∑ ω, p ω * X ω ≤ 0)
    (hvar : ∑ ω, p ω * X ω ^ 2 ≤ v) :
    ∑ ω, p ω * Real.exp (X ω) ≤ 1 + v / b ^ 2 * (Real.exp b - 1 - b) := by
  obtain ⟨ψ, hψ⟩ : ∃ ψ : ℝ, ψ = (Real.exp b - 1 - b) / b ^ 2 := ⟨_, rfl⟩
  have hψ0 : 0 ≤ ψ := by rw [hψ]; exact psi_nonneg b
  have hpt : ∀ ω, p ω * Real.exp (X ω) ≤ p ω * (1 + X ω + ψ * X ω ^ 2) := by
    intro ω
    by_cases h0 : p ω = 0
    · simp [h0]
    · have h1 := exp_le_parabola hb (hXb ω h0)
      rw [← hψ] at h1
      exact mul_le_mul_of_nonneg_left h1 (hp ω)
  have hsum : ∑ ω, p ω * (1 + X ω + ψ * X ω ^ 2) =
      ∑ ω, p ω + ∑ ω, p ω * X ω + ψ * ∑ ω, p ω * X ω ^ 2 := by
    rw [Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun ω _ => by ring
  have h2 := mul_le_mul_of_nonneg_left hvar hψ0
  have h3 : 1 + ψ * v = 1 + v / b ^ 2 * (Real.exp b - 1 - b) := by rw [hψ]; ring
  calc ∑ ω, p ω * Real.exp (X ω) ≤ ∑ ω, p ω * (1 + X ω + ψ * X ω ^ 2) :=
        Finset.sum_le_sum fun ω _ => hpt ω
    _ = ∑ ω, p ω + ∑ ω, p ω * X ω + ψ * ∑ ω, p ω * X ω ^ 2 := hsum
    _ ≤ 1 + ψ * v := by rw [hp1]; linarith
    _ = 1 + v / b ^ 2 * (Real.exp b - 1 - b) := h3

/-- **The two-point Bennett–Hoeffding bound** (Hoeffding 1963, Theorem 3, at the level of the
moment generating function).  For a finite law: if `X ≤ b` on the support, `b > 0`, `E X ≤ 0`
and `E X² ≤ v`, then `E e^X ≤ (b² e^{−v/b} + v e^b)/(b² + v)`.

Proof: with `a = v/b` and `c = a + b`, `e^{X + a} ≤ 1 + (X + a) + ψ(c)(X + a)²` because `X + a ≤ c`
(`exp_le_parabola`); multiply by `e^{−a}` — this is the parabola through the graph of `exp` that
touches it at `−a` and meets it at `b` — and take expectations: the coefficients of `E X` and of
`E X²` are nonnegative. -/
theorem mgf_le_bennettB {p X : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {b v : ℝ}
    (hb : 0 < b) (hXb : ∀ ω, p ω ≠ 0 → X ω ≤ b) (hmean : ∑ ω, p ω * X ω ≤ 0)
    (hvar : ∑ ω, p ω * X ω ^ 2 ≤ v) :
    ∑ ω, p ω * Real.exp (X ω) ≤ bennettB b v := by
  have hv : 0 ≤ v :=
    le_trans (Finset.sum_nonneg fun ω _ => mul_nonneg (hp ω) (sq_nonneg _)) hvar
  obtain ⟨a, ha⟩ : ∃ a : ℝ, a = v / b := ⟨_, rfl⟩
  have ha0 : 0 ≤ a := by rw [ha]; exact div_nonneg hv hb.le
  have hva : v = a * b := by rw [ha]; field_simp
  subst hva
  have hc : 0 < a + b := by linarith
  have hc' : a + b ≠ 0 := hc.ne'
  obtain ⟨ψ, hψ⟩ : ∃ ψ : ℝ, ψ = (Real.exp (a + b) - 1 - (a + b)) / (a + b) ^ 2 := ⟨_, rfl⟩
  have hψ0 : 0 ≤ ψ := by rw [hψ]; exact psi_nonneg _
  have hE : 0 < Real.exp (-a) := Real.exp_pos _
  have hpt : ∀ ω, p ω * Real.exp (X ω) ≤
      p ω * (Real.exp (-a) * (1 + (X ω + a) + ψ * (X ω + a) ^ 2)) := by
    intro ω
    by_cases h0 : p ω = 0
    · simp [h0]
    · refine mul_le_mul_of_nonneg_left ?_ (hp ω)
      have h1 := exp_le_parabola hc' (show X ω + a ≤ a + b by linarith [hXb ω h0])
      rw [← hψ] at h1
      have h2 : Real.exp (X ω) = Real.exp (-a) * Real.exp (X ω + a) := by
        rw [← Real.exp_add]
        congr 1
        ring
      rw [h2]
      exact mul_le_mul_of_nonneg_left h1 hE.le
  have hsum : ∑ ω, p ω * (Real.exp (-a) * (1 + (X ω + a) + ψ * (X ω + a) ^ 2)) =
      Real.exp (-a) * ((1 + a + ψ * a ^ 2) * ∑ ω, p ω + (1 + 2 * a * ψ) * ∑ ω, p ω * X ω +
        ψ * ∑ ω, p ω * X ω ^ 2) := by
    simp only [Finset.mul_sum, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun ω _ => by ring
  have hcoef : 0 ≤ 1 + 2 * a * ψ := by positivity
  have h4 : (1 + 2 * a * ψ) * ∑ ω, p ω * X ω ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos hcoef hmean
  have h5 := mul_le_mul_of_nonneg_left hvar hψ0
  have hbound : ∑ ω, p ω * Real.exp (X ω) ≤
      Real.exp (-a) * (1 + a + ψ * a ^ 2 + ψ * (a * b)) := by
    calc ∑ ω, p ω * Real.exp (X ω)
        ≤ ∑ ω, p ω * (Real.exp (-a) * (1 + (X ω + a) + ψ * (X ω + a) ^ 2)) :=
          Finset.sum_le_sum fun ω _ => hpt ω
      _ = Real.exp (-a) * ((1 + a + ψ * a ^ 2) * ∑ ω, p ω + (1 + 2 * a * ψ) * ∑ ω, p ω * X ω +
            ψ * ∑ ω, p ω * X ω ^ 2) := hsum
      _ ≤ Real.exp (-a) * (1 + a + ψ * a ^ 2 + ψ * (a * b)) := by
          refine mul_le_mul_of_nonneg_left ?_ hE.le
          rw [hp1]
          linarith
  have halg : Real.exp (-a) * (1 + a + ψ * a ^ 2 + ψ * (a * b)) = bennettB b (a * b) := by
    rw [hψ]
    exact tangent_parabola_value hb ha0
  rw [← halg]
  exact hbound

/-- **The two-point Bennett–Hoeffding bound on a general probability space.**  If `X ≤ b` almost
surely (`b > 0`), `X` and `X²` are integrable, `E X ≤ 0` and `E X² ≤ v`, then
`E e^X ≤ (b² e^{−v/b} + v e^b)/(b² + v)`.  (Integrability of `e^X` is not a hypothesis; the
proof needs only that of the majorant, a quadratic polynomial in `X`.) -/
theorem integral_exp_le_bennettB {α : Type*} [MeasurableSpace α] {μ : MeasureTheory.Measure α}
    [MeasureTheory.IsProbabilityMeasure μ] {X : α → ℝ} {b v : ℝ} (hb : 0 < b)
    (hXb : ∀ᵐ ω ∂μ, X ω ≤ b) (hX1 : MeasureTheory.Integrable X μ)
    (hX2 : MeasureTheory.Integrable (fun ω => X ω ^ 2) μ) (hmean : ∫ ω, X ω ∂μ ≤ 0)
    (hvar : ∫ ω, X ω ^ 2 ∂μ ≤ v) :
    ∫ ω, Real.exp (X ω) ∂μ ≤ bennettB b v := by
  have hv : 0 ≤ v := le_trans (MeasureTheory.integral_nonneg fun ω => sq_nonneg (X ω)) hvar
  obtain ⟨a, ha⟩ : ∃ a : ℝ, a = v / b := ⟨_, rfl⟩
  have ha0 : 0 ≤ a := by rw [ha]; exact div_nonneg hv hb.le
  have hva : v = a * b := by rw [ha]; field_simp
  subst hva
  have hc' : a + b ≠ 0 := by positivity
  obtain ⟨ψ, hψ⟩ : ∃ ψ : ℝ, ψ = (Real.exp (a + b) - 1 - (a + b)) / (a + b) ^ 2 := ⟨_, rfl⟩
  have hψ0 : 0 ≤ ψ := by rw [hψ]; exact psi_nonneg _
  have hE : 0 < Real.exp (-a) := Real.exp_pos _
  have i1 : MeasureTheory.Integrable (fun ω => (1 + 2 * a * ψ) * X ω) μ := hX1.const_mul _
  have i2 : MeasureTheory.Integrable (fun ω => ψ * X ω ^ 2) μ := hX2.const_mul _
  have i12 : MeasureTheory.Integrable (fun ω => (1 + 2 * a * ψ) * X ω + ψ * X ω ^ 2) μ :=
    i1.add i2
  have i0 : MeasureTheory.Integrable (fun _ : α => 1 + a + ψ * a ^ 2) μ :=
    MeasureTheory.integrable_const _
  have i012 : MeasureTheory.Integrable
      (fun ω => 1 + a + ψ * a ^ 2 + ((1 + 2 * a * ψ) * X ω + ψ * X ω ^ 2)) μ := i0.add i12
  have ig : MeasureTheory.Integrable (fun ω => Real.exp (-a) *
      (1 + a + ψ * a ^ 2 + ((1 + 2 * a * ψ) * X ω + ψ * X ω ^ 2))) μ := i012.const_mul _
  have hle : (fun ω => Real.exp (X ω)) ≤ᵐ[μ] fun ω => Real.exp (-a) *
      (1 + a + ψ * a ^ 2 + ((1 + 2 * a * ψ) * X ω + ψ * X ω ^ 2)) := by
    filter_upwards [hXb] with ω hω
    have h1 := exp_le_tangent_parabola (a := a) hc' hω
    rw [← hψ] at h1
    have e : Real.exp (-a) * (1 + (X ω + a) + ψ * (X ω + a) ^ 2) = Real.exp (-a) *
        (1 + a + ψ * a ^ 2 + ((1 + 2 * a * ψ) * X ω + ψ * X ω ^ 2)) := by ring
    rw [← e]
    exact h1
  have hmono := MeasureTheory.integral_mono_of_nonneg
    (Filter.Eventually.of_forall fun ω => (Real.exp_pos (X ω)).le) ig hle
  have hint : ∫ ω, Real.exp (-a) *
        (1 + a + ψ * a ^ 2 + ((1 + 2 * a * ψ) * X ω + ψ * X ω ^ 2)) ∂μ =
      Real.exp (-a) * (1 + a + ψ * a ^ 2 +
        ((1 + 2 * a * ψ) * ∫ ω, X ω ∂μ + ψ * ∫ ω, X ω ^ 2 ∂μ)) := by
    rw [MeasureTheory.integral_const_mul, MeasureTheory.integral_add i0 i12,
      MeasureTheory.integral_add i1 i2, MeasureTheory.integral_const_mul,
      MeasureTheory.integral_const_mul, MeasureTheory.integral_const,
      MeasureTheory.probReal_univ, one_smul]
  have h4 : (1 + 2 * a * ψ) * ∫ ω, X ω ∂μ ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos (by positivity) hmean
  have h5 := mul_le_mul_of_nonneg_left hvar hψ0
  have halg : Real.exp (-a) * (1 + a + ψ * a ^ 2 + ψ * (a * b)) = bennettB b (a * b) := by
    rw [hψ]
    exact tangent_parabola_value hb ha0
  rw [← halg]
  calc ∫ ω, Real.exp (X ω) ∂μ
      ≤ ∫ ω, Real.exp (-a) *
          (1 + a + ψ * a ^ 2 + ((1 + 2 * a * ψ) * X ω + ψ * X ω ^ 2)) ∂μ := hmono
    _ = Real.exp (-a) * (1 + a + ψ * a ^ 2 +
          ((1 + 2 * a * ψ) * ∫ ω, X ω ∂μ + ψ * ∫ ω, X ω ^ 2 ∂μ)) := hint
    _ ≤ Real.exp (-a) * (1 + a + ψ * a ^ 2 + ψ * (a * b)) := by
        refine mul_le_mul_of_nonneg_left ?_ hE.le
        linarith

/-! ## Part 3: the extremal two-point law -/

/-- Weights of the extremal law: `true` is the atom at `b`, of probability `v/(b² + v)`; `false`
is the atom at `−v/b`, of probability `b²/(b² + v)`. -/
def twoPointP (b v : ℝ) : Bool → ℝ
  | true => v / (b ^ 2 + v)
  | false => b ^ 2 / (b ^ 2 + v)

/-- Values of the extremal law: `b` and `−v/b`. -/
def twoPointX (b v : ℝ) : Bool → ℝ
  | true => b
  | false => -(v / b)

theorem twoPointP_nonneg {b v : ℝ} (hv : 0 ≤ v) (s : Bool) : 0 ≤ twoPointP b v s := by
  cases s
  · show 0 ≤ b ^ 2 / (b ^ 2 + v)
    positivity
  · show 0 ≤ v / (b ^ 2 + v)
    positivity

theorem sum_twoPointP {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) : ∑ s, twoPointP b v s = 1 := by
  have h : b ^ 2 + v ≠ 0 := by positivity
  rw [Fintype.sum_bool]
  show v / (b ^ 2 + v) + b ^ 2 / (b ^ 2 + v) = 1
  rw [← add_div, add_comm, div_self h]

theorem twoPointX_le {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) (s : Bool) : twoPointX b v s ≤ b := by
  cases s
  · show -(v / b) ≤ b
    have : 0 ≤ v / b := div_nonneg hv hb.le
    linarith
  · exact le_rfl

/-- The extremal law has mean `0`. -/
theorem twoPoint_mean {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) :
    ∑ s, twoPointP b v s * twoPointX b v s = 0 := by
  have h : b ^ 2 + v ≠ 0 := by positivity
  have hb' : b ≠ 0 := hb.ne'
  rw [Fintype.sum_bool]
  show v / (b ^ 2 + v) * b + b ^ 2 / (b ^ 2 + v) * -(v / b) = 0
  field_simp
  ring

/-- The extremal law has second moment `v`. -/
theorem twoPoint_sq {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) :
    ∑ s, twoPointP b v s * twoPointX b v s ^ 2 = v := by
  have h : b ^ 2 + v ≠ 0 := by positivity
  have hb' : b ≠ 0 := hb.ne'
  rw [Fintype.sum_bool]
  show v / (b ^ 2 + v) * b ^ 2 + b ^ 2 / (b ^ 2 + v) * (-(v / b)) ^ 2 = v
  field_simp

/-- **The extremal law attains the two-point bound.** -/
theorem twoPoint_mgf (b v : ℝ) :
    ∑ s, twoPointP b v s * Real.exp (twoPointX b v s) = bennettB b v := by
  rw [Fintype.sum_bool]
  show v / (b ^ 2 + v) * Real.exp b + b ^ 2 / (b ^ 2 + v) * Real.exp (-(v / b)) =
    (b ^ 2 * Real.exp (-(v / b)) + v * Real.exp b) / (b ^ 2 + v)
  rw [div_mul_eq_mul_div, div_mul_eq_mul_div, ← add_div, add_comm]

/-- **The two-point bound is the largest value** of `E e^X` over the finite laws on a two-point
space with `X ≤ b`, `E X ≤ 0`, `E X² ≤ v` (by `mgf_le_bennettB` it is an upper bound over all
finite laws). -/
theorem bennettB_isGreatest {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) :
    IsGreatest {y : ℝ | ∃ p X : Bool → ℝ, (∀ s, 0 ≤ p s) ∧ ∑ s, p s = 1 ∧ (∀ s, X s ≤ b) ∧
        ∑ s, p s * X s ≤ 0 ∧ ∑ s, p s * X s ^ 2 ≤ v ∧ y = ∑ s, p s * Real.exp (X s)}
      (bennettB b v) := by
  constructor
  · exact ⟨twoPointP b v, twoPointX b v, twoPointP_nonneg hv, sum_twoPointP hb hv,
      twoPointX_le hb hv, (twoPoint_mean hb hv).le, (twoPoint_sq hb hv).le,
      (twoPoint_mgf b v).symm⟩
  · rintro y ⟨p, X, hp, hp1, hX, hm, hs, rfl⟩
    exact mgf_le_bennettB hp hp1 hb (fun s _ => hX s) hm hs

/-! ## Part 4: properties of the two-point bound, from the theorem and the extremal law -/

/-- **The two-point bound is nondecreasing in both arguments**: the extremal law of `(b, v)` is
admissible for `(b', v')`. -/
theorem bennettB_mono {b b' v v' : ℝ} (hb : 0 < b) (hbb : b ≤ b') (hv : 0 ≤ v) (hvv : v ≤ v') :
    bennettB b v ≤ bennettB b' v' := by
  rw [← twoPoint_mgf b v]
  exact mgf_le_bennettB (twoPointP_nonneg hv) (sum_twoPointP hb hv) (hb.trans_le hbb)
    (fun s _ => (twoPointX_le hb hv s).trans hbb) (twoPoint_mean hb hv).le
    ((twoPoint_sq hb hv).le.trans hvv)

/-- `1 ≤ bennettB b v`. -/
theorem one_le_bennettB {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) : 1 ≤ bennettB b v := by
  have h := sum_add_sum_le_mgf (X := twoPointX b v) (twoPointP_nonneg (b := b) hv)
  rw [sum_twoPointP hb hv, twoPoint_mean hb hv, twoPoint_mgf] at h
  linarith

theorem bennettB_pos {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) : 0 < bennettB b v :=
  lt_of_lt_of_le zero_lt_one (one_le_bennettB hb hv)

/-- **The middle form**: `bennettB b v ≤ 1 + (v/b²)(e^b − 1 − b)`. -/
theorem bennettB_le_one_add {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) :
    bennettB b v ≤ 1 + v / b ^ 2 * (Real.exp b - 1 - b) := by
  rw [← twoPoint_mgf b v]
  exact mgf_le_one_add (twoPointP_nonneg hv) (sum_twoPointP hb hv) hb.ne'
    (fun s _ => twoPointX_le hb hv s) (twoPoint_mean hb hv).le (twoPoint_sq hb hv).le

/-- **Raising the floor by `δ` raises the bound by at most the factor `e^δ`**: for `0 < b₁ ≤ b₂`,
`bennettB b₂ v ≤ e^{b₂ − b₁} · bennettB b₁ v`.  (Scale the extremal law of `(b₂, v)` by
`λ = b₁/b₂ ≤ 1`: `λY ≤ b₁`, `E λY = 0`, `E (λY)² ≤ v`, and `e^{Y} ≤ e^{b₂ − b₁} e^{λY}` because
`(1 − λ)(b₂ − Y) ≥ 0`.) -/
theorem bennettB_le_exp_mul {b₁ b₂ v : ℝ} (hb₁ : 0 < b₁) (hb : b₁ ≤ b₂) (hv : 0 ≤ v) :
    bennettB b₂ v ≤ Real.exp (b₂ - b₁) * bennettB b₁ v := by
  have hb₂ : 0 < b₂ := hb₁.trans_le hb
  obtain ⟨lam, hlam⟩ : ∃ lam : ℝ, lam = b₁ / b₂ := ⟨_, rfl⟩
  have hlam0 : 0 ≤ lam := by rw [hlam]; exact div_nonneg hb₁.le hb₂.le
  have hlam1 : lam ≤ 1 := by rw [hlam]; exact (div_le_one hb₂).mpr hb
  have hlb : lam * b₂ = b₁ := by rw [hlam]; field_simp
  have hbound : ∑ s, twoPointP b₂ v s * Real.exp (lam * twoPointX b₂ v s) ≤ bennettB b₁ v := by
    refine mgf_le_bennettB (twoPointP_nonneg hv) (sum_twoPointP hb₂ hv) hb₁ ?_ ?_ ?_
    · intro s _
      calc lam * twoPointX b₂ v s ≤ lam * b₂ :=
            mul_le_mul_of_nonneg_left (twoPointX_le hb₂ hv s) hlam0
        _ = b₁ := hlb
    · have e : ∑ s, twoPointP b₂ v s * (lam * twoPointX b₂ v s) =
          lam * ∑ s, twoPointP b₂ v s * twoPointX b₂ v s := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun s _ => by ring
      rw [e, twoPoint_mean hb₂ hv, mul_zero]
    · have e : ∑ s, twoPointP b₂ v s * (lam * twoPointX b₂ v s) ^ 2 =
          lam ^ 2 * ∑ s, twoPointP b₂ v s * twoPointX b₂ v s ^ 2 := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun s _ => by ring
      rw [e, twoPoint_sq hb₂ hv]
      have h1 : lam ^ 2 ≤ 1 := by nlinarith
      nlinarith
  calc bennettB b₂ v = ∑ s, twoPointP b₂ v s * Real.exp (twoPointX b₂ v s) :=
        (twoPoint_mgf b₂ v).symm
    _ ≤ ∑ s, twoPointP b₂ v s *
          (Real.exp (b₂ - b₁) * Real.exp (lam * twoPointX b₂ v s)) := by
        refine Finset.sum_le_sum fun s _ =>
          mul_le_mul_of_nonneg_left ?_ (twoPointP_nonneg hv s)
        rw [← Real.exp_add, Real.exp_le_exp]
        have h1 := mul_nonneg (sub_nonneg.mpr hlam1) (sub_nonneg.mpr (twoPointX_le hb₂ hv s))
        linarith
    _ = Real.exp (b₂ - b₁) * ∑ s, twoPointP b₂ v s * Real.exp (lam * twoPointX b₂ v s) := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun s _ => by ring
    _ ≤ Real.exp (b₂ - b₁) * bennettB b₁ v :=
        mul_le_mul_of_nonneg_left hbound (Real.exp_pos _).le

/-! ## Part 5: `W(b, σ²) = ln (bennettB b σ²)` -/

/-- `W ≥ 0`. -/
theorem bennettW_nonneg {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) : 0 ≤ bennettW b v :=
  Real.log_nonneg (one_le_bennettB hb hv)

/-- **`W` is nondecreasing in `b` and in `σ²`.** -/
theorem bennettW_mono {b b' v v' : ℝ} (hb : 0 < b) (hbb : b ≤ b') (hv : 0 ≤ v) (hvv : v ≤ v') :
    bennettW b v ≤ bennettW b' v' :=
  Real.log_le_log (bennettB_pos hb hv) (bennettB_mono hb hbb hv hvv)

/-- `W(b, σ²) ≤ ln(1 + (σ²/b²)(e^b − 1 − b))`. -/
theorem bennettW_le_log_one_add {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) :
    bennettW b v ≤ Real.log (1 + v / b ^ 2 * (Real.exp b - 1 - b)) :=
  Real.log_le_log (bennettB_pos hb hv) (bennettB_le_one_add hb hv)

/-- `ln(1 + (σ²/b²)(e^b − 1 − b)) ≤ (σ²/b²)(e^b − 1 − b)`. -/
theorem log_one_add_le {b v : ℝ} (hv : 0 ≤ v) :
    Real.log (1 + v / b ^ 2 * (Real.exp b - 1 - b)) ≤ v / b ^ 2 * (Real.exp b - 1 - b) := by
  have h0 : 0 ≤ v / b ^ 2 * (Real.exp b - 1 - b) :=
    mul_nonneg (div_nonneg hv (sq_nonneg b)) (by linarith [Real.add_one_le_exp b])
  have h := Real.log_le_sub_one_of_pos (show 0 < 1 + v / b ^ 2 * (Real.exp b - 1 - b) by linarith)
  linarith

/-- `W(b, σ²) ≤ (σ²/b²)(e^b − 1 − b)` (Bennett's exponent). -/
theorem bennettW_le {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) :
    bennettW b v ≤ v / b ^ 2 * (Real.exp b - 1 - b) :=
  (bennettW_le_log_one_add hb hv).trans (log_one_add_le hv)

/-- **`b ↦ W(b, σ²) − b` is nonincreasing**: for `0 < b₁ ≤ b₂`, `W(b₂, v) − b₂ ≤ W(b₁, v) − b₁`. -/
theorem bennettW_sub_antitone {b₁ b₂ v : ℝ} (hb₁ : 0 < b₁) (hb : b₁ ≤ b₂) (hv : 0 ≤ v) :
    bennettW b₂ v - b₂ ≤ bennettW b₁ v - b₁ := by
  have h := Real.log_le_log (bennettB_pos (hb₁.trans_le hb) hv) (bennettB_le_exp_mul hb₁ hb hv)
  rw [Real.log_mul (Real.exp_pos _).ne' (bennettB_pos hb₁ hv).ne', Real.log_exp] at h
  unfold bennettW
  linarith

/-! ## Part 6: the remainder `r` — the Jensen gap `K = ln E e^{−(r − E r)}` and the certificate -/

/-- Expectation of `f` under the weights `p`. -/
def mean (p f : Ω → ℝ) : ℝ := ∑ ω, p ω * f ω

/-- Variance of `r` under the weights `p` (a law: `p ≥ 0`, `∑ p = 1`). -/
def variance (p r : Ω → ℝ) : ℝ := mean p fun ω => (r ω - mean p r) ^ 2

theorem variance_eq (p r : Ω → ℝ) :
    variance p r = ∑ ω, p ω * (mean p r - r ω) ^ 2 := by
  show ∑ ω, p ω * (r ω - mean p r) ^ 2 = ∑ ω, p ω * (mean p r - r ω) ^ 2
  exact Finset.sum_congr rfl fun ω _ => by ring

theorem variance_nonneg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (r : Ω → ℝ) : 0 ≤ variance p r :=
  Finset.sum_nonneg fun ω _ => mul_nonneg (hp ω) (sq_nonneg _)

theorem sum_mul_const_sub (p r : Ω → ℝ) (m : ℝ) :
    ∑ ω, p ω * (m - r ω) = m * ∑ ω, p ω - ∑ ω, p ω * r ω := by
  rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun ω _ => by ring

/-- The centred variable `E r − r` has mean `0`. -/
theorem sum_centered {p : Ω → ℝ} (hp1 : ∑ ω, p ω = 1) (r : Ω → ℝ) :
    ∑ ω, p ω * (mean p r - r ω) = 0 := by
  rw [sum_mul_const_sub, hp1, mul_one]
  exact sub_self _

/-- The moment generating function of the centred remainder, as a sum. -/
theorem mean_exp_centered (p r : Ω → ℝ) :
    (mean p fun ω => Real.exp (-(r ω - mean p r))) = ∑ ω, p ω * Real.exp (mean p r - r ω) := by
  show ∑ ω, p ω * Real.exp (-(r ω - mean p r)) = ∑ ω, p ω * Real.exp (mean p r - r ω)
  exact Finset.sum_congr rfl fun ω _ => by rw [neg_sub]

/-- Jensen: `1 ≤ E e^{−(r − E r)}`. -/
theorem one_le_mean_exp_centered {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1)
    (r : Ω → ℝ) : 1 ≤ mean p fun ω => Real.exp (-(r ω - mean p r)) := by
  have h := sum_add_sum_le_mgf (X := fun ω => mean p r - r ω) hp
  rw [hp1, sum_centered hp1 r] at h
  rw [mean_exp_centered]
  linarith

/-- **The floor-plus-variance bracket of the Jensen gap** (Proposition A17.7 with the middle
form).  If `r ≥ E r − b` on the support (`b > 0`) and `Var r ≤ v`, then
`0 ≤ ln E e^{−(r − E r)} ≤ W(b, v) ≤ ln(1 + (v/b²)(e^b − 1 − b)) ≤ (v/b²)(e^b − 1 − b)`. -/
theorem remainder_bracket {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {b v : ℝ}
    (hb : 0 < b) (hfloor : ∀ ω, p ω ≠ 0 → mean p r - b ≤ r ω) (hvar : variance p r ≤ v) :
    0 ≤ Real.log (mean p fun ω => Real.exp (-(r ω - mean p r))) ∧
      Real.log (mean p fun ω => Real.exp (-(r ω - mean p r))) ≤ bennettW b v ∧
      bennettW b v ≤ Real.log (1 + v / b ^ 2 * (Real.exp b - 1 - b)) ∧
      Real.log (1 + v / b ^ 2 * (Real.exp b - 1 - b)) ≤ v / b ^ 2 * (Real.exp b - 1 - b) := by
  have hv : 0 ≤ v := (variance_nonneg hp r).trans hvar
  have h1 := one_le_mean_exp_centered hp hp1 r
  have h2 : (mean p fun ω => Real.exp (-(r ω - mean p r))) ≤ bennettB b v := by
    rw [mean_exp_centered]
    refine mgf_le_bennettB hp hp1 hb (fun ω h0 => ?_) (sum_centered hp1 r).le ?_
    · linarith [hfloor ω h0]
    · rw [← variance_eq]
      exact hvar
  exact ⟨Real.log_nonneg h1, Real.log_le_log (lt_of_lt_of_le zero_lt_one h1) h2,
    bennettW_le_log_one_add hb hv, log_one_add_le hv⟩

/-- **The upper bound of `remainder_bracket` is attained** by the two-point remainder
`r = −Y`, `Y` the extremal law: mean `0`, floor `b` below the mean, variance `v`, and
`ln E e^{−(r − E r)} = W(b, v)` ("a state at the floor of probability `σ²/(b² + σ²)`"). -/
theorem remainder_bracket_attained {b v : ℝ} (hb : 0 < b) (hv : 0 ≤ v) :
    mean (twoPointP b v) (fun s => -twoPointX b v s) = 0 ∧
      (∀ s, mean (twoPointP b v) (fun s => -twoPointX b v s) - b ≤ -twoPointX b v s) ∧
      variance (twoPointP b v) (fun s => -twoPointX b v s) = v ∧
      Real.log (mean (twoPointP b v) fun s => Real.exp
        (-(-twoPointX b v s - mean (twoPointP b v) fun s => -twoPointX b v s))) =
        bennettW b v := by
  have hm : mean (twoPointP b v) (fun s => -twoPointX b v s) = 0 := by
    show ∑ s, twoPointP b v s * -twoPointX b v s = 0
    simp only [mul_neg, Finset.sum_neg_distrib]
    rw [twoPoint_mean hb hv, neg_zero]
  refine ⟨hm, fun s => ?_, ?_, ?_⟩
  · rw [hm]
    linarith [twoPointX_le hb hv s]
  · rw [variance_eq, hm]
    refine Eq.trans (Finset.sum_congr rfl fun s _ => ?_) (twoPoint_sq hb hv)
    ring
  · rw [hm]
    unfold bennettW
    congr 1
    rw [← twoPoint_mgf b v]
    show ∑ s, twoPointP b v s * Real.exp (-(-twoPointX b v s - 0)) = _
    exact Finset.sum_congr rfl fun s _ => by rw [sub_zero, neg_neg]

/-- `E e^{−r} = e^{−E r} · E e^{−(r − E r)}`. -/
theorem mean_exp_neg (p r : Ω → ℝ) :
    (mean p fun ω => Real.exp (-r ω)) =
      Real.exp (-mean p r) * mean p fun ω => Real.exp (-(r ω - mean p r)) := by
  show ∑ ω, p ω * Real.exp (-r ω) =
    Real.exp (-mean p r) * ∑ ω, p ω * Real.exp (-(r ω - mean p r))
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun ω _ => ?_
  have h : Real.exp (-r ω) = Real.exp (-mean p r) * Real.exp (-(r ω - mean p r)) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [h]
  ring

theorem mean_exp_neg_pos {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) (r : Ω → ℝ) :
    0 < mean p fun ω => Real.exp (-r ω) := by
  rw [mean_exp_neg]
  exact mul_pos (Real.exp_pos _) (lt_of_lt_of_le zero_lt_one (one_le_mean_exp_centered hp hp1 r))

/-- `ln E e^{−r} = −E r + ln E e^{−(r − E r)}`. -/
theorem log_mean_exp_neg {p : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) (r : Ω → ℝ) :
    Real.log (mean p fun ω => Real.exp (-r ω)) =
      -mean p r + Real.log (mean p fun ω => Real.exp (-(r ω - mean p r))) := by
  have h1 := one_le_mean_exp_centered hp hp1 r
  rw [mean_exp_neg, Real.log_mul (Real.exp_pos _).ne' (lt_of_lt_of_le zero_lt_one h1).ne',
    Real.log_exp]

/-- **The deterministic part of the certificate, non-degenerate case** (Corollary of
Proposition A17.7).  If `|r̄ − E r| ≤ η`, `lo ≤ r` on the support, `Var r ≤ v` and `lo < r̄ + η`,
then `−r̄ − η ≤ ln E e^{−r} ≤ −r̄ + η + W(r̄ + η − lo, v)`. -/
theorem deterministic_bracket_of_lt {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1)
    {rbar η lo v : ℝ} (hη : |rbar - mean p r| ≤ η) (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω)
    (hvar : variance p r ≤ v) (hpos : lo < rbar + η) :
    -rbar - η ≤ Real.log (mean p fun ω => Real.exp (-r ω)) ∧
      Real.log (mean p fun ω => Real.exp (-r ω)) ≤ -rbar + η + bennettW (rbar + η - lo) v := by
  obtain ⟨h1, h2⟩ := abs_le.mp hη
  have hK := remainder_bracket hp hp1 (b := rbar + η - lo) (by linarith)
    (fun ω h0 => by linarith [hlo ω h0]) hvar
  rw [log_mean_exp_neg hp hp1]
  exact ⟨by linarith [hK.1], by linarith [hK.2.1]⟩

/-- A floor of `r` on the support is a floor of its mean. -/
theorem le_mean_of_le {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {lo : ℝ}
    (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω) : lo ≤ mean p r := by
  have h : ∑ ω, p ω * lo ≤ ∑ ω, p ω * r ω := by
    refine Finset.sum_le_sum fun ω _ => ?_
    by_cases h0 : p ω = 0
    · simp [h0]
    · exact mul_le_mul_of_nonneg_left (hlo ω h0) (hp ω)
  rw [← Finset.sum_mul, hp1, one_mul] at h
  exact h

/-- The trivial upper end: `lo ≤ r` on the support gives `ln E e^{−r} ≤ −lo`. -/
theorem log_mean_exp_neg_le {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {lo : ℝ}
    (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω) :
    Real.log (mean p fun ω => Real.exp (-r ω)) ≤ -lo := by
  have h : (mean p fun ω => Real.exp (-r ω)) ≤ Real.exp (-lo) := by
    have h' : ∑ ω, p ω * Real.exp (-r ω) ≤ ∑ ω, p ω * Real.exp (-lo) := by
      refine Finset.sum_le_sum fun ω _ => ?_
      by_cases h0 : p ω = 0
      · simp [h0]
      · exact mul_le_mul_of_nonneg_left
          (Real.exp_le_exp.mpr (by linarith [hlo ω h0])) (hp ω)
    rw [← Finset.sum_mul, hp1, one_mul] at h'
    exact h'
  have h2 := Real.log_le_log (mean_exp_neg_pos hp hp1 r) h
  rw [Real.log_exp] at h2
  exact h2

/-- With Lean's conventions for division by zero, `W(0, v) = 0` (for `v > 0` this is the limit of
`W(b, v)` as `b ↓ 0`). -/
theorem bennettW_zero_left (v : ℝ) : bennettW 0 v = 0 := by
  unfold bennettW bennettB
  by_cases hv : v = 0
  · simp [hv]
  · simp [hv]

/-- **The deterministic part of the certificate** (Corollary of Proposition A17.7), as stated in
the sources: if `|r̄ − E r| ≤ η`, `lo ≤ r` on the support and `Var r ≤ v`, then
`−r̄ − η ≤ ln E e^{−r} ≤ −r̄ + η + W(r̄ + η − lo, v)`.  (`lo ≤ r̄ + η` follows from the hypotheses;
in the boundary case `lo = r̄ + η` the term `W(0, v)` is `0` by `bennettW_zero_left`.) -/
theorem deterministic_bracket {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1)
    {rbar η lo v : ℝ} (hη : |rbar - mean p r| ≤ η) (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω)
    (hvar : variance p r ≤ v) :
    -rbar - η ≤ Real.log (mean p fun ω => Real.exp (-r ω)) ∧
      Real.log (mean p fun ω => Real.exp (-r ω)) ≤ -rbar + η + bennettW (rbar + η - lo) v := by
  obtain ⟨h1, h2⟩ := abs_le.mp hη
  have hm := le_mean_of_le hp hp1 hlo
  rcases lt_or_eq_of_le (show lo ≤ rbar + η by linarith) with hlt | heq
  · exact deterministic_bracket_of_lt hp hp1 hη hlo hvar hlt
  · have hη0 : 0 ≤ η := (abs_nonneg _).trans hη
    have hK := one_le_mean_exp_centered hp hp1 r
    have hlow := Real.log_nonneg hK
    have hup := log_mean_exp_neg_le hp hp1 hlo
    have e : rbar + η - lo = 0 := by linarith
    rw [e, bennettW_zero_left]
    constructor
    · rw [log_mean_exp_neg hp hp1]
      linarith
    · linarith

/-- **A sharper upper end of the certificate** (not in the sources).  If `|r̄ − E r| ≤ η`,
`lo ≤ r` on the support, `Var r ≤ v` and `lo < r̄ − η`, then
`ln E e^{−r} ≤ −r̄ + η + W(r̄ − η − lo, v)`: the floor width `r̄ + η − lo` of the Corollary can be
replaced by `r̄ − η − lo`, because `b ↦ W(b, v) − b` is nonincreasing. -/
theorem deterministic_bracket_sharp {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1)
    {rbar η lo v : ℝ} (hη : |rbar - mean p r| ≤ η) (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω)
    (hvar : variance p r ≤ v) (hpos : lo < rbar - η) :
    Real.log (mean p fun ω => Real.exp (-r ω)) ≤ -rbar + η + bennettW (rbar - η - lo) v := by
  obtain ⟨h1, h2⟩ := abs_le.mp hη
  have hv : 0 ≤ v := (variance_nonneg hp r).trans hvar
  have hK := remainder_bracket hp hp1 (b := mean p r - lo) (by linarith)
    (fun ω h0 => by linarith [hlo ω h0]) hvar
  have hanti := bennettW_sub_antitone (b₁ := rbar - η - lo) (b₂ := mean p r - lo) (by linarith)
    (by linarith) hv
  rw [log_mean_exp_neg hp hp1]
  linarith [hK.2.1]

/-- When `r̄ − η ≤ lo` the trivial upper end `−lo` is at most the one of the Corollary (for
`lo < r̄ + η`, `v ≥ 0`). -/
theorem neg_lo_le_bracket {rbar η lo v : ℝ} (hv : 0 ≤ v) (h : rbar - η ≤ lo)
    (hpos : lo < rbar + η) : -lo ≤ -rbar + η + bennettW (rbar + η - lo) v := by
  have := bennettW_nonneg (b := rbar + η - lo) (by linarith) hv
  linarith

/-- The sharper upper end is at most the one of the Corollary. -/
theorem deterministic_bracket_sharp_le {rbar η lo v : ℝ} (hη : 0 ≤ η) (hv : 0 ≤ v)
    (hpos : lo < rbar - η) :
    -rbar + η + bennettW (rbar - η - lo) v ≤ -rbar + η + bennettW (rbar + η - lo) v := by
  have := bennettW_mono (b := rbar - η - lo) (b' := rbar + η - lo) (by linarith) (by linarith)
    hv le_rfl
  linarith

/-- `Var r ≤ E r²`. -/
theorem variance_le_mean_sq {p : Ω → ℝ} (hp1 : ∑ ω, p ω = 1) (r : Ω → ℝ) :
    variance p r ≤ ∑ ω, p ω * r ω ^ 2 := by
  obtain ⟨m, hm⟩ : ∃ m : ℝ, m = mean p r := ⟨_, rfl⟩
  have hm' : ∑ ω, p ω * r ω = m := hm.symm
  have e1 : ∑ ω, p ω * (r ω - m) ^ 2 =
      ∑ ω, p ω * r ω ^ 2 - 2 * m * ∑ ω, p ω * r ω + m ^ 2 * ∑ ω, p ω := by
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun ω _ => by ring
  have e : variance p r = ∑ ω, p ω * (r ω - m) ^ 2 := by
    rw [hm]
    rfl
  rw [e, e1, hp1, hm']
  nlinarith [sq_nonneg m]

/-- **Pointwise bounds give the inputs of the bracket** (general form of Proposition 6 of the P3
report).  If on the support `lo ≤ r ≤ h` and `r² ≤ s`, with `lo` a constant and `h`, `s` functions
whose means are known, then the floor `b = E h − lo` and the variance bound `σ² = E s` are
admissible: `0 ≤ ln E e^{−r} + E r ≤ W(E h − lo, E s)`. -/
theorem bracket_of_bounds {p r h s : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {lo : ℝ}
    (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω) (hhi : ∀ ω, p ω ≠ 0 → r ω ≤ h ω)
    (hsq : ∀ ω, p ω ≠ 0 → r ω ^ 2 ≤ s ω) (hpos : lo < mean p h) :
    0 ≤ Real.log (mean p fun ω => Real.exp (-r ω)) + mean p r ∧
      Real.log (mean p fun ω => Real.exp (-r ω)) + mean p r ≤
        bennettW (mean p h - lo) (mean p s) := by
  have hmr : mean p r ≤ mean p h := by
    show ∑ ω, p ω * r ω ≤ ∑ ω, p ω * h ω
    refine Finset.sum_le_sum fun ω _ => ?_
    by_cases h0 : p ω = 0
    · simp [h0]
    · exact mul_le_mul_of_nonneg_left (hhi ω h0) (hp ω)
  have hv : variance p r ≤ mean p s := by
    refine (variance_le_mean_sq hp1 r).trans ?_
    show ∑ ω, p ω * r ω ^ 2 ≤ ∑ ω, p ω * s ω
    refine Finset.sum_le_sum fun ω _ => ?_
    by_cases h0 : p ω = 0
    · simp [h0]
    · exact mul_le_mul_of_nonneg_left (hsq ω h0) (hp ω)
  have hK := remainder_bracket hp hp1 (b := mean p h - lo) (by linarith)
    (fun ω h0 => by linarith [hlo ω h0]) hv
  rw [log_mean_exp_neg hp hp1]
  exact ⟨by linarith [hK.1], by linarith [hK.2.1]⟩

/-- **A sandwich gives the inputs of the bracket** (Proposition 6 (i), (iv) of the P3 report;
request P3-T3).  If `0 ≤ r ≤ u` on the support — e.g. `r = β(E − m₋)`, `u = β(m₊ − m₋)` for a
certified sandwich `m₋ ≤ E ≤ m₊`, the law being the Gibbs measure of `m₋` — then the floor
`b = E u` and the variance bound `σ² = E u²` are admissible:
`0 ≤ ln E e^{−r} + E r ≤ W(E u, E u²)`. -/
theorem bracket_of_pointwise_bounds {p r u : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1)
    (hr0 : ∀ ω, p ω ≠ 0 → 0 ≤ r ω) (hru : ∀ ω, p ω ≠ 0 → r ω ≤ u ω) (hpos : 0 < mean p u) :
    0 ≤ Real.log (mean p fun ω => Real.exp (-r ω)) + mean p r ∧
      Real.log (mean p fun ω => Real.exp (-r ω)) + mean p r ≤
        bennettW (mean p u) (mean p fun ω => u ω ^ 2) := by
  have h := bracket_of_bounds (s := fun ω => u ω ^ 2) hp hp1 hr0 hru
    (fun ω h0 => pow_le_pow_left₀ (hr0 ω h0) (hru ω h0) 2) hpos
  rw [sub_zero] at h
  exact h

theorem mean_div_const (p f : Ω → ℝ) (c : ℝ) : (mean p fun ω => f ω / c) = mean p f / c := by
  show ∑ ω, p ω * (f ω / c) = (∑ ω, p ω * f ω) / c
  rw [Finset.sum_div]
  exact Finset.sum_congr rfl fun ω _ => by ring

/-- **The midpoint model** (Proposition 6 (ii), (iv) of the P3 report).  If `|r| ≤ u/2` and `u ≤ U`
on the support (`U` a constant; `r = β(E − (m₋ + m₊)/2)`, `u = β(m₊ − m₋)`, `U = β·max(m₊ − m₋)`),
then `0 ≤ ln E e^{−r} + E r ≤ W((E u + U)/2, E u²/4)`. -/
theorem bracket_of_midpoint {p r u : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {U : ℝ}
    (hru : ∀ ω, p ω ≠ 0 → |r ω| ≤ u ω / 2) (hU : ∀ ω, p ω ≠ 0 → u ω ≤ U)
    (hpos : 0 < mean p u + U) :
    0 ≤ Real.log (mean p fun ω => Real.exp (-r ω)) + mean p r ∧
      Real.log (mean p fun ω => Real.exp (-r ω)) + mean p r ≤
        bennettW ((mean p u + U) / 2) ((mean p fun ω => u ω ^ 2) / 4) := by
  have h := bracket_of_bounds (h := fun ω => u ω / 2) (s := fun ω => u ω ^ 2 / 4) (lo := -(U / 2))
    hp hp1
    (fun ω h0 => by linarith [(abs_le.mp (hru ω h0)).1, hU ω h0])
    (fun ω h0 => (abs_le.mp (hru ω h0)).2)
    (fun ω h0 => by
      have h1 := abs_le.mp (hru ω h0)
      nlinarith [h1.1, h1.2])
    (by rw [mean_div_const]; linarith)
  rw [mean_div_const, mean_div_const] at h
  have e : mean p u / 2 - -(U / 2) = (mean p u + U) / 2 := by ring
  rw [e] at h
  exact h

/-- **The lower bound under a ceiling** (addendum A17 (7), addition (ii)).  If `r ≤ E r + a` on the
support (`a > 0`), then `ln E e^{−(r − E r)} ≥ ln(1 + Var(r)·(e^{−a} − 1 + a)/a²)`. -/
theorem ceiling_lower_bound {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {a : ℝ}
    (ha : 0 < a) (hceil : ∀ ω, p ω ≠ 0 → r ω ≤ mean p r + a) :
    Real.log (1 + variance p r * (Real.exp (-a) - 1 + a) / a ^ 2) ≤
      Real.log (mean p fun ω => Real.exp (-(r ω - mean p r))) := by
  obtain ⟨ψ, hψ⟩ : ∃ ψ : ℝ, ψ = (Real.exp (-a) - 1 + a) / a ^ 2 := ⟨_, rfl⟩
  have hψ0 : 0 ≤ ψ := by
    rw [hψ]
    exact div_nonneg (by linarith [Real.add_one_le_exp (-a)]) (sq_nonneg a)
  have hpt : ∀ ω, p ω * (1 + (mean p r - r ω) + ψ * (mean p r - r ω) ^ 2) ≤
      p ω * Real.exp (mean p r - r ω) := by
    intro ω
    by_cases h0 : p ω = 0
    · simp [h0]
    · have h1 := parabola_le_exp ha.ne' (show -a ≤ mean p r - r ω by linarith [hceil ω h0])
      rw [← hψ] at h1
      exact mul_le_mul_of_nonneg_left h1 (hp ω)
  have hsum : ∑ ω, p ω * (1 + (mean p r - r ω) + ψ * (mean p r - r ω) ^ 2) =
      ∑ ω, p ω + ∑ ω, p ω * (mean p r - r ω) + ψ * ∑ ω, p ω * (mean p r - r ω) ^ 2 := by
    rw [Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun ω _ => by ring
  have hle : 1 + variance p r * (Real.exp (-a) - 1 + a) / a ^ 2 ≤
      mean p fun ω => Real.exp (-(r ω - mean p r)) := by
    rw [mean_exp_centered]
    have h := Finset.sum_le_sum fun ω (_ : ω ∈ Finset.univ) => hpt ω
    rw [hsum, hp1, sum_centered hp1 r, ← variance_eq] at h
    have e : variance p r * (Real.exp (-a) - 1 + a) / a ^ 2 = ψ * variance p r := by
      rw [hψ]
      ring
    rw [e]
    linarith
  have hpos : 0 < 1 + variance p r * (Real.exp (-a) - 1 + a) / a ^ 2 := by
    have e : variance p r * (Real.exp (-a) - 1 + a) / a ^ 2 = ψ * variance p r := by
      rw [hψ]
      ring
    rw [e]
    have := mul_nonneg hψ0 (variance_nonneg hp r)
    linarith
  exact Real.log_le_log hpos hle

/-! ## Part 7: unnormalised weights — the format of the theory division's `jensen_bracket` -/

/-- **The floor-plus-variance bracket for weights that are not normalised** (Theorem 11.110(f) of
the theory report in the vocabulary of `MetricChain.BoxClass.jensen_bracket`: `w ≥ 0` the Gibbs
weights of the known function, `Z₀ = ∑ w`, `Z = ∑ w e^{−r}` (their `Zw w r`),
`m = (∑ w r)/Z₀` the mean of the remainder).  If `r ≥ m − b` wherever `w ≠ 0` (`b > 0`) and the
variance `(∑ w (r − m)²)/Z₀` is at most `v`, then
`ln Z₀ − m ≤ ln Z ≤ ln Z₀ − m + W(b, v)`.
The left inequality is `jensen_bracket` (re-proved here); the right one is the new half. -/
theorem bennett_bracket_weights {w r : Ω → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : Ω} (hx₀ : 0 < w x₀)
    {b v : ℝ} (hb : 0 < b)
    (hfloor : ∀ x, w x ≠ 0 → (∑ y, w y * r y) / ∑ y, w y - b ≤ r x)
    (hvar : (∑ x, w x * (r x - (∑ y, w y * r y) / ∑ y, w y) ^ 2) / ∑ y, w y ≤ v) :
    Real.log (∑ x, w x) - (∑ x, w x * r x) / ∑ x, w x ≤
        Real.log (∑ x, w x * Real.exp (-r x)) ∧
      Real.log (∑ x, w x * Real.exp (-r x)) ≤
        Real.log (∑ x, w x) - (∑ x, w x * r x) / ∑ x, w x + bennettW b v := by
  have hW : 0 < ∑ x, w x :=
    Finset.sum_pos' (fun x _ => hw x) ⟨x₀, Finset.mem_univ x₀, hx₀⟩
  obtain ⟨W₀, hW₀⟩ : ∃ W₀ : ℝ, W₀ = ∑ x, w x := ⟨_, rfl⟩
  rw [← hW₀] at hW hfloor hvar ⊢
  obtain ⟨m, hm⟩ : ∃ m : ℝ, m = (∑ x, w x * r x) / W₀ := ⟨_, rfl⟩
  rw [← hm] at hfloor hvar ⊢
  have hp : ∀ x, 0 ≤ w x / W₀ := fun x => div_nonneg (hw x) hW.le
  have hp1 : ∑ x, w x / W₀ = 1 := by rw [← Finset.sum_div, ← hW₀, div_self hW.ne']
  have hmean : mean (fun x => w x / W₀) r = m := by
    show ∑ x, w x / W₀ * r x = m
    rw [hm, Finset.sum_div]
    exact Finset.sum_congr rfl fun x _ => by ring
  have hvar' : variance (fun x => w x / W₀) r = (∑ x, w x * (r x - m) ^ 2) / W₀ := by
    show ∑ x, w x / W₀ * (r x - mean (fun x => w x / W₀) r) ^ 2 = _
    rw [hmean, Finset.sum_div]
    exact Finset.sum_congr rfl fun x _ => by ring
  have hmgf : (mean (fun x => w x / W₀) fun x => Real.exp (-r x)) =
      (∑ x, w x * Real.exp (-r x)) / W₀ := by
    show ∑ x, w x / W₀ * Real.exp (-r x) = _
    rw [Finset.sum_div]
    exact Finset.sum_congr rfl fun x _ => by ring
  have hfloor' : ∀ x, w x / W₀ ≠ 0 → mean (fun x => w x / W₀) r - b ≤ r x := by
    intro x h0
    rw [hmean]
    exact hfloor x fun h => h0 (by rw [h, zero_div])
  have hvar'' : variance (fun x => w x / W₀) r ≤ v := by
    rw [hvar']
    exact hvar
  have hK := remainder_bracket (v := v) hp hp1 hb hfloor' hvar''
  have hsum : ∑ x, w x * Real.exp (-r x) =
      W₀ * mean (fun x => w x / W₀) fun x => Real.exp (-r x) := by
    rw [hmgf, mul_div_cancel₀ _ hW.ne']
  rw [hsum, Real.log_mul hW.ne' (mean_exp_neg_pos hp hp1 r).ne', log_mean_exp_neg hp hp1]
  exact ⟨by linarith [hK.1, hmean], by linarith [hK.2.1, hmean]⟩

/-! ## Part 8: the certificate with its probability (Corollary of Proposition A17.7) -/

/-- **Chebyshev's inequality for a finite law**, in the form without division:
`η² · P(|R − m| > η) ≤ E (R − m)²`. -/
theorem chebyshev_sum {Ω' : Type*} [Fintype Ω'] {P : Ω' → ℝ} (hP : ∀ ω, 0 ≤ P ω) (R : Ω' → ℝ)
    (m : ℝ) {η : ℝ} (hη : 0 ≤ η) :
    η ^ 2 * ∑ ω ∈ univ.filter (fun ω => η < |R ω - m|), P ω ≤ ∑ ω, P ω * (R ω - m) ^ 2 := by
  rw [Finset.mul_sum]
  calc ∑ ω ∈ univ.filter (fun ω => η < |R ω - m|), η ^ 2 * P ω
      ≤ ∑ ω ∈ univ.filter (fun ω => η < |R ω - m|), P ω * (R ω - m) ^ 2 := by
        refine Finset.sum_le_sum fun ω hω => ?_
        have h := (Finset.mem_filter.mp hω).2
        have h2 : η ^ 2 ≤ (R ω - m) ^ 2 := by
          rw [← sq_abs (R ω - m)]
          exact pow_le_pow_left₀ hη h.le 2
        nlinarith [hP ω]
    _ ≤ ∑ ω, P ω * (R ω - m) ^ 2 :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
          fun ω _ _ => mul_nonneg (hP ω) (sq_nonneg _)

/-- **The certificate for any estimator of the mean with a known mean-square error.**  Let
`(Ω, p)` be the law of the model and `r` the remainder with a floor `lo` on the support and
`Var r ≤ v`.  Let `(Ω', P)` be any finite law (the randomness of the estimator) and
`rbar : Ω' → ℝ` an estimator with `E (rbar − E r)² ≤ s2`.  Then for every `η > 0`, with
`P`-probability at least `1 − s2/η²`,
`−rbar − η ≤ ln E e^{−r} ≤ −rbar + η + W(rbar + η − lo, v)`. -/
theorem certificate_of_mse {Ω' : Type*} [Fintype Ω'] {P : Ω' → ℝ} (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω) (hp1 : ∑ ω, p ω = 1) {lo v s2 η : ℝ}
    (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω) (hvar : variance p r ≤ v) (rbar : Ω' → ℝ)
    (hmse : ∑ ω', P ω' * (rbar ω' - mean p r) ^ 2 ≤ s2) (hη : 0 < η) :
    1 - s2 / η ^ 2 ≤ ∑ ω' ∈ univ.filter (fun ω' =>
        -rbar ω' - η ≤ Real.log (mean p fun ω => Real.exp (-r ω)) ∧
          Real.log (mean p fun ω => Real.exp (-r ω)) ≤
            -rbar ω' + η + bennettW (rbar ω' + η - lo) v), P ω' := by
  have hη2 : 0 < η ^ 2 := by positivity
  have hcheb := (chebyshev_sum hP rbar (mean p r) hη.le).trans hmse
  have hbad : ∑ ω' ∈ univ.filter (fun ω' => η < |rbar ω' - mean p r|), P ω' ≤ s2 / η ^ 2 := by
    rw [le_div_iff₀ hη2]
    linarith
  have hsplit := Finset.sum_filter_add_sum_filter_not (univ : Finset Ω')
    (fun ω' => η < |rbar ω' - mean p r|) P
  rw [hP1] at hsplit
  have hsub : ∑ ω' ∈ univ.filter (fun ω' => ¬ η < |rbar ω' - mean p r|), P ω' ≤
      ∑ ω' ∈ univ.filter (fun ω' =>
        -rbar ω' - η ≤ Real.log (mean p fun ω => Real.exp (-r ω)) ∧
          Real.log (mean p fun ω => Real.exp (-r ω)) ≤
            -rbar ω' + η + bennettW (rbar ω' + η - lo) v), P ω' := by
    refine Finset.sum_le_sum_of_subset_of_nonneg (fun ω' hω' => ?_) fun ω' _ _ => hP ω'
    have h := not_lt.mp (Finset.mem_filter.mp hω').2
    exact Finset.mem_filter.mpr ⟨Finset.mem_univ ω', deterministic_bracket hp hp1 h hlo hvar⟩
  linarith

/-- Under the product law `∏ p` on `Fin N → Ω`, the expectation of a product of a function of
the coordinate `i` and a function of the coordinate `j` is `E (f g)` if `i = j` and `E f · E g`
otherwise. -/
theorem sum_prod_mul_two {N : ℕ} {p : Ω → ℝ} (hp1 : ∑ a, p a = 1) (f g : Ω → ℝ) (i j : Fin N) :
    ∑ ω : Fin N → Ω, (∏ k, p (ω k)) * (f (ω i) * g (ω j)) =
      if i = j then ∑ a, p a * (f a * g a) else (∑ a, p a * f a) * ∑ a, p a * g a := by
  have key : ∀ ω : Fin N → Ω, (∏ k, p (ω k)) * (f (ω i) * g (ω j)) =
      ∏ k, (p (ω k) * ((if k = i then f (ω k) else 1) * (if k = j then g (ω k) else 1))) := by
    intro ω
    rw [Finset.prod_mul_distrib, Finset.prod_mul_distrib, Finset.prod_ite_eq',
      Finset.prod_ite_eq']
    simp
  have hG := (Fintype.prod_sum (fun (k : Fin N) (a : Ω) =>
    p a * ((if k = i then f a else 1) * (if k = j then g a else 1)))).symm
  calc ∑ ω : Fin N → Ω, (∏ k, p (ω k)) * (f (ω i) * g (ω j))
      = ∑ ω : Fin N → Ω,
          ∏ k, (p (ω k) * ((if k = i then f (ω k) else 1) * (if k = j then g (ω k) else 1))) :=
        Finset.sum_congr rfl fun ω _ => key ω
    _ = ∏ k : Fin N, ∑ a, p a * ((if k = i then f a else 1) * (if k = j then g a else 1)) := hG
    _ = if i = j then ∑ a, p a * (f a * g a) else (∑ a, p a * f a) * ∑ a, p a * g a := by
        by_cases hij : i = j
        · subst hij
          rw [if_pos rfl]
          have hk : ∀ k : Fin N,
              ∑ a, p a * ((if k = i then f a else 1) * (if k = i then g a else 1)) =
                if k = i then ∑ a, p a * (f a * g a) else 1 := by
            intro k
            by_cases hki : k = i
            · simp [hki]
            · simp [hki, hp1]
          simp only [hk]
          rw [Finset.prod_ite_eq']
          simp
        · rw [if_neg hij]
          have hk : ∀ k : Fin N,
              ∑ a, p a * ((if k = i then f a else 1) * (if k = j then g a else 1)) =
                (if k = i then ∑ a, p a * f a else 1) * (if k = j then ∑ a, p a * g a else 1) := by
            intro k
            by_cases hki : k = i
            · have hkj : ¬ k = j := fun h => hij (hki.symm.trans h)
              simp [hki, hij]
            · by_cases hkj : k = j
              · have hji : ¬ j = i := fun h => hij h.symm
                simp [hkj, hji]
              · simp [hki, hkj, hp1]
          simp only [hk]
          rw [Finset.prod_mul_distrib, Finset.prod_ite_eq', Finset.prod_ite_eq']
          simp

/-- **The mean-square error of the mean of `N` independent samples is `Var r / N`.** -/
theorem iid_sample_mean_mse {N : ℕ} (hN : 0 < N) {p : Ω → ℝ} (hp1 : ∑ a, p a = 1) (r : Ω → ℝ) :
    ∑ ω : Fin N → Ω, (∏ k, p (ω k)) * ((∑ i, r (ω i)) / N - mean p r) ^ 2 =
      variance p r / N := by
  obtain ⟨m, hm⟩ : ∃ m : ℝ, m = mean p r := ⟨_, rfl⟩
  have hN0 : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  have hc0 : ∑ a, p a * (r a - m) = 0 := by
    have h := sum_centered hp1 r
    rw [← hm] at h
    have e : ∑ a, p a * (r a - m) = -∑ a, p a * (m - r a) := by
      rw [← Finset.sum_neg_distrib]
      exact Finset.sum_congr rfl fun a _ => by ring
    rw [e, h, neg_zero]
  have hc2 : ∑ a, p a * ((r a - m) * (r a - m)) = variance p r := by
    rw [hm]
    show _ = ∑ a, p a * (r a - mean p r) ^ 2
    exact Finset.sum_congr rfl fun a _ => by ring
  have hterm : ∀ ω : Fin N → Ω, (∏ k, p (ω k)) * ((∑ i, r (ω i)) / N - m) ^ 2 =
      (1 / (N : ℝ) ^ 2) *
        ∑ i, ∑ j, (∏ k, p (ω k)) * ((r (ω i) - m) * (r (ω j) - m)) := by
    intro ω
    have h1 : (∑ i : Fin N, r (ω i)) / N - m = (∑ i : Fin N, (r (ω i) - m)) / N := by
      rw [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
        nsmul_eq_mul]
      field_simp
    have h2 : (∑ i : Fin N, (r (ω i) - m)) ^ 2 = ∑ i, ∑ j, (r (ω i) - m) * (r (ω j) - m) := by
      rw [sq, Finset.sum_mul_sum]
    have h3 : ∑ i, ∑ j, (∏ k, p (ω k)) * ((r (ω i) - m) * (r (ω j) - m)) =
        (∏ k, p (ω k)) * ∑ i, ∑ j, (r (ω i) - m) * (r (ω j) - m) := by
      rw [Finset.mul_sum]
      exact Finset.sum_congr rfl fun i _ => by rw [Finset.mul_sum]
    rw [h1, div_pow, h2, h3]
    ring
  have hpair : ∀ i j : Fin N,
      ∑ ω : Fin N → Ω, (∏ k, p (ω k)) * ((r (ω i) - m) * (r (ω j) - m)) =
        if i = j then variance p r else 0 := by
    intro i j
    rw [sum_prod_mul_two hp1 (fun a => r a - m) (fun a => r a - m) i j]
    by_cases hij : i = j
    · rw [if_pos hij, if_pos hij, hc2]
    · rw [if_neg hij, if_neg hij, hc0, zero_mul]
  rw [← hm]
  calc ∑ ω : Fin N → Ω, (∏ k, p (ω k)) * ((∑ i, r (ω i)) / N - m) ^ 2
      = ∑ ω : Fin N → Ω, (1 / (N : ℝ) ^ 2) *
          ∑ i, ∑ j, (∏ k, p (ω k)) * ((r (ω i) - m) * (r (ω j) - m)) :=
        Finset.sum_congr rfl fun ω _ => hterm ω
    _ = (1 / (N : ℝ) ^ 2) * ∑ i : Fin N, ∑ j : Fin N,
          ∑ ω : Fin N → Ω, (∏ k, p (ω k)) * ((r (ω i) - m) * (r (ω j) - m)) := by
        rw [← Finset.mul_sum]
        congr 1
        rw [Finset.sum_comm]
        exact Finset.sum_congr rfl fun i _ => Finset.sum_comm
    _ = (1 / (N : ℝ) ^ 2) * ∑ i : Fin N, ∑ j : Fin N, (if i = j then variance p r else 0) := by
        congr 1
        exact Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => hpair i j
    _ = variance p r / N := by
        simp only [Finset.sum_ite_eq, Finset.mem_univ, if_true, Finset.sum_const,
          Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
        field_simp

/-- The product law is a law. -/
theorem sum_prod_eq_one {N : ℕ} {p : Ω → ℝ} (hp1 : ∑ a, p a = 1) :
    ∑ ω : Fin N → Ω, ∏ i, p (ω i) = 1 := by
  rw [← Fintype.prod_sum (fun (_ : Fin N) (a : Ω) => p a)]
  simp [hp1]

/-- **The certificate from `N` independent samples of the model** (Corollary of Proposition
A17.7; Theorem 11.110(f) of the theory report).  `r` has a floor `lo` on the support and
`Var r ≤ v`; `ω : Fin N → Ω` are `N` independent samples of `p`, `r̄ = (1/N) ∑ r(ω_i)`.  For every
`η > 0`, with probability at least `1 − v/(N η²)`,
`−r̄ − η ≤ ln E e^{−r} ≤ −r̄ + η + W(r̄ + η − lo, v)`. -/
theorem iid_certificate {N : ℕ} (hN : 0 < N) {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω)
    (hp1 : ∑ ω, p ω = 1) {lo v η : ℝ} (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω) (hvar : variance p r ≤ v)
    (hη : 0 < η) :
    1 - v / (N * η ^ 2) ≤ ∑ ω ∈ (univ : Finset (Fin N → Ω)).filter (fun ω =>
        -((∑ i, r (ω i)) / N) - η ≤ Real.log (mean p fun x => Real.exp (-r x)) ∧
          Real.log (mean p fun x => Real.exp (-r x)) ≤
            -((∑ i, r (ω i)) / N) + η + bennettW ((∑ i, r (ω i)) / N + η - lo) v),
        ∏ i, p (ω i) := by
  have hP : ∀ ω : Fin N → Ω, 0 ≤ ∏ i, p (ω i) := fun ω =>
    Finset.prod_nonneg fun i _ => hp (ω i)
  have hmse : ∑ ω : Fin N → Ω, (∏ i, p (ω i)) * ((∑ i, r (ω i)) / N - mean p r) ^ 2 ≤ v / N := by
    rw [iid_sample_mean_mse hN hp1 r]
    exact div_le_div_of_nonneg_right hvar (Nat.cast_nonneg N)
  have h := certificate_of_mse hP (sum_prod_eq_one hp1) hp hp1 hlo hvar
    (fun ω : Fin N → Ω => (∑ i, r (ω i)) / N) hmse hη
  rw [div_div] at h
  exact h

/-- **The certificate at confidence `1 − δ`** with `η = √(v/(Nδ))` (`= σ/√(Nδ)` for `v = σ²`):
with probability at least `1 − δ`, `−r̄ − η ≤ ln E e^{−r} ≤ −r̄ + η + W(r̄ + η − lo, v)`. -/
theorem iid_certificate_delta {N : ℕ} (hN : 0 < N) {p r : Ω → ℝ} (hp : ∀ ω, 0 ≤ p ω)
    (hp1 : ∑ ω, p ω = 1) {lo v δ : ℝ} (hlo : ∀ ω, p ω ≠ 0 → lo ≤ r ω) (hvar : variance p r ≤ v)
    (hv : 0 < v) (hδ : 0 < δ) :
    1 - δ ≤ ∑ ω ∈ (univ : Finset (Fin N → Ω)).filter (fun ω =>
        -((∑ i, r (ω i)) / N) - Real.sqrt (v / (N * δ)) ≤
            Real.log (mean p fun x => Real.exp (-r x)) ∧
          Real.log (mean p fun x => Real.exp (-r x)) ≤
            -((∑ i, r (ω i)) / N) + Real.sqrt (v / (N * δ)) +
              bennettW ((∑ i, r (ω i)) / N + Real.sqrt (v / (N * δ)) - lo) v),
        ∏ i, p (ω i) := by
  have hNpos : (0 : ℝ) < (N : ℝ) := Nat.cast_pos.mpr hN
  have hq : 0 < v / (N * δ) := by positivity
  have h := iid_certificate hN hp hp1 hlo hvar (Real.sqrt_pos.mpr hq)
  rw [Real.sq_sqrt hq.le] at h
  have e : v / (N * (v / (N * δ))) = δ := by
    field_simp
  rw [e] at h
  exact h

end Bennett

end ScienceL4
