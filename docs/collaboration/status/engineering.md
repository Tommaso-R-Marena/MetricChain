# Status of the Computational Research Division

*Updated at checkpoint 2 of the engineering branch (2026-11-25, about 06:00 UTC; the commit
time is authoritative).  Branch `research/ubuntu-engineering`.*

## Pins

| what | commit |
|---|---|
| theory checkpoint this branch is built on (branch point; not merged since) | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` — audit replicated (ENG-RES-0005) |
| latest theory commit read | `4cef47e` (THY-MSG-0003, THY-MSG-0004 read in full) |
| latest theory commit audited on the engineering machine | `4cef47e` — `AUDIT PASSED`, 46 Lean files, 3101 declarations (ENG-MSG-0002) |

## Verified state of the engineering branch

* `bash scripts/audit_all.sh --full` (the theory division's audit, unmodified) passes on this
  branch: the engineering additions do not disturb it.
* `python -m pytest tests/eng -q`: 78 tests pass.
* `python experiments/eng/chain_cover/run_lattice.py --check`: all published values of
  `P_REPORT.md` §3.3 for the lattice chain reproduced.
* `python experiments/eng/chain_cover/make_tables.py --verify <ENG-RES-0002.md | ENG-RES-0007.md>`:
  the tables of both messages equal the stored artifacts.

## Requests received from the Theoretical Research Division

| id | subject | decision | status | response |
|---|---|---|---|---|
| THY-REQ-0001 | attack the cost claim of the two-level algorithm (§11.18) | accepted | **not started**; plan revised after THY-MSG-0003 (end-to-end with real inner brackets, non-radial outer laws, three levels) | ENG-RES-0001, ENG-MSG-0002 §4 |
| THY-REQ-0002 | exact chain covering beyond 12 torsions | accepted | **in progress** — lattice chain complete to 24 torsions (questions 1, 2 exhaustive, 3(a), 3(b)); generic chain reproduced and extended to 12 torsions; open: generic chain beyond 12 and its questions 3(a), 3(b), sampling for question 2, questions 4 and 5 | ENG-RES-0002, ENG-RES-0007 |
| THY-REQ-0003 | useful constants in the profile format? | accepted in a revised design | not started | ENG-RES-0003 |
| THY-REQ-0004 | schema, checker, producer for the linear kernel | accepted, with differential testing against the Lean definitions | not started | ENG-RES-0004 |
| THY-REQ-0005 | independent replication of the audit | accepted | **completed** at `d81eb8a`, repeated at `4cef47e` — no divergence | ENG-RES-0005, ENG-MSG-0002 §2 |
| THY-REQ-0006 | exact hitting numbers over all sensitive sets | deferred | uniform cube done in closed form; general computation deferred with a better pricing formulation | ENG-RES-0006 |

## Requests and questions sent to the Theoretical Research Division

| id | subject | status |
|---|---|---|
| ENG-REQ-0001 | a limit shape for profile sets: formulation of the thermodynamic limit of certificate sizes; what the lower bounds need from the single-flip constants | proposed |
| ENG-MSG-0002 §4 | is the algorithm text of §11.18 at `4cef47e` the version to attack, and do `lv_two_level` / `lv_check_run` implement its abort rule? | proposed |
| ENG-RES-0003 | reading of the sup-norm remainder term `η(1 + ‖λ‖₁)` | proposed |
| ENG-RES-0004 | is evaluation order at `split`/`branch` nodes part of the kernel specification? | proposed |

## Engineering agenda (independent of requests; ENG-MSG-0001)

| item | subject | status |
|---|---|---|
| E-1 | what is actually trusted: the Lean kernel definitions run on generated certificates, against the Python reference checker | planned |
| E-2 | what a native `min` certificate costs at realistic sizes | planned |
| E-3 | which class do residuals live in (with THY-REQ-0003) | planned |
| E-4 | limit shape of profile sets | data available; question sent (ENG-REQ-0001) |

## Compute

Seven small Modal jobs (M-001…M-007), **$2.48 in total**; none is running (`modal app list`:
all stopped, 0 tasks); nothing is deployed.  Bounds, measured costs and the two jobs that
were stopped by hand: `docs/engineering/COMPUTE_LEDGER.md`.  Self-imposed ceiling until the
research owner confirms a workspace usage limit: worst case below $10 per job, $50
cumulative.

## Synchronisation log

See `docs/collaboration/UPSTREAM_SYNC.md`.
