# Workstream R16 — review of the certified third level (theory report §11.19, remark (1b); THY-RES-0013 §4), with a replication

*Science division, 2026-11-26 (started 08:43 UTC).  Object: the theory branch at commit `9befefd`,
read-only export `<EXP>` =
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_9befefd/`.
Line numbers below are those of `<EXP>/docs/THEORY_REPORT.md` ("TR"), `<EXP>/docs/workstreams/K_REPORT.md`
("KR"), `<EXP>/docs/collaboration/responses/theory/THY-RES-0013.md` ("MSG"),
`<EXP>/experiments/coordinator_checks/three_levels_certified/` (`README.md`, `cert3.py`).  Scripts, logs and
notes: `experiments/science/ws_R16/`.*

**Kinds of checking**, kept apart throughout: **review** = I re-derived it from the statement;
**replication** = recomputed with my own code written from the statements (`r16lib.py`; nothing of the
theory division imported); **re-run** = their code, run by me from the export with `python3 -I -B`;
**read only**.  Labels: **[P]** paper proof, **[X]** exact finite computation, **[N]** numerical /
model computation.  Everything here is model-relative mathematics (query complexity on `L_u(Q_n)`);
no physical claim is made or examined.

**Read** (in full unless a part is named): `R16_brief.md`, `COMMON.md`; MSG; TR §11.18 from "Bracket procedures" through the proof
of Theorem 11.52 (l.4544–4693), §11.19 Lemma 11.55, Theorem 11.56 with proof and both remarks
(l.4977–5146), Proposition 11.57, Theorem 11.58, remarks (1), (1a), (1b) (l.5148–5410); KR §§1.2–3.4
(Algorithm 2L⁺ §2.2, statement §2.3, the nine steps §2.4, Proposition K0 §3.2, Theorem K2 §3.4), §6.4;
`README.md`, `cert3.py`, `summary.py`, `terms.py`, `out_4000.txt`, `out_16000*.txt`, `out_summary.txt`,
`out_terms_4000.txt` (header and tables); `reviews/R8/r8_flat.py`, `r8_flat3.py`; `DEAD_ENDS.md` D61;
R8's referee report, its minor points m1–m10 (l.108–152); our `R6_REPORT.md` §§2.1–2.4, 2.7–2.9, 3.3 and `R13_REPORT.md` §3.4, and our
R6 code `r6lib.py`, `everyn.py`, `flat_exact.py`; the Computational Research Division's ENG-RES-0014
(copy in the scratchpad, full text) and ENG-RES-0008 (§1, tables `main_u1`, §6, limitations).

---

## 0. Verdict table

| # | what | where | verdict | kind of check |
|---|---|---|---|---|
| 1 | the contract of an inner procedure, written from Theorem 11.56's statement and proof | TR l.4544–4548, 5023–5043; KR l.297–334, 364–453 | written out in §2 | review |
| 1(i) | accuracy: the quantity that must be `≤ x_l` is the *certified* accuracy `x_out` of the two-level run; `cert3.py` enforces it | KR Step 1 (l.378–380), Step 8 (l.443–445); `cert3.py` l.92, 103, 137 | **holds, with a condition to add to the texts** (the tolerance formula as printed is the supremum, not an admissible value; m2) | review + replication |
| 1(ii) | failure probability: each call is designed for `δ′ = δ/(4LM̄)`; the union bound over all calls of all rungs is already inside the outer budget | KR (V1) l.365–366, 373–374; `cert3.py` (`ldelta=ldeltap`) | **holds** | review + replication |
| 1(iii) | cost bound `C_l` in every run; an abort inside an inner run returns the trivial bracket, valid, counted as a failure of that call | TR l.5033–5037; KR l.328–329, 345, 453 | **holds, with a condition to add** (the abort test must precede *every query*; as worded the always-bound is `C_max + M̄`; m1) | review |
| 1(iv) | the objects: every fibre is a member of `L_u(Q_{n_i})`, and Theorem 11.56 is proved for every member and every `n ≥ 2` | TR l.4572; KR l.254–256, 297, 344 | **holds** (through Theorem 11.56 for both middle designs; it would *not* hold through Theorem 11.52, whose failure bound is for `n ≥ n₀(η₀)`) | review |
| 2 | monotonicity; "three levels certified ≤ two levels certified, every `n`; more candidates can only lower it"; the choice is made from the design alone | TR l.5335–5346; MSG l.71–82; `cert3.py` l.112–151 | **holds**; held fixed: the whole outer design `(n, n_o; λ, η, η′, θ, ν₁; b; δ; x₀…x_L)`, hence `J, ν₀, r†, M̄, K, δ′, cnt, x_out` | review + replication (every server choice reproduced by a code that evaluates no instance) |
| 3 | replication of the certified columns | README table; `out_*.txt`, `out_terms_*.txt` | **reproduced**: 159 of 159 certified numbers (8 sizes, every outer fraction of their outputs) to four digits; 1 950 of 1 950 per-rung fields at `n = 4 000` (two fractions) and `16 000`; their `summary.py` output identical; one line of `cert3.py` identical | replication + re-run |
| 4 | what the comparison with "the worst instance found for two levels" proves | TR l.5375–5385, 5397–5408; MSG l.105–113, 131–135 | a theorem on the three-level side against a model computation on the other; **one major finding** (M1: at five of eight sizes the two-level number belongs to another outer design) and one sharpening (m3: without search and without the mean-run model the comparison is true from `n = 16 000` on and false at `4 000`, `8 000`) | review; replication (three-level side, the two ladders, flat cost at seven cells); re-run (flat cost on grids); read only (the division's searches) |

**In one paragraph.**  The rule of THY-RES-0013 §4 is right: a two-level run of Theorem 11.56, designed
for the fibre dimension, a certified accuracy at most `x_l` and the failure probability `δ′` of the level
above, *is* an inner procedure in the sense of the theorem, the bound `C_max` is coordinatewise
nondecreasing in the `C_l` with everything else fixed by the outer design, and `cert3.py` designs its
candidates exactly so.  I found no critical error and no error in the mathematics.  Every certified number
of the section is reproduced by independent code.  What needs correcting is on the *other* side of the
comparison: the two-level worst cases at `n = 1 400, 2 000, 8 000, 32 000, 64 000` are for a two-level
algorithm with a different ladder than the design they are compared with (M1), "at the level of
expectations" is a model, not an expectation (m3), and two sentences state a rule or a formula slightly
differently from what the proof and the code need (m1, m2).

---

## 1. Findings by severity, with replacement texts

### Critical

None.

### Major

**M1 — the two-level side of the comparison mixes two outer designs; "(β) … the two-level algorithm of the
same outer design" is not what was computed at `n = 8 000, 32 000, 64 000`** (TR l.5357–5366 the table,
l.5376–5381 (β), l.5397–5402; MSG l.89–98, 105–113; README l.42–51, 60–67, 160–162; `summary.py` l.18–27).
*Review + replication.*

The certified three-level bound is computed for "the outer level of your §2" (MSG l.86): constants
`b = 0.5, λ = 0.2, η = η′ = θ = 0.05, δ = 0.05` and the referee's ladder `x_l = x₀(b/x₀)^{l/40}`
(`r8_flat.py` l.106).  The two-level worst cases come from two messages of the Computational Research
Division:

* `n = 1 000, 4 000, 16 000`: ENG-RES-0014, table `three_worst` — "Design copied from the referee's script
  … a geometric ladder of 40 rungs" (its §2): **the same outer design**;
* `n = 1 400, 2 000, 8 000, 32 000, 64 000`: ENG-RES-0008, table `main_u1` — its §1 says "Design
  parameters: those of your table (§6.4): … ladder of inner rates `ε*·0.85^i` (`i < 40`)", the ladder of
  remark (1a) (TR l.5303–5304) and of our R6: **the same constants, another ladder** (31 to 41 rungs
  depending on `n`; first inner accuracy `ε*n_i` instead of `x₀(b/x₀)^{1/40}`).

That these are two designs is not a matter of reading: with the ladder `ε*·0.85^i` my code gives the
two-level certified bound `ln C_max/(na) = 0.9913, 0.8700, 0.7228, 0.6387, 0.5887, 0.5596, 0.5419` at
`n = 1 400, …, 64 000` (`φ = 0.50`) and `1.1720` at (`1 000`, `0.55`) — ENG-RES-0008's column "cap `C_max` at
that `φ`" to every digit it prints (`0.991, 0.870, 0.723, 0.639, 0.589, 0.560, 0.542; 1.172`) — and with
the referee's ladder `0.9933, 0.8721, 0.7262, 0.6415, 0.5899, 0.5646, 0.5407; 1.1854`, the two-level
column of the table under review (`r16_ladders.py`, `logs/ladders.log`).  Both ladders are "geometric
ladders of 40 rungs" (KR §6.4 l.844 says so of the first — workstream K's `flat_cost_bounded.py` l.66 has
`estar * 0.85 ** i` — and TR l.5353–5354 of the second), which is presumably how the two came to be
treated as one; README l.37–38 and l.160 call the table's design "the
parameters of the report's §6.4", and l.160–162 say that "a two-level design with another ladder … has
not been searched" — five entries of the column are exactly that.

*Consequence.*  No number is wrong; five entries of the column are attributed to an algorithm they do not
belong to, and the sentence (β) asserts for five sizes what was computed for two (`4 000`, `16 000`).  The
conclusion is not in doubt numerically: where both ladders were searched (reading (A)) the worst cases are
`1.040` against `1.0461` at `n = 1 000`, `0.694` against `0.6940` at `4 000`, `0.576` against `0.5753` at
`16 000` — at most `0.006` apart (at (`1 000`, `0.55`), the one cell where both are at the same fraction,
`1.0536 − 1.040 = 0.014`, which is also the difference of the two certified bounds there) — while the margins at `8 000, 32 000, 64 000` are `0.09` to `0.11`.
But as written the statement is not supported, and the margins `0.09, 0.11, 0.10` (`e^{82}, e^{377},
e^{702}`) are differences between quantities of two designs.

*Replacement text for (β)* (TR l.5376–5381; the same content for MSG l.105–113 and README l.60–67):

> (β) **from `n = 4 000` on the certified bound of three levels is below the worst instance found for two
> levels.**  At `n = 4 000` and `16 000` the two-level algorithm is the one of the same outer design, at
> every outer fraction of the division's grid (ENG-RES-0014; mean runs on searched instances; margins
> `0.07`, `0.10` in these units, factors `e^{32}`, `e^{172}`).  At `n = 8 000, 32 000, 64 000` it is the
> two-level algorithm of ENG-RES-0008, which has the same constants and **another ladder** (inner rates
> `ε*·0.85^i`; certified two-level bound `0.639, 0.560, 0.542` where the design of this table has
> `0.6415, 0.5646, 0.5407`), with inner answers placed adversarially (margins `0.09, 0.11, 0.10`); where
> both ladders were searched the two worst cases differ by at most `0.006`.

and in the table (TR l.5357–5366, MSG l.89–98, README l.42–51) a mark on the entries `0.924, 0.822, 0.619,
0.550, 0.537`: "† ENG-RES-0008: ladder `ε*·0.85^i`, not the ladder of this table".  README l.37–38:
"outer level with the constants of the report's §6.4 (`b = 0.5`, …) and the referee's ladder
`x_l = x₀(b/x₀)^{l/40}` — not the ladder `ε*·0.85^i` of §6.4, of remark (1a) and of ENG-RES-0008".
Alternatively the three numbers can be recomputed for the table's design (request R16-THY-1).

### Minor

**m1 — the abort rule in the statement of Theorem 11.56 bounds the cost by `C_max + M̄`, not `C_max`**
(TR l.5033–5037: "before every inner call the algorithm checks that the call does not take the number of
queries beyond `C_max`"; KR l.328–329 still has the after-the-fact rule).  *Review.*  The run makes three
kinds of queries: the reference query, one query per new outer point (its trivial bracket), and inner
calls.  With the test before inner calls only, the point queries are untested: in a run off the good event
the last inner call that passes the test can leave the count anywhere up to `C_max`, a doubling of `M` then
draws new points (one query each) before the next inner call is refused, and the run ends with up to
`C_max + M̄ − K` queries (`M ≤ M̄` holds in every run, TR l.5040).  The text of Theorem 11.52 has the right
rule (TR l.4602–4604: "Before every query — the one query that gives a new outer point its trivial
bracket, and every call of an inner procedure, counted with its cost bound").  It matters here because the
nesting consequence charges a middle run exactly `C_l = C_max`: a slack of `M̄` per call would be a factor
up to `3/2` in `C_l`, i.e. up to `0.0009` in the units of the table at `n = 4 000`.  With the rule stated
for every query nothing changes in any number (on the good event no test fails: claim (vi), KR l.353–354).
The finding is about what the stated rule *proves*: I did not construct a run that exceeds `C_max`, and in
the `2 648` stored runs of our R6 harness — which implements exactly the rule "before every inner call"
and has `142` budget aborts — none does (read from `ws_R6/data/`).
*Replacement* (TR l.5033–5037):

> (The cost bound holds always: before every query — the one query that gives a new outer point its
> trivial bracket, and every inner call, counted with its cost bound `C_l` — the algorithm checks that it
> does not take the number of queries beyond `C_max`, and aborts with the trivial bracket otherwise; …)

**m2 — "the largest [tolerance] its accuracy allows, `b = x − ln(e^c(1+c)/(1−c) + 2c)`" is the supremum,
not an admissible tolerance; and "an accuracy at most `x_l`" should say *certified* accuracy** (TR
l.5337–5339, 5370–5371; MSG l.100–103; README l.27–28, 74–78).  *Review + replication.*  A two-level run
in dimension `d` with `λ = η = η′ = θ = c` and tolerance `b` has certified accuracy
`x_out = ln[(2p_u)^d + e^b·A(c)]`, `A(c) = e^c(1+c)/(1−c) + 2c` (TR l.5028).  So `x_out ≤ x` iff
`b ≤ x − ln A(c) + ln(1 − (2p_u)^d e^{−x})`, which is *below* the printed value; with the printed value
`x_out = ln[(2p_u)^d + e^x] > x` and the run is not an inner procedure of accuracy `x` (by `10^{−673}` at
`d = 2 500`: no arithmetic sees it, and at the last rung, where `x_L ≤ b` is needed for the classification
to end, it would still be a violation of the hypothesis).  The code is right: `cert3.py` l.92 takes
`b = x − ln A(c) − 10⁻⁶`, admissible as soon as `(2p_u)^d ≤ e^x(1 − e^{−10⁻⁶})`, i.e. for `d ≥ 23` at
`u = 1` (it is used for `d ≥ 400`), and l.103, l.137 compare the certified accuracy with `x`.  In my
replication the certified accuracy of a chosen two-level server never exceeds the rung's: it equals
`x_l` to rounding for the extensive design (`θ` chosen so), `x_l − 10⁻⁶` for the bounded design with the
largest tolerance, and is well below `x_l` with `b = x/2` (e.g. `3.74` at `x_l = 5`).  The assertions allow
`x_out ≤ x + 10⁻⁹`; nothing uses that slack beyond rounding (largest excess observed: `0`).
*Replacement* (TR l.5370–5371 and the two other places):

> … with tolerance `x/2` or the largest its accuracy allows — any `b` with
> `(2p_u)^d + e^b(e^c(1+c)/(1−c) + 2c) ≤ e^x`; the computation takes
> `b = x − ln(e^c(1+c)/(1−c) + 2c) − 10⁻⁶` —

and TR l.5337–5339: "a two-level run (Algorithm 2L⁺ with its abort rule) designed for the fibre dimension,
a **certified** accuracy `x_out ≤ x_l` and a failure probability at most `δ′` is an admissible inner
procedure, with `C_l` its own `C_max`".

**m3 — "at the level of expectations" is the mean-run model, and it is not needed from `n = 16 000` on**
(TR l.5279–5281, 5376–5381, 5397–5403; MSG l.105–113, 131–135).  *Review; replication and re-run for the
numbers.*  The two-level numbers are costs of *mean runs* (ENG-RES-0008, "Epistemic status": "every count of the
algorithm is replaced by its mean"; ENG-RES-0014, "Assumptions and limitations": "Everything is at the
level of expectations").  A
mean-run cost is neither the expected number of evaluations nor the number of evaluations of a run (the
control flow depends on the counts through thresholds); its agreement with literal runs was measured at
`n_o ∈ {48, 120, 300}`, `n_i = 6` only (ENG-RES-0008 §6).  So (β) compares a theorem with a model
computation, and "needs more evaluations (at the level of expectations)" will be read as "in
expectation".  There is one instance where no model is involved: at `ψ = 0` the two-level run with base
brackets inside is deterministic (every fibre is the zero function, on which the base bracket is
`[1/(1+η), 1/(1−η) + 2^{−d}E_r̂]` whatever the samples), so its number of evaluations is exact and is a
lower bound on the worst case of that algorithm in every sense.  Against it (§5, table):

* from `n = 16 000` on the certified three-level bound is below the exact two-level cost at the flat
  instance at **every** outer fraction (grid of step `0.01` from `0.30` to `0.85`; minima `0.5027, 0.4998,
  0.4961` against `0.4782, 0.4439, 0.4381` at `n = 16 000, 32 000, 64 000`; at `16 000` every second `n_o`
  around the minimum: `0.4991`) — a margin of `37` nats at `16 000`, and on the grid `198` and `412` nats
  at the two larger sizes;
* at `n = 4 000` and `8 000` it is **not**: two levels at the flat instance cost `e^{0.5336na}` (at
  `φ = 0.63`) and `e^{0.5110na}` (`φ = 0.59`), *less* than the certified three-level bounds `0.6106` and
  `0.5262`, for `φ ∈ [0.56, 0.71]` and `[0.58, 0.60]`.  On the division's grid of step `0.05` this
  concerns `φ = 0.60, 0.65, 0.70` at `n = 4 000` (at its nine other fractions the exact flat cost of two
  levels already exceeds the three-level bound — at `φ = 0.55` by `0.003`) and `φ = 0.60` at `n = 8 000`.
  At those fractions (β) rests on non-flat searched instances in the mean-run model (worst found `0.7936,
  0.8466, 0.9027` at `n = 4 000`: margins `e^{81}` and more, so the claim is very plausible — and not a
  theorem).

*Replacement* for the bold sentence of remark (1) (TR l.5279–5281):

> **with the server of each rung chosen by certified cost, the certified bound of three levels is below
> the worst two-level instance found (mean runs) from `n = 4 000` on, and below the exact cost of two
> levels at the flat instance, at every outer fraction, from `n = 16 000` on** (remark (1b)).

and after (β) (TR l.5381), with numbers the theory division should recompute with its own evaluator
(request R16-THY-4):

> Two levels "at the level of expectations" means mean runs — every random count replaced by its mean; a
> model whose agreement with literal runs was measured at `n_o ≤ 300`, not an expected number of
> evaluations.  Without a search and without that model: from `n = 16 000` on the certified three-level
> bound is below the exact cost of the two-level algorithm at the flat instance at every outer fraction
> (on a grid of step `0.01`: minima `0.503, 0.500, 0.496` against `0.478, 0.444, 0.438`), so there the two-level algorithm as built
> needs — in every run on the zero function — more evaluations than three levels need in any run on any
> instance; at `n = 4 000` and `8 000` two levels at the flat instance with `φ ≈ 0.6` are cheaper than the
> three-level bound, and (β) rests on the searched instances.

### Observations (no change requested, or outside the offered section)

* **o1 — `τ₂/a` is not a finite-`n` lower bound for what two levels pay.**  With the base brackets' own
  answers the exact two-level cost at the flat instance, at its best outer fraction (step `0.01`), is
  `0.5336, 0.5110, 0.5027, 0.4998, 0.4961` at `n = 4 000, …, 64 000` — below `τ₂/a = 0.5004` from
  `n = 32 000` on (*re-run* of their `flat_run`; *replicated* with our own engine at the minimum cells of
  `n = 4 000`, `8 000`, `16 000` and `32 000` — `0.5336, 0.5110, 0.5027, 0.4998` — and at (`16 000`, `n_o = 9 024`):
  `0.4991`; so the value below `τ₂/a` at `n = 32 000` is replicated, the one at `64 000` is not).  The
  figures of remark (1) (TR l.5223–5225: `0.55, 0.52, 0.51`, "limit `τ₂/a`") are for another design
  (workstream K's: the ladder `ε*·0.85^i`, inner brackets `[W, We^x]`, a coarse grid of `φ`); for the
  design of (1b) the flat instance is cheap *again* for the level below (my reading **[H]**: on a flat
  fibre the base bracket returns far less width than it promises — ENG-RES-0014, table `k0_answers` — so
  points are classified at coarser rungs) — the same "best case twice over" as for three levels.  So (γ) ("below `τ₂/a`") is a statement about a limit, not a comparison of
  the two algorithms at that `n`; see §5.
* **o2 — finer outer fractions** (own code only; not cross-checked with theirs).  `n = 64 000`: the
  certified three-level bound is `0.4341` at `φ₁ = 0.275` (their two fractions: `0.4381` at `0.25`);
  `n = 8 000`: `0.5259` at `0.325` (theirs `0.5262` at `0.30`); `n = 4 000`: `0.6180, 0.6120, 0.6140, 0.6248`
  at `0.36, 0.37, 0.38, 0.39` — `0.6106` at `0.375` stands; `n = 32 000`: `0.4575`, `0.4629` at `0.225`,
  `0.275` — `0.4439` stands.  The two-level certified bound at `n = 32 000` is `0.5622` at `φ = 0.49` (their
  evaluator on the grid of step `0.01`, and mine: `0.5725, 0.5622, 0.5646, 0.5748` at `0.48 … 0.51`), below
  the table's `0.5646` at `0.50`: "nothing is optimised" covers it, and it changes no comparison.
* **o3 — the base bracket with an integer sample size.**  Proposition K0 takes
  `M = ⌈K2^d/((1−η)|B(d,r*)|)⌉`; their evaluator does not round (`r8_flat.py` l.85: "M taken without
  rounding up").  With the integer `M` the tail radius `r̂` is *below* `r*` at the coarsest rungs (where
  `r* = d − 1`: 10 to 12 of 40 rungs), and the base bracket's answer on the flat fibre is narrower there.
  The cost at the flat instance is the same to four digits in the three cells where I ran both variants
  — no number is affected.

---

## 2. The contract of an inner procedure, and the two-level run against it

### 2.1 The contract, from the statement and the proof of Theorem 11.56 *(review)*

Outer level: a design `D = (u; n, n_o; λ, η, η′, θ, ν₁; b; δ; x₀ > x₁ > … > x_L)` with `n ≥ 2`,
`1 ≤ n_o ≤ n − 1`, `n_i = n − n_o`, `0 < λ ≤ 1`, `0 < η ≤ ½`, `0 < η′ ≤ 1`, `θ > 0`, `ν₁ ≥ 1`, `x₀ = 2un_i`,
`x_L ≤ b` (TR l.5023–5025; KR l.297–300).  Its constants `J, ν₀, r†, π†, m_max, K, ν, M†, M̄, δ′, cnt(·)`,
its certified accuracy `x_out` and the coefficients of `C_max` are functions of `D` alone (KR l.304–307).
The procedure `I_l` that serves rung `l` (`1 ≤ l ≤ L`) is bound by the following and by nothing else.

| | clause | decided by |
|---|---|---|
| C1 | **Object.**  For an outer point `a ∈ Q_{n_o}` the fibre `ψ_a = ψ(a, ·)` on `Q_{n_i}`; `ψ_a ∈ L_u(Q_{n_i})`; the target is `W(a) = 2^{−n_i}Σ_b e^{−ψ_a(b)} = A(ψ_a)` — the same problem in dimension `n_i`, uniform reference measure.  The outer level already holds the fibre's trivial bracket `[e^{−ψ_a(0)−un_i}, e^{−ψ_a(0)+un_i}]` (one query; ratio `e^{x₀}`). | (F1), TR l.4572; KR Lemma K.2 l.254–256; algorithm step 1, KR l.312–315 |
| C2 | **Output.**  A pair `L ≤ U` (a pair with `L > U` may be replaced by the trivial bracket). | TR l.4546, 5035–5037 |
| C3 | **Accuracy and validity.**  For every fixed `ψ_a ∈ L_u(Q_{n_i})`, with probability at least `1 − δ′` over the procedure's own randomness (independent of the outer sample): `L ≤ W(a) ≤ U` **and** `U ≤ e^{x_l}L`.  Only the ratio is used: Step 1 needs `e^{x_L} ≤ e^b` at the last rung, Step 8 needs `U ≤ e^{x_{l−1}}L` at the rung before a call.  A procedure whose guaranteed ratio is `e^{x′}` with `x′ ≤ x_l` qualifies; where in `[L, U]` the truth lies is free. | definition TR l.4544–4548; KR (V1) l.365–366; Step 1 l.378–380; Step 8 l.443–445 |
| C4 | **Failure probability.**  `δ′ = δ/(4LM̄)` *per call*, for every member of the class. | TR l.5024–5025; KR l.306 |
| C5 | **How often.**  At most once per pair (point, rung) in the whole run, brackets being only refined; the potential calls are the pairs `(i, l)`, `i ≤ K2^{m_max} < 2M̄`; on the good event `I_l` is called at most `min{M̄, (J+1)·cnt(x_{l−1})}` times. | KR l.313–315, 365, 445–446; claim (vi) l.353–354 |
| C6 | **Union bound.**  Over *all potential calls of all rungs*: `L·K2^{m_max}·δ′ < 2LM̄δ′ = δ/2`.  The other `δ/2` pays for the Chernoff events (V2), (V3) of the outer sample, `(J+1)(m_max+1)(L+2)` of them, through `K`.  Not per rung, not absorbed otherwise, and nothing further to divide by. | KR l.371–374 |
| C7 | **Cost.**  At most `C_l` queries in *every* run on every member — not only on a good event.  This is what lets the outer level test its own budget before a call. | TR l.4546–4548 ("the bound `C` … holds always") |
| C8 | **What the outer level does at its budget.**  Before a query that would take its count beyond `C_max` (each inner call counted with `C_l`) it stops and returns its own trivial bracket `[s₀, s₀e^{2un}]` — valid for every `ψ`, of ratio `e^{2un}`; likewise if a point is unclassified at rung `L` or level `J` is left.  On the good event none of this happens (claims (i), (vi)); off it the cost bound is all that is claimed, plus the width of a bracket returned through the closure test. | TR l.5033–5041 (with m1); KR l.328–329, 345, 453 |

Nothing else is asked: no monotonicity of the cost in `x` or `δ′` (that belongs to *families*, TR l.4548–4550,
and is not used by Theorem 11.56), no independence between calls (a union bound), no property of the
distribution of the cost.

*Three lines I re-derived because the nesting leans on them.*  (a) The probability of the good event:
(V2) fails at one `(j, M)` with probability `≤ e^{−η²K/2}`, (V3) at one `(j, M, t)` with probability
`≤ e^{−η²K/(3(1+η))}` (Chernoff above `μ ≥ K/(1+η)`, domination below); there are `(J+1)(m_max+1)` and
`(J+1)(m_max+1)(L+1)` of them; `K = ⌈3(1+η)η^{−2}ln(2(J+1)(m_max+1)(L+2)/δ)⌉` makes the total `≤ δ/2`; and
`m_max = ⌈log₂(M̄/K)⌉` gives `M̄ ≤ K2^{m_max} < 2M̄`.  (b) The width (Step 4), term by term:
`s₀ = (2p_u)^n ℓ₀`; populated levels `≤ c_η^{−1}e^{λ+b}Σ`; negligible levels `≤ η′e^bℓ`; tail `≤ θe^bℓ` — hence
`x_out = ln[(2p_u)^n + e^b(e^λ(1+η)/(1−η) + η′ + θ)]`, the formula that m2 uses.  (c) Proposition K0: the
three events, `t⁺`, `t⁻`, both tail lemmas, `r̂ ≤ r*`, failure `≤ 4e^{−η²K/(3(1+η))} ≤ δ′` with
`K = ⌈3(1+η)η^{−2}ln(4/δ′)⌉`; cost exactly `2M`.  No gap found.  Steps 2, 3, 5, 6, 7, 9 of the proof I did
not re-derive this time (our R6 did; read only here).

### 2.2 A two-level run against the contract, as `cert3.py` designs it *(review; replication where stated)*

Both middle designs of `cert3.py` are instances of **Theorem 11.56** in dimension `d = n_i` — the
"extensive" one (`λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, `b′ = x/4`, `θ = e^{x−b′} − (3e+1) − (2p_u)^d e^{−b′}`,
l.69–81) and the "bounded" one (`λ = η = η′ = θ = c = min(x/12, ⅓)`, `ν₁ = 2e^un_o′/θ`, `b′ = x/2` or the
largest admissible, l.82–109) — each with base brackets on a geometric ladder of 30 rungs inside.

