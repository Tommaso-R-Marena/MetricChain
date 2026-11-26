# Internal review B of `docs/workstreams/R_REPORT.md` — slope map, lower bound, passage time (§§1–4, 7, 8 lower, 9, 10)

*Referee B (AI, internal review; not external peer review).  Written 2026-11-26.  Scripts and
their outputs: `experiments/workstreams/R/review_B/`.  Verdict scale: **correct as stated** /
**correct after a repair** / **gap** / **wrong**.  The version reviewed is commit `020e990`
(530 lines); the later commits `fc3f5d9`, `0b1b0f5` do not touch the sections under review
(see "§8a").*

## Result in one paragraph

**I found no error of substance in §§1–4, 7, the lower-bound half of §8, §9 and §10.**  Every
numbered statement was re-derived by hand and tested numerically with code of my own that
computes the slope map from the definition of `θ` (not through `J`, not from `rlib.py`), on
pairs the author did not use.  Two sentences are wrong or incomplete as written and should
be edited — the attainment claim in (Σ3) fails on the boundary `B = (1 − s)a` when `θ′(0+)` is
finite, and the sentence of (Σ5) about the fixed points for `B < h` has two families of
counterexamples — but both are expository and nothing in the proof of Theorem R uses them.
The constants of the cube are right to all printed digits.  An iteration of the recursion
itself (own implementation, four pairs with (H1), up to 61 levels) reproduces `τ_k ≥ B_∞(k)` and
the limit `2π²h²ϑ` to about `0.1 %`; for a kinked pair it gives the rate `1/k`, for `θ` affine near `h`
a geometric rate.  The summary table, the list of suggested edits and the list of what was
not checked are at the end.

## Status log

* §1 (constants, `J`, (H1)) — done: `b1_constants.py`.
* §2 (Σ1)–(Σ7) — done: `blib.py`, `b2_sigma.py`.
* §§3–4 (P1)–(P3), Lemma L / Proposition A against the Lean file — done: `b4_orbits_gauss.py`, `b8`, `b9`.
* §7 Lemma PT — done: `b3_passage.py`, `b11_H1_not_C2.py`, `b12_onesided.py`.
* §8 lower bound; §9; §10 — done: `b4`, `b5_kink_heuristic.py`.
* Global test — done: `b6_recursion.py`, `b7_compare.py`.
* Author's code read and compared — done: `b10_author_lib.py`; `r1_checks.py` re-run.
* §8a (new in the report) — quick consistency check only: `b13_profile_8a.py`.

## §1 — the dual function `J`, hypotheses

### 1.1 Properties of `J` (concavity, `max J = h`, set of maximisers)

**Verdict: correct as stated.**  Read line by line.

* `J` is an infimum of functions affine in `t`, hence concave (and upper semicontinuous) on `[0, 1]`.
* `J ≤ g_t(h) = (1 − t)h + th = h`.  `J(t) = h` iff `h` minimises the convex `g_t`; for `t < 1` this is
  `0 ∈ (1 − t)∂θ(h) + t`, i.e. `−t/(1 − t) ∈ ∂θ(h)`; `t = 1` is excluded (`J(1) = inf e = 0 < h`).  Since `h > 0` is
  an interior point of the domain, `∂θ(h) = [θ′(h−), θ′(h+)]` is a nonempty compact interval of
  nonpositive numbers, so the set of maximisers `{r/(1 + r) : −r ∈ ∂θ(h)}` is a nonempty compact
  subinterval of `[0, 1)`, a single point iff `θ` is differentiable at `h`.  ✓
* Remark (not an error): `J(0) = inf θ = θ(∞)`, which is positive when `θ(∞) > 0`; (H0) allows this.
  The docstring of `rlib.py` ("`J(0) = J(1) = 0`") is only true for pairs with `θ(∞) = 0`.  This
  matters for one sentence of (Σ5), see there.

### 1.2 Shear / identification with `θ_hint`, `θ_hint″(0) = −1/J″(L)`

**Verdict: correct as stated** (with the reading that for an abstract `θ` the function `θ_hint` is
*defined* by the shear, `θ_hint(x) = y ⇔ θ(x + y) = y`, and for the cube this is the `θ_hint` of the theory
report by (11.18.1)).

* A line `y = c − t·x` lies below the sheared curve `{(e − θ(e), θ(e))}` iff `(1 − t)θ(e) + te ≥ c` for all `e`;
  the largest such `c` is `J(t)`.  ✓
* (11.18.1) `θ_na(e + θ_hint(e)) = θ_hint(e)` says exactly that `(e, θ_hint(e))` is the image of the point
  `(e + θ_hint(e), θ_na(e + θ_hint(e)))` of the graph of `θ_na` under the shear.  ✓
* The image of the (convex) epigraph of `θ` under the linear shear is `{(x, y) : y ≥ θ(x + y)}`, and
  since `y − θ(x + y)` is strictly increasing in `y` this is the epigraph of `θ_hint` on `(−a, ∞)`: `θ_hint`
  is convex, with slopes `θ′/(1 − θ′) ∈ (−1, 0]`.  Its conjugate is `inf_x [θ_hint(x) + tx] = J(t)`, so
  `θ_hint(x) = sup_{0 ≤ t ≤ 1} [J(t) − tx]` (slopes outside `[0, 1)` do not occur).  ✓
* `θ_hint(0) = h` (`θ(y) = y`); `θ_hint′(0) = θ′(h)/(1 − θ′(h)) = −r/(1 + r) = −L`; second derivatives of
  conjugate functions are reciprocal, `θ_hint″(0) = −1/J″(L)`.  ✓  Direct check without duality:
  from `y = θ(x + y)`, `y″ = θ″·(1 + y′)²/(1 − θ′) = θ″(h)/(1 + r)³` at `x = 0`.  ✓
* Under (H1) as stated (a second-order expansion of `J` at the single point `L`, not `J ∈ C²`),
  "`θ_hint″(0)`" has to be read as the coefficient of the second-order expansion of `θ_hint` at `0`
  (it exists, by the same duality); wording only.

### 1.3 Formula `ϑ = θ″(h)/(1 + r)³` for `C²` functions

**Verdict: correct as stated.**  `J′(t) = e* − θ(e*)` (envelope), `J″ = (1 − θ′(e*))·de*/dt`, and from
`θ′(e*(t)) = −t/(1 − t)`: `θ″(e*)·de*/dt = −1/(1 − t)²`.  At `t = L`: `1 − L = 1/(1 + r)`, `1 − θ′(h) = 1 + r`, so
`J″(L) = −(1 + r)³/θ″(h)` and `ϑ = θ″(h)/(1 + r)³`.  The implicit function theorem gives `e*(t) ∈ C¹` near `L`;
`g_t` is convex, so the critical point is the global minimiser; `r > 0` is automatic (a nonincreasing
function with `θ′(h) = 0`, `θ″(h) > 0` would increase to the right of `h`), so `L ∈ (0, 1)`.
Gaussian pair by hand: `J(t) = t − t²` (minimiser `√e = 1 − t`), `h = ¼`, `L = ½`, `ϑ = ½`, `a = 1`, and
`θ″(h)/(1 + r)³ = 4/8 = ½`; `2π²h²ϑ = π²/16`.  ✓
Numerically (script `b2_sigma.py`, five further pairs): `−1/J″(L)` with `J` minimised numerically
agrees with `θ″(h)/(1 + r)³` — see (Σ5).

### 1.4 Consequence (i) of (H1): unique minimiser of `g_L`

**Verdict: correct as stated.**  `g_t(e′) = g_L(e′) + (t − L)(e′ − θ(e′)) = h + (t − L)(e′ − θ(e′))` if `e′` minimises
`g_L`; `e′ − θ(e′) ≠ 0` because `h` is the only fixed point; so `J(t) ≤ h − c|t − L|` on one side of `L`,
which contradicts `J(t) = h − O((t − L)²)`.  ✓  (Only the quadratic *lower* bound for `J` near `L` is used.)

### 1.5 Consequence (ii) of (H1): `L < 1 − h/a`

**Verdict: correct as stated.**  `h = J(L) ≤ g_L(0+) = (1 − L)a`.  If equality held, the convex function
`g_L`, whose minimum value `h` is attained at `h`, would have `g_L(0+) = h` and therefore `g_L ≡ h` on `(0, h]`,
against (i).  ✓  (Equivalent direct argument: equality gives `J(t) ≤ g_t(0+) = (1 − t)a = h − (t − L)a` for
`t > L`, a linear fall-off.)  Numbers: cube `u = 1`: `L = 0.4900 < 1 − h/a = 0.7374`; `u = 2`:
`0.4645 < 0.7032`; Gaussian: `½ < ¾`.

### 1.6 Constants for the cube (u = 1, u = 2), from the theory report's definitions

**Verdict: the numbers of the report are correct** (to all digits printed).

Script `review_B/b1_constants.py` (output `out_b1_constants.txt`), mpmath at 40 digits, from
`p_u = 1/(1 + e^u)`, `θ_na(e) = KL(ρ_e‖½)` with `KL(ρ_e‖p_u) = e`, `θ_hint(e) = KL((Λ₁ + e)/u‖½)`, `a = KL(p_u‖½)`
(theory report lines 4709–4715, 5250–5251); nothing imported from `rlib.py`.  `h` is found as the
root of `θ_na(h) = h` and compared with `KL(Λ₁/u‖½)`; `r = −θ_na′(h)` and `θ_na″(h)` by implicit
differentiation *and* by numerical differentiation; `ϑ` four ways (`θ_na″(h)/(1 + r)³`; numerical
`θ_hint″(0)`; `1/(u²ρ_h(1 − ρ_h))`, `ρ_h = Λ₁/u`; `−1/J″(L)` with `J` obtained by numerically minimising
`(1 − t)θ_na(e) + te` over `e`).  All routes agree to at least 9 digits.

| | `u = 1` | `u = 2` | report (`u = 1`) |
|---|---|---|---|
| `a` | 0.110944071672 | 0.327813325473 | 0.11094407 ✓ |
| `h` | 0.0291391385016 | 0.0972809077466 | 0.02913914 ✓ |
| `L` | 0.490034276419 | 0.464544471527 | 0.490034 ✓ |
| `ϑ` | 4.24497756677 | 1.23177862051 | 4.244977 ✓ |
| `2π²h²ϑ` | 0.0711473217006 `= 0.64128998·a` | 0.230100536814 `= 0.70192551·a` | 0.0711473 `= 0.64129·a` ✓ |
| `c_* = πh√(2ϑ)` | 0.266734552881 | 0.479687957753 | — |

