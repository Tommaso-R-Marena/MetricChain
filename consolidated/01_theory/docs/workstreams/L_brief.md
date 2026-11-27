# Workstream L — Lean: the exponent functions of the cube satisfy `HintPair`

A bounded formalisation task.  Deliver one Lean 4 file that compiles with **no errors, no
warnings, no `sorry`/`admit`**, and whose theorems depend only on the axioms `propext`,
`Classical.choice`, `Quot.sound`.

## Context (repository `/home/user/MetricChain`, read-only for you, commit b12a6c5)

`proofs/Frontiers/HintRecursion.lean` (namespace `MetricChain.HintRecursion`) proves, for an
*abstract* pair of functions `θna θh : ℝ → ℝ` and constants `a h E`, under the hypotheses collected
in the structure

```lean
structure HintPair (θna θh : ℝ → ℝ) (a h E : ℝ) : Prop where
  h_pos : 0 < h
  a_pos : 0 < a
  na_le : ∀ x, 0 < x → θna x ≤ a
  na_cont : ∀ x, 0 < x → ContinuousAt θna x
  na_h : θna h = h
  ident : ∀ e, 0 < e → e < E → θna (e + θh e) = θh e
  hint_pos : ∀ e, 0 < e → e < E → 0 < θh e
  hint_mono : ∀ e e', 0 < e → e ≤ e' → e' < E → e + θh e ≤ e' + θh e'
  hint_lower : ∃ L, ∀ e, 0 < e → e < E → h - L * e ≤ θh e
```

the theorems `superSolution_le_hint` and `iterates_lt_hint_add` (convergence of a recursion to
`θh`).  The file also has `klBin ρ q = ρ log(ρ/q) + (1−ρ) log((1−ρ)/(1−q))` and

```lean
theorem klBin_shift {ρ u : ℝ} (hρ0 : 0 < ρ) (hρ1 : ρ < 1) :
    klBin ρ (1 / (1 + Real.exp u)) = klBin ρ (1 / 2) + u * ρ - Real.log (2 / (1 + Real.exp (-u)))
```

and a witness `gaussPair` for a *different* pair of functions.  **Missing:** a proof that the
functions of the Hamming cube are an instance.  That is your task.

## The mathematics (theory report §11.18, Theorem 11.53; referee report R7 §3.10)

Fix `u > 0`.  `p_u = 1/(1 + e^u)`, `Λ₁ = ln(2/(1 + e^{-u}))`, `ε* = ln cosh(u/2) = klBin (1/2) p_u`,
`a = klBin p_u (1/2)`, `h = klBin (Λ₁/u) (1/2)`.

* `θ_hint(e) = klBin ((Λ₁ + e)/u) (1/2)` (the radius `ρ_h(e) = (Λ₁ + e)/u` lies in `(p_u, 1/2]` for
  `0 ≤ e ≤ ε*`, because `Λ₁ − u p_u = a > 0` and `Λ₁ + ε* = u/2`).
* `θ_na(x) = min { klBin ρ (1/2) : p_u ≤ ρ ≤ 1/2, klBin ρ p_u ≤ x }`.  Since `klBin · p_u` is continuous and
  strictly increasing on `[p_u, 1/2]` (from `0` to `ε*`) and `klBin · (1/2)` is strictly decreasing
  there, the minimiser is the largest feasible `ρ`: the root of `klBin ρ p_u = x` for `x ≤ ε*`, and
  `ρ = 1/2` (value `0`) for `x ≥ ε*`.  A convenient definition:
  `θ_na(x) = klBin (sSup {ρ | p_u ≤ ρ ∧ ρ ≤ 1/2 ∧ klBin ρ p_u ≤ x}) (1/2)` — but you may choose any
  definition for which you also prove the characterisation as that minimum (an `IsLeast`
  statement for `x ≥ 0`).
* The fields: `θ_na ≤ a` (nonincreasing with value `a` at `x = 0`); continuity on `(0, ∞)` (inverse
  of a continuous strictly increasing function; constant `0` from `ε*` on — continuity at `ε*`
  included); `θ_na(h) = h` and more generally `θ_na(e + θ_hint(e)) = θ_hint(e)` for `0 ≤ e < ε*` (by
  `klBin_shift`: `klBin ρ_h(e) p_u = θ_hint(e) + e`, so `ρ_h(e)` is the root); `θ_hint > 0` on `(0, ε*)`;
  `e + θ_hint(e)` nondecreasing (its derivative is `1 + u⁻¹ ln(ρ/(1−ρ)) ≥ 0` iff `ρ ≥ p_u`; or directly:
  `e + θ_hint(e) = klBin ρ_h(e) p_u` and `klBin · p_u` is increasing on `[p_u, 1/2]`); `θ_hint(e) ≥ h − e`
  (so `L = 1` works; equivalently `e + θ_hint(e) ≥ h`, which is the monotonicity just stated,
  from `e = 0`).

## Deliverable

`CubeHintPair.lean` in your directory, importing `Mathlib` and `proofs.Frontiers.HintRecursion`
(open the namespace), containing at least:

1. definitions `cubeP u`, `cubeLam u`, `cubeEstar u`, `cubeA u`, `cubeH u`, `cubeHint u`, `cubeNa u`;
2. `theorem cubePair {u : ℝ} (hu : 0 < u) : HintPair (cubeNa u) (cubeHint u) (cubeA u) (cubeH u) (cubeEstar u)`;
3. the characterisation of `cubeNa u x` as the least element of
   `{klBin ρ (1/2) | p_u ≤ ρ ≤ 1/2, klBin ρ p_u ≤ x}` for `0 ≤ x`;
4. the two corollaries obtained by instantiating `superSolution_le_hint` and
   `iterates_lt_hint_add` with `cubePair`;
5. `#print axioms` lines for the main theorems at the end of the file (as comments is fine
   if you record the output in your report).

Useful Mathlib facts may include: `Real.log` monotonicity and `Real.add_pow_le_pow_mul_pow_of_sq_le_sq`-free
elementary inequalities; `strictMonoOn_of_deriv_pos` / `StrictMonoOn`; `ContinuousOn.surjOn_Icc`,
`StrictMonoOn.orderIso`-type inverses, `intermediate_value_Icc`; `Real.binEntropy` and its
lemmas (the binary entropy function exists in Mathlib; `klBin ρ (1/2) = log 2 − binEntropy ρ`
may shorten things).  If a full proof of continuity through the inverse is too long, an
alternative is to prove that `cubeNa u` is **monotone and has the intermediate value property**
(a monotone function with the intermediate value property on an interval is continuous) —
any correct route is acceptable.

## Rules

* Do not modify anything under `/home/user/MetricChain`; no git commands that change state.
  Work in `scratch:ws/L/`.
* Verification command (about one minute per run; do **not** run `lake build`):
  `cd /home/user/MetricChain && export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH" && lake env lean scratch:ws/L/CubeHintPair.lean`
  Success = exit code 0 and **empty output** (no warnings: e.g. `push_neg` is deprecated in
  this Mathlib — use `rw [not_le]` and the like; unused variables are warnings).
* If one tactic approach fails three times, change the approach rather than repeating it.
* If you cannot finish everything, deliver a file that compiles with what you have proved
  (never with `sorry`), and say exactly which fields of `HintPair` are done and which are not.
* Do not delegate to further agents.

## Required return

A summary of at most 25 lines: whether the file compiles cleanly (paste the command's
output and exit code); the list of proved declarations with their statements; the output of
`#print axioms` for the main theorems; anything you could not prove and why.
