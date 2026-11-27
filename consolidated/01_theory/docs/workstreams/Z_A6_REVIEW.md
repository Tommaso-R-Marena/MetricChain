# Internal review of `Z_ADDENDUM.md` §§A6a, A6b, A9a and of `z6_certified_tops.py`

*Referee: an AI referee (**an internal review, not external peer review**), 2026-11-26/27.  Brief:
`docs/workstreams/Z_A6_review_brief.md`.  Own scripts and their stored outputs:
`experiments/workstreams/Z/review_a6/` (two libraries, eight scripts, fifteen outputs; every script runs with
`python3 -B experiments/workstreams/Z/review_a6/<script>.py`; §8 lists them with run times and peak memory).
No existing file was edited; `lake`, the audit script and state-changing git commands were not run.
Reviewed: the addendum as of commit `07cde81` (532 lines; A6a l. 196–256, A6b l. 257–297, A9a l. 463–518),
`z6_certified_tops.py` (327 lines), Theorem 11.58e of the theory report (l. 6149 ff. at `61461f3`; the coordinator
committed twice while the review ran — neither commit touches the text under review).  This file was written
incrementally; §0 is the authoritative summary.*

## 0. Summary of verdicts

**One statement is wrong as stated (a closed form, for large slopes); everything else is correct as stated or
correct after a repair of wording or of a citation.  The script is a sound certificate; what it prints is not
quite what it certifies (the last printed digit is rounded to nearest).**  I tried to break each statement on
paper and with code that shares nothing with the coordinator's; apart from the closed form none broke.

| statement | verdict |
|---|---|
| **A12(a)** `τ(T) = inf_x a(x + T^♯(x))/(a + x) = τ(T^♯)` | **correct as stated** (one unwritten step: `T^♯` is again nonincreasing and `≥ 0`) |
| **A12(b)** `M^♯ = M`; `M_{env f, b} = M_{f, b}`; `τ(M_{W,b}) = max_B min(B, (1 − W(B))a) = b⁺(W, b)` | **correct as stated**; the restriction "for a pair with infinite slope at zero" is not needed (the identity with `b⁺` holds for every pair) |
| **A12(c)** `θ^♯ = max(θ, a − ·) = M_{W₁, a}`; `τ₂ = b₂` | first sentence **correct as stated in every case** (also for a finite slope at zero, where one sentence of the proof is not literally right); `τ₂ = b₂` **correct after a gap of citation is filled**: it uses `sup T₂ = τ(θ)`, which the quoted place does not prove — Lemma R0 of §1.1 does; true for every pair with (H0) |
| **A12(d)** `τ_{j+1} = τ(T_j^♯) ≤ τ(M_{W_j, b_j}) = b_{j+1}` | **correct as stated**, direction included (the first equality by the same Lemma R0) |
| **the closed form** "for the cube … `τ₂ = b₂ = a²/(a + x*)`" | **wrong as stated**: true exactly for `u ≤ u₀ = 4.65352`, false above (counterexample `u = 5`: `τ₂ = b₂ = 0.602893·a < 0.604053·a = a²/(a + x*)`; `u = 8`: `0.7139·a` against `0.7874·a`).  Right at the slopes of the tables (`u = ½, 1, 2`).  Repair in §1.5 |
| **A13** (multi-rate sequences) | **correct after a repair of wording** (the cap line is below the *maximum* of such lines and the zero line; the reason for "nondecreasing"); "pair with infinite slope at zero" is not needed (the cube is one) |
| **the script as a certificate** | **sound** — every rounding goes in the valid direction, nothing that affects validity is decided in floating point, the hull is the exact upper envelope of the stored doubles.  What it certifies: the theorem of §3.3.  Three caveats: the printed decimals are roundings *to nearest* of the certified doubles (so the 9-digit table of A6b is not, digit for digit, a table of certified bounds; the theory report's table, rounded up, is); mpmath's interval logarithm is not a proved enclosure in its last bit (harmless here: §3.2); "by Lemma A1 and Proposition A8" needs Corollary A4, or the base case re-read |
| **Lemma A9′** | **correct as stated** |
| **Proposition A11′** | **correct as stated** (every constant checked; for the cube at `u = 1, 2`: `r₀ = L`, `g₀ > ε*`, `k₂(g)·g/h = 104.5, 99.3`) |
| **Theorem Z‴** | **correct as stated, conditionally** (as Theorem Z′); the earlier referees' statements on Propositions Z3, Z4 and on §6 of `Z_REPORT.md` cover the use at `x̂ = g·n` with `k ≤ n^{1/2}` |
| closing sentences of A9a; observation A8′ | **correct**; A8′ confirmed at the levels I computed (`k = 2 … 60`, `u = 1, 2`).  One imprecision in A10 (the range) |
| **Theory report, Theorem 11.58e (e)** | says what A6a proves, **except the parenthesis "(for the cube `a²/(a + x*)`, `θ_na(x*) = a − x*`)"**, which is wrong for `u > 4.65352` |
| **(f)** | says what A6b proves; its table is rounded up and is valid; "rounded outwards" should read "rounded downwards" |
| **(g), small rates** | says what A9a proves; "for all `n ≥ n₀`" is missing; "the true number of levels is of order `(h/g)·ln n`" is a numerical statement printed without a label |
| "what it is not" (ii), (vi) | consistent with the addendum ((vi) states the uncovered range better than A10 does) |

**Errors and slips, most serious first** (details and repairs in the sections named).

1. **The closed form of `τ₂` for the cube** (A6a l. 227; theory report 11.58e(e); the comment of harness XVI.11(e)).
   The minimum of `a·max(a, x + θ(x))/(a + x)` is at the kink `x*` only if `|θ′(x*)|·(a + x*) ≤ x*`, i.e. only if
   the top `b₂` lies on the cap line of `W₁`.  For the cube this holds iff `u ≤ u₀ = 4.6535196`; above, `τ₂ = b₂`
   is the root of `B = (1 − Σ(B, 0))·a` on the un-capped curve and is *smaller* than `a²/(a + x*)` (by
   `1.2·10⁻³a, 1.6·10⁻²a, 7.3·10⁻²a, 0.153a` at `u = 5, 6, 8, 12`).  No proof uses the closed form; the numbers
   quoted at `u = ½, 1, 2` are right.  At `u = 5` the coordinator's own script certifies `τ₂ ≤ 0.602893485·a`,
   below the closed form `0.604053203·a`.  (§1.5)
2. **What is printed is not what is certified** (script; table of A6b).  The certified objects are doubles; the
   script prints them with `%.12f` and `%.9f`, i.e. rounded to nearest: in the first eight levels of the
   published run 4 of 8 printed tops and 6 of 8 printed ratios are *below* the double they stand for (the
   certified `c₂/a ≤ 0.50041002444…` is printed `0.500410024`).  A rigorous reading adds one unit in the last
   printed place.  The 6-digit table of the theory report is rounded up and valid as it stands.  (§3.4)
3. **A citation that does not carry the claim** (A12(c), (d)): "theory report §11.19, remark (1): `τ_{k+1} = τ(T_k)`".
   There this is the *definition* of the bounded-accuracy sequence, and the theory report says of the
   recursion only "`sup T_{k+1}` is at most that number" (l. 5144).  The identity for `τ_k = sup T_k` is true;
   a proof is in §1.1 (ten lines), with a brute force on `R` itself.
4. **Two numbers of the table of A6a**: `τ₃ = 0.361189·a` is `5·10⁻⁶a` high (`0.361184·a` by a third independent
   computation, which reproduces the earlier referee's `x* = 1.467642h`); and "`τ(M_{W₂, b₂}) = 0.363303·a`"
   is a discretisation value of a quantity that *equals* `b₃ = 0.3633006502·a` by A12(b) — the table should
   say that its last two rows are the same number.  (§5)
5. **Wording of A13 and superfluous restrictions** (§2): the cap line; "nondecreasing"; "infinite slope at
   zero" (in A12(b), (c) and A13); "by Lemma A1 and Proposition A8" (add Corollary A4, or say "the base
   case of Proposition A8, read for a start on `[0, ā]`").
6. **mpmath's `iv.log` is not a proved enclosure in its last bit** (it rounds an approximation with 20 guard
   bits in the directed way).  Harmless for the lines — the four-ulp rounding of the coefficients leaves a
   proved headroom of one double ulp in `e` and in `ϑ`, some thirteen orders of magnitude more than needed —
   and for `ā` I verified `ā ≥ a` with my own arithmetic at `u = ¼, ½, 1, 2, 3, 5`.  One more `nextafter` in
   `up`/`dn` would make the script independent of it.  (§3.2)
7. Small things.  A10 "between `x̂ ≈ √n` and `n^{2/3}`": the range in which the error term is not shown to be
   `O(n^{1/3}(ln n)^{2/3})` is `n^{1/3}(ln n)^{2/3} ≪ x̂ ≪ n^{2/3}(ln n)^{4/3}` (the theory report (vi) has it right).
   A6b "`3·10⁻⁸` to `2·10⁻³` … (the larger figure at 80 levels)": over the three stored runs the range is
   `2.3·10⁻⁸ … 2.5·10⁻³`, the largest at `j = 78` of `u = 1` (`1.7·10⁻³` at 80) — fine as orders of magnitude.
   The table of A6a quotes the grid value `b₂ = 0.055517524693`, which is `2·10⁻⁹a` *below* `τ₂ = b₂` (the grid
   errs downwards, as A6 says — worth a word next to "equal, as proved").

**What I verified numerically, and how independently.**  Everything below is my own code (`a6lib.py`:
floating point, written from the definitions; `a6exact.py`: interval arithmetic on Python integers with my
own series for `exp` and `log`, exact fractions — no mpmath intervals).  Nothing is imported from `zetalib`,
`rlib`, the harness or the earlier referees' code; the coordinator's script is imported, unchanged, only
where its *output* is the object examined; its stored outputs are read as text.

* A12(a)–(d) on random step functions, random `f`, random convex `W`, and twelve pairs (infinite slope,
  finite slope above one, finite slope below one at zero): 67 checks, no violation; the threshold slope
  `u₀` (also with 40-digit arithmetic, `a6_08`); `sup T₂ = τ(θ)` by brute force on `R` for four pairs.
* **The script's output verified line by line by an independent verifier**: four small instances (`u = 1`:
  `K = 40, 300, 1000`, up to 12 levels; `u = 2`: `K = 200`; 12 906 lines) and **the first eight levels of the
  published run** (`u = 1`, `K = 3000`; 19 040 lines; the tops are those of the stored output, so the entries
  `j = 2, 3, 4, 5, 6, 8` of the table of A6b are covered).  Every line, the cap line included, is exactly
  `[B − ϑ₀(1 − ℓ(B))]/e₀` for a line `ℓ` of the previous level and a rational pair `(e₀, ϑ₀)` that I prove valid
  with my own enclosures; tops, cap values, hull and `M_upper` re-checked exactly; five mutations of the
  output all rejected.  The script's interval pairs and `ā` against my enclosures: 5 478 pairs at six
  slopes, all proved valid.
