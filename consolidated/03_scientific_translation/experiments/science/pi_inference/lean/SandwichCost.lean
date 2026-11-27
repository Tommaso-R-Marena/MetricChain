/-
Science division (coordinator), addendum A17 (16), Lemma A17.16: the cost of a sandwich is its mean band.

For a probability vector `w` on a finite set (the Gibbs measure of the true energy) and functions
`a = β (E − m₋) ≥ 0`, `b = β (m₊ − E) ≥ 0`:

    ⟨a⟩ ≤ log ⟨e^a⟩ ≤ ⟨a⟩ + (e^A / 2) ⟨a²⟩            (a ≤ A)
    ⟨b⟩ − ⟨b²⟩ / 2 ≤ − log ⟨e^{−b}⟩ ≤ ⟨b⟩

and `Z(m₋) / Z(E) = ⟨e^a⟩`, `Z(m₊) / Z(E) = ⟨e^{−b}⟩`, so that these are bounds on
`log Z(m₋) − log Z(E)` and `log Z(E) − log Z(m₊)`.  Mathlib only; no project import.
Compile:  lake env lean experiments/science/pi_inference/lean/SandwichCost.lean
-/
import Mathlib

namespace ScienceA17

open Finset

/-- `e^{-b} ≤ 1 - b + b²/2` for `b ≥ 0` (from `1 + b + b²/2 ≤ e^b`). -/
theorem exp_neg_le_quadratic {b : ℝ} (hb : 0 ≤ b) : Real.exp (-b) ≤ 1 - b + b ^ 2 / 2 := by
  have h := Real.quadratic_le_exp_of_nonneg hb
  have hx : 0 < Real.exp (-b) := Real.exp_pos _
  have hxy : Real.exp (-b) * Real.exp b = 1 := by rw [← Real.exp_add]; simp
  have hq : 0 < 1 + b + b ^ 2 / 2 := by positivity
  have h1 : Real.exp (-b) * (1 + b + b ^ 2 / 2) ≤ 1 := by
    calc Real.exp (-b) * (1 + b + b ^ 2 / 2) ≤ Real.exp (-b) * Real.exp b :=
          mul_le_mul_of_nonneg_left h hx.le
      _ = 1 := hxy
  have h2 : (1 - b + b ^ 2 / 2) * (1 + b + b ^ 2 / 2) = 1 + b ^ 4 / 4 := by ring
  by_contra hcon
  have hlt := not_le.mp hcon
  have h3 : (1 - b + b ^ 2 / 2) * (1 + b + b ^ 2 / 2) < Real.exp (-b) * (1 + b + b ^ 2 / 2) :=
    mul_lt_mul_of_pos_right hlt hq
  nlinarith [sq_nonneg (b ^ 2)]

