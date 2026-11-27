import Mathlib

/-!
# Two rounds of adaptivity: what two batches can see

Theory report §11.24, Lemma 11.85 for two rounds, in the generality in which its proof works.

A *two-round algorithm* asks a first batch of points, then a second batch that may depend on
the answers to the first, and returns a number that depends on the residual only through
the answers to both batches (`TwoRound`).

* `TwoRound.output_eq_of_virtual` — the deterministic core: if two residuals agree on the
  first batch with a "virtual" residual `v`, and with each other on the second batch that
  the algorithm asks when it is answered by `v`, the algorithm returns the same number on
  both.
* `card_distinguished_le` — the counting form of the coupling argument.  The residuals
  `g s₁ s₂` and `g' s₁ s₂` depend on two hidden parameters.  If on a set `W₁ s₁ s₂` both agree
  with a residual `v s₁` that does not depend on `s₂`, on a set `W₂ s₁ s₂` they agree with each
  other, a fixed point lies outside `W₁` for at most a fraction `p₁` of the pairs `(s₁, s₂)`
  and outside `W₂` for at most a fraction `p₂` of the `s₂`, for every `s₁`, then a two-round
  algorithm with batches of at most `M₁`, `M₂` points returns different numbers on the two
  residuals for at most a fraction `M₁ p₁ + M₂ p₂` of the pairs.  (The second batch is a
  function of `s₁` alone as long as the first batch has seen nothing; this is where "the
  algorithm is given more than it can know" enters: nothing is assumed about what it learns
  about `s₁`.)
* `two_round_bound` — hence a randomised two-round algorithm that is `(ε/2, δ)`-correct on a
  class containing all these residuals, whose targets differ by more than `ε`, satisfies
  `1 − 2δ ≤ M₁ p₁ + M₂ p₂`.
* `two_round_witness` — a concrete instance: to sum an arbitrary function on `N` points to
  within `1/4` with probability `1 − δ`, two batches need `M₁ + M₂ ≥ (1 − 2δ) N` points.

The application (Theorem 11.86: block-radial twins on two blocks of the cube, for which
`M₁ p₁ + M₂ p₂` is exponentially small at a budget above the adaptive exponent) is a paper
proof with exact finite computations; the general statement for `r` rounds is the same
argument by induction and is not formalised.
-/

namespace MetricChain.TwoRounds

open Finset

