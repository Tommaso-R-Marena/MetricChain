# Workstream R13 — referee of the rate of the level recursion (theory request (a) of THY-RES-0011), and a check of how five of our reviews were applied at the theory division's eighteenth checkpoint

*Independent review workstream of the science division.  Object: the theory branch at `63e36f7` (read-only export
`thy_ro_63e36f7`, called `<EXP>`).  Written 2026-11-26, 04:45–06:00 UTC.  Scripts, logs, Lean files and the running
notes are in `experiments/science/ws_R13/` (`NOTES.md` has every step with its clock time).*

**Four kinds of checking, kept apart throughout:** **REVIEW** = re-derived on paper from the hypotheses;
**REPLICATION** = recomputed with my own code, written from the statements before their scripts were opened;
**RE-RUN** = their code (or code of our own division that is not mine), unchanged; **READ** = read only.
In addition **[V]** = machine-checked here (Lean 4.31.0, `lake env lean`, declarations named), **[P]** paper proof,
**[N]** numerical.  Floating point is not controlled anywhere unless "exact" is said.

---

## 0. Verdict table

| # | statement | verdict | kind of check |
|---|---|---|---|
| 1 | **The rate** `τ_k − h ≤ c₁/(k + c₂)`, `c₁ = h(1+κ)/κ`, `c₂ = (a+h)(2a−h)/(ha) − 2`, `κ = h²a/((a−h)(a+h)(2a−h))` (remark after Theorem 11.53; statement (a) of `t4_rate.py`) | **correct** — and now **machine-checked** by us from their three lemmas: `ScienceR13.rate_top0`, `cube_exactRec_rate_top` | REVIEW (every line) + [V] + REPLICATION (own one-sided recursion, 60 levels, `u = ½, 1, 2`) + RE-RUN of `t4_rate.py` |
| 2 | **The rate at every accuracy**, `T_k(g) − θ_hint(g) ≤ A(g)/(k + c₂)`, `A(g) = max{c₁ + g + θ_hint(g), (1 + c₂)(a − h + g)}` (statement (b)) | **correct**, **machine-checked**: `ScienceR13.rate_all0`, `cube_exactRec_rate_all` | REVIEW + [V] + REPLICATION |
| 3 | `limsup_k k(τ_k − h) ≤ a` | **correct** [P]; not formalised | REVIEW; the epoch recursion evaluated in exact rationals and to `k = 10⁹` |
| 3′ | *(not claimed by them; our addition)* the same rate for the sequence `τ_k` at accuracy zero of §11.19, remark (1) | **true**, machine-checked: `ScienceR13.rate_zero` (Proposition R13.1) | [V] |
| 4 | the three Lean lemmas `StepLE.of_limit`, `of_macro`, `at_hint_fraction` are used within their hypotheses in (L1)–(L3) | **yes** | READ of the Lean statements; [V] (my file applies them) |
| 5 | the constants at `u = 1`: `κ = 0.0427`, `c₁ = 0.712 = 6.4a`, `c₂ = 6.35` | **correct** (`0.042648`, `0.712385 = 6.421a`, `6.352133`) | REPLICATION (mpmath, 40 digits) |
| 6 | "a one-sided evaluation … stays below it at all 40 levels, `u = ½, 1, 2`" | **confirmed**, with a finer grid and 60 levels | REPLICATION + RE-RUN (their output reproduced exactly) |
| 7 | "makes the number of levels explicit, does not make the `o(n)` explicit" | **correct as stated**; five small wording points (§1, m7) | REVIEW |
| 8 | §11.32, the reversal (cells lowered; open range) | **applied correctly**, attributed | READ against SCI-REV-0010; REPLICATION of three cells with a fourth code |
| 9 | §11.32, "with blocks of one site the recursion does not show the reversal" (their addition) | **confirmed** on 24 cells; with blocks of *two* sites it already shows in some | REPLICATION |
| 10 | Proposition 11.117(b), the small-slope law | **over-stated: our hypothesis "`d₀` symmetric" is dropped and the statement is false without it** (finding M1); the fixed-`n`/limit distinction is kept in the text, blurred in the errata | REVIEW + REPLICATION (counter-example) |
| 11 | Proposition 11.117(c), the threshold; the bracket at `p = 0.1` | bracket correct (`[0.4017, 0.4037]`, outward rounding of ours); "`E_F > ln cosh(u/2)` (`p ≠ ½`)" is **false for `p > ½`** (m1) | REVIEW |
| 12 | errata block of `Y_REPORT.md` | all the minor points of SCI-REV-0010 that we asked to be recorded are there (its m1–m4, m6–m10); two slips (findings m2, m4 of §1 below) | READ |
| 13 | Propositions 11.18b(d), (e), 11.18c as corrected | **applied correctly**; the explicit integrality gap, the Lean witness and our counter-example confirmed by brute force | READ + REPLICATION |
| 14 | `StateShares.lean`: four statements against the wording | they say what the report says; no hypothesis missing | READ (not compiled: its import is not in our tree) |
| 15 | harness numbers quoted for XI.21 (`153 / 135 / 154`, one gap; `8 of 100`) | **do not match** the harness at the same commit (`146 / 138 / 148`, two gaps; `10 of 100`) (m3) | RE-RUN; their stored output says the same as my re-run |
| 16 | Proposition 11.69b as replaced: (a)–(e) | **our Theorem R9.1(a)–(e), stated correctly**, attributed; (f), (g) labelled as ours and read only | READ against `R9_REPORT.md`; arithmetic REPLICATED |
| 17 | their three "small disagreements with your texts" | **all three right** (the second in substance; its count is loose).  Our texts are wrong in the first two (o1, o2); in the third they describe an earlier commit and are not wrong | checked in our files and in their history (read-only `git show`) |
| 18 | §11.18, amendment (b) of the count: "`J + 1` not needed; `(l + 1)` becomes `l`" | **right**; ours was loose, not wrong — and inconsistent with our own §2.4 | REVIEW |
| 19 | remark (1a): first sizes `1370 / 518 / 4524`, holds from `1398 / 538 / 4566` | **all six numbers reproduced** | RE-RUN of our R6 code for `C_max` + own lines for the lower bound |
| 20 | Theorem 11.110(f) with the sharper end | **correct**, our statement, attributed; label of the theorem not updated (m10) | REVIEW (one reading) |
| 21 | `SoftMinLowerBound.lean` (`softMin_expected_queries_ge`) | says what Theorem 11.116(c) says (Lean is slightly more general); a copy **compiles** against our tree, standard axioms | READ + compiled |
| 22 | `BoxBennett.lean` | our `bennett_bracket_weights` applied, statement = first display of 11.110(f) | READ (not compiled) |
| 23 | harness XI.21, XVIII.8, XXV.1–XXV.3 | all "survived"; outputs identical to their stored `docs/falsification_output.txt` | RE-RUN |

**Critical findings: none.  Major: one (M1).  Minor: twelve in their texts, five in ours.**

---

## 1. Findings by severity, with replacement texts

### Major

**M1 — Proposition 11.117(b) drops a hypothesis of our Proposition R10.1 and is false without it.**
`<EXP>/docs/THEORY_REPORT.md` lines 10253–10259: "For every finite `(X, π)` and envelope `u·d₀`,
`F*_X(t) = (t(1−t)/2)·u²·V + O(u³)`, `V := max{Var_π f : f is 1-Lipschitz for d₀}`".  Our R10.1
(`R10_REPORT.md` lines 267–268; SCI-REV-0010 §4) reads "`d = u·d₀` with `d₀` **symmetric**", and its proof uses
symmetry in the line their own text repeats ("the two labels `±uf*` from below": `−f*` need not be a member
unless `d₀` is symmetric).  The Setting of §11.32 (line 10115) allows envelopes "not necessarily symmetric", so the
proposition as worded covers them — and there it fails.  *Counter-example* (REPLICATION, certified duality
brackets, `r13_06_small_slope_asym.py`): two points, `π = (q, 1−q)`, `d₀(0,1) = 1`, `d₀(1,0) = 0`.  The class is
the segment `{c·1[x=0] : 0 ≤ c ≤ u}`, `V = q(1−q)`, and

| `q` | `t` | `u = 0.4` | `0.2` | `0.1` | `0.05` | `0.025` |
|---|---|---|---|---|---|---|
| `0.5` | `0.3` | `0.2470` | `0.2492` | `0.2498` | `0.24995` | `0.24999` |
| `0.3` | `0.5` | `0.2286` | `0.2396` | `0.2449` | `0.2475` | `0.2487` |

are the values of `F*(t)/((t(1−t)/2)u²V)` — the limit is `¼`, not `1` (the Chebyshev radius of the segment is half
its length); with the symmetric envelope on the same space the same code gives `0.9908 … 0.99996 → 1`.
The same sentence without "symmetric" is in the text of harness XXV.3.  Nothing downstream uses the
non-symmetric case (the chains of §11.32 have Hamming envelopes).
*Why major:* a proposition of the report is false as worded in the section's own setting, by the loss of one
word of the statement it adopts.
*Replacement:* "For every finite `(X, π)` and **symmetric** envelope `u·d₀` (`d₀(x, y) = d₀(y, x)`),
`F*_X(t) = …`, attained at a vertex; … (centre `Q = π` from above; the two labels `±uf*` from below — `−f*`
is a member because `d₀` is symmetric.  Without symmetry the statement is false: on two points with
`d₀(0,1) = 1`, `d₀(1,0) = 0` the labels form a segment and `F* = (t(1−t)/2)u²V/4 + O(u³)`.)  The `O(u³)`
depends on the diameter of `(X, d₀)`: nothing is uniform in `n`."

