import Mathlib
import proofs.Core.Basic
import proofs.Frontiers.Dominance
import proofs.CertificateAlgebra

/-!
# Partition-function certificates: the sum–product kernel

The optimisation kernel of `CertificateAlgebra.lean` works in the tropical `(min, +)` semiring.
This file is its `(+, ×)` counterpart: an executable checker that turns a certificate into a
**two-sided rational enclosure of the partition function** of a pairwise model over a box of
configurations, with exact rational arithmetic.

To keep the kernel transcendental-free the instance is given in the *weight domain*: rational
Boltzmann factors `w i a ≈ exp(-β h i a)` and `W i j a b ≈ exp(-β J i j a b)`.  Outward-rounded
enclosures of the true factors (from `Core/Rounding.lean`) give a lower instance and an upper
instance; `Z_encloses_partitionFn` shows that their exact rational partition sums bracket the real
partition function, so `lo(I⁻) ≤ Z_true ≤ hi(I⁺)`.

Certificate constructors (the `leaf` / `branch` / `prune` rules mirror those of the tropical
kernel; the tropical decomposition rule `sum` has no two-sided counterpart here — its one-sided
analogue is the Hölder bound `partitionFn_holder`, which is a theorem but not a kernel rule):

* `leaf lo hi` — factorised bound: pair factors are replaced by certified constants, the
  remaining product measure sums exactly (`∏ i, ∑ a, w i a`);
* `branch i children` — the partition function is *additive* over the states of a site;
* `prune i r t q₀ q rest` — **thermal dead-end elimination** in the weight domain: if the local
  weight of state `r` is at most `ρ = q₀ ∏ q j` times that of `t` in every context, deleting `r`
  changes the partition function by a factor in `[1, 1 + ρ]`.

`zverify_sound` is the Master Soundness Theorem of this kernel; it needs nonnegative factors, which
the top-level entry point `zverifyTop` checks itself (`zverifyTop_sound` has no side condition).
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-- A pairwise model in the weight domain (rational Boltzmann factors). -/
structure WInstance (n k : ℕ) where
  /-- one-body factors -/
  w : Fin n → Fin k → ℚ
  /-- two-body factors on ordered pairs `i ≠ j` -/
  W : Fin n → Fin n → Fin k → Fin k → ℚ

/-- All factors are nonnegative. -/
def WInstance.Nonneg (I : WInstance n k) : Prop :=
  (∀ i a, 0 ≤ I.w i a) ∧ ∀ i j a b, 0 ≤ I.W i j a b

/-- Boltzmann weight of a configuration. -/
def WInstance.weight (I : WInstance n k) (x : Config n k) : ℚ :=
  (∏ i, I.w i (x i)) * ∏ i, ∏ j ∈ univ.erase i, I.W i j (x i) (x j)

theorem WInstance.weight_nonneg {I : WInstance n k} (hI : I.Nonneg) (x : Config n k) :
    0 ≤ I.weight x :=
  mul_nonneg (Finset.prod_nonneg fun i _ => hI.1 i (x i))
    (Finset.prod_nonneg fun i _ => Finset.prod_nonneg fun j _ => hI.2 i j (x i) (x j))

/-- The box `∏ D` as a finite set of configurations. -/
def boxFinset (D : Dom n k) : Finset (Config n k) := Fintype.piFinset fun i => (D i).toFinset

theorem mem_boxFinset {D : Dom n k} {x : Config n k} : x ∈ boxFinset D ↔ InBox D x := by
  unfold boxFinset InBox
  simp [Fintype.mem_piFinset]

/-- Exact rational partition sum over the box. -/
def WInstance.Z (I : WInstance n k) (D : Dom n k) : ℚ := ∑ x ∈ boxFinset D, I.weight x

theorem WInstance.Z_nonneg {I : WInstance n k} (hI : I.Nonneg) (D : Dom n k) : 0 ≤ I.Z D :=
  Finset.sum_nonneg fun x _ => I.weight_nonneg hI x

/-! ### Structural identities -/

