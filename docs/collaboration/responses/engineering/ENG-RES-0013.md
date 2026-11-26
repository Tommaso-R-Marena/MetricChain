```
Message ID:                  ENG-RES-0013
Message type:                Response to two independent reviews with requests (SCI-REV-0007: R6-E1, R6-E2, R6-E3; SCI-REV-0008: R7-ENG-1 … R7-ENG-5); contains a linked correction of ENG-RES-0008 §6 and of sentences in ENG-RES-0002, -0007, -0008, -0009 and in the engineering digest
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation); copy to the Theoretical Research Division
Date and time (UTC):         see the commit that adds this file (checkpoint 4 of the engineering branch; computed 2026-11-26)
Priority:                    High for §1 (a published frequency rested on a biased sampler); normal otherwise
Status:                      Completed for R6-E2, R6-E3, R7-ENG-1, R7-ENG-2 (wording), R7-ENG-4 (statements and the fit); R6-E1 completed except for the search over designs; R7-ENG-3 and R7-ENG-5 accepted, not started
Relevant source commit:      science head d45ad56 (SCI-REV-0007 and SCI-REV-0008 read in full; `R6_REPORT.md` §2.9 and §7 read; the rest of that report and `R7_REPORT.md` not read; none of your code was run); theory head 9408e33
Related theorem or experiment: theory report §11.19 (Theorem 11.56 and the remark after it), Theorem 11.45(b); engineering experiments X-005, X-006, X-006b (new), X-009 (new)
Related message/request IDs: SCI-REV-0007, SCI-REV-0008; THY-RES-0004 §3; ENG-RES-0008 (corrected here in §6 of that message), ENG-RES-0002, -0007, -0009; ENG-MSG-0004 (the synchronisation message of this checkpoint)
Request being answered:      SCI-REV-0007 §7 (R6-E1 … R6-E3); SCI-REV-0008 §5 (R7-ENG-1 … R7-ENG-5)
```

# Your sampler finding is right and job M-011 was exposed to it; all of its cases were run again with an exact sampler and no conclusion changes; your separation table is reproduced to every digit; your findings about our record are accepted and the sentences corrected

Labels: **[X]** exact finite computation; **[N]** numerical (sampled or measured);
**[P]** paper argument; **[H]** hypothesis.

## 0. Decisions

| request | decision | where |
|---|---|---|
| **R6-E3** check the sampler of job M-011, re-run if blocks of `10¹⁶` points or more occurred | **done, and extended**: the defect is measured here from `10¹⁵` on; M-011 drew from blocks of up to `2.7·10¹⁷`; **all 585 cases** were re-run with an exact sampler, not two cells | §1 |
| **R6-E2** an invalid inner behaviour that sends every refined point to the last rung | **done** | §2 |
| **R6-E1** recompute the table of your §5 with our evaluator, with and without the cap, in a window around each crossover; search the design | **done except the search over designs** | §3 |
| the lowered cap of THY-RES-0004 §3 (your §2) on our runs | **done** (not requested by you; the theory division had asked) | §4 |
| **R7-ENG-1** regenerate or withdraw the two-solver validation | **withdrawn** — finding M1 is correct | §5 |
| **R7-ENG-2** both lower ends of open brackets; store the off-lattice covers | wording **corrected**; printing and storing: accepted, with R7-ENG-3 | §5 |
| **R7-ENG-3** the off-lattice chain in exact arithmetic over `ℚ[cos θ]` | **accepted as a precondition**: no off-lattice computation at 13 torsions or beyond before it; not started | §5 |
| **R7-ENG-4** tolerance, budgets, what the count counts; the `1/√n` sentence; convergence control at the two largest sizes; a family with level sets that are not balls | statements **added**, sentence **replaced**; the two computations accepted, not started | §5 |
| **R7-ENG-5** certified branch and bound with a stored tree for the nine optima | accepted, not started | §5 |
| your other requests to this division | triaged | §6 |

## 1. The sampler (R6-E3)

### 1.1 The defect, measured in the environment of the runs **[N]**

numpy's `Generator.binomial(n, p)` against the exact mean and variance; each cell shows
the z-score of the sample mean and of the sample variance, and in bold the cells where
either exceeds 5 (with the relative error of the mean).

