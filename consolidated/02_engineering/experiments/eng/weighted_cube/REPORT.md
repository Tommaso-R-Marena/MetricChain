# R10-E1 — exact vertex enumeration of the weighted cubes `(u, …, u, u*)` and the block bounds of the Markov recursion for `L = 3, 4, 5`

> **How this was made, and what the coordinator checked.**  Experiment X-013 of the
> Computational Research Division; request R10-E1 of the Scientific Discovery Division
> (SCI-REV-0010 §7), serving the theory division's workstream Y.  The computation, the code
> and the body of this report are by an independent subagent of this division, working
> from the mathematical definitions; other divisions' files were read as text and never
> executed.  Before filing, the coordinator re-ran the tests; counted the vertices for
> `L = 3` with an own brute-force enumeration over all 346 104 choices of seven tight
> constraints (96 for `u*/u = 3/2`, 72 for `u*/u = 3`: as below); and read §0, §§1.1–1.3,
> §4.1 and the head of §6 — not the rest.  Disclosures
> of the subagent: three exploratory size probes for `L = 5` ran with a vertex cap above
> the request's `10⁷` before the rule was applied in the drivers (their outcome is given as
> information only; every stored result respects the rule); `pplpy 0.9.0` (with `gmpy2`,
> `cysignals`) was installed into the research environment.


*Engineering sub-task, 2026-11-26.  Request: R10-E1 of the science division (SCI-REV-0010 §7, commit `2b4ccdf`),
serving its request R10-T2.  Code: `src/metricchain_eng/weighted_cube/`; drivers and results:
`experiments/eng/weighted_cube/`; tests: `tests/eng/test_weighted_cube.py`.  Every table between `BEGIN`/`END`
markers is generated from `results/*.json` by `make_tables.py`.*

**Vocabulary of status.**  **exact** = integer or rational arithmetic (vertex lists, walls, counts).
**certified** = an enclosure in interval arithmetic (`mpmath.iv`, 30 digits), of two kinds: *iv-all* (every vertex
is evaluated in interval arithmetic) and *screened* (a floating-point scan of all vertices, every vertex within
`10⁻⁷` of the maximum re-evaluated in interval arithmetic; rests in addition on the rounding analysis of §4.3,
which is an analysis and not a machine check).  **numerical** = floating point without enclosure.  **quoted** =
taken from another division's files, not recomputed.  **indication** = numerical evidence for an unproved
statement.  All bounds on `a_∞`, `h_∞` rest on Proposition F of the theory division's workstream Y (§1.4), an input.

## 0. Summary

1. **The combinatorial type of the polytope depends on the ratio `r = u*/u`** (irrational in general) and is
   constant on *chambers* of `r` with rational walls.  Every enumeration is done at one rational ratio per chamber
   in integer arithmetic and is valid for every real ratio of its chamber (§2).  Walls: `L = 3`: `2`;
   `L = 4`: `3/2, 2, 3`; `L = 5`: `3`, `4`, and unknown ones below `3`.
2. **Vertex counts (exact).**  `L = 3`: **96** for `1 < r < 2` (8 orbits), 72 for `r > 2` (7 orbits) — the request's
   "96 vertices" is the count for `u* < 2u`.  `L = 4`: **21 472** (`1 < r < 3/2`, 191 orbits), **21 184**
   (`3/2 < r < 2`, 189), **3 160** (`2 < r < 3`, 56), **2 888** (`r > 3`, 52).  `L = 5`: **1 965 480**
   (`3 < r < 4`, 2 719 orbits), **1 960 200** (`r > 4`, 2 704 orbits); **at every ratio tried below `3` the
   search passed the stopping rule of `10⁷` vertices and was stopped** (§3).
3. **Validation reproduced** (§4.1): 96 vertices and `a ≤ 3 × 0.495806` at `(0.3, 3)`, certified with all 96
   vertices in interval arithmetic.
4. **`L = 4` (complete, certified; §4.2).**  New cells where the chain's exponent is certified below the cube's:
   `a` at `(0.4, 4)`, `(0.4, 6)`, `(0.3, 2.5)`, `(0.2, 2)`; `h` at `(0.3, 4)`, `(0.3, 6)`, `(0.1, 3)`.  After
   `L = 4`, 14 cells of the grid remain undecided for `a` (`u = 1.5` at every `p`; `(0.3, 2)`; `(0.4, 2 … 3)`;
   `p = 0.45`, `u ≥ 1.5`) and 14 for `h` (`u ≥ 2.5` at `p = 0.45, 0.4`; `u = 2.5, 3` at `p = 0.3, 0.2`;
   `u = 2, 2.5` at `p = 0.1`).
5. **`L = 5`.**  Complete and certified at one grid cell only, `(0.1, 0.5)` (the only one with `u*/u > 3`).
   Elsewhere the enumeration does not finish within the stopping rule.  The part enumerated supports rigorous
   *lower* bounds of the 5-site block quantities, and these show that **the Markov recursion with `L = 5` cannot
   decide 13 of the 14 undecided cells of `a`** (all but `(0.4, 3)`; in particular not `(0.3, 1.5)`, `(0.3, 2)`,
   `(0.4, 1.5)`, `(0.4, 2)`, `(0.4, 2.5)`) **nor 13 of the 14 of `h`** (all but `(0.2, 3)`; in particular not `u = 3`
   at `p = 0.3, 0.4, 0.45`) (§5).
6. **For R10-T2 (§6).**  Of the six cells "`a` at `u = 1.5, 2, 2.5` for `p = 0.3, 0.4`" the recursion with `L = 4`
   decides one (`(0.3, 2.5)`: below), and with `L = 5` provably none of the other five; of "`h` at `u = 3`"
   `L = 4` decides `p = 0.1` only, and `L = 5` provably cannot decide `p = 0.3, 0.4, 0.45` (`p = 0.2` stays open).  Increments of the block capacities indicate that the true crossover of `a_∞` lies much
   lower than the slopes at which blocks of four sites cross the cube, out of reach of block lengths that can be
   enumerated.

## 1. The mathematics of what is computed

### 1.1 Setting (theory report `docs/workstreams/Y_REPORT.md` §1, §5.1; checked against it)

Binary symmetric chain on `{0,1}ⁿ`: `π(x) = ½ ∏ P(x_{i−1}, x_i)`, `P = [[1−p, p], [p, 1−p]]`, `0 < p < ½`,
`K = ln((1−p)/p)`.  Residuals `φ` with `|φ(x) − φ(y)| ≤ u·d_H(x, y)`.  Gibbs law `π_φ = π e^{−φ}/E_π e^{−φ}`.
For a finite space `(X, π)` with an envelope `d` and `0 < t < 1`:

    F*_X(t) = max_M G_t(M) = min_Q max_{φ ∈ Lip(d)} −ln Σ_x π_φ(x)^t Q(x)^{1−t},
    G_t(M)  = −t ln Σ_x ( Σ_φ M(φ) π_φ(x)^t )^{1/t},
    cap_X   = max_M I(M; φ ↦ π_φ) = min_Q max_φ KL(π_φ ‖ Q) ≥ F*_X(t)/(1−t)      (nats).

`F*(t)/t` is nonincreasing and `F*(t)/(1−t)` nondecreasing in `t` (for fixed `φ, Q`, `−ln Σ π_φ^t Q^{1−t}` equals
`(1−t) D_t(π_φ‖Q) = t D_{1−t}(Q‖π_φ)` and Rényi divergences are nondecreasing in their order; `max_φ`, `min_Q`
preserve this).  The exponents of the chain are defined through the limit game function
`F_∞(t) = lim F*_n(t)/n`: `h_∞ = max_t F_∞(t)`, `a_∞ = sup_t F_∞(t)/(1−t)`.  The uniform cube (`p = ½`):
`F_cube(t) = t ln cosh(u/2) − ln cosh(tu/2)`, `a_cube = (u/2) tanh(u/2) − ln cosh(u/2)`, `h_cube = max_t F_cube`.

