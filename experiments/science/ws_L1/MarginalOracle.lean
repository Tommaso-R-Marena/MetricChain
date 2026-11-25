import Mathlib
import proofs.Frontiers.NonAdaptive

/-!
# Theorems 4 and 4′: query lower bounds with a free marginal oracle

Science division, workstream L1.  Sources: `docs/science/INFERENCE_LIMITS.md` §4, Theorem 4
(adaptive algorithms, at the zero residual) and `docs/science/INFERENCE_LIMITS_ADDENDA.md` A1,
Theorem 4′ (non-adaptive algorithms).  Both say: on the cube class with zero known part, free
and exact knowledge of all marginals of `μ_g` on at most `k` sites lowers the query lower bound
by at most the factor `|C|`, for every linear code `C` of dual distance `> k`.

This file assembles the two theorems completely, as corollaries of the theory division's
machine-checked packing bounds `MetricChain.expected_queries_ge_packing` and
`MetricChain.nonadaptive_expected_queries_ge` (`proofs/Frontiers/QueryLowerBound.lean`,
`NonAdaptive.lean`), which are imported read-only.

## The model of an oracle-assisted algorithm

The theory division's `QueryAlgorithm` has no side information, and its consistency axiom
(residuals that agree on the queried points are treated alike) is *false* for an algorithm that
also sees an oracle answer depending on the residual.  Here an oracle-assisted algorithm is a
**family of query algorithms indexed by the oracle's answer**:
`alg ω o : QueryAlgorithm (ι → F)` for the random seed `ω` and the answer `o`; on the residual
`g` it runs `alg ω (marginalOracle β k g)`.  The oracle `marginalOracle β k g` returns, for
every set `S` of at most `k` sites and every pattern `y`, the `μ_g`-probability of the cylinder
`{x | ∀ i ∈ S, x i = y i}`.  "Non-adaptive given the oracle" (Theorem 4′) means that the
query set is a function `Q ω o` of the seed and the oracle answer only.

On a family of residuals with a common oracle answer `o₀`, the algorithm is the plain query
algorithm `alg ω o₀`, and it is correct on the class restricted to residuals with answer `o₀`;
the theory division's bounds apply to that restricted class.

## What is proved (for `ι → F`, `F` any finite field; `F = ZMod 2` is the cube)

