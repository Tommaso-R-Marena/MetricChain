import Mathlib

/-!
# Theorem 3: the basin bound for ensembles with uniform low-order marginals

Science division, workstream L1.  Source: `docs/science/INFERENCE_LIMITS.md` §3, Theorem 3:

> Let `μ` be any probability measure on `{0,1}ⁿ` with uniform marginals on every set of at most
> `k` coordinates, and `t = ⌊k/2⌋`.  With `f(x) = Σ_{|T| ≤ t} χ_T(a) χ_T(x)` and
> `M_t = Σ_{j ≤ t} C(n,j)`: `E_μ f² = M_t`, hence `μ(B)·min_B f² ≤ M_t` (Markov); in particular
> `μ({a}) ≤ 1/M_t`.

## What is proved

For a finite alphabet `A` with a balanced sign `s : A → ℝ` (`∑ b, s b = 0`, `s b * s b = 1`;
for `A = Bool`: `s = ±1`), characters `chi s T x = ∏ i ∈ T, s (x i)`:

* `chi_mul_chi` — `χ_T χ_{T'} = χ_{T ∆ T'}`;
* `sum_mul_chi_eq_zero` — a uniform marginal on a non-empty `T` gives `E_μ χ_T = 0`;
* `sum_mul_sq_eq_card` — `E_μ f² = M_t` when `2 t ≤ k`, where `M_t` is the number of subsets of
  the index set with at most `t` elements;
* `basin_bound` — **Theorem 3**, Markov form: if `m ≤ f(x)²` on a set `B` of configurations
  then `m · μ(B) ≤ M_t`;