* **An independent certified sequence** (my own pairs, rates, sample points, rounding, hull): `u = 1` to 40
  levels, `u = 2` to 20, `u = ½` to 10; and a **two-sided floating-point bracket of the envelope tops** (a grid
  sequence that errs downwards, a line sequence that errs upwards; they agree to `10⁻¹⁵a` at `j ≤ 4`).  Both
  certified sequences lie above the bracket at every level compared (also the coordinator's entries at
  `k = 50 … 400`); they agree with each other to `1.5·10⁻³` of `b_j − h`.
* The numbers of A6a (`τ₂`, `b₂`, `b₃`, `τ(M_j) = b_{j+1}` for `j ≤ 12`, `R[θ]` at seven rates, `τ₃`); the tables of
  A6b and of Theorem 11.58e(f) against the stored outputs; Lemma A9′ (chain of inequalities, orbits to 400
  steps), Proposition A11′ (`g₀`, `k₂(g)`, the inequality, and how conservative it is), A8′.

**What I did not check** is listed in §7.

## 1. Proposition A12 (A6a)

Notation: `θ` satisfies (H0) (convex, nonincreasing, `θ(0+) = a < ∞`); `T ≥ 0` nonincreasing on `[0, ∞)`;
`S_T(x) := sup_{0≤y≤x}(y + T(y)) = x + T^♯(x)`.

### 1.1 (a), and the identity it is used with

**(a) is correct as stated.**  With `y = γ/(1 − φ)`, `x = φa/(1 − φ)` the bracket is `(1 − φ)[min(y, x) + T(y)]`;
for `y ≥ x` it is `(1 − φ)(x + T(y)) ≤ (1 − φ)(x + T(x))`; so the supremum over `γ ≥ 0` is `(1 − φ)·S_T(x)`, attained
or not, and `1 − φ = a/(a + x)` maps `φ ∈ (0, 1)` onto `x ∈ (0, ∞)`.  Only "nonincreasing and bounded" is used.
The infimum need not be attained: `T ≡ c < a` gives `a(x + c)/(a + x) ↓ c` as `x → 0`; in general the limits
are `T(0)` at `x → 0` and `a` at `x → ∞`, so `τ(T) ≤ min(T(0), a)`.  *Unwritten step:* to apply the formula to
`T^♯` one needs `T^♯` nonincreasing and `≥ 0`: for `x < x′`, `y + T(y) − x′ ≤ T^♯(x)` both for `y ≤ x` and for
`x < y ≤ x′` (there it is `≤ T(y) ≤ T(x) ≤ T^♯(x)`).  `(T^♯)^♯ = T^♯` because `S_T` is nondecreasing.
Numerically: `a6_01` part A (12 random step functions with jumps, brute force on `inf_φ sup_γ`: agreement
to the grid, `2.5·10⁻⁴a`; `T^♯` nonincreasing, `≥ 0`, idempotent).

**The identity `τ_{k+1} = τ(T_k)`.**  A12(c), (d) use it for `τ_k = sup T_k` (the `τ_k` of Proposition A8 and of
`R_REPORT.md`), and cite "theory report §11.19, remark (1)".  There `τ_{k+1} := inf_φ sup_γ[…]` *defines* the
exponent at bounded accuracy, and the remark after Theorem 11.53 says of the recursion only: "`sup T_{k+1}`
is at most that number".  I found no proof of the equality in the repository's reports.  It is true:

> **Lemma R0.**  Let `θ` satisfy (H0), `T : (0, ∞) → [0, ∞)` be nonincreasing and bounded, `T(0) := T(0+)`.  Then
> `R[T]` is nonincreasing and `sup_g R[T](g) = lim_{g↓0} R[T](g) = τ(T)`.  Hence `sup min(T, R[T]) = τ(T)`, and
> `τ_{k+1} = τ(T_k)` for the level recursion.

*Proof.*  *Monotone:* a pair `(φ, β)` admissible at `g` gives `(φ, β + g′ − g)` at `g′ > g`, with the same outer
term and a smaller range of `γ`.  *`≤`:* `θ ≤ a`, so every bracket of `R[T](g)` is at most the bracket of `τ(T)`
with the same `φ`.  *`≥`:* let `0 < g < ¼`, `0 < φ < 1`, `0 < β < g`, `e = (g − β)/φ`, `μ = φθ(e)`, and `V` the supremum over
`γ ≥ β`.  Evaluating at `γ = max(β, μ)` gives `V ≥ μ` and `V ≥ (1 − φ)·T(max(β, μ)/(1 − φ))`.
(i) `φ ≥ 1 − √g`: `V ≥ μ ≥ (1 − √g)·θ(g/(1 − √g)) → a ≥ τ(T)`.
(ii) `φ ≤ √g`: `max(β, μ) ≤ max(g, a√g)`, so `V ≥ (1 − √g)·T(max(g, a√g)/(1 − √g)) → T(0+) ≥ τ(T)`.
(iii) `√g < φ < 1 − √g`: then `e ≤ √g` and `y₀ := β/(1 − φ) ≤ √g`.  With `x = μ/(1 − φ)`, `x_a = φa/(1 − φ)`:
`V = (1 − φ)·sup_{y≥y₀}[min(y, x) + T(y)] ≥ (1 − φ)·[S_T(x) − (T(0+) − T(√g))]` (if `y₀ ≤ x` the points `y < y₀` contribute
at most `y₀ + T(0+)` to `S_T(x)`; if `y₀ > x` the supremum is `x + T(y₀)` and `S_T(x) ≤ x + T(0+)`), and
`S_T(x) ≥ S_T(x_a) − (x_a − x)` with `(1 − φ)(x_a − x) = φ(a − θ(e)) ≤ a − θ(√g)`.  So
`V ≥ (1 − φ)S_T(x_a) − (a − θ(√g)) − (T(0+) − T(√g)) ≥ τ(T) − o(1)` by (a).
The three bounds are uniform in `(φ, β)`.  Finally `τ(T) ≤ T(0+)`, so `sup min(T, R[T]) = min(T(0+), τ(T)) = τ(T)`.  ∎