* `theorem4_adaptive_marginal_oracle` — **Theorem 4**.
* `theorem4'_nonadaptive_marginal_oracle` — **Theorem 4′**.
* supporting facts: `distToCoset_lipschitz` (a distance to a set is 1-Lipschitz),
  `distToCoset_add_mem` (invariance under the code), `card_centres_near` (every point lies in
  the difference sets of at most `|C| · |ball|` centres), `marginalOracle_of_invariant` (the
  oracle's answer on a code-invariant residual is the uniform one — Lemma 1).

The file is self-contained apart from the two imported packing bounds: the proofs of Lemma 1
(`OrthogonalArray.lean`) and of the separation inequality (`Separation.lean`) are repeated
verbatim, because the files of this directory do not import each other.

## Differences from the note

* A linear code is a finite set `C` containing `0` and closed under addition and scalar
  multiplication; its dual distance is `> k` in the form "every non-zero `u` with
  `∑ i, u i * a i = 0` for all `a ∈ C` has Hamming weight `> k`".
* Accuracy convention of the theory division: `(ε/2, δ)`-correct and gap `> ε` (the note's
  Theorem 4 says accuracy `ε` and gap `> 2ε`).
* The bound is stated without division:
  `(1 - 2δ) |F|^n ≤ E[#queries] · |C| · |{y : wt y < r}|`.
* In Theorem 4′, `D_R` appears as `log (A₁ / F₁)` with `A₁ = ∑ exp (-βc · wt)`,
  `F₁ = ∑ exp (-βc · max (wt, R))`; the closed forms of the note are not formalised.
* The expected number of queries is that of the run with the uniform oracle answer (the answer
  at the zero residual).
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL1

open Finset

/-! ## Part 0: Lemma 1 (repeated from `OrthogonalArray.lean`) -/

section Lemma1

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

end Lemma1

/-! ## Part 1: the separation inequality (repeated from `Separation.lean`) -/

section Abstract

variable {X : Type*} [Fintype X]

/-- The partition sum `∑ x, exp (-u * h x)` of the energy profile `h` at inverse temperature
`u` (zero known part). -/
def pSum (u : ℝ) (h : X → ℝ) : ℝ := ∑ x, Real.exp (-u * h x)

theorem pSum_pos [Nonempty X] (u : ℝ) (h : X → ℝ) : 0 < pSum u h :=
  Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty

omit [Fintype X] in
/-- For `u ≥ 0`, `t ↦ exp (-u t) - exp (-u max (t, R)) = (exp (-u t) - exp (-u R))₊` is
non-increasing. -/
theorem exp_sub_exp_max_antitone {u : ℝ} (hu : 0 ≤ u) (R : ℝ) {s t : ℝ} (hst : s ≤ t) :
    Real.exp (-u * t) - Real.exp (-u * max t R) ≤
      Real.exp (-u * s) - Real.exp (-u * max s R) := by
  rcases le_total t R with htR | hRt
  · rw [max_eq_right htR, max_eq_right (hst.trans htR)]
    have h1 : Real.exp (-u * t) ≤ Real.exp (-u * s) := by
      refine Real.exp_le_exp.mpr ?_
      have := mul_le_mul_of_nonneg_left hst hu
      linarith
    linarith
  · rw [max_eq_left hRt, sub_self]
    have h1 : Real.exp (-u * max s R) ≤ Real.exp (-u * s) := by
      refine Real.exp_le_exp.mpr ?_
      have := mul_le_mul_of_nonneg_left (le_max_left s R) hu
      linarith
    linarith

/-- Flattening at level `R` lowers the partition sum more for the lower profile:
`A₁ - F₁ ≤ A - F` when `dC ≤ d1` pointwise. -/
theorem pSum_sub_flat_mono {u : ℝ} (hu : 0 ≤ u) (R : ℝ) (dC d1 : X → ℝ)
    (hle : ∀ x, dC x ≤ d1 x) :
    pSum u d1 - pSum u (fun x => max (d1 x) R) ≤
      pSum u dC - pSum u (fun x => max (dC x) R) := by
  unfold pSum
  rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
  exact Finset.sum_le_sum fun x _ => exp_sub_exp_max_antitone hu R (hle x)

/-- Flattening does not increase the partition sum: `F ≤ A`. -/
theorem pSum_flat_le {u : ℝ} (hu : 0 ≤ u) (R : ℝ) (d : X → ℝ) :
    pSum u (fun x => max (d x) R) ≤ pSum u d := by
  unfold pSum
  refine Finset.sum_le_sum fun x _ => Real.exp_le_exp.mpr ?_
  have := mul_le_mul_of_nonneg_left (le_max_left (d x) R) hu
  linarith

/-- **Separation inequality of Theorem 4′, ratio form.**  `dC ≤ d1` pointwise, `u ≥ 0`.  With
`A = ∑ exp (-u dC)`, `F = ∑ exp (-u max (dC, R))`, `A₁ = ∑ exp (-u d1)`,
`F₁ = ∑ exp (-u max (d1, R))`: if `F ≤ m * F₁` then `1 + (A₁ / F₁ - 1) / m ≤ A / F`. -/
theorem separation_ratio [Nonempty X] {u : ℝ} (hu : 0 ≤ u) (R : ℝ) (dC d1 : X → ℝ)
    (hle : ∀ x, dC x ≤ d1 x) {m : ℝ}
    (hF : pSum u (fun x => max (dC x) R) ≤ m * pSum u (fun x => max (d1 x) R)) :
    1 + (pSum u d1 / pSum u (fun x => max (d1 x) R) - 1) / m ≤
      pSum u dC / pSum u (fun x => max (dC x) R) := by
  have hdiff := pSum_sub_flat_mono hu R dC d1 hle
  have hF1A1 := pSum_flat_le hu R d1
  have hFpos : 0 < pSum u (fun x => max (dC x) R) := pSum_pos u _
  have hF1pos : 0 < pSum u (fun x => max (d1 x) R) := pSum_pos u _
  revert hdiff hF1A1 hFpos hF1pos hF
  generalize pSum u dC = A
  generalize pSum u (fun x => max (dC x) R) = F
  generalize pSum u d1 = A1
  generalize pSum u (fun x => max (d1 x) R) = F1
  intro hF hdiff hF1A1 hFpos hF1pos
  have hm : 0 < m := by
    by_contra hneg
    have := mul_nonpos_of_nonpos_of_nonneg (not_lt.mp hneg) hF1pos.le
    linarith
  have hm' := hm.ne'
  have hF1' := hF1pos.ne'
  rw [le_div_iff₀ hFpos]
  have hq : F / (m * F1) ≤ 1 := (div_le_one (mul_pos hm hF1pos)).mpr hF
  have e : (1 + (A1 / F1 - 1) / m) * F = F + (A1 - F1) * (F / (m * F1)) := by
    field_simp
  rw [e]
  have h2 := mul_le_mul_of_nonneg_left hq (sub_nonneg.mpr hF1A1)
  linarith

/-- **Separation inequality of Theorem 4′, logarithmic form.**  If moreover `1 ≤ m`, then
`log (A₁ / F₁) - log m ≤ log A - log F`: symmetrising the cone over `m` translates costs at
most `log m` of the drop `D_R = log (A₁ / F₁)`. -/
theorem separation_log [Nonempty X] {u : ℝ} (hu : 0 ≤ u) (R : ℝ) (dC d1 : X → ℝ)
    (hle : ∀ x, dC x ≤ d1 x) {m : ℝ} (hm : 1 ≤ m)
    (hF : pSum u (fun x => max (dC x) R) ≤ m * pSum u (fun x => max (d1 x) R)) :
    Real.log (pSum u d1 / pSum u (fun x => max (d1 x) R)) - Real.log m ≤
      Real.log (pSum u dC) - Real.log (pSum u (fun x => max (dC x) R)) := by
  have hratio := separation_ratio hu R dC d1 hle hF
  have hF1A1 := pSum_flat_le hu R d1
  have hApos : 0 < pSum u dC := pSum_pos u _
  have hFpos : 0 < pSum u (fun x => max (dC x) R) := pSum_pos u _
  have hA1pos : 0 < pSum u d1 := pSum_pos u _
  have hF1pos : 0 < pSum u (fun x => max (d1 x) R) := pSum_pos u _
  have hm0 : 0 < m := by linarith
  have hρpos : 0 < pSum u d1 / pSum u (fun x => max (d1 x) R) := div_pos hA1pos hF1pos
  have hρ : 1 ≤ pSum u d1 / pSum u (fun x => max (d1 x) R) := (one_le_div hF1pos).mpr hF1A1
  have h1 : pSum u d1 / pSum u (fun x => max (d1 x) R) / m ≤
      1 + (pSum u d1 / pSum u (fun x => max (d1 x) R) - 1) / m := by
    have hinv : 1 / m ≤ 1 := (div_le_one hm0).mpr hm
    have e : 1 + (pSum u d1 / pSum u (fun x => max (d1 x) R) - 1) / m -
        pSum u d1 / pSum u (fun x => max (d1 x) R) / m = 1 - 1 / m := by ring
    linarith
  have h3 : Real.log (pSum u d1 / pSum u (fun x => max (d1 x) R) / m) ≤
      Real.log (pSum u dC / pSum u (fun x => max (dC x) R)) :=
    Real.log_le_log (div_pos hρpos hm0) (h1.trans hratio)
  rw [Real.log_div hρpos.ne' hm0.ne', Real.log_div hApos.ne' hFpos.ne'] at h3
  exact h3

end Abstract

section Hamming

variable {ι G : Type*} [Fintype ι] [DecidableEq ι] [AddCommGroup G] [Fintype G] [DecidableEq G]

omit [DecidableEq ι] [Fintype G] in
/-- The Hamming distance is translation invariant. -/
theorem hammingDist_add_right_cancel (x y a : ι → G) :
    hammingDist (x + a) (y + a) = hammingDist x y := by
  rw [hammingDist_eq_hammingNorm, hammingDist_eq_hammingNorm]
  congr 1
  abel

/-- `d_C(x) = d_H(x, s + C) = min_{a ∈ C} d_H(x, s + a)`: the Hamming distance from `x` to the
translate `s + C` of a non-empty finite set `C`, as a real number. -/
def distToCoset (C : Finset (ι → G)) (hC : C.Nonempty) (s x : ι → G) : ℝ :=
  C.inf' hC fun a => (hammingDist x (s + a) : ℝ)

omit [DecidableEq ι] [Fintype G] in
/-- `d_C ≤ d_H(·, s)` when `0 ∈ C`. -/
theorem distToCoset_le (C : Finset (ι → G)) (hC : C.Nonempty) (h0 : (0 : ι → G) ∈ C)
    (s x : ι → G) : distToCoset C hC s x ≤ (hammingDist x s : ℝ) := by
  unfold distToCoset
  refine (Finset.inf'_le (fun a => (hammingDist x (s + a) : ℝ)) h0).trans (le_of_eq ?_)
  simp

/-- **`F ≤ |C| · F₁`.**  The flattened symmetrised cone has partition sum at most `|C|` times
that of the flattened cone: `exp (-u max (d_C, R)) = max_a exp (-u max (d_H(·, s + a), R))` is
at most the sum over `a ∈ C`, and each translate has the same partition sum.  No sign
condition on `u`, no structure on `C`. -/
theorem pSum_flat_distToCoset_le (C : Finset (ι → G)) (hC : C.Nonempty) (s : ι → G)
    (u R : ℝ) :
    pSum u (fun x => max (distToCoset C hC s x) R) ≤
      C.card * pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R) := by
  have hshift : ∀ a : ι → G,
      ∑ x : ι → G, Real.exp (-u * max (hammingDist x (s + a) : ℝ) R) =
        pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R) := by
    intro a
    unfold pSum
    symm
    refine Fintype.sum_equiv (Equiv.addRight a) _ _ fun x => ?_
    show Real.exp (-u * max (hammingDist x s : ℝ) R) =
      Real.exp (-u * max (hammingDist (x + a) (s + a) : ℝ) R)
    rw [hammingDist_add_right_cancel]
  have hpt : ∀ x : ι → G, Real.exp (-u * max (distToCoset C hC s x) R) ≤
      ∑ a ∈ C, Real.exp (-u * max (hammingDist x (s + a) : ℝ) R) := by
    intro x
    obtain ⟨a, haC, ha⟩ := Finset.exists_mem_eq_inf' hC fun a => (hammingDist x (s + a) : ℝ)
    have e : distToCoset C hC s x = (hammingDist x (s + a) : ℝ) := ha
    rw [e]
    exact Finset.single_le_sum
      (f := fun a => Real.exp (-u * max (hammingDist x (s + a) : ℝ) R))
      (fun b _ => (Real.exp_pos _).le) haC
  calc pSum u (fun x => max (distToCoset C hC s x) R)
      = ∑ x : ι → G, Real.exp (-u * max (distToCoset C hC s x) R) := rfl
    _ ≤ ∑ x : ι → G, ∑ a ∈ C, Real.exp (-u * max (hammingDist x (s + a) : ℝ) R) :=
        Finset.sum_le_sum fun x _ => hpt x
    _ = ∑ a ∈ C, ∑ x : ι → G, Real.exp (-u * max (hammingDist x (s + a) : ℝ) R) :=
        Finset.sum_comm
    _ = ∑ _a ∈ C, pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R) :=
        Finset.sum_congr rfl fun a _ => hshift a
    _ = C.card * pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R) := by
        rw [Finset.sum_const, nsmul_eq_mul]