**(i) Accuracy — holds, with a condition to add to the texts (m2).**  The quantity to compare with `x_l`
is the certified accuracy `x_out` of the two-level run (larger than its tolerance `b′` by
`ln(e^λ(1+η)/(1−η) + η′ + θ)` plus the `(2p_u)^d` term), because C3 asks for the ratio of the returned
bracket and Theorem 11.56 certifies `U ≤ e^{x_out}L` (KR l.342, 355), nothing smaller.  `cert3.py`
compares exactly this (`r['xout'] <= x + 1e-9`, l.103, l.137).  The extensive design has `x_out = x`
exactly (the choice of `θ`); the bounded design with `b′ = x/2` has `x_out ≤ x` because `ln A(c) < x/2`
for `c = min(x/12, ⅓)` (`ln A(c) ≤ 5c` on `(0, ⅓]` — checked numerically, largest ratio `4.997` — so
`ln A(c) ≤ 5x/12` for `x ≤ 4`, and `ln A(⅓) = 1.24 ≤ x/2` for `x ≥ 4`; the term `(2p_u)^d` fits into the
remaining `e^x(1 − e^{−x/12})` for every `d` in use); with the "largest" tolerance see m2.  The tolerance `b′` itself is handled as the theorem requires: it is the last
rung of the middle run's own ladder (`x′_{30} = b′`, served by a base bracket of accuracy `b′`).
*Replication:* over all two-level servers chosen in all my runs the largest value of `x_out − x_l` is `0`
(the column "max(xout − x_l)" of `logs/rep_*.log`; the values that occur are `0`, `−7·10⁻¹⁵`, `−10⁻⁶`,
`−0.054`), and the hypotheses of the theorem are asserted for every candidate design (`r16lib.Level.__init__`: parameter ranges, a
strictly decreasing ladder with `x′_L ≤ b′`, `1 ≤ n_o′ ≤ d − 1`) — no assertion failed.

