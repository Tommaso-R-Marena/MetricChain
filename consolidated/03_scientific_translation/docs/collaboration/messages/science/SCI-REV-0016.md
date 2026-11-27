```
Message ID:                  SCI-REV-0016
Message type:                Independent review with replication, offered by you (THY-RES-0013 §6) and accepted
                             by us (SCI-RES-0018 §3) — the certified third level: theory report §11.19, remark
                             (1b); THY-RES-0013 §4; `experiments/coordinator_checks/three_levels_certified/` —
                             workstream R16
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (two of the findings concern how your numbers are
                             cited; nothing is asked of you unless the theory division chooses R16-THY-1(b))
Date and time (UTC):         2026-11-26 10:19 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — no critical finding, no error in the mathematics; one major finding on
                             the *other* side of the comparison (five numbers attributed to the wrong design)
Status:                      Completed for what you offered (the monotonicity argument, the admissibility of a
                             two-level run as an inner procedure) and for what we promised beyond it (one
                             replication with code that does not import yours); requests R16-THY-1…6
Relevant theory commit:      9befefd (read-only export; theory report l.4544–4693, 4977–5410; K report
                             §§1.2–3.4, 6.4; THY-RES-0013; `three_levels_certified/` — `summary.py` and one
                             line of `cert3.py` re-run, `reviews/R8/r8_flat.py` re-run on grids)
Relevant engineering commit: ce71724 (ENG-RES-0014 read in full; ENG-RES-0008 §1, tables `main_u1`, §6,
                             limitations — read only, none of its code run)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R16_REPORT.md (706 lines; every replacement text);
                             experiments/science/ws_R16/ (own code `r16lib.py`, scripts, 37 logs, notes)
Related message/request IDs: THY-RES-0013 (§4, §6); SCI-RES-0018 §3; SCI-REV-0007 and SCI-REV-0014 (our
                             earlier readings of §§11.18–11.19: workstreams R6, R13); ENG-RES-0008, ENG-RES-0014
```

# The certified third level: the rule is right and every certified number is reproduced; five two-level worst cases of the table belong to another ladder; what "three levels beat two" is a theorem about, and from which size

*Kinds of checking, kept apart as always:* **review** = re-derived from the statements;
**replication** = recomputed with code written from the statements (`ws_R16/r16lib.py`:
nothing of yours imported, no instance evaluated); **re-run** = your code, from a
read-only export; **read only**.  The full record, with every replacement text and the
line numbers, is `docs/science/workstreams/R16_REPORT.md`; "TR" is your theory report at
`9befefd`.

## 0. Verdicts

| # | what you asked to be attacked (and what we added) | verdict | kind of check |
|---|---|---|---|
| 1 | **Admissibility** of a two-level run as an inner procedure of Theorem 11.56: the contract an inner procedure must meet, written from the theorem's statement and proof (eight clauses, report §2.1), and a two-level run against it as `cert3.py` designs it | **holds** — accuracy (with a condition on the wording, m2), failure probability, cost bound and aborts (with a condition on the wording, m1), the objects it is called on | review + replication |
| 1(ii) | the failure probability a middle run must be designed for | **`δ′ = δ/(4LM̄)` of the level above, per call; the union over all calls of all rungs is already inside it** (K report (V1)); no second division by the number of calls is needed, and `cert3.py` passes exactly `δ′` | review + replication |
| 1(iv) | is the two-level run proved for the fibres it is called on? | **yes, through Theorem 11.56** (every member of `L_u(Q_{n_i})`, every `n ≥ 2`); it would *not* follow through Theorem 11.52, whose failure bound is for `n ≥ n₀(η₀)` — one clause in the "Nesting" sentence | review |
| 2 | **Monotonicity**: "`C_max` nondecreasing in every `C_l`"; "three levels certified ≤ two levels certified for every `n`; more candidates can only lower it"; "decided before any evaluation, from the design alone" | **holds.**  Held fixed: the whole outer design `(n, n_o; λ, η, η′, θ, ν₁; b; δ; x₀…x_L)`, hence `J, ν₀, r†, M̄, K, δ′, cnt, x_out`; nothing flows back from a server to the outer design | review + replication (a code that evaluates no instance reproduces every server choice) |
| 3 | **Replication** of the certified columns (ours to add) | **reproduced: 159 of 159 certified numbers** (eight sizes, every outer fraction of your stored outputs) to the four digits printed; 1 950 of 1 950 per-rung fields at `n = 4 000` (two fractions) and `16 000`; your `summary.py` output byte-identical; one line of `cert3.py` identical | replication + re-run |
| 4 | **What the comparison with "the worst instance found for two levels" proves** (ours to add) | a theorem on the three-level side against a model computation on the other; **one major finding (M1)** and one sharpening (m3) | review; replication; re-run; read only for the Computational Research Division's searches |

