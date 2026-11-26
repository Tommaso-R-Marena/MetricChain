# Workstream L3 — notes (kept from the first minute)

Lean 4.31.0 + pinned Mathlib (v4.31.0, rev fabf563a).  Compile command (single files only):

    export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path>

## Log

* 23:33 UTC (2026-11-25) — started.  Read COMMON.md and L3_brief.md.  Created `experiments/science/ws_L3/`.
  `.lake/packages` present (mathlib, batteries, aesop, …).  Repository state: branch
  `research/scientific-translation`, head 25626db (checkpoint 33).  Nothing of mine exists yet.
* Next: read SF_REPORT.md §2.0–§2.2, the L1/L2 Lean files and reports, then plan the files.
* 23:34–23:38 — read SF_REPORT §2.0–2.2 (Lemmas 0–3, Theorem A), L1 `MarginalOracle.lean` (oracle-indexed model:
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

## Log (continued)

(Times marked ~ were not read from the clock when the step ended; they are bracketed by the readings 23:33 and 23:55.)

* ~23:42 — `sanity_numerics.py` written and run (S1–S5 pass: Lemma 3 (i)/(ii) on 7 site groups with non-product
  invariant reference weights, 287 cases, errors ≤ 2.3e−13; a transitive set that is not a group; window, 200 random
  class members; abstract Lemma 2, 20 000 random pairs, never violated; every finite ingredient of Theorem A for
  184 parameter sets over Z2…Z6, Z2×Z2, S3 — including the "sites = any finite group" generalisation).  The A16 part of
  the script still has a bug of mine (overflow) — to fix when I get to A16.
* ~23:47 — `Compensation.lean` Parts 1–3 compile (exit 0): cone, `LipH ↔ InCone`, Lemma 3 (i), Lemma 3 (ii) in the
  general form (`lemma3_compensation`: any reference weight, any transitive set of site permutations, any
  normalised invariant class member as compensator).
  Lean notes: a theorem named `InCone.max` makes `max` inside its own proof resolve to itself → renamed
  `inCone_max`/`inCone_min`; `by linarith` inside `rw [max_eq_left (by …)]` is elaborated before unification → state
  the inequality first; `rw` does not see through beta-redexes → `show`.
* 23:55 (clock read) — Parts 4–6 compile (exit 0, no warning): product weights, Bernoulli reference, additive instances with
  site-dependent fields, Lemma 0 (`window_of_site_odds`, `lemma0_window`, `lemma0_window_lipH`, `lemma0_additive_fill`),
  abstract Lemma 2 (`excess_mass_bounds`, `excess_mean_bound`), report forms (`lemma3_compensation_bernoulli`,
  `lemma2_mass`, `lemma2_site`, `lemma2_dens`, `densW_coneW`), identification of my definitions with the report's
  formulas (`baseW_eq`, `coneW_eq`).  26 `#print axioms`: all `[propext, Classical.choice, Quot.sound]`.
* 00:05 (clock read, 2026-11-26) — `TheoremA.lean` compiles (exit 0, no warning; 26 s): Lemma 1 (a) in the oracle-indexed
  model (`lemma1a_weighted`, `lemma1a`, `lemma1a_div`, from `MetricChain.expected_queries_ge_packing` on the class
  restricted to the oracle answer of `g₀`), its form in the weights for the one-body oracle (`oracle_packing_weights`),
  the family of alternatives (`barW`: translation average of dips; invariance, mass, density, class membership,
  counting bound `card_barW_ne_zero_le`), `E_{k,r}`, `c_{k,r}` depend on `(k,r)` only (`massW_densW_dipW_of_wt_eq`, via
  `Equiv.extendSubtype`), the choice of the compensator (`exists_compensator`), and **Theorem A, every-n statement**
  (`theoremA_group`: sites = any finite additive group).  `#print axioms theoremA_group`:
  `[propext, Classical.choice, Quot.sound]`.
  `TheoremA.lean` is generated by `assemble.py` = head + Parts 1–6 of `Compensation.lean` verbatim + `parts/TheoremA_tail.txt`.
  Findings while proving: (1) hypotheses `0 < u`, `n ≥ 2`, `1 ≤ k ≤ n−1` of Theorem A are not needed as separate
  hypotheses (`|γ| ≤ u` gives `u ≥ 0`; `(e^r − 1)ω_m > 1` with `r > 0`, `k ≤ n` forces the rest); (2) `b ≤ β − 1`
  actually, the report's `b ≤ β` is what is stated; (3) `k ≤ n` is not needed for the margin inequality (only for
  `T_k ≠ ∅`).
