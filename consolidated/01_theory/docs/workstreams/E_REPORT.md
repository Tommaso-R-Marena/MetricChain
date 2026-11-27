# Workstream E — second-order classes: how many evaluations are really needed?

Directory: `<session scratch>/ws/E/`
(all scripts `t*.py`, `so.py`, `sparse.py`, `ihs.py` and their outputs `*.out` are here; nothing in the
repository was touched).

Status labels: **[K]** known (cited), **[R]** routine once stated, **[N]** apparently new (not found in
the searches of §4), **[LP]** verified by linear programming over the whole class, **[Lean]** machine-checked in a scratch
file (§3), **[C]** conjecture.

---

## 1. Verdicts

**The cost under dense constants is exponential, and the covering radius `(2·gap/c)^{1/2}` suggested in
§12 item 4 of the theory report is exactly right.**  Every member of the dense second-order class may be
perturbed by a *second-order dip* `c·C(r − d(x,y), 2)₊` (a class member supported on a Hamming ball), so
for *every* evaluation set `A` the uncertainty at `y` is at least `c·C(d(y,A)+1, 2)` — quadratic in the
Hamming distance to the evaluated set, whatever the shape of `A` (Theorem A).  Stars attain this:
for a union of stars the uncertainty is *exactly* `c·C(d(y, centres), 2)` — stars do not combine
(Theorem B).  Hence the least number of evaluations `N₂` is sandwiched between two covering numbers of
Hamming balls whose radii differ by one, `K₋ ≤ N₂ ≤ (n+1)·K₊ + 1 ≤ (n+1)·K₋ + 1` (Theorem C), also for
randomised algorithms.  (Theorems A and B(b) are machine-checked in Lean against the repository's
`MixedDiffBound`; everything else is a paper proof with LP verification.)  Consequences: for fixed `e/c` (`f = e|x|`, zero residual)
`log₂ N₂ = n − Θ(√n·log n)` — essentially everything must be evaluated; in the natural mean-field scaling
`c = γ/n` there is a sharp transition at `e/γ = 1/4`: above it `2n+2` evaluations (two opposite stars)
suffice, below it `N₂ = exp(n·R₂ + o(n))` with the explicit exponent
`R₂(λ) = max_ω [h(ω) − h(√(2λω))]`, `λ = e/γ` — the same variational formula as the first-order exponent of
the report with the distortion budget replaced by its square root (and by an `m`-th root for order `m`:
`R_m(λ) = max_ω [h(ω) − h((m!λω)^{1/m})]`, polynomial iff `λ ≥ 2^{1−m}/m!`; `m = 1` is the report's
Theorem 11.9 for binary sites).  **New on the positive side:** the star is *not* the best set of `n+1`
evaluations — a three-legged "spider" (three nested chains from `x₀`) certifies whenever `e ≥ c·n/3`,
against `e ≥ c·(n−1)/2` for the star; `n/3` is optimal among all tree-like simplices (proved) and among
all simplices for `n ≤ 6` (exhaustive) and `n ≤ 10` (annealing), so "`N₂ = n+1` iff `e ≥ cn/3`" is the
conjectured exact threshold.  **Sparse constants** are a different world: the class is then
finite-dimensional (spanned by the clique monomials of the coupling graph), the cost is at most the
number of cliques and at least exponential in the clique number — it is governed by the clique complex,
not by treewidth or degree; one star certifies iff a maximum-density-subgraph condition holds (a min-cut,
strictly weaker than the row-sum condition of the report), and on a chain cleverer sets than stars need
only `n+1` or `n+2` evaluations in all cases computed.  **Most important negative finding:** no
choice of evaluation set — covering arrays, random sets, Reed–Muller-type codes, several stars — escapes
the quadratic law; with polynomially many evaluations the residual is determined only to within
`≈ c·n²/8` in sup norm (a factor 4 better than one star and no more).  Not settled: the exact count in the
window `n/4 ≲ e/c < n/3` (at most `2n+2`; at least `n+2` if the simplex conjecture holds), and the
simplex conjecture itself for general `n`.

---

## 2. Precise statements, proofs, counterexamples

### 2.0 Setting and the basic quantity

`X = {0,1}ⁿ` (k-state sites: §2.9).  `D_iD_j h(x) = h(x⊕e_i⊕e_j) − h(x⊕e_i) − h(x⊕e_j) + h(x)`.
`C(c) = {h : |D_iD_j h(x)| ≤ c_ij for all x, i ≠ j}`; *dense*: `c_ij ≡ c`.  `C(0)` = additive (modular)
functions.  For `A ⊆ X`,

    w_A(y) := sup{ h(y) : h ∈ C(c), h = 0 on A }  ∈ [0, ∞]            (a linear program).

`d(·,·)` is the Hamming distance, `C(m,2) = m(m−1)/2` for `m ≥ 2` and `0` otherwise, `star(a)` = `a` and
its `n` neighbours, `N[A₀] = ∪_{a∈A₀} star(a)`.

**Lemma 0 (radius of information) [R].**  For `g ∈ C(c)` and `A ⊆ X`, the set of values
`{h(y) : h ∈ C(c), h|_A = g|_A}` is an interval of length `≤ 2·w_A(y)` containing `g(y)`; if `g` is
additive it is exactly `[g(y) − w_A(y), g(y) + w_A(y)]`.
*Proof.*  `C(c)` is convex and symmetric; if `h₁, h₂` are consistent then `(h₁−h₂)/2 ∈ C(c)` vanishes on
`A`.  If `g` is additive, `h` is consistent iff `h − g ∈ C(c)` vanishes on `A`. ∎
So `w_A` is the radius of information in the sense of optimal recovery (Micchelli–Rivlin;
Traub–Woźniakowski), and it is the second-order analogue of the distance to the evaluated set.

**Lemma 1 (duality) [R].**  `w_A(y) = min{ Σ c_ij|λ_{ij,x}| : δ_y = Σ_{a∈A} μ_a δ_a + Σ λ_{ij,x} D_{ij,x} }`:
the cheapest way to write the evaluation at `y` as a signed affine combination of evaluations on `A` plus
mixed differences.  It is finite iff `y` lies in the real affine hull of `A` (the span of the functionals
`D_{ij,x}` is the annihilator of the affine functions).  In particular **every certificate has at least
`n+1` points**, and since a vertex of the cube is never a convex combination of other vertices,
second-order information on the cube is always *extrapolated* — the reason for everything below.

**Certificates.**  Instance: known `f`, true residual `g ∈ C(c)`, `E = f+g`, `gap(y) = E(y) − min E`.
`A` is an `ε`-certificate iff `min_y [f(y) + L_A(y)] ≥ min_A E − ε`, `L_A(y) = inf{h(y) : h ∈ C(c), h|_A = g|_A}`.
`N₂(f,g,ε)` = least size.  As for the first-order class it is the instance-wise cost of the best
deterministic algorithm that is correct on the whole class (an algorithm that stops on `g` after querying
a non-certificate is wrong on some consistent `h`; conversely "query `A`; if the answers agree with
`g|_A` stop, else evaluate everything" is correct).  For additive `g` (in particular `g = 0`, the case of
the brief): `A` is an `ε`-certificate iff `w_A(y) ≤ E(y) − min_A E + ε` for all `y`.
Normalised problem of the brief: `f = e|x|`, `g = 0`, `θ := e/c`, `η := ε/c`; then (for `η < θ`, which
forces `0 ∈ A`)  `A` certifies iff `w_A(y) ≤ θ|y| + η` for all `y` (units `c = 1`).

### 2.1 Theorem A — second-order dips; the quadratic law  [N] [LP] [Lean]

