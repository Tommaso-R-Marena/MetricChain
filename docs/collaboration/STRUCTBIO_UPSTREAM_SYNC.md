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

(appended at each checkpoint: date, heads, what changed, what was read)

## Imports

Nothing has been copied from another branch.  Used *in place and unmodified* from the branch
point: `experiments/reference_checker.py` (the theory division's reference checker, called as
an external oracle by our tests), the Lean sources under `proofs/`.
