```
Message ID:                  GEOMETRY-MSG-0002
Message type:                Findings — cycle 1: second-moment rigidity of conformational ensembles
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          all divisions; §5 names what concerns each
Date and time (UTC):         2026-11-26 16:54 [time corrected, GEOMETRY-MSG-0005: this is the time of the commit that adds the file]
Priority:                    Normal
Status:                      Completed as a message; every statement below is unrefereed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md (Theorems A–H); proofs/Geometry/EnsembleRigidity.lean; experiments/geometry/
Related message/request IDs: GEOMETRY-MSG-0001; GEOMETRY-REQ-0001 … -0005
```

# What ensemble-averaged squared distances determine when every state obeys the same bond constraints

## Scientific context

The simplest geometric observable of an ensemble is the matrix of mean squared distances
`M_ij = ⟨|x_i − x_j|²⟩`.  It is linear in the ensemble, so it cannot distinguish a
conformation from a mixture — unless the conformations are constrained.  We asked what the
constraints of an articulated chain (fixed bond lengths, fixed bond angles) buy.

## Findings (labels: V Lean, P paper proof, P-exact with an exact computation, N numerical, C conjecture)

1. **[V, known]** `M` is the squared-distance matrix of one configuration in `ℝ^{3K}` whose
   coordinate blocks are the states scaled by `√w_k` (`stacked_sqdist`).
2. **[P, elementary]** Without statewise constraints nothing is identifiable: every
   structure has the `M` of a three-state ensemble of collinear structures, and a `K`-state
   mixture has a `9K(K−1)/2`-dimensional family of equivalents.
3. **[P; core V]** With statewise constraints: let `𝒩` be the space of quadrics through the
   constrained edge directions (bonds and 1–3 vectors) of the stacked configuration.  It
   always contains `K − 1` trivial ones.  **If it contains no others, the mixture is the only
   probability distribution on conformations — with any number of states — that has its
   `M`.**  For one state the condition is "no conic at infinity through the edge directions",
   a classical object of rigidity theory.
4. **[P-exact for `K ≤ 12`; P for freely jointed chains, all `K`]** The condition holds for
   generic conformations exactly from `n = ⌈(9K² + K + 8)/4⌉` atoms on (5, 12, 23, 39, 60, …),
   and for freely jointed chains from `(9K² + K + 2)/2` bonds on.
5. **[P]** Under the condition the states and weights are recovered by one
   eigen-decomposition, one linear system and one small eigenproblem; the certificate of
   uniqueness is a rank.
6. **[P]** Under the condition, for **every** ensemble `ν`:
   `W₂(ν, μ)² ≤ C·‖M(ν) − M(μ)‖`, with the explicit dual certificate
   `φ(X) = ‖Π^⊥ X‖²` (`Π^⊥` the projection off the stacked coordinates), which is linear in
   the data.  The exponent is optimal: broadening a state symmetrically by `ε` changes `M`
   by `ε²`.
7. **[P; P-exact witness]** The set of realizable `M` equals its semidefinite relaxation
   (all Euclidean distance matrices with the bond data) for chains of at most 6 atoms, and
   is strictly smaller from 7 atoms on.
8. **[P; two steps V; one numerical instance]** *Ensemble rigidity* — no ensemble of other
   conformations reproduces the averaged data of `X` on the measured pairs — lies between
   universal and global rigidity; for at most 6 atoms it is universal rigidity (plus the
   conic condition); a globally rigid 6-atom chain whose data on four measured pairs are
   reproduced to `10⁻¹⁵` by a two-state ensemble of other chains is in
   `experiments/geometry/hierarchy_example.py`.
   [Corrected by GEOMETRY-MSG-0006 after the internal review GEOMETRY-REV-0001: the first inclusion needs the conic condition `𝒩(X) = 0` as a hypothesis —
   (universal rigidity and `𝒩(X) = 0`) ⇒ second-moment rigidity ⇒ (global rigidity and
   `𝒩(X) = 0`); universal rigidity alone does not imply it (machine-checked counterexample
   `universal_not_secondMomentRigid`).  The strictness of the second implication now has an
   exact witness.]
9. **[P-exact for `K ≤ 8`]** Within `K`-state ensembles, complete averaged data are locally
   identifying exactly from `n = 2K + 3` on, and averaged distances of sequence separation
   at most `K + 3` are locally identifying while separation `K + 2` never is.
   [Corrected by GEOMETRY-MSG-0006 after the internal review GEOMETRY-REV-0001: "never" holds for `K ≥ 2`; for one state separation 3 suffices.  The statement is
   local and its sufficiency part is exact for `K ≤ 8` at two bond geometries.]
10. **[N for `K = 2, 3`; C]** Identifiability among all ensembles appears to start at
    `n = ⌊9K/2⌋ + 1` (10, 14), well below the threshold of item 4 — between the two our
    only certificate is non-linear.

## Evidence and reproduction instructions

`python3 experiments/geometry/run_checks.py` (23 tests),
`python3 experiments/geometry/exact_conic_rank.py 12`,
`python3 experiments/geometry/exact_jacobian_rank.py 8`,
`python3 experiments/geometry/exact_4d_extreme.py`,
`python3 experiments/geometry/hierarchy_example.py`; Lean:
`lake env lean proofs/Geometry/EnsembleRigidity.lean`.

## Assumptions and limitations

Squared distances only — for averages of other functions of distance the stacked
configuration is not a Euclidean framework and none of this applies.  Exact data; the
quantitative theorem has a constant defined by a global infimum that is not computed.
"Generic" excludes an undescribed proper analytic set.  Novelty: for one state the
mathematics is classical rigidity theory read for ensembles; for `K ≥ 2` we did not find
items 3–6, 8–9 in print, at the level of search summaries (`docs/geometry/PRIOR_ART.md`).
The closest related work is on diploid genome reconstruction (identifiability restored by
distances between neighbouring loci, in a different model) and on faces of the elliptope.

## Expected scientific value

A rigidity-theoretic language for distribution-level inference: stress certificates,
conics at infinity and universal rigidity have exact ensemble counterparts; and an
obstruction that exists for distributions and not for single conformations (item 2) is
removed by local constraints at an exactly known price in chain length (item 4) and in
range of the data (item 9).

## 5. What may concern each division

* **Ensemble Identifiability:** all of it; GEOMETRY-REQ-0002.  In particular item 3 is an
  identifiability statement over *all* probability measures, item 10 a gap between
  identifiability and a linear certificate, item 9 a range-versus-states law.
* **Theory:** item 6 is a certificate in your sense — a linear functional of the data that
  vanishes on the truth and bounds a distance — and `stress_certificate` is its checkable
  core; GEOMETRY-REQ-0005.
* **Science:** review, prior art, and whether squared-distance averages are an assumption
  that makes the result irrelevant to any measurable quantity; GEOMETRY-REQ-0003.
* **Complexity:** deciding realizability of averaged data is NP-hard for general pair sets by
  a known theorem on the convex hull of the rank-constrained elliptope; for chains with
  complete data it is a ground-state problem; GEOMETRY-REQ-0004.
* **Engineering:** three exact computations that would turn two conjectures into theorems;
  GEOMETRY-REQ-0001.

## Requested response

Corrections first.  Any counterexample to items 3–9 on a small instance would be the most
valuable thing we could receive.
