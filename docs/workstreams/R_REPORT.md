# Workstream R — the rate of the level recursion is exactly `2π²h²θ_hint″(0)/k²`

*Written by the coordinator on 2026-11-26 (after the twenty-second checkpoint of cycle 10).
The background investigation that had been commissioned for this workstream ended without
producing any output (four consecutive answers cut off at the output limit; nothing was
written to disk), so the coordinator did the work himself.  This file replaces the report
that the brief `R_brief.md` asked for.  Everything in it is the coordinator's; statements
are labelled **[V]** (machine-checked: `proofs/Frontiers/LineDynamics.lean`), **[P]** (paper
proof below, **not yet refereed** when this file was first committed — see §12 for the
state of the reviews), **[N]** (numerical), **[C]** (conjecture or heuristic).*

## 0. Result

Let `θ = θ_na` be the non-adaptive exponent function of a pair, `h` its fixed point
(`θ(h) = h`; the hinted exponent at accuracy zero), `T_1 = θ`, `T_{k+1} = min(T_k, R[T_k])` the
level recursion of Theorem 11.52 of the theory report (`(11.18.2)`), and `τ_k = sup T_k` the
exponent of `k` nested levels at accuracy zero.

> **Theorem R [P].**  Under the hypotheses (H0), (H1) of §1 —
> `θ` convex and nonincreasing with a finite value `a > h` at zero, and the dual function `J`
> of §1 twice differentiable at its maximum with `J″ < 0` there —
>
>     lim_{k → ∞} k²·(τ_k − h)  =  2π²·h²·ϑ,      ϑ = −1/J″(L) = θ_hint″(0) = θ″(h)/(1 + |θ′(h)|)³.
>
> For the cube with slope `u` this is `2π²h²/(u²ρ_h(1 − ρ_h))` (`0.0711473 = 0.64129·a` at `u = 1`); for the
> Gaussian pair `θ(x) = (1 − √x)²` it is `π²/16`.

So "Conjecture R" of the brief is a theorem, in both directions.  The proof has four
parts, each short:

1. **A one-dimensional map.**  One level of the recursion acts on *lines*: the line with
   intercept `B` and slope `−s` becomes the line with intercept `B` and slope `−Σ(B, s)`,
   `Σ(B, s) = sup_e [B − (1 − s)θ(e)]/e` (§2).  `Σ` is a supremum of functions that are **affine in
   `(B, s)`**, hence jointly convex and nondecreasing — this trivial remark carries the whole
   upper bound.  For `B = h` the map `s ↦ Σ(h, s)` has a fixed point `L` with multiplier one
   (a saddle-node); for `B = h + δ` an orbit needs `πh√(2ϑ/δ)·(1 + o(1))` steps to pass it (§7).
2. **Lower bound [V + P]** (§4).  A line *below* `T_k` stays below `T_{k+1}` after the map
   (Lemma L, machine-checked).  Hence `τ_k ≥ B` as long as the orbit of the flat line with
   intercept `B` is finite after `k` steps.
3. **Upper bound, one level [P]** (§5).  If `T_k` lies below the upper envelope of the lines
   `{(B, W(B)) : B ≤ b}` for a **convex** nondecreasing `W`, then `T_{k+1}` lies below the upper
   envelope of the image lines `{(B, Σ(B, W(B)))}` (Lemma M, machine-checked, and Sion's minimax
   theorem).  Convexity of `W` is what the minimax theorem needs, and it cannot be
   dispensed with: propagating the lines of a majorant one by one is *not* a bound
   (`DEAD_ENDS.md` D64).
4. **A convex sub-solution [P]** (§6).  The orbit curves `p_j(B) = Σ(B, p_{j−1}(B))`, `p_0 = 0`, are
   convex in `B` (composition of the jointly convex `Σ` with a convex function).  Cut at a
   slope level `s_t` slightly above `L` and continued by their tangent lines, they stay
   convex, and — because the tangent line of a convex function is a global minorant — the
   cut curve of level `j + 1` lies below the image of the cut curve of level `j`.  The only
   thing left to check is that the cut curves stay below slope one on the relevant
   range; this is where the saddle-node enters a second time (the multiplier at the
   cut is close to one), and where a restart from the a-priori bound `τ_k → h` is used.

Both bounds are then statements about the same orbit curves, and their difference is
of lower order.

**What is new, as far as we know.**  We have not found this recursion or its rate in the
literature (the recursion comes from our own nested algorithm); the mathematics is a
classical slow passage through a saddle-node (the "ghost" of a fold bifurcation,
passage time `π/√(Aδ)`) combined with a minimax argument.  We claim no novelty for either
ingredient.

**What it means and does not mean.**  The theorem is about the recursion `R` — the *analysis*
of the nested algorithms of Theorems 11.52/11.56 at the level of exponents.  It says
that `k` nested levels have exponent `h + (2π²h²ϑ + o(1))/k²` at accuracy zero **if each level is
analysed by `R`**; it says nothing about algorithms that are not of this nested form, and
nothing by itself about finite `n` (for that the sub-exponential factors of `k` levels are
needed uniformly in `k`: workstream Q2).  Constants at finite `k` are not certified: the
proof gives `o(1)` without a rate (§11 lists what is computed).

## 1. Setting and hypotheses

**(H0).**  `θ : (0, ∞) → [0, ∞)` is convex and nonincreasing, `a := θ(0+) < ∞`, and the unique
solution `h` of `θ(h) = h` satisfies `h < a`.  (`θ` is then continuous; `0 < h`.)

The level operator, for a nonincreasing bounded `T`:

    R[T](g) = inf_{0<φ<1, 0<β<g}  sup_{γ ≥ β} [ min(γ, φ·θ((g − β)/φ)) + (1 − φ)·T(γ/(1 − φ)) ],

`T_1 = θ`, `T_{k+1} = min(T_k, R[T_k])`, `τ_k = sup T_k = T_k(0+)`.  All `T_k` are nonincreasing, nonnegative
and bounded by `a` (`BoundedAccuracy.exactRec_props` **[V]**).

**The dual function.**  For `0 ≤ t ≤ 1`,

    J(t) = inf_{e > 0} [ (1 − t)·θ(e) + t·e ].

`J` is concave; `J ≤ h` (take `e = h`); and `J(t) = h` exactly when `h` minimises the convex function
`g_t(e) = (1 − t)θ(e) + te`, that is when `−t/(1 − t)` is a subgradient of `θ` at `h`.  So `max J = h`, attained
on the interval `{r/(1 + r) : −r ∈ ∂θ(h)}`, a single point `L` exactly when `θ` is differentiable at `h`.
(Geometrically: `J(t)` is the largest intercept of a line of slope `−t` below the curve obtained
from the graph of `θ` by the shear `(x, y) ↦ (x − y, y)`; by (11.18.1) of the theory report this
curve is the graph of `θ_hint`, continued along the shear to negative arguments.  Hence
`θ_hint(x) = sup_t [J(t) − tx]`, `θ_hint(0) = h`, `θ_hint′(0) = −L`, `θ_hint″(0) = −1/J″(L)`.)

