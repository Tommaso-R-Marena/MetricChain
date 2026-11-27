# Status of the Structural & Computational Biology division

*Updated at the consolidation halt, 2026-11-27 (the commit time is authoritative).  Branch
`research/structural-biology`.*

## State at the consolidation halt (2026-11-27) — this section governs where it differs from the tables below

**HALTED** under the research owner's consolidation directive (recorded as SB-D-3 in
`docs/structural_biology/OWNER_DIRECTIVES.md`).  No research cycle is running and none will
start, and no message will be acted on, until the owner authorises it.  Assessment:
`docs/collaboration/consolidation/structural-biology.md`.  Final message: STRUCTBIO-MSG-0004.

| | |
|---|---|
| heads read at the fourth synchronisation (00:28 UTC, through a read-only subagent) | theory `37ce6d3`, engineering `8df6e5e`, science `92d334d`, ensemble `297ec78`, geometry `a82b1cd`, complexity `d920323`, frontier `abbbd1c` |
| models | `v1` retired (seed dependence, R-8); `v2` and `v2-lib` (hydrogens by a deterministic rule) for all further work |
| C1 certified minimum | implemented, tested, reviewed three times; development results R-1 (v1), R-9 (v2); null method R-12 |
| C1b certified gaps (state, rotamer well), optimality under entrywise table error | implemented and tested; R-6 (v1), R-10 (v2, five structures) |
| C2 certified `ln Z` and populations | implemented with conditioning, state weights and a strict file format; rule semantics machine-checked in our Lean file; R-7 (v1), R-11 (v2-lib: crambin, all populations), R-13 (why it stops) |
| C3, C4 | not started |
| C5 | blocked |
| internal review STRUCTBIO-REV-0001 | done: no false acceptance under normal use in 100 000 certificates; 19 defects outside it; repair: see `HANDOFF.md`, unfinished work, item 1 |
| release frozen for held-out evaluation | **none**; the Frontier division's sealed list has not been opened by us |
| requests of ours | REQ-0001, REQ-0004 (Engineering): unanswered; REQ-0002: answered by SCI-REV-0026, our response RES-0003; REQ-0003: Q-5 answered by COMPLEXITY-RES-0010 |
| requests and reviews received since the second checkpoint | SCI-REV-0026 (answered: RES-0003); ENG-RES-0018, ENG-MSG-0007, FRONTIER-MSG-0002, FRONTIER-REQ-0001, COMPLEXITY-RES-0010, COMPLEXITY-MSG-0005, THY-MSG-0020, ENSEMBLE-MSG-0006/-0008, ENSEMBLE-RES-0007, GEOMETRY-MSG-0009/-0010 (answered in MSG-0004) |
| compute | everything ran locally on the session machine (4 cores); no Modal, no paid service; the credit balances are not visible to this division |

## Pins

| what | commit |
|---|---|
| theory checkpoint this branch is built on (not merged since) | `b2caab6` (twenty-third checkpoint); kernel files identical at theory `eb88823` |
| heads read at the first synchronisation (21:57–22:10 UTC) | theory `eb88823`, engineering `96c4fd2`, science `71bc661`, ensemble `8d42f60`, geometry `288b2de`, complexity `25bcd61` |
| heads at the second synchronisation (22:47 UTC) | theory `6ebcccd`, engineering `640cd9c`, science `4661a03`, ensemble `2d2054d`, geometry `9f164f9`, complexity `7856192`; `research/frontier-benchmarks` did not exist |
| read from the second synchronisation | SCI-MSG-0034 in full; engineering's BM-7 (`BENCHMARK_MASTER_PLAN.md` §3a) and `PREDICTION_FREEZE.md`; head of COMPLEXITY-MSG-0005.  **Not read:** ENSEMBLE-MSG-0006, GEOMETRY-MSG-0005 … -0008, the science division's protocol of its checkpoint 65, engineering's D-6/D-7 text, theory's new commit |
| software release offered for verification | `2976042` or later (was `c128625`; see STRUCTBIO-MSG-0003, C-5) |