### 1.2 The block of `L` sites and its polytope

* **Slope of the last site:** `u*` = the fixed point of `x = u + g(x)`, `g(x) = ln[((1−p)eˣ + p)/(p eˣ + 1 − p)]`
  (a contraction, `0 < g′ ≤ 1 − 2p`); `u < u* < u + K`.
* **Block law:** `π_L(x) = ∏_{i=1}^{L} P(x_{i−1}, x_i)` with `x₀ = 0` — the law of `L` consecutive sites given the
  letter before them (`x₀ = 1` gives the same numbers by the flip symmetry).
* **Polytope:** `P_L = { φ : {0,1}^L → ℝ : |φ(x) − φ(x ⊕ e_i)| ≤ w_i for all x, i } / constants`,
  `w = (u, …, u, u*)`; the *last* site of the block (the one farthest from the conditioning letter) carries `u*`.
  The weighted Hamming distance is the path metric of the cube graph, so these edge inequalities are the whole
  Lipschitz condition.  **`2^L − 1` dimensions and `L·2^L` inequalities: 7 and 24 for `L = 3`; 15 and 64 for
  `L = 4`; 31 and 160 for `L = 5`** (the request's numbers for `L = 4, 5`).
* **Block quantities:** `F^{DP}_L(t) := F*[π_L; w](t)`, `cap_L := cap[π_L; w]`.

### 1.3 What a vertex is used for

For fixed `Q`, `φ ↦ KL(π_φ‖Q)` and `φ ↦ −ln Σ_x π_φ(x)^t Q(x)^{1−t}` attain their maximum over `P_L` at a vertex:
in `v = e^{−φ}` the class is the polyhedral cone `{v > 0 : v(y) ≤ e^{w_i} v(x)}`; `ω = πv/Σπv` ranges over a
polytope; `KL(·‖Q)` is convex and `Σ (·)^t Q^{1−t}` concave on it; the extreme rays of the cone (tight
constraints of corank one) are the images of the vertices of `P_L`.  Hence, with the **complete** vertex list `V`,

    for every probability vector Q:   cap_L ≤ max_{φ∈V} KL(π_φ‖Q),     F^{DP}_L(t) ≤ max_{φ∈V} −ln Σ π_φ^t Q^{1−t};
    for every M on members of P_L:    cap_L ≥ I(M),                    F^{DP}_L(t) ≥ G_t(M).

A subset of `V` gives the lower bounds only — this is what limits §5.

### 1.4 How the bounds on `a` and `h` follow (input: Proposition F, block form)

**Proposition F (theory, Y §5.1; block form).**  `F_∞(t) ≤ F^{DP}_L(t)/L` for every `L` and `0 < t < 1`.  Hence

    h_∞ = max_t F_∞(t) ≤ sup_t F^{DP}_L(t) / L,        a_∞ = sup_t F_∞(t)/(1−t) ≤ cap_L / L.

*Status.*  Proved in the theory report; re-derived by the science division (R10 §3.1).  I went through the block
form: with `V_j = E_π[e^{−φ} | x_{≤jL}]`, `−ln V_j` has slope `u` in the block's sites except the last (given the
last site the future does not depend on them) and slope `u + g(u*) = u*` in the last (a positive function with
log-slope `≤ s` in a letter is mapped by `P` to a function of the previous letter with log-slope `≤ g(s)`; `u*` is
the fixed point), so the conditional law of a block given the past is a Gibbs law of a member of `P_L` with
respect to `P^{(L)}(·|x_prev)`; the backward induction of the theory report then gives the bound.  I found no
gap.  Nothing is machine-checked, and I did not touch the theorems that turn the game function into costs of
algorithms.

**The supremum over all `t`** is bounded from a finite grid by the monotonicity of §1.1: on `[t_k, t_{k+1}]`,
`F(t) ≤ min(t·B_k/t_k, (1−t)·B_{k+1}/(1−t_{k+1}))` with `B_k ≥ F(t_k)`; below the first point
`F(t) ≤ B₁/(1−t₁)`, above the last `F(t) ≤ B_m/t_m`.  The grid (`0.05 … 0.95`) is refined until the bound is
within `2·10⁻⁴` (relative) of the largest lower value `G_t(M_t)`.

### 1.5 Ambiguities in the sources and the readings used

* *Which site carries `u*`, and which block law.*  The request says only "weighted cubes `(u, u, u, u*)`".  Y §5.1:
  "`F^{DP}_L := max_b F*[P^{(L)}(· | previous letter b); envelope (d, …, d, d*)]`".  Both divisions' codes, read as
  text, put `u*` on the last site and condition on the letter before the first
  (`r10_06_markov_recursion.py: dp_block, cond_block_law`; `ylib.py: bsc_block_law_cond, ustar`).
* *"`a ≤ 3 × 0.495806`"* is the bound per **block** of three sites, `0.495806` per site; all tables here are per
  site.
* *"inputs `p`, `u`; output the vertex list".*  The vertex list depends on `(p, u)` only through `u*/u` and is
  piecewise constant in it; the validation count 96 is that of the chamber `1 < u*/u < 2` (72 for `u*/u > 2`,
  e.g. at `(0.1, 1)`; R10 §3.5 says so).
* *Grid.*  The review's own grid: `p ∈ {0.45, 0.4, 0.3, 0.2, 0.1}`, `u ∈ {0.5, 1, 1.5, 2, 2.5, 3, 4, 6}`.
* *"Stop at `10⁷` vertices".*  Applied to the number of vertices of the orbits found by the search (the number of
  orbit representatives stored stays below `10⁴`).  §3 discloses three exploratory runs that did not respect it.

## 2. Exact enumeration: the facts it rests on (proofs also in the module docstrings)

Units `u = 1`, weights `(1, …, 1, r)`.  The nodes with one value of the last letter form a *layer* (a cube of
dimension `L − 1` with unit weights); edges inside a layer are *horizontal*, the `2^{L−1}` edges of weight `r`
*vertical*.

**(V) Vertices.**  `φ ∈ P` is a vertex iff the graph of its tight edges is connected (the tight constraint rows
are `±(e_y − e_x)`; incidence vectors of a graph with `c` components on `N` nodes have rank `N − c`).  So a vertex
is determined by a spanning tree of tight edges and signs: for integer weights all vertices are integral, and in
general **`φ = A + rB` with integer arrays `A, B`** (along a tight horizontal edge `(ΔA, ΔB) = (±1, 0)`, along a
tight vertical edge `(0, ±1)`); `A(x) ≡` number of unit letters of `x`, `B(x) ≡` last letter of `x` (mod 2).

**(E) Edges of the polytope at a vertex.**  Orient every tight edge from its lower to its higher end (an acyclic
digraph `T`).  The edges of `P` at `φ` are the directions `−1_U`, `U` a proper non-empty node set that no arc of
`T` leaves and such that `U` and its complement are connected in `T`; the adjacent vertex is `φ − s·1_U`,
`s = min{φ(y) − φ(x) + w_e : {x, y}` an edge of the cube, `x ∉ U, y ∈ U}`.  (The cone of feasible directions is
`{ψ : ψ(y) ≤ ψ(x)` on arcs`}`; it is generated by the `−1_U` with `U` closed under arcs; such a generator is
extreme iff `U` and its complement are connected.)

