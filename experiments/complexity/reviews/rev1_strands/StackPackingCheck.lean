/-
Counting core of the bin-packing reduction to multi-strand nearest-neighbour folding
(docs/complexity/STRANDS_NN_HARDNESS.md, Theorem 1, step (d)).

Abstract setting.  The template `G^B (A G^B)^(m-1)` is the set of natural numbers `p < m*(B+1)`; position `p`
lies in block `p / (B+1)` and is a `G` iff `p % (B+1) < B` (residue `B` is the spacer `A`).  Item `i` has
`a i` bases; `f i j` is the template position paired with base `j` of item `i`.

Hypotheses of the "all stacks present" case: every base of every item is paired with a `G` (`hG`), different
bases with different positions (`hinj`), and consecutive bases of an item with adjacent positions (`hadj`:
this is what "the bond between bases `j` and `j+1` lies on a stack" means).

Conclusion: the items can be assigned to the `m` blocks with total length at most `B` in each block; if the
lengths sum to `m*B`, every block is filled exactly — a solution of the exact bin-packing instance.

Checked with:  lake env lean experiments/complexity/lean/StackPacking.lean
-/
import Mathlib

namespace Complexity.StackPacking

open Finset

/-- `p` and `p+1` are in the same block if `p` is not the last position before a block boundary. -/
theorem block_succ {B p : ℕ} (h : (p + 1) % (B + 1) ≠ 0) : (p + 1) / (B + 1) = p / (B + 1) := by
  rw [Nat.succ_div]
  have : ¬ (B + 1 ∣ p + 1) := by
    intro hdvd
    exact h (Nat.mod_eq_zero_of_dvd hdvd)
  simp [this]

/-- If `p` is a `G`, then `p` and `p+1` lie in the same block. -/
theorem block_adjacent {B p : ℕ} (hp : p % (B + 1) < B) :
    (p + 1) / (B + 1) = p / (B + 1) := by
  apply block_succ
  intro h0
  -- if (p+1) % (B+1) = 0 then p % (B+1) = B, contradicting hp
  have h1 : (p % (B + 1) + 1) % (B + 1) = 0 := by
    rw [← h0, Nat.add_mod p 1 (B + 1)]
    simp
  have hlt : p % (B + 1) + 1 < B + 1 := by omega
  rw [Nat.mod_eq_of_lt hlt] at h1
  omega

variable {n m B : ℕ}

/-- All bases of an item are paired inside one block. -/
theorem same_block (a : Fin n → ℕ) (f : (i : Fin n) → Fin (a i) → ℕ)
    (hG : ∀ i j, f i j % (B + 1) < B)
    (hadj : ∀ i (j : Fin (a i)) (h : j.1 + 1 < a i),
      f i ⟨j.1 + 1, h⟩ = f i j + 1 ∨ f i j = f i ⟨j.1 + 1, h⟩ + 1)
    (i : Fin n) (j : ℕ) (hj : j < a i) (h0 : 0 < a i) :
    f i ⟨j, hj⟩ / (B + 1) = f i ⟨0, h0⟩ / (B + 1) := by
  induction j with
  | zero => rfl
  | succ k ih =>
    have hk : k < a i := Nat.lt_of_succ_lt hj
    rw [← ih hk]
    rcases hadj i ⟨k, hk⟩ hj with h | h
    · -- f (k+1) = f k + 1
      have h1 : f i ⟨k + 1, hj⟩ = f i ⟨k, hk⟩ + 1 := h
      rw [h1]
      exact block_adjacent (hG i ⟨k, hk⟩)
    · -- f k = f (k+1) + 1
      have h1 : f i ⟨k, hk⟩ = f i ⟨k + 1, hj⟩ + 1 := h
      rw [h1]
      exact (block_adjacent (hG i ⟨k + 1, hj⟩)).symm

/-- The `G` positions of block `t`. -/
def blockG (B t : ℕ) : Finset ℕ := (range B).image (fun o => t * (B + 1) + o)

theorem card_blockG (B t : ℕ) : (blockG B t).card ≤ B := by
  unfold blockG
  exact (card_image_le).trans (by simp)

theorem mem_blockG {B t p : ℕ} (h1 : p % (B + 1) < B) (h2 : p / (B + 1) = t) : p ∈ blockG B t := by
  unfold blockG
  rw [mem_image]
  refine ⟨p % (B + 1), mem_range.mpr h1, ?_⟩
  rw [← h2]
  have := Nat.div_add_mod p (B + 1)
  rw [mul_comm]
  exact this

