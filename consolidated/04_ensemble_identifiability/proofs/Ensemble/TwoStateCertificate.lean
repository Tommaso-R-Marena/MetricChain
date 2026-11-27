/-
  MetricChain — Ensemble division.  The zero set of the two-state certificate (report §4c.4,
  Proposition E20′).

  Two states `p`, `q` of a product configuration space differ in every coordinate of an index set
  `ι` with at least two elements.  For non-negative functions `a k` ("distance of coordinate `k`
  from `p k`") and `b k` ("distance of coordinate `k` from `q k`") that never vanish together, the
  certificate

      f = ∑_{k ≠ l} a k * b l

  vanishes exactly when all `a k` vanish (the configuration is `p`) or all `b k` vanish (it is
  `q`).  This is the combinatorial content of Proposition E20′; that `a k = 2 - 2 cos(φ_k - p_k)`
  is non-negative and vanishes only at `φ_k = p_k` is the trigonometric part, on paper.

  `twoStateCert_growth_three` and `twoStateCert_growth_two` are the quantitative version
  (Proposition E20″): if at every coordinate one of `a k`, `b k` is at least `θ k`, the
  certificate is at least `c * min (∑ a) (∑ b)` — with `c = min θ` on three or more coordinates,
  and `c = θ 0 * θ 1 / (θ 0 + θ 1)` on two — quadratic growth away from the two states with a
  constant that can be computed.
-/
import Mathlib

namespace MetricChain.Ensemble

open Finset

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The two-state certificate `∑_{k ≠ l} a k * b l`. -/
def twoStateCert (a b : ι → ℝ) : ℝ :=
  ∑ k, ∑ l ∈ univ.filter (fun l => l ≠ k), a k * b l

/-- The purely logical core: if for all `k ≠ l` either coordinate `k` sits at `p` or coordinate
`l` sits at `q`, and no coordinate sits at both, then the configuration is `p` or it is `q`. -/
theorem all_left_or_all_right {A B : ι → Prop} (hne : ∀ k, ¬ (A k ∧ B k))
    (htwo : ∀ k : ι, ∃ l, l ≠ k) (h : ∀ k l, l ≠ k → A k ∨ B l) :
    (∀ k, A k) ∨ (∀ k, B k) := by
  by_cases hA : ∀ k, A k
  · exact Or.inl hA
  · right
    push Not at hA
    obtain ⟨k, hk⟩ := hA
    -- every other coordinate sits at `q`
    have hB : ∀ l, l ≠ k → B l := fun l hl => (h k l hl).resolve_left hk
    intro j
    by_cases hj : j = k
    · subst hj
      obtain ⟨l, hl⟩ := htwo j
      have hBl : B l := hB l hl
      have hAl : ¬ A l := fun hAl => hne l ⟨hAl, hBl⟩
      exact (h l j (fun e => hl e.symm)).resolve_left hAl
    · exact hB j hj

/-- **Zero set of the two-state certificate.**  For non-negative `a`, `b` that never vanish
together, on an index set in which every element has another one, the certificate vanishes iff
all `a k` vanish or all `b k` vanish. -/
theorem twoStateCert_eq_zero_iff (a b : ι → ℝ) (ha : ∀ k, 0 ≤ a k) (hb : ∀ k, 0 ≤ b k)
    (hne : ∀ k, ¬ (a k = 0 ∧ b k = 0)) (htwo : ∀ k : ι, ∃ l, l ≠ k) :
    twoStateCert a b = 0 ↔ (∀ k, a k = 0) ∨ (∀ k, b k = 0) := by
  constructor
  · intro h
    have hterm : ∀ k l, l ≠ k → a k * b l = 0 := by
      intro k l hl
      have h1 : ∀ k ∈ (univ : Finset ι), 0 ≤ ∑ l ∈ univ.filter (fun l => l ≠ k), a k * b l :=
        fun k _ => Finset.sum_nonneg (fun l _ => mul_nonneg (ha k) (hb l))
      have h2 := (Finset.sum_eq_zero_iff_of_nonneg h1).mp h k (Finset.mem_univ k)
      have h3 : ∀ l ∈ univ.filter (fun l => l ≠ k), 0 ≤ a k * b l :=
        fun l _ => mul_nonneg (ha k) (hb l)
      exact (Finset.sum_eq_zero_iff_of_nonneg h3).mp h2 l
        (Finset.mem_filter.mpr ⟨Finset.mem_univ l, hl⟩)
    exact all_left_or_all_right (A := fun k => a k = 0) (B := fun k => b k = 0) hne htwo
      (fun k l hl => mul_eq_zero.mp (hterm k l hl))
  · rintro (h | h)
    · simp [twoStateCert, h]
    · simp [twoStateCert, h]

/-- The certificate is non-negative. -/
theorem twoStateCert_nonneg (a b : ι → ℝ) (ha : ∀ k, 0 ≤ a k) (hb : ∀ k, 0 ≤ b k) :
    0 ≤ twoStateCert a b :=
  Finset.sum_nonneg (fun k _ => Finset.sum_nonneg (fun l _ => mul_nonneg (ha k) (hb l)))

/-- With a single coordinate the certificate is identically zero: two states that differ in one
coordinate only are not separated from the rest of that coordinate's fibre (the case `|D| = 1` of
Proposition E20′, in which no two-state ensemble is identified). -/
theorem twoStateCert_unique_eq_zero [Unique ι] (a b : ι → ℝ) : twoStateCert a b = 0 := by
  unfold twoStateCert
  refine Finset.sum_eq_zero (fun k _ => Finset.sum_eq_zero (fun l hl => ?_))
  exact absurd (Subsingleton.elim l k) (Finset.mem_filter.mp hl).2

