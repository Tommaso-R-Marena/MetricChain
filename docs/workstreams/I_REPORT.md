# Workstream I — isoperimetry on product spaces by induction over the sites: tail functions for the level theorem beyond the uniform cube

*Coordinator's own work, 2026-11-26/27, after the twenty-fourth checkpoint.  **Unrefereed.**
Labels: **[P]** paper proof in this file; **[N]** numerical (floating point unless "exact" is
said); **[C]** conjecture; **[K]** known.  Scripts and stored outputs:
`experiments/workstreams/I/`; harness test XXVII.1 (nine mutations, all caught) and the
documented refutation DEAD.29.  Nothing here is machine-checked.*

## I0. Why, and what is established

The level theorem on an arbitrary probability space (theory report, Theorem 11.118) needs two
functions of the outer integrand `V` — an upper tail function `Ξ` and a lower tail function `Θ`,

    (TU)   μ(V > s) ≤ q   ⟹   E(V − s)₊ ≤ s·Ξ(q),            (TL)   μ(V ≥ s) ≥ q   ⟹   E min(V, s) ≥ s·Θ(q),

*valid* at the finite size at hand ("a tail function that is too small costs validity").  For the
class of an envelope `ρ` (`V(x) ≤ V(z)e^{ρ(x,z)}`) they are isoperimetric quantities:

    Ξ_ρ(q) = sup{ ∫_D (e^{ρ(x → Dᶜ)} − 1) dμ : μ(D) ≤ q },        Θ_ρ(q) = inf{ ∫ e^{−ρ(S → z)} dμ(z) : μ(S) ≥ q }.

On the uniform cube with one slope Harper's theorem evaluates both (Lemma 11.43, Theorem 11.56).
Beyond it the programme had: for a field, an asymptotic statement with an error of the
typical-subset kind (`ω_n ≈ 2n^{−1/8}`, Theorem 11.63); for several slopes at finite `n`, a valid
bound that is not sharp (the sorted-slope bound, Lemma N14 of workstream N) — the gap that the
engineering division's work on cubes with site-dependent slopes names ("a sharp tail function
for an outer block that mixes types"), and that the Scientific Discovery Division's question on
the `p`-biased cube asks about.

**What is established here.**

1. **A growth bound by induction over the sites (Lemma I1) [P].**  For any product of finite
   sites with a product measure and an additive cost, the two-point recursion
   `g_{k+1}(m, t) = inf Σ_y μ(y)·max_x g_k(m_x, t − c(x, y))` over fibre measures with
   `Σ_x μ(x) m_x ≥ m` is a valid lower bound of `μ(E_t)` over all sets with `μ(E) ≥ m`.
   **[N]** It reproduces Harper's theorem at ball sizes on the uniform cube to the accuracy of
   the grid (`n = 12`: within `0.04` nats, of the order of the grid slack), is attained on every
   exhaustively enumerated instance (three products of four sites, uniform, two costs, biased
   with asymmetric costs: 65 534 sets each), and on the biased cube it gives the values of the
   balls around the **rare** vertex (`n = 14`, `p = 0.2`: within `0.11` nats) wherever those are
   not yet the whole cube.
2. **Both tail functions from a growth bound (Proposition I2) [P]**, valid for every set by
   construction; on the exhaustive instances within `2.2` per cent (upper) and attained (lower).
3. **An exact tensorisation for the lower tail (Theorem I3) [P]**: for every set `E` and every
   `λ ≥ 0`, `∫ e^{−λ c(E, y)} dμ(y) ≥ exp(−Φ_n^λ(ln 1/μ(E)))`, with `Φ_n^λ` the max-plus
   convolution of concave single-site functions — no error term, any finite product, any
   costs.  Hence `Θ(q) = exp(−Φ_n¹(ln 1/q))` is a valid lower tail function **in closed form**
   for cubes with site-dependent slopes and biases; on the uniform cube it is `≈ 2/√n` times
   the exact one for `n = 32 … 2048`.
4. **A composition lemma for blocks (Lemma I4) [P]**: growth bounds of two factors give a
   growth bound of the product with a loss of a factor `2⌈log₂(2/m)⌉` in the measure; with
   Harper in each block this gives, for a uniform cube with a fixed number of slope types,
   closed-form tail functions that are sharp up to polynomial factors.
