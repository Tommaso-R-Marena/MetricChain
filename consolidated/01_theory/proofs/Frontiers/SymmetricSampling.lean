import proofs.Frontiers.NonAdaptive
import proofs.Frontiers.TypeQuantiles

/-!
# Non-adaptive sampling for permutation-invariant problems

Theory report §11.20, Theorem 11.61(b)(i), in the generality in which its proof works: the
reference measure enters only through the permutation invariance of the target.

* `exists_perm_smul_eq`: permutations of the coordinates act transitively on the
  configurations of a given type (from Mathlib's `Set.powersetCard.isPretransitive`).
* `card_perm_smul_mem_mul`: a uniformly random permutation sends a configuration of type
  `k` to a uniformly random configuration of type `k` — as a counting identity.
* `symmetric_nonadaptive_queries_ge`: if the class `G` and the target `Φ` are invariant under
  permutations and two class members, whose targets differ by more than `ε`, differ in
  every type class on a set of density at most `q`, then every non-adaptive randomised
  algorithm that is `(ε/2, δ)`-correct on the class makes at least `(1 − 2δ)/q` evaluations
  in expectation (from `nonadaptive_expected_queries_ge` with the pairs permuted by all
  permutations).
* `truncated_weight_queries_ge`: the instance used in the theory — a weight against its
  truncation at type-wise admissible thresholds (`TypeQuantiles.lean`).
* `symmetric_nonadaptive_witness`: a concrete instance — summing an arbitrary function over
  the cube to within `1/4` needs `(1 − 2δ)·C(n, k)` non-adaptive evaluations for every `k`.
* `symmetric_queries_ge`: the same for **every** algorithm, adaptive or not, at an instance
  that is itself permutation-invariant (a function of the type): if a class member whose
  target differs by more than `ε` differs from it on density at most `q` in every type
  class, then `(1 − 2δ)/q` evaluations are needed at that instance (from
  `expected_queries_ge_packing` with the alternative permuted by all permutations);
  `perm_fraction_le` is the counting step, `symmetric_queries_witness` a concrete instance.

Together with `TypeQuantiles.truncate_lipschitz_insert`/`_erase` (the truncation stays in the
Lipschitz class) this is the every-`n` lower bound behind "a sample that is uniform on
every type class is optimal among non-adaptive samples" for **every** known part that is a
function of the type.  The matching upper bound (stratified sampling: Chernoff and Markov)
and all exponents are paper proofs.
-/

namespace MetricChain.SymmetricSampling

open Finset Equiv
open scoped Pointwise

variable {α : Type*} [Fintype α] [DecidableEq α]

omit [Fintype α] in
/-- Permutations act transitively on the configurations of a given type. -/
theorem exists_perm_smul_eq {a b : Finset α} (h : #a = #b) : ∃ τ : Perm α, τ • a = b := by
  haveI := Set.powersetCard.isPretransitive (α := α) (n := #a)
  have ha : a ∈ Set.powersetCard α #a := by simp [Set.powersetCard]
  have hb : b ∈ Set.powersetCard α #a := by simp [Set.powersetCard, h]
  obtain ⟨τ, hτ⟩ := MulAction.exists_smul_eq (Perm α)
    (⟨a, ha⟩ : Set.powersetCard α #a) ⟨b, hb⟩
  exact ⟨τ, by simpa using congrArg Subtype.val hτ⟩

/-- **Counting.**  For a configuration `a` of type `k` and a family `𝒟` of configurations of
type `k`, the number of permutations that send `a` into `𝒟`, times `C(n, k)`, is `#𝒟 · n!`:
a uniformly random permutation sends `a` to a uniformly random configuration of its type. -/
theorem card_perm_smul_mem_mul (a : Finset α) (𝒟 : Finset (Finset α)) (h𝒟 : ∀ t ∈ 𝒟, #t = #a) :
    #{σ : Perm α | σ • a ∈ 𝒟} * (Fintype.card α).choose #a
      = #𝒟 * (Fintype.card α).factorial := by
  have hA : ∀ b : Finset α, #b = #a →
      #{σ : Perm α | σ • b ∈ 𝒟} = #{σ : Perm α | σ • a ∈ 𝒟} := by
    intro b hb
    obtain ⟨τ, rfl⟩ := exists_perm_smul_eq (a := a) (b := b) hb.symm
    refine Finset.card_bij (fun σ _ => σ * τ) ?_ ?_ ?_
    · intro σ hσ
      simp only [mem_filter, mem_univ, true_and] at hσ ⊢
      rwa [mul_smul]
    · intro σ₁ _ σ₂ _ h
      exact mul_right_cancel h
    · intro σ' hσ'
      refine ⟨σ' * τ⁻¹, ?_, by simp⟩
      simp only [mem_filter, mem_univ, true_and] at hσ' ⊢
      rw [← mul_smul]
      simpa using hσ'
  have hB : ∑ b ∈ powersetCard #a (univ : Finset α), #{σ : Perm α | σ • b ∈ 𝒟}
      = ∑ σ : Perm α, #{b ∈ powersetCard #a (univ : Finset α) | σ • b ∈ 𝒟} := by
    simp_rw [card_filter]
    exact Finset.sum_comm
  have hC : ∀ σ : Perm α, #{b ∈ powersetCard #a (univ : Finset α) | σ • b ∈ 𝒟} = #𝒟 := by
    intro σ
    refine Finset.card_bij (fun b _ => σ • b) ?_ ?_ ?_
    · intro b hb
      exact (mem_filter.mp hb).2
    · intro b₁ _ b₂ _ h
      exact smul_left_cancel σ h
    · intro t ht
      refine ⟨σ⁻¹ • t, ?_, by simp⟩
      rw [mem_filter, mem_powersetCard]
      refine ⟨⟨subset_univ _, ?_⟩, by simpa using ht⟩
      rw [card_smul_finset]
      exact h𝒟 t ht
  calc #{σ : Perm α | σ • a ∈ 𝒟} * (Fintype.card α).choose #a
      = ∑ _b ∈ powersetCard #a (univ : Finset α), #{σ : Perm α | σ • a ∈ 𝒟} := by
        rw [sum_const, card_powersetCard, card_univ, smul_eq_mul, mul_comm]
    _ = ∑ b ∈ powersetCard #a (univ : Finset α), #{σ : Perm α | σ • b ∈ 𝒟} :=
        (sum_congr rfl fun b hb => (hA b (mem_powersetCard.mp hb).2).symm)
    _ = ∑ _σ : Perm α, #𝒟 := by rw [hB]; exact sum_congr rfl fun σ _ => hC σ
    _ = #𝒟 * (Fintype.card α).factorial := by
        rw [sum_const, card_univ, Fintype.card_perm, smul_eq_mul, mul_comm]

open Classical in
/-- **Non-adaptive lower bound for permutation-invariant problems** (theory report, Theorem
11.61(b)(i), for every reference measure that is uniform on type classes).  Let the class
`G` and the target `Φ` be invariant under permutations of the coordinates, and let `ψ`, `ψ'`
be two class members whose targets differ by more than `ε` and which differ, in every type
class, on a set of density at most `q`.  Then every non-adaptive randomised algorithm that
is `(ε/2, δ)`-correct on the class makes at least `(1 − 2δ)/q` evaluations in expectation. -/
theorem symmetric_nonadaptive_queries_ge {Ω : Type*} [Fintype Ω]
    {G : (Finset α → ℝ) → Prop} {Φ : (Finset α → ℝ) → ℝ}
    (alg : Ω → QueryAlgorithm (Finset α)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    (Q : Ω → Finset (Finset α)) (hna : ∀ ω g, (alg ω).queries g = Q ω)
    (hGperm : ∀ (σ : Perm α) g, G g → G (fun s => g (σ • s)))
    (hΦperm : ∀ (σ : Perm α) g, Φ (fun s => g (σ • s)) = Φ g)
    {ψ ψ' : Finset α → ℝ} (hψ : G ψ) (hψ' : G ψ') (hsens : ε < |Φ ψ' - Φ ψ|) {q : ℝ}
    (hdens : ∀ r : ℕ, (#{s ∈ powersetCard r (univ : Finset α) | ψ' s ≠ ψ s} : ℝ)
      ≤ q * (Fintype.card α).choose r) :
    1 - 2 * δ ≤ (∑ ω, P ω * (Q ω).card) * q := by
  have hfact : (0 : ℝ) < (Fintype.card α).factorial := by exact_mod_cast Nat.factorial_pos _
  have hcap : ∀ a : Finset α,
      ∑ σ ∈ univ.filter (fun σ : Perm α => ψ' (σ • a) ≠ ψ (σ • a)),
        (1 / ((Fintype.card α).factorial : ℝ)) ≤ q := by
    intro a
    rw [sum_const, nsmul_eq_mul]
    set 𝒟 : Finset (Finset α) := {s ∈ powersetCard #a (univ : Finset α) | ψ' s ≠ ψ s} with h𝒟def
    have hset : (univ.filter fun σ : Perm α => ψ' (σ • a) ≠ ψ (σ • a))
        = (univ.filter fun σ : Perm α => σ • a ∈ 𝒟) := by
      ext σ
      simp only [mem_filter, mem_univ, true_and, h𝒟def, mem_powersetCard, subset_univ,
        card_smul_finset]
    rw [hset]
    have hcount := card_perm_smul_mem_mul a 𝒟
      (fun t ht => (mem_powersetCard.mp (mem_filter.mp ht).1).2)
    have hC : (0 : ℝ) < (Fintype.card α).choose #a := by
      exact_mod_cast Nat.choose_pos (card_le_univ a)
    have hcountR : (#{σ : Perm α | σ • a ∈ 𝒟} : ℝ) * (Fintype.card α).choose #a
        = #𝒟 * (Fintype.card α).factorial := by exact_mod_cast hcount
    have hd : (#𝒟 : ℝ) ≤ q * (Fintype.card α).choose #a := hdens #a
    rw [mul_one_div, div_le_iff₀ hfact]
    have hmul : (#{σ : Perm α | σ • a ∈ 𝒟} : ℝ) * (Fintype.card α).choose #a
        ≤ q * (Fintype.card α).factorial * (Fintype.card α).choose #a := by
      rw [hcountR]
      nlinarith [mul_le_mul_of_nonneg_right hd hfact.le]
    exact le_of_mul_le_mul_right hmul hC
  have key := nonadaptive_expected_queries_ge (ι := Perm α) alg P hP hP1 hcorr Q hna
    (fun σ s => ψ (σ • s)) (fun σ s => ψ' (σ • s)) (fun σ => hGperm σ ψ hψ)
    (fun σ => hGperm σ ψ' hψ') (fun σ => by rw [hΦperm σ ψ', hΦperm σ ψ]; exact hsens)
    (fun _ => 1 / ((Fintype.card α).factorial : ℝ)) (fun _ => by positivity) hcap
  have hsum : ∑ _σ : Perm α, (1 / ((Fintype.card α).factorial : ℝ)) = 1 := by
    rw [sum_const, card_univ, Fintype.card_perm, nsmul_eq_mul]
    field_simp
  rwa [hsum, mul_one] at key

open Classical in
/-- **A weight against its type-wise truncation.**  If the class of weights and the target
are permutation-invariant, `w` and its truncation at thresholds that are admissible for
the density `q` in every type class both belong to the class, and their targets differ by
more than `ε`, then a non-adaptive algorithm needs at least `(1 − 2δ)/q` evaluations. -/
theorem truncated_weight_queries_ge {Ω : Type*} [Fintype Ω]
    {G : (Finset α → ℝ) → Prop} {Φ : (Finset α → ℝ) → ℝ}
    (alg : Ω → QueryAlgorithm (Finset α)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    (Q : Ω → Finset (Finset α)) (hna : ∀ ω g, (alg ω).queries g = Q ω)
    (hGperm : ∀ (σ : Perm α) g, G g → G (fun s => g (σ • s)))
    (hΦperm : ∀ (σ : Perm α) g, Φ (fun s => g (σ • s)) = Φ g)
    {w : Finset α → ℝ} {thr : ℕ → ℝ} (hw : G w) (hw' : G (TypeQuantiles.truncate w thr))
    (hsens : ε < |Φ (TypeQuantiles.truncate w thr) - Φ w|) {q : ℝ}
    (hadm : ∀ r, r ≤ Fintype.card α → TypeQuantiles.Admissible w q r (thr r)) :
    1 - 2 * δ ≤ (∑ ω, P ω * (Q ω).card) * q := by
  refine symmetric_nonadaptive_queries_ge alg P hP hP1 hcorr Q hna hGperm hΦperm hw hw' hsens ?_
  intro r
  rcases Nat.lt_or_ge (Fintype.card α) r with hr | hr
  · have hempty : powersetCard r (univ : Finset α) = ∅ :=
      powersetCard_eq_empty.mpr (by rwa [card_univ])
    rw [hempty, Nat.choose_eq_zero_of_lt hr]
    simp
  · have hC : (0 : ℝ) < (Fintype.card α).choose r := by exact_mod_cast Nat.choose_pos hr
    have hsub : {s ∈ powersetCard r (univ : Finset α) | TypeQuantiles.truncate w thr s ≠ w s}
        ⊆ TypeQuantiles.upperSet w (thr r) r := by
      intro s hs
      obtain ⟨hs1, hs2⟩ := mem_filter.mp hs
      have hcard : #s = r := (mem_powersetCard.mp hs1).2
      have := TypeQuantiles.truncate_ne_iff.mp hs2
      rwa [hcard] at this
    have h1 : (#{s ∈ powersetCard r (univ : Finset α) | TypeQuantiles.truncate w thr s ≠ w s} : ℝ)
        ≤ #(TypeQuantiles.upperSet w (thr r) r) := by exact_mod_cast card_le_card hsub
    have h2 := hadm r hr
    unfold TypeQuantiles.Admissible TypeQuantiles.upperDensity at h2
    rw [div_le_iff₀ hC] at h2
    exact h1.trans h2

open Classical in
/-- **Witness for `symmetric_nonadaptive_queries_ge`.**  Class: all functions on the
configurations; target: the sum of all values (invariant under permutations of the
coordinates); pair: the zero function and the indicator of one configuration `a`, which
differ on a set of density `1 / C(n, #a)` in the type class of `a` and nowhere else.  Hence
every non-adaptive randomised algorithm that computes the sum of an arbitrary function to
within `1/4` with probability `1 − δ` evaluates at least `(1 − 2δ)·C(n, #a)` points in
expectation, for every configuration `a`. -/
theorem symmetric_nonadaptive_witness {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Finset α)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {δ : ℝ}
    (hcorr : ∀ g : Finset α → ℝ, True →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - ∑ s, g s| ≤ (1 / 2 : ℝ) / 2), P ω)
    (Q : Ω → Finset (Finset α)) (hna : ∀ ω g, (alg ω).queries g = Q ω) (a : Finset α) :
    1 - 2 * δ ≤ (∑ ω, P ω * (Q ω).card) * (1 / ((Fintype.card α).choose #a : ℝ)) := by
  have hC : (0 : ℝ) < (Fintype.card α).choose #a := by
    exact_mod_cast Nat.choose_pos (card_le_univ a)
  refine symmetric_nonadaptive_queries_ge (G := fun _ => True) (Φ := fun g => ∑ s, g s)
    alg P hP hP1 hcorr Q hna (fun _ _ _ => trivial) (fun σ g => ?_)
    (ψ := fun _ => 0) (ψ' := fun s => if s = a then 1 else 0) trivial trivial ?_ ?_
  · exact Fintype.sum_equiv (MulAction.toPerm σ) _ _ (fun s => rfl)
  · simp
    norm_num
  · intro r
    have hsub : {s ∈ powersetCard r (univ : Finset α) | (if s = a then (1 : ℝ) else 0) ≠ 0}
        ⊆ {a} := by
      intro s hs
      have h2 := (mem_filter.mp hs).2
      by_contra hne
      rw [mem_singleton] at hne
      simp [hne] at h2
    have hcard : (#{s ∈ powersetCard r (univ : Finset α) | (if s = a then (1 : ℝ) else 0) ≠ 0} : ℝ)
        ≤ 1 := by
      exact_mod_cast (card_le_card hsub).trans (card_singleton a).le
    rcases eq_or_ne r #a with rfl | hr
    · rw [one_div, inv_mul_cancel₀ hC.ne']
      exact hcard
    · have hempty : {s ∈ powersetCard r (univ : Finset α) | (if s = a then (1 : ℝ) else 0) ≠ 0}
          = ∅ := by
        refine eq_empty_of_forall_notMem fun s hs => ?_
        obtain ⟨h1, h2⟩ := mem_filter.mp hs
        have hsa : s = a := by
          by_contra hne
          simp [hne] at h2
        exact hr (hsa ▸ (mem_powersetCard.mp h1).2).symm
      rw [hempty]
      simp only [card_empty, Nat.cast_zero]
      positivity

open Classical in
/-- If two functions differ on density at most `q` in every type class, then for every
configuration `a` the fraction of permutations `σ` with `ψ' (σ • a) ≠ ψ (σ • a)` is at
most `q`. -/
theorem perm_fraction_le {ψ ψ' : Finset α → ℝ} {q : ℝ}
    (hdens : ∀ r : ℕ, (#{s ∈ powersetCard r (univ : Finset α) | ψ' s ≠ ψ s} : ℝ)
      ≤ q * (Fintype.card α).choose r) (a : Finset α) :
    (#{σ : Perm α | ψ' (σ • a) ≠ ψ (σ • a)} : ℝ) * (1 / ((Fintype.card α).factorial : ℝ)) ≤ q := by
  have hfact : (0 : ℝ) < (Fintype.card α).factorial := by exact_mod_cast Nat.factorial_pos _
  set 𝒟 : Finset (Finset α) := {s ∈ powersetCard #a (univ : Finset α) | ψ' s ≠ ψ s} with h𝒟def
  have hset : (univ.filter fun σ : Perm α => ψ' (σ • a) ≠ ψ (σ • a))
      = (univ.filter fun σ : Perm α => σ • a ∈ 𝒟) := by
    ext σ
    simp only [mem_filter, mem_univ, true_and, h𝒟def, mem_powersetCard, subset_univ,
      card_smul_finset]
  rw [hset]
  have hcount := card_perm_smul_mem_mul a 𝒟
    (fun t ht => (mem_powersetCard.mp (mem_filter.mp ht).1).2)
  have hC : (0 : ℝ) < (Fintype.card α).choose #a := by
    exact_mod_cast Nat.choose_pos (card_le_univ a)
  have hcountR : (#{σ : Perm α | σ • a ∈ 𝒟} : ℝ) * (Fintype.card α).choose #a
      = #𝒟 * (Fintype.card α).factorial := by exact_mod_cast hcount
  have hd : (#𝒟 : ℝ) ≤ q * (Fintype.card α).choose #a := hdens #a
  rw [mul_one_div, div_le_iff₀ hfact]
  have hmul : (#{σ : Perm α | σ • a ∈ 𝒟} : ℝ) * (Fintype.card α).choose #a
      ≤ q * (Fintype.card α).factorial * (Fintype.card α).choose #a := by
    rw [hcountR]
    nlinarith [mul_le_mul_of_nonneg_right hd hfact.le]
  exact le_of_mul_le_mul_right hmul hC

open Classical in
/-- **Lower bound for every algorithm at a permutation-invariant instance.**  Let the class
`G` and the target `Φ` be invariant under permutations of the coordinates, let `g` be a
class member that is itself invariant (a function of the type), and let `ψ'` be a class
member whose target differs from that of `g` by more than `ε` and which differs from `g`,
in every type class, on a set of density at most `q`.  Then every randomised algorithm —
adaptive or not — that is `(ε/2, δ)`-correct on the class makes at least `(1 − 2δ)/q`
evaluations in expectation **at `g`**. -/
theorem symmetric_queries_ge {Ω : Type*} [Fintype Ω]
    {G : (Finset α → ℝ) → Prop} {Φ : (Finset α → ℝ) → ℝ}
    (alg : Ω → QueryAlgorithm (Finset α)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    (hGperm : ∀ (σ : Perm α) g, G g → G (fun s => g (σ • s)))
    (hΦperm : ∀ (σ : Perm α) g, Φ (fun s => g (σ • s)) = Φ g)
    {g ψ' : Finset α → ℝ} (hg : G g) (hginv : ∀ (σ : Perm α) s, g (σ • s) = g s)
    (hψ' : G ψ') (hsens : ε < |Φ ψ' - Φ g|) {q : ℝ}
    (hdens : ∀ r : ℕ, (#{s ∈ powersetCard r (univ : Finset α) | ψ' s ≠ g s} : ℝ)
      ≤ q * (Fintype.card α).choose r) :
    1 - 2 * δ ≤ (∑ ω, P ω * ((alg ω).queries g).card) * q := by
  have hfact : (0 : ℝ) < (Fintype.card α).factorial := by exact_mod_cast Nat.factorial_pos _
  have hcap : ∀ a : Finset α,
      ∑ σ ∈ univ.filter (fun σ : Perm α => ψ' (σ • a) ≠ g a),
        (1 / ((Fintype.card α).factorial : ℝ)) ≤ q := by
    intro a
    rw [sum_const, nsmul_eq_mul]
    have hset : (univ.filter fun σ : Perm α => ψ' (σ • a) ≠ g a)
        = (univ.filter fun σ : Perm α => ψ' (σ • a) ≠ g (σ • a)) := by
      ext σ
      simp only [mem_filter, mem_univ, true_and, hginv σ a]
    rw [hset]
    exact perm_fraction_le hdens a
  have key := expected_queries_ge_packing (ι := Perm α) alg P hP hP1 hcorr hg
    (fun σ s => ψ' (σ • s)) (fun σ => hGperm σ ψ' hψ')
    (fun σ => by rw [hΦperm σ ψ']; exact hsens)
    (fun _ => 1 / ((Fintype.card α).factorial : ℝ)) (fun _ => by positivity) hcap
  have hsum : ∑ _σ : Perm α, (1 / ((Fintype.card α).factorial : ℝ)) = 1 := by
    rw [sum_const, card_univ, Fintype.card_perm, nsmul_eq_mul]
    field_simp
  rwa [hsum, mul_one] at key

open Classical in
/-- **Witness for `symmetric_queries_ge`.**  Class: all functions; target: the sum of all
values; instance: the zero function (invariant); alternative: the indicator of one
configuration `a`.  Hence every randomised algorithm, adaptive or not, that computes the
sum of an arbitrary function to within `1/4` with probability `1 − δ` evaluates the zero
function at at least `(1 − 2δ)·C(n, #a)` points in expectation. -/
theorem symmetric_queries_witness {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Finset α)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {δ : ℝ}
    (hcorr : ∀ g : Finset α → ℝ, True →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - ∑ s, g s| ≤ (1 / 2 : ℝ) / 2), P ω)
    (a : Finset α) :
    1 - 2 * δ ≤ (∑ ω, P ω * ((alg ω).queries (fun _ => 0)).card)
      * (1 / ((Fintype.card α).choose #a : ℝ)) := by
  have hC : (0 : ℝ) < (Fintype.card α).choose #a := by
    exact_mod_cast Nat.choose_pos (card_le_univ a)
  refine symmetric_queries_ge (G := fun _ => True) (Φ := fun g => ∑ s, g s)
    alg P hP hP1 hcorr (fun _ _ _ => trivial) (fun σ g => ?_)
    (g := fun _ => 0) (ψ' := fun s => if s = a then 1 else 0) trivial (fun _ _ => rfl) trivial ?_ ?_
  · exact Fintype.sum_equiv (MulAction.toPerm σ) _ _ (fun s => rfl)
  · simp
    norm_num
  · intro r
    have hsub : {s ∈ powersetCard r (univ : Finset α) | (if s = a then (1 : ℝ) else 0) ≠ 0}
        ⊆ {a} := by
      intro s hs
      have h2 := (mem_filter.mp hs).2
      by_contra hne
      rw [mem_singleton] at hne
      simp [hne] at h2
    have hcard : (#{s ∈ powersetCard r (univ : Finset α) | (if s = a then (1 : ℝ) else 0) ≠ 0} : ℝ)
        ≤ 1 := by
      exact_mod_cast (card_le_card hsub).trans (card_singleton a).le
    rcases eq_or_ne r #a with rfl | hr
    · rw [one_div, inv_mul_cancel₀ hC.ne']
      exact hcard
    · have hempty : {s ∈ powersetCard r (univ : Finset α) | (if s = a then (1 : ℝ) else 0) ≠ 0}
          = ∅ := by
        refine eq_empty_of_forall_notMem fun s hs => ?_
        obtain ⟨h1, h2⟩ := mem_filter.mp hs
        have hsa : s = a := by
          by_contra hne
          simp [hne] at h2
        exact hr (hsa ▸ (mem_powersetCard.mp h1).2).symm
      rw [hempty]
      simp only [card_empty, Nat.cast_zero]
      positivity

end MetricChain.SymmetricSampling