**(ii) Failure probability — holds.**  By C4/C6 each call needs failure probability at most `δ′` of the
level above, and the union over the calls of all rungs is already paid for by the factor `4LM̄` in `δ′`.
`cert3.py` passes `ldelta=ldeltap` to every candidate (l.80–81, 84–85, 101–102), `ldeltap` being the
outer `ln δ′ = ln δ − ln(4·40) − ln M̄` (`r8_flat.py` l.131); the middle run then derives its own `K` from
that `δ` and hands `δ″ = δ′/(4·30·M̄′)` to its base brackets (same line, one level down).  So the design
does **not** need `δ′` divided by the number of calls a second time.  *Replication:* my code does the same
by construction and reproduces the certified cost of every best candidate to four digits; the digits
would show a different budget — at `n = 4 000`, `φ₁ = 0.375` (`ln δ′ = −253.9`) the server of the finest
rung has `K′ = 496 086` and is certified at `0.5291`; designed for the outer `δ = 0.05` instead it would
have `K′ = 44 461` and `0.5219`.

**(iii) Cost bound and aborts — holds, with a condition to add (m1).**  `C_l` is the middle run's own
`C_max`, which holds in every run *because of its abort rule* — in the form "before every query" (m1).  An
abort inside a middle run returns `[s₀′, s₀′e^{2ud}]` with `s₀′ = e^{−ψ_a(0)−ud}`: the very bracket the outer
level already holds for that point (C1).  It is valid for every fibre, so it cannot make the outer bracket
invalid; it has ratio `e^{x₀} > e^{x_l}`, so it is a *failure of that potential call* in the outer event
(V1).  Its probability is inside `δ′`: on the middle run's good event, of probability `≥ 1 − δ′`, no abort
occurs (claim (i), KR l.345).  Hence on the outer good event no middle run aborted, and the outer
accuracy claim — made on that event — is untouched.  After an aborted call the outer level simply moves
the point to the next rung; if the point ends unclassified at rung `L`, or the budget would be exceeded,
the outer level aborts with its own trivial bracket (C8), off its good event.

