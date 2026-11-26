```
Message ID:                  ENG-RES-0009
Message type:                Response to a computational request (accepted; two items completed, the others not started)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         see the commit that adds this file (checkpoint 3 of the engineering branch)
Priority:                    Medium
Status:                      In progress (items 5 and 6 in part: completed; items 1–4 and the bridge tables of item 6: accepted, not started)
Relevant source commit:      63efc69 (theory head read and audited); implementation: the commit that adds this file
Related theorem or experiment: theory report §11.22 (Proposition 11.74), THY-RES-0002 §§5, 6; docs/workstreams/P_REPORT.md §0 (generic chain); engineering experiments X-002, X-004
Related message/request IDs: THY-REQ-0008 (the request); THY-RES-0002; ENG-RES-0002, ENG-RES-0007 (the data used)
Request being answered:      THY-REQ-0008 (limit shape of profile sets: vertices, walks against bridges, the plateau, off-lattice distance entropy)
```

# THY-REQ-0008: the two items that need only stored data are done — the single-flip bounds hold in all 36 cases, and the off-lattice distance entropy is *not* independent of the chain length at 14 torsions

> **Linked correction (added at checkpoint 4; the text below is as published):** ENG-MSG-0004 §4, item 5 — in §2, "0.014 at `ρ = ¼`" is `0.013`
> (`0.0134`; it had been computed from rounded table entries).  The entropy table contains 305 exact ties that the message does not mention; they are
> decided correctly (SCI-REV-0008, finding M2).

## Decision

**Accepted**, below THY-REQ-0001 and THY-REQ-0003 as you rank it.  Items 5 and 6 (the part
about single-flip constants) needed only tables that already exist and are answered here.
Items 1–4 (optimisation over long conformations, walks against bridges, the plateau by set
cover) need an optimiser over lattice walks with an independent recount from coordinates;
it has not been written.  The class tables of bridges for 25–27 beads (item 6) need the
enumerator restricted to bridges; not started.

## Epistemic status

**[X]** exact enumeration for the lattice numbers of §1; **[X\*]** for the off-lattice numbers
of §2 (exact enumeration, floating-point distances; the tie analysis of ENG-RES-0007 §3
applies).  Nothing here is a theorem.

## 1. Item 6 — single-flip constants against Proposition 11.74 and against the scaling form

Data: the single-flip constants of the lattice chain for 3–16 torsions (ENG-RES-0002 §5,
exhaustive over all pairs differing in one torsion).  With your definition
`d_j = min(j, n + 1 − j)`:

<!-- TABLE:flip_bounds -->
| `n` | `j` with `d_j ≥ 5` | least `c_j − (14 d_j − 15)` | largest `c_j / (70 (d_j + 3))` | bound violated |
|---|---|---|---|---|
| 9 | 1 | 21 | 0.136 | 0 |
| 10 | 2 | 43 | 0.175 | 0 |
| 11 | 3 | 35 | 0.186 | 0 |
| 12 | 4 | 45 | 0.204 | 0 |
| 13 | 5 | 47 | 0.236 | 0 |
| 14 | 6 | 64 | 0.245 | 0 |
| 15 | 7 | 63 | 0.255 | 0 |
| 16 | 8 | 73 | 0.286 | 0 |
| all | 36 | | | **0** |
<!-- /TABLE:flip_bounds -->

`14 d_j − 15 ≤ c_j ≤ 70 (d_j + 3)` holds in every one of the pairs `(n, j)` with `d_j ≥ 5` that
exist up to 16 torsions.  The lower bound is never closer than 21; the measured constants
stay below 0.29 of the upper bound.  (This is a check of the *statement* against exact
data in the range where both exist; it says nothing about the proof.)

The scaling form `c_j ≈ n Φ(d_j / n)` — entries are `c_j / n`, with `d_j / n` in brackets:

<!-- TABLE:flip_scaling -->
| `n` | `d_j = 1` | `d_j = 2` | `d_j = 3` | `d_j = 4` | `d_j = 5` | `d_j = 6` | `d_j = 7` | `d_j = 8` |
|---|---|---|---|---|---|---|---|---|
| 8 | 4.38 (0.12) | 6.25 (0.25) | 7.00 (0.38) | 7.25 (0.50) |  |  |  |  |
| 9 | 4.00 (0.11) | 7.00 (0.22) | 7.67 (0.33) | 8.44 (0.44) | 8.44 (0.56) |  |  |  |
| 10 | 4.00 (0.10) | 6.80 (0.20) | 7.40 (0.30) | 8.10 (0.40) | 9.80 (0.50) |  |  |  |
| 11 | 4.36 (0.09) | 6.64 (0.18) | 7.36 (0.27) | 8.18 (0.36) | 9.45 (0.45) | 9.45 (0.55) |  |  |
| 12 | 4.33 (0.08) | 7.08 (0.17) | 7.67 (0.25) | 9.00 (0.33) | 9.50 (0.42) | 9.50 (0.50) |  |  |
| 13 | 4.08 (0.08) | 6.85 (0.15) | 7.54 (0.23) | 8.69 (0.31) | 10.15 (0.38) | 10.15 (0.46) | 10.00 (0.54) |  |
| 14 | 4.07 (0.07) | 6.57 (0.14) | 7.79 (0.21) | 8.43 (0.29) | 9.79 (0.36) | 11.00 (0.43) | 10.50 (0.50) |  |
| 15 | 3.87 (0.07) | 6.87 (0.13) | 7.93 (0.20) | 9.07 (0.27) | 9.53 (0.33) | 10.67 (0.40) | 10.67 (0.47) | 10.67 (0.53) |
| 16 | 3.62 (0.06) | 6.75 (0.12) | 7.75 (0.19) | 8.81 (0.25) | 10.00 (0.31) | 10.62 (0.38) | 10.56 (0.44) | 10.62 (0.50) |
<!-- /TABLE:flip_scaling -->

Reading.  At fixed `d_j / n` the ratio `c_j / n` is **not** yet a function of `d_j / n` alone: at
the centre of the chain it rises from 7.25 (8 torsions) to 10.6 (16 torsions), while at fixed
small `d_j` the *unnormalised* constant is nearly independent of `n` (the columns `d_j = 1, 2, 3`
divided by `n` fall like `1/n`).  So at these sizes the data are closer to "`c_j` is a function
of `d_j`, with a plateau towards the centre" than to the scaling form; the concave `Φ` of your
conjecture would need the centre values to stop rising, and they have not.  This is a
statement about 8–16 torsions only.

## 2. Item 5 — distance entropy of the off-lattice chain

Model "gen" of `P_REPORT.md` §0 as in ENG-RES-0007 (cutoff 16, hard core 3).  For `n` torsions,
`N = n + 3` beads, and a radius `ρN` in the profile distance, `m_c(ρ)` is the number of profile
classes within that distance of class `c` (itself included) and

    σ(ρ) = n⁻¹ · (mean over classes of ln m_c(ρ)).

`ρ ∈ {¼, ½, 1}` are your three radii for `L = 1`, `ρ ∈ {1.25, 2.5, 5}` those for `L = ⅕`.  (The
median over classes and the mean weighted by the number of conformations are in the result
file; they differ from the column shown by at most 0.05 at every size and by 0.03 at 13 and
14 torsions.)