/-- A deterministic two-round algorithm on the point set `X`: a first batch; a second batch
that depends on the residual only through its values on the first batch; an output that
depends on the residual only through its values on both batches. -/
structure TwoRound (X : Type*) where
  /-- The first batch. -/
  first : Finset X
  /-- The second batch, chosen after the answers to the first. -/
  second : (X → ℝ) → Finset X
  /-- The number returned. -/
  output : (X → ℝ) → ℝ
  second_congr : ∀ g g' : X → ℝ, (∀ x ∈ first, g x = g' x) → second g = second g'
  output_congr : ∀ g g' : X → ℝ, (∀ x ∈ first, g x = g' x) → (∀ x ∈ second g, g x = g' x) →
    output g = output g'

variable {X : Type*}

/-- **Deterministic core.**  If `g` and `g'` agree with a virtual residual `v` on the first
batch, and with each other on the second batch that the algorithm asks when answered by `v`,
the algorithm cannot tell them apart. -/
theorem TwoRound.output_eq_of_virtual (A : TwoRound X) {g g' v : X → ℝ}
    (h1 : ∀ x ∈ A.first, g x = v x) (h1' : ∀ x ∈ A.first, g' x = v x)
    (h2 : ∀ x ∈ A.second v, g x = g' x) : A.output g = A.output g' := by
  have hs : A.second g = A.second v := A.second_congr g v h1
  refine A.output_congr g g' (fun x hx => by rw [h1 x hx, h1' x hx]) (fun x hx => ?_)
  rw [hs] at hx
  exact h2 x hx

open scoped Classical in
/-- **What two batches can see (counting form).**  See the module docstring. -/
theorem card_distinguished_le {S₁ S₂ : Type*} [Fintype S₁] [Fintype S₂] (A : TwoRound X)
    (g g' : S₁ → S₂ → X → ℝ) (v : S₁ → X → ℝ) (W₁ W₂ : S₁ → S₂ → Set X)
    (hW₁ : ∀ s₁ s₂, ∀ x ∈ W₁ s₁ s₂, g s₁ s₂ x = v s₁ x ∧ g' s₁ s₂ x = v s₁ x)
    (hW₂ : ∀ s₁ s₂, ∀ x ∈ W₂ s₁ s₂, g s₁ s₂ x = g' s₁ s₂ x)
    {p₁ p₂ M₂ : ℝ} (hp₂ : 0 ≤ p₂)
    (h₁ : ∀ x, (#{s : S₁ × S₂ | x ∉ W₁ s.1 s.2} : ℝ) ≤ p₁ * (Fintype.card S₁ * Fintype.card S₂))
    (h₂ : ∀ x s₁, (#{s₂ : S₂ | x ∉ W₂ s₁ s₂} : ℝ) ≤ p₂ * Fintype.card S₂)
    (hM₂ : ∀ s₁, (#(A.second (v s₁)) : ℝ) ≤ M₂) :
    (#{s : S₁ × S₂ | A.output (g s.1 s.2) ≠ A.output (g' s.1 s.2)} : ℝ)
      ≤ (#A.first * p₁ + M₂ * p₂) * (Fintype.card S₁ * Fintype.card S₂) := by
  set bad₁ : Finset (S₁ × S₂) := A.first.biUnion fun x => {s : S₁ × S₂ | x ∉ W₁ s.1 s.2} with hbad₁
  set bad₂ : Finset (S₁ × S₂) :=
    (univ : Finset S₁).biUnion fun s₁ =>
      ((A.second (v s₁)).biUnion fun x => ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)).map
        ⟨fun s₂ => (s₁, s₂), fun a b h => by simpa using h⟩ with hbad₂
  -- the distinguished pairs are bad for one of the two batches
  have hsub : ({s : S₁ × S₂ | A.output (g s.1 s.2) ≠ A.output (g' s.1 s.2)} : Finset (S₁ × S₂))
      ⊆ bad₁ ∪ bad₂ := by
    intro s hs
    rw [mem_filter] at hs
    by_contra hnot
    rw [mem_union, not_or] at hnot
    obtain ⟨hn1, hn2⟩ := hnot
    apply hs.2
    refine A.output_eq_of_virtual (v := v s.1) (fun x hx => ?_) (fun x hx => ?_) (fun x hx => ?_)
    · have : x ∈ W₁ s.1 s.2 := by
        by_contra hx'
        exact hn1 (mem_biUnion.2 ⟨x, hx, by simp [hx']⟩)
      exact (hW₁ s.1 s.2 x this).1
    · have : x ∈ W₁ s.1 s.2 := by
        by_contra hx'
        exact hn1 (mem_biUnion.2 ⟨x, hx, by simp [hx']⟩)
      exact (hW₁ s.1 s.2 x this).2
    · have : x ∈ W₂ s.1 s.2 := by
        by_contra hx'
        refine hn2 (mem_biUnion.2 ⟨s.1, mem_univ _, ?_⟩)
        rw [mem_map]
        exact ⟨s.2, mem_biUnion.2 ⟨x, hx, by simp [hx']⟩, rfl⟩
      exact hW₂ s.1 s.2 x this
  have hc₁ : (#bad₁ : ℝ) ≤ #A.first * (p₁ * (Fintype.card S₁ * Fintype.card S₂)) := by
    calc (#bad₁ : ℝ) ≤ ∑ x ∈ A.first, (#({s : S₁ × S₂ | x ∉ W₁ s.1 s.2} : Finset (S₁ × S₂)) : ℝ) := by
          exact_mod_cast card_biUnion_le
      _ ≤ ∑ _x ∈ A.first, p₁ * (Fintype.card S₁ * Fintype.card S₂) := sum_le_sum fun x _ => h₁ x
      _ = #A.first * (p₁ * (Fintype.card S₁ * Fintype.card S₂)) := by rw [sum_const, nsmul_eq_mul]
  have hc₂ : (#bad₂ : ℝ) ≤ Fintype.card S₁ * (M₂ * (p₂ * Fintype.card S₂)) := by
    have hS₂ : (0 : ℝ) ≤ p₂ * Fintype.card S₂ := mul_nonneg hp₂ (Nat.cast_nonneg _)
    have hinner : ∀ s₁ : S₁,
        (#((A.second (v s₁)).biUnion fun x => ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)) : ℝ)
          ≤ M₂ * (p₂ * Fintype.card S₂) := by
      intro s₁
      calc (#((A.second (v s₁)).biUnion fun x => ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)) : ℝ)
          ≤ ∑ x ∈ A.second (v s₁), (#({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂) : ℝ) := by
            exact_mod_cast card_biUnion_le
        _ ≤ ∑ _x ∈ A.second (v s₁), p₂ * Fintype.card S₂ := sum_le_sum fun x _ => h₂ x s₁
        _ = #(A.second (v s₁)) * (p₂ * Fintype.card S₂) := by rw [sum_const, nsmul_eq_mul]
        _ ≤ M₂ * (p₂ * Fintype.card S₂) := mul_le_mul_of_nonneg_right (hM₂ s₁) hS₂
    calc (#bad₂ : ℝ) ≤ ∑ s₁ : S₁, (#(((A.second (v s₁)).biUnion fun x =>
            ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)).map
              ⟨fun s₂ => (s₁, s₂), fun a b h => by simpa using h⟩) : ℝ) := by
          exact_mod_cast card_biUnion_le
      _ = ∑ s₁ : S₁, (#((A.second (v s₁)).biUnion fun x =>
            ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)) : ℝ) := by
          simp only [card_map]
      _ ≤ ∑ _s₁ : S₁, M₂ * (p₂ * Fintype.card S₂) := sum_le_sum fun s₁ _ => hinner s₁
      _ = Fintype.card S₁ * (M₂ * (p₂ * Fintype.card S₂)) := by
          rw [sum_const, card_univ, nsmul_eq_mul]
  calc (#{s : S₁ × S₂ | A.output (g s.1 s.2) ≠ A.output (g' s.1 s.2)} : ℝ)
      ≤ #(bad₁ ∪ bad₂) := by exact_mod_cast card_le_card hsub
    _ ≤ #bad₁ + #bad₂ := by exact_mod_cast card_union_le _ _
    _ ≤ #A.first * (p₁ * (Fintype.card S₁ * Fintype.card S₂))
          + Fintype.card S₁ * (M₂ * (p₂ * Fintype.card S₂)) := add_le_add hc₁ hc₂
    _ = (#A.first * p₁ + M₂ * p₂) * (Fintype.card S₁ * Fintype.card S₂) := by ring

open scoped Classical in
/-- A randomised procedure that is within `ε / 2` of the target with probability at least
`1 − δ` on two residuals whose targets differ by more than `ε` returns different numbers on
them with probability at least `1 − 2δ`.  (No structure of the procedure is used.) -/
theorem prob_output_ne_ge {Ω : Type*} [Fintype Ω] (out : Ω → (X → ℝ) → ℝ) (P : Ω → ℝ)
    (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {Φ : (X → ℝ) → ℝ} {ε δ : ℝ} {g g' : X → ℝ}
    (hc : 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |out ω g - Φ g| ≤ ε / 2), P ω)
    (hc' : 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |out ω g' - Φ g'| ≤ ε / 2), P ω)
    (hΦ : ε < |Φ g - Φ g'|) :
    1 - 2 * δ ≤ ∑ ω ∈ univ.filter (fun ω => out ω g ≠ out ω g'), P ω := by
  have hsub : univ.filter (fun ω => |out ω g - Φ g| ≤ ε / 2) ∩
      univ.filter (fun ω => |out ω g' - Φ g'| ≤ ε / 2) ⊆
        univ.filter (fun ω => out ω g ≠ out ω g') := by
    intro ω hω
    obtain ⟨h1, h2⟩ := Finset.mem_inter.mp hω
    refine Finset.mem_filter.mpr ⟨mem_univ ω, fun heq => ?_⟩
    have c1 := abs_le.mp (Finset.mem_filter.mp h1).2
    have c2 := abs_le.mp (Finset.mem_filter.mp h2).2
    rw [← heq] at c2
    have h3 : |Φ g - Φ g'| ≤ ε := abs_le.mpr ⟨by linarith [c1.2, c2.1], by linarith [c1.1, c2.2]⟩
    linarith
  have hui := Finset.sum_union_inter
    (s₁ := univ.filter (fun ω => |out ω g - Φ g| ≤ ε / 2))
    (s₂ := univ.filter (fun ω => |out ω g' - Φ g'| ≤ ε / 2)) (f := P)
  have hunion : ∑ ω ∈ univ.filter (fun ω => |out ω g - Φ g| ≤ ε / 2) ∪
      univ.filter (fun ω => |out ω g' - Φ g'| ≤ ε / 2), P ω ≤ 1 := by
    rw [← hP1]
    exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) fun ω _ _ => hP ω
  have hinter : 1 - 2 * δ ≤ ∑ ω ∈ univ.filter (fun ω => |out ω g - Φ g| ≤ ε / 2) ∩
      univ.filter (fun ω => |out ω g' - Φ g'| ≤ ε / 2), P ω := by linarith
  exact hinter.trans (Finset.sum_le_sum_of_subset_of_nonneg hsub fun ω _ _ => hP ω)

open scoped Classical in
/-- **Two rounds: the bound.**  A randomised two-round algorithm with batches of at most
`M₁` and `M₂` points that is `(ε/2, δ)`-correct on a class `G` satisfies
`1 − 2δ ≤ M₁ p₁ + M₂ p₂` whenever the class contains twins `g s₁ s₂`, `g' s₁ s₂` (two hidden
parameters) whose targets differ by more than `ε`, which both agree on `W₁ s₁ s₂` with a
residual that does not depend on `s₂`, agree with each other on `W₂ s₁ s₂`, and for which a
fixed point is outside `W₁` for at most a fraction `p₁` of all pairs and outside `W₂` for at
most a fraction `p₂` of the `s₂`, whatever `s₁`. -/
theorem two_round_bound {S₁ S₂ Ω : Type*} [Fintype S₁] [Fintype S₂] [Nonempty S₁] [Nonempty S₂]
    [Fintype Ω] {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (alg : Ω → TwoRound X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ f, G f →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output f - Φ f| ≤ ε / 2), P ω)
    (g g' : S₁ → S₂ → X → ℝ) (v : S₁ → X → ℝ) (W₁ W₂ : S₁ → S₂ → Set X)
    (hg : ∀ s₁ s₂, G (g s₁ s₂)) (hg' : ∀ s₁ s₂, G (g' s₁ s₂))
    (hsens : ∀ s₁ s₂, ε < |Φ (g s₁ s₂) - Φ (g' s₁ s₂)|)
    (hW₁ : ∀ s₁ s₂, ∀ x ∈ W₁ s₁ s₂, g s₁ s₂ x = v s₁ x ∧ g' s₁ s₂ x = v s₁ x)
    (hW₂ : ∀ s₁ s₂, ∀ x ∈ W₂ s₁ s₂, g s₁ s₂ x = g' s₁ s₂ x)
    {p₁ p₂ M₁ M₂ : ℝ} (hp₁ : 0 ≤ p₁) (hp₂ : 0 ≤ p₂)
    (h₁ : ∀ x, (#{s : S₁ × S₂ | x ∉ W₁ s.1 s.2} : ℝ) ≤ p₁ * (Fintype.card S₁ * Fintype.card S₂))
    (h₂ : ∀ x s₁, (#{s₂ : S₂ | x ∉ W₂ s₁ s₂} : ℝ) ≤ p₂ * Fintype.card S₂)
    (hM₁ : ∀ ω, (#(alg ω).first : ℝ) ≤ M₁) (hM₂ : ∀ ω f, (#((alg ω).second f) : ℝ) ≤ M₂) :
    1 - 2 * δ ≤ M₁ * p₁ + M₂ * p₂ := by
  set N : ℝ := (Fintype.card S₁ : ℝ) * Fintype.card S₂ with hN
  have hNpos : 0 < N := by
    have h1 : (0 : ℝ) < Fintype.card S₁ := by exact_mod_cast Fintype.card_pos
    have h2 : (0 : ℝ) < Fintype.card S₂ := by exact_mod_cast Fintype.card_pos
    positivity
  have hdet : ∀ s : S₁ × S₂, 1 - 2 * δ ≤
      ∑ ω ∈ univ.filter (fun ω => (alg ω).output (g s.1 s.2) ≠ (alg ω).output (g' s.1 s.2)), P ω :=
    fun s => prob_output_ne_ge (fun ω => (alg ω).output) P hP hP1
      (hcorr _ (hg s.1 s.2)) (hcorr _ (hg' s.1 s.2)) (hsens s.1 s.2)
  have hrun : ∀ ω, (#{s : S₁ × S₂ | (alg ω).output (g s.1 s.2) ≠ (alg ω).output (g' s.1 s.2)} : ℝ)
      ≤ (M₁ * p₁ + M₂ * p₂) * N := by
    intro ω
    refine (card_distinguished_le (alg ω) g g' v W₁ W₂ hW₁ hW₂ hp₂ h₁ h₂
      (fun s₁ => hM₂ ω (v s₁))).trans ?_
    have : (#(alg ω).first : ℝ) * p₁ ≤ M₁ * p₁ := mul_le_mul_of_nonneg_right (hM₁ ω) hp₁
    exact mul_le_mul_of_nonneg_right (by linarith) hNpos.le
  have hcard : (Fintype.card (S₁ × S₂) : ℝ) = N := by rw [Fintype.card_prod]; push_cast; rfl
  have key : N * (1 - 2 * δ) ≤ (M₁ * p₁ + M₂ * p₂) * N := by
    calc N * (1 - 2 * δ) = ∑ _s : S₁ × S₂, (1 - 2 * δ) := by
          rw [sum_const, card_univ, nsmul_eq_mul, hcard]
      _ ≤ ∑ s : S₁ × S₂, ∑ ω ∈ univ.filter
            (fun ω => (alg ω).output (g s.1 s.2) ≠ (alg ω).output (g' s.1 s.2)), P ω :=
          sum_le_sum fun s _ => hdet s
      _ = ∑ s : S₁ × S₂, ∑ ω,
            if (alg ω).output (g s.1 s.2) ≠ (alg ω).output (g' s.1 s.2) then P ω else 0 := by
          refine sum_congr rfl fun s _ => ?_
          rw [sum_filter]
      _ = ∑ ω, ∑ s : S₁ × S₂,
            if (alg ω).output (g s.1 s.2) ≠ (alg ω).output (g' s.1 s.2) then P ω else 0 :=
          sum_comm
      _ = ∑ ω, P ω *
            #{s : S₁ × S₂ | (alg ω).output (g s.1 s.2) ≠ (alg ω).output (g' s.1 s.2)} := by
          refine sum_congr rfl fun ω _ => ?_
          rw [← sum_filter, sum_const, nsmul_eq_mul, mul_comm]
      _ ≤ ∑ ω, P ω * ((M₁ * p₁ + M₂ * p₂) * N) :=
          sum_le_sum fun ω _ => mul_le_mul_of_nonneg_left (hrun ω) (hP ω)
      _ = (M₁ * p₁ + M₂ * p₂) * N := by rw [← sum_mul, hP1, one_mul]
  have := le_of_mul_le_mul_left (by linarith : N * (1 - 2 * δ) ≤ N * (M₁ * p₁ + M₂ * p₂)) hNpos
  exact this

open scoped Classical in
/-- **A concrete instance (non-vacuity).**  To sum an arbitrary real function on `N` points to
within `1/4` with probability at least `1 − δ`, a randomised two-round algorithm needs
batches with `M₁ + M₂ ≥ (1 − 2δ) N` points: the hidden parameter is the position of a spike,
the twins are the zero function and the spike, and a point sees the difference for exactly
one position. -/
theorem two_round_witness {N : ℕ} [NeZero N] {Ω : Type*} [Fintype Ω]
    (alg : Ω → TwoRound (Fin N)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {δ : ℝ}
    (hcorr : ∀ f : Fin N → ℝ,
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output f - ∑ x, f x| ≤ 1 / 4), P ω)
    {M₁ M₂ : ℝ} (hM₁ : ∀ ω, (#(alg ω).first : ℝ) ≤ M₁)
    (hM₂ : ∀ ω f, (#((alg ω).second f) : ℝ) ≤ M₂) :
    (1 - 2 * δ) * N ≤ M₁ + M₂ := by
  have hNpos : (0 : ℝ) < N := by exact_mod_cast Nat.pos_of_ne_zero (NeZero.ne N)
  have hcardN : (Fintype.card (Fin N) : ℝ) = N := by simp
  have hcardU : (Fintype.card Unit : ℝ) = 1 := by simp
  have hmain := two_round_bound (S₁ := Unit) (S₂ := Fin N) (G := fun _ => True)
    (Φ := fun f : Fin N → ℝ => ∑ x, f x) (ε := 1 / 2) (δ := δ) alg P hP hP1
    (fun f _ => by
      have h := hcorr f
      rwa [show (1 / 4 : ℝ) = 1 / 2 / 2 by norm_num] at h)
    (fun _ _ _ => 0) (fun _ s₂ x => if x = s₂ then 1 else 0) (fun _ _ => 0)
    (fun _ s₂ => {x | x ≠ s₂}) (fun _ s₂ => {x | x ≠ s₂})
    (fun _ _ => trivial) (fun _ _ => trivial)
    (fun _ s₂ => by simp; norm_num)
    (fun _ s₂ x hx => by
      have hx' : x ≠ s₂ := hx
      simp [hx'])
    (fun _ s₂ x hx => by
      have hx' : x ≠ s₂ := hx
      simp [hx'])
    (p₁ := 1 / N) (p₂ := 1 / N) (M₁ := M₁) (M₂ := M₂) (by positivity) (by positivity)
    (fun x => by
      have hsub : ({s : Unit × Fin N | x ∉ ({y | y ≠ s.2} : Set (Fin N))} : Finset (Unit × Fin N))
          ⊆ {((), x)} := by
        intro s hs
        rw [mem_filter] at hs
        have hx : x = s.2 := by
          by_contra hne
          exact hs.2 hne
        rw [mem_singleton]
        exact Prod.ext rfl hx.symm
      have hle : (#({s : Unit × Fin N | x ∉ ({y | y ≠ s.2} : Set (Fin N))} :
          Finset (Unit × Fin N)) : ℝ) ≤ 1 := by
        exact_mod_cast (card_le_card hsub).trans (by simp)
      rw [hcardN, hcardU]
      have : (1 : ℝ) / N * (1 * N) = 1 := by field_simp
      rw [this]
      convert hle)
    (fun x _ => by
      have hsub : ({s₂ : Fin N | x ∉ ({y | y ≠ s₂} : Set (Fin N))} : Finset (Fin N)) ⊆ {x} := by
        intro s hs
        rw [mem_filter] at hs
        have hx : x = s := by
          by_contra hne
          exact hs.2 hne
        rw [mem_singleton]
        exact hx.symm
      have hle : (#({s₂ : Fin N | x ∉ ({y | y ≠ s₂} : Set (Fin N))} : Finset (Fin N)) : ℝ) ≤ 1 := by
        exact_mod_cast (card_le_card hsub).trans (by simp)
      rw [hcardN]
      have : (1 : ℝ) / N * N = 1 := by field_simp
      rw [this]
      convert hle)
    hM₁ hM₂
  have h2 : M₁ * (1 / N) + M₂ * (1 / N) = (M₁ + M₂) / N := by ring
  rw [h2, le_div_iff₀ hNpos] at hmain
  exact hmain

end MetricChain.TwoRounds
