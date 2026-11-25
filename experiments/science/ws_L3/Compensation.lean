import Mathlib

/-!
# The compensation lemma (Lemma 3 of workstream F), the window (Lemma 0) and the excess of a dip (Lemma 2)

Science division, workstream L3.  Source: `docs/science/workstreams/SF_REPORT.md` §2.0–§2.1.
This file imports **Mathlib only**.

Setting of the report: `X = {0,1}ⁿ`, reference weight `π = Bernoulli(p)^{⊗n}`, class
`L_u = {ψ : |ψ x − ψ y| ≤ u·d_H(x,y)}`, weights `w = e^{−ψ}`, cone
`𝒲_u = {w > 0 : e^{−u} w(x) ≤ w(x⁽ⁱ⁾) ≤ e^{u} w(x)}`, mass `A(w) = Σ_x π(x) w(x)`, Gibbs measure
`μ_w ∝ π w`, density `dens(w) = Σ_x π(x) w(x) |x| / (n·A(w))`.

Here the cube is `ι → Bool` for an arbitrary finite type `ι` of sites, and in Parts 1–3 the
reference weight `π` is an arbitrary function on the cube (positivity and invariance are
hypotheses where they are used); the product measure enters in Part 4.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL3

open Finset

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

end ScienceL3
