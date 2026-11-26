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

**ED15 (a theorem derived, then found in print).**  For the third checkpoint we proved that
the span of the pair-lifted vectors of up to `(1−ε)n²/2` random conformers contains no other
lifted vertex ("Odlyzko's theorem for symmetric squares"): reveal a first batch of
coordinates, where Abbe–Shpilka–Wigderson's independence theorem makes the coefficients
of a candidate unique; exclude candidates with few non-zero coefficients by a rank count;
and bound the probability that each further coordinate is consistent by Odlyzko's lemma on
sign vectors in a subspace.  The search made before writing it up — the first query about
spans of random rank-one sign matrices — returned Baldi and Vershynin (2019), Theorem 4.2:
the same statement for every degree, with the same method.  Recorded as a rediscovery;
the report cites the theorem and claims only what is built on it (E19(b)–(e)).  *Lesson:
search before proving when the statement has an obvious name ("Odlyzko for tensors");
the hour was not wasted — knowing the proof made it possible to check that the published
statement, in its `≤ d` lift with the constant coordinate, is exactly what E18 needs.*

**ED16 (two checks that failed for reasons of code, not of mathematics).**  The first run
of the torus checks (L4) reported that two states differing in both angles were *not*
identified, and that the projector certificate of five generic points on the 3-torus had
twelve zeros where six were expected.  The first was `True + True == True` for numpy
booleans in the test's bookkeeping (the linear programme had found the ensemble
identified, to `10⁻¹⁴`); the second was near-duplicate minimisers of a degenerate zero
that a tolerance of `10⁻⁴` did not merge.  Both were found by printing the quantities
before touching the mathematics.  A grid linear programme on the torus proves
non-identification when it finds a twin and proves nothing when it does not; the
exploratory grid runs for larger `K` are therefore not quoted in the report.

**ED17 (a hypothesis the kernel found missing, and a constant that was sixteen times too
small).**  The growth inequality behind Proposition E20″ was first proved with the
constant `min(β_−/4, β_min²/(64r))` — correct, machine-checked, and in the numerical search
never within a factor fifteen of the truth.  Looking at which case of the proof produced
the square showed that it was needed only for two angles; for three or more a pigeonhole
argument gives `β_min/4`, and for two the harmonic form `β_kβ_l/(4(β_k + β_l))`.  The first
Lean statement of the two-angle case had `θ ≥ 0` where the proof needs `θ > 0`: with
`θ = 0` the hypothesis `c(θ_0 + θ_1) ≤ θ_0θ_1` is empty and the conclusion is false; `linarith`
failed exactly there.  The crude version was removed from the proof tree.  *Lesson: when
a constant is far from what the numerics show, the proof has a case that deserves a
second look; and a formal statement is the cheapest referee for a missing positivity.*

**ED18 (a check that asserted more than the proposition).**  The first version of check
L7(c) required that on the cube, whenever the Hall condition of Proposition E21 fails,
the zero set of the permanent energy be strictly larger than the set of states.  It
failed — rightly: the proposition only says that the energy vanishes on the sub-cube of
states that agree with a violating set `I` where its members coincide, and on binary
sites that sub-cube can consist of the members of `I` alone (two conformers at Hamming
distance one: a sub-cube of two points).  Of the 10 944 triples on six sites that violate
the condition, only 960 have extra zeros.  The check now tests the containment that is
claimed; the proposition's wording says "on a torus a subtorus of positive dimension; on
binary coordinates possibly nothing but the states themselves".  So on finite alphabets
the Hall condition is sufficient and not necessary for this certificate.

**ED19 (a converse that was never proved, in a title).**  Version 2 called Theorem E15T
"the bound holds without frustration, **and only then**", and concluded that "frustration
is a real obstruction, not an artefact of the proof".  The theorem proved the bound for
references that are log-supermodular in the disagreement variables; the "only then" came
from five random chains with one violated bond on which the bound failed.  The second
internal review (ER2, F1) produced a triangle with a violated bond — `π ∝ exp(x₁x₂ + x₂x₃ −
½x₁x₃)` — on which both bounds hold for every member of the class, exactly; explained why
(the polarised member is positively associated although not log-supermodular: two
satisfied bonds induce an attraction that outweighs the direct repulsion); and gave the
two-line coupling proof under that weaker hypothesis.  The theorem is restated with the
hypothesis its proof uses.  A third example (population bound false, total-variation
bound true) shows that positive association is not necessary either: there is no
characterisation.  *Lessons: five failures are not a converse; a title is a statement;
and when a proof uses a strong hypothesis (FKG lattice condition) only through a weak
consequence (positive correlation of two monotone functions), state the weak one.*

**ED20 (quoted numbers that the script did not print — third occurrence, and a remedy).**
ER1 found it twice (F6, F18); ER2 found it again (F2): the text of check F6 quoted
`+0.23` to `+0.47` where the script printed `+0.024` to `+0.965`, "`0` to `10⁻¹⁵`" where it
printed `3·10⁻¹⁴`, and asserted a failure of the population bound that the script computed
and discarded.  The cause is the same each time: a sentence written from an exploratory
run, and a script changed afterwards.  The remedy is now mechanical:
`experiments/ensemble/check_quotes.py` ties sentences of the report to lines of the stored
output (literal matches, or bounds for round-off-level numbers), and `run_all.py` runs it
last, so a changed script fails the run until the sentence has been looked at again.