* `point_mass_le` — `μ({a}) ≤ 1 / M_t` (the weighted form of Rao's bound);
* `card_subsets_le` — `M_t = ∑_{j ≤ t} C(n, j)`;
* `theorem3_bool`, `theorem3_point_mass_bool` — the statements on `{0,1}ⁿ = ι → Bool`.

## Differences from the note

* The ball bound is stated for an arbitrary set `B` and any lower bound `m` of `f²` on `B`
  (`μ(B) ≤ M_t / min_B f²`).  The identification `f(x) = F_t(d_H(x, a))` with Krawtchouk
  polynomials, which turns `B` into a Hamming ball and `m` into `min_{d ≤ r} F_t(d)²`, is **not**
  formalised; nor are the asymptotics.
* `t` is any natural number with `2 t ≤ k` (the note takes `t = ⌊k/2⌋`).
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL1

open Finset

variable {ι A : Type*} [Fintype ι] [DecidableEq ι] [Fintype A] [DecidableEq A]

/-- The character `χ_T(x) = ∏_{i ∈ T} s (x i)` for a sign function `s` on the alphabet. -/
def chi (s : A → ℝ) (T : Finset ι) (x : ι → A) : ℝ := ∏ i ∈ T, s (x i)

omit [Fintype A] [DecidableEq A] in
theorem chi_eq_prod_ite (s : A → ℝ) (T : Finset ι) (x : ι → A) :
    chi s T x = ∏ i, if i ∈ T then s (x i) else 1 := by
  unfold chi
  rw [Finset.prod_ite_mem, Finset.univ_inter]

omit [Fintype A] [DecidableEq A] in
/-- `χ_T · χ_{T'} = χ_{T ∆ T'}` for a sign with `s² = 1`. -/
theorem chi_mul_chi (s : A → ℝ) (hs1 : ∀ b, s b * s b = 1) (T T' : Finset ι) (x : ι → A) :
    chi s T x * chi s T' x = chi s (symmDiff T T') x := by
  rw [chi_eq_prod_ite, chi_eq_prod_ite, chi_eq_prod_ite, ← Finset.prod_mul_distrib]
  refine Finset.prod_congr rfl fun i _ => ?_
  have ha := hs1 (x i)
  by_cases h1 : i ∈ T <;> by_cases h2 : i ∈ T' <;> simp [Finset.mem_symmDiff, h1, h2, ha]

omit [Fintype ι] [DecidableEq ι] [Fintype A] [DecidableEq A] in
theorem chi_empty (s : A → ℝ) (x : ι → A) : chi s (∅ : Finset ι) x = 1 := by
  unfold chi
  rw [Finset.prod_empty]

/-- **A uniform marginal kills the character.**  If the marginal of `μ` on a non-empty set `T`
of coordinates is uniform and the sign `s` is balanced, then `E_μ χ_T = 0`. -/
theorem sum_mul_chi_eq_zero (s : A → ℝ) (hs0 : ∑ b, s b = 0) (μ : (ι → A) → ℝ)
    (T : Finset ι) (hT : T.Nonempty)
    (hmarg : ∀ y : ι → A, ∑ x ∈ univ.filter (fun x : ι → A => ∀ i ∈ T, x i = y i), μ x =
      1 / (Fintype.card A : ℝ) ^ T.card) :
    ∑ x, μ x * chi s T x = 0 := by
  obtain ⟨i₀, h₀⟩ := hT
  have hfib : ∑ x, μ x * chi s T x =
      ∑ z : T → A, ∑ x ∈ univ.filter (fun x : ι → A => (fun i : T => x i) = z),
        μ x * chi s T x :=
    (Finset.sum_fiberwise univ (fun x : ι → A => (fun i : T => x i))
      (fun x => μ x * chi s T x)).symm
  have hinner : ∀ z : T → A,
      ∑ x ∈ univ.filter (fun x : ι → A => (fun i : T => x i) = z), μ x * chi s T x =
        (1 / (Fintype.card A : ℝ) ^ T.card) * ∏ i : T, s (z i) := by
    intro z
    have hchi : ∀ x ∈ univ.filter (fun x : ι → A => (fun i : T => x i) = z),
        μ x * chi s T x = μ x * ∏ i : T, s (z i) := by
      intro x hx
      have hxz : (fun i : T => x i) = z := (Finset.mem_filter.mp hx).2
      congr 1
      unfold chi
      rw [← Finset.prod_coe_sort T (fun i => s (x i))]
      refine Finset.prod_congr rfl fun i _ => ?_
      rw [← hxz]
    rw [Finset.sum_congr rfl hchi, ← Finset.sum_mul]
    congr 1
    have hy := hmarg (fun i => if h : i ∈ T then z ⟨i, h⟩ else z ⟨i₀, h₀⟩)
    rw [← hy]
    refine Finset.sum_congr (Finset.filter_congr fun x _ => ?_) fun _ _ => rfl
    constructor
    · intro h i hi
      show x i = if h : i ∈ T then z ⟨i, h⟩ else z ⟨i₀, h₀⟩
      rw [dif_pos hi]
      exact congrFun h ⟨i, hi⟩
    · intro h
      funext i
      have h1 : x i = if h : (i : ι) ∈ T then z ⟨i, h⟩ else z ⟨i₀, h₀⟩ := h i i.2
      rw [dif_pos i.2] at h1
      exact h1
  have hprod : ∑ z : T → A, ∏ i : T, s (z i) = ∏ _i : T, ∑ b, s b := by
    rw [Finset.prod_univ_sum, Fintype.piFinset_univ]
  rw [hfib, Finset.sum_congr rfl fun z _ => hinner z, ← Finset.mul_sum, hprod, hs0]
  have hzero : ∏ _i : T, (0 : ℝ) = 0 :=
    Finset.prod_eq_zero (Finset.mem_univ (⟨i₀, h₀⟩ : T)) rfl
  rw [hzero, mul_zero]

omit [DecidableEq A] in
/-- **`E_μ f² = M_t`.**  If `E_μ χ_U = 0` for every non-empty `U` with at most `k` elements,
`2 t ≤ k`, and `μ` has total mass `1`, then for `f(x) = ∑_{|T| ≤ t} χ_T(a) χ_T(x)`:
`∑ x, μ x · f(x)² = #{T : |T| ≤ t}`. -/
theorem sum_mul_sq_eq_card (s : A → ℝ) (hs1 : ∀ b, s b * s b = 1) (μ : (ι → A) → ℝ)
    (hμ1 : ∑ x, μ x = 1) (k t : ℕ) (hkt : 2 * t ≤ k)
    (hchar : ∀ U : Finset ι, U.Nonempty → U.card ≤ k → ∑ x, μ x * chi s U x = 0)
    (a : ι → A) :
    ∑ x, μ x * (∑ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
        chi s T a * chi s T x) ^ 2 =
      ((univ.filter fun T : Finset ι => T.card ≤ t).card : ℝ) := by
  -- orthogonality of the characters under `μ`
  have horth : ∀ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
      ∀ T' ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
      ∑ x, μ x * chi s (symmDiff T T') x = if T = T' then 1 else 0 := by
    intro T hT T' hT'
    have hTc : T.card ≤ t := (Finset.mem_filter.mp hT).2
    have hTc' : T'.card ≤ t := (Finset.mem_filter.mp hT').2
    split_ifs with h
    · subst h
      have he : symmDiff T T = (∅ : Finset ι) := by
        rw [symmDiff_self]
        rfl
      rw [he]
      have : ∀ x : ι → A, μ x * chi s (∅ : Finset ι) x = μ x := fun x => by
        rw [chi_empty, mul_one]
      rw [Finset.sum_congr rfl fun x _ => this x]
      exact hμ1
    · refine hchar _ ?_ ?_
      · refine Finset.nonempty_iff_ne_empty.mpr fun h0 => h ?_
        exact symmDiff_eq_bot.mp (h0.trans Finset.bot_eq_empty.symm)
      · have hsub : symmDiff T T' ⊆ T ∪ T' := by
          intro i hi
          rw [Finset.mem_symmDiff] at hi
          rw [Finset.mem_union]
          tauto
        have h1 := Finset.card_le_card hsub
        have h2 := Finset.card_union_le T T'
        omega
  -- expand the square
  have hsq : ∀ x : ι → A,
      μ x * (∑ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t), chi s T a * chi s T x) ^ 2 =
        ∑ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
          ∑ T' ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
            chi s T a * chi s T' a * (μ x * chi s (symmDiff T T') x) := by
    intro x
    rw [sq, Finset.sum_mul_sum, Finset.mul_sum]
    refine Finset.sum_congr rfl fun T _ => ?_
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun T' _ => ?_
    rw [← chi_mul_chi s hs1 T T' x]
    ring
  rw [Finset.sum_congr rfl fun x _ => hsq x, Finset.sum_comm]
  have hstep : ∀ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
      ∑ x, ∑ T' ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
        chi s T a * chi s T' a * (μ x * chi s (symmDiff T T') x) = 1 := by
    intro T hT
    rw [Finset.sum_comm]
    have hin : ∀ T' ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
        ∑ x, chi s T a * chi s T' a * (μ x * chi s (symmDiff T T') x) =
          if T = T' then chi s T a * chi s T' a else 0 := by
      intro T' hT'
      rw [← Finset.mul_sum, horth T hT T' hT']
      split_ifs <;> simp
    rw [Finset.sum_congr rfl hin, Finset.sum_ite_eq, if_pos hT, chi_mul_chi s hs1 T T a]
    have he : symmDiff T T = (∅ : Finset ι) := by
      rw [symmDiff_self]
      rfl
    rw [he, chi_empty]
  rw [Finset.sum_congr rfl hstep, Finset.sum_const, nsmul_eq_mul, mul_one]

