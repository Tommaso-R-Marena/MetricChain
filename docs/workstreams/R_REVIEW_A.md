# Internal review A of `docs/workstreams/R_REPORT.md` — the upper bound (§§5, 6, 8 "Upper bound")

*Referee A (AI, internal review; not external peer review).  2026-11-26.  Scripts and their outputs:
`experiments/workstreams/R/review_A/`.  **Version reviewed:** the report as first committed (`020e990`, 530
lines).  While I worked the report was revised three times (now `9626e4f`, 637 lines); §§5, 6 and the "Upper
bound" paragraph of §8 are textually unchanged, so §§1–7 below apply to the current text; what the revisions
change for this review is in §10.*

## 0. Verdicts

**Summary.**  I found **no error of substance** in Proposition U, Corollary U′, Lemma T, Proposition C, Lemma RC
or the upper-bound half of §8.  Every step was re-derived by hand (notes in §§1–7), and the statements were
attacked numerically with independent code (§8): brute force on the operator `R` itself (no shortcut for the
supremum over `γ`), fifteen functions `θ` (kinks, flat pieces, `θ(∞) > 0`, finite and infinite slope at zero),
random convex `W` of eight shapes, non-convex and non-monotone `W`, the chain of §6 for six pairs, and the recursion
itself against the majorants, pointwise in the accuracy.  What I did find are errors of wording or of
labelling, one false sentence in a remark that the proof does not use, and one overstated numerical claim;
they are listed below, most serious first.

| statement | verdict |
|---|---|
| Lemma M as quoted (§5) | **correct**; the label [V] covers `θ(e) > 0` only — the addendum for `θ(e) = 0` is [P] (two lines, correct); `T ≥ 0` is needed to quote the Lean lemma (1.2, 1.3) |
| Proposition U (§5) | **correct as stated** (§2); moreover `inf_{e>g} F(e) = U(g)` exactly (2.4) |
| Corollary U′ (§5) | **correct as stated** (§3) |
| Remark (1) of §5 (not used in the proof) | **wrong as stated for `θ` with a finite slope at zero; correct after a repair** (finding 1); right for the two pairs of the report (infinite slope) |
| Remark (2) of §5 | **correct** (2.6); the example is an instance with `W(B) = min(1, Σ(B, B))`, nondecreasing, continuous, not convex |
| Lemma T (§6), with the well-definedness paragraph | **correct as stated** (§4) |
| Proposition C (§6) | **correct as stated** (§5) |
| Lemma RC (§6) | **correct**; two routine steps of the "Uniformity" paragraph are not written (6.2 supplies them) — wording |
| Theorem R, upper bound (§8) | **correct as stated**, given Lemma PT, (Σ5)–(Σ7), (P1)–(P3) (Referee B's part, used here as stated) and the a-priori bound, which **is** available under (H0) alone (1.5) |
| Corollary E (§8b of the revised report; added after my brief) | **correct**; one step not written (that `B_∞(k)` is attained and `p_k` is continuous on `[0, B_∞(k)]`, needed for Proposition U) — supplied in §10 |

**Findings, most serious first.**

1. **Remark (1) of §5 is wrong as stated when `θ` has a finite slope at zero** (allowed by (H0)).  It prescribes
   "the lower convex envelope of `min(1, Σ(B, S_k(B)))` on `[0, τ_{k+1}]` with the value one at `τ_{k+1}` …; since
   `Σ(·, S_k(·))` is convex, this is 'cut by the tangent line through `(τ_{k+1}, 1)`'".  This presupposes that
   `Σ(B, S_k(B))` reaches one before `τ_{k+1}`, which is so when `θ′(0+) = −∞` (then `Σ → ∞` at `τ_{k+1}`).  If
   `|θ′(0+)| < ∞`, `Σ` is finite at the boundary point: `Σ(τ_{k+1}, S_k(τ_{k+1})) = (τ_{k+1}/a)·|θ′(0+)|`, possibly `< 1`; the line
   with intercept `τ_{k+1}` then belongs to the bound of Proposition U, Corollary U′ requires
   `W′(τ_{k+1}) ≤ (τ_{k+1}/a)|θ′(0+)|`, and there is no tangent line from `(τ_{k+1}, 1)`.
   *Counterexample* (`a7_remark1_finite_slope.py`): `θ(e) = (1 − 0.8e)₊`, `S_0 = 0`, `τ₁ = a = 1`, `Σ(B, 0) = 0.8B` on `[0, 1]`
   including `B = 1`.  The only line through `(1, 1)` that touches the graph of `0.8B` is the chord from the origin,
   `S₁(B) = B`, which is not below `Σ(·, S_0)`; it gives `M_{S₁,1}(x) = (1 − x)₊ < θ(x) = T₁(x)` for all `0 < x < 1.25` — not a
   majorant.  (Read with a jump at the endpoint — `0.8B` on `[0, 1)`, value one at `1` — the "envelope" gives the right
   `M` but is not continuous, as Corollary U′ requires, and is not a tangent cut.)  *Repair:* "`S_{k+1}` = the lower
   convex envelope of `min(1, Σ(B, S_k(B)))` on `[0, τ_{k+1}]`, with `Σ(τ_{k+1}, S_k(τ_{k+1})) = (τ_{k+1}/a)|θ′(0+)|` at the
   endpoint; when this number is `≥ 1` — always if `θ′(0+) = −∞`: Gaussian pair, cube — it is the cut by the tangent
   line through `(τ_{k+1}, 1)`; otherwise `S_{k+1} = Σ(·, S_k(·))` on `[0, τ_{k+1}]`".  Also "exact" should read "the best
   that Proposition U and Corollary U′ give" (finding 2).  **No consequence for the theorem** (the remark is not
   used; §6 never touches the boundary: `b_0 < (1 − s_t)a`, and Lemma T(b) holds on all of `[0, b_0]`; my chain tests
   include two pairs with finite slope), **and none for the numbers of §11** (both pairs there have infinite
   slope at zero).
2. **"Proposition U holds with equality" (§11, table; `r1_checks.py`: "the bound is attained") is true for
   `inf_e F(e)`, not for `R[T]`.**  The script evaluates only the family `φ = g/e`, `β → 0` (with the `γ`-shortcut),
   which is `inf_e F`; for that quantity equality is a theorem (2.4).  For the operator itself `R[M_{W,b}](g) < U(g)`
   is possible with `T ≥ 0`: Gaussian pair, `W(B) = 2B` on `[0, 0.4]`, `g = 0.45`: `U = 0.0673`, brute force `R = 0.0401`
   (§8, test 1a).  `R[M_{W,b}] = U` holds where `Σ(B, W(B)) ≥ W(B)` at a maximising `B` (by Lemma L).  For the same
   reason the "negative control" of that script proves nothing about `R[T]` (the fact it is meant to illustrate
   is true: 2.6, test 2).  Harmless for the proof; the table entry should be reworded.
3. **Labels.**  (a) The case `θ(e) = 0` of Lemma M is not in Lean (`monotoneS_step` assumes `μ > 0`); it is a correct
   two-line [P] argument.  (b) Proposition U should assume `T ≥ 0` (or "bounded below") if it quotes
   `StepLE.monotoneS_step` through `stepLE_Rstep`.  (c) "`RateFull.rate_top0` [V]" is a theorem about a `HintPair`;
   to use it under (H0) alone one line is missing — the construction of a `HintPair` from an (H0) function
   (`θh(e) = x(e) − e`, `x(e) − θ(x(e)) = e`, `E = h`, `L = 1`; 1.5) — or the remark that the Lean proof uses only
   `h_pos`, `a_pos`, `na_le`, `na_h` and `na_cont` at `h` (I checked that it does).