Numerically (`a6_01` part E, brute force on `R[θ]` itself over `(φ, β)` at rates `10⁻²a … 10⁻⁶a`): `T₂(g) ≤ τ(θ)`
always and increases to it — like `√g` for the cube (`τ − T₂ = 8.8·10⁻⁴a` at `g = 10⁻⁶a`, `u = 1`), like `g` for
`(1 − 3e)₊` and `e^{−3e}` (`3·10⁻⁶a`).  With the lemma, (c) and (d) are complete; without it they prove
`τ₂ ≤ b₂` for the recursion and the equality for the theory report's bounded-accuracy sequence only.

### 1.2 (b)

**Correct as stated.**  `x + M_{W,b}(x) = max_B[B + (1 − W(B))x]` is nondecreasing: `M^♯ = M`.
*The envelope loses nothing.*  A direct proof that needs no conjugate and no closedness: `env f ≤ f` gives
`M_{env f} ≥ M_f`; and if `c := sup_B(B − x·f(B))`, then `B ↦ (B − c)/x` is an affine — hence convex — minorant of
`f`, so it is below `env f`, i.e. `B − x·env f(B) ≤ c`.  This holds for every `f` and every `x > 0`; at `x = 0` both
sides are `b`.  It also covers the definition of A2, where the value of `env f` at the right end is lowered
to its limit (`M` is a supremum; one end value does not matter).  ("`M`" must be read as a supremum when
`f` is not lower semicontinuous.)  Numerically: 200 random `f`, difference exactly zero.
*The minimax step.*  `G(φ, B) = (1 − φ)B + (1 − W(B))φa` is affine in `φ ∈ (0, 1)`, concave and continuous in
`B ∈ [0, b]` (`W` convex and continuous): Sion's theorem (compactness on the side of the maximum only; the
open range of `φ` is no obstacle) gives `inf_φ max_B = max_B inf_φ`, and `inf_{0<φ<1}` of an affine function is
the smaller end value.  Right.  Numerically: ten random convex `W`, brute force on the definition of `τ`.
*The identification with `b⁺`.*  `ψ(B) := B + aW(B) − a` is continuous and strictly increasing with `ψ(0) < 0`;
`max_B min(B, (1 − W(B))a)` is `b` if `ψ(b) ≤ 0` and the root of `ψ` otherwise; and `sup{ψ < 0} = sup{ψ ≤ 0}`.
Since `Σ(B, s) < ∞` for `B < (1 − s)a` and `= ∞` for `B > (1 − s)a` whatever the slope at zero,
**`b⁺(W, b) = max_B min(B, (1 − W(B))a)` for every pair** — the words "for a pair with infinite slope at zero"
can go (by hand: `θ = (1 − 0.8e)₊`, `W₁ = 0.8B`, both sides `1/1.8`).

### 1.3 (c)

**The first sentence is correct in every case.**  `y + θ(y)` is convex with the value `a` at `0`: its supremum
over `[0, x]` is `max(a, x + θ(x))`.  For `M_{W₁, a} = M_{f, a}`, `f = min(1, Σ(·, 0))` on `[0, a]` (`b₁ = a`), let
`r₀ := |θ′(0+)| = Σ(a, 0) ∈ (0, ∞]`.
* `r₀ ≤ 1`: `f = Σ(·, 0)`, `M_{f, a} = θ` (envelope of tangent lines), and `max(θ, a − ·) = θ` because
  `θ(x) ≥ a − r₀x`.  (Here the proof's "the others give `sup B − x = a − x`" is not literally right — there are
  no others — but `a − x ≤ θ(x)`, so the conclusion stands.)
* `r₀ > 1` (finite or not): `Σ(·, 0) > 1` on a nonempty interval `(B₁, a]`, where the lines `B − x` have the
  supremum `a − x`; the lines with `Σ(B, 0) ≤ 1` are below `θ`; and where `θ(x) > a − x` a supporting line of
  `θ` at `x` has intercept `B_x ≤ a` and slope `λ_x ≤ (a − θ(x))/x < 1`, so it is one of them.  Hence
  `M_{f, a} = max(θ, a − ·)`.

Numerically (`a6_01` part C; `W₁` computed from the definition as the lower hull of `min(1, Σ(B, 0))` on a
grid): the cube at `u = ½, 1, 2, 6, 8`, the Gaussian pair, `(1 − √e)₊³`, `(1 − 0.8e)₊`, `(1 − 3e)₊`, `e^{−3e}`, `0.3e^{−e}`,
`(1 − e)₊²` — `max|M_{W₁,a} − θ^♯| ≤ 8·10⁻⁵a` and `|τ₂ − b₂| ≤ 6·10⁻⁶a` in all twelve (the accuracy of these generic
grids; for the cube the equality is checked to `10⁻¹⁶` in `a6_04`).
**`τ₂ = b₂`** follows by `τ₂ = τ(θ)` (Lemma R0) `= τ(θ^♯)` (a) `= τ(M_{W₁, a})` (c) `= b⁺(W₁, a)` (b) — **for every
pair with (H0)**, not only for an infinite slope at zero.

### 1.4 (d)

**Correct as stated.**  `T_j ≤ M_{W_j, b_j}` on `(0, ∞)` and `T_j(0) = τ_j ≤ b_j = M_{W_j, b_j}(0)`; `τ` and `♯` are monotone;
the direction is `τ_{j+1} ≤ b_{j+1}`, with equality if `T_j^♯ = M_{W_j, b_j}`.  (`τ_{j+1} = τ(T_j)`: Lemma R0.)

### 1.5 The closed form `τ₂ = a²/(a + x*)` — wrong for large slopes

`Q(x) := a·max(a, x + θ(x))/(a + x)` is `a²/(a + x)` (decreasing) on `[0, x*]`; beyond `x*` it is
`a(x + θ(x))/(a + x)`, whose derivative has the sign of `a(1 − λ_x) − B_x` (`λ_x = |θ′(x)|`, `B_x = θ(x) + λ_x x` the
intercept of the tangent line at `x`).  At `x*`, `B_{x*} = a − (1 − λ*)x*`, so
`Q′(x*+) ≥ 0  ⟺  λ* := |θ′(x*)| ≤ x*/(a + x*)`.  If this fails, the minimum is at an interior point beyond
`x*` — the tangent line with `B = (1 − λ)a`, i.e. the root of `B = (1 − Σ(B, 0))a` — and `τ₂ = b₂ < a²/(a + x*)`.
In terms of the curve: the cap line of `W₁` is the pencil of lines through the kink `(x*, a − x*)`, its slope
is `1/x*`, it touches `Σ(·, 0)` at `B_t(1) = a − (1 − λ*)x*`, and `a²/(a + x*)` is the root of `B = (1 − W₁(B))a`
*on the cap line*; the closed form holds iff that root is above `B_t(1)` — the same condition.

| `u` | `½` | `1` | `2` | `4` | `4.5` | **`5`** | **`6`** | **`8`** | **`12`** |
|---|---|---|---|---|---|---|---|---|---|
| `λ*` | `0.0103` | `0.0397` | `0.1378` | `0.3568` | `0.4014` | `0.4412` | `0.5079` | `0.6037` | `0.7150` |
| `x*/(a + x*)` | `0.49997` | `0.49959` | `0.49439` | `0.44411` | `0.42171` | `0.39595` | `0.33706` | `0.21256` | `0.05456` |
| `a²/(a + x*)`, in units of `a` | `0.500026736` | `0.500410018` | `0.505615442` | `0.555890847` | `0.578293905` | `0.604053203` | `0.662940062` | `0.787442884` | `0.945438646` |
| `τ₂ = b₂`, in units of `a` | `0.500026736` | `0.500410018` | `0.505615442` | `0.555890847` | `0.578293905` | **`0.602893472`** | **`0.646969826`** | **`0.713948380`** | **`0.792102221`** |

