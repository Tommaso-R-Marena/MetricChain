# Compute ledger (Computational Research Division)

Every remote job is entered here **before** launch (purpose, bound, stopping condition) and
completed **after** it finishes (measured usage).  Local runs of more than a few CPU-minutes
are listed too, because they are part of what a result cost.

## Authorisation and limits — what is and is not verified

| item | status |
|---|---|
| Modal workspace | the workspace designated by the research owner (name not recorded in this public repository), environment `main` — the active profile was verified with `modal profile current` (2026-11-25) |
| Remote CPU and GPU execution | verified by the research owner before this session (CPU test and a T4 allocation); not repeated |
| Allocation stated by the research owner | up to **$2,000** on Modal for this programme, shared with nothing else *by intent* — but see the next two rows |
| The workspace is shared with other projects | **yes**: `modal billing report --for "this month"` shows $32.72 of usage on 2026-11-20 by two apps of other projects, and three deployed apps of other projects exist (0 tasks).  None of this belongs to MetricChain; none of it is touched, and their names are not recorded here |
| Workspace budget ("usage limit") and spend limit | Not visible from the CLI (dashboard settings; `modal workspace settings list` shows only `default-environment` and `image-builder-version`).  **Stated by the research owner on 2026-11-25 (session 2), from the billing page:** the programme's Modal allocation is prepaid credit, of which about **$1,995 remained** at that time; a workspace usage limit exists but is *higher* than the credit balance, so the platform would not stop work at the credit line.  **Stated by the research owner on 2026-11-26 (session 3):** that limit cannot be changed for this programme; the credit line is to be respected as it stands ($1,990.63 left of $2,030.00 at that time), and whether engineering's own stop line should be lower or higher is left to this division.  The Modal CLI offers no command that changes a budget (`modal billing` has `summary`, `report`, `rates` only), and none was attempted |
| Deadline for expensive work | 2026-11-30 15:00 US Eastern (research owner's cutoff); credits stated to expire 2026-11-30 19:00 Eastern.  Not independently verifiable |
| Workspace resource limits | **Shown by the research owner on 2026-11-25 (session 2), from the workspace's resource-limits page:** 100 concurrent containers and 10 concurrent GPUs workspace-wide, 5 container creations per second.  Job M-008 was launched with a cap of 100 containers before this was known and held the whole workspace limit for about 20 minutes; the owner pointed it out |

**Instruction of the research owner (2026-11-25, session 2):** the remaining credit is a hard
ceiling — it must not be exceeded — and there is no obligation to use it: compute is to be
used where a computation needs it, not for its own sake.

**Authorisation of the research owner (2026-11-26, session 4; directive D-5 in
`DIRECTIVES.md`), which replaces the stop line of sessions 2–3:** up to **$1,750 of additional
Modal expenditure across the whole research programme** (all six divisions; this division
coordinates), counted from the owner's snapshot (credits granted $2,030.00, consumed $41.41),
with at least **$200 of credit preserved**, never beyond the remaining credit, **no paid
charge**, the worst case of active, queued and proposed jobs counted, and no change of any
billing setting.  The budget "is not a spending quota".

**Policy that follows (engineering's rules under that authorisation; they replace the rules
of sessions 2–3).**  No platform limit enforces any of this, so it is enforced here:

1. **Bounded jobs.**  Every job has a container cap, a per-task timeout and no retries, so
   that its worst-case cost (every task running to its timeout) is a number, computed and
   entered below before launch.
2. **The launch test**, made immediately before every launch with `modal billing summary`
   (which prints the month's metered cost, the credits applied and the billed cost) and
   `modal billing report --for "this month"`:
   * (a) **billed cost is $0.00** — if it is not, nothing is launched, everything of ours
     is stopped, and the research owner is told;
   * (b) credits consumed by the whole workspace (all projects) **+ the worst cases of
     every job of ours that is running or queued + the worst case of this job ≤ $1,791.41**
     (the snapshot's $41.41 plus $1,750);
   * (c) the same sum **≤ $1,830.00** (credits granted minus the $200 reserve) — implied by
     (b) today; kept because (b) moves if the owner changes the authorisation;
   * (d) the applicable workspace limits (100 containers, 10 GPUs) are respected by rule 5.
   Usage by other projects of the workspace counts against (b) and (c): the authorisation
   says "assuming no other spending", and this division cannot see such spending coming.
3. **Staged scaling.**  A job whose worst case exceeds **$60** is launched only as a later
   stage of a campaign whose earlier stage (at most $60) has finished and whose measured
   cost was within a factor two of its prediction; no single job has a worst case above
   **$250** (larger campaigns are split and re-tested between parts).  The provisional
   allocations of D-5 — $600 existing MetricChain benchmarking, $350 ensemble, $350
   geometry, $250 complexity, $200 replication and final verification — are tracked in the
   table "Allocations" below and are planning guidance, not entitlements.
4. Nothing is deployed; apps are ephemeral (`modal run`) and are checked to be stopped
   (`modal app list --json`, keys `state`, `description`, `tasks`; `modal container list
   --json`) after every job and at the end of every session.
5. **At most 50 containers in total** are requested by engineering at any time (half of the
   workspace limit of 100) unless a ledger entry says why more are needed, jobs are run
   one after another, and no GPU is used without a ledger entry that says why.
6. **Restarts by the platform (observed 2026-11-26).**  A container can be pre-empted and
   its task started again; `retries=0` does not prevent that.  Of the 20 long tasks of
   M-016 and M-022, five were restarted (their containers carry start times 45 minutes to
   three hours after the launch).  So "every task runs to its timeout" bounds one
   *attempt*, not one task: a worst case can be exceeded by a restarted task, by at most
   one more attempt each time.  Consequences: the launch test keeps its margin (the
   ceiling is two orders of magnitude above what is committed); after a long job the
   measured cost is compared with the bound, and a job whose restarts would carry it
   past its bound is stopped by hand (`modal app stop`); results are written by the task
   itself, so a restarted task costs time, not correctness.
   **It happened** (found at checkpoint 6): job M-022 cost **$2.48 against a "worst case"
   of $2.28** entered before launch — 12 tasks of a three-hour tier used 39 task-hours.
   The excess is 20 cents and nothing was near any limit, but the number entered before
   the launch was not a bound.  From checkpoint 6 on: **the worst case of a task whose
   timeout is an hour or more is entered as two attempts** (twice timeout × rate), and
   the ledger says so in the row; for shorter tasks one attempt.  This is still not a
   proof of a bound — a task can be restarted twice — which is why the launch test
   compares against the ceiling with the factor in.
7. **What cannot be verified from here.**  The terms of the Modal credit (in particular its
   expiry date) are not visible to the CLI; the owner has said not to assume they coincide
   with the Claude credits'.  Operational substitute: test (a) after every job — the
   exposure to an unnoticed lapse of the credit is the worst case of one job, which is why
   rule 3 keeps first stages small.  Hard stop for all computation: **2026-11-30 15:00 US
   Eastern**.

### Allocations (D-5; planning guidance; updated after every job)

| purpose | provisional | committed (worst cases of running or queued jobs) | spent |
|---|---|---|---|
| existing MetricChain certificates and algorithms | $600 | **$0** — nothing of ours is running or queued (2026-11-27 18:37 UTC; the last worst case entered here was $54.4 at 2026-11-26 23:51 UTC) | **$21.58** of credit consumed by the workspace since the owner's snapshot ($62.99 − $41.41; `modal billing summary`, 2026-11-27 18:37 UTC), all of it by engineering's app runs (by `modal billing report`: $15.84 on 2026-11-26 and $7.74 on 2026-11-27, less the $2.03 of session 3 that preceded the snapshot; per job: "Final reconciliation" and the table "Remote jobs").  Billed cost $0.00 |
| ensemble identifiability | $350 | $0 | $0 |
| geometric inference | $350 | $0 | $0 |
| complexity investigations, counterexample searches | $250 | $0 | $0 |
| independent replication, final verification | $200 | $0 | $0 |
| software of the structural-biology division; evaluations designed by the frontier division (D-6, D-7: no allocation of their own; from whichever line is ready) | — | $0 | $0 (the first review, ENG-RES-0018, ran locally) |
| **total authorised** | **$1,750** | **$0** (2026-11-27 18:37 UTC: nothing is running or queued on any line) | **$21.58** — credits consumed by the workspace since the owner's snapshot ($62.99 − $41.41 at 2026-11-27 18:37 UTC), all projects of the workspace included; the billing report attributes all of it to engineering's app runs ($21.55 after the snapshot; the three cents are the rounding of the snapshot).  By the billing report no app other than engineering's has run in the workspace since 2026-11-20.  (Until checkpoint 6 this cell still showed the figure of 15:40 UTC, $0.07, while the first row had moved: the frontier and structural-biology divisions both noticed.  The two cells are updated together.) |

Spend before the authorisation (jobs M-001 … M-014, sessions 1–3): $8.73, inside the
snapshot's $41.41.

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

**Engineering total at the end of session 1 (2026-11-25 05:57 UTC): $2.48** for seven app runs (M-001…M-007; per-run figures below, from `modal billing report`).

**Session 2, at checkpoint 3 (2026-11-25, about 18:00 UTC):** M-008 $2.07, M-009 $1.23, M-010 $0.07, M-011 $0.84, two smoke tests $0.001 — **$4.21**, against worst-case bounds of $25.88 + $9.95 + $0.44 + $32.35 = $68.62 entered before launch.  **Engineering total: $6.70.**  Workspace usage this month, all projects: $39.42, against a credit of about $1,995 and the stop line of $1,500 set above.  **No engineering app is running** (`modal app list`: all stopped, 0 tasks); nothing is deployed.

**Session 3 (2026-11-26):** before the first launch, workspace usage this month, all projects: **$39.42** (`modal billing report --for "this month"`, 2026-11-26 03:05 UTC; engineering $6.70 of it); no engineering app running, three deployed apps of other projects untouched.  Figures after each job: in the table and in the paragraph that closes this section at the end of the session.

**Session 3, at checkpoint 4 (2026-11-26 04:10 UTC):** M-012 $1.01 and three smoke tests $0.002 — against a worst-case bound of $17.07 entered before launch.  **Engineering total: $7.71**; workspace usage this month, all projects: $40.43, against a credit of about $1,990 and the stop line of $1,500.  Job M-013 was running at the time of that commit.

**Session 3, at checkpoint 5 (2026-11-26 05:40 UTC):** M-013 $0.55 and M-014 $0.48, against worst-case bounds of $1.99 and $19.91 entered before launch.  Session 3 in all: $2.03 (M-012 $1.01, M-013 $0.55, M-014 $0.48, smoke tests $0.001), against a sum of worst cases of $38.97.  **Engineering total: $8.73**; workspace usage this month, all projects: $41.46, against a credit of about $1,990 and the stop line of $1,500.  **No engineering app is running** (`modal app list --json`, 2026-11-26 05:51 UTC: the two engineering apps listed are in state `stopped` with 0 tasks; `modal container list`: 0 containers in the workspace; three deployed apps of other projects exist as before and were not touched); nothing of ours is deployed.  *Note:* the same check made between jobs during this session read the listing with the wrong key names and could not have failed; between the first and this last check the statement rested on each job's own completion line and on the billing report (`RESEARCH_LOG.md`, §3.4).

**Session 4, at checkpoint 6 (2026-11-26 23:51 UTC):** jobs M-015 … M-025.  Credits consumed by the workspace: **$55.39** (snapshot of the authorisation: $41.41), billed cost **$0.00**; engineering app runs of this session by the billing report: M-016 with M-017 $5.55 (open), M-018 $1.06, M-019 $0.25, M-020 first tier $0.54, M-020 second tier with M-021 $2.54 (open), M-022 $2.48, M-023 $0.14, M-024 $0.25, M-025 $0.25, smoke tests $0.01 — **$13.07**, against worst cases entered of more than $110.  One entry was exceeded: M-022, $2.48 against $2.28 (restarted tasks; policy rule 6, amended).  **Still running: two app runs of ours, 17 containers** (M-016: six tasks of the twelve-hour tier, launched 16:20 UTC; M-020/M-021: eleven tasks, launched 21:35 UTC); they end by themselves at their timeouts — at the latest 04:20 UTC and 09:35 UTC on 2026-11-27 for one attempt, later if the platform restarts them — and `python modal_jobs/bench_collect.py` collects them at any time.  Nothing is deployed.  The research owner's dashboard screenshot of about 22:44 UTC (four live `metricchain-eng-bench` apps, 47 containers, $52.88 of credits used, $0.00 current spend) agrees with this ledger.

**Consolidation (2026-11-27 01:16 UTC; the research owner's directive D-8) — reconciliation.**
Credits consumed by the workspace, all projects: **$56.99**; billed cost **$0.00**
(`modal billing summary`).  Since the snapshot of the authorisation ($41.41): **$15.58 of the
$1,750 authorised**.  Engineering app runs by `modal billing report` (2026-11-26 and 2026-11-27
so far): M-012 $1.01, M-013 $0.55, M-014 $0.48 (session 3; they agree with the entries above);
session 4: M-016 with M-017 **$6.42 (open)**, M-020 second tier with M-021 **$3.97 (open)**,
M-018 $1.06, M-019 $0.25, M-020 first tier $0.54, M-022 $2.48, M-023 $0.14, M-024 $0.25,
M-025 $0.25, smoke tests $0.01 — **$15.37**.  **Engineering total over all sessions: $24.10**
($8.73 to checkpoint 5 and $15.37 since), against worst cases entered of more than $170.
One entry was exceeded (M-022, $2.48 against $2.28).  No job was launched after the directive.

**Jobs left running, unsupervised, under D-8 §5** ("already authorized, bounded, useful") —
*closed on 2026-11-27; see "Final reconciliation" below; this block is kept as it was written.*
Two detached app runs of `metricchain-eng-bench`, 16 tasks, no retries; an app run stops by
itself when its last task ends or reaches its timeout, and nothing is deployed.

| job | tasks still running at 01:16 UTC | launched (UTC) | tier: timeout, memory | ends, one attempt | worst case still to be spent |
|---|---|---|---|---|---|
| M-016 | 6: the certified bound to six levels at `n = 32 000, 64 000, 128 000`, `u = 1`, two families | 2026-11-26 16:20 | 12 h, 4 GiB | by 04:20 on 2026-11-27 | $1.46 if they run to the timeout; $7.17 if each is restarted once by the platform at the last minute |
| M-021 | 4: `n = 64 000` at `u = ½` and `u = 2`, two families | 2026-11-26 21:35 | 12 h, 4 GiB | by 09:35 | $2.64; $6.45 with one restart each |
| M-021 | 3: `n = 16 000` (`u = ½` family "wide"; `u = 2` both families) | 21:35 | 6 h, 4 GiB | by 03:35 | $0.55; $1.98 |
| M-021 | 3: `n = 1000` (wide) and `n = 4000` (both) at `u = 2` | 21:35, started later behind M-020's tasks in the same tier | 3 h, 2 GiB | by about 04:00 | $0.57; $1.14 |

Worst case still to be spent: **$5.2** without restarts, **$16.7** with one restart of every
task (the planning rule since M-022); cumulative workspace credits would then be at most
$73.7, against the stop line of $1,500 and the ceiling of $1,791.41.  A restart gives a task a
fresh timeout, so the latest end with one restart each is 21:35 UTC on 2026-11-27 — before the
hard stop for computation (2026-11-30 20:00 UTC).

*To collect* (safe at any time, repeatable; results are in a `modal.Dict` whose entries expire
seven days after their last access, so collect before 2026-12-03):

    source <venv>; python modal_jobs/bench_collect.py --driver nested_bench --job certified1+certified2
    python experiments/eng/twolevel/make_tables_x011.py        # prints the tables; blocks with the suffixes _large and _late hold the new rows
    modal app list ; modal billing summary                     # nothing of ours running; Billed Cost $0.00

*To stop them early, or if anything is still running after 22:00 UTC on 2026-11-27:*
`modal app stop <app id>` for the two `metricchain-eng-bench` runs shown by `modal app list`
(tasks that have stored their result lose nothing).  At 01:02 UTC the collection stood at:
M-016 12 of 18 cells, M-020 288 of 288 (**complete**), M-021 6 of 16.

**Final reconciliation (2026-11-27 18:37 UTC; the research owner's directive D-10) — both jobs
closed, nothing running, nothing committed.**

*State.*  `modal app list --json`: the one engineering app run still listed is `stopped` with 0
tasks; `modal container list --json`: 0 containers in the workspace.  Nothing of ours is deployed.
What engineering leaves in the workspace: one `modal.Dict` (the result store of the benchmark
app; its entries expire seven days after their last access, which was 2026-11-27 18:32 UTC; no
charge is known for it).  Three deployed apps and five volumes of other projects exist as before
and were not touched.

*How the two jobs ended.*  M-021's app run ended by itself between 09:11 and 09:21 UTC on
2026-11-27 (16 of 16 cells stored).  M-016's app run still had one task at 18:20 UTC — the cell
`u = 1`, `n = 32 000`, family "wide" — in a container started at 13:01 UTC, 20 h 41 min after the
launch: a restart by the platform (rule 6), and not the task's first.  Its search stops itself
after 42 300 s, so that attempt would have returned at about 00:46 UTC on 2026-11-28, after the
cutoff of 22:00 UTC written above; D-10 forbids extending deadlines and restarting.  **The run
was stopped with `modal app stop` on 2026-11-27 at 18:24 UTC; that cell has no row** (17 of 18
cells stored).  The local watcher saw no open run at 18:32 UTC, collected once more (no new
row) and ended.  The planning rule of 01:16 UTC — one restart per task, latest end 21:35 UTC —
was exceeded by this one task, as rule 6 says it can be.

*Money.*  Credits consumed by the workspace, all projects: **$62.99**; billed cost **$0.00**
(`modal billing summary`: metered cost $66.03 = ephemeral apps $62.99 + volumes $2.99 + network
egress $0.05; credits −$62.99; egress allowance −$0.05).  Since the snapshot of the
authorisation ($41.41): **$21.58 of the $1,750 authorised**; by the owner's figure of $2,030.00
of credits granted, about **$1,967 are left** (reserve to be preserved: $200).  Since the
reconciliation of 01:16 UTC ($56.99): **$6.00**, against the worst cases stated there of $5.2
without restarts and $16.7 with one restart of every task.  (Read at 18:37 UTC and again at
18:45 UTC with the same figures, 21 minutes after the last task was stopped; if the platform
posts usage later than that, a later reading can be a few cents higher.)

By app run (`modal billing report` for 2026-11-26 and 2026-11-27): M-016 with M-017 **$9.35**
($5.82 + $3.52); the second tier of M-020 with M-021 **$7.23** ($3.01 + $4.22).  **Engineering
total over all sessions: $30.28** ($6.70 on 2026-11-25, $15.84 on 2026-11-26, $7.74 on
2026-11-27; it agrees to a cent with $24.10 at 01:16 UTC plus $2.93 and $3.26 for the two runs
since), against worst cases entered of more than $170.  Other projects of the workspace: $32.72,
unchanged since 2026-11-20.

*Entries exceeded.*  **M-016: about $8.97 against its entry of $8.56** (the app run's $9.35 less
M-017's $0.38, which was estimated from task times) — the second entry exceeded, after M-022,
and for the same reason: the entry counts one attempt per task.  By the task times stored in
the rows, the attempts that returned a row account for $6.28; the remaining $2.7 or so is
attempts that the platform interrupted, among them every attempt of the cell that has no row.
M-021: the attempts that returned account for $5.84 of the $7.23 of its app run (which it
shares with 144 tasks of M-020); within its entry of $7.23 unless interrupted attempts added
more than $1.39, which the billing report cannot show.

*The line "Volumes".*  $2.99 of metered cost, rising by about $0.03 an hour (it was $2.62 at
05:32 UTC), belongs to the five volumes of other projects (created in October and on
2026-11-19); engineering has never created a volume.  At this reading it is neither charged to
the credits nor billed.  It is recorded here because the authorisation counts all usage of the
shared workspace.

*Results and what they decide:* `docs/engineering/benchmarks/X-011_ADDENDUM.md`.

## Phase II (research owner's directive D-11, from 2026-11-28)

Authorisation: "An initial Modal expenditure ceiling of $25 is authorized for small, bounded pilots that
directly support the objectives of this directive, subject to the previously established resource
restrictions."  "Use local computation first."  "Do not launch large-scale benchmark campaigns."  "Do
not restart the previously missing M-016 cell merely for completeness."  A larger computation needs a
written proposal to the research owner (objective, protocol, competing methods, success and failure
criteria, estimated cost, worst-case committed cost, expected value) and an explicit answer.

| | |
|---|---|
| ceiling for this phase | $25 |
| committed (worst cases of running or queued jobs) | $0 |
| spent | $0 — **no Modal job was launched and no Modal command was run in Phase II** (final state, 2026-11-28) |
| running or deployed by this division | nothing |
| requests from the other Phase II divisions | one: HIE-REQ-0001 (adaptive hierarchy), which asked for local CPU only — accepted for Q1 and Q2, declined for Q3, answered in ENG-RES-0020; no Modal cost.  The theory instance sent no request |
| proposals for larger computation sent to the research owner | none: nothing in this phase needed more than the local machine |

The workspace's Modal figures are therefore those of the final reconciliation of Phase I above (credits
consumed, billed cost $0.00); they were not queried again in Phase II.

**Directive D-12 (2026-11-28, about 05:30 UTC).**  "Your existing Modal pilot ceiling remains $25 in total,
not $25 per division.  Any increase requires my explicit authorization."  "No substantial new
computational campaign is authorized by this message."  The table above therefore covers all four Phase
II branches.  State after the first cycle under D-12: ceiling $25, committed $0, spent $0, nothing
running or deployed, no Modal command run.  Requests received from the certified-MBAR division: one,
MBAR-REQ-0001 — about 120 GPU-hours of molecular dynamics, $80–$130 expected, $200 worst case, with an
optional pipeline pilot under $8.  Decision (ENG-RES-0021): not launched; three to eight times the ceiling
and a new molecular-dynamics campaign, hence the research owner's decision, and in our assessment
premature while local controls with correlated samplers and the replay of existing data have not been
tried; the pilot deferred because by the requester's own statement it cannot answer the question.  No
proposal for a larger computation has been sent to the owner by this division.  (How to send a request,
and the seven points by which it is judged: `docs/collaboration/README.md`, "Requests for computation in
Phase II").  The experiments of this cycle ran on the local machine (last row below).

Local computation of this phase (8 threads, at most four to five processes at a time):

| what | wall time | where |
|---|---|---|
| validation campaign under the protocol (grid, sensitivity, structure, recomputed baseline) | 2.2 h (about 6.5 core-hours of worker time in the grid) | `experiments/eng/certinf/REPORT.md` §7 |
| supplementary experiment S1 | about 5 minutes on three processes | `experiments/eng/phase2_tilt/` |
| supplementary experiment S2, the sequential bound, the coordinator's checks | minutes | `experiments/eng/phase2_nonproduct/`, `phase2_seq/`, `phase2_coord_checks/` |
| the referee's checks | not timed as a whole; scripts of seconds to minutes each | `experiments/eng/phase2_review/` |
| verification of the structural-biology certificates and of the memoised kernel | 1.4 s to 196 s per certificate in the kernel, peak memory 4.9 GB | `experiments/eng/phase2_gaps/REPORT.md` |
| replication for HIE-REQ-0001 | about 13 minutes of script time, two processes | `experiments/eng/phase2_hie_req/REPORT.md` |
| after D-12: Theorem M1 on enumerable models (16 cells, two runs, the second executed twice because of a defect of ours), the shared energy error, the tail-event diagnostic | 22, 19 and 13 minutes on seven processes for the three executions; about two minutes for the other two scripts | `experiments/eng/phase2_mbar/`; `docs/engineering/phase2/MBAR_INTEGRATION.md` §8 |

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

| M-008 | 2026-11-25 | `metricchain-eng-twolevel`: `modal run modal_jobs/twolevel_app.py --job smoke`, then `--job cost` | X-005 (THY-REQ-0001 Part B, target Algorithm 2L⁺): for every `(u, n, φ)` of the theory division's cost table — `u ∈ {½, 1, 2}`, 13 sizes `n = 250 … 128 000`, 12 outer fractions — the largest number of evaluations over radial instances found by differential evolution (monotone and general profiles, both inner oracles), with the extremes of every claim of Theorem 11.56 over all instances evaluated.  Remote because it is 30 core-hours of independent single-core tasks and the local machine has 8 threads | ≤ 100 containers × 1 core × 1 GiB (**the whole workspace limit**, see "Workspace resource limits" above; later jobs: 50), timeout 3600 s per task, no retries; 468 tasks, the longest expected to take 27 min (a Modal core runs this code about half as fast as the development machine: smoke test) | 468 × 1 h × ($0.0473 + $0.008) = **$25.88**; expected 51 core-hours ≈ **$2.82** | one pass; results appended per task to `experiments/eng/twolevel/results/x005_cost.jsonl`, so a stopped run loses only unfinished tasks; a task that reaches its timeout fails and is reported, not retried | **$2.07** (and $0.0006 for the smoke test); 468 tasks, 34.8 core-hours of task time, longest task 2 241 s, wall time 15:40–16:17 UTC; 5 144 256 instances evaluated, no claim violated; smoke-test results bit-identical to local ones.  Ran at commit `f85d6bd` (before the tie rule of `5b4c7ad`); every stored maximiser re-evaluated with the final code (`recheck.py`) | done |
| M-009 | 2026-11-25 | same app: `--job claims` | X-005: searches that maximise the slack of one claim of Theorem 11.56 at a time (cost against the cap `C_max`, the count (v), the bound on `M_j^neg`, the sample bound, claim (vi)) on 36 cells | ≤ 50 containers × 1 core × 1 GiB, timeout 3600 s, no retries; 180 tasks, longest expected 26 min | 180 × $0.0553 = **$9.95**; expected 30 core-hours ≈ **$1.66** | as M-008 (`x005_claims.jsonl`) | **$1.23**; 180 tasks, 20.7 core-hours of task time, longest task 2 147 s, wall time 16:18–17:11 UTC; 1 568 160 instances evaluated, no claim violated.  Ran at commit `ce08925` | done |
| M-010 | 2026-11-25 | same app: `--job converge` | X-005: is the search budget the limitation?  Five times the budget and two other seeds on four cells | 8 containers × 1 core × 1 GiB, timeout 3600 s, no retries | 8 × $0.0553 = **$0.44**; expected ≈ **$0.17** | as M-008 (`x005_converge.jsonl`) | **$0.07**; 8 tasks, 1.1 core-hours of task time, longest task 971 s, wall time 17:12–17:28 UTC; 383 424 instances evaluated, no claim violated; the worst case found changes by at most `0.0002·na`.  Ran at commit `ce08925` | done |
| M-011 | 2026-11-25 | same app: `modal run modal_jobs/twolevel_app.py::sampled --runs-full 5000 --runs-reduced 1000` | X-006 (THY-REQ-0001 Part A, outer loop): literal runs of Algorithm 2L⁺ with a randomly drawn outer sample and oracle brackets on 13 radial landscapes × 3 sizes × 3 inner behaviours, with the theorem's `K` (5 000 runs per case) and with `K` scaled by ¼, 1/16, 1/64, 1/256 (1 000 runs per case): does a claim fail on the good event, and where do the events of the proof and the validity of the bracket start to fail?  Remote because it is about 25 core-hours of independent tasks | ≤ 50 containers × 1 core × 1 GiB, timeout 3600 s per case, no retries; 585 cases, the longest expected to take 8 min | 585 × $0.0553 = **$32.35**; expected 1 053 000 runs × 0.09 s ≈ 26 core-hours ≈ **$1.46** | one pass; results appended per case to `experiments/eng/twolevel/results/x006_sampled.jsonl` | **$0.84** (and $0.0004 for a smoke test of 3 cases, whose results equal the local ones); 585 cases, 1 053 000 runs, 14.0 core-hours of task time, longest case 456 s; no run failed in any way with the theorem's `K`.  Ran at commit `a9ef1b4` | done |
| M-012 | 2026-11-26 | same app: `modal run modal_jobs/twolevel_app.py::sampled --job M-012` (defaults: `--runs-full 5000 --runs-reduced 1000 --runs-invalid 500 --sampler exact --tag x006b`), after a smoke test `--limit 8` | **X-006b: the literal runs of X-006 repeated with an exact sampler.**  The Scientific Discovery Division reported (SCI-REV-0007 §4, request R6-E3) that numpy's binomial sampler is biased for counts drawn from 10¹⁷ points and more; measured here from 10¹⁵ on (`experiments/eng/twolevel/binomial_bias.py`), and job M-011 drew from blocks of up to 5·10¹⁷ points in two of its three sizes.  The 585 cases of M-011 are repeated with `sampling.binomial_exact`, plus 156 cases with an invalid inner behaviour that sends every refined point to the last rung (their request R6-E2: the cost bound in every run).  No change of the experiment otherwise (same landscapes, sizes, seeds) | ≤ 50 containers × 1 core × 1 GiB, timeout 1500 s per task, no retries; 741 tasks | 741 × 1500 s × $0.0553/h = **$17.07** (every task to its timeout); expected ≈ 24 core-hours = **$1.30** (M-011 measured 14.0 core-hours; the exact sampler costs 3–65 % more per run; the 156 added cases about 5 core-hours).  Usage before launch $39.42 + $17.07 = $56.49 ≤ $1,500 | all cases stored (file is appended per task, a rerun resumes); a task that reaches its timeout is not retried and is reported | **16.9 core-hours** inside the tasks (sum of task times; longest task 569 s, none near its limit); billed **$1.01** for the job and $0.0005 for the smoke test (`modal billing report`, 2026-11-26); 24 minutes of wall time (03:25–03:49 UTC), at most 50 containers | **completed**: 741 of 741 cases stored, each row with commit `26029c9` and job id; app stopped |
| M-013 | 2026-11-26 | same app: `modal run modal_jobs/twolevel_app.py::main --job converge2 --ledger M-013` | **X-005, convergence control at the two largest sizes** (requested by the Scientific Discovery Division, SCI-REV-0008 R7-ENG-4: these sizes carry the statement "no persistent margin" and had the smallest search budgets in M-008).  `n ∈ {64 000, 128 000}`, `u ∈ {½, 1, 2}`, outer fraction 0.50, seeds 2 and 3, three times the budgets of M-008 (7 500 + 3 750 and 4 500 + 2 250 evaluations per search pair) | ≤ 12 containers × 1 core × 1 GiB, timeout 10 800 s per task, no retries; 12 tasks | 12 × 3 h × $0.0553/h = **$1.99**; expected ≈ 10 core-hours = **$0.55** (M-008's task times at these sizes scaled by the budget: longest task about 1.8 h).  Usage before launch $40.43 + $1.99 = $42.42 ≤ $1,500; session sum of worst cases $17.07 + $1.99 = $19.06 | all 12 tasks stored (file appended per task; a rerun resumes); a task that reaches its limit is not retried and is reported | **9.7 core-hours** inside the tasks (longest task 5 432 s of its 10 800 s limit); billed **$0.55** (`modal billing report`, 2026-11-26); 91 minutes of wall time (03:51–05:22 UTC), 12 containers | **completed**: 12 of 12 tasks stored, each row with commit `909751b` and job id; app stopped.  Workspace usage this month after the job: $40.98 (engineering $8.26) |
| M-014 | 2026-11-26 | same app: `modal run modal_jobs/twolevel_app.py::main --job anyplacement --ledger M-014` | **X-005b: can an instance that is not a product cost more?**  (The first objection of SCI-REV-0008 §4.)  The searches of job M-008 for the sizes up to `n = 16 000` — `u ∈ {½, 1, 2}`, 10 sizes, 12 outer fractions, the same budgets and seed — with a different objective: the upper bound on the evaluations of every instance with a given law of fibre averages, whatever the places of its fibres in their trivial brackets (`meanrun.rung_positions`).  The three largest sizes are covered at the stored maximisers only (`nonproduct_bound.py`, local) | ≤ 50 containers × 1 core × 1 GiB, timeout 3600 s per task, no retries; 360 tasks | 360 × 3600 s × $0.0553/h = **$19.91**; expected ≈ 8 core-hours = **$0.45** (the same cells took 7.3 core-hours in M-008, longest task 652 s).  Usage before launch $40.98 + $19.91 = $60.89 ≤ $1,500; session sum of worst cases $17.07 + $1.99 + $19.91 = $38.97 | all 360 cells stored (file appended per task; a rerun resumes); a task that reaches its limit is not retried and is reported | **7.5 core-hours** inside the tasks (longest task 683 s); billed **$0.48** (`modal billing report`, 2026-11-26); 11 minutes of wall time (05:23–05:35 UTC), at most 50 containers | **completed**: 360 of 360 cells stored, each row with commit `14ad5cd` and job id; app stopped.  Workspace usage this month after the job: $41.46 (engineering $8.73) |
| M-015 | 2026-11-26 | `metricchain-eng-bench` (new generic app, `modal_jobs/bench_app.py`): `modal run modal_jobs/bench_app.py::main --driver nested_bench --job smoke --ledger M-015` | smoke test of the new app and image: one certified cell (`n = 1000`, three nested levels) and one instance cell with a small search budget; the results must equal the local ones | 2 containers × 1 core × 1 GiB, timeout 1200 s, no retries | 2 × (1200/3600) h × ($0.0473 + $0.008) = **$0.04** | one pass | **$0.002** (billing report, 2026-11-26 16:25 UTC: three app runs of `metricchain-eng-bench`); attached run: 2 tasks, 3 s and 9 s; then the detached path on three more tiny tasks (`--job smoke2`, worst case $0.15): results reached the store, were collected, the app ended by itself (state `stopped`, 0 containers).  Certified values equal the local ones (`1.1384` at `n = 1000`) | done |
| M-016 | 2026-11-26 | same app: `--job certified1 --ledger M-016` | **X-011a (registry Q-01; BM-1, stage E, first stage): the certified cost bound of nested runs of Algorithm 2L⁺ with servers chosen by certified cost** — `u = 1`; `n ∈ {1000, 1400, 2000, 4000, 8000, 16 000, 32 000, 64 000, 128 000}`; two families of candidate designs ("theory": the candidates of the theory division's `cert3.py`, minimised exhaustively; "wide": both kinds of design at every accuracy, twelve outer fractions, three tolerances); up to five nested levels above base brackets ("six levels"); eighteen outer fractions of the top level.  Hypotheses written before launch: `benchmarks/protocols/BM-1_X-011.md`.  Local timing (one core): `n = 16 000`, family "theory": 3 s, 177 s for two and three nested levels; `n = 4000`: 19 s and 531 s for three and four | 18 containers × 1 core; 10 tasks of 3 h / 2 GiB, 2 of 6 h / 4 GiB, 6 of 12 h / 4 GiB; no retries; every task stops its own search 15 min before its timeout and returns what is finished | 10 × $0.190 + 2 × $0.476 + 6 × $0.952 = **$8.56** | one pass; no extension without a new entry | **$9.35 for the app run it shares with M-017** (billing report for 2026-11-26 and -27); M-017's part was about $0.38, so about **$8.97 for this job — above the entry of $8.56** (tasks restarted by the platform; policy rule 6).  **17 of 18 cells collected**; the cell `n = 32 000`, family "wide" has no row ("Final reconciliation"; `benchmarks/X-011_ADDENDUM.md` §1) | **closed, incomplete by one cell** — launched 2026-11-26 16:20 UTC at commit `55bec29`, detached, together with M-017 in one app run (container caps by tier 8/18/14/4/6, sum 50); the app run was stopped on 2026-11-27 at 18:24 UTC with one restarted task still running |
| M-017 | 2026-11-26 | same app: `--job instances1 --ledger M-017` | **X-011b (registry Q-02, Q-03; BM-1, stage C/E): the designs selected by certified cost, run in the mean-run model** — `u = 1`; for `n ∈ {1000, 4000, 16 000}`, one to three nested levels and ten outer fractions: the cost at the flat instance and the worst outer landscape found (differential evolution, monotone and general radial families, budgets 4000 + 2000 evaluations, 2500 + 1250 from `n = 8000`) with flat fibres, with cone fibres and the base brackets' own answers (reading (B)), and with base brackets at the bottom or the top of their promise (reading (A)); and the theory division's request R16-THY-1(b): two levels at `n ∈ {8000, 32 000, 64 000}`, six outer fractions, readings (B) and (A).  Validation before launch: the two-level numbers of ENG-RES-0014 at `n = 1000` reproduced (`0.9839`, `1.0114`, `1.0461`) | ≤ 50 containers × 1 core; 60 tasks of 1 h / 2 GiB, 42 of 3 h / 2 GiB, 6 of 6 h / 4 GiB; no retries | 60 × $0.063 + 42 × $0.190 + 6 × $0.476 = **$14.63** | one pass | **≈ $0.38** (108 tasks, 5.94 core-hours of task time, longest task 1 102 s; the app run it shares with M-016 is still open — its billed total is entered under M-016 when that job ends); 108 of 108 results collected by 2026-11-26 17:17 UTC; 822 searches, 2.0 million mean runs, no searched cost above its bound | done |
| M-018 | 2026-11-26 | same app: `modal run --detach modal_jobs/bench_app.py::launch --driver hetero_bench --job hetero1 --ledger M-018` | **X-014a (registry Q-11; BM-6): certified cost bounds at finite `n` for cubes with two site types** — slopes `(u_H, u_L) ∈ {(2, ½), (1, ½), (2, 1), (4, 1), (4, ¼)}`, heavy fraction `0.1 … 0.9`, `n ∈ {1000, 4000, 16 000}`: per cell the exact lower bound, the asymptotic exponent, the homogeneous algorithm with slope `u_H` and type-aligned nesting, up to three nested levels.  Protocol with hypotheses: `benchmarks/protocols/BM-6_X-014.md`.  Local timing: one cell at `n = 4000` took 526 s | ≤ 32 containers × 1 core (caps 18 + 14; together with the tasks of M-016 still running, at most 46); 50 tasks of 1 h / 2 GiB, 25 of 3 h / 2 GiB; no retries; every cell stops its own search 10–15 min before its timeout | 50 × $0.063 + 25 × $0.190 = **$7.91** | one pass | **$1.06** (billing report by app run, 2026-11-26 17:56 UTC; 75 tasks, 15.9 core-hours of task time, longest task 2 643 s); app stopped by itself at 17:47 UTC; 75 of 75 cells complete, none reached its time limit | done |
| M-019 | 2026-11-26 | same app: `modal run --detach modal_jobs/bench_app.py::launch --driver nested_literal --job nested1 --ledger M-019` | **X-011f (BM-1, stage B for nested runs): three nested levels run literally, end to end, on 15-site cubes with exact truth** — 4 block configurations with three different slopes × 8 kinds of energy table × 5 seeds × 8 runs = 1280 runs, each with a few hundred real nested runs; hypothesis H8 in `benchmarks/protocols/BM-1_X-011.md`.  Local timing: 1.5–29 s per run | ≤ 18 containers × 1 core × 2 GiB, timeout 1 h, no retries; 160 tasks | 160 × $0.063 = **$10.11**; expected ≈ 160 × 2 min ≈ 5 core-hours ≈ $0.3 | one pass | **$0.25** (billing report by app run; 160 tasks, 3.5 core-hours of task time, longest task 241 s); app stopped by itself at 17:33 UTC; 1 280 end-to-end runs, 643 000 nested runs, hypothesis H8 held without exception | done |
| M-020 | 2026-11-26 | same app: `--driver nested_bench --job instances2 --ledger M-020` | **X-011 stage 2 (registry Q-02, Q-10): both rules of design on the same instances, three slopes** — `u ∈ {½, 1, 2}`, `n ∈ {4000, 16 000}`, twelve outer fractions, four designs per cell (two, three, four levels by certified cost; the referee's three levels chosen at the flat fibre); flat instance, flat fibres, cone fibres of slope `¼u`, `½u`, `u`, reading (A).  Hypotheses H9–H11 in the protocol addendum.  Local timing: 6 searches of 6000 (3750) mean runs at 8–100 ms each | ≤ 32 containers × 1 core × 2 GiB (caps 18 + 14); 144 tasks of 1 h, 144 of 3 h; no retries.  To be launched when M-018 and M-019 have ended, so that the total with M-016 stays below 50 | 144 × $0.063 + 144 × $0.190 = **$36.43**; expected ≈ $5 | one pass | first tier $0.54 (its own app run); the second tier shares a run with M-021: **$7.23 for both** (final; billing report for 2026-11-26 and -27); **288 of 288 cells collected (complete, 01:02 UTC)** | done (the status read "running" until 2026-11-27 18:37 UTC although the job's last cell was collected at 01:02 UTC: the app run it shares with M-021 was still open) — first tier (144 tasks, `n = 4000`) launched 2026-11-26 17:34 UTC at commit `0c0db1f`, complete (144 of 144 collected, 6.9 core-hours of task time); second tier (144 tasks, `n = 16 000`) launched 21:35 UTC at commit `6bca3a2` in one app run with M-021 |
| M-021 | 2026-11-26 | same app: `--driver nested_bench --job certified2 --ledger M-021` | **X-011 stage 2 (registry Q-10): the certified bound to six levels at `u = ½` and `u = 2`**, `n ∈ {1000, 4000, 16 000, 64 000}`, both design families.  Hypothesis H12 | 16 containers × 1 core; 8 tasks of 3 h / 2 GiB, 4 of 6 h / 4 GiB, 4 of 12 h / 4 GiB; no retries; to be launched when the total stays below 50 | 8 × $0.190 + 4 × $0.476 + 4 × $0.952 = **$7.23** | one pass | **$7.23 for the app run it shares with the second tier of M-020** (see M-020); by the task times of its rows the attempts that returned account for $5.84 of it.  **16 of 16 cells collected** (10 of them after the halt) | done — launched 2026-11-26 21:35 UTC at commit `6bca3a2` (10 containers of M-016 and M-022 running at the time); the app run ended by itself on 2026-11-27 between 09:11 and 09:21 UTC |
| M-022 | 2026-11-26 | same app: `--driver hetero_bench --job profile1 --ledger M-022` | **X-014c (BM-6): a continuous profile of slopes, binned** — slopes equally spaced on `[½, 2]`, `n ∈ {4000, 16 000}`, `m ∈ {1, 2, 3, 4, 6, 8}` classes, type-aligned nesting with up to four nested levels.  Hypotheses H5, H6 in the addendum of `benchmarks/protocols/BM-6_X-014.md` | 12 containers × 1 core × 2 GiB, timeout 3 h, no retries; every cell stops its own search 15 min before | 12 × $0.190 = **$2.28** | one pass | **$2.48** (billing report by app run, 2026-11-26 23:35 UTC) — **above the worst case entered ($2.28)**: 39 task-hours for 12 tasks of a three-hour tier, because the platform restarted tasks (policy rule 6); 12 of 12 cells collected, the five-level searches all at their time limit | done — launched 2026-11-26 17:42 UTC at commit `7b9c979`; the app stopped by itself at 22:44 UTC |
| M-023 | 2026-11-26 | same app: `--driver r18_products --job search+seeds --ledger M-023+M-023` | **X-005c (the science division's request R18-ENG-2 (ii), (iii)): the product search and the bound search of X-005 at `n = 250, 350, 500` repeated with the review's starting points** (the reference point behind a ramp; the stored maximisers of both earlier searches) and three times the budgets; seeds 2 and 3 at `φ = 0.5, 0.85`.  The request's correctness criteria are the protocol (SCI-REV-0018 §5; no hypothesis of ours beyond them).  Moved from the local machine, where 30 of the 108 cells had finished and the rest was starved by four subagents' own computations | at most 18 containers × 1 core × 2 GiB (tier m), timeout 1 h, no retries; 78 + 36 tasks of about 5 to 10 minutes | 114 × $0.063 = **$7.22** | one pass | **$0.14** (billing report by app run; 114 tasks, all finished within eleven minutes) | done — launched 2026-11-26 22:23 UTC at commit `7b318c9`, detached (30 containers of the earlier jobs running at the time; launch test: credits consumed $52.05, billed cost $0.00); **finished**: all 114 rows collected at 22:34 UTC, no failure |
| M-024 | 2026-11-26 | same app: `--driver r18_products --job round2 --ledger M-024` | **X-005c, a second round** — M-023 moved the worst product instance in 73 of 108 cells, and seeds 2 and 3 still differ from seed 1 by more than `10⁻⁴·na` in 15 of 36 searches of each kind: the review's stopping condition ("when (iii) changes nothing above `10⁻⁴·na`") is not met.  Two more seeds (4, 5) on all 108 cells, each search starting from every maximiser found so far for either objective, so that a round can only move up.  Reported: how much the best known values move in this round (the convergence diagnostic), not a claim of convergence | at most 18 containers × 1 core × 2 GiB (tier m), timeout 1 h, no retries; 216 tasks of about 5 minutes (M-023: 114 tasks finished within 10 minutes) | 216 × $0.063 = **$13.67** | one pass | **$0.25** (billing report by app run; 216 tasks) | done — launched 2026-11-26 22:41 UTC at commit `b22322a`, detached (29 containers of the earlier jobs running at the time; launch test: credits consumed $52.98, billed cost $0.00); **finished**: all 216 rows collected at 22:57 UTC, no failure |
| M-025 | 2026-11-26 | same app: `--driver r18_products --job round3 --ledger M-025` | **X-005c, a third and last round** — round 2 (M-024) still raised the best known product value by more than `10⁻⁴·na` in 31 of 108 cells (at most `0.0019·na`, against `0.0247·na` in the first round), and its two seeds differ by more than `10⁻⁴·na` in 19 cells.  Seeds 6 and 7, starting from every maximiser of the earlier rounds.  Purpose: a third point of the convergence sequence; whatever it gives, no fourth round | at most 18 containers × 1 core × 2 GiB (tier m), timeout 1 h, no retries; 216 tasks of about 5 minutes | 216 × $0.063 = **$13.67** | one pass | **$0.25** (billing report by app run; 216 tasks) | done — launched 2026-11-26 23:05 UTC at commit `1900a76` (26 containers of the earlier jobs running at the time; launch test: credits consumed $54.01, billed cost $0.00); all 216 rows collected at 23:21 UTC, no failure |

## Local runs worth recording

| date (UTC) | command | wall time | note |
|---|---|---|---|
| 2026-11-25 | `lake exe cache get` (Mathlib v4.31.0 cache) | 2 min 15 s | 7.3 GB under `.lake/` |
| 2026-11-25 | `lake build` at `d81eb8a`, 2 then 4 Lake threads | see ENG-RES-0005 | peak resident set per `lean` process ≈ 4.1 GB (mostly shared, memory-mapped Mathlib) |
| 2026-11-25 | `build/dia_enum -n 19`, `-n 20` | 83 s, 261 s | single core, with pattern bitmaps |
| 2026-11-25 | read-only worktree of the theory branch at `63efc69`: `LEAN_NUM_THREADS=4 lake build` (incremental over the build of `d81eb8a`), then `bash scripts/audit_all.sh --full` | 39 min in total (14:56 → 15:36 UTC) | `AUDIT PASSED`; log in `experiments/eng/audit_replication/audit_all_full_63efc69.log` |
| 2026-11-26 | read-only worktree of the theory branch at `9408e33`: `LEAN_NUM_THREADS=4 lake build` (incremental over the build of `d81eb8a`: 24 Lean files more than at the branch point), then `bash scripts/audit_all.sh --full` | 60 min (03:05 → 04:05 UTC) | `AUDIT PASSED`; the mutation stage and the checks after it about 14 min (435 mutations, 136 baselines) |
| 2026-11-26 | `binomial_bias.py --draws 400000`; `lowered_cap.py`; `recheck_classification.py`; `nonproduct_bound.py`; `separation.py`; `ball_exponents.py`; `three_levels.py --check` | 2 min; 2 min; 2 min; 2 min; 3 s; 5 s; 5 s | single core |
| 2026-11-26 | `run_three_levels.py` (X-010): the base grid of 36 cells, the two-level partner columns, 252 + 108 runs with cone fibres | about 75 min of wall time on 6 to 8 busy threads (04:27 → 05:45 UTC); the 36 base cells alone 4.2 core-hours | local process pools; an estimate made beforehand for the placement-free search (17 min) was five times too low and that search went to Modal (M-014) |