/-- **Theorem 3 (basin bound), Markov form.**  `μ` a probability vector on `ι → A` with uniform
marginals on every set of at most `k` coordinates; `s` a balanced sign; `2 t ≤ k`;
`f_a(x) = ∑_{|T| ≤ t} χ_T(a) χ_T(x)`.  For every set `B` of configurations and every `m` with
`m ≤ f_a(x)²` on `B`:  `m · μ(B) ≤ M_t = #{T : |T| ≤ t}`. -/
theorem basin_bound (s : A → ℝ) (hs0 : ∑ b, s b = 0) (hs1 : ∀ b, s b * s b = 1)
    (μ : (ι → A) → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hμ1 : ∑ x, μ x = 1) (k t : ℕ) (hkt : 2 * t ≤ k)
    (hmarg : ∀ S : Finset ι, S.card ≤ k → ∀ y : ι → A,
      ∑ x ∈ univ.filter (fun x : ι → A => ∀ i ∈ S, x i = y i), μ x =
        1 / (Fintype.card A : ℝ) ^ S.card)
    (a : ι → A) (B : Finset (ι → A)) (m : ℝ)
    (hm : ∀ x ∈ B, m ≤ (∑ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
      chi s T a * chi s T x) ^ 2) :
    m * ∑ x ∈ B, μ x ≤ ((univ.filter fun T : Finset ι => T.card ≤ t).card : ℝ) := by
  have hE := sum_mul_sq_eq_card s hs1 μ hμ1 k t hkt
    (fun U hU hUk => sum_mul_chi_eq_zero s hs0 μ U hU (hmarg U hUk)) a
  rw [← hE, Finset.mul_sum]
  calc ∑ x ∈ B, m * μ x
      ≤ ∑ x ∈ B, μ x * (∑ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
          chi s T a * chi s T x) ^ 2 := by
        refine Finset.sum_le_sum fun x hx => ?_
        have := mul_le_mul_of_nonneg_left (hm x hx) (hμ x)
        linarith
    _ ≤ ∑ x, μ x * (∑ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
          chi s T a * chi s T x) ^ 2 :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ B)
          fun x _ _ => mul_nonneg (hμ x) (sq_nonneg _)

