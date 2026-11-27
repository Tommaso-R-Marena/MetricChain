import Mathlib
import proofs.Frontiers.SecondOrderEnvelope

/-!
# Dense second-order classes: the second-order dip, and why stars do not combine

Found by an independent workstream (`docs/workstreams/E_REPORT.md`, Theorems A and B(b)) and
verified by an independent reviewer (`docs/reviews/R_E_review.md`).  Everything is stated against
`MixedDiffBound` (`SecondOrderEnvelope.lean`) with a dense constant `c`, on general product
spaces `∀ i, σ i`.

* `dip c y r x = c · C(r - d_H(x, y), 2)` — the **second-order dip**: `dip_mixedDiffBound` (it has
  all mixed second differences bounded by `c`), `dip_center` (value `c · C(r, 2)` at the centre),
  `dip_eq_zero` (it vanishes outside the Hamming ball of radius `r - 2`), and `dip_witness`:
  for every evaluated set `A` and every `y` at Hamming distance at least `d` from `A` there is a
  member of the class that vanishes on `A` and equals `c · C(d + 1, 2)` at `y`.  So the
  uncertainty that remains after any evaluations grows quadratically with the distance to the
  evaluated set — the counterpart, for second-order classes, of the dips of
  `QueryLowerBound.lean`, and the reason why dense constants force exponentially many
  evaluations (theory report §11.12).
* `pairRemainder_const`, `star_upper` — a class member that vanishes on the star of `x₀` is at
  most `c · C(d_H(y, x₀), 2)` at `y` (the star remainder of `secondOrder_remainder`).
* `stars_do_not_combine` — if `A` contains the star of a nearest centre `a⋆ ∈ A₀` of `y`, at
  distance `D ≥ 1`, and every point of `A` is within distance one of a centre, then the largest
  value at `y` of a class member vanishing on `A` is **exactly** `c · C(D, 2)`: evaluating several
  stars gives the best single-star bound and nothing more.
-/

namespace MetricChain
namespace SecondOrderDip

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-- the profile of a dip as a real number -/
noncomputable def prof (r t : ℕ) : ℝ := ((r - t).choose 2 : ℝ)

theorem prof_second_diff_inside (r t : ℕ) (h : t + 2 ≤ r) :
    prof r (t + 2) - 2 * prof r (t + 1) + prof r t = 1 := by
  obtain ⟨k, rfl⟩ : ∃ k, r = t + 2 + k := ⟨r - (t + 2), by omega⟩
  have h0 : t + 2 + k - (t + 2) = k := by omega
  have h1 : t + 2 + k - (t + 1) = k + 1 := by omega
  have h2 : t + 2 + k - t = k + 2 := by omega
  simp only [prof, h0, h1, h2]
  have e1 : (k + 1).choose 2 = k + k.choose 2 := by
    rw [Nat.choose_succ_succ, Nat.choose_one_right]
  have e2 : (k + 2).choose 2 = (k + 1) + (k + 1).choose 2 := by
    rw [Nat.choose_succ_succ, Nat.choose_one_right]
  rw [e2, e1]
  push_cast
  ring

theorem prof_second_diff_outside (r t : ℕ) (h : r < t + 2) :
    prof r (t + 2) - 2 * prof r (t + 1) + prof r t = 0 := by
  have h0 : r - (t + 2) = 0 := by omega
  have c1 : (r - (t + 1)).choose 2 = 0 := Nat.choose_eq_zero_of_lt (by omega)
  have c2 : (r - t).choose 2 = 0 := Nat.choose_eq_zero_of_lt (by omega)
  simp [prof, h0, c1, c2]

theorem prof_second_diff_nonneg (r t : ℕ) :
    0 ≤ prof r (t + 2) - 2 * prof r (t + 1) + prof r t := by
  by_cases h : t + 2 ≤ r
  · rw [prof_second_diff_inside r t h]; norm_num
  · rw [prof_second_diff_outside r t (by omega)]

