# Compute and Modal record

*Written for the archive on 2026-11-27; §§3a, 4 and 5 rewritten at the final refresh of the same day,
after the last two jobs were closed.  The authoritative record is the engineering division's ledger,
`02_engineering/docs/engineering/COMPUTE_LEDGER.md` (authorisation and limits, rates, every remote job
with its worst-case cost entered before launch, its measured cost and its state).  This file summarises
it and adds nothing.*

**Final state in one line: no job is running or queued; credits consumed by the workspace $62.99; billed
cost $0.00; $21.58 of the $1,750 authorised used; nothing committed.**

## 1. Who used shared compute

Only the engineering division launched Modal jobs.  In their consolidation reports: science "never used
Modal"; ensemble "never started a Modal job and none is pending"; geometry "no shared compute was ever
used"; complexity "no Modal or other remote jobs (this division never launched one)"; structural biology
"no remote job of this division is running or pending"; frontier "has never launched a Modal job and has
none"; theory "No subagent, background process, scheduled session or computational job of this division
remains active".  The Modal workspace is shared with projects outside MetricChain; the ledger separates
the engineering runs from the workspace total.

## 2. Authorisation and limits (the ledger, "Authorisation and limits")

The research owner authorised "up to $1,750 in additional justified Modal expenditure across the research
program", with at least $200 of credits preserved and no paid charges; from the snapshot at the
authorisation (credits consumed $41.41) that is a ceiling of $1,791.41 of cumulative workspace usage, and
the engineering division kept its own ask-first line at $1,500.  "The available compute budget is not a
spending quota."

## 3. State at the reconciliation of 2026-11-27 01:16 UTC (quoted from the ledger)

> Credits consumed by the workspace, all projects: **$56.99**; billed cost **$0.00**
> (`modal billing summary`).  Since the snapshot of the authorisation ($41.41): **$15.58 of the
> $1,750 authorised**.  Engineering app runs by `modal billing report` (2026-11-26 and 2026-11-27
> so far): M-012 $1.01, M-013 $0.55, M-014 $0.48 (session 3; they agree with the entries above);
> session 4: M-016 with M-017 **$6.42 (open)**, M-020 second tier with M-021 **$3.97 (open)**,
> M-018 $1.06, M-019 $0.25, M-020 first tier $0.54, M-022 $2.48, M-023 $0.14, M-024 $0.25,
> M-025 $0.25, smoke tests $0.01 — **$15.37**.  **Engineering total over all sessions: $24.10**
> ($8.73 to checkpoint 5 and $15.37 since), against worst cases entered of more than $170.
> One entry was exceeded (M-022, $2.48 against $2.28).  No job was launched after the directive.

## 3a. Final reconciliation of 2026-11-27 18:37 UTC (quoted from the ledger)

> Credits consumed by the workspace, all projects: **$62.99**; billed cost **$0.00**
> (`modal billing summary`: metered cost $66.03 = ephemeral apps $62.99 + volumes $2.99 + network
> egress $0.05; credits −$62.99; egress allowance −$0.05).  Since the snapshot of the
> authorisation ($41.41): **$21.58 of the $1,750 authorised**; by the owner's figure of $2,030.00
> of credits granted, about **$1,967 are left** (reserve to be preserved: $200).  Since the
> reconciliation of 01:16 UTC ($56.99): **$6.00**, against the worst cases stated there of $5.2
> without restarts and $16.7 with one restart of every task.

> By app run (`modal billing report` for 2026-11-26 and 2026-11-27): M-016 with M-017 **$9.35**
> ($5.82 + $3.52); the second tier of M-020 with M-021 **$7.23** ($3.01 + $4.22).  **Engineering
> total over all sessions: $30.28** […] against worst cases entered of more than $170.  Other
> projects of the workspace: $32.72, unchanged since 2026-11-20.

Also from the ledger: job **M-016 cost about $8.97 against its entry of $8.56** — the second entry
exceeded, after M-022, because the platform restarted tasks and an entry counts one attempt per task.
The line "Volumes" of the billing summary ($2.99, rising by about $0.03 an hour) belongs to volumes of
projects outside MetricChain; at that reading it was neither charged to the credits nor billed.  What
engineering leaves in the workspace is one result store (a `modal.Dict` whose entries expire seven days
after their last access); nothing is deployed.