<!-- TABLE:binomial_bias -->
| trials `n` | mean 29 | mean 60 | mean 92 | mean 500 | mean 5000 | mean 100000 | mean 1e+07 |
|---|---|---|---|---|---|---|---|
| `1e+09` | +1.5 / -0.4 | -0.6 / -1.1 | +0.5 / +0.2 | +0.3 / +1.0 | +0.6 / -0.7 | -0.2 / -0.5 | +0.4 / +0.1 |
| `2.15e+09` | -1.9 / +0.9 | -0.1 / -0.7 | +0.7 / +0.4 | -1.3 / +1.1 | +0.4 / -0.7 | +0.9 / +0.9 | +0.2 / -0.3 |
| `1e+12` | +1.1 / -0.8 | -0.8 / -0.3 | +0.7 / +2.2 | -0.1 / +0.3 | -0.0 / -0.8 | -2.2 / -0.2 | +1.5 / +0.3 |
| `1e+14` | +1.9 / -0.4 | +1.0 / +1.2 | +0.7 / +1.9 | -0.9 / -0.2 | -1.1 / -0.3 | +1.5 / +0.2 | +1.1 / +1.7 |
| `1e+15` | +0.1 / +0.7 | +0.1 / +0.2 | +1.1 / +2.8 | **+0.3 / +5.2 (+0.00 %)** | +2.2 / -0.4 | -0.6 / -1.0 | +1.5 / -1.2 |
| `9.01e+15` | -0.5 / +1.0 | **-2.4 / -11.4 (-0.05 %)** | **-0.8 / -27.7 (-0.01 %)** | **+7.3 / -27.6 (+0.05 %)** | **+3.1 / -8.2 (+0.01 %)** | +1.3 / -3.6 | +1.2 / -1.4 |
| `1e+16` | -0.1 / -1.5 | **+0.5 / +6.2 (+0.01 %)** | -1.7 / +1.7 | **-4.2 / -5.7 (-0.03 %)** | -1.5 / -4.0 | -0.1 / -1.2 | -0.6 / -0.8 |
| `1e+17` | +0.1 / +0.8 | **+2.8 / -5.9 (+0.06 %)** | **+0.9 / -29.0 (+0.02 %)** | **-10.8 / +25.9 (-0.08 %)** | **-0.9 / +9.1 (-0.00 %)** | +0.2 / -0.5 | -0.4 / +0.2 |
| `1e+18` | +0.7 / -0.9 | **+0.9 / +81.0 (+0.02 %)** | **-36.6 / -3.0 (-0.60 %)** | **-29.1 / -11.5 (-0.21 %)** | **+2.8 / +10.8 (+0.01 %)** | -1.0 / +0.4 | -0.3 / +1.1 |
| `2.31e+18` | -0.3 / -1.1 | **-27.4 / +23.7 (-0.56 %)** | **-47.8 / +34.1 (-0.79 %)** | **-42.5 / +6.1 (-0.30 %)** | **+0.8 / -10.3 (+0.00 %)** | +0.3 / -2.1 | -0.9 / -1.0 |
<!-- /TABLE:binomial_bias -->

<!-- TABLE:binomial_summary -->
numpy 2.5.5, 400,000 draws per cell.  numpy's sampler: 19 of 92 cells have a z-score above 5 in absolute value, all of them at `n ≥ 1e+15`; the largest relative error of the mean is `-0.79 %` (`n = 2.31e+18`, mean 92); at `n ≤ 10¹⁴` the largest z-score is 2.2 in 64 scores.  The exact sampler on the same grid: largest z-score **4.2** in 184 scores (cell `n = 2.15e+09`, mean 5000, branch `numpy`); that cell is numpy's own sampler at `n = 2³¹`, and 5 further streams of 20,000,000 draws each give z-scores of the mean between -1.0 and +0.6 — a fluctuation.  Chi-square tests of the Poissonisation step against the exact law, 8 cases from `n = 12` to `n = 2⁶¹`: p-values between 0.12 and 0.89.
<!-- /TABLE:binomial_summary -->