**Theorem A.**  Dense constants.  For `y ∈ X` and an integer `r ≥ 0` let
`b_{y,r}(x) = c·C(r − d(x,y), 2)₊`.  Then `b_{y,r} ∈ C(c)`, `b_{y,r}(y) = c·C(r,2)`, and `b_{y,r}` vanishes
outside the ball `B(y, r−2)`.  Consequently, for every `A ⊆ X` and every `y`,

    w_A(y)  ≥  c·C(d(y,A) + 1, 2)  =  c·d(d+1)/2 ,   d = d(y,A).

*Proof.*  Write `φ(t) = c·C(r−t,2)₊`.  The four corners of a 2-face in directions `i, j` are at distances
`t₀, t₀+1, t₀+1, t₀+2` from `y` (`t₀` = distance on the other coordinates), the two extreme ones being
diagonal, so `D_iD_j b = ±Δ²φ(t₀)`.  For `t₀ ≤ r−2`, `Δ²φ(t₀) = c` (second difference of `C(·,2)`); for
`t₀ ≥ r−1` all three values vanish.  So `|D_iD_j b| ∈ {0, c}`.  For the bound take `r = d(y,A)+1`: the dip
vanishes on `A`. ∎

*Remarks.*  (i) `r = 2` is the point indicator `c·1[x = y]`: **every unevaluated point has uncertainty at
least `c`**.  (ii) The bound is attained by the star (`d = w−1`: `C(w,2)`), by the radius-2 ball
(`C(w−1,2)`; the referee's function `−c·C(|x|−1,2)` is a dip centred at the far corner) and by every
thickened set (Theorem B).  (iii) More general profiles do not help: for
`h(x) = Φ(Σ_i t_i[x_i ≠ y_i])` one has `|D_iD_j h| ≤ t_i t_j·max|Φ''|`, so
`½c(R − Σ t_i[x_i≠y_i])₊²` with `0 ≤ t_i ≤ 1` is in the class, but `max_t min_{a∈A} Σ_i t_i[a_i ≠ y_i] = d(y,A)`
(the `ℓ₁` distance from a vertex to a convex hull of vertices is attained at a vertex), so half-space dips
give nothing beyond Hamming balls.  (iv) Weighted constants: if `c_ij ≥ t_i t_j` for all `i ≠ j` then
`w_A(y) ≥ ½·min_{a∈A}(Σ_i t_i[a_i ≠ y_i])²`; in particular for a clique `K` of the coupling graph with
`c_ij ≥ c₀` on `K`: `w_A(y) ≥ c₀·C(d_K(y,A)+1, 2)`, `d_K` = Hamming distance on the coordinates in `K` (§2.7).
(v) *Robust form.*  If the true residual `g ∈ C(c′)` with `c′_ij ≤ c_ij − c₀`, then `g − b^{(c₀)}_{y,r} ∈ C(c)`:
the lower envelope satisfies `L_A(y) ≤ g(y) − c₀·C(d(y,A)+1,2)`.  (The class is *not* closed under `min`,
so there is no dip construction at instances on the boundary of the class.)

LP check (`t01`): 1 069 pairs `(A, y)` with random affinely spanning `A`, `n = 3…6`: no violation, tight in
438 cases.

### 2.2 Theorem B — stars do not combine; exact values  [N] [LP] [(b): Lean]

**Theorem B.**  Dense constants.
(a) If `a ∈ A` and `a⊕e_i ∈ A` for all `i` with `a_i ≠ y_i` (a *partial star in the directions of `y`*),
then `w_A(y) ≤ c·C(d(a,y), 2)`.
(b) Hence `c·C(d(y,A)+1, 2) ≤ w_A(y) ≤ c·C(d(y, int A), 2)` with `int A = {a : star(a) ⊆ A}`, and for
every thickened set `A = N[A₀]`:  **`w_A(y) = c·C(d(y,A₀), 2)` for all `y`.**
(c) `w_A(y) = c` (the least possible value at an unevaluated point) iff `y` *completes a square*: some
2-face through `y` has its other three corners in `A`.
(d) The even-weight code (`2^{n−1}` points, no two adjacent, empty interior) has `w ≡ 3c/2` on the odd
points (`n ≥ 3`).

*Proof.*  (a) is the star remainder (Theorem 11.16 of the report) in the subcube spanned by `a` and `y`.
(b) For `y ∉ N[A₀]`, `d(y,A) = d(y,A₀) − 1`, so the bounds of Theorem A and of (a) coincide.
(c) "⇐": `|h(y)| = |D_iD_jh| ≤ c`, and `≥ c` by the point dip.  "⇒": in an optimal dual solution with
`Σ|λ| = 1` the coefficient of `δ_y` forces all weight onto faces through `y` with coherent signs; the
opposite corner `y⊕e_i⊕e_j` of a used face occurs in no other such face, and the corner `y⊕e_i` occurs
in all of them with the same sign, so neither coefficient can cancel: these points lie in `A`.
(d) Upper bound: the three faces `(y; i,j)`, `(y; j,k)`, `(y⊕e_j; i,k)` give, with known `K₁,K₂,K₃`,
`h(y)+h(y⊕e_i⊕e_j) = K₁ ± c`, `h(y)+h(y⊕e_j⊕e_k) = K₂ ± c`,
`h(y⊕e_i⊕e_j)+h(y⊕e_j⊕e_k) = K₃ ± c`, hence `h(y) = (K₁+K₂−K₃)/2 ± 3c/2`.  Lower bound: on odd points
put `h = 3c/2` at `y` and `(−1)^{d/2}·c/2` at distance `d ≥ 2`; zero on even points. ∎

*Meaning.*  (b) generalises the referee's observation "two opposite stars: the better of the two star
bounds, no more" to arbitrary unions of stars: information from different stars is combined by a
*minimum* (tropically), exactly as in the first-order class.  (c)–(d) show that the general `w_A` is
richer than a nearest-point formula (fractional values, cancellations), but only between the two
bounds of (b).

LP checks (`t01`, `t09`): unions of 1–4 random stars, `n = 3…6`, 1 870 points: error `< 10⁻¹³`; criterion
(c) on all `(A,y)` for one representative of each of the 1 896 orbits of spanning sets containing `0`,
`n = 3, 4` (13 615 pairs): no mismatch; the next value above `c` is `3c/2`.

### 2.3 Theorem C — the covering sandwich  [N]

Let `G(y) = (gap(y) + ε)/c`,
`ρ₋(y) = max{d ≥ 0 : C(d+1,2) ≤ G(y)}`, `ρ₊(y) = ρ₋(y) + 1 = max{d : C(d,2) ≤ G(y)}`, and let `K_∓` be the
least size of a code `A₀` with `d(y,A₀) ≤ ρ_∓(y)` for all `y` (a covering code whose radius depends
on the point to be covered).

**Theorem C.**  Dense constants, arbitrary known `f`, additive true residual `g`.  Then

    K₋  ≤  N₂(f,g,ε)  ≤  (n+1)·K₊ + 1  ≤  (n+1)·K₋ + 1 .

Moreover every randomised algorithm that outputs, with error probability at most `δ` on every member of
the class, a lower bound of `min E` that is within `ε` of it (for two-sided approximations read `2ε`)
makes on this instance at least
`(1−2δ)·Σ_y v(y) / max_a Σ_{y : d(a,y) ≤ ρ₋(y)} v(y)` evaluations in expectation, for every `v ≥ 0`.

*Proof.*  Lower bound: for a certificate `w_A(y) ≤ gap(y)+ε`; apply Theorem A.  Upper bound: take a
`ρ₊`-covering `A₀`, `A = N[A₀] ∪ {x*}` (`x*` a minimiser); by Theorem B(a)
`w_A(y) ≤ c·C(d(y,A₀),2) ≤ gap(y)+ε`.  `K₊ ≤ K₋` since `ρ₊ ≥ ρ₋`.  Randomised: with `r = ρ₋(y)+2`
the instance `g − b_{y,r}` has a minimum below `min E − ε` and differs from `g` only on `B(y, ρ₋(y))`;
the algorithm must hit this ball with probability `≥ 1−2δ` on instance `g`; sum with weights `v`
(the packing argument of the report, §11.10). ∎

*General residual.*  If `g ∈ C(c′)`, `c′ ≤ c − c₀` entrywise, the same proof gives
`K[c₀·C(ρ+1,2) ≤ gap+ε] ≤ N₂ ≤ (n+1)·K[2c·C(ρ,2) ≤ gap+ε] + 1` (the star envelope has half-width
`≤ c·C(d,2)` around the star interpolant, which itself is within `c·C(d,2)` of `g`).

Exact small cases against the sandwich (`t13`; exact set-cover ILPs): `n = 5`, `θ = 1, 2/3, 1/2, 1/3, 1/4, 1/5`:
`K₋ = 5, 10, 10, 17, 27, 31`, exact `N₂ = 7, 11, 12, 21, 27, 31`, `|N[A₀]| = 12, 12, 12, 22, 29, 32`.

### 2.4 Corollary D — polynomial or exponential?  [N]

`f = e|x|`, `g = 0`, dense `c`; `h` = binary entropy (nats), `h₂` in bits, `V(n,r)` = volume of the
Hamming ball.

**(a) Fixed `θ = e/c > 0`, `ε = O(c)`.**  `log₂ N₂ = n − Θ_θ(√n·log n)`.  More precisely
`2ⁿ/V(n, ρ_max) ≤ N₂` with `ρ_max ≤ √(2(θn+η))`, and
`N₂ ≤ (n+1)[2^{h₂(1/4)n} + (1+n ln 2)·2ⁿ/V(n, ⌊√(θn/2)⌋)] + 1` (points of weight `< n/4` as their own
centres, a common radius for the others, greedy covering); the layers near `|y| = n/2` dominate and
give `n − log₂N₂ = (1+o(1))·log₂V(n, √(θn)) ~ ½√(θn)·log₂ n`.  (`t05`: at `n = 1024`, `θ = 1`:
`176.6 ≤ n − log₂N₂ ≤ 195.0`, `½√(θn)log₂n = 160`; the ratio tends to 1 like `1 + O(1/log n)`.)
**So with dense constants of order one the second-order class does not help at all at the exponential
scale: all but a `2^{−Θ(√n log n)}` fraction of the cube must be evaluated, for every value of `e/c`.**

**(b) Mean-field scaling `c = γ/n`, `λ = e/γ` (so `θ = λn`), sub-extensive accuracy `ε = o(n)`.**

    lim (1/n) ln N₂ = R₂(λ) := max{ h(ω) − h(√(2λω)) : 0 ≤ ω ≤ 1, √(2λω) ≤ min(ω, 1−ω) }  (:= 0 if empty),

`R₂(λ) > 0` iff `λ < 1/4`; `R₂(λ) → ln 2` as `λ → 0`
(`R₂ = 0.295, 0.173, 0.078, 0.031, 0.007, 0.0003` at `λ = 0.02, 0.05, 0.1, 0.15, 0.2, 0.24`).
*Proof.*  Lower bound: a certificate covers the layer `|y| = ωn` with radius `ρ₋ ≈ n√(2λω)`, and a ball
of radius `δn ≤ n/2` has at most `e^{nh(δ)}` points.  Upper bound: stars at a layer-wise covering; the
layer `ω` is covered by `0` if `√(2λω) ≥ ω`, by `1` if `√(2λω) ≥ 1−ω`, and otherwise by
`exp(n[h(ω) − h(δ)] + o(n))` balls of radius `δn`, `δ = √(2λω)` (type covering lemma; `h(ω) − h(δ)` is the
rate–distortion function of a Bernoulli(`ω`) source under Hamming distortion `δ ≤ min(ω,1−ω)`). ∎
In the language of the report this is `max_P R(P; d_H, √(2·E_P[gap]/γ))`: *the same rate–distortion
formula with a square-root budget.*

**(c) The polynomial side.**  Exact finite-`n` statements (`η = 0`):
* one star certifies iff `θ ≥ (n−1)/2` (report);
* **a balanced 3-spider (`n+1` evaluations) certifies iff `θ ≥ n/3`** (Theorem E below);
* `star(0) ∪ {1}` (`n+2` evaluations) certifies iff `θ ≥ max_w min(C(w,2), C(n,2)−C(w,2))/w ≈ n/(2√2) − O(1)`
  (its `w_A(y)` equals `c·min(C(w,2), C(n,2) − C(w,2))`: upper bound by two derivations, lower bound by a
  pairwise adversary; LP-verified pointwise for `n = 5, 6`, `t14`); its threshold is below `n/3` for `n ≤ 27`;
* two opposite stars (`2n+2`) certify iff `θ ≥ τ₂(n) := max_w min(C(w,2), C(n−w,2))/w = (⌊n/2⌋ − 1)/2`;
* for `θ ≤ (1/4 − δ)n` every certificate has at least `exp(n[ln 2 − h(½√(1−4δ))] − o(n)) ≥ e^{2δ²n − o(n)}`
  points.
So **polynomially many evaluations suffice iff `e ≥ (1/4 − o(1))·c·n`**; the window in which the count
passes from `2n+2` to super-polynomial has width `Θ(√(n log n))` in `θ` (covering the middle layer with
radius `n/2 − t` needs `≈ e^{2t²/n}` points).

**(d) Sup-norm recovery.**  Let `r_n(N) = min_{|A| ≤ N} max_y w_A(y)` (the `N`-th minimal radius of
information for recovery in the sup norm) and `t(n,N)` the least covering radius of a binary code of
length `n` and size `N` (the classical function `t[n,K]`).  Then

    c·C(t(n,N)+1, 2)  ≤  r_n(N)  ≤  c·C(t(n, ⌊N/(n+1)⌋), 2).

This is the second-order analogue of Sukharev's theorem (Lipschitz classes: radius of information = `c` ×
covering radius).  Consequences: to determine every member of the class to within `K·c` everywhere one
needs a covering code of radius `ρ(K) = max{d : C(d+1,2) ≤ K}`, hence at least `2ⁿ/V(n,ρ(K))` points, and
`(n+1)·K(n, ρ(K)+1)` suffice — for fixed `K` both are `Θ_K(2ⁿ/n^{ρ(K)})` (the best covering codes of fixed
radius have bounded density; Krivelevich–Sudakov–Vu).  With `N = poly(n)` evaluations
`t(n,N) = n/2 − Θ(√(n log n))`, so `r_n(N) = (1 − o(1))·c·n²/8`: *polynomially many evaluations reduce the
worst-case uncertainty from `c·C(n,2)` (one star) by a factor 4 (two opposite stars) and no further.*
Exact small values (`t02`): `r₃(4) = 3/2` (even-weight code, not a star), `r₃(5…7) = 1`;
`r₄(5) = 3`, `r₄(6) = r₄(7) = 2`, `r₄(8…15) = 1`.

