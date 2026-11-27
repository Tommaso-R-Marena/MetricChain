# Workstream R17 (launched 2026-11-26, after the theory division's twenty-second checkpoint) — referee of their Theorem 11.58a: adaptive cost `exp(n·h + O(√(n ln n)))` without a hint

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date).  The object is the theory branch at commit `dd067f1`; a read-only export of the
parts you need is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_dd067f1/`
(called `<EXP>`; it has `docs/`, `experiments/workstreams/Q/`, `experiments/reviews/R12/`,
`experiments/reviews/R8/`, `experiments/coordinator_checks/` — our own tree is built on
the much older `5ed4072`, do not confuse them).  If the agent of this workstream is gone,
its notes are in `experiments/science/ws_R17/` and its draft in `R17_REPORT.md`.*

## What was asked

`<EXP>/docs/collaboration/responses/theory/THY-RES-0015.md`, §7 — read it first.  The
theory division offers a new theorem "for review to whoever has a referee to spare":

> **Theorem 11.58a.**  For every `u > 0`, `ε > 0`, `0 < δ < 1`: the least number `N(n; ε, δ)` of
> evaluations with which an adaptive randomised algorithm without a hint is
> `(ε/2, δ)`-correct on `L_u(Q_n)` (counted in every run, at every instance) satisfies
> `n·h − O(1) ≤ ln N(n; ε, δ) ≤ n·h + C·√(n ln n)` …
> **What to attack, if you take it:** Proposition Q6 (the slope step: two pages of
> bookkeeping on Theorem 11.56 at `θ = e^{Θ(n)}` with a ladder of `Θ(n)` rungs and failure
> probabilities `e^{−Θ(n)}` — a regime no simulation covers) and the invariant
> "`ln(1/δ) + dimension·ln 2` grows by `O(ln n)` per level".

Where things are in `<EXP>`: `docs/workstreams/Q_REPORT.md` (922 lines: the proofs —
§2 one level at finite `n` with Lemmas Q3, Q4 and Corollary Q4a, §3 the base family
(Proposition Q5), §4.1 the slope step (Proposition Q6), §4.2 the drop (Proposition Q7),
§5 the epoch schedule (Theorem Q8, Proposition Q9a, §5.3 "why the error is uniform in
the number of levels"), §6 the optimisation (Theorem Q9), §7 numerical checks, §8 "what
is not proved; the weakest link"); `docs/reviews/R12_referee_report.md` (their own
referee: read it early — do not repeat what it did; attack what it did not or could
not); `docs/THEORY_REPORT.md` §11.19 (`grep -n "Theorem 11.58a"`, `grep -n "Theorem 11.56
(one more level"`, Lemma 11.55, Proposition 11.57, the remark after Theorem 11.53 with the
epoch sequences); `experiments/workstreams/Q/` (`qlib.py`, `qscheme.py`, `q1`–`q4`, their
outputs); `experiments/reviews/R12/`.  In *our* tree, use: workstream R16's contract of
an inner procedure of Theorem 11.56 (`docs/science/workstreams/R16_REPORT.md` §1:
conditions C1–C8, Proposition R16.1, the abort rule finding m1, the tolerance finding
m2 — the theory division has since adopted them, THY-RES-0015 §1) and its replication
code (`experiments/science/ws_R16/`); workstream R6's own implementation of the cost
count of the nested algorithm (`experiments/science/ws_R6/`, `R6_REPORT.md`); workstream
R13's review of the rate (`R13_REPORT.md`; `RateFull.lean` is ours — the epoch sequences
`d_m`, `J_m`, `k_m` and the bound `B_m − h ≤ c₁/(k_m + c₂)` are machine-checked there).

## Item 1 (the most important) — the slope step, Proposition Q6 with Lemma Q4

