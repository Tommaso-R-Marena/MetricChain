import Mathlib

/-!
# Recovering a partition function between a floor model and a ceiling model

Four inequalities for the logarithm of a partition function on a finite set, from a model that
lies above the true energy, a model that lies below it, and known lower bounds of the two gaps.
This is Proposition A17.19 of the Scientific Discovery Division (its addendum A17 (19); message
SCI-MSG-0028 §7, request A19-T1).  The statements are theirs; the paper proofs were re-derived by
the coordinator from that message, and this file is their machine check.  Added in the
formalisation: the two iterations do not increase (`ueStep_iterate_antitone`,
`upStep_iterate_antitone`).

## Setting

`Ω` is a non-empty finite set of configurations and `β ≥ 0`.  The true energy `E : Ω → ℝ` lies
between a floor model `mlo` and a ceiling model `mhi`, and each of the two gaps is at least a
sum of non-negative slack functions indexed by a finite type `G`:

`∑ g, Sp g ω ≤ mhi ω - E ω`  and  `∑ g, Sm g ω ≤ E ω - mlo ω`  for every `ω`.

* `Z β f = ∑ ω, exp (-β * f ω)` — the partition function of the energy function `f`.
* `avg β m X = (∑ ω, X ω * exp (-β * m ω)) / Z β m` — the mean of the observable `X` in the Gibbs
  ensemble of the model `m`.

The right-hand sides of the four inequalities contain the partition functions of the two models
and means under the ceiling model, `avg β mhi`, only.  The mean under the true ensemble,
`avg β E`, occurs in the proofs.

## Results

* `lower_jensen` — **(LJ)** `log (Z mhi) + β * ∑ g, avg β mhi (Sp g) ≤ log (Z E)` (the signs of
  the slack functions are not used).
* `lower_product` — **(LP)**
  `log (Z mhi) + log (1 + ∑ g, avg β mhi (exp (β * Sp g) - 1)) ≤ log (Z E)`.
* `upper_jensen` — **(UE)** if `log (Z E) ≤ u`, then
  `log (Z E) ≤ log (Z mlo) - β * (∑ g, avg β mhi (Sm g * exp (β * Sp g))) * exp (log (Z mhi) - u)`.
* `upper_product` — **(UP)** if `log (Z E) ≤ u`, then `log (Z E) ≤ log (Z mlo) -
  log (1 + (∑ g, avg β mhi ((exp (β * Sm g) - 1) * exp (β * Sp g))) * exp (log (Z mhi) - u))`.
* `log_Z_le_log_Z_floor`, `log_Z_le_of_steps`, `log_Z_le_ueStep_iterate`,
  `log_Z_le_upStep_iterate` — `log (Z E) ≤ log (Z mlo)`, and every sequence that starts at an
  upper bound of `log (Z E)` (for instance at `log (Z mlo)`) and passes from `u` to the
  right-hand side of (UE) or of (UP) at `u` (`ueStep`, `upStep`) consists of upper bounds of
  `log (Z E)`.
* `ueStep_iterate_antitone`, `upStep_iterate_antitone` — the two iterations from `log (Z mlo)`
  do not increase.

## Proofs

Change of measure (`Z_div_eq_avg`): `Z b / Z a = avg β a (exp (β * (a - b)))`.  If
`∑ g, S g ≤ a - b`, this is at least `avg β a (exp (β * ∑ g, S g))`, which is at least
`exp (β * ∑ g, avg β a (S g))` by Jensen's inequality for `exp` (`exp_slack_le_Z_div`), and, for
`S ≥ 0`, at least `1 + ∑ g, avg β a (exp (β * S g) - 1)` by `1 + ∑ y_g ≤ ∏ (1 + y_g)` for
`y_g = exp (β * S g ω) - 1 ≥ 0` (`one_add_slack_le_Z_div`).  With `a = mhi`, `b = E`, `S = Sp`
these are (LJ) and (LP).  With `a = E`, `b = mlo`, `S = Sm` they are upper bounds of `log (Z E)`
in terms of means under the true ensemble; such a mean of an observable `X ≥ 0` is bounded from
below by a mean under the ceiling model (`avg_ceiling_le_avg_true`): for a slack `S` with
`E ≤ mhi - S` and for `Z E ≤ exp u`,

`avg β E X ≥ (Z mhi / Z E) * avg β mhi (X * exp (β * S))`
`          ≥ exp (log (Z mhi) - u) * avg β mhi (X * exp (β * S))`.