**(C) Completeness; symmetry.**  The graph of a polytope is connected, so a set of vertices that contains one
vertex and is closed under (E) is the vertex set.  The search starts at `φ(x) = Σ w_i x_i` and works with
**orbits** of the group generated by the permutations of the `L − 1` unit sites, the translations `x ↦ x ⊕ t` and
`φ ↦ −φ` (order `2·(L−1)!·2^L` = 32, 192, 1 536 for `L = 3, 4, 5`): every orbit is represented by a canonical
member, all neighbours (E) of every canonical member are generated, and the search ends when no new orbit
appears.  The block law is *not* invariant under this group, so the bounds need **all** vertices; the scans of §4
run over all images of the stored representatives.

**Chambers of the ratio (the polytope is not rational).**  A symbolic vertex `(A, B)` is feasible exactly for `r`
in a closed interval with rational ends (its interval of validity).  *Chamber lemma:* if at the rational ratio
`r₀` every tight edge of every vertex is identically tight, and `V` is the set of symbolic vertices at `r₀`, then
for every real `r` in the interior `J` of the intersection of their intervals of validity the vertex set of
`P(r)` is exactly `{A + rB : (A, B) ∈ V}`, and it changes at both ends of `J`.  (Two different symbolic vertices
that coincide at some `r₁` cannot both be feasible on both sides of `r₁`; every vertex of `P(r₁)` is a limit of
vertices of `P(r)`; a symbolic vertex not in `V` that became feasible inside `J` would therefore coincide, where
it first appears, with a member of `V` that is feasible around that point.)  So one enumeration in **integer**
arithmetic at the weights `(Q, …, Q, P)`, `P/Q = r₀`, with exact checks, gives the vertex set for all real ratios
of the chamber; whether the real number `u*/u` of a cell lies in a chamber is decided by an interval enclosure of
`u*` against the two rational walls.

**The unbounded chamber.**  For `r > L − 1` there are exactly `2·N_{L−1}²` vertices (`N_m` = number of height
functions of the `m`-cube: `2, 6, 38, 990`): two vertical edges tight with opposite signs at `x₊, x₋` would force
`2r ≤ 2d(x₊, x₋) ≤ 2(L−1)`; with one sign, parity makes every horizontal edge tight.  `2·6² = 72`,
`2·38² = 2 888`, `2·990² = 1 960 200` are the counts found.  Below `r = 2` contacts of both signs at distance two
become possible and the number of vertices explodes.

## 3. Results of the enumeration (exact)

<!-- BEGIN enumeration -->
| `L` | dim | ineq. | chamber of `r = u*/u` | vertices | orbits | degree min / mean / max | vertices ending at lower / upper wall | checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 2 | `(0, inf)` | 2 | 1 | 1 / 1.0 / 1 | 2 / 0 | `9789123f57f26fe0…` |
| 2 | 3 | 8 | `(1, inf)` | 8 | 2 | 3 / 3.5 / 4 | 4 / 0 | `b64ffebc96e5498c…` |
| 3 | 7 | 24 | `(1, 2)` | 96 | 8 | 8 / 11.3 / 18 | 84 / 32 | `b484b2c523861eb9…` |
| 3 | 7 | 24 | `(2, inf)` | 72 | 7 | 9 / 12.6 / 18 | 8 / 0 | `95e48ec0f221afc6…` |
| 4 | 15 | 64 | `(1, 3/2)` | 21 472 | 191 | 16 / 36.2 / 205 | 21 396 / 576 | `9a9b63c4227a6ba4…` |
| 4 | 15 | 64 | `(3/2, 2)` | 21 184 | 189 | 16 / 36.4 / 205 | 288 / 19 280 | `f90a186c2a424e3b…` |
| 4 | 15 | 64 | `(2, 3)` | 3 160 | 56 | 26 / 80.3 / 205 | 1 256 / 288 | `93ba0c63861b11da…` |
| 4 | 15 | 64 | `(3, inf)` | 2 888 | 52 | 28 / 85.3 / 205 | 16 / 0 | `6ee00ad8521fd9dd…` |
| 5 | 31 | 160 | just above `1` (at `102/101`) | **stopped** at 10 420 620 found | 8 426 found | — | — | — |
| 5 | 31 | 160 | just above `3/2` (at `152/101`) | **stopped** at 10 420 620 found | 8 426 found | — | — | — |
| 5 | 31 | 160 | just above `2` (at `203/101`) | **stopped** at 10 084 552 found | 9 409 found | — | — | — |
| 5 | 31 | 160 | `(3, 4)` | 1 965 480 | 2 719 | 135 / 8665.7 / 51972 | 48 736 / 5 312 | `9f151500357aec5c…` |
| 5 | 31 | 160 | `(4, inf)` | 1 960 200 | 2 704 | 135 / 8688.5 / 51972 | 32 / 0 | `7adfed569d8dae27…` |
<!-- END enumeration -->

Checksum: sum modulo `2²⁵⁶` of the SHA-256 digests of all vertices (each as the bytes `A‖B`, int8, normalised at
node 0), independent of order; full values in `results/chambers_L*.json`.  Orbit representatives (symbolic, with
stabiliser orders and degrees): `results/orbits_L<L>_<k>.npz`.

Symbolic vertices that do not end at a wall exist on both sides of it; the two enumerations (at different ratios)
must find the same ones:

<!-- BEGIN walls -->
| `L` | wall | vertices that exist on both sides | orbits | same orbits found by the two enumerations |
|---|---|---|---|---|
| 3 | `2` | 64 | 6 | yes |
| 4 | `3/2` | 20 896 | 187 | yes |
| 4 | `2` | 1 904 | 36 | yes |
| 4 | `3` | 2 872 | 51 | yes |
| 5 | `4` | 1 960 168 | 2 703 | yes |
<!-- END walls -->

**`L = 5` below `r = 3`: not enumerated.**  The search was stopped by the rule "`10⁷` vertices" at each ratio tried
(just above `1`, `3/2`, `2`); the walls there are unknown, and no vertex list exists for any grid cell with
`u*/u < 3`: 39 of the 40 cells.

**Disclosure — three exploratory runs beyond the stopping rule.**  Before the drivers existed I probed the size of
the problem with the vertex limit set to `4·10⁹` instead of `10⁷` (one thread; 64 s, 88 s, 110 s; under `ulimit -v` 3 GiB).
Their outcome is information only; no stored result and no bound uses it: at `r₀ = 5/2` the search *completed*
with **11 685 512 vertices in 10 870 orbits** (17 % above the rule); at `r₀ = 7/4` and `r₀ = 5/4` it was stopped
with more than `4.0·10⁹` vertices in `2.69·10⁶` orbits found and 4–5 % of them processed.  So the chamber that
contains `5/2` would be enumerated in about a minute if the rule were relaxed to `1.2·10⁷` vertices (possibly
adding the cells `(0.1, 1)`, `(0.1, 1.5)`, `(0.1, 2)`, `(0.2, 0.5)`), whereas below `r = 2` the 5-site polytope has
more than `4·10⁹` vertices and is out of reach of this method on this machine.

## 4. The block bounds

**Method.**  For a cell: (1) locate `u*/u` in a chamber (rigorous); (2) *column generation*: solve the capacity /
Rényi problem on a small working set of vertices — in dual form, a convex programme in the centre `Q` with one
linear constraint per vertex, by an active-set SQP method (scipy SLSQP), recovering weights `M` on the active
vertices by non-negative least squares — then scan **all** vertices for the largest value at the centre `Q_M`,
add the violators, repeat until the scan's maximum equals the primal value; (3) certify: lower bound = `I(M)`
resp. `G_t(M)` in interval arithmetic; upper bound = the maximum over all vertices at `Q_M`, either with every
vertex in interval arithmetic (*iv-all*: everything for `L ≤ 3`; the capacity for `L = 4`) or *screened* (`h` for
`L = 4`; `L = 5`).  The upper bound is valid whatever the solver did; the solver only determines how tight it is.