### 2.5 Theorem E — which `n+1` evaluations?  Tree simplices and spiders  [N] [LP]

A *tree simplex* is given by a rooted tree `T` on `{0} ∪ [n]` (root `0`): `a⁰ = 0`,
`a^k = a^{parent(k)} ⊕ e_k`.  (These are exactly the simplices in which every coordinate has a
"derivative pair" `b, b⊕e_k ∈ A`.)  The star is the tree of depth one; a *spider* is a union of paths
("legs") from the root.  For `y ⊆ [n]` let
`X_T(y) = #{(j,k) : j a proper ancestor of k, k ∈ y, j ∉ y}` and
`I_T(y) = #{pairs in y that are incomparable in T}`.

**Theorem E.**  Dense constants.
(a) For every tree simplex, **`w_{A_T}(y) = c·[X_T(y) + I_T(y)]`** for all `y`.
(b) For the balanced 3-spider (legs of lengths `⌊n/3⌋` or `⌈n/3⌉`), `max_{y≠0} w(y)/|y| = c·n/3`
(`n ≥ 3`).  Hence, for `f = e|x|`, `g = 0`, any `ε ≥ 0`: **`N₂ = n+1` whenever `e ≥ c·n/3`.**
(c) For *every* rooted tree `T` on `n ≥ 3` nodes, `max_{y≠0} [X_T(y)+I_T(y)]/|y| ≥ n/3`; a universal
witness is `U = {k : |D(k)| ≤ ⌊n/3⌋}`, `D(k)` = the subtree of `k`.  So `n/3` is the exact optimum over
tree simplices (the star has `(n−1)/2`, the path `n−1`).

