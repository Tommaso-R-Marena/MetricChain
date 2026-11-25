import Mathlib

/-!
# The level recursion of algorithms without a hint converges to the hinted exponent

Theory report §11.18.  A two-level algorithm that uses, on the fibres of a splitting of the
coordinates, a bracket procedure with exponent function `T`, has the exponent function

  `R[T](g) = inf_{φ, β} sup_{γ ≥ β} [ min(γ, φ θna((g - β)/φ)) + (1 - φ) T(γ/(1 - φ)) ]`,

where `θna` is the exponent of non-adaptive sampling.  This file contains the analysis of that
recursion and nothing about algorithms:

* `StepLE θna T T'` says `T' ≤ R[T]` without mentioning suprema;
* `HintPair` collects what is used about `θna` and the hinted exponent `θh`: the identity
  `θna (e + θh e) = θh e`, monotonicity of `e + θh e`, and continuity and boundedness of `θna`;
* `superSolution_le_hint`: a nonincreasing bounded `T` with `T ≤ R[T]` is at most `θh`;
* `iterates_lt_hint_add`: for a sequence with `T (k+1) ≤ R[T k]`, `T (k+1) ≤ T k`, the values
  `T k g` come within any `η > 0` of `θh g`;
* `klBin_shift`: the identity between the two relative entropies from which
  `θna (e + θh e) = θh e` follows on the cube;
* `gaussPair`: the hypotheses hold for the small-slope limit `θna x = (1 - √x)²`,
  `θh e = (1 - e)²/4`, so the theorems are not vacuous; `gauss_hint_superSolution`: in that
  limit the hinted exponent itself satisfies `T ≤ R[T]`, so it is a fixed point of the
  recursion and a positive function to which `superSolution_le_hint` applies.

The second part (`namespace LayerCake`) is the deterministic core of the two-level bracket of
Theorem 11.52: Markov's inequality for the lower end (`level_mul_exceed_le_mean`), the
layer-cake bound for the upper end (`mean_le_layer_cake`, `mean_le_upper`), the width of the
bracket (`upper_le_width`), the fact that fibre averages of a Lipschitz function are
Lipschitz (`fibre_sum_le`), and the two algebraic inequalities behind the cost: the expected
number of sampled points close to a level (`close_points_bound`) and the growth of the
negligibility threshold (`negligibility_threshold_le`).  **Not formalised:** the algorithm
itself, its probabilistic events and the summation of its cost — Theorem 11.52 as a statement
about the number of evaluations is a paper proof — nor Harper's theorem, nor that the
functions of the cube satisfy `HintPair` (elementary calculus from `klBin_shift`).
-/

namespace MetricChain
namespace HintRecursion

open Set