(UE) is the case `X = Sm g`, `S = Sp g`, and (UP) the case `X = exp (β * Sm g) - 1`, `S = Sp g`.
This last step is the only one that is not the textbook argument: it replaces the true ensemble,
which is not available, by the ceiling model at the price of the factor `exp (log (Z mhi) - u)`.

## Not proved here

That given models and slack functions satisfy the two hypotheses; how the partition functions
of the two models and the means under the ceiling model are computed (the transfer matrices are
not formalised); anything about the floating-point evaluation of the right-hand sides.
-/

namespace MetricChain.GibbsRecovery

variable {Ω : Type*} [Fintype Ω]

/-! ### Partition functions and Gibbs means -/

/-- The partition function `Z f = ∑ ω, exp (-β f ω)` of the energy function `f`. -/
noncomputable def Z (β : ℝ) (f : Ω → ℝ) : ℝ := ∑ ω, Real.exp (-β * f ω)

/-- The mean of the observable `X` in the Gibbs ensemble of the model `m`:
`avg β m X = (∑ ω, X ω * exp (-β m ω)) / Z m`. -/
noncomputable def avg (β : ℝ) (m X : Ω → ℝ) : ℝ := (∑ ω, X ω * Real.exp (-β * m ω)) / Z β m

/-- A partition function on a non-empty finite set is positive. -/
theorem Z_pos [Nonempty Ω] (β : ℝ) (f : Ω → ℝ) : 0 < Z β f :=
  Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty

/-- Gibbs means are monotone in the observable. -/
theorem avg_mono [Nonempty Ω] (β : ℝ) (m : Ω → ℝ) {X Y : Ω → ℝ} (h : ∀ ω, X ω ≤ Y ω) :
    avg β m X ≤ avg β m Y := by
  unfold avg
  refine div_le_div_of_nonneg_right (Finset.sum_le_sum fun ω _ => ?_) (Z_pos β m).le
  exact mul_le_mul_of_nonneg_right (h ω) (Real.exp_pos _).le

/-- The Gibbs mean of a non-negative observable is non-negative. -/
theorem avg_nonneg [Nonempty Ω] (β : ℝ) (m : Ω → ℝ) {X : Ω → ℝ} (h : ∀ ω, 0 ≤ X ω) :
    0 ≤ avg β m X :=
  div_nonneg (Finset.sum_nonneg fun ω _ => mul_nonneg (h ω) (Real.exp_pos _).le) (Z_pos β m).le

/-- The Gibbs mean of the constant `1` is `1`. -/
theorem avg_one [Nonempty Ω] (β : ℝ) (m : Ω → ℝ) : avg β m (fun _ => 1) = 1 := by
  unfold avg
  simp only [one_mul]
  exact div_self (Z_pos β m).ne'

/-- Gibbs means are additive. -/
theorem avg_add (β : ℝ) (m X Y : Ω → ℝ) :
    avg β m (fun ω => X ω + Y ω) = avg β m X + avg β m Y := by
  unfold avg
  rw [← add_div, ← Finset.sum_add_distrib]
  congr 1
  exact Finset.sum_congr rfl fun ω _ => add_mul _ _ _

/-- The Gibbs mean of a finite sum of observables is the sum of the means. -/
theorem avg_sum {G : Type*} (s : Finset G) (β : ℝ) (m : Ω → ℝ) (X : G → Ω → ℝ) :
    avg β m (fun ω => ∑ g ∈ s, X g ω) = ∑ g ∈ s, avg β m (X g) := by
  unfold avg
  rw [← Finset.sum_div, Finset.sum_comm]
  congr 1
  exact Finset.sum_congr rfl fun ω _ => Finset.sum_mul _ _ _

/-- Constants can be pulled out of a Gibbs mean. -/
theorem avg_const_mul (β : ℝ) (m : Ω → ℝ) (c : ℝ) (X : Ω → ℝ) :
    avg β m (fun ω => c * X ω) = c * avg β m X := by
  unfold avg
  rw [← mul_div_assoc, Finset.mul_sum]
  congr 1
  exact Finset.sum_congr rfl fun ω _ => mul_assoc _ _ _

/-! ### Change of measure, Jensen's inequality, the product inequality -/

/-- **Change of measure.**  The ratio of two partition functions is a Gibbs mean under the model
in the denominator: `Z b / Z a = avg β a (exp (β (a - b)))`. -/
theorem Z_div_eq_avg (β : ℝ) (a b : Ω → ℝ) :
    Z β b / Z β a = avg β a (fun ω => Real.exp (β * (a ω - b ω))) := by
  unfold avg
  congr 1
  unfold Z
  refine Finset.sum_congr rfl fun ω _ => ?_
  rw [← Real.exp_add]
  congr 1
  ring