**(iv) The objects — holds.**  Theorem 11.56 is stated for every `ψ ∈ L_u(Q_n)` and every `n ≥ 2`, with no
"for `n` large" (KR l.297, 344; our R6 §2.2), and its reference point is arbitrary (`ψ₀` enters only
through `s₀` and `ℓ₀`).  A fibre of a member of `L_u(Q_n)` is a member of `L_u(Q_{n_i})` (restriction to a
subcube; the Hamming distance is additive over blocks), and the fibre average is the quantity `A` of the
theorem in dimension `n_i`.  So the two-level run is proved for exactly the objects it is called on; that
`flat_run` evaluates *costs at the flat fibre* is irrelevant for the columns `tuned` and `searched`, which
use only `C_max`.  One distinction worth a clause in the text: admissibility is through Theorem 11.56 —
Algorithm 2L of Theorem 11.52 would not qualify for every `n` (its failure bound is proved for
`n ≥ n₀(η₀)`, TR l.4621–4622).

### 2.3 The statement that the section uses, with its hypotheses

**Proposition R16.1 (nesting, every `n`) [P: two applications of Theorem 11.56 — theirs, refereed (R8),
re-derived by our R6; this is the "Nesting" and "Monotonicity" of remark (1b) with the hypotheses
written out].**  Let `D` be an outer design as in §2.1.  For each rung `l` let `𝒫_l` be a finite set of
procedures, each a bracket procedure for (dimension `n_i`, accuracy `x_l`, failure probability `δ′(D)`)
with a cost bound valid in every run — for instance (a) the base bracket of Proposition K0 for
`(n_i, x_l, δ′)`, or enumeration; (b) Algorithm 2L⁺ in dimension `n_i` with a design `D′` that satisfies the
hypotheses of Theorem 11.56, has `x_out(D′) ≤ x_l` and `δ(D′) ≤ δ′(D)`, tests its budget before every
query, and is itself served by procedures admissible for its own triples `(n_i′, x′_k, δ′(D′))`.  Let
`c_l` be the smallest cost bound in `𝒫_l` and `I_l` a procedure attaining it (a choice made from the
designs alone).  Then Algorithm 2L⁺ with design `D` and inner procedures `I_1, …, I_L`

1. makes at most `B(c) = 1 + 2M̄ + Σ_l min{2M̄, (J+1)·cnt(x_{l−1})}·c_l` evaluations in every run on every
   `ψ ∈ L_u(Q_n)`;
