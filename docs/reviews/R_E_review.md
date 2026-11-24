# Referee report on workstream E — "second-order classes: how many evaluations are really needed?"

Report under review: `<session scratch>/ws/E/REPORT.md`
(scripts `t01…t20`, `ihs.py`, `so.py`, `sparse.py`, Lean files in `lean/`).
Referee's scratch directory (all my code and outputs): `<session scratch>/referee_E/`.
Nothing in the repository was modified; no `lake build`; no author script was run (I only read `ihs.py`
and some `*.out` files to see what had been computed).  The container was restarted once near the end of
the review (out of memory on the shared machine); all computations listed in §3 had completed and their
outputs survived, nothing was rerun afterwards.

---

## 0. Summary

**No critical error, and no error in any theorem.**  One *major wording error* (a false sentence in a
bolded conclusion; the mathematics behind it is right) and ten minor points.  Every headline statement
that I could test survived a line-by-line re-derivation and an independent numerical check with my own
code:

* **Theorem A (dip)** — correct.  Re-derived (the mixed difference on a 2-face is `±Δ²φ(t₀)` with `t₀` the
  distance on the other coordinates; `Δ²φ = c` for `t₀ ≤ r−2`, `0` for `t₀ ≥ r−1`, including the boundary
  layer `t₀ = r−2`, where `C(2,2) − 2C(1,2) + C(0,2) = 1`).  The three Lean files type-check
  (`lake env lean`, exit 0, axioms `propext, Classical.choice, Quot.sound`), and the Lean statements are the
  prose statements, against the repository's `MixedDiffBound`, for general product spaces.  Brute force
  (all `x`, all pairs, all `r`) for `n ≤ 8`, `k`-state sites in the repository's form, order `m`; LP over the
  whole class: all 255 sets for `n = 3`, all 401 orbits for `n = 4`, random sets `n = 5, 6` — no violation.
* **Theorem B (stars do not combine)** — correct; (b) exact in the LP (error 0 to machine precision) for
  all centre sets `n = 3`, all orbits `n = 4`, random centre sets `n = 5, 6`, and for `k`-state sites;
  (a), (c), (d) also confirmed.
* **Theorem C (sandwich)** — correct as stated, including the last inequality (`ρ₊ ≥ ρ₋` pointwise, so a
  `ρ₋`-code is a `ρ₊`-code and `K₊ ≤ K₋`; the chain uses the right objects), and the randomised bound
  (it is Theorem 11.22(c) of the theory report applied to the alternatives `g − b_{y, ρ₋(y)+2}`).
* **Asymptotics** — `R₂(λ)` values, the transition at `λ = 1/4`, the two-opposite-stars criterion
  `τ₂(n) = (⌊n/2⌋−1)/2`, `R_m` and the threshold `2^{1−m}/m!`, and the `m = 1` case all check.  My own
  exact-count brackets (binomial layers, `n ≤ 2000`) reproduce the report's table and, for `m = 1`,
  reproduce *to all four digits* the numbers quoted in Theorem 11.9 of the theory report
  (0.2073, 0.1994, 0.1947, 0.1919).
* **Spider / Theorem E** — correct.  The proof of (c) (tree optimality) is complete; I checked every
  intermediate inequality on all 7 809 rooted trees with `n ≤ 11`, and the conclusion on all 20 295 trees
  with `n ≤ 12`; LP over the whole class confirms `w = c(X+I)` for all trees `n ≤ 6` and spiders `n ≤ 9`.
  Exhaustive search over *all* simplices confirms the minimum `n/3` for `n = 3, 4, 5, 6`
  (same counts as the author: 29 / 940 / 104 286 / 40 050 850 simplices).
* **Exact small-`n` data** — the step functions for `n = 3, 4` (exhaustive over all evaluation sets) and
  `n = 5` (two independent methods of mine) are reproduced in every entry; for `n = 6` the entries
  `7 [θ ≥ 2]`, `8 [3/2, 2)`, `9 [5/4, 3/2)` and the bound "`≥ 11` just below `5/4`" are confirmed, upper and
  lower bounds, with my own hitting-set solver.
* **Sparse constants** — the finite-dimensionality statement, the upper bound `κ(G)`, the clique lower
  bound and the density criterion for one star are correct (rank computations and LPs); the chain table
  is correct in every entry.
* **Negative finding** (`r_n(poly) = (1−o(1))·c·n²/8`) — correct (Theorem A + sphere covering bound).

What is wrong or overstated is all at the level of wording, small side remarks and attribution
(Section 2): one **false sentence in a bolded conclusion** (§2.4(a): "all but a `2^{−Θ(√n log n)}` fraction of
the cube must be evaluated" — it is the *evaluated* fraction that is `2^{−Θ(√n log n)}`; the summary's
"essentially everything must be evaluated" inherits the slip), an inaccurate side remark about the
crossover `n = 28`, an ambiguous "equality cases" remark, the identification of `N₂` with the algorithmic
complexity (the argument given is invalid; the statement holds up to `+1`), "also for randomised algorithms" in the summary (only the fractional
bound), and a missing piece of prior art: **Chierichetti–Dasgupta–Kumar, "On additive approximate
submodularity" (arXiv 2010.02912, TCS 2022) already has the `Θ(ε n²)` law for the one-sided local
second-order class** (distance to submodularity exactly `⌊n²/2⌋ε/8`, same extremal quadratic function of
`|S|`); the report lists this paper in its search log but does not say so.  The statements about
*evaluations* (Theorems A–C, E) are not in that literature as far as I could read.

Depth: as the author says, short proofs — a discrete second difference, the anchored remainder, type
covering.  The only argument with some combinatorial content is Theorem E(c).  The work is a complete and
correct answer to §12 item 4 of the theory report, not a deep theorem.

---

## 1. Verdict per statement

Depth: E = elementary (≤ 10 lines), S = short, M = moderate.  Novelty: K = known, R = routine once stated,
N? = not found by me in the literature I could read (see §4 for what that was).

