## 3. Numerical tests (replication with my own code), with their controls

All code is mine and was written before I opened any script of the reviewed branch
(`experiments/science/ws_R21/`: `r21_common.py`, `t1`–`t7`, `t2b`, `t4b`).  Plane (`d = 2`), conformer
coordinates i.i.d. standard normal (fixed seeds; mean squared edge length = 4), float64.  Every log cited reached
its last line (`DONE …`); stopped or failed runs are in `not_cited/` (one: a follow-up script that crashed on a
coding error).  Two independent methods decide whether a vector of squared lengths is realisable:
**LM** — batched Levenberg–Marquardt on `‖F(p) − q‖₂` from random starts (the method prescribed by the brief; a
local search, it can miss); **EXACT** — ruler-and-compass enumeration of all `2^{N−3}` realisations of a spanning
subgraph built by adding vertices of degree two, then comparison of the remaining edges (exhaustive; validated on
2 000 planted realisable vectors per graph: all found, largest defect `9·10⁻¹²`).

**T1 — the graphs** (`logs/t1_graphs_run1.log`; 0 violations of 3 consistency checks × 14 graphs).  Rank, redundant
rigidity, vertex connectivity, stress-matrix rank at three random points, and all separators of the rigidity
matroid by brute force over the bipartitions of the edge set.

| graph | N | \|E\| | globally rigid (stress rank `N−3`; 3-connected and redundantly rigid) | separators | matroid |
|---|---|---|---|---|---|
| `K_4`, `K_5`, `K_5 − e`, wheel `W_5`, `K_6`, wheel `W_6`, `K_{3,3} + e` | 4–6 | 6–15 | yes | 0 | connected |
| triangle, `K_4 − e`, `K_4` + vertex of degree 2, `K_{3,3}`, prism | 3–6 | 3–9 | no | 3–255 | not connected |
| two `K_4` glued along an edge; the same without that edge | 6 | 11; 10 | **no** (connectivity 2) | **0** | **connected** |

**T2 — chimera search on globally rigid graphs** (`logs/t2_<graph>_K<K>_run1.log`).  Every non-constant colouring
of the edges by the conformers, for random ensembles.  "Found" was defined before the runs as LM residual
`< 10⁻⁶` or EXACT defect `< 10⁻⁹`.

| graph | K | ensembles | colourings examined | smallest LM residual | smallest EXACT defect | found | control violations |
|---|---|---|---|---|---|---|---|
| `W_5` | 2 | 10 | 2 540 | 3.5e-4 | 2.3e-3 | 0 | 0 |
| `K_5 − e` | 2 | 10 | 5 100 | 2.4e-3 | 5.3e-3 | 0 | 0 |
| `K_5` | 2 | 10 | 10 220 | 6.3e-3 | 1.5e-2 | 0 | 0 |
| `W_6` | 2 | 10 | 10 220 | 4.4e-6 | 1.5e-4 | 0 | 6 (LM) |
| `K_{3,3} + e` | 2 | 10 | 10 220 | 1.0e-5 | 5.2e-5 | 0 | 8 (LM) |
| `K_6` | 2 | 3 | 98 298 (LM on 11 614 of them) | 3.6e-2 | 8.0e-2 | 0 | 0 |
| `W_5` | 3 | 3 | 19 674 | 3.4e-5 | 1.4e-4 | 0 | 2 (LM) |
| `K_5 − e` | 3 | 2 | 39 360 | 1.3e-4 | 1.2e-4 | 0 | 0 |
| `K_5` | 3 | 2 | 118 092 | 1.3e-2 | 1.3e-2 | 0 | 0 |
| `W_6` | 3 | 2 | 118 092 | **7.9e-7** | 2.3e-6 | **1 (LM threshold)** | 30 (LM) |
| `K_{3,3} + e` | 3 | 2 | 118 092 | 5.3e-6 | 1.8e-5 | 0 | 18 (LM) |