/-- `e^a ≤ 1 + a + (a²/2) e^a` for `a ≥ 0` (Taylor with the remainder bounded at the right end). -/
theorem exp_le_quadratic_mul_exp {a : ℝ} (ha : 0 ≤ a) :
    Real.exp a ≤ 1 + a + a ^ 2 / 2 * Real.exp a := by
  -- g s = e^a s²/2 − (e^s − 1 − s) is nondecreasing on [0, a]
  let g : ℝ → ℝ := fun s => Real.exp a * s ^ 2 / 2 - (Real.exp s - 1 - s)
  have hd : ∀ s : ℝ, HasDerivAt g (Real.exp a * s - (Real.exp s - 1)) s := by
    intro s
    have h1 : HasDerivAt (fun s : ℝ => Real.exp a * s ^ 2 / 2) (Real.exp a * s) s := by
      have h := ((hasDerivAt_pow 2 s).const_mul (Real.exp a)).div_const 2
      refine h.congr_deriv ?_
      have e : (2 - 1 : ℕ) = 1 := rfl
      rw [e, pow_one]
      push_cast
      ring
    have h2 : HasDerivAt (fun s : ℝ => Real.exp s - 1 - s) (Real.exp s - 1) s :=
      ((Real.hasDerivAt_exp s).sub_const 1).sub (hasDerivAt_id' s)
    exact h1.sub h2
  have hmono : MonotoneOn g (Set.Icc 0 a) := by
    apply monotoneOn_of_deriv_nonneg (convex_Icc 0 a)
    · exact (continuous_iff_continuousAt.mpr fun s => (hd s).continuousAt).continuousOn
    · exact fun s _ => (hd s).differentiableAt.differentiableWithinAt
    · intro s hs
      rw [interior_Icc] at hs
      rw [(hd s).deriv]
      have hs0 : 0 ≤ s := hs.1.le
      have hsa : Real.exp s ≤ Real.exp a := Real.exp_le_exp.mpr hs.2.le
      -- e^s − 1 ≤ s e^s ≤ s e^a
      have h1 : Real.exp s - 1 ≤ s * Real.exp s := by
        have h := Real.one_sub_le_exp_neg s
        have hp : 0 < Real.exp s := Real.exp_pos s
        have hxy : Real.exp (-s) * Real.exp s = 1 := by rw [← Real.exp_add]; simp
        nlinarith
      nlinarith [mul_le_mul_of_nonneg_left hsa hs0]
  have h0 : g 0 ≤ g a := hmono (Set.left_mem_Icc.mpr ha) (Set.right_mem_Icc.mpr ha) ha
  simp only [g] at h0
  have : Real.exp 0 = 1 := Real.exp_zero
  nlinarith [h0, this]

variable {ι : Type*} [Fintype ι]

/-- Jensen for the exponential, by `1 + t ≤ e^t`. -/
theorem exp_mean_le_mean_exp {w : ι → ℝ} (hw : ∀ i, 0 ≤ w i) (hsum : ∑ i, w i = 1) (a : ι → ℝ) :
    Real.exp (∑ i, w i * a i) ≤ ∑ i, w i * Real.exp (a i) := by
  have key : ∀ μ : ℝ, μ = ∑ i, w i * a i → Real.exp μ ≤ ∑ i, w i * Real.exp (a i) := by
    intro μ hμ
    have h : ∀ i, w i * (Real.exp μ * (a i - μ + 1)) ≤ w i * Real.exp (a i) := by
      intro i
      have h1 : Real.exp μ * (a i - μ + 1) ≤ Real.exp (a i) := by
        have h2 := Real.add_one_le_exp (a i - μ)
        calc Real.exp μ * (a i - μ + 1) ≤ Real.exp μ * Real.exp (a i - μ) :=
              mul_le_mul_of_nonneg_left h2 (Real.exp_pos μ).le
          _ = Real.exp (a i) := by rw [← Real.exp_add]; congr 1; ring
      exact mul_le_mul_of_nonneg_left h1 (hw i)
    have e1 : ∀ i, w i * (Real.exp μ * (a i - μ + 1))
        = Real.exp μ * (w i * a i) - Real.exp μ * μ * w i + Real.exp μ * w i := by
      intro i; ring
    have e2 : ∑ i, w i * (Real.exp μ * (a i - μ + 1)) = Real.exp μ := by
      simp_rw [e1]
      rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.mul_sum,
        ← Finset.mul_sum, hsum, ← hμ]
      ring
    calc Real.exp μ = ∑ i, w i * (Real.exp μ * (a i - μ + 1)) := e2.symm
      _ ≤ ∑ i, w i * Real.exp (a i) := Finset.sum_le_sum fun i _ => h i
  exact key _ rfl

/-- The floor's side: `⟨a⟩ ≤ log⟨e^a⟩ ≤ ⟨a⟩ + (e^A/2)⟨a²⟩` for `0 ≤ a ≤ A`. -/
theorem floor_side {w : ι → ℝ} (hw : ∀ i, 0 ≤ w i) (hsum : ∑ i, w i = 1) {a : ι → ℝ} {A : ℝ}
    (ha0 : ∀ i, 0 ≤ a i) (haA : ∀ i, a i ≤ A) :
    ∑ i, w i * a i ≤ Real.log (∑ i, w i * Real.exp (a i)) ∧
    Real.log (∑ i, w i * Real.exp (a i)) ≤
      ∑ i, w i * a i + Real.exp A / 2 * ∑ i, w i * a i ^ 2 := by
  have hJ := exp_mean_le_mean_exp hw hsum a
  have hpos : 0 < ∑ i, w i * Real.exp (a i) := lt_of_lt_of_le (Real.exp_pos _) hJ
  refine ⟨(Real.le_log_iff_exp_le hpos).mpr hJ, ?_⟩
  have hlog := Real.log_le_sub_one_of_pos hpos
  have hpt : ∀ i, w i * Real.exp (a i) ≤ w i + w i * a i + Real.exp A / 2 * (w i * a i ^ 2) := by
    intro i
    have h1 := exp_le_quadratic_mul_exp (ha0 i)
    have h2 : Real.exp (a i) ≤ Real.exp A := Real.exp_le_exp.mpr (haA i)
    have h3 : a i ^ 2 / 2 * Real.exp (a i) ≤ a i ^ 2 / 2 * Real.exp A :=
      mul_le_mul_of_nonneg_left h2 (by positivity)
    have h4 : Real.exp (a i) ≤ 1 + a i + a i ^ 2 / 2 * Real.exp A := by linarith
    calc w i * Real.exp (a i) ≤ w i * (1 + a i + a i ^ 2 / 2 * Real.exp A) :=
          mul_le_mul_of_nonneg_left h4 (hw i)
      _ = w i + w i * a i + Real.exp A / 2 * (w i * a i ^ 2) := by ring
  have hs : ∑ i, w i * Real.exp (a i)
      ≤ 1 + ∑ i, w i * a i + Real.exp A / 2 * ∑ i, w i * a i ^ 2 := by
    calc ∑ i, w i * Real.exp (a i)
        ≤ ∑ i, (w i + w i * a i + Real.exp A / 2 * (w i * a i ^ 2)) :=
          Finset.sum_le_sum fun i _ => hpt i
      _ = 1 + ∑ i, w i * a i + Real.exp A / 2 * ∑ i, w i * a i ^ 2 := by
          rw [Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.mul_sum, hsum]
  linarith