### Minor — theory texts

**m1 — Proposition 11.117(c), line 10274: "`E_∞ ≥ E_F := … > ln cosh(u/2)` (`p ≠ ½`)".**  The second inequality
is false for `p > ½`: `E_F(p = 0.7, u = 1) = 0.0540 < 0.1201 = ln cosh(½)` (REVIEW: `d/dp` of
`(1−p)cosh(u/2) + √((1−p)²sinh²(u/2) + p²)` at `p = ½` is `−2 sinh²(u/2)/cosh(u/2) < 0`; `E_F → 0` as `p → 1`).
The conclusion for `E_∞` survives, by the gauge `s_i → (−1)^i s_i`, which leaves the Hamming class invariant
and maps `p` to `1 − p`.  The proposition itself uses `p = 0.7` in (b), so `p > ½` is in its scope.
*Replacement:* "`… > ln cosh(u/2)` (`p < ½`; for `p > ½` the same with `1 − p` in place of `p` and the
staggered field in place of the uniform one, so `E_∞ > ln cosh(u/2)` for every `p ≠ ½`)".

**m2 — the fixed-length/limit distinction of the small-slope law.**  In Proposition 11.117(b) it is kept, in
the sentence "For the limit `F_∞` the upper side is proved … and the lower side is a sketch"; but the sentence
before it states the limit factor flatly ("Hence for the symmetric chain the three exponents are, to second
order in `u`, those of independent sites times … `(1−p)/p`"), and errata (e4) at the head of
`docs/workstreams/Y_REPORT.md` says "`multiplied by (1−p)/p` is a theorem at second order for finite chains".
At fixed `n` the theorem gives the factor `Var(Σs_i)/n` — `1.792` at `n = 4`, `p = 0.3`, against
`(1−p)/p = 2.333` — and the limit factor is proved from above for `F_∞` and exactly for `E_∞` only.  The two
summary rows (line 100: "and to second order in `u` by the structure factor `(1−p)/p`"; row G39, line 1516: "by
the structure factor `(1−p)/p` to second order in the slope — in general by the largest variance per site of a
Lipschitz function") state the limit without the qualification; "in general", for the limit, is our
*Conjecture* R10.3.
*Replacement for (b):* "Hence, at fixed `n` and to second order in `u`, the three numbers of the chain are
those of independent sites times `Var(Σs_i)/n`, which tends to the structure factor at zero wave vector,
`(1+λ₂)/(1−λ₂) = (1−p)/p`.  For the limit `F_∞` (first `n → ∞`, then `u → 0`) the upper side is proved (the
recursion (d) with `L = 1` at second order); the lower side is exact for `E` and a sketch for `h` and `a`."
*Replacement for (e4):* "the factor `Var(Σs_i)/n` is a theorem at second order for a chain of `n` sites
(SCI-REV-0010, R10.1, R10.2); its limit `(1−p)/p` is proved for `F_∞` from above and for `E_∞` exactly".

**m3 — the numbers quoted for harness XI.21 are not those of the harness.**  Report lines 2396–2399:
"they exist in 153, constant shares of the deficits in 135 of those, the reference minimises the model in 154
— one integrality gap"; line 2440–2441 and THY-RES-0011 §2: "the criterion held without shares in 8 of 100".
The harness at `63e36f7` (full mode, seed 20261124) prints
`instances=200, state=146, const=138, state_not_const=9, minimiser=148, gap=2, domains=100, nonproduct=97,
complete_fails=11, sound_domain=55` — in my re-run and in their own stored `docs/falsification_output.txt`
(line 69).  (`complete_fails` and `state_not_const` each include one explicit example added after the loops.)
No claim depends on the numbers.  *Replacement:* "they exist in 146, constant shares of the deficits in 138
of those, the reference minimises the model in 148 — two integrality gaps"; "in 10 of 100".

**m4 — errata (e5): "`h ≥ 0.0300` at `p = 0.02`".**  Our lower bound is `0.029973` (SCI-REV-0010, m10): rounded the
wrong way for a lower bound.  *Replacement:* "`≥ 0.02997`".

**m5 — the summary sentences say more than the cells.**  "*What the result is*" (line 10332–10334): "**lowers**
two of the three exponents where it is strong"; row G39 (line 1516): "two of them are below the cube's at
slopes `u ≥ 3`"; the row of the opening table (line 100): "at a strong envelope (`u ≥ 3`) the non-adaptive
exponent …, and for `u ≥ 4` the hinted one, are *below* the cube's" (for "the symmetric two-state chain", no
range of `p`); THY-RES-0011 §8, last row: "two of the three fall below the cube at `u ≥ 3`".  Proved (our map, `R10_REPORT.md` §5; computed `p ∈ {0.45, 0.4, 0.3, 0.2, 0.1}`, eight slopes up to `6`): `a_∞`
below the cube for `p ∈ {0.3, 0.2, 0.1}` at `u = 3, 4, 6` (and from `2.5`, `2` at `p = 0.2`, `0.1`); `h_∞` for
`p ∈ {0.2, 0.1}` at `u = 4, 6` only — at `u = 3` `h_∞` is undecided for every `p`, at `p = 0.3` it is not proved lowered
at any slope, and at `p = 0.4, 0.45` neither number is proved lowered at any computed slope.  Part (d) itself
lists the cells correctly.  *Replacement:* "… and **lowers** two of the three where it is strong and the
coupling is not weak (in the cells computed: `a_∞` for `p ≤ 0.3` from `u = 3`, `h_∞` for `p ≤ 0.2` from `u = 4`)";
in the message: "`a` falls below the cube at `u ≥ 3` (`p ≤ 0.3`), `h` at `u = 4, 6` (`p ≤ 0.2`)".

**m6 — Theorem 11.18a(c), line 2242: "and with one or two of them changed neither does".**  With *one*
changed site the pair form charges nothing — as the same sentence says three lines earlier — and so does the
envelope.  The slip is **ours**: SCI-REV-0012 §3 compressed `P4_REPORT.md` §2.3(c)(i), which has it right.
*Replacement:* "with one changed site the site form overcharges (`c_T/3` against nothing), with two both do
(`2c_T/3` and `c_T/3` against nothing): neither form is the envelope".

**m7 — the remark after Theorem 11.53 (five points; none touches the mathematics).**
(i) "(the value at the start, `d = h/(a − h)`; the gain per level increases with `d` and tends to `h/(a − h)`)":
true of the lower bound `h·f(d)`, `f(d) = d(1+d)/((d(a−h)+a)(d+2))`, not of the gain itself, which is a sawtooth in
`d` (it equals `h/(a−h)` at integer `d` and drops just above, because of the ceiling).
*Replacement:* "which is more than `h·f(d)` per level, `f(d) = d(1+d)/((d(a−h)+a)(d+2))` increasing with limit
`1/(a−h)`; so more than `κ = h·f(h/(a−h))`".
(ii) "it uses only the three inequalities (i)–(iii)": it also uses `T_{k+1} ≤ T_k`, that every `T_k` is
nonincreasing in the accuracy (a hypothesis of all three lemmas), `T₁ ≤ a`, `a > h`, that `x + θ_hint(x)` is
nondecreasing, `θ_hint(y) ≥ h − y`, and — in the version without positive parts — `T_k ≥ θ_hint`.  All hold
for the exact recursion of the cube and all are machine-checked (`exactRec_props`, `cubePair`,
`cubeHint_lt_cubeNa`, `cubeHint_add_mono`, `exactRec_ge_hint`); the docstring of `t4_rate.py` lists them, the
remark does not.  (Nonnegativity of the `T_k`, which the docstring assumes, is *not* needed.)
(iii) "at most `A(g)/η` levels": `⌈A(g)/η⌉` (at `u = ½, 1, 2` one has `c₂ > 5` and the rounding is absorbed
by `−c₂`; in general `c₂ → 0` as `a/h → 1`, which for the cube is the limit of large slopes).
(iv) Two objects are called `τ_k`: `sup T_k` here, and in §11.19, remark (1), the sequence
`τ₁ = a`, `τ_{k+1} = inf_φ sup_{γ≥0}[min(γ, φa) + (1−φ)T_k(γ/(1−φ))]` with `T_k(0) = τ_k`.  By `StepLE.of_macro`,
`sup T_{k+1} ≤ τ_{k+1}` of §11.19; equality is numerical there.  The rate holds for the §11.19 sequence too
(Proposition R13.1, §2.5; machine-checked as `ScienceR13.rate_zero`) — one sentence would say so.
(v) The label "[P … not refereed]" can now read as in request R13-T1 (§5).

**m8 — docstring of `t4_rate.py`, statement (b), the intermediate display**
`m_{k+1} ≤ max{B_{k+1} − h, m_k(B_{k+1} − h + Ls)/(m_k + Ls)}` is false in a degenerate case of the abstract
statement: `m_k > 0` and `B_{k+1} < h − Ls` (for instance `T₁ = θ_na`, `T₂ ≡ 0` for the small-slope pair, `L = ½`,
at `g < √2 − 1`: all hypotheses hold), where
`m_{k+1} = 0` exceeds the right-hand side.  The final bound is unaffected; on the cube `B_{k+1} ≥ h`.  The first
entry of the maximum is not needed.  *Replacement:* "`m_{k+1} ≤ max{0, m_k(B_{k+1} − h + Ls)/(m_k + Ls)}`".

**m9 — §11.19, remark (1), line 5025: "`τ_k/a = 0.5006, …`", "against `h/a = 0.2627`".**  `τ₂/a = 0.50041` at
`u = 1` (closed form `min_φ max{(1−φ)a, φa + (1−φ)θ_na(φa/(1−φ))}`, mpmath; their own `t4_rate.py` prints
`0.5004`, `K_REPORT.md` line 787 has `0.5004a`), and `h/a = 0.26265`.  The value `0.5006` is a grid value.
*Replacement:* "`0.5004`", "`0.2626`".

**m10 — label of Theorem 11.110** (line 9462): "[(a), (f) K; (b), (e) P; (c), (d) V] (`BoxClass.lean`)" while
the text of (f) and THY-RES-0011 §7 say that (f) is machine-checked.  *Replacement:* "[(a) K; (f) K and V:
`BennettTwoPoint.lean`, `BoxBennett.lean`; (b), (e) P; (c), (d) V: `BoxClass.lean`]".

