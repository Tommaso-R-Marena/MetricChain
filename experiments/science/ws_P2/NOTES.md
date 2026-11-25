# Workstream P2 — running notes

(Second wave, continues workstream P.  Measurement of class constants of a real residual
— GBn2 polarisation energy against Amber ff14SB — in ROTAMER variables on a FIXED backbone.)

Started 2026-11-25 19:59 UTC.

## Step 0 — orientation (19:59)

* Read `docs/science/workstreams/COMMON.md` and `P2_brief.md` in full.
* Directory `experiments/science/ws_P2/` existed and was empty; this file is the first thing written.
* Hard constraints noted: write only here and `docs/science/workstreams/P2_REPORT.md`; no
  state-changing git; no `lake build`; no subagents; fixed sequences stated in advance; controls first;
  OMP_NUM_THREADS=1 etc.; computations < ~20 min, < ~5 GB; grid data goes into `data/` (git-ignored `*.npz`, `*.npy`).
* Next: read SP_REPORT §1, §2, §2.B, §3.1, §5, §6 and PHYSICAL_APPLICABILITY.md; then P's code.
