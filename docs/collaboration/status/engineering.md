# Status of the Computational Research Division

*Updated 2026-11-25 05:45 UTC.  Branch `research/ubuntu-engineering`.*

## Pins

| what | commit |
|---|---|
| theory checkpoint this branch is built on | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` (audit replicated: ENG-RES-0005) |
| latest theory commit read | `1bff191` (mailbox only; nothing merged) |

## Verified state of the engineering branch

* `bash scripts/audit_all.sh --full` (the theory division's audit, unmodified) passes on this
  branch: the engineering additions do not disturb it.
* `python -m pytest tests/eng -q`: 69 tests pass.
* `python experiments/eng/chain_cover/run_lattice.py --check`: all published values of
  `P_REPORT.md` §3.3 reproduced.
* `python experiments/eng/chain_cover/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0002.md`:
  the tables of that message equal the stored artifacts.

## Requests received from the Theoretical Research Division

| id | subject | decision | status | response |
|---|---|---|---|---|
| THY-REQ-0001 | attack the cost claim of the two-level algorithm (§11.18) | accepted | **not started** — next after the chain work | ENG-RES-0001 |
| THY-REQ-0002 | exact chain covering beyond 12 torsions | accepted | **in progress** — lattice chain: enumeration to 24 torsions, covers, entropy, patterns (proved for all `n`), single-flip constants and envelope test done; generic chain, sampling, sum class, span format pending | ENG-RES-0002 |
| THY-REQ-0003 | useful constants in the profile format? | accepted in a revised design | not started | ENG-RES-0003 |
| THY-REQ-0004 | schema, checker, producer for the linear kernel | accepted, with differential testing against the Lean definitions | not started | ENG-RES-0004 |
| THY-REQ-0005 | independent replication of the audit | accepted | **completed** — no divergence | ENG-RES-0005 |
| THY-REQ-0006 | exact hitting numbers over all sensitive sets | deferred | uniform cube done in closed form; general computation deferred with a better pricing formulation | ENG-RES-0006 |

## Requests sent to the Theoretical Research Division

| id | subject | status |
|---|---|---|
| ENG-REQ-0001 | a limit shape for profile sets: formulation of the thermodynamic limit of certificate sizes; what the lower bounds need from the single-flip constants | proposed |

Two smaller questions are inside responses: the reading of the sup-norm remainder term
(ENG-RES-0003) and whether evaluation order at `split`/`branch` nodes is part of the kernel
specification (ENG-RES-0004).

## Engineering agenda (independent of requests; ENG-MSG-0001)

| item | subject | status |
|---|---|---|
| E-1 | what is actually trusted: the Lean kernel definitions run on generated certificates, against the Python reference checker | planned |
| E-2 | what a native `min` certificate costs at realistic sizes (producer, fast checker, synthetic chains, public fixed-sequence side-chain-positioning instances) | planned |
| E-3 | which class do residuals live in (first-order, second-order, linear-in-features constants, exactly on enumerable domains) | planned (with THY-REQ-0003) |
| E-4 | limit shape of profile sets | data available; question sent (ENG-REQ-0001) |

## Compute

Remote usage so far: five small Modal jobs (M-001…M-005), of the order of two dollars in
total; details and bounds in `docs/engineering/COMPUTE_LEDGER.md`.  No app is deployed; no
workload is left running at the time of this update except as stated in the ledger.
Self-imposed ceiling until the research owner confirms a workspace usage limit: worst case
below $10 per job, $50 cumulative.

## Synchronisation log

See `docs/collaboration/UPSTREAM_SYNC.md`.
