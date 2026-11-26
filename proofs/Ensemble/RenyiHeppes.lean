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

end MetricChain.Ensemble
