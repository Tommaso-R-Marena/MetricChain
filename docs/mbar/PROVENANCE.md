# Division 9 — provenance of the branch `research/phase2-certified-mbar`

*Division 9: Certified Statistical Thermodynamics and Optimal Molecular Simulation (identifier prefix
`MBAR-`).  Opened 2026-11-28 05:23 UTC under the research owner's directive "MetricChain Phase II —
Division 9".*

## 1. Base of the branch

| item | value |
|---|---|
| branch | `research/phase2-certified-mbar` |
| base commit | `b3c5d6115df06bb160d6490a95d9ec6e1a108d02` — head of the Theoretical Research Division (`claude/determined-ride-og1u7j`), the commit the consolidated archive pins as division 01 |
| why this tree | it is the common ancestor tree of every division; it holds the common collaboration protocol (`docs/collaboration/README.md`), the programme's Lean pins (`lean-toolchain`: `leanprover/lean4:v4.31.0`; `lake-manifest.json`: Mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, tag `v4.31.0`) and the audit scripts.  `research/phase2-foundations` and `research/phase2-adaptive-hierarchy` are based on the same commit |
| immutable reference | consolidated archive `fe9f58c1f0bfe5de8c6434c3490a33cd1d94023f` (`research/consolidated-archive`), read-only; entry point `consolidated/00_MASTER_INDEX.md` |
| other branches read (never written) | `research/phase2-foundations` at `d3b13a291ab350874b8c1797069f21f157e46ab8`; `research/phase2-adaptive-hierarchy` at `c66a4019a0ee0301034b90f8917bfdf9522bacb1`; `research/phase2-certified-inference` at `1bb0dcc6c7e272b6bd34720b0ad48360d821ca33` (heads at 2026-11-28 05:23 UTC) |
| the same branches, second read (messages addressed to this division only) | `research/phase2-foundations` at `3daa07d4ad2c82374cb925fa0a953084411bcd2e`; `research/phase2-adaptive-hierarchy` at `3e3e7d9d77dfe867bb23111af2f5a123dfd41e8f`; `research/phase2-certified-inference` at `2d0255f0117b4a9f3fa1b8d9bc7511c387306504` (heads at 2026-11-28 08:53 UTC) |

Nothing outside the paths of §3 is modified on this branch (checked: `git diff --stat b3c5d61 HEAD` lists
only those paths).  No merge into any established branch, no
force push, no pull request.

## 2. The imported MBAR package (preserved byte for byte)

| item | value |
|---|---|
| uploaded archive | `experiments/mbar/handoff/MBAR_MetricChain_Strengthened_v2.zip`, 512 669 bytes, SHA-256 `b4c4710d74e4746615b3eacd9fcd73f3fd175778e76aadad15b07513060dc3c7` |
| extracted copy | `experiments/mbar/handoff/MBAR_strengthened/` — all 16 files verify against the package's own `MANIFEST.sha256` |
| nested original handoff | `experiments/mbar/handoff/MBAR_strengthened/original_handoff.zip`, SHA-256 `e3dcbd4a3bafec6e0a013caefc773817acd4f9a8a42f32ce111bf7fa9281fbf3` — kept zipped, unchanged (the recovered manuscript, transcript, audit, code and uncompiled Lean file of the earlier programme).  **Historical; not authoritative; not to be submitted.** |

The files under `experiments/mbar/handoff/` are never edited.  Everything this division derives,
corrects or adds lives elsewhere (§3) and refers to the package by path.

## 3. Paths owned by this division

```
docs/mbar/                          reports, proofs, audit, prior art, negative results, log
docs/collaboration/messages/mbar/   MBAR-MSG-nnnn.md
docs/collaboration/requests/mbar/   MBAR-REQ-nnnn.md
docs/collaboration/responses/mbar/  MBAR-RES-nnnn.md
docs/collaboration/status/mbar.md
docs/collaboration/MBAR_TO_ALL.md   digest for the other divisions
experiments/mbar/                   handoff (read-only), src, tests, bench, results, data, review
experiments/mbar/lean/              Lean 4 sources: a standalone Lake project with the programme's pins
```

The Lean sources are deliberately **not** under `proofs/`: the theory division's audit
(`scripts/audit_all.sh`) requires every module under `proofs/` to be registered in its own
`proofs/AxiomAudit.lean`, and this division does not edit files of another division.  The standalone
project copies `lean-toolchain` and `lake-manifest.json` from the repository root, so the pins are
identical (`docs/mbar/LEAN_CORRESPONDENCE.md`).

## 4. Epistemic labels

The labels of the common protocol: **[V]** machine-checked in Lean 4 (declaration named; only
`propext`, `Classical.choice`, `Quot.sound`), **[P]** paper proof (refereed internally or not, stated),
**[K]** known and cited, **[N]** numerical evidence, **[C]** conjecture; and one more used here,
**[X]** external lemma assumed with its exact statement (a concentration inequality, a central limit
theorem) — never presented as machine-checked.
