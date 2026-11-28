# Phase II verification gaps: the twelve later structural-biology certificates, the F1 repair, the memoised kernel

*Report of a subagent of the Computational Research Division, 2026-11-28; local computation only.  The
subagent could not write this file itself (its harness returns reports as text); the coordinator saved its
text here, shortened only by removing repetitions.  What the coordinator re-ran himself is stated in
`docs/engineering/phase2/VERIFICATION_GAPS.md`.  `<sb-worktree>` is a read-only worktree of the
structural-biology (SB) branch.*

**Commits:** SB `41fa668` (the last one engineering had reviewed) and `a5cc106` (its final head, which
contains the repair `0e934eb`); this checkout at `67b6bc2`, unchanged.  **Environments:** SB's own virtual
environment (Python 3.12.16, numpy 2.5.5, OpenMM 8.6.1) for everything that imports OpenMM; engineering's
(python-flint) for the Arb reproducers; no bytecode cache written; SB is installed in neither — every
import of its code comes from `<sb-worktree>/src`.

## SB code executed, and what changed after `41fa668`

* Changed under `src/`: expo, gmec, itables, mincert, mincheck, model, partition, stability, zcert, zcheck.
  **Unchanged:** `molecular/` (byte-identical at `41fa668`, `87082ef` and `a5cc106`) and `run.py`.
* `model.py` (full diff read): stricter integer-only constructor, no cached neighbour list, `integer_tables`,
  `MAX_SCALE_BITS = 1024`; `from_float` unchanged.
* `mincheck.py` (full diff read): works on a normalised certificate and a snapshot of the tables;
  `message_bits ≤ 49`; new `check_text(..., expected_model_sha256)`.  The leaf and prune inequalities are
  unchanged.
* `mincert`, `zcert`, `partition`, `stability`, `gmec`: diffs scanned for I/O, subprocess, network, eval and
  pickle; none found.
* `zcheck`, `expo`, `itables` (full diffs read).  The repair has two parts: `_ldexp_up` and `_ldexp_down` now
  decide on the value; `exp_bits` is range-checked, 16–512 in the float tier and 16–1024 in the exact tier.
  Also new: `β·|entry| ≤ 2^16`; prune steps with `β·margin < −9` are refused and `β·margin > 2^13` is capped;
  `exp_bounds_me` picks its number of Taylor terms from `bits`.

## T1 — the twelve later certificates