4. **Lemma RC, "Uniformity".**  Not written: why `σ₁ ≥ L` for `b_0` near `h` (needed before using that `Σ(h, ·)` is
   strictly increasing on `[L, s_t]`), and why the maximisers `e₁` stay in a compact subset of `(0, ∞)` uniformly
   in `j`.  Both are routine (6.2).  The lemma should also repeat `h + ε₁ < (1 − s_t)a`.
5. **Proposition U with `W(0) > 0`** is true but vacuous for `T ≥ 0` (`M_{W,b}` is negative far out).  The
   hypotheses "nondecreasing" and "`W ≤ 1`" are both used and both necessary (test 2; 2.5).
6. **Lemma T(b), proof.**  The sub-case "`j` in case A, `j + 1` in case B" is covered only if one reads `B_t(j) = b_0`
   (then (b) is (a)).  Wording.
7. Outside my part but noticed: (Σ3) ("if `0 < Σ(B, s) < ∞` the supremum is attained") fails on the boundary
   `B = (1 − s)a` when `θ` has a finite slope at zero and is not affine near zero.  Not used on the boundary in
   §§5–8.

## 1. Quotation of the machine-checked lemmas (Lemma M, `Rstep`, `exactRec`)

Read: `proofs/Frontiers/BoundedAccuracy.lean` (`admissible`, `Rstep`, `exactRec`, `exactRec_props`,
`stepLE_exact`), `proofs/Frontiers/HintRecursion.lean` (`StepLE`, `StepLE.of_limit`, `StepLE.of_macro`),
`proofs/Frontiers/LineDynamics.lean` (`line_le_Rstep`, `StepLE.monotoneS_step`, `stepLE_Rstep`),
`proofs/Frontiers/RateFull.lean` (`rate_top0` and what it uses).  Nothing was compiled by me.

1.1 **The operator.**  `Rstep θna T g = sInf {B | ∃ φ β, 0<β<g, 0<φ<1, ∀ γ ≥ β, min γ (φ θna((g−β)/φ)) + (1−φ) T(γ/(1−φ)) ≤ B}`
is the operator `R` of §1 of the report and of (11.18.2).  `exactRec θna k = T_{k+1}`.  **Agrees.**

1.2 **Lemma M.**  `StepLE.monotoneS_step` has the hypotheses: `StepLE θna T T'`; `T` nonincreasing on `(0, ∞)`;
`T ≤ M` and `x + M x` nondecreasing on a range `(0, R]`; `g > 0`, `0 < φ < 1`; `θna` continuous at `g/φ`;
`μ = φ θna(g/φ) > 0`; `X = μ/(1−φ) ≤ R`.  Conclusion `T' g ≤ (1−φ)(X + M X)`.  With `φ = g/e` this is the report's
display.  The report's quotation is **right, with two hypotheses left implicit** (wording, not substance):

* `T' = R[T]` satisfies `StepLE` by `stepLE_Rstep`, which needs `θna ≥ 0` and **`T ≥ 0`** (so that the admissible
  set is bounded below and the real-valued `sInf` is the infimum).  Proposition U is stated for "`T` nonincreasing
  with `T ≤ M_{W,b}`" without `T ≥ 0`.  Mathematically nothing is lost (if the brackets are unbounded below then
  `R[T] = −∞` and the bound is trivial), and every use in the report has `T = T_k ≥ 0`
  (`exactRec_props`); but to *quote the Lean lemma* Proposition U should say "`T ≥ 0`" (or "bounded below").
* continuity of `θ` at `e` — automatic under (H0) (convex on the open half-line); the report says so.

1.3 **The addendum for `θ(e) = 0`** ("the same choice gives `R[T](g) ≤ (1 − g/e)·sup T`") is **not** machine-checked
(the Lean lemma requires `μ > 0`).  It is correct, by a two-line argument which I checked: with `φ = g/e` and any
`β`, every bracket is `≤ μ_β + (1−φ) sup T`, `μ_β = φ θ((g−β)/φ) → φ θ(e) = 0` as `β → 0` (continuity of `θ` at `e`).
The label "[V]" on Lemma M therefore covers only the case `θ(e) > 0`; the case `θ(e) = 0` is [P] (trivial).
In Proposition U it is used with `sup T ≤ sup M_{W,b} = b = S(0)` (needs `W ≥ 0`), which is right.

1.4 **Lemma L** (`line_le_Rstep`): hypotheses `θna ≥ 0`, `0 ≤ σ ≤ σ'`, `B − σx ≤ T x` on `(0,∞)`, `T ≤ C`,
`B − (1−σ)θna(e) ≤ σ' e` for all `e > 0`; conclusion `B − σ' g ≤ Rstep θna T g`.  As quoted in §4.  (Used by me in
§2.6 below, only to explain why the bound of Proposition U is attained.)

1.5 **The a-priori bound** (`RateFull.rate_top0`) is stated for a `HintPair θna θh a h E` with `h < a` and a
sequence with `StepLE θna (T k) (T (k+1))`, `T (k+1) ≤ T k`, every `T k` nonincreasing, `T 0 ≤ a`.  I traced the
fields of `HintPair` that its proof uses (`lemma1_top`, `lemma2`, `epoch_of_stepLE`, `StepLE.of_macro`,
`StepLE.of_limit`): only `h_pos`, `a_pos`, `na_le`, `na_h` and `na_cont` **at the point `h`**.  So the report's
sentence "uses only that the `T_k` are nonincreasing and bounded by `a`, `θ(h) = h`, and the continuity of `θ` at
`h`" is accurate (add: `T_{k+1} ≤ T_k`, `T_{k+1} ≤ R[T_k]`, `0 < h < a`).  Formally, to *apply* the Lean theorem to
a general (H0) function one must exhibit a `HintPair`; this is possible under (H0) alone: let `x(e)` be the root of
`x − θ(x) = e` (the left side is continuous and strictly increasing from `−a` to `∞`), `θh(e) := x(e) − e = θ(x(e))`,
`E := h`.  Then `ident` holds by construction, `e + θh(e) = x(e)` is nondecreasing, and `θh(e) ≥ h − e > 0` on `(0, h)`
because `x(e) ≥ x(0) = h` (`hint_pos`, `hint_lower` with `L = 1`).  **Verdict: the a-priori bound `τ_k → h` is
available under (H0) alone**, as [V] + a three-line [P] construction that the report does not spell out.

## 2. Proposition U

**Verdict: correct as stated** (for `T ≥ 0`, or reading `R[T] = −∞` when the brackets are unbounded below; see 1.2).
I re-derived every step; the notes below record what each step needs, so that the next reader does not have to.

2.1 **`F(e) = max_𝓔 Φ`.**  `(1 − g/e)·[B + (1 − W(B))·gθ(e)/(e − g)] = B − (g/e)[B − (1 − W(B))θ(e)]` — checked.
`Φ(e; B, s)` is nonincreasing in `s` because `θ ≥ 0`, so the maximum over `s ∈ [W(B), 1]` is at `s = W(B)`.
For `θ(e) = 0`: `F(e) = (1 − g/e)·b`, which is the bound of the addendum to Lemma M (1.3), since `sup T ≤ b`.