**(H1).**  `J` has a unique maximiser `L ∈ (0, 1)` and `J(t) = h − (t − L)²/(2ϑ) + o((t − L)²)` as `t → L`,
with `0 < ϑ < ∞`.

If `θ` is twice continuously differentiable near `h` with `θ″(h) > 0` then (H1) holds with
`L = r/(1 + r)`, `r = −θ′(h)`, and `ϑ = θ″(h)/(1 + r)³` (differentiate `J(t) = g_t(e*(t))`, `θ′(e*) = −t/(1 − t)`:
`J′ = e* − θ(e*)`, `J″ = (1 − θ′(e*))·de*/dt`, `de*/dt = −1/((1 − t)²θ″(e*))`).  For the Gaussian pair
`J(t) = t − t²` (`h = ¼`, `L = ½`, `ϑ = ½`, `a = 1`); for the cube `J(t) = Λ(tu) − tΛ(u)`, `Λ(v) = ln(2/(1 + e^{−v}))`
(at `u = 1`: `h = 0.02913914`, `L = 0.490034`, `ϑ = 4.244977`, `a = 0.11094407`).

**Two consequences of (H1) used below.**
(i) *The minimiser of `g_L` is unique* (it is `h`): if `e′ ≠ h` also minimised `g_L`, then
`J(t) ≤ g_t(e′) = h + (t − L)(e′ − θ(e′))` with `e′ − θ(e′) ≠ 0`, so `J` would fall off linearly on one side
of `L`.
(ii) *`L < 1 − h/a`*: always `h = J(L) ≤ g_L(0+) = (1 − L)a`; equality would make the convex function
`g_L` constant on `(0, h]`, against (i).

**The a-priori bound.**  `τ_k − h ≤ c₁/(k + c₂)` for all `k`, with explicit `c₁, c₂` depending on `(a, h)` only
(`RateFull.rate_top0` **[V]** for every `HintPair`, in particular for the cube at every slope and
for the Gaussian pair; its proof, "Step I with numbers" of the remark after Theorem
11.53, uses only that the `T_k` are nonincreasing and bounded by `a`, `θ(h) = h`, and the
continuity of `θ` at `h`).  We use it only through `τ_k → h`.

## 2. The slope map

For `B ≥ 0` and real `s` put

    Σ(B, s) = sup_{e > 0} [B − (1 − s)·θ(e)]/e   ∈ [0, ∞]

(the limit `e → ∞` gives `Σ ≥ 0`).

**(Σ1) [P, trivial].**  `Σ` is the supremum of the functions `(B, s) ↦ B/e − θ(e)/e + s·θ(e)/e`, affine in `(B, s)`
with nonnegative coefficients.  Hence **`Σ` is jointly convex, lower semicontinuous, and
nondecreasing in `B` and in `s`.**

**(Σ2).**  `Σ(B, s) < ∞` if `B < (1 − s)a`, and `Σ(B, s) = ∞` if `B > (1 − s)a` (in particular for `s ≥ 1`, `B > 0`).  On the
open half-plane `{B < (1 − s)a}` (intersected with `B > 0`) `Σ` is finite and convex, hence continuous.
We call `(B, s)` *regular* if `Σ(B, s) < ∞`.

**(Σ3).**  `σ′ = Σ(B, s)` is the least `σ′ ≥ 0` with `(1 − s)θ(e) + σ′e ≥ B` for all `e > 0`: the line `x ↦ B − σ′x` is the
*flattest* line through `(0, B)` that stays below `(1 − s)θ`.  If `0 < Σ(B, s) < ∞` the supremum is
attained, at the points `e` where this line touches `(1 − s)θ`; write `𝓜(B, s)` for the (compact,
nonempty) set of these maximisers.

**(Σ4) (the subgradient inequality).**  If `e₁ ∈ 𝓜(B₁, s₁)`, then for all `(B, s)`

    Σ(B, s) ≥ Σ(B₁, s₁) + (B − B₁)/e₁ + (s − s₁)·θ(e₁)/e₁

(evaluate the supremum at `e₁`).

**(Σ5) (through `J`).**  For `s < 1` and `w ≥ −s` put `Ψ_s(w) = inf_e [(1 − s)θ(e) + (s + w)e] = (1 + w)·J((s + w)/(1 + w))`,
concave, continuous and nondecreasing in `w`.  By (Σ3), `D(B, s) := Σ(B, s) − s = min{w ≥ −s : Ψ_s(w) ≥ B}`.
Consequences:

* `D(B, s) ≤ 0` iff `J(s) ≥ B`.  The fixed points of `s ↦ Σ(B, s)` are the solutions of `J(s) = B`: two
  for `B < h` (the lower one stable: the tangent lines of `θ_hint`), one for `B = h` (namely `L`), none
  for `B > h`.  **The hinted exponent is the saddle-node value of the slope map.**
* Since `J ≤ h`: `Ψ_s(w) ≤ (1 + w)h`, hence

      D(B, s) ≥ (B − h)/h      for all s and all B ≥ h.                                   (2.1)

* `Σ(h, L) = L`, and `𝓜(h, L) = {h}` by consequence (i) of (H1) (`e` maximises iff `g_L(e) = h`).
  Note `θ(h)/h = 1`: by (Σ4) the multiplier `∂Σ/∂s` at the fixed point is one.

**(Σ6) (the bottleneck) [P].**  *Assume (H1).  For every `ε ∈ (0, 1)` there are `η > 0` and `δ₀ > 0` such
that for all `0 < δ ≤ δ₀` and `|v| ≤ η`*

    (1 − ε)·[δ + v²/(2ϑ)]/h  ≤  D(h + δ, L + v)  ≤  (1 + ε)·[δ + v²/(2ϑ)]/h.

*Proof.*  `(h, L)` is a regular interior point by consequence (ii), so `D` is continuous there
and `w := D(h + δ, L + v) → 0` as `(δ, v) → 0`; `w ≥ δ/h > 0` by (2.1).  By continuity of `Ψ_s`, `Ψ_s(w) = h + δ`
with `s = L + v`.  The argument of `J` is `L + q`, `q = (v + (1 − L)w)/(1 + w)`, so by (H1), with `r(q) → 0`,

    (1 + w)·[h − q²(1 + r(q))/(2ϑ)] = h + δ,     that is     h·w = δ + (v + (1 − L)w)²·(1 + r(q))/((1 + w)·2ϑ).