/-- The partition sum is additive over the states of a site. -/
theorem WInstance.Z_branch (I : WInstance n k) (D : Dom n k) (i : Fin n) :
    I.Z D = ∑ a ∈ (D i).toFinset, I.Z (D.fix i a) := by
  unfold WInstance.Z
  have hmaps : ∀ x ∈ boxFinset D, x i ∈ (D i).toFinset := fun x hx =>
    List.mem_toFinset.mpr (mem_boxFinset.mp hx i)
  rw [← Finset.sum_fiberwise_of_maps_to hmaps]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr _ (fun _ _ => rfl)
  ext x
  simp only [Finset.mem_filter, mem_boxFinset]
  constructor
  · rintro ⟨hx, hxa⟩ j
    unfold Dom.fix
    by_cases hj : j = i
    · subst hj
      simp [hxa]
    · rw [Function.update_of_ne hj]
      exact hx j
  · intro hx
    have hxi : x i = a := by
      have h := hx i
      unfold Dom.fix at h
      simpa using h
    refine ⟨fun j => ?_, hxi⟩
    by_cases hj : j = i
    · subst hj
      rw [hxi]
      exact List.mem_toFinset.mp ha
    · have h := hx j
      unfold Dom.fix at h
      rwa [Function.update_of_ne hj] at h

/-- Context-only part of the weight (everything not involving site `i`). -/
def WInstance.wbase (I : WInstance n k) (i : Fin n) (x : Config n k) : ℚ :=
  (∏ l ∈ univ.erase i, I.w l (x l)) *
    ∏ l ∈ univ.erase i, ∏ j ∈ (univ.erase l).erase i, I.W l j (x l) (x j)

/-- Local weight of state `a` at site `i` in context `x`. -/
def WInstance.wlocal (I : WInstance n k) (i : Fin n) (a : Fin k) (x : Config n k) : ℚ :=
  I.w i a * ∏ j ∈ univ.erase i, (I.W i j a (x j) * I.W j i (x j) a)

/-- Multiplicative separability of the weight at a site. -/
theorem WInstance.weight_update (I : WInstance n k) (x : Config n k) (i : Fin n) (a : Fin k) :
    I.weight (Function.update x i a) = I.wbase i x * I.wlocal i a x := by
  unfold WInstance.weight WInstance.wbase WInstance.wlocal
  have hmem : i ∈ (univ : Finset (Fin n)) := mem_univ i
  rw [← Finset.mul_prod_erase _ _ hmem, ← Finset.mul_prod_erase univ
    (fun l => ∏ j ∈ univ.erase l, I.W l j (Function.update x i a l) (Function.update x i a j)) hmem]
  have h1 : ∏ l ∈ univ.erase i, I.w l (Function.update x i a l) =
      ∏ l ∈ univ.erase i, I.w l (x l) := by
    apply Finset.prod_congr rfl
    intro l hl
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hl)]
  have h2 : ∏ j ∈ univ.erase i, I.W i j a (Function.update x i a j) =
      ∏ j ∈ univ.erase i, I.W i j a (x j) := by
    apply Finset.prod_congr rfl
    intro j hj
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hj)]
  have h3 : ∏ l ∈ univ.erase i, ∏ j ∈ univ.erase l,
        I.W l j (Function.update x i a l) (Function.update x i a j) =
      ∏ l ∈ univ.erase i,
        (I.W l i (x l) a * ∏ j ∈ (univ.erase l).erase i, I.W l j (x l) (x j)) := by
    apply Finset.prod_congr rfl
    intro l hl
    have hli : l ≠ i := Finset.ne_of_mem_erase hl
    have hil : i ∈ univ.erase l := Finset.mem_erase.mpr ⟨fun h => hli h.symm, mem_univ i⟩
    rw [← Finset.mul_prod_erase _ _ hil, Function.update_of_ne hli, Function.update_self]
    congr 1
    apply Finset.prod_congr rfl
    intro j hj
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hj)]
  rw [Function.update_self, h1, h2, h3, Finset.prod_mul_distrib, Finset.prod_mul_distrib]
  ring