### 4.1 The validation value

<!-- BEGIN validation -->
* vertices of the 3-site block at `(p, u) = (0.3, 3)`: **96** (chamber `(1, 2)`; `u* = 3.8062061299414`, `u*/u = 1.26873537665`);
* capacity of the block, all 96 vertices in interval arithmetic: `1.48741657378 <= cap_3 <= 1.48741657379`, per site **`0.495805524594 <= cap_3/3 <= 0.495805524595`** (certified; the two ends agree to the 12 decimals stored);
* the request's `a <= 3 x 0.495806` is this bound per block: `0.495805524595` rounded up to six decimals is `0.495806`;
* the cube: `a_cube(3)` in `[0.502282209453, 0.502282209454]`; ratio of the bound to the cube `<= 0.9872`.
<!-- END validation -->

Agreement with the science division's `L = 3` numbers on all 40 cells (quoted from its logs in
`results/quoted_science_L3.json`):

<!-- BEGIN compare_science -->
* `a`, 40 cells: largest `|ours - theirs|` = `4.8e-07` (their values have six decimals);
* `h`, their largest dual value on a grid of step 0.005 against our lower end `max_t G_t(M_t)`: ours - theirs in `[-3.9e-07, 9.1e-06]`;
* `h`, their upper bound (interval rule on that grid) minus ours (refined grid): in `[8.8e-05, 2.5e-03]` — ours is smaller in every cell.
<!-- END compare_science -->

Also asserted in the tests: the theory report's `u* = 1.218, 1.526, 1.981, 2.750`, its "DP" values
`a ≤ 0.12970, 0.15401, 0.17747, 0.19678` (`L = 3`, `u = 1`) and `h ≤ 0.05484, 0.05180, 0.04902`,
`0.09157, 0.08299, 0.07542` (`p = 0.3, 0.1`; `L = 1, 2, 3`), and the product control (three independent sites as
one super-site with its 38 vertices give the cube's exponents to `10⁻¹⁰`).

### 4.2 Tables: `L = 3` and `L = 4` on the grid (certified; per site)

<!-- BEGIN bounds_a -->
`a`: certified upper bound per site with blocks of `L = 3` / `L = 4` sites (in brackets: ratio to the cube, rounded up); bold = certified below the cube; last row: the cube (closed form, rounded down)

| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | 0.034366 (1.1342) / 0.034034 (1.1233) | 0.118768 (1.0706) / 0.117367 (1.0579) | 0.227569 (1.0435) / 0.225208 (1.0327) | 0.336926 (1.0278) / 0.334245 (1.0197) | 0.432148 (1.0178) / 0.429658 (1.0119) | 0.507949 (1.0113) / 0.505895 (1.0072) | 0.605801 (1.0046) / 0.604656 (1.0027) | 0.676351 (1.0008) / 0.676101 (1.0004) |
| `0.4` | 0.040824 (1.3474) / 0.039654 (1.3087) | 0.129698 (1.1691) / 0.126996 (1.1447) | 0.236806 (1.0858) / 0.232176 (1.0646) | 0.342802 (1.0458) / 0.337491 (1.0296) | 0.434926 (1.0243) / 0.429957 (1.0126) | 0.508653 (1.0127) / 0.504515 (1.0045) | 0.605012 (1.0033) / **0.602655** (0.9994) | 0.675931 (1.0002) / **0.675401** (0.9994) |
| `0.3` | 0.058225 (1.9217) / 0.055187 (1.8214) | 0.154012 (1.3882) / 0.148377 (1.3374) | 0.253516 (1.1625) / 0.244575 (1.1215) | 0.345590 (1.0543) / 0.335653 (1.0240) | 0.427435 (1.0067) / **0.417817** (0.9840) | **0.495806** (0.9872) / **0.487418** (0.9705) | **0.591983** (0.9817) / **0.586713** (0.9730) | **0.671581** (0.9938) / **0.670235** (0.9918) |
| `0.2` | 0.083017 (2.7399) / 0.077203 (2.5480) | 0.177467 (1.5997) / 0.166193 (1.4980) | 0.262497 (1.2036) / 0.249544 (1.1442) | 0.340137 (1.0376) / **0.326041** (0.9946) | **0.408174** (0.9613) / **0.394873** (0.9300) | **0.467509** (0.9308) / **0.455132** (0.9062) | **0.559987** (0.9286) / **0.550802** (0.9134) | **0.658014** (0.9737) / **0.654936** (0.9691) |
| `0.1` | 0.114467 (3.7778) / 0.104259 (3.4409) | 0.196777 (1.7737) / 0.175895 (1.5855) | 0.261810 (1.2005) / 0.242043 (1.1098) | **0.323642** (0.9873) / **0.305875** (0.9331) | **0.381519** (0.8986) / **0.364692** (0.8589) | **0.432593** (0.8613) / **0.416668** (0.8296) | **0.509683** (0.8452) / **0.496015** (0.8226) | **0.614287** (0.9090) / **0.606621** (0.8976) |
| cube | 0.030299 | 0.110944 | 0.218095 | 0.327813 | 0.424611 | 0.502282 | 0.603052 | 0.675835 |
<!-- END bounds_a -->

<!-- BEGIN bounds_h -->
`h`: certified upper bound per site with blocks of `L = 3` / `L = 4` sites (in brackets: ratio to the cube, rounded up); bold = certified below the cube; last row: the cube (closed form, rounded down)

| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | 0.009125 (1.1892) / 0.009041 (1.1784) | 0.032430 (1.1130) / 0.032159 (1.1037) | 0.064642 (1.0681) / 0.064036 (1.0581) | 0.101397 (1.0424) / 0.100484 (1.0330) | 0.139527 (1.0291) / 0.138456 (1.0212) | 0.176502 (1.0213) / 0.175397 (1.0149) | 0.242295 (1.0128) / 0.241306 (1.0086) | 0.338115 (1.0061) / 0.337466 (1.0042) |
| `0.4` | 0.011010 (1.4349) / 0.010888 (1.4190) | 0.037367 (1.2824) / 0.036405 (1.2494) | 0.069980 (1.1563) / 0.068934 (1.1390) | 0.106073 (1.0904) / 0.104416 (1.0734) | 0.142718 (1.0527) / 0.140670 (1.0376) | 0.178728 (1.0342) / 0.176527 (1.0214) | 0.243587 (1.0182) / 0.241557 (1.0097) | 0.338965 (1.0086) / 0.337619 (1.0046) |
| `0.3` | 0.016134 (2.1028) / 0.015870 (2.0683) | 0.049029 (1.6826) / 0.046509 (1.5961) | 0.081196 (1.3417) / 0.078591 (1.2986) | 0.114625 (1.1783) / 0.111820 (1.1495) | 0.148388 (1.0945) / 0.144609 (1.0666) | 0.180406 (1.0439) / 0.176429 (1.0209) | 0.241217 (1.0083) / **0.237027** (0.9908) | 0.336957 (1.0027) / **0.333968** (0.9938) |
| `0.2` | 0.024043 (3.1335) / 0.023442 (3.0551) | 0.061981 (2.1271) / 0.057766 (1.9825) | 0.092947 (1.5358) / 0.085831 (1.4182) | 0.120347 (1.2372) / 0.116398 (1.1966) | 0.150951 (1.1134) / 0.146308 (1.0792) | 0.180892 (1.0467) / 0.174894 (1.0120) | **0.234641** (0.9808) / **0.228623** (0.9556) | **0.328000** (0.9760) / **0.322801** (0.9606) |
| `0.1` | 0.036125 (4.7081) / 0.034715 (4.5244) | 0.075437 (2.5889) / 0.068885 (2.3640) | 0.103751 (1.7143) / 0.093076 (1.5380) | 0.127479 (1.3105) / 0.115922 (1.1917) | 0.149217 (1.1006) / 0.143539 (1.0587) | 0.175957 (1.0181) / **0.170304** (0.9854) | **0.227631** (0.9515) / **0.219380** (0.9170) | **0.308297** (0.9174) / **0.301039** (0.8958) |
| cube | 0.007672 | 0.029139 | 0.060521 | 0.097280 | 0.135582 | 0.172830 | 0.239249 | 0.336075 |
<!-- END bounds_h -->

Brackets: for `a` the certified lower and upper ends of `cap_L/L` agree to the 12 decimals stored in every cell
(the numbers above *are* the block capacities per site); for `h` the certified lower end `max_t G_t(M_t)/L` is
within `2·10⁻⁴` (relative) of the upper bound.  Methods: `a` iv-all for `L = 3, 4`; `h` iv-all for `L = 3`,
screened for `L = 4` (up to 174 grid points of `t` per cell).  Everything with 12 decimals:
`results/bounds_L<L>.json` (`L = 1, 2` included).

**Status of every cell.**  `B3`, `B4`: certified below the cube, with the first block length `L` that shows it.
`A`: above the cube according to the science division's map (R10 §5: a proved lower bound above the cube; `A*` =
its mark `R*`, by Proposition I only) — **quoted, not recomputed here**; no cell is in conflict with it.  `U-`:
undecided, and `L = 5` provably cannot decide (§5).  `U?`: undecided, `L = 5` open.

