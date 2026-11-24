import Mathlib
import proofs.Frontiers.PartitionCertificate

/-!
# Partition-function certificates: the cut rule and the elimination rules

The sum–product kernel `zverify` of `PartitionCertificate.lean` has three rules (factorised leaf,
branch, thermal prune).  This file extends it by a **cut** rule and two **elimination** rules
and proves the extended kernel `zverify2` sound.  The rules, and what each of them is exact on:

* **Leaf** (via `base`): exact when the pair factors are constant on the box, and with positive
  factors only then (`zleaf_exact_const`).
* **Branch** (`branch`, and via `base`): exact — the partition sum is additive over the states
  of a site — at the price of one subtree per state.
* **Thermal prune** (via `base`): its upper endpoint carries a factor `1 + ρ`, and with positive
  factors its lower endpoint is exact only if nothing is removed (see the proof of
  `zverify_exact_leaves`).
* **Cut** (`cut`): split the sites into `S` and `Sᶜ`, certify the two halves separately and
  multiply the results.  Two-sided; exact when the pair factors across the cut are constant on
  the box, in particular for independent subsystems (which the tropical kernel handles with its
  decomposition rule `sum`).
* **Elimination** (`elim1`, `elim2`): sum out a site that interacts with at most two other
  sites.  Always exact.  Iterated elimination is exact on every interaction graph that can be
  reduced by repeatedly removing a site of degree at most two and joining its neighbours: trees,
  cycles, series–parallel graphs, i.e. treewidth at most two (what is proved here is stated in
  the section on elimination).

Without the last two rules exactness is expensive.  On a rigid instance with positive factors, a
certificate with an exact lower endpoint that uses only leaf, branch and thermal prune has to
enumerate the box (section on separation): the *product* of the state spaces of independent
subsystems, and all `2ⁿ` configurations of the ferromagnetic two-state chain on `n ≥ 2` sites
(`ferroChain_separation`), although a transfer matrix computes the partition sum of a chain with
`O(n k²)` operations.

## The cut inequality

For an instance `I` (one-body factors `w`, pair factors `W` on ordered pairs) and a set of sites
`S`, the *restricted* instance `I.restrict S` keeps the factors inside `S` and replaces every
other factor by `1`.  The weight of a configuration factorises along the cut
(`WInstance.weight_cut`):

  `weight x = (I.restrict S).weight x · (I.restrict Sᶜ).weight x · ∏ W i j (x i) (x j)`,

the last product running over the ordered pairs `(i, j)` *across the cut*, i.e. those with
exactly one of `i`, `j` in `S` (`cutConst`).  The first factor only depends on the states of the
sites of `S`, the second only on those of `Sᶜ` (`WInstance.restrict_weight_congr`), and the box
`∏ D` is the product of its `S`-part and its `Sᶜ`-part (`sum_boxFinset_cut`).  With the sites
outside `S` pinned to a reference configuration `p` (`D.pinOutside S p`), the partition sum of a
half,

  `Z_S = (I.restrict S).Z (D.pinOutside S p)`,

is the sum over the states of the sites of `S` of the factors inside `S`; it does not depend on
`p` (`WInstance.Z_restrict_pinOutside`).  Hence, for nonnegative factors whose pair factors across
the cut lie in `[lo i j, hi i j]` on the box, with `0 ≤ lo i j`,

  `Λ · Z_S · Z_Sᶜ ≤ Z ≤ Υ · Z_S · Z_Sᶜ`,   `Λ = ∏ lo i j`,   `Υ = ∏ hi i j` (pairs across the cut)

(`WInstance.Z_cut`, the **cut inequality**), with equality `Z = Z_S · Z_Sᶜ` when the factors
across the cut are identically `1` (`WInstance.Z_cut_eq`: independent subsystems).

## Elimination

Let site `i` have trivial pair factors (identically `1` on the current domains) with every site
other than `j`.  The sum over the states of `i` is then a function of the state of `j` alone and
is absorbed into the one-body factor of `j`: the instance `I.elim1 D i j` has

  `w' j b = w j b · ∑ a ∈ D i, w i a · W i j a b · W j i b a`,

all its factors at site `i` are `1`, and its partition sum over the box with site `i` pinned is
that of `I` (`WInstance.Z_elim1`).  If `i` interacts with two sites `j` and `l`, the sum is a
function of the states of both and is absorbed into the pair factor of the ordered pair `(j, l)`
(`I.elim2 D i j l`, `WInstance.Z_elim2`):

  `W' j l b c = W j l b c · ∑ a ∈ D i, w i a · W i j a b · W j i b a · W i l a c · W l i c a`.

Both statements are identities (no sign condition), and both new instances inherit nonnegative
factors.  They follow from one lemma on summing out a site (`WInstance.Z_sumOut`), which rests on
the factorisation `weight (update x i a) = wbase i x · wlocal i a x` of
`PartitionCertificate.lean`.

Repeated elimination is the transfer-matrix (variable-elimination) algorithm.  Eliminations
followed by one leaf compute the partition sum exactly whenever the interaction graph can be
reduced to a single site by repeatedly removing a site with at most two neighbours and joining
these two neighbours (the new pair factor of `elim2` is the fill-in edge).  The graphs that can
be reduced in this way are those of treewidth at most two; they include trees, cycles and
series–parallel graphs.  In this file the general statement is proved for chains of every length
(`zverify2_chainCert`, with the separation `chain_separation`); a chain, a tree with a branch
point and a ring are run in the kernel.

## Kernel

`ZCert2` has five constructors: `base c` (a certificate of `zverify`: leaf, branch, thermal
prune), `branch i children` (as in `zverify`), `cut S p lo hi c₁ c₂`, `elim1 i j p rest` and
`elim2 i j l p rest`.  On a cut node `zverify2`

* checks `CutOK`: the pin lies in the box (`p i ∈ D i` for all `i`) and, for every ordered pair
  `i ≠ j` with exactly one of `i`, `j` in `S`, `0 ≤ lo i j` and `lo i j ≤ W i j a b ≤ hi i j`
  for all `a ∈ D i`, `b ∈ D j`;
* runs `c₁` on `I.restrict S` over `D.pinOutside S p` and `c₂` on `I.restrict Sᶜ` over
  `D.pinOutside Sᶜ p`, obtaining intervals `(l₁, h₁)` and `(l₂, h₂)`;
* requires `0 ≤ l₁` and `0 ≤ l₂` and returns `(Λ · l₁ · l₂, Υ · h₁ · h₂)`.

A cut node is checked in one pass over the ordered pairs of sites, with a scan of the pair table
(restricted to the current domains) for each pair across the cut; the two halves are then checked
independently of each other.

On a node `elim1 i j p rest` the kernel checks `Elim1OK` — `i ≠ j`, and
`W i m a b = 1 = W m i b a` for every site `m` other than `i`, `j` and all `a ∈ D i`,
`b ∈ D m` — and runs `rest` on `I.elim1 D i j` over `D.fix i p`.  On `elim2 i j l p rest` it
checks `Elim2OK` — `i`, `j`, `l` pairwise distinct, and the same condition for every site `m`
other than `i`, `j`, `l` — and runs `rest` on `I.elim2 D i j l` over `D.fix i p`.  The pin `p`
is arbitrary; it need not lie in `D i`.  A checker that tabulates the new factors spends
`O(n k²)` operations on an `elim1` node and `O(n k² + k³)` on an `elim2` node.  (In Lean the new
instances are closures, not tables; the kernel runs below are small.)

`zverify2_sound` is the soundness theorem (for nonnegative factors; restricted and eliminated
instances inherit them).  The top-level entry point `zverify2Top` checks nonnegativity itself:
`zverify2Top_sound` has no side condition.  On `base` certificates the new kernel is the old one
(`zverify2Top_base`).

## Kernel runs and the two separations

A certificate is *elementary* if it uses neither `cut` nor `elim1`/`elim2`
(`ZCert2.Elementary`).  On an instance with positive factors in which every site has a partner
whose pair factors tell its states apart (`WInstance.Rigid`), an elementary certificate whose
lower endpoint is exact has at least as many leaves as the box has configurations
(`zverify2_elementary_exact_leaves`).  Two limits of this statement: it concerns *exact* lower
endpoints only (nothing is proved about certificates whose lower end is slightly below `Z`),
and `Rigid` depends on how the weights are split into ordered pair factors (see its
docstring).

* **Cut versus elementary** (`cut_rule_separation`).  Two disjoint frustrated triangles on six
  binary sites, `Z = (13/4)² = 169/16`: the cut certificate enumerates each triangle separately
  (`2 · 8 = 16` leaves) and the kernel returns the exact value (`twoTriangles_cut_exact`),
  whereas an elementary certificate needs `64` leaves, attained by full enumeration
  (`twoTriangles_enum_exact`).
* **Elimination versus elementary** (`elimination_separation`).  The ferromagnetic two-state
  chain on six sites, `Z = 2 · (3/2)⁵ = 243/16`: five eliminations and one leaf give the exact
  value (`chain_elim_exact`), whereas an elementary certificate needs `64` leaves.  The same
  holds on chains of every length, one leaf against `kⁿ` (`chain_separation`, and
  `ferroChain_separation` for the ferromagnetic two-state chain on `n ≥ 2` sites).

Further kernel runs: with a weak bond across the cut the cut gives a strict enclosure
(`coupledTriangles_cut_enclosure`), and branching on the two ends of the bond first makes the cut
exact again (`coupledTriangles_branch_cut_exact`, `32` leaves); cuts nest
(`threePairs_nested_cut_exact`: `4 + 4 + 4 = 12` leaves against at least `4 · 4 · 4 = 64` for
elementary certificates, `threePairs_elementary_leaves`); a tree with a branch point is reduced
by four `elim1` nodes (`tree_elim_exact`), and a ferromagnetic ring of five sites by three
`elim2` nodes and one `elim1` node (`ring_elim_exact`: one leaf against at least `32`,
`ring_elementary_leaves`).
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-! ### Restriction to a set of sites, pinned boxes, gluing -/

/-- Restriction of an instance to the sites of `S`: every factor that involves a site outside
`S` is replaced by `1`. -/
def WInstance.restrict (I : WInstance n k) (S : Finset (Fin n)) : WInstance n k where
  w i a := if i ∈ S then I.w i a else 1
  W i j a b := if i ∈ S ∧ j ∈ S then I.W i j a b else 1

/-- The restriction of an instance with nonnegative factors has nonnegative factors. -/
theorem WInstance.restrict_nonneg {I : WInstance n k} (hI : I.Nonneg) (S : Finset (Fin n)) :
    (I.restrict S).Nonneg := by
  constructor
  · intro i a
    unfold WInstance.restrict
    dsimp only
    split_ifs
    · exact hI.1 i a
    · exact zero_le_one
  · intro i j a b
    unfold WInstance.restrict
    dsimp only
    split_ifs
    · exact hI.2 i j a b
    · exact zero_le_one

/-- Pin every site outside `S` to its state in `p`; the domains of the sites of `S` are kept. -/
def Dom.pinOutside (D : Dom n k) (S : Finset (Fin n)) (p : Config n k) : Dom n k :=
  fun i => if i ∈ S then D i else [p i]

/-- Inside `S` the pinned domains are the original ones. -/
theorem Dom.pinOutside_of_mem (D : Dom n k) {S : Finset (Fin n)} (p : Config n k) {i : Fin n}
    (hi : i ∈ S) : D.pinOutside S p i = D i := if_pos hi

/-- Outside `S` the pinned domain is the singleton of the pin. -/
theorem Dom.pinOutside_of_not_mem (D : Dom n k) {S : Finset (Fin n)} (p : Config n k)
    {i : Fin n} (hi : i ∉ S) : D.pinOutside S p i = [p i] := if_neg hi

/-- Membership in the pinned box: in the original domains on `S`, equal to the pin elsewhere. -/
theorem inBox_pinOutside {D : Dom n k} {S : Finset (Fin n)} {p y : Config n k} :
    InBox (D.pinOutside S p) y ↔ (∀ i ∈ S, y i ∈ D i) ∧ ∀ i, i ∉ S → y i = p i := by
  constructor
  · intro h
    refine ⟨fun i hi => ?_, fun i hi => ?_⟩
    · have := h i
      rwa [D.pinOutside_of_mem p hi] at this
    · have := h i
      rw [D.pinOutside_of_not_mem p hi] at this
      simpa using this
  · rintro ⟨h1, h2⟩ i
    by_cases hi : i ∈ S
    · rw [D.pinOutside_of_mem p hi]
      exact h1 i hi
    · rw [D.pinOutside_of_not_mem p hi, h2 i hi]
      simp

/-- Glue the `S`-part of `y` to the part of `z` outside `S`. -/
def cutGlue (S : Finset (Fin n)) (y z : Config n k) : Config n k :=
  fun i => if i ∈ S then y i else z i

/-- On `S` the glued configuration is the first one. -/
theorem cutGlue_of_mem {S : Finset (Fin n)} (y z : Config n k) {i : Fin n} (hi : i ∈ S) :
    cutGlue S y z i = y i := if_pos hi

/-- Outside `S` the glued configuration is the second one. -/
theorem cutGlue_of_not_mem {S : Finset (Fin n)} (y z : Config n k) {i : Fin n} (hi : i ∉ S) :
    cutGlue S y z i = z i := if_neg hi

/-- Gluing a point of the `S`-half of the box to a point of the `Sᶜ`-half gives a point of the
box. -/
theorem inBox_cutGlue {D : Dom n k} {S : Finset (Fin n)} {p y z : Config n k}
    (hy : InBox (D.pinOutside S p) y) (hz : InBox (D.pinOutside Sᶜ p) z) :
    InBox D (cutGlue S y z) := by
  intro i
  rw [inBox_pinOutside] at hy hz
  by_cases hi : i ∈ S
  · rw [cutGlue_of_mem y z hi]
    exact hy.1 i hi
  · rw [cutGlue_of_not_mem y z hi]
    exact hz.1 i (Finset.mem_compl.mpr hi)