Since `|(v + (1 − L)w)² − v²| ≤ 2|v|w + w²`: `h·w ≤ δ + (1 + |r|)(v² + (2|v| + w)w)/(2ϑ)` and
`h·w ≥ δ + (1 − |r|)(v² − 2|v|w)/((1 + w)2ϑ)`.  Solving both for `w`, with `|v| ≤ η`, `w ≤ ω`, `|r| ≤ ε′`:

    w ≤ (1 + ε′)[δ + v²/(2ϑ)] / (h − (1 + ε′)(2η + ω)/(2ϑ)),      w ≥ ((1 − ε′)/(1 + ω))·[δ + v²/(2ϑ)] / (h + η/ϑ),

and `η, δ₀` small make `ω, ε′` small.  ∎

**(Σ7) (away from the bottleneck).**  Fix `s_t ∈ (L, 1 − h/a)`.  For `B ≥ h` and `s ∈ [0, s_t]` with `|s − L| ≥ η`:
`D(B, s) ≥ D(h, s) ≥ c(η) := min{D(h, s) : 0 ≤ s ≤ s_t, |s − L| ≥ η} > 0` (monotonicity in `B`; `D(h, ·)` is
continuous on `[0, s_t]`, where `(h, s)` is regular, and vanishes only at `L`).

**The Gaussian pair [V].**  `Σ(B, s) = B(1 − s)/(1 − s − B)` for `s + B < 1` (`gauss_slope_map`,
`gauss_slope_map_least`): a Möbius map in `s`, parabolic at `B = ¼` and elliptic for `B > ¼` (§10;
nothing in the proof of Theorem R uses this).

## 3. The orbit curves

`p_0 ≡ 0`, `p_{j+1}(B) = Σ(B, p_j(B))` (`= ∞` if `p_j(B) = ∞`), for `0 ≤ B < a`.

**(P1) [P].**  *Every `p_j` is convex, nondecreasing and lower semicontinuous with values in
`[0, ∞]`; `p_j(0) = 0`; `p_j ≤ p_{j+1}`.*
*Proof.*  Induction: for `B = λB₁ + (1 − λ)B₂`, by convexity of `p_j`, monotonicity of `Σ` in `s`, and
joint convexity of `Σ`,
`Σ(B, p_j(B)) ≤ Σ(B, λp_j(B₁) + (1 − λ)p_j(B₂)) ≤ λΣ(B₁, p_j(B₁)) + (1 − λ)Σ(B₂, p_j(B₂))`.
`p_1 ≥ 0 = p_0` and monotonicity of `Σ` in `s` give `p_{j+1} ≥ p_j`.  ∎

**(P2).**  `p_j(h) ≤ L` for all `j` (`Σ(h, ·)` is nondecreasing and fixes `L ≥ 0 = p_0`).

**(P3).**  For `B > h`: `p_j(B) ≥ j·(B − h)/h` by (2.1); in particular `p_j(B) = ∞` for large `j`.

`p_1(B) = Σ(B, 0)` is the slope of the tangent line of `θ` with intercept `B`.

## 4. The lower bound

**Lemma L [V: `LineDynamics.line_le_Rstep`, `line_le_min_Rstep`].**  *Let `θ ≥ 0`, `0 ≤ σ ≤ σ′`, `T` bounded
above with `T(x) ≥ B − σx` for all `x > 0`, and `(1 − σ)θ(e) + σ′e ≥ B` for all `e > 0`.  Then `R[T](g) ≥ B − σ′g` and
`min(T, R[T])(g) ≥ B − σ′g` for all `g > 0`.*  (Proof: for any `φ, β` evaluate the bracket of `R` at
`γ₀ = max(β, μ)`, `μ = φθ((g − β)/φ)`; two cases; three lines — in `R_brief.md` §2.2 and in the Lean
file.)

**Proposition A [V for the iteration (`lines_le_exactRec`, `le_sSup_exactRec`), given Lemma L and
(Σ3)].**  *If `p_k(B) < ∞` then `T_k(x) ≥ B − p_k(B)·x` for all `x > 0`.  Hence*

    τ_k  ≥  B_∞(k) := sup{B : p_k(B) < ∞}.

*Proof.*  `k = 1`: (Σ3) with `s = 0`.  Step: Lemma L with `σ = p_k(B) ≤ σ′ = p_{k+1}(B) < ∞` (P1), whose
hypothesis is (Σ3).  ∎

## 5. The upper bound: one level, in dual form

For `b > 0` and a function `W : [0, b] → [0, 1]` put

    M_{W,b}(x) = max_{0 ≤ B ≤ b} (B − W(B)·x),      x > 0

— the upper envelope of the lines with intercept `B` and slope `−W(B)`.  It is convex and
nonincreasing with slopes in `[−1, 0]` (so `x + M_{W,b}(x)` is nondecreasing), and `M_{W,b}(0+) = b`.

**Lemma M [V: `LineDynamics.StepLE.monotoneS_step`].**  *Let `T` be nonincreasing, `T ≤ M` on `(0, ∞)`
with `x + M(x)` nondecreasing.  For `g > 0`, `e > g` with `θ(e) > 0`, and `X = g·θ(e)/(e − g)`:*
`R[T](g) ≤ (1 − g/e)·(X + M(X))`.  (This is the choice `φ = g/e`, `β → 0` in `R`; `θ` is continuous at `e`.)
If `θ(e) = 0` the same choice gives `R[T](g) ≤ (1 − g/e)·sup T` (the outer term `μ_β = φθ((g − β)/φ)` tends
to zero with `β`).

**Proposition U [P].**  *Let `b > 0`, let `W : [0, b] → [0, 1]` be convex, nondecreasing and continuous,
and let `T` be nonincreasing with `T ≤ M_{W,b}` on `(0, ∞)`.  Then for every `g > 0`*

    R[T](g)  ≤  sup{ B − Σ(B, W(B))·g  :  0 ≤ B ≤ b,  Σ(B, W(B)) < ∞ }.

*Proof.*  Write `M = M_{W,b}`, `S(X) = X + M(X)` for `X > 0` and `S(0) = b`.  `S(X) = max_{B ≤ b} [B + (1 − W(B))X]`.
By Lemma M, `R[T](g) ≤ inf_{e > g} F(e)` with

    F(e) = (1 − g/e)·S(g·θ(e)/(e − g)) = max_{(B,s) ∈ 𝓔} Φ(e; B, s),      Φ(e; B, s) = B − (g/e)·[B − (1 − s)·θ(e)],

`𝓔 = {(B, s) : 0 ≤ B ≤ b, W(B) ≤ s ≤ 1}` (for fixed `B` the maximum over `s` is at `s = W(B)`).
`𝓔` is compact and **convex because `W` is convex**.  `Φ` is affine and continuous in `(B, s)`;
in `e` it is continuous on `(g, ∞)` and quasi-convex: `{e : Φ ≤ c} = {e : g(1 − s)θ(e) + (B − c)e − gB ≤ 0}` is a
sublevel set of a convex function, because `θ` is convex and `s ≤ 1`.  By Sion's minimax theorem
(compact convex set on the side of the maximum)

    inf_{e > g} max_𝓔 Φ  =  max_𝓔 inf_{e > g} Φ.

