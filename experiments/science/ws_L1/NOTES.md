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

## 18:40 environment probe

* `lake env lean` on a file that only imports Mathlib and runs `#check`s: 26 s wall.
* Mathlib at `fabf563a` (2026-06-15, "bump toolchain to v4.31.0").
* **Pinsker**: `grep -rIl -i pinsker .lake/packages/` → no file at all (not in Mathlib, not in any
  dependency).  No total-variation distance (`tvDist`, `totalVariationDist`) either.
  `Mathlib/InformationTheory/KullbackLeibler/{Basic,ChainRule,KLFun}.lean` exist (measure-theoretic
  `klDiv`, non-negativity, chain rule) but no Pinsker, no Donsker–Varadhan (`grep -i "donsker\|varadhan"` → nothing).
* The theory division's proofs have `klFin`, `tilt`, `expTilt`, `klFin_nonneg_of_dominated`,
  `logMGF_eq_tilt` (ThermalRobustness / EnsembleDivergence) but no Pinsker either.
* Lemma names checked: `Finset.sum_sq_le_sum_mul_sum_of_sq_eq_mul` is deprecated →
  `Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul`; `Real.add_pow_le_pow_mul_pow_of_add_eq_one` (named in
  the brief) does not exist under that name; `Real.hasSum_log_one_add_inv` exists (gives
  `log(1+1/a) ≥ 2/(2a+1)`), `hammingDist_eq_hammingNorm : hammingDist x y = hammingNorm (-x + y)`.

## 18:55 Target 1 DONE — `IdentifiedSets.lean` (checks, 38 s, no errors)

All of §8 soundness + Theorem 8(b) inequality + 8(c):
`modelFree_certificate_sound_support` (note's form, arbitrary data set D + support-function bound),
`modelFree_certificate_sound` (box form of the brief), `flow_term_nonpos`,
`envelope_flow_sound_weights` (brief's (b)), `envelope_flow_sound_normalised`,
`envelope_flow_sound_gibbs` (note's form: every admissible g consistent with the data),
`falsification_sound_weights` / `_ensemble` / `_gibbs`, `theorem8c_falsification` (note's form with b, β),
`gibbs_variational` (Donsker–Varadhan on a finite type, μ₀ need not be normalised),
`divergenceBall_certificate_sound` (§8 second bullet), `kl_lower_bound_certificate_sound` (Thm 8(b) inequality),
witnesses `envelope_flow_certificate_witness` (certificate satisfiable AND tight: t = 2/3 attained),
`falsification_certificate_witness` (certificate exists for data some ensemble satisfies).
`#print axioms`: all 14 → `[propext, Classical.choice, Quot.sound]`.

Observations while formalising (for the report):
* (b) needs NO sign condition on μ₀ or κ, only `w ≥ 0`, `Σ μ₀ w > 0`.
* DV inequality does not need μ₀ normalised; needs `μ ≪ μ₀` (with the real-valued KL formula; if
  not `μ ≪ μ₀` the true KL is +∞ and the claim is trivial but the real formula is not the KL).
* Thm 8(c): proved "no member of the class is consistent with the data".  The note's conclusion
  `b_min(D) > b` (strict, about an infimum) additionally needs attainment (D closed) — true by a
  compactness argument but NOT formalised.
* Model-free soundness needs neither convexity nor compactness of D.