theorem prof_second_diff_le_one (r t : ℕ) :
    prof r (t + 2) - 2 * prof r (t + 1) + prof r t ≤ 1 := by
  by_cases h : t + 2 ≤ r
  · rw [prof_second_diff_inside r t h]
  · rw [prof_second_diff_outside r t (by omega)]; norm_num

section
variable [Fintype ι] [∀ i, DecidableEq (σ i)]

/-- Hamming distance (number of sites at which `x` and `y` differ). -/
def hdist (x y : ∀ i, σ i) : ℕ := ∑ i, (if x i = y i then 0 else 1)

/-- **Second-order dip** of parameter `r` centred at `y`. -/
noncomputable def dip (c : ℝ) (y : ∀ i, σ i) (r : ℕ) (x : ∀ i, σ i) : ℝ :=
  c * prof r (hdist x y)

theorem hdist_self (y : ∀ i, σ i) : hdist y y = 0 := by simp [hdist]

theorem hdist_comm (x y : ∀ i, σ i) : hdist x y = hdist y x := by
  unfold hdist
  apply Finset.sum_congr rfl
  intro i _
  by_cases h : x i = y i
  · simp [h]
  · have h' : ¬ y i = x i := fun e => h e.symm
    simp [h, h']

theorem hdist_triangle (x a y : ∀ i, σ i) : hdist x y ≤ hdist x a + hdist a y := by
  unfold hdist
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_le_sum
  intro i _
  by_cases h1 : x i = a i
  · by_cases h2 : a i = y i
    · have : x i = y i := h1.trans h2
      simp [h1, h2]
    · simp [h1, h2]
  · by_cases h3 : x i = y i <;> simp [h1, h3]

theorem dip_center (c : ℝ) (y : ∀ i, σ i) (r : ℕ) : dip c y r y = c * (r.choose 2 : ℝ) := by
  simp [dip, prof, hdist_self]

theorem dip_eq_zero (c : ℝ) (y x : ∀ i, σ i) (r : ℕ) (h : r ≤ hdist x y + 1) : dip c y r x = 0 := by
  have : (r - hdist x y).choose 2 = 0 := Nat.choose_eq_zero_of_lt (by omega)
  simp [dip, prof, this]

theorem hdist_decomp [DecidableEq ι] (x y z : ∀ i, σ i) (i j : ι) (hij : i ≠ j)
    (hz : ∀ k, k ≠ i → k ≠ j → z k = x k) :
    hdist z y = (if z i = y i then 0 else 1) + (if z j = y j then 0 else 1)
      + ∑ k ∈ (univ.erase i).erase j, (if x k = y k then 0 else 1) := by
  unfold hdist
  rw [← Finset.add_sum_erase univ _ (mem_univ i)]
  have hj : j ∈ (univ : Finset ι).erase i := Finset.mem_erase.mpr ⟨hij.symm, mem_univ j⟩
  rw [← Finset.add_sum_erase (univ.erase i) _ hj]
  rw [← add_assoc]
  congr 1
  apply Finset.sum_congr rfl
  intro k hk
  have hkj : k ≠ j := (Finset.mem_erase.mp hk).1
  have hki : k ≠ i := (Finset.mem_erase.mp (Finset.mem_erase.mp hk).2).1
  rw [hz k hki hkj]

set_option linter.unusedSimpArgs false in
/-- **Theorem A (membership).**  The dip has all mixed second differences bounded by `c`. -/
theorem dip_mixedDiffBound [DecidableEq ι] (c : ℝ) (hc : 0 ≤ c) (y : ∀ i, σ i) (r : ℕ) :
    MixedDiffBound (dip c y r) (fun _ _ => c) := by
  intro x i j hij a b
  have hji : j ≠ i := hij.symm
  set T : ℕ := ∑ k ∈ (univ.erase i).erase j, (if x k = y k then 0 else 1) with hT
  have e1 : hdist (Function.update (Function.update x i a) j b) y
      = (if a = y i then 0 else 1) + (if b = y j then 0 else 1) + T := by
    rw [hdist_decomp x y _ i j hij]
    · rw [Function.update_of_ne hij, Function.update_self, Function.update_self]
    · intro k hki hkj
      rw [Function.update_of_ne hkj, Function.update_of_ne hki]
  have e2 : hdist (Function.update x i a) y
      = (if a = y i then 0 else 1) + (if x j = y j then 0 else 1) + T := by
    rw [hdist_decomp x y _ i j hij]
    · rw [Function.update_self, Function.update_of_ne hji]
    · intro k hki _
      rw [Function.update_of_ne hki]
  have e3 : hdist (Function.update x j b) y
      = (if x i = y i then 0 else 1) + (if b = y j then 0 else 1) + T := by
    rw [hdist_decomp x y _ i j hij]
    · rw [Function.update_of_ne hij, Function.update_self]
    · intro k _ hkj
      rw [Function.update_of_ne hkj]
  have e4 : hdist x y = (if x i = y i then 0 else 1) + (if x j = y j then 0 else 1) + T :=
    hdist_decomp x y x i j hij (fun _ _ _ => rfl)
  have H1 := mul_nonneg hc (prof_second_diff_nonneg r T)
  have H2 := mul_le_mul_of_nonneg_left (prof_second_diff_le_one r T) hc
  have t0 : (0 : ℕ) + 0 + T = T := by omega
  have t1 : (1 : ℕ) + 0 + T = T + 1 := by omega
  have t1' : (0 : ℕ) + 1 + T = T + 1 := by omega
  have t2 : (1 : ℕ) + 1 + T = T + 2 := by omega
  simp only [dip, e1, e2, e3, e4]
  rw [abs_le]
  by_cases ha : a = y i <;> by_cases hx : x i = y i <;> by_cases hb : b = y j <;>
    by_cases hxj : x j = y j <;>
    simp only [ha, hx, hb, hxj, if_true, if_false, t0, t1, t1', t2] <;>
    constructor <;> nlinarith [H1, H2]

/-- **Theorem A (witness).**  If every point of `A` is at Hamming distance at least `d` from `y`,
some member of the dense second-order class with constant `c` vanishes on `A` and equals
`c * C(d+1, 2)` at `y`. -/
theorem dip_witness [DecidableEq ι] (c : ℝ) (hc : 0 ≤ c) (y : ∀ i, σ i) (A : Set (∀ i, σ i)) (d : ℕ)
    (hA : ∀ a ∈ A, d ≤ hdist a y) :
    ∃ h : (∀ i, σ i) → ℝ, MixedDiffBound h (fun _ _ => c) ∧ (∀ a ∈ A, h a = 0) ∧
      h y = c * ((d + 1).choose 2 : ℝ) :=
  ⟨dip c y (d + 1), dip_mixedDiffBound c hc y (d + 1),
    fun a ha => dip_eq_zero c y a (d + 1) (by have := hA a ha; omega),
    dip_center c y (d + 1)⟩

/-- For a constant table the pair remainder is `c * C(d, 2)`, `d` the Hamming distance. -/
theorem pairRemainder_const [DecidableEq ι] (c : ℝ) (x₀ x : ∀ i, σ i) :
    pairRemainder (fun _ _ => c) x₀ x = c * ((hdist x x₀).choose 2 : ℝ) := by
  have hD : ((hdist x x₀ : ℕ) : ℝ) = ∑ i, changed x₀ x i := by
    unfold hdist changed
    push_cast
    apply Finset.sum_congr rfl
    intro i _
    split_ifs <;> simp
  have hsq : ∀ i, changed x₀ x i * changed x₀ x i = changed x₀ x i := by
    intro i
    unfold changed
    split_ifs <;> simp
  have hinner : ∀ i, ∑ j ∈ univ.erase i, c * changed x₀ x i * changed x₀ x j
      = c * changed x₀ x i * (∑ j, changed x₀ x j) - c * changed x₀ x i := by
    intro i
    have hsplit : ∑ j, changed x₀ x j
        = changed x₀ x i + ∑ j ∈ univ.erase i, changed x₀ x j :=
      (Finset.add_sum_erase univ (fun j => changed x₀ x j) (mem_univ i)).symm
    rw [← Finset.mul_sum, hsplit]
    linear_combination (-c) * hsq i
  have hmain : pairRemainder (fun _ _ => c) x₀ x
      = (1 / 2) * ∑ i, (c * changed x₀ x i * (∑ j, changed x₀ x j) - c * changed x₀ x i) := by
    unfold pairRemainder
    congr 1
    apply Finset.sum_congr rfl
    intro i _
    exact hinner i
  rw [hmain, Finset.sum_sub_distrib, ← Finset.sum_mul, ← Finset.mul_sum, ← hD, Nat.cast_choose_two]
  ring

/-- **Theorem B(a).**  A member of the class that vanishes on the star of `x₀` is at most
`c * C(d(y, x₀), 2)` in absolute value at `y`. -/
theorem star_upper [DecidableEq ι] (c : ℝ) (h : (∀ i, σ i) → ℝ)
    (hh : MixedDiffBound h (fun _ _ => c)) (x₀ : ∀ i, σ i) (h0 : h x₀ = 0)
    (hstar : ∀ i (a : σ i), h (Function.update x₀ i a) = 0) (y : ∀ i, σ i) :
    |h y| ≤ c * ((hdist y x₀).choose 2 : ℝ) := by
  have key := secondOrder_remainder h (fun _ _ => c) hh (fun _ _ => rfl) x₀ y
  have hs : starPart h x₀ y = 0 := by simp [starPart, h0, hstar]
  rw [hs, sub_zero, pairRemainder_const] at key
  exact key

/-- **Theorem B(b): stars do not combine.**  Let `A` contain the star of `a⋆ ∈ A₀`, let every point
of `A` be within Hamming distance one of some centre in `A₀`, and let `a⋆` be a nearest centre to
`y`, at distance `D ≥ 1`.  Then every member of the class vanishing on `A` is at most `c * C(D,2)`
at `y`, and some member attains this value. -/
theorem stars_do_not_combine [DecidableEq ι] (c : ℝ) (hc : 0 ≤ c)
    (A₀ A : Set (∀ i, σ i)) (y aStar : ∀ i, σ i) (D : ℕ) (hD1 : 1 ≤ D)
    (hstarA : aStar ∈ A ∧ ∀ i (a : σ i), Function.update aStar i a ∈ A)
    (hthick : ∀ x ∈ A, ∃ a ∈ A₀, hdist x a ≤ 1)
    (hnear : hdist y aStar = D) (hmin : ∀ a ∈ A₀, D ≤ hdist a y) :
    (∀ h : (∀ i, σ i) → ℝ, MixedDiffBound h (fun _ _ => c) → (∀ x ∈ A, h x = 0) →
        |h y| ≤ c * (D.choose 2 : ℝ)) ∧
    (∃ h : (∀ i, σ i) → ℝ, MixedDiffBound h (fun _ _ => c) ∧ (∀ x ∈ A, h x = 0) ∧
        h y = c * (D.choose 2 : ℝ)) := by
  constructor
  · intro h hh hA
    have := star_upper c h hh aStar (hA _ hstarA.1) (fun i a => hA _ (hstarA.2 i a)) y
    rwa [hnear] at this
  · have hfar : ∀ x ∈ A, D - 1 ≤ hdist x y := by
      intro x hx
      obtain ⟨a, ha, hxa⟩ := hthick x hx
      have h1 := hmin a ha
      have h2 := hdist_triangle a x y
      have h3 := hdist_comm a x
      omega
    obtain ⟨h, hh, hz, hy⟩ := dip_witness c hc y A (D - 1) hfar
    refine ⟨h, hh, hz, ?_⟩
    have : D - 1 + 1 = D := by omega
    rw [hy, this]

end

end SecondOrderDip
end MetricChain