/-- **Theorem 4′, the separation step.**  `C` a finite set of translations containing `0`,
`s` a centre, `u ≥ 0`, any level `R`.  With `d_C = d_H(·, s + C)`:
`log (A₁ / F₁) - log |C| ≤ log Z(cone^C_s) - log Z(flat^C_s)`,
where `log (A₁ / F₁) = D_R` is the drop for the unsymmetrised cone. -/
theorem separation_distToCoset (C : Finset (ι → G)) (hC : C.Nonempty)
    (h0 : (0 : ι → G) ∈ C) (s : ι → G) {u : ℝ} (hu : 0 ≤ u) (R : ℝ) :
    Real.log (pSum u (fun x : ι → G => (hammingDist x s : ℝ)) /
        pSum u (fun x : ι → G => max (hammingDist x s : ℝ) R)) - Real.log C.card ≤
      Real.log (pSum u (distToCoset C hC s)) -
        Real.log (pSum u (fun x => max (distToCoset C hC s x) R)) := by
  have hcard : (1 : ℝ) ≤ C.card := by exact_mod_cast Finset.card_pos.mpr hC
  exact separation_log hu R (distToCoset C hC s) (fun x => (hammingDist x s : ℝ))
    (distToCoset_le C hC h0 s) hcard (pSum_flat_distToCoset_le C hC s u R)

end Hamming

/-! ## Part 2: the cube, the marginal oracle, and the two theorems -/

section Cube

variable {ι F : Type*} [Fintype ι] [DecidableEq ι] [Field F] [Fintype F] [DecidableEq F]

/-! ### Geometry of the distance to a translated code -/

