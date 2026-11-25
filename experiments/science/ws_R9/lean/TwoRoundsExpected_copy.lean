import proofs.Frontiers.TwoRounds

/-!
# R4 (review SCI-REV-0003): two rounds, with *expected* batch sizes, at one instance

*Provenance.*  This file was written by the Scientific Discovery Division (branch `research/scientific-translation`,
`experiments/science/ws_R4/lean/TwoRoundsExpected.lean`, as published with its review SCI-REV-0003) and is adopted here
unchanged except for this paragraph and the removal of its four closing `#print axioms` commands, which are now in
`proofs/AxiomAudit.lean`.  It was compiled by the theory division against `TwoRounds.lean` before adoption
(theory report §11.24, Theorem R4.1 and Corollary R4.2).

`proofs/Frontiers/TwoRounds.lean` (`two_round_bound`) assumes worst-case bounds on the two batch
sizes, the second one for *every* function `f : X → ℝ`.  The proof needs much less: the second
batch is only ever counted when the first batch is answered by the virtual residual `v s₁`.
Hence the bound holds with

* the expected size of the first batch (it does not depend on the instance), and
* the expected size of the second batch **on the instances `v s₁`**, averaged over `s₁`.

In the application (theory report §11.24, Theorem 11.86) `v s₁ = g₁(d(x¹, s₁))` is itself a member
of the class `L_u` (the flat histogram of the first block), so the statement becomes a lower
bound for the expected number of evaluations **at the flat-histogram instances**, exactly as
Theorem 11.25(a) is a lower bound at the zero function.  No Markov inequality is needed, and no
assumption on what the algorithm does on other instances.

* `card_distinguished_le_sum` — the counting form with the sizes of the second batches summed
  over the first hidden parameter.
* `two_round_expected_bound` — `1 − 2δ ≤ E|B₁|·p₁ + E_{ω,s₁}|B₂(v s₁)|·p₂`.
* `two_round_expected_cost` — `1 − 2δ ≤ p · E_{ω,s₁}[ |B₁| + |B₂(v s₁)| ]` if `p₁, p₂ ≤ p`.
* `two_round_bound_of_class` — the worst-case form with the bound on the second batch required
  only on a class `G` that contains the `v s₁` (the form in which the paper lemma is applied).
-/

namespace MetricChain.TwoRounds.R4

open Finset MetricChain.TwoRounds

variable {X : Type*}

