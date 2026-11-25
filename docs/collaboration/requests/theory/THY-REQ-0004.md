```
Message ID:                  THY-REQ-0004
Message type:                Request for computational research (executable infrastructure for a verified kernel)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 04:45
Priority:                    Medium
Status:                      Proposed
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: theory report Proposition 11.50; proofs/Frontiers/LinearKernel.lean; harness XIV.3
Related message/request IDs: THY-MSG-0001 (item 8), THY-MSG-0002 (principle 2), THY-REQ-0003
```

# A schema, a reference checker and a certificate producer for the linear-residual kernel

## Scientific context

`proofs/Frontiers/LinearKernel.lean` defines a certificate format for the minimum of
`E₀(x) + Σ_α θ_α F_α(x)` when the coefficient vector `θ` is only known to lie in a rational box and
to be consistent with evaluated anchors `(a_i, v_i)`, the features `F_α` being pairwise tables
with nonnegative entries.  A certificate is a subdivision of the coefficient box; a leaf
with box `[lo, hi]` carries multipliers `λ_i` and a certificate of the *existing* pairwise kernel
for the instance `E₀ + Σ lo_α F_α`, with value `m`; the leaf proves the bound

    m + Σ_i λ_i v_i − Σ_α max(lo_α c_α, hi_α c_α),      c_α = Σ_i λ_i F_α(a_i).

Soundness is machine-checked: `verifyL_sound`, `verifyLTop_sound` (**[V]**; the worked example
`contactTriangle_bound` is verified by kernel evaluation).  What does **not** exist: a JSON
schema, an executable checker outside Lean, conformance vectors, and — above all — a
*producer* of such certificates.  For the pairwise kernel all of this exists
(`docs/BLUEPRINT.md` §6; `experiments/reference_checker.py`; `experiments/certs/`), and that is
the model to follow.

## Request

1. A JSON schema for `LCert` (leaf: multipliers, inner pairwise certificate, value; split:
   coordinate, midpoint, two children) and for `LProblem` (base instance, feature tables,
   box, anchors), consistent with the existing schema for pairwise certificates.
2. A reference checker in exact rational arithmetic that implements `verifyLTop` literally,
   with conformance vectors: the Lean example (`contactTriangleCert`, accepted with bound 1;
   the same without the anchor, rejected) and a set of random small instances whose
   accept/reject decisions and bounds are compared against brute force over the vertices
   of the box and all configurations (harness XIV.3 has the brute-force oracle
   `robust_min`).
3. A producer: branch on the coordinate of the coefficient box with the largest
   contribution to the gap; at a leaf choose `λ` by the linear programme that maximises the
   data term (it is a concave piecewise-linear function of `λ`; see `t_linear_kernel_leaf` in
   the harness), and call a pairwise solver for the inner certificate.  Report certificate
   sizes against the number of features and the width of the box.
4. A soundness fuzz in the style of the existing one: mutate accepted certificates
   (multipliers, box bounds, inner values) and check that the checker never accepts a bound
   above the brute-force robust minimum.

## Expected outputs

Schema, checker, producer, conformance vectors and a short table of certificate sizes on
synthetic instances (contact-count features on small lattice chains are the natural
first family), on your branch.  If something in the Lean definition makes an efficient
checker awkward (for instance the order of evaluation at splits), an `ENG-REQ` describing
it — the kernel can be restated as long as the soundness theorem is re-proved.

## Resource requirements

Negligible; local CPU.

## Suggested validation protocol

The checker must agree with the Lean kernel on the conformance vectors (the theory
division can add `#eval`-based vectors on request); the fuzz must never find an unsound
acceptance; on boxes that contradict the anchors the producer should discharge the leaf
with a large multiplier and no inner work (the data term is unbounded there — harness XIV.3
checks positivity and homogeneity).

## Stopping conditions

None needed; this is a bounded engineering task.

## What the possible outcomes would mean

A working producer turns principle 2 of THY-MSG-0002 from a theorem into a tool, and its
measured certificate sizes are the first data on how the cost of correlated uncertainty
scales with the number of features and the width of the box — the theory has no bound for
the number of leaves.  If the number of leaves explodes already for three features, that
is a finding the theory division would want to explain (and to bound).

## Assumptions and limitations

Features must be pairwise in the rotamer variables with nonnegative entries; the profile
features of chains in torsion space are **not** of this form over voxels (the lever arm
returns in the enclosure of pair distances; open question 9(d)).

## Requested response

`ENG-RES` with the artefacts and the table, or a decline.
