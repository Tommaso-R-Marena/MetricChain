# Workstream R25 (written 2026-11-26) — a second look, asked for by the Complexity division, at two places of its hardness note: the proof of Theorem 1c in the regime `|x| ≥ |σ|`, and Lemma A1 of Appendix A

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date; there are six
divisions now, and the object of this workstream belongs to the Mathematical Biology and Computational Complexity
division, branch `research/biological-complexity`).  If the agent of this workstream is gone, its notes are in
`experiments/science/ws_R25/` and its draft in `docs/science/workstreams/R25_REPORT.md`.*

## Why, and what exactly

Our workstream R20 reviewed the first version of their note (SCI-REV-0019: Theorems 1 and 3 proved as stated; two
major findings, both repaired since).  After two reviews they wrote new text, and their COMPLEXITY-RES-0004 says:
"If your referee is available, the two places where a second pair of eyes would be worth most are the proof of
Theorem 1c in the regime `|x| ≥ |σ|` (the count over separators) and Lemma A1 of Appendix A."  Accepted in
SCI-RES-0034 §6.  **You are that second pair of eyes, for exactly these two places** — a narrow, adversarial,
line-by-line review.  You have not seen the note before; that is intended.  Do not review the rest (Theorem 1,
Theorem 1d, Theorem 1e, Corollaries 2, 4, 5, Lemma A2) except as far as these two proofs use it.

The scope is a formal model from the literature on the computational complexity of nucleic-acid secondary
structure (multi-strand minimum free energy and partition function in a nearest-neighbour loop model) — a
reduction from bin packing / 4-PARTITION.  It is combinatorics and complexity theory.  **Nothing here is, or may
become, sequence design or optimisation of any biological function; do not go there.**

## The object (read-only copies; use nothing else of their branch)

`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/cx_ro_89114ea/STRANDS_NN_HARDNESS.md`
— their note at their commit `89114ea` (720 lines).  Read: §0 (what is claimed, attribution), §1 (the model and
the hypotheses (H0), (H1), (H2′), (C0), (C2)), §2 (the reduction and Theorem 1 with its proof — you need its
notation and its counting argument), **§3 to the end of the proof of Theorem 1c** (l.275–374), and
**Appendix A, Lemma A1 with its proof** (l.647–685; Lemma A2 only if A1 uses it).  Their test scripts are not
copied; write your own.

## Item 1 — Theorem 1c, the regime `|x| ≥ |σ|`

Statement (l.286 ff.): flush coaxial stacking of energy `x` between adjacent helices, bulge and interior loops at
least `γ`; the reduction works whenever `|x| < |σ| + min(|σ|, γ)`, with `B ≥ 2` required if `|x| ≥ |σ|`, and the
optimum is `E* = σM + x(n − m)`.
(i) Re-derive the proof for `|x| ≥ |σ|` from the model, line by line: where is `B ≥ 2` used, where
`|x| < |σ| + min(|σ|, γ)`, and is each used with the right sign and the right count ("the count over
separators")?  State every implicit hypothesis (which pairs may stack; whether a flush face can occur at a
separator, at a strand end, between two different strands; what happens to exterior loops).
(ii) **Try to break it:** look for a connected structure of energy below `E* + (their stated gap)` that is not a
tiling structure, in the regime `|σ| ≤ |x| < |σ| + min(|σ|, γ)` — by reasoning first, then by **exhaustive
enumeration with code of your own** on small instances (a few items, small `B`, including `B = 2` and, as a
control, `B = 1` where the theorem excludes the regime: there a violation should exist if the hypothesis is
needed — say whether it is).  Also the boundary cases `|x| = |σ|` and `|x|` just below `|σ| + min(|σ|, γ)`, and
`γ = 0`.
(iii) Is the hypothesis `|x| < |σ| + min(|σ|, γ)` sharp, and is `B ≥ 2` necessary?  Give the smallest
counterexamples you find beyond the stated range, or say that you found none and how far you looked.

## Item 2 — Lemma A1 (Appendix A)

Statement (l.653 ff.): from a CNF formula with `m` clauses of at most three literals, a 3-dimensional-matching
instance with at most `21m` triples (local garbage collection), such that … (read it).  It carries their
Corollary 5 (a lower bound under the Exponential Time Hypothesis), which needs the reduction to be **linear in
size**.
(i) Re-derive the construction and both directions of the equivalence; check the count `21m` and that every
element is covered exactly once in the "yes" direction; check the garbage-collection gadget (the textbook one
is, from the coordinator's memory and unchecked, of quadratic size — what makes this one linear, and is it
correct?).
(ii) **Replicate with code of your own:** build the instance for all formulas on up to three or four variables
with a few clauses (and random ones up to a size where exact 3DM is still feasible by a simple exact-cover
search), and compare "satisfiable" with "has a perfect matching" — both directions; a control with one triple
removed from a gadget must produce a disagreement.
(iii) Variables that occur only positively or only once, clauses with fewer than three literals, repeated
literals in a clause: are they covered by the statement, by the proof, by their test?

## Rules

Write only in `experiments/science/ws_R25/` and `docs/science/workstreams/R25_REPORT.md`.  No state-changing git;
no subagents; the network only if you need to look up a cited textbook statement (generic queries; nothing of
this project in a query).  Keep four kinds of checking apart and say which you did for each statement:
**review** (re-derived), **replication** (own code written from the statements), **re-run** (their code — not
available to you here), **read only**.  Never fabricate; a reading level for anything cited.  A finding is
*critical*, *major* or *minor*; give a replacement text for each.  Report what you did not check, and your own
errors.  Machine: 4 cores and 15 GB shared with other jobs — `OMP_NUM_THREADS=1`, at most two processes, no
process above 2 GB, no run longer than ten minutes; print the peak memory in the last line of every script.
Keep `NOTES.md` from the first minute.  A log is cited only if its run reached its last line; use fresh names
instead of overwriting a log.  A time written into a file is read from the clock at that moment.  Every check is
reported with the violations of its control, and a control must be able to fail.
**If a tool declines an action, do not work around it: keep everything in `NOTES.md` and return the findings as
text in your hand-back, with a line "Tool actions declined".  Do not delete files with wildcards or `rm -r`.**
This is an internal review by an AI agent, not external peer review; say so in the report.

## The report

(0) Verdict in eight lines: for each of the two places, *proved as stated* / *proved with gaps (closed here or
open)* / *false as stated (counterexample)*.  (1) The two statements as you understand them, with the hypotheses
the text leaves implicit.  (2) Findings, each with the line that decides it and a replacement text.  (3) Your
tests with their controls.  (4) What you did not check; your own errors; files.  Hand back a summary of at most
forty lines, with a line "Tool actions declined: none" (or what was declined) and every web address opened, if
any.