/-- `T'` is at most the two-level bound built on the inner exponent `T`: for all parameters
`φ ∈ (0,1)`, `β ∈ (0,g)`, every upper bound of
`γ ↦ min γ (φ θna((g-β)/φ)) + (1-φ) T(γ/(1-φ))` on `γ ≥ β` is an upper bound of `T' g`. -/
def StepLE (θna T T' : ℝ → ℝ) : Prop :=
  ∀ g φ β B : ℝ, 0 < β → β < g → 0 < φ → φ < 1 →
    (∀ γ, β ≤ γ → min γ (φ * θna ((g - β) / φ)) + (1 - φ) * T (γ / (1 - φ)) ≤ B) → T' g ≤ B

/-- What the analysis of the recursion uses about the non-adaptive exponent `θna` and the
hinted exponent `θh` on `(0, E)`; `a` bounds `θna`, `h` is the value of `θh` at `0+`. -/
structure HintPair (θna θh : ℝ → ℝ) (a h E : ℝ) : Prop where
  h_pos : 0 < h
  a_pos : 0 < a
  na_le : ∀ x, 0 < x → θna x ≤ a
  na_cont : ∀ x, 0 < x → ContinuousAt θna x
  na_h : θna h = h
  ident : ∀ e, 0 < e → e < E → θna (e + θh e) = θh e
  hint_pos : ∀ e, 0 < e → e < E → 0 < θh e
  hint_mono : ∀ e e', 0 < e → e ≤ e' → e' < E → e + θh e ≤ e' + θh e'
  hint_lower : ∃ L, ∀ e, 0 < e → e < E → h - L * e ≤ θh e

variable {θna θh : ℝ → ℝ} {a h E : ℝ}

private theorem scale_aux {p τ σ γ : ℝ} (hp : p ≠ 0) : p * (τ - σ * (γ / p)) = p * τ - σ * γ := by
  field_simp

/-- The tolerance `β` can be sent to zero: it is enough to bound the bracket on
`0 < γ ≤ φ θna(g/φ)`. -/
theorem StepLE.of_limit {T T' : ℝ → ℝ} (hs : StepLE θna T T')
    (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x)
    {g φ : ℝ} (hg : 0 < g) (hφ0 : 0 < φ) (hφ1 : φ < 1)
    (hc : ContinuousAt θna (g / φ)) (hμ : 0 < φ * θna (g / φ)) {B : ℝ}
    (hB : ∀ γ, 0 < γ → γ ≤ φ * θna (g / φ) → γ + (1 - φ) * T (γ / (1 - φ)) ≤ B) :
    T' g ≤ B := by
  refine le_of_forall_pos_le_add fun η hη => ?_
  have h1 : 0 < 1 - φ := by linarith
  obtain ⟨δ, hδ, hδ'⟩ := Metric.continuousAt_iff.mp hc (η / φ) (div_pos hη hφ0)
  obtain ⟨β, hβ0, hβg, hβδ⟩ : ∃ β : ℝ, 0 < β ∧ β < g ∧ β < δ * φ := by
    refine ⟨min (g / 2) (δ * φ / 2), lt_min (by linarith) (by positivity), ?_, ?_⟩
    · exact lt_of_le_of_lt (min_le_left _ _) (by linarith)
    · exact lt_of_le_of_lt (min_le_right _ _) (by nlinarith [mul_pos hδ hφ0])
  have hclose : dist ((g - β) / φ) (g / φ) < δ := by
    rw [Real.dist_eq]
    have e1 : (g - β) / φ - g / φ = -(β / φ) := by field_simp; ring
    rw [e1, abs_neg, abs_of_pos (div_pos hβ0 hφ0), div_lt_iff₀ hφ0]
    exact hβδ
  have hμβ : φ * θna ((g - β) / φ) ≤ φ * θna (g / φ) + η := by
    have h2 := hδ' hclose
    rw [Real.dist_eq] at h2
    have h3 : θna ((g - β) / φ) - θna (g / φ) < η / φ := lt_of_le_of_lt (le_abs_self _) h2
    have h4 : φ * (θna ((g - β) / φ) - θna (g / φ)) < φ * (η / φ) := mul_lt_mul_of_pos_left h3 hφ0
    have h5 : φ * (η / φ) = η := by field_simp
    linarith
  apply hs g φ β (B + η) hβ0 hβg hφ0 hφ1
  intro γ hγ
  have hγ0 : 0 < γ := lt_of_lt_of_le hβ0 hγ
  by_cases hcase : γ ≤ φ * θna (g / φ)
  · have h6 := hB γ hγ0 hcase
    have h7 : min γ (φ * θna ((g - β) / φ)) ≤ γ := min_le_left _ _
    linarith
  · rw [not_le] at hcase
    have hT : T (γ / (1 - φ)) ≤ T (φ * θna (g / φ) / (1 - φ)) := by
      apply hanti _ _ (div_pos hμ h1)
      exact div_le_div_of_nonneg_right hcase.le h1.le
    have hmin : min γ (φ * θna ((g - β) / φ)) ≤ φ * θna (g / φ) + η :=
      le_trans (min_le_right _ _) hμβ
    have h8 := hB (φ * θna (g / φ)) hμ le_rfl
    have h9 := mul_le_mul_of_nonneg_left hT h1.le
    linarith

/-- With a fixed outer fraction `φ` the outer sample never needs more than `φ a`. -/
theorem StepLE.of_macro (hp : HintPair θna θh a h E) {T T' : ℝ → ℝ} (hs : StepLE θna T T')
    (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x)
    {g φ : ℝ} (hg : 0 < g) (hφ0 : 0 < φ) (hφ1 : φ < 1) {B : ℝ}
    (hB : ∀ γ, 0 < γ → γ ≤ φ * a → γ + (1 - φ) * T (γ / (1 - φ)) ≤ B) : T' g ≤ B := by
  have h1 : 0 < 1 - φ := by linarith
  have hφa : 0 < φ * a := mul_pos hφ0 hp.a_pos
  apply hs g φ (g / 2) B (by linarith) (by linarith) hφ0 hφ1
  intro γ hγ
  have hγ0 : 0 < γ := by linarith
  have hμ : φ * θna ((g - g / 2) / φ) ≤ φ * a := by
    apply mul_le_mul_of_nonneg_left _ hφ0.le
    apply hp.na_le
    apply div_pos _ hφ0
    linarith
  by_cases hcase : γ ≤ φ * a
  · have h6 := hB γ hγ0 hcase
    have h7 : min γ (φ * θna ((g - g / 2) / φ)) ≤ γ := min_le_left _ _
    linarith
  · rw [not_le] at hcase
    have hT : T (γ / (1 - φ)) ≤ T (φ * a / (1 - φ)) := by
      apply hanti _ _ (div_pos hφa h1)
      exact div_le_div_of_nonneg_right hcase.le h1.le
    have hmin : min γ (φ * θna ((g - g / 2) / φ)) ≤ φ * a := le_trans (min_le_right _ _) hμ
    have h8 := hB (φ * a) hφa le_rfl
    have h9 := mul_le_mul_of_nonneg_left hT h1.le
    linarith

/-- The step with the outer fraction `φ = x/(x + θh x)`: by the identity `θna (x + θh x) = θh x`
the outer sample has exponent `(1 - φ) x`, and the bracket is `(1 - φ) (y + T y)` with `y ≤ x`. -/
theorem StepLE.at_hint_fraction (hp : HintPair θna θh a h E) {T T' : ℝ → ℝ} (hs : StepLE θna T T')
    (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x) {x : ℝ} (hx : 0 < x) (hxE : x < E) {C : ℝ}
    (hC : ∀ y, 0 < y → y ≤ x → y + T y ≤ C) :
    T' x ≤ θh x / (x + θh x) * C := by
  have hθx : 0 < θh x := hp.hint_pos x hx hxE
  have hsum : 0 < x + θh x := by linarith
  have hφ0 : 0 < x / (x + θh x) := div_pos hx hsum
  have hφ1 : x / (x + θh x) < 1 := by rw [div_lt_one hsum]; linarith
  have h1eq : 1 - x / (x + θh x) = θh x / (x + θh x) := by field_simp; ring
  have h1 : 0 < θh x / (x + θh x) := div_pos hθx hsum
  have hxφ : x / (x / (x + θh x)) = x + θh x := by field_simp
  have hμ : x / (x + θh x) * θna (x / (x / (x + θh x))) = θh x / (x + θh x) * x := by
    rw [hxφ, hp.ident x hx hxE]; ring
  have hμpos : 0 < x / (x + θh x) * θna (x / (x / (x + θh x))) := by
    rw [hμ]; exact mul_pos h1 hx
  apply StepLE.of_limit hs hanti hx hφ0 hφ1 (by rw [hxφ]; exact hp.na_cont _ hsum) hμpos
  intro γ hγ0 hγ
  rw [hμ] at hγ
  rw [h1eq]
  have hy0 : 0 < γ / (θh x / (x + θh x)) := div_pos hγ0 h1
  have hyx : γ / (θh x / (x + θh x)) ≤ x := by rw [div_le_iff₀ h1]; linarith
  have hγy : γ = θh x / (x + θh x) * (γ / (θh x / (x + θh x))) := by field_simp
  have h2 := hC _ hy0 hyx
  have h3 := mul_le_mul_of_nonneg_left h2 h1.le
  nlinarith

/-- **No super-solution above the hinted exponent.**  A nonincreasing bounded `T` with
`T ≤ R[T]` satisfies `T ≤ θh` on `(0, E)`. -/
theorem superSolution_le_hint (hp : HintPair θna θh a h E) {T : ℝ → ℝ}
    (hs : StepLE θna T T) (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x)
    (hbdd : ∀ x, 0 < x → T x ≤ a) : ∀ g, 0 < g → g < E → T g ≤ θh g := by
  -- the supremum of `T`
  have hne : (T '' Ioi (0 : ℝ)).Nonempty := ⟨T 1, 1, by simp, rfl⟩
  have hbd : BddAbove (T '' Ioi (0 : ℝ)) := ⟨a, by rintro _ ⟨x, hx, rfl⟩; exact hbdd x hx⟩
  obtain ⟨τ, hTτ, hτle⟩ : ∃ τ : ℝ, (∀ x, 0 < x → T x ≤ τ) ∧ ∀ B, (∀ x, 0 < x → T x ≤ B) → τ ≤ B :=
    ⟨sSup (T '' Ioi (0 : ℝ)), fun x hx => le_csSup hbd ⟨x, hx, rfl⟩,
      fun B hB => csSup_le hne (by rintro _ ⟨x, hx, rfl⟩; exact hB x hx)⟩
  -- Step I: the supremum is at most `h`
  have hτh : τ ≤ h := by
    by_contra hcon
    rw [not_le] at hcon
    have hτ0 : 0 < τ := lt_trans hp.h_pos hcon
    obtain ⟨c, hc0, hcτ⟩ : ∃ c : ℝ, 0 < c ∧ τ = h * (c + 1) := by
      refine ⟨τ / h - 1, ?_, ?_⟩
      · have : 1 < τ / h := by rw [lt_div_iff₀ hp.h_pos]; linarith
        linarith
      · rw [sub_add_cancel, mul_div_cancel₀ _ hp.h_pos.ne']
    -- a linear bound near zero has slope below one (fixed outer fraction)
    have lemS : ∀ σ : ℝ, (∃ x0, 0 < x0 ∧ ∀ x, 0 < x → x ≤ x0 → T x ≤ τ - σ * x) → σ < 1 := by
      rintro σ ⟨x0, hx0, hx⟩
      by_contra hσ1
      rw [not_lt] at hσ1
      have hax : 0 < a + x0 := by linarith [hp.a_pos]
      have hφ0 : 0 < x0 / (a + x0) := div_pos hx0 hax
      have hφ1 : x0 / (a + x0) < 1 := by rw [div_lt_one hax]; linarith [hp.a_pos]
      have h1 : 0 < 1 - x0 / (a + x0) := by linarith
      have hφa : x0 / (a + x0) * a = x0 * (1 - x0 / (a + x0)) := by field_simp; ring
      have hkey : ∀ g, 0 < g → T g ≤ (1 - x0 / (a + x0)) * τ := by
        intro g hg
        apply StepLE.of_macro hp hs hanti hg hφ0 hφ1
        intro γ hγ0 hγ
        have hle : γ / (1 - x0 / (a + x0)) ≤ x0 := by
          rw [div_le_iff₀ h1]; linarith
        have h2 := hx _ (div_pos hγ0 h1) hle
        have h3 := mul_le_mul_of_nonneg_left h2 h1.le
        have h4 : (1 - x0 / (a + x0)) * (τ - σ * (γ / (1 - x0 / (a + x0))))
            = (1 - x0 / (a + x0)) * τ - σ * γ := scale_aux h1.ne'
        nlinarith [mul_nonneg (sub_nonneg.mpr hσ1) hγ0.le]
      have h5 := hτle _ hkey
      nlinarith [mul_pos hφ0 hτ0]
    -- the slope improves by `c` at every step (outer fraction `g/h`)
    have ind : ∀ j : ℕ, ∃ x0, 0 < x0 ∧ ∀ x, 0 < x → x ≤ x0 → T x ≤ τ - (j * c) * x := by
      intro j
      induction j with
      | zero => exact ⟨1, one_pos, fun x hx _ => by simpa using hTτ x hx⟩
      | succ j ih =>
        obtain ⟨x0, hx0, hx⟩ := ih
        have hσ1 : (j : ℝ) * c < 1 := lemS _ ⟨x0, hx0, hx⟩
        refine ⟨min (x0 / 2) (h / 2), lt_min (by linarith) (by linarith [hp.h_pos]), ?_⟩
        intro g hg hgle
        have hg1 : g ≤ x0 / 2 := le_trans hgle (min_le_left _ _)
        have hg2 : g ≤ h / 2 := le_trans hgle (min_le_right _ _)
        have hφ0 : 0 < g / h := div_pos hg hp.h_pos
        have hφhalf : g / h ≤ 1 / 2 := by rw [div_le_iff₀ hp.h_pos]; linarith
        have hφ1 : g / h < 1 := by linarith
        have h1 : 0 < 1 - g / h := by linarith
        have hgφ : g / (g / h) = h := by field_simp
        have hμ : g / h * θna (g / (g / h)) = g := by
          rw [hgφ, hp.na_h]; exact div_mul_cancel₀ g hp.h_pos.ne'
        apply StepLE.of_limit hs hanti hg hφ0 hφ1 (by rw [hgφ]; exact hp.na_cont h hp.h_pos)
          (by rw [hμ]; exact hg)
        intro γ hγ0 hγ
        rw [hμ] at hγ
        have hle : γ / (1 - g / h) ≤ x0 := by
          rw [div_le_iff₀ h1]; nlinarith
        have h2 := hx _ (div_pos hγ0 h1) hle
        have h3 := mul_le_mul_of_nonneg_left h2 h1.le
        have h4 : (1 - g / h) * (τ - (j * c) * (γ / (1 - g / h)))
            = (1 - g / h) * τ - (j * c) * γ := scale_aux h1.ne'
        have hh : h ≠ 0 := hp.h_pos.ne'
        have h5 : g / h * τ = g * (c + 1) := by rw [hcτ]; field_simp
        push_cast
        nlinarith [mul_nonneg (sub_nonneg.mpr hσ1.le) (sub_nonneg.mpr hγ)]
    obtain ⟨j, hj⟩ := exists_nat_gt (1 / c)
    have h6 := lemS _ (ind j)
    rw [div_lt_iff₀ hc0] at hj
    linarith
  -- Step II: the excess over `θh` contracts
  intro g1 hg1 hg1E
  by_contra hcon
  rw [not_le] at hcon
  have hθ1 : 0 < θh g1 := hp.hint_pos g1 hg1 hg1E
  have hSne : ((fun x => T x - θh x) '' Ioc 0 g1).Nonempty := ⟨_, g1, ⟨hg1, le_rfl⟩, rfl⟩
  have hSbd : BddAbove ((fun x => T x - θh x) '' Ioc 0 g1) := ⟨h, by
    rintro _ ⟨x, ⟨hx0, hx1⟩, rfl⟩
    have h2 := hp.hint_pos x hx0 (lt_of_le_of_lt hx1 hg1E)
    have h3 := hTτ x hx0
    show T x - θh x ≤ h
    linarith⟩
  obtain ⟨M, hMpos, hDM, hMle⟩ : ∃ M : ℝ, 0 < M ∧ (∀ x, 0 < x → x ≤ g1 → T x - θh x ≤ M) ∧
      ∀ B, (∀ x, 0 < x → x ≤ g1 → T x - θh x ≤ B) → M ≤ B := by
    refine ⟨sSup ((fun x => T x - θh x) '' Ioc 0 g1), ?_, ?_, ?_⟩
    · exact lt_of_lt_of_le (by linarith) (le_csSup hSbd ⟨g1, ⟨hg1, le_rfl⟩, rfl⟩)
    · exact fun x h0 h1 => le_csSup hSbd ⟨x, ⟨h0, h1⟩, rfl⟩
    · exact fun B hB => csSup_le hSne (by rintro _ ⟨x, ⟨h0, h1⟩, rfl⟩; exact hB x h0 h1)
  obtain ⟨L, hL⟩ := hp.hint_lower
  have hL1 : 0 < 2 * (|L| + 1) := by positivity
  obtain ⟨x0, hx0pos, hx0g, hx0M⟩ : ∃ x0 : ℝ, 0 < x0 ∧ x0 ≤ g1 ∧ x0 ≤ M / (2 * (|L| + 1)) :=
    ⟨min g1 (M / (2 * (|L| + 1))), lt_min hg1 (by positivity), min_le_left _ _, min_le_right _ _⟩
  have hc0pos : 0 < x0 / (g1 + θh g1) := div_pos hx0pos (by linarith)
  have hbound : ∀ x, 0 < x → x ≤ g1 →
      T x - θh x ≤ max (M / 2) ((1 - x0 / (g1 + θh g1)) * M) := by
    intro x hx hxg
    by_cases hsmall : x ≤ x0
    · apply le_max_of_le_left
      have h1 := hL x hx (lt_of_le_of_lt hxg hg1E)
      have h2 := hTτ x hx
      have h3 : L * x ≤ |L| * x := mul_le_mul_of_nonneg_right (le_abs_self L) hx.le
      have h4 : x ≤ M / (2 * (|L| + 1)) := le_trans hsmall hx0M
      rw [le_div_iff₀ hL1] at h4
      nlinarith [abs_nonneg L]
    · rw [not_le] at hsmall
      apply le_max_of_le_right
      have hxE : x < E := lt_of_le_of_lt hxg hg1E
      have hθx : 0 < θh x := hp.hint_pos x hx hxE
      have hsum : 0 < x + θh x := by linarith
      have key : T x ≤ θh x / (x + θh x) * (x + θh x + M) := by
        apply StepLE.at_hint_fraction hp hs hanti hx hxE
        intro y hy0 hyx
        have hmono := hp.hint_mono y x hy0 hyx hxE
        have hD := hDM y hy0 (le_trans hyx hxg)
        linarith
      have h5 : θh x / (x + θh x) * (x + θh x + M) = θh x + θh x / (x + θh x) * M := by
        field_simp
      have h6 : θh x / (x + θh x) = 1 - x / (x + θh x) := by field_simp; ring
      have hφc : x0 / (g1 + θh g1) ≤ x / (x + θh x) := by
        rw [div_le_div_iff₀ (by linarith) hsum]
        have hm := hp.hint_mono x g1 hx hxg hg1E
        nlinarith [mul_le_mul_of_nonneg_left hm hx.le, mul_le_mul_of_nonneg_right hsmall.le hsum.le]
      rw [h5, h6] at key
      nlinarith [mul_le_mul_of_nonneg_right hφc hMpos.le]
  have hfin := hMle _ hbound
  rcases max_cases (M / 2) ((1 - x0 / (g1 + θh g1)) * M) with ⟨he, _⟩ | ⟨he, _⟩
  · rw [he] at hfin; linarith
  · rw [he] at hfin; nlinarith [mul_pos hc0pos hMpos]

/-- One step from the hinted exponent does not leave it: `R[θh] ≤ θh` on `(0, E)`
(the parameters are `φ = g/(g + θh g)`, `β → 0`). -/
theorem step_from_hint_le (hp : HintPair θna θh a h E) {T' : ℝ → ℝ} (hs : StepLE θna θh T')
    (hanti : ∀ x y, 0 < x → x ≤ y → θh y ≤ θh x) {g : ℝ} (hg : 0 < g) (hgE : g < E) :
    T' g ≤ θh g := by
  have hθ : 0 < θh g := hp.hint_pos g hg hgE
  have hsum : 0 < g + θh g := by linarith
  have key := StepLE.at_hint_fraction hp hs hanti hg hgE (C := g + θh g)
    (fun y hy0 hyg => hp.hint_mono y g hy0 hyg hgE)
  have h1 : θh g / (g + θh g) * (g + θh g) = θh g := by field_simp
  linarith

/-- **The level recursion converges to the hinted exponent.**  If every `T (k+1)` is at most
the two-level bound built on `T k` and at most `T k`, and the `T k` are nonincreasing,
nonnegative and bounded, then for every accuracy `g ∈ (0, E)` and every `η > 0` some level
has `T k g < θh g + η`. -/
theorem iterates_lt_hint_add (hp : HintPair θna θh a h E) (T : ℕ → ℝ → ℝ)
    (hstep : ∀ k, StepLE θna (T k) (T (k + 1)))
    (hmono : ∀ k x, 0 < x → T (k + 1) x ≤ T k x)
    (hanti : ∀ k x y, 0 < x → x ≤ y → T k y ≤ T k x)
    (hbdd : ∀ x, 0 < x → T 0 x ≤ a) (hnn : ∀ k x, 0 < x → 0 ≤ T k x)
    {g : ℝ} (hg : 0 < g) (hgE : g < E) {η : ℝ} (hη : 0 < η) : ∃ k, T k g < θh g + η := by
  have hmono' : ∀ k k', k ≤ k' → ∀ x, 0 < x → T k' x ≤ T k x := by
    intro k k' hkk'
    induction hkk' with
    | refl => exact fun x _ => le_rfl
    | step _ ih => exact fun x hx => (hmono _ x hx).trans (ih x hx)
  have hbelow : ∀ x, 0 < x → BddBelow (range fun k => T k x) := fun x hx =>
    ⟨0, by rintro _ ⟨k, rfl⟩; exact hnn k x hx⟩
  have hinf_le : ∀ k x, 0 < x → (⨅ k, T k x) ≤ T k x := fun k x hx => ciInf_le (hbelow x hx) k
  have hinf_anti : ∀ x y, 0 < x → x ≤ y → (⨅ k, T k y) ≤ ⨅ k, T k x := fun x y hx hxy =>
    le_ciInf fun k => (hinf_le k y (lt_of_lt_of_le hx hxy)).trans (hanti k x y hx hxy)
  have hinf_bdd : ∀ x, 0 < x → (⨅ k, T k x) ≤ a := fun x hx => (hinf_le 0 x hx).trans (hbdd x hx)
  have hsup : StepLE θna (fun x => ⨅ k, T k x) (fun x => ⨅ k, T k x) := by
    intro g φ β B hβ hβg hφ0 hφ1 hB
    show (⨅ k, T k g) ≤ B
    refine le_of_forall_pos_le_add fun η hη => ?_
    have hg0 : 0 < g := lt_trans hβ hβg
    have h1 : 0 < 1 - φ := by linarith
    have hδ0 : 0 < η / 2 := by positivity
    obtain ⟨N, hN⟩ := exists_nat_gt ((max β (φ * θna ((g - β) / φ)) - β) / (η / 2))
    have hex : ∀ i : ℕ, ∃ k, (1 - φ) * T k ((β + i * (η / 2)) / (1 - φ))
        < (1 - φ) * (⨅ k, T k ((β + i * (η / 2)) / (1 - φ))) + η / 2 := by
      intro i
      have hlt : (⨅ k, T k ((β + i * (η / 2)) / (1 - φ)))
          < (⨅ k, T k ((β + i * (η / 2)) / (1 - φ))) + η / (2 * (1 - φ)) := by
        have : 0 < η / (2 * (1 - φ)) := by positivity
        linarith
      obtain ⟨k, hk⟩ := exists_lt_of_ciInf_lt hlt
      refine ⟨k, ?_⟩
      have h2 := mul_lt_mul_of_pos_left hk h1
      have e : (1 - φ) * (η / (2 * (1 - φ))) = η / 2 := by field_simp
      linarith
    choose kk hkk using hex
    have hkge : ∀ i, i ≤ N → kk i ≤ (Finset.range (N + 1)).sup kk := fun i hi =>
      Finset.le_sup (Finset.mem_range.mpr (Nat.lt_succ_of_le hi))
    refine (hinf_le ((Finset.range (N + 1)).sup kk + 1) g hg0).trans
      (hstep _ g φ β (B + η) hβ hβg hφ0 hφ1 ?_)
    intro γ hγ
    obtain ⟨i, hiN, hγi, hmin⟩ : ∃ i : ℕ, i ≤ N ∧ β + i * (η / 2) ≤ γ ∧
        min γ (φ * θna ((g - β) / φ)) ≤ min (β + i * (η / 2)) (φ * θna ((g - β) / φ)) + η / 2 := by
      have hfl : (⌊(γ - β) / (η / 2)⌋₊ : ℝ) ≤ (γ - β) / (η / 2) :=
        Nat.floor_le (div_nonneg (by linarith) hδ0.le)
      rcases Nat.lt_or_ge ⌊(γ - β) / (η / 2)⌋₊ N with hlt | hge
      · refine ⟨⌊(γ - β) / (η / 2)⌋₊, hlt.le, ?_, ?_⟩
        · rw [le_div_iff₀ hδ0] at hfl; linarith
        · have h5 : (γ - β) / (η / 2) < ⌊(γ - β) / (η / 2)⌋₊ + 1 := Nat.lt_floor_add_one _
          rw [div_lt_iff₀ hδ0] at h5
          rcases le_total (β + ⌊(γ - β) / (η / 2)⌋₊ * (η / 2)) (φ * θna ((g - β) / φ)) with hc | hc
          · rw [min_eq_left hc]; exact (min_le_left _ _).trans (by linarith)
          · rw [min_eq_right hc]; exact (min_le_right _ _).trans (by linarith)
      · refine ⟨N, le_rfl, ?_, ?_⟩
        · have h6 : (N : ℝ) ≤ ⌊(γ - β) / (η / 2)⌋₊ := by exact_mod_cast hge
          have h7 := h6.trans hfl
          rw [le_div_iff₀ hδ0] at h7; linarith
        · have h8 := hN.le
          rw [div_le_iff₀ hδ0] at h8
          have h9 : φ * θna ((g - β) / φ) ≤ β + N * (η / 2) := by
            have := le_max_right β (φ * θna ((g - β) / φ)); linarith
          rw [min_eq_right h9]; exact (min_le_right _ _).trans (by linarith)
    have hpos : 0 < (β + i * (η / 2)) / (1 - φ) := div_pos (by positivity) h1
    have hTk : T ((Finset.range (N + 1)).sup kk) (γ / (1 - φ))
        ≤ T (kk i) ((β + i * (η / 2)) / (1 - φ)) :=
      (hanti _ _ _ hpos (div_le_div_of_nonneg_right hγi h1.le)).trans
        (hmono' _ _ (hkge i hiN) _ hpos)
    have h10 := hkk i
    have h11 := hB (β + i * (η / 2)) (by nlinarith [Nat.cast_nonneg (α := ℝ) i])
    have h12 := mul_le_mul_of_nonneg_left hTk h1.le
    linarith
  have hfinal := superSolution_le_hint hp hsup hinf_anti hinf_bdd g hg hgE
  have hlt : (⨅ k, T k g) < θh g + η := by
    have : (⨅ k, T k g) ≤ θh g := hfinal
    linarith
  exact exists_lt_of_ciInf_lt hlt

/-! ### The identity between the two relative entropies -/

/-- Relative entropy of the two-point distribution `(ρ, 1 - ρ)` with respect to `(q, 1 - q)`. -/
noncomputable def klBin (ρ q : ℝ) : ℝ :=
  ρ * Real.log (ρ / q) + (1 - ρ) * Real.log ((1 - ρ) / (1 - q))

/-- `KL(ρ ‖ p_u) = KL(ρ ‖ 1/2) + u ρ - ln(2/(1 + e^{-u}))` with `p_u = 1/(1 + e^u)`.  In the
notation of the theory report: the accuracy of non-adaptive sampling at radius `ρ n` is the
hinted accuracy `u ρ - Λ₁` plus the exponent `KL(ρ ‖ 1/2)` of the number of samples. -/
theorem klBin_shift {ρ u : ℝ} (hρ0 : 0 < ρ) (hρ1 : ρ < 1) :
    klBin ρ (1 / (1 + Real.exp u))
      = klBin ρ (1 / 2) + u * ρ - Real.log (2 / (1 + Real.exp (-u))) := by
  have he : 0 < Real.exp u := Real.exp_pos u
  have hen : 0 < Real.exp (-u) := Real.exp_pos (-u)
  have h1ρ : 0 < 1 - ρ := by linarith
  have hq1 : 1 - 1 / (1 + Real.exp u) = Real.exp u / (1 + Real.exp u) := by field_simp; ring
  have hneg : Real.exp (-u) = (Real.exp u)⁻¹ := Real.exp_neg u
  unfold klBin
  rw [hq1]
  have e1 : ρ / (1 / (1 + Real.exp u)) = ρ * (1 + Real.exp u) := by field_simp
  have e2 : (1 - ρ) / (Real.exp u / (1 + Real.exp u)) = (1 - ρ) * (1 + Real.exp u) / Real.exp u := by
    field_simp
  have e3 : ρ / (1 / 2) = ρ * 2 := by field_simp
  have e4 : (1 - ρ) / (1 - 1 / 2) = (1 - ρ) * 2 := by field_simp; ring
  have e5 : (2 : ℝ) / (1 + Real.exp (-u)) = 2 * Real.exp u / (1 + Real.exp u) := by
    rw [hneg]; field_simp; ring
  rw [e1, e2, e3, e4, e5]
  rw [Real.log_mul hρ0.ne' (by positivity), Real.log_div (by positivity) he.ne',
    Real.log_mul h1ρ.ne' (by positivity), Real.log_mul hρ0.ne' (by norm_num),
    Real.log_mul h1ρ.ne' (by norm_num), Real.log_div (by positivity) (by positivity),
    Real.log_mul (by norm_num) he.ne', Real.log_exp]
  ring

/-! ### Non-vacuity: the small-slope limit -/

/-- The non-adaptive exponent in the small-slope limit (in units of `u²/8`). -/
noncomputable def gaussNa (x : ℝ) : ℝ := (1 - Real.sqrt (min x 1)) ^ 2

/-- The hinted exponent in the small-slope limit. -/
noncomputable def gaussHint (e : ℝ) : ℝ := (1 - e) ^ 2 / 4

theorem gaussPair : HintPair gaussNa gaussHint 1 (1 / 4) 1 where
  h_pos := by norm_num
  a_pos := one_pos
  na_le := by
    intro x hx
    unfold gaussNa
    have h0 : 0 ≤ Real.sqrt (min x 1) := Real.sqrt_nonneg _
    have h1 : Real.sqrt (min x 1) ≤ 1 := by
      calc Real.sqrt (min x 1) ≤ Real.sqrt 1 := Real.sqrt_le_sqrt (min_le_right _ _)
        _ = 1 := Real.sqrt_one
    nlinarith
  na_cont := by
    intro x _
    unfold gaussNa
    fun_prop
  na_h := by
    unfold gaussNa
    have h1 : min (1 / 4 : ℝ) 1 = (1 / 2) ^ 2 := by norm_num
    rw [h1, Real.sqrt_sq (by norm_num)]
    norm_num
  ident := by
    intro e he0 he1
    unfold gaussNa gaussHint
    have h1 : e + (1 - e) ^ 2 / 4 = ((1 + e) / 2) ^ 2 := by ring
    have h2 : ((1 + e) / 2) ^ 2 ≤ 1 := by nlinarith
    rw [h1, min_eq_left h2, Real.sqrt_sq (by linarith)]
    ring
  hint_pos := by
    intro e _ he1
    unfold gaussHint
    have : 0 < 1 - e := by linarith
    positivity
  hint_mono := by
    intro e e' he hee' _
    unfold gaussHint
    nlinarith
  hint_lower := ⟨1 / 2, by
    intro e _ _
    unfold gaussHint
    nlinarith [sq_nonneg e]⟩

/-- The zero function satisfies the hypotheses of `superSolution_le_hint` for the small-slope
pair, so they are consistent. -/
theorem zero_superSolution : StepLE gaussNa (fun _ => 0) (fun _ => 0) := by
  intro g φ β B hβ _ hφ0 _ hB
  have h1 := hB β le_rfl
  have h2 : 0 ≤ min β (φ * gaussNa ((g - β) / φ)) :=
    le_min hβ.le (mul_nonneg hφ0.le (by unfold gaussNa; positivity))
  simp only [mul_zero, add_zero] at h1
  show (0 : ℝ) ≤ B
  linarith

/-- The hinted exponent of the small-slope limit, continued by zero beyond the threshold. -/
noncomputable def gaussHintClip (e : ℝ) : ℝ := (1 - min e 1) ^ 2 / 4

theorem gaussHintClip_eq {e : ℝ} (he : e ≤ 1) : gaussHintClip e = gaussHint e := by
  unfold gaussHintClip gaussHint
  rw [min_eq_left he]

/-- **The hinted exponent is a super-solution** (small-slope limit): one step of the recursion
from it does not go below it.  With `step_from_hint_le` it is a fixed point, and it is a
positive function to which `superSolution_le_hint` applies.  The proof is the convexity
argument of the theory report: the cost at `γ = max(β, μ)` is a convex combination of an
outer and an inner term whose mean radius is at most that of the target accuracy. -/
theorem gauss_hint_superSolution : StepLE gaussNa gaussHintClip gaussHintClip := by
  intro g φ β B hβ hβg hφ0 hφ1 hB
  have h1 : 0 < 1 - φ := by linarith
  have ht0 : 0 ≤ min ((g - β) / φ) 1 := le_min (div_nonneg (by linarith) hφ0.le) zero_le_one
  have ht1 : min ((g - β) / φ) 1 ≤ 1 := min_le_right _ _
  obtain ⟨r, hr0, hr1, hr2⟩ : ∃ r : ℝ, 0 ≤ r ∧ r ≤ 1 ∧ r ^ 2 = min ((g - β) / φ) 1 := by
    refine ⟨Real.sqrt (min ((g - β) / φ) 1), Real.sqrt_nonneg _, ?_, Real.sq_sqrt ht0⟩
    calc Real.sqrt (min ((g - β) / φ) 1) ≤ Real.sqrt 1 := Real.sqrt_le_sqrt ht1
      _ = 1 := Real.sqrt_one
  have hna : gaussNa ((g - β) / φ) = (1 - r) ^ 2 := by
    unfold gaussNa
    rw [← hr2, Real.sqrt_sq hr0]
  have hμ0 : 0 ≤ φ * (1 - r) ^ 2 := by positivity
  have hkey := hB (max β (φ * gaussNa ((g - β) / φ))) (le_max_left _ _)
  rw [hna, min_eq_right (le_max_right _ _)] at hkey
  -- the inner accuracy
  have hx0 : 0 ≤ max β (φ * (1 - r) ^ 2) / (1 - φ) := div_nonneg (le_trans hβ.le (le_max_left _ _)) h1.le
  have hm0 : 0 ≤ min (max β (φ * (1 - r) ^ 2) / (1 - φ)) 1 := le_min hx0 zero_le_one
  have hm1 : min (max β (φ * (1 - r) ^ 2) / (1 - φ)) 1 ≤ 1 := min_le_right _ _
  have hmx : (1 - φ) * min (max β (φ * (1 - r) ^ 2) / (1 - φ)) 1 ≤ max β (φ * (1 - r) ^ 2) := by
    have h2 : min (max β (φ * (1 - r) ^ 2) / (1 - φ)) 1 ≤ max β (φ * (1 - r) ^ 2) / (1 - φ) :=
      min_le_left _ _
    have h3 := mul_le_mul_of_nonneg_left h2 h1.le
    have h4 : (1 - φ) * (max β (φ * (1 - r) ^ 2) / (1 - φ)) = max β (φ * (1 - r) ^ 2) := by
      field_simp
    linarith
  -- the outer accuracy: `φ r² ≤ g − β`
  have hout : φ * r ^ 2 ≤ g - β := by
    rw [hr2]
    have h2 : min ((g - β) / φ) 1 ≤ (g - β) / φ := min_le_left _ _
    have h3 := mul_le_mul_of_nonneg_left h2 hφ0.le
    have h4 : φ * ((g - β) / φ) = g - β := by field_simp
    linarith
  unfold gaussHintClip at hkey ⊢
  generalize min (max β (φ * (1 - r) ^ 2) / (1 - φ)) 1 = m at hkey hm0 hm1 hmx
  -- `max β μ − β − μ ≤ 0`
  have hmax : max β (φ * (1 - r) ^ 2) ≤ β + φ * (1 - r) ^ 2 := max_le (by linarith) (by linarith)
  -- mean radius: `1 − min g 1 ≤ 2 φ (1 − r) + (1 − φ)(1 − m)`
  have hmean : 1 - min g 1 ≤ 2 * φ * (1 - r) + (1 - φ) * (1 - m) := by
    rcases le_total g 1 with hg | hg
    · rw [min_eq_left hg]; nlinarith
    · rw [min_eq_right hg]
      have : 0 ≤ 2 * φ * (1 - r) + (1 - φ) * (1 - m) := by
        have := mul_nonneg hφ0.le (sub_nonneg.mpr hr1)
        have := mul_nonneg h1.le (sub_nonneg.mpr hm1)
        linarith
      linarith
  have hlhs0 : 0 ≤ 1 - min g 1 := by linarith [min_le_right g 1]
  -- Jensen
  have hjen : (2 * φ * (1 - r) + (1 - φ) * (1 - m)) ^ 2
      ≤ 4 * (φ * (1 - r) ^ 2) + (1 - φ) * (1 - m) ^ 2 := by
    nlinarith [mul_nonneg (mul_nonneg hφ0.le h1.le) (sq_nonneg (2 * (1 - r) - (1 - m)))]
  have hsq : (1 - min g 1) ^ 2 ≤ (2 * φ * (1 - r) + (1 - φ) * (1 - m)) ^ 2 :=
    pow_le_pow_left₀ hlhs0 hmean 2
  linarith

end HintRecursion

/-! ## The deterministic core of the two-level bracket -/

namespace LayerCake

open Finset

variable {α : Type*} [Fintype α]

/-- The fraction of points at which `W` exceeds the level `s`. -/
noncomputable def exceed (W : α → ℝ) (s : ℝ) : ℝ :=
  ((univ.filter fun a => s < W a).card : ℝ) / Fintype.card α

/-- The mean of `W` over the (finite, uniform) space. -/
noncomputable def mean (W : α → ℝ) : ℝ := (∑ a, W a) / Fintype.card α

theorem exceed_eq_mean_indicator (W : α → ℝ) (s : ℝ) :
    exceed W s = mean (fun a => if s < W a then (1 : ℝ) else 0) := by
  unfold exceed mean
  rw [Finset.sum_ite, Finset.sum_const_zero, add_zero, Finset.sum_const, nsmul_eq_mul, mul_one]

theorem mean_mono [Nonempty α] {V W : α → ℝ} (h : ∀ a, V a ≤ W a) : mean V ≤ mean W := by
  unfold mean
  have hc : (0 : ℝ) < Fintype.card α := by exact_mod_cast Fintype.card_pos
  exact div_le_div_of_nonneg_right (Finset.sum_le_sum fun a _ => h a) hc.le

theorem mean_add (V W : α → ℝ) : mean (fun a => V a + W a) = mean V + mean W := by
  unfold mean
  rw [Finset.sum_add_distrib, add_div]

theorem mean_const_mul (c : ℝ) (W : α → ℝ) : mean (fun a => c * W a) = c * mean W := by
  unfold mean
  rw [← Finset.mul_sum, mul_div_assoc]

theorem mean_const [Nonempty α] (c : ℝ) : mean (fun _ : α => c) = c := by
  unfold mean
  have hc : (Fintype.card α : ℝ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  field_simp

theorem mean_sum {ι : Type*} (t : Finset ι) (V : ι → α → ℝ) :
    mean (fun a => ∑ i ∈ t, V i a) = ∑ i ∈ t, mean (V i) := by
  unfold mean
  rw [Finset.sum_comm, Finset.sum_div]

/-- Markov's inequality in the form used for the lower end: `s · P(W > s) ≤ E W`. -/
theorem level_mul_exceed_le_mean [Nonempty α] {W : α → ℝ} (hW : ∀ a, 0 ≤ W a) (s : ℝ) :
    s * exceed W s ≤ mean W := by
  rw [exceed_eq_mean_indicator, ← mean_const_mul]
  apply mean_mono
  intro a
  by_cases h : s < W a
  · simp only [h, if_true, mul_one]; exact h.le
  · simp only [h, if_false, mul_zero]; exact hW a

/-- The layer-cake bound at one point, for any sequence of levels:
`w ≤ s₀ + Σ_{i<j} (s_{i+1} − s_i)·[w > s_i] + (w − s_j)₊`. -/
theorem pointwise_layer_cake (s : ℕ → ℝ) (w : ℝ) (j : ℕ) :
    w ≤ s 0 + ∑ i ∈ range j, (s (i + 1) - s i) * (if s i < w then (1 : ℝ) else 0) + max (w - s j) 0 := by
  induction j with
  | zero =>
    simp only [Finset.range_zero, Finset.sum_empty, add_zero]
    have := le_max_left (w - s 0) 0
    linarith
  | succ j ih =>
    rw [Finset.sum_range_succ]
    have hstep : max (w - s j) 0
        ≤ (s (j + 1) - s j) * (if s j < w then (1 : ℝ) else 0) + max (w - s (j + 1)) 0 := by
      by_cases h : s j < w
      · simp only [h, if_true, mul_one]
        have h1 := le_max_left (w - s (j + 1)) 0
        have h2 : max (w - s j) 0 = w - s j := max_eq_left (by linarith)
        linarith
      · simp only [h, if_false, mul_zero, zero_add]
        have h2 : max (w - s j) 0 = 0 := max_eq_right (by linarith [not_lt.mp h])
        rw [h2]
        exact le_max_right _ _
    linarith

/-- **Layer cake (F3), upper end.**  For nondecreasing nonnegative levels,
`E W ≤ s₀ + Σ_{i<j} s_{i+1}·P(W > s_i) + E (W − s_j)₊`. -/
theorem mean_le_layer_cake [Nonempty α] (W : α → ℝ) (s : ℕ → ℝ) (hs : Monotone s) (hs0 : 0 ≤ s 0) (j : ℕ) :
    mean W ≤ s 0 + ∑ i ∈ range j, s (i + 1) * exceed W (s i) + mean (fun a => max (W a - s j) 0) := by
  have hpt : ∀ a, W a ≤ s 0 + ∑ i ∈ range j, s (i + 1) * (if s i < W a then (1 : ℝ) else 0)
      + max (W a - s j) 0 := by
    intro a
    refine (pointwise_layer_cake s (W a) j).trans ?_
    have : ∑ i ∈ range j, (s (i + 1) - s i) * (if s i < W a then (1 : ℝ) else 0)
        ≤ ∑ i ∈ range j, s (i + 1) * (if s i < W a then (1 : ℝ) else 0) := by
      apply Finset.sum_le_sum
      intro i _
      have hsi : 0 ≤ s i := hs0.trans (hs (Nat.zero_le i))
      by_cases h : s i < W a
      · simp only [h, if_true, mul_one]; linarith
      · simp only [h, if_false, mul_zero]; exact le_rfl
    linarith
  have h1 := mean_mono hpt
  have h2 : mean (fun a => s 0 + ∑ i ∈ range j, s (i + 1) * (if s i < W a then (1 : ℝ) else 0)
      + max (W a - s j) 0)
      = s 0 + ∑ i ∈ range j, s (i + 1) * exceed W (s i) + mean (fun a => max (W a - s j) 0) := by
    rw [mean_add (fun a => s 0 + ∑ i ∈ range j, s (i + 1) * (if s i < W a then (1 : ℝ) else 0))
      (fun a => max (W a - s j) 0),
      mean_add (fun _ => s 0) (fun a => ∑ i ∈ range j, s (i + 1) * (if s i < W a then (1 : ℝ) else 0)),
      mean_const, mean_sum]
    congr 2
    apply Finset.sum_congr rfl
    intro i _
    rw [mean_const_mul, exceed_eq_mean_indicator]
  linarith

/-- **Validity of the upper end.**  With certified bounds `q i ≥ P(W > s_i)` and
`tail ≥ E (W − s_j)₊`, the mean is at most `s₀ + Σ_{i<j} s_{i+1} q_i + tail`. -/
theorem mean_le_upper [Nonempty α] (W : α → ℝ) (s : ℕ → ℝ) (hs : Monotone s) (hs0 : 0 ≤ s 0) (j : ℕ)
    (q : ℕ → ℝ) (hq : ∀ i, i < j → exceed W (s i) ≤ q i) {tail : ℝ}
    (htail : mean (fun a => max (W a - s j) 0) ≤ tail) :
    mean W ≤ s 0 + ∑ i ∈ range j, s (i + 1) * q i + tail := by
  have h1 := mean_le_layer_cake W s hs hs0 j
  have h2 : ∑ i ∈ range j, s (i + 1) * exceed W (s i) ≤ ∑ i ∈ range j, s (i + 1) * q i := by
    apply Finset.sum_le_sum
    intro i hi
    exact mul_le_mul_of_nonneg_left (hq i (Finset.mem_range.mp hi)) (hs0.trans (hs (Nat.zero_le _)))
  linarith

/-- **Width.**  If the bottom level is at most `ℓ`, every level contributes at most
`4e^{b+1} ℓ` (populated) or at most `e^b ℓ/J` (negligible), there are at most `J` levels and the
tail is at most `e^G ℓ`, then the upper end is at most `(1 + 4J e^{b+1} + e^b + e^G) ℓ`. -/
theorem upper_le_width {s0 ℓ tail b G : ℝ} {J j : ℕ} (c : ℕ → ℝ) (hℓ : 0 ≤ ℓ) (hs0 : s0 ≤ ℓ)
    (hJ : 0 < J) (hjJ : j ≤ J)
    (hc : ∀ i, i < j → c i ≤ 4 * Real.exp (b + 1) * ℓ ∨ c i ≤ Real.exp b * ℓ / J)
    (htail : tail ≤ Real.exp G * ℓ) :
    s0 + ∑ i ∈ range j, c i + tail
      ≤ (1 + 4 * J * Real.exp (b + 1) + Real.exp b + Real.exp G) * ℓ := by
  have hJr : (0 : ℝ) < J := by exact_mod_cast hJ
  have hjr : (j : ℝ) ≤ J := by exact_mod_cast hjJ
  have hpos1 : 0 ≤ 4 * Real.exp (b + 1) * ℓ := by positivity
  have hpos2 : 0 ≤ Real.exp b * ℓ / J := by positivity
  have hsum : ∑ i ∈ range j, c i ≤ ∑ _i ∈ range j, (4 * Real.exp (b + 1) * ℓ + Real.exp b * ℓ / J) := by
    apply Finset.sum_le_sum
    intro i hi
    rcases hc i (Finset.mem_range.mp hi) with h | h <;> linarith
  rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul] at hsum
  have h3 : (j : ℝ) * (4 * Real.exp (b + 1) * ℓ + Real.exp b * ℓ / J)
      ≤ J * (4 * Real.exp (b + 1) * ℓ + Real.exp b * ℓ / J) :=
    mul_le_mul_of_nonneg_right hjr (by linarith)
  have h4 : (J : ℝ) * (4 * Real.exp (b + 1) * ℓ + Real.exp b * ℓ / J)
      = 4 * J * Real.exp (b + 1) * ℓ + Real.exp b * ℓ := by
    field_simp
  nlinarith

/-- **Fibre averages of a Lipschitz function are Lipschitz (F2).**  If
`ψ(a, y) ≤ ψ(a', y) + c` for all `y`, then `Σ_y e^{−ψ(a', y)} ≤ e^{c} Σ_y e^{−ψ(a, y)}`. -/
theorem fibre_sum_le {β : Type*} [Fintype β] (ψ ψ' : β → ℝ) {c : ℝ} (h : ∀ y, ψ y ≤ ψ' y + c) :
    ∑ y, Real.exp (-ψ' y) ≤ Real.exp c * ∑ y, Real.exp (-ψ y) := by
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro y _
  rw [← Real.exp_add]
  apply Real.exp_le_exp.mpr
  linarith [h y]

/-- **The count on which the cost rests.**  Let the negligibility threshold of level `s` be
`Mneg = 2KJe·s/(ℓ e^b)`, and let an earlier level `sᵢ` with `s e^{-x-1} ≤ sᵢ` have exceedance
probability `P` with `sᵢ·P ≤ 4 e^b ℓ` (which every level that was left as populated or as
negligible satisfies).  Then `Mneg·P ≤ 8KJe²·e^x`: the two factors `e^b` cancel, and the expected
number of sampled points within a factor `e^x` of the level is at most `e^x` up to a
polynomial factor, whatever the instance. -/
theorem close_points_bound {K J ℓ b x s si P : ℝ} (hK : 0 ≤ K) (hJ : 0 ≤ J) (hℓ : 0 < ℓ)
    (hsi : s * Real.exp (-x - 1) ≤ si) (hP : 0 ≤ P)
    (hcert : si * P ≤ 4 * Real.exp b * ℓ) :
    2 * K * J * Real.exp 1 * s / (ℓ * Real.exp b) * P ≤ 8 * K * J * Real.exp 1 ^ 2 * Real.exp x := by
  have hb : 0 < Real.exp b := Real.exp_pos b
  have he : 0 < Real.exp 1 := Real.exp_pos 1
  have hx : 0 < Real.exp x := Real.exp_pos x
  have hden : 0 < ℓ * Real.exp b := mul_pos hℓ hb
  -- `s·P ≤ 4 e^b ℓ e^{x+1}`
  have hexp : Real.exp (-x - 1) * (Real.exp x * Real.exp 1) = 1 := by
    rw [← Real.exp_add, ← Real.exp_add]; simp
  have h1 : s * P ≤ 4 * Real.exp b * ℓ * (Real.exp x * Real.exp 1) := by
    have h2 : s * Real.exp (-x - 1) * P ≤ 4 * Real.exp b * ℓ :=
      (mul_le_mul_of_nonneg_right hsi hP).trans hcert
    have h3 := mul_le_mul_of_nonneg_right h2 (mul_pos hx he).le
    have h4 : s * Real.exp (-x - 1) * P * (Real.exp x * Real.exp 1) = s * P := by
      calc s * Real.exp (-x - 1) * P * (Real.exp x * Real.exp 1)
          = s * P * (Real.exp (-x - 1) * (Real.exp x * Real.exp 1)) := by ring
        _ = s * P := by rw [hexp, mul_one]
    linarith
  rw [div_mul_eq_mul_div, div_le_iff₀ hden]
  have hKJ : 0 ≤ 2 * K * J * Real.exp 1 := by positivity
  calc 2 * K * J * Real.exp 1 * s * P = 2 * K * J * Real.exp 1 * (s * P) := by ring
    _ ≤ 2 * K * J * Real.exp 1 * (4 * Real.exp b * ℓ * (Real.exp x * Real.exp 1)) :=
        mul_le_mul_of_nonneg_left h1 hKJ
    _ = 8 * K * J * Real.exp 1 ^ 2 * Real.exp x * (ℓ * Real.exp b) := by ring

/-- **How large the negligibility threshold gets.**  If the previous level `s/e` was left as
populated with certified exceedance probability `q` (so that `ℓ ≥ (s/e) e^{-b} q/4`), then the
threshold of the next level is at most `8KJe²/q`. -/
theorem negligibility_threshold_le {K J ℓ b s q : ℝ} (hK : 0 ≤ K) (hJ : 0 ≤ J) (hs : 0 < s) (hq : 0 < q)
    (hℓ : s / Real.exp 1 * Real.exp (-b) * q / 4 ≤ ℓ) :
    2 * K * J * Real.exp 1 * s / (ℓ * Real.exp b) ≤ 8 * K * J * Real.exp 1 ^ 2 / q := by
  have hb : 0 < Real.exp b := Real.exp_pos b
  have he : 0 < Real.exp 1 := Real.exp_pos 1
  have hpos : 0 < s / Real.exp 1 * Real.exp (-b) * q / 4 := by positivity
  have hℓ0 : 0 < ℓ := lt_of_lt_of_le hpos hℓ
  rw [div_le_div_iff₀ (mul_pos hℓ0 hb) hq]
  have hbb : Real.exp (-b) * Real.exp b = 1 := by rw [← Real.exp_add]; simp
  have h1 : s * q ≤ 4 * Real.exp 1 * (ℓ * Real.exp b) := by
    have h2 := mul_le_mul_of_nonneg_right hℓ (mul_pos (mul_pos (by norm_num : (0:ℝ) < 4) he) hb).le
    have h3 : s / Real.exp 1 * Real.exp (-b) * q / 4 * (4 * Real.exp 1 * Real.exp b)
        = s * q * (Real.exp (-b) * Real.exp b) := by field_simp
    rw [h3, hbb, mul_one] at h2
    linarith
  have hKJ : 0 ≤ 2 * K * J * Real.exp 1 := by positivity
  calc 2 * K * J * Real.exp 1 * s * q = 2 * K * J * Real.exp 1 * (s * q) := by ring
    _ ≤ 2 * K * J * Real.exp 1 * (4 * Real.exp 1 * (ℓ * Real.exp b)) := mul_le_mul_of_nonneg_left h1 hKJ
    _ = 8 * K * J * Real.exp 1 ^ 2 * (ℓ * Real.exp b) := by ring

end LayerCake

end MetricChain