549 908 colourings in 64 ensembles.  **EXACT: no chimera; none of its controls violated** (the conformers and 200
planted realisable vectors per ensemble, all found).  **LM: one colouring below the pre-set threshold** (`W_6`,
`K = 3`, ensemble 0, colouring `2211222020`, residual `7.9·10⁻⁷`; EXACT defect of the same colouring `2.3·10⁻⁶`).
Follow-up (`t2b_w6_followup.py`, `logs/t2b_w6_followup_run1.log`): the same ensemble reproduced; the residual is
`7.9229962·10⁻⁷` after 120, 1 000 and 5 000 iterations from 400 starts each (about 100 starts reach that same
value), gradient norm `10⁻¹⁴`, smallest singular value of the Jacobian `0.28`, unchanged by 60 Gauss–Newton steps,
while the three conformers reach `10⁻¹⁶` under the same procedure.  It is a converged *positive* minimum — a
framework whose ten squared lengths are within `8·10⁻⁷` of lengths of the three conformers, not all of the same
one — i.e. no chimera, and a measure of how thin the margin is.  The threshold `10⁻⁶` was too loose for this
graph (realisable targets end below `10⁻⁹`); I did not relabel the log.
*Controls of the LM search:* 64 violations, all of them misses of things that exist — planted realisable vectors
not found by any start (63) and, once, a conformer itself (`W_6`, `K = 3`, 10 starts).  Per-start success of LM on
planted realisable vectors: `0.995`–`1.00` on `K_5`, `K_6`; `0.83`–`0.88` on `K_5 − e`; `0.61`–`0.68` on `W_5`;
`0.45`–`0.50` on `K_{3,3} + e`; `0.31`–`0.37` on `W_6`.  So on the sparse graphs **the
LM search alone is not evidence of absence** (it misses 1–7 % of realisable vectors at the numbers of starts
used); the verdict of T2 rests on EXACT, with LM as the second method.

**T3 — controls that must find a chimera** (`logs/t3_controls_run1.log`; 1 violation of a prediction in total).
(a) `K_4` + vertex of degree two (rigid, not globally rigid, matroid not connected), 40 generic pairs × 254
colourings: a closed-form criterion coded separately (the splice is constant on the `K_4` block and the two
pendant radii satisfy the triangle inequality with the base edge) predicts 160 chimeras, at least one in 40 of 40
pairs; LM found 160, EXACT 160, neither found anything not predicted.
(b) Example D2, 20 pairs: 320 predicted chimera colourings; EXACT 320, LM 319 (one miss, 12 starts); the two
ensembles have identical per-edge multisets (difference `0.0`) and the chimeras are not congruent to the
conformers (smallest difference of the full distance vectors `0.22`).  The same conformers on `K_5`: 0 chimeras.
(c) Two `K_4` glued along an edge, with and without that edge (not globally rigid, connected matroid), 10 generic
pairs × 2 046 / 1 022 colourings: 0 chimeras (smallest LM residual `4·10⁻⁴` / `7·10⁻⁶`), while the flip of one
`K_4` changes no measured squared length (`10⁻¹⁴`) and an unmeasured one by at least `0.70`: the ensemble is not
determined, at `K = 1`, without any chimera (m9).
(d) Example D1 in exact rational arithmetic (the four frameworks, the equality of the per-edge multisets, no
common length); the search on `(x_1, x_2)` finds exactly the two complementary colourings `011111`, `100000`
among 62 (smallest residual of the other 60: `0.094`); 20 random members of the family: both chimeras found by
both methods and nothing else in 20 of 20.

**T4 — Corollary E8 in numbers** (`logs/t4_{K4,W5}_K{1,2,3}_run1.log`; three random instances each, random
weights; statistics extracted by `summarize_t4.py`, `logs/summarize_t4_run1.log`).  (1) The mean of `f` under `μ`
is at most `1.8·10⁻²⁴` evaluated on the conformers and at most `6.7·10⁻⁸` in absolute value evaluated from the
moments, with a cancellation `C_abs = Σ|c_{e,j}| m_{e,j}` of `1.3·10²`–`1.8·10³` (`K = 1`), `7.8·10³`–`1.6·10⁵`
(`K = 2`), `8.6·10⁵`–`7.1·10⁸` (`K = 3`): **an error `ε` of the moments is an error `ε·C_abs` of the mean of the
certificate.**  (2) Perturbed ensembles: other weights — mean of `f` unchanged (at most `1.1·10⁻²⁴`) although a
moment changes by a relative amount of up to `5.4`; every conformer displaced by `δ` — mean of `f` `∝ δ^p` with
fitted `p` between `1.994` and `2.004`; one conformer split in two at `±s` — largest relative change of a moment
`∝ s^p`, `p` between `2.00` and `2.02`, so moments within `ε` cannot exclude a spread `s ≈ (0.05…1.5)·√ε` of a
conformer.
(3) Zeros of `f` by LM from 6 000 starts: no zero that is not a conformer in any of the 18 instances — but the
control of this check (every conformer must be reached) **fails in 4 of the 18** (`K_4`, `K = 3`, instance 1:
conformers reached `[41, 0, 597]` times; all three `W_5`, `K = 3` instances, where only 9–17 runs reach any zero
and one conformer is never reached).  In those four the check says nothing; it supports E8 in the other 14.
(4) What error of the moments is tolerated.  `D(p)` = distance of the vector of all squared pair distances of `p`
to the nearest conformer's; "far" = `D ≥ 1` (about 10 % of the norm of that vector).  *Guarantee* (Markov with
their certificate): `ν(far) ≤ ε·C_abs/γ*`, `γ*` the least value of `f` on the far set (near-chimeras; found by LM
and a constrained search).  *Adversary*: a linear programme over an explicit finite candidate set gives an
ensemble with all `2K|E|` moments within relative `ε` of those of `μ` and as much mass as possible far away (287
programmes solved, achieved error `≤ 1.05ε` in all; 1 programme failed and is not used).  Far mass of the
adversary at `ε = 10⁻³ / 10⁻⁴ / 10⁻⁵` (three instances), and the `ε` the certificate needs to keep it below 10 %:

| graph | K | adversary: far mass at `ε = 10⁻³ / 10⁻⁴ / 10⁻⁵` | certificate guarantees `≤ 10 %` far mass only if `ε ≤` |
|---|---|---|---|
| `K_4` | 1 | .37/.042/.0043  .77/.081/.0083  .073/.0075/.00075 | 1.0e-4 … 7.6e-4 |
| `K_4` | 2 | .28/.038/.0043  .92/.15/.017  .18/.021/.0022 | 3.5e-9 … 4.6e-8 |
| `K_4` | 3 | .59/.15/.027  1/1/.76  1/.58/.30 | 1.8e-19 … 1.1e-12 |
| `W_5` | 1 | .24/.028/.0030  1/.11/.013  .11/.012/.0012 | 3.1e-7 … 9.4e-5 |
| `W_5` | 2 | .81/.28/.14  1/.83/.24  1/1/.62 | 2.0e-12 … 8.0e-11 |
| `W_5` | 3 | 1/.97/.57  .91/.51/.14  1/.78/.28 | 5.6e-18 … 2.7e-15 |

Reading.  For one conformation on `K_4` the two sides agree within a factor two: a relative accuracy `10⁻⁴` of
the two moments per edge keeps all but 1–10 % of the ensemble near `x`.  From `K = 2` on the adversary
needs no near-chimera to be exact: with moments accurate to `10⁻⁵` (relative; moments up to `E ℓ⁸` for `K = 2`,
`E ℓ¹²` for `K = 3`) an explicit ensemble still has 0.2–2 % (`K_4`, `K = 2`), 3–76 % (`K_4`, `K = 3`), 14–62 %
(`W_5`, `K = 2, 3`) of its mass far from every conformer.  The adversary's numbers are lower bounds of the worst
case (finite candidate set; with a second, three times larger random candidate set they changed by a factor
between 0.93 and 2.6, median 1.03, over 143 pairs of programmes); the certificate's are upper bounds; the truth is between, and the gap between the two is itself a finding: **their
certificate is a very weak witness of stability.**  Even `K = 1` can be fragile on a minimally globally rigid
graph: in `W_5` instance 0 a visibly different framework (`D = 0.63`) has all eight squared lengths within
`7.7·10⁻⁵` of those of `x` (`t4b_w5_followup.py`, `logs/t4b_w5_followup_run2.log`: a converged positive minimum,
same value after 300 and 3 000 iterations, gradient `4·10⁻¹⁴`) — a *near-flip*, the one-conformer analogue of a
near-chimera.

**T5 — how close do random ensembles come to a chimera?** (`logs/t5_<graph>_K<K>_run1.log`; table extracted by
`summarize_t5.py` into `logs/summarize_t5_run1.log`.)  *Chimera gap* `g_1` = least distance (2-norm, squared-length
units; mean squared edge length = 4) from a non-constant splice to the set of realisable vectors, computed by
LM; every value is realised by an explicit framework (re-checked in the log), so each is an upper bound of the
true gap; with more than 2 000 colourings LM is run on the 1 000 colourings of smallest EXACT defect and 1 000
random ones.  *Switching gap* `g_2` (`K = 2`): least over colourings of the larger of the distances of a
colouring and of its complement.  `c` = codimension of the measurement variety.

