/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# Residuals in a Hilbert ball: the hypercircle band as a certificate (theory report §11.17, Proposition 11.50a)

A first-order class is a polytope, and what several evaluations say about an unevaluated configuration combines by a
*minimum* (certificates are coverings).  In the ball of a reproducing-kernel Hilbert space evaluations combine
*linearly*.  For a finite index type and a positive semidefinite kernel `K`, functions are `g = K α` with squared norm
`αᵀ K α ≤ B²`.  If `s = K γ` interpolates `g` on the evaluated set `A` (with `γ` supported on `A`), then at every `x` and for
every weight vector `lam` supported on `A`

    (g x − s x)²  ≤  (‖g‖² − ‖s‖²) · ‖K_x − Σ_a lam_a K_a‖²                      (`hypercircle_band`).

The right-hand side is a product of two numbers that a checker computes from the data by additions and
multiplications: `‖s‖² = γᵀ K γ` and the squared power function of the rule `lam`.  No square root is needed.

* `cauchy_schwarz` — the Cauchy–Schwarz inequality for a kernel (from the discriminant of a quadratic);
* `hypercircle_band` — the band, with the reduced radius `B² − ‖s‖²`;
* `ball_certificate_sound` — if `L ≤ F + s − r` everywhere and `r x² ≥ (B² − ‖s‖²)·`(squared power function at `x`), then
  `L ≤ F + g` for every member `g` of the ball with the evaluated values;
* `verify_sound_ball` — the same with the pairwise kernel: a certificate accepted for an instance that lies termwise
  below a pairwise model of `F + s` bounds `F + g` from below by `L − r̄`;
* `isKernel_of_features` — Gram matrices of feature maps are kernels;
* `band_witness` — the band is an equality for the identity kernel on two points.

The statement and its place next to the three kernels were proposed by the Scientific Discovery Division (its message
SCI-MSG-0007, workstream X, Theorem 1 and request X-T1).  The inequality is the classical hypercircle inequality of
optimal recovery (Golomb–Weinberger); nothing here is new mathematics.
-/
import Mathlib
import proofs.Frontiers.SecondOrderEnvelope

namespace MetricChain.Hypercircle

open Matrix Finset

variable {ι : Type*} [Fintype ι]

/-- The bilinear form of a kernel matrix. -/
def form (K : Matrix ι ι ℝ) (a b : ι → ℝ) : ℝ := a ⬝ᵥ K *ᵥ b

/-- A (positive semidefinite, symmetric) kernel. -/
structure IsKernel (K : Matrix ι ι ℝ) : Prop where
  symm : ∀ a b, form K a b = form K b a
  nonneg : ∀ a, 0 ≤ form K a a