theorem WInstance.wbase_nonneg {I : WInstance n k} (hI : I.Nonneg) (i : Fin n) (x : Config n k) :
    0 ≤ I.wbase i x :=
  mul_nonneg (Finset.prod_nonneg fun l _ => hI.1 l (x l))
    (Finset.prod_nonneg fun l _ => Finset.prod_nonneg fun j _ => hI.2 l j (x l) (x j))

/-! ### Certificates and the kernel -/

/-- Certificates for two-sided partition-function bounds. -/
inductive ZCert (n k : ℕ) : Type
  | leaf (lo hi : Fin n → Fin n → ℚ) : ZCert n k
  | branch (i : Fin n) (children : Fin k → ZCert n k) : ZCert n k
  | prune (i : Fin n) (r t : Fin k) (q₀ : ℚ) (q : Fin n → ℚ) (rest : ZCert n k) : ZCert n k

/-- Leaf check: every pair factor on the current domains lies in `[lo i j, hi i j]`, `lo ≥ 0`. -/
def LeafZOK (I : WInstance n k) (D : Dom n k) (lo hi : Fin n → Fin n → ℚ) : Prop :=
  ∀ i, ∀ j ∈ univ.erase i, 0 ≤ lo i j ∧
    ∀ a ∈ D i, ∀ b ∈ D j, lo i j ≤ I.W i j a b ∧ I.W i j a b ≤ hi i j

instance (I : WInstance n k) (D : Dom n k) (lo hi : Fin n → Fin n → ℚ) :
    Decidable (LeafZOK I D lo hi) := by
  unfold LeafZOK; infer_instance

/-- Thermal prune check: `t` survives, differs from `r`, and the local weight of `r` is at most
`q₀ ∏ q j` times the local weight of `t`, factor by factor. -/
def PruneZOK (I : WInstance n k) (D : Dom n k) (i : Fin n) (r t : Fin k) (q₀ : ℚ)
    (q : Fin n → ℚ) : Prop :=
  t ∈ D i ∧ t ≠ r ∧ 0 ≤ q₀ ∧ I.w i r ≤ q₀ * I.w i t ∧
    ∀ j ∈ univ.erase i, 0 ≤ q j ∧
      ∀ s ∈ D j, I.W i j r s * I.W j i s r ≤ q j * (I.W i j t s * I.W j i s t)

instance (I : WInstance n k) (D : Dom n k) (i : Fin n) (r t : Fin k) (q₀ : ℚ) (q : Fin n → ℚ) :
    Decidable (PruneZOK I D i r t q₀ q) := by
  unfold PruneZOK
  refine @instDecidableAnd _ _ ?_ (@instDecidableAnd _ _ ?_ (@instDecidableAnd _ _ ?_
    (@instDecidableAnd _ _ ?_ ?_))) <;> infer_instance

/-- Sum of two optional intervals. -/
def addIv : Option (ℚ × ℚ) → Option (ℚ × ℚ) → Option (ℚ × ℚ)
  | some (l, h), some (L, H) => some (l + L, h + H)
  | _, _ => none

/-- **The partition-function kernel.**  Returns a certified interval `(lo, hi)` for the partition
sum over the box, or `none` if a check fails. -/
def zverify : ZCert n k → WInstance n k → Dom n k → Option (ℚ × ℚ)
  | .leaf lo hi, I, D =>
      if LeafZOK I D lo hi then
        some ((∏ i, ∑ a ∈ (D i).toFinset, I.w i a) * ∏ i, ∏ j ∈ univ.erase i, lo i j,
          (∏ i, ∑ a ∈ (D i).toFinset, I.w i a) * ∏ i, ∏ j ∈ univ.erase i, hi i j)
      else none
  | .branch i ch, I, D =>
      (D i).dedup.foldr (fun a acc => addIv (zverify (ch a) I (D.fix i a)) acc) (some (0, 0))
  | .prune i r t q₀ q rest, I, D =>
      if PruneZOK I D i r t q₀ q then
        (zverify rest I (D.remove i r)).map fun lh =>
          (lh.1, (1 + q₀ * ∏ j ∈ univ.erase i, q j) * lh.2)
      else none

/-! ### Soundness of the rules -/

