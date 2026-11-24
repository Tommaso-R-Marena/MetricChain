import Mathlib
import proofs.Frontiers.QueryRefinements

/-!
# Generalised dips, and the two-measure sandwich

Single dips (`dip d g y c`, `QueryLowerBound.lean`) are not the only admissible perturbations
that a correct algorithm for the free energy has to detect.  For **every** function `Φ` that is
Lipschitz for the slack, `Φ x - Φ y ≤ s(x, y)`, the residual lowered by `(c - Φ)₊` is admissible;
single dips are the case `Φ = s(·, y)`.  On product landscapes with three or more states per
site the additional members are needed: the conjecture that single dips are extremal at the
exponential scale is false (theory report §11.10, `DEAD_ENDS.md` D38).  Found by an independent
workstream (`docs/workstreams/A_REPORT.md`); the statements below are its Lemma 1, the
ingredients of its Proposition 2 and the core of its Theorem B, restated in the vocabulary of
this development and connected to the query bounds.

## Generalised dips (any instance)

* `genDip g Φ c` — the residual `g` lowered by `(c - Φ)₊`; `genDip_admissible`,
  `genDip_ne_imp_lt`, `dip_eq_genDip`.
* `softGapOf β f g Φ` — `log Z(f + g) - log Z(f + g + Φ)`, the soft gap of the "centre" `Φ`
  (`softGap_eq_softGapOf`: for `Φ = s(·, y)` it is `softGap`); `sum_exp_genDip`,
  `log_sum_exp_genDip_ge`: the generalised dip raises `log Z` by at least `β c - softGapOf Φ`.
* `genDip_expected_queries_ge`, `genDip_expected_queries_ge_exp_weights` — **every randomised
  algorithm pays the packing price of every family of generalised dips**: if
  `softGapOf (Φ j) + ε < β · r j`, then `(1 - 2δ) ∑ w ≤ E|Q| · max_a ∑_{j : Φ j a < r j} w j`, and in
  exponential-weights form with `∑_j w j · exp (-t (Φ j a - r j))`.

## The two-measure sandwich

* `TwoMeasureBound W Q s β γ` — for every profile `h` with `h y - h x ≤ s x y`:
  `∑ W e^{β h} ≤ exp (β ∑ Q h + γ)`.  For one site and `W = π` this defines the constant
  `γ(Q) = max_Φ [β E_Q Φ - Λ(Φ)]`; `Q = π` is the passive sandwich (Jensen gap).
* `twoMeasureBound_prod`, `twoMeasureBound_pow` — the bound **tensorises**: on `n` sites with the
  additive slack the constant is `n γ`.
* `mass_ge_of_twoMeasureBound`, `product_mass_ge` — hence a set that supports a profile
  `0 ≤ h ≤ H` raising `log Z` by `ε` has `Q`-mass at least `(ε - γ) / (β H)`: above the threshold
  `γ` per site, the detection probability of a sample from `Qⁿ` does not depend on `n`.
* `TwoMeasureLower`, `twoMeasureLower_prod`, `twoMeasureLower_pow`, `product_sandwich` — the
  **reverse** bound `exp (β ∑ Q h + m) ≤ ∑ W e^{β h}` tensorises as well.  With the weights
  `W = e^{-β f₁}` of the known part of one site and `h = -g` this is a sandwich for the partition
  function of **every** admissible residual `g` on `n` sites around a single reference law `Q`,
  with no reference instance: `n m ≤ log Z(f + g) + β E_{Qⁿ} g ≤ n M`, where `m`, `M` are the least
  and the largest value of the tilted site pressure `F_Q(ψ) = log ∑ e^{-β(f₁+ψ)} + β E_Q ψ` over
  the admissible site functions.  Its width per site, minimised over `Q`, is the accuracy
  threshold of the whole class for algorithms without a hint (theory report Theorem 11.28).
-/

namespace MetricChain

open Finset

/-! ### Generalised dips -/

section GenDip

variable {X : Type*}

/-- The residual `g` lowered by `(c - Φ)₊`: a **generalised dip** with centre function `Φ` and
depth parameter `c`. -/
noncomputable def genDip (g Φ : X → ℝ) (c : ℝ) : X → ℝ := fun a => g a - max 0 (c - Φ a)

theorem genDip_le (g Φ : X → ℝ) (c : ℝ) (a : X) : genDip g Φ c a ≤ g a := by
  unfold genDip
  have := le_max_left 0 (c - Φ a)
  linarith

/-- A generalised dip differs from `g` only where `Φ < c`. -/
theorem genDip_ne_imp_lt {g Φ : X → ℝ} {c : ℝ} {a : X} (h : genDip g Φ c a ≠ g a) : Φ a < c := by
  by_contra hge
  apply h
  unfold genDip
  rw [max_eq_left (by linarith [not_lt.mp hge])]
  ring

/-- **Generalised dips are admissible.**  If `Φ` is Lipschitz for the slack of `g`,
`Φ x - Φ y ≤ s(x, y)`, then `g - (c - Φ)₊` is admissible. -/
theorem genDip_admissible {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) {Φ : X → ℝ}
    (hΦ : ∀ x y, Φ x - Φ y ≤ slack d g x y) (c : ℝ) : Admissible d (genDip g Φ c) := by
  intro x y
  have hs : slack d g x y = d x y - g x + g y := rfl
  have h1 := hΦ x y
  have h2 := slack_nonneg hg x y
  unfold genDip
  rcases le_total (c - Φ y) 0 with hy | hy
  · rw [max_eq_left hy]
    have := le_max_left 0 (c - Φ x)
    linarith
  · rw [max_eq_right hy]
    have := le_max_right 0 (c - Φ x)
    linarith

/-- Single dips are the generalised dips whose centre function is a slack distance. -/
theorem dip_eq_genDip (d : X → X → ℝ) (g : X → ℝ) (y : X) (c : ℝ) :
    dip d g y c = genDip g (fun a => slack d g a y) c := by
  funext a
  exact dip_eq_sub d g y c a

