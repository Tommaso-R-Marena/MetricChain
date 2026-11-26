# Referee report R12 — workstream Q: the sub-exponential term of the adaptive exponent without a hint

*Independent referee, 2026-11-26.  Under review: `docs/workstreams/Q_REPORT.md` (878 lines, as
delivered, unrefereed).  Brief: `docs/reviews/R12_brief.md`.  Own code and stored outputs:
`experiments/reviews/R12/` (§6 below).  Nothing in `experiments/workstreams/Q/` was imported or
run; from the author's stored outputs I compared only numbers that are also printed in the
report (typed into my scripts).  The earlier referee's `experiments/reviews/R8/r8_flat.py` was
used for one cross-check of my evaluator.  No existing file was edited, no state-changing git
command was run, `lake` and the audit script were not run, nothing was delegated.*

Labels used throughout: **[R]** re-derived by me on paper from the definitions of
`K_REPORT.md` §2.1–2.2 and the text of the report; **[N]** tested numerically with my own code
(sizes and counts given); **[–]** not checked.  Line numbers are those of `Q_REPORT.md` **as
delivered** (878 lines); the coordinator has since put a repository note of 42 lines at its
head, so add 42 for the file as it stands now.

*Note on versions.*  A draft of this report lay in this file while my last runs were
still going, and the coordinator integrated it (repository note and errata of `Q_REPORT.md`,
Theorem 11.58a of the theory report, `DEAD_ENDS.md` D63) before this final version existed.
Nothing of substance changed between the two; the differences are: (i) the count of checks
(the draft said "about 55 million"; the finished runs give about 220 million node checks of
the nested design); (ii) the condition under which the lower bound of finding m1 is
*proved* — the draft said "`k*(ε) ≤ n/2`", the argument needs one more condition or a slightly
larger constant, see m1; the statement as integrated is confirmed numerically; (iii) two
numbers of mine that were wrong in the draft and that nobody quoted (O4; the ratio
`Λ̄_T/Λ̄_0` in §2.5); (iv) the table of §2.6 and the timings of §6.

---

## 0. Verdict

**The main claim survives, with the constants as stated.**  For every `u > 0`, `ε > 0`,
`0 < δ < 1` there is `C` with `N(n; ε, δ) ≤ exp(n·h + C·√(n ln n))` for all `n ≥ 2`; the design of
Theorem Q8 costs at most `exp(n·B_M + 𝓔_M)` with `𝓔_M` as in (5.2); and
`limsup (ln N − nh)/√(n ln n) ≤ C_*(u) = 2√((1 + r̄)c₁(a/h + 4))` — **given** Theorem 11.56 (= K1,
paper proof, refereed R8) *with its abort test made before every query* (finding m2), Lemma
11.55(a),(b), Proposition 11.57(a), Harper's theorem, the binomial median, Chernoff–Hoeffding,
and the epoch arithmetic of `RateFull.lean`.

**No Major finding.**  I re-derived every new statement of the report (list in §5) and found
no false statement and no proof step that fails.  In the numerical checks with independent
code — exact arithmetic for the two closing-radius lemmas (0.9 million radii and cases),
exact constants of Theorem K1 for the two inductive steps (523 000 levels with worst-case
inner families, far outside the epoch schedule), the nested design evaluated exactly for
up to seven levels (220 million node checks; awkward sizes `n = 2 … 200`, the first sizes at
which each kind of level is built, and extreme `ε`, `δ`, `u` included) — **no inequality of the
report is violated**, and every number of its tables that I recomputed is reproduced (two
auxiliary numbers excepted: m4).

Minor findings (§1): two touch the *statement* — the lower bound quoted in Theorem Q(c)
needs `δ < ½` and is not in the theory report in the form used (m1), and the nesting needs the
abort rule in a form that the report does not state and that Theorem 11.56 of the theory
report did not have when the brief was written (m2; the result is not affected) — the
others are wording and presentation (m3–m6).

What this verdict does **not** cover: the truth of Theorem 11.56 in the regime in which the
report uses it (never simulated there), and the composition at the depth at which the
theorem says something new, which no exact evaluation reaches (§4).

---

## 1. Findings by severity

### Major

None.

### Minor

**m1.  Theorem Q(c), lines 52–54, and §1.2, line 149: the lower bound `n·h − O(ln n) ≤ ln N` is
stated for `0 < δ < 1`, labelled "[V, quoted]", and attributed to "Theorem 11.25(a),(d)" — it
needs `δ < ½`, and neither part of Theorem 11.25 states it in this form.**
Theorem 11.25(a) is the finite inequality `E|Q(0)| ≥ (1 − 2δ)·2ⁿ/|B(n, k)|` whenever `ε < Δ_k`
(machine-checked); it is void for `δ ≥ ½`.  Theorem 11.25(d) is labelled [P] in the theory
report and gives the *exponent* (`lim n⁻¹ ln`), i.e. `n·h − o(n)`; the remark "up to a factor
polynomial in `n`" in 11.25(c) compares the hinted upper and lower bounds with each other, not
with `e^{nh}`.  The missing two lines **[R]**: for `k ≥ p_u n` the binomial median gives
`2^{-n}E_k(n) ≥ ½e^{u(k+1) − nΛ₁} − 1`, so `Δ_k > ε` as soon as `u(k+1) ≥ nΛ₁ + ε + ln 2`; hence
`k*(ε) < ρ_h n + (ε + ln 2)/u`, and with `|B(n,k)| ≤ e^{nH(k/n)}` (`k ≤ n/2`) and the concavity of `H`

    ln N(n; ε, δ)  ≥  n·h − c₀·ln((1−ρ_h)/ρ_h) + ln(1 − 2δ),        c₀ = (ε + ln 2)/u,

for `δ < ½` and every `n` with `k*(ε) ≤ n/2`, **provided** the radius of the argument,
`⌈ρ_h n + c₀ − 1⌉`, is at least `p_u n` (the median step) — which holds whenever
`(ρ_h − p_u)·n ≥ 1 − c₀`, in particular whenever `ε + ln 2 ≥ u` or `n ≥ 1/(ρ_h − p_u)`.  For the
remaining small `n` the same argument with the radius `max{⌈ρ_h n + c₀ − 1⌉, ⌈p_u n⌉}` gives the
bound with `max{1, c₀}` in place of `c₀` **[R]**.  (The draft of this report, and Theorem
11.58a(c) as integrated from it, say "every `n` with `k*(ε) ≤ n/2`" without the proviso.  That
is *numerically* true: `u ∈ {0.3, …, 12}`, `n = 2 … 200`, `ε ∈ {10⁻³, …, 20}`, 19 839 cases with
`k* ≤ n/2`, among them the 255 in which the proviso fails — no violation, least slack `0.60`
**[N]**; but what the three lines *prove* there is the bound with `max{1, c₀}`.)