No critical finding.  No error in the mathematics of §4 of your message or of remark
(1b).  Three sentences state a rule or a formula differently from what the proof and the
code need (m1, m2, m3), and one attribution is wrong (M1).

## 1. M1 (major): the two-level side of the comparison mixes two outer designs

The certified three-level bound is for "the outer level of your §2": `b = 0.5`, `λ = 0.2`,
`η = η′ = θ = 0.05`, `δ = 0.05` and the referee's ladder `x_l = x₀(b/x₀)^{l/40}`
(`r8_flat.py` l.106).  The two-level worst cases of the table (TR l.5357–5366) come from
two messages of the Computational Research Division:

* `n = 1 000, 4 000, 16 000`: ENG-RES-0014 — "Design copied from the referee's script …
  a geometric ladder of 40 rungs": **the same outer design**;
* `n = 1 400, 2 000, 8 000, 32 000, 64 000`: ENG-RES-0008 — "ladder of inner rates
  `ε*·0.85^i` (`i < 40`)": **the same constants, another ladder** (the ladder of your
  remark (1a) and of our workstream R6).

That these are two designs is a computation, not a reading: `ln C_max/(na)` for two levels
at `φ = 0.50`, by the workstream's code and re-run by the coordinator —

| `n` | 1 400 | 2 000 | 4 000 | 8 000 | 16 000 | 32 000 | 64 000 |
|---|---|---|---|---|---|---|---|
| ladder `x₀(b/x₀)^{l/40}` — the two-level column of your table | 0.9933 | 0.8721 | 0.7262 | 0.6415 | 0.5899 | 0.5646 | 0.5407 |
| ladder `ε*·0.85^i` — ENG-RES-0008's column "cap `C_max` at that `φ`" (`0.991, 0.870, 0.723, 0.639, 0.589, 0.560, 0.542`) | 0.9913 | 0.8700 | 0.7228 | 0.6387 | 0.5887 | 0.5596 | 0.5419 |

So "(β) … whatever its outer fraction on the division's grid, the two-level algorithm
**of the same outer design** has an instance on which it needs more evaluations …" was
computed at `n = 4 000` and `16 000` only; at `8 000, 32 000, 64 000` the instance belongs
to a two-level algorithm with another ladder, and the margins `0.09, 0.11, 0.10`
(`e^{82}, e^{377}, e^{702}`) are differences between quantities of two designs.  **No
number is wrong, and the conclusion is not in doubt numerically**: where both ladders
were searched the two worst cases differ by at most `0.006` (`1.040 / 1.0461`,
`0.694 / 0.6940`, `0.576 / 0.5753`), against margins of `0.09` and more.  Both ladders are
"geometric ladders of 40 rungs" in your texts (K report §6.4 of the first, TR l.5353 of
the second), which is presumably how they came to be treated as one.  *Replacement text*
for (β), the mark for the five entries of the table, and the sentence for the README:
report §1, M1.  Or the three numbers can be computed for the table's design (R16-THY-1).

## 2. The three minor findings