2.2 **Hypotheses of Sion's theorem** (in the form: `X` compact convex, `f(·, y)` usc quasi-concave on `X`,
`f(x, ·)` lsc quasi-convex on the convex set `Y` ⟹ `max_X inf_Y f = inf_Y max_X f`).
* `X = 𝓔 = {0 ≤ B ≤ b, W(B) ≤ s ≤ 1}`: convex because `W` is convex; closed because `W` is continuous (for a
  convex nondecreasing `W` on `[0, b]` continuity is automatic except for a possible upward jump at `B = b`; that
  is the only place where "continuous" is a real hypothesis); nonempty fibres because `W ≤ 1`.
* `Φ(e; ·)` is affine and continuous on `𝓔`: `Φ = B(1 − g/e) + (g/e)θ(e) − s·(g/e)θ(e)`.  ✓.
* `Y = (g, ∞)`; `Φ(·; B, s)` is continuous (θ is) and quasi-convex: multiplying `Φ ≤ c` by `e > 0` gives
  `g(1 − s)θ(e) + (B − c)e − gB ≤ 0`, a sublevel set of a convex function of `e` (`s ≤ 1`, `θ` convex).  ✓.
  (This is the only place where convexity of `θ` enters Proposition U, and `s ≤ 1` — i.e. `W ≤ 1` — is needed
  here as well as in Lemma M.)
The compact set is on the side of the maximum, as required.  No semicontinuity problem: all functions are finite
and continuous on `𝓔 × (g, ∞)`.

2.3 **The inner infimum.**  `inf_{e>g} Φ = B − g·sup_{e>g} N(e)/e`, `N = B − (1 − s)θ` concave nondecreasing, bounded,
so `N(e)/e → 0` at infinity and `N/e` is quasi-concave on `(0, ∞)`.
* (a), (b): immediate (in (b), `sup_{e>g} N/e = 0` is the limit at infinity).
* (c): I checked the dichotomy in detail.  Suppose `N(x)/x < N(y)/y` for some `g ≤ x < y`.  Quasi-concavity gives
  `N/e ≤ N(x)/x` on `(0, x]`.  Let `M₀ = sup_{[x,∞)} N/e ≥ N(y)/y`.  If `M₀ > 0` it is attained (continuity, limit `0`
  at infinity) at a point `> x ≥ g`, which is then a maximiser over `(0, ∞)`: case (a).  If `M₀ ≤ 0` then `N ≤ 0` on
  `[x, ∞)` and `N/e < 0` on `(0, x]`: case (b).  So in case (c) `N/e` is nonincreasing on `[g, ∞)`, `N(g)/g ≥ lim = 0`,
  and `sup_{e>g} N/e = N(g)/g` by continuity of `N` at `g`.  This covers `Σ(B, s) = ∞` (`B > (1 − s)a`; `s = 1`, `B > 0`)
  and the boundary case `B = (1 − s)a` with a finite slope of `θ` at zero, where `Σ` is finite but not attained.
* `λ := −[(1 − s)θ]′(g+)`: `0 ≤ λ ≤ N(g)/g` from the displayed inequality; the right derivative of a convex function
  is a subgradient, so `B″ − λx` with `B″ = (1 − s)θ(g) + λg` is a global minorant touching at `g`, whence
  `Σ(B″, s) = λ` exactly, `B″ − Σ(B″, s)g = (1 − s)θ(g)`, `0 ≤ B″ ≤ (1 − s)θ(g) + N(g) = B`.  ✓.
  `(B″, s) ∈ 𝓔` uses **`W` nondecreasing** (`W(B″) ≤ W(B) ≤ s`) — the only use of monotonicity of `W`.
* Last line: `Σ(B′, W(B′)) ≤ Σ(B′, s′)` by monotonicity of `Σ` in `s`.  ✓.

2.4 **A remark the report does not make: the bound of Proposition U is an identity for `inf_e F`.**  For every `B`,
`B − Σ(B, W(B))g ≤ B − g·sup_{e>g} N/e = inf_{e>g} Φ(e; B, W(B)) ≤ max_𝓔 inf Φ = inf_{e>g} F(e)`.  So
`U(g) := sup_B (B − Σ(B, W(B))g) ≤ inf_{e>g} F(e)` trivially, and the proof gives the converse: **`inf_{e>g} F(e) = U(g)`
exactly**.  This makes a sharp numerical test possible (§8, tests 1a/1b: equality to `2·10⁻¹³·a`).

2.5 **Answers to the questions of the brief.**
* `W(0) > 0`: the proof does not use `W(0) = 0`, and the statement is true; but then `M_{W,b}(x) ≤ b − W(0)x < 0`
  for large `x`, so **no nonnegative `T` satisfies the hypothesis** — the statement is vacuous for exponent
  functions (and for `T` not bounded below one is outside the Lean lemma, 1.2).  Harmless: in §6 `W_j(0) = 0`.
* `θ(∞) > 0`, finite slope at zero, flat pieces, kinks: nothing in the proof uses more than "convex,
  nonincreasing, `≥ 0`, continuous on `(0, ∞)`"; (c) handles the non-attained cases.  Tested numerically for
  each of these shapes (§8).
* `W` not nondecreasing: (c) can fail to produce a point of `𝓔` — the hypothesis is used.  `W` not convex: false
  (2.6).  `W` with values above one: Lemma M fails (`x + M(x)` not nondecreasing) *and* quasi-convexity fails.

2.6 **Non-convex `W`: why the bound fails, exactly.**  `M_{W,b}(x) = max_B (B − W(B)x)` depends on `W` only through its
lower convex envelope `W**` on `[0, b]` (it is `x·W*(1/x)`, a Legendre transform).  So for non-convex nondecreasing
`W`, `R[M_{W,b}] = R[M_{W**,b}]`, to which Proposition U applies with `W**`; and by Lemma L applied to each line of
`W**` (a minorant of `M_{W,b}`), `R[M_{W,b}](g) ≥ sup_B [B − max(W**(B), Σ(B, W**(B)))·g]`.  Wherever `Σ(B, W**(B)) ≥ W**(B)`
at the maximising `B` this is the exact value, and it is strictly larger than the line-by-line value
`sup_B [B − Σ(B, W(B))g]` as soon as the maximiser sits where `W** < W`.  Confirmed by brute force on `R` (§8,
test 2).  Remark (2) of §5 is therefore right; its example (harness XVI.7) is an instance with
`W(B) = min(1, Σ(B, B))`, which is nondecreasing and continuous but not convex.  Note that the coordinator's own
negative control in `r1_checks.py` does **not** by itself show this: it compares the line-by-line value with
`R_ref`, which is an *upper* estimate of `R[T]` (the family `β → 0` only); a value of `R_ref` above the line-by-line
value proves nothing about `R[T]`.  The conclusion is nevertheless true, by the argument just given (Lemma L).

## 3. Corollary U′

**Verdict: correct as stated.**

* The set `{B ∈ [0, b] : Σ(B, W(B)) < ∞}` is an interval containing `0` (`B ↦ Σ(B, W(B))` is convex and nondecreasing with
  values in `[0, ∞]`, `Σ(0, ·) = 0`), contained in `[0, b′]`; on it `B − Σ(B, W(B))g ≤ B − W′(B)g ≤ M_{W′,b′}(g)`.  Whether
  `b′` itself belongs to the set is irrelevant (`W′ ≤ Σ(·, W(·))` is trivially true where the right side is `∞`).
