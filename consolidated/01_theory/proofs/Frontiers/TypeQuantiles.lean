import Mathlib

/-!
# Type-wise quantiles of a Lipschitz weight are Lipschitz

Theory report §11.20, Theorem 11.61(a) (workstream F, Theorem F4(a)), in a form that does
not mention the reference measure: it is a statement about a positive weight `w` on the
cube `{0,1}^α` — configurations are identified with the sets of their `1`-coordinates —
whose logarithm is `u`-Lipschitz for the Hamming distance, i.e. `w` changes by at most the
factor `c = e^u` when one coordinate is flipped.

* `upperSet w τ r`: the configurations of type `r` (with `r` ones) on which `w > τ`;
  `upperDensity w τ r`: its fraction of the type class.
* `upperDensity_succ_le`, `upperDensity_pred_le`: the density of `{w > c·τ}` in a type class is
  at most the density of `{w > τ}` in either adjacent type class (the local LYM inequality:
  flipping one uniformly chosen coordinate of the right kind maps the uniform law of a
  type class to that of the adjacent one).
* `admissible_succ`, `admissible_pred`: hence if `τ` is an admissible threshold at type `r` —
  the set above it has density at most `q` — then `c·τ` is admissible at the types `r ± 1`:
  **type-wise upper quantiles differ by at most the factor `c` between adjacent types.**
* `truncate_lipschitz_insert`, `truncate_lipschitz_erase`: truncating `w` at type-dependent
  levels that differ by at most the factor `c` between adjacent types gives a weight in the
  same class; `truncate_ne_iff`: it differs from `w` exactly on the sets above the levels.

Consequence (paper, theory report Theorem 11.61(b)): the weight truncated at its type-wise
`q`-quantiles is a member of the class that differs from the original on a set of density
at most `q` in every type class, so a sample that is uniform on every type class cannot
distinguish the two with fewer than about `1/q` points — for every reference measure that
is uniform on type classes.
-/

namespace MetricChain.TypeQuantiles

open Finset
open scoped FinsetFamily

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- The configurations of type `r` on which the weight exceeds `τ`. -/
noncomputable def upperSet (w : Finset α → ℝ) (τ : ℝ) (r : ℕ) : Finset (Finset α) :=
  (powersetCard r univ).filter fun s => τ < w s

