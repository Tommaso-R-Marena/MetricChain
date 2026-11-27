import Mathlib
import proofs.Core.Basic
import proofs.Frontiers.EnvelopeDuality
import proofs.Frontiers.CertificationGeometry
import proofs.Frontiers.FreeEnergySandwich
import proofs.Frontiers.EnsembleDivergence
import proofs.Frontiers.ConditionalEnvelope

/-!
# Thermal robustness: the envelope theorems at finite temperature

Setting of `EnvelopeDuality.lean`: an energy `E = f + g` on a finite configuration space, with a
known part `f` and a residual `g` that is only known to be admissible for an envelope `d`
(`g x - g y ≤ d x y`).  At zero temperature, the question "can `x` be optimal?" is answered by
the contact-set theorem (`robust_minimizer_iff`), and the question "is `x` certainly optimal?"
by the sharp-minimum theorem (`robust_certified_iff`).  This file gives the finite-temperature
versions, in which optimality is replaced by the Gibbs probability
`gibbsProb β E x = exp (-β E x) / ∑ y, exp (-β E y)`.

## The exact range of a Gibbs probability

For every `β ≥ 0` and every admissible residual `g`

  `1 / ∑ y, exp (-β (f y - f x - d x y)) ≤ gibbsProb β (f + g) x`
  `gibbsProb β (f + g) x ≤ 1 / ∑ y, exp (-β (f y - f x + d y x))`

(`gibbsProb_ge_sharp`, `gibbsProb_le_contact`).  Both bounds are attained, at every temperature,
by the same extremal residuals as at zero temperature, `-d x ·` and `d · x`
(`gibbsProb_sharp_attained`, `gibbsProb_contact_attained`), and every value in between is
attained (`gibbsProb_range_exact`): over the envelope class, the set of Gibbs probabilities of
`x` is exactly this interval (`gibbsProb_range_eq`).  The zero-temperature shadows of the two
bounds are the contact-set and the sharp-minimum criteria:

* `gibbsProb_le_exp_of_contact_violation` — a configuration that violates the contact condition
  by a margin `δ` has Gibbs probability at most `exp (-β δ)` for every admissible residual;
* `gibbsProb_ge_of_sharp` — a `δ`-sharp minimum of `f` has Gibbs probability at least
  `1 / (1 + (|X| - 1) exp (-β δ))` for every admissible residual.

After evaluations of the residual on a set of anchors, the same statements hold with `d`
replaced by the conditional envelope of `ConditionalEnvelope.lean`
(`gibbsProb_range_with_anchors_eq`): Gibbs probabilities do not see the additive constant of the
residual, so conditioning is exactly the update of the envelope.

## The envelope class in Boltzmann weights

`admissible_iff_weights` — in the Boltzmann weights `w = exp (-β g)` the envelope class is the
polyhedral cone `w y ≤ exp (β d x y) · w x`.

## Finite-temperature certificates

Let `g` be evaluated on the anchors `A`.  The partition function `Z` of `f + g` is bracketed by
the partition functions `Zlo ≤ Z ≤ Zhi` of `f` plus the upper and the lower McShane envelope
(`robust_partition_bracket`).  In terms of the slack quasi-metric of `CertificationGeometry.lean`

* `Zhi_eq`, `Zlo_eq` — `Zhi = ∑ y, exp (-β E y) · exp (β s(A, y))` and
  `Zlo = ∑ y, exp (-β E y) · exp (-β s(y, A))`;
* `mean_slack_le` — (Jensen) if `Zhi ≤ exp ε · Z` then the Gibbs average of the slack distance
  from the evaluated set satisfies `β ⟨s(A, ·)⟩ ≤ ε`;
* `card_ge_laplace` — (Cauchy–Schwarz) under the same hypothesis `exp (-ε) ≤ |A| · B`, where `B`
  bounds the Gibbs average of `exp (-β · slack a ·)` for every evaluated point `a`: the number of
  evaluations is at least `exp (-ε)` divided by the Gibbs weight of a (soft) slack ball.

`Zhi_le_of_bracket` derives the hypothesis `Zhi ≤ exp ε · Z` from the computable certificate
`Zhi ≤ exp ε · Zlo`.

## Transport–entropy bound

For a reference probability vector `μ`, an admissible `g`, the tilted vector
`ν = expTilt μ g β ∝ μ · exp (β g)` and any coupling `γ` of `ν` and `μ`:

* `transport_le` — weak Kantorovich–Rubinstein duality: `E_ν g - E_μ g ≤ ∑ γ · d`;
* `logMGF_eq_tilt` — the Gibbs variational identity at its optimiser:
  `log E_μ exp (β (g - E_μ g)) = β (E_ν g - E_μ g) - KL(ν ‖ μ)`;
* `logMGF_le_transport_entropy` — hence `log E_μ exp (β (g - E_μ g)) ≤ β ∑ γ · d - KL(ν ‖ μ)`;
* `gap_le_of_T1` — if the cost of the coupling satisfies the transport–entropy inequality
  `(∑ γ · d)² ≤ 2 C · KL(ν ‖ μ)`, the Jensen gap of the free-energy sandwich is at most
  `β² C / 2` (the direction "`T₁` implies a sub-Gaussian moment generating function" of the
  Bobkov–Götze theorem, for a single tilted measure and a single coupling).
-/

namespace MetricChain

open Finset

variable {X : Type*}

/-! ### Gibbs probabilities -/

section Gibbs

variable [Fintype X]

/-- The Gibbs (Boltzmann) probability of the configuration `x` for the energy `E` at inverse
temperature `β`. -/
noncomputable def gibbsProb (β : ℝ) (E : X → ℝ) (x : X) : ℝ :=
  Real.exp (-β * E x) / ∑ y, Real.exp (-β * E y)

/-- Gibbs probabilities are nonnegative. -/
theorem gibbsProb_nonneg (β : ℝ) (E : X → ℝ) (x : X) : 0 ≤ gibbsProb β E x :=
  gibbs_weight_nonneg E β x

/-- Gibbs probabilities sum to one. -/
theorem sum_gibbsProb [Nonempty X] (β : ℝ) (E : X → ℝ) : ∑ x, gibbsProb β E x = 1 :=
  gibbs_weight_sum_one E β

