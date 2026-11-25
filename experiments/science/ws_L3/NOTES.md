# Workstream L3 — notes (kept from the first minute)

Lean 4.31.0 + pinned Mathlib (v4.31.0, rev fabf563a).  Compile command (single files only):

    export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path>

## Log

* 23:33 UTC (2026-11-25) — started.  Read COMMON.md and L3_brief.md.  Created `experiments/science/ws_L3/`.
  `.lake/packages` present (mathlib, batteries, aesop, …).  Repository state: branch
  `research/scientific-translation`, head 25626db (checkpoint 33).  Nothing of mine exists yet.
* Next: read SF_REPORT.md §2.0–§2.2, the L1/L2 Lean files and reports, then plan the files.
* 23:36–23:50 — read SF_REPORT §2.0–2.2 (Lemmas 0–3, Theorem A), L1 `MarginalOracle.lean` (oracle-indexed model:
  `alg ω o : MetricChain.QueryAlgorithm`, run with `o = oracle g`; Theorem 4 derived from the theory division's
  `MetricChain.expected_queries_ge_packing` applied to the class restricted to a common oracle answer), L2 `Window.lean`
  (`condLaw_mem_window`), L2 report §2.7 (format of the discrepancy list).
  Facts: files in `experiments/science/` cannot import each other (not in the lake globs; L1/L2 repeat proofs);
  `proofs.Frontiers.QueryLowerBound` has an `.olean` and can be imported.  `import Mathlib` alone compiles in ~7 s here.
* Re-derived by hand (independent review) Lemma 2, Lemma 3 and the proof of Theorem A; no error found so far.
  Details checked: `c₀(m) = p₋ + mω`, distance `≥ ω·min(m,1−m)` from both window ends; `b ≤ (ω−κ)/κ = β − 1 ≤ β`;
  `A(w₀) = 1 + b`, `A(w₁) = 1 + b + E`; Lemma 2 gives the *closed* interval `[p₋+κ, p₊−κ]` (the report says open;
  immaterial).

## Design decisions

1. **Unification**: an additive instance with site-dependent fields `γ : ι → ℝ` has weight
   `tiltW p γ x = ∏_i (if x i then e^{−γ i} else 1)/(q + p e^{−γ i})`, and `π·tiltW = ⊗_i π_{γ i}`.  The constant field is
   `w̃_γ`; the field `γ_i = u(1 − 2 s_i)` is the normalised cone `c̃_s`.  One set of product lemmas serves both.
2. **Group**: Lemma 3 for an arbitrary *set* `G` of permutations of the sites that is transitive (no group structure is
   needed for (i)/(ii)).  Theorem A needs averaging over a group of order `n`: I take the sites `ι` to be any finite
   additive group acting on itself by translation (`Fin n` with `n ≥ 1` is the paper's cyclic shift).
3. **Lemma 2 abstractly**: for two probability vectors `P₁, P₂` on any finite type, `R > 1`, `D = (R·P₁ − P₂)₊`:
   `R − 1 ≤ ΣD ≤ R` and `|ΣDf/ΣD − ΣP₁f| ≤ 1/(R−1)` for every `f` with values in `[0,1]`.  No product structure.
4. Division-free forms where the paper divides (as L1 did).
5. Files: `Compensation.lean` (Mathlib only: cone, Lemma 3, Lemma 0, Lemma 2) and `TheoremA.lean`
   (imports `proofs.Frontiers.QueryLowerBound` read-only for `QueryAlgorithm` and the packing bound; repeats what it
   needs from the first file, because files here cannot import each other).