* `sup min(T, R[T]) ≤ b′` because `M_{W′,b′} ≤ b′` (`W′ ≥ 0`).
* `b′ ≤ min(b, E(W))`: `Σ(B, s) = ∞` for `B > (1 − s)a` is elementary (the ratio tends to `+∞` as `e → 0`), and
  `B ↦ W(B) − 1 + B/a` is strictly increasing, so the root is unique.  Note the non-strict inequality: when `θ` has
  a finite slope at zero, `Σ((1 − s)a, s) = (1 − s)|θ′(0+)| < ∞` (not attained unless `θ` is affine near zero), so
  the boundary line `B = (1 − s)a` can be regular.  The corollary is stated correctly for this case ("forces
  `B ≤ (1 − W(B))a`").  [(Σ3) of §2 — "if `0 < Σ(B, s) < ∞` the supremum is attained" — is false exactly on this
  boundary; that is Referee B's part, and it does not affect §§5–8, where every `𝓜(B, s)` that is used has
  `B < (1 − s)a` strictly: see 6.1, 6.3.]
* For the iteration one also needs `min(T, R[T])` nonincreasing (`exactRec_props` [V]) and `b′ > 0`; in §6
  `b_j ≥ h` because `Σ(h, W_j(h)) ≤ Σ(h, p_j(h)) ≤ Σ(h, L) = L < ∞`.

## 4. Lemma T

**Verdict: correct as stated** (well-definedness paragraph, (a) and (b)).

4.1 *Well-definedness.*  I checked the induction behind the paragraph: `I_j := {B ∈ [0, b_0] : p_j(B) ≤ s_t}` is a closed
interval `[0, c_j] ∋ h` (convex, nondecreasing, lsc; (P2)); on `I_{j−1}` the points `(B, p_{j−1}(B))` satisfy
`B ≤ b_0 < (1 − s_t)a ≤ (1 − p_{j−1}(B))a`, so `p_j` is finite there, hence (convex + lsc + finite on a closed
interval) continuous there.  If `c_{j−1} < b_0` then `p_{j−1}(c_{j−1}) = s_t` (continuity of `p_{j−1}` on a neighbourhood,
by the induction hypothesis) and `p_j(c_{j−1}) = Σ(c_{j−1}, s_t) ≥ s_t + (c_{j−1} − h)/h > s_t` by (2.1) — this needs
`c_{j−1} > h`, which holds because `p_{j−1}(h) ≤ L < s_t` and `p_{j−1}` is continuous.  So `c_j < c_{j−1}`, `p_j` is finite
on a neighbourhood of `c_j = B_t(j)`, and `p_j(B_t(j)) = s_t` exactly.  The borderline `p_j(b_0) = s_t` is case A with
`c_j = b_0`; the next level is then in case B by (2.1).  Case B is absorbing (`p_{j+1} ≥ p_j`), and reached by (P3).
`m_j ≥ s_t/B_t(j) > 0`.  All fine.

4.2 *(a).*  The left derivative at `B_t(j)` — an interior point of the set where `p_j` is finite — is a subgradient;
hence the continuation is convex and `≤ p_j` everywhere (also where `p_j = ∞`).

4.3 *(b).*  `H_j = Σ(·, W_j(·))` is convex on `[0, b_0]` with values in `[0, ∞]`: the argument of (P1) uses joint
convexity of `Σ` on all of `ℝ²` and monotonicity in `s` for all real `s`, both of which hold because `Σ` is a supremum
of affine functions with nonnegative coefficients; in particular nothing goes wrong where `W_j > 1` (there
`Σ = ∞`).  If `j` is in case A and `j + 1` in case B, then `H_j = p_{j+1}` on all of `[0, b_0]` and (b) is (a) — the proof's
"Otherwise `B_t(j + 1) < B_t(j)`" silently reads `B_t(j) = b_0` in this sub-case; wording only.  If both are in case B:
`H_j = p_{j+1}` on `[0, B_t(j)] ∋ B_t(j + 1)`, the left derivative of `H_j` at `B_t(j + 1)` is that of `p_{j+1}`, i.e. `m_{j+1}`,
and `B_t(j + 1)` is interior to `{H_j < ∞} ⊇ [0, B_t(j)]` (`Σ(B_t(j), s_t) < ∞` as `B_t(j) < b_0 < (1 − s_t)a`).  A
subgradient inequality of a convex `[0, ∞]`-valued function at an interior point of its domain holds globally,
including at points where the function is `+∞`.  ✓.

Numerical confirmation with my own code, six pairs: §8, test 5 (no violation on grids; a 0.5 % increase of the
tangent slope is detected).

## 5. Proposition C

**Verdict: correct as stated.**

* Base: `W_0 = p_0 = 0` (case A), `M_{W_0,b_0} ≡ b_0`, and `T_{k₁} ≤ b_0`.
* Step `j → j + 1`: Corollary U′ with `T = T_{k₁+j}` (nonincreasing, `≥ 0` [V]), `W = W_j|[0, b_j]` — values in `[0, 1]` by
  the range condition at index `j` (`j ≥ 1`) or trivially (`j = 0`), convex, nondecreasing, continuous by Lemma T(a) —
  `b′ = b_{j+1}` by definition, and `W′ = W_{j+1}|[0, b_{j+1}]`, which is `≤ Σ(·, W_j(·))` by Lemma T(b) and `≤ 1` by the range
  condition at index `j + 1`.  The range condition "for all `0 ≤ j < n`" gives exactly the indices `1, …, n` that are
  needed for the conclusion at all `j ≤ n`.  ✓.
* `E_j`: the algebra is right (`s_t + m_j(B − B_t(j)) = 1 − B/a`), the root lies on the linear part because
  `s_t < 1 − b_0/a < 1 − B_t(j)/a`, and `b_{j+1} ≤ E_j` follows from "`Σ(B, W_j(B)) < ∞ ⟹ W_j(B) ≤ 1 − B/a`" — also when
  `E_j > b_0` (then the statement is void).  This bound does not depend on the range condition, so there is no
  circularity in Lemma RC, which uses it.
* A point of presentation: `W_j` is defined on the fixed interval `[0, b_0]`, the majorant uses its restriction to
  `[0, b_j]`, and `W_j` may exceed one on `(b_j, b_0]`; this is harmless (Lemma T(b) is a statement on `[0, b_0]` with
  `Σ = ∞` where `W_j > 1`), but the reader has to notice it.

## 6. Lemma RC

**Verdict: correct; two small steps of the "Uniformity" paragraph are left to the reader (wording, not
substance).  I supply them in 6.2.**

6.1 *Cases.*  `j + 1` in case A: trivial.  (α) `j` in A, `j + 1` in B: then `b_{j+1} = b_0` (all points `(B, p_j(B))`, `B ≤ b_0`,
are regular), and `W_{j+1}(b_0) ≤ p_{j+1}(b_0) = Σ(b_0, p_j(b_0)) ≤ Σ(b_0, s_t) → Σ(h, s_t) < 1` — continuity of `Σ(·, s_t)` at `h`
holds because `(h, s_t)` is an interior regular point (`h < (1 − s_t)a`).  ✓.  (β) both in B: the reduction to
`s_t + m_{j+1}(E_j − B_t(j + 1)) ≤ 1` is right (also when `E_j > b_0`), and I checked each inequality:
* `m_{j+1}(B_t(j) − B_t(j + 1)) ≤ p_{j+1}(B_t(j)) − s_t` — subgradient inequality for `p_{j+1}` at `B_t(j + 1)`;
  `p_{j+1}(B_t(j)) = Σ(B_t(j), s_t)`; `D` nondecreasing in `B`.  ✓
