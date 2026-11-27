import Mathlib
import proofs.Frontiers.Dominance
import proofs.CertificateAlgebra

/-!
# Second-order envelopes: a nearly additive residual has pairwise models

The energies certified in this project are `E = E₀ + g`: an explicit pairwise model `E₀` plus a
residual `g` that can only be evaluated pointwise.  If `g` is known only through a *first-order*
envelope (bounded single-site differences), an anchor certificate has to evaluate the residual at
every configuration whose energy gap is small compared with the envelope (`anchor_necessary`,
`anchor_card_lower_bound` in `EnvelopeDuality.lean`) — in general exponentially many.  This file
proves the constructive counterpart: a *second-order* envelope — bounded mixed differences, "the
residual is nearly additive" — together with one evaluation of the residual per (site, state)
pair yields explicit **pairwise** lower and upper models of the full energy, which the pairwise
kernel of `CertificateAlgebra.lean` certifies.  This is the anchored (cut-HDMR, many-body)
expansion at order one with a rigorous remainder.

## Objects

Sites `ι`, state spaces `σ i`, configurations `x : ∀ i, σ i`, a reference configuration `x₀`, a
residual `g : (∀ i, σ i) → ℝ` and constants `c : ι → ι → ℝ`.

* `MixedDiffBound g c` — for every context `x`, all sites `i ≠ j` and all states `a`, `b`:
  `|g (x[i ↦ a][j ↦ b]) - g (x[i ↦ a]) - g (x[j ↦ b]) + g x| ≤ c i j`.  With `c = 0` the residual
  is additive (a sum of one-site functions); in general `c i j` bounds the strength of the
  coupling of the sites `i` and `j` inside the residual.
* `starPart g x₀ x = g x₀ + ∑ i, (g (x₀[i ↦ x i]) - g x₀)` — the order-one expansion of `g` around
  `x₀`.  It uses only the values of `g` on the *star* of `x₀` (`x₀` and its single-site
  modifications): `n (k - 1) + 1` evaluations for `n` sites with `k` states each.
* `pairRemainder c x₀ x = ½ ∑_{i ≠ j} c i j · [x i ≠ x₀ i] · [x j ≠ x₀ j]` — for symmetric `c`,
  the sum of `c i j` over the unordered pairs of sites at which `x` differs from `x₀`.
* `lowerModel M g c x₀`, `upperModel M g c x₀` — the pairwise models obtained from the explicit
  part `M` by adding the star increments of `g` to the one-body table and subtracting (adding)
  `c i j / 2` on the pair entries whose two states both differ from the reference.

## Results

* `secondOrder_remainder` — `|g x - starPart g x₀ x| ≤ pairRemainder c x₀ x` for symmetric `c`.
* `starPart_eq_of_additive` — for `c = 0` the expansion is exact: an additive residual is
  determined by its values on the star.
* `pairwise_sandwich` — for every configuration `x` the true energy `M.energy x + g x` lies
  between `(lowerModel M g c x₀).energy x + g x₀` and `(upperModel M g c x₀).energy x + g x₀`.
* `verify_sound_secondOrder` — the kernel statement: a certificate accepted by `verify` for a
  rational instance lying termwise below `lowerModel M g c x₀` proves
  `L + g x₀ ≤ M.energy x + g x` for every `x` of the box.
* `secondOrder_witness` — non-vacuity and sharpness: for the two-site coupling
  `g x = ¼ · [x 0 = 1] · [x 1 = 1]` (not additive) and `c = ¼` the remainder bound is an equality
  at `x = (1, 1)`.  `coupling_class_lower_bound` and `secondOrder_kernel_witness` run the kernel
  on the corresponding lower instance.

## Sharpness: the star sandwich is the optimal recovery from star data

For symmetric *nonnegative* `c` the two bounds of the remainder theorem are themselves residuals
with the envelope `c` and the star values of `g`.  `SecondOrderClass g c x₀ g'` says that `g'`
has the second-order envelope `c` and agrees with `g` on the star of `x₀`.

* `PairModel.energy_mixedDiff`, `PairModel.mixedDiffBound_energy` — the mixed difference of a
  pairwise energy at two sites only involves the two pair tables of these sites, so pairwise
  energies have second-order envelopes that can be read off their tables;
  `mixedDiffBound_add`, `mixedDiffBound_neg`, `mixedDiffBound_sub`, `mixedDiffBound_of_additive`:
  second-order envelopes are stable under sums, differences and negation, and additive functions
  have the envelope `0`.
* `pairRemainder_mixedDiffBound`, `starPart_mixedDiffBound` — the remainder has the envelope `c`
  and the star part the envelope `0`; hence the extremal residuals
  `lowerExt g c x₀ = starPart g x₀ - pairRemainder c x₀` and
  `upperExt g c x₀ = starPart g x₀ + pairRemainder c x₀` belong to the class.
* `secondOrder_envelope_exact` — every residual of the class lies between `lowerExt` and
  `upperExt`, and both are members (`secondOrder_lower_attained`, `secondOrder_upper_attained`):
  the enclosure cannot be improved from the same data, and the class is never empty.
* `secondOrder_robust_min_exact` — lossless pairwise reduction: over any finite set of
  configurations the least (greatest) possible minimum energy over the class is exactly the
  minimum of the lower (upper) pairwise model.
* `secondOrder_certified_minimizer_iff` — `x₀` minimises `M.energy + g'` for every residual of
  the class iff it minimises its own lower model (`secondOrder_minimizer_witness`: a concrete
  instance).

## Proof of the remainder bound

Switch the sites from `x₀` to `x` one at a time: for a set `S` of sites let `mixConfig x₀ x S` be
the configuration equal to `x` on `S` and to `x₀` elsewhere.

1. `siteDiff_mixConfig_le`: for `j ∉ S` the single-site difference `D_j g y = g (y[j ↦ b]) - g y`
   satisfies `|D_j g (mixConfig x₀ x S) - D_j g x₀| ≤ ∑ i ∈ S, c i j · [x i ≠ x₀ i]`, because
   switching one more site `i` changes `D_j g` by a mixed difference, which is at most `c i j` and
   vanishes when `x i = x₀ i`.
2. `secondOrder_remainder_finset`: switching the site `j` after the sites of `S` adds
   `D_j g (mixConfig x₀ x S)` to `g` and `D_j g x₀` to the star part (both with `b = x j`); by
   step 1 they differ by at most `∑ i ∈ S, c i j · [x i ≠ x₀ i] · [x j ≠ x₀ j]`, which is the
   increase of the pair sum (`sum_insert_erase_pairs`; the symmetry of `c` is used here).
3. `S = univ` is the theorem.
-/

namespace MetricChain

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-! ### Second-order envelopes and the order-one expansion -/

/-- **Second-order envelope.**  The mixed second differences of the residual `g` between two
distinct sites `i ≠ j` are bounded by `c i j`, uniformly in the context `x` and in the new states
`a`, `b`.  For `c = 0` the residual is additive; in general `c i j` bounds the strength of the
coupling of the sites `i` and `j` inside the residual. -/
def MixedDiffBound [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) : Prop :=
  ∀ (x : ∀ i, σ i) (i j : ι), i ≠ j → ∀ (a : σ i) (b : σ j),
    |g (Function.update (Function.update x i a) j b) - g (Function.update x i a) -
      g (Function.update x j b) + g x| ≤ c i j

/-- Indicator (`0` or `1`) that the state of site `i` in `x` differs from the reference `x₀`. -/
def changed [∀ i, DecidableEq (σ i)] (x₀ x : ∀ i, σ i) (i : ι) : ℝ :=
  if x i = x₀ i then 0 else 1

/-- **Order-one (anchored) expansion** of the residual around the reference configuration `x₀`:
the reference value plus the sum of the single-site increments.  Only the values of `g` on the
star of `x₀` (the reference and its single-site modifications) enter. -/
def starPart [Fintype ι] [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x₀ x : ∀ i, σ i) : ℝ :=
  g x₀ + ∑ i, (g (Function.update x₀ i (x i)) - g x₀)