theorem form_add_left (K : Matrix ι ι ℝ) (a a' b : ι → ℝ) :
    form K (a + a') b = form K a b + form K a' b := by
  unfold form
  rw [add_dotProduct]

theorem form_add_right (K : Matrix ι ι ℝ) (a b b' : ι → ℝ) :
    form K a (b + b') = form K a b + form K a b' := by
  unfold form
  rw [mulVec_add, dotProduct_add]

theorem form_sub_left (K : Matrix ι ι ℝ) (a a' b : ι → ℝ) :
    form K (a - a') b = form K a b - form K a' b := by
  unfold form
  rw [sub_dotProduct]

theorem form_sub_right (K : Matrix ι ι ℝ) (a b b' : ι → ℝ) :
    form K a (b - b') = form K a b - form K a b' := by
  unfold form
  rw [mulVec_sub, dotProduct_sub]

theorem form_smul_left (K : Matrix ι ι ℝ) (t : ℝ) (a b : ι → ℝ) :
    form K (t • a) b = t * form K a b := by
  unfold form
  rw [smul_dotProduct, smul_eq_mul]

theorem form_smul_right (K : Matrix ι ι ℝ) (t : ℝ) (a b : ι → ℝ) :
    form K a (t • b) = t * form K a b := by
  unfold form
  rw [mulVec_smul, dotProduct_smul, smul_eq_mul]

/-- **Cauchy–Schwarz inequality for a kernel.** -/
theorem cauchy_schwarz {K : Matrix ι ι ℝ} (hK : IsKernel K) (a b : ι → ℝ) :
    form K a b ^ 2 ≤ form K a a * form K b b := by
  have h : ∀ t : ℝ, 0 ≤ form K b b * (t * t) + 2 * form K a b * t + form K a a := by
    intro t
    have h0 := hK.nonneg (a + t • b)
    rw [form_add_left, form_add_right, form_add_right, form_smul_left, form_smul_left,
      form_smul_right, form_smul_right, hK.symm b a] at h0
    nlinarith [h0]
  have hd := discrim_le_zero h
  unfold discrim at hd
  nlinarith [hd]

/-- The function with coefficients `α`: `g = K α`. -/
def fn (K : Matrix ι ι ℝ) (α : ι → ℝ) : ι → ℝ := K *ᵥ α

theorem fn_eq_form [DecidableEq ι] (K : Matrix ι ι ℝ) (α : ι → ℝ) (x : ι) :
    fn K α x = form K (Pi.single x 1) α := by
  unfold fn form
  simp

/-- If a vector is supported on `A` and the function of `δ` vanishes on `A`, their pairing vanishes. -/
theorem form_eq_zero_of_support {K : Matrix ι ι ℝ} {A : Finset ι} {lam δ : ι → ℝ}
    (hlam : ∀ y, y ∉ A → lam y = 0) (hδ : ∀ a ∈ A, fn K δ a = 0) : form K lam δ = 0 := by
  unfold form dotProduct
  refine Finset.sum_eq_zero fun y _ => ?_
  by_cases hy : y ∈ A
  · have := hδ y hy
    unfold fn at this
    rw [this, mul_zero]
  · rw [hlam y hy, zero_mul]

/-- **The hypercircle band, with the reduced radius.** -/
theorem hypercircle_band [DecidableEq ι] {K : Matrix ι ι ℝ} (hK : IsKernel K) (A : Finset ι)
    (α γ lam : ι → ℝ) (hγ : ∀ y, y ∉ A → γ y = 0) (hint : ∀ a ∈ A, fn K γ a = fn K α a)
    (hlam : ∀ y, y ∉ A → lam y = 0) (x : ι) :
    (fn K α x - fn K γ x) ^ 2 ≤
      (form K α α - form K γ γ) * form K (Pi.single x 1 - lam) (Pi.single x 1 - lam) := by
  have hδ : ∀ a ∈ A, fn K (α - γ) a = 0 := by
    intro a ha
    have := hint a ha
    unfold fn at this ⊢
    rw [mulVec_sub, Pi.sub_apply, this, sub_self]
  have h1 : fn K α x - fn K γ x = form K (Pi.single x 1 - lam) (α - γ) := by
    rw [form_sub_left, form_eq_zero_of_support hlam hδ, sub_zero, form_sub_right,
      ← fn_eq_form, ← fn_eq_form]
  have h2 : form K (α - γ) (α - γ) = form K α α - form K γ γ := by
    have h3 : form K γ (α - γ) = 0 := form_eq_zero_of_support hγ hδ
    rw [form_sub_left, h3, sub_zero, form_sub_right]
    have h4 : form K α γ = form K γ γ := by
      have := form_sub_right K γ α γ
      rw [h3] at this
      rw [hK.symm α γ]
      linarith
    rw [h4]
  rw [h1, ← h2]
  have := cauchy_schwarz hK (Pi.single x 1 - lam) (α - γ)
  linarith [mul_comm (form K (Pi.single x 1 - lam) (Pi.single x 1 - lam)) (form K (α - γ) (α - γ))]

/-- **Soundness of a ball certificate.** -/
theorem ball_certificate_sound [DecidableEq ι] {K : Matrix ι ι ℝ} (hK : IsKernel K)
    (A : Finset ι) (α γ : ι → ℝ) (B2 : ℝ) (hB : form K α α ≤ B2)
    (hγ : ∀ y, y ∉ A → γ y = 0) (hint : ∀ a ∈ A, fn K γ a = fn K α a)
    (lam : ι → ι → ℝ) (hlam : ∀ x y, y ∉ A → lam x y = 0) (r : ι → ℝ) (hr : ∀ x, 0 ≤ r x)
    (hcert : ∀ x, (B2 - form K γ γ) *
      form K (Pi.single x 1 - lam x) (Pi.single x 1 - lam x) ≤ r x ^ 2)
    (F : ι → ℝ) (L : ℝ) (hL : ∀ x, L ≤ F x + fn K γ x - r x) (x : ι) :
    L ≤ F x + fn K α x := by
  have hb := hypercircle_band hK A α γ (lam x) hγ hint (hlam x) x
  have hp : 0 ≤ form K (Pi.single x 1 - lam x) (Pi.single x 1 - lam x) := hK.nonneg _
  have h1 : (fn K α x - fn K γ x) ^ 2 ≤ r x ^ 2 := by
    refine le_trans hb (le_trans ?_ (hcert x))
    exact mul_le_mul_of_nonneg_right (by linarith) hp
  have h3 := (abs_le_of_sq_le_sq' h1 (hr x)).1
  linarith [hL x]

/-- A Gram matrix of features is a kernel. -/
theorem isKernel_of_features {κ : Type*} [Fintype κ] (Φ : κ → ι → ℝ) :
    IsKernel (Matrix.of fun x y => ∑ j, Φ j x * Φ j y) := by
  have key : ∀ a b : ι → ℝ, form (Matrix.of fun x y => ∑ j, Φ j x * Φ j y) a b =
      ∑ j, (∑ x, a x * Φ j x) * (∑ y, Φ j y * b y) := by
    intro a b
    have hx : ∀ x, a x * ∑ y, (∑ j, Φ j x * Φ j y) * b y =
        ∑ j, ∑ y, a x * Φ j x * (Φ j y * b y) := by
      intro x
      rw [Finset.mul_sum, Finset.sum_comm]
      refine Finset.sum_congr rfl fun y _ => ?_
      rw [Finset.sum_mul, Finset.mul_sum]
      refine Finset.sum_congr rfl fun j _ => ?_
      ring
    have h1 : form (Matrix.of fun x y => ∑ j, Φ j x * Φ j y) a b =
        ∑ x, a x * ∑ y, (∑ j, Φ j x * Φ j y) * b y := by
      unfold form dotProduct mulVec dotProduct
      simp only [Matrix.of_apply]
    rw [h1, Finset.sum_congr rfl fun x _ => hx x, Finset.sum_comm]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Finset.sum_mul_sum]
  constructor
  · intro a b
    rw [key, key]
    refine Finset.sum_congr rfl fun j _ => ?_
    have e1 : ∑ x, a x * Φ j x = ∑ y, Φ j y * a y := Finset.sum_congr rfl fun _ _ => mul_comm _ _
    have e2 : ∑ y, Φ j y * b y = ∑ x, b x * Φ j x := Finset.sum_congr rfl fun _ _ => mul_comm _ _
    rw [e1, e2, mul_comm]
  · intro a
    rw [key]
    refine Finset.sum_nonneg fun j _ => ?_
    have e1 : ∑ y, Φ j y * a y = ∑ x, a x * Φ j x := Finset.sum_congr rfl fun _ _ => mul_comm _ _
    rw [e1]
    exact mul_self_nonneg _

/-- **Kernel soundness for a Hilbert ball.** -/
theorem verify_sound_ball {n k : ℕ} {K : Matrix (Config n k) (Config n k) ℝ} (hK : IsKernel K)
    (A : Finset (Config n k)) (α γ : Config n k → ℝ) (B2 : ℝ) (hB : form K α α ≤ B2)
    (hγ : ∀ y, y ∉ A → γ y = 0) (hint : ∀ a ∈ A, fn K γ a = fn K α a)
    (lam : Config n k → Config n k → ℝ) (hlam : ∀ x y, y ∉ A → lam x y = 0) (rbar : ℝ)
    (hr : 0 ≤ rbar)
    (hcert : ∀ x, (B2 - form K γ γ) *
      form K (Pi.single x 1 - lam x) (Pi.single x 1 - lam x) ≤ rbar ^ 2)
    (M : PairModel ℝ (Fin n) (fun _ => Fin k)) (F : Config n k → ℝ)
    (hM : ∀ x, M.energy x ≤ F x + fn K γ x) (I : PairInstance n k)
    (hh : ∀ i a, (I.h i a : ℝ) ≤ M.h i a) (hJ : ∀ i j a b, (I.J i j a b : ℝ) ≤ M.J i j a b)
    (cert : Cert n k) (D : Dom n k) (L : ℚ) (hv : verify cert I D L = true)
    (x : Config n k) (hx : InBox D x) : (L : ℝ) - rbar ≤ F x + fn K α x := by
  have h1 := verify_sound_real cert I D L hv M hh hJ x hx
  have hb := hypercircle_band hK A α γ (lam x) hγ hint (hlam x) x
  have hp : 0 ≤ form K (Pi.single x 1 - lam x) (Pi.single x 1 - lam x) := hK.nonneg _
  have h2 : (fn K α x - fn K γ x) ^ 2 ≤ rbar ^ 2 := by
    refine le_trans hb (le_trans ?_ (hcert x))
    exact mul_le_mul_of_nonneg_right (by linarith) hp
  have h3 := (abs_le_of_sq_le_sq' h2 hr).1
  linarith [hM x]

/-- **Non-vacuity and sharpness.**  For the identity kernel on two points (the function is its
coefficient vector), after evaluating the first point the band at the second point is
`g(1)² ≤ ‖g‖² − g(0)²`, an equality. -/
theorem band_witness :
    IsKernel (1 : Matrix (Fin 2) (Fin 2) ℝ) ∧
      (fn (1 : Matrix (Fin 2) (Fin 2) ℝ) ![3, 4] 1 - fn (1 : Matrix (Fin 2) (Fin 2) ℝ) ![3, 0] 1) ^ 2 =
        (form (1 : Matrix (Fin 2) (Fin 2) ℝ) ![3, 4] ![3, 4] -
            form (1 : Matrix (Fin 2) (Fin 2) ℝ) ![3, 0] ![3, 0]) *
          form (1 : Matrix (Fin 2) (Fin 2) ℝ) (Pi.single 1 1 - 0) (Pi.single 1 1 - 0) := by
  refine ⟨⟨fun a b => ?_, fun a => ?_⟩, ?_⟩
  · unfold form
    rw [one_mulVec, one_mulVec, dotProduct_comm]
  · unfold form
    rw [one_mulVec]
    exact Finset.sum_nonneg fun i _ => mul_self_nonneg _
  · unfold form fn
    simp [one_mulVec, dotProduct, Fin.sum_univ_two, Pi.single_apply]
    norm_num

end MetricChain.Hypercircle
