/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# Scattering curves of one conformation are members of the pair-profile class (theory report §11.17, Theorem 11.48(d))

The orientationally averaged (Debye) intensity of `N` equal point scatterers at wave number `q` is
`I(q) = N + 2 ∑_{pairs} sinc(q · r)`, `r = √s` the pair distance.  The statement that makes it a member of the class of
pair-additive functionals with a radial function that is Lipschitz in the *squared* distance (Theorem 11.48) is

* `sinc_sqrt_lipschitz` — `|sinc(q√s) − sinc(q√s')| ≤ (q²/6)·|s − s'|` for `s, s' ≥ 0`.

It follows from `abs_sinc_sub_le` (`|sinc b − sinc a| ≤ (b² − a²)/6` for `0 ≤ a ≤ b`), i.e. `sinc t + t²/6` is nondecreasing
and `sinc t − t²/6` nonincreasing on `t ≥ 0`, which is `|sin t − t cos t| ≤ t³/3` (`sub_cube_le`, `le_add_cube`).

* `debye_sum_sub_le`, `debye_sub_le` — for two conformations with the same number of pairs and *any* matching `σ` of their
  pairs, `|I_x(q) − I_y(q)| ≤ (q²/3) ∑_k |s^x_k − s^y_{σ k}|`; with the sorted matching the right side is `q²/3` times the
  transport distance between the two multisets of squared distances.

The statement was proposed, with this proof, by the Scientific Discovery Division (its Proposition A2.1, message
SCI-REV-0006); the formalisation is ours.
-/
import Mathlib

namespace MetricChain.Scattering

open Real Finset

/-- `t cos t − sin t + t³/3 ≥ 0` for `t ≥ 0`: the function vanishes at `0` and its derivative is `t (t − sin t) ≥ 0`. -/
theorem le_add_cube {t : ℝ} (ht : 0 ≤ t) : 0 ≤ t * cos t - sin t + t ^ 3 / 3 := by
  have hmono : MonotoneOn (fun x : ℝ => x * cos x - sin x + x ^ 3 / 3) (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0)
    · fun_prop
    · fun_prop
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      have hd : HasDerivAt (fun x : ℝ => x * cos x - sin x + x ^ 3 / 3)
          (1 * cos x + x * (-sin x) - cos x + 3 * x ^ 2 / 3) x := by
        have h1 : HasDerivAt (fun x : ℝ => x * cos x) (1 * cos x + x * (-sin x)) x :=
          (hasDerivAt_id x).mul (hasDerivAt_cos x)
        have h2 : HasDerivAt (fun x : ℝ => x ^ 3 / 3) (3 * x ^ 2 / 3) x := by
          simpa using (hasDerivAt_pow 3 x).div_const 3
        exact (h1.sub (hasDerivAt_sin x)).add h2
      rw [hd.deriv]
      have hs : sin x ≤ x := sin_le hx0.le
      nlinarith [mul_nonneg hx0.le (sub_nonneg.mpr hs)]
  have h0 := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr ht) ht
  simpa using h0

/-- `sin t − t cos t + t³/3 ≥ 0` for `t ≥ 0`: the function vanishes at `0` and its derivative is `t (t + sin t) ≥ 0`. -/
theorem sub_cube_le {t : ℝ} (ht : 0 ≤ t) : 0 ≤ sin t - t * cos t + t ^ 3 / 3 := by
  have hmono : MonotoneOn (fun x : ℝ => sin x - x * cos x + x ^ 3 / 3) (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0)
    · fun_prop
    · fun_prop
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      have hd : HasDerivAt (fun x : ℝ => sin x - x * cos x + x ^ 3 / 3)
          (cos x - (1 * cos x + x * (-sin x)) + 3 * x ^ 2 / 3) x := by
        have h1 : HasDerivAt (fun x : ℝ => x * cos x) (1 * cos x + x * (-sin x)) x :=
          (hasDerivAt_id x).mul (hasDerivAt_cos x)
        have h2 : HasDerivAt (fun x : ℝ => x ^ 3 / 3) (3 * x ^ 2 / 3) x := by
          simpa using (hasDerivAt_pow 3 x).div_const 3
        exact ((hasDerivAt_sin x).sub h1).add h2
      rw [hd.deriv]
      have hs : -x ≤ sin x := by
        have := abs_le.mp (abs_sin_le_abs (x := x))
        rw [abs_of_pos hx0] at this
        exact this.1
      nlinarith [mul_nonneg hx0.le (by linarith : (0 : ℝ) ≤ x + sin x)]
  have h0 := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr ht) ht
  simpa using h0

