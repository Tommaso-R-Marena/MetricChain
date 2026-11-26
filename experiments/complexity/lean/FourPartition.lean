/-
Arithmetic core of Garey and Johnson's reduction from 3-dimensional matching to 4-PARTITION, as written out in
docs/complexity/STRANDS_NN_HARDNESS.md, Appendix A, Lemma A2.

Items: for every element of the three classes, copies `w i act`, `x j act`, `y k act` (`act = true` for the actual
copy, `false` for a dummy copy), and one item `u i j k` per triple.  With `r = 32 q`:

  size (w i act) = (10 | 11) r⁴ + i r   + 1        size (x j act) = (10 | 11) r⁴ + j r² + 2
  size (y k act) = (10 |  8) r⁴ + k r³  + 4        size (u i j k) = 10 r⁴ − k r³ − j r² − i r + 8
  bin size  B = 40 r⁴ + 15.

`four_sum`: four admissible items (indices between 1 and q) whose sizes add up to `B` are one item `u i j k`
together with copies of exactly `w i`, `x j`, `y k`, all actual or all dummy.
`sum_good`: conversely such four items add up to `B`.
`size_bounds`: every admissible item has `B/5 < size < B/3` (so a bin of an exact packing has four items).

Not formalised: the 3DM instance, the packing, and the equivalence itself.

Checked with:  lake env lean experiments/complexity/lean/FourPartition.lean
-/
import Mathlib

namespace Complexity.FourPartition

inductive Item where
  | w (i : ℕ) (act : Bool)
  | x (j : ℕ) (act : Bool)
  | y (k : ℕ) (act : Bool)
  | u (i j k : ℕ)

open Item

/-- coefficient of `r⁰` -/
def d0 : Item → ℤ
  | w _ _ => 1 | x _ _ => 2 | y _ _ => 4 | u _ _ _ => 8
/-- coefficient of `r¹` -/
def d1 : Item → ℤ
  | w i _ => i | x _ _ => 0 | y _ _ => 0 | u i _ _ => -i
/-- coefficient of `r²` -/
def d2 : Item → ℤ
  | w _ _ => 0 | x j _ => j | y _ _ => 0 | u _ j _ => -j
/-- coefficient of `r³` -/
def d3 : Item → ℤ
  | w _ _ => 0 | x _ _ => 0 | y k _ => k | u _ _ k => -k
/-- coefficient of `r⁴` -/
def d4 : Item → ℤ
  | w _ act => if act then 10 else 11
  | x _ act => if act then 10 else 11
  | y _ act => if act then 10 else 8
  | u _ _ _ => 10

/-- the size of an item -/
def size (r : ℤ) (it : Item) : ℤ :=
  d0 it + r * (d1 it + r * (d2 it + r * (d3 it + r * d4 it)))

/-- the indices of an admissible item lie between `1` and `q` -/
def ok (q : ℕ) : Item → Prop
  | w i _ => 1 ≤ i ∧ i ≤ q
  | x j _ => 1 ≤ j ∧ j ≤ q
  | y k _ => 1 ≤ k ∧ k ≤ q
  | u i j k => (1 ≤ i ∧ i ≤ q) ∧ (1 ≤ j ∧ j ≤ q) ∧ (1 ≤ k ∧ k ≤ q)

theorem size_w (r : ℤ) (i : ℕ) (act : Bool) :
    size r (w i act) = (if act then 10 else 11) * r ^ 4 + i * r + 1 := by
  unfold size d0 d1 d2 d3 d4; ring
theorem size_x (r : ℤ) (j : ℕ) (act : Bool) :
    size r (x j act) = (if act then 10 else 11) * r ^ 4 + j * r ^ 2 + 2 := by
  unfold size d0 d1 d2 d3 d4; ring
theorem size_y (r : ℤ) (k : ℕ) (act : Bool) :
    size r (y k act) = (if act then 10 else 8) * r ^ 4 + k * r ^ 3 + 4 := by
  unfold size d0 d1 d2 d3 d4; ring
theorem size_u (r : ℤ) (i j k : ℕ) :
    size r (u i j k) = 10 * r ^ 4 - k * r ^ 3 - j * r ^ 2 - i * r + 8 := by
  unfold size d0 d1 d2 d3 d4; ring

