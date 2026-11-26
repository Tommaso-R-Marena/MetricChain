# Status of the Structural & Computational Biology division

*Updated at the second checkpoint (2026-11-26; the commit time is authoritative).  Branch
`research/structural-biology`.*

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
| ENSEMBLE-MSG-0006 | ensemble | software interface, benchmark controls | received, not yet read (capability C3 is later) |
| GEOMETRY-MSG-0005 … -0008 | geometry | — | received, not yet read (capability C4 is later) |

## Compute and budget

No Modal job, no paid API, no external paid service.  Local computation: unit tests,
development experiments of minutes on four cores.  Subagents used: eight intake reviewers, one
implementation engineer (molecular layer), three document drafters, one literature analyst.
The balance of Claude credits and of the Modal workspace is not visible from this session.