`a`:

<!-- BEGIN status_a -->
| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | A | A | U- | U- | U- | U- | U- | U- |
| `0.4` | A | A | U- | U- | U- | U? | **B4** | **B4** |
| `0.3` | A | A | U- | U- | **B4** | **B3** | **B3** | **B3** |
| `0.2` | A | A | U- | **B4** | **B3** | **B3** | **B3** | **B3** |
| `0.1` | A | A* | U- | **B3** | **B3** | **B3** | **B3** | **B3** |
<!-- END status_a -->

`h`:

<!-- BEGIN status_h -->
| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | A | A | A | A | U- | U- | U- | U- |
| `0.4` | A | A | A | A | U- | U- | U- | U- |
| `0.3` | A | A | A | A | U- | U- | **B4** | **B4** |
| `0.2` | A | A | A | A* | U- | U? | **B3** | **B3** |
| `0.1` | A | A | A | U- | U- | **B4** | **B3** | **B3** |
<!-- END status_h -->

*Where is the capacity attained?*

<!-- BEGIN optimal_support -->
* `L = 3`: the capacity is attained by the `2^L` site-wise labels alone in 35 of 40 cells (all cells with `p` in {0.45, 0.4, 0.3}); exceptions (site-wise optimum / capacity): `(0.2, 2)` 0.99943, `(0.1, 1)` 0.99915, `(0.1, 2)` 0.99998, `(0.1, 2.5)` 0.99949, `(0.1, 3)` 0.99955.
* `L = 4`: the capacity is attained by the `2^L` site-wise labels alone in 34 of 40 cells (all cells with `p` in {0.45, 0.4, 0.3}); exceptions (site-wise optimum / capacity): `(0.2, 1.5)` 0.99998, `(0.2, 2)` 0.99991, `(0.1, 1.5)` 0.99998, `(0.1, 2)` 0.99981, `(0.1, 2.5)` 0.99987, `(0.1, 3)` 0.99990.
<!-- END optimal_support -->

### 4.3 Rounding in the *screened* certificates

The scan evaluates, for every vertex, `Z = Σ_x π(x)e^{−φ(x)}` and `S = Σ_x π(x)e^{−φ(x)}(ln π(x) − φ(x) − ln Q(x))`
(resp. `Σ_x π(x)^t Q(x)^{1−t} e^{−tφ(x)}`) in IEEE double precision, from at most `2·2^L` tabulated exponentials
per orbit representative and order, and then `S/Z − ln Z` (resp. `t ln Z − ln Σ`).  With `|φ| ≤ 60`, positive
terms in `Z`, logarithmic factors below 200 in modulus and at most 32 terms, recursive summation and one unit in
the last place for the library's `exp` and `log` give an absolute error below `10⁻¹¹`.  The certificate allows
`10⁻⁹`: every vertex whose scan value is within `10⁻⁷` of the maximum is enclosed in interval arithmetic, all
others are bounded by (maximum `− 10⁻⁷ + 10⁻⁹`).  This is an analysis of the kernel's arithmetic, not an interval
computation; the *iv-all* certificates do not depend on it.  Spot check (five cells with `L = 4, 5`; 100 vertices
each for the capacity and for `t = 0.4`): the largest difference between a scan value and its interval enclosure
is `1.4·10⁻¹⁵`.

## 5. `L = 5`

### 5.1 The one cell whose chamber is enumerated (certified, screened)

<!-- BEGIN L5_complete -->
| `(p, u)` | chamber | vertices | `a`: certified bracket of `cap_5/5` | upper / cube | `h`: certified bracket of `sup_t F*/5` | upper / cube | method |
|---|---|---|---|---|---|---|---|
| `(0.1, 0.5)` | `(3, 4)` | 1 965 480 | [0.095526, 0.095527] | 3.1527 | [0.033376, 0.033384] | 4.3509 | screened |
<!-- END L5_complete -->

### 5.2 Where the enumeration stops: what the enumerated part supports

For each of the other 39 cells the search was run at a rational ratio next to the cell's `u*/u` and stopped at
`10⁷` vertices.  Every orbit found is a symbolic vertex (exact checks); those whose interval of validity contains
the cell's ratio (decided with the enclosure of `u*`) are vertices of the cell's own polytope.  On this *part* of
the vertex set the problems are solved as in §4, followed by **local pricing**: all polytope neighbours (E) of
every vertex in the support are generated and added if they improve.  The result is a weight vector `M` on
genuine members of the class, so that, certified in interval arithmetic,

    cap₅/5 ≥ I(M)/5      and      sup_t F^{DP}_5(t)/5 ≥ G_t(M_t)/5.

These are **lower bounds of the quantities that bound `a_∞` and `h_∞` from above** — not bounds on `a_∞`, `h_∞`.
What they prove: *where the lower bound is at or above the cube's exponent (bold), the Markov recursion with
`L = 5` cannot show that the chain is below the cube.*  Where it is below, `L = 5` would show it **if** the optimum
over the part were the optimum over all vertices — an indication only: for `a`, in every cell no vertex of the
part scanned (about `10⁷`) and no neighbour of the support has a larger value; for `h`, no vertex of the part
scanned has (one round of local pricing found four improving neighbours in the 39 cells together; they were
added).

`a` — certified lower bound of `cap₅/5` (ratio to the cube, rounded down); bold = `L = 5` cannot show "below":

<!-- BEGIN L5_partial_a -->
| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | **0.033830** (1.1165) | **0.116525** (1.0503) | **0.223791** (1.0261) | **0.332635** (1.0147) | **0.428162** (1.0083) | **0.504661** (1.0047) | **0.603968** (1.0015) | **0.675950** (1.0001) |
| `0.4` | **0.039163** (1.2925) | **0.125375** (1.1300) | **0.229397** (1.0518) | **0.334304** (1.0198) | **0.426975** (1.0055) | 0.502031 (0.9995) | 0.601239 (0.9969) | 0.675083 (0.9988) |
| `0.3` | **0.053109** (1.7528) | **0.144558** (1.3029) | **0.239318** (1.0973) | **0.329679** (1.0056) | 0.412043 (0.9704) | 0.482385 (0.9603) | 0.583551 (0.9676) | 0.669426 (0.9905) |
| `0.2` | **0.072250** (2.3845) | **0.160260** (1.4445) | **0.241582** (1.1076) | 0.317881 (0.9697) | 0.386793 (0.9109) | 0.447695 (0.8913) | 0.545303 (0.9042) | 0.653088 (0.9663) |
| `0.1` | (enumerated) | **0.165085** (1.4880) | **0.231805** (1.0628) | 0.295179 (0.9004) | 0.354269 (0.8343) | 0.406906 (0.8101) | 0.487993 (0.8092) | 0.602041 (0.8908) |
<!-- END L5_partial_a -->