Fix `(B, s) ∈ 𝓔` and put `N(e) = B − (1 − s)θ(e)`, concave and nondecreasing; `inf_{e>g} Φ = B − g·sup_{e>g} N(e)/e`.
The ratio `N(e)/e` is quasi-concave on `(0, ∞)` (its superlevel sets `{N(e) ≥ ce}` are intervals)
and has `limsup_{e→∞} ≤ 0`.  Three cases.
(a) `N/e` has a maximiser `e* > g` over `(0, ∞)`: then `sup_{e>g} N/e = Σ(B, s) < ∞` and the value is
`B − Σ(B, s)g`.
(b) `N ≤ 0` everywhere: then `Σ(B, s) = 0` and the value is `B = B − Σ(B, s)g`.
(c) Otherwise `N/e` is nonincreasing on `[g, ∞)` and `N(g) ≥ 0` (if the ratio increased somewhere
on `[g, ∞)` it would, being quasi-concave, be nondecreasing before that point and then
either attain a positive maximum beyond `g` — case (a) — or stay nonpositive — case (b)).
Then `sup_{e>g} N/e = N(g)/g` and the value is `(1 − s)θ(g)`.  For `e > g`, `N(e)/e ≤ N(g)/g` reads
`(1 − s)θ(e) ≥ (1 − s)θ(g) − (N(g)/g)(e − g)`, so `λ := −[(1 − s)θ]′(g+)` satisfies `0 ≤ λ ≤ N(g)/g`.  The line
`x ↦ B″ − λx` with `B″ = (1 − s)θ(g) + λg` supports `(1 − s)θ` at `g`; hence `Σ(B″, s) = λ` (by (Σ3), with
equality at `e = g`), the value is `(1 − s)θ(g) = B″ − Σ(B″, s)·g`, and `0 ≤ B″ ≤ (1 − s)θ(g) + N(g) = B`.  Since
`W` is nondecreasing, `W(B″) ≤ W(B) ≤ s`: `(B″, s) ∈ 𝓔`.
In all cases the value is `B′ − Σ(B′, s′)g` for some `(B′, s′) ∈ 𝓔` with `Σ(B′, s′) < ∞`, and
`Σ(B′, W(B′)) ≤ Σ(B′, s′)`.  ∎

**Corollary U′ (the induction step).**  *In the situation of Proposition U let
`b′ = sup{B ∈ [0, b] : Σ(B, W(B)) < ∞}` and let `W′ : [0, b′] → [0, 1]` be convex, nondecreasing and continuous
with `W′(B) ≤ Σ(B, W(B))` on `[0, b′]`.  Then `min(T, R[T]) ≤ R[T] ≤ M_{W′,b′}` on `(0, ∞)`; in particular
`sup min(T, R[T]) ≤ b′`.*  Since `Σ(B, W(B)) < ∞` forces `B ≤ (1 − W(B))·a`,

    b′ ≤ min(b, E(W)),      E(W) := the root of W(B) = 1 − B/a   (or b, if W < 1 − B/a on [0, b]).

So upper bounds for the recursion are produced by **convex sub-solutions of the slope
map**: sequences `(W_j, b_j)` with `W_{j+1} ≤ Σ(·, W_j(·))` and `W_{j+1} ≤ 1` on `[0, b_{j+1}]`.  The two
requirements pull against each other: `W_{j+1}` has to stay below the image, which blows
up near `b_{j+1}`, *and* below one, *and* convex.

*Remarks.*  (1) The *exact* dynamics of the best convex majorant is: `S_{k+1}` = the lower convex
envelope of `min(1, Σ(B, S_k(B)))` on `[0, τ_{k+1}]` with the value one at `τ_{k+1}` = the root of
`S_k(B) = 1 − B/a`; since `Σ(·, S_k(·))` is convex, this is "cut by the tangent line through
`(τ_{k+1}, 1)`".  The scripts `dual_ub_gauss.py`, `dual_ub_cube.py` iterate it on grids.  The proof below does
not use it.  (2) Convexity of `W` is used for the minimax theorem; without it the
statement is false (harness XVI.7: for the Gaussian pair the line-by-line formula gives
`τ₃ ≤ ⅓`, while `τ₃ ≥ 1/(2√2)`).

## 6. Sub-solutions by cutting the orbit curves

Fix a level `s_t ∈ (L, 1 − h/a)` and an interval `[0, b_0]` with `h < b_0 < (1 − s_t)·a`.

**Definition.**  For `j ≥ 0`: if `p_j(b_0) ≤ s_t` ("case A") put `W_j = p_j` on `[0, b_0]`.  Otherwise ("case B")
let `B_t(j) ∈ (h, b_0)` be the point with `p_j(B_t(j)) = s_t`, `m_j := p_j′(B_t(j)−) > 0` the left derivative
there, and

    W_j(B) = p_j(B)   for B ≤ B_t(j),          W_j(B) = s_t + m_j·(B − B_t(j))   for B_t(j) ≤ B ≤ b_0.

(*Well-defined.*  On `[0, b_0]`, where `p_{j−1} ≤ s_t` the point `(B, p_{j−1}(B))` is regular (`B ≤ b_0 < (1 − s_t)a`), so
`p_j` is finite and continuous on the closed interval `{p_{j−1} ≤ s_t}`, and `{p_j ≤ s_t} ⊂ {p_{j−1} ≤ s_t}`; at the
right end of that interval, if it is inside `(0, b_0)`, `p_j = Σ(B_t(j − 1), s_t) > s_t` by (2.1).  So `p_j`
crosses the level `s_t` continuously, at a point `B_t(j) < B_t(j − 1)`, in whose neighbourhood it is
finite; the crossing point is unique because a convex nondecreasing function with `p_j(0) = 0`
is strictly increasing where it is positive; `B_t(j) > h` by (P2).  Case A holds for small `j`,
case B from some `j` on, by (P3).)

**Lemma T [P].**  *(a) Every `W_j` is convex, nondecreasing, continuous, `0 ≤ W_j ≤ p_j`.
(b) `W_{j+1}(B) ≤ Σ(B, W_j(B))` for all `B ∈ [0, b_0]` and all `j ≥ 0`.*
*Proof.*  (a) The slopes of `p_j` to the left of `B_t(j)` are at most `m_j`, and a supporting line
is a minorant.  (b) `H_j := Σ(·, W_j(·))` is convex on `[0, b_0]` (as in (P1)), and `H_j = p_{j+1}` wherever
`W_j = p_j`, that is on `[0, B_t(j)]` (on all of `[0, b_0]` in case A).  If `j + 1` is in case A there is
nothing to prove.  Otherwise `B_t(j + 1) < B_t(j)`; on `[0, B_t(j + 1)]`, `W_{j+1} = p_{j+1} = H_j`; and beyond,
`W_{j+1}` is the line through `(B_t(j + 1), H_j(B_t(j + 1)))` whose slope is the left derivative of `H_j`
there — a subgradient of the convex function `H_j` at an interior point of the set where
it is finite — hence a global minorant of `H_j`.  ∎