/-- The ceiling's side: `⟨b⟩ − ⟨b²⟩/2 ≤ −log⟨e^{−b}⟩ ≤ ⟨b⟩` for `b ≥ 0` — no exponential. -/
theorem ceiling_side {w : ι → ℝ} (hw : ∀ i, 0 ≤ w i) (hsum : ∑ i, w i = 1) {b : ι → ℝ}
    (hb0 : ∀ i, 0 ≤ b i) :
    ∑ i, w i * b i - (∑ i, w i * b i ^ 2) / 2 ≤ -Real.log (∑ i, w i * Real.exp (-b i)) ∧
    -Real.log (∑ i, w i * Real.exp (-b i)) ≤ ∑ i, w i * b i := by
  have hJ := exp_mean_le_mean_exp hw hsum (fun i => -b i)
  have hpos : 0 < ∑ i, w i * Real.exp (-b i) := lt_of_lt_of_le (Real.exp_pos _) hJ
  have hneg : ∑ i, w i * -b i = -∑ i, w i * b i := by
    rw [← Finset.sum_neg_distrib]; exact Finset.sum_congr rfl fun i _ => by ring
  constructor
  · have hlog := Real.log_le_sub_one_of_pos hpos
    have hpt : ∀ i, w i * Real.exp (-b i) ≤ w i - w i * b i + (w i * b i ^ 2) / 2 := by
      intro i
      calc w i * Real.exp (-b i) ≤ w i * (1 - b i + b i ^ 2 / 2) :=
            mul_le_mul_of_nonneg_left (exp_neg_le_quadratic (hb0 i)) (hw i)
        _ = w i - w i * b i + (w i * b i ^ 2) / 2 := by ring
    have hs : ∑ i, w i * Real.exp (-b i) ≤ 1 - ∑ i, w i * b i + (∑ i, w i * b i ^ 2) / 2 := by
      calc ∑ i, w i * Real.exp (-b i)
          ≤ ∑ i, (w i - w i * b i + (w i * b i ^ 2) / 2) := Finset.sum_le_sum fun i _ => hpt i
        _ = 1 - ∑ i, w i * b i + (∑ i, w i * b i ^ 2) / 2 := by
            rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.sum_div, hsum]
    linarith
  · have h := (Real.le_log_iff_exp_le hpos).mpr hJ
    rw [hneg] at h
    linarith

/-- Partition functions.  `Z β f = Σ_x e^{−β f(x)}`. -/
noncomputable def Z (β : ℝ) (f : ι → ℝ) : ℝ := ∑ x, Real.exp (-β * f x)

/-- The Gibbs weights of `E`. -/
noncomputable def gibbs (β : ℝ) (E : ι → ℝ) (x : ι) : ℝ := Real.exp (-β * E x) / Z β E

theorem Z_pos [Nonempty ι] (β : ℝ) (f : ι → ℝ) : 0 < Z β f :=
  Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty

theorem gibbs_nonneg [Nonempty ι] (β : ℝ) (E : ι → ℝ) (x : ι) : 0 ≤ gibbs β E x :=
  div_nonneg (Real.exp_pos _).le (Z_pos β E).le