/-- Its density in the type class. -/
noncomputable def upperDensity (w : Finset α → ℝ) (τ : ℝ) (r : ℕ) : ℝ :=
  (#(upperSet w τ r) : ℝ) / (Fintype.card α).choose r

omit [DecidableEq α] in
theorem sized_upperSet (w : Finset α → ℝ) (τ : ℝ) (r : ℕ) :
    (upperSet w τ r : Set (Finset α)).Sized r := by
  intro s hs
  exact (mem_powersetCard.mp (mem_filter.mp (mem_coe.mp hs)).1).2

omit [DecidableEq α] in
theorem mem_upperSet {w : Finset α → ℝ} {τ : ℝ} {r : ℕ} {s : Finset α} :
    s ∈ upperSet w τ r ↔ #s = r ∧ τ < w s := by
  simp [upperSet, mem_powersetCard]

/-- The shadow of the set above `c·τ` at type `r + 1` lies above `τ` at type `r`. -/
theorem shadow_upperSet_subset {w : Finset α → ℝ} {c : ℝ} (hc : 0 < c)
    (hup : ∀ (t : Finset α) (a : α), a ∉ t → w (insert a t) ≤ c * w t) (τ : ℝ) (r : ℕ) :
    ∂ (upperSet w (c * τ) (r + 1)) ⊆ upperSet w τ r := by
  intro t ht
  obtain ⟨s, hs, a, ha, rfl⟩ := mem_shadow_iff.mp ht
  obtain ⟨hcard, hw⟩ := mem_upperSet.mp hs
  refine mem_upperSet.mpr ⟨by rw [card_erase_of_mem ha, hcard]; rfl, ?_⟩
  have h1 : w s ≤ c * w (s.erase a) := by
    have := hup (s.erase a) a (notMem_erase a s)
    rwa [insert_erase ha] at this
  have h2 : c * τ < c * w (s.erase a) := lt_of_lt_of_le hw h1
  exact lt_of_mul_lt_mul_left h2 hc.le

/-- The upper shadow of the set above `c·τ` at type `r` lies above `τ` at type `r + 1`. -/
theorem upShadow_upperSet_subset {w : Finset α → ℝ} {c : ℝ} (hc : 0 < c)
    (hdown : ∀ (t : Finset α) (a : α), a ∉ t → w t ≤ c * w (insert a t)) (τ : ℝ) (r : ℕ) :
    ∂⁺ (upperSet w (c * τ) r) ⊆ upperSet w τ (r + 1) := by
  intro t ht
  obtain ⟨s, hs, a, ha, rfl⟩ := mem_upShadow_iff.mp ht
  obtain ⟨hcard, hw⟩ := mem_upperSet.mp hs
  refine mem_upperSet.mpr ⟨by rw [card_insert_of_notMem ha, hcard], ?_⟩
  have h2 : c * τ < c * w (insert a s) := lt_of_lt_of_le hw (hdown s a ha)
  exact lt_of_mul_lt_mul_left h2 hc.le

/-- **Going up one type.**  The density of `{w > c·τ}` at type `r + 1` is at most the density
of `{w > τ}` at type `r`. -/
theorem upperDensity_succ_le {w : Finset α → ℝ} {c : ℝ} (hc : 0 < c)
    (hup : ∀ (t : Finset α) (a : α), a ∉ t → w (insert a t) ≤ c * w t) (τ : ℝ) (r : ℕ) :
    upperDensity w (c * τ) (r + 1) ≤ upperDensity w τ r := by
  unfold upperDensity
  have hlym := local_lubell_yamamoto_meshalkin_inequality_div (𝕜 := ℝ) (Nat.succ_ne_zero r)
    (sized_upperSet w (c * τ) (r + 1))
  simp only [Nat.succ_eq_add_one, Nat.add_sub_cancel] at hlym
  refine hlym.trans (div_le_div_of_nonneg_right ?_ (Nat.cast_nonneg _))
  exact_mod_cast card_le_card (shadow_upperSet_subset hc hup τ r)

/-- **Going down one type.**  For `r < n`, the density of `{w > c·τ}` at type `r` is at most
the density of `{w > τ}` at type `r + 1`. -/
theorem upperDensity_pred_le {w : Finset α → ℝ} {c : ℝ} (hc : 0 < c)
    (hdown : ∀ (t : Finset α) (a : α), a ∉ t → w t ≤ c * w (insert a t)) (τ : ℝ) {r : ℕ}
    (hr : r < Fintype.card α) :
    upperDensity w (c * τ) r ≤ upperDensity w τ (r + 1) := by
  unfold upperDensity
  set 𝒜 := upperSet w (c * τ) r with h𝒜
  -- the complements form a family of sets of size `n - r`
  have hsized : ((𝒜ᶜˢ : Finset (Finset α)) : Set (Finset α)).Sized (Fintype.card α - r) := by
    intro s hs
    have hs' : sᶜ ∈ 𝒜 := mem_compls.mp (mem_coe.mp hs)
    have hcard := (mem_upperSet.mp hs').1
    rw [card_compl] at hcard
    have := card_le_univ s
    omega
  have hlym := local_lubell_yamamoto_meshalkin_inequality_div (𝕜 := ℝ)
    (Nat.sub_ne_zero_of_lt hr) hsized
  rw [card_compls, shadow_compls, card_compls, Nat.choose_symm hr.le] at hlym
  have hsym : (Fintype.card α).choose (Fintype.card α - r - 1) = (Fintype.card α).choose (r + 1) := by
    rw [Nat.sub_sub, Nat.choose_symm (Nat.succ_le_of_lt hr)]
  rw [hsym] at hlym
  refine hlym.trans (div_le_div_of_nonneg_right ?_ (Nat.cast_nonneg _))
  exact_mod_cast card_le_card (upShadow_upperSet_subset hc hdown τ r)

/-- A threshold is admissible at type `r` for the density `q` if the set above it has
density at most `q` in the type class. -/
def Admissible (w : Finset α → ℝ) (q : ℝ) (r : ℕ) (τ : ℝ) : Prop := upperDensity w τ r ≤ q

/-- **Type-wise quantiles are Lipschitz, upwards.** -/
theorem admissible_succ {w : Finset α → ℝ} {c : ℝ} (hc : 0 < c)
    (hup : ∀ (t : Finset α) (a : α), a ∉ t → w (insert a t) ≤ c * w t) {q τ : ℝ} {r : ℕ}
    (h : Admissible w q r τ) : Admissible w q (r + 1) (c * τ) :=
  (upperDensity_succ_le hc hup τ r).trans h

/-- **Type-wise quantiles are Lipschitz, downwards.** -/
theorem admissible_pred {w : Finset α → ℝ} {c : ℝ} (hc : 0 < c)
    (hdown : ∀ (t : Finset α) (a : α), a ∉ t → w t ≤ c * w (insert a t)) {q τ : ℝ} {r : ℕ}
    (hr : r < Fintype.card α) (h : Admissible w q (r + 1) τ) : Admissible w q r (c * τ) :=
  (upperDensity_pred_le hc hdown τ hr).trans h

/-- The weight truncated at type-dependent levels. -/
noncomputable def truncate (w : Finset α → ℝ) (thr : ℕ → ℝ) (s : Finset α) : ℝ := min (w s) (thr #s)

omit [Fintype α] in
/-- **The truncated weight stays in the class** (one coordinate switched on). -/
theorem truncate_lipschitz_insert {w : Finset α → ℝ} {c : ℝ} (hc : 0 < c) {thr : ℕ → ℝ}
    (hup : ∀ (t : Finset α) (a : α), a ∉ t → w (insert a t) ≤ c * w t)
    (hthr : ∀ r, thr (r + 1) ≤ c * thr r) (t : Finset α) (a : α) (ha : a ∉ t) :
    truncate w thr (insert a t) ≤ c * truncate w thr t := by
  unfold truncate
  rw [card_insert_of_notMem ha, mul_min_of_nonneg _ _ hc.le]
  exact min_le_min (hup t a ha) (hthr _)

omit [Fintype α] in
/-- **The truncated weight stays in the class** (one coordinate switched off). -/
theorem truncate_lipschitz_erase {w : Finset α → ℝ} {c : ℝ} (hc : 0 < c) {thr : ℕ → ℝ}
    (hdown : ∀ (t : Finset α) (a : α), a ∉ t → w t ≤ c * w (insert a t))
    (hthr : ∀ r, thr r ≤ c * thr (r + 1)) (t : Finset α) (a : α) (ha : a ∉ t) :
    truncate w thr t ≤ c * truncate w thr (insert a t) := by
  unfold truncate
  rw [card_insert_of_notMem ha, mul_min_of_nonneg _ _ hc.le]
  exact min_le_min (hdown t a ha) (hthr _)

omit [DecidableEq α] in
/-- The truncated weight differs from the weight exactly on the sets above the levels. -/
theorem truncate_ne_iff {w : Finset α → ℝ} {thr : ℕ → ℝ} {s : Finset α} :
    truncate w thr s ≠ w s ↔ s ∈ upperSet w (thr #s) #s := by
  unfold truncate
  rw [mem_upperSet]
  constructor
  · intro h
    refine ⟨rfl, ?_⟩
    by_contra hle
    exact h (min_eq_left (not_lt.mp hle))
  · rintro ⟨-, hlt⟩ h
    rw [min_eq_right hlt.le] at h
    exact absurd h hlt.ne

/-- Non-vacuity: the weight `w(s) = 2^{#s}` on three sites changes by the factor `2` per
flipped coordinate; the threshold `1` is admissible at type `0` for the density `0` (the
empty configuration has weight `1`), hence `2` is admissible at type `1`. -/
theorem witness_admissible :
    Admissible (fun s : Finset (Fin 3) => (2 : ℝ) ^ #s) 0 1 (2 * 1) := by
  refine admissible_succ (by norm_num) (fun t a ha => ?_) ?_
  · rw [card_insert_of_notMem ha, pow_succ]; linarith
  · unfold Admissible upperDensity
    have hempty : upperSet (fun s : Finset (Fin 3) => (2 : ℝ) ^ #s) 1 0 = ∅ := by
      ext s
      simp only [mem_upperSet, notMem_empty, iff_false, not_and, not_lt]
      intro hs
      rw [hs]; norm_num
    rw [hempty]; simp

end MetricChain.TypeQuantiles