**Proposition C (the chain) [P].**  *Suppose `T_{k₁} ≤ b_0` everywhere (that is, `τ_{k₁} ≤ b_0`).  Define
`b_{j+1} = sup{B ∈ [0, b_j] : Σ(B, W_j(B)) < ∞}`.  If*

    W_{j+1}(b_{j+1}) ≤ 1      for all 0 ≤ j < n                    (the range condition)

*then `T_{k₁+j} ≤ M_{W_j, b_j}` and `τ_{k₁+j} ≤ b_j` for all `j ≤ n`.  Moreover, for `j` in case B,*

    b_{j+1}  ≤  E_j := B_t(j) + (1 − s_t − B_t(j)/a)/(m_j + 1/a).

*Proof.*  `M_{W_0, b_0} ≡ b_0`.  Induction with Corollary U′: `W_j` restricted to `[0, b_j]` has values in
`[0, 1]` by the range condition, `W_{j+1} ≤ Σ(·, W_j(·))` by Lemma T, and `W_{j+1} ≤ 1` on `[0, b_{j+1}]` by
the range condition and monotonicity.  `E_j` is the root of `W_j(B) = 1 − B/a` (on the linear
part, because `s_t < 1 − B_t(j)/a`).  ∎

**Lemma RC (the range condition holds near the bottleneck) [P].**  *Assume (H0), (H1) and*

    (C1)   Σ(h, s_t) < 1,
    (C2)   D(h, s_t) + λ̄·(1 − s_t − h/a) < 1 − s_t,     λ̄ := max{θ(e)/e : e ∈ 𝓜(h, σ_*)},   Σ(h, σ_*) = s_t,  σ_* ∈ (L, s_t).

*Then there is `ε₁ > 0` such that for every `b_0 ∈ (h, h + ε₁]` the range condition holds for all
`j ≥ 0`.  Moreover (C1) and (C2) hold for every `s_t ∈ (L, L + η₀]`, for some `η₀ > 0`.*

*Proof.*  Let `j ≥ 0`.  If `j + 1` is in case A, `W_{j+1} = p_{j+1} ≤ s_t < 1` on `[0, b_0]`.  Let `j + 1` be in case B.
(α) *`j` in case A.*  `W_{j+1}(b_{j+1}) ≤ W_{j+1}(b_0) ≤ p_{j+1}(b_0) = Σ(b_0, p_j(b_0)) ≤ Σ(b_0, s_t)`, and `Σ(·, s_t)` is continuous at
`h` with `Σ(h, s_t) < 1`: this is `≤ 1` for `b_0 − h` small.
(β) *`j` in case B*: `h < B_t(j + 1) < B_t(j) < b_0`.  Since `b_{j+1} ≤ E_j` and `W_{j+1}` is nondecreasing it suffices that
`s_t + m_{j+1}·(E_j − B_t(j + 1)) ≤ 1`.  Now

    m_{j+1}·(B_t(j) − B_t(j + 1))  ≤  p_{j+1}(B_t(j)) − s_t  =  D(B_t(j), s_t)  ≤  D(b_0, s_t)

(convexity of `p_{j+1}`; `p_{j+1}(B_t(j)) = Σ(B_t(j), s_t)`; monotonicity in `B`), and

    m_{j+1}·(1 − s_t − B_t(j)/a)/(m_j + 1/a)  ≤  (m_{j+1}/m_j)·(1 − s_t − h/a).

*The ratio of the slopes.*  Let `B₁ = B_t(j + 1)`, `σ₁ = p_j(B₁)`, `e₁ ∈ 𝓜(B₁, σ₁)` (`Σ(B₁, σ₁) = s_t > 0`).  For `B < B₁`,
by (Σ4), `p_{j+1}(B) = Σ(B, p_j(B)) ≥ s_t + (B − B₁)/e₁ + (p_j(B) − σ₁)θ(e₁)/e₁`; dividing by `B₁ − B` and
letting `B ↑ B₁`:

    m_{j+1}  ≤  1/e₁ + (θ(e₁)/e₁)·p_j′(B₁−)  ≤  1/e₁ + (θ(e₁)/e₁)·m_j

(`p_j′(B₁−) ≤ p_j′(B_t(j)−) = m_j` by convexity, as `B₁ < B_t(j)`).  And `m_j ≥ (s_t − p_j(h))/(B_t(j) − h) ≥ (s_t − L)/(b_0 − h)`
(left derivative against a chord; (P2)).
*Uniformity.*  As `b_0 ↓ h`, uniformly in all such `j`: `B₁ → h`; `σ₁ → σ_*` (it is the solution of
`Σ(B₁, σ₁) = s_t`, and `Σ(h, ·)` is strictly increasing on `[L, s_t]`, being convex, `≥` the identity,
and equal to it at `L`); the maximisers stay in a compact subset of `(0, ∞)` and their limit
points lie in `𝓜(h, σ_*)`, so `limsup θ(e₁)/e₁ ≤ λ̄`; and `1/(e₁m_j) → 0`.  Hence

    limsup_{b_0 ↓ h} sup_j [ m_{j+1}·(E_j − B_t(j + 1)) ]  ≤  D(h, s_t) + λ̄·(1 − s_t − h/a)  <  1 − s_t

by (C2).
*(C1), (C2) near `L`.*  As `s_t ↓ L`: `Σ(h, s_t) → L < 1`; `D(h, s_t) → 0`; `σ_* → L`, `𝓜(h, σ_*) → 𝓜(h, L) = {h}`, so
`λ̄ → θ(h)/h = 1`; the left side of (C2) tends to `1 − L − h/a`, the right side to `1 − L`.  ∎

The margin in (C2) at the bottleneck is `h/a` — the distance between the fixed point
and the line `s = 1 − B/a` beyond which a line can be dropped — and the multiplier one of
the saddle-node is what makes the cut curve of the next level nearly parallel to the
present one.  Numbers for the Gaussian pair (`r2_chain.py`, floating point): with `s_t = L + 0.05`
the left side of (C2) is `0.3005` against `0.45`, and from `b_0 = h + 0.02` the range condition holds
at all `1000` levels computed (largest value of `W_{j+1}(b_{j+1})`: `0.83`); from the wider start
`b_0 = h + 0.15` it **fails** (`1.06` at an early level) — the restart near `h` is needed, not a
convenience.  (C2) is sufficient, not necessary: at `s_t = L + 0.15` it fails (`0.48` against `0.35`)
while the range condition still holds from `b_0 = h + 0.02` (the bound `λ̄` on the ratio of
consecutive slopes is crude: the ratio itself tends to one).  Cube, `u = 1`, `s_t = L + 0.05`,
`b_0 = h + 0.003`: holds at all `600` levels computed.

## 7. The passage time