2. returns, with probability at least `1 − δ`, `L ≤ A ≤ U` with `U ≤ e^{x_out(D)}L`;
3. `B` is nondecreasing in every `c_l`; so enlarging any `𝒫_l` cannot raise `B`, and `B` is at most the
   two-level bound of `D` as soon as every `𝒫_l` contains the base bracket.

*Proof.*  A procedure of kind (b) is, by Theorem 11.56 in dimension `n_i` (applicable to every fibre by
(F1)), a bracket procedure for `(n_i, x_out(D′), δ(D′))` with cost `C_max(D′)`, hence one for the weaker
triple `(n_i, x_l, δ′(D))`.  Theorem 11.56 for `D` gives 1 and 2.  The coefficients of the `c_l` are
positive and are functions of `D` alone: 3.  ∎

---

## 3. The monotonicity argument: what is held fixed *(review; replication for the last point)*

From `C_max = 1 + 2M̄ + Σ_l min{2M̄, (J+1)·cnt(x_{l−1})}·C_l`:

* **`J`, `ν₀`** depend on `(u, n, n_o, λ, η, η′, ν₁, b)`; **`r†`, `π†`** on `(u, n_o, η, θ, ν₀)`; **`m_max`,
  `K`, `ν`, `M†`, `M̄`** on these and `(L, δ)`; **`cnt(x)`** on `(η, λ, ν)` and the *ladder value* `x`;
  **`δ′`** on `(δ, L, M̄)`; **`x_out`** on `(u, n, λ, η, η′, θ, b)`.  None of them contains anything of an
  inner procedure.  The dependence runs one way: the triple `(n_i, x_l, δ′)` an inner procedure must be
  designed for is a function of the outer design; nothing flows back.
* **Tolerance.**  `b` is tied to the inner procedures only through the hypothesis `x_L ≤ b`: the server
  of the last rung must certify a ratio `≤ e^b`.  Every candidate does (`x_out ≤ x_L = b`); so `b`, and
  with it the certified accuracy `0.8715` of the outer level, is the same for two and for three levels.
* **Failure budget handed down.**  `δ′` is fixed by the outer design; a server must meet it, and its cost
  grows with `ln(1/δ′)`, but the outer design does not change with the server.
* **The accuracy the server actually certifies.**  If the server of rung `l − 1` certifies `x′ < x_{l−1}`,
  the multiplier `(J+1)·cnt(x_{l−1})` of rung `l` stays valid (it could be lowered to `(J+1)·cnt(x′)`; the
  bound does not use this).  A server certifying more than `x_{l−1}` would not be admissible.  So again
  nothing in the outer design moves.

Hence, with **the whole outer design held fixed** — `n`, the outer fraction, the five constants, `b`, `δ`,
the number of rungs and the ladder — and every server admissible for its rung's triple, monotonicity in
the `C_l` alone *is* the whole argument for "three levels certified ≤ two levels certified, for every
`n`" and for "more candidates can only lower it".  Two remarks on its scope.  (1) It is a statement at a
fixed outer fraction; the table's columns are minima over a grid of fractions, and the inequality passes
to the minima because both columns are computed on the same grid (it does: every line of `out_*.txt`
carries both; in my logs `searched ≤ tuned ≤ two levels` at all 54 pairs `(n, φ₁)`, strictly from
`n = 1 400` on at the best fraction).  (2) It compares two *upper bounds*; that the three-level
*algorithm* is cheaper than the two-level one is a different statement — §5.

**"Decided before any evaluation, from the design alone" — true.**  In `cert3.make_inner` (modes `tuned`,
`searched`) the server is `min(cands, key = lCmax)` and it replaces the base bracket iff `lCmax < c0`
(l.144–145), `c0` being the base bracket's cost, a design quantity; the candidate lists are built from
design quantities only (l.73–79, 91–108: the fractions, the three stop rules on `2u(d − n_o′) ≤ 1.5b′`,
`x_out > x`, `lCmax` not improving; the gates l.127, 134).  The flat-instance quantities that `flat_run`
also returns enter assertions only (l.137–139).  *Replication:* my code contains no evaluation of any
instance at all, and it reproduces the server of every rung and the design string of the best candidate
in all 1 950 per-rung fields compared (§4.3).

---

## 4. The replication: numbers against theirs

### 4.1 What was written, and what was read to write it

`r16lib.py` (own code, from the statements): tables on `Q_m` with **exact integer** binomial coefficients
and ball sizes (logarithms by `math.log`), `E_r` and `T_m(k)` as sums of positive terms
(`E_r = (e^u − 1)Σ_{i≤r}e^{u(r−i)}|B(m,i)|`, from `E_r = e^uE_{r−1} + (e^u − 1)|B(m,r)|`); class `Level` =
the constants of Theorem 11.56 in the order of KR §2.2; `k0` = the family of Proposition K0; the
candidates and the rule.  No flat-instance run, no instance of any kind.  Nothing of the theory division
is imported.  Their code was **read** to resolve the following ambiguities of the *design* (marked
`[RESOLVED-BY-READING]` in the file):

1. the ladder: `x_l = x₀(b/x₀)^{l/L}`, `x_L = b` (`r8_flat.py` l.106) — *not* the ladder `ε*·0.85^i` that KR
   §6.4, remark (1a) and our R6 use (this is M1);
2. `n_o = ⌊φn⌋` evaluated in floating point and clipped to `[1, n−1]` (`r8_flat.py` l.100–101);
3. the referee's extensive candidates: the second outer fraction is `min(0.8, 1.5·φ₂)`, and a candidate
   with `2u(d − n_o′) ≤ 1.5b′` is skipped (`r8_flat3.py` l.48–51);
4. the added candidates: `b_max = x − ln A(c) − 10⁻⁶`; fractions `0.50, 0.45, …, 0.20`, stopping at the
   first whose bound does not improve, whose `x_out` exceeds `x`, or with `2u(d − n_o′) ≤ 1.5b′`
   (`cert3.py` l.89–109);
5. the gates: no two-level candidate where `x/d ≥ 0.9ε*` or `d < 50`; the added candidates only where the
   base bracket costs more than `e^{0.2da}` (`cert3.py` l.127, 134);
6. the base bracket: enumeration when it is cheaper; their `M` is not rounded up (I round, below `e^{40}`:
   invisible).

### 4.2 The table *(replication)*

`ln(bound)/(na)`, `u = 1`, at the best outer fraction of their grid (in brackets).  Mine / theirs:

| `n` | two levels: certified | servers by certified cost, the referee's two middle designs | the same with more middle designs |
|---|---|---|---|
| 1 000 | 1.1384 (0.5) / 1.1384 | 1.1384 (0.5) / 1.1384 | 1.1384 (0.5) / 1.1384 |
| 1 400 | 0.9933 (0.5) / 0.9933 | 0.9669 (0.45) / 0.9669 | 0.9659 (0.45) / 0.9659 |
| 2 000 | 0.8721 (0.5) / 0.8721 | 0.8120 (0.45) / 0.8120 | 0.8118 (0.45) / 0.8118 |
| **4 000** | **0.7262 (0.5) / 0.7262** | **0.6331 (0.4) / 0.6331** | **0.6106 (0.375) / 0.6106** |
| 8 000 | 0.6415 (0.5) / 0.6415 | 0.5890 (0.4) / 0.5890 | 0.5262 (0.3) / 0.5262 |
| 16 000 | 0.5899 (0.5) / 0.5899 | 0.5500 (0.45) / 0.5500 | 0.4782 (0.3) / 0.4782 |
| 32 000 | 0.5646 (0.5) / 0.5646 | 0.5400 (0.45) / 0.5400 | 0.4439 (0.25) / 0.4439 |
| 64 000 | 0.5407 (0.5) / 0.5407 | 0.5325 (0.45) / 0.5325 | 0.4381 (0.25) / 0.4381 |

Per outer fraction at `n = 4 000` (mine; equal to `out_4000.txt` in all 21 numbers):

| `φ₁` | 0.30 | 0.35 | 0.375 | 0.40 | 0.425 | 0.45 | 0.50 |
|---|---|---|---|---|---|---|---|
| two levels | 0.9359 | 0.8822 | 0.8553 | 0.8261 | 0.7992 | 0.7723 | 0.7262 |
| tuned | 0.7352 | 0.6919 | 0.6387 | 0.6331 | 0.6596 | 0.6718 | 0.7261 |
| searched | 0.6485 | 0.6214 | 0.6106 | 0.6331 | 0.6596 | 0.6718 | 0.7261 |