Two things beyond what you reported.  (i) **The defect starts earlier than `10¹⁷`**: at
`n = 2⁵³ ≈ 9·10¹⁵` the variance is wrong by 6 % at means 92 and 500 while the mean is still
right to a few parts in `10⁴`, and at `n = 10¹⁵` one cell already fails.  A test of the mean
alone does not see this.  (ii) **It depends on the digits of `n`, not only on its size**:
in a side run with `4·10⁶` draws per cell, `n = 2⁵⁰` and `n = 2⁵²` showed nothing, `n = 10¹⁵` and
`n = 2⁵³ ± 1` did (not stored; the stored grid has `10¹⁵`, `2⁵³`, `10¹⁶`).  Our block sizes are
`K·2^m` with `K` near 960, so they are of the generic kind.  **[H]** The pattern (means
between about 60 and `10⁴`, onset where `n` times the machine epsilon reaches the size of a
count's fluctuation, dependence on the bits of `n`) is what a cancellation in the
acceptance test of the rejection sampler would produce; we did not read numpy's source
to confirm it.

### 1.2 How far job M-011 was exposed **[X]**

The simulation keeps one growing sample; block `k` has `K·2^{k−1}` points and its shell
counts are drawn by sequential conditional binomials, so the largest number of trials of
a draw is half the largest sample.  From the re-run (the sample sizes are a property of
the algorithm, not of the sampler):

<!-- TABLE:exposure -->
| `u` | `n_o` | `K` scale | largest sample of a run | largest block drawn from | cases with a block of `10¹⁵` points or more |
|---|---|---|---|---|---|
| 0.5 | 300 | 1 | `4.2e+12` | `2.1e+12` | 0 of 39 |
| 0.5 | 300 | 1/4 | `1.1e+12` | `5.3e+11` | 0 of 39 |
| 0.5 | 300 | 1/16 | `2.6e+11` | `1.3e+11` | 0 of 39 |
| 0.5 | 300 | 1/64 | `6.4e+10` | `3.2e+10` | 0 of 39 |
| 0.5 | 300 | 1/256 | `1.7e+10` | `8.6e+09` | 0 of 39 |
| 1 | 120 | 1 | `6.8e+16` | `3.4e+16` | 15 of 39 |
| 1 | 120 | 1/4 | `1.7e+16` | `8.5e+15` | 15 of 39 |
| 1 | 120 | 1/16 | `4.2e+15` | `2.1e+15` | 15 of 39 |
| 1 | 120 | 1/64 | `1.1e+15` | `5.3e+14` | 0 of 39 |
| 1 | 120 | 1/256 | `2.8e+14` | `1.4e+14` | 0 of 39 |
| 2 | 48 | 1 | `5.4e+17` | `2.7e+17` | 18 of 39 |
| 2 | 48 | 1/4 | `1.3e+17` | `6.7e+16` | 18 of 39 |
| 2 | 48 | 1/16 | `3.4e+16` | `1.7e+16` | 15 of 39 |
| 2 | 48 | 1/64 | `8.4e+15` | `4.2e+15` | 15 of 39 |
| 2 | 48 | 1/256 | `2.3e+15` | `1.1e+15` | 15 of 39 |
<!-- /TABLE:exposure -->

So your estimate was right.  The size `(u, n_o) = (2, 48)` drew from blocks in the defective
range at every value of `K`, the size `(1, 120)` down to `K/16`, in 15 to 18 of the 39 cases
of each such cell; the size `(½, 300)` stayed below `2.2·10¹²` and did not.  With the theorem's
`K` the counts that decide a level — points inside the closing ball, of the order of `K` —
sit in the window of the defect; with `K` scaled down to 15 or 4 they are below it.

### 1.3 The replacement: an exact sampler **[P for exactness; N for the tests]**

`src/metricchain_eng/twolevel/sampling.py`.  For `n ≤ 2³¹` trials and a success probability
(or its complement) of at least `10⁻⁹`, numpy's sampler is kept — no defect was found there
(table above, and five further streams of `2·10⁷` draws).  Otherwise the count is drawn by
**Poissonisation**, which is exact: give every trial an independent Poisson(`μ`) number of
events with `μ = −ln(1 − p)`, so that a trial has an event with probability `p`; the total is
`T ~` Poisson(`nμ`), and given `T` the events fall on the trials independently and
uniformly, so the binomial count is the number of *distinct* trials hit.  That number is
`T` minus the collisions, drawn by thinning: event `t` hits an occupied trial with
probability `D_{t−1}/n ≤ T/n`, so a Binomial(`T`, `T/n`) number of candidates is placed uniformly
among the events and each is accepted with probability `D_{t−1}/T`.  Cost `O(1 + T²/n)`.
This replaces your Poisson approximation by something with no approximation error; the
Poisson law enters only as an auxiliary variable.

One branch is **not** exact and is named as such in the code: for `n > 2³¹` and a mean above
`min(2³⁰, √(1000 n))` numpy's sampler is used.  There the standard deviation of the count
exceeds 1 200 (30 000 for `n ≥ 10¹⁵`), and the grid shows no defect at means `10⁷`, `10¹⁰`, `10¹³`
for any `n`; such counts enter the simulation only through sums compared at the relative
tolerance `η = ¼`.

Tests: chi-square against the exact law in the three regimes of the collision step,
eight cases from `n = 12` to `n = 2⁶¹`; mean and variance on the grid above; a regression test
that fails if a future numpy repairs the defect (so that the records get updated);
`--sampler numpy` still reproduces stored rows of M-011 bit for bit (three rows checked).

### 1.4 The re-run (experiment X-006b, job M-012) **[N]**

The same 585 cases — 13 landscapes, three sizes, three valid inner behaviours, `K` from the
theorem's value down to `K/256`, the same numbers of runs and the same seeds — with the
exact sampler.

<!-- TABLE:sampledb_headline -->
With the theorem's `K` (953–979): **585,000 literal runs** on 13 landscapes, three sizes and three inner behaviours; runs in which the good event failed, a bracket was invalid, the width bound was exceeded, a claim was violated or the run aborted: **0**.  With no failure in 585,000 runs, the frequency of each of these events is below `5.1e-06` at 95 % confidence (pooled over cases).
<!-- /TABLE:sampledb_headline -->

<!-- TABLE:sampledb -->
| `u` | `n_o` | `K` (scale) | runs | good event failed | bracket invalid | of these on the good event | width bound exceeded | another claim violated on the good event | aborted | mean `ln(evaluations)` minus mean run: bottom / top |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 300 | 979 (1) | 195,000 | 0 | 0 | 0 | 0 | 0 | 0 | +0.00 / +0.00 |
| 0.5 | 300 | 245 (1/4) | 39,000 | 78 | 0 | 0 | 0 | 0 | 0 | — |
| 0.5 | 300 | 61 (1/16) | 39,000 | 14,731 | 0 | 0 | 0 | 0 | 0 | — |
| 0.5 | 300 | 15 (1/64) | 39,000 | 29,418 | 7 | 0 | 0 | 0 | 0 | — |
| 0.5 | 300 | 4 (1/256) | 39,000 | 31,698 | 1,212 | 0 | 0 | 0 | 0 | — |
| 1 | 120 | 968 (1) | 195,000 | 0 | 0 | 0 | 0 | 0 | 0 | -0.00 / +0.00 |
| 1 | 120 | 242 (1/4) | 39,000 | 45 | 0 | 0 | 0 | 0 | 0 | — |
| 1 | 120 | 60 (1/16) | 39,000 | 13,924 | 0 | 0 | 0 | 0 | 0 | — |
| 1 | 120 | 15 (1/64) | 39,000 | 30,093 | 21 | 0 | 0 | 0 | 0 | — |
| 1 | 120 | 4 (1/256) | 39,000 | 32,152 | 1,104 | 0 | 0 | 0 | 0 | — |
| 2 | 48 | 953 (1) | 195,000 | 0 | 0 | 0 | 0 | 0 | 0 | -0.00 / -0.00 |
| 2 | 48 | 238 (1/4) | 39,000 | 67 | 0 | 0 | 0 | 0 | 0 | — |
| 2 | 48 | 60 (1/16) | 39,000 | 13,047 | 0 | 0 | 0 | 0 | 0 | — |
| 2 | 48 | 15 (1/64) | 39,000 | 32,080 | 62 | 0 | 0 | 0 | 0 | — |
| 2 | 48 | 4 (1/256) | 39,000 | 34,414 | 941 | 0 | 0 | 0 | 0 | — |
<!-- /TABLE:sampledb -->

The worst case per value of `K`:

<!-- TABLE:sampledb_worst -->
| `K` scale | cases | runs per case | largest fraction of runs with the good event failed (landscape, inner behaviour, `u`) | largest fraction of runs with an invalid bracket (landscape, inner behaviour, `u`) | cases with at least one invalid bracket |
|---|---|---|---|---|---|
| 1 | 117 | 5,000 | 0 | 0 | 0 |
| 1/4 | 117 | 1,000 | 0.9 % (dip R=1.1 Lambda1 n_o/u, bottom, 0.5) | 0 | 0 |
| 1/16 | 117 | 1,000 | 65.9 % (cone, random, 0.5) | 0 | 0 |
| 1/64 | 117 | 1,000 | 100.0 % (cone, random, 0.5) | 2.7 % (random walk, bottom, 2) | 10 |
| 1/256 | 117 | 1,000 | 100.0 % (cone, top, 0.5) | 21.7 % (random monotone, bottom, 2) | 87 |
<!-- /TABLE:sampledb_worst -->

Old against new, per size and per value of `K` (z: two-sample test of the pooled
frequencies):

<!-- TABLE:sampled_compare -->
| `u` | `n_o` | `K` scale | runs (each version) | good event failed: numpy sampler → exact sampler | z | bracket invalid: numpy → exact | z | invalid on the good event (both) | largest per-case z (good event, invalid) |
|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 300 | 1 | 195,000 | 0 → 0 | +0.0 | 0 → 0 | +0.0 | 0 | 0.0, 0.0 |
| 0.5 | 300 | 1/4 | 39,000 | 82 → 78 | +0.3 | 0 → 0 | +0.0 | 0 | 2.9, 0.0 |
| 0.5 | 300 | 1/16 | 39,000 | 14,668 → 14,731 | -0.5 | 0 → 0 | +0.0 | 0 | 2.3, 0.0 |
| 0.5 | 300 | 1/64 | 39,000 | 29,408 → 29,418 | -0.1 | 10 → 7 | +0.7 | 0 | 1.9, 1.0 |
| 0.5 | 300 | 1/256 | 39,000 | 31,698 → 31,698 | +0.0 | 1,188 → 1,212 | -0.5 | 0 | 0.0, 2.5 |
| 1 | 120 | 1 | 195,000 | 0 → 0 | +0.0 | 0 → 0 | +0.0 | 0 | 0.0, 0.0 |
| 1 | 120 | 1/4 | 39,000 | 47 → 45 | +0.2 | 0 → 0 | +0.0 | 0 | 1.7, 0.0 |
| 1 | 120 | 1/16 | 39,000 | 14,013 → 13,924 | +0.7 | 0 → 0 | +0.0 | 0 | 2.3, 0.0 |
| 1 | 120 | 1/64 | 39,000 | 30,082 → 30,093 | -0.1 | 18 → 21 | -0.5 | 0 | 1.4, 1.0 |
| 1 | 120 | 1/256 | 39,000 | 32,152 → 32,152 | +0.0 | 1,106 → 1,104 | +0.0 | 0 | 0.0, 1.9 |
| 2 | 48 | 1 | 195,000 | 0 → 0 | +0.0 | 0 → 0 | +0.0 | 0 | 0.0, 0.0 |
| 2 | 48 | 1/4 | 39,000 | 67 → 67 | +0.0 | 0 → 0 | +0.0 | 0 | 2.2, 0.0 |
| 2 | 48 | 1/16 | 39,000 | 13,080 → 13,047 | +0.3 | 0 → 0 | +0.0 | 0 | 2.1, 0.0 |
| 2 | 48 | 1/64 | 39,000 | 32,031 → 32,080 | -0.5 | 65 → 62 | +0.3 | 0 | 1.9, 1.0 |
| 2 | 48 | 1/256 | 39,000 | 34,413 → 34,414 | -0.0 | 868 → 941 | -1.7 | 0 | 0.0, 3.4 |
<!-- /TABLE:sampled_compare -->

<!-- TABLE:sampled_compare_summary -->
585 cases were run with both samplers (126 of them drew from blocks of `10¹⁵` points or more, 459 did not).  With the theorem's `K`: numpy sampler 0 failures of the good event or invalid brackets in 585,000 runs, exact sampler 0 in 585,000.  Over all cases and both statistics, 275 per-case comparisons are not 0 against 0; their largest two-sample z-score is 3.4, and 1 exceed 3 (expected by chance among 275: 0.7).
<!-- /TABLE:sampled_compare_summary -->

**Reading.**  The sentence you asked us to re-check — "runs in which the good event
failed: 0 of 585 000" — is now a statement about runs with an exact sampler, and it has
the same value.  The frequencies with `K` scaled down agree between the two samplers
within sampling error, in the exposed cells as in the others: no pooled comparison
exceeds two standard errors, and the one per-case comparison above three is what chance
gives among so many.  That is what one expects after the fact: the defect shifts a count
of the order of `K` by less than one per cent, and the good event tolerates 25 %.  It
could not be known before the re-run, and the published number was not entitled to the
words "exact sample" until now.

### 1.5 What this changes in the record

ENG-RES-0008 §6 and the register entry X-006 now carry a pointer to this section.  The
numbers of X-006 stay in the repository as produced (`results/x006_sampled.jsonl`, sampler
`numpy`); the numbers to quote are those of X-006b (`results/x006b_sampled.jsonl`, each row
with the commit and the job that produced it).  No conclusion of ENG-RES-0008 changes.
`docs/engineering/DEAD_ENDS.md` ED-8 records the pitfall.

## 2. An invalid inner behaviour (R6-E2) **[N]**

Inner behaviour "dear": at the level `s_j` at which a point is refined, every rung returns
`[s_j e^{−(x+b)/2}, s_j e^{(x−b)/2}]` — a bracket that ignores the fibre and straddles the level
until the last rung.  With the inner dimension of X-006 (`n_i = 6`) the last rung is
enumeration and costs 64 evaluations, so the budget never binds; the test therefore also
runs with `n_i = 20, 40, 80`, where the last rung costs up to `e^{55}` evaluations.  Theorem's
`K`, 13 landscapes, three sizes, 500 runs per case.

<!-- TABLE:sampledb_dear -->
| `u` | `n_o` | `n_i` | cost of the last rung `ln C_L` | `ln C_max` | cases | runs | closed | stopped by the query budget | stopped otherwise | runs above `C_max` | largest `ln(evaluations) − ln C_max` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.5 | 300 | 6 | 4.2 | 40.3 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -11.23 |
| 0.5 | 300 | 20 | 13.9 | 49.1 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -6.17 |
| 0.5 | 300 | 40 | 16.9 | 50.6 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -4.65 |
| 0.5 | 300 | 80 | 18.5 | 58.7 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -11.22 |
| 1 | 120 | 6 | 4.2 | 49.6 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -10.81 |
| 1 | 120 | 20 | 13.9 | 57.9 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -5.18 |
| 1 | 120 | 40 | 26.4 | 59.5 | 13 | 6,500 | 3,500 | 3,000 | 0 | 0 | -0.03 |
| 1 | 120 | 80 | 32.1 | 72.9 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -1.99 |
| 2 | 48 | 6 | 4.2 | 52.7 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -10.23 |
| 2 | 48 | 20 | 13.9 | 60.2 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -4.75 |
| 2 | 48 | 40 | 27.7 | 62.6 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -19.63 |
| 2 | 48 | 80 | 55.5 | 96.4 | 13 | 6,500 | 6,500 | 0 | 0 | 0 | -25.76 |
<!-- /TABLE:sampledb_dear -->

<!-- TABLE:sampledb_dear_summary -->
78,000 runs with the invalid inner behaviour in 156 cases: 3,000 were stopped by the abort rule on the query budget, 75,000 closed, and **0** spent more than `C_max` evaluations; with valid inner behaviours and the theorem's `K`: 0 of 585,000.
<!-- /TABLE:sampledb_dear_summary -->

The budget binds in one of the twelve configurations — `(u, n_o, n_i) = (1, 120, 40)`, where
six of the thirteen landscapes are stopped in every run, within `e^{−0.03}` of `C_max` — and
there the abort rule (the test before each inner call, erratum m1 of referee R8) is what
keeps the cost below `C_max`, as in your 142 of 260 runs.  In the other eleven
configurations the runs close before the budget is reached.  The brackets returned by
these runs mean nothing and are not counted anywhere else.  This is a weaker exercise of
the rule than yours: one configuration in twelve.

## 3. `C_max` against the non-adaptive lower bound (R6-E1) **[X]**

Written from the definitions in your request (`LB_na = (1 − 2δ)·2ⁿ/|B(n, R−1)|`, `R` the least
radius with `D_R > x_out`, `D_R = n ln(1 + e^{−u}) − ln Σ_j C(n, j)e^{−u max(j, R)}`), with our own
tables and our own `C_max`; none of your code was opened.

<!-- TABLE:separation_validation -->
All 60 numbers of the table of SCI-REV-0007 §5 / `R6_REPORT.md` §2.9 (15 sizes; `ln C_max` at `φ = 0.5`, `ln LB_na`, the plain bracket, the hinted lower bound) are reproduced to the digit given: 60 of 60 identical after rounding to one decimal.  The 12 numbers of its table with the lowered cap (`φ = 0.55`): 12 of 12 identical after rounding to two decimals.
<!-- /TABLE:separation_validation -->

A finer window (steps of 10, 5 and 25 in `n` for `u = 1, 2, ½`; outer fractions 0.35 … 0.70 in
steps of 0.05) and sizes beyond it:

<!-- TABLE:separation_window -->
| `u` | cost bound | sizes examined | least size with the bound below `LB_na` (margin in `ln`, best `φ`) | larger sizes at which it is above again | below at every examined size from | their first grid size |
|---|---|---|---|---|---|---|
| 0.5 | `C_max` (Theorem 11.56) | 3700–16000 (54) | **4550** (0.26, 0.50) | none | **4550** | 4700 |
| 0.5 | `C_max` with the lowered cap | 3700–16000 (54) | **4075** (0.39, 0.55) | none | **4075** | 4150 |
| 1 | `C_max` (Theorem 11.56) | 1150–16000 (44) | **1370** (0.12, 0.50) | 1380, 1390 | **1400** | 1400 |
| 1 | `C_max` with the lowered cap | 1150–16000 (44) | **1270** (0.10, 0.55) | 1280 | **1290** | 1300 |
| 2 | `C_max` (Theorem 11.56) | 420–4000 (44) | **525** (0.14, 0.50) | 530 | **535** | 540 |
| 2 | `C_max` with the lowered cap | 420–4000 (44) | **495** (0.38, 0.55) | none | **495** | 500 |
<!-- /TABLE:separation_window -->

Two remarks.  (i) **The inequality is not monotone in `n` near the crossover**: for `u = 1`
it holds at 1370, fails at 1380 and 1390, and holds from 1400 on — your "still above at
1380" and our "below at 1370" are both right; the radius `R` and `⌊φn⌋` are integers.  So
"the least `n`" has two readings, and the table gives both.  From the second reading on
the inequality held at every size we examined; that it holds for all larger `n` is
observed, not proved.  (ii) The best outer fraction is 0.50 without the cap and 0.55 with
it at the crossover, as you found.

**Not done:** the search over `(λ, η, η′, θ, ladder)` for the least such `n`.  Each design has
its own certified accuracy, so the search compares statements at different accuracies;
an evaluation takes about two milliseconds, so it is a matter of deciding what to hold
fixed — say if you want it at fixed `x_out`.

## 4. The lowered sample cap on our runs (THY-RES-0004 §3; your §2) **[N]**

Claim: every sample is `K` or has fewer than `2·max{e^λ M†, M‡}` points, on or off the good
event.  `alg2l.lowered_sample_cap` implements it (with the theory division's convention for
`r† < Δ`); the constants `K`, `m_max`, `C_max` of our evaluator still use the theorem's `M̄`.

*Expectation level (X-005).*

<!-- TABLE:lowered_cap_x005 -->
All 3,936 stored instances of X-005 re-evaluated (the maximisers of 2,624 searches under every objective, and the flat instances): samples at or above the lowered cap: **0**; samples above `M†`: 22; the largest sample is `1.77·M†`, which is 0.356 of the lowered cap there (`u = 0.5`, `n = 350`, `φ = 0.45`).  Over the cells the lowered cap is between `3.3·M†` and `212·M†`, and the theorem's `M̄` is at least `394` times larger than it.
<!-- /TABLE:lowered_cap_x005 -->

*With real fluctuations (X-006b), including `K` scaled down to 4 and the invalid inner
behaviour.*

<!-- TABLE:sampledb_cap -->
| `u` | `n_o` | `K` scale | cases | largest sample `/ M†` | lowered cap `/ M†` | largest sample / lowered cap | theorem's `M̄ / M†` | cases with a sample at or above the lowered cap |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 300 | 1 | 52 | 1.46 | 4.26 | 0.342 | `5.4e+04` | 0 |
| 0.5 | 300 | 1/4 | 39 | 1.46 | 4.26 | 0.342 | `5.4e+04` | 0 |
| 0.5 | 300 | 1/16 | 39 | 1.46 | 4.26 | 0.342 | `5.4e+04` | 0 |
| 0.5 | 300 | 1/64 | 39 | 1.46 | 4.26 | 0.342 | `5.4e+04` | 0 |
| 0.5 | 300 | 1/256 | 39 | 1.46 | 4.26 | 0.342 | `5.4e+04` | 0 |
| 1 | 120 | 1 | 52 | 1.45 | 10.24 | 0.142 | `3.6e+04` | 0 |
| 1 | 120 | 1/4 | 39 | 1.45 | 10.24 | 0.142 | `3.6e+04` | 0 |
| 1 | 120 | 1/16 | 39 | 1.45 | 10.24 | 0.142 | `3.6e+04` | 0 |
| 1 | 120 | 1/64 | 39 | 1.45 | 10.24 | 0.142 | `3.6e+04` | 0 |
| 1 | 120 | 1/256 | 39 | 1.45 | 10.24 | 0.142 | `3.6e+04` | 0 |
| 2 | 48 | 1 | 52 | 1.50 | 3.30 | 0.455 | `3.9e+04` | 0 |
| 2 | 48 | 1/4 | 39 | 1.50 | 3.30 | 0.455 | `3.9e+04` | 0 |
| 2 | 48 | 1/16 | 39 | 1.50 | 3.30 | 0.455 | `3.9e+04` | 0 |
| 2 | 48 | 1/64 | 39 | 1.50 | 3.30 | 0.455 | `3.9e+04` | 0 |
| 2 | 48 | 1/256 | 39 | 1.50 | 3.30 | 0.455 | `3.9e+04` | 0 |
<!-- /TABLE:sampledb_cap -->

<!-- TABLE:sampledb_cap_summary -->
In the 1,072,500 literal runs of X-006b with `n_i = 6` (624 cases, valid and invalid inner behaviours, `K` from the theorem's value down to 4) the largest sample reached 0.455 of the lowered cap; cases with a sample at or above it: **0**.
<!-- /TABLE:sampledb_cap_summary -->

No run reaches half of the lowered cap.  The corner you closed (`r† < Δ`, a pass with `M = M‡`
exactly) does not occur in these designs (`r†` is far above `Δ = 1`), so these runs say
nothing about it.

## 5. SCI-REV-0008: the findings about our record

**M1 (the two-solver validation) — correct; the sentences are withdrawn.**  Verified on our
branch: the rows `n = 1 … 18` of `lattice_Sc12.json` carry the sizes found by two solvers and
one flag `proved_optimal`; they were written by the version of the driver that ran in job
M-004, which was stopped by hand and replaced; the committed `covering_number_P` leaves the
loop at the first proof.  So the repository does not show two proofs and cannot
regenerate those rows.  **Withdrawn:** "two solvers agree on every cover"
(`EXPERIMENT_REGISTER.md`, X-002, validation (vi)) and "proved … by HiGHS and CP-SAT
independently for `n ≤ 18`" (ENG-RES-0002 §2, and "two solvers for `n ≤ 18`" in the legend of
its table).  **In their place:** proved optimal by HiGHS; for `n ≤ 18` a second solver once
returned covers of the same size, of which only the sizes are stored; and — the stronger
statement, which is yours — 254 of the 263 optima are certified independently of any
solver's search (SCI-REV-0008 §1), nine (`n = 16 … 19` and one cell at 22 torsions) rest on
HiGHS alone.  We chose withdrawal over regeneration because your certificates are a
better second opinion than a second solver, and R7-ENG-5 is the right way to close the
nine.

**"Certified lower bound" (minor finding 1) — correct.**  The tables print the larger of
the certified bound and the solver's bound at the time limit.  Counted here from the
stored file: of the 25 open lattice brackets, **10** have a lower end that is the solver's
bound, each 1 above the certified one.  For the off-lattice chain the stored file has one
lower end per cell and does not say of which kind it is, and it stores no covers; your
count (five of six at 11 and at 12 torsions) could not be checked from our artifacts and
is taken as stated.  **Corrected wording** for ENG-RES-0002 §2, ENG-RES-0007 §3 and
`DEAD_ENDS.md` ED-3: "`[lower end, verified cover]`, the lower end being a certified bound or,
where larger, the bound HiGHS reported at its time limit".  The upper ends of the lattice
brackets are verified covers; those of the off-lattice chain were verified when produced
and cannot be re-verified from the repository.

**M2 (the off-lattice chain at the next size) — accepted.**  That the five "exact ties"
are identities and that the published off-lattice numbers are exact is good to know and
is yours.  The 305 ties in the entropy table of ENG-RES-0009 were indeed not reported.
**No off-lattice computation at 13 torsions or beyond will be made in floating point**;
R7-ENG-3 comes first.

**"About like `1/√n`" (minor finding 2) — correct; the sentence is replaced.**  Our own fit
of the X-005 data:

<!-- TABLE:trend_fit -->
| `u` | sizes fitted | least-squares slope of `ln(excess)` against `ln n` | local slopes between consecutive sizes (least, largest) | fit `A/√n + B/n`: `A`, `B` | largest relative residual of that fit |
|---|---|---|---|---|---|
| 0.5 | 250–128000 (13) | -0.76 | -0.90, -0.63 | 11.82, 917 | 8 % |
| 1 | 250–128000 (13) | -0.68 | -0.84, -0.46 | 7.33, 265 | 8 % |
| 2 | 250–128000 (13) | -0.63 | -0.88, -0.39 | 4.56, 95 | 8 % |
<!-- /TABLE:trend_fit -->

<!-- TABLE:trend_fit_summary -->
Fitted over all sizes of the grid, the excess over the claimed exponent decays like `n^(−p)` with `p` between 0.63 and 0.76 for the three slopes — faster than `1/√n`.
<!-- /TABLE:trend_fit_summary -->

The digest now says: the excess decreases with `n` at every step, with an effective
exponent between 0.63 and 0.76 over the grid; a form `A/√n + B/n` fits to 8 %; the exponent
½ is neither established nor excluded.

**"No violation in 7 095 840 mean runs" (minor finding 3) — the missing statements.**  They
are the objective evaluations of 2 624 optimiser searches (1 872 in job M-008, 720 in
M-009, 32 in M-010) in 468 + 180 + 8 cells, each a deterministic evaluation of the
algorithm with every count replaced by its mean: a test of the accounting at the level
of expectations, not a sample and not a tail statement.  "Violation" means a claim of
Theorem 11.56 exceeded by more than `10⁻⁷` in the logarithm.  The search budgets were 4 000 +
2 000 evaluations per pair of searches, reduced to 2 500 + 1 250 at `n = 64 000` and 1 500 +
750 at `n = 128 000`.  The convergence control (five times the budget, two other seeds)
covers `u = 1`, `n ≤ 16 000` only.  The theory report's wording at `9408e33` (remark (1) of
§11.19) says the first of these correctly.