theorem gibbs_sum [Nonempty ι] (β : ℝ) (E : ι → ℝ) : ∑ x, gibbs β E x = 1 := by
  unfold gibbs
  rw [← Finset.sum_div]
  exact div_self (Z_pos β E).ne'

/-- `Z(m)/Z(E) = ⟨e^{β(E − m)}⟩` under the Gibbs measure of `E`. -/
theorem Z_ratio [Nonempty ι] (β : ℝ) (E m : ι → ℝ) :
    Z β m / Z β E = ∑ x, gibbs β E x * Real.exp (β * (E x - m x)) := by
  unfold gibbs
  have h : ∀ x, Real.exp (-β * E x) / Z β E * Real.exp (β * (E x - m x))
      = Real.exp (-β * m x) / Z β E := by
    intro x
    rw [div_mul_eq_mul_div, ← Real.exp_add]
    congr 2; ring
  simp_rw [h]
  rw [← Finset.sum_div]
  rfl

/-- **Lemma A17.16.**  For `m₋ ≤ E ≤ m₊`, `β ≥ 0`, means under the Gibbs measure of `E`,
`a = β (E − m₋) ≤ A`, `b = β (m₊ − E)`:
`⟨a⟩ ≤ log Z(m₋) − log Z(E) ≤ ⟨a⟩ + (e^A/2)⟨a²⟩` and `⟨b⟩ − ⟨b²⟩/2 ≤ log Z(E) − log Z(m₊) ≤ ⟨b⟩`. -/
theorem sandwich_cost [Nonempty ι] {β A : ℝ} (hβ : 0 ≤ β) {E lo up : ι → ℝ}
    (hlo : ∀ x, lo x ≤ E x) (hup : ∀ x, E x ≤ up x) (hA : ∀ x, β * (E x - lo x) ≤ A) :
    (∑ x, gibbs β E x * (β * (E x - lo x)) ≤ Real.log (Z β lo) - Real.log (Z β E) ∧
     Real.log (Z β lo) - Real.log (Z β E) ≤
       ∑ x, gibbs β E x * (β * (E x - lo x)) +
         Real.exp A / 2 * ∑ x, gibbs β E x * (β * (E x - lo x)) ^ 2) ∧
    (∑ x, gibbs β E x * (β * (up x - E x)) - (∑ x, gibbs β E x * (β * (up x - E x)) ^ 2) / 2
       ≤ Real.log (Z β E) - Real.log (Z β up) ∧
     Real.log (Z β E) - Real.log (Z β up) ≤ ∑ x, gibbs β E x * (β * (up x - E x))) := by
  have hw := gibbs_nonneg β E
  have hsum := gibbs_sum β E
  have hZE := Z_pos β E
  have hZlo := Z_pos β lo
  have hZup := Z_pos β up
  have ha0 : ∀ x, 0 ≤ β * (E x - lo x) := fun x => mul_nonneg hβ (sub_nonneg.mpr (hlo x))
  have hb0 : ∀ x, 0 ≤ β * (up x - E x) := fun x => mul_nonneg hβ (sub_nonneg.mpr (hup x))
  have hF := floor_side hw hsum ha0 hA
  have hC := ceiling_side hw hsum hb0
  have e1 : Real.log (Z β lo) - Real.log (Z β E)
      = Real.log (∑ x, gibbs β E x * Real.exp (β * (E x - lo x))) := by
    rw [← Z_ratio, Real.log_div hZlo.ne' hZE.ne']
  have e2 : Real.log (Z β E) - Real.log (Z β up)
      = -Real.log (∑ x, gibbs β E x * Real.exp (-(β * (up x - E x)))) := by
    have h : ∀ x, -(β * (up x - E x)) = β * (E x - up x) := fun x => by ring
    simp_rw [h]
    rw [← Z_ratio, Real.log_div hZup.ne' hZE.ne']
    ring
  rw [e1, e2]
  exact ⟨hF, hC⟩

end ScienceA17

#print axioms ScienceA17.exp_neg_le_quadratic
#print axioms ScienceA17.exp_le_quadratic_mul_exp
#print axioms ScienceA17.exp_mean_le_mean_exp
#print axioms ScienceA17.floor_side
#print axioms ScienceA17.ceiling_side
#print axioms ScienceA17.Z_ratio
#print axioms ScienceA17.sandwich_cost