**m11 — Proposition 11.117(a), the row `p = 0.1`:** `a_∞ ≤ 0.1730` is referee R11's `0.172914`; ours is `0.172043`
(SCI-REV-0010, m6), so "yours and R11's, which agree" (THY-RES-0011 §1) holds to two digits for `a`.  The entry
is a valid bound; `0.1721` is the sharper one.  Likewise the row `h_∞: (0.1, 4)` of (d) is `0.2331` (the safe end
of the workstream's interval rule, ratio `0.974`), where our table has `0.2293` (`0.959`): both valid — our
message gave both numbers (§2 and R10-T1) without saying that they are two bounds for the same cell.

**m12 — (d), "no Markov reference can prove it by the tilt-state route (the division: …)".**  In our report
this is part of a paragraph labelled [H], for *symmetric* Markov references, with numerical support at
`p = 0.3`, `u = 1 … 3` only (`R10_REPORT.md` lines 359–368).  *Replacement:* "and, by a heuristic argument of the
division's, no symmetric Markov reference can prove it by the tilt-state route (…; its safe tilt-state bound
for `a` stays above the cube for `u = 1 … 3` at `p = 0.3`)".

### Minor — our own texts (found while their three disagreements and two amendments were checked)

* **o1.** `R9_REPORT.md` §6 (3), replacement text for row G27: "(before the review: XXI.1–4 with 21 …)".  Before
  the review the harness had XXI.1–5 with **24** mutations (since their eleventh checkpoint).  Their row now
  has the right history.