<!-- TABLE:generic_entropy -->
| `n` | `N` | conformations | classes | `ln(classes)/n` | pairs within the cutoff per bead: mean over classes / over conformations / max | `σ(ρ = 0.25)` | `σ(ρ = 0.5)` | `σ(ρ = 1)` | `σ(ρ = 1.25)` | `σ(ρ = 2.5)` | `σ(ρ = 5)` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 8 | 99 | 30 | 0.680 | 1.62 / 1.63 / 1.88 | 0.009 | 0.087 | 0.313 | 0.354 | 0.560 | 0.661 |
| 6 | 9 | 239 | 60 | 0.682 | 1.88 / 1.86 / 2.33 | 0.019 | 0.091 | 0.314 | 0.385 | 0.567 | 0.661 |
| 7 | 10 | 577 | 136 | 0.702 | 2.08 / 2.05 / 2.80 | 0.034 | 0.119 | 0.358 | 0.433 | 0.591 | 0.675 |
| 8 | 11 | 1 393 | 291 | 0.709 | 2.27 / 2.21 / 3.27 | 0.085 | 0.182 | 0.390 | 0.460 | 0.606 | 0.682 |
| 9 | 12 | 3 363 | 639 | 0.718 | 2.43 / 2.34 / 3.75 | 0.101 | 0.229 | 0.424 | 0.484 | 0.620 | 0.689 |
| 10 | 13 | 8 115 | 1 360 | 0.722 | 2.58 / 2.46 / 4.23 | 0.116 | 0.258 | 0.448 | 0.502 | 0.628 | 0.692 |
| 11 | 14 | 19 559 | 2 908 | 0.725 | 2.72 / 2.56 / 4.71 | 0.130 | 0.279 | 0.465 | 0.518 | 0.635 | 0.696 |
| 12 | 15 | 47 141 | 6 137 | 0.727 | 2.85 / 2.65 / 5.20 | 0.146 | 0.298 | 0.480 | 0.530 | 0.640 | 0.697 |
| 13 | 16 | 113 587 | 13 012 | 0.729 | 2.98 / 2.73 / 5.69 | 0.161 | 0.316 | 0.492 | 0.541 | 0.645 | 0.699 |
| 14 | 17 | 273 623 | 27 421 | 0.730 | 3.10 / 2.80 / 6.18 | 0.175 | 0.329 | 0.503 | 0.549 | 0.649 | 0.701 |
<!-- /TABLE:generic_entropy -->

Three observations.

1. **Replication, one size further than before.**  At 13 torsions the enumerator gives
   113 587 conformations and 13 012 profile classes — the two numbers `P_REPORT.md` publishes
   for that size, which ENG-RES-0007 had left as a target.  14 torsions (273 623 and 27 421) is
   new.
2. **`σ` is not independent of `n` at these sizes.**  At your `L = 1` radii it is still rising at
   14 torsions — by 0.013 per torsion at `ρ = ½` and 0.014 at `ρ = ¼` in the last step, with
   increments that shrink slowly.  At the `L = ⅕` radii it has nearly stopped (`ρ = 2.5`:
   `+0.004` in the last step), because there a ball already contains most classes
   (`σ(5) = 0.701` against `ln(classes)/n = 0.730`).
3. **The number of pairs per bead within the cutoff is 3.1 at 17 beads and rising by 0.12 per
   bead.**  Your heuristic for the plateau (THY-RES-0002 §6) uses a bulk coordination of
   about 63; the chains that can be enumerated are at one twentieth of it.

The test you asked for — growth of the covering number per torsion against growth of the
number of classes divided by `e^σ`, with `σ` taken at the larger of the two sizes:

<!-- TABLE:generic_entropy_growth -->
| `n → n+1` | growth of the number of classes | `L=1, ε=1/4 N`: predicted (classes growth / `e^σ`, `ρ = 0.25`) / measured | `L=1, ε=1/2 N`: predicted (classes growth / `e^σ`, `ρ = 0.5`) / measured | `L=1/5, ε=1/4 N`: predicted (classes growth / `e^σ`, `ρ = 1.25`) / measured | `L=1/5, ε=1/2 N`: predicted (classes growth / `e^σ`, `ρ = 2.5`) / measured |
|---|---|---|---|---|---|
| 5 → 6 | 2.000 | 1.96 / 1.53 | 1.83 / 1.67 | 1.36 / 1.50 | 1.13 / 1.00 |
| 6 → 7 | 2.267 | 2.19 / 1.52 | 2.01 / 1.40 | 1.47 / 1.00 | 1.26 / 1.00 |
| 7 → 8 | 2.140 | 1.96 / 1.34 | 1.78 / 1.62 | 1.35 / 1.33 | 1.17 / 1.50 |
| 8 → 9 | 2.196 | 1.99 / 1.46 | 1.75 / 1.26 | 1.35 / 1.00 | 1.18 / 1.00 |
| 9 → 10 | 2.128 | 1.89 / [1.38, 1.43] | 1.64 / 1.40 | 1.29 / 1.25 | 1.14 / 1.00 |
| 10 → 11 | 2.138 | 1.88 / [1.37, 1.50] | 1.62 / [1.42, 1.50] | 1.27 / 1.20 | 1.13 / 1.33 |
| 11 → 12 | 2.110 | 1.82 / [1.40, 1.69] | 1.57 / [1.21, 1.60] | 1.24 / 1.00 | 1.11 / 1.00 |
| 12 → 13 | 2.120 | 1.80 / — | 1.55 / — | 1.23 / — | 1.11 / — |
| 13 → 14 | 2.107 | 1.77 / — | 1.52 / — | 1.22 / — | 1.10 / — |
<!-- /TABLE:generic_entropy_growth -->

("Measured" is the ratio of consecutive covering numbers of ENG-RES-0007; an interval where
one of the two is a bracket.  No covering numbers exist yet beyond 12 torsions.)

Reading.  At `L = 1` the prediction exceeds every measured ratio that is known exactly (for
`ε = N/2`: 1.64 against 1.40 at `9 → 10`, 1.75 against 1.26 at `8 → 9`) and lies above or inside
the brackets elsewhere; it falls towards the measured values as `n` grows, because `σ` is
still rising.  So the relation is not an identity at these sizes, but it is not
contradicted either — with a growth of 1.38–1.43 per torsion and 2.11 for the classes it
would hold in the limit if `σ(½)` settled near 0.39–0.42, which the present increments
neither establish nor exclude.  Your inferred `σ ≈ 0.39` at `L = 1` is therefore a statement about a limit that the
enumerable sizes have not reached; the value measured at 14 torsions is 0.33.  At `L = ⅕` the
measured ratios are ratios of integers below 10 and carry no information; your inferred
`σ ≈ 0.6` there compares with a measured 0.65 (`ρ = 2.5`) that has nearly converged.
In your own words for the two outcomes: *the growth rate is still transient at 12–14
torsions* for `L = 1`, and `σ` *does* extrapolate for `L = ⅕`.

## What was not done

* Items 1–4 and the bridge tables: not started.
* No covering numbers of the off-lattice chain beyond 12 torsions (the class tables for 13
  and 14 now exist; the covers need the primal heuristic with the certified dual bound
  described in the research log).
* `σ` was computed with the mean of `ln m_c`; no attempt was made to decide which notion of
  "typical class" the heuristic needs.

## Execution environment, resources, reproduction

Local machine, single core: 5–12 torsions 25 s, 13 torsions 73 s, 14 torsions 334 s.  No
remote compute.

```
python experiments/eng/chain_cover/generic_entropy.py --nmin 5 --nmax 14      # results/generic_Sc16_entropy.json
python experiments/eng/chain_cover/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0009.md
```

## Assumptions and limitations

The off-lattice chain is enumerated in floating point (classes are formed after rounding
squared distances to eight decimals).  Synthetic chains with a made-up energy; nothing here
concerns a physical system.

## Recommended theoretical follow-up

If the growth rate of off-lattice certificates is to be predicted from the distance
entropy, the prediction needs the dependence of `σ` on `n` — a finite-size form — not a
constant: with `σ` taken at the size itself the growth at `L = 1` is over-predicted by 10–50 %
wherever it can be checked against an exact value.
