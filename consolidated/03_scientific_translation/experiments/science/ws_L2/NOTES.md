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

## 20:07 UTC — sources read; first observations (before any Lean)

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

## 20:17 UTC — priority 1 DONE: `Sandwich.lean` (checks, 8 s, exit 0, no warning, no sorry)

34 headline declarations, all `[propext, Classical.choice, Quot.sound]`.

Abstract part (finite distributive lattice `α`, weights unnormalised):
`holley_cross_nonneg`, `holley_cross` (any monotone `φ`, no sign condition),
`updown_cross` (lower set `A`, upper set `B`, not necessarily complementary:
`w₁(B)·w₂(A) ≤ w₁(A)·w₂(B)`), `holley_condition_lower_of_saturation`,
`holley_condition_upper_of_saturation` (arbitrary envelope `d`, with the "saturation"
inequalities `d(x∨y,y) ≤ h↑x − h↑(x∧y)`, `d(x∧y,x) ≤ h↓(x∨y) − h↓y` as hypotheses),
`sandwich_cross_lower/upper`, `sandwich_mean`, `macrostate_cross_lower/upper`, `macrostate_ratio`.

No lattice at all (`Mixture` section): `exists_convex_ratio`, `mixRes`, `boltz_mixRes`,
`mixRes_admissible` (the class is convex in the weights, any envelope `d`, `β > 0`),
`exists_admissible_ratio` (a linear-fractional functional takes every value between its values
at two admissible residuals).

Cube `ι → Bool` (any finite `ι`): `envDist`, `field`, `envDist_sup_right`, `envDist_inf_left`
(saturation holds with equality), `field_admissible`, `neg_field_admissible` (need only
`0 ≤ cup i + cdn i`), `add_nonneg_of_admissible` (that condition is necessary for the class to
be non-empty), `cube_holley_lower/upper` (written out with `Real.exp`, as in the brief),
`cube_sandwich_cross_lower/upper`, `cube_sandwich_mean` (Theorem A11, inequalities),
`cube_macrostate_cross_lower/upper`, `cube_macrostate_ratio`, `cube_macrostate_ratio_compl`
(Corollary A11.1, inequalities), `cube_mean_isLeast`, `cube_mean_isGreatest` (ends attained),
`cube_mean_range_eq_Icc`, `cube_ratio_range_eq_Icc` (**"fills exactly the interval"**, `β > 0`),
`cube_sandwich_strict_witness` (two sites, `f = −[x₀∧x₁]`, `c = 1`, `g = 0`, `β = 1`,
`φ = [x₀]`: all hypotheses hold and both inequalities are strict).

What the formalisation showed (for the report):
1. `c↑, c↓ ≥ 0` is not needed anywhere; the sandwich needs no sign condition, attainment needs
   `c↑_i + c↓_i ≥ 0`, which is equivalent to non-emptiness of the class.
2. `β ≥ 0` is needed (implicit in the note) and `β > 0` for "every value in between" (the mixture
   residual divides by `β`; for `β = 0` the interval is a point and the statement is trivially true
   but not covered by `cube_mean_range_eq_Icc`).
3. `φ ≥ 0` not needed; Mathlib's `holley` (normalised) not used — `four_functions_theorem_univ`
   gives the cross-multiplied statement for unnormalised weights directly.
4. Corollary A11.1 holds for any lower set `A` and upper set `B` (e.g. two macrostates separated by
   a transition region), not only `A = X∖B`.
5. The proof never uses the cube: it works on any finite distributive lattice with any envelope
   `d` for which two functions saturate it in the sense above.  This is the note's Remark (1) in
   abstract form (the instance "product of chains" is not instantiated yet).
6. Technical: `(x ⊔ y) i = (x i || y i)` is `rfl`; proofs of the site identities are
   `cases x i <;> cases y i <;> simp`.  `linarith` multiplies out products of atoms, so the
   cross-multiplied forms follow by `linarith` from the four-functions statement.