Re-derive line by line.  (i) **Lemma Q4**: the closing radius at an extensive threshold
`θ = e^{x − O(1)}` is `ρ_h·n_o` and the outer sample then costs `e^{n_o h}` up to a factor
`n_o + 1`.  What exactly is assumed about `x` relative to `n_o` (the report: "`x ≫ ln n`",
"an outer block of only `≈ x/h` coordinates")?  Is the statement uniform in the range in
which the schedule uses it, including the smallest and the largest slope step of an
epoch?  (ii) **The use of Theorem 11.56** in that regime.  Write down what Theorem 11.56
requires of the outer level and of every inner procedure (take our R16 contract C1–C8
as the checklist and the theorem's present wording in `<EXP>` as the authority) and
check each requirement in the slope step: the accuracy handed down to each rung of a
ladder with `Θ(n)` rungs (the arithmetic ladder of step 1, capped — "loses at most 1
nat": re-derive), the tolerance (the supremum form `b`), the failure probability
`δ′ = δ/(4LM̄)` **per call** and the union bound over calls, rungs *and levels* when
`M̄ = e^{Θ(n)}`, the abort rule (before every query, the query of a new outer point
included) and what an aborted inner run returns.  (iii) **The loss**: "a slope step
loses `(a/h + 4)·ln n + O(1)` nats".  Where does each of `a/h` and `4` come from; is the
`O(1)` uniform in the level index, in `δ`, in the epoch?  State each step as: holds /
holds with a condition to add / gap / false, with the line that decides it.

## Item 2 — the invariant on failure probabilities and dimensions

"Along a chain of nested levels `Σ ln M̄ ≤ n ln 2 + k·O(ln n)`", so that the failure
probability handed down costs "at most `ln n + O(1)` nats per level, whatever the
depth".  Re-derive.  In which quantities does `ln(1/δ′)` enter the cost of a level
(the number of samples `K`, the ladder, the outer sample) — is there any place where
it multiplies an exponential in a way that is not absorbed (for instance a bounded
level, the drop, run at failure probability `e^{−Θ(n)}`: its `√`-loss
`u·√((n_o/2)·ln(2e^{u(m₀+2)}/θ))` and its sample count depend on `δ′` how)?  Check the
base family (Proposition Q5) at the failure probabilities it is actually called with.

## Item 3 — the drop, the schedule and the uniformity in the number of levels

Proposition Q7, Theorem Q8, Proposition Q9a and §5.3.  The claim: all `√`-losses
together are `C₁√n` with `C₁ = u·[√(ℓ⁰/2) + Σ_m √(φ_m ℓ_m/2)·B_{m+1}/a]` a convergent series
independent of the number of levels (`C₁ ≈ 5.5` at `u = 1`, `ε = 1`), because there is one
drop per epoch, `O(ln k)` epochs up to level `k`, and geometrically decreasing outer
fractions.  Re-derive the geometric decay from the epoch sequences (use the
machine-checked recursion, compute the sequences yourself) and the value of `C₁`;
check the three places §5.3 names (accuracies, failure probabilities, ladders) and
look for a fourth.  Then Theorem Q9: `n·c₁/k + k·ln n` at `k ≈ √(n/ln n)`, the constant
`C_*(u) = 2√((1 + r̄)c₁(a/h + 4))` (`4.65, 8.64, 13.5` at `u = ½, 1, 2`), and the side
condition `(k_M − 1)·O(ln n) ≤ n`.

## Item 4 — the lower bound and the statement

THY-RES-0015 §7 states `n·h − O(1) ≤ ln N` "for `δ < ½`: your machine-checked hinted
bound and three lines"; the report's page-one statement has `n·h − O(ln n)` "with the
lower bound of Theorem 11.25(a)".  Which is in the theory report's Theorem 11.58a,
which is proved, and what are the three lines?  Check the definition of `N(n; ε, δ)`
(`(ε/2, δ)`-correct; counted in every run at every instance) against what the upper
bound delivers (a bracket of ratio at most `e^ε` with probability at least `1 − δ`, a
cost bound in every run).

## Item 5 — one replication with code that is not theirs, and re-runs

(a) From the formulas of the report (not from `qlib.py`), compute the bound of Theorem
Q8 / formula (5.2) at `u = 1`, `ε = 1`, `δ = 0.05` for the best number of epochs at
`n = 6.4·10⁴, 10⁶, 10⁸, 10^{10}`; targets `0.71, 0.37, 0.273, 0.2637` in units of `n·a`
(`h = 0.2626·a`), with 13 and 43 levels at the first two sizes; and
`(bound − nh)/√(n ln n)` "between 2.4 and 3.8 for `1.6·10⁴ ≤ n ≤ 10^{12}`".  Say which
ambiguities you resolved by reading their code.  (b) If time allows: one entry of the
exact nested design of §7.3 (three nested levels at one size) with our R16/R6 cost
code extended, against `out_q3_scheme_exact.txt`.  (c) Re-run `q1`–`q4` from a scratch
copy of `<EXP>/experiments/workstreams/Q/` with `python3 -I -B` (each only if it takes
under twenty minutes; `<EXP>` itself stays untouched) and compare with the stored
outputs.

## Item 6 — what the theorem is and is not (one paragraph)

"It is a statement about the order of the error term; at every size where the design
can be evaluated exactly it is worse than the tuned designs of remark (1b)."  Say what
a reader may and may not conclude, and whether the report's §8 ("what is not proved")
is complete.

## Rules

Write only in `experiments/science/ws_R17/` and `docs/science/workstreams/R17_REPORT.md`.
No state-changing git; no `lake build`; no subagents.  Keep four kinds of checking apart
and say which you did for each statement: **review** (re-derived), **replication** (own
code written from the statements), **re-run** (their code), **read only**.  Never
fabricate; reading levels for anything cited.  A finding is *critical*, *major* or
*minor*; give a replacement text for each.  Report what you did not check, and your
own errors.  Machine: 4 cores and 14 GB **shared with other jobs (a Lean build is
running)** — `OMP_NUM_THREADS=1`, at most two processes, no process above 2 GB (print
the peak RSS in the last line of every script), no run longer than 20 minutes — and
before any run of more than five minutes write into `NOTES.md` its cost per step, the
number of steps and what its result will be compared with.  Keep `NOTES.md` from the
first minute.  A log is cited only if its run reached its last line; logs of stopped or
failed runs go into a subdirectory `not_cited/` and are named in the report.  A time
written into a file is read from the clock at that moment.  Before a cause is written
down, the size of every candidate cause is computed.  **If a tool declines an action,
do not work around it: keep everything in `NOTES.md` and return the findings as text in
your hand-back.  Do not delete files with wildcards or `rm -r`; use fresh names.**

## The report

(0) Verdict in ten lines: is Theorem 11.58a proved as stated; the findings by class.
(1) The statements as you understand them, with the hypotheses that the report leaves
implicit.  (2) Findings — critical, major, minor — each with the line that decides it
and a replacement text.  (3) The replication (item 5a, 5b), with what agreed and what
did not.  (4) Re-runs.  (5) Requests to the theory division that can be sent as they
stand.  (6) What you did not check; your own errors.
