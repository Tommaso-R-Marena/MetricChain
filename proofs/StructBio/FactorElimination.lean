import Mathlib
import proofs.Core.Rounding
import proofs.Frontiers.PartitionProduct

/-!
# Rule semantics of the partition-function checker: elimination, pruning, relaxation, rounding

Structural & Computational Biology division (branch `research/structural-biology`).

The division's checker of partition-function ("Z") certificates (`src/metricchain_sb/zcheck.py`,
with `zcert.py`, `itables.py`, `expo.py`) replays a recipe on a pairwise energy model over a box
of configurations.  It conditions on the states of a site, removes thermally dominated states,
replaces a pair table by a sum of two one-body tables up to a bounded residual, and sums the
sites out one at a time on tables of rational bounds for the Boltzmann factors; these bounds
come from a certified exponential that is rounded outward after every squaring.  This file
machine-checks the mathematical statement behind each of these rules — items R-1 … R-4 of the
request STRUCTBIO-REQ-0003 (`docs/collaboration/requests/structural-biology/`).

## What is proved, and what is not

All statements are about finite sums of functions on configurations over a box `∏ D`.  The
vocabulary of the kernel files is reused unchanged: `Config`, `Dom`, `InBox`, `Dom.fix`,
`Dom.remove`, `inBox_remove_update` (`CertificateAlgebra.lean`), `boxFinset`, `boxFinset_remove`
(`PartitionCertificate.lean`), `inBox_fix_iff` (`PartitionProduct.lean`), `update_injOn`
(`Dominance.lean`), `partitionFn` (`Core/Basic.lean`), `expLo`, `expHi`, `exp_enclosure`
(`Core/Rounding.lean`).

These are *rule semantics*, not an executable kernel.  Nothing is proved here about the Python
implementation: neither that its tables represent the functions and sums below, nor that its
arithmetic rounds in the directions that the hypotheses of this file require.

## Scalars

The identities hold for functions with values in any commutative semiring `R`, the inequalities
in any ordered commutative semiring.  Two cases matter: `R = ℚ` (tables of rational bounds) and
`R = ℝ` (the Boltzmann weights `exp (-β E x)` themselves, which are not rational, and to which
the prune and relax steps of the checker apply).  The kernel files state the corresponding
facts for the rational weights of pairwise instances (`WInstance`).

No hypothesis is assumed that the proofs do not use.  In particular the relaxation of a pair
needs neither `i ≠ j` nor a sign of `lo`, `hi`, `u`, `v` (the request states it with `0 ≤ lo` and
`u, v ≥ 0`), the monotonicity of sums needs no sign, and where weights have to be nonnegative
they have to be so on the box only.

## Contents

Below `y[i ↦ a]` stands for `Function.update y i a`, `D[i ↦ a]` for `D.fix i a` (site `i`
pinned to the state `a`) and `D ∖ᵢ r` for `D.remove i r`.

**R-1, conditioning and elimination.**

* `sum_boxFinset_branch` — `∑ x ∈ ∏ D, f x = ∑ a ∈ D i, ∑ x ∈ ∏ D[i ↦ a], f x`
  (`WInstance.Z_branch` for an arbitrary summand).
* `sum_boxFinset_sumOut` — the same with every fibre moved to one pinned box:
  `∑ x ∈ ∏ D, f x = ∑ y ∈ ∏ D[i ↦ p], ∑ a ∈ D i, f (y[i ↦ a])` for any pin `p`
  (`sum_boxFinset_repin` moves a fibre; it is `sum_boxFinset_fix` for general scalars).
* `sum_boxFinset_elim` — **general elimination**: if `G` does not depend on site `i`, then
  `∑ x ∈ ∏ D, F x * G x = ∑ y ∈ ∏ D[i ↦ p], (∑ a ∈ D i, F (y[i ↦ a])) * G y`.
  With `F` the product of the factors that mention site `i` and `G` the product of the others
  this is one step of bucket (variable) elimination.  The number of neighbours of `i` is not
  bounded: the kernel rules `elim1`, `elim2` of `PartitionProduct.lean` are limited to two
  neighbours because their result has to be a pairwise instance again, a limit of that type and
  not of the identity (`WInstance.Z_sumOut`).
