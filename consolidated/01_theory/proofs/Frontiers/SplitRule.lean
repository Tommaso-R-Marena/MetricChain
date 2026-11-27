import Mathlib
import proofs.CertificateAlgebra

/-!
# A domain-split rule as a layer over the verification kernel

The kernel `verify` of `proofs/CertificateAlgebra.lean` divides a box in one way only: a `branch`
node on site `i` has one child per state `a` of site `i`, checked on the box `D.fix i a`.  The
Scientific Discovery Division asked (its message SCI-RES-0014, request P7-T2) for a *domain-split*
rule: a node `split i B c₁ c₂` whose first child is checked on the box in which the list of site
`i` is filtered to the states listed in `B`, and whose second child is checked on the box in which
it is filtered to the states not listed in `B`.  The two boxes cover the box, so the rule is sound
for the same reason as `branch`.  Its use: a dual leaf accepted on a box is accepted on every
sub-box (`leafOK_mono`), so under `branch` the children of several states can only repeat one
leaf, whereas under `split` that leaf is checked once for all the states of a block — "state `a`
of site `i` | everything else" costs two leaf checks instead of one per state.

This file implements the rule as a **layer on top of the kernel**.  The kernel type `Cert`, the
checker `verify` and their theorems are not changed: a split certificate (`SCert`) is a binary
tree of `split` nodes whose leaves are certificates of the kernel, and the layered checker
`verifyS` calls `verify` on them.  A consequence of this design: a `split` node can stand above
any kernel certificate, but not below a `branch`, `prune` or `sum` node of `Cert` (that would
need the constructor inside `Cert`).

## Definitions

* `Dom.keep D i B`, `Dom.drop D i B` — the two sub-boxes of a split: the list of site `i` filtered
  to the states listed in `B`, respectively to the states not listed in `B`.  (They are the
  sub-boxes that `proofs/Frontiers/BarrierCertificate.lean` calls `Dom.restrict` and `Dom.exclude`
  for the `split` node of its cut trees; they are restated here so that this file depends on the
  kernel file only.)
* `SCert n k` — split certificates: `base c` for a kernel certificate `c`, and
  `split i B c₁ c₂`.
* `verifyS : SCert n k → PairInstance n k → Dom n k → ℚ → Bool` — the layered checker:
  `verifyS (.base c) = verify c` (`verifyS_base`) and
  `verifyS (.split i B c₁ c₂) I D L = verifyS c₁ I (D.keep i B) L && verifyS c₂ I (D.drop i B) L`
  (`verifyS_split`).
* `SCert.size` — number of nodes (the nodes of the kernel certificates, as counted by
  `Cert.size`, plus one per `split` node).

## Statements

* `Dom.mem_keep`, `Dom.mem_drop`, `inBox_keep_iff`, `inBox_drop_iff` — the two sub-boxes consist
  of the configurations of the box whose state at site `i` is, respectively is not, listed in `B`;
  `inBox_keep_or_drop` — they cover the box (`inBox_keep`, `inBox_drop` are the two halves).
* `verifyS_sound` — **soundness**: `verifyS c I D L = true → ∀ x, InBox D x → L ≤ I.energy x`.
* `verifyS_sound_real` — the same for a real pairwise model bounded below, entry by entry, by the
  rational instance (the analogue of `verify_sound_real`).
* `leafOK_mono` — a dual leaf accepted on a box is accepted on every sub-box.
* `split_leaves_imp_branch` — **a split of two leaves adds no proving power**: if it is accepted,
  so is the `branch` node whose children repeat the first leaf for the states listed in `B` and
  the second leaf for the other states.
* `branch_leaves_imp_split`, `split_leaves_iff_branch` — the converse, when each of the two blocks
  contains a state of the current list of site `i`: the two certificates are then accepted
  together.  The reason is `leafOK_iff_fix` (its non-trivial half is `leafOK_of_fix`): on a box
  whose list at site `i` is not empty, a dual leaf is accepted iff it is accepted on every box
  `D.fix i a`, `a ∈ D i`.
* `split_leaves_size`, `branch_leaves_size` — what the split saves: `3` nodes instead of `1 + k`.
* Auxiliary relations between the boxes: `Dom.keep_subset`, `Dom.drop_subset`, `Dom.fix_self`,
  `Dom.fix_of_ne`, `Dom.fix_subset`, `Dom.fix_subset_keep`, `Dom.fix_subset_drop`, `Dom.fix_keep`,
  `Dom.fix_drop`.

## A worked instance

