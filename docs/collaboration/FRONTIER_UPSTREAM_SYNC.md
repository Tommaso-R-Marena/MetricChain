# Upstream synchronisation log of the Frontier Benchmarking division

Read-only record of which commits of the other seven branches this division has examined and
what, if anything, it adopted.  Nothing from another branch is merged automatically; an
import is a deliberate, reviewed, pinned copy and is listed in the last section.

## Branch point

`research/frontier-benchmarks` was created on 2026-11-26 at about 22:50 UTC at the theory
division's commit

    b2caab6  "Cycle 10, twenty-third checkpoint: the rate of the nested levels is a theorem; the
              abstract nesting theorem with its obstructions; the assumption audit applied;
              THY-MSG-0018 to all five other divisions"   (2026-11-26 19:23 UTC)

**Why this commit.**  (1) It is the latest commit that the theory division itself declares a
checkpoint; the fourteen commits after it on `claude/determined-ride-og1u7j` (to `6ebcccd`)
are marked by their authors "work in progress", "not yet audited" or "unrefereed", or are
corrections of prose.  (2) It is the branch point the structural-biology division chose and
justified an hour earlier (`STRUCTBIO_UPSTREAM_SYNC.md` at `720e0ec`), so the software under
evaluation and its evaluator inherit the same frozen snapshot of the theory files.
(3) Nothing an evaluation would execute differs between the checkpoint and the theory head:
`git diff --stat b2caab6 6ebcccd -- proofs experiments/reference_checker.py experiments/certs scripts lakefile.lean lean-toolchain lake-manifest.json docs/BLUEPRINT.md`
is empty (checked 2026-11-26 22:49 UTC).  This division builds no mathematics on the snapshot;
it cites other divisions' results from their own branches at the commits below.

The session harness had created a branch `claude/exciting-franklin-867ejh` at the theory head
`6ebcccd`; it is not used (see `docs/frontier_benchmarks/OWNER_DIRECTIVES.md`, last section).

## Heads inspected at the first synchronisation (2026-11-26, 22:35–23:00 UTC)

| division | branch | head commit | head date (git) | what was read, and by whom |
|---|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `6ebcccd81b3a67a84a320a79bab4a9974a9fa7e8` | 2026-11-26 22:04 UTC | coordinator: root `README.md` (status), `docs/collaboration/README.md`; intake reviewer TE (subagent): README, `BLUEPRINT.md`, theory report §§6.4, 8, 9, 10, 12 by section, `ASSUMPTION_AUDIT.md`, `benchmarks_output.txt`, headers of the benchmark and checker scripts, head of `status/theory.md`, THY-MSG-0018.  Not read: theory report §11 in full, any Lean file, the referee reports |
| engineering | `research/ubuntu-engineering` | `c683fde48da4004713691983392c74e3cbeaff07` | 2026-11-26 22:24 UTC | coordinator: `docs/engineering/benchmarks/BENCHMARK_MASTER_PLAN.md`, `BENCHMARK_READINESS.md`, `BENCHMARK_RESULTS.md` in full; intake reviewer TE: `DIRECTIVES.md`, `COMPUTE_LEDGER.md`, `EXPERIMENT_REGISTER.md`, all of `benchmarks/`, `status/engineering.md`, `ENGINEERING_TO_THEORY.md`, drafts (summaries), `leafcert/REPORT.md`, inventory of `src/`, `tests/`, `modal_jobs/`.  Not read in full: ENG-RES-0002/0008/0013/0014, ENG-MSG-0001…0006 |
| science | `research/scientific-translation` | `4661a037eaa0c4e889ce29778412e00322ac5b69` | 2026-11-26 22:27 UTC | coordinator: `docs/science/SOFTWARE_EVALUATION_PROTOCOL.md` in full, `BENCHMARK_DESIGN.md` §§0–2 (B1–B5); intake reviewer S: `OWNER_DIRECTIVES.md`, `SOFTWARE_EVALUATION_PROTOCOL.md`, `BENCHMARK_DESIGN.md`, `PRIOR_ART_MATRIX.md`, SCI-MSG-0033/0034, SCI-REV-0006, SCI-RES-0030 and the request template in full; the large synthesis, validation, applicability, inference-limit and status files by section.  Not read: workstream reports, `INFERENCE_LIMITS_ADDENDA.md` |
| ensemble | `research/ensemble-identifiability` | `2d2054ddefdd4e586719bbee8094684b18ed46e0` | 2026-11-26 22:34 UTC | intake reviewer EGC (subagent): digest, status, theorem register, report, `BENCHMARK_CONTROLS.md`, `SOFTWARE_INTERFACE.md`, prior art, dead ends, handoff, obligations |
| geometry | `research/geometric-inference` | `9f164f9795f4dd50e704246a862d68ef95238578` | 2026-11-26 22:35 UTC | intake reviewer EGC: digest, status, theorem register, reports, prior art, dead ends, handoff, requests GEOMETRY-REQ-0001…0006 and responses |
| complexity | `research/biological-complexity` | `75266b2508477ae419666c4d2f87b6ef1b00041b` | 2026-11-26 22:05 UTC | intake reviewer EGC: digest, status, `THEOREMS.md`, reports, prior art, dead ends, handoff, open problems |
| structural biology | `research/structural-biology` | `720e0ec9130c59ff574b473d822b0485f23827de` | 2026-11-26 22:30 UTC | coordinator: `OWNER_DIRECTIVES.md`, `STRUCTBIO_UPSTREAM_SYNC.md`, `docs/collaboration/README.md`, `src/metricchain_sb/model.py` and `synthetic.py` in full, `gmec.py`, `mincert.py`, `mincheck.py` by docstring and signature, `requirements-structbio.txt` |

The intake reviewers were read-only subagents of this division, each confined to its slice
and to the pinned commits above; none re-ran another division's scripts or checked a proof.
Their reports are condensed, with what the coordinator verified directly, in
`docs/frontier_benchmarks/RESEARCH_INTAKE.md`.

## Later synchronisations

(appended at each checkpoint: date, heads, what changed, what was read)

## Imports

Nothing has been copied from another branch.  Other divisions' software is evaluated from
detached, pinned copies outside this branch's tree, never from an edited copy.