* `sumOut_update_self`, `sumOut_update_of_invariant` — the new factor
  `y ↦ ∑ a ∈ D i, F (y[i ↦ a])` does not depend on site `i`, nor on any site on which `F` does
  not depend.  So after a step no factor depends on the eliminated site, the new factor depends
  only on sites on which `F` depended, and the rule can be applied to the next site.
* `sum_boxFinset_mono`, `sum_boxFinset_prod_mono` — **interval tables**: sums over a box are
  monotone in the summand, and for factors with `0 ≤ lo e ≤ f e ≤ hi e` on the box the sum of
  the product of the lower (upper) tables bounds the sum of the product of the factors from
  below (above).

**R-2, thermal pruning.**

* `sum_boxFinset_prune` — if `w ≥ 0` on the box, `t ∈ D i`, `t ≠ r`, `0 ≤ ρ` and
  `w x ≤ ρ * w (x[i ↦ t])` for every `x` of the box with `x i = r`, then
  `∑ x ∈ ∏ (D ∖ᵢ r), w x ≤ ∑ x ∈ ∏ D, w x ≤ (1 + ρ) * ∑ x ∈ ∏ (D ∖ᵢ r), w x`.
  This is the inequality inside `zprune_sound` for an arbitrary weight function, so that it
  composes with any enclosure of the pruned sum.
* `partitionFn_prune` — its energy form, the prune step of the checker: `w x = exp (-β E x)`
  and `ρ = exp (-β γ)` for a dominance margin `γ` (`thermal_dee` of `Dominance.lean` in the
  vocabulary of `Dom`).

**R-3, product-form relaxation.**

* `sum_boxFinset_relax` — termwise comparison: `lo * w' x ≤ w x ≤ hi * w' x` on the box gives
  `lo * ∑ w' ≤ ∑ w ≤ hi * ∑ w'`.
* `sum_boxFinset_relax_pair` — a factor `P (x i) (x j)` with
  `lo * (u a * v b) ≤ P a b ≤ hi * (u a * v b)` on `D i × D j` is replaced by the product
  `u (x i) * v (x j)` at the price of the factors `lo` and `hi`, the remaining weight being
  nonnegative on the box.  (With `u = v = 1` a pair factor is replaced by constants, as in the
  leaf and cut rules of the kernel.)
* `partitionFn_relax_pair` — its energy form, the relax step of the checker: if
  `E x = E' x + ε (x i) (x j)` on the box with `rlo ≤ ε a b ≤ rhi` on `D i × D j` and `0 ≤ β`,
  then `exp (-β rhi) * Z' ≤ Z ≤ exp (-β rlo) * Z'`.

**R-4, the certified exponential with rounding after every squaring.**

* `iterate_sq_rounded_down`, `iterate_sq_rounded_up` — for nonnegative rationals, `m` squarings
  each followed by rounding down (up) give at most (at least) the exact `2 ^ m`-th power.
* `exp_enclosure_rounded` — hence the rounded squarings of a lower and an upper Taylor value at
  the reduced argument `q / 2 ^ K` bracket `exp q`.  The two rational comparisons with `expLo`
  and `expHi` are `iterate_sq_rounded_down_le_expLo` and `expHi_le_iterate_sq_rounded_up`; the
  real statement then is `exp_enclosure`.
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-! ### R-1: conditioning on a site and summing a site out (identities) -/

section Identities

variable {R : Type*} [CommSemiring R]

/-- **Conditioning on a site** (the branch rule for an arbitrary summand).  The sum of a function
over the box `∏ D` is the sum, over the states `a` of site `i`, of its sums over the boxes with
site `i` fixed to `a`.  This is `WInstance.Z_branch` with the Boltzmann weight replaced by any
function with values in a commutative semiring.  The outer sum runs over the set
`(D i).toFinset`: repetitions in the list `D i` do not matter. -/
theorem sum_boxFinset_branch (D : Dom n k) (i : Fin n) (f : Config n k → R) :
    ∑ x ∈ boxFinset D, f x = ∑ a ∈ (D i).toFinset, ∑ x ∈ boxFinset (D.fix i a), f x := by
  have hmaps : ∀ x ∈ boxFinset D, x i ∈ (D i).toFinset := fun x hx =>
    List.mem_toFinset.mpr (mem_boxFinset.mp hx i)
  rw [← Finset.sum_fiberwise_of_maps_to hmaps]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr _ (fun _ _ => rfl)
  ext x
  simp only [Finset.mem_filter, mem_boxFinset, inBox_fix_iff]
  constructor
  · rintro ⟨hx, hxa⟩
    exact ⟨hxa, fun m _ => hx m⟩
  · rintro ⟨hxa, hx⟩
    refine ⟨fun m => ?_, hxa⟩
    by_cases hm : m = i
    · rw [hm, hxa]
      exact List.mem_toFinset.mp ha
    · exact hx m hm

