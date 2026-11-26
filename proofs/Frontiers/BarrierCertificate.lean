import Mathlib
import proofs.CertificateAlgebra
import proofs.Frontiers.KineticsCertificates

/-!
# Barrier certificates: a tree checker on top of the verified min-kernels

Workstream BK of the theory division.  This file answers request K-T1 of the Scientific Discovery
Division (its message SCI-MSG-0005; its report on certified kinetics,
`docs/science/workstreams/SK_REPORT.md` on the branch `research/scientific-translation`, §2.5 and
§7): the decision-tree checker for lower bounds on minimax barriers.

## What the file proves, in words

The *barrier* between two configurations `a` and `b` is the smallest value, over all walks of
single-site moves from `a` to `b`, of the largest energy met on the walk.  A lower bound on it is a
*cut*: a region `S` that contains `a` and not `b`, such that every configuration that can be
reached from `S` in one move without being in `S` (the *wall*) has energy at least `L`.

A **barrier certificate** (`BCert n k`) describes `S` and its wall by a decision tree.  A `branch`
node splits the current box on the state of one site, exactly as `Cert.branch` does; a `split`
node divides the domain of one site into the states of a list and the others.  Every leaf has a
box and one of three labels: `inside` (the box belongs to `S`), `wall c` (the box belongs to the
wall, and `c` is a certificate of the min-kernel for the bound on that box) or `outside`.

The checker `bverify c I a b L` accepts iff

1. the min-kernel accepts every wall certificate on its box for the bound `L`;
2. no `inside` box is adjacent to an `outside` box — two boxes are *adjacent* iff both are
   non-empty and at most one site has disjoint domains (`Dom.Adjacent`);
3. `a` lies in an `inside` box and `b` lies in no `inside` box.

Main statements:

* `bverify_sound` — if the checker accepts, every walk of single-site moves from `a` to `b` visits
  a configuration of energy at least `L` (exact rational arithmetic, as in `verify_sound`).
  Variants: `bcheck_sound` (every walk that starts in `S` and ends outside `S`, the form of the
  science division's `box_cut_barrier`), `bverifyIn_sound` (a root box other than the full one:
  walks that stay in the root box), `bverify_sound_rev` (the certificate may be built around the
  target instead of the start), `bverify_sound_real` (real pairwise models bounded below by the
  rational instance, as in `verify_sound_real`).
* `Dom.adjacent_of_singleSite`, `Dom.exists_singleSite_of_adjacent`, `Dom.adjacent_iff` — the
  adjacency lemma, both directions: two boxes contain configurations that differ in at most one
  site iff they are adjacent.  Soundness uses the first direction only; the second one says that
  check 2 is exact (`cutCheck_boxAdjacent_iff`).  The non-emptiness clause is necessary
  (`sep_card_le_one_not_sufficient`).
* `CutTree.leaves_cover`, `CutTree.leaves_partition` — the leaf boxes cover the root box
  (used by soundness) and are pairwise disjoint (not used by soundness).
* `bverifyR_sound`, `bverifyR_height`, `bverifyR_trap_height`, `bverifyRTop_sound` — the same on
  the residual kernel `verifyR`: for every residual of the bounded-difference class the walk
  visits a configuration of true energy at least `L`, and the height of the barrier above an
  evaluated anchor is at least `L - (E a + v)`.
* `bverifyOn_sound` — site-graph products: every site moves along the edges of its own move
  relation (for instance nearest voxels of a torsion); `Dom.adjacentOn_iff` is the adjacency lemma
  of that move graph.
