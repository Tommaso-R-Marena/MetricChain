import Mathlib

/-!
# Lemma 1: a linear code is an orthogonal array of strength `d^⊥ - 1`

Science division, workstream L1.  Source: `docs/science/INFERENCE_LIMITS.md` §1, Lemma 1:

> Let `C ⊆ F₂ⁿ` be a linear code whose dual `C^⊥` has minimum distance at least `k + 1`.  Every
> probability measure `μ` on `F₂ⁿ` with `μ(x + a) = μ(x)` for all `a ∈ C` has uniform marginals
> on every set `S` of at most `k` coordinates.

## What is proved

For any finite field `F` (in particular `ZMod 2`), any finite index type `ι`, a subspace
`C ≤ ι → F`:

* `restrict_surjective_of_dual` — if no non-zero vector supported on `S` is orthogonal to `C`
  (for the standard bilinear form `∑ i, u i * c i`), then the projection of `C` to the
  coordinates in `S` is onto;
* `marginal_const_of_invariant` — hence a `C`-invariant weight function has the same total
  weight on all cylinders over `S`;
* `uniform_marginal_of_invariant` — and if its total mass is `1`, every cylinder
  `{x | ∀ i ∈ S, x i = y i}` has weight `1 / |F| ^ |S|`;
* `lemma1_uniform_marginals` — **Lemma 1** in the dual-distance form: if every non-zero `u`
  orthogonal to `C` has Hamming weight `> k`, then every `C`-invariant `μ` of total mass `1`
  has uniform marginals on every `S` with `|S| ≤ k`;
* `lemma1_binary` — the case `F = ZMod 2` literally as in the note (value `1 / 2 ^ |S|`);
* `lemma1_marginals_agree` — two `C`-invariant probability vectors have the same marginals of
  order `≤ k` (the form used for the marginal oracle in Theorems 4 and 4′);
* `lemma1_sharp_witness` — non-vacuity and sharpness: for the repetition code `{00, 11}`
  (dual distance `2`, so `k = 1`) the hypothesis holds, and the uniform measure on the code is
  invariant but its marginal on the two coordinates is not uniform: `|S| ≤ k` cannot be relaxed
  to `|S| ≤ k + 1`.

## Differences from the note

* The hypothesis is the dual distance in the explicit form "every non-zero `u` with
  `∑ i, u i * c i = 0` for all `c ∈ C` has `hammingNorm u > k`".
* `μ` is not required to be non-negative: total mass `1` and invariance suffice.
* The proof is shorter than the note's: no decomposition into coset-uniform measures and no
  counting of fibres; translating by a codeword that projects to `y' - y` maps one cylinder
  onto the other.
* `C` is a `Submodule F (ι → F)`.  Over `ZMod 2` every additive subgroup is a subspace; that
  identification is not restated here.
-/

set_option autoImplicit false

namespace ScienceL1

open Finset

variable {ι F : Type*} [Fintype ι] [DecidableEq ι] [Field F] [Fintype F] [DecidableEq F]

/-- Restriction of a word to the coordinates in `S`. -/
def restr (S : Finset ι) (x : ι → F) : S → F := fun i => x i