/-- Slack distances are Lipschitz for the slack (triangle inequality of the envelope). -/
theorem slack_lipschitz {d : X → X → ℝ} (hd : IsEnvelope d) (g : X → ℝ) (y x x' : X) :
    slack d g x y - slack d g x' y ≤ slack d g x x' := by
  have h := hd.triangle x x' y
  unfold slack
  linarith

variable [Fintype X]

/-- The **soft gap of a centre function** `Φ`: `log Z(f + g) - log Z(f + g + Φ)`. -/
noncomputable def softGapOf (β : ℝ) (f g Φ : X → ℝ) : ℝ :=
  Real.log (∑ x, Real.exp (-β * (f x + g x))) -
    Real.log (∑ x, Real.exp (-β * (f x + g x + Φ x)))

theorem softGap_eq_softGapOf (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (y : X) :
    softGap β d f g y = softGapOf β f g (fun x => slack d g x y) := rfl

/-- The partition function of a generalised dip, exactly. -/
theorem sum_exp_genDip (β : ℝ) (f g Φ : X → ℝ) (c : ℝ) :
    ∑ x, Real.exp (-β * (f x + genDip g Φ c x)) =
      ∑ x, Real.exp (-β * (f x + g x)) * Real.exp (β * max 0 (c - Φ x)) := by
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [← Real.exp_add]
  congr 1
  unfold genDip
  ring

variable [Nonempty X]

/-- **Effect of a generalised dip on the free energy.**  For `β ≥ 0` it raises `log Z` by at
least `β c - softGapOf Φ`. -/
theorem log_sum_exp_genDip_ge (f g Φ : X → ℝ) (c : ℝ) {β : ℝ} (hβ : 0 ≤ β) :
    Real.log (∑ x, Real.exp (-β * (f x + g x))) + (β * c - softGapOf β f g Φ) ≤
      Real.log (∑ x, Real.exp (-β * (f x + genDip g Φ c x))) := by
  have hpos : 0 < ∑ x, Real.exp (-β * (f x + g x + Φ x)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hle : Real.exp (β * c) * ∑ x, Real.exp (-β * (f x + g x + Φ x)) ≤
      ∑ x, Real.exp (-β * (f x + genDip g Φ c x)) := by
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum fun x _ => ?_
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    have h1 := mul_le_mul_of_nonneg_left (le_max_right 0 (c - Φ x)) hβ
    unfold genDip
    nlinarith
  have hlog := Real.log_le_log (mul_pos (Real.exp_pos _) hpos) hle
  rw [Real.log_mul (Real.exp_pos _).ne' hpos.ne', Real.log_exp] at hlog
  unfold softGapOf
  linarith

/-- A generalised dip with `softGapOf Φ + ε < β c` is sensitive for `log Z` at level `ε`. -/
theorem genDip_sensitive (f g Φ : X → ℝ) {c β ε : ℝ} (hβ : 0 ≤ β)
    (hc : softGapOf β f g Φ + ε < β * c) :
    ε < |Real.log (∑ x, Real.exp (-β * (f x + genDip g Φ c x))) -
      Real.log (∑ x, Real.exp (-β * (f x + g x)))| := by
  have h := log_sum_exp_genDip_ge f g Φ c hβ
  have h1 : ε < Real.log (∑ x, Real.exp (-β * (f x + genDip g Φ c x))) -
      Real.log (∑ x, Real.exp (-β * (f x + g x))) := by linarith
  exact lt_of_lt_of_le h1 (le_abs_self _)

variable {Ω : Type*} [Fintype Ω] {J : Type*} [Fintype J]

open Classical in
/-- **Every randomised algorithm pays the packing price of every family of generalised dips.**
Let `Φ j` be functions that are Lipschitz for the slack of `g`, with radii `r j` such that
`softGapOf (Φ j) + ε < β · r j`, and let `w ≥ 0` be weights such that the family members whose
support `{Φ j < r j}` contains a given point have total weight at most `B`.  Then a randomised
algorithm that returns `log Z(f + g)` within `ε / 2` with probability at least `1 - δ` on every
admissible residual makes at least `(1 - 2δ) (∑ w) / B` evaluations on `g` in expectation.  For
`Φ j = s(·, j)` this is `thermal_expected_queries_ge`. -/
theorem genDip_expected_queries_ge {d : X → X → ℝ} (f : X → ℝ) (alg : Ω → QueryAlgorithm X)
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {β ε δ : ℝ} (hβ : 0 ≤ β)
    (hcorr : ∀ g, Admissible d g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) (Φ : J → X → ℝ)
    (hΦ : ∀ j x y, Φ j x - Φ j y ≤ slack d g x y) (r : J → ℝ)
    (hr : ∀ j, softGapOf β f g (Φ j) + ε < β * r j) (w : J → ℝ) (hw : ∀ j, 0 ≤ w j) {B : ℝ}
    (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => Φ j a < r j), w j ≤ B) :
    (1 - 2 * δ) * ∑ j, w j ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B := by
  refine expected_queries_ge_packing (G := Admissible d)
    (Φ := fun g => Real.log (∑ x, Real.exp (-β * (f x + g x)))) alg P hP hP1 hcorr hg
    (fun j => genDip g (Φ j) (r j)) (fun j => genDip_admissible hg (hΦ j) (r j))
    (fun j => genDip_sensitive f g (Φ j) hβ (hr j)) w hw fun a => ?_
  refine le_trans (Finset.sum_le_sum_of_subset_of_nonneg ?_ fun j _ _ => hw j) (hcap a)
  intro j hj
  exact Finset.mem_filter.mpr ⟨mem_univ j, genDip_ne_imp_lt (Finset.mem_filter.mp hj).2⟩

open Classical in
/-- **Exponential-weights form.**  In the situation of `genDip_expected_queries_ge`, for every
`t ≥ 0`: `(1 - 2δ) ∑ w ≤ E|Q| · max_a ∑_j w j · exp (-t (Φ j a - r j))`. -/
theorem genDip_expected_queries_ge_exp_weights {d : X → X → ℝ} (f : X → ℝ)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {β ε δ : ℝ} (hβ : 0 ≤ β)
    (hcorr : ∀ g, Admissible d g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) (Φ : J → X → ℝ)
    (hΦ : ∀ j x y, Φ j x - Φ j y ≤ slack d g x y) (r : J → ℝ)
    (hr : ∀ j, softGapOf β f g (Φ j) + ε < β * r j) {t : ℝ} (ht : 0 ≤ t) (w : J → ℝ)
    (hw : ∀ j, 0 ≤ w j) {B : ℝ}
    (hB : ∀ a, ∑ j, w j * Real.exp (-t * (Φ j a - r j)) ≤ B) :
    (1 - 2 * δ) * ∑ j, w j ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B := by
  refine genDip_expected_queries_ge f alg P hP hP1 hβ hcorr hg Φ hΦ r hr w hw fun a => ?_
  refine le_trans ?_ (hB a)
  calc ∑ j ∈ univ.filter (fun j => Φ j a < r j), w j
      ≤ ∑ j ∈ univ.filter (fun j => Φ j a < r j), w j * Real.exp (-t * (Φ j a - r j)) := by
        refine Finset.sum_le_sum fun j hj => ?_
        have hlt := (Finset.mem_filter.mp hj).2
        have hone : (1 : ℝ) ≤ Real.exp (-t * (Φ j a - r j)) := by
          have h0 : (0 : ℝ) ≤ -t * (Φ j a - r j) := by nlinarith
          calc (1 : ℝ) = Real.exp 0 := Real.exp_zero.symm
            _ ≤ _ := Real.exp_le_exp.mpr h0
        calc w j = w j * 1 := (mul_one _).symm
          _ ≤ _ := mul_le_mul_of_nonneg_left hone (hw j)
    _ ≤ ∑ j, w j * Real.exp (-t * (Φ j a - r j)) :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _)
          fun j _ _ => mul_nonneg (hw j) (Real.exp_pos _).le

open Classical in
/-- **Single dips are a special case** (sanity check and non-vacuity of
`genDip_expected_queries_ge`): with the centre functions `Φ y = s(·, y)`, which are Lipschitz for
the slack by the triangle inequality, the generalised bound is the packing bound for the open
slack balls of radii `r y` with `softGap y + ε < β · r y`. -/
theorem genDip_recovers_dips {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {β ε δ : ℝ} (hβ : 0 ≤ β)
    (hcorr : ∀ g, Admissible d g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) (r : X → ℝ)
    (hr : ∀ y, softGap β d f g y + ε < β * r y) (w : X → ℝ) (hw : ∀ y, 0 ≤ w y) {B : ℝ}
    (hcap : ∀ a, ∑ y ∈ univ.filter (fun y => slack d g a y < r y), w y ≤ B) :
    (1 - 2 * δ) * ∑ y, w y ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B :=
  genDip_expected_queries_ge f alg P hP hP1 hβ hcorr hg (fun y x => slack d g x y)
    (fun y x x' => slack_lipschitz hd g y x x') r hr w hw hcap

end GenDip


/-! ### The two-measure sandwich -/

section TwoMeasure

/-- Effect of a generalised dip in weight form: `e^{βc} ∑ w e^{-βΦ} ≤ ∑ w e^{β (c - Φ)₊}`. -/
theorem weighted_genDip_effect {X : Type*} [Fintype X] (w : X → ℝ) (hw : ∀ x, 0 ≤ w x) (Φ : X → ℝ)
    (c β : ℝ) (hβ : 0 ≤ β) :
    Real.exp (β * c) * ∑ x, w x * Real.exp (-(β * Φ x))
      ≤ ∑ x, w x * Real.exp (β * max (c - Φ x) 0) := by
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro x _
  have h1 : Real.exp (β * c) * (w x * Real.exp (-(β * Φ x))) = w x * Real.exp (β * (c - Φ x)) := by
    rw [mul_sub, sub_eq_add_neg, Real.exp_add]; ring
  rw [h1]
  apply mul_le_mul_of_nonneg_left _ (hw x)
  apply Real.exp_le_exp.mpr
  exact mul_le_mul_of_nonneg_left (le_max_left _ _) hβ

variable {S T : Type*} [Fintype S] [Fintype T]

/-- The two-measure bound of a site: for every admissible profile `h` (`h b - h a ≤ s a b`),
`∑ π e^{β h} ≤ exp (β ∑ Q h + γ)`. -/
def TwoMeasureBound (π Q : S → ℝ) (s : S → S → ℝ) (β γ : ℝ) : Prop :=
  ∀ h : S → ℝ, (∀ a b, h b - h a ≤ s a b) →
    ∑ a, π a * Real.exp (β * h a) ≤ Real.exp (β * ∑ a, Q a * h a + γ)

/-- **Tensorisation with two measures**: if two sites satisfy the two-measure bound, so does their
product with the additive slack, with the sum of the constants.  (Condition on the second
coordinate, then apply the first bound to the `Q'`-averaged profile.) -/
theorem twoMeasureBound_prod (π Q : S → ℝ) (π' Q' : T → ℝ) (s : S → S → ℝ) (s' : T → T → ℝ)
    (β γ γ' : ℝ) (hπ : ∀ a, 0 ≤ π a) (hQ' : ∀ b, 0 ≤ Q' b) (hQ'1 : ∑ b, Q' b = 1)
    (hs0 : ∀ a, s a a = 0) (hs'0 : ∀ b, s' b b = 0)
    (h1 : TwoMeasureBound π Q s β γ) (h2 : TwoMeasureBound π' Q' s' β γ') :
    TwoMeasureBound (fun x : S × T => π x.1 * π' x.2) (fun x : S × T => Q x.1 * Q' x.2)
      (fun x y => s x.1 y.1 + s' x.2 y.2) β (γ + γ') := by
  intro h hh
  -- slices in the second coordinate are admissible on `T`
  have hslice : ∀ a : S,
      ∑ b, π' b * Real.exp (β * h (a, b)) ≤ Real.exp (β * ∑ b, Q' b * h (a, b) + γ') := by
    intro a
    apply h2 (fun b => h (a, b))
    intro b b'
    have := hh (a, b) (a, b')
    simp only [hs0, zero_add] at this
    exact this
  -- the averaged profile is admissible on `S`
  have hbar_adm : ∀ a a', (∑ b, Q' b * h (a', b)) - (∑ b, Q' b * h (a, b)) ≤ s a a' := by
    intro a a'
    have e : (∑ b, Q' b * h (a', b)) - (∑ b, Q' b * h (a, b))
        = ∑ b, Q' b * (h (a', b) - h (a, b)) := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro b _
      ring
    rw [e]
    calc ∑ b, Q' b * (h (a', b) - h (a, b)) ≤ ∑ b, Q' b * s a a' := by
          apply Finset.sum_le_sum
          intro b _
          apply mul_le_mul_of_nonneg_left _ (hQ' b)
          have := hh (a, b) (a', b)
          simp only [hs'0, add_zero] at this
          exact this
      _ = s a a' := by rw [← Finset.sum_mul, hQ'1, one_mul]
  have hmain := h1 (fun a => ∑ b, Q' b * h (a, b)) hbar_adm
  have eQ : ∑ x : S × T, Q x.1 * Q' x.2 * h x = ∑ a, Q a * ∑ b, Q' b * h (a, b) := by
    rw [Fintype.sum_prod_type]
    apply Finset.sum_congr rfl
    intro a _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro b _
    ring
  show ∑ x : S × T, π x.1 * π' x.2 * Real.exp (β * h x)
      ≤ Real.exp (β * ∑ x : S × T, Q x.1 * Q' x.2 * h x + (γ + γ'))
  calc ∑ x : S × T, π x.1 * π' x.2 * Real.exp (β * h x)
      = ∑ a, π a * ∑ b, π' b * Real.exp (β * h (a, b)) := by
        rw [Fintype.sum_prod_type]
        apply Finset.sum_congr rfl
        intro a _
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro b _
        ring
    _ ≤ ∑ a, π a * Real.exp (β * ∑ b, Q' b * h (a, b) + γ') := by
        apply Finset.sum_le_sum
        intro a _
        exact mul_le_mul_of_nonneg_left (hslice a) (hπ a)
    _ = Real.exp γ' * ∑ a, π a * Real.exp (β * ∑ b, Q' b * h (a, b)) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro a _
        rw [Real.exp_add]; ring
    _ ≤ Real.exp γ' * Real.exp (β * ∑ a, Q a * ∑ b, Q' b * h (a, b) + γ) := by
        exact mul_le_mul_of_nonneg_left hmain (Real.exp_pos _).le
    _ = Real.exp (β * ∑ x : S × T, Q x.1 * Q' x.2 * h x + (γ + γ')) := by
        rw [← Real.exp_add, eQ]
        congr 1
        ring