* `m_{j+1}(1 − s_t − B_t(j)/a)/(m_j + 1/a) ≤ (m_{j+1}/m_j)(1 − s_t − h/a)`.  ✓ (`B_t(j) > h`)
* `m_{j+1} ≤ 1/e₁ + (θ(e₁)/e₁)·p_j′(B₁−)`: from (Σ4) at `(B₁, σ₁)`, dividing by `B₁ − B > 0` and letting `B ↑ B₁`; then
  `p_j′(B₁−) ≤ m_j` by convexity (`B₁ < B_t(j)`).  ✓.  `𝓜(B₁, σ₁) ≠ ∅` because `B₁ < b_0 < (1 − s_t)a ≤ (1 − σ₁)a`
  (`σ₁ = p_j(B₁) ≤ p_{j+1}(B₁) = s_t`) and `Σ(B₁, σ₁) = s_t > 0`: the ratio `N/e` tends to `−∞` at `0`, to `0` at `∞`, and is
  positive somewhere.  (So the false boundary case of (Σ3) is not touched.)
* `m_j ≥ (s_t − p_j(h))/(B_t(j) − h) ≥ (s_t − L)/(b_0 − h)`.  ✓

6.2 *Uniformity in `j`.*  The claim is justified.  After the inequalities above, `j` enters only through
(1) `B_t(j) ∈ (h, b_0)` in `D(B_t(j), s_t) ≤ D(b_0, s_t)`; (2) the pair `(B₁, σ₁)`, about which only
`B₁ ∈ (h, b_0)`, `0 ≤ σ₁ ≤ s_t` and `Σ(B₁, σ₁) = s_t` are used; (3) `m_j ≥ (s_t − L)/(b_0 − h)`.  The two missing steps:
* *`σ₁ → σ_*` uniformly.*  `Σ` is uniformly continuous on the compact set `K = [h, b̄] × [0, s_t]`, `b̄ < (1 − s_t)a`
  (interior regular points); let `ω` be its modulus.  First, `σ₁ ≥ L` once `ω(b_0 − h) < s_t − L`: for `σ < L`,
  `Σ(B₁, σ) ≤ Σ(B₁, L) ≤ L + ω(b_0 − h) < s_t`.  (The report uses strict monotonicity of `Σ(h, ·)` "on `[L, s_t]`" without
  saying why `σ₁` is in that interval.)  Then `|Σ(h, σ₁) − s_t| ≤ ω(b_0 − h)`, and `Σ(h, ·)` has slope `≥ 1` on `[L, s_t]`
  (convex, `≥` identity, equal to it at `L`), so `|σ₁ − σ_*| ≤ ω(b_0 − h)`.
* *The maximisers.*  `e₁ ≤ B₁/s_t ≤ b̄/s_t` (the numerator of the ratio is `≤ B₁`), and `θ(e₁) < B₁/(1 − σ₁) ≤ b̄/(1 − s_t) < a`
  gives `e₁ ≥ e_min(b̄, s_t) > 0`.  If `θ(e₁)/e₁` exceeded `λ̄ + κ` along a sequence `b_0 ↓ h`, a limit point `e°` of the
  `e₁` would satisfy `[h − (1 − σ_*)θ(e°)]/e° = s_t`, i.e. `e° ∈ 𝓜(h, σ_*)`, and `θ(e°)/e° ≥ λ̄ + κ` — contradiction.  So
  "upper hemicontinuity" is the usual closed-graph argument and is uniform in `j`.  `1/(e₁ m_j) ≤ (b_0 − h)/(e_min(s_t − L)) → 0`.
Hence `limsup_{b_0↓h} sup_j m_{j+1}(E_j − B_t(j + 1)) ≤ D(h, s_t) + λ̄(1 − s_t − h/a)`, as claimed.  (The bound is a limit
statement: for the Gaussian pair, `s_t = L + 0.05`, I find `sup_j m_{j+1}(E_j − B_t(j+1)) = 0.514, 0.316, 0.257, 0.234` for
`b_0 − h = 0.15, 0.02, 0.005, 0.001` against the limit bound `0.3005` and the requirement `< 0.45`; for `θ = 1/(1 + 2e)²`,
`b_0 − h = 0.002`: `0.177` against `0.2104`; for the cube at `u = 1`, `b_0 − h = 0.0003`: `0.2415` against `0.2978`; §8, test 5.)

6.3 *(C1), (C2) near `L`.*  `Σ(h, ·)` is continuous at `L` (interior regular point, by consequence (ii) of (H1)), so
`Σ(h, s_t) → L < 1`, `D(h, s_t) → 0`; `L < σ_* < s_t`; `𝓜(h, σ_*) → 𝓜(h, L) = {h}` by the same closed-graph argument
(`Σ(h, σ_*) = s_t → L > 0`, maximisers in a compact subset of `(0, ∞)`), and `𝓜(h, L) = {h}` is consequence (i) of (H1)
(I re-checked (i): a second minimiser `e′ ≠ h` of `g_L` gives `J(t) ≤ h + (t − L)(e′ − θ(e′))` with `e′ − θ(e′) ≠ 0`).
So the two sides of (C2) tend to `1 − L − h/a < 1 − L`.  ✓.  This is the only place of §§5–8 (upper bound) where
(H1) is used besides Lemma PT, as §9 of the report says.

6.4 *Statement.*  `ε₁` must also satisfy the standing assumption `h + ε₁ < (1 − s_t)a` of §6; the lemma does not
repeat it, §8 does.  Wording.

## 7. §8, upper bound

