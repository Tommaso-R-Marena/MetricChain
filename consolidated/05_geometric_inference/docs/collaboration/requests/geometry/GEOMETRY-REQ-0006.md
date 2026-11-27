```
Message ID:                  GEOMETRY-REQ-0006
Message type:                Request for certified computation (this is item 2 of GEOMETRY-REQ-0001, now actionable)
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Computational Research Division (branch research/ubuntu-engineering)
Date and time (UTC):         2026-11-26 17:56 [time corrected, GEOMETRY-MSG-0005: this is the time of the commit that adds the file]
Priority:                    Medium
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md §8.2; docs/geometry/PROOF_OBLIGATIONS.md O-3; experiments/geometry/er_not_ur_instance.py, explore_er3.py
Related message/request IDs: GEOMETRY-REQ-0001 (item 2), GEOMETRY-MSG-0003
```

# A certified global maximum on a 4-torus, and a certified realisation in four dimensions

A request grants no permission to spend anything.  We estimate that this needs no Modal:
one machine, an interval library, hours at most.

## Scientific context

"Second-moment rigidity" of a conformation `X` on a set `F` of measured pairs means: no
ensemble of other conformations has the averaged squared distances of `X` on `F`.  It is
implied by universal rigidity and implies global rigidity [Corrected by GEOMETRY-MSG-0006 after the internal review GEOMETRY-REV-0001: implied by universal
rigidity *together with the conic condition `𝒩(X) = 0`*, which holds for the instances of this
request; the request itself is unaffected].  We have numerical instances in
which it holds without universal rigidity; a proof needs a certified global optimum.

## Question

Chain of 7 atoms in `ℝ³`, unit bonds, bond angle 111° (statewise constraints: 6 bonds, 5
one-three distances), torsions `θ ∈ T⁴`.  Instance A (0-based atom indices):

    torsions θ* = (1.517404361415525, −1.046332870741514, 2.7119835539236874, −1.6743919325698102)
    F = {(0,4), (0,5), (1,4), (1,6), (2,6)}
    c = (−0.317197…, 0.185025…, 0.307367…, −0.150204…, 0.115451…)   [exact values: the stress of
        (F ∪ E₀, X*) restricted to F, sign chosen as in er_not_ur_instance.py; you may round c
        to rationals and re-optimise θ* — the claim is about the rounded c]

**(Q-a)** Is `H_c(θ) = Σ_{ij∈F} c_ij |x_i(θ) − x_j(θ)|²` maximised over `T⁴` exactly at
`±θ*` (the conformation and its mirror image), i.e. is every other `θ` strictly below?
**(Q-b)** Is there a configuration of 7 points in `ℝ⁴`, of affine dimension 4, with the
squared lengths of `X*` on all 16 pairs of `F ∪ E₀`?

## Proposed approach

(Q-a) Interval branch-and-bound on `[−π, π]⁴` for `H_c` (a trigonometric polynomial,
multi-affine in the `(cos θ_k, sin θ_k)`): a first-order exclusion test far from `±θ*`; near
`±θ*` an interval Hessian that is negative definite on a box `B` around `θ*` (then `θ*` is
the only critical point in `B`), and a second-order (centred-form) exclusion test in the
shells between `B` and the region where the first-order test works.  Our floating-point
numbers: `H_c(θ*) = 1.170181`; best value on a `24⁴` grid `1.167688`; best other local
maximum in 2 000 BFGS searches `1.154995` (margin `0.0152`); Hessian eigenvalues at `θ*` in
units of the largest stress eigenvalue: `−0.342, −0.099, −0.080, −0.0064` — the last one is
small, so `B` is small and most of the work is in the shells.  If that is too costly:
`python3 experiments/geometry/explore_er3.py <seed> <trials>` produces further candidates
(about one per thousand trials); pick one with a larger smallest curvature and margin and
certify that one instead — any certified instance proves the statement.
(Q-b) Interval Newton (Krawczyk) on the 16 length equations plus gauge conditions, started
at the configuration that `er_not_ur_instance.py` prints (residual `10⁻¹⁵`, singular values
`2.89, 1.61, 0.85, 0.15`).

## Expected outputs, validation, stopping

Outputs: for (Q-a) the list of boxes not excluded (expected: contained in `B ∪ −B`) and the
verified enclosure of the maximum; for (Q-b) an enclosure of a solution with a certified
positive fourth singular value.  Validation: the same code must *fail* to certify instance
`hierarchy_example.py`-style frameworks whose stress is positive semidefinite as "not
universally rigid" (there (Q-b) has no solution), and must find the second local maximum of
instance A.  Stopping condition: 24 core-hours without convergence of (Q-a) — then report
the size of the unresolved region and we choose a better-conditioned instance.

## Assumptions and limitations

We have not attempted the certification.  The statement that would follow — second-moment
rigidity is strictly weaker than universal rigidity — also needs the one-line argument of
report §8.2 (a unique maximiser of a functional supported on `F` is an exposed point of the
realizable set), which is not part of the computation.

## Requested response

Accept / revise / defer / decline; if accepted, which instance you certify.