| # | statement (location) | correct? | how checked | depth | novelty | remark |
|---|---|---|---|---|---|---|
| 1 | Lemma 0: consistent values at `y` form an interval of length `≤ 2w_A(y)`, exactly `g(y) ± w_A(y)` for additive `g` (§2.0) | yes | re-derived; LP `r10` (663 pairs, max error `4·10⁻¹⁵`) | E | K (optimal recovery) | — |
| 2 | Lemma 1: LP dual; `w_A(y) < ∞` iff `y ∈ aff(A)`; certificates have `≥ n+1` points (§2.0) | yes | re-derived; LP `r02`: `w = ∞` exactly off the affine hull (3 925 infinite cases among 14 541 pairs, 0 mismatches) | E | R | — |
| 3 | **Theorem A**: `b_{y,r} = c·C(r−d(x,y),2)₊ ∈ C(c)`, support `B(y,r−2)`, `b(y) = c·C(r,2)`; hence `w_A(y) ≥ c·C(d(y,A)+1,2)` (§2.1) | **yes** | re-derived; Lean type-checked and statement compared; brute force `n ≤ 8`, `k`-ary, order `m` (`r01`); LP exhaustive `n=3`, orbit-exhaustive `n=4`, random `n=5,6` (`r02`): 0 violations in 10 616 finite pairs | E | N? (generalises the D32 function of the second referee) | Lean hypothesis `0 ≤ c`; general product spaces |
| 4 | Remarks (iii)–(v) to Theorem A (continuous profiles, weighted/clique form, robust form) | yes | re-derived; (iv) clique form LP `r07` (600 pairs), (v) LP `r10` | E | R | (iii) covers only the family `Φ(Σ t_i[x_i≠y_i])` |
| 5 | **Theorem B(a),(b)**: partial star bound; `w_{N[A₀]}(y) = c·C(d(y,A₀),2)` (§2.2) | **yes** | re-derived; Lean (b) type-checked; LP: all 255 centre sets `n=3`, 401 orbits `n=4`, 250 random `n=5`, 25 random `n=6` (max error `0`); (a): 556 random partial stars, 0 violations | E | N? | Lean has (a) only for a *full* star; (b) for `D ≥ 1` |
| 6 | Theorem B(c): `w_A(y) = c` iff `y` completes a square | yes | dual argument re-derived; LP: 0 mismatches in 10 616 pairs (all sets `n=3`, all orbits `n=4`, random `n=5,6`) | S | N? | — |
| 7 | Theorem B(d): even-weight code has `w ≡ 3c/2` on odd points | yes | both bounds re-derived; LP `n = 3…6` | E | N? | — |
| 8 | **Theorem C** (deterministic): `K₋ ≤ N₂ ≤ (n+1)K₊+1 ≤ (n+1)K₋+1` (§2.3) | **yes** | each inequality re-derived; `K_∓` by my own ILP against exact `N₂`, `n = 4, 5` (`r08`): same numbers as the report (`K₋ = 5,10,10,17,27,31`, `|N[A₀]| = 12,12,12,22,29,32`) | E | N? (given A, B) | holds for value certificates too |
| 9 | Theorem C (randomised): `E#queries ≥ (1−2δ)·Σv / max_a Σ_{d(a,y)≤ρ₋(y)} v` | yes | re-derived (coupling of the runs on `g` and `g − b`); = theory report Thm 11.22(c) | E | R | this is a *fractional* bound, not `K₋` |
| 10 | "`N₂` = instance-wise cost of the best deterministic algorithm" (§2.0) | up to `+1` | re-derived | E | R | see m4 |
| 11 | General-residual sandwich (after Thm C) | yes | re-derived; LP `r10` | E | R | — |
| 12 | Cor. D(a): fixed `θ`: `log₂N₂ = n − Θ_θ(√n log n)`; explicit bounds (§2.4) | yes (`Θ`); leading constant `½√θ` plausible, not proved in the text | explicit bounds re-derived; exact layer counts `n ≤ 4096` (`r03 fixed`) | S | R | the bolded verbal conclusion is false as worded — M1 |
| 13 | Cor. D(b): `lim n⁻¹ ln N₂ = R₂(λ)`; `R₂ > 0` iff `λ < 1/4`; table of values | yes | re-derived; `R₂` values recomputed (0.2948, 0.1731, 0.0783, 0.0306, 0.0070, 0.0003); exact-count brackets `n = 100…2000` (`r03 mf`) | S | N? as a statement; method K (type covering) | upper bound rests on the type covering lemma (cited, not re-proved) |
| 14 | D(c): star iff `θ ≥ (n−1)/2`; two opposite stars iff `θ ≥ (⌊n/2⌋−1)/2`; `star(0)∪{1}` formula; `e^{2δ²n}` bound | yes | exact arithmetic `n < 200`; LP `n = 5,6,7` (`r08`); algebra | E | R | side remark on `n ≤ 27` inaccurate — m1 |
| 15 | D(d) + "negative finding": `c·C(t(n,N)+1,2) ≤ r_n(N) ≤ c·C(t(n,⌊N/(n+1)⌋),2)`; `r_n(poly) = (1−o(1))cn²/8`; small exact values | yes | re-derived; `r₃`, `r₄` reproduced exhaustively (`r05`); sphere-covering numbers (`r09`) | E | N? | convergence to `n²/8` is slow: relative deficit `≈ 2√(2 ln N / n)` |
| 16 | **Theorem E(a)**: `w_{A_T}(y) = c[X_T(y)+I_T(y)]` (§2.5) | **yes** | both bounds re-derived; LP over the whole class: all 81 rooted trees `n = 3…6`, spiders `n ≤ 9` (`r04`) | S | N? | — |
| 17 | Theorem E(b): balanced 3-spider has `max_y w/|y| = c n/3` | yes | algebra re-derived; exact for `n = 3…60`; LP `n ≤ 9` | E | N? | — |
| 18 | Theorem E(c): every tree simplex has `max_y w/|y| ≥ c n/3`, witness `U` | **yes** | proof checked line by line; every intermediate inequality on 7 809 trees (`r12`); conclusion and witness on all 20 295 trees `n ≤ 12` (`r04`) | M | N? | the one argument with content |
| 19 | Conjecture E′ evidence (all simplices, `n ≤ 6`; annealing `n ≤ 10`) | reproduced `n ≤ 6` | my own exhaustive enumeration, pairwise subclass (`r06`); my own local search `n = 7, 8` (`r11`) | — | — | a conjecture; "optimal for `n ≤ 10` (annealing)" is evidence, not proof |
| 20 | §2.6 step functions `N₂(n;θ,0)` | `n = 3, 4, 5`: yes; `n = 6`: yes for `7 [θ≥2]`, `8 [3/2,2)`, `9 [5/4,3/2)`; the bound "`≥ 11` just below `5/4`" is also confirmed; between 11 and 13 points on `[1, 5/4)` remains open (as the author says) | `n=3,4`: exhaustive (all sets); `n=5`: forced inclusions + exhaustive remainder (`r05`) and my own hitting-set solver (`r17`); `n=6`: LP of the certificates (`r08`), all simplices (`r06`), `r17` | — | — | — |
| 21 | Prop. F(a): class = span of clique monomials (§2.7) | yes | re-derived; rank computation on 7 graphs (`r07`) | E | R/K | — |
| 22 | Prop. F(b): `N₂ ≤ κ(G)`; `κ−1` points never suffice to identify | yes | LP: clique indicators give `w ≡ 0`; 0/280 random `(κ−1)`-sets identify | E | R | needs the indicators translated to a minimiser — m5 |
| 23 | Prop. F(c): clique lower bound, `N₂ ≥ 2^{ω−O(√ω log ω)}` for `f = e|x|` | yes | re-derived; LP (600 random pairs, 0 violations) | E | R (given A) | instance-specific |
| 24 | Prop. F(d): one star certifies iff max-density condition; `K_{1,m}` example | yes | LP: threshold `= m/(m+1)`; 5 random weighted graphs: LP = brute-force density | E | R | — |
| 25 | Chain table (§2.7) | `n = 3, 4`: yes; `n = 5`: yes | exhaustive (`r07`): all sets `n = 3, 4`; all 104 286 simplices + the claimed sets `n = 5` | — | — | — |
| 26 | §2.8 pairwise subclass (b), (c) | (b) plausible; (c) not checked | (b): steps re-derived (vertex count, cut norm via Khintchine–Szarek gives `3n^{3/2}/64 ≥ n^{3/2}/(32√2)`); no numerics | S | N? | labelled "sketch" by the author |
| 27 | Theorem G (order `m`; `k` states) (§2.9) | yes | re-derived; brute force (`r01`); LP `m = 3`, `n = 5, 6` (`r08`); exact-count brackets `m = 3`; `m = 1` against Thm 11.9 | E | R (given A–C) | — |
| 28 | Lean claims (§3) | yes | type-checked, statements compared | — | — | table row says "B(a)": full star only; "no warnings" holds for `StarsDoNotCombine.lean` (one linter warning in `SecondOrderDip.lean`); 246 lines, not 220 |
| 29 | Prior-art assessment (§4) | incomplete | see §4 | — | — | CDK 2020 not credited for the `n²` law — m7 |