**Every certified number of their stored outputs** — the two-level bound, `tuned`, `searched`, at every
`(n, φ₁)` of `out_small.txt`, `out_4000.txt`, `out_8000*.txt`, `out_16000*.txt`, `out_32000*.txt`,
`out_64000*.txt` — against mine: **159 of 159 equal to the four digits printed** (`r16_compare_all.py`,
`logs/compare_all.log`; per size 21, 21, 21, 21, 21, 24, 20, 10).  The stopping condition of the brief
("the first number that differs") was not met: none differs.  Run times of my code, all three columns and
all fractions: `2 s` (`n = 4 000`), `14 s` (`16 000`), `33 s` (`32 000`), `67 s` (`64 000`); peak memory
`136 MB`.

### 4.3 The per-rung choice *(replication)*

`r16_cert.py --terms` against `out_terms_4000.txt` and `out_terms_16000.txt` (`r16_compare_terms.py`): per
rung the accuracy, the multiplier (cap or count, and its value), the cost of the base bracket, the
certified bound of the best two-level candidate, its design string (middle design, tolerance, outer
fraction of the middle run), the server, and the term of `C_max`.

| `n`, `φ₁`, mode | rungs served by a two-level run (mine = theirs) | fields compared | differ |
|---|---|---|---|
| 4 000, 0.375, tuned | 20–21, 28–40 (15 of 40) | 325 | 0 |
| 4 000, 0.375, searched | 20–21, 24–40 (19) | 325 | 0 |
| 4 000, 0.40, tuned | 21, 28–40 (14) | 325 | 0 |
| 4 000, 0.40, searched | 21, 24–40 (18) | 325 | 0 |
| 16 000, 0.30, tuned | 15–21, 30–40 (18) | 325 | 0 |
| 16 000, 0.30, searched | 15–40 (26) | 325 | 0 |

The descriptions of the text check against my tables: at `n = 16 000`, `φ₁ = 0.30`, the bounded design
serves the rungs of accuracy `0.5` to `106` with an outer fraction of its own falling from `0.50` to `0.30`,
the extensive one those of `138` to `404`; at the finest rung the base bracket costs `e^{0.7691na}` and the
two-level run is certified at `e^{0.4323na}`; the bound is the term of rung 14 (accuracy `528`, a base
bracket at the sample cap).  The example of remark (1b) and D61 (`n = 4 000`, `φ₁ = 0.40`, the rung of
accuracy `9.8`): base bracket `0.5122`, the referee's first extensive design (`φ₂ = 0.1312`) certified at
`0.7041` — reproduced; the flat cost `0.223` of that middle run I did not compute.  The two coincidences of MSG l.118–122 (the
column of the referee's two designs equals the referee's "`C_max` with flat middle costs" at (`4 000`, `0.40`)
and (`16 000`, `0.45`): `0.6331`, `0.5500`): in my tables the bound is there the term of a rung served by a
base bracket at the sample cap (rung 14, accuracy `194`; rung 12, accuracy `761`), as the message says.

### 4.4 Cross-check of my code against exact arithmetic *(replication, own codes)*

`r16_validate.py`: `r16lib` (float64 logarithms) against our R6 implementation (`ws_R6/r6lib.py`,
`everyn.py`: exact integers, Fractions, 40-digit mpmath; written before any code of the theory division
was read).  Tables on `Q_{300}`, `Q_{1500}`, `Q_{2500}`: logarithms agree to `7·10⁻¹³`.  The outer level at
`n = 4 000`, `φ₁ = 0.375` and `0.5`, and two middle designs in dimension `2 500` (bounded, `x = 0.5`, largest
tolerance, `φ₂ = 0.5`; extensive, `x = 50`, `φ₂ = 0.7466`): `J`, `r†`, `m_max`, `K` identical (e.g. `45 202`,
`355`, `340`, `30 212`); `ln ν₀`, `ln M̄`, `ln δ′`, `x_out` to `10⁻⁸`; the base-bracket costs at all rungs
to `1.1·10⁻⁴` in the logarithm (R6 rounds `η` down to a multiple of `10⁻⁶`); `ln C_max` to `1.7·10⁻⁵`.
No check differs.

### 4.5 Re-runs of their code *(re-run)*

From the export with `python3 -I -B`; the export had `1 240` files before and after, no `__pycache__`, no
file newer than mine.

* `summary.py` → `logs/rerun_summary_runpy.log` (through `runpy`, so that the log ends with the peak RSS;
  a first plain run is in `logs/rerun_summary.log`): output byte-identical to their stored `out_summary.txt`,
  including its line "54 of 54 numbers agree" for the cross-check with ENG-RES-0014.
* `cert3.py 4000 0.375 tuned,searched` → `logs/rerun_cert3_4000_0375.log`: two levels `0.8553`, `tuned`
  `0.6387`, `searched` `0.6106` — their stored line, and mine; `30 s`, `37 MB`.
* `r8_flat.flat_run` (two levels at the flat instance) on grids of the outer fraction — §5.

---

## 5. What the comparison proves

**The paragraph asked for.**  One side of the comparison is a theorem: for the outer design of the
table, with the servers fixed by the rule, the three-level algorithm makes at most `e^{B₃}` evaluations
in every run on every member of `L_u(Q_n)` and returns a bracket of ratio `e^{0.8715}` with probability
`0.95` **[P: Proposition R16.1; X: `B₃`, replicated]**.  The other side is a lower estimate of the worst
case of *one* two-level algorithm: that the instances were *found by a search* does no harm — any
instance is a witness, and a search can only understate a maximum — but the number attached to each
witness is the cost of a **mean run**, a model of the algorithm, not a proved lower bound on its number
of evaluations **[N]**; at five sizes the algorithm searched has another ladder than the design of the
table (M1), where only reading (A) exists its inner answers are placed adversarially (not the algorithm
as built), and "two levels" means that one family with the outer fraction on a grid of step `0.05`, not
two-level algorithms as a class.  So "three levels beat two levels from `n = 4 000` on" is **not a theorem
about the two algorithms as designed**; it is a theorem-against-model comparison whose margin (`e^{32}`
at `n = 4 000`) makes the conclusion very plausible, and it would become a theorem with one lemma: a lower
bound, holding with positive probability, of the two-level algorithm's evaluations at the witness by a
fixed fraction of its mean-run cost.  It *is* a theorem already — given Theorem 11.56 and the arithmetic of a deterministic run — with no
search and no model, from `n = 16 000` on and at every outer fraction scanned, if the witness is the flat
instance, where the two-level run is deterministic and its cost exact (table below); and with that
witness it is false at `n = 4 000` and `8 000`.  The limits
`τ₂/a = 0.500` and `τ₃/a = 0.361` are asymptotic worst-case exponents of the best two- and three-level
designs, with unquantified `o(n)`: they say that for large `n` three levels win by `e^{(τ₂−τ₃)n}`, and they
measure how far the finite-`n` certificate still is from what three levels can reach (`0.438` against
`0.361` at `n = 64 000`); they bound nothing at a given `n` — the two-level algorithm as built costs less
than `e^{τ₂n}` at the flat instance from `n = 32 000` on (o1) — so "(γ) below `τ₂/a` from `n = 16 000` on"
is a remark about a limit, and the finite-`n` content of (γ) is exactly the flat-instance comparison of
the table.

`ln(·)/(na)`, `u = 1`, the outer design of the table:

| `n` | certified three-level bound (mine = theirs) | two levels at the flat instance, exact: minimum over `φ ∈ {0.30, 0.31, …, 0.85}` (at `φ`) | fractions at which two levels at the flat instance cost no more than the three-level bound | two levels: worst found, mean runs, (B) / (A) |
|---|---|---|---|---|
| 2 000 | 0.8118 | 0.5818 (0.68) | 38 of 56 (`0.48 … 0.85`) | — / 0.822† |
| 4 000 | 0.6106 | 0.5336 (0.63) | 16 of 56 (`0.56 … 0.71`) | 0.6829 / 0.6940 |
| 8 000 | 0.5262 | 0.5110 (0.59) | 3 of 56 (`0.58 … 0.60`) | — / 0.619† |
| 16 000 | 0.4782 | 0.5027 (0.56); every second `n_o` in `[8 880, 9 120]`: 0.4991 | none | 0.5749 / 0.5753 |
| 32 000 | 0.4439 | 0.4998 (0.54) | none | — / 0.550† |
| 64 000 | 0.4381 | 0.4961 (0.53) | none | — / 0.537† |

† ENG-RES-0008: the ladder `ε*·0.85^i` (M1).  Column 3: *re-run* of their `r8_flat.flat_run`
(`r16_rerun_flat2.py`, `r16_rerun_flat2_local.py`; `logs/rerun_flat2_a.log`, `_b.log`,
`rerun_flat2_local_16000.log`).  *Replicated* with our own engine — the literal pass-by-pass engine of
workstream R6 (exact arithmetic) with an oracle that returns the base bracket's deterministic answer on
the zero fibre (`r16_flat_own.py`; for `n ≥ 16 000` `r16_flat_own_fast.py`, a copy of the engine's loop with
an exact shortcut at the levels where no point can be high, checked against the unmodified engine at
`n = 4 000` and `8 000`: same evaluations, levels, last sample, closing radius, width): `0.9839` at (`1 000`, `0.50`), `0.6670` at
(`4 000`, `0.50`), `0.5336` at (`4 000`, `0.63`), `0.5110` at (`8 000`, `0.59`), `0.5027` at (`16 000`, `0.56`),
`0.4991` at (`16 000`, `n_o = 9 024`), `0.4998` at (`32 000`, `0.54`) — theirs: the same seven numbers.  So
the minimum cell of column 3 is replicated at every size from `4 000` to `32 000`; `64 000` is re-run only.
Column 5: read only.

