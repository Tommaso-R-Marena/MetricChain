/-
Kernel-checked recomputation of the finite facts behind docs/complexity/NANUQ_LOCAL_CRITERION.md
(Proposition 2 on six points, Lemma 4, Lemma 8, Theorem 10: the numbers 16, 150, 141, 127, 108).

Conventions (as in experiments/complexity/nanuq/splitsys.py).  Points `0..n-1` are in circular order.  A
non-trivial circular split is the bitmask of its side not containing point `0` (an interval `{i..j}`,
`1 ≤ i`).  A system is the list of its non-trivial splits; all trivial splits are understood to belong to
every system.  For four points `a b c d` listed in circular order the two planar quartets are `ab|cd` and
`bc|da`; `w2 sys a b c d` is twice the weight of `ab|cd`: `2` if only `ab|cd` is displayed, `1` if both
are, `0` otherwise.

  phi6x2 = 2·Φ6(u₁; z, w; u_p; v₁, v_q),   phi5x2 = 2·Φ5(u₁; z; u_p; v₁, v_q),   psix2 = 2·Ψ(a; u; b; z, w),
  d2     = 2·d_Σ (the NANUQ metric of the system),   alpha2 = 2·α_ij.

What is and is not proved here.  Everything below is a statement about explicit finite objects and is
proved by `decide +kernel` (evaluation in the kernel; no native code, no axioms beyond those of Mathlib's
`import`, see `#print axioms` at the end).  The trees and the tree-generated systems are *defined* (not
listed).  The list `C6` of the 108 systems of the substitution closure `𝒞₆` is *imported* from the Python
enumeration (`experiments/complexity/nanuq/export_lean_lists.py`); that this list is `𝒞₆` is not checked
here.  The general statements of the note (Proposition 2 for all `n`, Theorem 4, Proposition 6,
Theorem 7) are paper proofs and are not formalised.

Checked with:  lake env lean experiments/complexity/lean/NanuqFinite.lean
(about 3.5 minutes; peak resident memory about 11 GB, of which 6.6 GB is the memory-mapped Mathlib).
-/
import Mathlib

namespace Complexity.NanuqFinite

/-! ### Quartets displayed by a system, and the local terms -/

/-- the split with mask `m` separates `{a,b}` from `{c,d}` -/
def sep (m a b c d : Nat) : Bool :=
  (m.testBit a && m.testBit b && !m.testBit c && !m.testBit d) ||
  (!m.testBit a && !m.testBit b && m.testBit c && m.testBit d)

/-- the system displays the quartet `ab|cd` -/
def disp (sys : List Nat) (a b c d : Nat) : Bool := sys.any (fun m => sep m a b c d)

/-- twice the weight of `ab|cd`, for `a b c d` in circular order (the other planar quartet is `bc|da`) -/
def w2 (sys : List Nat) (a b c d : Nat) : Int :=
  if disp sys a b c d then (if disp sys b c d a then 1 else 2) else 0

/-- `2·Φ6` for the circular order `u₁, z, w, u_p, v₁, v_q` -/
def phi6x2 (sys : List Nat) (u1 z w up v1 vq : Nat) : Int :=
  w2 sys z w v1 vq + w2 sys z w up u1 - w2 sys z w up vq - w2 sys z w v1 u1

/-- `2·Φ5` for the circular order `u₁, z, u_p, v₁, v_q` -/
def phi5x2 (sys : List Nat) (u1 z up v1 vq : Nat) : Int :=
  w2 sys u1 z v1 vq + w2 sys z up v1 vq - w2 sys z up v1 u1 - w2 sys u1 z up vq

/-- `2·Ψ` for the circular order `a, u, b, z, w` -/
def psix2 (sys : List Nat) (a u b z w : Nat) : Int :=
  2 - w2 sys a u z w - w2 sys u b z w + w2 sys a b z w

/-- the dihedral placement `t ↦ r + t` or `t ↦ r - t` (mod `n`) -/
def place (n r : Nat) (fwd : Bool) (t : Nat) : Nat := if fwd then (r + t) % n else (r + n - t) % n