/-- The certificate with the two sums exchanged. -/
theorem twoStateCert_comm (a b : ι → ℝ) :
    twoStateCert a b = ∑ l, ∑ k ∈ univ.filter (fun k => k ≠ l), a k * b l := by
  unfold twoStateCert
  simp only [Finset.sum_filter]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl (fun l _ => Finset.sum_congr rfl (fun k _ => ?_))
  by_cases h : l = k
  · subst h; simp
  · have h' : k ≠ l := fun e => h e.symm
    simp [h, h']

/-- If two distinct coordinates are far from the second state, every inner sum `∑_{l ≠ k} b l` is at
least `c`, and the certificate dominates `c * ∑ a`. -/
theorem twoStateCert_ge_of_two_far (a b θ : ι → ℝ) (c : ℝ) (ha : ∀ k, 0 ≤ a k) (hb : ∀ k, 0 ≤ b k)
    (hcθ : ∀ k, c ≤ θ k) {u v : ι} (huv : u ≠ v) (hu : θ u ≤ b u) (hv : θ v ≤ b v) :
    c * ∑ k, a k ≤ twoStateCert a b := by
  unfold twoStateCert
  rw [Finset.mul_sum]
  refine Finset.sum_le_sum (fun k _ => ?_)
  have hinner : c ≤ ∑ l ∈ univ.filter (fun l => l ≠ k), b l := by
    by_cases hk : u = k
    · have hvk : v ≠ k := fun e => huv (hk.trans e.symm)
      exact le_trans (le_trans (hcθ v) hv)
        (Finset.single_le_sum (f := b) (fun l _ => hb l)
          (Finset.mem_filter.mpr ⟨Finset.mem_univ v, hvk⟩))
    · exact le_trans (le_trans (hcθ u) hu)
        (Finset.single_le_sum (f := b) (fun l _ => hb l)
          (Finset.mem_filter.mpr ⟨Finset.mem_univ u, hk⟩))
  calc c * a k = a k * c := mul_comm _ _
    _ ≤ a k * ∑ l ∈ univ.filter (fun l => l ≠ k), b l := mul_le_mul_of_nonneg_left hinner (ha k)
    _ = ∑ l ∈ univ.filter (fun l => l ≠ k), a k * b l := by rw [Finset.mul_sum]

/-- The mirror statement: two distinct coordinates far from the first state give `c * ∑ b`. -/
theorem twoStateCert_ge_of_two_far' (a b θ : ι → ℝ) (c : ℝ) (ha : ∀ k, 0 ≤ a k) (hb : ∀ k, 0 ≤ b k)
    (hcθ : ∀ k, c ≤ θ k) {u v : ι} (huv : u ≠ v) (hu : θ u ≤ a u) (hv : θ v ≤ a v) :
    c * ∑ k, b k ≤ twoStateCert a b := by
  rw [twoStateCert_comm, Finset.mul_sum]
  refine Finset.sum_le_sum (fun l _ => ?_)
  have hinner : c ≤ ∑ k ∈ univ.filter (fun k => k ≠ l), a k := by
    by_cases hl : u = l
    · have hvl : v ≠ l := fun e => huv (hl.trans e.symm)
      exact le_trans (le_trans (hcθ v) hv)
        (Finset.single_le_sum (f := a) (fun k _ => ha k)
          (Finset.mem_filter.mpr ⟨Finset.mem_univ v, hvl⟩))
    · exact le_trans (le_trans (hcθ u) hu)
        (Finset.single_le_sum (f := a) (fun k _ => ha k)
          (Finset.mem_filter.mpr ⟨Finset.mem_univ u, hl⟩))
  calc c * b l ≤ (∑ k ∈ univ.filter (fun k => k ≠ l), a k) * b l :=
        mul_le_mul_of_nonneg_right hinner (hb l)
    _ = ∑ k ∈ univ.filter (fun k => k ≠ l), a k * b l := by rw [Finset.sum_mul]

/-- **Quadratic growth of the two-state certificate, three or more coordinates.**  If at every
coordinate one of `a k`, `b k` is at least `θ k` (for squared chordal distances to two points at
squared distance `β k`: `θ k = β k / 4`), `0 ≤ c ≤ θ k` for all `k`, and there are three distinct
coordinates, then `c * min (∑ a) (∑ b) ≤ ∑_{k ≠ l} a k * b l`. -/
theorem twoStateCert_growth_three (a b θ : ι → ℝ) (c : ℝ) (ha : ∀ k, 0 ≤ a k) (hb : ∀ k, 0 ≤ b k)
    (hor : ∀ k, θ k ≤ a k ∨ θ k ≤ b k) (hc0 : 0 ≤ c) (hcθ : ∀ k, c ≤ θ k)
    {i j m : ι} (hij : i ≠ j) (him : i ≠ m) (hjm : j ≠ m) :
    c * min (∑ k, a k) (∑ k, b k) ≤ twoStateCert a b := by
  have hA : c * min (∑ k, a k) (∑ k, b k) ≤ c * ∑ k, a k :=
    mul_le_mul_of_nonneg_left (min_le_left _ _) hc0
  have hB : c * min (∑ k, a k) (∑ k, b k) ≤ c * ∑ k, b k :=
    mul_le_mul_of_nonneg_left (min_le_right _ _) hc0
  rcases hor i with hi | hi <;> rcases hor j with hj | hj <;> rcases hor m with hm | hm
  · exact le_trans hB (twoStateCert_ge_of_two_far' a b θ c ha hb hcθ hij hi hj)
  · exact le_trans hB (twoStateCert_ge_of_two_far' a b θ c ha hb hcθ hij hi hj)
  · exact le_trans hB (twoStateCert_ge_of_two_far' a b θ c ha hb hcθ him hi hm)
  · exact le_trans hA (twoStateCert_ge_of_two_far a b θ c ha hb hcθ hjm hj hm)
  · exact le_trans hB (twoStateCert_ge_of_two_far' a b θ c ha hb hcθ hjm hj hm)
  · exact le_trans hA (twoStateCert_ge_of_two_far a b θ c ha hb hcθ him hi hm)
  · exact le_trans hA (twoStateCert_ge_of_two_far a b θ c ha hb hcθ hij hi hj)
  · exact le_trans hA (twoStateCert_ge_of_two_far a b θ c ha hb hcθ hij hi hj)

/-- On two coordinates the certificate is `a 0 * b 1 + a 1 * b 0`. -/
theorem twoStateCert_fin_two (a b : Fin 2 → ℝ) :
    twoStateCert a b = a 0 * b 1 + a 1 * b 0 := by
  have h0 : (univ.filter (fun l : Fin 2 => l ≠ 0)) = {1} := by decide
  have h1 : (univ.filter (fun l : Fin 2 => l ≠ 1)) = {0} := by decide
  simp [twoStateCert, Fin.sum_univ_two, h0, h1]

/-- **Quadratic growth of the two-state certificate, two coordinates.**  With `θ` as before,
positive, and `0 ≤ c`, `c * (θ 0 + θ 1) ≤ θ 0 * θ 1` (so `c` is at most half the harmonic mean of
`θ 0`, `θ 1`): `c * min (a 0 + a 1) (b 0 + b 1) ≤ a 0 * b 1 + a 1 * b 0`.  (Positivity of `θ` cannot
be dropped: with `θ = 0` the hypothesis on `c` is empty and the conclusion fails.) -/
theorem twoStateCert_growth_two (a b θ : Fin 2 → ℝ) (c : ℝ) (ha : ∀ k, 0 ≤ a k) (hb : ∀ k, 0 ≤ b k)
    (hθ : ∀ k, 0 < θ k) (hor : ∀ k, θ k ≤ a k ∨ θ k ≤ b k) (hc0 : 0 ≤ c)
    (hc : c * (θ 0 + θ 1) ≤ θ 0 * θ 1) :
    c * min (a 0 + a 1) (b 0 + b 1) ≤ twoStateCert a b := by
  rw [twoStateCert_fin_two]
  have ha0 := ha 0; have ha1 := ha 1; have hb0 := hb 0; have hb1 := hb 1
  have hθ0 := hθ 0; have hθ1 := hθ 1
  -- `c ≤ θ 0` and `c ≤ θ 1`
  have hc0' : c ≤ θ 0 := by
    by_contra h
    push Not at h
    nlinarith [mul_pos hθ0 hθ0, mul_lt_mul_of_pos_right h (add_pos hθ0 hθ1)]
  have hc1' : c ≤ θ 1 := by
    by_contra h
    push Not at h
    nlinarith [mul_pos hθ1 hθ1, mul_lt_mul_of_pos_right h (add_pos hθ0 hθ1)]
  have hA : c * min (a 0 + a 1) (b 0 + b 1) ≤ c * (a 0 + a 1) :=
    mul_le_mul_of_nonneg_left (min_le_left _ _) hc0
  have hB : c * min (a 0 + a 1) (b 0 + b 1) ≤ c * (b 0 + b 1) :=
    mul_le_mul_of_nonneg_left (min_le_right _ _) hc0
  by_cases h0 : θ 0 ≤ a 0
  · by_cases h1 : θ 1 ≤ a 1
    · -- both coordinates far from the first state: `c * (b 0 + b 1)`
      refine le_trans hB ?_
      nlinarith [mul_le_mul_of_nonneg_right (le_trans hc0' h0) hb1,
        mul_le_mul_of_nonneg_right (le_trans hc1' h1) hb0]
    · -- coordinate 1 is close to the first state, hence far from the second
      have hb1' : θ 1 ≤ b 1 := (hor 1).resolve_left h1
      push Not at h1
      refine le_trans hA ?_
      nlinarith [mul_le_mul_of_nonneg_left hb1' ha0, mul_nonneg ha1 hb0,
        mul_le_mul_of_nonneg_right h0 (sub_nonneg.mpr hc1'),
        mul_nonneg hc0 (sub_nonneg.mpr (le_of_lt h1))]
  · have hb0' : θ 0 ≤ b 0 := (hor 0).resolve_left h0
    push Not at h0
    by_cases h1 : θ 1 ≤ a 1
    · refine le_trans hA ?_
      nlinarith [mul_le_mul_of_nonneg_left hb0' ha1, mul_nonneg ha0 hb1,
        mul_le_mul_of_nonneg_right h1 (sub_nonneg.mpr hc0'),
        mul_nonneg hc0 (sub_nonneg.mpr (le_of_lt h0))]
    · -- both coordinates far from the second state: `c * (a 0 + a 1)`
      have hb1' : θ 1 ≤ b 1 := (hor 1).resolve_left h1
      refine le_trans hA ?_
      nlinarith [mul_le_mul_of_nonneg_left (le_trans hc1' hb1') ha0,
        mul_le_mul_of_nonneg_left (le_trans hc0' hb0') ha1]

end MetricChain.Ensemble