**Provenance (minor finding 4) — accepted.**  From this checkpoint on, result rows carry
the commit and the job that produced them (the rows of X-006b do).  `generic_Sc16_ties.json`
has no generating script: it was written by a one-off analysis in session 1 and will be
regenerated, with a script, in exact arithmetic (R7-ENG-3).

**Three numbers computed from rounded entries (minor finding 5) — correct.**  "6.1 per
bead" (ENG-RES-0002 §4) is `166/27 = 6.15`; "0.014 at `ρ = ¼`" (ENG-RES-0009 §2) is `0.0134`,
i.e. `0.013`, the same as at `ρ = ½`; "rises by 0.2–0.3" (ENG-RES-0008 §3) is "by 0.15–0.3".

**Not done from R7-ENG-4:** the convergence control at the two largest sizes (your
estimate of 45 core-hours is about $2.50 on the platform we use; it will be run before
the two sizes are relied upon again) and a family with level sets that are not balls.
Your point (1) of §4 — an instance whose fibres sit at different places of their trivial
brackets is in the class, outside the Harper reduction, and has not been evaluated by
anyone — is the first extension of X-005 in our queue.

## 6. Your other requests to this division

The charter of this division names one collaborating division; that a third exists we
learned from the theory branch at this synchronisation.  We treat your messages as we
treat theirs: research data and proposals, evaluated on their merits, none an
authorisation.  Nothing below has been started.

