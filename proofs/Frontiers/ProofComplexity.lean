import Mathlib
import proofs.CertificateAlgebra

/-!
# Proof complexity of the certificate algebra: the `sum` rule is exponentially powerful

The kernel `verify` of `proofs/CertificateAlgebra.lean` checks certificates built from four
rules: dual `leaf`, `branch`, dominance `prune` (dead-end elimination) and dual-decomposition
`sum`.  This file shows that the `sum` rule cannot be dispensed with: on `m` disjoint frustrated
triangles every certificate *without* `sum` for the optimal bound needs exponentially many
leaves, whereas `2 * m` leaves suffice with `sum`.

## Definitions

* `Cert.SumFree c` — `c` uses only `leaf`, `branch`, `prune`.
* `Cert.visited c D` — the number of leaves the kernel visits when it checks `c` on the domains
  `D` (the domain evolution mirrors `verify`); `Cert.visited_le_size` compares it with the
  syntactic `Cert.size` on duplicate-free domains.
* `triangles m : PairInstance (m * 3) 2` — `m` disjoint frustrated triangles on `m * 3` binary
  sites (`blockOf i` is the triangle of site `i`, `blockSite q r` the `r`-th site of triangle `q`);
  cost `1` for every in-block pair of equal states.  Its optimum is `m`
  (`triangles_energy_ge`, `triangles_energy_opt`), and `triangles 1 = triangle`.

## Main results

* `leaf_two_config` — **two-configuration weak duality**: a dual leaf with bound `L` valid on a
  box satisfies `4 L ≤ 2 Σ_i (h_i(x_i) + h_i(x'_i)) + Σ_{i ≠ j} Pat_ij` for any two
  configurations `x, x'` of the box and any crossing pattern `χ`, where every pair is evaluated
  either consistently, `Pat_ij = Jsym(x_i, x_j) + Jsym(x'_i, x'_j)`, or crossed,
  `Pat_ij = Jsym(x_i, x'_j) + Jsym(x'_i, x_j)`.
* `triangle_leaf_gap`, `triangle_no_leaf_certificate` — **LP integrality gap**: on the full box of
  the frustrated triangle every dual leaf certifies at most `0`, although the optimum is `1`.
* `sumFree_exponential` — **exponential lower bound**: a sum-free certificate accepted for the
  optimal bound `m` of `triangles m` visits at least `2 ^ m` leaves (dominance steps included);
  `sumFree_size_exponential` is the same bound for `Cert.size`.  More generally
  (`sumFree_gap_exponential`) a sum-free certificate for any bound `L ≥ m - d` visits at least
  `2 ^ (m - d)` leaves: an additive gap `d` only saves a factor `2 ^ d`.
* `sumFree_complexity`, `sumFree_tight` — the bounds are attained: for every `K ≤ m` the least
  number of leaves of a sum-free certificate for the bound `K` is exactly `2 ^ K` (branch on one
  site in each of `K` triangles, then one dual leaf).
* `peelCert_verified`, `peelCert_visited`, `sum_linear` — **linear upper bound with `sum`**: the
  peeling certificate (split off one triangle with `sum`, branch once, two dual leaves) is
  accepted for the bound `m` and visits `2 * m` leaves for `m ≥ 1` (for `m = 0` there are no
  sites and one trivial leaf is needed, `peelCert_visited_le`); its size is `4 * m - 1`.
* `sum_rule_separation` — for `m ≥ 3` the certificate with `sum` beats every sum-free one.

## Proof of the lower bound

Call a block *untouched* by `D` if all its sites still have both states, and call `D` *good* if
its box contains a configuration with no monochromatic block.  By induction on the certificate,
a sum-free certificate accepted on a good `D` for a bound `L ≥ m - d` visits at least
`2 ^ (#untouched - d)` leaves:

* *leaf*: apply `leaf_two_config` to the good witness `x`, to `x'` := `x` complemented on the
  untouched blocks, and to the pattern that crosses the agreeing pairs of untouched blocks.  All
  pattern terms of untouched blocks vanish, touched blocks contribute at most `4` each, hence
  `4 L ≤ 4 (m - #untouched)`: at most `d` blocks are untouched (none for `L = m`).
* *branch* on a site of an untouched block: both children are checked, both child domains are
  good (flip the witness on the block) and have one untouched block less.  On a site of a touched
  block: follow the witness.
* *prune* (`prune_obstruction`): the Goldstein margin of a state against its dominator is negative
  as soon as the box contains a configuration in which all block-mates are in the dominating
  state.  Hence dominance never fires in an untouched block, and in a touched block it preserves
  goodness and the set of untouched blocks.

The separation is the tree-like versus DAG-like phenomenon known for branch-and-bound (Jeroslow
1974; Basu, Conforti, Di Summa, Jiang 2023, for the same family in the stable-set formulation;
see `docs/THEORY_REPORT.md`, §6.3); here it is established for this kernel, i.e. for LP-dual
leaves together with dominance steps.
-/

namespace MetricChain

open Finset

variable {n k : ℕ}

/-! ### Sum-free certificates and the number of visited leaves -/

/-- A certificate is *sum-free* if it is built from `leaf`, `branch` and `prune` only. -/
def Cert.SumFree : Cert n k → Prop
  | .leaf _ _ _ => True
  | .branch _ ch => ∀ a, (ch a).SumFree
  | .prune _ _ _ _ rest => rest.SumFree
  | .sum _ _ _ _ _ _ => False

/-- Number of leaves the kernel actually visits when it checks a certificate on the domains `D`
(the domain evolution mirrors `verify`). -/
def Cert.visited : Cert n k → Dom n k → ℕ
  | .leaf _ _ _, _ => 1
  | .branch i ch, D => ((D i).map fun a => (ch a).visited (D.fix i a)).sum
  | .prune i r _ _ rest, D => rest.visited (D.remove i r)
  | .sum _ _ _ _ c₁ c₂, D => c₁.visited D + c₂.visited D

/-- On duplicate-free domains the kernel visits at most `Cert.size` leaves. -/
theorem Cert.visited_le_size (c : Cert n k) (D : Dom n k) (hD : ∀ i, (D i).Nodup) :
    c.visited D ≤ c.size := by
  induction c generalizing D with
  | leaf u p msg =>
    simp [Cert.visited, Cert.size]
  | branch i ch ih =>
    simp only [Cert.visited, Cert.size]
    have h1 : ((D i).map fun a => (ch a).visited (D.fix i a)).sum ≤
        ((D i).map fun a => (ch a).size).sum := by
      apply List.sum_le_sum
      intro a _
      apply ih a
      intro j
      unfold Dom.fix
      by_cases hj : j = i
      · subst hj
        simp
      · rw [Function.update_of_ne hj]
        exact hD j
    have h2 : ((D i).map fun a => (ch a).size).sum = ∑ a ∈ (D i).toFinset, (ch a).size :=
      (List.sum_toFinset _ (hD i)).symm
    have h3 : ∑ a ∈ (D i).toFinset, (ch a).size ≤ ∑ a, (ch a).size :=
      Finset.sum_le_sum_of_subset (Finset.subset_univ _)
    omega
  | prune i r t ℓ rest ih =>
    simp only [Cert.visited, Cert.size]
    have h1 := ih (D.remove i r) (by
      intro j
      unfold Dom.remove
      by_cases hj : j = i
      · subst hj
        simp only [Function.update_self]
        exact (hD j).filter _
      · rw [Function.update_of_ne hj]
        exact hD j)
    omega
  | sum I₁ I₂ L₁ L₂ c₁ c₂ ih₁ ih₂ =>
    simp only [Cert.visited, Cert.size]
    have h1 := ih₁ D hD
    have h2 := ih₂ D hD
    omega

/-! ### Two-configuration weak duality for dual leaves -/

/-- Symmetrised pair table: both orientations of the unordered pair `{i, j}`. -/
def PairInstance.Jsym (I : PairInstance n k) (i j : Fin n) (a b : Fin k) : ℚ :=
  I.J i j a b + I.J j i b a

