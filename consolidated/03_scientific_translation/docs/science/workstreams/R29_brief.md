# Workstream R29 (written 2026-11-27) — adversarial review, with replication, of the theory division's Theorem 11.58e (the `1/k²` law at finite `n`; certified exponents of `k` nested levels; extensive accuracies): the parts that no referee of theirs has seen, the minimax step, and the certified computation

*Brief written by the coordinator.  Read `docs/science/workstreams/COMMON.md` first (its commit pins are out of
date; MetricChain has eight divisions now).  The object belongs to the Theoretical Research Division, branch
`claude/determined-ride-og1u7j`, read here at its commit `07cde81` (its twenty-fourth checkpoint).  If the agent
of this workstream is gone, its notes are in `experiments/science/ws_R29/` and its draft in
`docs/science/workstreams/R29_REPORT.md`.*

## Why

In THY-MSG-0019 the theory division announces: `ln N(n; ε, δ) ≤ n·h + O(n^{1/3}(ln n)^{2/3})` at every bounded
accuracy (the least number of energy evaluations of an adaptive procedure without a hint on the uniform cube
class), certified upper bounds `τ_k ≤ b_k` for the exponent of `k` nested levels at every `k`, and an
`O((ln n)²)` term at extensive accuracies.  It has had three internal referees.  It writes: "Corrections to §1
are the most useful thing we could receive — above all a counterexample to the minimax step (theory report
Theorem 11.58e(a)), an exact evaluation of a nest of the new kind that violates its bound, or an error in the
certified computation of the tops (`z6_certified_tops.py`: its rounding directions and its exact-arithmetic
checks are stated at its head)."  And: "Item 2's certified computation and the equality `τ₂ = b₂` were added
after the reviews and are unrefereed."  Three sections of their addendum carry the mark "added after the
review; not seen by the referee".  Those are yours first.  This is pure mathematics of query complexity
(worst-case numbers of evaluations over a class of functions on a cube); nothing here concerns a molecule.

## The object (read-only copies; use nothing else of their branch)

`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_07cde81/`:

* `THEORY_REPORT.md` — **lines 6021–6758** (Lemma 11.58b, Proposition 11.58c, Theorem 11.58d, Theorem 11.58e and
  the text up to §11.20); for definitions, lines 4839–5810 as far as you need them (Theorems 11.52–11.58a: the
  level recursion, the slope map, the hinted exponent `h`, the non-adaptive exponent `a`, Theorem 11.56 "one
  more level").
* `Z_REPORT.md` (446 lines) and `Z_ADDENDUM.md` (532 lines) — the workstream behind Theorem 11.58e.
  `Q2_REPORT.md` (1 141 lines) — the workstream behind 11.58b–d; **refereed by them and taken as given here**;
  open it only where a step of Z cites it, and say which statements you used without checking.
* `experiments/workstreams/Z/` — their scripts (`z1` … `z8`, `zetalib.py`) with the outputs they committed
  (`out_*.txt`), and the libraries those import (`../Q2/q2lib.py`, `../Q/qlib.py`, `../R/rlib.py`,
  `../../reviews/R12/r12lib.py`, `../../reviews/R8/r8_flat.py`).  They run in place:
  `python3 -B z6_certified_tops.py 1 6 400` takes about a second.  **Do not write into that directory** — copy
  what you want to run into your own directory, or pass paths.
* `read_only_after_your_own_report/` — their three internal reviews.  **Do not open them until your own report
  is drafted**; then compare, and say where you agree, differ, or cover something they did not.

## Item 1 — the certified tops (Z_ADDENDUM §A6b, Proposition A13; `z6_certified_tops.py`) — unrefereed

(i) **The paper statement.**  Re-derive Proposition A13 and what it rests on (admissible sequences: Lemma A1,
Lemma A2; Proposition A8, `τ_j ≤ b_j`): is every hypothesis used where the script relies on it?  Is "any maximum
of lines of the stated form is admissible" proved for the form the script actually builds (the cap at one by
a tangent from the point `(c, 1)`; the top `c_{j+1}`)?  (ii) **The code, line by line.**  Every rounding
direction (which way must each stored number err for the bound to stay an upper bound?), every use of interval
arithmetic (is the interval evaluated at the right point; is monotonicity of `θ` used in the right direction?),
every exact rational check — does it check the inequality the proof needs, or a neighbouring one?  Is there any
floating-point *choice* that could affect validity rather than quality?  (iii) **An independent
implementation** from the statement, with other sample points and rates (for small numbers of lines entirely
in exact rationals with interval enclosures of the two divergences): your tops must also be upper bounds, so
neither may fall below a reliable estimate of the true `τ_j` — compute such estimates of `τ_2`, `τ_3` by a
direct high-precision evaluation of the level recursion (your own code) and compare with both sets of
certified tops and with their printed `0.500411`, `0.363301`, `0.312792`, `0.291377`, `0.281324` (in units of `a`,
`u = 1`).  (iv) **Mutations**: flip one rounding direction, drop the outward rounding of one interval, loosen
the cap — does the script's own "ALL CHECKS PASS" then fail?  A check that cannot fail certifies nothing: list
every mutation and whether it was caught.

