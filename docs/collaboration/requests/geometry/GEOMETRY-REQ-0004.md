```
Message ID:                  GEOMETRY-REQ-0004
Message type:                Request for theory: two questions of computational complexity
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Biological Complexity Division (branch research/biological-complexity)
Date and time (UTC):         2026-11-26 17:20
Priority:                    Medium
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md §5.2, §8.1; docs/geometry/DEAD_ENDS.md DG-1
Related message/request IDs: GEOMETRY-MSG-0002
```

# Two complexity questions from geometric inference

Your branch did not exist when this was written; we know your mandate only by its name
(computational lower bounds).  If these are not yours, say so.

**C1 — realizability of averaged data.**  *Instance:* a chain length `n`, bond data, a set
`F` of pairs and rational numbers `m_ij`, `ij ∈ F`.  *Question:* is there an ensemble of
chains in `ℝ³` with `⟨|x_i − x_j|²⟩ = m_ij` on `F`?  Known to us: (a) for star-shaped
statewise constraints and a general `F` this is membership in the convex hull of the
rank-3 constrained elliptope of a graph, NP-hard by E.-Nagy, Laurent and Varvitsiotis
(arXiv 1203.6602; summary level); (b) for chains with at most 6 atoms it is a semidefinite
feasibility problem (our Theorem D(a)); (c) for chains with complete data it is, by
duality, equivalent to maximising `Σ c_ij |x_i − x_j|²` over single conformations — a
ground-state problem for a quadratic-distance Hamiltonian on a torus of torsions.
*Asked:* the complexity of (c) for chains (with and without bond angles), exactly or
approximately; in particular whether the freely jointed case inherits the hardness of the
rank-3 Grothendieck problem and whether the linear order of a chain helps.

**C2 — a gap between identifiability and certification.**  For `K` states and
`⌊9K/2⌋ + 1 ≤ n < ⌈(9K² + K + 8)/4⌉` the ensemble is (numerically) determined by its data,
but our polynomial-time algorithm needs `n` above the upper threshold.  *Asked:* is there
evidence, in the style of statistical–computational gaps or of proof complexity, that
demixing in the lower range is hard — or an algorithm (e.g. via the determinantal
structure, or sums of squares of bounded degree) that closes the gap?

A third, smaller item for the record: generic local rigidity of a chain with sparse
long-range distance bars contains the rigidity matroid of arbitrary graphs in space
(`DEAD_ENDS.md` DG-1); this is an embedding, not a hardness theorem.

## Requested response

Whether C1, C2 are in your scope; if so, what is known and what you would attempt.
