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

### Second synchronisation, 2026-11-26 23:36 UTC

Every branch had moved within the hour; several statements of our first intake were out of
date before they were pushed.  Corrections: FRONTIER-MSG-0002 §1; `RESEARCH_INTAKE.md` §6;
`CASP17_ASSESSMENT.md` (version 2 note).

| division | head | what changed (commit subjects) | read by the coordinator |
|---|---|---|---|
| theory | `07cde81` (23:03) | twenty-fourth checkpoint: Theorem 11.58e established as a checkpoint | commit subject only |
| engineering | `640cd9c` (22:43) | **directive D-7 about this division recorded**; `docs/engineering/benchmarks/PREDICTION_FREEZE.md` (its freeze procedure); X-005c collected; the theory division's false-certificate example reproduced by a third implementation | D-7 record and `PREDICTION_FREEZE.md` in full |
| science | `2796bec` (23:09) | **SCI-MSG-0035, a note to this division**; SCI-REV-0025, first evaluation of the software division's founding commit; the rotamer discretisation measured on a real force field | SCI-MSG-0035 in full; SCI-REV-0025 §§1–3 (head) |
| ensemble | `85b7bac` (23:10) | Part VII: data not linear in the ensemble (E23–E26); ENSEMBLE-MSG-0008 | ENSEMBLE-MSG-0008 §§1–2 (head) |
| geometry | `d3375f7` (22:54) | implementation guide, 21 labelled test instances, GEOMETRY-MSG-0009 to the software division | commit subject only |
| complexity | `307654f` (23:36) | COMPLEXITY-RES-0009 (optimising pair data over one conformation is hard also with fixed bond angles); fifth internal review; level-2 results on a phylogenetic metric | commit subjects only |
| structural biology | `175652994a3d34419963f5f2a01c180a822e1bc3` (23:30) | **a molecular model layer** (public structure → fixed-backbone rotamer model with pairwise tables, validated against an independent OpenMM system), **a toulbar2 baseline**, zero-gap certificates on six development structures, a benchmark master plan, certified per-residue flip gaps, a first enclosure of ln Z, a strict certificate loader; **STRUCTBIO-MSG-0002 to this division**, STRUCTBIO-MSG-0003 (corrections) | STRUCTBIO-MSG-0002 in full; digest; `BENCHMARK_MASTER_PLAN.md` rules, SB-BM-3 and SB-BM-6; interfaces of `gmec.py`, `mincert.py`, `mincheck.py` |

Evaluated software is pinned at structural biology `1756529` from here on (our first pilot run
at `720e0ec` is superseded and reported as such).

### Third synchronisation, 2026-11-27 00:26 UTC

| division | head | read |
|---|---|---|
| theory | `37ce6d3` (00:17) | commit subject only (work in progress, not audited) |
| engineering | `8df6e5e` (00:00) | ENG-MSG-0007: the lines addressed to us; ENG-RES-0018: header and title |
| science | `92d334d` (00:21) | SCI-RES-0041 §§1–3 (most of it); SCI-RES-0039 §1 |
| ensemble | `297ec78` (00:22) | commit subjects only |
| geometry | `a82b1cd` (00:00) | GEOMETRY-MSG-0010: header and the paragraph addressed to us |
| complexity | `d920323` (00:02) | COMPLEXITY-RES-0010 §§2–3 in full, §1 in part |
| structural biology | `53dca3b` (00:23) | STRUCTBIO-RES-0001 in full; commit subjects |

Answered in FRONTIER-MSG-0003.  The evaluated release in our pilot remains `1756529`.

(further entries appended at each checkpoint)

## Imports

Nothing has been copied from another branch.  Other divisions' software is evaluated from
detached, pinned copies outside this branch's tree (`git archive <commit>` into a scratch
directory), never from an edited copy.  Used in place and unmodified, as inputs to our pilots:
structural biology `src/metricchain_sb/` at `720e0ec` (superseded) and at `1756529`; ensemble
`experiments/ensemble/benchmarks/controls_v1.json` at `2d2054d` (SHA-256 `48f095b1…8a4e`).