/-- the six-point condition in one placement: `Φ6 ≥ 0`, and `Φ6 = 0` if `u₁u_p|v₁v_q` is not displayed -/
def ok6at (sys : List Nat) (y : Nat → Nat) : Bool :=
  let f := phi6x2 sys (y 0) (y 1) (y 2) (y 3) (y 4) (y 5)
  decide (0 ≤ f) && (disp sys (y 0) (y 3) (y 4) (y 5) || decide (f = 0))

/-- the five-point facts in one placement: `Φ5, Ψ ∈ {0, ½, 1}`, and `Φ5 = 0` if `u₁u_p|v₁v_q` is not
displayed -/
def ok5at (sys : List Nat) (y : Nat → Nat) : Bool :=
  let f := phi5x2 sys (y 0) (y 1) (y 2) (y 3) (y 4)
  let g := psix2 sys (y 0) (y 1) (y 2) (y 3) (y 4)
  decide (0 ≤ f) && decide (f ≤ 2) && (disp sys (y 0) (y 2) (y 3) (y 4) || decide (f = 0))
    && decide (0 ≤ g) && decide (g ≤ 2)

/-- a system on six points is 6-locally good: the condition holds in all twelve dihedral placements -/
def good6 (sys : List Nat) : Bool :=
  (List.range 6).all (fun r => ok6at sys (place 6 r true) && ok6at sys (place 6 r false))

def good5 (sys : List Nat) : Bool :=
  (List.range 5).all (fun r => ok5at sys (place 5 r true) && ok5at sys (place 5 r false))

/-! ### Circular splits, binary trees and tree-generated systems on `n` points -/

/-- mask of the interval `{i,…,j}` -/
def interval (i j : Nat) : Nat := 2 ^ (j + 1) - 2 ^ i

/-- the non-trivial circular splits of `n` points: the intervals `{i..j}` with `1 ≤ i ≤ j ≤ n-1` and
`2 ≤ j - i + 1 ≤ n - 2` -/
def splits (n : Nat) : List Nat :=
  (List.range n).flatMap (fun i => (List.range n).filterMap (fun j =>
    if 1 ≤ i ∧ i + 1 ≤ j ∧ j + 3 ≤ n + i then some (interval i j) else none))

/-- two splits (sides not containing `0`) are compatible: disjoint or nested -/
def compat (a b : Nat) : Bool := (a &&& b == 0) || (a &&& b == a) || (a &&& b == b)

/-- the system with code `k`: the splits of `splits n` selected by the bits of `k` -/
def sysOf (n k : Nat) : List Nat := ((splits n).zipIdx.filter (fun p => k.testBit p.2)).map (·.1)

/-- all systems on `n` points -/
def allSystems (n : Nat) : List (List Nat) := (List.range (2 ^ (splits n).length)).map (sysOf n)

/-- the binary trees with the given circular order of leaves: `n - 3` pairwise compatible non-trivial
circular splits -/
def trees (n : Nat) : List (List Nat) :=
  (allSystems n).filter (fun s => s.length == n - 3 && s.all (fun a => s.all (fun b => compat a b)))

/-- `s` is a non-empty union of trees of the list `ts` (i.e. it contains a tree of `ts`, and each of its
splits lies in a tree of `ts` contained in `s`) -/
def treeGenWith (ts : List (List Nat)) (s : List Nat) : Bool :=
  ts.any (fun t => t.all (fun m => s.contains m)) &&
    s.all (fun m => ts.any (fun t => t.contains m && t.all (fun m' => s.contains m')))

def trees5 : List (List Nat) := [[6, 24], [6, 14], [14, 12], [12, 28], [28, 24]]

def trees6 : List (List Nat) :=
  [[6, 14, 30], [6, 14, 48], [6, 30, 24], [6, 24, 56], [6, 56, 48], [14, 30, 12], [14, 12, 48],
   [30, 12, 28], [30, 28, 24], [12, 28, 60], [12, 60, 48], [28, 60, 24], [60, 24, 56], [60, 56, 48]]

