/-
Gadget inequalities of docs/complexity/CHAIN_GEOMETRY_HARDNESS.md (complexity division).

* `right_angle_triangle`  (section 2a):  5 √(25 + 24 t) − 12 t ≤ 25 − t²  on [−1, 1], with equality only at t = 0.
* `orthogonality_gadget`  (section 2):   √(25 + 24 t) + √(25 − 24 t) ≤ 10 − t²  on [−1, 1], with equality only at t = 0.
* `cyclic_core`: the combinatorial core of Theorem 12′ of docs/complexity/NANUQ_LOCAL_CRITERION.md — three points
  cannot lie pairwise on different sides of a chord (a two-colouring of three points has two points of one colour).

No placeholder proofs, no added axioms, no native evaluation; the file prints the axioms of its four theorems.
-/
import Mathlib

namespace Complexity.ChainGadgets

open Real

/-- The right-angle triangle with multiplicities 3, 4, 5. -/
theorem right_angle_triangle {t : ℝ} (h₁ : -1 ≤ t) (h₂ : t ≤ 1) :
    5 * √(25 + 24 * t) - 12 * t ≤ 25 - t ^ 2 := by
  have hpos : 0 ≤ (25 + 12 * t - t ^ 2) / 5 := by nlinarith
  have hsq : 25 + 24 * t ≤ ((25 + 12 * t - t ^ 2) / 5) ^ 2 := by
    have key : ((25 + 12 * t - t ^ 2) / 5) ^ 2 - (25 + 24 * t) = t ^ 2 * (94 - 24 * t + t ^ 2) / 25 := by ring
    have h94 : 0 ≤ 94 - 24 * t + t ^ 2 := by nlinarith
    have : 0 ≤ t ^ 2 * (94 - 24 * t + t ^ 2) / 25 := by positivity
    linarith
  have hs : √(25 + 24 * t) ≤ (25 + 12 * t - t ^ 2) / 5 := Real.sqrt_le_iff.mpr ⟨hpos, hsq⟩
  linarith

/-- Equality in `right_angle_triangle` forces `t = 0`. -/
theorem right_angle_triangle_eq {t : ℝ} (h₁ : -1 ≤ t) (h₂ : t ≤ 1)
    (h : 5 * √(25 + 24 * t) - 12 * t = 25 - t ^ 2) : t = 0 := by
  have h0 : (0:ℝ) ≤ 25 + 24 * t := by linarith
  have hs : √(25 + 24 * t) = (25 + 12 * t - t ^ 2) / 5 := by linarith
  have hsq : 25 + 24 * t = ((25 + 12 * t - t ^ 2) / 5) ^ 2 := by
    rw [← hs, Real.sq_sqrt h0]
  have key : t ^ 2 * (94 - 24 * t + t ^ 2) = 0 := by nlinarith
  have h94 : 0 < 94 - 24 * t + t ^ 2 := by nlinarith
  have : t ^ 2 = 0 := by
    rcases mul_eq_zero.mp key with h' | h'
    · exact h'
    · exact absurd h' (ne_of_gt h94)
  exact pow_eq_zero_iff (two_ne_zero) |>.mp this

/-- The orthogonality gadget with couplings 3, 4 and 3, −4. -/
theorem orthogonality_gadget {t : ℝ} (h₁ : -1 ≤ t) (h₂ : t ≤ 1) :
    √(25 + 24 * t) + √(25 - 24 * t) ≤ 10 - t ^ 2 := by
  have ha : (0:ℝ) ≤ 25 + 24 * t := by linarith
  have hb : (0:ℝ) ≤ 25 - 24 * t := by linarith
  have ht2 : t ^ 2 ≤ 1 := by nlinarith
  have hpos : 0 ≤ 10 - t ^ 2 := by linarith
  -- the product of the two roots
  have hprod : √(25 + 24 * t) * √(25 - 24 * t) ≤ 25 - 10 * t ^ 2 + t ^ 4 / 2 := by
    rw [← Real.sqrt_mul ha]
    apply Real.sqrt_le_iff.mpr
    refine ⟨by nlinarith [sq_nonneg (t ^ 2)], ?_⟩
    have key : (25 - 10 * t ^ 2 + t ^ 4 / 2) ^ 2 - (25 + 24 * t) * (25 - 24 * t)
        = t ^ 2 * (76 + 125 * t ^ 2 - 10 * t ^ 4 + t ^ 6 / 4) := by ring
    have hin : 0 ≤ 76 + 125 * t ^ 2 - 10 * t ^ 4 + t ^ 6 / 4 := by
      have h4 : t ^ 4 ≤ 1 := by nlinarith [sq_nonneg (t ^ 2)]
      have h6 : 0 ≤ t ^ 6 := by positivity
      nlinarith [sq_nonneg t]
    have : 0 ≤ t ^ 2 * (76 + 125 * t ^ 2 - 10 * t ^ 4 + t ^ 6 / 4) := mul_nonneg (sq_nonneg t) hin
    linarith
  have hsum_sq : (√(25 + 24 * t) + √(25 - 24 * t)) ^ 2 ≤ (10 - t ^ 2) ^ 2 := by
    have e : (√(25 + 24 * t) + √(25 - 24 * t)) ^ 2
        = 50 + 2 * (√(25 + 24 * t) * √(25 - 24 * t)) := by
      have s1 := Real.sq_sqrt ha
      have s2 := Real.sq_sqrt hb
      nlinarith
    rw [e]
    nlinarith
  have hnn : 0 ≤ √(25 + 24 * t) + √(25 - 24 * t) := by positivity
  by_contra hcon
  rw [not_le] at hcon
  nlinarith

/-- Combinatorial core of Theorem 12′: if a chord separates `Z` from `Y` and `Z` from `X`, it does not separate
`Y` from `X` (sides of the chord as a two-colouring). -/
theorem cyclic_core (side : Fin 3 → Bool) (hZY : side 0 ≠ side 1) (hZX : side 0 ≠ side 2) : side 1 = side 2 := by
  revert hZY hZX
  cases side 0 <;> cases side 1 <;> cases side 2 <;> simp

end Complexity.ChainGadgets

#print axioms Complexity.ChainGadgets.right_angle_triangle
#print axioms Complexity.ChainGadgets.right_angle_triangle_eq
#print axioms Complexity.ChainGadgets.orthogonality_gadget
#print axioms Complexity.ChainGadgets.cyclic_core