**Statement R16.2 (three levels against two, without a search and without the mean-run model) [P:
Proposition R16.1, and the determinism of the two-level run at `ψ = 0`; X: the numbers — the three-level
side replicated, the two-level side re-run on the grid and replicated at its minimum cells for
`n = 16 000` and `32 000`, re-run only for `64 000`].**  Let
`u = 1`, `n ∈ {16 000, 32 000, 64 000}`, and let `D(φ)` be the outer design of the table with outer fraction
`φ`.  For every `φ ∈ {0.30, 0.31, …, 0.85}` the two-level algorithm `D(φ)` with base brackets inside makes,
in **every run on the zero function**, at least `e^{0.5027na}`, `e^{0.4998na}`, `e^{0.4961na}` evaluations
(at `n = 16 000` at least `e^{0.4991na}` for the `n_o` scanned around the minimum), while the three-level
algorithm of the column "more middle designs" makes at most `e^{0.4782na}`, `e^{0.4439na}`, `e^{0.4381na}`
evaluations in **any run on any member** of `L_u(Q_n)`; both return a bracket of ratio `e^{0.8715}` with
probability `0.95`.  At `n = 4 000` and `8 000` the same comparison fails for `φ ∈ [0.56, 0.71]` and
`[0.58, 0.60]`.  Not covered: outer fractions off the grid (between grid points the flat cost moves by a
few thousandths), `φ < 0.30` or `> 0.85` (the cost increases away from the minimum on both sides of the
grid), two-level designs with another ladder or other constants.

---

## 6. Requests to the theory division (can be sent as they stand; none is an authorisation)

* **R16-THY-1 (M1).**  In TR §11.19 remark (1b) (table and (β)), THY-RES-0013 §4 and the README of
  `three_levels_certified/`, mark the two-level worst cases at `n = 1 400, 2 000, 8 000, 32 000, 64 000` as
  belonging to the design of ENG-RES-0008 (ladder of inner rates `ε*·0.85^i`, `i < 40`; certified
  two-level bound `0.991, 0.870, 0.639, 0.560, 0.542` at `φ = 0.50`), not to the outer design of the table
  (ladder `x_l = x₀(b/x₀)^{l/40}`; `0.9933, 0.8721, 0.6415, 0.5646, 0.5407`), and replace "the two-level
  algorithm of the same outer design" by the text of §1, M1.  If you prefer the sentence as it stands:
  ask the Computational Research Division for the two-level worst case *of the table's design* at
  `n = 8 000, 32 000, 64 000` (reading (B) if possible); stopping condition: three numbers, or the first
  that is below the certified three-level bound.
* **R16-THY-2 (m1).**  State the abort rule of Theorem 11.56 for every query, as Theorem 11.52's text
  does (replacement in §1), and bring KR §2.2 step 3 in line.  No number changes.
* **R16-THY-3 (m2).**  Replace "the largest its accuracy allows, `b = x − ln(e^c(1+c)/(1−c) + 2c)`" by the
  admissible form (§1) in the three places, and write "certified accuracy `x_out ≤ x_l`" in the
  "Nesting" sentence; one clause there on *which* theorem makes a two-level run admissible would help a
  reader who nests further: Theorem 11.56 (failure bound for every `n`), not Theorem 11.52 (for
  `n ≥ n₀(η₀)`).  Proposition R16.1 (§2.3) is offered as the statement with its hypotheses.
* **R16-THY-4 (m3).**  Say in (β) that the two-level numbers are mean runs, and add the comparison that
  needs neither a search nor that model: the exact two-level cost at the flat instance, minimised over
  the outer fraction, against the certified three-level bound — by our re-run of your evaluator (and, at the minimum
  cells up to `n = 32 000`, by our own engine) `0.5336, 0.5110, 0.5027, 0.4998, 0.4961` against `0.6106, 0.5262, 0.4782, 0.4439, 0.4381` at
  `n = 4 000, …, 64 000`: true from `n = 16 000` on, false at `4 000` and `8 000`.  Please recompute these
  on a grid you choose (ours: step `0.01`, and every second `n_o` around the minimum at `n = 16 000`),
  and say whether the minimum over *every* `n_o` is wanted.  (γ) can then point to it: "below `τ₂/a`" is a
  remark about a limit, this is its finite-`n` content.
* **R16-THY-5 (the missing lemma).**  If "(β) from `n = 4 000` on" is to be a statement about the two
  algorithms: a lower bound for the number of evaluations of Algorithm 2L⁺ (base brackets inside) at the
  division's worst instances for the fractions where the flat instance does not suffice — at `n = 4 000`
  the grid fractions `0.60, 0.65, 0.70` (mean-run costs `e^{0.7936na}, e^{0.8466na}, e^{0.9027na}`), at
  `n = 8 000` the fraction `0.60` — holding with positive probability and within a factor `e^{−81}` of the
  mean-run cost (the smallest margin to the three-level bound among these at `n = 4 000`).  A crude
  concentration argument on the good event should do; nobody has written it.
* **R16-THY-6 (o1, o2; optional).**  (a) Remark (1), TR l.5223–5225: say that the flat-instance figures
  `0.55, 0.52, 0.51` are for workstream K's design and a coarse grid of `φ`, and that with the base
  brackets' own answers and the outer fraction on a grid of step `0.01` the two-level cost at the flat
  instance is `0.534, 0.503, 0.4998, 0.4961` at `n = 4 000, 16 000, 32 000, 64 000` — below `τ₂/a = 0.5004`
  at the last two sizes.
  (b) `n = 64 000`: at `φ₁ = 0.275` our code gives the certified three-level bound `0.4341` (your two
  fractions: `0.4381`); to be confirmed with `cert3.py 64000 0.275 searched`.

---

## 7. How to re-run

All from `experiments/science/ws_R16/`, `OMP_NUM_THREADS=1`; every script prints its peak RSS in its last
line; every log cited in this report reached that line.  `<EXP>` as in the header.

    python3 -B r16_cert.py 4000 0.30,0.35,0.375,0.40,0.425,0.45,0.50 two,tuned,searched > logs/rep_4000.log     # 2 s
    python3 -B r16_cert.py 1000 0.30,0.35,0.40,0.45,0.50,0.55,0.60 two,tuned,searched > logs/rep_1000.log       # 1 s; likewise 1400, 2000
    python3 -B r16_cert.py 8000 0.25,0.275,0.30,0.35,0.40,0.45,0.50 two,tuned,searched > logs/rep_8000.log      # 5 s
    python3 -B r16_cert.py 16000 0.25,0.275,0.30,0.325,0.35,0.40,0.45,0.50 two,tuned,searched > logs/rep_16000.log   # 14 s
    python3 -B r16_cert.py 32000 0.20,0.25,0.30,0.35,0.40,0.45,0.50 two,tuned,searched > logs/rep_32000.log     # 33 s
    python3 -B r16_cert.py 64000 0.20,0.25,0.45,0.50 two,tuned,searched > logs/rep_64000.log                    # 67 s, 136 MB
    python3 -B r16_compare_all.py <EXP>/experiments/coordinator_checks/three_levels_certified logs > logs/compare_all.log
    python3 -B r16_cert.py 4000 0.375,0.40 tuned,searched --terms > logs/rep_terms_4000.log
    python3 -B r16_cert.py 16000 0.30 two,tuned,searched --terms > logs/rep_terms_16000.log
    python3 -B r16_compare_terms.py logs/rep_terms_4000.log <EXP>/experiments/coordinator_checks/three_levels_certified/out_terms_4000.txt > logs/compare_terms_4000.log
    python3 -B r16_compare_terms.py logs/rep_terms_16000.log <EXP>/experiments/coordinator_checks/three_levels_certified/out_terms_16000.txt > logs/compare_terms_16000.log
    python3 -B r16_validate.py > logs/validate.log                         # against ws_R6 (exact arithmetic); 1 s
    python3 -B r16_ladders.py 1000,1400,2000,4000,8000,16000,32000,64000 0.50,0.55 > logs/ladders.log      # M1; 2 s
    python3 -B r16_cert.py 4000 0.36,0.37,0.38,0.39,0.55,0.60,0.65 two,tuned,searched > logs/rep_4000_extra_fractions.log   # o2; likewise 8000, 32000, 64000
    python3 -I -B <EXP>/experiments/coordinator_checks/three_levels_certified/summary.py > logs/rerun_summary.log           # their code (the cited log rerun_summary_runpy.log: the same through runpy, command in its first line)
    python3 -I -B r16_rerun_flat2.py <EXP>/experiments/reviews/R8 logs 2000,4000,8000,16000 > logs/rerun_flat2_a.log        # their flat_run; 131 s
    python3 -I -B r16_rerun_flat2.py <EXP>/experiments/reviews/R8 logs 32000,64000 > logs/rerun_flat2_b.log                 # 453 s, 162 MB
    python3 -I -B r16_rerun_flat2_local.py <EXP>/experiments/reviews/R8 16000 8880 9120 2 > logs/rerun_flat2_local_16000.log   # 145 s
    python3 -B r16_flat_own.py 4000 0.5 rstar > logs/flat_own_4000_050_rstar.log        # our R6 engine at the flat instance; 20 s
    python3 -B r16_flat_own.py 4000 0.63 int > logs/flat_own_4000_063_int.log           # 33 s
    python3 -B r16_flat_own.py 8000 0.59 rstar > logs/flat_own_8000_059_rstar.log
    python3 -B r16_flat_own_fast.py 4000 0.5 rstar > logs/flat_own_fast_4000_050_rstar.log          # the engine with the exact shortcut; 6 s
    python3 -B r16_flat_own_fast.py 8000 0.59 rstar > logs/flat_own_fast_8000_059_rstar.log         # 18 s
    python3 -B r16_flat_own_fast.py 16000 n_o=9024 rstar > logs/flat_own_fast_16000_no9024_rstar.log   # 79 s, 187 MB
    python3 -B r16_flat_own_fast.py 16000 0.56 rstar > logs/flat_own_fast_16000_056_rstar.log          # 76 s
    python3 -B r16_flat_own_fast.py 32000 0.54 rstar > logs/flat_own_fast_32000_054_rstar.log          # 430 s, 387 MB