| graph | \|E\| | c | K | splices | ensembles | `g_1` median | `g_1` smallest | sup-norm gap / mean squared length (median) | `g_2` median | heuristic `splices^{−1/c}` |
|---|---|---|---|---|---|---|---|---|---|---|
| `K_4` | 6 | 1 | 2 | 62 | 8 | 3.2e-2 | 1.9e-2 | 4.7e-3 | 0.22 | 1.6e-2 |
| `K_4` | 6 | 1 | 3 | 726 | 8 | 2.3e-3 | 2.2e-4 | 5.1e-4 | | 1.4e-3 |
| `K_4` | 6 | 1 | 4 | 4 092 | 8 | 2.8e-4 | 3.5e-5 | 3.9e-5 | | 2.4e-4 |
| `K_4` | 6 | 1 | 5 | 15 620 | 8 | 8.1e-5 | 8.1e-6 | 1.5e-5 | | 6.4e-5 |
| `K_4` | 6 | 1 | 6 | 46 650 | 8 | 1.7e-5 | 4.3e-6 | 4.5e-6 | | 2.1e-5 |
| `W_5` | 8 | 1 | 2 | 254 | 8 | 1.1e-3 | 2.0e-5 | 4.0e-4 | 0.025 | 3.9e-3 |
| `W_5` | 8 | 1 | 3 | 6 558 | 8 | 2.4e-5 | 1.0e-6 | 6.0e-6 | | 1.5e-4 |
| `W_5` | 8 | 1 | 4 | 65 532 | 8 | 6.8e-6 | 4.8e-8 | 1.2e-6 | | 1.5e-5 |
| `W_6` | 10 | 1 | 2 | 1 022 | 6 | 8.3e-4 | 1.3e-4 | 1.4e-4 | 0.044 | 9.8e-4 |
| `W_6` | 10 | 1 | 3 | 59 046 | 6 | 6.8e-6 | **1.2e-9** | 1.6e-6 | | 1.7e-5 |
| `K_5 − e` | 9 | 2 | 2 | 510 | 8 | 3.7e-2 | 2.7e-4 | 6.0e-3 | 0.24 | 4.4e-2 |
| `K_5 − e` | 9 | 2 | 3 | 19 680 | 8 | 3.2e-3 | 8.1e-4 | 8.7e-4 | | 7.1e-3 |
| `K_5 − e` | 9 | 2 | 4 | 262 140 | 8 | 1.4e-3 | 3.2e-5 | 1.8e-4 | | 2.0e-3 |
| `K_5` | 10 | 3 | 2 | 1 022 | 8 | 8.3e-2 | 2.3e-2 | 1.1e-2 | 0.23 | 9.9e-2 |
| `K_5` | 10 | 3 | 3 | 59 046 | 8 | 1.2e-2 | 3.1e-4 | 2.3e-3 | | 2.6e-2 |
| `K_5` | 10 | 3 | 4 | 1 048 572 | 8 | 1.0e-2 | 6.4e-4 | 1.5e-3 | | 9.8e-3 |
| `K_6` | 15 | 6 | 2 | 32 766 | 6 | 0.11 | 7.4e-2 | 2.4e-2 | | 0.18 |
| `K_6` | 15 | 6 | 3 | 14 348 904 (2·10⁶ sampled) | 6 | 0.17 | 7.8e-3 | 2.1e-2 | | 6.4e-2 |

The heuristic agrees with the medians within a factor of about 6 over four orders of magnitude **[N]**.  On the
minimally globally rigid graphs (`c = 1`) the median gap of two conformers is `8·10⁻⁴`–`3·10⁻²`, of three
`7·10⁻⁶`–`2·10⁻³`, and it loses roughly one order of magnitude per further conformer; redundancy is what buys a margin (`K_6`: a
few per cent of a squared length).  *One value was examined before use:* `W_6`, `K = 3`, ensemble 2:
`g_1 = 1.19·10⁻⁹`.  Follow-up `t5b_w6_followup.py` (`logs/t5b_w6_followup_run1.log`; the random stream is replayed
exactly): three independent checks agree that it is positive — LM gives `1.1901008·10⁻⁹` after 1 000 and 10 000
iterations from the minimiser and from 126–127 of 400 random starts (gradient `2·10⁻¹⁴`, Jacobian singular values
`0.58`–`8.5`); EXACT gives a check-edge deviation `+5.39·10⁻⁷` for the nearest of the 16 flip patterns; and in
40-digit arithmetic the stationary point of `‖F − q‖²` lies `2.9·10⁻¹⁵` from the float minimiser with residual
`1.19010123465522·10⁻⁹`.  A chimera to nine digits, not a chimera; the reason is a nearly degenerate conformer
(three of its points almost collinear, triangle area `1.1·10⁻³`), which makes the angle at the hub about `10³`
times more sensitive to the lengths.