---

## 2. Errors and gaps

### CRITICAL
None.

### MAJOR
**M1. A false sentence in a bolded conclusion (§2.4(a), last sentence; repeated in §1).**
The report writes: "*So with dense constants of order one the second-order class does not help at all at
the exponential scale: all but a `2^{−Θ(√n log n)}` fraction of the cube must be evaluated*", and in §1
"`log₂N₂ = n − Θ(√n·log n)` — essentially everything must be evaluated".
What is proved is `N₂ = 2^{n − Θ(√n log n)}`, i.e. **the evaluated fraction `N₂/2ⁿ` is
`2^{−Θ(√n log n)}` → 0** — the opposite of "all but a `2^{−Θ(…)}` fraction".  (My exact counts: `θ = 1`,
`n = 1024`: `179.0 ≤ n − log₂N₂ ≤ 195.0`, i.e. a `2^{−179}` fraction of the cube suffices.)
*Correct statement:* "the exponent is the full one, `n⁻¹ log₂ N₂ → 1`: a `2^{−Θ(√n log n)}` fraction of the
cube is necessary and sufficient".  The mathematics (formulas, bounds) is right; only the sentence is
wrong, but it is the sentence most likely to be copied into the theory report.  I classify it as major
for that reason only; the fix is one line.

### MINOR
**m1. Crossover of `star(0) ∪ {1}` and the spider (§2.4(c), §2.11 item 7).**  "its threshold is below
`n/3` for `n ≤ 27`" and "the spider is better from `n = 28` on" are both inaccurate.  With
`T(n) = max_w min(C(w,2), C(n,2)−C(w,2))/w` (exact arithmetic, `r08`):
`T(n) < n/3` for `n ≤ 20` and `n ∈ {22, 23, 25, 26, 29, 32}`; `T(n) = n/3` for
`n ∈ {21, 24, 27, 30, 33, 36, 39}`; `T(n) > n/3` for `n ∈ {28, 31, 34, 35, 37, 38}` and all `n ≥ 40`
(checked to 200).  So e.g. at `n = 29` and `32` the set `star(0)∪{1}` is still strictly better than the
spider's `n/3`, and at `n = 21, 24, 27` it is not below but equal.  Asymptotic statement
(`1/(2√2) > 1/3`) unaffected.

**m2. "Equality cases include the spiders `(s+N, s, s−N)`" (§2.5, Verification).**  True as equality in the
*witness* inequality `X(U)+I(U) ≥ (n/3)|U|`, false if read as "these spiders are optimal trees": for
`n = 9` the spider `(5,3,1)` has `max_y (X+I)/|y| = 4 > 3`, and `(6,4,2)` has `5 > 4` for `n = 12`.  The
optimal trees are exactly one for `n ≢ 0 (mod 3)` and two for `n ≡ 0` (the spiders `(m,m,m)` and
`(m+1,m,m−1)`), `n ≤ 12` (`r04`); so the remark is right only for `N ≤ 1`.

**m3. Summary: "`K₋ ≤ N₂ ≤ … ` (Theorem C), also for randomised algorithms".**  For randomised algorithms
only the fractional (packing) bound `(1−2δ)·Σv/max_a Σ_{ball} v` is proved — correctly stated in Theorem C
itself.  It is within a factor `1 + n ln 2` of `K₋`, not equal to it.