The closed form `J(t) = Λ(tu) − tΛ(u)` of the report is right: by the identity
`KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁`, `J(t) = min_ρ [KL(ρ‖½) + tuρ] − tΛ₁ = Λ(tu) − tΛ₁` (the minimiser
`ρ = 1/(1 + e^{tu})` lies in `[p_u, ½]`); numerical difference to the minimised `J`: below `10⁻³⁹`.
The report gives no numbers for `u = 2`; the author's library reproduces the column above
(`ϑ = 1.23177864` there, from a second difference with step `10⁻⁴`: 8 digits).

The cube satisfies the hypotheses of Theorem R: with `t = −logit(ρ_e)/u ∈ [0, 1]`,
`θ_na′(e) = logit(ρ_e)/(logit(ρ_e) + u) = −t/(1 − t) ≤ 0`, and `t` decreases from `1` to `0` as `e` runs from `0` to
`ε*`, so `θ_na` is nonincreasing and convex (slope `−∞` at `0`, slope `0` at `ε*`, where it joins the
zero function in a `C¹` way); `a = KL(p_u‖½) < ∞`, `h < a`: (H0).  `J(t) = Λ(tu) − tΛ(u)` is smooth with
`J″(t) = −u²·e^{tu}/(1 + e^{tu})² < 0` and its maximiser is interior: (H1).  ✓

### 1.7 The a-priori bound (as quoted)