*Proof.*  (a) Upper bound.  Let `h ∈ C(c)` vanish on `A_T`; `D_kh(B) := h(B∪{k}) − h(B)`.  Changing one
element of `B` changes `D_kh(B)` by a mixed difference, so `|D_kh(B) − D_kh(B′)| ≤ c|B △ B′|`.  Order
`y = {k₁,…,k_w}` by a linear extension of the tree order, `S_t = {k₁..k_t}`; since
`D_kh(anc(k)) = h(a^k) − h(a^{parent(k)}) = 0`,
`h(y) = Σ_t [D_{k_t}h(S_{t−1}) − D_{k_t}h(anc(k_t))]`, so `|h(y)| ≤ c Σ_t |S_{t−1} △ anc(k_t)|`, and
`Σ_t |anc(k_t) ∖ S_{t−1}| = X_T(y)`, `Σ_t |S_{t−1} ∖ anc(k_t)| = I_T(y)`.  Lower bound.  The pairwise
function `h(x) = c·Σ_{incomparable j,k ∈ y} x_jx_k + c·Σ_{j anc k, k∈y, j∉y} (x_k − x_jx_k)` is in `C(c)`,
vanishes on every root path `a^m`, and equals `c(I+X)` at `y`.
(b) Given the numbers `s_r` of elements of `y` on the legs, `X` is largest for the top (deepest) `s_r`
nodes: `X + I = Σ_r s_r(ℓ_r − s_r) + Σ_{r<r′} s_rs_{r′} = Σ_r s_rℓ_r − ½Σ_{r<r′}(s_r−s_{r′})²`.  For
`ℓ = (m,m,m)` this is `≤ m·|y|` with equality iff `s₁=s₂=s₃`; for `(m,m,m+1)` and `(m,m+1,m+1)` the
claim `≤ (n/3)|y|` reduces to `u + v ≤ (3/2)(u²+v²+(u−v)²)` for integers `u, v`.
(c) Let `s = ⌊n/3⌋`, `n = 3s+ρ`, `J = {k : |D(k)| > s}` (ancestor-closed), `N = |J|`, `m = |U| = n − N`.
`U` is a disjoint union of subtrees ("components") of sizes `s_i ≤ s`; component `i` has `a_i` ancestors,
all in `J`.  Then `X(U) = Σ s_ia_i` and `I(U) ≥ Σ_{i<i′}s_is_{i′} = ½(m² − Σs_i²)`.  (i) Below a deepest
node `j` of `J` hang components of total size `|D(j)| − 1 ≥ s`, at depth `dp(j)` = number of nodes of `J`
on the root path of `j`; `J` is the union of these root paths, so `X(U) ≥ s·Σ_j dp(j) ≥ sN`.
(ii) If `m = ks + r` with an integer `k ≥ 0` and `r ≥ 0`, then `Σ s_i² ≤ ks² + r²` (majorisation if
`r < s`; `Σs_i² ≤ sm` if `r ≥ s`), so `I(U) ≥ C(k,2)s² + ksr`.  Three cases:
`N ≤ ρ` (`k = 3`, `r = ρ−N`): `X+I − (n/3)m ≥ (ρ−N)(s − ρ/3) ≥ 0`;
`ρ < N ≤ s+ρ` (`k = 2`, `r = s+ρ−N`): `≥ (ρ/3)(N−ρ) ≥ 0`;
`s+ρ < N ≤ 2s+ρ` (`k = 1`, `r = 2s+ρ−N`): `≥ s(N−s−ρ) + (ρ/3)(N−ρ) > 0`;
and `N ≤ n − s = 2s+ρ` always, since `m ≥ s` when `J ≠ ∅`. ∎

Verification (`t03`, `t07`, `t14`): formula (a) against the full-class LP for all rooted trees `n ≤ 6`
(81 trees) and random trees `n = 7, 8`; `min_T max_y` over all rooted trees is exactly `n/3` for
`n = 3…12` (20 295 trees); the witness `U` of (c) works for every tree, `n ≤ 12`; the three algebraic
cases checked in exact arithmetic for all `n < 400`.  Equality cases include the spiders
`(s+N, s, s−N)`.

**Conjecture E′ [C].**  For every simplex `A ∋ 0` of the `n`-cube (`n ≥ 3`) there is `y ≠ 0` with
`w_A(y) ≥ c·(n/3)|y|`; i.e. `N₂(n; θ, 0) = n+1` iff `θ ≥ n/3`.
*Evidence.*  Exhaustive over all simplices for `n ≤ 6` (`n = 6`: 40 050 850 simplices), already for the
pairwise subclass (`t04`): the minimum is exactly `n/3`, attained for `n = 6` by 850 simplices in 3
orbits — the spiders `(2,2,2)`, `(3,2,1)` and one *non-tree* simplex
`{0, e₁+e₂, e₁+e₃, e₂+e₃, e₄+e₅, e₄+e₆, e₅+e₆}`; simulated annealing over all simplices `n = 7…10`
(`t12`, 6 runs each) ends at exactly `n/3` in 23 of 24 runs and never below.  The exact values
`θ_{n+1} = 1, 4/3, 5/3` for `n = 3, 4, 5` from the hitting-set solver (full class, all sets) agree.
*What a proof needs.*  In the pairwise subclass the error of a simplex is
`err(y) = ½‖M(μμᵀ − diag μ)Mᵀ‖₁`, `μ = M⁻¹y` (`M` = the matrix of the points); the bound `(n−1)/4` follows
from `y = e_i` and `y = 1` alone, and a fictitious "frame" `G_i = ¼·1[pairs ∋ i]` (the gradient at the
interior point `¼·1`) would attain it — the gap between `n/4` and `n/3` is entirely due to the fact that
gradients can only be measured at vertices.
*Caveat.*  For `η > 0` non-tree simplices can be strictly better at small `n`: `n = 4`, `η = ½`:
`θ = 1` with `{0, e₁, e₂+e₃, e₂+e₄, e₃+e₄}` against `7/6` for the best tree; the conjecture is for `η = 0`.

### 2.6 The window `τ₂(n) ≤ θ < n/3`: exact small-`n` data  [LP]

Exact step functions `θ ↦ N₂(n; θ, 0)` (dense, `c = 1`, `f = θ|x|`, `g = 0`), by exhaustive enumeration
(`n = 3, 4`: all 1 965 orbits of evaluation sets, `t02`) and by an implicit-hitting-set method
(`ihs.py`: master = minimum hitting set by MILP, separation = LPs producing maximal non-certifying sets;
it reproduces the exhaustive tables for `n = 3, 4`):