**ED21 (a conditional statement about chains whose two conditions were false).**  After
the third checkpoint we wrote (ENSEMBLE-RES-0003 §4, report §4c.4) that Proposition E20′ —
two states on a torus are determined iff they differ in at least two angles — "becomes a
theorem for chains" if (i) competing ensembles live on the torus of the differing
torsions and (ii) the mean squared distances span the products over pairs of those
torsions.  Both fail (GEOMETRY-RES-0005 §§2–3; the science division's SCI-REV-0021):
competitors live on `O(2)^r` — consecutive rigid segments may also be related by a
reflection in a plane through the hinge bond — and for three torsions the span contains
only the products of *adjacent* pairs.  The statement for chains is those divisions'
(identifiable unless two of `R₁`, `R₂`, `R₁R₂` are half-turns).  Ours remains a statement
about measures on a torus; the adjacent-pair certificate that survives is the geometry
division's.  Linked correction: ENSEMBLE-RES-0004 §3.  *Lesson: a conditional statement
that names its conditions is honest, and still costs the reader who has to check them;
ask before publishing the conditional.*

**ED22 (the thermal union bound as a falsification test).**  We suggested (ENSEMBLE-MSG-0003,
E-S3) that Theorem E15 could certify that an ensemble is *not* in a first-order class:
data showing a distance to the polarised member larger than the bound.  The science
division tried it on two five-residue instances with exact least envelopes and the most
favourable datum (the exact total variation) at 232 centres: the test never fires above
`b = 0.015`, although the truth leaves the class as soon as `b < 1` (SCI-RES-0032 §2).  The
true ensemble is far from polarised, and as the class shrinks the polarised member moves
towards it.  For one-body data the exact test is that division's ratio test (the product
structure of the one-body marginals).  Suggestion withdrawn.

**ED23 (a conjecture refuted before it was stated: random sampling is not an adversary).**
After finding the exact condition for the thermal union bound (Proposition E15U: one
inequality per up-set), we observed that for known parts with pair interactions the
whole condition coincided with its `n` single-site instances — `Cov(e_i, N − e_i) ≥ 0` for
every site — on every one of 17 000 random pair models on three and four sites, and
drafted it as a conjecture.  It is false: a direct minimisation of the worst non-dictator
slack subject to the single-site conditions found a four-site pair model within twenty
restarts (two strongly bound pairs that repel each other; the up-set "both sites of a
pair are switched" violates the condition; margin `0.01`).  The region is thin, which is
why sampling missed it.  For general measures a three-body ("parity") known part on
three sites is a counterexample in closed form.  On three sites with pair interactions
no counterexample was found by the same adversarial search (1 650 restarts); that case
is left open without a conjecture.  *Lesson: before writing "in every instance tried",
let an optimiser try.*

**ED24 (a count of conditions that was never computed; and what a grid cannot show).**
Remark 3 to Proposition E21, the torus row of the table of §4c.5 and Problem O10 said that
"three double points impose nine conditions on the nine-dimensional span" of the bilinear
data on a torus of two angles, concluded that three states "generically" fail to be
identified, and extrapolated the count to a conjectural threshold `(3^r − 1)/(r + 1)`.  The
rank was never computed.  It is 8 for every triple: the squared modulus of the bilinear
form through the three states lies in the span, vanishes at the states with its
gradient, and is not zero.  Read with the right rank the count would have suggested the
opposite conclusion.  The conclusion is nevertheless true — for *every* triple, by a
different argument (competing measures live on a circle on which the data are
trigonometric moments of order two of a weighted measure: Proposition E22) — and the
extrapolated threshold is wrong (`r = 3`: five generic states are identified, six are
not).  All of this was found by the third internal review (ER3, F1).  The same review
points out why our numerical habit could not have caught it: a linear programme over a
*product grid* of angles reports three states as identified in 38 of 40 cases, because
the twin lives on a curve that misses the grid.  *Lessons: a parameter count is a
computation — do it; on a continuous space, look for twins on the zero set of the
certificate, not on a grid.*

**ED25 ("ratios of averages are covered by nothing" — written, published, and wrong within
two hours).**  Proposition E17.1 and the first version of `SOFTWARE_INTERFACE.md` listed "a
ratio or a square of averages" among the data that no statement of ours covers.  For a
ratio of two means with a positive denominator this is false: multiplying by the
denominator gives two linear constraints, and the whole linear theory applies; likewise
an unknown overall calibration factor only removes the normalisation (Proposition E23).
The sentence had been written as a caution, without trying the first thing one would
try.  Squares and lengths of means are genuinely different (Theorems E25, E26).  *Lesson:
a statement of what is not covered is a mathematical claim too; test it before sending
it to people who will build on it.*

