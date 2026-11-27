# Workstream L2 — machine-checking the science division's newest statements (Lean 4, Mathlib)

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_L2/`; your report: `docs/science/workstreams/L2_REPORT.md`.
(Second wave.  You continue workstream L1: read `docs/science/workstreams/L1_REPORT.md` and
look at its files in `experiments/science/ws_L1/` for conventions and for lemmas you can
import — `import` them by copying what you need into your own files or by referring to
the theory division's library as L1 did; do not modify `ws_L1/` or `proofs/`.  Each of your
files must check alone with
`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path>`,
exit 0, no `sorry`, no `admit`, no `native_decide`, no new axiom; end every file with
`#print axioms` for each theorem.  Never run `lake build`.)

Formalise, in this order of priority; stop where time runs out and say where you stopped.

## 1. The stochastic sandwich for robust macrostate ratios (addendum A11)

Statement and paper proof: `docs/science/INFERENCE_LIMITS_ADDENDA.md`, section A11 (Theorem
A11, Corollary A11.1).  Mathlib has what is needed:
`Mathlib/Combinatorics/SetFamily/FourFunctions.lean` — `four_functions_theorem_univ`,
`holley`, `fkg` (on a finite distributive lattice).  Target statements, for the cube
`Fin n → Bool` (or `Finset (Fin n)`, whichever makes the lattice structure easiest), real
energies `f g : (Fin n → Bool) → ℝ`, constants `cup cdn : Fin n → ℝ` (nonnegative),
`d x y = Σ_i (if x i && !y i then cup i else 0) + Σ_i (if !x i && y i then cdn i else 0)`,
admissibility `∀ x y, g x − g y ≤ d x y`, submodularity
`∀ x y, f (x ⊔ y) + f (x ⊓ y) ≤ f x + f y`, fields `hup x = Σ_i if x i then cup i else 0`:

* **Holley condition:** `exp(−(f x + hup x)) * exp(−(f y + g y)) ≤ exp(−(f (x ⊓ y) + hup (x ⊓ y))) * exp(−(f (x ⊔ y) + g (x ⊔ y)))`,
  and the mirror statement with `cdn`.
* **Sandwich, cross-multiplied (no division):** for every monotone `φ ≥ 0`,
  `(Σ_x φ x * w₁ x) * (Σ_x w₂ x) ≤ (Σ_x w₁ x) * (Σ_x φ x * w₂ x)` with
  `w₁ = exp(−(f + hup))`, `w₂ = exp(−(f + g))`; and the mirror statement with
  `w₂ = exp(−(f − hdn))` on the other side.
* **Macrostates:** for an up-set `B` (a `Finset` or a decidable predicate closed
  upwards), the ratio statement in cross-multiplied form:
  `Z_{f+g}(A) * Z_{f+hup}(B) ≤ Z_{f+hup}(A) * Z_{f+g}(B)` and the mirror one.
* The two fields are admissible (`hup` and `−hdn`).
* A small kernel-evaluated or `norm_num` instance showing the hypotheses are jointly
  satisfiable with a strict conclusion, if cheap.

## 2. Three finite statements of our referee (R3 report, §4: R6.1, R6.2, R5(2))

`docs/science/workstreams/R3_REPORT.md` §4.  (a) **R6.1, the excess identity** — pure
algebra on finite sums: with `g′ = min(g₀, T)`, `Z′ = Z₀ + E` and
`U′ − U₀ = (E/(Z₀+E))·(D/E − U₀)` for the stated `E`, `D`.  State it for an arbitrary finite
type and two real functions; no cube needed.  (b) **R5(2)**: for finitely many "centres"
with weights, the two inequalities used there — a maximum of nonnegative terms is at
least their sum minus the sum of pairwise minima; and `Z(flat^C) ≤ |C|·Z(flat)`.  Abstract
form on a finite type suffices.  (c) **R6.2, the sign lemma** — only if (a), (b) and
section 1 are done: its two hypotheses and the two signs, in an abstract form that
isolates the inequalities used (you decide the right abstraction; say what it covers).

## 3. Proposition A1.2, items 1–3 (workstream A1's report, §9.3)

`docs/science/workstreams/A1_REPORT.md` §9.3.  For one site: the "window"
`{p : π a * p b ≤ exp(d a b) * π b * p a}` contains every conditional law of every member
of the class (item 2: summing the admissibility inequality over the remaining
coordinates) — state it for a product of two finite types `α × β` with `α` the site and
`β` "the rest", a positive product weight and a function `ψ` on `α × β` with
`ψ (a, r) − ψ (b, r) ≤ d a b`.  Then the chain-rule bound of item 3 in whatever generality
Mathlib's present tools allow without building entropy theory from scratch (L1 found
that relative entropy and its chain rule are thin in Mathlib; if item 3 needs more than
a day's worth of infrastructure, stop at item 2 and say so).

## What to report

For every statement: the Lean name, the exact statement in words, what it covers and
what it does not (which part of the paper statement remains on paper), and every place
where the paper statement had to be changed to be true or formalisable — **discrepancies
are the most valuable output** (L1 found two that mattered).  A table "paper statement →
Lean declaration → status".  Final message: at most 500 words.
