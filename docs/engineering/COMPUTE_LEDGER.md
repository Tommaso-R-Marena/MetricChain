# Compute ledger (Computational Research Division)

Every remote job is entered here **before** launch (purpose, bound, stopping condition) and
completed **after** it finishes (measured usage).  Local runs of more than a few CPU-minutes
are listed too, because they are part of what a result cost.

## Authorisation and limits — what is and is not verified

| item | status |
|---|---|
| Modal workspace | the research owner's workspace (name not recorded in this public repository), environment `main` — the active profile was verified with `modal profile current` (2026-11-25) |
| Remote CPU and GPU execution | verified by the research owner before this session (CPU test and a T4 allocation); not repeated |
| Allocation stated by the research owner | up to **$2,000** on Modal for this programme, shared with nothing else *by intent* — but see the next two rows |
| The workspace is shared with other projects | **yes**: `modal billing report --for "this month"` shows $32.72 of usage on 2026-11-20 by two apps of other projects, and three deployed apps of other projects exist (0 tasks).  None of this belongs to MetricChain; none of it is touched, and their names are not recorded here |
| Workspace budget ("usage limit") and spend limit | **not verifiable from the CLI.**  They are dashboard settings (Usage & Billing page; owners and managers only); `modal workspace settings list` shows only `default-environment` and `image-builder-version`.  The remaining credit balance is not visible either |
| Deadline for expensive work | 2026-11-30 15:00 US Eastern (research owner's cutoff); credits stated to expire 2026-11-30 19:00 Eastern.  Not independently verifiable |

**Policy until the research owner confirms a workspace usage limit:** only jobs whose
*worst-case* cost (every container running to its timeout) is below **$10**, with explicit
timeouts, a container cap and no retries; cumulative engineering spend below **$50**.  Larger
workloads are prepared, costed and deferred.

## Rates (from `modal billing rates`, 2026-11-25)

| resource | price |
|---|---|
| CPU | $0.0473 per physical core-hour |
| memory | $0.0080 per GiB-hour |
| GPU T4 / L4 / A10G / L40S / A100-40 / A100-80 / H100 | $0.59 / $0.80 / $1.10 / $1.95 / $2.10 / $2.50 / $3.95 per hour |

Billing is on the larger of request and actual usage.

## Baseline and running total

Workspace usage this month before any engineering job: **$32.72** (all on 2026-11-20, other
projects; covered by credits).  Engineering usage is read from `modal billing report`,
restricted to apps named `metricchain-eng-*`, per app run.

**Engineering total at the end of session 1 (2026-11-25 05:57 UTC): $2.48** for seven app runs (M-001…M-007; per-run figures below, from `modal billing report`).  **No engineering app is running**: `modal app list` shows all seven stopped with 0 tasks.  Workspace total this month: $35.20 including the $32.72 of other projects.

## Remote jobs

| id | date (UTC) | app / command | purpose | resources requested | worst-case bound | stopping condition | measured | status |
|---|---|---|---|---|---|---|---|---|
| M-001 | 2026-11-25 | `metricchain-eng-chain-enum`: `modal run modal_jobs/chain_enum_app.py --nmin 14 --nmax 14 --splits 8 --k 4` | smoke test of the image (C compiler, enumerator) and of the split/merge logic: the merged table must be byte-identical in content to the local run at n = 14 | 8 containers × 1 core × 512 MiB, timeout 1800 s | 8 × 0.5 h × ($0.0473 + $0.004) = **$0.21** | one pass | **$0.0002**; 3.3 s wall; merged table equal to the local one (641 classes) | done |
| M-002 | 2026-11-25 | same app: `--nmin 21 --nmax 24 --splits 64 --k 8` | THY-REQ-0002 question 1 and 3(a): class tables and trans/gauche pattern bitmaps of the diamond-lattice chain for n = 21…24 (local single-core estimates: 13 min, 38 min, 1.8 h, 5.3 h) | ≤ 64 containers × 1 core × 512 MiB, timeout 1800 s per piece, no retries | 4 lengths × 64 × 0.5 h × $0.0513 = **$6.57**; expected ≈ 12 core-hours ≈ **$0.65** | one pass; a piece that reaches its timeout fails the run (the split is then refined, not retried blindly) | **$0.26**; 11 061 core-seconds in total (296 + 877 + 2 561 + 7 328), 4 min 23 s wall for the four lengths; one transient client heartbeat warning, no failed piece | done |
| M-003 | 2026-11-25 | `metricchain-eng-harness`: `modal run modal_jobs/harness_app.py --seeds 101,202,303` | THY-REQ-0005 item 2: the theory division's full falsification harness under three seeds other than its default, on a third platform (Modal container; library versions pinned to the local ones) | 3 containers × 2 cores × 4 GiB, timeout 3 h, no retries | 3 × 3 h × (2 × $0.0473 + 4 × $0.008) = **$1.14** | one pass per seed | **$0.024**; 188 s, 218 s, 195 s per seed | done |
| M-004 | 2026-11-25 | `metricchain-eng-chain-cover`: `modal run modal_jobs/chain_cover_app.py --nmin 1 --nmax 24` | THY-REQ-0002 questions 1 and 2: exact covering numbers (two solvers) and entropy brackets for n = 1…24; moved off the local machine because the Lean build was competing for its 8 threads | ≤ 24 containers × 4 cores × 8 GiB, timeout 1 h, no retries | 24 × 1 h × (4 × $0.0473 + 8 × $0.008) = **$6.08**; expected ≈ $0.30 | one pass | **$0.72**; rows n = 1…18 completed in ≤ 286 s each; the six containers for n = 19…24 were stopped by hand after 22 min (`modal app stop`) — see `DEAD_ENDS.md` ED-3 | stopped; superseded by M-005 |
| M-005 | 2026-11-25 | `metricchain-eng-chain-cover`: `modal run modal_jobs/chain_cover_app.py --nmin 19 --nmax 24` (after adding time limits and certified brackets) | THY-REQ-0002 question 1 for n = 19…24: M-004 was stopped by hand after 22 min because the covers at these sizes do not reduce to small instances and the integer programmes had no time limit | 6 containers × 4 cores × 8 GiB, timeout 1.5 h, no retries; 300 s per solver and setting | 6 × 1.5 h × $0.253 = **$2.28** | one pass; unproved cells are reported as brackets | **$0.65**; 1 090–1 732 s per chain length; exit 0 | done |
| M-006 | 2026-11-25 | `metricchain-eng-chain-cover`: `modal run modal_jobs/chain_cover_app.py::generic --nmin 5 --nmax 13` | THY-REQ-0002 question 1 for the generic (off-lattice) chain: enumeration inside the container, covers bracketed with 300 s per integer programme; published values exist for n ≤ 10, n = 11…13 are new | ≤ 6 containers × 8 cores × 24 GiB, timeout 2 h, no retries | 6 × 2 h × (8 × $0.0473 + 24 × $0.008) = **$6.85**; expected ≈ $1–2 (small sizes finish in seconds) | one pass; unproved cells are brackets | **$0.53**; rows n = 5…9 returned within 14 s; stopped by hand after 13 min (`modal app stop`) because the larger sizes would have used their full time limits | stopped; superseded by M-007 |
| M-007 | 2026-11-25 | `metricchain-eng-chain-cover`: `modal run modal_jobs/chain_cover_app.py::generic --nmin 10 --nmax 12 --cover-time-limit 90` | as M-006 for n = 10…12 only, with 90 s per integer programme: at 300 s the three sizes would have needed more than an hour and n = 13 would probably have hit its timeout, so M-006 was stopped by hand after 13 min | 3 containers × 8 cores × 24 GiB, timeout 2 h, no retries | 3 × 2 h × $0.57 = **$3.42**; expected ≈ $1 | one pass; unproved cells are brackets | **$0.30**; 389 s, 565 s, 701 s for n = 10, 11, 12; exit 0 | done |

## Local runs worth recording

| date (UTC) | command | wall time | note |
|---|---|---|---|
| 2026-11-25 | `lake exe cache get` (Mathlib v4.31.0 cache) | 2 min 15 s | 7.3 GB under `.lake/` |
| 2026-11-25 | `lake build` at `d81eb8a`, 2 then 4 Lake threads | see ENG-RES-0005 | peak resident set per `lean` process ≈ 4.1 GB (mostly shared, memory-mapped Mathlib) |
| 2026-11-25 | `build/dia_enum -n 19`, `-n 20` | 83 s, 261 s | single core, with pattern bitmaps |
