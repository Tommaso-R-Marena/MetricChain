# Dead ends, refuted claims and known-already findings — Geometric Inference division

Every claim that was made in this division's working notes and withdrawn, weakened or found
to be known.  Numbering `DG-n`.  Linked corrections of published messages are separate
messages (`docs/collaboration/README.md`).

**DG-1 (false; found before publication).  "For chains with fixed bond lengths and angles, a
set of additional distance bars is generically independent iff every window of atoms contains
at most as many bars as torsions (an interval Hall count)."**  False: all nine distances
between two rigid triangles `{a, a+1, a+2}` and `{b, b+1, b+2}` have rank at most 6 (two
bodies have six relative degrees of freedom) although the window between them may contain
nine torsions or more.  Worse, no count on windows can work: a generic chain with generic
heterogeneous bond data is a generic point configuration, so the rigidity matroid of *any*
graph `H` appears, restricted to bars among atoms that are pairwise at least three apart
along the chain — e.g. a "double banana" on eight such atoms is dependent while every
`3|V'| − 6` count holds.  Consequence recorded: generic local rigidity of chains with sparse
long-range distance data is exactly as hard as generic rigidity in three dimensions, for which
no combinatorial characterisation is known.  (Not a hardness theorem in the complexity
sense: the rank is computable in randomised polynomial time.)

**DG-2 (no gain).  "A conformation-independent quadratic form in the torsion changes can
replace the `ℓ¹` lever-arm bound of theory report §4.4 and gain a factor `√m`."**  The
displacement fields of two torsions can be parallel (parallel axes), so the supremum over
conformations of their inner product is the product of their norms, and every uniform
quadratic majorant is no better than the `ℓ¹` bound on coherent changes.  A gain needs the
conformation (the torsion-space metric tensor along a path), i.e. a certificate that depends
on the pair of conformations and not only on which torsions changed.  This is the content of
`docs/DEAD_ENDS.md` D10 of the theory division from another angle; nothing new.

**DG-3 (known).  "A positive semidefinite stress matrix with a spectral gap gives a global
Hölder-½ stability bound for a universally rigid framework — a new quantitative rigidity
theorem."**  Known in substance: it is the error bound for semidefinite feasibility problems
of singularity degree one (Sturm 2000; Drusvyatskiy–Pataki–Wolkowicz 2015; the role of
iterated stresses: Connelly–Gortler 2015).  Not claimed.  What we keep is the ensemble version
(Theorems F, G), which we did not find.

**DG-4 (known).  "For a sequentially localisable (trilateration) chain the stability constant
grows like `n²` (the softest mode is the bending mode of a beam)."**  The scaling is that of
the lowest bending frequency of a truss beam; equivalent-continuum models of lattice trusses
are classical in structural mechanics, and the Cramér–Rao analysis of range-based
localisation shows the same accumulation.  Not pursued in cycle 1; if taken up, the
contribution could only be a sharp constant or a global (non-infinitesimal) statement.

**DG-5 (overcount).  "The number of complex realizations of a minimally rigid chain framework
is `2^N per(S)`, `S` the incidence matrix of bars and the torsions they span."**  It is an
upper bound (the mixed volume of the Newton boxes of the bar equations in half-angle tangents)
and it is not attained: for the 6-atom chain with bars `15, 26, 16` the framework is the
octahedron graph with 16 realizations, the bound is 24.

**DG-6 (artefact).  First numerical search for a conformation that is second-moment rigid but not
universally rigid** (7 atoms, 5 measured pairs, maximiser of a quadratic-distance functional
with an indefinite stress): the two "candidates" had stress matrices of rank 4 and 5, which is
impossible for a non-planar equilibrium configuration of 7 points (rank at most 3) — the
optimiser had not converged and the eigenvalue threshold was loose.  The refined search (random couplings, polished maximisers) found nothing in the time it
was given; the inverse construction — start from the stress of a random framework and ask
whether the chain is a maximiser — finds instances at once (`explore_er3.py`; report §8.2).

**DG-7 (implementation).  DEMIX with automatic detection of the number of states under
noise** failed at noise `10⁻⁴` (the rank of the centred matrix and the nullity of the conic
system were read off with fixed thresholds).  The script now takes `K` as an input for noisy
data and enforces the certificate only for exact data; no stability claim is made for the
algorithm (the stability theorem is Theorem G, which is about the data, not the algorithm).