(`a6_01` part D; `τ₂` by direct minimisation of `Q`; `b₂` from the curve; the two agree to `2·10⁻⁹a` at every
slope.)  The threshold is `u₀ = 4.6535196` (bisection in double precision in `a6_01` and in 40-digit arithmetic
in `a6_08`, which shares no code with it and reproduces the whole table); there
`τ₂ = 0.585873·a`.  At `u = 8` the brute force on `R` itself gives `T₂(10⁻⁶a) = 0.71382·a`, increasing to
`0.71395·a` and nowhere near `0.78744·a`.  **At `u = 5` the coordinator's own certificate refutes the closed
form:** `z6_certified_tops.py` run at `u = 5` (two levels, `K = 2000`) certifies `τ₂ ≤ c₂ = 0.602893485·a`, and so
does my independent sequence (`0.602893485·a`) — `1.2·10⁻³a` below `a²/(a + x*) = 0.604053203·a` (`a6_07` (3)).  For small slopes the cube tends to the Gaussian pair (`x* → a`,
`λ* → 0`, `τ₂ → a/2`).
*Repair.*  "For the cube `x + θ(x) − a` changes sign once, at `x* > 0`, and `τ₂ = b₂ = min_x a·max(a, x + θ(x))/(a + x)`;
this is `a²/(a + x*)` when `|θ′(x*)|(a + x*) ≤ x*` — for the cube exactly when `u ≤ 4.6535` — and otherwise the
root of `B = (1 − Σ(B, 0))·a`, which is smaller."  The same in Theorem 11.58e(e) and in the comment of
harness XVI.11(e) (which tests `u = 1, 2` only).  The expression
`min_φ max{(1 − φ)a, φa + (1 − φ)θ_na(φa/(1 − φ))}` of §11.19 is the general formula and is right at every slope.
The earlier referee's `τ₃ = a·τ₂/(a + x₂*)` has the same proviso; at `u = 1` I checked that the kink is the
minimiser (§5).

### 1.6 The paragraphs after the proposition

"From the third level on …" is labelled [N] and is what the numbers show at `k = 3` (§5); for `k = 4, 5, 6` it
rests on three-digit values of the theory report that I did not recompute.  "Where the loss is": the quoted
numbers are those of `out_z7_exactness_u1.txt` (`a6_06` (4)); `M₂(g) = b₂ − g` up to `1/m₂ = 0.3486ε*` and
`T₂^♯(g) = τ₂ − g` up to `x₂* = 0.3560ε*` — the second level stays on the line `τ₂ − g` a little longer than its
majorant, which is the whole of `b₃ − τ₃`.  The last sentence ("the exact solution of the recursion restricted
to families handed down as convex sets of lines with the inner tolerance zero") is an interpretation; what
is proved is A12(b): the *top* of the next family is exactly the value of the level formula on the majorant.

## 2. Proposition A13 (A6b)

**Correct after a repair of wording.**

* *The inequality.*  `Σ(B, s) ≥ [B − (1 − s)θ(e_m)]/e_m ≥ [B − (1 − s)ϑ_m]/e_m` needs `e_m > 0` and `s ≤ 1` (so that
  `(1 − s)(ϑ_m − θ(e_m)) ≥ 0`); the right side is nondecreasing in `s` for every real `s` because `ϑ_m ≥ 0`; with
  `s = V(B) ≤ 1` and `ℓ_i ≤ V` this is the claim on `[0, c]`.  A line `ℓ_i` may be negative, or above one beyond
  `c`; neither matters.  What matters is `V ≤ 1` on `[0, c]` — *this* is where "a line steeper than the cap"
  would break the argument (the factor `1 − s` must not change sign), and it is excluded by "`(V, c)` is
  a family"; the script enforces it exactly (lines with value above one at `c` are dropped before the cap
  is added, and `V(c) ≤ 1` is asserted in fractions).
* *(S1), literally.*  `c ≥ c′` is assumed.  If `c′ = c` there is nothing to prove.  Otherwise: `Σ(B, V(B)) < ∞`
  forces `B ≤ (1 − V(B))a ≤ (1 − V(B))ā`, i.e. `B + āV(B) ≤ ā ≤ c′ + āV(c′)`, and `B ↦ B + āV(B)` is *strictly*
  increasing (`V` nondecreasing): `B ≤ c′`.  So `c′ ≥ b⁺(V, c)`.  Right, for every pair.  (`c′ > 0` is automatic.)
* *(S2), literally.*  Each line of `V′` is below a lower bound of `Σ(·, V(·))` on `[0, c′] ⊂ [0, c]`, and `0 ≤ Σ`.
* *`V′` is a family.*  Convex, continuous: a maximum of lines.  `V′(0) = 0`: every such line is `−ϑ_m(1 − ℓ_i(0))/e_m ≤ 0`
  at zero because `ℓ_i(0) ≤ V(0) = 0`, and lines below them too.  *Nondecreasing:* the reason given — "the slopes
  `(1 + ϑ_mα_i)/e_m` are positive" — covers the such-lines generated from lines with `α_i ≥ 0`, not "lines that
  are below such lines"; the right reason is that a convex function that is `≥ 0` and vanishes at the left
  end is nondecreasing (as in Lemma A3).  Values in `[0, 1]` on `[0, c′]`: `V′(c′) ≤ 1` and monotone.
* *Wording of the hypothesis.*  "`V′` is a maximum of the zero line and of lines that are below such lines on
  `[0, c′]`" should read "… of lines each of which is, on `[0, c′]`, below the *maximum* of the zero line and
  of such lines".  The cap line — the tangent from `(c′, 1)` to the hull of the such-lines — is below that
  maximum; it is below one single such-line only when its point of contact lies between two lines
  generated from the same line of `V` (then it *is* a such-line for a slightly larger pair: with
  `r = B/(1 − ℓ(B))` the such-lines are `(1 − ℓ(B))` times the tangent lines `(r − θ(e))/e` of the convex function
  `Σ(r, 0)`, and a line through the crossing of two tangents with an intermediate slope is below the
  function).  In all the script's outputs that I verified this was the case — every cap line had a
  single-line certificate (§3.5) — but the proposition should not depend on it.
* *"Pair with infinite slope at zero"* is not needed anywhere in the statement or the proof ((S1) uses
  `Σ = ∞` beyond `B = (1 − s)a`, true for every pair).  The cube is such a pair:
  `θ(e) = a − u·√(2p_u(1 − p_u)e)·(1 + o(1))`.
* *What the proposition is used for* — "its tops are upper bounds of `τ_j`": see §3.3 for the exact chain.

## 3. The script `z6_certified_tops.py` as a certificate

### 3.1 Line by line

