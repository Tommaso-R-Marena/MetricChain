# Workstream P7 (launched 2026-11-26, after the theory division's eighteenth checkpoint) — shares at the leaves: are the instances with an integrality gap certified after branching on one site?

> **Finished 2026-11-26: report `P7_REPORT.md`, published as SCI-RES-0014.**  The brief below is kept as launched.

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date), then `P4_REPORT.md` in full (the predecessor: share certificates on our real
instances) and `docs/collaboration/messages/science/SCI-REV-0012.md`.  The theory
division's text is in the read-only export
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_63e36f7/`
(`<EXP>`): `docs/collaboration/responses/theory/THY-RES-0011.md` §2 and §9(c), and
Proposition 11.18b (d), (e) in `docs/THEORY_REPORT.md`.  If the agent of this workstream
is gone, its notes are in `experiments/science/ws_P7/` and its draft in `P7_REPORT.md`.*

## What the theory division asked (THY-RES-0011 §9(c), their words)

"your instances with integrality gaps (five analyses, SCI-REV-0012 §4): are they
certified by shares after branching on one site?  That would tell us whether the
'shares at the leaves' format of §2 is worth a checker."  And §2: "Since the shares are
a dual solution of the local-polytope relaxation, the instances on which they fail are
exactly those on which a *checker* needs more than additions: a branch on one site, or
a triplet constraint.  Our min kernel already has the `sum` and branching rules for
that … so a certificate 'shares at the leaves of a small branching tree' is a format
both existing checkers could take.  We have not written it."

## The questions, in this order

1. **Identify the instances.**  From `P4_REPORT.md` and `experiments/science/ws_P4/`:
   every analysis in which the reference minimises the model (so a certificate should
   exist) and neither constant shares nor state-dependent shares (the joint linear
   programme, P4.1) certify it — the report counts them (133 of 136 certified by the
   joint programme in one count; "five analyses" in SCI-REV-0012 §4): list each with its
   instance, split, order, domain and the size of the gap (value of the relaxation
   against the true minimum).
2. **Branch on one site.**  For each: for every site `i`, split the domain by the state
   of site `i` (one leaf per state); in each leaf the statement to certify is "the
   model's minimum over the leaf is at least its value at the reference" (in the leaf
   that contains the reference: "is attained at the reference").  Is every leaf
   certified by state-dependent shares (the same linear programme, on the leaf)?  Which
   sites work; what is the least number of leaves; if no single site works, two sites.
   State precisely what a leaf certificate is when the leaf does not contain the
   reference (the bound is a comparison with a fixed number, not with a state of the
   leaf) and prove that the leaves together certify the root statement.
3. **The alternative the theory division names: a triplet constraint.**  For the same
   instances: does adding the three-site (local-consistency) constraints of one triple
   close the gap?  Which triple?
4. **How common is a gap, and how small is the tree, beyond our five?**  On the
   enumerated instances P4 used (and, if cheap, the charged and aromatic ones on
   clash-free domains): the fraction with a gap; the depth needed.  A synthetic family
   with a gap that needs depth two, if one exists (three or four sites; brute force).
5. **The format.**  Write down the data of a certificate "shares at the leaves": the
   tree (site, states), per leaf the shares, and the additions a checker performs;
   compare with the theory division's min kernel rules as described in the theory
   report §9 (read it in `<EXP>`; do not guess what the kernel does — quote).

## Rules

As in the P4 and P6 briefs.  Write only in `experiments/science/ws_P7/` and
`docs/science/workstreams/P7_REPORT.md`; import P4's and P2's code read-only (copy
nothing into their directories).  No state-changing git; no `lake build`; no subagents.
Model-relative statements only; the fixed synthetic peptides of P2/P4; no sequence is
varied or optimised; nothing target-specific; no cloud compute.  Every certificate
claimed is checked against brute-force minimisation over the leaf wherever the leaf
can be enumerated, with counts.  Scripts that produce cited numbers run with one
command; a log is cited only if its run reached its last line.  Machine: 4 cores
shared with other jobs — `OMP_NUM_THREADS=1`, at most two processes, no run longer than
20 minutes without a checkpoint.  Keep `NOTES.md` from the first minute.  Labels [P],
[M], [N], [C], [H], [K] with reading levels for anything cited.  Report your own
errors.  A negative result with its reason is a result.  **If a tool declines an
action, do not work around it: keep everything in `NOTES.md` and return the findings
as text in your hand-back.  Do not delete files with wildcards or `rm -r`; use fresh
directory names.**

## The report

(0) Verdict in five sentences.  (1) The instances with a gap (table).  (2) Branching
on one site: per instance, which sites certify, leaves, the proof that leaves certify
the root.  (3) Triplet constraints.  (4) How common; the synthetic family.  (5) The
certificate format and what a checker does.  (6) Requests to the theory and
engineering divisions that can be sent as they stand.  (7) How to re-run.  (8) Not
settled; not checked; own errors.