`h` — certified lower bound of `sup_t F^{DP}_5/5` (ratio to the cube, rounded down); bold = `L = 5` cannot show
"below":

<!-- BEGIN L5_partial_h -->
| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | **0.008958** (1.1675) | **0.031968** (1.0970) | **0.063660** (1.0518) | **0.099914** (1.0270) | **0.137786** (1.0162) | **0.174700** (1.0108) | **0.240657** (1.0058) | **0.337007** (1.0027) |
| `0.4` | **0.010766** (1.4031) | **0.036022** (1.2362) | **0.068163** (1.1262) | **0.103412** (1.0630) | **0.139412** (1.0282) | **0.175170** (1.0135) | **0.240290** (1.0043) | **0.336742** (1.0019) |
| `0.3` | **0.015609** (2.0343) | **0.044980** (1.5436) | **0.077266** (1.2766) | **0.109709** (1.1277) | **0.142481** (1.0508) | **0.174004** (1.0067) | 0.234468 (0.9800) | 0.332113 (0.9882) |
| `0.2` | **0.022859** (2.9793) | **0.054206** (1.8602) | **0.083932** (1.3868) | **0.113608** (1.1678) | **0.142565** (1.0515) | 0.171632 (0.9930) | 0.225042 (0.9406) | 0.319635 (0.9510) |
| `0.1` | (enumerated) | **0.063460** (2.1778) | **0.086226** (1.4247) | **0.113334** (1.1650) | **0.139766** (1.0308) | 0.165087 (0.9551) | 0.214741 (0.8975) | 0.296451 (0.8820) |
<!-- END L5_partial_h -->

The searches behind these two tables (per cell: `results/partial_L5.json`; table: block `L5_partial_search_full`
of `results/tables.txt`):

<!-- BEGIN L5_partial_search -->
* 35 cells (`u*/u` from 1.0333 to 1.9807): search stopped with 10 420 620 vertices in 8 426 orbits found (23 processed); vertices of the cell's own polytope among them (a rigorous lower bound of its number of vertices): 10 420 620;
* 4 cells (`u*/u` from 2.0270 to 2.7497): search stopped with 10 084 552 vertices in 9 409 orbits found (1646 processed); vertices of the cell's own polytope among them (a rigorous lower bound of its number of vertices): 10 084 552;
* neighbours of the support examined per cell (`a`): 37 895 to 283 061; improving neighbours found: 0 (`a`), 4 (`h`);
* the optimum over the part equals the optimum over the 32 site-wise labels in 32 of 39 cells (all cells with `p >= 0.3`); it is larger at `(0.2, 1)`, `(0.2, 1.5)`, `(0.2, 2)`, `(0.1, 1.5)`, `(0.1, 2)`, `(0.1, 2.5)`, `(0.1, 3)`.
<!-- END L5_partial_search -->

## 6. What this decides for R10-T2, and what it does not

**The cells named in R10-T2.**

* `a` at `(0.3, 2.5)`: **decided — below the cube** (`L = 4`; certified, iv-all).
* `a` at `(0.3, 2)`, `(0.3, 1.5)`, `(0.4, 1.5)`, `(0.4, 2)`, `(0.4, 2.5)`: **not decided by `L = 4`, and provably
  not decidable by `L = 5`** (the certified lower bound of `cap₅/5` is above the cube).  The expectation of the
  request ("the Markov recursion with `L = 4, 5` decides `a` at `u = 1.5, 2, 2.5` for `p = 0.3, 0.4`") is thereby
  refuted for five of the six cells.
* `h` at `u = 3`: `p = 0.1` **decided — below** (`L = 4`; certified, screened); `p = 0.3, 0.4, 0.45`: not decided
  by `L = 4` and provably not decidable by `L = 5` (second table of §5.2); `p = 0.2`: not decided by `L = 4`, open
  for `L = 5` (the optimum over the enumerated part is below the cube, an indication only).
* `h` at `(0.3, 4)`: **decided — below** (`L = 4`; certified, screened).

**Where the block bound crosses the cube** (floating-point bisection in `u`; the two neighbouring slopes with two
decimals certified).  Nothing proves that "below" persists between or beyond the certified slopes: for `h`,
`p = 0.3`, `L = 4` the bound is below the cube only between `u ≈ 3.45` and `u ≈ 9.41`.

<!-- BEGIN crossover -->
| `L` | `p` | exponent | bound crosses the cube at `u ≈` (numerical) | certified below the cube at | block quantity certified above the cube at |
|---|---|---|---|---|---|
| 3 | `0.45` | `a` | none: above the cube at every tabulated slope in `[1, 12]` | — | — |
| 3 | `0.45` | `h` | none: above the cube at every tabulated slope in `[1, 12]` | — | — |
| 3 | `0.4` | `a` | `7.267` (downwards) | `u = 7.27`: `0.687394042 < 0.687394096` | `u = 7.26`: `0.687343483 > 0.687343342` |
| 3 | `0.4` | `h` | none: above the cube at every tabulated slope in `[1, 12]` | — | — |
| 3 | `0.3` | `a` | `2.622` (downwards) | `u = 2.63`: `0.446563252 < 0.446726583` | `u = 2.62`: `0.445125182 > 0.445073250` |
| 3 | `0.3` | `h` | none: above the cube at every tabulated slope in `[1, 12]` | — | — |
| 3 | `0.2` | `a` | `2.196` (downwards) | `u = 2.20`: `0.368356234 < 0.368612784` | `u = 2.19`: `0.366974167 > 0.366633769` |
| 3 | `0.2` | `h` | `3.585` (downwards) | `u = 3.59`: `0.213456561 < 0.213524595` | `u = 3.58`: `0.212891525 > 0.212870164` |
| 3 | `0.1` | `a` | `1.954` (downwards) | `u = 1.96`: `0.318816303 < 0.319370787` | `u = 1.95`: `0.317606319 > 0.317247058` |
| 3 | `0.1` | `h` | `3.190` (downwards) | `u = 3.20`: `0.186941056 < 0.187081811` | `u = 3.19`: bracket `[0.186359143, 0.186395547]` contains the cube's `0.186379798` |
| 4 | `0.45` | `a` | none: above the cube at every tabulated slope in `[1, 12]` | — | — |
| 4 | `0.45` | `h` | none: above the cube at every tabulated slope in `[1, 12]` | — | — |
| 4 | `0.4` | `a` | `3.707` (downwards) | `u = 3.71`: `0.580316841 < 0.580322553` | `u = 3.70`: `0.579466387 > 0.579454356` |
| 4 | `0.4` | `h` | none: above the cube at every tabulated slope in `[1, 12]` | — | — |
| 4 | `0.3` | `a` | `2.241` (downwards) | `u = 2.25`: `0.378137479 < 0.378404325` | `u = 2.24`: `0.376488638 > 0.376459990` |
| 4 | `0.3` | `h` | `3.452` (downwards) | `u = 3.46`: `0.204875622 < 0.204918372` | `u = 3.45`: bracket `[0.204225602, 0.204265854]` contains the cube's `0.204247571` |
| 4 | `0.3` | `h` | `9.405` (upwards) | `u = 9.40`: `0.429961552 < 0.429964368` | `u = 9.41`: bracket `[0.430078775, 0.430163056]` contains the cube's `0.430162485` |
| 4 | `0.2` | `a` | `1.972` (downwards) | `u = 1.98`: `0.323108429 < 0.323602706` | `u = 1.97`: `0.321637672 > 0.321489367` |
| 4 | `0.2` | `h` | `3.134` (downwards) | `u = 3.14`: `0.182752038 < 0.182852689` | `u = 3.13`: `0.182158325 > 0.182143899` |
| 4 | `0.1` | `a` | `1.758` (downwards) | `u = 1.76`: `0.275858428 < 0.276046212` | `u = 1.75`: `0.274578947 > 0.273840434` |
| 4 | `0.1` | `h` | `2.880` (downwards) | `u = 2.88`: `0.164070820 < 0.164080561` | `u = 2.87`: `0.163513271 > 0.163345154` |
<!-- END crossover -->

