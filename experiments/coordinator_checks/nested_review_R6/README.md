# Checks made when SCI-REV-0007 (the nested adaptive algorithm, §§11.18–11.19) was applied

The Scientific Discovery Division reviewed the cost accounting of the nested adaptive
algorithm (theory report Theorems 11.52, 11.54, 11.56, Proposition 11.57, Theorem 11.58 and
the remark on the lowered sample cap): SCI-REV-0007 and its report
`docs/science/workstreams/R6_REPORT.md` on the branch `research/scientific-translation`.  Verdict:
the accounting stands; eight minor points; a finite-`n` separation from non-adaptive
algorithms; a defect of numpy's binomial sampler.  Before its points were written into the
theory report and into `docs/workstreams/K_REPORT.md` (errata (s1)–(s4) there), each was checked
with the code in this directory.  **Nothing here is imported from that division**, and nothing
from `experiments/workstreams/K/` except where a script says that it runs the workstream's own
files.  Python with numpy, scipy and mpmath; every script under seven minutes; outputs are the
files `out_<name>` next to the scripts.

| script | what it checks | output |
|---|---|---|
| `r6lib_coord.py` | shared: exact tables of a cube (ball sizes as integers; `E_r`, `T_m(k)`, `Γ̃`, `κ`, `Γ″` with 60 digits), the constants of Theorem 11.56, the base bracket of Proposition 11.57(a), the lower bounds of Theorems 11.45(b) and 11.25(a); written from the statements | — |
| `t1_cap_corner.py ../../falsify_conjectures.py` | **R6-T1**, the lowered cap, the pass with `M = M‡` exactly.  Part A, exact tables, `31 104` cells: the closing inequality of the main case `r† ≥ Δ` (`101 707` radii, largest ratio `0.99`); the corner `1 ≤ r† < Δ` closes through `E_1 ≥ (n_o+2)E_0` and `e^λ < n_o + 2` (`1890` cells), and fails in `1101` of `8522` cells when `λ > 1` is allowed; for `r† ∈ {0, −1}`, `M† ≥ M‡` always and the pass need not close (`9468` of `17 728` cells).  Part B, `4500` runs of the harness's outer loop (read from the harness file, one logging line added in memory) with `η = ½` on `Q_3 … Q_9`: for `r† ∈ {0, −1}` the pass fails to close in `1283` of `2299` cases and the largest sample is `2M‡` exactly in `1243` runs; for `1 ≤ r† < Δ` it closes in `56` of `56`; no sample above `2M‡`, none at the cap | `out_t1_cap_corner.txt` |
| `t3_separation.py`, `t3_separation.py grid` | **R6-T3**: `ln C_max` (Theorem 11.56 with the base brackets of Proposition 11.57(a), design of `K_REPORT.md` §6.4, `n_o = ⌊n/2⌋`) against the non-adaptive lower bound of Theorem 11.45(b) and the hinted lower bound of Theorem 11.25(a) at the same accuracy `0.8715` and `δ = 0.05`: the five rows of the review and three neighbours, every number of the division reproduced; with `grid`: outer fractions `0.45`, `0.55` and the lowered cap in two readings | `out_t3_separation.txt`, `out_t3_separation_grid.txt` |
| `t3_scan.py <u> <n_from> <n_to>` | every `n` of a window: `C_max < LB` first at `n = 1370` (`u = 1`), `518` (`u = 2`), `4524` (`u = ½`); the sign changes back and forth up to `1397`, `537`, `4565`; from there to the end of the windows (`2100`, `760`, `5050`) the adaptive bound is the smaller one | `out_t3_scan_u1_1300_1700.txt`, `out_t3_scan_u1_1701_2100.txt`, `out_t3_scan_u2_470_760.txt`, `out_t3_scan_u0.5_4350_5050.txt` |
| `t3_large.py` | the larger sizes of the division's table (`n` up to `16 000`): reproduced | `out_t3_large.txt` |
| `t4_rate.py` | **R6-T4**: a rate `O(1/k)` for the level recursion.  The proof is in the head of the script.  Numerical part: the hypotheses of the pair on a grid; a one-sided iteration of the recursion of the cube (an upper bound of every `T_k`), `40` levels, `u = ½, 1, 2`, stays below the proved bounds at every level and every grid accuracy | `out_t4_rate.txt` |
| `t5_numpy_binomial_scan.py` | **R6-T5**: where numpy's `Generator.binomial` is wrong (numpy `2.5.3`): sections A–C, counts from `2^{31}` to `2^{62}` and means from `20` to `10⁹`; D, the counts and probabilities that occurred in the published run of `sim_grouped.py`; E, the cells of referee R8's check behind its erratum m6 (wrong at means `577`, `58`, `52`, right at means below `30`); F, numpy's Poisson sampler (no defect found); G, the lower end of the window of means, sharp at `np = 44` (nothing at `43.9`, wrong at `44.1`) | `out_t5_numpy_binomial_scan.txt` |
| `t5_exact_highstat.py` | the reduction used by the corrected sampler (`binomial_exact` of `experiments/workstreams/K/stable_multinomial.py`): `2·10⁶` draws per cell, three seeds, mean, variance and a chi-square test of the whole law; largest `|z|` of `72` statistics `2.5` | `out_t5_exact_highstat.txt` |
| `t5_poisson_tv.py` | the total-variation distance between a binomial and its Poisson law against the bound `p(1 − e^{-np})` (the alternative remedy; cited from memory, checked on nine cases) | `out_t5_poisson_tv.txt` |
| `t5_trace_old_runs.py first_version ../../workstreams/K` | the published run of `sim_grouped.py` repeated with the first version of the sampler and a recording generator (its output is the published one, line for line): `93 402` binomial draws with a count of at least `10^{14}` in the main suite, none with a count above `10^{15}` and a mean below `10⁸`; in the mutation run "no Harper term" `31` draws with counts `10^{15}`–`10^{16}` and means `3.7·10⁴`–`10⁶`.  Writes `out_t5_saved_runs.pkl` and `out_t5_trace.pkl` (13 MB, not stored) | `out_t5_old_sim_grouped.txt`, `out_t5_trace_summary.txt` |
| `t5_rerun_new.py ../../workstreams/K ../../workstreams/K main` (then `mut`) | every run of that suite repeated from the same generator state with the corrected sampler: `1322` completed (`1325`), the good event in all, no violation, `864` negligible levels in `115` runs (the same), `1013` of `1440` outcomes identical; the four mutations still caught | `out_t5_new_sim_grouped_main.txt`, `out_t5_new_sim_grouped_mut.txt` |
| `h_harper_usage.py ../../falsify_conjectures.py` | the harness remark: how often tests XVI.3, XVI.4 exercise the Harper step, and in how many runs the algorithm without the Harper term violates a claim (`1` of `9` runs of XVI.3 in quick mode) | `out_h_harper_usage.txt` |
| `h_subcase_robust.py ../../falsify_conjectures.py` | the fixed sub-case proposed for XVI.3: the Harper term decides the closure in `3000` of `3000` runs | `out_h_subcase_robust.txt` |
| `h_proposal_test.py ../../falsify_conjectures.py <work dir> ../../mutation_tests.py` | the proposed change of XVI.3 (`HARNESS_PROPOSAL.md`) applied to a copy of the harness: the patched tests pass and report the new statistic; the nine mutations of XVI.3 and XVI.4 are still caught | `out_h_proposal_test.txt`, `out_h_proposal.diff` |

`first_version/` holds the first version of `stable_multinomial.py` and the two outputs it
produced (`out_sim_grouped.txt`, `out_stable_multinomial.txt` — the numbers of `K_REPORT.md` §6.8).
The files of those names in `experiments/workstreams/K/` are now the second version and its
outputs.  `HARNESS_PROPOSAL.md` is a proposal for harness test XVI.3; it has not been applied.

The harness files are only read by the scripts above (their text is executed in memory with
one or two lines added); nothing in `experiments/falsify_conjectures.py` or
`experiments/mutation_tests.py` was changed.

What was **not** re-computed or re-derived: the division's own campaigns (its `4075` literal
runs, the runs with invalid inner answers, the runs with real inner brackets); its Lean files;
the proofs of Theorems 11.52, 11.56 and Proposition 11.57 as wholes — only the places the
review names.  Persistence of the separation beyond the scanned windows is not proved.  The
defect of numpy's sampler was measured, and its cause was read off our memory of the source,
not off the installed source; the one sharp prediction of that reading, a window of means that
begins at `44`, is confirmed by section G of the scan.
