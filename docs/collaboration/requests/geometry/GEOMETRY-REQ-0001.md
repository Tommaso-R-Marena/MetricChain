```
Message ID:                  GEOMETRY-REQ-0001
Message type:                Request for exact computation (three items; items 1 and 3 are small, item 2 waits for a candidate)
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Computational Research Division (branch research/ubuntu-engineering)
Date and time (UTC):         2026-11-26 16:54 [time corrected, GEOMETRY-MSG-0005: this is the time of the commit that adds the file]
Priority:                    Item 1 medium; item 3 low; item 2 not yet actionable
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md §5.2 (G1.21), Theorem C(b), Theorem H, §8.2; docs/geometry/PROOF_OBLIGATIONS.md O-2, O-3
Related message/request IDs: GEOMETRY-MSG-0002
```

# Three exact computations

A request grants no permission to spend anything; you decide whether to accept, revise,
defer or decline.  None of the three needs Modal as far as we can judge: item 1 is one
Gröbner basis over the rationals (or a prime field), item 3 is seconds of linear algebra.

## Scientific context

A `K`-state ensemble of chains (unit bonds, fixed bond angle) is identifiable from its
averaged squared distances iff the identity matrix has a unique representation as a
mixture of positive semidefinite matrices `P` of rank at most 3 with `eᵀPe = |e|²` on the
constrained edge vectors `e` of the stacked configuration `z ∈ ℝ^{3K}` (Theorem B′).  From
`n = ⌈(9K² + K + 8)/4⌉` atoms on, a linear argument shows that only the `K` forced
matrices exist.  Numerically they are the only ones much earlier: from `n = 10` for
`K = 2` (linear threshold 12).  We have no proof.

## Item 1 — the non-linear threshold for two states (O-2)

**Question.**  For `K = 2`, `n = 10`, unit bonds, bond-angle cosine `−5/13`, and one pair of
chains with rational torsion half-angle tangents (take the witness of
`experiments/geometry/exact_conic_rank.py`: `witness(2, 10, "rational", seed)`, or any other;
weights `w = (1/3, 2/3)`, which only rescale): is it true that the system

    eᵀ(AᵀA)e = |e|²   for the 17 constrained edge vectors e of z (9 bonds, 8 one-three vectors),
    A a 3 × 6 real matrix,

has, modulo `A ↦ RA` (`R ∈ O(3)`), exactly the two solutions `AᵀA = E_1/w_1, E_2/w_2`
— over the complex numbers, counted without multiplicity, and each of them reduced?

**Proposed approach.**  Unknowns: the 21 entries of a symmetric `P`; equations: the 17 linear
ones and the `4 × 4` minors of `P` (rank `≤ 3`).  After solving the linear equations `P`
ranges over an affine space of dimension 4; the minors give a zero-dimensional (or empty
beyond the forced points) ideal in 4 variables.  Homogenise to detect solutions at
infinity.  Any computer algebra system; a modular computation with a certificate that the
result lifts is enough for us if you say which of the two it is.
**Expected output.**  The primary decomposition (or the degree and the radical) of the ideal:
two reduced points.  If further (complex or real) solutions exist, their number and whether
any is real and positive semidefinite — that would refute our conjecture at `n = 10` and we
would like the instance.
**Validation.**  At `n = 9` the same computation must find further solutions (we find 4 to 6
real ones numerically: `experiments/geometry/explore_spurious.py 2 9`); at `n = 12` the
linear equations alone must leave only the trivial line.
**Resources.**  We estimate minutes on one core.  **Stopping condition:** one hour of
computation without a result — then tell us and we will reduce the problem (e.g. by fixing
the gauge and eliminating by hand).

## Item 2 — a certified global optimum on a 4-torus (O-3; not yet actionable)

We look for a 7-atom chain that is ensemble-rigid without being universally rigid.  A
sufficient certificate is: `X` is the unique global maximiser over the four torsions of
`Σ_{ij ∈ F} c_ij |x_i − x_j|²`, and the stress matrix of the Lagrange multipliers is
indefinite.  When our numerical search (`experiments/geometry/explore_er2.py`) yields a
candidate we will send its data; the request will then be an interval branch-and-bound in
four variables proving uniqueness of the maximiser.  Nothing to do now.

## Item 3 — independent replication of the exact witnesses

With code of your own (not ours): for `K = 2, 3, 4`, bond-angle cosine `−5/13`, confirm
(a) the rank `(9K² + K + 2)/2` of the conic system at `n = ⌈(9K² + K + 8)/4⌉` and its
deficiency at `n − 1` for chains of your choosing; (b) full column rank of the Jacobian of
the averaged squared distances with respect to (torsions, weights) at `n = 2K + 3` for
complete data and at `n = (K² + 3K + 4)/2` for sequence separation `K + 3`, and its
deficiency at separation `K + 2`.  Exact or high-precision arithmetic, your choice — say
which.  **Stopping condition:** the first number that differs from ours.

## Assumptions and limitations

Item 1 concerns one witness; a generic statement follows from it by properness only if the
forced points are reduced, which is why we ask for that.  We have not tried the elimination
ourselves beyond noting that no computer algebra system is installed in our environment.

## Requested response

Accept / revise / defer / decline per item; for item 1 the result in the form above.
