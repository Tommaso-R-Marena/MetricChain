# Workstream R26 (written 2026-11-26) — adversarial review of the theory division's §11.33: the nested algorithm on an arbitrary probability space (Theorems 11.118–11.120, Proposition 11.121; their workstream N), with the question that matters to us — is nesting valid on a known part that is a band model?

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date; there are six divisions
now).  The object belongs to the Theoretical Research Division, branch `claude/determined-ride-og1u7j`, read here at
its commit `4692f59`.  If the agent of this workstream is gone, its notes are in `experiments/science/ws_R26/` and
its draft in `docs/science/workstreams/R26_REPORT.md`.*

## Why

THY-MSG-0018 (their twenty-third checkpoint) announces, as item 3 of its §1 (abridged here; two parentheses left out): "the level theorem holds for an
integrand on any probability space with an upper and a lower tail function; for a dependent known part under a
certified *class-relative influence* between the blocks.  Obstructions: on Gauss space … nesting over a fixed
split of the coordinates gains nothing; with unbounded influence between the blocks the algorithm returns a
**false certificate** (an explicit 28-site instance; every run of two independent implementations); an exponential
moment of the envelope is necessary and sufficient for any certified upper bound."  Labels: "[P; simulated;
refereed internally: correct as stated; one proposition is a plan, one claim corrected]".  And to us (§2): "for a
band model that influence is computable from the transfer operator, and whether it is small on your instances
decides whether nesting is even valid there — with unbounded influence the certificate is false, which is the
reason to compute it before anything else."  They ask all divisions for corrections to §1.

This division's known parts are band models of rotamer chains (transfer-matrix models with interactions up to
sequence separation 4 to 7), with steric clashes of tens of `kT` between neighbouring side chains.  So their
dividing line runs through our instances.  The research owner's directives ask for adversarial verification of
other divisions' results, for the class of every assumption, and for general theorems with computationally empty
guarantees to be named as such.

## The object (read-only copies; use nothing else of their branch)

`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_4692f59/`:
`N_REPORT.md` (their workstream report, 1 124 lines: §2 the abstract level theorem N1, N1′, tail functions,
Theorem N3 (two blocks, product), **Theorem N4 (dependence under bounded influence, §2.7)**, Lemma N18; §5 the
obstructions — N9–N11 (Gauss space), **N12 (the false certificate, §5.2)**, N13; §6 their assumption table; §7
their numerical checks; §8 their own errors; §9 what is not proved), and `THEORY_REPORT.md` (13 001 lines — read only
§11.33, l. 12113 to about l. 12290: Theorems 11.118–11.120, Proposition 11.121, which are the report's versions of
N1, N3/N4, N9–N11, N12; and Theorem 11.56 where N1 refers to its proof).  Their scripts are not copied; write
your own.  Their internal review of this workstream is not given to you.

## Item 1 — Theorem N4 / 11.119 (b): dependence under bounded class-relative influence

(i) Re-derive it from the definitions (what is a bracket procedure, a tail function, Algorithm A — N_REPORT §2.1–2.3).
Is (F1′) — "the inner procedures must be valid under every conditional law" — satisfiable by the procedures of
their own theorems when the conditional laws are not products?  Is anything used about `ι` beyond the displayed
inequality (symmetry? a triangle inequality? finiteness everywhere)?
(ii) **Compute the influence for a band model, with code of your own.**  Take (a) a synthetic nearest-neighbour
chain of 8 to 10 sites with 3 to 6 states per site and random pair energies of a chosen scale `J` (in `kT`), and (b)
the same with a few forbidden-like pairs (energy `+10` to `+30 kT`: a steric clash).  Outer block = the first half,
inner block = the rest.  Compute, for single-site changes of the outer configuration and for arbitrary pairs:
the pointwise influence `max_b ln[μ(b | a)/μ(b | a′)]`; the class-relative influence for fibre weights that are
`u`-Lipschitz in the Hamming distance; and for a "box" class of fibre weights `l(b) ≤ w(b) ≤ u(b)` with a ratio
`u/l = e^{D}` (the class our sandwiches define).  How do they scale with `J`, with the clash energy, with the block
length, with the bandwidth?  Is the influence of a band model governed by the interaction across the cut only
(the boundary sites), as their sentence to us says — prove or refute, and give the formula.
(iii) With those numbers: for which `(J, clash, u)` is the slope `u + ι` of their theorem still a useful
hypothesis, and for which is the theorem true and computationally empty?  One paragraph that a reader of our
handoff can act on: "nesting on a rotamer band model is valid if …, and worth … ".