/-- **The box is the product of its `S`-part and its `Sᶜ`-part** (summation form): gluing is a
bijection from the product of the two pinned boxes onto the box. -/
theorem sum_boxFinset_cut (D : Dom n k) (S : Finset (Fin n)) (p : Config n k)
    (f : Config n k → ℚ) :
    ∑ x ∈ boxFinset D, f x =
      ∑ y ∈ boxFinset (D.pinOutside S p), ∑ z ∈ boxFinset (D.pinOutside Sᶜ p),
        f (cutGlue S y z) := by
  rw [← Finset.sum_product' (boxFinset (D.pinOutside S p)) (boxFinset (D.pinOutside Sᶜ p))
    (fun y z => f (cutGlue S y z))]
  symm
  apply Finset.sum_nbij' (fun yz : Config n k × Config n k => cutGlue S yz.1 yz.2)
    (fun x => (cutGlue S x p, cutGlue S p x))
  · rintro ⟨y, z⟩ hyz
    rw [Finset.mem_product, mem_boxFinset, mem_boxFinset] at hyz
    exact mem_boxFinset.mpr (inBox_cutGlue hyz.1 hyz.2)
  · intro x hx
    rw [mem_boxFinset] at hx
    rw [Finset.mem_product, mem_boxFinset, mem_boxFinset, inBox_pinOutside, inBox_pinOutside]
    refine ⟨⟨fun i hi => ?_, fun i hi => ?_⟩, ⟨fun i hi => ?_, fun i hi => ?_⟩⟩
    · show cutGlue S x p i ∈ D i
      rw [cutGlue_of_mem x p hi]
      exact hx i
    · exact cutGlue_of_not_mem x p hi
    · show cutGlue S p x i ∈ D i
      rw [cutGlue_of_not_mem p x (Finset.mem_compl.mp hi)]
      exact hx i
    · exact cutGlue_of_mem p x (by simpa using hi)
  · rintro ⟨y, z⟩ hyz
    rw [Finset.mem_product, mem_boxFinset, mem_boxFinset, inBox_pinOutside,
      inBox_pinOutside] at hyz
    obtain ⟨⟨_, hy⟩, ⟨_, hz⟩⟩ := hyz
    refine Prod.ext (funext fun i => ?_) (funext fun i => ?_)
    · by_cases hi : i ∈ S
      · simp only [cutGlue, if_pos hi]
      · simp only [cutGlue, if_neg hi]
        exact (hy i hi).symm
    · by_cases hi : i ∈ S
      · simp only [cutGlue, if_pos hi]
        exact (hz i (by simpa using hi)).symm
      · simp only [cutGlue, if_neg hi]
  · intro x _
    funext i
    by_cases hi : i ∈ S
    · simp only [cutGlue, if_pos hi]
    · simp only [cutGlue, if_neg hi]
  · intro yz _
    rfl

/-! ### Factorisation of the weight along a cut -/

/-- Product of the constants `c i j` over the ordered pairs `(i, j)` across the cut `S | Sᶜ`
(exactly one end in `S`). -/
def cutConst (S : Finset (Fin n)) (c : Fin n → Fin n → ℚ) : ℚ :=
  ∏ i, ∏ j ∈ univ.erase i, if (i ∈ S ↔ j ∈ S) then 1 else c i j

/-- The cut constant of bounds that are nonnegative across the cut is nonnegative. -/
theorem cutConst_nonneg (S : Finset (Fin n)) (c : Fin n → Fin n → ℚ)
    (h : ∀ i, ∀ j ∈ univ.erase i, ¬ (i ∈ S ↔ j ∈ S) → 0 ≤ c i j) : 0 ≤ cutConst S c := by
  unfold cutConst
  apply Finset.prod_nonneg
  intro i _
  apply Finset.prod_nonneg
  intro j hj
  split_ifs with hij
  · exact zero_le_one
  · exact h i j hj hij

/-- The cut constant is monotone on bounds that are nonnegative across the cut. -/
theorem cutConst_le_cutConst (S : Finset (Fin n)) (c d : Fin n → Fin n → ℚ)
    (h0 : ∀ i, ∀ j ∈ univ.erase i, ¬ (i ∈ S ↔ j ∈ S) → 0 ≤ c i j)
    (h : ∀ i, ∀ j ∈ univ.erase i, ¬ (i ∈ S ↔ j ∈ S) → c i j ≤ d i j) :
    cutConst S c ≤ cutConst S d := by
  unfold cutConst
  apply Finset.prod_le_prod
  · intro i _
    apply Finset.prod_nonneg
    intro j hj
    split_ifs with hij
    · exact zero_le_one
    · exact h0 i j hj hij
  · intro i _
    apply Finset.prod_le_prod
    · intro j hj
      split_ifs with hij
      · exact zero_le_one
      · exact h0 i j hj hij
    · intro j hj
      split_ifs with hij
      · exact le_refl 1
      · exact h i j hj hij

/-- The weight of the restricted instance only depends on the states of the sites of `S`. -/
theorem WInstance.restrict_weight_congr (I : WInstance n k) (S : Finset (Fin n))
    {x y : Config n k} (h : ∀ i ∈ S, x i = y i) :
    (I.restrict S).weight x = (I.restrict S).weight y := by
  unfold WInstance.weight WInstance.restrict
  dsimp only
  congr 1
  · apply Finset.prod_congr rfl
    intro i _
    by_cases hi : i ∈ S
    · rw [if_pos hi, if_pos hi, h i hi]
    · rw [if_neg hi, if_neg hi]
  · apply Finset.prod_congr rfl
    intro i _
    apply Finset.prod_congr rfl
    intro j _
    by_cases hij : i ∈ S ∧ j ∈ S
    · rw [if_pos hij, if_pos hij, h i hij.1, h j hij.2]
    · rw [if_neg hij, if_neg hij]