Tables: SB stores none.  `export_tables_v2.py` (a copy of engineering's `export_tables.py` with the
`MODELS["v2"]` / `MODELS["v2-lib"]` parameters of SB's `run.py`) runs SB's builder from `<sb-worktree>` at
`a5cc106`.  These are regenerated tables, not stored files; their canonical SHA-256, computed by
engineering's code, equals the certificate's `model_sha256` and SB's result row in all 12.  The tables
therefore do not come from the certificates; the physics behind them (SB's claim K5) is still SB's code.

Checkers: engineering's `check_files.py` (unchanged); engineering's `indep_mincheck.check_plain`
(unchanged) through an adapter in `t1_check.py`, because `indep_mincheck.strict_loads` cannot read detached
files (it needs an embedded `model` and nested `prune` nodes; the files have flat `prunes` chains) — so the
two engineering checkers share one parser; SB's repaired `mincheck.check_text` at `a5cc106`.

    bash experiments/eng/phase2_gaps/run_t1.sh <sb python> <sb-worktree> <scratch>      # 12 certificates x 3 checkers, 20-minute limit each
    python experiments/eng/phase2_gaps/t1_controls.py ; python experiments/eng/phase2_gaps/t1_summary.py --results <sb-worktree>/experiments/structbio/gmec_dev/results.jsonl

| model | id | sites / states / pairs | bytes | leaves / branches / eliminations | claimed minimum, kcal/mol | check_files / indep / SB | proves = claim; gap | seconds (files / indep / SB) |
|---|---|---|---|---|---|---|---|---|
| v2 | 1CRN | 26 / 380 / 325 | 37,015 | 1 / 0 / 349 | −42.493639 | accepted ×3, full box | yes; 0 | 0.03 / 0.06 / 0.08 |
| v2 | 5PTI | 36 / 1152 / 630 | 131,859 | 1 / 0 / 1074 | −121.344662 | accepted ×3 | yes; 0 | 0.12 / 0.49 / 0.41 |
| v2 | 1BPI | 36 / 1152 / 630 | 127,042 | 1 / 0 / 1089 | −123.735561 | accepted ×3 | yes; 0 | 0.14 / 0.48 / 0.41 |
| v2 | 1PGA | 46 / 967 / 1035 | 200,381 | 1 / 0 / 775 | 4.513694 | accepted ×3 | yes; 0 | 0.13 / 0.36 / 0.37 |
| v2 | 2IGD | 49 / 1027 / 1176 | 2,119,287 | 13 / 1 / 1383 | −21.798523 | accepted ×3 | yes; 0 | 0.72 / 0.77 / 1.05 |
| v2 | 1UBQ | 65 / 1763 / 2080 | 15,901,276 | 30 / 4 / 2428 | −76.093704 | accepted ×3 | yes; 0 | 2.85 / 4.15 / 4.14 |
| v2-lib | 1CRN | 26 / 354 / 325 | 35,392 | 1 / 0 / 323 | 12.097671 | accepted ×3 | yes; 0 | 0.03 / 0.05 / 0.05 |
| v2-lib | 5PTI | 36 / 1116 / 630 | 127,491 | 1 / 0 / 1047 | 118.874406 | accepted ×3 | yes; 0 | 0.12 / 0.54 / 0.36 |
| v2-lib | 1BPI | 36 / 1116 / 630 | 133,237 | 1 / 0 / 1030 | 397.944123 | accepted ×3 | yes; 0 | 0.14 / 0.47 / 0.39 |
| v2-lib | 1PGA | 46 / 921 / 1035 | 191,412 | 1 / 0 / 746 | 855.192956 | accepted ×3 | yes; 0 | 0.13 / 0.32 / 0.29 |
| v2-lib | 2IGD | 49 / 978 / 1176 | 208,325 | 1 / 0 / 804 | 198.220426 | accepted ×3 | yes; 0 | 0.15 / 0.35 / 0.31 |
| v2-lib | 1UBQ | 65 / 1698 / 2080 | 10,035,244 | 19 / 2 / 1382 | −1.776812 | accepted ×3 | yes; 0 | 1.90 / 2.33 / 2.33 |

In all 12: the tree proves exactly the claimed bound, the witness gap is 0, the box is full; checksum,
bound, file SHA and node counts equal SB's rows; the bound equals the optimum of engineering's own
toulbar2 call.  Negative controls (claim + 1; one table entry altered): refused by all three checkers.
Generated table: `results/t1_table.md`.

## T2 — the old floating-point exploit (finding F1 of `experiments/eng/sb_zcheck/REPORT.md`) and the repair

    python experiments/eng/sb_zcheck/f1_direct.py <sb-worktree>            -> results/t2_f1_direct_{41fa668,a5cc106}.txt
    python experiments/eng/phase2_gaps/t2_probe.py <sb-worktree>            -> results/t2_probe_*.jsonl   (truth to 60 digits; containment decided exactly)
    python experiments/eng/phase2_gaps/t2_findings.py <sb-worktree> <out>   # findings_repro.py unchanged, pointed at the worktree

* (a) At `41fa668` F1 reproduces exactly: the float tier at `exp_bits` 990 and 991 accepts
  `[−677.0000000006, −676.9999958362]` against `ln Z = −676.6867383125`.
* (b) At `a5cc106` the exploit is refused ("exp_bits = 990 is outside the range of the float tier (16 to
  512)"), and the faulty conversion itself (`_ldexp_up`) is corrected.
* (c) Probe, 104 calls: float tier at 16, 17, 64, 256, 511, 512 and exact tier at 16, 64, 990, 1023, 1024
  accept and contain the truth; 15, 513 and 1025 are refused.  Energies `E, E+1` and `E, E+40` for `E` from
  600 to 760: no unsound acceptance; the float tier abstains for `E ≥ 690` at both commits.  Called directly
  on mantissas of about 1000 bits, the old conversion gives a wrong upper bound in 3 of 5 cases, the new one
  in none.  **No acceptance that misses the exact value; no new finding.**
* (d) The other findings of that report:

| finding | at `41fa668` | at `a5cc106` | status |
|---|---|---|---|
| F1 | unsound at 990, 991 | refused | fixed |
| F2 | 1,096 of 1,924 contain | 1,085 of 1,905 contain; all contain the truth | persists (claim Z3 as worded is still false) |
| F3 | −10 kT: upper 22,016 | −2 / −5 kT as loose (sound); −9 kT accepted (upper 8,094); −9.5 to −20,000 kT refused in under 1 ms | memory exhaustion fixed by refusal; looseness persists |
| F4 | 7 of 35 files raise | 0 of 35 | fixed |
| F5 | 8 lax loader cases | 5 lax: −0, one-sided claim, missing keep, missing meta, unsorted domain | partly fixed |
| F6 | rejection by IndexError | same | persists (sound) |
| F7 | 181 of 280 | 0 of 280 | fixed |
| F8 | width `2^−29.7` at `2^64`; the `2^200` case timed out at 100 s (cause not investigated) | below `2^−69` up to `2^200`, sound by Arb | fixed |
| F9 | 1 case | 1 case | persists |

New, a loss of completeness by design: 15 certificates that engineering's checker accepts are now refused
by SB's.  Engineering's test `tests/eng/test_sb_zcheck.py::test_finding_f3…` fails when pointed at
`a5cc106`, because it asserts that SB accepts the −10 kT case (an intended change in SB); at `a5cc106`:
11 passed, 1 expected failure (F2), 1 failed (F3); at `41fa668`: 10 passed, 3 expected failures.  The test
was not edited.

## T3 — the memoised kernel `verifyM`

`experiments/eng/sb_review/lean_kernel/RunKernel.lean` (ENG-RES-0019 §3): `export_for_kernel.py` writes a
token file from engineering's parser and the tables; the Lean file evaluates `verifyM`, proved equal to the
theory division's verified `verify` by `verifyM_eq`; `collect.py` compares digests with the Python side.
Here: `t3_run_kernel.py` runs `lake env lean --run …/RunKernel.lean full TOKENS…` with four threads, no
address-space limit, one Lean process at a time, a 20-minute watchdog per file.

The Lean file still elaborates, `verifyM_eq` included; loading took 1 to 1.5 minutes.

| certificate | leaves / branches / eliminations | `verifyM` | bound + 1 | witness = bound; digests | checking, ms | wall, s |
|---|---|---|---|---|---|---|
| v2 1CRN | 1 / 0 / 349 | accepted | refused | yes; yes | 1,583 | first block at 94.5 (with loading) |
| v2 5PTI | 1 / 0 / 1074 | accepted | refused | yes; yes | 9,156 | 36.5 |
| v2 1BPI | 1 / 0 / 1089 | accepted | refused | yes; yes | 9,261 | 37.1 |
| v2 1PGA | 1 / 0 / 775 | accepted | refused | yes; yes | 8,520 | 41.4 |
| v2 2IGD | 13 / 1 / 1383 | accepted | refused | yes; yes | 22,396 | 66.7 |
| v2 1UBQ | 30 / 4 / 2428 | accepted | refused | yes; yes | 195,712 | 409.7 (with loading) |
| v2-lib 1CRN | 1 / 0 / 323 | accepted | refused | yes; yes | 1,403 | first block at 61.5 |
| v2-lib 5PTI | 1 / 0 / 1047 | accepted | refused | yes; yes | 8,661 | 34.7 |
| v2-lib 1BPI | 1 / 0 / 1030 | accepted | refused | yes; yes | 8,731 | 35.4 |
| v2-lib 1PGA | 1 / 0 / 746 | accepted | refused | yes; yes | 7,842 | 39.4 |
| v2-lib 2IGD | 1 / 0 / 804 | accepted | refused | yes; yes | 8,893 | 44.2 |
| v2-lib 1UBQ | 19 / 2 / 1382 | accepted | refused | yes; yes | 121,184 | 283.6 (with loading) |

Controls on 1CRN v2 (bound + 1; prune order reversed; a witness entry lowered): all refused.  Memory for
1UBQ v2: peak 4,948 MB.  Generated table: `results/kernel_table.md`.

"Executed by the kernel" means: `verifyM`, proved equal to the verified `verify`, was evaluated by Lean's
runtime (`lean --run`).  It is not a proof term.  Trusted: the Lean kernel (for `verify_sound` and
`verifyM_eq`); faithful execution by Lean's runtime; engineering's reader and translator (checked through
the digests and the kernel's own witness energy); the identity of the tables with SB's (SHA-256).  It says
nothing about K5 or about the rounding of real energies to integers.

## Not verified

K5 (the physics behind the tables); the repair commit beyond what the reproducers touch (`stability.py`,
`partition.py`, the normalisation under adversarial use); the F1 window on other instances; the campaign
z12 on 300 of 1,500 instances only (seed 102 not re-run); the fuzz campaign for claim Z5 and the
rounding-mode experiment (still never run).

## Files

Scripts: `export_tables_v2.py`, `t1_check.py`, `run_t1.sh`, `t1_controls.py`, `t1_summary.py`,
`t2_probe.py`, `t2_findings.py`, `t2_f8.py`, `t2_f3_large.py`, `t3_run_kernel.py`, `t3_collect.py`,
`t3_table.py`; outputs in `results/`.  The exported tables and token files (up to 41 MB) are not in the
repository; `export_tables_v2.py` and `export_for_kernel.py` regenerate them.
