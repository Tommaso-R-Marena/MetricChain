# Workstream L — Lean: the exponent functions of the cube satisfy `HintPair`

*Return summary of the workstream (2026-11-25), lightly edited; the deliverable is
`proofs/Frontiers/CubeHintPair.lean` in this repository.  Before integration the coordinator
recompiled the file (empty output, exit code 0), scanned it for forbidden tokens (none), and
read the definitions and the statements of the main theorems against the brief
(`L_brief.md`).*

**Deliverable.**  775 lines, 69 declarations, namespace `MetricChain.HintRecursion`; imports
`Mathlib` and `proofs.Frontiers.HintRecursion`.  No `sorry`/`admit`, no warnings.

**Definitions** (literal transcriptions of the brief): `cubeP u = 1/(1+exp u)`;
`cubeLam u = log(2/(1+exp(-u)))`; `cubeEstar u = klBin (1/2) (cubeP u)`; `cubeA u = klBin (cubeP u) (1/2)`;
`cubeH u = klBin (cubeLam u / u) (1/2)`; `cubeHint u e = klBin ((cubeLam u + e)/u) (1/2)`;
`cubeRadius u x = sSup {ρ | cubeP u ≤ ρ ∧ ρ ≤ 1/2 ∧ klBin ρ (cubeP u) ≤ x}`; `cubeNa u x = klBin (cubeRadius u x) (1/2)`.

**Main theorems.**

* `cubePair (hu : 0 < u) : HintPair (cubeNa u) (cubeHint u) (cubeA u) (cubeH u) (cubeEstar u)` — all nine
  fields; `hint_lower` with `L = 1`.
* `cubeNa_isLeast`: for `x ≥ 0`, `cubeNa u x` is the least element of
  `{klBin ρ (1/2) | cubeP u ≤ ρ ≤ 1/2, klBin ρ (cubeP u) ≤ x}`; `cubeNa_isLeast_allRadii`: also over all
  `ρ ∈ [0, 1]`, which is the definition of `θ_na` in the theory report.
* `cube_superSolution_le_hint`, `cube_iterates_lt_hint_add`: the two theorems of
  `HintRecursion.lean` for the pair of the cube.
* `cubeHint_lt_cubeNa`: `θ_hint(e) < θ_na(e)` for `0 ≤ e < ε*`.

**Supporting lemmas.**  `klBin_half_eq` (`klBin ρ (1/2) = log 2 − Real.binEntropy ρ`);
`klBin_half_strictAntiOn` (on `[0, 1/2]`); `klBin_cubeP_strictMonoOn` (`KL(·‖p_u)` strictly increasing
on `[p_u, 1/2]`, from the derivative `log(ρ/(1−ρ)) + u > 0`); `sSup_sublevel_continuousAt` and
companions (the generalised inverse of a strictly increasing function is continuous);
`cubeEstar_eq` (`ε* = u/2 − Λ₁`), `cubeEstar_eq_log_cosh`, `cubeA_eq` (`a = Λ₁ − u p_u`);
`cubeHintRadius_mem`; `klBin_cubeHintRadius` (the accuracy at the hinted radius is `e + θ_hint(e)`);
`cubeNa_add_cubeHint` (the identity (11.18.1) on the closed interval `[0, ε*]`); `cubeHint_add_mono`;
`cubeHint_pos`; `klBin_cubeRadius`; `cubeNa_of_cubeEstar_le` (`θ_na = 0` from `ε*` on); `cubeNa_zero`,
`cubeNa_antitoneOn`, `cubeNa_le_cubeA`, `cubeNa_nonneg`, `cubeNa_continuousAt`;
`cube_zero_superSolution`.

**Beyond the brief.**

* **A finding.**  `step_from_hint_le` cannot be instantiated with `cubePair`: its hypothesis that
  the hinted exponent is nonincreasing on all of `(0, ∞)` is false for `cubeHint u`, which
  increases again beyond `ε*` (the radius exceeds `1/2`).  Remedy, as for the small-slope pair:
  `cubeHintClip u e = cubeHint u (min e (cubeEstar u))`, `cubePairClip`, and
  `cube_step_from_hint_le : StepLE (cubeNa u) (cubeHintClip u) T' → 0 < g → g < cubeEstar u → T' g ≤ cubeHint u g`.
* `cube_hint_superSolution : StepLE (cubeNa u) (cubeHintClip u) (cubeHintClip u)` — the "`≥`" half of
  Theorem 11.53(b) on the cube, by the convexity argument of the theory report (Mathlib's
  `strictConcave_binEntropy`).  `cube_hintRecursion_witness`: the hypotheses of the two
  corollaries are satisfied by a positive function and the bound is attained.

**Axioms.**  `#print axioms` for `cubePair`, `cubeNa_isLeast`, `cubeNa_isLeast_allRadii`,
`cube_superSolution_le_hint`, `cube_iterates_lt_hint_add`, `cube_step_from_hint_le`,
`cube_hint_superSolution`, `cube_hintRecursion_witness`: `[propext, Classical.choice, Quot.sound]`
(also printed by `proofs/AxiomAudit.lean`).

**Not proved / caveats.**  No field of `HintPair` and no item of the brief is missing.
`cubeNa u x` for `x < 0` is a junk value (no feasible radius); irrelevant to `HintPair`.  The
operator `R[T]` and the sequence `T₁ = θ_na`, `T_{k+1} = min(T_k, R[T_k])` are not defined in Lean
(everything goes through `StepLE`), so the corollaries are for an abstract `T`; the facts
needed about `T₁ = θ_na` (nonincreasing, at most `a`, nonnegative) are proved.  Nothing about
algorithms is formalised.