theorem splits5_eq : splits 5 = [6, 14, 12, 28, 24] := by decide +kernel
theorem splits6_eq : splits 6 = [6, 14, 30, 12, 28, 60, 24, 56, 48] := by decide +kernel

def sameSet (a b : List Nat) : Bool := a.all (fun m => b.contains m) && b.all (fun m => a.contains m)

/-- `trees5` and `trees6` are the lists of all trees (as sets of splits) -/
theorem trees5_spec : (trees 5).length = 5 ∧ trees5.length = 5 ∧
    (trees 5).all (fun t => trees5.any (sameSet t)) = true := by decide +kernel

theorem trees6_spec : (trees 6).length = 14 ∧ trees6.length = 14 ∧
    (trees 6).all (fun t => trees6.any (sameSet t)) = true ∧
    trees6.all (fun t => (trees 6).any (sameSet t)) = true := by decide +kernel

/-- the tree-generated systems on five and on six points -/
def tg5 : List (List Nat) := (allSystems 5).filter (treeGenWith trees5)
def tg6 : List (List Nat) := (allSystems 6).filter (treeGenWith trees6)

/-! ### The NANUQ metric of a system and its split weights -/

/-- `4·ρ_xy` on the 4-set `{x,y,z,w}`: `4 ×` the fraction of the displayed quartets in which `xy` is not a
cherry -/
def rho4 (sys : List Nat) (x y z w : Nat) : Nat :=
  let s := (disp sys x z y w).toNat + (disp sys x w y z).toNat
  4 * s / ((disp sys x y z w).toNat + s)

/-- `2·d_Σ(x,y)`, where `d_Σ(x,y) = Σ_{z,w} 2ρ_xy({x,y,z,w}) + 2n - 4` -/
def d2 (n : Nat) (sys : List Nat) (x y : Nat) : Nat :=
  if x = y then 0 else
    2 * (2 * n - 4) + ((List.range n).flatMap (fun z => (List.range n).filterMap (fun w =>
      if z < w ∧ z ≠ x ∧ z ≠ y ∧ w ≠ x ∧ w ≠ y then some (rho4 sys x y z w) else none))).sum

/-- `2·α_ij`, the weight of the split `{x_{i+1},…,x_j} | rest` (gaps `i`, `j`) -/
def alpha2 (n : Nat) (sys : List Nat) (i j : Nat) : Int :=
  (d2 n sys i j : Int) + d2 n sys ((i + 1) % n) ((j + 1) % n)
    - d2 n sys i ((j + 1) % n) - d2 n sys ((i + 1) % n) j

/-- the metric is Kalmanson for the given order with support exactly the system:
`α_ij ≥ 0` for all gaps `i < j`, and `α_ij > 0` iff the split is trivial or belongs to the system -/
def globallyGood (n : Nat) (sys : List Nat) : Bool :=
  (List.range n).all (fun i => (List.range n).all (fun j =>
    !(decide (i < j)) ||
      (decide (0 ≤ alpha2 n sys i j) &&
        (decide (0 < alpha2 n sys i j) ==
          ((j == i + 1) || (i == 0 && j == n - 1) || sys.contains (interval (i + 1) j))))))

/-- ordered pairs `(l[a], l[b])`, `a < b` -/
def pairsOf (l : List Nat) : List (Nat × Nat) :=
  (List.range l.length).flatMap (fun a => (List.range l.length).filterMap (fun b =>
    if a < b then some (l.getD a 0, l.getD b 0) else none))

