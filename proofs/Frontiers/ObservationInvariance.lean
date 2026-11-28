import Mathlib
import proofs.Frontiers.QueryLowerBound
import proofs.Frontiers.NonAdaptive

/-!
# Phase II: observation oracles — the machine-checked cores

Source: `docs/phase2/PHASE2_REPORT.md` (Theorems A, A″, B, C; Lemmas 2.1–2.4, 2.6, 3.1, 3.2).

An *observation oracle* gives an algorithm, besides evaluations of the residual, information
about the normalised ensemble.  The report proves that such information changes the query
complexity of a certified free energy by at most an explicit factor.  This file checks the
parts of those proofs that are not probability theory:

* Part 1 — **indistinguishability with a tolerant oracle** (`tolerant_oracle_packing`,
  `tolerant_oracle_packing_nonadaptive`).  The oracle is a *relation* `valid g o` ("the answer
  `o` is admissible for the instance `g`"; for a tolerance `τ`: every reported mean is within `τ`
  of the true one), the algorithm must be correct for every instance and every admissible
  answer, and the bound counts the alternatives for which the answer given at the baseline is
  admissible as well.  For a functional oracle this is the science division's `lemma1a`,
  `lemma1b` (`OracleLowerBound.lean`).
* Part 2 — **the admissible cone** `LogLip u d` (weights `w > 0` with
  `w x ≤ e^{u d(x,y)} w y`): closed under isometries, convex combinations and maxima; cones
  `H e^{−u d(·,c)}` and dips `max(1, H e^{−u d(·,c)})` belong to it.
* Part 3 — **mixtures**: the partition function of a convex combination is the combination of
  the partition functions; if the members have equal partition functions the normalised ensemble
  of the combination is the combination of the ensembles; translations preserve the uniform
  partition function and transport the ensemble; the average over a simply transitive family of
  translations is constant.
* Part 4 — **the flat mixture** (`flat_mixture`, `hiding_law_sum`, `flat_mixture_truncated`):
  for *any* reference measure `π` and any kernel with constant row sums, the cones scaled to
  equal `π`-mass and mixed with the law `q(c) ∝ E_π K(·,c)` add up to a constant.
* Part 5 — **exact observables**: a weight invariant under a translation `c₀` has no component
  along a character with `χ(c₀) ≠ 1` (`sum_mul_char_eq_zero`), hence reproduces the uniform
  mean of every observable whose spectrum avoids the annihilator (`ensemble_mean_eq_of_spectrum`);
  the counting form of the union bound (`exists_separating_tuple`): `M < 2^r` balanced
  predicates are all separated by some `r`-tuple; parities on the cube are balanced
  (`parity_balanced`), so `r` translations with `2^r > M` kill `M` prescribed Walsh
  frequencies (`exists_generators_cube`).
* Part 6 — **Hoeffding for independent translations** (`hoeffding_iid_mean`): the form of
  Mathlib's Hoeffding inequality used in the report, for the coordinates of a product measure.

* Part 7 — **cores of the upper bounds**: relative accuracy gives logarithmic accuracy
  (`abs_log_le_of_abs_sub_one_le`); the random-cell estimator of Theorem C (b) and of the full
  oracle (`random_cell_failure_le`); Chebyshev's inequality for the mean of independent draws —
  the probabilistic core of plain Monte Carlo, theory report Theorem 11.44 (`chebyshev_iid_mean`).

Nothing is assumed: no statement of the report enters as a hypothesis.  What is *not* here: the
passage from these cores to exponents (binomial asymptotics), the bound on the relative variance
of the class, and the nested adaptive algorithm.
-/

set_option autoImplicit false

noncomputable section

namespace MetricChain

open Finset

/-! # Part 1: indistinguishability with a tolerant oracle -/

section TolerantOracle