**Brackets for the first slope at which the exponent itself is below the cube's**: lower end = the largest grid
slope at which "above" is proved (quoted from the science division's map), upper end = the smallest slope at which
"below" is certified here (`L = 4`).  `a`: `p = 0.4`: `(1, 3.71]`; `p = 0.3`: `(1, 2.25]`; `p = 0.2`: `(1, 1.98]`;
`p = 0.1`: `(1, 1.76]`; `p = 0.45`: `(1, ∞)` — no slope up to 12 is certified below.  `h`: `p = 0.3`: `(2, 3.46]`;
`p = 0.2`: `(2, 3.14]`; `p = 0.1`: `(1.5, 2.88]`; `p = 0.4, 0.45`: `(2, ∞)`.

**Indications (numerical, not bounds).**  (i) *Increments.*  `cap_L = L·(limit of cap_L/L) + O(1)`, so the
increment `cap₄ − cap₃` estimates that limit far better than `cap₄/4`; divided by the cube's `a`:

<!-- BEGIN increments -->
| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | 1.0904 | 1.0200 | 1.0001 | 0.9951 | 0.9943 | 0.9949 | 0.9970 | 0.9993 |
| `0.4` | 1.1928 | 1.0716 | 1.0009 | 0.9809 | 0.9775 | 0.9797 | 0.9876 | 0.9970 |
| `0.3` | 1.5206 | 1.1850 | 0.9984 | 0.9330 | 0.9160 | 0.9203 | 0.9467 | 0.9857 |
| `0.2` | 1.9722 | 1.1931 | 0.9660 | 0.8656 | 0.8360 | 0.8322 | 0.8677 | 0.9554 |
| `0.1` | 2.4302 | 1.0208 | 0.8379 | 0.7705 | 0.7400 | 0.7344 | 0.7545 | 0.8636 |
<!-- END increments -->

(At `(0.3, 3)` the increment is the `0.4623` that SCI-REV-0010 §2 finds for increments of exact finite chains.)
(ii) *Longer blocks through site-wise labels.*  The `2^L` site-wise labels `φ_σ(x) = Σ_i w_i[x_i ≠ σ_i]` belong to
the class for every ratio; their optimum `sw_L ≤ cap_L` needs no enumeration, and for `L ≤ 4` it *is* the capacity
in all cells with `p ≥ 0.3` (§4.2).  Hence blocks shorter than the length in the first table below cannot show
"below" (rigorous up to floating point); and **if** site-wise labels stayed optimal for all `L` (unproved) the
increments of `sw_L` would converge to `a_∞` itself:

<!-- BEGIN sitewise -->
shortest block length `L` with (site-wise optimum)`/L <` cube; shorter blocks cannot show `a` below the cube (`> 8 (≈ n)`: none up to `L = 8`, `n` extrapolated; `none`: the increment itself is above the cube)

| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | none | none | none | > 8 (≈ 20) | > 8 (≈ 13) | > 8 (≈ 10) | 8 | 7 |
| `0.4` | none | none | none | > 8 (≈ 11) | 7 | 5 | 4 | 4 |
| `0.3` | none | none | none | 6 | 4 | 3 | 2 | 2 |
| `0.2` | none | none | > 8 (≈ 20) | 4 | 3 | 2 | 2 | 2 |
| `0.1` | none | none | 8 | 3 | 2 | 2 | 2 | 2 |

increment `sw_8 - sw_7` of the site-wise optimum divided by the cube's `a` (numerical indication of `a_inf / a_cube` where site-wise labels are optimal; not a bound)

| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | 1.0884 | 1.0200 | 1.0001 | 0.9951 | 0.9943 | 0.9949 | 0.9970 | 0.9993 |
| `0.4` | 1.2257 | 1.0716 | 1.0009 | 0.9809 | 0.9775 | 0.9797 | 0.9876 | 0.9970 |
| `0.3` | 1.5632 | 1.1688 | 1.0004 | 0.9328 | 0.9160 | 0.9203 | 0.9467 | 0.9857 |
| `0.2` | 1.9413 | 1.2118 | 0.9631 | 0.8680 | 0.8350 | 0.8321 | 0.8678 | 0.9554 |
| `0.1` | 2.0530 | 1.1335 | 0.8670 | 0.7675 | 0.7353 | 0.7322 | 0.7558 | 0.8637 |

slope at which the increment of the block capacity crosses the cube's `a` (numerical; search interval `[1, 3]`)

| `p` | exact capacities, `cap_4 - cap_3` | site-wise optima, `sw_7 - sw_6` |
|---|---|---|
| `0.45` | 1.51 | 1.51 |
| `0.4` | 1.51 | 1.51 |
| `0.3` | 1.49 | 1.50 |
| `0.2` | 1.41 | 1.39 |
| `0.1` | 1.03 | 1.19 |
<!-- END sitewise -->

Reading (indication only): the crossover of `a_∞` would be near `u ≈ 1.5` for `p = 0.45, 0.4, 0.3` and near `1.4`
for `p = 0.2`; for `p = 0.1` the two estimates disagree (site-wise labels are not optimal there and short blocks are
far from the limit).  At `(0.3, 1.5)` the increment is within `5·10⁻⁴` of the cube: the crossover for `p = 0.3`
cannot be resolved by block bounds of any length that can be enumerated; it needs the first-order expansion asked
for in R10-T2 or bounds of the Lyapunov type (theory report, Propositions H, I) at these slopes.

## 7. Cross-checks performed

<!-- BEGIN crosschecks -->
* `L <= 3`, 9 weight vectors (`(1,)`: 2, `(4, 5)`: 8, `(1, 1)`: 6, `(4, 4, 5)`: 96, `(2, 2, 3)`: 96, `(7, 7, 13)`: 96, `(4, 4, 9)`: 72, `(1, 1, 2)`: 68, `(1, 1, 1)`: 38 vertices): the methods bases, bfs, bfs_orbits, dfs, kernel, ppl give identical vertex sets in every case; every vertex passes the exact rank test.
* `L = 4`, chamber `(1, 3/2)`, 21 472 vertices: identical to the vertex set of the Parma Polyhedra Library; orbits, stabilisers and degrees identical to the reference implementation.
* `L = 4`, chamber `(3/2, 2)`, 21 184 vertices: identical to the vertex set of the Parma Polyhedra Library; orbits, stabilisers and degrees identical to the reference implementation.
* `L = 4`, chamber `(2, 3)`, 3 160 vertices: identical to the vertex set of the Parma Polyhedra Library; orbits, stabilisers and degrees identical to the reference implementation.
* `L = 4`, chamber `(3, inf)`, 2 888 vertices: identical to the vertex set of the Parma Polyhedra Library; orbits, stabilisers and degrees identical to the reference implementation.
* uniform 5-cube: 395 094 vertices in 237 orbits (known number of height functions: 395 094).
* `L = 5`, chamber `(3, 4)`: all 522 744 neighbours of 43 representatives (the three of largest degree and 40 random ones) recomputed with the reference implementation lie in the enumerated orbits; 25 random representatives pass the exact rank test.
* `L = 5`, chamber `(4, inf)`: all 555 917 neighbours of 43 representatives (the three of largest degree and 40 random ones) recomputed with the reference implementation lie in the enumerated orbits; 25 random representatives pass the exact rank test; the count equals `2 x 990^2`.
<!-- END crosschecks -->

Methods, independent in what they use: breadth-first search over the polytope graph ((V), (E), (C)); depth-first
search over attachment orders ((V) only); brute force over all sets of `2^L − 1` edges with an exact rank test and
all sign patterns (the definition of a vertex; `L ≤ 3`); the double-description code of the Parma Polyhedra
Library (`pplpy`, exact integers; `L ≤ 4`); the C kernel against the Python reference implementation.  In the
tests in addition: the edges (E) against the exact rank criterion of adjacency for `L = 3`; the vertex criterion
(V) against exact rank; the counts `2N²`; the uniform cubes `2, 6, 38, 990` (`395 094` in the driver); the
agreement across every wall; the kernel's floating-point scans against plain numpy on explicit vertex lists
(`L = 3, 4, 5`); the solvers against Blahut–Arimoto and Arimoto iterations; the Jacobian of the Rényi problem
against differences.

## 8. Sources read (read-only, as text; nothing of them was executed)

* science, `2b4ccdf`: `docs/collaboration/messages/science/SCI-REV-0010.md` (in full);
  `docs/science/workstreams/R10_REPORT.md` (in full); `experiments/science/ws_R10/r10_13_reversal.py`,
  `r10lib.py`, `r10_06_markov_recursion.py` (in full); `r10_13_reversal_a.log`, `r10_13_reversal_b.log` (in full;
  parsed into `results/quoted_science_L3.json`).  Extracted with `git show` but not read:
  `r10_14_rerun_their_functions.py/.log`, `r10_15_large_slope_checks.py`, `NOTES.md`,
  `r10_06_markov_recursion.log`, `r10_06_markov_recursion_large_u.log`.
* theory, `8ff0667`: `docs/workstreams/Y_REPORT.md` (in full); `experiments/workstreams/Y/code/ylib.py`, lines
  147–321 (`cube_numbers` … `ustar`).  Extracted but not read: `y02_blocks.py`.

**What looks wrong or ambiguous in the sources.**

1. *The request's expectation is too optimistic* (§6): `L = 4` decides one of the six `a`-cells of R10-T2 and `h`
   at `u = 3` for `p = 0.1` only; `L = 5` cannot decide the other five `a`-cells nor `h` at `u = 3` for `p ≥ 0.3`.
2. *"Stop at `10⁷` vertices; estimate: minutes for `L = 4`".*  `L = 4` takes milliseconds; `L = 5` exceeds `10⁷`
   vertices at every ratio tried below `3`.
3. *The request does not say that the vertex set depends on `u*/u`* (R10 §3.5 does for `L = 3`); for `L = 4`
   there are the further walls `3/2` and `3`.
4. *A precision, not an error:* the science division's `h` upper bounds (interval rule on a fixed grid of step
   `0.005`) are valid but up to about `1 %` above what the same block gives with a refined grid; no verdict of its
   map changes.