## Verified state of this branch

* `python -m pytest tests/structbio -q`: 47 passed, 1 skipped (slow), on the session machine at `2976042`.
* `python experiments/structbio/gmec_dev/run.py --check`: six instances rebuilt bit for bit, six
  stored certificates accepted, zero gap.
* `lake build proofs.CertificateAlgebra proofs.Frontiers.PartitionProduct`: succeeds (Lean
  4.31.0, Mathlib v4.31.0).  The full `scripts/audit_all.sh` has **not** been run on this
  branch; no file under `proofs/` or `scripts/` has been touched.

## Capabilities

| # | capability | state |
|---|---|---|
| C1 | certified global minimum of a fixed-backbone rotamer model | implemented and tested; development results R-1; verification requested (REQ-0001) |
| C1b | certified per-residue flip gaps; gap to the second-best configuration; rounding robustness | implemented and tested (`stability.py`); development results R-6 |
| C2 | certified partition function, free energy, populations | first version implemented and tested against enumeration in two arithmetic tiers (`expo.py`, `itables.py`, `zcert.py`, `zcheck.py`, `partition.py`); crambin enclosed within 1.36 nats (R-7); no conditioning, no file format, rule semantics [P] beyond two neighbours (Lean file in progress); obstruction at protein size measured (R-3) |
| C3 | ensemble partial identification on finite libraries | not started |
| C4 | geometric observability analyser | not started |
| C5 | residual-class certificates on real energy terms | blocked (no certified constant exists) |

## Internal reviews

| id | scope | state |
|---|---|---|
| (unnumbered) | specification of the `min` checker written from the code by a subagent | done; found the loader and scope defects (STRUCTBIO-MSG-0003 C-2, C-3) and the misattributed theorem (C-1) |
| STRUCTBIO-REV-0001 | adversarial review of all checkers by a subagent with a mandate to break them | in progress at this checkpoint |

## Requests we have sent

| id | to | subject | status |
|---|---|---|---|
| STRUCTBIO-REQ-0001 | engineering | independent verification, held-out run, proof-logging baseline | proposed |
| STRUCTBIO-REQ-0002 | science | adversarial review | proposed |
| STRUCTBIO-REQ-0003 | theory, complexity | four rules; question Q-5 | proposed |

## Requests and orientation received

| id | from | subject | our status |
|---|---|---|---|
| SCI-MSG-0034 (S-1 … S-6) | science | orientation; six requests | answered in REQ-0002 and MSG-0001; error budget adopted |
| BM-7, D-6, D-7 | engineering | how our software is verified; freezing predictions | read (BM-7, freeze rules); adopted |
| COMPLEXITY-MSG-0005 | complexity | algorithmic feasibility | head read; no request to us |
| SCI-REV-0025 (SB-1 … SB-5) | science | first evaluation of our software: sound as a claim about the model; rigid-rotamer discretisation measured (minimum in the wrong well for leucine; `ln Z` off by nats per torsion) | answered in STRUCTBIO-RES-0002; wording "certified minimum of the table" adopted; benchmark SB-BM-7 added |
| FRONTIER-MSG-0001 §3 | frontier | contradict the maturity table with a commit, by 2026-11-28 18:00 UTC | answered in STRUCTBIO-RES-0001 |
| ENSEMBLE-MSG-0006, -0008 | ensemble | software interface, benchmark controls; data not linear in the ensemble | received, not yet read (capability C3 is later) |
| GEOMETRY-MSG-0005 … and its implementation guide with 21 labelled test instances | geometry | orientation for us | received, not yet read (capability C4 is later) |

## Compute and budget

No Modal job, no paid API, no external paid service.  Local computation: unit tests,
development experiments of minutes on four cores.  Subagents used: eight intake reviewers, one
implementation engineer (molecular layer), three document drafters, one literature analyst.
The balance of Claude credits and of the Modal workspace is not visible from this session.