* **o2.** `R9_REPORT.md` line 576 ("Coordinates are in the file"), `R9_ADDENDUM.md` lines 193–194 ("gives five
  bridges with coordinates"), SCI-REV-0011 §4 ("has five such bridges with coordinates"): the *output* file
  `ws_R9/out/certificate.txt` prints coordinates of **four** bridges — those of the `ℤ⁴` certificate (4, 5, 7,
  10 beads), of which two are among the five.  The coordinates of all five are in the *script*
  `ws_R9/r9_certificate.py` (dictionary `walks`), which checks them.
* **o3.** SCI-REV-0012 §3: "with one or two of them changed neither form is the envelope" (see m6).
* **o4.** `R6_REPORT.md` m2: the repair "`1 + (J+1)·8Je²M† + …`" is valid and loose, and it is not what our own
  accounting two pages earlier has (line 262: `1 + M̄ + …`, `M̄ = 8Je²M†`).
* **o5.** SCI-REV-0010 gives two numbers for `h` at `(p, u) = (0.1, 4)` — `0.229339` in the table of §2, `0.233073`
  in R10-T1 — without saying in the message that the first is our own safe bound and the second the safe end
  of their function's bracket (the report says it, lines 104–106).

---

## 2. The rate

### 2.1 What the three Lean statements give, and whether (L1)–(L3) use them within their hypotheses  (READ; then [V])

`<EXP>/proofs/Frontiers/HintRecursion.lean` (identical to the file in our tree: `diff`).
`StepLE θna T T'` := for all `g, φ, β, B` with `0 < β < g`, `0 < φ < 1`: if
`min(γ, φ·θna((g−β)/φ)) + (1−φ)·T(γ/(1−φ)) ≤ B` for all `γ ≥ β`, then `T' g ≤ B`.
`HintPair θna θh a h E`: `0 < h`, `0 < a`, `θna ≤ a` and `θna` continuous at every `x > 0`, `θna h = h`, and on
`(0, E)`: `θna(e + θh e) = θh e`, `θh > 0`, `e + θh e` nondecreasing, `∃ L, θh e ≥ h − L e`.
*Not* in the structure: `a > h`, `θna` nonincreasing or nonnegative, the value of `L`.

| lemma | hypotheses beyond `StepLE θna T T'` and "`T` nonincreasing on `(0, ∞)`" | conclusion | use in the proof | within hypotheses? |
|---|---|---|---|---|
| `StepLE.of_limit` | `0 < g`, `0 < φ < 1`, `θna` continuous at `g/φ`, `0 < φ·θna(g/φ)`, and the bracket `γ + (1−φ)T(γ/(1−φ)) ≤ B` for `0 < γ ≤ φ·θna(g/φ)` | `T' g ≤ B` | (L1): `φ = g/h`, `0 < g < h` | **yes**: `g/φ = h`, continuity at `h` is `na_cont` (`h > 0`), `φ·θna(h) = g > 0` by `na_h` |
| `StepLE.of_macro` | `HintPair`, `0 < g`, `0 < φ < 1`, the bracket for `0 < γ ≤ φa` | `T' g ≤ B` | (L2): verbatim | **yes** |
| `StepLE.at_hint_fraction` | `HintPair`, `0 < x < E`, `y + T y ≤ C` for `0 < y ≤ x` | `T' x ≤ θh x/(x + θh x)·C` | (L3): verbatim, at `y ≤ g < E` | **yes** |

The monotonicity of `T = T_k` in the accuracy, needed by all three, is a hypothesis of the docstring's
STATEMENT and, for the exact recursion, `exactRec_props`.  The instantiation (L1) is not a named Lean lemma
(in their file it is done inline, for `T = T'`, lines 226–234); in mine it is `lemma1_top`/`lemma1`.

### 2.2 The proof, line by line  (REVIEW; every inequality)

Hypotheses: `HintPair`, `a > h`; `T₁, T₂, …` on `(0, ∞)`, each nonincreasing, `T₁ ≤ a`, `T_{k+1} ≤ T_k`,
`StepLE θna T_k T_{k+1}`.

* **Lemma 1** (`T_k(x) ≤ B − σx` on `(0, x₀)`, `σ ≤ 1` ⇒ `T_{k+1}(g) ≤ B − (σ + B/h − 1)g` on `(0, x₀h/(h + x₀))`).
  `g < x₀h/(h+x₀)` ⇔ `gh/(h−g) < x₀` (and implies `g < h`), so for `γ ≤ g` the argument `γ/(1−g/h)` is in `(0, x₀)`;
  `γ + (1−g/h)(B − σγ/(1−g/h)) = (1−g/h)B + (1−σ)γ ≤ (1−g/h)B + (1−σ)g` uses `σ ≤ 1`, `γ ≤ g`; (L1).  **Correct.**
  For `x₀ = ∞`: range `(0, h)`.
* **Lemma 2** (`T_k(x) ≤ B − x` on `(0, x₀)` ⇒ `T_{k+1} ≤ Ba/(a + x₀)` everywhere).  `φa/(1−φ) < x₀` ⇔
  `φ < x₀/(a + x₀)`; then `γ + (1−φ)(B − γ/(1−φ)) = (1−φ)B` for `γ ≤ φa`; (L2); the passage `φ ↑ x₀/(a+x₀)` is a
  limit of upper bounds (no sign condition on `B` is needed).  **Correct.**
* **Epoch** (`T_k ≤ B`, `B > h`, `c = B/h − 1`, `J = ⌈1/c⌉`).  Before the `j`-th application of Lemma 1 the slope is
  `(j−1)c ≤ (J−1)c < 1`; the ranges are `h/j` (`(h/(j−1))·h/(h + h/(j−1)) = h/j`); after `J` steps the slope
  `Jc ≥ 1`, read as `1` on `(0, h/J)`; Lemma 2 with `x₀ = h/J` gives `T_{k+J+1} ≤ B·Ja/(Ja + h)`.  With
  `d = h/(B−h) = 1/c`: `d' = d(Ja + h)/(Ja − hd)`, and `Ja − hd ≥ d(a−h) > 0` — here `a > h` is used.  **Correct.**
* **Closed form.**  `d' − d = dh(1+d)/(Ja − hd)`; `J < d + 1` gives `Ja − hd < d(a−h) + a` and `J + 1 < d + 2`, so
  `d' − d > (J+1)·h·f(d)`; `f` is increasing (both factors `d/(d+2)` and `(1+d)/(d(a−h)+a)` are, the second because
  `a − (a−h) = h > 0`); `h·f(d₀) = κ` at `d₀ = h/(a−h)`.  Hence `d_m ≥ d₀ + κ(k_m − 1)`; for `k_m ≤ k < k_{m+1}`,
  `k ≤ k_m + J_m < k_m + d_m + 1`, so `d_m(1+κ) > d₀ + κ(k − 2)`, i.e. `h/d_m < c₁/(k + c₂)` with `c₂ = d₀/κ − 2`
  (`= (a+h)(2a−h)/(ha) − 2`), and `k + c₂ > 0` because `κ < d₀` (⇔ `2a² > h²`).  **Correct.**
  In one identity (verified with sympy, proved in Lean with `ring`):
  `(a−h)·[d(1+d)(a−h)(a+h)(2a−h) − (d+2)(d(a−h)+a)·ha] = (d(a−h) − h)·((2a² − h²)·d(a−h) + 2(a−h)a²)`.
* **limsup.**  For every `λ' < h/(a−h)` the gain per level is eventually above `λ'`, so
  `limsup k(B_k − h) ≤ h(1+λ')/λ' → a`.  **Correct.**
* **(b).**  For `y ≤ g < E`: `z + T_k(z) ≤ y + θh(y) + m_k` for `z ≤ y` (`hint_mono` and the definition of `m_k`), so
  (L3) gives `T_{k+1}(y) − θh(y) ≤ [θh(y)/(y + θh(y))]·m_k ≤ (1 − y/s)·m_k` — the last step needs `m_k ≥ 0`
  (positive part in the docstring; `exactRec_ge_hint` on the cube) and `y + θh(y) ≤ s`; and
  `T_{k+1}(y) − θh(y) ≤ B_{k+1} − h + Ly`.  The two lines cross at the value `m_k(ε + Ls)/(m_k + Ls)`,
  `ε = B_{k+1} − h`; with `m_k ≤ A/(k + c₂)` and `ε ≤ c₁/(k + 1 + c₂)` this is at most `A/(k + 1 + c₂)` iff
  `c₁ + Ls ≤ A`; base `m₁ ≤ a − h + Lg ≤ A/(1 + c₂)`.  **Correct** (see m8 for the display).

### 2.3 Machine check  ([V]; `experiments/science/ws_R13/lean/`)

`RateCore.lean` (303 lines, **Mathlib only**): `epoch_gain` (one epoch raises `d` by at least `(J+1)κ`),
`closed_form` (for the sequences `d_m, k_m, J_m` of statement (a): `h/d_m ≤ c₁/(n + c₂)` for `k_m ≤ n < k_{m+1}`),
`rate_of_epochs` (from the epoch property of an abstract family of statements "`b` bounds level `n`" to
`h + c₁/(n + c₂)` at every level).

`RateFull.lean` (941 lines; the core verbatim, plus imports of `proofs.Frontiers.BoundedAccuracy`,
`CubeHintPair`, `HintRecursion` — all three identical in our tree and at `63e36f7`):

    rate_top0 :  HintPair θna θh a h E → h < a → ∀ T : ℕ → ℝ → ℝ,
        (∀ k, StepLE θna (T k) (T (k+1))) → (∀ k x, 0 < x → T (k+1) x ≤ T k x) →
        (∀ k x y, 0 < x → x ≤ y → T k y ≤ T k x) → (∀ x, 0 < x → T 0 x ≤ a) →
        ∀ n x, 0 < x → T n x ≤ h + c1 a h / (↑(n+1) + c2 a h)

    rate_all0 :  … → 0 ≤ L → (∀ e, 0 < e → e < E → h − L*e ≤ θh e) → … → 0 < g → g < E →
        ∀ n y, 0 < y → y ≤ g →
          T n y − θh y ≤ max (c1 a h + L*(g + θh g)) ((1 + c2 a h)*(a − h + L*g)) / (↑(n+1) + c2 a h)

    cube_exactRec_rate_top :  0 < u → ∀ k, 0 < x →
        exactRec (cubeNa u) k x ≤ cubeH u + c1 (cubeA u) (cubeH u) / (↑(k+1) + c2 (cubeA u) (cubeH u))

    cube_exactRec_rate_all :  0 < u → ∀ k, 0 < g → g < cubeEstar u →
        exactRec (cubeNa u) k g − cubeHint u g ≤
          max (c1 … + (g + cubeHint u g)) ((1 + c2 …)*(cubeA u − cubeH u + g)) / (↑(k+1) + c2 …)

    rate_zero :  HintPair θna θh a h E → h < a → ∀ (T : ℕ → ℝ → ℝ) (τ : ℕ → ℝ),
        (the four hypotheses on T of rate_top0) → τ 0 ≤ a →
        (∀ k φ B, 0 < φ → φ < 1 → (1 − φ)*τ k ≤ B →
            (∀ γ, 0 < γ → γ ≤ φ*a → γ + (1 − φ)*T k (γ/(1 − φ)) ≤ B) → τ (k+1) ≤ B) →
        ∀ n, τ n ≤ h + c1 a h / (↑(n+1) + c2 a h)

(`T 0`, `exactRec … 0`, `τ 0` are `T₁`, `τ₁` of the report; `c1`, `c2`, `kappa` are defined as in the remark; the
hypothesis on `τ` in `rate_zero` is word for word `hstep0` of their `levels_reach_hint_at_zero`.)  Also `lemma1_top`,
`lemma1`, `lemma2`, `epoch_of_stepLE`, `slope_of_stepLE`, `rate_top` (levels numbered from one).  Both files:
`lake env lean`, exit 0, no error, no warning, no `sorry`/`admit`/`native_decide`/`axiom`; `#print axioms` gives
`[propext, Classical.choice, Quot.sound]` for all thirteen theorems printed (`out/lean_RateCore.log`,
`out/lean_RateFull.log`).
For the cube nothing is assumed: `L = 1` comes from `cubeHint_add_mono` and `cubeHint_zero`, `h < a` from
`cubeHint_lt_cubeNa` at zero.  **So the remark's two displays are machine-checked for the exact recursion of the
cube, for every `u > 0`.**  Not formalised: the limsup; the sentence about the number of levels; that the
exponents of algorithms at accuracy zero satisfy the hypothesis of `rate_zero` (on paper in their §11.19).  Caveat: compiled against the `.olean` files of our tree's existing build (their sources are identical to
the theory tree's; no `lake build` was run).

### 2.4 The constants and the numerical tests

**Constants** (REPLICATION, mpmath at 40 digits, `r13_03_closed_form.py`):

| `u` | `a = KL(p_u‖½)` | `h = KL(Λ₁/u‖½)` | `κ` | `c₁` | `c₂` | `c₁/a` |
|---|---|---|---|---|---|---|
| `0.5` | `0.0302998619808` | `0.00767286647803` | `0.039226642` | `0.20327632` | `6.6446939` | `6.709` |
| `1` | `0.110944071672` | `0.0291391385016` | `0.04264811` | `0.71238485` | `6.3521334` | `6.421` |
| `2` | `0.327813325473` | `0.0972809077466` | `0.056697173` | `1.8130791` | `5.4427633` | `5.531` |

They agree with `t4_rate.py` (`0.03923 / 0.20328 / 6.645`, `0.04265 / 0.71238 / 6.352`, …) and with the remark.

**The closed form against the epoch recursion** (REPLICATION): in exact rational arithmetic, eleven pairs
`(a, h)` — the three cubes, the small-slope pair, integer `d₀`, `h/a` from `0.01` to `0.999` — to `k ≈ 10⁷`: the
three claims (`d' − d > (J+1)κ`; `d_m ≥ d₀ + κ(k_m − 1)`; `h/d_m ≤ c₁/(k + c₂)` at the last level of every epoch)
hold in every epoch; the largest ratio `(h/d_m)/(c₁/(k + c₂))` is `0.959` for the cube at `u = 1` (at `k = 2`) and
tends to one as `h/a → 0` or `1` (`0.99995` at `0.01`, `0.999001` at `0.999`): the closed form cannot be improved
much as a bound for the epoch recursion.  In floating point, 4 016 pairs to `k = 10⁹`: no violation;
`k(B_k − h)/a` at the last level of the last epoch lies in `[1.000000, 1.000276]` (the limsup statement is sharp
for the epoch recursion).

**The recursion of the cube, one-sided** (REPLICATION; `r13_01_cube_recursion.py`, written from Theorem 11.52's
display and Theorem 11.53(d) before `nested_review_R6/` was opened — its hash at that moment is in `NOTES.md`).
*What mine does.*  It carries a nonincreasing step function `Û_k ≥ T_k` on a grid `x₁ < … < x_N = ε*` and a number
`B_k ≥ sup T_k` for the cell `(0, x₁)`.  It can only over-estimate because (1) `T_k` is nonincreasing, so the
value at the left end of a cell bounds the cell; (2) `R` is monotone in `T`; (3) the infimum over `(φ, β)` is
replaced by a minimum over finitely many admissible pairs, parametrised by an outer radius `ρ`
(`β = g − φ·KL(ρ‖p_u)`, so that `φ·θ_na((g−β)/φ) = φ·KL(ρ‖½)` in closed form — no root finding anywhere; the grid
itself is `x_j = KL(ρ_j‖p_u)`); (4) the supremum over `γ` is bounded cell by cell with the right end of the
cell and the value of its left end (a sparse table for the range maxima); (5) `B_{k+1}` comes from the macro
bracket over all cells, the bottom cell included; (6) running minima use that `T_{k+1}` is nonincreasing.  The
only uncontrolled thing is rounding (`10⁻¹⁵`; the margins below are `≥ 10⁻³`).  Self-checks: one step from
`θ_hint` returns values in `[θ_hint, θ_hint + 4·10⁻⁵]` at `u = 1` (both grids); no computed value is below `θ_hint` at any
level (the lower barrier `exactRec_ge_hint`); `B₂` is above the exact `τ₂`.

Grid ratio `1.003` (`N = 6 151` points, `x₁ ≈ 10⁻⁹`), 60 levels; `B_k` is my upper bound of `τ_k`:

| `u` | `(B_k − h)/(c₁/(k + c₂))` at `k = 1, 2, 3, 4, 8, 16, 40, 60` | largest `(Û_k(g) − θ_hint(g))/(A(g)/(k + c₂))` over the grid, `k = 1, 2, 8, 40, 60` |
|---|---|---|
| `0.5` | `0.851, 0.318, 0.149, 0.081, 0.021, 0.0088, 0.0042, 0.0038` | `0.820, 0.306, 0.020, 0.0040, 0.0037` |
| `1` | `0.844, 0.310, 0.145, 0.078, 0.022, 0.0092, 0.0044, 0.0040` | `0.811, 0.297, 0.021, 0.0042, 0.0039` |
| `2` | `0.819, 0.282, 0.130, 0.073, 0.025, 0.0110, 0.0053, 0.0047` | `0.777, 0.267, 0.024, 0.0050, 0.0045` |

**Both bounds hold at all 60 levels and at every grid accuracy, for the three slopes** (also with the grid
ratio `1.01`, `N = 1 853`).  By construction `B_k` is also an upper bound of the `τ_k` at accuracy zero of §11.19,
remark (1) (its recursion is my macro step with the bottom cell at `B_k`), so the first column tests
Proposition R13.1 of §2.5 as well.  The value at `k = 1` is exact, `(a − h)(1 + c₂)/c₁`.  `B_k/a` at `u = 1`:
`0.50081, 0.36209, 0.31124, 0.29016, 0.28051` for `k = 2 … 6` and `0.26326` at `k = 40`, against workstream K's
`0.5006, 0.3613, 0.3108, 0.2898, 0.2803, …, 0.2631` (all below my upper bounds, as accurate estimates must be) and against the
exact `τ₂/a = 0.50041`; their one-sided values are `0.5009, 0.3640, 0.3136, 0.2936, …, 0.2723`.  `(B_k − h)k²/a` is
`0.95, 0.90, 0.78, 0.69, 0.64, 0.63, 0.64, 0.68, 0.71` at `k = 2, 3, 4, 5, 6, 8, 10, 16, 20` and rises afterwards
(`0.98` at 40, `1.40` at 60 — my over-estimate stalls too, later than theirs): "`≈ 0.65/k²`" is right for
`k ≈ 5 … 10` and is not contradicted beyond; at `k = 2, 3, 4` the factor is `0.95, 0.90, 0.78`.
**How meaningful the test is:** it is one-sided and it passes, but from `k = 2` on the margin is a factor three
and more — the recursion of the cube does not stress the proof.  The check that does is §2.3.

**RE-RUN** of `t4_rate.py` (a byte-identical copy placed so that its output lands in my directory — as stored
it writes next to itself): exit 0, "all checks passed: True", output identical to their `out_t4_rate.txt`
except the timing line.

### 2.5 What the statement gives and what it does not

*It gives:* (1) for the exact recursion — the object of `BoundedAccuracy.lean` — an explicit level count:
`T_k(g) ≤ θ_hint(g) + η` as soon as `k ≥ A(g)/η − c₂`, and `sup T_k ≤ h + η` as soon as `k ≥ c₁/η − c₂`; so in the
proof of Theorem 11.54 "then `k` with `T_k(g) < θ_hint(g) + η`" may read `k = ⌈A(g)/η⌉`, and in the proof of
Theorem 11.58 the level with `T_k(ξ/2) < θ_hint(ξ/2) + η/2` is `k = ⌈2A(ξ/2)/η⌉`, which with the
`m ≥ ln(a/h)/φ` two-rung steps makes the total number of levels explicit and `O(1/η)`
(`A(0+) = max{c₁ + h, (1 + c₂)(a − h)}`, `0.742` at `u = 1`).  (2) A quantitative form of Theorem 11.53(c), (d), whose proof is by
contradiction.  (3) With §2.3, the first rate statement about the recursion that is machine-checked.

*It does not give:* (1) the `o(n)` — as they say: the families with `k` nested levels have sub-exponential
factors that nobody has bounded uniformly in `k`, and the algorithmic exponent functions obey
`T̃_{k+1} ≤ min(T̃_k, R[T̃_k])(·⁻) + η₀`, with left limits and a loss per level, so `k` must be fixed before `η₀`.
(2) The true rate: the bound is `O(1/k)`, the recursion of the cube behaves like `0.65a/k²`; at `k = 40`,
`u = 1` the bound is `0.0154` and the truth is below `7·10⁻⁵`.  The count `A(g)/η` is therefore pessimistic by
orders of magnitude (`g = ε*/2`, `η = 0.01a`: about 940 levels by the bound).  (3) Anything better at a fixed
accuracy than at accuracy zero: `A(g) ≥ c₁` for every `g`.  (4) A lower bound on the number of levels.
(5) A statement about the limsup constant for the true recursion beyond `≤ a`.

**Proposition R13.1 [V: `ScienceR13.rate_zero`] (the same rate at accuracy zero).**  Let the `T_k` be as in
statement (a) and let `τ̃₁ ≤ a`, `τ̃_{k+1} ≤ max{(1−φ)τ̃_k, sup_{0<γ≤φa}[γ + (1−φ)T_k(γ/(1−φ))]}` for every `k` and
`0 < φ < 1` — the recursion at accuracy zero of §11.19, remark (1), and of `BoundedAccuracy.lean`, group 2.
Then `max(τ̃_k, sup T_k) ≤ h + c₁/(k + c₂)` for every `k ≥ 1`.  *Proof.*  Apply `rate_of_epochs` to
`P(n, b)` := "`τ̃_n ≤ b` and `T_n ≤ b` everywhere".  Persistence: `τ̃_{n+1} ≤ φa + (1−φ)b` for every `φ`, hence `≤ b`.
Epoch: after `J` applications of Lemma 1, `T_{n+J}(x) ≤ b − x` on `(0, h/J)` and `τ̃_{n+J} ≤ b`; for
`φ < h/(Ja + h)` both entries of the maximum are at most `(1−φ)b`; Lemma 2 for `T_{n+J+1}`.  ∎  It is the
quantitative form of their `levels_reach_hint_at_zero` (which gives "some `τ_k < h + ε`"), and it needs neither
`T_k ≤ τ_k` nor nonnegativity.  Numerically: the first column of the table of §2.4.  That the exponents of the
families at bounded accuracy satisfy the hypothesis is their paper statement (Proposition 11.57(b)), not
examined here.

### 2.6 Is the core a small Lean target?  Yes — done (§2.3).

The recursion on `d` and its closed form took 300 lines of Mathlib-only Lean; Lemma 1, Lemma 2, the epoch,
statement (b), the cube and the sequence at accuracy zero another 640 on top of their three lemmas.  Three
failed compilations in all (two `field_simp` steps, one algebra step), each fixed in one line; the parts for
(b), for the cube and for accuracy zero compiled at the first attempt.

---

## 3. Our reviews as applied  (our finding → their text → verdict)

### 3.1 SCI-REV-0010 / `R10_REPORT.md` → §11.32 (Theorem 11.116, Proposition 11.117), errata of `Y_REPORT.md`

| our finding | their text | verdict |
|---|---|---|
| M1: the direction depends on the slope; `a` below the cube at `u = 3, 4, 6` (`p ≤ 0.3`), `2.5` (`p ≤ 0.2`), `2` (`p = 0.1`); `h` at `u = 4, 6` (`p ≤ 0.2`); only `E` rises at every slope | 11.117(d), with our cell list verbatim, the sentence that "Yes — upwards" is not the answer, four cells re-computed by them; errata (e1); title of the section | **correct**, attributed.  Their four rows reproduced by my own code: `0.495806`, `0.467509`, `0.509682` (96 vertices each; ratios `0.9871, 0.9308, 0.8452`); `h` at `(0.1, 4)`: my bracket `[0.2275, 0.2327]` below the cube's `0.2393` |
| "Between about `u = 1.5` and these values the direction of `a` is open, with every lower bound below the cube" | the same sentence in (d) | **correct** (our words) |
| "(Computed cells only …)" | cells listed in (d); the summary sentences drop the range | **incomplete in the summaries** (m5) |
| mechanism and "no Markov reference can prove it" [H] | "Reading (the division's, heuristic)" for the mechanism; the Markov sentence stated flatly | mechanism **correct**; the other slightly **over-stated** (m12) |
| R10.1 (symmetric envelope; fixed `n`; `O(u³)` not uniform in `n`) | 11.117(b), without "symmetric" and without the remark on uniformity | **over-stated — false as worded** (M1) |
| R10.2 (associated law: `V = ¼Var Σs_i`) | 11.117(b), with the two-line proof | **correct**; the antiferromagnetic example (`0.43` against `1.23` on three sites, `p = 0.7`) re-derived by hand |
| Corollary: structure factor; for `F_∞` upper side proved, lower side a sketch (exact for `E`) | "For the limit `F_∞` the upper side is proved … the lower side is a sketch"; "the limit of the small-slope factor is proved on one side" | **distinction kept**, with a flat sentence before it and a wrong errata line (m2) |
| "the susceptibility" false in general; the general quantity | (b), last sentence; R10.3 in the open list | **correct** |
| m7, m8: `E_∞ = E_F` to `10⁻¹⁰`; `E_∞ ∈ [0.401719, 0.403619]` at `p = 0.1` | (c): "`E_∞ ∈ [0.4017, 0.4037]` with a better reference (the division)"; table (a); errata (e5) with our six digits | **correct**; "`p ≥ 0.14`" is their referee's; (c) has the slip m1 |
| m6: upper ends at `p = 0.1` (`0.062762`, `0.172043`) | table (a): `0.0628`, `0.1730` | **correct for `h`; for `a` the weaker of two valid numbers** (m11) |
| m1, m2, m3, m4, m9, m10 (corrections of record) | errata (e5), (e6); m2 in 11.117(e) with our example | **all present and correct**, except the rounding of m10 (m4 above).  Our example for the truncated residual re-checked by hand |
| their addition: blocks of one site do not show the reversal | (d) and THY-RES-0011 §1 | **confirmed** (REPLICATION): `L = 1` bound/cube for `a`: `1.78 … 1.010` (`p = 0.3`), `2.20 … 1.012` (`0.2`), `2.56 … 1.013` (`0.1`) at `u = 1 … 6`; for `h`: at least `1.075`.  *Not in their text:* with `L = 2` the reversal of `a` already shows at `(0.2, 3)` `0.979`, `(0.1, 4)` `0.885`, `(0.1, 6)` `0.931` (not at `(0.3, 3)`: `1.020`), and of `h` at `(0.1, 4)` `0.998`, `(0.1, 6)` `0.960` |

### 3.2 SCI-REV-0012 / `P4_REPORT.md` → Theorem 11.18a, Propositions 11.18b (d), (e), 11.18c, `StateShares.lean`

| our finding | their text | verdict |
|---|---|---|
| 11.18c(a) false for the completeness part; two-site counter-example | 11.18c(a) rewritten: bounds and sufficient directions (a), (d), (e) survive, completeness fails, our example, attributed; 11.18b(b) "on a product domain" | **correct**.  The example by brute force: 5 of 9 rectangles inside `D`; least member `−3` at the three inner points; `8, 8, 17`; `Δ₁ + Δ₂ = 2 < 3` |
| 11.18c last sentence; our own correction (14 of 40; 34 of 40; 79 %; reference first) | lines 2470–2480, with the admission | **correct**, our numbers |
| 11.18c(c) strengthening (unbounded below on `D ∖ D′`) | (c), attributed, with the reason | **correct** |
| third mechanism of 11.18b(d) | (d), attributed; "all four failures on its instances" | **correct** (ours: all four `g_GB` failures) |
| state-dependent shares; "exist iff `x₀` solves the pairwise relaxation" | (e): statement, proof of soundness, duality in five lines, the two-site witness, an explicit integrality gap | **correct**.  Brute force of the gap (three binary sites, `A = (1,1,1)`, `c₁₂ = c₁₃ = 2`, `T₂₃ = 10`; `c₂₃ = 0` or `2`): `L − L(x₀) = 0, 1, 1, 1, 0, 0, 12 (10), 9 (7)` — `x₀` minimises, with ties at `{1,2}`, `{1,3}`; relaxation value `−½` (HiGHS; exact on a rational grid of the reduced problem) at the point of the text; no shares (`4 > 3`); no joint law has those marginals.  Witness: shares `(½, 5/2)` valid, deficit `3` at `(1,2), (2,1), (2,2)` against `Δ₁ + Δ₂ = 2`.  Own random test: "shares exist ⇔ relaxation solved by `x₀`" in 395 of 395 decided instances, 3 gaps |
| machine check requested (P4-T3(iii)) | `StateShares.lean` | **as requested** (§4) |
| 11.18a(c) rewordings; pair shares pointwise best; coverings are more than shares | (c), (d) | **correct**, with the slip m6, which is ours |
| measured numbers of §1, §2, §6 | "Site form against pair form", "On the division's instances" | **correct** (`11 of 13`, `106 of 110`, `91`, `0.036`, `0.034`, `133 of 136`, `55 of 180`, seven, `132 / 113 / 133`, `6.8`, `129 of 136`, `16.4 / 0.064 / 0.157`), labelled measured and not re-computed |
| — | harness numbers of XI.21 quoted in the text | **stale** (m3) |

### 3.3 Theorem R9.1 (`R9_REPORT.md`, `R9_ADDENDUM.md`, SCI-REV-0009 §4, SCI-REV-0011) → Proposition 11.69b

| part | their text | verdict |
|---|---|---|
| definitions (`A`, `B`, admissible `c₁`, "at chain separation at least 3", clean) | identical; their earlier wordings named | **correct** |
| (a) coboundary; additivity of `q̂` for all bridges | identical, plus "the bonds admissible for the concatenation are the `φ(c₁″)`" | **correct**, attributed |
| (b) clean bridges | identical, plus `0 ∈ 𝒮_M` for `M ≥ 6` (theirs) | **correct** |
| (c) head 2 + tail 3, exact cost `A + B`; bounds `(1,6,10;1)`, `(0,3,4;0)`, attained first at 21 and 14 beads; minimality (8 and 12 beads) | identical; norms `44`, `16`, `β = 60` attained | **correct**; norms re-computed (`44`, `16`, `60`) |
| (d) exact points; `108/(N+3)` | identical | **correct**; `108 = 15 + 54 + 36 + 3` |
| (e) five bridges, determinant 1; profiles generate `ℤ⁴` | ours and a set of their own (4, 5, 7, 8, 10 beads) | **correct**; all three determinants (ours, theirs, ours of SCI-REV-0011) equal `1`, the `4×4` minors of the projections have gcd `1` (exact) |
| (f), (g) | "the division's; read by us, the lemma re-derived, nothing computed"; `7.5` and `5` both quoted | **status kept as ours, read only** — as they say |
| R9b-T1 … T3 (cleaning, the false remark, the interior estimate for every `M ≥ 6`, `m ≥ 13`, `3 132`); R9b-T2 (the false parenthesis) | applied, lines 5975–5981, 6098–6114 | **correct** |

**Their three disagreements with our texts — all right:**
1. *The history of the mutation counts.*  `git show <commit>:experiments/mutation_tests.py` (their commits are in
   our object store): 21 mutations for XXI.1–4 at `5ed4072` (`5 + 5 + 5 + 6`), **24** at `89ac710 … dcdfea6`
   (XXI.5, three more), 28 from `658b77f` (XXI.6, four more).  Our replacement text had "before the review: XXI.1–4
   with 21" (o1).
2. *`out/certificate.txt`.*  Right in substance: the file has coordinates of four bridges, not five.  Their count
   "four of your five" is loose: the four are those of the `ℤ⁴` certificate — `(0,0,1,1;7)`, `(0,0,1,1;8)`,
   `(0,1,3,3;10)`, `(1,6,10,5;13)`, recomputed from the coordinates — and two of them are among the five (o2).
3. *The inheritance of the ends for clean bridges.*  At `24a3c27`, Proposition 11.69b(a): "The concatenation of
   Lemma 11.68 of two clean bridges is a clean bridge".  Our sentence "(You had half of it … without the
   inheritance of the ends)" was written against `658b77f`, where the *report* had the decomposition only (their
   message THY-RES-0007 §1.3 already said "and stay clean", as an observation); our own `R9_ADDENDUM.md` §2 says
   their proof is right in every step.  No text of ours denies it for the sixteenth checkpoint; their sentence
   in the new (a) describes the history correctly.

