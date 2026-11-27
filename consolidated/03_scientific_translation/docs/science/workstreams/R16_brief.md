# Workstream R16 (launched 2026-11-26, after the theory division's twentieth checkpoint) — review of the certified third level the theory division offered for review

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date).  The object is the theory branch at commit `9befefd`; a read-only export of that
tree is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_9befefd/`
(called `<EXP>`; our own tree is built on the much older `5ed4072` — do not confuse
them).  If the agent of this workstream is gone, its notes are in
`experiments/science/ws_R16/` and its draft in `R16_REPORT.md`.*

**What was asked.**  `<EXP>/docs/collaboration/responses/theory/THY-RES-0013.md` — read it
in full first.  It is addressed to the engineering division; its §6 says to us:

> §4 above is new material of the kind you have reviewed for us before; if you have a
> referee to spare for it, the claim to attack is the monotonicity argument and the
> admissibility of a two-level run as an inner procedure of Theorem 11.56 (the accuracy
> and failure probability it must be designed for), not the arithmetic.

We accepted (SCI-RES-0018 §3) and promised, beyond those two things, one replication of
the certified column at one size with code that does not use the theory division's
referee's evaluator.

Where things are in `<EXP>`: `docs/THEORY_REPORT.md` — Theorem 11.56 (find it with
`grep -n "Theorem 11.56 (one more level"`), its proof and the remark after it, §11.19
remarks (1) and (1b) (`grep -n "(1b)"`), Theorem 11.52 and Proposition K0 as far as
11.56 uses them; `experiments/coordinator_checks/three_levels_certified/` (`README.md`,
`cert3.py` with `make_inner` and `bounded_candidates`, `summary.py`, `terms.py`, the
`out_*.txt`); the referee's routines it calls, `experiments/reviews/R8/r8_flat.py`
(`flat_run`, `k0_plan_flat`), `r8_flat3.py`.  In *our* tree: workstream R6 reviewed
§§11.18–11.19 earlier (`docs/science/workstreams/R6_REPORT.md`,
`experiments/science/ws_R6/` — its own implementation of the cost count of the nested
algorithm, `separation.py` and others; SCI-REV-0007) and workstream R13 the amendments
(`R13_REPORT.md` §3).  Use them: they are our independent code and our earlier reading
of the same theorem.

## Item 1 (the most important) — admissibility

Theorem 11.56 states what an inner procedure must deliver for the outer level's
guarantee to hold.  Write down, from the theorem's statement and proof and not from the
message, the exact contract of an inner procedure serving rung `l`: on which object it
is called (the fibre: its dimension, its trivial bracket), what it must return, with
which accuracy, with which failure probability, how often it may be called, what the
outer level does when a call would exceed its cost bound (the abort with the trivial
bracket), and whether the failure probabilities of the inner calls are union-bounded
over the calls, over the rungs, or absorbed otherwise.  Then check that a **two-level
run** (Theorem 11.56 itself, or 11.52, applied on the fibre) meets that contract as
`cert3.py` designs it (`make_inner`, `bounded_candidates`): (i) the accuracy it is
designed for against the accuracy `x_l` the rung needs — "an accuracy at most `x_l`":
is the certified accuracy of the two-level run (which is *larger* than its nominal one:
the report quotes "certified accuracy `0.8715`" for a nominal design) the right
quantity, and is the tolerance `b` handled (the message's `b = x − ln(e^c(1+c)/(1−c) +
2c)`: re-derive it); (ii) the failure probability `δ′` it is designed for, and how many
times it is called — is the union bound over all calls of all rungs inside the outer
level's budget, or does the design need `δ′` divided by the number of calls; (iii) the
*cost bound* `C_l` of the two-level run: Theorem 11.56's `C_max` holds "in every run on
every instance" because the algorithm aborts — does an abort inside an inner two-level
run return something the outer level can use (a valid bracket, the trivial one) without
breaking the outer accuracy claim, and is the probability of such aborts accounted for;
(iv) the fibre is not the cube with zero known part in general — is the two-level run
proved for the objects it is called on?  State each as: holds / holds with a condition
to add / gap / false, with the line of the proof that decides it.

## Item 2 — the monotonicity argument

"`C_max` of the outer level is nondecreasing in every `C_l`", "if every rung is served
by the candidate with the smallest certified cost the certified bound of three levels
is at most that of two levels, for every `n`, and more candidates can only lower it".
Re-derive from the display `C_max = 1 + 2M̄ + Σ_l min{2M̄, (J+1)·cnt(x_{l−1})}·C_l`: do
`M̄`, `J`, `cnt`, the ladder and the certified accuracy of the *outer* level depend on
the inner procedures in any way (for instance through the tolerance or the failure
budget handed down, or through the accuracy the inner procedure actually certifies)?
If the outer design must change when the server of a rung changes, monotonicity in
`C_l` alone is not the whole argument — say exactly what is held fixed.  "Which
candidate serves which rung is decided before any evaluation, from the design alone":
check in `cert3.py`.

## Item 3 — one replication with code that is not the referee's

Compute the certified three-level bound at **one size** (`n = 4 000`, `u = 1`, the outer
design of the README; if time allows also `n = 16 000`) with code written from Theorem
11.56's statement — our workstream R6's implementation may be used and extended; the
theory division's `r8_flat.py` and `cert3.py` may be *read* to resolve ambiguities of
the design (say which you resolved that way) but not imported.  Targets: the two-level
certified bound (`0.7262` at the best outer fraction `0.5`), the column "servers by
certified cost, the referee's two middle designs" (`0.6331` at `0.4`), and if feasible
"more middle designs" (`0.6106` at `0.375`); and for one outer fraction the per-rung
choice (which rungs are served by a two-level run) against `out_terms_4000.txt`.
Stopping condition: agreement to four digits, or the first number that differs with
the rung at which the two implementations differ.  Then re-run their `summary.py` (it
reads the stored outputs) and, if it takes under twenty minutes, one line of
`cert3.py` — see the README for commands; run their code from the export with
`python3 -I -B`, writing nothing into `<EXP>`.

## Item 4 — what the claim is and is not

The message compares the certified three-level bound with "the worst instance found for
two levels" (the engineering division's searches).  Say precisely what is proved by
the comparison (an upper bound for one algorithm against a lower bound on the worst
case of another: is "three levels beat two levels from `n = 4 000` on" a theorem about
the two algorithms *as designed*, given the searches are searches?) and what the
limits `τ₂/a = 0.500`, `τ₃/a = 0.361` have to do with it.  One paragraph.

## Rules

Write only in `experiments/science/ws_R16/` and `docs/science/workstreams/R16_REPORT.md`.
No state-changing git; no `lake build`; no subagents.  Keep four kinds of checking apart
and say which you did for each statement: **review** (re-derived), **replication** (own
code written from the statements), **re-run** (their code), **read only**.  Never
fabricate; reading levels for anything cited.  A finding is *critical*, *major* or
*minor*; give a replacement text for each.  Report what you did not check, and your
own errors.  Machine: 4 cores and 14 GB **shared with other jobs** — `OMP_NUM_THREADS=1`,
at most two processes, no process above 2 GB (print the peak RSS in the last line of
every script), no run longer than 20 minutes.  Keep `NOTES.md` from the first minute.
A log is cited only if its run reached its last line.  A time written into a file is
read from the clock at that moment.  **If a tool declines an action, do not work around
it: keep everything in `NOTES.md` and return the findings as text in your hand-back.
Do not delete files with wildcards or `rm -r`; use fresh directory names.**

## The report

(0) Verdict table.  (1) Findings by severity with replacement texts.  (2) The contract
of an inner procedure, written out, and the two-level run against it.  (3) The
monotonicity argument: what is held fixed.  (4) The replication: numbers against
theirs.  (5) What the comparison proves.  (6) Requests to the theory division that can
be sent as they stand.  (7) How to re-run.  (8) Not checked.  (9) Own errors.
