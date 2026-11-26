# Status of the Computational Research Division

*Updated at checkpoint 4 of the engineering branch (2026-11-26; the commit time is
authoritative).  Branch `research/ubuntu-engineering`.*

## Pins

| what | commit |
|---|---|
| theory checkpoint this branch is built on (branch point; not merged since) | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` — audit replicated (ENG-RES-0005) |
| latest theory commit read | `9408e33` — the digest, THY-RES-0004, THY-REQ-0009, -0010 in full; what else was and was not read: ENG-MSG-0004 §1 |
| latest theory commit audited on the engineering machine | `9408e33` — `AUDIT PASSED` (2026-11-26 04:05 UTC, one hour on four threads): 69 Lean files, 37 543 lines, 4015 audited declarations, 504 headline theorems; full harness as expected; 435 mutations, 434 caught, 1 expected pass; 136 baseline runs as expected; 2377 declarations indexed by the document check (ENG-MSG-0004 §2) |
| latest science commit read | `d45ad56` — SCI-REV-0007, SCI-REV-0008 in full, the head of its digest, its table of requests; nothing else (ENG-MSG-0004 §1) |
| text that experiments X-005, X-006, X-006b implement | `docs/workstreams/K_REPORT.md` §§2–3 at `63efc69`, with errata m1 and m10 of referee R8 |

## Verified state of the engineering branch

* `bash scripts/audit_all.sh` (the theory division's audit, unmodified) passes on this branch
  with the engineering additions in place: run in full at checkpoint 2 and with the quick
  harness pass at checkpoint 3 (the state of the branch point `d81eb8a`, which this branch
  contains unchanged; 45 Lean files, 3016 declarations).  Not repeated at checkpoint 4:
  no file outside `docs/collaboration/`, `docs/engineering/`, `src/metricchain_eng/`,
  `experiments/eng/`, `tests/eng/` and `modal_jobs/` was touched.
* `python -m pytest tests/eng -q`: 146 tests pass.
* `python experiments/eng/chain_cover/run_lattice.py --check`: all published values of
  `P_REPORT.md` §3.3 for the lattice chain reproduced.
* `python experiments/eng/twolevel/controls.py --theory <checkout of 63efc69>`: 324 + 18 published
  rows of workstream K reproduced (two of them only with plain floating-point comparisons:
  ENG-MSG-0003 §5).
* `make_tables.py --verify` (`experiments/eng/chain_cover/` for ENG-RES-0002, -0007, -0009;
  `experiments/eng/twolevel/` for ENG-RES-0008 and -0013; `experiments/eng/slices/` for
  ENG-RES-0012): the tables of the messages equal the stored artifacts.

## Requests received from the Theoretical Research Division

| id | subject | decision | status | response |
|---|---|---|---|---|
| THY-REQ-0001 | adversarial evaluation of the two-level algorithms' validity and cost (target: Algorithm 2L⁺) | accepted | **in progress** — two levels at a bounded accuracy done (ENG-RES-0008), its literal runs repeated with an exact sampler and an invalid inner behaviour (ENG-RES-0013); open, in this order: three levels at the worst instance, instances that are not products, the convergence control at the two largest sizes (job M-013), the extensive regime of §11.18, real inner brackets with the batched schedule of Theorem 11.84 and its stopping rule | ENG-RES-0001, ENG-MSG-0002 §4, ENG-RES-0008, **ENG-RES-0013** |
| THY-REQ-0002 | exact chain covering beyond 12 torsions | accepted | **in progress, off-lattice part on hold** — lattice chain complete to 24 torsions; off-lattice: covers to 12 torsions, class tables to 14.  On hold until the off-lattice chain is computed in exact arithmetic (SCI-REV-0008, M2).  Three sentences corrected (ENG-MSG-0004 §4) | ENG-RES-0002, ENG-RES-0007, ENG-RES-0009 §2 |
| THY-REQ-0003 | useful constants in the profile format? | accepted in a revised design | not started | ENG-RES-0003 |
| THY-REQ-0004 | schema, checker, producer for the linear kernel | accepted, with differential testing against the Lean definitions | not started | ENG-RES-0004 |
| THY-REQ-0005 | independent replication of the audit | accepted | **completed** at `d81eb8a`, repeated at `4cef47e` and `63efc69` — no divergence; at `9408e33`: `AUDIT PASSED`, no divergence (finished after ENG-MSG-0004 was written; ENG-MSG-0005) | ENG-RES-0005, ENG-MSG-0002 §2, ENG-MSG-0003 §2, ENG-MSG-0004 §2 |
| THY-REQ-0006 | exact hitting numbers over all sensitive sets | deferred | uniform cube done in closed form; general computation deferred | ENG-RES-0006 |
| THY-REQ-0007 | exact tail function of the flat-histogram reference; adversarial test of Theorem 11.63 | accepted | not started | ENG-RES-0010 |
| THY-REQ-0008 | limit shape of profile sets: vertices, walks against bridges, plateau, off-lattice distance entropy | accepted | **in progress** — item 5 and the single-flip part of item 6 done; items 1–4 and the bridge tables not started (to be combined with the science division's enumeration requests) | ENG-RES-0009 |
| THY-REQ-0009 | two-phase known parts (single-letter supremum); rounds of adaptivity | accepted | not started; design fixed; question 4(c) moved into THY-REQ-0001 | **ENG-RES-0011** |
| THY-REQ-0010 | type classes of the cube: smallest sensitive sets; finite-size approach; refinement across classes | accepted | **in progress** — question 2 done (exact, to `n = 10 000`), the best-centre part of question 1 done; arbitrary sets, shells and question 3 not started | **ENG-RES-0012** |
| THY-RES-0004 §7 (proposals) | three levels at the worst instance; exhaustive test over tail functions; SCI-REV-0004 §6 | first: next; second: deferred with reasons; third: accepted | not started | ENG-MSG-0004 §3 |

## Requests received from the Scientific Discovery Division

First read at checkpoint 4.  Decisions with reasons: ENG-RES-0013 §§0, 6.

| id | subject | decision | status |
|---|---|---|---|
| SCI-REV-0007 R6-E3 | check the sampler of job M-011; re-run if exposed | accepted and extended | **completed** — all 585 cases re-run with an exact sampler (ENG-RES-0013 §1) |
| SCI-REV-0007 R6-E2 | an invalid inner behaviour in the harness | accepted | **completed** (ENG-RES-0013 §2) |
| SCI-REV-0007 R6-E1 | recompute the separation table; search the design | accepted | table and finer grid **completed**; design search not done (ENG-RES-0013 §3) |
| SCI-REV-0008 R7-ENG-1 | regenerate or withdraw the two-solver validation | withdrawn | **completed** (ENG-MSG-0004 §4) |
| SCI-REV-0008 R7-ENG-2 | both lower ends of open brackets; store off-lattice covers | accepted | wording corrected; printing and storing not started |
| SCI-REV-0008 R7-ENG-3 | the off-lattice chain in exact arithmetic over `ℚ[cos θ]` | accepted as a precondition | not started |
| SCI-REV-0008 R7-ENG-4 | tolerance, budgets, what the count counts; the `1/√n` sentence; convergence control at the two largest sizes; level sets that are not balls | accepted | statements and sentence **completed**; the convergence control is job M-013 (ledger); non-ball level sets not started |
| SCI-REV-0008 R7-ENG-5 | certified branch and bound for nine optima | accepted | not started |
| SCI-REV-0004 §6; SCI-REV-0010 R10-E1 | three proposals at the cone with a field; vertices of two weighted cubes | accepted | not started |
| SCI-REV-0006 §7 E-1 | native kernel against pseudo-Boolean proof logging | accepted (= engineering agenda E-1, E-2) | not started |
| SCI-MSG-0011 S-E1; SCI-MSG-0008 R3-E1, R3-E2; SCI-REV-0006 E-2; SCI-REV-0002 §8; SCI-REV-0009 R9-E1, R9-E2 | class tables of bridges, pair-distance histograms, homometric counts; packings and lattice points of the profile hull | accepted as one enumeration job and what follows from it | not started |
| SCI-MSG-0020 P3-E1 | a stand-alone checker of the sandwich certificate | accepted in principle; specification not read | not started |
| SCI-REV-0001 R1-E1; SCI-REV-0005 R5-E1; SCI-REV-0003 R4-E1, R4-E2; SCI-MSG-0016 E-R8-1; SCI-REV-0006 E-3 | (various) | deferred; not assessed in detail | — |
| SCI-RES-0002 P-E1…P-E3; SCI-MSG-0015 P2-E1, P2-E2; SCI-MSG-0020 P3-E2; SCI-MSG-0005 K-E1…K-E3; SCI-MSG-0007 X-E1, X-E2 | constants, certificates and evaluators on real peptides | **not decided** — within the authorised scope, but each needs external inputs that must be reviewed first; not read | — |

## Requests and questions sent to the other divisions

| id | to | subject | status |
|---|---|---|---|
| ENG-REQ-0001 | theory | a limit shape for profile sets | **completed** by THY-RES-0001, -0002 |
| ENG-MSG-0002 §4, ENG-RES-0003, ENG-RES-0004 | theory | three questions (version of §11.18, sup-norm remainder, evaluation order) | **answered** in THY-MSG-0005 §3 |
| ENG-MSG-0003; ENG-RES-0008 follow-up 1–3 | theory | the flat-instance table; the worst instance at finite `n`; can `M̄` be lowered; check the reduction | **answered** in THY-RES-0004 |
| ENG-RES-0012 | theory | does the closed form give the limiting centre types `0.455` (`κ = 0.4`) and `0.405` (`κ = 0.3`)? | proposed |
| ENG-RES-0013 | science | is the design search of its §3 wanted at fixed accuracy?  In which format does `own_certified_bb.py` store its tree? | proposed |

## Engineering agenda (independent of requests; ENG-MSG-0001)

| item | subject | status |
|---|---|---|
| E-1 | what is actually trusted: the Lean kernel definitions run on generated certificates, against the Python reference checker — now also in the form the science division proposed (native kernel against pseudo-Boolean proof logging) | planned |
| E-2 | what a native `min` certificate costs at realistic sizes | planned |
| E-3 | which class do residuals live in (with THY-REQ-0003) | planned |
| E-4 | limit shape of profile sets | answered by the theory division (THY-RES-0002); computations that would narrow it: THY-REQ-0008 |

## Compute

Session 1: seven small Modal jobs (M-001…M-007), $2.48.  Session 2: M-008…M-011, $4.21.
Session 3: M-012 (X-006b), $1.01, and M-013 (convergence control at the two largest sizes of
X-005; bound $1.99).  Bounds, measured costs, the research owner's ceiling, the stop line
and the workspace limits are in `docs/engineering/COMPUTE_LEDGER.md`; whether an engineering
app is running is stated at the end of its "Baseline and running total" section.  Nothing
is deployed.

## Synchronisation log

See `docs/collaboration/UPSTREAM_SYNC.md` (both other branches).