**Verdict: correct as stated, given Lemma PT, (Σ5)–(Σ7), (P1)–(P3) (Referee B's part) and the a-priori bound
(1.5).**

* Choice of parameters: `s_t ∈ (L, 1 − h/a)` with (C1), (C2) exists by 6.3 and consequence (ii) of (H1) (`L < 1 − h/a`);
  `b_0 = h + ε₁ < (1 − s_t)a`; `k₁` with `T_{k₁} ≤ b_0` by `τ_k → h` — available under (H0) alone (1.5).
* `τ_{k₁+j+1} ≤ b_{j+1} ≤ E_j` (Proposition C with the range condition for all indices, Lemma RC), and
  `E_j − h = δ_t(j) + (1 − s_t − B_t(j)/a)/(m_j + 1/a) ≤ δ_t(j) + (1 − s_t)/m_j`.  ✓
* (i): `δ_t(j) ≤ s_t h/j → 0` by (P3).  `δ < δ_t(j) ⟹ p_n(h + δ) ≤ p_j(h + δ) ≤ s_t` for `n ≤ j ⟹ N_t(δ) > j`;
  `δ > δ_t(j) ⟹ p_j(h + δ) > s_t` (strict monotonicity of `p_j` where positive, or `p_j = ∞`) `⟹ N_t(δ) ≤ j`.  With
  Lemma PT at `δ = (1 ∓ ι)δ_t(j) → 0`: `c_*²/(1 + ι) ≤ liminf j²δ_t(j) ≤ limsup j²δ_t(j) ≤ c_*²/(1 − ι)`.  ✓
* (ii): `N_t((1 − ι)δ_t(j)) − j → ∞` from (i) and Lemma PT; if `p_j(B′) > L + ω` (take `ω < s_t − L`), (Σ7) forces
  `N_t((1 − ι)δ_t(j)) ≤ j + (s_t − L)/c(ω) + 1`, a contradiction for large `j`; the chord from `B′` to `B_t(j)` gives
  `m_j ≥ (s_t − L − ω)/(ι δ_t(j))`.  ✓  Hence `(1 − s_t)/m_j ≤ ι·δ_t(j)·(1 − s_t)/(s_t − L − ω)` for large `j`, for every `ι`.
* Final limit: `τ_{k₁+j+1} − h ≤ (c_*² + o(1))/j²` and `k = k₁ + j + 1` with `k₁` fixed.  ✓
* "What the proof gives at finite `k`": the right inequality holds for `j = k − k₁ − 1` in case B, i.e.
  `k ≥ k₁ + 1 + N_t(ε₁)`, as stated.  The sentence about `ub_subsolution.py` (`κ₀ = 2`, "from `k = 4` on") concerns a
  different construction (no restart) and is not covered by the proof; it is labelled "not certified".  Fine.

## 8. Numerical experiments (scripts, key numbers)

All scripts and outputs are in `experiments/workstreams/R/review_A/`; floating point, nothing certified.  My code
does not import `rlib.py`: the pairs are given by `θ` itself (not by `J`), and `Σ` is computed either by direct
maximisation over `e` (`ralib.py`) or through the tangency condition `θ(e*) − e*θ′(e*) = B/(1 − s)` (`smooth.py`); the
two agree to `10⁻¹³` relative, and for the cube at `u = 1` my `θ`-based constants reproduce the report's
(`h = 0.02913914`, `L = 0.490034`, `ϑ = θ″(h)/(1 + r)³ = 4.244978`, `a = 0.11094407`, `2π²h²ϑ = 0.07114732`).

**Pairs used beyond the report's two:** `θ = e^{−e/0.3}` (finite slope at zero); `θ = 0.08 + 0.92e^{−e/0.25}` (`θ(∞) > 0`);
`θ = 1/(1 + 2e)²` (finite slope, positive everywhere); `θ = (1 − e)²₊` (finite slope, vanishes from `1` on);
`θ = (1 − (e/0.7)^{0.35})^{1.5}₊` (infinite slope); piecewise-linear `θ` with kinks, with a positive floor, a single
line `(1 − 0.8e)₊`, and one with floor `0.6` above every intercept tested; the cube at `u = 1, 3`.

**Test 1a — Proposition U on the operator `R` itself** (`a1_propU.py`, outputs `out_a1_propU_seed7.txt`,
`out_a1_propU_seed3.txt`).  `T := M_{W,b}` *exactly* (`W` convex piecewise linear, given by its kinks: `W ≡ 0`, constant,
linear, random with 1–4 kinks, flat pieces, `W(b) = 1`, `W(0) > 0`, `W ≡ 1`); `R_bf` = minimum over a `(φ, β)` grid
(`φ` on a logit grid, `β/g` from `10⁻¹⁰` to `0.999`) plus a pattern search, of the supremum over a `γ`-grid — **no
shortcut for `γ`**; `U = sup_B (B − Σ(B, W(B))g)`; `F_inf = inf_{e>g} F(e)`; `Llow = sup_B (B − max(W, Σ(B, W))g)` (Lemma L).
10 functions `θ` × 6 `(W, b)` × 4 values of `g` (from `10⁻⁴h` to `6h`), two seeds, 480 cases:

    max (F_inf − U)/a = +1.7·10⁻¹³      max (R_bf − U)/a = +7.2·10⁻¹²      min (R_bf − Llow)/a ≥ 0

and at the brute-force optimum the supremum over `γ` equals the bracket at `max(β, μ)` to `2·10⁻¹⁶` (for
`T = M_{W,b}`, `0 ≤ W ≤ 1`, this is a theorem: the bracket is nondecreasing on `γ ≤ μ` because `x + M(x)` is, and
nonincreasing on `γ ≥ μ`).  So **`R ≤ U` in every case**, to rounding.
*Not attained in general:* `min (R_bf − U)/a` is as low as `−1.1`.  With `W(0) > 0` this is expected (`T` is negative
far out); but it also happens for legitimate `T ≥ 0`: e.g. Gaussian pair, `W(B) = 2B` on `[0, 0.4]`, `g = 0.45`:
`U = inf_e F = 0.0673`, `R_bf = 0.0401 ≈ M_W(g) = 0.04`; `g = 0.6`: `U = 0.0357`, `R_bf = 0 = M_W(g)`.  Reason: `R[T](g) ≤ T(g−)`
always (`φ → 0`, `β → g`), and where the image line is *flatter* than the original (`Σ(B, W(B)) < W(B)`, i.e.
`J(W(B)) > B`) the bound `U` is above `M_W` itself.  The equality that does hold is `inf_e F = U` (2.4), and
`R[M_{W,b}](g) = U(g)` whenever `Σ ≥ W` at a maximising `B` (Lemma L).  The sentence "Proposition U holds **with
equality**" in the table of §11 (and "the bound is attained" in `r1_checks.py`) is true for `R_ref = inf_e F`, the
quantity that script computes, **not for `R[T]`**.  Harmless for the theorem (in §6, `W_j ≤ p_j ≤ p_{j+1}`).

**Test 1b — the minimax identity, many cases** (`a1b_minimax_many.py`, `out_a1b_minimax_seed11.txt`).  15 functions
`θ` × 40 `(W, b)` (`b` from `0.2a` to `1.2a`) × 3 values of `g` (from `10⁻⁵h` to `30h`) = 1800 cases:
`|F_inf − U|/a ≤ 5.5·10⁻¹³`, except one case at `2.8·10⁻⁹` which is the truncation of my `e`-range (floor `0.6 > b`,
`W ≡ 0`: the infimum is approached only as `e → ∞`).  A second run with `b` from `0.02a` to `3a`
(`out_a1b_minimax_seed5_wide_b.txt`, 900 cases): `≤ 1.1·10⁻¹²`, with one case at `2.2·10⁻⁹` of the same kind
(`b < (1 − W)θ(∞)`).  (My first version of `F` had a cancellation in `1 − g/e` for `e → g` and showed spurious
deviations of `4·10⁻⁴`; fixed by writing `F` in the variable `t = (e − g)/g`.)

**Test 2 — non-convex and non-monotone `W`** (`a2_nonconvex.py`, `out_a2_nonconvex.txt`).  `T = M_{W,b}`, `W` nondecreasing
but not convex.  In all 17 cases `U_W < Llow(W**) ≤ R_bf ≈ U_{W**}` (`|R_bf − U_{W**}| ≤ 2·10⁻⁸ a`), e.g.
Gaussian, `W = 0.8√(B/b)`, `b = 0.45`, `g = 0.002`: `U_W = 0.3025`, `Llow = 0.34049`, `R_bf = U_{W**} = 0.34049`; the instance
behind harness XVI.7 (`W = min(1, B(1 − B)/(1 − 2B))` on `[0, ½]`), `g = 5·10⁻⁴`: `U_W = 0.3271` (→ `⅓`), `Llow = 0.34853`,
`R_bf = U_{W**} = 0.34853` (→ `5/14`).  Since `Llow` is a rigorous lower bound (Lemma L), the line-by-line value is
**not** an upper bound for non-convex `W`; with the convex envelope it is.  A convex but *decreasing* `W`
(`W = 0.5(1 − B/1.2)` on `[0, 1.2]`, Gaussian, `g = 0.1`): `M_W ≡ 1.2`, `R = θ(g) = 0.4675 > U_W = 0.3306` — monotonicity of
`W` cannot be dropped either.

**Test 3 — the exact dynamics of convex majorants, remark (1) of §5 (item 5 of the brief)**
(`a3_dual_dynamics.py`, `dual_dyn.py`; `out_a3_dual_gauss.txt`, `out_a3_dual_cube1.txt`).  Own implementation, semi-analytic
(no `B`-grid: `S_k` is stored as its list of tangent cuts and evaluated by iterating `Σ` with its partial
derivatives; cut points by bisection).  Agreement with `experiments/coordinator_checks/level_rate/README.md`:

| | mine | coordinator |
|---|---|---|
| Gaussian `τ₂`, `τ₃` | `0.500000000000`, `0.357142857143` | `½`, `5/14` |
| Gaussian `k²(τ_k^UB − h)/const`, `k = 100, 160, 320` | `1.000166, 1.000065, 1.000016` | `1.00016, 1.00006, 1.00001` |
| cube `u = 1`, `τ₂` | `0.055517524915` | `0.0555175` |
| cube `u = 1`, ratio at `k = 120, 160` | `0.998738, 0.999032` | `0.99873, 0.99903` |

(For the cube the upper-bound sequence has ratio *below* one from `k ≈ 15` on, `0.9958` at `k = 20`, increasing to
one; no contradiction — the lower bound from lines is lower still.)  The word "exact" in remark (1) means "the
best that Proposition U and Corollary U′ give"; it is not the recursion (test 1a shows `R[M] < U` is possible, and
test 4 that `T_k` is strictly below `M_{S_k,τ_k}`: `τ₃ = 0.3559` against `5/14`).