/-- Soundness of the factorised leaf. -/
theorem zleaf_sound {I : WInstance n k} (hI : I.Nonneg) (D : Dom n k) (lo hi : Fin n → Fin n → ℚ)
    (h : LeafZOK I D lo hi) :
    (∏ i, ∑ a ∈ (D i).toFinset, I.w i a) * ∏ i, ∏ j ∈ univ.erase i, lo i j ≤ I.Z D ∧
      I.Z D ≤ (∏ i, ∑ a ∈ (D i).toFinset, I.w i a) * ∏ i, ∏ j ∈ univ.erase i, hi i j := by
  have hprod : (∏ i, ∑ a ∈ (D i).toFinset, I.w i a) = ∑ x ∈ boxFinset D, ∏ i, I.w i (x i) := by
    unfold boxFinset
    exact Finset.prod_univ_sum (fun i => (D i).toFinset) (fun i a => I.w i a)
  rw [hprod, Finset.sum_mul, Finset.sum_mul]
  unfold WInstance.Z WInstance.weight
  constructor
  · apply Finset.sum_le_sum
    intro x hx
    have hxD := mem_boxFinset.mp hx
    apply mul_le_mul_of_nonneg_left _ (Finset.prod_nonneg fun i _ => hI.1 i (x i))
    apply Finset.prod_le_prod
    · intro i _
      exact Finset.prod_nonneg fun j hj => (h i j hj).1
    · intro i _
      apply Finset.prod_le_prod
      · intro j hj
        exact (h i j hj).1
      · intro j hj
        exact ((h i j hj).2 (x i) (hxD i) (x j) (hxD j)).1
  · apply Finset.sum_le_sum
    intro x hx
    have hxD := mem_boxFinset.mp hx
    apply mul_le_mul_of_nonneg_left _ (Finset.prod_nonneg fun i _ => hI.1 i (x i))
    apply Finset.prod_le_prod
    · intro i _
      exact Finset.prod_nonneg fun j _ => hI.2 i j (x i) (x j)
    · intro i _
      apply Finset.prod_le_prod
      · intro j _
        exact hI.2 i j (x i) (x j)
      · intro j hj
        exact ((h i j hj).2 (x i) (hxD i) (x j) (hxD j)).2

/-- Soundness of interval accumulation over a duplicate-free list of branch values. -/
theorem foldr_addIv_sound (val : Fin k → ℚ) (iv : Fin k → Option (ℚ × ℚ))
    (hiv : ∀ a l h, iv a = some (l, h) → l ≤ val a ∧ val a ≤ h) :
    ∀ (l : List (Fin k)), l.Nodup → ∀ L H,
      l.foldr (fun a acc => addIv (iv a) acc) (some (0, 0)) = some (L, H) →
        L ≤ ∑ a ∈ l.toFinset, val a ∧ ∑ a ∈ l.toFinset, val a ≤ H := by
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
        constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

/-- The box after removing state `r` at site `i` is the part of the box with `x i ≠ r`. -/
theorem boxFinset_remove (D : Dom n k) (i : Fin n) (r : Fin k) :
    boxFinset (D.remove i r) = (boxFinset D).filter fun x => x i ≠ r := by
  ext x
  simp only [Finset.mem_filter, mem_boxFinset]
  constructor
  · intro hx
    have hi := hx i
    unfold Dom.remove at hi
    simp only [Function.update_self, List.mem_filter, decide_eq_true_eq] at hi
    refine ⟨fun j => ?_, hi.2⟩
    by_cases hj : j = i
    · subst hj
      exact hi.1
    · have h := hx j
      unfold Dom.remove at h
      rwa [Function.update_of_ne hj] at h
  · rintro ⟨hx, hne⟩
    exact inBox_remove_of_ne hx i r hne

