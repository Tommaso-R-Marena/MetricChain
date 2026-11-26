# Workstream R18 (launched 2026-11-26) — referee of two arguments of the engineering division: ENG-RES-0014 §1 (the exact classification rule of the mean-run evaluator) and §4 (a bound for instances that are not products)

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date).  The object is the
engineering branch at commit `1cc4e1c` (ENG-RES-0014 is unchanged there since `ce71724`); a read-only export is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro_1cc4e1c/`
(called `<ENG>`; it has `docs/`, `src/metricchain_eng/`, `experiments/eng/`, `tests/eng/`).  If the agent of this
workstream is gone, its notes are in `experiments/science/ws_R18/` and its draft in `R18_REPORT.md`.*

## What was asked, and by whom

In SCI-RES-0015 we offered to referee ENG-RES-0014 §1 and §4; the engineering division accepted in ENG-MSG-0006 §4:
"Yes, please referee ENG-RES-0014 §1 and §4 line by line — two arguments of ours that nobody else has checked (the
theory division re-derived §4; §1 only by reading)."  Read first:
`<ENG>/docs/collaboration/responses/engineering/ENG-RES-0014.md` (418 lines; §0, §1, §4, the limitations), then what
it builds on: ENG-RES-0008 (the mean-run evaluator and its search family: `ls <ENG>/docs/collaboration/responses/engineering/`),
ENG-MSG-0003 §5 (the tie rule), and the theory division's Theorem 11.56 / Algorithm 2L⁺ as our own workstreams read
it: `docs/science/workstreams/R6_REPORT.md` and `R16_REPORT.md` (the contract C1–C8 of an inner procedure), with our
literal implementation `experiments/science/ws_R6/r6lib.py` (exact constants, the loop as written) and
`experiments/science/ws_R16/r16lib.py`.  Their code: `<ENG>/src/metricchain_eng/twolevel/` (`meanrun.py` — the
Python reference of the evaluator; `alg2l.py`, `simulate.py` — literal runs; `meanrun_kernel.c` — do not build it),
`<ENG>/experiments/eng/twolevel/recheck_classification.py`, `nonproduct_bound.py`, `<ENG>/tests/eng/test_twolevel.py`.

## Item 1 (§1) — the classification rule

The claim.  After rung `l` a point holds the bracket `[W e^{−A_l}, W e^{B_l}]`, `A₀ = t₀`, `B₀ = x₀ − t₀`,
`A_l = min(A_{l−1}, α_l)`, `B_l = min(B_{l−1}, β_l)` with `α_l + β_l ≤ x_l`; "a point leaves the loop HIGH at the first
rung with `L > s e^{−b}` while `U > s`, and LOW at the first rung with `U ≤ s`.  Since `B_l` decreases in `l`, it is HIGH
iff `W > s·e^{−c}`, `c = max_{0 ≤ l ≤ L} min(b − A_l, B_l)`."

Re-derive it line by line from the algorithm as the theory report and our R6 state it (which test comes first at a
rung; strict and non-strict inequalities; what happens at the last rung; ties at `W = s e^{−c}`, at `U = s`, at
`L = s e^{−b}`; a point never classified).  State each step as: holds / holds with a condition to add / gap / false,
with the line that decides it.  Then: (i) are "bottom gives `c = b`, top gives `c = 0` as long as `t₀ ≥ b` and
`x₀ − t₀ ≥ b`" and the range `t₀ ∈ [n_i(u − Λ₁), n_i(2u − Λ₁)]` of a `u`-Lipschitz fibre correct; (ii) is the refinement
window "`W e^{b−A_l} ≤ s_j < W e^{B_l}`" the set of points that call rung `l + 1`, exactly; (iii) does the rule hold
when the inner positions `(α_l, β_l)` differ from rung to rung in any admissible way, and where exactly does it
need them to be the same for all points (their own limitation: "inner behaviours that differ from point to
point").  **Test it with code that is not theirs:** a literal loop (our `r6lib.py` or twenty lines of your own) over
random ladders, positions, thresholds and values, including the corners and ties, against the closed rule; and a
control that must fail (the rule with `min` and `max` exchanged, or the old conventions outside their range —
their own example says the cost ratio reaches `e^{4.2}`).

## Item 2 (§4) — instances that are not products

The claim.  For any instance with the same law of fibre averages whose fibres sit at places `t₀(a) ∈ [lo, hi]`, with
either uniform inner behaviour: the classification shift `c` is the same, so the sample sizes are those of the
product instance; the refinement window of an atom at rung `l → l+1` is contained in
`W e^{b − min(hi, α_l)} ≤ s_j < W e^{min(x₀ − lo, β_l)}`; hence the mean run with `A₀ = hi`, `B₀ = x₀ − lo` "counts at least as
many calls at every rung as any such instance: an upper bound on the evaluations of every instance with that law,
product or not", for `[lo, hi] = [n_i(u − Λ₁), n_i(2u − Λ₁)]`.

Re-derive.  The points to press: (a) "its classification shift `c` is the same" — for *either uniform inner
behaviour*, with places that differ between fibres: is `c` really independent of `t₀(a)` (by Item 1 it depends on
`A₀ = t₀`: in which range of `t₀` is it constant, and is the feasible range inside it for every design used —
their §1 says so; check the inequality, not the sentence); (b) the union of windows: is the window monotone in
`A_l` and `B_l` in the direction used, at every rung, also after the minima with `α_l`, `β_l`; (c) "counts at least
as many calls at every rung" — the mean run is an expectation over samples: is the comparison pointwise in the
sample, or only in the mean, and does the cost (which also has the outer queries and the cap) inherit it;
(d) what an instance "with the same law of fibre averages" may still vary — the joint law of place and average —
and whether the bound covers all of it; (e) the range `[lo, hi]` for a `u`-Lipschitz fibre: re-derive.
**Test with your own code:** small exact or simulated instances whose fibres sit at different places (two or
three places, correlated with the fibre average in the worst way you can construct), the literal algorithm's
calls per rung against the mean run at `A₀ = hi`, `B₀ = x₀ − lo`; a control that must fail (the bound with `lo` and
`hi` exchanged).  Then re-run their two checks from a scratch copy (`recheck_classification.py`,
`nonproduct_bound.py`: two minutes each by their note; Python reference only; `python3 -I -B`) and compare with the
tables `recheck_classification`, `nonproduct` of the message.  **Do not run anything on Modal** (the two jobs
`anyplacement`, `converge2` are theirs; this division has no Modal access and wants none); the second table of §4 is
then "read only".

## Item 3 — what the two sections do and do not show (one paragraph)

Their reading: "leaving the product family does not change the picture of ENG-RES-0008".  Say what a reader may
conclude and what not (they name two limits themselves: inner behaviours that differ from point to point; outer
level sets that are not balls).  Under the research owner's directive of 2026-11-26 on generality
(`docs/science/OWNER_DIRECTIVES.md`) classify each assumption of the two arguments — essential / needed by the
proof only / convenience / replaceable by a quantitative condition / changes the complexity when removed / makes
the claim false when removed — with the evidence you have for each; "not established" is an answer.

## Rules

Write only in `experiments/science/ws_R18/` and `docs/science/workstreams/R18_REPORT.md`.  No state-changing git;
nothing on Modal; no network; no subagents; `<ENG>` stays untouched (copy what you run into
`ws_R18/rerun_copy/`, which will not be committed).  Keep four kinds of checking apart and say which you did for
each statement: **review** (re-derived), **replication** (own code written from the statements), **re-run** (their
code), **read only**.  Never fabricate; reading levels for anything cited.  A finding is *critical*, *major* or
*minor*; give a replacement text for each.  Report what you did not check, and your own errors.  Machine: 4 cores
and 15 GB shared with other jobs — `OMP_NUM_THREADS=1`, at most two processes, no process above 2 GB (print the
peak RSS in the last line of every script), no run longer than 20 minutes — and before any run of more than five
minutes write into `NOTES.md` its cost per step, the number of steps and what its result will be compared with.
Keep `NOTES.md` from the first minute.  A log is cited only if its run reached its last line; logs of stopped or
failed runs go into a subdirectory `not_cited/` and are named in the report; use fresh names instead of
overwriting a log.  A time written into a file is read from the clock at that moment.  Before a cause is written
down, the size of every candidate cause is computed.  Every check is reported with the violations of its
control.  **If a tool declines an action, do not work around it: keep everything in `NOTES.md` and return the
findings as text in your hand-back.  Do not delete files with wildcards or `rm -r`.**  This is an internal review,
not external peer review; say so in the report.

## The report

(0) Verdict in ten lines: are the two arguments proved as stated; the findings by class.  (1) The statements as you
understand them, with the hypotheses the message leaves implicit.  (2) Findings — critical, major, minor — each
with the line that decides it and a replacement text.  (3) The replication, with what agreed and what did not.
(4) Re-runs.  (5) The assumption table of Item 3.  (6) Requests to the engineering division that can be sent as
they stand.  (7) What you did not check; your own errors; files.