So the truth is better than quoted: `n·h − O(1)` for fixed `ε` and `δ < ½`.  **[N]**
(`r12_06`, part A: `u ∈ {½, 1, 2}`, `ε ∈ {0.01, 0.1, 1, 10}`, `n ≤ 256 000`, no violation of the
displayed bound; in fact `ln[(1−2δ)2ⁿ/|B(n,k*)|] − nh` is *positive* and grows like `½ ln n`:
`0.58, 2.55, 4.07, 5.22` at `n = 10, 10³, 1.6·10⁴, 2.56·10⁵` for `u = 1`, `ε = 1`, `δ = 0.05`.)
*Repaired statement:* "for `0 < δ < ½`: `n·h − O(1) ≤ ln N(n; ε, δ) ≤ n·h + O(√(n ln n))`
[lower bound: Theorem 11.25(a) (machine-checked) and the lines above (paper)]".

**m2.  §1.2 (T), lines 132–135, and the last line of the proof of Theorem Q8 (line 533): "the
cost bound holding in every run (abort rule)" — the abort rule that the nesting needs is
not stated, and the wording of the theory report does not give it.  The result is not
affected.**  This is the known issue of the brief, carried through **[R]**:

* *What is needed.*  Rule (P): a level keeps a counter in which each of its own queries (the
  reference point, the trivial bracket of a new outer point) counts `1` and each call of `I_l`
  counts its **certified** bound `C_l`, whatever the call actually uses; **before every
  query and before every inner call** it tests that the counter stays `≤ C_max`, and
  otherwise returns the trivial bracket.  (This is step 3 of `K_REPORT.md` §2.2 read with its
  erratum (m1) and applied to the point queries as well; it is also the abort rule as
  Theorem 11.52 in §11.18 of the theory report words it — "before every query — the one
  query that gives a new outer point its trivial bracket, and every call of an inner
  procedure, counted with its cost bound".  When the brief was written the parenthesis of
  Theorem 11.56 said "before every inner call"; the coordinator has since changed it to
  rule (P), at the twenty-second checkpoint.)
* *Under (P) the nesting argument of Q is exact.*  Induction over the levels: the base
  procedure makes `2M` (or `2^d`) queries in every run; if every `I_l` makes at most `C_l`
  queries in every run, then actual queries `≤` counter `≤ C_max` in every run.  On the good
  event the test never fires, because claim (vi) of Theorem K1 bounds exactly this counter
  (each call counted with `C_l`) by `1 + M̄ + Σ_l min{M̄, (J+1)cnt(x_{l−1})}·C_l ≤ C_max − M̄`; so the
  failure probability is unchanged.  A `k`-level run *is* an inner procedure of cost exactly
  its certified bound, as the report assumes, and `N(n; ε, δ)` (cost in every run) is what is
  bounded.