**Verdict: the quotation is accurate for a `HintPair`; for an abstract (H0) function one sentence
is missing** (this paragraph belongs to Referee A's item 4; I only compared the statement).
`RateFull.rate_top0 (hp : HintPair θna θh a h E) (hah : h < a) (T : ℕ → ℝ → ℝ)` with `StepLE θna (T k) (T (k+1))`,
`T (k+1) ≤ T k`, every `T k` nonincreasing, `T 0 ≤ a`, concludes `T n x ≤ h + c1 a h/((n + 1) + c2 a h)`; `T n` is
level `n + 1`, so this is `τ_k − h ≤ c₁/(k + c₂)`, with `c₁ = h(1 + κ)/κ`, `κ = h²a/((a − h)(a + h)(2a − h))`,
`c₂ = (a + h)(2a − h)/(ha) − 2` (for `(a, h) = (1, ¼)`: `c₁ = 6.8125`, `c₂ = 6.75`).  ✓  A `HintPair` needs a
hinted function `θh` with `θna(e + θh e) = θh e`, `θh > 0`, `e + θh e` nondecreasing on `(0, E)` and
`θh(e) ≥ h − L·e`.  For a general `θ` satisfying (H0) these hold for the sheared function of §1
(`L = 1`, `E = h`, say); the report should say so where it claims the bound "under (H0)"
(it is used for an abstract `θ` in §8 and in Proposition K).  I did not re-read the proof.

## §2 — the slope map

*Numerics for this section:* `review_B/b2_sigma.py` (output `out_b2_sigma.txt`), on five pairs none
of which is among the author's test cases except through a different route: `θ = (1 − e)₊²`
(finite slope at zero; closed form `Σ = 2(1 − s)(1 − √(1 − B/(1 − s)))`), `θ = (1 − √e)₊³` (infinite slope at
zero), `θ = e^{−2e}` (never zero), `θ = 0.1 + 0.9e^{−3e}` (`θ(∞) > 0`), and the cube at `u = 2` built from the
`KL` definitions.  `Σ` is computed from its definition (scan of 2401 log-spaced `e` + golden
section on the ratio; second route: bisection on the tangent intercept), never through `J`;
the two routes agree to `10⁻⁸` or better (`blib.py`; `10⁻¹¹` away from the boundary of the regular
region).

### (Σ1)

**Verdict: correct as stated.**  Each function `(B, s) ↦ [B − (1 − s)θ(e)]/e` is affine with coefficients
`1/e > 0` and `θ(e)/e ≥ 0`; a supremum of such functions is convex, lower semicontinuous and
nondecreasing in each variable, as an extended-real function on `[0, ∞) × ℝ`.  Numerically: 1500
random midpoints per pair, largest value of `Σ(mid) − mean` is `≤ 0` (to rounding), no violation
of monotonicity.

### (Σ2)

**Verdict: correct as stated.**  As `e ↓ 0` the numerator tends to `B − (1 − s)a`; if negative, the ratio
tends to `−∞` at `0`, is continuous, bounded on `[e₀, ∞)` and tends to `0` at `∞`: finite supremum.  If
positive: `+∞`.  The boundary `B = (1 − s)a` is (rightly) left open: there the ratio is
`(1 − s)(a − θ(e))/e`, a chord slope that increases as `e ↓ 0`, so `Σ = (1 − s)·|θ′(0+)|`, finite iff `θ` has a
finite slope at zero.  A finite convex function on the open convex set `{B > 0, B < (1 − s)a}` is
continuous.  ✓

### (Σ3)

**Verdict: correct after a repair (wording; harmless for the proof).**  The first sentence
(least admissible slope, flattest line) is the definition of the supremum.  ✓  The second
sentence, "*if `0 < Σ(B, s) < ∞` the supremum is attained*", is **false on the boundary `B = (1 − s)a`
when `θ` has a finite slope at zero and is not affine near zero**: for `θ = (1 − e)₊²`, `s = 0.3`, `B = 0.7`
the ratio is `(1 − s)(2 − e)` for `e ≤ 1`, with supremum `1.4 = Σ ∈ (0, ∞)` approached only as `e → 0` (same
for `θ = e^{−2e}`; numbers in `out_b2_sigma.txt`).  (For the author's kinked pair, which is affine
near zero, the supremum on the boundary happens to be attained.)  Since the report calls
boundary points with `Σ < ∞` "regular", the hypothesis should read

> if `0 < Σ(B, s) < ∞` **and `B < (1 − s)a`**, the supremum is attained and `𝓜(B, s)` is compact and nonempty.

Proof of the repaired statement: the ratio is continuous, tends to `−∞` at `0` and to `0 < Σ` at `∞`.
Every later use of `𝓜` in my part is at such interior points: `(h, L)` (by consequence (ii)); in
Lemma RC (Referee A's part) `(B₁, σ₁)` with `B₁ ≤ b_0 < (1 − s_t)a ≤ (1 − σ₁)a`.  So nothing downstream is
affected.

### (Σ4)

**Verdict: correct as stated.**  Evaluate the supremum defining `Σ(B, s)` at `e₁`:
`[B − (1 − s)θ(e₁)]/e₁ = Σ(B₁, s₁) + (B − B₁)/e₁ + (s − s₁)θ(e₁)/e₁`.  Numerically: 300 random pairs of points per
pair of functions, no violation.

### (Σ5)

**Verdict: the formula and the consequences used in the proof are correct; one sentence of
the first bullet is wrong as stated (not used anywhere).**

* `Ψ_s(w) = (1 + w)·J((s + w)/(1 + w))`: with `t = (s + w)/(1 + w)`, `1 − t = (1 − s)/(1 + w)`, so
  `(1 + w)[(1 − t)θ(e) + te] = (1 − s)θ(e) + (s + w)e`; `t ∈ [0, 1]` needs `w ≥ −s` and `s ≤ 1`.  ✓  `Ψ_s` is an infimum
  of nondecreasing affine functions of `w`: concave, nondecreasing, and continuous on `[−s, ∞)`
  (finite concave + upper semicontinuous).  ✓
* `D = min{w ≥ −s : Ψ_s(w) ≥ B}`: by (Σ3), `σ′ ≥ Σ(B, s)` iff `inf_e [(1 − s)θ(e) + σ′e] ≥ B` iff `Ψ_s(σ′ − s) ≥ B`.  ✓
  (To be added: `D = ∞` when the set is empty, i.e. `B > sup Ψ_s = (1 − s)a`, or `B = (1 − s)a` with
  an infinite slope at zero.)  Numerically: `|D − min w| ≤ 10⁻¹²` at 60 random points per pair,
  with `Ψ` computed directly and through a numerically minimised `J`.
* `D(B, s) ≤ 0 ⇔ J(s) ≥ B` (for `0 ≤ s < 1`): `D ≤ 0` iff `Ψ_s(0) = J(s) ≥ B`.  ✓  Hence for `B > h` no fixed point,
  and for `B = h` under (H1) exactly one, `L` (`D(h, s) ≥ 0` by (2.1), `= 0` iff `J(s) = h`).  ✓  These are the
  only cases the proof uses.
* **"The fixed points of `s ↦ Σ(B, s)` are the solutions of `J(s) = B`: two for `B < h`" — wrong as
  stated**, in two situations:
  (a) *`θ(∞) > 0` and `B < θ(∞)`*: `Σ(B, 0) = 0`, so `s = 0` is a fixed point although `J(0) = θ(∞) ≠ B`
  (checked: `θ = 0.1 + 0.9e^{−3e}`, `B = 0.05`: `Σ(B, 0) = 0`, `J(0) = 0.1`), and `J(s) = B` has only one root;
  (b) *finite slope at zero*: the upper root of `J(s) = B` can lie on the linear piece
  `J(t) = (1 − t)a`, i.e. on the boundary `B = (1 − s)a`, and there `Σ(B, s) = (1 − s)|θ′(0+)|` need not equal
  `s`.  Example `θ = (1 − e)₊²` (`J(t) = t − t²/(4(1 − t))` for `t ≤ ⅔`, `= 1 − t` for `t ≥ ⅔`, `h = 0.381966`): for
  `B = 0.8h = 0.30557` the upper root is `s₂ = 1 − B = 0.69443`, where `Σ(B, s₂) = 2(1 − s₂) = 0.611 < s₂`, and
  `Σ(B, s) = ∞` for `s > s₂`: the map has **one** fixed point, not two (in `out_b2_sigma.txt` the
  floating-point evaluation lands on the infinite side).
  Correct statement: *for `0 ≤ s < 1` with `B < (1 − s)a`: `Σ(B, s) = s` iff `J(s) = B` or (`s = 0` and
  `B ≤ θ(∞)`)*.  The sentence is expository; the bold conclusion ("the hinted exponent is the
  saddle-node value") stands.
* (2.1): from `Ψ_s(D) ≥ B` and `Ψ_s(w) ≤ (1 + w)h`: `D ≥ (B − h)/h` (and `D = ∞` for `s ≥ 1`).  ✓  Numerically
  the minimum of `D − (B − h)/h` over 400 random points per pair is positive.
* `Σ(h, L) = L`, `𝓜(h, L) = {h}`, multiplier one: `e ∈ 𝓜(h, L)` iff `g_L(e) = h`; (i).  ✓  Numerically for all
  five pairs: `Σ(h, L) − L = 0` to rounding, maximiser `= h`, `∂Σ/∂s = 1.000000`, `h·∂Σ/∂B = 1.000000`, and
  `−1/J″(L)` (second difference of the numerically minimised `J`) `= θ″(h)/(1 + r)³` to 5 digits.

### (Σ6)

**Verdict: correct as stated; the proof is complete.**  Checked line by line:

1. `(h, L)` is an interior point of the open regular region by (ii), `Σ` is continuous there, and
   `D(h, L) = 0`; continuity *at this one point as a function of two variables* is exactly the
   uniform statement needed: for every `ω > 0` there are `η, δ₀` with `0 ≤ w ≤ ω` for all `|v| ≤ η`,
   `0 < δ ≤ δ₀`.  ✓ (So "`w → 0` uniformly" is justified.)
2. `w ≥ δ/h > 0` by (2.1); since `w > 0 > −s` is interior to the domain of the continuous
   nondecreasing `Ψ_s` and `w` is the least point with `Ψ_s ≥ h + δ`: `Ψ_s(w) = h + δ`.  ✓
3. `t − L = (L + v + w)/(1 + w) − L = (v + (1 − L)w)/(1 + w) = q`.  ✓  With `r(q) := 2ϑ(h − J(L + q))/q² − 1` (`→ 0` by (H1),
   and `1 + r ≥ 0` because `J ≤ h`): `(1 + w)[h − q²(1 + r)/(2ϑ)] = h + δ ⇔ hw = δ + (v + (1 − L)w)²(1 + r)/((1 + w)2ϑ)`.  ✓
   (`q = 0` is consistent: then `w = δ/h`.)
4. `|(v + cw)² − v²| = |2vcw + c²w²| ≤ 2|v|w + w²` for `c = 1 − L ∈ (0, 1)`.  ✓  Upper inequality: drop `1/(1 + w) ≤ 1`.  ✓
   Lower inequality: `(1 + r)(v + cw)² ≥ (1 − |r|)(v² − 2|v|w)` holds also when the right side is negative,
   because the left side is `≥ 0`.  ✓
5. Solving: `w·[h − (1 + ε′)(2η + ω)/(2ϑ)] ≤ δ + (1 + ε′)v²/(2ϑ) ≤ (1 + ε′)[δ + v²/(2ϑ)]` ✓ (bracket positive for small
   `η, ω`); `w·[h + (1 − ε′)η/ϑ] ≥ δ + (1 − ε′)v²/((1 + ω)2ϑ) ≥ ((1 − ε′)/(1 + ω))[δ + v²/(2ϑ)]` ✓, and the report's
   denominator `h + η/ϑ` is larger, so its inequality follows.
6. `|q| ≤ |v| + w ≤ η + ω`, so `ε′ = sup{|r(q)| : |q| ≤ η + ω} → 0`: all constants depend on `(δ, v)` only
   through `η, δ₀`.  ✓  (H1) is used exactly here (and in step 1 through (ii)).

Numerically (five new pairs, `out_b2_sigma.txt`): the ratio `D(h + δ, L + v)·h/(δ + v²/(2ϑ))` is `1.0000`
at `v = 0`, `δ ≤ 10⁻⁶`, and `sup_{|v| ≤ η, δ ≤ δ₀} |ratio − 1|` decreases *linearly* in `η`:
e.g. `0.117, 0.036, 0.0106, 0.0035` at `η = 0.03, 0.01, 0.003, 0.001` for `θ = (1 − √e)₊³`, and
`0.383, 0.098, 0.027, 0.0089` for `θ = (1 − e)₊²`.  (The deviation is of first order in `v` — a cubic term
of `J` and the term `2v(1 − L)w` — so (Σ6) cannot be improved to `1 + O(v²)`, and it need not be.)

### (Σ7)

**Verdict: correct as stated.**  For `s ∈ [0, s_t]`: `h < (1 − s_t)a ≤ (1 − s)a`, so `(h, s)` is in the open
regular region and `D(h, ·)` is continuous on `[0, s_t]`; `D(h, s) ≥ 0` by (2.1) and `D(h, s) ≤ 0 ⇔ J(s) ≥ h ⇔ s = L`
(no boundary subtlety: this is the first bullet of (Σ5) in the form that is correct).  A
positive continuous function on the compact set `[0, s_t] ∖ (L − η, L + η)` has a positive minimum;
monotonicity in `B` extends it to `B ≥ h`.  ✓  Numerically `c(η) ≈ η²/(2ϑh)` (attained at `L − η`), as
(Σ6) predicts: e.g. `c(0.01) = 3.38·10⁻⁴` against `3.41·10⁻⁴` for `θ = (1 − √e)₊³`.

### The Gaussian pair (quotation of the Lean statements)

**Verdict: quoted correctly.**  `gauss_slope_map`: for `0 ≤ B`, `σ + B < 1`,
`∀ e > 0, B − (1 − σ)·gaussNa e ≤ B(1 − σ)/(1 − σ − B)·e`; `gauss_slope_map_least`: every `σ′` with
`∀ e > 0, B − (1 − σ)·gaussNa e ≤ σ′e` is `≥ B(1 − σ)/(1 − σ − B)`.  Together: `Σ(B, s) = B(1 − s)/(1 − s − B)` on
`{s + B < 1}`, as the report says (`gaussNa x = (1 − √(min x 1))²`, `HintRecursion.lean:443`).  My own
`Σ` (from the definition) agrees with the Möbius formula to `3·10⁻¹⁶` at five test points.

## §3 — orbit curves

*Numerics for §3:* `review_B/b4_orbits_gauss.py` (output `out_b4_orbits_gauss.txt`), four new pairs.

### (P1)

**Verdict: correct as stated.**  The induction is right for extended values: if `p_j(B₁)` or `p_j(B₂)` is
infinite the convexity inequality is trivial; otherwise `Σ(B, p_j(B)) ≤ Σ(B, λp_j(B₁) + (1 − λ)p_j(B₂))`
(monotone in `s`, for all real `s`, with value `∞` allowed) `≤ λΣ(B₁, p_j(B₁)) + (1 − λ)Σ(B₂, p_j(B₂))` (joint
convexity).  Monotone in `B`: both arguments of `Σ` increase.  Lower semicontinuity (not proved in
the report, but true): `Σ(B, ·)` is lsc and nondecreasing, hence left-continuous, and `Σ` is lsc
jointly; so `liminf_{B′→B} Σ(B′, p_j(B′)) ≥ Σ(B, s⁻)` for every `s⁻ < p_j(B)`, and `s⁻ ↑ p_j(B)`.  `p_j(0) = 0`:
`Σ(0, 0) = sup_e −θ(e)/e = 0`.  `p_{j+1} ≥ p_j` by induction from `p_1 ≥ 0 = p_0`.  ✓
Numerically (601 values of `B` in `[0, 1.5h]`, `j ≤ 34`): no negative second difference, no decrease
in `B` or in `j`, `p_j(0) = 0`, and the set `{p_j < ∞}` is an initial segment.

### (P2)

**Verdict: correct as stated.**  `p_j(h) ≤ L ⇒ p_{j+1}(h) = Σ(h, p_j(h)) ≤ Σ(h, L) = L`.  (Under (H0) alone, with `L`
any maximiser of `J`: `Σ(h, L) ≤ L` because `D(h, L) ≤ 0 ⇔ J(L) ≥ h`; so (P2) is indeed structural.)
Numerically `p_j(h) ≤ L` for `j ≤ 10⁵`, and `j·(L − p_j(h)) → 2ϑh` (e.g. `0.29312` against `0.29312` for
`θ = (1 − √e)₊³`), which is the parabolic approach `dv/dn = v²/(2ϑh)` predicted by (Σ6) at `δ = 0`.

### (P3)

**Verdict: correct as stated.**  Each step adds `D ≥ (B − h)/h` (2.1) as long as the orbit is finite;
and `Σ(B, s) = ∞` once `s > 1 − B/a`.  ✓  Numerically the minimum of `p_j(B) − j(B − h)/h` over
`j ≤ 60`, 40 values of `B ∈ (h, 1.3h]` is positive for all four pairs.

## §4 — the lower bound

### Lemma L (quotation against `LineDynamics.lean`)

**Verdict: quoted with exactly the right hypotheses.**

    theorem line_le_Rstep {θna T : ℝ → ℝ} {B σ σ' C : ℝ}
        (hθ : ∀ x, 0 < x → 0 ≤ θna x) (hσ : 0 ≤ σ) (hσσ' : σ ≤ σ')
        (hT : ∀ x, 0 < x → B - σ * x ≤ T x) (hTC : ∀ x, 0 < x → T x ≤ C)
        (hmap : ∀ e, 0 < e → B - (1 - σ) * θna e ≤ σ' * e)
        {g : ℝ} (hg : 0 < g) : B - σ' * g ≤ Rstep θna T g

— `θ ≥ 0`; `0 ≤ σ ≤ σ′`; the line below `T` on `(0, ∞)`; `T` bounded above; the slope-map inequality for all
`e > 0`: this is the report's Lemma L word for word.  `line_le_min_Rstep` has the same hypotheses
and the conclusion for `min(T g, Rstep θna T g)`.  `Rstep` (`BoundedAccuracy.lean:50–55`) is the infimum
of the set of all upper bounds `B₀` of the bracket `min(γ, φθ((g − β)/φ)) + (1 − φ)T(γ/(1 − φ))` over `γ ≥ β`, for
some `0 < β < g`, `0 < φ < 1` — the `inf sup` of (11.18.2) when `T` is bounded above (theory report line
4792; same ranges of `φ, β, γ`).  `exactRec θna k` is `T_{k+1}` (`exactRec θna 0 = θna`).
I also re-did the three-line proof by hand (bracket at `γ₀ = max(β, μ)`; case `β ≤ μ`:
`(1 − σ)μ + (1 − φ)B ≥ B − σ′(g − β)`; case `μ ≤ β`: `μ + (1 − φ)B − σβ ≥ B − σ′g + (σ′ − σ)β`, which uses `σμ ≥ 0` and
`σ ≤ σ′`): correct, and no hypothesis `σ ≤ 1` is needed.

### Proposition A

**Verdict: correct as stated.**

* Base case `k = 1`: `T_1 = θ`, and (Σ3) at `s = 0` is `θ(e) ≥ B − p_1(B)e` for all `e` (needs `p_1(B) = Σ(B, 0) < ∞`).  ✓
* Step: `p_{k+1}(B) < ∞` forces `p_k(B) < ∞` (P1), the induction hypothesis gives the line `(B, p_k(B))`
  below `T_k`; Lemma L with `σ = p_k(B) ≥ 0`, `σ′ = p_{k+1}(B) ≥ σ` (P1); its hypothesis `(1 − σ)θ(e) + σ′e ≥ B` is (Σ3)
  at `s = p_k(B)`, valid because `σ′ = Σ(B, σ) < ∞`; `T_k ≤ a` (`exactRec_props`, which needs `θ ≥ 0`,
  nonincreasing, bounded — all in (H0)).  ✓
* Against `lines_le_exactRec (s : ℕ → ℝ) (K)`: hypotheses `0 ≤ s 0`; `s j ≤ s (j+1)` for `j < K`;
  `B − s 0·x ≤ θna x`; `B − (1 − s j)θna e ≤ s (j+1)·e` for `j < K`; conclusion `B − s k·x ≤ exactRec θna k x` for `k ≤ K`.
  With `s j := p_{j+1}(B)` this is the statement for `T_{k+1}`; the index shift is handled correctly
  in the report (`p_k ↔ T_k`, the flat line `p_0` is *not* claimed to lie below anything).  `σ ≤ σ′` is
  available from (P1).  ✓
* `τ_k = sup T_k = T_k(0+) ≥ lim_{x↓0} (B − p_k(B)x) = B` for every `B` with `p_k(B) < ∞`.  ✓
  (`le_sSup_exactRec` is this statement.)
* Cross-check on a non-trivial case: Gaussian pair, `B_∞(2) = (3 − √5)/2`, `B_∞(3) = 0.30798`, consistent
  with the machine-checked witnesses `3/8` and `3/10` (slopes `3/7, 12/19, 21/13` re-computed by hand).
* Independent test of the inequality `τ_k ≥ B_∞(k)` against my own implementation of the recursion:
  see "Global test" below.

## §7 — Lemma PT (passage time)

**Verdict: correct as stated; I found no gap in the proof.**  Every inequality was re-derived:

* `G′ = 1/F`: `d/dx arctan((x − L)√(A/δ)) = √(Aδ)/F`.  ✓
* *Choice of the constants.*  (Σ6) for a given `ε` remains true for smaller `η, δ₀`, so one may assume
  `[L − η, L + η] ⊂ (0, s_t)`, `(1 + ε)Aη²/h ≤ η/4`, `(1 + ε)δ₀/h ≤ η/4` (hence `Δ̄ ≤ η/2`), and `κ = 3A(1 + ε)η/h < 1`.  ✓
  (The report does not say "`κ < 1`"; it is needed for the upper bound of the integral and is
  implied by "`η → 0`" — wording.)
* *Orbit.*  `x_n = p_n(h + δ)` is strictly increasing with steps `≥ δ/h` (2.1); for `δ` small,
  `h + δ < (1 − s_t)a`, so `x_{n+1} < ∞` whenever `x_n ≤ s_t`.  ✓
* *Outside the window.*  Points `x_n ≤ s_t` outside `[L − η, L + η]` are followed by a step `≥ c(η)` (Σ7), so
  there are at most `(L − η)/c + 1` of them below and `(s_t − L − η)/c + 1` above: `≤ s_t/c(η) + 2 = K(η)`.  ✓
* *Inside.*  `Δ_n ≤ (1 + ε)F(x_n)/h ≤ (1 + ε)(δ₀ + Aη²)/h = Δ̄`.  For `x ∈ [x_n, x_{n+1}]`:
  `|F(x) − F(x_n)| = A|x − x_n|·|x + x_n − 2L| ≤ A·Δ_n·(2η + Δ̄) ≤ A(1 + ε)(F(x_n)/h)(5η/2) ≤ κF(x_n)`.  ✓  Hence
  `Δ_n/((1 + κ)F(x_n)) ≤ ∫_{x_n}^{x_{n+1}} dx/F ≤ Δ_n/((1 − κ)F(x_n))`, and with (Σ6) the displayed two-sided bound.  ✓
* *Upper count.*  For `n₀ ≤ n < n₁` the point `x_n` is in the window, each such step raises `G` by at
  least `(1 − ε)/((1 + κ)h)`, and `G(x_{n₁}) − G(x_{n₀}) ≤ π/√(Aδ)` (`x_{n₁} ≤ L + η + Δ̄` is finite).  ✓
* *Lower count — the role of the overshoot.*  `n₀ ≥ 1` because `0 < L − η`; `x_{n₀−1} < L − η` gives
  `x_{n₀} ≤ Σ(h + δ, L − η) ≤ L − η + Δ̄ ≤ L − η/2` by monotonicity of `Σ` in `s` and (Σ6) at `v = −η`.  ✓  So the orbit
  enters the window in its left quarter and the part of `∫ dx/F` it misses is at most
  `(Aδ)^{−1/2}·2√(δ/A)/η`; on the right it passes `L + η`, missing at most `(Aδ)^{−1/2}·√(δ/A)/η`
  (`arctan y ≥ π/2 − 1/y`).  Total `3/(Aη)`, independent of `δ`.  ✓
* *Count.*  `N_t(δ) = #{n : x_n ≤ s_t} = #(inside) + #(outside) ≤ (n₁ − n₀) + K(η)`, and `N_t ≥ n₁ ≥ n₁ − n₀`
  because `x_{n₁−1} ≤ L + η < s_t`.  ✓
* *Order of limits.*  For fixed `(ε, η)` let `δ → 0`: `√δ·K(η) → 0` and `√δ·3/(Aη) → 0`; then `η → 0` at fixed `ε`
  (`κ → 0`), then `ε → 0`.  ✓

**Numerics** (`review_B/b3_passage.py`, output `out_b3_passage.txt`; `Σ` from the definition of `θ`).
Six pairs, none of them the Gaussian pair or the cube at `u = 1`; two cut levels each (`L + 0.02`
and close to `1 − h/a`); `δ/h = 10⁻², …, 10⁻¹⁰` (cube: to `10⁻⁸`):

| pair | `c_* = πh√(2ϑ)` | `√δ·N_t/c_*` at `δ/h = 10⁻⁴, 10⁻⁶, 10⁻⁸, 10⁻¹⁰` (`s_t = L + 0.02`) | `N_t − c_*/√δ` (same, last) |
|---|---|---|---|
| `(1 − e)₊²` | 0.717756 | 0.94717, 0.99453, 0.99944, 0.99994 | −6.4 |
| `(1 − √e)₊³` | 0.731647 | 0.91718, 0.99126, 0.99913, 0.99992 | −14.3 |
| `e^{−2e}` | 0.980839 | 0.93194, 0.99252, 0.99924, 0.99993 | −10.7 |
| `0.1 + 0.9e^{−3e}` | 1.082675 | 0.91603, 0.99160, 0.99916, 0.99991 | −15.4 |
| cube `u = 2` | 0.479688 | 0.92330, 0.99222, 0.99925 (`10⁻⁸`) | −11.6 |
| cube `u = 3` | 0.623187 | 0.92727, 0.99265, 0.99925 (`10⁻⁸`) | −11.2 |

The limit is `c_*` in all cases, and `N_t(δ) − c_*/√δ` stays bounded (a constant depending on the
pair and on `s_t`), as the proof predicts (`K(η)` and `3/(Aη)` are `δ`-free).  Part (c) of the script
checks the inequalities of the proof themselves for `θ = (1 − √e)₊³`, `η = 0.01` and `0.003`: with `ε`
measured on the window, `Δ̄ ≤ η/2`, `x_{n₀} − (L − η) ≤ Δ̄`, the increments of `G` lie in the proof's interval
(they are `5.400…5.409`, i.e. `1/h = 5.404`), `n₁ − n₀` lies between the proof's two bounds and
`N_t ∈ [n₁ − n₀, n₁ − n₀ + K(η)]` — all true at `δ = δ₀, δ₀/10², δ₀/10⁴`.

**(H1) is the right hypothesis — it is about `J`, not about `θ ∈ C²`** (`review_B/b11_H1_not_C2.py`,
output `out_b11_H1_not_C2.txt`).  For `θ(e) = (1 − √e)² + 0.3·x⁴sin²(1/x)·ψ(x)`, `x = e − ¼`, `ψ` a `C²` cut-off
(convex and decreasing: checked on `4.5·10⁵` points), the second derivative
`θ″(¼ + x) = 4 + 0.6cos(2/x) + O(x)` has **no limit** at the fixed point (measured values between `3.75`
and `4.58` down to `x = 3·10⁻⁵`), while `J(t) = t − t² + O((t − ½)⁴)` satisfies (H1) with `ϑ = ½`.  Result:
the ratio of (Σ6) is `1.00000` at `v = 0` and `1 ± 0.004` at `|v| = 10⁻³` for `δ ≤ 10⁻⁶` (identical to the
Gaussian pair), and `√δ·N_t/(π/4) = 0.96766, 0.99695, 0.99962, 0.99996` at `δ = 10⁻⁴, …, 10⁻¹⁰` —
the same numbers as for the Gaussian pair to five digits.  So the constant is governed by
the second-order expansion of `J` at `L`, exactly as (H1) and (Σ6) say.

## §8 — lower bound of Theorem R

**Verdict: correct as stated** (`liminf k²(τ_k − h) ≥ 2π²h²ϑ` under (H0), (H1)).

* `k < N_t(δ)` means `x_k = p_k(h + δ) ≤ s_t` (the orbit is increasing and `N_t` is the first index above
  `s_t`), so `p_k(h + δ) < ∞` and Proposition A gives `τ_k ≥ h + δ`.  ✓
* Lemma PT: for small `δ`, `N_t(δ) ≥ (1 − ε)c_*/√δ`; with `δ = (1 − ε)²c_*²/(k + 1)²` (small when `k` is large) this is
  `N_t(δ) ≥ k + 1 > k`.  ✓  Hence `k²(τ_k − h) ≥ (1 − ε)²c_*²·k²/(k + 1)²`.  ✓
* A cut level `s_t ∈ (L, 1 − h/a)` exists by consequence (ii).  ✓
* Ingredients and their status: Lemma L and its iteration [V]; (Σ3) (definition); (P1) (two lines);
  (2.1), (Σ6), (Σ7), Lemma PT [P] — all checked above.  The lower bound does not use §§5–6.

Numerical confirmation that the inequality `τ_k ≥ B_∞(k)` is true and asymptotically sharp: see
the global test.

## §8a (added to the report while this review was in progress — not in the brief)

The report was changed twice after the version I was given (commit `020e990`, 530 lines): commits
`fc3f5d9` and `0b1b0f5` add §8a (Proposition S, a closed form for the profile at positive
accuracy, marked "P-sketch"), two rows of §11 (`r3_gauss_exact_lb.py`, `r4_profile.py`) and rewrite
items 2 and 4 of §12.  `git diff 020e990 HEAD` shows **no change in §§1–7, 8, 9, 10**, so the verdicts
of this review apply to the current text (line numbers after §8 are shifted by 44).

I did **not** review the sketch of Proposition S.  A quick consistency check
(`review_B/b13_profile_8a.py`, output `out_b13_profile_8a.txt`), for what it is worth:

* the stated properties of `f(ζ) = sup_z [2z² + 2ζz·cot z] − ζ²/2` hold: `f(0) = 2π²` (supremum as `z → π`),
  `f(2) = π²/2 − 2` (maximiser `z = π/2`, from the stationarity condition `cot z·(1 − z·cot z) = 0`),
  `f′(2) = −2`, `f(3) = 3/2`, `f′(3) = −1` (`z → 0`); the residual of `ζf′²/2 + ζf′ + (ζ − 2)f` is `≤ 4·10⁻⁴` by
  finite differences at `ζ = 0.5, 1, 2, 3, 4`; the limit `ζ → 0` of the equation is consistent
  (`ζf′²/2 → 4π² = 2f(0)`);
* the algebra `B − p_k(B)x − θ_hint(x) = (h²ϑ/k²)[2z² + 2ζz·cot z − ζ²/2]` from the position formula is right;
* the position formula `p_k(h + δ) − L ≈ −√(δ/A)·cot(√(Aδ)k/h)` on a pair of mine (`(1 − √e)₊³`):
  `k(p_k − L) = −0.2682, −0.1881, +0.0002, +0.4700, +2.3138` at `z = 0.5, 1, π/2, 2.2, 2.8`, `k = 1600`, against
  `−0.2683, −0.1882, 0, +0.4694, +2.3085` (the error decreases like `1/k`);
* the profile of **my** iteration of the recursion against `f`: `(1 − √e)₊³` at `k = 61`:
  `11.89, 9.19, 6.07, 2.98, 1.52, 0.394` at `ζ = ¼, ½, 1, 2, 3, 5` against `f = 11.77, 9.09, 5.99, 2.93, 1.50, 0.388`;
  Gaussian at `k = 40`: `11.61, 8.96, 5.90, 2.88, 1.47, 0.376`.  Agreement within `1–3 %`, with the sign
  of the deviation following the sign of the offset `c₀` of each pair.
* `r3_gauss_exact_lb.py`: its exact rational lower bounds agree with the closed form of §10 in
  my simplified version, e.g. `τ_160 ≥ 0.250023947` against `1/(4cos²(π/321)) = 0.2500239473…`.

So I see nothing against Proposition S, but its two unwritten steps (a *uniform* position
estimate, and the exchange of the limit with the supremum over `z`) are real gaps as long
as they are not written; the label "P-sketch" is the right one.

## §9 — Proposition K and the heuristic classification

### Proposition K

**Verdict: the lower bound `τ_k − h ≥ (L₂ − L₁)h/(k + 2)` is correct as stated; the two-sided
"`Θ(1/k)`" needs one sentence that is not in the report (the a-priori bound applied to an
abstract (H0) function) — a gap of exposition, not of substance.**

Line by line:

* `J = h` on `[L₁, L₂]`: §1.  ✓
* *The exact step.*  `t(s) = (s + w₀)/(1 + w₀)` is increasing in `s`, `t(s_max) = (L₂ + L₂w₀)/(1 + w₀) = L₂`, `t(L₁) ≥ L₁`; so for
  `s ∈ [L₁, s_max]`: `Ψ_s(w₀) = (1 + w₀)·h = h + δ`, and `Ψ_s(w) ≤ (1 + w)h < h + δ` for `w < w₀`.  Hence
  `D(h + δ, s) = δ/h` exactly.  ✓  (This is the case of equality in (2.1).)
* *The count.*  `x_{n₀} ≤ Σ(B, L₁) = L₁ + w₀` (monotonicity in `s`; the points below `L₁` are regular because
  `L₁ ≤ s_max`), then `x_{n₀+m} ≤ L₁ + (m + 1)w₀ ≤ s_max` as long as `m + 1 ≤ (L₂ − L₁)/w₀ − (1 − L₂)`, i.e. `m ≤ n*`; as
  `n₀ ≥ 0`, `x_n ≤ s_max` for all `n ≤ n*`.  ✓
* *Regularity.*  `1 − s_max = (1 − L₂)(1 + w₀)` and `(1 − L₂)a ≥ J(L₂) = h`, so `B = h(1 + w₀) ≤ (1 − s_max)a`, with strict
  inequality for `s < s_max`.  ✓  (At `s = s_max` itself `Σ = s_max + w₀ < ∞` by the exact step even if the
  point is on the boundary.)  So `p_n(B) < ∞` for `n ≤ n*` (in fact for `n ≤ n* + 1`).  ✓
* `k ≤ n* ⇔ k ≤ (L₂ − L₁)h/δ − (1 − L₂) − 1` (`k` integer); with `δ = (L₂ − L₁)h/(k + 2)` the right side is `k + L₂ ≥ k`,
  and `n* = k`.  ✓  Proposition A then gives `τ_k ≥ h + δ`.  ✓
* The example: `θ = max(1 − 3e, ½ − e, 0)`, `θ(¼) = ¼`, `∂θ(¼) = [−3, −1]`, `L₁ = ½`, `L₂ = ¾`, and
  `J(t) = min(1 − t, ¼, t/2)` (values at the vertices `0+, ¼, ½`).  ✓  `τ_k − ¼ ≥ 1/(16(k + 2))`.  ✓
* *The upper half of `Θ(1/k)`.*  `RateFull.rate_top0` is stated for a `HintPair θna θh a h E`
  (`HintRecursion.lean:53`), whose fields involve a hinted function `θh` (`ident`, `hint_pos`,
  `hint_mono`, `hint_lower`).  For an abstract `θ` with (H0) — in particular for the kinked
  example — the report does not say which `θh` is meant.  It is the sheared function of §1,
  `θh(e) = y ⇔ θ(e + y) = y`: `ident` holds by definition, `e + θh(e)` is increasing, `θh > 0` where
  `θ > 0` (take `E = h`, say), and `hint_lower` holds with `L = 1` because `θh` is convex with slopes in
  `(−1, 0]`.  With this sentence the claim "`τ_k − h ≤ c₁/(k + c₂)` under (H0) alone" is justified as
  far as the *hypotheses* go (I did not re-read the proof of `rate_top0`; that is Referee A's
  item 4).

**Numerics** (`review_B/b5_kink_heuristic.py`, output `out_b5_kink_heuristic.txt`; `Σ` from the
definition of `θ`).  Three kinked functions: the author's; `max((1 − √e)², ¼ + 0.4(¼ − e))` (a kink
between a strictly convex and an affine piece, `[L₁, L₂] = [2/7, ½]`); and the edge case `L₁ = 0`,
`θ = max(1 − 3e, ¼)` (flat to the right of `h`, `[L₁, L₂] = [0, ¾]`).  In all three: `J = h` on `[L₁, L₂]` and
`< h` outside; `|D(h + δ, s) − δ/h| ≤ 2·10⁻¹⁶` on `[L₁, s_max]` and `D > δ/h` outside; `p_n(h + δ) < ∞` for all
`n ≤ n*` (`δ = 10⁻², 10⁻³, 10⁻⁴`); `B_∞(k) − h ≥ (L₂ − L₁)h/(k + 2)` for `k = 1, …, 320`, and
`k·(B_∞(k) − h) → (L₂ − L₁)h` (`0.06275 → 0.0625`; `0.18794 → 0.1875`): the constant of Proposition K is
the sharp constant of the lower bound `B_∞`.

### The heuristic classification [C]

**Verdict: plausible; the lower-bound halves are confirmed numerically, and for `p = 1` my
own iteration of the recursion shows geometric convergence at the rate of the lower
bound.  No error found; two refinements are offered.**

* *`p > 1`.*  From the identity of (Σ6), `hw = δ + (1 + w)(h − J(L + q))`, `q = (v + (1 − L)w)/(1 + w)`: if `h − J(L + q) ≍ |q|^p`
  with `p > 1` then `w ≍ δ + |v|^p` (the feedback term `(1 − L)w` is of lower order), the passage time is
  `≍ ∫ dv/(δ + |v|^p) ≍ δ^{−(p−1)/p}`, and `B_∞(k) − h ≍ k^{−p/(p−1)}`.  Checked on two functions built for the
  purpose: quartic contact `θ = ¼ − x + 8x⁴` (`x = e − ¼`; `θ″(h) = 0`, `p = 4/3`): measured exponent of
  `N_t(δ)` `0.2542` (prediction `0.25`), of `B_∞(k) − h` `3.92` at `k = 160…320` (prediction `4`, still
  converging); and `θ = ¼ − x + 2|x|^{3/2}` (`θ″(h) = ∞`, `p = 3`): `0.6667` (prediction `⅔`) and `1.5085`
  (prediction `1.5`).  ✓  So for `1 < p < 2` the recursion is *faster* than `k⁻²` (at least its lower
  bound is), for `p > 2` slower.
* *`p = 1`* (`θ` affine near `h`).  The report's "passage time `≍ ln(1/δ)`" is right, and can be made
  precise: with `c_∓ = ±J′(L∓)` the map `s ↦ Σ(h, s)` has at `L` the one-sided multipliers

      λ₋ = (h − c₋L)/(h + c₋(1 − L)) ∈ [0, 1),        λ₊ = 1 + c₊/(h − c₊(1 − L)) ∈ (1, ∞]

  (solve `hw = c|v + (1 − L)w|` for `w` on each side), the passage time is
  `ln(1/δ)·[1/ln(1/λ₋) + 1/ln λ₊]·(1 + o(1))`, and `B_∞(k) − h = exp(−(ρ + o(1))k)`,
  `ρ = 1/[1/ln(1/λ₋) + 1/ln λ₊]`.  Test: the Gaussian `θ` with the arc over `[0.16, 0.36]` replaced by its
  chord (`h = 0.26`, `L = ½`, `c_∓ = 0.2`): predicted `λ₋ = 4/9`, `λ₊ = 9/4`, measured `0.444444`, `2.250000`;
  predicted ratio of consecutive `B_∞(k) − h`: `e^{−ρ} = ⅔`, measured `0.66666` at `k = 30`.  ✓
  **The recursion itself** (my implementation, see the global test; `out_b7_chord.txt`):
  `τ_k − h` decreases geometrically, by factors alternating `0.638 / 0.698` (product `0.445 ≈ (⅔)²`)
  for `k = 10, …, 31`, with `τ_k ≥ B_∞(k)` throughout and `(τ_k − h)/(B_∞(k) − h) ∈ [1.16, 1.21]`.  So in this
  example the true rate is geometric *with the same ratio as the lower bound*.
* *Degenerate `p = 1`.*  For `θ = (1 − 2e)₊` (affine through the fixed point, `J = min(1 − t, t/2)`),
  `λ₋ = 0` and `λ₊ = ∞`: `Σ(B, s) = 2B` for `s ≤ 1 − B`, `B_∞(k) = h = ⅓` for every `k ≥ 2`, and my iteration
  of the recursion gives `τ_2 = ½`, `τ_3 = 0.33368`, `τ_4 = 0.3333333 = h` (to grid accuracy): the
  recursion reaches `h` after finitely many levels.  "Geometric" in the report's sentence should
  therefore read "geometric or faster".
* *`p → ∞`* is the kink (flat maximum): consistent with Proposition K.  ✓
* *A case the classification omits: `p = 2` with different curvatures on the two sides*
  (`θ″(h−) ≠ θ″(h+)`, so `J(L + q) ≈ h − q²/(2ϑ_±)`; (H1) fails, rightly, since it asks for one `ϑ`).
  The proof of Lemma PT goes through side by side and gives
  `√δ·N_t(δ) → (πh/2)(√(2ϑ₊) + √(2ϑ₋))`, hence `liminf k²(τ_k − h) ≥ [(πh/2)(√(2ϑ₊) + √(2ϑ₋))]²`.
  Checked (`b12_onesided.py`): `θ = (1 − √e)²` left of `¼`, `¼ − x + 4x²` right of it (`ϑ = ½` and `1`):
  `√δ·N_t = 0.94813` at `δ = 10⁻¹⁰` against `(π/8)(1 + √2) = 0.94806` (and not `π/4 = 0.785` or `1.111`).
  Worth one line in §9: the constant of Theorem R is the square of the *mean* of the two
  one-sided values of `πh√(2ϑ)`.
* The report is right that only the lower bounds follow from Proposition A as it stands.

## §10 — the Gaussian pair (Möbius computation)

**Verdict: correct as stated; the closed form, marked [N] in the report, can be upgraded to
[P] — the conjugation is written out here, and it simplifies.**

* `y = 1 − s`: `1 − B(1 − s)/(1 − s − B) = ((1 − B)y − B)/(y − B)`.  ✓  Matrix `[[1 − B, −B], [1, −B]]`: trace `1 − 2B`,
  determinant `−B(1 − B) + B = B²`.  ✓  Characteristic polynomial `λ² − (1 − 2B)λ + B²`, discriminant `1 − 4B`:
  parabolic at `B = ¼`, elliptic for `B > ¼`, `λ = Be^{±iψ}`, `cos ψ = (1 − 2B)/(2B)`, `sin ψ = √(4B − 1)/(2B)`.  ✓
  `tan ψ = √(4B − 1)/(1 − 2B) ≈ 4√(B − ¼)`.  ✓  (For `B > ½` the arctangent has to be read as `atan2`.)
* *The conjugation.*  An eigenvector for `λ = Be^{iψ}` is `(λ + B, 1)ᵀ = u₁ + iu₂` with `u₁ = (½, 1)ᵀ`
  (because `B(1 + cos ψ) = ½`), `u₂ = (√(4B − 1)/2, 0)ᵀ`.  Writing `(y, 1)ᵀ = u₁ + c·u₂`, `c = (2y − 1)/√(4B − 1)`, the
  map multiplies the complex coordinate `1 − ic` by `Be^{iψ}`; so `α̃(y) := arccot((2y − 1)/√(4B − 1)) ∈ (0, π)`
  increases by `ψ` per level (mod `π`), with `α̃(+∞) = 0`, `α̃(−∞) = π`.  For `y_1 = (1 − 2B)/(1 − B)`:
  `2y_1 − 1 = (1 − 3B)/(1 − B)`, so `α̃(y_1) = arccot((1 − 3B)/((1 − B)√(4B − 1))) = φ₀(B)` — the report's formula.  ✓
  `p_k(B) < ∞` iff `y_j > B` for `j ≤ k − 1` iff `α̃(y_{k−1}) < α̃(B) = π − ψ` iff `(k − 1)ψ + φ₀ < π`.  ✓
* *Simplification.*  With `ε = √(4B − 1)`: `tan ψ = 2ε/(1 − ε²)`, so **`ψ = 2 arctan ε`**, and `α̃(y_0) = α̃(1) = arctan ε`.
  The equation becomes `(2k + 1)·arctan √(4B − 1) = π`, i.e.

      B_∞(k) = 1/(4·cos²(π/(2k + 1)))        (Gaussian pair, every k ≥ 1),

  which gives `B_∞(1) = 1 = a`, `B_∞(2) = (3 − √5)/2`, and
  `B_∞(k) − ¼ = ¼tan²(π/(2k + 1)) = (π²/16)/(k + ½)²·(1 + (π²/6 + o(1))/k²)`.  ✓ (the report's `1 + O(k⁻²)`).
* Numerically (`b4_orbits_gauss.py`, mpmath 40 digits): for `k = 1, …, 1000` the root of the report's
  equation, the formula `1/(4cos²(π/(2k + 1)))` and the bisection on the orbit itself agree to
  `10⁻³³`; the ratios to `(π²/16)/k²` at `k = 100, 160, 320` are `0.990236, 0.993843, 0.996898` (report §11:
  `0.9902, 0.9938, 0.9969` ✓); `k²·[(B_∞ − ¼)(k + ½)²/(π²/16) − 1] → 1.643 ≈ π²/6`.
* `c_* = πh√(2ϑ) = π/4` and the rotation number `π/ψ ≈ π/(4√δ)` agree: the Gaussian pair is an exact
  instance of Lemma PT.  ✓

## Global test of Theorem R (own implementation of the recursion)

**Scripts:** `review_B/b6_recursion.py` (the recursion), `b7_compare.py` (comparison with the orbit
lower bound and the claimed limit), `b8_lines_vs_levels.py` (Proposition A at positive accuracy).
Outputs `out_b6_*.txt`, `out_b7_*.txt`, `out_b8_lines_gauss.txt`.

**What is computed.**  `T_{k+1} = min(T_k, R[T_k])` on a geometric grid of accuracies
(`[10⁻⁹, x_max]`, ratio `1.01` or `1.005`, i.e. 2084 or 4157 nodes), `T` piecewise linear in between.
For each node `g` the bracket is minimised over `(φ, β)` — a grid of 160–640 values of `logit φ`
(covering `φ ≈ g/(40x_max)` up to `1 − 10⁻⁶`) times 14 values of `logit(β/g)` (from `β/g = 10⁻¹⁵` to `0.998`),
followed by 7 rounds of a 9 × 9 local zoom.  The supremum over `γ ≥ β` is evaluated exactly for the
interpolant: `(1 − φ)·max_{[β/(1−φ), μ/(1−φ)]} (y + T(y))` by a range-maximum table if `β ≤ μ`, and
`μ + (1 − φ)T(β/(1 − φ))` otherwise.  **No shortcut is used**: not "`x + T(x)` nondecreasing", not
"`β → 0`" (at levels 2–4 the optimal `β/g` is not small: median `0.34, 0.15, 0.05` for the Gaussian
pair; from level 6 on it is at the lower end of the grid).  `τ_k` is taken (A) from the node
`g_min = 10⁻⁹` and (B) from the one-parameter formula at accuracy zero,
`τ_{k+1} = min(τ_k, inf_φ (1 − φ)·sup_{0<y≤φa/(1−φ)} (y + T_k(y)))`; the two agree to `10⁻⁵` at the first
levels and to `5·10⁻⁷` or better from `k = 20` on (A is slightly smaller: the computed `T_k(g)`
behaves like `τ_k − c_k√g` for `g ≲ 10⁻⁶`, with a small `c_k` — the square-root singularity of `θ` at
zero is inherited by every level; this does not conflict with anything in the report).  All
numbers quoted below are (B).  The minimisation over a grid can only *over*-estimate
the infimum; the interpolation error has no sign.  The code shares nothing with the report's
machinery (no `J`, no `Σ`, no lines).

**Cross-check with the author's implementation** (`iterate_exact.py`, different grids and
parametrisation): Gaussian pair, `τ_2 = 0.5000000` (mine; exact value `½`: `sup_{y≤Y}(y + θ(y)) = max(1, Y)`,
so `inf_φ max(1 − φ, φ) = ½`) against his `0.50033`; `τ_10 = 0.2559953` against `0.2560224`;
`τ_20 = 0.2515109` against `0.2515146`; `τ_40 = 0.2503812` against `0.2503816`.  Mine are
consistently a little lower (finer minimisation), the difference is `≤ 3·10⁻⁵` from `k = 10` on.

**Results for four pairs with (H1)** (`h`, `c_*` from `blib.py`; `B_∞(k)` from the orbit of the slope map,
computed from the definition of `θ`; `Q_k := (τ_k − h)^{−1/2}`: Theorem R says `c_*·Q_k/k → 1`, and the
increments `c_*·(Q_k − Q_{k−4})/4` are the sharper diagnostic of the same statement):

| pair | `c_*²` | `k` | `τ_k − B_∞(k)` | `k²(B_∞ − h)/c_*²` | `k²(τ_k − h)/c_*²` | `c_*(Q_k − Q_{k−4})/4` | offset `c_*Q_k − k` |
|---|---|---|---|---|---|---|---|
| `(1 − √e)₊³` (new) | 0.535308 | 20 | `+1.1·10⁻⁴` | 0.9509 | 1.0365 | 1.0114 | −0.355 |
| | | 40 | `+1.4·10⁻⁵` | 0.9739 | 1.0149 | 1.0013 | −0.294 |
| | | 60 | `+4.1·10⁻⁶` | 0.9822 | 1.0095 | 0.9998 (1.0005 on the finer grid) | −0.283 |
| `(1 − e)₊²` (new, finite slope at 0) | 0.515174 | 20 | `+3.8·10⁻⁵` | 0.8979 | 0.9272 | 1.0051 | +0.771 |
| | | 40 | `+5.1·10⁻⁶` | 0.9451 | 0.9608 | 1.0010 | +0.808 |
| | | 60 | `+1.6·10⁻⁶` | 0.9624 | 0.9734 | 0.9999 | +0.816 |
| Gaussian | 0.616850 | 16 | `+7.3·10⁻⁵` | 0.9460 | 0.9764 | 1.0064 | +0.193 |
| | | 40 | `+4.7·10⁻⁶` | 0.9764 | 0.9887 | 1.0005 | +0.228 |
| | | 52 | `+2.2·10⁻⁶` | 0.9816 | 0.9912 | 0.9999 | +0.230 |
| cube `u = 2` (from the `KL` definitions; the author iterated `u = 1`) | 0.230101 | 20 | `+4.4·10⁻⁶` | 0.9535 | 0.9611 | 1.0024 | +0.401 |
| | | 40 | `+5.8·10⁻⁷` | 0.9755 | 0.9795 | 1.0004 | +0.417 |
| | | 60 | `+1.8·10⁻⁷` | 0.9833 | 0.9862 | 0.9995 | +0.418 |

* **`τ_k ≥ B_∞(k)` at every level computed** (`k ≤ 61`, all pairs, including the kinked and the
  affine ones below): Proposition A is confirmed, and for the four pairs of the table the gap
  `τ_k − B_∞(k)` decays faster than `τ_k − h` (like `k⁻³`, as it must if both are `c_*²/(k + c)²` with
  different offsets).
* **The increments of `(τ_k − h)^{−1/2}` converge to `1/c_*`** within `10⁻³` (the noise of the computation)
  for all four pairs; equivalently `τ_k − h = c_*²/(k + c₀ + o(1))²`.  This is Theorem R with the
  constant `2π²h²ϑ`, on three cases the author did not iterate, to about `0.1 %` in the constant.
  A wrong constant would show as a drift of the "offset" column proportional to `k`; the
  offsets are stable to `±0.01` between `k = 40` and `60`.
* Accuracy of the computation (`(1 − √e)₊³`).  Grid ratio `1.01` against `1.005` (160 against 200
  values of `φ`): `τ_k` changes by `≤ 4·10⁻⁸` for `24 ≤ k ≤ 60` (`τ_60 − h = 1.5·10⁻⁴`).  160 against 640
  values of `φ` at ratio `1.01`: the runs differ by `1.6·10⁻⁵` at `k = 10` (the *coarser* search found
  the lower value — the two-parameter minimisation is not convex and neither search is
  guaranteed to find the global minimum at the early levels), decaying to `1.4·10⁻⁷` at `k = 40`
  (`0.04 %` of `τ_40 − h`), with the same increments (`1.0013` in both).  So the early levels carry an
  uncertainty of a few `10⁻⁵`, which only shifts the offset `c₀` by `≈ 0.01`; the constant of the
  `k⁻²` law is insensitive to it.
* *A remark on §8, "the true sequence behaves like `c_*²/(k + c)²` with `c ≈ 0.15–0.25`, between `c = ½`
  (lower bound) and `c ≈ 0`".*  That is specific to the author's two pairs.  For `(1 − √e)₊³` the
  offset of the true sequence is **negative**, `c ≈ −0.28` (`k²(τ_k − h)` approaches its limit *from
  above*; the lower bound has `c ≈ +0.54`), and for `(1 − e)₊²` it is `≈ +0.82` (lower bound `≈ +1.16`).
  Not an error — a finite-`k` remark that should not be read as general.

**Pairs without (H1)** (the law changes, as §9 says):

* *Kinked pair `θ = max(1 − 3e, ½ − e, 0)`* (`out_b7_kink_q1.0075_nz640.txt`; 640 values of `φ`):
  `k(τ_k − h) = 0.0873, 0.0773, 0.0709, 0.0679, 0.0669` at `k = 8, 12, 20, 32, 40`, decreasing towards
  `(L₂ − L₁)h = 0.0625`; the increments of `1/(τ_k − h)` are `15.75…15.93` for `8 ≤ k ≤ 40` (those of the
  lower bound `B_∞` are `16`); `τ_k − B_∞(k) > 0` decreasing (`6·10⁻⁵` at `k = 40`).  So `τ_k − h ≈ (L₂ − L₁)h/(k + c)`:
  rate `1/k` as Proposition K says, and apparently with the *same constant* as the lower bound.
  `k²(τ_k − h)` grows linearly (`2.7` at `k = 40`), nothing like a `k⁻²` law.
  **Caveat on my own numerics:** for this piecewise-linear pair the result depends on the
  resolution of the `φ`-search.  With 160–200 values of `φ` (three grids, ratios `1.01`, `1.005`,
  `1.0017`) the increments of `1/(τ_k − h)` drop in steps (`15.9 → 14.9 → 13.4 → …`) from `k ≈ 17` on and
  `k(τ_k − h)` turns upward (`0.0706` at `k = 32` instead of `0.0679`); refining the *accuracy grid*
  does not remove this, refining the *search* does.  I therefore trust the 640-point run to
  `k ≈ 40` only, and the statement "same constant" is an observation, not a result.
* *`θ` affine near `h`* (Gaussian with a chord, `p = 1`): geometric convergence with ratio `≈ ⅔` per
  level, as reported under §9.  *`θ = (1 − 2e)₊`:* `τ_4 = h` to grid accuracy.

**An adversarial test of Proposition A** (`b9_stress_propA.py`, output `out_b9_stress_propA.txt`):
six unusual (H0) functions, 9 levels each, `τ_k` from the recursion against `B_∞(k)` from the orbit:
`0.3e^{−e}` (`a` barely above `h`), `max(1 − 10e, 0.05)` (steep, then flat at a positive value), `(1 + e)⁻⁴`
(never zero), `0.1 + 0.9e^{−3e}` (`θ(∞) > 0`), a kink at `h` next to a strictly convex piece, and `1 − √e`.
In no case and at no level is `τ_k < B_∞(k)`.  The test has teeth: **for `0.3e^{−e}` and for `1 − √e`
the two numbers coincide to the accuracy of the computation** (`τ_k − B_∞(k)` between `0` and
`+2·10⁻⁷` for `0.3e^{−e}`, between `0` and `+2.6·10⁻⁶` for `1 − √e`, `k = 2, …, 9`; e.g. `τ_3 = 0.4285740` against
`B_∞(3) = 3/7` for `1 − √e`), i.e. there are pairs for which the lower bound of Proposition A is
attained (apparently exactly), so a lower bound even slightly too large would have shown
up as a violation.  (A numerical `τ_k` can err upwards through the minimisation, so a
violation could in principle be masked by an error larger than the true gap; with gaps
`≥ 0` and errors of `10⁻⁷…10⁻⁶` the test is meaningful only at that level.)  The coincidence is what
remark (1) of §5 of the report predicts when the cut by the tangent through `(τ_{k+1}, 1)` does
not reach the root of `S_k(B) = 1 − B/a`.  For `0.3e^{−e}` it follows from the report's own
statements: `Σ(B, s) ≤ (1 − s)·|θ′(0+)| ≤ 0.3` on the regular region, so every `p_k ≤ 0.3 < 1` is an
admissible `W` in Proposition U, `T_1 = θ` is the envelope of its tangent lines `(B, p_1(B))`, and
Corollary U′ gives `τ_k ≤ sup{B : p_k(B) < ∞} = B_∞(k)` by induction, with no cut at all.  So this
test supports Proposition U from the other side as well: *for every (H0) function with
`|θ′(0+)| ≤ 1` the report's two bounds coincide, `τ_k = B_∞(k)` exactly* (if Proposition U is right),
and the numbers agree with that to `2·10⁻⁷`.

**A sharp test of the two bounds together** (`b14_slope_le_one.py`, output
`out_b14_slope_le_one.txt`), following the last remark.  Functions with slope `m = |θ′(0+)| ≤ 1`:
`0.3e^{−e}` (`m = 0.3`), `e^{−0.8e}` (`0.8`), `0.5e^{−2e}` (`1`), `(1 − e)₊` (`1`, affine); and for contrast
`e^{−1.5e}` (`m = 1.5`) and `e^{−3e}` (`m = 3`).  `τ_k` from my iteration of the recursion (320 values of `φ`),
`B_∞(k)` from the orbit, `k = 2, …, 9`:

| `θ` | `m` | `τ_k − B_∞(k)`, `k = 2…9` | relative to `τ_k − h` |
|---|---|---|---|
| `0.3e^{−e}` | 0.3 | `2·10⁻⁸ … 2·10⁻⁷` | `≤ 2.6·10⁻⁵` |
| `e^{−0.8e}` | 0.8 | `3·10⁻⁸ … 5·10⁻⁷` | `≤ 3·10⁻⁵` |
| `0.5e^{−2e}` | 1 | `1·10⁻⁹ … 3·10⁻⁷` | `≤ 4.4·10⁻⁵` |
| `(1 − e)₊` | 1 | `0` (both equal `h = ½` from `k = 2`) | — |
| `e^{−1.5e}` | 1.5 | `3·10⁻⁷ … 2·10⁻⁶` | `≤ 3.5·10⁻⁵` |
| `e^{−3e}` | 3 | `3.7·10⁻², 7.5·10⁻³, …, 2.5·10⁻⁴` | `22 % … 2.8 %` |

For `m ≤ 1` the recursion and the orbit bound agree to the accuracy of my computation at
every level, as Propositions A and U together predict; for `m = 3` they differ by `22 %` of
`τ_2 − h`, so the agreement is not an artefact of the code.  (For `m = 1.5` they still agree
numerically, although `p_1 > 1` near `B = a`: the cut that Proposition U then requires apparently
does not reach the root of `S_k(B) = 1 − B/a`; I have no proof of that.)  A by-product worth a
remark in the report:
**for pairs with `|θ_na′(0+)| ≤ 1`, `τ_k = B_∞(k)` for every `k` and Theorem R follows from the
lower-bound analysis (Lemma PT) and Proposition U alone — §6 (cut curves, restart, Lemma RC)
is not needed.**  The cube and the Gaussian pair have `m = ∞` and do need §6.

**Proposition A at positive accuracy** (`b8_lines_vs_levels.py`, Gaussian pair, levels
`2, 3, 5, 10, 20, 40`): for 400 intercepts `B ∈ (0, B_∞(k))` per level the line `B − p_k(B)x` lies below the
computed `T_k` at every grid node: `max_{B,x} [B − p_k(B)x − T_k(x)]` is between `−4·10⁻⁹` and `−1.5·10⁻¹⁰`
(never positive; the lines with small `B` touch `T_k`).

## The author's code (`rlib.py`, `r1_checks.py`), read critically

* `r1_checks.py` re-run: output identical to the stored `out_r1_checks.txt`, "ALL CHECKS PASS".
* `rlib.Pair.sigma` computes `Σ` through `J`: `Σ = t′(1 − s)/(1 − t′)` with `t′` the least root of
  `Q(t′) = J(t′)/(1 − t′) ≥ B/(1 − s)`.  This is (Σ5) rewritten (`1 + w = (1 − s)/(1 − t′)`), and `Q` is
  nondecreasing (an infimum of increasing functions of `t`), so the bisection is legitimate.  But
  it means that checks 1–4 of `r1_checks.py` test consequences of (Σ5), not (Σ5) itself: e.g.
  "joint convexity of `Σ`: 0.00e+00" is convexity of the formula, not of the supremum over `e`.
  My `b2_sigma.py` closes this: `Σ` from the definition agrees with `min{w : Ψ_s(w) ≥ B}` to `10⁻¹²`.
* The docstring "`J(0) = J(1) = 0`" and "`Q` increasing from 0 to `a`" assume `θ(∞) = 0`.
* `rlib.Kinked.sigma` (vertices `¼`, `½`, the limits `e → 0` on the boundary and `e → ∞`) is the correct
  supremum for `max(1 − 3e, ½ − e, 0)`.
* Direct comparison (`b10_author_lib.py`, 400 random regular points per pair): `Σ` of `rlib` (through
  `J`) against my `Σ` from the definition — relative difference `≤ 6·10⁻¹⁵` (Gaussian), `7·10⁻¹³`
  (cube `u = 1`), `3·10⁻¹³` (cube `u = 2`), `3·10⁻¹⁶` (kinked pair); `θ_na` identical at six points.
  So the library is right; my objection is only to what the checks can and cannot show.
* The constants `h, L, ϑ, a` produced by `rlib` for the cube at `u = 1, 2` agree with mine from the
  `KL` definitions (`ϑ` to 8 digits — it is a second difference with step `10⁻⁴`).

## Minor points and suggested edits (none affects Theorem R)

1. (Σ3): add "and `B < (1 − s)a`" to the attainment claim (it can fail on the boundary when `θ′(0+)`
   is finite).
2. (Σ5), first bullet: "the fixed points are the solutions of `J(s) = B`: two for `B < h`" is wrong
   when `B ≤ θ(∞)` (`s = 0` is a fixed point, one root) and when the upper root lies on the boundary
   `B = (1 − s)a` of a pair with a finite slope at zero (no upper fixed point).  State it for
   `B ≥ h` only, or add the two exceptions.  Also say `D = ∞` when `{w : Ψ_s(w) ≥ B}` is empty.
3. §1: say that for an abstract `θ` the function `θ_hint` is *defined* by the shear, and that under
   (H1) "`θ_hint″(0)`" is the coefficient of its second-order expansion at `0`.
4. (P1): lower semicontinuity is asserted but not argued (two lines, given above).
5. Lemma PT: say "`η` so small that `κ < 1`".
6. §1 / §8 / Proposition K: the a-priori bound is machine-checked for a `HintPair`; say that every
   (H0) function gives one through the shear (`L = 1` in `hint_lower`).
7. §8, last paragraph ("`c ≈ 0.15–0.25`, between `c = ½` and `c ≈ 0`"): pair-specific; for `(1 − √e)₊³`
   the offset of the true sequence is `≈ −0.28` (approach from above).
8. §9, heuristic for `p = 1`: "geometric or faster" (finite termination for `θ = (1 − 2e)₊`); the
   rate of the lower bound is explicit, `exp(−k/[1/ln(1/λ₋) + 1/ln λ₊])`.
9. §10: the closed form can be marked [P] (conjugation written out above) and simplifies to
   `B_∞(k) = 1/(4cos²(π/(2k + 1)))`.
10. `rlib.py` docstring: `J(0) = θ(∞)`, not `0` in general.

## Summary table of verdicts

| statement | verdict |
|---|---|
| §1 properties of `J` (concave, `max J = h`, maximisers) | correct as stated |
| §1 shear, `θ_hint = sup_t [J(t) − tx]`, `θ_hint″(0) = −1/J″(L)` | correct as stated (reading: `θ_hint` defined by the shear) |
| §1 `ϑ = θ″(h)/(1 + r)³` for `C²` | correct as stated |
| §1 consequence (i) | correct as stated |
| §1 consequence (ii) | correct as stated |
| §1 constants of the cube, `u = 1` (and `u = 2`) | correct (all digits printed in the report) |
| (Σ1) | correct as stated |
| (Σ2) | correct as stated |
| (Σ3) | correct after a repair (attainment only for `B < (1 − s)a`); wording, harmless |
| (Σ4) | correct as stated |
| (Σ5) | formula for `D`, (2.1), the cases `B ≥ h`, `Σ(h, L) = L`, `𝓜(h, L) = {h}`: correct; the sentence on fixed points for `B < h`: wrong as stated (two counterexamples), not used |
| (Σ6) | correct as stated; proof complete |
| (Σ7) | correct as stated |
| Gaussian slope map (quotation of Lean) | quoted correctly |
| (P1) | correct as stated (lsc: argument supplied) |
| (P2) | correct as stated |
| (P3) | correct as stated |
| Lemma L (quotation of Lean) | quoted with exactly the hypotheses of `line_le_Rstep` / `line_le_min_Rstep` |
| Proposition A | correct as stated |
| Lemma PT | correct as stated; no gap found |
| Theorem R, lower bound (`liminf k²(τ_k − h) ≥ 2π²h²ϑ`) | correct as stated |
| Proposition K | lower bound correct as stated; "`Θ(1/k)`" needs the one-sentence `HintPair` remark (exposition) |
| Heuristic classification [C] | plausible; lower-bound halves confirmed numerically for `p = 4/3, 3, 1`; for `p = 1` the recursion itself is geometric in my computation ("geometric or faster") |
| §10 formulas | correct as stated; closed form proved here, simplifies to `1/(4cos²(π/(2k + 1)))` |
| Theorem R as a whole (global numerical test, not a proof) | consistent: four pairs with (H1), increments of `(τ_k − h)^{−1/2}` equal `1/c_*` to `≈ 10⁻³` at `k = 40…60` |

**I found no error of substance in §§1–4, 7, 8 (lower bound), 9, 10.**  The two statements that
are wrong or incomplete as written ((Σ3) attainment on the boundary; the fixed-point sentence of
(Σ5)) are expository and nothing in the proof depends on them.

## What was not checked

* §§5–6 and the upper-bound half of §8 (Proposition U, Corollary U′, Lemma T, Proposition C,
  Lemma RC): Referee A's part.  My global test supports the *conclusion* of the upper bound
  numerically (and the stress test shows pairs where `τ_k = B_∞(k)` to `10⁻⁷`), but I did not read
  those proofs.
* The proof of `RateFull.rate_top0` and the claim that it "uses only" the facts listed in §1.
* The Lean files were read, not compiled (`lake` was not run, by instruction); I rely on the
  repository's statement that they build.
* The identification of the recursion with algorithms (theory report §11.18–11.19); finite `n`.
* My iteration of the recursion is floating point on grids, with a non-convex two-parameter
  minimisation that is not guaranteed to find the global minimum (see the accuracy notes and
  the caveat for the kinked pair); it is evidence, not certification.  Levels beyond `k = 61`
  were not computed.
* For pairs outside (H1) (kink, corner, other exponents, one-sided curvatures) only the
  lower-bound side (`B_∞`, passage times) was tested systematically; the recursion itself was
  iterated for the kinked, the chord and the affine pair only.
* §8a (Proposition S), added after the review began: consistency check only.

## How to reproduce

All in `experiments/workstreams/R/review_B/` (Python 3, `numpy`, `mpmath`; every run under five
minutes, memory below 200 MB; nothing outside this directory is written):

    python3 b1_constants.py                      # cube constants from the KL definitions            -> out_b1_constants.txt
    python3 b2_sigma.py                          # (Sigma1)-(Sigma7) on five pairs                    -> out_b2_sigma.txt
    python3 b3_passage.py                        # Lemma PT on six pairs + the proof's inequalities  -> out_b3_passage.txt
    python3 b4_orbits_gauss.py                   # (P1)-(P3); section 10 closed form                 -> out_b4_orbits_gauss.txt
    python3 b5_kink_heuristic.py                 # Proposition K; p = 1, 4/3, 3                       -> out_b5_kink_heuristic.txt
    python3 b6_recursion.py PAIR LEVELS [q] [nphi] [xmin] [chunk]     # the recursion itself          -> out_b6_*.txt
        # PAIR in gauss, cubroot, quad, kink, kinksmooth, chord, lin, cube<u>;  SAVE_LEVELS=2,3,5 saves T_k
    python3 b7_compare.py PAIR out_b6_....txt    # against B_inf(k) and c_*                           -> out_b7_*.txt
    python3 b8_lines_vs_levels.py gauss 2 3 5 10 20 40               # lines of Proposition A below T_k  -> out_b8_lines_gauss.txt
    python3 b9_stress_propA.py                   # tau_k >= B_inf(k) on six unusual functions        -> out_b9_stress_propA.txt
    python3 b10_author_lib.py                    # rlib.py against the definitions                   -> out_b10_author_lib.txt
    python3 b11_H1_not_C2.py                     # (H1) without theta in C^2                         -> out_b11_H1_not_C2.txt
    python3 b12_onesided.py                      # one-sided curvatures (outside (H1))               -> out_b12_onesided.txt
    python3 b13_profile_8a.py                    # section 8a, consistency only                      -> out_b13_profile_8a.txt
    python3 b14_slope_le_one.py                  # tau_k = B_inf(k) when |theta'(0+)| <= 1            -> out_b14_slope_le_one.txt

The runs quoted above: `b6_recursion.py cubroot 61 1.01 160 1e-9 200`, `… cubroot 61 1.005 200 1e-9 200`,
`… cubroot 41 1.01 640 1e-9 60`, `… gauss 61 1.01 160 1e-9 200`, `… quad 61 1.01 160 1e-9 200`,
`… cube2 61 1.01 200 1e-10 100`, `… kink 41 1.0074530 640 1e-9 60` (and the three coarser kink runs),
`… chord 31 1.01 160 1e-9 200`, `… lin 8 1.01 160 1e-9 200`.
