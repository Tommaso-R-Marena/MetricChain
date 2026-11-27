import Mathlib
import proofs.Core.Basic

/-!
# Envelope duality: certification under a non-decomposable residual

The conformational energy is `E = f + g`, where `f` is the explicit ("white-box") part and `g`
is a non-decomposable residual (for instance a neural correction) that is only known through

* an **envelope** `d : X → X → ℝ` (a possibly *asymmetric* cost with `d x x = 0` and the triangle
  inequality) such that `g x - g y ≤ d x y`, and
* its values on a finite set of evaluated **anchors**.

Global bounds `lo ≤ g ≤ hi` are the envelope `d x y = (hi - lo)·[x ≠ y]`; per-site differential
envelopes `δ_i` are the site-additive envelope `d x y = ∑ i, δ i (x i) (y i)`
(`admissible_of_single_site`), and certified Lipschitz bounds in torsion space are metric envelopes.

Main results (all are exact characterisations, valid for every envelope):

* `robust_minimizer_iff` — a configuration can be optimal for *some* admissible residual iff it
  lies on the contact set of the Pasch–Hausdorff envelope of `f`: `∀ y, f x ≤ f y + d y x`.
* `robust_certified_iff` — a configuration is optimal for *every* admissible residual iff it is
  a `d`-sharp minimum of `f`: `∀ y, d x y ≤ f y - f x`.
* `lowerEnv`, `upperEnv` — the McShane envelopes of the anchor data are admissible, interpolate
  the data and bracket every admissible residual, so the minimum energy and the partition function
  (at every `β ≥ 0`) lie between their values at the two envelopes (`robust_min_bracket`,
  `robust_partition_bracket`); conversely every value in between is attained by an admissible
  residual matching the data (`robust_min_interval_exact`, `robust_partition_interval_exact`), so
  the set of possible values is *exactly* that interval.
* `anchor_necessary`, `anchor_card_lower_bound` — witness-size lower bound: if the true residual is
  `κ`-Lipschitz for the envelope (`κ ≤ 1`), every configuration whose energy gap is below
  `(1 - κ)·σ - ε` (with `σ` the envelope separation) *must* be evaluated by any `ε`-certificate.
* `differential_dee_sound` — differential dead-end elimination is the single-site, uniform-dominator
  shadow of the contact-set criterion.
* `energy_window_exact` — with global bounds only, the exact set of possibly-optimal
  configurations is the energy window; the "global residual bottleneck" is information-theoretic.
-/

namespace MetricChain

open Finset

variable {X : Type*}

/-- An *envelope*: a possibly asymmetric cost with zero diagonal and the triangle inequality. -/
structure IsEnvelope (d : X → X → ℝ) : Prop where
  self : ∀ x, d x x = 0
  triangle : ∀ x y z, d x z ≤ d x y + d y z

/-- A residual `g` is admissible for the envelope `d` when `g x - g y ≤ d x y` for all `x y`. -/
def Admissible (d : X → X → ℝ) (g : X → ℝ) : Prop := ∀ x y, g x - g y ≤ d x y

/-! ### Exact characterisations of robust optimality -/

