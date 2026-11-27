import Mathlib
import proofs.Core.Basic
import proofs.Frontiers.EnvelopeDuality
import proofs.Frontiers.CertificationGeometry
import proofs.Frontiers.ThermalRobustness

/-!
# Exponential-weights converses for certificate size, at zero and at finite temperature

Setting of `CertificationGeometry.lean` and `ThermalRobustness.lean`: known part `f`, residual `g`
admissible for an envelope `d`, energy `E = f + g`, slack `s(a, y) = d a y - g a + g y`, and a
finite set `A` of evaluated points.

**Zero temperature** (`card_ge_exp_weights`).  If every `y` is covered by some `a ∈ A`
(`s(a, y) ≤ E y - Estar + ε`), then for every `t ≥ 0` and every nonnegative weight `v`

  `e^{-tε} ∑_y v y ≤ |A| · max_a ∑_y v y e^{-t (s(a, y) - (E y - Estar))}`.

`partition_bound` is the choice `v y = e^{-t (E y - Estar)}`.  The supremum of the bound over `t`
and `v` is the dual (Csiszár) form of `max_P R(P, ε)`, the largest rate–distortion function over
sources `P` for the distortion `s(a, y) - gap y`; on product landscapes it is attained by product
weights and gives the exact exponential growth rate of the minimal certificate (theory report
§11.4; the matching upper bound is the type covering lemma and is not formalised).

**Finite temperature.**  A free-energy certificate (the optimistic partition function within the
factor `e^ε` of the true one) satisfies:

* `card_ge_entropy` — for every `t ≥ 0`,
  `H(π) ≤ log (|A| · max_a ∑_y e^{-t s(a, y)}) + t ε / β`, with `H(π)` the Shannon entropy of the
  Gibbs ensemble: the number of evaluations is at least `exp (entropy)` divided by the partition
  sum of a slack ball.  (Gibbs' inequality plus `mean_slack_le`.)
* `thermal_exp_weights` — for every `p ∈ (0, 1)` and every nonnegative weight `v`,
  `∑_y π(y)^{1-p} v(y)^p ≤ (|A| · max_a ∑_y v y e^{-t s(a, y)})^p · e^{(1-p) ε}`, `t = β(1-p)/p`.
  (Hölder's inequality.)  Its optimum over `p` and `v` is the dual form of
  `max_Q R(Q; s, KL(Q ‖ π)/β)`: the rate–distortion function of the macrostate `Q` at a distortion
  equal to its *free-energy gap* `F[Q] - F = KL(Q ‖ π)/β`.  As `β → ∞` this is the
  zero-temperature statement with the energy gap in place of the free-energy gap.
-/

namespace MetricChain

open Finset

variable {X : Type*} [Fintype X]

/-! ### Zero temperature -/

/-- **Exponential-weights converse.**  If the evaluated set `A` covers every point at the level
`Estar - ε`, then for every `t ≥ 0`, every nonnegative weight `v`, and every bound `B` on the
weighted partition sums `∑_y v y · exp (-t (slack a y - (E y - Estar)))` of the evaluated points,
`exp (-t ε) · ∑_y v y ≤ |A| · B`. -/
theorem card_ge_exp_weights {d : X → X → ℝ} {f g : X → ℝ} {A : Finset X} {ε Estar t B : ℝ}
    (ht : 0 ≤ t) (v : X → ℝ) (hv : ∀ y, 0 ≤ v y)
    (hcov : ∀ y, ∃ a ∈ A, Covers d f g Estar ε a y)
    (hB : ∀ a ∈ A, ∑ y, v y * Real.exp (-t * (slack d g a y - (f y + g y - Estar))) ≤ B) :
    Real.exp (-t * ε) * ∑ y, v y ≤ A.card * B := by
  calc Real.exp (-t * ε) * ∑ y, v y
      = ∑ y, v y * Real.exp (-t * ε) := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun y _ => mul_comm _ _
    _ ≤ ∑ y, ∑ a ∈ A, v y * Real.exp (-t * (slack d g a y - (f y + g y - Estar))) := by
        refine Finset.sum_le_sum fun y _ => ?_
        obtain ⟨a, ha, hcy⟩ := hcov y
        have hcy' : slack d g a y ≤ f y + g y - Estar + ε := hcy
        have h1 : Real.exp (-t * ε) ≤
            Real.exp (-t * (slack d g a y - (f y + g y - Estar))) := by
          apply Real.exp_le_exp.mpr
          nlinarith
        calc v y * Real.exp (-t * ε)
            ≤ v y * Real.exp (-t * (slack d g a y - (f y + g y - Estar))) :=
              mul_le_mul_of_nonneg_left h1 (hv y)
          _ ≤ ∑ a ∈ A, v y * Real.exp (-t * (slack d g a y - (f y + g y - Estar))) :=
              Finset.single_le_sum
                (f := fun a => v y * Real.exp (-t * (slack d g a y - (f y + g y - Estar))))
                (fun a _ => mul_nonneg (hv y) (Real.exp_pos _).le) ha
    _ = ∑ a ∈ A, ∑ y, v y * Real.exp (-t * (slack d g a y - (f y + g y - Estar))) :=
        Finset.sum_comm
    _ ≤ ∑ _a ∈ A, B := Finset.sum_le_sum fun a ha => hB a ha
    _ = A.card * B := by rw [Finset.sum_const, nsmul_eq_mul]

/-- The exponential-weights converse for an `ε`-certificate (`cover_of_certificate`). -/
theorem card_ge_exp_weights_certificate [Nonempty X] {d : X → X → ℝ} {f g : X → ℝ}
    {A : Finset X} {hA : A.Nonempty} {ε Estar t B : ℝ} (ht : 0 ≤ t) (v : X → ℝ)
    (hv : ∀ y, 0 ≤ v y) (hE : ∀ y, Estar ≤ f y + g y) (hcert : IsCertificate d f g A hA ε)
    (hB : ∀ a ∈ A, ∑ y, v y * Real.exp (-t * (slack d g a y - (f y + g y - Estar))) ≤ B) :
    Real.exp (-t * ε) * ∑ y, v y ≤ A.card * B :=
  card_ge_exp_weights ht v hv (cover_of_certificate hE hcert) hB

/-! ### Finite temperature -/

section Thermal

variable [Nonempty X]

/-- Gibbs probabilities are strictly positive. -/
theorem gibbsProb_pos (β : ℝ) (E : X → ℝ) (x : X) : 0 < gibbsProb β E x := by
  unfold gibbsProb
  exact div_pos (Real.exp_pos _) (Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty)

/-- **Gibbs' inequality.**  For a strictly positive probability vector `p` and strictly positive
weights `u`, `-∑ p log p ≤ -∑ p log u + log ∑ u`. -/
theorem entropy_le_cross (p u : X → ℝ) (hp : ∀ x, 0 < p x) (hsum : ∑ x, p x = 1)
    (hu : ∀ x, 0 < u x) :
    -∑ x, p x * Real.log (p x) ≤ -∑ x, p x * Real.log (u x) + Real.log (∑ x, u x) := by
  have hS : 0 < ∑ x, u x := Finset.sum_pos (fun x _ => hu x) univ_nonempty
  have hterm : ∀ x, p x * (Real.log (u x) - Real.log (p x) - Real.log (∑ z, u z)) ≤
      u x / (∑ z, u z) - p x := by
    intro x
    have hr : 0 < u x / ((∑ z, u z) * p x) := div_pos (hu x) (mul_pos hS (hp x))
    have hlog := Real.log_le_sub_one_of_pos hr
    rw [Real.log_div (hu x).ne' (mul_pos hS (hp x)).ne',
      Real.log_mul hS.ne' (hp x).ne'] at hlog
    have hmul := mul_le_mul_of_nonneg_left hlog (hp x).le
    have he : p x * (u x / ((∑ z, u z) * p x) - 1) = u x / (∑ z, u z) - p x := by
      have hpx : p x ≠ 0 := (hp x).ne'
      have hSne : (∑ z, u z) ≠ 0 := hS.ne'
      have h1 : p x * (u x / ((∑ z, u z) * p x)) = u x / (∑ z, u z) := by
        field_simp
      rw [mul_sub, h1, mul_one]
    rw [he] at hmul
    linarith
  have hsumle := Finset.sum_le_sum fun x (_ : x ∈ univ) => hterm x
  have hR : ∑ x, (u x / (∑ z, u z) - p x) = 0 := by
    rw [Finset.sum_sub_distrib, ← Finset.sum_div, div_self hS.ne', hsum, sub_self]
  rw [hR] at hsumle
  have hL : ∑ x, p x * (Real.log (u x) - Real.log (p x) - Real.log (∑ z, u z)) =
      ∑ x, p x * Real.log (u x) - ∑ x, p x * Real.log (p x) - Real.log (∑ z, u z) := by
    have h1 : ∀ x, p x * (Real.log (u x) - Real.log (p x) - Real.log (∑ z, u z)) =
        p x * Real.log (u x) - p x * Real.log (p x) - p x * Real.log (∑ z, u z) := fun x => by
      ring
    rw [Finset.sum_congr rfl fun x _ => h1 x, Finset.sum_sub_distrib, Finset.sum_sub_distrib,
      ← Finset.sum_mul, hsum, one_mul]
  rw [hL] at hsumle
  linarith

omit [Nonempty X] in
/-- The partition sum of the slack distance from `A` is at most the sum of the partition sums of
the evaluated points: `∑_y v y e^{-t s(A, y)} ≤ |A| · B`. -/
theorem sum_exp_slackFrom_le (d : X → X → ℝ) (g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    {t B : ℝ} (v : X → ℝ) (hv : ∀ y, 0 ≤ v y)
    (hB : ∀ a ∈ A, ∑ y, v y * Real.exp (-t * slack d g a y) ≤ B) :
    ∑ y, v y * Real.exp (-t * slackFrom d g A hA y) ≤ A.card * B := by
  calc ∑ y, v y * Real.exp (-t * slackFrom d g A hA y)
      ≤ ∑ y, ∑ a ∈ A, v y * Real.exp (-t * slack d g a y) := by
        refine Finset.sum_le_sum fun y _ => ?_
        obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g a y)
        have hs : slackFrom d g A hA y = slack d g a y := hmin
        rw [hs]
        exact Finset.single_le_sum
          (f := fun a => v y * Real.exp (-t * slack d g a y))
          (fun a _ => mul_nonneg (hv y) (Real.exp_pos _).le) ha
    _ = ∑ a ∈ A, ∑ y, v y * Real.exp (-t * slack d g a y) := Finset.sum_comm
    _ ≤ ∑ _a ∈ A, B := Finset.sum_le_sum fun a ha => hB a ha
    _ = A.card * B := by rw [Finset.sum_const, nsmul_eq_mul]

/-- **Entropy bound for free-energy certificates.**  If the optimistic partition function of the
evaluated set `A` is within the factor `exp ε` of the true one (`β > 0`), and `B` bounds the
partition sums `∑_y exp (-t · slack a y)` of the evaluated points, then the Shannon entropy of
the Gibbs ensemble satisfies

  `H(π) ≤ log (|A| · B) + t ε / β`     for every `t ≥ 0`.

So `|A| ≥ exp (H(π) - t ε / β) / B`: a free-energy certificate under envelope uncertainty needs
at least `exp (entropy)` evaluations, up to the partition sum of a slack ball. -/
theorem card_ge_entropy (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    {β ε t B : ℝ} (hβ : 0 < β) (ht : 0 ≤ t)
    (hcert : ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + g y)))
    (hB : ∀ a ∈ A, ∑ y, Real.exp (-t * slack d g a y) ≤ B) :
    -∑ y, gibbsProb β (fun y => f y + g y) y *
        Real.log (gibbsProb β (fun y => f y + g y) y) ≤
      Real.log (A.card * B) + t * ε / β := by
  set π := gibbsProb β (fun y => f y + g y) with hπ
  have hG := entropy_le_cross π (fun y => Real.exp (-t * slackFrom d g A hA y))
    (fun y => gibbsProb_pos β _ y) (sum_gibbsProb β _) (fun y => Real.exp_pos _)
  have hmean := mean_slack_le d f g A hA hcert
  have hS : ∑ y, Real.exp (-t * slackFrom d g A hA y) ≤ A.card * B := by
    have := sum_exp_slackFrom_le d g A hA (t := t) (fun _ => (1 : ℝ)) (fun _ => zero_le_one)
      (by simpa using hB)
    simpa using this
  have hSpos : 0 < ∑ y, Real.exp (-t * slackFrom d g A hA y) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hlog := Real.log_le_log hSpos hS
  have hcross : -∑ y, π y * Real.log (Real.exp (-t * slackFrom d g A hA y)) =
      t * ∑ y, π y * slackFrom d g A hA y := by
    rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [Real.log_exp]
    ring
  rw [hcross] at hG
  have htβ : t * ∑ y, π y * slackFrom d g A hA y ≤ t * ε / β := by
    have h1 : ∑ y, π y * slackFrom d g A hA y ≤ ε / β := by
      rw [le_div_iff₀ hβ]
      linarith [hmean]
    calc t * ∑ y, π y * slackFrom d g A hA y ≤ t * (ε / β) := mul_le_mul_of_nonneg_left h1 ht
      _ = t * ε / β := by ring
  linarith

omit [Nonempty X] in
/-- **Exponential-weights converse at finite temperature (Hölder form).**  Let the optimistic
partition function of the evaluated set `A` be within the factor `exp ε` of the true one (the
regime of interest is `β > 0`; the inequality does not need it).  For `p ∈ (0, 1)` put
`t = β (1 - p) / p`.  Then for every nonnegative weight `v` and
every bound `B` on the weighted partition sums `∑_y v y · exp (-t · slack a y)`,

  `∑_y π(y)^{1-p} · v(y)^p ≤ (|A| · B)^p · exp ((1 - p) ε)`.

Proof: Hölder's inequality with exponents `1/p`, `1/(1-p)` for the functions
`(v e^{-t s})^p` and `(π e^{β s})^{1-p}`, `s = s(A, ·)`, whose product is `π^{1-p} v^p` because
`t p = β (1 - p)`; then `∑ v e^{-t s} ≤ |A| B` and `∑ π e^{β s} ≤ e^ε`. -/
theorem thermal_exp_weights (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    {β ε p B : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (v : X → ℝ) (hv : ∀ y, 0 ≤ v y)
    (hcert : ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + g y)))
    (hB : ∀ a ∈ A, ∑ y, v y * Real.exp (-(β * (1 - p) / p) * slack d g a y) ≤ B) :
    ∑ y, gibbsProb β (fun y => f y + g y) y ^ (1 - p) * v y ^ p ≤
      (A.card * B) ^ p * Real.exp ((1 - p) * ε) := by
  set π := gibbsProb β (fun y => f y + g y) with hπ
  set t := β * (1 - p) / p with ht
  set s := slackFrom d g A hA with hs
  have hq0 : 0 < 1 - p := sub_pos.mpr hp1
  have hπ0 : ∀ y, 0 ≤ π y := fun y => gibbsProb_nonneg β _ y
  have hconj : (1 / p).HolderConjugate (1 / (1 - p)) :=
    Real.holderConjugate_one_div hp0 hq0 (by ring)
  -- the two Hölder factors
  have hF0 : ∀ y, 0 ≤ v y * Real.exp (-t * s y) := fun y =>
    mul_nonneg (hv y) (Real.exp_pos _).le
  have hG0 : ∀ y, 0 ≤ π y * Real.exp (β * s y) := fun y =>
    mul_nonneg (hπ0 y) (Real.exp_pos _).le
  have hprod : ∀ y, (v y * Real.exp (-t * s y)) ^ p * (π y * Real.exp (β * s y)) ^ (1 - p) =
      π y ^ (1 - p) * v y ^ p := by
    intro y
    rw [Real.mul_rpow (hv y) (Real.exp_pos _).le, Real.mul_rpow (hπ0 y) (Real.exp_pos _).le,
      ← Real.exp_mul, ← Real.exp_mul]
    have hexp : Real.exp (-t * s y * p) * Real.exp (β * s y * (1 - p)) = 1 := by
      have h0 : -t * s y * p + β * s y * (1 - p) = 0 := by
        rw [ht]
        field_simp
        ring
      rw [← Real.exp_add, h0, Real.exp_zero]
    calc v y ^ p * Real.exp (-t * s y * p) * (π y ^ (1 - p) * Real.exp (β * s y * (1 - p)))
        = π y ^ (1 - p) * v y ^ p *
            (Real.exp (-t * s y * p) * Real.exp (β * s y * (1 - p))) := by ring
      _ = π y ^ (1 - p) * v y ^ p := by rw [hexp, mul_one]
  have hH := Real.inner_le_Lp_mul_Lq_of_nonneg univ hconj
    (f := fun y => (v y * Real.exp (-t * s y)) ^ p)
    (g := fun y => (π y * Real.exp (β * s y)) ^ (1 - p))
    (fun y _ => Real.rpow_nonneg (hF0 y) _) (fun y _ => Real.rpow_nonneg (hG0 y) _)
  have hFp : ∀ y, ((v y * Real.exp (-t * s y)) ^ p) ^ (1 / p) = v y * Real.exp (-t * s y) := by
    intro y
    rw [← Real.rpow_mul (hF0 y), mul_one_div_cancel hp0.ne', Real.rpow_one]
  have hGq : ∀ y, ((π y * Real.exp (β * s y)) ^ (1 - p)) ^ (1 / (1 - p)) =
      π y * Real.exp (β * s y) := by
    intro y
    rw [← Real.rpow_mul (hG0 y), mul_one_div_cancel hq0.ne', Real.rpow_one]
  simp only [hprod, hFp, hGq, one_div_one_div] at hH
  -- the two sums
  have hS1 : ∑ y, v y * Real.exp (-t * s y) ≤ A.card * B :=
    sum_exp_slackFrom_le d g A hA v hv hB
  have hS1' : 0 ≤ ∑ y, v y * Real.exp (-t * s y) := Finset.sum_nonneg fun y _ => hF0 y
  have hS2 : ∑ y, π y * Real.exp (β * s y) ≤ Real.exp ε := mean_exp_slack_le d f g A hA hcert
  have hS2' : 0 ≤ ∑ y, π y * Real.exp (β * s y) := Finset.sum_nonneg fun y _ => hG0 y
  calc ∑ y, π y ^ (1 - p) * v y ^ p
      ≤ (∑ y, v y * Real.exp (-t * s y)) ^ p * (∑ y, π y * Real.exp (β * s y)) ^ (1 - p) := hH
    _ ≤ (A.card * B) ^ p * Real.exp ε ^ (1 - p) :=
        mul_le_mul (Real.rpow_le_rpow hS1' hS1 hp0.le) (Real.rpow_le_rpow hS2' hS2 hq0.le)
          (Real.rpow_nonneg hS2' _) (Real.rpow_nonneg (hS1'.trans hS1) _)
    _ = (A.card * B) ^ p * Real.exp ((1 - p) * ε) := by
        rw [← Real.exp_mul, mul_comm ε]

end Thermal

end MetricChain