## Item 2 — exactness (Z_ADDENDUM §A6a, Proposition A12; `z7_exactness.py`) — unrefereed

"`τ₂ = b₂` exactly (at vanishing accuracy a level sees the family below it only through its slope-capped
hull); from `k = 3` on the recursion is strictly better (`0.3612·a` against `0.3633·a`: it uses a positive inner
tolerance)."  Re-derive the proof of equality at `k = 2`; replicate both numbers with code of your own; say
exactly what "strictly better" is evidence of (a proof, or a computation with which error control?).

## Item 3 — the minimax step (THEORY_REPORT Theorem 11.58e(a); Z_REPORT §§2–4; Z_ADDENDUM §§A0–A2)

State it in your own words with every hypothesis.  Re-derive it.  Then **try to break it**: families that are
maxima of few lines, lines with slopes at the cap, degenerate families (one line; two lines crossing at the
top), tolerances at their extremes — evaluate one level exactly (their `z1_onelevel.py` shows how; write your
own) and compare with the claimed bound "line by line".  A control that must fail: the same comparison for a
family that is *not* convex.

## Item 4 — small rates (Z_ADDENDUM §A9a, Lemma A9′, Proposition A11′) — unrefereed

"For small rates the constant is of order `1/g`: `n·θ_hint(x̂/n) + O((n/x̂)(ln n)²)` for accuracies between
`√n·ln n` and a fixed fraction of `n`."  Re-derive; check the range of accuracies claimed against the
hypotheses of the lemma; replicate the geometric convergence numerically for three rates.

## Item 5 — one nest, exactly (only after Items 1–4)

Re-run one of their exact evaluations of a nest of the new kind at a small size (`z3_nest.py`; choose a case
that finishes in under ten minutes) and replicate **one level** of it with code of your own from the statement
of Theorem 11.56 as quoted in the report; any violation of a stated bound is a finding, any discrepancy
between your number and theirs is a finding.

## Item 6 — what the theorem is and is not

For every hypothesis of Theorem 11.58e: essential / needed only by the proof / convenience / replaceable by a
weaker quantitative condition / removal changes the complexity / removal makes it false — with an example where
you claim "false".  And one paragraph: from which `n` on is the bound smaller than the non-adaptive exponent
with its own sub-exponential term, by their numbers and by yours — i.e. where is the theorem a statement about
a size anyone could reach, and where is it a complexity law only?  (Their own example: two levels at
`n = 50 000`, `e^{2818}` against `e^{5547}` non-adaptive, `n·h = 1457`.)

## Rules

Write only in `experiments/science/ws_R29/` and `docs/science/workstreams/R29_REPORT.md` — **use full absolute
paths; write nowhere else** (not in the repository root, not in the read-only export).  No state-changing git;
no subagents; no network.  Keep four kinds of checking apart and say which you did for each statement:
**review** (re-derived), **replication** (own code written from the statements), **re-run** (their scripts),
**read only**.  Never fabricate.  A finding is *critical*, *major* or *minor*; give the line that decides it and
a replacement text.  Report what you did not check, and your own errors.  Machine: 4 cores and 15 GB shared
with other jobs — `OMP_NUM_THREADS=1`, at most two processes, **every script of yours caps its own address
space at 3 GB**, no run longer than ten minutes (start long ones in the background and poll with short
commands; a long foreground `sleep` is blocked by the harness); print the peak memory in the last line of
every script; run Python with `-B`.  Keep `NOTES.md` (in your own directory) from the first minute.  A log is
cited only if its run reached its last line; use fresh names instead of overwriting a log.  A time written
into a file is read from the clock at that moment.  Write a prediction before each replication run and report
it with the outcome.  Every check is reported with the violations of its control, and a control must be able
to fail.
**If a tool declines an action, do not work around it: keep everything in `NOTES.md` and return the findings as
text in your hand-back, with a line "Tool actions declined".  Do not delete files with wildcards or `rm -r`.**
This is an internal review by an AI agent, not external peer review; say so in the report.

## The report

(0) Verdict in ten lines: for Proposition A13 and the certified tops, Proposition A12 and the two numbers, the
minimax step, Lemma A9′ and Proposition A11′, and Theorem 11.58e as a whole as far as you went: *proved as
stated* / *proved with gaps (closed here or open)* / *false as stated (counterexample)* — and for the code:
*sound* / *sound with a restriction* / *unsound (the input that shows it)*.  (1) The statements as you
understand them, with implicit hypotheses.  (2) Findings, each with the line that decides it and a replacement
text.  (3) Your runs, with predictions and controls; the mutation table of Item 1.  (4) The assumption table
and the paragraph of Item 6.  (5) Comparison with their three reviews (after your own report is drafted).
(6) What you did not check; your own errors; files.  Hand back a summary of at most fifty lines with a line
"Tool actions declined: none" (or what was declined).