/-- uniqueness of a balanced representation in base `r` with five digits -/
theorem digits_zero {r c0 c1 c2 c3 c4 : ℤ} (hr : 0 < r)
    (h0 : |c0| < r) (h1 : |c1| < r) (h2 : |c2| < r) (h3 : |c3| < r)
    (h : c0 + r * (c1 + r * (c2 + r * (c3 + r * c4))) = 0) :
    c0 = 0 ∧ c1 = 0 ∧ c2 = 0 ∧ c3 = 0 ∧ c4 = 0 := by
  have hr' : r ≠ 0 := ne_of_gt hr
  have e0 : c0 = 0 :=
    Int.eq_zero_of_abs_lt_dvd ⟨-(c1 + r * (c2 + r * (c3 + r * c4))), by linarith⟩ h0
  have s1 : c1 + r * (c2 + r * (c3 + r * c4)) = 0 := by
    have : r * (c1 + r * (c2 + r * (c3 + r * c4))) = 0 := by linarith
    exact (mul_eq_zero.mp this).resolve_left hr'
  have e1 : c1 = 0 := Int.eq_zero_of_abs_lt_dvd ⟨-(c2 + r * (c3 + r * c4)), by linarith⟩ h1
  have s2 : c2 + r * (c3 + r * c4) = 0 := by
    have : r * (c2 + r * (c3 + r * c4)) = 0 := by linarith
    exact (mul_eq_zero.mp this).resolve_left hr'
  have e2 : c2 = 0 := Int.eq_zero_of_abs_lt_dvd ⟨-(c3 + r * c4), by linarith⟩ h2
  have s3 : c3 + r * c4 = 0 := by
    have : r * (c3 + r * c4) = 0 := by linarith
    exact (mul_eq_zero.mp this).resolve_left hr'
  have e3 : c3 = 0 := Int.eq_zero_of_abs_lt_dvd ⟨-c4, by linarith⟩ h3
  have e4 : c4 = 0 := by
    have : r * c4 = 0 := by linarith
    exact (mul_eq_zero.mp this).resolve_left hr'
  exact ⟨e0, e1, e2, e3, e4⟩

theorem d0_bounds (it : Item) : 1 ≤ d0 it ∧ d0 it ≤ 8 := by cases it <;> simp [d0]

theorem d1_bound {q : ℕ} {it : Item} (h : ok q it) : |d1 it| ≤ q := by
  cases it <;> simp only [d1, ok] at * <;> simp <;> omega
theorem d2_bound {q : ℕ} {it : Item} (h : ok q it) : |d2 it| ≤ q := by
  cases it <;> simp only [d2, ok] at * <;> simp <;> omega
theorem d3_bound {q : ℕ} {it : Item} (h : ok q it) : |d3 it| ≤ q := by
  cases it <;> simp only [d3, ok] at * <;> simp <;> omega

theorem abs4_lt {q : ℤ} {p1 p2 p3 p4 : ℤ} (hq : 1 ≤ q) (h1 : |p1| ≤ q) (h2 : |p2| ≤ q) (h3 : |p3| ≤ q)
    (h4 : |p4| ≤ q) : |p1 + p2 + p3 + p4| < 32 * q := by
  rw [abs_le] at h1 h2 h3 h4
  rw [abs_lt]
  constructor <;> linarith

