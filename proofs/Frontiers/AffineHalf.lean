import Mathlib

/-!
# An affine function on the cube is large on half of the points

**Provenance.**  This file was written and machine-checked by the Scientific Discovery Division in its independent
review of the seventeenth checkpoint (workstream R12, message SCI-REV-0013, finding M1; the last section of its file
`experiments/science/ws_R12/lean/R12Additions.lean` on the branch `research/scientific-translation`), and is adopted
here with its namespace, statements and proofs unchanged.  It is the core of the division's counter-algorithm to the
first version of our Proposition 11.18e(b) ("randomised algorithms without a hint need the Hamming ball as well"),
which was false as written.

`affine_half_large`: for every affine function `h(s) = α + ∑ β_i s_i` on the cube `{-1, 1}^n` and every point `s₀`,
at least half of the points `s` satisfy `|h(s₀)| ≤ (n + 1) |h(s)|`.  Hence `q` uniformly random evaluations fail to
show the scale of `h` with probability at most `2^{-q}`, whatever `n`; with a remainder bounded by `C` this gives
a finite bound for the minimum and for `ln Z` on a second-order class from `⌈log₂(1/δ)⌉` random evaluations
(theory report §11.7, Proposition 11.18e(b); harness XI.22).
-/

namespace ScienceR12

open Finset

/-! ### New (R12): the core of the counter-algorithm to Proposition 11.18e(b), on the cube, order below two

An affine function `h(s) = α + ∑ β_i s_i` on the cube `{-1, 1}^n` has absolute value at least
`max |h| / (n + 1)` on at least half of the points.  Hence `q` uniformly random evaluations fail to
show the scale of `h` with probability at most `2^{-q}`, for every `h` — whatever `n`. -/

/-- The sign `±1` of a Boolean coordinate. -/
noncomputable def sgn (b : Bool) : ℝ := if b then 1 else -1

theorem sgn_true : sgn true = 1 := by simp [sgn]

theorem sgn_false : sgn false = -1 := by simp [sgn]

theorem sgn_not (b : Bool) : sgn (!b) = -sgn b := by
  cases b
  · rw [Bool.not_false, sgn_true, sgn_false]; ring
  · rw [Bool.not_true, sgn_true, sgn_false]

theorem abs_sgn (b : Bool) : |sgn b| = 1 := by
  cases b
  · rw [sgn_false]; norm_num
  · rw [sgn_true]; norm_num

theorem abs_two_mul_sgn (x : ℝ) (b : Bool) : |-2 * x * sgn b| = 2 * |x| := by
  cases b
  · rw [sgn_false, show (-2 * x * -1 : ℝ) = 2 * x by ring, abs_mul,
      abs_of_pos (by norm_num : (0 : ℝ) < 2)]
  · rw [sgn_true, show (-2 * x * 1 : ℝ) = -(2 * x) by ring, abs_neg, abs_mul,
      abs_of_pos (by norm_num : (0 : ℝ) < 2)]

