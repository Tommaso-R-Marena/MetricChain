import Mathlib
import proofs.Frontiers.QueryLowerBound

/-!
# Theorem A of workstream F: the adaptive bound survives an exact one-body marginal oracle

Science division, workstream L3.  Source: `docs/science/workstreams/SF_REPORT.md` §2.0–§2.2
(setting, Lemmas 0–3, Theorem A).

This file imports Mathlib and, read-only, the theory division's
`proofs/Frontiers/QueryLowerBound.lean` (for `MetricChain.QueryAlgorithm` and the packing bound
`MetricChain.expected_queries_ge_packing`).  Parts 1–6 are repeated verbatim from
`Compensation.lean` (same directory; that file imports Mathlib only), because the files of this
directory cannot import each other.  New here:

* Part 7 — **Lemma 1 (a)** in the oracle-indexed model of workstream L1
  (`lemma1a_weighted`, `lemma1a`): an oracle algorithm is a family `alg ω o` of query algorithms
  indexed by the seed `ω` and the oracle's answer `o`; on the instance `g` it runs
  `alg ω (O g)`.  Derived from `MetricChain.expected_queries_ge_packing` applied to the class
  restricted to the instances with the oracle answer of `g₀`.
* Part 8 — the same in the weights, for the one-body marginal oracle on the cube
  (`oracle_packing_weights`); the family of alternatives of Theorem A (cyclic averages of dips,
  `barW`) with its invariance, mass, density, membership of the class and the counting bound.
* Part 9 — **Theorem A, the every-`n` statement** (`theoremA_group`, `theoremA_fin`,
  `theoremA_fin_div`).
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL3

open Finset

/-! # Parts 1–6: repeated verbatim from `Compensation.lean` -/

/-! ## Part 1: flips, the cone `𝒲_u` and the class `L_u` -/

section Cone

variable {ι : Type*} [DecidableEq ι]

/-- `x⁽ⁱ⁾`: the configuration `x` with the letter at site `i` flipped. -/
def flipAt (x : ι → Bool) (i : ι) : ι → Bool := Function.update x i (!x i)

theorem flipAt_same (x : ι → Bool) (i : ι) : flipAt x i i = !x i := by
  unfold flipAt
  rw [Function.update_self]

theorem flipAt_ne (x : ι → Bool) {i j : ι} (h : j ≠ i) : flipAt x i j = x j := by
  unfold flipAt
  rw [Function.update_of_ne h]

theorem flipAt_flipAt (x : ι → Bool) (i : ι) : flipAt (flipAt x i) i = x := by
  funext j
  by_cases h : j = i
  · subst h
    rw [flipAt_same, flipAt_same, Bool.not_not]
  · rw [flipAt_ne _ h, flipAt_ne _ h]

/-- Flipping the letter at site `i` is an involution of the cube. -/
def flipEquiv (i : ι) : (ι → Bool) ≃ (ι → Bool) where
  toFun x := flipAt x i
  invFun x := flipAt x i
  left_inv x := flipAt_flipAt x i
  right_inv x := flipAt_flipAt x i

/-- **The class in the weights**, `𝒲_u = {w > 0 : e^{−u} w(x) ≤ w(x⁽ⁱ⁾) ≤ e^{u} w(x) for all x, i}`. -/
def InCone (u : ℝ) (w : (ι → Bool) → ℝ) : Prop :=
  (∀ x, 0 < w x) ∧
    ∀ x i, Real.exp (-u) * w x ≤ w (flipAt x i) ∧ w (flipAt x i) ≤ Real.exp u * w x

/-- The upper inequality at every point implies the lower one. -/
theorem inCone_of_upper {u : ℝ} {w : (ι → Bool) → ℝ} (hpos : ∀ x, 0 < w x)
    (h : ∀ x i, w (flipAt x i) ≤ Real.exp u * w x) : InCone u w := by
  refine ⟨hpos, fun x i => ⟨?_, h x i⟩⟩
  have h' := h (flipAt x i) i
  rw [flipAt_flipAt] at h'
  have h2 := mul_le_mul_of_nonneg_left h' (Real.exp_pos (-u)).le
  rw [← mul_assoc, ← Real.exp_add, neg_add_cancel, Real.exp_zero, one_mul] at h2
  exact h2

/-- The cone is closed under sums. -/
theorem InCone.add {u : ℝ} {w v : (ι → Bool) → ℝ} (hw : InCone u w) (hv : InCone u v) :
    InCone u (fun x => w x + v x) := by
  refine inCone_of_upper (fun x => add_pos (hw.1 x) (hv.1 x)) fun x i => ?_
  have h1 := (hw.2 x i).2
  have h2 := (hv.2 x i).2
  show w (flipAt x i) + v (flipAt x i) ≤ Real.exp u * (w x + v x)
  rw [mul_add]
  exact add_le_add h1 h2

/-- The cone is closed under positive multiples. -/
theorem InCone.smul {u : ℝ} {w : (ι → Bool) → ℝ} (hw : InCone u w) {a : ℝ} (ha : 0 < a) :
    InCone u (fun x => a * w x) := by
  refine inCone_of_upper (fun x => mul_pos ha (hw.1 x)) fun x i => ?_
  have h1 := mul_le_mul_of_nonneg_left (hw.2 x i).2 ha.le
  show a * w (flipAt x i) ≤ Real.exp u * (a * w x)
  calc a * w (flipAt x i) ≤ a * (Real.exp u * w x) := h1
    _ = Real.exp u * (a * w x) := by ring

/-- A member of the cone plus a non-negative multiple of a member is a member. -/
theorem InCone.add_smul {u : ℝ} {w v : (ι → Bool) → ℝ} (hw : InCone u w) (hv : InCone u v)
    {b : ℝ} (hb : 0 ≤ b) : InCone u (fun x => w x + b * v x) := by
  refine inCone_of_upper (fun x => add_pos_of_pos_of_nonneg (hw.1 x) (mul_nonneg hb (hv.1 x).le))
    fun x i => ?_
  have h1 := (hw.2 x i).2
  have h2 := mul_le_mul_of_nonneg_left (hv.2 x i).2 hb
  show w (flipAt x i) + b * v (flipAt x i) ≤ Real.exp u * (w x + b * v x)
  calc w (flipAt x i) + b * v (flipAt x i) ≤ Real.exp u * w x + b * (Real.exp u * v x) :=
        add_le_add h1 h2
    _ = Real.exp u * (w x + b * v x) := by ring

/-- The cone is closed under pointwise maxima. -/
theorem inCone_max {u : ℝ} {w v : (ι → Bool) → ℝ} (hw : InCone u w) (hv : InCone u v) :
    InCone u (fun x => max (w x) (v x)) := by
  refine inCone_of_upper (fun x => lt_max_of_lt_left (hw.1 x)) fun x i => ?_
  have he := (Real.exp_pos u).le
  exact max_le ((hw.2 x i).2.trans (mul_le_mul_of_nonneg_left (le_max_left _ _) he))
    ((hv.2 x i).2.trans (mul_le_mul_of_nonneg_left (le_max_right _ _) he))

/-- The cone is closed under pointwise minima. -/
theorem inCone_min {u : ℝ} {w v : (ι → Bool) → ℝ} (hw : InCone u w) (hv : InCone u v) :
    InCone u (fun x => min (w x) (v x)) := by
  refine inCone_of_upper (fun x => lt_min (hw.1 x) (hv.1 x)) fun x i => ?_
  have h1 : w (flipAt x i) ≤ Real.exp u * w x := (hw.2 x i).2
  have h2 : v (flipAt x i) ≤ Real.exp u * v x := (hv.2 x i).2
  show min (w (flipAt x i)) (v (flipAt x i)) ≤ Real.exp u * min (w x) (v x)
  rcases le_total (w x) (v x) with hle | hle
  · rw [min_eq_left hle]
    exact (min_le_left _ _).trans h1
  · rw [min_eq_right hle]
    exact (min_le_right _ _).trans h2

/-- The cone is closed under finite non-empty sums. -/
theorem InCone.sum {u : ℝ} {κ : Type*} {s : Finset κ} (hs : s.Nonempty)
    {f : κ → (ι → Bool) → ℝ} (h : ∀ k ∈ s, InCone u (f k)) :
    InCone u (fun x => ∑ k ∈ s, f k x) := by
  refine inCone_of_upper (fun x => Finset.sum_pos (fun k hk => (h k hk).1 x) hs) fun x i => ?_
  show ∑ k ∈ s, f k (flipAt x i) ≤ Real.exp u * ∑ k ∈ s, f k x
  rw [Finset.mul_sum]
  exact Finset.sum_le_sum fun k hk => ((h k hk).2 x i).2

variable [Fintype ι]

/-- **The class in the energies**, `L_u = {ψ : |ψ x − ψ y| ≤ u · d_H(x, y)}`. -/
def LipH (u : ℝ) (ψ : (ι → Bool) → ℝ) : Prop := ∀ x y, |ψ x - ψ y| ≤ u * hammingDist x y

theorem hammingDist_flipAt (x : ι → Bool) (i : ι) : hammingDist (flipAt x i) x = 1 := by
  unfold hammingDist
  rw [Finset.card_eq_one]
  refine ⟨i, ?_⟩
  ext j
  simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_singleton]
  constructor
  · intro h
    by_contra hne
    exact h (flipAt_ne x hne)
  · rintro rfl
    rw [flipAt_same]
    cases x j <;> simp

/-- A function that rises by at most `u` under every single flip rises by at most `u · d_H`. -/
theorem sub_le_mul_hammingDist {u : ℝ} {ψ : (ι → Bool) → ℝ}
    (h : ∀ x i, ψ (flipAt x i) - ψ x ≤ u) (x y : ι → Bool) :
    ψ y - ψ x ≤ u * hammingDist x y := by
  induction' hd : hammingDist x y with d ih generalizing y
  · rw [hammingDist_eq_zero] at hd
    subst hd
    simp
  · have hne : x ≠ y := by
      intro hxy
      rw [← hammingDist_eq_zero, hd] at hxy
      exact Nat.succ_ne_zero d hxy
    obtain ⟨i, hi⟩ := Function.ne_iff.mp hne
    have hy : hammingDist x (flipAt y i) = d := by
      have hset : (univ.filter fun j => x j ≠ flipAt y i j) =
          (univ.filter fun j => x j ≠ y j).erase i := by
        ext j
        simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_erase]
        by_cases hj : j = i
        · subst hj
          rw [flipAt_same]
          constructor
          · intro h1
            exfalso
            revert hi h1
            cases x j <;> cases y j <;> simp
          · rintro ⟨h1, _⟩
            exact absurd rfl h1
        · rw [flipAt_ne y hj]
          exact ⟨fun h1 => ⟨hj, h1⟩, fun h1 => h1.2⟩
      have hmem : i ∈ univ.filter fun j => x j ≠ y j := by
        simp only [Finset.mem_filter, Finset.mem_univ, true_and]
        exact hi
      have hcard : (univ.filter fun j => x j ≠ y j).card = d + 1 := hd
      show (univ.filter fun j => x j ≠ flipAt y i j).card = d
      rw [hset, Finset.card_erase_of_mem hmem, hcard]
      rfl
    have h1 := ih (flipAt y i) hy
    have h2 := h (flipAt y i) i
    rw [flipAt_flipAt] at h2
    push_cast
    linarith

/-- `L_u` is the class of functions that change by at most `u` under every single flip. -/
theorem lipH_iff_flip {u : ℝ} {ψ : (ι → Bool) → ℝ} :
    LipH u ψ ↔ ∀ x i, |ψ (flipAt x i) - ψ x| ≤ u := by
  constructor
  · intro h x i
    have h1 := h (flipAt x i) x
    rw [hammingDist_flipAt] at h1
    simpa using h1
  · intro h x y
    rw [abs_le]
    constructor
    · have h1 := sub_le_mul_hammingDist (fun x i => (abs_le.mp (h x i)).2) x y
      linarith
    · have h1 := sub_le_mul_hammingDist (fun x i => (abs_le.mp (h x i)).2) y x
      rw [hammingDist_comm] at h1
      linarith

/-- **`ψ ∈ L_u` iff `e^{−ψ} ∈ 𝒲_u`.** -/
theorem lipH_iff_inCone {u : ℝ} {ψ : (ι → Bool) → ℝ} :
    LipH u ψ ↔ InCone u (fun x => Real.exp (-ψ x)) := by
  rw [lipH_iff_flip]
  constructor
  · intro h
    refine ⟨fun x => Real.exp_pos _, fun x i => ?_⟩
    have h1 := abs_le.mp (h x i)
    show Real.exp (-u) * Real.exp (-ψ x) ≤ Real.exp (-ψ (flipAt x i)) ∧
      Real.exp (-ψ (flipAt x i)) ≤ Real.exp u * Real.exp (-ψ x)
    constructor
    · rw [← Real.exp_add, Real.exp_le_exp]
      linarith [h1.2]
    · rw [← Real.exp_add, Real.exp_le_exp]
      linarith [h1.1]
  · intro h x i
    have h1 : Real.exp (-u) * Real.exp (-ψ x) ≤ Real.exp (-ψ (flipAt x i)) := (h.2 x i).1
    have h2 : Real.exp (-ψ (flipAt x i)) ≤ Real.exp u * Real.exp (-ψ x) := (h.2 x i).2
    rw [← Real.exp_add, Real.exp_le_exp] at h1 h2
    rw [abs_le]
    constructor <;> linarith

/-- **`w ∈ 𝒲_u` iff `w > 0` and `−ln w ∈ L_u`.** -/
theorem inCone_iff_lipH_log {u : ℝ} {w : (ι → Bool) → ℝ} (hw : ∀ x, 0 < w x) :
    InCone u w ↔ LipH u (fun x => -Real.log (w x)) := by
  rw [lipH_iff_inCone]
  have e : (fun x => Real.exp (-(-Real.log (w x)))) = w := by
    funext x
    rw [neg_neg, Real.exp_log (hw x)]
  rw [e]

end Cone

/-! ## Part 2: masses, one-body marginals, density; Lemma 3 (i) -/

section Marginals

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- `A(w) = Σ_x π(x) w(x)`: the mass of the weight `w` for the reference weight `π`. -/
def massW (π w : (ι → Bool) → ℝ) : ℝ := ∑ x, π x * w x

/-- The mass of `{x : x_i = 1}`. -/
def oneW (π w : (ι → Bool) → ℝ) (i : ι) : ℝ := ∑ x, if x i = true then π x * w x else 0

/-- The one-body marginal `μ_w(x_i = 1)` of the Gibbs measure `μ_w ∝ π w`. -/
def margW (π w : (ι → Bool) → ℝ) (i : ι) : ℝ := oneW π w i / massW π w

/-- `|x|`, the number of ones. -/
def wt (x : ι → Bool) : ℕ := (univ.filter fun i => x i = true).card

/-- `dens(w) = Σ_x π(x) w(x) |x| / (n · A(w))`. -/
def densW (π w : (ι → Bool) → ℝ) : ℝ :=
  (∑ x, π x * w x * (wt x : ℝ)) / ((Fintype.card ι : ℝ) * massW π w)