5. *Monotonicity in the slope is not available:* statements of the form "lowered at `u = 4, 6`" should not be read
   as "from `u = 4` on" — for `h`, `p = 0.3`, `L = 4` the bound returns above the cube at `u ≈ 9.4`.
6. I found nothing wrong in the definitions; both codes agree with the theory report on the envelope and the
   block law.

## 9. How to re-run

Repository root; `source "$HOME/.venvs/metricchain/bin/activate"`; one thread each
(`export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`).

| command | writes | time (one thread) |
|---|---|---|
| `python experiments/eng/weighted_cube/run_enumeration.py --L 1 2 3 4` | `results/chambers_L1..4.json`, `orbits_L*.npz` | 1 s |
| `python experiments/eng/weighted_cube/run_enumeration.py --L 5 --start 1 --also-start 3/2 2 3` | `results/chambers_L5.json`, `orbits_L5_*.npz` | 6 min |
| `python experiments/eng/weighted_cube/run_bounds.py --L 1 2 3 4` | `results/bounds_L1..4.json` | 5 min |
| `python experiments/eng/weighted_cube/run_bounds.py --L 5` | `results/bounds_L5.json` | 35 s |
| `python experiments/eng/weighted_cube/run_partial_L5.py --h` | `results/partial_L5.json` | 24 min |
| `python experiments/eng/weighted_cube/run_crossover.py` | `results/crossover.json` | 2 min |
| `python experiments/eng/weighted_cube/run_sitewise.py` | `results/sitewise.json` | 3 min |
| `python experiments/eng/weighted_cube/run_crosschecks.py` | `results/crosschecks.json` | 15 min |
| `python experiments/eng/weighted_cube/make_tables.py --out results/tables.txt` / `--verify` | `results/tables.txt` | 1 s |
| `python -m pytest tests/eng/test_weighted_cube.py -q` | — | 10 s (`WCUBE_SLOW=1`: 2.3 min) |

The kernel `wcube_kernel.c` is compiled on first use with `cc` into `$METRICCHAIN_ENG_BUILD` or, by default, into
`build/` at the repository root (git-ignored, the convention of the other engineering kernels); the tests compile
into a temporary directory.  If this text is saved as `REPORT.md` next to the drivers,
`make_tables.py --write` / `--verify` maintain its tables.

## 10. Limitations

* **Proposition F is an input.**  "Below the cube" is a statement about the limit game function given that
  proposition; as a statement about costs of algorithms it inherits the status of the theory report's theorems
  (R10 §3.3), which this work did not touch.  "Above (quoted)" entries rest entirely on the other divisions' lower
  bounds.
* **`L = 5` is essentially not done:** one cell of forty.  The rigorous statements of §5.2 are *negative* ones
  (what `L = 5` cannot show); the entries there that are below the cube are indications.
* **Screened certificates** (`h` for `L = 4`; `L = 5`) rest on the rounding analysis of §4.3 and on IEEE
  arithmetic in the kernel; iv-all certificates (`L ≤ 3`; `a` for `L = 4`) do not.  Interval arithmetic is
  `mpmath.iv`; no proof assistant is involved.
* **The enumeration for `L = 5`** has no fully independent second method at full scale (the Parma library is
  feasible up to `L = 4`); it is supported by the count `2·990²`, the uniform cube, the agreement across the wall
  `r = 4`, and a closure check of a sample of orbits with the reference implementation.
* The supremum over `t` carries a relative overshoot of at most `2·10⁻⁴`, on the safe side.
* Site-wise sequences and increments (§6) are floating-point numbers and, as estimates of `a_∞`, conditional on an
  unproved optimality: indications.
* No statement is made between grid slopes except at the slopes listed in §6.

---

## Note added at checkpoint 6 (2026-11-27): the Parma library and the rounding mode

Importing `pplpy` — used here for one cross-check of the vertex sets (§7) — switches the
floating-point unit of the whole Python process to upward rounding and leaves it there.
We found this on 2026-11-26, when an unrelated test failed only in sessions that had
collected this module's tests.  **No result of this report is affected**: the vertex
sets are exact integers and rationals; the certified capacities and exponents use
software interval arithmetic (`mpmath.iv`) on exact rational inputs, which does not
depend on the hardware rounding mode; the uncertified floating-point values can differ
by a unit in the last place, far below the digits reported; and the science division
re-ran the tests and reproduced the capacities on a machine without the library
(SCI-RES-0033).  `polytope.py` now restores round-to-nearest after the import and after
every call into the library, a test checks it, and the suite guards the rounding mode
before and after every test.
