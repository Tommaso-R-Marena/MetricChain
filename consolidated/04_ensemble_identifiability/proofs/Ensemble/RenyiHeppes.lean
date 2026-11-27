import Mathlib

/-!
# A Rényi–Heppes theorem for arbitrary observables

Ensemble division (`docs/ensemble/ENSEMBLE_REPORT.md`, Part II, Theorem E4).

Rényi (1952) and Heppes (1956): a discrete probability distribution with `K` atoms in the plane
is determined, among all probability distributions, by its projections on `K + 1` distinct
lines.  The proof uses one property of projections only: two of them determine the point.
`renyi_heppes` is the statement for arbitrary maps on a finite set.

Let `T j : X → Y j`, `j < m`, be any *features* such that two distinct configurations agree on
fewer than `r` of them (any `r` features determine the configuration).  Let `μ` be a
non-negative weight vector supported on at most `K` configurations and `ν` any non-negative
weight vector such that every feature has the same law under `ν` and `μ`.  If
`m ≥ K (r − 1) + 1`, then `ν = μ`.

Nothing is assumed about `ν` beyond non-negativity: it need not be supported on few points.

`renyi_heppes_mass_off_support` is the quantitative form of the first step (report Proposition
E4.1): if for every feature the `ν`-mass of the values that no conformer takes is at most `ε`
— as it is when each law is known within `ε` in total variation — then
`(m − K (r − 1)) · ν(X ∖ S) ≤ m · ε`.
-/

namespace MetricChain.Ensemble

open Finset

variable {X : Type*} [Fintype X] [DecidableEq X]

/-- The law of the feature `T` under the weight vector `ν`, evaluated at the value `t`. -/
def featureLaw {Y : Type*} [DecidableEq Y] (ν : X → ℝ) (T : X → Y) (t : Y) : ℝ :=
  ∑ x ∈ Finset.univ.filter (fun x => T x = t), ν x

