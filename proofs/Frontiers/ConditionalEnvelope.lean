import Mathlib
import proofs.Frontiers.EnvelopeDuality

/-!
# Conditioning on evaluations is a rank-one update of the envelope

Setting of `EnvelopeDuality.lean`: an energy `E = f + g` with a known part `f` and a residual `g`
that is only known to be admissible for an envelope `d` (`g x - g y ≤ d x y`).  Suppose `g` has
been evaluated on a finite nonempty set `A` of anchors, with consistent values `v`.  Write
`U = upperEnv d A hA v` and `L = lowerEnv d A hA v` for the two McShane envelopes of the data.

The **conditional envelope** is

  `condEnv d A hA v x y = min (d x y) (U x - L y)`.

In the min-plus (tropical) semiring the matrix `(x, y) ↦ U x - L y` has rank one and `min` is the
addition, so conditioning on the evaluations is a *rank-one update* of the envelope.  (Since
`U x - L y = min_{a, b ∈ A} (d x a + (v a - v b) + d b y)`, the conditional envelope is also the
shortest-path closure of `d` after adding an edge `a → b` of length `v a - v b` for every pair of
anchors: in the language of difference constraints it is the *minimal network* of the system
`g x - g y ≤ d x y`, `g a - g b = v a - v b`, as for simple temporal networks and difference-bound
matrices.)  The results of this file say that the updated envelope carries exactly the
information "admissible for `d` and equal to `v` on `A`":

* `condEnv_isEnvelope` — the conditional envelope is again an envelope (zero diagonal, triangle
  inequality), although it is in general asymmetric and may take negative values
  (`condEnv_eq_of_mem`: on the anchors it is the difference of the data);
* `admissible_condEnv`, `admissible_of_condEnv`, `exists_consistent_shift` — a residual is
  admissible for `d` and matches the data iff it is admissible for `condEnv` and matches the data
  at *one* anchor (`admissible_condEnv_iff`); hence, up to an additive constant, the residuals
  consistent with the evaluations are exactly the residuals admissible for the conditional
  envelope;
* `condEnv_attained`, `condEnv_isGreatest` — exactness: `condEnv d A hA v x y` is the largest
  value of `g x - g y` over the consistent admissible residuals (`sub_le_condEnv`), and it is
  attained;
* `condEnv_tower` — conditioning in stages: for anchor sets `A ⊆ A'`, updating with the
  evaluations on `A` and then with those on `A'` is the same as updating once with those on `A'`
  (in particular the update is idempotent);
* `robust_minimizer_with_anchors_iff'` — the query-model contact theorem
  (`robust_minimizer_with_anchors_iff`) *is* the contact-set theorem `robust_minimizer_iff` for
  the updated envelope: `x` can be optimal for some consistent residual iff
  `∀ y, f x ≤ f y + condEnv d A hA v y x` (`contact_condEnv_iff` unfolds this into the two
  conditions of the earlier statement);
* `robust_certified_with_anchors_iff` — the sharp-minimum theorem with evaluations: `x` is optimal
  for *every* consistent residual iff `∀ y, condEnv d A hA v x y ≤ f y - f x`;
* `max_regret_le`, `max_regret_attained`, `worst_case_regret_isGreatest` — the worst-case regret
  of declaring `x` optimal is exactly `max_y (f x - f y + condEnv d A hA v x y)`.

A single evaluation only fixes the additive constant and leaves the envelope unchanged
(`condEnv_singleton`); the first informative update needs two anchors
(`condEnv_three_point_witness`, `certified_three_point_witness`, `pruned_three_point_witness`).
-/

namespace MetricChain

open Finset

variable {X : Type*}

/-! ### The conditional envelope -/

/-- The **conditional envelope** of `d` given the evaluations `v` on the anchors `A`: the
tropical rank-one update `min (d x y) (U x - L y)` of `d` by the McShane envelopes of the data. -/
noncomputable def condEnv (d : X → X → ℝ) (A : Finset X) (hA : A.Nonempty) (v : X → ℝ)
    (x y : X) : ℝ :=
  min (d x y) (upperEnv d A hA v x - lowerEnv d A hA v y)