### 3.4 SCI-REV-0007 / `R6_REPORT.md` → §§11.18–11.19, the two amendments

**(b) The count.**  REVIEW.  Algorithm 2L keeps *one* list of outer points, "each carries a bracket … that is only
ever refined" (line 4392–4394), and runs through the levels `0, …, J`.  So: one reference query; one rung-0 query
per sampled point, at most `8Je²M†` in the whole run — no factor `J + 1`; and for a point refined during level `j`
the last time at rung `l ≥ 1`, inner calls at rungs `1, …, l` at most, of cost at most `l·C_l` (`C` nonincreasing in
the accuracy), with at most `min(8Je²M†, 32KJe³e^{x_{l−1}} + 4K)` such points.  Their display
`1 + 8Je²M† + Σ_{j≤J}Σ_{l≥1} min(…)·l·C(n_i, ξ_l n_i, δ′)` is **right**.  Ours — the repair
"`1 + (J+1)·8Je²M† + …`" of `R6_REPORT.md` m2 — was **only loose** (a valid upper bound; no exponent differs), and
their text says exactly that ("a valid bound as well").  Our own derivation (`R6_REPORT.md` line 262) has
`1 + M̄ + Σ_{l≥1} min{M̄, (J+1)·cnt}·C_l`, which is *tighter* than theirs in the other terms (each point is called
at most once per rung in the whole run, so neither the factor `l` nor the sum over levels outside the minimum is
needed).