/-- **Factorisation of the weight along a cut**: the factors inside `S`, the factors inside `Sᶜ`
and the pair factors across the cut. -/
theorem WInstance.weight_cut (I : WInstance n k) (S : Finset (Fin n)) (x : Config n k) :
    I.weight x = (I.restrict S).weight x * (I.restrict Sᶜ).weight x *
      cutConst S (fun i j => I.W i j (x i) (x j)) := by
  unfold WInstance.weight WInstance.restrict cutConst
  dsimp only
  have h1 : ∏ i, I.w i (x i) =
      (∏ i, if i ∈ S then I.w i (x i) else 1) * ∏ i, if i ∈ Sᶜ then I.w i (x i) else 1 := by
    rw [← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro i _
    by_cases hi : i ∈ S <;> simp [hi]
  have h2 : ∏ i, ∏ j ∈ univ.erase i, I.W i j (x i) (x j) =
      (∏ i, ∏ j ∈ univ.erase i, if i ∈ S ∧ j ∈ S then I.W i j (x i) (x j) else 1) *
        (∏ i, ∏ j ∈ univ.erase i, if i ∈ Sᶜ ∧ j ∈ Sᶜ then I.W i j (x i) (x j) else 1) *
          ∏ i, ∏ j ∈ univ.erase i, if (i ∈ S ↔ j ∈ S) then 1 else I.W i j (x i) (x j) := by
    simp only [← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro i _
    apply Finset.prod_congr rfl
    intro j _
    by_cases hi : i ∈ S <;> by_cases hj : j ∈ S <;> simp [hi, hj]
  rw [h1, h2]
  ring

/-! ### The cut inequality -/

/-- The product of the partition sums of the two halves, as a double sum. -/
theorem WInstance.Z_mul_Z_cut (I : WInstance n k) (D : Dom n k) (S : Finset (Fin n))
    (p : Config n k) :
    (I.restrict S).Z (D.pinOutside S p) * (I.restrict Sᶜ).Z (D.pinOutside Sᶜ p) =
      ∑ y ∈ boxFinset (D.pinOutside S p), ∑ z ∈ boxFinset (D.pinOutside Sᶜ p),
        (I.restrict S).weight y * (I.restrict Sᶜ).weight z := by
  unfold WInstance.Z
  rw [Finset.sum_mul_sum]

/-- The partition sum as a double sum over the two halves of the box: the weights of the halves
times the pair factors across the cut. -/
theorem WInstance.Z_eq_sum_cut (I : WInstance n k) (D : Dom n k) (S : Finset (Fin n))
    (p : Config n k) :
    I.Z D = ∑ y ∈ boxFinset (D.pinOutside S p), ∑ z ∈ boxFinset (D.pinOutside Sᶜ p),
      (I.restrict S).weight y * (I.restrict Sᶜ).weight z *
        cutConst S (fun i j => I.W i j (cutGlue S y z i) (cutGlue S y z j)) := by
  unfold WInstance.Z
  rw [sum_boxFinset_cut D S p]
  apply Finset.sum_congr rfl
  intro y _
  apply Finset.sum_congr rfl
  intro z _
  rw [I.weight_cut S (cutGlue S y z),
    I.restrict_weight_congr S (fun i hi => cutGlue_of_mem y z hi),
    I.restrict_weight_congr Sᶜ (fun i hi => cutGlue_of_not_mem y z (Finset.mem_compl.mp hi))]

/-- Pair part of the cut check: every pair factor across the cut `S | Sᶜ` (ordered pairs with
exactly one end in `S`) lies in `[lo i j, hi i j]` on the current domains, and `0 ≤ lo i j`. -/
def CutBoundsOK (I : WInstance n k) (D : Dom n k) (S : Finset (Fin n))
    (lo hi : Fin n → Fin n → ℚ) : Prop :=
  ∀ i, ∀ j ∈ univ.erase i, ¬ (i ∈ S ↔ j ∈ S) → 0 ≤ lo i j ∧
    ∀ a ∈ D i, ∀ b ∈ D j, lo i j ≤ I.W i j a b ∧ I.W i j a b ≤ hi i j

/-- The pair part of the cut check is decidable (finitely many rational comparisons). -/
instance decidableCutBoundsOK (I : WInstance n k) (D : Dom n k) (S : Finset (Fin n))
    (lo hi : Fin n → Fin n → ℚ) : Decidable (CutBoundsOK I D S lo hi) := by
  unfold CutBoundsOK; infer_instance

/-- **Cut inequality.**  If the factors are nonnegative and the pair factors across the cut
`S | Sᶜ` lie in `[lo, hi]` on the box, the partition sum is the product of the partition sums of
the two halves up to the factors `Λ = cutConst S lo` and `Υ = cutConst S hi`.  (No condition on
the pin `p`.) -/
theorem WInstance.Z_cut {I : WInstance n k} (hI : I.Nonneg) (D : Dom n k) (S : Finset (Fin n))
    (p : Config n k) (lo hi : Fin n → Fin n → ℚ) (h : CutBoundsOK I D S lo hi) :
    cutConst S lo * ((I.restrict S).Z (D.pinOutside S p) *
        (I.restrict Sᶜ).Z (D.pinOutside Sᶜ p)) ≤ I.Z D ∧
      I.Z D ≤ cutConst S hi * ((I.restrict S).Z (D.pinOutside S p) *
        (I.restrict Sᶜ).Z (D.pinOutside Sᶜ p)) := by
  have hnn : ∀ y z : Config n k, 0 ≤ (I.restrict S).weight y * (I.restrict Sᶜ).weight z :=
    fun y z => mul_nonneg ((I.restrict S).weight_nonneg (I.restrict_nonneg hI S) y)
      ((I.restrict Sᶜ).weight_nonneg (I.restrict_nonneg hI Sᶜ) z)
  rw [I.Z_mul_Z_cut D S p, I.Z_eq_sum_cut D S p, Finset.mul_sum, Finset.mul_sum]
  constructor
  · apply Finset.sum_le_sum
    intro y hy
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro z hz
    have hx := inBox_cutGlue (mem_boxFinset.mp hy) (mem_boxFinset.mp hz)
    rw [mul_comm]
    apply mul_le_mul_of_nonneg_left _ (hnn y z)
    exact cutConst_le_cutConst S _ _ (fun i j hj hij => (h i j hj hij).1)
      (fun i j hj hij => ((h i j hj hij).2 _ (hx i) _ (hx j)).1)
  · apply Finset.sum_le_sum
    intro y hy
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro z hz
    have hx := inBox_cutGlue (mem_boxFinset.mp hy) (mem_boxFinset.mp hz)
    rw [mul_comm (cutConst S hi)]
    apply mul_le_mul_of_nonneg_left _ (hnn y z)
    exact cutConst_le_cutConst S _ _ (fun i j _ _ => hI.2 i j _ _)
      (fun i j hj hij => ((h i j hj hij).2 _ (hx i) _ (hx j)).2)

/-- **Independent subsystems.**  If every pair factor across the cut is identically `1` on the
box, the partition sum is exactly the product of the partition sums of the two halves (an
identity: no sign condition on the factors). -/
theorem WInstance.Z_cut_eq (I : WInstance n k) (D : Dom n k) (S : Finset (Fin n))
    (p : Config n k)
    (h : ∀ i, ∀ j ∈ univ.erase i, ¬ (i ∈ S ↔ j ∈ S) → ∀ a ∈ D i, ∀ b ∈ D j, I.W i j a b = 1) :
    I.Z D = (I.restrict S).Z (D.pinOutside S p) * (I.restrict Sᶜ).Z (D.pinOutside Sᶜ p) := by
  rw [I.Z_mul_Z_cut D S p, I.Z_eq_sum_cut D S p]
  apply Finset.sum_congr rfl
  intro y hy
  apply Finset.sum_congr rfl
  intro z hz
  have hx := inBox_cutGlue (mem_boxFinset.mp hy) (mem_boxFinset.mp hz)
  have hone : cutConst S (fun i j => I.W i j (cutGlue S y z i) (cutGlue S y z j)) = 1 := by
    unfold cutConst
    apply Finset.prod_eq_one
    intro i _
    apply Finset.prod_eq_one
    intro j hj
    split_ifs with hij
    · rfl
    · exact h i j hj hij _ (hx i) _ (hx j)
  rw [hone, mul_one]

/-- The partition sum of a half does not depend on the pin. -/
theorem WInstance.Z_restrict_pinOutside (I : WInstance n k) (D : Dom n k) (S : Finset (Fin n))
    (p q : Config n k) :
    (I.restrict S).Z (D.pinOutside S p) = (I.restrict S).Z (D.pinOutside S q) := by
  have hmaps : ∀ p q : Config n k, ∀ y ∈ boxFinset (D.pinOutside S p),
      cutGlue S y q ∈ boxFinset (D.pinOutside S q) := by
    intro p q y hy
    rw [mem_boxFinset, inBox_pinOutside] at hy ⊢
    refine ⟨fun i hi => ?_, fun i hi => cutGlue_of_not_mem y q hi⟩
    rw [cutGlue_of_mem y q hi]
    exact hy.1 i hi
  have hinv : ∀ p q : Config n k, ∀ y ∈ boxFinset (D.pinOutside S p),
      cutGlue S (cutGlue S y q) p = y := by
    intro p q y hy
    rw [mem_boxFinset, inBox_pinOutside] at hy
    funext i
    by_cases hi : i ∈ S
    · rw [cutGlue_of_mem _ p hi, cutGlue_of_mem y q hi]
    · rw [cutGlue_of_not_mem _ p hi, hy.2 i hi]
  unfold WInstance.Z
  exact Finset.sum_nbij' (fun y => cutGlue S y q) (fun y => cutGlue S y p) (hmaps p q)
    (hmaps q p) (hinv p q) (hinv q p)
    (fun y _ => I.restrict_weight_congr S fun i hi => (cutGlue_of_mem y q hi).symm)

/-! ### Summing out a site: the elimination identities

Site `i` is summed out; it stays in the instance with trivial factors and a singleton domain.
The proofs rest on the factorisation `weight (update x i a) = wbase i x · wlocal i a x`
(`WInstance.weight_update` in `PartitionCertificate.lean`). -/

/-- Membership in a box with site `i` fixed to `a`. -/
theorem inBox_fix_iff {D : Dom n k} {i : Fin n} {a : Fin k} {x : Config n k} :
    InBox (D.fix i a) x ↔ x i = a ∧ ∀ m, m ≠ i → x m ∈ D m := by
  unfold InBox Dom.fix
  constructor
  · intro h
    refine ⟨by simpa using h i, fun m hm => ?_⟩
    have := h m
    rwa [Function.update_of_ne hm] at this
  · rintro ⟨h1, h2⟩ m
    by_cases hm : m = i
    · subst hm
      simp [h1]
    · rw [Function.update_of_ne hm]
      exact h2 m hm

/-- Changing the state of the fixed site is a bijection between the two fixed boxes
(summation form). -/
theorem sum_boxFinset_fix (D : Dom n k) (i : Fin n) (a p : Fin k) (f : Config n k → ℚ) :
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

/-- **Summing out a site.**  If the factors of `I'` at site `i` are trivial and, on the box with
site `i` pinned, the weight of `I'` away from `i` is the weight of `I` away from `i` times the
sum of the local weights of `I` over the states of site `i`, then the partition sum of `I` over
the box is the partition sum of `I'` over the pinned box. -/
theorem WInstance.Z_sumOut (I I' : WInstance n k) (D : Dom n k) (i : Fin n) (p : Fin k)
    (hloc : ∀ (a : Fin k) (y : Config n k), I'.wlocal i a y = 1)
    (hbase : ∀ y, InBox (D.fix i p) y →
      I'.wbase i y = I.wbase i y * ∑ a ∈ (D i).toFinset, I.wlocal i a y) :
    I.Z D = I'.Z (D.fix i p) := by
  have h1 : ∀ a ∈ (D i).toFinset, I.Z (D.fix i a) =
      ∑ y ∈ boxFinset (D.fix i p), I.wbase i y * I.wlocal i a y := by
    intro a _
    unfold WInstance.Z
    rw [sum_boxFinset_fix D i a p]
    apply Finset.sum_congr rfl
    intro y _
    exact I.weight_update y i a
  have h2 : I'.Z (D.fix i p) = ∑ y ∈ boxFinset (D.fix i p), I'.wbase i y := by
    unfold WInstance.Z
    apply Finset.sum_congr rfl
    intro y _
    have h := I'.weight_update y i (y i)
    rw [Function.update_eq_self] at h
    rw [h, hloc, mul_one]
  rw [I.Z_branch D i, h2, Finset.sum_congr rfl h1, Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro y hy
  rw [hbase y (mem_boxFinset.mp hy), Finset.mul_sum]

/-- Sum out site `i`, which interacts only with site `j`: the sum over the states of `i` is
absorbed into the one-body factor of `j`, and all factors at site `i` become `1`. -/
def WInstance.elim1 (I : WInstance n k) (D : Dom n k) (i j : Fin n) : WInstance n k where
  w m b :=
    if m = i then 1
    else if m = j then
      I.w j b * ∑ a ∈ (D i).toFinset, I.w i a * I.W i j a b * I.W j i b a
    else I.w m b
  W m m' b c := if m = i ∨ m' = i then 1 else I.W m m' b c

/-- Sum out site `i`, which interacts only with the sites `j` and `l`: the sum over the states of
`i` is absorbed into the pair factor of the ordered pair `(j, l)`, and all factors at site `i`
become `1`. -/
def WInstance.elim2 (I : WInstance n k) (D : Dom n k) (i j l : Fin n) : WInstance n k where
  w m b := if m = i then 1 else I.w m b
  W m m' b c :=
    if m = i ∨ m' = i then 1
    else if m = j ∧ m' = l then
      I.W j l b c *
        ∑ a ∈ (D i).toFinset, I.w i a * I.W i j a b * I.W j i b a * I.W i l a c * I.W l i c a
    else I.W m m' b c

/-- Check of the rule `elim1`: `i ≠ j`, and on the current domains site `i` has trivial pair
factors (both orientations) with every site other than `j`. -/
def Elim1OK (I : WInstance n k) (D : Dom n k) (i j : Fin n) : Prop :=
  i ≠ j ∧ ∀ m, m ≠ i → m ≠ j → ∀ a ∈ D i, ∀ b ∈ D m, I.W i m a b = 1 ∧ I.W m i b a = 1

/-- The check of `elim1` is decidable. -/
instance decidableElim1OK (I : WInstance n k) (D : Dom n k) (i j : Fin n) :
    Decidable (Elim1OK I D i j) := by
  unfold Elim1OK; infer_instance

/-- Check of the rule `elim2`: `i`, `j`, `l` are pairwise distinct, and on the current domains
site `i` has trivial pair factors (both orientations) with every site other than `j` and `l`. -/
def Elim2OK (I : WInstance n k) (D : Dom n k) (i j l : Fin n) : Prop :=
  i ≠ j ∧ i ≠ l ∧ j ≠ l ∧
    ∀ m, m ≠ i → m ≠ j → m ≠ l → ∀ a ∈ D i, ∀ b ∈ D m, I.W i m a b = 1 ∧ I.W m i b a = 1

/-- The check of `elim2` is decidable. -/
instance decidableElim2OK (I : WInstance n k) (D : Dom n k) (i j l : Fin n) :
    Decidable (Elim2OK I D i j l) := by
  unfold Elim2OK; infer_instance

/-- Pair factors of `I.elim1`. -/
theorem WInstance.elim1_W (I : WInstance n k) (D : Dom n k) (i j m m' : Fin n) (b c : Fin k) :
    (I.elim1 D i j).W m m' b c = if m = i ∨ m' = i then 1 else I.W m m' b c := rfl

/-- One-body factors of `I.elim1` away from the eliminated site. -/
theorem WInstance.elim1_w_of_ne (I : WInstance n k) (D : Dom n k) (i j : Fin n) {m : Fin n}
    (hm : m ≠ i) (b : Fin k) :
    (I.elim1 D i j).w m b = I.w m b *
      if m = j then ∑ a ∈ (D i).toFinset, I.w i a * I.W i j a b * I.W j i b a else 1 := by
  unfold WInstance.elim1
  dsimp only
  rw [if_neg hm]
  by_cases hmj : m = j
  · rw [if_pos hmj, if_pos hmj, hmj]
  · rw [if_neg hmj, if_neg hmj, mul_one]

/-- All factors of `I.elim1` at the eliminated site are trivial. -/
theorem WInstance.elim1_wlocal (I : WInstance n k) (D : Dom n k) (i j : Fin n) (a : Fin k)
    (y : Config n k) : (I.elim1 D i j).wlocal i a y = 1 := by
  unfold WInstance.wlocal WInstance.elim1
  simp

/-- **Elimination of a site with one neighbour is exact** (an identity: no sign condition on the
factors, and the pin `p` is arbitrary). -/
theorem WInstance.Z_elim1 (I : WInstance n k) (D : Dom n k) (i j : Fin n) (p : Fin k)
    (h : Elim1OK I D i j) : I.Z D = (I.elim1 D i j).Z (D.fix i p) := by
  obtain ⟨hij, hone⟩ := h
  apply I.Z_sumOut (I.elim1 D i j) D i p (I.elim1_wlocal D i j)
  intro y hy
  rw [inBox_fix_iff] at hy
  have hj : j ∈ univ.erase i := Finset.mem_erase.mpr ⟨fun e => hij e.symm, mem_univ j⟩
  have hloc : ∀ a ∈ (D i).toFinset,
      I.wlocal i a y = I.w i a * I.W i j a (y j) * I.W j i (y j) a := by
    intro a ha
    unfold WInstance.wlocal
    rw [Finset.prod_eq_single_of_mem j hj]
    · ring
    · intro m hm hmj
      have hmi := Finset.ne_of_mem_erase hm
      obtain ⟨e1, e2⟩ := hone m hmi hmj a (List.mem_toFinset.mp ha) (y m) (hy.2 m hmi)
      rw [e1, e2, mul_one]
  rw [Finset.sum_congr rfl hloc]
  unfold WInstance.wbase
  have hw : ∏ m ∈ univ.erase i, (I.elim1 D i j).w m (y m) =
      (∏ m ∈ univ.erase i, I.w m (y m)) *
        ∑ a ∈ (D i).toFinset, I.w i a * I.W i j a (y j) * I.W j i (y j) a := by
    rw [Finset.prod_congr rfl fun m hm => I.elim1_w_of_ne D i j (Finset.ne_of_mem_erase hm) (y m),
      Finset.prod_mul_distrib, Finset.prod_ite_eq', if_pos hj]
  have hW : ∏ m ∈ univ.erase i, ∏ m' ∈ (univ.erase m).erase i,
        (I.elim1 D i j).W m m' (y m) (y m') =
      ∏ m ∈ univ.erase i, ∏ m' ∈ (univ.erase m).erase i, I.W m m' (y m) (y m') := by
    apply Finset.prod_congr rfl
    intro m hm
    apply Finset.prod_congr rfl
    intro m' hm'
    rw [I.elim1_W, if_neg]
    rintro (e | e)
    · exact Finset.ne_of_mem_erase hm e
    · exact Finset.ne_of_mem_erase hm' e
  rw [hw, hW]
  ring

/-- Eliminating a site with one neighbour preserves nonnegativity of the factors. -/
theorem WInstance.elim1_nonneg {I : WInstance n k} (hI : I.Nonneg) (D : Dom n k) (i j : Fin n) :
    (I.elim1 D i j).Nonneg := by
  constructor
  · intro m b
    unfold WInstance.elim1
    dsimp only
    split_ifs
    · exact zero_le_one
    · exact mul_nonneg (hI.1 j b) (Finset.sum_nonneg fun a _ =>
        mul_nonneg (mul_nonneg (hI.1 i a) (hI.2 i j a b)) (hI.2 j i b a))
    · exact hI.1 m b
  · intro m m' b c
    rw [I.elim1_W]
    split_ifs
    · exact zero_le_one
    · exact hI.2 m m' b c

/-- One-body factors of `I.elim2`. -/
theorem WInstance.elim2_w (I : WInstance n k) (D : Dom n k) (i j l m : Fin n) (b : Fin k) :
    (I.elim2 D i j l).w m b = if m = i then 1 else I.w m b := rfl

/-- Pair factors of `I.elim2` away from the eliminated site. -/
theorem WInstance.elim2_W_of_ne (I : WInstance n k) (D : Dom n k) (i j l : Fin n)
    {m m' : Fin n} (hm : m ≠ i) (hm' : m' ≠ i) (b c : Fin k) :
    (I.elim2 D i j l).W m m' b c = I.W m m' b c *
      if m = j ∧ m' = l then
        ∑ a ∈ (D i).toFinset, I.w i a * I.W i j a b * I.W j i b a * I.W i l a c * I.W l i c a
      else 1 := by
  unfold WInstance.elim2
  dsimp only
  rw [if_neg (by rintro (e | e); exacts [hm e, hm' e])]
  by_cases hjl : m = j ∧ m' = l
  · rw [if_pos hjl, if_pos hjl, hjl.1, hjl.2]
  · rw [if_neg hjl, if_neg hjl, mul_one]

/-- All factors of `I.elim2` at the eliminated site are trivial. -/
theorem WInstance.elim2_wlocal (I : WInstance n k) (D : Dom n k) (i j l : Fin n) (a : Fin k)
    (y : Config n k) : (I.elim2 D i j l).wlocal i a y = 1 := by
  unfold WInstance.wlocal WInstance.elim2
  simp

/-- **Elimination of a site with two neighbours is exact** (an identity: no sign condition on
the factors, and the pin `p` is arbitrary). -/
theorem WInstance.Z_elim2 (I : WInstance n k) (D : Dom n k) (i j l : Fin n) (p : Fin k)
    (h : Elim2OK I D i j l) : I.Z D = (I.elim2 D i j l).Z (D.fix i p) := by
  obtain ⟨hij, hil, hjl, hone⟩ := h
  apply I.Z_sumOut (I.elim2 D i j l) D i p (I.elim2_wlocal D i j l)
  intro y hy
  rw [inBox_fix_iff] at hy
  have hj : j ∈ univ.erase i := Finset.mem_erase.mpr ⟨fun e => hij e.symm, mem_univ j⟩
  have hl : l ∈ univ.erase i := Finset.mem_erase.mpr ⟨fun e => hil e.symm, mem_univ l⟩
  have hl' : l ∈ (univ.erase j).erase i :=
    Finset.mem_erase.mpr ⟨fun e => hil e.symm, Finset.mem_erase.mpr ⟨fun e => hjl e.symm,
      mem_univ l⟩⟩
  have hloc : ∀ a ∈ (D i).toFinset, I.wlocal i a y =
      I.w i a * I.W i j a (y j) * I.W j i (y j) a * I.W i l a (y l) * I.W l i (y l) a := by
    intro a ha
    unfold WInstance.wlocal
    rw [Finset.prod_eq_mul_of_mem j l hj hl hjl]
    · ring
    · intro m hm hmjl
      have hmi := Finset.ne_of_mem_erase hm
      obtain ⟨e1, e2⟩ := hone m hmi hmjl.1 hmjl.2 a (List.mem_toFinset.mp ha) (y m)
        (hy.2 m hmi)
      rw [e1, e2, mul_one]
  rw [Finset.sum_congr rfl hloc]
  unfold WInstance.wbase
  have hw : ∏ m ∈ univ.erase i, (I.elim2 D i j l).w m (y m) =
      ∏ m ∈ univ.erase i, I.w m (y m) := by
    apply Finset.prod_congr rfl
    intro m hm
    rw [I.elim2_w, if_neg (Finset.ne_of_mem_erase hm)]
  have hW : ∏ m ∈ univ.erase i, ∏ m' ∈ (univ.erase m).erase i,
        (I.elim2 D i j l).W m m' (y m) (y m') =
      (∏ m ∈ univ.erase i, ∏ m' ∈ (univ.erase m).erase i, I.W m m' (y m) (y m')) *
        ∑ a ∈ (D i).toFinset,
          I.w i a * I.W i j a (y j) * I.W j i (y j) a * I.W i l a (y l) * I.W l i (y l) a := by
    have hsplit : ∀ m ∈ univ.erase i, ∏ m' ∈ (univ.erase m).erase i,
          (I.elim2 D i j l).W m m' (y m) (y m') =
        (∏ m' ∈ (univ.erase m).erase i, I.W m m' (y m) (y m')) *
          if m = j then ∑ a ∈ (D i).toFinset,
            I.w i a * I.W i j a (y j) * I.W j i (y j) a * I.W i l a (y l) * I.W l i (y l) a
          else 1 := by
      intro m hm
      rw [Finset.prod_congr rfl fun m' hm' => I.elim2_W_of_ne D i j l
        (Finset.ne_of_mem_erase hm) (Finset.ne_of_mem_erase hm') (y m) (y m'),
        Finset.prod_mul_distrib]
      congr 1
      by_cases hmj : m = j
      · subst hmj
        rw [if_pos rfl, Finset.prod_eq_single_of_mem l hl']
        · rw [if_pos ⟨rfl, rfl⟩]
        · intro m' _ hm'l
          rw [if_neg fun e => hm'l e.2]
      · rw [if_neg hmj]
        apply Finset.prod_eq_one
        intro m' _
        rw [if_neg fun e => hmj e.1]
    rw [Finset.prod_congr rfl hsplit, Finset.prod_mul_distrib, Finset.prod_ite_eq', if_pos hj]
  rw [hw, hW]
  ring

/-- Eliminating a site with two neighbours preserves nonnegativity of the factors. -/
theorem WInstance.elim2_nonneg {I : WInstance n k} (hI : I.Nonneg) (D : Dom n k)
    (i j l : Fin n) : (I.elim2 D i j l).Nonneg := by
  constructor
  · intro m b
    rw [I.elim2_w]
    split_ifs
    · exact zero_le_one
    · exact hI.1 m b
  · intro m m' b c
    unfold WInstance.elim2
    dsimp only
    split_ifs
    · exact zero_le_one
    · exact mul_nonneg (hI.2 j l b c) (Finset.sum_nonneg fun a _ =>
        mul_nonneg (mul_nonneg (mul_nonneg (mul_nonneg (hI.1 i a) (hI.2 i j a b))
          (hI.2 j i b a)) (hI.2 i l a c)) (hI.2 l i c a))
    · exact hI.2 m m' b c

/-! ### Certificates and the kernel -/

/-- Cut check: the pin lies in the box, and the pair factors across the cut are bounded
(`CutBoundsOK`).  The pin makes the box non-empty, which forces `0 ≤ lo ≤ hi` across the cut
(used for `Υ ≥ 0` in `zverify2_sound`; the cut inequality `WInstance.Z_cut` itself needs no
condition on the pin). -/
def CutOK (I : WInstance n k) (D : Dom n k) (S : Finset (Fin n)) (p : Config n k)
    (lo hi : Fin n → Fin n → ℚ) : Prop :=
  (∀ i, p i ∈ D i) ∧ CutBoundsOK I D S lo hi

/-- The cut check is decidable. -/
instance decidableCutOK (I : WInstance n k) (D : Dom n k) (S : Finset (Fin n)) (p : Config n k)
    (lo hi : Fin n → Fin n → ℚ) : Decidable (CutOK I D S p lo hi) := by
  unfold CutOK; infer_instance

/-- Certificates of the partition kernel extended by the cut rule and the elimination rules. -/
inductive ZCert2 (n k : ℕ) : Type
  /-- a certificate of the kernel `zverify` (leaf, branch, thermal prune) -/
  | base (c : ZCert n k) : ZCert2 n k
  /-- case split on the state of site `i` -/
  | branch (i : Fin n) (children : Fin k → ZCert2 n k) : ZCert2 n k
  /-- cut `S | Sᶜ` with pin `p`, bounds `lo`, `hi` on the pair factors across the cut, and one
  certificate for each half -/
  | cut (S : Finset (Fin n)) (p : Config n k) (lo hi : Fin n → Fin n → ℚ)
      (c₁ c₂ : ZCert2 n k) : ZCert2 n k
  /-- sum out site `i`, whose only neighbour is `j`, and pin it to the state `p` -/
  | elim1 (i j : Fin n) (p : Fin k) (rest : ZCert2 n k) : ZCert2 n k
  /-- sum out site `i`, whose only neighbours are `j` and `l`, and pin it to the state `p` -/
  | elim2 (i j l : Fin n) (p : Fin k) (rest : ZCert2 n k) : ZCert2 n k

/-- Product of two optional intervals with nonnegative lower endpoints, scaled by the cut
constants `Λ` (lower endpoint) and `Υ` (upper endpoint); `none` if an interval is missing or a
lower endpoint is negative. -/
def cutIv (Λ Υ : ℚ) : Option (ℚ × ℚ) → Option (ℚ × ℚ) → Option (ℚ × ℚ)
  | some (l₁, h₁), some (l₂, h₂) =>
      if 0 ≤ l₁ ∧ 0 ≤ l₂ then some (Λ * l₁ * l₂, Υ * h₁ * h₂) else none
  | _, _ => none

/-- **The extended partition-function kernel** (cut and elimination rules).  Returns a
certified interval `(lo, hi)` for the partition sum over the box, or `none` if a check fails.  A
`base` node hands over to `zverify`; a `branch` node adds the intervals of the children over the
distinct states of the site; a `cut` node multiplies the intervals of the two halves (on the
restricted instances over the pinned boxes) and the cut constants; an `elim1` or `elim2` node
sums out one site and continues with the resulting instance. -/
def zverify2 : ZCert2 n k → WInstance n k → Dom n k → Option (ℚ × ℚ)
  | .base c, I, D => zverify c I D
  | .branch i ch, I, D =>
      (D i).dedup.foldr (fun a acc => addIv (zverify2 (ch a) I (D.fix i a)) acc) (some (0, 0))
  | .cut S p lo hi c₁ c₂, I, D =>
      if CutOK I D S p lo hi then
        cutIv (cutConst S lo) (cutConst S hi) (zverify2 c₁ (I.restrict S) (D.pinOutside S p))
          (zverify2 c₂ (I.restrict Sᶜ) (D.pinOutside Sᶜ p))
      else none
  | .elim1 i j p rest, I, D =>
      if Elim1OK I D i j then zverify2 rest (I.elim1 D i j) (D.fix i p) else none
  | .elim2 i j l p rest, I, D =>
      if Elim2OK I D i j l then zverify2 rest (I.elim2 D i j l) (D.fix i p) else none

/-! ### Soundness -/

/-- Soundness of the interval product of the cut rule: enclosures of two nonnegative numbers
`Z₁`, `Z₂` and a two-sided cut inequality for `Z` give an enclosure of `Z`. -/
theorem cutIv_sound {Λ Υ Z Z₁ Z₂ : ℚ} (hΛ : 0 ≤ Λ) (hΥ : 0 ≤ Υ) (hZ₁ : 0 ≤ Z₁) (hZ₂ : 0 ≤ Z₂)
    (hcut : Λ * (Z₁ * Z₂) ≤ Z ∧ Z ≤ Υ * (Z₁ * Z₂)) {iv₁ iv₂ : Option (ℚ × ℚ)}
    (h₁ : ∀ l h, iv₁ = some (l, h) → l ≤ Z₁ ∧ Z₁ ≤ h)
    (h₂ : ∀ l h, iv₂ = some (l, h) → l ≤ Z₂ ∧ Z₂ ≤ h) {lo hi : ℚ}
    (hv : cutIv Λ Υ iv₁ iv₂ = some (lo, hi)) : lo ≤ Z ∧ Z ≤ hi := by
  cases iv₁ with
  | none => simp [cutIv] at hv
  | some lh₁ =>
    obtain ⟨l₁, u₁⟩ := lh₁
    cases iv₂ with
    | none => simp [cutIv] at hv
    | some lh₂ =>
      obtain ⟨l₂, u₂⟩ := lh₂
      simp only [cutIv] at hv
      split_ifs at hv with hnn
      simp only [Option.some.injEq, Prod.mk.injEq] at hv
      obtain ⟨rfl, rfl⟩ := hv
      have e₁ := h₁ l₁ u₁ rfl
      have e₂ := h₂ l₂ u₂ rfl
      have hlow : l₁ * l₂ ≤ Z₁ * Z₂ := mul_le_mul e₁.1 e₂.1 hnn.2 hZ₁
      have hupp : Z₁ * Z₂ ≤ u₁ * u₂ := mul_le_mul e₁.2 e₂.2 hZ₂ (le_trans hZ₁ e₁.2)
      constructor
      · calc Λ * l₁ * l₂ = Λ * (l₁ * l₂) := by ring
          _ ≤ Λ * (Z₁ * Z₂) := mul_le_mul_of_nonneg_left hlow hΛ
          _ ≤ Z := hcut.1
      · calc Z ≤ Υ * (Z₁ * Z₂) := hcut.2
          _ ≤ Υ * (u₁ * u₂) := mul_le_mul_of_nonneg_left hupp hΥ
          _ = Υ * u₁ * u₂ := by ring

/-- **Master Soundness Theorem of the extended partition kernel** (cut and elimination rules).
If the kernel returns the interval `(lo, hi)` for an instance with nonnegative factors, then
`lo ≤ Z ≤ hi` for the exact rational partition sum over the box. -/
theorem zverify2_sound {I : WInstance n k} (hI : I.Nonneg) (c : ZCert2 n k) (D : Dom n k)
    (lo hi : ℚ) (hv : zverify2 c I D = some (lo, hi)) : lo ≤ I.Z D ∧ I.Z D ≤ hi := by
  induction c generalizing I D lo hi with
  | base c => exact zverify_sound hI c D lo hi hv
  | branch i ch ih =>
    unfold zverify2 at hv
    have key := foldr_addIv_sound (fun a => I.Z (D.fix i a))
      (fun a => zverify2 (ch a) I (D.fix i a))
      (fun a l h hval => ih a hI (D.fix i a) l h hval) (D i).dedup (List.nodup_dedup _) lo hi hv
    have hded : (D i).dedup.toFinset = (D i).toFinset := by
      ext a
      simp
    rw [hded] at key
    rw [I.Z_branch D i]
    exact key
  | cut S p l h c₁ c₂ ih₁ ih₂ =>
    unfold zverify2 at hv
    split_ifs at hv with hok
    have hhi : ∀ i, ∀ j ∈ univ.erase i, ¬ (i ∈ S ↔ j ∈ S) → 0 ≤ h i j := fun i j hj hij =>
      le_trans (hI.2 i j (p i) (p j)) ((hok.2 i j hj hij).2 (p i) (hok.1 i) (p j) (hok.1 j)).2
    exact cutIv_sound (cutConst_nonneg S l fun i j hj hij => (hok.2 i j hj hij).1)
      (cutConst_nonneg S h hhi) ((I.restrict S).Z_nonneg (I.restrict_nonneg hI S) _)
      ((I.restrict Sᶜ).Z_nonneg (I.restrict_nonneg hI Sᶜ) _) (I.Z_cut hI D S p l h hok.2)
      (fun l₁ h₁ e => ih₁ (I.restrict_nonneg hI S) _ l₁ h₁ e)
      (fun l₂ h₂ e => ih₂ (I.restrict_nonneg hI Sᶜ) _ l₂ h₂ e) hv
  | elim1 i j p rest ih =>
    unfold zverify2 at hv
    split_ifs at hv with hok
    rw [I.Z_elim1 D i j p hok]
    exact ih (I.elim1_nonneg hI D i j) _ lo hi hv
  | elim2 i j l p rest ih =>
    unfold zverify2 at hv
    split_ifs at hv with hok
    rw [I.Z_elim2 D i j l p hok]
    exact ih (I.elim2_nonneg hI D i j l) _ lo hi hv

/-- **Top-level extended kernel**: reject instances with a negative factor, then run
`zverify2`. -/
def zverify2Top (c : ZCert2 n k) (I : WInstance n k) (D : Dom n k) : Option (ℚ × ℚ) :=
  if I.Nonneg then zverify2 c I D else none

/-- **Master Soundness Theorem of the top-level extended kernel** — no side condition is left
to the caller: whatever the instance and the certificate, a returned interval contains the exact
rational partition sum over the box. -/
theorem zverify2Top_sound (c : ZCert2 n k) (I : WInstance n k) (D : Dom n k) (lo hi : ℚ)
    (hv : zverify2Top c I D = some (lo, hi)) : lo ≤ I.Z D ∧ I.Z D ≤ hi := by
  unfold zverify2Top at hv
  split_ifs at hv with hI
  exact zverify2_sound hI c D lo hi hv

/-- Acceptance by the top-level kernel means: nonnegative factors and acceptance by
`zverify2`. -/
theorem zverify2Top_eq_some {c : ZCert2 n k} {I : WInstance n k} {D : Dom n k} {r : ℚ × ℚ}
    (hv : zverify2Top c I D = some r) : I.Nonneg ∧ zverify2 c I D = some r := by
  unfold zverify2Top at hv
  split_ifs at hv with hI
  exact ⟨hI, hv⟩

/-- The extended kernel is conservative: on `base` certificates it is the top-level kernel
`zverifyTop`. -/
theorem zverify2Top_base (c : ZCert n k) (I : WInstance n k) (D : Dom n k) :
    zverify2Top (.base c) I D = zverifyTop c I D := rfl

/-! ### Kernel runs: independent and weakly coupled triangles

Two frustrated triangles `{0, 1, 2}` and `{3, 4, 5}` on six binary sites, pair factor `1/2` for
equal states inside a triangle (the instance `triangleW` twice).  All results below are obtained
by running the checker inside Lean's kernel on exact rationals. -/

/-- Exact leaf at a single configuration: the pair bounds are the pair factors at `x`. -/
def pointZLeaf (I : WInstance n k) (x : Config n k) : ZCert n k :=
  .leaf (fun i j => I.W i j (x i) (x j)) (fun i j => I.W i j (x i) (x j))

/-- Two disjoint frustrated triangles `{0, 1, 2}` and `{3, 4, 5}` in the weight domain: pair
factor `1/2` for equal states on the pairs `i < j` of the same triangle, `1` otherwise. -/
def twoTrianglesW : WInstance 6 2 where
  w := fun _ _ => 1
  W := fun i j a b => if i < j ∧ (i < 3 ↔ j < 3) ∧ a = b then 1 / 2 else 1

/-- Cut into the two triangles (cut bounds `1`), each half certified by full enumeration of its
three sites: `2 · 8 = 16` leaves. -/
def twoTrianglesCert : ZCert2 6 2 :=
  .cut {0, 1, 2} (fun _ => 0) (fun _ _ => 1) (fun _ _ => 1)
    (.base (.branch 0 fun a => .branch 1 fun b => .branch 2 fun c =>
      pointZLeaf (twoTrianglesW.restrict {0, 1, 2}) ![a, b, c, 0, 0, 0]))
    (.base (.branch 3 fun a => .branch 4 fun b => .branch 5 fun c =>
      pointZLeaf (twoTrianglesW.restrict {0, 1, 2}ᶜ) ![0, 0, 0, a, b, c]))

/-- **The cut rule on independent subsystems.**  From the cut certificate the top-level kernel
computes the exact partition sum `(13/4)² = 169/16` of the two triangles. -/
theorem twoTriangles_cut_exact :
    zverify2Top twoTrianglesCert twoTrianglesW (fullDom 6 2) = some (169 / 16, 169 / 16) := by
  decide +kernel

/-- Hence the partition sum of the two triangles is `169/16`. -/
theorem twoTriangles_Z : twoTrianglesW.Z (fullDom 6 2) = 169 / 16 := by
  have h := zverify2Top_sound _ _ _ _ _ twoTriangles_cut_exact
  exact le_antisymm h.2 h.1

/-- Two frustrated triangles joined by one weak bond between the sites `2` and `3`: pair factor
`9/10` for equal states on that bond. -/
def coupledTrianglesW : WInstance 6 2 where
  w := fun _ _ => 1
  W := fun i j a b =>
    if i < j ∧ (i < 3 ↔ j < 3) ∧ a = b then 1 / 2
    else if i = 2 ∧ j = 3 ∧ a = b then 9 / 10 else 1

/-- One cut through the weak bond, with bounds `[9/10, 1]` on it and `[1, 1]` on the other pairs
across the cut; each triangle is enumerated. -/
def coupledTrianglesCert : ZCert2 6 2 :=
  .cut {0, 1, 2} (fun _ => 0) (fun i j => if i = 2 ∧ j = 3 then 9 / 10 else 1) (fun _ _ => 1)
    (.base (.branch 0 fun a => .branch 1 fun b => .branch 2 fun c =>
      pointZLeaf (coupledTrianglesW.restrict {0, 1, 2}) ![a, b, c, 0, 0, 0]))
    (.base (.branch 3 fun a => .branch 4 fun b => .branch 5 fun c =>
      pointZLeaf (coupledTrianglesW.restrict {0, 1, 2}ᶜ) ![0, 0, 0, a, b, c]))

/-- **The cut rule across a weak bond**: the kernel returns the enclosure
`[9/10 · 169/16, 169/16] = [1521/160, 169/16]`. -/
theorem coupledTriangles_cut_enclosure :
    zverify2Top coupledTrianglesCert coupledTrianglesW (fullDom 6 2) =
      some (1521 / 160, 169 / 16) := by
  decide +kernel

/-- Branch on the two ends `2`, `3` of the weak bond; in every branch the pair factors across
the cut are constant on the box, so the cut is exact (`4 · (4 + 4) = 32` leaves). -/
def coupledTrianglesExactCert : ZCert2 6 2 :=
  .branch 2 fun u => .branch 3 fun v =>
    .cut {0, 1, 2} ![0, 0, u, v, 0, 0]
      (fun i j => coupledTrianglesW.W i j (![0, 0, u, v, 0, 0] i) (![0, 0, u, v, 0, 0] j))
      (fun i j => coupledTrianglesW.W i j (![0, 0, u, v, 0, 0] i) (![0, 0, u, v, 0, 0] j))
      (.base (.branch 0 fun a => .branch 1 fun b =>
        pointZLeaf (coupledTrianglesW.restrict {0, 1, 2}) ![a, b, u, v, 0, 0]))
      (.base (.branch 4 fun a => .branch 5 fun b =>
        pointZLeaf (coupledTrianglesW.restrict {0, 1, 2}ᶜ) ![0, 0, u, v, a, b]))

/-- **Branch, then cut**: conditioning on the interface sites makes the two halves independent,
and the kernel computes the exact partition sum `3211/320` of the coupled triangles. -/
theorem coupledTriangles_branch_cut_exact :
    zverify2Top coupledTrianglesExactCert coupledTrianglesW (fullDom 6 2) =
      some (3211 / 320, 3211 / 320) := by
  decide +kernel

/-- Hence the partition sum of the coupled triangles is `3211/320`. -/
theorem coupledTriangles_Z : coupledTrianglesW.Z (fullDom 6 2) = 3211 / 320 := by
  have h := zverify2Top_sound _ _ _ _ _ coupledTriangles_branch_cut_exact
  exact le_antisymm h.2 h.1

/-- The enclosure `[1521/160, 169/16]` of the single cut through the weak bond is strict on both
sides. -/
theorem coupledTriangles_cut_strict :
    1521 / 160 < coupledTrianglesW.Z (fullDom 6 2) ∧
      coupledTrianglesW.Z (fullDom 6 2) < 169 / 16 := by
  rw [coupledTriangles_Z]
  constructor <;> norm_num

/-- The check of the cut bounds matters: the certificate of the *independent* triangles claims
the bounds `[1, 1]` across the cut, and the kernel rejects it on the coupled instance. -/
theorem coupledTriangles_cut_rejected :
    zverify2Top twoTrianglesCert coupledTrianglesW (fullDom 6 2) = none := by
  decide +kernel

/-! ### Kernel runs: elimination on a chain, on a tree and on a ring

One ordered pair per bond, pair factor `1/2` for unequal neighbours (transfer matrix
`T = (1, 1/2; 1/2, 1)` with eigenvalues `3/2` and `1/2`). -/

/-- Leaf with the pair bounds `[1, 1]`; it is exact once all pair factors are `1` on the box
(`zverify_unitZLeaf`). -/
def unitZLeaf : ZCert n k := .leaf (fun _ _ => 1) (fun _ _ => 1)

/-- Ferromagnetic two-state chain on six sites in the weight domain: pair factor `1/2` for
unequal states on the ordered pairs `(i, i + 1)`, `1` otherwise. -/
def chainW : WInstance 6 2 where
  w := fun _ _ => 1
  W := fun i j a b => if j.val = i.val + 1 ∧ a ≠ b then 1 / 2 else 1

/-- Transfer-matrix certificate of the six-site chain: eliminate site `0` into `1`, `1` into
`2`, …, `4` into `5`, then one leaf. -/
def chainCert6 : ZCert2 6 2 :=
  .elim1 0 1 0 (.elim1 1 2 0 (.elim1 2 3 0 (.elim1 3 4 0 (.elim1 4 5 0 (.base unitZLeaf)))))

/-- **Elimination on a chain.**  From five eliminations and one leaf the top-level kernel
computes the exact partition sum `2 · (3/2)⁵ = 243/16` of the six-site chain. -/
theorem chain_elim_exact :
    zverify2Top chainCert6 chainW (fullDom 6 2) = some (243 / 16, 243 / 16) := by
  decide +kernel

/-- Hence the partition sum of the six-site chain is `243/16`. -/
theorem chain_Z : chainW.Z (fullDom 6 2) = 243 / 16 := by
  have h := zverify2Top_sound _ _ _ _ _ chain_elim_exact
  exact le_antisymm h.2 h.1

/-- Ferromagnetic two-state tree on five sites with the bonds `0–1`, `0–2`, `0–3` and `3–4` (a
branch point at site `0`): pair factor `1/2` for unequal states on these ordered pairs, `1`
otherwise. -/
def treeW : WInstance 5 2 where
  w := fun _ _ => 1
  W := fun i j a b =>
    if ((i.val = 0 ∧ (j.val = 1 ∨ j.val = 2 ∨ j.val = 3)) ∨ (i.val = 3 ∧ j.val = 4)) ∧ a ≠ b
    then 1 / 2 else 1

/-- Elimination certificate of the tree: sum out the leaves `1`, `2` and `4` of the tree into
their neighbours, then site `3` into site `0`, then one leaf of the certificate. -/
def treeCert : ZCert2 5 2 :=
  .elim1 1 0 0 (.elim1 2 0 0 (.elim1 4 3 0 (.elim1 3 0 0 (.base unitZLeaf))))

/-- **Elimination on a tree.**  From four `elim1` nodes and one leaf the top-level kernel
computes the exact partition sum `2 · (3/2)⁴ = 81/8` of the tree. -/
theorem tree_elim_exact :
    zverify2Top treeCert treeW (fullDom 5 2) = some (81 / 8, 81 / 8) := by
  decide +kernel

/-- Ferromagnetic two-state ring on five sites: pair factor `1/2` for unequal states on the
ordered pairs `(i, i + 1)` and `(4, 0)`, `1` otherwise. -/
def ringW : WInstance 5 2 where
  w := fun _ _ => 1
  W := fun i j a b =>
    if (j.val = i.val + 1 ∨ (i.val = 4 ∧ j.val = 0)) ∧ a ≠ b then 1 / 2 else 1

/-- Elimination certificate of the ring: sum out site `0` (neighbours `1`, `4`), then `1`
(neighbours `2`, `4`), then `2` (neighbours `3`, `4`), then `3` into `4`, then one leaf. -/
def ringCert : ZCert2 5 2 :=
  .elim2 0 1 4 0 (.elim2 1 2 4 0 (.elim2 2 3 4 0 (.elim1 3 4 0 (.base unitZLeaf))))

/-- **Elimination on a ring.**  From three `elim2` nodes, one `elim1` node and one leaf the
top-level kernel computes the exact partition sum `(3/2)⁵ + (1/2)⁵ = 61/8` of the ring. -/
theorem ring_elim_exact :
    zverify2Top ringCert ringW (fullDom 5 2) = some (61 / 8, 61 / 8) := by
  decide +kernel

/-- Hence the partition sum of the ring is `61/8`. -/
theorem ring_Z : ringW.Z (fullDom 5 2) = 61 / 8 := by
  have h := zverify2Top_sound _ _ _ _ _ ring_elim_exact
  exact le_antisymm h.2 h.1

/-! ### Separation: elementary certificates with an exact lower endpoint enumerate the box

Leaf counts, and a lower bound for *elementary* certificates (no `cut`, no `elim1`, no `elim2`):
on an instance with positive factors in which every site has a partner whose pair factors tell
its states apart, a leaf whose lower endpoint is exact covers at most one configuration,
branching only partitions the box, and pruning cannot remove anything.  Hence such a certificate
has at least as many leaves as the box has configurations — for independent subsystems the
product of the sizes of their state spaces, for a chain of `n` sites `kⁿ`. -/

/-- All factors are strictly positive. -/
def WInstance.Pos (I : WInstance n k) : Prop :=
  (∀ i a, 0 < I.w i a) ∧ ∀ i j a b, 0 < I.W i j a b

/-- Positivity of the factors is decidable. -/
instance WInstance.decidablePos (I : WInstance n k) : Decidable I.Pos := by
  unfold WInstance.Pos
  infer_instance

/-- Positive factors are nonnegative. -/
theorem WInstance.Pos.nonneg {I : WInstance n k} (hI : I.Pos) : I.Nonneg :=
  ⟨fun i a => (hI.1 i a).le, fun i j a b => (hI.2 i j a b).le⟩

/-- With positive factors every configuration has a positive weight. -/
theorem WInstance.weight_pos {I : WInstance n k} (hI : I.Pos) (x : Config n k) :
    0 < I.weight x :=
  mul_pos (Finset.prod_pos fun i _ => hI.1 i (x i))
    (Finset.prod_pos fun i _ => Finset.prod_pos fun j _ => hI.2 i j (x i) (x j))

/-- Every site `i` has a partner site `j` whose pair factors (in one of the two orientations)
tell any two states of `i` apart, whatever the state of `j`.

This is a property of the *representation* of the instance, not of the model it defines: the
two ordered factors `W i j` and `W j i` are examined separately, so an instance in which they
compensate each other (every configuration of weight one) can be rigid — see
`gauge_trivial_separation` in `RefereeLemmas.lean`.  The separation theorems that assume
`Rigid` are therefore statements about what the leaf rule can do with the given tables. -/
def WInstance.Rigid (I : WInstance n k) : Prop :=
  ∀ i, ∃ j, j ≠ i ∧ ∀ a a' b, a ≠ a' →
    I.W i j a b ≠ I.W i j a' b ∨ I.W j i b a ≠ I.W j i b a'

/-- Rigidity is decidable. -/
instance WInstance.decidableRigid (I : WInstance n k) : Decidable I.Rigid := by
  unfold WInstance.Rigid
  infer_instance

/-- Number of leaves of a certificate of the kernel `zverify` (a branch node counts the leaves
of all its `k` children). -/
def ZCert.leaves : ZCert n k → ℕ
  | .leaf _ _ => 1
  | .branch _ ch => ∑ a, (ch a).leaves
  | .prune _ _ _ _ _ rest => rest.leaves

/-- Number of leaves of a certificate of the extended kernel. -/
def ZCert2.leaves : ZCert2 n k → ℕ
  | .base c => c.leaves
  | .branch _ ch => ∑ a, (ch a).leaves
  | .cut _ _ _ _ c₁ c₂ => c₁.leaves + c₂.leaves
  | .elim1 _ _ _ rest => rest.leaves
  | .elim2 _ _ _ _ rest => rest.leaves

/-- Number of elimination nodes (`elim1` and `elim2`) of a certificate. -/
def ZCert2.elims : ZCert2 n k → ℕ
  | .base _ => 0
  | .branch _ ch => ∑ a, (ch a).elims
  | .cut _ _ _ _ c₁ c₂ => c₁.elims + c₂.elims
  | .elim1 _ _ _ rest => rest.elims + 1
  | .elim2 _ _ _ _ rest => rest.elims + 1

/-- A certificate is *elementary* if it contains no `cut`, `elim1` or `elim2` node: it uses the
rules of `zverify` (leaf, branch, thermal prune) only. -/
def ZCert2.Elementary : ZCert2 n k → Prop
  | .base _ => True
  | .branch _ ch => ∀ a, (ch a).Elementary
  | .cut _ _ _ _ _ _ => False
  | .elim1 _ _ _ _ => False
  | .elim2 _ _ _ _ _ => False

/-- A leaf whose lower endpoint is exact, on an instance with positive factors: every pair factor
equals its lower bound at every configuration of the box. -/
theorem zleaf_exact_const {I : WInstance n k} (hI : I.Pos) (D : Dom n k)
    (lo hi : Fin n → Fin n → ℚ) (h : LeafZOK I D lo hi)
    (hex : (∏ i, ∑ a ∈ (D i).toFinset, I.w i a) * ∏ i, ∏ j ∈ univ.erase i, lo i j = I.Z D)
    (x : Config n k) (hx : InBox D x) (i j : Fin n) (hj : j ∈ univ.erase i) :
    I.W i j (x i) (x j) = lo i j := by
  have hprod : (∏ i, ∑ a ∈ (D i).toFinset, I.w i a) = ∑ x ∈ boxFinset D, ∏ i, I.w i (x i) := by
    unfold boxFinset
    exact Finset.prod_univ_sum (fun i => (D i).toFinset) (fun i a => I.w i a)
  rw [hprod, Finset.sum_mul] at hex
  unfold WInstance.Z WInstance.weight at hex
  have hle : ∀ y ∈ boxFinset D, (∏ i, I.w i (y i)) * ∏ i, ∏ j ∈ univ.erase i, lo i j ≤
      (∏ i, I.w i (y i)) * ∏ i, ∏ j ∈ univ.erase i, I.W i j (y i) (y j) := by
    intro y hy
    have hyD := mem_boxFinset.mp hy
    apply mul_le_mul_of_nonneg_left _ (Finset.prod_nonneg fun i _ => (hI.1 i (y i)).le)
    apply Finset.prod_le_prod
    · intro i _
      exact Finset.prod_nonneg fun j hj => (h i j hj).1
    · intro i _
      apply Finset.prod_le_prod
      · intro j hj
        exact (h i j hj).1
      · intro j hj
        exact ((h i j hj).2 (y i) (hyD i) (y j) (hyD j)).1
  have heq := (Finset.sum_eq_sum_iff_of_le hle).mp hex x (mem_boxFinset.mpr hx)
  have hw : 0 < ∏ i, I.w i (x i) := Finset.prod_pos fun i _ => hI.1 i (x i)
  have hL : ∏ i, ∏ j ∈ univ.erase i, lo i j = ∏ i, ∏ j ∈ univ.erase i, I.W i j (x i) (x j) :=
    mul_left_cancel₀ hw.ne' heq
  have hWpos : 0 < ∏ i, ∏ j ∈ univ.erase i, I.W i j (x i) (x j) :=
    Finset.prod_pos fun i _ => Finset.prod_pos fun j _ => hI.2 i j (x i) (x j)
  have hlopos : ∀ i, ∀ j ∈ univ.erase i, 0 < lo i j := by
    intro i' j' hj'
    apply lt_of_le_of_ne (h i' j' hj').1
    intro h0
    have hzero : ∏ i, ∏ j ∈ univ.erase i, lo i j = 0 :=
      Finset.prod_eq_zero (mem_univ i') (Finset.prod_eq_zero hj' h0.symm)
    rw [← hL, hzero] at hWpos
    exact lt_irrefl _ hWpos
  by_contra hne
  have hlt : lo i j < I.W i j (x i) (x j) :=
    lt_of_le_of_ne ((h i j hj).2 (x i) (hx i) (x j) (hx j)).1 (Ne.symm hne)
  have hstrict : ∏ i, ∏ j ∈ univ.erase i, lo i j <
      ∏ i, ∏ j ∈ univ.erase i, I.W i j (x i) (x j) := by
    apply Finset.prod_lt_prod
    · intro i' _
      exact Finset.prod_pos (hlopos i')
    · intro i' _
      exact Finset.prod_le_prod (fun j' hj' => (hlopos i' j' hj').le)
        (fun j' hj' => ((h i' j' hj').2 _ (hx i') _ (hx j')).1)
    · exact ⟨i, mem_univ i, Finset.prod_lt_prod (hlopos i)
        (fun j' hj' => ((h i j' hj').2 _ (hx i) _ (hx j')).1) ⟨j, hj, hlt⟩⟩
  exact hstrict.ne hL

/-- On a rigid instance with positive factors, a leaf whose lower endpoint is exact covers at
most one configuration. -/
theorem zleaf_exact_card {I : WInstance n k} (hI : I.Pos) (hR : I.Rigid) (D : Dom n k)
    (lo hi : Fin n → Fin n → ℚ) (h : LeafZOK I D lo hi)
    (hex : (∏ i, ∑ a ∈ (D i).toFinset, I.w i a) * ∏ i, ∏ j ∈ univ.erase i, lo i j = I.Z D) :
    (boxFinset D).card ≤ 1 := by
  rw [Finset.card_le_one]
  intro x hx y hy
  rw [mem_boxFinset] at hx hy
  funext i
  by_contra hne
  obtain ⟨j, hji, hsep⟩ := hR i
  have hx' : InBox D (Function.update x i (y i)) := by
    intro l
    by_cases hl : l = i
    · subst hl
      rw [Function.update_self]
      exact hy l
    · rw [Function.update_of_ne hl]
      exact hx l
  have hj : j ∈ univ.erase i := Finset.mem_erase.mpr ⟨hji, mem_univ j⟩
  have hi' : i ∈ univ.erase j := Finset.mem_erase.mpr ⟨fun e => hji e.symm, mem_univ i⟩
  have e1 := zleaf_exact_const hI D lo hi h hex x hx i j hj
  have e2 := zleaf_exact_const hI D lo hi h hex _ hx' i j hj
  have e3 := zleaf_exact_const hI D lo hi h hex x hx j i hi'
  have e4 := zleaf_exact_const hI D lo hi h hex _ hx' j i hi'
  rw [Function.update_self, Function.update_of_ne hji] at e2 e4
  rcases hsep (x i) (y i) (x j) hne with h1 | h2
  · exact h1 (e1.trans e2.symm)
  · exact h2 (e3.trans e4.symm)

/-- Interval accumulation with an exact lower endpoint: if every summand interval has a valid
lower endpoint and the accumulated lower endpoint is the exact sum, every summand is exact. -/
theorem foldr_addIv_exact (val : Fin k → ℚ) (iv : Fin k → Option (ℚ × ℚ))
    (hiv : ∀ a l h, iv a = some (l, h) → l ≤ val a) :
    ∀ (l : List (Fin k)), l.Nodup → ∀ L H,
      l.foldr (fun a acc => addIv (iv a) acc) (some (0, 0)) = some (L, H) →
        L ≤ ∑ a ∈ l.toFinset, val a ∧
          (L = ∑ a ∈ l.toFinset, val a → ∀ a ∈ l, ∃ h, iv a = some (val a, h)) := by
  intro l
  induction l with
  | nil =>
    intro _ L H h
    simp only [List.foldr_nil, Option.some.injEq, Prod.mk.injEq] at h
    obtain ⟨rfl, rfl⟩ := h
    simp
  | cons a l ih =>
    intro hnd L H h
    rw [List.nodup_cons] at hnd
    simp only [List.foldr_cons] at h
    cases hia : iv a with
    | none => rw [hia] at h; simp [addIv] at h
    | some lh =>
      obtain ⟨l₁, h₁⟩ := lh
      cases hacc : l.foldr (fun a acc => addIv (iv a) acc) (some (0, 0)) with
      | none => rw [hia, hacc] at h; simp [addIv] at h
      | some LH =>
        obtain ⟨L₂, H₂⟩ := LH
        rw [hia, hacc] at h
        simp only [addIv, Option.some.injEq, Prod.mk.injEq] at h
        obtain ⟨rfl, rfl⟩ := h
        have h1 := hiv a l₁ h₁ hia
        have h2 := ih hnd.2 L₂ H₂ hacc
        have hnot : a ∉ l.toFinset := fun hmem => hnd.1 (List.mem_toFinset.mp hmem)
        rw [List.toFinset_cons, Finset.sum_insert hnot]
        refine ⟨by linarith [h2.1], fun hex b hb => ?_⟩
        have hl₁ : l₁ = val a := by linarith [h2.1]
        have hL₂ : L₂ = ∑ a ∈ l.toFinset, val a := by linarith [h2.1]
        rcases List.mem_cons.mp hb with rfl | hb'
        · exact ⟨h₁, by rw [hia, hl₁]⟩
        · exact h2.2 hL₂ b hb'

/-- The number of configurations of a box is additive over the states of a site. -/
theorem card_boxFinset_branch (D : Dom n k) (i : Fin n) :
    (boxFinset D).card = ∑ a ∈ (D i).toFinset, (boxFinset (D.fix i a)).card := by
  have h := WInstance.Z_branch ⟨fun _ _ => 1, fun _ _ _ _ => 1⟩ D i
  simp only [WInstance.Z, WInstance.weight, Finset.prod_const_one, mul_one, Finset.sum_const,
    nsmul_eq_mul] at h
  exact_mod_cast h

/-- The full box has `k ^ n` configurations. -/
theorem card_boxFinset_fullDom (n k : ℕ) : (boxFinset (fullDom n k)).card = k ^ n := by
  unfold boxFinset fullDom
  simp

/-- Branch step of the leaf count: if the accumulated lower endpoint of a branch node is exact,
every visited child is exact, and the boxes of the children partition the box. -/
theorem branch_exact_card (I : WInstance n k) (D : Dom n k) (i : Fin n)
    (iv : Fin k → Option (ℚ × ℚ)) (cnt : Fin k → ℕ)
    (hsound : ∀ a l h, iv a = some (l, h) → l ≤ I.Z (D.fix i a))
    (hcnt : ∀ a h, iv a = some (I.Z (D.fix i a), h) → (boxFinset (D.fix i a)).card ≤ cnt a)
    {hi : ℚ}
    (hv : (D i).dedup.foldr (fun a acc => addIv (iv a) acc) (some (0, 0)) = some (I.Z D, hi)) :
    (boxFinset D).card ≤ ∑ a, cnt a := by
  have key := foldr_addIv_exact (fun a => I.Z (D.fix i a)) iv hsound (D i).dedup
    (List.nodup_dedup _) (I.Z D) hi hv
  have hded : (D i).dedup.toFinset = (D i).toFinset := by
    ext a
    simp
  rw [hded] at key
  have hch : ∀ a ∈ (D i).toFinset, (boxFinset (D.fix i a)).card ≤ cnt a := by
    intro a ha
    obtain ⟨h', hval⟩ := key.2 (I.Z_branch D i) a (by simpa using ha)
    exact hcnt a h' hval
  calc (boxFinset D).card = ∑ a ∈ (D i).toFinset, (boxFinset (D.fix i a)).card :=
        card_boxFinset_branch D i
    _ ≤ ∑ a ∈ (D i).toFinset, cnt a := Finset.sum_le_sum hch
    _ ≤ ∑ a, cnt a := Finset.sum_le_sum_of_subset (Finset.subset_univ _)

/-- **Exact certificates of `zverify` enumerate the box.**  On a rigid instance with positive
factors, a certificate of `zverify` whose lower endpoint is the exact partition sum has at least
as many leaves as the box has configurations. -/
theorem zverify_exact_leaves {I : WInstance n k} (hI : I.Pos) (hR : I.Rigid) (c : ZCert n k)
    (D : Dom n k) (hi : ℚ) (hv : zverify c I D = some (I.Z D, hi)) :
    (boxFinset D).card ≤ c.leaves := by
  induction c generalizing D hi with
  | leaf l h =>
    unfold zverify at hv
    split_ifs at hv with hok
    simp only [Option.some.injEq, Prod.mk.injEq] at hv
    exact zleaf_exact_card hI hR D l h hok hv.1
  | branch i ch ih =>
    unfold zverify at hv
    exact branch_exact_card I D i (fun a => zverify (ch a) I (D.fix i a))
      (fun a => (ch a).leaves)
      (fun a l h hval => (zverify_sound hI.nonneg (ch a) (D.fix i a) l h hval).1)
      (fun a h' hval => ih a (D.fix i a) h' hval) hv
  | prune i r t q₀ q rest ih =>
    unfold zverify at hv
    split_ifs at hv with hok
    cases hrest : zverify rest I (D.remove i r) with
    | none => rw [hrest] at hv; simp at hv
    | some lh =>
      obtain ⟨l', h'⟩ := lh
      rw [hrest] at hv
      simp only [Option.map_some, Option.some.injEq, Prod.mk.injEq] at hv
      obtain ⟨hl', _⟩ := hv
      have h1 := (zverify_sound hI.nonneg rest (D.remove i r) l' h' hrest).1
      have h2 := (zprune_sound hI.nonneg D i r t q₀ q hok).1
      have hZ : l' = I.Z (D.remove i r) := le_antisymm h1 (by rw [hl']; exact h2)
      have hbox : boxFinset (D.remove i r) = boxFinset D := by
        rw [boxFinset_remove]
        apply Finset.filter_true_of_mem
        intro x hx hxr
        have hlt : I.Z (D.remove i r) < I.Z D := by
          unfold WInstance.Z
          rw [boxFinset_remove]
          exact Finset.sum_lt_sum_of_subset (Finset.filter_subset _ _) hx
            (by simp [hxr]) (I.weight_pos hI x) (fun y _ _ => (I.weight_pos hI y).le)
        rw [← hZ, hl'] at hlt
        exact lt_irrefl _ hlt
      rw [hZ] at hrest
      rw [← hbox]
      exact ih (D.remove i r) h' hrest

/-- **Without cut and elimination, exact certificates enumerate the box.**  On a rigid instance
with positive factors, an elementary certificate whose lower endpoint is the exact partition sum
has at least as many leaves as the box has configurations. -/
theorem zverify2_elementary_exact_leaves {I : WInstance n k} (hI : I.Pos) (hR : I.Rigid)
    (c : ZCert2 n k) (hc : c.Elementary) (D : Dom n k) (hi : ℚ)
    (hv : zverify2 c I D = some (I.Z D, hi)) : (boxFinset D).card ≤ c.leaves := by
  induction c generalizing D hi with
  | base c => exact zverify_exact_leaves hI hR c D hi hv
  | branch i ch ih =>
    unfold zverify2 at hv
    exact branch_exact_card I D i (fun a => zverify2 (ch a) I (D.fix i a))
      (fun a => (ch a).leaves)
      (fun a l h hval => (zverify2_sound hI.nonneg (ch a) (D.fix i a) l h hval).1)
      (fun a h' hval => ih a (hc a) (D.fix i a) h' hval) hv
  | cut S p l h c₁ c₂ _ _ => exact absurd hc (by simp [ZCert2.Elementary])
  | elim1 i j p rest _ => exact absurd hc (by simp [ZCert2.Elementary])
  | elim2 i j l p rest _ => exact absurd hc (by simp [ZCert2.Elementary])

/-- On the full box such a certificate has at least `k ^ n` leaves. -/
theorem zverify2_elementary_exact_leaves_fullDom {I : WInstance n k} (hI : I.Pos)
    (hR : I.Rigid) (c : ZCert2 n k) (hc : c.Elementary) (hi : ℚ)
    (hv : zverify2 c I (fullDom n k) = some (I.Z (fullDom n k), hi)) : k ^ n ≤ c.leaves := by
  have h := zverify2_elementary_exact_leaves hI hR c hc (fullDom n k) hi hv
  rwa [card_boxFinset_fullDom] at h

/-- The two triangles have positive factors. -/
theorem twoTrianglesW_pos : twoTrianglesW.Pos := by decide +kernel

/-- The two triangles are rigid: the partner of a site is another site of its triangle. -/
theorem twoTrianglesW_rigid : twoTrianglesW.Rigid := by decide +kernel

/-- The cut certificate of the two triangles has `16` leaves. -/
theorem twoTrianglesCert_leaves : twoTrianglesCert.leaves = 16 := by decide +kernel

/-- The branch-then-cut certificate of the coupled triangles has `32` leaves. -/
theorem coupledTrianglesExactCert_leaves : coupledTrianglesExactCert.leaves = 32 := by
  decide +kernel

/-- Every elementary certificate whose lower endpoint is the exact partition sum `169/16` of the
two triangles has at least `64` leaves. -/
theorem twoTriangles_elementary_leaves (c : ZCert2 6 2) (hc : c.Elementary) (hi : ℚ)
    (hv : zverify2 c twoTrianglesW (fullDom 6 2) = some (169 / 16, hi)) : 64 ≤ c.leaves := by
  rw [← twoTriangles_Z] at hv
  exact zverify2_elementary_exact_leaves_fullDom twoTrianglesW_pos twoTrianglesW_rigid c hc hi
    hv

/-- Full enumeration of the two triangles (branch and leaf only): `64` leaves. -/
def twoTrianglesEnum : ZCert 6 2 :=
  .branch 0 fun a => .branch 1 fun b => .branch 2 fun c => .branch 3 fun d =>
    .branch 4 fun e => .branch 5 fun f => pointZLeaf twoTrianglesW ![a, b, c, d, e, f]

/-- The bound `64` is attained: full enumeration is elementary, has `64` leaves and is exact. -/
theorem twoTriangles_enum_exact :
    (ZCert2.base twoTrianglesEnum).Elementary ∧ (ZCert2.base twoTrianglesEnum).leaves = 64 ∧
      zverify2Top (.base twoTrianglesEnum) twoTrianglesW (fullDom 6 2) =
        some (169 / 16, 169 / 16) := by
  refine ⟨trivial, ?_, ?_⟩ <;> decide +kernel

/-- **Separation of the cut rule.**  On the two disjoint triangles the cut certificate with `16`
leaves is exact, whereas every elementary certificate that the top-level kernel accepts with the
exact lower endpoint has at least `64` leaves. -/
theorem cut_rule_separation :
    (twoTrianglesCert.leaves = 16 ∧
      zverify2Top twoTrianglesCert twoTrianglesW (fullDom 6 2) = some (169 / 16, 169 / 16)) ∧
      ∀ c : ZCert2 6 2, c.Elementary → ∀ hi : ℚ,
        zverify2Top c twoTrianglesW (fullDom 6 2) = some (169 / 16, hi) → 64 ≤ c.leaves :=
  ⟨⟨twoTrianglesCert_leaves, twoTriangles_cut_exact⟩, fun c hc hi hv =>
    twoTriangles_elementary_leaves c hc hi (zverify2Top_eq_some hv).2⟩

/-- The six-site chain has positive factors. -/
theorem chainW_pos : chainW.Pos := by decide +kernel

/-- The six-site chain is rigid: the partner of a site is a neighbour on the chain. -/
theorem chainW_rigid : chainW.Rigid := by decide +kernel

/-- The elimination certificate of the six-site chain has one leaf. -/
theorem chainCert6_leaves : chainCert6.leaves = 1 := by decide +kernel

/-- Every elementary certificate whose lower endpoint is the exact partition sum `243/16` of the
six-site chain has at least `64` leaves. -/
theorem chain_elementary_leaves (c : ZCert2 6 2) (hc : c.Elementary) (hi : ℚ)
    (hv : zverify2 c chainW (fullDom 6 2) = some (243 / 16, hi)) : 64 ≤ c.leaves := by
  rw [← chain_Z] at hv
  exact zverify2_elementary_exact_leaves_fullDom chainW_pos chainW_rigid c hc hi hv

/-- **Separation of the elimination rule.**  The six-site chain has positive factors and is
rigid; its elimination certificate has one leaf and is exact, whereas every elementary
certificate that the top-level kernel accepts with the exact lower endpoint has at least `64`
leaves. -/
theorem elimination_separation :
    (chainW.Pos ∧ chainW.Rigid) ∧
      (chainCert6.leaves = 1 ∧
        zverify2Top chainCert6 chainW (fullDom 6 2) = some (243 / 16, 243 / 16)) ∧
      ∀ c : ZCert2 6 2, c.Elementary → ∀ hi : ℚ,
        zverify2Top c chainW (fullDom 6 2) = some (243 / 16, hi) → 64 ≤ c.leaves :=
  ⟨⟨chainW_pos, chainW_rigid⟩, ⟨chainCert6_leaves, chain_elim_exact⟩, fun c hc hi hv =>
    chain_elementary_leaves c hc hi (zverify2Top_eq_some hv).2⟩

/-- The ring certificate has one leaf, whereas every elementary certificate whose lower endpoint
is the exact partition sum `61/8` of the ring has at least `32` leaves. -/
theorem ring_elementary_leaves :
    ringCert.leaves = 1 ∧ ∀ c : ZCert2 5 2, c.Elementary → ∀ hi : ℚ,
      zverify2 c ringW (fullDom 5 2) = some (61 / 8, hi) → 32 ≤ c.leaves := by
  refine ⟨by decide +kernel, fun c hc hi hv => ?_⟩
  rw [← ring_Z] at hv
  exact zverify2_elementary_exact_leaves_fullDom (by decide +kernel) (by decide +kernel) c hc hi
    hv

/-! ### Nested cuts: three subsystems

A cut node may sit below another cut node.  Here the second half of the outer cut is cut again;
at that point the instance is already restricted and the box already pinned on the first
subsystem.  The leaves add up, whereas for elementary certificates the sizes of the state spaces
multiply. -/

/-- Three independent pairs `{0, 1}`, `{2, 3}`, `{4, 5}` of binary sites: pair factor `1/2` for
equal states inside a pair, `1` otherwise. -/
def threePairsW : WInstance 6 2 where
  w := fun _ _ => 1
  W := fun i j a b => if i < j ∧ i.val / 2 = j.val / 2 ∧ a = b then 1 / 2 else 1

/-- Nested cuts `{0, 1} | {2, 3} | {4, 5}`, each pair enumerated: `4 + 4 + 4 = 12` leaves. -/
def threePairsCert : ZCert2 6 2 :=
  .cut {0, 1} (fun _ => 0) (fun _ _ => 1) (fun _ _ => 1)
    (.base (.branch 0 fun a => .branch 1 fun b =>
      pointZLeaf (threePairsW.restrict {0, 1}) ![a, b, 0, 0, 0, 0]))
    (.cut {2, 3} (fun _ => 0) (fun _ _ => 1) (fun _ _ => 1)
      (.base (.branch 2 fun a => .branch 3 fun b =>
        pointZLeaf ((threePairsW.restrict {0, 1}ᶜ).restrict {2, 3}) ![0, 0, a, b, 0, 0]))
      (.base (.branch 4 fun a => .branch 5 fun b =>
        pointZLeaf ((threePairsW.restrict {0, 1}ᶜ).restrict {2, 3}ᶜ) ![0, 0, 0, 0, a, b])))

/-- **Nested cuts.**  The kernel computes the exact partition sum `3³ = 27` of the three pairs
from a certificate with `12` leaves. -/
theorem threePairs_nested_cut_exact :
    zverify2Top threePairsCert threePairsW (fullDom 6 2) = some (27, 27) ∧
      threePairsCert.leaves = 12 := by
  constructor <;> decide +kernel

/-- An elementary certificate of the three pairs with the exact lower endpoint `27` has at least
`64` leaves. -/
theorem threePairs_elementary_leaves (c : ZCert2 6 2) (hc : c.Elementary) (hi : ℚ)
    (hv : zverify2 c threePairsW (fullDom 6 2) = some (27, hi)) : 64 ≤ c.leaves := by
  have hs := zverify2Top_sound _ _ _ _ _ threePairs_nested_cut_exact.1
  have hZ : threePairsW.Z (fullDom 6 2) = 27 := le_antisymm hs.2 hs.1
  rw [← hZ] at hv
  exact zverify2_elementary_exact_leaves_fullDom (by decide +kernel) (by decide +kernel) c hc hi
    hv

/-! ### Chains of any length

An instance is chain-structured if its pair factors are `1` except between consecutive sites.
For such an instance on `m + 1` sites the transfer-matrix certificate `chainCert m p` — eliminate
site `0` into site `1`, then `1` into `2`, …, then one leaf — is accepted with the exact
partition sum, for every number of states `k ≥ 1` (a pin `p : Fin k` is needed) and without any
sign condition.  Together with the lower bound for elementary certificates this separates the
elimination rule on chains of every length. -/

/-- A leaf with the pair bounds `[1, 1]` is exact when it is accepted, i.e. when all pair
factors are `1` on the box (an identity: no sign condition on the factors). -/
theorem zverify_unitZLeaf {I : WInstance n k} {D : Dom n k}
    (h : LeafZOK I D (fun _ _ => 1) (fun _ _ => 1)) :
    zverify unitZLeaf I D = some (I.Z D, I.Z D) := by
  have hZ : I.Z D = ∏ i, ∑ a ∈ (D i).toFinset, I.w i a := by
    have hprod : (∏ i, ∑ a ∈ (D i).toFinset, I.w i a) =
        ∑ x ∈ boxFinset D, ∏ i, I.w i (x i) := by
      unfold boxFinset
      exact Finset.prod_univ_sum (fun i => (D i).toFinset) (fun i a => I.w i a)
    rw [hprod]
    unfold WInstance.Z WInstance.weight
    apply Finset.sum_congr rfl
    intro x hx
    have hxD := mem_boxFinset.mp hx
    have hone : ∏ i, ∏ j ∈ univ.erase i, I.W i j (x i) (x j) = 1 := by
      apply Finset.prod_eq_one
      intro i _
      apply Finset.prod_eq_one
      intro j hj
      have hb := (h i j hj).2 (x i) (hxD i) (x j) (hxD j)
      exact le_antisymm hb.2 hb.1
    rw [hone, mul_one]
  unfold unitZLeaf zverify
  rw [if_pos h, hZ]
  simp

/-- Chain structure from site `s` on: on the current domains every pair factor is `1`, except
possibly between consecutive sites that both have index at least `s`. -/
def ChainFrom (I : WInstance n k) (D : Dom n k) (s : ℕ) : Prop :=
  ∀ m m' : Fin n, m ≠ m' →
    (m.val + 1 ≠ m'.val ∧ m'.val + 1 ≠ m.val) ∨ m.val < s ∨ m'.val < s →
      ∀ a ∈ D m, ∀ b ∈ D m', I.W m m' a b = 1

/-- Chain structure only depends on the value of the index. -/
theorem ChainFrom.of_eq {I : WInstance n k} {D : Dom n k} {s s' : ℕ} (h : ChainFrom I D s)
    (e : s = s') : ChainFrom I D s' := e ▸ h

/-- In a chain from `s` on, site `s` may be eliminated into site `s + 1`. -/
theorem ChainFrom.elim1OK {I : WInstance n k} {D : Dom n k} {s : ℕ} (h : ChainFrom I D s)
    (hs : s + 1 < n) : Elim1OK I D ⟨s, by omega⟩ ⟨s + 1, hs⟩ := by
  refine ⟨fun e => ?_, fun m hmi hmj a ha b hb => ?_⟩
  · have e' := congrArg Fin.val e
    simp at e'
  · have h1 : m.val ≠ s := fun e => hmi (Fin.ext e)
    have h2 : m.val ≠ s + 1 := fun e => hmj (Fin.ext e)
    have hc1 : (s + 1 ≠ m.val ∧ m.val + 1 ≠ s) ∨ s < s ∨ m.val < s := by omega
    have hc2 : (m.val + 1 ≠ s ∧ s + 1 ≠ m.val) ∨ m.val < s ∨ s < s := by omega
    exact ⟨h _ m (Ne.symm hmi) hc1 a ha b hb, h m _ hmi hc2 b hb a ha⟩

/-- Eliminating site `s` of a chain from `s` on leaves a chain from `s + 1` on. -/
theorem ChainFrom.elim1 {I : WInstance n k} {D : Dom n k} {s : ℕ} (h : ChainFrom I D s)
    (hs : s + 1 < n) (p : Fin k) :
    ChainFrom (I.elim1 D ⟨s, by omega⟩ ⟨s + 1, hs⟩) (D.fix ⟨s, by omega⟩ p) (s + 1) := by
  intro m m' hmm hcond a ha b hb
  rw [I.elim1_W]
  split_ifs with hi
  · rfl
  · have hmi : m ≠ ⟨s, by omega⟩ := fun e => hi (Or.inl e)
    have hmi' : m' ≠ ⟨s, by omega⟩ := fun e => hi (Or.inr e)
    have h1 : m.val ≠ s := fun e => hmi (Fin.ext e)
    have h2 : m'.val ≠ s := fun e => hmi' (Fin.ext e)
    unfold Dom.fix at ha hb
    rw [Function.update_of_ne hmi] at ha
    rw [Function.update_of_ne hmi'] at hb
    exact h m m' hmm (by omega) a ha b hb

/-- A chain from its last site on has no non-trivial pair factor: the unit leaf is accepted. -/
theorem ChainFrom.leafOK {I : WInstance n k} {D : Dom n k} {s : ℕ} (h : ChainFrom I D s)
    (hs : n ≤ s + 1) : LeafZOK I D (fun _ _ => 1) (fun _ _ => 1) := by
  unfold LeafZOK
  intro i j hj
  refine ⟨zero_le_one, fun a ha b hb => ?_⟩
  have hij : i ≠ j := (Finset.ne_of_mem_erase hj).symm
  have hne : i.val ≠ j.val := fun e => hij (Fin.ext e)
  have hi := i.isLt
  have hjlt := j.isLt
  rw [h i j hij (by omega) a ha b hb]
  exact ⟨le_refl 1, le_refl 1⟩

/-- The transfer-matrix certificate with `t` eliminations left: eliminate the sites
`m - t, …, m - 1` in turn, each into its right neighbour, then one unit leaf. -/
def chainCertAux (m : ℕ) (p : Fin k) : (t : ℕ) → t ≤ m → ZCert2 (m + 1) k
  | 0, _ => .base unitZLeaf
  | t + 1, h =>
      .elim1 ⟨m - (t + 1), by omega⟩ ⟨m - (t + 1) + 1, by omega⟩ p
        (chainCertAux m p t (by omega))

/-- **The transfer-matrix certificate of a chain of `m + 1` sites**: eliminate site `0` into
site `1`, then `1` into `2`, …, `m - 1` into `m` (`m` nodes `elim1`), then one unit leaf.  The
pin `p` is the state to which the eliminated sites are fixed. -/
def chainCert (m : ℕ) (p : Fin k) : ZCert2 (m + 1) k := chainCertAux m p m le_rfl

/-- The chain certificate with `t` eliminations left has one leaf. -/
theorem chainCertAux_leaves (m : ℕ) (p : Fin k) :
    ∀ (t : ℕ) (ht : t ≤ m), (chainCertAux m p t ht).leaves = 1 := by
  intro t
  induction t with
  | zero =>
    intro _
    rfl
  | succ t ih =>
    intro ht
    rw [chainCertAux, ZCert2.leaves]
    exact ih (by omega)

/-- The transfer-matrix certificate has exactly one leaf. -/
theorem chainCert_leaves (m : ℕ) (p : Fin k) : (chainCert m p).leaves = 1 :=
  chainCertAux_leaves m p m le_rfl

/-- The chain certificate with `t` eliminations left has `t` elimination nodes. -/
theorem chainCertAux_elims (m : ℕ) (p : Fin k) :
    ∀ (t : ℕ) (ht : t ≤ m), (chainCertAux m p t ht).elims = t := by
  intro t
  induction t with
  | zero =>
    intro _
    rfl
  | succ t ih =>
    intro ht
    rw [chainCertAux, ZCert2.elims, ih (by omega)]

/-- The transfer-matrix certificate of a chain of `m + 1` sites has exactly `m` elimination
nodes. -/
theorem chainCert_elims (m : ℕ) (p : Fin k) : (chainCert m p).elims = m :=
  chainCertAux_elims m p m le_rfl

/-- On a chain from site `m - t` on, the chain certificate with `t` eliminations left is
accepted with the exact partition sum. -/
theorem zverify2_chainCertAux (m : ℕ) (p : Fin k) :
    ∀ (t : ℕ) (ht : t ≤ m) (I : WInstance (m + 1) k) (D : Dom (m + 1) k),
      ChainFrom I D (m - t) → zverify2 (chainCertAux m p t ht) I D = some (I.Z D, I.Z D) := by
  intro t
  induction t with
  | zero =>
    intro ht I D h
    rw [chainCertAux, zverify2]
    exact zverify_unitZLeaf (h.leafOK (by omega))
  | succ t ih =>
    intro ht I D h
    have hs : m - (t + 1) + 1 < m + 1 := by omega
    have hok := h.elim1OK hs
    have hnext := (h.elim1 hs p).of_eq (show m - (t + 1) + 1 = m - t by omega)
    rw [chainCertAux, zverify2, if_pos hok, ih (by omega) _ _ hnext, ← I.Z_elim1 D _ _ p hok]

/-- **Chains of every length are certified exactly by elimination.**  Let the pair factors of
an instance on `m + 1` sites be identically `1` except between consecutive sites.  Then the
kernel accepts the transfer-matrix certificate (`m` eliminations, one leaf) on the full box and
returns the exact partition sum as both endpoints.  No sign condition is needed. -/
theorem zverify2_chainCert (m : ℕ) (p : Fin k) (I : WInstance (m + 1) k)
    (hI : ∀ i j : Fin (m + 1), i ≠ j → i.val + 1 ≠ j.val → j.val + 1 ≠ i.val →
      ∀ a b, I.W i j a b = 1) :
    zverify2 (chainCert m p) I (fullDom (m + 1) k) =
      some (I.Z (fullDom (m + 1) k), I.Z (fullDom (m + 1) k)) := by
  apply zverify2_chainCertAux m p m le_rfl I (fullDom (m + 1) k)
  intro i j hij hcond a _ b _
  rcases hcond with h | h | h
  · exact hI i j hij h.1 h.2 a b
  · omega
  · omega

/-- The same for the top-level kernel, for chain-structured instances with nonnegative
factors. -/
theorem zverify2Top_chainCert (m : ℕ) (p : Fin k) (I : WInstance (m + 1) k) (hnn : I.Nonneg)
    (hI : ∀ i j : Fin (m + 1), i ≠ j → i.val + 1 ≠ j.val → j.val + 1 ≠ i.val →
      ∀ a b, I.W i j a b = 1) :
    zverify2Top (chainCert m p) I (fullDom (m + 1) k) =
      some (I.Z (fullDom (m + 1) k), I.Z (fullDom (m + 1) k)) := by
  unfold zverify2Top
  rw [if_pos hnn]
  exact zverify2_chainCert m p I hI

/-- The explicit certificate of the six-site chain is the transfer-matrix certificate. -/
theorem chainCert6_eq : chainCert6 = chainCert 5 0 := rfl

/-- **Separation of the elimination rule on chains of every length.**  On `m + 1` sites, let a
chain-structured instance have positive factors and be rigid.  Then the transfer-matrix
certificate has `m` elimination nodes and one leaf, and the top-level kernel accepts it with the
exact partition sum, whereas every elementary certificate that the top-level kernel accepts with
the exact lower endpoint has at least `k ^ (m + 1)` leaves. -/
theorem chain_separation (m : ℕ) (p : Fin k) (I : WInstance (m + 1) k) (hpos : I.Pos)
    (hrig : I.Rigid)
    (hI : ∀ i j : Fin (m + 1), i ≠ j → i.val + 1 ≠ j.val → j.val + 1 ≠ i.val →
      ∀ a b, I.W i j a b = 1) :
    ((chainCert m p).elims = m ∧ (chainCert m p).leaves = 1 ∧
      zverify2Top (chainCert m p) I (fullDom (m + 1) k) =
        some (I.Z (fullDom (m + 1) k), I.Z (fullDom (m + 1) k))) ∧
      ∀ c : ZCert2 (m + 1) k, c.Elementary → ∀ hi : ℚ,
        zverify2Top c I (fullDom (m + 1) k) = some (I.Z (fullDom (m + 1) k), hi) →
          k ^ (m + 1) ≤ c.leaves :=
  ⟨⟨chainCert_elims m p, chainCert_leaves m p, zverify2Top_chainCert m p I hpos.nonneg hI⟩,
    fun c hc hi hv =>
      zverify2_elementary_exact_leaves_fullDom hpos hrig c hc hi (zverify2Top_eq_some hv).2⟩

/-- Ferromagnetic two-state chain on `m + 1` sites: pair factor `1/2` for unequal states on the
ordered pairs `(i, i + 1)`, `1` otherwise (`chainW` is the case `m = 5`). -/
def ferroChainW (m : ℕ) : WInstance (m + 1) 2 where
  w := fun _ _ => 1
  W := fun i j a b => if j.val = i.val + 1 ∧ a ≠ b then 1 / 2 else 1

/-- The six-site chain of the kernel run is the ferromagnetic chain with `m = 5`. -/
theorem chainW_eq : chainW = ferroChainW 5 := rfl

/-- The ferromagnetic chain has positive factors. -/
theorem ferroChainW_pos (m : ℕ) : (ferroChainW m).Pos := by
  constructor
  · intro i a
    exact zero_lt_one
  · intro i j a b
    unfold ferroChainW
    dsimp only
    split_ifs <;> norm_num

/-- On a bond of the ferromagnetic chain, two different states of one end are told apart by the
pair factor, whatever the state of the other end. -/
theorem ferroChainW_bond (m : ℕ) {i j : Fin (m + 1)} (hij : j.val = i.val + 1) :
    (∀ a a' b : Fin 2, a ≠ a' → (ferroChainW m).W i j a b ≠ (ferroChainW m).W i j a' b) ∧
      ∀ a a' b : Fin 2, a ≠ a' → (ferroChainW m).W i j b a ≠ (ferroChainW m).W i j b a' := by
  have key : ∀ a a' b : Fin 2, a ≠ a' → (a ≠ b ↔ ¬ a' ≠ b) := by decide
  have key' : ∀ a a' b : Fin 2, a ≠ a' → (b ≠ a ↔ ¬ b ≠ a') := by decide
  constructor
  · intro a a' b haa
    unfold ferroChainW
    dsimp only
    by_cases hab : a ≠ b
    · rw [if_pos ⟨hij, hab⟩, if_neg fun e => (key a a' b haa).mp hab e.2]
      norm_num
    · rw [if_neg fun e => hab e.2, if_pos ⟨hij, by_contra fun e => hab ((key a a' b haa).mpr e)⟩]
      norm_num
  · intro a a' b haa
    unfold ferroChainW
    dsimp only
    by_cases hab : b ≠ a
    · rw [if_pos ⟨hij, hab⟩, if_neg fun e => (key' a a' b haa).mp hab e.2]
      norm_num
    · rw [if_neg fun e => hab e.2, if_pos ⟨hij, by_contra fun e => hab ((key' a a' b haa).mpr e)⟩]
      norm_num

/-- The ferromagnetic chain on at least two sites is rigid: the partner of a site is its right
neighbour, and for the last site its left neighbour. -/
theorem ferroChainW_rigid (m : ℕ) (hm : 1 ≤ m) : (ferroChainW m).Rigid := by
  intro i
  by_cases hi : i.val < m
  · have hij : (⟨i.val + 1, by omega⟩ : Fin (m + 1)).val = i.val + 1 := rfl
    refine ⟨⟨i.val + 1, by omega⟩, fun e => ?_, fun a a' b haa => ?_⟩
    · have e' := congrArg Fin.val e
      simp at e'
    · exact Or.inl ((ferroChainW_bond m hij).1 a a' b haa)
  · have hlast : i.val = m := by have := i.isLt; omega
    have hij : i.val = (⟨m - 1, by omega⟩ : Fin (m + 1)).val + 1 := by
      show i.val = m - 1 + 1
      omega
    refine ⟨⟨m - 1, by omega⟩, fun e => ?_, fun a a' b haa => ?_⟩
    · have e' := congrArg Fin.val e
      simp only [] at e'
      omega
    · exact Or.inr ((ferroChainW_bond m hij).2 a a' b haa)

/-- **Exponential separation on a connected family.**  For the ferromagnetic two-state chain on
`n = m + 1 ≥ 2` sites, `n - 1` eliminations and one leaf give the exact partition sum, whereas
every elementary certificate that the top-level kernel accepts with the exact lower endpoint has
at least `2 ^ n` leaves. -/
theorem ferroChain_separation (m : ℕ) (hm : 1 ≤ m) :
    ((chainCert m (0 : Fin 2)).elims = m ∧ (chainCert m (0 : Fin 2)).leaves = 1 ∧
      zverify2Top (chainCert m 0) (ferroChainW m) (fullDom (m + 1) 2) =
        some ((ferroChainW m).Z (fullDom (m + 1) 2), (ferroChainW m).Z (fullDom (m + 1) 2))) ∧
      ∀ c : ZCert2 (m + 1) 2, c.Elementary → ∀ hi : ℚ,
        zverify2Top c (ferroChainW m) (fullDom (m + 1) 2) =
          some ((ferroChainW m).Z (fullDom (m + 1) 2), hi) → 2 ^ (m + 1) ≤ c.leaves :=
  chain_separation m 0 (ferroChainW m) (ferroChainW_pos m) (ferroChainW_rigid m hm)
    (fun i j _ h1 _ a b => by
      unfold ferroChainW
      dsimp only
      rw [if_neg fun e => h1 e.1.symm])

end MetricChain
