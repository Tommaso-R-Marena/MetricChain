# Phase II validation campaign (Workstream D): report

*Carried out by a subagent of the Computational Research Division on branch `research/phase2-certified-inference`
(library as of commit `bf7b71a`), following `docs/engineering/phase2/PROTOCOL.md` (not edited).  Every number
below is produced by `make_tables.py` from the files in `results/`; nothing is typed by hand.  Prose is limited
to definitions and to what was done.*

## 1. Bugs found in the library

No unsound step found.  One defect of the optimiser, not of soundness:

* **`tau_grad` returns NaN in the model-free case** (`Lw = 0`, no exact part `b`): at the root no point has
  `s > 0`, the extremal weights are all zero and the gradient is 0/0 (`core.py`, `tau_grad`, last line).  Reproduction:
  `bugs/tau_grad_nan_modelfree.py` (exits 1).  Effect: the L-BFGS-B stages of `solve_upper(..., "descent")` get NaN
  gradients for `l ≡ 0` with a non-box region; Nelder–Mead still runs and the returned end is still certified
  (`tau_root` at any `η`), but it can be wider than the exact end.  Affected here: B3 on F3 (ellipsoid) only;
  B3 on F1, F2, F4 and F6 use the linear programme.

**Library change during the campaign.**  The coordinator changed `src/metricchain_eng/certinf/` (uncommitted;
modification time 02:35:33 UTC on 28 Nov) after an independent referee's findings, among them this defect.  Per the
coordinator's notice, the change leaves `certify_upper`, `certify_lower`, `s3_interval`, `interval()` on box regions
and for l > 0, and `certify_upper_gap` under the default declaration numerically unchanged for valid input; it
changes `tau_grad` (no NaN for l = 0), `solve_upper('auto')` (descent followed by cutting planes for model-free
problems on non-box regions or with more than 20 000 points) and `certify_inconsistent` (abstains when L = 0 at every
validation draw; certifies deterministically when the declared range of φ excludes the region).  Consequences here:
every B3 value on F3 was recomputed with the changed library on the same draws (`rerun_b3_f3.py`); the pre-fix
values are kept in `results/superseded/B3_F3_pre_fix.jsonl`, marked superseded; both are compared in §4.14, and
H-F(iii) is decided on the recomputed values.  No other finished cell was rerun.  No cell of run (c) is model-free
(L = e^{−ρ} > 0 at every draw), so the abstention rule of `certify_inconsistent` cannot apply there; run (c)
was produced before the change, runs (a), (b), (d) after it.  Which file was produced before or after:

<!-- GEN:provenance -->
| result files | produced by | process start (UTC) | relative to the library change |
|---|---|---|---|
| results/validation/*.jsonl except F3_B3_recomputed.jsonl | run_validation.py grid (two invocations; the second resumed) | 2026-11-28 00:55:39 and 01:08:26 | before |
| results/sens_c.jsonl, sens_c_exact.json | run_sensitivity.py c | 2026-11-28 02:34:28 | before |
| results/sens_a.jsonl, sens_b.jsonl, sens_d.jsonl | run_sensitivity.py a, b, d | after 02:47 (see results/run_starts.txt) | after |
| results/contexts.json, structure.json, memory.jsonl | run_validation.py --contexts / --memory, run_structure.py | after the sensitivity runs (see results/run_starts.txt) | after |
| results/validation/F3_B3_recomputed.jsonl | rerun_b3_f3.py | after the above | after |
| results/superseded/B3_F3_pre_fix.jsonl | the grid's B3 rows on F3, moved there by rerun_b3_f3.py | 2026-11-28 00:55-02:34 | after |
<!-- /GEN:provenance -->

**Exact references are floating point.**  The "exact" intervals (M0, F4 by level counts, F5 by the programme and by
Corollary 9.3, F6) are double-precision results of linear programmes (HiGHS) or of the descent route, not interval
arithmetic; their agreement checks are in §4.1, §4.11, §4.12, §4.13.

## 2. Deviations from the protocol

| # | protocol | done instead | reason |
|---|---|---|---|
| D1 | 200 repetitions (50 at n = 10⁵) | 100 at n = 10³ and 10⁴, 30 at n = 10⁵ (the minimum allowed by the brief) | runtime: the training dual of M3/M4 is a linear programme on 5000 draws (about 0.8 s each, two per method and repetition) |
| D2 | B1 in every cell | B1 at n = 10³ only, on F1 and F2 (every envelope) and on one F3 cell (`stress`, Γ = 10); not run on F4 | runtime: 200 bootstrap resamples × 2 ends per repetition; on F3 (ellipsoid: descent) 10–17 s per repetition, on F4 up to 70 s.  H-F(i) needs only n = 10³ |
| D3 | B3 in every cell | on F3 only for `stress` at n = 10³ and Γ ≤ 10 | runtime (descent on the model-free problem, 4–5 s per repetition); H-F(iii) concerns Γ ≤ 10 |
| D4 | timing split preprocessing / sampling / optimisation / certification | `certify_upper`/`certify_lower` do optimisation and certification in one call; the optimisation alone was timed by a second, identical `solve_upper` call on the first 5 repetitions of each cell (certification = total − that); for M4, M5, M6, B1–B3 only the time after sampling is recorded (in one column) | the library does not expose the split |
| D5 | sensitivity runs: sizes not fixed | (a) F1 `nnn_corr`, F2, F3 `stress`; declared ρ ∈ {0.2, 0.55, 1.15}, true R = 2ρ·r; n = 10⁴; 50 reps.  (b) F1 `nnn_corr`, ρ = 1.15, n = 10⁴, 50 reps; "uninformative" = both observables with the region [−1, 1]² (centre 0, half-width 1).  (c) F1, F2, F3 (first target; the certificate does not depend on it), ρ ∈ {0.2, 0.55} (Γ ≈ 1.5, 3), displacement d ∈ {0, 0.05, 0.1, 0.2, 0.3, 0.5} along the first observable beyond the largest E_p φ₁ over the class, n = 10⁴, 50 reps; d = 0 is the consistent data region | runtime; the protocol leaves these choices open |
| D6 | H-D: "the least n" | separate sweep on F1 `nnn_corr`, n ∈ {200, 500, 10³, 2·10³, 5·10³, 10⁴, 2·10⁴, 5·10⁴, 10⁵, 2·10⁵}, 20 reps, stopping at the first n with median excess < 0.05; n* log-linearly interpolated between the two grid points around 0.05 (the fit on the grid value is reported too) | the grid's three sample sizes cannot locate n* |
| D7 | S3 (M1, M2) via `ci.s3_interval` | the same computation with the draws lumped (equal (φ, f) merged with their multiplicities, Proposition 8.1); checked against `ci.s3_interval` on the raw draws in the first repetition of every n = 10³ cell (line below table 4.2) | runtime at n = 10⁵ |
| D8 | — | B1 and B3 are computed on the lumped sample (exact identity; a bootstrap resample is a multinomial draw of the multiplicities) | runtime |
| D9 | the inconsistency certificate's level | δ = 0.05 for the one test | the protocol fixes δ = 0.05 and δ/2 per end of an interval; the certificate is one test |
| D10 | M0 "cross-checked against the primal programme on F1, F2" | done (agreement to 2.4·10⁻⁷ or better, §4.1); on F3 (ellipsoid, no linear programme) M0 is the descent route, which returns a valid certificate for each end, so the M0 interval contains I but may be wider than it; the extremal-ensemble check of Theorem 4.1(c) in §4.1 assigns tied cells (s = 0) to l and is therefore inconclusive wherever ties carry mass (it also "fails" on F1/F2, where the programme agrees) — F3's reference is not independently verified.  A too-wide M0 makes coverage of I harder and understates excess | no independent exact route for the ellipsoid in the library |
| D11 | F1 state-dependent ρ(x) | ρ(x) = 0.55·(0.5 + \|magnetisation(x)\|) ∈ [0.275, 0.825] (label `var`, Γ = e^{2·0.825}); R = ρ(x)·r(x) | not specified |
| D12 | the data | region centred at the exact averages of p_true (no simulated measurement noise); r(x) = clip(0.6 φ₁ − 0.3 φ₂ + 0.4 ξ(x), −1, 1), ξ iid uniform on [−1, 1] with a fixed seed (F1–F3); F4: R = (ρ/50) Σᵢ sᵢ(xᵢ − ½), sᵢ = ±1 fixed | not specified |
| D13 | F5 two-spin product target | only the programme (Corollary 9.3 does not apply to it) | — |
| D14 | F4 methods | all of M1–M6, B2, B3 run on F4 (exact b, G from the level counts); B4, B5 exact from the law of the target | — |
| D16 | — | the protocol's grid ran on the library before the change of 02:35:33 UTC, the later runs after it (provenance table in §1) | the library changed during the campaign |
| D15 | REPORT.md written by the subagent | the subagent's file-writing tool refused a report file; `make_tables.py --write` writes this file from `report_template.py` | tool policy |

**Readings of the criteria** (fixed before the tables were produced):
"excess" of an interval = (hi − V⁺) + (V⁻ − lo) (both ends together); "M3 trivial" (H-B) = M3's median width is
the whole range 2; "M1 trivial" (H-B) = [−1, 1] in every repetition; "M3 not trivial" (H-E) = M3's interval is the
whole range in fewer than half the repetitions; H-F(i): a repetition misses if lo > V⁻ or hi < V⁺ (an empty
bootstrap counts as a miss); H-F(ii): per cell, B2's value inside [V⁻, V⁺] (a failed fit counts as outside);
H-F(iii): per cell, median width of B3 ≥ 2|I| (an empty pool interval has width 0); H-G: per cell (exact);
H-H: per (family, ρ, d), the fraction of repetitions in which `certify_inconsistent` returns `certified`;
H-I: per cell, the fraction of repetitions whose M3 interval does not contain the true value; H-K: "covers" read as
a coverage rate of at least 1 − δ = 0.95 (the rate is shown); H-C is evaluated on all families F1–F4; Γ thresholds
refer to the nominal envelopes (Γ = e^{2ρ} ≈ 1.5, 3, 10, 30, 100; e.g. e^{1.1} = 3.004 counts as Γ = 3), compared with a 1 % tolerance; `var` (Γ = 5.2) counts in Γ ≥ 3 and Γ ≤ 10.

## 3. Hypotheses

<!-- GEN:hypotheses -->
| hypothesis | criterion (as read) | outcome | the numbers |
|---|---|---|---|
| H-A | M1 and M2 cover I in every repetition on F1-F3; refuted by one miss | holds | 0 misses in 12420 repetitions |
| H-B | for Gamma >= 3, every n, F1-F3: median excess M1 >= 5 x M3 (unless M3 trivial), and M1 trivial at n = 10^3 for Gamma >= 10 | refuted | 66 cells; ratio min 1.00, median 10.66; 15 cells with ratio < 5 and M3 not trivial (e.g. F1/abs_mag/env 1.15/n 1000: ratio 2.71; F1/abs_mag/env 2.3/n 10000: ratio 3.58; F1/abs_mag/env var/n 1000: ratio 4.71); M1 not always trivial at n=10^3, Gamma>=10: 0 cells |
| H-C | miss rate of each certified end of M3, M4 <= delta/2 + 3 sqrt(delta/2 (1 - delta/2)/reps) in every cell | holds | 192 cells (F1-F4); largest miss rate 0.000; threshold 0.072 at 100 reps, 0.111 at 30 |
| H-D | F1 (nnn_corr), least n with median excess of M3 < 0.05 grows like Gamma^gamma, 0.7 <= gamma <= 1.3 | refuted | Gamma 1.5: n* 5541 (grid 10000; median excess 0.0368); Gamma 3.0: n* 4874 (grid 5000; median excess 0.0490); Gamma 10.0: n* 9079 (grid 10000; median excess 0.0464); Gamma 30.0: n* 14317 (grid 20000; median excess 0.0304); Gamma 99.5: n* 22200 (grid 50000; median excess 0.0229); fitted gamma 0.37 (interpolated n*), 0.45 (grid n*), over 5 envelopes |
| H-E | where M3 is not trivial: median excess M3 <= M6 <= M5 | holds | 87 cells; 0 violations |
| H-F(i) | B1's nominal 95 % interval misses an end of I in > 5 % of repetitions in >= 1 cell at n = 10^3, Gamma >= 10 | holds | 10 cells run; 9 with miss rate > 0.05; largest 0.160 (F1/nnn_corr/env 2.3) |
| H-F(ii) | B2's number lies inside I in >= 95 % of repetitions (consistent data), every cell F1-F3 | refuted | 81 cells; min rate 0.920; 1 cells below 0.95 (e.g. F2/pair_pop/env 0.2/n 1000: 0.92) |
| H-F(iii) | B3's interval on the pool at least twice as wide as I (median width) for Gamma <= 10 on F1-F3 | refuted | 36 cells; min ratio 1.76; 3 cells below 2 (e.g. F1/abs_mag/env 1.15/n 1000: 1.76, F1/abs_mag/env 1.15/n 10000: 1.76, F1/abs_mag/env 1.15/n 100000: 1.76) |
| H-G | B5 width >= 1.5 |I| on F1-F3 for Gamma >= 3; B4 wider than B5 in every cell | refuted | B5/|I|: min 1.20 over 22 cells, 10 below 1.5 (F1|nnn_corr|0.55: 1.24; F1|nnn_corr|1.15: 1.20; F1|nnn_corr|1.7: 1.35); B4 not wider than B5 in 0 of 27 cells |
| H-H | displacement >= 0.2, Gamma <= 3, n = 10^4: detection >= 90 %; consistent data: false alarms <= 5 % | holds | min detection at displacement >= 0.2: 1.00; max false-alarm rate 0.00 |
| H-I | true half-width 2 rho, declared rho: M3 misses the true value in > 10 % of repetitions in >= 1 cell | refuted | largest miss rate 0.00 (F1/nnn_corr/rho 0.55); cells above 0.10: 0 of 9 |
| H-J | F5: Cor. 9.3 = programme at 8, 12 sites to 1e-6; 200 sites in < 10 s; box hull within 1e-3 of the range from 20 sites (slope 0.5) | holds | max |Cor. 9.3 - programme| 2.42e-13 over 16 cases; largest time at 200 sites 2.70 s; hull gap at 20 sites 1.57e-04, cells >= 20 sites above 1e-3: 0 |
| H-K | F4: exact interval by level counts < 60 s; M3 at n = 10^5 covers I with median excess < 0.05 for Gamma <= 3 | holds | exact: largest time 8.03 s; M3 at n=10^5: rho 0.2: coverage 1.00, median excess 0.0049; rho 0.55: coverage 1.00, median excess 0.0045 |
<!-- /GEN:hypotheses -->

## 4. Results

### 4.1 Exact side (M0, B4, B5) for every cell

`|M0 − primal|`: difference to the primal programme (F1, F2).  `extremal gap`: |target average of the extremal
ensemble at the returned multipliers − the end|; `extremal in R`: its measured averages lie in the region (10⁻⁶).

<!-- GEN:exact -->
| fam | target | env | Γ | V− (M0) | V+ (M0) | true | cells | M0 s | |M0 − primal| | extremal gap | extremal in R | B5 lo | B5 hi | B4 lo | B4 hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | abs_mag | 0.2 | 1.492 | -0.358 | -0.198 | -0.287 | 51 | 0.018 | 3.89e-16 | 1.35e-04 | yes | -0.358 | -0.190 | -0.375 | -0.172 |
| F1 | abs_mag | 0.55 | 3.004 | -0.491 | -0.108 | -0.304 | 51 | 0.027 | 6.66e-16 | 0.022 | no | -0.492 | -0.033 | -0.539 | 0.014 |
| F1 | abs_mag | 1.15 | 9.974 | -0.674 | 0.043 | -0.328 | 51 | 0.017 | 1.33e-15 | 0.211 | no | -0.679 | 0.231 | -0.777 | 0.337 |
| F1 | abs_mag | 1.7 | 29.964 | -0.817 | 0.173 | -0.341 | 51 | 0.017 | 1.94e-16 | 0.015 | no | -0.833 | 0.441 | -0.935 | 0.617 |
| F1 | abs_mag | 2.3 | 99.484 | -0.927 | 0.285 | -0.345 | 51 | 0.016 | 2.22e-16 | 0.107 | no | -0.941 | 0.661 | -1.000 | 0.871 |
| F1 | abs_mag | var | 5.207 | -0.463 | -0.135 | -0.304 | 51 | 0.016 | 2.78e-16 | 0.162 | no | -0.463 | -0.043 | -0.656 | 0.163 |
| F1 | nnn_corr | 0.2 | 1.492 | -0.014 | 0.100 | 0.038 | 133 | 0.022 | 1.21e-17 | 2.43e-04 | no | -0.014 | 0.102 | -0.030 | 0.115 |
| F1 | nnn_corr | 0.55 | 3.004 | -0.095 | 0.168 | 0.032 | 133 | 0.018 | 2.32e-07 | 0.013 | no | -0.121 | 0.206 | -0.155 | 0.243 |
| F1 | nnn_corr | 1.15 | 9.974 | -0.239 | 0.272 | 0.027 | 133 | 0.031 | 1.71e-07 | 0.028 | no | -0.277 | 0.337 | -0.364 | 0.465 |
| F1 | nnn_corr | 1.7 | 29.964 | -0.325 | 0.370 | 0.026 | 133 | 0.019 | 8.05e-08 | 0.115 | no | -0.402 | 0.537 | -0.550 | 0.667 |
| F1 | nnn_corr | 2.3 | 99.484 | -0.366 | 0.470 | 0.029 | 133 | 0.020 | 2.92e-08 | 0.094 | no | -0.576 | 0.682 | -0.744 | 0.873 |
| F1 | nnn_corr | var | 5.207 | -0.077 | 0.153 | 0.029 | 133 | 0.018 | 3.19e-16 | 0.016 | no | -0.097 | 0.199 | -0.252 | 0.344 |
| F2 | pair_pop | 0.2 | 1.492 | -0.962 | -0.923 | -0.945 | 16 | 0.019 | 2.22e-16 | 0.019 | yes | -0.962 | -0.918 | -0.995 | -0.867 |
| F2 | pair_pop | 0.55 | 3.004 | -0.978 | -0.893 | -0.945 | 16 | 0.019 | 2.22e-16 | 0.052 | no | -0.981 | -0.841 | -1.000 | -0.685 |
| F2 | pair_pop | 1.15 | 9.974 | -0.991 | -0.802 | -0.946 | 16 | 0.030 | 1.11e-16 | 0.193 | no | -0.994 | -0.554 | -1.000 | -0.274 |
| F2 | pair_pop | 1.7 | 29.964 | -0.996 | -0.600 | -0.945 | 16 | 0.020 | 5.55e-16 | 0.437 | no | -0.998 | -0.073 | -1.000 | 0.180 |
| F2 | pair_pop | 2.3 | 99.484 | -0.999 | -0.033 | -0.945 | 16 | 0.018 | 1.85e-15 | 0.915 | no | -0.999 | 0.483 | -1.000 | 0.709 |
| F3 | rg2 | 0.2 | 1.492 | -0.649 | -0.580 | -0.616 | 1164 | 0.181 | – | 7.45e-05 | yes | -0.650 | -0.573 | -0.660 | -0.563 |
| F3 | rg2 | 0.55 | 3.004 | -0.682 | -0.556 | -0.622 | 1164 | 0.202 | – | 1.85e-04 | yes | -0.709 | -0.500 | -0.733 | -0.469 |
| F3 | rg2 | 1.15 | 9.974 | -0.729 | -0.518 | -0.631 | 1164 | 0.199 | – | 3.01e-04 | no | -0.791 | -0.365 | -0.834 | -0.286 |
| F3 | rg2 | 1.7 | 29.964 | -0.764 | -0.483 | -0.639 | 1164 | 0.172 | – | 0.006 | yes | -0.845 | -0.239 | -0.901 | -0.095 |
| F3 | rg2 | 2.3 | 99.484 | -0.795 | -0.442 | -0.646 | 1164 | 0.178 | – | 0.002 | no | -0.888 | -0.096 | -0.957 | 0.136 |
| F3 | stress | 0.2 | 1.492 | -0.383 | -0.302 | -0.347 | 1566 | 0.160 | – | 9.97e-05 | yes | -0.383 | -0.300 | -0.393 | -0.290 |
| F3 | stress | 0.55 | 3.004 | -0.435 | -0.267 | -0.355 | 1566 | 0.227 | – | 0.002 | no | -0.452 | -0.224 | -0.477 | -0.194 |
| F3 | stress | 1.15 | 9.974 | -0.508 | -0.213 | -0.368 | 1566 | 0.198 | – | 0.002 | no | -0.551 | -0.091 | -0.607 | -0.018 |
| F3 | stress | 1.7 | 29.964 | -0.573 | -0.168 | -0.380 | 1566 | 0.222 | – | 0.001 | no | -0.611 | 0.022 | -0.717 | 0.158 |
| F3 | stress | 2.3 | 99.484 | -0.643 | -0.123 | -0.392 | 1566 | 0.216 | – | 0.003 | no | -0.699 | 0.154 | -0.832 | 0.364 |
| F4 | ones_first20 | 0.2 | 1.492 | -0.183 | -0.116 | -0.150 | 33201 | 7.053 | – | 4.30e-16 | yes | -0.183 | -0.116 | -0.192 | -0.107 |
| F4 | ones_first20 | 0.55 | 3.004 | -0.241 | -0.057 | -0.151 | 33201 | 8.153 | – | 2.61e-04 | yes | -0.243 | -0.055 | -0.265 | -0.032 |
| F4 | ones_first20 | 1.15 | 9.974 | -0.323 | 0.023 | -0.152 | 33201 | 7.562 | – | 0.003 | no | -0.340 | 0.045 | -0.389 | 0.096 |
| F4 | ones_first20 | 1.7 | 29.964 | -0.390 | 0.090 | -0.154 | 33201 | 6.760 | – | 0.002 | no | -0.421 | 0.132 | -0.500 | 0.214 |
| F4 | ones_first20 | 2.3 | 99.484 | -0.458 | 0.157 | -0.155 | 33201 | 6.139 | – | 0.001 | no | -0.499 | 0.218 | -0.616 | 0.341 |
<!-- /GEN:exact -->

### 4.2 Median total excess over I, every cell and method

<!-- GEN:excess_summary -->
| fam | target | env | Γ | n | V− | V+ | M1 med ex | M2 med ex | M3 med ex | M4 med ex | M5 med ex | M6 med ex | B1 med ex | B3 med ex |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | abs_mag | 0.2 | 1.492 | 1000 | -0.358 | -0.198 | 0.389 | 0.347 | 0.162 | 0.056 | 0.567 | 0.424 | 0.050 | 0.931 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | -0.358 | -0.198 | 0.141 | 0.115 | 0.049 | 0.011 | 0.180 | 0.113 | – | 0.931 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | -0.358 | -0.198 | 0.054 | 0.041 | 0.011 | 0.002 | 0.060 | 0.052 | – | 0.931 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | -0.491 | -0.108 | 1.362 | 1.276 | 0.209 | 0.144 | 0.859 | 0.541 | 0.049 | 0.768 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | -0.491 | -0.108 | 0.618 | 0.512 | 0.052 | 0.029 | 0.284 | 0.114 | – | 0.768 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | -0.491 | -0.108 | 0.257 | 0.193 | 0.012 | 0.006 | 0.082 | 0.047 | – | 0.768 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | -0.674 | 0.043 | 1.283 | 1.283 | 0.473 | 0.431 | 1.155 | 0.829 | 0.058 | 0.545 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | -0.674 | 0.043 | 1.283 | 1.283 | 0.072 | 0.056 | 0.518 | 0.160 | – | 0.545 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | -0.674 | 0.043 | 0.932 | 0.810 | 0.015 | 0.015 | 0.141 | 0.040 | – | 0.545 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | -0.817 | 0.173 | 1.010 | 1.010 | 1.010 | 1.010 | 1.010 | 0.963 | 0.061 | 0.378 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | -0.817 | 0.173 | 1.010 | 1.010 | 0.098 | 0.096 | 0.903 | 0.207 | – | 0.378 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | -0.817 | 0.173 | 1.010 | 1.010 | 0.018 | 0.018 | 0.223 | 0.042 | – | 0.378 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | -0.927 | 0.285 | 0.788 | 0.788 | 0.788 | 0.788 | 0.788 | 0.788 | 0.055 | 0.231 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | -0.927 | 0.285 | 0.788 | 0.788 | 0.220 | 0.219 | 0.788 | 0.335 | – | 0.231 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | -0.927 | 0.285 | 0.788 | 0.788 | 0.017 | 0.018 | 0.532 | 0.042 | – | 0.231 |
| F1 | abs_mag | var | 5.207 | 1000 | -0.463 | -0.135 | 1.239 | 1.171 | 0.263 | 0.139 | 1.072 | 0.663 | 0.053 | 0.827 |
| F1 | abs_mag | var | 5.207 | 10000 | -0.463 | -0.135 | 0.519 | 0.436 | 0.064 | 0.032 | 0.379 | 0.146 | – | 0.827 |
| F1 | abs_mag | var | 5.207 | 100000 | -0.463 | -0.135 | 0.217 | 0.166 | 0.014 | 0.007 | 0.108 | 0.050 | – | 0.827 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | -0.014 | 0.100 | 0.382 | 0.340 | 0.126 | 0.055 | 0.476 | 0.336 | 0.036 | 1.133 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | -0.014 | 0.100 | 0.135 | 0.109 | 0.036 | 0.008 | 0.151 | 0.090 | – | 1.222 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | -0.014 | 0.100 | 0.048 | 0.036 | 0.009 | 0.002 | 0.060 | 0.059 | – | 1.244 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | -0.095 | 0.168 | 1.611 | 1.440 | 0.186 | 0.138 | 0.915 | 0.495 | 0.034 | 0.984 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | -0.095 | 0.168 | 0.605 | 0.500 | 0.033 | 0.018 | 0.283 | 0.111 | – | 1.039 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | -0.095 | 0.168 | 0.250 | 0.197 | 0.008 | 0.004 | 0.107 | 0.055 | – | 1.094 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | -0.239 | 0.272 | 1.489 | 1.489 | 0.447 | 0.407 | 1.489 | 0.860 | 0.034 | 0.732 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | -0.239 | 0.272 | 1.489 | 1.489 | 0.045 | 0.039 | 0.571 | 0.119 | – | 0.788 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | -0.239 | 0.272 | 0.938 | 0.720 | 0.009 | 0.007 | 0.136 | 0.045 | – | 0.843 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | -0.325 | 0.370 | 1.305 | 1.305 | 1.305 | 1.305 | 1.305 | 1.305 | 0.040 | 0.540 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | -0.325 | 0.370 | 1.305 | 1.305 | 0.078 | 0.077 | 1.218 | 0.177 | – | 0.595 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | -0.325 | 0.370 | 1.305 | 1.305 | 0.011 | 0.010 | 0.223 | 0.041 | – | 0.639 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | -0.366 | 0.470 | 1.164 | 1.164 | 1.164 | 1.164 | 1.164 | 1.164 | 0.045 | 0.386 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | -0.366 | 0.470 | 1.164 | 1.164 | 0.250 | 0.246 | 1.164 | 0.434 | – | 0.473 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | -0.366 | 0.470 | 1.164 | 1.164 | 0.014 | 0.016 | 0.662 | 0.050 | – | 0.494 |
| F1 | nnn_corr | var | 5.207 | 1000 | -0.077 | 0.153 | 1.290 | 1.155 | 0.248 | 0.129 | 1.224 | 0.645 | 0.034 | 1.022 |
| F1 | nnn_corr | var | 5.207 | 10000 | -0.077 | 0.153 | 0.494 | 0.410 | 0.034 | 0.016 | 0.403 | 0.114 | – | 1.078 |
| F1 | nnn_corr | var | 5.207 | 100000 | -0.077 | 0.153 | 0.206 | 0.161 | 0.008 | 0.004 | 0.113 | 0.053 | – | 1.133 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | -0.962 | -0.923 | 0.250 | 0.219 | 0.150 | 0.064 | 0.344 | 0.280 | 0.038 | 1.961 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | -0.962 | -0.923 | 0.116 | 0.099 | 0.040 | 0.011 | 0.161 | 0.082 | – | 1.961 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | -0.962 | -0.923 | 0.055 | 0.040 | 0.009 | 0.002 | 0.074 | 0.065 | – | 1.961 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | -0.978 | -0.893 | 0.915 | 0.790 | 0.215 | 0.150 | 0.567 | 0.441 | 0.055 | 1.915 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | -0.978 | -0.893 | 0.372 | 0.303 | 0.066 | 0.041 | 0.213 | 0.141 | – | 1.915 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | -0.978 | -0.893 | 0.177 | 0.143 | 0.017 | 0.009 | 0.071 | 0.058 | – | 1.915 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | -0.991 | -0.802 | 1.811 | 1.811 | 0.459 | 0.380 | 1.088 | 0.885 | 0.104 | 1.811 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | -0.991 | -0.802 | 1.584 | 1.275 | 0.148 | 0.129 | 0.479 | 0.243 | – | 1.811 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | -0.991 | -0.802 | 0.716 | 0.579 | 0.033 | 0.029 | 0.150 | 0.063 | – | 1.811 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | -0.996 | -0.600 | 1.604 | 1.604 | 0.823 | 0.769 | 1.500 | 1.339 | 0.202 | 1.604 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | -0.996 | -0.600 | 1.604 | 1.604 | 0.284 | 0.262 | 0.814 | 0.437 | – | 1.604 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | -0.996 | -0.600 | 1.604 | 1.568 | 0.073 | 0.074 | 0.269 | 0.113 | – | 1.604 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | -0.999 | -0.033 | 1.034 | 1.034 | 1.034 | 1.034 | 1.034 | 1.034 | 0.246 | 1.034 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | -0.999 | -0.033 | 1.034 | 1.034 | 0.443 | 0.396 | 1.034 | 0.638 | – | 1.034 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | -0.999 | -0.033 | 1.034 | 1.034 | 0.124 | 0.115 | 0.398 | 0.168 | – | 1.034 |
| F3 | rg2 | 0.2 | 1.492 | 1000 | -0.649 | -0.580 | 0.421 | 0.360 | 0.096 | 0.053 | 0.599 | 0.333 | – | – |
| F3 | rg2 | 0.2 | 1.492 | 10000 | -0.649 | -0.580 | 0.153 | 0.119 | 0.015 | 0.006 | 0.182 | 0.073 | – | – |
| F3 | rg2 | 0.2 | 1.492 | 100000 | -0.649 | -0.580 | 0.058 | 0.043 | 0.004 | 6.11e-04 | 0.073 | 0.061 | – | – |
| F3 | rg2 | 0.55 | 3.004 | 1000 | -0.682 | -0.556 | 1.216 | 1.091 | 0.172 | 0.129 | 0.867 | 0.457 | – | – |
| F3 | rg2 | 0.55 | 3.004 | 10000 | -0.682 | -0.556 | 0.670 | 0.537 | 0.017 | 0.012 | 0.334 | 0.071 | – | – |
| F3 | rg2 | 0.55 | 3.004 | 100000 | -0.682 | -0.556 | 0.288 | 0.221 | 0.003 | 0.001 | 0.081 | 0.060 | – | – |
| F3 | rg2 | 1.15 | 9.974 | 1000 | -0.729 | -0.518 | 1.789 | 1.789 | 0.516 | 0.488 | 1.249 | 0.809 | – | – |
| F3 | rg2 | 1.15 | 9.974 | 10000 | -0.729 | -0.518 | 1.747 | 1.438 | 0.033 | 0.030 | 0.663 | 0.084 | – | – |
| F3 | rg2 | 1.15 | 9.974 | 100000 | -0.729 | -0.518 | 0.881 | 0.745 | 0.003 | 0.002 | 0.150 | 0.057 | – | – |
| F3 | rg2 | 1.7 | 29.964 | 1000 | -0.764 | -0.483 | 1.719 | 1.719 | 1.108 | 1.081 | 1.623 | 1.238 | – | – |
| F3 | rg2 | 1.7 | 29.964 | 10000 | -0.764 | -0.483 | 1.719 | 1.719 | 0.079 | 0.077 | 1.049 | 0.211 | – | – |
| F3 | rg2 | 1.7 | 29.964 | 100000 | -0.764 | -0.483 | 1.719 | 1.515 | 0.004 | 0.004 | 0.342 | 0.055 | – | – |
| F3 | rg2 | 2.3 | 99.484 | 1000 | -0.795 | -0.442 | 1.647 | 1.647 | 1.647 | 1.647 | 1.647 | 1.647 | – | – |
| F3 | rg2 | 2.3 | 99.484 | 10000 | -0.795 | -0.442 | 1.647 | 1.647 | 0.358 | 0.355 | 1.508 | 0.577 | – | – |
| F3 | rg2 | 2.3 | 99.484 | 100000 | -0.795 | -0.442 | 1.647 | 1.647 | 0.009 | 0.009 | 0.809 | 0.054 | – | – |
| F3 | stress | 0.2 | 1.492 | 1000 | -0.383 | -0.302 | 0.415 | 0.353 | 0.102 | 0.050 | 0.545 | 0.328 | – | 0.706 |
| F3 | stress | 0.2 | 1.492 | 10000 | -0.383 | -0.302 | 0.147 | 0.113 | 0.022 | 0.006 | 0.185 | 0.080 | – | – |
| F3 | stress | 0.2 | 1.492 | 100000 | -0.383 | -0.302 | 0.052 | 0.037 | 0.005 | 0.001 | 0.061 | 0.060 | – | – |
| F3 | stress | 0.55 | 3.004 | 1000 | -0.435 | -0.267 | 1.448 | 1.323 | 0.176 | 0.131 | 1.034 | 0.501 | – | 0.613 |
| F3 | stress | 0.55 | 3.004 | 10000 | -0.435 | -0.267 | 0.650 | 0.512 | 0.020 | 0.013 | 0.308 | 0.077 | – | – |
| F3 | stress | 0.55 | 3.004 | 100000 | -0.435 | -0.267 | 0.264 | 0.202 | 0.004 | 0.002 | 0.077 | 0.059 | – | – |
| F3 | stress | 1.15 | 9.974 | 1000 | -0.508 | -0.213 | 1.705 | 1.705 | 0.633 | 0.574 | 1.588 | 1.080 | 0.018 | 0.481 |
| F3 | stress | 1.15 | 9.974 | 10000 | -0.508 | -0.213 | 1.705 | 1.628 | 0.036 | 0.034 | 0.765 | 0.125 | – | – |
| F3 | stress | 1.15 | 9.974 | 100000 | -0.508 | -0.213 | 1.071 | 0.807 | 0.004 | 0.003 | 0.141 | 0.054 | – | – |
| F3 | stress | 1.7 | 29.964 | 1000 | -0.573 | -0.168 | 1.595 | 1.595 | 1.479 | 1.451 | 1.595 | 1.519 | – | – |
| F3 | stress | 1.7 | 29.964 | 10000 | -0.573 | -0.168 | 1.595 | 1.595 | 0.092 | 0.089 | 1.294 | 0.207 | – | – |
| F3 | stress | 1.7 | 29.964 | 100000 | -0.573 | -0.168 | 1.595 | 1.595 | 0.007 | 0.006 | 0.340 | 0.053 | – | – |
| F3 | stress | 2.3 | 99.484 | 1000 | -0.643 | -0.123 | 1.481 | 1.481 | 1.481 | 1.481 | 1.481 | 1.481 | – | – |
| F3 | stress | 2.3 | 99.484 | 10000 | -0.643 | -0.123 | 1.481 | 1.481 | 0.405 | 0.401 | 1.481 | 0.720 | – | – |
| F3 | stress | 2.3 | 99.484 | 100000 | -0.643 | -0.123 | 1.481 | 1.481 | 0.011 | 0.011 | 1.046 | 0.053 | – | – |
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | -0.183 | -0.116 | 0.380 | 0.338 | 0.087 | 0.048 | 0.391 | 0.249 | – | 0.965 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | -0.183 | -0.116 | 0.133 | 0.107 | 0.021 | 0.006 | 0.126 | 0.062 | – | 1.149 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | -0.183 | -0.116 | 0.046 | 0.034 | 0.005 | 0.001 | 0.062 | 0.062 | – | 1.336 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | -0.241 | -0.057 | 1.535 | 1.382 | 0.137 | 0.106 | 0.631 | 0.341 | – | 0.838 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | -0.241 | -0.057 | 0.545 | 0.440 | 0.020 | 0.012 | 0.200 | 0.059 | – | 1.044 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | -0.241 | -0.057 | 0.190 | 0.142 | 0.004 | 0.002 | 0.058 | 0.057 | – | 1.211 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | -0.323 | 0.023 | 1.654 | 1.654 | 0.484 | 0.442 | 1.493 | 0.800 | – | 0.687 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | -0.323 | 0.023 | 1.654 | 1.654 | 0.034 | 0.031 | 0.534 | 0.106 | – | 0.889 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | -0.323 | 0.023 | 0.875 | 0.657 | 0.005 | 0.004 | 0.107 | 0.053 | – | 1.054 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | -0.390 | 0.090 | 1.520 | 1.520 | 1.520 | 1.520 | 1.520 | 1.491 | – | 0.548 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | -0.390 | 0.090 | 1.520 | 1.520 | 0.075 | 0.073 | 1.274 | 0.166 | – | 0.741 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | -0.390 | 0.090 | 1.520 | 1.520 | 0.006 | 0.006 | 0.263 | 0.049 | – | 0.909 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | -0.458 | 0.157 | 1.385 | 1.385 | 1.385 | 1.385 | 1.385 | 1.385 | – | 0.425 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | -0.458 | 0.157 | 1.385 | 1.385 | 0.290 | 0.285 | 1.385 | 0.479 | – | 0.611 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | -0.458 | 0.157 | 1.385 | 1.385 | 0.010 | 0.011 | 0.862 | 0.046 | – | 0.782 |
<!-- /GEN:excess_summary -->

<!-- GEN:s3check -->
Lumped S3 against `ci.s3_interval` on the raw draws: 64 comparisons, max |difference| 3.44e-15.
<!-- /GEN:s3check -->

### 4.3 Full tables per family

Columns: coverage of I and of the true value; median / 90th percentile of the width, of the total excess and of
the excess at each end (+: upper, −: lower); `triv`: fraction of repetitions with the whole range; `miss±`:
fraction of repetitions in which that end is certified and lies inside I (for B1, B3: the end lies inside I, or the
interval is empty); `incons`: the certified ends cross.

#### F1
<!-- GEN:grid_F1 -->
| fam | target | env | Γ | n | method | reps | cov I | cov true | med w | p90 w | med ex | p90 ex | med ex+ | p90 ex+ | med ex− | p90 ex− | triv | miss+ | miss− | incons |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | abs_mag | 0.2 | 1.492 | 1000 | B1 | 100 | 0.920 | 1.000 | 0.209 | 0.218 | 0.050 | 0.059 | 0.021 | 0.037 | 0.029 | 0.044 | 0.000 | 0.060 | 0.020 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.090 | 1.090 | 0.931 | 0.931 | 0.629 | 0.629 | 0.301 | 0.301 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 1000 | M1 | 100 | 1.000 | 1.000 | 0.548 | 0.554 | 0.389 | 0.394 | 0.199 | 0.203 | 0.190 | 0.193 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 1000 | M2 | 100 | 1.000 | 1.000 | 0.506 | 0.512 | 0.347 | 0.352 | 0.178 | 0.182 | 0.169 | 0.172 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.321 | 0.365 | 0.162 | 0.205 | 0.094 | 0.124 | 0.075 | 0.094 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.216 | 0.224 | 0.056 | 0.065 | 0.029 | 0.040 | 0.026 | 0.031 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.727 | 0.834 | 0.567 | 0.674 | 0.316 | 0.487 | 0.178 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.583 | 0.669 | 0.424 | 0.509 | 0.245 | 0.335 | 0.166 | 0.211 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.090 | 1.090 | 0.931 | 0.931 | 0.629 | 0.629 | 0.301 | 0.301 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.301 | 0.302 | 0.141 | 0.143 | 0.075 | 0.076 | 0.066 | 0.067 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.275 | 0.276 | 0.115 | 0.117 | 0.062 | 0.063 | 0.053 | 0.054 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.208 | 0.216 | 0.049 | 0.056 | 0.027 | 0.036 | 0.022 | 0.031 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.170 | 0.173 | 0.011 | 0.013 | 0.007 | 0.009 | 0.004 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.340 | 0.374 | 0.180 | 0.214 | 0.118 | 0.155 | 0.060 | 0.068 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.273 | 0.281 | 0.113 | 0.121 | 0.071 | 0.079 | 0.043 | 0.056 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.090 | 1.090 | 0.931 | 0.931 | 0.629 | 0.629 | 0.301 | 0.301 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.214 | 0.214 | 0.054 | 0.055 | 0.031 | 0.032 | 0.023 | 0.023 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.200 | 0.201 | 0.041 | 0.041 | 0.024 | 0.024 | 0.017 | 0.017 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.170 | 0.172 | 0.011 | 0.012 | 0.006 | 0.008 | 0.005 | 0.008 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.162 | 0.163 | 0.002 | 0.003 | 0.001 | 0.002 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.220 | 0.235 | 0.060 | 0.076 | 0.038 | 0.050 | 0.023 | 0.028 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.211 | 0.220 | 0.052 | 0.061 | 0.034 | 0.042 | 0.015 | 0.023 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | B1 | 100 | 0.900 | 1.000 | 0.432 | 0.445 | 0.049 | 0.062 | 0.026 | 0.051 | 0.022 | 0.035 | 0.000 | 0.040 | 0.060 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.151 | 1.151 | 0.768 | 0.768 | 0.538 | 0.538 | 0.230 | 0.230 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | M1 | 100 | 1.000 | 1.000 | 1.745 | 1.756 | 1.362 | 1.373 | 0.852 | 0.864 | 0.509 | 0.509 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | M2 | 100 | 1.000 | 1.000 | 1.659 | 1.671 | 1.276 | 1.287 | 0.767 | 0.778 | 0.509 | 0.509 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.592 | 0.627 | 0.209 | 0.244 | 0.132 | 0.176 | 0.077 | 0.099 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.527 | 0.559 | 0.144 | 0.176 | 0.089 | 0.119 | 0.055 | 0.066 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.243 | 1.328 | 0.859 | 0.945 | 0.627 | 0.725 | 0.238 | 0.309 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.925 | 0.983 | 0.541 | 0.600 | 0.373 | 0.438 | 0.174 | 0.201 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.151 | 1.151 | 0.768 | 0.768 | 0.538 | 0.538 | 0.230 | 0.230 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | M1 | 100 | 1.000 | 1.000 | 1.001 | 1.004 | 0.618 | 0.621 | 0.345 | 0.349 | 0.273 | 0.275 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.895 | 0.899 | 0.512 | 0.515 | 0.292 | 0.296 | 0.220 | 0.222 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.436 | 0.446 | 0.052 | 0.063 | 0.031 | 0.045 | 0.022 | 0.030 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.412 | 0.418 | 0.029 | 0.035 | 0.018 | 0.024 | 0.010 | 0.013 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.667 | 0.696 | 0.284 | 0.313 | 0.210 | 0.248 | 0.079 | 0.090 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.497 | 0.518 | 0.114 | 0.135 | 0.072 | 0.099 | 0.041 | 0.051 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.151 | 1.151 | 0.768 | 0.768 | 0.538 | 0.538 | 0.230 | 0.230 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.640 | 0.641 | 0.257 | 0.258 | 0.162 | 0.163 | 0.095 | 0.096 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.576 | 0.577 | 0.193 | 0.194 | 0.122 | 0.123 | 0.071 | 0.071 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.395 | 0.398 | 0.012 | 0.015 | 0.007 | 0.011 | 0.006 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.389 | 0.391 | 0.006 | 0.008 | 0.004 | 0.005 | 0.002 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.466 | 0.482 | 0.082 | 0.099 | 0.062 | 0.072 | 0.025 | 0.033 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.430 | 0.438 | 0.047 | 0.055 | 0.033 | 0.041 | 0.014 | 0.019 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | B1 | 100 | 0.880 | 1.000 | 0.775 | 0.795 | 0.058 | 0.079 | 0.038 | 0.062 | 0.019 | 0.031 | 0.000 | 0.040 | 0.080 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.261 | 1.261 | 0.545 | 0.545 | 0.389 | 0.389 | 0.155 | 0.155 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.283 | 1.283 | 0.957 | 0.957 | 0.326 | 0.326 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.283 | 1.283 | 0.957 | 0.957 | 0.326 | 0.326 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | M3 | 100 | 1.000 | 1.000 | 1.189 | 1.236 | 0.473 | 0.519 | 0.342 | 0.403 | 0.131 | 0.154 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | M4 | 100 | 1.000 | 1.000 | 1.147 | 1.192 | 0.431 | 0.476 | 0.308 | 0.347 | 0.121 | 0.139 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.872 | 1.958 | 1.155 | 1.242 | 0.957 | 0.957 | 0.198 | 0.285 | 0.050 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.546 | 1.584 | 0.829 | 0.867 | 0.675 | 0.711 | 0.151 | 0.184 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.261 | 1.261 | 0.545 | 0.545 | 0.389 | 0.389 | 0.155 | 0.155 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.283 | 1.283 | 0.957 | 0.957 | 0.326 | 0.326 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.283 | 1.283 | 0.957 | 0.957 | 0.326 | 0.326 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.788 | 0.802 | 0.072 | 0.086 | 0.052 | 0.064 | 0.021 | 0.026 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.773 | 0.785 | 0.056 | 0.068 | 0.040 | 0.054 | 0.015 | 0.020 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.234 | 1.260 | 0.518 | 0.543 | 0.440 | 0.462 | 0.071 | 0.094 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.877 | 0.899 | 0.160 | 0.183 | 0.123 | 0.145 | 0.036 | 0.044 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.261 | 1.261 | 0.545 | 0.545 | 0.389 | 0.389 | 0.155 | 0.155 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | M1 | 30 | 1.000 | 1.000 | 1.648 | 1.651 | 0.932 | 0.934 | 0.605 | 0.608 | 0.326 | 0.326 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | M2 | 30 | 1.000 | 1.000 | 1.526 | 1.528 | 0.810 | 0.812 | 0.496 | 0.498 | 0.314 | 0.315 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.732 | 0.736 | 0.015 | 0.019 | 0.011 | 0.014 | 0.005 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.731 | 0.734 | 0.015 | 0.018 | 0.010 | 0.014 | 0.003 | 0.005 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.857 | 0.867 | 0.141 | 0.150 | 0.122 | 0.127 | 0.021 | 0.027 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.757 | 0.764 | 0.040 | 0.047 | 0.029 | 0.035 | 0.013 | 0.016 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | B1 | 100 | 0.940 | 1.000 | 1.050 | 1.074 | 0.061 | 0.084 | 0.040 | 0.061 | 0.022 | 0.039 | 0.000 | 0.030 | 0.030 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.367 | 1.367 | 0.378 | 0.378 | 0.264 | 0.264 | 0.114 | 0.114 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 0.750 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.953 | 1.972 | 0.963 | 0.982 | 0.827 | 0.827 | 0.136 | 0.155 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.367 | 1.367 | 0.378 | 0.378 | 0.264 | 0.264 | 0.114 | 0.114 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | M3 | 100 | 1.000 | 1.000 | 1.087 | 1.111 | 0.098 | 0.122 | 0.073 | 0.094 | 0.025 | 0.033 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | M4 | 100 | 1.000 | 1.000 | 1.086 | 1.106 | 0.096 | 0.116 | 0.071 | 0.091 | 0.024 | 0.031 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.893 | 1.899 | 0.903 | 0.910 | 0.827 | 0.827 | 0.076 | 0.082 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | M6 | 100 | 1.000 | 1.000 | 1.197 | 1.219 | 0.207 | 0.230 | 0.170 | 0.193 | 0.034 | 0.043 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.367 | 1.367 | 0.378 | 0.378 | 0.264 | 0.264 | 0.114 | 0.114 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.010 | 1.010 | 0.827 | 0.827 | 0.183 | 0.183 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | M3 | 30 | 1.000 | 1.000 | 1.008 | 1.016 | 0.018 | 0.026 | 0.013 | 0.021 | 0.005 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | M4 | 30 | 1.000 | 1.000 | 1.007 | 1.018 | 0.018 | 0.028 | 0.013 | 0.023 | 0.004 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | M5 | 30 | 1.000 | 1.000 | 1.213 | 1.226 | 0.223 | 0.237 | 0.204 | 0.214 | 0.020 | 0.024 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | M6 | 30 | 1.000 | 1.000 | 1.032 | 1.044 | 0.042 | 0.054 | 0.034 | 0.043 | 0.008 | 0.013 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | B1 | 100 | 0.900 | 1.000 | 1.267 | 1.294 | 0.055 | 0.081 | 0.039 | 0.067 | 0.015 | 0.022 | 0.000 | 0.060 | 0.040 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.443 | 1.443 | 0.231 | 0.231 | 0.158 | 0.158 | 0.073 | 0.073 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 0.990 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | M6 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 0.810 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.443 | 1.443 | 0.231 | 0.231 | 0.158 | 0.158 | 0.073 | 0.073 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | M3 | 100 | 1.000 | 1.000 | 1.433 | 1.448 | 0.220 | 0.236 | 0.176 | 0.193 | 0.044 | 0.050 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | M4 | 100 | 1.000 | 1.000 | 1.431 | 1.446 | 0.219 | 0.233 | 0.175 | 0.189 | 0.043 | 0.048 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 0.940 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | M6 | 100 | 1.000 | 1.000 | 1.547 | 1.563 | 0.335 | 0.350 | 0.302 | 0.320 | 0.032 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.443 | 1.443 | 0.231 | 0.231 | 0.158 | 0.158 | 0.073 | 0.073 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 0.788 | 0.788 | 0.715 | 0.715 | 0.073 | 0.073 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | M3 | 30 | 1.000 | 1.000 | 1.229 | 1.238 | 0.017 | 0.026 | 0.011 | 0.022 | 0.004 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | M4 | 30 | 1.000 | 1.000 | 1.230 | 1.239 | 0.018 | 0.026 | 0.014 | 0.023 | 0.004 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | M5 | 30 | 1.000 | 1.000 | 1.744 | 1.759 | 0.532 | 0.547 | 0.508 | 0.527 | 0.023 | 0.025 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | M6 | 30 | 1.000 | 1.000 | 1.255 | 1.268 | 0.042 | 0.056 | 0.036 | 0.051 | 0.006 | 0.008 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 1000 | B1 | 100 | 0.930 | 1.000 | 0.381 | 0.398 | 0.053 | 0.070 | 0.028 | 0.051 | 0.025 | 0.038 | 0.000 | 0.050 | 0.020 | 0.000 |
| F1 | abs_mag | var | 5.207 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.155 | 1.155 | 0.827 | 0.827 | 0.562 | 0.562 | 0.265 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 1000 | M1 | 100 | 1.000 | 1.000 | 1.568 | 1.581 | 1.239 | 1.253 | 0.702 | 0.716 | 0.537 | 0.537 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 1000 | M2 | 100 | 1.000 | 1.000 | 1.500 | 1.513 | 1.171 | 1.185 | 0.635 | 0.648 | 0.537 | 0.537 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.591 | 0.637 | 0.263 | 0.309 | 0.161 | 0.213 | 0.098 | 0.118 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.467 | 0.498 | 0.139 | 0.169 | 0.089 | 0.117 | 0.053 | 0.062 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.400 | 1.479 | 1.072 | 1.150 | 0.807 | 0.888 | 0.246 | 0.353 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.991 | 1.049 | 0.663 | 0.721 | 0.466 | 0.537 | 0.187 | 0.224 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.155 | 1.155 | 0.827 | 0.827 | 0.562 | 0.562 | 0.265 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.848 | 0.851 | 0.519 | 0.523 | 0.305 | 0.309 | 0.214 | 0.217 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.764 | 0.768 | 0.436 | 0.440 | 0.263 | 0.267 | 0.172 | 0.175 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.392 | 0.409 | 0.064 | 0.081 | 0.042 | 0.058 | 0.022 | 0.027 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.360 | 0.369 | 0.032 | 0.041 | 0.023 | 0.031 | 0.008 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.707 | 0.737 | 0.379 | 0.408 | 0.293 | 0.323 | 0.085 | 0.094 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.474 | 0.491 | 0.146 | 0.163 | 0.104 | 0.115 | 0.043 | 0.054 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.155 | 1.155 | 0.827 | 0.827 | 0.562 | 0.562 | 0.265 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.546 | 0.546 | 0.217 | 0.218 | 0.143 | 0.144 | 0.074 | 0.075 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.494 | 0.495 | 0.166 | 0.166 | 0.111 | 0.112 | 0.055 | 0.056 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.343 | 0.349 | 0.014 | 0.020 | 0.010 | 0.013 | 0.005 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.336 | 0.338 | 0.007 | 0.010 | 0.005 | 0.008 | 0.002 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.436 | 0.456 | 0.108 | 0.128 | 0.079 | 0.100 | 0.029 | 0.034 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | abs_mag | var | 5.207 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.378 | 0.387 | 0.050 | 0.059 | 0.034 | 0.043 | 0.015 | 0.021 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | B1 | 100 | 0.920 | 1.000 | 0.150 | 0.155 | 0.036 | 0.041 | 0.014 | 0.025 | 0.022 | 0.032 | 0.000 | 0.040 | 0.040 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.247 | 1.302 | 1.133 | 1.189 | 0.679 | 0.734 | 0.454 | 0.454 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | M1 | 100 | 1.000 | 1.000 | 0.496 | 0.499 | 0.382 | 0.385 | 0.192 | 0.195 | 0.191 | 0.193 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | M2 | 100 | 1.000 | 1.000 | 0.454 | 0.457 | 0.340 | 0.343 | 0.171 | 0.174 | 0.170 | 0.172 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.240 | 0.254 | 0.126 | 0.140 | 0.063 | 0.083 | 0.064 | 0.084 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.168 | 0.172 | 0.055 | 0.058 | 0.028 | 0.031 | 0.026 | 0.030 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.590 | 0.684 | 0.476 | 0.570 | 0.254 | 0.349 | 0.204 | 0.300 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.450 | 0.504 | 0.336 | 0.390 | 0.175 | 0.224 | 0.164 | 0.196 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.335 | 1.335 | 1.222 | 1.222 | 0.767 | 0.767 | 0.454 | 0.454 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.248 | 0.249 | 0.135 | 0.136 | 0.068 | 0.069 | 0.066 | 0.068 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.222 | 0.223 | 0.109 | 0.110 | 0.055 | 0.056 | 0.053 | 0.055 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.150 | 0.153 | 0.036 | 0.039 | 0.017 | 0.022 | 0.019 | 0.027 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.121 | 0.123 | 0.008 | 0.009 | 0.004 | 0.005 | 0.004 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.265 | 0.294 | 0.151 | 0.181 | 0.087 | 0.093 | 0.067 | 0.091 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.204 | 0.208 | 0.090 | 0.094 | 0.041 | 0.058 | 0.038 | 0.064 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.357 | 1.357 | 1.244 | 1.244 | 0.790 | 0.790 | 0.454 | 0.454 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.161 | 0.161 | 0.048 | 0.048 | 0.025 | 0.025 | 0.023 | 0.023 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.149 | 0.149 | 0.036 | 0.036 | 0.019 | 0.019 | 0.017 | 0.017 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.122 | 0.123 | 0.009 | 0.010 | 0.004 | 0.005 | 0.004 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.115 | 0.116 | 0.002 | 0.002 | 8.86e-04 | 0.001 | 9.99e-04 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.174 | 0.175 | 0.060 | 0.062 | 0.029 | 0.036 | 0.031 | 0.036 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.173 | 0.175 | 0.059 | 0.062 | 0.027 | 0.030 | 0.030 | 0.035 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | B1 | 100 | 0.930 | 1.000 | 0.298 | 0.306 | 0.034 | 0.043 | 0.015 | 0.028 | 0.019 | 0.030 | 0.000 | 0.050 | 0.020 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.247 | 1.303 | 0.984 | 1.039 | 0.610 | 0.666 | 0.373 | 0.373 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | M1 | 100 | 1.000 | 1.000 | 1.875 | 1.884 | 1.611 | 1.621 | 0.811 | 0.818 | 0.800 | 0.809 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | M2 | 100 | 1.000 | 1.000 | 1.704 | 1.713 | 1.440 | 1.450 | 0.725 | 0.732 | 0.715 | 0.724 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.450 | 0.474 | 0.186 | 0.210 | 0.095 | 0.119 | 0.094 | 0.106 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.401 | 0.412 | 0.138 | 0.148 | 0.069 | 0.077 | 0.068 | 0.077 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.178 | 1.261 | 0.915 | 0.998 | 0.456 | 0.545 | 0.460 | 0.485 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.758 | 0.808 | 0.495 | 0.544 | 0.244 | 0.295 | 0.245 | 0.265 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.303 | 1.358 | 1.039 | 1.094 | 0.666 | 0.721 | 0.373 | 0.373 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.869 | 0.871 | 0.605 | 0.607 | 0.308 | 0.311 | 0.297 | 0.299 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.763 | 0.765 | 0.500 | 0.502 | 0.255 | 0.258 | 0.244 | 0.246 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.296 | 0.300 | 0.033 | 0.036 | 0.015 | 0.021 | 0.018 | 0.025 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.282 | 0.286 | 0.018 | 0.023 | 0.009 | 0.012 | 0.010 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.546 | 0.573 | 0.283 | 0.309 | 0.136 | 0.161 | 0.148 | 0.169 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.374 | 0.378 | 0.111 | 0.115 | 0.051 | 0.056 | 0.058 | 0.064 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.358 | 1.358 | 1.094 | 1.094 | 0.721 | 0.721 | 0.373 | 0.373 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.513 | 0.514 | 0.250 | 0.251 | 0.131 | 0.131 | 0.119 | 0.120 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.461 | 0.461 | 0.197 | 0.198 | 0.102 | 0.103 | 0.095 | 0.095 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.271 | 0.272 | 0.008 | 0.009 | 0.004 | 0.005 | 0.004 | 0.005 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.267 | 0.268 | 0.004 | 0.004 | 0.002 | 0.002 | 0.002 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.370 | 0.376 | 0.107 | 0.112 | 0.052 | 0.055 | 0.056 | 0.059 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.318 | 0.323 | 0.055 | 0.060 | 0.027 | 0.030 | 0.028 | 0.033 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | B1 | 100 | 0.920 | 1.000 | 0.545 | 0.563 | 0.034 | 0.051 | 0.021 | 0.035 | 0.014 | 0.025 | 0.000 | 0.050 | 0.030 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.244 | 1.299 | 0.732 | 0.788 | 0.507 | 0.562 | 0.225 | 0.225 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.489 | 1.489 | 0.728 | 0.728 | 0.761 | 0.761 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.489 | 1.489 | 0.728 | 0.728 | 0.761 | 0.761 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.959 | 1.003 | 0.447 | 0.492 | 0.266 | 0.299 | 0.189 | 0.218 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.918 | 0.951 | 0.407 | 0.440 | 0.237 | 0.261 | 0.177 | 0.188 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.489 | 1.489 | 0.728 | 0.728 | 0.761 | 0.761 | 0.580 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.371 | 1.471 | 0.860 | 0.960 | 0.471 | 0.514 | 0.425 | 0.491 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.299 | 1.354 | 0.788 | 0.843 | 0.562 | 0.617 | 0.225 | 0.225 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.489 | 1.489 | 0.728 | 0.728 | 0.761 | 0.761 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.489 | 1.489 | 0.728 | 0.728 | 0.761 | 0.761 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.556 | 0.563 | 0.045 | 0.052 | 0.025 | 0.032 | 0.020 | 0.026 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.550 | 0.557 | 0.039 | 0.046 | 0.021 | 0.028 | 0.018 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.082 | 1.113 | 0.571 | 0.602 | 0.304 | 0.308 | 0.268 | 0.297 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.631 | 0.651 | 0.119 | 0.140 | 0.068 | 0.075 | 0.051 | 0.071 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.354 | 1.354 | 0.843 | 0.843 | 0.617 | 0.617 | 0.225 | 0.225 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | M1 | 30 | 1.000 | 1.000 | 1.450 | 1.452 | 0.938 | 0.940 | 0.483 | 0.485 | 0.455 | 0.456 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | M2 | 30 | 1.000 | 1.000 | 1.232 | 1.234 | 0.720 | 0.722 | 0.374 | 0.376 | 0.346 | 0.347 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.520 | 0.522 | 0.009 | 0.010 | 0.005 | 0.006 | 0.004 | 0.005 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.518 | 0.520 | 0.007 | 0.008 | 0.004 | 0.005 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.647 | 0.657 | 0.136 | 0.146 | 0.068 | 0.075 | 0.068 | 0.075 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.557 | 0.562 | 0.045 | 0.051 | 0.021 | 0.028 | 0.023 | 0.028 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | B1 | 100 | 0.910 | 1.000 | 0.735 | 0.753 | 0.040 | 0.058 | 0.025 | 0.049 | 0.010 | 0.019 | 0.000 | 0.050 | 0.040 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.236 | 1.290 | 0.540 | 0.595 | 0.411 | 0.466 | 0.129 | 0.129 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 0.970 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 0.950 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 0.980 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | M6 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 0.900 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.290 | 1.345 | 0.595 | 0.650 | 0.466 | 0.520 | 0.129 | 0.129 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.774 | 0.785 | 0.078 | 0.089 | 0.050 | 0.061 | 0.028 | 0.033 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.772 | 0.780 | 0.077 | 0.085 | 0.048 | 0.058 | 0.028 | 0.031 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.913 | 2.000 | 1.218 | 1.305 | 0.630 | 0.630 | 0.588 | 0.675 | 0.170 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.873 | 0.889 | 0.177 | 0.193 | 0.114 | 0.128 | 0.065 | 0.068 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.334 | 1.345 | 0.639 | 0.650 | 0.509 | 0.520 | 0.129 | 0.129 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.305 | 1.305 | 0.630 | 0.630 | 0.675 | 0.675 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.706 | 0.710 | 0.011 | 0.014 | 0.008 | 0.011 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.705 | 0.707 | 0.010 | 0.012 | 0.007 | 0.009 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.919 | 0.936 | 0.223 | 0.240 | 0.141 | 0.153 | 0.084 | 0.088 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.736 | 0.747 | 0.041 | 0.052 | 0.020 | 0.028 | 0.021 | 0.025 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | B1 | 100 | 0.840 | 1.000 | 0.882 | 0.915 | 0.045 | 0.079 | 0.035 | 0.067 | 0.010 | 0.019 | 0.000 | 0.120 | 0.050 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.222 | 1.276 | 0.386 | 0.440 | 0.313 | 0.367 | 0.073 | 0.073 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | M6 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.309 | 1.309 | 0.473 | 0.473 | 0.400 | 0.400 | 0.073 | 0.073 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | M3 | 100 | 1.000 | 1.000 | 1.086 | 1.117 | 0.250 | 0.280 | 0.153 | 0.174 | 0.097 | 0.116 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | M4 | 100 | 1.000 | 1.000 | 1.083 | 1.113 | 0.246 | 0.277 | 0.150 | 0.169 | 0.097 | 0.117 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | M6 | 100 | 1.000 | 1.000 | 1.270 | 1.298 | 0.434 | 0.462 | 0.234 | 0.257 | 0.204 | 0.207 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.330 | 1.330 | 0.494 | 0.494 | 0.421 | 0.421 | 0.073 | 0.073 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.164 | 1.164 | 0.530 | 0.530 | 0.634 | 0.634 | 1.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.851 | 0.858 | 0.014 | 0.022 | 0.012 | 0.020 | 0.003 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.852 | 0.856 | 0.016 | 0.020 | 0.013 | 0.017 | 0.002 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | M5 | 30 | 1.000 | 1.000 | 1.498 | 1.510 | 0.662 | 0.674 | 0.325 | 0.337 | 0.329 | 0.347 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.887 | 0.895 | 0.050 | 0.059 | 0.031 | 0.040 | 0.020 | 0.024 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 1000 | B1 | 100 | 0.890 | 1.000 | 0.264 | 0.275 | 0.034 | 0.044 | 0.014 | 0.024 | 0.021 | 0.031 | 0.000 | 0.090 | 0.020 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.252 | 1.295 | 1.022 | 1.065 | 0.624 | 0.667 | 0.398 | 0.398 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 1000 | M1 | 100 | 1.000 | 1.000 | 1.521 | 1.528 | 1.290 | 1.298 | 0.659 | 0.665 | 0.632 | 0.638 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 1000 | M2 | 100 | 1.000 | 1.000 | 1.385 | 1.393 | 1.155 | 1.163 | 0.591 | 0.597 | 0.564 | 0.570 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.478 | 0.499 | 0.248 | 0.268 | 0.129 | 0.151 | 0.121 | 0.135 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.359 | 0.371 | 0.129 | 0.141 | 0.064 | 0.075 | 0.064 | 0.072 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.454 | 1.537 | 1.224 | 1.307 | 0.654 | 0.740 | 0.594 | 0.623 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.875 | 0.913 | 0.645 | 0.683 | 0.345 | 0.383 | 0.309 | 0.329 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.308 | 1.364 | 1.078 | 1.133 | 0.680 | 0.736 | 0.398 | 0.398 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.724 | 0.727 | 0.494 | 0.497 | 0.259 | 0.262 | 0.234 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.641 | 0.643 | 0.410 | 0.413 | 0.218 | 0.220 | 0.192 | 0.194 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.265 | 0.271 | 0.034 | 0.040 | 0.017 | 0.023 | 0.017 | 0.024 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.247 | 0.251 | 0.016 | 0.020 | 0.008 | 0.011 | 0.008 | 0.011 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.633 | 0.661 | 0.403 | 0.431 | 0.195 | 0.222 | 0.209 | 0.212 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.344 | 0.349 | 0.114 | 0.119 | 0.055 | 0.060 | 0.060 | 0.064 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.364 | 1.364 | 1.133 | 1.133 | 0.736 | 0.736 | 0.398 | 0.398 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.436 | 0.437 | 0.206 | 0.207 | 0.112 | 0.113 | 0.094 | 0.095 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.392 | 0.392 | 0.161 | 0.162 | 0.087 | 0.087 | 0.075 | 0.075 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.238 | 0.239 | 0.008 | 0.009 | 0.004 | 0.006 | 0.004 | 0.005 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.234 | 0.234 | 0.004 | 0.004 | 0.002 | 0.002 | 0.002 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.343 | 0.347 | 0.113 | 0.117 | 0.054 | 0.061 | 0.059 | 0.064 | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 | nnn_corr | var | 5.207 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.284 | 0.287 | 0.053 | 0.057 | 0.025 | 0.029 | 0.028 | 0.033 | 0.000 | 0.000 | 0.000 | 0.000 |
<!-- /GEN:grid_F1 -->

#### F2
<!-- GEN:grid_F2 -->
| fam | target | env | Γ | n | method | reps | cov I | cov true | med w | p90 w | med ex | p90 ex | med ex+ | p90 ex+ | med ex− | p90 ex− | triv | miss+ | miss− | incons |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F2 | pair_pop | 0.2 | 1.492 | 1000 | B1 | 100 | 0.890 | 1.000 | 0.078 | 0.096 | 0.038 | 0.057 | 0.026 | 0.052 | 0.012 | 0.020 | 0.000 | 0.050 | 0.060 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.961 | 1.961 | 1.923 | 1.923 | 0.038 | 0.038 | 0.950 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | M1 | 100 | 1.000 | 1.000 | 0.289 | 0.294 | 0.250 | 0.254 | 0.212 | 0.216 | 0.038 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | M2 | 100 | 1.000 | 1.000 | 0.258 | 0.263 | 0.219 | 0.224 | 0.181 | 0.186 | 0.038 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.189 | 0.229 | 0.150 | 0.189 | 0.114 | 0.156 | 0.038 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.103 | 0.117 | 0.064 | 0.078 | 0.033 | 0.048 | 0.029 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.383 | 0.446 | 0.344 | 0.407 | 0.306 | 0.368 | 0.038 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.319 | 0.383 | 0.280 | 0.344 | 0.242 | 0.306 | 0.038 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.961 | 1.961 | 1.923 | 1.923 | 0.038 | 0.038 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.155 | 0.157 | 0.116 | 0.117 | 0.077 | 0.079 | 0.038 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.138 | 0.140 | 0.099 | 0.100 | 0.060 | 0.062 | 0.038 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.079 | 0.087 | 0.040 | 0.048 | 0.028 | 0.039 | 0.011 | 0.018 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.050 | 0.053 | 0.011 | 0.014 | 0.008 | 0.011 | 0.003 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.200 | 0.209 | 0.161 | 0.170 | 0.124 | 0.132 | 0.038 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.122 | 0.135 | 0.082 | 0.096 | 0.062 | 0.073 | 0.019 | 0.030 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | B3 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.961 | 1.961 | 1.923 | 1.923 | 0.038 | 0.038 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.095 | 0.095 | 0.055 | 0.056 | 0.030 | 0.031 | 0.025 | 0.025 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.080 | 0.080 | 0.040 | 0.041 | 0.023 | 0.023 | 0.018 | 0.018 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.049 | 0.052 | 0.009 | 0.013 | 0.007 | 0.009 | 0.002 | 0.005 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.041 | 0.042 | 0.002 | 0.003 | 0.002 | 0.002 | 1.61e-04 | 1.77e-04 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.113 | 0.121 | 0.074 | 0.082 | 0.064 | 0.070 | 0.009 | 0.016 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.104 | 0.111 | 0.065 | 0.071 | 0.061 | 0.067 | 0.004 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | B1 | 100 | 0.930 | 1.000 | 0.140 | 0.173 | 0.055 | 0.088 | 0.046 | 0.083 | 0.008 | 0.012 | 0.000 | 0.040 | 0.030 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.915 | 1.915 | 1.893 | 1.893 | 0.022 | 0.022 | 0.940 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | M1 | 100 | 1.000 | 1.000 | 1.001 | 1.035 | 0.915 | 0.950 | 0.893 | 0.928 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | M2 | 100 | 1.000 | 1.000 | 0.875 | 0.910 | 0.790 | 0.825 | 0.768 | 0.803 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.300 | 0.364 | 0.215 | 0.279 | 0.193 | 0.257 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.235 | 0.279 | 0.150 | 0.194 | 0.128 | 0.172 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.652 | 0.716 | 0.567 | 0.631 | 0.544 | 0.609 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.526 | 0.590 | 0.441 | 0.505 | 0.419 | 0.483 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.915 | 1.915 | 1.893 | 1.893 | 0.022 | 0.022 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.457 | 0.463 | 0.372 | 0.378 | 0.350 | 0.356 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.388 | 0.394 | 0.303 | 0.309 | 0.281 | 0.287 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.151 | 0.167 | 0.066 | 0.082 | 0.052 | 0.072 | 0.014 | 0.018 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.126 | 0.137 | 0.041 | 0.052 | 0.033 | 0.043 | 0.008 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.298 | 0.349 | 0.213 | 0.264 | 0.191 | 0.242 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.226 | 0.235 | 0.141 | 0.150 | 0.119 | 0.127 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | B3 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.915 | 1.915 | 1.893 | 1.893 | 0.022 | 0.022 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.262 | 0.265 | 0.177 | 0.179 | 0.155 | 0.157 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.228 | 0.230 | 0.143 | 0.145 | 0.121 | 0.123 | 0.022 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.102 | 0.107 | 0.017 | 0.022 | 0.014 | 0.020 | 0.002 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.094 | 0.098 | 0.009 | 0.013 | 0.008 | 0.012 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.156 | 0.201 | 0.071 | 0.116 | 0.059 | 0.107 | 0.011 | 0.014 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.143 | 0.153 | 0.058 | 0.068 | 0.055 | 0.063 | 0.003 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | B1 | 100 | 0.970 | 1.000 | 0.293 | 0.360 | 0.104 | 0.171 | 0.101 | 0.169 | 0.003 | 0.004 | 0.000 | 0.020 | 0.010 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.811 | 1.811 | 1.802 | 1.802 | 0.009 | 0.009 | 0.880 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.811 | 1.811 | 1.802 | 1.802 | 0.009 | 0.009 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.811 | 1.811 | 1.802 | 1.802 | 0.009 | 0.009 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.649 | 0.775 | 0.459 | 0.586 | 0.450 | 0.577 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.569 | 0.688 | 0.380 | 0.499 | 0.371 | 0.490 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.277 | 1.336 | 1.088 | 1.147 | 1.079 | 1.138 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.074 | 1.171 | 0.885 | 0.982 | 0.876 | 0.973 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.811 | 1.811 | 1.802 | 1.802 | 0.009 | 0.009 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | M1 | 100 | 1.000 | 1.000 | 1.773 | 1.796 | 1.584 | 1.607 | 1.575 | 1.598 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | M2 | 100 | 1.000 | 1.000 | 1.464 | 1.487 | 1.275 | 1.298 | 1.266 | 1.289 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.337 | 0.399 | 0.148 | 0.210 | 0.139 | 0.201 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.318 | 0.363 | 0.129 | 0.173 | 0.120 | 0.164 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.668 | 0.717 | 0.479 | 0.528 | 0.470 | 0.519 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.432 | 0.488 | 0.243 | 0.299 | 0.234 | 0.290 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | B3 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.811 | 1.811 | 1.802 | 1.802 | 0.009 | 0.009 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.905 | 0.912 | 0.716 | 0.723 | 0.707 | 0.714 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.768 | 0.775 | 0.579 | 0.586 | 0.570 | 0.577 | 0.009 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.223 | 0.240 | 0.033 | 0.051 | 0.031 | 0.049 | 0.002 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.218 | 0.231 | 0.029 | 0.042 | 0.026 | 0.041 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.339 | 0.370 | 0.150 | 0.181 | 0.142 | 0.173 | 0.008 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.252 | 0.291 | 0.063 | 0.101 | 0.060 | 0.100 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | B1 | 100 | 0.930 | 1.000 | 0.598 | 0.754 | 0.202 | 0.358 | 0.201 | 0.357 | 0.001 | 0.002 | 0.000 | 0.050 | 0.020 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.604 | 1.604 | 1.600 | 1.600 | 0.004 | 0.004 | 0.940 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.604 | 1.604 | 1.600 | 1.600 | 0.004 | 0.004 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.604 | 1.604 | 1.600 | 1.600 | 0.004 | 0.004 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | M3 | 100 | 1.000 | 1.000 | 1.219 | 1.425 | 0.823 | 1.029 | 0.819 | 1.025 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | M4 | 100 | 1.000 | 1.000 | 1.165 | 1.318 | 0.769 | 0.922 | 0.765 | 0.918 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.896 | 2.000 | 1.500 | 1.604 | 1.496 | 1.600 | 0.004 | 0.004 | 0.260 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.735 | 1.899 | 1.339 | 1.503 | 1.335 | 1.499 | 0.004 | 0.004 | 0.040 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.604 | 1.604 | 1.600 | 1.600 | 0.004 | 0.004 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.604 | 1.604 | 1.600 | 1.600 | 0.004 | 0.004 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.604 | 1.604 | 1.600 | 1.600 | 0.004 | 0.004 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.680 | 0.790 | 0.284 | 0.394 | 0.280 | 0.390 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.659 | 0.741 | 0.262 | 0.345 | 0.259 | 0.342 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.210 | 1.269 | 0.814 | 0.873 | 0.810 | 0.869 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.833 | 0.928 | 0.437 | 0.531 | 0.433 | 0.528 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | B3 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.604 | 1.604 | 1.600 | 1.600 | 0.004 | 0.004 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.604 | 1.604 | 1.600 | 1.600 | 0.004 | 0.004 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | M2 | 30 | 1.000 | 1.000 | 1.964 | 1.976 | 1.568 | 1.579 | 1.564 | 1.576 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.469 | 0.515 | 0.073 | 0.119 | 0.071 | 0.117 | 0.001 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.470 | 0.503 | 0.074 | 0.107 | 0.073 | 0.105 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.665 | 0.707 | 0.269 | 0.311 | 0.265 | 0.308 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.509 | 0.560 | 0.113 | 0.163 | 0.111 | 0.163 | 0.001 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | B1 | 100 | 0.950 | 1.000 | 1.212 | 1.364 | 0.246 | 0.398 | 0.245 | 0.397 | 5.80e-04 | 8.43e-04 | 0.000 | 0.010 | 0.040 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 0.930 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 0.970 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 0.990 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | M6 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | B3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | M3 | 100 | 1.000 | 1.000 | 1.408 | 1.501 | 0.443 | 0.535 | 0.441 | 0.533 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | M4 | 100 | 1.000 | 1.000 | 1.362 | 1.486 | 0.396 | 0.520 | 0.395 | 0.518 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 0.940 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | M6 | 100 | 1.000 | 1.000 | 1.604 | 1.690 | 0.638 | 0.724 | 0.636 | 0.722 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | B3 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.034 | 1.034 | 1.033 | 1.033 | 0.001 | 0.001 | 1.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | M3 | 30 | 1.000 | 1.000 | 1.090 | 1.159 | 0.124 | 0.193 | 0.123 | 0.192 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | M4 | 30 | 1.000 | 1.000 | 1.081 | 1.123 | 0.115 | 0.157 | 0.113 | 0.156 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | M5 | 30 | 1.000 | 1.000 | 1.364 | 1.411 | 0.398 | 0.445 | 0.396 | 0.444 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | M6 | 30 | 1.000 | 1.000 | 1.134 | 1.187 | 0.168 | 0.221 | 0.168 | 0.221 | 4.38e-04 | 9.81e-04 | 0.000 | 0.000 | 0.000 | 0.000 |
<!-- /GEN:grid_F2 -->

#### F3
<!-- GEN:grid_F3 -->
| fam | target | env | Γ | n | method | reps | cov I | cov true | med w | p90 w | med ex | p90 ex | med ex+ | p90 ex+ | med ex− | p90 ex− | triv | miss+ | miss− | incons |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F3 | rg2 | 0.2 | 1.492 | 1000 | M1 | 100 | 1.000 | 1.000 | 0.490 | 0.492 | 0.421 | 0.424 | 0.213 | 0.216 | 0.208 | 0.210 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 1000 | M2 | 100 | 1.000 | 1.000 | 0.428 | 0.431 | 0.360 | 0.362 | 0.183 | 0.185 | 0.177 | 0.179 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.165 | 0.181 | 0.096 | 0.113 | 0.046 | 0.054 | 0.053 | 0.065 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.121 | 0.124 | 0.053 | 0.055 | 0.019 | 0.020 | 0.034 | 0.036 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.667 | 0.716 | 0.599 | 0.647 | 0.356 | 0.405 | 0.249 | 0.329 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.402 | 0.428 | 0.333 | 0.359 | 0.201 | 0.209 | 0.136 | 0.169 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.222 | 0.222 | 0.153 | 0.154 | 0.079 | 0.080 | 0.074 | 0.075 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.188 | 0.189 | 0.119 | 0.120 | 0.062 | 0.063 | 0.057 | 0.058 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.083 | 0.085 | 0.015 | 0.017 | 0.006 | 0.009 | 0.008 | 0.011 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.074 | 0.075 | 0.006 | 0.006 | 0.002 | 0.003 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.251 | 0.289 | 0.182 | 0.220 | 0.102 | 0.153 | 0.079 | 0.092 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.142 | 0.151 | 0.073 | 0.083 | 0.051 | 0.053 | 0.023 | 0.030 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.127 | 0.127 | 0.058 | 0.059 | 0.032 | 0.032 | 0.027 | 0.027 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.112 | 0.112 | 0.043 | 0.044 | 0.024 | 0.025 | 0.019 | 0.019 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.072 | 0.073 | 0.004 | 0.004 | 0.002 | 0.002 | 0.002 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.069 | 0.069 | 6.11e-04 | 7.38e-04 | 3.32e-04 | 4.64e-04 | 3.00e-04 | 4.01e-04 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.142 | 0.142 | 0.073 | 0.074 | 0.050 | 0.053 | 0.023 | 0.025 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.2 | 1.492 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.130 | 0.131 | 0.061 | 0.063 | 0.049 | 0.052 | 0.011 | 0.013 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 1000 | M1 | 100 | 1.000 | 1.000 | 1.341 | 1.348 | 1.216 | 1.222 | 0.898 | 0.904 | 0.318 | 0.318 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 1000 | M2 | 100 | 1.000 | 1.000 | 1.216 | 1.223 | 1.091 | 1.097 | 0.773 | 0.779 | 0.318 | 0.318 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.298 | 0.306 | 0.172 | 0.180 | 0.073 | 0.079 | 0.100 | 0.109 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.255 | 0.259 | 0.129 | 0.134 | 0.050 | 0.053 | 0.079 | 0.082 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.993 | 0.998 | 0.867 | 0.872 | 0.549 | 0.554 | 0.318 | 0.318 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.583 | 0.603 | 0.457 | 0.478 | 0.250 | 0.255 | 0.207 | 0.226 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.796 | 0.798 | 0.670 | 0.673 | 0.352 | 0.354 | 0.318 | 0.318 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.662 | 0.664 | 0.537 | 0.539 | 0.283 | 0.285 | 0.253 | 0.254 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.142 | 0.143 | 0.017 | 0.018 | 0.008 | 0.010 | 0.009 | 0.011 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.138 | 0.139 | 0.012 | 0.013 | 0.005 | 0.006 | 0.007 | 0.008 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.459 | 0.461 | 0.334 | 0.335 | 0.201 | 0.202 | 0.133 | 0.134 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.197 | 0.207 | 0.071 | 0.081 | 0.050 | 0.052 | 0.021 | 0.030 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.414 | 0.414 | 0.288 | 0.288 | 0.159 | 0.159 | 0.129 | 0.129 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.347 | 0.347 | 0.221 | 0.222 | 0.123 | 0.123 | 0.099 | 0.099 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.128 | 0.129 | 0.003 | 0.003 | 0.001 | 0.002 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.127 | 0.127 | 0.001 | 0.002 | 7.01e-04 | 9.48e-04 | 5.99e-04 | 7.84e-04 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.206 | 0.207 | 0.081 | 0.082 | 0.050 | 0.052 | 0.031 | 0.032 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 0.55 | 3.004 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.185 | 0.186 | 0.060 | 0.061 | 0.049 | 0.052 | 0.010 | 0.011 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.789 | 1.789 | 1.518 | 1.518 | 0.271 | 0.271 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.789 | 1.789 | 1.518 | 1.518 | 0.271 | 0.271 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.727 | 0.734 | 0.516 | 0.523 | 0.245 | 0.252 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.699 | 0.702 | 0.488 | 0.491 | 0.217 | 0.220 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.461 | 1.463 | 1.249 | 1.252 | 0.978 | 0.981 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.020 | 1.024 | 0.809 | 0.813 | 0.538 | 0.542 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 10000 | M1 | 100 | 1.000 | 1.000 | 1.958 | 1.962 | 1.747 | 1.751 | 1.476 | 1.480 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 10000 | M2 | 100 | 1.000 | 1.000 | 1.649 | 1.653 | 1.438 | 1.442 | 1.167 | 1.171 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.244 | 0.247 | 0.033 | 0.035 | 0.015 | 0.018 | 0.018 | 0.019 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.241 | 0.244 | 0.030 | 0.032 | 0.014 | 0.016 | 0.016 | 0.017 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.874 | 0.876 | 0.663 | 0.665 | 0.392 | 0.393 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.295 | 0.297 | 0.084 | 0.086 | 0.049 | 0.052 | 0.035 | 0.036 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 100000 | M1 | 30 | 1.000 | 1.000 | 1.093 | 1.094 | 0.881 | 0.882 | 0.610 | 0.611 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.956 | 0.957 | 0.745 | 0.746 | 0.474 | 0.475 | 0.271 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.214 | 0.215 | 0.003 | 0.004 | 0.002 | 0.002 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.214 | 0.214 | 0.002 | 0.003 | 0.001 | 0.002 | 9.34e-04 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.361 | 0.363 | 0.150 | 0.152 | 0.097 | 0.100 | 0.052 | 0.053 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.15 | 9.974 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.268 | 0.270 | 0.057 | 0.059 | 0.048 | 0.051 | 0.009 | 0.010 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.719 | 1.719 | 1.483 | 1.483 | 0.236 | 0.236 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.719 | 1.719 | 1.483 | 1.483 | 0.236 | 0.236 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 1000 | M3 | 100 | 1.000 | 1.000 | 1.389 | 1.397 | 1.108 | 1.116 | 0.872 | 0.880 | 0.236 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 1000 | M4 | 100 | 1.000 | 1.000 | 1.362 | 1.368 | 1.081 | 1.086 | 0.844 | 0.850 | 0.236 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.904 | 1.905 | 1.623 | 1.624 | 1.387 | 1.388 | 0.236 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.519 | 1.524 | 1.238 | 1.243 | 1.002 | 1.007 | 0.236 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.719 | 1.719 | 1.483 | 1.483 | 0.236 | 0.236 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.719 | 1.719 | 1.483 | 1.483 | 0.236 | 0.236 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.361 | 0.363 | 0.079 | 0.082 | 0.037 | 0.040 | 0.042 | 0.044 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.358 | 0.362 | 0.077 | 0.081 | 0.035 | 0.039 | 0.041 | 0.042 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.330 | 1.332 | 1.049 | 1.051 | 0.813 | 0.815 | 0.236 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.492 | 0.495 | 0.211 | 0.214 | 0.143 | 0.146 | 0.068 | 0.069 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.719 | 1.719 | 1.483 | 1.483 | 0.236 | 0.236 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 100000 | M2 | 30 | 1.000 | 1.000 | 1.796 | 1.798 | 1.515 | 1.517 | 1.279 | 1.281 | 0.236 | 0.236 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.285 | 0.286 | 0.004 | 0.005 | 0.002 | 0.003 | 0.002 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.285 | 0.286 | 0.004 | 0.005 | 0.002 | 0.003 | 0.002 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.623 | 0.626 | 0.342 | 0.345 | 0.191 | 0.195 | 0.152 | 0.153 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 1.7 | 29.964 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.336 | 0.338 | 0.055 | 0.057 | 0.047 | 0.050 | 0.008 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 1000 | M6 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 0.510 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.711 | 0.713 | 0.358 | 0.361 | 0.153 | 0.155 | 0.205 | 0.205 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.708 | 0.711 | 0.355 | 0.358 | 0.150 | 0.153 | 0.205 | 0.205 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.860 | 1.861 | 1.508 | 1.508 | 1.303 | 1.303 | 0.205 | 0.205 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.929 | 0.934 | 0.577 | 0.581 | 0.372 | 0.376 | 0.205 | 0.205 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.647 | 1.647 | 1.442 | 1.442 | 0.205 | 0.205 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.362 | 0.364 | 0.009 | 0.011 | 0.006 | 0.007 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.361 | 0.363 | 0.009 | 0.010 | 0.005 | 0.007 | 0.004 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 100000 | M5 | 30 | 1.000 | 1.000 | 1.162 | 1.165 | 0.809 | 0.812 | 0.604 | 0.607 | 0.205 | 0.205 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | rg2 | 2.3 | 99.484 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.406 | 0.415 | 0.054 | 0.062 | 0.046 | 0.050 | 0.008 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 1000 | B3 | 100 | 1.000 | 1.000 | 0.787 | 0.800 | 0.706 | 0.719 | 0.353 | 0.362 | 0.357 | 0.358 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 1000 | M1 | 100 | 1.000 | 1.000 | 0.496 | 0.499 | 0.415 | 0.418 | 0.208 | 0.211 | 0.206 | 0.208 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 1000 | M2 | 100 | 1.000 | 1.000 | 0.435 | 0.437 | 0.353 | 0.356 | 0.178 | 0.181 | 0.176 | 0.178 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.183 | 0.199 | 0.102 | 0.118 | 0.050 | 0.066 | 0.052 | 0.064 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.131 | 0.134 | 0.050 | 0.052 | 0.022 | 0.025 | 0.027 | 0.030 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.627 | 0.714 | 0.545 | 0.633 | 0.331 | 0.411 | 0.218 | 0.310 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.409 | 0.445 | 0.328 | 0.363 | 0.174 | 0.216 | 0.140 | 0.172 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.228 | 0.229 | 0.147 | 0.148 | 0.074 | 0.075 | 0.072 | 0.073 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.194 | 0.195 | 0.113 | 0.114 | 0.058 | 0.058 | 0.056 | 0.056 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.104 | 0.107 | 0.022 | 0.025 | 0.010 | 0.014 | 0.012 | 0.016 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.087 | 0.088 | 0.006 | 0.007 | 0.003 | 0.004 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.266 | 0.268 | 0.185 | 0.187 | 0.125 | 0.129 | 0.060 | 0.064 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.161 | 0.164 | 0.080 | 0.082 | 0.041 | 0.045 | 0.036 | 0.041 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.133 | 0.133 | 0.052 | 0.052 | 0.027 | 0.027 | 0.025 | 0.025 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.118 | 0.119 | 0.037 | 0.037 | 0.019 | 0.020 | 0.018 | 0.018 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.087 | 0.088 | 0.005 | 0.006 | 0.003 | 0.003 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.082 | 0.082 | 0.001 | 0.001 | 5.14e-04 | 6.87e-04 | 5.10e-04 | 6.63e-04 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.143 | 0.145 | 0.061 | 0.064 | 0.042 | 0.045 | 0.018 | 0.023 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.2 | 1.492 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.142 | 0.144 | 0.060 | 0.062 | 0.042 | 0.044 | 0.018 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 1000 | B3 | 100 | 1.000 | 1.000 | 0.782 | 0.794 | 0.613 | 0.625 | 0.309 | 0.318 | 0.309 | 0.310 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 1000 | M1 | 100 | 1.000 | 1.000 | 1.617 | 1.622 | 1.448 | 1.453 | 0.883 | 0.888 | 0.565 | 0.565 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 1000 | M2 | 100 | 1.000 | 1.000 | 1.492 | 1.497 | 1.323 | 1.328 | 0.758 | 0.763 | 0.565 | 0.565 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.345 | 0.354 | 0.176 | 0.185 | 0.082 | 0.092 | 0.094 | 0.104 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.300 | 0.305 | 0.131 | 0.136 | 0.059 | 0.063 | 0.071 | 0.076 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.203 | 1.247 | 1.034 | 1.078 | 0.572 | 0.651 | 0.455 | 0.509 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.670 | 0.690 | 0.501 | 0.522 | 0.282 | 0.292 | 0.219 | 0.242 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.819 | 0.821 | 0.650 | 0.652 | 0.338 | 0.339 | 0.313 | 0.314 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.681 | 0.683 | 0.512 | 0.514 | 0.269 | 0.270 | 0.244 | 0.245 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.188 | 0.190 | 0.020 | 0.022 | 0.009 | 0.012 | 0.011 | 0.013 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.182 | 0.184 | 0.013 | 0.015 | 0.006 | 0.008 | 0.007 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.476 | 0.501 | 0.308 | 0.332 | 0.167 | 0.205 | 0.128 | 0.130 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.246 | 0.248 | 0.077 | 0.079 | 0.041 | 0.044 | 0.037 | 0.039 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.432 | 0.433 | 0.264 | 0.265 | 0.144 | 0.145 | 0.119 | 0.120 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.371 | 0.372 | 0.202 | 0.203 | 0.114 | 0.114 | 0.089 | 0.089 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.172 | 0.173 | 0.004 | 0.004 | 0.002 | 0.002 | 0.002 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.171 | 0.171 | 0.002 | 0.002 | 0.001 | 0.001 | 8.82e-04 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.246 | 0.247 | 0.077 | 0.079 | 0.041 | 0.043 | 0.036 | 0.039 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 0.55 | 3.004 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.227 | 0.229 | 0.059 | 0.060 | 0.041 | 0.043 | 0.018 | 0.020 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 1000 | B1 | 100 | 0.930 | 1.000 | 0.313 | 0.320 | 0.018 | 0.025 | 0.010 | 0.016 | 0.008 | 0.015 | 0.000 | 0.020 | 0.050 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 1000 | B3 | 100 | 1.000 | 1.000 | 0.776 | 0.787 | 0.481 | 0.492 | 0.241 | 0.250 | 0.243 | 0.244 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.705 | 1.705 | 1.213 | 1.213 | 0.492 | 0.492 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.705 | 1.705 | 1.213 | 1.213 | 0.492 | 0.492 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.928 | 0.951 | 0.633 | 0.656 | 0.285 | 0.304 | 0.347 | 0.367 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.869 | 0.886 | 0.574 | 0.591 | 0.256 | 0.265 | 0.319 | 0.334 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.883 | 1.922 | 1.588 | 1.627 | 1.096 | 1.135 | 0.492 | 0.492 | 0.010 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.375 | 1.414 | 1.080 | 1.119 | 0.591 | 0.628 | 0.484 | 0.492 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.705 | 1.705 | 1.213 | 1.213 | 0.492 | 0.492 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 10000 | M2 | 100 | 1.000 | 1.000 | 1.923 | 1.927 | 1.628 | 1.632 | 1.136 | 1.140 | 0.492 | 0.492 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.332 | 0.335 | 0.036 | 0.040 | 0.018 | 0.020 | 0.019 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.329 | 0.333 | 0.034 | 0.038 | 0.016 | 0.018 | 0.018 | 0.020 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.060 | 1.075 | 0.765 | 0.780 | 0.430 | 0.432 | 0.334 | 0.349 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.420 | 0.423 | 0.125 | 0.128 | 0.078 | 0.081 | 0.047 | 0.050 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 100000 | M1 | 30 | 1.000 | 1.000 | 1.366 | 1.367 | 1.071 | 1.072 | 0.580 | 0.580 | 0.492 | 0.492 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 100000 | M2 | 30 | 1.000 | 1.000 | 1.102 | 1.103 | 0.807 | 0.808 | 0.443 | 0.444 | 0.364 | 0.364 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.299 | 0.300 | 0.004 | 0.005 | 0.002 | 0.003 | 0.002 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.298 | 0.299 | 0.003 | 0.004 | 0.002 | 0.002 | 0.002 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.436 | 0.439 | 0.141 | 0.144 | 0.078 | 0.081 | 0.064 | 0.065 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.15 | 9.974 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.349 | 0.352 | 0.054 | 0.057 | 0.038 | 0.041 | 0.016 | 0.018 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.595 | 1.595 | 1.168 | 1.168 | 0.427 | 0.427 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.595 | 1.595 | 1.168 | 1.168 | 0.427 | 0.427 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 1000 | M3 | 100 | 1.000 | 1.000 | 1.885 | 1.931 | 1.479 | 1.526 | 1.053 | 1.099 | 0.427 | 0.427 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 1000 | M4 | 100 | 1.000 | 1.000 | 1.857 | 1.911 | 1.451 | 1.506 | 1.025 | 1.079 | 0.427 | 0.427 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.595 | 1.595 | 1.168 | 1.168 | 0.427 | 0.427 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.924 | 1.966 | 1.519 | 1.561 | 1.092 | 1.134 | 0.427 | 0.427 | 0.100 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.595 | 1.595 | 1.168 | 1.168 | 0.427 | 0.427 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.595 | 1.595 | 1.168 | 1.168 | 0.427 | 0.427 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.497 | 0.503 | 0.092 | 0.097 | 0.041 | 0.045 | 0.051 | 0.056 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.495 | 0.502 | 0.089 | 0.096 | 0.040 | 0.043 | 0.050 | 0.055 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.699 | 1.737 | 1.294 | 1.331 | 0.867 | 0.905 | 0.427 | 0.427 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.613 | 0.619 | 0.207 | 0.213 | 0.113 | 0.116 | 0.094 | 0.101 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.595 | 1.595 | 1.168 | 1.168 | 0.427 | 0.427 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.595 | 1.595 | 1.168 | 1.168 | 0.427 | 0.427 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.412 | 0.413 | 0.007 | 0.008 | 0.003 | 0.004 | 0.004 | 0.005 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.412 | 0.413 | 0.006 | 0.008 | 0.003 | 0.004 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.746 | 0.762 | 0.340 | 0.356 | 0.189 | 0.192 | 0.151 | 0.166 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 1.7 | 29.964 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.458 | 0.463 | 0.053 | 0.058 | 0.038 | 0.041 | 0.015 | 0.019 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 1000 | M6 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.925 | 0.934 | 0.405 | 0.415 | 0.180 | 0.187 | 0.224 | 0.232 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.920 | 0.929 | 0.401 | 0.409 | 0.178 | 0.183 | 0.221 | 0.229 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 10000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 10000 | M6 | 100 | 1.000 | 1.000 | 1.240 | 1.253 | 0.720 | 0.734 | 0.434 | 0.436 | 0.288 | 0.300 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.481 | 1.481 | 1.123 | 1.123 | 0.357 | 0.357 | 1.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.530 | 0.532 | 0.011 | 0.012 | 0.005 | 0.007 | 0.006 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.531 | 0.532 | 0.011 | 0.013 | 0.005 | 0.006 | 0.006 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 100000 | M5 | 30 | 1.000 | 1.000 | 1.565 | 1.567 | 1.046 | 1.048 | 0.688 | 0.691 | 0.357 | 0.357 | 0.000 | 0.000 | 0.000 | 0.000 |
| F3 | stress | 2.3 | 99.484 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.573 | 0.578 | 0.053 | 0.059 | 0.037 | 0.041 | 0.015 | 0.022 | 0.000 | 0.000 | 0.000 | 0.000 |
<!-- /GEN:grid_F3 -->

#### F4
<!-- GEN:grid_F4 -->
| fam | target | env | Γ | n | method | reps | cov I | cov true | med w | p90 w | med ex | p90 ex | med ex+ | p90 ex+ | med ex− | p90 ex− | triv | miss+ | miss− | incons |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.032 | 1.106 | 0.965 | 1.038 | 0.491 | 0.545 | 0.460 | 0.526 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | M1 | 100 | 1.000 | 1.000 | 0.448 | 0.450 | 0.380 | 0.382 | 0.190 | 0.192 | 0.190 | 0.192 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | M2 | 100 | 1.000 | 1.000 | 0.406 | 0.408 | 0.338 | 0.340 | 0.169 | 0.171 | 0.169 | 0.171 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.155 | 0.158 | 0.087 | 0.090 | 0.042 | 0.056 | 0.045 | 0.055 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.116 | 0.119 | 0.048 | 0.051 | 0.022 | 0.026 | 0.026 | 0.029 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.459 | 0.469 | 0.391 | 0.401 | 0.205 | 0.216 | 0.184 | 0.199 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.317 | 0.344 | 0.249 | 0.276 | 0.135 | 0.147 | 0.126 | 0.138 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.217 | 1.306 | 1.149 | 1.238 | 0.582 | 0.633 | 0.563 | 0.612 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.201 | 0.201 | 0.133 | 0.134 | 0.066 | 0.067 | 0.066 | 0.067 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.175 | 0.175 | 0.107 | 0.108 | 0.054 | 0.054 | 0.053 | 0.054 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.089 | 0.090 | 0.021 | 0.022 | 0.011 | 0.015 | 0.010 | 0.014 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.073 | 0.074 | 0.006 | 0.006 | 0.003 | 0.003 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.193 | 0.219 | 0.126 | 0.152 | 0.071 | 0.075 | 0.059 | 0.080 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.130 | 0.131 | 0.062 | 0.063 | 0.035 | 0.039 | 0.027 | 0.031 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.404 | 1.455 | 1.336 | 1.387 | 0.685 | 0.717 | 0.650 | 0.693 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.114 | 0.114 | 0.046 | 0.046 | 0.023 | 0.023 | 0.023 | 0.023 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.102 | 0.102 | 0.034 | 0.034 | 0.017 | 0.017 | 0.017 | 0.017 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.073 | 0.073 | 0.005 | 0.005 | 0.002 | 0.003 | 0.003 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.069 | 0.069 | 0.001 | 0.001 | 5.34e-04 | 7.06e-04 | 5.51e-04 | 7.36e-04 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.130 | 0.131 | 0.062 | 0.063 | 0.035 | 0.037 | 0.027 | 0.030 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.129 | 0.131 | 0.062 | 0.063 | 0.035 | 0.036 | 0.026 | 0.028 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.022 | 1.106 | 0.838 | 0.922 | 0.427 | 0.477 | 0.420 | 0.469 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | M1 | 100 | 1.000 | 1.000 | 1.719 | 1.724 | 1.535 | 1.540 | 0.777 | 0.781 | 0.759 | 0.759 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | M2 | 100 | 1.000 | 1.000 | 1.566 | 1.571 | 1.382 | 1.387 | 0.691 | 0.695 | 0.691 | 0.695 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.321 | 0.331 | 0.137 | 0.147 | 0.068 | 0.080 | 0.072 | 0.084 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.290 | 0.295 | 0.106 | 0.111 | 0.052 | 0.056 | 0.054 | 0.059 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | M5 | 100 | 1.000 | 1.000 | 0.815 | 0.874 | 0.631 | 0.690 | 0.337 | 0.406 | 0.298 | 0.366 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | M6 | 100 | 1.000 | 1.000 | 0.525 | 0.555 | 0.341 | 0.371 | 0.174 | 0.207 | 0.162 | 0.186 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.228 | 1.308 | 1.044 | 1.124 | 0.539 | 0.595 | 0.503 | 0.548 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | M1 | 100 | 1.000 | 1.000 | 0.729 | 0.731 | 0.545 | 0.547 | 0.273 | 0.274 | 0.272 | 0.274 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | M2 | 100 | 1.000 | 1.000 | 0.624 | 0.625 | 0.440 | 0.441 | 0.220 | 0.221 | 0.219 | 0.221 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.204 | 0.206 | 0.020 | 0.023 | 0.010 | 0.013 | 0.010 | 0.013 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.196 | 0.199 | 0.012 | 0.015 | 0.006 | 0.008 | 0.006 | 0.008 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.384 | 0.386 | 0.200 | 0.202 | 0.102 | 0.106 | 0.097 | 0.100 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.243 | 0.266 | 0.059 | 0.082 | 0.034 | 0.037 | 0.025 | 0.047 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.395 | 1.470 | 1.211 | 1.286 | 0.617 | 0.667 | 0.588 | 0.634 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | M1 | 30 | 1.000 | 1.000 | 0.374 | 0.375 | 0.190 | 0.191 | 0.095 | 0.096 | 0.095 | 0.095 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | M2 | 30 | 1.000 | 1.000 | 0.326 | 0.326 | 0.142 | 0.142 | 0.071 | 0.072 | 0.070 | 0.071 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.188 | 0.189 | 0.004 | 0.005 | 0.002 | 0.003 | 0.002 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.186 | 0.187 | 0.002 | 0.003 | 0.001 | 0.001 | 0.001 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.242 | 0.244 | 0.058 | 0.060 | 0.034 | 0.038 | 0.025 | 0.027 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.241 | 0.244 | 0.057 | 0.060 | 0.033 | 0.035 | 0.024 | 0.027 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.032 | 1.113 | 0.687 | 0.767 | 0.348 | 0.407 | 0.331 | 0.394 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.654 | 1.654 | 0.977 | 0.977 | 0.677 | 0.677 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.654 | 1.654 | 0.977 | 0.977 | 0.677 | 0.677 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | M3 | 100 | 1.000 | 1.000 | 0.830 | 0.856 | 0.484 | 0.510 | 0.240 | 0.262 | 0.240 | 0.266 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | M4 | 100 | 1.000 | 1.000 | 0.788 | 0.806 | 0.442 | 0.460 | 0.217 | 0.230 | 0.224 | 0.245 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | M5 | 100 | 1.000 | 1.000 | 1.839 | 1.905 | 1.493 | 1.560 | 0.836 | 0.884 | 0.677 | 0.677 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.146 | 1.199 | 0.800 | 0.853 | 0.442 | 0.479 | 0.352 | 0.412 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.235 | 1.305 | 0.889 | 0.959 | 0.456 | 0.505 | 0.429 | 0.481 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.654 | 1.654 | 0.977 | 0.977 | 0.677 | 0.677 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.654 | 1.654 | 0.977 | 0.977 | 0.677 | 0.677 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.380 | 0.384 | 0.034 | 0.038 | 0.018 | 0.021 | 0.017 | 0.020 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.377 | 0.381 | 0.031 | 0.035 | 0.016 | 0.019 | 0.014 | 0.018 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | M5 | 100 | 1.000 | 1.000 | 0.880 | 0.902 | 0.534 | 0.557 | 0.313 | 0.316 | 0.239 | 0.242 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.452 | 0.455 | 0.106 | 0.110 | 0.063 | 0.066 | 0.043 | 0.046 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.400 | 1.455 | 1.054 | 1.109 | 0.546 | 0.570 | 0.505 | 0.547 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | M1 | 30 | 1.000 | 1.000 | 1.221 | 1.222 | 0.875 | 0.876 | 0.440 | 0.441 | 0.435 | 0.436 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | M2 | 30 | 1.000 | 1.000 | 1.003 | 1.004 | 0.657 | 0.658 | 0.331 | 0.332 | 0.326 | 0.327 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.351 | 0.352 | 0.005 | 0.006 | 0.002 | 0.003 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.350 | 0.351 | 0.004 | 0.005 | 0.002 | 0.003 | 0.002 | 0.003 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.452 | 0.455 | 0.107 | 0.109 | 0.062 | 0.065 | 0.044 | 0.047 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.399 | 0.401 | 0.053 | 0.055 | 0.031 | 0.033 | 0.021 | 0.025 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.028 | 1.095 | 0.548 | 0.615 | 0.284 | 0.332 | 0.265 | 0.305 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 0.910 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 0.860 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | M6 | 100 | 1.000 | 1.000 | 1.971 | 2.000 | 1.491 | 1.520 | 0.881 | 0.910 | 0.610 | 0.610 | 0.440 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.220 | 1.312 | 0.741 | 0.832 | 0.377 | 0.438 | 0.363 | 0.406 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.555 | 0.561 | 0.075 | 0.082 | 0.038 | 0.044 | 0.037 | 0.041 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.552 | 0.560 | 0.073 | 0.080 | 0.037 | 0.041 | 0.036 | 0.041 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | M5 | 100 | 1.000 | 1.000 | 1.754 | 1.794 | 1.274 | 1.314 | 0.704 | 0.706 | 0.571 | 0.592 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | M6 | 100 | 1.000 | 1.000 | 0.646 | 0.652 | 0.166 | 0.173 | 0.088 | 0.093 | 0.078 | 0.082 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.389 | 1.463 | 0.909 | 0.983 | 0.461 | 0.515 | 0.448 | 0.494 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.520 | 1.520 | 0.910 | 0.910 | 0.610 | 0.610 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.486 | 0.487 | 0.006 | 0.007 | 0.003 | 0.004 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.486 | 0.487 | 0.006 | 0.007 | 0.003 | 0.004 | 0.003 | 0.004 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | M5 | 30 | 1.000 | 1.000 | 0.743 | 0.749 | 0.263 | 0.269 | 0.147 | 0.151 | 0.117 | 0.122 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.529 | 0.534 | 0.049 | 0.054 | 0.031 | 0.034 | 0.019 | 0.024 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | B3 | 100 | 1.000 | 1.000 | 1.040 | 1.114 | 0.425 | 0.499 | 0.215 | 0.270 | 0.206 | 0.257 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | M3 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | M4 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | M6 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | B3 | 100 | 1.000 | 1.000 | 1.226 | 1.293 | 0.611 | 0.678 | 0.319 | 0.372 | 0.292 | 0.340 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | M1 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | M2 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | M3 | 100 | 1.000 | 1.000 | 0.905 | 0.916 | 0.290 | 0.301 | 0.145 | 0.153 | 0.145 | 0.158 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | M4 | 100 | 1.000 | 1.000 | 0.900 | 0.915 | 0.285 | 0.300 | 0.141 | 0.153 | 0.144 | 0.156 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | M5 | 100 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | M6 | 100 | 1.000 | 1.000 | 1.094 | 1.120 | 0.479 | 0.505 | 0.271 | 0.298 | 0.207 | 0.227 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | B3 | 30 | 1.000 | 1.000 | 1.397 | 1.468 | 0.782 | 0.853 | 0.412 | 0.452 | 0.369 | 0.410 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | M1 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | M2 | 30 | 1.000 | 1.000 | 2.000 | 2.000 | 1.385 | 1.385 | 0.843 | 0.843 | 0.542 | 0.542 | 1.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | M3 | 30 | 1.000 | 1.000 | 0.625 | 0.627 | 0.010 | 0.012 | 0.006 | 0.007 | 0.004 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | M4 | 30 | 1.000 | 1.000 | 0.626 | 0.628 | 0.011 | 0.013 | 0.006 | 0.007 | 0.005 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | M5 | 30 | 1.000 | 1.000 | 1.477 | 1.519 | 0.862 | 0.904 | 0.489 | 0.517 | 0.383 | 0.406 | 0.000 | 0.000 | 0.000 | 0.000 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | M6 | 30 | 1.000 | 1.000 | 0.661 | 0.667 | 0.046 | 0.052 | 0.026 | 0.034 | 0.019 | 0.025 | 0.000 | 0.000 | 0.000 | 0.000 |
<!-- /GEN:grid_F4 -->

### 4.4 B2 (maximum-entropy reweighting)

<!-- GEN:b2 -->
| fam | target | env | Γ | n | reps | V− | V+ | true | med B2 | B2 in I | fail | med Kish ESS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | abs_mag | 0.2 | 1.492 | 1000 | 100 | -0.358 | -0.198 | -0.287 | -0.287 | 1.000 | 0.000 | 996.532 |
| F1 | abs_mag | 0.2 | 1.492 | 10000 | 100 | -0.358 | -0.198 | -0.287 | -0.286 | 1.000 | 0.000 | 9980.456 |
| F1 | abs_mag | 0.2 | 1.492 | 100000 | 30 | -0.358 | -0.198 | -0.287 | -0.285 | 1.000 | 0.000 | 9.98e+04 |
| F1 | abs_mag | 0.55 | 3.004 | 1000 | 100 | -0.491 | -0.108 | -0.304 | -0.301 | 1.000 | 0.000 | 981.827 |
| F1 | abs_mag | 0.55 | 3.004 | 10000 | 100 | -0.491 | -0.108 | -0.304 | -0.303 | 1.000 | 0.000 | 9828.600 |
| F1 | abs_mag | 0.55 | 3.004 | 100000 | 30 | -0.491 | -0.108 | -0.304 | -0.302 | 1.000 | 0.000 | 9.83e+04 |
| F1 | abs_mag | 1.15 | 9.974 | 1000 | 100 | -0.674 | 0.043 | -0.328 | -0.320 | 1.000 | 0.000 | 924.653 |
| F1 | abs_mag | 1.15 | 9.974 | 10000 | 100 | -0.674 | 0.043 | -0.328 | -0.323 | 1.000 | 0.000 | 9252.259 |
| F1 | abs_mag | 1.15 | 9.974 | 100000 | 30 | -0.674 | 0.043 | -0.328 | -0.321 | 1.000 | 0.000 | 9.26e+04 |
| F1 | abs_mag | 1.7 | 29.964 | 1000 | 100 | -0.817 | 0.173 | -0.341 | -0.328 | 1.000 | 0.000 | 841.208 |
| F1 | abs_mag | 1.7 | 29.964 | 10000 | 100 | -0.817 | 0.173 | -0.341 | -0.330 | 1.000 | 0.000 | 8406.329 |
| F1 | abs_mag | 1.7 | 29.964 | 100000 | 30 | -0.817 | 0.173 | -0.341 | -0.330 | 1.000 | 0.000 | 8.40e+04 |
| F1 | abs_mag | 2.3 | 99.484 | 1000 | 100 | -0.927 | 0.285 | -0.345 | -0.332 | 1.000 | 0.000 | 719.505 |
| F1 | abs_mag | 2.3 | 99.484 | 10000 | 100 | -0.927 | 0.285 | -0.345 | -0.329 | 1.000 | 0.000 | 7207.939 |
| F1 | abs_mag | 2.3 | 99.484 | 100000 | 30 | -0.927 | 0.285 | -0.345 | -0.329 | 1.000 | 0.000 | 7.21e+04 |
| F1 | abs_mag | var | 5.207 | 1000 | 100 | -0.463 | -0.135 | -0.304 | -0.309 | 1.000 | 0.000 | 980.714 |
| F1 | abs_mag | var | 5.207 | 10000 | 100 | -0.463 | -0.135 | -0.304 | -0.304 | 1.000 | 0.000 | 9817.994 |
| F1 | abs_mag | var | 5.207 | 100000 | 30 | -0.463 | -0.135 | -0.304 | -0.305 | 1.000 | 0.000 | 9.81e+04 |
| F1 | nnn_corr | 0.2 | 1.492 | 1000 | 100 | -0.014 | 0.100 | 0.038 | 0.037 | 1.000 | 0.000 | 997.045 |
| F1 | nnn_corr | 0.2 | 1.492 | 10000 | 100 | -0.014 | 0.100 | 0.038 | 0.038 | 1.000 | 0.000 | 9977.888 |
| F1 | nnn_corr | 0.2 | 1.492 | 100000 | 30 | -0.014 | 0.100 | 0.038 | 0.038 | 1.000 | 0.000 | 9.98e+04 |
| F1 | nnn_corr | 0.55 | 3.004 | 1000 | 100 | -0.095 | 0.168 | 0.032 | 0.033 | 1.000 | 0.000 | 982.393 |
| F1 | nnn_corr | 0.55 | 3.004 | 10000 | 100 | -0.095 | 0.168 | 0.032 | 0.033 | 1.000 | 0.000 | 9832.181 |
| F1 | nnn_corr | 0.55 | 3.004 | 100000 | 30 | -0.095 | 0.168 | 0.032 | 0.033 | 1.000 | 0.000 | 9.84e+04 |
| F1 | nnn_corr | 1.15 | 9.974 | 1000 | 100 | -0.239 | 0.272 | 0.027 | 0.027 | 1.000 | 0.000 | 926.404 |
| F1 | nnn_corr | 1.15 | 9.974 | 10000 | 100 | -0.239 | 0.272 | 0.027 | 0.028 | 1.000 | 0.000 | 9260.964 |
| F1 | nnn_corr | 1.15 | 9.974 | 100000 | 30 | -0.239 | 0.272 | 0.027 | 0.028 | 1.000 | 0.000 | 9.26e+04 |
| F1 | nnn_corr | 1.7 | 29.964 | 1000 | 100 | -0.325 | 0.370 | 0.026 | 0.029 | 1.000 | 0.000 | 843.455 |
| F1 | nnn_corr | 1.7 | 29.964 | 10000 | 100 | -0.325 | 0.370 | 0.026 | 0.028 | 1.000 | 0.000 | 8405.500 |
| F1 | nnn_corr | 1.7 | 29.964 | 100000 | 30 | -0.325 | 0.370 | 0.026 | 0.028 | 1.000 | 0.000 | 8.41e+04 |
| F1 | nnn_corr | 2.3 | 99.484 | 1000 | 100 | -0.366 | 0.470 | 0.029 | 0.032 | 1.000 | 0.000 | 717.175 |
| F1 | nnn_corr | 2.3 | 99.484 | 10000 | 100 | -0.366 | 0.470 | 0.029 | 0.033 | 1.000 | 0.000 | 7213.483 |
| F1 | nnn_corr | 2.3 | 99.484 | 100000 | 30 | -0.366 | 0.470 | 0.029 | 0.033 | 1.000 | 0.000 | 7.21e+04 |
| F1 | nnn_corr | var | 5.207 | 1000 | 100 | -0.077 | 0.153 | 0.029 | 0.029 | 1.000 | 0.000 | 980.357 |
| F1 | nnn_corr | var | 5.207 | 10000 | 100 | -0.077 | 0.153 | 0.029 | 0.030 | 1.000 | 0.000 | 9816.510 |
| F1 | nnn_corr | var | 5.207 | 100000 | 30 | -0.077 | 0.153 | 0.029 | 0.030 | 1.000 | 0.000 | 9.82e+04 |
| F2 | pair_pop | 0.2 | 1.492 | 1000 | 100 | -0.962 | -0.923 | -0.945 | -0.945 | 0.920 | 0.000 | 991.457 |
| F2 | pair_pop | 0.2 | 1.492 | 10000 | 100 | -0.962 | -0.923 | -0.945 | -0.945 | 1.000 | 0.000 | 9937.181 |
| F2 | pair_pop | 0.2 | 1.492 | 100000 | 30 | -0.962 | -0.923 | -0.945 | -0.944 | 1.000 | 0.000 | 9.94e+04 |
| F2 | pair_pop | 0.55 | 3.004 | 1000 | 100 | -0.978 | -0.893 | -0.945 | -0.945 | 1.000 | 0.000 | 964.192 |
| F2 | pair_pop | 0.55 | 3.004 | 10000 | 100 | -0.978 | -0.893 | -0.945 | -0.946 | 1.000 | 0.000 | 9645.134 |
| F2 | pair_pop | 0.55 | 3.004 | 100000 | 30 | -0.978 | -0.893 | -0.945 | -0.945 | 1.000 | 0.000 | 9.64e+04 |
| F2 | pair_pop | 1.15 | 9.974 | 1000 | 100 | -0.991 | -0.802 | -0.946 | -0.947 | 1.000 | 0.000 | 881.751 |
| F2 | pair_pop | 1.15 | 9.974 | 10000 | 100 | -0.991 | -0.802 | -0.946 | -0.947 | 1.000 | 0.000 | 8832.270 |
| F2 | pair_pop | 1.15 | 9.974 | 100000 | 30 | -0.991 | -0.802 | -0.946 | -0.946 | 1.000 | 0.000 | 8.85e+04 |
| F2 | pair_pop | 1.7 | 29.964 | 1000 | 100 | -0.996 | -0.600 | -0.945 | -0.948 | 1.000 | 0.000 | 789.212 |
| F2 | pair_pop | 1.7 | 29.964 | 10000 | 100 | -0.996 | -0.600 | -0.945 | -0.947 | 1.000 | 0.000 | 7893.869 |
| F2 | pair_pop | 1.7 | 29.964 | 100000 | 30 | -0.996 | -0.600 | -0.945 | -0.947 | 1.000 | 0.000 | 7.91e+04 |
| F2 | pair_pop | 2.3 | 99.484 | 1000 | 100 | -0.999 | -0.033 | -0.945 | -0.950 | 1.000 | 0.000 | 666.133 |
| F2 | pair_pop | 2.3 | 99.484 | 10000 | 100 | -0.999 | -0.033 | -0.945 | -0.947 | 1.000 | 0.000 | 6731.762 |
| F2 | pair_pop | 2.3 | 99.484 | 100000 | 30 | -0.999 | -0.033 | -0.945 | -0.947 | 1.000 | 0.000 | 6.72e+04 |
| F3 | rg2 | 0.2 | 1.492 | 1000 | 100 | -0.649 | -0.580 | -0.616 | -0.617 | 1.000 | 0.000 | 997.195 |
| F3 | rg2 | 0.2 | 1.492 | 10000 | 100 | -0.649 | -0.580 | -0.616 | -0.617 | 1.000 | 0.000 | 9989.866 |
| F3 | rg2 | 0.2 | 1.492 | 100000 | 30 | -0.649 | -0.580 | -0.616 | -0.616 | 1.000 | 0.000 | 9.99e+04 |
| F3 | rg2 | 0.55 | 3.004 | 1000 | 100 | -0.682 | -0.556 | -0.622 | -0.622 | 1.000 | 0.000 | 992.323 |
| F3 | rg2 | 0.55 | 3.004 | 10000 | 100 | -0.682 | -0.556 | -0.622 | -0.622 | 1.000 | 0.000 | 9936.160 |
| F3 | rg2 | 0.55 | 3.004 | 100000 | 30 | -0.682 | -0.556 | -0.622 | -0.622 | 1.000 | 0.000 | 9.94e+04 |
| F3 | rg2 | 1.15 | 9.974 | 1000 | 100 | -0.729 | -0.518 | -0.631 | -0.631 | 1.000 | 0.000 | 970.888 |
| F3 | rg2 | 1.15 | 9.974 | 10000 | 100 | -0.729 | -0.518 | -0.631 | -0.631 | 1.000 | 0.000 | 9747.577 |
| F3 | rg2 | 1.15 | 9.974 | 100000 | 30 | -0.729 | -0.518 | -0.631 | -0.631 | 1.000 | 0.000 | 9.75e+04 |
| F3 | rg2 | 1.7 | 29.964 | 1000 | 100 | -0.764 | -0.483 | -0.639 | -0.639 | 1.000 | 0.000 | 941.755 |
| F3 | rg2 | 1.7 | 29.964 | 10000 | 100 | -0.764 | -0.483 | -0.639 | -0.638 | 1.000 | 0.000 | 9448.549 |
| F3 | rg2 | 1.7 | 29.964 | 100000 | 30 | -0.764 | -0.483 | -0.639 | -0.638 | 1.000 | 0.000 | 9.45e+04 |
| F3 | rg2 | 2.3 | 99.484 | 1000 | 100 | -0.795 | -0.442 | -0.646 | -0.646 | 1.000 | 0.000 | 899.395 |
| F3 | rg2 | 2.3 | 99.484 | 10000 | 100 | -0.795 | -0.442 | -0.646 | -0.646 | 1.000 | 0.000 | 9007.956 |
| F3 | rg2 | 2.3 | 99.484 | 100000 | 30 | -0.795 | -0.442 | -0.646 | -0.646 | 1.000 | 0.000 | 9.02e+04 |
| F3 | stress | 0.2 | 1.492 | 1000 | 100 | -0.383 | -0.302 | -0.347 | -0.346 | 1.000 | 0.000 | 997.068 |
| F3 | stress | 0.2 | 1.492 | 10000 | 100 | -0.383 | -0.302 | -0.347 | -0.347 | 1.000 | 0.000 | 9991.095 |
| F3 | stress | 0.2 | 1.492 | 100000 | 30 | -0.383 | -0.302 | -0.347 | -0.347 | 1.000 | 0.000 | 9.99e+04 |
| F3 | stress | 0.55 | 3.004 | 1000 | 100 | -0.435 | -0.267 | -0.355 | -0.356 | 1.000 | 0.000 | 991.727 |
| F3 | stress | 0.55 | 3.004 | 10000 | 100 | -0.435 | -0.267 | -0.355 | -0.355 | 1.000 | 0.000 | 9940.510 |
| F3 | stress | 0.55 | 3.004 | 100000 | 30 | -0.435 | -0.267 | -0.355 | -0.355 | 1.000 | 0.000 | 9.94e+04 |
| F3 | stress | 1.15 | 9.974 | 1000 | 100 | -0.508 | -0.213 | -0.368 | -0.368 | 1.000 | 0.000 | 973.863 |
| F3 | stress | 1.15 | 9.974 | 10000 | 100 | -0.508 | -0.213 | -0.368 | -0.368 | 1.000 | 0.000 | 9742.737 |
| F3 | stress | 1.15 | 9.974 | 100000 | 30 | -0.508 | -0.213 | -0.368 | -0.368 | 1.000 | 0.000 | 9.75e+04 |
| F3 | stress | 1.7 | 29.964 | 1000 | 100 | -0.573 | -0.168 | -0.380 | -0.379 | 1.000 | 0.000 | 942.609 |
| F3 | stress | 1.7 | 29.964 | 10000 | 100 | -0.573 | -0.168 | -0.380 | -0.380 | 1.000 | 0.000 | 9456.388 |
| F3 | stress | 1.7 | 29.964 | 100000 | 30 | -0.573 | -0.168 | -0.380 | -0.379 | 1.000 | 0.000 | 9.45e+04 |
| F3 | stress | 2.3 | 99.484 | 1000 | 100 | -0.643 | -0.123 | -0.392 | -0.391 | 1.000 | 0.000 | 898.123 |
| F3 | stress | 2.3 | 99.484 | 10000 | 100 | -0.643 | -0.123 | -0.392 | -0.391 | 1.000 | 0.000 | 9014.513 |
| F3 | stress | 2.3 | 99.484 | 100000 | 30 | -0.643 | -0.123 | -0.392 | -0.391 | 1.000 | 0.000 | 9.01e+04 |
| F4 | ones_first20 | 0.2 | 1.492 | 1000 | 100 | -0.183 | -0.116 | -0.150 | -0.150 | 1.000 | 0.000 | 998.715 |
| F4 | ones_first20 | 0.2 | 1.492 | 10000 | 100 | -0.183 | -0.116 | -0.150 | -0.150 | 1.000 | 0.000 | 9998.501 |
| F4 | ones_first20 | 0.2 | 1.492 | 100000 | 30 | -0.183 | -0.116 | -0.150 | -0.150 | 1.000 | 0.000 | 1.00e+05 |
| F4 | ones_first20 | 0.55 | 3.004 | 1000 | 100 | -0.241 | -0.057 | -0.151 | -0.151 | 1.000 | 0.000 | 998.830 |
| F4 | ones_first20 | 0.55 | 3.004 | 10000 | 100 | -0.241 | -0.057 | -0.151 | -0.151 | 1.000 | 0.000 | 9997.882 |
| F4 | ones_first20 | 0.55 | 3.004 | 100000 | 30 | -0.241 | -0.057 | -0.151 | -0.151 | 1.000 | 0.000 | 1.00e+05 |
| F4 | ones_first20 | 1.15 | 9.974 | 1000 | 100 | -0.323 | 0.023 | -0.152 | -0.152 | 1.000 | 0.000 | 998.386 |
| F4 | ones_first20 | 1.15 | 9.974 | 10000 | 100 | -0.323 | 0.023 | -0.152 | -0.151 | 1.000 | 0.000 | 9996.257 |
| F4 | ones_first20 | 1.15 | 9.974 | 100000 | 30 | -0.323 | 0.023 | -0.152 | -0.152 | 1.000 | 0.000 | 1.00e+05 |
| F4 | ones_first20 | 1.7 | 29.964 | 1000 | 100 | -0.390 | 0.090 | -0.154 | -0.152 | 1.000 | 0.000 | 997.932 |
| F4 | ones_first20 | 1.7 | 29.964 | 10000 | 100 | -0.390 | 0.090 | -0.154 | -0.153 | 1.000 | 0.000 | 9993.186 |
| F4 | ones_first20 | 1.7 | 29.964 | 100000 | 30 | -0.390 | 0.090 | -0.154 | -0.153 | 1.000 | 0.000 | 9.99e+04 |
| F4 | ones_first20 | 2.3 | 99.484 | 1000 | 100 | -0.458 | 0.157 | -0.155 | -0.154 | 1.000 | 0.000 | 997.778 |
| F4 | ones_first20 | 2.3 | 99.484 | 10000 | 100 | -0.458 | 0.157 | -0.155 | -0.153 | 1.000 | 0.000 | 9988.201 |
| F4 | ones_first20 | 2.3 | 99.484 | 100000 | 30 | -0.458 | 0.157 | -0.155 | -0.154 | 1.000 | 0.000 | 9.99e+04 |
<!-- /GEN:b2 -->

### 4.5 Timings (median seconds per repetition; cells with ρ = 1.15, first target)

<!-- GEN:timings -->
| fam | target | n | method | preproc s | sampling s | optim s | certif s | M3 total s |
|---|---|---|---|---|---|---|---|---|
| F1 | nnn_corr | 1000 | B1 | 0.000 | 4.35e-04 | 1.679 | 0.000 | – |
| F1 | nnn_corr | 1000 | B2 | – | – | – | – | – |
| F1 | nnn_corr | 1000 | B3 | 0.000 | 4.35e-04 | 0.009 | 0.000 | – |
| F1 | nnn_corr | 1000 | M1 | 3.08e-04 | 3.90e-04 | 0.009 | 0.000 | – |
| F1 | nnn_corr | 1000 | M2 | 3.08e-04 | 3.90e-04 | 0.009 | 0.000 | – |
| F1 | nnn_corr | 1000 | M3 | 0.000 | 4.35e-04 | 0.023 | 0.017 | 0.045 |
| F1 | nnn_corr | 1000 | M4 | 3.08e-04 | 3.90e-04 | 0.000 | 0.044 | – |
| F1 | nnn_corr | 1000 | M5 | 0.000 | 4.35e-04 | 0.000 | 8.87e-04 | – |
| F1 | nnn_corr | 1000 | M6 | 0.000 | 4.35e-04 | 0.000 | 0.001 | – |
| F1 | nnn_corr | 10000 | B2 | – | – | – | – | – |
| F1 | nnn_corr | 10000 | B3 | 0.000 | 0.002 | 0.021 | 0.000 | – |
| F1 | nnn_corr | 10000 | M1 | 4.91e-04 | 0.002 | 0.024 | 0.000 | – |
| F1 | nnn_corr | 10000 | M2 | 4.91e-04 | 0.002 | 0.024 | 0.000 | – |
| F1 | nnn_corr | 10000 | M3 | 0.000 | 0.002 | 1.230 | 0.060 | 1.148 |
| F1 | nnn_corr | 10000 | M4 | 4.91e-04 | 0.002 | 0.000 | 1.142 | – |
| F1 | nnn_corr | 10000 | M5 | 0.000 | 0.002 | 0.000 | 0.001 | – |
| F1 | nnn_corr | 10000 | M6 | 0.000 | 0.002 | 0.000 | 5.49e-04 | – |
| F1 | nnn_corr | 100000 | B2 | – | – | – | – | – |
| F1 | nnn_corr | 100000 | B3 | 0.000 | 0.013 | 0.181 | 0.000 | – |
| F1 | nnn_corr | 100000 | M1 | 5.11e-04 | 0.012 | 0.196 | 0.000 | – |
| F1 | nnn_corr | 100000 | M2 | 5.11e-04 | 0.012 | 0.193 | 0.000 | – |
| F1 | nnn_corr | 100000 | M3 | 0.000 | 0.013 | 0.976 | 1.570 | 2.864 |
| F1 | nnn_corr | 100000 | M4 | 5.11e-04 | 0.012 | 0.000 | 2.765 | – |
| F1 | nnn_corr | 100000 | M5 | 0.000 | 0.013 | 0.000 | 0.008 | – |
| F1 | nnn_corr | 100000 | M6 | 0.000 | 0.013 | 0.000 | 0.006 | – |
| F2 | pair_pop | 1000 | B1 | 0.000 | 4.56e-04 | 1.248 | 0.000 | – |
| F2 | pair_pop | 1000 | B2 | – | – | – | – | – |
| F2 | pair_pop | 1000 | B3 | 0.000 | 4.56e-04 | 0.007 | 0.000 | – |
| F2 | pair_pop | 1000 | M1 | 3.43e-04 | 3.88e-04 | 0.007 | 0.000 | – |
| F2 | pair_pop | 1000 | M2 | 3.43e-04 | 3.88e-04 | 0.007 | 0.000 | – |
| F2 | pair_pop | 1000 | M3 | 0.000 | 4.56e-04 | 0.037 | 0.009 | 0.049 |
| F2 | pair_pop | 1000 | M4 | 3.43e-04 | 3.88e-04 | 0.000 | 0.050 | – |
| F2 | pair_pop | 1000 | M5 | 0.000 | 4.56e-04 | 0.000 | 7.42e-04 | – |
| F2 | pair_pop | 1000 | M6 | 0.000 | 4.56e-04 | 0.000 | 0.001 | – |
| F2 | pair_pop | 10000 | B2 | – | – | – | – | – |
| F2 | pair_pop | 10000 | B3 | 0.000 | 0.002 | 0.025 | 0.000 | – |
| F2 | pair_pop | 10000 | M1 | 4.10e-04 | 0.002 | 0.026 | 0.000 | – |
| F2 | pair_pop | 10000 | M2 | 4.10e-04 | 0.002 | 0.023 | 0.000 | – |
| F2 | pair_pop | 10000 | M3 | 0.000 | 0.002 | 2.798 | -0.020 | 2.738 |
| F2 | pair_pop | 10000 | M4 | 4.10e-04 | 0.002 | 0.000 | 2.699 | – |
| F2 | pair_pop | 10000 | M5 | 0.000 | 0.002 | 0.000 | 0.002 | – |
| F2 | pair_pop | 10000 | M6 | 0.000 | 0.002 | 0.000 | 0.002 | – |
| F2 | pair_pop | 100000 | B2 | – | – | – | – | – |
| F2 | pair_pop | 100000 | B3 | 0.000 | 0.016 | 0.273 | 0.000 | – |
| F2 | pair_pop | 100000 | M1 | 5.20e-04 | 0.016 | 0.280 | 0.000 | – |
| F2 | pair_pop | 100000 | M2 | 5.20e-04 | 0.016 | 0.272 | 0.000 | – |
| F2 | pair_pop | 100000 | M3 | 0.000 | 0.016 | 3.083 | 1.603 | 4.697 |
| F2 | pair_pop | 100000 | M4 | 5.20e-04 | 0.016 | 0.000 | 4.669 | – |
| F2 | pair_pop | 100000 | M5 | 0.000 | 0.016 | 0.000 | 0.022 | – |
| F2 | pair_pop | 100000 | M6 | 0.000 | 0.016 | 0.000 | 0.013 | – |
| F3 | stress | 1000 | B1 | 0.000 | 0.001 | 15.899 | 0.000 | – |
| F3 | stress | 1000 | B2 | – | – | – | – | – |
| F3 | stress | 1000 | B3 | 0.000 | 0.001 | 2.324 | 0.000 | – |
| F3 | stress | 1000 | M1 | 0.002 | 0.001 | 0.088 | 0.000 | – |
| F3 | stress | 1000 | M2 | 0.002 | 0.001 | 0.085 | 0.000 | – |
| F3 | stress | 1000 | M3 | 0.000 | 0.001 | 0.092 | 0.029 | 0.110 |
| F3 | stress | 1000 | M4 | 0.002 | 0.001 | 0.000 | 0.115 | – |
| F3 | stress | 1000 | M5 | 0.000 | 0.001 | 0.000 | 8.62e-04 | – |
| F3 | stress | 1000 | M6 | 0.000 | 0.001 | 0.000 | 0.001 | – |
| F3 | stress | 10000 | B2 | – | – | – | – | – |
| F3 | stress | 10000 | M1 | 0.003 | 0.003 | 0.125 | 0.000 | – |
| F3 | stress | 10000 | M2 | 0.003 | 0.003 | 0.124 | 0.000 | – |
| F3 | stress | 10000 | M3 | 0.000 | 0.003 | 0.583 | 0.045 | 0.515 |
| F3 | stress | 10000 | M4 | 0.003 | 0.003 | 0.000 | 0.522 | – |
| F3 | stress | 10000 | M5 | 0.000 | 0.003 | 0.000 | 0.001 | – |
| F3 | stress | 10000 | M6 | 0.000 | 0.003 | 0.000 | 4.49e-04 | – |
| F3 | stress | 100000 | B2 | – | – | – | – | – |
| F3 | stress | 100000 | M1 | 0.002 | 0.023 | 0.376 | 0.000 | – |
| F3 | stress | 100000 | M2 | 0.002 | 0.023 | 0.381 | 0.000 | – |
| F3 | stress | 100000 | M3 | 0.000 | 0.021 | 0.636 | 1.175 | 1.852 |
| F3 | stress | 100000 | M4 | 0.002 | 0.023 | 0.000 | 1.825 | – |
| F3 | stress | 100000 | M5 | 0.000 | 0.021 | 0.000 | 0.007 | – |
| F3 | stress | 100000 | M6 | 0.000 | 0.021 | 0.000 | 0.005 | – |
| F4 | ones_first20 | 1000 | B2 | – | – | – | – | – |
| F4 | ones_first20 | 1000 | B3 | 0.000 | 8.48e-04 | 0.019 | 0.000 | – |
| F4 | ones_first20 | 1000 | M1 | 6.44e-04 | 8.40e-04 | 0.027 | 0.000 | – |
| F4 | ones_first20 | 1000 | M2 | 6.44e-04 | 8.40e-04 | 0.026 | 0.000 | – |
| F4 | ones_first20 | 1000 | M3 | 0.000 | 8.48e-04 | 0.024 | 0.019 | 0.043 |
| F4 | ones_first20 | 1000 | M4 | 6.44e-04 | 8.40e-04 | 0.000 | 0.041 | – |
| F4 | ones_first20 | 1000 | M5 | 0.000 | 8.48e-04 | 0.000 | 9.03e-04 | – |
| F4 | ones_first20 | 1000 | M6 | 0.000 | 8.48e-04 | 0.000 | 9.27e-04 | – |
| F4 | ones_first20 | 10000 | B2 | – | – | – | – | – |
| F4 | ones_first20 | 10000 | B3 | 0.000 | 0.007 | 0.056 | 0.000 | – |
| F4 | ones_first20 | 10000 | M1 | 6.03e-04 | 0.007 | 0.121 | 0.000 | – |
| F4 | ones_first20 | 10000 | M2 | 6.03e-04 | 0.007 | 0.121 | 0.000 | – |
| F4 | ones_first20 | 10000 | M3 | 0.000 | 0.007 | 0.760 | 0.045 | 0.822 |
| F4 | ones_first20 | 10000 | M4 | 6.03e-04 | 0.007 | 0.000 | 0.815 | – |
| F4 | ones_first20 | 10000 | M5 | 0.000 | 0.007 | 0.000 | 8.86e-04 | – |
| F4 | ones_first20 | 10000 | M6 | 0.000 | 0.007 | 0.000 | 4.70e-04 | – |
| F4 | ones_first20 | 100000 | B2 | – | – | – | – | – |
| F4 | ones_first20 | 100000 | B3 | 0.000 | 0.081 | 0.291 | 0.000 | – |
| F4 | ones_first20 | 100000 | M1 | 8.02e-04 | 0.080 | 0.826 | 0.000 | – |
| F4 | ones_first20 | 100000 | M2 | 8.02e-04 | 0.080 | 0.809 | 0.000 | – |
| F4 | ones_first20 | 100000 | M3 | 0.000 | 0.081 | 0.907 | 1.266 | 2.372 |
| F4 | ones_first20 | 100000 | M4 | 8.02e-04 | 0.080 | 0.000 | 2.262 | – |
| F4 | ones_first20 | 100000 | M5 | 0.000 | 0.081 | 0.000 | 0.007 | – |
| F4 | ones_first20 | 100000 | M6 | 0.000 | 0.081 | 0.000 | 0.005 | – |
<!-- /GEN:timings -->

### 4.6 Peak memory (one cell, one repetition, fresh process per method)

<!-- GEN:memory -->
| method | cell | baseline RSS MiB | peak RSS MiB | increase MiB | wall s |
|---|---|---|---|---|---|
| M1 | F1|nnn_corr|1.15|100000 | 86.805 | 103.430 | 16.625 | 0.281 |
| M2 | F1|nnn_corr|1.15|100000 | 86.820 | 103.570 | 16.750 | 0.252 |
| M3 | F1|nnn_corr|1.15|100000 | 86.668 | 127.652 | 40.984 | 2.713 |
| M4 | F1|nnn_corr|1.15|100000 | 86.816 | 127.250 | 40.434 | 2.463 |
| M5 | F1|nnn_corr|1.15|100000 | 86.566 | 127.543 | 40.977 | 2.438 |
| M6 | F1|nnn_corr|1.15|100000 | 86.742 | 127.598 | 40.855 | 2.430 |
| B1 | F1|nnn_corr|1.15|100000 | 86.668 | 105.543 | 18.875 | 1.813 |
| B2 | F1|nnn_corr|1.15|100000 | 86.727 | 106.477 | 19.750 | 0.170 |
| B3 | F1|nnn_corr|1.15|100000 | 86.629 | 106.379 | 19.750 | 0.139 |
<!-- /GEN:memory -->

### 4.7 Sensitivity (a): true half-width 2ρ, declared ρ

<!-- GEN:sens_a -->
| fam | target | declared ρ | Γ | reps | true value | V− (declared class) | V+ | I empty | M3 misses true | M3 covers I | incons. fires | ends cross |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | nnn_corr | 0.200 | 1.492 | 50 | 0.035 | -0.014 | 0.093 | no | 0.000 | 1.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 0.550 | 3.004 | 50 | 0.027 | -0.093 | 0.147 | no | 0.000 | 1.000 | 0.000 | 0.000 |
| F1 | nnn_corr | 1.150 | 9.974 | 50 | 0.029 | -0.200 | 0.236 | no | 0.000 | 1.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.200 | 1.492 | 50 | -0.945 | -0.959 | -0.935 | no | 0.000 | 1.000 | 0.000 | 0.000 |
| F2 | pair_pop | 0.550 | 3.004 | 50 | -0.946 | inf | -inf | yes | 0.000 | – | 0.680 | 0.000 |
| F2 | pair_pop | 1.150 | 9.974 | 50 | -0.945 | inf | -inf | yes | 0.000 | – | 0.940 | 0.000 |
| F3 | stress | 0.200 | 1.492 | 50 | -0.352 | -0.383 | -0.305 | no | 0.000 | 1.000 | 0.000 | 0.000 |
| F3 | stress | 0.550 | 3.004 | 50 | -0.367 | -0.442 | -0.279 | no | 0.000 | 1.000 | 0.000 | 0.000 |
| F3 | stress | 1.150 | 9.974 | 50 | -0.392 | -0.521 | -0.241 | no | 0.000 | 1.000 | 0.000 | 0.000 |
<!-- /GEN:sens_a -->

### 4.8 Sensitivity (b): what the observations add (F1 `nnn_corr`)

<!-- GEN:sens_b -->
| observation | ρ | Γ | reps | V− | V+ | |I| | M3 med width | M3 med excess | M3 covers I |
|---|---|---|---|---|---|---|---|---|---|
| full | 1.150 | 9.974 | 50 | -0.239 | 0.272 | 0.511 | 0.556 | 0.044 | 1.000 |
| one | 1.150 | 9.974 | 50 | -0.277 | 0.307 | 0.584 | 0.627 | 0.042 | 1.000 |
| none | 1.150 | 9.974 | 50 | -0.277 | 0.337 | 0.614 | 0.668 | 0.053 | 1.000 |
| uninformative | 1.150 | 9.974 | 50 | -0.277 | 0.337 | 0.614 | 0.668 | 0.054 | 1.000 |
<!-- /GEN:sens_b -->

### 4.9 Sensitivity (c): displaced regions, inconsistency certificate

<!-- GEN:sens_c -->
| fam | ρ | Γ | displacement | reps | exactly inconsistent | exact Φ | certificate fires | med s |
|---|---|---|---|---|---|---|---|---|
| F1 | 0.200 | 1.492 | 0.000 | 50 | no | -0.067 | 0.000 | 0.088 |
| F1 | 0.200 | 1.492 | 0.050 | 50 | yes | 0.049 | 1.000 | 0.100 |
| F1 | 0.200 | 1.492 | 0.100 | 50 | yes | 0.098 | 1.000 | 0.103 |
| F1 | 0.200 | 1.492 | 0.200 | 50 | yes | 0.192 | 1.000 | 0.106 |
| F1 | 0.200 | 1.492 | 0.300 | 50 | yes | 0.284 | 1.000 | 0.104 |
| F1 | 0.200 | 1.492 | 0.500 | 50 | yes | 0.457 | 1.000 | 0.104 |
| F1 | 0.550 | 3.004 | 0.000 | 50 | no | -0.128 | 0.000 | 0.094 |
| F1 | 0.550 | 3.004 | 0.050 | 50 | yes | 0.051 | 1.000 | 0.113 |
| F1 | 0.550 | 3.004 | 0.100 | 50 | yes | 0.096 | 1.000 | 0.135 |
| F1 | 0.550 | 3.004 | 0.200 | 50 | yes | 0.179 | 1.000 | 0.125 |
| F1 | 0.550 | 3.004 | 0.300 | 50 | yes | 0.253 | 1.000 | 0.109 |
| F1 | 0.550 | 3.004 | 0.500 | 50 | yes | 0.383 | 1.000 | 0.127 |
| F2 | 0.200 | 1.492 | 0.000 | 50 | no | -0.054 | 0.000 | 0.276 |
| F2 | 0.200 | 1.492 | 0.050 | 50 | yes | 0.043 | 0.680 | 2.585 |
| F2 | 0.200 | 1.492 | 0.100 | 50 | yes | 0.086 | 1.000 | 2.508 |
| F2 | 0.200 | 1.492 | 0.200 | 50 | yes | 0.173 | 1.000 | 2.385 |
| F2 | 0.200 | 1.492 | 0.300 | 50 | yes | 0.259 | 1.000 | 3.008 |
| F2 | 0.200 | 1.492 | 0.500 | 50 | yes | 0.432 | 1.000 | 2.171 |
| F2 | 0.550 | 3.004 | 0.000 | 50 | no | -0.073 | 0.000 | 0.378 |
| F2 | 0.550 | 3.004 | 0.050 | 50 | yes | 0.042 | 0.420 | 3.561 |
| F2 | 0.550 | 3.004 | 0.100 | 50 | yes | 0.076 | 1.000 | 2.710 |
| F2 | 0.550 | 3.004 | 0.200 | 50 | yes | 0.144 | 1.000 | 2.292 |
| F2 | 0.550 | 3.004 | 0.300 | 50 | yes | 0.214 | 1.000 | 2.267 |
| F2 | 0.550 | 3.004 | 0.500 | 50 | yes | 0.355 | 1.000 | 2.209 |
| F3 | 0.200 | 1.492 | 0.000 | 50 | no | -0.047 | 0.000 | 2.623 |
| F3 | 0.200 | 1.492 | 0.050 | 50 | yes | 0.059 | 1.000 | 3.252 |
| F3 | 0.200 | 1.492 | 0.100 | 50 | yes | 0.102 | 1.000 | 4.442 |
| F3 | 0.200 | 1.492 | 0.200 | 50 | yes | 0.189 | 1.000 | 1.081 |
| F3 | 0.200 | 1.492 | 0.300 | 50 | yes | 0.274 | 1.000 | 2.020 |
| F3 | 0.200 | 1.492 | 0.500 | 50 | yes | 0.441 | 1.000 | 0.450 |
| F3 | 0.550 | 3.004 | 0.000 | 50 | no | -0.092 | 0.000 | 1.998 |
| F3 | 0.550 | 3.004 | 0.050 | 50 | yes | 0.073 | 1.000 | 2.245 |
| F3 | 0.550 | 3.004 | 0.100 | 50 | yes | 0.108 | 1.000 | 2.207 |
| F3 | 0.550 | 3.004 | 0.200 | 50 | yes | 0.173 | 1.000 | 2.072 |
| F3 | 0.550 | 3.004 | 0.300 | 50 | yes | 0.234 | 1.000 | 0.951 |
| F3 | 0.550 | 3.004 | 0.500 | 50 | yes | 0.354 | 1.000 | 0.402 |
<!-- /GEN:sens_c -->

### 4.10 H-D sweep (F1 `nnn_corr`, M3)

<!-- GEN:sens_d -->
| ρ | Γ | n | reps | M3 med excess | p90 excess | covers I | med s |
|---|---|---|---|---|---|---|---|
| 0.200 | 1.492 | 200 | 20 | 0.525 | 0.768 | 1.000 | 0.034 |
| 0.200 | 1.492 | 500 | 20 | 0.215 | 0.249 | 1.000 | 0.042 |
| 0.200 | 1.492 | 1000 | 20 | 0.126 | 0.140 | 1.000 | 0.064 |
| 0.200 | 1.492 | 2000 | 20 | 0.083 | 0.091 | 1.000 | 0.137 |
| 0.200 | 1.492 | 5000 | 20 | 0.053 | 0.056 | 1.000 | 0.515 |
| 0.200 | 1.492 | 10000 | 20 | 0.037 | 0.039 | 1.000 | 1.529 |
| 0.550 | 3.004 | 200 | 20 | 1.049 | 1.158 | 1.000 | 0.029 |
| 0.550 | 3.004 | 500 | 20 | 0.354 | 0.408 | 1.000 | 0.045 |
| 0.550 | 3.004 | 1000 | 20 | 0.183 | 0.195 | 1.000 | 0.056 |
| 0.550 | 3.004 | 2000 | 20 | 0.100 | 0.116 | 1.000 | 0.118 |
| 0.550 | 3.004 | 5000 | 20 | 0.049 | 0.054 | 1.000 | 0.466 |
| 1.150 | 9.974 | 200 | 20 | 1.489 | 1.489 | 1.000 | 0.012 |
| 1.150 | 9.974 | 500 | 20 | 1.220 | 1.370 | 1.000 | 0.037 |
| 1.150 | 9.974 | 1000 | 20 | 0.448 | 0.478 | 1.000 | 0.055 |
| 1.150 | 9.974 | 2000 | 20 | 0.199 | 0.229 | 1.000 | 0.098 |
| 1.150 | 9.974 | 5000 | 20 | 0.079 | 0.091 | 1.000 | 0.361 |
| 1.150 | 9.974 | 10000 | 20 | 0.046 | 0.055 | 1.000 | 1.217 |
| 1.700 | 29.964 | 200 | 20 | 1.305 | 1.305 | 1.000 | 0.008 |
| 1.700 | 29.964 | 500 | 20 | 1.305 | 1.305 | 1.000 | 0.017 |
| 1.700 | 29.964 | 1000 | 20 | 1.305 | 1.305 | 1.000 | 0.030 |
| 1.700 | 29.964 | 2000 | 20 | 0.659 | 0.692 | 1.000 | 0.082 |
| 1.700 | 29.964 | 5000 | 20 | 0.163 | 0.179 | 1.000 | 0.266 |
| 1.700 | 29.964 | 10000 | 20 | 0.085 | 0.094 | 1.000 | 0.770 |
| 1.700 | 29.964 | 20000 | 20 | 0.030 | 0.039 | 1.000 | 0.907 |
| 2.300 | 99.484 | 200 | 20 | 1.164 | 1.164 | 1.000 | 0.009 |
| 2.300 | 99.484 | 500 | 20 | 1.164 | 1.164 | 1.000 | 0.012 |
| 2.300 | 99.484 | 1000 | 20 | 1.164 | 1.164 | 1.000 | 0.028 |
| 2.300 | 99.484 | 2000 | 20 | 1.164 | 1.164 | 1.000 | 0.050 |
| 2.300 | 99.484 | 5000 | 20 | 0.807 | 0.827 | 1.000 | 0.214 |
| 2.300 | 99.484 | 10000 | 20 | 0.258 | 0.276 | 1.000 | 0.626 |
| 2.300 | 99.484 | 20000 | 20 | 0.055 | 0.067 | 1.000 | 0.778 |
| 2.300 | 99.484 | 50000 | 20 | 0.023 | 0.033 | 1.000 | 1.074 |
<!-- /GEN:sens_d -->

### 4.11 F4: exactness at scale (2¹⁰⁰ states by level counts)

<!-- GEN:f4 -->
| ρ | Γ | cells | Σ prob | level counts s | V− (LP) | V+ (LP) | LP s | V− (descent) | V+ (descent) | descent s | true |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.200 | 1.492 | 33201 | 1.000 | 0.009 | -0.183 | -0.116 | 6.922 | -0.183 | -0.116 | 0.498 | -0.150 |
| 0.550 | 3.004 | 33201 | 1.000 | 0.007 | -0.241 | -0.057 | 8.028 | -0.241 | -0.057 | 0.480 | -0.151 |
| 1.150 | 9.974 | 33201 | 1.000 | 0.007 | -0.323 | 0.023 | 7.111 | -0.323 | 0.023 | 0.646 | -0.152 |
| 1.700 | 29.964 | 33201 | 1.000 | 0.008 | -0.390 | 0.090 | 6.985 | -0.390 | 0.090 | 0.693 | -0.154 |
| 2.300 | 99.484 | 33201 | 1.000 | 0.006 | -0.458 | 0.157 | 6.017 | -0.458 | 0.157 | 0.653 | -0.155 |

Level counts against enumeration (12 sites): max difference 4.16e-17.
<!-- /GEN:f4 -->

### 4.12 F5: bounded influence

Programme (`ci.lp_ratio_class` on the whole cube) against Corollary 9.3 (`ci.additive_interval`):

<!-- GEN:f5_small -->
| sites | slope | target | data | programme lo | programme hi | programme s | Cor. 9.3 lo | Cor. 9.3 hi | Cor. 9.3 s | |diff| |
|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 0.5 | additive | no | 0.014 | 0.210 | 0.051 | 0.014 | 0.210 | 4.67e-04 | 3.30e-17 |
| 8 | 0.5 | additive | yes | 0.061 | 0.192 | 0.067 | 0.061 | 0.192 | 0.114 | 9.89e-14 |
| 8 | 0.5 | one_spin | no | 0.189 | 0.599 | 0.048 | 0.189 | 0.599 | 3.96e-04 | 1.39e-16 |
| 8 | 0.5 | one_spin | yes | 0.189 | 0.599 | 0.113 | 0.189 | 0.599 | 0.038 | 5.55e-17 |
| 8 | 0.5 | two_spin | no | -0.372 | 0.109 | 0.048 | – | – | – | – |
| 8 | 0.5 | two_spin | yes | -0.372 | 0.109 | 0.088 | – | – | – | – |
| 8 | random | additive | no | -0.067 | 0.089 | 0.062 | -0.067 | 0.089 | 4.90e-04 | 4.16e-17 |
| 8 | random | additive | yes | -0.053 | 0.083 | 0.088 | -0.053 | 0.083 | 0.149 | 2.42e-13 |
| 8 | random | one_spin | no | 0.174 | 0.609 | 0.061 | 0.174 | 0.609 | 4.31e-04 | 1.67e-16 |
| 8 | random | one_spin | yes | 0.174 | 0.609 | 0.101 | 0.174 | 0.609 | 0.014 | 2.22e-16 |
| 8 | random | two_spin | no | -0.299 | 0.030 | 0.061 | – | – | – | – |
| 8 | random | two_spin | yes | -0.299 | 0.030 | 0.081 | – | – | – | – |
| 12 | 0.5 | additive | no | 0.149 | 0.282 | 12.023 | 0.149 | 0.282 | 6.18e-04 | 2.22e-16 |
| 12 | 0.5 | additive | yes | 0.149 | 0.282 | 12.265 | 0.149 | 0.282 | 0.090 | 5.55e-17 |
| 12 | 0.5 | one_spin | no | -0.577 | -0.157 | 14.477 | -0.577 | -0.157 | 5.93e-04 | 1.94e-16 |
| 12 | 0.5 | one_spin | yes | -0.577 | -0.157 | 40.326 | -0.577 | -0.157 | 0.116 | 9.99e-16 |
| 12 | 0.5 | two_spin | no | -0.433 | 0.037 | 16.310 | – | – | – | – |
| 12 | 0.5 | two_spin | yes | -0.433 | 0.037 | 35.942 | – | – | – | – |
| 12 | random | additive | no | 0.163 | 0.308 | 14.353 | 0.163 | 0.308 | 6.38e-04 | 6.94e-16 |
| 12 | random | additive | yes | 0.163 | 0.308 | 14.206 | 0.163 | 0.308 | 0.100 | 6.66e-16 |
| 12 | random | one_spin | no | -0.598 | -0.126 | 28.186 | -0.598 | -0.126 | 7.01e-04 | 5.55e-16 |
| 12 | random | one_spin | yes | -0.598 | -0.126 | 74.552 | -0.598 | -0.126 | 0.022 | 8.88e-16 |
| 12 | random | two_spin | no | -0.497 | 0.129 | 23.439 | – | – | – | – |
| 12 | random | two_spin | yes | -0.497 | 0.129 | 47.524 | – | – | – | – |
<!-- /GEN:f5_small -->

Corollary 9.3 at 50 and 200 sites:

<!-- GEN:f5_big -->
| sites | slope | target | lo | hi | s | true | covers true |
|---|---|---|---|---|---|---|---|
| 50 | 0.5 | additive | -0.063 | 0.068 | 1.187 | 0.006 | yes |
| 50 | 0.5 | one_spin | -0.436 | 0.033 | 0.711 | -0.144 | yes |
| 50 | random | additive | -0.053 | 0.117 | 1.050 | 0.024 | yes |
| 50 | random | one_spin | -0.590 | 0.240 | 0.709 | -0.514 | yes |
| 200 | 0.5 | additive | -0.119 | 0.031 | 2.696 | -0.043 | yes |
| 200 | 0.5 | one_spin | -0.501 | -0.051 | 2.486 | -0.186 | yes |
| 200 | random | additive | -0.144 | 0.015 | 2.572 | -0.069 | yes |
| 200 | random | one_spin | -0.645 | 0.163 | 2.637 | -0.122 | yes |
<!-- /GEN:f5_big -->

Box hull of the class (ratio e^{0.5·n}), target one spin, no data:

<!-- GEN:f5_hull -->
| sites | hull lo | hull hi | gap to [−1,1] | class lo (closed form) | class hi | Cor. 9.3 lo | Cor. 9.3 hi |
|---|---|---|---|---|---|---|---|
| 8 | -0.915 | 0.985 | 0.085 | 0.189 | 0.599 | 0.189 | 0.599 |
| 12 | -0.998 | 0.989 | 0.011 | -0.577 | -0.157 | -0.577 | -0.157 |
| 16 | -1.000 | 0.998 | 0.002 | -0.667 | -0.297 | -0.667 | -0.297 |
| 20 | -1.000 | 1.000 | 1.57e-04 | -0.482 | -0.025 | -0.482 | -0.025 |
| 30 | -1.000 | 1.000 | 8.33e-07 | -0.096 | 0.383 | -0.096 | 0.383 |
| 50 | -1.000 | 1.000 | 4.28e-11 | -0.436 | 0.033 | -0.436 | 0.033 |
| 100 | -1.000 | 1.000 | 0.000 | -0.543 | -0.108 | -0.543 | -0.108 |
| 200 | -1.000 | 1.000 | 0.000 | -0.501 | -0.051 | -0.501 | -0.051 |

Full-cube check of the hull at 8 sites (256 states): [-0.915149, 0.984970].
<!-- /GEN:f5_hull -->

### 4.13 F6: the ensemble division's frozen controls with l ≡ 0

<!-- GEN:f6 -->
| control | lo (l = 0) | hi | stored | primal programme | |diff| | s |
|---|---|---|---|---|---|---|
| B5-01 | -0.300 | 0.700 | [-3/10, 7/10] | [-0.300000, 0.700000] | 1.11e-16 | 0.005 |
| B5-02 | -0.000 | 0.350 | [0, 7/20] | [0.000000, 0.350000] | 0.000 | 0.005 |
| B5-03 | -0.400 | 0.800 | [-2/5, 4/5] | [-0.400000, 0.800000] | 1.11e-16 | 0.004 |
<!-- /GEN:f6 -->

### 4.14 B3 on F3: superseded (pre-fix) against recomputed values (same draws)

<!-- GEN:b3_rerun -->
H-F(iii) on the F3 cells: median width below 2|I| in 0 of 3 cells with the superseded values, 0 of 3 with the recomputed values (the hypothesis table uses the recomputed values; the F1, F2 cells are unaffected).

| target | env | reps | |I| | med width pre-fix (superseded) | med width recomputed | ratio pre-fix | ratio recomputed | med width change | max end change | fraction recomputed wider |
|---|---|---|---|---|---|---|---|---|---|---|
| stress | 0.2 | 100 | 0.081 | 1.600 | 0.787 | 19.697 | 9.694 | 0.814 | 0.967 | 0.000 |
| stress | 0.55 | 100 | 0.169 | 1.600 | 0.782 | 9.481 | 4.633 | 0.822 | 1.006 | 0.000 |
| stress | 1.15 | 100 | 0.295 | 1.600 | 0.776 | 5.423 | 2.629 | 0.828 | 1.001 | 0.000 |
<!-- /GEN:b3_rerun -->

## 5. What was not run

B1 at n ≥ 10⁴ and on F4; B3 on F3 at n ≥ 10⁴ or Γ > 10 (D2, D3); the sensitivity runs outside the scope of D5;
M1/M2/M4 in the sensitivity runs; the rigorous (interval-arithmetic) option of `certify_upper`.

## 6. Reproduce

```
source "$HOME/.venvs/metricchain/bin/activate"
python experiments/eng/certinf/run_validation.py --workers 4        # grid -> results/validation/*.jsonl (resumable)
python experiments/eng/certinf/run_validation.py --contexts         # exact side -> results/contexts.json
for m in M1 M2 M3 M4 M5 M6 B1 B2 B3; do python experiments/eng/certinf/run_validation.py --memory $m >> experiments/eng/certinf/results/memory.jsonl; done
python experiments/eng/certinf/run_sensitivity.py a                 # and b, c, d
python experiments/eng/certinf/run_structure.py                     # F4, F5, F6 -> results/structure.json
python experiments/eng/certinf/rerun_b3_f3.py                       # B3 on F3 with the changed library (moves the old rows to results/superseded/)
python experiments/eng/certinf/make_tables.py --write               # writes this file with its tables
```

Seeds: every repetition's generator is `SeedSequence([family, target, envelope, n, rep, 20261128])` (grid) or a
fixed key per run (sensitivity); instance seeds are fixed in `instances.py`.

## 7. Compute used

<!-- GEN:compute -->
| run | wall s | worker CPU s (sum of chunk times) |
|---|---|---|
| grid (run_validation.py) | 5908.000 | 2.33e+04 |
| rerun_b3_f3_wall | 203.743 | – |
| sens_a_wall | 610.868 | – |
| sens_b_wall | 44.173 | – |
| sens_c_wall | 787.719 | – |
| sens_d_wall | 61.925 | – |
| structure_wall | 387.322 | – |

Total wall of the recorded runs: 8004 s (2.22 h).  Grid rows: 58680.
<!-- /GEN:compute -->