/-- **Pairwise remainder**: half the sum of `c i j` over the ordered pairs of distinct sites at
which `x` differs from the reference `x₀` (for symmetric `c`: the sum over unordered pairs). -/
noncomputable def pairRemainder [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (c : ι → ι → ℝ) (x₀ x : ∀ i, σ i) : ℝ :=
  (1 / 2) * ∑ i, ∑ j ∈ univ.erase i, c i j * changed x₀ x i * changed x₀ x j

/-- A site at which `x` agrees with the reference has indicator `0`. -/
theorem changed_of_eq [∀ i, DecidableEq (σ i)] {x₀ x : ∀ i, σ i} {i : ι} (h : x i = x₀ i) :
    changed x₀ x i = 0 := by
  simp [changed, h]

/-- A site at which `x` differs from the reference has indicator `1`. -/
theorem changed_of_ne [∀ i, DecidableEq (σ i)] {x₀ x : ∀ i, σ i} {i : ι} (h : x i ≠ x₀ i) :
    changed x₀ x i = 1 := by
  simp [changed, h]

/-! ### Switching the sites one at a time -/

/-- The configuration equal to `x` on the sites of `S` and to the reference `x₀` elsewhere. -/
def mixConfig [DecidableEq ι] (x₀ x : ∀ i, σ i) (S : Finset ι) : ∀ i, σ i :=
  fun i => if i ∈ S then x i else x₀ i

/-- No site switched: the reference configuration. -/
theorem mixConfig_empty [DecidableEq ι] (x₀ x : ∀ i, σ i) : mixConfig x₀ x ∅ = x₀ := by
  funext i
  simp [mixConfig]

/-- All sites switched: the target configuration. -/
theorem mixConfig_univ [Fintype ι] [DecidableEq ι] (x₀ x : ∀ i, σ i) :
    mixConfig x₀ x univ = x := by
  funext i
  simp [mixConfig]

/-- Switching one more site is a single-site update. -/
theorem mixConfig_insert [DecidableEq ι] (x₀ x : ∀ i, σ i) (S : Finset ι) (j : ι) :
    mixConfig x₀ x (insert j S) = Function.update (mixConfig x₀ x S) j (x j) := by
  funext i
  by_cases hij : i = j
  · subst hij
    simp [mixConfig]
  · simp [mixConfig, hij]

/-- Switching a site at which `x` agrees with the reference changes nothing. -/
theorem mixConfig_update_self [DecidableEq ι] (x₀ x : ∀ i, σ i) {S : Finset ι} {j : ι}
    (hj : j ∉ S) (hx : x j = x₀ j) :
    Function.update (mixConfig x₀ x S) j (x j) = mixConfig x₀ x S := by
  have h : mixConfig x₀ x S j = x j := by simp [mixConfig, hj, hx]
  rw [← h]
  exact Function.update_eq_self j _

/-- Adding a new site `j` to a sum over the ordered pairs of distinct sites of `S`: the new pairs
are `(j, k)` and `(i, j)` with `i, k ∈ S`. -/
theorem sum_insert_erase_pairs {α : Type*} [DecidableEq α] (F : α → α → ℝ) {j : α}
    {S : Finset α} (hj : j ∉ S) :
    ∑ i ∈ insert j S, ∑ k ∈ (insert j S).erase i, F i k =
      ∑ k ∈ S, F j k + ∑ i ∈ S, F i j + ∑ i ∈ S, ∑ k ∈ S.erase i, F i k := by
  rw [Finset.sum_insert hj, Finset.erase_insert hj]
  have h : ∀ i ∈ S, ∑ k ∈ (insert j S).erase i, F i k = F i j + ∑ k ∈ S.erase i, F i k := by
    intro i hi
    have hji : j ≠ i := fun h => hj (h ▸ hi)
    rw [Finset.erase_insert_of_ne hji, Finset.sum_insert]
    exact fun h => hj (Finset.mem_of_mem_erase h)
  rw [Finset.sum_congr rfl h, Finset.sum_add_distrib]
  ring

/-- **Drift of a single-site difference.**  Let `j ∉ S` and let `b` be a state of site `j`.
Switching the sites of `S` from the reference `x₀` to `x` changes the single-site difference
`g (y[j ↦ b]) - g y` by at most `∑ i ∈ S, c i j · [x i ≠ x₀ i]`: each switched site contributes
one mixed difference, which vanishes if the site does not actually change. -/
theorem siteDiff_mixConfig_le [DecidableEq ι] [∀ i, DecidableEq (σ i)] (g : (∀ i, σ i) → ℝ)
    (c : ι → ι → ℝ) (hg : MixedDiffBound g c) (x₀ x : ∀ i, σ i) (j : ι) (b : σ j)
    (S : Finset ι) (hj : j ∉ S) :
    |(g (Function.update (mixConfig x₀ x S) j b) - g (mixConfig x₀ x S)) -
        (g (Function.update x₀ j b) - g x₀)| ≤ ∑ i ∈ S, c i j * changed x₀ x i := by
  induction S using Finset.induction_on with
  | empty => simp [mixConfig_empty]
  | insert i S hi ih =>
    have hij : i ≠ j := fun h => hj (h ▸ Finset.mem_insert_self i S)
    have hjS : j ∉ S := fun h => hj (Finset.mem_insert_of_mem h)
    have ih' := abs_le.mp (ih hjS)
    rw [Finset.sum_insert hi, mixConfig_insert]
    have hstep : |g (Function.update (Function.update (mixConfig x₀ x S) i (x i)) j b) -
        g (Function.update (mixConfig x₀ x S) i (x i)) -
        g (Function.update (mixConfig x₀ x S) j b) + g (mixConfig x₀ x S)| ≤
        c i j * changed x₀ x i := by
      by_cases hx : x i = x₀ i
      · rw [mixConfig_update_self x₀ x hi hx, changed_of_eq hx]
        simp
      · rw [changed_of_ne hx, mul_one]
        exact hg (mixConfig x₀ x S) i j hij (x i) b
    have hstep' := abs_le.mp hstep
    exact abs_le.mpr ⟨by linarith [hstep'.1, ih'.1], by linarith [hstep'.2, ih'.2]⟩

/-- **Remainder bound after switching the sites of `S`.**  The order-one expansion restricted to
`S` approximates `g (mixConfig x₀ x S)` up to half the sum of `c i j` over the ordered pairs of
distinct changed sites of `S`. -/
theorem secondOrder_remainder_finset [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hg : MixedDiffBound g c)
    (hc : ∀ i j, c i j = c j i) (x₀ x : ∀ i, σ i) (S : Finset ι) :
    |g (mixConfig x₀ x S) - g x₀ - ∑ i ∈ S, (g (Function.update x₀ i (x i)) - g x₀)| ≤
      (1 / 2) * ∑ i ∈ S, ∑ j ∈ S.erase i, c i j * changed x₀ x i * changed x₀ x j := by
  induction S using Finset.induction_on with
  | empty => simp [mixConfig_empty]
  | insert j S hj ih =>
    have ih' := abs_le.mp ih
    have hinc : |(g (Function.update (mixConfig x₀ x S) j (x j)) - g (mixConfig x₀ x S)) -
        (g (Function.update x₀ j (x j)) - g x₀)| ≤
        (∑ i ∈ S, c i j * changed x₀ x i) * changed x₀ x j := by
      by_cases hx : x j = x₀ j
      · have h0 : Function.update x₀ j (x j) = x₀ := by
          rw [hx]
          exact Function.update_eq_self j x₀
        rw [mixConfig_update_self x₀ x hj hx, h0, changed_of_eq hx]
        simp
      · rw [changed_of_ne hx, mul_one]
        exact siteDiff_mixConfig_le g c hg x₀ x j (x j) S hj
    have hinc' := abs_le.mp hinc
    have h1 : ∑ k ∈ S, c j k * changed x₀ x j * changed x₀ x k =
        (∑ i ∈ S, c i j * changed x₀ x i) * changed x₀ x j := by
      rw [Finset.sum_mul]
      refine Finset.sum_congr rfl fun k _ => ?_
      rw [hc j k]
      ring
    have h2 : ∑ i ∈ S, c i j * changed x₀ x i * changed x₀ x j =
        (∑ i ∈ S, c i j * changed x₀ x i) * changed x₀ x j := by
      rw [Finset.sum_mul]
    rw [mixConfig_insert, Finset.sum_insert hj,
      sum_insert_erase_pairs (fun i k => c i k * changed x₀ x i * changed x₀ x k) hj, h1, h2]
    exact abs_le.mpr ⟨by linarith [hinc'.1, ih'.1], by linarith [hinc'.2, ih'.2]⟩

/-! ### The remainder theorem -/

/-- **Second-order remainder theorem.**  If the mixed differences of the residual `g` are bounded
by a symmetric table `c`, the order-one expansion around any reference configuration `x₀` — which
only uses the values of `g` on the star of `x₀` — approximates `g` everywhere up to the sum of
`c i j` over the unordered pairs of sites at which `x` differs from `x₀`. -/
theorem secondOrder_remainder [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hg : MixedDiffBound g c)
    (hc : ∀ i j, c i j = c j i) (x₀ x : ∀ i, σ i) :
    |g x - starPart g x₀ x| ≤ pairRemainder c x₀ x := by
  have h := secondOrder_remainder_finset g c hg hc x₀ x univ
  rw [mixConfig_univ] at h
  have e : g x - starPart g x₀ x =
      g x - g x₀ - ∑ i, (g (Function.update x₀ i (x i)) - g x₀) := by
    unfold starPart
    ring
  rw [e]
  exact h

/-- **Exactness for additive residuals.**  A residual whose mixed differences vanish is equal to
its order-one expansion around every reference configuration: it is determined by its values on
the star. -/
theorem starPart_eq_of_additive [Fintype ι] [DecidableEq ι] (g : (∀ i, σ i) → ℝ)
    (hg : MixedDiffBound g (fun _ _ => 0)) (x₀ x : ∀ i, σ i) : g x = starPart g x₀ x := by
  classical
  have h := secondOrder_remainder g (fun _ _ => 0) hg (fun _ _ => rfl) x₀ x
  have h0 : pairRemainder (fun _ _ => (0 : ℝ)) x₀ x = 0 := by
    simp [pairRemainder]
  rw [h0] at h
  have := abs_nonpos_iff.mp h
  linarith

/-! ### Pairwise lower and upper models of the full energy -/

/-- **Pairwise lower model** of `M.energy + g`: the star increments of the residual are added to
the one-body table, and `c i j / 2` is subtracted from every pair entry whose two states both
differ from the reference (each unordered pair of sites is counted in both orientations). -/
noncomputable def lowerModel [DecidableEq ι] [∀ i, DecidableEq (σ i)] (M : PairModel ℝ ι σ)
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) : PairModel ℝ ι σ where
  h i s := M.h i s + (g (Function.update x₀ i s) - g x₀)
  J i j a b := M.J i j a b -
    c i j / 2 * (if a = x₀ i then 0 else 1) * (if b = x₀ j then 0 else 1)

