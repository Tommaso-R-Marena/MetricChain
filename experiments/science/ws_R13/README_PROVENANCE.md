# Provenance of the copied files in this directory (coordinator's note, 2026-11-26)

Two files here are **the theory division's**, copied by workstream R13 so that its
re-runs and its compile check can be repeated; they are not ours, not part of any
library of ours, and the theory division's files at their commit `63e36f7` (branch
`claude/determined-ride-og1u7j`) are the authority:

* `thy_copy_nested_R6/code/t4_rate.py` — their
  `experiments/coordinator_checks/nested_review_R6/t4_rate.py`, **byte-identical**
  (`cmp`, by the workstream and again by the coordinator against the read-only export
  at `63e36f7`).  `thy_copy_nested_R6/out/t4_rate.txt` is the output of the workstream's
  re-run of that copy (the script writes next to itself).
* `lean/SoftMinLowerBound_copy.lean` — their `proofs/Frontiers/SoftMinLowerBound.lean`,
  lines 1–249 unchanged, followed by a marked block of seven lines appended by the
  workstream (`#print axioms`, `#check`; `diff` by the coordinator: no other difference).

`r6_copy/everyn.py`, `r6_copy/r6lib.py` are copies of **our own** workstream R6's files
(`../ws_R6/`, identical by `cmp`).

Everything else in this directory is workstream R13's own: the scripts `r13_*`, the
logs in `out/`, and the Lean files `lean/RateCore.lean` (Mathlib only) and
`lean/RateFull.lean` (imports the theory division's `proofs.Frontiers.BoundedAccuracy`,
whose source — like `CubeHintPair.lean` and `HintRecursion.lean` — is byte-identical in
our tree and at `63e36f7`; it is imported, not copied).  The three files
`lean/Rate*_part.lean.txt` are the workstream's drafts of parts of `RateFull.lean`.
`out/sep_scan_u0.5_INCOMPLETE_stopped_not_cited.log` and `out/test_*.json` are not cited
anywhere (the report says so).
