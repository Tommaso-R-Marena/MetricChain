# Workstream R23 (launched 2026-11-26) — a sampled check of the theory division's assumption audit

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date).  The object is the
theory branch `claude/determined-ride-og1u7j` at commit `fc3f5d9`; a read-only export is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_fc3f5d9/`
(called `<THY>`: `docs/ASSUMPTION_AUDIT.md` — the synthesis, 364 lines; `docs/audit/AA1_REPORT.md` (1766 lines; theory
report §§2–6, 11.1–11.15) and `AA2_REPORT.md` (1702 lines; §§11.16–11.32); `docs/audit/APPLY_brief.md`;
`docs/THEORY_REPORT.md` (12 251 lines), `README.md`, `docs/DEAD_ENDS.md`, `docs/falsification_output.txt`,
`docs/workstreams/{N,R}_REPORT.md`, `experiments/audit/AA1`, `AA2` (14 scripts with stored outputs),
`experiments/falsify_conjectures.py`, `proofs/` (Lean sources, to read)).  If the agent of this workstream is gone,
its notes are in `experiments/science/ws_R23/` and its draft in `R23_REPORT.md`.*

## Why

The research owner's directive of 2026-11-26 asks every division for an assumption audit of its major theorems
in six classes — essential / needed only by the present proof / convenience / replaceable by a weaker
quantitative condition / removal changes the complexity / removal makes the result false — and asks this
division to "critically assess the assumptions, mathematical limitations, and potential relevance of
theoretical results, identifying gaps that require further mathematical investigation".  The theory division's
audit classifies 499 assumptions of 156 statements (tags `{E} {P} {C} {Q} {X} {F} {?}`).  We promised a review of
it (`docs/collaboration/responses/science/SCI-RES-0023.md`).  A full re-audit is neither possible nor wanted:
**this is a sampled check, and its main question is whether a tag can be trusted.**  The directive also says:
"Do not assume that these generalizations are necessarily possible" — so a tag `{P}` ("the statement survives,
only the proof needs the assumption") is a claim that needs evidence, as much as a tag `{F}` needs a
counterexample.

## Item 1 — the tags, by sample

Choose the sample by a rule you fix and record *before* reading the entries (for instance every `k`-th tagged
assumption of each kind in each report, from a starting index drawn with a seeded generator), so that the sample
is not chosen by what looks easy or wrong:

* **twelve `{P}`** (six per report): for each, what supports "the statement holds without it"?  Classify the
  support as: a proof by another route (given or cited) / a numerical or exhaustive check / an argument in
  words / nothing.  Where it is words or nothing, try for a bounded time (at most twenty minutes each) to
  decide it — a proof sketch you can check, or a counterexample on a small instance with your own code.  Say
  for each whether the tag should stand, become `{?}`, or become `{F}`.
* **ten `{F}`** (five per report): is the named object a counterexample to *the statement with the assumption
  removed* (not to a neighbouring statement)?  Re-run the audit's script where there is one (from a scratch
  copy, `python3 -I -B`) and compare with the stored output; for two of the ten, rebuild the counterexample
  with your own code.
* **six `{Q}`**: is the weaker quantitative condition stated precisely, and is its sufficiency proved, checked,
  or asserted?
* **four `{?}`**: is it really unknown — or is it decided somewhere in the theory report, in `DEAD_ENDS.md`, or in
  one of our reviews (`docs/collaboration/messages/science/SCI-REV-*.md` in the repository you work in)?

Report a table with one row per sampled assumption (report, entry, line, the assumption, their tag, the
support found, your verdict), and the rates: how many of each kind stand.

## Item 2 — the new counterexamples and facts of the audit (synthesis §6)

Check three, with your own code or argument, before opening the audit's scripts: (a) "every site non-sharp
and yet `n + 1` evaluations suffice" (two-state sites with margin below `1/n`; AA1 S3) — the proof and an
exhaustive check for small `n`; (b) the claim that their Theorem 11.33(a) is false without an additive known
part — the code-landscape instance (extended Golay code, `n = 24`, `w = 4`: "every algorithm with `ε < 10⁻³`
makes `(1 − 2δ)·4096` evaluations") — is the lower-bound argument sound, is the instance inside the class of
the theorem as the theory report states it (read the statement at `<THY>/docs/THEORY_REPORT.md` l.3877–3895), and
does it contradict (a) of the theorem or only a reading of it; (c) "with a `p`-biased measure Hamming balls are
not extremal for the tail functional (ratio up to 2.08 on the 4-cube, all 65 534 subsets)" — exhaustively.
The "positive facts" of §6 are flagged there as unrefereed; pick the one that looks most consequential and say
whether its argument holds.

## Item 3 — the synthesis against its sources, and against the tree

(a) Is the synthesis faithful to the two reports: the counts of §1 (recount the tags), the levels of §2 (does
each "lost" on the way down have its evidence where cited), the table of §5 (vacuous guarantees: is each row's
number in the cited place), §7 (the counts of overstatements)?  (b) **The state of the tree.**  The synthesis
says the corrections "are recorded item by item in `docs/audit/APPLIED_CORRECTIONS.md`" and that Theorem 11.33(a)
is "corrected".  The coordinator found that at `fc3f5d9` that file does not exist and that `docs/THEORY_REPORT.md`
and `README.md` are unchanged since the commit the audits read.  Confirm, and for the five overstatements the
synthesis calls the worst (§7) and the theorem, quote the sentence as it stands in `<THY>` now.  (c) Coverage:
which numbered statements of the theory report are in neither audit (sections 7–10; anything after §11.32;
the appendix) — a list, not a judgement.

## Item 4 — what our own reviews say about the same statements

The audits cite this division's reviews (SCI-REV-0001 … -0017, SCI-RES-…).  For five citations chosen by the
same kind of rule, open our message (in `docs/collaboration/messages/science/` or `responses/science/` of the
repository you work in) and say whether the audit reports our finding correctly.  Then the reverse, for the
sections we reviewed most closely (§11.19 with Theorem 11.58a, §11.26, §11.30, §11.32): is there a finding of
ours about an assumption or a finite-size limit that the audit does not have?  (One the coordinator knows of:
our SCI-REV-0017 states that the design of Theorem 11.58a costs more than the non-adaptive bound up to
`n = 2.04·10⁴` at `u = 1`; the synthesis §5 says "explicit but large constants" without the number.)

## Item 5 — gaps that need mathematics

From what you read: the three assumptions whose status matters most for anything outside the models and is
not settled by the audit (their own §8 ranks ten; you may agree or not), each with the smallest concrete
question that would settle it — a statement to prove or an instance to compute — in a form that can be sent
to the theory division as it stands.

## Rules

Write only in `experiments/science/ws_R23/` and `docs/science/workstreams/R23_REPORT.md`.  No state-changing git;
no subagents; no `lake`; `<THY>` stays untouched (copy what you run into `ws_R23/rerun_copy/`, which will not be
committed).  No web search is needed; if you use it, generic queries for published mathematics only, nothing
of this project in a query, cite only what you opened.  Keep four kinds of checking apart: **review**,
**replication** (own code), **re-run** (their code), **read only**.  A finding is *critical*, *major* or *minor*;
give a replacement text or a replacement tag for each.  Report what you did not check, and your own errors.
Machine: 4 cores and 15 GB shared with six other jobs — `OMP_NUM_THREADS=1`, at most two processes, no process
above 2 GB, no run longer than 20 minutes; before any run of more than five minutes write its cost into
`NOTES.md`.  Keep `NOTES.md` from the first minute.  A log is cited only if its run reached its last line; logs of
stopped or failed runs go into `not_cited/`; fresh names instead of overwriting.  A time written into a file is
read from the clock.  Every check is reported with the violations of its control.  **If a tool declines an
action, do not work around it: keep everything in `NOTES.md` and return the findings as text in your hand-back.
Do not delete files with wildcards or `rm -r`.**  This is an internal review, not external peer review; say so
in the report.

## The report

(0) Verdict in ten lines: can the tags be trusted, by kind; the findings by class.  (1) The sampling rule and
the sample.  (2) The table of sampled assumptions with verdicts, and the rates.  (3) The three counterexamples
of Item 2.  (4) The synthesis against its sources and against the tree.  (5) Our reviews against the audit.
(6) Three gaps, each with a question that can be sent as it stands.  (7) What you did not check; your own
errors; files.