`splitTriangle` (`n = 3`, `k = 3`) is a frustrated triangle on two classes of states (state `0`
against the states `1`, `2`).  The certificate `splitTriangleCert` divides the domain of site `0`
into the state `0` and the two other states, with one dual leaf for each part
(`splitTriangleKeepLeaf`, `splitTriangleDropLeaf`).  It is accepted for the bound `1`
(`splitTriangle_verified`), which is the minimum of the energy over the full box
(`splitTriangle_lower_bound`, `splitTriangle_optimum`).  Three controls are rejected: the bound
`2` (`splitTriangle_rejects`), the leaf of the first child alone on the full box
(`splitTriangle_keepLeaf_rejected`) and the certificate with its two children exchanged
(`splitTriangle_exchanged_rejected`).  In fact no dual leaf whatsoever is accepted on the full box
for a bound above `0` (`splitTriangle_leaf_gap`, `splitTriangle_no_leaf`).  The `branch`
certificate with the second leaf repeated is accepted as well, with three leaf checks where the
split needs two (`splitTriangle_branch_verified`).
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-! ### The two sub-boxes of a split -/

/-- The sub-box of `D` in which the list of site `i` is filtered to the states listed in `B`
(the order and the multiplicities of `D i` are kept; the other sites are unchanged). -/
def Dom.keep (D : Dom n k) (i : Fin n) (B : List (Fin k)) : Dom n k :=
  Function.update D i ((D i).filter fun s => decide (s ∈ B))

/-- The sub-box of `D` in which the list of site `i` is filtered to the states *not* listed in
`B` (the other sites are unchanged). -/
def Dom.drop (D : Dom n k) (i : Fin n) (B : List (Fin k)) : Dom n k :=
  Function.update D i ((D i).filter fun s => decide (s ∉ B))

/-- A state survives in `D.keep i B` iff it survives in `D` and, at site `i`, is listed in
`B`. -/
theorem Dom.mem_keep {D : Dom n k} {i : Fin n} {B : List (Fin k)} {j : Fin n} {a : Fin k} :
    a ∈ D.keep i B j ↔ a ∈ D j ∧ (j = i → a ∈ B) := by
  unfold Dom.keep
  by_cases hj : j = i
  · subst hj
    simp
  · simp [hj]

/-- A state survives in `D.drop i B` iff it survives in `D` and, at site `i`, is not listed in
`B`. -/
theorem Dom.mem_drop {D : Dom n k} {i : Fin n} {B : List (Fin k)} {j : Fin n} {a : Fin k} :
    a ∈ D.drop i B j ↔ a ∈ D j ∧ (j = i → a ∉ B) := by
  unfold Dom.drop
  by_cases hj : j = i
  · subst hj
    simp
  · simp [hj]

/-- `D.keep i B` is a sub-box of `D` (in the form of the hypothesis of `leafOK_mono`). -/
theorem Dom.keep_subset (D : Dom n k) (i : Fin n) (B : List (Fin k)) :
    ∀ j, ∀ a ∈ D.keep i B j, a ∈ D j := fun _ _ h => (Dom.mem_keep.mp h).1

/-- `D.drop i B` is a sub-box of `D` (in the form of the hypothesis of `leafOK_mono`). -/
theorem Dom.drop_subset (D : Dom n k) (i : Fin n) (B : List (Fin k)) :
    ∀ j, ∀ a ∈ D.drop i B j, a ∈ D j := fun _ _ h => (Dom.mem_drop.mp h).1

/-- The box of `D.keep i B` consists of the configurations of the box of `D` whose state at site
`i` is listed in `B`. -/
theorem inBox_keep_iff {D : Dom n k} {i : Fin n} {B : List (Fin k)} {x : Config n k} :
    InBox (D.keep i B) x ↔ InBox D x ∧ x i ∈ B := by
  constructor
  · intro h
    exact ⟨fun j => (Dom.mem_keep.mp (h j)).1, (Dom.mem_keep.mp (h i)).2 rfl⟩
  · rintro ⟨hx, hB⟩ j
    exact Dom.mem_keep.mpr ⟨hx j, fun hj => by rw [hj]; exact hB⟩

/-- The box of `D.drop i B` consists of the configurations of the box of `D` whose state at site
`i` is not listed in `B`. -/
theorem inBox_drop_iff {D : Dom n k} {i : Fin n} {B : List (Fin k)} {x : Config n k} :
    InBox (D.drop i B) x ↔ InBox D x ∧ x i ∉ B := by
  constructor
  · intro h
    exact ⟨fun j => (Dom.mem_drop.mp (h j)).1, (Dom.mem_drop.mp (h i)).2 rfl⟩
  · rintro ⟨hx, hB⟩ j
    exact Dom.mem_drop.mpr ⟨hx j, fun hj => by rw [hj]; exact hB⟩