* Kernel-evaluated instances (`decide +kernel`, so the checker runs inside Lean's kernel):
  `ferroWell_barrier`, `ferro_barrier_exact`, `ferroFrozen_barrier`, `maze_barrier_exact` with
  `maze_boxCut_start_le` and `maze_boxCut_target_le` (a barrier that the cut tree certifies exactly
  and no box cut certifies beyond the trivial bound), `ferroWellR_trap`, `ferroTopR_barrier`,
  `scan_barrier_exact` (a certified relaxed scan on a site-graph product, rejected on the Hamming
  graph), and rejected certificates, one for each of the three checks (`ferroTop_rejects_bound`,
  `ferroLeak_rejected`, `ferro_rejects_endpoints`).

The combinatorial part is proved once, for an arbitrary wall check and an arbitrary sound box
adjacency test (`cutCheck_sound`, `cutVerify_sound`), and then instantiated for each kernel
(`verify`, `verify` with a real model, `verifyR`) and each move graph.

## Reused from the library (`proofs/CertificateAlgebra.lean`, and `PairModel` of `Core/Basic.lean`)

`PairInstance`, `PairInstance.energy`, `Config`, `Dom`, `InBox`, `fullDom`, `inBox_fullDom`,
`Dom.fix`, `inBox_fix` (the split convention of `Cert.branch`: one child per state of the current
domain, on the box `D.fix i a`), `Cert`, `verify`, `verify_sound`, `verify_sound_real`, `RCert`,
`RProblem`, `ResidualClass`, `ResidualLowerClass`, `ResidualClass.lower`, `RProblem.Consistent`,
`RProblem.Consistent.nonempty`, `verifyR`, `verifyR_sound_lower`, `PairInstance.anchored`,
`exhaustive3`.  No library declaration is modified or restated.

## Taken from the science division's file

`proofs/Frontiers/KineticsCertificates.lean` (the division's file, adopted unchanged) supplies the
notions used here: `IsWalk`, `exists_exit`, `SingleSite`, `wallBox`, `mem_wallBox_of_exit`, `ferro`,
`ferroResidual`, `singleSite_symm`.  The format of the certificate, the three checks and the proof
idea (the first step that leaves `S` lands in a wall box) are those of §2.5 of that division's
report; the residual statements follow its `box_cut_barrier_residual` and `certified_trap_height`.
New here: the tree checker and its soundness, the `split` node, the non-emptiness clause of
adjacency and the converse direction of the adjacency lemma, the partition statement, the
reversed, real-valued and root-box variants, the site-graph version, `boxCut_closed`, and all
instances other than `ferro` and `ferroResidual`.
-/

namespace MetricChain

open Kinetics

variable {n k : ℕ}

/-! ### Part 1. Boxes: membership, sub-boxes, adjacency -/

/-- Membership of a configuration in a box is decidable (one list lookup per site). -/
instance decidableInBox (D : Dom n k) (x : Config n k) : Decidable (InBox D x) := by
  unfold InBox
  infer_instance

/-- Whether two configurations differ in at most one site is decidable. -/
instance decidableSingleSite (x y : Config n k) : Decidable (SingleSite x y) := by
  unfold SingleSite
  infer_instance

/-- The sub-box of `D` in which site `i` keeps only its states listed in `T`. -/
def Dom.restrict (D : Dom n k) (i : Fin n) (T : List (Fin k)) : Dom n k :=
  Function.update D i ((D i).filter fun s => s ∈ T)

/-- The sub-box of `D` in which site `i` loses its states listed in `T`. -/
def Dom.exclude (D : Dom n k) (i : Fin n) (T : List (Fin k)) : Dom n k :=
  Function.update D i ((D i).filter fun s => s ∉ T)

/-- A configuration of `D` whose state at site `i` is listed in `T` lies in `D.restrict i T`. -/
theorem inBox_restrict {D : Dom n k} {x : Config n k} (hx : InBox D x) (i : Fin n)
    (T : List (Fin k)) (hT : x i ∈ T) : InBox (D.restrict i T) x := by
  intro j
  unfold Dom.restrict
  by_cases hj : j = i
  · subst hj
    simp only [Function.update_self]
    exact List.mem_filter.mpr ⟨hx j, by simpa using hT⟩
  · rw [Function.update_of_ne hj]
    exact hx j

/-- A configuration of `D` whose state at site `i` is not listed in `T` lies in
`D.exclude i T`. -/
theorem inBox_exclude {D : Dom n k} {x : Config n k} (hx : InBox D x) (i : Fin n)
    (T : List (Fin k)) (hT : x i ∉ T) : InBox (D.exclude i T) x := by
  intro j
  unfold Dom.exclude
  by_cases hj : j = i
  · subst hj
    simp only [Function.update_self]
    exact List.mem_filter.mpr ⟨hx j, by simpa using hT⟩
  · rw [Function.update_of_ne hj]
    exact hx j

/-- A configuration of the box `D.fix i a`, where `a` is a state of `D i`, has state `a` at site
`i` and lies in `D`. -/
theorem inBox_of_fix {D : Dom n k} {x : Config n k} {i : Fin n} {a : Fin k} (ha : a ∈ D i)
    (hx : InBox (D.fix i a) x) : x i = a ∧ InBox D x := by
  have hi : x i = a := by
    have h := hx i
    unfold Dom.fix at h
    simpa using h
  refine ⟨hi, fun j => ?_⟩
  by_cases hj : j = i
  · subst hj
    rw [hi]
    exact ha
  · have h := hx j
    unfold Dom.fix at h
    rwa [Function.update_of_ne hj] at h

/-- A configuration of `D.restrict i T` has its state at site `i` listed in `T` and lies in
`D`. -/
theorem inBox_of_restrict {D : Dom n k} {x : Config n k} {i : Fin n} {T : List (Fin k)}
    (hx : InBox (D.restrict i T) x) : x i ∈ T ∧ InBox D x := by
  have hi : x i ∈ D i ∧ x i ∈ T := by
    have h := hx i
    unfold Dom.restrict at h
    simpa [List.mem_filter] using h
  refine ⟨hi.2, fun j => ?_⟩
  by_cases hj : j = i
  · subst hj
    exact hi.1
  · have h := hx j
    unfold Dom.restrict at h
    rwa [Function.update_of_ne hj] at h

/-- A configuration of `D.exclude i T` has its state at site `i` not listed in `T` and lies in
`D`. -/
theorem inBox_of_exclude {D : Dom n k} {x : Config n k} {i : Fin n} {T : List (Fin k)}
    (hx : InBox (D.exclude i T) x) : x i ∉ T ∧ InBox D x := by
  have hi : x i ∈ D i ∧ x i ∉ T := by
    have h := hx i
    unfold Dom.exclude at h
    simpa [List.mem_filter] using h
  refine ⟨hi.2, fun j => ?_⟩
  by_cases hj : j = i
  · subst hj
    exact hi.1
  · have h := hx j
    unfold Dom.exclude at h
    rwa [Function.update_of_ne hj] at h

/-- A box is closed under mixing the coordinates of two of its configurations. -/
theorem inBox_mix {D : Dom n k} {x y z : Config n k} (hx : InBox D x) (hy : InBox D y)
    (h : ∀ i, z i = x i ∨ z i = y i) : InBox D z := by
  intro i
  rcases h i with e | e
  · rw [e]
    exact hx i
  · rw [e]
    exact hy i

/-- Site `i` *separates* the boxes `D` and `D'`: their domains at site `i` have no common
state. -/
def Dom.SepAt (D D' : Dom n k) (i : Fin n) : Prop := ∀ s ∈ D i, s ∉ D' i

/-- Separation at a site is decidable (two list traversals). -/
instance Dom.decidableSepAt (D D' : Dom n k) (i : Fin n) : Decidable (D.SepAt D' i) := by
  unfold Dom.SepAt
  infer_instance

/-- **Adjacency of boxes** (unrestricted single-site moves).  Both boxes are non-empty — no
domain of either is the empty list — and at most one site separates them. -/
def Dom.Adjacent (D D' : Dom n k) : Prop :=
  (∀ i, D i ≠ [] ∧ D' i ≠ []) ∧ (Finset.univ.filter fun i => D.SepAt D' i).card ≤ 1

/-- Adjacency of boxes is decidable. -/
instance Dom.decidableAdjacent (D D' : Dom n k) : Decidable (D.Adjacent D') := by
  unfold Dom.Adjacent
  infer_instance

/-- **Adjacency lemma, soundness direction.**  If a configuration of `D` and a configuration of
`D'` differ in at most one site, the two boxes are adjacent.  This is the direction used by the
soundness of the barrier checker. -/
theorem Dom.adjacent_of_singleSite {D D' : Dom n k} {x y : Config n k} (hx : InBox D x)
    (hy : InBox D' y) (h : SingleSite x y) : D.Adjacent D' := by
  refine ⟨fun i => ⟨List.ne_nil_of_mem (hx i), List.ne_nil_of_mem (hy i)⟩, ?_⟩
  obtain ⟨i₀, hi₀⟩ := h
  have key : ∀ j ∈ Finset.univ.filter (fun i => D.SepAt D' i), j = i₀ := by
    intro j hj
    by_contra hne
    have hsep : D.SepAt D' j := (Finset.mem_filter.mp hj).2
    have hmem : x j ∈ D' j := by
      rw [hi₀ j hne]
      exact hy j
    exact hsep (x j) (hx j) hmem
  exact Finset.card_le_one.mpr fun a ha b hb => (key a ha).trans (key b hb).symm

/-- **Adjacency lemma, completeness direction.**  Two adjacent boxes (on at least one site)
contain two configurations that differ in at most one site.  Not used by soundness; it says that
the adjacency test rejects nothing it could accept. -/
theorem Dom.exists_singleSite_of_adjacent (hn : 0 < n) {D D' : Dom n k} (h : D.Adjacent D') :
    ∃ x y, InBox D x ∧ InBox D' y ∧ SingleSite x y := by
  have hc : ∀ i, ∃ s t, s ∈ D i ∧ t ∈ D' i ∧ (¬ D.SepAt D' i → s = t) := by
    intro i
    by_cases hs : D.SepAt D' i
    · obtain ⟨s, hs'⟩ := List.exists_mem_of_ne_nil _ (h.1 i).1
      obtain ⟨t, ht'⟩ := List.exists_mem_of_ne_nil _ (h.1 i).2
      exact ⟨s, t, hs', ht', fun hne => absurd hs hne⟩
    · unfold Dom.SepAt at hs
      push Not at hs
      obtain ⟨s, hs1, hs2⟩ := hs
      exact ⟨s, s, hs1, hs2, fun _ => rfl⟩
  choose x y hx hy hxy using hc
  refine ⟨x, y, hx, hy, ?_⟩
  by_cases hsep : ∃ i, D.SepAt D' i
  · obtain ⟨i₀, hi₀⟩ := hsep
    refine ⟨i₀, fun j hj => hxy j fun hjs => hj ?_⟩
    exact Finset.card_le_one.mp h.2 j (by simp [hjs]) i₀ (by simp [hi₀])
  · exact ⟨⟨0, hn⟩, fun j _ => hxy j fun hjs => hsep ⟨j, hjs⟩⟩

/-- **Adjacency lemma.**  Two boxes on at least one site contain a pair of configurations that
differ in at most one site if and only if they are adjacent: both non-empty, and at most one site
with disjoint domains. -/
theorem Dom.adjacent_iff (hn : 0 < n) {D D' : Dom n k} :
    D.Adjacent D' ↔ ∃ x y, InBox D x ∧ InBox D' y ∧ SingleSite x y :=
  ⟨Dom.exists_singleSite_of_adjacent hn,
    fun ⟨_, _, hx, hy, h⟩ => Dom.adjacent_of_singleSite hx hy h⟩

/-- The non-emptiness clause of `Dom.Adjacent` cannot be dropped from the adjacency lemma: the
boxes `∅ × {0}` and `{0} × {0}` have exactly one separating site, and the first one contains no
configuration at all. -/
theorem sep_card_le_one_not_sufficient :
    ∃ D D' : Dom 2 1, (Finset.univ.filter fun i => D.SepAt D' i).card ≤ 1 ∧
      ¬ ∃ x y, InBox D x ∧ InBox D' y ∧ SingleSite x y := by
  refine ⟨fun i => if i = 0 then [] else [0], fun _ => [0], by decide +kernel, ?_⟩
  rintro ⟨x, y, hx, -, -⟩
  have h := hx 0
  simp at h

/-! ### Part 2. Cut trees and their leaves -/

/-- The three kinds of leaves of a cut tree. -/
inductive Zone (W : Type) : Type
  /-- the box of the leaf belongs to the region `S` -/
  | inside : Zone W
  /-- the box of the leaf belongs to the wall; the payload certifies the bound on it -/
  | wall (w : W) : Zone W
  /-- the box of the leaf is unconstrained -/
  | outside : Zone W

/-- A **cut tree**: a decision tree over the sites whose leaves are labelled `inside`, `wall`
(with a payload of type `W`, a certificate of some kernel) or `outside`.  Read below a root box,
every node has a box: a `branch` node on site `i` has one child per state `a` of the current
domain of `i`, on the box with site `i` fixed to `a` (the convention of `Cert.branch`); a `split`
node on site `i` and list `T` has two children, on the box with site `i` restricted to the states
listed in `T` and on the box with these states removed. -/
inductive CutTree (W : Type) (n k : ℕ) : Type
  /-- the current box lies in the region `S` -/
  | inside : CutTree W n k
  /-- the current box lies in the wall; `w` certifies the bound on it -/
  | wall (w : W) : CutTree W n k
  /-- the current box is unconstrained -/
  | outside : CutTree W n k
  /-- case split on the state of site `i` -/
  | branch (i : Fin n) (children : Fin k → CutTree W n k) : CutTree W n k
  /-- binary split of the domain of site `i`: the states listed in `T`, and the other states -/
  | split (i : Fin n) (T : List (Fin k)) (yes no : CutTree W n k) : CutTree W n k

variable {W : Type}

/-- The leaves of a cut tree below the root box `D`, each with its box and its label. -/
def CutTree.leaves : CutTree W n k → Dom n k → List (Dom n k × Zone W)
  | .inside, D => [(D, .inside)]
  | .wall w, D => [(D, .wall w)]
  | .outside, D => [(D, .outside)]
  | .branch i ch, D => (D i).flatMap fun a => (ch a).leaves (D.fix i a)
  | .split i T yes no, D => yes.leaves (D.restrict i T) ++ no.leaves (D.exclude i T)

/-- **The leaf boxes cover the root box**: every configuration of the root box lies in the box of
some leaf.  This is the property of the tree that the soundness of the checker uses. -/
theorem CutTree.leaves_cover (c : CutTree W n k) :
    ∀ (D : Dom n k) (x : Config n k), InBox D x → ∃ l ∈ c.leaves D, InBox l.1 x := by
  induction c with
  | inside => exact fun D x hx => ⟨(D, .inside), List.mem_singleton.mpr rfl, hx⟩
  | wall w => exact fun D x hx => ⟨(D, .wall w), List.mem_singleton.mpr rfl, hx⟩
  | outside => exact fun D x hx => ⟨(D, .outside), List.mem_singleton.mpr rfl, hx⟩
  | branch i ch ih =>
    intro D x hx
    obtain ⟨l, hl, hlx⟩ := ih (x i) (D.fix i (x i)) x (inBox_fix hx i)
    exact ⟨l, List.mem_flatMap.mpr ⟨x i, hx i, hl⟩, hlx⟩
  | split i T yes no ih₁ ih₂ =>
    intro D x hx
    by_cases hT : x i ∈ T
    · obtain ⟨l, hl, hlx⟩ := ih₁ (D.restrict i T) x (inBox_restrict hx i T hT)
      exact ⟨l, List.mem_append_left _ hl, hlx⟩
    · obtain ⟨l, hl, hlx⟩ := ih₂ (D.exclude i T) x (inBox_exclude hx i T hT)
      exact ⟨l, List.mem_append_right _ hl, hlx⟩

/-- Every leaf box is contained in the root box. -/
theorem CutTree.leaves_subset (c : CutTree W n k) :
    ∀ (D : Dom n k), ∀ l ∈ c.leaves D, ∀ x, InBox l.1 x → InBox D x := by
  induction c with
  | inside =>
    intro D l hl x hx
    rw [List.mem_singleton.mp hl] at hx
    exact hx
  | wall w =>
    intro D l hl x hx
    rw [List.mem_singleton.mp hl] at hx
    exact hx
  | outside =>
    intro D l hl x hx
    rw [List.mem_singleton.mp hl] at hx
    exact hx
  | branch i ch ih =>
    intro D l hl x hx
    obtain ⟨a, ha, hla⟩ := List.mem_flatMap.mp hl
    exact (inBox_of_fix ha (ih a (D.fix i a) l hla x hx)).2
  | split i T yes no ih₁ ih₂ =>
    intro D l hl x hx
    rcases List.mem_append.mp hl with h | h
    · exact (inBox_of_restrict (ih₁ _ l h x hx)).2
    · exact (inBox_of_exclude (ih₂ _ l h x hx)).2

/-- Two leaves whose boxes share a configuration are the same leaf: the leaf boxes are pairwise
disjoint. -/
theorem CutTree.leaves_unique (c : CutTree W n k) :
    ∀ (D : Dom n k) (x : Config n k), ∀ l ∈ c.leaves D, ∀ l' ∈ c.leaves D,
      InBox l.1 x → InBox l'.1 x → l = l' := by
  induction c with
  | inside =>
    intro D x l hl l' hl' _ _
    rw [List.mem_singleton.mp hl, List.mem_singleton.mp hl']
  | wall w =>
    intro D x l hl l' hl' _ _
    rw [List.mem_singleton.mp hl, List.mem_singleton.mp hl']
  | outside =>
    intro D x l hl l' hl' _ _
    rw [List.mem_singleton.mp hl, List.mem_singleton.mp hl']
  | branch i ch ih =>
    intro D x l hl l' hl' hx hx'
    obtain ⟨a, ha, hla⟩ := List.mem_flatMap.mp hl
    obtain ⟨a', ha', hla'⟩ := List.mem_flatMap.mp hl'
    have e : x i = a := (inBox_of_fix ha ((ch a).leaves_subset _ l hla x hx)).1
    have e' : x i = a' := (inBox_of_fix ha' ((ch a').leaves_subset _ l' hla' x hx')).1
    have haa : a = a' := e.symm.trans e'
    subst haa
    exact ih a (D.fix i a) x l hla l' hla' hx hx'
  | split i T yes no ih₁ ih₂ =>
    intro D x l hl l' hl' hx hx'
    rcases List.mem_append.mp hl with h | h <;> rcases List.mem_append.mp hl' with h' | h'
    · exact ih₁ _ x l h l' h' hx hx'
    · exact absurd (inBox_of_restrict (yes.leaves_subset _ l h x hx)).1
        (inBox_of_exclude (no.leaves_subset _ l' h' x hx')).1
    · exact absurd (inBox_of_restrict (yes.leaves_subset _ l' h' x hx')).1
        (inBox_of_exclude (no.leaves_subset _ l h x hx)).1
    · exact ih₂ _ x l h l' h' hx hx'

/-- **The leaf boxes partition the root box**: every configuration of the root box lies in the
box of exactly one leaf.  (Soundness of the checker only uses the covering half.) -/
theorem CutTree.leaves_partition (c : CutTree W n k) (D : Dom n k) (x : Config n k)
    (hx : InBox D x) : ∃! l, l ∈ c.leaves D ∧ InBox l.1 x := by
  obtain ⟨l, hl, hlx⟩ := c.leaves_cover D x hx
  exact ⟨l, ⟨hl, hlx⟩, fun l' h' => c.leaves_unique D x l' h'.1 l hl h'.2 hlx⟩

/-- The boxes of the `inside` leaves. -/
def CutTree.insideBoxes (c : CutTree W n k) (D : Dom n k) : List (Dom n k) :=
  (c.leaves D).filterMap fun l =>
    match l.2 with
    | .inside => some l.1
    | _ => none

/-- A box is one of the inside boxes iff it is the box of an `inside` leaf. -/
theorem CutTree.mem_insideBoxes {c : CutTree W n k} {D B : Dom n k} :
    B ∈ c.insideBoxes D ↔ (B, Zone.inside) ∈ c.leaves D := by
  unfold CutTree.insideBoxes
  rw [List.mem_filterMap]
  constructor
  · rintro ⟨⟨B', z⟩, hl, h⟩
    cases z with
    | inside =>
      simp only [Option.some.injEq] at h
      subst h
      exact hl
    | wall w => simp at h
    | outside => simp at h
  · intro h
    exact ⟨(B, Zone.inside), h, rfl⟩

/-- The region `S` described by a cut tree below the root box `D`: the union of the boxes of its
`inside` leaves. -/
def CutTree.Inside (c : CutTree W n k) (D : Dom n k) (x : Config n k) : Prop :=
  ∃ B ∈ c.insideBoxes D, InBox B x

/-- Membership in the region of a cut tree is decidable. -/
instance CutTree.decidableInside (c : CutTree W n k) (D : Dom n k) (x : Config n k) :
    Decidable (c.Inside D x) := by
  unfold CutTree.Inside
  infer_instance

/-! ### Part 3. The generic cut check and its soundness

The combinatorial argument does not depend on the kernel that certifies the wall boxes, nor on the
move graph: it is stated for a wall check `wallOK` with a semantic consequence `good`, and for a
Boolean box test `adjB` that is sound for a move relation `adj`. -/

/-- **The cut check.**  Every `wall` leaf passes the wall check `wallOK` on its box, and no
`inside` leaf box is adjacent, in the sense of the Boolean test `adjB`, to an `outside` leaf
box. -/
def cutCheck (adjB : Dom n k → Dom n k → Bool) (wallOK : W → Dom n k → Bool)
    (c : CutTree W n k) (D : Dom n k) : Bool :=
  (c.leaves D).all fun l =>
    match l.2 with
    | .inside => true
    | .wall w => wallOK w l.1
    | .outside => (c.insideBoxes D).all fun B => !adjB B l.1

/-- What the cut check checks, leaf by leaf: the wall check on every wall leaf, and the adjacency
test on every pair of an inside leaf and an outside leaf. -/
theorem cutCheck_iff (adjB : Dom n k → Dom n k → Bool) (wallOK : W → Dom n k → Bool)
    (c : CutTree W n k) (D : Dom n k) :
    cutCheck adjB wallOK c D = true ↔
      (∀ B w, (B, Zone.wall w) ∈ c.leaves D → wallOK w B = true) ∧
        ∀ B B', (B, Zone.inside) ∈ c.leaves D → (B', Zone.outside) ∈ c.leaves D →
          adjB B B' = false := by
  unfold cutCheck
  rw [List.all_eq_true]
  constructor
  · intro h
    refine ⟨fun B w hl => h (B, .wall w) hl, fun B B' hB hB' => ?_⟩
    have h1 := List.all_eq_true.mp (h (B', .outside) hB') B (CutTree.mem_insideBoxes.mpr hB)
    simpa using h1
  · rintro ⟨h1, h2⟩ ⟨B', z⟩ hl
    cases z with
    | inside => rfl
    | wall w => exact h1 B' w hl
    | outside =>
      refine List.all_eq_true.mpr fun B hB => ?_
      simp [h2 B B' (CutTree.mem_insideBoxes.mp hB) hl]

/-- **Soundness of the cut check** (region form).  Let the Boolean test `adjB` hold for every pair
of boxes that contain the two ends of a move, and let the wall check imply the property `good` on
the whole box.  If the cut check accepts, then every walk that stays in the root box, starts in
the region `S` of the tree and ends outside `S` has a step from `S` onto a configuration with the
property `good`: the first step that leaves `S`. -/
theorem cutCheck_sound (adj : Config n k → Config n k → Prop) (adjB : Dom n k → Dom n k → Bool)
    (hadj : ∀ B B' x y, InBox B x → InBox B' y → adj x y → adjB B B' = true)
    (wallOK : W → Dom n k → Bool) (good : Config n k → Prop)
    (hgood : ∀ w B, wallOK w B = true → ∀ x, InBox B x → good x)
    (c : CutTree W n k) (D : Dom n k) (hv : cutCheck adjB wallOK c D = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk adj p m)
    (hD : ∀ j, j ≤ m → InBox D (p j)) (ha : c.Inside D (p 0)) (hb : ¬ c.Inside D (p m)) :
    ∃ j, j < m ∧ c.Inside D (p j) ∧ good (p (j + 1)) := by
  obtain ⟨j, hj, h1, h2⟩ := exists_exit {x | c.Inside D x} p m ha hb
  refine ⟨j, hj, h1, ?_⟩
  obtain ⟨⟨B', z⟩, hl, hly⟩ := c.leaves_cover D (p (j + 1)) (hD (j + 1) hj)
  have hchk := List.all_eq_true.mp hv (B', z) hl
  cases z with
  | inside => exact absurd ⟨B', CutTree.mem_insideBoxes.mpr hl, hly⟩ h2
  | wall w => exact hgood w B' hchk (p (j + 1)) hly
  | outside =>
    obtain ⟨B, hB, hBx⟩ := h1
    have hnadj := List.all_eq_true.mp hchk B hB
    have hadjB := hadj B B' (p j) (p (j + 1)) hBx hly (hp j hj)
    simp [hadjB] at hnadj

/-- **The cut verifier**: the cut check, and the start `a` lies in an `inside` leaf box while the
target `b` lies in no `inside` leaf box. -/
def cutVerify (adjB : Dom n k → Dom n k → Bool) (wallOK : W → Dom n k → Bool)
    (c : CutTree W n k) (D : Dom n k) (a b : Config n k) : Bool :=
  cutCheck adjB wallOK c D && decide (c.Inside D a) && !decide (c.Inside D b)

/-- **Soundness of the cut verifier** (endpoint form).  Under the hypotheses of `cutCheck_sound`,
if the cut verifier accepts, every walk from `a` to `b` that stays in the root box visits, after
its start, a configuration with the property `good`. -/
theorem cutVerify_sound (adj : Config n k → Config n k → Prop) (adjB : Dom n k → Dom n k → Bool)
    (hadj : ∀ B B' x y, InBox B x → InBox B' y → adj x y → adjB B B' = true)
    (wallOK : W → Dom n k → Bool) (good : Config n k → Prop)
    (hgood : ∀ w B, wallOK w B = true → ∀ x, InBox B x → good x)
    (c : CutTree W n k) (D : Dom n k) (a b : Config n k)
    (hv : cutVerify adjB wallOK c D a b = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk adj p m)
    (hD : ∀ j, j ≤ m → InBox D (p j)) (h0 : p 0 = a) (hm : p m = b) :
    ∃ j, 0 < j ∧ j ≤ m ∧ good (p j) := by
  simp only [cutVerify, Bool.and_eq_true, Bool.not_eq_true', decide_eq_true_eq,
    decide_eq_false_iff_not] at hv
  obtain ⟨⟨hc, ha⟩, hb⟩ := hv
  rw [← h0] at ha
  rw [← hm] at hb
  obtain ⟨j, hj, -, hg⟩ := cutCheck_sound adj adjB hadj wallOK good hgood c D hc p m hp hD ha hb
  exact ⟨j + 1, Nat.succ_pos j, hj, hg⟩

/-- A walk on a symmetric move relation can be traversed backwards. -/
theorem isWalk_reverse {X : Type*} {adj : X → X → Prop} (hsymm : ∀ x y, adj x y → adj y x)
    {p : ℕ → X} {m : ℕ} (hp : IsWalk adj p m) : IsWalk adj (fun j => p (m - j)) m := by
  intro j hj
  have h := hp (m - (j + 1)) (by omega)
  have e : m - (j + 1) + 1 = m - j := by omega
  rw [e] at h
  exact hsymm _ _ h

/-! ### Part 4. Barrier certificates on the min-kernel `verify` -/

/-- The Boolean adjacency test for unrestricted single-site moves. -/
def boxAdjacent (B B' : Dom n k) : Bool := decide (B.Adjacent B')

/-- The Boolean adjacency test holds for the boxes of the two ends of a single-site move. -/
theorem boxAdjacent_of_singleSite (B B' : Dom n k) (x y : Config n k) (hx : InBox B x)
    (hy : InBox B' y) (h : SingleSite x y) : boxAdjacent B B' = true :=
  decide_eq_true (Dom.adjacent_of_singleSite hx hy h)

/-- **Exactness of the adjacency check.**  With at least one site, the cut check for single-site
moves accepts if and only if every wall leaf passes the wall check and no single-site move leads
from the box of an `inside` leaf to the box of an `outside` leaf. -/
theorem cutCheck_boxAdjacent_iff (hn : 0 < n) (wallOK : W → Dom n k → Bool) (c : CutTree W n k)
    (D : Dom n k) :
    cutCheck boxAdjacent wallOK c D = true ↔
      (∀ B w, (B, Zone.wall w) ∈ c.leaves D → wallOK w B = true) ∧
        ∀ B B', (B, Zone.inside) ∈ c.leaves D → (B', Zone.outside) ∈ c.leaves D →
          ∀ x y, InBox B x → InBox B' y → ¬ SingleSite x y := by
  rw [cutCheck_iff]
  constructor
  · rintro ⟨h1, h2⟩
    refine ⟨h1, fun B B' hB hB' x y hx hy hss => ?_⟩
    have h := h2 B B' hB hB'
    rw [boxAdjacent_of_singleSite B B' x y hx hy hss] at h
    exact absurd h (by decide)
  · rintro ⟨h1, h2⟩
    refine ⟨h1, fun B B' hB hB' => ?_⟩
    unfold boxAdjacent
    rw [decide_eq_false_iff_not]
    intro hadj
    obtain ⟨x, y, hx, hy, hss⟩ := Dom.exists_singleSite_of_adjacent hn hadj
    exact h2 B B' hB hB' x y hx hy hss

/-- **Barrier certificates** for pairwise energies: cut trees whose `wall` leaves carry
certificates of the min-kernel. -/
abbrev BCert (n k : ℕ) : Type := CutTree (Cert n k) n k

/-- The cut part of the barrier checker (all configurations): the min-kernel accepts every wall
certificate on its box for the bound `L`, and no `inside` box is adjacent to an `outside` box. -/
def bcheck (c : BCert n k) (I : PairInstance n k) (L : ℚ) : Bool :=
  cutCheck boxAdjacent (fun w B => verify w I B L) c (fullDom n k)

/-- The barrier checker below a root box `D`. -/
def bverifyIn (c : BCert n k) (I : PairInstance n k) (D : Dom n k) (a b : Config n k) (L : ℚ) :
    Bool :=
  cutVerify boxAdjacent (fun w B => verify w I B L) c D a b

/-- **The barrier checker.**  `bverify c I a b L = true` certifies that every walk of single-site
moves from `a` to `b` visits a configuration of energy at least `L`: the kernel accepts every wall
certificate for the bound `L`, no `inside` box is adjacent to an `outside` box, `a` lies in an
`inside` box and `b` lies in none. -/
def bverify (c : BCert n k) (I : PairInstance n k) (a b : Config n k) (L : ℚ) : Bool :=
  bverifyIn c I (fullDom n k) a b L

/-- The barrier checker is the cut part followed by the two endpoint tests. -/
theorem bverify_eq (c : BCert n k) (I : PairInstance n k) (a b : Config n k) (L : ℚ) :
    bverify c I a b L =
      (bcheck c I L && decide (c.Inside (fullDom n k) a) && !decide (c.Inside (fullDom n k) b)) :=
  rfl

/-- **Soundness of the cut part** (region form; this is `box_cut_barrier` of the science
division with a cut tree in place of a box).  If the cut part of the barrier checker accepts,
every walk of single-site moves that starts in the region `S` of the tree and ends outside `S`
visits a configuration of energy at least `L`. -/
theorem bcheck_sound (c : BCert n k) (I : PairInstance n k) (L : ℚ) (hv : bcheck c I L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m)
    (ha : c.Inside (fullDom n k) (p 0)) (hb : ¬ c.Inside (fullDom n k) (p m)) :
    ∃ j, j ≤ m ∧ L ≤ I.energy (p j) := by
  obtain ⟨j, hj, -, hL⟩ := cutCheck_sound SingleSite boxAdjacent boxAdjacent_of_singleSite
    (fun w B => verify w I B L) (fun x => L ≤ I.energy x)
    (fun w B h x hx => verify_sound w I B L h x hx) c (fullDom n k) hv p m hp
    (fun j _ => inBox_fullDom (p j)) ha hb
  exact ⟨j + 1, hj, hL⟩

/-- **Soundness below a root box.**  If the barrier checker accepts below the root box `D`, every
walk of single-site moves from `a` to `b` that stays in `D` visits a configuration of energy at
least `L`. -/
theorem bverifyIn_sound (c : BCert n k) (I : PairInstance n k) (D : Dom n k) (a b : Config n k)
    (L : ℚ) (hv : bverifyIn c I D a b L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m)
    (hD : ∀ j, j ≤ m → InBox D (p j)) (h0 : p 0 = a) (hm : p m = b) :
    ∃ j, j ≤ m ∧ L ≤ I.energy (p j) := by
  obtain ⟨j, -, hj, hL⟩ := cutVerify_sound SingleSite boxAdjacent boxAdjacent_of_singleSite
    (fun w B => verify w I B L) (fun x => L ≤ I.energy x)
    (fun w B h x hx => verify_sound w I B L h x hx) c D a b hv p m hp hD h0 hm
  exact ⟨j, hj, hL⟩

/-- **Soundness of the barrier checker.**  If `bverify c I a b L = true`, every walk of
single-site moves from `a` to `b` visits a configuration of energy at least `L`: the minimax
barrier between `a` and `b` is at least `L`. -/
theorem bverify_sound (c : BCert n k) (I : PairInstance n k) (a b : Config n k) (L : ℚ)
    (hv : bverify c I a b L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m) (h0 : p 0 = a) (hm : p m = b) :
    ∃ j, j ≤ m ∧ L ≤ I.energy (p j) :=
  bverifyIn_sound c I (fullDom n k) a b L hv p m hp (fun j _ => inBox_fullDom (p j)) h0 hm

/-- **The certificate may be built around the target.**  Single-site moves can be undone, so a
certificate accepted for the pair `(b, a)` also bounds the barrier of the walks from `a` to
`b`. -/
theorem bverify_sound_rev (c : BCert n k) (I : PairInstance n k) (a b : Config n k) (L : ℚ)
    (hv : bverify c I b a L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m) (h0 : p 0 = a) (hm : p m = b) :
    ∃ j, j ≤ m ∧ L ≤ I.energy (p j) := by
  have hq : IsWalk SingleSite (fun j => p (m - j)) m :=
    isWalk_reverse (fun _ _ => singleSite_symm) hp
  obtain ⟨j, -, hL⟩ := bverify_sound c I b a L hv (fun j => p (m - j)) m hq
    (by simpa using hm) (by simpa using h0)
  exact ⟨m - j, Nat.sub_le m j, hL⟩

/-- **Soundness for real energies.**  If the rational instance lies termwise below a real pairwise
model (every table entry rounded down), an accepted barrier certificate bounds the barrier of the
real model: every walk of single-site moves from `a` to `b` visits a configuration of real energy
at least `L`. -/
theorem bverify_sound_real (c : BCert n k) (I : PairInstance n k) (a b : Config n k) (L : ℚ)
    (hv : bverify c I a b L = true) (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (hh : ∀ i s, (I.h i s : ℝ) ≤ M.h i s) (hJ : ∀ i j s t, (I.J i j s t : ℝ) ≤ M.J i j s t)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m) (h0 : p 0 = a) (hm : p m = b) :
    ∃ j, j ≤ m ∧ (L : ℝ) ≤ M.energy (p j) := by
  obtain ⟨j, -, hj, hL⟩ := cutVerify_sound SingleSite boxAdjacent boxAdjacent_of_singleSite
    (fun w B => verify w I B L) (fun x => (L : ℝ) ≤ M.energy x)
    (fun w B h x hx => verify_sound_real w I B L h M hh hJ x hx) c (fullDom n k) a b hv p m hp
    (fun j _ => inBox_fullDom (p j)) h0 hm
  exact ⟨j, hj, hL⟩

/-- **Box cuts are closed under cheap moves.**  If the min-kernel accepts the bound `L` on every
wall box of `D` (the hypothesis of the science division's `box_cut_barrier`), a single-site move
from a configuration of `D` to a configuration of energy below `L` stays in `D`. -/
theorem boxCut_closed (I : PairInstance n k) (D : Dom n k) (L : ℚ) (certs : Fin n → Cert n k)
    (hv : ∀ i, verify (certs i) I (wallBox D i) L = true) {x y : Config n k} (hx : InBox D x)
    (hxy : SingleSite x y) (hE : I.energy y < L) : InBox D y := by
  by_contra hy
  obtain ⟨i, hi⟩ := mem_wallBox_of_exit hx hy hxy
  exact absurd (verify_sound (certs i) I (wallBox D i) L (hv i) y hi) (not_le.mpr hE)

/-! ### Part 5. Barrier certificates on the residual kernel `verifyR` -/

/-- **Residual barrier certificates**: cut trees whose `wall` leaves carry certificates of the
residual kernel. -/
abbrev RBCert (n k : ℕ) : Type := CutTree (RCert n k) n k

/-- **The residual barrier checker**: as `bverify`, with the residual kernel `verifyR` on the wall
boxes. -/
def bverifyR (c : RBCert n k) (P : RProblem n k) (a b : Config n k) (L : ℚ) : Bool :=
  cutVerify boxAdjacent (fun w B => verifyR w P B L) c (fullDom n k) a b

/-- **Soundness of the residual barrier checker.**  If `bverifyR c P a b L = true`, every walk of
single-site moves from `a` to `b` visits a configuration whose true energy `E + g` is at least
`L` — the same configuration for every residual `g` with the bounded differences whose values at
the anchors are at least the published ones. -/
theorem bverifyR_sound (c : RBCert n k) (P : RProblem n k) (a b : Config n k) (L : ℚ)
    (hv : bverifyR c P a b L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m) (h0 : p 0 = a) (hm : p m = b) :
    ∃ j, j ≤ m ∧ ∀ g : Config n k → ℝ, ResidualLowerClass P g →
      (L : ℝ) ≤ (P.base.energy (p j) : ℝ) + g (p j) := by
  obtain ⟨j, -, hj, hL⟩ := cutVerify_sound SingleSite boxAdjacent boxAdjacent_of_singleSite
    (fun w B => verifyR w P B L)
    (fun x => ∀ g : Config n k → ℝ, ResidualLowerClass P g →
      (L : ℝ) ≤ (P.base.energy x : ℝ) + g x)
    (fun w B h x hx g hg => verifyR_sound_lower w P B L h g hg x hx) c (fullDom n k) a b hv p m hp
    (fun j _ => inBox_fullDom (p j)) h0 hm
  exact ⟨j, hj, hL⟩

/-- **Height of the barrier above the start.**  If the residual barrier checker accepts and
`u` bounds the residual at `a` from above, the true energy climbs at least `L - (E a + u)` above
the true energy of `a` on every walk of single-site moves from `a` to `b`. -/
theorem bverifyR_height (c : RBCert n k) (P : RProblem n k) (a b : Config n k) (L : ℚ)
    (hv : bverifyR c P a b L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m) (h0 : p 0 = a) (hm : p m = b) :
    ∃ j, j ≤ m ∧ ∀ (g : Config n k → ℝ) (u : ℚ), ResidualLowerClass P g → g a ≤ (u : ℝ) →
      ((L - (P.base.energy a + u) : ℚ) : ℝ) ≤
        ((P.base.energy (p j) : ℝ) + g (p j)) - ((P.base.energy a : ℝ) + g a) := by
  obtain ⟨j, hj, hL⟩ := bverifyR_sound c P a b L hv p m hp h0 hm
  refine ⟨j, hj, fun g u hg hu => ?_⟩
  have h := hL g hg
  push_cast
  linarith

/-- **Certified kinetic trap (tree form of `certified_trap_height`).**  If the walk starts at an
evaluated anchor `(a, v)` and the residual barrier checker accepts, then for every residual of the
class (bounded differences, published anchor values) the true energy climbs at least
`L - (E a + v)` above the true energy of the start before the walk reaches `b`. -/
theorem bverifyR_trap_height (c : RBCert n k) (P : RProblem n k) (b : Config n k) (L : ℚ)
    (av : Config n k × ℚ) (hav : av ∈ P.anchors) (hv : bverifyR c P av.1 b L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m) (h0 : p 0 = av.1) (hm : p m = b) :
    ∃ j, j ≤ m ∧ ∀ g : Config n k → ℝ, ResidualClass P g →
      ((L - (P.base.energy av.1 + av.2) : ℚ) : ℝ) ≤
        ((P.base.energy (p j) : ℝ) + g (p j)) - ((P.base.energy (p 0) : ℝ) + g (p 0)) := by
  obtain ⟨j, hj, h⟩ := bverifyR_height c P av.1 b L hv p m hp h0 hm
  refine ⟨j, hj, fun g hg => ?_⟩
  rw [h0]
  exact h g av.2 hg.lower (hg.2 av hav).le

/-- **Top-level residual barrier checker**: reject inconsistent residual data, then run the
residual barrier checker. -/
def bverifyRTop (c : RBCert n k) (P : RProblem n k) (a b : Config n k) (L : ℚ) : Bool :=
  decide P.Consistent && bverifyR c P a b L

/-- Acceptance by the top-level residual barrier checker means: consistent residual data and
acceptance by the residual barrier checker. -/
theorem bverifyRTop_eq_true {c : RBCert n k} {P : RProblem n k} {a b : Config n k} {L : ℚ}
    (hv : bverifyRTop c P a b L = true) : P.Consistent ∧ bverifyR c P a b L = true := by
  simpa [bverifyRTop] using hv

/-- **Soundness of the top-level residual barrier checker.**  If it accepts, the published data
are satisfiable (some residual has the bounded differences and the published anchor values), and
every walk of single-site moves from `a` to `b` visits a configuration of true energy at least
`L` for every residual of the lower class. -/
theorem bverifyRTop_sound (c : RBCert n k) (P : RProblem n k) (a b : Config n k) (L : ℚ)
    (hv : bverifyRTop c P a b L = true) :
    (∃ g : Config n k → ℝ, ResidualClass P g) ∧
      ∀ (p : ℕ → Config n k) (m : ℕ), IsWalk SingleSite p m → p 0 = a → p m = b →
        ∃ j, j ≤ m ∧ ∀ g : Config n k → ℝ, ResidualLowerClass P g →
          (L : ℝ) ≤ (P.base.energy (p j) : ℝ) + g (p j) :=
  ⟨(bverifyRTop_eq_true hv).1.nonempty,
    fun p m hp h0 hm => bverifyR_sound c P a b L (bverifyRTop_eq_true hv).2 p m hp h0 hm⟩

/-! ### Part 6. Site-graph products

On the Hamming graph a site may jump to any state.  If site `i` can only move along the edges of
its own move relation `G i` (nearest voxels of a torsion, for instance), fewer boxes are adjacent
and more cuts are accepted: this is what makes coordinate cuts ("certified relaxed scans",
Proposition K2(b) of the science division's report) useful. -/

/-- A move of the site-graph product: one site `i` moves along an edge of its move relation `G i`
and every other site keeps its state. -/
def SiteMove (G : Fin n → Fin k → Fin k → Bool) (x y : Config n k) : Prop :=
  ∃ i : Fin n, G i (x i) (y i) = true ∧ ∀ j, j ≠ i → x j = y j

/-- Whether two configurations are joined by a move of the site-graph product is decidable. -/
instance decidableSiteMove (G : Fin n → Fin k → Fin k → Bool) (x y : Config n k) :
    Decidable (SiteMove G x y) := by
  unfold SiteMove
  infer_instance

/-- **Adjacency of boxes on a site-graph product.**  Some site `i` has an edge of `G i` from a
state of `D i` to a state of `D' i`, and at every other site the two domains share a state. -/
def Dom.AdjacentOn (G : Fin n → Fin k → Fin k → Bool) (D D' : Dom n k) : Prop :=
  ∃ i : Fin n, (∃ s ∈ D i, ∃ t ∈ D' i, G i s t = true) ∧ ∀ j, j ≠ i → ¬ D.SepAt D' j

/-- Adjacency of boxes on a site-graph product is decidable. -/
instance Dom.decidableAdjacentOn (G : Fin n → Fin k → Fin k → Bool) (D D' : Dom n k) :
    Decidable (D.AdjacentOn G D') := by
  unfold Dom.AdjacentOn
  infer_instance

/-- **Adjacency lemma on a site-graph product**, both directions and without side condition: two
boxes contain the two ends of a move if and only if they are adjacent. -/
theorem Dom.adjacentOn_iff (G : Fin n → Fin k → Fin k → Bool) {D D' : Dom n k} :
    D.AdjacentOn G D' ↔ ∃ x y, InBox D x ∧ InBox D' y ∧ SiteMove G x y := by
  constructor
  · rintro ⟨i, ⟨s, hs, t, ht, hG⟩, hrest⟩
    have hc : ∀ j, ∃ c, j ≠ i → c ∈ D j ∧ c ∈ D' j := by
      intro j
      by_cases hj : j = i
      · exact ⟨s, fun h => absurd hj h⟩
      · have h := hrest j hj
        unfold Dom.SepAt at h
        push Not at h
        obtain ⟨c, hc1, hc2⟩ := h
        exact ⟨c, fun _ => ⟨hc1, hc2⟩⟩
    choose c hc using hc
    refine ⟨Function.update c i s, Function.update c i t, fun j => ?_, fun j => ?_, i, ?_, ?_⟩
    · by_cases hj : j = i
      · subst hj
        rw [Function.update_self]
        exact hs
      · rw [Function.update_of_ne hj]
        exact (hc j hj).1
    · by_cases hj : j = i
      · subst hj
        rw [Function.update_self]
        exact ht
      · rw [Function.update_of_ne hj]
        exact (hc j hj).2
    · rw [Function.update_self, Function.update_self]
      exact hG
    · intro j hj
      rw [Function.update_of_ne hj, Function.update_of_ne hj]
  · rintro ⟨x, y, hx, hy, i, hG, hrest⟩
    refine ⟨i, ⟨x i, hx i, y i, hy i, hG⟩, fun j hj hsep => hsep (x j) (hx j) ?_⟩
    rw [hrest j hj]
    exact hy j

/-- Unrestricted single-site moves are the moves of the product of complete site graphs. -/
theorem singleSite_iff_siteMove {x y : Config n k} :
    SingleSite x y ↔ SiteMove (fun _ _ _ => true) x y := by
  unfold SingleSite SiteMove
  simp

/-- With complete site graphs (and at least one site) the adjacency of the site-graph product is
the adjacency used by `bverify`: the Hamming graph is a special case. -/
theorem Dom.adjacentOn_true_iff (hn : 0 < n) {D D' : Dom n k} :
    D.AdjacentOn (fun _ _ _ => true) D' ↔ D.Adjacent D' := by
  rw [Dom.adjacentOn_iff, Dom.adjacent_iff hn]
  simp only [singleSite_iff_siteMove]

/-- **The barrier checker on a site-graph product**: as `bverify`, with the adjacency test of the
move relations `G`. -/
def bverifyOn (G : Fin n → Fin k → Fin k → Bool) (c : BCert n k) (I : PairInstance n k)
    (a b : Config n k) (L : ℚ) : Bool :=
  cutVerify (fun B B' => decide (B.AdjacentOn G B')) (fun w B => verify w I B L) c
    (fullDom n k) a b

/-- **Soundness on a site-graph product.**  If `bverifyOn G c I a b L = true`, every walk from
`a` to `b` whose steps move one site along an edge of its move relation visits a configuration of
energy at least `L`. -/
theorem bverifyOn_sound (G : Fin n → Fin k → Fin k → Bool) (c : BCert n k)
    (I : PairInstance n k) (a b : Config n k) (L : ℚ) (hv : bverifyOn G c I a b L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk (SiteMove G) p m) (h0 : p 0 = a) (hm : p m = b) :
    ∃ j, j ≤ m ∧ L ≤ I.energy (p j) := by
  obtain ⟨j, -, hj, hL⟩ := cutVerify_sound (SiteMove G)
    (fun B B' => decide (B.AdjacentOn G B'))
    (fun B B' x y hx hy h => decide_eq_true ((Dom.adjacentOn_iff G).mpr ⟨x, y, hx, hy, h⟩))
    (fun w B => verify w I B L) (fun x => L ≤ I.energy x)
    (fun w B h x hx => verify_sound w I B L h x hx) c (fullDom n k) a b hv p m hp
    (fun j _ => inBox_fullDom (p j)) h0 hm
  exact ⟨j, hj, hL⟩

/-! ### Part 7. Kernel-evaluated instances (non-vacuity)

Every `… = true` and `… = false` below is proved by `decide +kernel`: the checker, including the
min-kernel on the wall boxes, runs inside Lean's kernel on exact rationals.

#### The double well `ferro` (three binary sites)

`E(000) = 0`, `E(111) = -3/2`; the three configurations with one `1` have energy `7/2`, the three
with two `1`s have energy `3`. -/

/-- Cut tree for the region `{000}` in the format of §2.5 of the science division's report
(`branch` nodes only): the three configurations with a single `1` are wall leaves with the same
payload `w`, the other four configurations are `outside` (three leaves, one of them the box
`11*`). -/
def ferroWellTree {W : Type} (w : W) : CutTree W 3 2 :=
  .branch 0 fun a =>
    if a = 0 then
      .branch 1 fun b =>
        if b = 0 then .branch 2 fun c => if c = 0 then .inside else .wall w
        else .branch 2 fun c => if c = 0 then .wall w else .outside
    else
      .branch 1 fun b =>
        if b = 0 then .branch 2 fun c => if c = 0 then .wall w else .outside
        else .outside

/-- Cut tree for the region "at least two `1`s" (not a box), written with `split` nodes: the
inside leaves are the boxes `11*`, `101`, `011`, the wall leaves the three configurations with a
single `1`, and `000` is the only `outside` leaf. -/
def ferroTopTree {W : Type} (w : W) : CutTree W 3 2 :=
  .split 0 [1]
    (.split 1 [1] .inside (.split 2 [1] .inside (.wall w)))
    (.split 1 [1] (.split 2 [1] .inside (.wall w)) (.split 2 [1] (.wall w) .outside))

/-- A cut tree without a wall: `000` is `inside` and every other configuration is `outside`. -/
def ferroLeakTree : BCert 3 2 :=
  .split 0 [0] (.split 1 [0] (.split 2 [0] .inside .outside) .outside) .outside

/-- The barrier checker accepts the bound `7/2` for the walks from `000` to `111`. -/
theorem ferroWell_verified :
    bverify (ferroWellTree (exhaustive3 ferro)) ferro ![0, 0, 0] ![1, 1, 1] (7 / 2) = true := by
  decide +kernel

/-- **Certified barrier, kernel-evaluated.**  Every walk of single-site moves from `000` to `111`
visits a configuration of energy at least `7/2`. -/
theorem ferroWell_barrier (p : ℕ → Config 3 2) (m : ℕ) (hp : IsWalk SingleSite p m)
    (h0 : p 0 = ![0, 0, 0]) (hm : p m = ![1, 1, 1]) :
    ∃ j, j ≤ m ∧ (7 / 2 : ℚ) ≤ ferro.energy (p j) :=
  bverify_sound _ ferro _ _ (7 / 2) ferroWell_verified p m hp h0 hm

/-- The region of `ferroWellTree` is the single configuration `000`. -/
theorem ferroWell_region : ∀ x : Config 3 2,
    (ferroWellTree (exhaustive3 ferro)).Inside (fullDom 3 2) x ↔ x = ![0, 0, 0] := by
  decide +kernel

/-- **The trap of the science division's `ferro_barrier`, through the tree checker.**  Every walk
of single-site moves from `000` to any other configuration visits a configuration of energy at
least `7/2`. -/
theorem ferroWell_trap (p : ℕ → Config 3 2) (m : ℕ) (hp : IsWalk SingleSite p m)
    (h0 : p 0 = ![0, 0, 0]) (hm : p m ≠ ![0, 0, 0]) :
    ∃ j, j ≤ m ∧ (7 / 2 : ℚ) ≤ ferro.energy (p j) := by
  have hv : bcheck (ferroWellTree (exhaustive3 ferro)) ferro (7 / 2) = true := by decide +kernel
  exact bcheck_sound _ ferro (7 / 2) hv p m hp ((ferroWell_region _).mpr h0)
    fun h => hm ((ferroWell_region _).mp h)

/-- The barrier checker accepts the bound `7/2` for the walks from `111` to `000`, with a region
that is not a box. -/
theorem ferroTop_verified :
    bverify (ferroTopTree (exhaustive3 ferro)) ferro ![1, 1, 1] ![0, 0, 0] (7 / 2) = true := by
  decide +kernel

/-- The barrier checker rejects the same certificate for the (false) bound `4`. -/
theorem ferroTop_rejects_bound :
    bverify (ferroTopTree (exhaustive3 ferro)) ferro ![1, 1, 1] ![0, 0, 0] 4 = false := by
  decide +kernel

/-- The barrier checker rejects the tree without a wall: its `inside` box `000` is adjacent to an
`outside` box. -/
theorem ferroLeak_rejected : bverify ferroLeakTree ferro ![0, 0, 0] ![1, 1, 1] 1000 = false := by
  decide +kernel

/-- Check 2 is what rejects it: with the adjacency test switched off the same tree is accepted
for the bound `1000`, which no configuration reaches. -/
theorem ferroLeak_needs_adjacency :
    cutVerify (fun _ _ => false) (fun w B => verify w ferro B 1000) ferroLeakTree (fullDom 3 2)
        ![0, 0, 0] ![1, 1, 1] = true ∧ ∀ x : Config 3 2, ferro.energy x < 1000 := by
  decide +kernel

/-- Check 3 rejects a start that is not in an `inside` box (`111` for `ferroWellTree`) and a
target that is in an `inside` box (`110` for `ferroTopTree`). -/
theorem ferro_rejects_endpoints :
    bverify (ferroWellTree (exhaustive3 ferro)) ferro ![1, 1, 1] ![0, 0, 0] (7 / 2) = false ∧
      bverify (ferroTopTree (exhaustive3 ferro)) ferro ![1, 1, 1] ![1, 1, 0] (7 / 2) = false := by
  decide +kernel

/-- `ferroWellTree` below a `split` node whose second child has an empty box, labelled
`outside`. -/
def ferroEmptyLeafTree : BCert 3 2 :=
  .split 0 [0, 1] (ferroWellTree (exhaustive3 ferro)) .outside

/-- A leaf with an empty box is harmless: the barrier checker accepts the certificate. -/
theorem ferroEmptyLeaf_verified :
    bverify ferroEmptyLeafTree ferro ![0, 0, 0] ![1, 1, 1] (7 / 2) = true := by
  decide +kernel

/-- The non-emptiness clause of `Dom.Adjacent` is what accepts it: with the test "at most one
separating site" alone, the box `000` and the empty box count as adjacent and the same certificate
is rejected. -/
theorem ferroEmptyLeaf_literal_rejected :
    cutVerify (fun B B' => decide ((Finset.univ.filter fun i => B.SepAt B' i).card ≤ 1))
      (fun w B => verify w ferro B (7 / 2)) ferroEmptyLeafTree (fullDom 3 2)
      ![0, 0, 0] ![1, 1, 1] = false := by
  decide +kernel

/-- The walk `111 → 110 → 100 → 000`. -/
def ferroPath : ℕ → Config 3 2 := fun j =>
  if j = 0 then ![1, 1, 1] else if j = 1 then ![1, 1, 0] else if j = 2 then ![1, 0, 0]
  else ![0, 0, 0]

/-- `ferroPath` is a walk of single-site moves with three steps. -/
theorem ferroPath_isWalk : IsWalk SingleSite ferroPath 3 := by
  unfold IsWalk
  decide +kernel

/-- No configuration on `ferroPath` has energy above `7/2`. -/
theorem ferroPath_energy : ∀ j, j ≤ 3 → ferro.energy (ferroPath j) ≤ 7 / 2 := by
  decide +kernel

/-- **The certified barrier is exact.**  Every walk of single-site moves from `111` to `000`
visits a configuration of energy at least `7/2`, and some walk never exceeds `7/2`: the barrier
between `111` and `000` is exactly `7/2`. -/
theorem ferro_barrier_exact :
    (∀ (p : ℕ → Config 3 2) (m : ℕ), IsWalk SingleSite p m → p 0 = ![1, 1, 1] →
        p m = ![0, 0, 0] → ∃ j, j ≤ m ∧ (7 / 2 : ℚ) ≤ ferro.energy (p j)) ∧
      ∃ (p : ℕ → Config 3 2) (m : ℕ), IsWalk SingleSite p m ∧ p 0 = ![1, 1, 1] ∧
        p m = ![0, 0, 0] ∧ ∀ j, j ≤ m → ferro.energy (p j) ≤ 7 / 2 :=
  ⟨fun p m hp h0 hm => bverify_sound _ ferro _ _ (7 / 2) ferroTop_verified p m hp h0 hm,
    ferroPath, 3, ferroPath_isWalk, rfl, rfl, ferroPath_energy⟩

/-- Cut tree below the root box "site `2` frozen at `0`": `00` inside, `10` and `01` wall, `11`
outside (states of the sites `0` and `1`). -/
def ferroFrozenTree : BCert 3 2 :=
  .branch 0 fun a => .branch 1 fun b =>
    if a = 0 ∧ b = 0 then .inside
    else if a = 1 ∧ b = 1 then .outside
    else .wall (exhaustive3 ferro)

/-- The barrier checker accepts the bound `7/2` below the root box in which site `2` is frozen. -/
theorem ferroFrozen_verified :
    bverifyIn ferroFrozenTree ferro ((fullDom 3 2).fix 2 0) ![0, 0, 0] ![1, 1, 0] (7 / 2) =
      true := by
  decide +kernel

/-- **A barrier of a restricted dynamics.**  Every walk of single-site moves from `000` to `110`
that never moves site `2` visits a configuration of energy at least `7/2`. -/
theorem ferroFrozen_barrier (p : ℕ → Config 3 2) (m : ℕ) (hp : IsWalk SingleSite p m)
    (hD : ∀ j, j ≤ m → InBox ((fullDom 3 2).fix 2 0) (p j))
    (h0 : p 0 = ![0, 0, 0]) (hm : p m = ![1, 1, 0]) :
    ∃ j, j ≤ m ∧ (7 / 2 : ℚ) ≤ ferro.energy (p j) :=
  bverifyIn_sound _ ferro _ _ _ (7 / 2) ferroFrozen_verified p m hp hD h0 hm

/-! #### A barrier that no box cut certifies (`maze`, four binary sites)

`E(x) = x₁ + x₂ + x₃ - x₀x₁ + 2x₀x₂ - 2x₁x₂ - 2x₂x₃`.  The configurations `0000`, `1000`, `1100`
(energy `0`) form the basin of `0000`; its seven neighbours have energy at least `1`; the target
`1111` has energy `0`.  The barrier between `0000` and `1111` is exactly `1`.  The basin is not a
box, and every box that contains one of the two endpoints and not the other has a configuration
of energy at most `0` in one of its wall boxes. -/

/-- The instance `maze` on four binary sites. -/
def maze : PairInstance 4 2 where
  h := fun i s => if s = 1 ∧ i ≠ 0 then 1 else 0
  J := fun i j s t =>
    if s = 1 ∧ t = 1 then
      (if i = 0 ∧ j = 1 then -1 else if i = 0 ∧ j = 2 then 2 else if i = 1 ∧ j = 2 then -2
        else if i = 2 ∧ j = 3 then -2 else 0)
    else 0

/-- Exhaustive min-kernel certificate for four binary sites: branch on every site, exact
leaves. -/
def exhaustive4 (I : PairInstance 4 2) : Cert 4 2 :=
  .branch 0 fun a => .branch 1 fun b => .branch 2 fun c => .branch 3 fun d =>
    .leaf (fun i => I.h i (![a, b, c, d] i))
      (fun i j => (I.J i j (![a, b, c, d] i) (![a, b, c, d] j) +
        I.J j i (![a, b, c, d] j) (![a, b, c, d] i)) / 2)
      (fun _ _ _ => 0)

/-- Cut tree for the basin `{0000, 1000, 1100}` of `maze`: inside leaves `*000` and `1100`, wall
leaves `**01`, `1110`, `*010`, `0100`, outside leaves `**11` and `0110`. -/
def mazeCut : BCert 4 2 :=
  .split 3 [1]
    (.split 2 [1] .outside (.wall (exhaustive4 maze)))
    (.split 2 [1]
      (.split 1 [1] (.split 0 [1] (.wall (exhaustive4 maze)) .outside) (.wall (exhaustive4 maze)))
      (.split 1 [1] (.split 0 [1] .inside (.wall (exhaustive4 maze))) .inside))

/-- The barrier checker accepts the bound `1` for the walks from `0000` to `1111` in `maze`. -/
theorem maze_verified : bverify mazeCut maze ![0, 0, 0, 0] ![1, 1, 1, 1] 1 = true := by
  decide +kernel

/-- The walk `0000 → 0100 → 0110 → 0111 → 1111`. -/
def mazePath : ℕ → Config 4 2 := fun j =>
  if j = 0 then ![0, 0, 0, 0] else if j = 1 then ![0, 1, 0, 0] else if j = 2 then ![0, 1, 1, 0]
  else if j = 3 then ![0, 1, 1, 1] else ![1, 1, 1, 1]

/-- `mazePath` is a walk of single-site moves with four steps. -/
theorem mazePath_isWalk : IsWalk SingleSite mazePath 4 := by
  unfold IsWalk
  decide +kernel

/-- No configuration on `mazePath` has energy above `1`. -/
theorem mazePath_energy : ∀ j, j ≤ 4 → maze.energy (mazePath j) ≤ 1 := by
  decide +kernel

/-- **The cut tree certifies the exact barrier of `maze`.**  Every walk of single-site moves from
`0000` to `1111` visits a configuration of energy at least `1`, and some walk never exceeds
`1`. -/
theorem maze_barrier_exact :
    (∀ (p : ℕ → Config 4 2) (m : ℕ), IsWalk SingleSite p m → p 0 = ![0, 0, 0, 0] →
        p m = ![1, 1, 1, 1] → ∃ j, j ≤ m ∧ (1 : ℚ) ≤ maze.energy (p j)) ∧
      ∃ (p : ℕ → Config 4 2) (m : ℕ), IsWalk SingleSite p m ∧ p 0 = ![0, 0, 0, 0] ∧
        p m = ![1, 1, 1, 1] ∧ ∀ j, j ≤ m → maze.energy (p j) ≤ 1 :=
  ⟨fun p m hp h0 hm => bverify_sound _ maze _ _ 1 maze_verified p m hp h0 hm,
    mazePath, 4, mazePath_isWalk, rfl, rfl, mazePath_energy⟩

/-- **No box cut around the start beats the trivial bound.**  If the min-kernel accepts the bound
`L` on every wall box of a box that contains `0000` and not `1111` (the hypotheses of
`box_cut_barrier`), then `L ≤ 0`, the energy of both endpoints. -/
theorem maze_boxCut_start_le (D : Dom 4 2) (L : ℚ) (certs : Fin 4 → Cert 4 2)
    (hv : ∀ i, verify (certs i) maze (wallBox D i) L = true)
    (ha : InBox D ![0, 0, 0, 0]) (hb : ¬ InBox D ![1, 1, 1, 1]) : L ≤ 0 := by
  by_contra hL
  have step : ∀ x y : Config 4 2, InBox D x → SingleSite x y → maze.energy y ≤ 0 → InBox D y :=
    fun x y hx hxy hE => boxCut_closed maze D L certs hv hx hxy (lt_of_le_of_lt hE (not_le.mp hL))
  have h1 : InBox D ![1, 0, 0, 0] := step _ _ ha (by decide +kernel) (by decide +kernel)
  have h2 : InBox D ![1, 1, 0, 0] := step _ _ h1 (by decide +kernel) (by decide +kernel)
  have h3 : InBox D ![0, 1, 0, 0] := inBox_mix h2 ha (by decide +kernel)
  have h4 : InBox D ![0, 1, 1, 0] := step _ _ h3 (by decide +kernel) (by decide +kernel)
  have h5 : InBox D ![0, 1, 1, 1] := step _ _ h4 (by decide +kernel) (by decide +kernel)
  exact hb (step _ _ h5 (by decide +kernel) (by decide +kernel))

/-- **No box cut around the target beats the trivial bound either.**  If the min-kernel accepts
the bound `L` on every wall box of a box that contains `1111` and not `0000`, then `L ≤ 0`. -/
theorem maze_boxCut_target_le (D : Dom 4 2) (L : ℚ) (certs : Fin 4 → Cert 4 2)
    (hv : ∀ i, verify (certs i) maze (wallBox D i) L = true)
    (hb : InBox D ![1, 1, 1, 1]) (ha : ¬ InBox D ![0, 0, 0, 0]) : L ≤ 0 := by
  by_contra hL
  have step : ∀ x y : Config 4 2, InBox D x → SingleSite x y → maze.energy y ≤ 0 → InBox D y :=
    fun x y hx hxy hE => boxCut_closed maze D L certs hv hx hxy (lt_of_le_of_lt hE (not_le.mp hL))
  have h1 : InBox D ![0, 1, 1, 1] := step _ _ hb (by decide +kernel) (by decide +kernel)
  have h2 : InBox D ![0, 1, 1, 0] := step _ _ h1 (by decide +kernel) (by decide +kernel)
  have h3 : InBox D ![1, 1, 1, 0] := inBox_mix h2 hb (by decide +kernel)
  have h4 : InBox D ![1, 1, 0, 0] := step _ _ h3 (by decide +kernel) (by decide +kernel)
  have h5 : InBox D ![1, 0, 0, 0] := step _ _ h4 (by decide +kernel) (by decide +kernel)
  exact ha (step _ _ h5 (by decide +kernel) (by decide +kernel))

/-! #### The residual kernel: `ferroResidual`

Bounded differences `1/4` per site and one evaluated anchor, `g(000) = 0`.  The anchored energy of
a configuration with a single `1` is `7/2 - 1/4 = 13/4`. -/

/-- The top-level residual barrier checker accepts the bound `13/4` for the walks from the anchor
`000` to `111`. -/
theorem ferroWellR_verified :
    bverifyRTop
      (ferroWellTree (.anchor 0 (exhaustive3 (ferro.anchored (fun _ => 1 / 4) ![0, 0, 0]))))
      ferroResidual ![0, 0, 0] ![1, 1, 1] (13 / 4) = true := by
  decide +kernel

/-- **Certified kinetic trap under an unknown residual, through the tree checker.**  For every
residual with bounded differences `1/4` and `g(000) = 0`, every walk of single-site moves from
`000` to `111` climbs at least `13/4` above the true energy of `000`. -/
theorem ferroWellR_trap (g : Config 3 2 → ℝ) (hg : ResidualClass ferroResidual g)
    (p : ℕ → Config 3 2) (m : ℕ) (hp : IsWalk SingleSite p m)
    (h0 : p 0 = ![0, 0, 0]) (hm : p m = ![1, 1, 1]) :
    ∃ j, j ≤ m ∧ ((13 / 4 : ℚ) : ℝ) ≤
      ((ferro.energy (p j) : ℝ) + g (p j)) - ((ferro.energy (p 0) : ℝ) + g (p 0)) := by
  obtain ⟨j, hj, h⟩ := bverifyR_trap_height _ ferroResidual ![1, 1, 1] (13 / 4) (![0, 0, 0], 0)
    (by simp [ferroResidual]) (bverifyRTop_eq_true ferroWellR_verified).2 p m hp h0 hm
  refine ⟨j, hj, ?_⟩
  have h' := h g hg
  have e : ferro.energy ![0, 0, 0] = 0 := by decide +kernel
  have e' : ferroResidual.base = ferro := rfl
  rw [e'] at h'
  simp only [e] at h'
  norm_num at h' ⊢
  linarith

/-- The top-level residual barrier checker accepts the bound `13/4` for the walks from `111` to
`000`, with the region "at least two `1`s". -/
theorem ferroTopR_verified :
    bverifyRTop
      (ferroTopTree (.anchor 0 (exhaustive3 (ferro.anchored (fun _ => 1 / 4) ![0, 0, 0]))))
      ferroResidual ![1, 1, 1] ![0, 0, 0] (13 / 4) = true := by
  decide +kernel

/-- **A robust barrier.**  For every residual with bounded differences `1/4` and `g(000) ≥ 0`,
every walk of single-site moves from `111` to `000` visits a configuration of true energy at
least `13/4`. -/
theorem ferroTopR_barrier (p : ℕ → Config 3 2) (m : ℕ) (hp : IsWalk SingleSite p m)
    (h0 : p 0 = ![1, 1, 1]) (hm : p m = ![0, 0, 0]) :
    ∃ j, j ≤ m ∧ ∀ g : Config 3 2 → ℝ, ResidualLowerClass ferroResidual g →
      ((13 / 4 : ℚ) : ℝ) ≤ (ferro.energy (p j) : ℝ) + g (p j) :=
  (bverifyRTop_sound _ ferroResidual _ _ (13 / 4) ferroTopR_verified).2 p m hp h0 hm

/-! #### A certified relaxed scan on a site-graph product (`scan`, two sites with three states)

Site `0` is a coordinate with the states `0 — 1 — 2` on a line and a barrier of height `3` at its
middle state; site `1` relaxes: `E(1, t) = 3, 5/2, 3` for `t = 0, 1, 2`.  With nearest-state moves
the barrier between `(0,0)` and `(2,0)` is `5/2`; with unrestricted single-site moves the two
configurations are neighbours. -/

/-- The instance `scan`. -/
def scan : PairInstance 2 3 where
  h := fun i s =>
    if i = 0 then (if s = 1 then 3 else 0) else (if s = 0 then 0 else if s = 1 then 1 / 2 else 2)
  J := fun i j s t => if i = 0 ∧ j = 1 ∧ s = 1 then -(t.val : ℚ) else 0

/-- Nearest-state moves at every site: a site may keep its state or move to a state whose number
differs by one. -/
def pathMove : Fin 2 → Fin 3 → Fin 3 → Bool :=
  fun _ s t => decide (s.val ≤ t.val + 1 ∧ t.val ≤ s.val + 1)

/-- Exhaustive min-kernel certificate for two sites with three states. -/
def exhaustive2 (I : PairInstance 2 3) : Cert 2 3 :=
  .branch 0 fun a => .branch 1 fun b =>
    .leaf (fun i => I.h i (![a, b] i))
      (fun i j => (I.J i j (![a, b] i) (![a, b] j) + I.J j i (![a, b] j) (![a, b] i)) / 2)
      (fun _ _ _ => 0)

/-- The coordinate cut of site `0`: state `0` inside, state `1` wall, state `2` outside. -/
def scanCut : BCert 2 3 :=
  .split 0 [0] .inside (.split 0 [1] (.wall (exhaustive2 scan)) .outside)

/-- On the site-graph product the barrier checker accepts the coordinate cut for the bound
`5/2`. -/
theorem scan_verified : bverifyOn pathMove scanCut scan ![0, 0] ![2, 0] (5 / 2) = true := by
  decide +kernel

/-- On the Hamming graph the same certificate is rejected: the boxes "site `0` in state `0`" and
"site `0` in state `2`" are adjacent there. -/
theorem scan_hamming_rejected : bverify scanCut scan ![0, 0] ![2, 0] (5 / 2) = false := by
  decide +kernel

/-- Rightly so: with unrestricted single-site moves `(0,0)` and `(2,0)` are neighbours, and both
have energy `0`. -/
theorem scan_hamming_direct :
    SingleSite (![0, 0] : Config 2 3) ![2, 0] ∧ scan.energy ![0, 0] = 0 ∧
      scan.energy ![2, 0] = 0 := by
  decide +kernel

/-- The walk `(0,0) → (0,1) → (1,1) → (2,1) → (2,0)`. -/
def scanPath : ℕ → Config 2 3 := fun j =>
  if j = 0 then ![0, 0] else if j = 1 then ![0, 1] else if j = 2 then ![1, 1]
  else if j = 3 then ![2, 1] else ![2, 0]

/-- `scanPath` is a walk of nearest-state moves with four steps. -/
theorem scanPath_isWalk : IsWalk (SiteMove pathMove) scanPath 4 := by
  unfold IsWalk
  decide +kernel

/-- No configuration on `scanPath` has energy above `5/2`. -/
theorem scanPath_energy : ∀ j, j ≤ 4 → scan.energy (scanPath j) ≤ 5 / 2 := by
  decide +kernel

/-- **A certified relaxed scan, kernel-evaluated.**  Every walk of nearest-state moves from
`(0,0)` to `(2,0)` visits a configuration of energy at least `5/2`, and some such walk never
exceeds `5/2`. -/
theorem scan_barrier_exact :
    (∀ (p : ℕ → Config 2 3) (m : ℕ), IsWalk (SiteMove pathMove) p m → p 0 = ![0, 0] →
        p m = ![2, 0] → ∃ j, j ≤ m ∧ (5 / 2 : ℚ) ≤ scan.energy (p j)) ∧
      ∃ (p : ℕ → Config 2 3) (m : ℕ), IsWalk (SiteMove pathMove) p m ∧ p 0 = ![0, 0] ∧
        p m = ![2, 0] ∧ ∀ j, j ≤ m → scan.energy (p j) ≤ 5 / 2 :=
  ⟨fun p m hp h0 hm => bverifyOn_sound pathMove _ scan _ _ (5 / 2) scan_verified p m hp h0 hm,
    scanPath, 4, scanPath_isWalk, rfl, rfl, scanPath_energy⟩

end MetricChain