/-- **Thermal dead-end elimination in the weight domain.** -/
theorem zprune_sound {I : WInstance n k} (hI : I.Nonneg) (D : Dom n k) (i : Fin n) (r t : Fin k)
    (q₀ : ℚ) (q : Fin n → ℚ) (h : PruneZOK I D i r t q₀ q) :
    I.Z (D.remove i r) ≤ I.Z D ∧
      I.Z D ≤ (1 + q₀ * ∏ j ∈ univ.erase i, q j) * I.Z (D.remove i r) := by
  classical
  obtain ⟨ht, htr, hq₀, hw, hq⟩ := h
  set ρ := q₀ * ∏ j ∈ univ.erase i, q j with hρ
  have hρ0 : 0 ≤ ρ := mul_nonneg hq₀ (Finset.prod_nonneg fun j hj => (hq j hj).1)
  set B := boxFinset D
  set A := B.filter fun x => x i = r
  set S := B.filter fun x => x i ≠ r
  have hsplit : I.Z D = ∑ x ∈ A, I.weight x + ∑ x ∈ S, I.weight x := by
    unfold WInstance.Z
    exact (Finset.sum_filter_add_sum_filter_not B (fun x => x i = r) I.weight).symm
  have hS : I.Z (D.remove i r) = ∑ x ∈ S, I.weight x := by
    unfold WInstance.Z
    rw [boxFinset_remove]
  have hA0 : 0 ≤ ∑ x ∈ A, I.weight x := Finset.sum_nonneg fun x _ => I.weight_nonneg hI x
  -- pointwise domination along the transport map
  have hpt : ∀ x ∈ A, I.weight x ≤ ρ * I.weight (Function.update x i t) := by
    intro x hx
    have hxB : InBox D x := mem_boxFinset.mp (Finset.mem_filter.mp hx).1
    have hxr : x i = r := (Finset.mem_filter.mp hx).2
    have hself : Function.update x i r = x := by
      rw [← hxr]
      exact Function.update_eq_self i x
    have e1 := I.weight_update x i r
    rw [hself] at e1
    rw [e1, I.weight_update x i t]
    have hloc : I.wlocal i r x ≤ ρ * I.wlocal i t x := by
      unfold WInstance.wlocal
      have hprod : ∏ j ∈ univ.erase i, (I.W i j r (x j) * I.W j i (x j) r) ≤
          ∏ j ∈ univ.erase i, (q j * (I.W i j t (x j) * I.W j i (x j) t)) := by
        apply Finset.prod_le_prod
        · intro j _
          exact mul_nonneg (hI.2 i j r (x j)) (hI.2 j i (x j) r)
        · intro j hj
          exact (hq j hj).2 (x j) (hxB j)
      have hsplit : ∏ j ∈ univ.erase i, (q j * (I.W i j t (x j) * I.W j i (x j) t)) =
          (∏ j ∈ univ.erase i, q j) * ∏ j ∈ univ.erase i, (I.W i j t (x j) * I.W j i (x j) t) :=
        Finset.prod_mul_distrib
      rw [hsplit] at hprod
      have hnn : 0 ≤ ∏ j ∈ univ.erase i, (I.W i j r (x j) * I.W j i (x j) r) :=
        Finset.prod_nonneg fun j _ => mul_nonneg (hI.2 i j r (x j)) (hI.2 j i (x j) r)
      have hnn2 : 0 ≤ q₀ * I.w i t := le_trans (hI.1 i r) hw
      calc I.w i r * ∏ j ∈ univ.erase i, (I.W i j r (x j) * I.W j i (x j) r)
          ≤ (q₀ * I.w i t) * ((∏ j ∈ univ.erase i, q j) *
              ∏ j ∈ univ.erase i, (I.W i j t (x j) * I.W j i (x j) t)) :=
            mul_le_mul hw hprod hnn hnn2
        _ = ρ * (I.w i t * ∏ j ∈ univ.erase i, (I.W i j t (x j) * I.W j i (x j) t)) := by
            rw [hρ]; ring
    calc I.wbase i x * I.wlocal i r x ≤ I.wbase i x * (ρ * I.wlocal i t x) :=
          mul_le_mul_of_nonneg_left hloc (I.wbase_nonneg hI i x)
      _ = ρ * (I.wbase i x * I.wlocal i t x) := by ring
  -- injective transport into the survivors
  have hinj : Set.InjOn (fun x : Config n k => Function.update x i t) A := by
    intro x hx y hy hxy
    have hx' : x i = r := (Finset.mem_filter.mp hx).2
    have hy' : y i = r := (Finset.mem_filter.mp hy).2
    funext j
    by_cases hj : j = i
    · subst hj
      rw [hx', hy']
    · have := congrFun hxy j
      simpa [Function.update_of_ne hj] using this
  have himg : A.image (fun x : Config n k => Function.update x i t) ⊆ S := by
    intro y hy
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hy
    have hxB : InBox D x := mem_boxFinset.mp (Finset.mem_filter.mp hx).1
    refine Finset.mem_filter.mpr ⟨mem_boxFinset.mpr fun j => ?_, by simpa using htr⟩
    by_cases hj : j = i
    · subst hj
      simpa using ht
    · rw [Function.update_of_ne hj]
      exact hxB j
  have htrans : ∑ x ∈ A, I.weight x ≤ ρ * ∑ x ∈ S, I.weight x := by
    calc ∑ x ∈ A, I.weight x ≤ ∑ x ∈ A, ρ * I.weight (Function.update x i t) :=
          Finset.sum_le_sum hpt
      _ = ρ * ∑ x ∈ A, I.weight (Function.update x i t) := by rw [Finset.mul_sum]
      _ = ρ * ∑ y ∈ A.image (fun x : Config n k => Function.update x i t), I.weight y := by
          rw [Finset.sum_image hinj]
      _ ≤ ρ * ∑ y ∈ S, I.weight y := by
          apply mul_le_mul_of_nonneg_left _ hρ0
          exact Finset.sum_le_sum_of_subset_of_nonneg himg fun y _ _ => I.weight_nonneg hI y
  rw [hS, hsplit]
  constructor
  · linarith
  · nlinarith