* Next: `theoremA_fin` (ι = Fin n), division form, positivity of `H_{k,r}`; then Lemma 0 rigidity?, the `ρ_t` form
  (optional), A16.5 core, A1.1 items.
* 00:11 — added `theoremA_group_sharp` (the proof gives `1 + b ≤ β`, so the threshold on `ε` improves from
  `ln(1 + (e^r−1)/(1+β))` to `ln(1 + (e^r−1)/β)`), the report's constants as a corollary (`theoremA_group`),
  `Hkr_pos`, the displayed form with division (`theoremA_group_div`), and `theoremA_fin` (`Fin n`, cyclic shifts).
  Both files compile, exit 0, no warning.  Lean note: `(by rw [Fintype.card_fin]; exact hk)` as an argument let the
  implicit `k` be unified with `n` by the `rfl` that `rw` tries — state the hypothesis first.
* Item 5 (A16.5): workstream R8's `A16Core.lean` already has (a)–(d) of the brief ([V] there: `sum_le_sum_f`,
  `f_le_max`, `f_mono_below`, `f_anti_above`, `F_mono`, `F_eq_plateau`, `sum_le_sum_F`, `plateau_optimal`).  R8's
  report (§7, T-R8-1) names what is missing for a full check: the rearrangement step with Harper's theorem as a
  hypothesis.  Plan, not duplicating: (1) the rearrangement lemma; (2) Lemma A16.5 assembled, conditional on
  Harper's inequality between the level-set counts and on the existence of the level; (3) `ConcaveOn` for `f_η`;
  (4) the general clipped maximiser (hill case `t* < 1`, and `η = 0`).
* Item 6 (A1.1 items 1–2): item 1 is in L2's `condLaw_mem_window` in window form; to add: the explicit interval
  `[a₀, a₁]` for the cube, any conditioning set.  Item 2: L2's `klBound_pi` is the general chain-rule bound; to add
  the two-letter specialisation `KL(ν_ψ‖Bern(r)ⁿ) ≤ n·max(KL(a₀‖r), KL(a₁‖r))`.
* 00:16 — `A16Rearrangement.lean` compiles (exit 0, no warning; 8 axioms lines standard).  Part 0 = R8's core
  verbatim (credited).  New: `sum_comp_le_of_card_le` (rearrangement, Harper as hypothesis), `lemmaA16_5_of_harper`
  (+ `_ge` form), `tail_of_harper` (η = 0), `f_concaveOn`, `F_eq_clip` (every level, hills included), `F_zero`,
  `sum_eq_sum_f_add`.  Numerics S6 re-written and passing (20 000 cases).
  Small generalisation found: the plateau needs only `φ(t_pl) ≥ 0`, not `= 0`.
* 00:19 — item 6, part 1: `condMarg_mem_window` in `Compensation.lean` (A1.1 item 1 in the explicit two-letter form,
  any conditioning set `P ∌ i`, any pattern): Lemma 0 generalised to a non-negative reference weight with positive
  mass (`window_of_site_odds_nonneg`) and applied to the reference weight restricted to a cylinder.
  Also added: `window_of_equal_marginals`, `lemma3_compensation_exists` (Remark (1) after Lemma 3, both directions).