| step | what must hold | what the script does | verdict |
|---|---|---|---|
| `up(x)`, `dn(x)` | a double `≥ x.b` / `≤ x.a` | `float(x.b)` — in mpmath 1.3.0 an interval end is converted by *truncation towards zero* (`round_fast`), error below one ulp — then one `nextafter` outwards | valid in all four sign cases; the slack is in `(0, 1]` ulp and can be arbitrarily small |
| `A_IV`, `ABAR`, `ALOW` | `ā ≥ a ≥ ALOW` | interval evaluation of `KL(p_u‖½)` with `p_u = 1/(1 + e^u)` an interval | valid given the interval functions (§3.2); verified independently at six slopes (slack `0.13 … 0.84` ulp) |
| `certified_pair(ρ)` | `ϑ ≥ θ(e′)` for the **rounded** `e′` | `e′ = up(KL(ρ‖p_u))`, `ϑ = max(0, up(KL(ρ‖½)))`; `ρ ≥ ½`: `(up(ε*), 0)` | valid: `e′ ≥ KL(ρ‖p_u)` and `θ` nonincreasing give `θ(e′) ≤ θ(KL(ρ‖p_u)) = KL(ρ‖½) ≤ ϑ`.  Rounding `e` **up** is the valid direction, and it is the one taken.  The assertion `e.a > 0` does not check `ρ > p_u`, but a `ρ < p_u` would give a valid (useless) pair too: `KL(ρ‖½) > a ≥ θ` |
| `step`: the line | stored line `≤ [B − ϑ(1 − ℓ(B))]/e′` on `B ≥ 0` | slope `(1 + ϑa₀)/e′` four ulps down, `β = ϑ(1 + b₀)/e′` four ulps up | valid: three correctly rounded operations give a relative error below `(1 + 2⁻⁵³)³ − 1`, four steps of `nextafter` move by a factor `(1 ∓ 2⁻⁵³)⁴` at least.  `ℓ = (a₀, b₀)` is whatever line the floating-point `argmax` returned, or the zero line: any of them is admissible |
| `_hull` | the stored arrays are the upper envelope of zero and the lines on `[0, c]` | sorting, equal slopes merged (smaller `β` kept), the classical stack with the test `(b₃ − b₁)(a₂ − a₁) ≤ (b₂ − b₁)(a₃ − a₁)` in fractions; lines activated beyond `c` dropped | exact; the zero line is never popped.  Needed for validity through `vertices()` (cap, `M_upper`), not for the lines themselves.  My exact hull of the stored lines returns the stored list at every level examined |
| the cap | a line through `(c, ≤ 1)` below the curve on `[0, c]`; no kept line above one at `c` | `m* = max` over the exact vertices of `(1 − V)/(c − X)` (the supremum of the chord slope: on each linear piece it is monotone, and it tends to `−∞` at `c`); `m` rounded **up**, `β_L = m·c − 1` rounded **up**; lines with value `> 1` at `c` dropped; `H(c) ≤ 1` asserted exactly | valid (a steeper line through `(c, 1)` is lower on `[0, c]`; `m > 0`, `β_L ≥ 0` because `m* ≥ 1/c`) |
| `next_top` | `c′ = c`, or `c′ + āV(c′) ≥ ā` exactly | exact test at `c`; floating-point bisection; then the **exact** test in fractions, stepping up by `nextafter` until it holds; `min(c′, c)` | valid; the floating-point part only proposes |
| `M_upper(g)` | a double `≥ max_B(B − V(B)g)` | exact maximum over the exact vertices (the function is concave piecewise linear), rounded up | valid for the double `g` that is passed (the printed columns are at the doubles `0.1·h`, `0.5·h`, `h` with a floating-point `h`: "at `g = 0.1h`" is exact to `10⁻¹¹` only — immaterial, `M` is 1-Lipschitz) |
| `main` | — | prints; `mono`, `above` and "ALL CHECKS PASS" compare doubles, the second with an uncertified `h` | not part of the certificate (the docstring says so for `h`, `c_*²`) |

**Nothing that affects validity is decided in floating point**: the sample points, `V.val` (values and the
index of the line), the filters `keep`/`good`, the golden-section search and the bisection of `next_top`
choose *which* valid line or *which* candidate top is tried; every stored line is valid whatever they
return, and the top is accepted only by the exact test.

### 3.2 The interval arithmetic

mpmath's `iv` arithmetic rounds `+ − × ÷` outwards exactly.  Its `iv.log` is `mpf_log(·, prec, round_floor/ceiling)`,
and `mpf_log` computes a fixed-point *approximation* with `prec + 20` bits and rounds *that* in the directed
way (I read `libelefun.mpf_log`): the result is a correct enclosure unless the true value lies within
about `2⁻²⁰` units of the last place of a 30-digit number — a proof-grade statement it is not.  For the
script this is harmless, for a reason worth recording:

* *the lines.*  The stored line determines a unique rational pair `(e₀, ϑ₀)` with
  `stored line ≡ [B − ϑ₀(1 − ℓ(B))]/e₀`, and by the four-ulp rounding `e₀ ≥ e′(1 + 2⁻⁵³)`, `ϑ₀ ≥ ϑ′(1 + 2⁻⁵³)²` (up
  to factors `1 − 2⁻¹⁰⁶`).  So the stored line is valid as soon as `ϑ′(1 + 2⁻⁵²) ≥ θ(e′)`: an error of the
  interval arithmetic of *any* size below `10⁻¹⁶` relative is absorbed.  This is exactly what my verifier
  measures: the witness windows have width `7·10⁻¹⁷` in `ρ`.
* *`ā`.*  Here there is no such headroom (`ā` is used as it is); I verified `Fraction(ABAR) ≥ a` with my own
  enclosure (width `10⁻⁵⁸`) at `u = ¼, ½, 1, 2, 3, 5` (`a6_07`).  Also 5 478 pairs of `certified_pair` at these
  slopes — random `ρ`, `ρ` next to `p_u` (the script's lower end `w = 10⁻⁶`) and next to `½`, `ρ = ½` — satisfy
  `e′ ≥ KL(ρ‖p_u)` and `ϑ ≥ KL(ρ‖½)` by my enclosures, with slacks down to `4·10⁻⁵` ulp.  (Next to `p_u` the
  script's `e′` is up to `2·10⁻⁵` relatively too large — the dependency problem of interval arithmetic at
  30 digits; valid, and immaterial for the quality.)

*A hardening that costs nothing:* a second `nextafter` in `up` and `dn` makes the certificate independent
of the last bits of mpmath.

### 3.3 What exactly is certified

> **Theorem (the certificate).**  Let `u` be the decimal number given to the script, `θ = θ_na` of the cube at
> slope `u`, `a = θ(0+)`, and `(T_j)` the level recursion (`T₁ = θ`, `T_{j+1} = min(T_j, R[T_j])`, `τ_j = sup T_j`).
> Suppose the script ends without an exception, and let `c_j` (doubles) and `V_j = max(0, stored lines)` on
> `[0, c_j]` be what it computed, `c₀ = ā`, `V₀ ≡ 0`.  Then
> (i) `(V_j, c_j)_{0 ≤ j ≤ J}` is admissible in the sense of A1: families; (S1); (S2).
> (ii) `T_j(g) ≤ M_{V_j, c_j}(g)` for every `j ≥ 1` and `g > 0`; in particular `τ_j ≤ c_j`, and `T_j(g) ≤ M_upper(g)` for every
> double `g ≥ 0`.
> (iii) `c_j ≥ b_j` (the envelope tops), so Theorem Z′ holds with `c_k` in place of `b_k`.
>
> *Hypotheses.*  For (i): Proposition A13 (§2); exact integer and fraction arithmetic, IEEE double arithmetic
> with rounding to nearest, `nextafter`; the interval functions of mpmath correct to a relative `10⁻¹⁶` for
> the pairs, and `ā ≥ a` (verified independently at `u = ¼, ½, 1, 2, 3, 5`).  For (ii): (i), the exponent-level
> clause of Lemma A1 — i.e. Proposition U and Corollary U′ of `R_REPORT.md` (paper proofs with Sion's theorem
> and the machine-checked Lemma M; refereed twice; not re-derived here) — and the base case
> `θ(x) = sup{B − Σ(B, 0)x : B < a} ≤ M_{V₁, c₁}(x)`, which needs `c₁ ≥ a` (here `c₁ = ā`) and `V₁ ≤ Σ(·, 0)` on `[0, c₁]`.
> For (iii): Corollary A4 (`b₀ = a ≤ ā = c₀`, `W₀ = V₀ = 0`).
>
> *Not certified:* `h`, `c_*²`, the comparison columns, the line "ALL CHECKS PASS", the closeness of the
> bounds to the truth; and the *printed decimals* only up to one unit of their last place (§3.4).

*On the citation.*  A6b says "by Lemma A1 and Proposition A8".  Proposition A8 is a statement about the
envelope sequence from `b₀ = a`; for the script's sequence one needs either its *proof* (the base case
above, which goes through verbatim for any admissible sequence from a flat start on `[0, c₀]`, `c₀ ≥ a`) or
Corollary A4 (`T_j ≤ M_{W_j, b_j} ≤ M_{V_j, c_j}`).  The docstring of the script states the right theorem.

### 3.4 What is printed

The certified numbers are the doubles `c_j` and `nextafter(c_j/ALOW)`.  The script prints them with `%.12f`
and `%.9f` — rounded to nearest.  In a re-run of the published instance (`u = 1`, `K = 3000`; `a6_06` (3), which
reproduces the stored tops, ratios and numbers of lines for `j ≤ 8`):

| `j` | certified ratio (double) | printed | printed below the double? |
|---|---|---|---|
| 2 | `0.50041002444165616` | `0.500410024` | yes, by `4.4·10⁻¹⁰` |
| 3 | `0.36330065318179994` | `0.363300653` | yes |
| 4 | `0.31279146158214088` | `0.312791462` | no |
| 6 | `0.28132325010092901` | `0.281323250` | yes |

