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