/-- The Gibbs probability of `x` only depends on the energy differences to `x`:
`gibbsProb β E x = 1 / ∑ y, exp (-β (E y - E x))`. -/
theorem gibbsProb_eq_one_div (β : ℝ) (E : X → ℝ) (x : X) :
    gibbsProb β E x = 1 / ∑ y, Real.exp (-β * (E y - E x)) := by
  have hsum : ∑ y, Real.exp (-β * (E y - E x)) =
      Real.exp (β * E x) * ∑ y, Real.exp (-β * E y) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [← Real.exp_add]
    congr 1
    ring
  unfold gibbsProb
  rw [hsum, one_div, mul_inv, ← Real.exp_neg, div_eq_mul_inv, neg_mul]

/-- Gibbs probabilities do not change when a constant is added to the energy. -/
theorem gibbsProb_add_const (β : ℝ) (E : X → ℝ) (c : ℝ) (x : X) :
    gibbsProb β (fun y => E y + c) x = gibbsProb β E x := by
  rw [gibbsProb_eq_one_div, gibbsProb_eq_one_div]
  congr 1
  refine Finset.sum_congr rfl fun y _ => ?_
  show Real.exp (-β * (E y + c - (E x + c))) = _
  congr 1
  ring

/-! ### The exact range of a Gibbs probability over the envelope class -/

