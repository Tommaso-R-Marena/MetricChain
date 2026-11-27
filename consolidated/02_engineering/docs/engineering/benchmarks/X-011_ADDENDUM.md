# Addendum to ENG-RES-0015 (experiment X-011, campaign BM-1): the rows collected after the halt

*Written on 2026-11-27 at about 19:00 UTC by the Computational Research Division, during the controlled
halt, under the research owner's directive D-10 ("Final Collection, Archive Refresh and Research
Handoff"; `docs/engineering/DIRECTIVES.md`).  This is the "linked addendum" that ENG-RES-0015 announces
for the rows that were still being computed when it was published.  It is **not a mailbox message**: it
asks nothing of any division and nobody is expected to act on it.*

*It is administrative.  The tables are generated from the stored rows by the generator of ENG-RES-0015
(`experiments/eng/twolevel/make_tables_x011.py`; blocks added for these rows, the fifty existing blocks
unchanged).  The hypotheses are the ones written down before the rows existed
(`protocols/BM-1_X-011.md`).  Nothing was re-run, extended, tuned or restarted, and no conclusion is
drawn here beyond what each hypothesis itself names.  **Unrefereed**: no referee of this division or of
any other has read it, and the coordinator who wrote it also ran the jobs.*

Evidence class of everything below: **[X]** exact arithmetic of a published formula (the cost bound of
the theory division's Theorem 11.56, minimised over finite families of designs by
`src/metricchain_eng/twolevel/certified.py`).  No instance was run at these sizes or slopes; no
statement about an algorithm's behaviour on an instance follows from these rows.

## 0. Summary