open Classical in
/-- **Tolerant-oracle packing bound (adaptive algorithms).**  `valid g o`: the answer `o` is
admissible for the instance `g`.  An oracle algorithm is a family `alg ω o` of query algorithms;
it is `(ε/2, δ)`-correct if for every instance of the class and *every* admissible answer its
output is within `ε/2` of the target with probability at least `1 − δ`.  Let `o₀` be admissible
for the baseline `g₀`, and let `alt j` be alternatives; call `j` *good* if `alt j` is in the
class, `o₀` is admissible for it as well, and its target differs from that of `g₀` by more than
`ε`.  If every point lies in difference sets `{alt j ≠ g₀}` of total weight at most `B`, then
`(1 − 2δ) · (weight of the good alternatives) ≤ E[#evaluations at g₀ with the answer o₀] · B`. -/
theorem tolerant_oracle_packing {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (valid : (X → ℝ) → Θ → Prop) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g o, G g → valid g o →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω o).output g - Φ g| ≤ ε / 2), P ω)
    {g₀ : X → ℝ} (hg₀ : G g₀) {o₀ : Θ} (ho₀ : valid g₀ o₀)
    {J : Type*} [Fintype J] (alt : J → X → ℝ) (good : J → Prop)
    (halt : ∀ j, good j → G (alt j)) (hO : ∀ j, good j → valid (alt j) o₀)
    (hsens : ∀ j, good j → ε < |Φ (alt j) - Φ g₀|) (wgt : J → ℝ) (hwgt : ∀ j, 0 ≤ wgt j)
    {B : ℝ} (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => alt j a ≠ g₀ a), wgt j ≤ B) :
    (1 - 2 * δ) * ∑ j ∈ univ.filter good, wgt j ≤
      (∑ ω, P ω * ((alg ω o₀).queries g₀).card) * B := by
  have hcorr' : ∀ g : X → ℝ, (G g ∧ valid g o₀) →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω o₀).output g - Φ g| ≤ ε / 2), P ω :=
    fun g hg => hcorr g o₀ hg.1 hg.2
  have hcap' : ∀ a, ∑ j ∈ (univ : Finset {j // good j}).filter (fun j => alt j.1 a ≠ g₀ a),
      wgt j.1 ≤ B := by
    intro a
    have h1 : ∑ j ∈ (univ : Finset {j // good j}).filter (fun j => alt j.1 a ≠ g₀ a), wgt j.1 =
        ∑ j ∈ ((univ : Finset {j // good j}).filter (fun j => alt j.1 a ≠ g₀ a)).map
          (Function.Embedding.subtype good), wgt j := by
      rw [Finset.sum_map]
      rfl
    rw [h1]
    refine le_trans (Finset.sum_le_sum_of_subset_of_nonneg ?_ (fun j _ _ => hwgt j)) (hcap a)
    intro j hj
    rw [Finset.mem_map] at hj
    obtain ⟨j', hj', rfl⟩ := hj
    rw [Finset.mem_filter] at hj' ⊢
    exact ⟨Finset.mem_univ _, hj'.2⟩
  have key := expected_queries_ge_packing (G := fun g => G g ∧ valid g o₀) (Φ := Φ)
    (fun ω => alg ω o₀) P hP hP1 hcorr' (g := g₀) ⟨hg₀, ho₀⟩
    (fun j : {j // good j} => alt j.1) (fun j => ⟨halt j.1 j.2, hO j.1 j.2⟩)
    (fun j => hsens j.1 j.2) (fun j => wgt j.1) (fun j => hwgt j.1) (B := B) hcap'
  have h2 : ∑ j : {j // good j}, wgt j.1 = ∑ j ∈ univ.filter good, wgt j := by
    rw [← Finset.sum_subtype_eq_sum_filter, Finset.subtype_univ]
  rwa [h2] at key

open Classical in
/-- **Tolerant-oracle packing bound (non-adaptive algorithms).**  The evaluation points `Q ω o`
may depend on the seed and on the oracle's answer, not on the instance.  Pairs `(g j, g' j)`;
`j` is *good* if both members are in the class, the *same* answer `o₀` is admissible for both,
and their targets differ by more than `ε`.  Then
`(1 − 2δ) · (weight of the good pairs) ≤ E[#evaluations with the answer o₀] · B`. -/
theorem tolerant_oracle_packing_nonadaptive {X Θ : Type*} {G : (X → ℝ) → Prop}
    {Φ : (X → ℝ) → ℝ} (valid : (X → ℝ) → Θ → Prop) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g o, G g → valid g o →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω o).output g - Φ g| ≤ ε / 2), P ω)
    (Q : Ω → Θ → Finset X) (hna : ∀ ω o g, (alg ω o).queries g = Q ω o) (o₀ : Θ)
    {J : Type*} [Fintype J] (g g' : J → X → ℝ) (good : J → Prop)
    (hg : ∀ j, good j → G (g j)) (hg' : ∀ j, good j → G (g' j))
    (hO : ∀ j, good j → valid (g j) o₀) (hO' : ∀ j, good j → valid (g' j) o₀)
    (hsens : ∀ j, good j → ε < |Φ (g' j) - Φ (g j)|) (wgt : J → ℝ) (hwgt : ∀ j, 0 ≤ wgt j)
    {B : ℝ} (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => g' j a ≠ g j a), wgt j ≤ B) :
    (1 - 2 * δ) * ∑ j ∈ univ.filter good, wgt j ≤ (∑ ω, P ω * (Q ω o₀).card) * B := by
  have hcorr' : ∀ f : X → ℝ, (G f ∧ valid f o₀) →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω o₀).output f - Φ f| ≤ ε / 2), P ω :=
    fun f hf => hcorr f o₀ hf.1 hf.2
  have hcap' : ∀ a, ∑ j ∈ (univ : Finset {j // good j}).filter (fun j => g' j.1 a ≠ g j.1 a),
      wgt j.1 ≤ B := by
    intro a
    have h1 : ∑ j ∈ (univ : Finset {j // good j}).filter (fun j => g' j.1 a ≠ g j.1 a),
        wgt j.1 =
        ∑ j ∈ ((univ : Finset {j // good j}).filter (fun j => g' j.1 a ≠ g j.1 a)).map
          (Function.Embedding.subtype good), wgt j := by
      rw [Finset.sum_map]
      rfl
    rw [h1]
    refine le_trans (Finset.sum_le_sum_of_subset_of_nonneg ?_ (fun j _ _ => hwgt j)) (hcap a)
    intro j hj
    rw [Finset.mem_map] at hj
    obtain ⟨j', hj', rfl⟩ := hj
    rw [Finset.mem_filter] at hj' ⊢
    exact ⟨Finset.mem_univ _, hj'.2⟩
  have key := nonadaptive_expected_queries_ge (G := fun f => G f ∧ valid f o₀) (Φ := Φ)
    (fun ω => alg ω o₀) P hP hP1 hcorr' (fun ω => Q ω o₀) (fun ω f => hna ω o₀ f)
    (fun j : {j // good j} => g j.1) (fun j : {j // good j} => g' j.1)
    (fun j => ⟨hg j.1 j.2, hO j.1 j.2⟩) (fun j => ⟨hg' j.1 j.2, hO' j.1 j.2⟩)
    (fun j => hsens j.1 j.2) (fun j => wgt j.1) (fun j => hwgt j.1) (B := B) hcap'
  have h2 : ∑ j : {j // good j}, wgt j.1 = ∑ j ∈ univ.filter good, wgt j := by
    rw [← Finset.sum_subtype_eq_sum_filter, Finset.subtype_univ]
  rwa [h2] at key

end TolerantOracle

/-! # Part 2: the admissible cone -/

section Cone

variable {X : Type*}

/-- Admissible weights: positive, and `w x ≤ e^{u d(x,y)} w y` for all `x, y`. -/
def LogLip (u : ℝ) (d : X → X → ℝ) (w : X → ℝ) : Prop :=
  (∀ x, 0 < w x) ∧ ∀ x y, w x ≤ Real.exp (u * d x y) * w y

/-- A positive constant is admissible. -/
theorem LogLip.const {u : ℝ} {d : X → X → ℝ} (hu : 0 ≤ u) (hd : ∀ x y, 0 ≤ d x y) {c : ℝ}
    (hc : 0 < c) : LogLip u d (fun _ => c) := by
  refine ⟨fun _ => hc, fun x y => ?_⟩
  have h1 : (1 : ℝ) ≤ Real.exp (u * d x y) := Real.one_le_exp (mul_nonneg hu (hd x y))
  nlinarith

/-- The cone is invariant under maps that preserve `d` (translations of the cube, permutations
of the coordinates). -/
theorem LogLip.comp_isometry {u : ℝ} {d : X → X → ℝ} {w : X → ℝ} (hw : LogLip u d w)
    (σ : X → X) (hσ : ∀ x y, d (σ x) (σ y) = d x y) : LogLip u d (fun x => w (σ x)) :=
  ⟨fun x => hw.1 (σ x), fun x y => by simpa [hσ] using hw.2 (σ x) (σ y)⟩

/-- The cone is convex: a convex combination of admissible weights is admissible. -/
theorem LogLip.convex_comb {u : ℝ} {d : X → X → ℝ} {J : Type*} (s : Finset J) (lam : J → ℝ)
    (W : J → X → ℝ) (hlam : ∀ j ∈ s, 0 ≤ lam j) (hsum : ∑ j ∈ s, lam j = 1)
    (hW : ∀ j ∈ s, LogLip u d (W j)) : LogLip u d (fun x => ∑ j ∈ s, lam j * W j x) := by
  refine ⟨fun x => ?_, fun x y => ?_⟩
  · have hne : ∃ j ∈ s, 0 < lam j := by
      by_contra hcon
      have hcon' : ∀ j ∈ s, lam j ≤ 0 := fun j hj => not_lt.mp fun h => hcon ⟨j, hj, h⟩
      have h0 : ∑ j ∈ s, lam j = 0 :=
        Finset.sum_eq_zero fun j hj => le_antisymm (hcon' j hj) (hlam j hj)
      rw [h0] at hsum
      exact zero_ne_one hsum
    obtain ⟨j, hj, hpos⟩ := hne
    exact Finset.sum_pos' (fun i hi => mul_nonneg (hlam i hi) ((hW i hi).1 x).le)
      ⟨j, hj, mul_pos hpos ((hW j hj).1 x)⟩
  · rw [Finset.mul_sum]
    refine Finset.sum_le_sum fun j hj => ?_
    have h := (hW j hj).2 x y
    calc lam j * W j x ≤ lam j * (Real.exp (u * d x y) * W j y) :=
          mul_le_mul_of_nonneg_left h (hlam j hj)
      _ = Real.exp (u * d x y) * (lam j * W j y) := by ring

/-- The pointwise maximum of two admissible weights is admissible. -/
theorem LogLip.max {u : ℝ} {d : X → X → ℝ} {w₁ w₂ : X → ℝ} (h₁ : LogLip u d w₁)
    (h₂ : LogLip u d w₂) : LogLip u d (fun x => Max.max (w₁ x) (w₂ x)) := by
  refine ⟨fun x => lt_max_of_lt_left (h₁.1 x), fun x y => ?_⟩
  have he : 0 ≤ Real.exp (u * d x y) := (Real.exp_pos _).le
  refine max_le ?_ ?_
  · exact (h₁.2 x y).trans (mul_le_mul_of_nonneg_left (le_max_left _ _) he)
  · exact (h₂.2 x y).trans (mul_le_mul_of_nonneg_left (le_max_right _ _) he)

/-- The maximum of a nonempty finite family of admissible weights is admissible (a landscape of
several dips). -/
theorem LogLip.sup' {u : ℝ} {d : X → X → ℝ} {J : Type*} (s : Finset J) (hs : s.Nonempty)
    (W : J → X → ℝ) (hW : ∀ j ∈ s, LogLip u d (W j)) :
    LogLip u d (fun x => s.sup' hs (fun j => W j x)) := by
  refine ⟨fun x => ?_, fun x y => ?_⟩
  · obtain ⟨j, hj⟩ := hs
    exact lt_of_lt_of_le ((hW j hj).1 x) (Finset.le_sup' (fun j => W j x) hj)
  · have he : 0 ≤ Real.exp (u * d x y) := (Real.exp_pos _).le
    refine Finset.sup'_le hs _ fun j hj => ?_
    exact ((hW j hj).2 x y).trans
      (mul_le_mul_of_nonneg_left (Finset.le_sup' (fun j => W j y) hj) he)

/-- A cone `H e^{−u d(·,c)}` is admissible when `d` is symmetric and satisfies the triangle
inequality. -/
theorem LogLip.cone {u : ℝ} {d : X → X → ℝ} (hu : 0 ≤ u) (hsymm : ∀ x y, d x y = d y x)
    (htri : ∀ x y z, d x z ≤ d x y + d y z) {H : ℝ} (hH : 0 < H) (c : X) :
    LogLip u d (fun x => H * Real.exp (-(u * d x c))) := by
  refine ⟨fun x => mul_pos hH (Real.exp_pos _), fun x y => ?_⟩
  have h1 : -(u * d x c) ≤ u * d x y + -(u * d y c) := by
    have h2 : d y c ≤ d y x + d x c := htri y x c
    rw [hsymm y x] at h2
    nlinarith [mul_le_mul_of_nonneg_left h2 hu]
  calc H * Real.exp (-(u * d x c)) ≤ H * Real.exp (u * d x y + -(u * d y c)) :=
        mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr h1) hH.le
    _ = Real.exp (u * d x y) * (H * Real.exp (-(u * d y c))) := by
        rw [Real.exp_add]; ring

/-- A dip `max(1, H e^{−u d(·,c)})` is admissible. -/
theorem LogLip.dip {u : ℝ} {d : X → X → ℝ} (hu : 0 ≤ u) (hd : ∀ x y, 0 ≤ d x y)
    (hsymm : ∀ x y, d x y = d y x) (htri : ∀ x y z, d x z ≤ d x y + d y z) {H : ℝ} (hH : 0 < H)
    (c : X) : LogLip u d (fun x => Max.max 1 (H * Real.exp (-(u * d x c)))) :=
  LogLip.max (LogLip.const hu hd one_pos) (LogLip.cone hu hsymm htri hH c)

/-- A dip equals `1` exactly where the cone is at most `1`. -/
theorem dip_eq_one_iff {H e : ℝ} : Max.max 1 (H * e) = 1 ↔ H * e ≤ 1 := max_eq_left_iff

end Cone

/-! # Part 3: partition functions and ensembles of mixtures -/

section Mixtures

variable {X : Type*} [Fintype X]

/-- The partition function `A_π(w) = Σ_x π(x) w(x)` of a weight against a reference `π`. -/
def massOf (π w : X → ℝ) : ℝ := ∑ x, π x * w x

/-- The mean of the observable `φ` in the normalised ensemble `w π / A_π(w)`. -/
def ensOf (π w φ : X → ℝ) : ℝ := (∑ x, π x * w x * φ x) / massOf π w

theorem massOf_convex_comb (π : X → ℝ) {J : Type*} (s : Finset J) (lam : J → ℝ)
    (W : J → X → ℝ) :
    massOf π (fun x => ∑ j ∈ s, lam j * W j x) = ∑ j ∈ s, lam j * massOf π (W j) := by
  unfold massOf
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun x _ => by ring

/-- **Averaging preserves the partition function**: a convex combination of weights with the
same partition function `A` has partition function `A`. -/
theorem massOf_convex_comb_eq (π : X → ℝ) {J : Type*} (s : Finset J) (lam : J → ℝ)
    (W : J → X → ℝ) {A : ℝ} (hA : ∀ j ∈ s, massOf π (W j) = A) (hsum : ∑ j ∈ s, lam j = 1) :
    massOf π (fun x => ∑ j ∈ s, lam j * W j x) = A := by
  rw [massOf_convex_comb, Finset.sum_congr rfl fun j hj => by rw [hA j hj], ← Finset.sum_mul,
    hsum, one_mul]

/-- **The ensemble of an average is the average of the ensembles** (members with equal
partition functions). -/
theorem ensOf_convex_comb (π φ : X → ℝ) {J : Type*} (s : Finset J) (lam : J → ℝ)
    (W : J → X → ℝ) {A : ℝ} (hA : ∀ j ∈ s, massOf π (W j) = A) (hsum : ∑ j ∈ s, lam j = 1) :
    ensOf π (fun x => ∑ j ∈ s, lam j * W j x) φ = ∑ j ∈ s, lam j * ensOf π (W j) φ := by
  unfold ensOf
  rw [massOf_convex_comb_eq π s lam W hA hsum]
  have h1 : ∑ x, π x * (∑ j ∈ s, lam j * W j x) * φ x =
      ∑ j ∈ s, lam j * ∑ x, π x * W j x * φ x := by
    simp_rw [Finset.mul_sum, Finset.sum_mul]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun x _ => by ring
  rw [h1, Finset.sum_div]
  refine Finset.sum_congr rfl fun j hj => ?_
  rw [hA j hj, mul_div_assoc]

/-- A bijection that preserves the reference preserves the partition function. -/
theorem massOf_comp_equiv (π w : X → ℝ) (σ : X ≃ X) (hπ : ∀ x, π (σ x) = π x) :
    massOf π (fun x => w (σ x)) = massOf π w := by
  unfold massOf
  rw [← Equiv.sum_comp σ (fun x => π x * w x)]
  exact Finset.sum_congr rfl fun x _ => by rw [hπ x]

/-- ... and transports the ensemble: the mean of `φ` in the translated ensemble is the mean of
the back-translated observable in the original one. -/
theorem ensOf_comp_equiv (π w φ : X → ℝ) (σ : X ≃ X) (hπ : ∀ x, π (σ x) = π x) :
    ensOf π (fun x => w (σ x)) φ = ensOf π w (fun x => φ (σ.symm x)) := by
  unfold ensOf
  rw [massOf_comp_equiv π w σ hπ]
  congr 1
  rw [← Equiv.sum_comp σ (fun x => π x * w x * φ (σ.symm x))]
  exact Finset.sum_congr rfl fun x _ => by rw [hπ x, Equiv.symm_apply_apply]

/-- **The average over a simply transitive family of translations is constant**: if for every
`x` the map `c ↦ T c x` is a bijection of the index set onto the space, then
`Σ_c w(T c x) = Σ_y w(y)` for every `x`. -/
theorem sum_translates_eq {C : Type*} [Fintype C] (T : C → X → X)
    (hT : ∀ x, Function.Bijective fun c => T c x) (w : X → ℝ) (x : X) :
    ∑ c, w (T c x) = ∑ y, w y :=
  Function.Bijective.sum_comp (hT x) w

end Mixtures

/-! # Part 4: the flat mixture -/

section FlatMixture

variable {X C : Type*} [Fintype X] [Fintype C]

/-- The `π`-mass of the kernel column `c`: `m(c) = Σ_x π(x) K(x,c)`. -/
def colMass (π : X → ℝ) (K : X → C → ℝ) (c : C) : ℝ := ∑ x, π x * K x c

/-- **The hiding law is a probability vector.**  If the kernel has constant row sums `S₀` and
`π` has total mass one, then `q(c) = m(c)/S₀` sums to one. -/
theorem hiding_law_sum (π : X → ℝ) (K : X → C → ℝ) {S₀ : ℝ} (hS₀ : S₀ ≠ 0)
    (hrow : ∀ x, ∑ c, K x c = S₀) (hπ : ∑ x, π x = 1) :
    ∑ c, colMass π K c / S₀ = 1 := by
  rw [← Finset.sum_div]
  have h : ∑ c, colMass π K c = S₀ := by
    unfold colMass
    rw [Finset.sum_comm]
    have h2 : ∀ x, ∑ c, π x * K x c = π x * S₀ := fun x => by rw [← Finset.mul_sum, hrow x]
    rw [Finset.sum_congr rfl fun x _ => h2 x, ← Finset.sum_mul, hπ, one_mul]
  rw [h, div_self hS₀]

/-- **The flat mixture.**  Scale every cone `K(·,c)` to `π`-mass `ε₀` (height
`H(c) = ε₀/m(c)`) and mix with the hiding law `q(c) = m(c)/S₀`: the mixture is the constant
`ε₀`, at every point, for every reference measure. -/
theorem flat_mixture (π : X → ℝ) (K : X → C → ℝ) {S₀ : ℝ} (hS₀ : S₀ ≠ 0)
    (hrow : ∀ x, ∑ c, K x c = S₀) (hm : ∀ c, colMass π K c ≠ 0) (ε₀ : ℝ) (x : X) :
    ∑ c, colMass π K c / S₀ * (ε₀ / colMass π K c * K x c) = ε₀ := by
  have h : ∀ c, colMass π K c / S₀ * (ε₀ / colMass π K c * K x c) = ε₀ / S₀ * K x c := by
    intro c
    field_simp [hm c]
  rw [Finset.sum_congr rfl fun c _ => h c, ← Finset.mul_sum, hrow x, div_mul_cancel₀ _ hS₀]

/-- The same for the truncated members `max(1, H(c) K(·,c))` (the dips): their mixture is
`1 + ε₀ −` the truncation defect `Σ_c q(c) min(1, H(c) K(x,c))`. -/
theorem flat_mixture_truncated (π : X → ℝ) (K : X → C → ℝ) {S₀ : ℝ} (hS₀ : S₀ ≠ 0)
    (hrow : ∀ x, ∑ c, K x c = S₀) (hm : ∀ c, colMass π K c ≠ 0) (hπ : ∑ x, π x = 1) (ε₀ : ℝ)
    (x : X) :
    ∑ c, colMass π K c / S₀ * Max.max 1 (ε₀ / colMass π K c * K x c) =
      1 + ε₀ - ∑ c, colMass π K c / S₀ * Min.min 1 (ε₀ / colMass π K c * K x c) := by
  have h : ∀ c, colMass π K c / S₀ * Max.max 1 (ε₀ / colMass π K c * K x c) =
      colMass π K c / S₀ + colMass π K c / S₀ * (ε₀ / colMass π K c * K x c) -
        colMass π K c / S₀ * Min.min 1 (ε₀ / colMass π K c * K x c) := by
    intro c
    have hmm := max_add_min (1 : ℝ) (ε₀ / colMass π K c * K x c)
    have : Max.max 1 (ε₀ / colMass π K c * K x c) =
        1 + ε₀ / colMass π K c * K x c - Min.min 1 (ε₀ / colMass π K c * K x c) := by linarith
    rw [this]; ring
  rw [Finset.sum_congr rfl fun c _ => h c, Finset.sum_sub_distrib, Finset.sum_add_distrib,
    hiding_law_sum π K hS₀ hrow hπ, flat_mixture π K hS₀ hrow hm ε₀ x]

end FlatMixture

/-! # Part 5: exact observables — characters and the counting form of the union bound -/

section Characters

variable {G : Type*} [Fintype G] [AddCommGroup G]

/-- **A weight invariant under a translation has no component along a character that the
translation moves.**  If `w(x + c₀) = w(x)` and `χ(x + c₀) = χ(x)·χ(c₀)` with `χ(c₀) ≠ 1`, then
`Σ_x w(x) χ(x) = 0`. -/
theorem sum_mul_char_eq_zero (w χ : G → ℝ) (c₀ : G) (hχ : ∀ x, χ (x + c₀) = χ x * χ c₀)
    (hc : χ c₀ ≠ 1) (hw : ∀ x, w (x + c₀) = w x) : ∑ x, w x * χ x = 0 := by
  have h1 : ∑ x, w x * χ x = ∑ x, w (x + c₀) * χ (x + c₀) :=
    (Equiv.sum_comp (Equiv.addRight c₀) (fun x => w x * χ x)).symm
  have h2 : ∑ x, w (x + c₀) * χ (x + c₀) = χ c₀ * ∑ x, w x * χ x := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun x _ => by rw [hw x, hχ x]; ring
  have h3 : (1 - χ c₀) * ∑ x, w x * χ x = 0 := by
    rw [sub_mul, one_mul, ← h2, ← h1, sub_self]
  rcases mul_eq_zero.mp h3 with h | h
  · exact absurd (sub_eq_zero.mp h).symm hc
  · exact h

/-- **Exact observables whose spectrum avoids the annihilator see nothing.**  Let
`φ = a₀ + Σ_{s ∈ S} a(s) χ_s` and let the weight `w` (with nonzero total mass) be invariant
under translations `gen s`, one for each `s ∈ S`, with `χ_s(gen s) ≠ 1`.  Then the mean of `φ`
in the normalised ensemble of `w` is `a₀` — its mean under the uniform measure. -/
theorem ensemble_mean_eq_of_spectrum {S : Type*} [Fintype S] (w : G → ℝ) (χ : S → G → ℝ)
    (a : S → ℝ) (a₀ : ℝ) (gen : S → G)
    (hχ : ∀ s x, χ s (x + gen s) = χ s x * χ s (gen s)) (hc : ∀ s, χ s (gen s) ≠ 1)
    (hw : ∀ s x, w (x + gen s) = w x) (hmass : ∑ x, w x ≠ 0) :
    (∑ x, w x * (a₀ + ∑ s, a s * χ s x)) / ∑ x, w x = a₀ := by
  have h1 : ∑ x, w x * (a₀ + ∑ s, a s * χ s x) = a₀ * ∑ x, w x := by
    have h2 : ∀ x, w x * (a₀ + ∑ s, a s * χ s x) = a₀ * w x + ∑ s, a s * (w x * χ s x) := by
      intro x
      rw [mul_add, Finset.mul_sum]
      congr 1
      · ring
      · exact Finset.sum_congr rfl fun s _ => by ring
    rw [Finset.sum_congr rfl fun x _ => h2 x, Finset.sum_add_distrib, ← Finset.mul_sum,
      Finset.sum_comm]
    have h3 : ∀ s, ∑ x, a s * (w x * χ s x) = 0 := fun s => by
      rw [← Finset.mul_sum, sum_mul_char_eq_zero w (χ s) (gen s) (hχ s) (hc s) (hw s), mul_zero]
    rw [Finset.sum_congr rfl fun s _ => h3 s, Finset.sum_const_zero, add_zero]
  rw [h1, mul_div_assoc, div_self hmass, mul_one]

end Characters

section Counting

/-- **The counting form of the union bound.**  Let `f s : V → Bool` be *balanced* predicates
(each is `false` on exactly half of `V`), one for each `s` in a set of fewer than `2^r`
elements.  Then some `r`-tuple `g` of points separates all of them: for every `s` some `g i` has
`f s (g i) = true`.  (For a fixed `s` a uniformly random tuple fails with probability `2^{-r}`.) -/
theorem exists_separating_tuple {V S : Type*} [Fintype V] [Fintype S] [Nonempty V]
    (f : S → V → Bool)
    (hbal : ∀ s, 2 * (univ.filter (fun v => f s v = false)).card = Fintype.card V)
    (r : ℕ) (hM : Fintype.card S < 2 ^ r) :
    ∃ g : Fin r → V, ∀ s, ∃ i, f s (g i) = true := by
  classical
  by_contra hcon0
  have hcon : ∀ g : Fin r → V, ∃ s, ∀ i, f s (g i) = false := by
    intro g
    by_contra hg
    refine hcon0 ⟨g, fun s => ?_⟩
    by_contra hs
    refine hg ⟨s, fun i => ?_⟩
    by_contra hi
    exact hs ⟨i, by simpa using hi⟩
  have hcover : (univ : Finset (Fin r → V)) ⊆ (univ : Finset S).biUnion
      (fun s => Fintype.piFinset (fun _ : Fin r => univ.filter (fun v => f s v = false))) := by
    intro g _
    obtain ⟨s, hs⟩ := hcon g
    rw [Finset.mem_biUnion]
    refine ⟨s, Finset.mem_univ s, ?_⟩
    rw [Fintype.mem_piFinset]
    intro i
    rw [Finset.mem_filter]
    refine ⟨Finset.mem_univ _, ?_⟩
    exact hs i
  have h1 := Finset.card_le_card hcover
  have h2 := Finset.card_biUnion_le (s := (univ : Finset S))
    (t := fun s => Fintype.piFinset (fun _ : Fin r => univ.filter (fun v => f s v = false)))
  have hV : 0 < Fintype.card V := Fintype.card_pos
  -- half of `V`
  obtain ⟨k, hk⟩ : ∃ k, Fintype.card V = 2 * k := by
    by_cases hS : Nonempty S
    · obtain ⟨s⟩ := hS
      exact ⟨_, (hbal s).symm⟩
    · -- `S` is empty: every tuple separates
      exfalso
      obtain ⟨s, _⟩ := hcon (fun _ => Classical.arbitrary V)
      exact hS ⟨s⟩
  have hkpos : 0 < k := by omega
  have hcard : ∀ s, (Fintype.piFinset (fun _ : Fin r =>
      univ.filter (fun v => f s v = false))).card = k ^ r := by
    intro s
    rw [Fintype.card_piFinset, Finset.prod_const, Finset.card_univ, Fintype.card_fin]
    have := hbal s
    congr 1
    omega
  rw [Finset.sum_congr rfl fun s _ => hcard s, Finset.sum_const, Finset.card_univ,
    smul_eq_mul] at h2
  have h3 : (univ : Finset (Fin r → V)).card = (2 * k) ^ r := by
    rw [Finset.card_univ, Fintype.card_fun, Fintype.card_fin, hk]
  rw [h3] at h1
  have h4 : (2 * k) ^ r ≤ Fintype.card S * k ^ r := h1.trans h2
  rw [mul_pow] at h4
  have h5 : Fintype.card S * k ^ r < 2 ^ r * k ^ r :=
    Nat.mul_lt_mul_of_pos_right hM (pow_pos hkpos r)
  omega

end Counting

/-! ## The cube `F₂ⁿ`: Walsh characters, parities, generators -/

section CubeWalsh

variable {n : ℕ}

/-- The Walsh character `χ_s(x) = (−1)^{s·x}` on `F₂ⁿ = Fin n → ZMod 2`. -/
def walsh (s x : Fin n → ZMod 2) : ℝ := if s ⬝ᵥ x = 0 then 1 else -1

theorem zmod2_cases (a : ZMod 2) : a = 0 ∨ a = 1 := by
  revert a
  decide

theorem walsh_add (s x c : Fin n → ZMod 2) : walsh s (x + c) = walsh s x * walsh s c := by
  unfold walsh
  rw [dotProduct_add]
  have h11 : (1 : ZMod 2) + 1 = 0 := by decide
  have h10 : (1 : ZMod 2) ≠ 0 := by decide
  rcases zmod2_cases (s ⬝ᵥ x) with h | h <;> rcases zmod2_cases (s ⬝ᵥ c) with h' | h' <;>
    simp [h, h', h11, h10]

theorem walsh_eq_neg_one {s c : Fin n → ZMod 2} (h : s ⬝ᵥ c = 1) : walsh s c = -1 := by
  unfold walsh
  have h10 : (1 : ZMod 2) ≠ 0 := by decide
  simp [h, h10]

/-- **Lemma 3.1 on the cube.**  A weight invariant under the translations `g i` has no Walsh
component at any frequency `s` that is not orthogonal to all of them. -/
theorem walsh_coeff_eq_zero_of_invariant {r : ℕ} (w : (Fin n → ZMod 2) → ℝ)
    (g : Fin r → Fin n → ZMod 2) (hw : ∀ i x, w (x + g i) = w x) (s : Fin n → ZMod 2)
    (hs : ∃ i, s ⬝ᵥ g i = 1) : ∑ x, w x * walsh s x = 0 := by
  obtain ⟨i, hi⟩ := hs
  refine sum_mul_char_eq_zero w (walsh s) (g i) (fun x => walsh_add s x (g i)) ?_ (hw i)
  rw [walsh_eq_neg_one hi]
  norm_num

/-- **Parities are balanced.**  For `s ≠ 0`, exactly half of the points `g` of the cube have
`s·g ≠ 1`. -/
theorem parity_balanced (s : Fin n → ZMod 2) (hs : s ≠ 0) :
    2 * (univ.filter (fun g : Fin n → ZMod 2 => decide (s ⬝ᵥ g = 1) = false)).card =
      Fintype.card (Fin n → ZMod 2) := by
  classical
  obtain ⟨i₀, hi₀⟩ : ∃ i, s i = 1 := by
    by_contra hcon
    apply hs
    funext i
    rcases zmod2_cases (s i) with h | h
    · simpa using h
    · exact absurd ⟨i, h⟩ hcon
  let e : Fin n → ZMod 2 := Pi.single i₀ 1
  have hdot : ∀ g : Fin n → ZMod 2, s ⬝ᵥ (g + e) = s ⬝ᵥ g + 1 := by
    intro g
    rw [dotProduct_add, dotProduct_single, hi₀, mul_one]
  have hinv : ∀ g : Fin n → ZMod 2, g + e + e = g := by
    intro g
    funext i
    have h2 : e i + e i = 0 := CharTwo.add_self_eq_zero (e i)
    simp only [Pi.add_apply]
    rw [add_assoc, h2, add_zero]
  have hflip : ∀ a : ZMod 2, decide (a + 1 = 1) = !decide (a = 1) := by decide
  have hcard : (univ.filter (fun g : Fin n → ZMod 2 => decide (s ⬝ᵥ g = 1) = false)).card =
      (univ.filter (fun g : Fin n → ZMod 2 => decide (s ⬝ᵥ g = 1) = true)).card := by
    refine Finset.card_nbij' (fun g => g + e) (fun g => g + e) ?_ ?_ ?_ ?_
    · intro g hg
      simp only [Finset.coe_filter, Finset.mem_univ, true_and, Set.mem_setOf_eq] at hg ⊢
      rw [hdot, hflip, hg]
      rfl
    · intro g hg
      simp only [Finset.coe_filter, Finset.mem_univ, true_and, Set.mem_setOf_eq] at hg ⊢
      rw [hdot, hflip, hg]
      rfl
    · intro g _
      exact hinv g
    · intro g _
      exact hinv g
  have hsplit := Finset.card_filter_add_card_filter_not
    (s := (univ : Finset (Fin n → ZMod 2))) (fun g => decide (s ⬝ᵥ g = 1) = false)
  have hneg : (univ.filter (fun g : Fin n → ZMod 2 => ¬ decide (s ⬝ᵥ g = 1) = false)) =
      univ.filter (fun g : Fin n → ZMod 2 => decide (s ⬝ᵥ g = 1) = true) := by
    refine Finset.filter_congr fun g _ => ?_
    simp
  rw [hneg, ← hcard, Finset.card_univ] at hsplit
  omega

/-- **Lemma 3.2 (a small set of generators avoiding `M` frequencies).**  For every set `S` of
fewer than `2^r` non-zero frequencies there are `g_1, …, g_r` such that every `s ∈ S` has
`s·g_i = 1` for some `i`. -/
theorem exists_generators_cube (S : Finset (Fin n → ZMod 2)) (h0 : ∀ s ∈ S, s ≠ 0) (r : ℕ)
    (hM : S.card < 2 ^ r) :
    ∃ g : Fin r → Fin n → ZMod 2, ∀ s ∈ S, ∃ i, s ⬝ᵥ g i = 1 := by
  classical
  have hM' : Fintype.card {s // s ∈ S} < 2 ^ r := by rwa [Fintype.card_coe]
  obtain ⟨g, hg⟩ := exists_separating_tuple
    (fun (s : {s // s ∈ S}) (v : Fin n → ZMod 2) => decide (s.1 ⬝ᵥ v = 1))
    (fun s => parity_balanced s.1 (h0 s.1 s.2)) r hM'
  refine ⟨g, fun s hs => ?_⟩
  obtain ⟨i, hi⟩ := hg ⟨s, hs⟩
  exact ⟨i, by simpa using hi⟩

/-- **Lemmas 3.1 and 3.2 together.**  For fewer than `2^r` prescribed non-zero frequencies
there are `r` translations such that *every* weight invariant under them has none of these
Walsh components — in particular the average of any weight over the subgroup (of at most `2^r`
elements) that they generate. -/
theorem exists_generators_kill (S : Finset (Fin n → ZMod 2)) (h0 : ∀ s ∈ S, s ≠ 0) (r : ℕ)
    (hM : S.card < 2 ^ r) :
    ∃ g : Fin r → Fin n → ZMod 2, ∀ w : (Fin n → ZMod 2) → ℝ,
      (∀ i x, w (x + g i) = w x) → ∀ s ∈ S, ∑ x, w x * walsh s x = 0 := by
  obtain ⟨g, hg⟩ := exists_generators_cube S h0 r hM
  exact ⟨g, fun w hw s hs => walsh_coeff_eq_zero_of_invariant w g hw s (hg s hs)⟩

end CubeWalsh

/-! # Part 6: Hoeffding's inequality for independent translations -/

section Hoeffding

open MeasureTheory ProbabilityTheory

/-- **Hoeffding's inequality in the form used in the report.**  Let `ν` be a probability
measure (the law of a random translation) and `Y` a measurable function with values in
`[a, b]` (the mean of an observable in the translated ensemble).  For `L` independent draws
`c_1, …, c_L` (the product measure on `Fin L → Ω₀`),
`P( Σ_j (Y(c_j) − E Y) ≥ t ) ≤ exp(−t² / (2 L ((b − a)/2)²))`.  With `t = L·τ` and `b − a = 2`
this is `exp(−L τ²/2)`; the two-sided bound is twice this (apply it to `−Y`). -/
theorem hoeffding_iid_mean {Ω₀ : Type*} [MeasurableSpace Ω₀] (ν : Measure Ω₀)
    [IsProbabilityMeasure ν] (Y : Ω₀ → ℝ) (hY : Measurable Y) {a b : ℝ}
    (hab : ∀ x, Y x ∈ Set.Icc a b) (L : ℕ) {t : ℝ} (ht : 0 ≤ t) :
    (Measure.pi fun _ : Fin L => ν).real
        {c | t ≤ ∑ j : Fin L, (Y (c j) - ∫ x, Y x ∂ν)} ≤
      Real.exp (-t ^ 2 / (2 * (L * ((b - a) / 2) ^ 2))) := by
  have hsub : HasSubgaussianMGF (fun x => Y x - ∫ x, Y x ∂ν) ((‖b - a‖₊ / 2) ^ 2) ν :=
    hasSubgaussianMGF_of_mem_Icc hY.aemeasurable (Filter.Eventually.of_forall hab)
  have hindep : iIndepFun (fun (j : Fin L) (c : Fin L → Ω₀) => Y (c j) - ∫ x, Y x ∂ν)
      (Measure.pi fun _ : Fin L => ν) :=
    iIndepFun_pi (X := fun (_ : Fin L) (x : Ω₀) => Y x - ∫ x, Y x ∂ν)
      (fun _ => (hY.sub_const _).aemeasurable)
  have hsubj : ∀ j ∈ (Finset.univ : Finset (Fin L)),
      HasSubgaussianMGF (fun c : Fin L → Ω₀ => Y (c j) - ∫ x, Y x ∂ν)
        ((‖b - a‖₊ / 2) ^ 2) (Measure.pi fun _ : Fin L => ν) := by
    intro j _
    have hmap : (Measure.pi fun _ : Fin L => ν).map (fun c : Fin L → Ω₀ => c j) = ν :=
      (measurePreserving_eval (fun _ : Fin L => ν) j).map_eq
    have h2 : HasSubgaussianMGF (fun x => Y x - ∫ x, Y x ∂ν) ((‖b - a‖₊ / 2) ^ 2)
        ((Measure.pi fun _ : Fin L => ν).map (fun c : Fin L → Ω₀ => c j)) := by
      rw [hmap]; exact hsub
    exact HasSubgaussianMGF.of_map (μ := Measure.pi fun _ : Fin L => ν)
      (Y := fun c : Fin L → Ω₀ => c j) (X := fun x => Y x - ∫ x, Y x ∂ν)
      (measurable_pi_apply j).aemeasurable h2
  have key := HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun hindep
    (c := fun _ => (‖b - a‖₊ / 2) ^ 2) (s := Finset.univ) hsubj ht
  have hc : ((∑ _i : Fin L, (‖b - a‖₊ / 2) ^ 2 : NNReal) : ℝ) = L * ((b - a) / 2) ^ 2 := by
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    push_cast
    rw [Real.norm_eq_abs, div_pow, div_pow, sq_abs]
  rw [hc] at key
  exact key

end Hoeffding

/-! # Part 7: cores of the upper bounds -/

section UpperBounds

/-- **Relative accuracy gives logarithmic accuracy.**  If `|x − 1| ≤ 1 − e^{−t}` then `|ln x| ≤ t`
(used for an estimate `x·A` of `A`, and for a reported cell mass `ν̂ = ν/x`). -/
theorem abs_log_le_of_abs_sub_one_le {x t : ℝ}
    (hx : |x - 1| ≤ 1 - Real.exp (-t)) : |Real.log x| ≤ t := by
  have hlo : Real.exp (-t) ≤ x := by
    have := (abs_le.mp hx).1
    linarith
  have hhi : x ≤ Real.exp t := by
    have h1 := (abs_le.mp hx).2
    have h2 : (2 : ℝ) ≤ Real.exp t + Real.exp (-t) := by
      have a1 := Real.add_one_le_exp t
      have a2 := Real.add_one_le_exp (-t)
      linarith
    linarith
  have hpos : 0 < x := lt_of_lt_of_le (Real.exp_pos _) hlo
  rw [abs_le]
  constructor
  · have := Real.log_le_log (Real.exp_pos _) hlo
    rwa [Real.log_exp] at this
  · have := Real.log_le_log hpos hhi
    rwa [Real.log_exp] at this

variable {S : Type*} [Fintype S]

open Classical in
/-- **The random-cell estimator (Theorem C (b), Proposition C′ (a)).**  Let `ν` be the true masses of
the cells (or points) and `ν̂ > 0` the reported ones.  The `ν̂`-probability of drawing a cell whose
reported mass is off by more than the relative amount `κ` is at most `‖ν − ν̂‖₁/κ`. -/
theorem random_cell_failure_le (ν νh : S → ℝ) (hνh : ∀ s, 0 < νh s) {κ : ℝ} (hκ : 0 < κ) :
    ∑ s ∈ univ.filter (fun s => κ < |ν s / νh s - 1|), νh s ≤ (∑ s, |ν s - νh s|) / κ := by
  rw [le_div_iff₀ hκ, Finset.sum_mul]
  have h1 : ∀ s ∈ univ.filter (fun s => κ < |ν s / νh s - 1|), νh s * κ ≤ |ν s - νh s| := by
    intro s hs
    rw [Finset.mem_filter] at hs
    have h2 : |ν s / νh s - 1| = |ν s - νh s| / νh s := by
      rw [div_sub_one (hνh s).ne', abs_div, abs_of_pos (hνh s)]
    rw [h2, lt_div_iff₀ (hνh s)] at hs
    nlinarith [hs.2, hνh s]
  calc ∑ s ∈ univ.filter (fun s => κ < |ν s / νh s - 1|), νh s * κ
      ≤ ∑ s ∈ univ.filter (fun s => κ < |ν s / νh s - 1|), |ν s - νh s| := Finset.sum_le_sum h1
    _ ≤ ∑ s, |ν s - νh s| :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _) fun s _ _ => abs_nonneg _

open MeasureTheory ProbabilityTheory in
/-- **Plain Monte Carlo: the probabilistic core of the non-adaptive upper bound** (theory report,
Theorem 11.44).  For `L` independent draws from `ν` and a bounded measurable `Y` (the weight at a
sampled point), the sample mean misses the mean by `t` or more with probability at most
`Var(Y)/(L t²)`.  With `t = κ·E Y` and `Var(Y) ≤ R·(E Y)²` this is `R/(L κ²)`: `L ≥ R/(κ² δ)`
samples give relative accuracy `κ` with probability `1 − δ`.  (The bound `R = e^{2na + o(n)}` on
the class is the paper part of Theorem 11.44.) -/
theorem chebyshev_iid_mean {Ω₀ : Type*} [MeasurableSpace Ω₀] (ν : Measure Ω₀)
    [IsProbabilityMeasure ν] (Y : Ω₀ → ℝ) (hY : Measurable Y) {Bd : ℝ} (hb : ∀ x, |Y x| ≤ Bd)
    (L : ℕ) (hL : 0 < L) {t : ℝ} (ht : 0 < t) :
    (Measure.pi fun _ : Fin L => ν)
        {c | t ≤ |(∑ j : Fin L, Y (c j)) / L - ∫ x, Y x ∂ν|} ≤
      ENNReal.ofReal (variance Y ν / (L * t ^ 2)) := by
  set μ : Measure (Fin L → Ω₀) := Measure.pi fun _ : Fin L => ν with hμ
  let X : Fin L → (Fin L → Ω₀) → ℝ := fun j c => Y (c j)
  have hXmeas : ∀ j, Measurable (X j) := fun j => hY.comp (measurable_pi_apply j)
  have hmap : ∀ j, μ.map (fun c : Fin L → Ω₀ => c j) = ν := fun j =>
    (measurePreserving_eval (fun _ : Fin L => ν) j).map_eq
  have hLp : ∀ j ∈ (Finset.univ : Finset (Fin L)), MemLp (X j) 2 μ := fun j _ =>
    MemLp.of_bound (hXmeas j).aestronglyMeasurable Bd
      (Filter.Eventually.of_forall fun c => by simpa [Real.norm_eq_abs] using hb (c j))
  have hindep : iIndepFun X μ :=
    iIndepFun_pi (X := fun (_ : Fin L) (x : Ω₀) => Y x) (fun _ => hY.aemeasurable)
  have hpair : Set.Pairwise (↑(Finset.univ : Finset (Fin L))) fun i j => X i ⟂ᵢ[μ] X j :=
    fun i _ j _ hij => hindep.indepFun hij
  have hvar : variance (∑ j, X j) μ = L * variance Y ν := by
    rw [IndepFun.variance_sum hLp hpair]
    have h1 : ∀ j ∈ (Finset.univ : Finset (Fin L)), variance (X j) μ = variance Y ν := by
      intro j _
      have h := variance_map (μ := μ) (Y := fun c : Fin L → Ω₀ => c j) (X := Y)
        (by rw [hmap j]; exact hY.aemeasurable) (measurable_pi_apply j).aemeasurable
      rw [hmap j] at h
      exact h.symm
    rw [Finset.sum_congr rfl h1, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      nsmul_eq_mul]
  have hmean : ∫ c, (∑ j, X j) c ∂μ = L * ∫ x, Y x ∂ν := by
    have h2 : ∀ j ∈ (Finset.univ : Finset (Fin L)), ∫ c, X j c ∂μ = ∫ x, Y x ∂ν := by
      intro j _
      have h := integral_map (μ := μ) (φ := fun c : Fin L → Ω₀ => c j)
        (measurable_pi_apply j).aemeasurable (f := Y)
        (by rw [hmap j]; exact hY.aestronglyMeasurable)
      rw [hmap j] at h
      exact h.symm
    simp_rw [Finset.sum_apply]
    rw [integral_finsetSum _ fun j hj => (hLp j hj).integrable one_le_two,
      Finset.sum_congr rfl h2, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      nsmul_eq_mul]
  have hSLp : MemLp (∑ j, X j) 2 μ := memLp_finsetSum' _ hLp
  have hLpos : (0 : ℝ) < L := Nat.cast_pos.mpr hL
  have hcheb := meas_ge_le_variance_div_sq hSLp (c := L * t) (mul_pos hLpos ht)
  rw [hvar, hmean] at hcheb
  have hset : {c : Fin L → Ω₀ | t ≤ |(∑ j : Fin L, Y (c j)) / L - ∫ x, Y x ∂ν|} =
      {c | (L : ℝ) * t ≤ |(∑ j, X j) c - L * ∫ x, Y x ∂ν|} := by
    ext c
    simp only [Set.mem_setOf_eq, Finset.sum_apply]
    have h3 : (∑ j : Fin L, Y (c j)) / L - ∫ x, Y x ∂ν =
        ((∑ j : Fin L, Y (c j)) - L * ∫ x, Y x ∂ν) / L := by
      field_simp
    rw [h3, abs_div, abs_of_pos hLpos, le_div_iff₀ hLpos, mul_comm]
  rw [hset]
  refine hcheb.trans (le_of_eq ?_)
  congr 1
  field_simp

end UpperBounds

end MetricChain
