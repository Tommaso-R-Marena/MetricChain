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

**ED7 (a threshold that is not where two heuristics put it).**  After Theorem E10 we expected
the capacity of pair data to be exactly `n`: the positive semidefinite certificate stops
there, and a count of Wendel type (the `Kn` single-flip constraints against the
`n(n−1)/2` couplings: a generic subspace of that dimension meets an orthant of `ℝ^{Kn}` iff
`K < n − 1`) agreed.  Exact linear programmes say otherwise (report §4.4): at `K = n` random
conformers are faces with frequency rising to one, the point of frequency one half is
at `1.12n`–`1.15n` for `n = 14, …, 20`, and single-flip stability with symmetric couplings
survives to about `1.6n`.  The count fails because the constraint vectors are not in general position
(they all correlate with the anti-Hebbian direction).  The conjecture "`α* = 1`" was
written in a draft and never published; what is published is Conjecture C2.

**ED8 (an experiment confounded at small sizes).**  The first run of
`symmetric_stability.py` showed, at `n = 10`, a *smaller* probability for the necessary
condition (strict single-flip stability) than for the property it is necessary for.  The
script draws conformers independently, and at `n = 10` two of them are equal or adjacent
modulo the flip with probability near one, which makes strict stability impossible; the
face computation draws distinct conformers and allows adjacent ones.  The numbers quoted
in the report are for `n ≥ 20`, where adjacency has probability below one per cent.

**ED9 (the constant 6.34 was not the right bound).**  Checkpoint 1 stated non-identification
beyond `6.34n` conformers (Gaussian signs, equal weights) as Theorem E11.  The argument of
Theorem E12(c), used at one site, gives `2n` for every weighting (Cover's count); it was in
the report all along and we did not see it.  E11(a) is now the `2n` bound; the Gaussian
twin is kept as E11(b) because it is explicit.

**ED10 (a "violation" that was the solver's tolerance).**  The first numerical test of the
thermal union bound for complete-graph references reported excesses of `7·10⁻⁵` and
`2·10⁻⁴` at five and six sites — where the theorem had just been proved.  The class
constraints had been written as `μ(y)π(x) ≤ e^b μ(x)π(y)` with coefficients of order
`10⁻³`, so the solver's absolute feasibility tolerance allowed relative violations of the
class of the size of the excess.  In the weights `w = μ/π` (coefficients of order one),
with the returned vertices repaired by the least Lipschitz majorant of `−log w`, the excess
is `3·10⁻¹⁵`.  The published check F6 uses the well-scaled form.  *Lesson: a numerical
counterexample to a proved statement is first a statement about the numerics.*

**ED11 (a theorem first stated too narrowly).**  The extension of the thermal union bound
to interacting references was first written for trees (induction over leaves, with a
"satisfied bond" hypothesis on the parent–child factor).  The induction needs only that
the conditional law of the last site is monotone and that marginals stay
log-supermodular, which is the FKG lattice condition and holds on any graph.  The tree
version was never published; Theorem E15T is stated for log-supermodular references.

**ED12 (three slogans that said more than the theorems; found by the internal review
ER1).**  Version 1 of the report summarised its results in sentences that were false as
written, although every numbered statement behind them was correct.
(i) "An ensemble is determined exactly when it is exposed by a non-negative function in
the span."  False both ways: with one feature `(0, 0, 1)` on three configurations the
ensemble `½δ_a + ½δ_b` is exposed and not identified (the independence condition was
dropped); Example E1.2 is identified and not exposed (compact spaces need the minimal
face).  (ii) "Identification = absence of chimeras."  Only one direction holds: chimeras
that cannot be combined into a table with the right marginals do no harm — three
configurations with features `(0,0), (1,1), (0,1)`; and, on an open set of pairs, `K₄` plus
a vertex of degree two with a wide second conformer (report §3.2, check R7).  The exact
criterion is the uniqueness of a non-negative table on the realisable colourings.
(iii) "An identified `K`-conformer ensemble has correlation rank `K`."  True on the event of
Theorem E10 only: `CUT₃` is a simplex, so four conformers on three sites are identified
with rank three.  *Lesson: the sentence that summarises a theorem is a statement and gets
the same scrutiny as the theorem; an "exactly when" needs both directions proved for the
objects it names.*

**ED13 (a number in the text that no script printed).**  The report quoted "all 22 zeros"
for check R5; the script printed 82 (one at the first conformer, 81 at the second).  The
number had been typed from an earlier run with a different seed.  The check now starts
100 runs near each conformer and 200 at random (203 zeros: 63 and 140), and the text
quotes the stored output.  Two further checks tested less than they said: T2 carried an
assertion ending in `or True`; C2 accepted `0.278` against `0.401` under a tolerance of
fifty per cent.  Both are tightened (review ER1, F18).

**ED14 (a theorem about two bodies stated with one leg too few and two quantifiers
exchanged).**  Theorem E7′ of the second checkpoint said the leg-length matroid is
connected iff `m ≥ D_d + 1`; for one leg it is connected too (a single element), and the
failure of identification there is for the trivial reason that one length does not fix a
pose.  Its proof of (b) took the pose first and the extra leg generic afterwards, while
the statement fixes generic attachment points first; the dimension count on the incidence
set that justifies the exchange is now written out.  Found by the review ER1 in passing.