## 4. Every job

| jobs | final state | what |
|---|---|---|
| M-001 | done | smoke test of the image |
| M-002, M-005, M-007 | done | lattice and off-lattice chain covers and class tables (THY-REQ-0002) |
| M-004, M-006 | stopped by hand; superseded by M-005, M-007 | the same, first attempts |
| M-003 | done | the theory division's falsification harness under other seeds on a third platform (THY-REQ-0005) |
| M-008 … M-011 | done | X-005, X-006: searches and literal runs of Algorithm 2L⁺ (THY-REQ-0001) |
| M-012, M-013, M-014 | completed (741 of 741 cases; 12 of 12 tasks; 360 of 360 cells) | X-006b (exact sampler), X-005 convergence control, X-005b (non-product instances), asked for by science |
| M-015 | done | smoke test of the batch driver |
| M-017, M-019 | done | X-011b (designs run in the mean-run model), X-011f (three nested levels run literally) |
| M-018, M-022 | done | X-014: cubes with several site types; a binned continuous profile of slopes |
| M-023, M-024, M-025 | done | X-005c: three rounds of the searches asked for by SCI-REV-0018 |
| M-020 | complete: 288 of 288 cells | X-011 stage 2, runs |
| **M-016** | **closed, incomplete by one cell**: 17 of 18 cells stored; the app run was stopped on 2026-11-27 at 18:24 UTC with one restarted task still running | X-011a: the certified bound to six levels, `u = 1`; the six cells that were open at the halt are `n = 32 000, 64 000, 128 000` |
| **M-021** | **done**: 16 of 16 cells stored; its app run ended by itself on 2026-11-27 between 09:11 and 09:21 UTC | X-011 stage 2: the same bound at slopes ½ and 2 |

No deployment, no persistent service, no scheduled job, no GPU.

## 5. The two jobs that were left running under the consolidation directive, and how they ended

Both were detached runs with fixed timeouts and no retries.  From the ledger ("Jobs left running"):
M-016 six tasks in the 12-hour tier, launched 2026-11-26 16:20 UTC; M-021 four tasks in the 12-hour
tier, three in the 6-hour tier and three in the 3-hour tier, launched 21:35 UTC.  "Worst case still to be
spent: **$5.2** without restarts, **$16.7** with one restart of every" task.

How they ended (ledger, "Final reconciliation"; the engineering division's own account):

* **M-021 finished**: 16 of 16 cells.
* **M-016 is one cell short.**  "M-016's app run still had one task at 18:20 UTC — the cell `u = 1`,
  `n = 32 000`, family "wide" — in a container started at 13:01 UTC, 20 h 41 min after the launch: a
  restart by the platform (rule 6), and not the task's first.  Its search stops itself after 42 300 s, so
  that attempt would have returned at about 00:46 UTC on 2026-11-28, after the cutoff of 22:00 UTC
  written above; D-10 forbids extending deadlines and restarting.  **The run was stopped with
  `modal app stop` on 2026-11-27 at 18:24 UTC; that cell has no row**".  It was not restarted.
* The local watcher that waited for the runs saw no open run at 18:32 UTC, collected once more (no new
  row) and ended.
* Spent after the reconciliation of 01:16 UTC: $6.00.

The collected rows, their integrity check, the tables and what they decide:
[`X-011_ADDENDUM.md`](../02_engineering/docs/engineering/benchmarks/X-011_ADDENDUM.md) (unrefereed).

**State when this version of the archive was built:**
<!-- GEN:status -->
FINAL (built 2026-11-27 under the research owner's directive for the final collection and handoff): every Modal job of the programme is closed and nothing is running.  The engineering section is pinned at the commit that holds the collected results of jobs M-016 and M-021, the tables made from them and the closed compute ledger; one cell of job M-016 has no result, and most of the larger searches ran into their time limits (see the record of incomplete items).  The other seven divisions pushed nothing after the interim version and are pinned at the same commits as there.  The interim version remains in the history of this branch as commit 5c2bcec.
<!-- /GEN:status -->

## 6. Local computations

Everything else in the programme ran on local processors or in the divisions' cloud sessions.  The
engineering ledger lists its local runs worth recording ("Local runs worth recording"); the other
divisions give run times in their handoff documents.  Measured bottlenecks: engineering consolidation
report §G.
