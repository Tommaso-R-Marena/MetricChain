import Mathlib
import proofs.Core.Basic
import proofs.Frontiers.Dominance
import proofs.Frontiers.EnvelopeDuality

/-!
# Certificate algebra: a computable verification kernel with a Master Soundness Theorem

This file defines an *executable* checker for lower-bound certificates on the minimum of a
pairwise conformational energy over a product domain, with exact rational arithmetic, and proves
it sound.  It then lifts the kernel to energies with a **non-decomposable residual** known only
through bounded-difference envelopes and evaluated anchors.

## Objects

* `PairInstance n k` — rational one- and two-body tables on `n` sites with `k` states each.
* `Dom n k` — current domains (a list of surviving states per site); `InBox D x`.
* `Cert n k` — certificates, an algebra with four constructors:
  * `leaf u p m` — a dual (reparameterisation) bound: messages `m`, claimed lower bounds `u i`
    on the reparameterised unaries and `p i j` on the reparameterised pair tables;
  * `branch i children` — case split on the state of site `i`;
  * `prune i r t ℓ rest` — dead-end elimination of state `r` at site `i` (dominated by `t`), with
    claimed per-neighbour lower bounds `ℓ j` of the Goldstein link terms;
  * `sum I₁ I₂ L₁ L₂ c₁ c₂` — dual decomposition: `E ≥ E₁ + E₂` termwise on the box, each part
    certified separately (independent components, tree decompositions, relaxations).
* `verify : Cert n k → PairInstance n k → Dom n k → ℚ → Bool` — the kernel.  Every check is a
  comparison of rationals; the verifier never searches and never minimises.

## Master Soundness Theorems

* `verify_sound` : `verify c I D L = true → ∀ x ∈ box D, L ≤ I.energy x`.
* `verifyR_sound` : for a residual problem (pairwise part, bounded-difference constants, evaluated
  anchors) `verifyR c P D L = true → ∀ g ∈ ResidualClass P, ∀ x ∈ box D, L ≤ E x + g x`;
  `verifyR_sound_lower` is the same for the larger class `ResidualLowerClass` in which the
  published anchor values are only lower bounds on the residual.
* `verifyRTop_sound`, `verifyRLowerTop_sound` : the top-level kernels also check the published
  data, so that the statement is never vacuous — `RProblem.Consistent` is exactly non-emptiness
  of `ResidualClass` (`RProblem.consistent_iff_nonempty`), and nonnegative constants suffice for
  `ResidualLowerClass` (`RProblem.lowerClass_nonempty`).
* `verifyITop_sound` : the recommended entry point for residual problems takes *interval* anchor
  data `lo ≤ g x ≤ hi` (`hi` optional); `IProblem.Consistent` is exactly non-emptiness of the
  interval class (`IProblem.consistent_iff_nonempty`), acceptance gives the lower bound on the box
  and certified incumbent values at the anchors, and `verifyRTop` / `verifyRLowerTop` are the
  special cases `[v, v]` and `[v, ∞)` (`verifyITop_ofExact`, `verifyITop_ofLower`).
* `certified_gap` : together with an evaluated anchor in the box this pins the global optimum of
  the true (unknown-residual) energy inside `[L, U]`; `certified_gap_interval` is the version for
  a separately certified upper value.

## Complexity (see `docs/BLUEPRINT.md`)

Each `leaf`, `prune` or `sum` node is checked in time linear in the size of the instance tables
restricted to the current domains; a `branch` node costs one list traversal.  Witness size is
the number of nodes times the table size (`Cert.dataSize` in `ProofComplexity.lean`).
`proofs/Frontiers/ProofComplexity.lean` shows that the `sum` constructor is necessary: without it
certificates can be exponentially larger, also when `sum` nodes are charged for the sub-instances
they embed.
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-! ### Instances, configurations, domains -/

/-- A pairwise instance with rational tables: `h i a` and, for ordered pairs `i ≠ j`, `J i j a b`. -/
structure PairInstance (n k : ℕ) where
  /-- one-body table -/
  h : Fin n → Fin k → ℚ
  /-- two-body table (ordered pairs `i ≠ j`; the diagonal is ignored) -/
  J : Fin n → Fin n → Fin k → Fin k → ℚ

/-- A configuration assigns a state to every site. -/
abbrev Config (n k : ℕ) := Fin n → Fin k

/-- Current domains: the list of surviving states of every site. -/
abbrev Dom (n k : ℕ) := Fin n → List (Fin k)

/-- `x` lies in the box `∏ D`. -/
def InBox (D : Dom n k) (x : Config n k) : Prop := ∀ i, x i ∈ D i

/-- The full box. -/
def fullDom (n k : ℕ) : Dom n k := fun _ => List.finRange k

theorem inBox_fullDom (x : Config n k) : InBox (fullDom n k) x := fun i => List.mem_finRange (x i)

/-- The associated pairwise model (scalars `ℚ`). -/
def PairInstance.toModel (I : PairInstance n k) : PairModel ℚ (Fin n) (fun _ => Fin k) where
  h := I.h
  J := I.J

/-- Total energy of a configuration (exact rational arithmetic). -/
def PairInstance.energy (I : PairInstance n k) (x : Config n k) : ℚ :=
  ∑ i, I.h i (x i) + ∑ i, ∑ j ∈ univ.erase i, I.J i j (x i) (x j)

theorem PairInstance.energy_eq (I : PairInstance n k) (x : Config n k) :
    I.energy x = I.toModel.energy x := rfl

/-- Goldstein link term. -/
def PairInstance.link (I : PairInstance n k) (i : Fin n) (r t : Fin k) (j : Fin n) (s : Fin k) : ℚ :=
  I.J i j r s + I.J j i s r - I.J i j t s - I.J j i s t

/-- Energy difference between two states of one site: exact, context-separable. -/
theorem PairInstance.energy_update_sub (I : PairInstance n k) (x : Config n k) (i : Fin n)
    (r t : Fin k) :
    I.energy (Function.update x i r) - I.energy (Function.update x i t) =
      I.h i r - I.h i t + ∑ j ∈ univ.erase i, I.link i r t j (x j) := by
  have h1 := PairModel.energy_update_sub I.toModel x i r t
  have h2 := PairModel.localE_sub I.toModel x i r t
  rw [h2] at h1
  exact h1

/-! ### Certificates and the kernel -/

/-- Certificates for lower bounds on the minimum energy over a box. -/
inductive Cert (n k : ℕ) : Type
  | leaf (u : Fin n → ℚ) (p : Fin n → Fin n → ℚ) (m : Fin n → Fin n → Fin k → ℚ) : Cert n k
  | branch (i : Fin n) (children : Fin k → Cert n k) : Cert n k
  | prune (i : Fin n) (r t : Fin k) (ℓ : Fin n → ℚ) (rest : Cert n k) : Cert n k
  | sum (I₁ I₂ : PairInstance n k) (L₁ L₂ : ℚ) (c₁ c₂ : Cert n k) : Cert n k

/-- Leaf check: the reparameterised unaries are bounded below by `u i`, the reparameterised
interaction of every unordered pair `{i, j}` (both orientations of the table, messages from both
ends) is bounded below by `p i j + p j i` (stated symmetrically as `2 p i j ≤ …`), and the claimed
values add up to at least `L`. -/
def LeafOK (I : PairInstance n k) (D : Dom n k) (L : ℚ) (u : Fin n → ℚ) (p : Fin n → Fin n → ℚ)
    (m : Fin n → Fin n → Fin k → ℚ) : Prop :=
  (∀ i, ∀ a ∈ D i, u i ≤ I.h i a + ∑ j ∈ univ.erase i, m i j a) ∧
    (∀ i, ∀ j ∈ univ.erase i, ∀ a ∈ D i, ∀ b ∈ D j,
      2 * p i j ≤ I.J i j a b + I.J j i b a - m i j a - m j i b) ∧
      L ≤ ∑ i, u i + ∑ i, ∑ j ∈ univ.erase i, p i j

instance (I : PairInstance n k) (D : Dom n k) (L : ℚ) (u : Fin n → ℚ) (p : Fin n → Fin n → ℚ)
    (m : Fin n → Fin n → Fin k → ℚ) : Decidable (LeafOK I D L u p m) := by
  unfold LeafOK
  refine @instDecidableAnd _ _ ?_ (@instDecidableAnd _ _ ?_ ?_) <;> infer_instance

/-- Prune check: `t` survives, differs from `r`, and the Goldstein margin of `r` against `t`
(with claimed per-neighbour bounds `ℓ`) is at least `margin`. -/
def PruneOK (I : PairInstance n k) (D : Dom n k) (i : Fin n) (r t : Fin k) (ℓ : Fin n → ℚ)
    (margin : ℚ) : Prop :=
  t ∈ D i ∧ t ≠ r ∧ (∀ j ∈ univ.erase i, ∀ s ∈ D j, ℓ j ≤ I.link i r t j s) ∧
    margin ≤ I.h i r - I.h i t + ∑ j ∈ univ.erase i, ℓ j