5. **Four negative results** (I5): a "Harper theorem for the biased cube" is false in the
   concentration regime (exhaustive, `n ≤ 4`); the piecewise-linear interpolation of ball
   values is not preserved by the induction on a biased cube; the natural one-dimensional
   recursion for `Ξ` is valid, exact on small cases and exponentially lossy; Laplace
   inequalities at all scales do not imply pointwise growth.
6. **A conjecture with numerical support (I6) [C, N]**: the Chernoff (single-letter) potential
   fails the induction step of Lemma I1 by at most `c₀/n` (`n·defect ≤ 0.632` for the uniform
   cube, `n ≤ 1000`, the value `1 − 1/e` being attained at single points), which would give a
   closed-form growth bound on every finite product space that is sharp up to a factor
   `n^{−c₀}` — the true order on the cube is `n^{−1/2}`.

**What it is not.**  Not a theorem for all `n` in closed form with polynomial precision beyond
the uniform measure (that is the conjecture).  The DP is floating point with rounding
*directions* that keep it valid, not interval arithmetic.  For a field (a biased product
measure) the right reference of the *algorithm* is not the zero instance (theory report
§11.20), so tail functions relative to the zero instance — which is what this workstream
provides for biased measures — do not by themselves give the optimal exponent there.

## I1. The growth induction

**Setting.**  Finite sets `X_1, …, X_n`; probability measures `μ_i` of full support; costs
`c_i : X_i × X_i → [0, ∞)` with `c_i(x, x) = 0` (no symmetry, no triangle inequality needed);
`X = ΠX_i`, `μ = ⊗μ_i`, `c(x, y) = Σ_i c_i(x_i, y_i)`.  For `E ⊆ X`, `t ≥ 0`:

    E_t := { y : c(x, y) ≤ t for some x ∈ E },        c(E, y) := min_{x ∈ E} c(x, y).

A *growth bound* is a function `g(m, t)`, nondecreasing in both arguments, with `g(0, ·) = 0`,
`g(·, t) := 0` for `t < 0`, and `μ(E_t) ≥ g(μ(E), t)` for every nonempty `E`.

**Lemma I1 [P].**  *Write `X = X_1 × X′`, and for `E ⊆ X` let `E_x := {x′ : (x, x′) ∈ E}` be its
fibres.  Then for every `t ≥ 0` and every `y ∈ X_1`*

    (E_t)_y  =  ⋃_{x : c_1(x,y) ≤ t} (E_x)_{t − c_1(x,y)}        (neighbourhoods in X′),

*and therefore, for a growth bound `g′` of `X′`,*

    μ(E_t)  ≥  Σ_y μ_1(y) · max_x g′( μ′(E_x), t − c_1(x, y) ).

*Hence `g(m, t) := inf{ Σ_y μ_1(y)·max_x g′(m_x, t − c_1(x, y)) : m_x ∈ [0, 1], Σ_x μ_1(x) m_x ≥ m }` is a
growth bound of `X`.*

*Proof.*  `(y, y′) ∈ E_t` iff there is `(x, x′) ∈ E` with `c_1(x, y) + c′(x′, y′) ≤ t`, i.e. iff `y′`
lies in the `(t − c_1(x, y))`-neighbourhood of `E_x` for some `x` with `c_1(x, y) ≤ t`.  The measure of
a union is at least the largest measure of its members, `μ′((E_x)_s) ≥ g′(μ′(E_x), s)`, and
`μ(E) = Σ_x μ_1(x) μ′(E_x)`.  Monotonicity of `g` in `m` and `t` is inherited.  ∎

Starting from the one-point space (`g_0(m, t) = 1` for `m > 0`) and adding the sites one at a
time gives a growth bound `g_n` of any product.  The only inequality used is "union ≥ maximum":
the recursion is exact whenever the neighbourhoods contributed by the different letters are
nested — which is what happens for balls.