**m4. `N₂` versus the algorithmic complexity (§2.0, "Certificates").**  `N₂` is defined through *point*
certificates (`min(f+L_A) ≥ min_A E − ε`).  In the model of the theory report (§11.10: the algorithm
returns a number) the instance complexity is the size of a *value* certificate
(`sup_h min(f+h) − inf_h min(f+h) ≤ ε` over consistent `h`).  The exchange lemma that gives
`N_value = N_point` in the first-order class (Theorem 11.5) is not available here, and the parenthetical
argument "an algorithm that stops on `g` after querying a non-certificate is wrong on some consistent `h`"
is false as stated.  *Counterexample to the argument:* `n = 2`, `c = 1`, `g = 0`, `f = (10, 10, 10, 0)` on
`(00, 10, 01, 11)`, `ε = 2`, `A = {00, 10, 01}`: every consistent `h` has `min(f+h) = h(11) ∈ [−1, 1]`, so
stopping after `A` and returning `0` (or the lower bound `−1`) is correct on the whole class, although
`A` is not a point certificate (`min_A E − LB = 11`).  (Here another 3-point set, `{11, 10, 01}`, *is* a
point certificate, so the number is not affected; in an exhaustive comparison on 180 random instances
with `n = 3` (`r13`) I found `N_value = N_point` every time.)  What is true in general:
`N_value ≤ N₂ ≤ N_value + 1` (add a minimiser), and **both bounds of Theorem C hold for `N_value`**
(the dip argument gives `K₋ ≤ N_value` directly).  No result changes.

**m5. Proposition F(b), "`N₂ ≤ κ(G)` for every instance".**  The clique indicators identify `h`, but a
point certificate also needs an `ε`-optimal evaluated point; take the translated set
`{x* ⊕ 1_K}` (the class is invariant under coordinate flips), or write `κ(G) + 1`.  Trivial, unstated.

**m6. "The cost is governed by the clique complex, not by treewidth or degree" (§1, §2.7).**  Proved:
`N₂ ≤ κ(G)` (so bounded degree *or* bounded treewidth do give polynomial cost: `κ ≤ 1+n2^Δ`,
`κ ≤ 1+n2^{tw}`) and `N₂ ≥ 2^{ω−o(ω)}` *for the instance `f = e|x|`, `g = 0`, fixed `e/c₀`*.  This is a
coarse two-sided statement only in the sense "polynomial if `ω = O(1)`, super-polynomial if
`ω ≫ log n`".  For triangle-free graphs the bounds are `n+1` and `1+n+|E|` and the truth is open (the
author says so in §5.5); "on a chain … `n+1` or `n+2` in all cases computed" means `n ≤ 5`.

**m7. Prior art for the quadratic law (§2.10, §4).**  The sentence "Locally modular functions are not
close to modular ones (`c·C(|x|,2)`)" should cite Chierichetti–Dasgupta–Kumar (arXiv 2010.02912,
Theorems 3 and 14): for the *one-sided* form of exactly this class (`𝒞^cross`: second-order differences
`≥ −ε`) the distance to submodularity is exactly `⌊n²/2⌋ε/8`, with witness `(n−2|S|)²/8 = C(|S|,2)` + affine.
That witness has all mixed differences equal to `1`, so it lies in the two-sided class as well: the
`Θ(c n²)` distance of the dense second-order class from modular functions is a corollary of their Theorem 14.
The report's `c n²/8` is a different quantity (radius of information with polynomially many queries), and
Theorems A–C are not in that paper; but the `n²` scaling of the *class* is prior art and the paper is
only listed, as "(S) search summary", in the log.

**m8. "optimal … among all simplices for `n ≤ 6` (exhaustive) and `n ≤ 10` (annealing)" (§1).**  For
`7 ≤ n ≤ 10` this is the failure of a heuristic search to find a counterexample, in the pairwise subclass.
(My own local search, a different method, also found nothing below `n/3` for `n = 7, 8`.)

**m9. Lean bookkeeping (§3).**  The table row "Theorems A and B(a),(b)" should read "A, B(a) for a full
star, B(b)" (the text below the table says so).  `stars_do_not_combine` does not require `a⋆ ∈ A₀` (a
harmless generalisation) and assumes `D ≥ 1`.

**m10. Leading constant in D(a).**  "`n − log₂N₂ = (1+o(1))·log₂V(n,√(θn)) ~ ½√(θn) log₂n`" is asserted
with "the layers near `n/2` dominate"; the explicit bounds in the text only give constants between
`½√(θ/2)` and `½√(2θ)`.  The claim is true (take weight-`< n/2 − t` points as their own centres with
`t = n^{3/4}(θ ln²n)^{1/4}` and use the radius of the layer `n/2 − t` for the rest), but the argument is not
written.  Note also that the convergence is logarithmic: at `n = 4096`, `θ = 1` the ratio of the deficit to
`½√(θn)log₂n` is still between 1.16 and 1.21 (1.26–1.35 for `θ = ¼`).

### Not errors, but to be kept in mind when the results are reused
* Theorems A–C are for *dense* constants and (lower bounds) an *additive* true residual; for a residual on
  the boundary of the class the lower bound is void (stated by the author, §5.4).
* The upper bound of D(b) and of Theorem G uses the type covering lemma as a black box (as Theorem 11.9
  of the theory report does).
* `ε` in the randomised statement is a one-sided width; the repository's convention (`ε/2`-correct,
  two-sided) corresponds to the author's "read `2ε`".

---

## 3. Independent numerical checks (all code mine; directory `referee_E/`)

LPs: `scipy.optimize.linprog` (HiGHS) on the full cube, variables `h(x)`, two inequalities per 2-face
(`ref_lp.py`).  Exact integer / rational arithmetic wherever no LP is involved.