**(1a) The first sizes.**  `C_max` by a RE-RUN of our R6 code (byte-identical copies of `ws_R6/everyn.py`,
`r6lib.py`; `φ = 0.5`, design K64), the non-adaptive lower bound by own lines from Theorem 11.45(b) (equal to
R6's column to `10⁻⁶` at every size):

| `u` | scanned | first `n` with `C_max < LB` | failures after it | holds from |
|---|---|---|---|---|
| `1` | every `n` in `1000 … 2100` | **1370** | `1371–1376, 1378–1383, 1390, 1397` | **1398** (to 2100) |
| `2` | every `n` in `300 … 760` | **518** | `520–523, 528–531, 537` | **538** (to 760) |
| `½` | every `n` in `4500 … 4600`; every 50th in `4000 … 5050` | **4524** | `4525–4528, 4530–4533, 4536–4538, 4541, 4544, 4546, 4549, 4554, 4560, 4565` | **4566** (to 4600; yes at `4650 … 5050`) |

All six numbers of the remark are reproduced, and its table (`126.26 / 110.90`, `150.76 / 149.02`,
`153.96 / 155.02`).  Not checked: the entry at `n = 16 000`; the sizes with the lowered cap (`1300, 500, 4150`,
`1275`).

### 3.5 SCI-MSG-0023 (L4-T2) → Theorem 11.110(f)

One reading.  `ln Z = ln Z₀ − μ + ln E e^{−(r−μ)} ≤ ln Z₀ − lo + [W(b, σ²) − b]` at `b = μ − lo`; `b ↦ W(b) − b` is
nonincreasing and `μ ≥ r̄ − η`, so for `lo < r̄ − η`: `ln Z ≤ ln Z₀ − r̄ + η + W(r̄ − η − lo, σ²)` — **correct**, and
it is our `deterministic_bracket_sharp` with its hypothesis.  The gain "between `0` and `2η`", "70 % at `8 k_BT`"
(ours), the three redundant hypotheses: stated and attributed.  Not carried: "at `lo = r̄ + η` read `W(0, v)` as
`0`" (harmless).  The adopted `BennettTwoPoint.lean` differs from our file in exactly two hunks (the provenance
paragraph; the closing `#print axioms` block removed): "declarations unchanged" is true.  Slip: m10.