omit [DecidableEq ι] [Fintype F] in
/-- A distance to a set is 1-Lipschitz for the Hamming distance. -/
theorem distToCoset_lipschitz (C : Finset (ι → F)) (hC : C.Nonempty) (s x y : ι → F) :
    distToCoset C hC s x ≤ distToCoset C hC s y + hammingDist x y := by
  unfold distToCoset
  obtain ⟨a, haC, ha⟩ := Finset.exists_mem_eq_inf' hC fun a => (hammingDist y (s + a) : ℝ)
  rw [ha]
  refine (Finset.inf'_le (fun a => (hammingDist x (s + a) : ℝ)) haC).trans ?_
  have h := hammingDist_triangle x y (s + a)
  have h2 : (hammingDist x (s + a) : ℝ) ≤ (hammingDist x y : ℝ) + (hammingDist y (s + a) : ℝ) := by
    exact_mod_cast h
  show (hammingDist x (s + a) : ℝ) ≤ (hammingDist y (s + a) : ℝ) + (hammingDist x y : ℝ)
  linarith

omit [DecidableEq ι] [Fintype F] in
/-- The distance to `s + C` is invariant under translation of the point by an element of `C`,
when `C` is closed under addition and negation. -/
theorem distToCoset_add_mem (C : Finset (ι → F)) (hC : C.Nonempty)
    (hadd : ∀ a ∈ C, ∀ b ∈ C, a + b ∈ C) (hneg : ∀ a ∈ C, -a ∈ C) (s x b : ι → F)
    (hb : b ∈ C) : distToCoset C hC s (x + b) = distToCoset C hC s x := by
  unfold distToCoset
  apply le_antisymm
  · obtain ⟨a, haC, ha⟩ := Finset.exists_mem_eq_inf' hC fun a => (hammingDist x (s + a) : ℝ)
    rw [ha]
    refine (Finset.inf'_le (fun a => (hammingDist (x + b) (s + a) : ℝ))
      (hadd a haC b hb)).trans (le_of_eq ?_)
    show (hammingDist (x + b) (s + (a + b)) : ℝ) = (hammingDist x (s + a) : ℝ)
    rw [← add_assoc, hammingDist_add_right_cancel]
  · obtain ⟨a, haC, ha⟩ :=
      Finset.exists_mem_eq_inf' hC fun a => (hammingDist (x + b) (s + a) : ℝ)
    rw [ha]
    refine (Finset.inf'_le (fun a => (hammingDist x (s + a) : ℝ))
      (hadd a haC (-b) (hneg b hb))).trans (le_of_eq ?_)
    show (hammingDist x (s + (a + -b)) : ℝ) = (hammingDist (x + b) (s + a) : ℝ)
    have e : s + (a + -b) + b = s + a := by abel
    rw [← hammingDist_add_right_cancel x (s + (a + -b)) b, e]

/-- **Every point is near few centres.**  For a point `x`, the centres `s` with
`d_H(x, s + C) < r` number at most `|C|` times the size of the open Hamming ball of radius
`r`. -/
theorem card_centres_near (C : Finset (ι → F)) (hC : C.Nonempty) (x : ι → F) (r : ℝ) :
    ((univ.filter fun s : ι → F => distToCoset C hC s x < r).card : ℝ) ≤
      C.card * ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < r).card : ℝ) := by
  have hsub : (univ.filter fun s : ι → F => distToCoset C hC s x < r) ⊆
      C.biUnion fun a => univ.filter fun s : ι → F => (hammingDist x (s + a) : ℝ) < r := by
    intro s hs
    obtain ⟨a, haC, ha⟩ := Finset.exists_mem_eq_inf' hC fun a => (hammingDist x (s + a) : ℝ)
    have hs' : distToCoset C hC s x < r := (Finset.mem_filter.mp hs).2
    have e : distToCoset C hC s x = (hammingDist x (s + a) : ℝ) := ha
    rw [e] at hs'
    exact Finset.mem_biUnion.mpr ⟨a, haC, Finset.mem_filter.mpr ⟨Finset.mem_univ s, hs'⟩⟩
  have hcard : ∀ a : ι → F,
      (univ.filter fun s : ι → F => (hammingDist x (s + a) : ℝ) < r).card =
        (univ.filter fun y : ι → F => (hammingNorm y : ℝ) < r).card := by
    intro a
    refine Finset.card_equiv ((Equiv.addRight a).trans (Equiv.addLeft (-x))) fun s => ?_
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Equiv.trans_apply,
      Equiv.coe_addRight, Equiv.coe_addLeft]
    rw [hammingDist_eq_hammingNorm]
  calc ((univ.filter fun s : ι → F => distToCoset C hC s x < r).card : ℝ)
      ≤ ((C.biUnion fun a => univ.filter fun s : ι → F =>
          (hammingDist x (s + a) : ℝ) < r).card : ℝ) := by
        exact_mod_cast Finset.card_le_card hsub
    _ ≤ ∑ a ∈ C, ((univ.filter fun s : ι → F => (hammingDist x (s + a) : ℝ) < r).card : ℝ) := by
        exact_mod_cast Finset.card_biUnion_le
    _ = ∑ _a ∈ C, ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < r).card : ℝ) :=
        Finset.sum_congr rfl fun a _ => by rw [hcard a]
    _ = C.card * ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < r).card : ℝ) := by
        rw [Finset.sum_const, nsmul_eq_mul]

/-! ### The class, the target, the ensembles and the oracle -/

/-- The first-order class on the cube: `g x - g y ≤ c · d_H(x, y)`. -/
def HammingLip (c : ℝ) (g : (ι → F) → ℝ) : Prop := ∀ x y, g x - g y ≤ c * hammingDist x y

omit [DecidableEq ι] [Field F] [Fintype F] in
/-- `HammingLip c` is, by definition, the theory division's envelope class `Admissible` for the
envelope `c · d_H`. -/
theorem hammingLip_iff_admissible (c : ℝ) (g : (ι → F) → ℝ) :
    HammingLip c g ↔ MetricChain.Admissible (fun x y : ι → F => c * (hammingDist x y : ℝ)) g :=
  Iff.rfl

/-- `log Z_g = log ∑ x, exp (-β g x)` (zero known part). -/
def logZ (β : ℝ) (g : (ι → F) → ℝ) : ℝ := Real.log (∑ x, Real.exp (-β * g x))

/-- The Gibbs ensemble `μ_g` of the residual `g` (zero known part). -/
def gibbs (β : ℝ) (g : (ι → F) → ℝ) (x : ι → F) : ℝ :=
  Real.exp (-β * g x) / ∑ y, Real.exp (-β * g y)

/-- **The marginal oracle of order `k`**: for every set `S` of at most `k` sites and every
pattern `y`, the `μ_g`-probability that the configuration agrees with `y` on `S`; no information
(`0`) for larger sets. -/
def marginalOracle (β : ℝ) (k : ℕ) (g : (ι → F) → ℝ) : Finset ι → (ι → F) → ℝ := fun S y =>
  if S.card ≤ k then ∑ x ∈ univ.filter (fun x : ι → F => ∀ i ∈ S, x i = y i), gibbs β g x else 0

/-- The symmetrised dip `g_a^C(x) = -c (r - d_H(x, a + C))₊` of Theorem 4. -/
def symDip (C : Finset (ι → F)) (hC : C.Nonempty) (c r : ℝ) (a x : ι → F) : ℝ :=
  -(c * max (r - distToCoset C hC a x) 0)

/-- The dip `g_a(x) = -c (r - d_H(x, a))₊`. -/
def dipAt (c r : ℝ) (a x : ι → F) : ℝ := -(c * max (r - (hammingDist x a : ℝ)) 0)

omit [DecidableEq F] in
theorem sum_gibbs (β : ℝ) (g : (ι → F) → ℝ) : ∑ x, gibbs β g x = 1 := by
  unfold gibbs
  rw [← Finset.sum_div]
  exact div_self (Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty).ne'

omit [DecidableEq F] in
/-- `log Z` is antitone in the residual (for `β ≥ 0`). -/
theorem logZ_anti {β : ℝ} (hβ : 0 ≤ β) {g g' : (ι → F) → ℝ} (h : ∀ x, g x ≤ g' x) :
    logZ β g' ≤ logZ β g := by
  unfold logZ
  refine Real.log_le_log (Finset.sum_pos (fun _ _ => Real.exp_pos _) Finset.univ_nonempty) ?_
  refine Finset.sum_le_sum fun x _ => Real.exp_le_exp.mpr ?_
  have := mul_le_mul_of_nonneg_left (h x) hβ
  linarith

omit [Field F] [DecidableEq F] in
/-- `log Z` of `c · h` is the logarithm of the partition sum of `h` at `u = β c`. -/
theorem logZ_mul (β c : ℝ) (h : (ι → F) → ℝ) :
    logZ β (fun x => c * h x) = Real.log (pSum (β * c) h) := by
  unfold logZ pSum
  congr 1
  refine Finset.sum_congr rfl fun x _ => ?_
  congr 1
  ring