/-! #### `n` identical sites -/

/-- `Pw S n = S × (S × ⋯ × Unit)`: the product of `n` copies of the site. -/
def Pw (S : Type) : ℕ → Type
  | 0 => Unit
  | n + 1 => S × Pw S n

instance Pw.fintype (S : Type) [Fintype S] : (n : ℕ) → Fintype (Pw S n)
  | 0 => (inferInstance : Fintype Unit)
  | n + 1 => @instFintypeProd S (Pw S n) _ (Pw.fintype S n)

/-- product weights -/
def prodW {S : Type} (π : S → ℝ) : (n : ℕ) → Pw S n → ℝ
  | 0, _ => 1
  | n + 1, x => π x.1 * prodW π n x.2

/-- additive slack -/
def sumS {S : Type} (s : S → S → ℝ) : (n : ℕ) → Pw S n → Pw S n → ℝ
  | 0, _, _ => 0
  | n + 1, x, y => s x.1 y.1 + sumS s n x.2 y.2

theorem prodW_nonneg {S : Type} (Q : S → ℝ) (hQ : ∀ a, 0 ≤ Q a) :
    ∀ (n : ℕ) (x : Pw S n), 0 ≤ prodW Q n x
  | 0, _ => zero_le_one
  | n + 1, x => mul_nonneg (hQ x.1) (prodW_nonneg Q hQ n x.2)