---

## 4. Lean statements against the wording; harness re-runs

| file | imports in our tree? | what was done | statement against wording |
|---|---|---|---|
| `SoftMinLowerBound.lean` | yes: `GeneralisedDips` and its eleven transitive project imports are identical and built | **copy compiled** (`lean/SoftMinLowerBound_copy.lean` = their file + five appended lines): exit 0, 8 s; axioms `[propext, Classical.choice, Quot.sound]` for `softMin_expected_queries_ge`, `softMinLabel_admissible`, `renyiG_eq`, `renyiG_le_log_card` | Theorem 11.116(c).  Lean: finite `X`, any `f`, any `d : X → X → ℝ`, a finite mixture of deterministic adaptive algorithms, any `ε, δ`, labels admissible, `M` a probability vector, **any `t > 0`** (the report: `0 < t < 1`), **for every `r > ε`** `(1−2δ)·exp(G_t(M) − t r) ≤` expected number of *distinct* points evaluated at `γ*`.  The report states the limit `r ↓ ε` and says so in its parenthesis.  The label is normalised with `ln Z(f + φ)` instead of `ln E_π e^{−φ}`: `γ*` shifts by the constant `ln Z(f)`, nothing changes.  **No hypothesis missing; none added.**  Not in Lean, as they say: `sup_M G_t(M) =` site function, and every number |
| `StateShares.lean` | **no** (`ShareCertificates` is not in our tree) | read in full; not compiled | `secondOrder_certified_of_state_shares` = 11.18b(e): no additivity hypothesis; cover `c i k − (T_ik(a,b) + T_ki(b,a)) ≤ s i k a + s k i b` for changed `a, b`; load against the excitation energy of `M.energy + g`; nonnegativity asked for all states (harmless).  `secondOrder_certified_of_deficit_shares` = (d) (any `w` dominating the deficits; no positive part needed).  `energy_sub_eq_excitations_add_secondDiff`: the identity for the known part.  `stateShare_witness`: the two-site instance; its negative half does not even assume `s ≥ 0`.  **Says what the report says** |
| `BoxBennett.lean` | **no** (`BoxClass`, `BennettTwoPoint` not under `proofs/` in our tree) | read in full; not compiled | `bennett_bracket` = our `bennett_bracket_weights` applied: `w ≥ 0`, a point of positive weight, `b > 0`, floor on the support, variance bound `v` (no `v ≥ 0`) ⇒ `log W − m ≤ log Z ≤ log W − m + W(b, v)`: the first display of 11.110(f).  The sharper end is in the adopted file, not restated here |

**Harness** (RE-RUN, their code from the export, `python3 -I -B … --only "<ID> "`, full mode, seed 20261124; the
harness writes no file): XI.21, XVIII.8, XXV.1, XXV.2, XXV.3 — all `survived`, exit 0, 0.5–4 s each, and the five
result strings are **identical to their stored `docs/falsification_output.txt`**: XVIII.8 `bridges=1312,
pairs=1750, …, closest_108=0.142`; XXV.1 `chains=20, U=80, …`; XXV.2 `block_bound=0.03276, reversal=0.9308`;
XXV.3 expansion in `[0.9971, 0.9995]`; XI.21 as in m3.  The numbers quoted in the text for XXV.2, XXV.3 and
XVIII.8 match; those for XI.21 do not (m3).  Mutations were not run (the audit is being replicated separately).

---

## 5. Requests to the theory division (can be sent as they stand; none is an authorisation)

* **R13-T1 — the rate is refereed and machine-checked; adopt or cite.**  Verdict: correct, every line.  Our file
  `experiments/science/ws_R13/lean/RateFull.lean` (namespace `ScienceR13`; imports `Mathlib` and your
  `BoundedAccuracy`) proves `rate_top0`, `rate_all0` for every `HintPair` with `h < a`,
  `cube_exactRec_rate_top`, `cube_exactRec_rate_all` for the exact recursion of the cube, and `rate_zero` for
  the sequence at accuracy zero; `RateCore.lean` is the Mathlib-only core.  Suggested label of the remark: "[V for the two displays: `ScienceR13.cube_exactRec_rate_top`,
  `cube_exactRec_rate_all` (the Scientific Discovery Division, workstream R13, on top of `StepLE.of_limit`,
  `of_macro`, `at_hint_fraction`); P for the limsup; refereed by that workstream]".  Wording: m7 (i)–(iv), m8, m9.
* **R13-T2 — Proposition 11.117(b): restore "symmetric"** (M1; also in the text of XXV.3), and take the
  replacement sentences of m2 for (b) and for errata (e4).
* **R13-T3 — Proposition 11.117(c): "`p < ½`"** with the gauge sentence (m1).
* **R13-T4 — the numbers of XI.21** in Propositions 11.18b, 11.18c and in THY-RES-0011 §2 (m3): `146 / 138 / 148`,
  two gaps; `10 of 100`.
* **R13-T5 — small corrections of record:** m4 (`0.02997`), m5 (the two summary sentences), m6 (Theorem
  11.18a(c)), m10 (label of Theorem 11.110), m11 (`0.1721` is available), m12 ("heuristic", "symmetric").
* **R13-T6 — offered, at your choice:** `rate_zero` (Proposition R13.1: the same rate for the sequence at
  accuracy zero of §11.19, remark (1) — the quantitative form of your `levels_reach_hint_at_zero`, with the same
  hypothesis `hstep0`); it makes "`τ_k → h`" of that remark `τ_k − h ≤ c₁/(k + c₂)`.  And a remark for (d) of
  11.117: with blocks of two sites the reversal already shows
  at `(0.2, 3)`, `(0.1, 4)`, `(0.1, 6)`.