**Test 4 — the recursion itself against these majorants, end to end** (`a4b_recursion_fine.py`,
`out_a4b_recursion_fine_gauss_NU641.txt`).  Gaussian pair, `T₁ = θ`, `T_{k+1} = min(T_k, R[T_k])` on 781 accuracies in
`[10⁻⁸, 1]`; `T_k` piecewise linear; the supremum over `γ` evaluated *exactly* for the interpolant, using only the
proved monotonicity of `T_k` (for nonincreasing `T` the supremum is a range maximum of `y + T(y)` over
`[β/(1−φ), μ/(1−φ)]`, or the value at `β` if `β > μ`; checked against the brute-force `γ`-grid: `10⁻⁸`); the infimum
over `(φ, β)` on a `700 × 72` mesh, then a zoom in `φ` for every `β`, then a 2-d zoom.  Levels `2, …, 16`:

    max_g (T_k − M_{S_k,τ_k})(g) ≤ 2.7·10⁻⁹,        min_g (T_k − sup_B (B − p_k(B)g)) ≥ 0        at every level

(the first is positive only at rounding level, where the lower bound from lines, `T_k` and the majorant coincide
to `10⁻⁷`); e.g. `T₃(10⁻⁸) = 0.355155 ≤ τ₃^UB = 0.357143` (lines: `0.307958`); `T₁₆(10⁻⁸) = 0.252354 ≤ 0.252426` (lines:
`0.252275`).  So Proposition U + Corollary U′, iterated on the true recursion, and Lemma L/Proposition A are both
confirmed pointwise in `g`.
*A pitfall, recorded because it nearly produced a false alarm:* my first search over `(φ, β)` (coarse mesh, 2-d
zoom around the best cells) gave `T_k − M` up to `+8·10⁻⁵` at `g ≈ 0.2–0.9`, stable under refinement of the `g`-grid.
It was a failure of the search, not of the proposition: the optimum (the family `β → 0`, `φ = g/e*`) is a narrow
valley, hidden on the mesh behind the plateau `φ → 0, β → g` whose value is `T(g)`.  Proof that it was the search:
it returned `R[T₂](0.853) = 0.0054065 > R[M_{S₂}](0.853) = 0.0054024` although `T₂ ≤ M_{S₂}` pointwise and `R` is
monotone.  With the row-wise zoom: `R[T₂](0.853) = 0.0054023 ≤ 0.0054024 = M_{S₃}(0.853)`, lines `0.0054023`.
(`a4_recursion_vs_majorant.py` is the earlier, cruder version with the brute-force `γ`-grid; superseded.)

**Test 5 — §§6 and 8 for other pairs** (`a5_chain.py`, outputs `out_a5_chain_*.txt`).  For each pair, `s_t = L + 0.05`,
`b_0 = h + ε₁`: (C1), (C2); `B_t(j)` by bisection; `m_j` by the chain rule; `E_j`; `b_j`; the range condition; the bound on
`m_{j+1}/m_j`; Lemma T(b) on a grid of `[0, b_0]` and on 120 points per level of the linear part of `W_{j+1}`;
convexity of `W_j`.

| pair | `ε₁` | levels | (C2): lhs `<` rhs | largest `W_{j+1}(b_{j+1})` | Lemma T(b): min of `Σ(B, W_j) − W_{j+1}` on linear parts | `j²(b_j − h)/const` at the last level |
|---|---|---|---|---|---|---|
| Gaussian | `0.02` | 200 | `0.3005 < 0.45` | `0.8277` | `−7·10⁻¹³` | `1.143` |
| `e^{−e/0.3}` | `0.02` | 300 | `0.1474 < 0.4252` | `0.7187` | `≥ 0` (grid) | `1.032` |
| `0.08 + 0.92e^{−e/0.25}` | `0.02` | 300 | `0.1765 < 0.4521` | `0.7186` | `+1·10⁻⁸` (grid) | `1.062` |
| `1/(1 + 2e)²` | `0.02` | 300 | `0.2104 < 0.4993` | `0.6958` | `≥ 0` (grid) | `1.084` |
| `(1 − (e/0.7)^{0.35})^{1.5}` | `0.01` | 300 | `0.3709 < 0.4547` | `0.8615` | `+9·10⁻¹⁰` (grid) | `1.128` |
| cube `u = 1` (own `θ`) | `0.003` | 250 | `0.2978 < 0.4600` | `0.8177` | `−2·10⁻¹²` | `1.139` (at `j = 200`) |

The range condition holds at every level in all six runs; the slope-ratio bound `m_{j+1}/m_j ≤ 1/(e₁m_j) + θ(e₁)/e₁`
holds with room (`m_{j+1}/m_j → 1`, bound `→ λ̄ ≈ 1.33–1.44`); a 0.5 % increase of the tangent slope of `W_{j+1}` is
detected at every level sampled (so the test of Lemma T(b) is not vacuous); second differences of `W_j` are
`≥ −10⁻¹³`.  My Gaussian numbers agree with the coordinator's `r2_chain.py` to all printed digits (e.g. `j = 200`:
`B_t − h = 1.460877·10⁻⁵`, `m_j = 7.07314·10⁴`, `W_{j+1}(b_{j+1}) = 0.763037`).  The remarks at the end of §6 are
reproduced: from `b_0 = h + 0.15` the range condition fails (`1.0643` at `j = 1`); at `s_t = L + 0.15` (C2) fails
(`0.481` against `0.35`) while the range condition holds from `b_0 = h + 0.02` (largest value `0.931`).

(Entries `−7·10⁻¹³`, `−2·10⁻¹²` are from the adaptive sampling next to the tangent point, where the two sides agree
to rounding; "(grid)" means the fixed grid of `[0, b_0]` only.)

**Test 6 — Proposition C end to end** (`a6_chain_vs_recursion.py`, `out_a6_chain_vs_recursion_gauss.txt`).  Gaussian pair,
the recursion of test 4 (461 accuracies, 20 levels), `s_t = L + 0.05`, `b_0 = h + 0.02`; restart at `k₁ = 6`
(`τ₆ ≤ τ₆^UB = 0.26906 < 0.27`, grid value `0.26784`).  For `j = 0, …, 14` (levels `6, …, 20`):
`max_g (T_{k₁+j} − M_{W_j,b_j})(g) ≤ 1.0·10⁻¹⁰` (rounding level, attained at `g ≈ 0.4–1`, where both sides equal the
hinted exponent to that accuracy), and `τ_{k₁+j} ≤ b_j` with large room at small `g` (`T₂₀(10⁻⁸) = 0.25152`, `b₁₄ = 0.25469`).
The chain is far from tight at these levels (it is delayed by `k₁ + N_t(ε₁)` levels) — this is a test of the logic,
not of the constant.