/-- Changing the state of the fixed site is a bijection between the two pinned boxes (summation
form).  This is `sum_boxFinset_fix` of `PartitionProduct.lean`, which is stated for rational
summands, for summands with values in a commutative semiring; the proof is the same. -/
theorem sum_boxFinset_repin (D : Dom n k) (i : Fin n) (a p : Fin k) (f : Config n k → R) :
    ∑ x ∈ boxFinset (D.fix i a), f x =
      ∑ y ∈ boxFinset (D.fix i p), f (Function.update y i a) := by
  have hmaps : ∀ a p : Fin k, ∀ y ∈ boxFinset (D.fix i p),
      Function.update y i a ∈ boxFinset (D.fix i a) := by
    intro a p y hy
    rw [mem_boxFinset, inBox_fix_iff] at hy ⊢
    refine ⟨Function.update_self i a y, fun m hm => ?_⟩
    rw [Function.update_of_ne hm]
    exact hy.2 m hm
  have hinv : ∀ a p : Fin k, ∀ y ∈ boxFinset (D.fix i p),
      Function.update (Function.update y i a) i p = y := by
    intro a p y hy
    rw [mem_boxFinset, inBox_fix_iff] at hy
    rw [Function.update_idem, ← hy.1, Function.update_eq_self]
  symm
  exact Finset.sum_nbij' (fun y => Function.update y i a) (fun x => Function.update x i p)
    (hmaps a p) (hmaps p a) (hinv a p) (hinv p a) (fun _ _ => rfl)

/-- **Summing a site out.**  The sum of a function over the box `∏ D` is the sum, over the box
with site `i` pinned to `p`, of its sums over the states of site `i`.  The pin `p` is arbitrary;
it need not lie in `D i`. -/
theorem sum_boxFinset_sumOut (D : Dom n k) (i : Fin n) (p : Fin k) (f : Config n k → R) :
    ∑ x ∈ boxFinset D, f x =
      ∑ y ∈ boxFinset (D.fix i p), ∑ a ∈ (D i).toFinset, f (Function.update y i a) := by
  rw [sum_boxFinset_branch D i, Finset.sum_comm]
  exact Finset.sum_congr rfl fun a _ => sum_boxFinset_repin D i a p f

/-- **General elimination** (item R-1 of STRUCTBIO-REQ-0003: summing a site out against an
arbitrary product).  If `G` does not depend on the state of site `i`, the sum of `F * G` over the
box `∏ D` is the sum, over the box with site `i` pinned to `p`, of the new factor
`∑ a ∈ D i, F (y[i ↦ a])` times `G y`.  With `F` the product of the factors that mention site `i`
and `G` the product of the others this is one step of bucket elimination, whatever the number of
neighbours of `i`.  It is an identity: there is no sign condition, and the pin `p` is arbitrary. -/
theorem sum_boxFinset_elim (D : Dom n k) (i : Fin n) (p : Fin k) (F G : Config n k → R)
    (hG : ∀ x a, G (Function.update x i a) = G x) :
    ∑ x ∈ boxFinset D, F x * G x =
      ∑ y ∈ boxFinset (D.fix i p), (∑ a ∈ (D i).toFinset, F (Function.update y i a)) * G y := by
  rw [sum_boxFinset_sumOut D i p]
  apply Finset.sum_congr rfl
  intro y _
  rw [Finset.sum_mul]
  exact Finset.sum_congr rfl fun a _ => by rw [hG]

/-- The factor produced by summing site `i` out does not depend on the state of site `i`: it
satisfies the condition that `sum_boxFinset_elim` imposes on `G`.  So after an elimination step
neither factor of the new summand depends on the eliminated site, and the rule can be applied to
the next site. -/
theorem sumOut_update_self (D : Dom n k) (i : Fin n) (F : Config n k → R) (y : Config n k)
    (b : Fin k) :
    ∑ a ∈ (D i).toFinset, F (Function.update (Function.update y i b) i a) =
      ∑ a ∈ (D i).toFinset, F (Function.update y i a) := by
  simp only [Function.update_idem]

