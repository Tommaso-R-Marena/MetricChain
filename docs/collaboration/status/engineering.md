# Status of the Computational Research Division

*Updated at checkpoint 3 of the engineering branch (2026-11-25; the commit time is
authoritative).  Branch `research/ubuntu-engineering`.*

## Pins

| what | commit |
|---|---|
| theory checkpoint this branch is built on (branch point; not merged since) | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` — audit replicated (ENG-RES-0005) |
| latest theory commit read | `63efc69` (THY-MSG-0005…0008, THY-REQ-0007, -0008, THY-RES-0002 read in full; what else was and was not read: ENG-MSG-0003 §1) |
| latest theory commit audited on the engineering machine | `63efc69` — `AUDIT PASSED`, 53 Lean files, 3369 declarations (ENG-MSG-0003 §2) |
| text that experiments X-005, X-006 implement | `docs/workstreams/K_REPORT.md` §§2–3 at `63efc69` |

## Verified state of the engineering branch

* `bash scripts/audit_all.sh --full` (the theory division's audit, unmodified) passes on this
  branch: the engineering additions do not disturb it.
* `python -m pytest tests/eng -q`: 128 tests pass.
* `python experiments/eng/chain_cover/run_lattice.py --check`: all published values of
  `P_REPORT.md` §3.3 for the lattice chain reproduced.
* `python experiments/eng/twolevel/controls.py --theory <checkout of 63efc69>`: 324 + 18 published
  rows of workstream K reproduced (two of them only with plain floating-point comparisons:
  ENG-MSG-0003 §5).
* `make_tables.py --verify` (`experiments/eng/chain_cover/` for ENG-RES-0002, -0007, -0009;
  `experiments/eng/twolevel/` for ENG-RES-0008): the tables of the messages equal the stored
  artifacts.

## Requests received from the Theoretical Research Division

| id | subject | decision | status | response |
|---|---|---|---|---|
| THY-REQ-0001 | adversarial evaluation of the two-level algorithms' validity and cost (target: Algorithm 2L⁺) | accepted | **in progress** — two levels at a bounded accuracy done: Parts B and C (no claim violated; the flat instance is not the worst one; crossover moved), outer loop of Part A; open: three levels on non-flat instances, the extensive regime of §11.18, real inner brackets beyond 13 coordinates | ENG-RES-0001, ENG-MSG-0002 §4, **ENG-RES-0008** |
| THY-REQ-0002 | exact chain covering beyond 12 torsions | accepted | **in progress** — lattice chain complete to 24 torsions; generic chain: covers to 12 torsions, class tables to 14 (published counts at 13 reproduced); open: generic covers beyond 12 and its questions 3(a), 3(b), sampling for question 2, questions 4 and 5 | ENG-RES-0002, ENG-RES-0007, ENG-RES-0009 §2 |
| THY-REQ-0003 | useful constants in the profile format? | accepted in a revised design | not started (your clarification of the remainder term received) | ENG-RES-0003 |
| THY-REQ-0004 | schema, checker, producer for the linear kernel | accepted, with differential testing against the Lean definitions | not started (your answer on evaluation order received) | ENG-RES-0004 |
| THY-REQ-0005 | independent replication of the audit | accepted | **completed** at `d81eb8a`, repeated at `4cef47e` and at `63efc69` — no divergence | ENG-RES-0005, ENG-MSG-0002 §2, ENG-MSG-0003 §2 |
| THY-REQ-0006 | exact hitting numbers over all sensitive sets | deferred | uniform cube done in closed form; general computation deferred | ENG-RES-0006 |
| THY-REQ-0007 | exact tail function of the flat-histogram reference; adversarial test of Theorem 11.63 | accepted | not started; what will be done is fixed in the response | **ENG-RES-0010** |
| THY-REQ-0008 | limit shape of profile sets: vertices, walks against bridges, plateau, off-lattice distance entropy | accepted | **in progress** — item 5 and the single-flip part of item 6 done; items 1–4 and the bridge tables not started | **ENG-RES-0009** |

## Requests and questions sent to the Theoretical Research Division

| id | subject | status |
|---|---|---|
| ENG-REQ-0001 | a limit shape for profile sets | **completed** by THY-RES-0001, -0002 |
| ENG-MSG-0002 §4, ENG-RES-0003, ENG-RES-0004 | three questions (version of §11.18, sup-norm remainder, evaluation order) | **answered** in THY-MSG-0005 §3 |
| ENG-MSG-0003 | is the flat-instance cost table quoted without its qualification?  Is the worst instance of Algorithm 2L⁺ at finite `n` stated anywhere? | proposed |
| ENG-RES-0008, follow-up 2 and 3 | can the sample bound `M̄` be lowered to a multiple of `M†`?  Please check the reduction of outer landscapes to tail functions (§5) | proposed |

## Engineering agenda (independent of requests; ENG-MSG-0001)

| item | subject | status |
|---|---|---|
| E-1 | what is actually trusted: the Lean kernel definitions run on generated certificates, against the Python reference checker | planned |
| E-2 | what a native `min` certificate costs at realistic sizes | planned |
| E-3 | which class do residuals live in (with THY-REQ-0003) | planned |
| E-4 | limit shape of profile sets | answered by the theory division (THY-RES-0002); computations that would narrow it: THY-REQ-0008 |

## Compute

Session 1: seven small Modal jobs (M-001…M-007), $2.48.  Session 2: jobs M-008…M-011 for
X-005 and X-006; bounds, measured costs, the research owner's ceiling and the workspace
limits are in `docs/engineering/COMPUTE_LEDGER.md`.  No engineering app is deployed; whether
one is running is stated at the end of the ledger.

## Synchronisation log

See `docs/collaboration/UPSTREAM_SYNC.md`.
