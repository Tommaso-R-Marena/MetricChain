# Dead ends, refuted claims, and things that turned out to be known (complexity division)

Numbered `CX-Dn`.  Each entry: what was believed, what refuted it, where the evidence is.

## CX-D1 — "PF-polynomial magnifiability of the NN model is open" (2026-11-26)

*Believed (from the DNA 31 paper, Future Work item 2, and the research owner's brief):* whether the
multi-stranded nearest-neighbour model with rotational symmetry admits a polynomial-time magnifiable
partition-function algorithm is open.  On first reading we sketched a positive answer (Burnside/Möbius
decomposition by symmetry order + a dynamic programme over rotation-invariant structures).

*Fact:* the question was answered in the affirmative by two of its own authors three days before
this division started: A. Shalaby, D. Woods, *One partition function call to rule them all*,
arXiv:2611.27945 (v2, 23 Nov 2026) — the same idea (decomposition by symmetry degree `R`, "slices",
inclusion–exclusion).  Found by a web search on 2026-11-26 before any text of ours was written.
Nothing of our sketch is claimed.  See `PRIOR_ART.md` §A and `OPEN_PROBLEMS.md` A2.

## CX-D2 — "The NANUQ metric of every circular split system is circular decomposable" (2026-11-26)

*Tempting generalisation:* since the NANUQ metric `d_N` of a network depends only on the circular split
system `Σ = Split(T(N))` (through the displayed quartets), one might hope that `d_Σ` is Kalmanson with
support `Σ` for *every* circular split system that displays a quartet on every 4-set.

*Refuted [X]* by exhaustive enumeration (`experiments/complexity/nanuq/exhaust_all_systems.py`,
`exhaust_tree_generated.py`): on 5 points there are systems whose metric has support strictly larger
than `Σ`; on 6 points there are 33 systems with a negative split weight, and 3 of them are unions of
split systems of binary trees, e.g. all nine non-trivial circular splits except the two antipodal
2-splits `{x0,x1}` and `{x3,x4}` give `α = −1` on exactly those two.  So the conjectures of Holtgrefe
et al. are statements about network structure, not about circular split systems in general.

## CX-D3 — two flagship candidates were not cleanly open (2026-11-26)

Both starting problems of the brief had moved by the time we verified them: A2 is solved (CX-D1) and
B1/B2 carry an unreviewed third-party claim of a computer-assisted proof for all levels (see
`OPEN_PROBLEMS.md` B, `PRIOR_ART.md` §B).  Recorded here because the brief asked that the candidates
be *verified*, and the verification changed the plan.

## CX-D4 — false or too broad sentences in our own first versions (2026-11-26; found by review)

Recorded so that they are not repeated.  (i) "(H0)–(H2) is the sign pattern of every physical parameter set"
— false: the single-nucleotide bulge rule of the 2004 parameters gives a bulged C between G–C pairs a
negative energy (COMPLEXITY-REV-0001 finding 1; SCI-REV-0019 F2, independently).  (ii) "With coaxial stacking
as strong as stacking the reduction fails" — false unless the bulge over the separator is free; the truth is
Theorem 1c.  (iii) The ETH corollary cited a lower bound for 3-dimensional matching that its source states
without the linear bound on the number of triples it needs; a citation taken from a citation.  (iv) "The
partition function is #P-hard as soon as the number of species is unbounded" — only with the magnification
or temperature as input.  (v) "All displayed trees of a galled planar network are restrictions of one planar
tree" — only if every hybrid node has a leaf child.  (vi) "Direct tests" of the all-level NANUQ theorem that
generated networks from the very structure lemmas they were meant to test.  (vii) Times in message headers
that were estimates.  All corrected in COMPLEXITY-MSG-0003 §1.

## CX-D5 — the all-level NANUQ theorem is probably not new (2026-11-26)

The third-party summary's "122 distinct quartet systems" equals `|𝒜_3|+|𝒜_4|+|𝒜_5|+|𝒜_6|` (referee's
observation).  The method — six-leaf reduction, plane trees with duplicated leaves, composition — is in all
likelihood the same.  What remains without prior art found: the necessity of "galled" (CX-T7), sharpness
(CX-T8), the parametric family in our extension (CX-T13).

## CX-D6 — Ising ground sets: things that are not true or did not work (2026-11-26)

(i) "Exposed iff the span of the states contains no other sign vector" is false in general: only
"not exposed ⟹ another sign vector in the span" holds (if the column types are linearly independent the span
is everything and the set can be exposed); it becomes an equivalence under a pair-separating sign symmetry
(Proposition 10).  (ii) "Not exposed iff some four states have constant product": false from `K = 5` on (one
of the six non-exposed orbits has no such four states; three exposed orbits have them).  (iii) Attempts at
co-NP-hardness for `K` in the input: the most symmetric instances (sets of characters of `F_2^r`) are decided
by the Sidon criterion in polynomial time; adding further orbits of types obtained by twisting with Boolean
functions of two or three linear forms gives constraints that are linear over `F_2`.  Approaches through
faces cut out by tight valid inequalities need the known solutions to span the equality space, i.e. about
`K²/2` planted solutions.  No reduction found.

## CX-D7 — Lean: two practical traps (2026-11-26)

(i) A hand-typed list of the 14 binary trees on six circularly ordered leaves contained an incompatible
triple (15 entries); the statements proved from it would have been about the wrong object.  It was caught
only because the trees were also *defined* in Lean (maximal sets of pairwise compatible splits) and the list
compared with the definition (`trees6_spec`).  Lists that enter a kernel check should be defined or
specified inside Lean whenever that is feasible; the one list that is still imported (`C6`) is flagged.
(ii) Evaluating the NANUQ metric of all 150 six-point systems in a single `decide +kernel` exhausts 16 GB;
splitting into sixteen pieces and reassembling by proved lemmas keeps the peak near 11 GB (6.6 GB of which
is the memory-mapped Mathlib).