| `n` | `N₂` and the range of `θ = e/c` on which it holds |
|---|---|
| 3 | 4 `[θ ≥ 1]`, 5 `[1/2, 1)`, 7 `[1/3, 1/2)`, 8 `[0, 1/3)` |
| 4 | 5 `[θ ≥ 4/3]`, 6 `[1, 4/3)`, 7 `[2/3, 1)`, 9 `[1/2, 2/3)`, 12 `[1/3, 1/2)`, 15 `[1/4, 1/3)`, 16 `[0, 1/4)` |
| 5 | 6 `[θ ≥ 5/3]`, 7 `[1, 5/3)`, 11 `[2/3, 1)`, 12 `[1/2, 2/3)`, 21 `[1/3, 1/2)`, 27 `[1/4, 1/3)`, 31 `[1/5, 1/4)`, 32 `[0, 1/5)` |
| 6 | 7 `[θ ≥ 2]`, 8 `[3/2, 2)`, 9 `[5/4, 3/2)`; just below `5/4`: at least 11 (bound of the long hitting-set run; `≥ 10` confirmed by an independent fresh run, `t18`) and at most 13 (which suffice for `θ ≥ 1`) — not finished |

Optimal sets: `n+1`: spiders; `n+2`: `star(0) ∪ {1}`; `n+3` (`n = 6`): `star(0) ∪ {1, 1−e₆}`;
`2n+1`: two opposite stars without one centre; `2n+2`: two opposite stars; then thickened codes;
`2ⁿ − 1` for `1/n ≤ θ < 1/(n−1)`; everything for `θ < 1/n` (point dips).  For `η = ½, 1` see
`t02_n3.out`, `t02_n4.out`.

The family `A_k = star(0) ∪ {1} ∪ {1−e_i : i < k}` (`n+2+k` points; `t17`) interpolates between the two
ends, in steps: `n = 6`: `θ* = 3/2, 5/4, 5/4, 5/4, 5/4, 1, 1` for `k = 0…6`; `n = 7`:
`2, 8/5, 8/5, 8/5, 8/5, 8/5, 5/4, 1`.  Further design data (`t10`, `t11`): `n = 7`: star `3`, spider `7/3`,
two stars minus a centre `5/4`; "spider + co-spider" and "spider + star(1)" are *worse* than two stars
(`2` against `1`) — the spider is good only as a simplex; `n = 6`: spider plus its two tight "top" sets
(9 points): `5/3`; spider + `{1}`: no gain (`2`).

**Open (§5).**  In the mean-field limit the count for `1/4 < λ < 1/3` lies between `n+1` (`n+2` if
Conjecture E′ holds) and `2n+2`.
For sets containing `star(0)` one can show that `Ω(n)` extra points are needed below `λ = 1/(2√2)`
(§2.8(c)), but spiders beat that family, so this says nothing about general sets.

### 2.7 Sparse constants: the clique complex governs  [R]/[N] [LP]

Let `G` be the graph of pairs with `c_ij > 0`.

**Proposition F.**
(a) *Finite dimension.*  `D_iD_jh ≡ 0` kills every monomial `x^S` with `S ⊇ {i,j}`; hence
`C(c) = {Σ_{K clique of G} ĥ_K x^K : |Σ_{K ⊇ {i,j}, K∖{i,j} ⊆ ctx} ĥ_K| ≤ c_ij}`, a polytope-cylinder in a
space of dimension `κ(G)` = number of cliques of `G` (including `∅` and the vertices).  For a
triangle-free `G`: `h = a₀ + Σ a_ix_i + Σ_{e∈E} b_e x_ix_j`, `|b_e| ≤ c_e`.
(b) *Upper bound.*  `N₂ ≤ κ(G)` for every instance: the indicator vectors of the cliques determine `h`
exactly (Möbius inversion on a down-set), and no set of fewer than `κ(G)` points determines every member
everywhere.  `κ(G) ≤ 1 + n·2^{Δ}` for maximum degree `Δ`, `= 1+n+|E|` for triangle-free `G`
(chain: `2n`).
(c) *Lower bound.*  For every clique `K` of `G` with `c_ij ≥ c₀` on `K`, a certificate must satisfy
`c₀·C(d_K(y,A)+1,2) ≤ gap(y)+ε` (Theorem A(iv)); so the projection of `A` to `{0,1}^K` is a covering
code, and for `f = e|x|` and fixed `e/c₀`: `N₂ ≥ 2^{ω − O(√ω log ω)}`, `ω = ω(G)` the clique number.
(d) *One star.*  For additive `f` with excitation energies `e_i` and zero residual, the star at the
minimiser certifies iff `max_S [Σ_{i<j∈S} c_ij − Σ_{i∈S} e_i] ≤ ε` — a maximum-weight-closure /
densest-subgraph condition, decidable by one min-cut (the lower pairwise model of Theorem 11.17 is
submodular in the set of changed sites; for `k` states take the smallest measured excitation at each
site).  For `e_i ≡ e`, `ε = 0`: iff the maximum subgraph density `max_S c(S)/|S| ≤ e`.  This is implied
by, and can be much weaker than, the row-sum condition `½Σ_j c_ij ≤ e_i` of the report: for the graph
`K_{1,m}` the row-sum condition asks `mc/2 ≤ e`, the truth is `mc/(m+1) ≤ e`.

So the answer to "is the cost governed by the graph (treewidth, degree)?" is: *by its cliques.*
`K_{m,m}` (treewidth `m`, dense) costs at most `1 + 2m + m²`; `K_n` costs `2^{n−o(n)}`; a chain costs at
most `2n`.  Treewidth governs the *computation* of the minimum of the identified model, not the number of
evaluations.

*What replaces the star on a chain?*  Not "a star plus pair evaluations".  Exact values
(`t06c`: hitting sets over all `2ⁿ` points, clique-space LP; `c = 1`, `f = θ|x|`, `η = 0`; one star
needs `θ ≥ (n−1)/n`):

| `θ` | `n = 3` | `n = 4` | `n = 5` |
|---|---|---|---|
| 1/2 | 5 | 6 | 7 |
| 2/3 | 4 (star) | 6 | **6** |
| 3/4 | 4 (star) | 5 (star) | **6** |
| 4/5 | 4 | 5 | 6 (star) |

So `N₂ ≤ n+2` in every case computed, although full identification needs `2n` points, and for `n = 5`,
`θ = 2/3, 3/4` a *non-star simplex* certifies where the star does not
(`{∅, {1,3}, {1,4}, {2,3,4}, {2,5}, {3,5}}`, resp. `{∅, {2,3}, {1,4}, {2,5}, {3,5}, {1,3,5}}`; tree
simplices cannot do this on a chain).  The optimal set for `n = 5`, `θ = 1/2` contains no single-site
point: `{∅, {1,3}, {1,4}, {2,4}, {3,5}, {1,2,3,4}, {1,2,3,5}}`; it leaves a 3-parameter family
(`a = (b₃/2)(1,1,−1,−1,1)`, `b₃ = −b₁−b₂`, `b₄` free) and works by *entangling* the unknown one-body terms
with the couplings so that every single site carries uncertainty exactly `θc`.  (My first guess —
star plus evaluations of blocks of `⌊1/(1−θ)⌋` sites — is not optimal: 6, 8, 10 at `θ = 1/2`.)
Whether the overhead `N₂ − (n+1)` stays bounded as `n` grows is open (§5).

LP checks (`t06`): full-cube LP with zero constants = clique-space LP (chain, cycle, `K₃,₃`; error
`< 10⁻¹²`); the star gives `c·#edges(y)`; clique indicators give `w ≡ 0`; no set of `κ−1` points does
(240 random trials); clique lower bound: 642 random pairs, no violation.

### 2.8 The pairwise subclass (bounded unknown couplings): polynomial, but quadratic  [N, proof sketch]

