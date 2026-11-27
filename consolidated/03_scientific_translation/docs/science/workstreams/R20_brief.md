# Workstream R20 (launched 2026-11-26) — adversarial reading of the Complexity division's first result: hardness of multi-stranded folding in the nearest-neighbour model (their Theorems 1 and 3)

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date).  The object is the
branch `research/biological-complexity` at commit `fc4b238` (the first commit of the Mathematical Biology and
Computational Complexity Division, one of three divisions the research owner added on 2026-11-26); a read-only
export of its files is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/cx_ro_fc4b238/`
(called `<CX>`: `docs/complexity/`, `docs/collaboration/messages/complexity/`, `experiments/complexity/`).  If the
agent of this workstream is gone, its notes are in `experiments/science/ws_R20/` and its draft in `R20_REPORT.md`.*

## What was asked, and by whom

`<CX>/docs/collaboration/messages/complexity/COMPLEXITY-MSG-0001.md` — read it first.  They ask "Science (or any
division): an adversarial reading of Theorem 1 and Theorem 3 of `docs/complexity/STRANDS_NN_HARDNESS.md` — in
particular hypothesis (H0) against the multi-strand model as you know it, and step (c) (every stack has one
template bond and one item bond)."  The claim: in the multi-stranded nearest-neighbour model (connected
unpseudoknotted secondary structures of a complex of strands, with an association term and a rotational-symmetry
term), for every loop-energy function with exterior loops 0 (H0), the GG/CC stack negative (H1) and bulge,
interior and multi loops non-negative (H2), the minimum-free-energy problem for unboundedly many strands is
NP-hard in the strong sense (a reduction from exact bin packing: a template `G^B(AG^B)^{m−1}` and homopolymer items
`C^{a_i}`); counting minimum-energy structures is #P-hard, and so is the partition function when the temperature
is part of the input.  This is combinatorics of an abstract model on synthetic strings; nothing in this
workstream designs, optimises or evaluates a sequence for any function, and none of that is to be done.

## Item 1 — the model and the hypotheses

`STRANDS_NN_HARDNESS.md` §1 (263 lines in all; read all of it).  (i) Is the model as they define it the
multi-stranded nearest-neighbour model of the literature — which structures are admissible (connected,
unpseudoknotted for some circular ordering of the strands), which loops exist, how an exterior loop, a nick and a
stack across a nick are treated, the association term, the symmetry term?  You may look the definitions up
(see "Rules: literature"); say for each point whether it is checked against a source you opened or from memory.
(ii) (H0)–(H2): which features of published parameter sets do they exclude (dangling ends, coaxial stacking,
terminal penalties, …), and is their §6 ("Limitations") accurate and complete about it?  (iii) Does the reduction
need unboundedly many strand *species* or only unboundedly many strands; is the encoding unary (strong
NP-hardness needs polynomially bounded numbers)?

## Item 2 — Theorem 1, line by line

Re-derive.  The points to press: (a) which base pairs are possible at all between and within the strands of the
instance (and what if the alphabet or the pairing rule is larger than they assume — wobble pairs, for instance:
does the theorem say which pairing rule it needs?); (b) the upper bound on the number of stacks, `st(S) ≤ M`;
(c) **their step (c)**: every stack has one template bond and one item bond — hence every item bond carries at
most one stack, and all are realised iff the items tile the blocks; what exactly happens at a nick between two
items inside a block, at the separator `A`, at the two ends of the template; (d) connectedness and the
unpseudoknotted condition for the structure that realises the bound, and for every structure that attains it;
(e) the symmetry term: can a complex of this instance have a rotational symmetry; (f) the association term: is
the number of strands in the complex forced, or can a structure gain by leaving items out — and if the problem
is stated for one complex containing all strands, is that the problem of the literature; (g) the equality case:
is "minimum free energy `= σM + nΔG_assoc`" really equivalent to a yes-instance of the packing problem they reduce
from, and is that problem strongly NP-hard in the form used (`a_i ≥ 1`, `Σa_i = mB`, any `m`).  State each step as:
holds / holds with a condition to add / gap / false, with the line that decides it.

## Item 3 — Theorem 3 (counting) and the partition function

The reduction must control *how many* minimum-energy structures correspond to one solution of the packing
problem: identical items, the order of items inside a block, the identity of blocks, indistinguishable strands
and the symmetry number.  Is the count a known #P-hard quantity, and is the reduction parsimonious or weakly
parsimonious with an explicit factor?  For "the partition function is #P-hard when the temperature is part of
the input": what is the encoding of the temperature, and how is the count extracted from `Z` (interpolation?
a low-temperature limit with which precision?).

## Item 4 — replication with your own code

Write your own exhaustive enumerator of the admissible structures of small instances (do not import theirs
before yours is final): for a handful of yes- and no-instances of the packing problem with a few short items,
the minimum number of... i.e. the maximum number of stacks, the minimum free energy for two or three choices of
the loop function inside (H0)–(H2), and the number of minimum-energy structures — against the theorem's values;
and a control that must fail (an instance for which the theorem's equivalence would be violated if (H0) is
dropped — for instance a negative energy for a stack across a nick).  Then run their two test scripts from a
scratch copy and compare (`<CX>/experiments/complexity/strands/`; `python3 -I -B`; their note says seconds to
minutes).

## Item 5 — novelty, as far as a short search can say

They write "our searches found no earlier proof; that does not establish novelty".  The coordinator's own search
(summaries only, papers not opened) found: Condon, Hajiaghayi and Thachuk, DNA 27 (2021) — NP-hard and APX-hard
for unboundedly many strands *in a simple energy model*; Ducloz, Shalaby and Woods, DNA 31 (2025) — the partition
function is #P-hard for unboundedly many strands in base-pair models, hardness in the nearest-neighbour model
conjectured; Shalaby and Woods, ICALP 2025 — the nearest-neighbour case for unboundedly many strands listed as
open.  Check these three statements against the papers if you can open them, and say whether the result of the
Complexity division is (i) new as far as you can see, (ii) a corollary of something published, or (iii) the
answer to a question that a paper states as open — with the sentence of the paper.

## Rules

Write only in `experiments/science/ws_R20/` and `docs/science/workstreams/R20_REPORT.md`.  No state-changing git;
no subagents; `<CX>` stays untouched (copy what you run into `ws_R20/rerun_copy/`, which will not be committed).
**Literature:** you may use web search and fetch for published papers and their definitions only, with generic
queries (titles, authors, standard terms); put no name, file or text of this project into a query; upload
nothing; cite only what you opened, and say "from memory" or "from a search summary" otherwise; never invent a
bibliographic detail.  Keep four kinds of checking apart: **review** (re-derived), **replication** (own code),
**re-run** (their code), **read only**.  A finding is *critical*, *major* or *minor*; give a replacement text for
each.  Report what you did not check, and your own errors.  Machine: 4 cores and 15 GB shared with other jobs —
`OMP_NUM_THREADS=1`, at most two processes, no process above 2 GB, no run longer than 20 minutes; before any run
of more than five minutes write its cost into `NOTES.md`.  Keep `NOTES.md` from the first minute.  A log is cited
only if its run reached its last line; logs of stopped or failed runs go into `not_cited/`; use fresh names
instead of overwriting a log.  A time written into a file is read from the clock.  Every check is reported with
the violations of its control.  **If a tool declines an action, do not work around it: keep everything in
`NOTES.md` and return the findings as text in your hand-back.  Do not delete files with wildcards or `rm -r`.**
This is an internal review, not external peer review; say so in the report.

## The report

(0) Verdict in ten lines: are Theorems 1 and 3 proved as stated; the findings by class.  (1) The statements as
you understand them, with the hypotheses the note leaves implicit.  (2) Findings, each with the line that decides
it and a replacement text.  (3) Your enumeration, with its control.  (4) Re-runs.  (5) Novelty (Item 5).
(6) Requests to the Complexity division that can be sent as they stand.  (7) What you did not check; your own
errors; files.
