import Mathlib
import proofs.CertificateAlgebra
import proofs.Frontiers.SecondOrderEnvelope

/-!
# Kernel soundness for real models under the symmetrised pair hypothesis

The energy of a pairwise instance (`PairInstance.energy`, `PairModel.energy`) sums the pair table
of every unordered pair of sites in both orientations, `J i j (x i) (x j)` and
`J j i (x j) (x i)`: it depends on the two orientations of a pair table only through their sum
`J i j a b + J j i b a`.  The comparison lemma `PairInstance.cast_energy_le` and its consequences
`verify_sound_real` (`CertificateAlgebra.lean`) and `verify_sound_secondOrder`
(`SecondOrderEnvelope.lean`) ask for more: the pair inequality `I.J i j a b ≤ M.J i j a b` for
*each ordered pair* `(i, j)` separately.  A rational instance that stores every unordered pair
table once — in one orientation, the other orientation being zero, as `triangle` in
`CertificateAlgebra.lean` does — can fail that termwise hypothesis against `lowerModel M g c x₀`,
which subtracts `c i j / 2` in *both* orientations, although the sums of the two orientations are
in the right order.

This file proves the three statements under the **symmetrised pair hypothesis**

  `∀ i j, i ≠ j → ∀ a b, I.J i j a b + I.J j i b a ≤ M.J i j a b + M.J j i b a`,

which constrains exactly what the energy depends on (and nothing on the diagonal `i = j`, which
the energy ignores).  This is the soundness of the pairwise kernel for real-valued models, and
for real-valued models with a residual known through a second-order envelope, when the published
rational instance is free to distribute every pair table over its two orientations.

**Provenance.**  The statements were requested by the Scientific Discovery Division in its
message SCI-RES-0014 (request P7-T3); `PairInstance.cast_energy_le_symm` is its Lemma P7.7.  No
existing file is changed: the termwise theorems remain as they are, and by `symm_of_termwise`
they are the special cases of the theorems of this file.

## Declarations

* `sum_erase_swap_fin` — a sum over the ordered pairs of distinct sites is invariant under
  exchanging the two indices (real summands indexed by `Fin n`).
* `PairInstance.cast_energy_le_symm` — Lemma P7.7: a rational instance whose one-body table and
  whose symmetrised pair tables lie below those of a real pairwise model has a smaller energy.
* `verify_sound_real_symm` — `verify_sound_real` under the symmetrised pair hypothesis.
* `verify_sound_secondOrder_symm` — `verify_sound_secondOrder` under the symmetrised pair
  hypothesis against `lowerModel M g c x₀`.
* `symm_of_termwise` — the termwise pair hypothesis implies the symmetrised one.
* `onceModel`, `onceResidual`, `onceBound`, `onceRef`, `onceInstance` — the data of the witness:
  two binary sites, zero explicit part, zero residual, constants `c = 1`, reference `(0, 0)`, and
  the rational instance that stores the pair once (`J 0 1 1 1 = -1`, every other entry `0`).
* `onceResidual_mixedDiffBound`, `onceInstance_h_le`, `onceInstance_symm_le`,
  `onceInstance_not_termwise` — the four facts about the witness.
* `symm_hypothesis_witness` — the symmetrised hypothesis is strictly weaker: for the data above
  the hypotheses of `verify_sound_secondOrder_symm` on the residual, the constants and the
  instance hold, and the termwise hypothesis `hJ` of `verify_sound_secondOrder` fails (at
  `(i, j, a, b) = (1, 0, 1, 1)`).

## Proof of the comparison lemma

Write `f i j = I.J i j (x i) (x j)` and `F i j = M.J i j (x i) (x j)`.  The pair parts of the two
energies are the sums of `f i j` and of `F i j` over the ordered pairs `i ≠ j`.  Such a sum does
not change when the roles of `i` and `j` are exchanged (`sum_erase_swap_fin`), so twice the pair
part of `I` is the sum of `f i j + f j i`, which the hypothesis bounds term by term by
`F i j + F j i`, whose sum is twice the pair part of `M`.
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-! ### Exchanging the two indices of a sum over ordered pairs -/

/-- **Exchanging the two indices in a sum over the ordered pairs of distinct sites.**  For a
real-valued `f` on pairs of sites, the sum of `f i j` over the ordered pairs `i ≠ j` equals the
sum of `f j i` over the same pairs: write every inner sum as a sum over all `j` whose summand is
switched off at `j = i`, and exchange the two summations.