* *Under the earlier wording of Theorem 11.56* ("before every inner call the algorithm checks
  that the call does not take the number of queries beyond `C_max`") the point queries made
  after the last tested call are not tested: one level can make up to `C_max + M̄ ≤ (3/2)C_max`
  queries (`≤ M̄` points in every run, by claim (iv), which holds off the good event).  Nested:
  if the inner procedures can overrun their certified bounds by a factor `ρ`, the level
  overruns by at most `ρ + ½`; a nest of `k` levels by at most `1 + (k−1)/2`.  So even with that
  wording `ln(cost)` grows by at most `ln(1 + k_M/2)` in all: nothing changes in Theorem Q(b),(c),
  and (a) would lose `ln(1 + k_M/2)` nats.
*Repair:* state rule (P) in (T) (one sentence) and cite it in the proof of Theorem Q8.  (In
the theory report this is now done.)

**m3.  §0, line 59, and §7.4(i), line 781: "below the non-adaptive exponent `n·a` from `n ≈ 3·10⁴`
on".**  Recomputed from (5.2) (`u = 1`, `ε = 1`, `δ = 0.05`, best `M`, 200 sizes per decade): the
bound is first below `n·a` at `n ≈ 2.07·10⁴` and stays below from there on (last size not
below: `20 417`).  The sentence is true as written but the crossover is at `2.1·10⁴`, not
`3·10⁴` **[N]** (`r12_04`, part D).

**m4.  §7.4(v), lines 788–789: the "closed form of Theorem Q9(b)" numbers `1.72, 0.655` (at
`n = 6.4·10⁴, 10⁶`) are not the closed form with the `M` of the proof.**  With
`M = max{m : k_m ≤ k†}` as in the proof of Theorem Q9(b) (`M = 9, 14, 21, 29`) I get
`1.813, 0.663, 0.3055, 0.2673` (in units of `na`); the report's `1.72, 0.655, 0.305, 0.2673` are close
to a variant in which `C₁`, `ℓ_D`, `ℓ_B` are taken at the best `M` of the table
(`1.724, 0.656, 0.3054, 0.2673`).  Harmless (both are far above (5.2), which is what the sentence says), but the two
numbers are not what the theorem states **[N]** (`r12_04`, part E).

**m5.  Corollary Q4a (lines 254–263) against §7.1, part C (lines 668–673).**  The column "`Err`
proved (2.3)" (`107.89, 151.65, 236.30, 402.74`) is computed with the *refined* bound of Lemma Q3,
whereas Corollary Q4a is stated with `c_π = c̄_π` (which gives `143.47, 161.56, 246.22, 412.66`).
Both are proved and both hold; the table and the statement should use the same one **[N]**
(`r12_07`).

**m6.  Wording that says more than is proved, or less than is needed.**
(a) Line 89 and line 657: "proved: `u·√((n_o/2)·ln(…))`", "`1.83·√n_o` proved".  That is the leading
term of Lemma Q3, not a bound: the proved bound at `u = 1`, `θ = η = 0.05` is
`3.64, 2.76, 2.31, 2.08` times `√n_o` at `n_o = 500 … 32 000` (the report's own column), and the leading constant
alone is exceeded by the measured value at other parameters (`u = ½`, `θ = η = 10⁻³`, `m = 500`:
measured `1.245·√m`, leading constant `1.067`) **[N]** (`r12_02`, part B).
(b) Lemma Q4(b), line 230: the hypothesis "`ν₁ ≥ 1`" should read "`(1−η)ν₀ ≥ 1`" (the statement
is about `r†`, which depends on `ν₀`; this is what the proof uses).
(c) Theorem Q(c) / Theorem Q9(c): `C(u, ε, δ)` and `n₀` are not explicit, and `C` is **not** `C_*`:
see observation O1 — when the sentence of the theory report is rewritten, `C_*` may be
quoted for the limsup only.

### Observations

**O1.  How large is `C`?  [N]** (`r12_06`, part C; formula (5.2) or enumeration, whichever is
smaller; every `n ≤ 300`, then a grid up to `10^{12}`.)  `sup_n (bound − nh)/√(n ln n)`:

| `u` | `ε` | `δ` | sup of the ratio | attained at | ratio at `n = 10^{12}` | `C_*` |
|---|---|---|---|---|---|---|
| 1 | 1 | 0.05 | 3.77 | `n = 16 788` (`M = 2`) | 2.41 | 8.64 |
| ½ | 1 | 0.05 | 2.77 | `n = 69` (enumeration) | 1.17 | 4.65 |
| 2 | 1 | 0.05 | 8.74 | `n = 8 913` (`M = 1`) | 4.59 | 13.5 |
| 1 | 0.01 | 0.05 | 4.80 | `n = 299` (`M = 0`) | 2.69 | 8.64 |
| 1 | 1 | `10⁻⁹` | 3.77 | `n = 16 788` | 2.41 | 8.64 |
| 4 | 1 | 0.05 | 32.2 | `n = 56 234` (`M = 1`) | 8.54 | 14.8 |

So on this range `C = 3.8` serves at `u = 1`, `ε = 1`, `δ = 0.05`, while at `u = 4` the constant of
"for all `n ≥ 2`" is above `32 > C_*`: the error terms carry factors of order `1/p_u² ≈ e^{2u}`
(through `m*(ℓ)·H(p_u)` in `c̄_π`), and at `u = 4` the bound (5.2) beats enumeration only from
`n ≈ 5.6·10⁴`.
**O2.  `C_*` is a valid but loose limsup.  [N]**  Beyond `10^{12}` (closed form of Proposition
Q9a, minimised over `M`, `n` up to `10^{150}`) the ratio keeps decreasing towards
`≈ 2√((a−h)(a/h+4))` (`0.85, 1.60, 2.61` for `u = ½, 1, 2`): `0.99, 1.92, 3.31` at `n = 10^{150}`.  This
agrees with the report's heuristic remark (1) of §6.1 and confirms that `C_*` overstates the
method by a factor of about five (`r12_04`, part F).
**O3.**  `ℓ_S − (a/h + 4)·ln n` is `31, 39, 60` nats at `u = ½, 1, 2` (`δ = 0.05`): the "`O(1)`" of
Proposition Q9a is as large as the logarithmic term up to `n ≈ 10³–10⁴`.
**O4.**  In every nest I evaluated, the top drop chooses "no shift" or the pass-through; a
level *with* shift is built and checked wherever it is defined (153 of them in the
five-level nest at `n = 8000`, `u = 1`; none is defined at `u = 4`, `n ≤ 2000`) but it is never
the cheapest at the top.  The shift is a device of the proof of Proposition Q7, as the
report says.
**O5.**  Both steps use `x_L = b` exactly (slope step: `x_L = b = 1`; drop: `x_L = b = β`).  In exact
arithmetic this is covered by Theorem K1; an implementation meets the tie of erratum (m10)
of `K_REPORT.md` at every level.
**O6.**  Least slack of the induction inequality: I find `34.5 … 42.5` nats at `u = 1`
(`37.2` already for five levels at `n = 1000`), the report says `39–57` for up to five levels
(line 749) and `34–56` for seven (line 745).  My count includes the base nodes and the
"proof" variant; there is no violation either way.
**O7.**  The lower bound is in fact `n·h + ½ ln n − O(1)` numerically (m1), so the gap that
remains is between `n·h + Θ(ln n)` and `n·h + O(√(n ln n))`.

---

## 2. The seven items of the brief

### 2.1 Lemma Q4 (closing radius at an extensive threshold) — correct [R, N]

*Re-derivation* from the definitions (`Γ̃(0) = e^u − 1`, `Γ̃(r) = E_r(m)/|B(m,r−1)|`; `[N]`, `[P]`, `r†`,
`π†` as in `K_REPORT.md` §2.1).  (a) For `1 ≤ r ≤ p_u(m+1)` the ratios `C(m,i−1)/C(m,i) = i/(m−i+1)`
are `≤ e^{-u}` up to `i = r`, so `E_r ≤ (r+1)e^u C(m,r)` and `Γ̃(r) ≤ e^u(r+1)(m−r+1)/r ≤ 2e^u m`
(Lemma K.4(a), re-derived).  For `p_u(m+1) < r ≤ min(m, ρ_e m + 1)`:
`E_r ≤ e^{u(r+1)}(1+e^{-u})^m`, `|B(m,r−1)| ≥ (m+1)^{-1}e^{mH(ρ′)}`, `ρ′ = (r−1)/m`, and (F1) give
`Γ̃(r) ≤ (m+1)e^{2u}e^{m·KL(ρ′‖p_u)}`; `ρ′ ≤ ρ_e` gives `KL ≤ e` if `ρ′ ≥ p_u`, and
`p_u − (1−p_u)/m < ρ′ < p_u` gives `m·KL ≤ m·χ² < e^u/m ≤ e^u`.  (b) With
`θ ≥ c_η^{-1}(m+1)e^{2u+e^u+me}`: `Γ̃(r′)/c_η ≤ θ` for all `r′ ≤ r₁ := min{m−1, ⌊ρ_e m⌋+1}`, so [P] holds through
its first entry and [N] because `(1−η)ν₀ ≥ 1`; and `|B(m,r₁)| ≥ 2^{m−1}` if `r₁ = m−1` or `r₁ > m/2`,
otherwise `≥ C(m,r₁) ≥ (m+1)^{-1}e^{mH(ρ_e)}` because `ρ_e ≤ r₁/m ≤ ½`.  I found no gap; in particular
the three ends are in order: `r₁ = m − 1` (ball of size `2^m − 1`), `e ≥ ε*` (`ρ_e = ½`, the bound is
`ln(m+1)`), `m = 1` (`r₁ = 0`, `π† = ½`, equality when `θ_na(e) = 0`).

*Exact test* (`r12_01`; big integers for the binomial sums, mpmath 60 digits for `E_r`, `T_m`;
`r†` computed from the definition; `θ` **exactly at** the threshold and `(1−η)ν₀ = 1`, the least
values allowed): `u ∈ {0.1, 0.3, 0.5, 1, 2, 4}`, every `m ≤ 40` and 21 sizes up to `5000`,
`η ∈ {½, ¼, 1/20, 1/100}`, 16 rates `e/ε* ∈ {0, 10⁻⁶, …, 0.999999, 1, 1.000001, 1.5, 3, 50}` and `e = h`.
Part (a): 870 451 radii, no violation, least slack `2.48` in the logarithm.  Part (b):
23 424 cases, **no violation** of `r† ≥ r₁` or of `ln(1/π†) ≤ m·θ_na(e) + ln(m+1)`; least slack
`0.000000` (`m = 1`, `e ≥ ε*`, as the report says); `r† = r₁` exactly in about 5 % of the cases, so
the radius is not improvable in general.  The threshold has room: with `θ` a factor `e` below
it nothing fails; a factor `e⁵` below, the radius fails in 3 424 of 3 904 cases at `u = 0.1` and in
none at `u ≥ 2`.  At `e = h`, `η = ½`: slack `12.6 … 15.2` nats at `m = 5000` (the report: 5–18 at
`64 000`).  My float tables agree with the exact ones to `5·10^{-13}` and with the earlier
referee's `TablesF` exactly.

### 2.2 Lemma Q3 (bounded `θ`) — correct [R, N]

*Re-derivation.*  Lemma K.4(b),(c) re-derived (median of the binomial law for `T_m(κ(r))`,
`r + 1 − κ(r) ≤ m₀ + 2`, Hoeffding).  Then, if `s = √(mℓ₁/2) ≤ p_u m/2 − 1`: `r₊ = ⌊p_u m − s⌋ ≥ p_u m/2`,
`ρ₊ ∈ [p_u/2, p_u]`, and Taylor's formula for `f = KL(·‖½)` at `p_u` (`f′(p_u) = −u`,
`f″ ≤ 8/(3p_u)` on `[p_u/2, p_u]`) gives the constant `u` where Lemma K.4(d) has `u + ln 4` (it bounds
the chord by `ln(2/p_u)`); `(s+1)² ≤ mℓ₁ + 2`.  Otherwise `m < m*(ℓ)` (the quadratic in `√m`), and
`ln(1/π†) ≤ (m+1)ln 2 = m·a + m·H(p_u) + ln 2`.  This case distinction is what replaces the two
hypotheses "`r₊ ≥ 0`" and "`r₊ ≥ p_u m/2`" of Lemma K.4(c),(d); the hypotheses `θ ≤ 2e^{u(m₀+2)}` and
`ν₀ ≥ 2e^u m/(θ(1−η))` remain, and are verified where the lemma is used (Proposition Q7(2):
`θ = c ≤ ⅓`, `ν₀ ≥ ν₁/(1−η)`).  Correct.

*Exact test* (`r12_02`): `u ∈ {0.1, ½, 1, 2, 4}`, every `m ≤ 40` and 14 sizes up to `5000`,
`η ∈ {½, ⅓, 1/10, 1/20, 1/100, 1/1000}`, `θ` from `2e^{u(m₀+2)}` down to `10^{-30}`, `ν₀` at its least value:
12 960 cases, no violation of the uniform bound (least slack `5.7`), of the refined bound
(least slack `3.0`), of Lemma K.4(c) or (d).  Float tables up to `m = 64 000`: at `u = 1`,
`θ = η = 0.05`, `(ln(1/π†) − ma)/√m = 1.535, 1.418, 1.338, 1.297, 1.282` at `m = 500 … 64 000` (the
report: `1.53 … 1.30`), against the leading constant `1.83` of Lemma Q3 and `4.36` of K.4(d).  The
`√m` is really there at a bounded `θ`.

### 2.3 Proposition Q6 (the slope step) — correct [R, N]

*Hypotheses of Theorem 11.56, one by one* [R]: `n ≥ 2` and `1 ≤ n_o ≤ n − 1` (from `X₀(n) ≤ x̂ ≤ hn`);
`λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1` admissible; `θ ≥ e^{x̂−1}/2 > 0` (`e^{x̂−1} ≥ 12e > 2(3e+2)`); `b = 1 > 0`;
ladder `x₀ = 2un_i > x₁ > … > x_L = 1 = b` with `1 ≤ x₁ = min(⌈x̂⌉, ⌈2un_i⌉ − 1) < 2un_i` (uses
`n_i ≥ (1 + c_log)/h` and `h ≤ u`, i.e. (F3)); inner procedures at accuracies `x_l ≥ 1 ≥ x_min`,
failure probability `δ′`, cost bounds in every run (m2).  Nothing is violated, and the
proof of Theorem K1 (which I read in full, re-deriving the probability of the good event
and its steps 4–8) uses nothing that fails at `θ = e^{Θ(n)}`, at `L = Θ(n)` rungs, or at `x_L = b`.

*Accuracy.*  `e^λ(1+η)/(1−η) + η′ = 3e + 1`, so `x_out = ln[(2p_u)^n + e(3e + 1 + θ)] = x̂` exactly;
the family delivers `x̂ = min(x, R′n) ≤ x`, which is what the majorant `−σ′·min(x, R′n)` charges.

*The slope.*  With `Λ_lev ≤ x̂ − 1 + P_M` (Lemma Q4 at `m = n_o`, `e = h`; the factor `6(n+1)e^{2u+e^u}`
in `θ` is exactly what `c_log` buys), the three cases of step (5) (`l = 1` with `x₁ ≥ x̂`; `l = 1`
with `x₁ = ⌈2un_i⌉ − 1 < x̂`; `l ≥ 2`) and the outer term are each `≤ V`; I re-derived each, and
`n_i B ≤ nB − x̂B/h + (1 + c_log + h)B/h`.  The loss relative to the affine majorant is `c_S`, i.e.
`(B/h + 4)·ln n + O(1)`: one `ln n` each from `c_log·B/h` (times `B/h`), `J`, `ν₀`, `K` and `L + 2`.
**Yes — a slope step loses only a polynomial factor.**

*The quantifier.*  `𝓗(B, σ, R; E)` is a statement for **all** `d ≥ 1`, `x ≥ x_min`, `δ`, `Λ`, and the
induction is over families, so the hypothesis is available at every `(n_i, x_l, δ′)`.  The
two places where a lost quantifier would bite are both handled: (i) the range — step (4)
proves `R·n_i ≥ x̂`, so `min(x_l, Rn_i) ≥ min(x_l, x̂)` at every rung, including the first one,
which is *coarser* than the level (`x₁ = ⌈x̂⌉ ≥ x̂`); (ii) dimensions and accuracies at which no
level can be built (`x̂ < X₀(n)`, in particular every small `n`) — the pass-through, paid by
the term `(1 + c_log + h)B/h` of `c_S`.  The failure probability: (2.1) gives
`ln(1/δ′) + n_i ln 2 ≤ Λ + q_S(n, Λ)`, which is the third argument at which the inner error
function is evaluated.  No quantifier is lost.

*The ladder.*  Rungs `l ≥ 2` have gap exactly `1`, which is the `+1` in `V`; the first rung is
charged the sample cap `2M̄`, not `e^{x₀}`.  The number of rungs enters through `ln(L+2)`,
`ln L` in `δ′` and in `K` only.  Confirmed.

*Tests* (`r12_03`, part A).  The inner family is given the cost
`d·B − σ·min(x, Rd) + E(d, x; ln(1/δ) + d ln 2)` exactly (the worst that `𝓗` allows; `C_max` is
monotone in the inner costs), with `E = 0` and with `E = 3√d`, `Λ/7`, `5/x + ln Λ`; the level as
built is evaluated with the exact constants of Theorem K1 (own evaluator, which reproduces
`r8_flat.flat_run`'s `J`, `K`, `r†`, `ln M̄`, `ln δ′`, `x_out`, `ln C_max` for the design of `K_REPORT.md`
§6.4 and the eight certified numbers `1.1384 … 0.5407` of §11.19(1b)).  `u ∈ {0.1, ½, 1, 2, 4}`;
`(B, σ, R)` along 12 epochs **and** off the schedule (`B/h ∈ {1, 1.01, 2, 11, 101}`,
`σ ∈ {0, 0.3, 1}`, `R/h ∈ {1, ⅓, 1/50, ∞}`); `n` from the first size at which a level exists
(`n = 470` at `u = 1`, `202` at `u = 2`, `299` at `u = 4`, `1678` at `u = ½`, `≈ 5·10⁴` at `u = 0.1`) to `10⁶`;
`x̂` at both ends of its range; `δ` from `0.999` to `e^{-50n}`.  **296 649 levels, no violation**
of the bound of Proposition Q6, of Lemma Q4, of (4.1), of (2.1), of any constant of step (3)
(`J + 1 ≤ A_n`, `m_max + 1 ≤ m̄_S`, `K ≤ K̄_S`, `P_cnt`, `P_M`, `L ≤ hn + 1`, `θ ≥ e^{x̂−1}/2`), and
`x_out = x̂` to rounding.  Least slack `2.2 … 10.2` nats (at `B = h`, `σ = 1`, `R = h`, `δ = e^{-50n}`),
against `c_S = 48 … 8 096`: the proposition is nearly sharp and I could not push it below
zero.  The second case of step (5) occurs in 2 176 of the levels.

### 2.4 Proposition Q7 (the drop) and the series `C₁` — correct [R, N]

*Re-derivation.*  Admissibility (`n_o ≤ φn < n/2`, `n_i > 1/u + 1`, `⌈Rn_i⌉ < 2un_i`); accuracy
(`e^β(e^c(1+c)/(1−c) + 2c) = e^{α−c}` and `(2p_u)^n ≤ 5c/6 ≤ 1 − e^{-c}`); Lemma Q3 with
`ℓ_c ≥ ln(2e^{u(m₀+2)}/c)`; (4.2) with `φa = R(1−φ)`; the constants `1.2, 1.5, 5.6, 7.45, 11.17, 4`,
`w(c) ≤ 6.25c` (sup of `w(c)/c` is `6`), `ln((1+c)/(1−c)) ≤ 2.25c`; the four kinds of term; the
dimension.  All re-derived; all numerical constants also checked on a grid of `c`.

*Tests* (`r12_03`, part B): inner cost `d·B − min(x, Rd) + E` exactly; `u ∈ {0.1, ½, 1, 2, 4}`,
`B ∈ {h, a, 3a}`, `R/h ∈ {1, ½, 1/7, 1/100}`, `c ∈ {⅓, 1/26, 10⁻², 10⁻⁴, 10⁻⁸}`, four values of `α` down
to `1.0001·w(c)`, every `n` from 2 to 200 and sizes up to `10⁶`, `δ` from `0.999` to `e^{-n}`:
**226 652 levels (5 352 with shift), no violation**; least slack `6.2` nats with shift, `45`
without; the pass-through inequality `nφB ≤ c_D` in all 310 848 cases where no level with
shift exists; Lemma Q3 at every level.

*The series.*  `φ_m ≤ r̄^{-1}(1+κ)^{-m}` follows from `d_{m+1} + 1 ≥ (d_m + 1)(1+κ)` (machine-checked
`epoch_gain`) and one line of algebra [R]; checked for 300 epochs at five slopes [N].  So
`C₁` is finite and independent of `M`.  Value at `u = 1`, `ε = 1`: base `1.597`, drops
`2.34, 3.47, 3.931, 3.936, 3.936` after `5, 13, 44, 120, 400` epochs: **`C₁ = 5.53`**, as stated (`ε = 0.1`: `6.31`;
`u = ½`: `2.43`; `u = 2`: `11.87`).  The crude geometric majorant of Proposition Q9a is `81`
(drops part), as the report says.

### 2.5 Theorem Q8, Proposition Q9a, Theorem Q9 — correct [R, N]

* *The induction* [R].  `B_0 = a`; step `j → j+1` of an epoch satisfies the hypotheses of Q6
  (`σ = j/d_m ≤ 1` because `j ≤ J_m − 1 < d_m`); `B_m/h − 1 = 1/d_m`; `R′ = h/(j+1)`; at `j = J_m` slope
  `≥ 1` on `(0, h/J_m)`; Q7 with `R = R_m`, `φ_m = h/(J_m a + h)`, and `B_{m+1} = B_m J_m a/(J_m a + h)`
  (algebra, re-derived; checked for 30 epochs at 260 slopes).  Least accuracies fit
  (`β = α_{m+1} − w(c_m) = α_m`; slope steps call at accuracies `≥ 1` or pass the accuracy
  through).  The error functions `E^{(t)}` are monotone as required (also checked on 12 000
  random arguments), and unrolling at `(n, ε̂, δ)` gives (5.2) with last accuracy exactly `α_0`.
* *The invariant* [R, N]: (2.1), `ln(1/δ′) + n_i ln 2 ≤ [ln(1/δ) + n ln 2] + ln(4L) + P_M`, because
  `ln M̄ ≤ P_M + n_o ln 2`; checked at every level built in every run.  Telescoped along a chain
  of nested levels it is the claim `Σ ln M̄ ≤ n ln 2 + k·O(ln n)`: the outer blocks of a chain
  are disjoint sets of coordinates, so their sizes add up to at most `n`.  The condition
  "`(k_M − 1)·O(ln n) ≤ n`" of Theorem Q(a) is precisely `T·q* ≤ ln(1/δ) + n ln 2` of Proposition
  Q9a, with `q* ≈ 3 ln n + 3 ln(1/c_{M−1}) + O(1)`; (5.2) itself holds without it.
* *The schedule* `c_m = ε̂/(13(m+1)(m+2))`: `Σw(c_m) ≤ 6.25ε̂/13`, `α_0 ≥ 0.519ε̂` [R]; `α_0 = 0.5611`
  for 44 epochs at `ε = 1` [N].
* *Small dimensions* [R, N].  The inner block is never empty (`n_o ≤ n − 1` in both steps;
  `n_i ≥ (1 + c_log)/h` in a slope step, `n_i > n/2` in a drop); an inner dimension `O(1)` is
  served by the pass-through and, at the bottom, by enumeration, and the hypothesis `𝓗`
  covers every `d ≥ 1`.  Tested: every `n` from 2 to 200, `M ≤ 3`, `ε ∈ {10⁻⁶, 0.01, 0.8715, 50}`,
  `δ ∈ {0.999, 0.05, 10⁻⁹, e^{-n}}`, `u ∈ {0.1, 1, 4}` — 38 208 designs, 77 272 drop levels built and
  checked (none chosen at these sizes), no violation, cost never above `2^n`; and the first
  sizes at which slope steps are built (outer blocks of `1, 2, …` coordinates).
* *Integrality*: `n_o` is a floor in both steps and the proofs carry the `±1`; `J_m = ⌈d_m⌉`
  satisfies `d_m ≤ J_m < d_m + 1`, also when `d_m` is an integer.
* *Proposition Q9a* [R, N]: `Λ̄_t ≤ Λ̄_0 + t·q*`; the closed form is `≥` (5.2) in all 90 cases
  evaluated (`u ∈ {½, 1, 2}`, `n = 10³ … 10^{10}`, `M ≤ 25`); in the 73 of them in which the
  hypothesis `Tq* ≤ Λ̄_0` holds, `Λ̄_T/Λ̄_0 ≤ 1.32` (claimed: `≤ 2`).  Here `q* = 38 … 105` nats.
* *Theorem Q9* [R]: `k_{m+1} < (1 + r̄)k_m` (re-derived; `3 + d_0 = 1 + r̄`), `c₂ = (2a+h)(a−h)/(ha) > 0`,
  the choice `k† = √((1+r̄)c₁n/ℓ_S)`, and `ℓ_S = (a/h + 4)ln n + O(1)`.  **`C_* = 4.646, 8.641, 13.524`
  at `u = ½, 1, 2`** (claimed `4.65, 8.64, 13.5`) [N].  Part (d) (`ε_n ≥ n^{-A}`) I checked at the
  level of orders [R] and by evaluating (5.2) at `ε_n = n^{-A}`, `A ∈ {½, 1, 3}`, `n ≤ 10^{12}`: the
  ratio stays between `3.1` and `6.0` [N].

### 2.6 Numerics — everything recomputed is reproduced [N]

* *Formula (5.2)* (`r12_04`, own evaluator typed from the text).  All 12 rows of the table of
  §7.4 agree (best `M`, `k_M`, bound`/(na)`, `𝓔_M`) to the digits printed; **`n = 6.4·10⁴`: `M = 5`,
  13 levels, `0.7072·na`**; also the 12 further numbers of §7.4(iv) (`ε = 0.1`, `δ = e^{-n}`,
  `u = ½, 2`), the epoch table of §5.1, the ranges of `(bound − nh)/√(n ln n)`.
* *One level* (`r12_07`): the tables of §7.1, parts A/B and C, agree in every column
  (`τ₂/a = 0.5004` recomputed from its closed form); Proposition Q1 and Lemma Q2 on 3 000 random
  admissible levels.
* *The nested design, exactly* (`r12_05`; my own implementation of `𝔊_0`, `S[·]`, `D[·]`, "proof"
  and "min" variants).  At every node: the induction inequality with `E^{(t)}`; at every
  level built: the bound of Q6/Q7 with the real inner family, Lemma Q3/Q4, (4.1)/(4.2),
  (2.1), the accuracy, the constants of step (3); at the top: Theorem Q8.

  | run (mode) | sizes | node checks | violations | agreement with the report |
  |---|---|---|---|---|
  | `u = 1`, `M = 0, 1`, both variants (A) | `n = 10³ … 6.4·10⁴` | 4.6·10⁶ | 0 | all 40 numbers of §7.3 to `10⁻³` |
  | `u = 1`, `M = 2`, both variants (A); "min" (big) | `n ≤ 8 000`; `n = 16 000` | 5.0·10⁶; 2.8·10⁷ | 0 | all 17 numbers (`0.7564`, bound `1.1018` at `16 000`) |
  | `M = 2, 3` (5 and 7 levels), `u = 1, 2` (D) | `u = 1`: `n ≤ 4000`; `u = 2`: `n ≤ 2000` | 8.3·10⁶ | 0 | all 18 numbers of the "seven levels" table |
  | `u = 2` and `u = ½`, `M = 1` (D) | `n = 1.6·10⁴`, `6.4·10⁴` | 1.8·10⁶ | 0 | `0.914 / 0.826 / 1.009` at `u = 2` |
  | awkward sizes (B) | `n = 2 … 200`; first sizes of slope steps | 1.7·10⁶ | 0 | — |
  | extremes (E) | `ε = 10⁻⁴ … 50`, `δ = 0.999 … e^{-100n}`, `u = 0.1, 1, 4`, `n ≤ 2·10⁵` | 1.7·10⁸ | 0 | — |

  "Exact certified cost `≤` formula" holds at every node I could afford.  The gap is large
  (`280 … 800` nats at `u = 1`), as the report says.

### 2.7 The statement itself

* *"For all `n ≥ 2`"* [R]: for `n < n₀` the bound `N ≤ 2ⁿ` is used and `C` is finite
  (`n(ln 2 − h) ≤ C√(n ln n)` for `2 ≤ n < n₀`); `n = 1` is rightly excluded (`ln 1 = 0`).  `n₀` and
  `C` are not computed in the report; see O1 for their size.
* *The lower bound*: see m1 (needs `δ < ½`; true and in fact `n·h − O(1)`; not in the theory
  report in the form used).
* *The definition of `N`* (at most `C` evaluations in every run, at every instance) is what
  the design delivers, **provided** the abort rule is (P) of m2; the bracket of ratio `e^{ε̂}`,
  `ε̂ = min(ε, 1)`, gives an `(ε/2, δ)`-correct midpoint.  The upper bound holds for every
  `0 < δ < 1`.

---

## 3. What I would write in the theory report

> For every `u > 0`, `ε > 0` and `0 < δ < 1` there is `C(u, ε, δ)` such that for all `n ≥ 2`
> `N(n; ε, δ) ≤ exp(n·h + C·√(n ln n))`, and `limsup_n (ln N − nh)/√(n ln n) ≤ C_*(u)`; for
> `δ < ½`, `ln N ≥ n·h − O(1)`.  **[P; workstream Q, refereed R12: given Theorem 11.56 with the
> abort test before every query, Lemma 11.55(a),(b), Proposition 11.57(a) and the epoch
> arithmetic of `RateFull.lean`.]**

with the caveats: `C` is not `C_*` (O1); the bound (5.2) is below `n·a` only from `n ≈ 2·10⁴`
(`u = 1`) and says nothing useful at `u ≳ 4` before `n ≈ 5·10⁴`; the exponent `½` is an upper bound
for this method, not shown to be its true order.

*The text that now stands in the theory report.*  The coordinator wrote Theorem 11.58a and
Lemma 11.55(c),(d) from the draft of this report while my last runs were going.  I read
both afterwards (not line by line beyond the statements and the six steps of the proof
sketch).  They state what I verified: 11.55(c) is the refined form of Lemma Q3 (the ball of
radius `⌊p_u m − s⌋`, under `s ≤ p_u m/2 − 1`), 11.55(d) is Lemma Q4, 11.58a(a),(b) are Theorems Q8
and Q9 with the caveat on `C`.  Three corrections, all to things taken over from my draft:
(1) 11.58a(c) gives the lower bound "for every `n` with `k*(ε) ≤ n/2`"; what is *proved* needs
the proviso of m1 (`(ρ_h − p_u)n ≥ 1 − (ε + ln 2)/u`) or the constant `max{1, (ε + ln 2)/u}`; as stated
it is confirmed numerically only (19 839 small cases).  (2) "What it is not", item (v):
"the smallest slope step exists at `n = 202`, `u = 2`, and costs `e^{100}` evaluations" — see the
first weakest link below for the right numbers.  (3) The counts "about 55 million checks"
and "51 million nodes" are those of the unfinished runs; the finished ones have 220 million
node checks.  Its item (iii), "no lower bound beyond `n·h − O(ln n)`", should read `n·h − O(1)`
to agree with its own part (c).

---

## 4. The three weakest links that remain

1. **Theorem 11.56 in the regime of Q, with rule (P).**  Everything is conditional on a
   paper proof that has been simulated only at bounded `θ` and at `θ ≤ e^{40}` with short
   ladders.  Q uses it at `θ = e^{Θ(n)}`, with unit-step ladders of `Θ(n)` rungs ending at
   `x_L = b` exactly, nested `√(n/ln n)` deep, with inner failure probabilities `e^{-Θ(n)}`, and
   with the abort rule (P), which the theory report prints for Theorem 11.56 only since
   the twenty-second checkpoint (m2).  I checked the hypotheses and re-read the proof; I
   did not simulate the algorithm, and it cannot be simulated in this regime: the
   smallest slope-step level exists at `n = 187` (`u = 2.5`; `n = 202` at `u = 2`, `470` at `u = 1`),
   its certified bound there is `e^{142}` (`e^{125}`, `e^{101}`), and any run of it that does not
   abort makes at least `K·C₁ ≈ e^{49}` (`e^{43}`, `e^{36}`) evaluations, because none of the first
   `K ≈ 300` outer points can be classified low before it has been given the base bracket
   of the first rung, whose cost is deterministic (`r12_06`, part E).  (The draft of this
   report said "costs `e^{100}` evaluations" for `n = 202`, `u = 2`; that figure was a guess and
   is replaced by these.)
2. **The composition at depth.**  Exact evaluation reaches seven levels (`M ≤ 3`) and
   `n ≤ 6.4·10⁴` — sizes at which the design is not better than the base family or the tuned
   designs of §11.19.  Where the theorem says something new (`n ≳ 2·10⁴` with `M ≥ 2`;
   `M = 5 … 32` for `n = 6.4·10⁴ … 10^{12}`) it rests on the paper induction and on one-level
   checks with saturating families (`n ≤ 10⁶`).  I re-derived the induction and the
   bookkeeping of `Λ`, accuracies and ranges; a numerical confirmation at depth does not
   exist and is out of reach of direct recursion.
3. **The inputs below Q.**  Proposition 11.57(a) (base bracket: I re-derived its proof from
   the two tail lemmas, which I did not re-derive), Harper's theorem and the binomial
   median (literature, not read), and the Lean file `RateFull.lean` (statements read against
   the report's (R); arithmetic checked numerically for 30 epochs at 260 slopes; not
   compiled here).  In addition `n₀` and `C` of Theorem Q(c) are not explicit, and for larger
   slopes the error terms grow like `e^{2u}` (O1).

---

## 5. What was done

**Re-derived completely [R]** (and tested numerically where a count is given in §2):
(F1)–(F4); Lemma K.4(a),(b),(c) as quoted in (L) (given the binomial median and Hoeffding);
Proposition Q1; Lemma Q2(a)–(d) and (2.1); Lemma Q3; Lemma Q4(a),(b); Corollary Q4a and the
remark on ladders; Proposition Q5(a),(b) (given Proposition K0, whose proof I also re-derived
given Lemma K.1); Proposition Q6 including every hypothesis of Theorem K1 for its
parameters; Proposition Q7 likewise; Theorem Q8 (induction on slopes, error recursion,
(5.2)); Proposition Q9a; Theorem Q9(a),(b),(c), and (d) at the level of orders; the algebra
`B_{m+1} = B_m J_m a/(J_m a + h)`, `k_{m+1} < (1+r̄)k_m`, `φ_m ≤ r̄^{-1}(1+κ)^{-m}`; the nesting under the
abort rule (m2, my argument); the form of the lower bound (m1, my argument).  Of Theorem
K1 itself: the probability of the good event and steps 4–8 re-derived, steps 1–3 and 9 read.

**Checked only numerically [N]**: the table of §7.4 and the numbers of §0 (all reproduced);
the tables of §5.1, §7.1, §7.3 (all reproduced; `M ≤ 3`); `C₁ ≈ 5.5`; `C_*`; the relations of
(R) (30 epochs, 260 slopes); the monotonicity of the error functions; the constant of
Theorem Q(c) on a grid (O1); the behaviour beyond `10^{12}` (O2); Theorem Q9(d) at
`ε_n = n^{-A}`; the lower bound at `n ≤ 2.56·10⁵`, and — numerically only — in the form "for
every `n` with `k*(ε) ≤ n/2`" at the small sizes where my argument gives a weaker constant (m1).

**Not checked [–]**: the Lean proofs (not compiled; statements of `kappa`, `c1`, `c2`,
`epoch_gain`, `closed_form`, `lemma1_top`, `lemma1`, `lemma2` read); Harper's theorem, the binomial
median, Chernoff–Hoeffding in the literature; Lemma K.1 (the tail lemmas); Theorem 11.56 by
simulation; Theorem 11.25(a); the author's scripts (not read, not run; only the numbers of
the report compared); §7.2 of the report case by case (replaced by my own, wider, tests);
exact nests beyond `M = 3`, beyond `n = 1.6·10⁴` for `M = 2`, beyond `n = 4000` for `M = 3`;
§6.2–§6.3 (conjecture and heuristic: read only); §9 (the report's remarks on the theory
report: items 3 and 4 agree with my checks, the others read only); slopes other than
`u ∈ {0.1, ½, 1, 2, 4}` in the level checks.