/-- the right-hand side of Proposition 2 for the non-trivial split `U|V`, `U = (u₁..u_p)`,
`V = (v₁..v_q)`:  `Φ4 + Σ Φ5 + Σ Φ6` (times 2) -/
def localSum (sys : List Nat) (U V : List Nat) : Int :=
  let u1 := U.getD 0 0
  let up := U.getD (U.length - 1) 0
  let v1 := V.getD 0 0
  let vq := V.getD (V.length - 1) 0
  let Ui := U.tail.dropLast
  let Vi := V.tail.dropLast
  2 * w2 sys u1 up v1 vq
    + (Ui.map (fun z => phi5x2 sys u1 z up v1 vq)).sum
    + (Vi.map (fun z => phi5x2 sys v1 z vq u1 up)).sum
    + ((pairsOf Ui).map (fun p => phi6x2 sys u1 p.1 p.2 up v1 vq)).sum
    + ((pairsOf Vi).map (fun p => phi6x2 sys v1 p.1 p.2 vq u1 up)).sum

/-- Proposition 2 for one system on `n` points: `α_ij / 2 = Φ4 + ΣΦ5 + ΣΦ6` for the non-trivial splits
and `α / 2 = n - 2 + ΣΨ` for the trivial ones -/
def decompOK (n : Nat) (sys : List Nat) : Bool :=
  (List.range n).all (fun i => (List.range n).all (fun j =>
    !(decide (i + 2 ≤ j ∧ j + 2 ≤ n + i)) ||
      decide (alpha2 n sys i j =
        2 * localSum sys ((List.range (j - i)).map (fun t => i + 1 + t))
                         ((List.range (n - (j - i))).map (fun t => (j + 1 + t) % n))))) &&
  (List.range n).all (fun i =>
    decide (alpha2 n sys i ((i + 1) % n) = 4 * ((n : Int) - 2) +
      2 * ((pairsOf ((List.range (n - 3)).map (fun t => (i + 3 + t) % n))).map
            (fun p => psix2 sys i ((i + 1) % n) ((i + 2) % n) p.1 p.2)).sum))

/-! ### Doubling a leaf -/

/-- replace point `k` by the two adjacent points `k, k+1` in a mask -/
def dblMask (k m : Nat) : Nat :=
  m % 2 ^ k + (if m.testBit k then 3 * 2 ^ k else 0) + (m / 2 ^ (k + 1)) * 2 ^ (k + 2)

/-- the system on `n + 1` points obtained from a system on `n` points by replacing leaf `k` by a cherry -/
def dbl (n k : Nat) (sys : List Nat) : List Nat :=
  (if k = 0 then 2 ^ (n + 1) - 4 else 3 * 2 ^ k) :: sys.map (dblMask k)

/-! ### The statements -/

/-- there are 16 tree-generated systems on five points -/
theorem tg5_length : tg5.length = 16 := by decide +kernel

/-- **Lemma 4.**  Every tree-generated system on five points satisfies the five-point facts in all ten
placements. -/
theorem five_point_facts : tg5.all good5 = true := by decide +kernel

/-- **Proposition 2 on five points**: the local decomposition of the split weights holds for every
tree-generated system (a consistency check of the definitions above against the metric). -/
theorem decomposition_five : tg5.all (decompOK 5) = true := by decide +kernel

/-- there are 150 tree-generated systems on six points -/
theorem tg6_length : tg6.length = 150 := by decide +kernel

/-- 127 of them are 6-locally good -/
theorem tg6_locally_good : (tg6.filter good6).length = 127 := by decide +kernel

/-- **Theorem 10 (c), computational part.**  A tree-generated system on five points with one leaf doubled
is tree-generated and 6-locally good. -/
theorem doubled_five_point_systems :
    tg5.all (fun s => (List.range 5).all (fun k =>
      treeGenWith trees6 (dbl 5 k s) && good6 (dbl 5 k s))) = true := by decide +kernel

/-! #### The metric on six points

Evaluating the metric of all 150 systems in one kernel call needs more than 10 GB, so the systems are
split by their code into sixteen pieces, three facts per system are computed once and packed in a number,
and the statements about `tg6` are deduced from the sixteen pieces by (real) proofs. -/

/-- bit 0: 6-locally good; bit 1: Kalmanson with exact support; bit 2: Proposition 2 holds -/
def code3 (s : List Nat) : Nat :=
  (good6 s).toNat + 2 * (globallyGood 6 s).toNat + 4 * (decompOK 6 s).toNat

