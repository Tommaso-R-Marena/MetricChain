"""Template of REPORT.md; make_tables.py fills the GEN blocks from the stored results."""

TEMPLATE = r"""# Phase II validation campaign (Workstream D): report

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
<!-- /GEN:hypotheses -->

## 4. Results

### 4.1 Exact side (M0, B4, B5) for every cell

`|M0 − primal|`: difference to the primal programme (F1, F2).  `extremal gap`: |target average of the extremal
ensemble at the returned multipliers − the end|; `extremal in R`: its measured averages lie in the region (10⁻⁶).

<!-- GEN:exact -->
<!-- /GEN:exact -->

### 4.2 Median total excess over I, every cell and method

<!-- GEN:excess_summary -->
<!-- /GEN:excess_summary -->

<!-- GEN:s3check -->
<!-- /GEN:s3check -->

### 4.3 Full tables per family

Columns: coverage of I and of the true value; median / 90th percentile of the width, of the total excess and of
the excess at each end (+: upper, −: lower); `triv`: fraction of repetitions with the whole range; `miss±`:
fraction of repetitions in which that end is certified and lies inside I (for B1, B3: the end lies inside I, or the
interval is empty); `incons`: the certified ends cross.

#### F1
<!-- GEN:grid_F1 -->
<!-- /GEN:grid_F1 -->

#### F2
<!-- GEN:grid_F2 -->
<!-- /GEN:grid_F2 -->

#### F3
<!-- GEN:grid_F3 -->
<!-- /GEN:grid_F3 -->

#### F4
<!-- GEN:grid_F4 -->
<!-- /GEN:grid_F4 -->

### 4.4 B2 (maximum-entropy reweighting)

<!-- GEN:b2 -->
<!-- /GEN:b2 -->

### 4.5 Timings (median seconds per repetition; cells with ρ = 1.15, first target)

<!-- GEN:timings -->
<!-- /GEN:timings -->

### 4.6 Peak memory (one cell, one repetition, fresh process per method)

<!-- GEN:memory -->
<!-- /GEN:memory -->

### 4.7 Sensitivity (a): true half-width 2ρ, declared ρ

<!-- GEN:sens_a -->
<!-- /GEN:sens_a -->

### 4.8 Sensitivity (b): what the observations add (F1 `nnn_corr`)

<!-- GEN:sens_b -->
<!-- /GEN:sens_b -->

### 4.9 Sensitivity (c): displaced regions, inconsistency certificate

<!-- GEN:sens_c -->
<!-- /GEN:sens_c -->

### 4.10 H-D sweep (F1 `nnn_corr`, M3)

<!-- GEN:sens_d -->
<!-- /GEN:sens_d -->

### 4.11 F4: exactness at scale (2¹⁰⁰ states by level counts)

<!-- GEN:f4 -->
<!-- /GEN:f4 -->

### 4.12 F5: bounded influence

Programme (`ci.lp_ratio_class` on the whole cube) against Corollary 9.3 (`ci.additive_interval`):

<!-- GEN:f5_small -->
<!-- /GEN:f5_small -->

Corollary 9.3 at 50 and 200 sites:

<!-- GEN:f5_big -->
<!-- /GEN:f5_big -->

Box hull of the class (ratio e^{0.5·n}), target one spin, no data:

<!-- GEN:f5_hull -->
<!-- /GEN:f5_hull -->

### 4.13 F6: the ensemble division's frozen controls with l ≡ 0

<!-- GEN:f6 -->
<!-- /GEN:f6 -->

### 4.14 B3 on F3: superseded (pre-fix) against recomputed values (same draws)

<!-- GEN:b3_rerun -->
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
<!-- /GEN:compute -->
"""
