/-
Corollary 5′ of docs/complexity/NANUQ_LOCAL_CRITERION.md on six points, checked by the Lean kernel.

For every tree-generated circular split system on six points and each of the twelve dihedral placements
`(u₁; z, w; u_p; v₁, v_q)`:

    Φ6 < 0   ⟺   the system contains its three 3-splits and does not contain the 2-split {z, w}.

Also: 133 of the 150 systems have no negative six-leaf term, and 17 contain the three 3-splits while
missing a 2-split (the six-point part of Theorem 10′(d)).

The definitions are those of `NanuqFinite.lean`, copied (that file is not a module that can be imported):
systems are lists of masks of the sides not containing leaf 0; `tg6` is defined from the list of the 14
trees, whose correctness is `NanuqFinite.trees6_spec`.

Only `decide +kernel` is used; no `native_decide`, no `sorry`, no axioms beyond the standard ones.
-/
import Mathlib

namespace Complexity.NanuqPattern

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

/-- the dihedral placement `t ↦ r + t` or `t ↦ r - t` (mod `n`) -/
def place (n r : Nat) (fwd : Bool) (t : Nat) : Nat := if fwd then (r + t) % n else (r + n - t) % n

/-- mask of the interval `{i,…,j}` -/
def interval (i j : Nat) : Nat := 2 ^ (j + 1) - 2 ^ i

/-- the non-trivial circular splits of `n` points -/
def splits (n : Nat) : List Nat :=
  (List.range n).flatMap (fun i => (List.range n).filterMap (fun j =>
    if 1 ≤ i ∧ i + 1 ≤ j ∧ j + 3 ≤ n + i then some (interval i j) else none))

def sysOf (n k : Nat) : List Nat := ((splits n).zipIdx.filter (fun p => k.testBit p.2)).map (·.1)

def allSystems (n : Nat) : List (List Nat) := (List.range (2 ^ (splits n).length)).map (sysOf n)

def treeGenWith (ts : List (List Nat)) (s : List Nat) : Bool :=
  ts.any (fun t => t.all (fun m => s.contains m)) &&
    s.all (fun m => ts.any (fun t => t.contains m && t.all (fun m' => s.contains m')))

def trees6 : List (List Nat) :=
  [[6, 14, 30], [6, 14, 48], [6, 30, 24], [6, 24, 56], [6, 56, 48], [14, 30, 12], [14, 12, 48],
   [30, 12, 28], [30, 28, 24], [12, 28, 60], [12, 60, 48], [28, 60, 24], [60, 24, 56], [60, 56, 48]]

/-- the tree-generated systems on six points -/
def tg6 : List (List Nat) := (allSystems 6).filter (treeGenWith trees6)

/-- canonical mask (the side without leaf 0) of the 2-split `{a,b}` of six points -/
def pairMask (a b : Nat) : Nat :=
  let m := 2 ^ a + 2 ^ b
  if m.testBit 0 then 63 - m else m

/-- the three 3-splits of six points: `{1,2,3}`, `{2,3,4}`, `{3,4,5}` -/
def hasThree (sys : List Nat) : Bool := sys.contains 14 && sys.contains 28 && sys.contains 56

/-- the forbidden pattern at a placement: the three 3-splits without the 2-split `{z,w} = {y 1, y 2}` -/
def patternAt (sys : List Nat) (y : Nat → Nat) : Bool :=
  hasThree sys && !(sys.contains (pairMask (y 1) (y 2)))

/-- `Φ6 < 0` at a placement -/
def negAt (sys : List Nat) (y : Nat → Nat) : Bool :=
  decide (phi6x2 sys (y 0) (y 1) (y 2) (y 3) (y 4) (y 5) < 0)

theorem tg6_length : tg6.length = 150 := by decide +kernel

/-- **Corollary 5′ on six points.** -/
theorem phi6_neg_iff_pattern :
    tg6.all (fun s => (List.range 6).all (fun r =>
      (negAt s (place 6 r true) == patternAt s (place 6 r true)) &&
      (negAt s (place 6 r false) == patternAt s (place 6 r false)))) = true := by decide +kernel

/-- no negative six-leaf term in any placement -/
def noNeg (s : List Nat) : Bool :=
  (List.range 6).all (fun r => !negAt s (place 6 r true) && !negAt s (place 6 r false))

/-- the six 2-splits: `{1,2}`, `{2,3}`, `{3,4}`, `{4,5}`, `{5,0}`, `{0,1}` -/
def twoSplits : List Nat := [6, 12, 24, 48, 30, 60]

/-- 133 of the 150 systems have no negative six-leaf term (the class `𝒦′` on six points). -/
theorem kprime_six : (tg6.filter noNeg).length = 133 := by decide +kernel

/-- 17 systems contain the three 3-splits and miss a 2-split; they are exactly the systems with a
negative six-leaf term. -/
theorem seventeen :
    (tg6.filter (fun s => hasThree s && !(twoSplits.all (fun m => s.contains m)))).length = 17 ∧
    tg6.all (fun s => (hasThree s && !(twoSplits.all (fun m => s.contains m))) == !noNeg s) = true := by
  decide +kernel

end Complexity.NanuqPattern

#print axioms Complexity.NanuqPattern.phi6_neg_iff_pattern
#print axioms Complexity.NanuqPattern.kprime_six
#print axioms Complexity.NanuqPattern.seventeen