/-- A configuration of `D` whose state at site `i` is listed in `B` lies in `D.keep i B`. -/
theorem inBox_keep {D : Dom n k} {x : Config n k} (hx : InBox D x) (i : Fin n) (B : List (Fin k))
    (h : x i ∈ B) : InBox (D.keep i B) x := inBox_keep_iff.mpr ⟨hx, h⟩

/-- A configuration of `D` whose state at site `i` is not listed in `B` lies in `D.drop i B`. -/
theorem inBox_drop {D : Dom n k} {x : Config n k} (hx : InBox D x) (i : Fin n) (B : List (Fin k))
    (h : x i ∉ B) : InBox (D.drop i B) x := inBox_drop_iff.mpr ⟨hx, h⟩

/-- **The two boxes of a split cover the box.**  This is the property that makes the rule
sound. -/
theorem inBox_keep_or_drop {D : Dom n k} {x : Config n k} (hx : InBox D x) (i : Fin n)
    (B : List (Fin k)) : InBox (D.keep i B) x ∨ InBox (D.drop i B) x := by
  by_cases h : x i ∈ B
  · exact Or.inl (inBox_keep hx i B h)
  · exact Or.inr (inBox_drop hx i B h)

/-! ### Split certificates and the layered checker -/

/-- **Split certificates**: a binary tree of domain splits over certificates of the kernel.  The
kernel type `Cert` is not changed; `SCert` adds the rule `split` on top of it. -/
inductive SCert (n k : ℕ) : Type
  /-- a certificate of the kernel, checked by `verify` on the current box -/
  | base (c : Cert n k) : SCert n k
  /-- domain split at site `i`: `c₁` is checked on the box in which the list of site `i` is
  filtered to the states listed in `B`, `c₂` on the box in which it is filtered to the others -/
  | split (i : Fin n) (B : List (Fin k)) (c₁ c₂ : SCert n k) : SCert n k

/-- **The layered checker.**  `verifyS c I D L = true` certifies `L ≤ min_{x ∈ ∏ D} I.energy x`
(`verifyS_sound`).  A `base` node is handed to the kernel `verify`; a `split` node checks its two
children on the two sub-boxes `D.keep i B` and `D.drop i B`. -/
def verifyS : SCert n k → PairInstance n k → Dom n k → ℚ → Bool
  | .base c, I, D, L => verify c I D L
  | .split i B c₁ c₂, I, D, L => verifyS c₁ I (D.keep i B) L && verifyS c₂ I (D.drop i B) L

/-- Number of nodes of a split certificate: the nodes of its kernel certificates (`Cert.size`)
plus one per `split` node. -/
def SCert.size : SCert n k → ℕ
  | .base c => c.size
  | .split _ _ c₁ c₂ => 1 + c₁.size + c₂.size

/-- On a kernel certificate the layered checker is the kernel. -/
theorem verifyS_base (c : Cert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ) :
    verifyS (.base c) I D L = verify c I D L := rfl

/-- The defining equation of the split rule. -/
theorem verifyS_split (i : Fin n) (B : List (Fin k)) (c₁ c₂ : SCert n k) (I : PairInstance n k)
    (D : Dom n k) (L : ℚ) :
    verifyS (.split i B c₁ c₂) I D L =
      (verifyS c₁ I (D.keep i B) L && verifyS c₂ I (D.drop i B) L) := rfl

/-- **Soundness of the layered checker.**  If `verifyS` accepts the split certificate `c` for
the instance `I`, the domains `D` and the bound `L`, then `L` is a lower bound on the energy of
every configuration of the box `∏ D`. -/
theorem verifyS_sound : ∀ (c : SCert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ),
    verifyS c I D L = true → ∀ x, InBox D x → L ≤ I.energy x := by
  intro c
  induction c with
  | base c =>
    intro I D L hv x hx
    exact verify_sound c I D L hv x hx
  | split i B c₁ c₂ ih₁ ih₂ =>
    intro I D L hv x hx
    simp only [verifyS, Bool.and_eq_true] at hv
    rcases inBox_keep_or_drop hx i B with h | h
    · exact ih₁ I (D.keep i B) L hv.1 x h
    · exact ih₂ I (D.drop i B) L hv.2 x h

