# Workstream L1 — notes (machine-checking the science division's core statements)

Chronological log; updated after every step.  All times UTC, 2026-11-25.

## 18:27 start

* Read `COMMON.md`, `L1_brief.md`, `INFERENCE_LIMITS.md` (all), `INFERENCE_LIMITS_ADDENDA.md` (all).
* Environment: Lean 4.31.0 at `~/.lean/lean-4.31.0-linux/bin`; `.lake/packages` has mathlib, batteries,
  aesop, Qq, proofwidgets, plausible, importGraph, LeanSearchClient, Cli.  `lakefile.lean` options:
  `autoImplicit false`, `relaxedAutoImplicit false`.
* Rules I am bound by: write only in `experiments/science/ws_L1/` and `docs/science/workstreams/L1_REPORT.md`;
  no git state change; check files only with `lake env lean <abs path>`, one at a time; no sorry/admit/
  native_decide/axioms; `#print axioms` at the end of each file.

## Plan (targets in priority order from the brief)

1. `IdentifiedSets.lean` — Theorem 8 / §8: (a) model-free certificate, (b) envelope ("flow with gains"),
   (c) falsification, (d) divergence ball via Gibbs variational inequality.
2. `Separation.lean` — Theorem 4′ separation inequality (abstract) + concrete `F ≤ |C|·F1`.
3. `OrthogonalArray.lean` — Lemma 1.
4. `MaxEntStability.lean` — Theorem 7 algebraic core; Pinsker search in Mathlib.
5. optional: Theorem 3 / Theorem 2(d).