/-- An affine function on the cube, in Boolean coordinates. -/
noncomputable def aff (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (s : Fin n → Bool) : ℝ :=
  α + ∑ i, β i * sgn (s i)

/-- Flip one coordinate. -/
def flipAt {n : ℕ} (j : Fin n) (s : Fin n → Bool) : Fin n → Bool := Function.update s j (!s j)

/-- Flip every coordinate. -/
def negAll {n : ℕ} (s : Fin n → Bool) : Fin n → Bool := fun i => !s i

theorem flipAt_involutive {n : ℕ} (j : Fin n) : Function.Involutive (flipAt (n := n) j) := by
  intro s
  funext i
  unfold flipAt
  by_cases h : i = j
  · subst h
    simp
  · rw [Function.update_of_ne h, Function.update_of_ne h]

theorem negAll_involutive {n : ℕ} : Function.Involutive (negAll (n := n)) := by
  intro s
  funext i
  simp [negAll]

theorem aff_flip (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (j : Fin n) (s : Fin n → Bool) :
    aff n α β (flipAt j s) - aff n α β s = -2 * β j * sgn (s j) := by
  unfold aff
  have e1 : ∑ i, β i * sgn (flipAt j s i)
      = β j * sgn (flipAt j s j) + ∑ i ∈ univ.erase j, β i * sgn (flipAt j s i) :=
    (Finset.add_sum_erase _ _ (mem_univ j)).symm
  have e2 : ∑ i, β i * sgn (s i) = β j * sgn (s j) + ∑ i ∈ univ.erase j, β i * sgn (s i) :=
    (Finset.add_sum_erase _ _ (mem_univ j)).symm
  have e3 : ∑ i ∈ univ.erase j, β i * sgn (flipAt j s i) = ∑ i ∈ univ.erase j, β i * sgn (s i) := by
    refine Finset.sum_congr rfl fun i hi => ?_
    have hij : i ≠ j := Finset.ne_of_mem_erase hi
    unfold flipAt
    rw [Function.update_of_ne hij]
  have e4 : flipAt j s j = !s j := by
    unfold flipAt
    simp
  rw [e1, e2, e3, e4, sgn_not]
  ring

theorem aff_negAll (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (s : Fin n → Bool) :
    aff n α β (negAll s) + aff n α β s = 2 * α := by
  unfold aff negAll
  have : ∑ i, β i * sgn (!s i) = -∑ i, β i * sgn (s i) := by
    rw [← Finset.sum_neg_distrib]
    exact Finset.sum_congr rfl fun i _ => by rw [sgn_not]; ring
  rw [this]
  ring

theorem tri_add (x y : ℝ) : |x + y| ≤ |x| + |y| :=
  abs_le.mpr ⟨by linarith [neg_abs_le x, neg_abs_le y], by linarith [le_abs_self x, le_abs_self y]⟩

theorem tri_sub (x y : ℝ) : |x - y| ≤ |x| + |y| :=
  abs_le.mpr ⟨by linarith [le_abs_self y, neg_abs_le x], by linarith [le_abs_self x, neg_abs_le y]⟩

theorem abs_aff_le (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (s : Fin n → Bool) :
    |aff n α β s| ≤ |α| + ∑ i, |β i| := by
  unfold aff
  have h1 := tri_add α (∑ i, β i * sgn (s i))
  have h2 := Finset.abs_sum_le_sum_abs (fun i => β i * sgn (s i)) univ
  have h3 : ∑ i, |β i * sgn (s i)| = ∑ i, |β i| :=
    Finset.sum_congr rfl fun i _ => by rw [abs_mul, abs_sgn, mul_one]
  linarith

/-- If an involution maps every point outside `G` into `G`, then `G` contains half of the points. -/
theorem card_le_two_mul_of_involution {S : Type*} [Fintype S] [DecidableEq S] (f : S → S)
    (hf : Function.Involutive f) (G : Finset S) (h : ∀ s, s ∈ G ∨ f s ∈ G) :
    Fintype.card S ≤ 2 * G.card := by
  have hsub : (univ : Finset S) ⊆ G ∪ G.image f := by
    intro s _
    rcases h s with hs | hs
    · exact Finset.mem_union_left _ hs
    · exact Finset.mem_union_right _ (Finset.mem_image.mpr ⟨f s, hs, hf s⟩)
  calc Fintype.card S = (univ : Finset S).card := Finset.card_univ.symm
    _ ≤ (G ∪ G.image f).card := Finset.card_le_card hsub
    _ ≤ G.card + (G.image f).card := Finset.card_union_le _ _
    _ ≤ G.card + G.card := Nat.add_le_add_left Finset.card_image_le _
    _ = 2 * G.card := by ring

open Classical in
/-- **Half of the cube sees the scale of an affine function.**  For every affine `h` on `{-1, 1}^n` and every
point `s₀` (in particular a maximiser of `|h|`), at least `2^{n-1}` points `s` have
`|h(s₀)| ≤ (n + 1) |h(s)|`. -/
theorem affine_half_large (n : ℕ) (α : ℝ) (β : Fin n → ℝ) (s₀ : Fin n → Bool) :
    2 ^ n ≤ 2 * (univ.filter fun s : Fin n → Bool =>
      |aff n α β s₀| ≤ ((n : ℝ) + 1) * |aff n α β s|).card := by
  have hcard : Fintype.card (Fin n → Bool) = 2 ^ n := by simp
  have h0 := abs_aff_le n α β s₀
  have key : ∃ T : ℝ, |aff n α β s₀| ≤ ((n : ℝ) + 1) * T ∧
      ∃ f : (Fin n → Bool) → (Fin n → Bool), Function.Involutive f ∧
        ∀ s, T ≤ |aff n α β s| ∨ T ≤ |aff n α β (f s)| := by
    by_cases hα : ∀ i, |β i| ≤ |α|
    · refine ⟨|α|, ?_, negAll, negAll_involutive, ?_⟩
      · have hsum : ∑ i, |β i| ≤ ∑ _i : Fin n, |α| := Finset.sum_le_sum fun i _ => hα i
        rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hsum
        linarith
      · intro s
        by_contra hcon
        push Not at hcon
        have e := aff_negAll n α β s
        have t := tri_add (aff n α β (negAll s)) (aff n α β s)
        rw [e, abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 2)] at t
        linarith [hcon.1, hcon.2]
    · push Not at hα
      obtain ⟨i₀, hi₀⟩ := hα
      obtain ⟨j, -, hj⟩ := Finset.exists_max_image (univ : Finset (Fin n)) (fun i => |β i|)
        ⟨i₀, mem_univ i₀⟩
      have hαj : |α| ≤ |β j| := le_trans hi₀.le (hj i₀ (mem_univ _))
      refine ⟨|β j|, ?_, flipAt j, flipAt_involutive j, ?_⟩
      · have hsum : ∑ i, |β i| ≤ ∑ _i : Fin n, |β j| := Finset.sum_le_sum fun i _ => hj i (mem_univ _)
        rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hsum
        linarith
      · intro s
        by_contra hcon
        push Not at hcon
        have e := aff_flip n α β j s
        have t := tri_sub (aff n α β (flipAt j s)) (aff n α β s)
        rw [e, abs_two_mul_sgn] at t
        linarith [hcon.1, hcon.2]
  obtain ⟨T, hT, f, hf, hcov⟩ := key
  have hG := card_le_two_mul_of_involution f hf (univ.filter fun s => T ≤ |aff n α β s|)
    (fun s => by
      rcases hcov s with h | h
      · exact Or.inl (Finset.mem_filter.mpr ⟨mem_univ _, h⟩)
      · exact Or.inr (Finset.mem_filter.mpr ⟨mem_univ _, h⟩))
  rw [hcard] at hG
  refine hG.trans (Nat.mul_le_mul_left 2 (Finset.card_le_card ?_))
  intro s hs
  have hs' : T ≤ |aff n α β s| := (Finset.mem_filter.mp hs).2
  refine Finset.mem_filter.mpr ⟨mem_univ _, ?_⟩
  have hn : (0 : ℝ) ≤ (n : ℝ) + 1 := by positivity
  calc |aff n α β s₀| ≤ ((n : ℝ) + 1) * T := hT
    _ ≤ ((n : ℝ) + 1) * |aff n α β s| := mul_le_mul_of_nonneg_left hs' hn

end ScienceR12