Next: `Referee.lean` — R6.1, R5(2), then R6.2.

## 20:25 UTC — priority 2 (a), (b) DONE in `Referee.lean` (checks, 9 s, clean)

* R6.1: `partSum_twinMin` (`Z′ = Z₀ + E`), `enSum_twinMin`, `meanEn_twinMin_sub`
  (`U′ − U₀ = (D − U₀E)/(Z₀+E)`, no condition), `excess_identity` (referee's form, `E ≠ 0`),
  `excessMass_eq_zero_iff` (`E = 0 ⇔ g₀ ≤ T` everywhere), `twinMin_eq_of_excessMass_eq_zero`,
  `meanEn_twinMin_eq_iff` (`U′ = U₀ ⇔ D/E = U₀` for `E ≠ 0`).  Arbitrary finite type, two real
  functions.  Note for the report: the referee's formula divides by `E`; it is stated for
  `E ≠ 0`, and the case `E = 0` is the trivial one `g′ = g₀`.
* R5(2), abstract: `sum_sub_pair_min_le_sup'` (ordered pairs, factor ½),
  `sum_offDiag_eq_two_mul_sum_lt`, `sum_sub_pair_min_lt_le_sup'` (pairs `i < j`),
  `sum_sub_pair_min_needs_nonneg` (fails for `(0,0,−1)`), `distTo`, `sum_apply_distTo_le`,
  `flat_distTo_le` (any real `u`), `flat_distTo_le_card_mul` (`Z(flat^C) ≤ |C|·F₁`),
  `min_exp_le_exp_half`, `cone_distTo_ge` (`u ≥ 0`), `r5_2_abstract` (the assembled
  `log Z(cone^C) − log Z(flat^C) ≥ log A₁ − log F₁ + log(1−γ)` from: equal single-cone sums `A₁`,
  equal flattened sums `F₁`, pair sums `≤ κA₁`, `γ = ½(|C|−1)κ < 1`).
  Not yet: the cube facts (pair sum `= Z(cone)·cosh(u/2)^{−D}`, translation invariance).

Next: R6.2 (`Signs` section).  Plan: (A) pointwise comparison of the true excess sums with the
"free" ones (`g₀ ≡ 0`) with the overlap weight `ω` as error; (B) the basin/twin sums for an
ℕ-valued distance profile, levels `r₁`, `r₁ ± 1`; equidistribution of the two profiles through a
bijection; (C) two real-arithmetic lemmas for the signs; (D) continuity + intermediate value +
the bound on `ln Z′ − ln Z₀`.

## 20:33 UTC — priority 2 (c) DONE: Lemma R6.2 in full, `Referee.lean` (checks, 34 s, clean)

Abstract setting: finite non-empty `X`, two ℕ-valued distance profiles `d₀, d'` equidistributed
through a bijection `σ` (`d'(σx) = d₀x`), `u > 0`, `r₁ ≥ 1`; `basin u ρ d = −u(ρ − d)₊`,
`g₀ = basin u r₁ d₀`, `T_s = basin u (r₁+s) d'`, `g′_s = min(g₀, T_s)`.

* Layer A (any `g₀, T ≤ 0`): `excessMass_le_freeMass`, `freeMass_sub_overlapW_le`,
  `enSum_le_excessEnergy`, `excessEnergy_le`  (`E^f − ω ≤ E ≤ E^f`, `D^f ≤ D ≤ D^f + Mω`).
* Layer B: `partSum_basin` (`Z₀ = |X| + W − V`), `enSum_basin` (`= −A′`), `freeMass_basin_succ`,
  `enSum_basin_succ`, `freeMass_basin_pred`, `enSum_basin_pred`, `basinA_le` (`A′ ≤ u r W`),
  `sum_comp_of_equidist`.
* Layer C: `sign_plus_arith`, `sign_minus_arith`, `gain_arith` (pure real arithmetic).
* `r6_2_core`, `r6_2_signs` (**`U′_{+1} < U₀ < U′_{−1}`**), `r6_2_root` (**∃ `s* ∈ (−1,1)`,
  `U′_{s*} = U₀`, `log Z′_{s*} − log Z₀ ≥ log(1 + e^{−u}(1 − 1/r₁))`, `g′_{s*} = g₀` where
  `d' > r₁`**; continuity by `fun_prop`, root by `intermediate_value_Icc'`).
* `r6_2_binary_cube`: the same on `Fin n → ZMod 2` with Hamming distances to `a₀, a′`, `2ⁿ`, and
  `W = Σ_j C(n,j)[j<r₁]e^{u(r₁−j)}` (via `sum_hammingDist_binary`, copied idea from L1).

Findings: the lemma is correct as stated.  Hypotheses that are implicit in the report and explicit
in Lean: `u > 0`, `r₁ ≥ 1`.  `r₁ < n/2` (stated before the lemma) is not used.  The proof at
`s = −1` uses `ω_{−1} ≤ ω_{+1}` (`overlapW_mono`), which the report does not mention.
The constant 8 in (i) is not tight for the argument (the proof uses `rK ≤ ⅝·e^{−u}W`).
Not formalised: Lemma R6.3 (Hoeffding overlap bound), Theorem R6, Corollary R6′ (the abstract
form covers its "algebra is unchanged" sentence for two equidistributed profiles, but the
overlap bound "at most `|C|²` times that of a pair" is not formalised).

Next: `Window.lean` — Proposition A1.2 items 1–3.

## 20:41 UTC — priority 3 DONE: Proposition A1.2 items 1–3, `Window.lean` (checks, 12 s, clean)

* Item 1: `gibbsLaw`, `Admissible`, `window`; `gibbsLaw_mem_window`, `window_pos`,
  `exists_gibbsLaw_of_mem_window` (`γ = log π − log p`), `window_eq_gibbs_image`
  (`𝒲 = {π_γ : γ ∈ L}`), `window_convex`, `lipClass_extremePoints_eq_empty`
  (`L` has no extreme points — "vertices of the Lipschitz polytope" must be read mod constants).
  NOT done: the vertex correspondence.
* Item 2: `site_conditional_mem_window` (brief's `α × β` form; the weight on the rest only needs
  to be non-negative with positive mass and independent of the site letter),
  `cylW`, `condLaw`, `cylinder_cross_le`, `condLaw_mem_window` (dependent product `∀ i, S i`, any
  conditioning set `P ∌ i`, any pattern — contains every order and every prefix),
  `single_site_of_admissible` (class membership ⟹ single-site property, needs `d j s s ≤ 0`).
* Item 3: `klDivFin`, `KLBound`, `softMin`, `gibbsLaw_add_const`, `exp_neg_softMin`,
  `softMin_admissible`, `gibbsLaw_prod_apply` (marginal × conditional), `kl_gibbs_prod_eq`
  (**chain rule as an explicit identity on `α × β`**), `klBound_prod` (tensorisation of the
  bound), `kl_gibbs_prod_additive`, `gibbsLaw_equiv`, `klDivFin_gibbs_equiv`, `klBound_equiv`,
  `klBound_pi` (**item 3 inequality on `∀ i : Fin n, S i`, dependent alphabets, by induction on
  `n` through `Fin.consEquiv`**), `kl_additive_pi` (equality at additive instances),
  `kl_pi_isGreatest` (if `M i` is the greatest site value then `Σ M i` is the greatest value
  on the product class).

No entropy theory from Mathlib was needed: the chain rule for a Gibbs law against a product
vector is `log(ν₂(r)·ν(a|r)) − log(Q₁(a)Q₂(r))` split in two, with `Σ_a ν(a|r) = 1`.
`Q i` need not be normalised.

Findings for the report:
1. Hypotheses of A1.2 "`d_j ≥ 0` with the triangle inequality" are used nowhere in items 1–3.
   What IS used and is not listed: `d_j(a,a) ≤ 0` (i.e. `= 0`), in `single_site_of_admissible`
   and in `klBound_prod` — without it a member of `𝒞` can vary at site `i` by more than `d_i`
   (two sites, `d₁ ≡ 0`, `d₂ ≡ 1` (non-negative, triangle inequality holds), `ψ(a,r) = [a]`:
   in `𝒞`, conditional law of site 1 not in the window `{π₁}`).  To machine-check next.
2. "Vertices of the Lipschitz polytope `L_j`": `L_j` has no extreme points.
3. The statement proved is for arbitrary positive `Q i`, any `n`; the Shannon-centre/capacity
   reading (`= n·a`) and "max over vertices" (convexity of KL + vertex correspondence) remain
   on paper.

Next: report skeleton; then extras in this order: (E0) counterexample `d(s,s) > 0`;
(E1) R5(2) on the binary cube (pair-sum closed form); (E2) non-vacuity witness for R6.2;
(E3) A11 Remark (1), ordered alphabets; (E4) vertex correspondence of item 1.

## 20:48 UTC — extras E0 and E1 done

* E0 `window_needs_diag_zero` (`Window.lean`): two binary sites, `d₁ ≡ 0`, `d₂ ≡ 1`,
  `ψ(a,r) = [a]`: `ψ` in the class of `d₁ ⊕ d₂`, law of the first letter NOT in the window of
  `d₁`.  So A1.2 needs `d_j(a,a) = 0`, which it does not list (it lists `d_j ≥ 0` and the triangle
  inequality, neither of which is used).  `Window.lean` re-checked: clean, 12 s.
* E1 R5(2) on the binary cube (`Referee.lean`, section `BinaryCube`): `hammingDist_cast_eq_sum`,
  `cone_sum_binary` (`Z(cone) = (1+e^{−u})ⁿ`), `site_pair_sum`, `pair_sum_binary`
  (`Σ_x e^{−u(d(x,c)+d(x,c′))/2} = (1+e^{−u})ⁿ ρ^D`, `ρ = 2e^{−u/2}/(1+e^{−u})`),
  `rho_eq_inv_cosh` (`ρ = 1/cosh(u/2)`), `r5_2_binary_cube`:
  `n log(1+e^{−u}) − log Σ_j C(n,j)e^{−u max(j,R)} + log(1−γ) ≤ log Z(cone^C) − log Z(flat^C)`,
  `γ = ½(|C|−1)cosh(u/2)^{−δ} < 1`, for ANY non-empty set `C` of centres with pairwise distances
  `≥ δ`, any `u ≥ 0`, any real `R`.  (Report: coset of a linear code, `R ≥ 1`; neither linearity
  nor `R ≥ 1` is used.)  `Referee.lean` re-checked: clean (68 s wall, machine busy).

## 21:00 UTC — extras E2, E3 done; refactor; full check (clock read: 21:00)

* E2 `r6_2_nonvacuous` (`Referee.lean`): `n = 4`, `r₁ = 2`, `u = 6`, `a₀ = 0000`, `a′ = 1111`:
  (i) is `256e⁶ ≤ e¹² + 4e⁶` (from `e > 2.7`), (ii) holds because `ω_{+1} = 0`
  (`hammingDist x 0 + hammingDist x 1 = 4` by `decide` over the 16 points).  So the hypotheses
  of R6.2 are jointly satisfiable [V] (note `r₁ = 2 = n/2` here, not `< n/2`; the lemma does not
  need `r₁ < n/2`).
* Refactor of `Sandwich.lean`: the exact-range theorems are now abstract
  (`mean_range_eq_Icc`, `ratio_range_eq_Icc`: any finite distributive lattice, any envelope
  saturated by two admissible functions); the cube versions are corollaries.
* `field_submodular`, `pairTerm_submodular`, `submodular_sum`, `pairwise_submodular`: additive
  and pairwise-without-frustration known parts are submodular (the note's examples) [V].
* E3 Remark (1) of A11 (`Chains` section): product of finite chains `∀ i, Fin (k i)`,
  `chainDist`, `chainField`, saturation identities, admissibility of the two additive functions
  (`0 ≤ c↑ i r + c↓ i r`), `chain_sandwich_mean`, `chain_mean_range_eq_Icc`,
  `chain_ratio_range_eq_Icc`.
* `check_all.sh` → `check_log.txt` (20:57–20:59 UTC): `Sandwich.lean` 30 s, `Referee.lean` 78 s,
  `Window.lean` 23 s; exit codes 0; 105 `#print axioms` lines, all
  `[propext, Classical.choice, Quot.sound]`; no error, no warning; no forbidden token.

Next: write `L2_REPORT.md`.  Possible further extras afterwards: (E4) vertex correspondence of
A1.2 item 1 and "max at a vertex"; FKG nonnegativity of the summands of A11.2.

## 21:12 UTC — report drafted; all theorems now have `#print axioms`; full check clean

* Added `cube_sandwich_fails_negative_beta` (two-site witness at `β = −1`: lower inequality of
  A11 fails) — `β ≥ 0` is needed [V].
* Every theorem of every file now has a `#print axioms` line (59 + 62 + 27 = 148);
  `check_all.sh` (21:09–21:11 UTC): three exit codes 0, 148/148 lines
  `[propext, Classical.choice, Quot.sound]`, no error, no warning.
* Numerics extended: the Lean witness of R6.2 (`n=4, r₁=2, u=6`) and products of chains.
* `docs/science/workstreams/L2_REPORT.md` written (first complete version).

Next (extra E4): vertex correspondence of A1.2 item 1 — `gibbsLaw π γ` extreme in the window
⇔ `γ` extreme in the class normalised at a base point.  Plan: tight pairs; a perturbation
`θ` constant along tight pairs; `ε` = minimum over the finitely many pairs of
`slack/(1 + |Δθ|)` (1 on tight pairs).

## 21:27 UTC — extras E4 and A11.2-sign done; final full check

* E4 (`Window.lean`, sections `Vertices`, `VertexBound`):
  `lipNorm d a₀` (class normalised at a base point), `exists_pos_scale` (finitely many strict
  slacks leave a common positive scale), `eq_of_convex_comb_eq`, `window_slack_eq`,
  `window_tight_iff` (window constraint tight at `π_γ` ⇔ Lipschitz constraint tight at `γ`),
  `perturb_mem_lipNorm`, `perturb_mem_window`, `gibbsLaw_extreme_of_extreme`,
  `extreme_of_gibbsLaw_extreme`, **`extremePoints_window_eq`**:
  `extremePoints (window π d) = gibbsLaw π '' extremePoints (lipNorm d a₀)` — item 1's vertex
  statement in corrected form.
  `isCompact_window`, `klDivFin_convexOn_window` (from `Real.convexOn_mul_log`),
  `continuous_klDivFin`, **`klBound_of_vertices`** (Krein–Milman
  `closure_convexHull_extremePoints` + `ConvexOn.exists_ge_of_mem_convexHull`: a bound at the
  vertex laws is a bound on the class), **`klBound_pi_of_vertices`** (item 3's inequality as
  stated), `exists_site_max`, **`kl_pi_exists_isGreatest`** (site maxima exist; their sum is the
  greatest value over the product class).
  Remaining on paper for A1.2 items 1–3: finiteness of the vertex set; `Σ M_i = n·a`.
* A11.2, sign of the summands (`Sandwich.lean`, section `Occupation`): `updown_inter_cross`
  (`w(A∩U)w(B) ≤ w(A)w(B∩U)` for log-supermodular `w`, lower `A`, upper `B, U` — one application
  of the four functions theorem), `boltz_logSupermodular`, `field_modular`,
  `cube_occupation_cross`, `cube_occupation_mono` (`⟨x_i⟩_{A,t} ≤ ⟨x_i⟩_{B,t}`).  The integral
  formula itself is not formalised.
* `check_all.sh` 21:23–21:27 UTC: `Sandwich.lean` (1 247 lines, 64 theorems) 75 s,
  `Referee.lean` (1 396, 62) 92 s, `Window.lean` (1 295, 43) 50 s; exit codes 0; 169/169
  `#print axioms` lines `[propext, Classical.choice, Quot.sound]`; no error, no warning.
  (Wall times are inflated by the other workstreams; user time is 12–30 s per file.)

Next: update the report; final message.

## 21:35 UTC — the addenda file has grown since I started (read-only check with `git diff`)

`docs/science/INFERENCE_LIMITS_ADDENDA.md` section A11 is unchanged since my start (compared
with `a014576`), but the coordinator has added A12–A16.  Relevant to this workstream:
* **A13** "The sandwich of A11 on ordered alphabets (written out; replaces remark (1) of A11)":
  site envelopes are arbitrary quasi-metrics `d_i`, step fields
  `Γ↑ x = Σ_i Σ_{r<x_i} d_i(r+1,r)`, `Γ↓ x = Σ_i Σ_{r<x_i} d_i(r,r+1)`; bounds sound always,
  attained for path envelopes.  My abstract theorem covers it through the saturation
  *inequalities*; my `Chains` section has only the path-envelope case.  → add the general
  instance (triangle inequality telescoped along the order).
* **A12**, notes of the coordinator's second reading of R6.2: "the gain … `≥ e^{−u}(1 − 3/(4r₁))`,
  slightly better than stated" → check in Lean (my `gain_arith` proves the stated `1 − 1/r₁`).
* **A12**, Corollary R6′ written out, step (3): the two signs for coset profiles "follow as
  before" → the abstract `r6_2_*` apply; add the explicit instance for distances to translates
  of a finite set `C ⊂ F₂ⁿ`.

## 21:42 UTC — additions for A12/A13; final check; report final

* `Sandwich.lean`, section `StepFields` (addendum A13): `siteDist`, `stepUp`, `stepDn`,
  `le_sum_steps_up`, `le_sum_steps_dn` (triangle inequality telescoped along the order, by
  `Nat.le_induction`), `siteDist_sup_right_le`, `siteDist_inf_left_le`,
  `stepField_sandwich_mean`, `stepField_macrostate_ratio` — Theorem A13 for arbitrary site
  quasi-metrics [V]; attainment for path envelopes is the `Chains` section.
* `Referee.lean`: `gain_arith` now proves the constant `1 − 3/(4r)` (the note in A12's second
  reading is correct [V]); `r6_2_core` carries it; `r6_2_root_sharp` (sharp gain) and
  `r6_2_root` (referee's `1 − 1/r₁`, derived); `cosetDist`, `cosetDist_translate`,
  `r6_2_cosets` (Lemma R6.2 for distances to `a₀ + C`, `a′ + C`, any non-empty finite `C`:
  step (3) of "R6′ written out" in A12).
* Final `check_all.sh` 21:37–21:40 UTC: `Sandwich.lean` 1 392 lines / 70 theorems,
  `Referee.lean` 1 490 / 65, `Window.lean` 1 295 / 43; exit codes 0; 178/178 `#print axioms`
  lines `[propext, Classical.choice, Quot.sound]`; no error, no warning; no forbidden token.
* Mathlib `grep` for the items not done: `azuma`/`hoeffding` only in
  `Probability/Moments/SubGaussian.lean`; no hypergeometric distribution found.
* Report `docs/science/workstreams/L2_REPORT.md` updated to this state.

Where I stopped: everything in the brief is done; beyond it A13 and the finite parts of the A12
notes.  Not done: A11.2's integral, A11.3, R5(1),(3),(4), R6.3, Theorem R6, R6′ (4),(5),
A1.2 items 4–5, finiteness of the vertex set, `Σ M_i = n·a`.