| script → output | what | size | result |
|---|---|---|---|
| `r01_dip_bruteforce.py` | dip `C(r−d,2)₊`: every 2-face, every `r ≤ n+3`; all centres for `n ≤ 6`, 3 centres for `n = 7, 8`; predicted value `|D_iD_jb| = 1[t₀ ≤ r−2]`; support; `k`-ary sites in the repository's form (all `x`, `i≠j`, `a`, `b`); order-`m` dips | 266 760 binary (face, centre, r) triples; 1 072 038 `k`-ary differences, `(n,k) ≤ (4,3),(3,4),(2,5)`; `(n,m)` up to `(8,4)`, `(7,5)` | 0 mismatches, 0 violations |
| `r02_lp_theoremAB.py` | Theorem A, B(a)–(d), Lemma 1 by LP | A: all 255 sets `n=3`; 401 hyperoctahedral orbits `n=4`; 400 random sets `n=5`; 40 random `n=6` (14 541 pairs, 10 616 finite). B(b): 255 + 401 + 250 + 25 centre sets (6 058 unevaluated points). B(a): 556 partial stars. B(d): `n=3…6` | 0 violations of `w ≥ C(d+1,2)` (tight in 4 739 cases); `w = ∞` iff outside the affine hull; B(b) error `0`; square criterion: 0 mismatches; next value above `c` is `3c/2`; even code `≡ 3/2` |
| `lean/typecheck.log` | `lake env lean` on copies of the three Lean files | — | all exit 0 (27 s, 26 s, 5 s); axioms `[propext, Classical.choice, Quot.sound]`; one linter warning in `SecondOrderDip.lean` |
| `r03_asymptotics.py` (`m1`, `mf`, `fixed`, `m3`) | Theorem C/G brackets by exact layer counts: lower `max_w C(n,w)/max_u cover(u,w,ρ₋)`, upper `V(n,m−1)·Σ_w K_w + 1` with the Lovász–Stein bound per layer; log-domain floats validated against exact integers and brute force | `m=1`: `n ≤ 800`; `m=2` mean field: `n = 100…2000`, 8 values of `λ`; fixed `θ ∈ {¼,1,4}`: `n ≤ 4096`; `m=3`: `n ≤ 800` | see below |
| `r04_trees.py`, `r12_treeproof_steps.py` | Theorem E: LP vs `X+I`; all rooted trees; proof steps | LP: 81 trees `n ≤ 6`, spiders `n = 3…9`; combinatorics: 20 295 trees `n ≤ 12`; proof steps: 7 809 trees `n ≤ 11` | LP error `≤ 4·10⁻¹⁵` (trees), `≤ 7·10⁻¹⁴` (spider `n = 9`); `min_T max_y = n/3` for every `n`; witness never fails; every intermediate inequality holds |
| `r05_small_exact.py` | exact `θ_N` and `r_n(N)` | `n=3`: all 99 sets `∋ 0` with `≥ 4` points; `n=4`: one representative of each of the 1 935 `S₄`-orbits of sets `∋ 0` with `≥ 5` points (same orbit counts as the author: 30 and 1 935; 28 + 1 868 = 1 896 spanning); `n=5`: forced inclusions + exhaustive remainder | tables of §2.6 and §2.4(d) reproduced for `n = 3, 4`; `n = 5`: see below |
| `r06_simplices.py` | all simplices `∋ 0`, pairwise-subclass threshold (a lower bound for the full class) | `n = 3, 4, 5, 6` (29, 940, 104 286, 40 050 850 simplices) | minimum `= n/3` exactly; minimisers 7, 12, 60, 850 — see below |
| `r07_sparse.py` | Prop. F and the chain | 7 graphs `n = 5, 6`; chain `n = 3, 4` all sets, `n = 5` all simplices | see below |
| `r08_misc.py` | `K_∓` by ILP; designs; crossover; order 3 | `n = 4…7` | all values of the report reproduced except the `n ≤ 27` remark (m1) |
| `r09_supnorm.py` | sphere-covering form of the negative finding | `n ≤ 10⁴`, `N = 2n+2, n³, n¹⁰` | lower bound / `(n²/8)` = 0.66 (`n=10³`, `N=n³`), 0.86 (`n=10⁴`, `N = n³`) |
| `r10_general_residual.py` | Lemma 0, Remark (v), general-residual bound | 663 pairs, `n = 4, 5` | 0 violations |
| `r11_simplex_search.py` | adversarial local search for a simplex below `n/3` | `n = 7, 8` | none found — see below |
| `r17_ihs_n6.py` | my own implicit-hitting-set solver (LP-verified cuts + `S_n` images, MILP master) | `n = 4` (6 breakpoints), `n = 5` (7 breakpoints, both directions), `n = 6` (`N ≤ 8`, `≤ 9`, `≤ 10`) | reproduces the exhaustive `n = 4` table; proves the `n = 5` row; `n = 6`: see below |
| `r15_n6_falsify.py` | local search for an `N`-point certificate below the claimed `θ_N(6)` (full-class LP) | `N = 8, 9, 10`, 700 s each | none found: the least thresholds reached are `3/2`, `5/4`, `5/4`, i.e. exactly the claimed values (`star(0)∪{1}`; `star(0)∪{1, 1−e_i}`; a 10-point set at `5/4`) |
| `r18_chain_trees.py` | chain: all labelled tree simplices against the star | `n = 4, 5, 6` (125, 1 296, 16 807 trees) | none below `(n−1)/n` |
| `r13_value_vs_point.py` | least value certificate vs least point certificate, all subsets | `n = 3`, 180 random instances `(f, ε)` | equal in all cases (m4) |
| `r16_thmC_general_f.py` | Theorem C with *arbitrary* `f`, additive `g`, `ε ∈ {0,…,2}`: exact `N₂` over all 255 subsets against `K_∓` | `n = 3`, 3 000 random instances | 0 violations of `K₋ ≤ N₂ ≤ (n+1)K₊+1`, `K₊ ≤ K₋` |
| `r14_kary_lp.py` | `k`-state sites, LP in the repository's form: Theorem A on random sets, Theorem B(b) on unions of full stars | `(n,k) = (2,4), (3,3), (4,3), (3,4)` | B(b) exact (794 points); A: 0 violations in 170 pairs |