/-! ### Master Soundness Theorem (partition functions) -/

/-- **Master Soundness Theorem for partition-function certificates.**  If the kernel returns the
interval `(lo, hi)`, then `lo ≤ Z ≤ hi` for the exact rational partition sum over the box. -/
theorem zverify_sound {I : WInstance n k} (hI : I.Nonneg) :
    ∀ (c : ZCert n k) (D : Dom n k) (lo hi : ℚ), zverify c I D = some (lo, hi) →
      lo ≤ I.Z D ∧ I.Z D ≤ hi := by
  intro c
  induction c with
  | leaf l h =>
    intro D lo hi hv
    unfold zverify at hv
    split_ifs at hv with hok
    simp only [Option.some.injEq, Prod.mk.injEq] at hv
    obtain ⟨rfl, rfl⟩ := hv
    exact zleaf_sound hI D l h hok
  | branch i ch ih =>
    intro D lo hi hv
    unfold zverify at hv
    have key := foldr_addIv_sound (fun a => I.Z (D.fix i a))
      (fun a => zverify (ch a) I (D.fix i a))
      (fun a l h hval => ih a (D.fix i a) l h hval) (D i).dedup (List.nodup_dedup _) lo hi hv
    have hded : (D i).dedup.toFinset = (D i).toFinset := by
      ext a
      simp
    rw [hded] at key
    rw [I.Z_branch D i]
    exact key
  | prune i r t q₀ q rest ih =>
    intro D lo hi hv
    unfold zverify at hv
    split_ifs at hv with hok
    cases hrest : zverify rest I (D.remove i r) with
    | none => rw [hrest] at hv; simp at hv
    | some lh =>
      obtain ⟨l', h'⟩ := lh
      rw [hrest] at hv
      simp only [Option.map_some, Option.some.injEq, Prod.mk.injEq] at hv
      obtain ⟨rfl, rfl⟩ := hv
      have h1 := ih (D.remove i r) l' h' hrest
      have h2 := zprune_sound hI D i r t q₀ q hok
      have hρ0 : 0 ≤ 1 + q₀ * ∏ j ∈ univ.erase i, q j := by
        have := mul_nonneg hok.2.2.1 (Finset.prod_nonneg fun j hj => (hok.2.2.2.2 j hj).1)
        linarith
      constructor
      · linarith [h1.1, h2.1]
      · calc I.Z D ≤ (1 + q₀ * ∏ j ∈ univ.erase i, q j) * I.Z (D.remove i r) := h2.2
          _ ≤ (1 + q₀ * ∏ j ∈ univ.erase i, q j) * h' := mul_le_mul_of_nonneg_left h1.2 hρ0