/-- Partition sums of a function of the Hamming distance to a centre do not depend on the
centre. -/
theorem pSum_hammingDist_shift (u : ℝ) (φ : ℝ → ℝ) (s : ι → F) :
    pSum u (fun x : ι → F => φ (hammingDist x s)) =
      pSum u (fun x : ι → F => φ (hammingNorm x)) := by
  unfold pSum
  symm
  refine Fintype.sum_equiv (Equiv.addRight s) _ _ fun x => ?_
  have h := hammingDist_add_right_cancel x 0 s
  rw [zero_add, hammingDist_zero_right] at h
  show Real.exp (-u * φ (hammingNorm x)) = Real.exp (-u * φ (hammingDist (x + s) s))
  rw [h]

/-- `log Z` of a dip does not depend on its centre. -/
theorem logZ_dipAt (β c r : ℝ) (a : ι → F) :
    logZ β (dipAt c r a) = logZ β (dipAt c r (0 : ι → F)) := by
  unfold logZ
  congr 1
  symm
  refine Fintype.sum_equiv (Equiv.addRight a) _ _ fun x => ?_
  have h := hammingDist_add_right_cancel x 0 a
  rw [zero_add] at h
  show Real.exp (-β * dipAt c r 0 x) = Real.exp (-β * dipAt c r a (x + a))
  unfold dipAt
  rw [h]

omit [DecidableEq ι] [Field F] [Fintype F] in
theorem zero_hammingLip {c : ℝ} (hc : 0 ≤ c) : HammingLip c (0 : (ι → F) → ℝ) := by
  intro x y
  show (0 : ℝ) - 0 ≤ c * hammingDist x y
  rw [sub_zero]
  exact mul_nonneg hc (Nat.cast_nonneg _)

omit [DecidableEq ι] [Fintype F] in
/-- The symmetrised dip is in the class. -/
theorem symDip_lip (C : Finset (ι → F)) (hC : C.Nonempty) {c : ℝ} (hc : 0 ≤ c) (r : ℝ)
    (a : ι → F) : HammingLip c (symDip C hC c r a) := by
  intro x y
  unfold symDip
  have h1 := max_sub_max_le_max (r - distToCoset C hC a y) 0 (r - distToCoset C hC a x) 0
  have h2 : max (r - distToCoset C hC a y - (r - distToCoset C hC a x)) (0 - 0) ≤
      (hammingDist x y : ℝ) := by
    refine max_le ?_ (by simp)
    linarith [distToCoset_lipschitz C hC a x y]
  have h3 := mul_le_mul_of_nonneg_left (h1.trans h2) hc
  linarith

