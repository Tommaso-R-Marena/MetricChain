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