/-! ### Top-level kernel: the nonnegativity side condition is checked, not assumed -/

instance (I : WInstance n k) : Decidable I.Nonneg := by
  unfold WInstance.Nonneg
  infer_instance

/-- **Top-level partition kernel**: reject instances with a negative factor, then run `zverify`. -/
def zverifyTop (c : ZCert n k) (I : WInstance n k) (D : Dom n k) : Option (ℚ × ℚ) :=
  if I.Nonneg then zverify c I D else none

/-- **Master Soundness Theorem of the top-level partition kernel** — no side condition is left to
the caller: whatever the instance and the certificate, a returned interval contains the exact
rational partition sum over the box. -/
theorem zverifyTop_sound (c : ZCert n k) (I : WInstance n k) (D : Dom n k) (lo hi : ℚ)
    (hv : zverifyTop c I D = some (lo, hi)) : lo ≤ I.Z D ∧ I.Z D ≤ hi := by
  unfold zverifyTop at hv
  split_ifs at hv with hI
  exact zverify_sound hI c D lo hi hv

/-- Acceptance by the top-level kernel means: nonnegative factors and acceptance by `zverify`. -/
theorem zverifyTop_eq_some {c : ZCert n k} {I : WInstance n k} {D : Dom n k} {r : ℚ × ℚ}
    (hv : zverifyTop c I D = some r) : I.Nonneg ∧ zverify c I D = some r := by
  unfold zverifyTop at hv
  split_ifs at hv with hI
  exact ⟨hI, hv⟩

/-! ### From rational weight instances to the real partition function -/

/-- **Enclosure theorem.**  If the rational factors of `Ilo` and `Ihi` bracket the true Boltzmann
factors `exp(-β h)`, `exp(-β J)` of a real pairwise model, then their exact rational partition
sums bracket the real partition function over the box. -/
theorem Z_encloses_partitionFn (M : PairModel ℝ (Fin n) (fun _ => Fin k)) (β : ℝ)
    (Ilo Ihi : WInstance n k) (hlo : Ilo.Nonneg)
    (hw : ∀ i a, (Ilo.w i a : ℝ) ≤ Real.exp (-β * M.h i a) ∧
      Real.exp (-β * M.h i a) ≤ (Ihi.w i a : ℝ))
    (hW : ∀ i j a b, (Ilo.W i j a b : ℝ) ≤ Real.exp (-β * M.J i j a b) ∧
      Real.exp (-β * M.J i j a b) ≤ (Ihi.W i j a b : ℝ))
    (D : Dom n k) :
    ((Ilo.Z D : ℚ) : ℝ) ≤ partitionFn β M.energy (boxFinset D) ∧
      partitionFn β M.energy (boxFinset D) ≤ ((Ihi.Z D : ℚ) : ℝ) := by
  have hexp : ∀ x : Config n k, Real.exp (-β * M.energy x) =
      (∏ i, Real.exp (-β * M.h i (x i))) *
        ∏ i, ∏ j ∈ univ.erase i, Real.exp (-β * M.J i j (x i) (x j)) := by
    intro x
    unfold PairModel.energy
    rw [mul_add, Real.exp_add, Finset.mul_sum, Real.exp_sum, Finset.mul_sum, Real.exp_sum]
    congr 1
    apply Finset.prod_congr rfl
    intro i _
    rw [Finset.mul_sum, Real.exp_sum]
  unfold partitionFn WInstance.Z WInstance.weight
  push_cast
  constructor
  · apply Finset.sum_le_sum
    intro x _
    rw [hexp x]
    apply mul_le_mul
    · exact Finset.prod_le_prod (fun i _ => by exact_mod_cast hlo.1 i (x i)) fun i _ => (hw i (x i)).1
    · apply Finset.prod_le_prod
      · intro i _
        exact Finset.prod_nonneg fun j _ => by exact_mod_cast hlo.2 i j (x i) (x j)
      · intro i _
        exact Finset.prod_le_prod (fun j _ => by exact_mod_cast hlo.2 i j (x i) (x j))
          fun j _ => (hW i j (x i) (x j)).1
    · exact Finset.prod_nonneg fun i _ =>
        Finset.prod_nonneg fun j _ => by exact_mod_cast hlo.2 i j (x i) (x j)
    · exact Finset.prod_nonneg fun i _ => (Real.exp_pos _).le
  · apply Finset.sum_le_sum
    intro x _
    rw [hexp x]
    apply mul_le_mul
    · exact Finset.prod_le_prod (fun i _ => (Real.exp_pos _).le) fun i _ => (hw i (x i)).2
    · apply Finset.prod_le_prod
      · intro i _
        exact Finset.prod_nonneg fun j _ => (Real.exp_pos _).le
      · intro i _
        exact Finset.prod_le_prod (fun j _ => (Real.exp_pos _).le) fun j _ => (hW i j (x i) (x j)).2
    · exact Finset.prod_nonneg fun i _ => Finset.prod_nonneg fun j _ => (Real.exp_pos _).le
    · exact Finset.prod_nonneg fun i _ =>
        le_trans (Real.exp_pos _).le (hw i (x i)).2