instance (I : PairInstance n k) (D : Dom n k) (i : Fin n) (r t : Fin k) (ℓ : Fin n → ℚ)
    (margin : ℚ) : Decidable (PruneOK I D i r t ℓ margin) := by
  unfold PruneOK
  refine @instDecidableAnd _ _ ?_ (@instDecidableAnd _ _ ?_ (@instDecidableAnd _ _ ?_ ?_)) <;>
    infer_instance

/-- Sum check: on the current box `I` dominates `I₁ + I₂` termwise and `L ≤ L₁ + L₂`. -/
def SumOK (I I₁ I₂ : PairInstance n k) (D : Dom n k) (L L₁ L₂ : ℚ) : Prop :=
  (∀ i, ∀ a ∈ D i, I₁.h i a + I₂.h i a ≤ I.h i a) ∧
    (∀ i, ∀ j ∈ univ.erase i, ∀ a ∈ D i, ∀ b ∈ D j, I₁.J i j a b + I₂.J i j a b ≤ I.J i j a b) ∧
      L ≤ L₁ + L₂

instance (I I₁ I₂ : PairInstance n k) (D : Dom n k) (L L₁ L₂ : ℚ) :
    Decidable (SumOK I I₁ I₂ D L L₁ L₂) := by
  unfold SumOK
  refine @instDecidableAnd _ _ ?_ (@instDecidableAnd _ _ ?_ ?_) <;> infer_instance

/-- Domain after removing state `r` from site `i`. -/
def Dom.remove (D : Dom n k) (i : Fin n) (r : Fin k) : Dom n k :=
  Function.update D i ((D i).filter fun s => s ≠ r)

/-- Domain after fixing site `i` to state `a`. -/
def Dom.fix (D : Dom n k) (i : Fin n) (a : Fin k) : Dom n k := Function.update D i [a]

/-- **The verification kernel.**  `verify c I D L = true` certifies `L ≤ min_{x ∈ ∏ D} I.energy x`. -/
def verify : Cert n k → PairInstance n k → Dom n k → ℚ → Bool
  | .leaf u p m, I, D, L => decide (LeafOK I D L u p m)
  | .branch i ch, I, D, L => (D i).all fun a => verify (ch a) I (D.fix i a) L
  | .prune i r t ℓ rest, I, D, L =>
      decide (PruneOK I D i r t ℓ 0) && verify rest I (D.remove i r) L
  | .sum I₁ I₂ L₁ L₂ c₁ c₂, I, D, L =>
      decide (SumOK I I₁ I₂ D L L₁ L₂) && verify c₁ I₁ D L₁ && verify c₂ I₂ D L₂

/-- Number of *nodes* of a certificate (leaves, branch nodes, prune nodes and sum nodes; a `sum`
node additionally carries two full sub-instances, which this count does not charge for).  The
number of leaves actually visited by the kernel is `Cert.visited` in `ProofComplexity.lean`. -/
def Cert.size : Cert n k → ℕ
  | .leaf _ _ _ => 1
  | .branch _ ch => 1 + ∑ a, (ch a).size
  | .prune _ _ _ _ rest => 1 + rest.size
  | .sum _ _ _ _ c₁ c₂ => 1 + c₁.size + c₂.size

/-! ### Soundness of the individual rules -/

theorem inBox_fix {D : Dom n k} {x : Config n k} (hx : InBox D x) (i : Fin n) :
    InBox (D.fix i (x i)) x := by
  intro j
  unfold Dom.fix
  by_cases hj : j = i
  · subst hj
    simp
  · rw [Function.update_of_ne hj]
    exact hx j

theorem inBox_remove_of_ne {D : Dom n k} {x : Config n k} (hx : InBox D x) (i : Fin n) (r : Fin k)
    (hne : x i ≠ r) : InBox (D.remove i r) x := by
  intro j
  unfold Dom.remove
  by_cases hj : j = i
  · subst hj
    simp only [Function.update_self]
    exact List.mem_filter.mpr ⟨hx j, by simpa using hne⟩
  · rw [Function.update_of_ne hj]
    exact hx j

theorem inBox_remove_update {D : Dom n k} {x : Config n k} (hx : InBox D x) (i : Fin n)
    (r t : Fin k) (ht : t ∈ D i) (htr : t ≠ r) : InBox (D.remove i r) (Function.update x i t) := by
  intro j
  unfold Dom.remove
  by_cases hj : j = i
  · subst hj
    simp only [Function.update_self]
    exact List.mem_filter.mpr ⟨ht, by simpa using htr⟩
  · rw [Function.update_of_ne hj, Function.update_of_ne hj]
    exact hx j

/-- Swapping the roles of the two indices in a sum over ordered pairs of distinct sites. -/
theorem sum_erase_swap {α : Type*} [Fintype α] [DecidableEq α] (F : α → α → ℚ) :
    ∑ i, ∑ j ∈ univ.erase i, F j i = ∑ i, ∑ j ∈ univ.erase i, F i j := by
  have h : ∀ G : α → α → ℚ,
      ∑ i, ∑ j ∈ univ.erase i, G i j = ∑ i, ∑ j, if j ≠ i then G i j else 0 := by
    intro G
    apply Finset.sum_congr rfl
    intro i _
    rw [← Finset.sum_filter]
    congr 1
    ext j
    simp [Finset.mem_erase]
  rw [h (fun i j => F j i), h F, Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  by_cases hij : i = j
  · simp [hij]
  · have hji : j ≠ i := fun e => hij e.symm
    simp [hij, hji]

/-- Soundness of the dual (reparameterisation) leaf. -/
theorem leaf_sound (I : PairInstance n k) (D : Dom n k) (L : ℚ) (u : Fin n → ℚ)
    (p : Fin n → Fin n → ℚ) (m : Fin n → Fin n → Fin k → ℚ) (h : LeafOK I D L u p m)
    (x : Config n k) (hx : InBox D x) : L ≤ I.energy x := by
  obtain ⟨hu, hp, hL⟩ := h
  have h1 : ∑ i, u i ≤ ∑ i, (I.h i (x i) + ∑ j ∈ univ.erase i, m i j (x i)) :=
    Finset.sum_le_sum fun i _ => hu i (x i) (hx i)
  have h2 : ∑ i, ∑ j ∈ univ.erase i, 2 * p i j ≤
      ∑ i, ∑ j ∈ univ.erase i,
        (I.J i j (x i) (x j) + I.J j i (x j) (x i) - m i j (x i) - m j i (x j)) :=
    Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j hj =>
      hp i j hj (x i) (hx i) (x j) (hx j)
  have hswapJ := sum_erase_swap (fun i j => I.J i j (x i) (x j))
  have hswapm := sum_erase_swap (fun i j => m i j (x i))
  have h3 : ∑ i, ∑ j ∈ univ.erase i,
        (I.J i j (x i) (x j) + I.J j i (x j) (x i) - m i j (x i) - m j i (x j)) =
      2 * ∑ i, ∑ j ∈ univ.erase i, (I.J i j (x i) (x j) - m i j (x i)) := by
    simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib]
    rw [hswapJ, hswapm]
    ring
  have h4 : ∑ i, ∑ j ∈ univ.erase i, 2 * p i j = 2 * ∑ i, ∑ j ∈ univ.erase i, p i j := by
    simp only [Finset.mul_sum]
  have h5 : ∑ i, (I.h i (x i) + ∑ j ∈ univ.erase i, m i j (x i)) +
      ∑ i, ∑ j ∈ univ.erase i, (I.J i j (x i) (x j) - m i j (x i)) = I.energy x := by
    unfold PairInstance.energy
    simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib]
    ring
  linarith