/-- The factor produced by summing site `i` out does not depend on the state of a site `m` on
which `F` does not depend: the sites it depends on are among those of `F` other than `i`.  (For
`m = i` no hypothesis on `F` is needed, see `sumOut_update_self`.) -/
theorem sumOut_update_of_invariant (D : Dom n k) (i m : Fin n) (F : Config n k → R)
    (hF : ∀ x c, F (Function.update x m c) = F x) (y : Config n k) (c : Fin k) :
    ∑ a ∈ (D i).toFinset, F (Function.update (Function.update y m c) i a) =
      ∑ a ∈ (D i).toFinset, F (Function.update y i a) := by
  apply Finset.sum_congr rfl
  intro a _
  by_cases hm : m = i
  · rw [hm, Function.update_idem]
  · rw [Function.update_comm hm, hF]

end Identities

/-! ### Inequalities: interval tables, thermal pruning, product-form relaxation -/

section Inequalities

variable {R : Type*} [CommSemiring R] [PartialOrder R] [IsOrderedRing R]

/-- **Monotonicity of box sums** (interval tables, item R-1).  If `wlo ≤ w ≤ whi` pointwise on
the box, the sums over the box are ordered in the same way.  The scalars form an ordered
commutative semiring; with `R = ℝ` and `wlo`, `whi` the casts of rational tables, a real sum is
compared with the casts of two rational sums.  No sign condition is needed for sums; it is
needed for products of tables, see `sum_boxFinset_prod_mono`. -/
theorem sum_boxFinset_mono (D : Dom n k) (wlo w whi : Config n k → R)
    (h : ∀ x, InBox D x → wlo x ≤ w x ∧ w x ≤ whi x) :
    ∑ x ∈ boxFinset D, wlo x ≤ ∑ x ∈ boxFinset D, w x ∧
      ∑ x ∈ boxFinset D, w x ≤ ∑ x ∈ boxFinset D, whi x :=
  ⟨Finset.sum_le_sum fun x hx => (h x (mem_boxFinset.mp hx)).1,
    Finset.sum_le_sum fun x hx => (h x (mem_boxFinset.mp hx)).2⟩

/-- **Interval tables: products of factors.**  For a finite family of factors with
`0 ≤ lo e x ≤ f e x ≤ hi e x` on the box, the sum over the box of the product of the lower
tables is at most the sum of the product of the factors, which is at most the sum of the product
of the upper tables. -/
theorem sum_boxFinset_prod_mono (D : Dom n k) {ι : Type*} (s : Finset ι)
    (lo f hi : ι → Config n k → R)
    (h : ∀ e ∈ s, ∀ x, InBox D x → 0 ≤ lo e x ∧ lo e x ≤ f e x ∧ f e x ≤ hi e x) :
    ∑ x ∈ boxFinset D, ∏ e ∈ s, lo e x ≤ ∑ x ∈ boxFinset D, ∏ e ∈ s, f e x ∧
      ∑ x ∈ boxFinset D, ∏ e ∈ s, f e x ≤ ∑ x ∈ boxFinset D, ∏ e ∈ s, hi e x := by
  apply sum_boxFinset_mono
  intro x hx
  exact ⟨Finset.prod_le_prod (fun e he => (h e he x hx).1) fun e he => (h e he x hx).2.1,
    Finset.prod_le_prod (fun e he => (h e he x hx).1.trans (h e he x hx).2.1)
      fun e he => (h e he x hx).2.2⟩

/-- **Thermal pruning, composable form** (item R-2).  Let `w` be nonnegative on the box, let
`t ∈ D i` be different from `r`, and let `0 ≤ ρ`.  If `w x ≤ ρ * w (x[i ↦ t])` for every `x` of
the box with `x i = r`, then removing the state `r` of site `i` changes the sum of `w` over the
box by a factor in `[1, 1 + ρ]`: the removed part of the box is carried injectively into the
remaining part by `x ↦ x[i ↦ t]`.  This is the inequality inside `zprune_sound`, for a weight
function that need not be that of a pairwise instance, so that it composes with any enclosure of
the pruned sum.