/-- The derivative of `sinc` away from the origin. -/
theorem hasDerivAt_sinc {t : ℝ} (ht : t ≠ 0) :
    HasDerivAt sinc ((cos t * t - sin t) / t ^ 2) t := by
  have h : HasDerivAt (fun x : ℝ => sin x / x) ((cos t * t - sin t * 1) / t ^ 2) t :=
    (hasDerivAt_sin t).div (hasDerivAt_id t) ht
  have h2 : sinc =ᶠ[nhds t] fun x : ℝ => sin x / x := by
    filter_upwards [isOpen_ne.mem_nhds ht] with x hx
    exact sinc_of_ne_zero hx
  simpa using h.congr_of_eventuallyEq h2

/-- `sinc t + t²/6` is nondecreasing on `t ≥ 0`. -/
theorem sinc_add_sq_monotoneOn : MonotoneOn (fun t : ℝ => sinc t + t ^ 2 / 6) (Set.Ici 0) := by
  apply monotoneOn_of_deriv_nonneg (convex_Ici 0)
  · fun_prop
  · intro x hx
    rw [interior_Ici] at hx
    have hx0 : (0 : ℝ) < x := hx
    exact (((hasDerivAt_sinc hx0.ne').add
      ((hasDerivAt_pow 2 x).div_const 6)).differentiableAt).differentiableWithinAt
  · intro x hx
    rw [interior_Ici] at hx
    have hx0 : (0 : ℝ) < x := hx
    have hd : HasDerivAt (fun t : ℝ => sinc t + t ^ 2 / 6)
        ((cos x * x - sin x) / x ^ 2 + (2 : ℕ) * x ^ (2 - 1) / 6) x :=
      (hasDerivAt_sinc hx0.ne').add ((hasDerivAt_pow 2 x).div_const 6)
    rw [hd.deriv]
    have hk := le_add_cube hx0.le
    have hx2 : (0 : ℝ) < x ^ 2 := by positivity
    have : (cos x * x - sin x) / x ^ 2 + (2 : ℕ) * x ^ (2 - 1) / 6
        = (x * cos x - sin x + x ^ 3 / 3) / x ^ 2 := by
      field_simp
      ring
    rw [this]
    exact div_nonneg hk hx2.le

/-- `sinc t − t²/6` is nonincreasing on `t ≥ 0`. -/
theorem sinc_sub_sq_antitoneOn : AntitoneOn (fun t : ℝ => sinc t - t ^ 2 / 6) (Set.Ici 0) := by
  apply antitoneOn_of_deriv_nonpos (convex_Ici 0)
  · fun_prop
  · intro x hx
    rw [interior_Ici] at hx
    have hx0 : (0 : ℝ) < x := hx
    exact (((hasDerivAt_sinc hx0.ne').sub
      ((hasDerivAt_pow 2 x).div_const 6)).differentiableAt).differentiableWithinAt
  · intro x hx
    rw [interior_Ici] at hx
    have hx0 : (0 : ℝ) < x := hx
    have hd : HasDerivAt (fun t : ℝ => sinc t - t ^ 2 / 6)
        ((cos x * x - sin x) / x ^ 2 - (2 : ℕ) * x ^ (2 - 1) / 6) x :=
      (hasDerivAt_sinc hx0.ne').sub ((hasDerivAt_pow 2 x).div_const 6)
    rw [hd.deriv]
    have hk := sub_cube_le hx0.le
    have hx2 : (0 : ℝ) < x ^ 2 := by positivity
    have : (cos x * x - sin x) / x ^ 2 - (2 : ℕ) * x ^ (2 - 1) / 6
        = -((sin x - x * cos x + x ^ 3 / 3) / x ^ 2) := by
      field_simp
      ring
    rw [this]
    exact neg_nonpos.mpr (div_nonneg hk hx2.le)

/-- **Two-point form.**  For `0 ≤ a ≤ b`: `|sinc b − sinc a| ≤ (b² − a²)/6`. -/
theorem abs_sinc_sub_le {a b : ℝ} (ha : 0 ≤ a) (hab : a ≤ b) :
    |sinc b - sinc a| ≤ (b ^ 2 - a ^ 2) / 6 := by
  have hb : 0 ≤ b := ha.trans hab
  have h1 := sinc_add_sq_monotoneOn (Set.mem_Ici.mpr ha) (Set.mem_Ici.mpr hb) hab
  have h2 := sinc_sub_sq_antitoneOn (Set.mem_Ici.mpr ha) (Set.mem_Ici.mpr hb) hab
  simp only at h1 h2
  rw [abs_le]
  constructor <;> linarith

/-- **The radial function of the Debye formula is Lipschitz in the squared distance, with constant `q²/6`.** -/
theorem sinc_sqrt_lipschitz (q : ℝ) {s s' : ℝ} (hs : 0 ≤ s) (hs' : 0 ≤ s') :
    |sinc (q * √s) - sinc (q * √s')| ≤ q ^ 2 / 6 * |s - s'| := by
  -- reduce to `q ≥ 0` (sinc is even) and to `s ≤ s'`
  have key : ∀ {u v : ℝ}, 0 ≤ u → u ≤ v →
      |sinc (|q| * √v) - sinc (|q| * √u)| ≤ q ^ 2 / 6 * (v - u) := by
    intro u v hu huv
    have hv : 0 ≤ v := hu.trans huv
    have ha : 0 ≤ |q| * √u := mul_nonneg (abs_nonneg q) (sqrt_nonneg u)
    have hab : |q| * √u ≤ |q| * √v :=
      mul_le_mul_of_nonneg_left (sqrt_le_sqrt huv) (abs_nonneg q)
    have h := abs_sinc_sub_le ha hab
    have e1 : (|q| * √v) ^ 2 = q ^ 2 * v := by rw [mul_pow, sq_abs, sq_sqrt hv]
    have e2 : (|q| * √u) ^ 2 = q ^ 2 * u := by rw [mul_pow, sq_abs, sq_sqrt hu]
    rw [e1, e2] at h
    calc |sinc (|q| * √v) - sinc (|q| * √u)| ≤ (q ^ 2 * v - q ^ 2 * u) / 6 := h
      _ = q ^ 2 / 6 * (v - u) := by ring
  have even : ∀ x : ℝ, sinc (q * x) = sinc (|q| * x) := by
    intro x
    rcases le_total 0 q with hq | hq
    · rw [abs_of_nonneg hq]
    · rw [abs_of_nonpos hq, neg_mul, sinc_neg]
  rw [even, even]
  rcases le_total s s' with h | h
  · have := key hs h
    rw [abs_sub_comm, abs_sub_comm s s', abs_of_nonneg (sub_nonneg.mpr h)]
    exact this
  · have := key hs' h
    rw [abs_of_nonneg (sub_nonneg.mpr h)]
    exact this

/-- For any matching `σ` of the pairs of two conformations, the pair sums of the Debye formula differ by at most
`q²/6` times the matched `ℓ¹` distance of the squared distances. -/
theorem debye_sum_sub_le {ι : Type*} [Fintype ι] (q : ℝ) (s s' : ι → ℝ)
    (hs : ∀ k, 0 ≤ s k) (hs' : ∀ k, 0 ≤ s' k) (σ : Equiv.Perm ι) :
    |∑ k, sinc (q * √(s k)) - ∑ k, sinc (q * √(s' k))|
      ≤ q ^ 2 / 6 * ∑ k, |s k - s' (σ k)| := by
  have hre : ∑ k, sinc (q * √(s' k)) = ∑ k, sinc (q * √(s' (σ k))) :=
    (Equiv.sum_comp σ (fun k => sinc (q * √(s' k)))).symm
  rw [hre, ← Finset.sum_sub_distrib, Finset.mul_sum]
  calc |∑ k, (sinc (q * √(s k)) - sinc (q * √(s' (σ k))))|
      ≤ ∑ k, |sinc (q * √(s k)) - sinc (q * √(s' (σ k)))| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ k, q ^ 2 / 6 * |s k - s' (σ k)| :=
        Finset.sum_le_sum fun k _ => sinc_sqrt_lipschitz q (hs k) (hs' (σ k))

/-- The Debye intensity of `N` equal point scatterers with squared pair distances `s`. -/
noncomputable def debye {ι : Type*} [Fintype ι] (N : ℕ) (q : ℝ) (s : ι → ℝ) : ℝ :=
  N + 2 * ∑ k, sinc (q * √(s k))

/-- **Scattering curves are members of the profile class (Theorem 11.48(d)).**  Two conformations with the same number of
beads: for every wave number and every matching of their pairs the intensities differ by at most `q²/3` times the
matched `ℓ¹` distance of the squared distances. -/
theorem debye_sub_le {ι : Type*} [Fintype ι] (N : ℕ) (q : ℝ) (s s' : ι → ℝ)
    (hs : ∀ k, 0 ≤ s k) (hs' : ∀ k, 0 ≤ s' k) (σ : Equiv.Perm ι) :
    |debye N q s - debye N q s'| ≤ q ^ 2 / 3 * ∑ k, |s k - s' (σ k)| := by
  have h := debye_sum_sub_le q s s' hs hs' σ
  have e : debye N q s - debye N q s'
      = 2 * (∑ k, sinc (q * √(s k)) - ∑ k, sinc (q * √(s' k))) := by
    unfold debye; ring
  rw [e, abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 2)]
  calc 2 * |∑ k, sinc (q * √(s k)) - ∑ k, sinc (q * √(s' k))|
      ≤ 2 * (q ^ 2 / 6 * ∑ k, |s k - s' (σ k)|) := by linarith
    _ = q ^ 2 / 3 * ∑ k, |s k - s' (σ k)| := by ring

/-- Conformations with the same multiset of squared distances (some matching with equal values) have the same
scattering curve. -/
theorem debye_eq_of_matching {ι : Type*} [Fintype ι] (N : ℕ) (q : ℝ) (s s' : ι → ℝ)
    (hs : ∀ k, 0 ≤ s k) (hs' : ∀ k, 0 ≤ s' k) (σ : Equiv.Perm ι) (h : ∀ k, s k = s' (σ k)) :
    debye N q s = debye N q s' := by
  have hb := debye_sub_le N q s s' hs hs' σ
  have hz : ∑ k, |s k - s' (σ k)| = 0 := Finset.sum_eq_zero fun k _ => by rw [h k, sub_self, abs_zero]
  rw [hz, mul_zero] at hb
  exact sub_eq_zero.mp (abs_nonpos_iff.mp hb)

/-- Non-vacuity and sharpness at the origin: the bound is an equality in the limit of small arguments, in the sense that
`1 − sinc t ≤ t²/6` (the case `a = 0` of `abs_sinc_sub_le`) cannot hold with a constant below `1/6` — here only the
inequality itself is recorded, together with a concrete instance. -/
theorem one_sub_sinc_le (t : ℝ) (ht : 0 ≤ t) : 1 - sinc t ≤ t ^ 2 / 6 := by
  have h := abs_sinc_sub_le (le_refl (0 : ℝ)) ht
  rw [sinc_zero] at h
  have := (abs_le.mp h).1
  linarith

end MetricChain.Scattering

-- R9: appended to the scratch copy only (the file above is byte-identical to the export's Scattering.lean)
open MetricChain.Scattering in
#check @sinc_sqrt_lipschitz
open MetricChain.Scattering in
#check @debye_sub_le
open MetricChain.Scattering in
#check @debye_eq_of_matching
open MetricChain.Scattering in
#print debye
#print axioms MetricChain.Scattering.le_add_cube
#print axioms MetricChain.Scattering.sub_cube_le
#print axioms MetricChain.Scattering.abs_sinc_sub_le
#print axioms MetricChain.Scattering.sinc_sqrt_lipschitz
#print axioms MetricChain.Scattering.debye_sum_sub_le
#print axioms MetricChain.Scattering.debye_sub_le
#print axioms MetricChain.Scattering.debye_eq_of_matching
#print axioms MetricChain.Scattering.one_sub_sinc_le
