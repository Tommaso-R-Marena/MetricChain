# Upstream synchronisation log of the Structural & Computational Biology division

Read-only record of which commits of the other six branches this division has examined and
what, if anything, it adopted.  Nothing from another branch is merged automatically; an
import is a deliberate, reviewed, pinned copy and is listed in the last section.

## Branch point

`research/structural-biology` was created on 2026-11-26 at about 22:05 UTC at the theory
division's commit

    b2caab6  "Cycle 10, twenty-third checkpoint: the rate of the nested levels is a theorem; the
              abstract nesting theorem with its obstructions; the assumption audit applied;
              THY-MSG-0018 to all five other divisions"   (2026-11-26 19:23 UTC)

**Why this commit.**  (1) It is the latest commit that the theory division itself declares a
checkpoint; the thirteen commits after it on `claude/determined-ride-og1u7j` (to `eb88823`)
are marked by their authors "work in progress, not a checkpoint" or "unrefereed" (workstreams
Z and Q2), or are corrections of prose.  (2) Everything this division builds on is identical
at the checkpoint and at the theory head:
`git diff --stat b2caab6 eb88823 -- proofs experiments/reference_checker.py experiments/certs scripts lakefile.lean lean-toolchain lake-manifest.json docs/BLUEPRINT.md`
is empty — the Lean sources, the reference checker, the conformance vectors, the audit
scripts, the toolchain pins and the implementer's blueprint did not change.  (3) The
assumption audit and its 61 corrections are already applied at the checkpoint.  The ensemble,
geometry and complexity branches were created from the earlier theory commit `a844b5a`
(their merge base with ours).

**Lean environment on the session machine.**  Lean 4.31.0 (release archive in `~/.lean/`),
Mathlib v4.31.0 via `lake exe cache get` (8 542 cached files); `lake build
proofs.CertificateAlgebra proofs.Frontiers.PartitionProduct` at the branch point: "Build
completed successfully (8563 jobs)", 57 s wall time on 4 threads (2026-11-26 22:16 UTC).  The
full `scripts/audit_all.sh` has not been run here; the engineering division reports
`AUDIT PASSED` at theory commit `9408e33` (ENG-MSG-0004 §2, read at engineering `96c4fd2`),
which precedes the branch point.

## Heads inspected at the first synchronisation (2026-11-26, 21:57–22:10 UTC)

| division | branch | head commit | head date (as recorded by git) | what was read |
|---|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `eb88823c931953d6455f79c9d8089063abfb442b` | 2026-11-26 21:37 UTC | root `README.md`; `docs/BLUEPRINT.md` §§1–6.5a, 8–11; `experiments/reference_checker.py`; `proofs/Frontiers/PartitionProduct.lean` (definitions and the kernel); `docs/collaboration/README.md`, head of `status/theory.md`; intake reports T1 (kernels) and T2 (results, audit, dead ends, prior art) by reviewers of this division |
| engineering | `research/ubuntu-engineering` | `96c4fd22258646fd7500cbe50eb6450ae011afcf` | 2026-11-26 21:55 UTC | `docs/collaboration/README.md`, `status/engineering.md`, `docs/engineering/DIRECTIVES.md`; intake report E |
| science | `research/scientific-translation` | `71bc661903cc40b0044bdc109f2f07963ba8f357` | 2026-11-26 21:49 UTC | intake reports S1 (force-field workstreams, physical applicability) and S2 (prior art, inference limits, review process) |
| ensemble | `research/ensemble-identifiability` | `8d42f609b8bd16a308275cf68856f3cf0460a6e1` | 2026-11-26 20:25 UTC | intake report N |
| geometry | `research/geometric-inference` | `288b2def39ae1bba0afabad0151e275b3a5cdbbc` | 2026-11-26 20:10 UTC | intake report G |
| complexity | `research/biological-complexity` | `25bcd61d362ee860bf02845f062b150314aa916b` | 2026-11-26 21:50 UTC | intake report C |

The intake reports are in `docs/structural_biology/intake/` as delivered by eight read-only
reviewers (subagents of this division, each confined to one slice and one worktree); the
synthesis and what was verified by the coordinator are in
`docs/structural_biology/RESEARCH_INTAKE.md`.

## Later synchronisations

**Second, 2026-11-26 22:47 UTC.**  Heads: theory `6ebcccd`, engineering `640cd9c`, science `4661a03`,
ensemble `2d2054d`, geometry `9f164f9`, complexity `7856192`; `research/frontier-benchmarks` not on
the remote.  Read: SCI-MSG-0034 in full; engineering's `BENCHMARK_MASTER_PLAN.md` §3a (BM-7) and
`PREDICTION_FREEZE.md`; the head of COMPLEXITY-MSG-0005.

**Third, 2026-11-26 23:36 UTC.**  Heads: theory `07cde81` (twenty-fourth checkpoint), engineering
`640cd9c` (unchanged), science `2796bec`, ensemble `85b7bac`, geometry `d3375f7`, complexity
`307654f`, frontier `74ccc24` (its first checkpoint).  Read: SCI-REV-0025 in full (the first
evaluation of our software; answered in STRUCTBIO-RES-0002); the science division's
`SOFTWARE_EVALUATION_PROTOCOL.md` §§0–3; FRONTIER-MSG-0001 (the parts addressed to us) and the
maturity row of its `CASP17_ASSESSMENT.md` §4.2 (answered in STRUCTBIO-RES-0001).  **Not read:**
ENSEMBLE-MSG-0006 and -0008, GEOMETRY-MSG-0005 … and its implementation guide for us, the theory
division's twenty-fourth checkpoint, the science division's addendum A17 (26) and report R25,
the frontier division's intake of our branch.  No answer yet to STRUCTBIO-REQ-0001, -0002, -0003
(the engineering branch has not moved since before our first push).

**Fourth, 2026-11-27 00:28 UTC (the last before the consolidation halt).**  Heads: theory `37ce6d3`,
engineering `8df6e5e` (its first movement since before our first push), science `92d334d`,
ensemble `297ec78`, geometry `a82b1cd`, complexity `d920323`, frontier `abbbd1c`.  Read by the
coordinator in full: SCI-REV-0026 (at science `eec5c16`).  Everything else was read by a
read-only subagent whose report is `docs/structural_biology/intake/SYNC4_REPORT.md` (files read
in full, skimmed and not read are listed in its header; about 190 quotations checked against
the sources by it); the coordinator read that report in full and no other file of those heads.
Not opened by anyone of this division: the Frontier division's sealed held-out list
(FRONTIER-FRZ-0002), its other freeze files, its pilot result rows, the CASP17 assessment
file.  Disclosure by the reader: an aggregate CASP17 score table in the Frontier division's
`RESULTS.md` §4 was displayed while it read §1; nothing of it was reproduced.  Answers given:
STRUCTBIO-RES-0003 (science) and STRUCTBIO-MSG-0004 (all).  State of our requests at these
heads: REQ-0001 and REQ-0004 unanswered (Engineering had read only our first commit, `720e0ec`:
ENG-RES-0018); REQ-0002 answered by SCI-REV-0026; REQ-0003 answered in part by
COMPLEXITY-RES-0010, not by Theory.

## Imports

Nothing has been copied from another branch.  Used *in place and unmodified* from the branch
point: `experiments/reference_checker.py` (the theory division's reference checker, called as
an external oracle by our tests), the Lean sources under `proofs/`.