/-! ### Executable example

Three binary sites with pair factor `1/2` for equal neighbours (`exp(-β) = 1/2`, the frustrated
triangle at `β = ln 2`).  Exact value: `Z = 2·(1/8) + 6·(1/2) = 13/4`. -/

/-- Frustrated triangle in the weight domain. -/
def triangleW : WInstance 3 2 where
  w := fun _ _ => 1
  W := fun i j a b => if i < j ∧ a = b then 1 / 2 else 1

/-- Full enumeration certificate: branch on every site, exact leaves. -/
def triangleZCert : ZCert 3 2 :=
  .branch 0 fun a => .branch 1 fun b => .branch 2 fun c =>
    .leaf (fun i j => triangleW.W i j (![a, b, c] i) (![a, b, c] j))
      (fun i j => triangleW.W i j (![a, b, c] i) (![a, b, c] j))

/-- The kernel computes the exact partition sum `13/4` from the enumeration certificate. -/
theorem triangleZ_exact : zverify triangleZCert triangleW (fullDom 3 2) = some (13 / 4, 13 / 4) := by
  decide +kernel

/-- A one-leaf certificate gives the cheap factorised enclosure `[8·(1/2)^3, 8] = [1, 8]`. -/
theorem triangleZ_coarse :
    zverify (.leaf (fun i j => if i < j then 1 / 2 else 1) (fun _ _ => 1)) triangleW
      (fullDom 3 2) = some (1, 8) := by
  decide +kernel

/-- The top-level kernel (nonnegativity check included) returns the same exact value. -/
theorem triangleZ_exactTop :
    zverifyTop triangleZCert triangleW (fullDom 3 2) = some (13 / 4, 13 / 4) := by
  decide +kernel

/-- An instance with a negative one-body factor (two sites, one state each). -/
def negativeW : WInstance 2 1 where
  w := fun i _ => if i = 0 then -1 else 1
  W := fun _ _ _ _ => 2

/-- On it the bare rule checker returns the "interval" `(-1, -9)`, which does not contain the
partition sum `-4`: the hypothesis `Nonneg` of `zverify_sound` cannot be dropped … -/
theorem negativeW_unguarded :
    zverify (.leaf (fun _ _ => 1) (fun _ _ => 3)) negativeW (fullDom 2 1) = some (-1, -9) ∧
      negativeW.Z (fullDom 2 1) = -4 := by
  decide +kernel

/-- … and the top-level kernel rejects the instance for every certificate. -/
theorem negativeW_rejected (c : ZCert 2 1) : zverifyTop c negativeW (fullDom 2 1) = none := by
  have h : ¬ negativeW.Nonneg := by decide +kernel
  simp [zverifyTop, h]

end MetricChain