/-- The conditional envelope is at most the original envelope. -/
theorem condEnv_le (d : X → X → ℝ) (A : Finset X) (hA : A.Nonempty) (v : X → ℝ) (x y : X) :
    condEnv d A hA v x y ≤ d x y :=
  min_le_left _ _

/-- The conditional envelope is at most the width `U x - L y` of the McShane bracket. -/
theorem condEnv_le_bracket (d : X → X → ℝ) (A : Finset X) (hA : A.Nonempty) (v : X → ℝ)
    (x y : X) : condEnv d A hA v x y ≤ upperEnv d A hA v x - lowerEnv d A hA v y :=
  min_le_right _ _

/-- **The conditional envelope is an envelope.**  The zero diagonal uses `L ≤ U`; the triangle
inequality has four cases, which use the triangle inequality of `d`, the admissibility of the two
McShane envelopes and `L ≤ U`. -/
theorem condEnv_isEnvelope {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) : IsEnvelope (condEnv d A hA v) where
  self x := by
    have h := lowerEnv_le_upperEnv hd A hA v hv x
    unfold condEnv
    rw [hd.self x]
    exact min_eq_left (by linarith)
  triangle x y z := by
    have hU := upperEnv_admissible hd A hA v x y
    have hL := lowerEnv_admissible hd A hA v y z
    have hLU := lowerEnv_le_upperEnv hd A hA v hv y
    have hT := hd.triangle x y z
    unfold condEnv
    rcases min_choice (d x y) (upperEnv d A hA v x - lowerEnv d A hA v y) with h1 | h1 <;>
      rcases min_choice (d y z) (upperEnv d A hA v y - lowerEnv d A hA v z) with h2 | h2 <;>
      rw [h1, h2]
    · exact (min_le_left _ _).trans hT
    · exact (min_le_right _ _).trans (by linarith)
    · exact (min_le_right _ _).trans (by linarith)
    · exact (min_le_right _ _).trans (by linarith)

/-- On the anchors the conditional envelope is the difference of the data. -/
theorem condEnv_eq_of_mem {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) {a b : X} (ha : a ∈ A) (hb : b ∈ A) :
    condEnv d A hA v a b = v a - v b := by
  unfold condEnv
  rw [upperEnv_eq_of_mem hd A hA v hv ha, lowerEnv_eq_of_mem hd A hA v hv hb]
  exact min_eq_right (hv a ha b hb)

/-- **A single evaluation does not change the envelope**: it only fixes the additive constant of
the residual. -/
theorem condEnv_singleton {d : X → X → ℝ} (hd : IsEnvelope d) (a : X) (v : X → ℝ) (x y : X) :
    condEnv d {a} (singleton_nonempty a) v x y = d x y := by
  have h := hd.triangle x a y
  unfold condEnv upperEnv lowerEnv
  rw [Finset.inf'_singleton, Finset.sup'_singleton]
  exact min_eq_left (by linarith)

/-! ### Consistent residuals are the residuals admissible for the conditional envelope -/

/-- A residual that is admissible for `d` and matches the data on the anchors is admissible for
the conditional envelope. -/
theorem admissible_condEnv {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hgv : ∀ a ∈ A, g a = v a) :
    Admissible (condEnv d A hA v) g := by
  intro x y
  have h1 := le_upperEnv hg A hA v hgv x
  have h2 := lowerEnv_le hg A hA v hgv y
  exact le_min (hg x y) (by linarith)

/-- Conversely, a residual that is admissible for the conditional envelope and matches the data
at **one** anchor is admissible for `d` and matches the data on **all** anchors. -/
theorem admissible_of_condEnv {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) {g : X → ℝ}
    (hg : Admissible (condEnv d A hA v) g) {a₀ : X} (ha₀ : a₀ ∈ A) (h₀ : g a₀ = v a₀) :
    Admissible d g ∧ ∀ a ∈ A, g a = v a := by
  refine ⟨fun x y => (hg x y).trans (condEnv_le d A hA v x y), fun a ha => ?_⟩
  have h1 := hg a a₀
  have h2 := hg a₀ a
  rw [condEnv_eq_of_mem hd A hA v hv ha ha₀] at h1
  rw [condEnv_eq_of_mem hd A hA v hv ha₀ ha] at h2
  linarith