/-- **Soundness for real energies.**  If the rational instance is an outward-rounded
*lower* instance of a real pairwise model (every table entry rounded down), an accepted split
certificate bounds the true real energy on the box.  The analogue of `verify_sound_real`. -/
theorem verifyS_sound_real (c : SCert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ)
    (hv : verifyS c I D L = true) (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (hh : ∀ i a, (I.h i a : ℝ) ≤ M.h i a) (hJ : ∀ i j a b, (I.J i j a b : ℝ) ≤ M.J i j a b)
    (x : Config n k) (hx : InBox D x) : (L : ℝ) ≤ M.energy x := by
  have h1 := verifyS_sound c I D L hv x hx
  have h2 := I.cast_energy_le M hh hJ x
  have h3 : (L : ℝ) ≤ ((I.energy x : ℚ) : ℝ) := by exact_mod_cast h1
  linarith

/-! ### Dual leaves on sub-boxes, and the comparison with `branch` -/

/-- **A dual leaf accepted on a box is accepted on every sub-box**: the conditions of `LeafOK`
are universally quantified over the lists of the box, and the last one does not mention the box.
With `Dom.keep_subset` and `Dom.drop_subset`: a leaf accepted on `D` is accepted on both parts of
every split of `D`. -/
theorem leafOK_mono (I : PairInstance n k) (D D' : Dom n k) (L : ℚ) (u : Fin n → ℚ)
    (p : Fin n → Fin n → ℚ) (m : Fin n → Fin n → Fin k → ℚ) (hsub : ∀ i, ∀ a ∈ D' i, a ∈ D i) :
    LeafOK I D L u p m → LeafOK I D' L u p m := by
  rintro ⟨hu, hp, hL⟩
  exact ⟨fun i a ha => hu i a (hsub i a ha),
    fun i j hj a ha b hb => hp i j hj a (hsub i a ha) b (hsub j b hb), hL⟩

/-- In the box `D.fix i a` the list of site `i` is `[a]`. -/
theorem Dom.fix_self (D : Dom n k) (i : Fin n) (a : Fin k) : D.fix i a i = [a] := by
  simp [Dom.fix]

/-- In the box `D.fix i a` the lists of the sites other than `i` are those of `D`. -/
theorem Dom.fix_of_ne (D : Dom n k) {i j : Fin n} (a : Fin k) (h : j ≠ i) :
    D.fix i a j = D j := by
  simp [Dom.fix, h]

/-- Fixing site `i` to one of its surviving states gives a sub-box. -/
theorem Dom.fix_subset {D : Dom n k} {i : Fin n} {a : Fin k} (ha : a ∈ D i) :
    ∀ j, ∀ b ∈ D.fix i a j, b ∈ D j := by
  intro j b hb
  by_cases hj : j = i
  · subst hj
    rw [Dom.fix_self, List.mem_singleton] at hb
    subst hb
    exact ha
  · rwa [D.fix_of_ne a hj] at hb

/-- Fixing site `i` to a surviving state listed in `B` gives a sub-box of `D.keep i B`. -/
theorem Dom.fix_subset_keep {D : Dom n k} {i : Fin n} {B : List (Fin k)} {a : Fin k}
    (ha : a ∈ D i) (hB : a ∈ B) : ∀ j, ∀ b ∈ D.fix i a j, b ∈ D.keep i B j := by
  intro j b hb
  by_cases hj : j = i
  · subst hj
    rw [Dom.fix_self, List.mem_singleton] at hb
    subst hb
    exact Dom.mem_keep.mpr ⟨ha, fun _ => hB⟩
  · rw [D.fix_of_ne a hj] at hb
    exact Dom.mem_keep.mpr ⟨hb, fun h => absurd h hj⟩

/-- Fixing site `i` to a surviving state not listed in `B` gives a sub-box of `D.drop i B`. -/
theorem Dom.fix_subset_drop {D : Dom n k} {i : Fin n} {B : List (Fin k)} {a : Fin k}
    (ha : a ∈ D i) (hB : a ∉ B) : ∀ j, ∀ b ∈ D.fix i a j, b ∈ D.drop i B j := by
  intro j b hb
  by_cases hj : j = i
  · subst hj
    rw [Dom.fix_self, List.mem_singleton] at hb
    subst hb
    exact Dom.mem_drop.mpr ⟨ha, fun _ => hB⟩
  · rw [D.fix_of_ne a hj] at hb
    exact Dom.mem_drop.mpr ⟨hb, fun h => absurd h hj⟩

/-- Fixing site `i` in `D.keep i B` gives the same box as fixing it in `D`. -/
theorem Dom.fix_keep (D : Dom n k) (i : Fin n) (B : List (Fin k)) (a : Fin k) :
    (D.keep i B).fix i a = D.fix i a := by
  simp [Dom.fix, Dom.keep]

/-- Fixing site `i` in `D.drop i B` gives the same box as fixing it in `D`. -/
theorem Dom.fix_drop (D : Dom n k) (i : Fin n) (B : List (Fin k)) (a : Fin k) :
    (D.drop i B).fix i a = D.fix i a := by
  simp [Dom.fix, Dom.drop]

/-- A dual leaf accepted on every box `D.fix i a`, `a ∈ D i`, is accepted on `D`, provided the
list of site `i` is not empty: every condition of `LeafOK` on `D` is a condition on one of these
boxes. -/
theorem leafOK_of_fix (I : PairInstance n k) (D : Dom n k) (L : ℚ) (u : Fin n → ℚ)
    (p : Fin n → Fin n → ℚ) (m : Fin n → Fin n → Fin k → ℚ) (i : Fin n) (hne : D i ≠ [])
    (h : ∀ a ∈ D i, LeafOK I (D.fix i a) L u p m) : LeafOK I D L u p m := by
  obtain ⟨a₀, ha₀⟩ := List.exists_mem_of_ne_nil _ hne
  have self : ∀ a, a ∈ D.fix i a i := fun a => by
    rw [Dom.fix_self]
    exact List.mem_singleton.mpr rfl
  have other : ∀ a j, j ≠ i → ∀ b ∈ D j, b ∈ D.fix i a j := fun a j hj b hb => by
    rw [D.fix_of_ne a hj]
    exact hb
  refine ⟨fun j b hb => ?_, fun j l hl b hb c hc => ?_, (h a₀ ha₀).2.2⟩
  · by_cases hj : j = i
    · subst hj
      exact (h b hb).1 j b (self b)
    · exact (h a₀ ha₀).1 j b (other a₀ j hj b hb)
  · by_cases hj : j = i
    · subst hj
      have hl' : l ≠ j := (Finset.mem_erase.mp hl).1
      exact (h b hb).2.1 j l hl b (self b) c (other b l hl' c hc)
    · by_cases hl' : l = i
      · subst hl'
        exact (h c hc).2.1 j l hl b (other c j hj b hb) c (self c)
      · exact (h a₀ ha₀).2.1 j l hl b (other a₀ j hj b hb) c (other a₀ l hl' c hc)

/-- **A dual leaf on a box is the same leaf on every slice of the box.**  On a box whose list at
site `i` is not empty, a dual leaf is accepted iff it is accepted on each of the boxes
`D.fix i a`, `a ∈ D i`, on which a `branch` node checks its children. -/
theorem leafOK_iff_fix (I : PairInstance n k) (D : Dom n k) (L : ℚ) (u : Fin n → ℚ)
    (p : Fin n → Fin n → ℚ) (m : Fin n → Fin n → Fin k → ℚ) (i : Fin n) (hne : D i ≠ []) :
    LeafOK I D L u p m ↔ ∀ a ∈ D i, LeafOK I (D.fix i a) L u p m :=
  ⟨fun h a ha => leafOK_mono I D (D.fix i a) L u p m (Dom.fix_subset ha) h,
    leafOK_of_fix I D L u p m i hne⟩

/-- **A split of two leaves adds no proving power over `branch` with repeated leaves.**  If the
layered checker accepts the split whose children are the dual leaves `(u₁, p₁, m₁)` and
`(u₂, p₂, m₂)`, the kernel accepts the `branch` node whose child is the first leaf for every
state listed in `B` and the second leaf for every other state.  The split only saves checks. -/
theorem split_leaves_imp_branch (I : PairInstance n k) (D : Dom n k) (L : ℚ) (i : Fin n)
    (B : List (Fin k)) (u₁ u₂ : Fin n → ℚ) (p₁ p₂ : Fin n → Fin n → ℚ)
    (m₁ m₂ : Fin n → Fin n → Fin k → ℚ)
    (hv : verifyS (.split i B (.base (.leaf u₁ p₁ m₁)) (.base (.leaf u₂ p₂ m₂))) I D L = true) :
    verify (.branch i fun a => if a ∈ B then .leaf u₁ p₁ m₁ else .leaf u₂ p₂ m₂) I D L = true := by
  simp only [verifyS, verify, Bool.and_eq_true, decide_eq_true_eq] at hv
  obtain ⟨h₁, h₂⟩ := hv
  simp only [verify, List.all_eq_true]
  intro a ha
  by_cases hB : a ∈ B
  · rw [if_pos hB]
    simp only [verify, decide_eq_true_eq]
    exact leafOK_mono I _ _ L u₁ p₁ m₁ (Dom.fix_subset_keep ha hB) h₁
  · rw [if_neg hB]
    simp only [verify, decide_eq_true_eq]
    exact leafOK_mono I _ _ L u₂ p₂ m₂ (Dom.fix_subset_drop ha hB) h₂

/-- **Converse of `split_leaves_imp_branch`.**  If each of the two blocks contains a state of the
current list of site `i`, a `branch` node that repeats one leaf for the states listed in `B` and
another leaf for the other states can be replaced by the split of the two leaves.  (Without the
two hypotheses the split still checks its leaf on a box with an empty list, where the inequality
`L ≤ Σ u + Σ p` and the conditions of the other sites remain.) -/
theorem branch_leaves_imp_split (I : PairInstance n k) (D : Dom n k) (L : ℚ) (i : Fin n)
    (B : List (Fin k)) (u₁ u₂ : Fin n → ℚ) (p₁ p₂ : Fin n → Fin n → ℚ)
    (m₁ m₂ : Fin n → Fin n → Fin k → ℚ) (hB : ∃ a ∈ D i, a ∈ B) (hB' : ∃ a ∈ D i, a ∉ B)
    (hv : verify (.branch i fun a => if a ∈ B then .leaf u₁ p₁ m₁ else .leaf u₂ p₂ m₂) I D L =
      true) :
    verifyS (.split i B (.base (.leaf u₁ p₁ m₁)) (.base (.leaf u₂ p₂ m₂))) I D L = true := by
  simp only [verify, List.all_eq_true] at hv
  simp only [verifyS, verify, Bool.and_eq_true, decide_eq_true_eq]
  constructor
  · obtain ⟨a₀, ha₀, haB₀⟩ := hB
    refine leafOK_of_fix I (D.keep i B) L u₁ p₁ m₁ i
      (List.ne_nil_of_mem (Dom.mem_keep.mpr ⟨ha₀, fun _ => haB₀⟩)) fun a ha => ?_
    obtain ⟨haD, haB⟩ := Dom.mem_keep.mp ha
    have hva := hv a haD
    rw [if_pos (haB rfl)] at hva
    simp only [verify, decide_eq_true_eq] at hva
    rw [Dom.fix_keep]
    exact hva
  · obtain ⟨a₀, ha₀, haB₀⟩ := hB'
    refine leafOK_of_fix I (D.drop i B) L u₂ p₂ m₂ i
      (List.ne_nil_of_mem (Dom.mem_drop.mpr ⟨ha₀, fun _ => haB₀⟩)) fun a ha => ?_
    obtain ⟨haD, haB⟩ := Dom.mem_drop.mp ha
    have hva := hv a haD
    rw [if_neg (haB rfl)] at hva
    simp only [verify, decide_eq_true_eq] at hva
    rw [Dom.fix_drop]
    exact hva

/-- **Split of two leaves = `branch` with repeated leaves**, when each of the two blocks contains
a state of the current list of site `i`: the two certificates are accepted together. -/
theorem split_leaves_iff_branch (I : PairInstance n k) (D : Dom n k) (L : ℚ) (i : Fin n)
    (B : List (Fin k)) (u₁ u₂ : Fin n → ℚ) (p₁ p₂ : Fin n → Fin n → ℚ)
    (m₁ m₂ : Fin n → Fin n → Fin k → ℚ) (hB : ∃ a ∈ D i, a ∈ B) (hB' : ∃ a ∈ D i, a ∉ B) :
    verifyS (.split i B (.base (.leaf u₁ p₁ m₁)) (.base (.leaf u₂ p₂ m₂))) I D L = true ↔
      verify (.branch i fun a => if a ∈ B then .leaf u₁ p₁ m₁ else .leaf u₂ p₂ m₂) I D L =
        true :=
  ⟨split_leaves_imp_branch I D L i B u₁ u₂ p₁ p₂ m₁ m₂,
    branch_leaves_imp_split I D L i B u₁ u₂ p₁ p₂ m₁ m₂ hB hB'⟩

/-- A split of two leaves has three nodes … -/
theorem split_leaves_size (i : Fin n) (B : List (Fin k)) (u₁ u₂ : Fin n → ℚ)
    (p₁ p₂ : Fin n → Fin n → ℚ) (m₁ m₂ : Fin n → Fin n → Fin k → ℚ) :
    (SCert.split i B (.base (.leaf u₁ p₁ m₁)) (.base (.leaf u₂ p₂ m₂))).size = 3 := rfl

/-- … whereas the `branch` node with the two leaves repeated has `1 + k` nodes, one leaf per
state. -/
theorem branch_leaves_size (i : Fin n) (B : List (Fin k)) (u₁ u₂ : Fin n → ℚ)
    (p₁ p₂ : Fin n → Fin n → ℚ) (m₁ m₂ : Fin n → Fin n → Fin k → ℚ) :
    (Cert.branch i fun a => if a ∈ B then Cert.leaf u₁ p₁ m₁ else Cert.leaf u₂ p₂ m₂).size =
      1 + k := by
  have h : ∀ a : Fin k,
      (if a ∈ B then Cert.leaf u₁ p₁ m₁ else Cert.leaf u₂ p₂ m₂).size = 1 := by
    intro a
    split_ifs <;> rfl
  simp [Cert.size, h]

/-! ### A worked instance: one state against the others (non-vacuity)

The acceptance and rejection facts below are proved by `decide +kernel`: the checker is run
inside Lean's kernel on exact rationals, as for the instances of `CertificateAlgebra.lean`. -/

/-- A frustrated triangle with three states per site (`n = 3`, `k = 3`).  State `0` forms one
class and the states `1`, `2` the other.  Two sites in the same class cost `1` (each unordered
pair is stored once, in the orientation `i < j`), and state `2` costs `1/2` more than state `1`
at every site.  The minimum of the energy is `1` (`splitTriangle_lower_bound`,
`splitTriangle_optimum`). -/
def splitTriangle : PairInstance 3 3 where
  h := fun _ a =>
    match a with
    | 0 => 0
    | 1 => 0
    | 2 => 1 / 2
  J := fun i j a b =>
    if i < j then
      match a, b with
      | 0, 0 => 1
      | 0, _ => 0
      | _, 0 => 0
      | _, _ => 1
    else 0

/-- Dual leaf for the box in which site `0` is in state `0`.  The messages are those of
`triangleCert` in `CertificateAlgebra.lean` with the class of a state in place of the state:
`m 1 0 s = m 2 0 s = [s = 0]`, `m 1 2 s = [s ≠ 0]`, `m 2 1 s = -[s = 0]`. -/
def splitTriangleKeepLeaf : Cert 3 3 :=
  .leaf (fun i => if i = 1 then 1 else 0) (fun _ _ => 0)
    (fun i j s =>
      match i, j, s with
      | 1, 0, 0 => 1
      | 2, 0, 0 => 1
      | 1, 2, 1 => 1
      | 1, 2, 2 => 1
      | 2, 1, 0 => -1
      | _, _, _ => 0)

/-- Dual leaf for the box in which site `0` is in state `1` or `2`: the same messages with the
two classes exchanged, `m 1 0 s = m 2 0 s = [s ≠ 0]`, `m 1 2 s = [s = 0]`, `m 2 1 s = -[s ≠ 0]`.
One leaf serves the two states. -/
def splitTriangleDropLeaf : Cert 3 3 :=
  .leaf (fun i => if i = 1 then 1 else 0) (fun _ _ => 0)
    (fun i j s =>
      match i, j, s with
      | 1, 0, 1 => 1
      | 1, 0, 2 => 1
      | 2, 0, 1 => 1
      | 2, 0, 2 => 1
      | 1, 2, 0 => 1
      | 2, 1, 1 => -1
      | 2, 1, 2 => -1
      | _, _, _ => 0)

/-- The split certificate: state `0` of site `0` against the states `1` and `2`, one dual leaf
for each part. -/
def splitTriangleCert : SCert 3 3 :=
  .split 0 [0] (.base splitTriangleKeepLeaf) (.base splitTriangleDropLeaf)

/-- The layered checker accepts the two-leaf split certificate for the bound `1`. -/
theorem splitTriangle_verified :
    verifyS splitTriangleCert splitTriangle (fullDom 3 3) 1 = true := by decide +kernel

/-- Hence every configuration of `splitTriangle` has energy at least `1` … -/
theorem splitTriangle_lower_bound (x : Config 3 3) : 1 ≤ splitTriangle.energy x :=
  verifyS_sound splitTriangleCert splitTriangle (fullDom 3 3) 1 splitTriangle_verified x
    (inBox_fullDom x)

/-- … and the bound is attained: `1` is the minimum of the energy over the full box. -/
theorem splitTriangle_optimum : splitTriangle.energy ![0, 1, 0] = 1 := by decide +kernel

/-- Control: the same certificate is rejected for the (false) bound `2`. -/
theorem splitTriangle_rejects :
    verifyS splitTriangleCert splitTriangle (fullDom 3 3) 2 = false := by decide +kernel

/-- Control: the leaf of the first child alone is rejected on the full box; its messages are
valid only where site `0` is in state `0`. -/
theorem splitTriangle_keepLeaf_rejected :
    verify splitTriangleKeepLeaf splitTriangle (fullDom 3 3) 1 = false := by decide +kernel

/-- Control: with its two children exchanged the certificate is rejected; each leaf is valid on
its own part of the box only. -/
theorem splitTriangle_exchanged_rejected :
    verifyS (.split 0 [0] (.base splitTriangleDropLeaf) (.base splitTriangleKeepLeaf))
      splitTriangle (fullDom 3 3) 1 = false := by decide +kernel

/-- **No single dual leaf does the work of the split.**  A dual leaf accepted on the full box of
`splitTriangle` certifies at most `0`, although the minimum is `1`.  (The fractional configuration
that puts every site half in state `0` and half in state `1`, and every pair of sites half in
`(0, 1)` and half in `(1, 0)`, costs nothing; the proof evaluates the conditions of `LeafOK` at
these states and adds them up.) -/
theorem splitTriangle_leaf_gap (L : ℚ) (u : Fin 3 → ℚ) (p : Fin 3 → Fin 3 → ℚ)
    (m : Fin 3 → Fin 3 → Fin 3 → ℚ) (h : LeafOK splitTriangle (fullDom 3 3) L u p m) :
    L ≤ 0 := by
  obtain ⟨hu, hp, hL⟩ := h
  have mem : ∀ (i : Fin 3) (a : Fin 3), a ∈ fullDom 3 3 i := fun _ a => List.mem_finRange a
  have h1 : ∀ i, 2 * u i ≤ ∑ j ∈ univ.erase i, (m i j 0 + m i j 1) := by
    intro i
    have a0 := hu i 0 (mem i 0)
    have a1 := hu i 1 (mem i 1)
    have e0 : splitTriangle.h i 0 = 0 := rfl
    have e1 : splitTriangle.h i 1 = 0 := rfl
    rw [Finset.sum_add_distrib]
    linarith
  have h2 : ∀ i, ∀ j ∈ univ.erase i,
      4 * p i j ≤ -(m i j 0 + m i j 1) - (m j i 0 + m j i 1) := by
    intro i j hj
    have b01 := hp i j hj 0 (mem i 0) 1 (mem j 1)
    have b10 := hp i j hj 1 (mem i 1) 0 (mem j 0)
    have e : ∀ i j : Fin 3, splitTriangle.J i j 0 1 = 0 ∧ splitTriangle.J i j 1 0 = 0 := by
      decide +kernel
    rw [(e i j).1, (e j i).2] at b01
    rw [(e i j).2, (e j i).1] at b10
    linarith
  have h3 : 4 * ∑ i, u i ≤ 2 * ∑ i, ∑ j ∈ univ.erase i, (m i j 0 + m i j 1) := by
    rw [Finset.mul_sum, Finset.mul_sum]
    exact Finset.sum_le_sum fun i _ => by linarith [h1 i]
  have h4 : 4 * ∑ i, ∑ j ∈ univ.erase i, p i j ≤
      -(∑ i, ∑ j ∈ univ.erase i, (m i j 0 + m i j 1)) -
        ∑ i, ∑ j ∈ univ.erase i, (m j i 0 + m j i 1) := by
    simp only [Finset.mul_sum, ← Finset.sum_neg_distrib, ← Finset.sum_sub_distrib]
    exact Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j hj => h2 i j hj
  have h5 := sum_erase_swap (fun i j : Fin 3 => m i j 0 + m i j 1)
  linarith

/-- The kernel rejects every single dual leaf for the bound `1` on the full box of
`splitTriangle`. -/
theorem splitTriangle_no_leaf (u : Fin 3 → ℚ) (p : Fin 3 → Fin 3 → ℚ)
    (m : Fin 3 → Fin 3 → Fin 3 → ℚ) :
    verify (.leaf u p m) splitTriangle (fullDom 3 3) 1 = false := by
  by_contra hne
  have hv : verify (.leaf u p m) splitTriangle (fullDom 3 3) 1 = true := by simpa using hne
  simp only [verify, decide_eq_true_eq] at hv
  have := splitTriangle_leaf_gap 1 u p m hv
  norm_num at this

/-- By `split_leaves_imp_branch` the kernel accepts the `branch` certificate in which the second
leaf is repeated for the states `1` and `2`: three leaf checks where the split needs two. -/
theorem splitTriangle_branch_verified :
    verify (.branch 0 fun a => if a ∈ [0] then splitTriangleKeepLeaf else splitTriangleDropLeaf)
      splitTriangle (fullDom 3 3) 1 = true :=
  split_leaves_imp_branch _ _ _ _ _ _ _ _ _ _ _ splitTriangle_verified

end MetricChain