/-- **Pairwise upper model** of `M.energy + g`: as `lowerModel`, with `c i j / 2` added. -/
noncomputable def upperModel [DecidableEq ι] [∀ i, DecidableEq (σ i)] (M : PairModel ℝ ι σ)
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) : PairModel ℝ ι σ where
  h i s := M.h i s + (g (Function.update x₀ i s) - g x₀)
  J i j a b := M.J i j a b +
    c i j / 2 * (if a = x₀ i then 0 else 1) * (if b = x₀ j then 0 else 1)

/-- The pair corrections of the two models add up to the pairwise remainder. -/
theorem sum_half_changed_eq_pairRemainder [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (c : ι → ι → ℝ) (x₀ x : ∀ i, σ i) :
    ∑ i, ∑ j ∈ univ.erase i, c i j / 2 * (if x i = x₀ i then (0 : ℝ) else 1) *
      (if x j = x₀ j then (0 : ℝ) else 1) = pairRemainder c x₀ x := by
  unfold pairRemainder changed
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  ring

/-- Energy of the lower model: explicit energy plus star part minus pairwise remainder (up to
the reference value `g x₀`, which is a constant). -/
theorem lowerModel_energy [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ x : ∀ i, σ i) :
    (lowerModel M g c x₀).energy x + g x₀ =
      M.energy x + starPart g x₀ x - pairRemainder c x₀ x := by
  rw [← sum_half_changed_eq_pairRemainder]
  unfold PairModel.energy lowerModel starPart
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  ring

/-- Energy of the upper model: explicit energy plus star part plus pairwise remainder (up to
the reference value `g x₀`, which is a constant). -/
theorem upperModel_energy [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ x : ∀ i, σ i) :
    (upperModel M g c x₀).energy x + g x₀ =
      M.energy x + starPart g x₀ x + pairRemainder c x₀ x := by
  rw [← sum_half_changed_eq_pairRemainder]
  unfold PairModel.energy upperModel starPart
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  ring

/-- **Pairwise sandwich.**  If the residual `g` has mixed differences bounded by a symmetric
table `c`, the full energy `M.energy + g` lies between the energies of two explicit *pairwise*
models (shifted by the constant `g x₀`) that are built from the explicit part `M`, the constants
`c` and the values of `g` on the star of the reference configuration `x₀` only. -/
theorem pairwise_sandwich [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hg : MixedDiffBound g c)
    (hc : ∀ i j, c i j = c j i) (x₀ x : ∀ i, σ i) :
    (lowerModel M g c x₀).energy x + g x₀ ≤ M.energy x + g x ∧
      M.energy x + g x ≤ (upperModel M g c x₀).energy x + g x₀ := by
  have h := abs_le.mp (secondOrder_remainder g c hg hc x₀ x)
  rw [lowerModel_energy, upperModel_energy]
  exact ⟨by linarith [h.2], by linarith [h.1]⟩

/-! ### The kernel statement -/

/-- **Kernel soundness with a second-order envelope.**  Let the residual `g` on `n` sites with
`k` states have mixed differences bounded by a symmetric table `c`, and let the rational instance
`I` lie termwise below the pairwise lower model built from the explicit part `M`, the constants
`c` and the star of `x₀` (outward rounding).  If the pairwise kernel accepts a certificate for
`I` and the bound `L` on the box `D`, then `L + g x₀` is a lower bound on the *true* energy
`M.energy x + g x` of every configuration of the box.

In words: `n (k - 1) + 1` evaluations of the residual and the second-order envelope constants turn
the residual problem into a pairwise one, which the tropical kernel certifies. -/
theorem verify_sound_secondOrder {n k : ℕ} (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (g : Config n k → ℝ) (c : Fin n → Fin n → ℝ) (x₀ : Config n k)
    (hg : MixedDiffBound g c) (hc : ∀ i j, c i j = c j i) (I : PairInstance n k)
    (hh : ∀ i a, (I.h i a : ℝ) ≤ (lowerModel M g c x₀).h i a)
    (hJ : ∀ i j a b, (I.J i j a b : ℝ) ≤ (lowerModel M g c x₀).J i j a b)
    (cert : Cert n k) (D : Dom n k) (L : ℚ) (hv : verify cert I D L = true)
    (x : Config n k) (hx : InBox D x) : (L : ℝ) + g x₀ ≤ M.energy x + g x := by
  have h1 := verify_sound_real cert I D L hv (lowerModel M g c x₀) hh hJ x hx
  have h2 := (pairwise_sandwich M g c hg hc x₀ x).1
  linarith

/-! ### Sharpness I: closure properties, additive functions and pairwise energies

The functions with a second-order envelope are closed under sums, differences and negation;
additive functions have the envelope `0`; and the mixed differences of a pairwise energy can be
read off its pair tables.  In particular the pairwise remainder has the envelope `c`. -/

/-- The sum of two residuals has the sum of their second-order envelopes. -/
theorem mixedDiffBound_add [DecidableEq ι] {g₁ g₂ : (∀ i, σ i) → ℝ} {c₁ c₂ : ι → ι → ℝ}
    (h₁ : MixedDiffBound g₁ c₁) (h₂ : MixedDiffBound g₂ c₂) :
    MixedDiffBound (fun x => g₁ x + g₂ x) (fun i j => c₁ i j + c₂ i j) := by
  intro x i j hij a b
  have e₁ := abs_le.mp (h₁ x i j hij a b)
  have e₂ := abs_le.mp (h₂ x i j hij a b)
  dsimp only
  exact abs_le.mpr ⟨by linarith [e₁.1, e₂.1], by linarith [e₁.2, e₂.2]⟩

/-- A residual and its negative have the same second-order envelopes. -/
theorem mixedDiffBound_neg [DecidableEq ι] {g : (∀ i, σ i) → ℝ} {c : ι → ι → ℝ}
    (h : MixedDiffBound g c) : MixedDiffBound (fun x => -g x) c := by
  intro x i j hij a b
  have e := abs_le.mp (h x i j hij a b)
  dsimp only
  exact abs_le.mpr ⟨by linarith [e.1, e.2], by linarith [e.1, e.2]⟩

/-- The difference of two residuals has the sum of their second-order envelopes. -/
theorem mixedDiffBound_sub [DecidableEq ι] {g₁ g₂ : (∀ i, σ i) → ℝ} {c₁ c₂ : ι → ι → ℝ}
    (h₁ : MixedDiffBound g₁ c₁) (h₂ : MixedDiffBound g₂ c₂) :
    MixedDiffBound (fun x => g₁ x - g₂ x) (fun i j => c₁ i j + c₂ i j) := by
  intro x i j hij a b
  have e₁ := abs_le.mp (h₁ x i j hij a b)
  have e₂ := abs_le.mp (h₂ x i j hij a b)
  dsimp only
  exact abs_le.mpr ⟨by linarith [e₁.1, e₂.2], by linarith [e₁.2, e₂.1]⟩

/-- **Additive functions have vanishing mixed differences**: a constant plus a sum of one-site
functions has the second-order envelope `0`.  (Conversely, a residual with the envelope `0` is of
this form by `starPart_eq_of_additive`.) -/
theorem mixedDiffBound_of_additive [Fintype ι] [DecidableEq ι] (k : ℝ) (φ : ∀ i, σ i → ℝ) :
    MixedDiffBound (fun x : ∀ i, σ i => k + ∑ i, φ i (x i)) (fun _ _ => 0) := by
  intro x p q hpq a b
  have hterm : ∀ i : ι, φ i (Function.update (Function.update x p a) q b i) -
      φ i (Function.update x p a i) - φ i (Function.update x q b i) + φ i (x i) = 0 := by
    intro i
    by_cases hiq : i = q
    · subst hiq
      rw [Function.update_self, Function.update_self, Function.update_of_ne (Ne.symm hpq)]
      ring
    · rw [Function.update_of_ne hiq, Function.update_of_ne hiq]
      ring
  have hsum : (k + ∑ i, φ i (Function.update (Function.update x p a) q b i)) -
      (k + ∑ i, φ i (Function.update x p a i)) - (k + ∑ i, φ i (Function.update x q b i)) +
      (k + ∑ i, φ i (x i)) = ∑ i, (φ i (Function.update (Function.update x p a) q b i) -
      φ i (Function.update x p a i) - φ i (Function.update x q b i) + φ i (x i)) := by
    simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib]
    ring
  dsimp only
  rw [hsum, Finset.sum_eq_zero fun i _ => hterm i]
  simp

/-- The order-one expansion is additive, so its mixed differences vanish. -/
theorem starPart_mixedDiffBound [Fintype ι] [DecidableEq ι] (g : (∀ i, σ i) → ℝ)
    (x₀ : ∀ i, σ i) : MixedDiffBound (starPart g x₀) (fun _ _ => 0) :=
  mixedDiffBound_of_additive (g x₀) fun i s => g (Function.update x₀ i s) - g x₀

/-- **Mixed differences of a pairwise energy are local.**  For two distinct sites `p ≠ q` the
mixed difference of a pairwise energy only involves the pair tables `J p q` and `J q p`: it is
the sum of their second differences between the old states `x p`, `x q` and the new states `a`,
`b`.  The one-body terms and all other pair tables cancel. -/
theorem PairModel.energy_mixedDiff {R : Type*} [CommRing R] [Fintype ι] [DecidableEq ι]
    (M : PairModel R ι σ) (x : ∀ i, σ i) {p q : ι} (hpq : p ≠ q) (a : σ p) (b : σ q) :
    M.energy (Function.update (Function.update x p a) q b) - M.energy (Function.update x p a) -
        M.energy (Function.update x q b) + M.energy x =
      (M.J p q a b - M.J p q a (x q) - M.J p q (x p) b + M.J p q (x p) (x q)) +
        (M.J q p b a - M.J q p (x q) a - M.J q p b (x p) + M.J q p (x q) (x p)) := by
  have hD : ∀ y : ∀ i, σ i, M.energy (Function.update y q b) - M.energy y =
      M.h q b - M.h q (y q) + ∑ j ∈ univ.erase q, M.link q b (y q) j (y j) := by
    intro y
    have h := M.energy_update_sub y q b (y q)
    rw [Function.update_eq_self, PairModel.localE_sub] at h
    exact h
  have h1 := hD (Function.update x p a)
  have h2 := hD x
  rw [Function.update_of_ne (Ne.symm hpq)] at h1
  have hsum : ∑ j ∈ univ.erase q, M.link q b (x q) j (Function.update x p a j) -
      ∑ j ∈ univ.erase q, M.link q b (x q) j (x j) =
      M.link q b (x q) p a - M.link q b (x q) p (x p) := by
    rw [← Finset.sum_sub_distrib, Finset.sum_eq_single p]
    · rw [Function.update_self]
    · intro j _ hj
      rw [Function.update_of_ne hj, sub_self]
    · intro h
      exact absurd (Finset.mem_erase.mpr ⟨hpq, mem_univ p⟩) h
  have hlink : M.energy (Function.update (Function.update x p a) q b) -
      M.energy (Function.update x p a) - M.energy (Function.update x q b) + M.energy x =
      M.link q b (x q) p a - M.link q b (x q) p (x p) := by
    linear_combination h1 - h2 + hsum
  rw [hlink]
  unfold PairModel.link
  ring

/-- **Second-order envelope of a pairwise energy.**  If the second differences of the pair tables
of every two distinct sites (both orientations together) are bounded by `c i j`, the energy of
the model has the second-order envelope `c`. -/
theorem PairModel.mixedDiffBound_energy [Fintype ι] [DecidableEq ι] (M : PairModel ℝ ι σ)
    (c : ι → ι → ℝ)
    (h : ∀ i j, i ≠ j → ∀ (a a' : σ i) (b b' : σ j),
      |(M.J i j a b - M.J i j a b' - M.J i j a' b + M.J i j a' b') +
        (M.J j i b a - M.J j i b' a - M.J j i b a' + M.J j i b' a')| ≤ c i j) :
    MixedDiffBound M.energy c := by
  intro x i j hij a b
  rw [M.energy_mixedDiff x hij a b]
  exact h i j hij a (x i) b (x j)

/-- `|w · u · v| ≤ w` for a weight `w ≥ 0` and two factors of absolute value at most `1`. -/
theorem abs_mul_mul_le_of_abs_le_one {w u v : ℝ} (hw : 0 ≤ w) (hu : |u| ≤ 1) (hv : |v| ≤ 1) :
    |w * u * v| ≤ w := by
  rw [abs_mul, abs_mul, abs_of_nonneg hw]
  calc w * |u| * |v| ≤ w * |u| * 1 :=
        mul_le_mul_of_nonneg_left hv (mul_nonneg hw (abs_nonneg u))
    _ ≤ w * 1 * 1 := by
        have := mul_le_mul_of_nonneg_left hu hw
        linarith
    _ = w := by ring

/-- **The pairwise remainder has the second-order envelope `c`** (symmetric nonnegative `c`).
It is the energy of the pairwise model with the tables `c i j / 2 · [a ≠ x₀ i] · [b ≠ x₀ j]`,
and its mixed difference at two sites `i ≠ j` is `c i j` times two differences of indicators. -/
theorem pairRemainder_mixedDiffBound [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j) (x₀ : ∀ i, σ i) :
    MixedDiffBound (pairRemainder c x₀) c := by
  have hR : pairRemainder c x₀ = PairModel.energy (R := ℝ) (σ := σ) ⟨fun _ _ => 0, fun i j a b =>
      c i j / 2 * (if a = x₀ i then 0 else 1) * (if b = x₀ j then 0 else 1)⟩ := by
    funext x
    rw [← sum_half_changed_eq_pairRemainder]
    unfold PairModel.energy
    simp
  rw [hR]
  apply PairModel.mixedDiffBound_energy
  intro i j hij a a' b b'
  have hA : |(if a = x₀ i then (0 : ℝ) else 1) - (if a' = x₀ i then (0 : ℝ) else 1)| ≤ 1 := by
    split_ifs <;> norm_num
  have hB : |(if b = x₀ j then (0 : ℝ) else 1) - (if b' = x₀ j then (0 : ℝ) else 1)| ≤ 1 := by
    split_ifs <;> norm_num
  have h := abs_mul_mul_le_of_abs_le_one (hc0 i j) hA hB
  have e : ∀ A A' B B' : ℝ, (c i j / 2 * A * B - c i j / 2 * A * B' - c i j / 2 * A' * B +
      c i j / 2 * A' * B') + (c i j / 2 * B * A - c i j / 2 * B' * A - c i j / 2 * B * A' +
      c i j / 2 * B' * A') = c i j * (A - A') * (B - B') := by
    intro A A' B B'
    ring
  dsimp only
  rw [hc j i, e]
  exact h

/-! ### Sharpness II: the extremal residuals

`lowerExt g c x₀ = starPart g x₀ - pairRemainder c x₀` and
`upperExt g c x₀ = starPart g x₀ + pairRemainder c x₀` are the two bounds of the
remainder theorem, read as residuals.  They agree with `g` on the star of `x₀` and, for
symmetric nonnegative `c`, they have the second-order envelope `c`. -/

/-- The order-one expansion is exact at the reference configuration. -/
theorem starPart_self [Fintype ι] [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i) :
    starPart g x₀ x₀ = g x₀ := by
  simp [starPart]

/-- The order-one expansion is exact on the star of the reference configuration. -/
theorem starPart_update [Fintype ι] [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (x₀ : ∀ i, σ i)
    (i : ι) (s : σ i) : starPart g x₀ (Function.update x₀ i s) = g (Function.update x₀ i s) := by
  unfold starPart
  rw [Finset.sum_eq_single i]
  · rw [Function.update_self]
    ring
  · intro k _ hk
    rw [Function.update_of_ne hk, Function.update_eq_self, sub_self]
  · intro h
    exact absurd (mem_univ i) h

/-- **The order-one expansion only depends on star data**: two residuals that agree at the
reference configuration and at all its single-site modifications have the same star part. -/
theorem starPart_congr [Fintype ι] [DecidableEq ι] {g g' : (∀ i, σ i) → ℝ} {x₀ : ∀ i, σ i}
    (h₀ : g' x₀ = g x₀)
    (h : ∀ i s, g' (Function.update x₀ i s) = g (Function.update x₀ i s)) :
    starPart g' x₀ = starPart g x₀ := by
  funext x
  unfold starPart
  rw [h₀]
  congr 1
  exact Finset.sum_congr rfl fun i _ => by rw [h i (x i)]

/-- The pairwise remainder vanishes at the reference configuration. -/
theorem pairRemainder_self [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) : pairRemainder c x₀ x₀ = 0 := by
  simp [pairRemainder, changed]

/-- The pairwise remainder vanishes on the star of the reference configuration: at most one
site is changed. -/
theorem pairRemainder_update [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) (i : ι) (s : σ i) :
    pairRemainder c x₀ (Function.update x₀ i s) = 0 := by
  have h0 : ∀ k, k ≠ i → changed x₀ (Function.update x₀ i s) k = 0 := fun k hk =>
    changed_of_eq (Function.update_of_ne hk s x₀)
  unfold pairRemainder
  rw [Finset.sum_eq_zero, mul_zero]
  intro k _
  apply Finset.sum_eq_zero
  intro j hj
  have hjk : j ≠ k := Finset.ne_of_mem_erase hj
  by_cases hk : k = i
  · rw [h0 j (hk ▸ hjk), mul_zero]
  · rw [h0 k hk, mul_zero, zero_mul]

/-- **Lower extremal residual**: the order-one expansion minus the pairwise remainder. -/
noncomputable def lowerExt [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) : (∀ i, σ i) → ℝ :=
  fun x => starPart g x₀ x - pairRemainder c x₀ x

/-- **Upper extremal residual**: the order-one expansion plus the pairwise remainder. -/
noncomputable def upperExt [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) : (∀ i, σ i) → ℝ :=
  fun x => starPart g x₀ x + pairRemainder c x₀ x

/-- The lower extremal residual agrees with `g` at the reference configuration. -/
theorem lowerExt_self [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) : lowerExt g c x₀ x₀ = g x₀ := by
  unfold lowerExt
  rw [starPart_self, pairRemainder_self, sub_zero]

/-- The lower extremal residual agrees with `g` on the star of the reference configuration. -/
theorem lowerExt_update [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) (i : ι) (s : σ i) :
    lowerExt g c x₀ (Function.update x₀ i s) = g (Function.update x₀ i s) := by
  unfold lowerExt
  rw [starPart_update, pairRemainder_update, sub_zero]

/-- The upper extremal residual agrees with `g` at the reference configuration. -/
theorem upperExt_self [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) : upperExt g c x₀ x₀ = g x₀ := by
  unfold upperExt
  rw [starPart_self, pairRemainder_self, add_zero]

/-- The upper extremal residual agrees with `g` on the star of the reference configuration. -/
theorem upperExt_update [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i) (i : ι) (s : σ i) :
    upperExt g c x₀ (Function.update x₀ i s) = g (Function.update x₀ i s) := by
  unfold upperExt
  rw [starPart_update, pairRemainder_update, add_zero]

/-- The lower extremal residual has the second-order envelope `c` (symmetric nonnegative `c`). -/
theorem lowerExt_mixedDiffBound [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j)
    (x₀ : ∀ i, σ i) : MixedDiffBound (lowerExt g c x₀) c := by
  have h := mixedDiffBound_sub (starPart_mixedDiffBound g x₀)
    (pairRemainder_mixedDiffBound c hc hc0 x₀)
  simp only [zero_add] at h
  exact h

/-- The upper extremal residual has the second-order envelope `c` (symmetric nonnegative `c`). -/
theorem upperExt_mixedDiffBound [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j)
    (x₀ : ∀ i, σ i) : MixedDiffBound (upperExt g c x₀) c := by
  have h := mixedDiffBound_add (starPart_mixedDiffBound g x₀)
    (pairRemainder_mixedDiffBound c hc hc0 x₀)
  simp only [zero_add] at h
  exact h

/-! ### Sharpness III: the star sandwich is the optimal recovery from star data -/

/-- **The class of residuals consistent with the data**: `g'` has the second-order envelope `c`
and takes the same values as `g` on the star of `x₀` (at `x₀` and at all its single-site
modifications).  Only the star values of `g` enter the definition. -/
def SecondOrderClass [DecidableEq ι] (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ : ∀ i, σ i)
    (g' : (∀ i, σ i) → ℝ) : Prop :=
  MixedDiffBound g' c ∧ g' x₀ = g x₀ ∧
    ∀ i s, g' (Function.update x₀ i s) = g (Function.update x₀ i s)

/-- A residual with the second-order envelope `c` belongs to its own class. -/
theorem secondOrderClass_self [DecidableEq ι] {g : (∀ i, σ i) → ℝ} {c : ι → ι → ℝ}
    (hg : MixedDiffBound g c) (x₀ : ∀ i, σ i) : SecondOrderClass g c x₀ g :=
  ⟨hg, rfl, fun _ _ => rfl⟩

/-- The lower extremal residual belongs to the class (symmetric nonnegative `c`). -/
theorem lowerExt_mem_class [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j)
    (x₀ : ∀ i, σ i) : SecondOrderClass g c x₀ (lowerExt g c x₀) :=
  ⟨lowerExt_mixedDiffBound g c hc hc0 x₀, lowerExt_self g c x₀, lowerExt_update g c x₀⟩

/-- The upper extremal residual belongs to the class (symmetric nonnegative `c`). -/
theorem upperExt_mem_class [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j)
    (x₀ : ∀ i, σ i) : SecondOrderClass g c x₀ (upperExt g c x₀) :=
  ⟨upperExt_mixedDiffBound g c hc hc0 x₀, upperExt_self g c x₀, upperExt_update g c x₀⟩

/-- Every residual of the class lies between the two extremal residuals (symmetric `c`): the
remainder theorem for `g'`, whose star part is the star part of `g`. -/
theorem secondOrderClass_sandwich [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (x₀ : ∀ i, σ i)
    (g' : (∀ i, σ i) → ℝ) (hg' : SecondOrderClass g c x₀ g') (x : ∀ i, σ i) :
    lowerExt g c x₀ x ≤ g' x ∧ g' x ≤ upperExt g c x₀ x := by
  have h := abs_le.mp (secondOrder_remainder g' c hg'.1 hc x₀ x)
  rw [starPart_congr hg'.2.1 hg'.2.2] at h
  unfold lowerExt upperExt
  exact ⟨by linarith [h.2], by linarith [h.1]⟩

/-- **Exact envelope theorem (optimal recovery from star data).**  For symmetric nonnegative `c`
the two extremal residuals belong to the class, and every residual of the class lies between
them.  Hence, at every configuration `x`, the set of values `g' x` over the class has minimum
`lowerExt g c x₀ x` and maximum `upperExt g c x₀ x`, and each extreme is attained at all
configurations simultaneously by a single residual: no method that only uses the star values and
the constants `c` can report a tighter enclosure.  In particular the class is never empty. -/
theorem secondOrder_envelope_exact [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j)
    (x₀ : ∀ i, σ i) :
    SecondOrderClass g c x₀ (lowerExt g c x₀) ∧ SecondOrderClass g c x₀ (upperExt g c x₀) ∧
      ∀ g', SecondOrderClass g c x₀ g' →
        ∀ x, lowerExt g c x₀ x ≤ g' x ∧ g' x ≤ upperExt g c x₀ x :=
  ⟨lowerExt_mem_class g c hc hc0 x₀, upperExt_mem_class g c hc hc0 x₀,
    fun g' hg' x => secondOrderClass_sandwich g c hc x₀ g' hg' x⟩

/-- **The lower bound of the remainder theorem is attained**: some residual with the envelope `c`
and the star values of `g` equals `starPart g x₀ - pairRemainder c x₀` at every configuration. -/
theorem secondOrder_lower_attained [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j)
    (x₀ : ∀ i, σ i) :
    ∃ g' : (∀ i, σ i) → ℝ, MixedDiffBound g' c ∧ g' x₀ = g x₀ ∧
      (∀ i s, g' (Function.update x₀ i s) = g (Function.update x₀ i s)) ∧
      ∀ x, g' x = starPart g x₀ x - pairRemainder c x₀ x :=
  ⟨lowerExt g c x₀, lowerExt_mixedDiffBound g c hc hc0 x₀, lowerExt_self g c x₀,
    lowerExt_update g c x₀, fun _ => rfl⟩

/-- **The upper bound of the remainder theorem is attained**: some residual with the envelope `c`
and the star values of `g` equals `starPart g x₀ + pairRemainder c x₀` at every configuration. -/
theorem secondOrder_upper_attained [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j)
    (x₀ : ∀ i, σ i) :
    ∃ g' : (∀ i, σ i) → ℝ, MixedDiffBound g' c ∧ g' x₀ = g x₀ ∧
      (∀ i s, g' (Function.update x₀ i s) = g (Function.update x₀ i s)) ∧
      ∀ x, g' x = starPart g x₀ x + pairRemainder c x₀ x :=
  ⟨upperExt g c x₀, upperExt_mixedDiffBound g c hc hc0 x₀, upperExt_self g c x₀,
    upperExt_update g c x₀, fun _ => rfl⟩

/-! ### Sharpness IV: lossless pairwise reduction and the sharp-minimum certificate -/

/-- The lower pairwise model is the explicit part plus the lower extremal residual (up to the
constant `g x₀`). -/
theorem lowerModel_energy_eq_lowerExt [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ x : ∀ i, σ i) :
    (lowerModel M g c x₀).energy x + g x₀ = M.energy x + lowerExt g c x₀ x := by
  rw [lowerModel_energy]
  unfold lowerExt
  ring

/-- The upper pairwise model is the explicit part plus the upper extremal residual (up to the
constant `g x₀`). -/
theorem upperModel_energy_eq_upperExt [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (x₀ x : ∀ i, σ i) :
    (upperModel M g c x₀).energy x + g x₀ = M.energy x + upperExt g c x₀ x := by
  rw [upperModel_energy]
  unfold upperExt
  ring

/-- **Pairwise sandwich for the whole class.**  The true energy `M.energy + g'` of *every*
residual `g'` of the class lies between the energies of the two pairwise models built from the
star data of `g` (symmetric `c`). -/
theorem pairwise_sandwich_of_class [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i)
    (x₀ : ∀ i, σ i) (g' : (∀ i, σ i) → ℝ) (hg' : SecondOrderClass g c x₀ g') (x : ∀ i, σ i) :
    (lowerModel M g c x₀).energy x + g x₀ ≤ M.energy x + g' x ∧
      M.energy x + g' x ≤ (upperModel M g c x₀).energy x + g x₀ := by
  have h := secondOrderClass_sandwich g c hc x₀ g' hg' x
  rw [lowerModel_energy_eq_lowerExt, upperModel_energy_eq_upperExt]
  exact ⟨by linarith [h.1], by linarith [h.2]⟩

/-- **Lossless pairwise reduction.**  Let `S` be a finite non-empty set of configurations and
let `g'` range over the class.  The set of possible minimum energies `min_S (M.energy + g')` has
least element `min_S` of the lower pairwise model and greatest element `min_S` of the upper
pairwise model (both shifted by the constant `g x₀`).  So the pairwise kernel applied to the
lower model certifies the *exact* robust minimum: the bound holds for every residual of the
class and is attained by the lower extremal residual. -/
theorem secondOrder_robust_min_exact [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i)
    (hc0 : ∀ i j, 0 ≤ c i j) (x₀ : ∀ i, σ i) (S : Finset (∀ i, σ i)) (hS : S.Nonempty) :
    IsLeast {v : ℝ | ∃ g', SecondOrderClass g c x₀ g' ∧
        S.inf' hS (fun x => M.energy x + g' x) = v}
        (S.inf' hS fun x => (lowerModel M g c x₀).energy x + g x₀) ∧
      IsGreatest {v : ℝ | ∃ g', SecondOrderClass g c x₀ g' ∧
        S.inf' hS (fun x => M.energy x + g' x) = v}
        (S.inf' hS fun x => (upperModel M g c x₀).energy x + g x₀) := by
  refine ⟨⟨⟨lowerExt g c x₀, lowerExt_mem_class g c hc hc0 x₀, ?_⟩, ?_⟩,
    ⟨⟨upperExt g c x₀, upperExt_mem_class g c hc hc0 x₀, ?_⟩, ?_⟩⟩
  · congr 1
    funext x
    exact (lowerModel_energy_eq_lowerExt M g c x₀ x).symm
  · rintro v ⟨g', hg', rfl⟩
    apply Finset.le_inf'
    intro x hx
    have h1 := Finset.inf'_le (fun x => (lowerModel M g c x₀).energy x + g x₀) hx
    have h2 := (pairwise_sandwich_of_class M g c hc x₀ g' hg' x).1
    linarith
  · congr 1
    funext x
    exact (upperModel_energy_eq_upperExt M g c x₀ x).symm
  · rintro v ⟨g', hg', rfl⟩
    apply Finset.le_inf'
    intro x hx
    have h1 := Finset.inf'_le (fun x => M.energy x + g' x) hx
    have h2 := (pairwise_sandwich_of_class M g c hc x₀ g' hg' x).2
    linarith

/-- **Second-order sharp-minimum certificate.**  If the reference configuration minimises its own
lower pairwise model, it minimises the true energy `M.energy + g'` for every residual `g'` of the
class (symmetric `c`). -/
theorem secondOrder_certified_minimizer [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ) (hc : ∀ i j, c i j = c j i)
    (x₀ : ∀ i, σ i)
    (hmin : ∀ x, (lowerModel M g c x₀).energy x₀ ≤ (lowerModel M g c x₀).energy x)
    (g' : (∀ i, σ i) → ℝ) (hg' : SecondOrderClass g c x₀ g') (x : ∀ i, σ i) :
    M.energy x₀ + g' x₀ ≤ M.energy x + g' x := by
  have h1 := (pairwise_sandwich_of_class M g c hc x₀ g' hg' x).1
  have h2 := lowerModel_energy_eq_lowerExt M g c x₀ x₀
  rw [lowerExt_self] at h2
  have h3 := hmin x
  have h4 := hg'.2.1
  linarith

/-- **Sharp-minimum theorem for second-order envelopes.**  For symmetric nonnegative `c`, the
reference configuration `x₀` minimises `M.energy + g'` for *every* residual `g'` of the class if
and only if it minimises its own lower pairwise model: the certificate of
`secondOrder_certified_minimizer` is exact (for the converse, take the lower extremal
residual). -/
theorem secondOrder_certified_minimizer_iff [Fintype ι] [DecidableEq ι]
    [∀ i, DecidableEq (σ i)] (M : PairModel ℝ ι σ) (g : (∀ i, σ i) → ℝ) (c : ι → ι → ℝ)
    (hc : ∀ i j, c i j = c j i) (hc0 : ∀ i j, 0 ≤ c i j) (x₀ : ∀ i, σ i) :
    (∀ x, (lowerModel M g c x₀).energy x₀ ≤ (lowerModel M g c x₀).energy x) ↔
      ∀ g', SecondOrderClass g c x₀ g' → ∀ x, M.energy x₀ + g' x₀ ≤ M.energy x + g' x := by
  constructor
  · intro h g' hg' x
    exact secondOrder_certified_minimizer M g c hc x₀ h g' hg' x
  · intro h x
    have h1 := h _ (lowerExt_mem_class g c hc hc0 x₀) x
    have e1 := lowerModel_energy_eq_lowerExt M g c x₀ x
    have e2 := lowerModel_energy_eq_lowerExt M g c x₀ x₀
    linarith

/-! ### Non-vacuity and sharpness

Two binary sites, reference configuration `(0, 0)`, and the pure two-body coupling
`g x = ¼ · [x 0 = 1] · [x 1 = 1]`.  It is not additive, its mixed differences are bounded by
`c = ¼`, its star part vanishes identically, and at `x = (1, 1)` the remainder bound
`|g x - starPart g x₀ x| ≤ pairRemainder c x₀ x` reads `¼ ≤ ¼`: the theorem is sharp. -/

/-- Witness residual on two binary sites: the pure two-body coupling `¼ · [x 0 = 1] · [x 1 = 1]`. -/
noncomputable def couplingResidual (x : Config 2 2) : ℝ :=
  if x 0 = 1 ∧ x 1 = 1 then 1 / 4 else 0

/-- Second-order envelope constants of the witness: `c i j = ¼`. -/
noncomputable def couplingBound : Fin 2 → Fin 2 → ℝ := fun _ _ => 1 / 4

/-- The witness residual with rational values (evaluated by the kernel of Lean). -/
def couplingResidualQ (x : Config 2 2) : ℚ := if x 0 = 1 ∧ x 1 = 1 then 1 / 4 else 0

/-- The real witness residual is the cast of the rational one. -/
theorem couplingResidual_cast (x : Config 2 2) :
    couplingResidual x = (couplingResidualQ x : ℝ) := by
  unfold couplingResidual couplingResidualQ
  split_ifs <;> norm_num

/-- All mixed differences of the rational witness are at most `¼` in absolute value (exhaustive
evaluation in exact rational arithmetic). -/
theorem couplingResidualQ_mixed : ∀ (x : Config 2 2) (i j : Fin 2), i ≠ j → ∀ a b : Fin 2,
    |couplingResidualQ (Function.update (Function.update x i a) j b) -
      couplingResidualQ (Function.update x i a) - couplingResidualQ (Function.update x j b) +
      couplingResidualQ x| ≤ 1 / 4 := by decide +kernel

/-- The witness residual has the second-order envelope `c = ¼`. -/
theorem couplingResidual_mixedDiffBound : MixedDiffBound couplingResidual couplingBound := by
  intro x i j hij a b
  have h : ((|couplingResidualQ (Function.update (Function.update x i a) j b) -
      couplingResidualQ (Function.update x i a) - couplingResidualQ (Function.update x j b) +
      couplingResidualQ x| : ℚ) : ℝ) ≤ ((1 / 4 : ℚ) : ℝ) :=
    Rat.cast_le.mpr (couplingResidualQ_mixed x i j hij a b)
  push_cast at h
  simp only [couplingResidual_cast, couplingBound]
  exact h

/-- The star part of the witness around `(0, 0)` vanishes identically: no single-site
modification of the reference switches the coupling on. -/
theorem coupling_starPart (x : Config 2 2) : starPart couplingResidual ![0, 0] x = 0 := by
  simp [starPart, couplingResidual, Fin.sum_univ_two]

/-- The pairwise remainder of the witness at `(1, 1)` is `¼`: one unordered pair of changed
sites. -/
theorem coupling_pairRemainder :
    pairRemainder couplingBound (![0, 0] : Config 2 2) ![1, 1] = 1 / 4 := by
  norm_num [pairRemainder, changed, couplingBound, Fin.sum_univ_two]

/-- **Non-vacuity and sharpness of the remainder theorem.**  The coupling residual satisfies the
hypotheses of `secondOrder_remainder` with the symmetric, non-zero constants `c = ¼`; it is not
additive; and at `x = (1, 1)` with reference `(0, 0)` both sides of the remainder bound are equal
to `¼`. -/
theorem secondOrder_witness :
    MixedDiffBound couplingResidual couplingBound ∧
      (∀ i j, couplingBound i j = couplingBound j i) ∧
      ¬ MixedDiffBound couplingResidual (fun _ _ => 0) ∧
      |couplingResidual ![1, 1] - starPart couplingResidual ![0, 0] ![1, 1]| = 1 / 4 ∧
      pairRemainder couplingBound (![0, 0] : Config 2 2) ![1, 1] = 1 / 4 := by
  have hval : couplingResidual ![1, 1] = 1 / 4 := by simp [couplingResidual]
  refine ⟨couplingResidual_mixedDiffBound, fun _ _ => rfl, ?_, ?_, coupling_pairRemainder⟩
  · intro h
    have h1 := starPart_eq_of_additive couplingResidual h ![0, 0] ![1, 1]
    rw [coupling_starPart, hval] at h1
    norm_num at h1
  · rw [coupling_starPart, hval]
    norm_num

/-! ### An end-to-end kernel run

The explicit part favours state `1` at both sites (`E₀ = -(number of ones)`); the residual is
known only through the second-order envelope `c = ¼` and through lower bounds on its star
increments around `(0, 0)`.  The lower instance has the one-body table of `E₀` and the pair
entries `-⅛` on `(1, 1)` in both orientations; a single dual leaf certifies the bound `-9/4` for
it, and `verify_sound_secondOrder` transfers the bound to the true energy, for every residual of
the class. -/

/-- Explicit part of the kernel run: a unit field favouring state `1` at both sites, no explicit
pair term. -/
noncomputable def couplingModel : PairModel ℝ (Fin 2) (fun _ => Fin 2) where
  h := fun _ s => if s = 1 then -1 else 0
  J := fun _ _ _ _ => 0

/-- Rational lower instance of the kernel run: the one-body table of the explicit part (star
increments bounded below by `0`) and the pair corrections `-c / 2 = -⅛` on the entries whose two
states differ from the reference `(0, 0)`. -/
def couplingInstance : PairInstance 2 2 where
  h := fun _ s => if s = 1 then -1 else 0
  J := fun _ _ a b => if a = 1 ∧ b = 1 then -1 / 8 else 0

/-- A one-leaf certificate (no messages) for the lower instance. -/
def couplingCert : Cert 2 2 := .leaf (fun _ => -1) (fun _ _ => -1 / 8) (fun _ _ _ => 0)

/-- The kernel accepts the bound `-9/4` for the lower instance on the full box. -/
theorem couplingInstance_verified :
    verify couplingCert couplingInstance (fullDom 2 2) (-9 / 4) = true := by decide +kernel

/-- **The kernel run certifies a whole class of residuals.**  For *every* residual with mixed
differences at most `¼` whose star increments around `(0, 0)` are nonnegative, the true energy of
every configuration is at least `-9/4 + g (0, 0)` — obtained from the accepted pairwise
certificate, without evaluating the residual anywhere else. -/
theorem coupling_class_lower_bound (g : Config 2 2 → ℝ) (hg : MixedDiffBound g couplingBound)
    (hstar : ∀ i s, g ![0, 0] ≤ g (Function.update ![0, 0] i s)) (x : Config 2 2) :
    (-9 / 4 : ℝ) + g ![0, 0] ≤ couplingModel.energy x + g x := by
  have h := verify_sound_secondOrder couplingModel g couplingBound ![0, 0] hg (fun _ _ => rfl)
    couplingInstance ?_ ?_ couplingCert (fullDom 2 2) (-9 / 4) couplingInstance_verified x
    (inBox_fullDom x)
  · push_cast at h
    linarith
  · intro i a
    have h1 := hstar i a
    have h2 : ((couplingInstance.h i a : ℚ) : ℝ) = couplingModel.h i a := by
      simp only [couplingInstance, couplingModel]
      split_ifs <;> norm_num
    show ((couplingInstance.h i a : ℚ) : ℝ) ≤
      couplingModel.h i a + (g (Function.update ![0, 0] i a) - g ![0, 0])
    linarith
  · intro i j a b
    show ((couplingInstance.J i j a b : ℚ) : ℝ) ≤ couplingModel.J i j a b -
      couplingBound i j / 2 * (if a = (![0, 0] : Config 2 2) i then 0 else 1) *
        (if b = (![0, 0] : Config 2 2) j then 0 else 1)
    fin_cases i <;> fin_cases j <;> fin_cases a <;> fin_cases b <;>
      norm_num [couplingInstance, couplingModel, couplingBound]

/-- **Non-vacuity of the kernel statement.**  The coupling residual belongs to the class of
`coupling_class_lower_bound`, so the true energy `E₀ + g` of every configuration is at least the
certified `-9/4`; its value at `(1, 1)` is `-7/4`, so the certified bound is within `½` (twice
the pairwise remainder) of the optimum. -/
theorem secondOrder_kernel_witness :
    (∀ x : Config 2 2, (-9 / 4 : ℝ) ≤ couplingModel.energy x + couplingResidual x) ∧
      couplingModel.energy ![1, 1] + couplingResidual ![1, 1] = -7 / 4 := by
  have h0 : couplingResidual ![0, 0] = 0 := by simp [couplingResidual]
  have hnonneg : ∀ y : Config 2 2, 0 ≤ couplingResidual y := by
    intro y
    unfold couplingResidual
    split_ifs <;> norm_num
  refine ⟨fun x => ?_, ?_⟩
  · have h := coupling_class_lower_bound couplingResidual couplingResidual_mixedDiffBound
      (fun i s => by rw [h0]; exact hnonneg _) x
    rw [h0] at h
    linarith
  · norm_num [PairModel.energy, couplingModel, couplingResidual, Fin.sum_univ_two]

/-! ### A certified minimiser

Two binary sites, the coupling residual and `c = ¼` once more, with an explicit part in which
every excitation (state `1`) costs `⅛`.  The pairwise remainder around `(0, 0)` never exceeds the
excitation energy, so the reference minimises its own lower model, and
`secondOrder_certified_minimizer` certifies `(0, 0)` as a minimiser of the true energy for every
residual of the class — from the three star evaluations of the residual. -/

/-- Explicit part of the minimiser witness: every excitation (state `1`) costs `⅛`, no explicit
pair term. -/
noncomputable def excitationModel : PairModel ℝ (Fin 2) (fun _ => Fin 2) where
  h := fun _ s => if s = 1 then 1 / 8 else 0
  J := fun _ _ _ _ => 0

/-- The pairwise remainder of the witness never exceeds the excitation energy (four cases). -/
theorem excitation_pairRemainder_le (x : Config 2 2) :
    pairRemainder couplingBound (![0, 0] : Config 2 2) x ≤ excitationModel.energy x := by
  have two : ∀ t : Fin 2, t = 0 ∨ t = 1 := by decide
  have hx : x = ![x 0, x 1] := by
    funext i
    fin_cases i <;> rfl
  rcases two (x 0) with h0 | h0 <;> rcases two (x 1) with h1 | h1 <;> rw [hx, h0, h1] <;>
    norm_num [pairRemainder, changed, couplingBound, excitationModel, PairModel.energy,
      Fin.sum_univ_two]

/-- The reference `(0, 0)` minimises its own lower model: the hypothesis of the sharp-minimum
certificate holds for the witness. -/
theorem excitation_lowerModel_min (x : Config 2 2) :
    (lowerModel excitationModel couplingResidual couplingBound ![0, 0]).energy ![0, 0] ≤
      (lowerModel excitationModel couplingResidual couplingBound ![0, 0]).energy x := by
  have h1 := lowerModel_energy excitationModel couplingResidual couplingBound ![0, 0] x
  have h2 := lowerModel_energy excitationModel couplingResidual couplingBound ![0, 0] ![0, 0]
  rw [coupling_starPart] at h1 h2
  rw [pairRemainder_self] at h2
  have h3 := excitation_pairRemainder_le x
  have h4 : excitationModel.energy ![0, 0] = 0 := by
    simp [PairModel.energy, excitationModel]
  linarith

/-- **Non-vacuity of the sharp-minimum certificate.**  For the (non-additive) coupling residual
with `c = ¼` and excitation cost `⅛`: the reference `(0, 0)` minimises its own lower model; the
class of residuals consistent with the star data is non-empty (it contains the coupling residual
itself); and `(0, 0)` minimises the true energy for every residual of the class. -/
theorem secondOrder_minimizer_witness :
    (∀ x : Config 2 2,
        (lowerModel excitationModel couplingResidual couplingBound ![0, 0]).energy ![0, 0] ≤
          (lowerModel excitationModel couplingResidual couplingBound ![0, 0]).energy x) ∧
      SecondOrderClass couplingResidual couplingBound ![0, 0] couplingResidual ∧
      ∀ g' : Config 2 2 → ℝ, SecondOrderClass couplingResidual couplingBound ![0, 0] g' →
        ∀ x : Config 2 2,
          excitationModel.energy ![0, 0] + g' ![0, 0] ≤ excitationModel.energy x + g' x :=
  ⟨excitation_lowerModel_min, secondOrderClass_self couplingResidual_mixedDiffBound _,
    fun g' hg' x => secondOrder_certified_minimizer excitationModel couplingResidual
      couplingBound (fun _ _ => rfl) ![0, 0] excitation_lowerModel_min g' hg' x⟩

end MetricChain