/-- **Rényi–Heppes for arbitrary features.** -/
theorem renyi_heppes {m : ℕ} {Y : Fin m → Type*} [∀ j, DecidableEq (Y j)]
    (T : ∀ j, X → Y j) (r K : ℕ)
    (hdet : ∀ x x' : X, x ≠ x' → (Finset.univ.filter fun j => T j x = T j x').card < r)
    (μ ν : X → ℝ) (hν : ∀ x, 0 ≤ ν x)
    (S : Finset X) (hS : ∀ x, x ∉ S → μ x = 0) (hK : S.card ≤ K) (hm : K * (r - 1) < m)
    (hlaw : ∀ j t, featureLaw ν (T j) t = featureLaw μ (T j) t) :
    ν = μ := by
  have hcardS : S.card * (r - 1) < (Finset.univ : Finset (Fin m)).card := by
    rw [Finset.card_univ, Fintype.card_fin]
    exact lt_of_le_of_lt (Nat.mul_le_mul_right _ hK) hm
  -- Step 1: `ν` vanishes outside `S`.
  have step1 : ∀ x, x ∉ S → ν x = 0 := by
    intro x hx
    by_contra hne
    have hpos : 0 < ν x := lt_of_le_of_ne (hν x) (Ne.symm hne)
    have hex : ∀ j, ∃ a ∈ S, T j a = T j x := by
      intro j
      by_contra hno
      push Not at hno
      have h1 : 0 < featureLaw ν (T j) (T j x) := by
        unfold featureLaw
        refine lt_of_lt_of_le hpos ?_
        exact Finset.single_le_sum (f := ν) (fun y _ => hν y)
          (Finset.mem_filter.mpr ⟨Finset.mem_univ x, rfl⟩)
      rw [hlaw] at h1
      have h0 : featureLaw μ (T j) (T j x) = 0 := by
        unfold featureLaw
        refine Finset.sum_eq_zero fun a ha => ?_
        have hTa : T j a = T j x := (Finset.mem_filter.mp ha).2
        exact hS a (fun haS => hno a haS hTa)
      rw [h0] at h1
      exact lt_irrefl _ h1
    choose f hfS hfT using hex
    obtain ⟨a, haS, hcard⟩ :=
      Finset.exists_lt_card_fiber_of_mul_lt_card_of_maps_to
        (s := (Finset.univ : Finset (Fin m))) (t := S) (f := f) (n := r - 1)
        (fun j _ => hfS j) hcardS
    have hsub : (Finset.univ.filter fun j => f j = a) ⊆
        (Finset.univ.filter fun j => T j x = T j a) := by
      intro j hj
      have hja : f j = a := (Finset.mem_filter.mp hj).2
      refine Finset.mem_filter.mpr ⟨Finset.mem_univ j, ?_⟩
      rw [← hja]
      exact (hfT j).symm
    have hle := Finset.card_le_card hsub
    by_cases hxa : x = a
    · exact hx (hxa ▸ haS)
    · have hlt := hdet x a hxa
      omega
  -- Step 2: on `S` the weights agree.
  have step2 : ∀ a, a ∈ S → ν a = μ a := by
    intro a haS
    have hexj : ∃ j, ∀ b ∈ S, b ≠ a → T j b ≠ T j a := by
      by_contra hno
      push Not at hno
      choose g hgS hgne hgT using hno
      have hmaps : ∀ j ∈ (Finset.univ : Finset (Fin m)), g j ∈ S.erase a :=
        fun j _ => Finset.mem_erase.mpr ⟨hgne j, hgS j⟩
      have hcardE : (S.erase a).card * (r - 1) < (Finset.univ : Finset (Fin m)).card := by
        refine lt_of_le_of_lt (Nat.mul_le_mul_right _ ?_) hcardS
        exact Finset.card_le_card (Finset.erase_subset a S)
      obtain ⟨b, hbE, hcard⟩ :=
        Finset.exists_lt_card_fiber_of_mul_lt_card_of_maps_to
          (s := (Finset.univ : Finset (Fin m))) (t := S.erase a) (f := g) (n := r - 1)
          hmaps hcardE
      have hba : b ≠ a := (Finset.mem_erase.mp hbE).1
      have hsub : (Finset.univ.filter fun j => g j = b) ⊆
          (Finset.univ.filter fun j => T j b = T j a) := by
        intro j hj
        have hjb : g j = b := (Finset.mem_filter.mp hj).2
        refine Finset.mem_filter.mpr ⟨Finset.mem_univ j, ?_⟩
        rw [← hjb]
        exact hgT j
      have hle := Finset.card_le_card hsub
      have hlt := hdet b a hba
      omega
    obtain ⟨j, hj⟩ := hexj
    have key : ∀ ρ : X → ℝ, (∀ x, x ∉ S → ρ x = 0) → featureLaw ρ (T j) (T j a) = ρ a := by
      intro ρ hρ
      unfold featureLaw
      refine Finset.sum_eq_single a ?_ ?_
      · intro b hb hba
        have hTb : T j b = T j a := (Finset.mem_filter.mp hb).2
        by_cases hbS : b ∈ S
        · exact absurd hTb (hj b hbS hba)
        · exact hρ b hbS
      · intro ha
        exact (ha (Finset.mem_filter.mpr ⟨Finset.mem_univ a, rfl⟩)).elim
    rw [← key ν step1, ← key μ hS, hlaw]
  funext x
  by_cases hx : x ∈ S
  · exact step2 x hx
  · rw [step1 x hx, hS x hx]

/-- **A modulus for Rényi–Heppes (report Proposition E4.1, first bound).**  Let the features
`T j`, `j < m`, be such that two distinct configurations agree on fewer than `r` of them, let
`S` be a set of at most `K` configurations (the conformers) and `ν` any non-negative weight
vector.  Suppose that for every feature the `ν`-mass of the configurations whose value of that
feature is taken by no conformer is at most `ε` — which holds when the law of the feature
under `ν` is within `ε` in total variation of its law under a measure carried by `S`.  Then

  `(m − K (r − 1)) · ν(X ∖ S) ≤ m · ε`.

Nothing is assumed about `ν` beyond non-negativity. -/
theorem renyi_heppes_mass_off_support {m : ℕ} {Y : Fin m → Type*} [∀ j, DecidableEq (Y j)]
    (T : ∀ j, X → Y j) (r K : ℕ)
    (hdet : ∀ x x' : X, x ≠ x' → (Finset.univ.filter fun j => T j x = T j x').card < r)
    (ν : X → ℝ) (hν : ∀ x, 0 ≤ ν x)
    (S : Finset X) (hK : S.card ≤ K) (ε : ℝ)
    (hlaw : ∀ j, ∑ x ∈ Finset.univ.filter (fun x => ∀ a ∈ S, T j x ≠ T j a), ν x ≤ ε) :
    ((m : ℝ) - ((K * (r - 1) : ℕ) : ℝ)) * ∑ x ∈ Finset.univ.filter (fun x => x ∉ S), ν x
      ≤ (m : ℝ) * ε := by
  classical
  -- the features of `x` whose value no conformer takes
  set good : X → Finset (Fin m) := fun x => Finset.univ.filter fun j => ∀ a ∈ S, T j x ≠ T j a
    with hgood
  -- a configuration outside `S` has at least `m − K (r − 1)` such features
  have hcount : ∀ x, x ∉ S → (m : ℝ) - ((K * (r - 1) : ℕ) : ℝ) ≤ ((good x).card : ℝ) := by
    intro x hx
    have hbad : (Finset.univ.filter fun j : Fin m => ¬ ∀ a ∈ S, T j x ≠ T j a).card
        ≤ S.card * (r - 1) := by
      have hsub : (Finset.univ.filter fun j : Fin m => ¬ ∀ a ∈ S, T j x ≠ T j a) ⊆
          S.biUnion (fun a => Finset.univ.filter fun j : Fin m => T j x = T j a) := by
        intro j hj
        have hj' := (Finset.mem_filter.mp hj).2
        push Not at hj'
        obtain ⟨a, haS, hTa⟩ := hj'
        exact Finset.mem_biUnion.mpr ⟨a, haS, Finset.mem_filter.mpr ⟨Finset.mem_univ j, hTa⟩⟩
      refine (Finset.card_le_card hsub).trans ?_
      refine (Finset.card_biUnion_le).trans ?_
      calc ∑ a ∈ S, (Finset.univ.filter fun j : Fin m => T j x = T j a).card
          ≤ ∑ _a ∈ S, (r - 1) := by
            refine Finset.sum_le_sum fun a ha => ?_
            have hxa : x ≠ a := fun h => hx (h ▸ ha)
            have := hdet x a hxa
            omega
        _ = S.card * (r - 1) := by rw [Finset.sum_const, smul_eq_mul]
    have hsplit : (good x).card +
        (Finset.univ.filter fun j : Fin m => ¬ ∀ a ∈ S, T j x ≠ T j a).card = m := by
      have := Finset.card_filter_add_card_filter_not
        (s := (Finset.univ : Finset (Fin m))) (p := fun j => ∀ a ∈ S, T j x ≠ T j a)
      simpa [hgood] using this
    have hle : S.card * (r - 1) ≤ K * (r - 1) := Nat.mul_le_mul_right _ hK
    have hnat : m ≤ (good x).card + K * (r - 1) := by omega
    have : (m : ℝ) ≤ ((good x).card : ℝ) + ((K * (r - 1) : ℕ) : ℝ) := by exact_mod_cast hnat
    linarith
  -- double counting
  have hswap : ∑ j : Fin m, ∑ x ∈ Finset.univ.filter (fun x => ∀ a ∈ S, T j x ≠ T j a), ν x
      = ∑ x : X, ((good x).card : ℝ) * ν x := by
    have h1 : ∀ j : Fin m, ∑ x ∈ Finset.univ.filter (fun x => ∀ a ∈ S, T j x ≠ T j a), ν x
        = ∑ x : X, if (∀ a ∈ S, T j x ≠ T j a) then ν x else 0 := by
      intro j
      rw [Finset.sum_filter]
    simp_rw [h1]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
  have htotal : ∑ x : X, ((good x).card : ℝ) * ν x ≤ (m : ℝ) * ε := by
    rw [← hswap]
    calc ∑ j : Fin m, ∑ x ∈ Finset.univ.filter (fun x => ∀ a ∈ S, T j x ≠ T j a), ν x
        ≤ ∑ _j : Fin m, ε := Finset.sum_le_sum fun j _ => hlaw j
      _ = (m : ℝ) * ε := by rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  calc ((m : ℝ) - ((K * (r - 1) : ℕ) : ℝ)) * ∑ x ∈ Finset.univ.filter (fun x => x ∉ S), ν x
      = ∑ x ∈ Finset.univ.filter (fun x => x ∉ S), ((m : ℝ) - ((K * (r - 1) : ℕ) : ℝ)) * ν x := by
        rw [Finset.mul_sum]
    _ ≤ ∑ x ∈ Finset.univ.filter (fun x => x ∉ S), ((good x).card : ℝ) * ν x := by
        refine Finset.sum_le_sum fun x hx => ?_
        exact mul_le_mul_of_nonneg_right (hcount x (Finset.mem_filter.mp hx).2) (hν x)
    _ ≤ ∑ x : X, ((good x).card : ℝ) * ν x := by
        refine Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _) ?_
        intro x _ _
        exact mul_nonneg (Nat.cast_nonneg _) (hν x)
    _ ≤ (m : ℝ) * ε := htotal

end MetricChain.Ensemble