The one line of `cert3.py` was run through `runpy` so that the peak RSS could be printed (the command is
the first line of `logs/rerun_cert3_4000_0375.log`).

---

## 8. Not checked

* **The proof of Theorem 11.56 beyond what touches the inner procedures.**  Re-derived here: the good
  event and its probability, Step 1, the width (Step 4), Step 8, the abort accounting, Proposition K0.
  Steps 2, 3, 5, 6, 7, 9 (certificates, validity, closing radius, sample sizes, the count, termination):
  read only this time; our R6 re-derived them (`R6_REPORT.md` §2.3–2.4).
* **The flat-instance columns** of the table (costs of the `tuned`/`searched` designs at the flat
  instance: `0.9839 … 0.4237`) and the modes `flat`, `cert` (servers chosen at the flat fibre): not
  replicated — they need the flat-instance run of a *three*-level design.  Of the mode `cert` only the
  certified bound and the base cost at the one rung quoted in the text.  The *two*-level flat cost is
  re-run on grids and replicated at seven cells only (none at `n = 64 000`).
* **The Computational Research Division's numbers** (worst instances, readings (A) and (B), the mean-run
  evaluator, the literal runs): read only; none of their code was run.  ENG-RES-0008 and ENG-RES-0014 were
  read from copies in the scratchpad, not from their branch.
* **Whether real runs follow mean runs at `n ≥ 4 000`** (the lemma of R16-THY-5): not attempted.
* **The exact two-level flat cost at every `n_o`**: grids of step `0.01`, and every second `n_o` in one
  window at `n = 16 000`; between grid points the cost is a saw-tooth of amplitude about `0.002` around a
  V-shaped curve (seen in that window), which I did not bound.
* **Exact-arithmetic confirmation of my floating-point evaluation** beyond four designs at `n = 4 000`
  (§4.4); a threshold comparison within `10⁻¹²` of a tie would move `r†` by one — none was seen, and the
  agreement with their independent evaluator at 159 numbers makes it unlikely.
* **Other slopes** (`u ≠ 1`), **four levels**, the lowered cap of the remark after Theorem 11.56 inside the
  nested bound, the Lean files, prior art: nothing.
* **A literal three-level run** (small cubes, real brackets, both abort rules): not done here; the
  admissibility is a consequence of the theorem's statement, and R8 and our R6 ran such nests on
  `Q_9`–`Q_10` earlier.  **A run that exceeds `C_max` under the rule of m1**: not constructed.
* **Prior art**: not part of this brief; nothing searched.

---

## 9. Own errors

1. My first re-run of `cert3.py` used `/usr/bin/time`, which does not exist on this machine (exit 127;
   nothing ran; the log was overwritten by the second attempt through `runpy`).
2. The first version of my tables kept lists of exact binomial coefficients (0.3 GB at `m = 51 200`); I
   changed it to a streamed computation before the large sizes.  The logs of `n = 4 000` and the
   validation had been produced with the first version and showed the same numbers; all logs cited were
   produced again after the change.
3. In `r16_flat_own.py` I first asserted that the tail radius of the base bracket equals `r*`.  With the
   integer sample size of Proposition K0 it does not at the coarsest rungs; the assertion failed at the
   first run, I then ran both conventions (o3).
4. I started from the expectation that "the design of §6.4" is one design; our own R6 code (`everyn.py`,
   ladder `ε*·0.85^i`) would have "replicated" the two-level bound as `0.7228` instead of `0.7262` at
   `n = 4 000`.  Reading `r8_flat.py` l.106 resolved it before any number was produced — and led to M1.
5. One tool action was declined: a foreground `sleep 60; cat <log>` while I waited for my own background
   job.  I did not retry or work around it; the job's completion notice arrived and the log was read
   then.  Recorded in `NOTES.md`.
6. I started the pass-by-pass engine at `n = 16 000` (`r16_flat_own_light.py`) without estimating its run
   time; it needs about `2.6` million passes.  I stopped it myself after ten minutes, before the
   twenty-minute limit (one `kill` of its PID); its log did not reach the last line, says so, and is not
   cited.  The cell was then computed in `79 s` with the exact shortcut (`r16_flat_own_fast.py`).

---

## Coordinator's note (added 2026-11-26 after the hand-back; not part of the workstream's report)

*What the coordinator did with this report before it was sent as SCI-REV-0016.*

* **Read in full.**
* **Re-read in the export of the theory branch at `9befefd`:** `r8_flat.py` l.100–107 (the ladder
  `x_l = x₀(b/x₀)^{l/L}`); TR l.5350–5385 (the table and (α)–(γ): the five entries `— / 0.924, 0.822,
  0.619, 0.550, 0.537` and the words "the two-level algorithm of the same outer design"); TR l.5026–5043
  and l.4600–4606 (the two abort rules, as quoted in m1); the accuracy formula (TR l.5028) and
  `cert3.py` l.88–104 (`bmax = x − acc_const(c) − 1e-6`; `if r['xout'] > x + 1e-9: break`).  **In the
  Computational Research Division's messages:** ENG-RES-0008 l.84 ("ladder of inner rates `ε*·0.85^i`
  (`i < 40`)") and its table (worst found `0.924, 0.822, 0.694, 0.619, 0.576, 0.550, 0.537`; cap `C_max`
  `0.991, 0.870, 0.723, 0.639, 0.589, 0.560, 0.542`; `1.172` at (`1 000`, `0.55`)); ENG-RES-0014 l.67–68
  ("Design copied from the referee's script … a geometric ladder of 40 rungs").  M1 is confirmed by
  these readings.
* **Re-ran** (outputs in the scratchpad, compared with the workstream's logs after removing time
  stamps): `r16_ladders.py` — identical; `r16_cert.py 4000 …` — identical; `r16_validate.py` —
  identical; `r16_compare_all.py` — "159 of 159"; `r16_flat_own_fast.py 4000 0.5 rstar` — `0.6670`;
  `r16_flat_own.py 4000 0.63 int` — `0.5336`; `r16_rerun_flat2.py … 4000` (their `flat_run` on the grid
  of step `0.01`) — minimum `0.5336` at `φ = 0.63`.  `r16lib.py` imports `math` and `numpy` only.
* **Two files of the workstream were moved out of the tree** before the commit, because they are logs
  of runs that did not reach their last line (rule of the division: such a log is not committed):
  `logs/flat_own_1000_050.log` (the failed assertion of §9, item 3) and
  `logs/flat_own_light_16000_no9024_rstar.log` (the run of §9, item 6, stopped by the workstream);
  likewise `logs/rerun_cert3_time.txt`, the one-line output of the failed command of §9, item 1.
  None of the three is cited in the report.
* **Not checked by the coordinator:** the per-rung comparison (§4.3); the sizes above `4 000` beyond
  what the stored logs show; Steps 2–9 of the proof of Theorem 11.56; the algebra of the contract
  clauses C5–C6 beyond reading.
* **One remark.**  m2's algebra is immediate from the accuracy formula; m1 I agree with as a statement
  about what the worded rule proves — the theory division's algorithm of Theorem 11.52 already tests
  every query, so this is a sentence to align, not a gap in a proof.