For `δ > 0` let `N_t(δ) = min{n : p_n(h + δ) > s_t}` (finite by (P3)).

**Lemma PT [P].**  *Under (H0), (H1), for every `s_t ∈ (L, 1 − h/a)`:*

    lim_{δ ↓ 0} √δ·N_t(δ)  =  c_* := π·h·√(2ϑ).

*Proof.*  Put `A = 1/(2ϑ)`, `F(x) = δ + A(x − L)²`, `G(x) = (Aδ)^{−1/2}·arctan((x − L)√(A/δ))`, so `G′ = 1/F`.  Fix `ε` and
take `η, δ₀` from (Σ6), with `η` so small that `[L − η, L + η] ⊂ (0, s_t)` and `Δ̄ := (1 + ε)(δ₀ + Aη²)/h ≤ η/2`.  The
orbit `x_n = p_n(h + δ)` is increasing with steps `Δ_n = D(h + δ, x_n)`.
*Outside the window.*  By (Σ7) at most `K(η) = s_t/c(η) + 2` of the `x_n ≤ s_t` lie outside `[L − η, L + η]`.
*Inside.*  For `x_n ∈ [L − η, L + η]`: `(1 − ε)F(x_n)/h ≤ Δ_n ≤ (1 + ε)F(x_n)/h ≤ Δ̄`, and for `x ∈ [x_n, x_{n+1}]`,
`|F(x) − F(x_n)| ≤ A·Δ_n·(2η + Δ̄) ≤ κ·F(x_n)` with `κ := 3A(1 + ε)η/h`.  Hence

    (1 − ε)/((1 + κ)h)  ≤  G(x_{n+1}) − G(x_n) = ∫_{x_n}^{x_{n+1}} dx/F  ≤  (1 + ε)/((1 − κ)h).

Let `n₀` be the first index with `x_n ≥ L − η` and `n₁` the first with `x_n > L + η`.  The total variation
of `G` is `π/√(Aδ)`, so `n₁ − n₀ ≤ πh(1 + κ)/((1 − ε)√(Aδ))`.  Conversely `x_{n₀} ≤ Σ(h + δ, L − η) ≤ L − η + Δ̄ ≤ L − η/2`
(monotonicity of `Σ` in `s`), so `G(x_{n₁}) − G(x_{n₀}) ≥ G(L + η) − G(L − η/2) ≥ (Aδ)^{−1/2}(π − 3√(δ/A)/η)` (using
`arctan y ≥ π/2 − 1/y`), and `n₁ − n₀ ≥ (π/√(Aδ) − 3/(Aη))·h(1 − κ)/(1 + ε)`.  Since `n₁ − n₀ ≤ N_t(δ) ≤ n₁ − n₀ + K(η)`,

    πh(1 − κ)/((1 + ε)√A)  ≤  liminf √δ·N_t  ≤  limsup √δ·N_t  ≤  πh(1 + κ)/((1 − ε)√A),

and `ε → 0`, `η → 0` (so `κ → 0`) give the limit `πh/√A`.  ∎

## 8. Proof of Theorem R

Write `c_*² = 2π²h²ϑ`.

**Lower bound.**  If `k < N_t(δ)` then `p_k(h + δ) ≤ s_t < ∞`, so `τ_k ≥ h + δ` by Proposition A.  Given
`ε > 0`, Lemma PT gives `N_t(δ) ≥ (1 − ε)c_*/√δ` for small `δ`; with `δ = (1 − ε)²c_*²/(k + 1)²` this is `N_t(δ) ≥ k + 1`.
So `τ_k − h ≥ (1 − ε)²c_*²/(k + 1)²` for large `k`: `liminf k²(τ_k − h) ≥ c_*²`.

**Upper bound.**  Choose `s_t ∈ (L, 1 − h/a)` satisfying (C1), (C2); `ε₁` from Lemma RC, with also
`h + ε₁ < (1 − s_t)a`; `b_0 = h + ε₁`; and `k₁` with `τ_{k₁} ≤ b_0` (the a-priori bound).  By Proposition C and
Lemma RC, for every `j` in case B,

    τ_{k₁+j+1} − h  ≤  E_j − h  ≤  δ_t(j) + (1 − s_t)/m_j,      δ_t(j) := B_t(j) − h.

(i) *`j²·δ_t(j) → c_*²`.*  `δ_t(j) → 0` by (P3).  For `δ < δ_t(j)`: `p_j(h + δ) ≤ s_t`, so `N_t(δ) > j`; for `δ > δ_t(j)`:
`N_t(δ) ≤ j`.  With Lemma PT, taking `δ = (1 ∓ ι)δ_t(j)` and then `ι → 0`: `j²δ_t(j) → c_*²`.
(ii) *`1/m_j = o(δ_t(j))`.*  Fix `ι ∈ (0, 1)` and `ω > 0`, and let `B′ = h + (1 − ι)δ_t(j)`.  By (i) and Lemma PT,
`N_t((1 − ι)δ_t(j)) − j → ∞` (it is `j·((1 − ι)^{−1/2} − 1 + o(1))`).  If `p_j(B′) > L + ω`, the orbit at `B′` would,
from step `j` on, move in `(L + ω, s_t]` with steps at least `c(ω)` (Σ7) and exceed `s_t` within
`(s_t − L)/c(ω) + 1` further steps.  So `p_j(B′) ≤ L + ω` for large `j`, and by convexity
`m_j ≥ (s_t − p_j(B′))/(ι·δ_t(j)) ≥ (s_t − L − ω)/(ι·δ_t(j))`.  As `ι` is arbitrary, `1/(m_jδ_t(j)) → 0`.
Hence `τ_{k₁+j+1} − h ≤ (c_*² + o(1))/j²`, and with `k = k₁ + j + 1` (`k₁` fixed): `limsup k²(τ_k − h) ≤ c_*²`.  ∎

**What the proof gives at finite `k`.**  The sandwich

    B_∞(k)  ≤  τ_k  ≤  B_t(k − k₁ − 1) + (1 − s_t)/m_{k−k₁−1}

between two points of the same family of orbit curves — the point where the `k`-th
curve blows up, and the point where a curve `k₁ + 1` levels earlier reaches the slope
`s_t`, plus a term of relative order `1/k`.  The left inequality holds for every `k`
(machine-checked chain); the right one for `k > k₁ + N_t(ε₁)`, with a restart level `k₁` that
the proof does not quantify.  Numerically (not certified) the chain works with a
restart two levels back from `k = 4` on (`ub_subsolution.py`: `κ₀ = 2`) and the true sequence
behaves like `c_*²/(k + c)²` with `c ≈ 0.15–0.25`, between `c = ½` (lower bound) and `c ≈ 0`
(the exact dynamics of convex majorants).

## 8a. The profile at positive accuracy: a closed form for the similarity solution