omit [DecidableEq ι] [Fintype F] in
/-- The symmetrised cone `c · d_H(·, s + C)` is in the class. -/
theorem cone_lip (C : Finset (ι → F)) (hC : C.Nonempty) {c : ℝ} (hc : 0 ≤ c) (s : ι → F) :
    HammingLip c (fun x => c * distToCoset C hC s x) := by
  intro x y
  have h := mul_le_mul_of_nonneg_left
    (sub_le_iff_le_add'.mpr (distToCoset_lipschitz C hC s x y)) hc
  show c * distToCoset C hC s x - c * distToCoset C hC s y ≤ c * hammingDist x y
  linarith

omit [DecidableEq ι] [Fintype F] in
/-- The flattened symmetrised cone `c · max (d_H(·, s + C), R)` is in the class. -/
theorem flat_lip (C : Finset (ι → F)) (hC : C.Nonempty) {c : ℝ} (hc : 0 ≤ c) (R : ℝ)
    (s : ι → F) : HammingLip c (fun x => c * max (distToCoset C hC s x) R) := by
  intro x y
  have h1 := max_sub_max_le_max (distToCoset C hC s x) R (distToCoset C hC s y) R
  have h2 : max (distToCoset C hC s x - distToCoset C hC s y) (R - R) ≤
      (hammingDist x y : ℝ) := by
    refine max_le ?_ (by simp)
    linarith [distToCoset_lipschitz C hC s x y]
  have h3 := mul_le_mul_of_nonneg_left (h1.trans h2) hc
  show c * max (distToCoset C hC s x) R - c * max (distToCoset C hC s y) R ≤
    c * hammingDist x y
  linarith

omit [DecidableEq ι] [Fintype F] in
/-- The symmetrised dip lies below the dip (when `0 ∈ C`). -/
theorem symDip_le_dipAt (C : Finset (ι → F)) (hC : C.Nonempty) (h0 : (0 : ι → F) ∈ C)
    {c : ℝ} (hc : 0 ≤ c) (r : ℝ) (a x : ι → F) : symDip C hC c r a x ≤ dipAt c r a x := by
  unfold symDip dipAt
  have h1 := distToCoset_le C hC h0 a x
  have h2 : max (r - (hammingDist x a : ℝ)) 0 ≤ max (r - distToCoset C hC a x) 0 :=
    max_le_max (by linarith) le_rfl
  have h3 := mul_le_mul_of_nonneg_left h2 hc
  linarith

/-! ### The oracle cannot tell code-invariant residuals apart -/

/-- A finite set containing `0` and closed under addition and scalar multiplication, as a
subspace. -/
def codeSubmodule (C : Finset (ι → F)) (h0 : (0 : ι → F) ∈ C)
    (hadd : ∀ a ∈ C, ∀ b ∈ C, a + b ∈ C) (hsmul : ∀ (t : F), ∀ a ∈ C, t • a ∈ C) :
    Submodule F (ι → F) where
  carrier := ↑C
  add_mem' := fun {a b} ha hb => hadd a ha b hb
  zero_mem' := h0
  smul_mem' := fun t {a} ha => hsmul t a ha

/-- **The oracle's answer on a code-invariant residual is the uniform one** (Lemma 1). -/
theorem marginalOracle_of_invariant (C : Submodule F (ι → F)) (k : ℕ)
    (hdist : ∀ u : ι → F, u ≠ 0 → (∀ c ∈ C, ∑ i, u i * c i = 0) → k < hammingNorm u)
    (β : ℝ) (g : (ι → F) → ℝ) (hg : ∀ a ∈ C, ∀ x, g (x + a) = g x) :
    marginalOracle β k g =
      fun S _ => if S.card ≤ k then 1 / (Fintype.card F : ℝ) ^ S.card else 0 := by
  funext S y
  show marginalOracle β k g S y = if S.card ≤ k then 1 / (Fintype.card F : ℝ) ^ S.card else 0
  unfold marginalOracle
  split_ifs with hS
  · exact lemma1_uniform_marginals C k hdist (gibbs β g) (sum_gibbs β g)
      (fun a ha x => by unfold gibbs; rw [hg a ha x]) S hS y
  · rfl

/-- Two residuals invariant under a linear code of dual distance `> k` receive the same answer
from the marginal oracle of order `k`; in particular the answer at the zero residual. -/
theorem marginalOracle_eq_of_invariant (C : Finset (ι → F)) (h0 : (0 : ι → F) ∈ C)
    (hadd : ∀ a ∈ C, ∀ b ∈ C, a + b ∈ C) (hsmul : ∀ (t : F), ∀ a ∈ C, t • a ∈ C) (k : ℕ)
    (hdist : ∀ u : ι → F, u ≠ 0 → (∀ a ∈ C, ∑ i, u i * a i = 0) → k < hammingNorm u)
    (β : ℝ) (g : (ι → F) → ℝ) (hg : ∀ a ∈ C, ∀ x, g (x + a) = g x) :
    marginalOracle β k g = marginalOracle β k (0 : (ι → F) → ℝ) := by
  rw [marginalOracle_of_invariant (codeSubmodule C h0 hadd hsmul) k
      (fun u hu h => hdist u hu fun a ha => h a ha) β g (fun a ha x => hg a ha x),
    marginalOracle_of_invariant (codeSubmodule C h0 hadd hsmul) k
      (fun u hu h => hdist u hu fun a ha => h a ha) β 0 (fun _ _ _ => rfl)]

omit [Field F] in
/-- Sanity check on the oracle: for `k ≥ 1` its answer on a singleton `{i}` is the one-site
marginal of `μ_g` at site `i` (so the oracle is informative, and not constant on the class). -/
theorem marginalOracle_singleton (β : ℝ) {k : ℕ} (hk : 1 ≤ k) (g : (ι → F) → ℝ) (i : ι)
    (y : ι → F) :
    marginalOracle β k g {i} y =
      ∑ x ∈ univ.filter (fun x : ι → F => x i = y i), gibbs β g x := by
  unfold marginalOracle
  rw [if_pos (by rw [Finset.card_singleton]; exact hk)]
  refine Finset.sum_congr (Finset.filter_congr fun x _ => ?_) fun _ _ => rfl
  simp

/-! ### Theorem 4 -/

open Classical in
/-- **Theorem 4 (a marginal oracle is worth at most the factor `|C|` at the zero residual).**
Cube class `HammingLip c` on `ι → F`, zero known part, `β, c ≥ 0`.  `C` a linear code of dual
distance `> k`.  A randomised oracle-assisted algorithm (`alg ω o`, run with
`o = marginalOracle β k g`) that returns `log Z_g` within `ε / 2` with probability at least
`1 - δ` on every member of the class.  If the dip of radius `r` raises `log Z` by more than `ε`,
then at the zero residual
`(1 - 2δ) · |F|^n ≤ E[number of evaluations] · |C| · |{y : wt y < r}|`. -/
theorem theorem4_adaptive_marginal_oracle
    (C : Finset (ι → F)) (h0 : (0 : ι → F) ∈ C) (hadd : ∀ a ∈ C, ∀ b ∈ C, a + b ∈ C)
    (hsmul : ∀ (t : F), ∀ a ∈ C, t • a ∈ C) (k : ℕ)
    (hdist : ∀ u : ι → F, u ≠ 0 → (∀ a ∈ C, ∑ i, u i * a i = 0) → k < hammingNorm u)
    {β c : ℝ} (hβ : 0 ≤ β) (hc : 0 ≤ c) (r : ℝ) {ε δ : ℝ} {Ω : Type*} [Fintype Ω]
    (alg : Ω → (Finset ι → (ι → F) → ℝ) → MetricChain.QueryAlgorithm (ι → F))
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    (hcorr : ∀ g : (ι → F) → ℝ, HammingLip c g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
        |(alg ω (marginalOracle β k g)).output g - logZ β g| ≤ ε / 2), P ω)
    (hsens : ε < logZ β (dipAt c r (0 : ι → F)) - logZ β (0 : (ι → F) → ℝ)) :
    (1 - 2 * δ) * (Fintype.card F : ℝ) ^ Fintype.card ι ≤
      (∑ ω, P ω * ((alg ω (marginalOracle β k 0)).queries 0).card) *
        (C.card * ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < r).card : ℝ)) := by
  have hC : C.Nonempty := ⟨0, h0⟩
  have hneg : ∀ a ∈ C, -a ∈ C := fun a ha => by
    have h := hsmul (-1) a ha
    rwa [neg_one_smul] at h
  have hOinv : ∀ g : (ι → F) → ℝ, (∀ a ∈ C, ∀ x, g (x + a) = g x) →
      marginalOracle β k g = marginalOracle β k (0 : (ι → F) → ℝ) := fun g hg =>
    marginalOracle_eq_of_invariant C h0 hadd hsmul k hdist β g hg
  have hcorr' : ∀ g : (ι → F) → ℝ,
      (HammingLip c g ∧ marginalOracle β k g = marginalOracle β k (0 : (ι → F) → ℝ)) →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
        |(alg ω (marginalOracle β k (0 : (ι → F) → ℝ))).output g - logZ β g| ≤ ε / 2), P ω := by
    rintro g ⟨hg, hO⟩
    have h := hcorr g hg
    rw [hO] at h
    exact h
  have key := MetricChain.expected_queries_ge_packing
    (G := fun g : (ι → F) → ℝ =>
      HammingLip c g ∧ marginalOracle β k g = marginalOracle β k (0 : (ι → F) → ℝ))
    (Φ := logZ β) (fun ω => alg ω (marginalOracle β k (0 : (ι → F) → ℝ))) P hP hP1 hcorr'
    (g := (0 : (ι → F) → ℝ)) ⟨zero_hammingLip hc, rfl⟩
    (fun a => symDip C hC c r a)
    (fun a => ⟨symDip_lip C hC hc r a, hOinv _ fun b hb x => by
      unfold symDip
      rw [distToCoset_add_mem C hC hadd hneg a x b hb]⟩)
    (fun a => by
      have h1 : logZ β (dipAt c r a) ≤ logZ β (symDip C hC c r a) :=
        logZ_anti hβ (symDip_le_dipAt C hC h0 hc r a)
      have h2 := logZ_dipAt β c r a
      refine lt_of_lt_of_le ?_ (le_abs_self _)
      show ε < logZ β (symDip C hC c r a) - logZ β (0 : (ι → F) → ℝ)
      linarith)
    (fun _ => (1 : ℝ)) (fun _ => zero_le_one)
    (B := C.card * ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < r).card : ℝ))
    (fun x => by
      rw [Finset.sum_const, nsmul_eq_mul, mul_one]
      refine le_trans ?_ (card_centres_near C hC x r)
      refine Nat.cast_le.mpr (Finset.card_le_card fun a ha => ?_)
      have ha' := (Finset.mem_filter.mp ha).2
      refine Finset.mem_filter.mpr ⟨Finset.mem_univ a, ?_⟩
      by_contra hnot
      apply ha'
      have hmax : max (r - distToCoset C hC a x) 0 = 0 :=
        max_eq_right (by linarith [not_lt.mp hnot])
      show symDip C hC c r a x = 0
      unfold symDip
      rw [hmax, mul_zero, neg_zero])
  have hcard : ∑ _j : ι → F, (1 : ℝ) = (Fintype.card F : ℝ) ^ Fintype.card ι := by
    rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one, Fintype.card_fun,
      Nat.cast_pow]
  have key' : (1 - 2 * δ) * ∑ _j : ι → F, (1 : ℝ) ≤
      (∑ ω, P ω * ((alg ω (marginalOracle β k 0)).queries 0).card) *
        (C.card * ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < r).card : ℝ)) := key
  rw [hcard] at key'
  exact key'