## Item 2 — Proposition N12 / 11.121: the false certificate

(i) Re-derive (a)–(c).  (ii) **Replicate (d) with an implementation of Algorithm A of your own**, written from
N_REPORT §2.2–2.3: the instance `m = 12`, `k = 16`, `u = 1`, `J = 4`, `τ = 10.5` (or a smaller one with the same
mechanism if the full one is above your limits — say which), run with the tail function of the assumed class:
does it return a bracket that excludes the true value, how often, and at which step is the false inference made?
Then with the tail function of the true class.  A control: the same algorithm on a product known part must be
valid in every run.  (iii) Their sentence "every certificate obtained by sampling stays true, the false step is
the tail bound": is that what your runs show?  (iv) "Not a counterexample: unbounded influence confined to
boundedly many outer sites (a hub): condition on them" — is the claimed repair complete?

## Item 3 — Theorem N1 / N1′ / 11.118: the abstract level theorem

(i) What exactly must a pair of tail functions satisfy, and where does the proof use it?  Try to break the
statement with an integrand whose tail functions are valid but whose distribution has an atom at its maximum, a
gap, or a heavy lower tail.  (ii) N1′ ("no cap on `V`"): which hypothesis replaces the cap, and is the cost bound
still finite — or is this a case of a general theorem with a computationally empty guarantee?  (iii) The class
of every assumption (essential / proof technique / convenience / replaceable by a weaker quantitative condition /
removal changes the complexity / removal makes it false), against their own table in §6: where do you disagree?

## Item 4 — Theorems N9–N11 / 11.120: Gauss space (only if time remains)

Given the Gaussian isoperimetric inequality, is "nesting over a fixed split of the coordinates gains nothing"
proved as stated, and what exactly does "gains nothing" quantify over (which algorithms, which instances)?  Is the
fixed split essential?

## Rules

Write only in `experiments/science/ws_R26/` and `docs/science/workstreams/R26_REPORT.md`.  No state-changing git;
no subagents; the network only to look up a cited theorem (generic queries; nothing of this project in a
query).  Keep four kinds of checking apart and say which you did for each statement: **review** (re-derived),
**replication** (own code written from the statements), **re-run** (their code — not available to you), **read
only**.  Never fabricate; a reading level for anything cited.  A finding is *critical*, *major* or *minor*; give a
replacement text for each.  Report what you did not check, and your own errors.  Machine: 4 cores and 15 GB
shared with other jobs — `OMP_NUM_THREADS=1`, at most two processes, no process above 2 GB, no run longer than
fifteen minutes; print the peak memory in the last line of every script; run Python with `-B`.  Keep `NOTES.md`
from the first minute.  A log is cited only if its run reached its last line; use fresh names instead of
overwriting a log.  A time written into a file is read from the clock at that moment.  Every check is reported
with the violations of its control, and a control must be able to fail.  A statement about a random algorithm is
reported with the number of runs and seeds.
**If a tool declines an action, do not work around it: keep everything in `NOTES.md` and return the findings as
text in your hand-back, with a line "Tool actions declined".  Do not delete files with wildcards or `rm -r`.**
This is an internal review by an AI agent, not external peer review; say so in the report.

## The report

(0) Verdict in ten lines: for each of Theorem N4, Proposition N12, Theorems N1/N1′ (and N9–N11 if reached):
*proved as stated* / *proved with gaps (closed here or open)* / *false as stated (counterexample)* — and the
paragraph of Item 1 (iii).  (1) The statements as you understand them, with the hypotheses the texts leave
implicit.  (2) Findings, each with the line that decides it and a replacement text.  (3) Your computations and
runs, with their controls.  (4) The assumption table of Item 3 (iii).  (5) What you did not check; your own
errors; files.  Hand back a summary of at most fifty lines, with a line "Tool actions declined: none" (or what
was declined) and every web address opened, if any.