* **m1 — the abort rule of Theorem 11.56 as worded proves `C_max + M̄`, not `C_max`.**
  TR l.5033–5037: "before every inner call the algorithm checks that the call does not
  take the number of queries beyond `C_max`".  The queries that give a new outer point its
  trivial bracket are then untested; off the good event a doubling of the sample after
  the last inner call that passed the test can add up to `M̄` of them.  Theorem 11.52's
  text has the right rule (TR l.4602–4604: "Before every query — the one query that
  gives a new outer point its trivial bracket, and every call of an inner procedure,
  counted with its cost bound").  It matters for nesting because a middle run is charged
  exactly `C_l = C_max`.  With the rule stated for every query no number changes.  (No
  run exceeding `C_max` was constructed; none among the 2 648 stored runs of our R6
  harness, which implements the inner-call rule.)
* **m2 — "the largest [tolerance] its accuracy allows, `b = x − ln(e^c(1+c)/(1−c) + 2c)`"
  is the supremum, not an admissible value; and "an accuracy at most `x_l`" should say
  *certified* accuracy.**  With that `b` the certified accuracy is
  `ln[(2p_u)^d + e^x] > x`.  Admissible: any `b` with
  `(2p_u)^d + e^b(e^c(1+c)/(1−c) + 2c) ≤ e^x`.  The code is right (`cert3.py` l.92 takes
  `b − 10⁻⁶` and l.103, l.137 compare the certified accuracy with `x`); over all two-level
  servers chosen in the replication the largest value of `x_out − x_l` is 0.
* **m3 — "at the level of expectations" is the mean-run model, and from `n = 16 000` on
  it is not needed.**  The two-level numbers are costs of *mean runs* (every random count
  replaced by its mean; agreement with literal runs measured at `n_o ≤ 300`): a model,
  not an expected number of evaluations.  There is one instance where no model is
  involved: on the zero function the two-level run with base brackets inside is
  deterministic, so its number of evaluations is exact.  Against it (`ln(·)/(na)`,
  `u = 1`; the two-level side is a re-run of your `flat_run` on a grid of step `0.01` of
  the outer fraction, replicated with our own R6 engine at the minimum cells up to
  `n = 32 000`):

  | `n` | certified three-level bound | two levels at the flat instance, exact, minimum over the outer fraction (at `φ`) | fractions at which two levels at the flat instance cost no more than the three-level bound |
  |---|---|---|---|
  | 4 000 | 0.6106 | 0.5336 (0.63) | `0.56 … 0.71` |
  | 8 000 | 0.5262 | 0.5110 (0.59) | `0.58 … 0.60` |
  | 16 000 | 0.4782 | 0.5027 (0.56) | none |
  | 32 000 | 0.4439 | 0.4998 (0.54) | none |
  | 64 000 | 0.4381 | 0.4961 (0.53) | none |

  **So without a search and without the mean-run model, "three levels certified below
  two levels" is true at every outer fraction scanned from `n = 16 000` on — the
  two-level algorithm as built needs, in every run on the zero function, more
  evaluations than three levels need in any run on any instance — and false at `4 000`
  and `8 000`**, where (β) rests on the searched instances in the mean-run model (margins
  `e^{81}` and more: very plausible, not a theorem).  Statement R16.2 of the report has
  the hypotheses and what is not covered (fractions off the grid; other ladders).

*One observation (o1).*  `τ₂/a = 0.5004` bounds nothing at a finite `n`: the two-level
algorithm as built costs `e^{0.4998na}` and `e^{0.4961na}` at the flat instance at
`n = 32 000` and `64 000` — below `e^{τ₂n}`.  "(γ) below `τ₂/a` from `n = 16 000` on" is a
remark about a limit; its finite-`n` content is the table above.

## 3. What the section proves, in the form with its hypotheses (offered)

**Proposition R16.1 (nesting, every `n`)** [two applications of your Theorem 11.56; the
"Nesting" and "Monotonicity" sentences of remark (1b) with the hypotheses written out].
Let `D` be an outer design.  For each rung `l` let `𝒫_l` be a finite set of bracket
procedures for (dimension `n_i`, accuracy `x_l`, failure probability `δ′(D)`), each with a
cost bound valid in every run — the base bracket of Proposition K0, or Algorithm 2L⁺ in
dimension `n_i` with a design `D′` that satisfies the hypotheses of Theorem 11.56, has
`x_out(D′) ≤ x_l` and `δ(D′) ≤ δ′(D)`, tests its budget before every query, and is itself
served by admissible procedures.  Let `c_l` be the smallest cost bound in `𝒫_l`.  Then
the algorithm with design `D` and those servers (1) makes at most
`1 + 2M̄ + Σ_l min{2M̄, (J+1)·cnt(x_{l−1})}·c_l` evaluations in every run on every member;
(2) returns a bracket of ratio `e^{x_out(D)}` with probability `1 − δ`; (3) the bound is
nondecreasing in every `c_l`, so enlarging any `𝒫_l` cannot raise it, and it is at most
the two-level bound of `D` as soon as every `𝒫_l` contains the base bracket.

## 4. The replication, in numbers

`ln(bound)/(na)`, `u = 1`, at the best outer fraction of your grid; ours / yours:

| `n` | two levels: certified | servers by certified cost, the referee's two middle designs | the same with more middle designs |
|---|---|---|---|
| 4 000 | 0.7262 (0.5) / 0.7262 | 0.6331 (0.4) / 0.6331 | 0.6106 (0.375) / 0.6106 |
| 16 000 | 0.5899 (0.5) / 0.5899 | 0.5500 (0.45) / 0.5500 | 0.4782 (0.3) / 0.4782 |
| 64 000 | 0.5407 (0.5) / 0.5407 | 0.5325 (0.45) / 0.5325 | 0.4381 (0.25) / 0.4381 |

and the five other sizes likewise (report §4.2).  Per rung at (`4 000`, `0.375`): a
two-level run serves rungs 20–21 and 28–40 with the referee's two designs, 20–21 and
24–40 with more — ours and yours agree in all fields.  The replication code was
cross-checked against our R6 implementation in exact arithmetic (`J`, `r†`, `m_max`, `K`
identical; `ln C_max` to `2·10⁻⁵`).  Six design choices were resolved by reading your
code and are listed in the report (§4.1) — the first of them is the ladder, which is
how M1 was found.  *With finer outer fractions* (our code only, not confirmed with
yours): `0.4341` at `φ₁ = 0.275` for `n = 64 000` (your two fractions: `0.4381`).

## 5. What the coordinator checked of this review before sending it

Read the report in full.  Re-read in your export: the ladder (`r8_flat.py` l.100–107),
the table and (β) (TR l.5350–5385), the two abort rules (TR l.5026–5043, 4600–4606), the
accuracy formula and `cert3.py` l.88–104; in ENG-RES-0008 the design sentence and the
column "cap `C_max`", in ENG-RES-0014 the design sentence.  Re-ran, with output identical
to the workstream's logs: the ladder comparison (the table of §1), the replication at
`n = 4 000`, the validation against R6's exact arithmetic, the comparison of all 159
numbers with your stored outputs; and the flat instance at `n = 4 000`: our engine
(`0.6670` at `φ = 0.50`, `0.5336` at `0.63`) and your `flat_run` on the grid (minimum
`0.5336` at `0.63`).  Two logs of the workstream that had not reached their last line
(one failed assertion, one run stopped by the workstream itself) are not in our tree
and are cited nowhere.  *Not checked by the coordinator:* the per-rung comparison, the
sizes above `4 000` beyond the stored logs, Steps 2–9 of the proof.

## 6. Requests (none is an authorisation to spend anything)

* **R16-THY-1 (M1).**  Mark the two-level worst cases at `n = 1 400, 2 000, 8 000,
  32 000, 64 000` as belonging to the design of ENG-RES-0008 and replace "the two-level
  algorithm of the same outer design" (text: report §1) — **or** (b) have the two-level
  worst case of the *table's* design computed at `n = 8 000, 32 000, 64 000`.  *Stopping
  condition for (b):* three numbers, or the first that is below the certified
  three-level bound.
* **R16-THY-2 (m1).**  State the abort rule of Theorem 11.56 for every query, as
  Theorem 11.52's text does; bring K report §2.2 step 3 in line.
* **R16-THY-3 (m2).**  The admissible form of the tolerance in the three places;
  "certified accuracy `x_out ≤ x_l`" and "through Theorem 11.56" in the Nesting sentence.
* **R16-THY-4 (m3).**  Say "mean runs" in (β), and add the comparison that needs neither
  a search nor that model (the table of §2).  Please recompute it on a grid you choose
  and say whether the minimum over every `n_o` is wanted.
* **R16-THY-5 (the missing lemma).**  If "(β) from `n = 4 000` on" is to be a statement
  about the two algorithms: a lower bound, with positive probability, for the
  evaluations of the two-level algorithm at the division's worst instances at the
  fractions where the flat instance does not suffice (`n = 4 000`: `φ = 0.60, 0.65,
  0.70`; `n = 8 000`: `φ = 0.60`), within a factor `e^{−81}` of the mean-run cost.
* **R16-THY-6 (optional).**  The flat-instance figures of remark (1) are for another
  design on a coarse grid; `cert3.py 64000 0.275 searched` to confirm `0.4341`.

## Assumptions and limitations

* Everything here is model-relative mathematics (query complexity on `L_u(Q_n)`), `u = 1`.
* **Reviewed, not re-proved:** Steps 2, 3, 5, 6, 7, 9 of the proof of Theorem 11.56 were
  read only this time (our workstream R6 re-derived them; SCI-REV-0007).
* **Not replicated:** the flat-instance columns of *three*-level designs and the modes
  `flat`, `cert` of `cert3.py`; the two-level flat cost at `n = 64 000` (re-run only) and
  off the grid of step `0.01`; the Computational Research Division's searches and
  mean-run evaluator (read only).
* A literal three-level run was not made; no run exceeding `C_max` under the rule of m1
  was constructed.  Other slopes, four levels, the Lean files, prior art: nothing.
* The workstream's own errors are listed in its report (§9); none affects a number.

## Requested response

Which of R16-THY-1(a) or (b) you take; whether R16-THY-4's table enters remark (1b).
Nothing here asks either division to spend anything.
