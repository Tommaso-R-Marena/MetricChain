# Dead ends — Ensemble division

Claims made and withdrawn, conjectures refuted, approaches that failed, each with the reason
and — where one exists — the counterexample.

**ED1 (a question that the literature had answered).**  ENSEMBLE-MSG-0001 asked the Geometric
Inference Division (E-G1) whether generic global rigidity in `ℝ³` implies a connected
rigidity matroid, and planned Theorem E7 with connectivity as an extra hypothesis.  The
first literature search found the answer: yes, in every dimension
(Garamvölgyi–Gortler–Jordán 2022, Theorem 3.5).  The question is withdrawn
(ENSEMBLE-MSG-0002); Theorem E7 has no extra hypothesis.  *Lesson: search before asking.*

**ED2 (a capacity that was not ours).**  The first plan for Theorem E10 was to prove a
capacity `K < 0.2933n` by a Littlewood–Offord lemma and a union bound, and to present the
constant `ln(4/3)/ln(8/3)` as the result.  Odlyzko (1988) had determined the probability up
to `K ≤ n − 10n/ln n` with the exact leading term.  Our argument is kept only as a
self-contained proof of a weaker range; the theorem cites Odlyzko.

**ED3 (a heuristic that contradicts a theorem).**  For the threshold of Problem O1 we tried
the kinematic heuristic "`K` cones of statistical dimension `δ` in `ℝ^D` meet iff
`K(D − δ) < D`", with the normal cone of the cut polytope at a vertex.  The single-ray
estimate of the Gaussian width of the cut cone (`≈ 0.76√n`, the Sherrington–Kirkpatrick
constant) gives a threshold below `0.86n`, which contradicts E10(c).  The normal cones at
the vertices are images of one another under the switching group, not under random
rotations; the heuristic does not apply.  Nothing was claimed.

**ED4 (unlabeled PCA is not a special case).**  We first described Theorem E5 as a
generalisation of unlabeled principal component analysis "from linear subspaces to
varieties".  It is not: there the subspace is unknown (the variety is the determinantal
variety) and generic; here the variety is known and arbitrary.  The two results are
neighbours, neither contains the other.  The report says so.

**ED5 (a numerical control with the wrong expectation).**  The first version of check R4
expected every splice along a separator of `K₄` plus a vertex of degree two to be
realisable for nearby conformers; 18 of 20 were.  Theorem E5(b) asserts realisability on a
neighbourhood whose size depends on the base point; the exact criterion (two circles meet)
agrees with the solver in 40 of 40 cases.  The check now tests the criterion.  Similarly
the threshold of check R3 was an arbitrary constant; it is now relative to the residual at
a true conformer.

**ED6 (not pursued: counting bits for adaptive lower bounds).**  A lower bound on the number
of adaptively chosen pair observables by counting cells of a hyperplane arrangement gives
only `K/2`: exact real-valued data carry unbounded information per measurement.  The
lower bound of Theorem E12(c) is structural (local stability and Cover's theorem) instead.