`P(c) = {a₀ + Σa_ix_i + Σ_{i<j} q_ijx_ix_j : |q_ij| ≤ c}` — the residual is *known* to be pairwise.
`P(c) ⊂ C(c)`, dimension `1+n+C(n,2)`.
(a) `N₂^{pair} ≤ 1+n+C(n,2)` (radius-2 ball), and all tree-simplex results hold verbatim (the extremal
functions of Theorem E are pairwise): `n+1` evaluations for `e ≥ cn/3`.
(b) **If `e/c ≤ √n/92 − 2ε/(cn)` (`n ≥ 6`) then `N₂^{pair} ≥ n + 1 + n²/10`.**  *Sketch.*  With
`k = |A| − n − 1`, the consistent coupling matrices form `W ∩ [−c,c]^{pairs}` with `codim W ≤ k`; a vertex
`Q*` has at least `C(n,2) − k` entries `±c`.  For disjoint `S, T`,
`h(S∪T) − h(S) − h(T) + h(∅) = Q*(S,T)` (the affine part cancels), so a certificate forces
`|Q*(S,T)| ≤ 2en + 4ε`.  But a balanced bipartite block of `Q*/c` with at most `n²/16` entries not `±1`
has cut norm `≥ n^{3/2}/(32√2)` (Khintchine–Szarek for each row, then `‖·‖_cut ≥ ¼‖·‖_{∞→1}`) — the
Erdős–Spencer discrepancy phenomenon; and a random balanced partition contains at most `0.6k` of the
exceptional pairs. ∎  (Constants not optimised; not checked numerically.)
So knowing that the residual is pairwise removes the exponential but, for couplings stronger than
`≈ e/√n`, not the need to identify essentially all `Θ(n²)` couplings.
(c) For sets `A ⊇ star(0)` and `λ = e/(cn) < 1/(2√2)`: `|A| ≥ n + 1 + Ω(n)` (sketch: for such `A` the
pairwise adversaries give `w_A(y) ≥ dist_{ℓ₁}(1_{K_y}, span{1_{K_b}})`; a fixed approximant is at distance
`≥ (1−o(1))·min(C(w,2), C(n,2)−C(w,2))` from all but an exponentially small fraction of a layer, and a
subspace of dimension `o(n)` has too few essentially different approximants).
This does *not* extend to general `A` (spiders).

### 2.9 Order `m`, and `k`-state sites  [N] [LP]

**Theorem G.**  Let all mixed differences of order `m` be bounded by `c` (dense).  Then
`c·C(r − d(x,y), m)₊` is in the class, vanishes outside `B(y, r−m)` and equals `c·C(r,m)` at `y`; hence
`w_A(y) ≥ c·C(d(y,A)+m−1, m)` for every `A`.  For a union of balls of radius `m−1` around centres `A₀`,
`w_A(y) = c·C(d(y,A₀), m)` exactly.  Therefore, with
`ρ₋ = max{d : c·C(d+m−1,m) ≤ gap+ε}`, `ρ₊ = ρ₋+m−1`:  `K₋ ≤ N_m ≤ V(n,m−1)·K₊ + 1`.
In the scaling `c = γ/n^{m−1}`, `λ = e/γ`:
`lim (1/n) ln N_m = R_m(λ) = max_ω [h(ω) − h((m!λω)^{1/m})]₊` (over `ω` with
`(m!λω)^{1/m} ≤ min(ω,1−ω)`), positive iff `λ < 2^{1−m}/m!`; for `λ ≥ 2^{1−m}/m!` two opposite balls of
radius `m−1` (`O(n^{m−1})` evaluations) suffice, and one ball suffices iff `λ ≥ 1/m!` (asymptotically).
*For `m = 1` this is the first-order theorem of the report* (binary sites, zero residual:
`R* = max_μ[h(μ) − h(ρμ)]`, one evaluation iff `c ≤ e`).  The covering radius improves only from `gap/c`
to `(m!·gap/c)^{1/m}`: higher-order smoothness buys a polynomially larger radius, never a polynomial
cost, unless the coupling is of mean-field strength.
*Proof.*  As Theorem A with the `m`-th difference of `C(·,m)`; upper bound: Theorem 11.18 of the report. ∎
(`t08`: `(n,m) = (5,3), (6,3), (6,4), (7,3)`: dips in the class, the ball of radius `m−1` gives `C(w,m)`,
unions of balls exact (592 points), dip bound on 256 random pairs: no violation.)

**`k`-state sites.**  With the Hamming distance (number of differing sites), Theorems A–C hold verbatim:
the dip is the same function of the distance, the star has `1+n(k−1)` points, and
`K₋ ≤ N₂ ≤ (1+n(k−1))K₊ + 1` with covering codes in `{0..k−1}ⁿ` (`t08`: `(n,k) = (3,3), (4,3), (3,4)`:
star, unions of stars (1 117 points) and dip bound (437 pairs) all exact / without violation).

### 2.10 Relation to local correction, interpolation, designs

* *Interpolation.*  `w_A(y)` is the norm of the error functional of the best formula that is exact on
  affine functions, in the dual of the mixed-difference seminorm.  For a simplex it is the error of *the*
  affine interpolant; tree simplices are the nodal sets with an explicit kernel (Theorem E(a)); the star
  is the Taylor (anchored, cut-HDMR) case.  The intrinsic obstruction is that all nodes are extreme
  points: every formula extrapolates.
* *Local correction of degree-1 functions.*  Linear functions on the cube are locally correctable from a
  constant fraction of *arbitrary sparse* corruptions with `Õ(log n)` queries
  (Amireddy–Behera–Paraashar–Srinivasan–Sudan 2024).  In the present noise model (a perturbation that is
  small in the mixed-difference seminorm) the opposite holds: a corrector whose queries are at distance
  `≥ d` from `y` has error `≥ c·C(d+1,2)` (Theorem A), three queries give error `c` iff they complete a
  square, and the partial star (`d+1` queries, error `c·C(d,2)`) is the natural trade-off: correction is
  necessarily local in the Hamming metric.  The two models are incomparable; "smooth" second-order
  perturbations are invisible to far queries.
* *Approximate modularity.*  The class is the set of *locally* `c`-modular set functions
  (`|f(S∪T)+f(S∩T)−f(S)−f(T)| ≤ c|S∖T||T∖S|`).  For *uniformly* `ε`-modular functions (defect `≤ ε` for
  all `S,T`) Kalton–Roberts gives a modular function within `O(ε)`, `O(n)` value queries learn it to
  `O(ε√n)` (Feige–Feldman–Talgam-Cohen) and polynomially many queries cannot do better than
  `Ω(ε√n/log n)` (Chierichetti–Das–Dasgupta–Kumar, as quoted by FFT).  Locally modular functions are not
  close to modular ones (`c·C(|x|,2)`), and the analogue of that query bound is §2.4(d): `≈ c·n²/8`.
* *Designs.*  Orthogonal/covering arrays and codes with large minimum distance are *thin*: they contain
  no star, the upper bound of Theorem B is void, and their covering radius is what matters (Theorem A).
  The right objects are covering codes `K(n,R)`, thickened by radius 1 (radius `m−1` for order `m`).

### 2.11 Negative results and dead ends (mine)

1. *"Some cleverer evaluation set avoids the quadratic remainder."*  No (Theorem A): for every `A`.
2. *"Covering arrays of strength 2 / random sets / Reed–Muller-type sets are the right design."*  No:
   thickened covering codes; the even-weight code (half the cube) only reaches `3c/2`.
3. *"The star is the best simplex; the row-sum condition is the threshold for `n+1` evaluations."*  No:
   spiders (`n/3` against `(n−1)/2`); for sparse graphs the exact one-star criterion is the density
   condition, and on a chain non-star simplices do better still.
4. *"A simplex could reach `e = cn/4`"* (suggested by the relaxation with fractional frames).  Not
   realisable: `n/3` for trees (proved), for all simplices `n ≤ 6` (exhaustive).
5. *"Two trees (spider + co-spider) beat two stars."*  No (LP, `n = 6, 7`).
6. *"Half-space dips improve on ball dips."*  No (Remark (iii) to Theorem A).
7. *"Below the `star(0)∪{1}` threshold, `Ω(n)` extra points are needed."*  Proved only for sets containing
   `star(0)`; false as a statement about general sets in the mean-field limit, where the spider (no
   extra point) is better (`1/3 < 1/(2√2)`, from `n = 28` on).