**Proposition S (the scaled defect) [P-sketch — see the status below; N].**  *Under (H0), (H1), for
every `ζ ≥ 0`,*

    lim_{k → ∞} k²·[ T_k(ζh/k) − θ_hint(ζh/k) ]  =  h²·ϑ·f(ζ),
    f(ζ)  =  sup{ 2z² + 2ζ·z·cot z  :  z ∈ (0, π)  or  z = iy, y > 0 }  −  ζ²/2

*(for imaginary `z`: `−2y² + 2ζ·y·coth y`).*  `f(0) = 2π²` is Theorem R.  `f` is decreasing and convex,
`f(3) = 3/2`, `f′(2) = −2`; the supremum is attained at a real `z` for `ζ < 3` (intercepts above `h`) and
at an imaginary one for `ζ > 3` (intercepts below `h`, where the orbit approaches the stable
fixed point); and `f` solves

    ζ·f′²/2 + ζ·f′ + (ζ − 2)·f = 0,

the similarity equation of the continuum heuristic `∂_kD = −x·[D/h + (∂_xD)²/(2q)]`, `q = hϑ`, of
the brief (§2.4), through its folded saddle `(3, 3/2)`: the heuristic is a theorem about
Legendre transforms of the orbit curves.

*Derivation.*  Both bounds are envelopes of lines over the same curves: `T_k(x) ≥ sup_B [B − p_k(B)x]`
(Proposition A) and `T_{k₁+j}(x) ≤ max_{B ≤ b_j} [B − W_j(B)x]` (Proposition C; for `x ≍ 1/j` the maximum
is at slopes within `O(1/j)` of `L`, where `W_j = p_j`).  With `A = 1/(2ϑ)`, `B = h + δ`, the comparison
of the proof of Lemma PT gives the *position* of the orbit after `k` steps, not only the
number of steps: `p_k(h + δ) − L = −√(δ/A)·cot(√(Aδ)·k/h)·(1 + o(1))` for `δ > 0` (and the same with
`coth` for `δ < 0`), uniformly for `z = √(Aδ)·k/h` in compact subsets of `(0, π)`.  With
`δ = z²h²/(Ak²)`, `x = ζh/k` and `θ_hint(x) = h − Lx + ϑx²/2 + o(x²)`:

    B − p_k(B)·x − θ_hint(x)  =  (h²ϑ/k²)·[ 2z² + 2ζ·z·cot z − ζ²/2 ] + o(k⁻²).

The equation for `f`: at the maximiser, `f′ = 2z·cot z − ζ`, and the stationarity condition
`2z + ζ(cot z − z/sin²z) = 0` eliminates `z`.

*Status.*  The two envelope bounds are Propositions A and C.  The uniform position
estimate is the argument of Lemma PT read for positions; it is **not written out**, and
the exchange of the limit with the supremum over `z` (the maximiser stays in a compact
subset of `(0, π)` for `0 < ζ < 3`) is not written out either.  Numerically
(`r4_profile.py`, `out_r4_profile.txt`): the lower envelope of the lines of Proposition A,
computed from the exact orbit curves, increases to `f` for both pairs — at `ζ = 1`:
`5.611, 5.793, 5.891, 5.941` at `k = 20, 40, 80, 160` (Gaussian; the cube at `u = 1` agrees to
three digits) against `f(1) = 5.992` — and the recursion itself on a grid has
`11.742, 9.068, 5.980, 2.933, 1.501, 0.396` at `ζ = ¼, ½, 1, 2, 3, 5` and `k = 160` against
`f = 11.765, 9.089, 5.992, 2.935, 1.500, 0.388`; the residual of the differential equation
is below `2·10⁻⁴` on the closed form (finite differences).

## 9. Other shapes of the maximum of `J`: where the law changes

The proof separates what is structural from what is (H1).

* **Structural, for every `θ` with (H0):** Lemma L, Proposition A (`τ_k ≥ B_∞(k)`), Lemma M,
  Proposition U and its corollary, (Σ1)–(Σ5), (P1)–(P3), Lemma T, Proposition C.
* **(H1) is used** in (Σ6), hence in Lemma PT (the value of the passage time), and in
  Lemma RC (multiplier one and a unique maximiser at the fixed point).

**Proposition K (a kink at the fixed point gives the rate `1/k`, and the a-priori bound is
then sharp) [P].**  *Let `θ` satisfy (H0) and have a kink at `h`: `∂θ(h) = [−r₂, −r₁]` with `r₁ < r₂`.  Then `J = h`
on `[L₁, L₂]`, `L_i = r_i/(1 + r_i)`, and*

    τ_k − h  ≥  (L₂ − L₁)·h/(k + 2)      for all k ≥ 1;

*together with `τ_k − h ≤ c₁/(k + c₂)`: `τ_k − h = Θ(1/k)`.*
*Proof.*  Let `B = h + δ`, `w₀ = δ/h` and `s_max = L₂ − (1 − L₂)w₀`.  For `s ∈ [L₁, s_max]` the point `(s + w₀)/(1 + w₀)` lies in
`[L₁, L₂]`, so `Ψ_s(w₀) = (1 + w₀)h = B`, while `Ψ_s(w) ≤ (1 + w)h < B` for `w < w₀`: **`D(h + δ, s) = δ/h` exactly on
`[L₁, s_max]`.**  The orbit `x_n = p_n(B)` is increasing.  Let `n₀` be the first index with `x_n ≥ L₁`; by
monotonicity of `Σ` in `s`, `x_{n₀} ≤ Σ(B, L₁) = L₁ + w₀` (or `x_0 = 0 = L₁`).  From there the steps are exactly
`w₀` as long as the points are `≤ s_max`, so `x_n ≤ s_max` for all
`n ≤ n* := ⌊(L₂ − L₁)/w₀ − (1 − L₂)⌋ − 1`.  All points `s < s_max` are regular: `(1 − s)a > (1 − s_max)a = (1 − L₂)a·(1 + w₀) ≥ h(1 + w₀) = B`,
because `h = J(L₂) ≤ g_{L₂}(0+) = (1 − L₂)a`.  Hence `p_n(B) < ∞` for `n ≤ n*`, and Proposition A gives
`τ_k ≥ h + δ` whenever `k ≤ (L₂ − L₁)h/δ − (1 − L₂) − 1`; take `δ = (L₂ − L₁)h/(k + 2)`.  ∎
Example (`rlib.Kinked`): `θ(e) = max(1 − 3e, ½ − e, 0)`, `a = 1`, `h = ¼`, `J(t) = min(1 − t, ¼, t/2)`, flat on `[½, ¾]`:
`τ_k − ¼ ≥ 1/(16(k + 2))` (`r1_checks.py` follows the orbit).

So over the class of all pairs with (H0) the rate `O(1/k)` of the remark after Theorem
11.53 cannot be improved, and the `1/k²` of the cube is a consequence of the smoothness
and strict convexity of `θ_na` at its fixed point.

