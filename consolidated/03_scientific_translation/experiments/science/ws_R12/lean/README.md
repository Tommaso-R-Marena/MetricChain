# Provenance of the two Lean files in this directory (coordinator's note, 2026-11-26)

* `BoxClass_copy_9408e33.lean` — **the theory division's** `proofs/Frontiers/BoxClass.lean` at
  their commit `9408e33` (branch `claude/determined-ride-og1u7j`), copied unchanged (lines
  1–513; checked with `diff` by the workstream and again by the coordinator), followed by a
  marked block of twelve `#print axioms` commands appended by workstream R12.  It is here
  only so that the compile check of `r12_08_lean_boxclass.sh` can be repeated; it is not
  ours, not part of any library of ours, and their file is the authority.
* `R12Additions.lean` — workstream R12's own file (namespace `ScienceR12`, imports Mathlib
  only).  Because `BoxClass.lean` and `BoxRatio.lean` at `9408e33` are not modules of our
  tree, it **copies from the theory division** the definitions `Box`, `Zw`, `dip`, `bump`,
  `bumpAlt`, `restr`, `logRatio` and five of their lemmas with their proofs (`dip_nonneg`,
  `bump_nonneg`, `Zw_pos`, `Zw_sub_le_dip`, `Zw_sub_le_bump`), and proves on them seven
  statements of the workstream: `detect_ge_at_floor`, `detect_ge_at_ceiling`,
  `detect_ge_weighted`, `weighted_opt`, `logRatio_bumpAlt_lt`, `logRatio_bumpAlt_gt`,
  `affine_half_large`.  Compiled by the coordinator with `lake env lean` (exit 0, 9 s;
  the seven depend on `propext`, `Classical.choice`, `Quot.sound` only); sha256
  `ef6481c4eed0390879773dd595eb8006a5b421afe182eb6faee04eb8a8afc495`.