**DG-8 (wrong count, corrected before publication).  "The non-linear threshold for
identifiability among all ensembles is where a generic affine space of dimension
`dim 𝒩(z)` misses the variety of matrices with an eigenvalue of multiplicity `3K − 3`."**
The count gives the right numbers (`n = 10` for `K = 2`, `14` for `K = 3`) but the space
`I + 𝒩(z)` is not generic — it contains the `K` forced points — so the count is a heuristic,
confirmed numerically for `K = 2, 3` and not a proof.  Stated as a conjecture (G1.21).

**DG-9 (wrong expectation, published in GEOMETRY-REQ-0001 item 1 and corrected in
GEOMETRY-MSG-0003).  "For two states and ten atoms the chains that are linear images of the
stacked configuration form a projective scheme of two reduced points."**  The exact
computation (Singular, over `ℚ` and over `𝔽_32003`) gives degree 7.  The five extra units are
one point at infinity of length 5: the rank-2 quadric `abᵀ + baᵀ`, a pair of hyperplanes that
contains all seventeen stacked edge vectors (five consecutive bonds span each).  It is not a
chain (`c = 0`), and the statement that matters — no solution with `c ≠ 0` other than the two
states — is true and is now Theorem I; but the request as worded ("exactly the two solutions,
each reduced") described the affine chart only and would have been reported false by anyone
computing in projective space.  Lesson: the heuristic count of DG-8 ignores structural
low-rank quadrics, which exist whenever the stacked bonds can be covered by two hyperplanes
(`n ≤ 6K − 2`).

**DG-10 (narrowed).  "Identifiability among all ensembles starts where local identifiability
within `K` states starts."**  False for two states: at `n = 7, 8` the ensemble is locally the
only two-state ensemble with its data (Theorem H) and is nevertheless reproduced exactly by
mixtures of 9 to 11 other chains (`explore_below.py`).  The number of states is a prior with
real content in that range.

**DG-11 (name clash).  "Ensemble rigidity"** was our name, in the first two checkpoints, for
"no ensemble of other conformations has the averaged squared distances of `X` on the measured
pairs".  The Ensemble Identifiability Division had published the same words six minutes
earlier for determination by the *laws* of the edge lengths, which it proves equivalent to
generic global rigidity.  Ours is renamed *second-moment rigidity* everywhere except in the
published messages GEOMETRY-MSG-0001 … -0003 and the requests, which are records
(GEOMETRY-RES-0001 states the renaming).

**DG-12 (errors of record: clock times and two statements about other branches).**  The
"Date and time" headers of GEOMETRY-MSG-0001 … -0004, GEOMETRY-REQ-0001 … -0006 and
GEOMETRY-RES-0001, -0002 were estimates, not readings of a clock, and were wrong by up to
three hours (the third checkpoint was committed at 17:56 UTC; its messages said 20:10–20:50).
They now carry the commit times, with a bracketed note.  Two sentences were false for the
same reason — we wrote "your branch did not exist when this was written" to the Ensemble and
Complexity divisions on the strength of a fetch at 15:35 UTC, when both branches had existed
since 15:59 and 16:17 — and "forty minutes before our first commit" should have been six.
None of this touches a mathematical statement.  Rule adopted: a header time is either
`date -u` at the moment of writing or "the commit that adds this file"; every statement
about another branch names the fetch it rests on.  GEOMETRY-MSG-0005.

## Found by the internal review GEOMETRY-REV-0001 (2026-11-26, 18:55 UTC)

No stated theorem was found false.  What was wrong:

**DG-13 (a false slogan: "universal rigidity ⇒ second-moment rigidity ⇒ global rigidity").**
Written in the Summary (item 7: "a new rigidity notion between global and universal
rigidity"), in §9, in register row G1.18, in the heading of section 5 of the Lean file, and
sent in GEOMETRY-MSG-0002 (item 8), GEOMETRY-RES-0001 and GEOMETRY-REQ-0006.  Theorem E(a)
itself has the hypothesis `𝒩(X) = 0`, and the Lean theorem `secondMomentRigid_of_universal`
the hypothesis `SecondMomentRigid E₀ univ x`; the summaries dropped it.  Without it the
implication is false: when measurements and constraints together form the complete graph
the framework is universally rigid for a trivial reason, and a cis/trans mixture reproduces
the averaged data (Example 3.3 with `F = {14}`; three points `(1, 0, i)` with the path as
constraints — now `universal_not_secondMomentRigid` in Lean, the referee's proof).  Correct:
(universal rigidity and `𝒩(X) = 0`) ⇒ second-moment rigidity ⇒ (global rigidity and
`𝒩(X) = 0`).  "For chains with at most 6 atoms the first is an equivalence" is true in this
form only.  Lesson: a slogan in a summary is a statement and gets the hypotheses of the
theorem it summarises; the non-vacuity of each hypothesis should have been tested by trying
to drop it.

**DG-14 (sentences that claimed more than Theorem H proves).**  Theorem H is local (full
column rank of a Jacobian) and its sufficiency part is exact for `K ≤ 8` at two bond
geometries.  We wrote "identifiable if the number of states is known (`n ≥ 7`)" and "the
number of states is exactly the prior that restores identifiability" (local injectivity
only; global uniqueness among two-state ensembles is numerical); "the minimal separation is
exactly `K + 3`: each additional state costs one more unit of range, and nothing else"
(false for `K = 1`, where separation 3 suffices; unproved for `K ≥ 9`); "separation `K + 2`
never is" (needs `K ≥ 2`).  All corrected; GEOMETRY-MSG-0002 item 9 and GEOMETRY-MSG-0003
carry notes.

**DG-15 (a gap in the proof of Theorem E(d)).**  The proof invoked theorems about generic
frameworks (global rigidity from a stress matrix of maximal rank; a positive semidefinite
stress for generic universally rigid frameworks) and supported the existence of a generic
framework with an indefinite stress by a floating-point instance with unit bonds and one
bond angle — which is not generic, so the theorems did not apply to it, and whose global
rigidity was not shown at all.  Filled by an exact rational witness found by the referee
(six integer points; rigidity rank 12, stress matrix of rank 2 with the sum of principal
`2 × 2` minors `−5761/128`, conic rank 6) together with the openness of these conditions;
re-verified by an independent implementation (`exact_hierarchy_witness.py`).

**DG-16 (Corollary 9.1: "the constraints lower the order from `q = 3` to `q = 2`").**  Wrong
or ambiguous for both groups: second moments are blind to a reflection of each state, so
for proper rotations order 2 leaves the `2^K` handedness assignments open (order 3 is still
needed for them), and for rotations with reflections the unconstrained order is at least 4,
not 3.  The corollary now names the group and the estimand.

**DG-17 (sixteen minor defects, corrected).**  A false constant in the proof of Theorem G(d)
(`‖D(Δ)‖ ≤ 4‖Δ‖²`; correct `2n‖Δ‖²` in the Frobenius norm); Summary item 3 without "spans
space"; "every geometry" where only one bond angle at all positions is covered; Corollary
4.2 with an unstated hypothesis; Proposition 3.1 weaker than the truth in (a) and with a
wrong dimension in (b) (the weights are free without constraints: 10, not 9, for two states);
Theorem F without any instance; the hypotheses of Theorem F′ dropped in the Summary and the
genericity of one of them unproved (now proved for every `K`); "4 to 6" extra points at
`n = 9` (2 to 10); "a surface" for a four-dimensional family; `dim L` at `n = 12`; a claim
about the Kipnis–Shamir linearisation in Remark 5.1 that the count does not support
(**withdrawn**); real chimeras claimed for a single separation `s ≥ 4`; missing limitations
(helices never satisfy (CC); constraints must hold exactly and identically; `κ` is 2 to 12
times smaller than its local values); a misattributed result in `PRIOR_ART.md`; two Lean
lemmas called "non-vacuity" that instantiate no hypothesis; and a **process error**: the
register's review column said "REV-0001" in twenty rows while the review was still running,
and the report cited a review file that did not exist.  Rule adopted: a review column is
filled from the review, never before it.

## After the sixth checkpoint

**DG-18 (a wrong count for several states at the same hinges).**  While writing
`HINGE_ENSEMBLES.md` we guessed that `K` states at `s` hinges have finitely many candidate
chains (hence, presumably, an identifiable mixture) iff `s ≥ ⌈3(K − 1)/2⌉`, by counting
`9(K − 1)` unknowns of a matrix-affine combination against `6s` orthogonality conditions.
The conditions are not independent: the kernel of the block moment matrix contains the `s`
hinge relations, which every assembly satisfies, so for `3K ≥ 2s + 3` *every* assembly is a
candidate.  The computation (`hinge_multistate.py`) contradicts the guess at `K = 3, s = 3`
(a continuum of candidates).  The guess was written into a draft of the note and removed
before any commit; it is recorded here because the corrected statement is in the note.