open scoped Classical in
/-- **Counting form, second batches summed.**  As `card_distinguished_le`, but the sizes of the
second batches asked under the virtual answers `v s₁` are summed over `s₁` instead of being
bounded uniformly. -/
theorem card_distinguished_le_sum {S₁ S₂ : Type*} [Fintype S₁] [Fintype S₂] (A : TwoRound X)
    (g g' : S₁ → S₂ → X → ℝ) (v : S₁ → X → ℝ) (W₁ W₂ : S₁ → S₂ → Set X)
    (hW₁ : ∀ s₁ s₂, ∀ x ∈ W₁ s₁ s₂, g s₁ s₂ x = v s₁ x ∧ g' s₁ s₂ x = v s₁ x)
    (hW₂ : ∀ s₁ s₂, ∀ x ∈ W₂ s₁ s₂, g s₁ s₂ x = g' s₁ s₂ x)
    {p₁ p₂ : ℝ}
    (h₁ : ∀ x, (#{s : S₁ × S₂ | x ∉ W₁ s.1 s.2} : ℝ) ≤ p₁ * (Fintype.card S₁ * Fintype.card S₂))
    (h₂ : ∀ x s₁, (#{s₂ : S₂ | x ∉ W₂ s₁ s₂} : ℝ) ≤ p₂ * Fintype.card S₂) :
    (#{s : S₁ × S₂ | A.output (g s.1 s.2) ≠ A.output (g' s.1 s.2)} : ℝ)
      ≤ #A.first * (p₁ * (Fintype.card S₁ * Fintype.card S₂))
        + (∑ s₁ : S₁, (#(A.second (v s₁)) : ℝ)) * (p₂ * Fintype.card S₂) := by
  set bad₁ : Finset (S₁ × S₂) := A.first.biUnion fun x => {s : S₁ × S₂ | x ∉ W₁ s.1 s.2} with hbad₁
  set bad₂ : Finset (S₁ × S₂) :=
    (univ : Finset S₁).biUnion fun s₁ =>
      ((A.second (v s₁)).biUnion fun x => ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)).map
        ⟨fun s₂ => (s₁, s₂), fun a b h => by simpa using h⟩ with hbad₂
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
  have hc₂ : (#bad₂ : ℝ) ≤ (∑ s₁ : S₁, (#(A.second (v s₁)) : ℝ)) * (p₂ * Fintype.card S₂) := by
    have hinner : ∀ s₁ : S₁,
        (#((A.second (v s₁)).biUnion fun x => ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)) : ℝ)
          ≤ #(A.second (v s₁)) * (p₂ * Fintype.card S₂) := by
      intro s₁
      calc (#((A.second (v s₁)).biUnion fun x => ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)) : ℝ)
          ≤ ∑ x ∈ A.second (v s₁), (#({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂) : ℝ) := by
            exact_mod_cast card_biUnion_le
        _ ≤ ∑ _x ∈ A.second (v s₁), p₂ * Fintype.card S₂ := sum_le_sum fun x _ => h₂ x s₁
        _ = #(A.second (v s₁)) * (p₂ * Fintype.card S₂) := by rw [sum_const, nsmul_eq_mul]
    calc (#bad₂ : ℝ) ≤ ∑ s₁ : S₁, (#(((A.second (v s₁)).biUnion fun x =>
            ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)).map
              ⟨fun s₂ => (s₁, s₂), fun a b h => by simpa using h⟩) : ℝ) := by
          exact_mod_cast card_biUnion_le
      _ = ∑ s₁ : S₁, (#((A.second (v s₁)).biUnion fun x =>
            ({s₂ : S₂ | x ∉ W₂ s₁ s₂} : Finset S₂)) : ℝ) := by
          simp only [card_map]
      _ ≤ ∑ s₁ : S₁, (#(A.second (v s₁)) : ℝ) * (p₂ * Fintype.card S₂) :=
          sum_le_sum fun s₁ _ => hinner s₁
      _ = (∑ s₁ : S₁, (#(A.second (v s₁)) : ℝ)) * (p₂ * Fintype.card S₂) := by rw [sum_mul]
  calc (#{s : S₁ × S₂ | A.output (g s.1 s.2) ≠ A.output (g' s.1 s.2)} : ℝ)
      ≤ #(bad₁ ∪ bad₂) := by exact_mod_cast card_le_card hsub
    _ ≤ #bad₁ + #bad₂ := by exact_mod_cast card_union_le _ _
    _ ≤ #A.first * (p₁ * (Fintype.card S₁ * Fintype.card S₂))
          + (∑ s₁ : S₁, (#(A.second (v s₁)) : ℝ)) * (p₂ * Fintype.card S₂) := add_le_add hc₁ hc₂

open scoped Classical in
/-- **Two rounds, expected batch sizes.**  A randomised two-round algorithm that is
`(ε/2, δ)`-correct on a class `G` containing the twins satisfies
`1 − 2δ ≤ E|B₁| · p₁ + E_{ω, s₁}|B₂(v s₁)| · p₂`:
the first expectation is over the coins, the second over the coins and a uniformly random first
hidden parameter, of the size of the second batch *when the algorithm is run on the virtual
residual `v s₁`*.  No bound on batch sizes is assumed. -/
theorem two_round_expected_bound {S₁ S₂ Ω : Type*} [Fintype S₁] [Fintype S₂] [Nonempty S₁]
    [Nonempty S₂] [Fintype Ω] {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (alg : Ω → TwoRound X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ f, G f →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output f - Φ f| ≤ ε / 2), P ω)
    (g g' : S₁ → S₂ → X → ℝ) (v : S₁ → X → ℝ) (W₁ W₂ : S₁ → S₂ → Set X)
    (hg : ∀ s₁ s₂, G (g s₁ s₂)) (hg' : ∀ s₁ s₂, G (g' s₁ s₂))
    (hsens : ∀ s₁ s₂, ε < |Φ (g s₁ s₂) - Φ (g' s₁ s₂)|)
    (hW₁ : ∀ s₁ s₂, ∀ x ∈ W₁ s₁ s₂, g s₁ s₂ x = v s₁ x ∧ g' s₁ s₂ x = v s₁ x)
    (hW₂ : ∀ s₁ s₂, ∀ x ∈ W₂ s₁ s₂, g s₁ s₂ x = g' s₁ s₂ x)
    {p₁ p₂ : ℝ}
    (h₁ : ∀ x, (#{s : S₁ × S₂ | x ∉ W₁ s.1 s.2} : ℝ) ≤ p₁ * (Fintype.card S₁ * Fintype.card S₂))
    (h₂ : ∀ x s₁, (#{s₂ : S₂ | x ∉ W₂ s₁ s₂} : ℝ) ≤ p₂ * Fintype.card S₂) :
    1 - 2 * δ ≤ (∑ ω, P ω * (#(alg ω).first : ℝ)) * p₁
      + (∑ ω, P ω * ((∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) / Fintype.card S₁)) * p₂ := by
  have h1 : (0 : ℝ) < Fintype.card S₁ := by exact_mod_cast Fintype.card_pos
  have h2 : (0 : ℝ) < Fintype.card S₂ := by exact_mod_cast Fintype.card_pos
  set c₁ : ℝ := (Fintype.card S₁ : ℝ) with hc₁
  set c₂ : ℝ := (Fintype.card S₂ : ℝ) with hc₂
  have hNpos : 0 < c₁ * c₂ := mul_pos h1 h2
  have hdet : ∀ s : S₁ × S₂, 1 - 2 * δ ≤
      ∑ ω ∈ univ.filter (fun ω => (alg ω).output (g s.1 s.2) ≠ (alg ω).output (g' s.1 s.2)), P ω :=
    fun s => prob_output_ne_ge (fun ω => (alg ω).output) P hP hP1
      (hcorr _ (hg s.1 s.2)) (hcorr _ (hg' s.1 s.2)) (hsens s.1 s.2)
  have hrun : ∀ ω, (#{s : S₁ × S₂ | (alg ω).output (g s.1 s.2) ≠ (alg ω).output (g' s.1 s.2)} : ℝ)
      ≤ #(alg ω).first * (p₁ * (c₁ * c₂))
        + (∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) * (p₂ * c₂) :=
    fun ω => card_distinguished_le_sum (alg ω) g g' v W₁ W₂ hW₁ hW₂ h₁ h₂
  have hcard : (Fintype.card (S₁ × S₂) : ℝ) = c₁ * c₂ := by
    rw [Fintype.card_prod]; push_cast; rfl
  have key : (c₁ * c₂) * (1 - 2 * δ) ≤ ∑ ω, P ω * (#(alg ω).first * (p₁ * (c₁ * c₂))
        + (∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) * (p₂ * c₂)) := by
    calc (c₁ * c₂) * (1 - 2 * δ) = ∑ _s : S₁ × S₂, (1 - 2 * δ) := by
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
      _ ≤ ∑ ω, P ω * (#(alg ω).first * (p₁ * (c₁ * c₂))
            + (∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) * (p₂ * c₂)) :=
          sum_le_sum fun ω _ => mul_le_mul_of_nonneg_left (hrun ω) (hP ω)
  have hrew : ∑ ω, P ω * (#(alg ω).first * (p₁ * (c₁ * c₂))
        + (∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) * (p₂ * c₂))
      = (c₁ * c₂) * ((∑ ω, P ω * (#(alg ω).first : ℝ)) * p₁
        + (∑ ω, P ω * ((∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) / c₁)) * p₂) := by
    rw [mul_add, sum_mul, sum_mul, mul_sum, mul_sum, ← sum_add_distrib]
    refine sum_congr rfl fun ω _ => ?_
    field_simp
  rw [hrew] at key
  exact le_of_mul_le_mul_left key hNpos

open scoped Classical in
/-- **Two rounds: expected cost at the virtual instances.**  If a point is outside `W₁` for at
most a fraction `p` of the pairs and outside `W₂` for at most a fraction `p` of the `s₂`, then
`1 − 2δ ≤ p · E_{ω, s₁}[ |B₁| + |B₂(v s₁)| ]`: the expected number of evaluations of a correct
randomised two-round algorithm *on the instance `v s₁`*, averaged over `s₁`, is at least
`(1 − 2δ)/p`. -/
theorem two_round_expected_cost {S₁ S₂ Ω : Type*} [Fintype S₁] [Fintype S₂] [Nonempty S₁]
    [Nonempty S₂] [Fintype Ω] {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (alg : Ω → TwoRound X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ f, G f →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output f - Φ f| ≤ ε / 2), P ω)
    (g g' : S₁ → S₂ → X → ℝ) (v : S₁ → X → ℝ) (W₁ W₂ : S₁ → S₂ → Set X)
    (hg : ∀ s₁ s₂, G (g s₁ s₂)) (hg' : ∀ s₁ s₂, G (g' s₁ s₂))
    (hsens : ∀ s₁ s₂, ε < |Φ (g s₁ s₂) - Φ (g' s₁ s₂)|)
    (hW₁ : ∀ s₁ s₂, ∀ x ∈ W₁ s₁ s₂, g s₁ s₂ x = v s₁ x ∧ g' s₁ s₂ x = v s₁ x)
    (hW₂ : ∀ s₁ s₂, ∀ x ∈ W₂ s₁ s₂, g s₁ s₂ x = g' s₁ s₂ x)
    {p : ℝ}
    (h₁ : ∀ x, (#{s : S₁ × S₂ | x ∉ W₁ s.1 s.2} : ℝ) ≤ p * (Fintype.card S₁ * Fintype.card S₂))
    (h₂ : ∀ x s₁, (#{s₂ : S₂ | x ∉ W₂ s₁ s₂} : ℝ) ≤ p * Fintype.card S₂) :
    1 - 2 * δ ≤ p * ∑ ω, P ω * ((∑ s₁ : S₁,
        ((#(alg ω).first : ℝ) + #((alg ω).second (v s₁)))) / Fintype.card S₁) := by
  have h1 : (0 : ℝ) < Fintype.card S₁ := by exact_mod_cast Fintype.card_pos
  have hmain := two_round_expected_bound alg P hP hP1 hcorr g g' v W₁ W₂ hg hg' hsens hW₁ hW₂ h₁ h₂
  have hsplit : ∀ ω, (∑ s₁ : S₁, ((#(alg ω).first : ℝ) + #((alg ω).second (v s₁))))
      / Fintype.card S₁
      = (#(alg ω).first : ℝ) + (∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) / Fintype.card S₁ := by
    intro ω
    rw [sum_add_distrib, sum_const, card_univ, nsmul_eq_mul, add_div]
    congr 1
    field_simp
  calc 1 - 2 * δ ≤ (∑ ω, P ω * (#(alg ω).first : ℝ)) * p
        + (∑ ω, P ω * ((∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) / Fintype.card S₁)) * p := hmain
    _ = p * ∑ ω, P ω * ((∑ s₁ : S₁,
          ((#(alg ω).first : ℝ) + #((alg ω).second (v s₁)))) / Fintype.card S₁) := by
        rw [← add_mul, ← sum_add_distrib, mul_comm]
        congr 1
        refine sum_congr rfl fun ω _ => ?_
        rw [hsplit ω]
        ring

open scoped Classical in
/-- **Two rounds: the worst-case bound with batch sizes bounded on the class only.**  The form in
which Lemma 11.85 is applied: the second batch need only be bounded when the algorithm runs on
members of the class `G`, provided the virtual residuals `v s₁` are members. -/
theorem two_round_bound_of_class {S₁ S₂ Ω : Type*} [Fintype S₁] [Fintype S₂] [Nonempty S₁]
    [Nonempty S₂] [Fintype Ω] {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (alg : Ω → TwoRound X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ f, G f →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output f - Φ f| ≤ ε / 2), P ω)
    (g g' : S₁ → S₂ → X → ℝ) (v : S₁ → X → ℝ) (W₁ W₂ : S₁ → S₂ → Set X)
    (hg : ∀ s₁ s₂, G (g s₁ s₂)) (hg' : ∀ s₁ s₂, G (g' s₁ s₂)) (hv : ∀ s₁, G (v s₁))
    (hsens : ∀ s₁ s₂, ε < |Φ (g s₁ s₂) - Φ (g' s₁ s₂)|)
    (hW₁ : ∀ s₁ s₂, ∀ x ∈ W₁ s₁ s₂, g s₁ s₂ x = v s₁ x ∧ g' s₁ s₂ x = v s₁ x)
    (hW₂ : ∀ s₁ s₂, ∀ x ∈ W₂ s₁ s₂, g s₁ s₂ x = g' s₁ s₂ x)
    {p₁ p₂ M₁ M₂ : ℝ} (hp₁ : 0 ≤ p₁) (hp₂ : 0 ≤ p₂)
    (h₁ : ∀ x, (#{s : S₁ × S₂ | x ∉ W₁ s.1 s.2} : ℝ) ≤ p₁ * (Fintype.card S₁ * Fintype.card S₂))
    (h₂ : ∀ x s₁, (#{s₂ : S₂ | x ∉ W₂ s₁ s₂} : ℝ) ≤ p₂ * Fintype.card S₂)
    (hM₁ : ∀ ω, (#(alg ω).first : ℝ) ≤ M₁)
    (hM₂ : ∀ ω f, G f → (#((alg ω).second f) : ℝ) ≤ M₂) :
    1 - 2 * δ ≤ M₁ * p₁ + M₂ * p₂ := by
  have h1 : (0 : ℝ) < Fintype.card S₁ := by exact_mod_cast Fintype.card_pos
  have hmain := two_round_expected_bound alg P hP hP1 hcorr g g' v W₁ W₂ hg hg' hsens hW₁ hW₂ h₁ h₂
  have hA : ∑ ω, P ω * (#(alg ω).first : ℝ) ≤ M₁ := by
    calc ∑ ω, P ω * (#(alg ω).first : ℝ) ≤ ∑ ω, P ω * M₁ :=
          sum_le_sum fun ω _ => mul_le_mul_of_nonneg_left (hM₁ ω) (hP ω)
      _ = M₁ := by rw [← sum_mul, hP1, one_mul]
  have hB : ∑ ω, P ω * ((∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) / Fintype.card S₁) ≤ M₂ := by
    have hav : ∀ ω, (∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) / Fintype.card S₁ ≤ M₂ := by
      intro ω
      rw [div_le_iff₀ h1]
      calc ∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ) ≤ ∑ _s₁ : S₁, M₂ :=
            sum_le_sum fun s₁ _ => hM₂ ω (v s₁) (hv s₁)
        _ = M₂ * Fintype.card S₁ := by rw [sum_const, card_univ, nsmul_eq_mul, mul_comm]
    calc ∑ ω, P ω * ((∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) / Fintype.card S₁)
        ≤ ∑ ω, P ω * M₂ := sum_le_sum fun ω _ => mul_le_mul_of_nonneg_left (hav ω) (hP ω)
      _ = M₂ := by rw [← sum_mul, hP1, one_mul]
  calc 1 - 2 * δ ≤ (∑ ω, P ω * (#(alg ω).first : ℝ)) * p₁
        + (∑ ω, P ω * ((∑ s₁ : S₁, (#((alg ω).second (v s₁)) : ℝ)) / Fintype.card S₁)) * p₂ := hmain
    _ ≤ M₁ * p₁ + M₂ * p₂ :=
        add_le_add (mul_le_mul_of_nonneg_right hA hp₁) (mul_le_mul_of_nonneg_right hB hp₂)

end MetricChain.TwoRounds.R4

-- R9: appended to the scratch copy only
#print axioms MetricChain.TwoRounds.R4.card_distinguished_le_sum
#print axioms MetricChain.TwoRounds.R4.two_round_expected_bound
#print axioms MetricChain.TwoRounds.R4.two_round_expected_cost
#print axioms MetricChain.TwoRounds.R4.two_round_bound_of_class