/-- **Finite-temperature contact bound.**  For every admissible residual and every `β ≥ 0`, the
Gibbs probability of `x` is at most `1 / ∑ y, exp (-β (f y - f x + d y x))`. -/
theorem gibbsProb_le_contact {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (f : X → ℝ)
    {β : ℝ} (hβ : 0 ≤ β) (x : X) :
    gibbsProb β (fun y => f y + g y) x ≤ 1 / ∑ y, Real.exp (-β * (f y - f x + d y x)) := by
  rw [gibbsProb_eq_one_div]
  apply one_div_le_one_div_of_le
  · exact Finset.sum_pos (fun _ _ => Real.exp_pos _) ⟨x, mem_univ x⟩
  · refine Finset.sum_le_sum fun y _ => Real.exp_le_exp.mpr ?_
    have h1 := mul_le_mul_of_nonneg_left (hg y x) hβ
    show -β * (f y - f x + d y x) ≤ -β * (f y + g y - (f x + g x))
    linarith

/-- **The contact bound is attained**, at every temperature, by the envelope itself: the residual
`g = d · x` is admissible and gives equality in `gibbsProb_le_contact`. -/
theorem gibbsProb_contact_attained {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (β : ℝ)
    (x : X) :
    Admissible d (fun y => d y x) ∧
      gibbsProb β (fun y => f y + d y x) x =
        1 / ∑ y, Real.exp (-β * (f y - f x + d y x)) := by
  refine ⟨fun y z => ?_, ?_⟩
  · have := hd.triangle y z x
    show d y x - d z x ≤ d y z
    linarith
  · rw [gibbsProb_eq_one_div]
    congr 1
    refine Finset.sum_congr rfl fun y _ => ?_
    show Real.exp (-β * (f y + d y x - (f x + d x x))) = _
    rw [hd.self x]
    congr 1
    ring

/-- **Finite-temperature sharp-minimum bound.**  For every admissible residual and every `β ≥ 0`,
the Gibbs probability of `x` is at least `1 / ∑ y, exp (-β (f y - f x - d x y))`. -/
theorem gibbsProb_ge_sharp {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (f : X → ℝ)
    {β : ℝ} (hβ : 0 ≤ β) (x : X) :
    1 / ∑ y, Real.exp (-β * (f y - f x - d x y)) ≤ gibbsProb β (fun y => f y + g y) x := by
  rw [gibbsProb_eq_one_div]
  apply one_div_le_one_div_of_le
  · exact Finset.sum_pos (fun _ _ => Real.exp_pos _) ⟨x, mem_univ x⟩
  · refine Finset.sum_le_sum fun y _ => Real.exp_le_exp.mpr ?_
    have h1 := mul_le_mul_of_nonneg_left (hg x y) hβ
    show -β * (f y + g y - (f x + g x)) ≤ -β * (f y - f x - d x y)
    linarith

/-- **The sharp-minimum bound is attained**, at every temperature, by the residual `g = -d x ·`:
it is admissible and gives equality in `gibbsProb_ge_sharp`. -/
theorem gibbsProb_sharp_attained {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (β : ℝ)
    (x : X) :
    Admissible d (fun y => -d x y) ∧
      gibbsProb β (fun y => f y + -d x y) x =
        1 / ∑ y, Real.exp (-β * (f y - f x - d x y)) := by
  refine ⟨fun y z => ?_, ?_⟩
  · have := hd.triangle x y z
    show -d x y - -d x z ≤ d y z
    linarith
  · rw [gibbsProb_eq_one_div]
    congr 1
    refine Finset.sum_congr rfl fun y _ => ?_
    show Real.exp (-β * (f y + -d x y - (f x + -d x x))) = _
    rw [hd.self x]
    congr 1
    ring

/-- **Every intermediate value is attained.**  For an envelope `d`, every number between the
sharp-minimum bound and the contact bound is the Gibbs probability of `x` for some admissible
residual (a convex combination of the two extremal residuals). -/
theorem gibbsProb_range_exact {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (β : ℝ) (x : X)
    (τ : ℝ)
    (hτ : τ ∈ Set.Icc (1 / ∑ y, Real.exp (-β * (f y - f x - d x y)))
      (1 / ∑ y, Real.exp (-β * (f y - f x + d y x)))) :
    ∃ g, Admissible d g ∧ gibbsProb β (fun y => f y + g y) x = τ := by
  obtain ⟨hlo, elo⟩ := gibbsProb_sharp_attained hd f β x
  obtain ⟨hhi, ehi⟩ := gibbsProb_contact_attained hd f β x
  let F : ℝ → ℝ := fun t => gibbsProb β (fun y => f y + ((1 - t) * -d x y + t * d y x)) x
  have hcont : Continuous F := by
    show Continuous fun t => gibbsProb β (fun y => f y + ((1 - t) * -d x y + t * d y x)) x
    unfold gibbsProb
    refine Continuous.div (by fun_prop) (by fun_prop) fun t => ?_
    exact (Finset.sum_pos (fun _ _ => Real.exp_pos _) ⟨x, mem_univ x⟩).ne'
  have h0 : F 0 = 1 / ∑ y, Real.exp (-β * (f y - f x - d x y)) := by
    rw [← elo]
    show gibbsProb β (fun y => f y + ((1 - 0) * -d x y + 0 * d y x)) x = _
    congr 1
    funext y
    ring
  have h1 : F 1 = 1 / ∑ y, Real.exp (-β * (f y - f x + d y x)) := by
    rw [← ehi]
    show gibbsProb β (fun y => f y + ((1 - 1) * -d x y + 1 * d y x)) x = _
    congr 1
    funext y
    ring
  have hmem : τ ∈ Set.Icc (F 0) (F 1) := by rw [h0, h1]; exact hτ
  obtain ⟨t, ht, hFt⟩ := intermediate_value_Icc (zero_le_one' ℝ) hcont.continuousOn hmem
  exact ⟨_, hlo.convex hhi ht.1 ht.2, hFt⟩

/-- **The exact range of a Gibbs probability over the envelope class.**  For an envelope `d` and
`β ≥ 0`, the set of values of the Gibbs probability of `x` over all admissible residuals is the
interval between the sharp-minimum bound and the contact bound. -/
theorem gibbsProb_range_eq {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) {β : ℝ}
    (hβ : 0 ≤ β) (x : X) :
    {p | ∃ g, Admissible d g ∧ gibbsProb β (fun y => f y + g y) x = p} =
      Set.Icc (1 / ∑ y, Real.exp (-β * (f y - f x - d x y)))
        (1 / ∑ y, Real.exp (-β * (f y - f x + d y x))) := by
  ext p
  constructor
  · rintro ⟨g, hg, rfl⟩
    exact ⟨gibbsProb_ge_sharp hg f hβ x, gibbsProb_le_contact hg f hβ x⟩
  · exact fun hp => gibbsProb_range_exact hd f β x p hp

/-! ### Zero-temperature shadows: thermal pruning and thermal certification -/

/-- **Thermal pruning.**  If `x` violates the contact condition by a margin `δ` (some `y` has
`f y + d y x + δ ≤ f x`), then for every admissible residual and every `β ≥ 0` the Gibbs
probability of `x` is at most `exp (-β δ)`.  For `δ > 0` the zero-temperature limit is the
"only if" part of `robust_minimizer_iff`: such an `x` is never optimal. -/
theorem gibbsProb_le_exp_of_contact_violation {d : X → X → ℝ} {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) {β : ℝ} (hβ : 0 ≤ β) {x y : X} {δ : ℝ}
    (hy : f y + d y x + δ ≤ f x) :
    gibbsProb β (fun z => f z + g z) x ≤ Real.exp (-β * δ) := by
  refine (gibbsProb_le_contact hg f hβ x).trans ?_
  have h1 : Real.exp (β * δ) ≤ Real.exp (-β * (f y - f x + d y x)) := by
    apply Real.exp_le_exp.mpr
    nlinarith [mul_le_mul_of_nonneg_left hy hβ]
  have h2 : Real.exp (-β * (f y - f x + d y x)) ≤
      ∑ z, Real.exp (-β * (f z - f x + d z x)) :=
    Finset.single_le_sum (f := fun z => Real.exp (-β * (f z - f x + d z x)))
      (fun z _ => (Real.exp_pos _).le) (mem_univ y)
  have h3 := one_div_le_one_div_of_le (Real.exp_pos (β * δ)) (h1.trans h2)
  rwa [one_div (Real.exp (β * δ)), ← Real.exp_neg, ← neg_mul] at h3

/-- **Thermal certification.**  If `x` is a `δ`-sharp minimum of `f` for the envelope
(`d x y + δ ≤ f y - f x` for all `y ≠ x`), then for every admissible residual and every `β ≥ 0`
the Gibbs probability of `x` is at least `1 / (1 + (|X| - 1) exp (-β δ))`.  For `δ > 0` the
zero-temperature limit is the "if" part of `robust_certified_iff`: the Gibbs measure concentrates
on `x`, uniformly over the envelope class. -/
theorem gibbsProb_ge_of_sharp {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) {β : ℝ} (hβ : 0 ≤ β) (x : X) {δ : ℝ}
    (hδ : ∀ y, y ≠ x → d x y + δ ≤ f y - f x) :
    1 / (1 + (Fintype.card X - 1 : ℝ) * Real.exp (-β * δ)) ≤
      gibbsProb β (fun y => f y + g y) x := by
  classical
  refine le_trans ?_ (gibbsProb_ge_sharp hg f hβ x)
  apply one_div_le_one_div_of_le
  · exact Finset.sum_pos (fun _ _ => Real.exp_pos _) ⟨x, mem_univ x⟩
  · rw [← Finset.add_sum_erase univ _ (mem_univ x)]
    have hx : Real.exp (-β * (f x - f x - d x x)) = 1 := by
      rw [hd.self x, sub_self, sub_zero, mul_zero, Real.exp_zero]
    rw [hx]
    have hrest : ∑ y ∈ univ.erase x, Real.exp (-β * (f y - f x - d x y)) ≤
        ((univ.erase x).card : ℝ) * Real.exp (-β * δ) := by
      rw [← nsmul_eq_mul]
      apply Finset.sum_le_card_nsmul
      intro y hy
      apply Real.exp_le_exp.mpr
      have h1 := hδ y (Finset.ne_of_mem_erase hy)
      nlinarith [mul_le_mul_of_nonneg_left h1 hβ]
    rw [Finset.cast_card_erase_of_mem (mem_univ x), Finset.card_univ] at hrest
    linarith

/-! ### With evaluations: the same range for the conditional envelope -/

/-- **The exact range of a Gibbs probability given evaluations.**  For consistent evaluations
`v` on the anchors `A` and `β ≥ 0`, the set of values of the Gibbs probability of `x` over all
admissible residuals that agree with the evaluations is the interval of `gibbsProb_range_eq` for
the *conditional* envelope.  (Gibbs probabilities are invariant under adding a constant to the
residual, and up to a constant the consistent residuals are the residuals admissible for the
conditional envelope: `admissible_condEnv`, `exists_consistent_shift`.) -/
theorem gibbsProb_range_with_anchors_eq {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (f : X → ℝ)
    {β : ℝ} (hβ : 0 ≤ β) (x : X) :
    {p | ∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧
        gibbsProb β (fun y => f y + g y) x = p} =
      Set.Icc (1 / ∑ y, Real.exp (-β * (f y - f x - condEnv d A hA v x y)))
        (1 / ∑ y, Real.exp (-β * (f y - f x + condEnv d A hA v y x))) := by
  ext p
  constructor
  · rintro ⟨g, hg, hgv, rfl⟩
    have hc := admissible_condEnv hg A hA v hgv
    exact ⟨gibbsProb_ge_sharp hc f hβ x, gibbsProb_le_contact hc f hβ x⟩
  · intro hp
    obtain ⟨g, hg, rfl⟩ := gibbsProb_range_exact (condEnv_isEnvelope hd A hA v hv) f β x p hp
    obtain ⟨c, hadm, hval⟩ := exists_consistent_shift hd A hA v hv hg
    refine ⟨fun z => g z + c, hadm, hval, ?_⟩
    have e : (fun y => f y + (g y + c)) = fun y => (f y + g y) + c := by
      funext y
      ring
    show gibbsProb β (fun y => f y + (g y + c)) x = _
    rw [e, gibbsProb_add_const]

end Gibbs

/-! ### The envelope class in Boltzmann weights -/

/-- **The envelope class is a polyhedral cone in the Boltzmann weights.**  For `β > 0`, a
residual is admissible iff its Boltzmann weights `w = exp (-β g)` satisfy the homogeneous linear
inequalities `w y ≤ exp (β d x y) · w x`. -/
theorem admissible_iff_weights {d : X → X → ℝ} {g : X → ℝ} {β : ℝ} (hβ : 0 < β) :
    Admissible d g ↔
      ∀ x y, Real.exp (-β * g y) ≤ Real.exp (β * d x y) * Real.exp (-β * g x) := by
  unfold Admissible
  refine forall_congr' fun x => forall_congr' fun y => ?_
  rw [← Real.exp_add, Real.exp_le_exp]
  constructor
  · intro h
    have := mul_le_mul_of_nonneg_left h hβ.le
    linarith
  · intro h
    have h' : β * (g x - g y) ≤ β * d x y := by linarith
    exact le_of_mul_le_mul_left h' hβ

/-! ### Finite-temperature certificates -/

section Certificates

variable [Fintype X]

/-- **The optimistic partition function in slack form.**  The partition function of `f` plus the
lower McShane envelope is the true partition function reweighted by `exp (β · s(A, y))`, where
`s(A, y)` is the slack distance from the evaluated set. -/
theorem Zhi_eq (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty) (β : ℝ) :
    ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) =
      ∑ y, Real.exp (-β * (f y + g y)) * Real.exp (β * slackFrom d g A hA y) := by
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [lowerEnv_eq_sub_slack, ← Real.exp_add]
  congr 1
  ring

/-- **The pessimistic partition function in slack form.**  The partition function of `f` plus the
upper McShane envelope is the true partition function reweighted by `exp (-β · s(y, A))`, where
`s(y, A)` is the slack distance to the evaluated set. -/
theorem Zlo_eq (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty) (β : ℝ) :
    ∑ y, Real.exp (-β * (f y + upperEnv d A hA g y)) =
      ∑ y, Real.exp (-β * (f y + g y)) * Real.exp (-β * slackTo d g A hA y) := by
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [upperEnv_eq_add_slack, ← Real.exp_add]
  congr 1
  ring

/-- **From a computable certificate to the hypothesis of `mean_slack_le` and `card_ge_laplace`.**
The two envelope partition functions only involve the evaluations of `g` on `A`.  If they agree
up to the factor `exp ε` then, for an admissible residual and `β ≥ 0`, the optimistic one is
within the factor `exp ε` of the true partition function (`robust_partition_bracket`). -/
theorem Zhi_le_of_bracket {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (f : X → ℝ)
    (A : Finset X) (hA : A.Nonempty) {β ε : ℝ} (hβ : 0 ≤ β)
    (h : ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + upperEnv d A hA g y))) :
    ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + g y)) := by
  have hb : ∑ y, Real.exp (-β * (f y + upperEnv d A hA g y)) ≤
      ∑ y, Real.exp (-β * (f y + g y)) :=
    (robust_partition_bracket hg A hA g (fun _ _ => rfl) f univ hβ).1
  exact h.trans (mul_le_mul_of_nonneg_left hb (Real.exp_pos _).le)

/-- A free-energy certificate bounds the exponential moment of the slack: if the optimistic
partition function is within the factor `exp ε` of the true one, then the Gibbs average of
`exp (β · s(A, ·))` is at most `exp ε`. -/
theorem mean_exp_slack_le (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    {β ε : ℝ}
    (hcert : ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + g y))) :
    ∑ y, gibbsProb β (fun y => f y + g y) y * Real.exp (β * slackFrom d g A hA y) ≤
      Real.exp ε := by
  have hZ : 0 < ∑ y, Real.exp (-β * (f y + g y)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) (hA.mono (subset_univ A))
  rw [Zhi_eq] at hcert
  have e : ∑ y, gibbsProb β (fun y => f y + g y) y * Real.exp (β * slackFrom d g A hA y) =
      (∑ y, Real.exp (-β * (f y + g y)) * Real.exp (β * slackFrom d g A hA y)) /
        ∑ y, Real.exp (-β * (f y + g y)) := by
    rw [Finset.sum_div]
    refine Finset.sum_congr rfl fun y _ => ?_
    show Real.exp (-β * (f y + g y)) / (∑ z, Real.exp (-β * (f z + g z))) *
      Real.exp (β * slackFrom d g A hA y) = _
    ring
  rw [e, div_le_iff₀ hZ]
  exact hcert

/-- **Mean slack of a free-energy certificate (Jensen).**  If the optimistic partition function
is within the factor `exp ε` of the true one, then `β` times the Gibbs average of the slack
distance from the evaluated set is at most `ε`: for `β > 0`, the evaluated set is within mean
slack distance `ε / β` of the Gibbs ensemble.  (The inequality holds for every real `β` and every
`g`; admissibility of `g` and `β ≥ 0` are what make the hypothesis checkable from the evaluations,
see `Zhi_le_of_bracket`.) -/
theorem mean_slack_le (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty) {β ε : ℝ}
    (hcert : ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + g y))) :
    β * ∑ y, gibbsProb β (fun y => f y + g y) y * slackFrom d g A hA y ≤ ε := by
  haveI : Nonempty X := hA.to_type
  have h1 := mean_exp_slack_le d f g A hA hcert
  have hJ := jensen_exp_weighted (gibbsProb β fun y => f y + g y)
    (fun y => β * slackFrom d g A hA y) (gibbsProb_nonneg β _) (sum_gibbsProb β _)
  have h2 := Real.exp_le_exp.mp (hJ.trans h1)
  calc β * ∑ y, gibbsProb β (fun y => f y + g y) y * slackFrom d g A hA y
      = ∑ y, gibbsProb β (fun y => f y + g y) y * (β * slackFrom d g A hA y) := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun y _ => by ring
    _ ≤ ε := h2