`D.remove i r` deletes every occurrence of `r` from the list `D i`, and `boxFinset` only sees
the set of the listed states: there is no hypothesis on multiplicities, and none that `r ∈ D i`
(if it is not, the two boxes coincide). -/
theorem sum_boxFinset_prune (D : Dom n k) (i : Fin n) (r t : Fin k) (w : Config n k → R) (ρ : R)
    (hw : ∀ x, InBox D x → 0 ≤ w x) (ht : t ∈ D i) (htr : t ≠ r) (hρ : 0 ≤ ρ)
    (hdom : ∀ x, InBox D x → x i = r → w x ≤ ρ * w (Function.update x i t)) :
    ∑ x ∈ boxFinset (D.remove i r), w x ≤ ∑ x ∈ boxFinset D, w x ∧
      ∑ x ∈ boxFinset D, w x ≤ (1 + ρ) * ∑ x ∈ boxFinset (D.remove i r), w x := by
  -- `A`: the removed part of the box; `S`: the remaining part
  set A := (boxFinset D).filter fun x => x i = r
  set S := boxFinset (D.remove i r) with hSdef
  have hA : ∀ x ∈ A, InBox D x ∧ x i = r := fun x hx =>
    ⟨mem_boxFinset.mp (Finset.mem_filter.mp hx).1, (Finset.mem_filter.mp hx).2⟩
  have hS : ∀ y ∈ S, InBox D y := by
    intro y hy
    rw [hSdef, boxFinset_remove] at hy
    exact mem_boxFinset.mp (Finset.mem_filter.mp hy).1
  have hsplit : ∑ x ∈ boxFinset D, w x = ∑ x ∈ A, w x + ∑ x ∈ S, w x := by
    rw [hSdef, boxFinset_remove]
    exact (Finset.sum_filter_add_sum_filter_not (boxFinset D) (fun x => x i = r) w).symm
  have hA0 : 0 ≤ ∑ x ∈ A, w x := Finset.sum_nonneg fun x hx => hw x (hA x hx).1
  -- the transport map `x ↦ x[i ↦ t]` sends `A` into `S` ...
  have himg : A.image (fun x : Config n k => Function.update x i t) ⊆ S := by
    intro y hy
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hy
    exact mem_boxFinset.mpr (inBox_remove_update (hA x hx).1 i r t ht htr)
  -- ... injectively (`update_injOn`), and `w x ≤ ρ * w (x[i ↦ t])` on `A`
  have htrans : ∑ x ∈ A, w x ≤ ρ * ∑ x ∈ S, w x := by
    calc ∑ x ∈ A, w x ≤ ∑ x ∈ A, ρ * w (Function.update x i t) :=
          Finset.sum_le_sum fun x hx => hdom x (hA x hx).1 (hA x hx).2
      _ = ρ * ∑ y ∈ A.image (fun x : Config n k => Function.update x i t), w y := by
          rw [Finset.sum_image (update_injOn i r t (boxFinset D)), Finset.mul_sum]
      _ ≤ ρ * ∑ y ∈ S, w y :=
          mul_le_mul_of_nonneg_left
            (Finset.sum_le_sum_of_subset_of_nonneg himg fun y hy _ => hw y (hS y hy)) hρ
  rw [hsplit]
  refine ⟨le_add_of_nonneg_left hA0, ?_⟩
  calc ∑ x ∈ A, w x + ∑ x ∈ S, w x ≤ ρ * ∑ x ∈ S, w x + ∑ x ∈ S, w x :=
        add_le_add htrans le_rfl
    _ = (1 + ρ) * ∑ x ∈ S, w x := by ring