**The coordinator's scripts.**  `python3 r1_checks.py` and `python3 r2_chain.py gauss 0.05 0.02 200` run and print what
the report says.  Two remarks on `r1_checks.py`, part 5: (i) it is not a brute force on `R` — it evaluates the family
`φ = g/e, β = 10⁻⁹g` with the `γ`-shortcut, i.e. `inf_e F(e)`; that is the right quantity for testing the minimax step
(the only step of Proposition U that is not machine-checked), but it should be described as such; (ii) for the
same reason its "negative control" does not show that `R[T]` exceeds the line-by-line value (2.6 gives the
argument that does).

## 9. Not checked

* Nothing was compiled: I read the Lean statements and the proofs I cite (`monotoneS_step`, `of_limit`, `of_macro`,
  `line_le_Rstep`, `stepLE_Rstep`, `exactRec_props`, the dependencies of `rate_top0` on `HintPair`) but did not run
  `lake` (forbidden by the brief).
* Referee B's part — (Σ1)–(Σ7), (P1)–(P3), Lemma PT, Proposition A, §§9–10 — was used as stated.  I only
  re-derived what my part needs in passing: joint convexity and monotonicity of `Σ` on all of `ℝ²`, (2.1),
  consequence (i) of (H1), `Σ(h, L) = L`, and I saw numerically (test 5) that `j²δ_t(j)/c_*²` is `0.95–0.96` at
  `j = 200–300` and increasing, and `m_jδ_t(j) ≈ j/190 → ∞` (Gaussian), consistent with (i), (ii) of §8.  This is not
  a check of Lemma PT.
* No interval arithmetic; all numerics are floating point.  The brute force on `R` gives *upper* estimates of the
  infimum over `(φ, β)`; where I assert "`R ≤` bound" this is conservative, where I assert "`R <` bound" (finding 2)
  it is rigorous in direction for `T = M_{W,b}` (there the supremum over `γ` sits at `max(β, μ)`, which is in the `γ`-grid;
  and the example of finding 2 also follows by hand from `R[T](g) ≤ T(g−)`).  Tests 4 and 6 rest on a piecewise-linear interpolant of `T_k` (an over-estimate where
  `T_k` is convex); levels `≤ 20`, Gaussian pair only.
* The chain of §6 was followed to `j ≤ 300` only (the coordinator reports `1000`), for `s_t − L ∈ {0.05, 0.15}`.
* The cube at slopes other than `u = 1` (dual dynamics, chain) and `u = 3` (Proposition U) was not run.
* `ub_subsolution.py`, `dual_ub_*.py`, `iterate_exact.py`, `lines_lb*.py` were not read; I compared only their
  reported numbers with mine (test 3).
* I did not try to formalise anything, and did not check the heuristic remarks of §0 on novelty and on finite `n`.

## 10. Addendum — the report was revised during the review (`020e990` → `9626e4f`)

I diffed the two versions.  Unchanged: §5, §6, the "Upper bound" paragraph of §8, the row of `r1_checks.py` in
§11.  So the verdicts of §0 and findings 1, 2, 3(a), 3(b), 4, 5, 6 apply to the current text as they stand.

* **Finding 3(c) is now met** (§1: "Every `θ` with (H0) is covered: the shear defines its partner …").  The
  sentence is right; to be a `HintPair` it still needs an `E` with `θ_hint > 0` on `(0, E)` — `E = h` works, since
  `θ_hint(e) ≥ h − e`.
* **Finding 7 is now met** ((Σ3) restricted to `B < (1 − s)a`, with the same kind of example).
* **Corollary E (new §8b)** — *for `|θ′(0+)| ≤ 1`: `T_k(x) = sup{B − p_k(B)x : p_k(B) < ∞}`* — is in the domain of this
  review (it is an application of Corollary U′).  **Verdict: correct.**  Checked: (1) for a regular pair
  `B ≤ (1 − s)a`, hence `[B − (1 − s)θ(e)]/e ≤ (1 − s)(a − θ(e))/e ≤ (1 − s)|θ′(0+)| ≤ 1 − s`: image slopes are at most
  `1 − s ≤ 1`.  (2) `θ = M_{p_1,a}`: `p_1 = Σ(·, 0)` is finite on the closed interval `[0, a]` (value `|θ′(0+)|` at `a`),
  convex, lsc, hence continuous there, and `θ` is the envelope of its tangent lines.  (3) *The step that is not
  written:* Proposition U needs `W = p_k` continuous on a closed interval `[0, b_k]` with `b_k` attained.  This
  holds here, by induction: with finite slope at zero `Σ(B, s) < ∞` iff `B ≤ (1 − s)a` (for `s ≤ 1`), so
  `{p_k < ∞} = {B ≤ b_{k−1} : B + a·p_{k−1}(B) ≤ a}` is a closed interval `[0, b_k]` (`p_{k−1}` continuous), and `p_k` is
  convex, lsc and finite on it, hence continuous, with `p_k ≤ 1 − p_{k−1} ≤ 1`.  (With infinite slope the set
  `{p_k < ∞}` is half-open and `p_k` is unbounded on it — which is why §6 is needed there.)  (4) Corollary U′ with
  `W′ = p_{k+1}` then gives `T_{k+1} ≤ M_{p_{k+1}, b_{k+1}}`; "`≥`" is Proposition A.
  *Numerically* (`a8_corollaryE.py`: the recursion itself on 810 accuracies, method of test 4, against the
  Legendre transform of `p_k` computed with my slope map): `θ = e^{−0.8e}` (slope `0.8`): `0 ≤ T_k − sup_B(B − p_k(B)g) ≤ 6·10⁻⁶,
  1.1·10⁻⁵, 2.0·10⁻⁵` at `k = 2, 3, 4` (the size of my interpolation error), `T_2(0+) = B_∞(2) = 0.718891`;
  `θ = 0.5e^{−2e}` (slope exactly one): `≤ 3·10⁻⁶, 5·10⁻⁶` at `k = 2, 3`; negative control `θ = e^{−3e}` (slope `3`):
  `T_2(0+) = 0.5153` against `B_∞(2) = 0.4782` (the difference is `22` per cent of `τ_2 − h`, as the report says),
  `T_3(0+) = 0.4186` against `0.4111`.
  Corollary E is also the right form of remark (1) of §5 for these pairs: `S_k = p_k`, no cut (finding 1), and my
  counterexample there, `θ = (1 − 0.8e)₊`, is an instance (`T_2 = h·(1 − 0.8x)₊`, `τ_2 = h = 5/9`).
* **Not reviewed** (added after my brief; labelled sketch / "not re-written" by the author): Proposition S
  (§8a, profile at positive accuracy; its upper half quotes Proposition C) and the paragraph "One-sided
  curvatures" of §9.  One remark on the latter: its claim that Lemma RC needs only "the multiplier one and the
  unique maximiser at the fixed point, which differentiability of `J` at `L` gives" agrees with my reading of
  Lemma RC — (H1) enters it only through consequences (i) and (ii), and both follow from "`J` has a unique
  maximiser `L ∈ (0, 1)` and is differentiable there" (6.3); the passage-time input ((Σ6), Lemma PT) is
  Referee B's part.

