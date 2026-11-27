# Compute and Modal record

*Written for the archive on 2026-11-27.  The authoritative record is the engineering division's ledger,
`02_engineering/docs/engineering/COMPUTE_LEDGER.md` (authorisation and limits, rates, every remote job
with its worst-case cost entered before launch, its measured cost and its state).  This file summarises
it and adds nothing.*

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

## 4. Every job

| jobs | state at the halt | what |
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
| **M-016** | **6 of 18 tasks still running at 01:16 UTC** | X-011a: the certified bound to six levels at `n = 32 000, 64 000, 128 000` |
| **M-021** | **10 of 16 tasks still running at 01:16 UTC** | X-011 stage 2: the same bound at slopes ½ and 2 |

No deployment, no persistent service, no scheduled job, no GPU.

## 5. The two jobs left running under the consolidation directive

Both are detached runs with fixed timeouts and no retries; they end by themselves and leave nothing
deployed.  From the ledger ("Jobs left running"): M-016 six tasks in the 12-hour tier, launched
2026-11-26 16:20 UTC; M-021 four tasks in the 12-hour tier, three in the 6-hour tier and three in the
3-hour tier, launched 21:35 UTC.  "Worst case still to be spent: **$5.2** without restarts, **$16.7**
with one restart of every" task; cumulative workspace credits then at most $73.7 against the stop line of
$1,500.  Results are collected with

```
python modal_jobs/bench_collect.py --driver nested_bench --job certified1+certified2
```

from the engineering checkout (the result store expires seven days after its last access).

**State when this version of the archive was built:**
<!-- GEN:status -->
INTERIM (built 2026-11-27): two bounded Modal runs of the engineering division (compute-ledger jobs M-016 and M-021) were still running when this version was built, and their results are not in it.  The engineering section is refreshed once after they have been collected; the other seven divisions are pinned at the heads they pushed under the consolidation directive.
<!-- /GEN:status -->

## 6. Local computations

Everything else in the programme ran on local processors or in the divisions' cloud sessions.  The
engineering ledger lists its local runs worth recording ("Local runs worth recording"); the other
divisions give run times in their handoff documents.  Measured bottlenecks: engineering consolidation
report §G.