**Heuristic classification [C].**  If `h − J(t) ≍ |t − L|^p` near `L` with `p > 1`, the passage time is
`≍ ∫ dv/(δ + |v|^p) ≍ δ^{−(p−1)/p}` and one expects `τ_k − h ≍ k^{−p/(p−1)}`: `k^{−2}` for `p = 2`, tending to `k^{−1}` as
`p → ∞` (a flat maximum, the kink of Proposition K).  For `p = 1` — a corner of `J` at its
maximum, which happens when `θ` is affine on a neighbourhood of `h`, so that `g_L` has an
interval of minimisers — the passage time is `≍ ln(1/δ)` and one expects geometric
convergence.  Only the lower bounds of these statements follow from Proposition A as it
stands; the upper bounds would need a version of Lemma RC without the multiplier one.
Not pursued.

## 10. The Gaussian pair, exactly

`Σ(B, s) = B(1 − s)/(1 − s − B)` **[V]**.  In the variable `y = 1 − s` the map is
`y ↦ ((1 − B)y − B)/(y − B)`, a Möbius map with matrix `[[1 − B, −B], [1, −B]]`, trace `1 − 2B` and determinant `B²`.
Its eigenvalues are `B·e^{±iψ}` with `cos ψ = (1 − 2B)/(2B)`, `sin ψ = √(4B − 1)/(2B)`: for `B > ¼` the map is elliptic,
and in the angular coordinate of the projective line (period `π`) it is the rotation by
`ψ(B) = arctan(√(4B − 1)/(1 − 2B)) ≈ 4√(B − ¼)` per level.  In that coordinate the orbit of the flat
line is at `φ₀(B) = arccot((1 − 3B)/((1 − B)√(4B − 1)))` after one level and blows up at `π`, so the lower
bound `B_∞(k)` of Proposition A is the root of

    (k − 1)·ψ(B) + φ₀(B) = π

**[N: the closed form agrees with the orbit itself to rounding for every `k` tested —
harness XVI.6; the conjugation is routine and is not written out]**: `(3 − √5)/2 = 0.381966` at
`k = 2`, and `¼ + (π²/16)/(k + ½)²·(1 + O(k⁻²))`.  Machine-checked instances: `T_2(0+) ≥ 3/8`, `T_3(0+) ≥ 3/10`
(`gauss_level_two_ge`, `gauss_level_three_ge`).

## 11. Numerical checks (scripts in `experiments/workstreams/R/` and
`experiments/coordinator_checks/level_rate/`)

| script | what it checks | result |
|---|---|---|
| `r1_checks.py` | joint convexity and monotonicity of `Σ` (12 000 random midpoints); convexity of the orbit curves; (Σ6); Lemma PT; Proposition U by brute force — the bracket of `R` minimised over `φ` at `β → 0` against the envelope of the image lines, for random convex piecewise-linear `W`; a negative control with a concave `W`; Proposition K | all pass (`out_r1_checks.txt`): `√δ·N_t(δ)/c_* = 0.764, 0.906, 0.968, 0.990, 0.997` at `δ/h = 10⁻², …, 10⁻⁶` (Gaussian; the cube alike); Proposition U holds **with equality** up to the discretisation (`2·10⁻⁶·a`, 240 cases); with a concave `W` the line-by-line value is exceeded by up to `0.07·a` |
| `r2_chain.py pair s_t−L b_0−h [levels]` | the restarted chain of §6: case A/B, `B_t(j)`, `m_j`, `E_j`, `b_j`, the range condition, the ratio of consecutive slopes against its bound; `j²(b_j − h)/c_*²` | `out_r2_chain_gauss.txt` (`1.031` at `j = 1000`), `out_r2_chain_cube1.txt` (`1.049` at `j = 600`), `out_r2_chain_gauss_st015.txt`, `out_r2_chain_gauss_wide.txt` (range condition fails) |
| `r3_gauss_exact_lb.py` | **exact** lower bounds for the Gaussian pair at finite `k` (Proposition A with the orbit in rational arithmetic: no rounding; the chain behind it is machine-checked) | `τ_k ≥ 0.381966011, 0.307978528, 0.255679562, 0.250376448, 0.250023947` at `k = 2, 3, 10, 40, 160`; `(k + ½)²(τ_k − ¼) ≥ 1.0151, 1.0010, 1.00005` times `π²/16` at `k = 10, 40, 160` (`out_r3_gauss_exact_lb.txt`) |
| `r4_profile.py` | the closed form `f` of §8a, the residual of its differential equation, and the lower envelope of the lines of Proposition A at `k = 20 … 160` for two pairs | `out_r4_profile.txt` (increasing to `f`; the two pairs agree to three digits) |
| `level_rate/lines_lb*.py` | `B_∞(k)` (lower bound) for the Gaussian pair, the cube, four biased cubes | ratio to `c_*²`: `0.9902, 0.9938, 0.9969` at `k = 100, 160, 320` (Gaussian) |
| `level_rate/dual_ub_*.py` | the exact dynamics of convex majorants on grids | ratio `1.00016, 1.00006, 1.00001` at `k = 100, 160, 320` (Gaussian); `0.99873, 0.99903` at `120, 160` (cube `u = 1`) |
| `level_rate/iterate_exact.py` | the recursion itself on a grid (not one-sided) | ratio `0.9960, 0.9982` at `100, 160` (Gaussian); `0.99467, 0.99585` at `100, 120` (cube) |
| `level_rate/ub_subsolution.py` | the cut curves without restart (`W_k` = cut `p_{k−2}`) | all conditions hold from `k = 4` on, three pairs |

## 12. What is not done

1. **Review.**  When first committed, nothing in this file had been read by anyone but its
   author.  Independent internal reviews are commissioned; their outcome is recorded in
   the research log and in the theory report (Theorem 11.53a).
2. **No certified upper constants at finite `k`.**  The `o(1)` terms are not quantified; the
   restart level `k₁` is not computed.  From below the bound is exact for the Gaussian pair
   (`r3_gauss_exact_lb.py`: rational arithmetic on top of the machine-checked chain); for the
   cube it would need interval arithmetic for the slope map.  A certified *upper* table needs
   a certified restart value and has not been done.
3. **Not machine-checked:** Proposition U (it needs Sion's minimax theorem), Lemma T,
   Proposition C, Lemma RC, Lemma PT, (Σ6).  Machine-checked: Lemma L and the iteration of
   Proposition A, Lemma M, the Gaussian slope map and three numerical instances.
4. **Positive accuracy.**  The theorem is about `τ_k = T_k(0+)`.  The profile at `x ≍ 1/k` has the
   closed form of §8a; its proof is a sketch (a uniform position estimate is not written
   out).
5. **Finite `n`.**  With a schedule of `k ≍ n^{1/3}` levels and a loss of `O(ln n)` per level one
   expects `n·h + O(n^{1/3}(ln n)^{2/3})` for the adaptive cost; this needs the uniform
   sub-exponential factors (workstream Q2) and is **not established**.
6. **Other maxima** (§9): only the kink is proved.