**T6 — E1.3 and its reading** (`logs/t6_e13_reading_run2.log`; `logs/t6d_chains_<n>bonds_run1.log`; run 1 of the
first script exceeded its time estimate and was stopped — `not_cited/`).  (a) E1.3(b) replicated (`N = 5`, two
conformers, all ten pairs): the mean squared lengths under the law of `R·p`, `R² ∈ {0, 2}`, agree with those of
`μ` to `5·10⁻¹⁵`, `P(Q = 0)` is `0` and `0.5`; the affine mechanism (`A_1`, `A_2` with `tA_1A_1ᵀ + (1−t)A_2A_2ᵀ = I`)
gives equality to `2·10⁻¹⁵` with conformers not congruent to those of `μ`.  (b) `⟨r⁻⁶⟩` of all pairs is preserved
(to `9·10⁻¹⁶`) by a scaling with `R⁻⁶ ∈ {0.5, 1.5}`.  (c) Proposition A on planar chains with unit bonds, all pairs
measured, 20 random conformations × 400 minimisations of `‖P^⊥ b(p)‖²` over the chain space each: with 3, 4 and 6
bonds, 8 000 of 8 000 minimisations end in a zero congruent to `x` and none elsewhere; `‖P^⊥ b(p)‖²` is an affine
function of the squared pair distances on the chain space to `10⁻¹⁴`; with 2 bonds the function vanishes
identically (8 000 non-congruent zeros — not determined); for a conformation with two parallel bonds the explicit
two-point mixture of part (ii) has the bond lengths of the chain to `7·10⁻¹⁶` and the mean squared distances of
`x` to `3·10⁻¹⁵`, with a conformer that differs from `x` by `1.33` in a squared distance.  (d) Two generic chain
conformers (12 random pairs per bond count, weights 0.4/0.6, 2 000 LM starts on the bond-length equations of
`x_1A_1 + x_2A_2`; control: `x_1` and `x_2` themselves are reached — in 12 of 12 pairs from 7 bonds on):

| bonds | quadrics through the bond vectors | chains `x_1A_1 + x_2A_2` other than `x_1, x_2` | largest mass an ensemble with the same mean squared distances puts off `{x_1, x_2}` |
|---|---|---|---|
| 4, 5, 6 | 6, 5, 4 | a continuum (600 kept) in 12/12 | **1.000 in 12/12 — not determined** |
| 7 | 3 | 2 (median), up to 4, in 11/12 | 0 in 12/12 (the solutions are affinely independent) — determined |
| 8 | 2 | none in 12/12 | 0 — determined |
| 9, 10, 12 | 1 | none in 12/12 | 0 — determined |

For at least nine bonds this is a proof given the rank that the script computes: the quadratic forms vanishing
on the vectors `c_u = (b_u(x_1), b_u(x_2)) ∈ ℝ⁴` are then the multiples of `diag(I, −I)`, so the only positive
semidefinite solutions of rank at most two of `c_u S c_uᵀ = 1` are `diag(I, 0)` and `diag(0, I)` **[P given N]**.
In general one expects that a chain of `n_b` bonds in `ℝ^d` resolves of the order of `√(2n_b)/d` generic
conformers from mean squared distances **[H]** — the `d`-dimensional analogue of the capacity question of their
Part III.

**T7 — Proposition C** (`logs/t7_fewer_means_run1.log`; 0 violations).  `K_4` and `K_5` in the plane, 10 random
frameworks each: the stress matrix built from the affine dependencies is positive semidefinite of rank `N − 3`
in 10 of 10, in equilibrium to `10⁻¹⁵`, and `tr(pᵀΩp) = Σ_e ω_e ℓ_e(p)²` to `10⁻¹⁴`; of 20 000 minimisations of
`f = tr(pᵀΩp) + Σ_{E_2}(ℓ_e² − ℓ_e(x)²)²` all end in a zero congruent to `x`, none elsewhere; with only two edges in
`E_2` (directions on a conic) all 20 000 zeros are non-congruent affine images.  So 9 means instead of 12 for
`K_4`, 13 instead of 20 for `K_5`.

*How to re-run everything:* `cd experiments/science/ws_R21; export OMP_NUM_THREADS=1;` then `python3 -B
t1_graphs.py`, `./run_t2_A.sh`, `./run_t2_B.sh`, `python3 -B t3_controls.py`, `./run_t4.sh`, `./run_t5_C.sh`,
`./run_t5_D.sh`, `./run_t7_t6.sh`, `python3 -B t2b_w6_followup.py`, `python3 -B t4b_w5_followup.py`,
`python3 -B t5b_w6_followup.py`, `python3 -B summarize_t4.py`, `python3 -B summarize_t5.py` (about 75 minutes of
CPU in total, at most two processes, below 0.5 GB each).