* 00:22 — item 6, part 2: `ChainRuleCube.lean` compiles (exit 0, no warning): Part 0 = L2's chain rule verbatim
  (lines 69–93 and 421–757 of `ws_L2/Window.lean`, extracted by script), Part 1 new: `klB_le_max` (binary KL is
  largest at an end of an interval, from `Real.convexOn_mul_log`), `klDivFin_bern`, `klBound_bool`, `a1_item2`,
  `a1_item2_lip` (the bound of A1.1 item 2), `a1_item2_cone0/1` (equality at the two cones), `a1_item2_isGreatest`
  (the supremum over the class).  Numerics S7 added (300 members, all conditioning sets): no violation.
* 00:23 — `TheoremA.lean` re-assembled from the current `Compensation.lean` and recompiled.
* 00:25 — `no_compensation_at_upper_end/_lower_end` (finding F1: Remark (1) of Lemma 3 holds with the open window).
* 00:33 — first complete state: report written (`docs/science/workstreams/L3_REPORT.md`), `check_all.sh` run:
  four files, exit 0 each, 0 warnings, 33 + 23 + 8 + 11 axioms lines all standard, `TheoremA.lean` identical to the
  output of `assemble.py`.
* Next (optional in the brief): the Chernoff form `H_{k,r} ≤ (n+1) e^{tr} ρ_t(k/n;γ)ⁿ`.  Plan: (A) Markov with real
  powers pointwise; (B) `Σ_s Bern(m)ⁿ(s) ∏ ratio^t = ∏_i [...]` by `sum_prodW`; (C) `refW m s = m^k(1−m)^{n−k}` on `T_k`;
  (D) `|T_k| = C(n,k)`; (E) binomial mode bound `1 ≤ (n+1)·C(n,k)(k/n)^k(1−k/n)^{n−k}` by the ratio argument and
  `add_pow`.
* 00:39 — **the Chernoff form of Theorem A is machine-checked** (`TheoremA.lean` Part 10, compiled exit 0 first time,
  no warning): `binomPmf_step`, `binomPmf_le_mode`, `binomial_mode_bound` (`1 ≤ (n+1)·C(n,k)(k/n)^k(1−k/n)^{n−k}`),
  `card_wt_eq` (`|T_j| = C(n,j)`), `refW_eq_pow`, `one_le_of_dipW_pos` (Markov with real powers),
  `dipCount_mul_le`, `Hkr_le_chernoff` (`H_{k,r} ≤ (n+1) e^{tr} ρ_t(k/n;γ)ⁿ`, `t ≥ 0`, `0 < k < n`),
  `theoremA_group_chernoff`, `theoremA_fin_chernoff`.  Numerics S8 (1 680 cases, n = 2..8) passes.
  Remaining of Theorem A: only the "in particular" with `C_m` (a choice of `r`).
* 00:43 — **the last display of Theorem A is machine-checked** (`TheoremA.lean` Part 11: `theoremA_group_Cm`,
  `theoremA_fin_Cm`): with the explicit depth `r = ln C_m + ε` (so `e^r = C_m e^ε`) one instance `ψ₀` (independent of
  `t`) satisfies `1 − 2δ ≤ E|Q(ψ₀)|·n(n+1)·C_m·e^{tε}·ρ_t(k/n;γ)ⁿ` for all `t ∈ [0,1]`.  This replaces the report's
  "`r = ln(1 + max{…}) + η`, `η ↓ 0`" (finding F4: there the instance depends on `η`).  Checks used:
  `e^r − 1 ≥ 2/m̲ + 2/ω_m` ⇒ `(e^r−1)ω_m > 2`, `κ > ω_m/2`, `β < 2/m̲`; `C_m e^ε − 1 ≥ (1 + 2/m̲)(e^ε − 1)`;
  `e^{tr} = C_m^t e^{tε} ≤ C_m e^{tε}`.  Compiled exit 0, no warning.  So all three displays of Theorem A are [V].