omit [Fintype F] [DecidableEq F] in
/-- **The projection of a code to a set of coordinates carrying no dual word is onto.**
If the only vector supported on `S` and orthogonal to `C` is zero, then every pattern on `S` is
the restriction of a codeword. -/
theorem restrict_surjective_of_dual (C : Submodule F (ι → F)) (S : Finset ι)
    (hdual : ∀ u : ι → F, (∀ i, i ∉ S → u i = 0) → (∀ c ∈ C, ∑ i, u i * c i = 0) → u = 0)
    (y : S → F) : ∃ c ∈ C, ∀ i : S, c i = y i := by
  classical
  obtain ⟨π, hπ⟩ : ∃ π : (ι → F) →ₗ[F] (S → F), ∀ (x : ι → F) (i : S), π x i = x i :=
    ⟨LinearMap.funLeft F F Subtype.val, fun x i => rfl⟩
  by_contra hno
  have hlt : C.map π < ⊤ := by
    rw [lt_top_iff_ne_top]
    intro htop
    have hy : y ∈ C.map π := by
      rw [htop]
      exact Submodule.mem_top
    obtain ⟨c, hc, hcy⟩ := Submodule.mem_map.mp hy
    exact hno ⟨c, hc, fun i => by rw [← hcy, hπ]⟩
  obtain ⟨f, hf0, hker⟩ := Submodule.exists_le_ker_of_lt_top (C.map π) hlt
  have hgC : ∀ c ∈ C, f (π c) = 0 := fun c hc =>
    LinearMap.mem_ker.mp (hker (Submodule.mem_map_of_mem hc))
  have hrep : ∀ x : ι → F,
      f (π x) = ∑ i, f (π (fun j => if i = j then (1 : F) else 0)) * x i := by
    intro x
    have h := LinearMap.pi_apply_eq_sum_univ (f.comp π) x
    simp only [LinearMap.comp_apply, smul_eq_mul] at h
    rw [h]
    exact Finset.sum_congr rfl fun i _ => mul_comm _ _
  have hu : (fun i => f (π (fun j => if i = j then (1 : F) else 0))) = 0 := by
    apply hdual
    · intro i hi
      have h0 : π (fun j => if i = j then (1 : F) else 0) = 0 := by
        funext j
        rw [hπ]
        have hne : i ≠ (j : ι) := fun h => hi (by rw [h]; exact j.2)
        simp [hne]
      show f (π (fun j => if i = j then (1 : F) else 0)) = 0
      rw [h0, map_zero]
    · intro c hc
      have h := hgC c hc
      rw [hrep c] at h
      exact h
  refine hf0 (LinearMap.ext fun y' => ?_)
  obtain ⟨x, hx⟩ := (Subtype.val_injective (p := fun i => i ∈ S)).surjective_comp_right y'
  have hx' : π x = y' := by
    funext i
    rw [hπ]
    exact congrFun hx i
  rw [LinearMap.zero_apply, ← hx', hrep x]
  refine Finset.sum_eq_zero fun i _ => ?_
  have h := congrFun hu i
  simp only [Pi.zero_apply] at h
  rw [h, zero_mul]

/-- **Cylinders over `S` have equal weight.**  Under the hypothesis of
`restrict_surjective_of_dual`, a weight function invariant under translation by `C` gives the
same total weight to `{x | x|_S = z}` and to `{x | x|_S = z'}`. -/
theorem marginal_const_of_invariant (C : Submodule F (ι → F)) (S : Finset ι)
    (hdual : ∀ u : ι → F, (∀ i, i ∉ S → u i = 0) → (∀ c ∈ C, ∑ i, u i * c i = 0) → u = 0)
    (μ : (ι → F) → ℝ) (hinv : ∀ a ∈ C, ∀ x, μ (x + a) = μ x) (z z' : S → F) :
    ∑ x ∈ univ.filter (fun x : ι → F => restr S x = z), μ x =
      ∑ x ∈ univ.filter (fun x : ι → F => restr S x = z'), μ x := by
  obtain ⟨c, hc, hcz⟩ := restrict_surjective_of_dual C S hdual (z' - z)
  refine Finset.sum_equiv (Equiv.addRight c) (fun x => ?_) (fun x _ => ?_)
  · simp only [Finset.mem_filter, Finset.mem_univ, true_and, Equiv.coe_addRight]
    constructor
    · intro h
      funext i
      have h1 : x i = z i := congrFun h i
      have h2 : c i = z' i - z i := hcz i
      show x i + c i = z' i
      rw [h1, h2]
      ring
    · intro h
      funext i
      have h1 : x i + c i = z' i := congrFun h i
      have h2 : c i = z' i - z i := hcz i
      show x i = z i
      calc x i = x i + c i - c i := by ring
        _ = z' i - (z' i - z i) := by rw [h1, h2]
        _ = z i := by ring
  · exact (hinv c hc x).symm

/-- **Uniform marginal on `S`, restriction form.** -/
theorem marginal_eq_of_invariant (C : Submodule F (ι → F)) (S : Finset ι)
    (hdual : ∀ u : ι → F, (∀ i, i ∉ S → u i = 0) → (∀ c ∈ C, ∑ i, u i * c i = 0) → u = 0)
    (μ : (ι → F) → ℝ) (hsum : ∑ x, μ x = 1) (hinv : ∀ a ∈ C, ∀ x, μ (x + a) = μ x)
    (z : S → F) :
    ∑ x ∈ univ.filter (fun x : ι → F => restr S x = z), μ x =
      1 / (Fintype.card F : ℝ) ^ S.card := by
  have htotal : ∑ z' : S → F, ∑ x ∈ univ.filter (fun x : ι → F => restr S x = z'), μ x = 1 := by
    rw [Finset.sum_fiberwise]
    exact hsum
  obtain ⟨m, hm⟩ : ∃ m : ℝ, m = ∑ x ∈ univ.filter (fun x : ι → F => restr S x = z), μ x :=
    ⟨_, rfl⟩
  have hconst : ∀ z' : S → F,
      ∑ x ∈ univ.filter (fun x : ι → F => restr S x = z'), μ x = m := fun z' => by
    rw [hm]
    exact marginal_const_of_invariant C S hdual μ hinv z' z
  have h2 : ∑ _z' : S → F, m = 1 := by
    rw [← htotal]
    exact (Finset.sum_congr rfl fun z' _ => hconst z').symm
  rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, Fintype.card_fun, Fintype.card_coe]
    at h2
  push_cast at h2
  have hc : (0 : ℝ) < Fintype.card F := by exact_mod_cast Fintype.card_pos
  have hpos : (0 : ℝ) < (Fintype.card F : ℝ) ^ S.card := pow_pos hc _
  rw [← hm, eq_div_iff hpos.ne']
  linarith

/-- **Uniform marginal on `S`.**  If no non-zero vector supported on `S` is orthogonal to the
code `C`, then for every weight function `μ` of total mass `1` that is invariant under
translation by `C`, and every pattern `y`, the cylinder `{x | ∀ i ∈ S, x i = y i}` has weight
`1 / |F| ^ |S|`. -/
theorem uniform_marginal_of_invariant (C : Submodule F (ι → F)) (S : Finset ι)
    (hdual : ∀ u : ι → F, (∀ i, i ∉ S → u i = 0) → (∀ c ∈ C, ∑ i, u i * c i = 0) → u = 0)
    (μ : (ι → F) → ℝ) (hsum : ∑ x, μ x = 1) (hinv : ∀ a ∈ C, ∀ x, μ (x + a) = μ x)
    (y : ι → F) :
    ∑ x ∈ univ.filter (fun x : ι → F => ∀ i ∈ S, x i = y i), μ x =
      1 / (Fintype.card F : ℝ) ^ S.card := by
  have hfilter : univ.filter (fun x : ι → F => ∀ i ∈ S, x i = y i) =
      univ.filter (fun x : ι → F => restr S x = restr S y) := by
    refine Finset.filter_congr fun x _ => ?_
    constructor
    · intro h
      funext i
      exact h i i.2
    · intro h i hi
      exact congrFun h ⟨i, hi⟩
  rw [hfilter]
  exact marginal_eq_of_invariant C S hdual μ hsum hinv (restr S y)

omit [Fintype F] in
/-- A dual distance `> k` excludes non-zero dual words supported on a set of at most `k`
coordinates. -/
theorem no_dual_word_on_small_set (C : Submodule F (ι → F)) (k : ℕ)
    (hdist : ∀ u : ι → F, u ≠ 0 → (∀ c ∈ C, ∑ i, u i * c i = 0) → k < hammingNorm u)
    (S : Finset ι) (hS : S.card ≤ k) :
    ∀ u : ι → F, (∀ i, i ∉ S → u i = 0) → (∀ c ∈ C, ∑ i, u i * c i = 0) → u = 0 := by
  intro u hsupp horth
  by_contra hne
  have h1 := hdist u hne horth
  have h2 : hammingNorm u ≤ S.card := by
    unfold hammingNorm
    refine Finset.card_le_card fun i hi => ?_
    by_contra hiS
    exact (Finset.mem_filter.mp hi).2 (hsupp i hiS)
  omega

/-- **Lemma 1 (orthogonal-array property of linear codes).**  Let `C` be a linear code over a
finite field `F` whose dual has minimum distance `> k`: every non-zero `u` with
`∑ i, u i * c i = 0` for all `c ∈ C` has Hamming weight `> k`.  Then every weight function `μ`
of total mass `1` with `μ (x + a) = μ x` for all `a ∈ C` has uniform marginals on every set
`S` of at most `k` coordinates: each cylinder `{x | ∀ i ∈ S, x i = y i}` has weight
`1 / |F| ^ |S|`. -/
theorem lemma1_uniform_marginals (C : Submodule F (ι → F)) (k : ℕ)
    (hdist : ∀ u : ι → F, u ≠ 0 → (∀ c ∈ C, ∑ i, u i * c i = 0) → k < hammingNorm u)
    (μ : (ι → F) → ℝ) (hsum : ∑ x, μ x = 1) (hinv : ∀ a ∈ C, ∀ x, μ (x + a) = μ x)
    (S : Finset ι) (hS : S.card ≤ k) (y : ι → F) :
    ∑ x ∈ univ.filter (fun x : ι → F => ∀ i ∈ S, x i = y i), μ x =
      1 / (Fintype.card F : ℝ) ^ S.card :=
  uniform_marginal_of_invariant C S (no_dual_word_on_small_set C k hdist S hS) μ hsum hinv y

/-- **Lemma 1 as stated in the note** (`F = F₂`): a probability vector on `F₂ⁿ` invariant under
a linear code of dual distance at least `k + 1` has uniform marginals on every set of at most
`k` coordinates. -/
theorem lemma1_binary {n : ℕ} (C : Submodule (ZMod 2) (Fin n → ZMod 2)) (k : ℕ)
    (hdist : ∀ u : Fin n → ZMod 2, u ≠ 0 → (∀ c ∈ C, ∑ i, u i * c i = 0) → k + 1 ≤ hammingNorm u)
    (μ : (Fin n → ZMod 2) → ℝ) (_hμ : ∀ x, 0 ≤ μ x) (hsum : ∑ x, μ x = 1)
    (hinv : ∀ a ∈ C, ∀ x, μ (x + a) = μ x) (S : Finset (Fin n)) (hS : S.card ≤ k)
    (y : Fin n → ZMod 2) :
    ∑ x ∈ univ.filter (fun x : Fin n → ZMod 2 => ∀ i ∈ S, x i = y i), μ x =
      1 / (2 : ℝ) ^ S.card := by
  have h := lemma1_uniform_marginals C k (fun u hu horth => hdist u hu horth) μ hsum hinv S hS y
  have hcard : (Fintype.card (ZMod 2) : ℝ) = 2 := by
    rw [ZMod.card 2]
    norm_num
  rw [hcard] at h
  -- the two sides differ only in the `Decidable` instance chosen for `∀ i ∈ S, _` on `Fin n`
  convert h using 3

/-- **Two invariant ensembles have the same low-order marginals.**  The form used for the
marginal oracle: on `C`-invariant probability vectors the oracle for marginals of order `≤ k`
returns the same answer. -/
theorem lemma1_marginals_agree (C : Submodule F (ι → F)) (k : ℕ)
    (hdist : ∀ u : ι → F, u ≠ 0 → (∀ c ∈ C, ∑ i, u i * c i = 0) → k < hammingNorm u)
    (μ ν : (ι → F) → ℝ) (hμ : ∑ x, μ x = 1) (hν : ∑ x, ν x = 1)
    (hμinv : ∀ a ∈ C, ∀ x, μ (x + a) = μ x) (hνinv : ∀ a ∈ C, ∀ x, ν (x + a) = ν x)
    (S : Finset ι) (hS : S.card ≤ k) (y : ι → F) :
    ∑ x ∈ univ.filter (fun x : ι → F => ∀ i ∈ S, x i = y i), μ x =
      ∑ x ∈ univ.filter (fun x : ι → F => ∀ i ∈ S, x i = y i), ν x := by
  rw [lemma1_uniform_marginals C k hdist μ hμ hμinv S hS y,
    lemma1_uniform_marginals C k hdist ν hν hνinv S hS y]

/-! ### Non-vacuity and sharpness: the repetition code of length 2 -/

/-- **The hypothesis is satisfiable and `|S| ≤ k` is sharp.**  For the repetition code
`C = {00, 11} ⊆ F₂²`: every non-zero dual word has weight `2 > 1` (so Lemma 1 applies with
`k = 1`), the uniform measure on `C` is a `C`-invariant probability vector, and its marginal on
the set of both coordinates (`|S| = 2 = k + 1`) is not uniform: the cylinder `{00}` has weight
`1/2 ≠ 1/4`. -/
theorem lemma1_sharp_witness :
    ∃ (C : Submodule (ZMod 2) (Fin 2 → ZMod 2)) (μ : (Fin 2 → ZMod 2) → ℝ),
      (∀ u : Fin 2 → ZMod 2, u ≠ 0 → (∀ c ∈ C, ∑ i, u i * c i = 0) → 1 < hammingNorm u) ∧
      (∀ x, 0 ≤ μ x) ∧ ∑ x, μ x = 1 ∧ (∀ a ∈ C, ∀ x, μ (x + a) = μ x) ∧
      ∑ x ∈ univ.filter (fun x : Fin 2 → ZMod 2 => ∀ i ∈ (univ : Finset (Fin 2)), x i = 0), μ x ≠
        1 / (2 : ℝ) ^ (univ : Finset (Fin 2)).card := by
  have key : ∀ u : Fin 2 → ZMod 2, u ≠ 0 → u 0 + u 1 = 0 → 1 < hammingNorm u := by decide
  have hfil : (univ.filter fun x : Fin 2 → ZMod 2 => ∀ i ∈ (univ : Finset (Fin 2)), x i = 0) =
      {0} := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_singleton,
      forall_true_left]
    exact ⟨fun h => funext h, fun h i => by rw [h]; rfl⟩
  have hfil2 : (univ.filter fun x : Fin 2 → ZMod 2 => x 0 = x 1) = {0, fun _ => 1} := by decide
  refine ⟨Submodule.span (ZMod 2) {fun _ => 1}, fun x => if x 0 = x 1 then 1 / 2 else 0,
    ?_, ?_, ?_, ?_, ?_⟩
  · intro u hu horth
    have h := horth (fun _ => 1) (Submodule.mem_span_singleton_self _)
    rw [Fin.sum_univ_two] at h
    simp only [mul_one] at h
    exact key u hu h
  · intro x
    dsimp only
    split_ifs <;> norm_num
  · rw [← Finset.sum_filter, hfil2, Finset.sum_pair (by decide)]
    norm_num
  · intro a ha x
    obtain ⟨t, rfl⟩ := Submodule.mem_span_singleton.mp ha
    simp
  · rw [hfil, Finset.sum_singleton]
    norm_num

end ScienceL1

#print axioms ScienceL1.restrict_surjective_of_dual
#print axioms ScienceL1.marginal_const_of_invariant
#print axioms ScienceL1.uniform_marginal_of_invariant
#print axioms ScienceL1.lemma1_uniform_marginals
#print axioms ScienceL1.lemma1_binary
#print axioms ScienceL1.lemma1_marginals_agree
#print axioms ScienceL1.lemma1_sharp_witness