/-- **Point masses.**  Under the hypotheses of `basin_bound`, every configuration has weight at
most `1 / M_t`. -/
theorem point_mass_le (s : A → ℝ) (hs0 : ∑ b, s b = 0) (hs1 : ∀ b, s b * s b = 1)
    (μ : (ι → A) → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hμ1 : ∑ x, μ x = 1) (k t : ℕ) (hkt : 2 * t ≤ k)
    (hmarg : ∀ S : Finset ι, S.card ≤ k → ∀ y : ι → A,
      ∑ x ∈ univ.filter (fun x : ι → A => ∀ i ∈ S, x i = y i), μ x =
        1 / (Fintype.card A : ℝ) ^ S.card)
    (a : ι → A) :
    μ a ≤ 1 / ((univ.filter fun T : Finset ι => T.card ≤ t).card : ℝ) := by
  -- `f_a(a) = M_t`
  have hfa : ∑ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t), chi s T a * chi s T a =
      ((univ.filter fun T : Finset ι => T.card ≤ t).card : ℝ) := by
    have h1 : ∀ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
        chi s T a * chi s T a = 1 := by
      intro T _
      rw [chi_mul_chi s hs1 T T a]
      have he : symmDiff T T = (∅ : Finset ι) := by
        rw [symmDiff_self]
        rfl
      rw [he, chi_empty]
    rw [Finset.sum_congr rfl h1, Finset.sum_const, nsmul_eq_mul, mul_one]
  have hMpos : (0 : ℝ) < ((univ.filter fun T : Finset ι => T.card ≤ t).card : ℝ) := by
    have hmem : (∅ : Finset ι) ∈ univ.filter fun T : Finset ι => T.card ≤ t :=
      Finset.mem_filter.mpr ⟨Finset.mem_univ _, by simp⟩
    exact_mod_cast Finset.card_pos.mpr ⟨∅, hmem⟩
  have hb := basin_bound s hs0 hs1 μ hμ hμ1 k t hkt hmarg a {a}
    (((univ.filter fun T : Finset ι => T.card ≤ t).card : ℝ) ^ 2)
    (fun x hx => by
      rw [Finset.mem_singleton.mp hx, hfa])
  rw [Finset.sum_singleton] at hb
  rw [le_div_iff₀ hMpos]
  nlinarith

omit [DecidableEq ι] in
/-- `M_t = ∑_{j ≤ t} C(n, j)`: the number of subsets of the index set with at most `t`
elements. -/
theorem card_subsets_le (t : ℕ) :
    (univ.filter fun T : Finset ι => T.card ≤ t).card =
      ∑ j ∈ Finset.range (t + 1), (Fintype.card ι).choose j := by
  classical
  rw [Finset.card_eq_sum_card_fiberwise (f := fun T : Finset ι => T.card)
    (t := Finset.range (t + 1))
    (fun T hT => Finset.mem_range.mpr (Nat.lt_succ_of_le (Finset.mem_filter.mp hT).2))]
  refine Finset.sum_congr rfl fun j hj => ?_
  have hjt : j ≤ t := Nat.lt_succ_iff.mp (Finset.mem_range.mp hj)
  have hset : ((univ.filter fun T : Finset ι => T.card ≤ t).filter fun T => T.card = j) =
      Finset.powersetCard j (univ : Finset ι) := by
    ext T
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_powersetCard,
      Finset.subset_univ]
    constructor
    · intro h
      exact h.2
    · intro h
      exact ⟨by omega, h⟩
  rw [hset, Finset.card_powersetCard, Finset.card_univ]

/-! ### The binary cube `{0,1}ⁿ` -/

/-- The sign `(-1)^b` on `Bool`. -/
def boolSign (b : Bool) : ℝ := if b then -1 else 1