/-! ### Theorem 4′ -/

open Classical in
/-- **Theorem 4′ (the non-adaptive bound survives a marginal oracle).**  Cube class
`HammingLip c` on `ι → F`, zero known part, `β, c ≥ 0`.  `C` a linear code of dual distance
`> k`.  A randomised oracle-assisted algorithm whose query set `Q ω o` depends only on the seed
and on the oracle's answer, `(ε/2, δ)`-correct for `log Z` on the class.  If
`ε < D_R - log |C|`, with `D_R = log (A₁ / F₁)` the drop of `log Z` when the cone `c · wt` is
flattened at level `R`, then
`(1 - 2δ) · |F|^n ≤ E[number of evaluations] · |C| · |{y : wt y < R}|`,
the expectation being taken for the uniform oracle answer. -/
theorem theorem4'_nonadaptive_marginal_oracle
    (C : Finset (ι → F)) (h0 : (0 : ι → F) ∈ C) (hadd : ∀ a ∈ C, ∀ b ∈ C, a + b ∈ C)
    (hsmul : ∀ (t : F), ∀ a ∈ C, t • a ∈ C) (k : ℕ)
    (hdist : ∀ u : ι → F, u ≠ 0 → (∀ a ∈ C, ∑ i, u i * a i = 0) → k < hammingNorm u)
    {β c : ℝ} (hβ : 0 ≤ β) (hc : 0 ≤ c) (R : ℝ) {ε δ : ℝ} {Ω : Type*} [Fintype Ω]
    (alg : Ω → (Finset ι → (ι → F) → ℝ) → MetricChain.QueryAlgorithm (ι → F))
    (Q : Ω → (Finset ι → (ι → F) → ℝ) → Finset (ι → F))
    (hna : ∀ ω o g, (alg ω o).queries g = Q ω o)
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    (hcorr : ∀ g : (ι → F) → ℝ, HammingLip c g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
        |(alg ω (marginalOracle β k g)).output g - logZ β g| ≤ ε / 2), P ω)
    (hsens : ε < Real.log (pSum (β * c) (fun x : ι → F => (hammingNorm x : ℝ)) /
        pSum (β * c) (fun x : ι → F => max (hammingNorm x : ℝ) R)) - Real.log C.card) :
    (1 - 2 * δ) * (Fintype.card F : ℝ) ^ Fintype.card ι ≤
      (∑ ω, P ω * (Q ω (marginalOracle β k 0)).card) *
        (C.card * ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < R).card : ℝ)) := by
  have hC : C.Nonempty := ⟨0, h0⟩
  have hneg : ∀ a ∈ C, -a ∈ C := fun a ha => by
    have h := hsmul (-1) a ha
    rwa [neg_one_smul] at h
  have hOinv : ∀ g : (ι → F) → ℝ, (∀ a ∈ C, ∀ x, g (x + a) = g x) →
      marginalOracle β k g = marginalOracle β k (0 : (ι → F) → ℝ) := fun g hg =>
    marginalOracle_eq_of_invariant C h0 hadd hsmul k hdist β g hg
  have hcorr' : ∀ g : (ι → F) → ℝ,
      (HammingLip c g ∧ marginalOracle β k g = marginalOracle β k (0 : (ι → F) → ℝ)) →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
        |(alg ω (marginalOracle β k (0 : (ι → F) → ℝ))).output g - logZ β g| ≤ ε / 2), P ω := by
    rintro g ⟨hg, hO⟩
    have h := hcorr g hg
    rw [hO] at h
    exact h
  have hu : 0 ≤ β * c := mul_nonneg hβ hc
  have key := MetricChain.nonadaptive_expected_queries_ge
    (G := fun g : (ι → F) → ℝ =>
      HammingLip c g ∧ marginalOracle β k g = marginalOracle β k (0 : (ι → F) → ℝ))
    (Φ := logZ β) (fun ω => alg ω (marginalOracle β k (0 : (ι → F) → ℝ))) P hP hP1 hcorr'
    (fun ω => Q ω (marginalOracle β k (0 : (ι → F) → ℝ))) (fun ω g => hna ω _ g)
    (fun s x => c * distToCoset C hC s x) (fun s x => c * max (distToCoset C hC s x) R)
    (fun s => ⟨cone_lip C hC hc s, hOinv _ fun b hb x => by
      show c * distToCoset C hC s (x + b) = c * distToCoset C hC s x
      rw [distToCoset_add_mem C hC hadd hneg s x b hb]⟩)
    (fun s => ⟨flat_lip C hC hc R s, hOinv _ fun b hb x => by
      show c * max (distToCoset C hC s (x + b)) R = c * max (distToCoset C hC s x) R
      rw [distToCoset_add_mem C hC hadd hneg s x b hb]⟩)
    (fun s => by
      have hsep := separation_distToCoset C hC h0 s hu R
      have e1 : pSum (β * c) (fun x : ι → F => (hammingDist x s : ℝ)) =
          pSum (β * c) (fun x : ι → F => (hammingNorm x : ℝ)) :=
        pSum_hammingDist_shift (β * c) (fun t => t) s
      have e2 : pSum (β * c) (fun x : ι → F => max (hammingDist x s : ℝ) R) =
          pSum (β * c) (fun x : ι → F => max (hammingNorm x : ℝ) R) :=
        pSum_hammingDist_shift (β * c) (fun t => max t R) s
      rw [e1, e2] at hsep
      have e3 : logZ β (fun x => c * distToCoset C hC s x) =
          Real.log (pSum (β * c) (distToCoset C hC s)) := logZ_mul β c _
      have e4 : logZ β (fun x => c * max (distToCoset C hC s x) R) =
          Real.log (pSum (β * c) (fun x => max (distToCoset C hC s x) R)) := logZ_mul β c _
      rw [abs_sub_comm]
      refine lt_of_lt_of_le ?_ (le_abs_self _)
      show ε < logZ β (fun x => c * distToCoset C hC s x) -
        logZ β (fun x => c * max (distToCoset C hC s x) R)
      rw [e3, e4]
      linarith)
    (fun _ => (1 : ℝ)) (fun _ => zero_le_one)
    (B := C.card * ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < R).card : ℝ))
    (fun x => by
      rw [Finset.sum_const, nsmul_eq_mul, mul_one]
      refine le_trans ?_ (card_centres_near C hC x R)
      refine Nat.cast_le.mpr (Finset.card_le_card fun s hs => ?_)
      have hs' := (Finset.mem_filter.mp hs).2
      refine Finset.mem_filter.mpr ⟨Finset.mem_univ s, ?_⟩
      by_contra hnot
      apply hs'
      show c * max (distToCoset C hC s x) R = c * distToCoset C hC s x
      rw [max_eq_left (not_lt.mp hnot)])
  have hcard : ∑ _j : ι → F, (1 : ℝ) = (Fintype.card F : ℝ) ^ Fintype.card ι := by
    rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one, Fintype.card_fun,
      Nat.cast_pow]
  have key' : (1 - 2 * δ) * ∑ _j : ι → F, (1 : ℝ) ≤
      (∑ ω, P ω * (Q ω (marginalOracle β k 0)).card) *
        (C.card * ((univ.filter fun y : ι → F => (hammingNorm y : ℝ) < R).card : ℝ)) := key
  rw [hcard] at key'
  exact key'