/-- **Main statement.**  If every bond of every item lies on a stack, the items pack into the blocks. -/
theorem packing_of_all_stacked (a : Fin n → ℕ) (f : (i : Fin n) → Fin (a i) → ℕ)
    (hpos : ∀ i, 0 < a i)
    (hG : ∀ i j, f i j % (B + 1) < B)
    (hblock : ∀ i j, f i j / (B + 1) < m)
    (hinj : Function.Injective (fun x : (i : Fin n) × Fin (a i) => f x.1 x.2))
    (hadj : ∀ i (j : Fin (a i)) (h : j.1 + 1 < a i),
      f i ⟨j.1 + 1, h⟩ = f i j + 1 ∨ f i j = f i ⟨j.1 + 1, h⟩ + 1) :
    ∃ β : Fin n → Fin m, ∀ t : Fin m, ∑ i ∈ univ.filter (fun i => β i = t), a i ≤ B := by
  refine ⟨fun i => ⟨f i ⟨0, hpos i⟩ / (B + 1), hblock i ⟨0, hpos i⟩⟩, ?_⟩
  intro t
  -- the bases of the items of block t, as a finset of the sigma type
  let S : Finset ((i : Fin n) × Fin (a i)) :=
    (univ.filter (fun i : Fin n =>
      (⟨f i ⟨0, hpos i⟩ / (B + 1), hblock i ⟨0, hpos i⟩⟩ : Fin m) = t)).sigma (fun _ => univ)
  have hcard : S.card = ∑ i ∈ univ.filter (fun i : Fin n =>
      (⟨f i ⟨0, hpos i⟩ / (B + 1), hblock i ⟨0, hpos i⟩⟩ : Fin m) = t), a i := by
    simp [S, card_sigma]
  rw [← hcard]
  calc S.card = (S.image (fun x => f x.1 x.2)).card := by
        rw [card_image_of_injective _ hinj]
    _ ≤ (blockG B t.1).card := by
        apply card_le_card
        intro p hp
        rw [mem_image] at hp
        obtain ⟨x, hx, rfl⟩ := hp
        have hx' : (⟨f x.1 ⟨0, hpos x.1⟩ / (B + 1), hblock x.1 ⟨0, hpos x.1⟩⟩ : Fin m) = t := by
          have := (mem_sigma.mp hx).1
          exact (mem_filter.mp this).2
        have hb : f x.1 x.2 / (B + 1) = t.1 := by
          have h1 := same_block a f hG hadj x.1 x.2.1 x.2.2 (hpos x.1)
          have h2 : f x.1 ⟨0, hpos x.1⟩ / (B + 1) = t.1 := congrArg Fin.val hx'
          have h3 : f x.1 x.2 = f x.1 ⟨x.2.1, x.2.2⟩ := rfl
          rw [h3, h1, h2]
        exact mem_blockG (hG x.1 x.2) hb
    _ ≤ B := card_blockG B t.1

/-- If moreover the lengths sum to `m * B`, every block is filled exactly. -/
theorem exact_packing_of_all_stacked (a : Fin n → ℕ) (f : (i : Fin n) → Fin (a i) → ℕ)
    (hpos : ∀ i, 0 < a i)
    (hG : ∀ i j, f i j % (B + 1) < B)
    (hblock : ∀ i j, f i j / (B + 1) < m)
    (hinj : Function.Injective (fun x : (i : Fin n) × Fin (a i) => f x.1 x.2))
    (hadj : ∀ i (j : Fin (a i)) (h : j.1 + 1 < a i),
      f i ⟨j.1 + 1, h⟩ = f i j + 1 ∨ f i j = f i ⟨j.1 + 1, h⟩ + 1)
    (hsum : ∑ i, a i = m * B) :
    ∃ β : Fin n → Fin m, ∀ t : Fin m, ∑ i ∈ univ.filter (fun i => β i = t), a i = B := by
  obtain ⟨β, hβ⟩ := packing_of_all_stacked a f hpos hG hblock hinj hadj
  refine ⟨β, ?_⟩
  -- the block sums are each ≤ B and add up to m * B
  have htot : ∑ t : Fin m, ∑ i ∈ univ.filter (fun i => β i = t), a i = m * B := by
    rw [← hsum]
    exact (sum_fiberwise_of_maps_to (g := β) (f := a) (s := univ) (t := univ) (fun _ _ => mem_univ _))
  by_contra hne
  obtain ⟨t0, ht0⟩ := not_forall.mp hne
  have hlt : ∑ i ∈ univ.filter (fun i => β i = t0), a i < B := lt_of_le_of_ne (hβ t0) ht0
  have : ∑ t : Fin m, ∑ i ∈ univ.filter (fun i => β i = t), a i < ∑ _t : Fin m, B := by
    apply sum_lt_sum
    · intro t _
      exact hβ t
    · exact ⟨t0, mem_univ _, hlt⟩
  rw [htot] at this
  simp at this

end Complexity.StackPacking

#print axioms Complexity.StackPacking.packing_of_all_stacked
#print axioms Complexity.StackPacking.exact_packing_of_all_stacked