theorem boolSign_sum : ∑ b, boolSign b = 0 := by
  rw [Fintype.sum_bool]
  simp [boolSign]

theorem boolSign_sq (b : Bool) : boolSign b * boolSign b = 1 := by
  cases b <;> simp [boolSign]

/-- **Theorem 3 on `{0,1}ⁿ`, Markov form.**  `μ` a probability vector on `ι → Bool` with uniform
marginals on every set of at most `k` coordinates, `2 t ≤ k`,
`f_a(x) = ∑_{|T| ≤ t} χ_T(a) χ_T(x)` with `χ_T(x) = (-1)^{∑_{i ∈ T} x_i}`.  For every set `B` of
configurations and every `m ≤ min_B f_a²`:  `m · μ(B) ≤ ∑_{j ≤ t} C(n, j)`. -/
theorem theorem3_bool (μ : (ι → Bool) → ℝ) (hμ : ∀ x, 0 ≤ μ x) (hμ1 : ∑ x, μ x = 1)
    (k t : ℕ) (hkt : 2 * t ≤ k)
    (hmarg : ∀ S : Finset ι, S.card ≤ k → ∀ y : ι → Bool,
      ∑ x ∈ univ.filter (fun x : ι → Bool => ∀ i ∈ S, x i = y i), μ x = 1 / (2 : ℝ) ^ S.card)
    (a : ι → Bool) (B : Finset (ι → Bool)) (m : ℝ)
    (hm : ∀ x ∈ B, m ≤ (∑ T ∈ univ.filter (fun T : Finset ι => T.card ≤ t),
      chi boolSign T a * chi boolSign T x) ^ 2) :
    m * ∑ x ∈ B, μ x ≤ ((∑ j ∈ Finset.range (t + 1), (Fintype.card ι).choose j : ℕ) : ℝ) := by
  have h := basin_bound boolSign boolSign_sum boolSign_sq μ hμ hμ1 k t hkt
    (fun S hS y => by
      rw [hmarg S hS y, Fintype.card_bool]
      norm_num) a B m hm
  rw [card_subsets_le] at h
  exact h

/-- **Theorem 3 on `{0,1}ⁿ`, point masses** (`r = 0`): `μ({a}) ≤ 1 / ∑_{j ≤ t} C(n, j)`. -/
theorem theorem3_point_mass_bool (μ : (ι → Bool) → ℝ) (hμ : ∀ x, 0 ≤ μ x)
    (hμ1 : ∑ x, μ x = 1) (k t : ℕ) (hkt : 2 * t ≤ k)
    (hmarg : ∀ S : Finset ι, S.card ≤ k → ∀ y : ι → Bool,
      ∑ x ∈ univ.filter (fun x : ι → Bool => ∀ i ∈ S, x i = y i), μ x = 1 / (2 : ℝ) ^ S.card)
    (a : ι → Bool) :
    μ a ≤ 1 / ((∑ j ∈ Finset.range (t + 1), (Fintype.card ι).choose j : ℕ) : ℝ) := by
  have h := point_mass_le boolSign boolSign_sum boolSign_sq μ hμ hμ1 k t hkt
    (fun S hS y => by
      rw [hmarg S hS y, Fintype.card_bool]
      norm_num) a
  rw [card_subsets_le] at h
  exact h

/-- Non-vacuity: the uniform measure on `{0,1}ⁿ` has uniform marginals of every order; here
for one site, where the bound `μ({a}) ≤ 1/M_t` with `t = 0` reads `1/2 ≤ 1`. -/
example : ∃ μ : (Fin 1 → Bool) → ℝ, (∀ x, 0 ≤ μ x) ∧ ∑ x, μ x = 1 :=
  ⟨fun _ => 1 / 2, fun _ => by norm_num, by
    rw [Finset.sum_const, Finset.card_univ]
    simp⟩

end ScienceL1

end

#print axioms ScienceL1.chi_mul_chi
#print axioms ScienceL1.sum_mul_chi_eq_zero
#print axioms ScienceL1.sum_mul_sq_eq_card
#print axioms ScienceL1.basin_bound
#print axioms ScienceL1.point_mass_le
#print axioms ScienceL1.card_subsets_le
#print axioms ScienceL1.theorem3_bool
#print axioms ScienceL1.theorem3_point_mass_bool