**I1.3 The recursion on a grid.**  `i1_dp_growth.py`, `tail_product.py`: `−ln m` on a grid of
step `h`; a table `G[t, k] ≤ g(e^{−kh}, t)`.  For a real set with fibre measures `(m_0, m_1)` and
`μ(E) ≥ e^{−kh}` round each fibre measure *down* to the grid (`g′` is nondecreasing; a fibre
below the grid counts as empty): the rounded pair satisfies the constraint relaxed by the
factor `e^{−h}`, so the minimum over grid pairs with the relaxed constraint is a valid value
of `G[t, k]` for the *exact* threshold `e^{−kh}`.  The relaxation costs sharpness — a slack of
`h` per site in `−ln m` — not validity.  (The arithmetic is floating point; an interval
version is not written.)  Cost: `O(K²)` per site and budget for `K` grid points.

**I1.4 Numbers [N].**
* *Uniform cube against Harper* (`out_i1_dp_growth_n12.txt`): `n = 12`, `h = 0.01`; at the measure of
  the ball of radius `r` and budgets `t ∈ {1, 2, 3, 6}` the bound is within `0.037` nats of the
  ball of radius `r + t`, and equal to it (to four digits) for `r ≤ 1`.  The loss is of the
  order of the built-in slack `n·h = 0.12`.
* *Biased cube* (`out_i2_biased_n14_p0.2.txt`): `n = 14`, `P(x_i = 1) = 0.2`.  Among the sets
  `{a ≤ |x| ≤ b}` the ones closest to the bound are the balls around the **rare** vertex,
  `{|x| ≥ n − r}` (within `0.11` nats for all `r`, `t ≤ 3`; exactly attained for `r = 0`); the
  balls around the likely vertex are above it, by up to `0.5` nats at small radii.  No
  candidate is below.
* *Exhaustive* (`out_tail_product.txt`; harness XXVII.1 on products of three sites, without a
  grid): on three products of four sites — uniform; costs `(1, 1, 2, 2)`; laws
  `(0.5, 0.3, 0.2, 0.6)` with asymmetric costs — all 65 534 proper nonempty subsets satisfy
  the bound at every budget, and the bound is attained (ratio `1.0000`).

## I2. Tail functions from a growth bound

**Proposition I2 [P].**  *Let `g` be a growth bound for the cost `c = ρ` (so `ρ(x → Dᶜ) = c(x, Dᶜ)` and
`ρ(S → z) = c(S, z)`), and `M(q, t) := sup{ m : g(m, t) ≤ q }` (`:= 0` if there is none).  Then*

    Ξ(q) := ∫_0^∞ e^t · M(q, t) dt        and        Θ(q) := ∫_0^∞ e^{−t} · g(q, t) dt

*are an upper and a lower tail function of the class of `ρ`.  For costs in multiples of a unit
`u`: `Ξ(q) = Σ_{j≥1} (e^{uj} − e^{u(j−1)})·M(q, u(j − 1))` and `Θ(q) = Σ_{j≥0} (e^{−uj} − e^{−u(j+1)})·g(q, uj)`.*

*Proof.*  (TU): let `D = {V > s}`, `μ(D) ≤ q`.  For `x ∈ D`, `V(x) ≤ s·e^{c(x, Dᶜ)}`, so
`E(V − s)₊ ≤ s∫_D (e^{c(x,Dᶜ)} − 1)dμ = s∫_0^∞ e^t μ(I_t)dt` with `I_t := {x ∈ D : c(x, Dᶜ) > t}`.  A point
within cost `t` of `I_t` is in `D`, so `g(μ(I_t), t) ≤ μ((I_t)_t) ≤ μ(D) ≤ q`, i.e. `μ(I_t) ≤ M(q, t)`.
(TL): let `S = {V ≥ s}`, `μ(S) ≥ q`.  `min(V(z), s) ≥ s·e^{−c(S, z)}`, and
`∫ e^{−c(S,z)}dμ(z) = ∫_0^∞ e^{−t} μ(S_t) dt ≥ ∫_0^∞ e^{−t} g(q, t) dt`.  The lattice forms are Abel
summations.  ∎