For our own division (not requests to theory): corrections of record o1–o5 — a line each in the next digest.

---

## 6. How to re-run  (all from `experiments/science/ws_R13/`; `OMP_NUM_THREADS=1`; times on a loaded 4-core machine)

| what | command | time | log (each ends with its last line) |
|---|---|---|---|
| constants; closed form against the epoch recursion | `python3 r13_03_closed_form.py` | 10 s | `out/closed_form.log` |
| own one-sided recursion of the cube | `bash r13_02_run_cube.sh` (= `python3 r13_01_cube_recursion.py <u> 60 <ratio> <json>` six times) | 1.5 min (ratio 1.01), 5–6 min (1.003) each | `out/cube_u{0.5,1.0,2.0}_k60_r{1.01,1.003}.log` |
| exact `τ₂` | `python3 r13_04_tau2.py` | 8 s | `out/tau2.log` |
| RE-RUN of their `t4_rate.py` | `python3 -I -B thy_copy_nested_R6/code/t4_rate.py 40` | 2 min | `thy_copy_nested_R6/out/t4_rate.txt` |
| Lean | `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean experiments/science/ws_R13/lean/RateCore.lean` (18 s), `…/RateFull.lean` (37 s), `…/SoftMinLowerBound_copy.lean` (8 s) | | `out/lean_*.log` |
| blocks of one, two, three sites | `python3 r13_05_blocks_recursion.py` | 4 min | `out/blocks_recursion.log` |
| counter-example to 11.117(b) as worded | `python3 r13_06_small_slope_asym.py` | 24 s | `out/small_slope_asym.log` |
| shares: the three instances, random test | `python3 r13_07_shares_bruteforce.py` | 3 s | `out/shares_bruteforce.log` |
| arithmetic of 11.69b | `python3 r13_08_r9_arith.py` | 1 s | `out/r9_arith.log` |
| first sizes of remark (1a) | `python3 r13_09_separation_scan.py 1.0 1000 2100`; `… 2.0 300 760`; `… 0.5 4500 4600`; `… 0.5 4000 5050 50` | 4, 1, 3, 1 min | `out/sep_scan_u1.log`, `_u2.log`, `_u0.5_window.log`, `_u0.5_coarse.log` |
| harness blocks | `bash r13_10_harness_rerun.sh` | 15 s | `out/harness_rerun.log` |

Not to be cited: `out/sep_scan_u0.5_INCOMPLETE_stopped_not_cited.log` (a run I stopped), and the three
`out/test_*.json` of the first trials.

---

## 7. Not checked

* The Lean *proofs* of the theory division (statements only); `StateShares.lean` and `BoxBennett.lean` were not
  compiled; the build of our tree against which my files compile was not re-made.
* Theorem 11.116(a), (b), (d), (e), (f) and Proposition 11.117(a), (e) beyond a reading; the upper ends of the
  table at `u = 1` (tilt-state recursion); the numbers of referee R11; the helix–coil numbers; the claim
  "`E_∞ = E_F` for `p ≥ 0.14`".  My `h` values for blocks of three sites are brackets at grid points of `t`
  (step `0.005`), not certified between them, and my iteration left the bracket open by `0.005` there.
* Theorem R9.1(f), (g) as stated in 11.69b (read); their verification on `2.5·10⁹` pairs (read; not re-run).
* The cost count of Theorem 11.52 as a whole (only the display and the two amended terms were re-derived); the
  entry `n = 16 000` and the lowered-cap sizes of remark (1a); for `u = ½`, every `n` only in `4500 … 4600`.
* Theorems 11.54 and 11.58 themselves; the sentence on the `o(n)` was read, not examined.
* The measured numbers of ours that their text quotes were compared with our messages, not recomputed.
* The mutation tests of the five harness blocks; the rest of the audit at `63e36f7`.
* The parts of THY-RES-0011 on SCI-MSG-0019 (L3), SCI-RES-0010, SCI-MSG-0022, THY-MSG-0015 (read only).
* Prior art: none searched; no novelty is claimed for anything here.
* Proposition R13.1 (`rate_zero`) is machine-checked and consistent with my one-sided run; its hypothesis was
  not verified for any family of algorithms.

---

## 8. Own errors

1. **Resources.**  The scan "`u = ½`, every `n` in `4000 … 5050`" was started with an estimate of 9 minutes and
   would have run about 26, over the 20-minute limit; I stopped it after 8 minutes and replaced it by a window
   and a coarse scan.  The partial log is kept, marked, and not cited.
2. **A forbidden command.**  In the command that stopped that run I used `sleep 1` and `sleep 2` in the
   foreground (three seconds).  Not repeated.
3. **Lean.**  Three failed compilations before the files passed (two `field_simp` calls that did not clear a
   denominator, one algebra step); the first note on `RateCore.lean` gave 262 lines for a file of 303.  A first
   version of this report called Proposition R13.1 a paper argument; it was formalised afterwards.
4. **A first reading that was too quick.**  I first took "`h ≤ 0.233073`" (THY-RES-0011) and our table's `0.229339`
   for a discrepancy; they are two valid bounds for the same cell (m11, o5).
5. **Independence.**  The constants `κ, c₁, c₂` and Lemma 1/Lemma 2 were re-derived from the *remark* before the
   docstring was opened, but the remark already contains the outline; my re-derivation of the closed form is
   therefore a check, not an independent discovery.  The cube recursion was written before any file of
   `nested_review_R6/` was opened; my block-recursion code before any file of workstream Y, of the harness or of
   our `ws_R10/` code was opened (I had read `R10_REPORT.md` and the logs' numbers).
6. No tool declined an action.

---

## Coordinator's note (2026-11-26, before publication as SCI-REV-0014)

Read in full by the coordinator.  What the coordinator did beyond reading:

1. **The rate, statement (a), re-derived on paper from the three Lean statements as the
   report quotes them** — Lemma 1 (slope `+ (B/h − 1)` per level, range `h/j`), Lemma 2
   (`B → B·a/(a + x₀)`), the epoch map `d′ = d(Ja + h)/(Ja − hd)`, the gain
   `d′ − d = dh(1 + d)/(Ja − hd) > (J + 1)·h·f(d)`, `f(d₀) = ha/((a − h)(a + h)(2a − h))` at
   `d₀ = h/(a − h)`, and the passage to `c₁/(k + c₂)`: every line agrees with §2.2.
   Statement (b) and the limsup were read, not re-derived.
2. **Both Lean files compiled by the coordinator** (`lake env lean`, under a 16 GB
   address-space limit): `RateCore.lean` (303 lines, sha256 `1c7a0d36929ea66f…`) exit 0 in
   20 s; `RateFull.lean` (941 lines, sha256 `824c929aaaa4795f…`) exit 0 in 44 s; no error,
   no warning; no `sorry`, `admit`, `native_decide` or `axiom` in either; thirteen
   theorems printed, all on `propext`, `Classical.choice`, `Quot.sound`
   (`experiments/science/pi_inference/r13_adoption_lean_RateCore.log`, `…_RateFull.log`).
   The three imported files (`BoundedAccuracy`, `CubeHintPair`, `HintRecursion`) are
   byte-identical in our tree and at `63e36f7` (`cmp`).  `cube_exactRec_rate_top` read:
   with `exactRec θna k = T_{k+1}` (their definition) it is the remark's first display.
3. **M1 recomputed with code written from the statement**
   (`pi_inference/r13_adoption_check.py`): the Setting of §11.32 was read in the export
   (envelopes "not necessarily symmetric"; `F*_X(t) = min_Q max_φ (1 − t)D_t(π_φ‖Q)`), the
   proposition's sentence too ("For every finite `(X, π)` and envelope `u·d₀`"), and on
   the two-point example the ratio to the claimed second-order term is
   `0.24696 … 0.24999` and `0.22856 … 0.24874` at `u = 0.4 … 0.025` — the report's table to
   every digit — against `0.99083 … 0.99996` with the symmetric envelope.
4. **m1, m3, m9 checked against the theory division's text and stored output:**
   `E_F(0.7, 1) = 0.054044 < 0.120115 = ln cosh ½` with the formula of their line 10274;
   their report says "153 … 135 … 154 — one integrality gap" where their own
   `docs/falsification_output.txt` has `state=146, const=138, minimiser=148, gap=2`; their
   line 5025 has `0.5006` and `0.2627`.
5. **The constants at `u = 1`** recomputed (`κ = 0.042648`, `c₁ = 0.712385 = 6.421a`,
   `c₂ = 6.352133`) and the epoch recursion run against the closed form in exact
   rationals to level `2·10⁵`: largest ratio `0.9591`, as the report says.
6. **Not checked by the coordinator:** the one-sided recursion of the cube; the
   re-runs of their harness and of `t4_rate.py`; the block recursions; the brute-force
   checks of the share instances; the first sizes; the readings of `StateShares.lean`
   and `BoxBennett.lean`; the minor findings m2, m4–m8, m10–m12 beyond reading them;
   our own slips o1–o5 are taken over as the workstream states them (o3 and o5 were
   compared with the two messages concerned: they are as described).