/-- **Two-configuration weak duality.**  A dual leaf valid on the box `D` is bounded by the
average of *two* configurations `x, x'` of the box, where every pair `{i, j}` may independently be
evaluated either consistently (`(x, x)` and `(x', x')`) or crossed (`(x, x')` and `(x', x)`). -/
theorem leaf_two_config (I : PairInstance n k) (D : Dom n k) (L : ℚ) (u : Fin n → ℚ)
    (p : Fin n → Fin n → ℚ) (msg : Fin n → Fin n → Fin k → ℚ) (h : LeafOK I D L u p msg)
    (x x' : Config n k) (hx : InBox D x) (hx' : InBox D x') (χ : Fin n → Fin n → Bool) :
    4 * L ≤ 2 * ∑ i, (I.h i (x i) + I.h i (x' i)) +
      ∑ i, ∑ j ∈ univ.erase i,
        (if χ i j then I.Jsym i j (x i) (x' j) + I.Jsym i j (x' i) (x j)
          else I.Jsym i j (x i) (x j) + I.Jsym i j (x' i) (x' j)) := by
  obtain ⟨hu, hp, hL⟩ := h
  have h1 : 2 * ∑ i, u i ≤ ∑ i, (I.h i (x i) + I.h i (x' i)) +
      ∑ i, ∑ j ∈ univ.erase i, (msg i j (x i) + msg i j (x' i)) := by
    rw [Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_le_sum
    intro i _
    have a1 := hu i (x i) (hx i)
    have a2 := hu i (x' i) (hx' i)
    rw [Finset.sum_add_distrib]
    linarith
  have h2 : ∑ i, ∑ j ∈ univ.erase i, 4 * p i j ≤
      ∑ i, ∑ j ∈ univ.erase i,
        ((if χ i j then I.Jsym i j (x i) (x' j) + I.Jsym i j (x' i) (x j)
          else I.Jsym i j (x i) (x j) + I.Jsym i j (x' i) (x' j)) -
          (msg i j (x i) + msg i j (x' i)) - (msg j i (x j) + msg j i (x' j))) := by
    apply Finset.sum_le_sum
    intro i _
    apply Finset.sum_le_sum
    intro j hj
    unfold PairInstance.Jsym
    cases χ i j
    · have b1 := hp i j hj (x i) (hx i) (x j) (hx j)
      have b2 := hp i j hj (x' i) (hx' i) (x' j) (hx' j)
      simp only [Bool.false_eq_true, if_false]
      linarith
    · have b1 := hp i j hj (x i) (hx i) (x' j) (hx' j)
      have b2 := hp i j hj (x' i) (hx' i) (x j) (hx j)
      simp only [if_true]
      linarith
  have h3 := sum_erase_swap (fun i j => msg i j (x i) + msg i j (x' i))
  have h4 : ∑ i, ∑ j ∈ univ.erase i, 4 * p i j = 4 * ∑ i, ∑ j ∈ univ.erase i, p i j := by
    simp only [Finset.mul_sum]
  simp only [Finset.sum_sub_distrib] at h2
  rw [h3, h4] at h2
  linarith

/-- **LP integrality gap of the frustrated triangle.**  No dual leaf can certify a positive bound
for the triangle on the full box (take the two constant configurations and cross every pair). -/
theorem triangle_leaf_gap (L : ℚ) (u : Fin 3 → ℚ) (p : Fin 3 → Fin 3 → ℚ)
    (msg : Fin 3 → Fin 3 → Fin 2 → ℚ) (h : LeafOK triangle (fullDom 3 2) L u p msg) : L ≤ 0 := by
  have key := leaf_two_config triangle (fullDom 3 2) L u p msg h (fun _ => 0) (fun _ => 1)
    (inBox_fullDom _) (inBox_fullDom _) (fun _ _ => true)
  have hval : (2 * ∑ i : Fin 3, (triangle.h i 0 + triangle.h i 1) +
      ∑ i : Fin 3, ∑ j ∈ univ.erase i,
        (if (true : Bool) then triangle.Jsym i j 0 1 + triangle.Jsym i j 1 0
          else triangle.Jsym i j 0 0 + triangle.Jsym i j 1 1)) = 0 := by decide +kernel
  have key' : 4 * L ≤ 0 := by
    rw [← hval]
    exact key
  linarith

/-- A dual leaf alone never certifies the optimum `1` of the frustrated triangle
(`triangle_lower_bound`): pure reparameterisation certificates are incomplete. -/
theorem triangle_no_leaf_certificate (u : Fin 3 → ℚ) (p : Fin 3 → Fin 3 → ℚ)
    (msg : Fin 3 → Fin 3 → Fin 2 → ℚ) :
    verify (.leaf u p msg) triangle (fullDom 3 2) 1 = false := by
  by_contra hne
  have hv : verify (.leaf u p msg) triangle (fullDom 3 2) 1 = true := by simpa using hne
  simp only [verify, decide_eq_true_eq] at hv
  have := triangle_leaf_gap 1 u p msg hv
  norm_num at this

/-! ### The hard family: `m` disjoint frustrated triangles -/

section Triangles

variable {m : ℕ}

/-- The `r`-th site of block `q`. -/
def blockSite (q : Fin m) (r : Fin 3) : Fin (m * 3) := finProdFinEquiv (q, r)

/-- The block (triangle) containing a site. -/
def blockOf (i : Fin (m * 3)) : Fin m := (finProdFinEquiv.symm i).1

/-- The position of a site inside its block. -/
def posOf (i : Fin (m * 3)) : Fin 3 := (finProdFinEquiv.symm i).2

@[simp] theorem blockOf_blockSite (q : Fin m) (r : Fin 3) : blockOf (blockSite q r) = q := by
  simp [blockOf, blockSite]

@[simp] theorem posOf_blockSite (q : Fin m) (r : Fin 3) : posOf (blockSite q r) = r := by
  simp [posOf, blockSite]

@[simp] theorem blockSite_blockOf_posOf (i : Fin (m * 3)) : blockSite (blockOf i) (posOf i) = i :=
  finProdFinEquiv.apply_symm_apply i

theorem eq_blockSite_of_blockOf {i : Fin (m * 3)} {q : Fin m} (h : blockOf i = q) :
    i = blockSite q (posOf i) := by
  rw [← h, blockSite_blockOf_posOf]

/-- Every site has another site in its block. -/
theorem exists_blockmate (i : Fin (m * 3)) : ∃ j, j ≠ i ∧ blockOf j = blockOf i := by
  refine ⟨blockSite (blockOf i) (posOf i + 1), ?_, blockOf_blockSite _ _⟩
  intro h
  have h2 := congrArg posOf h
  rw [posOf_blockSite] at h2
  revert h2
  generalize posOf i = r
  revert r
  decide

/-- Row sums over the other sites reduce to the block when the summand is supported there. -/
theorem sum_erase_block (i : Fin (m * 3)) (f : Fin (m * 3) → ℚ)
    (hf : ∀ j, blockOf j ≠ blockOf i → f j = 0) :
    ∑ j ∈ univ.erase i, f j = ∑ r : Fin 3, f (blockSite (blockOf i) r) - f i := by
  rw [Finset.sum_erase_eq_sub (Finset.mem_univ i)]
  congr 1
  rw [← (finProdFinEquiv (m := m) (n := 3)).sum_comp f, Fintype.sum_prod_type,
    Finset.sum_eq_single (blockOf i)]
  · rfl
  · intro q _ hq
    exact Finset.sum_eq_zero fun r _ => hf _ (by
      change blockOf (blockSite q r) ≠ blockOf i
      rw [blockOf_blockSite]
      exact hq)
  · intro h
    exact absurd (Finset.mem_univ _) h

/-- Sums over ordered pairs of distinct sites decompose over the blocks when the summand
vanishes across blocks. -/
theorem sum_pairs_blocks (F : Fin (m * 3) → Fin (m * 3) → ℚ)
    (hF : ∀ i j, blockOf j ≠ blockOf i → F i j = 0) :
    ∑ i, ∑ j ∈ univ.erase i, F i j =
      ∑ q : Fin m, (F (blockSite q 0) (blockSite q 1) + F (blockSite q 0) (blockSite q 2) +
        F (blockSite q 1) (blockSite q 0) + F (blockSite q 1) (blockSite q 2) +
        F (blockSite q 2) (blockSite q 0) + F (blockSite q 2) (blockSite q 1)) := by
  have hrow : ∀ i, ∑ j ∈ univ.erase i, F i j =
      ∑ r : Fin 3, F i (blockSite (blockOf i) r) - F i i :=
    fun i => sum_erase_block i (F i) (hF i)
  rw [← (finProdFinEquiv (m := m) (n := 3)).sum_comp, Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro q _
  have e : ∀ r : Fin 3, finProdFinEquiv (q, r) = blockSite q r := fun _ => rfl
  simp only [Fin.sum_univ_three, hrow, e, blockOf_blockSite]
  ring

/-- `m` disjoint frustrated triangles on `m * 3` binary sites: cost `1` for every pair of sites
of the same block that agree (each unordered pair stored once, in the orientation `i < j`). -/
def triangles (m : ℕ) : PairInstance (m * 3) 2 where
  h := fun _ _ => 0
  J := fun i j a b => if blockOf i = blockOf j ∧ i < j ∧ a = b then 1 else 0

/-- For `m = 1` the family is the frustrated triangle of `CertificateAlgebra.lean`. -/
theorem triangles_one : triangles 1 = triangle := by
  unfold triangles triangle
  congr 1
  funext i j a b
  simp [Subsingleton.elim (blockOf i) (blockOf j)]

/-- The symmetrised pair table of the family: `1` exactly on agreeing pairs inside a block. -/
theorem triangles_Jsym (m : ℕ) {i j : Fin (m * 3)} (hij : i ≠ j) (a b : Fin 2) :
    (triangles m).Jsym i j a b = if blockOf i = blockOf j ∧ a = b then 1 else 0 := by
  simp only [PairInstance.Jsym, triangles]
  rcases lt_or_gt_of_ne hij with h | h
  · have h' : ¬ j < i := not_lt_of_gt h
    by_cases hb : blockOf i = blockOf j <;> by_cases hab : a = b <;>
      simp [h, h', hb, hab, eq_comm]
  · have h' : ¬ i < j := not_lt_of_gt h
    by_cases hb : blockOf i = blockOf j <;> by_cases hab : a = b <;>
      simp [h, h', hb, hab, eq_comm]

/-- Goldstein link of the triangle family: only the block of `i` contributes. -/
theorem triangles_link (m : ℕ) {i j : Fin (m * 3)} (hij : i ≠ j) (r t s : Fin 2) :
    (triangles m).link i r t j s =
      (if blockOf i = blockOf j ∧ r = s then 1 else 0) -
        (if blockOf i = blockOf j ∧ t = s then 1 else 0) := by
  rw [← triangles_Jsym m hij r s, ← triangles_Jsym m hij t s]
  unfold PairInstance.link PairInstance.Jsym
  ring

/-- The energy of the triangle family, block by block. -/
theorem triangles_energy (m : ℕ) (x : Config (m * 3) 2) :
    (triangles m).energy x = ∑ q : Fin m,
      ((if x (blockSite q 0) = x (blockSite q 1) then (1 : ℚ) else 0) +
        (if x (blockSite q 0) = x (blockSite q 2) then 1 else 0) +
        (if x (blockSite q 1) = x (blockSite q 2) then 1 else 0)) := by
  let G : Fin (m * 3) → Fin (m * 3) → ℚ := fun i j =>
    if blockOf i = blockOf j ∧ x i = x j then 1 else 0
  have h1 : ∑ i, ∑ j ∈ univ.erase i,
      ((triangles m).J i j (x i) (x j) + (triangles m).J j i (x j) (x i)) =
      ∑ i, ∑ j ∈ univ.erase i, G i j := by
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j hj => ?_
    exact triangles_Jsym m (Finset.ne_of_mem_erase hj).symm (x i) (x j)
  have h2 := sum_erase_swap (fun i j => (triangles m).J i j (x i) (x j))
  have h3 : ∑ i, ∑ j ∈ univ.erase i,
      ((triangles m).J i j (x i) (x j) + (triangles m).J j i (x j) (x i)) =
      2 * ∑ i, ∑ j ∈ univ.erase i, (triangles m).J i j (x i) (x j) := by
    simp only [Finset.sum_add_distrib]
    rw [h2]
    ring
  have hGz : ∀ i j, blockOf j ≠ blockOf i → G i j = 0 := by
    intro i j hb
    have hb' : ¬ blockOf i = blockOf j := fun e => hb e.symm
    simp [G, hb']
  have h4 := sum_pairs_blocks G hGz
  have h5 : ∀ q : Fin m,
      G (blockSite q 0) (blockSite q 1) + G (blockSite q 0) (blockSite q 2) +
        G (blockSite q 1) (blockSite q 0) + G (blockSite q 1) (blockSite q 2) +
        G (blockSite q 2) (blockSite q 0) + G (blockSite q 2) (blockSite q 1) =
      2 * ((if x (blockSite q 0) = x (blockSite q 1) then (1 : ℚ) else 0) +
        (if x (blockSite q 0) = x (blockSite q 2) then 1 else 0) +
        (if x (blockSite q 1) = x (blockSite q 2) then 1 else 0)) := by
    intro q
    simp only [G, blockOf_blockSite, true_and]
    rw [if_congr (eq_comm (a := x (blockSite q 1)) (b := x (blockSite q 0))) rfl rfl,
      if_congr (eq_comm (a := x (blockSite q 2)) (b := x (blockSite q 0))) rfl rfl,
      if_congr (eq_comm (a := x (blockSite q 2)) (b := x (blockSite q 1))) rfl rfl]
    ring
  have h6 : (triangles m).energy x =
      ∑ i, ∑ j ∈ univ.erase i, (triangles m).J i j (x i) (x j) := by
    unfold PairInstance.energy
    simp [triangles]
  rw [h1, h4, Finset.sum_congr rfl (fun q _ => h5 q), ← Finset.mul_sum] at h3
  rw [h6]
  linarith

/-- Every configuration of `m` disjoint frustrated triangles has energy at least `m` … -/
theorem triangles_energy_ge (m : ℕ) (x : Config (m * 3) 2) :
    (m : ℚ) ≤ (triangles m).energy x := by
  rw [triangles_energy]
  have key : ∀ a b c : Fin 2, (1 : ℚ) ≤ (if a = b then (1 : ℚ) else 0) +
      (if a = c then 1 else 0) + (if b = c then 1 else 0) := by decide +kernel
  have h := Finset.sum_le_sum (fun q (_ : q ∈ (univ : Finset (Fin m))) =>
    key (x (blockSite q 0)) (x (blockSite q 1)) (x (blockSite q 2)))
  simpa using h

/-- … and the bound is attained (first site of every block in state `1`, the others in state
`0`): the optimum of the family is exactly `m`. -/
theorem triangles_energy_opt (m : ℕ) :
    (triangles m).energy (fun i => if posOf i = 0 then 1 else 0) = (m : ℚ) := by
  rw [triangles_energy]
  simp

end Triangles

/-! ### Lower bound for sum-free certificates -/

section LowerBound

variable {m : ℕ}

/-- Block `q` is *untouched* by the domains `D` if every site of the block still has both
states available. -/
def Untouched (D : Dom (m * 3) 2) (q : Fin m) : Prop :=
  ∀ i, blockOf i = q → ∀ a : Fin 2, a ∈ D i

instance (D : Dom (m * 3) 2) : DecidablePred (Untouched D) := fun q => by
  unfold Untouched
  infer_instance

/-- Number of untouched blocks. -/
def untouchedCount (D : Dom (m * 3) 2) : ℕ := (univ.filter (Untouched D)).card

/-- The domains `D` are *good* if the box contains a configuration under which no block is
monochromatic (so that every block has exactly one agreeing pair). -/
def GoodDom (D : Dom (m * 3) 2) : Prop :=
  ∃ x : Config (m * 3) 2, InBox D x ∧ ∀ q, ∃ i j, blockOf i = q ∧ blockOf j = q ∧ x i ≠ x j

theorem untouched_update_of_ne {D : Dom (m * 3) 2} {i : Fin (m * 3)} {q : Fin m}
    (hq : q ≠ blockOf i) (l : List (Fin 2)) :
    Untouched (Function.update D i l) q ↔ Untouched D q := by
  unfold Untouched
  refine forall_congr' fun j => imp_congr_right fun hj => ?_
  have hji : j ≠ i := by
    rintro rfl
    exact hq hj.symm
  rw [Function.update_of_ne hji]

theorem untouched_update_mono {D : Dom (m * 3) 2} {i : Fin (m * 3)} (l : List (Fin 2))
    (hl : ∀ a ∈ l, a ∈ D i) {q : Fin m} (h : Untouched (Function.update D i l) q) :
    Untouched D q := by
  intro j hj a
  have h1 := h j hj a
  by_cases hji : j = i
  · subst hji
    rw [Function.update_self] at h1
    exact hl a h1
  · rwa [Function.update_of_ne hji] at h1

/-- Shrinking the domain of a site in a touched block does not change the number of untouched
blocks. -/
theorem untouchedCount_update_touched {D : Dom (m * 3) 2} {i : Fin (m * 3)} (l : List (Fin 2))
    (hl : ∀ a ∈ l, a ∈ D i) (hT : ¬ Untouched D (blockOf i)) :
    untouchedCount (Function.update D i l) = untouchedCount D := by
  unfold untouchedCount
  congr 1
  apply Finset.filter_congr
  intro q _
  by_cases hq : q = blockOf i
  · subst hq
    exact ⟨fun h => untouched_update_mono l hl h, fun h => absurd h hT⟩
  · exact untouched_update_of_ne hq l

/-- Fixing a site of an untouched block touches exactly that block. -/
theorem untouchedCount_fix_untouched {D : Dom (m * 3) 2} {i : Fin (m * 3)} (a : Fin 2)
    (hU : Untouched D (blockOf i)) :
    untouchedCount (D.fix i a) + 1 = untouchedCount D := by
  unfold untouchedCount
  have hnot : ¬ Untouched (D.fix i a) (blockOf i) := by
    intro h
    have h1 := h i rfl (Fin.rev a)
    unfold Dom.fix at h1
    rw [Function.update_self, List.mem_singleton] at h1
    have key : ∀ b : Fin 2, Fin.rev b ≠ b := by decide
    exact key a h1
  have heq : univ.filter (Untouched D) =
      insert (blockOf i) (univ.filter (Untouched (D.fix i a))) := by
    ext q
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert]
    by_cases hq : q = blockOf i
    · subst hq
      simp [hU]
    · simp only [hq, false_or]
      exact (untouched_update_of_ne hq [a]).symm
  rw [heq, Finset.card_insert_of_notMem (by simp [hnot])]

theorem untouchedCount_fullDom (m : ℕ) : untouchedCount (fullDom (m * 3) 2) = m := by
  unfold untouchedCount
  rw [Finset.filter_true_of_mem, Finset.card_univ, Fintype.card_fin]
  intro q _ i _ a
  exact List.mem_finRange a

theorem goodDom_fullDom (m : ℕ) : GoodDom (fullDom (m * 3) 2) := by
  refine ⟨fun i => if posOf i = 0 then 1 else 0, inBox_fullDom _, fun q => ?_⟩
  refine ⟨blockSite q 0, blockSite q 1, blockOf_blockSite _ _, blockOf_blockSite _ _, ?_⟩
  simp

/-- Both children of a branching on a site of an untouched block are good: flip the witness on
the whole block if necessary. -/
theorem goodDom_fix_untouched {D : Dom (m * 3) 2} {i : Fin (m * 3)}
    (hU : Untouched D (blockOf i)) (hG : GoodDom D) (a : Fin 2) : GoodDom (D.fix i a) := by
  obtain ⟨x, hx, hmono⟩ := hG
  by_cases hxa : x i = a
  · exact ⟨x, hxa ▸ inBox_fix hx i, hmono⟩
  · refine ⟨fun j => if blockOf j = blockOf i then Fin.rev (x j) else x j, ?_, ?_⟩
    · intro j
      by_cases hji : j = i
      · subst hji
        unfold Dom.fix
        rw [Function.update_self, List.mem_singleton]
        simp only [if_true]
        have key : ∀ b c : Fin 2, b ≠ c → Fin.rev b = c := by decide
        exact key _ _ hxa
      · unfold Dom.fix
        rw [Function.update_of_ne hji]
        by_cases hb : blockOf j = blockOf i
        · simp only [hb, if_true]
          exact hU j hb _
        · simp only [hb, if_false]
          exact hx j
    · intro q
      obtain ⟨i₁, j₁, h1, h2, hne⟩ := hmono q
      refine ⟨i₁, j₁, h1, h2, ?_⟩
      simp only [h1, h2]
      by_cases hq : q = blockOf i
      · simp only [hq, if_true]
        exact fun h => hne (Fin.rev_injective h)
      · simp only [hq, if_false]
        exact hne

/-! #### The prune rule cannot touch an untouched block -/

/-- **Key obstruction for dominance pruning.**  A valid prune step `r ↦ t` at site `i` is
impossible as soon as the box contains (away from `i`) a configuration in which all block-mates
of `i` are in state `t`: the Goldstein margin would be negative. -/
theorem prune_obstruction {D : Dom (m * 3) 2} {i : Fin (m * 3)} {r t : Fin 2}
    {ℓ : Fin (m * 3) → ℚ} (hp : PruneOK (triangles m) D i r t ℓ 0) (y : Config (m * 3) 2)
    (hyD : ∀ j, j ≠ i → y j ∈ D j) (hyt : ∀ j, j ≠ i → blockOf j = blockOf i → y j = t) :
    False := by
  obtain ⟨_, htr, hℓ, hmargin⟩ := hp
  obtain ⟨j₀, hj₀i, hj₀b⟩ := exists_blockmate i
  have hj₀ : j₀ ∈ univ.erase i := Finset.mem_erase.mpr ⟨hj₀i, Finset.mem_univ _⟩
  have hle : ∀ j ∈ univ.erase i, ℓ j ≤ if blockOf j = blockOf i then -1 else 0 := by
    intro j hj
    have hji : j ≠ i := Finset.ne_of_mem_erase hj
    have h1 := hℓ j hj (y j) (hyD j hji)
    rw [triangles_link m hji.symm] at h1
    by_cases hb : blockOf j = blockOf i
    · have hrt : ¬ r = t := fun h => htr h.symm
      rw [hyt j hji hb] at h1
      simpa [hb, hrt] using h1
    · have hb' : ¬ blockOf i = blockOf j := fun h => hb h.symm
      simpa [hb, hb'] using h1
  have h2 : ∑ j ∈ univ.erase i, ℓ j ≤
      ∑ j ∈ univ.erase i, (if blockOf j = blockOf i then (-1 : ℚ) else 0) :=
    Finset.sum_le_sum hle
  have h3 : ∑ j ∈ univ.erase i, (if blockOf j = blockOf i then (-1 : ℚ) else 0) ≤ -1 := by
    rw [← Finset.add_sum_erase _ _ hj₀]
    have h4 : ∑ j ∈ (univ.erase i).erase j₀,
        (if blockOf j = blockOf i then (-1 : ℚ) else 0) ≤ 0 :=
      Finset.sum_nonpos fun j _ => by split_ifs <;> norm_num
    simp only [hj₀b, if_true]
    linarith
  have h5 : (triangles m).h i r = 0 := rfl
  have h6 : (triangles m).h i t = 0 := rfl
  rw [h5, h6] at hmargin
  linarith

/-- A valid prune step acts on a touched block. -/
theorem prune_touched {D : Dom (m * 3) 2} {i : Fin (m * 3)} {r t : Fin 2}
    {ℓ : Fin (m * 3) → ℚ} (hp : PruneOK (triangles m) D i r t ℓ 0) (hG : GoodDom D) :
    ¬ Untouched D (blockOf i) := by
  intro hU
  obtain ⟨x, hx, -⟩ := hG
  refine prune_obstruction hp (fun j => if blockOf j = blockOf i then t else x j) ?_ ?_
  · intro j _
    by_cases hb : blockOf j = blockOf i
    · simp only [hb, if_true]
      exact hU j hb t
    · simp only [hb, if_false]
      exact hx j
  · intro j _ hb
    simp only [hb, if_true]

/-- A valid prune step preserves goodness. -/
theorem goodDom_remove {D : Dom (m * 3) 2} {i : Fin (m * 3)} {r t : Fin 2}
    {ℓ : Fin (m * 3) → ℚ} (hp : PruneOK (triangles m) D i r t ℓ 0) (hG : GoodDom D) :
    GoodDom (D.remove i r) := by
  obtain ⟨x, hx, hmono⟩ := hG
  by_cases hxr : x i = r
  · refine ⟨Function.update x i t, inBox_remove_update hx i r t hp.1 hp.2.1, ?_⟩
    intro q
    by_contra hcon
    push Not at hcon
    by_cases hq : q = blockOf i
    · subst hq
      refine prune_obstruction hp x (fun j _ => hx j) ?_
      intro j hji hb
      have h1 := hcon j i hb rfl
      rwa [Function.update_self, Function.update_of_ne hji] at h1
    · obtain ⟨i₁, j₁, h1, h2, hne⟩ := hmono q
      have hi₁ : i₁ ≠ i := by
        rintro rfl
        exact hq h1.symm
      have hj₁ : j₁ ≠ i := by
        rintro rfl
        exact hq h2.symm
      have h3 := hcon i₁ j₁ h1 h2
      rw [Function.update_of_ne hi₁, Function.update_of_ne hj₁] at h3
      exact hne h3
  · exact ⟨x, inBox_remove_of_ne hx i r hxr, hmono⟩

/-! #### Dual leaves need every block to be touched -/

/-- A block that is not monochromatic, in terms of its three sites. -/
theorem not_mono_blockSite {x : Config (m * 3) 2} {q : Fin m}
    (h : ∃ i j, blockOf i = q ∧ blockOf j = q ∧ x i ≠ x j) :
    ¬ (x (blockSite q 0) = x (blockSite q 1) ∧ x (blockSite q 1) = x (blockSite q 2)) := by
  rintro ⟨h01, h12⟩
  obtain ⟨i, j, hi, hj, hne⟩ := h
  have hall : ∀ r : Fin 3, x (blockSite q r) = x (blockSite q 0) := by
    intro r
    fin_cases r
    · rfl
    · exact h01.symm
    · exact (h01.trans h12).symm
  apply hne
  rw [eq_blockSite_of_blockOf hi, eq_blockSite_of_blockOf hj, hall, hall (posOf j)]

/-- In a non-monochromatic binary triangle exactly one unordered pair agrees. -/
theorem triangle_pairs_le (a b c : Fin 2) (h : ¬ (a = b ∧ b = c)) :
    (if a = b then (2 : ℚ) else 0) + (if a = c then 2 else 0) + (if b = a then 2 else 0) +
      (if b = c then 2 else 0) + (if c = a then 2 else 0) + (if c = b then 2 else 0) ≤ 4 := by
  revert a b c
  decide +kernel

/-- **Leaf lemma.**  A dual leaf on a good box loses one unit for every untouched block: it
certifies at most `m - #untouched`.  In particular a leaf certifying the optimum `m` forces every
block to be touched. -/
theorem leaf_untouchedCount_le {D : Dom (m * 3) 2} {L : ℚ} {u : Fin (m * 3) → ℚ}
    {p : Fin (m * 3) → Fin (m * 3) → ℚ} {msg : Fin (m * 3) → Fin (m * 3) → Fin 2 → ℚ}
    (h : LeafOK (triangles m) D L u p msg) (hG : GoodDom D) :
    (untouchedCount D : ℚ) ≤ (m : ℚ) - L := by
  obtain ⟨x, hx, hmono⟩ := hG
  -- second configuration: complement on the untouched blocks
  let x' : Config (m * 3) 2 := fun i => if Untouched D (blockOf i) then Fin.rev (x i) else x i
  have hx' : InBox D x' := by
    intro i
    by_cases hU : Untouched D (blockOf i)
    · exact hU i rfl _
    · simp only [x', hU, if_false]
      exact hx i
  -- crossing pattern: agreeing pairs inside untouched blocks
  let χ : Fin (m * 3) → Fin (m * 3) → Bool := fun i j =>
    decide (blockOf i = blockOf j ∧ Untouched D (blockOf i) ∧ x i = x j)
  have key := leaf_two_config (triangles m) D L u p msg h x x' hx hx' χ
  have hh : ∑ i, ((triangles m).h i (x i) + (triangles m).h i (x' i)) = 0 := by
    simp [triangles]
  -- the pattern terms: `2` on agreeing pairs of touched blocks, `0` otherwise
  let F : Fin (m * 3) → Fin (m * 3) → ℚ := fun i j =>
    if blockOf j = blockOf i ∧ ¬ Untouched D (blockOf i) ∧ x i = x j then 2 else 0
  have hrev : ∀ a : Fin 2, Fin.rev a ≠ a := by decide
  have hpat : ∀ i, ∀ j ∈ univ.erase i,
      (if χ i j then (triangles m).Jsym i j (x i) (x' j) + (triangles m).Jsym i j (x' i) (x j)
        else (triangles m).Jsym i j (x i) (x j) + (triangles m).Jsym i j (x' i) (x' j)) =
        F i j := by
    intro i j hj
    have hij : i ≠ j := (Finset.ne_of_mem_erase hj).symm
    rw [triangles_Jsym m hij, triangles_Jsym m hij, triangles_Jsym m hij, triangles_Jsym m hij]
    by_cases hb : blockOf i = blockOf j
    · by_cases hU : Untouched D (blockOf i)
      · have hUj : Untouched D (blockOf j) := hb ▸ hU
        by_cases hxx : x i = x j
        · have e1 : ¬ x j = Fin.rev (x j) := fun e => hrev _ e.symm
          simp [χ, F, x', hb, hUj, hxx, hrev, e1]
        · have e1 : ¬ Fin.rev (x i) = Fin.rev (x j) := fun e => hxx (Fin.rev_injective e)
          simp [χ, F, x', hb, hUj, hxx, e1]
      · have hUj : ¬ Untouched D (blockOf j) := hb ▸ hU
        by_cases hxx : x i = x j
        · simp [χ, F, x', hb, hUj, hxx]
          norm_num
        · simp [χ, F, x', hb, hUj, hxx]
    · have hb' : ¬ blockOf j = blockOf i := fun e => hb e.symm
      simp [χ, F, hb, hb']
  have hsum : ∑ i, ∑ j ∈ univ.erase i,
      (if χ i j then (triangles m).Jsym i j (x i) (x' j) + (triangles m).Jsym i j (x' i) (x j)
        else (triangles m).Jsym i j (x i) (x j) + (triangles m).Jsym i j (x' i) (x' j)) =
        ∑ i, ∑ j ∈ univ.erase i, F i j :=
    Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl (hpat i)
  have hFz : ∀ i j, blockOf j ≠ blockOf i → F i j = 0 := by
    intro i j hb
    simp [F, hb]
  rw [hh, hsum, sum_pairs_blocks F hFz] at key
  -- every touched block contributes at most `4`, every untouched block `0`
  have hblock : ∀ q : Fin m,
      F (blockSite q 0) (blockSite q 1) + F (blockSite q 0) (blockSite q 2) +
        F (blockSite q 1) (blockSite q 0) + F (blockSite q 1) (blockSite q 2) +
        F (blockSite q 2) (blockSite q 0) + F (blockSite q 2) (blockSite q 1) ≤
        4 - 4 * (if Untouched D q then (1 : ℚ) else 0) := by
    intro q
    by_cases hU : Untouched D q
    · simp [F, hU]
    · have h6 := triangle_pairs_le _ _ _ (not_mono_blockSite (hmono q))
      simp only [F, blockOf_blockSite, hU, not_false_eq_true, true_and, if_false]
      linarith
  have hcount : ∑ q : Fin m, (4 - 4 * (if Untouched D q then (1 : ℚ) else 0)) =
      4 * (m : ℚ) - 4 * (untouchedCount D : ℚ) := by
    rw [Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_boole, Finset.sum_const,
      Finset.card_univ, Fintype.card_fin]
    simp [untouchedCount]
    ring
  have hle := Finset.sum_le_sum (fun q (_ : q ∈ (univ : Finset (Fin m))) => hblock q)
  rw [hcount] at hle
  linarith

/-! #### The exponential lower bound -/

theorem natList_le_sum_map {α : Type*} (f : α → ℕ) {a : α} {l : List α} (ha : a ∈ l) :
    f a ≤ (l.map f).sum :=
  List.single_le_sum (fun _ _ => Nat.zero_le _) _ (List.mem_map_of_mem ha)

theorem natList_add_le_sum_map {α : Type*} (f : α → ℕ) {a b : α} (hab : a ≠ b) :
    ∀ {l : List α}, a ∈ l → b ∈ l → f a + f b ≤ (l.map f).sum := by
  intro l
  induction l with
  | nil => intro ha; simp at ha
  | cons c l ih =>
    intro ha hb
    rw [List.map_cons, List.sum_cons]
    rcases List.mem_cons.mp ha with rfl | ha'
    · rcases List.mem_cons.mp hb with rfl | hb'
      · exact absurd rfl hab
      · have := natList_le_sum_map f hb'
        omega
    · rcases List.mem_cons.mp hb with rfl | hb'
      · have := natList_le_sum_map f ha'
        omega
      · have := ih ha' hb'
        omega

/-- Inductive form of the lower bound: on a good box, a sum-free certificate accepted for a
bound `L ≥ m - d` visits at least `2 ^ (#untouched - d)` leaves. -/
theorem sumFree_visited_aux (m d : ℕ) (L : ℚ) (hL : (m : ℚ) - d ≤ L) (c : Cert (m * 3) 2)
    (D : Dom (m * 3) 2) (hc : c.SumFree) (hv : verify c (triangles m) D L = true)
    (hG : GoodDom D) : 2 ^ (untouchedCount D - d) ≤ c.visited D := by
  induction c generalizing D with
  | leaf u p msg =>
    simp only [verify, decide_eq_true_eq] at hv
    have h1 := leaf_untouchedCount_le hv hG
    have h2 : (untouchedCount D : ℚ) ≤ (d : ℚ) := by linarith
    have h3 : untouchedCount D ≤ d := by exact_mod_cast h2
    have h4 : untouchedCount D - d = 0 := by omega
    rw [h4]
    simp [Cert.visited]
  | branch i ch ih =>
    simp only [verify, List.all_eq_true] at hv
    simp only [Cert.visited]
    by_cases hU : Untouched D (blockOf i)
    · -- untouched block: both children are visited, each has one untouched block less
      have h0 : (0 : Fin 2) ∈ D i := hU i rfl 0
      have h1 : (1 : Fin 2) ∈ D i := hU i rfl 1
      have e0 := ih 0 (D.fix i 0) (hc 0) (hv 0 h0) (goodDom_fix_untouched hU hG 0)
      have e1 := ih 1 (D.fix i 1) (hc 1) (hv 1 h1) (goodDom_fix_untouched hU hG 1)
      have c0 := untouchedCount_fix_untouched (0 : Fin 2) hU
      have c1 := untouchedCount_fix_untouched (1 : Fin 2) hU
      have hsum := natList_add_le_sum_map (fun a => (ch a).visited (D.fix i a))
        (show (0 : Fin 2) ≠ 1 by decide) h0 h1
      have c1' : untouchedCount (D.fix i 1) = untouchedCount (D.fix i 0) := by omega
      rw [c1'] at e1
      have hpow : 2 ^ (untouchedCount D - d) ≤ 2 ^ (untouchedCount (D.fix i 0) - d + 1) :=
        Nat.pow_le_pow_right (by norm_num) (by omega)
      rw [pow_succ] at hpow
      omega
    · -- touched block: follow the witness
      obtain ⟨x, hx, hmono⟩ := hG
      have e := ih (x i) (D.fix i (x i)) (hc (x i)) (hv (x i) (hx i))
        ⟨x, inBox_fix hx i, hmono⟩
      have hcnt : untouchedCount (D.fix i (x i)) = untouchedCount D :=
        untouchedCount_update_touched [x i] (fun a ha => by
          rw [List.mem_singleton.mp ha]
          exact hx i) hU
      rw [hcnt] at e
      exact e.trans (natList_le_sum_map (fun a => (ch a).visited (D.fix i a)) (hx i))
  | prune i r t ℓ rest ih =>
    simp only [verify, Bool.and_eq_true, decide_eq_true_eq] at hv
    obtain ⟨hp, hrest⟩ := hv
    have hT : ¬ Untouched D (blockOf i) := prune_touched hp hG
    have e := ih (D.remove i r) hc hrest (goodDom_remove hp hG)
    have hcnt : untouchedCount (D.remove i r) = untouchedCount D :=
      untouchedCount_update_touched _ (fun a ha => (List.mem_filter.mp ha).1) hT
    rw [hcnt] at e
    exact e
  | sum I₁ I₂ L₁ L₂ c₁ c₂ _ _ =>
    exact absurd hc (by simp [Cert.SumFree])

/-- **Exponential lower bound with an additive gap.**  A sum-free certificate that the kernel
accepts for any bound `L ≥ m - d` on `m` disjoint frustrated triangles visits at least
`2 ^ (m - d)` leaves: giving up `d` units of the bound saves at most a factor `2 ^ d`. -/
theorem sumFree_gap_exponential (m d : ℕ) (L : ℚ) (hL : (m : ℚ) - d ≤ L) (c : Cert (m * 3) 2)
    (hc : c.SumFree) (hv : verify c (triangles m) (fullDom (m * 3) 2) L = true) :
    2 ^ (m - d) ≤ c.visited (fullDom (m * 3) 2) := by
  have h := sumFree_visited_aux m d L hL c (fullDom (m * 3) 2) hc hv (goodDom_fullDom m)
  rwa [untouchedCount_fullDom] at h

/-- **Exponential lower bound for sum-free certificates.**  Every certificate built from `leaf`,
`branch` and `prune` only that the kernel accepts for the optimal bound `m` of `m` disjoint
frustrated triangles visits at least `2 ^ m` leaves. -/
theorem sumFree_exponential (m : ℕ) (c : Cert (m * 3) 2) (hc : c.SumFree)
    (hv : verify c (triangles m) (fullDom (m * 3) 2) (m : ℚ) = true) :
    2 ^ m ≤ c.visited (fullDom (m * 3) 2) := by
  have h := sumFree_gap_exponential m 0 (m : ℚ) (by simp) c hc hv
  simpa using h

/-- **Exponential lower bound on the syntactic size** (`Cert.size`) of sum-free certificates for
the optimum of `m` disjoint frustrated triangles. -/
theorem sumFree_size_exponential (m : ℕ) (c : Cert (m * 3) 2) (hc : c.SumFree)
    (hv : verify c (triangles m) (fullDom (m * 3) 2) (m : ℚ) = true) : 2 ^ m ≤ c.size :=
  (sumFree_exponential m c hc hv).trans
    (c.visited_le_size _ fun _ => List.nodup_finRange 2)

end LowerBound

/-! ### Upper bounds: `2 ^ K` leaves without `sum`, `2 * m` leaves with `sum` -/

section UpperBound

variable {m : ℕ}

/-- Exact dynamic-programming messages of one frustrated triangle whose first site is fixed to
the state `v` (the message table of `triangleCert`). -/
def triMsg (v : Fin 2) (r r' : Fin 3) (s : Fin 2) : ℚ :=
  if r = 1 ∧ r' = 0 then (if s = v then 1 else 0)
  else if r = 2 ∧ r' = 0 then (if s = v then 1 else 0)
  else if r = 1 ∧ r' = 2 then (if s = v then 0 else 1)
  else if r = 2 ∧ r' = 1 then (if s = v then -1 else 0)
  else 0

/-- Unary check of the triangle messages: the second site carries the bound `1`. -/
theorem triMsg_unary : ∀ (v : Fin 2) (r : Fin 3) (a : Fin 2),
    (if r = 1 then (1 : ℚ) else 0) ≤ ∑ r' : Fin 3, triMsg v r r' a - triMsg v r r a := by
  decide +kernel

/-- Pair check of the triangle messages, the first site being restricted to the state `v`. -/
theorem triMsg_pair : ∀ (v : Fin 2) (r r' : Fin 3) (a b : Fin 2), r ≠ r' → (r = 0 → a = v) →
    (r' = 0 → b = v) →
    (0 : ℚ) ≤ (if a = b then 1 else 0) - triMsg v r r' a - triMsg v r' r b := by
  decide +kernel

/-! #### Tightness of the lower bound: `2 ^ K` leaves for the bound `K` without `sum` -/

/-- Dual leaf for the blocks `0, …, K - 1` at once, the first site of block `q` being fixed to
`v q`; the other blocks are ignored. -/
def prodLeaf (K : ℕ) (v : Fin m → Fin 2) : Cert (m * 3) 2 :=
  .leaf (fun i => if (blockOf i).val < K ∧ posOf i = 1 then 1 else 0) (fun _ _ => 0)
    (fun i j s =>
      if (blockOf i).val < K ∧ blockOf i = blockOf j then
        triMsg (v (blockOf i)) (posOf i) (posOf j) s
      else 0)

/-- Branch on the first site of each of the blocks `k - 1, …, 0` (recording the chosen states in
`v`), then close with the dual leaf `prodLeaf K v`. -/
def prodCert (m K : ℕ) : ℕ → (Fin m → Fin 2) → Cert (m * 3) 2
  | 0, v => prodLeaf K v
  | k + 1, v =>
    if h : k < m then
      .branch (blockSite ⟨k, h⟩ 0) fun a => prodCert m K k (Function.update v ⟨k, h⟩ a)
    else prodLeaf K v

theorem prodLeaf_ok (K : ℕ) (hK : K ≤ m) (v : Fin m → Fin 2) (D : Dom (m * 3) 2)
    (hD : ∀ q : Fin m, q.val < K → ∀ c ∈ D (blockSite q 0), c = v q) :
    LeafOK (triangles m) D (K : ℚ)
      (fun i => if (blockOf i).val < K ∧ posOf i = 1 then 1 else 0) (fun _ _ => 0)
      (fun i j s =>
        if (blockOf i).val < K ∧ blockOf i = blockOf j then
          triMsg (v (blockOf i)) (posOf i) (posOf j) s
        else 0) := by
  refine ⟨?_, ?_, ?_⟩
  · -- reparameterised unaries
    intro i a _
    rw [sum_erase_block i _ (by
      intro j hb
      have hn : ¬ blockOf i = blockOf j := fun e => hb e.symm
      simp [hn])]
    have h0 : (triangles m).h i a = 0 := rfl
    by_cases hiK : (blockOf i).val < K
    · have h1 := triMsg_unary (v (blockOf i)) (posOf i) a
      simp only [hiK, true_and, blockOf_blockSite, posOf_blockSite, if_true, h0]
      linarith
    · simp [hiK, h0]
  · -- reparameterised pair tables
    intro i j hj a ha b hb
    have hji : j ≠ i := Finset.ne_of_mem_erase hj
    have hs := triangles_Jsym m hji.symm a b
    unfold PairInstance.Jsym at hs
    rw [hs]
    by_cases hq : blockOf i = blockOf j
    · by_cases hiK : (blockOf i).val < K
      · have hjK : (blockOf j).val < K := hq ▸ hiK
        have hpos : posOf i ≠ posOf j := by
          intro e
          apply hji
          rw [eq_blockSite_of_blockOf hq.symm, ← e, blockSite_blockOf_posOf]
        have hfix : ∀ (l : Fin (m * 3)) (c : Fin 2), (blockOf l).val < K → c ∈ D l →
            posOf l = 0 → c = v (blockOf l) := by
          intro l c hl hc e
          rw [eq_blockSite_of_blockOf (rfl : blockOf l = blockOf l), e] at hc
          exact hD _ hl c hc
        have h3 := triMsg_pair (v (blockOf i)) (posOf i) (posOf j) a b hpos (hfix i a hiK ha)
          (by rw [hq]; exact hfix j b hjK hb)
        simp only [hq, hjK, true_and, and_self, if_true] at h3 ⊢
        linarith
      · have hjK : ¬ (blockOf j).val < K := hq ▸ hiK
        simp only [hiK, hjK, false_and, if_false]
        split_ifs <;> norm_num
    · have hq' : ¬ blockOf j = blockOf i := fun e => hq e.symm
      simp [hq, hq']
  · -- total
    have h1 : ∑ i : Fin (m * 3), (if (blockOf i).val < K ∧ posOf i = 1 then (1 : ℚ) else 0) =
        (K : ℚ) := by
      rw [← (finProdFinEquiv (m := m) (n := 3)).sum_comp, Fintype.sum_prod_type]
      have e : ∀ (q : Fin m) (r : Fin 3), finProdFinEquiv (q, r) = blockSite q r :=
        fun _ _ => rfl
      have h2 : ∀ q : Fin m, ∑ r : Fin 3, (if q.val < K ∧ r = 1 then (1 : ℚ) else 0) =
          if q.val < K then 1 else 0 := by
        intro q
        by_cases hq : q.val < K <;> simp [hq]
      simp only [e, blockOf_blockSite, posOf_blockSite, h2]
      rw [Finset.sum_boole, Fin.card_filter_val_lt, min_eq_right hK]
    rw [h1]
    simp

theorem prodCert_verified_aux (m K k : ℕ) (hK : K ≤ m) (hk : k ≤ K) (v : Fin m → Fin 2)
    (D : Dom (m * 3) 2)
    (hD : ∀ q : Fin m, k ≤ q.val → q.val < K → ∀ c ∈ D (blockSite q 0), c = v q) :
    verify (prodCert m K k v) (triangles m) D (K : ℚ) = true := by
  induction k generalizing v D with
  | zero =>
    simp only [prodCert, prodLeaf, verify, decide_eq_true_eq]
    exact prodLeaf_ok K hK v D fun q => hD q (Nat.zero_le _)
  | succ k ih =>
    have hkm : k < m := by omega
    simp only [prodCert, hkm, dif_pos, verify, List.all_eq_true]
    intro a _
    apply ih (by omega)
    intro q hq hqK c hc
    by_cases hqk : q = ⟨k, hkm⟩
    · subst hqk
      unfold Dom.fix at hc
      rw [Function.update_self, List.mem_singleton] at hc
      rw [Function.update_self]
      exact hc
    · have hne : blockSite q 0 ≠ blockSite ⟨k, hkm⟩ 0 := by
        intro e
        apply hqk
        have e2 := congrArg blockOf e
        rwa [blockOf_blockSite, blockOf_blockSite] at e2
      unfold Dom.fix at hc
      rw [Function.update_of_ne hne] at hc
      rw [Function.update_of_ne hqk]
      refine hD q ?_ hqK c hc
      have hqv : q.val ≠ k := fun e => hqk (Fin.ext e)
      omega

theorem prodCert_sumFree (m K k : ℕ) (v : Fin m → Fin 2) : (prodCert m K k v).SumFree := by
  induction k generalizing v with
  | zero =>
    simp [prodCert, prodLeaf, Cert.SumFree]
  | succ k ih =>
    by_cases hkm : k < m
    · simp only [prodCert, hkm, dif_pos, Cert.SumFree]
      exact fun a => ih _
    · simp [prodCert, hkm, prodLeaf, Cert.SumFree]

theorem prodCert_visited (m K k : ℕ) (v : Fin m → Fin 2) (D : Dom (m * 3) 2) (hk : k ≤ m)
    (hD : ∀ q : Fin m, q.val < k → D (blockSite q 0) = List.finRange 2) :
    (prodCert m K k v).visited D = 2 ^ k := by
  induction k generalizing v D with
  | zero =>
    simp [prodCert, prodLeaf, Cert.visited]
  | succ k ih =>
    have hkm : k < m := hk
    simp only [prodCert, hkm, dif_pos, Cert.visited]
    rw [hD ⟨k, hkm⟩ (Nat.lt_succ_self k)]
    have hstep : ∀ a : Fin 2,
        (prodCert m K k (Function.update v ⟨k, hkm⟩ a)).visited
          (D.fix (blockSite ⟨k, hkm⟩ 0) a) = 2 ^ k := by
      intro a
      apply ih _ _ (by omega)
      intro q hq
      have hne : blockSite q 0 ≠ blockSite ⟨k, hkm⟩ 0 := by
        intro e
        have e2 := congrArg blockOf e
        rw [blockOf_blockSite, blockOf_blockSite] at e2
        rw [e2] at hq
        exact lt_irrefl _ hq
      unfold Dom.fix
      rw [Function.update_of_ne hne]
      exact hD q (by omega)
    simp only [hstep]
    simp [pow_succ]
    ring

/-- **Exact sum-free complexity.**  For every `K ≤ m`, the least number of leaves visited by a
sum-free certificate accepted for the bound `K` on `m` disjoint frustrated triangles is exactly
`2 ^ K`: branching on one site in each of `K` triangles suffices, and nothing smaller does. -/
theorem sumFree_complexity (m K : ℕ) (hK : K ≤ m) :
    (∃ c : Cert (m * 3) 2, c.SumFree ∧
      verify c (triangles m) (fullDom (m * 3) 2) (K : ℚ) = true ∧
      c.visited (fullDom (m * 3) 2) = 2 ^ K) ∧
    ∀ c : Cert (m * 3) 2, c.SumFree →
      verify c (triangles m) (fullDom (m * 3) 2) (K : ℚ) = true →
      2 ^ K ≤ c.visited (fullDom (m * 3) 2) := by
  refine ⟨⟨prodCert m K K fun _ => 0, prodCert_sumFree m K K _,
    prodCert_verified_aux m K K hK le_rfl _ _ fun q h1 h2 => absurd h2 (by omega),
    prodCert_visited m K K _ _ hK fun _ _ => rfl⟩, fun c hc hv => ?_⟩
  have hL : (m : ℚ) - ((m - K : ℕ) : ℚ) ≤ (K : ℚ) := by
    rw [Nat.cast_sub hK]
    linarith
  have h := sumFree_gap_exponential m (m - K) (K : ℚ) hL c hc hv
  have e : m - (m - K) = K := by omega
  rwa [e] at h

/-- **The lower bound is tight.**  There is a sum-free certificate accepted for the optimal bound
`m` that visits exactly `2 ^ m` leaves. -/
theorem sumFree_tight (m : ℕ) :
    ∃ c : Cert (m * 3) 2, c.SumFree ∧
      verify c (triangles m) (fullDom (m * 3) 2) (m : ℚ) = true ∧
      c.visited (fullDom (m * 3) 2) = 2 ^ m :=
  (sumFree_complexity m m le_rfl).1

/-! #### With the `sum` rule the certificate is linear -/

/-- The sub-family consisting of the triangles whose block index satisfies `P`. -/
def trianglesOn (m : ℕ) (P : ℕ → Prop) [DecidablePred P] : PairInstance (m * 3) 2 where
  h := fun _ _ => 0
  J := fun i j a b =>
    if P (blockOf i).val ∧ blockOf i = blockOf j ∧ i < j ∧ a = b then 1 else 0

theorem trianglesOn_J_nonneg (m : ℕ) (P : ℕ → Prop) [DecidablePred P] (i j : Fin (m * 3))
    (a b : Fin 2) : 0 ≤ (trianglesOn m P).J i j a b := by
  simp only [trianglesOn]
  split_ifs <;> norm_num

/-- Dual leaf for block `q` once its first site is fixed to `v`. -/
def blockLeaf (q : Fin m) (v : Fin 2) : Cert (m * 3) 2 :=
  .leaf (fun i => if blockOf i = q ∧ posOf i = 1 then 1 else 0) (fun _ _ => 0)
    (fun i j s => if blockOf i = q ∧ blockOf j = q then triMsg v (posOf i) (posOf j) s else 0)

/-- Two-leaf certificate for the single triangle `q`: branch on its first site. -/
def blockCert (q : Fin m) : Cert (m * 3) 2 := .branch (blockSite q 0) fun v => blockLeaf q v

theorem blockLeaf_ok (q : Fin m) (v : Fin 2) (I : PairInstance (m * 3) 2)
    (hh : ∀ i a, 0 ≤ I.h i a) (hJ0 : ∀ i j a b, 0 ≤ I.J i j a b)
    (hJ : ∀ i j a, blockOf i = q → blockOf j = q → i < j → 1 ≤ I.J i j a a) :
    LeafOK I ((fullDom (m * 3) 2).fix (blockSite q 0) v) 1
      (fun i => if blockOf i = q ∧ posOf i = 1 then 1 else 0) (fun _ _ => 0)
      (fun i j s =>
        if blockOf i = q ∧ blockOf j = q then triMsg v (posOf i) (posOf j) s else 0) := by
  refine ⟨?_, ?_, ?_⟩
  · -- reparameterised unaries
    intro i a _
    rw [sum_erase_block i _ (by
      intro j hb
      have hn : ¬ (blockOf i = q ∧ blockOf j = q) := fun ⟨h1, h2⟩ => hb (h2.trans h1.symm)
      simp [hn])]
    have h0 := hh i a
    by_cases hi : blockOf i = q
    · have h1 := triMsg_unary v (posOf i) a
      simp only [hi, blockOf_blockSite, posOf_blockSite, true_and, and_self, if_true]
      linarith
    · simp only [hi, false_and, if_false, Finset.sum_const_zero]
      linarith
  · -- reparameterised pair tables
    intro i j hj a ha b hb
    have hji : j ≠ i := Finset.ne_of_mem_erase hj
    have h1 := hJ0 i j a b
    have h2 := hJ0 j i b a
    by_cases hq : blockOf i = q ∧ blockOf j = q
    · obtain ⟨hi, hj'⟩ := hq
      have hpos : posOf i ≠ posOf j := by
        intro e
        apply hji
        rw [eq_blockSite_of_blockOf hi, eq_blockSite_of_blockOf hj', e]
      have hfix : ∀ (l : Fin (m * 3)) (c : Fin 2), blockOf l = q →
          c ∈ ((fullDom (m * 3) 2).fix (blockSite q 0) v) l → posOf l = 0 → c = v := by
        intro l c hl hc e
        have hl' : l = blockSite q 0 := by rw [eq_blockSite_of_blockOf hl, e]
        rw [hl'] at hc
        unfold Dom.fix at hc
        rw [Function.update_self, List.mem_singleton] at hc
        exact hc
      have hJs : (if a = b then (1 : ℚ) else 0) ≤ I.J i j a b + I.J j i b a := by
        by_cases hab : a = b
        · subst hab
          rcases lt_or_gt_of_ne hji with h | h
          · have h3 := hJ j i a hj' hi h
            simp only [if_true]
            linarith
          · have h3 := hJ i j a hi hj' h
            simp only [if_true]
            linarith
        · simp only [hab, if_false]
          linarith
      have h3 := triMsg_pair v (posOf i) (posOf j) a b hpos (hfix i a hi ha) (hfix j b hj' hb)
      simp only [hi, hj', and_self, if_true]
      linarith
    · have hq' : ¬ (blockOf j = q ∧ blockOf i = q) := fun ⟨e1, e2⟩ => hq ⟨e2, e1⟩
      simp only [hq, hq', if_false]
      linarith
  · -- total
    have h1 : ∑ i : Fin (m * 3), (if blockOf i = q ∧ posOf i = 1 then (1 : ℚ) else 0) = 1 := by
      rw [Finset.sum_eq_single (blockSite q 1)]
      · simp
      · intro i _ hi
        have hn : ¬ (blockOf i = q ∧ posOf i = 1) := by
          rintro ⟨e1, e2⟩
          apply hi
          rw [eq_blockSite_of_blockOf e1, e2]
        simp [hn]
      · intro h
        exact absurd (Finset.mem_univ _) h
    rw [h1]
    simp

/-- The two-leaf block certificate is accepted for the bound `1` by every instance with
non-negative tables that contains triangle `q`. -/
theorem blockCert_verified (q : Fin m) (I : PairInstance (m * 3) 2)
    (hh : ∀ i a, 0 ≤ I.h i a) (hJ0 : ∀ i j a b, 0 ≤ I.J i j a b)
    (hJ : ∀ i j a, blockOf i = q → blockOf j = q → i < j → 1 ≤ I.J i j a a) :
    verify (blockCert q) I (fullDom (m * 3) 2) 1 = true := by
  simp only [blockCert, blockLeaf, verify, List.all_eq_true, decide_eq_true_eq]
  intro v _
  exact blockLeaf_ok q v I hh hJ0 hJ

theorem blockCert_visited (q : Fin m) : (blockCert q).visited (fullDom (m * 3) 2) = 2 := by
  simp [blockCert, blockLeaf, Cert.visited, fullDom]

theorem blockCert_size (q : Fin m) : (blockCert q).size = 3 := by
  simp [blockCert, blockLeaf, Cert.size]

/-- The trivial leaf: certifies the bound `0` for non-negative tables. -/
def Cert.zeroLeaf (n k : ℕ) : Cert n k := .leaf (fun _ => 0) (fun _ _ => 0) (fun _ _ _ => 0)

/-- **Peeling certificate.**  `peelCert m k` certifies the bound `k` for the first `k` triangles:
split off triangle `k - 1` with the `sum` rule (certified by the two-leaf `blockCert`) and recurse
on the remaining triangles; the last remaining triangle needs no `sum`. -/
def peelCert (m : ℕ) : ℕ → Cert (m * 3) 2
  | 0 => Cert.zeroLeaf _ _
  | k + 1 =>
    if h : k < m then
      if k = 0 then blockCert ⟨k, h⟩
      else .sum (trianglesOn m (· = k)) (trianglesOn m (· < k)) 1 k (blockCert ⟨k, h⟩)
        (peelCert m k)
    else Cert.zeroLeaf _ _

theorem peelCert_verified_aux (m k : ℕ) (hk : k ≤ m) (I : PairInstance (m * 3) 2)
    (hh : ∀ i a, 0 ≤ I.h i a)
    (hJ : ∀ i j a b, (trianglesOn m (· < k)).J i j a b ≤ I.J i j a b) :
    verify (peelCert m k) I (fullDom (m * 3) 2) (k : ℚ) = true := by
  induction k generalizing I with
  | zero =>
    have hJ0 : ∀ i j a b, 0 ≤ I.J i j a b := fun i j a b =>
      le_trans (trianglesOn_J_nonneg m _ i j a b) (hJ i j a b)
    simp only [peelCert, Cert.zeroLeaf, verify, decide_eq_true_eq]
    refine ⟨fun i a _ => ?_, fun i j _ a _ b _ => ?_, ?_⟩
    · simpa using hh i a
    · have h1 := hJ0 i j a b
      have h2 := hJ0 j i b a
      simp only [mul_zero, sub_zero]
      linarith
    · simp
  | succ k ih =>
    have hkm : k < m := hk
    have hJ0 : ∀ i j a b, 0 ≤ I.J i j a b := fun i j a b =>
      le_trans (trianglesOn_J_nonneg m _ i j a b) (hJ i j a b)
    simp only [peelCert, hkm, dif_pos]
    by_cases hk0 : k = 0
    · subst hk0
      simp only [if_true]
      have h1 := blockCert_verified ⟨0, hkm⟩ I hh hJ0 (by
        intro i j a hi hj hij
        have h2 := hJ i j a a
        have hi' : (blockOf i).val = 0 := by rw [hi]
        have hb : blockOf i = blockOf j := hi.trans hj.symm
        simpa [trianglesOn, hi', ← hb, hij] using h2)
      simpa using h1
    · simp only [hk0, if_false, verify, Bool.and_eq_true, decide_eq_true_eq]
      refine ⟨⟨⟨?_, ?_, ?_⟩, ?_⟩, ?_⟩
      · intro i a _
        simpa [trianglesOn] using hh i a
      · intro i j _ a _ b _
        refine le_trans ?_ (hJ i j a b)
        simp only [trianglesOn]
        by_cases h1 : (blockOf i).val = k
        · simp [h1]
        · by_cases h2 : (blockOf i).val < k
          · have h3 : (blockOf i).val < k + 1 := by omega
            simp [h1, h2, h3]
          · have h3 : ¬ (blockOf i).val < k + 1 := by omega
            simp [h1, h2, h3]
      · push_cast
        linarith
      · exact blockCert_verified ⟨k, hkm⟩ _ (fun _ _ => le_refl _)
          (trianglesOn_J_nonneg m _) (by
            intro i j a hi hj hij
            have hi' : (blockOf i).val = k := by rw [hi]
            have hb : blockOf i = blockOf j := hi.trans hj.symm
            simp [trianglesOn, hi', ← hb, hij])
      · exact ih (by omega) _ (fun _ _ => le_refl _) (fun _ _ _ _ => le_refl _)

/-- The peeling certificate is accepted for the optimal bound `m`. -/
theorem peelCert_verified (m : ℕ) :
    verify (peelCert m m) (triangles m) (fullDom (m * 3) 2) (m : ℚ) = true :=
  peelCert_verified_aux m m le_rfl (triangles m) (fun _ _ => le_refl _) (by
    intro i j a b
    simp only [trianglesOn, triangles]
    split_ifs <;> simp_all)

/-- The peeling certificate visits exactly `2 * k` leaves. -/
theorem peelCert_visited (m k : ℕ) (h1 : 1 ≤ k) (hk : k ≤ m) :
    (peelCert m k).visited (fullDom (m * 3) 2) = 2 * k := by
  induction k with
  | zero => omega
  | succ k ih =>
    have hkm : k < m := hk
    simp only [peelCert, hkm, dif_pos]
    by_cases hk0 : k = 0
    · subst hk0
      simp [blockCert_visited]
    · simp only [hk0, if_false, Cert.visited, blockCert_visited]
      rw [ih (by omega) (by omega)]
      ring

/-- For every `m` (including `m = 0`, where a single trivial leaf is needed) the peeling
certificate visits at most `2 * m + 1` leaves. -/
theorem peelCert_visited_le (m : ℕ) :
    (peelCert m m).visited (fullDom (m * 3) 2) ≤ 2 * m + 1 := by
  rcases Nat.eq_zero_or_pos m with rfl | hm
  · simp [peelCert, Cert.zeroLeaf, Cert.visited]
  · rw [peelCert_visited m m hm le_rfl]
    omega

/-- The syntactic size of the peeling certificate is `4 * k - 1`. -/
theorem peelCert_size (m k : ℕ) (h1 : 1 ≤ k) (hk : k ≤ m) :
    (peelCert m k).size + 1 = 4 * k := by
  induction k with
  | zero => omega
  | succ k ih =>
    have hkm : k < m := hk
    simp only [peelCert, hkm, dif_pos]
    by_cases hk0 : k = 0
    · subst hk0
      simp [blockCert_size]
    · simp only [hk0, if_false, Cert.size, blockCert_size]
      have h2 := ih (by omega) (by omega)
      omega

/-- **Linear upper bound with the `sum` rule.**  For every `m ≥ 1` there is a certificate (using
`sum`) that the kernel accepts for the optimal bound `m` of the triangle family and that visits
only `2 * m` leaves. -/
theorem sum_linear (m : ℕ) (hm : 0 < m) :
    ∃ c : Cert (m * 3) 2, verify c (triangles m) (fullDom (m * 3) 2) (m : ℚ) = true ∧
      c.visited (fullDom (m * 3) 2) = 2 * m :=
  ⟨peelCert m m, peelCert_verified m, peelCert_visited m m hm le_rfl⟩

theorem two_mul_lt_two_pow_of_three_le (m : ℕ) (hm : 3 ≤ m) : 2 * m < 2 ^ m := by
  induction m, hm using Nat.le_induction with
  | base => norm_num
  | succ k hk ih =>
    rw [pow_succ]
    omega

/-- **Exponential separation.**  For `m ≥ 3` there is an accepted certificate with `sum` that
visits `2 * m` leaves, strictly fewer than *every* accepted sum-free certificate for the same
bound (which visits at least `2 ^ m` leaves). -/
theorem sum_rule_separation (m : ℕ) (hm : 3 ≤ m) :
    ∃ c : Cert (m * 3) 2, verify c (triangles m) (fullDom (m * 3) 2) (m : ℚ) = true ∧
      c.visited (fullDom (m * 3) 2) = 2 * m ∧
      ∀ c' : Cert (m * 3) 2, c'.SumFree →
        verify c' (triangles m) (fullDom (m * 3) 2) (m : ℚ) = true →
        c.visited (fullDom (m * 3) 2) < c'.visited (fullDom (m * 3) 2) := by
  have hvis := peelCert_visited m m (by omega) le_rfl
  refine ⟨peelCert m m, peelCert_verified m, hvis, fun c' hc' hv' => ?_⟩
  have h1 := sumFree_exponential m c' hc' hv'
  have h2 := two_mul_lt_two_pow_of_three_le m hm
  omega

/-! #### The case `m = 1`: the triangle example of `CertificateAlgebra.lean` -/

theorem triangleCert_sumFree : triangleCert.SumFree := by
  simp [triangleCert, Cert.SumFree]

theorem triangleCert_visited : triangleCert.visited (fullDom 3 2) = 2 := by
  simp [triangleCert, Cert.visited, fullDom]

/-- The two-leaf certificate `triangleCert` is optimal among sum-free certificates: every
accepted sum-free certificate for the bound `1` of the frustrated triangle visits two leaves. -/
theorem triangle_sumFree_two_leaves (c : Cert 3 2) (hc : c.SumFree)
    (hv : verify c triangle (fullDom 3 2) 1 = true) : 2 ≤ c.visited (fullDom 3 2) := by
  have h := sumFree_exponential 1 c hc (by rw [triangles_one]; simpa using hv)
  simpa using h

end UpperBound

end MetricChain