On the uniform cube with Harper's `g`, both are the exact functions at ball sizes.  **[N]** With
the grid recursion (`out_tail_product.txt`): on the three exhaustive instances every set
satisfies (TU) and (TL), the closest ratios being `0.978`–`0.981` (upper) and `1.0000` (lower);
on the uniform cube `n = 14`, `u = 1`, `h = 0.005` the derived functions are within `6.2` per cent
(upper) and `4.2` per cent (lower) of the exact ones at ball sizes — the size of the grid slack `n·h = 0.07`.

## I3. The Laplace functional: an exact tensorisation, and the lower tail in closed form

For a site `(X_i, μ_i, c_i)`, `λ ≥ 0`, and a law `P` on `X_i` put

    r_i^λ(P) := min_Q [ D(Q‖μ_i) + λ·T_{c_i}(P, Q) ]         (T the optimal transport cost; Q = P is allowed, so r ≤ D(P‖μ_i)),
    φ_i^λ(d) := sup{ r_i^λ(P) : D(P‖μ_i) ≤ d },        φ̂_i^λ := its least concave majorant on [0, ∞),
    Φ_n^λ(d) := sup{ Σ_i φ̂_i^λ(d_i) : d_i ≥ 0, Σ_i d_i = d }        (nondecreasing, concave, ≤ d).

**Theorem I3 [P].**  *For every probability measure `ν ≪ μ` on the product and every `λ ≥ 0`
there is a coupling `(X, Y)`, `X ∼ ν`, with*

    D(P_Y‖μ) + λ·E c(X, Y)  ≤  Φ_n^λ( D(ν‖μ) ).

*Consequently, for every nonempty `E ⊆ X`:  `∫ e^{−λ c(E, y)} dμ(y) ≥ exp( −Φ_n^λ( ln 1/μ(E) ) )`.*

*Proof.*  Let `p_i(· | x^{i−1})` be the conditional laws of `ν`, and `W_i(· | x_i; x^{i−1})` a kernel
attaining `r_i^λ(p_i(· | x^{i−1}))` (the optimal coupling of `p_i` with the optimal `Q`).  Given `X`,
draw the `Y_i ∼ W_i(· | X_i; X^{i−1})` independently.  Given `X^{i−1}`, the pair `(X_i, Y_i)` is
independent of `Y^{i−1}` (which is a function of `X^{i−1}` and of independent randomness), so
`P(Y_i ∈ · | X^{i−1}, Y^{i−1}) = p_iW_i =: Q_i(· | X^{i−1})`, and `P_{Y_i | Y^{i−1}}` is a mixture of the
`Q_i(· | X^{i−1})`.  By the chain rule against the product measure and convexity of the
relative entropy,

    D(P_Y‖μ) = Σ_i E D(P_{Y_i|Y^{i−1}}‖μ_i) ≤ Σ_i E D(Q_i(· | X^{i−1})‖μ_i),        E c(X, Y) = Σ_i E T_{c_i}(p_i, Q_i),

so the left side of the claim is at most `Σ_i E r_i^λ(p_i(· | X^{i−1})) ≤ Σ_i E φ̂_i^λ(D_i)`, with
`D_i := D(p_i(· | X^{i−1})‖μ_i)`; by Jensen this is at most `Σ_i φ̂_i^λ(E D_i) ≤ Φ_n^λ(Σ_i E D_i)`, and
`Σ_i E D_i = D(ν‖μ)` (chain rule).  For the consequence take `ν = μ(· | E)`, for which
`D(ν‖μ) = ln 1/μ(E)`; by the variational formula for the logarithm of an exponential integral,
`ln ∫ e^{−λ c(E,y)}dμ ≥ −D(P_Y‖μ) − λ E c(E, Y)`, and `c(E, Y) ≤ c(X, Y)` because `X ∈ E`.  ∎

**Corollary I3.1 (lower tail function in closed form) [P].**  `Θ(q) := exp(−Φ_n¹(ln 1/q))` (the
envelope as cost, `λ = 1`) satisfies (TL): `∫ e^{−ρ(S → z)}dμ ≥ exp(−Φ_n¹(ln 1/μ(S))) ≥ Θ(q)` for
`μ(S) ≥ q`.