/-- the tree-generated systems on six points with codes in `[a, a + m)` -/
def codesTG (a m : Nat) : List (List Nat) :=
  ((List.range' a m).map (sysOf 6)).filter (treeGenWith trees6)

theorem tg6_split : tg6 = codesTG 0 32 ++ codesTG 32 32 ++ codesTG 64 32 ++ codesTG 96 32 ++ codesTG 128 32 ++ codesTG 160 32 ++ codesTG 192 32 ++ codesTG 224 32 ++ codesTG 256 32 ++ codesTG 288 32 ++ codesTG 320 32 ++ codesTG 352 32 ++ codesTG 384 32 ++ codesTG 416 32 ++ codesTG 448 32 ++ codesTG 480 32 := by
  decide +kernel

theorem facts_0 : (codesTG 0 32).map code3 = [7, 7, 7, 7, 7, 7] := by decide +kernel
theorem facts_1 : (codesTG 32 32).map code3 = [7, 7, 7, 7] := by decide +kernel
theorem facts_2 : (codesTG 64 32).map code3 = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7] := by decide +kernel
theorem facts_3 : (codesTG 96 32).map code3 = [7, 7, 7, 7, 7, 7, 7, 7, 7] := by decide +kernel
theorem facts_4 : (codesTG 128 32).map code3 = [] := by decide +kernel
theorem facts_5 : (codesTG 160 32).map code3 = [] := by decide +kernel
theorem facts_6 : (codesTG 192 32).map code3 = [7, 7, 7, 7, 7, 6, 7, 6] := by decide +kernel
theorem facts_7 : (codesTG 224 32).map code3 = [7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 6, 7, 7, 7, 7, 4, 6] := by decide +kernel
theorem facts_8 : (codesTG 256 32).map code3 = [7, 7, 7, 7, 7, 7, 7, 7] := by decide +kernel
theorem facts_9 : (codesTG 288 32).map code3 = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7] := by decide +kernel
theorem facts_10 : (codesTG 320 32).map code3 = [7, 7, 7, 7, 7] := by decide +kernel
theorem facts_11 : (codesTG 352 32).map code3 = [7, 7, 7, 4, 7, 7, 4, 7, 7, 7, 7] := by decide +kernel
theorem facts_12 : (codesTG 384 32).map code3 = [7, 7, 7, 7, 7, 7, 4] := by decide +kernel
theorem facts_13 : (codesTG 416 32).map code3 = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 7, 4, 6, 6] := by decide +kernel
theorem facts_14 : (codesTG 448 32).map code3 = [7, 7, 7, 7, 7, 7, 7, 6, 4, 6] := by decide +kernel
theorem facts_15 : (codesTG 480 32).map code3 = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 4, 7, 7, 6, 7, 7, 6, 6, 7, 7, 6, 7] := by decide +kernel

theorem tg6_codes : tg6.map code3 = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 6, 7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 6, 7, 7, 7, 7, 4, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 7, 4, 6, 6, 7, 7, 7, 7, 7, 7, 7, 6, 4, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 4, 7, 7, 6, 7, 7, 6, 6, 7, 7, 6, 7] := by
  rw [tg6_split]
  simp only [List.map_append, facts_0, facts_1, facts_2, facts_3, facts_4, facts_5, facts_6, facts_7, facts_8, facts_9, facts_10, facts_11, facts_12, facts_13, facts_14, facts_15]
  rfl

theorem code3_bits (a b c : Bool) :
    (a.toNat + 2 * b.toNat + 4 * c.toNat).testBit 0 = a ∧
    (a.toNat + 2 * b.toNat + 4 * c.toNat).testBit 1 = b ∧
    (a.toNat + 2 * b.toNat + 4 * c.toNat).testBit 2 = c := by
  cases a <;> cases b <;> cases c <;> decide

theorem good6_eq_bit (s : List Nat) : (code3 s).testBit 0 = good6 s := by
  unfold code3; exact (code3_bits _ _ _).1