---

## 6. Files and commands

All in `experiments/reviews/R12/`; Python 3 with numpy and mpmath only; run from that
directory, one process at a time; largest memory use about 0.8 GB (`r12_03`, part A: four
cached tables of cubes of `10⁶` coordinates, measured `0.72` GB for the tables; `0.5` GB for
the nest at `u = 0.1`, `n = 2·10⁵`).  The stored outputs are those of the final versions of the
scripts and of the library: everything was re-run after the last change.

| file | what | command | time |
|---|---|---|---|
| `r12lib.py` | constants of the cube; exact tables (big integers, mpmath) and float tables of `Q_m`; all constants of Theorem K1 and `ln C_max` of one level; the families `𝔊_0`, `S[·]`, `D[·]`, `𝔊_M` with the checks at every node and level; the error terms of the report and (5.2) | (library) | |
| `r12_01_lemmaQ4.py` → `out_01_lemmaQ4.txt` | Lemma Q4 and Lemma K.4(a),(b) in exact arithmetic; float tables against exact ones and against `r8_flat.TablesF` | `python3 r12_01_lemmaQ4.py > out_01_lemmaQ4.txt` | 40 s |
| `r12_02_lemmaQ3.py` → `out_02_lemmaQ3.txt` | Lemma Q3, Lemma K.4(c),(d): exact, `m ≤ 5000`; float tables to `m = 64 000` | `python3 r12_02_lemmaQ3.py > out_02_lemmaQ3.txt` | 7 s |
| `r12_03_steps.py` → `out_03_steps.txt` | own level evaluator against `r8_flat.flat_run`; Propositions Q6 and Q7 with saturating inner families; the small facts and constants | `python3 r12_03_steps.py > out_03_steps.txt` | 6 min |
| `r12_04_formula.py` → `out_04_formula.txt` | constants, `C_*`, epochs, `C₁`, the table of §7.4, Proposition Q9a, Theorem Q9(b),(d), beyond `10^{12}`, monotonicity | `python3 r12_04_formula.py > out_04_formula.txt` | 30 s |
| `r12_05_nest.py` → `out_05_nest_A.txt`, `_B`, `_D`, `_E`, `_big` | the nested design evaluated exactly: tables of §7.3 (A, D, big), awkward sizes (B), extremes (E) | `python3 r12_05_nest.py A > out_05_nest_A.txt`, likewise `B`, `D`, `E`, `big` | 3 min, 0.5 min, 2.5 min, 19 min, 10 min |
| `r12_06_misc.py` → `out_06_misc.txt` | the lower bound (m1), also at small sizes; Proposition Q5(a),(b); an explicit constant (O1); sensitivity of `r†` to ties; the smallest slope-step level and its cost | `python3 r12_06_misc.py > out_06_misc.txt` | 10 s |
| `r12_07_onelevel.py` → `out_07_onelevel.txt` | tables of §7.1; Proposition Q1, Lemma Q2 on random levels; Corollary Q4a | `python3 r12_07_onelevel.py > out_07_onelevel.txt` | 2 s |

Numerical conventions: tables of `Q_m` as float64 logarithms (validated against exact
arithmetic to `5·10^{-13}` for `m ≤ 400`); comparisons of table entries with tolerance `10^{-12}`
(`r†` does not depend on it in the 21 designs tried); the ceiling in the base sample size is
kept (`M ≤ X + 1`), which is why my `ln C_max` differs from `flat_run`'s by up to `10^{-4}`; the
block size `⌊(x̂ − 1 − c_log)/h⌋` is computed with `+10^{-12}` so that `x̂ = X₀(n)` gives `n_o = 1` in
floating point.
