## 7. How to re-run (one command per number)

Everything is in `experiments/science/ws_P9/`; run from that directory with
`export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1` and `python3 -B`.  Nothing
is written outside `ws_P9/` (the library `p9lib.py` guards the imports of the other
workstreams' modules; every log ends with the number of foreign writes attempted — 0 in
every run — and with its peak resident memory, printed as `ru_maxrss/1024` and called "MB"
there: mebibytes; where this section says GB it is a thousand of those).  Read-only inputs: P8's cached balls
`ws_P8/cache/ball_*`, P8's stored constants `ws_P8/out/g12b_*.npz`, `bc_*.json`, P8's stored
enumerations (comparison only).  `.npz`/`.npy` files are regenerable and may be ignored by git —
`cache/` is 0.52 GB (redirected caches of P3's evaluator, enumerations, Gibbs samples, the
stored tables `Θ²_T` that the sampler driver reads) and `out/*.npz` 0.64 GB (the tables the
bracket driver reads); `out/*.json`, `logs/*.log`, the scripts, `NOTES.md` and `report_parts/` are
the record (about 1.5 MB).

| what | command | log | time, peak RSS |
|---|---|---|---|
| probe: P8's constants reproduced, first look | `p9_00_probe.py K4` | `logs/probe_K4_H_0.70.log` | 2 s, 0.15 GB |
| consistency of the two-stage resolver with P8's code | `p9_00b_consistency.py K4`; `p9_00b_consistency.py K12 --m 5 --sample 4` | `logs/consistency_K4_H_0.70.log`, `consistency_K12_H_0.70_m5.log` | 2 s; 23 s, 0.46 GB |
| **validation by enumeration** (§2) | `p9_01_validate.py K4`; `… LKSE:5`; `… K5` | `logs/validate_K4_H_0.70.log`, `validate_LKSEc5_H_0.60.log`, `validate_K5_H_0.70.log` | 12 s; 16 s; 229 s, 1.6 GB |
| Gibbs samples (seeds 4242, 777) | `p9_02_gibbs.py K12`; `… LKSE:12`; `… K5` | `logs/gibbs_*.log` | 3–4 min; 2.5 min; 26 s |
| **tables**, both stages (§3) | `p9_03_tables.py K12 4 --keeptabs`; `p9_03_tables.py K12 5 --keeptabs`; `p9_03_tables.py LKSE:12 5 --part 0 2 --keeptabs`, `… --part 1 2 --keeptabs`, `… --merge 2`; `p9_03_tables.py LKSE:12 4 --keeptabs`; `p9_03_tables.py K12 3 --keeptabs`; `p9_03_tables.py LKSE:12 3 --keeptabs`; `p9_03_tables.py K5 4 --w 2`, `K5 4 --w 3`, `K5 5 --w 3` | `logs/tables_*.log` | 87 s; 378 s; 231 s + 249 s (+ 1 s for the merge); 81 s; 29 s; 19 s; 3 s each; at most 1.1 GB |
| gain on the Gibbs samples (§3.2) | `p9_04_gain.py K12 4`; `K12 5`; `LKSE:12 5`; `LKSE:12 4`; `K12 3`; `LKSE:12 3` | `logs/gain_*.log` | 1–2 s |
| **certified brackets** (§4) | `p9_05_brackets.py K12 4 7 --sources ref,s1 --forms S,B,T,W --floor ref:T,s1:T --label A`; `p9_05_brackets.py K12 4 7 --pairs s2:S,s2:B,s2:T,s2:W,sab:W,cJ2:T,cJ2:W --floor s2:T,s2:W,sab:W --label B`; `p9_05_brackets.py K12 5 7 --pairs ref:S,ref:B,ref:T,s1:S,s1:B,s1:T,s1:W --floor ref:T,s1:T --label A` and the same `--label B` line with `K12 5 7`; `p9_05_brackets.py LKSE:12 5 7 --pairs ref:T,s1:T,s1:W,s2:S,s2:B,s2:T,s2:W,sab:W,cJ2:T,cJ2:W --floor ref:T,s2:T,s2:W,sab:W --label A` | `logs/brackets_<tag>_m<m>_w7_A.log`, `…_B.log` | see the list below |
| the extra orders and Ser₁₂ (§5.2, §5.3) | `p9_05_brackets.py LKSE:12 4 7 --pairs s2:W,s2:T,s1:W,cJ2:W --floor s2:W,s2:T --label X`; `p9_05_brackets.py K12 3 7 --pairs s2:W,s2:T,s1:W,cJ2:W --floor s2:W --label X`; `p9_05_brackets.py LKSE:12 3 7 --pairs s2:W,s2:T --floor s2:W --label X`; `p9_02_gibbs.py S12`, `p9_03_tables.py S12 5 --keeptabs`, `p9_05_brackets.py S12 5 7 --pairs ref:T,s2:T,sab:W,s2:W,cJ2:T,s1:T --floor s2:W,s2:T --label X` | `logs/brackets_<tag>_m<m>_w7_X.log` | see the list below |
| brackets on Lys₅ with **every state** checked | `p9_05_brackets.py K5 4 2 --enum --sources ref,sab,cJ2,s1,s2 --forms S,B,T,W`; `… K5 4 3 --enum …`; `… K5 5 3 --enum …` | `logs/brackets_K5_H_0.70_m4_w2.log`, `_m4_w3.log`, `_m5_w3.log` | 6–7 s, 0.25 GB |
| checks at twelve residues (§3.4) | `p9_06_check12.py K12 4`; `K12 3`; `K12 5 --noa`; `LKSE:12 4`; `LKSE:12 3`; `LKSE:12 5 --noa`; `S12 5 --noa`; and at order 5 `p9_06_check12.py K12 5 --noa --nob --shell 20000`, `LKSE:12 5 --noa --nob --shell 20000` | `logs/check12_*.log`, `check12_*_shell.log` | 4–53 s, at most 1.4 GB |
| my chains with constants against the coordinator's forms, as functions (§4) | `p9_08_chaincheck.py K12 4`; `K12 5`; `LKSE:12 5` | `logs/chaincheck_K12_H_0.70_m4.log`, `_m5.log`, `chaincheck_LKSEc12_H_0.60_m5.log` | under 1 s each |
| enumerated brackets for LKSE:5 (§4.4) | `p9_02_gibbs.py LKSE:5`; `p9_03_tables.py LKSE:5 4 --w 2`, `LKSE:5 5 --w 2`; `p9_05_brackets.py LKSE:5 4 2 --enum --sources ref,cJ2,s1,s2 --forms S,B,T,W`, `… LKSE:5 5 2 --enum …` | `logs/brackets_LKSEc5_H_0.60_m4_w2.log`, `_m5_w2.log` | seconds |
| stretch: the nested sampler (§5.4) | {RERUN_NESTED} | `logs/nested_*.log` | see §5.4 |
| the tables of this report | `mk_tables.py`, then `mk_report.py` | — | 1 s |

Times and peak resident memory of the twelve-residue bracket runs (last lines of their logs):
{TIMES_BRACKETS}.

Logs of stopped, failed or superseded runs — none is cited — are in `not_cited/`:
{NOT_CITED}

Files named `logs/*.stdout` are the captured screen output of chained runs (the same lines
as the `.log` files of the scripts they ran); they are not cited.