end Cube

/-! ### The binary cube `F₂ⁿ`

Over `ZMod 2` a linear code is a set containing `0` and closed under addition. -/

section BinaryCube

theorem smul_mem_of_binary {n : ℕ} (C : Finset (Fin n → ZMod 2))
    (h0 : (0 : Fin n → ZMod 2) ∈ C) : ∀ (t : ZMod 2), ∀ a ∈ C, t • a ∈ C := by
  intro t a ha
  rcases (by decide : ∀ t : ZMod 2, t = 0 ∨ t = 1) t with rfl | rfl
  · rw [zero_smul]
    exact h0
  · rw [one_smul]
    exact ha

open Classical in
/-- **Theorem 4 on the binary cube**, as in the note:
`(1 - 2δ) · 2ⁿ ≤ E[number of evaluations at g ≡ 0] · |C| · V(n, r)`. -/
theorem theorem4_binary_cube {n : ℕ} (C : Finset (Fin n → ZMod 2))
    (h0 : (0 : Fin n → ZMod 2) ∈ C) (hadd : ∀ a ∈ C, ∀ b ∈ C, a + b ∈ C) (k : ℕ)
    (hdist : ∀ u : Fin n → ZMod 2, u ≠ 0 → (∀ a ∈ C, ∑ i, u i * a i = 0) → k < hammingNorm u)
    {β c : ℝ} (hβ : 0 ≤ β) (hc : 0 ≤ c) (r : ℝ) {ε δ : ℝ} {Ω : Type*} [Fintype Ω]
    (alg : Ω → (Finset (Fin n) → (Fin n → ZMod 2) → ℝ) →
      MetricChain.QueryAlgorithm (Fin n → ZMod 2))
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    (hcorr : ∀ g : (Fin n → ZMod 2) → ℝ, HammingLip c g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
        |(alg ω (marginalOracle β k g)).output g - logZ β g| ≤ ε / 2), P ω)
    (hsens : ε < logZ β (dipAt c r (0 : Fin n → ZMod 2)) -
      logZ β (0 : (Fin n → ZMod 2) → ℝ)) :
    (1 - 2 * δ) * 2 ^ n ≤
      (∑ ω, P ω * ((alg ω (marginalOracle β k 0)).queries 0).card) *
        (C.card * ((univ.filter fun y : Fin n → ZMod 2 => (hammingNorm y : ℝ) < r).card : ℝ)) := by
  have h := theorem4_adaptive_marginal_oracle C h0 hadd (smul_mem_of_binary C h0) k hdist hβ hc r
    alg P hP hP1 hcorr hsens
  rw [ZMod.card 2, Fintype.card_fin] at h
  exact_mod_cast h

open Classical in
/-- **Theorem 4′ on the binary cube**, as in the note:
`(1 - 2δ) · 2ⁿ ≤ E[number of evaluations] · |C| · |B(R - 1)|` whenever `ε < D_R - log |C|`. -/
theorem theorem4'_binary_cube {n : ℕ} (C : Finset (Fin n → ZMod 2))
    (h0 : (0 : Fin n → ZMod 2) ∈ C) (hadd : ∀ a ∈ C, ∀ b ∈ C, a + b ∈ C) (k : ℕ)
    (hdist : ∀ u : Fin n → ZMod 2, u ≠ 0 → (∀ a ∈ C, ∑ i, u i * a i = 0) → k < hammingNorm u)
    {β c : ℝ} (hβ : 0 ≤ β) (hc : 0 ≤ c) (R : ℝ) {ε δ : ℝ} {Ω : Type*} [Fintype Ω]
    (alg : Ω → (Finset (Fin n) → (Fin n → ZMod 2) → ℝ) →
      MetricChain.QueryAlgorithm (Fin n → ZMod 2))
    (Q : Ω → (Finset (Fin n) → (Fin n → ZMod 2) → ℝ) → Finset (Fin n → ZMod 2))
    (hna : ∀ ω o g, (alg ω o).queries g = Q ω o)
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    (hcorr : ∀ g : (Fin n → ZMod 2) → ℝ, HammingLip c g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
        |(alg ω (marginalOracle β k g)).output g - logZ β g| ≤ ε / 2), P ω)
    (hsens : ε < Real.log (pSum (β * c) (fun x : Fin n → ZMod 2 => (hammingNorm x : ℝ)) /
        pSum (β * c) (fun x : Fin n → ZMod 2 => max (hammingNorm x : ℝ) R)) -
      Real.log C.card) :
    (1 - 2 * δ) * 2 ^ n ≤
      (∑ ω, P ω * (Q ω (marginalOracle β k 0)).card) *
        (C.card * ((univ.filter fun y : Fin n → ZMod 2 => (hammingNorm y : ℝ) < R).card : ℝ)) := by
  have h := theorem4'_nonadaptive_marginal_oracle C h0 hadd (smul_mem_of_binary C h0) k hdist
    hβ hc R alg Q hna P hP hP1 hcorr hsens
  rw [ZMod.card 2, Fintype.card_fin] at h
  exact_mod_cast h

end BinaryCube

end ScienceL1

end

#print axioms ScienceL1.card_centres_near
#print axioms ScienceL1.marginalOracle_eq_of_invariant
#print axioms ScienceL1.marginalOracle_singleton
#print axioms ScienceL1.theorem4_adaptive_marginal_oracle
#print axioms ScienceL1.theorem4'_nonadaptive_marginal_oracle
#print axioms ScienceL1.theorem4_binary_cube
#print axioms ScienceL1.theorem4'_binary_cube