/-- the digit equations that follow from "four sizes add up to `B`" -/
theorem digit_equations {q : ℕ} (hq : 1 ≤ q) {a b c d : Item}
    (ha : ok q a) (hb : ok q b) (hc : ok q c) (hd : ok q d)
    (h : size (32 * q) a + size (32 * q) b + size (32 * q) c + size (32 * q) d = 40 * (32 * (q : ℤ)) ^ 4 + 15) :
    d0 a + d0 b + d0 c + d0 d = 15 ∧ d1 a + d1 b + d1 c + d1 d = 0 ∧ d2 a + d2 b + d2 c + d2 d = 0 ∧
      d3 a + d3 b + d3 c + d3 d = 0 ∧ d4 a + d4 b + d4 c + d4 d = 40 := by
  have hq' : (1 : ℤ) ≤ q := by exact_mod_cast hq
  have hr : (0 : ℤ) < 32 * q := by linarith
  have key := @digits_zero (32 * q) (d0 a + d0 b + d0 c + d0 d - 15) (d1 a + d1 b + d1 c + d1 d)
    (d2 a + d2 b + d2 c + d2 d) (d3 a + d3 b + d3 c + d3 d) (d4 a + d4 b + d4 c + d4 d - 40) hr
    (by
      have := d0_bounds a; have := d0_bounds b; have := d0_bounds c; have := d0_bounds d
      rw [abs_lt]; constructor <;> linarith)
    (abs4_lt hq' (d1_bound ha) (d1_bound hb) (d1_bound hc) (d1_bound hd))
    (abs4_lt hq' (d2_bound ha) (d2_bound hb) (d2_bound hc) (d2_bound hd))
    (abs4_lt hq' (d3_bound ha) (d3_bound hb) (d3_bound hc) (d3_bound hd))
    (by unfold size at h; linear_combination h)
  obtain ⟨k0, k1, k2, k3, k4⟩ := key
  exact ⟨by linarith, k1, k2, k3, by linarith⟩

/-! Selectors used to name the witnesses of `four_sum` uniformly in all cases. -/
def isU : Item → Bool | u _ _ _ => true | _ => false
def isW : Item → Bool | w _ _ => true | _ => false
def pickU (a b c d : Item) : Item := if isU a then a else if isU b then b else if isU c then c else d
def pickW (a b c d : Item) : Item := if isW a then a else if isW b then b else if isW c then c else d
def idxI : Item → ℕ | u i _ _ => i | _ => 0
def idxJ : Item → ℕ | u _ j _ => j | _ => 0
def idxK : Item → ℕ | u _ _ k => k | _ => 0
def flag : Item → Bool | w _ act => act | _ => true

/-- **Lemma A2, the four-element property.**  Four admissible items whose sizes add up to the bin size are
`u i j k` together with copies of `w i`, `x j`, `y k`, all actual or all dummy. -/
theorem four_sum {q : ℕ} (hq : 1 ≤ q) {a b c d : Item}
    (ha : ok q a) (hb : ok q b) (hc : ok q c) (hd : ok q d)
    (h : size (32 * q) a + size (32 * q) b + size (32 * q) c + size (32 * q) d = 40 * (32 * (q : ℤ)) ^ 4 + 15) :
    ∃ i j k act, ({a} + {b} + {c} + {d} : Multiset Item) =
      {u i j k} + {w i act} + {x j act} + {y k act} := by
  obtain ⟨h0, h1, h2, h3, h4⟩ := digit_equations hq ha hb hc hd h
  refine ⟨idxI (pickU a b c d), idxJ (pickU a b c d), idxK (pickU a b c d), flag (pickW a b c d), ?_⟩
  clear h ha hb hc hd
  cases a <;> cases b <;> cases c <;> cases d <;>
    simp only [d0, d1, d2, d3, d4] at h0 h1 h2 h3 h4 <;>
    first
      | omega
      | (simp only [pickU, pickW, isU, isW, idxI, idxJ, idxK, flag, if_true, if_false, Bool.false_eq_true]
         simp only [add_zero, zero_add] at h1 h2 h3
         first | rw [add_neg_eq_zero] at h1 | rw [neg_add_eq_zero] at h1
         first | rw [add_neg_eq_zero] at h2 | rw [neg_add_eq_zero] at h2
         first | rw [add_neg_eq_zero] at h3 | rw [neg_add_eq_zero] at h3
         norm_cast at h1 h2 h3
         subst h1 h2 h3
         split_ifs at h4 <;>
           first
             | omega
             | (try simp only [Bool.not_eq_true] at *
                subst_vars
                abel))

/-- conversely, an item `u i j k` with copies of its three elements, all actual or all dummy, fills a bin -/
theorem sum_good (r : ℤ) (i j k : ℕ) (act : Bool) :
    size r (u i j k) + size r (w i act) + size r (x j act) + size r (y k act) = 40 * r ^ 4 + 15 := by
  cases act <;> simp [size, d0, d1, d2, d3, d4] <;> ring

/-- every admissible item is strictly between a fifth and a third of the bin size -/
theorem size_bounds {q : ℕ} (hq : 1 ≤ q) {it : Item} (h : ok q it) :
    40 * (32 * (q : ℤ)) ^ 4 + 15 < 5 * size (32 * q) it ∧
      3 * size (32 * q) it < 40 * (32 * (q : ℤ)) ^ 4 + 15 := by
  have hq' : (1 : ℤ) ≤ q := by exact_mod_cast hq
  obtain ⟨R, hRdef⟩ : ∃ R : ℤ, R = 32 * q := ⟨_, rfl⟩
  rw [← hRdef]
  have hR : 32 ≤ R := by linarith
  have hR0 : 0 ≤ R := by linarith
  have p2 : 32 * R ≤ R ^ 2 := by nlinarith
  have p3 : 32 * R ^ 2 ≤ R ^ 3 := by nlinarith [sq_nonneg R]
  have p4 : 32 * R ^ 3 ≤ R ^ 4 := by nlinarith [pow_nonneg hR0 3]
  have idx : ∀ i : ℕ, 1 ≤ i → i ≤ q → (1 : ℤ) ≤ i ∧ 32 * (i : ℤ) ≤ R := by
    intro i h1 h2
    refine ⟨by exact_mod_cast h1, ?_⟩
    have : (i : ℤ) ≤ q := by exact_mod_cast h2
    linarith
  have mono : ∀ a : ℤ, 1 ≤ a → 32 * a ≤ R →
      0 ≤ a * R ∧ 32 * (a * R) ≤ R ^ 2 ∧ 0 ≤ a * R ^ 2 ∧ 32 * (a * R ^ 2) ≤ R ^ 3 ∧
        0 ≤ a * R ^ 3 ∧ 32 * (a * R ^ 3) ≤ R ^ 4 := by
    intro a ha1 ha2
    have a0 : 0 ≤ a := by linarith
    refine ⟨by positivity, by nlinarith, by positivity, ?_, by positivity, ?_⟩
    · nlinarith [mul_le_mul_of_nonneg_right ha2 (sq_nonneg R)]
    · nlinarith [mul_le_mul_of_nonneg_right ha2 (pow_nonneg hR0 3)]
  cases it with
  | w i act =>
    obtain ⟨hi1, hi2⟩ := idx i h.1 h.2
    obtain ⟨m0, m1, -, -, -, -⟩ := mono i hi1 hi2
    rw [size_w]
    cases act <;> simp only [if_true, if_false, Bool.false_eq_true] <;> constructor <;> nlinarith
  | x j act =>
    obtain ⟨hj1, hj2⟩ := idx j h.1 h.2
    obtain ⟨-, -, m0, m1, -, -⟩ := mono j hj1 hj2
    rw [size_x]
    cases act <;> simp only [if_true, if_false, Bool.false_eq_true] <;> constructor <;> nlinarith
  | y k act =>
    obtain ⟨hk1, hk2⟩ := idx k h.1 h.2
    obtain ⟨-, -, -, -, m0, m1⟩ := mono k hk1 hk2
    rw [size_y]
    cases act <;> simp only [if_true, if_false, Bool.false_eq_true] <;> constructor <;> nlinarith
  | u i j k =>
    obtain ⟨hi1, hi2⟩ := idx i h.1.1 h.1.2
    obtain ⟨hj1, hj2⟩ := idx j h.2.1.1 h.2.1.2
    obtain ⟨hk1, hk2⟩ := idx k h.2.2.1 h.2.2.2
    obtain ⟨a0, a1, -, -, -, -⟩ := mono i hi1 hi2
    obtain ⟨-, -, b0, b1, -, -⟩ := mono j hj1 hj2
    obtain ⟨-, -, -, -, c0, c1⟩ := mono k hk1 hk2
    rw [size_u]
    constructor <;> nlinarith

end Complexity.FourPartition

#print axioms Complexity.FourPartition.size_bounds
#print axioms Complexity.FourPartition.four_sum
#print axioms Complexity.FourPartition.sum_good