theorem sumS_self {S : Type} (s : S → S → ℝ) (hs0 : ∀ a, s a a = 0) :
    ∀ (n : ℕ) (x : Pw S n), sumS s n x x = 0
  | 0, _ => rfl
  | n + 1, x => by
      show s x.1 x.1 + sumS s n x.2 x.2 = 0
      rw [hs0, sumS_self s hs0 n x.2, add_zero]

theorem prodW_sum {S : Type} [Fintype S] (Q : S → ℝ) (hQ1 : ∑ a, Q a = 1) :
    ∀ n : ℕ, ∑ x : Pw S n, prodW Q n x = 1
  | 0 => by
      show ∑ _x : Unit, (1 : ℝ) = 1
      simp
  | n + 1 => by
      show ∑ x : S × Pw S n, Q x.1 * prodW Q n x.2 = 1
      rw [Fintype.sum_prod_type]
      have : ∀ a : S, ∑ b : Pw S n, Q a * prodW Q n b = Q a := by
        intro a
        rw [← Finset.mul_sum, prodW_sum Q hQ1 n, mul_one]
      simp only [this, hQ1]

/-- **The two-measure bound tensorises**: on `n` identical sites, with product weights and the
additive slack, the constant is `n γ`. -/
theorem twoMeasureBound_pow {S : Type} [Fintype S] (π Q : S → ℝ) (s : S → S → ℝ) (β γ : ℝ)
    (hπ : ∀ a, 0 ≤ π a) (hQ : ∀ a, 0 ≤ Q a) (hQ1 : ∑ a, Q a = 1) (hs0 : ∀ a, s a a = 0)
    (h1 : TwoMeasureBound π Q s β γ) :
    ∀ n : ℕ, TwoMeasureBound (prodW π n) (prodW Q n) (sumS s n) β (n * γ)
  | 0 => by
      intro h _
      show ∑ x : Unit, (1 : ℝ) * Real.exp (β * h x)
          ≤ Real.exp (β * ∑ x : Unit, (1 : ℝ) * h x + ((0 : ℕ) : ℝ) * γ)
      simp
  | n + 1 => by
      intro h hh
      have key := twoMeasureBound_prod (S := S) (T := Pw S n) π Q (prodW π n) (prodW Q n) s
        (sumS s n) β γ (n * γ) hπ (prodW_nonneg Q hQ n) (prodW_sum Q hQ1 n) hs0
        (sumS_self s hs0 n) h1 (twoMeasureBound_pow π Q s β γ hπ hQ hQ1 hs0 h1 n) h hh
      have e : ((n + 1 : ℕ) : ℝ) * γ = γ + n * γ := by push_cast; ring
      rw [e]
      exact key