(`sum_erase_swap` in `CertificateAlgebra.lean` is this identity for rational summands;
`sum_erase_swap_real` in `StateShares.lean`, which this file does not import, is the identity for
real summands on an arbitrary finite index type.) -/
theorem sum_erase_swap_fin (f : Fin n → Fin n → ℝ) :
    ∑ i, ∑ j ∈ univ.erase i, f i j = ∑ i, ∑ j ∈ univ.erase i, f j i := by
  have key : ∀ g : Fin n → Fin n → ℝ,
      ∑ i, ∑ j ∈ univ.erase i, g i j = ∑ i, ∑ j, if j ≠ i then g i j else 0 := by
    intro g
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [← Finset.filter_ne' univ i, Finset.sum_filter]
  rw [key f, key (fun i j => f j i), Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  by_cases h : i = j
  · subst h
    rfl
  · rw [if_pos h, if_pos (Ne.symm h)]

/-! ### The comparison lemma and the two kernel statements -/

/-- **Comparison under the symmetrised pair hypothesis** (Lemma P7.7 of the Scientific Discovery
Division, message SCI-RES-0014).  If the one-body table of the rational instance `I` lies below
that of the real pairwise model `M` and, for every two distinct sites `i ≠ j` and all states `a`,
`b`, the *sum of the two orientations* of the pair table of `I` lies below that of `M`, then the
energy of `I` is at most the energy of `M` at every configuration.

`PairInstance.cast_energy_le` asks for the pair inequality in each orientation separately; here
`I` is free to distribute a pair table over its two orientations (for instance to store it once).
Nothing is asked on the diagonal `i = j`, which the energy ignores. -/
theorem PairInstance.cast_energy_le_symm (I : PairInstance n k)
    (M : PairModel ℝ (Fin n) (fun _ => Fin k)) (hh : ∀ i a, (I.h i a : ℝ) ≤ M.h i a)
    (hJ : ∀ i j, i ≠ j → ∀ a b,
      (I.J i j a b : ℝ) + (I.J j i b a : ℝ) ≤ M.J i j a b + M.J j i b a)
    (x : Config n k) : ((I.energy x : ℚ) : ℝ) ≤ M.energy x := by
  unfold PairInstance.energy PairModel.energy
  push_cast
  apply add_le_add
  · exact Finset.sum_le_sum fun i _ => hh i (x i)
  · have h1 := sum_erase_swap_fin fun i j => (I.J i j (x i) (x j) : ℝ)
    have h2 := sum_erase_swap_fin fun i j => M.J i j (x i) (x j)
    have h3 : ∑ i, ∑ j ∈ univ.erase i,
          ((I.J i j (x i) (x j) : ℝ) + (I.J j i (x j) (x i) : ℝ)) ≤
        ∑ i, ∑ j ∈ univ.erase i, (M.J i j (x i) (x j) + M.J j i (x j) (x i)) :=
      Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j hj =>
        hJ i j (Finset.ne_of_mem_erase hj).symm (x i) (x j)
    simp only [Finset.sum_add_distrib] at h3
    linarith

/-- **Soundness for real energies under the symmetrised pair hypothesis.**  This is
`verify_sound_real` with the pair hypothesis asked only for the sum of the two orientations of
every pair of distinct sites: if the one-body table of the published rational instance `I` lies
below that of the real pairwise model `M`, and the symmetrised pair tables of `I` lie below those
of `M`, then a certificate accepted by the kernel for `I`, the bound `L` and the box `D` bounds
the real energy `M.energy x` of every configuration of the box. -/
theorem verify_sound_real_symm (c : Cert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ)
    (hv : verify c I D L = true) (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (hh : ∀ i a, (I.h i a : ℝ) ≤ M.h i a)
    (hJ : ∀ i j, i ≠ j → ∀ a b,
      (I.J i j a b : ℝ) + (I.J j i b a : ℝ) ≤ M.J i j a b + M.J j i b a)
    (x : Config n k) (hx : InBox D x) : (L : ℝ) ≤ M.energy x := by
  have h1 := verify_sound c I D L hv x hx
  have h2 := I.cast_energy_le_symm M hh hJ x
  have h3 : (L : ℝ) ≤ ((I.energy x : ℚ) : ℝ) := by exact_mod_cast h1
  linarith

/-- **Kernel soundness with a second-order envelope under the symmetrised pair hypothesis.**
This is `verify_sound_secondOrder` with the pair hypothesis against the lower model asked only
for the sum of the two orientations of every pair of distinct sites.  Let the residual `g` on `n`
sites with `k` states have mixed differences bounded by a symmetric table `c`, let the one-body
table of the rational instance `I` lie below that of the pairwise lower model
`lowerModel M g c x₀`, and let the symmetrised pair tables of `I` lie below those of the lower
model.  If the pairwise kernel accepts a certificate for `I` and the bound `L` on the box `D`,
then `L + g x₀` is a lower bound on the true energy `M.energy x + g x` of every configuration of
the box.

The lower model subtracts `c i j / 2` in each of the two orientations when both states differ
from the reference, so for symmetric `c` the right-hand side of `hJ` is
`M.J i j a b + M.J j i b a - c i j` at such states and `M.J i j a b + M.J j i b a` at the others.
An instance that stores the pair table once (the whole correction in one orientation, nothing in
the other) can satisfy this hypothesis without satisfying the termwise one:
`symm_hypothesis_witness`. -/
theorem verify_sound_secondOrder_symm (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (g : Config n k → ℝ) (c : Fin n → Fin n → ℝ) (x₀ : Config n k)
    (hg : MixedDiffBound g c) (hc : ∀ i j, c i j = c j i) (I : PairInstance n k)
    (hh : ∀ i a, (I.h i a : ℝ) ≤ (lowerModel M g c x₀).h i a)
    (hJ : ∀ i j, i ≠ j → ∀ a b, (I.J i j a b : ℝ) + (I.J j i b a : ℝ) ≤
      (lowerModel M g c x₀).J i j a b + (lowerModel M g c x₀).J j i b a)
    (cert : Cert n k) (D : Dom n k) (L : ℚ) (hv : verify cert I D L = true)
    (x : Config n k) (hx : InBox D x) : (L : ℝ) + g x₀ ≤ M.energy x + g x := by
  have h1 := verify_sound_real_symm cert I D L hv (lowerModel M g c x₀) hh hJ x hx
  have h2 := (pairwise_sandwich M g c hg hc x₀ x).1
  linarith

/-- **The termwise pair hypothesis implies the symmetrised one.**  If
`I.J i j a b ≤ M.J i j a b` for every ordered pair of sites — the hypothesis `hJ` of
`PairInstance.cast_energy_le`, of `verify_sound_real` and, with `lowerModel M g c x₀` in the
place of `M`, of `verify_sound_secondOrder` — then the sums of the two orientations are in the
same order.  So these three theorems are the special cases of
`PairInstance.cast_energy_le_symm`, `verify_sound_real_symm` and `verify_sound_secondOrder_symm`.
The converse implication is false: `symm_hypothesis_witness`. -/
theorem symm_of_termwise (I : PairInstance n k) (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (hJ : ∀ i j a b, (I.J i j a b : ℝ) ≤ M.J i j a b) :
    ∀ i j, i ≠ j → ∀ a b,
      (I.J i j a b : ℝ) + (I.J j i b a : ℝ) ≤ M.J i j a b + M.J j i b a :=
  fun i j _ a b => add_le_add (hJ i j a b) (hJ j i b a)

/-! ### The symmetrised hypothesis is strictly weaker

Two binary sites, reference configuration `(0, 0)`, zero explicit part, zero residual and the
constants `c i j = 1`.  The pair tables of the lower model are `-1/2` at the states `(1, 1)` and
`0` elsewhere, in both orientations.  The rational instance stores the pair once: its only
non-zero entry is `J 0 1 1 1 = -1`.  The sums of the two orientations of the instance and of the
lower model are equal, so the symmetrised hypothesis holds; but the orientation `(1, 0)` of the
instance is zero, and `0 ≤ -1/2` is false: the termwise hypothesis of `verify_sound_secondOrder`
fails at `(i, j, a, b) = (1, 0, 1, 1)`. -/

/-- Explicit part of the witness: the zero pairwise model on two binary sites. -/
def onceModel : PairModel ℝ (Fin 2) (fun _ => Fin 2) where
  h _ _ := 0
  J _ _ _ _ := 0

/-- Residual of the witness: identically zero. -/
def onceResidual : Config 2 2 → ℝ := fun _ => 0

/-- Second-order envelope constants of the witness: `c i j = 1` (symmetric). -/
def onceBound : Fin 2 → Fin 2 → ℝ := fun _ _ => 1

/-- Reference configuration of the witness: `(0, 0)`. -/
def onceRef : Config 2 2 := fun _ => 0

/-- Rational instance of the witness: zero one-body table, and the pair table of the unordered
pair `{0, 1}` **stored once**, in the orientation `(0, 1)`.  The entry `J 0 1 1 1 = -1` carries
the whole correction `-(c 0 1 / 2 + c 1 0 / 2) = -1` of the pair of changed states `(1, 1)`, and
every other entry — in particular the whole orientation `(1, 0)` — is `0`. -/
def onceInstance : PairInstance 2 2 where
  h := fun _ _ => 0
  J := fun i j a b => if i = 0 ∧ j = 1 ∧ a = 1 ∧ b = 1 then -1 else 0

/-- The zero residual has the second-order envelope `c = 1`. -/
theorem onceResidual_mixedDiffBound : MixedDiffBound onceResidual onceBound := by
  intro x i j _ a b
  simp [onceResidual, onceBound]

/-- The one-body hypothesis `hh` holds for the witness (with equality: both tables vanish). -/
theorem onceInstance_h_le (i a : Fin 2) :
    (onceInstance.h i a : ℝ) ≤ (lowerModel onceModel onceResidual onceBound onceRef).h i a := by
  simp [onceInstance, lowerModel, onceModel, onceResidual]

/-- The symmetrised pair hypothesis holds for the witness: for `i ≠ j` both sides are `-1` at the
states `(1, 1)` and `0` elsewhere. -/
theorem onceInstance_symm_le (i j : Fin 2) (hij : i ≠ j) (a b : Fin 2) :
    (onceInstance.J i j a b : ℝ) + (onceInstance.J j i b a : ℝ) ≤
      (lowerModel onceModel onceResidual onceBound onceRef).J i j a b +
        (lowerModel onceModel onceResidual onceBound onceRef).J j i b a := by
  have hcases : ∀ p q : Fin 2, p ≠ q → (p = 0 ∧ q = 1) ∨ (p = 1 ∧ q = 0) := by decide
  rcases hcases i j hij with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> fin_cases a <;> fin_cases b <;>
    norm_num [onceInstance, lowerModel, onceModel, onceBound, onceRef]

/-- The termwise pair hypothesis fails for the witness in the orientation that the instance
leaves empty: `onceInstance.J 1 0 1 1 = 0`, whereas the lower model has `-1/2` there. -/
theorem onceInstance_not_termwise :
    ¬ ((onceInstance.J 1 0 1 1 : ℝ) ≤
      (lowerModel onceModel onceResidual onceBound onceRef).J 1 0 1 1) := by
  norm_num [onceInstance, lowerModel, onceModel, onceBound, onceRef]

/-- **The symmetrised pair hypothesis is strictly weaker than the termwise one.**  For the zero
model on two binary sites, the zero residual, the constants `c = 1`, the reference `(0, 0)` and
the rational instance that stores the pair once (`onceInstance`):

* the residual has the second-order envelope `c`, and `c` is symmetric (the hypotheses `hg`, `hc`
  of `verify_sound_secondOrder` and of `verify_sound_secondOrder_symm`);
* the one-body hypothesis `hh` of both theorems holds;
* the symmetrised pair hypothesis `hJ` of `verify_sound_secondOrder_symm` holds;
* the termwise pair hypothesis `hJ` of `verify_sound_secondOrder` fails: there are `i`, `j`, `a`,
  `b` (namely `1`, `0`, `1`, `1`) at which the instance is not below the lower model.

So the hypotheses of `verify_sound_secondOrder_symm` on the model, the residual, the constants
and the instance hold here and those of `verify_sound_secondOrder` do not, while by
`symm_of_termwise` the former hold whenever the latter do. -/
theorem symm_hypothesis_witness :
    MixedDiffBound onceResidual onceBound ∧ (∀ i j, onceBound i j = onceBound j i) ∧
      (∀ i a, (onceInstance.h i a : ℝ) ≤
        (lowerModel onceModel onceResidual onceBound onceRef).h i a) ∧
      (∀ i j, i ≠ j → ∀ a b, (onceInstance.J i j a b : ℝ) + (onceInstance.J j i b a : ℝ) ≤
        (lowerModel onceModel onceResidual onceBound onceRef).J i j a b +
          (lowerModel onceModel onceResidual onceBound onceRef).J j i b a) ∧
      ∃ (i j : Fin 2) (a b : Fin 2), ¬ ((onceInstance.J i j a b : ℝ) ≤
        (lowerModel onceModel onceResidual onceBound onceRef).J i j a b) :=
  ⟨onceResidual_mixedDiffBound, fun _ _ => rfl, onceInstance_h_le, onceInstance_symm_le,
    1, 0, 1, 1, onceInstance_not_termwise⟩

end MetricChain
