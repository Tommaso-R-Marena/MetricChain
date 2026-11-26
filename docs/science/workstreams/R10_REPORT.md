# R10 — independent review and replication of the theory division's workstream Y (a known part with interactions along the chain)

*Science division, workstream R10, 2026-11-26.  Object: `docs/workstreams/Y_REPORT.md` of the theory division at
commit `658b77f` (read-only export), 612 lines, with `experiments/workstreams/Y/`.  Everything of mine is in
`experiments/science/ws_R10/` (scripts `r10_*.py`, one log per run, running notes `NOTES.md`).  Labels: **[V]**
machine-checked, **[P]** paper proof (given or re-derived here), **[K]** known and cited, **[N]** numerical only,
**[C]** conjecture, **[H]** heuristic.  **REVIEW** = read and re-derived by me; **REPL** = re-computed with my own
code, written from the definitions of the report before I opened any file of `experiments/workstreams/Y/`;
**RERUN** = their code run from a scratch copy.  "Y" = the report under review; "the cube" = the uniform product
measure with the same slope.*

## 0. How far I got, and the verdicts in five sentences

All five tasks of the brief were done; nothing in §§3–5, 8 of Y was found false, and **every number that carries
the headline at `u = 1` was replicated with own code** (controls and lower ends to all printed digits, the Markov
recursion to all printed digits, the tilt-state recursion with an independent, differently built safe
discretisation that gives slightly *smaller* upper ends than Y's).
**The headline stands exactly where Y states it — slope `u = 1`, `p ∈ {0.4, 0.3, 0.2, 0.1}` — and is proved there
in the sense Y says** (lower ends: every algorithm, every `n`, machine-checked Theorem 11.27(b) plus paper algebra
plus a numerical evaluation; upper ends and the reading of `h`, `a` as exponents of algorithms: given unrefereed
or once-refereed theorems of the theory report).
**It is not a statement about "an interaction" in general: the direction depends on the slope.**  With Y's own
Proposition F (and, as a cross-check, with Y's own functions) I prove the *opposite* direction at larger slopes:
the capacity exponent `a` of the chain is **below** the cube's at every slope computed from `u = 3` on for
`p ≤ 0.3` (`u = 3, 4, 6`), from `u = 2.5` on for `p ≤ 0.2`, from `u = 2` on for `p = 0.1`, and `h` is below the
cube's at `u = 4, 6` for `p ≤ 0.2`; only the threshold `E` is raised for every slope.  Two sharpenings: the threshold bracket closes (`E_∞ = E_F` to `10⁻¹⁰` at `p = 0.4, 0.3, 0.2`;
`[0.401719, 0.403619]` at `p = 0.1` instead of `[0.401719, 0.417991]`), and `h` is raised down to `p = 0.02`.
The small-slope factor `(1−p)/p` is a theorem at second order — the maximal variance of a Lipschitz function —
and it is the zero-wave-vector susceptibility **only for ferromagnetic (associated) chains**.

One sentence of Y is wrong (§7.2 at `p = 0.4`, minor); one "negative result" is proved for a different object
than the one its consequence needs (§8.3; repaired here with an explicit example); the rest are precisions.

## 1. Verdict table

Columns: Y's label → my verdict; how it was checked; where.  "digits" = agreement to every digit Y prints.
Vocabulary of the verdict column: **proved** = re-derived by me (REVIEW); **replicated** = re-computed with my own
code (REPL), with the agreement stated; **confirmed** = valid, and my independent values are compatible;
**conditional** = follows from inputs I did not check; **wrong** = with the counter-example; **not checked**.
Nothing in this table was "checked only by re-running their code": the one RERUN (row 38) accompanies an own
computation.

| # | statement of Y | Y's label | verdict | checked by | script / log |
|---|---|---|---|---|---|
| 1 | §2 controls: cube `h = 0.0291391`, `a = 0.1109441`, `E = 0.1201145`; 2 (3) independent sites as one super-site, 6 (38) vertices, same per-site values; non-additive vertices carry no weight; field control `(0.7, 0.3)`; vertex counts `2, 6, 38, 990, 395 094`; 120 vertices for slopes `(1.847, 1, 1.847)` | reproduced | **replicated**, digits | REPL; REVIEW of "vertices for one slope = integer height functions" | `r10_01_controls` |
| 2 | Theorem Y1 (U): `π = ρe^{−g}/Z`, `A_π(ψ) = A_ρ(ψ+g)/A_ρ(g)`, `ψ + g ∈ 𝒞_{d⁺}`, `d⁺` attained | proved | **proved** | REVIEW (proof re-derived) + REPL (480 cases on 40 chains: identity `7·10⁻¹⁵`, admissibility `2·10⁻¹⁴`, slack left `2·10⁻¹⁵`, control violated 480/480) | `r10_02_reductions` |
| 3 | Theorem Y2 (L): marginal `= ⊗π_{B_j}·Πρ_j`; two-sided bound | proved | **proved** | REVIEW + REPL (marginal `5·10⁻¹⁶`; 480 cases, 0 violations) | `r10_02_reductions` |
| 4 | Theorem Y3 (L′): `ψ′∘proj + Σ ln ρ_j ∈ 𝒞_d`, `A_π(ψ) = A_⊗(ψ′)` exactly | proved; new | **proved** (the proof does not need `d⁻ ≥ 0`; only the application to §11.26 does) | REVIEW + REPL (180 cases: `2·10⁻¹⁴`, `4·10⁻¹⁵`; control violated 178/180; 25 of 40 random chains had an empty `d⁻` class) | `r10_02_reductions` |
| 5 | §3.3 table of the brute force | numerical | **replicated** in substance (own random chains incl. mixed binary/ternary alphabets; not their instances) | REPL | `r10_02_reductions` |
| 6 | Lemma A (every algorithm, every `n`, any reference measure) | proved from 11.27(a),(b) [V] | **proved**, given the statement of Theorem 11.27(a),(b) as printed in the theory report | REVIEW (I did not open the Lean file) | §3.1 below |
| 7 | Lemma B (product theorem) | proved given strong duality | **proved** | REVIEW; numerically row 1 | §3.1 |
| 8 | Lemma C (monotonicity, bounded changes of the law) | proved | **proved** | REVIEW | §3.1 |
| 9 | Proposition D (a)–(d): `F⁺_L` sub-additive, `F⁻_L` super-additive, sandwich, gap `≤ tC`, limit | proved | **proved** (with the caveat Y states: at `m = 0` it needs `u > K`, `u > 2K` for `L = 1`) | REVIEW + REPL of the numbers of §4.2 (`−0.0415 … −0.1150`, `+0.0189 … +0.0351`, `0.096`) and of `F*_n(0.45)/n = 0.02895, 0.03280, 0.03359, 0.03354`; "`≤ 0.09`" for the plain `F_L` is consistent with my exact values (largest ratio `0.086`, by hand from the log) | `r10_08_sandwich`, `r10_03_small_n A` |
| 10 | Theorem E(a): lower bound for every algorithm and every `n` | proved; only 11.27(b) [V] | **proved** (given rows 6, 9) | REVIEW | §3.1 |
| 11 | Theorem E(b), (c): adaptive and non-adaptive exponents as iterated limits | proved given 11.101(b); 11.95, 11.98(d) | **conditional, as Y says**; the steps that are Y's own (the reductions, `R̂_∞(ε₁ − C/L) → R̂_∞(ε₁)`, the bound `τ ≤ a/(a + ε₁)` on the maximiser) re-derived; the cited theorems not re-derived.  Status of the inputs at `658b77f`: §3.2 | REVIEW of the logic only | §3.2 |
| 12 | Theorem E(d), (e); inhomogeneous chains [sketch]; open side question `inf_L a⁺_L/L = a_∞` | — / sketch / open | **not checked** | — | §12 |
| 13 | Proposition F (Markov recursion), site and block form | proved | **proved** | REVIEW (both forms re-derived) + REPL: `u* = 1.2183, 1.5261, 1.9807, 2.7497`; `h ≤`, `a ≤`, `E ≤` for `L = 1, 2, 3`, digits; finite-`n` inequality against exact values, 36 + 24 cases, never violated | `r10_06_markov_recursion`, `r10_15_large_slope_checks` |
| 14 | Proposition G (tilt-state recursion): relation (★), relaxation, growth bounds | proved | **proved** | REVIEW ((★) re-derived and solved for `θ_±`) + REPL with an own discretisation | `r10_tilt`, `r10_07a`, `r10_07b` |
| 15 | §5.2 "conservative discretisation" is on the safe side | proved | **confirmed** | reading of `ydp3.py` line by line (REVIEW) + an independent safe scheme of mine that is everywhere `≤` Y's values + finite chains: safe value `≥` exact maximum over all vertices in 144 cases | §4.3; `r10_07b_tilt_finite` |
| 16 | §5.2 tightness of the relaxation for `q̃ ≥ p` (`n = 3, 4`); "no such test for `q̃ < p`" | numerical | **replicated and extended**: tight for `q̃ ≥ 0.85p` (`n = 3, 4, 5`), **not tight at `q̃ = 0.6p`** (excess up to `0.17`) | REPL | `r10_07b_tilt_finite` |
| 17 | Proposition H (tilted Markov labels; every-`n` formula; `G_∞`) | proved | **proved**; **replicated**, digits: `0.033503, 0.038695, 0.041770, 0.039608` at the same `(t*, c*)`; `c = 0`: `0.028907, 0.028151, 0.026626, 0.023418` | REVIEW + REPL (formula against the definition at `n = 8`, 27 cases, `3·10⁻¹⁵`; moment Lyapunov exponents by two independent methods, `10⁻¹¹`) | `r10_04_lower_bounds`, `r10_lyap` |
| 18 | Proposition I (labels i.i.d. over blocks, exact boundary term) | proved | **proved**; **replicated** to `3·10⁻⁵`: mine `0.034040, 0.040143, 0.044618, 0.044372` at Y's `(L, t)` against `0.034026, 0.040115, 0.044599, 0.044378` (the difference is their unconverged block law, §2 m5) | REVIEW + REPL (identity against the definition, 27 cases with random asymmetric block laws, `10⁻¹⁵`) | `r10_05_block_labels` |
| 19 | Proposition J(a): `E_n ≥ ln Z_n(h)/Z_n(0)`, `E_∞ ≥ E_F` | proved, every `n` | **proved**; `E_F = 0.169127, 0.232400, 0.310766, 0.401719`, digits | REVIEW + REPL | `r10_04_lower_bounds` |
| 20 | Proposition J(b): `E_n = ln Z_n(h)/Z_n(0)` for `n ≤ 4` and `n = 5`, `p = 0.3` | numerical, exact enumeration | **replicated** (`10⁻¹⁵` for `n ≤ 4`; `n = 5` at `p = 0.3` **and** `p = 0.1`, `3·10⁻⁹`); the LP ascent at `n = 8, 10, 12` **not checked** | REPL | `r10_03_small_n` |
| 21 | Proposition J(c): `E_∞ = E_F` at `p = 0.4, 0.3, 0.2` "up to margins `1–2·10⁻⁴`" | numerical evaluation of a proved bound | **confirmed and sharpened**: the margin is an artefact of Y's cells; my safe value is `E_F + 1·10⁻¹¹, 3·10⁻¹¹, 5·10⁻¹¹` | REPL | `r10_07d_upper_ends`, `r10_07a` |
| 22 | Proposition J(d): at `p = 0.1` the relaxation is not tight, `E_∞ ∈ [0.40172, 0.41799]` | — | **true for the reference `Q = π` only**; with the reference Markov(`q̃ ≥ 0.12`) the relaxation is tight; `E_∞ ∈ [0.401719, 0.403619]` | REPL | `r10_07f_p01_scan` |
| 23 | Conjecture `E_n = ln Z_n(u/2)/Z_n(0)` for all `n`, `p` | conjecture | **not settled** | — | §12 |
| 24 | Tables 6.1 (U) and 6.2 (L′) | numerical | **replicated**: 6.1: 36 entries, largest deviation `4.9·10⁻⁶`; 6.2: the 19 entries of the (L′) columns incl. the best gaps `m`, identical; the column "(L), `L = 3`" (4 entries) **not checked** | REPL | `r10_08_sandwich` |
| 25 | Table 6.3, tilt-state columns: `h ≤ 0.036163, 0.044995, 0.054353, 0.066765`; `a ≤ 0.121446, 0.140860, 0.160745, 0.192774`; `E ≤ … 0.232538, 0.310956, …` | numerical evaluation of proved bounds | **valid upper bounds** (mine are all smaller): `h ≤ 0.036028, 0.044719, 0.054121, 0.062762`; `a ≤ 0.120996, 0.140182, 0.160048, 0.172043`; `E ≤ 0.169127, 0.232400, 0.310766, 0.403619` | REPL (own safe scheme) | `r10_07d`, `r10_07e`, `r10_07f`, `r10_07g` |
| 26 | Table 6.4: the lower ends | proved formulas, numerical | **replicated** (rows 17–19); `a ≥`: mine `0.116817, 0.127042, 0.130486, 0.116429` against `0.116817, 0.126444, 0.129797, 0.116632` | REPL | `r10_04`, `r10_05` |
| 27 | §6.4 exact site-wise optimum for `n = 6 … 12`, "sparse and slowly varying" label law, best domain lengths, "best estimate `0.0405–0.041`" | numerical | **not checked** | — | §12 |
| 28 | §6.5 slope table at `p = 0.3` and strong coupling | numerical | **replicated** (Markov labels, `L = 1` recursion, `E_F`), and **extended** in both directions (§5) | REPL | `r10_10_map`, `r10_13_reversal` |
| 29 | §6.5 "small slopes: all three exponents are multiplied by `χ = (1−p)/p`" | numerical | **upgraded**: a theorem at second order for every finite chain, and for `F_∞` the upper side is proved (§3.4) | own derivation + REPL | `r10_11_small_slope` |
| 30 | §7.1 non-additive vertices carry weight at `p = 0.1` (`a_4 = 0.5726559` against `0.5626014`, weight `0.092` on `−min(|x|, 4−|x|)`; `n = 5` dual values `0.25009`, `0.10662`) | numerical, exact | **replicated**, digits; **added**: the true optimum at `n = 5` (column generation over all 395 094 vertices) is `0.1965988` (`0.0945869`), i.e. `+1.4 %` (`+1.9 %`) | REPL | `r10_03_small_n` |
| 31 | §7.2 the Rényi centre is not a Markov chain: `I(x₁;x₃|x₂) = 2.9·10⁻³, 5.7·10⁻³, 1.2·10⁻³`; Walsh norms `0, 0.245, 0, 0.009`, pair coefficient `−0.100` | numerical | **replicated** (`2.904·10⁻³, 5.730·10⁻³, 1.150·10⁻³`; `0, 0.2448, 0, 0.0089`; `−0.1000`) | REPL | `r10_03_small_n A` |
| 32 | §7.2 "for short chains (`n = 4`, `t = 0.45`) the optimal labels are the two uniform fields and `γ* = −t⁻¹ ln cosh(th·m)`" | numerical | **wrong at `p = 0.4`**, right at `p = 0.3, 0.1` (§2 m1) | REPL | `r10_03_small_n A` |
| 33 | §8.1 every-`n` statements for the block-stratified sample | proved given 11.95 | **not checked** (it is rows 2, 4 plus Theorem 11.95) | — | §12 |
| 34 | §8.2 the pair-type-stratified sample is unbiased | proved, same proof | "π is uniform on Markov-type classes" **re-derived**; the guarantee **not checked** | REVIEW | — |
| 35 | §8.3 class-wise quantiles of an admissible residual are not admissible for Markov types: explicit example; 598 of 600 | proved by example; brute force | **replicated** (the example verified by hand and for `n = 5 … 9`; 599 of 600 with my own residuals, largest excess 6 flips, 74 classes, 0 for the cube) — **for the level function**; for the *truncated residual*, which is what the lower-bound argument needs, Y gives no example: **supplied here** (464 of 600; explicit `n = 4` example) | REVIEW + REPL | `r10_09_markov_types`, `r10_09b` |
| 36 | §9 beyond chains | sketch | **not checked** | — | §12 |
| 37 | §0.2 headline at `u = 1`: all three exponents above the cube for `p ∈ {0.4, 0.3, 0.2, 0.1}`; "at `p = 0.3`: `h` +38 % to +54 %, `a` +14 % to +27 %, `E ×1.935`" | — | **confirmed**; with my brackets: `h` +37.8 % to +53.5 %, `a` +14.5 % to +26.4 %, `E ×1.9348` | REPL | §4 |
| 38 | "a nearest-neighbour interaction … raises all three exponents" read as a statement beyond `u = 1` | (Y: "`u ≥ 2` undecided for `h`"; nothing said about `a`) | **false for `a` and `h` at larger slopes** (counter-examples proved, §3.5); true for `E` at every slope | own computation with Y's Proposition F + RERUN of Y's functions | `r10_13_reversal`, `r10_14_rerun_their_functions`, `r10_06 … large_u` |

## 2. Findings

**Critical: none.**  No proof of Y fails and no reported number is wrong beyond its last digit.

**Major (1).**

* **M1 — the direction of the effect depends on the slope; "raises all three exponents" must carry its range.**
  Y's §0.2 answers "does a nearest-neighbour interaction without a field change the exponents?" with "Yes —
  upwards", states the range `u = 1`, and adds that for `u ≥ 2` its lower bound for `h` drops below the cube
  ("not decided there").  That is correct as written, but the answer to the question is not "upwards": by Y's
  own Proposition F with blocks of three sites (all 72–96 vertices, duality brackets `≤ 10⁻¹¹`; `r10_13_reversal`)

  | `(p, u)` | chain, proved upper bound | cube | ratio |
  |---|---|---|---|
  | `a`: `(0.3, 3)`, `(0.3, 4)`, `(0.3, 6)` | `0.495806`, `0.591982`, `0.671581` | `0.502282`, `0.603052`, `0.675836` | `0.987`, `0.982`, `0.994` |
  | `a`: `(0.2, 2.5)`, `(0.2, 3)`, `(0.2, 4)` | `0.408174`, `0.467509`, `0.559986` | `0.424612`, `0.502282`, `0.603052` | `0.961`, `0.931`, `0.929` |
  | `a`: `(0.1, 2)`, `(0.1, 3)`, `(0.1, 4)` | `0.323641`, `0.432593`, `0.509682` | `0.327813`, `0.502282`, `0.603052` | `0.987`, `0.861`, `0.845` |
  | `h`: `(0.2, 4)`, `(0.2, 6)` | `0.236455`, `0.330399` | `0.239250`, `0.336076` | `0.988`, `0.983` |
  | `h`: `(0.1, 4)`, `(0.1, 6)` | `0.229339`, `0.310496` | `0.239250`, `0.336076` | `0.959`, `0.924` |

  (`h`: supremum over all `t` certified by a grid of step `0.005` and the interval rule.)  The same numbers come
  out of Y's own functions `lip_vertices`, `capacity`, `h_bracket` run at these slopes (`r10_14`): e.g.
  `a ≤ 0.495806` at `(0.3, 3)`, `h ∈ [0.227585, 0.233073]` at `(0.1, 4)`.  So **at slopes of two to three `k_BT`
  per site and more the interaction lowers the non-adaptive exponent, and at four and more also `h`** (for
  `p ≤ 0.2`; at `p = 0.3` exact finite chains indicate the same, `r10_15`, but the proved bound is `1.6 %` above
  the cube).  Only `E` is raised for all `u` (`E_F > ln cosh(u/2)`, closed form).  Mechanism, §6.
  *Why major:* the sentence that travels — in the brief of this review, and into
  `PHYSICAL_APPLICABILITY.md` if copied — is "interactions raise the exponents; the product-measure exponents
  are optimistic for real chains".  It is true for the threshold, and for `h`, `a` at slopes up to about `1`–`2`;
  it is false beyond.
  *Replacement text for Y §0.2, first line:* "**Yes, and the direction depends on the slope.**  At `u = 1` all
  three exponents rise for every `p ∈ {0.4, 0.3, 0.2, 0.1}` (table).  The threshold rises for every slope
  (`E_∞ ≥ E_F > ln cosh(u/2)`).  The capacity exponent `a` and the exponent `h` do **not** rise for every slope:
  the Markov recursion with `L = 3` gives `a_∞ <` cube at `u = 3, 4, 6` (`p ≤ 0.3`), also at `u = 2.5` (`p ≤ 0.2`)
  and `u = 2` (`p = 0.1`), and `h_∞ <` cube at `u = 4, 6` (`p ≤ 0.2`).  Between about `u = 1.5` and these values the direction
  of `a` is open, with every lower bound below the cube."
  *Replacement for §6.5, last sentence of the slope paragraph:* "For `u ≥ 2` the lower bound is below the cube;
  at `u = 4, 6` and `p ≤ 0.2` the Markov recursion (`L = 3`) is below the cube as well: **at large slopes `h` is
  lowered.**"

**Minor (12).**

* **m1 — §7.2, one sentence wrong at `p = 0.4`.**  Y: "For short chains (`n = 4`, `t = 0.45`) the optimal labels
  are the two uniform fields and `γ* = −t⁻¹ ln cosh(th·m)`".  Exact optimum over all 990 vertices
  (`r10_03_small_n A`, bracket `< 10⁻⁷`): at `p = 0.3` and `p = 0.1` yes (two labels, weights `½, ½`;
  `max|γ* − model| = 8·10⁻¹²`, `2·10⁻¹²`); **at `p = 0.4` the optimal law has four labels** — the uniform fields
  `++++`, `−−−−` with weight `0.4165` each and the two-domain labels `++−−`, `−−++` with weight `0.0835` each —
  and `max_x |γ*(x) − (−t⁻¹ ln cosh(th·m(x)))| = 0.156`; the Walsh norms by order are `0, 0.1972, 0, 0.0038` and
  the nearest-neighbour coefficient `−0.1051` (Y's `0, 0.245, 0, 0.009`, `−0.100` are those of `p = 0.3, 0.1`).
  Y's value `I(x₁;x₃|x₂) = 2.9·10⁻³` at `p = 0.4` is nevertheless the right one (mine: `2.904·10⁻³`, with the
  four-label optimum).  *Replacement:* "For `p = 0.3, 0.1` (`n = 4`, `t = 0.45`) the optimal labels are the two
  uniform fields …; for `p = 0.4` two-domain labels already carry weight `0.167`."
* **m2 — §8.3 proves non-admissibility of the level function, not of the truncated residual.**  In Y's example
  (`ψ = d(·, 0…010)`, `x = 110…0`, `y = 010…0`, `q < 1/(n−2)`) the class of `y` has the values `{0, 2}` and level
  `0`, the class of `x` is a singleton with level `3`, `d(x, y) = 1`: the *levels* violate `t(x) − t(y) ≤ d(x, y)`
  — verified by hand.  But the truncated residual `max(ψ, t)` is `ψ` itself on both classes
  (`ψ^{tr}(x) − ψ^{tr}(y) = 1 = d`), and Y's brute force (`y08`, part (c)) also tests levels only.  What the
  optimality argument of Theorem 11.76/11.95 needs is that the *truncated residual* stays in the class.  It does
  not: with my own residuals (`n = 9`) `max(ψ, t)` is inadmissible in 464 of 600 cases (largest excess 4 flips),
  0 for the type classes of the cube.  *Explicit example, checked by hand* (`n = 4`, `u = 1`, `q = ½`):
  `ψ = d_H(·, 0100)`; `a = 1101` lies in the Markov-type class `{1101, 1011}` (first letter 1; pairs 11, 10, 01
  once each) with `ψ = 2, 4`, so the level is `4` and `ψ^{tr}(a) = 4`; `b = 0101` is a singleton class with
  `ψ^{tr}(b) = 1`; `d(a, b) = 1`; `4 − 1 = 3 > 1`.  *Replacement:* add this example and the count for the
  truncated residual.
* **m3 — status of inputs out of date.**  Y §1 and §4 call Theorems 11.99 and 11.101 "unrefereed".  At `658b77f`
  both are reviewed (SCI-REV-0005; §3.2).  Unrefereed are 11.95 (non-machine-checked parts), 11.98(d), 11.97(a),
  (b).
* **m4 — "restricted" value `0.04435` (§6.3) is the open end of a bracket.**  Y's own output
  (`y15_dp3_controls.txt`) shows the grid-restricted iteration at `G = 1601` between `0.0439975` and `0.0443495`;
  only the lower end is a certified lower bound of the relaxed value.  With nodes at cell midpoints the bracket
  closes at `0.044357` (`r10_07a`), so Y's conclusion ("finer grids would lower the `h`-bound to about `0.0446`")
  stands: relaxed value `∈ [0.044357, 0.044622]` at `(t, q̃) = (0.43, 0.255)`.
* **m5 — Proposition I is evaluated with an unconverged block law.**  `y07` calls the Arimoto iteration with
  `itmax = min(40000, 300 + 3·10⁸/size)`, i.e. 400 iterations at `L = 14`.  Any block law gives a valid bound, so
  nothing is wrong; the family gives a little more (`+1…3·10⁻⁵`; with `L = 16`: `0.040166, 0.044739, 0.044732` at
  `p = 0.3, 0.2, 0.1`).
* **m6 — the upper ends at `p = 0.1` are not optimised.**  `y13` scans the reference flip probability up to
  `1.15p` (`h`) and `1.1p` (`a`); at `p = 0.1` the minimum sits at the edge of the scan (their own output for `a`
  is monotone: `0.24926 … 0.19277`).  With the range up to `1.6p`: `h ≤ 0.062762` (Y `0.066765`), `a ≤ 0.172043`
  at `q̃ = 0.16` (Y `0.192774`).
* **m7 — the threshold at `p = 0.1` (§5.4(d)).**  "The relaxation is not tight" holds for the reference `Q = π`
  (my safe value `0.426387` at `G = 1601`, Y `0.42766`), but the reference is free: for a symmetric Markov
  reference with `q̃ ≥ 0.12` the safe value equals `E_F + KL`-rate`(q̃‖p)` to `7·10⁻¹¹` (the uniform fields are
  the relaxed optimum again), and the minimum over `q̃` is `0.403619` at `q̃ = 0.115`, `G = 1601`.  *Replacement:*
  "`E_∞ ∈ [0.401719, 0.403619]`".
* **m8 — the margins `1.0, 1.4, 1.9·10⁻⁴` of §5.4(c) are an artefact.**  In `ydp3.py` the cells are
  `[μ_k − D/2, μ_k + D/2]` around nodes that include `±u*`, so the end cells overhang the range of the tilt by
  `D/2` and the reward is taken at `u* + D/2`; with `k′_+(u*) = 0.215`, `k′_−(u*) = 0.363` (`p = 0.3`) and
  `D/2 = 4.8·10⁻⁴` that is `1.4·10⁻⁴` — exactly their margin.  Since `|λ| ≤ u*` is proved, cells inside the range
  are legitimate, and then safe value `=` restricted value `= E_F` (`r10_07a`, `r10_07d`).
* **m9 — §7.1, the dual value overstates the effect.**  "`0.25009` (`0.10662`) against the site-wise optimum
  `0.19396` (`0.09283`)" compares an upper bound with a lower bound.  The exact `F*_5` over all vertices is
  `0.1965988` (`0.0945869`) with weight `0.094` (`0.163`) on non-additive vertices: the effect at `n = 5`,
  `p = 0.1` is `1.4 %` (`1.9 %`).
* **m10 — §6.5, "nothing is decided for `p ≤ 0.05`".**  With the two uniform fields on blocks of any length
  (Proposition I with a dynamic programme over the block magnetisation, `r10_blockfield`): `h ≥ 0.037540`
  (`p = 0.05`, `L = 6`; `×1.288`), `h ≥ 0.029973` (`p = 0.02`, `L = 7`; `×1.029`).  Undecided remains `p ≤ 0.01`
  (best checked lower bound `0.023164`, `×0.795`).  The formula is validated in `r10_16_blockfield_check` (36
  cases against the definition, `8·10⁻¹⁶`; `Λ_blk` against exact increments, `10⁻⁹`).
* **m11 — §6.5, "the susceptibility of the chain".**  Right for this chain; in general the small-slope factor is
  the maximal Lipschitz variance, which is the susceptibility only under association (§3.4).  `[numerical]` can
  be replaced by `[proved at second order; upper side proved for F_∞]`.
* **m12 — Theorem Y3, parenthesis.**  "it must have no negative entries" is a condition for applying §11.26, not
  for the theorem: the identity and the admissibility hold whenever the `d⁻` class is non-empty (3 random chains
  with negative entries of `d⁻`: no violation).

**My own errors, for the record.**  (i) A first run of Proposition I converged the Arimoto iteration to
`10⁻¹²` inside a golden-section search and had to be killed after 28 CPU-minutes.  (ii) An import of a script
without a `__main__` guard started its body a second time.  (iii) In restricted mode the power iteration does
not close its bracket at small `p`; lower ends I had printed for `p = 0.01, 0.001` are withdrawn (they are in
`NOTES.md`, marked).  (iv) My first range for the reference flip probability at `p = 0.1` was as narrow as Y's
(`r10_07d`); the log is kept, the numbers quoted are from the wider range (`r10_07e`, `r10_07f`).  (v) A first
map script crashed on a format; (vi) three logs from runs that timed out or crashed are kept under
`*_superseded.log` and are **not** cited.

## 3. Statements: what I re-derived, and what is new here

### 3.1 Re-derivations (REVIEW)

*Vertices.*  `{e^{−φ} : φ ∈ 𝒞_d}` is the convex cone `{v > 0 : v(y) ≤ e^{d(x,y)} v(x)}`; in `w = πv` the functional
`w ↦ Σ_x w(x)^t Q(x)^{1−t}/(Σw)^t` is concave on the normalised slice, so `max_φ (1−t)D_t(π_φ‖Q)` is attained at an
extreme ray, i.e. where the tight constraints determine `φ` up to a constant: a vertex of the Lipschitz polytope.
For one slope on the cube a connected tight graph forces `f(x) − f(y) ≡ dist(x, y) mod 2`, hence every edge is
tight: the vertices are the integer height functions (homomorphisms of the cube to `ℤ`).  [P]

*Lemma A.*  `Φ_φ = φ̃ − γ̃*` is Lipschitz for the slack of `γ*`, `E_{π_{γ*}} e^{−Φ_φ} = 1`, and 11.27(b) with weights `M`
gives `(1−2δ) ≤ E|Q|·e^{tr}·max_x Σ_φ M(φ)(π_φ(x)/π_{γ*}(x))^t`; with `π_{γ*} ∝ (ΣMπ_φ^t)^{1/t}` the sum equals
`e^{−G_t(M)}` for every `x`.  Correct.  [P from V]

*Lemma B, C, Proposition D.*  Re-derived as written; (a) uses Theorem Y1 and Lemma B, (b) Theorem Y3, (c) the
minimum over the two end letters (needs `d⁻ ≥ 0`), (d) Fekete twice.  `|F*_n − nF_∞| ≤ tC` with `C = 2(u+K)`.  [P]

*Proposition F.*  With `V_i = E_π[e^{−φ} | x_{≤i}]`: `−ln V_i` is Lipschitz in `x_i` with `d*_i = d_i + G_i` (the
future depends on the past through `x_i` only), the conditional law of `x_i` under `π_φ` is a Gibbs law of a
member of `Lip(d*_i)` with respect to `P_i(x_{i−1}, ·)`, and the backward induction `U_{i−1} ≥ c_i ⋯ c_n V_{i−1}^t`
gives the bound.  Block form: inside a block the site recursion shows that `E[w | first letter]` has log-slope
`≤ u*`, hence the slack of a block is `g(u*)` at its last site only.  The same argument with the chain rule for
`KL` gives `a_n ≤ Σ_i max_b a[P_i(b,·); d*_i]` directly.  For the binary symmetric chain
`g(x) = 2 artanh(λ tanh(x/2))`, `λ = 1 − 2p`.  [P]

*Proposition G.*  (★) is `V_i(…,a) = Σ_c P(a,c)V_{i+1}(…,a,c)` in ratios; solved for the controls,

    θ_− = λ + ln(p e^{μ_−} + 1 − p) − ln((1−p) e^{μ_+} + p),      θ_+ = λ + ln(p + (1−p) e^{−μ_−}) − ln(1 − p + p e^{−μ_+}),

feasible iff both lie in `[−u, u]`.  `θ_−` increases in `λ`, `μ_−` and decreases in `μ_+`; `θ_+` increases in `λ`,
`μ_+` and decreases in `μ_−`: on a box of cells the ranges are attained at corners.  My safe scheme uses this (no
Lipschitz slack); Y's uses that `θ_±` are 1-Lipschitz in each argument (slack `1.5D`).  Both are correct.  [P]

*Propositions H, I, J(a).*  Re-derived line by line (gauge `τ = σs`; the tilt by `Z(σ)^t`, resp. `c_φ^t`, cancels
the normalisation; `½[KL(Q‖π₊) + KL(Q‖π₋)] = KL(Q‖π) + ln E_π e^{hm}`).  `λ_max(B_Q ρ₀) = 1` for a flip-symmetric
block law because the row sums of `B_Q ρ₀` are `2Q(first letter)`.  [P]

### 3.2 Inputs of Theorem E and their status at `658b77f`

| input | used for | status in the theory report at `658b77f` |
|---|---|---|
| Theorem 11.22, 11.27(a), (b) | Lemma A, every lower bound | **[V]** (`QueryLowerBound.lean`, `GeneralisedDips.lean`) |
| Theorem 11.28(d), remark (i) | "the threshold of the `n`-chain is `E_n`" | [V inequality; P] |
| Theorem 11.99 | Rényi form, monotonicity of `F/t`, `F/(1−t)`, strong duality | [P; two steps V]; **reviewed: proved** (SCI-REV-0005) — Y says "unrefereed" |
| Theorem 11.101(b) | E(b): an adaptive algorithm with exponent `R̂` exists | [P by transfer]; **reviewed: proved with two gaps, closed** (SCI-REV-0005); the count of evaluations of Theorem 11.52 inherited; **nothing simulated** — Y says "unrefereed" |
| Theorem 11.95 | E(c), §8 | truncation and lower bounds [V]; the rest [P], **unrefereed** |
| Theorem 11.98(d) | E(c): non-adaptive exponent | [P], **unrefereed**; its upper bound rests on 11.97(c) (re-derived by the reviewer of SCI-REV-0005) |
| Theorem 11.97 | error terms in E(d) | [P]; (c) re-derived, (a), (b) **unrefereed** |

All of them are applied to product landscapes whose sites are blocks (alphabet `2^L`, one site type, envelope
`d⁺` or `d⁻`), which is inside their stated scope (any alphabet, envelopes not necessarily symmetric, full
support).  I did not re-derive any of them here.

### 3.3 What "raised" and "lowered" mean, exactly

`F_∞(t) = lim_L F^±_L(t)/L` exists [P, row 9].  `E_∞ = lim F_∞(t)/t`, `h_∞ = max_t F_∞(t)`, `a_∞ = sup_t F_∞(t)/(1−t)`.

* A **lower bound** `F_∞(t) ≥ G` says: every `(ε₁n/2, δ)`-correct algorithm makes at least
  `(1−2δ)exp(n[G − tε₁] − tC)` evaluations, for every `n` — [V] + [P] + a numerical evaluation.
* An **upper bound** `F_∞(t) ≤ B` for all `t` says: no label law in Lemma A gives more than `B`; that an
  *algorithm* achieves it is Theorem E(b), (c), given the inputs above.
* So "`h` raised" (lower bound above the cube's exact exponent) is unconditional; "`h` lowered" and "`a`
  lowered" are unconditional statements about the game function, and statements about algorithms given
  11.101(b), resp. 11.95 and 11.98(d).  "`a` raised" as a statement about non-adaptive algorithms needs the
  every-`n` bound of 11.98(d).

### 3.4 The small-slope law  (new here; `r10_11_small_slope`)

**Proposition R10.1 [P; checked numerically].**  Let `(X, π)` be finite, `π` of full support, `d = u·d₀` with `d₀`
symmetric, `0 < t < 1`.  Then

    F*_X(t) = (t(1−t)/2)·u²·V + O(u³),        V := max{ Var_π(f) : f ∈ Lip(d₀) },

and `V` is attained at a vertex.  Consequently `E_X, a_X = u²V/2 + O(u³)` and `h_X = u²V/8 + O(u³)`.  The `O(u³)`
depends on the diameter of `(X, d₀)`: nothing is uniform in `n`.
*Proof.*  Upper bound with the centre `Q = π`: `(1−t)D_t(π_φ‖π) = t ln E_π e^{−φ} − ln E_π e^{−tφ}`, whose cumulant
expansion is `(t − t²)κ₂(φ)/2 − (t − t³)κ₃(φ)/6 + …` (sign of the third-order term corrected by the coordinator; it does not enter the statement).  Lower bound with the two labels `±u f*`, weights `½, ½`
(`−f*` is in the class because `d₀` is symmetric): `Σ_x (½π₊^t + ½π₋^t)^{1/t} = 1 − (1−t)u²Var(f*)/2 + O(u³)`.  For
`E` and `a` the same two labels and the same centre.  ∎
*Checks.*  Binary chain, `n = 4`, all 990 vertices, `t = 0.3`: `F*_4/(u²t(1−t)/2) = 1.7168, 1.7725, 1.7871, 1.7908`
at `u = 0.4, 0.2, 0.1, 0.05` against `V_4 = 1.7920`; three-letter Potts chain, `n = 2`, all 534 vertices:
`0.5970, 0.5791, 0.5684, 0.5627 → 0.5567`.

**Proposition R10.2 [P].**  Binary alphabet, Hamming envelope, `π` associated (in particular: a
nearest-neighbour chain with ferromagnetic couplings and arbitrary fields — the FKG lattice condition holds
because the pair weights have a non-negative determinant; [K], FKG inequality, from memory).  Then
`V = ¼·Var_π(Σ_i s_i)`, attained by the uniform field.
*Proof.*  Let `f ∈ Lip(d₀)` and `g = ½Σ_i s_i`.  Both `g + f` and `g − f` are coordinatewise nondecreasing, so
`Cov(g + f, g − f) ≥ 0`, i.e. `Var f ≤ Var g`.  ∎  (The trick of Newman's inequality; no citation is needed.)
*Check:* all vertices, `n ≤ 5` (395 094 at `n = 5`): `V_n = ¼Var(m)` to all digits for `p = 0.4, 0.3, 0.1`
(`V_5 = 1.7188, 2.3668, 4.5268`), and for the helix–coil chain with Zimm–Bragg weights at four parameter sets
(e.g. `s = 1, σ = 10⁻³`: `V_5 = Var(N_helix) = 0.102379`).

**Corollary [P for the first statement; P-upper / sketch-lower for the second].**  For such a chain the
small-slope factor relative to the product measure with the same one-site marginals is, at fixed `n`,
`Var(Σs_i)/Σ Var(s_i)`, and per site in the limit the **zero-wave-vector structure factor**
`S(0) = Σ_k corr(s_0, s_k) = (1+λ₂)/(1−λ₂)`: `(1−p)/p` for Y's chain, `σ^{−1/2}` for the helix–coil chain at its
midpoint `s = 1`.  For `F_∞` (first `n → ∞`, then `u → 0`) the upper side is proved: Proposition F with `L = 1`
gives `F_∞(t) ≤ F*[(1−p, p); u*](t)`, `u* = u/(2p) + O(u³)`, and the two-letter site has
`F* = (t(1−t)/2)p(1−p)u*² + O(u³) = (t(1−t)/8)u²·(1−p)/p`.  The lower side for `h` and `a` follows from block
fields on blocks of length `∼ 1/u` with gaps `∼ ln(1/u)` (Theorem Y3) — a sketch, not written out; for `E` it is
exact (`E_F/ln cosh(u/2) → (1−p)/p`).  Numerically `r10_10_map` (table in §5).

**The statement "the exponents at small slope scale with the `k = 0` susceptibility" is false in general
[counter-examples, N exact].**  The right quantity is `v* = lim V_n/n`, the maximal variance per site of a
Lipschitz function; it is `≥` every mode of the structure factor and equals `S(0)` only under association.
(i) Antiferromagnetic chain `p = 0.7`: `V_n` is attained by the *staggered* field (`V_5 = 2.3668` against
`¼Var(m) = 0.6388`) — the gauge image of `p = 0.3`.  (ii) Frustrated binary chain
`π ∝ exp(J₁Σs_is_{i+1} + J₂Σs_is_{i+2})`, `n = 5`, all 395 094 vertices: for `(J₁, J₂) = (0.5, −0.5)` the maximiser is
the modulated site-wise label `−−+++` with `V_5 = 1.9620` against `¼Var(m) = 1.0140`; for `(0.3, −0.8)`:
`2.3905` against `0.5304`; for `(−0.4, −0.6)`: `2.0419` against `0.4813`.  (iii) Three-letter Potts chain: for
`J > 0` the maximiser is the number of sites in one letter and the factor is the structure-factor sum
(`n = 2` exact; `n = 3, 4` by LP ascent, a lower estimate: `1.3793, 1.9086` and `1.4507, 2.1718` for
`J = 0.7, 1.5`, equal to the finite-`n` sums); for `J = −1` the best label found has variance `1.3166` at `n = 4`
against `0.5878` for the letter count.
*Status and support, statement by statement.*

| statement | label | supported by |
|---|---|---|
| `F*_X(t) = (t(1−t)/2)u²V + O(u³)` for every finite `(X, π)`, symmetric envelope (R10.1) | **[P]**, checked [N] | proof above; `r10_11_small_slope` part 1 (binary chain, `n = 4`, 990 vertices, four slopes) and part 3 (Potts, `n = 2`, 534 vertices) |
| `V = ¼Var(Σs_i)` for a binary associated reference (R10.2) | **[P]**, checked [N] over all vertices, `n ≤ 5` | proof above; `r10_11_small_slope` parts 1 and 4 |
| small-slope factor `= S(0)` for ferromagnetic two-state chains, at fixed `n` | **[P]** | R10.1 + R10.2 |
| the same for `F_∞` (first `n → ∞`): upper side | **[P]** (given Proposition F) | expansion of the `L = 1` recursion; `r10_10_map`: upper/cube `2.331` at `u = 0.05`, `p = 0.3` (`S(0) = 2.333`) |
| the same for `F_∞`: lower side for `h`, `a` | **[P-sketch]**, [N]: lower/cube `2.260` at `u = 0.05` | `r10_10_map`; for `E`: exact, `E_F`/cube `= 2.332` |
| "scales with the `k = 0` susceptibility" for a general one-dimensional known part | **false** — counter-examples [N, exact enumeration] | `r10_11_small_slope` parts 1 (antiferromagnet), 2 (frustrated chain, all 395 094 vertices), 3 and 3b (antiferromagnetic Potts; `n = 3, 4` by LP ascent, a lower estimate) |
| the general quantity is `v* = lim V_n/n` (R10.3) | **[C]** | — |
| helix–coil chain at its midpoint: factor `σ^{−1/2}` | **[P]** at second order and fixed `n`; bulk value by the two-state formula | `r10_11_small_slope` part 4 (`n = 5`, all vertices, four parameter sets) |

**Conjecture R10.3 [C].**  For a homogeneous finite-range one-dimensional known part and a symmetric site
envelope, `lim_{u→0} F_∞(t; u)/u² = (t(1−t)/2)·v*` for every `t ∈ (0,1)`; `v*` is attained by labels that are
additive over sites and periodic.  (In every binary case computed the maximiser is site-wise.)

*Connection to our addendum A17 (not re-derived here).*  Proposition A17.8 bounds the variance under a Markov
reference by `¼Σ_i C_i²`, `C_i = Σ_{j≥i} c_jθ_i⋯θ_{j−1}` (in print: inequality (10) in the proof of Theorem 1 of
Chazottes–Collet–Külske–Redig, arXiv:math/0503483; Kontorovich–Ramanan 2008, Theorem 1.2).  For Y's chain
`θ = |1 − 2p|`, `c = u`, `C = u/(2p)`.  Y's Proposition F is the same martingale argument for Rényi divergences
with a *non-linear* slack: `u* = u + 2 artanh(λ tanh(u*/2)) ≤ u/(1−λ) = C`, with equality only as `u → 0`
(`u* = 1.526` against `C = 1.667` at `u = 1`, `p = 0.3`).  At second order the two differ in the conditional
variance: A17.8 uses "range `C` ⇒ variance `≤ C²/4`", Proposition F the variance of a two-letter law
`(1−p, p)`, i.e. `p(1−p)C²`; the latter is attained (Proposition R10.2), so **for Y's chain the sharp
constant in the variance bound of A17.8 is `p(1−p)` in place of `¼`**, and `¼ΣC_i²` overshoots by `1/(4p(1−p))`
(`1.19` at `p = 0.3`, `2.78` at `p = 0.1`).  For the product measure, `F_cube(t)/(1−t) = [t ln cosh(u/2) −
ln cosh(tu/2)]/(1−t)` is the exact per-site Rényi divergence of order `t < 1` between the worst Gibbs law and the
reference; the sharp bound A17.6, `D_p ≤ Σ[(p−1)c_i²/8 + L(c_i)]` (there `p > 1` is the Rényi order), is its
counterpart for orders above one: at second order both read (order)`·c²/8` per site.

### 3.5 The reversal at large slopes  (new here)

**Proposition R10.4 [P given Proposition F; numerical evaluation with duality brackets; RERUN-confirmed].**
For the binary symmetric chain and the pairs `(p, u)` of the table of M1, `a_∞(p, u) < a_cube(u)`, resp.
`h_∞(p, u) < h_cube(u)`.
*Proof.*  `F_∞(t) ≤ F^{DP}_3(t)/3` (row 13), with `F^{DP}_3 = F*[P^{(3)}(·|+); (u, u, u*)]` computed over all vertices
of the weighted cube (96; 72 where `u* > 2u`) with a duality bracket; `a_∞ ≤` capacity`/3`; for `h` the supremum
over `t` from a grid of step `0.005` by `F(t) ≤ min(B(t₁)t₂/t₁, B(t₂)(1−t₁)/(1−t₂))` and the tails `t·E`, `(1−t)·a`.
The cube's values are closed forms.  ∎
*Checks.*  (1) Y's own functions at the same parameters give the same numbers (`r10_14`).  (2) On finite chains
with all vertices the block form of the recursion is never violated (24 comparisons at `u = 1, 3, 4, 6`,
`r10_15`).  (3) Exact increments `a_n − a_{n−1}` for `n = 2, 3, 4`: `0.4582, 0.4623, 0.4623` at `(0.3, 3)` against
the cube's `0.5023`; `0.5704, 0.5709, 0.5709` at `(0.3, 4)` against `0.6031`; increments of `F*_n(t_cube)` at
`(0.3, 4)`: `0.2226, 0.2244, 0.2244` against `h_cube = 0.2392` [N: finite chains, indicative].
*Why [H].*  At large slope a label pins a configuration `σ`; the Gibbs law leaks to a single flip at site `i` with
relative weight `e^{−u}·r_i`, `r_i = e^{−K(β_{i−1}+β_i)}`, where `β = ±1` are the bonds of `σ` on both sides of `i`: an
isolated spin leaks `e^{2K}` times more, a spin inside a domain `e^{2K}` times less.  For a uniform label law
`E[r^t] = cosh²(Kt) > 1`, so to first order `F(t) ≈ (1−t) ln 2 − e^{−tu}cosh²(Kt)` against the cube's
`(1−t) ln 2 − e^{−tu}`, and shifting the label law towards long domains costs entropy at second order only.  This
predicted the reversal before the computation (see `NOTES.md`); it also shows why no Markov reference can prove
it: for any symmetric Markov `Q` the period-four label `++−−` (every spin has one equal and one opposite
neighbour) leaks exactly like the cube and has `−ln Q ≥ n ln 2`, so `max_φ(1−t)D_t(π_φ‖Q) ≥` cube.  Indeed my safe
tilt-state bound for `a` stays above the cube at every slope (`r10_07g`: ratios `1.26, 1.17, 1.10, 1.04, 1.011,
1.004` for `u = 1 … 3`, `p = 0.3`).

## 4. Replication: my numbers next to theirs

### 4.1 `u = 1`: the table of Y §0.2

Lower ends: Proposition H and I and `E_F`; upper ends: my safe tilt-state recursion (`G = 801`; `E` at `p = 0.1`:
`G = 1601`).  Cube: `h = 0.029139`, `a = 0.110944`, `E = 0.120115`.

| `p` | `h`: Y | `h`: mine | `a`: Y | `a`: mine | `E`: Y | `E`: mine |
|---|---|---|---|---|---|---|
| `0.4` | `[0.034026, 0.036163]` | `[0.034049, 0.036028]` | `[0.116817, 0.121446]` | `[0.116817, 0.120996]` | `[0.169127, 0.169165]` | `0.169127` (`±10⁻¹¹`) |
| `0.3` | `[0.040115, 0.044995]` | `[0.040166, 0.044719]` | `[0.126444, 0.140860]` | `[0.127042, 0.140182]` | `[0.232400, 0.232538]` | `0.232400` |
| `0.2` | `[0.044599, 0.054353]` | `[0.044739, 0.054121]` | `[0.129797, 0.160745]` | `[0.130486, 0.160048]` | `[0.310766, 0.310956]` | `0.310766` |
| `0.1` | `[0.044378, 0.066765]` | `[0.044732, 0.062762]` | `[0.116632, 0.192774]` | `[0.116429, 0.172043]` | `[0.401719, 0.417991]` | `[0.401719, 0.403619]` |

Every lower end of Y is confirmed as a valid lower bound and lies above the cube; every upper end of Y is
confirmed as valid (mine are smaller).  (My `a ≥ 0.116429` at `p = 0.1` is `2·10⁻⁴` below Y's `0.116632`: other
`(L, t)`, a less converged block law; both exceed the cube by `5 %`.  At `p = 0.1` the tilted-Markov family alone
gives `a ≥ 0.101876 <` cube: there the direction of `a` rests on Proposition I.)

### 4.2 Other replicated numbers

| quantity | Y | mine | log |
|---|---|---|---|
| Proposition H `(t*, c*)` at `p = 0.4, 0.3, 0.2, 0.1` | `(0.458, 0.774)`, `(0.431, 0.859)`, `(0.402, 0.861)`, `(0.364, 0.833)` | identical | `r10_04` |
| Markov recursion, `p = 0.3`: `h ≤` (`L = 1, 2, 3`); `a ≤` (`L = 3`); `E ≤` | `0.05484, 0.05180, 0.04902`; `0.15401`; `0.23419, 0.23324, 0.23285` | `0.054838, 0.051796, 0.049019`; `0.154011`; `0.234188, 0.233237, 0.232849` | `r10_06` |
| the same, `p = 0.1` | `0.09157, 0.08299, 0.07542`; `0.19678`; `0.43245, 0.42378, 0.41799` | `0.091565, 0.082987, 0.075422`; `0.196777`; `0.432449, 0.423779, 0.417991` | `r10_06` |
| tilt-state, `p = 0.3`, `t = 0.43`, `q̃ = 0.255`: safe (`G = 1601`) / restricted | `0.04468` / `0.04435` | `0.044622` / `0.044357` (closed bracket) | `r10_07a` |
| control `p = ½`, safe, `t = 0.49` | `0.0292072` (`G = 3201`) | `0.0292413` (`G = 1601`); `E`, `a` exact at every `G` | `r10_07a` |
| `a_4`, `p = 0.1`, all vertices / site-wise | `0.5726559` / `0.5626014` | `0.5726559` / `0.5626014` | `r10_03 A` |
| quantile levels, Markov types, `n = 9` | 598 of 600, excess 6 | 599 of 600, excess 6 | `r10_09` |

### 4.3 Is the discretisation on the safe side?  Yes.

Y (`ydp3.py`): nodes `μ_k`, cells `[μ_k ± D/2]`, a grid triple is feasible if the constraints hold with slack
`1.5D` (justified: `θ_±` are 1-Lipschitz in each of three arguments, each moved by at most `D/2`), stage factors
at the worse end of the cell, `KL` rewards at cell ends (convex), the Shannon reward with a slack `2D²`
(ample: `|f″| ≤ 1.3`; in fact `KL(τ‖q)` is convex in `τ(+)` and `τ(+)` is monotone in `λ`, so no slack is needed),
value function `≤ 0` with the smallest transition weights.  Each step is correct.  Mine (`r10_tilt.py`): cells
inside `[−u*, u*]`, feasibility of a box decided by corner values (exact monotonicity), the same treatment of
stage factors.  Agreement: mine `≤` Y's everywhere, by `0.3–0.6 %` for `p ≥ 0.2` (same range of references; at `p = 0.1` by `6–11 %`
because of the wider range, m6); on finite chains the safe value is never below
the exact maximum over all vertices (144 cases, smallest margin `1.2·10⁻³`).  Floating-point rounding is
controlled in neither.

## 5. Is the headline what the evidence supports?  The `(p, u)` map

**Fairness of the comparison.**  Same slope per site, same accuracy convention (`ε = ε₁n`), same class.  The cube
*is* the product measure with the same one-site marginals (the chain has uniform marginals).  Against the
product measure with the same **entropy rate** — the site `(1−p, p)`, e.g. `(0.7, 0.3)` with `h = 0.0250335`,
`a = 0.0953005`, `E = 0.1031310` — the rise at `u = 1`, `p = 0.3` is larger (`h ×1.60–1.79`, `a ×1.33–1.47`,
`E ×2.25`).  So the baseline is the right one and the comparison is fair; what is not general is the direction.

**Map** (`r10_13_reversal`: lower bounds from Propositions H and block fields, upper bounds from Proposition F
with `L = 3`; entries are `[lower, upper]/cube`; **R** = raised proved, **L** = lowered proved, `·` = undecided;
`R*` = raised only by Proposition I with `≤ 2` walls; at `u = 1, 1.5, 2` the lower ends shown include
Proposition I where it is larger, `r10_05`, `r10_05b`).

`h`:

| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | R `[1.13, 1.20]` | R `[1.06, 1.12]` | R `[1.02, 1.08]` | R `[1.003, 1.05]` | · `[0.997, 1.04]` | · `[0.995, 1.03]` | · `[0.996, 1.02]` | · `[0.997, 1.01]` |
| `0.4` | R `[1.30, 1.45]` | R `[1.15, 1.29]` | R `[1.06, 1.17]` | R `[1.008, 1.10]` | · `[0.99, 1.06]` | · `[0.98, 1.04]` | · `[0.98, 1.03]` | · `[0.99, 1.02]` |
| `0.3` | R `[1.75, 2.12]` | R `[1.35, 1.70]` | R `[1.12, 1.35]` | R `[1.007, 1.19]` | · `[0.94, 1.10]` | · `[0.92, 1.05]` | · `[0.93, 1.02]` | · `[0.94, 1.01]` |
| `0.2` | R `[2.31, 3.16]` | R `[1.50, 2.15]` | R `[1.14, 1.55]` | R* `[1.005, 1.25]` | · `[0.88, 1.12]` | · `[0.83, 1.06]` | **L** `[0.83, 0.988]` | **L** `[0.86, 0.983]` |
| `0.1` | R `[2.80, 4.75]` | R `[1.47, 2.61]` | R `[1.03, 1.73]` | · `[0.83, 1.32]` | · `[0.70, 1.11]` | · `[0.67, 1.03]` | **L** `[0.66, 0.959]` | **L** `[0.71, 0.924]` |

`a`:

| `p` \ `u` | `0.5` | `1` | `1.5` | `2` | `2.5` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| `0.45` | R `[1.07, 1.13]` | R `[1.02, 1.07]` | · `[0.999, 1.04]` | · `[0.99, 1.03]` | · `[0.99, 1.02]` | · `[0.99, 1.01]` | · `[0.99, 1.005]` | · `[0.99, 1.001]` |
| `0.4` | R `[1.20, 1.35]` | R `[1.05, 1.17]` | · `[0.997, 1.09]` | · `[0.98, 1.05]` | · `[0.97, 1.02]` | · `[0.97, 1.01]` | · `[0.97, 1.003]` | · `[0.97, 1.0001]` |
| `0.3` | R `[1.49, 1.92]` | R `[1.15, 1.39]` | · `[0.98, 1.16]` | · `[0.92, 1.05]` | · `[0.90, 1.007]` | **L** `[0.89, 0.987]` | **L** `[0.88, 0.982]` | **L** `[0.88, 0.994]` |
| `0.2` | R `[1.82, 2.74]` | R `[1.18, 1.60]` | · `[0.93, 1.20]` | · `[0.83, 1.04]` | **L** `[0.76, 0.961]` | **L** `[0.74, 0.931]` | **L** `[0.73, 0.929]` | **L** `[0.72, 0.974]` |
| `0.1` | R `[1.93, 3.78]` | R* `[1.05, 1.77]` | · `[0.67, 1.20]` | **L** `[0.58, 0.987]` | **L** `[0.54, 0.899]` | **L** `[0.51, 0.861]` | **L** `[0.48, 0.845]` | **L** `[0.47, 0.909]` |

(At `u = 1` the tilt-state upper ends of §4.1 are tighter than the `L = 3` recursion used here.)
`E`: raised for every `(p, u)` with `p ≠ ½`; `E_F/E_cube = 2.19, 1.94, 1.71, 1.55, 1.43, 1.35, 1.24, 1.15` at
`p = 0.3`, `u = 0.5 … 6`.

**Small slopes and strong coupling** (`r10_10_map`; `p = 0.3`: Y's slope table next to mine;
lower = best of Proposition H and block fields, upper = Proposition F with `L = 1`):

| `u` | `0.05` | `0.1` | `0.25` | `0.5` | `1` | `2` | `3` | `4` |
|---|---|---|---|---|---|---|---|---|
| `h` lower/cube, Y (Markov labels) | `2.271` | `2.209` | `2.022` | `1.736` | `1.328` | `0.994` | `0.925` | `0.928` |
| `h` lower/cube, mine (Markov labels) | `2.260` | `2.209` | `2.022` | `1.736` | `1.328` | `0.994` | `0.925` | `0.928` |
| `h` lower/cube, mine (block fields, `L ≤ 40`) | `2.260` | `2.210` | `2.028` | `1.751` | `1.353` | `1.007` | `0.922` | `0.928` |
| `h` upper/cube (`L = 1`), Y | `2.33` | `2.33` | `2.29` | `2.17` | `1.88` | `1.46` | `1.26` | `1.16` |
| `h` upper/cube (`L = 1`), mine | `2.331` | `2.326` | `2.289` | `2.174` | `1.882` | `1.461` | `1.258` | `1.159` |
| `E_F`/cube, Y | `2.332` | `2.327` | `2.294` | `2.194` | `1.935` | `1.546` | `1.348` | `1.243` |
| `E_F`/cube, mine | `2.332` | `2.327` | `2.294` | `2.194` | `1.935` | `1.546` | `1.348` | `1.243` |

(Identical to Y except at `u = 0.05`, where my optimiser over `(t, c)` stopped at `c = 2.18` and my block length is capped at 40: `2.260` against Y's `2.271`.)
Strong coupling at `u = 1` (lower bounds for `h`; cube `0.029139`): `p = 0.05`: `0.034299` (Markov labels, `×1.177`), `0.037540` (block fields, `L = 6`; `×1.288`); `p = 0.02`: `0.027390` (Markov labels, `×0.940`; Y: `0.0274`), `0.029973` (block fields, `L = 7`; `×1.029`); `p = 0.01`: `0.023164` (Markov labels, `×0.795`; block fields with `L > 2` are rejected there by my own check of the operator with 48 and 96 nodes).  The `L = 1` recursion gives `h ≤ 0.102297, 0.109534, 0.112374` (Y: "saturates", `0.116`).  The block-field formula is validated against the definition and against exact increments in `r10_16_blockfield_check`.

**Answer to the brief's question 3.**  "Raises all three exponents" is **proved** for `u ≤ 1` at every `p`
computed in `[0.1, 0.45]` (`a` at `p = 0.1`: by Proposition I only), for `h` also up to `u = 2` (`p ≥ 0.2`) and
`u = 1.5` (`p = 0.1`) and down to `p = 0.02` at `u = 1`; for `E` at every `(p, u)`.  It is **numerical only**
nowhere (every entry of the map is a proved bound evaluated numerically).  It is **undecided** in the dotted
cells — with every lower bound for `a` below the cube from `u = 1.5` on — and for `p ≤ 0.01` at `u = 1`.  It is
**refuted** in the cells marked L.  My attempt to refute it at `u = 1` failed, as it should: all lower ends are
valid.

## 6. Physical reading  (kept apart from the mathematics; every sentence here is [H] unless marked)

*What the model is.*  A two-state chain with a nearest-neighbour coupling `K = ln((1−p)/p)` in units of `k_BT`
(correlation length `ξ = −1/ln(1−2p)`: `1.1`, `2.0`, `4.5` sites at `p = 0.3, 0.2, 0.1`), and a residual of which
only this is known: flipping one site changes it by at most `u` (in `k_BT`).  No experimental observable occurs;
"cost" is the number of evaluations of the residual needed to certify `ln Z` to `ε₁n`.

*Small slopes (`u·S(0) ≲ 1`): cooperative response.*  The cheapest way for the residual to move `ln Z` is a
perturbation that the chain answers collectively.  By Propositions R10.1–R10.2 [P] the three exponents are, to
second order in `u`, proportional to the largest variance of a Lipschitz function, and for a ferromagnetic chain
that function is the uniform field: the variance of the block magnetisation, i.e. **the structure factor at
zero wave vector, `S(0) = (1−p)/p`** — the brief's guess is right for this chain.  The hard instances are a
shifted field over domains; Y's "domains of about `2K/u` sites" is the finite-slope version (replicated: best
block lengths `4, 5, 6, 7` sites at `p = 0.3, 0.1, 0.05, 0.02` for the two-field family).  For a chain whose
dominant fluctuation is not uniform (antiferromagnetic, frustrated) the same holds with the dominant mode in
place of `k = 0`: the factor is a property of the strongest collective fluctuation, not of the susceptibility.

*Helix–coil chain near its transition* (assumptions: Zimm–Bragg weights; the residual has single-residue
effect `≤ u`; second order in `u`): at the midpoint `s = 1` the factor is `S(0) = σ^{−1/2}` — `32` for `σ = 10⁻³`,
`100` for `σ = 10⁻⁴` — so the three exponents are `σ^{−1/2}` times those of independent two-state residues
[P at second order; `V_5 = Var(N_helix)` checked over all vertices], as long as `u ≲ σ^{1/2}` (the field over a
cooperative unit stays below `k_BT`).  This is the query-complexity counterpart of our addendum A14(ii) ("the
robust uncertainty of a local free energy is the per-site constant times the cooperative length"): the same
factor multiplies the *cost exponents* and the *threshold accuracy* `E ≈ u²S(0)/8` per residue.  Beyond
`u ∼ σ^{1/2}` the response saturates (`E_F → u/2` per residue) and nothing of the second-order statement survives.

*Large slopes (`u ≳ 2–3`): stiffness removes hiding places.*  When the residual may change by several `k_BT` per
site it can stabilise any single configuration.  Certification is then a search among the configurations the
residual could have made dominant, and the interaction makes that search **easier**: a pinned configuration
with isolated spins is destabilised by the coupling (leak `e^{2K}` times larger), so fewer configurations can be
made sharply dominant.  That is the mechanism of the reversal (Proposition R10.4 [P]).  The threshold `E` does
not reverse because it is governed by the coarse, cooperative perturbation (the uniform field) at every slope.

*Consequence for `PHYSICAL_APPLICABILITY.md`.*  "The product-measure exponents are optimistic for real chains"
is supported in this model for the threshold at every slope, and for `h` and `a` at per-site envelopes up to
about one `k_BT` (with a factor that grows like the structure factor at small slopes).  For per-site envelopes of
several `k_BT` the product-measure values of `a` and `h` are **pessimistic**.  Model-relative throughout: a
two-state nearest-neighbour chain, one slope, no field; nothing here is fitted to a molecule.

## 7. Prior art  (brief; reading level stated; I cite nothing I did not open beyond what is marked)

| item | what it is here | read |
|---|---|---|
| Rached, Alajaji, Campbell, "Rényi's divergence and entropy rates for finite alphabet Markov sources", IEEE Trans. Inf. Theory 47 (2001) 1553 | the Rényi divergence *rate* between two fixed Markov laws is the logarithm of a Perron eigenvalue; covers the closed forms `tE_F(u) − E_F(tu)` and `E_F` (one label, one Markov reference), not the max–min over labels and centres | [search snippet / abstract-level description] |
| Vanneste, "Estimating generalised Lyapunov exponents for products of random matrices", arXiv:0911.2161 | `ℓ(q) = lim N⁻¹ ln E‖X_N‖^q` and its link to large deviations; the object `L_q(κ, η; r)` of Proposition H is of this kind, and the transfer-operator method is standard | [search snippet] |
| Holliday, Goldsmith, Glynn, "Capacity of finite state channels based on Lyapunov exponents of random matrices", IEEE Trans. Inf. Theory 52 (2006) 3509–3532 | entropies and mutual information of finite-state channels as top Lyapunov exponents; Proposition H is the Rényi-order analogue (moment exponents) for the channel "label sequence → Gibbs law", with the tilt that cancels the normalisation | [search snippet / abstract] |
| Newman, "Normal fluctuations and the FKG inequalities", Commun. Math. Phys. 74 (1980) 119–128 | FKG and finite susceptibility give Gaussian block-spin fluctuations; the inequality behind Proposition R10.2 is of this family | [search snippet]; the proof of R10.2 is given in full above, so nothing rests on it |
| Bulinski, Shabanovich, Fundam. Prikl. Mat. 4(2) (1998) 479–492 | Lipschitz covariance inequality for associated variables (as I remember it) | [metadata only — statement from memory, unverified]; not used |
| Galvin, "On homomorphisms from the Hamming cube to ℤ", Israel J. Math. 138 (2003) 189–213 | the vertex set for one slope; the counts `2, 6, 38, 990, 395 094` were computed by Y and by me, not looked up | [search snippet] |
| Chazottes, Collet, Külske, Redig, arXiv:math/0503483; Kontorovich, Ramanan, Ann. Probab. 36 (2008) | the martingale bound of which Proposition F is the non-linear Rényi version (§3.4) | via our addendum A17.8 only; not opened by me |
| Csiszár (1995), Rényi capacity = Rényi radius; Arimoto (1976), the iteration | used throughout | [from memory — unverified]; cited in the theory report |

Search log: seven web searches (Lipschitz covariance inequality for associated variables; Rényi divergence rate
of Markov sources; generalised Lyapunov exponents; Bulinski–Shabanovich bibliographic data; Newman 1980;
Holliday–Goldsmith–Glynn; Galvin) and two page fetches that yielded nothing usable (a PDF in which the
reference sought does not occur; a redirect).  No full text was read.  I found no statement of the reversal of §3.5 or of
the regularised formula; I did not search for them systematically and claim no novelty.

## 8. Requests to the theory division  (can be sent as they stand)

1. **Scope of the headline (M1).**  Please replace the first line of Y §0.2 and the last sentence of the slope
   paragraph of §6.5 by the texts of §2, M1, and do not carry "an interaction raises the exponents" into the
   theory report without the range: raised for `E` at every slope; raised for `h`, `a` at `u ≤ 1` (`h` up to
   `u = 2`); **lowered** for `a` at `u = 3, 4, 6` (`p ≤ 0.3`), also `u = 2.5` (`p ≤ 0.2`) and `u = 2` (`p = 0.1`), and for `h`
   at `u = 4, 6` (`p ≤ 0.2`).  Check: `ylib.lip_vertices([u, u, ustar(u, p)])`, `bsc_block_law_cond(3, p, 0)`,
   `capacity`, `h_bracket` at `(p, u) = (0.3, 3)`, `(0.1, 4)` give `a ≤ 0.495806 < 0.502282` and
   `h ≤ 0.233073 < 0.239250`.
2. **Close the crossover.**  With the Markov recursion for `L = 4, 5` (vertices of the weighted cube
   `(u, …, u, u*)`; a double-description code does it) decide `a` at `u = 1.5, 2, 2.5` for `p = 0.3, 0.4` and `h` at
   `u = 3` and at `(0.3, 4)`.  Expected from exact finite chains: lowered.  A proof of the first-order statement
   `F_∞(t) = (1−t) ln 2 − e^{−tu}cosh²(Kt) + o(e^{−tu})` would settle all large slopes at once.
3. **The small-slope law.**  Adopt Propositions R10.1–R10.2 in place of "[numerical]" in §6.5 and write out the
   lower side for `F_∞` (blocks of length `∼ 1/u`); state the general quantity (maximal Lipschitz variance), not
   the susceptibility.
4. **Corrections of record:** m1 (§7.2 at `p = 0.4`), m2 (§8.3: add the example for the truncated residual), m3
   (status of 11.99, 11.101), m4 (the restricted value is an open bracket end), m7 (`E_∞ ∈ [0.401719, 0.403619]`
   at `p = 0.1` with a reference `q̃ ≠ p`), m8 (cells inside `[−u*, u*]`: `E_∞ = E_F` to rounding at
   `p = 0.4, 0.3, 0.2`), m9 (true `F*_5`).
5. **The threshold conjecture.**  For `Q = π` and `p = 0.1` the relaxed value lies between Y's restricted value `0.42389` and my safe value
   `0.426387` (`G = 1601`), well above `E_F = 0.401719`.  Is the
   maximiser of the relaxation realisable by a member of the class?  If yes, `E_n = ln Z_n(u/2)/Z_n(0)` fails for
   long chains; if no, an added constraint (two-step consistency) should close the bracket.

*To the engineering division:* exact vertex enumeration of the weighted cubes `(u, u, u, u*)` and
`(u, u, u, u, u*)` (15 and 31 dimensions, 64 and 160 inequalities; inputs `p`, `u`; output the vertex list or
directly capacity and `max_t F*`; validation: `L = 3` gives 96 vertices and `a ≤ 0.495806·3` at `(0.3, 3)`; stop at
`10⁷` vertices; estimate: minutes for `L = 4`).

## 9. The three most promising next steps

1. Decide the crossover slope `u_c(p)` of `a` and `h` (request 2) and prove the large-slope expansion.
2. Prove Conjecture R10.3 for ferromagnetic chains with a field (the helix–coil chain): upper side from
   Proposition F at second order, lower side from block fields; it gives the physically usable statement
   "exponents `= S(0) ×` independent residues for envelopes below `k_BT/ξ`".
3. Replace the Markov reference of the tilt-state recursion by a hidden-Markov reference (state: previous
   letter, tilt, and the direction of a `2×2` matrix product): by §3.5 this is necessary for any upper bound
   below the cube, and it is the natural centre (the Rényi centre of Proposition H is of this form).

## 10. How to re-run

All from `experiments/science/ws_R10/` with `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` (one core each;
times measured on the shared 4-core machine, some under load).  Each command writes the log named (redirect
the output to it); every log cited in this report is from a run that reached its last line.  (The logs of
`r10_07f`, `r10_09b` and of the `check` part of `r10_05` end with their last result line; all others end with a
`time` line or the shell's timing.)

| command | log | time |
|---|---|---|
| `python3 r10_01_controls.py` | `r10_01_controls.log` | 14 s |
| `python3 r10_02_reductions.py` | `r10_02_reductions.log` | 8 s |
| `python3 r10_03_small_n.py A` ; `python3 r10_03_small_n.py D` | `r10_03_small_n_A.log`, `_D.log` | 31 s ; 40 s |
| `python3 r10_04_lower_bounds.py` | `r10_04_lower_bounds.log` | 3 s |
| `python3 -u r10_05_block_labels.py check` ; `… h` ; `… a` | `r10_05_block_labels_check.log`, `_h.log`, `_a.log` | 1 s ; 8 min ; 7 min |
| `python3 -u r10_05b_propI_other_slopes.py` | `r10_05b_propI_other_slopes.log` | 5 s |
| `python3 r10_06_markov_recursion.py 1.0` ; `… 3.0 4.0 6.0 8.0` | `r10_06_markov_recursion.log` ; `…_large_u.log` | 29 s ; 13 min |
| `python3 -u r10_07a_tilt_quick.py` | `r10_07a_tilt_quick.log` | 2.5 min |
| `python3 -u r10_07b_tilt_finite.py` | `r10_07b_tilt_finite.log` | 20 s |
| `python3 -u r10_07c_smallp_convergence.py` | `r10_07c_smallp_convergence.log` | 4 min |
| `python3 -u r10_07d_upper_ends.py p 801`, `p = 0.4, 0.3, 0.2, 0.1` | `r10_07d_upper_p<p>.log` | 2.5–5 min each |
| `python3 -u r10_07e_upper_ends_general.py 0.1 801 1.0` ; `… 0.2 801 1.0` | `r10_07e_p0.1_u1.log`, `r10_07e_p0.2_u1.log` | 3 min ; 2 min |
| `python3 -u r10_07f_p01_scan.py` | `r10_07f_p01_scan.log` | 1 min |
| `python3 -u r10_07g_capacity_slopes.py 0.3` | `r10_07g_capacity_p0.3.log` | 4 min |
| `python3 r10_08_sandwich.py` | `r10_08_sandwich.log` | 3 min |
| `python3 r10_09_markov_types.py` ; `python3 r10_09b_trunc_example.py` | `r10_09_markov_types.log`, `r10_09b_trunc_example.log` | 1 s ; 1 s |
| `python3 -u r10_10_map.py` | `r10_10_map.log` | 2 min |
| `python3 -u r10_16_blockfield_check.py` | `r10_16_blockfield_check.log` | 1 s |
| `python3 -u r10_11_small_slope.py` | `r10_11_small_slope.log` | 65 s |
| `python3 -u r10_13_reversal.py 0.45 0.4 0.3` ; `… 0.2 0.1` | `r10_13_reversal_a.log`, `_b.log` | 10 min ; 15 min |
| `python3 -u r10_14_rerun_their_functions.py <copy of experiments/workstreams/Y/code at 658b77f>` | `r10_14_rerun_their_functions.log` | 10 min |
| `python3 -u r10_15_large_slope_checks.py` | `r10_15_large_slope_checks.log` | 103 s |

Libraries (no output of their own): `r10lib.py` (vertices, solvers with duality brackets), `r10_lyap.py` (moment
Lyapunov exponents, two methods), `r10_tilt.py` (tilt-state recursion; modes `safe`, `restricted`,
`restricted_mid`), `r10_blockfield.py` (block fields of any length).  Not cited and kept only as a record:
`r10_13_reversal_INCOMPLETE_superseded.log`, `r10_10_map_CRASHED_superseded.log`,
`r10_07c_smallp_convergence_INCOMPLETE_superseded.log`.

## 11. What I did not settle

* The direction of `a` for `1.5 ≤ u ≤ 2.5` (`p ≥ 0.3`) and of `h` for `2.5 ≤ u ≤ 3` and at `p = 0.3`, `u ≥ 4`; the
  direction of everything for `p ≤ 0.01` at `u = 1` (the tilt-state relaxation is useless there: safe value
  `0.0672` at `G = 1601`, converging like the cell width, against a lower bound `0.023` at `p = 0.01`, `t = 0.15`;
  `r10_07c`).
* Whether `E_n = ln Z_n(u/2)/Z_n(0)` for all `n` at strong coupling; whether `E_∞ = E_F` at `p = 0.1`.
* Conjecture R10.3; the lower side of the small-slope law for `F_∞`.

## 12. What I did not check

* The Lean files (`GeneralisedDips.lean`, `QueryLowerBound.lean`): I used Theorem 11.27(a), (b) as printed.
* Theorems 11.95, 11.97, 11.98, 11.99, 11.101, 11.28 of the theory report: not re-derived; only their status
  was looked up.  Hence nothing about algorithms' *upper* bounds is verified by me, and nothing was simulated.
* Theorem E(d) (uniformity; the remark on `n` not a multiple of `L`), E(e), the inhomogeneous sketch, the open
  side question `inf_L a⁺_L/L = a_∞`.
* Y §6.4: the exact site-wise optimum for `n = 6 … 12` (`y06`), the statements on the sparse label law and the
  best domain lengths, the "best estimate" `0.0405–0.041`; `y16` (their re-evaluation).
* Y §5.4(b): the LP ascent for `n = 8, 10, 12` (`y14`).
* Y §8.1, the guarantee of §8.2, §8.4; Y §9 (strips, `ℤ^d`, trees) entirely.
* Y §6.5: the strong-coupling numbers of the `L = 1` recursion (`h ≤ 0.116`, `a ≤ 0.302`) and `E_F → 0.499` at
  `p = 0.001` — only what `r10_10_map` prints.
* Their scripts were **not** re-run as they stand, except their library functions at new parameters (`r10_14`);
  I read `ydp3.py`, `y13`, `y07`, `ylib.py` in full and the relevant part of `y08`; I did not read `y00`–`y06`,
  `y09`–`y12`, `y14`–`y16`, `ydp2.py`, `ylyap.py`, nor `Y_notes.md`.
* Alphabets with more than two letters and chains with a field: reductions only (brute force), plus the
  small-slope variance for Potts (`n ≤ 4`) and Zimm–Bragg (`n = 5`); no exponents.
* Floating-point rounding: not controlled anywhere (theirs or mine); "certified" always means a duality bracket
  or a safe discretisation evaluated in double precision.
* Prior art: no full text read; no systematic novelty search.
* The proved-lowered cells rest on Proposition F, which I re-derived and tested on finite chains but which no
  third party has refereed.

---

## Coordinator's note (2026-11-26, before publication as SCI-REV-0010)

*What the coordinator did with this report, so that the message claims no more than was done.*

1. **Read in full**; the message SCI-REV-0010 was compared with it number by number (the verdict table, the
   table of M1, the minor findings, §§3.4–3.5, §5, §8, §12).
2. **Re-derived:** both expansions in the proof of Proposition R10.1 (the cumulant expansion of
   `t ln E e^{−φ} − ln E e^{−tφ}`, where the third-order term has the opposite sign to the one first printed —
   corrected above; and `Σ_x(½π₊^t + ½π₋^t)^{1/t} = 1 − (1−t)u²Var f/2 + O(u³)`); Proposition R10.2 (the
   covariance of two nondecreasing functions); `S(0) = σ^{−1/2}` for the helix–coil chain at its midpoint, from
   the eigenvalues `1 ± σ^{1/2}` of the symmetrised transfer matrix; the explicit example of m2 by hand (the
   classes `{1101, 1011}` and `{0101}`, the values `2, 4` and `1`), including that the quantile convention of
   `r10_09b_trunc_example.py` is the one of the theory division's `y08` (level = the `(⌊q·|class|⌋ + 1)`-th
   value from the favourable side).
3. **Re-ran the theory division's own functions** (`ylib.py` at `658b77f`, scratch copy) through a driver of the
   coordinator's at two of the reversal cells: capacity bracket `/3 = 0.495806` at `(p, u) = (0.3, 3)` and
   `0.467509` at `(0.2, 3)`, cube `0.502282` (0.7 s).
4. **Computed with a third code** (`experiments/science/pi_inference/r10_reversal_check.py`, written from the
   definitions: integer height functions as vertices, Blahut–Arimoto with duality brackets): the exact
   capacities `a_n` of chains of one to four sites at `u = 1, 3, 4` and `p = 0.5, 0.3, 0.2, 0.1`.  Vertex counts
   `2, 6, 38, 990`; `a_4 = 0.572656` at `(0.1, 1)` as in Y and here; increments at `(0.3, 3)`:
   `0.458217, 0.462282, 0.462258` and at `(0.3, 4)`: `0.570383, 0.570894, 0.570907` — the digits of §3.5.
   **A caution the same log shows:** increments of short chains are not monotone and are no evidence of a
   direction by themselves — at `(0.1, 1)` the last increment is `0.9908` of the cube, although `a_∞ ≥ 1.05 ×`
   cube is proved there (Proposition I).  The proved cells rest on Proposition F, not on increments.
5. **Followed up the connection of §3.4 to addendum A17.8**: the constant `¼` of the variance bound can be
   replaced by the worst two-point split of the transition law, the bound is then an *equality* at every
   length for the uniform field on the symmetric two-state chain, and for two letters the Kearns–Saul
   inequality sharpens the bound on the moment generating function
   (`experiments/science/pi_inference/a17_8_sharp_constant_check.py`; addendum A17 (8), remark added).
6. **Not re-run by the coordinator:** every script of `experiments/science/ws_R10/`.  **Not re-derived by the
   coordinator:** Proposition F (the reviewer's re-derivation was read, and the chain-rule argument for the
   capacity form was followed step by step); Propositions G–J; the tilt-state discretisations.