/-- **Jensen's inequality for `exp`** with respect to a Gibbs ensemble. -/
theorem exp_avg_le_avg_exp [Nonempty Ω] (β : ℝ) (m X : Ω → ℝ) :
    Real.exp (avg β m X) ≤ avg β m (fun ω => Real.exp (X ω)) := by
  have hZ := Z_pos β m
  have h := convexOn_exp.map_sum_le (t := Finset.univ)
    (w := fun ω => Real.exp (-β * m ω) / Z β m) (p := X)
    (fun ω _ => div_nonneg (Real.exp_pos _).le hZ.le)
    (by rw [← Finset.sum_div]; exact div_self hZ.ne')
    (fun ω _ => Set.mem_univ _)
  have e1 : avg β m X = ∑ ω, (Real.exp (-β * m ω) / Z β m) • X ω := by
    unfold avg
    rw [Finset.sum_div]
    exact Finset.sum_congr rfl fun ω _ => by rw [smul_eq_mul]; ring
  have e2 : avg β m (fun ω => Real.exp (X ω)) =
      ∑ ω, (Real.exp (-β * m ω) / Z β m) • Real.exp (X ω) := by
    unfold avg
    rw [Finset.sum_div]
    exact Finset.sum_congr rfl fun ω _ => by rw [smul_eq_mul]; ring
  rw [e1, e2]
  exact h

/-- **The Jensen bound of a ratio of partition functions.**  If the slack functions `S g` add up
to at most `a - b`, then `exp (β ∑ g, avg β a (S g)) ≤ Z b / Z a`.  No sign condition on the
slack functions is needed. -/
theorem exp_slack_le_Z_div [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (a b : Ω → ℝ) (S : G → Ω → ℝ) (hS : ∀ ω, ∑ g, S g ω ≤ a ω - b ω) :
    Real.exp (β * ∑ g, avg β a (S g)) ≤ Z β b / Z β a := by
  have e : β * ∑ g, avg β a (S g) = avg β a (fun ω => β * ∑ g, S g ω) := by
    rw [avg_const_mul, avg_sum]
  rw [e, Z_div_eq_avg]
  refine (exp_avg_le_avg_exp β a _).trans (avg_mono β a fun ω => ?_)
  exact Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left (hS ω) hβ)

/-- **The product inequality** `1 + ∑ y_g ≤ ∏ (1 + y_g)` for non-negative `y_g`. -/
theorem one_add_sum_le_prod_one_add {G : Type*} (s : Finset G) (y : G → ℝ)
    (hy : ∀ g ∈ s, 0 ≤ y g) : 1 + ∑ g ∈ s, y g ≤ ∏ g ∈ s, (1 + y g) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih =>
    rw [Finset.sum_insert ha, Finset.prod_insert ha]
    have hya : 0 ≤ y a := hy a (Finset.mem_insert_self a s)
    have ih' := ih fun g hg => hy g (Finset.mem_insert_of_mem hg)
    have hs : 0 ≤ ∑ g ∈ s, y g :=
      Finset.sum_nonneg fun g hg => hy g (Finset.mem_insert_of_mem hg)
    calc 1 + (y a + ∑ g ∈ s, y g) ≤ (1 + y a) * (1 + ∑ g ∈ s, y g) := by
          linarith [mul_nonneg hya hs]
      _ ≤ (1 + y a) * ∏ g ∈ s, (1 + y g) := mul_le_mul_of_nonneg_left ih' (by linarith)

/-- **The product bound of a ratio of partition functions.**  If the non-negative slack functions
`S g` add up to at most `a - b`, then `1 + ∑ g, avg β a (exp (β S g) - 1) ≤ Z b / Z a`. -/
theorem one_add_slack_le_Z_div [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (a b : Ω → ℝ) (S : G → Ω → ℝ) (hS0 : ∀ g ω, 0 ≤ S g ω)
    (hS : ∀ ω, ∑ g, S g ω ≤ a ω - b ω) :
    1 + ∑ g, avg β a (fun ω => Real.exp (β * S g ω) - 1) ≤ Z β b / Z β a := by
  have e : 1 + ∑ g, avg β a (fun ω => Real.exp (β * S g ω) - 1) =
      avg β a (fun ω => 1 + ∑ g, (Real.exp (β * S g ω) - 1)) := by
    rw [avg_add, avg_one, avg_sum]
  rw [e, Z_div_eq_avg]
  refine avg_mono β a fun ω => ?_
  calc 1 + ∑ g, (Real.exp (β * S g ω) - 1)
      ≤ ∏ g, (1 + (Real.exp (β * S g ω) - 1)) :=
        one_add_sum_le_prod_one_add _ _ fun g _ =>
          sub_nonneg.mpr (Real.one_le_exp (mul_nonneg hβ (hS0 g ω)))
    _ = Real.exp (β * ∑ g, S g ω) := by
        rw [Finset.mul_sum, Real.exp_sum]
        exact Finset.prod_congr rfl fun g _ => by ring
    _ ≤ Real.exp (β * (a ω - b ω)) :=
        Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left (hS ω) hβ)

/-! ### The two lower bounds -/

/-- **(LJ) Lower bound, Jensen form.**  If the slack functions `Sp g` add up to at most the gap
`mhi - E` between the ceiling model and the true energy, then

`log (Z mhi) + β * ∑ g, avg β mhi (Sp g) ≤ log (Z E)`.

The slack functions need not be non-negative here. -/
theorem lower_jensen [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (E mhi : Ω → ℝ) (Sp : G → Ω → ℝ) (hSp : ∀ ω, ∑ g, Sp g ω ≤ mhi ω - E ω) :
    Real.log (Z β mhi) + β * ∑ g, avg β mhi (Sp g) ≤ Real.log (Z β E) := by
  have h := (Real.le_log_iff_exp_le (div_pos (Z_pos β E) (Z_pos β mhi))).mpr
    (exp_slack_le_Z_div hβ mhi E Sp hSp)
  rw [Real.log_div (Z_pos β E).ne' (Z_pos β mhi).ne'] at h
  linarith

/-- **(LP) Lower bound, product form.**  If the non-negative slack functions `Sp g` add up to at
most the gap `mhi - E`, then

`log (Z mhi) + log (1 + ∑ g, avg β mhi (exp (β * Sp g) - 1)) ≤ log (Z E)`. -/
theorem lower_product [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (E mhi : Ω → ℝ) (Sp : G → Ω → ℝ) (hSp0 : ∀ g ω, 0 ≤ Sp g ω)
    (hSp : ∀ ω, ∑ g, Sp g ω ≤ mhi ω - E ω) :
    Real.log (Z β mhi) + Real.log (1 + ∑ g, avg β mhi (fun ω => Real.exp (β * Sp g ω) - 1)) ≤
      Real.log (Z β E) := by
  have hnn : 0 ≤ ∑ g, avg β mhi (fun ω => Real.exp (β * Sp g ω) - 1) :=
    Finset.sum_nonneg fun g _ => avg_nonneg β mhi fun ω =>
      sub_nonneg.mpr (Real.one_le_exp (mul_nonneg hβ (hSp0 g ω)))
  have h := Real.log_le_log (by linarith) (one_add_slack_le_Z_div hβ mhi E Sp hSp0 hSp)
  rw [Real.log_div (Z_pos β E).ne' (Z_pos β mhi).ne'] at h
  linarith

/-! ### From the true ensemble to the ceiling model -/

/-- **A mean under the true ensemble is bounded from below by a mean under the ceiling model.**
Let `S` be a slack function with `E ≤ mhi - S`, let `X ≥ 0` and `log (Z E) ≤ u`.  Then

`exp (log (Z mhi) - u) * avg β mhi (X * exp (β * S)) ≤ avg β E X`.

Indeed `exp (-β E) ≥ exp (-β mhi) * exp (β S)` pointwise, so
`avg β E X ≥ (Z mhi / Z E) * avg β mhi (X * exp (β * S))`, and `Z E ≤ exp u`. -/
theorem avg_ceiling_le_avg_true [Nonempty Ω] {β : ℝ} (hβ : 0 ≤ β) (E mhi S X : Ω → ℝ)
    (hS : ∀ ω, S ω ≤ mhi ω - E ω) (hX : ∀ ω, 0 ≤ X ω) {u : ℝ} (hu : Real.log (Z β E) ≤ u) :
    Real.exp (Real.log (Z β mhi) - u) * avg β mhi (fun ω => X ω * Real.exp (β * S ω)) ≤
      avg β E X := by
  have hZE := Z_pos β E
  have hZhi := Z_pos β mhi
  have hnum : ∑ ω, X ω * Real.exp (β * S ω) * Real.exp (-β * mhi ω) ≤
      ∑ ω, X ω * Real.exp (-β * E ω) := by
    refine Finset.sum_le_sum fun ω _ => ?_
    rw [mul_assoc, ← Real.exp_add]
    refine mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr ?_) (hX ω)
    linarith [mul_le_mul_of_nonneg_left (hS ω) hβ]
  have hA : 0 ≤ avg β mhi (fun ω => X ω * Real.exp (β * S ω)) :=
    avg_nonneg β mhi fun ω => mul_nonneg (hX ω) (Real.exp_pos _).le
  have hexp : Real.exp (Real.log (Z β mhi) - u) ≤ Z β mhi / Z β E := by
    rw [Real.exp_sub, Real.exp_log hZhi]
    refine div_le_div_of_nonneg_left hZhi.le hZE ?_
    calc Z β E = Real.exp (Real.log (Z β E)) := (Real.exp_log hZE).symm
      _ ≤ Real.exp u := Real.exp_le_exp.mpr hu
  calc Real.exp (Real.log (Z β mhi) - u) * avg β mhi (fun ω => X ω * Real.exp (β * S ω))
      ≤ Z β mhi / Z β E * avg β mhi (fun ω => X ω * Real.exp (β * S ω)) :=
        mul_le_mul_of_nonneg_right hexp hA
    _ = (∑ ω, X ω * Real.exp (β * S ω) * Real.exp (-β * mhi ω)) / Z β E := by
        unfold avg
        rw [div_mul_div_comm, mul_comm (Z β mhi), mul_div_mul_right _ _ hZhi.ne']
    _ ≤ avg β E X := div_le_div_of_nonneg_right hnum hZE.le

omit [Fintype Ω] in
/-- Each slack function is at most the gap: `Sp g ≤ ∑ g', Sp g' ≤ mhi - E`. -/
theorem slack_le_gap {G : Type*} [Fintype G] (E mhi : Ω → ℝ) (Sp : G → Ω → ℝ)
    (hSp0 : ∀ g ω, 0 ≤ Sp g ω) (hSp : ∀ ω, ∑ g, Sp g ω ≤ mhi ω - E ω) (g : G) (ω : Ω) :
    Sp g ω ≤ mhi ω - E ω :=
  (Finset.single_le_sum (fun g' _ => hSp0 g' ω) (Finset.mem_univ g)).trans (hSp ω)

/-! ### The two upper bounds -/

/-- **(UE) Upper bound, Jensen form.**  Let the non-negative slack functions `Sp g` add up to at
most `mhi - E` and the non-negative slack functions `Sm g` to at most `E - mlo`.  If `u` is an
upper bound of `log (Z E)`, then

`log (Z E) ≤ log (Z mlo) - β * (∑ g, avg β mhi (Sm g * exp (β * Sp g))) * exp (log (Z mhi) - u)`.

Proof: (LJ) for the pair `mlo ≤ E` gives `log (Z E) ≤ log (Z mlo) - β * ∑ g, avg β E (Sm g)`, and
`avg β E (Sm g) ≥ exp (log (Z mhi) - u) * avg β mhi (Sm g * exp (β * Sp g))` by
`avg_ceiling_le_avg_true`. -/
theorem upper_jensen [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo E mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSp0 : ∀ g ω, 0 ≤ Sp g ω)
    (hSm0 : ∀ g ω, 0 ≤ Sm g ω) (hSp : ∀ ω, ∑ g, Sp g ω ≤ mhi ω - E ω)
    (hSm : ∀ ω, ∑ g, Sm g ω ≤ E ω - mlo ω) {u : ℝ} (hu : Real.log (Z β E) ≤ u) :
    Real.log (Z β E) ≤ Real.log (Z β mlo) -
      β * (∑ g, avg β mhi (fun ω => Sm g ω * Real.exp (β * Sp g ω))) *
        Real.exp (Real.log (Z β mhi) - u) := by
  have h1 := lower_jensen hβ mlo E Sm hSm
  have h2 : (∑ g, avg β mhi (fun ω => Sm g ω * Real.exp (β * Sp g ω))) *
      Real.exp (Real.log (Z β mhi) - u) ≤ ∑ g, avg β E (Sm g) := by
    rw [Finset.sum_mul]
    refine Finset.sum_le_sum fun g _ => ?_
    rw [mul_comm]
    exact avg_ceiling_le_avg_true hβ E mhi (Sp g) (Sm g) (slack_le_gap E mhi Sp hSp0 hSp g)
      (hSm0 g) hu
  have h3 := mul_le_mul_of_nonneg_left h2 hβ
  rw [← mul_assoc] at h3
  linarith

/-- **(UP) Upper bound, product form.**  Under the hypotheses of `upper_jensen`, if `u` is an
upper bound of `log (Z E)`, then

`log (Z E) ≤ log (Z mlo) -
  log (1 + (∑ g, avg β mhi ((exp (β * Sm g) - 1) * exp (β * Sp g))) * exp (log (Z mhi) - u))`.

Proof: the product bound for the pair `mlo ≤ E` gives
`1 + ∑ g, avg β E (exp (β * Sm g) - 1) ≤ Z mlo / Z E`, and the means under the true ensemble are
bounded from below by `avg_ceiling_le_avg_true`. -/
theorem upper_product [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo E mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSp0 : ∀ g ω, 0 ≤ Sp g ω)
    (hSm0 : ∀ g ω, 0 ≤ Sm g ω) (hSp : ∀ ω, ∑ g, Sp g ω ≤ mhi ω - E ω)
    (hSm : ∀ ω, ∑ g, Sm g ω ≤ E ω - mlo ω) {u : ℝ} (hu : Real.log (Z β E) ≤ u) :
    Real.log (Z β E) ≤ Real.log (Z β mlo) -
      Real.log (1 + (∑ g, avg β mhi
        (fun ω => (Real.exp (β * Sm g ω) - 1) * Real.exp (β * Sp g ω))) *
          Real.exp (Real.log (Z β mhi) - u)) := by
  have hX : ∀ g ω, 0 ≤ Real.exp (β * Sm g ω) - 1 := fun g ω =>
    sub_nonneg.mpr (Real.one_le_exp (mul_nonneg hβ (hSm0 g ω)))
  have h1 := one_add_slack_le_Z_div hβ E mlo Sm hSm0 hSm
  have h2 : (∑ g, avg β mhi (fun ω => (Real.exp (β * Sm g ω) - 1) * Real.exp (β * Sp g ω))) *
      Real.exp (Real.log (Z β mhi) - u) ≤
        ∑ g, avg β E (fun ω => Real.exp (β * Sm g ω) - 1) := by
    rw [Finset.sum_mul]
    refine Finset.sum_le_sum fun g _ => ?_
    rw [mul_comm]
    exact avg_ceiling_le_avg_true hβ E mhi (Sp g) (fun ω => Real.exp (β * Sm g ω) - 1)
      (slack_le_gap E mhi Sp hSp0 hSp g) (hX g) hu
  have hnn : 0 ≤ (∑ g, avg β mhi
      (fun ω => (Real.exp (β * Sm g ω) - 1) * Real.exp (β * Sp g ω))) *
        Real.exp (Real.log (Z β mhi) - u) :=
    mul_nonneg (Finset.sum_nonneg fun g _ => avg_nonneg β mhi fun ω =>
      mul_nonneg (hX g ω) (Real.exp_pos _).le) (Real.exp_pos _).le
  have h3 := Real.log_le_log (by linarith) ((add_le_add le_rfl h2).trans h1)
  rw [Real.log_div (Z_pos β mlo).ne' (Z_pos β E).ne'] at h3
  linarith

/-! ### The iterations -/

/-- The floor model gives an upper bound: `log (Z E) ≤ log (Z mlo)`. -/
theorem log_Z_le_log_Z_floor [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo E : Ω → ℝ) (Sm : G → Ω → ℝ) (hSm0 : ∀ g ω, 0 ≤ Sm g ω)
    (hSm : ∀ ω, ∑ g, Sm g ω ≤ E ω - mlo ω) : Real.log (Z β E) ≤ Real.log (Z β mlo) := by
  have h := lower_jensen hβ mlo E Sm hSm
  have h2 : 0 ≤ β * ∑ g, avg β E (Sm g) :=
    mul_nonneg hβ (Finset.sum_nonneg fun g _ => avg_nonneg β E (hSm0 g))
  linarith

/-- The right-hand side of (UE) as a function of the upper bound `u`. -/
noncomputable def ueStep {G : Type*} [Fintype G] (β : ℝ) (mlo mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ)
    (u : ℝ) : ℝ :=
  Real.log (Z β mlo) -
    β * (∑ g, avg β mhi (fun ω => Sm g ω * Real.exp (β * Sp g ω))) *
      Real.exp (Real.log (Z β mhi) - u)

/-- The right-hand side of (UP) as a function of the upper bound `u`. -/
noncomputable def upStep {G : Type*} [Fintype G] (β : ℝ) (mlo mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ)
    (u : ℝ) : ℝ :=
  Real.log (Z β mlo) -
    Real.log (1 + (∑ g, avg β mhi
      (fun ω => (Real.exp (β * Sm g ω) - 1) * Real.exp (β * Sp g ω))) *
        Real.exp (Real.log (Z β mhi) - u))

/-- **Every sequence of (UE) and (UP) steps consists of upper bounds.**  If `u 0` is an upper
bound of `log (Z E)` and every `u (t + 1)` is the right-hand side of (UE) or of (UP) at `u t`,
then every `u t` is an upper bound of `log (Z E)`. -/
theorem log_Z_le_of_steps [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo E mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSp0 : ∀ g ω, 0 ≤ Sp g ω)
    (hSm0 : ∀ g ω, 0 ≤ Sm g ω) (hSp : ∀ ω, ∑ g, Sp g ω ≤ mhi ω - E ω)
    (hSm : ∀ ω, ∑ g, Sm g ω ≤ E ω - mlo ω) (u : ℕ → ℝ) (h0 : Real.log (Z β E) ≤ u 0)
    (hstep : ∀ t, u (t + 1) = ueStep β mlo mhi Sp Sm (u t) ∨
      u (t + 1) = upStep β mlo mhi Sp Sm (u t)) (t : ℕ) :
    Real.log (Z β E) ≤ u t := by
  induction t with
  | zero => exact h0
  | succ t ih =>
    rcases hstep t with h | h
    · rw [h]
      exact upper_jensen hβ mlo E mhi Sp Sm hSp0 hSm0 hSp hSm ih
    · rw [h]
      exact upper_product hβ mlo E mhi Sp Sm hSp0 hSm0 hSp hSm ih

/-- **The (UE) iteration.**  `u_0 = log (Z mlo)`, `u_{t+1} = ` the right-hand side of (UE) at
`u_t`: every `u_t` is an upper bound of `log (Z E)`. -/
theorem log_Z_le_ueStep_iterate [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo E mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSp0 : ∀ g ω, 0 ≤ Sp g ω)
    (hSm0 : ∀ g ω, 0 ≤ Sm g ω) (hSp : ∀ ω, ∑ g, Sp g ω ≤ mhi ω - E ω)
    (hSm : ∀ ω, ∑ g, Sm g ω ≤ E ω - mlo ω) (t : ℕ) :
    Real.log (Z β E) ≤ (ueStep β mlo mhi Sp Sm)^[t] (Real.log (Z β mlo)) :=
  log_Z_le_of_steps hβ mlo E mhi Sp Sm hSp0 hSm0 hSp hSm
    (fun t => (ueStep β mlo mhi Sp Sm)^[t] (Real.log (Z β mlo)))
    (log_Z_le_log_Z_floor hβ mlo E Sm hSm0 hSm)
    (fun t => Or.inl (Function.iterate_succ_apply' _ t _)) t

/-- **The (UP) iteration.**  `u_0 = log (Z mlo)`, `u_{t+1} = ` the right-hand side of (UP) at
`u_t`: every `u_t` is an upper bound of `log (Z E)`. -/
theorem log_Z_le_upStep_iterate [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo E mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSp0 : ∀ g ω, 0 ≤ Sp g ω)
    (hSm0 : ∀ g ω, 0 ≤ Sm g ω) (hSp : ∀ ω, ∑ g, Sp g ω ≤ mhi ω - E ω)
    (hSm : ∀ ω, ∑ g, Sm g ω ≤ E ω - mlo ω) (t : ℕ) :
    Real.log (Z β E) ≤ (upStep β mlo mhi Sp Sm)^[t] (Real.log (Z β mlo)) :=
  log_Z_le_of_steps hβ mlo E mhi Sp Sm hSp0 hSm0 hSp hSm
    (fun t => (upStep β mlo mhi Sp Sm)^[t] (Real.log (Z β mlo)))
    (log_Z_le_log_Z_floor hβ mlo E Sm hSm0 hSm)
    (fun t => Or.inr (Function.iterate_succ_apply' _ t _)) t

/-- The coefficient of (UE) is non-negative. -/
theorem ue_coeff_nonneg [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSm0 : ∀ g ω, 0 ≤ Sm g ω) :
    0 ≤ β * ∑ g, avg β mhi (fun ω => Sm g ω * Real.exp (β * Sp g ω)) :=
  mul_nonneg hβ (Finset.sum_nonneg fun g _ => avg_nonneg β mhi fun ω =>
    mul_nonneg (hSm0 g ω) (Real.exp_pos _).le)

/-- The coefficient of (UP) is non-negative. -/
theorem up_coeff_nonneg [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSm0 : ∀ g ω, 0 ≤ Sm g ω) :
    0 ≤ ∑ g, avg β mhi (fun ω => (Real.exp (β * Sm g ω) - 1) * Real.exp (β * Sp g ω)) :=
  Finset.sum_nonneg fun g _ => avg_nonneg β mhi fun ω =>
    mul_nonneg (sub_nonneg.mpr (Real.one_le_exp (mul_nonneg hβ (hSm0 g ω)))) (Real.exp_pos _).le

/-- The (UE) step is monotone: a smaller upper bound `u` gives a smaller right-hand side. -/
theorem ueStep_mono [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSm0 : ∀ g ω, 0 ≤ Sm g ω) :
    Monotone (ueStep β mlo mhi Sp Sm) := by
  intro u v huv
  have he : Real.exp (Real.log (Z β mhi) - v) ≤ Real.exp (Real.log (Z β mhi) - u) :=
    Real.exp_le_exp.mpr (by linarith)
  have h := mul_le_mul_of_nonneg_left he (ue_coeff_nonneg hβ mhi Sp Sm hSm0)
  unfold ueStep
  linarith

/-- The (UP) step is monotone: a smaller upper bound `u` gives a smaller right-hand side. -/
theorem upStep_mono [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSm0 : ∀ g ω, 0 ≤ Sm g ω) :
    Monotone (upStep β mlo mhi Sp Sm) := by
  intro u v huv
  have hB := up_coeff_nonneg hβ mhi Sp Sm hSm0
  have he : Real.exp (Real.log (Z β mhi) - v) ≤ Real.exp (Real.log (Z β mhi) - u) :=
    Real.exp_le_exp.mpr (by linarith)
  have h := mul_le_mul_of_nonneg_left he hB
  have hpos : 0 < 1 + (∑ g, avg β mhi
      (fun ω => (Real.exp (β * Sm g ω) - 1) * Real.exp (β * Sp g ω))) *
        Real.exp (Real.log (Z β mhi) - v) := by
    have := mul_nonneg hB (Real.exp_pos (Real.log (Z β mhi) - v)).le
    linarith
  have hlog := Real.log_le_log hpos (add_le_add le_rfl h)
  unfold upStep
  linarith

/-- The (UE) iteration from `log (Z mlo)` does not increase. -/
theorem ueStep_iterate_antitone [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSm0 : ∀ g ω, 0 ≤ Sm g ω) :
    Antitone fun t => (ueStep β mlo mhi Sp Sm)^[t] (Real.log (Z β mlo)) := by
  refine (ueStep_mono hβ mlo mhi Sp Sm hSm0).antitone_iterate_of_map_le ?_
  have h := mul_nonneg (ue_coeff_nonneg hβ mhi Sp Sm hSm0)
    (Real.exp_pos (Real.log (Z β mhi) - Real.log (Z β mlo))).le
  unfold ueStep
  linarith

/-- The (UP) iteration from `log (Z mlo)` does not increase. -/
theorem upStep_iterate_antitone [Nonempty Ω] {G : Type*} [Fintype G] {β : ℝ} (hβ : 0 ≤ β)
    (mlo mhi : Ω → ℝ) (Sp Sm : G → Ω → ℝ) (hSm0 : ∀ g ω, 0 ≤ Sm g ω) :
    Antitone fun t => (upStep β mlo mhi Sp Sm)^[t] (Real.log (Z β mlo)) := by
  refine (upStep_mono hβ mlo mhi Sp Sm hSm0).antitone_iterate_of_map_le ?_
  have h := mul_nonneg (up_coeff_nonneg hβ mhi Sp Sm hSm0)
    (Real.exp_pos (Real.log (Z β mhi) - Real.log (Z β mlo))).le
  have hlog := Real.log_nonneg (by linarith : (1 : ℝ) ≤ 1 + (∑ g, avg β mhi
      (fun ω => (Real.exp (β * Sm g ω) - 1) * Real.exp (β * Sp g ω))) *
        Real.exp (Real.log (Z β mhi) - Real.log (Z β mlo)))
  unfold upStep
  linarith

end MetricChain.GibbsRecovery