theorem globallyGood_eq_bit (s : List Nat) : (code3 s).testBit 1 = globallyGood 6 s := by
  unfold code3; exact (code3_bits _ _ _).2.1

theorem decompOK_eq_bit (s : List Nat) : (code3 s).testBit 2 = decompOK 6 s := by
  unfold code3; exact (code3_bits _ _ _).2.2

theorem count_via_code (l : List (List Nat)) (p : List Nat → Bool) (q : Nat → Bool)
    (h : ∀ s, q (code3 s) = p s) : (l.filter p).length = ((l.map code3).filter q).length := by
  have hp : p = q ∘ code3 := funext (fun s => (h s).symm)
  rw [hp, List.filter_map, List.length_map]

theorem all_via_code (l : List (List Nat)) (p : List Nat → Bool) (q : Nat → Bool)
    (h : ∀ s, q (code3 s) = p s) : l.all p = (l.map code3).all q := by
  have hp : p = q ∘ code3 := funext (fun s => (h s).symm)
  rw [hp, List.all_map]

/-- **Proposition 2 on six points**: the local decomposition of the split weights holds for every
tree-generated system. -/
theorem decomposition_six : tg6.all (decompOK 6) = true := by
  rw [all_via_code tg6 (decompOK 6) (fun c => c.testBit 2) decompOK_eq_bit, tg6_codes]
  decide +kernel

/-- 141 of the 150 tree-generated systems on six points have a NANUQ metric that is Kalmanson for the given
order with exact support -/
theorem tg6_globally_good : (tg6.filter (globallyGood 6)).length = 141 := by
  rw [count_via_code tg6 (globallyGood 6) (fun c => c.testBit 1) globallyGood_eq_bit, tg6_codes]
  decide +kernel

/-- on six points, 6-locally good implies Kalmanson with exact support (Theorem 4 for `n = 6`) -/
theorem locally_good_imp_globally_good_six :
    tg6.all (fun s => !good6 s || globallyGood 6 s) = true := by
  rw [all_via_code tg6 (fun s => !good6 s || globallyGood 6 s) (fun c => !c.testBit 0 || c.testBit 1)
        (fun s => by
          show (!(code3 s).testBit 0 || (code3 s).testBit 1) = (!good6 s || globallyGood 6 s)
          rw [good6_eq_bit, globallyGood_eq_bit]), tg6_codes]
  decide +kernel

/-! #### The closure -/