**Asymptotics (item 4).**  `R₂(λ)` on a grid of `2·10⁶` points: 0.29476, 0.17313, 0.07832, 0.03064, 0.00705,
0.00027 at `λ = 0.02, 0.05, 0.1, 0.15, 0.2, 0.24`; `0` at `λ ≥ 1/4`.  Rigorous brackets
`lo ≤ n⁻¹ ln N₂ ≤ up` from my code (`lo` uses only `K₋`; the report's table uses `max(K₋, n+1)`):

| `λ` | `R₂` | `n = 100` | `n = 400` | `n = 800` | `n = 1600` | `n = 2000` |
|---|---|---|---|---|---|---|
| 0.02 | 0.2948 | 0.3310 – 0.4137 | 0.3060 – 0.3351 | 0.3008 – 0.3175 | 0.2980 – 0.3074 | 0.2974 – 0.3052 |
| 0.05 | 0.1731 | 0.2036 – 0.2974 | 0.1832 – 0.2149 | 0.1786 – 0.1966 | 0.1760 – 0.1862 | 0.1755 – 0.1839 |
| 0.10 | 0.0783 | 0.1047 – 0.2055 | 0.0864 – 0.1206 | 0.0829 – 0.1021 | 0.0809 – 0.0915 | 0.0804 – 0.0892 |
| 0.15 | 0.0306 | 0.0522 – 0.1570 | 0.0375 – 0.0728 | 0.0346 – 0.0543 | 0.0328 – 0.0438 | 0.0324 – 0.0415 |
| 0.20 | 0.0070 | 0.0228 – 0.1285 | 0.0122 – 0.0482 | 0.0100 – 0.0303 | 0.0087 – 0.0199 | 0.0084 – 0.0177 |
| 0.24 | 0.0003 | 0.0087 – 0.1008 | 0.0030 – 0.0370 | 0.0018 – 0.0214 | 0.0011 – 0.0122 | 0.0010 – 0.0102 |
| 0.25 | 0 | 0.0069 – 0.0923 | 0.0017 – 0.0300 | 0.0009 – 0.0167 | 0.0004 – 0.0092 | 0.0003 – 0.0076 |

The lower brackets agree with the report's to all printed digits (`n = 100, 200, 400`); `lo − R₂` decays
like `≈ 0.5·ln n / n`.  Two opposite stars certify (exact integer test, all layers) for `λ = 0.25, 0.3`
and fail for `λ ≤ 0.24`, at every `n` tried; `τ₂(n) = (⌊n/2⌋−1)/2` holds for all `2 ≤ n < 200`.
At `λ = 0.24` the exponent `2.7·10⁻⁴` is invisible below `n ≈ 10⁴` — the transition is sharp only in the
limit (as the author notes, the window has width `Θ(√(n log n))` in `θ`).

`m = 1` (first-order class, `ρ = e/c = ½`): `R₁ = 0.18823` at `ω = 0.2929`; my lower bracket
`n⁻¹ ln max_w C(n,w)/max_u cover` gives **0.2073, 0.1994, 0.1947, 0.1919** for `n = 100, 200, 400, 800` —
exactly the four numbers quoted after Theorem 11.9 of the theory report.  `ρ = ¼, ¾, 0.9`:
`R₁ = 0.3509, 0.0798, 0.0293` (brackets at `n = 400`: 0.359–0.377, 0.087–0.108, 0.036–0.058).

`m = 3`, `c = γ/n²`: `R₃ = 0.0773, 0.0256, 0.0029, 0, 0` at `λ = 0.01, 0.02, 1/30, 1/24, 0.05`; brackets at
`n = 800`: 0.0824–0.1080, 0.0297–0.0564, 0.0053–0.0329; two opposite radius-2 balls certify exactly for
`λ ≥ 1/24` (`n = 100…800`), as claimed (`2^{1−m}/m! = 1/24`).

Fixed `θ` (deficit `n − log₂N₂`, rigorous brackets; last column `½√(θn)log₂n`):

| `θ` | `n` | `n − log₂N₂` (rigorous bracket) | `log₂V(n,⌊√(θn)⌋)` | `½√(θn)log₂n` | deficit / `½√(θn)log₂n` | deficit / `log₂V` |
|---|---|---|---|---|---|---|
| 0.25 | 64 | 8.0 – 16.9 | 19.4 | 12.0 | 0.663 – 1.405 | 0.412 – 0.871 |
| 0.25 | 256 | 33.1 – 44.3 | 48.6 | 32.0 | 1.033 – 1.383 | 0.681 – 0.912 |
| 0.25 | 1024 | 95.8 – 109.6 | 115.6 | 80.0 | 1.198 – 1.370 | 0.829 – 0.948 |
| 0.25 | 2048 | 153.2 – 168.9 | 171.9 | 124.5 | 1.231 – 1.357 | 0.891 – 0.983 |
| 0.25 | 4096 | 242.0 – 258.6 | 266.2 | 192.0 | 1.260 – 1.347 | 0.909 – 0.971 |
| 1.00 | 64 | 19.2 – 29.0 | 32.3 | 24.0 | 0.798 – 1.209 | 0.594 – 0.898 |
| 1.00 | 256 | 65.3 – 78.1 | 83.2 | 64.0 | 1.021 – 1.221 | 0.785 – 0.939 |
| 1.00 | 1024 | 179.0 – 195.0 | 201.7 | 160.0 | 1.119 – 1.219 | 0.887 – 0.967 |
| 1.00 | 2048 | 284.3 – 301.5 | 308.0 | 248.9 | 1.142 – 1.211 | 0.923 – 0.979 |
| 1.00 | 4096 | 443.6 – 462.8 | 471.3 | 384.0 | 1.155 – 1.205 | 0.941 – 0.982 |
| 4.00 | 64 | 34.7 – 46.6 | 49.3 | 48.0 | 0.724 – 0.972 | 0.704 – 0.945 |
| 4.00 | 256 | 115.0 – 130.1 | 135.6 | 128.0 | 0.899 – 1.016 | 0.848 – 0.959 |
| 4.00 | 1024 | 314.0 – 331.9 | 341.2 | 320.0 | 0.981 – 1.037 | 0.920 – 0.973 |
| 4.00 | 2048 | 499.8 – 519.1 | 528.2 | 497.8 | 1.004 – 1.043 | 0.946 – 0.983 |
| 4.00 | 4096 | 782.6 – 803.3 | 817.0 | 768.0 | 1.019 – 1.046 | 0.958 – 0.983 |

So the deficit is `Θ(√n log n)` with the predicted leading behaviour: for `n ≥ 2048` it lies between 0.89
and 0.98 of `log₂V(n, ⌊√(θn)⌋)`, and the ratio to `½√(θn)log₂n` drifts towards 1 at the logarithmic rate
`1 + 2log₂(e/√θ)/log₂n` (the report's `t05` numbers for `θ = 1`, `n = 1024`, `[176.6, 195.0]`, agree with
my `[179.0, 195.0]`: same lower bound for `N₂`, slightly different upper bound).

**Small exact data (§2.6).**  `n = 3`: `θ₄ = 1, θ₅ = θ₆ = ½, θ₇ = ⅓`; `n = 4`: `θ₅ = 4/3, θ₆ = 1,
θ₇ = θ₈ = 2/3, θ₉…₁₁ = ½, θ₁₂…₁₄ = ⅓, θ₁₅ = ¼` — the report's two rows exactly;
`r₃(4) = 3/2`, `r₃(5…7) = 1`, `r₄(5) = 3`, `r₄(6) = r₄(7) = 2`, `r₄(8…15) = 1` as reported.
`n = 5`: two independent methods of my own (a point with `θ|y| < 1` must be evaluated, so the search space
collapses).
(i) Exhaustive (`r05`, `r06`): `θ₆(5) = 5/3` (all 104 286 simplices, pairwise lower bound, + spider LP);
`star(0)∪{1}` has threshold 1; among the 14 950 sets `star(0)` + 4 points the least threshold is exactly 1
(325 pass the Theorem-A filter), so **no set with ≤ 10 points certifies below 1**; among the 65 780 sets
`star(0)` + 5 points the least threshold is exactly `2/3` (two stars minus a centre), so `θ₁₁(5) = 2/3` and no
11-point set certifies below `2/3`; two opposite stars: `½`.  (I stopped this run after these three searches.)
(ii) My own implicit-hitting-set solver (`r17`: cuts = complements of maximal non-certificates, each verified
by LP, plus their `S_n`-images; master MILP with zero gap; it reproduces my exhaustive `n = 4` table):
no certificate with `≤ 6, 10, 11, 20, 26, 30, 31` points at `θ = 1.6665, 0.9999, 0.6665, 0.4999, 0.3332, 0.2499,
0.1999`, and minimum certificates of sizes `6, 7, 11, 12, 21, 27, 31` at
`θ = 1.66667, 1.00001, 0.66667, 0.50001, 0.33334, 0.25001, 0.20001`.
Hence the report's row `6 | 7 | 11 | 12 | 21 | 27 | 31 | 32` with breakpoints `5/3, 1, 2/3, ½, ⅓, ¼, 1/5` is
correct (to the resolution `10⁻⁴` in `θ` for the last four breakpoints).

`n = 6`: certificates of the report verified by LP (spider 2; `star(0)∪{1}`: 3/2;
`star(0)∪{1, 1−e₆}`: 5/4; two stars minus a centre, 13 points: 1; non-tree simplex: 2); family `A_k`:
`3/2, 5/4, 5/4, 5/4, 5/4, 1, 1` (`n = 6`), `2, 8/5, 8/5, 8/5, 8/5, 8/5, 5/4, 1` (`n = 7`) — as reported.
Lower bounds, with my own hitting-set solver (`r17`): **no certificate with ≤ 8 points at `θ = 1.4999`**
(11 rounds, 4 922 cuts, 166 s) and **none with ≤ 9 points at `θ = 1.2499`** (8 rounds, 3 207 cuts, 60 s); so
`θ₇(6) = 2`, `θ₈(6) = 3/2`, `θ₉(6) = 5/4` are all confirmed independently.  And **none with ≤ 10 points at
`θ = 1.2499`** (12 rounds, 4 617 cuts, 190 s): the author's "at least 11 just below 5/4" is confirmed too.  An independent local search for certificates *below* the claimed thresholds
(`r15`, full-class LP, 700 s each for `N = 8, 9, 10`) found nothing better than `3/2`, `5/4`, `5/4`.
I also read `ihs.py`: its cuts are valid (a superset-maximal non-certificate must be left by every
certificate; symmetric copies; master solved with zero gap).

**All simplices (Conjecture E′).**
Minimum over all simplices `{0, a₁,…,a_n}` of the pairwise-subclass threshold `max_y w^{pair}_A(y)/|y|`
(closed form; a lower bound for the full class):

| `n` | `n`-subsets of non-zero points | simplices | minimum | minimisers | orbits under `S_n` |
|---|---|---|---|---|---|
| 3 | 35 | 29 | 1 | 7 | 2 |
| 4 | 1 365 | 940 | 4/3 | 12 | 1 |
| 5 | 169 911 | 104 286 | 5/3 | 60 | 1 |
| 6 | 67 945 521 | 40 050 850 | 2 | 850 | 3: spiders (2,2,2), (3,2,1), and `{0, e₁+e₂, e₁+e₃, e₂+e₃, e₄+e₅, e₄+e₆, e₅+e₆}` |

No simplex is below `n/3`; every count coincides with the author's (`t04`).  Since the spider attains `n/3`
in the full class (LP), `θ_{n+1}(n) = n/3` for `n ≤ 6`.  The non-tree simplex has full-class threshold 2 (LP).
Local search for a counterexample (`r11`; first-improvement with random restarts, move = replace one point;
`4.6·10⁶` evaluations for `n = 7`, `7.3·10⁶` for `n = 8`): the least local optimum is exactly `n/3`
(reached in 541 of 3 782 restarts for `n = 7`, 182 of 2 116 for `n = 8`), never below; the best simplices
found are spiders with legs `(3,2,2)` and `(3,3,2)`.

**Sparse constants.**  `dim{h : D_iD_jh ≡ 0 off E}` = number of cliques for chain₅ (10), cycle₅ (11),
`K₃,₃` (16), `K₄`+pendant (18), triangle+path (12), `K₅` (32), `K₁,₄` (10); clique indicators give
`w ≡ 0`; the star gives `Σ_{edges in y} c_e` exactly; clique bound: 0 violations in 600 random pairs;
`K_{1,m}`: star threshold `m/(m+1)` (`m = 2…5`).
Chain (`c = 1` on edges `i, i+1`; `θ_N` = least threshold of an `N`-point set `∋ 0`): `n = 3`:
`θ₄ = 2/3` (star), `θ₅ = ½`, `θ₆ = 0`; `n = 4`: `θ₅ = ¾` (star), `θ₆ = θ₇ = ½`, `θ₈ = 0` (all sets, clique-space
LP validated against the full-cube LP); `n = 5`: over all 104 286 simplices the least threshold is `2/3`
(star: `4/5`), the two 6-point sets of the report have thresholds `2/3` and `3/4`, the 7-point set `½`.
Hence the report's chain table (5/4/4/4, 6/6/5/5, 7/6/6/6) is correct in every entry.  The remark "tree
simplices cannot do this on a chain" is confirmed for `n = 4, 5, 6`: over all 125 / 1 296 / 16 807 labelled
tree simplices the least threshold is the star's `(n−1)/n` (`r18`).

---

## 4. Literature

What I read (the web-search budget shared by the session ran out after these; I could not run further
searches):

* **Feige–Feldman–Talgam-Cohen, "Approximate modularity revisited"** (arXiv 1612.02034) — full text on
  ar5iv through the summariser, two passes (both halves), with verbatim quotes requested.  Content:
  `ε`-modular = defect `≤ ε` for *all* `S, T` (weakly: disjoint `S, T`); such functions are `O(ε)`-close to
  linear (Kalton–Roberts); `O(n)` non-adaptive queries learn to `O(Δ√n)`; the lower bound
  `Ω(Δ√n/log n)` for polynomially many queries is attributed to Chierichetti–Das–Dasgupta–Kumar and
  re-proved (Thm D.1: a perturbation supported on unbalanced sets, which polynomially many queries miss).
  **No local / second-order variant, no `n²` law, nothing like Theorems A/B.**  The report's quotations
  from this paper are accurate.
* **Chierichetti–Das–Dasgupta–Kumar, "Approximate modularity", FOCS 2015** — *not read* (no accessible
  text found; only what FFT and search summaries say about it: uniform `ε`-modularity, `O(ε log n)`
  closeness, a randomised `O(n² log n)`-query learner, the `√n/log n` lower bound).  I cannot exclude that
  it discusses a second-order (marginal) definition.
* **Chierichetti–Dasgupta–Kumar, "On additive approximate submodularity"** (arXiv 2010.02912; TCS 2022
  per a repository record) — arXiv abstract plus full text on ar5iv through the summariser, two passes
  with verbatim theorem statements requested.  Content relevant here: three constraint sets, among them
  `𝒞^cross` = "cross second-order derivatives" `f(A+a₁)+f(A+a₂) ≥ f(A+a₁+a₂)+f(A) − ε` — the one-sided
  version of the class of this workstream; Theorem 3: distance to submodularity `≤ ⌊n²/2⌋ε/8`;
  Theorem 14: this is attained, witness `(n−2|S|)²/8`; footnote: `𝒞^cross` is the minimal constraint set
  with finite distance.  No query/evaluation results.  **So the `Θ(εn²)` scaling for locally (second-order)
  approximately sub/modular functions, with the quadratic-in-`|S|` extremal function, is known**; the
  two-sided statement "dense second-order class is `Θ(cn²)` from modular" follows from their Theorem 14.
* **Amireddy–Behera–Paraashar–Srinivasan–Sudan** (arXiv 2403.20305) — abstract only; the report's
  description (`Õ(log n)` queries, constant fraction of corruptions) is accurate.
* Search summaries only (no text read): optimal recovery on the Boolean cube with bounded mixed
  differences / covering codes — nothing found; Sukharev's theorem — not located, only secondary
  mentions; Ling–Gu arXiv 2510.15277 (continuous second-order optimal recovery with sphere coverings).
  Not checked at all: Krivelevich–Sudakov–Vu, Kalton–Roberts, Choi et al., Babenko–Borodachov–Skorokhodov.

Novelty assessment.
* *Known*: the anchored remainder (theory report / KSWW); radius of information; covering picture for
  Lipschitz classes; type covering; the `n²` law for the distance of the local second-order class from
  (sub)modular functions (CDK 2020) and, inside the project, the function `−c·C(|x|−1,2)` and the
  two-opposite-stars example of the second referee (D32) — the dip is the natural common generalisation.
* *Not found by me* (within the reading above): the dip bound `w_A(y) ≥ c·C(d(y,A)+1,2)` for arbitrary
  evaluation sets, exactness for unions of stars, the covering sandwich and the exponents `R₂`, `R_m`, the
  tree-simplex formula with the `n/3` optimum.  These are statements about *evaluations*, absent from the
  approximate-modularity papers I read, whose query results concern the uniform class (`√n` scale).
  The CDDK/FFT lower-bound mechanism (a perturbation invisible to polynomially many queries) is the same
  idea as the report's negative finding; the report's version is quantitatively different (`n²/8` instead
  of `√n`) because the class is local.
* The author's own assessment ("one complete answer and one design problem with a clean conjecture, not a
  deep theorem") is fair.

---

## 5. Not checked

* The `n = 6` step function below `θ = 5/4` beyond the bound "`≥ 11`" (the author's runs are unfinished
  there; that 13 points suffice for `θ ≥ 1` is verified).  All `n = 6` lower bounds are established at the
  test values `θ = 1.4999, 1.2499` (resolution `10⁻⁴`), with LP tolerance `10⁻⁷`.
* The author's annealing for `n = 9, 10` (I ran an independent local search for `n = 7, 8` only).
* §2.8(c) (sets containing `star(0)` need `Ω(n)` extra points below `1/(2√2)`) — a sketch, not examined;
  §2.8(b) — the steps were re-derived on paper, the constants only roughly, no numerics.
* `η > 0` tables (`t02_n3.out`, `t02_n4.out`) except the single caveat example (`n = 4`, `η = ½`: 1 against
  7/6, confirmed).
* The type covering lemma (uniformity in the type) — used as a black box, as in the theory report.
* The `k`-state version of Theorem C (only Theorems A and B(b) were tested for `k > 2`: Lean statement,
  brute-force membership of the dip, and a `k`-ary LP for four small `(n,k)`).
* The chain for `n = 6` (beyond tree simplices); triangle-free graphs other than the chain.
* Literature: the FOCS 2015 paper of Chierichetti et al. itself; Kalton–Roberts; Krivelevich–Sudakov–Vu;
  Sukharev; anything beyond the searches listed in §4 (search budget exhausted).