/-- **Conditioning = updating the envelope.**  Given one anchor `a₀` at which the residual takes
the recorded value, "admissible for `d` and equal to the data on all anchors" is the same as
"admissible for the conditional envelope". -/
theorem admissible_condEnv_iff {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (g : X → ℝ)
    {a₀ : X} (ha₀ : a₀ ∈ A) (h₀ : g a₀ = v a₀) :
    (Admissible d g ∧ ∀ a ∈ A, g a = v a) ↔ Admissible (condEnv d A hA v) g :=
  ⟨fun h => admissible_condEnv h.1 A hA v h.2,
    fun h => admissible_of_condEnv hd A hA v hv h ha₀ h₀⟩

/-- **Normalisation at an anchor.**  A residual that is admissible for the conditional envelope
becomes, after adding a suitable constant, admissible for `d` and equal to the data on the
anchors.  Together with `admissible_condEnv`: up to an additive constant, the residuals consistent
with the evaluations are exactly the residuals admissible for the conditional envelope. -/
theorem exists_consistent_shift {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) {g : X → ℝ}
    (hg : Admissible (condEnv d A hA v) g) :
    ∃ c : ℝ, Admissible d (fun z => g z + c) ∧ ∀ a ∈ A, g a + c = v a := by
  obtain ⟨a₀, ha₀⟩ := id hA
  have hshift : Admissible (condEnv d A hA v) (fun z => g z + (v a₀ - g a₀)) := by
    intro y z
    have := hg y z
    show g y + (v a₀ - g a₀) - (g z + (v a₀ - g a₀)) ≤ condEnv d A hA v y z
    linarith
  exact ⟨v a₀ - g a₀, admissible_of_condEnv hd A hA v hv hshift ha₀ (add_sub_cancel _ _)⟩

/-! ### Exactness -/

/-- The conditional envelope bounds the differences of every admissible residual that is
consistent with the evaluations (the bound is attained: `condEnv_attained`). -/
theorem sub_le_condEnv {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hgv : ∀ a ∈ A, g a = v a) (x y : X) :
    g x - g y ≤ condEnv d A hA v x y :=
  admissible_condEnv hg A hA v hgv x y

/-- **The conditional envelope is exact.**  For consistent data and every pair `x y` there is a
residual, admissible for `d` and equal to the data on the anchors, with
`g x - g y = condEnv d A hA v x y`.  (The extremal residual is
`g z = max (L z) (c - d x z)` with `c = min (U x) (L y + d x y)`.) -/
theorem condEnv_attained {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (x y : X) :
    ∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧ g x - g y = condEnv d A hA v x y := by
  set c := min (upperEnv d A hA v x) (lowerEnv d A hA v y + d x y) with hc
  have hcU : c ≤ upperEnv d A hA v x := min_le_left _ _
  have hcL : c ≤ lowerEnv d A hA v y + d x y := min_le_right _ _
  have hLc : lowerEnv d A hA v x ≤ c := by
    have h1 := lowerEnv_le_upperEnv hd A hA v hv x
    have h2 := lowerEnv_admissible hd A hA v x y
    exact le_min h1 (by linarith)
  refine ⟨fun z => max (lowerEnv d A hA v z) (c - d x z), ?_, ?_, ?_⟩
  · -- admissible: a maximum of two admissible functions
    intro z w
    have e1 := lowerEnv_admissible hd A hA v z w
    have e2 := hd.triangle x z w
    have m1 := le_max_left (lowerEnv d A hA v w) (c - d x w)
    have m2 := le_max_right (lowerEnv d A hA v w) (c - d x w)
    have e3 : max (lowerEnv d A hA v z) (c - d x z) ≤
        max (lowerEnv d A hA v w) (c - d x w) + d z w :=
      max_le (by linarith) (by linarith)
    show max (lowerEnv d A hA v z) (c - d x z) - max (lowerEnv d A hA v w) (c - d x w) ≤ d z w
    linarith
  · -- agrees with the anchor data
    intro a ha
    have e1 := lowerEnv_eq_of_mem hd A hA v hv ha
    have e2 : upperEnv d A hA v x ≤ v a + d x a := Finset.inf'_le (fun b => v b + d x b) ha
    show max (lowerEnv d A hA v a) (c - d x a) = v a
    rw [e1]
    exact max_eq_left (by linarith)
  · -- the difference between `x` and `y` is the conditional envelope
    have hx : max (lowerEnv d A hA v x) (c - d x x) = c := by
      rw [hd.self x, sub_zero]
      exact max_eq_right hLc
    have hy : max (lowerEnv d A hA v y) (c - d x y) = lowerEnv d A hA v y :=
      max_eq_left (by linarith)
    show max (lowerEnv d A hA v x) (c - d x x) - max (lowerEnv d A hA v y) (c - d x y) =
      condEnv d A hA v x y
    rw [hx, hy, hc, ← min_sub_sub_right, add_sub_cancel_left, min_comm]
    rfl

/-- **The conditional envelope is the exact bound on differences**: it is the greatest value of
`g x - g y` over the admissible residuals that are consistent with the evaluations. -/
theorem condEnv_isGreatest {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (x y : X) :
    IsGreatest {r | ∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧ g x - g y = r}
      (condEnv d A hA v x y) := by
  refine ⟨condEnv_attained hd A hA v hv x y, ?_⟩
  rintro r ⟨g, hg, hgv, rfl⟩
  exact sub_le_condEnv hg A hA v hgv x y

/-- **Tower property: conditioning in stages.**  Let `A ⊆ A'` be two anchor sets and let the data
`v` be consistent on `A'`.  Updating the envelope with the evaluations on `A` and then updating
the result with the evaluations on `A'` gives the same envelope as updating `d` once with the
evaluations on `A'`; for `A' = A` the update is idempotent.  (Both envelopes are exact for the
same class of residuals, `condEnv_isGreatest`.) -/
theorem condEnv_tower {d : X → X → ℝ} (hd : IsEnvelope d) {A A' : Finset X} (hAA' : A ⊆ A')
    (hA : A.Nonempty) (hA' : A'.Nonempty) (v : X → ℝ)
    (hv : ∀ a ∈ A', ∀ b ∈ A', v a - v b ≤ d a b) (x y : X) :
    condEnv (condEnv d A hA v) A' hA' v x y = condEnv d A' hA' v x y := by
  have hvA : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b := fun a ha b hb =>
    hv a (hAA' ha) b (hAA' hb)
  -- the data on `A'` are consistent for the updated envelope
  have hv₁ : ∀ a ∈ A', ∀ b ∈ A', v a - v b ≤ condEnv d A hA v a b := by
    intro a ha b hb
    have hU : v a ≤ upperEnv d A hA v a := by
      unfold upperEnv
      apply Finset.le_inf'
      intro c hc
      have := hv a ha c (hAA' hc)
      linarith
    have hL : lowerEnv d A hA v b ≤ v b := by
      unfold lowerEnv
      apply Finset.sup'_le
      intro c hc
      have := hv c (hAA' hc) b hb
      linarith
    exact le_min (hv a ha b hb) (by linarith)
  -- the two classes of consistent residuals coincide
  have hset : {r | ∃ g, Admissible (condEnv d A hA v) g ∧ (∀ a ∈ A', g a = v a) ∧
        g x - g y = r} =
      {r | ∃ g, Admissible d g ∧ (∀ a ∈ A', g a = v a) ∧ g x - g y = r} := by
    ext r
    constructor
    · rintro ⟨g, hg, hgv, rfl⟩
      exact ⟨g, fun p q => (hg p q).trans (condEnv_le d A hA v p q), hgv, rfl⟩
    · rintro ⟨g, hg, hgv, rfl⟩
      exact ⟨g, admissible_condEnv hg A hA v fun a ha => hgv a (hAA' ha), hgv, rfl⟩
  have h1 := condEnv_isGreatest (condEnv_isEnvelope hd A hA v hvA) A' hA' v hv₁ x y
  rw [hset] at h1
  exact h1.unique (condEnv_isGreatest hd A' hA' v hv x y)

/-! ### The query-model theorems are the envelope theorems for the updated envelope -/

/-- The contact condition for the conditional envelope, unfolded: it is the conjunction of the two
conditions of `robust_minimizer_with_anchors_iff`. -/
theorem contact_condEnv_iff (d : X → X → ℝ) (A : Finset X) (hA : A.Nonempty) (v : X → ℝ)
    (f : X → ℝ) (x : X) :
    (∀ y, f x ≤ f y + condEnv d A hA v y x) ↔
      (∀ y, f x ≤ f y + d y x) ∧
        ∀ y, f x + lowerEnv d A hA v x ≤ f y + upperEnv d A hA v y := by
  constructor
  · intro h
    refine ⟨fun y => ?_, fun y => ?_⟩
    · have h1 := h y
      have h2 := condEnv_le d A hA v y x
      linarith
    · have h1 := h y
      have h2 := condEnv_le_bracket d A hA v y x
      linarith
  · rintro ⟨h1, h2⟩ y
    have e1 := h1 y
    have e2 := h2 y
    unfold condEnv
    rw [← min_add_add_left]
    exact le_min e1 (by linarith)

/-- **Query-model contact theorem, envelope form.**  A configuration `x` can be a minimiser of
`f + g` for *some* admissible residual `g` that agrees with the evaluations iff it lies on the
contact set of the *conditional* envelope: `f x ≤ f y + condEnv d A hA v y x` for all `y`.

The proof is `robust_minimizer_iff` applied to the conditional envelope, together with the
identification of the consistent residuals with the residuals admissible for `condEnv`
(`admissible_condEnv`, and `exists_consistent_shift`, which normalises the residual at one
anchor by adding a constant). -/
theorem robust_minimizer_with_anchors_iff' {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (f : X → ℝ)
    (x : X) :
    (∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧ ∀ y, f x + g x ≤ f y + g y) ↔
      ∀ y, f x ≤ f y + condEnv d A hA v y x := by
  rw [← robust_minimizer_iff (condEnv_isEnvelope hd A hA v hv) f x]
  constructor
  · rintro ⟨g, hg, hgv, hmin⟩
    exact ⟨g, admissible_condEnv hg A hA v hgv, hmin⟩
  · rintro ⟨g, hg, hmin⟩
    obtain ⟨c, hadm, hval⟩ := exists_consistent_shift hd A hA v hv hg
    refine ⟨fun z => g z + c, hadm, hval, fun y => ?_⟩
    have := hmin y
    show f x + (g x + c) ≤ f y + (g y + c)
    linarith

/-- **Sharp-minimum theorem with evaluations.**  A configuration `x` minimises `f + g` for
*every* admissible residual `g` that agrees with the evaluations iff `f` grows at least as fast
as the conditional envelope away from `x`: `condEnv d A hA v x y ≤ f y - f x` for all `y`.  This
is the exact criterion for declaring `x` optimal after the evaluations: no sound rule can certify
more, and a rule that certifies less is not optimal. -/
theorem robust_certified_with_anchors_iff {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (f : X → ℝ)
    (x : X) :
    (∀ g, Admissible d g → (∀ a ∈ A, g a = v a) → ∀ y, f x + g x ≤ f y + g y) ↔
      ∀ y, condEnv d A hA v x y ≤ f y - f x := by
  constructor
  · intro h y
    obtain ⟨g, hg, hgv, hxy⟩ := condEnv_attained hd A hA v hv x y
    have := h g hg hgv y
    linarith
  · intro h g hg hgv y
    have h1 := h y
    have h2 := sub_le_condEnv hg A hA v hgv x y
    linarith

/-! ### Worst-case regret -/

/-- **Regret bound.**  For every admissible residual consistent with the evaluations, the regret
of `x` against `y` is at most `f x - f y + condEnv d A hA v x y`. -/
theorem max_regret_le {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (A : Finset X)
    (hA : A.Nonempty) (v : X → ℝ) (hgv : ∀ a ∈ A, g a = v a) (f : X → ℝ) (x y : X) :
    (f x + g x) - (f y + g y) ≤ f x - f y + condEnv d A hA v x y := by
  have := sub_le_condEnv hg A hA v hgv x y
  linarith

/-- **The regret bound is attained**: for each competitor `y` some admissible residual consistent
with the evaluations has regret exactly `f x - f y + condEnv d A hA v x y`. -/
theorem max_regret_attained {d : X → X → ℝ} (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty)
    (v : X → ℝ) (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (f : X → ℝ) (x y : X) :
    ∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧
      (f x + g x) - (f y + g y) = f x - f y + condEnv d A hA v x y := by
  obtain ⟨g, hg, hgv, hxy⟩ := condEnv_attained hd A hA v hv x y
  exact ⟨g, hg, hgv, by linarith⟩

/-- **Worst-case regret.**  On a finite configuration space, the largest regret
`(f x + g x) - (f y + g y)` of declaring `x` optimal, over all competitors `y` and all admissible
residuals `g` consistent with the evaluations, is `max_y (f x - f y + condEnv d A hA v x y)`. -/
theorem worst_case_regret_isGreatest [Fintype X] [Nonempty X] {d : X → X → ℝ}
    (hd : IsEnvelope d) (A : Finset X) (hA : A.Nonempty) (v : X → ℝ)
    (hv : ∀ a ∈ A, ∀ b ∈ A, v a - v b ≤ d a b) (f : X → ℝ) (x : X) :
    IsGreatest
      {r | ∃ g, Admissible d g ∧ (∀ a ∈ A, g a = v a) ∧ ∃ y, r = (f x + g x) - (f y + g y)}
      (univ.sup' univ_nonempty fun y => f x - f y + condEnv d A hA v x y) := by
  constructor
  · obtain ⟨y, -, hy⟩ := Finset.exists_mem_eq_sup' univ_nonempty
      (fun y => f x - f y + condEnv d A hA v x y)
    obtain ⟨g, hg, hgv, hxy⟩ := max_regret_attained hd A hA v hv f x y
    exact ⟨g, hg, hgv, y, by rw [hy, hxy]⟩
  · rintro r ⟨g, hg, hgv, y, rfl⟩
    exact (max_regret_le hg A hA v hgv f x y).trans
      (Finset.le_sup' (fun y => f x - f y + condEnv d A hA v x y) (mem_univ y))

/-! ### Non-vacuity witnesses -/

/-- **Two-point witness.**  On `Bool` with the discrete envelope of oscillation `1`, the data
`v false = 0`, `v true = 1` on both points are consistent, and the conditional envelope is the
difference of the data: `1` from `true` to `false` and `-1` back.  In particular a conditional
envelope is asymmetric and can be negative. -/
theorem condEnv_bool_witness :
    (∀ a ∈ (univ : Finset Bool), ∀ b ∈ (univ : Finset Bool),
        (if a then (1 : ℝ) else 0) - (if b then (1 : ℝ) else 0) ≤ discreteEnvelope 1 a b) ∧
      condEnv (discreteEnvelope 1) univ univ_nonempty (fun c : Bool => if c then (1 : ℝ) else 0)
        true false = 1 ∧
      condEnv (discreteEnvelope 1) univ univ_nonempty (fun c : Bool => if c then (1 : ℝ) else 0)
        false true = -1 := by
  have hcons : ∀ a ∈ (univ : Finset Bool), ∀ b ∈ (univ : Finset Bool),
      (if a then (1 : ℝ) else 0) - (if b then (1 : ℝ) else 0) ≤ discreteEnvelope 1 a b := by
    intro a _ b _
    cases a <;> cases b <;> simp [discreteEnvelope]
  refine ⟨hcons, ?_, ?_⟩
  · rw [condEnv_eq_of_mem (discreteEnvelope_isEnvelope zero_le_one) univ univ_nonempty
      (fun c : Bool => if c then (1 : ℝ) else 0) hcons (mem_univ true) (mem_univ false)]
    simp
  · rw [condEnv_eq_of_mem (discreteEnvelope_isEnvelope zero_le_one) univ univ_nonempty
      (fun c : Bool => if c then (1 : ℝ) else 0) hcons (mem_univ false) (mem_univ true)]
    simp

/-- **Three-point witness: two evaluations strictly tighten the envelope.**  On `Fin 3` with the
discrete envelope of oscillation `1`, the evaluations `v 0 = 0`, `v 1 = 1` on the anchors `{0, 1}`
are consistent, and the conditional envelope from `0` to the unevaluated point `2` is `0`,
strictly below `d 0 2 = 1`. -/
theorem condEnv_three_point_witness :
    (∀ a ∈ ({0, 1} : Finset (Fin 3)), ∀ b ∈ ({0, 1} : Finset (Fin 3)),
        (![0, 1, 0] : Fin 3 → ℝ) a - (![0, 1, 0] : Fin 3 → ℝ) b ≤ discreteEnvelope 1 a b) ∧
      condEnv (discreteEnvelope 1) {0, 1} (insert_nonempty 0 {1}) ![0, 1, 0] 0 2 = 0 ∧
      discreteEnvelope (1 : ℝ) (0 : Fin 3) 2 = 1 := by
  refine ⟨?_, ?_, ?_⟩
  · intro a _ b _
    fin_cases a <;> fin_cases b <;> simp [discreteEnvelope]
  · simp [condEnv, upperEnv, lowerEnv, discreteEnvelope]
  · simp [discreteEnvelope]

/-- **Three-point witness: certification needs the evaluations.**  In the setting of
`condEnv_three_point_witness` with `f = 0`: every admissible residual with `g 0 = 0`, `g 1 = 1`
is minimal at `0` (by `robust_certified_with_anchors_iff`), although `0` is not optimal for every
admissible residual when the evaluations are ignored. -/
theorem certified_three_point_witness :
    (∀ g : Fin 3 → ℝ, Admissible (discreteEnvelope 1) g → g 0 = 0 → g 1 = 1 →
        ∀ y, g 0 ≤ g y) ∧
      ¬ ∀ g : Fin 3 → ℝ, Admissible (discreteEnvelope 1) g → ∀ y, g 0 ≤ g y := by
  constructor
  · intro g hg h0 h1 y
    have key := (robust_certified_with_anchors_iff (discreteEnvelope_isEnvelope zero_le_one)
      {0, 1} (insert_nonempty 0 {1}) ![0, 1, 0] condEnv_three_point_witness.1 (fun _ => 0) 0).mpr
      (fun y => by fin_cases y <;> simp [condEnv, upperEnv, lowerEnv, discreteEnvelope])
      g hg (fun a ha => by
        rw [Finset.mem_insert, Finset.mem_singleton] at ha
        rcases ha with rfl | rfl <;> simp [h0, h1]) y
    simpa using key
  · intro h
    have h2 : (if (0 : Fin 3) = 0 then (1 : ℝ) else 0) ≤ if (2 : Fin 3) = 0 then (1 : ℝ) else 0 :=
      h (fun i => if i = 0 then 1 else 0)
        (admissible_of_bounds (lo := 0) _ fun i => by split_ifs <;> norm_num) 2
    rw [if_pos rfl, if_neg (by decide)] at h2
    linarith

/-- **Three-point witness: pruning needs the evaluations.**  In the setting of
`condEnv_three_point_witness` with `f = 0`: no admissible residual with `g 0 = 0`, `g 1 = 1` is
minimal at `1` (by `robust_minimizer_with_anchors_iff'`: the contact condition for the conditional
envelope fails at `y = 0`, where `condEnv 0 1 = -1`), although `1` is optimal for some admissible
residual when the evaluations are ignored. -/
theorem pruned_three_point_witness :
    (¬ ∃ g : Fin 3 → ℝ, Admissible (discreteEnvelope 1) g ∧ g 0 = 0 ∧ g 1 = 1 ∧
        ∀ y, g 1 ≤ g y) ∧
      ∃ g : Fin 3 → ℝ, Admissible (discreteEnvelope 1) g ∧ ∀ y, g 1 ≤ g y := by
  constructor
  · rintro ⟨g, hg, h0, h1, hmin⟩
    have hc : condEnv (discreteEnvelope 1) {0, 1} (insert_nonempty 0 {1}) ![0, 1, 0]
        (0 : Fin 3) 1 = -1 := by
      simp [condEnv, upperEnv, lowerEnv, discreteEnvelope]
    have key := (robust_minimizer_with_anchors_iff' (discreteEnvelope_isEnvelope zero_le_one)
      {0, 1} (insert_nonempty 0 {1}) ![0, 1, 0] condEnv_three_point_witness.1 (fun _ => 0) 1).mp
      ⟨g, hg, fun a ha => by
        rw [Finset.mem_insert, Finset.mem_singleton] at ha
        rcases ha with rfl | rfl <;> simp [h0, h1], fun y => by simpa using hmin y⟩ 0
    rw [hc] at key
    linarith
  · exact ⟨fun _ => 0, admissible_of_bounds (lo := 0) _ fun _ => by norm_num, fun _ => le_rfl⟩

end MetricChain