/-- the list of the 108 systems of the substitution closure on six points
(exported by experiments/complexity/nanuq/export_lean_lists.py) -/
def C6 : List (List Nat) := [[6, 12, 14, 24, 28, 30], [6, 12, 14, 24, 28, 30, 48], [6, 12, 14, 24, 28, 30, 48, 56, 60], [6, 12, 14, 24, 28, 30, 48, 60], [6, 12, 14, 24, 28, 30, 60], [6, 12, 14, 24, 30], [6, 12, 14, 24, 30, 48], [6, 12, 14, 24, 30, 48, 56], [6, 12, 14, 24, 30, 48, 56, 60], [6, 12, 14, 24, 48, 56], [6, 12, 14, 24, 48, 56, 60], [6, 12, 14, 28, 30], [6, 12, 14, 28, 30, 48], [6, 12, 14, 28, 30, 48, 60], [6, 12, 14, 28, 30, 60], [6, 12, 14, 30], [6, 12, 14, 30, 48], [6, 12, 14, 30, 48, 56], [6, 12, 14, 30, 48, 56, 60], [6, 12, 14, 30, 48, 60], [6, 12, 14, 48], [6, 12, 14, 48, 56], [6, 12, 14, 48, 56, 60], [6, 12, 14, 48, 60], [6, 12, 24, 28, 30], [6, 12, 24, 28, 30, 48, 56, 60], [6, 12, 24, 28, 30, 56, 60], [6, 12, 24, 28, 30, 60], [6, 12, 24, 28, 48, 56, 60], [6, 12, 24, 28, 56, 60], [6, 12, 24, 48, 56, 60], [6, 12, 48, 56, 60], [6, 14, 24, 28, 30], [6, 14, 24, 30], [6, 14, 24, 30, 48], [6, 14, 24, 30, 48, 56], [6, 14, 24, 30, 48, 56, 60], [6, 14, 24, 30, 56], [6, 14, 24, 48, 56], [6, 14, 24, 48, 56, 60], [6, 14, 30], [6, 14, 30, 48], [6, 14, 30, 48, 56], [6, 14, 30, 48, 56, 60], [6, 14, 48], [6, 14, 48, 56], [6, 14, 48, 56, 60], [6, 24, 28, 30], [6, 24, 28, 30, 48, 56, 60], [6, 24, 28, 30, 56], [6, 24, 28, 30, 56, 60], [6, 24, 28, 30, 60], [6, 24, 28, 48, 56, 60], [6, 24, 28, 56, 60], [6, 24, 30], [6, 24, 30, 48, 56], [6, 24, 30, 48, 56, 60], [6, 24, 30, 56], [6, 24, 30, 56, 60], [6, 24, 48, 56], [6, 24, 48, 56, 60], [6, 24, 56], [6, 24, 56, 60], [6, 48, 56], [6, 48, 56, 60], [12, 14, 24, 28, 30], [12, 14, 24, 28, 30, 48], [12, 14, 24, 28, 30, 48, 60], [12, 14, 24, 28, 30, 60], [12, 14, 28, 30], [12, 14, 28, 30, 48], [12, 14, 28, 30, 48, 60], [12, 14, 28, 30, 60], [12, 14, 28, 48, 60], [12, 14, 30], [12, 14, 30, 48], [12, 14, 30, 48, 60], [12, 14, 48], [12, 14, 48, 56, 60], [12, 14, 48, 60], [12, 24, 28, 30], [12, 24, 28, 30, 48, 56, 60], [12, 24, 28, 30, 48, 60], [12, 24, 28, 30, 56, 60], [12, 24, 28, 30, 60], [12, 24, 28, 48, 56, 60], [12, 24, 28, 48, 60], [12, 24, 28, 56, 60], [12, 24, 28, 60], [12, 24, 48, 56, 60], [12, 28, 30], [12, 28, 30, 48, 60], [12, 28, 30, 60], [12, 28, 48, 56, 60], [12, 28, 48, 60], [12, 28, 60], [12, 48, 56, 60], [12, 48, 60], [24, 28, 30], [24, 28, 30, 48, 56, 60], [24, 28, 30, 56, 60], [24, 28, 30, 60], [24, 28, 48, 56, 60], [24, 28, 56, 60], [24, 28, 60], [24, 48, 56, 60], [24, 56, 60], [48, 56, 60]]

/-- `C6` consists of 108 pairwise distinct tree-generated systems -/
theorem C6_spec : C6.length = 108 ∧ C6.all (fun c => tg6.any (sameSet c)) = true ∧
    (tg6.filter (fun s => C6.any (sameSet s))).length = 108 := by decide +kernel

/-- **Lemma 8, computational part.**  Every system of `C6` is 6-locally good. -/
theorem closure_locally_good : C6.all good6 = true := by decide +kernel

end Complexity.NanuqFinite

#print axioms Complexity.NanuqFinite.trees5_spec
#print axioms Complexity.NanuqFinite.trees6_spec
#print axioms Complexity.NanuqFinite.five_point_facts
#print axioms Complexity.NanuqFinite.decomposition_five
#print axioms Complexity.NanuqFinite.tg6_length
#print axioms Complexity.NanuqFinite.tg6_locally_good
#print axioms Complexity.NanuqFinite.doubled_five_point_systems
#print axioms Complexity.NanuqFinite.decomposition_six
#print axioms Complexity.NanuqFinite.tg6_globally_good
#print axioms Complexity.NanuqFinite.locally_good_imp_globally_good_six
#print axioms Complexity.NanuqFinite.C6_spec
#print axioms Complexity.NanuqFinite.closure_locally_good