| | |
|---|---|
| job M-021 (`certified2`: slopes `u = ½` and `u = 2`, `n = 1000 … 64 000`, two families) | **16 of 16 cells collected.**  10 of them end with a search that ran into its time limit |
| job M-016 (`certified1`: `u = 1`; the sizes that were open: `n = 32 000, 64 000, 128 000`, two families) | **5 of 6 cells collected** (17 of the job's 18).  All five end with a search that ran into its time limit |
| missing | **one cell: `u = 1`, `n = 32 000`, family "wide"** — no row, no partial result (§1) |
| integrity of the 33 stored rows | structure consistent; the first two nested levels of every row recomputed locally and equal (§2).  Deeper levels not recomputed |
| H12 (saturation after four levels at `u = ½`, `2`, `n ≤ 16 000`) | **refuted**: a fifth level still lowers the certified bound at `u = ½`, `n = 16 000` and at `u = 2` at all three sizes; it holds at `u = ½`, `n = 1000` and `4000` (§5) |
| H13 (shares of each level's asymptotic gain kept, `u = 1`, `n ≥ 16 000`) | part (a) **refuted at the new sizes too** (4 of 10 finished shares outside the predicted ranges); part (b) **formally refuted by one share, on a margin inside the rounding of the constants** (`0.5018` against "less than `0.50`") — in effect undecided; the other shares of part (b) are unfinished (§5) |
| H3 (the two families differ by less than `0.02` up to four levels) | **refuted at `n = 64 000` and `128 000`** (`0.037`, `0.031` with four levels); not decidable at `32 000` (one family) (§5) |
| H1 (a fifth nested level never gains more than `0.001`) | **not decided at `n ≥ 32 000`**: no search with five nested levels finished (§5) |
| H2 (excess over the lower bound grows in nats, ratio falls, constant near 1) | holds on the bounds found; every one of them comes from an unfinished search, and the row at `32 000` has one family (§3, §5) |
| cost | the two app runs: **$9.35** (M-016 with M-017) and **$7.23** (second tier of M-020 with M-021); nothing running; billed cost $0.00 (`docs/engineering/COMPUTE_LEDGER.md`) |

## 1. What was collected, and what is missing

Collected with `python modal_jobs/bench_collect.py --driver nested_bench --job certified1+certified2` on
2026-11-27 at 18:20 UTC (5 new rows of `certified1`, 10 of `certified2`; no failure recorded by a task),
again at 18:24 UTC after the stop below and once more by the local watcher at 18:32 UTC (no new row
either time).

**Job M-021 is complete.**  Its app run ended by itself between 09:11 and 09:21 UTC on 2026-11-27.

**Job M-016 is incomplete by one cell: `u = 1`, `n = 32 000`, family "wide".**  What happened to it:

* The job was launched on 2026-11-26 at 16:20 UTC; a task of the twelve-hour tier stops its own search
  after 42 300 s and returns what it has, so one attempt ends about 11 h 45 min after it starts.
* On 2026-11-27 at 18:20 UTC this task was still running, in a container that had started at 13:01 UTC —
  20 h 41 min after the launch.  The functions have no retries; a start that late is a restart by the
  platform after a pre-emption (ledger, policy rule 6), and by its time it was not this task's first.
  Nothing of an interrupted attempt is kept: the task returns its row only at the end.
* That attempt would have returned at about 00:46 UTC on 2026-11-28.  The ledger's rule for these jobs,
  written at the halt, was to stop anything still running after 22:00 UTC on 2026-11-27; so no row of
  this cell could arrive within the existing deadline, and directive D-10 forbids extending it ("Do not
  restart failed computations, launch new jobs, or extend existing resource authorizations … Do not wait
  indefinitely").
* The app run was therefore stopped by this division on 2026-11-27 at 18:24 UTC
  (`modal app stop`), three and a half hours before that cutoff, rather than paying for hours that could
  not produce a result.  **The cell has no row and no partial result, and it was not restarted.**  To
  obtain it, one task of twelve hours on one core with 4 GiB (about $0.95) would have to be authorised
  and launched again; nothing here assumes that it will be.

Consequence for the tables: at `n = 32 000` every number is from the family "theory" alone ("…" stands
where the other family would be).  At every other size the tables take the better of two families, so
**the row of `32 000` is not comparable with its neighbours** in the tables of the excess, the overhead and
the gain of a level (§3).

## 2. Integrity of the stored rows

    python experiments/eng/twolevel/check_late_rows.py --recompute

(output stored in `experiments/eng/twolevel/results/x011_late_rows_check.txt`).  For both jobs:

* every stored row belongs to a task of its job, once, with the task's parameters and the job's ledger
  number; the commits the rows name (`55bec29` for M-016, `6bca3a2` for M-021) are in the history of this
  branch, and `certified.py` has not changed since either;
* levels are numbered consecutively, only the last level of a row is unfinished, a row with fewer
  levels than were asked for ends unfinished, no run exceeded its time limit, the best bound found never
  increases with the number of levels, and the two families of a size agree on the lower bound, the
  base bracket and the constants — **0 structural problems in 33 rows; 1 task without a row**;
* **recomputation:** for each of the 33 rows, the bounds with one and two nested levels at each of the
  18 outer fractions (36 numbers) and six constants were recomputed on the local machine with the code
  of this branch and agree with the stored row to `10⁻⁹` — 33 of 33.

**Not checked:** the levels beyond the second (three to five nested levels), which took from minutes to
twelve hours per cell and were not recomputed.  Twenty of the 33 rows end with a search that ran into
its time limit; what such a search reports is the best bound found in that time on that machine — a
valid bound of the formula, an upper bound of the minimum over the family, and **not reproducible to
the digit**.  The rows carry no time stamps, so when each task ran, and how often it was restarted, is
known only from the platform's listing at the moments it was looked at.

## 3. Job M-016: `u = 1` at `n = 32 000`, `64 000`, `128 000`

The same tables as ENG-RES-0015 §2 (which has `n ≤ 16 000`), for the rows that arrived later.

<!-- TABLE:x011_bounds_large -->
| `n` | lower bound, every algorithm | base bracket alone (not adaptive) | 2 levels | 3 levels | 4 levels | 5 levels | 6 levels | levels after which nothing improves |
|---|---|---|---|---|---|---|---|---|
| 32000 | 0.2639 | 1.0472 | 0.5646 / … | 0.4439 / … | 0.4328 / … | 0.4221 / … | 0.4221* / … | not determined (unfinished) |
| 64000 | 0.2633 | 1.0325 | 0.5407 | 0.4341 / 0.4229 | 0.4125 / 0.3754 | 0.3947* / 0.3754* | 0.3947* / 0.3754* | not determined (unfinished) |
| 128000 | 0.2630 | 1.0227 | 0.5362 | 0.4254 / 0.4115 | 0.4000 / 0.3688 | 0.3907* / 0.3688* | 0.3907* / 0.3688* | not determined (unfinished) |
<!-- /TABLE:x011_bounds_large -->

<!-- TABLE:x011_bounds_caption_large -->
`ln(bound)/(n a)`, `u = 1` (`a = 0.11094`; the exponent of every algorithm is `h/a = 0.2626` in these units, enumeration costs `6.248`).  "`k` levels" = `k − 1` nested runs of Algorithm 2L⁺ above base brackets, every server chosen by certified cost; the least bound over 18 outer fractions of the top level.  Where two numbers are given: candidate family "theory" / family "wide".  An asterisk: the search did not finish within its time limit — the number is the best bound found, an upper bound of the minimum over the family.
<!-- /TABLE:x011_bounds_caption_large -->

"…": the cell of the family "wide" at `n = 32 000` has no row (§1).  At `64 000` and `128 000` the searches
with five levels did not finish and those with six were not started; at `32 000` the search with six
levels did not finish.  So the number of levels after which nothing improves is not determined at any
of the three sizes.

Distance from the lower bound for every algorithm (the theory division's Theorem 11.25(a) at the
certified accuracy; computed by `alg2l.hinted_lower_bound`):

<!-- TABLE:x011_excess_large -->
| `n` | best certified bound | lower bound | ratio | excess in nats | excess / `√(n ln n)` |
|---|---|---|---|---|---|
| 32000 | 0.4221* | 0.2639 | 1.60 | 561 | 0.97 |
| 64000 | 0.3754* | 0.2633 | 1.43 | 796 | 0.95 |
| 128000 | 0.3688* | 0.2630 | 1.40 | 1502 | 1.22 |
<!-- /TABLE:x011_excess_large -->

Against the theory division's certified exponents `c_k` of the same number of levels (its workstream Z;
`c_2, …, c_6 = 0.5004, 0.3633, 0.3128, 0.2914, 0.2813` in units of `a`; quoted to four decimals, not
recomputed by us):

<!-- TABLE:x011_overhead_large -->
| `n` | 2 levels: bound − `c_2`; in nats | 3 levels: bound − `c_3`; in nats | 4 levels: bound − `c_4`; in nats | 5 levels: bound − `c_5`; in nats |
|---|---|---|---|---|
| 32000 | 0.0642; 228 | 0.0806; 286 | 0.1200; 426 | 0.1307; 464 |
| 64000 | 0.0403; 286 | 0.0596; 423 | 0.0626; 445 | 0.0840*; 597 |
| 128000 | 0.0358; 508 | 0.0482; 684 | 0.0560; 795 | 0.0774*; 1099 |
<!-- /TABLE:x011_overhead_large -->

What one more level gains in the limit, and what the best bound found keeps of it (nats; "share" =
realised gain over the gain in the limit):

<!-- TABLE:x011_level_gain_large -->
| `n` | level 3: gain in the limit, `n a (c_2 − c_3)`; realised; share | level 4: gain in the limit, `n a (c_3 − c_4)`; realised; share | level 5: gain in the limit, `n a (c_4 − c_5)`; realised; share |
|---|---|---|---|
| 32000 | 487; 429; 0.88 | 179; 39; 0.22 | 76; 38; 0.50 |
| 64000 | 973; 837; 0.86 | 359; 337; 0.94 | 152; 0; 0.00 |
| 128000 | 1947; 1771; 0.91 | 717; 607; 0.85 | 304; 0; 0.00 |
<!-- /TABLE:x011_level_gain_large -->

The shares per family (the table that prediction H13 is about):

<!-- TABLE:x011_h13_large -->
| `n` | family | level 3: share kept | level 4 | level 5 | level 6 |
|---|---|---|---|---|---|
| 32000 | theory | 0.88 | 0.22 | 0.50 | 0.00* |
| 64000 | theory | 0.78 | 0.43 | 0.83* | — |
| 64000 | wide | 0.86 | 0.94 | 0.00* | — |
| 128000 | theory | 0.81 | 0.50 | 0.44* | — |
| 128000 | wide | 0.91 | 0.85 | 0.00* | — |
<!-- /TABLE:x011_h13_large -->

In the three tables before the last, the row of `32 000` uses the family "theory" only and the rows of
`64 000` and `128 000` the better of the two families; the last table separates the families.

## 4. Job M-021: the certified bound at `u = ½` and `u = 2`

The first two tables of §3 at the other two slopes.  The tables that compare with the exponents `c_k`
are not given: those constants were computed by the theory division for `u = 1` only.  No hypothesis
was registered about the excess over the lower bound at these slopes; its table is given for
completeness and is not read here.

**`u = ½`**

<!-- TABLE:x011_bounds_u05 -->
| `n` | lower bound, every algorithm | base bracket alone (not adaptive) | 2 levels | 3 levels | 4 levels | 5 levels | 6 levels | levels after which nothing improves |
|---|---|---|---|---|---|---|---|---|
| 1000 | 0.3239 | 1.6475 | 2.2692 | 2.2692 | 2.2692 | 2.2692 | 2.2692 | 2 |
| 4000 | 0.2751 | 1.2440 | 1.0509 | 1.0509 | 1.0509 | 1.0509 | 1.0509 | 2 |
| 16000 | 0.2605 | 1.1010 | 0.6930 | 0.5857 | 0.5561 / 0.5558 | 0.5532 / 0.5513 | 0.5532 / 0.5513* | not determined (unfinished) |
| 64000 | 0.2554 | 1.0452 | 0.5774 | 0.4644 | 0.4545 / 0.4239 | 0.4446 / 0.4239* | 0.4446* / 0.4239* | not determined (unfinished) |
<!-- /TABLE:x011_bounds_u05 -->

<!-- TABLE:x011_bounds_caption_u05 -->
`ln(bound)/(n a)`, `u = ½` (`a = 0.03030`; the exponent of every algorithm is `h/a = 0.2532` in these units, enumeration costs `22.876`).  "`k` levels" = `k − 1` nested runs of Algorithm 2L⁺ above base brackets, every server chosen by certified cost; the least bound over 18 outer fractions of the top level.  Where two numbers are given: candidate family "theory" / family "wide".  An asterisk: the search did not finish within its time limit — the number is the best bound found, an upper bound of the minimum over the family.
<!-- /TABLE:x011_bounds_caption_u05 -->

<!-- TABLE:x011_excess_u05 -->
| `n` | best certified bound | lower bound | ratio | excess in nats | excess / `√(n ln n)` |
|---|---|---|---|---|---|
| 1000 | 2.2692 | 0.3239 | 7.01 | 59 | 0.71 |
| 4000 | 1.0509 | 0.2751 | 3.82 | 94 | 0.52 |
| 16000 | 0.5513* | 0.2605 | 2.12 | 141 | 0.36 |
| 64000 | 0.4239* | 0.2554 | 1.66 | 327 | 0.39 |
<!-- /TABLE:x011_excess_u05 -->

At `n = 1000` (30 nats) the certified bound of every nested design of the two families is above that of
the base bracket alone (`2.2692` against `1.6475`), and at `n = 4000` (121 nats) a third and further levels
certify nothing below the bound of two.  (The searches of these four cells finished.)

**`u = 2`**

<!-- TABLE:x011_bounds_u2 -->
| `n` | lower bound, every algorithm | base bracket alone (not adaptive) | 2 levels | 3 levels | 4 levels | 5 levels | 6 levels | levels after which nothing improves |
|---|---|---|---|---|---|---|---|---|
| 1000 | 0.3061 | 1.2285 | 0.8043 | 0.7087 | 0.6884 / 0.6883 | 0.6810 | 0.6810 / 0.6810* | not determined (unfinished) |
| 4000 | 0.2999 | 1.1043 | 0.6230 | 0.5308 / 0.5239 | 0.5257 / 0.4916 | 0.5170 / 0.4916* | 0.5170* / 0.4916* | not determined (unfinished) |
| 16000 | 0.2977 | 1.0500 | 0.5595 | 0.4722 / 0.4578 | 0.4559 / 0.4174 | 0.4501* / 0.4174* | 0.4501* / 0.4174* | not determined (unfinished) |
| 64000 | 0.2970 | 1.0242 | 0.5438 | 0.4559 / 0.4373 | 0.4332 / 0.3931 | 0.4278* / 0.3931* | 0.4278* / 0.3931* | not determined (unfinished) |
<!-- /TABLE:x011_bounds_u2 -->

<!-- TABLE:x011_bounds_caption_u2 -->
`ln(bound)/(n a)`, `u = 2` (`a = 0.32781`; the exponent of every algorithm is `h/a = 0.2968` in these units, enumeration costs `2.114`).  "`k` levels" = `k − 1` nested runs of Algorithm 2L⁺ above base brackets, every server chosen by certified cost; the least bound over 18 outer fractions of the top level.  Where two numbers are given: candidate family "theory" / family "wide".  An asterisk: the search did not finish within its time limit — the number is the best bound found, an upper bound of the minimum over the family.
<!-- /TABLE:x011_bounds_caption_u2 -->

<!-- TABLE:x011_excess_u2 -->
| `n` | best certified bound | lower bound | ratio | excess in nats | excess / `√(n ln n)` |
|---|---|---|---|---|---|
| 1000 | 0.6810* | 0.3061 | 2.22 | 123 | 1.48 |
| 4000 | 0.4916* | 0.2999 | 1.64 | 251 | 1.38 |
| 16000 | 0.4174* | 0.2977 | 1.40 | 628 | 1.60 |
| 64000 | 0.3931* | 0.2970 | 1.32 | 2016 | 2.40 |
<!-- /TABLE:x011_excess_u2 -->

## 5. The hypotheses these rows were to decide

All five were written before the rows existed (`protocols/BM-1_X-011.md`: H1–H3 before job M-016, H12
before job M-021, H13 on 2026-11-26 at 21:57 UTC before any row at `n ≥ 16 000`).  The outcomes for
`n ≤ 16 000` are in ENG-RES-0015 §1 and are not repeated.

**H12.**  *"At `u = ½` and `2` the certified bound stops improving after four levels for `n ≤ 16 000`."*

<!-- TABLE:x011_h12 -->
| `u` | `n` | `n a` in nats | family | four levels | five levels | six levels | does a fifth or sixth level lower the bound? |
|---|---|---|---|---|---|---|---|
| ½ | 1000 | 30 | theory | 2.2692 | 2.2692 | 2.2692 | no |
| ½ | 1000 | 30 | wide | 2.2692 | 2.2692 | 2.2692 | no |
| ½ | 4000 | 121 | theory | 1.0509 | 1.0509 | 1.0509 | no |
| ½ | 4000 | 121 | wide | 1.0509 | 1.0509 | 1.0509 | no |
| ½ | 16000 | 485 | theory | 0.5561 | 0.5532 | 0.5532 | **yes**, by 0.0030 (1.4 nats) |
| ½ | 16000 | 485 | wide | 0.5558 | 0.5513 | 0.5513* | **yes**, by 0.0045 (2.2 nats) at least (search unfinished) |
| 2 | 1000 | 328 | theory | 0.6884 | 0.6810 | 0.6810 | **yes**, by 0.0073 (2.4 nats) |
| 2 | 1000 | 328 | wide | 0.6883 | 0.6810 | 0.6810* | **yes**, by 0.0074 (2.4 nats) at least (search unfinished) |
| 2 | 4000 | 1311 | theory | 0.5257 | 0.5170 | 0.5170* | **yes**, by 0.0087 (11.5 nats) at least (search unfinished) |
| 2 | 4000 | 1311 | wide | 0.4916 | 0.4916* | 0.4916* | not determined (search unfinished; nothing better found) |
| 2 | 16000 | 5245 | theory | 0.4559 | 0.4501* | 0.4501* | **yes**, by 0.0059 (30.7 nats) at least (search unfinished) |
| 2 | 16000 | 5245 | wide | 0.4174 | 0.4174* | 0.4174* | not determined (search unfinished; nothing better found) |
<!-- /TABLE:x011_h12 -->

<!-- TABLE:x011_h12_summary -->
`u = ½`: of 6 cells (three sizes, two families) a fifth or sixth level lowers the certified bound by more than `0.0001` in 2, lowers nothing in 4 whose searches finished, and 0 are not determined;  `u = 2`: of 6 cells (three sizes, two families) a fifth or sixth level lowers the certified bound by more than `0.0001` in 4, lowers nothing in 0 whose searches finished, and 2 are not determined.  An asterisk: the search did not finish within its time limit; a bound it found is still a bound.
<!-- /TABLE:x011_h12_summary -->

**Outcome: refuted.**  It holds at `u = ½` for `n = 1000` and `4000`, where nothing improves after two
levels.  It fails at `u = ½`, `n = 16 000` in both families, and at `u = 2` at all three sizes in the
family "theory" and at `n = 1000` in the family "wide".  For the family "wide" at `u = 2`, `n = 4000` and
`16 000`, the search with five levels found nothing better before its time limit, which decides nothing.
The gains are small in absolute terms (1.4 to 31 nats).

**H13.**  *"At `u = 1`, with either family, at every size of M-016 from `16 000` to `128 000`: (a) the share
kept of a third level's gain in the limit is at least `0.80`, of a fourth level's between `0.40` and `0.80`;
(b) a fifth level keeps less than half of its gain in the limit, and a sixth level less than a quarter of
its own.  Refuted by one size and level outside these ranges among the rows whose searches finished;
rows that ran into their time limit are reported and do not count."*

<!-- TABLE:x011_h13_check_large -->
| `n` | family | level | share kept | search finished | predicted | inside | same side within the rounding of `c_k` |
|---|---|---|---|---|---|---|---|
| 32000 | theory | 3 | 0.8807 | yes | at least `0.80` | yes | yes |
| 32000 | theory | 4 | 0.2192 | yes | `0.40` to `0.80` | **no** | yes |
| 32000 | theory | 5 | 0.5018 | yes | less than `0.50` | **no** | no (0.4994 … 0.5041) |
| 32000 | theory | 6 | 0.0000 | no — reported, not counted | less than `0.25` | yes | yes |
| 64000 | theory | 3 | 0.7776 | yes | at least `0.80` | **no** | yes |
| 64000 | theory | 4 | 0.4270 | yes | `0.40` to `0.80` | yes | yes |
| 64000 | theory | 5 | 0.8304 | no — reported, not counted | less than `0.50` | **no** | yes |
| 64000 | wide | 3 | 0.8594 | yes | at least `0.80` | yes | yes |
| 64000 | wide | 4 | 0.9392 | yes | `0.40` to `0.80` | **no** | yes |
| 64000 | wide | 5 | 0.0002 | no — reported, not counted | less than `0.50` | yes | yes |
| 128000 | theory | 3 | 0.8083 | yes | at least `0.80` | yes | yes |
| 128000 | theory | 4 | 0.5020 | yes | `0.40` to `0.80` | yes | yes |
| 128000 | theory | 5 | 0.4364 | no — reported, not counted | less than `0.50` | yes | yes |
| 128000 | wide | 3 | 0.9096 | yes | at least `0.80` | yes | yes |
| 128000 | wide | 4 | 0.8458 | yes | `0.40` to `0.80` | **no** | yes |
| 128000 | wide | 5 | 0.0000 | no — reported, not counted | less than `0.50` | yes | yes |
<!-- /TABLE:x011_h13_check_large -->

<!-- TABLE:x011_h13_summary_large -->
Shares whose searches finished: 11; inside the predicted range: 6; outside: 5, of which 1 within what the rounding of the constants `c_k` can move (0 of those inside likewise).  Shares with an unfinished search (reported, not counted, as the protocol fixed): 5.
<!-- /TABLE:x011_h13_summary_large -->

**Outcome at the three new sizes.**  **(a) refuted**, as at `16 000`: the third level's share is below
`0.80` once (`0.78`; `64 000`, family "theory") and the fourth level's is outside `0.40`–`0.80` in three of
five cells (`0.22`; `0.94`; `0.85`) — 4 of the 10 finished shares of part (a).  **(b) formally refuted by one
share, on a margin that the constants do not support — in effect undecided**: the only fifth-level share
whose searches finished is `0.5018` (`32 000`, family "theory") against "less than half"; by the rule fixed
in advance that refutes (b), but the margin of `0.0018` is inside what the four-decimal rounding of the
constants `c_k` moves the share (`0.4994` to `0.5041`), and those constants were not recomputed.  The four
other fifth-level shares and the one sixth-level share come from unfinished searches; one of them,
`0.83` at `64 000` in the family "theory", is a share already realised by a bound that was found and is
above one half — by the rule fixed in advance it is reported and does not count.  The last column of
the table is the only thing added to what the protocol asks: it says whether a verdict would change
within the rounding of constants that are not ours.

**H3.**  *"'wide' lowers `B_k(n)` by less than `0.02` against 'theory' for `k ≤ 3` at every size."*

<!-- TABLE:x011_h3_large -->
| `n` | levels | family "theory" | family "wide" | difference | below `0.02` |
|---|---|---|---|---|---|
| 32000 | 2, 3, 4 | present | no row | — | not decidable: one family has no row |
| 64000 | 2 | 0.5407 | 0.5407 | 0.0000 | yes |
| 64000 | 3 | 0.4341 | 0.4229 | 0.0112 | yes |
| 64000 | 4 | 0.4125 | 0.3754 | 0.0371 | **no** |
| 128000 | 2 | 0.5362 | 0.5362 | 0.0000 | yes |
| 128000 | 3 | 0.4254 | 0.4115 | 0.0139 | yes |
| 128000 | 4 | 0.4000 | 0.3688 | 0.0312 | **no** |
<!-- /TABLE:x011_h3_large -->

**Outcome: refuted at `64 000` and `128 000`** with four levels (as at `16 000` in ENG-RES-0015), holding
with two and three; **not decidable at `32 000`**, where one family has no row.

**H1.**  *"… stops decreasing at some `k*(n) ≤ 5` for every `n ≤ 128 000` … Refuted if a fifth nested level
still lowers the bound by more than `0.001` at some size."*

<!-- TABLE:x011_h1_large -->
| `n` | family | five levels (four nested) | six levels (five nested) | the search with five nested levels |
|---|---|---|---|---|
| 32000 | theory | 0.4221 | 0.4221* | reached, unfinished; best bound found lower by 0.0000 |
| 64000 | theory | 0.3947* | — | not reached: the search with four nested levels ran into the time limit |
| 64000 | wide | 0.3754* | — | not reached: the search with four nested levels ran into the time limit |
| 128000 | theory | 0.3907* | — | not reached: the search with four nested levels ran into the time limit |
| 128000 | wide | 0.3688* | — | not reached: the search with four nested levels ran into the time limit |
<!-- /TABLE:x011_h1_large -->

**Outcome: not decided at `n ≥ 32 000`.**  The refuting event was not observed, and it could not have been:
no search with five nested levels finished at these sizes, and at `64 000` and `128 000` none was started.

**H2.**  *"The excess of the best certified bound over the lower bound … grows with `n` over the whole
range … while the ratio … decreases … an effective constant `excess/√(n ln n)` near 1 and far below
`8.6` … No prediction of its trend; the fit of `excess = c·n^γ` is reported whatever it gives."*

**Outcome: holds on the bounds found** (table `x011_excess_large`, §3): the excess grows (`561`, `796`, `1502`
nats after `293` at `16 000`), the ratio falls (`1.60`, `1.43`, `1.40` after `1.62`), the constant is `0.97`,
`0.95`, `1.22`.  Two reservations: all three best bounds come from unfinished searches, so each is an
upper bound of the best its family can certify; and the row of `32 000` rests on one family.  **The fit
named in the hypothesis was not reported in ENG-RES-0015 and is not computed here** — a deviation from
the protocol, now recorded in its section "Deviations".

## 6. What these rows cannot show

* Every bound here is a valid certified bound of the formula for a design that was found; where a
  search did not finish it is not the minimum over the family.  "How many levels pay" is therefore not
  determined at any size above `16 000` at `u = 1`, above `4000` at `u = ½`, or at any size at `u = 2`.
* The shares of H13 are properties of the designs searched and of the two finite families, as
  ENG-RES-0015 §2 already says; the two families give shares on opposite sides of the predicted range
  at the same size.
* One cell is missing (§1).  Unfinished searches are not reproducible to the digit (§2).
* Bounds only: no design of these sizes or slopes was run on an instance, so nothing here bears on the
  worst-case findings of ENG-RES-0015 §§3–6 or on their limitation by SCI-REV-0018.
* The constants `c_k` are the theory division's and were not recomputed.
* Unrefereed (see the head of this file).

## 7. Cost and state of the jobs

`docs/engineering/COMPUTE_LEDGER.md`, "Final reconciliation": measured cost of the two app runs $9.35
(jobs M-016 and M-017) and $7.23 (second tier of M-020 and M-021); job M-016 exceeded its entry of
$8.56 by about $0.4 because the platform restarted tasks; no engineering app is running; billed cost
$0.00.

## 8. Reproduction

    python experiments/eng/twolevel/check_late_rows.py --recompute                                  # §2 (a few minutes, local)
    python experiments/eng/twolevel/make_tables_x011.py --verify docs/engineering/benchmarks/X-011_ADDENDUM.md
    python experiments/eng/twolevel/make_tables_x011.py --verify docs/collaboration/responses/engineering/ENG-RES-0015.md   # unchanged

Artifacts: `experiments/eng/twolevel/results/x011_certified1.jsonl` (17 rows; the 12 used by ENG-RES-0015
are listed in `x011_published_rows.json`, the other 5 are the rows of §3) and `x011_certified2.jsonl` (16
rows, §4).  The jobs cannot be reproduced to the digit where a search ran into its time limit.