theorem massW_add (π w v : (ι → Bool) → ℝ) :
    massW π (fun x => w x + v x) = massW π w + massW π v := by
  unfold massW
  rw [← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl fun x _ => by ring

theorem massW_smul (π w : (ι → Bool) → ℝ) (a : ℝ) :
    massW π (fun x => a * w x) = a * massW π w := by
  unfold massW
  rw [Finset.mul_sum]
  exact Finset.sum_congr rfl fun x _ => by ring

theorem oneW_add (π w v : (ι → Bool) → ℝ) (i : ι) :
    oneW π (fun x => w x + v x) i = oneW π w i + oneW π v i := by
  unfold oneW
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun x _ => ?_
  split_ifs <;> ring

theorem oneW_smul (π w : (ι → Bool) → ℝ) (a : ℝ) (i : ι) :
    oneW π (fun x => a * w x) i = a * oneW π w i := by
  unfold oneW
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun x _ => ?_
  split_ifs <;> ring

theorem massW_pos {π w : (ι → Bool) → ℝ} (hπ : ∀ x, 0 < π x) (hw : ∀ x, 0 < w x) :
    0 < massW π w :=
  Finset.sum_pos (fun x _ => mul_pos (hπ x) (hw x)) Finset.univ_nonempty

theorem massW_nonneg {π w : (ι → Bool) → ℝ} (hπ : ∀ x, 0 ≤ π x) (hw : ∀ x, 0 ≤ w x) :
    0 ≤ massW π w :=
  Finset.sum_nonneg fun x _ => mul_nonneg (hπ x) (hw x)

theorem massW_pos_of_ne_zero {π w : (ι → Bool) → ℝ} (hπ : ∀ x, 0 < π x) (hw : ∀ x, 0 ≤ w x)
    (hw1 : ∃ x, w x ≠ 0) : 0 < massW π w := by
  obtain ⟨x₀, hx₀⟩ := hw1
  have h1 : 0 < π x₀ * w x₀ := mul_pos (hπ x₀) (lt_of_le_of_ne (hw x₀) (Ne.symm hx₀))
  have h2 : π x₀ * w x₀ ≤ massW π w :=
    Finset.single_le_sum (f := fun x => π x * w x)
      (fun x _ => mul_nonneg (hπ x).le (hw x)) (Finset.mem_univ x₀)
  linarith

theorem oneW_nonneg {π w : (ι → Bool) → ℝ} (hπ : ∀ x, 0 ≤ π x) (hw : ∀ x, 0 ≤ w x) (i : ι) :
    0 ≤ oneW π w i := by
  unfold oneW
  refine Finset.sum_nonneg fun x _ => ?_
  split_ifs
  · exact mul_nonneg (hπ x) (hw x)
  · exact le_rfl

/-- The sum of the masses of the `n` events `{x_i = 1}` is `Σ_x π(x) w(x) |x|`. -/
theorem sum_oneW (π w : (ι → Bool) → ℝ) : ∑ i, oneW π w i = ∑ x, π x * w x * (wt x : ℝ) := by
  unfold oneW
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
  unfold wt
  ring

/-- The density is the average of the one-body marginals. -/
theorem densW_eq_avg (π w : (ι → Bool) → ℝ) :
    densW π w = (∑ i, margW π w i) / (Fintype.card ι : ℝ) := by
  unfold densW margW
  rw [← sum_oneW, ← Finset.sum_div, div_div, mul_comm]

/-- The density as the mean of `|x|/n`. -/
theorem densW_eq_mean (π w : (ι → Bool) → ℝ) :
    densW π w = (∑ x, π x * w x * ((wt x : ℝ) / (Fintype.card ι : ℝ))) / massW π w := by
  unfold densW
  rw [mul_comm (Fintype.card ι : ℝ), ← div_div, div_right_comm, Finset.sum_div]
  congr 1
  exact Finset.sum_congr rfl fun x _ => by ring

/-- The action of a site permutation on the cube, `x ↦ x ∘ σ`. -/
def permCube (σ : Equiv.Perm ι) : (ι → Bool) ≃ (ι → Bool) where
  toFun x := x ∘ σ
  invFun x := x ∘ σ.symm
  left_inv x := by
    funext i
    simp
  right_inv x := by
    funext i
    simp

/-- A site permutation that preserves `π` and `w` permutes the masses of the events `{x_i = 1}`. -/
theorem oneW_perm {π w : (ι → Bool) → ℝ} (σ : Equiv.Perm ι) (hπ : ∀ x, π (x ∘ σ) = π x)
    (hw : ∀ x, w (x ∘ σ) = w x) (i : ι) : oneW π w (σ i) = oneW π w i := by
  unfold oneW
  refine Fintype.sum_equiv (permCube σ) _ _ fun x => ?_
  show (if x (σ i) = true then π x * w x else 0) =
    if (x ∘ σ) i = true then π (x ∘ σ) * w (x ∘ σ) else 0
  rw [hπ, hw]
  rfl

/-- The weight `w` is invariant under every site permutation in `G`. -/
def Invariant (G : Set (Equiv.Perm ι)) (w : (ι → Bool) → ℝ) : Prop :=
  ∀ σ ∈ G, ∀ x, w (x ∘ σ) = w x

/-- `G` is transitive on the sites. -/
def SiteTransitive (G : Set (Equiv.Perm ι)) : Prop := ∀ i j, ∃ σ ∈ G, σ i = j

omit [Fintype ι] [DecidableEq ι] in
theorem Invariant.add {G : Set (Equiv.Perm ι)} {w v : (ι → Bool) → ℝ} (hw : Invariant G w)
    (hv : Invariant G v) : Invariant G (fun x => w x + v x) := by
  intro σ hσ x
  show w (x ∘ σ) + v (x ∘ σ) = w x + v x
  rw [hw σ hσ, hv σ hσ]

omit [Fintype ι] [DecidableEq ι] in
theorem Invariant.smul {G : Set (Equiv.Perm ι)} {w : (ι → Bool) → ℝ} (hw : Invariant G w)
    (a : ℝ) : Invariant G (fun x => a * w x) := by
  intro σ hσ x
  show a * w (x ∘ σ) = a * w x
  rw [hw σ hσ]

/-- All the events `{x_i = 1}` have the same mass under an invariant weight. -/
theorem oneW_eq_of_invariant {G : Set (Equiv.Perm ι)} (hG : SiteTransitive G)
    {π w : (ι → Bool) → ℝ} (hπ : Invariant G π) (hw : Invariant G w) (i j : ι) :
    oneW π w i = oneW π w j := by
  obtain ⟨σ, hσ, rfl⟩ := hG i j
  exact (oneW_perm σ (hπ σ hσ) (hw σ hσ) i).symm

theorem card_mul_oneW {G : Set (Equiv.Perm ι)} (hG : SiteTransitive G)
    {π w : (ι → Bool) → ℝ} (hπ : Invariant G π) (hw : Invariant G w) (i : ι) :
    (Fintype.card ι : ℝ) * oneW π w i = ∑ x, π x * w x * (wt x : ℝ) := by
  rw [← sum_oneW, ← Finset.card_univ, ← nsmul_eq_mul, ← Finset.sum_const]
  exact Finset.sum_congr rfl fun j _ => oneW_eq_of_invariant hG hπ hw i j

/-- **Lemma 3 (i), first half.**  If `π` and `w` are invariant under a set `G` of site
permutations that is transitive on the sites, every one-body marginal of `μ_w` equals the
density of `w`. -/
theorem margW_eq_densW {G : Set (Equiv.Perm ι)} (hG : SiteTransitive G)
    {π w : (ι → Bool) → ℝ} (hπ : Invariant G π) (hw : Invariant G w) (i : ι) :
    margW π w i = densW π w := by
  have h := card_mul_oneW hG hπ hw i
  have hn : (Fintype.card ι : ℝ) ≠ 0 := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨i⟩
    exact_mod_cast h0.ne'
  unfold margW densW
  rw [← h, mul_div_mul_left _ _ hn]

/-- Division-free form: the mass of `{x_i = 1}` is the density times the mass. -/
theorem oneW_eq_densW_mul {G : Set (Equiv.Perm ι)} (hG : SiteTransitive G)
    {π w : (ι → Bool) → ℝ} (hπ : Invariant G π) (hw : Invariant G w) (hm : massW π w ≠ 0)
    (i : ι) : oneW π w i = densW π w * massW π w := by
  rw [← margW_eq_densW hG hπ hw i]
  unfold margW
  field_simp

/-- **The one-body marginals of a sum are the mass-weighted averages.** -/
theorem margW_add {π w v : (ι → Bool) → ℝ} (hw : massW π w ≠ 0) (hv : massW π v ≠ 0) (i : ι) :
    margW π (fun x => w x + v x) i =
      (massW π w * margW π w i + massW π v * margW π v i) / (massW π w + massW π v) := by
  have e1 : massW π w * margW π w i = oneW π w i := by
    unfold margW
    field_simp
  have e2 : massW π v * margW π v i = oneW π v i := by
    unfold margW
    field_simp
  rw [e1, e2]
  unfold margW
  rw [oneW_add, massW_add]

/-- Adding a weight leaves a one-body marginal unchanged iff the added weight has the same
marginal. -/
theorem margW_add_eq_iff {π w v : (ι → Bool) → ℝ} (hw : 0 < massW π w) (hv : 0 < massW π v)
    (i : ι) :
    margW π (fun x => w x + v x) i = margW π w i ↔ margW π v i = margW π w i := by
  rw [margW_add hw.ne' hv.ne', div_eq_iff (by positivity)]
  constructor
  · intro h
    have h1 : massW π v * (margW π v i - margW π w i) = 0 := by linarith
    rcases mul_eq_zero.mp h1 with h2 | h2
    · exact absurd h2 hv.ne'
    · linarith
  · intro h
    rw [h]
    ring

/-- **Lemma 3 (i).**  `G` a set of site permutations, transitive on the sites; `π > 0`, `w > 0`
and `Δ ≥ 0`, `Δ ≢ 0`, all `G`-invariant.  Then all one-body marginals of `μ_w` equal `c_w`, all
those of `μ_{w+Δ}` equal `(A_w c_w + A_Δ c_Δ)/(A_w + A_Δ)`, and the two instances have the same
one-body marginals iff `c_Δ = c_w`. -/
theorem lemma3_i [Nonempty ι] {G : Set (Equiv.Perm ι)} (hG : SiteTransitive G)
    {π w Δ : (ι → Bool) → ℝ} (hπ : ∀ x, 0 < π x) (hπG : Invariant G π)
    (hw : ∀ x, 0 < w x) (hwG : Invariant G w)
    (hΔ0 : ∀ x, 0 ≤ Δ x) (hΔ1 : ∃ x, Δ x ≠ 0) (hΔG : Invariant G Δ) :
    (∀ i, margW π w i = densW π w) ∧
    (∀ i, margW π (fun x => w x + Δ x) i =
      (massW π w * densW π w + massW π Δ * densW π Δ) / (massW π w + massW π Δ)) ∧
    ((∀ i, margW π (fun x => w x + Δ x) i = margW π w i) ↔ densW π Δ = densW π w) := by
  have hAw := massW_pos hπ hw
  have hAΔ := massW_pos_of_ne_zero hπ hΔ0 hΔ1
  refine ⟨fun i => margW_eq_densW hG hπG hwG i, fun i => ?_, ?_⟩
  · rw [margW_add hAw.ne' hAΔ.ne', margW_eq_densW hG hπG hwG i, margW_eq_densW hG hπG hΔG i]
  · constructor
    · intro h
      obtain ⟨i⟩ := ‹Nonempty ι›
      have h1 := (margW_add_eq_iff hAw hAΔ i).mp (h i)
      rw [margW_eq_densW hG hπG hwG i, margW_eq_densW hG hπG hΔG i] at h1
      exact h1
    · intro h i
      rw [margW_add_eq_iff hAw hAΔ i, margW_eq_densW hG hπG hwG i,
        margW_eq_densW hG hπG hΔG i, h]

end Marginals

/-! ## Part 3: the compensation lemma, Lemma 3 (ii) -/

section Compensation

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The mass of the compensated base `w₀ = w + b·v`, `b = A_w (c_Δ − c_w)/(p₂ − c_Δ)`, `A(v) = 1`:
`A(w₀) = A_w (p₂ − c_w)/(p₂ − c_Δ)`. -/
theorem massW_compensated {π w v : (ι → Bool) → ℝ} {cw cΔ p₂ : ℝ} (hv1 : massW π v = 1)
    (hne : p₂ ≠ cΔ) :
    massW π (fun x => w x + massW π w * (cΔ - cw) / (p₂ - cΔ) * v x) =
      massW π w * (p₂ - cw) / (p₂ - cΔ) := by
  have hne' : p₂ - cΔ ≠ 0 := sub_ne_zero.mpr hne
  rw [massW_add, massW_smul, hv1]
  field_simp
  ring

/-- **The linear equation of the compensation lemma, at one site, division-free.**  If the event
`{x_i = 1}` has the fraction `c_w` of the mass of `w` and the fraction `p₂` of the mass of `v`,
`A(v) = 1` and `p₂ ≠ c_Δ`, then with `b = A_w (c_Δ − c_w)/(p₂ − c_Δ)` it has the fraction `c_Δ` of
the mass of `w + b·v`.  No sign condition, no invariance. -/
theorem oneW_compensated {π w v : (ι → Bool) → ℝ} {i : ι} {cw cΔ p₂ : ℝ}
    (hw : oneW π w i = cw * massW π w) (hv : oneW π v i = p₂ * massW π v) (hv1 : massW π v = 1)
    (hne : p₂ ≠ cΔ) :
    oneW π (fun x => w x + massW π w * (cΔ - cw) / (p₂ - cΔ) * v x) i =
      cΔ * massW π (fun x => w x + massW π w * (cΔ - cw) / (p₂ - cΔ) * v x) := by
  have hne' : p₂ - cΔ ≠ 0 := sub_ne_zero.mpr hne
  rw [oneW_add, oneW_smul, massW_add, massW_smul, hw, hv, hv1]
  field_simp
  ring

/-- Adding to a weight whose event `{x_i = 1}` has the fraction `c` of the mass another weight
with the same property keeps the property. -/
theorem oneW_add_of_eq {π w₀ Δ : (ι → Bool) → ℝ} {i : ι} {c : ℝ}
    (h₀ : oneW π w₀ i = c * massW π w₀) (hΔ : oneW π Δ i = c * massW π Δ) :
    oneW π (fun x => w₀ x + Δ x) i = c * massW π (fun x => w₀ x + Δ x) := by
  rw [oneW_add, massW_add, h₀, hΔ]
  ring

/-- **Lemma 3 (ii) (compensation).**  `G` a set of site permutations, transitive on the sites;
`π > 0` a `G`-invariant reference weight; `w ∈ 𝒲_u` and `Δ ≥ 0`, `Δ ≢ 0`, with `w + Δ ∈ 𝒲_u`,
both `G`-invariant; `v ∈ 𝒲_u` a `G`-invariant weight of mass `1` (in the report: the normalised
additive instance `w̃_{γ₂}`, `|γ₂| ≤ u`) with density `p₂`.  If `c_Δ` lies strictly between `c_w`
and `p₂`, then with

    b := A_w (c_Δ − c_w) / (p₂ − c_Δ) > 0

the weights `w₀ := w + b·v` and `w₁ := w + Δ + b·v` are in `𝒲_u`, are `G`-invariant, have all
one-body marginals equal to `c_Δ`, differ exactly on `{Δ > 0}`, and
`A(w₁)/A(w₀) = 1 + (A_Δ/A_w)·(p₂ − c_Δ)/(p₂ − c_w)`. -/
theorem lemma3_compensation {G : Set (Equiv.Perm ι)} (hG : SiteTransitive G)
    {π : (ι → Bool) → ℝ} (hπ : ∀ x, 0 < π x) (hπG : Invariant G π) {u : ℝ}
    {w Δ v : (ι → Bool) → ℝ} (hw : InCone u w) (hwG : Invariant G w)
    (hΔ0 : ∀ x, 0 ≤ Δ x) (hΔ1 : ∃ x, Δ x ≠ 0) (hwΔ : InCone u (fun x => w x + Δ x))
    (hΔG : Invariant G Δ) (hv : InCone u v) (hvG : Invariant G v) (hv1 : massW π v = 1)
    (hbetween : (densW π w < densW π Δ ∧ densW π Δ < densW π v) ∨
      (densW π v < densW π Δ ∧ densW π Δ < densW π w)) :
    ∃ b : ℝ, b = massW π w * (densW π Δ - densW π w) / (densW π v - densW π Δ) ∧ 0 < b ∧
      InCone u (fun x => w x + b * v x) ∧ InCone u (fun x => w x + Δ x + b * v x) ∧
      Invariant G (fun x => w x + b * v x) ∧ Invariant G (fun x => w x + Δ x + b * v x) ∧
      (∀ i, margW π (fun x => w x + b * v x) i = densW π Δ) ∧
      (∀ i, margW π (fun x => w x + Δ x + b * v x) i = densW π Δ) ∧
      (∀ x, w x + Δ x + b * v x ≠ w x + b * v x ↔ 0 < Δ x) ∧
      massW π (fun x => w x + Δ x + b * v x) / massW π (fun x => w x + b * v x) =
        1 + massW π Δ / massW π w * ((densW π v - densW π Δ) / (densW π v - densW π w)) := by
  have hAw : 0 < massW π w := massW_pos hπ hw.1
  have hAΔ : 0 < massW π Δ := massW_pos_of_ne_zero hπ hΔ0 hΔ1
  have hne : densW π v ≠ densW π Δ := by
    rcases hbetween with h | h
    · exact h.2.ne'
    · exact h.1.ne
  have hne2 : densW π v - densW π w ≠ 0 := by
    rcases hbetween with h | h
    · exact (sub_pos.mpr (h.1.trans h.2)).ne'
    · exact (sub_neg.mpr (h.1.trans h.2)).ne
  have hne' : densW π v - densW π Δ ≠ 0 := sub_ne_zero.mpr hne
  have hb : 0 < massW π w * (densW π Δ - densW π w) / (densW π v - densW π Δ) := by
    rcases hbetween with h | h
    · exact div_pos (mul_pos hAw (sub_pos.mpr h.1)) (sub_pos.mpr h.2)
    · exact div_pos_of_neg_of_neg (mul_neg_of_pos_of_neg hAw (sub_neg.mpr h.2))
        (sub_neg.mpr h.1)
  -- the two weights
  have hc0 : InCone u (fun x => w x + massW π w * (densW π Δ - densW π w) /
      (densW π v - densW π Δ) * v x) := hw.add_smul hv hb.le
  have hc1 : InCone u (fun x => w x + Δ x + massW π w * (densW π Δ - densW π w) /
      (densW π v - densW π Δ) * v x) := hwΔ.add_smul hv hb.le
  have hm0 := massW_compensated (π := π) (w := w) (v := v) (cw := densW π w) hv1 hne
  have hm0pos : 0 < massW π (fun x => w x + massW π w * (densW π Δ - densW π w) /
      (densW π v - densW π Δ) * v x) := massW_pos hπ hc0.1
  have hm1 : massW π (fun x => w x + Δ x + massW π w * (densW π Δ - densW π w) /
      (densW π v - densW π Δ) * v x) =
      massW π (fun x => w x + massW π w * (densW π Δ - densW π w) /
        (densW π v - densW π Δ) * v x) + massW π Δ := by
    rw [← massW_add]
    congr 1
    funext x
    ring
  have hm1pos : 0 < massW π (fun x => w x + Δ x + massW π w * (densW π Δ - densW π w) /
      (densW π v - densW π Δ) * v x) := massW_pos hπ hc1.1
  have h0 : ∀ i, oneW π (fun x => w x + massW π w * (densW π Δ - densW π w) /
      (densW π v - densW π Δ) * v x) i =
      densW π Δ * massW π (fun x => w x + massW π w * (densW π Δ - densW π w) /
        (densW π v - densW π Δ) * v x) := fun i =>
    oneW_compensated (oneW_eq_densW_mul hG hπG hwG hAw.ne' i)
      (oneW_eq_densW_mul hG hπG hvG (by rw [hv1]; exact one_ne_zero) i) hv1 hne
  have h1 : ∀ i, oneW π (fun x => w x + Δ x + massW π w * (densW π Δ - densW π w) /
      (densW π v - densW π Δ) * v x) i =
      densW π Δ * massW π (fun x => w x + Δ x + massW π w * (densW π Δ - densW π w) /
        (densW π v - densW π Δ) * v x) := by
    intro i
    have h := oneW_add_of_eq (h0 i) (oneW_eq_densW_mul hG hπG hΔG hAΔ.ne' i)
    have e : (fun x => w x + Δ x + massW π w * (densW π Δ - densW π w) /
        (densW π v - densW π Δ) * v x) =
        fun x => w x + massW π w * (densW π Δ - densW π w) /
          (densW π v - densW π Δ) * v x + Δ x := by
      funext x
      ring
    rw [e]
    exact h
  refine ⟨_, rfl, hb, hc0, hc1, hwG.add (hvG.smul _), (hwG.add hΔG).add (hvG.smul _),
    fun i => ?_, fun i => ?_, fun x => ?_, ?_⟩
  · unfold margW
    rw [h0 i, mul_div_assoc, div_self hm0pos.ne', mul_one]
  · unfold margW
    rw [h1 i, mul_div_assoc, div_self hm1pos.ne', mul_one]
  · constructor
    · intro h
      refine lt_of_le_of_ne (hΔ0 x) fun h0' => h ?_
      rw [← h0']
      ring
    · intro h h'
      linarith
  · rw [hm1, hm0]
    field_simp

end Compensation

/-! ## Part 4: product weights, the Bernoulli reference weight, the additive instances;
Lemma 0 (window) -/

section Product

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- A product weight `x ↦ ∏_i f_i(x_i)`. -/
def prodW (f : ι → Bool → ℝ) (x : ι → Bool) : ℝ := ∏ i, f i (x i)

omit [DecidableEq ι] in
theorem prodW_pos {f : ι → Bool → ℝ} (hf : ∀ i a, 0 < f i a) (x : ι → Bool) : 0 < prodW f x :=
  Finset.prod_pos fun i _ => hf i (x i)

omit [DecidableEq ι] in
theorem prodW_mul (f g : ι → Bool → ℝ) (x : ι → Bool) :
    prodW f x * prodW g x = prodW (fun i a => f i a * g i a) x := by
  unfold prodW
  rw [← Finset.prod_mul_distrib]

theorem prodW_eq_mul_erase (f : ι → Bool → ℝ) (x : ι → Bool) (i : ι) :
    prodW f x = f i (x i) * ∏ j ∈ univ.erase i, f j (x j) :=
  (Finset.mul_prod_erase univ (fun j => f j (x j)) (Finset.mem_univ i)).symm

theorem prodW_flipAt (f : ι → Bool → ℝ) (x : ι → Bool) (i : ι) :
    prodW f (flipAt x i) = f i (!x i) * ∏ j ∈ univ.erase i, f j (x j) := by
  rw [prodW_eq_mul_erase f (flipAt x i) i, flipAt_same]
  congr 1
  refine Finset.prod_congr rfl fun j hj => ?_
  rw [flipAt_ne x (Finset.ne_of_mem_erase hj)]

/-- A product weight with positive site factors whose two values at each site differ by at
most the factor `e^u` is in the cone. -/
theorem prodW_inCone {u : ℝ} {f : ι → Bool → ℝ} (hf : ∀ i a, 0 < f i a)
    (hf2 : ∀ i a, f i (!a) ≤ Real.exp u * f i a) : InCone u (prodW f) := by
  refine inCone_of_upper (prodW_pos hf) fun x i => ?_
  rw [prodW_flipAt, prodW_eq_mul_erase f x i, ← mul_assoc]
  exact mul_le_mul_of_nonneg_right (hf2 i (x i))
    (Finset.prod_nonneg fun j _ => (hf j (x j)).le)

omit [DecidableEq ι] in
/-- Permuting the sites of the factors and of the configuration leaves a product weight
unchanged. -/
theorem prodW_perm (f : ι → Bool → ℝ) (σ : Equiv.Perm ι) (x : ι → Bool) :
    prodW (fun i => f (σ i)) (x ∘ σ) = prodW f x :=
  Equiv.prod_comp σ (fun i => f i (x i))

/-- `Σ_x ∏_i f_i(x_i) = ∏_i (f_i(1) + f_i(0))`. -/
theorem sum_prodW (f : ι → Bool → ℝ) : ∑ x, prodW f x = ∏ i, (f i true + f i false) := by
  unfold prodW
  refine (Fintype.prod_sum f).symm.trans ?_
  refine Finset.prod_congr rfl fun i _ => ?_
  rw [Fintype.sum_bool]

/-- `Σ_{x : x_j = 1} ∏_i f_i(x_i) = f_j(1) ∏_{i ≠ j} (f_i(1) + f_i(0))`. -/
theorem sum_prodW_one (f : ι → Bool → ℝ) (j : ι) :
    ∑ x, (if x j = true then prodW f x else 0) =
      f j true * ∏ i ∈ univ.erase j, (f i true + f i false) := by
  have key : ∀ x : ι → Bool, (if x j = true then prodW f x else 0) =
      prodW (fun i a => if i = j then (if a = true then f i a else 0) else f i a) x := by
    intro x
    unfold prodW
    by_cases hx : x j = true
    · rw [if_pos hx]
      refine Finset.prod_congr rfl fun i _ => ?_
      show f i (x i) = if i = j then (if x i = true then f i (x i) else 0) else f i (x i)
      by_cases hij : i = j
      · subst hij
        rw [if_pos rfl, if_pos hx]
      · rw [if_neg hij]
    · rw [if_neg hx]
      symm
      refine Finset.prod_eq_zero (Finset.mem_univ j) ?_
      show (if j = j then (if x j = true then f j (x j) else 0) else f j (x j)) = 0
      rw [if_pos rfl, if_neg hx]
  rw [Finset.sum_congr rfl fun x _ => key x, sum_prodW,
    ← Finset.mul_prod_erase univ _ (Finset.mem_univ j)]
  congr 1
  · simp
  · refine Finset.prod_congr rfl fun i hi => ?_
    rw [if_neg (Finset.ne_of_mem_erase hi), if_neg (Finset.ne_of_mem_erase hi)]

/-- The site law of the reference weight: `Bernoulli(p)`. -/
def bernW (p : ℝ) : Bool → ℝ
  | true => p
  | false => 1 - p

/-- **The reference weight** `π = Bernoulli(p)^{⊗n}`. -/
def refW (p : ℝ) : (ι → Bool) → ℝ := prodW fun _ => bernW p

/-- `q + p e^{−γ}`, the normalising constant of one site of the additive instance `γ`. -/
def tiltZ (p γ : ℝ) : ℝ := (1 - p) + p * Real.exp (-γ)

/-- `p_γ = π_γ(1) = p e^{−γ}/(q + p e^{−γ})`. -/
def pTilt (p γ : ℝ) : ℝ := p * Real.exp (-γ) / tiltZ p γ

/-- The site factor of the normalised additive weight: `e^{−γ a}/(q + p e^{−γ})`. -/
def tiltFac (p γ : ℝ) : Bool → ℝ
  | true => Real.exp (-γ) / tiltZ p γ
  | false => 1 / tiltZ p γ

/-- **The normalised weight of the additive instance with site fields `γ i`**:
`x ↦ ∏_i e^{−γ_i x_i}/(q + p e^{−γ_i})`.  For a constant field it is the report's `w̃_γ`; for the
field `γ_i = u(1 − 2 s_i)` it is the normalised cone `c̃_s`. -/
def tiltW (p : ℝ) (γ : ι → ℝ) : (ι → Bool) → ℝ := prodW fun i => tiltFac p (γ i)

/-- The site law `π_γ` of the additive instance `γ`. -/
def siteLaw (p γ : ℝ) : Bool → ℝ
  | true => p * Real.exp (-γ) / tiltZ p γ
  | false => (1 - p) / tiltZ p γ

theorem tiltZ_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) : 0 < tiltZ p γ :=
  add_pos (by linarith) (mul_pos hp0 (Real.exp_pos _))

theorem siteLaw_sum {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) :
    siteLaw p γ true + siteLaw p γ false = 1 := by
  have hZ := (tiltZ_pos hp0 hp1 γ).ne'
  show p * Real.exp (-γ) / tiltZ p γ + (1 - p) / tiltZ p γ = 1
  rw [← add_div, div_eq_one_iff_eq hZ]
  unfold tiltZ
  ring

theorem pTilt_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) : 0 < pTilt p γ :=
  div_pos (mul_pos hp0 (Real.exp_pos _)) (tiltZ_pos hp0 hp1 γ)

theorem pTilt_lt_one {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) : pTilt p γ < 1 := by
  unfold pTilt
  rw [div_lt_one (tiltZ_pos hp0 hp1 γ)]
  unfold tiltZ
  linarith

/-- `γ ↦ p_γ` is non-increasing. -/
theorem pTilt_anti {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {γ γ' : ℝ} (h : γ ≤ γ') :
    pTilt p γ' ≤ pTilt p γ := by
  unfold pTilt
  rw [div_le_div_iff₀ (tiltZ_pos hp0 hp1 γ') (tiltZ_pos hp0 hp1 γ)]
  unfold tiltZ
  have he : Real.exp (-γ') ≤ Real.exp (-γ) := Real.exp_le_exp.mpr (by linarith)
  have h1 : 0 < p * (1 - p) := mul_pos hp0 (by linarith)
  nlinarith [mul_le_mul_of_nonneg_left he h1.le]

/-- `γ ↦ p_γ` is strictly decreasing. -/
theorem pTilt_strictAnti {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {γ γ' : ℝ} (h : γ < γ') :
    pTilt p γ' < pTilt p γ := by
  unfold pTilt
  rw [div_lt_div_iff₀ (tiltZ_pos hp0 hp1 γ') (tiltZ_pos hp0 hp1 γ)]
  unfold tiltZ
  have he : Real.exp (-γ') < Real.exp (-γ) := Real.exp_lt_exp.mpr (by linarith)
  have h1 : 0 < p * (1 - p) := mul_pos hp0 (by linarith)
  nlinarith [mul_lt_mul_of_pos_left he h1]

omit [DecidableEq ι] in
theorem refW_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (x : ι → Bool) : 0 < refW p x := by
  refine prodW_pos (fun _ a => ?_) x
  cases a
  · show 0 < 1 - p
    linarith
  · exact hp0

omit [DecidableEq ι] in
theorem tiltW_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ι → ℝ) (x : ι → Bool) :
    0 < tiltW p γ x := by
  refine prodW_pos (fun i a => ?_) x
  have hZ := tiltZ_pos hp0 hp1 (γ i)
  cases a
  · exact div_pos one_pos hZ
  · exact div_pos (Real.exp_pos _) hZ

omit [DecidableEq ι] in
/-- `π · w̃_γ = ⊗_i π_{γ_i}`. -/
theorem refW_mul_tiltW (p : ℝ) (γ : ι → ℝ) (x : ι → Bool) :
    refW p x * tiltW p γ x = prodW (fun i => siteLaw p (γ i)) x := by
  unfold refW tiltW
  rw [prodW_mul]
  congr 1
  funext i a
  cases a
  · show (1 - p) * (1 / tiltZ p (γ i)) = (1 - p) / tiltZ p (γ i)
    ring
  · show p * (Real.exp (-γ i) / tiltZ p (γ i)) = p * Real.exp (-γ i) / tiltZ p (γ i)
    ring

/-- The reference weight is a probability vector. -/
theorem sum_refW {p : ℝ} : ∑ x : ι → Bool, refW p x = 1 := by
  unfold refW
  rw [sum_prodW]
  refine Finset.prod_eq_one fun i _ => ?_
  show p + (1 - p) = 1
  ring

/-- The additive weights are normalised: `A(w̃_γ) = 1`. -/
theorem massW_tiltW {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ι → ℝ) :
    massW (refW p) (tiltW p γ) = 1 := by
  unfold massW
  rw [Finset.sum_congr rfl fun x _ => refW_mul_tiltW p γ x, sum_prodW]
  exact Finset.prod_eq_one fun i _ => siteLaw_sum hp0 hp1 (γ i)

/-- The mass of `{x_j = 1}` under `π · w̃_γ` is `p_{γ_j}`. -/
theorem oneW_tiltW {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ι → ℝ) (j : ι) :
    oneW (refW p) (tiltW p γ) j = pTilt p (γ j) := by
  unfold oneW
  have key : ∀ x : ι → Bool, (if x j = true then refW p x * tiltW p γ x else 0) =
      if x j = true then prodW (fun i => siteLaw p (γ i)) x else 0 := fun x => by
    rw [refW_mul_tiltW]
  rw [Finset.sum_congr rfl fun x _ => key x, sum_prodW_one,
    Finset.prod_eq_one fun i _ => siteLaw_sum hp0 hp1 (γ i), mul_one]
  rfl

/-- The one-body marginals of the additive instance: `μ(x_j = 1) = p_{γ_j}`. -/
theorem margW_tiltW {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ι → ℝ) (j : ι) :
    margW (refW p) (tiltW p γ) j = pTilt p (γ j) := by
  unfold margW
  rw [oneW_tiltW hp0 hp1, massW_tiltW hp0 hp1, div_one]

/-- The density of an additive instance is the average of the `p_{γ_i}`. -/
theorem densW_tiltW {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ι → ℝ) :
    densW (refW p) (tiltW p γ) = (∑ i, pTilt p (γ i)) / (Fintype.card ι : ℝ) := by
  rw [densW_eq_avg]
  congr 1
  exact Finset.sum_congr rfl fun i _ => margW_tiltW hp0 hp1 γ i

/-- `dens(w̃_γ) = p_γ`. -/
theorem densW_tiltW_const [Nonempty ι] {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) :
    densW (refW p) (tiltW (ι := ι) p fun _ => γ) = pTilt p γ := by
  have hn : (Fintype.card ι : ℝ) ≠ 0 := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos
    exact_mod_cast h0.ne'
  rw [densW_tiltW hp0 hp1, Finset.sum_const, Finset.card_univ, nsmul_eq_mul,
    mul_div_cancel_left₀ _ hn]

/-- An additive instance with all fields in `[−u, u]` is in the class. -/
theorem tiltW_inCone {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {γ : ι → ℝ} (hγ : ∀ i, |γ i| ≤ u) :
    InCone u (tiltW p γ) := by
  refine prodW_inCone (fun i a => ?_) fun i a => ?_
  · have hZ := tiltZ_pos hp0 hp1 (γ i)
    cases a
    · exact div_pos one_pos hZ
    · exact div_pos (Real.exp_pos _) hZ
  · have hZ := tiltZ_pos hp0 hp1 (γ i)
    have h := abs_le.mp (hγ i)
    cases a
    · show Real.exp (-γ i) / tiltZ p (γ i) ≤ Real.exp u * (1 / tiltZ p (γ i))
      rw [mul_one_div]
      exact div_le_div_of_nonneg_right (Real.exp_le_exp.mpr (by linarith [h.1])) hZ.le
    · show 1 / tiltZ p (γ i) ≤ Real.exp u * (Real.exp (-γ i) / tiltZ p (γ i))
      rw [← mul_div_assoc, ← Real.exp_add]
      exact div_le_div_of_nonneg_right (Real.one_le_exp (by linarith [h.2])) hZ.le

omit [DecidableEq ι] in
/-- The reference weight is invariant under every site permutation. -/
theorem refW_perm (p : ℝ) (σ : Equiv.Perm ι) (x : ι → Bool) : refW p (x ∘ σ) = refW p x :=
  prodW_perm (fun _ => bernW p) σ x

omit [DecidableEq ι] in
/-- Covariance of the additive weights under site permutations. -/
theorem tiltW_perm (p : ℝ) (γ : ι → ℝ) (σ : Equiv.Perm ι) (x : ι → Bool) :
    tiltW p (fun i => γ (σ i)) (x ∘ σ) = tiltW p γ x :=
  prodW_perm (fun i => tiltFac p (γ i)) σ x

omit [DecidableEq ι] in
theorem refW_invariant (p : ℝ) (G : Set (Equiv.Perm ι)) : Invariant G (refW (ι := ι) p) :=
  fun σ _ x => refW_perm p σ x

omit [DecidableEq ι] in
theorem tiltW_const_invariant (p γ : ℝ) (G : Set (Equiv.Perm ι)) :
    Invariant G (tiltW (ι := ι) p fun _ => γ) :=
  fun σ _ x => tiltW_perm p (fun _ => γ) σ x

/-! ### Lemma 0 (window) -/

/-- The mass of `{x : x_i = 0}`. -/
def zeroW (π w : (ι → Bool) → ℝ) (i : ι) : ℝ := ∑ x, if x i = true then 0 else π x * w x

theorem oneW_add_zeroW (π w : (ι → Bool) → ℝ) (i : ι) :
    oneW π w i + zeroW π w i = massW π w := by
  unfold oneW zeroW massW
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun x _ => ?_
  split_ifs <;> ring

/-- The mass of `{x_i = 1}` as a sum over `{x_i = 0}`, through the flip of site `i`. -/
theorem oneW_eq_sum_flip (π w : (ι → Bool) → ℝ) (i : ι) :
    oneW π w i = ∑ x, if x i = true then 0 else π (flipAt x i) * w (flipAt x i) := by
  unfold oneW
  refine Fintype.sum_equiv (flipEquiv i) _ _ fun x => ?_
  show (if x i = true then π x * w x else 0) =
    if flipAt x i i = true then 0 else π (flipAt (flipAt x i) i) * w (flipAt (flipAt x i) i)
  rw [flipAt_flipAt, flipAt_same]
  by_cases h : x i = true
  · simp [h]
  · simp [h]

/-- **Lemma 0 (window), for any reference weight with site odds `p : 1 − p` at site `i`.**
If `π > 0` satisfies `π(x^{i←1})·(1 − p) = π(x^{i←0})·p` and `w ∈ 𝒲_u`, then
`p₋ ≤ μ_w(x_i = 1) ≤ p₊`, `p₋ = p_u`, `p₊ = p_{−u}`. -/
theorem window_of_site_odds {π w : (ι → Bool) → ℝ} {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1)
    (i : ι) (hπ0 : ∀ x, 0 < π x)
    (hπ : ∀ x, x i = false → π (flipAt x i) * (1 - p) = π x * p) (hw : InCone u w) :
    pTilt p u ≤ margW π w i ∧ margW π w i ≤ pTilt p (-u) := by
  have hmass : 0 < massW π w := massW_pos hπ0 hw.1
  have hsum := oneW_add_zeroW π w i
  have hflip := oneW_eq_sum_flip π w i
  have hup : (1 - p) * oneW π w i ≤ p * Real.exp u * zeroW π w i := by
    rw [hflip]
    unfold zeroW
    rw [Finset.mul_sum, Finset.mul_sum]
    refine Finset.sum_le_sum fun x _ => ?_
    by_cases hx : x i = true
    · rw [if_pos hx, if_pos hx, mul_zero, mul_zero]
    · rw [if_neg hx, if_neg hx]
      have hx' : x i = false := by simpa using hx
      have h1 := hπ x hx'
      have h2 := (hw.2 x i).2
      have h3 : π (flipAt x i) * (1 - p) * w (flipAt x i) ≤ π x * p * (Real.exp u * w x) := by
        rw [h1]
        exact mul_le_mul_of_nonneg_left h2 (mul_pos (hπ0 x) hp0).le
      linarith
  have hlo : p * Real.exp (-u) * zeroW π w i ≤ (1 - p) * oneW π w i := by
    rw [hflip]
    unfold zeroW
    rw [Finset.mul_sum, Finset.mul_sum]
    refine Finset.sum_le_sum fun x _ => ?_
    by_cases hx : x i = true
    · rw [if_pos hx, if_pos hx, mul_zero, mul_zero]
    · rw [if_neg hx, if_neg hx]
      have hx' : x i = false := by simpa using hx
      have h1 := hπ x hx'
      have h2 := (hw.2 x i).1
      have h3 : π x * p * (Real.exp (-u) * w x) ≤ π (flipAt x i) * (1 - p) * w (flipAt x i) := by
        rw [h1]
        exact mul_le_mul_of_nonneg_left h2 (mul_pos (hπ0 x) hp0).le
      linarith
  constructor
  · unfold margW pTilt
    rw [div_le_div_iff₀ (tiltZ_pos hp0 hp1 u) hmass, ← hsum]
    unfold tiltZ
    nlinarith
  · unfold margW pTilt
    rw [div_le_div_iff₀ hmass (tiltZ_pos hp0 hp1 (-u)), ← hsum]
    unfold tiltZ
    rw [neg_neg]
    nlinarith

/-- The Bernoulli reference weight has site odds `p : 1 − p` at every site. -/
theorem refW_flip_odds (p : ℝ) (x : ι → Bool) (i : ι) (hx : x i = false) :
    refW p (flipAt x i) * (1 - p) = refW p x * p := by
  unfold refW
  rw [prodW_flipAt, prodW_eq_mul_erase (fun _ => bernW p) x i, hx]
  show p * _ * (1 - p) = (1 - p) * _ * p
  ring

/-- **Lemma 0 (window), in the weights.**  For every `w ∈ 𝒲_u` and every site,
`p₋ ≤ μ_w(x_i = 1) ≤ p₊` with `p₋ = p_u`, `p₊ = p_{−u}`. -/
theorem lemma0_window {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {w : (ι → Bool) → ℝ}
    (hw : InCone u w) (i : ι) :
    pTilt p u ≤ margW (refW p) w i ∧ margW (refW p) w i ≤ pTilt p (-u) :=
  window_of_site_odds hp0 hp1 i (refW_pos hp0 hp1) (fun x hx => refW_flip_odds p x i hx) hw

/-- **Lemma 0 (window), in the energies.**  For every `ψ ∈ L_u` and every site,
`μ_ψ(x_i = 1) ∈ [p₋, p₊]`. -/
theorem lemma0_window_lipH {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) {ψ : (ι → Bool) → ℝ}
    (hψ : LipH u ψ) (i : ι) :
    pTilt p u ≤ margW (refW p) (fun x => Real.exp (-ψ x)) i ∧
      margW (refW p) (fun x => Real.exp (-ψ x)) i ≤ pTilt p (-u) :=
  lemma0_window hp0 hp1 (lipH_iff_inCone.mp hψ) i

/-- **Lemma 0, second sentence: the additive instances fill the window.**  For every `c` in
`[p₋, p₊]` there is a field `γ ∈ [−u, u]` whose additive instance is in the class and has all
its one-body marginals equal to `c`. -/
theorem lemma0_additive_fill {p u c : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hu : 0 ≤ u)
    (hc : pTilt p u ≤ c) (hc' : c ≤ pTilt p (-u)) :
    ∃ γ : ℝ, |γ| ≤ u ∧ InCone u (tiltW (ι := ι) p fun _ => γ) ∧
      ∀ i : ι, margW (refW p) (tiltW p fun _ => γ) i = c := by
  have hcont : ContinuousOn (fun γ : ℝ => pTilt p γ) (Set.Icc (-u) u) := by
    apply Continuous.continuousOn
    show Continuous fun γ : ℝ => p * Real.exp (-γ) / ((1 - p) + p * Real.exp (-γ))
    exact Continuous.div (by fun_prop) (by fun_prop) fun γ => (tiltZ_pos hp0 hp1 γ).ne'
  obtain ⟨γ, hγ, hγc⟩ := intermediate_value_Icc' (by linarith : -u ≤ u) hcont ⟨hc, hc'⟩
  have hγu : |γ| ≤ u := abs_le.mpr ⟨hγ.1, hγ.2⟩
  refine ⟨γ, hγu, tiltW_inCone hp0 hp1 (fun _ => hγu), fun i => ?_⟩
  rw [margW_tiltW hp0 hp1]
  exact hγc

end Product

/-! ## Part 5: Lemma 2 (the excess of a dip is the cone law) -/

section Lemma2

theorem max_sub_zero_eq (a b : ℝ) : max (a - b) 0 = a - min a b := by
  rcases le_total a b with h | h
  · rw [max_eq_right (by linarith), min_eq_left h]
    ring
  · rw [max_eq_left (by linarith), min_eq_right h]

/-- The arithmetic of Lemma 2: `c − c₀ = J(c₀ − c_J)/(R − J)` and `J ≤ 1 < R`. -/
theorem excess_core {R J Jf c₀ : ℝ} (hR : 1 < R) (hJ0 : 0 ≤ J) (hJ1 : J ≤ 1) (hJf0 : 0 ≤ Jf)
    (hJfJ : Jf ≤ J) (hc0 : 0 ≤ c₀) (hc1 : c₀ ≤ 1) :
    |(R * c₀ - Jf) / (R - J) - c₀| ≤ 1 / (R - 1) := by
  have hEpos : 0 < R - J := by linarith
  have hR1 : 0 < R - 1 := by linarith
  have e : (R * c₀ - Jf) / (R - J) - c₀ = (J * c₀ - Jf) / (R - J) := by
    field_simp
    ring
  have hJR : J * R ≤ R := mul_le_of_le_one_left (by linarith) hJ1
  have hJc : J * c₀ ≤ J := mul_le_of_le_one_right hJ0 hc1
  have hJc0 : 0 ≤ J * c₀ := mul_nonneg hJ0 hc0
  rw [e, abs_le]
  constructor
  · rw [neg_le, ← neg_div, div_le_div_iff₀ hEpos hR1]
    have h1 : -(J * c₀ - Jf) ≤ J := by linarith
    have h2 := mul_le_mul_of_nonneg_right h1 hR1.le
    linarith
  · rw [div_le_div_iff₀ hEpos hR1]
    have h1 : J * c₀ - Jf ≤ J := by linarith
    have h2 := mul_le_mul_of_nonneg_right h1 hR1.le
    linarith

variable {X : Type*} [Fintype X]

/-- **Lemma 2, the mass, for two arbitrary probability vectors.**  `P₁, P₂ ≥ 0` of total mass
`1`, `R ≥ 0`: the excess `D = (R·P₁ − P₂)₊` has mass in `[R − 1, R]`. -/
theorem excess_mass_bounds {P₁ P₂ : X → ℝ} (h₁ : ∀ x, 0 ≤ P₁ x) (h₂ : ∀ x, 0 ≤ P₂ x)
    (s₁ : ∑ x, P₁ x = 1) (s₂ : ∑ x, P₂ x = 1) {R : ℝ} (hR : 0 ≤ R) :
    R - 1 ≤ ∑ x, max (R * P₁ x - P₂ x) 0 ∧ ∑ x, max (R * P₁ x - P₂ x) 0 ≤ R := by
  have hJ0 : 0 ≤ ∑ x, min (R * P₁ x) (P₂ x) :=
    Finset.sum_nonneg fun x _ => le_min (mul_nonneg hR (h₁ x)) (h₂ x)
  have hJ1 : ∑ x, min (R * P₁ x) (P₂ x) ≤ 1 := by
    rw [← s₂]
    exact Finset.sum_le_sum fun x _ => min_le_right _ _
  have hE : ∑ x, max (R * P₁ x - P₂ x) 0 = R - ∑ x, min (R * P₁ x) (P₂ x) := by
    rw [Finset.sum_congr rfl fun x _ => max_sub_zero_eq (R * P₁ x) (P₂ x),
      Finset.sum_sub_distrib, ← Finset.mul_sum, s₁, mul_one]
  rw [hE]
  constructor <;> linarith

/-- **Lemma 2, the mean of a bounded observable, for two arbitrary probability vectors.**
`P₁, P₂ ≥ 0` of total mass `1`, `R > 1`, `0 ≤ f ≤ 1`: the `f`-mean of the normalised excess
`D = (R·P₁ − P₂)₊` differs from the `f`-mean of `P₁` by at most `1/(R − 1)`. -/
theorem excess_mean_bound {P₁ P₂ : X → ℝ} (h₁ : ∀ x, 0 ≤ P₁ x) (h₂ : ∀ x, 0 ≤ P₂ x)
    (s₁ : ∑ x, P₁ x = 1) (s₂ : ∑ x, P₂ x = 1) {R : ℝ} (hR : 1 < R) {f : X → ℝ}
    (hf0 : ∀ x, 0 ≤ f x) (hf1 : ∀ x, f x ≤ 1) :
    |(∑ x, max (R * P₁ x - P₂ x) 0 * f x) / (∑ x, max (R * P₁ x - P₂ x) 0) -
        ∑ x, P₁ x * f x| ≤ 1 / (R - 1) := by
  have hR0 : 0 ≤ R := by linarith
  have hmin0 : ∀ x, 0 ≤ min (R * P₁ x) (P₂ x) := fun x =>
    le_min (mul_nonneg hR0 (h₁ x)) (h₂ x)
  have hJ0 : 0 ≤ ∑ x, min (R * P₁ x) (P₂ x) := Finset.sum_nonneg fun x _ => hmin0 x
  have hJ1 : ∑ x, min (R * P₁ x) (P₂ x) ≤ 1 := by
    rw [← s₂]
    exact Finset.sum_le_sum fun x _ => min_le_right _ _
  have hJf0 : 0 ≤ ∑ x, min (R * P₁ x) (P₂ x) * f x :=
    Finset.sum_nonneg fun x _ => mul_nonneg (hmin0 x) (hf0 x)
  have hJfJ : ∑ x, min (R * P₁ x) (P₂ x) * f x ≤ ∑ x, min (R * P₁ x) (P₂ x) :=
    Finset.sum_le_sum fun x _ => mul_le_of_le_one_right (hmin0 x) (hf1 x)
  have hc0 : 0 ≤ ∑ x, P₁ x * f x := Finset.sum_nonneg fun x _ => mul_nonneg (h₁ x) (hf0 x)
  have hc1 : ∑ x, P₁ x * f x ≤ 1 := by
    rw [← s₁]
    exact Finset.sum_le_sum fun x _ => mul_le_of_le_one_right (h₁ x) (hf1 x)
  have hE : ∑ x, max (R * P₁ x - P₂ x) 0 = R - ∑ x, min (R * P₁ x) (P₂ x) := by
    rw [Finset.sum_congr rfl fun x _ => max_sub_zero_eq (R * P₁ x) (P₂ x),
      Finset.sum_sub_distrib, ← Finset.mul_sum, s₁, mul_one]
  have hN : ∑ x, max (R * P₁ x - P₂ x) 0 * f x =
      R * ∑ x, P₁ x * f x - ∑ x, min (R * P₁ x) (P₂ x) * f x := by
    rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [max_sub_zero_eq]
    ring
  rw [hE, hN]
  exact excess_core hR hJ0 hJ1 hJf0 hJfJ hc0 hc1

end Lemma2

/-! ## Part 6: Lemma 3 (ii) and Lemma 2 in the setting of the report -/

section Report

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- **Lemma 3 (ii), as in the report**: reference weight `π = Bernoulli(p)^{⊗n}`, compensator
the normalised additive instance `w̃_{γ₂}` with `|γ₂| ≤ u`, of density `p₂ = p_{γ₂}`. -/
theorem lemma3_compensation_bernoulli [Nonempty ι] {G : Set (Equiv.Perm ι)}
    (hG : SiteTransitive G) {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1)
    {w Δ : (ι → Bool) → ℝ} (hw : InCone u w) (hwG : Invariant G w)
    (hΔ0 : ∀ x, 0 ≤ Δ x) (hΔ1 : ∃ x, Δ x ≠ 0) (hwΔ : InCone u (fun x => w x + Δ x))
    (hΔG : Invariant G Δ) {γ₂ : ℝ} (hγ₂ : |γ₂| ≤ u)
    (hbetween : (densW (refW p) w < densW (refW p) Δ ∧ densW (refW p) Δ < pTilt p γ₂) ∨
      (pTilt p γ₂ < densW (refW p) Δ ∧ densW (refW p) Δ < densW (refW p) w)) :
    ∃ b : ℝ, b = massW (refW p) w * (densW (refW p) Δ - densW (refW p) w) /
        (pTilt p γ₂ - densW (refW p) Δ) ∧ 0 < b ∧
      InCone u (fun x => w x + b * tiltW p (fun _ => γ₂) x) ∧
      InCone u (fun x => w x + Δ x + b * tiltW p (fun _ => γ₂) x) ∧
      Invariant G (fun x => w x + b * tiltW p (fun _ => γ₂) x) ∧
      Invariant G (fun x => w x + Δ x + b * tiltW p (fun _ => γ₂) x) ∧
      (∀ i, margW (refW p) (fun x => w x + b * tiltW p (fun _ => γ₂) x) i = densW (refW p) Δ) ∧
      (∀ i, margW (refW p) (fun x => w x + Δ x + b * tiltW p (fun _ => γ₂) x) i =
        densW (refW p) Δ) ∧
      (∀ x, w x + Δ x + b * tiltW p (fun _ => γ₂) x ≠ w x + b * tiltW p (fun _ => γ₂) x ↔
        0 < Δ x) ∧
      massW (refW p) (fun x => w x + Δ x + b * tiltW p (fun _ => γ₂) x) /
          massW (refW p) (fun x => w x + b * tiltW p (fun _ => γ₂) x) =
        1 + massW (refW p) Δ / massW (refW p) w *
          ((pTilt p γ₂ - densW (refW p) Δ) / (pTilt p γ₂ - densW (refW p) w)) := by
  have hd : densW (refW p) (tiltW (ι := ι) p fun _ => γ₂) = pTilt p γ₂ :=
    densW_tiltW_const hp0 hp1 γ₂
  have h := lemma3_compensation hG (refW_pos hp0 hp1) (refW_invariant p G) hw hwG hΔ0 hΔ1 hwΔ hΔG
    (tiltW_inCone hp0 hp1 (fun _ => hγ₂)) (tiltW_const_invariant p γ₂ G)
    (massW_tiltW hp0 hp1 _) (by rw [hd]; exact hbetween)
  rw [hd] at h
  exact h

/-- The fields of the cone at `s`: `−u` where `s_i = 1`, `+u` where `s_i = 0`. -/
def coneField (u : ℝ) (s : ι → Bool) (i : ι) : ℝ := if s i = true then -u else u

/-- **The normalised cone weight** `c̃_s = e^{−u·d(·,s)}/Z_s`, as the additive instance with the
site fields `coneField u s` (see `coneW_eq`). -/
def coneW (p u : ℝ) (s : ι → Bool) : (ι → Bool) → ℝ := tiltW p (coneField u s)

/-- **The normalised additive base** `w̃_γ = e^{−γ|x|}/(q + p e^{−γ})ⁿ` (see `baseW_eq`). -/
def baseW (p γ : ℝ) : (ι → Bool) → ℝ := tiltW p fun _ => γ

/-- **The excess of the dip** of depth `r` at `s` on the base `γ`:
`Δ_{s,r} = (e^r c̃_s − w̃_γ)₊`. -/
def dipW (p u γ r : ℝ) (s : ι → Bool) (x : ι → Bool) : ℝ :=
  max (Real.exp r * coneW p u s x - baseW p γ x) 0

omit [Fintype ι] [DecidableEq ι] in
theorem abs_coneField {u : ℝ} (hu : 0 ≤ u) (s : ι → Bool) (i : ι) : |coneField u s i| ≤ u := by
  unfold coneField
  split_ifs
  · rw [abs_neg, abs_of_nonneg hu]
  · rw [abs_of_nonneg hu]

/-- `c̃_s ∈ 𝒲_u`. -/
theorem coneW_inCone {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hu : 0 ≤ u) (s : ι → Bool) :
    InCone u (coneW p u s) :=
  tiltW_inCone hp0 hp1 (abs_coneField hu s)

/-- `w̃_γ ∈ 𝒲_u` for `|γ| ≤ u`. -/
theorem baseW_inCone {p u γ : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hγ : |γ| ≤ u) :
    InCone u (baseW (ι := ι) p γ) :=
  tiltW_inCone hp0 hp1 fun _ => hγ

omit [DecidableEq ι] in
/-- `w̃_γ = e^{−γ|x|}/(q + p e^{−γ})ⁿ`. -/
theorem baseW_eq (p γ : ℝ) (x : ι → Bool) :
    baseW p γ x = Real.exp (-γ * (wt x : ℝ)) / tiltZ p γ ^ Fintype.card ι := by
  have hsite : ∀ i, tiltFac p γ (x i) = (if x i = true then Real.exp (-γ) else 1) / tiltZ p γ := by
    intro i
    cases x i
    · rfl
    · rfl
  show ∏ i, tiltFac p γ (x i) = _
  rw [Finset.prod_congr rfl fun i _ => hsite i, Finset.prod_div_distrib, Finset.prod_const,
    Finset.card_univ, ← Finset.prod_filter, Finset.prod_const, ← Real.exp_nat_mul]
  unfold wt
  congr 2
  ring

omit [DecidableEq ι] in
/-- `c̃_s = e^{−u·d_H(x,s)}/Z_s` with `Z_s = ∏_i z_{s_i}`, `z_0 = q + p e^{−u}`, `z_1 = q e^{−u} + p`:
the additive instance with the fields `±u` is the normalised cone of the report. -/
theorem coneW_eq {p u : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (s x : ι → Bool) :
    coneW p u s x = Real.exp (-u * (hammingDist x s : ℝ)) /
      ∏ i, (if s i = true then (1 - p) * Real.exp (-u) + p else (1 - p) + p * Real.exp (-u)) := by
  have he : Real.exp u * Real.exp (-u) = 1 := by
    rw [← Real.exp_add, add_neg_cancel, Real.exp_zero]
  have hZ1 : 0 < (1 - p) * Real.exp (-u) + p :=
    add_pos (mul_pos (by linarith) (Real.exp_pos _)) hp0
  have hZ2 : 0 < (1 - p) + p * Real.exp (-u) := tiltZ_pos hp0 hp1 u
  have hZ3 : 0 < (1 - p) + p * Real.exp u := by
    have h := tiltZ_pos hp0 hp1 (-u)
    unfold tiltZ at h
    rwa [neg_neg] at h
  have hsite : ∀ i, tiltFac p (coneField u s i) (x i) =
      Real.exp (-u * (if x i ≠ s i then (1 : ℝ) else 0)) /
        (if s i = true then (1 - p) * Real.exp (-u) + p else (1 - p) + p * Real.exp (-u)) := by
    intro i
    unfold coneField
    rcases Bool.eq_false_or_eq_true (s i) with hs | hs <;>
      rcases Bool.eq_false_or_eq_true (x i) with hx | hx <;> rw [hs, hx]
    · -- s = 1, x = 1
      show Real.exp (-(-u)) / tiltZ p (-u) = Real.exp (-u * 0) / ((1 - p) * Real.exp (-u) + p)
      rw [mul_zero, Real.exp_zero]
      unfold tiltZ
      rw [neg_neg, div_eq_div_iff hZ3.ne' hZ1.ne']
      linear_combination (1 - p) * he
    · -- s = 1, x = 0
      show 1 / tiltZ p (-u) = Real.exp (-u * 1) / ((1 - p) * Real.exp (-u) + p)
      rw [mul_one]
      unfold tiltZ
      rw [neg_neg, div_eq_div_iff hZ3.ne' hZ1.ne']
      linear_combination (-p) * he
    · -- s = 0, x = 1
      show Real.exp (-u) / tiltZ p u = Real.exp (-u * 1) / ((1 - p) + p * Real.exp (-u))
      rw [mul_one]
      rfl
    · -- s = 0, x = 0
      show 1 / tiltZ p u = Real.exp (-u * 0) / ((1 - p) + p * Real.exp (-u))
      rw [mul_zero, Real.exp_zero]
      rfl
  have hd : (hammingDist x s : ℝ) = ∑ i, (if x i ≠ s i then (1 : ℝ) else 0) := by
    unfold hammingDist
    rw [Finset.card_filter]
    push_cast
    rfl
  show ∏ i, tiltFac p (coneField u s i) (x i) = _
  rw [Finset.prod_congr rfl fun i _ => hsite i, Finset.prod_div_distrib, ← Real.exp_sum, hd,
    Finset.mul_sum]

omit [DecidableEq ι] in
/-- `π · Δ_{s,r} = (e^r π_s − π_γⁿ)₊`. -/
theorem refW_mul_dipW {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u γ r : ℝ) (s x : ι → Bool) :
    refW p x * dipW p u γ r s x =
      max (Real.exp r * (refW p x * coneW p u s x) - refW p x * baseW p γ x) 0 := by
  unfold dipW
  rw [mul_max_of_nonneg _ _ (refW_pos hp0 hp1 x).le, mul_zero]
  congr 1
  ring

omit [DecidableEq ι] in
theorem dipW_nonneg (p u γ r : ℝ) (s x : ι → Bool) : 0 ≤ dipW p u γ r s x :=
  le_max_right _ _

omit [DecidableEq ι] in
/-- `w̃_γ + Δ_{s,r} = max(w̃_γ, e^r c̃_s)`. -/
theorem baseW_add_dipW (p u γ r : ℝ) (s x : ι → Bool) :
    baseW p γ x + dipW p u γ r s x = max (baseW p γ x) (Real.exp r * coneW p u s x) := by
  unfold dipW
  rcases le_total (Real.exp r * coneW p u s x) (baseW p γ x) with h | h
  · have h' : Real.exp r * coneW p u s x - baseW p γ x ≤ 0 := by linarith
    rw [max_eq_right h', max_eq_left h, add_zero]
  · have h' : 0 ≤ Real.exp r * coneW p u s x - baseW p γ x := by linarith
    rw [max_eq_left h', max_eq_right h]
    ring

/-- The dip `w̃_γ + Δ_{s,r} = max(w̃_γ, e^r c̃_s)` is in the class. -/
theorem baseW_add_dipW_inCone {p u γ : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hu : 0 ≤ u)
    (hγ : |γ| ≤ u) (r : ℝ) (s : ι → Bool) :
    InCone u (fun x => baseW p γ x + dipW p u γ r s x) := by
  have h := inCone_max (baseW_inCone (ι := ι) hp0 hp1 hγ)
    ((coneW_inCone hp0 hp1 hu s).smul (Real.exp_pos r))
  have e : (fun x => baseW p γ x + dipW p u γ r s x) =
      fun x => max (baseW p γ x) (Real.exp r * coneW p u s x) := by
    funext x
    exact baseW_add_dipW p u γ r s x
  rw [e]
  exact h

/-- **Lemma 2, the mass:** `e^r − 1 ≤ E = A(Δ_{s,r}) ≤ e^r`. -/
theorem lemma2_mass {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u γ r : ℝ) (s : ι → Bool) :
    Real.exp r - 1 ≤ massW (refW p) (dipW p u γ r s) ∧
      massW (refW p) (dipW p u γ r s) ≤ Real.exp r := by
  unfold massW
  rw [Finset.sum_congr rfl fun x _ => refW_mul_dipW hp0 hp1 u γ r s x]
  exact excess_mass_bounds (P₁ := fun x => refW p x * coneW p u s x)
    (P₂ := fun x => refW p x * baseW p γ x)
    (fun x => (mul_pos (refW_pos hp0 hp1 x) (tiltW_pos hp0 hp1 _ x)).le)
    (fun x => (mul_pos (refW_pos hp0 hp1 x) (tiltW_pos hp0 hp1 _ x)).le)
    (massW_tiltW hp0 hp1 (coneField u s)) (massW_tiltW hp0 hp1 fun _ => γ) (Real.exp_pos r).le

/-- **Lemma 2, site by site:** for `r > 0` every one-body marginal of the normalised excess of
the dip is within `1/(e^r − 1)` of the corresponding marginal of the cone law `π_s`. -/
theorem lemma2_site {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u γ : ℝ) {r : ℝ} (hr : 0 < r)
    (s : ι → Bool) (i : ι) :
    |margW (refW p) (dipW p u γ r s) i - pTilt p (coneField u s i)| ≤
      1 / (Real.exp r - 1) := by
  have h := excess_mean_bound (P₁ := fun x => refW p x * coneW p u s x)
    (P₂ := fun x => refW p x * baseW p γ x)
    (fun x => (mul_pos (refW_pos hp0 hp1 x) (tiltW_pos hp0 hp1 _ x)).le)
    (fun x => (mul_pos (refW_pos hp0 hp1 x) (tiltW_pos hp0 hp1 _ x)).le)
    (massW_tiltW hp0 hp1 (coneField u s)) (massW_tiltW hp0 hp1 fun _ => γ)
    (Real.one_lt_exp_iff.mpr hr) (f := fun x => if x i = true then (1 : ℝ) else 0)
    (fun x => by split_ifs <;> norm_num) (fun x => by split_ifs <;> norm_num)
  have e1 : margW (refW p) (dipW p u γ r s) i =
      (∑ x, max (Real.exp r * (refW p x * coneW p u s x) - refW p x * baseW p γ x) 0 *
        (if x i = true then (1 : ℝ) else 0)) /
      ∑ x, max (Real.exp r * (refW p x * coneW p u s x) - refW p x * baseW p γ x) 0 := by
    unfold margW oneW massW
    congr 1
    · refine Finset.sum_congr rfl fun x _ => ?_
      rw [refW_mul_dipW hp0 hp1]
      split_ifs <;> ring
    · exact Finset.sum_congr rfl fun x _ => refW_mul_dipW hp0 hp1 u γ r s x
  have e2 : pTilt p (coneField u s i) =
      ∑ x, refW p x * coneW p u s x * (if x i = true then (1 : ℝ) else 0) := by
    rw [← oneW_tiltW hp0 hp1 (coneField u s) i]
    unfold oneW coneW
    refine Finset.sum_congr rfl fun x _ => ?_
    split_ifs <;> ring
  rw [e1, e2]
  exact h

/-- **Lemma 2, the density:** for `r > 0`, `|c − c₀| ≤ 1/(e^r − 1)`, where `c = dens(Δ_{s,r})` and
`c₀ = dens(c̃_s)` is the density of the cone law. -/
theorem lemma2_dens [Nonempty ι] {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u γ : ℝ) {r : ℝ}
    (hr : 0 < r) (s : ι → Bool) :
    |densW (refW p) (dipW p u γ r s) - densW (refW p) (coneW p u s)| ≤
      1 / (Real.exp r - 1) := by
  have hn : (0 : ℝ) < Fintype.card ι := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos
    exact_mod_cast h0
  have h := excess_mean_bound (P₁ := fun x => refW p x * coneW p u s x)
    (P₂ := fun x => refW p x * baseW p γ x)
    (fun x => (mul_pos (refW_pos hp0 hp1 x) (tiltW_pos hp0 hp1 _ x)).le)
    (fun x => (mul_pos (refW_pos hp0 hp1 x) (tiltW_pos hp0 hp1 _ x)).le)
    (massW_tiltW hp0 hp1 (coneField u s)) (massW_tiltW hp0 hp1 fun _ => γ)
    (Real.one_lt_exp_iff.mpr hr) (f := fun x => (wt x : ℝ) / (Fintype.card ι : ℝ))
    (fun x => div_nonneg (Nat.cast_nonneg _) hn.le)
    (fun x => by
      rw [div_le_one hn]
      exact_mod_cast Finset.card_le_univ _)
  have e1 : densW (refW p) (dipW p u γ r s) =
      (∑ x, max (Real.exp r * (refW p x * coneW p u s x) - refW p x * baseW p γ x) 0 *
        ((wt x : ℝ) / (Fintype.card ι : ℝ))) /
      ∑ x, max (Real.exp r * (refW p x * coneW p u s x) - refW p x * baseW p γ x) 0 := by
    rw [densW_eq_mean]
    unfold massW
    congr 1
    · exact Finset.sum_congr rfl fun x _ => by rw [refW_mul_dipW hp0 hp1]
    · exact Finset.sum_congr rfl fun x _ => refW_mul_dipW hp0 hp1 u γ r s x
  have e2 : densW (refW p) (coneW p u s) =
      ∑ x, refW p x * coneW p u s x * ((wt x : ℝ) / (Fintype.card ι : ℝ)) := by
    have hm : massW (refW p) (coneW p u s) = 1 := massW_tiltW hp0 hp1 (coneField u s)
    rw [densW_eq_mean, hm, div_one]
  rw [e1, e2]
  exact h

/-- The density of the cone law of a centre with `k = |s|` ones:
`c₀ = (k·p₊ + (n − k)·p₋)/n`, `p₊ = p_{−u}`, `p₋ = p_u`. -/
theorem densW_coneW {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u : ℝ) (s : ι → Bool) :
    densW (refW p) (coneW p u s) =
      ((wt s : ℝ) * pTilt p (-u) + ((Fintype.card ι : ℝ) - (wt s : ℝ)) * pTilt p u) /
        (Fintype.card ι : ℝ) := by
  unfold coneW
  rw [densW_tiltW hp0 hp1]
  congr 1
  have hsite : ∀ i, pTilt p (coneField u s i) =
      pTilt p u + (if s i = true then pTilt p (-u) - pTilt p u else 0) := by
    intro i
    unfold coneField
    split_ifs <;> ring
  rw [Finset.sum_congr rfl fun i _ => hsite i, Finset.sum_add_distrib, Finset.sum_const,
    Finset.card_univ, nsmul_eq_mul, ← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
  unfold wt
  ring

end Report

/-! # Part 7: Lemma 1 (a) — indistinguishability with an oracle -/

section OracleLemma

open Classical in
/-- **Lemma 1 (a) (indistinguishability with an oracle), weighted form.**  `G` a class of
instances, `Φ` the target, `O` an oracle (any function of the instance).  An oracle algorithm is
a family `alg ω o` of query algorithms indexed by the seed `ω` and the oracle's answer `o`; on
the instance `g` it runs `alg ω (O g)`.  If it is `(ε/2, δ)`-correct on `G`, and `alt j` are
members of `G` with the oracle answer of `g₀ ∈ G` and `|Φ (alt j) − Φ g₀| > ε`, then for all
weights `wgt ≥ 0` such that every point lies in difference sets `{alt j ≠ g₀}` of total weight at
most `B`: `(1 − 2δ) · Σ_j wgt j ≤ E[#evaluations on g₀] · B`.

This is the theory division's `MetricChain.expected_queries_ge_packing` applied to the plain
query algorithm `alg ω (O g₀)` and the class `{g ∈ G : O g = O g₀}` (the argument of workstream
L1's `theorem4_adaptive_marginal_oracle`, for an arbitrary oracle and class). -/
theorem lemma1a_weighted {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
    {g₀ : X → ℝ} (hg₀ : G g₀) {J : Type*} [Fintype J] (alt : J → X → ℝ)
    (halt : ∀ j, G (alt j)) (hO : ∀ j, O (alt j) = O g₀)
    (hsens : ∀ j, ε < |Φ (alt j) - Φ g₀|) (wgt : J → ℝ) (hwgt : ∀ j, 0 ≤ wgt j) {B : ℝ}
    (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => alt j a ≠ g₀ a), wgt j ≤ B) :
    (1 - 2 * δ) * ∑ j, wgt j ≤ (∑ ω, P ω * ((alg ω (O g₀)).queries g₀).card) * B := by
  have hcorr' : ∀ g : X → ℝ, (G g ∧ O g = O g₀) →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g₀)).output g - Φ g| ≤ ε / 2), P ω := by
    rintro g ⟨hg, hOg⟩
    have h := hcorr g hg
    rw [hOg] at h
    exact h
  exact MetricChain.expected_queries_ge_packing (G := fun g => G g ∧ O g = O g₀) (Φ := Φ)
    (fun ω => alg ω (O g₀)) P hP hP1 hcorr' (g := g₀) ⟨hg₀, rfl⟩ alt
    (fun j => ⟨halt j, hO j⟩) hsens wgt hwgt hcap

open Classical in
/-- **Lemma 1 (a), counting form** (the statement of the report): if every point lies in at most
`B` of the difference sets `D_j = {alt j ≠ g₀}`, then
`(1 − 2δ) · |J| ≤ E[#evaluations on g₀] · B`. -/
theorem lemma1a {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
    {g₀ : X → ℝ} (hg₀ : G g₀) {J : Type*} [Fintype J] (alt : J → X → ℝ)
    (halt : ∀ j, G (alt j)) (hO : ∀ j, O (alt j) = O g₀)
    (hsens : ∀ j, ε < |Φ (alt j) - Φ g₀|) {B : ℝ}
    (hcap : ∀ a, ((univ.filter fun j => alt j a ≠ g₀ a).card : ℝ) ≤ B) :
    (1 - 2 * δ) * (Fintype.card J : ℝ) ≤
      (∑ ω, P ω * ((alg ω (O g₀)).queries g₀).card) * B := by
  have h := lemma1a_weighted O alg P hP hP1 hcorr hg₀ alt halt hO hsens (fun _ => (1 : ℝ))
    (fun _ => zero_le_one) (B := B) (fun a => by
      rw [Finset.sum_const, nsmul_eq_mul, mul_one]
      exact hcap a)
  rwa [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one] at h

open Classical in
/-- **Lemma 1 (a), as displayed in the report:**
`E[#evaluations on g₀] ≥ (1 − 2δ)·|J| / max_x #{j : x ∈ D_j}` (for a positive bound `B` on the
multiplicity). -/
theorem lemma1a_div {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
    {g₀ : X → ℝ} (hg₀ : G g₀) {J : Type*} [Fintype J] (alt : J → X → ℝ)
    (halt : ∀ j, G (alt j)) (hO : ∀ j, O (alt j) = O g₀)
    (hsens : ∀ j, ε < |Φ (alt j) - Φ g₀|) {B : ℝ} (hB : 0 < B)
    (hcap : ∀ a, ((univ.filter fun j => alt j a ≠ g₀ a).card : ℝ) ≤ B) :
    (1 - 2 * δ) * (Fintype.card J : ℝ) / B ≤
      ∑ ω, P ω * ((alg ω (O g₀)).queries g₀).card := by
  rw [div_le_iff₀ hB]
  exact lemma1a O alg P hP hP1 hcorr hg₀ alt halt hO hsens hcap

end OracleLemma

/-! # Part 8: the one-body oracle on the cube; the family of alternatives of Theorem A -/

section CubeOracle

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- **The target** `ln A(ψ) = ln Σ_x π(x) e^{−ψ(x)}`. -/
def logA (π ψ : (ι → Bool) → ℝ) : ℝ := Real.log (massW π fun x => Real.exp (-ψ x))

/-- **The exact one-body marginal oracle** `o(ψ) = (μ_ψ(x_i = 1))_i`. -/
def oracle1 (π ψ : (ι → Bool) → ℝ) : ι → ℝ := fun i => margW π (fun x => Real.exp (-ψ x)) i

theorem oracle1_neg_log {π w : (ι → Bool) → ℝ} (hw : ∀ x, 0 < w x) :
    oracle1 π (fun x => -Real.log (w x)) = fun i => margW π w i := by
  have e : (fun x => Real.exp (-(-Real.log (w x)))) = w := by
    funext x
    rw [neg_neg, Real.exp_log (hw x)]
  show (fun i => margW π (fun x => Real.exp (-(-Real.log (w x)))) i) = _
  rw [e]

theorem logA_neg_log {π w : (ι → Bool) → ℝ} (hw : ∀ x, 0 < w x) :
    logA π (fun x => -Real.log (w x)) = Real.log (massW π w) := by
  have e : (fun x => Real.exp (-(-Real.log (w x)))) = w := by
    funext x
    rw [neg_neg, Real.exp_log (hw x)]
  show Real.log (massW π (fun x => Real.exp (-(-Real.log (w x))))) = _
  rw [e]

open Classical in
/-- **Lemma 1 (a) in the weights, for the one-body oracle on the cube.**  Class `L_u`, target
`ln A`, oracle `oracle1 π`.  Let `w₀ ∈ 𝒲_u` and `w₁ j ∈ 𝒲_u` (`j ∈ J`) all have **all one-body
marginals equal to the same number `c`**, with `ln A(w₁ j) − ln A(w₀) > ε`.  If every point `x`
has `w₁ j x ≠ w₀ x` for at most `B` indices `j`, every `(ε/2, δ)`-correct oracle algorithm makes
at least `(1 − 2δ)|J|/B` evaluations in expectation on `ψ₀ = −ln w₀`. -/
theorem oracle_packing_weights {π : (ι → Bool) → ℝ} {u : ℝ}
    {Ω : Type*} [Fintype Ω] (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool))
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω (oracle1 π ψ)).output ψ - logA π ψ| ≤ ε / 2), P ω)
    {w₀ : (ι → Bool) → ℝ} (hw₀ : InCone u w₀) {c : ℝ} (hc₀ : ∀ i, margW π w₀ i = c)
    {J : Type*} [Fintype J] (w₁ : J → (ι → Bool) → ℝ) (hw₁ : ∀ j, InCone u (w₁ j))
    (hc₁ : ∀ j i, margW π (w₁ j) i = c)
    (hgap : ∀ j, ε < Real.log (massW π (w₁ j)) - Real.log (massW π w₀)) {B : ℝ}
    (hcap : ∀ x, ((univ.filter fun j => w₁ j x ≠ w₀ x).card : ℝ) ≤ B) :
    (1 - 2 * δ) * (Fintype.card J : ℝ) ≤
      (∑ ω, P ω * ((alg ω (oracle1 π fun x => -Real.log (w₀ x))).queries
        fun x => -Real.log (w₀ x)).card) * B := by
  refine lemma1a (G := LipH u) (Φ := logA π) (oracle1 π) alg P hP hP1 hcorr
    (g₀ := fun x => -Real.log (w₀ x)) ((inCone_iff_lipH_log hw₀.1).mp hw₀)
    (fun j x => -Real.log (w₁ j x)) (fun j => (inCone_iff_lipH_log (hw₁ j).1).mp (hw₁ j))
    (fun j => ?_) (fun j => ?_) (fun a => ?_)
  · rw [oracle1_neg_log (hw₁ j).1, oracle1_neg_log hw₀.1]
    funext i
    rw [hc₁ j i, hc₀ i]
  · rw [logA_neg_log (hw₁ j).1, logA_neg_log hw₀.1]
    exact lt_of_lt_of_le (hgap j) (le_abs_self _)
  · refine le_trans ?_ (hcap a)
    have hsub : (univ.filter fun j => (fun j x => -Real.log (w₁ j x)) j a ≠
        (fun x => -Real.log (w₀ x)) a) ⊆ univ.filter fun j => w₁ j a ≠ w₀ a := by
      intro j hj
      rw [Finset.mem_filter] at hj ⊢
      exact ⟨hj.1, fun h => hj.2 (congrArg (fun t => -Real.log t) h)⟩
    exact_mod_cast Finset.card_le_card hsub

/-! ### Site permutations: number of ones, masses, densities, dips -/

omit [DecidableEq ι] in
theorem wt_perm (σ : Equiv.Perm ι) (x : ι → Bool) : wt (x ∘ σ) = wt x := by
  unfold wt
  exact Finset.card_equiv σ fun i => by simp

/-- A site permutation that preserves `π` and carries `w'` to `w` preserves the mass. -/
theorem massW_perm {π w w' : (ι → Bool) → ℝ} (σ : Equiv.Perm ι) (hπ : ∀ x, π (x ∘ σ) = π x)
    (hw : ∀ x, w' (x ∘ σ) = w x) : massW π w' = massW π w := by
  unfold massW
  symm
  refine Fintype.sum_equiv (permCube σ) _ _ fun x => ?_
  show π x * w x = π (x ∘ σ) * w' (x ∘ σ)
  rw [hπ, hw]

theorem wtsum_perm {π w w' : (ι → Bool) → ℝ} (σ : Equiv.Perm ι) (hπ : ∀ x, π (x ∘ σ) = π x)
    (hw : ∀ x, w' (x ∘ σ) = w x) :
    ∑ x, π x * w' x * (wt x : ℝ) = ∑ x, π x * w x * (wt x : ℝ) := by
  symm
  refine Fintype.sum_equiv (permCube σ) _ _ fun x => ?_
  show π x * w x * (wt x : ℝ) = π (x ∘ σ) * w' (x ∘ σ) * (wt (x ∘ σ) : ℝ)
  rw [hπ, hw, wt_perm]

/-- … and the density. -/
theorem densW_perm {π w w' : (ι → Bool) → ℝ} (σ : Equiv.Perm ι) (hπ : ∀ x, π (x ∘ σ) = π x)
    (hw : ∀ x, w' (x ∘ σ) = w x) : densW π w' = densW π w := by
  unfold densW
  rw [wtsum_perm σ hπ hw, massW_perm σ hπ hw]

omit [DecidableEq ι] in
theorem coneW_perm (p u : ℝ) (s : ι → Bool) (σ : Equiv.Perm ι) (x : ι → Bool) :
    coneW p u (s ∘ σ) (x ∘ σ) = coneW p u s x :=
  tiltW_perm p (coneField u s) σ x

omit [DecidableEq ι] in
theorem baseW_perm (p γ : ℝ) (σ : Equiv.Perm ι) (x : ι → Bool) :
    baseW p γ (x ∘ σ) = baseW p γ x :=
  tiltW_perm p (fun _ => γ) σ x

omit [DecidableEq ι] in
/-- Covariance of the dips: `Δ_{s∘σ, r}(x∘σ) = Δ_{s,r}(x)`. -/
theorem dipW_perm (p u γ r : ℝ) (s : ι → Bool) (σ : Equiv.Perm ι) (x : ι → Bool) :
    dipW p u γ r (s ∘ σ) (x ∘ σ) = dipW p u γ r s x := by
  unfold dipW
  rw [coneW_perm, baseW_perm]

theorem massW_dipW_perm (p u γ r : ℝ) (s : ι → Bool) (σ : Equiv.Perm ι) :
    massW (refW p) (dipW p u γ r (s ∘ σ)) = massW (refW p) (dipW p u γ r s) :=
  massW_perm σ (refW_perm p σ) fun x => dipW_perm p u γ r s σ x

theorem densW_dipW_perm (p u γ r : ℝ) (s : ι → Bool) (σ : Equiv.Perm ι) :
    densW (refW p) (dipW p u γ r (s ∘ σ)) = densW (refW p) (dipW p u γ r s) :=
  densW_perm σ (refW_perm p σ) fun x => dipW_perm p u γ r s σ x

omit [DecidableEq ι] in
/-- Two configurations with the same number of ones differ by a site permutation. -/
theorem exists_perm_of_wt_eq {s s' : ι → Bool} (h : wt s = wt s') :
    ∃ σ : Equiv.Perm ι, s' = s ∘ σ := by
  have hcard : Fintype.card {i // s' i = true} = Fintype.card {i // s i = true} := by
    rw [Fintype.card_subtype, Fintype.card_subtype]
    exact h.symm
  let e : {i // s' i = true} ≃ {i // s i = true} := Fintype.equivOfCardEq hcard
  refine ⟨e.extendSubtype, ?_⟩
  funext i
  show s' i = s (e.extendSubtype i)
  rw [Bool.eq_iff_iff]
  constructor
  · intro hi
    exact e.extendSubtype_mem i hi
  · intro hi
    by_contra hni
    exact e.extendSubtype_not_mem i hni hi

/-- **`E_{k,r}` and `c_{k,r}` depend on `(k, r)` only**: the mass and the density of the excess
of a dip are the same for all centres with the same number of ones. -/
theorem massW_densW_dipW_of_wt_eq (p u γ r : ℝ) {s s' : ι → Bool} (h : wt s = wt s') :
    massW (refW p) (dipW p u γ r s') = massW (refW p) (dipW p u γ r s) ∧
      densW (refW p) (dipW p u γ r s') = densW (refW p) (dipW p u γ r s) := by
  obtain ⟨σ, rfl⟩ := exists_perm_of_wt_eq h
  exact ⟨massW_dipW_perm p u γ r s σ, densW_dipW_perm p u γ r s σ⟩

/-- There is a configuration with exactly `k` ones, for every `k ≤ n`. -/
theorem exists_wt_eq {k : ℕ} (hk : k ≤ Fintype.card ι) : ∃ s : ι → Bool, wt s = k := by
  have hk' : k ≤ (univ : Finset ι).card := by
    rw [Finset.card_univ]
    exact hk
  obtain ⟨t, _, ht⟩ := Finset.exists_subset_card_eq hk'
  refine ⟨fun i => decide (i ∈ t), ?_⟩
  unfold wt
  rw [← ht]
  congr 1
  ext i
  simp

/-- `T_k`, the configurations with exactly `k` ones, as a type. -/
abbrev Tk (ι : Type*) [Fintype ι] (k : ℕ) : Type _ := {s : ι → Bool // wt s = k}

/-- A site permutation acts on `T_k`. -/
def permTk (k : ℕ) (σ : Equiv.Perm ι) : Tk ι k ≃ Tk ι k where
  toFun j := ⟨j.1 ∘ σ, by rw [wt_perm]; exact j.2⟩
  invFun j := ⟨j.1 ∘ σ.symm, by rw [wt_perm]; exact j.2⟩
  left_inv j := by
    apply Subtype.ext
    funext i
    simp
  right_inv j := by
    apply Subtype.ext
    funext i
    simp

theorem card_filter_subtype {α : Type*} [Fintype α] (p q : α → Prop) [DecidablePred p]
    [DecidablePred q] :
    (univ.filter fun j : {a // p a} => q j.1).card = (univ.filter fun a => p a ∧ q a).card := by
  refine Finset.card_bij (fun j _ => j.1) ?_ ?_ ?_
  · intro j hj
    rw [Finset.mem_filter] at hj ⊢
    exact ⟨Finset.mem_univ _, j.2, hj.2⟩
  · intro j₁ _ j₂ _ h
    exact Subtype.ext h
  · intro a ha
    rw [Finset.mem_filter] at ha
    exact ⟨⟨a, ha.2.1⟩, Finset.mem_filter.mpr ⟨Finset.mem_univ _, ha.2.2⟩, rfl⟩

omit [DecidableEq ι] in
/-- `D_{s,r} = {Δ_{s,r} > 0} = {x : π_γⁿ(x) < e^r π_s(x)}`. -/
theorem dipW_pos_iff {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u γ r : ℝ) (s x : ι → Bool) :
    0 < dipW p u γ r s x ↔
      refW p x * baseW p γ x < Real.exp r * (refW p x * coneW p u s x) := by
  unfold dipW
  have hπ := refW_pos hp0 hp1 x
  rw [lt_max_iff]
  constructor
  · rintro (h | h)
    · have h1 := mul_lt_mul_of_pos_left (sub_pos.mp h) hπ
      linarith
    · exact absurd h (lt_irrefl 0)
  · intro h
    left
    rw [sub_pos]
    by_contra hle
    have h1 := mul_le_mul_of_nonneg_left (not_lt.mp hle) hπ.le
    linarith

/-- The number of centres `s ∈ T_k` with `x ∈ D_{s,r}`. -/
def dipCount (p u γ r : ℝ) (k : ℕ) (x : ι → Bool) : ℕ :=
  (univ.filter fun s : ι → Bool => wt s = k ∧ 0 < dipW p u γ r s x).card

/-- **`H_{k,r} = max_x P_{s ∼ Unif(T_k)}[x ∈ D_{s,r}]`.** -/
def Hkr (ι : Type*) [Fintype ι] [DecidableEq ι] (p u γ r : ℝ) (k : ℕ) : ℝ :=
  ((univ.sup' univ_nonempty fun x : ι → Bool => dipCount p u γ r k x : ℕ) : ℝ) /
    ((univ.filter fun s : ι → Bool => wt s = k).card : ℝ)

/-! ### Translations of the sites; the averaged excess -/

section Shifts

variable [AddGroup ι]

/-- The translations `i ↦ i + a` of the sites (for `ι = Fin n`: the cyclic shifts). -/
def shiftSet (ι : Type*) [AddGroup ι] : Set (Equiv.Perm ι) :=
  Set.range (Equiv.addRight : ι → Equiv.Perm ι)

omit [Fintype ι] [DecidableEq ι] in
theorem shiftSet_transitive : SiteTransitive (shiftSet ι) := fun i j =>
  ⟨Equiv.addRight (-i + j), ⟨_, rfl⟩, by
    show i + (-i + j) = j
    rw [add_neg_cancel_left]⟩

/-- **The averaged excess** `Δ̄_s = n⁻¹ Σ_a Δ_{σ^a s, r}`, the average of the excess of the dip
over the `n` translates of its centre. -/
def barW (p u γ r : ℝ) (s : ι → Bool) (x : ι → Bool) : ℝ :=
  (∑ a : ι, dipW p u γ r (s ∘ Equiv.addRight a) x) / (Fintype.card ι : ℝ)

omit [DecidableEq ι] in
theorem barW_nonneg (p u γ r : ℝ) (s x : ι → Bool) : 0 ≤ barW p u γ r s x :=
  div_nonneg (Finset.sum_nonneg fun _ _ => dipW_nonneg p u γ r _ x) (Nat.cast_nonneg _)

omit [DecidableEq ι] in
/-- `Δ̄_s` is invariant under the translations. -/
theorem barW_shift (p u γ r : ℝ) (s x : ι → Bool) (b : ι) :
    barW p u γ r s (x ∘ Equiv.addRight b) = barW p u γ r s x := by
  unfold barW
  congr 1
  have h1 : ∀ a : ι, dipW p u γ r (s ∘ Equiv.addRight a) (x ∘ Equiv.addRight b) =
      dipW p u γ r (s ∘ Equiv.addRight (-b + a)) x := by
    intro a
    have e : s ∘ Equiv.addRight a = (s ∘ Equiv.addRight (-b + a)) ∘ Equiv.addRight b := by
      funext i
      show s (i + a) = s (i + b + (-b + a))
      rw [add_assoc, add_neg_cancel_left]
    rw [e, dipW_perm]
  rw [Finset.sum_congr rfl fun a _ => h1 a]
  exact Equiv.sum_comp (Equiv.addLeft (-b)) fun c => dipW p u γ r (s ∘ Equiv.addRight c) x

omit [DecidableEq ι] in
theorem barW_invariant (p u γ r : ℝ) (s : ι → Bool) :
    Invariant (shiftSet ι) (barW p u γ r s) := by
  rintro σ ⟨b, rfl⟩ x
  exact barW_shift p u γ r s x b

omit [AddGroup ι] in
/-- The mass of an average is the average of the masses. -/
theorem massW_avg (π : (ι → Bool) → ℝ) {κ : Type*} (t : Finset κ)
    (f : κ → (ι → Bool) → ℝ) (N : ℝ) :
    massW π (fun x => (∑ a ∈ t, f a x) / N) = (∑ a ∈ t, massW π (f a)) / N := by
  unfold massW
  rw [Finset.sum_comm, Finset.sum_div]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [← Finset.mul_sum, mul_div_assoc]

omit [AddGroup ι] in
theorem wtsum_eq_massW (π w : (ι → Bool) → ℝ) :
    ∑ x, π x * w x * (wt x : ℝ) = massW (fun x => π x * (wt x : ℝ)) w := by
  unfold massW
  exact Finset.sum_congr rfl fun x _ => by ring

/-- `A(Δ̄_s) = A(Δ_{s,r})`. -/
theorem massW_barW (p u γ r : ℝ) (s : ι → Bool) :
    massW (refW p) (barW p u γ r s) = massW (refW p) (dipW p u γ r s) := by
  have hn : (Fintype.card ι : ℝ) ≠ 0 := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0.ne'
  unfold barW
  rw [massW_avg, Finset.sum_congr rfl fun a _ => massW_dipW_perm p u γ r s (Equiv.addRight a),
    Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_div_cancel_left₀ _ hn]

/-- `dens(Δ̄_s) = dens(Δ_{s,r})`. -/
theorem densW_barW (p u γ r : ℝ) (s : ι → Bool) :
    densW (refW p) (barW p u γ r s) = densW (refW p) (dipW p u γ r s) := by
  have hn : (Fintype.card ι : ℝ) ≠ 0 := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0.ne'
  have hw : ∑ x, refW p x * barW p u γ r s x * (wt x : ℝ) =
      ∑ x, refW p x * dipW p u γ r s x * (wt x : ℝ) := by
    rw [wtsum_eq_massW, wtsum_eq_massW]
    unfold barW
    have hterm : ∀ a : ι, massW (fun x => refW p x * (wt x : ℝ))
        (dipW p u γ r (s ∘ Equiv.addRight a)) =
        massW (fun x => refW p x * (wt x : ℝ)) (dipW p u γ r s) := fun a =>
      massW_perm (Equiv.addRight a) (fun x => by rw [refW_perm, wt_perm])
        fun x => dipW_perm p u γ r s (Equiv.addRight a) x
    rw [massW_avg, Finset.sum_congr rfl fun a _ => hterm a, Finset.sum_const, Finset.card_univ,
      nsmul_eq_mul, mul_div_cancel_left₀ _ hn]
  unfold densW
  rw [hw, massW_barW]

/-- `w̃_γ + Δ̄_s`, an average of `n` dips, is in the class. -/
theorem baseW_add_barW_inCone {p u γ : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hu : 0 ≤ u)
    (hγ : |γ| ≤ u) (r : ℝ) (s : ι → Bool) :
    InCone u (fun x => baseW p γ x + barW p u γ r s x) := by
  have hn : (0 : ℝ) < Fintype.card ι := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0
  have h := (InCone.sum (s := (univ : Finset ι)) ⟨0, Finset.mem_univ 0⟩
    (f := fun a x => baseW p γ x + dipW p u γ r (s ∘ Equiv.addRight a) x)
    (fun a _ => baseW_add_dipW_inCone hp0 hp1 hu hγ r _)).smul (inv_pos.mpr hn)
  have e : (fun x => baseW p γ x + barW p u γ r s x) =
      fun x => (Fintype.card ι : ℝ)⁻¹ *
        ∑ a : ι, (baseW p γ x + dipW p u γ r (s ∘ Equiv.addRight a) x) := by
    funext x
    unfold barW
    rw [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    field_simp
  rw [e]
  exact h

omit [DecidableEq ι] in
/-- `{Δ̄_s > 0} ⊆ ∪_a D_{σ^a s, r}`. -/
theorem exists_of_barW_ne_zero {p u γ r : ℝ} {s x : ι → Bool} (h : barW p u γ r s x ≠ 0) :
    ∃ a : ι, dipW p u γ r (s ∘ Equiv.addRight a) x ≠ 0 := by
  by_contra hno
  apply h
  unfold barW
  rw [Finset.sum_eq_zero fun a _ => not_not.mp fun h' => hno ⟨a, h'⟩, zero_div]

/-- **The counting step of Theorem A**: a point lies in `{Δ̄_s > 0}` for at most
`n · #{s ∈ T_k : x ∈ D_{s,r}}` centres `s ∈ T_k` (the translations permute `T_k`). -/
theorem card_barW_ne_zero_le (p u γ r : ℝ) (k : ℕ) (x : ι → Bool) :
    (univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0).card ≤
      Fintype.card ι * (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card := by
  have hsub : (univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0) ⊆
      (univ : Finset ι).biUnion fun a =>
        univ.filter fun j : Tk ι k => dipW p u γ r (j.1 ∘ Equiv.addRight a) x ≠ 0 := by
    intro j hj
    obtain ⟨a, ha⟩ := exists_of_barW_ne_zero (Finset.mem_filter.mp hj).2
    exact Finset.mem_biUnion.mpr
      ⟨a, Finset.mem_univ a, Finset.mem_filter.mpr ⟨Finset.mem_univ j, ha⟩⟩
  have hcard : ∀ a : ι,
      (univ.filter fun j : Tk ι k => dipW p u γ r (j.1 ∘ Equiv.addRight a) x ≠ 0).card =
        (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card := by
    intro a
    refine Finset.card_equiv (permTk k (Equiv.addRight a)) fun j => ?_
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    rfl
  calc (univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0).card
      ≤ ((univ : Finset ι).biUnion fun a =>
          univ.filter fun j : Tk ι k => dipW p u γ r (j.1 ∘ Equiv.addRight a) x ≠ 0).card :=
        Finset.card_le_card hsub
    _ ≤ ∑ a : ι, (univ.filter fun j : Tk ι k =>
          dipW p u γ r (j.1 ∘ Equiv.addRight a) x ≠ 0).card := Finset.card_biUnion_le
    _ = ∑ _a : ι, (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card :=
        Finset.sum_congr rfl fun a _ => hcard a
    _ = Fintype.card ι * (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card := by
        rw [Finset.sum_const, Finset.card_univ, smul_eq_mul]

end Shifts

end CubeOracle

/-! # Part 9: Theorem A -/

section TheoremA

/-- `ω = p₊ − p₋`, the width of the window. -/
def omegaW (p u : ℝ) : ℝ := pTilt p (-u) - pTilt p u

/-- `ω_m = ω · min(m, 1 − m)`, `m = k/n`. -/
def omegaM (p u : ℝ) (k n : ℕ) : ℝ := omegaW p u * min ((k : ℝ) / n) (1 - (k : ℝ) / n)

/-- `κ = ω_m − 1/(e^r − 1)`. -/
def kappaA (p u r : ℝ) (k n : ℕ) : ℝ := omegaM p u k n - 1 / (Real.exp r - 1)

/-- `β = ω/κ`. -/
def betaA (p u r : ℝ) (k n : ℕ) : ℝ := omegaW p u / kappaA p u r k n

/-- The density `c₀(m) = (1 − m)p₋ + m·p₊` of the cone law is at distance at least
`ω·min(m, 1 − m)` from both ends of the window. -/
theorem cone_density_margin {pm pp : ℝ} (hω : pm ≤ pp) {k n : ℕ} (hn : 0 < n) :
    pm + (pp - pm) * min ((k : ℝ) / n) (1 - (k : ℝ) / n) ≤
        ((k : ℝ) * pp + ((n : ℝ) - k) * pm) / n ∧
      ((k : ℝ) * pp + ((n : ℝ) - k) * pm) / n ≤
        pp - (pp - pm) * min ((k : ℝ) / n) (1 - (k : ℝ) / n) := by
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  have e : ((k : ℝ) * pp + ((n : ℝ) - k) * pm) / n = pm + (pp - pm) * ((k : ℝ) / n) := by
    field_simp
    ring
  have h0 : 0 ≤ pp - pm := by linarith
  have h1 := mul_le_mul_of_nonneg_left (min_le_left ((k : ℝ) / n) (1 - (k : ℝ) / n)) h0
  have h2 := mul_le_mul_of_nonneg_left (min_le_right ((k : ℝ) / n) (1 - (k : ℝ) / n)) h0
  rw [e]
  constructor <;> linarith

/-- The choice of the compensator in the proof of Theorem A: if `p_γ` is in the window
`[p₋, p₊]` and `c` is in `[p₋ + κ, p₊ − κ]`, one end `p₂` of the window and a coefficient
`b ≥ 0` with `1 + b ≤ ω/κ` satisfy `p_γ + b·p₂ = c·(1 + b)`.  (The report states `b ≤ ω/κ`; the
proof gives `1 + b ≤ ω/κ`.) -/
theorem exists_compensator {pm pp pg c κ : ℝ} (hκ : 0 < κ) (hpg1 : pm ≤ pg) (hpg2 : pg ≤ pp)
    (hc1 : pm + κ ≤ c) (hc2 : c ≤ pp - κ) :
    ∃ p₂ : ℝ, (p₂ = pp ∨ p₂ = pm) ∧ ∃ b : ℝ, 0 ≤ b ∧ 1 + b ≤ (pp - pm) / κ ∧
      pg + b * p₂ = c * (1 + b) := by
  by_cases h : pg ≤ c
  · have hpos : 0 < pp - c := by linarith
    refine ⟨pp, Or.inl rfl, (c - pg) / (pp - c), div_nonneg (by linarith) hpos.le, ?_, ?_⟩
    · have e : 1 + (c - pg) / (pp - c) = (pp - pg) / (pp - c) := by
        field_simp
        ring
      rw [e, div_le_div_iff₀ hpos hκ]
      exact mul_le_mul (by linarith) (by linarith) hκ.le (by linarith)
    · field_simp
      ring
  · have hpos : 0 < c - pm := by linarith
    have h' : c < pg := not_le.mp h
    refine ⟨pm, Or.inr rfl, (pg - c) / (c - pm), div_nonneg (by linarith) hpos.le, ?_, ?_⟩
    · have e : 1 + (pg - c) / (c - pm) = (pg - pm) / (c - pm) := by
        field_simp
        ring
      rw [e, div_le_div_iff₀ hpos hκ]
      exact mul_le_mul (by linarith) (by linarith) hκ.le (by linarith)
    · field_simp
      ring

universe v

variable {ι : Type*} [Fintype ι] [DecidableEq ι] [AddGroup ι]

open Classical in
/-- **Theorem A, sharpened (every `n`; adaptive algorithms with an exact one-body oracle).**

Sites: any finite additive group `ι` acting on itself by translation, `n = |ι|` (for `ι = Fin n`
the cyclic shifts of the report: `theoremA_fin`).  `0 < p < 1`, `|γ| ≤ u`, `r > 0`, `k ≤ n`,
`ω_m = ω·min(k/n, 1 − k/n)`, `(e^r − 1)·ω_m > 1`, `κ = ω_m − 1/(e^r − 1)`, `β = ω/κ`.

There are `γ₂ ∈ {−u, +u}` and `b ≥ 0` with `1 + b ≤ β` such that the instance
`ψ₀ = −ln(w̃_γ + b·w̃_{γ₂})` is in `L_u`, and every randomised oracle algorithm
(`alg ω o`, run on `ψ` with the oracle answer `o = oracle1 π ψ`, the vector of the one-body
marginals of `μ_ψ`) that is `(ε/2, δ)`-correct for `ln A` on `L_u`, for some
`ε < ln(1 + (e^r − 1)/β)`, satisfies

    1 − 2δ ≤ E[#evaluations on ψ₀] · n · H_{k,r},

`H_{k,r} = max_x P_{s∼Unif(T_k)}[x ∈ D_{s,r}]`.  (The report has `b ≤ β` and the smaller
threshold `ln(1 + (e^r − 1)/(1 + β))`: `theoremA_group`.) -/
theorem theoremA_group_sharp {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hγ : |γ| ≤ u)
    (hr : 0 < r) {k : ℕ} (hk : k ≤ Fintype.card ι)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι)) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ 1 + b ≤ betaA p u r k (Fintype.card ι) ∧
      LipH u (fun x : ι → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / betaA p u r k (Fintype.card ι)) →
        (∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        1 - 2 * δ ≤
          (∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
            ((Fintype.card ι : ℝ) * Hkr ι p u γ r k) := by
  -- basic quantities
  have hu : 0 ≤ u := (abs_nonneg γ).trans hγ
  have hnpos : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
  haveI : Nonempty ι := ⟨0⟩
  have hR1 : 0 < Real.exp r - 1 := by
    have h := Real.one_lt_exp_iff.mpr hr
    linarith
  have hpmpp : pTilt p u ≤ pTilt p (-u) := pTilt_anti hp0 hp1 (by linarith)
  have hω0 : 0 ≤ omegaW p u := by
    unfold omegaW
    linarith
  have hκ : 0 < kappaA p u r k (Fintype.card ι) := by
    unfold kappaA
    rw [sub_pos, div_lt_iff₀ hR1]
    linarith [mul_comm (Real.exp r - 1) (omegaM p u k (Fintype.card ι))]
  -- a fixed centre; mass and density of the dips
  obtain ⟨s₀, hs₀⟩ := exists_wt_eq (ι := ι) hk
  obtain ⟨E, hE⟩ : ∃ E : ℝ, massW (refW p) (dipW p u γ r s₀) = E := ⟨_, rfl⟩
  obtain ⟨c, hc⟩ : ∃ c : ℝ, densW (refW p) (dipW p u γ r s₀) = c := ⟨_, rfl⟩
  have hEc : ∀ s : ι → Bool, wt s = k →
      massW (refW p) (dipW p u γ r s) = E ∧ densW (refW p) (dipW p u γ r s) = c := by
    intro s hs
    have h := massW_densW_dipW_of_wt_eq p u γ r (hs₀.trans hs.symm)
    rw [hE, hc] at h
    exact h
  -- Lemma 2
  have hE1 : Real.exp r - 1 ≤ E := by
    rw [← hE]
    exact (lemma2_mass hp0 hp1 u γ r s₀).1
  have hEpos : 0 < E := lt_of_lt_of_le hR1 hE1
  have hc0 := lemma2_dens hp0 hp1 u γ hr s₀
  rw [hc, densW_coneW hp0 hp1 u s₀, hs₀] at hc0
  have hmargin := cone_density_margin (k := k) hpmpp hnpos
  have hc0' := abs_le.mp hc0
  have hc_lo : pTilt p u + kappaA p u r k (Fintype.card ι) ≤ c := by
    unfold kappaA omegaM omegaW
    linarith [hmargin.1, hc0'.1]
  have hc_hi : c ≤ pTilt p (-u) - kappaA p u r k (Fintype.card ι) := by
    unfold kappaA omegaM omegaW
    linarith [hmargin.2, hc0'.2]
  -- the compensator
  have hγ' := abs_le.mp hγ
  have hpg1 : pTilt p u ≤ pTilt p γ := pTilt_anti hp0 hp1 hγ'.2
  have hpg2 : pTilt p γ ≤ pTilt p (-u) := pTilt_anti hp0 hp1 hγ'.1
  obtain ⟨p₂, hp₂, b, hb0, hbβ', hbeq⟩ := exists_compensator hκ hpg1 hpg2 hc_lo hc_hi
  have hbβ : 1 + b ≤ betaA p u r k (Fintype.card ι) := hbβ'
  obtain ⟨γ₂, hγ₂, hγ₂p⟩ : ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ pTilt p γ₂ = p₂ := by
    rcases hp₂ with h | h
    · exact ⟨-u, Or.inl rfl, h.symm⟩
    · exact ⟨u, Or.inr rfl, h.symm⟩
  have hγ₂u : |γ₂| ≤ u := by
    rcases hγ₂ with h | h
    · rw [h, abs_neg, abs_of_nonneg hu]
    · rw [h, abs_of_nonneg hu]
  have hw₀ : InCone u (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x) :=
    (baseW_inCone hp0 hp1 hγ).add_smul (baseW_inCone hp0 hp1 hγ₂u) hb0
  have hb1 : 0 < 1 + b := by linarith
  refine ⟨γ₂, hγ₂, b, hb0, hbβ, (inCone_iff_lipH_log hw₀.1).mp hw₀, ?_⟩
  intro Ω _ alg P hP hP1 ε δ hε hcorr
  -- the compensated base: mass 1 + b, all marginals c
  have hm0 : massW (refW p) (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x) = 1 + b := by
    rw [massW_add, massW_smul]
    unfold baseW
    rw [massW_tiltW hp0 hp1, massW_tiltW hp0 hp1, mul_one]
  have ho0 : ∀ i, oneW (refW p) (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x) i =
      c * (1 + b) := by
    intro i
    rw [oneW_add, oneW_smul]
    unfold baseW
    rw [oneW_tiltW hp0 hp1, oneW_tiltW hp0 hp1, hγ₂p]
    exact hbeq
  have hmarg0 : ∀ i,
      margW (refW p) (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x) i = c := by
    intro i
    unfold margW
    rw [ho0 i, hm0, mul_div_assoc, div_self hb1.ne', mul_one]
  -- the alternatives
  have hbarm : ∀ j : Tk ι k, massW (refW p) (barW p u γ r j.1) = E := fun j => by
    rw [massW_barW]
    exact (hEc j.1 j.2).1
  have hbard : ∀ j : Tk ι k, densW (refW p) (barW p u γ r j.1) = c := fun j => by
    rw [densW_barW]
    exact (hEc j.1 j.2).2
  have hbaro : ∀ (j : Tk ι k) (i : ι), oneW (refW p) (barW p u γ r j.1) i = c * E := by
    intro j i
    have h := oneW_eq_densW_mul shiftSet_transitive (refW_invariant p _)
      (barW_invariant p u γ r j.1) (by rw [hbarm j]; exact hEpos.ne') i
    rw [hbard j, hbarm j] at h
    exact h
  have hw₁ : ∀ j : Tk ι k, InCone u (fun x : ι → Bool =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) := by
    intro j
    have h := (baseW_add_barW_inCone hp0 hp1 hu hγ r j.1).add_smul
      (baseW_inCone (ι := ι) hp0 hp1 hγ₂u) hb0
    have e : (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) =
        fun x => baseW p γ x + barW p u γ r j.1 x + b * baseW p γ₂ x := by
      funext x
      ring
    rw [e]
    exact h
  have hm1 : ∀ j : Tk ι k, massW (refW p) (fun x : ι → Bool =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) = 1 + b + E := by
    intro j
    rw [massW_add (refW p) (fun x => baseW p γ x + b * baseW p γ₂ x) (barW p u γ r j.1), hm0,
      hbarm j]
  have hm1pos : 0 < 1 + b + E := by linarith
  have hmarg1 : ∀ (j : Tk ι k) (i : ι), margW (refW p) (fun x : ι → Bool =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) i = c := by
    intro j i
    have ho1 : oneW (refW p) (fun x : ι → Bool =>
        baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) i = c * (1 + b + E) := by
      rw [oneW_add (refW p) (fun x => baseW p γ x + b * baseW p γ₂ x) (barW p u γ r j.1),
        ho0 i, hbaro j i]
      ring
    unfold margW
    rw [ho1, hm1 j, mul_div_assoc, div_self hm1pos.ne', mul_one]
  -- the gap
  have hgap : ∀ j : Tk ι k, ε < Real.log (massW (refW p) (fun x : ι → Bool =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x)) -
      Real.log (massW (refW p) (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x)) := by
    intro j
    rw [hm1 j, hm0, ← Real.log_div hm1pos.ne' hb1.ne']
    have hβ1 : 0 < betaA p u r k (Fintype.card ι) := by linarith
    have h1 : (Real.exp r - 1) / betaA p u r k (Fintype.card ι) * (1 + b) ≤ E := by
      calc (Real.exp r - 1) / betaA p u r k (Fintype.card ι) * (1 + b)
          ≤ (Real.exp r - 1) / betaA p u r k (Fintype.card ι) *
            betaA p u r k (Fintype.card ι) :=
            mul_le_mul_of_nonneg_left hbβ (div_nonneg hR1.le hβ1.le)
        _ = Real.exp r - 1 := div_mul_cancel₀ _ hβ1.ne'
        _ ≤ E := hE1
    refine lt_of_lt_of_le hε (Real.log_le_log
      (add_pos_of_pos_of_nonneg one_pos (div_nonneg hR1.le hβ1.le)) ?_)
    rw [le_div_iff₀ hb1]
    linarith
  -- the counting bound
  have hTpos : 0 < (univ.filter fun s : ι → Bool => wt s = k).card :=
    Finset.card_pos.mpr ⟨s₀, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hs₀⟩⟩
  have hTR : (0 : ℝ) < ((univ.filter fun s : ι → Bool => wt s = k).card : ℝ) := by
    exact_mod_cast hTpos
  have hJcard : (Fintype.card (Tk ι k) : ℝ) =
      ((univ.filter fun s : ι → Bool => wt s = k).card : ℝ) := by
    rw [Fintype.card_subtype]
  have hcap : ∀ x : ι → Bool, ((univ.filter fun j : Tk ι k =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x ≠
        baseW p γ x + b * baseW p γ₂ x).card : ℝ) ≤
      (Fintype.card ι : ℝ) * (Hkr ι p u γ r k * (Fintype.card (Tk ι k) : ℝ)) := by
    intro x
    have h1 : (univ.filter fun j : Tk ι k =>
        baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x ≠
          baseW p γ x + b * baseW p γ₂ x) ⊆
        univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0 := by
      intro j hj
      rw [Finset.mem_filter] at hj ⊢
      refine ⟨hj.1, fun h0 => hj.2 ?_⟩
      rw [h0, add_zero]
    have h2 := card_barW_ne_zero_le p u γ r k x
    have h3 : (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card =
        dipCount p u γ r k x := by
      unfold dipCount
      rw [← card_filter_subtype (fun s : ι → Bool => wt s = k)
        (fun s => 0 < dipW p u γ r s x)]
      congr 1
      refine Finset.filter_congr fun j _ => ?_
      exact ⟨fun h => lt_of_le_of_ne (dipW_nonneg p u γ r j.1 x) (Ne.symm h), fun h => h.ne'⟩
    have h4 : dipCount p u γ r k x ≤
        univ.sup' univ_nonempty (fun x : ι → Bool => dipCount p u γ r k x) :=
      Finset.le_sup' (fun x : ι → Bool => dipCount p u γ r k x) (Finset.mem_univ x)
    have h5 : Hkr ι p u γ r k * (Fintype.card (Tk ι k) : ℝ) =
        ((univ.sup' univ_nonempty fun x : ι → Bool => dipCount p u γ r k x : ℕ) : ℝ) := by
      unfold Hkr
      rw [hJcard]
      exact div_mul_cancel₀ _ hTR.ne'
    rw [h5]
    calc ((univ.filter fun j : Tk ι k =>
          baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x ≠
            baseW p γ x + b * baseW p γ₂ x).card : ℝ)
        ≤ ((univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0).card : ℝ) := by
          exact_mod_cast Finset.card_le_card h1
      _ ≤ ((Fintype.card ι * (univ.filter fun j : Tk ι k =>
            dipW p u γ r j.1 x ≠ 0).card : ℕ) : ℝ) := by
          exact_mod_cast h2
      _ = (Fintype.card ι : ℝ) * (dipCount p u γ r k x : ℝ) := by
          rw [h3]
          push_cast
          ring
      _ ≤ (Fintype.card ι : ℝ) *
            ((univ.sup' univ_nonempty fun x : ι → Bool => dipCount p u γ r k x : ℕ) : ℝ) := by
          refine mul_le_mul_of_nonneg_left ?_ (Nat.cast_nonneg _)
          exact_mod_cast h4
  -- Lemma 1 (a)
  have key := oracle_packing_weights alg P hP hP1 hcorr hw₀ hmarg0
    (fun (j : Tk ι k) (x : ι → Bool) => baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x)
    hw₁ hmarg1 hgap hcap
  have hJpos : (0 : ℝ) < (Fintype.card (Tk ι k) : ℝ) := by
    rw [hJcard]
    exact hTR
  have key' : (1 - 2 * δ) * (Fintype.card (Tk ι k) : ℝ) ≤
      (∑ ω, P ω * (((alg ω (oracle1 (refW p)
          fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
          fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
        ((Fintype.card ι : ℝ) * Hkr ι p u γ r k) * (Fintype.card (Tk ι k) : ℝ) := by
    refine le_trans key (le_of_eq ?_)
    ring
  exact le_of_mul_le_mul_right key' hJpos

open Classical in
/-- **Theorem A (every `n`; adaptive algorithms with an exact one-body oracle), with the
constants of the report**: `b ∈ [0, β]` and `ε < ln(1 + (e^r − 1)/(1 + β))`;
`1 − 2δ ≤ E[#evaluations on ψ₀] · n · H_{k,r}`.  A consequence of `theoremA_group_sharp`. -/
theorem theoremA_group {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hγ : |γ| ≤ u) (hr : 0 < r)
    {k : ℕ} (hk : k ≤ Fintype.card ι)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι)) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k (Fintype.card ι) ∧
      LipH u (fun x : ι → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι))) →
        (∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        1 - 2 * δ ≤
          (∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
            ((Fintype.card ι : ℝ) * Hkr ι p u γ r k) := by
  obtain ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, h⟩ :=
    theoremA_group_sharp (ι := ι) hp0 hp1 hγ hr hk hcond
  refine ⟨γ₂, hγ₂, b, hb0, by linarith, hlip, fun Ω _ alg P hP hP1 ε δ hε hcorr => ?_⟩
  have hR1 : 0 < Real.exp r - 1 := by
    have h' := Real.one_lt_exp_iff.mpr hr
    linarith
  have hβ : 0 < betaA p u r k (Fintype.card ι) := by linarith
  refine h Ω alg P hP hP1 ε δ (lt_of_lt_of_le hε (Real.log_le_log ?_ ?_)) hcorr
  · exact add_pos_of_pos_of_nonneg one_pos (div_nonneg hR1.le (by linarith))
  · have h2 : (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι)) ≤
        (Real.exp r - 1) / betaA p u r k (Fintype.card ι) :=
      div_le_div_of_nonneg_left hR1.le hβ (by linarith)
    linarith

omit [AddGroup ι] in
/-- `H_{k,r} > 0`: since `E_{k,r} ≥ e^r − 1 > 0`, some point lies in some dip. -/
theorem Hkr_pos {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr : 0 < r) {k : ℕ}
    (hk : k ≤ Fintype.card ι) : 0 < Hkr ι p u γ r k := by
  obtain ⟨s₀, hs₀⟩ := exists_wt_eq (ι := ι) hk
  have hR1 : 0 < Real.exp r - 1 := by
    have h := Real.one_lt_exp_iff.mpr hr
    linarith
  have hmass : 0 < massW (refW p) (dipW p u γ r s₀) :=
    lt_of_lt_of_le hR1 (lemma2_mass hp0 hp1 u γ r s₀).1
  obtain ⟨x, hx⟩ : ∃ x, dipW p u γ r s₀ x ≠ 0 := by
    by_contra hno
    have hz : massW (refW p) (dipW p u γ r s₀) = 0 := by
      unfold massW
      exact Finset.sum_eq_zero fun x _ => by
        rw [not_not.mp fun h' => hno ⟨x, h'⟩, mul_zero]
    linarith
  have hxpos : 0 < dipW p u γ r s₀ x :=
    lt_of_le_of_ne (dipW_nonneg p u γ r s₀ x) (Ne.symm hx)
  have h1 : 0 < dipCount p u γ r k x :=
    Finset.card_pos.mpr ⟨s₀, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hs₀, hxpos⟩⟩
  have h2 : dipCount p u γ r k x ≤
      univ.sup' univ_nonempty (fun x : ι → Bool => dipCount p u γ r k x) :=
    Finset.le_sup' (fun x : ι → Bool => dipCount p u γ r k x) (Finset.mem_univ x)
  have h3 : 0 < (univ.filter fun s : ι → Bool => wt s = k).card :=
    Finset.card_pos.mpr ⟨s₀, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hs₀⟩⟩
  unfold Hkr
  exact div_pos (by exact_mod_cast lt_of_lt_of_le h1 h2) (by exact_mod_cast h3)

open Classical in
/-- **Theorem A, as displayed in the report:**
`E|Q(ψ₀)| ≥ (1 − 2δ)/(n · H_{k,r})`. -/
theorem theoremA_group_div {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hγ : |γ| ≤ u)
    (hr : 0 < r) {k : ℕ} (hk : k ≤ Fintype.card ι)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι)) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k (Fintype.card ι) ∧
      LipH u (fun x : ι → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι))) →
        (∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        (1 - 2 * δ) / ((Fintype.card ι : ℝ) * Hkr ι p u γ r k) ≤
          ∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ) := by
  obtain ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, h⟩ := theoremA_group (ι := ι) hp0 hp1 hγ hr hk hcond
  refine ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, fun Ω _ alg P hP hP1 ε δ hε hcorr => ?_⟩
  have hnpos : (0 : ℝ) < Fintype.card ι := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0
  rw [div_le_iff₀ (mul_pos hnpos (Hkr_pos hp0 hp1 hr hk))]
  exact h Ω alg P hP hP1 ε δ hε hcorr

open Classical in
/-- **Theorem A on `{0,1}ⁿ` with the cyclic shifts** (the statement of the report):
`X = Fin n → Bool`, `π = Bernoulli(p)^{⊗n}`; the translations of `Fin n` are the cyclic shifts
`i ↦ i + a mod n`.  There are `γ₂ ∈ {−u, +u}` and `b ∈ [0, β]` such that `ψ₀ = −ln(w̃_γ + b·w̃_{γ₂})`
is in `L_u` and every `(ε/2, δ)`-correct oracle algorithm, `ε < ln(1 + (e^r − 1)/(1 + β))`, makes
at least `(1 − 2δ)/(n · H_{k,r})` evaluations on `ψ₀` in expectation. -/
theorem theoremA_fin {n : ℕ} [NeZero n] {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1)
    (hγ : |γ| ≤ u) (hr : 0 < r) {k : ℕ} (hk : k ≤ n)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k n) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k n ∧
      LipH u (fun x : Fin n → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (Fin n → ℝ) → MetricChain.QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k n)) →
        (∀ ψ : (Fin n → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        (1 - 2 * δ) / ((n : ℝ) * Hkr (Fin n) p u γ r k) ≤
          ∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ) := by
  have hk' : k ≤ Fintype.card (Fin n) := by
    rw [Fintype.card_fin]
    exact hk
  have hcond' : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card (Fin n)) := by
    rw [Fintype.card_fin]
    exact hcond
  have h := theoremA_group_div (ι := Fin n) (γ := γ) hp0 hp1 hγ hr hk' hcond'
  rw [Fintype.card_fin] at h
  exact h

end TheoremA

end ScienceL3

/-! ## Axioms -/

#print axioms ScienceL3.lemma3_i
#print axioms ScienceL3.lemma3_compensation
#print axioms ScienceL3.lemma3_compensation_bernoulli
#print axioms ScienceL3.lemma0_window_lipH
#print axioms ScienceL3.lemma2_mass
#print axioms ScienceL3.lemma2_dens
#print axioms ScienceL3.lemma1a_weighted
#print axioms ScienceL3.lemma1a
#print axioms ScienceL3.lemma1a_div
#print axioms ScienceL3.oracle_packing_weights
#print axioms ScienceL3.massW_densW_dipW_of_wt_eq
#print axioms ScienceL3.dipW_pos_iff
#print axioms ScienceL3.barW_invariant
#print axioms ScienceL3.massW_barW
#print axioms ScienceL3.densW_barW
#print axioms ScienceL3.baseW_add_barW_inCone
#print axioms ScienceL3.card_barW_ne_zero_le
#print axioms ScienceL3.exists_compensator
#print axioms ScienceL3.theoremA_group_sharp
#print axioms ScienceL3.theoremA_group
#print axioms ScienceL3.Hkr_pos
#print axioms ScienceL3.theoremA_group_div
#print axioms ScienceL3.theoremA_fin