— 6 of 8 ratios and 4 of 8 tops are printed below the double.  So the row "certified `c_j/a ≥ τ_j/a`" of the
table of A6b is, digit for digit, not a row of certified upper bounds; each entry `+ 10⁻⁹` is.  (That the
printed values are above `τ_j/a` is true at `j = 2` by the closed form, and no doubt at every `j`; but that
is not what "certified" means.)  The table of Theorem 11.58e(f) rounds up to six digits, and every entry
is at least `5·10⁻¹⁰` above the printed ratio (`a6_06` (1)): valid as it stands.  *Repair:* print with a
directed rounding, or say "add one unit in the last place".

### 3.5 Independent check of outputs (`a6_02_verify_z6_output.py`, `a6_07_pairs.py`)

The script is imported unchanged, its own `step` is run, and the curves it returns are verified by code
that shares nothing with it.  For each level `V → V′`:
(T) the top, in fractions; (F) slopes `> 0`, `β ≥ 0`, `V′(c′) ≤ 1`, stored lines = exact hull;
(L) for every line `(α, β)` of `V′`: a line `ℓ = (a₀, b₀)` of `V` (or the zero line) is found for which the
rational pair `e₀ = 1/(α − βa₀/(1 + b₀))`, `ϑ₀ = βe₀/(1 + b₀)` — it reproduces the line identically — is **proved**
valid by a rational witness `ρ` with `KL(ρ‖p_u) ≤ e₀` and `KL(ρ‖½) ≤ ϑ₀` (my enclosures; `ρ` is located with
60-digit floating point, which proves nothing by itself);
(C) a line without such a certificate would be checked against the maximum of the certified lines and of
lines of my own making, at every vertex — this branch was needed only for the mutations;
(M) `M_upper` equals the least double above my exact maximum.

| instance | levels | lines | result |
|---|---|---|---|
| `u = 1`, `K = 300` | 6 | 1 287 | all certified, cap lines included; tops and hull exact; 5 mutations rejected |
| `u = 1`, `K = 40` | 10 | 339 | the same (coarse sampling: `c₁₀ = 0.2713a`, a valid bound all the same) |
| `u = 2`, `K = 200` | 5 | 731 | the same |
| `u = 1`, `K = 1000` | 12 | 10 549 | the same |
| `u = 1`, `K = 3000` — **the published run**, levels 1–8 | 8 | 19 040 | all certified; tops `0.0555175256169059, 0.040306053704987, …, 0.0302600726830818` = the stored ones (mutations not repeated) |

Mutations (each rejected): a line raised by `10⁻⁹` in `β`; a slope raised by `10⁻⁹`; the top lowered by `10⁻⁹`;
the cap line made flatter by `10⁻³` through `(c′, 1)`; an `ā` below `a`.
This shows that *these outputs* are admissible multi-rate sequences; it is not a proof of the script on
every input.  Beyond level 8 of the `u = 1` run, and for the runs at `u = 2, ½` and to 400 levels, I have the
comparisons of §3.6 only.

### 3.6 Independent re-implementation (`a6_03_own_certified.py`)

My own certified sequence — pairs from my enclosures, rates from the closed form of the slope map through
`J` (the script: golden section), exact directed rounding of the coefficients (the script: four ulps), own
sample points with a second pass around the point where the cap line leaves the curve, own hull, cap and
top — against the coordinator's stored tops and against a two-sided floating-point bracket `[grid, lines]`
of the envelope tops (`K = 20 000`, refined), `u = 1`:

| `j` | 2 | 3 | 4 | 6 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|---|
| bracket of `b_j/a` | `0.5004100181` | `0.3633006502` | `0.3127914479` | `0.28132304(09…24)` | `0.26906489(17…81)` | `0.2642436(470…649)` | `0.2630466(521…643)` |
| referee's certified `c_j/a ≤` (exact ceiling) | `0.5004100182` | `0.3633006503` | `0.3127914480` | `0.2813231757` | `0.2690662543` | `0.2642448538` | `0.2630470197` |
| coordinator's certified (as printed) | `0.500410024` | `0.363300653` | `0.312791462` | `0.281323250` | `0.269065250` | `0.264243938` | `0.263047017` |

