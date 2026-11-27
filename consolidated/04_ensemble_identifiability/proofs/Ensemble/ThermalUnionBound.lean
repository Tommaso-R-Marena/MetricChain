import Mathlib

/-!
# The thermal union bound: the core inequality

Ensemble division (`docs/ensemble/ENSEMBLE_REPORT.md`, Part IV, Theorem E15(c)).

Let the sites of a binary product space be independent, site `i` being in its "excited" state
`true` with probability `p_i`.  Let `r ≥ 0` be a function of the configuration that does not
decrease when a site is switched from `false` to `true` (in the report: the density of a member
of a first-order class with respect to the most polarised member; `true` = the site disagrees
with the centre).  Then

    E |r − E r|  ≤  2 · Σ_i ( E[r · 1{x_i = true}] − p_i · E r ) .

The right-hand side is twice the sum of the covariances of `r` with the single sites; when `r`
is a probability density it is twice the sum of the *one-body deficits*, and the left-hand side
is twice the total variation distance.  The constant is sharp (`thermal_union_bound_sharp`).

The product expectation is defined by iterating over the sites (`prodE`), configurations being
lists of Booleans; no measure theory is used.  The proof is an induction over the sites: one
site contributes `2 p (1 − p) (m₁ − m₀)`, which is twice its covariance with `r`.
-/

namespace MetricChain.Ensemble

/-- Expectation under the product measure on `{false, true}ⁿ` in which site `i` is `true` with
probability `ps[i]`, defined by iterating over the sites. -/
def prodE : List ℝ → (List Bool → ℝ) → ℝ
  | [], f => f []
  | p :: ps, f => (1 - p) * prodE ps (fun x => f (false :: x)) + p * prodE ps (fun x => f (true :: x))

theorem prodE_cons (p : ℝ) (ps : List ℝ) (f : List Bool → ℝ) :
    prodE (p :: ps) f =
      (1 - p) * prodE ps (fun x => f (false :: x)) + p * prodE ps (fun x => f (true :: x)) := rfl

theorem prodE_const (ps : List ℝ) (c : ℝ) : prodE ps (fun _ => c) = c := by
  induction ps with
  | nil => rfl
  | cons p ps ih =>
    rw [prodE_cons, ih]
    ring

theorem prodE_add (ps : List ℝ) (f g : List Bool → ℝ) :
    prodE ps (fun x => f x + g x) = prodE ps f + prodE ps g := by
  induction ps generalizing f g with
  | nil => rfl
  | cons p ps ih =>
    rw [prodE_cons, prodE_cons, prodE_cons, ih, ih]
    ring

theorem prodE_mul_left (ps : List ℝ) (c : ℝ) (f : List Bool → ℝ) :
    prodE ps (fun x => c * f x) = c * prodE ps f := by
  induction ps generalizing f with
  | nil => rfl
  | cons p ps ih =>
    rw [prodE_cons, prodE_cons, ih, ih]
    ring

theorem prodE_mono (ps : List ℝ) (hp : ∀ p ∈ ps, 0 ≤ p ∧ p ≤ 1) (f g : List Bool → ℝ)
    (h : ∀ x, f x ≤ g x) : prodE ps f ≤ prodE ps g := by
  induction ps generalizing f g with
  | nil => exact h []
  | cons p ps ih =>
    have hp0 := (hp p (List.mem_cons_self)).1
    have hp1 := (hp p (List.mem_cons_self)).2
    have hps : ∀ q ∈ ps, 0 ≤ q ∧ q ≤ 1 := fun q hq => hp q (List.mem_cons_of_mem p hq)
    rw [prodE_cons, prodE_cons]
    have h0 := ih hps (fun x => f (false :: x)) (fun x => g (false :: x)) (fun x => h _)
    have h1 := ih hps (fun x => f (true :: x)) (fun x => g (true :: x)) (fun x => h _)
    have e0 := mul_le_mul_of_nonneg_left h0 (sub_nonneg.mpr hp1)
    have e1 := mul_le_mul_of_nonneg_left h1 hp0
    linarith