8. *"On a chain the optimum is a star plus block evaluations."*  No (`n+2` at `θ = 1/2`, `n ≤ 5`).
9. Proof attempts for Theorem E(c) that failed before the right witness was found: uniform averaging over
   the family `U_s = {|D(k)| ≤ s}` (fails at lower order, e.g. `−n(n+1)/6` for the path) and the threshold
   `n/3 + 1/2` instead of `⌊n/3⌋`.
10. Two errors of mine caught by cross-checks: (i) the pickles of `t02` store `w` for the first-seen
    member of each orbit under a canonical key — harmless for the permutation-invariant quantities
    reported there, wrong for point-wise use (fixed in `t09` by recomputation); (ii) I first misread the
    log of the `n = 6` hitting-set run as "`≥ 11` points just below `θ = 3/2`"; a greedy search found a
    9-point certificate at `θ = 5/4` (verified with fresh primal and dual LPs, `t16`), and the log in fact
    refers to `θ` just below `5/4`.

---

## 3. Numerics

All linear programs with HiGHS 1.16 (through `highspy`/`scipy`); values agree with exact rationals to
`10⁻¹²`.  The machine was shared (load 15–19 on 4 cores), so sizes are modest.

| script | what | sizes | result |
|---|---|---|---|
| `so.py` | LP model of `w_A(y)` (dense or weighted `c`), explicit dual, helpers | `n ≤ 9` | — |
| `t01_core_checks` | star, radius-2 ball, two stars; dips in class; dip bound; unions of stars; even code | `n = 3…6` | all exact; 0 violations in 1 069 random pairs; unions of stars exact (1 870 pts); even code `3/2` |
| `t02_exhaustive_small` | all evaluation sets `∋ 0` up to `S_n`; thresholds `θ_N` for `η = 0, ½, 1`; `r_n(N)` | `n = 3` (30 orbits), `n = 4` (1 935 orbits) | tables of §2.6, §2.4(d) |
| `t03_tree_simplices` | formula `X+I` vs LP; all rooted trees | LP `n ≤ 8`; trees `n ≤ 12` (20 295) | exact; best tree `= n/3` |
| `t04_all_simplices` | all simplices, pairwise error, full LP on the optima | `n = 3…6` (40 050 850 simplices at `n = 6`) | minimum `= n/3`; 3 optimal orbits at `n = 6` |
| `t05_exponent` | covering sandwich with exact binomials | `n ≤ 400` (mean field), `n ≤ 1024` (fixed `θ`) | brackets converge to `R₂(λ)` at rate `O(log n/n)`; deficit `~ ½√(θn)log₂n` |
| `ihs.py` | exact `N₂(n;θ,η)` by implicit hitting sets | `n = 3, 4, 5` complete; `n = 6` partial | step functions of §2.6 |
| `t06_sparse`, `t06c_chain`, `sparse.py` | sparse classes; chain exact values | LP `n ≤ 7`; chain hitting sets `n ≤ 5` | §2.7 |
| `t07_tree_lower`, `t07b_explore` | test sets `U_s`; the witness of Theorem E(c) | all trees `n ≤ 12` | witness works for every tree |
| `t08_order_m_kary` | order `m` and `k`-state sites | `(n,m) ≤ (7,3),(6,4)`; `(n,k) = (3,3),(4,3),(3,4)` | exact; 0 violations |
| `t09_square_completion` | criterion `w = c` | all orbits `n = 3, 4` (13 615 pairs) | 0 mismatches |
| `t10_designs`, `t11_spider_plus`, `t17_partial_two_stars` | natural designs, full LP | `n = 6, 7` | §2.6 |
| `t12_simplex_search` | annealing over all simplices (pairwise error) | `n = 7…10`, 6 runs each | never below `n/3` |
| `t13_sandwich_small` | `K₋`, `K₊` (exact ILP) vs exact `N₂` | `n = 4, 5` | `K₋ ≤ N₂ ≤ |N[A₀]|` always; `K₋ = N₂` for small `θ` |
| `t14_misc_checks` | `star(0)∪{1}` formula; best trees for `η > 0`; crossover `n = 28`; algebra of Thm E(c) | `n ≤ 6` (LP), `n < 400` (algebra) | all as stated |
| `t15_greedy_n6`, `t16_verify_A9`, `t18_n6_theta9` | 9-point certificate for `n = 6` at `θ = 5/4` (independent primal/dual check); no 9-point certificate at `θ = 1.2499` | `n = 6` | `θ₉(6) = 5/4` exactly |
| `t19_validate_ihs` | every generating cut of the hitting-set run at `n = 5`, `θ = 0.9999` re-verified by a fresh LP | 13 base cuts (260 with symmetry) | all valid; `N₂ = 11`; no abnormal LP status |
| `lean/StarsDoNotCombine.lean` | Theorems A and B(a),(b) in Lean 4 + Mathlib against `MixedDiffBound` | general product spaces | compiles, standard axioms |

Mean-field brackets (`t05`; natural logarithms; `lo ≤ (1/n) ln N₂ ≤ up`):

| `λ` | `R₂(λ)` | `n = 100` | `n = 200` | `n = 400` |
|---|---|---|---|---|
| 0.02 | 0.2948 | 0.331 – 0.420 | 0.315 – 0.368 | 0.306 – 0.337 |
| 0.05 | 0.1731 | 0.204 – 0.301 | 0.191 – 0.248 | 0.183 – 0.216 |
| 0.10 | 0.0783 | 0.105 – 0.207 | 0.093 – 0.153 | 0.086 – 0.121 |
| 0.15 | 0.0306 | 0.052 – 0.158 | 0.043 – 0.105 | 0.038 – 0.073 |
| 0.25 | 0 | 0.046 – 0.131 | 0.027 – 0.076 | 0.015 – 0.043 |

(the upper bracket carries a crude polynomial factor `≈ n³`, i.e. `3 ln n / n`; at `λ ≥ 1/4` the true value
is `ln(2n+2)/n`).

**Lean.**  Theorems A and B(a),(b) are machine-checked in a scratch file against the repository's own
definitions `MetricChain.MixedDiffBound`, `pairRemainder`, `secondOrder_remainder`, for general product
spaces (`k`-state sites included): `lean/StarsDoNotCombine.lean` (220 lines; compiled with
`lake env lean`, no `sorry`, no warnings, axioms `propext`, `Classical.choice`, `Quot.sound` only):
* `dip_mixedDiffBound : 0 ≤ c → MixedDiffBound (dip c y r) (fun _ _ => c)`,
  `dip_eq_zero : r ≤ hdist x y + 1 → dip c y r x = 0`, `dip_center : dip c y r y = c * C(r,2)`;
* `dip_witness` (Theorem A): if every point of `A` is at Hamming distance `≥ d` from `y`, some member of
  the class vanishes on `A` and equals `c·C(d+1,2)` at `y`;
* `pairRemainder_const`, `star_upper` (Theorem B(a) for a full star): a member vanishing on the star of
  `x₀` is at most `c·C(hdist y x₀, 2)` at `y`;
* `stars_do_not_combine` (Theorem B(b)): if `A` contains the star of a nearest centre `a⋆ ∈ A₀` at
  distance `D ≥ 1` from `y` and every point of `A` is within distance one of a centre, then every member
  vanishing on `A` is at most `c·C(D,2)` at `y` *and some member attains it*.
(`lean/SecondOrderDip.lean` is the earlier Theorem-A-only version, `lean/DipSecondDifference.lean` the
scalar lemma over `ℤ`.)  Nothing else is formalised: Theorems C–G and Proposition F are paper proofs
with the numerical checks listed above.

---

## 4. Prior art and search log

