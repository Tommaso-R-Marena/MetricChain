# R29 — adversarial review with replication of Theorem 11.58e (theory division, export at `07cde81`)

*Science division, workstream R29, 2026-11-27.  An internal review by an AI agent — **not external peer review**.
Written under a wind-down order of the coordinator (hand-back within ten minutes): everything below is what was
established when the order came; unfinished items are marked **NOT FINISHED** with how to resume.  Kinds of
checking: **review** (re-derived on paper), **replication** (own code, nothing of theirs imported), **re-run** (their
scripts), **read only**.  Code and logs: `experiments/science/ws_R29/` (a log is cited only if it reached its last
line).  Notes with every step, prediction and own error: `experiments/science/ws_R29/NOTES.md`.*

## 0. Verdicts

| object | verdict | kind of checking |
|---|---|---|
| Proposition A13 (multi-rate sequences) | **proved, with two gaps of wording, closed here** (F2, F3): the cap line is below the *maximum* of two lines of the stated form, not below one; the base case for a start `c₀ = ā > a` is not the one of Proposition A8 | review |
| the certified tops (tables of 11.58e(f), A6b) | the three committed runs (`u = 1`: 80 levels; `u = 2, ½`: 40 levels; `K = 3000`) are **reproduced digit for digit and verified by an independent exact checker: 0 violations** — rigorous upper bounds of `τ_j` *given* Lemma A1, Corollary A4, Proposition A8 (re-derived).  The 400-level run (`K = 4000`): **NOT FINISHED** | re-run + replication |
| the code `z6_certified_tops.py` | **sound** on those runs, **with restrictions**: (i) its own final verdict "ALL CHECKS PASS" certifies nothing — 17 of 30 mutations that break a certificate, one of them gross, still end with it (F1); (ii) printed decimals are rounded to nearest, not upwards (F4); (iii) other slopes, tiny `K`, the 400-level run not verified by me | review + replication (mutation table, §3) |
| Proposition A12, `τ₂ = b₂` | (a)–(d) **proved as stated**.  The closed form "for the cube `τ₂ = a²/(a + x*)`" is **false as stated for `u > u₀ = 4.6535196185`** (counterexample `u = 5`); true and rigorously verified at `u = ½, 1, 2` (F5) | review + replication |
| the two numbers | `τ₂ = 0.500410018113·a` replicated (20 digits; rigorous enclosure).  `τ₃`: **mine `0.361184·a`, not `0.361189·a`** (theirs is above an upper bound of mine; their referee's `0.361184` agrees) (F6).  "Strictly better from `k = 3`" is a **computation**, [N] as they label it; in my replication with one-sided control on the `τ₃` side, margin `2.117·10⁻³·a`; not interval-certified (F7) | replication |
| the minimax step, 11.58e(a) / Lemma A1 | **proved as stated**; no gap found; could not be broken (1 067 exponent-level cases, 122 472 exactly evaluated levels; all controls fail as they must) | review + replication |
| Lemma A9′, Proposition A11′, Theorem Z‴ (small rates) | **proved as stated, given Lemma A10** (read, not re-derived) and the finite-`n` statements the theorem is conditional on; the range `C₄ ln n/√n ≤ g ≤ g₀` matches the hypotheses; geometric decay replicated at five rates (`u = 1`) | review + replication |
| Theorem 11.58e as a whole | as far as I went ((a), (e) equality, (f), small rates of (g)): **no error of substance**.  (b)–(d): **not re-derived** (rest on Q2's Lemma U and Proposition T, taken as given); one level of (b) checked numerically only.  Items 5 and 6 of the brief and the comparison with their three reviews: **NOT FINISHED** | — |

No critical finding.  One major finding (F1, about what the script's verdict is evidence of — not about its numbers).

## 1. The statements as I understand them (with implicit hypotheses)

Pair of the cube: `p_u = 1/(1+e^u)`, `θ = θ_na(e) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ e}`, `a = KL(p_u‖½)`, `J(t) = Λ(tu) − tΛ(u)`
(re-derived), `Σ(B, s) = sup_e [B − (1−s)θ(e)]/e = t′(1−s)/(1−t′)` with `J(t′)/(1−t′) = B/(1−s)` (re-derived; both forms agree
to `3·10⁻³⁸` in my code).  *Family*: `W : [0, b] → [0, 1]` convex, nondecreasing, continuous, `W(0) = 0`.

* **Minimax step.**  For families `(W, b)`, `(W′, b′)` with (S1) `b ≥ b′ ≥ sup{B ≤ b : Σ(B, W(B)) < ∞}` and (S2)
  `W′ ≤ Σ(·, W(·))` on `[0, b′]`, every `g > 0`: `inf_{0<φ<1} max_{B ≤ b, W(B) ≤ s ≤ 1} [(1−φ)B + (1−s)φθ(g/φ)] ≤ M_{W′,b′}(g)`.
  Implicit: (H0) `θ` convex, nonincreasing, `≥ 0`, `θ(0+) = a < ∞`; the infimum is in general *not attained* (it is
  approached as `φ → 1`), which is why the statement carries `+ η`.  My derivation gives more: the left side
  **equals** `sup{B − Σ(B, W(B))g : Σ < ∞}`.
* **A13.**  Any pair `(e′, ϑ)` with `ϑ ≥ θ(e′)` and any line `ℓ ≤ V` give a line `[B − ϑ(1 − ℓ(B))]/e′ ≤ Σ(B, V(B))` on
  `[0, c]`; a convex `V′ ≤ max(0, such lines)` with `V′(0) = 0`, `V′(c′) ≤ 1` and a top `c′ ≤ c` with `c′ = c` or
  `c′ + āV(c′) ≥ ā`, `ā ≥ a`, continue an admissible sequence.  For the cube **any** `ρ ∈ (0, 1)` gives a valid pair
  from upper bounds of `KL(ρ‖p_u)` and `KL(ρ‖½)` (`ρ` is feasible in the minimum): `ρ > p_u` is not needed.
* **A12.**  `τ(T) = inf_x a(x + T^♯(x))/(a + x)`; `τ(M_{W,b}) = max_B min(B, (1 − W(B))a) = b⁺(W, b)`; `θ^♯ = M_{W₁,a}`; hence
  `τ₂ = b₂` for every pair with infinite slope at zero.

## 2. Findings (line that decides it; replacement text)

**F1 (major — evidence, not numbers).  The script's verdict cannot fail for the errors it is meant to exclude.**
`z6_certified_tops.py` lines 320–323: `mono` is true by construction (`next_top` returns `≤ V.c`), `above` compares
with a floating `h`.  The only checks that can fail are `assert H.val_exact(c) <= 1`, the sign assert, and the exact
test in `next_top`.  Mutation study (§3): of 30 mutations, 2 are caught by the script (both put the cap above one at the top);
17 break a certificate and still end with "ALL CHECKS PASS" — among them every flipped rounding direction, and
**M18 (the two divergences swapped), which prints `c₂ = 0.055481623494 < τ₂ = 0.055517524915` and `c₃/a = 0.360741 < τ₃/a = 0.361184`
as "certified"** (its own comparison column is negative, `−1.4·10⁻³`, `−2.5·10⁻²`, `−4.1·10⁻²`, but is not part of the verdict).
So the validity of the tables rests on the code path, not on a check; my independent checker shows that code path
is right on the committed runs.  *Replacement* (Z_ADDENDUM A6b, after "computed in exact rational arithmetic"):
"The script's final line tests only monotonicity and `c_j > h`; the pairs and the rounding of the lines are valid by
construction and are not re-checked by the script.  [Add:] the script writes, for every stored line, its
certificate (rate, pair, parent line; for the cap line two witness lines), and a separate exact checker verifies
them — prototype: the science division's `r29lib.check_step`; and the verdict includes `c_j ≥ b_j − tol` against the
floating envelope tops (Corollary A4)."  Their harness XVI.11 ("eleven mutations, all caught") is not in my export
and was not assessed.

**F2 (minor).  A13 does not literally cover the cap line.**  Z_ADDENDUM line 267–268: "`V′` is a maximum of the zero
line and of lines that are below such lines".  The cap line (script lines 257–269) is below the maximum of *two*
such lines that meet at the tangent vertex, below neither alone; and "nondecreasing (the slopes … are positive)"
does not apply to lines that are merely *below* such lines.  The proof of (S2) needs only `V′ ≤ max(0, such lines)`.
*Replacement*: "…and `V′` is convex with `V′(0) = 0`, `V′(c′) ≤ 1` and `V′ ≤` the maximum of the zero line and of such
lines on `[0, c′]` (a convex nonnegative function that vanishes at 0 is nondecreasing)."  The cap is then covered:
a line through `(c′, 1)` that is below the hull at all its vertices is below the hull.

**F3 (minor).  Base case and start of the certified sequence.**  A6b line 281 cites "Lemma A1 and Proposition A8", but
A8 is for the envelope sequence from `b₀ = a`; the script starts at `c₀ = ā = up(a) > a`, and 11.58e(d) asks for
`b₀ ≤ a`.  *Replacement*: "by Corollary A4 (start `V₀ ≡ 0`, `c₀ = ā ≥ a = b₀`) `c_j ≥ b_j` and `V_j ≤ W_j` on `[0, b_j]`, hence by
Proposition A8 `τ_j ≤ b_j ≤ c_j` and `T_j ≤ M_{W_j,b_j} ≤ M_{V_j,c_j}`"; and in (d) "`b₀ ≤ a`" → "a base family of flat type `b₀`"
if the certified tops are to be used at finite `n`.

**F4 (minor).  Printed certified numbers are rounded to nearest.**  Script line 318 (`"%.12f"`, `"%.9f"`); the ratio is
rounded up as a double (line 308) and then printed to nearest.  All entries of the committed tables stay above
the true envelope tops (smallest margin I computed: `2.7·10⁻⁸` of `b_j − h`, against `5·10⁻¹³` of print rounding), so no
number is wrong.  *Replacement*: print with a ceiling at the last digit.

**F5 (minor; false as stated for large slopes).**  Z_ADDENDUM line 227 and 11.58e(e) ("for the cube `a²/(a + x*)`,
`θ_na(x*) = a − x*`").  `τ₂ = min_x a·max(a, x + θ(x))/(a + x)`, and the minimum is at `x*` iff `θ′(x*) ≥ −x*/(a + x*)`.
That holds at `u = ½, 1, 2` (verified with rigorous intervals) and **fails for `u > u₀ = 4.6535196185`**: at `u = 5` the
level formula gives `0.602893·a`, the closed form `0.604053·a`; at `u = 10`, `0.75971·a` against `0.88596·a`.  `τ₂ = b₂` is
not affected.  *Replacement*: "for the cube with `u ≤ 4.6535` (where `θ′(x*) ≥ −x*/(a + x*)`): `a²/(a + x*)`; in general
`τ₂ = min_x a·max(a, x + θ_na(x))/(a + x)`."  (`log_i1_tau2_01.txt`.)

**F6 (minor; numbers).**  Z_ADDENDUM table after line 235 and `out_z7_exactness_u1.txt`: `τ₃ = 0.361189·a`.  Mine:
`τ₃ = a·τ₂/(a + x₂*) = 0.0400711983953 = 0.361183773·a`, `x₂* = 0.042765837436` the first root of `x + T₂(x) = τ₂`, and an
upper bound that does not depend on any minimisation being converged, `0.361184025·a`.  Their minimiser of
`R[θ]` (a zooming grid) stalls: at their own 16 table rates my values are lower by up to `2.9·10⁻⁶` (`0.7ε*`), nowhere
higher.  `b₃ − τ₃ = 2.117·10⁻³·a` (theirs `2.112·10⁻³`).  `(M₂ − T₂)/a = −1.98·10⁻⁹` at `0.95ε*` in their output is noise:
there `T₂ = M₂` exactly (to `5·10⁻²⁰` in 30 digits) — the maximising line lies on the uncapped orbit part, where the
lower bound of Theorem 11.53a(c) meets the upper bound.  *Replacement*: `0.361184·a`, `2.117·10⁻³·a`; `τ(M₂) = b₃ = 0.363300650·a`
(their grid value `0.363303` is `2·10⁻⁶` high; mine agrees to `2·10⁻¹⁶·a`).  (`log_i2_tau3_u1_03.txt`.)

**F7 (minor; status of a claim).**  "From the third level on the recursion is strictly better": a floating-point
computation whose errors have no common direction in their script (interpolation of `T₂`, a grid for the supremum,
a stalling minimiser).  In my replication the `τ₃` side is bounded one-sidedly (every `(φ, β)` bounds `T₂` from
above; `T₂` nonincreasing and `≤ τ₂`); the `b₃` side is a 30-digit semi-analytic value, not an interval.  Margin
`2.1·10⁻³·a`, four orders above any error I can see.  Still [N]; an interval proof is within reach, not done.

**Observations (no change needed).**  (o1) mpmath's `float(mpf)` truncates, so `up()` returns the least double above
the interval end (margins `0.00` ulp); valid in every sign case.  (o2) `assert e.a > 0, "rho must be above p_u"` tests
`ρ ≠ p_u` only; validity needs no more.  (o3) The four `nextafter` steps on the stored lines cover at most three
relative rounding errors: least margins observed `2.20` ulp (slope), `1.83` ulp (beta) over 278 704 lines.  (o4) A cap
line with nonpositive slope would be dropped silently by `_hull` (cannot occur: `m ≥ 1/c`).

## 3. Runs (predictions and controls in `NOTES.md`)

| run | what | result | log |
|---|---|---|---|
| re-run | `z6 1 6 400` in place | ALL CHECKS PASS, 0.9 s; nothing written into the export | `log_rerun_z6_u1_J6_K400.txt` |
| replication | my library: own integer interval arithmetic vs mpmath (1 308 containments), exact hull (11 096 comparisons), slope map two ways | all pass; 4 controls fail as they must | `log_i1_selftest_02.txt` |
| replication | `τ₂`: closed form, direct minimisation, brute force, rigorous enclosure; scan over `u` | P1 confirmed; `u₀ = 4.6535196185` | `log_i1_tau2_01.txt` |
| replication | my certified tops (exact rationals, own intervals, other points and rates), `u = 1`, 6 levels, `K = 200` | checker 0 violations; 841 pairs cross-checked; 5/5 controls rejected; `c_j/a ≤ 0.500414264, 0.363304343, 0.312794265, 0.291389012, 0.281339442`; all `≥ b_j`; `u = 2, ½` **NOT run** | `log_i1_mytops_u1_J6_K200_01.txt` |
| re-run + replication | their unmodified `z6` under a shadow + my exact checker | `u = 1`, 80 levels, `K = 3000`: 257 394 stored / 278 704 generated lines, 0 violations, 0 hull mismatches, 0 of 80 tops differ from the committed output, none below the semi-analytic envelope top; `u = 2`, `u = ½` (40 levels): the same, 0 of 40 differ | `log_i1_verify_theirs_u1_J80_K3000_01.txt`, `…_u2_J40_K3000_01.txt`, `…_u0.5_J40_K3000_02.txt` |
| replication | mutation study, `u = 1`, 6 levels, `K = 400` | table below | `log_i1_mutations_u1_J6_K400_01.txt`, `mutants/` |
| replication | `T₂`, `τ₃`, `τ(M₂)`, bounds | F6 | `log_i2_tau3_u1_03.txt` |
| replication | minimax step, exponent level: 97 convex families × 11 rates (`10⁻⁶ε*`…`1.5ε*`; envelope curves, flat, chord to the cap, lines at the cap, two lines crossing at the top, random) | 0 violations; `|LHS − RHS| ≤ 8.8·10⁻¹³·a`; controls: non-convex families 147 of 160 fail (up to `0.293·a`), two steps for one 635 of 1 067 | `log_i3_minimax_u1_03.txt` |
| replication (+ their evaluators for Part 1) | one level of Lemma Z2 exactly, my evaluator from the statement of Theorem 11.56 | Part 1: 2 548 levels, mine vs theirs `≤ 1.2·10⁻¹²`, integer constants identical.  Part 2: 18 families (5 envelope, 13 adversarial) × 7 accuracies × `d = 300, 1000, 3000`: 122 472 levels, **0 violations** of accuracy, (U∞), the exponent step, the type; least slacks `7.67`, `1.22`, `15.6` nats; controls fail (362; 127; non-convex 6 of 24) | `log_i35_onelevel_u1_01.txt` |
| replication | small rates, `u = 1`, 400 levels | Lemma A9: 0 violations on 400 `η`; Lemma A9′ holds for **all** `η < h` on the grid (no `η₀` needed at `u = 1`); defect decay ratio vs `κ_g`: `0.951242…0.951257` vs `0.951251` (`g = 0.05h`), `0.904882…0.904914` vs `0.904908` (`0.1h`), `0.7777…0.7790` vs `0.779025` (`0.25h`), `0.02h` still converging; proved rate `μ_g = 1/(1 + g/(48h))` holds with `g·k₂/h = 0.2 … 2.0` (bounded); 5/5 controls fail | `log_i4_smallrates_u1_K400_02.txt` |

**Mutation table** (own verdict of the mutated script / my exact checker).  *Caught by the script* (assert "cap
failed"): M11 cap intercept rounded down, M13 cap at 1.001.  *Not caught by the script ("ALL CHECKS PASS"), rejected
by my checker*: M01 `up()` towards −∞; M03 `up()` without `nextafter`; M04 `e′ := dn`; M05 `ϑ := dn`; M06 midpoints
(pairs truly invalid in 40 digits in each of these); M22 `θ` bound at `ρ(1+10⁻⁷)`; M23 rate at `ρ(1−10⁻⁷)`; M18 divergences
swapped (3 tops below the true envelope top); M07 slope rounded up; M08 beta rounded down; M09 no rounding steps;
M09b one step; M21 parent line `×(1+10⁻⁹)`; M10 cap slope rounded down; M12 tangent from `(c(1+10⁻⁶), 1)`; M15 top with a
lower bound of `a`; M17 top unverified from the low end.  *Not caught and valid or equivalent on this input*: M02
(`x.a` for `x.b`), M19 (`p_u` as a double: harmless only because that double is below `p_u`), M20 (12-digit intervals:
valid — specificity control), M09c (two steps), M14 (cap slope `min`: negative slope, line dropped, tops `2·10⁻³` worse),
M16, M26 (top verification: not exercised), M24 (hull reversed: one line per level, valid and useless), M27, M28,
M32 (`ρ = ½` branch not exercised).  Baseline: passes both.

## 4. Assumption table and the size paragraph (Item 6) — **PARTLY DONE**

| hypothesis of 11.58e | status | basis |
|---|---|---|
| `θ` convex, nonincreasing, `θ(0+) < ∞` | essential for (a) (Sion needs quasi-convexity in `e`; the one-line case needs tangent lines) | review |
| `W_j` convex | **removal makes (a) false**: for non-convex families the minimax value is that of the convex hull and exceeds the line-by-line value (147 of 160 of my cases, by up to `0.293·a`; 6 of 24 at `d = 300`) | replication |
| `W_j` nondecreasing | used by the proof (the image line `(B″, s)`, `B″ ≤ B`, must stay in the family); "false without" is their claim | review / read only |
| `W_j` continuous on a closed interval | needed only by the proof (compactness for Sion) | review |
| `W_j(0) = 0` (zero line), values `≤ 1` | zero line: needed at finite `n` (Lemma Z2(iii); "false without" is their claim).  Slopes `≤ 1`: essential for (b) — the shift by `X₀(d)` costs `X₀(d)` only then | read only / review |
| (S1), (S2) | essential: claiming two steps for one fails (635 of 1 067; 127 of 378) | replication |
| `W₀ ≡ 0`, `b₀ ≤ a` | convenience; `b₀ = ā ≥ a` serves as well (F3) | review |
| infinite slope of `θ` at zero | convenience for `b⁺`; the direction used by A13 holds without it | review |
| (H1), `J` twice differentiable at `L` | changes the rate (`1/k²`; with a kink `1/k`) | read only |
| `k ≤ n^{1/2}`, `n ≥ n₀(u, δ)`, uniform cube, the level theorem | needed by the proofs of (b)–(d); not effective | read only |
| (g), small rates: `C₄ ln n/√n ≤ g ≤ g₀` | lower end from `k ≤ √n` (proof); upper end from `m(g) ≥ ϑg²/4`, `g ≤ 48h` (at `u = 1` Lemma A9′ itself holds for every `η < h`) | review + replication |

*Size.*  By **their** numbers (read only): as a formula the bound is above the non-adaptive `n·a` at `n = 10⁴`
(`1 025` against `818` nats above `n·h`) and below from `n ≈ 1.5·10⁴`–`3·10⁴`; their exact nest (two envelope levels over the
real base) certifies `e^{889.66}` at `n = 12 000` (`n·a = 1 331`, `n·h = 350`) and `e^{2817.79}` at `n = 50 000` (`n·a = 5 547`).
`e^{889.66} ≈ 10^{386}`: at every size where the bound is below the non-adaptive cost it certifies a number of
evaluations nobody can make, so the theorem is a complexity law only; the reachable-size separation of the
programme is remark (1a) of the theory report (`n = 1 400`), not this theorem.  **By my numbers: NOT FINISHED** —
`r29_i6_crossover.py` (my exact non-adaptive lower bound of Theorem 11.45(b)) is written and was never run.

## 5. Comparison with their three reviews — **NOT FINISHED**

`read_only_after_your_own_report/` was **not opened** (not even listed): the wind-down order came while this
report was first being drafted.  To do: read the three reviews and compare with §§0–2.

## 6. Not checked; not finished; own errors; files

**NOT FINISHED, how to resume** (all from `experiments/science/ws_R29/`, `python3 -B`, `OMP_NUM_THREADS=1`):
* Item 5 (nest): nothing run.  `python3 -B r29_wrap.py <export>/experiments/workstreams/Z/z3_nest.py 2.0 0.02 3000 2 env sat`
  (13 s by their log; compare with `out_z3_nest_env_u2_N3000_k2.txt`), `… 1.0 0.003 12000 2 env real` (28 s); then
  `r29_i5_level_of_nest.py 2 3000` (written, **never run, untested**; expected under 2 min).
* Item 6 numbers: `r29_i6_crossover.py 1 12000:889.66 50000:2817.79` (written, never run; under 1 min).
* Item 1: my tops at `u = 2, ½`: `r29_i1_mytops.py 2 6 200`, `… 1/2 6 200` (7 s each).  The 400-level run:
  `R29_STATE_OUT=s100.npz python3 -B r29_i1_verify_theirs.py 1 100 4000`, then `R29_J0=101 R29_STATE_IN=s100.npz
  R29_STATE_OUT=s200.npz … 1 200 4000`, and so on (chunk support written, **untested**; about 4 s per level).
  Odd inputs (`u = 0.3`, `8`; `K < 10`), mutations at other slopes: not run.
* Section 5.

**Not checked.**  (b)–(d) of the theorem, `c_Z`, `n₀`, the chain (Proposition T), Lemma U's proof; Theorem 11.56
itself; Sion's theorem and Theorem 11.53a(c), Lemma M (used as quoted; Lemma M's limit `β → 0` re-derived);
`τ_j` for `j ≥ 4` (compared with envelope tops only); slopes other than `u = 1` for Items 2–4; (g) at fixed rates
(Lemma A10 read, not re-derived); every formula table.  **Used without checking**: Q2's `ℓ₀`, `q` (Lemma U); the
constants `K`, `m_max` of Theorem 11.56 from their `qlib.level_consts` (the quoted statement has only `K = O(·)`).

**Own errors** (all in `NOTES.md`).  (1) a run started with `u = "1/2"` (crash).  (2) My first two minimisers of
`R[θ]` missed minima (found because their values were *lower* than mine); the third is at or below theirs
everywhere.  (3) Three bugs in my minimax test (range of `φ` cut at `1 − 10⁻⁷`; a Newton slope map that could
overshoot and return a huge negative slope; a duplicated grid point) produced false "violations" in two discarded
runs.  (4) Two of my controls could not fail as first written (τ₃ script c3; small-rates control B) and were
replaced.  (5) A wrong stopping criterion crashed one run.  Discarded logs (not cited): `log_i2_tau3_u1_01/02`,
`log_i3_minimax_u1_01/02`, `log_i4_smallrates_u1_K400_01`, `log_i1_verify_theirs_u0.5_J40_K3000_01`.

**Predictions missed.**  P5: I expected the script to catch M14, M18 and perhaps M24; it caught none of them.
P3: pair margins are `0.00` ulp, not `≥ 0.5` (truncation).  P2: my sampling is worse than predicted at level 2.
P4: their `τ₃` is not reproduced in the sixth digit.  P1, P6, P7, P8 held.

**Tool actions declined.**  One: a Bash call beginning with a foreground `sleep 25` was blocked by the harness;
not worked around.  **Web addresses opened:** none.  **Processes left running:** none.

**Files** (`experiments/science/ws_R29/`): `NOTES.md`; libraries `r29lib.py` (intervals, exact hull, builder,
checker), `r29env.py` (semi-analytic envelope), `r29rec.py` (level recursion), `r29fam.py`, `r29level.py` (one-level
evaluator), `r29_wrap.py`; scripts `r29_i1_selftest.py`, `r29_i1_tau2.py`, `r29_i1_mytops.py`, `r29_i1_verify_theirs.py`,
`r29_i1_mutations.py`, `r29_i1_mutworker.py`, `r29_i2_tau3.py`, `r29_i3_minimax.py`, `r29_i35_onelevel.py`,
`r29_i4_smallrates.py`, and — written, never run — `r29_i5_level_of_nest.py`, `r29_i6_crossover.py`; logs `log_*.txt`;
`mutants/` (generated mutant sources, marked as not the theory division's files, and their outputs).

---

## Coordinator's note (27 November 2026; written under the owner's consolidation directive D-5)

*This workstream was wound down on my order*, sent at about 01:01 UTC when the directive arrived; it had run
for an hour and handed back at about 01:06 UTC with the items above marked NOT FINISHED.  It reported one
declined tool action — a foreground wait blocked by the harness, which it did not work around and which
nothing was asked of me about.  It opened no web address.

*Read by me:* this report, in full.  **Checked by me: nothing.**  Under the directive I did not re-run or
re-derive any of its findings; `NOTES.md`, the scripts and the logs were not opened.  Every statement above is
therefore **one referee's finding** — replication with its own exact code where it says so — and is sent to the
theory division with that label (SCI-REV-0030).  The directory `ws_R29/mutants/` (124 generated files: mutated
copies of the theory division's script and their outputs) is not tracked — it is another division's code in
altered form and is regenerable with `r29_i1_mutations.py` from a read-only export; the mutation log
(`log_i1_mutations_u1_J6_K400_01.txt`) is tracked.

*What I would check first if this is resumed* (cheapest and most consequential): F5 — the closed form of `τ₂`
at `u = 5` is a one-line evaluation against the level formula; F1's mutant M18 — one run of the mutated script
shows whether a top below the true value is printed as certified; F6 — the upper bound `0.361184025·a` that
"does not depend on any minimisation".

