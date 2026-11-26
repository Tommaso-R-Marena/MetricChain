---

## 6. How to re-run

Everything runs from `experiments/science/ws_P8/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1` and
`python3 -B` (`./run_queue.sh LIST` sets them and runs the lines of a list file one after the
other).  The scripts import workstream P3's modules (`p3core`, `encl`, `gfbound`, `termwise`,
`pwmodel`), P5's `p5lib` and, through them, P2's and P's, read-only; `p8lib.py` redirects P3's
enclosure cache to `ws_P8/cache/` (pre-filled with copies of the tables P3, P5 and P6 had built) and
wraps P5's `anch_walk` with a garbage collection (§7).  `p8_12_certificate.py` also imports P6's
`p6lib`, `p6_09_triple` and the coordinator's `pi_inference/window_model.py`, with the copy that
`p6lib` makes into its own cache at import time switched off.  Nothing is written outside
`ws_P8/` and this report.

A log is complete when its last line is `DONE in … s; peak RSS … MB` (runs of before 06:46 UTC:
`DONE in … s`; the probe: `DONE`).  Runs with `--budget` stop at a checkpoint and continue when
the same command is run again (the log is appended; "BUDGET REACHED" lines are not last lines;
`p8_14` wants `--resume` to continue a ball).  The list files `queue_H1.txt` (enumeration passes,
one at a time), `queue_L2.txt`, `queue_X1.txt`, `queue_X2.txt`, `queue_C1.txt`, `queue_C2.txt` are the commands as they were run
after 06:50 UTC (`logs/queue_*.out`: start and end of every command); the Lys₃–Lys₅, LKSE:4,
LKSE:5 measurements and the first twelve-residue runs were made before, with the same commands
(the lists of that time are in `logs/superseded/`).

| what | one command (`python3 -B …`) | log in `logs/` | output in `out/` |
|---|---|---|---|
| sizes of the instances | `p8_00_probe.py > logs/p8_00_probe.log` | `p8_00_probe.log` | — |
| step 1: exact constants per (subset, atom pair), P3's bound per pair, classes | `p8_01_measure.py SEQ BB TAU [--budget s]` | `m1_<tag>.log` | `m1_<tag>.npz`, `.json` |
| exact constants with the hosts outside `T` at the anchor | `p8_01b_restricted.py SEQ BB TAU` | `m1b_<tag>.log` | `m1b_<tag>.npz` |
| sign-blind lower bounds | `p8_02_signblind.py SEQ BB TAU` | `sb_<tag>.log` | `sb_<tag>.json`, `.npz` |
| validation of the pair-wise variants (C0–C6) | `p8_03_sr_validate.py SEQ BB TAU` | `sr_<tag>.log` | `sr_<tag>.json`, `.npz` |
| every pair term at every state (C7) | `p8_03b_statecheck.py SEQ BB TAU` | `sc_<tag>.log` | `sc_<tag>.json` |
| validation of the block-wise variants (B1–B5) | `p8_03c_blockcheck.py SEQ BB TAU` | `bc_<tag>.log` | `bc_<tag>.json`, `.npz` |
| the remainder identity for arbitrary orders | `p8_10_order_identity.py` | `p8_10_order_identity.log` | — |
| twelve residues, all subsets, variants P3 / S / AH / SA | `p8_04_gamma12.py SEQ BB TAU M` | `g12_<tag>_m<M>.log` | `g12_<tag>_m<M>.npz` |
| the same, block-wise variants Sb / SAb | `p8_04b_gamma12_blocks.py SEQ BB TAU M` | `g12b_<tag>_m<M>.log` | `g12b_<tag>_m<M>.npz` |
| 'Sb' against P3's `termwise` at twelve residues | `p8_04c_termwise12.py SEQ BB TAU M NSUB` | `tw12_<tag>_m<M>.log` | `tw12_<tag>_m<M>.json` |
| Gibbs sample of the true ensemble | `p8_05_gibbs.py SEQ BB TAU` | `gibbs_<tag>.log` | `gibbs_<tag>.npz` |
| step 2: group responses and all triples at twelve residues | `p8_06_distance.py SEQ BB TAU` | `dist_<tag>.log` | `dist_<tag>.npz` |
| step 2: fits | `p8_11_distance_fit.py SEQ BB TAU` | `dfit_<tag>.log` | `dfit_<tag>.json` |
| step 4: first-order brackets | `p8_07_estimate.py SEQ BB TAU BAND` | `est_<tag>.log` | `est_<tag>.json` |
| the exact remainder on the Gibbs sample | `p8_08_ideal.py SEQ BB TAU` | `ideal_<tag>.log` | `ideal_<tag>.json` |
| the pipeline with the new constants | `p8_12_certificate.py SEQ BB TAU M W [--variant V] [--enum]` | `cert_<tag>_m<M>_w<W>_<V>.log` | `cert_….json` |
| step 2: exact anchored terms at twelve residues from the ball; "exact term ≤ constant" for every subset | `p8_14_exact_terms12.py SEQ BB TAU M` | `exact_<tag>_M<M>.log` | `exact_<tag>_M<M>.npz`, `.json` |
| tables of this report; the report itself | `p8_09_tables.py`; `mk_report.py` | — | `tables.md` |

`<tag>` is `SEQ_BB_TAU` with `:` replaced by `c` (e.g. `LKSEc6_H_0.60`).  Instances and thresholds:
`K3 K4 K5 H 0.70`, `LKSE:4 LKSE:5 LKSE:6 H 0.60`, `S4 S5 S6 H 0.70`, `L6 L8 H 0.60`, `K3 K4 E 0.70`,
`LKSE:5 E 0.60`; twelve residues `K12 H 0.70` (band 6; the pipeline also with band 7), `LKSE:12 H 0.60` (band 7), `S12 H 0.70` (band 7),
`L12 H 0.60` (band 11).  Library files: `p8lib.py`, `p8sr.py` (the bounds).  Exploration, not cited
for any statement except §3.6 and §7: `x01_ff_proto.py`, `x02_ah_probe.py`, `x03_termwise_compare.py`,
`x04_block_probe.py`, `x05_memdiag.py`, `x05b_memdiag_m1.py`.

**Run times and peak memory** (one core of a machine shared with other jobs; load 5–6 on four
cores during most runs):

<!--T:T11-->

Runs of before 06:46 UTC have no memory record in their logs; four of them were far above the
limit (§7, error 1).  The order-5 ball of Lys₁₂ took two budgeted legs (1 000 s and 884 s);
the logs of the runs that evaluated the Lys₁₂ balls are kept as `logs/ballrun_cert_K12_*.log`,
and `logs/cert_K12_*.log` are the same runs repeated from the cached balls with one more
output line ((3b), §4.1) — identical brackets.

**Not cited, superseded** (kept in `logs/superseded/`, `cache/superseded/`): the first runs of
K3, K4, LKSE:4, LKSE:5 and a killed K5 run with the sign error of §7 (suffix `_signbug`); the first
version of the validation logs (`sr_*` before the variants AH/SA existed); two timing logs; the
killed restricted pass on LKSE:6 (`m1b_LKSEc6_H_0.60_killed_0646_11.7GB.log`) and its checkpoint; the
four stopped queue lists.  `logs/queue_*.out` and `logs/run_m1_*.out` are captures of wrapper
output, not logs of runs.