All tops of both certified sequences are above the lower end of the bracket at every level (`u = 1`: 40
levels; `u = 2`: 20; `u = ½`: 10), as Corollary A4 requires; the two agree to within `1.5·10⁻³` of `b_j − h`
(mine are the smaller ones at the first levels, the coordinator's — with twice the sample points — later);
`c₂ ≥ τ₂` with `(c₂ − τ₂)/a = 1.2·10⁻¹¹` (mine), `6.3·10⁻⁹` (coordinator's).  Far out (`a6_05`, bracket with
`K = 6 000` to 450 levels): the coordinator's certified `k²(c_k − h)/c_*² = 0.99759, 0.99897, 0.99970, 1.00017,
1.00091` at `k = 50, 100, 200, 300, 400` against my brackets of the envelope value `[0.99704, 0.99743]`,
`[0.99791, 0.99874]`, `[0.99824, 0.99936]`, `[0.99806, 0.99979]`, `[0.99623, 0.99977]` — above, as required.

## 4. A9a: Lemma A9′, Proposition A11′, Theorem Z‴

### 4.1 Lemma A9′ — correct as stated

* *`r₀`, `η₀`.*  (H1) gives `J(t) ≤ h − (L − t)²/(2ϑ) + (L − t)²/(4ϑ)` near `L`: `r₀` exists (take `r₀ < L`);
  `η₀ = h − J(L − r₀) ∈ (0, h)`; `η ≤ η₀ ⟹ t₁(h − η) ≥ L − r₀` (`J` increasing on `[0, L]`) `⟹ η ≥ (L − t₁(h − η))²/(4ϑ)`.
* *Monotonicity.*  `t₁` is increasing in `B`, `J′` is nonincreasing in `t` (concave): `B ≤ h − η ⟹ J′(t₁(B)) ≥ J′(t₁(h − η))`.
  Right way round.
* *The chord.*  `J(L) ≤ J(t) + J′(t)(L − t)` for concave `J`: `J′(t₁(h − η)) ≥ η/(L − t₁(h − η)) ≥ η/(2√(ϑη)) = ½√(η/ϑ)`.
* *How the bound enters.*  What the proof of Lemma A9 delivers is
  `1 − κ = J′/(B + (1 − t₁)J′) ≥ x/(B + (1 − t₁)x) ≥ x/(h + x)` for any `x ≤ J′(t₁(B))` (the map `x ↦ x/(B + (1 − t₁)x)`
  is increasing; `B ≤ h`, `1 − t₁ ≤ 1`): with `x = ½√(η/ϑ)`, `κ ≤ h/(h + ½√(η/ϑ)) = μ_η`.  Yes, `κ ≤ μ_η` is what comes out.

Numerically (`a6_05` (A), (B); cube `u = 1, 2`): `J(t) ≤ h − (L − t)²/(4ϑ)` holds on all of `[0, L]` (so `r₀` may be taken
as close to `L` as one likes and `η₀` close to `h`); for eight `η` from `0.9h` to `10⁻⁶h` the chain of inequalities,
`κ(B) ≤ μ_η` for all `B ≤ h − η`, and `0 ≤ t₁ − p_i ≤ t₁μ_η^i` for `i < 400` at 50 intercepts each: no violation.  The lemma
is conservative by the factor `(1 − κ)/(1 − μ) = 1.7 … 2.83`, tending to `2√2` as `η → 0` (the contraction is
`1 − √(2η/ϑ)/h`, the lemma has `1 − √(η/ϑ)/(2h)`).

### 4.2 Proposition A11′ — correct as stated

* `m(g) = ½ϑg² + o(g²)`: from (H1) (lower bound at `t = L − ϑg`; upper bound because the maximiser tends to `L`).
* The constants: `η_g = ϑg²/576` gives `2√(ϑη_g)·g = ϑg²/12 = (ϑg²/4)/3 ≤ m/3`; `½√(η_g/ϑ) = g/48`, so
  `μ_{η_g} = h/(h + g/48) = (1 + g/(48h))^{−1}`; `g ≤ 48h` is used only in Theorem Z‴ (`ln(1 + x) ≥ x/2` on `[0, 1]`).
* `k₂(g)`: both conditions persist for larger `k` (`b_k` nonincreasing); with `C″ = sup_k k²(b_k − h)`,
  `k₂(g) ≤ max{√(576LC″/((1 − L)ϑ)), √(12C″/ϑ)}/g + 1 ≤ C₃/g` on `(0, g₀]`.  `k(η_g) ≤ k₂(g)`, so Lemma A10 gives
  `W_k ≥ p_{k − k(η_g) + 1} ≥ p_{i+1}` on `[0, h − η_g]` for `i = k − k₂(g)` (the `p_j` increase in `j`).
* *Lemma A10's hypothesis.*  `b_k − h < η(1 − L)/L` is the right (sufficient) condition: for `B ≤ h − η` the tangent line
  of `H = Σ(·, W_{k−1}(·))` at `B` has at `b_k` the value `≤ H(h) + (L/η)(b_k − h) < L + (1 − L) = 1`, so the cap line touches
  beyond `h − η`.  Numerically it is far from necessary: `B_t(k) > h` for every `2 ≤ k ≤ 450` (`u = 1`; the earlier
  referee's observation), so that for the cube the second condition alone would do and `k₂(g)·g/h` would be
  `π√24 = 15.4` instead of `104.5`.
* *The two regions.*  `B ≤ h − η_g`: `B − W_k(B)g ≤ B − t₁(B)g + gμ^i ≤ θ_hint(g) + gμ^i` (`t₁ − p_{i+1} ≤ t₁μ^{i+1} ≤ μ^i`).
  `h − η_g ≤ B ≤ b_k`: `B − W_k(B)g ≤ (h − Lg) + (b_k − h) + (L − t₁(h − η_g))g + gμ^i ≤ θ_hint(g) − m + m/3 + m/3 + gμ^i`.
  This is below `θ_hint(g) + gμ^i` "whatever the size of the last term": right — in A11 the geometric term
  had to be `≤ m/3` only because the bound claimed there for these lines was `θ_hint(g)` itself.

Numerically (`a6_05` (C)): for the cube `g₀ = 3.26ε*` (`u = 1`), `2.90ε*` (`u = 2`) — limited by `m ≥ ϑg²/4` beyond `ε*` — so
the proposition covers every rate with `θ_hint > 0`; `k₂(g)·g/h = 106, 105, 104.5, 104.75` at `g = 2h, h, h/2, h/4`
(`u = 1`; `99.5 … 100` at `u = 2`); the tangency points are beyond `h − η_g` from `k₂(g)` on; the inequality holds
for `k₂ ≤ k ≤ k₂ + 25` — trivially: the defect there is below `10⁻⁸` against a bound of order `g`.
*How conservative.*  The true decay per level is `κ_g = 1 − g/(J(t_g) + (1 − t_g)g)` (measured between my two
brackets: `0.360 … 0.367` against `κ_g = 0.36356` at `g = h`); `ln(1/κ_g)/ln(1 + g/(48h)) = 52.7, 49.1, 48.3, 48.1` at
`g = 2h, h, h/2, h/4`.  Levels needed for `n·(M_k(g) − θ_hint(g)) ≤ 1`: `9` computed against `604` from the proof at
`g = h`, `n = 10⁶`; `25` against `2 132` at `g = h/4`, `n = 10⁶` — a factor `49 … 125` over the cases computed, of which
`48` is the rate and the rest the offset `k₂(g)`.

### 4.3 Theorem Z‴ — correct as stated, conditionally

* *The count.*  `k − k₂ ≥ ln(gn)/ln(1 + g/(48h))` gives `n·g·μ^{k−k₂} ≤ 1` (`gn ≥ 1`); `k ≤ C₃/g + 96h·ln(gn)/g + 1 ≤ (C₅/g)·ln n`;
  `k ≤ n^{1/2}` iff `g ≥ C₅ ln n/√n`: that is `C₄`.  Then
  `n·M_{W_k, b_k}(g) + k·c_Z·ln n + C′ ln n ≤ n·θ_hint(g) + 1 + (C₅c_Z/g)(ln n)² + C′ ln n ≤ n·θ_hint(g) + (C/g)(ln n)²`.
* *May the per-level term be used at `x̂ = g·n` with these `k`?*  Yes.  Proposition Z3 gives the type of the level
  family at every `x̂ ≥ 𝒳` (`g = (x̂ − X₀(d))/d` enters through Lemma A1, valid for every `g > 0`, and Lemma Z1a, whose
  constant does not depend on `g`); `E⁺`, `Ê` are constant in the accuracy; for `x ≥ 𝒳` the family `Ẑ` *is* the level
  family (the top chain is not used at all).  This is what the earlier referee wrote for a fixed rate, and
  nothing in it depends on the rate being fixed.  The uniformity in `k ≤ n^{1/2}` is §6 of `Z_REPORT.md` (growth
  of `Λ̄`, orders), refereed in `Z_REVIEW.md` §5 ("`k ≤ n^{1/2}` is enough, with `n₀(u, δ)`").  `x̂ = gn ≥ C₄√n ln n ≥ 𝒳` for
  `n ≥ n₀`.  The constants do not depend on `g` in the stated range.  I did not re-derive the finite-`n`
  statements themselves.
* *The two closing sentences.*  `C(n/x̂)(ln n)² ≤ n^{1/3}(ln n)^{2/3}` from `x̂ = C·n^{2/3}(ln n)^{4/3}` on: right, up to `g₀·n` by
  the theorem (above `g₀·n` there is Theorem Z″ at each fixed rate; uniformity on `[g₀, ε*)` is not written,
  and is routine — `m(g)` is bounded below there — and for the cube at `u = 1, 2` not needed, since `g₀ > ε*`).
  `ln N(n; x̂, δ) ≤ ln N(n; 1, δ) ≤ n·θ_hint(x̂/n) + L·x̂ + O(n^{1/3}(ln n)^{2/3})`: right (`θ_hint(g) ≥ h − Lg`).  The two
  bounds cross at `x̂ ≈ √(C/L)·√n·ln n`, where both are of order `√n·ln n`: right.
* *A8′.*  The duality is right: `M_k ≤ θ_hint + D` on `[0, ∞)` iff `B − D ≤ max_{t ≤ W_k(B)} J(t)` on `[0, b_k]` iff
  `W_k(B) ≥ t₁(B − D)` (with `t₁ = 0` below zero, `t₁(h) = L`).  Numerically (`a6_05` (D); `k = 2, 3, 5, 8, 12, 20, 40, 60`,
  `u = 1, 2`, 6 000 rates up to `5ε*`, both brackets): the defect is largest at accuracy zero; in the dual
  form `sup_B[B − J(min(W_k(B), L))] = b_k − h` is attained at the top only, and on the part of the curve
  below slope `L` it is at most `0.25·(b_k − h)`.  The inequality that the "obvious induction" needs fails
  from `k = 12` (`u = 1`), `k = 11` (`u = 2`) on — "from about ten levels on" (asymptotically from `π² = 9.87`).

## 5. Numbers (own code; floating point unless called certified)

| quantity | addendum | referee |
|---|---|---|
| `τ₂` at `u = 1` | `0.055517524915 = 0.500410018·a` | `0.055517524915 = 0.5004100181·a` (formula of (a), closed form, and both envelope sequences, to `10⁻¹⁶`) |
| `b₂` at `u = 1` | grid `0.055517524693` / certified `0.055517525617` | `0.055517524915` (two-sided); own certified `0.055517524916064` |
| `τ₂ = b₂` at `u = 2`, `½` | (`0.505615446·a`, `0.500026741·a` certified) | `0.5056154420·a`, `0.5000267364·a` |
| `τ(M_{W₂, b₂})` | `0.363303·a` | `0.3633006502·a = b₃` (equal to `2·10⁻¹⁶a`; so for `j = 1 … 12`, `u = 1, 2`) |
| `b₃` | `0.363301·a` | `0.3633006502·a` |
| `R[θ](g)` at seven rates | `out_z7` | reproduced to `3·10⁻⁷a`; mine are never above (a mesh point is an upper bound) |
| `τ₃` | `0.361189·a` | **`0.361184·a`**: first root of `x + T₂(x) = τ₂` at `x* = 1.467642h = 0.356042ε*`; the function increases beyond it, so `τ₃ = a·τ₂/(a + x*)`.  The earlier referee's numbers to all digits |
| `b₃ − τ₃` | `2.1·10⁻³a` | `2.117·10⁻³a` |
| certified tops, `u = 1, 2, ½` | table of A6b | the 30 entries are the printed ratios of the stored outputs; `j ≤ 8` of `u = 1` reproduced by a re-run and verified line by line |
| `h/a` | `0.262647098, 0.296757, 0.253231` | `0.262647098, 0.296757027, 0.253231070` |
| `(c_j − b_j)/(b_j − h)` | "`3·10⁻⁸` to `2·10⁻³`" | `2.3·10⁻⁸ … 2.5·10⁻³` over the three stored runs |

## 6. The theory report, Theorem 11.58e (e)–(g) and "what it is not"

* **(e)** "the level formula at vanishing accuracy sees the family below it only through its slope-capped
  hull …, and the convex envelope loses nothing, so `b_{j+1}` is exactly the value of that formula on
  `M_{W_j, b_j}`; … `τ₂ = b₂`" — what A12 proves (with Lemma R0 if `τ₂` means `sup T₂`; in the theory report's own
  convention, where `τ_{k+1}` is *defined* by the formula, nothing is missing).  **"(for the cube
  `a²/(a + x*)`, `θ_na(x*) = a − x*`)" is wrong for `u > 4.6535`** (§1.5); the theorem is stated for every slope.
  "From the third level on the recursion is strictly better (… at `u = 1` [N])": labelled, and confirmed at
  `k = 3`.  "Both sequences have the same constant in the limit": Proposition A7.
* **(f)** agrees with Proposition A13 and the script.  "the lines are rounded outwards" should read
  "downwards" (slope down, intercept down).  "Given (a) and (e)" is the right conditional.  The table is
  valid (rounded up; checked entry by entry).  The header's "certified exponents of `k` levels" means
  certified *upper bounds* of the exponents of the level recursion.
* **(g), small rates** agrees with Theorem Z‴; the sentence drops "for all `n ≥ n₀(u, δ)`".  "The true number
  of levels is of order `(h/g)·ln n` (… the defect decays like `κ^k` …)" is a numerical observation (the
  earlier referee's, confirmed here) stated without a label; the addendum calls it heuristic.  "the proof
  has `48h` in place of `h`" is right for the rate and omits the offset `k₂(g) ≈ 100h/g`.
* **"What it is not"** (ii) and (vi) say no more than the addendum; (ii)'s "by `0.5`–`0.6` per cent at
  `k = 3, …, 6`" is numerical (I confirm `k = 3`); (vi) states the uncovered range correctly.

## 7. What was not checked

* Proposition U / Corollary U′ of `R_REPORT.md` (the exponent-level step on which every "`τ_j ≤ c_j`" rests): not
  re-derived (two earlier referees did); the certificate is conditional on it, as the texts say.
* The finite-`n` statements behind Theorem Z‴ (Theorem 11.56, Lemma U, Proposition T, Propositions Z3, Z4,
  §6 of `Z_REPORT.md`): statements read for their range in the accuracy and in `k`, proofs not re-derived.
* The script on inputs other than those run.  Of the published runs: levels 1–8 of `u = 1` were re-run and
  verified line by line; the rest (levels 9–80 of `u = 1`, the runs at `u = 2`, `½`, the run to 400 levels) was
  not re-run; its printed tops were compared with my own certified tops and floating-point brackets
  (`u = 1` to `j = 40` and at `k = 50 … 400`, `u = 2` to `20`, `u = ½` to `10`).
* Harness XVI.11 was read, not run.  `z7_exactness.py` and `z8_defect_profile.py` were not re-run (their
  stored outputs were compared with my numbers).
* `τ_k` for `k ≥ 4` (the "0.5 to 0.6 per cent" at `k = 4, 5, 6` rest on three-digit values of the theory report).
* Pairs other than the cube in A9a; slopes other than `u = 1, 2` there.
* Nothing of mine is machine-checked; my "rigorous" arithmetic is rigorous as code is — written once, tested
  against 80-digit values and brute force, not proved.  No Lean file was opened.

## 8. Scripts, outputs, resources; working log

All in `experiments/workstreams/Z/review_a6/`; every stored output ends with "ALL CHECKS PASS" and was
produced by the final version of its script.  Run times and peak memory (maximum resident set of the
process) as measured in the final re-run:

| script → output | what | time, memory |
|---|---|---|
| `a6lib.py` | floating-point library (own derivations of `J`, `θ_na`, `θ_hint`, `t₁`, the slope map by two routes; the envelope sequence on grids and as a line sequence, erring in opposite directions) | — |
| `a6exact.py` | interval arithmetic on integers (200 bits), `exp`, `log`, the two divergences, exact rounding, exact hull, own certified step | — |
| `a6_01_prop_a12.py` → `out_a6_01_prop_a12.txt` | Proposition A12 (a)–(d), the closed form and its threshold, Lemma R0 by brute force on `R` (67 checks) | 217 s, 247 MB |
| `a6_02_verify_z6_output.py [u] [levels] [K]` → `out_a6_02_verify_z6_output.txt` (`1 6 300`), `…_u1_J10_K40.txt`, `…_u2_J5_K200.txt`, `…_u1_J12_K1000.txt`, `…_u1_J8_K3000.txt` (the last with a fourth argument `nocontrols`) | the script's outputs verified line by line; mutations | 22 s, 10 s, 20 s, 97 s, 192 s; ≤ 217 MB |
| `a6_03_own_certified.py [u] [levels] [K] [refine]` → `out_a6_03_own_certified.txt` (`1 40 1500 400`), `…_u2_J20.txt`, `…_u0.5_J10.txt` | independent certified sequence; brackets; comparison with the stored tops | 164 s, 74 s, 33 s; 132 MB |
| `a6_04_numbers.py` → `out_a6_04_numbers.txt` | `τ₂`, `b₂`, `τ(M_j) = b_{j+1}`, `R[θ]`, `τ₃` | 84 s, 268 MB |
| `a6_05_a9a.py [u] [levels]` → `out_a6_05_a9a.txt` (`1 450`), `out_a6_05_a9a_u2.txt` (`2 230`) | Lemma A9′, Proposition A11′, A8′, far tops | 64 s, 34 s; 187 MB |
| `a6_06_tables.py` → `out_a6_06_tables.txt` | tables against stored outputs; printed decimals; quoted numbers of A6a | 6 s, 216 MB |
| `a6_07_pairs.py` → `out_a6_07_pairs.txt` | `ā` and the script's pairs against my enclosures, six slopes; the certified second top at `u = 5` against the closed form | 16 s, < 100 MB |
| `a6_08_threshold_mp.py` → `out_a6_08_threshold_mp.txt` | the closed form of `τ₂` and its threshold slope in 40-digit arithmetic | 1 s |

Rules of the brief, honestly: every run was below five minutes (the longest: 222 s) and far below 1 GB
(the largest: 268 MB); `python3 -B` throughout (no `__pycache__` was written); no existing file was edited
and no state-changing git command was run (`git status`, `log`, `diff`, `show`, `ls-files` only).  Three shell
commands were not prefixed with `cd /home/user/MetricChain &&` as the brief asks — a wrapper in the session's
scratch directory that re-ran my scripts (it changes into the repository itself), a read of its log, and a
wait loop on that log; they touched nothing in the repository.  (A git-ignored
`experiments/__pycache__/falsify_conjectures.cpython-313.pyc` was written at 00:59 UTC while this review ran;
it is not from my runs — no script of mine imports the harness, and all of them ran with `-B`; likewise an
untracked `docs/collaboration/consolidation/` that appeared at 01:05 UTC is not mine.  The only files I
created are this report and the directory `experiments/workstreams/Z/review_a6/`.)  No file I read asked me
to change permissions, spending or scope.

Order of work: paper derivation of A12, A13, the script and A9a before any computation (the closed form
was suspected on paper from the sign of `Q′(x*+)`, then confirmed); libraries with self-tests; `a6_01`;
`a6_02` (small instances), `a6_03`, `a6_04`, `a6_05`, `a6_06`, `a6_07`; then the larger instance and the first
levels of the published run; a full re-run of everything with the final scripts.  One mistake of my own
on the way, recorded because it concerns a number: a first tolerance in `a6_04` treated the coordinator's
`R[θ]` values as exact; they are upper bounds, up to `3·10⁻⁷a` above mine.