**Symmetric binary sites.**  For a uniform bit with flip cost `u` and `λ = 1`: with
`k(x) := KL(x‖½)`, `π(d) := k^{−1}(d) ∈ [½, 1]`, `σ_u := e^u/(1 + e^u)`,

    φ_u(d) = d   for π(d) ≤ σ_u,        φ_u(d) = k(σ_u) + u·(π(d) − σ_u)   for π(d) ≥ σ_u,

concave and `C¹`.  For `n_j` sites of slope `u_j` (`j = 1, …, J`) the maximum in `Φ` is attained at a
common slope `θ ∈ (0, 1]`: `π_j = e^{u_j/θ}/(1 + e^{u_j/θ})`, `d = Σ_j n_j k(π_j)`,
`Φ = Σ_j n_j[k(σ_{u_j}) + u_j(π_j − σ_{u_j})]`, and `Φ(d) = d` for `d ≤ Σ_j n_j k(σ_{u_j})` — the "one slope
common to all types" of the exponents of theory report §11.26, now as an inequality at every `n`.

**Sharpness [N].**  On the uniform cube, `u = 1`, the closed form is `0.40, 0.20, 0.094, 0.042` times
the exact lower tail function (worst ball size) at `n = 32, 128, 512, 2048`: a factor `≈ 2/√n`,
the gap between a Chernoff bound and a binomial tail.  On the three exhaustive instances
of four sites it is valid for every set and attained within `0.15` per cent.

## I4. Two blocks

**Lemma I4 [P].**  *Let `(X_1, μ_1, c_1)`, `(X_2, μ_2, c_2)` have growth bounds `g_1`, `g_2`, and put
`F_t(a, s) := sup{ g_1(a, t_1)·g_2(s, t_2) : t_1 + t_2 ≤ t }`.  For `E ⊆ X_1 × X_2` with fibre measures
`m_a := μ_2(E_a)` and `A_s := {a : m_a ≥ s}`:*

    μ(E_t) ≥ F_t( μ_1(A_s), s )   for every s with A_s ≠ ∅,        μ(E) = ∫_0^1 μ_1(A_s) ds,

*hence `μ(E_t) ≥ v*(μ(E), t)`, `v*(m, t) := inf{ v : ∫_0^1 sup{a : F_t(a, s) ≤ v} ds ≥ m }`, and in particular*

    μ(E_t)  ≥  min{ F_t(a, s) : a·s ≥ m/(2K) },        m = μ(E),   K = ⌈log₂(2/m)⌉.

*Proof.*  For `a′` within cost `t_1` of some `a ∈ A_s`, the fibre `(E_t)_{a′}` contains `(E_a)_{t_2}`, of
measure at least `g_2(s, t_2)`; integrate over `a′ ∈ (A_s)_{t_1}`, of measure at least `g_1(μ_1(A_s), t_1)`.
The layer-cake formula gives `μ(E)`.  If `F_t(μ_1(A_s), s) ≤ v` for all `s`, then
`μ_1(A_s) ≤ sup{a : F_t(a, s) ≤ v}` and integration gives the statement on `v*`.  Pigeonhole: the
integral over `(0, 2^{−K}]` is at most `2^{−K} ≤ m/2`, so one of the `K` dyadic intervals
`(2^{−k−1}, 2^{−k}]` carries at least `m/(2K)`; `μ_1(A_s)` is nonincreasing, so with `s = 2^{−k−1}`,
`a = μ_1(A_s)`: `a·s ≥ m/(2K)`.  ∎