/-- Changing the centre of an absolute deviation costs at most the distance of the centres. -/
theorem prodE_abs_sub_le (ps : List ℝ) (hp : ∀ p ∈ ps, 0 ≤ p ∧ p ≤ 1) (f : List Bool → ℝ)
    (c c' : ℝ) :
    prodE ps (fun x => |f x - c|) ≤ prodE ps (fun x => |f x - c'|) + |c' - c| := by
  have h := prodE_mono ps hp (fun x => |f x - c|) (fun x => |f x - c'| + |c' - c|)
    (fun x => by
      have e : f x - c = (f x - c') + (c' - c) := by ring
      rw [e]
      exact abs_add_le _ _)
  rw [prodE_add, prodE_const] at h
  exact h

/-- Indicator that site `i` of the configuration `x` is `true`. -/
def siteInd (i : ℕ) (x : List Bool) : ℝ := if x.getD i false = true then 1 else 0

theorem siteInd_zero_cons (b : Bool) (x : List Bool) :
    siteInd 0 (b :: x) = if b = true then 1 else 0 := by
  simp [siteInd]

theorem siteInd_succ_cons (i : ℕ) (b : Bool) (x : List Bool) :
    siteInd (i + 1) (b :: x) = siteInd i x := by
  simp [siteInd]

/-- The sum over the sites of `E[r · 1{x_i = true}] − p_i · E r` (the covariances of `r` with the
sites; for a probability density `r`, the one-body deficits). -/
noncomputable def deficit (ps : List ℝ) (r : List Bool → ℝ) : ℝ :=
  ∑ i ∈ Finset.range ps.length,
    (prodE ps (fun x => r x * siteInd i x) - ps.getD i 0 * prodE ps r)

theorem deficit_nil (r : List Bool → ℝ) : deficit [] r = 0 := by
  simp [deficit]

theorem deficit_cons (p : ℝ) (ps : List ℝ) (r : List Bool → ℝ) :
    deficit (p :: ps) r =
      p * (1 - p) * (prodE ps (fun x => r (true :: x)) - prodE ps (fun x => r (false :: x)))
        + (1 - p) * deficit ps (fun x => r (false :: x))
        + p * deficit ps (fun x => r (true :: x)) := by
  unfold deficit
  rw [List.length_cons, Finset.sum_range_succ']
  have h0 : prodE (p :: ps) (fun x => r x * siteInd 0 x) = p * prodE ps (fun x => r (true :: x)) := by
    rw [prodE_cons]
    have e0 : (fun x : List Bool => r (false :: x) * siteInd 0 (false :: x)) = fun _ => (0 : ℝ) := by
      funext x
      rw [siteInd_zero_cons]
      simp
    have e1 : (fun x : List Bool => r (true :: x) * siteInd 0 (true :: x)) = fun x => r (true :: x) := by
      funext x
      rw [siteInd_zero_cons]
      simp
    rw [e0, e1, prodE_const]
    ring
  have hs : ∀ i : ℕ,
      prodE (p :: ps) (fun x => r x * siteInd (i + 1) x) - (p :: ps).getD (i + 1) 0 * prodE (p :: ps) r
        = (1 - p) * (prodE ps (fun x => r (false :: x) * siteInd i x)
              - ps.getD i 0 * prodE ps (fun x => r (false :: x)))
          + p * (prodE ps (fun x => r (true :: x) * siteInd i x)
              - ps.getD i 0 * prodE ps (fun x => r (true :: x))) := by
    intro i
    rw [prodE_cons, prodE_cons]
    have e0 : (fun x : List Bool => r (false :: x) * siteInd (i + 1) (false :: x))
        = fun x => r (false :: x) * siteInd i x := by
      funext x
      rw [siteInd_succ_cons]
    have e1 : (fun x : List Bool => r (true :: x) * siteInd (i + 1) (true :: x))
        = fun x => r (true :: x) * siteInd i x := by
      funext x
      rw [siteInd_succ_cons]
    rw [e0, e1, List.getD_cons_succ]
    ring
  rw [Finset.sum_congr rfl (fun i _ => hs i), Finset.sum_add_distrib, ← Finset.mul_sum,
    ← Finset.mul_sum, h0, List.getD_cons_zero, prodE_cons]
  ring

/-- **The thermal union bound, core inequality.**  For independent binary sites and a function
`r` that does not decrease when a site is switched from `false` to `true`,
`E|r − E r| ≤ 2 Σ_i (E[r·1{x_i = true}] − p_i E r)`. -/
theorem thermal_union_bound (ps : List ℝ) (hp : ∀ p ∈ ps, 0 ≤ p ∧ p ≤ 1) (r : List Bool → ℝ)
    (hmono : ∀ pre suf : List Bool, r (pre ++ false :: suf) ≤ r (pre ++ true :: suf)) :
    prodE ps (fun x => |r x - prodE ps r|) ≤ 2 * deficit ps r := by
  induction ps generalizing r with
  | nil =>
    rw [deficit_nil]
    show |r [] - r []| ≤ 2 * 0
    simp
  | cons p ps ih =>
    have hp0 := (hp p (List.mem_cons_self)).1
    have hp1 := (hp p (List.mem_cons_self)).2
    have hps : ∀ q ∈ ps, 0 ≤ q ∧ q ≤ 1 := fun q hq => hp q (List.mem_cons_of_mem p hq)
    set m0 := prodE ps (fun x => r (false :: x)) with hm0
    set m1 := prodE ps (fun x => r (true :: x)) with hm1
    have hm : prodE (p :: ps) r = (1 - p) * m0 + p * m1 := prodE_cons p ps r
    have hle : m0 ≤ m1 :=
      prodE_mono ps hps _ _ (fun x => by simpa using hmono [] x)
    have ih0 := ih hps (fun x => r (false :: x)) (fun pre suf => hmono (false :: pre) suf)
    have ih1 := ih hps (fun x => r (true :: x)) (fun pre suf => hmono (true :: pre) suf)
    have s0 := prodE_abs_sub_le ps hps (fun x => r (false :: x)) (prodE (p :: ps) r) m0
    have s1 := prodE_abs_sub_le ps hps (fun x => r (true :: x)) (prodE (p :: ps) r) m1
    have d0 : |m0 - prodE (p :: ps) r| = p * (m1 - m0) := by
      rw [hm]
      have e : m0 - ((1 - p) * m0 + p * m1) = -(p * (m1 - m0)) := by ring
      rw [e, abs_neg, abs_of_nonneg (mul_nonneg hp0 (sub_nonneg.mpr hle))]
    have d1 : |m1 - prodE (p :: ps) r| = (1 - p) * (m1 - m0) := by
      rw [hm]
      have e : m1 - ((1 - p) * m0 + p * m1) = (1 - p) * (m1 - m0) := by ring
      rw [e, abs_of_nonneg (mul_nonneg (sub_nonneg.mpr hp1) (sub_nonneg.mpr hle))]
    rw [d0] at s0
    rw [d1] at s1
    have lhs : prodE (p :: ps) (fun x => |r x - prodE (p :: ps) r|)
        = (1 - p) * prodE ps (fun x => |r (false :: x) - prodE (p :: ps) r|)
          + p * prodE ps (fun x => |r (true :: x) - prodE (p :: ps) r|) := prodE_cons p ps _
    rw [lhs, deficit_cons]
    have e0 := mul_le_mul_of_nonneg_left s0 (sub_nonneg.mpr hp1)
    have e1 := mul_le_mul_of_nonneg_left s1 hp0
    have f0 := mul_le_mul_of_nonneg_left ih0 (sub_nonneg.mpr hp1)
    have f1 := mul_le_mul_of_nonneg_left ih1 hp0
    nlinarith [e0, e1, f0, f1]

/-- **The thermal union bound for a density.**  If moreover `E r = 1` (`r` is the density of a
probability measure `μ` with respect to the product measure), the left-hand side is twice the
total variation distance and the right-hand side is twice the sum over the sites of
`μ(x_i = true) − p_i`, the one-body deficits. -/
theorem thermal_union_bound_density (ps : List ℝ) (hp : ∀ p ∈ ps, 0 ≤ p ∧ p ≤ 1)
    (r : List Bool → ℝ)
    (hmono : ∀ pre suf : List Bool, r (pre ++ false :: suf) ≤ r (pre ++ true :: suf))
    (hr : prodE ps r = 1) :
    prodE ps (fun x => |r x - 1|) ≤
      2 * ∑ i ∈ Finset.range ps.length, (prodE ps (fun x => r x * siteInd i x) - ps.getD i 0) := by
  have h := thermal_union_bound ps hp r hmono
  simp only [deficit, hr, mul_one] at h
  exact h

/-- **Sharpness.**  On one site, for the function that is `2` on the excited state and `0`
otherwise, the two sides of `thermal_union_bound` are equal (both are `4 p (1 − p)`). -/
theorem thermal_union_bound_sharp (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    prodE [p] (fun x => |(if x = [true] then (2 : ℝ) else 0)
        - prodE [p] (fun x => if x = [true] then (2 : ℝ) else 0)|)
      = 2 * deficit [p] (fun x => if x = [true] then (2 : ℝ) else 0) := by
  have hE : prodE [p] (fun x => if x = [true] then (2 : ℝ) else 0) = 2 * p := by
    simp [prodE]
    ring
  have hD : deficit [p] (fun x => if x = [true] then (2 : ℝ) else 0) = 2 * p * (1 - p) := by
    rw [deficit_cons, deficit_nil, deficit_nil]
    simp [prodE]
    ring
  rw [hD, hE]
  have a0 : |(0 : ℝ) - 2 * p| = 2 * p := by
    rw [zero_sub, abs_neg, abs_of_nonneg (by linarith)]
  have a1 : |(2 : ℝ) - 2 * p| = 2 - 2 * p := abs_of_nonneg (by linarith)
  have hL : prodE [p] (fun x => |(if x = [true] then (2 : ℝ) else 0) - 2 * p|)
      = (1 - p) * |(0 : ℝ) - 2 * p| + p * |(2 : ℝ) - 2 * p| := by
    simp [prodE]
  rw [hL, a0, a1]
  ring

end MetricChain.Ensemble