What I actually read is marked: (A) abstract/listing only, (S) search-engine summary, (F) fetched page,
read through an automatic summariser (first 100 000 characters).  No full paper was read by me line by
line; novelty claims are therefore "not found", not "absent".

| query (WebSearch) | relevant hits | read |
|---|---|---|
| "approximate modularity" Chierichetti Das Dasgupta Kumar value queries | Feige–Feldman–Talgam-Cohen, *Approximate modularity revisited* (STOC'17, SICOMP 49 (2020), arXiv 1612.02034); CDDK FOCS'15 | (F) ar5iv text of FFT: `ε`-modular ⇒ `Δ < 12.62ε`-linear; `O(n)` non-adaptive queries, error `O(Δ(1+√min(|S|,n−|S|)))`; quotes CDDK: polynomially many queries cannot beat `Ω(Δ√n/log n)`; Kalton–Roberts 1983 |
| optimal recovery radius of information Lipschitz covering radius Sukharev | Sukharev 1976 (Dokl. AN SSSR; mathnet); surveys arXiv 2211.02312, 1908.05943 | (S) |
| Babenko Borodachov Skorokhodov optimal recovery twice-differentiable | J. Complexity 26 (2010) 591–607; Ling–Gu arXiv 2510.15277 | (A) continuous analogue: optimal recovery of twice-differentiable classes from values / gradients |
| "Local correction of linear functions over the Boolean cube" | Amireddy, Behera, Paraashar, Srinivasan, Sudan, STOC 2024 (arXiv 2403.20305); follow-up arXiv 2411.07374 (degree `d`) | (S) |
| Krivelevich Sudakov Vu covering codes improved density | IEEE-IT 49 (2003) 1812–1815: `μ*(R) ≤ e(R log R + log R + log log R + 2)` | (S) |
| optimal recovery Hamming cube bounded second-order differences covering codes | nothing on this problem; Elimelech–Schwartz "second-order covering codes" (a different notion) | (S) |
| pseudo-Boolean k-bounded Walsh coefficients query complexity | Choi et al. (COLT 2008; "almost tight upper bound…"): `O(m log n)` queries for a `k`-bounded function with `m` non-zero coefficients (relevant to §2.7–2.8: finite-dimensional classes) | (S) |
| approximately supermodular / bounded Hessian multilinear extension zeroth-order lower bound | Chierichetti–Dasgupta–Kumar, *On additive approximate submodularity* (arXiv 2010.02912); one-sided smoothness of multilinear extensions | (S) |

Assessment.
* **[K]** the anchored (star / ball) remainder and its exactness (report, Theorems 11.16–11.18;
  Kuo–Sloan–Wasilkowski–Woźniakowski); radius of information for symmetric convex classes; Sukharev's
  covering theorem for Lipschitz classes; type covering; covering codes; discrepancy of sign matrices;
  densest subgraph by min-cut.
* **[N] (not found)** the second-order dip and the law `w_A ≥ c·C(d+1,2)` for arbitrary evaluation sets
  on the cube; "stars do not combine"; the covering sandwich and the exponents `R₂`, `R_m` with the root
  budget; the tree-simplex formula and the `n/3` spider; the clique-complex statement for sparse
  constants.  All proofs are short (a discrete second difference, the star remainder, type covering, a
  counting argument for trees): in the referees' terms this adds *one complete answer* (to §12 item 4)
  and one design problem with a clean conjecture, not a deep theorem.

---

## 5. What is not settled

1. **Conjecture E′**: no simplex certifies below `e = cn/3` (all `n`).  Proved for tree simplices;
   exhaustive for `n ≤ 6`; annealing for `n ≤ 10`.
2. **The window `1/4 < e/(cn) < 1/3`** (mean-field): is `N₂ − n` bounded, or `Θ(n)`?  The small-`n` data
   (`n = 5`: 6, 7, then 11; `n = 6`: 7, 8, 9, then ≥ 11) show a gradual start and then a jump towards
   `2n`, but these sizes are dominated by finite-size effects (`star(0)∪{1}` beats the spider up to
   `n = 27`).  Adding to a spider the sets on which it is tight helps (`n = 6`: `2 → 5/3` with two
   points), and one added point relieves a whole range of the tight family, so `n + O_λ(1)` is not
   excluded; the family of §2.6 gives `n + 2 + k` with a threshold that decreases in steps.
3. **Polynomial factors**: `K₋ ≤ N₂ ≤ (n+1)K₊`.  For fixed radius the two sides agree up to a constant;
   in general up to `O(ρ² log ρ)`.  Is the thickening necessary at the level of constants (density of an
   optimal "second-order covering")?  The exact small cases have `N₂` close to `K₋`.
4. **Instances on the boundary of the class** (non-additive `g` with mixed differences close to `c`):
   the dip construction needs slack `c₀`; the bracket is between radii for `c₀` and for `2c`.
5. **Sparse graphs**: the overhead `N₂ − (n+1)` on a chain as `n → ∞` (bounded? linear with a small
   constant?), and a formula in terms of the graph for triangle-free graphs.  The exact data
   (`≤ n+2` for `n ≤ 5`) show that entangled designs beat the natural ones; I have no lower bound beyond
   `n+1` and no construction beyond these sizes.
6. **Pairwise subclass between `e ≈ c√n` and `e ≈ cn/3`**: `N₂^{pair}` lies between `n+1` and `Θ(n²)`;
   §2.8(b),(c) are proof sketches without numerical confirmation.
7. The asymptotic constant of `r_n(n+1)` (best simplex for sup-norm recovery): between `n²/8` and the
   path simplex `≈ n²/4`.
8. The exact `n = 6` step function below `θ = 5/4`, and the chain with `n = 6` at `θ = 1/2`: the
   hitting-set runs (`t20_n6_levels`, `t06c_chain 6 0.5`) were stopped unfinished after about 30 minutes
   each on a loaded machine.

---

## 6. The three most promising next steps

1. **Prove (or refute) Conjecture E′** — the cleanest open statement: "`n+1` evaluations certify iff
   `e ≥ cn/3`".  A proof in the pairwise subclass suffices.  Route: `err(y) = ½‖M(μμᵀ−diag μ)Mᵀ‖₁`; the
   two tests `y = e_i`, `y = 1` give `n/4`; the missing ingredient is a third family of tests playing the
   role of the set `U` of Theorem E(c) for a general simplex (for a direct sum of blocks the cross terms
   alone give `Σ_{r<r′}n_rn_{r′}/n`).  Then attack the window `(1/4, 1/3)` with "tree + corrections"
   designs and the same adversaries.
2. **Put Theorems A–C and Corollary D into the report as the resolution of §12 item 4** (and of the
   sentence "whether other evaluation sets do better is open" in §11.7): they are short, they have the
   same shape as Theorems 11.8–11.9 (dichotomy + exponent, with `R₁ = R*`), they extend to order `m`, to
   `k` states and to randomised algorithms, and Theorems A and B(b) are already machine-checked against
   `MixedDiffBound` (`lean/StarsDoNotCombine.lean`; it can be moved next to `SecondOrderEnvelope.lean`
   as it stands, and the order-`m` dip is the same proof with `C(·,m)`).  Replace the row-sum condition by the density (min-cut) criterion of
   Proposition F(d), and "a star" by "a spider" where `n+1` evaluations are discussed.
3. **Make the sparse case the positive story**: for bounded-degree coupling graphs the class is a
   `κ(G)`-dimensional polytope and certification is a *linear* design problem (`N₂ ≤ κ(G) ≤ 1+n·2^Δ`,
   exact small cases `≤ n+2`); determine the optimal overhead on chains and trees (the entangled designs
   of §2.7), and combine with a certified choice of the constants `c_ij` for one concrete residual — the
   interface that §12 item 4 calls hypothetical becomes a finite-dimensional, polynomial problem exactly
   when the coupling graph has small cliques.
