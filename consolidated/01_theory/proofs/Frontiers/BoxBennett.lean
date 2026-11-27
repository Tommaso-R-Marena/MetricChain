/-
Copyright (c) 2026 MetricChain contributors. Released under Apache 2.0.

# The floor-plus-variance bracket in the vocabulary of box classes (theory report §11.30, Theorem 11.110(f))

`BennettTwoPoint.lean` — written by the Scientific Discovery Division, its workstream L4, and adopted — proves the
two-point Bennett–Hoeffding bound and the bracket built on it for finite laws.  This file states the bracket with
the objects of `BoxClass.lean`: unnormalised Gibbs weights `w ≥ 0` of the known function, `Z = Zw w r`, and the mean
`m` of the remainder under the Gibbs measure of the known function.  The lower end is `jensen_bracket`; the upper
end is the division's `ScienceL4.Bennett.bennett_bracket_weights`, which was written for this vocabulary and fits
it without change (the division asked us to check: its message SCI-MSG-0023, request L4-T1).
-/
import Mathlib
import proofs.Frontiers.BoxClass
import proofs.Frontiers.BennettTwoPoint

namespace MetricChain.BoxClass

open Finset

variable {X : Type*} [Fintype X]

/-- **The floor-plus-variance bracket for a box class** (theory report Theorem 11.110(f)), in the vocabulary of
`jensen_bracket`: with `m` the mean of the remainder under the Gibbs measure of the known function, a floor
`r ≥ m - b` on the support and a variance bound `v`, `log W - m ≤ log Z ≤ log W - m + W(b, v)`, where
`W(b, v) = ScienceL4.Bennett.bennettW b v` is the logarithm of the two-point bound. -/
theorem bennett_bracket {w r : X → ℝ} (hw : ∀ x, 0 ≤ w x) {x₀ : X} (hx₀ : 0 < w x₀) {b v : ℝ} (hb : 0 < b)
    (hfloor : ∀ x, w x ≠ 0 → (∑ y, w y * r y) / ∑ y, w y - b ≤ r x)
    (hvar : (∑ x, w x * (r x - (∑ y, w y * r y) / ∑ y, w y) ^ 2) / ∑ y, w y ≤ v) :
    Real.log (∑ x, w x) - (∑ x, w x * r x) / ∑ x, w x ≤ Real.log (Zw w r) ∧
      Real.log (Zw w r) ≤
        Real.log (∑ x, w x) - (∑ x, w x * r x) / ∑ x, w x + ScienceL4.Bennett.bennettW b v :=
  ScienceL4.Bennett.bennett_bracket_weights hw hx₀ hb hfloor hvar

end MetricChain.BoxClass