/-- **Contact-set theorem.** `x` minimises `f + g` for *some* admissible residual `g` iff
`f x ≤ f y + d y x` for all `y`, i.e. iff `x` lies on the contact set of the Pasch–Hausdorff
(`d`-Lipschitz) envelope of `f`.  The extremal residual is the envelope itself, `g = d · x`. -/
theorem robust_minimizer_iff {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (x : X) :
    (∃ g, Admissible d g ∧ ∀ y, f x + g x ≤ f y + g y) ↔ ∀ y, f x ≤ f y + d y x := by
  constructor
  · rintro ⟨g, hg, hmin⟩ y
    have h1 := hmin y
    have h2 := hg y x
    linarith
  · intro h
    refine ⟨fun y => d y x, ?_, ?_⟩
    · intro y z
      have := hd.triangle y z x
      linarith
    · intro y
      have h1 := h y
      have h2 := hd.self x
      simp only [h2]
      linarith

/-- **Sharp-minimum theorem.** `x` minimises `f + g` for *every* admissible residual `g` iff `f`
grows at least as fast as the envelope away from `x`: `d x y ≤ f y - f x` for all `y`. -/
theorem robust_certified_iff {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (x : X) :
    (∀ g, Admissible d g → ∀ y, f x + g x ≤ f y + g y) ↔ ∀ y, d x y ≤ f y - f x := by
  constructor
  · intro h y
    have hadm : Admissible d (fun z => -d x z) := by
      intro z w
      have := hd.triangle x z w
      linarith
    have h1 := h _ hadm y
    have h2 := hd.self x
    simp only [h2] at h1
    linarith
  · intro h g hg y
    have h1 := h y
    have h2 := hg x y
    linarith

/-! ### McShane envelopes of anchor data -/

/-- Lower McShane envelope: the smallest admissible residual compatible with the anchor data. -/
noncomputable def lowerEnv (d : X → X → ℝ) (A : Finset X) (hA : A.Nonempty) (v : X → ℝ)
    (y : X) : ℝ :=
  A.sup' hA fun a => v a - d a y

/-- Upper McShane envelope: the largest admissible residual compatible with the anchor data. -/
noncomputable def upperEnv (d : X → X → ℝ) (A : Finset X) (hA : A.Nonempty) (v : X → ℝ)
    (y : X) : ℝ :=
  A.inf' hA fun a => v a + d y a

theorem lowerEnv_admissible {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) : Admissible d (lowerEnv d A hA v) := by
  intro y z
  have key : lowerEnv d A hA v y ≤ lowerEnv d A hA v z + d y z := by
    unfold lowerEnv
    apply Finset.sup'_le
    intro a ha
    have h1 : v a - d a z ≤ A.sup' hA (fun a => v a - d a z) :=
      Finset.le_sup' (fun a => v a - d a z) ha
    have h2 := hd.triangle a y z
    linarith
  linarith

theorem upperEnv_admissible {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) : Admissible d (upperEnv d A hA v) := by
  intro y z
  have key : upperEnv d A hA v y ≤ upperEnv d A hA v z + d y z := by
    obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => v a + d z a)
    have h1 : upperEnv d A hA v y ≤ v a + d y a := by
      unfold upperEnv
      exact Finset.inf'_le (fun a => v a + d y a) ha
    have h2 := hd.triangle y z a
    have h3 : upperEnv d A hA v z = v a + d z a := hmin
    linarith
  linarith

/-- Every admissible residual that agrees with the data on the anchors lies above the lower
envelope. -/
theorem lowerEnv_le {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, g a = v a) (y : X) :
    lowerEnv d A hA v y ≤ g y := by
  unfold lowerEnv
  apply Finset.sup'_le
  intro a ha
  have := hg a y
  rw [← hv a ha]
  linarith

/-- Every admissible residual that agrees with the data on the anchors lies below the upper
envelope. -/
theorem le_upperEnv {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, g a = v a) (y : X) :
    g y ≤ upperEnv d A hA v y := by
  unfold upperEnv
  apply Finset.le_inf'
  intro a ha
  have := hg y a
  rw [← hv a ha]
  linarith

/-- The lower envelope interpolates consistent anchor data. -/
theorem lowerEnv_eq_of_mem {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) {a : X} (ha : a ∈ A) :
    lowerEnv d A hA v a = v a := by
  apply le_antisymm
  · unfold lowerEnv
    apply Finset.sup'_le
    intro b hb
    have := hv b hb a ha
    linarith
  · have h1 : v a - d a a ≤ lowerEnv d A hA v a :=
      Finset.le_sup' (fun b => v b - d b a) ha
    have h2 := hd.self a
    linarith

/-- The upper envelope interpolates consistent anchor data. -/
theorem upperEnv_eq_of_mem {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) {a : X} (ha : a ∈ A) :
    upperEnv d A hA v a = v a := by
  apply le_antisymm
  · have h1 : upperEnv d A hA v a ≤ v a + d a a :=
      Finset.inf'_le (fun b => v b + d a b) ha
    have h2 := hd.self a
    linarith
  · unfold upperEnv
    apply Finset.le_inf'
    intro b hb
    have := hv a ha b hb
    linarith

/-! ### The exact robust interval (zero and finite temperature) -/

/-- **Robust interval, zero temperature (bracket).**  For every admissible residual compatible
with the anchor data, the minimum energy over a finite configuration set lies between the minima
computed with the two McShane envelopes.  For consistent data both endpoints and every value in
between are attained by admissible residuals (`robust_min_interval_exact`), so no certificate
based on the same information can report a tighter interval. -/
theorem robust_min_bracket {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, g a = v a) (f : X → ℝ) (S : Finset X)
    (hS : S.Nonempty) :
    S.inf' hS (fun y => f y + lowerEnv d A hA v y) ≤ S.inf' hS (fun y => f y + g y) ∧
      S.inf' hS (fun y => f y + g y) ≤ S.inf' hS (fun y => f y + upperEnv d A hA v y) := by
  constructor
  · apply Finset.le_inf'
    intro y hy
    have h1 := Finset.inf'_le (fun y => f y + lowerEnv d A hA v y) hy
    have h2 := lowerEnv_le hg A hA v hv y
    linarith
  · apply Finset.le_inf'
    intro y hy
    have h1 := Finset.inf'_le (fun y => f y + g y) hy
    have h2 := le_upperEnv hg A hA v hv y
    linarith

/-- **Robust interval, finite temperature (bracket).**  The partition function of `f + g` is
bracketed by the partition functions of `f` plus the two McShane envelopes, at every `β ≥ 0`;
every value in between is attained (`robust_partition_interval_exact`). -/
theorem robust_partition_bracket {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g)
    (A : Finset X) (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, g a = v a) (f : X → ℝ)
    (S : Finset X) {β : ℝ} (hβ : 0 ≤ β) :
    partitionFn β (fun y => f y + upperEnv d A hA v y) S ≤ partitionFn β (fun y => f y + g y) S ∧
      partitionFn β (fun y => f y + g y) S ≤
        partitionFn β (fun y => f y + lowerEnv d A hA v y) S := by
  constructor
  · apply partitionFn_anti hβ
    intro y _
    have := le_upperEnv hg A hA v hv y
    linarith
  · apply partitionFn_anti hβ
    intro y _
    have := lowerEnv_le hg A hA v hv y
    linarith

/-! ### The robust interval is exact: every intermediate value is attained -/

/-- Convex combinations of admissible residuals are admissible. -/
theorem Admissible.convex {d : X → X → ℝ} {g₁ g₂ : X → ℝ} (h₁ : Admissible d g₁)
    (h₂ : Admissible d g₂) {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    Admissible d (fun x => (1 - t) * g₁ x + t * g₂ x) := by
  intro x y
  have e1 := mul_le_mul_of_nonneg_left (h₁ x y) (sub_nonneg.mpr ht1)
  have e2 := mul_le_mul_of_nonneg_left (h₂ x y) ht0
  show (1 - t) * g₁ x + t * g₂ x - ((1 - t) * g₁ y + t * g₂ y) ≤ d x y
  nlinarith

/-- The convex interpolation between the two McShane envelopes is admissible and matches
consistent anchor data. -/
theorem interpEnv_admissible_and_interpolates {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) {t : ℝ}
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    Admissible d (fun x => (1 - t) * lowerEnv d A hA v x + t * upperEnv d A hA v x) ∧
      ∀ a ∈ A, (1 - t) * lowerEnv d A hA v a + t * upperEnv d A hA v a = v a := by
  refine ⟨(lowerEnv_admissible hd A hA v).convex (upperEnv_admissible hd A hA v) ht0 ht1, ?_⟩
  intro a ha
  rw [lowerEnv_eq_of_mem hd A hA v hv ha, upperEnv_eq_of_mem hd A hA v hv ha]
  ring

/-- **The robust interval is exact (zero temperature).**  For consistent anchor data, every value
between the minimum energies computed with the two McShane envelopes is the minimum energy of
`f + g` for some admissible residual `g` that matches the data on the anchors.  Together with
`robust_min_bracket`: the set of possible optimal values is exactly this interval. -/
theorem robust_min_interval_exact {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (f : X → ℝ)
    (S : Finset X) (hS : S.Nonempty) (τ : ℝ)
    (hτ : τ ∈ Set.Icc (S.inf' hS fun y => f y + lowerEnv d A hA v y)
      (S.inf' hS fun y => f y + upperEnv d A hA v y)) :
    ∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧ S.inf' hS (fun y => f y + g y) = τ := by
  let F : ℝ → ℝ := fun t =>
    S.inf' hS fun y => f y + ((1 - t) * lowerEnv d A hA v y + t * upperEnv d A hA v y)
  have hcont : Continuous F := by
    apply Continuous.finset_inf'_apply
    intro y _
    fun_prop
  have h0 : F 0 = S.inf' hS fun y => f y + lowerEnv d A hA v y := by
    show (S.inf' hS fun y => f y + ((1 - 0) * lowerEnv d A hA v y + 0 * upperEnv d A hA v y)) = _
    congr 1
    funext y
    ring
  have h1 : F 1 = S.inf' hS fun y => f y + upperEnv d A hA v y := by
    show (S.inf' hS fun y => f y + ((1 - 1) * lowerEnv d A hA v y + 1 * upperEnv d A hA v y)) = _
    congr 1
    funext y
    ring
  have hmem : τ ∈ Set.Icc (F 0) (F 1) := by rw [h0, h1]; exact hτ
  obtain ⟨t, ht, hFt⟩ := intermediate_value_Icc (zero_le_one' ℝ) hcont.continuousOn hmem
  obtain ⟨hadm, hint⟩ := interpEnv_admissible_and_interpolates hd A hA v hv ht.1 ht.2
  exact ⟨_, hadm, hint, hFt⟩

/-- **The robust interval is exact (finite temperature).**  For consistent anchor data, every
value between the partition functions computed with the upper and the lower McShane envelope is
the partition function of `f + g` for some admissible residual `g` that matches the data on the
anchors.  The statement is meaningful for `β ≥ 0`, where the hypothesis interval is the range of
`Z` (`robust_partition_bracket`); for `β < 0` the two ends are exchanged and the hypothesis
interval is empty or a single point. -/
theorem robust_partition_interval_exact {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (f : X → ℝ)
    (S : Finset X) (β : ℝ) (τ : ℝ)
    (hτ : τ ∈ Set.Icc (partitionFn β (fun y => f y + upperEnv d A hA v y) S)
      (partitionFn β (fun y => f y + lowerEnv d A hA v y) S)) :
    ∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧ partitionFn β (fun y => f y + g y) S = τ := by
  let F : ℝ → ℝ := fun t =>
    partitionFn β (fun y => f y + ((1 - t) * lowerEnv d A hA v y + t * upperEnv d A hA v y)) S
  have hcont : Continuous F := by
    show Continuous fun t => partitionFn β
      (fun y => f y + ((1 - t) * lowerEnv d A hA v y + t * upperEnv d A hA v y)) S
    unfold partitionFn
    fun_prop
  have h0 : F 0 = partitionFn β (fun y => f y + lowerEnv d A hA v y) S := by
    show partitionFn β
      (fun y => f y + ((1 - 0) * lowerEnv d A hA v y + 0 * upperEnv d A hA v y)) S = _
    congr 1
    funext y
    ring
  have h1 : F 1 = partitionFn β (fun y => f y + upperEnv d A hA v y) S := by
    show partitionFn β
      (fun y => f y + ((1 - 1) * lowerEnv d A hA v y + 1 * upperEnv d A hA v y)) S = _
    congr 1
    funext y
    ring
  have hmem : τ ∈ Set.Icc (F 1) (F 0) := by rw [h0, h1]; exact hτ
  obtain ⟨t, ht, hFt⟩ := intermediate_value_Icc' (zero_le_one' ℝ) hcont.continuousOn hmem
  obtain ⟨hadm, hint⟩ := interpEnv_admissible_and_interpolates hd A hA v hv ht.1 ht.2
  exact ⟨_, hadm, hint, hFt⟩

/-! ### The query model: exact pruning criterion given evaluated anchors -/

/-- For consistent anchor data the lower envelope lies below the upper envelope. -/
theorem lowerEnv_le_upperEnv {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (y : X) :
    lowerEnv d A hA v y ≤ upperEnv d A hA v y := by
  unfold lowerEnv upperEnv
  apply Finset.sup'_le
  intro a ha
  apply Finset.le_inf'
  intro b hb
  have h1 := hv a ha b hb
  have h2 := hd.triangle a y b
  linarith

/-- **Query-model contact theorem (optimal pruning with evaluated anchors).**  Suppose the
residual has been evaluated on the anchors `A` (consistent data `v`).  A configuration `x` can be
a minimiser of `f + g` for *some* admissible residual `g` that agrees with the data iff

1. `f x ≤ f y + d y x` for all `y` (the contact-set condition), and
2. `f x + lowerEnv x ≤ f y + upperEnv y` for all `y` (its optimistic value does not exceed the
   pessimistic value of any competitor; for an anchor `y` this is "lower bound ≤ incumbent").

Hence the set violating 1 or 2 is *exactly* the set of configurations that are minimisers for no
admissible residual consistent with the evaluations: a rule that keeps every possible minimiser
cannot discard more, and any rule discarding less is not optimal.  (A rule that only preserves
the minimum *value* may discard more because of ties; the exact criterion for certifying a
configuration is `robust_certified_with_anchors_iff` in `ConditionalEnvelope.lean`.)  With one
anchor and the discrete envelope this is the pruning-interval rule of minimised dead-end
elimination. -/
theorem robust_minimizer_with_anchors_iff {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (f : X → ℝ)
    (x : X) :
    (∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧ ∀ y, f x + g x ≤ f y + g y) ↔
      (∀ y, f x ≤ f y + d y x) ∧
        ∀ y, f x + lowerEnv d A hA v x ≤ f y + upperEnv d A hA v y := by
  constructor
  · rintro ⟨g, hg, hgv, hmin⟩
    refine ⟨fun y => ?_, fun y => ?_⟩
    · have h1 := hmin y
      have h2 := hg y x
      linarith
    · have h1 := hmin y
      have h2 := lowerEnv_le hg A hA v hgv x
      have h3 := le_upperEnv hg A hA v hgv y
      linarith
  · rintro ⟨h1, h2⟩
    set γ := lowerEnv d A hA v x with hγ
    refine ⟨fun y => min (upperEnv d A hA v y) (γ + d y x), ?_, ?_, ?_⟩
    · -- admissible: a minimum of two admissible functions
      intro y z
      have e1 := upperEnv_admissible hd A hA v y z
      have e2 := hd.triangle y z x
      have e3 : min (upperEnv d A hA v y) (γ + d y x) ≤ upperEnv d A hA v z + d y z :=
        le_trans (min_le_left _ _) (by linarith)
      have e4 : min (upperEnv d A hA v y) (γ + d y x) ≤ γ + d z x + d y z :=
        le_trans (min_le_right _ _) (by linarith)
      have e5 : min (upperEnv d A hA v y) (γ + d y x) ≤
          min (upperEnv d A hA v z) (γ + d z x) + d y z := by
        rw [← min_add_add_right]
        exact le_min e3 e4
      linarith
    · -- agrees with the anchor data
      intro a ha
      have e1 := upperEnv_eq_of_mem hd A hA v hv ha
      have e2 : v a - d a x ≤ γ := Finset.le_sup' (fun b => v b - d b x) ha
      show min (upperEnv d A hA v a) (γ + d a x) = v a
      rw [e1]
      exact min_eq_left (by linarith)
    · -- `x` is optimal
      intro y
      have e1 := lowerEnv_le_upperEnv hd A hA v hv x
      have e2 := hd.self x
      have hx : min (upperEnv d A hA v x) (γ + d x x) = γ := by
        rw [e2, add_zero]
        exact min_eq_right e1
      show f x + min (upperEnv d A hA v x) (γ + d x x) ≤
        f y + min (upperEnv d A hA v y) (γ + d y x)
      rw [hx]
      have e3 := h1 y
      have e4 := h2 y
      have e5 : f x + γ ≤ f y + (γ + d y x) := by linarith
      rw [← min_add_add_left]
      exact le_min e4 e5

/-! ### Witness-size lower bound -/

/-- **Anchors are necessary.**  Let the true residual `g` be `κ`-Lipschitz for the envelope with
`κ ≤ 1` (so the certified envelope is loose by the factor `1 - κ`).  Suppose the anchor set `A`
yields an `ε`-certificate: the best evaluated value minus `ε` is a lower bound on `f` plus the
lower envelope everywhere.  Then every configuration `y` that is `σ`-separated from the anchors
and whose energy gap is below `(1 - κ) σ - ε` must itself be an anchor. -/
theorem anchor_necessary {d : X → X → ℝ} (f g : X → ℝ) {κ : ℝ} (hκ : κ ≤ 1)
    (hgκ : ∀ x y, g x - g y ≤ κ * d x y) (A : Finset X) (hA : A.Nonempty) {ε Estar σ : ℝ}
    (hstar : ∀ a ∈ A, Estar ≤ f a + g a)
    (hcert : ∀ y, A.inf' hA (fun a => f a + g a) - ε ≤ f y + lowerEnv d A hA g y)
    (y : X) (hsep : ∀ a ∈ A, a ≠ y → σ ≤ d a y)
    (hy : f y + g y - Estar < (1 - κ) * σ - ε) : y ∈ A := by
  by_contra hyA
  have henv : lowerEnv d A hA g y ≤ g y - (1 - κ) * σ := by
    unfold lowerEnv
    apply Finset.sup'_le
    intro a ha
    have hne : a ≠ y := fun h => hyA (h ▸ ha)
    have h1 := hgκ a y
    have h2 := hsep a ha hne
    have h3 : (1 - κ) * σ ≤ (1 - κ) * d a y :=
      mul_le_mul_of_nonneg_left h2 (by linarith)
    nlinarith
  have hU : Estar ≤ A.inf' hA (fun a => f a + g a) := by
    apply Finset.le_inf'
    intro a ha
    exact hstar a ha
  have h4 := hcert y
  linarith

open Classical in
/-- **Witness-size lower bound (envelope-resolution entropy bound).**  Under the hypotheses of
`anchor_necessary` with a uniform separation `σ`, the number of residual evaluations in any
`ε`-certificate is at least the number of configurations whose energy gap is below
`(1 - κ) σ - ε`. -/
theorem anchor_card_lower_bound [Fintype X] {d : X → X → ℝ} (f g : X → ℝ) {κ : ℝ} (hκ : κ ≤ 1)
    (hgκ : ∀ x y, g x - g y ≤ κ * d x y) (A : Finset X) (hA : A.Nonempty) {ε Estar σ : ℝ}
    (hstar : ∀ a ∈ A, Estar ≤ f a + g a)
    (hcert : ∀ y, A.inf' hA (fun a => f a + g a) - ε ≤ f y + lowerEnv d A hA g y)
    (hsep : ∀ a y, a ≠ y → σ ≤ d a y) :
    (Finset.univ.filter fun y => f y + g y - Estar < (1 - κ) * σ - ε).card ≤ A.card := by
  apply Finset.card_le_card
  intro y hy
  rw [Finset.mem_filter] at hy
  exact anchor_necessary f g hκ hgκ A hA hstar hcert y (fun a _ hne => hsep a y hne) hy.2

/-! ### Site-additive envelopes: from local differential envelopes to a global envelope -/

section Site

variable {ι : Type*} [Fintype ι] [DecidableEq ι] {σ : ι → Type*}

/-- The site-additive envelope generated by per-site differential envelopes `δ i`. -/
def siteEnvelope (δ : ∀ i, σ i → σ i → ℝ) (x y : ∀ i, σ i) : ℝ := ∑ i, δ i (x i) (y i)

omit [DecidableEq ι] in
theorem siteEnvelope_isEnvelope (δ : ∀ i, σ i → σ i → ℝ) (hδ : ∀ i, IsEnvelope (δ i)) :
    IsEnvelope (siteEnvelope δ) where
  self x := by
    unfold siteEnvelope
    exact Finset.sum_eq_zero fun i _ => (hδ i).self (x i)
  triangle x y z := by
    unfold siteEnvelope
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_le_sum fun i _ => (hδ i).triangle (x i) (y i) (z i)

/-- **Local-to-global envelope lemma.**  A residual that satisfies the single-site differential
envelopes `g (x[i ↦ a]) - g x ≤ δ i a (x i)` is admissible for the site-additive envelope. -/
theorem admissible_of_single_site (δ : ∀ i, σ i → σ i → ℝ) (g : (∀ i, σ i) → ℝ)
    (hloc : ∀ (x : ∀ i, σ i) (i : ι) (a : σ i), g (Function.update x i a) - g x ≤ δ i a (x i)) :
    Admissible (siteEnvelope δ) g := by
  have key : ∀ s : Finset ι, ∀ x y : ∀ i, σ i, (∀ i, i ∉ s → x i = y i) →
      g x - g y ≤ ∑ i ∈ s, δ i (x i) (y i) := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      intro x y hxy
      have : x = y := funext fun i => hxy i (Finset.notMem_empty i)
      simp [this]
    | insert j s hj ih =>
      intro x y hxy
      have hz : ∀ i, i ∉ s → x i = Function.update y j (x j) i := by
        intro i hi
        by_cases hij : i = j
        · subst hij
          simp
        · rw [Function.update_of_ne hij]
          exact hxy i (by simp [hij, hi])
      have h1 := ih x (Function.update y j (x j)) hz
      have h2 := hloc y j (x j)
      have h3 : ∑ i ∈ s, δ i (x i) (Function.update y j (x j) i) = ∑ i ∈ s, δ i (x i) (y i) := by
        apply Finset.sum_congr rfl
        intro i hi
        have hij : i ≠ j := fun h => hj (h ▸ hi)
        rw [Function.update_of_ne hij]
      rw [Finset.sum_insert hj]
      linarith
  intro x y
  have := key Finset.univ x y (fun i hi => absurd (Finset.mem_univ i) hi)
  simpa [siteEnvelope] using this

/-- The site-additive envelope between a configuration and a single-site modification of it. -/
theorem siteEnvelope_update (δ : ∀ i, σ i → σ i → ℝ) (hδ : ∀ i a, δ i a a = 0)
    (x : ∀ i, σ i) (i : ι) (t : σ i) :
    siteEnvelope δ (Function.update x i t) x = δ i t (x i) := by
  unfold siteEnvelope
  rw [Finset.sum_eq_single i]
  · simp
  · intro j _ hji
    rw [Function.update_of_ne hji]
    exact hδ j (x j)
  · intro h
    exact absurd (Finset.mem_univ i) h

/-- **Differential dead-end elimination is sound for the whole residual class.**  If replacing
state `r` at site `i` by `t` lowers the white-box energy by more than the differential envelope
`δ i t r` in every context, then no configuration with `x i = r` can be optimal for any admissible
residual. -/
theorem differential_dee_sound (δ : ∀ i, σ i → σ i → ℝ) (hδ : ∀ i a, δ i a a = 0)
    (f : (∀ i, σ i) → ℝ) (i : ι) (r t : σ i)
    (hdom : ∀ x : ∀ i, σ i, x i = r → f (Function.update x i t) + δ i t r < f x)
    (g : (∀ i, σ i) → ℝ) (hg : Admissible (siteEnvelope δ) g) (x : ∀ i, σ i) (hx : x i = r) :
    ∃ y, f y + g y < f x + g x := by
  refine ⟨Function.update x i t, ?_⟩
  have h1 := hg (Function.update x i t) x
  rw [siteEnvelope_update δ hδ x i t, hx] at h1
  have h2 := hdom x hx
  linarith

end Site

/-! ### Global bounds only: the energy window is exact -/

section Window

variable [DecidableEq X]

/-- The envelope encoding "only global bounds are known": oscillation `ω` between distinct
configurations. -/
def discreteEnvelope (ω : ℝ) (x y : X) : ℝ := if x = y then 0 else ω

theorem discreteEnvelope_isEnvelope {ω : ℝ} (hω : 0 ≤ ω) :
    IsEnvelope (discreteEnvelope (X := X) ω) where
  self x := by simp [discreteEnvelope]
  triangle x y z := by
    unfold discreteEnvelope
    by_cases hxz : x = z
    · simp only [hxz, if_true]
      split_ifs <;> linarith
    · by_cases hxy : x = y
      · subst hxy
        simp [hxz]
      · simp only [hxz, hxy, if_false]
        split_ifs <;> linarith

/-- A residual with values in an interval of length `ω` is admissible for the discrete envelope. -/
theorem admissible_of_bounds {ω lo : ℝ} (g : X → ℝ) (h : ∀ x, lo ≤ g x ∧ g x ≤ lo + ω) :
    Admissible (discreteEnvelope ω) g := by
  intro x y
  unfold discreteEnvelope
  split_ifs with hxy
  · subst hxy
    simp
  · have h1 := (h x).2
    have h2 := (h y).1
    linarith

/-- **The energy window is exact.**  If only global bounds on the residual are known
(oscillation `ω ≥ 0`), a configuration can be optimal for some admissible residual iff its
white-box energy is within `ω` of every other configuration's.  Hence *no* sound pruning rule
using this information alone can remove a configuration inside the window: the classical
"global residual bottleneck" is information-theoretic, not an algorithmic weakness. -/
theorem energy_window_exact {ω : ℝ} (hω : 0 ≤ ω) (f : X → ℝ) (x : X) :
    (∃ g, Admissible (discreteEnvelope ω) g ∧ ∀ y, f x + g x ≤ f y + g y) ↔
      ∀ y, f x ≤ f y + ω := by
  rw [robust_minimizer_iff (discreteEnvelope_isEnvelope hω)]
  constructor
  · intro h y
    have := h y
    unfold discreteEnvelope at this
    split_ifs at this <;> linarith
  · intro h y
    unfold discreteEnvelope
    split_ifs with hyx
    · subst hyx
      simp
    · exact h y

end Window

end MetricChain
