# Workstream L2 — running notes

(Lean 4.31.0 + Mathlib; all files in this directory; one Lean check at a time.)

## 2026-11-25 19:59 UTC — start

* Read `COMMON.md`, `L2_brief.md`, `L1_REPORT.md`.  Created this directory and this file.
* Toolchain present: `~/.lean/lean-4.31.0-linux/bin`; Mathlib cache present under
  `.lake/packages/mathlib`.
* Plan (priority order of the brief):
  1. A11 (stochastic sandwich) — `Sandwich.lean`.
  2. R3 §4: R6.1 (excess identity), R5(2) (two inequalities), R6.2 (sign lemma) — `Referee.lean`.
  3. A1.2 items 1–3 — `Window.lean`.
* Next: read A11 in `INFERENCE_LIMITS_ADDENDA.md`, R3 §4, A1 §9.3, the L1 files, and Mathlib's
  `FourFunctions.lean`.

## 20:10 UTC — sources read; first observations (before any Lean)

Read: A11 (addenda lines 376–478), R3 §4 (R5, R6), A1 §2.5 and §9.3, Mathlib
`Combinatorics/SetFamily/FourFunctions.lean` (whole file), L1's `Separation.lean` head/tail,
`check_log.txt`, L1 `NOTES.md` (first 140 lines).

Environment probe (`lake env lean` on a scratch file, 21 s): `DistribLattice (Fin n → Bool)` and
`Fintype` resolve; `(x ⊔ y) i = (x i || y i)` and `(x ⊓ y) i = (x i && y i)` are `rfl`;
`four_functions_theorem_univ`, `holley`, `fkg` have the expected statements.  Mathlib's `holley`
assumes equal total mass (`∑ f = ∑ g`); for the cross-multiplied form I use
`four_functions_theorem_univ` directly with `f₁ = φ·w₁, f₂ = w₂, f₃ = w₁, f₄ = φ·w₂`.

Paper re-derivations (by hand) and what they show:

* **A11.**  Both Holley conditions re-derived; correct for `β ≥ 0`.  Observations:
  (a) the sandwich needs **no sign condition on `c↑, c↓`**; (b) admissibility of the two fields
  needs exactly `c↑_i + c↓_i ≥ 0` (which is also necessary for the class to be non-empty), not
  `c↑, c↓ ≥ 0` separately; (c) `β ≥ 0` is an implicit hypothesis (for `β < 0` the order reverses:
  two sites, `f = g = 0`, `β = −1`: `E_{f+h↑}φ = 1.354 > 1 = E_{f+g}φ`); (d) the statement for
  monotone `φ` does not need `φ ≥ 0` (the cross-multiplied inequality is invariant under adding a
  constant to `φ`), although the four-functions theorem does.
* **R6.1.**  Correct.  `U′ − U₀ = (D − U₀E)/(Z₀+E)` always; the paper's form with `D/E` needs
  `E ≠ 0` on paper (in Lean it is true also for `E = 0` by `x/0 = 0`, since then `D = 0`).
* **R5(2).**  "max ≥ sum − pairwise minima" needs nonnegativity for three or more terms
  (`(0,0,−1)`: max `0`, sum minus pairwise minima `1`).  The paper says "nonnegative": fine.
* **R6.2.**  Re-derived every line; all inequalities correct.  Implicit hypotheses used:
  `u > 0` (strictness), `r₁ ≥ 1`; `ω_{−1} ≤ ω_{+1}` is used silently at `s = −1` (hypothesis (ii)
  is about `ω_{+1}`); `r₁ < n/2` is not used in R6.2.
* **A1.2.**  Item 2 needs only single-site differences and a weight on "the rest" that does not
  depend on the site letter; `d ≥ 0` and the triangle inequality are not used.

Numerics (`sanity_numerics.py`, 42 s, output in `sanity_numerics_output.txt`): 400 random A11
instances (half with signed constants), 2000 R6.1 pairs, R5(2) on random families and on cubes
`n = 3…8`, R6.2 on 2622 exact instances (hypotheses hold in 465, conclusion never violated;
each hypothesis alone does not suffice for both signs), A1.2 items 2–3 on 300 instances.
No formal statement falsified.

Next: `Sandwich.lean` (A11).