/-- Soundness of the dominance step: replacing the dominated state lowers the energy by at least
the certified margin. -/
theorem prune_step (I : PairInstance n k) (D : Dom n k) (i : Fin n) (r t : Fin k) (ℓ : Fin n → ℚ)
    (margin : ℚ) (h : PruneOK I D i r t ℓ margin) (x : Config n k) (hx : InBox D x)
    (hxr : x i = r) : I.energy (Function.update x i t) + margin ≤ I.energy x := by
  obtain ⟨_, _, hℓ, hmargin⟩ := h
  have hx' : Function.update x i r = x := by
    rw [← hxr]
    exact Function.update_eq_self i x
  have h1 := I.energy_update_sub x i r t
  rw [hx'] at h1
  have h2 : ∑ j ∈ univ.erase i, ℓ j ≤ ∑ j ∈ univ.erase i, I.link i r t j (x j) :=
    Finset.sum_le_sum fun j hj => hℓ j hj (x j) (hx j)
  linarith

/-- Soundness of dual decomposition. -/
theorem sum_step (I I₁ I₂ : PairInstance n k) (D : Dom n k) (L L₁ L₂ : ℚ)
    (h : SumOK I I₁ I₂ D L L₁ L₂) (x : Config n k) (hx : InBox D x) :
    I₁.energy x + I₂.energy x ≤ I.energy x := by
  obtain ⟨hh, hJ, _⟩ := h
  unfold PairInstance.energy
  have h1 : ∑ i, (I₁.h i (x i) + I₂.h i (x i)) ≤ ∑ i, I.h i (x i) :=
    Finset.sum_le_sum fun i _ => hh i (x i) (hx i)
  have h2 : ∑ i, ∑ j ∈ univ.erase i, (I₁.J i j (x i) (x j) + I₂.J i j (x i) (x j)) ≤
      ∑ i, ∑ j ∈ univ.erase i, I.J i j (x i) (x j) :=
    Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j hj =>
      hJ i j hj (x i) (hx i) (x j) (hx j)
  simp only [Finset.sum_add_distrib] at h1 h2
  linarith

/-! ### Master Soundness Theorem (decomposable energies) -/

/-- **Master Soundness Theorem.**  If the kernel accepts certificate `c` for instance `I`,
domains `D` and bound `L`, then `L` is a lower bound on the energy of *every* configuration in
the box `∏ D`. -/
theorem verify_sound : ∀ (c : Cert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ),
    verify c I D L = true → ∀ x, InBox D x → L ≤ I.energy x := by
  intro c
  induction c with
  | leaf u p m =>
    intro I D L hv x hx
    simp only [verify, decide_eq_true_eq] at hv
    exact leaf_sound I D L u p m hv x hx
  | branch i ch ih =>
    intro I D L hv x hx
    simp only [verify, List.all_eq_true] at hv
    exact ih (x i) I (D.fix i (x i)) L (hv (x i) (hx i)) x (inBox_fix hx i)
  | prune i r t ℓ rest ih =>
    intro I D L hv x hx
    simp only [verify, Bool.and_eq_true, decide_eq_true_eq] at hv
    obtain ⟨hp, hrest⟩ := hv
    by_cases hxr : x i = r
    · have h1 := ih I (D.remove i r) L hrest (Function.update x i t)
        (inBox_remove_update hx i r t hp.1 hp.2.1)
      have h2 := prune_step I D i r t ℓ 0 hp x hx hxr
      linarith
    · exact ih I (D.remove i r) L hrest x (inBox_remove_of_ne hx i r hxr)
  | sum I₁ I₂ L₁ L₂ c₁ c₂ ih₁ ih₂ =>
    intro I D L hv x hx
    simp only [verify, Bool.and_eq_true, decide_eq_true_eq] at hv
    obtain ⟨⟨hs, h1⟩, h2⟩ := hv
    have e1 := ih₁ I₁ D L₁ h1 x hx
    have e2 := ih₂ I₂ D L₂ h2 x hx
    have e3 := sum_step I I₁ I₂ D L L₁ L₂ hs x hx
    have e4 := hs.2.2
    linarith

/-- Certified optimality gap: a verified lower bound and any feasible witness bracket the
optimal value. -/
theorem certified_optimum (c : Cert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ)
    (hv : verify c I D L = true) (w : Config n k) (hw : InBox D w) :
    (∀ x, InBox D x → L ≤ I.energy x) ∧ L ≤ I.energy w ∧
      ∀ x, InBox D x → I.energy w - I.energy x ≤ I.energy w - L := by
  refine ⟨verify_sound c I D L hv, verify_sound c I D L hv w hw, fun x hx => ?_⟩
  have := verify_sound c I D L hv x hx
  linarith

/-! ### Non-decomposable residuals: anchored kernel -/

/-- A residual problem: the pairwise part, bounded-difference constants `c i` certified for the
residual, and a list of evaluated anchors `(configuration, residual value)`. -/
structure RProblem (n k : ℕ) where
  /-- explicit pairwise part -/
  base : PairInstance n k
  /-- bounded-difference envelope of the residual -/
  c : Fin n → ℚ
  /-- evaluated residual values -/
  anchors : List (Config n k × ℚ)

/-- The class of residuals compatible with the problem data: single-site bounded differences and
agreement with every evaluated anchor. -/
def ResidualClass (P : RProblem n k) (g : Config n k → ℝ) : Prop :=
  (∀ (x : Config n k) (i : Fin n) (s : Fin k), g (Function.update x i s) - g x ≤ (P.c i : ℝ)) ∧
    ∀ p ∈ P.anchors, g p.1 = (p.2 : ℝ)

/-- The weaker class that already suffices for *lower* bounds: single-site bounded differences and
anchor values that are lower bounds on the residual.  Publishing outward-rounded-*down*
floating-point evaluations of the residual as anchor values is therefore sound
(`verifyR_sound_lower`). -/
def ResidualLowerClass (P : RProblem n k) (g : Config n k → ℝ) : Prop :=
  (∀ (x : Config n k) (i : Fin n) (s : Fin k), g (Function.update x i s) - g x ≤ (P.c i : ℝ)) ∧
    ∀ p ∈ P.anchors, (p.2 : ℝ) ≤ g p.1

theorem ResidualClass.lower {P : RProblem n k} {g : Config n k → ℝ} (hg : ResidualClass P g) :
    ResidualLowerClass P g :=
  ⟨hg.1, fun p hp => (hg.2 p hp).ge⟩

/-- Pairwise minorant generated by one anchor: the envelope `c i · [x i ≠ a i]` is absorbed into
the one-body table. -/
def PairInstance.anchored (I : PairInstance n k) (c : Fin n → ℚ) (a : Config n k) :
    PairInstance n k where
  h i s := I.h i s - if s = a i then 0 else c i
  J := I.J

theorem PairInstance.anchored_energy (I : PairInstance n k) (c : Fin n → ℚ) (a x : Config n k) :
    (I.anchored c a).energy x = I.energy x - ∑ i, if x i = a i then 0 else c i := by
  unfold PairInstance.energy PairInstance.anchored
  simp only [Finset.sum_sub_distrib]
  ring

/-- Certificates for residual problems: choose an anchor and hand over to the pairwise kernel,
branch, or prune by *differential* dead-end elimination (margin at least the envelope `c i`). -/
inductive RCert (n k : ℕ) : Type
  | anchor (idx : ℕ) (cert : Cert n k) : RCert n k
  | branch (i : Fin n) (children : Fin k → RCert n k) : RCert n k
  | prune (i : Fin n) (r t : Fin k) (ℓ : Fin n → ℚ) (rest : RCert n k) : RCert n k

/-- The residual kernel. -/
def verifyR : RCert n k → RProblem n k → Dom n k → ℚ → Bool
  | .anchor idx cert, P, D, L =>
      match P.anchors[idx]? with
      | some av => verify cert (P.base.anchored P.c av.1) D (L - av.2)
      | none => false
  | .branch i ch, P, D, L => (D i).all fun a => verifyR (ch a) P (D.fix i a) L
  | .prune i r t ℓ rest, P, D, L =>
      decide (PruneOK P.base D i r t ℓ (P.c i)) && verifyR rest P (D.remove i r) L

/-- Every residual in the (lower) class lies above the anchor's lower envelope. -/
theorem residual_ge_anchor (P : RProblem n k) (g : Config n k → ℝ) (hg : ResidualLowerClass P g)
    (av : Config n k × ℚ) (hav : av ∈ P.anchors) (x : Config n k) :
    (av.2 : ℝ) - ∑ i, (if x i = av.1 i then (0 : ℝ) else (P.c i : ℝ)) ≤ g x := by
  have hadm : Admissible
      (siteEnvelope (σ := fun _ : Fin n => Fin k) fun i s s' => if s = s' then (0 : ℝ) else (P.c i : ℝ)) g := by
    apply admissible_of_single_site
    intro y i s
    by_cases hs : s = y i
    · subst hs
      simp
    · simp only [hs, if_false]
      exact hg.1 y i s
  have h1 := hadm av.1 x
  have h2 := hg.2 av hav
  unfold siteEnvelope at h1
  have h3 : ∑ i, (if av.1 i = x i then (0 : ℝ) else (P.c i : ℝ)) =
      ∑ i, (if x i = av.1 i then (0 : ℝ) else (P.c i : ℝ)) := by
    apply Finset.sum_congr rfl
    intro i _
    by_cases h : x i = av.1 i
    · simp [h]
    · have h' : ¬ av.1 i = x i := fun e => h e.symm
      simp [h, h']
  rw [h3] at h1
  linarith

/-- **Master Soundness Theorem (non-decomposable residuals), lower-bound form.**  If the residual
kernel accepts, then `L` is a lower bound on the *true* energy `E + g` of every configuration in
the box, for every residual `g` with the bounded-difference envelope whose values at the anchors
are *at least* the published ones. -/
theorem verifyR_sound_lower : ∀ (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ),
    verifyR c P D L = true → ∀ g : Config n k → ℝ, ResidualLowerClass P g →
      ∀ x, InBox D x → (L : ℝ) ≤ (P.base.energy x : ℝ) + g x := by
  intro c
  induction c with
  | anchor idx cert =>
    intro P D L hv g hg x hx
    unfold verifyR at hv
    split at hv
    · next av hget =>
      have hmem : av ∈ P.anchors := List.mem_of_getElem? hget
      have h1 := verify_sound cert _ D _ hv x hx
      rw [PairInstance.anchored_energy] at h1
      have h2 := residual_ge_anchor P g hg av hmem x
      have h3 : ((L - av.2 : ℚ) : ℝ) ≤
          ((P.base.energy x - ∑ i, if x i = av.1 i then 0 else P.c i : ℚ) : ℝ) := by
        exact_mod_cast h1
      push_cast at h3
      have h4 : (∑ i, (if x i = av.1 i then (0 : ℝ) else (P.c i : ℝ))) =
          ∑ i, ((if x i = av.1 i then (0 : ℚ) else P.c i : ℚ) : ℝ) := by
        apply Finset.sum_congr rfl
        intro i _
        split_ifs <;> simp
      linarith
    · exact absurd hv (by simp)
  | branch i ch ih =>
    intro P D L hv g hg x hx
    simp only [verifyR, List.all_eq_true] at hv
    exact ih (x i) P (D.fix i (x i)) L (hv (x i) (hx i)) g hg x (inBox_fix hx i)
  | prune i r t ℓ rest ih =>
    intro P D L hv g hg x hx
    simp only [verifyR, Bool.and_eq_true, decide_eq_true_eq] at hv
    obtain ⟨hp, hrest⟩ := hv
    by_cases hxr : x i = r
    · have h1 := ih P (D.remove i r) L hrest g hg (Function.update x i t)
        (inBox_remove_update hx i r t hp.1 hp.2.1)
      have h2 := prune_step P.base D i r t ℓ (P.c i) hp x hx hxr
      have h3 : ((P.base.energy (Function.update x i t) + P.c i : ℚ) : ℝ) ≤
          (P.base.energy x : ℝ) := by exact_mod_cast h2
      push_cast at h3
      have h4 := hg.1 x i t
      linarith
    · exact ih P (D.remove i r) L hrest g hg x (inBox_remove_of_ne hx i r hxr)

/-- **Master Soundness Theorem (non-decomposable residuals).**  If the residual kernel accepts,
then `L` is a lower bound on the *true* energy `E + g` of every configuration in the box, for
every residual `g` compatible with the bounded-difference envelope and the evaluated anchors.
(The statement is vacuous if no such residual exists; the top-level kernel `verifyRTop` rules
that out, see `verifyRTop_sound`.) -/
theorem verifyR_sound (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ)
    (hv : verifyR c P D L = true) (g : Config n k → ℝ) (hg : ResidualClass P g) (x : Config n k)
    (hx : InBox D x) : (L : ℝ) ≤ (P.base.energy x : ℝ) + g x :=
  verifyR_sound_lower c P D L hv g hg.lower x hx

/-- **Certified gap under an unknown residual.**  A verified residual certificate together with an
evaluated anchor `(a, v)` inside the box pins the true global optimum `min (E + g)` inside
`[L, E a + v]`, for every admissible residual. -/
theorem certified_gap (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ)
    (hv : verifyR c P D L = true) (g : Config n k → ℝ) (hg : ResidualClass P g)
    (av : Config n k × ℚ) (hav : av ∈ P.anchors) (hbox : InBox D av.1) :
    (∀ x, InBox D x → (L : ℝ) ≤ (P.base.energy x : ℝ) + g x) ∧
      (P.base.energy av.1 : ℝ) + g av.1 = ((P.base.energy av.1 + av.2 : ℚ) : ℝ) ∧
        (L : ℝ) ≤ ((P.base.energy av.1 + av.2 : ℚ) : ℝ) := by
  have h1 := verifyR_sound c P D L hv g hg
  have h2 : (P.base.energy av.1 : ℝ) + g av.1 = ((P.base.energy av.1 + av.2 : ℚ) : ℝ) := by
    rw [hg.2 av hav]
    push_cast
    ring
  exact ⟨h1, h2, by rw [← h2]; exact h1 av.1 hbox⟩

/-! ### Consistency of the published residual data (non-vacuity of the residual kernel)

`verifyR` checks the *rules*; it does not check that the published residual data describe a
non-empty class.  With a negative envelope constant, or with two anchors whose values differ by
more than the envelope allows, no residual satisfies the data and every statement quantified over
`ResidualClass` holds vacuously.  The decidable predicate `RProblem.Consistent` is *exactly*
non-emptiness of the class (`RProblem.consistent_iff_nonempty`), and the top-level kernel
`verifyRTop` rejects inconsistent data.  If the anchor values are only claimed to be *lower
bounds* on the residual (rounded-down floating-point evaluations), pairwise compatibility is not
required — a legitimate producer could even violate it by rounding — and nonnegativity of the
constants is the only side condition: `verifyRLowerTop`, `verifyRLowerTop_sound`. -/

/-- Consistency of published residual data: nonnegative envelope constants, and anchor values
that are pairwise compatible with the site-additive (weighted Hamming) envelope. -/
def RProblem.Consistent (P : RProblem n k) : Prop :=
  (∀ i, 0 ≤ P.c i) ∧
    ∀ p ∈ P.anchors, ∀ q ∈ P.anchors, p.2 - q.2 ≤ ∑ i, if p.1 i = q.1 i then 0 else P.c i

instance (P : RProblem n k) : Decidable P.Consistent := by
  unfold RProblem.Consistent
  infer_instance

/-- Changing one coordinate changes the weighted Hamming distance to a fixed configuration by at
most the weight of that coordinate. -/
theorem hamming_update_le (c : Fin n → ℝ) (hc : ∀ i, 0 ≤ c i) (a x : Config n k) (i : Fin n)
    (s : Fin k) :
    (∑ j, if a j = x j then (0 : ℝ) else c j) -
      (∑ j, if a j = Function.update x i s j then (0 : ℝ) else c j) ≤ c i := by
  rw [← Finset.sum_sub_distrib, Finset.sum_eq_single i]
  · rw [Function.update_self]
    have := hc i
    split_ifs <;> linarith
  · intro j _ hj
    rw [Function.update_of_ne hj]
    simp
  · intro h
    exact absurd (Finset.mem_univ i) h

/-- Real form of the pairwise anchor condition. -/
theorem RProblem.Consistent.anchor_le {P : RProblem n k} (hP : P.Consistent)
    {p q : Config n k × ℚ} (hp : p ∈ P.anchors) (hq : q ∈ P.anchors) :
    (p.2 : ℝ) - (q.2 : ℝ) ≤ ∑ i, if p.1 i = q.1 i then (0 : ℝ) else (P.c i : ℝ) := by
  have h := hP.2 p hp q hq
  have h' : ((p.2 - q.2 : ℚ) : ℝ) ≤ ((∑ i, if p.1 i = q.1 i then 0 else P.c i : ℚ) : ℝ) := by
    exact_mod_cast h
  push_cast at h'
  have h4 : (∑ i, ((if p.1 i = q.1 i then (0 : ℚ) else P.c i : ℚ) : ℝ)) =
      ∑ i, if p.1 i = q.1 i then (0 : ℝ) else (P.c i : ℝ) := by
    apply Finset.sum_congr rfl
    intro i _
    split_ifs <;> simp
  linarith

/-- **Consistent data describe a non-empty class.**  The McShane lower envelope of the anchors
(the zero function if there are none) has the bounded differences and interpolates the anchors. -/
theorem RProblem.Consistent.nonempty {P : RProblem n k} (hP : P.Consistent) :
    ∃ g : Config n k → ℝ, ResidualClass P g := by
  have hc : ∀ i, (0 : ℝ) ≤ (P.c i : ℝ) := fun i => by exact_mod_cast hP.1 i
  by_cases hne : P.anchors.toFinset.Nonempty
  · let φ : Config n k → Config n k × ℚ → ℝ := fun y p =>
      (p.2 : ℝ) - ∑ j, if p.1 j = y j then (0 : ℝ) else (P.c j : ℝ)
    refine ⟨fun y => P.anchors.toFinset.sup' hne (φ y), ?_, ?_⟩
    · intro x i s
      have key : P.anchors.toFinset.sup' hne (φ (Function.update x i s)) ≤
          P.anchors.toFinset.sup' hne (φ x) + (P.c i : ℝ) := by
        apply Finset.sup'_le
        intro p hp
        have h1 : φ x p ≤ P.anchors.toFinset.sup' hne (φ x) := Finset.le_sup' (φ x) hp
        have h2 := hamming_update_le (fun j => (P.c j : ℝ)) hc p.1 x i s
        show (p.2 : ℝ) - ∑ j, (if p.1 j = Function.update x i s j then (0 : ℝ) else (P.c j : ℝ)) ≤
          P.anchors.toFinset.sup' hne (φ x) + (P.c i : ℝ)
        have h1' : (p.2 : ℝ) - ∑ j, (if p.1 j = x j then (0 : ℝ) else (P.c j : ℝ)) ≤
            P.anchors.toFinset.sup' hne (φ x) := h1
        linarith
      show P.anchors.toFinset.sup' hne (φ (Function.update x i s)) -
        P.anchors.toFinset.sup' hne (φ x) ≤ (P.c i : ℝ)
      linarith
    · intro q hq
      have hq' : q ∈ P.anchors.toFinset := List.mem_toFinset.mpr hq
      show P.anchors.toFinset.sup' hne (φ q.1) = (q.2 : ℝ)
      apply le_antisymm
      · apply Finset.sup'_le
        intro p hp
        have h := hP.anchor_le (List.mem_toFinset.mp hp) hq
        show (p.2 : ℝ) - ∑ j, (if p.1 j = q.1 j then (0 : ℝ) else (P.c j : ℝ)) ≤ (q.2 : ℝ)
        linarith
      · have h1 : φ q.1 q ≤ P.anchors.toFinset.sup' hne (φ q.1) := Finset.le_sup' (φ q.1) hq'
        have h2 : φ q.1 q = (q.2 : ℝ) := by
          show (q.2 : ℝ) - ∑ j, (if q.1 j = q.1 j then (0 : ℝ) else (P.c j : ℝ)) = (q.2 : ℝ)
          simp
        linarith
  · refine ⟨fun _ => 0, ?_, ?_⟩
    · intro x i s
      simpa using hc i
    · intro p hp
      exact absurd ⟨p, List.mem_toFinset.mpr hp⟩ hne

/-- **Inconsistent data describe an empty class** (given that configurations exist at all). -/
theorem RProblem.consistent_of_nonempty (P : RProblem n k) (x₀ : Config n k)
    (h : ∃ g : Config n k → ℝ, ResidualClass P g) : P.Consistent := by
  obtain ⟨g, hg⟩ := h
  constructor
  · intro i
    have h1 := hg.1 x₀ i (x₀ i)
    rw [Function.update_eq_self] at h1
    have h0 : (0 : ℝ) ≤ (P.c i : ℝ) := by linarith
    exact_mod_cast h0
  · intro p hp q hq
    have h1 := residual_ge_anchor P g hg.lower p hp q.1
    rw [hg.2 q hq] at h1
    have h3 : ∑ i, (if q.1 i = p.1 i then (0 : ℝ) else (P.c i : ℝ)) =
        ∑ i, ((if p.1 i = q.1 i then (0 : ℚ) else P.c i : ℚ) : ℝ) := by
      apply Finset.sum_congr rfl
      intro i _
      by_cases hi : p.1 i = q.1 i
      · simp [hi]
      · have hi' : ¬ q.1 i = p.1 i := fun e => hi e.symm
        simp [hi, hi']
    rw [h3] at h1
    have h4 : ((p.2 - q.2 : ℚ) : ℝ) ≤ ((∑ i, if p.1 i = q.1 i then 0 else P.c i : ℚ) : ℝ) := by
      push_cast
      linarith
    exact_mod_cast h4

/-- **Consistency is exactly non-emptiness of the residual class.** -/
theorem RProblem.consistent_iff_nonempty (P : RProblem n k) (x₀ : Config n k) :
    P.Consistent ↔ ∃ g : Config n k → ℝ, ResidualClass P g :=
  ⟨fun h => h.nonempty, P.consistent_of_nonempty x₀⟩

/-- **Top-level residual kernel**: reject inconsistent residual data, then check the rules. -/
def verifyRTop (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ) : Bool :=
  decide P.Consistent && verifyR c P D L

/-- **Master Soundness Theorem of the top-level residual kernel.**  If `verifyRTop` accepts, then
(i) the published data are satisfiable — some residual has the bounded differences and takes
exactly the published anchor values — and (ii) `L` is a lower bound on `E + g` over the box for
*every* residual with the bounded differences whose anchor values are at least the published
ones (in particular for every residual in `ResidualClass`). -/
theorem verifyRTop_sound (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ)
    (hv : verifyRTop c P D L = true) :
    (∃ g : Config n k → ℝ, ResidualClass P g) ∧
      ∀ g : Config n k → ℝ, ResidualLowerClass P g →
        ∀ x, InBox D x → (L : ℝ) ≤ (P.base.energy x : ℝ) + g x := by
  simp only [verifyRTop, Bool.and_eq_true, decide_eq_true_eq] at hv
  exact ⟨hv.1.nonempty, verifyR_sound_lower c P D L hv.2⟩

/-- With nonnegative envelope constants the *lower* class is never empty (a large constant
function belongs to it): when anchor values are only claimed to be lower bounds — e.g.
rounded-down floating-point evaluations — nonnegativity of the constants is the only side
condition. -/
theorem RProblem.lowerClass_nonempty (P : RProblem n k) (hc : ∀ i, 0 ≤ P.c i) :
    ∃ g : Config n k → ℝ, ResidualLowerClass P g := by
  refine ⟨fun _ => (P.anchors.map fun p => |(p.2 : ℝ)|).sum, fun x i s => ?_, fun p hp => ?_⟩
  · have h : (0 : ℝ) ≤ (P.c i : ℝ) := by exact_mod_cast hc i
    simpa using h
  · have h1 : |(p.2 : ℝ)| ≤ (P.anchors.map fun p => |(p.2 : ℝ)|).sum := by
      apply List.single_le_sum
      · intro y hy
        obtain ⟨q, _, rfl⟩ := List.mem_map.mp hy
        exact abs_nonneg _
      · exact List.mem_map.mpr ⟨p, hp, rfl⟩
    exact le_trans (le_abs_self _) h1

/-- **Top-level residual kernel, lower-bound semantics**: the published anchor values are only
claimed to be lower bounds on the residual; the kernel checks the envelope constants and the
rules. -/
def verifyRLowerTop (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ) : Bool :=
  decide (∀ i, 0 ≤ P.c i) && verifyR c P D L

/-- **Master Soundness Theorem, lower-bound semantics.**  If `verifyRLowerTop` accepts, the class
of residuals with the bounded differences whose anchor values are at least the published ones is
non-empty, and `L` bounds `E + g` on the box for every residual of that class. -/
theorem verifyRLowerTop_sound (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ)
    (hv : verifyRLowerTop c P D L = true) :
    (∃ g : Config n k → ℝ, ResidualLowerClass P g) ∧
      ∀ g : Config n k → ℝ, ResidualLowerClass P g →
        ∀ x, InBox D x → (L : ℝ) ≤ (P.base.energy x : ℝ) + g x := by
  simp only [verifyRLowerTop, Bool.and_eq_true, decide_eq_true_eq] at hv
  exact ⟨P.lowerClass_nonempty hv.1, verifyR_sound_lower c P D L hv.2⟩

/-- **Two-sided certified gap with interval anchor data.**  With a lower-class residual and any
certified upper value `u ≥ g a` at a configuration `a` of the box, the true optimum of `E + g`
over the box lies in `[L, E a + u]`. -/
theorem certified_gap_interval (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ)
    (hv : verifyR c P D L = true) (g : Config n k → ℝ) (hg : ResidualLowerClass P g)
    (a : Config n k) (ha : InBox D a) (u : ℚ) (hu : g a ≤ (u : ℝ)) :
    (∀ x, InBox D x → (L : ℝ) ≤ (P.base.energy x : ℝ) + g x) ∧
      (P.base.energy a : ℝ) + g a ≤ ((P.base.energy a + u : ℚ) : ℝ) ∧
        (L : ℝ) ≤ ((P.base.energy a + u : ℚ) : ℝ) := by
  have h1 := verifyR_sound_lower c P D L hv g hg
  have h2 : (P.base.energy a : ℝ) + g a ≤ ((P.base.energy a + u : ℚ) : ℝ) := by
    push_cast
    linarith
  exact ⟨h1, h2, le_trans (h1 a ha) h2⟩

/-! ### Interval anchor data: one top-level kernel for exact, rounded and one-sided evaluations

The two readings of anchor values above (`verifyRTop`: exact; `verifyRLowerTop`: lower bounds) are
the extreme cases of *interval* anchor data: the residual at an anchor is known to lie in
`[lo, hi]`, where `hi` may be absent.  A producer with floating-point evaluations publishes
`[fl - err, fl + err]`.  Consistency of interval data — `lo_p - hi_q ≤ d(x_p, x_q)` for all
ordered pairs with an upper value — is again decidable and *exactly* non-emptiness of the class
(`IProblem.consistent_iff_nonempty`), a legitimate producer always satisfies it, and inconsistent
evaluations are rejected even after rounding. -/

/-- An anchor with interval data: the residual at `x` lies in `[lo, hi]`; `hi = none` means that
only the lower bound is known. -/
structure IAnchor (n k : ℕ) where
  /-- evaluated configuration -/
  x : Config n k
  /-- certified lower value of the residual at `x` -/
  lo : ℚ
  /-- certified upper value of the residual at `x`, if any -/
  hi : Option ℚ

/-- A residual problem with interval anchor data. -/
structure IProblem (n k : ℕ) where
  /-- explicit pairwise part -/
  base : PairInstance n k
  /-- bounded-difference envelope of the residual -/
  c : Fin n → ℚ
  /-- interval evaluations of the residual -/
  anchors : List (IAnchor n k)

/-- The residual problem seen by the rule checker: the lower values. -/
def IProblem.lower (P : IProblem n k) : RProblem n k where
  base := P.base
  c := P.c
  anchors := P.anchors.map fun p => (p.x, p.lo)

/-- Residuals compatible with interval data: bounded differences, and at every anchor a value in
the published interval. -/
def ResidualIntervalClass (P : IProblem n k) (g : Config n k → ℝ) : Prop :=
  (∀ (x : Config n k) (i : Fin n) (s : Fin k), g (Function.update x i s) - g x ≤ (P.c i : ℝ)) ∧
    ∀ p ∈ P.anchors, (p.lo : ℝ) ≤ g p.x ∧ ∀ h ∈ p.hi, g p.x ≤ (h : ℝ)

theorem ResidualIntervalClass.lower {P : IProblem n k} {g : Config n k → ℝ}
    (hg : ResidualIntervalClass P g) : ResidualLowerClass P.lower g := by
  refine ⟨hg.1, ?_⟩
  intro p hp
  obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hp
  exact (hg.2 a ha).1

/-- Consistency of interval data: nonnegative constants, and `lo_p - hi_q ≤ d(x_p, x_q)` for all
ordered pairs of anchors of which the second has an upper value (`p = q` gives `lo ≤ hi`). -/
def IProblem.Consistent (P : IProblem n k) : Prop :=
  (∀ i, 0 ≤ P.c i) ∧
    ∀ p ∈ P.anchors, ∀ q ∈ P.anchors, ∀ h ∈ q.hi,
      p.lo - h ≤ ∑ i, if p.x i = q.x i then 0 else P.c i

instance (P : IProblem n k) : Decidable P.Consistent := by
  unfold IProblem.Consistent
  infer_instance

/-- Real form of the pairwise interval condition. -/
theorem IProblem.Consistent.anchor_le {P : IProblem n k} (hP : P.Consistent)
    {p q : IAnchor n k} (hp : p ∈ P.anchors) (hq : q ∈ P.anchors) {h : ℚ} (hh : h ∈ q.hi) :
    (p.lo : ℝ) - (h : ℝ) ≤ ∑ i, if p.x i = q.x i then (0 : ℝ) else (P.c i : ℝ) := by
  have e := hP.2 p hp q hq h hh
  have e' : ((p.lo - h : ℚ) : ℝ) ≤ ((∑ i, if p.x i = q.x i then 0 else P.c i : ℚ) : ℝ) := by
    exact_mod_cast e
  push_cast at e'
  have h4 : (∑ i, ((if p.x i = q.x i then (0 : ℚ) else P.c i : ℚ) : ℝ)) =
      ∑ i, if p.x i = q.x i then (0 : ℝ) else (P.c i : ℝ) := by
    apply Finset.sum_congr rfl
    intro i _
    split_ifs <;> simp
  linarith

/-- **Consistent interval data describe a non-empty class**: the McShane lower envelope of the
lower values stays below every published upper value. -/
theorem IProblem.Consistent.nonempty {P : IProblem n k} (hP : P.Consistent) :
    ∃ g : Config n k → ℝ, ResidualIntervalClass P g := by
  have hc : ∀ i, (0 : ℝ) ≤ (P.c i : ℝ) := fun i => by exact_mod_cast hP.1 i
  by_cases hlen : 0 < P.anchors.length
  · have hne : (Finset.univ : Finset (Fin P.anchors.length)).Nonempty :=
      ⟨⟨0, hlen⟩, Finset.mem_univ _⟩
    let φ : Config n k → Fin P.anchors.length → ℝ := fun y j =>
      ((P.anchors.get j).lo : ℝ) -
        ∑ i, if (P.anchors.get j).x i = y i then (0 : ℝ) else (P.c i : ℝ)
    refine ⟨fun y => Finset.univ.sup' hne (φ y), ?_, ?_⟩
    · intro x i s
      have key : Finset.univ.sup' hne (φ (Function.update x i s)) ≤
          Finset.univ.sup' hne (φ x) + (P.c i : ℝ) := by
        apply Finset.sup'_le
        intro j hj
        have h1 : φ x j ≤ Finset.univ.sup' hne (φ x) := Finset.le_sup' (φ x) hj
        have h2 := hamming_update_le (fun l => (P.c l : ℝ)) hc (P.anchors.get j).x x i s
        show ((P.anchors.get j).lo : ℝ) -
            ∑ l, (if (P.anchors.get j).x l = Function.update x i s l then (0 : ℝ)
              else (P.c l : ℝ)) ≤ Finset.univ.sup' hne (φ x) + (P.c i : ℝ)
        have h1' : ((P.anchors.get j).lo : ℝ) -
            ∑ l, (if (P.anchors.get j).x l = x l then (0 : ℝ) else (P.c l : ℝ)) ≤
              Finset.univ.sup' hne (φ x) := h1
        linarith
      show Finset.univ.sup' hne (φ (Function.update x i s)) - Finset.univ.sup' hne (φ x) ≤
        (P.c i : ℝ)
      linarith
    · intro q hq
      obtain ⟨j, hj⟩ := List.get_of_mem hq
      constructor
      · have h1 : φ q.x j ≤ Finset.univ.sup' hne (φ q.x) :=
          Finset.le_sup' (φ q.x) (Finset.mem_univ j)
        have h2 : φ q.x j = (q.lo : ℝ) := by
          show ((P.anchors.get j).lo : ℝ) -
            ∑ i, (if (P.anchors.get j).x i = q.x i then (0 : ℝ) else (P.c i : ℝ)) = (q.lo : ℝ)
          rw [hj]
          simp
        show (q.lo : ℝ) ≤ Finset.univ.sup' hne (φ q.x)
        linarith
      · intro h hh
        show Finset.univ.sup' hne (φ q.x) ≤ (h : ℝ)
        apply Finset.sup'_le
        intro l _
        have e := hP.anchor_le (List.get_mem P.anchors l) hq hh
        show ((P.anchors.get l).lo : ℝ) -
          ∑ i, (if (P.anchors.get l).x i = q.x i then (0 : ℝ) else (P.c i : ℝ)) ≤ (h : ℝ)
        linarith
  · refine ⟨fun _ => 0, ?_, ?_⟩
    · intro x i s
      simpa using hc i
    · intro p hp
      exact absurd (List.length_pos_of_mem hp) hlen

/-- **Inconsistent interval data describe an empty class** (given that configurations exist). -/
theorem IProblem.consistent_of_nonempty (P : IProblem n k) (x₀ : Config n k)
    (h : ∃ g : Config n k → ℝ, ResidualIntervalClass P g) : P.Consistent := by
  obtain ⟨g, hg⟩ := h
  constructor
  · intro i
    have h1 := hg.1 x₀ i (x₀ i)
    rw [Function.update_eq_self] at h1
    have h0 : (0 : ℝ) ≤ (P.c i : ℝ) := by linarith
    exact_mod_cast h0
  · intro p hp q hq u hu
    have hmem : (p.x, p.lo) ∈ P.lower.anchors := List.mem_map.mpr ⟨p, hp, rfl⟩
    have h1 := residual_ge_anchor P.lower g hg.lower (p.x, p.lo) hmem q.x
    have h2 := (hg.2 q hq).2 u hu
    have h3 : ∑ i, (if q.x i = p.x i then (0 : ℝ) else (P.c i : ℝ)) =
        ∑ i, ((if p.x i = q.x i then (0 : ℚ) else P.c i : ℚ) : ℝ) := by
      apply Finset.sum_congr rfl
      intro i _
      by_cases hi : p.x i = q.x i
      · simp [hi]
      · have hi' : ¬ q.x i = p.x i := fun e => hi e.symm
        simp [hi, hi']
    have h1' : (p.lo : ℝ) - ∑ i, (if q.x i = p.x i then (0 : ℝ) else (P.c i : ℝ)) ≤ g q.x := h1
    rw [h3] at h1'
    have h4 : ((p.lo - u : ℚ) : ℝ) ≤ ((∑ i, if p.x i = q.x i then 0 else P.c i : ℚ) : ℝ) := by
      push_cast
      linarith
    exact_mod_cast h4

/-- **Interval consistency is exactly non-emptiness of the interval class.** -/
theorem IProblem.consistent_iff_nonempty (P : IProblem n k) (x₀ : Config n k) :
    P.Consistent ↔ ∃ g : Config n k → ℝ, ResidualIntervalClass P g :=
  ⟨fun h => h.nonempty, P.consistent_of_nonempty x₀⟩

/-- **Top-level residual kernel for interval anchor data**: reject inconsistent data, then check
the rules against the lower values. -/
def verifyITop (c : RCert n k) (P : IProblem n k) (D : Dom n k) (L : ℚ) : Bool :=
  decide P.Consistent && verifyR c P.lower D L

/-- **Master Soundness Theorem, interval anchor data.**  If `verifyITop` accepts, then (i) some
residual has the bounded differences and takes a value in every published interval, and for
*every* such residual (ii) `L` is a lower bound on `E + g` over the box and (iii) at every anchor
with an upper value `h` the true energy is at most `E + h` — so that an anchor inside the box
certifies the optimum to lie in `[L, E + h]`. -/
theorem verifyITop_sound (c : RCert n k) (P : IProblem n k) (D : Dom n k) (L : ℚ)
    (hv : verifyITop c P D L = true) :
    (∃ g : Config n k → ℝ, ResidualIntervalClass P g) ∧
      ∀ g : Config n k → ℝ, ResidualIntervalClass P g →
        (∀ x, InBox D x → (L : ℝ) ≤ (P.base.energy x : ℝ) + g x) ∧
          ∀ p ∈ P.anchors, ∀ h ∈ p.hi,
            (P.base.energy p.x : ℝ) + g p.x ≤ ((P.base.energy p.x + h : ℚ) : ℝ) := by
  simp only [verifyITop, Bool.and_eq_true, decide_eq_true_eq] at hv
  refine ⟨hv.1.nonempty, fun g hg => ⟨verifyR_sound_lower c P.lower D L hv.2 g hg.lower, ?_⟩⟩
  intro p hp h hh
  have h2 := (hg.2 p hp).2 h hh
  push_cast
  linarith

/-- Exact anchor values as interval data `[v, v]`. -/
def IProblem.ofExact (P : RProblem n k) : IProblem n k where
  base := P.base
  c := P.c
  anchors := P.anchors.map fun p => ⟨p.1, p.2, some p.2⟩

/-- Lower-bound anchor values as interval data `[v, ∞)`. -/
def IProblem.ofLower (P : RProblem n k) : IProblem n k where
  base := P.base
  c := P.c
  anchors := P.anchors.map fun p => ⟨p.1, p.2, none⟩

theorem IProblem.ofExact_lower (P : RProblem n k) : (IProblem.ofExact P).lower = P := by
  cases P
  simp [IProblem.ofExact, IProblem.lower, List.map_map, Function.comp_def]

theorem IProblem.ofLower_lower (P : RProblem n k) : (IProblem.ofLower P).lower = P := by
  cases P
  simp [IProblem.ofLower, IProblem.lower, List.map_map, Function.comp_def]

/-- For exact data, interval consistency is the consistency of `verifyRTop`. -/
theorem IProblem.ofExact_consistent (P : RProblem n k) :
    (IProblem.ofExact P).Consistent ↔ P.Consistent := by
  unfold IProblem.Consistent RProblem.Consistent IProblem.ofExact
  simp only [List.mem_map, forall_exists_index, and_imp, forall_apply_eq_imp_iff₂,
    Option.mem_def, Option.some.injEq, forall_eq']

/-- For lower-bound data, interval consistency is nonnegativity of the constants. -/
theorem IProblem.ofLower_consistent (P : RProblem n k) :
    (IProblem.ofLower P).Consistent ↔ ∀ i, 0 ≤ P.c i := by
  constructor
  · intro h
    exact h.1
  · intro h
    refine ⟨h, ?_⟩
    intro p _ q hq u hu
    obtain ⟨a, _, rfl⟩ := List.mem_map.mp hq
    exact (Option.not_mem_none u hu).elim

/-- The exact-value kernel is the interval kernel on intervals `[v, v]`. -/
theorem verifyITop_ofExact (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ) :
    verifyITop c (IProblem.ofExact P) D L = verifyRTop c P D L := by
  unfold verifyITop verifyRTop
  rw [IProblem.ofExact_lower, decide_eq_decide.mpr (IProblem.ofExact_consistent P)]

/-- The lower-bound kernel is the interval kernel on intervals `[v, ∞)`. -/
theorem verifyITop_ofLower (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ) :
    verifyITop c (IProblem.ofLower P) D L = verifyRLowerTop c P D L := by
  unfold verifyITop verifyRLowerTop
  rw [IProblem.ofLower_lower, decide_eq_decide.mpr (IProblem.ofLower_consistent P)]

/-! ### From rational certificates to real-valued energies (outward rounding) -/

/-- A rational instance that lies termwise below a real pairwise model has a smaller energy. -/
theorem PairInstance.cast_energy_le (I : PairInstance n k)
    (M : PairModel ℝ (Fin n) (fun _ => Fin k)) (hh : ∀ i a, (I.h i a : ℝ) ≤ M.h i a)
    (hJ : ∀ i j a b, (I.J i j a b : ℝ) ≤ M.J i j a b) (x : Config n k) :
    ((I.energy x : ℚ) : ℝ) ≤ M.energy x := by
  unfold PairInstance.energy PairModel.energy
  push_cast
  apply add_le_add
  · exact Finset.sum_le_sum fun i _ => hh i (x i)
  · exact Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => hJ i j (x i) (x j)

/-- **Soundness for real energies.**  If the published rational instance is an outward-rounded
*lower* instance of a real pairwise model (every table entry rounded down), an accepted
certificate bounds the true real energy on the box. -/
theorem verify_sound_real (c : Cert n k) (I : PairInstance n k) (D : Dom n k) (L : ℚ)
    (hv : verify c I D L = true) (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (hh : ∀ i a, (I.h i a : ℝ) ≤ M.h i a) (hJ : ∀ i j a b, (I.J i j a b : ℝ) ≤ M.J i j a b)
    (x : Config n k) (hx : InBox D x) : (L : ℝ) ≤ M.energy x := by
  have h1 := verify_sound c I D L hv x hx
  have h2 := I.cast_energy_le M hh hJ x
  have h3 : (L : ℝ) ≤ ((I.energy x : ℚ) : ℝ) := by exact_mod_cast h1
  linarith

/-- **Soundness for real energies with an unknown residual.** -/
theorem verifyR_sound_real (c : RCert n k) (P : RProblem n k) (D : Dom n k) (L : ℚ)
    (hv : verifyR c P D L = true) (M : PairModel ℝ (Fin n) (fun _ => Fin k))
    (hh : ∀ i a, (P.base.h i a : ℝ) ≤ M.h i a)
    (hJ : ∀ i j a b, (P.base.J i j a b : ℝ) ≤ M.J i j a b) (g : Config n k → ℝ)
    (hg : ResidualLowerClass P g) (x : Config n k) (hx : InBox D x) :
    (L : ℝ) ≤ M.energy x + g x := by
  have h1 := verifyR_sound_lower c P D L hv g hg x hx
  have h2 := P.base.cast_energy_le M hh hJ x
  linarith

/-! ### Executable examples (non-vacuity of the kernel)

All `verify … = true` facts below are proved by `decide`, i.e. the checker is *run inside Lean's
trusted kernel* on exact rationals; no compiler or floating point is in the trusted base. -/

/-- Frustrated antiferromagnetic triangle (`n = 3`, `k = 2`): cost `1` whenever two sites agree
(each unordered pair stored once, in the orientation `i < j`).  Its optimum is `1`. -/
def triangle : PairInstance 3 2 where
  h := fun _ _ => 0
  J := fun i j a b => if i < j ∧ a = b then 1 else 0

/-- A two-leaf certificate for the triangle: branch on site `0`, then one dual leaf whose
messages are the exact dynamic-programming messages of the remaining edge `1 — 2`. -/
def triangleCert : Cert 3 2 :=
  .branch 0 fun a =>
    .leaf (fun i => if i = 1 then 1 else 0) (fun _ _ => 0)
      (fun i j s =>
        if i = 1 ∧ j = 0 then (if s = a then 1 else 0)
        else if i = 2 ∧ j = 0 then (if s = a then 1 else 0)
        else if i = 1 ∧ j = 2 then (if s = a then 0 else 1)
        else if i = 2 ∧ j = 1 then (if s = a then -1 else 0)
        else 0)

/-- The kernel accepts the two-leaf certificate for the bound `1`. -/
theorem triangle_verified : verify triangleCert triangle (fullDom 3 2) 1 = true := by decide +kernel

/-- Hence every configuration of the frustrated triangle has energy at least `1` … -/
theorem triangle_lower_bound (x : Config 3 2) : 1 ≤ triangle.energy x :=
  verify_sound triangleCert triangle (fullDom 3 2) 1 triangle_verified x (inBox_fullDom x)

/-- … and the bound is attained: the certified gap is zero. -/
theorem triangle_optimum : triangle.energy ![0, 1, 0] = 1 := by decide +kernel

/-- The kernel rejects the same certificate for the (false) bound `2`. -/
theorem triangle_rejects : verify triangleCert triangle (fullDom 3 2) 2 = false := by decide +kernel

/-- A dead-end-elimination certificate: with a field favouring state `1` on site `0`
(`h 0 0 = 3`), state `0` of site `0` is dominated by state `1` and is pruned; the remaining box
is certified by one dual leaf. -/
def biased : PairInstance 3 2 where
  h := fun i a => if i = 0 ∧ a = 0 then 3 else 0
  J := fun i j a b => if i < j ∧ a = b then 1 else 0

def biasedCert : Cert 3 2 :=
  .prune 0 0 1 (fun _ => -1)
    (.leaf (fun i => if i = 1 then 1 else 0) (fun _ _ => 0)
      (fun i j s =>
        if i = 1 ∧ j = 0 then (if s = 1 then 1 else 0)
        else if i = 2 ∧ j = 0 then (if s = 1 then 1 else 0)
        else if i = 1 ∧ j = 2 then (if s = 1 then 0 else 1)
        else if i = 2 ∧ j = 1 then (if s = 1 then -1 else 0)
        else 0))

theorem biased_verified : verify biasedCert biased (fullDom 3 2) 1 = true := by decide +kernel

/-- Exhaustive certificate for three binary sites (used as a generic fallback in examples). -/
def exhaustive3 (I : PairInstance 3 2) : Cert 3 2 :=
  .branch 0 fun a => .branch 1 fun b => .branch 2 fun c =>
    .leaf (fun i => I.h i (![a, b, c] i))
      (fun i j => (I.J i j (![a, b, c] i) (![a, b, c] j) + I.J j i (![a, b, c] j) (![a, b, c] i)) / 2)
      (fun _ _ _ => 0)

/-- A residual problem on the triangle: bounded differences `1/4` per site and one evaluated
anchor `x₀ = (0,1,0)` with residual value `-1/8`. -/
def triangleResidual : RProblem 3 2 where
  base := triangle
  c := fun _ => 1 / 4
  anchors := [(![0, 1, 0], -1 / 8)]

/-- Residual certificate: bound the residual from the anchor and certify the anchored pairwise
minorant exhaustively. -/
def triangleResidualCert : RCert 3 2 :=
  .anchor 0 (exhaustive3 (triangle.anchored (fun _ => 1 / 4) ![0, 1, 0]))

theorem triangleResidual_verified :
    verifyR triangleResidualCert triangleResidual (fullDom 3 2) (1 / 8) = true := by decide +kernel

/-- For *every* residual with bounded differences `1/4` and `g (0,1,0) = -1/8`, the true optimum
of `E + g` over all `8` configurations lies in `[1/8, 7/8]`. -/
theorem triangleResidual_gap (g : Config 3 2 → ℝ) (hg : ResidualClass triangleResidual g)
    (x : Config 3 2) : ((1 / 8 : ℚ) : ℝ) ≤ (triangle.energy x : ℝ) + g x :=
  verifyR_sound triangleResidualCert triangleResidual (fullDom 3 2) (1 / 8)
    triangleResidual_verified g hg x (inBox_fullDom x)

/-- The top-level kernel (consistency check included) accepts the same certificate. -/
theorem triangleResidual_verifiedTop :
    verifyRTop triangleResidualCert triangleResidual (fullDom 3 2) (1 / 8) = true := by
  decide +kernel

/-- Inconsistent residual data: two anchors at Hamming distance one whose values differ by `10`
although the envelope allows at most `1/4`.  No residual satisfies these data. -/
def inconsistentResidual : RProblem 3 2 where
  base := triangle
  c := fun _ => 1 / 4
  anchors := [(![0, 1, 0], 0), (![1, 1, 0], 10)]

/-- The bare rule checker accepts the bound `41/4` on these data (the minimum of `E` alone is
`1`).  Read with *exact* anchor semantics this is vacuous … -/
theorem inconsistentResidual_unguarded :
    verifyR (.anchor 1 (exhaustive3 (triangle.anchored (fun _ => 1 / 4) ![1, 1, 0])))
      inconsistentResidual (fullDom 3 2) (41 / 4) = true := by decide +kernel

/-- … whereas with *lower-bound* semantics (`g (0,1,0) ≥ 0`, `g (1,1,0) ≥ 10`) the same bound is
a meaningful, non-vacuous statement and the lower-semantics kernel accepts it … -/
theorem inconsistentResidual_lowerTop :
    verifyRLowerTop (.anchor 1 (exhaustive3 (triangle.anchored (fun _ => 1 / 4) ![1, 1, 0])))
      inconsistentResidual (fullDom 3 2) (41 / 4) = true := by decide +kernel

/-- … the exact class is empty … -/
theorem inconsistentResidual_empty :
    ¬ ∃ g : Config 3 2 → ℝ, ResidualClass inconsistentResidual g := by
  intro h
  have hc := inconsistentResidual.consistent_of_nonempty ![0, 1, 0] h
  revert hc
  decide +kernel

/-- … and the exact-semantics top-level kernel rejects the data for every certificate and every
bound. -/
theorem inconsistentResidual_rejected (c : RCert 3 2) (L : ℚ) :
    verifyRTop c inconsistentResidual (fullDom 3 2) L = false := by
  have h : decide inconsistentResidual.Consistent = false := by decide +kernel
  simp [verifyRTop, h]

/-- A negative envelope constant: both top-level kernels reject, whatever the certificate. -/
def negativeEnvelope : RProblem 3 2 where
  base := triangle
  c := fun i => if i = 0 then -10 else 1 / 4
  anchors := [(![0, 1, 0], 0)]

theorem negativeEnvelope_rejected (c : RCert 3 2) (L : ℚ) :
    verifyRTop c negativeEnvelope (fullDom 3 2) L = false ∧
      verifyRLowerTop c negativeEnvelope (fullDom 3 2) L = false := by
  have h1 : decide negativeEnvelope.Consistent = false := by decide +kernel
  have h2 : decide (∀ i, 0 ≤ negativeEnvelope.c i) = false := by decide +kernel
  simp [verifyRTop, verifyRLowerTop, h1, h2]

/-- The triangle with an interval evaluation of the residual at `(0,1,0)`: `g ∈ [-9/64, -7/64]`. -/
def triangleInterval : IProblem 3 2 where
  base := triangle
  c := fun _ => 1 / 4
  anchors := [⟨![0, 1, 0], -9 / 64, some (-7 / 64)⟩]

/-- Accepted for the bound `7/64`; the incumbent `E + hi = 57/64` then brackets the optimum. -/
theorem triangleInterval_verified :
    verifyITop triangleResidualCert triangleInterval (fullDom 3 2) (7 / 64) = true := by
  decide +kernel

/-- Rounded but incompatible evaluations: `g (0,1,0) ∈ [-1/64, 1/64]`, `g (1,1,0) ∈ [639/64, 641/64]`
at Hamming distance one with envelope constant `1/4`. -/
def inconsistentInterval : IProblem 3 2 where
  base := triangle
  c := fun _ => 1 / 4
  anchors := [⟨![0, 1, 0], -1 / 64, some (1 / 64)⟩, ⟨![1, 1, 0], 639 / 64, some (641 / 64)⟩]

/-- The interval kernel rejects them for every certificate and every bound — rounding does not
hide an inconsistency larger than the rounding error. -/
theorem inconsistentInterval_rejected (c : RCert 3 2) (L : ℚ) :
    verifyITop c inconsistentInterval (fullDom 3 2) L = false := by
  have h : decide inconsistentInterval.Consistent = false := by decide +kernel
  simp [verifyITop, h]

end MetricChain
