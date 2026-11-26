/-
The orbit formula behind docs/complexity/STRANDS_ALGORITHM.md, Lemma 2 (CX-T10), for an arbitrary
permutation `ρ` of a finite set with `ρ ^ c = 1` (a cyclic group of order dividing `c` acting):

  with  R x = #{ j < c | ρ^j x = x }   (the order of the stabiliser, counted inside `ℤ/c`)
  and   J k d = Σ_{e | d} μ(d/e) e^k  (Jordan's totient with an integer exponent `k`, possibly negative),

      Σ_x (R x)^k · g x  =  Σ_{d | c} J k d · Σ_{x : ρ^(c/d) x = x} g x       for every g : X → ℚ.

With `k = 1 - α` and `g = w^α` this is formula (1) of the working paper (after division by `c`);
`k = 1` is Burnside's lemma, `k = 0` says that only `d = 1` contributes.

Checked with:  lake env lean experiments/complexity/lean/JordanOrbit.lean
-/
import Mathlib

namespace Complexity.JordanOrbit

open Finset

/-- Jordan's totient with integer exponent, as a Möbius transform. -/
noncomputable def jordan (k : ℤ) (n : ℕ) : ℚ :=
  ∑ x ∈ n.divisorsAntidiagonal, (ArithmeticFunction.moebius x.1 : ℚ) * (x.2 : ℚ) ^ k

/-- `Σ_{d | n} J_k(d) = n^k`. -/
theorem sum_jordan (k : ℤ) {n : ℕ} (hn : 0 < n) : ∑ d ∈ n.divisors, jordan k d = (n : ℚ) ^ k := by
  have h := (ArithmeticFunction.sum_eq_iff_sum_mul_moebius_eq
    (f := fun d => jordan k d) (g := fun m : ℕ => (m : ℚ) ^ k)).mpr (fun m _ => rfl)
  exact h n hn

/-- `J_0(d) = [d = 1]`. -/
theorem jordan_zero (n : ℕ) : jordan 0 n = if n = 1 then 1 else 0 := by
  unfold jordan
  simp only [zpow_zero, mul_one]
  have h := ArithmeticFunction.coe_moebius_mul_coe_zeta (R := ℚ)
  have h2 : ((ArithmeticFunction.moebius : ArithmeticFunction ℤ) : ArithmeticFunction ℚ) *
      (ArithmeticFunction.zeta : ArithmeticFunction ℚ) = 1 := h
  have h3 := congrArg (fun F : ArithmeticFunction ℚ => F n) h2
  simp only [ArithmeticFunction.mul_apply, ArithmeticFunction.one_apply] at h3
  rw [← h3]
  apply Finset.sum_congr rfl
  intro x hx
  have hx2 : x.2 ≠ 0 := by
    have := Nat.mem_divisorsAntidiagonal.mp hx
    intro h0
    rw [h0, mul_zero] at this
    exact this.2 this.1.symm
  simp [ArithmeticFunction.natCoe_apply, ArithmeticFunction.zeta_apply, hx2]

/-- `ρ^j` fixes `x` iff the minimal period of `x` divides `j`. -/
theorem pow_fix_iff {X : Type*} (ρ : Equiv.Perm X) (x : X) (j : ℕ) :
    (ρ ^ j) x = x ↔ Function.minimalPeriod (⇑ρ) x ∣ j := by
  rw [← Function.isPeriodicPt_iff_minimalPeriod_dvd]
  unfold Function.IsPeriodicPt Function.IsFixedPt
  rw [Equiv.Perm.iterate_eq_pow]

theorem minimalPeriod_dvd {X : Type*} (ρ : Equiv.Perm X) (c : ℕ) (hρ : ρ ^ c = 1) (x : X) :
    Function.minimalPeriod (⇑ρ) x ∣ c := by
  rw [← pow_fix_iff ρ x c, hρ]
  rfl

theorem minimalPeriod_pos {X : Type*} (ρ : Equiv.Perm X) (c : ℕ) (hc : 0 < c) (hρ : ρ ^ c = 1) (x : X) :
    0 < Function.minimalPeriod (⇑ρ) x :=
  Nat.pos_of_dvd_of_pos (minimalPeriod_dvd ρ c hρ x) hc

theorem card_multiples_range {p c : ℕ} (hp : 0 < p) (hpc : p ∣ c) :
    ((range c).filter (fun j => p ∣ j)).card = c / p := by
  obtain ⟨q, rfl⟩ := hpc
  rw [Nat.mul_div_cancel_left q hp]
  have : (range (p * q)).filter (fun j => p ∣ j) = (range q).image (fun i => p * i) := by
    ext j
    simp only [mem_filter, mem_range, mem_image]
    constructor
    · rintro ⟨hj, i, rfl⟩
      exact ⟨i, Nat.lt_of_mul_lt_mul_left hj, rfl⟩
    · rintro ⟨i, hi, rfl⟩
      exact ⟨Nat.mul_lt_mul_of_pos_left hi hp, dvd_mul_right p i⟩
  rw [this, card_image_of_injective _ (mul_right_injective₀ (Nat.pos_iff_ne_zero.mp hp)), card_range]

variable {X : Type*} [DecidableEq X]

/-- the number of `j < c` with `ρ^j x = x` (the order of the stabiliser of `x` in `ℤ/c`) -/
def stab (ρ : Equiv.Perm X) (c : ℕ) (x : X) : ℕ := ((range c).filter (fun j => (ρ ^ j) x = x)).card

/-- the stabiliser has `c / (minimal period)` elements -/
theorem stab_eq (ρ : Equiv.Perm X) (c : ℕ) (hc : 0 < c) (hρ : ρ ^ c = 1) (x : X) :
    stab ρ c x = c / Function.minimalPeriod (⇑ρ) x := by
  unfold stab
  rw [← card_multiples_range (minimalPeriod_pos ρ c hc hρ x) (minimalPeriod_dvd ρ c hρ x)]
  congr 1
  apply filter_congr
  intro j _
  exact pow_fix_iff ρ x j

theorem stab_dvd (ρ : Equiv.Perm X) (c : ℕ) (hc : 0 < c) (hρ : ρ ^ c = 1) (x : X) : stab ρ c x ∣ c := by
  rw [stab_eq ρ c hc hρ x]
  exact Nat.div_dvd_of_dvd (minimalPeriod_dvd ρ c hρ x)

theorem stab_pos (ρ : Equiv.Perm X) (c : ℕ) (hc : 0 < c) (hρ : ρ ^ c = 1) (x : X) : 0 < stab ρ c x :=
  Nat.pos_of_dvd_of_pos (stab_dvd ρ c hc hρ x) hc

/-- `ρ^(c/d)` fixes `x` iff `d` divides the order of the stabiliser of `x` (for `d ∣ c`). -/
theorem fix_iff_dvd_stab (ρ : Equiv.Perm X) (c : ℕ) (hc : 0 < c) (hρ : ρ ^ c = 1) (x : X) {d : ℕ}
    (hd : d ∣ c) : (ρ ^ (c / d)) x = x ↔ d ∣ stab ρ c x := by
  rw [pow_fix_iff ρ x, stab_eq ρ c hc hρ x,
    Nat.dvd_div_iff_mul_dvd hd, Nat.dvd_div_iff_mul_dvd (minimalPeriod_dvd ρ c hρ x), mul_comm]

/-- **The orbit formula.** -/
theorem weighted_fixed_point_formula [Fintype X] (ρ : Equiv.Perm X) (c : ℕ) (hc : 0 < c)
    (hρ : ρ ^ c = 1) (g : X → ℚ) (k : ℤ) :
    ∑ x, ((stab ρ c x : ℕ) : ℚ) ^ k * g x
      = ∑ d ∈ c.divisors, jordan k d * ∑ x ∈ univ.filter (fun x => (ρ ^ (c / d)) x = x), g x := by
  have hc0 : c ≠ 0 := Nat.pos_iff_ne_zero.mp hc
  have hR : ∀ d ∈ c.divisors,
      jordan k d * ∑ x ∈ univ.filter (fun x => (ρ ^ (c / d)) x = x), g x
        = ∑ x, (if d ∣ stab ρ c x then jordan k d * g x else 0) := by
    intro d hd
    have hdc : d ∣ c := (Nat.mem_divisors.mp hd).1
    rw [mul_sum, sum_filter]
    apply sum_congr rfl
    intro x _
    by_cases h : (ρ ^ (c / d)) x = x
    · rw [if_pos h, if_pos ((fix_iff_dvd_stab ρ c hc hρ x hdc).mp h)]
    · rw [if_neg h, if_neg (fun h' => h ((fix_iff_dvd_stab ρ c hc hρ x hdc).mpr h'))]
  rw [sum_congr rfl hR, sum_comm]
  apply sum_congr rfl
  intro x _
  rw [← sum_filter, ← sum_mul, Nat.divisors_filter_dvd_of_dvd hc0 (stab_dvd ρ c hc hρ x),
    sum_jordan k (stab_pos ρ c hc hρ x)]

/-- `k = 0`: only `d = 1` contributes (the classical division by the symmetry number). -/
theorem sum_eq_fixed_one [Fintype X] (ρ : Equiv.Perm X) (c : ℕ) (hc : 0 < c) (hρ : ρ ^ c = 1)
    (g : X → ℚ) :
    ∑ x, g x = ∑ d ∈ c.divisors, jordan 0 d * ∑ x ∈ univ.filter (fun x => (ρ ^ (c / d)) x = x), g x := by
  rw [← weighted_fixed_point_formula ρ c hc hρ g 0]
  simp

end Complexity.JordanOrbit