**Corollary I4.1 (several slopes on the uniform cube) [P, given Harper's theorem].**  For blocks
`Q_{n_1}, …, Q_{n_J}` with uniform measures and flip costs `u_1, …, u_J`, take Harper's exact function
in each block (piecewise linear between ball sizes, which is valid by the normalised matching
property) and compose `J − 1` times: the result is a growth bound in closed form whose
minimisers are products of balls, with a loss of a factor at most `Π(2K)` in the measure — and
the neighbourhood of a product of balls is a union over at most `Π(t/u_j + 1)` budget splits.
So for a fixed number of types the bound is sharp up to polynomial factors.  **[N]**
(`out_i8_blocks.txt`.)  Exhaustive on `Q_2 × Q_2` with costs `(1, 2)`: `v*` is below the true minimum
for every cardinality and budget (smallest ratio `0.28`); for `n_1 = n_2 = 10` it is `0.10`–`0.50` of
the neighbourhood of a product of two balls.  The site-by-site recursion of I1 is sharper and
costs more; the composition is the closed form.

## I5. What is not true

**(a) There is no Harper theorem for the biased cube in the concentration regime [N, exact].**
`i6_bruteforce_biased.py`: all subsets of `Q_n`, `n ≤ 4`, `P(x_i = 1) = p ∈ {1/10, 1/5, 1/3, 2/5, 1/2}`, exact
rational arithmetic, 95 cases `(n, p, r, t)`.  In all 78 cases in which the `t`-neighbourhood
of the ball `U_r = {|x| ≥ n − r}` around the rare vertex is not the whole cube, **the ball is an
exact minimiser** of `μ(E_t)` among sets with `μ(E) ≥ μ(U_r)`.  In the 17 cases in which it is the
whole cube, some set of at least that measure has a smaller neighbourhood (for `p ≤ 1/3`; e.g.
`n = 3`, `p = 1/5`, `r = 1`, `t = 2`: `0.968 < 1`) — a set near the likely vertex has large measure and
small radius.  Harness DEAD.29.  (Bollobás and Leader's exact inequality for the weighted cube
is for down-sets.)

**(b) The piecewise-linear interpolation of ball values is not preserved by the induction on
a biased cube [P].**  Let `w_j = P(Bin(n, q_0) = j)` (`q_0 = 1 − p ≥ ½`), `C` its distribution function,
`A_j = C(j − 1) + q_1w_j` the measure of the ball of radius `j` around the rare vertex of `Q_{n+1}`, and
`B_j = C(j − 1) + q_0w_j` that of the ball around a vertex with one likely letter.  The linear
interpolation of the `B`-balls at the measure `A_j`, grown by one, has measure

    A_{j+1} − q_1(q_0 − q_1)(w_j² − w_{j−1}w_{j+1}) / (q_0w_j + q_1w_{j−1})   <   A_{j+1}

(log-concavity of the binomial weights; checked numerically).  No real set has that measure
and that neighbourhood — at the sizes of the `B`-balls themselves the inequality goes the
right way — but the recursion of Lemma I1 fed with the *interpolated* function admits it.
On the uniform cube the two families coincide and the interpolation is inductive
(Bollobás–Leader's fractional form of Harper's theorem).  The recursion with the exact step
functions (I1.3) does not have this defect; a closed form must interpolate differently
(I6).

**(c) The one-dimensional recursion for `Ξ` is valid, exact on small cases, and exponentially
lossy [P for validity; N].**  `U(A) := ∫ e^{ρ(x → A)}dμ` satisfies
`U(A) ≤ Σ_x μ_1(x)·min_y e^{c_1(x,y)} U′(A_y)` ("integral of a minimum ≤ minimum of integrals"), so
`1 + Ξ_{k+1}(q) := sup{ Σ_x μ_1(x) min_y e^{c_1(x,y)}(1 + Ξ_k(s_y)) : Σ_x μ_1(x)s_x ≤ q }` is an upper tail
function; likewise for `Θ` with a maximum.  It needs one variable instead of two.  It is exact
for the cubes of dimension one and two (worked by hand).  But a set confined to one fibre is charged the
integral of its depth *inside the fibre*, capped at `e^u − 1`, although every one of its points
leaves at cost `u`: with `Ξ` superadditive the recursion prefers `½Ξ_k(2q)` to the ball's value,
and iterating, a ball of the critical radius inside a subcube.  On the uniform cube this
gives `Ξ^{rec}(e^{−nα}) ≥ exp(−n·ln 2·(α − h)/(ln 2 − h))` (`h` the hinted exponent), above the true
`≈ e^{−nα}` for every `h < α < ln 2`; the rate is small (`0.02` per site at `α = 0.21`, `u = 1`), which
is why the measured ratio is only `2.7` at `n = 16` and `7.2` at `n = 32` (`out_i3_tail_dp_n*.txt`, grid
step `0.005`).  The lower recursion loses `0.82`, `0.65` at the same sizes.  Use the growth bound (I1, I2).

**(d) Laplace inequalities at all scales do not imply growth at a given radius.**  Theorem I3
applied to every neighbourhood `E_s` gives `∫_0^∞ λe^{−λr} μ(E_{s+r}) dr ≥ exp(−Φ^λ(ln 1/μ(E_s)))` for all
`s, λ`.  The profile that stays at `μ(E)` until `r = inf_λ Φ^λ(d)/λ` and then jumps to one satisfies
all of them.  A bound at a fixed radius needs the two-variable induction.

## I6. A conjecture: the Chernoff potential is inductive up to `n^{−c}`

For identical sites let `Γ_n(d, t) := sup_{λ≥0} [Φ_n^λ(d) − λt]`.  On the uniform cube with unit cost,
`Γ_n(d, t) = n·k(max(π(d/n) − t/n, ½))` — the exponent of the ball of measure `e^{−d}` grown by `t`.

**Conjecture I6 [C].**  *There is `c₀` (depending on the sites only) such that
`G_n(m, t) := (e·n)^{−c₀}·exp(−Γ_n(ln 1/m, t))` satisfies the recursion inequality of Lemma I1, and is
therefore a growth bound, for every `n`.*

*Evidence [N]* (`out_i4_potential_defect.txt`, `out_i5_defect_corners.txt`; uniform cube, unit cost).
The defect of `e^{−Γ}` in the recursion,
`−ln[½max(e^{−Γ_n(d_0,t)}, e^{−Γ_n(d_1,t−1)}) + ½max(e^{−Γ_n(d_1,t)}, e^{−Γ_n(d_0,t−1)})] − Γ_{n+1}(d, t)`, maximised
over the fibre exponents `(d_0, d_1)` and the budget, is between `0.42/n` and `0.50/n` in the
interior for `n = 20 … 1000`, and at most `0.632/n` anywhere searched — the value `(1 − 1/e)/n`, attained at a
single point with one fibre empty and `t = 1` (there it is exact:
`ln[(1 + 1/n)/(1 + 1/(en))]`).  Summed over the sites this is a factor `n^{−0.64}`; the truth on the
cube is `n^{−1/2}` (a binomial tail against its Chernoff bound).
*Why `≈ ½/n`.*  For a fixed `λ` the step is exact: by the proof of Theorem I3,
`min_W [D(p_1W‖μ_1) + λ·cost + Σ_x p_1(x)Φ_n^λ(d_x)] ≤ Φ_{n+1}^λ(d)`.  The defect is the mean, under the
optimal one-site kernel, of the gap `Γ_n(d′, t′) − [Φ_n^λ(d′) − λt′]` at `(d′, t′) = (d_X, t − c_1(X, Y))` — a
Bregman divergence of the convex function `Γ_n(d′, ·)`, of size `½·∂_t²Γ_n·Var`.  The curvature
`∂_t²Γ_n` is the reciprocal of the total variance of the cost under the tilted kernels, and the
fluctuation is the variance of one site: `½·Var_1/Σ_i Var_i` — the increments of
`½ ln(total variance)`, the local-limit prefactor.  A proof has to make this uniform at
the corners (few points; small budgets; the edge `Γ = 0`), where the numbers above say
it stays true.
*A second candidate* (`out_i7_beta_potential.txt`).  Binomial tails with a *real* radius
(the regularised incomplete beta function, for which Pascal's rule holds) are an almost
exact sub-solution of the recursion on the uniform cube (largest violation `5·10^{−5}` at
`n = 6`, below `10^{−6}` at `n = 12, 24`), and around the rare vertex of a biased cube violate
it only where the neighbourhood has measure above `0.99` (`6·10^{−3}` at `n = 12`, `7·10^{−4}` at
`n = 24`, `p = 0.2`); around the likely vertex they fail by `0.10`.

## I7. Prior art, and what is ours

* Harper (1966): exact vertex isoperimetry on the uniform cube **[K]**.  Bollobás and Leader,
  "Isoperimetric inequalities and fractional set systems" (J. Combin. Theory A 56, 1991): the
  weighted cube, for down-sets, by fractional set systems **[K; abstract and a review read]**.
* Ahlswede and Zhang (asymptotic isoperimetric problem; finite alphabets), and Lei Yu, "Exact
  exponents for concentration and isoperimetry in product Polish spaces" (arXiv 2205.07596):
  variational formulas for the exponents, asymptotic in the isoperimetric regime, and a
  dimension-free bound in the concentration regime (its Theorem 1(1) and Corollary 1, an
  improved Talagrand inequality) **[K; introduction and Section II-A read through a fetch, the
  rest by a summary]**.  Marton; Gozlan and Léonard: transport–entropy inequalities and
  their tensorisation.
* **Theorem I3** is a tensorisation of a transport–entropy inequality by the chain rule
  (Marton's coupling with the exact single-letter trade-off in place of Pinsker's
  inequality).  We did not find it in the form of a Laplace functional of the distance to a
  set of given measure, and the fetched text of Yu's paper has no inequality of that form;
  the method is standard and **no novelty is claimed** beyond the statement's use as a
  lower tail function valid at every `n`.
* **Lemma I1** is the natural induction (it is how Talagrand-type inequalities and the
  fractional form of Harper's theorem are proved).  What is ours is its use as a
  *computation* that produces valid tail functions for the level theorem on heterogeneous
  products, the observation that with exact step functions it reproduces Harper's values and
  the rare-vertex balls, and the negative results of I5.  **Not searched:** whether the
  rare-vertex statement of I5(a) in the isoperimetric regime, or Conjecture I6, are in print.

## I8. What this gives the programme, and what stays open

* **Theorem 11.118 can now be run on a block that mixes slopes (and biases)** with tail
  functions that are valid at the block's size and sharp where sharpness can be tested: the
  recursion of I1 with Proposition I2 for blocks of moderate size (cost `O(n·T·K²)`), the closed
  form of Corollary I3.1 for the lower side at any size, and Corollary I4.1 for a fixed number
  of slope types at any size, up to polynomial factors.  This is the missing input named by
  the engineering division for mixed outer blocks; whether mixed blocks then beat blocks of
  one type at the sizes it computes is for its recursion to say.
* **Open.**  (1) Conjecture I6 — a closed-form growth bound with polynomial precision on every
  finite product space; with it Lemma 11.58b – Theorem 11.58e would transfer to cubes with
  several slopes with the same second-order terms (not written: the transfer also needs the
  exponent functions of §11.26 with polynomial error).  (2) Whether the balls around the rare
  vertex are exact minimisers whenever their neighbourhood is not the whole cube (true in 78
  of 78 exhaustive cases).  (3) An interval-arithmetic version of the recursion (a
  certificate), and a faster one (the minimisation over the split is one-dimensional and
  local).  (4) For a field: tail functions *relative to the flat-histogram reference* of
  Theorem 11.63 with polynomial precision — the reference is a mixture of product measures
  (`μ_H(x) ≥ Qⁿ(x)/(n + 1)` for every product `Qⁿ`), so the present tools apply to each `Qⁿ`, but
  the type-dependent budget of that theorem is not an additive cost.
* **Not done:** no referee; no Lean; no end-to-end run of the level algorithm with these
  tail functions.

## I9. Reproduction

```
python3 -B experiments/workstreams/I/tail_product.py              # exhaustive validity (three products of four sites); cube against Harper (25 s)
python3 -B experiments/workstreams/I/i1_dp_growth.py 12 0.01 0.5    # the growth recursion against Harper
python3 -B experiments/workstreams/I/i2_biased_compare.py 14 0.01 0.2
python3 -B experiments/workstreams/I/i3_tail_dp.py 32 1.0 0.005     # the one-dimensional recursions (lossy)
python3 -B experiments/workstreams/I/i4_potential_defect.py         # the defect of the Chernoff potential
python3 -B experiments/workstreams/I/i5_defect_corners.py
python3 -B experiments/workstreams/I/i6_bruteforce_biased.py        # exhaustive, exact: rare-vertex balls
python3 -B experiments/workstreams/I/i7_beta_potential.py           # binomial tails with a real radius
python3 -B experiments/workstreams/I/i8_blocks.py                   # the composition lemma (several minutes)
python3 -B experiments/falsify_conjectures.py --only XXVII ;  python3 -B experiments/falsify_conjectures.py --only DEAD.29
```