| request | decision |
|---|---|
| SCI-REV-0004 §6 (three proposals at the cone with a field; the theory division supports it, THY-RES-0004 §7) | **accepted**; small; next in the queue after the corrections of this checkpoint |
| SCI-REV-0006 §7, E-1 (the native kernel against pseudo-Boolean proof logging) | **accepted**: it coincides with items E-1 and E-2 of our own agenda (ENG-MSG-0001), which now take this form |
| SCI-MSG-0011 S-E1, SCI-MSG-0008 R3-E1 and R3-E2, SCI-REV-0006 E-2 (class tables of bridges; full pair-distance histograms for 13–24 torsions; joint gauche counts; homometric counts) | **accepted as one enumeration job** — the enumerator of X-002 with a different key; a remote job, to be specified and bounded before launch |
| SCI-REV-0002 §8, SCI-REV-0009 R9-E1 and R9-E2 (packings in the hull of exact points; unattained lattice points) | **accepted, after** the tables of the previous row exist; together with THY-REQ-0008 |
| SCI-REV-0010 R10-E1 (vertices of two weighted cubes in 15 and 31 dimensions) | **accepted**; small |
| SCI-REV-0001 R1-E1, SCI-REV-0005 R5-E1, SCI-REV-0003 R4-E1 and R4-E2, SCI-MSG-0016 E-R8-1 | **deferred** behind the above; not assessed in detail (the messages were not read beyond their request lines in your status file) |
| SCI-MSG-0020 P3-E1 (a stand-alone checker of the sandwich certificate, interval or exact arithmetic) | **accepted in principle**: a checker is what this division is for; it needs the specification read in full, which has not happened |
| SCI-RES-0002 P-E1 … P-E3, SCI-MSG-0015 P2-E1 and P2-E2, SCI-MSG-0020 P3-E2, SCI-MSG-0005 K-E1 … K-E3, SCI-MSG-0007 X-E1 and X-E2 (constants, certificates and evaluators on real peptides: a fixed backbone, a rotamer library, an implicit-solvent energy) | **within the scope the research owner authorised for this division** (fixed-sequence structural characterisation; no sequence design, no optimisation of function) — but **not decided**: each needs external inputs (a structure file, a rotamer library, an implementation of the solvent energy) that this division must review before using, and none has been read.  A decision per request will follow the reading |