/-- **Hitting bound**: under the two-measure bound, a set `D` that supports a profile `0 ≤ h ≤ H`
with `∑ π e^{β h} ≥ e^ε` has `Q`-mass at least `(ε - γ)/(β H)`. -/
theorem mass_ge_of_twoMeasureBound {X : Type} [Fintype X] (π Q : X → ℝ) (s : X → X → ℝ)
    (β γ H ε : ℝ) (hβ : 0 < β) (hH : 0 < H) (hQ : ∀ x, 0 ≤ Q x)
    (hb : TwoMeasureBound π Q s β γ) (D : Finset X) (h : X → ℝ)
    (hadm : ∀ a b, h b - h a ≤ s a b) (h0 : ∀ x, x ∉ D → h x = 0) (hH' : ∀ x, h x ≤ H)
    (hsens : Real.exp ε ≤ ∑ x, π x * Real.exp (β * h x)) :
    (ε - γ) / (β * H) ≤ ∑ x ∈ D, Q x := by
  have h2 := le_trans hsens (hb h hadm)
  have h3 : ε ≤ β * ∑ x, Q x * h x + γ := Real.exp_le_exp.mp h2
  have h4 : ∑ x, Q x * h x ≤ H * ∑ x ∈ D, Q x := by
    have e1 : ∑ x, Q x * h x = ∑ x ∈ D, Q x * h x := by
      symm
      apply Finset.sum_subset (Finset.subset_univ D)
      intro x _ hx
      rw [h0 x hx, mul_zero]
    rw [e1, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro x _
    have := mul_le_mul_of_nonneg_left (hH' x) (hQ x)
    linarith
  have h5 : ε - γ ≤ (∑ x ∈ D, Q x) * (β * H) := by
    have := mul_le_mul_of_nonneg_left h4 hβ.le
    nlinarith
  exact (div_le_iff₀ (mul_pos hβ hH)).mpr h5

/-- **Dimension-free hitting bound**: on `n` identical sites, every set `D` that supports an
admissible profile `0 ≤ h ≤ H` with `∑ πⁿ e^{β h} ≥ e^ε` has `Qⁿ(D) ≥ (ε - n γ)/(β H)`.  With
`H = n · s_max` and `ε = n ε₁` the bound is `(ε₁ - γ)/(β s_max)`, independent of `n`. -/
theorem product_mass_ge {S : Type} [Fintype S] (π Q : S → ℝ) (s : S → S → ℝ) (β γ H ε : ℝ)
    (hβ : 0 < β) (hH : 0 < H) (hπ : ∀ a, 0 ≤ π a) (hQ : ∀ a, 0 ≤ Q a) (hQ1 : ∑ a, Q a = 1)
    (hs0 : ∀ a, s a a = 0) (h1 : TwoMeasureBound π Q s β γ) (n : ℕ)
    (D : Finset (Pw S n)) (h : Pw S n → ℝ)
    (hadm : ∀ a b, h b - h a ≤ sumS s n a b) (h0 : ∀ x, x ∉ D → h x = 0) (hH' : ∀ x, h x ≤ H)
    (hsens : Real.exp ε ≤ ∑ x, prodW π n x * Real.exp (β * h x)) :
    (ε - n * γ) / (β * H) ≤ ∑ x ∈ D, prodW Q n x :=
  mass_ge_of_twoMeasureBound (prodW π n) (prodW Q n) (sumS s n) β (n * γ) H ε hβ hH
    (prodW_nonneg Q hQ n) (twoMeasureBound_pow π Q s β γ hπ hQ hQ1 hs0 h1 n) D h hadm h0 hH' hsens

/-! #### Generalised dips on `n` sites: the two ingredients of the every-`n` lower bound

`F` indexes the site functions ("centres"), `σ φ a` is the normalised distortion
`φ(a) - Λ(φ)/β`; a tuple `φ⃗ : Pw F n` defines the additive function `sumSig σ n φ⃗`.  With
`genDip_expected_queries_ge` (weights `M^{⊗n}`, radius `c`, `B = e^{tc} ρⁿ`) the two lemmas
`genDip_product_effect` and `detect_weight_le` give: every randomised algorithm makes at least
`(1 - 2δ) e^{-tc} ρ^{-n}` evaluations at the product instance, for every `n` (the identification
of `Pw S n` with an instance of the envelope class is not formalised). -/

/-- the additive function `x ↦ ∑ᵢ σ (φᵢ) (xᵢ)` -/
def sumSig {F S : Type} (σ : F → S → ℝ) : (n : ℕ) → Pw F n → Pw S n → ℝ
  | 0, _, _ => 0
  | n + 1, φ, x => σ φ.1 x.1 + sumSig σ n φ.2 x.2

/-- an additive function with site-Lipschitz components is Lipschitz for the additive slack -/
theorem sumSig_lipschitz {F S : Type} (σ : F → S → ℝ) (s : S → S → ℝ)
    (hσ : ∀ φ a b, σ φ a - σ φ b ≤ s a b) :
    ∀ (n : ℕ) (φ : Pw F n) (x y : Pw S n), sumSig σ n φ x - sumSig σ n φ y ≤ sumS s n x y
  | 0, _, _, _ => by
      show (0 : ℝ) - 0 ≤ 0
      norm_num
  | n + 1, φ, x, y => by
      show (σ φ.1 x.1 + sumSig σ n φ.2 x.2) - (σ φ.1 y.1 + sumSig σ n φ.2 y.2)
          ≤ s x.1 y.1 + sumS s n x.2 y.2
      have h1 := hσ φ.1 x.1 y.1
      have h2 := sumSig_lipschitz σ s hσ n φ.2 x.2 y.2
      linarith

theorem sumS_nonneg {S : Type} (s : S → S → ℝ) (hs : ∀ a b, 0 ≤ s a b) :
    ∀ (n : ℕ) (x y : Pw S n), 0 ≤ sumS s n x y
  | 0, _, _ => le_refl _
  | n + 1, x, y => add_nonneg (hs x.1 y.1) (sumS_nonneg s hs n x.2 y.2)

/-- product formula: if every site function is normalised, `∑ₐ π a e^{-β σ φ a} = 1`, then
`∑ₓ πⁿ(x) e^{-β Φ(x)} = 1` for the additive function `Φ = sumSig σ n φ⃗`. -/
theorem normalised_sum {F S : Type} [Fintype S] (π : S → ℝ) (σ : F → S → ℝ) (β : ℝ)
    (hnorm : ∀ φ, ∑ a, π a * Real.exp (-(β * σ φ a)) = 1) :
    ∀ (n : ℕ) (φ : Pw F n), ∑ x : Pw S n, prodW π n x * Real.exp (-(β * sumSig σ n φ x)) = 1
  | 0, _ => by
      show ∑ _x : Unit, (1 : ℝ) * Real.exp (-(β * 0)) = 1
      simp
  | n + 1, φ => by
      show ∑ x : S × Pw S n, π x.1 * prodW π n x.2
          * Real.exp (-(β * (σ φ.1 x.1 + sumSig σ n φ.2 x.2))) = 1
      rw [Fintype.sum_prod_type]
      have e : ∀ a : S, ∑ b : Pw S n, π a * prodW π n b
          * Real.exp (-(β * (σ φ.1 a + sumSig σ n φ.2 b)))
          = π a * Real.exp (-(β * σ φ.1 a)) := by
        intro a
        have e2 : ∀ b : Pw S n, π a * prodW π n b * Real.exp (-(β * (σ φ.1 a + sumSig σ n φ.2 b)))
            = π a * Real.exp (-(β * σ φ.1 a)) * (prodW π n b * Real.exp (-(β * sumSig σ n φ.2 b))) := by
          intro b
          rw [mul_add, neg_add, Real.exp_add]; ring
        simp only [e2]
        rw [← Finset.mul_sum, normalised_sum π σ β hnorm n φ.2, mul_one]
      simp only [e]
      exact hnorm φ.1

/-- **Every generalised dip at depth `c` is sensitive**: with normalised site functions it
multiplies `Z` by at least `e^{βc}`. -/
theorem genDip_product_effect {F S : Type} [Fintype S] (π : S → ℝ) (hπ : ∀ a, 0 ≤ π a)
    (σ : F → S → ℝ) (β c : ℝ) (hβ : 0 ≤ β)
    (hnorm : ∀ φ, ∑ a, π a * Real.exp (-(β * σ φ a)) = 1) (n : ℕ) (φ : Pw F n) :
    Real.exp (β * c)
      ≤ ∑ x : Pw S n, prodW π n x * Real.exp (β * max (c - sumSig σ n φ x) 0) := by
  have h := weighted_genDip_effect (prodW π n) (prodW_nonneg π hπ n) (sumSig σ n φ) c β hβ
  rw [normalised_sum π σ β hnorm n φ, mul_one] at h
  exact h

/-- exponential-moment product formula for the random centre `φ⃗ ∼ M^{⊗n}` -/
theorem weighted_exp_le {F S : Type} [Fintype F] (σ : F → S → ℝ) (M : F → ℝ)
    (hM : ∀ φ, 0 ≤ M φ) (t ρ : ℝ) (hρ : ∀ a, ∑ φ, M φ * Real.exp (-(t * σ φ a)) ≤ ρ) :
    ∀ (n : ℕ) (x : Pw S n),
      ∑ φ : Pw F n, prodW M n φ * Real.exp (-(t * sumSig σ n φ x)) ≤ ρ ^ n
  | 0, _ => by
      show ∑ _φ : Unit, (1 : ℝ) * Real.exp (-(t * 0)) ≤ ρ ^ 0
      simp
  | n + 1, x => by
      show ∑ φ : F × Pw F n, M φ.1 * prodW M n φ.2
          * Real.exp (-(t * (σ φ.1 x.1 + sumSig σ n φ.2 x.2))) ≤ ρ ^ (n + 1)
      rw [Fintype.sum_prod_type]
      have ih := weighted_exp_le σ M hM t ρ hρ n x.2
      have e : ∀ a : F, ∑ b : Pw F n, M a * prodW M n b
          * Real.exp (-(t * (σ a x.1 + sumSig σ n b x.2)))
          = M a * Real.exp (-(t * σ a x.1))
            * ∑ b : Pw F n, prodW M n b * Real.exp (-(t * sumSig σ n b x.2)) := by
        intro a
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro b _
        rw [mul_add, neg_add, Real.exp_add]; ring
      simp only [e]
      rw [← Finset.sum_mul]
      have hρ0 : 0 ≤ ∑ a, M a * Real.exp (-(t * σ a x.1)) :=
        Finset.sum_nonneg (fun a _ => mul_nonneg (hM a) (Real.exp_pos _).le)
      have hs0 : 0 ≤ ∑ b : Pw F n, prodW M n b * Real.exp (-(t * sumSig σ n b x.2)) :=
        Finset.sum_nonneg (fun b _ => mul_nonneg (prodW_nonneg M hM n b) (Real.exp_pos _).le)
      calc (∑ a, M a * Real.exp (-(t * σ a x.1)))
            * ∑ b : Pw F n, prodW M n b * Real.exp (-(t * sumSig σ n b x.2))
          ≤ ρ * ρ ^ n := mul_le_mul (hρ x.1) ih hs0 (le_trans hρ0 (hρ x.1))
        _ = ρ ^ (n + 1) := by ring

/-- **The packing estimate**: a fixed point `x` lies in the supports `{Φ < c}` of generalised dips
with centres `φ⃗` of total `M^{⊗n}`-weight at most `e^{tc} ρⁿ`, whenever
`∑_φ M φ · e^{-t σ φ a} ≤ ρ` for every letter `a` (Markov's inequality and independence). -/
theorem detect_weight_le {F S : Type} [Fintype F] (σ : F → S → ℝ) (M : F → ℝ)
    (hM : ∀ φ, 0 ≤ M φ) (t ρ c : ℝ) (ht : 0 ≤ t)
    (hρ : ∀ a, ∑ φ, M φ * Real.exp (-(t * σ φ a)) ≤ ρ) (n : ℕ) (x : Pw S n) :
    ∑ φ : Pw F n, (if sumSig σ n φ x < c then prodW M n φ else 0) ≤ Real.exp (t * c) * ρ ^ n := by
  have h1 : ∀ φ : Pw F n, (if sumSig σ n φ x < c then prodW M n φ else 0)
      ≤ Real.exp (t * c) * (prodW M n φ * Real.exp (-(t * sumSig σ n φ x))) := by
    intro φ
    have hw := prodW_nonneg M hM n φ
    have e : Real.exp (t * c) * (prodW M n φ * Real.exp (-(t * sumSig σ n φ x)))
        = prodW M n φ * Real.exp (t * (c - sumSig σ n φ x)) := by
      rw [mul_sub, sub_eq_add_neg, Real.exp_add]; ring
    rw [e]
    split_ifs with hlt
    · have : (1 : ℝ) ≤ Real.exp (t * (c - sumSig σ n φ x)) := by
        rw [← Real.exp_zero]
        apply Real.exp_le_exp.mpr
        apply mul_nonneg ht
        linarith
      calc prodW M n φ = prodW M n φ * 1 := (mul_one _).symm
        _ ≤ prodW M n φ * Real.exp (t * (c - sumSig σ n φ x)) :=
            mul_le_mul_of_nonneg_left this hw
    · exact mul_nonneg hw (Real.exp_pos _).le
  calc ∑ φ : Pw F n, (if sumSig σ n φ x < c then prodW M n φ else 0)
      ≤ ∑ φ : Pw F n, Real.exp (t * c) * (prodW M n φ * Real.exp (-(t * sumSig σ n φ x))) :=
        Finset.sum_le_sum (fun φ _ => h1 φ)
    _ = Real.exp (t * c) * ∑ φ : Pw F n, prodW M n φ * Real.exp (-(t * sumSig σ n φ x)) := by
        rw [Finset.mul_sum]
    _ ≤ Real.exp (t * c) * ρ ^ n :=
        mul_le_mul_of_nonneg_left (weighted_exp_le σ M hM t ρ hρ n x) (Real.exp_pos _).le

/-! #### The reverse bound, and the sandwich around one reference law -/

/-- The reverse two-measure bound of a site: for every admissible profile `h`,
`exp (β ∑ Q h + m) ≤ ∑ π e^{β h}`. -/
def TwoMeasureLower {S : Type*} [Fintype S] (π Q : S → ℝ) (s : S → S → ℝ) (β m : ℝ) : Prop :=
  ∀ h : S → ℝ, (∀ a b, h b - h a ≤ s a b) →
    Real.exp (β * ∑ a, Q a * h a + m) ≤ ∑ a, π a * Real.exp (β * h a)

/-- **Tensorisation of the reverse bound.** -/
theorem twoMeasureLower_prod (π Q : S → ℝ) (π' Q' : T → ℝ) (s : S → S → ℝ) (s' : T → T → ℝ)
    (β m m' : ℝ) (hπ : ∀ a, 0 ≤ π a) (hQ' : ∀ b, 0 ≤ Q' b) (hQ'1 : ∑ b, Q' b = 1)
    (hs0 : ∀ a, s a a = 0) (hs'0 : ∀ b, s' b b = 0)
    (h1 : TwoMeasureLower π Q s β m) (h2 : TwoMeasureLower π' Q' s' β m') :
    TwoMeasureLower (fun x : S × T => π x.1 * π' x.2) (fun x : S × T => Q x.1 * Q' x.2)
      (fun x y => s x.1 y.1 + s' x.2 y.2) β (m + m') := by
  intro h hh
  have hslice : ∀ a : S,
      Real.exp (β * ∑ b, Q' b * h (a, b) + m') ≤ ∑ b, π' b * Real.exp (β * h (a, b)) := by
    intro a
    apply h2 (fun b => h (a, b))
    intro b b'
    have := hh (a, b) (a, b')
    simp only [hs0, zero_add] at this
    exact this
  have hbar_adm : ∀ a a', (∑ b, Q' b * h (a', b)) - (∑ b, Q' b * h (a, b)) ≤ s a a' := by
    intro a a'
    have e : (∑ b, Q' b * h (a', b)) - (∑ b, Q' b * h (a, b))
        = ∑ b, Q' b * (h (a', b) - h (a, b)) := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro b _
      ring
    rw [e]
    calc ∑ b, Q' b * (h (a', b) - h (a, b)) ≤ ∑ b, Q' b * s a a' := by
          apply Finset.sum_le_sum
          intro b _
          apply mul_le_mul_of_nonneg_left _ (hQ' b)
          have := hh (a, b) (a', b)
          simp only [hs'0, add_zero] at this
          exact this
      _ = s a a' := by rw [← Finset.sum_mul, hQ'1, one_mul]
  have hmain := h1 (fun a => ∑ b, Q' b * h (a, b)) hbar_adm
  have eQ : ∑ x : S × T, Q x.1 * Q' x.2 * h x = ∑ a, Q a * ∑ b, Q' b * h (a, b) := by
    rw [Fintype.sum_prod_type]
    apply Finset.sum_congr rfl
    intro a _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro b _
    ring
  show Real.exp (β * ∑ x : S × T, Q x.1 * Q' x.2 * h x + (m + m'))
      ≤ ∑ x : S × T, π x.1 * π' x.2 * Real.exp (β * h x)
  calc Real.exp (β * ∑ x : S × T, Q x.1 * Q' x.2 * h x + (m + m'))
      = Real.exp m' * Real.exp (β * ∑ a, Q a * ∑ b, Q' b * h (a, b) + m) := by
        rw [← Real.exp_add, eQ]
        congr 1
        ring
    _ ≤ Real.exp m' * ∑ a, π a * Real.exp (β * ∑ b, Q' b * h (a, b)) :=
        mul_le_mul_of_nonneg_left hmain (Real.exp_pos _).le
    _ = ∑ a, π a * Real.exp (β * ∑ b, Q' b * h (a, b) + m') := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro a _
        rw [Real.exp_add]
        ring
    _ ≤ ∑ a, π a * ∑ b, π' b * Real.exp (β * h (a, b)) := by
        apply Finset.sum_le_sum
        intro a _
        exact mul_le_mul_of_nonneg_left (hslice a) (hπ a)
    _ = ∑ x : S × T, π x.1 * π' x.2 * Real.exp (β * h x) := by
        rw [Fintype.sum_prod_type]
        apply Finset.sum_congr rfl
        intro a _
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro b _
        ring

/-- **The reverse bound on `n` identical sites**, with constant `n m`. -/
theorem twoMeasureLower_pow {S : Type} [Fintype S] (π Q : S → ℝ) (s : S → S → ℝ) (β m : ℝ)
    (hπ : ∀ a, 0 ≤ π a) (hQ : ∀ a, 0 ≤ Q a) (hQ1 : ∑ a, Q a = 1) (hs0 : ∀ a, s a a = 0)
    (h1 : TwoMeasureLower π Q s β m) :
    ∀ n : ℕ, TwoMeasureLower (prodW π n) (prodW Q n) (sumS s n) β (n * m)
  | 0 => by
      intro h _
      show Real.exp (β * ∑ x : Unit, (1 : ℝ) * h x + ((0 : ℕ) : ℝ) * m)
          ≤ ∑ x : Unit, (1 : ℝ) * Real.exp (β * h x)
      simp
  | n + 1 => by
      intro h hh
      have key := twoMeasureLower_prod (S := S) (T := Pw S n) π Q (prodW π n) (prodW Q n) s
        (sumS s n) β m (n * m) hπ (prodW_nonneg Q hQ n) (prodW_sum Q hQ1 n) hs0
        (sumS_self s hs0 n) h1 (twoMeasureLower_pow π Q s β m hπ hQ hQ1 hs0 h1 n) h hh
      have e : ((n + 1 : ℕ) : ℝ) * m = m + n * m := by push_cast; ring
      rw [e]
      exact key

/-- **A sandwich around one reference law, for every admissible residual on `n` sites.**  Let the
site weights `W ≥ 0` (for instance `W a = exp (-β f₁ a)`, the known part of one site) and a
reference law `Q` satisfy both bounds on one site, with constants `m ≤ M`.  Then every profile
`h` on `n` sites that is admissible for the additive envelope (for instance `h = -g`) satisfies
`exp (β E_{Qⁿ} h + n m) ≤ ∑ Wⁿ e^{β h} ≤ exp (β E_{Qⁿ} h + n M)`.  No reference instance and no
hint are involved: the reference law is fixed in advance. -/
theorem product_sandwich {S : Type} [Fintype S] (W Q : S → ℝ) (s : S → S → ℝ) (β m M : ℝ)
    (hW : ∀ a, 0 ≤ W a) (hQ : ∀ a, 0 ≤ Q a) (hQ1 : ∑ a, Q a = 1) (hs0 : ∀ a, s a a = 0)
    (hlo : TwoMeasureLower W Q s β m) (hhi : TwoMeasureBound W Q s β M) (n : ℕ)
    (h : Pw S n → ℝ) (hadm : ∀ a b, h b - h a ≤ sumS s n a b) :
    Real.exp (β * ∑ x, prodW Q n x * h x + n * m) ≤ ∑ x, prodW W n x * Real.exp (β * h x) ∧
      ∑ x, prodW W n x * Real.exp (β * h x) ≤ Real.exp (β * ∑ x, prodW Q n x * h x + n * M) :=
  ⟨twoMeasureLower_pow W Q s β m hW hQ hQ1 hs0 hlo n h hadm,
    twoMeasureBound_pow W Q s β M hW hQ hQ1 hs0 hhi n h hadm⟩

end TwoMeasure

end MetricChain