/-- **Covering bound at finite temperature (Cauchy–Schwarz form).**  If the optimistic partition
function is within the factor `exp ε` of the true one and `B` bounds the Gibbs average of
`exp (-β · slack a ·)` for every evaluated point `a`, then `exp (-ε) ≤ |A| · B`: the number of
evaluations is at least `exp (-ε) / B`.

Proof: by Cauchy–Schwarz `1 = (∑ π)² ≤ (∑ π e^{β s}) (∑ π e^{-β s})` with `s = s(A, ·)`; the
first factor is at most `exp ε` (`mean_exp_slack_le`), and `e^{-β s(A, y)}` is one of the terms
of `∑ a ∈ A, e^{-β · slack a y}`. -/
theorem card_ge_laplace (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    {β ε B : ℝ}
    (hcert : ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + g y)))
    (hB : ∀ a ∈ A, ∑ y, gibbsProb β (fun y => f y + g y) y * Real.exp (-β * slack d g a y) ≤ B) :
    Real.exp (-ε) ≤ A.card * B := by
  haveI : Nonempty X := hA.to_type
  have hP := mean_exp_slack_le d f g A hA hcert
  have hπ := gibbsProb_nonneg β (fun y => f y + g y)
  have hQ0 : 0 ≤ ∑ y, gibbsProb β (fun y => f y + g y) y *
      Real.exp (-β * slackFrom d g A hA y) :=
    Finset.sum_nonneg fun y _ => mul_nonneg (hπ y) (Real.exp_pos _).le
  -- Cauchy–Schwarz: `1 = (∑ π)² ≤ (∑ π e^{βs}) (∑ π e^{-βs})`
  have hCS : (∑ y, gibbsProb β (fun y => f y + g y) y) ^ 2 ≤
      (∑ y, gibbsProb β (fun y => f y + g y) y * Real.exp (β * slackFrom d g A hA y)) *
        ∑ y, gibbsProb β (fun y => f y + g y) y * Real.exp (-β * slackFrom d g A hA y) := by
    apply Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul
    · exact fun y _ => mul_nonneg (hπ y) (Real.exp_pos _).le
    · exact fun y _ => mul_nonneg (hπ y) (Real.exp_pos _).le
    · intro y _
      have h1 : Real.exp (β * slackFrom d g A hA y) * Real.exp (-β * slackFrom d g A hA y) = 1 := by
        rw [← Real.exp_add, ← Real.exp_zero]
        congr 1
        ring
      rw [mul_mul_mul_comm, h1, mul_one, sq]
  rw [sum_gibbsProb, one_pow] at hCS
  -- the second factor is at most `|A| · B`
  have hQ : ∑ y, gibbsProb β (fun y => f y + g y) y * Real.exp (-β * slackFrom d g A hA y) ≤
      A.card * B := by
    calc ∑ y, gibbsProb β (fun y => f y + g y) y * Real.exp (-β * slackFrom d g A hA y)
        ≤ ∑ y, ∑ a ∈ A, gibbsProb β (fun y => f y + g y) y *
            Real.exp (-β * slack d g a y) := by
          refine Finset.sum_le_sum fun y _ => ?_
          obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g a y)
          have hs : slackFrom d g A hA y = slack d g a y := hmin
          rw [hs]
          exact Finset.single_le_sum
            (f := fun a => gibbsProb β (fun y => f y + g y) y * Real.exp (-β * slack d g a y))
            (fun a _ => mul_nonneg (hπ y) (Real.exp_pos _).le) ha
      _ = ∑ a ∈ A, ∑ y, gibbsProb β (fun y => f y + g y) y *
            Real.exp (-β * slack d g a y) := Finset.sum_comm
      _ ≤ ∑ _a ∈ A, B := Finset.sum_le_sum hB
      _ = A.card * B := by rw [Finset.sum_const, nsmul_eq_mul]
  have h1 : 1 ≤ Real.exp ε * (A.card * B) :=
    hCS.trans ((mul_le_mul_of_nonneg_right hP hQ0).trans
      (mul_le_mul_of_nonneg_left hQ (Real.exp_pos _).le))
  rw [Real.exp_neg, inv_le_iff_one_le_mul₀' (Real.exp_pos ε)]
  exact h1

end Certificates

/-! ### Transport–entropy upper bound -/

section Transport

variable [Fintype X]

/-- **Weak Kantorovich–Rubinstein duality.**  For an admissible `g` and any coupling `γ ≥ 0` with
row sums `ν` and column sums `μ`, the difference of the two means of `g` is at most the transport
cost of the coupling for the envelope. -/
theorem transport_le {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (μ ν : X → ℝ)
    (γ : X → X → ℝ) (hγ : ∀ x y, 0 ≤ γ x y) (hrow : ∀ x, ∑ y, γ x y = ν x)
    (hcol : ∀ y, ∑ x, γ x y = μ y) :
    ∑ x, ν x * g x - ∑ y, μ y * g y ≤ ∑ x, ∑ y, γ x y * d x y := by
  have e1 : ∑ x, ν x * g x = ∑ x, ∑ y, γ x y * g x := by
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [← hrow x, Finset.sum_mul]
  have e2 : ∑ y, μ y * g y = ∑ x, ∑ y, γ x y * g y := by
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [← hcol y, Finset.sum_mul]
  rw [e1, e2, ← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum fun x _ => ?_
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum fun y _ => ?_
  have := mul_le_mul_of_nonneg_left (hg x y) (hγ x y)
  linarith

/-- The exponentially tilted weights `ν x = μ x · exp (β g x) / ∑ y, μ y · exp (β g y)`. -/
noncomputable def expTilt (μ g : X → ℝ) (β : ℝ) (x : X) : ℝ :=
  μ x * Real.exp (β * g x) / ∑ y, μ y * Real.exp (β * g y)

/-- The exponential tilt is the `tilt` of `EnsembleDivergence.lean` at inverse temperature `-β`. -/
theorem expTilt_eq_tilt (μ g : X → ℝ) (β : ℝ) : expTilt μ g β = tilt μ g (-β) := by
  funext x
  unfold expTilt tilt
  simp only [neg_neg]

/-- Tilted weights are nonnegative. -/
theorem expTilt_nonneg (μ g : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (β : ℝ) (x : X) :
    0 ≤ expTilt μ g β x :=
  div_nonneg (mul_nonneg (hμ x) (Real.exp_pos _).le)
    (Finset.sum_nonneg fun y _ => mul_nonneg (hμ y) (Real.exp_pos _).le)

/-- The tilted weights of a probability vector sum to one. -/
theorem sum_expTilt (μ g : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hsum : ∑ x, μ x = 1) (β : ℝ) :
    ∑ x, expTilt μ g β x = 1 := by
  unfold expTilt
  rw [← Finset.sum_div]
  exact div_self (weighted_exp_sum_pos μ (fun y => β * g y) hμ hsum).ne'

/-- **Gibbs variational identity at its optimiser.**  For a probability vector `μ` and the tilted
vector `ν = expTilt μ g β`, the logarithm of the centred moment generating function of `g` is
`β (E_ν g - E_μ g) - KL(ν ‖ μ)`.  Points with `μ x = 0` have `ν x = 0` and do not contribute to
the relative entropy (the convention of `klFin`). -/
theorem logMGF_eq_tilt (μ g : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hsum : ∑ x, μ x = 1) (β : ℝ) :
    Real.log (∑ x, μ x * Real.exp (β * (g x - ∑ y, μ y * g y))) =
      β * (∑ x, expTilt μ g β x * g x - ∑ y, μ y * g y) - klFin (expTilt μ g β) μ := by
  have hM : 0 < ∑ y, μ y * Real.exp (β * g y) :=
    weighted_exp_sum_pos μ (fun y => β * g y) hμ hsum
  -- the left-hand side is `log M - β m`
  have hL : Real.log (∑ x, μ x * Real.exp (β * (g x - ∑ y, μ y * g y))) =
      Real.log (∑ y, μ y * Real.exp (β * g y)) - β * ∑ y, μ y * g y := by
    have e : ∑ x, μ x * Real.exp (β * (g x - ∑ y, μ y * g y)) =
        Real.exp (-(β * ∑ y, μ y * g y)) * ∑ y, μ y * Real.exp (β * g y) := by
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl fun x _ => ?_
      rw [mul_left_comm, ← Real.exp_add]
      congr 2
      ring
    rw [e, Real.log_mul (Real.exp_pos _).ne' hM.ne', Real.log_exp]
    ring
  -- the relative entropy is `β E_ν g - log M`
  have hterm : ∀ x, expTilt μ g β x * (Real.log (expTilt μ g β x) - Real.log (μ x)) =
      expTilt μ g β x * (β * g x - Real.log (∑ y, μ y * Real.exp (β * g y))) := by
    intro x
    rcases (hμ x).eq_or_lt with h0 | hpos
    · have hz : expTilt μ g β x = 0 := by
        unfold expTilt
        rw [← h0, zero_mul, zero_div]
      rw [hz, zero_mul, zero_mul]
    · congr 1
      unfold expTilt
      rw [Real.log_div (mul_pos hpos (Real.exp_pos _)).ne' hM.ne',
        Real.log_mul hpos.ne' (Real.exp_pos _).ne', Real.log_exp]
      ring
  have hK : klFin (expTilt μ g β) μ =
      β * ∑ x, expTilt μ g β x * g x - Real.log (∑ y, μ y * Real.exp (β * g y)) := by
    unfold klFin
    rw [Finset.sum_congr rfl fun x _ => hterm x]
    simp only [mul_sub, Finset.sum_sub_distrib]
    rw [← Finset.sum_mul, sum_expTilt μ g hμ hsum β, one_mul, Finset.mul_sum]
    congr 1
    exact Finset.sum_congr rfl fun x _ => by ring
  rw [hL, hK]
  ring

/-- **Gibbs' inequality.**  The relative entropy `klFin p q` of nonnegative weights is
nonnegative when `p` vanishes wherever `q` does and the total mass of `q` is at most that of
`p`. -/
theorem klFin_nonneg_of_dominated (p q : X → ℝ) (hp : ∀ x, 0 ≤ p x) (hq : ∀ x, 0 ≤ q x)
    (hpq : ∀ x, q x = 0 → p x = 0) (hsum : ∑ x, q x ≤ ∑ x, p x) : 0 ≤ klFin p q := by
  have hterm : ∀ x, p x - q x ≤ p x * (Real.log (p x) - Real.log (q x)) := by
    intro x
    rcases (hp x).eq_or_lt with h0 | hpos
    · rw [← h0, zero_mul]
      linarith [hq x]
    · have hq0 : 0 < q x := lt_of_le_of_ne (hq x) fun h => hpos.ne' (hpq x h.symm)
      have h1 := Real.log_le_sub_one_of_pos (div_pos hq0 hpos)
      rw [Real.log_div hq0.ne' hpos.ne'] at h1
      have h2 := mul_le_mul_of_nonneg_left h1 hpos.le
      have h3 : p x * (q x / p x - 1) = q x - p x := by
        field_simp
      linarith
  have h := Finset.sum_le_sum fun x (_ : x ∈ univ) => hterm x
  rw [Finset.sum_sub_distrib] at h
  unfold klFin
  linarith

/-- The relative entropy of the tilted weights with respect to the reference is nonnegative. -/
theorem klFin_expTilt_nonneg (μ g : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hsum : ∑ x, μ x = 1) (β : ℝ) :
    0 ≤ klFin (expTilt μ g β) μ := by
  apply klFin_nonneg_of_dominated _ _ (expTilt_nonneg μ g hμ β) hμ
  · intro x hx
    unfold expTilt
    rw [hx, zero_mul, zero_div]
  · rw [sum_expTilt μ g hμ hsum β, hsum]

/-- **Transport–entropy bound.**  For a probability vector `μ`, an admissible `g`, `β ≥ 0` and
any coupling `γ` of the tilted vector `ν = expTilt μ g β` (row sums) with `μ` (column sums), the
logarithm of the centred moment generating function of `g` is at most
`β · (cost of γ) - KL(ν ‖ μ)`. -/
theorem logMGF_le_transport_entropy {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g)
    (μ : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hsum : ∑ x, μ x = 1) {β : ℝ} (hβ : 0 ≤ β)
    (γ : X → X → ℝ) (hγ : ∀ x y, 0 ≤ γ x y) (hrow : ∀ x, ∑ y, γ x y = expTilt μ g β x)
    (hcol : ∀ y, ∑ x, γ x y = μ y) :
    Real.log (∑ x, μ x * Real.exp (β * (g x - ∑ y, μ y * g y))) ≤
      β * ∑ x, ∑ y, γ x y * d x y - klFin (expTilt μ g β) μ := by
  rw [logMGF_eq_tilt μ g hμ hsum β]
  have h := mul_le_mul_of_nonneg_left (transport_le hg μ (expTilt μ g β) γ hγ hrow hcol) hβ
  linarith

/-- **A transport–entropy inequality bounds the Jensen gap.**  If moreover the cost of the
coupling satisfies the `T₁` inequality `(cost of γ)² ≤ 2 C · KL(ν ‖ μ)` with `C ≥ 0`, then
`log E_μ exp (β (g - E_μ g)) ≤ β² C / 2` (maximise `β w - w² / (2 C)` over `w`). -/
theorem gap_le_of_T1 {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g)
    (μ : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hsum : ∑ x, μ x = 1) {β : ℝ} (hβ : 0 ≤ β)
    (γ : X → X → ℝ) (hγ : ∀ x y, 0 ≤ γ x y) (hrow : ∀ x, ∑ y, γ x y = expTilt μ g β x)
    (hcol : ∀ y, ∑ x, γ x y = μ y) {C : ℝ} (hC : 0 ≤ C)
    (hT1 : (∑ x, ∑ y, γ x y * d x y) ^ 2 ≤ 2 * C * klFin (expTilt μ g β) μ) :
    Real.log (∑ x, μ x * Real.exp (β * (g x - ∑ y, μ y * g y))) ≤ β ^ 2 * C / 2 := by
  have h := logMGF_le_transport_entropy hg μ hμ hsum hβ γ hγ hrow hcol
  have hK := klFin_expTilt_nonneg μ g hμ hsum β
  rcases hC.eq_or_lt with h0 | hpos
  · rw [← h0, mul_zero, zero_mul] at hT1
    have hW : ∑ x, ∑ y, γ x y * d x y = 0 :=
      (pow_eq_zero_iff two_ne_zero).mp (le_antisymm hT1 (sq_nonneg _))
    rw [hW, mul_zero] at h
    rw [← h0]
    linarith
  · have key : 2 * C * (β * (∑ x, ∑ y, γ x y * d x y) - klFin (expTilt μ g β) μ) ≤
        2 * C * (β ^ 2 * C / 2) := by
      nlinarith [sq_nonneg (β * C - ∑ x, ∑ y, γ x y * d x y)]
    have := le_of_mul_le_mul_left key (by positivity)
    linarith

/-- **Couplings exist: the product coupling.**  The hypotheses of `logMGF_le_transport_entropy`
are satisfied by `γ x y = ν x · μ y`, for every probability vector `μ` and every admissible
`g`. -/
theorem logMGF_le_product_coupling {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g)
    (μ : X → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hsum : ∑ x, μ x = 1) {β : ℝ} (hβ : 0 ≤ β) :
    Real.log (∑ x, μ x * Real.exp (β * (g x - ∑ y, μ y * g y))) ≤
      β * ∑ x, ∑ y, expTilt μ g β x * μ y * d x y - klFin (expTilt μ g β) μ :=
  logMGF_le_transport_entropy hg μ hμ hsum hβ (fun x y => expTilt μ g β x * μ y)
    (fun x y => mul_nonneg (expTilt_nonneg μ g hμ β x) (hμ y))
    (fun x => by rw [← Finset.mul_sum, hsum, mul_one])
    (fun y => by rw [← Finset.sum_mul, sum_expTilt μ g hμ hsum β, one_mul])

end Transport

/-! ### Non-vacuity witnesses on a two-state system -/

/-- **Two-state witness: the exact range of a Gibbs probability.**  On `Bool` with `f = 0` and
the discrete envelope of oscillation `1` (a residual with values in an interval of length `1`),
the Gibbs probability of a state ranges exactly over `[1 / (1 + e^β), 1 / (1 + e^{-β})]`: the
bounds hold for every admissible residual and both are attained. -/
theorem gibbsProb_bool_range {β : ℝ} (hβ : 0 ≤ β) :
    (∀ g : Bool → ℝ, Admissible (discreteEnvelope 1) g →
        1 / (1 + Real.exp β) ≤ gibbsProb β g true ∧
          gibbsProb β g true ≤ 1 / (1 + Real.exp (-β))) ∧
      (∃ g : Bool → ℝ, Admissible (discreteEnvelope 1) g ∧
        gibbsProb β g true = 1 / (1 + Real.exp β)) ∧
      ∃ g : Bool → ℝ, Admissible (discreteEnvelope 1) g ∧
        gibbsProb β g true = 1 / (1 + Real.exp (-β)) := by
  have hd : IsEnvelope (discreteEnvelope (X := Bool) 1) := discreteEnvelope_isEnvelope zero_le_one
  have elo : ∑ y : Bool, Real.exp (-β * ((0 : ℝ) - 0 - discreteEnvelope 1 true y)) =
      1 + Real.exp β := by
    simp [discreteEnvelope]
  have ehi : ∑ y : Bool, Real.exp (-β * ((0 : ℝ) - 0 + discreteEnvelope 1 y true)) =
      1 + Real.exp (-β) := by
    simp [discreteEnvelope]
  refine ⟨fun g hg => ⟨?_, ?_⟩, ?_, ?_⟩
  · have h := gibbsProb_ge_sharp hg (fun _ => 0) hβ true
    simp only [zero_add] at h
    rwa [elo] at h
  · have h := gibbsProb_le_contact hg (fun _ => 0) hβ true
    simp only [zero_add] at h
    rwa [ehi] at h
  · obtain ⟨hadm, heq⟩ := gibbsProb_sharp_attained hd (fun _ => 0) β true
    refine ⟨_, hadm, ?_⟩
    simp only [zero_add] at heq
    rwa [elo] at heq
  · obtain ⟨hadm, heq⟩ := gibbsProb_contact_attained hd (fun _ => 0) β true
    refine ⟨_, hadm, ?_⟩
    simp only [zero_add] at heq
    rwa [ehi] at heq

/-- **Two-state witness for the range with evaluations.**  On `Bool` with the discrete envelope
of oscillation `1`, `f = 0` and both states evaluated (`v false = 0`, `v true = 1`, consistent by
`condEnv_bool_witness`), the interval of `gibbsProb_range_with_anchors_eq` degenerates to the
single point `1 / (1 + e^β)`: the evaluations determine the Gibbs probability. -/
theorem gibbsProb_bool_anchored_witness {β : ℝ} (hβ : 0 ≤ β) :
    {p | ∃ g : Bool → ℝ, Admissible (discreteEnvelope 1) g ∧
        (∀ a ∈ (univ : Finset Bool), g a = if a then (1 : ℝ) else 0) ∧
        gibbsProb β g true = p} = {1 / (1 + Real.exp β)} := by
  have hd : IsEnvelope (discreteEnvelope (X := Bool) 1) := discreteEnvelope_isEnvelope zero_le_one
  have hcons := condEnv_bool_witness.1
  have h := gibbsProb_range_with_anchors_eq hd univ univ_nonempty
    (fun c : Bool => if c then (1 : ℝ) else 0) hcons (fun _ => 0) hβ true
  have ce : ∀ a b : Bool, condEnv (discreteEnvelope 1) univ univ_nonempty
      (fun c : Bool => if c then (1 : ℝ) else 0) a b =
      (if a then (1 : ℝ) else 0) - (if b then (1 : ℝ) else 0) := fun a b =>
    condEnv_eq_of_mem hd univ univ_nonempty _ hcons (mem_univ a) (mem_univ b)
  simp only [zero_add, Fintype.sum_bool, ce] at h
  rw [h]
  simp

/-- **Two-state witness for the certificate theorems.**  On `Bool` with the discrete envelope of
oscillation `1`, `f = g = 0` and the single evaluation `A = {true}`, the hypothesis of
`mean_slack_le` and `card_ge_laplace` holds with `ε = log ((1 + e^β) / 2)` (with equality) and
`B = (1 + e^{-β}) / 2`; the two theorems then give the inequalities
`β / 2 ≤ log ((1 + e^β) / 2)` and `2 / (1 + e^β) ≤ (1 + e^{-β}) / 2`. -/
theorem thermal_certificate_bool_witness (β : ℝ) :
    β / 2 ≤ Real.log ((1 + Real.exp β) / 2) ∧
      2 / (1 + Real.exp β) ≤ (1 + Real.exp (-β)) / 2 := by
  have hpos : (0 : ℝ) < (1 + Real.exp β) / 2 := by positivity
  have hcert : ∑ y : Bool, Real.exp (-β * ((fun _ => (0 : ℝ)) y +
        lowerEnv (discreteEnvelope 1) {true} (singleton_nonempty true) (fun _ => 0) y)) ≤
      Real.exp (Real.log ((1 + Real.exp β) / 2)) *
        ∑ y : Bool, Real.exp (-β * ((fun _ => (0 : ℝ)) y + (fun _ => (0 : ℝ)) y)) := by
    rw [Real.exp_log hpos]
    simp [lowerEnv, discreteEnvelope]
  have h6 := mean_slack_le (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) (fun _ => 0) {true}
    (singleton_nonempty true) hcert
  have h7 := card_ge_laplace (discreteEnvelope 1) (fun _ : Bool => (0 : ℝ)) (fun _ => 0) {true}
    (singleton_nonempty true) (B := (1 + Real.exp (-β)) / 2) hcert (by
      intro a ha
      rw [Finset.mem_singleton] at ha
      subst ha
      simp [gibbsProb, slack, discreteEnvelope]
      linarith)
  simp [gibbsProb, slackFrom, slack, discreteEnvelope] at h6
  rw [Real.exp_neg, Real.exp_log hpos] at h7
  simp at h7
  exact ⟨by linarith, h7⟩

/-- **Two-state witness for the transport–entropy bound.**  On `Bool` with the uniform reference
`μ = (1/2, 1/2)`, the discrete envelope of oscillation `1`, `g` the indicator of `true` and
`β = log 3`: the tilted vector is `ν = (3/4, 1/4)` on `(true, false)`, the coupling
`γ = [[1/2, 1/4], [0, 1/4]]` has cost `1/4`, and `KL(ν ‖ μ) = (3/4) log 3 - log 2 ≥ 1/32`, so
the `T₁` hypothesis of `gap_le_of_T1` holds with `C = 1`; the conclusion is the displayed
bound. -/
theorem gap_le_of_T1_bool_witness :
    Real.log (∑ x : Bool, (1 / 2 : ℝ) * Real.exp (Real.log 3 *
      ((if x then (1 : ℝ) else 0) - ∑ y : Bool, (1 / 2 : ℝ) * (if y then (1 : ℝ) else 0)))) ≤
      Real.log 3 ^ 2 * 1 / 2 := by
  have hadm : Admissible (discreteEnvelope 1) (fun b : Bool => if b then (1 : ℝ) else 0) :=
    admissible_of_bounds (lo := 0) _ fun b => by cases b <;> norm_num
  have hμ : ∀ b : Bool, (0 : ℝ) ≤ (fun _ : Bool => (1 / 2 : ℝ)) b := fun _ => by norm_num
  have hsum : ∑ b : Bool, (fun _ : Bool => (1 / 2 : ℝ)) b = 1 := by
    rw [Fintype.sum_bool]
    norm_num
  have hν : ∀ b : Bool, expTilt (fun _ : Bool => (1 / 2 : ℝ))
      (fun b : Bool => if b then (1 : ℝ) else 0) (Real.log 3) b = if b then 3 / 4 else 1 / 4 := by
    intro b
    unfold expTilt
    rw [Fintype.sum_bool]
    have e3 : Real.exp (Real.log 3) = 3 := Real.exp_log (by norm_num)
    cases b <;> simp [e3] <;> norm_num
  have hK : klFin (expTilt (fun _ : Bool => (1 / 2 : ℝ))
      (fun b : Bool => if b then (1 : ℝ) else 0) (Real.log 3)) (fun _ => 1 / 2) =
      3 / 4 * Real.log 3 - Real.log 2 := by
    have h4 : Real.log 4 = 2 * Real.log 2 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]
      norm_num
    unfold klFin
    rw [Fintype.sum_bool, hν true, hν false]
    simp only [if_true, if_false, Bool.false_eq_true]
    rw [Real.log_div (by norm_num) (by norm_num), Real.log_div (by norm_num) (by norm_num),
      Real.log_div (by norm_num) (by norm_num), Real.log_one, h4]
    ring
  have h32 : 1 / 3 ≤ Real.log 3 - Real.log 2 := by
    have h := Real.one_sub_inv_le_log_of_pos (by norm_num : (0 : ℝ) < 3 / 2)
    rw [Real.log_div (by norm_num) (by norm_num)] at h
    norm_num at h
    linarith
  have h2 : Real.log 2 < 0.6931471808 := Real.log_two_lt_d9
  refine gap_le_of_T1 hadm _ hμ hsum (Real.log_nonneg (by norm_num))
    (fun x y => if x then (if y then 1 / 2 else 1 / 4) else (if y then 0 else 1 / 4))
    (fun x y => by cases x <;> cases y <;> norm_num) (fun x => ?_) (fun y => ?_) zero_le_one ?_
  · rw [hν, Fintype.sum_bool]
    cases x <;> norm_num
  · rw [Fintype.sum_bool]
    cases y <;> norm_num
  · rw [hK]
    simp only [Fintype.sum_bool, discreteEnvelope]
    norm_num
    linarith

end MetricChain