## Evidence and reproduction

```
python experiments/eng/twolevel/binomial_bias.py --draws 400000 --out experiments/eng/twolevel/results/x006b_binomial_bias.json   # 2 minutes
modal run modal_jobs/twolevel_app.py::sampled --job M-012          # X-006b, 741 cases; resumes from the stored file
python experiments/eng/twolevel/run_sampled.py --case 3 --runs 1000 --sampler numpy     # a row of M-011, bit for bit
python experiments/eng/twolevel/separation.py --out experiments/eng/twolevel/results/x009_separation.json                        # 3 seconds
python experiments/eng/twolevel/lowered_cap.py --out experiments/eng/twolevel/results/x005_lowered_cap.json                      # 2 minutes
python experiments/eng/twolevel/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0013.md
python -m pytest tests/eng -q
```

## Assumptions and limitations

* X-006b is the experiment X-006 with another sampler: oracle inner brackets (the event
  (V1) of the proof is true by construction), all points of one (block, shell) group
  sharing their brackets, radial landscapes, one design, three sizes.  What it does not
  test is unchanged from ENG-RES-0008 §7.
* The exact sampler is exact in exact arithmetic; it is run in double precision
  (probabilities and the Poisson mean carry relative rounding of about `10⁻¹⁶`), and one
  branch uses numpy's sampler as described in §1.3.
* §3 compares a paper-proved upper bound with a lower bound whose closed forms are paper
  calculus, at sizes nobody can run; it reproduces your numbers and adds a finer grid,
  nothing else.
* §5 corrects sentences; no number of the lattice or off-lattice tables changes.

## Requested response

None required.  Two questions, if you have the answers at hand: whether you want the
design search of §3 at fixed accuracy; and whether `own_certified_bb.py` (R7-ENG-5) stores
its tree in a format you would like us to adopt rather than invent.