/-- **Termwise comparison** (item R-3, general form).  If `lo * w' x ≤ w x ≤ hi * w' x` for
every `x` of the box, then `lo * ∑ w' ≤ ∑ w ≤ hi * ∑ w'` for the sums over the box.  There is no
sign condition on `lo`, `hi`, `w`, `w'`. -/
theorem sum_boxFinset_relax (D : Dom n k) (w w' : Config n k → R) (lo hi : R)
    (h : ∀ x, InBox D x → lo * w' x ≤ w x ∧ w x ≤ hi * w' x) :
    lo * ∑ x ∈ boxFinset D, w' x ≤ ∑ x ∈ boxFinset D, w x ∧
      ∑ x ∈ boxFinset D, w x ≤ hi * ∑ x ∈ boxFinset D, w' x := by
  rw [Finset.mul_sum, Finset.mul_sum]
  exact ⟨Finset.sum_le_sum fun x hx => (h x (mem_boxFinset.mp hx)).1,
    Finset.sum_le_sum fun x hx => (h x (mem_boxFinset.mp hx)).2⟩

/-- **Product-form relaxation of a pair, weight form** (item R-3).  Let the weight of a
configuration be `P (x i) (x j) * W x`: a factor of the states of the sites `i` and `j`, times a
remaining weight `W` that is nonnegative on the box.  If
`lo * (u a * v b) ≤ P a b ≤ hi * (u a * v b)` for all `a ∈ D i`, `b ∈ D j`, then replacing the
factor `P (x i) (x j)` by the product `u (x i) * v (x j)` changes the sum over the box by a
factor in `[lo, hi]`.  Neither `i ≠ j` nor a sign condition on `lo`, `hi`, `u`, `v` is needed. -/
theorem sum_boxFinset_relax_pair (D : Dom n k) (i j : Fin n) (u v : Fin k → R)
    (P : Fin k → Fin k → R) (W : Config n k → R) (lo hi : R)
    (hW : ∀ x, InBox D x → 0 ≤ W x)
    (h : ∀ a ∈ D i, ∀ b ∈ D j, lo * (u a * v b) ≤ P a b ∧ P a b ≤ hi * (u a * v b)) :
    lo * ∑ x ∈ boxFinset D, u (x i) * v (x j) * W x ≤ ∑ x ∈ boxFinset D, P (x i) (x j) * W x ∧
      ∑ x ∈ boxFinset D, P (x i) (x j) * W x ≤
        hi * ∑ x ∈ boxFinset D, u (x i) * v (x j) * W x := by
  apply sum_boxFinset_relax
  intro x hx
  have hP := h (x i) (hx i) (x j) (hx j)
  constructor
  · calc lo * (u (x i) * v (x j) * W x) = lo * (u (x i) * v (x j)) * W x := by ring
      _ ≤ P (x i) (x j) * W x := mul_le_mul_of_nonneg_right hP.1 (hW x hx)
  · calc P (x i) (x j) * W x ≤ hi * (u (x i) * v (x j)) * W x :=
          mul_le_mul_of_nonneg_right hP.2 (hW x hx)
      _ = hi * (u (x i) * v (x j) * W x) := by ring

end Inequalities

/-! ### Energy forms of the prune and relax steps (real Boltzmann weights) -/

/-- **Thermal pruning, energy form** (the prune step of the checker): `sum_boxFinset_prune` for
the real weights `exp (-β E x)` with `ρ = exp (-β γ)`.  If on the box the state `r` of site `i`
is dominated by a state `t ∈ D i`, `t ≠ r`, with margin `γ`, and `0 ≤ β`, then deleting `r`
changes the partition function of the box by a factor in `[1, 1 + exp (-β γ)]`.  (`thermal_dee`
of `Dominance.lean` is this statement for domains given as finite sets.) -/
theorem partitionFn_prune (D : Dom n k) (i : Fin n) (r t : Fin k) {β γ : ℝ} (hβ : 0 ≤ β)
    (E : Config n k → ℝ) (ht : t ∈ D i) (htr : t ≠ r)
    (hdom : ∀ x, InBox D x → x i = r → E (Function.update x i t) + γ ≤ E x) :
    partitionFn β E (boxFinset (D.remove i r)) ≤ partitionFn β E (boxFinset D) ∧
      partitionFn β E (boxFinset D) ≤
        (1 + Real.exp (-β * γ)) * partitionFn β E (boxFinset (D.remove i r)) := by
  unfold partitionFn
  apply sum_boxFinset_prune D i r t _ _ (fun x _ => (Real.exp_pos _).le) ht htr
    (Real.exp_pos _).le
  intro x hx hxr
  rw [← Real.exp_add]
  apply Real.exp_le_exp.mpr
  have := mul_le_mul_of_nonneg_left (hdom x hx hxr) hβ
  linarith

/-- **Product-form relaxation of a pair, energy form** (the relax step of the checker).  If on
the box `E x = E' x + ε (x i) (x j)` with `rlo ≤ ε a b ≤ rhi` for all `a ∈ D i`, `b ∈ D j`, and
`0 ≤ β`, then the partition functions `Z`, `Z'` of `E`, `E'` over the box satisfy
`exp (-β rhi) * Z' ≤ Z ≤ exp (-β rlo) * Z'`.  In the checker `E'` is the working model with the
pair table of `(i, j)` removed and two one-body tables `f`, `g` added at `i` and `j`, and `ε` is
the residual of the pair table after subtraction of `f` and `g`. -/
theorem partitionFn_relax_pair (D : Dom n k) (i j : Fin n) {β : ℝ} (hβ : 0 ≤ β)
    (E E' : Config n k → ℝ) (ε : Fin k → Fin k → ℝ) (rlo rhi : ℝ)
    (hE : ∀ x, InBox D x → E x = E' x + ε (x i) (x j))
    (hε : ∀ a ∈ D i, ∀ b ∈ D j, rlo ≤ ε a b ∧ ε a b ≤ rhi) :
    Real.exp (-β * rhi) * partitionFn β E' (boxFinset D) ≤ partitionFn β E (boxFinset D) ∧
      partitionFn β E (boxFinset D) ≤ Real.exp (-β * rlo) * partitionFn β E' (boxFinset D) := by
  unfold partitionFn
  apply sum_boxFinset_relax
  intro x hx
  have hr := hε (x i) (hx i) (x j) (hx j)
  have h1 := mul_le_mul_of_nonneg_left hr.1 hβ
  have h2 := mul_le_mul_of_nonneg_left hr.2 hβ
  rw [hE x hx, ← Real.exp_add, ← Real.exp_add]
  exact ⟨Real.exp_le_exp.mpr (by linarith), Real.exp_le_exp.mpr (by linarith)⟩

/-! ### R-4: repeated squaring with outward rounding, and the rounded certified exponential -/

/-- **Repeated squaring with rounding down** (item R-4).  Let `rd` send every nonnegative
rational to a nonnegative rational that is not larger.  Starting from `0 ≤ a' ≤ a`, squaring `m`
times and applying `rd` after every squaring gives a nonnegative number that is at most the exact
power `a ^ 2 ^ m`. -/
theorem iterate_sq_rounded_down (rd : ℚ → ℚ) (hrd : ∀ x, 0 ≤ x → 0 ≤ rd x ∧ rd x ≤ x) (m : ℕ)
    {a' a : ℚ} (h0 : 0 ≤ a') (h : a' ≤ a) :
    0 ≤ (fun y => rd (y ^ 2))^[m] a' ∧ (fun y => rd (y ^ 2))^[m] a' ≤ a ^ (2 ^ m) := by
  induction m generalizing a' a with
  | zero =>
    rw [Function.iterate_zero_apply, pow_zero, pow_one]
    exact ⟨h0, h⟩
  | succ m ih =>
    have hsq := hrd (a' ^ 2) (sq_nonneg a')
    rw [Function.iterate_succ_apply, pow_succ 2 m, pow_mul']
    exact ih hsq.1 (hsq.2.trans (pow_le_pow_left₀ h0 h 2))

/-- **Repeated squaring with rounding up** (item R-4).  Let `ru` send every nonnegative rational
to a rational that is not smaller.  Starting from `0 ≤ a ≤ a'`, squaring `m` times and applying
`ru` after every squaring gives a number that is at least the exact power `a ^ 2 ^ m`. -/
theorem iterate_sq_rounded_up (ru : ℚ → ℚ) (hru : ∀ x, 0 ≤ x → x ≤ ru x) (m : ℕ)
    {a a' : ℚ} (h0 : 0 ≤ a) (h : a ≤ a') :
    a ^ (2 ^ m) ≤ (fun y => ru (y ^ 2))^[m] a' := by
  induction m generalizing a a' with
  | zero =>
    rw [Function.iterate_zero_apply, pow_zero, pow_one]
    exact h
  | succ m ih =>
    rw [Function.iterate_succ_apply, pow_succ 2 m, pow_mul']
    exact ih (sq_nonneg a) ((pow_le_pow_left₀ h0 h 2).trans (hru (a' ^ 2) (sq_nonneg a')))

/-- The upper Taylor value `expTaylor N x + expErr N x` is positive on the unit interval: it is
at least `exp x`. -/
theorem expTaylor_add_expErr_pos {N : ℕ} (hN : 0 < N) {x : ℚ} (hx : |x| ≤ 1) :
    0 < expTaylor N x + expErr N x := by
  have hb := abs_le.mp (abs_exp_sub_expTaylor_le hN hx)
  have hpos : (0 : ℝ) < ((expTaylor N x + expErr N x : ℚ) : ℝ) := by
    push_cast
    linarith [hb.2, Real.exp_pos (x : ℝ)]
  exact_mod_cast hpos

/-- The rounded-down squarings stay below `expLo`.  If `0 ≤ lo0` is at most the clipped lower
Taylor value at the reduced argument `q / 2 ^ K`, then `K` squarings, each followed by rounding
down, give a nonnegative rational that is at most `expLo N K q`. -/
theorem iterate_sq_rounded_down_le_expLo (N K : ℕ) (q : ℚ) (rd : ℚ → ℚ)
    (hrd : ∀ x, 0 ≤ x → 0 ≤ rd x ∧ rd x ≤ x) {lo0 : ℚ} (hlo0 : 0 ≤ lo0)
    (hlo : lo0 ≤ max 0 (expTaylor N (q / 2 ^ K) - expErr N (q / 2 ^ K))) :
    0 ≤ (fun y => rd (y ^ 2))^[K] lo0 ∧ (fun y => rd (y ^ 2))^[K] lo0 ≤ expLo N K q :=
  iterate_sq_rounded_down rd hrd K hlo0 hlo

/-- The rounded-up squarings stay above `expHi`.  For `N > 0` Taylor terms and `|q| ≤ 2 ^ K`, if
`hi0` is at least the upper Taylor value at the reduced argument `q / 2 ^ K`, then `K`
squarings, each followed by rounding up, give a rational that is at least `expHi N K q`. -/
theorem expHi_le_iterate_sq_rounded_up (N K : ℕ) (hN : 0 < N) (q : ℚ) (hq : |q| ≤ 2 ^ K)
    (ru : ℚ → ℚ) (hru : ∀ x, 0 ≤ x → x ≤ ru x) {hi0 : ℚ}
    (hhi : expTaylor N (q / 2 ^ K) + expErr N (q / 2 ^ K) ≤ hi0) :
    expHi N K q ≤ (fun y => ru (y ^ 2))^[K] hi0 := by
  have h2k : (0 : ℚ) < 2 ^ K := by positivity
  have hy1 : |q / 2 ^ K| ≤ 1 := by
    rw [abs_div, abs_of_pos h2k]
    exact (div_le_one h2k).mpr hq
  exact iterate_sq_rounded_up ru hru K (expTaylor_add_expErr_pos hN hy1).le hhi

/-- **The certified exponential with rounding after every squaring** (item R-4).  For `N > 0`
Taylor terms and `K` halvings with `|q| ≤ 2 ^ K`, let `lo0 ≥ 0` be at most the clipped lower
Taylor value and `hi0` at least the upper Taylor value at the reduced argument `q / 2 ^ K` (the
two values themselves, or the two values rounded outward).  Then `K` squarings, each followed by
rounding down for the lower value and by rounding up for the upper value, bracket the real number
`exp q`.  With `rd = ru = id` and the two Taylor values themselves this is `exp_enclosure`. -/
theorem exp_enclosure_rounded (N K : ℕ) (hN : 0 < N) (q : ℚ) (hq : |q| ≤ 2 ^ K)
    (rd ru : ℚ → ℚ) (hrd : ∀ x, 0 ≤ x → 0 ≤ rd x ∧ rd x ≤ x) (hru : ∀ x, 0 ≤ x → x ≤ ru x)
    {lo0 hi0 : ℚ} (hlo0 : 0 ≤ lo0)
    (hlo : lo0 ≤ max 0 (expTaylor N (q / 2 ^ K) - expErr N (q / 2 ^ K)))
    (hhi : expTaylor N (q / 2 ^ K) + expErr N (q / 2 ^ K) ≤ hi0) :
    (((fun y => rd (y ^ 2))^[K] lo0 : ℚ) : ℝ) ≤ Real.exp (q : ℝ) ∧
      Real.exp (q : ℝ) ≤ (((fun y => ru (y ^ 2))^[K] hi0 : ℚ) : ℝ) :=
  ⟨le_exp_of_le_expLo hN hq (iterate_sq_rounded_down_le_expLo N K q rd hrd hlo0 hlo).2,
    exp_le_of_expHi_le hN hq (expHi_le_iterate_sq_rounded_up N K hN q hq ru hru hhi)⟩

end MetricChain
