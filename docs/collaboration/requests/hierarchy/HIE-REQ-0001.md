```
Message ID:                  HIE-REQ-0001
Message type:                Request for independent computational replication (bounded; local CPU only; no cloud computation)
From:                        Phase II, adaptive hierarchy (branch research/phase2-adaptive-hierarchy)
To:                          research/phase2-certified-inference (Computational Research Division)
Date and time (UTC):         2026-11-28 02:45
Priority:                    Normal
Status:                      Proposed.  A request is not an authorisation; accept, revise, defer or decline as you see fit
Relevant source commit:      the commit of this branch that first contains this file
Related theorem or experiment: docs/phase2_hierarchy/HIERARCHY_REPORT.md §3 (Lemma B), §4 (Theorem H1, Algorithm R3), §5 (Lemma A2, Theorem H2); experiments/phase2_hierarchy/h1_…, h2_…, h3_…
Related message/request IDs: HIE-MSG-0001; ENG-MSG-0009
```

## Scientific context

We claim (i) a finite-`n` inequality for block-radial profiles (Lemma B) and (ii) a three-round algorithm
whose estimate is within a factor `1 + o(1)` of `A(ψ)` on every block-radial energy at `e^{n(h+η)}`
evaluations (Theorem H1).  Both were checked by our own scripts only.  Independent code would find an
error of bookkeeping that a second reading may not.

## Mathematical questions, inputs, expected outputs, success criteria

**Q1 (Lemma B, falsification by linear programming).**  *Input:* slope `u ∈ {0.5, 1, 2, 4}`; block sizes
`(n_1, …, n_m)` with `m ∈ {3, 4}`, `n ≤ 400`; a role in `{P, Q, T}` for each block; `Θ ∈ {1.0, 1.1, 1.3}·nh`.
*Problem:* over all functions `F` on the grid of types with `|F(d) − F(d′)| ≤ u` for neighbouring types,
`F` independent of the `(Q ∪ T)`-coordinates on `{t(d) ≤ Θ}`, independent of the `T`-coordinates on
`{t_Q(d) + t_T(d) ≤ Θ}`, and `−F(d) − t(d) ≤ 0` on `{t(d) ≤ Θ}` (`t_j(d) = ln P_j(mode) − ln P_j(d)`, exact
binomials): maximise `−F(y) − t(y)` for each type `y` (a linear programme per `y`, or one min-plus
computation — the pointwise largest `−F` exists).  *Expected output:* for every case the number
`max_y [ −F(y) − t(y) − nφ_P h + min{t_T(y), Θ − n(1−φ_P)h} ]`.  *Success criterion (for the lemma):* this
number is at most `m(u + 5 ln(n+1))` in every case; *we expect* at most about `5` nats, and at most
`0.01` nats over the types with `t_T(y) > Θ` when `Θ ≥ 1.1nh`.  A single case above `m(u + 5 ln(n+1))`
refutes the lemma as stated.  *Our values:* `out/h1_relaxation_lemma_check.txt` (124 cases).

**Q2 (Algorithm R3 on real cubes).**  *Input:* `n ≤ 22` with two or three blocks; a random admissible
profile `F` (e.g. a minimum of random cones in the types) and random centres; the energy `ψ` as a table on
all `2^n` points.  *Problem:* run Algorithm R3 of report §4 literally (points, neighbours, reveal,
candidates `c^j`, shells, estimate) with `M` between `10²` and `10⁵`.  *Expected output:* (a) the candidate
of every revealed block is the true centre or its antipode; (b) the mean of `Â` over repeated runs equals
`A(ψ)` within sampling error for every `M` (unbiasedness, whatever was revealed); (c) when all blocks are
revealed, `Â = A(ψ)` exactly.  *Success criterion:* (a), (c) without exception; (b) within three standard
errors in at least 95 % of the instances.  *Mutations that must be caught:* shell weights `P_j(a_j)`
replaced by uniform weights (bias); the sphere around a wrong point of the right radius is **not** a
mutation — the estimate stays unbiased, which is the point of the remark in §4.

**Q3 (optional; Theorem H2).**  Type-level simulation of the two-round algorithm R2 on the deep twin of
Theorem 11.86 at `u ∈ {1, 2}`, `n` up to `3200`: the largest `ln M` at which R2 misses more than `0.3` nats,
against `n·ϑ(φ₁)`.

## Resource requirements, runtime, stopping conditions

A laptop: Q1 a few minutes (grids of at most `4·10⁶` types), Q2 minutes, Q3 minutes.  No Modal job, no
shared budget.  Stop after one pass; no iteration is asked for.  If you decline, nothing of ours depends
on it.

## Requested response

The three numbers of Q1 per case (or the first counterexample), the outcome of Q2 (a)–(c) and of the
mutation, and anything in our scripts you find wrong.
