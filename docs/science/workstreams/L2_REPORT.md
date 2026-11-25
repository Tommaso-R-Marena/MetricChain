# Workstream L2 — machine-checking the science division's newest statements

*Lean 4.31.0 + Mathlib (the repository's pinned version, commit `fabf563a`).  Three files,
3 260 lines, in `experiments/science/ws_L2/`; log `NOTES.md`; last full check `check_log.txt`
(2026-11-25, see the time stamps in that file); numerics `sanity_numerics.py`.*

Labels: **[V]** machine-checked here (declaration named) · **[P]** paper proof given here ·
**[K]** known · **[N]** numerical only.

**What [V] means in this file.**  The declaration is in one of the three files; each file imports
only `Mathlib` and was checked on its own with
`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path>`;
exit code 0, no error, no warning; `#print axioms` was run for **every** theorem of every file
(148 in all) and printed exactly `[propext, Classical.choice, Quot.sound]` each time
(`check_log.txt`; re-run with `bash experiments/science/ws_L2/check_all.sh`).  No `sorry`,
`admit`, `native_decide` or `axiom` occurs in any file.  Nothing was written outside
`experiments/science/ws_L2/` and this report; `lake build` was never run.  All declarations are
in the namespace `ScienceL2`.  The files do not import each other or workstream L1.

What kind of check this is: every paper proof was first re-derived by hand (*independent
review*), the formal statements were then tested on random small instances with my own code
(§3; this is not a replication of the notes' own numerics), and finally proved in Lean.

---

## 1. Verdicts

All three priorities of the brief are done, each beyond the minimum asked.
**(1) Addendum A11.**  Theorem A11 and Corollary A11.1 are **[V] in full**: the two Holley
conditions, the sandwich for every monotone observable, the macrostate ratios, attainment of both
ends, and "fills exactly the interval" — on the cube, and more generally on *any finite
distributive lattice with any envelope that two functions saturate* (so Remark (1), products of
finite chains, is [V] as an instance).
**(2) Referee statements.**  R6.1 is [V].  R5(2) is [V] in abstract form *and* on the binary cube
with the referee's `D_R` and `γ`.  **Lemma R6.2 is [V] in full** — the two signs, the exact root
`s*` (intermediate value theorem), the bound on `ln Z′ − ln Z₀` and locality — in an abstract
setting and on the binary cube; its hypotheses are shown to be jointly satisfiable [V].
**(3) Proposition A1.2.**  Item 1: the window is the set of Gibbs laws of the Lipschitz class, and
is convex [V]; the vertex correspondence is not formalised.  Item 2 [V] in the report's form
(dependent product, any conditioning set, any pattern).  Item 3: the chain-rule inequality on
`∏_{i<n} S_i`, equality at additive instances, and "maximum over the class = sum of the site
maxima" are [V]; "site maximum is at a vertex" and the identification with `n·a` remain on paper.
**No statement was found false.**  Nine places where the formal statement differs from the text
are in §2.7.  The ones that matter: Proposition A1.2 lists two hypotheses on the site envelopes
that are not used and omits the one that is needed (`d_j(a,a) = 0`; machine-checked
counterexample without it); "the vertices of the Lipschitz polytope" cannot be read literally
(that set has no extreme points [V]); Theorem A11 needs `β ≥ 0` (machine-checked failure at
`β = −1`) but **no** sign condition on the envelope constants, and Corollary A11.1 holds for any
lower set against any upper set, not only for complementary macrostates.

## 2. Statements

### 2.1 Table: paper statement → Lean declaration → status

| paper statement | Lean declaration(s) | file | status; hypotheses as formalised |
|---|---|---|---|
| A11, Holley condition, lower end (brief, bullet 1) | `cube_holley_lower`; abstract `holley_condition_lower_of_saturation` | `Sandwich` | [V]; `f` submodular, `g` admissible, `β ≥ 0`; no condition on `c↑, c↓` |
| A11, Holley condition, upper end | `cube_holley_upper`; `holley_condition_upper_of_saturation` | `Sandwich` | [V]; same |
| Holley's inequality, cross-multiplied, unnormalised | `holley_cross_nonneg`, `holley_cross` | `Sandwich` | [V]; any finite distributive lattice; `φ` monotone of any sign |
| A11, sandwich cross-multiplied (brief, bullet 2) | `cube_sandwich_cross_lower`, `cube_sandwich_cross_upper` | `Sandwich` | [V]; every monotone `φ`, not only `φ ≥ 0` |
| **Theorem A11**, `E_{f+h↑}φ ≤ E_{f+g}φ ≤ E_{f−h↓}φ` | `cube_sandwich_mean`; abstract `sandwich_mean` | `Sandwich` | [V] |
| A11, "both ends are attained" | `cube_mean_isLeast`, `cube_mean_isGreatest`, `field_admissible`, `neg_field_admissible` | `Sandwich` | [V]; needs `c↑_i + c↓_i ≥ 0`, which is necessary for the class to be non-empty (`add_nonneg_of_admissible`) |
| A11, "every value in between is attained" | `cube_mean_range_eq_Icc`; abstract `mean_range_eq_Icc`, `exists_admissible_ratio`, `mixRes_admissible` | `Sandwich` | [V] for `β > 0` |
| **Corollary A11.1**, inequalities (brief, bullet 3) | `cube_macrostate_cross_upper`, `cube_macrostate_cross_lower`, `cube_macrostate_ratio`, `cube_macrostate_ratio_compl`; abstract `updown_cross`, `macrostate_ratio` | `Sandwich` | [V]; `A` any lower set, `B` any upper set (non-empty for the ratio form) |
| Corollary A11.1, "fills exactly the interval" | `cube_ratio_range_eq_Icc`; abstract `ratio_range_eq_Icc` | `Sandwich` | [V] for `β > 0` |
| A11, examples of submodular `f` (additive; pairwise, `J_ij ≤ 0`) | `field_submodular`, `pairTerm_submodular`, `pairwise_submodular` | `Sandwich` | [V] |
| A11, Remark (1), ordered alphabets | `chainDist_sup_right`, `chainDist_inf_left`, `chainField_admissible`, `neg_chainField_admissible`, `chain_sandwich_mean`, `chain_mean_range_eq_Icc`, `chain_ratio_range_eq_Icc` | `Sandwich` | [V]; alphabets `Fin (k i)`, costs `c↑ i r`, `c↓ i r` with `c↑ + c↓ ≥ 0` |
| satisfiable instance with strict conclusion (brief, bullet 5) | `cube_sandwich_strict_witness` | `Sandwich` | [V]; two sites, `f = −[x₀∧x₁]`, `c = 1`, `g = 0`, `β = 1`, `φ = [x₀]` |
| `β ≥ 0` is needed | `cube_sandwich_fails_negative_beta` | `Sandwich` | [V]; same instance, `β = −1` |
| Corollaries A11.2, A11.3; "the hypotheses are needed"; Remark (2) | — | — | not formalised (§5) |
| **R6.1**, `Z′ = Z₀ + E` | `partSum_twinMin` | `Referee` | [V]; any finite type, any `g₀, T` |
| R6.1, `U′ − U₀ = (E/(Z₀+E))(D/E − U₀)` | `excess_identity`; division-free `meanEn_twinMin_sub` | `Referee` | [V]; the referee's form for `E ≠ 0` |
| R6.1, "unchanged iff the mean energy of the excess mass is `U₀`" | `meanEn_twinMin_eq_iff`, `excessMass_eq_zero_iff`, `twinMin_eq_of_excessMass_eq_zero` | `Referee` | [V] |
| **R5(2)**, max ≥ sum − pairwise minima | `sum_sub_pair_min_le_sup'`, `sum_sub_pair_min_lt_le_sup'`, `sum_offDiag_eq_two_mul_sum_lt` | `Referee` | [V]; non-negative terms; fails otherwise: `sum_sub_pair_min_needs_nonneg` |
| R5(2), `Z(flat^C) ≤ |C|·Z(flat)` | `flat_distTo_le`, `flat_distTo_le_card_mul`, `sum_apply_distTo_le` | `Referee` | [V]; any real `u`, `R` |
| R5(2), `Z(cone^C) ≥ |C|Z(cone) − Σ_{pairs}Σ_x e^{−u(d+d′)/2}` | `cone_distTo_ge` | `Referee` | [V]; `u ≥ 0` |
| R5(2), `ln Z(cone^C) − ln Z(flat^C) ≥ D_R + ln(1−γ)` | `r5_2_abstract`; **`r5_2_binary_cube`** with `pair_sum_binary`, `rho_eq_inv_cosh`, `cone_sum_binary`, `sum_hammingDist_binary` | `Referee` | [V]; any finite set of centres with pairwise distances `≥ δ`; `D_R` and `γ` as in the report |
| R5(1), (3), (4) | — | — | not formalised |
| **R6.2**, `U′_{+1} < U₀ < U′_{−1}` under (i), (ii) | `r6_2_signs` (abstract), `r6_2_binary_cube` | `Referee` | [V]; `u > 0`, `r₁ ≥ 1` explicit; `r₁ < n/2` not needed |
| R6.2, exact root, gain, locality | `r6_2_root`, `r6_2_binary_cube` | `Referee` | [V] |
| R6.2, hypotheses satisfiable | `r6_2_nonvacuous` | `Referee` | [V]; `n = 4`, `r₁ = 2`, `u = 6`, antipodal centres |
| R6.3, Theorem R6, Corollary R6′ | — | — | not formalised (the abstract `r6_2_*` apply verbatim to the coset profiles of R6′) |
| **A1.2 item 1**, `𝒲 = {π_γ : γ ∈ L}`, convex | `window_eq_gibbs_image`, `gibbsLaw_mem_window`, `exists_gibbsLaw_of_mem_window`, `window_convex` | `Window` | [V]; `π > 0` |
| A1.2 item 1, vertices | `lipClass_extremePoints_eq_empty` | `Window` | the literal reading is empty [V]; the intended statement is [P] here (§2.6), not machine-checked |
| **A1.2 item 2** (brief's `α × β` form) | `site_conditional_mem_window` | `Window` | [V]; weight on the rest only `≥ 0`, positive mass |
| A1.2 item 2 (report's form) | `cylinder_cross_le`, `condLaw_mem_window`, `single_site_of_admissible` | `Window` | [V]; dependent product, any conditioning set `P ∌ i`, any pattern |
| A1.2 needs `d_j(a,a) = 0` | `window_needs_diag_zero` | `Window` | [V] counterexample |
| **A1.2 item 3**, `KL(ν_ψ‖⊗Q_i) ≤ Σ_i M_i` | `klBound_pi`, `klBound_prod`, `kl_gibbs_prod_eq`, `softMin_admissible` | `Window` | [V]; `M_i` any bound on `KL(π_γ‖Q_i)` over `L_i` |
| A1.2 item 3, equality at additive instances | `kl_additive_pi`, `kl_gibbs_prod_additive` | `Window` | [V] |
| A1.2 item 3, `sup_𝒞 = Σ_i max_{L_i}` | `kl_pi_isGreatest` | `Window` | [V], *given* that each site maximum exists |
| A1.2 item 3, "max over vertices", `= n·a`; items 4, 5 | — | — | not formalised |

### 2.2 Addendum A11 (`Sandwich.lean`) [V]

**Definitions.**  `boltz β e x = exp(−(β·e x))`; `Admissible d g := ∀ x y, g x − g y ≤ d x y`;
`Submodular f := ∀ x y, f (x ⊔ y) + f (x ⊓ y) ≤ f x + f y`;
`gibbsMean β e φ = (Σ_x φ x·boltz β e x)/Σ_x boltz β e x`; `zOn β e S = Σ_{x∈S} boltz β e x`.
On `ι → Bool` (`ι` any finite type): `envDist cup cdn x y = Σ_i [x_i ∧ ¬y_i]·cup i + Σ_i [¬x_i ∧ y_i]·cdn i`
(the brief's formula) and `field c x = Σ_i [x_i]·c i`.

**The abstract theorem** (`sandwich_mean`, `mean_range_eq_Icc`, `ratio_range_eq_Icc`).  Let `α`
be a finite distributive lattice, `d : α → α → ℝ` *arbitrary*, `f` submodular, `β ≥ 0`, and let
`h↑, h↓ : α → ℝ` satisfy

    d (x ⊔ y) y ≤ h↑ x − h↑ (x ⊓ y),        d (x ⊓ y) x ≤ h↓ (x ⊔ y) − h↓ y        for all x, y.

Then for every `g` admissible for `d` and every monotone `φ`:
`E_{f+h↑} φ ≤ E_{f+g} φ ≤ E_{f−h↓} φ`; for a lower set `A` and a non-empty upper set `B`:
`Z_{f−h↓}(A)/Z_{f−h↓}(B) ≤ Z_{f+g}(A)/Z_{f+g}(B) ≤ Z_{f+h↑}(A)/Z_{f+h↑}(B)`.  If moreover `h↑` and
`−h↓` are admissible and `β > 0`, the set of values of `E_{f+g}φ` (resp. of the ratio) over the
admissible class **equals** the closed interval between the two ends.

On the cube the two displayed inequalities are identities (`envDist_sup_right`,
`envDist_inf_left`), which gives Theorem A11 and Corollary A11.1 as stated in the note
(`cube_sandwich_mean`, `cube_mean_range_eq_Icc`, `cube_ratio_range_eq_Icc`, …).  On a product of
chains `∏_i {0,…,k_i−1}` with costs `c↑ i r` (raise site `i` from level `r` to `r+1`) and
`c↓ i r` (lower it from `r+1` to `r`), `d x y = Σ_i (Σ_{y_i ≤ r < x_i} c↑ i r + Σ_{x_i ≤ r < y_i} c↓ i r)`,
`h↑ x = Σ_i Σ_{r<x_i} c↑ i r`, they are identities too (`chainDist_sup_right`,
`chainDist_inf_left`): Remark (1) of the note is [V] (`chain_sandwich_mean`,
`chain_mean_range_eq_Icc`, `chain_ratio_range_eq_Icc`).

**Proof structure as formalised.**
(a) `holley_cross`: for non-negative `w₁, w₂` with `w₁ x·w₂ y ≤ w₁(x⊓y)·w₂(x⊔y)` and monotone `φ`,
`(Σφw₁)(Σw₂) ≤ (Σw₁)(Σφw₂)`.  This is Mathlib's `four_functions_theorem_univ` with
`f₁ = φw₁, f₂ = w₂, f₃ = w₁, f₄ = φw₂` for `φ ≥ 0`; the general case follows because the
inequality is invariant under `φ ↦ φ + c`.  Mathlib's `holley` is not used (it assumes
`Σf = Σg`).  (b) `updown_cross`: `w₁(B)·w₂(A) ≤ w₁(A)·w₂(B)` from `four_functions_theorem` with
`s = B, t = A` and `B ⊼ A ⊆ A`, `B ⊻ A ⊆ B`.  (c) The Holley conditions are the note's two
lines.  (d) "Every value in between": for `β > 0` and admissible `g₀, g₁` the residual
`mixRes β g₀ g₁ t = −β⁻¹ log((1−t)e^{−βg₀} + t e^{−βg₁})` is admissible for every `t ∈ [0,1]`
(`mixRes_admissible`; *any* type, *any* envelope — "the class is convex in the weights"), its
Boltzmann weight is the convex combination (`boltz_mixRes`), and a ratio of two linear functionals
of the weights takes every value between its values at the ends at an explicit `t`
(`exists_convex_ratio`; no continuity argument is needed).

**Instances.**  `cube_sandwich_strict_witness`: two sites, `f = −[x₀∧x₁]`, `c↑ = c↓ = 1`, `g = 0`,
`β = 1`, `φ = [x₀]`: `f` is submodular, `φ` monotone, `g` admissible, and
`E_{f+h↑}φ = 2e⁻¹/(1+3e⁻¹) < E_fφ = (1+e)/(3+e) < E_{f−h↓}φ = (e+e³)/(1+2e+e³)`.
`cube_sandwich_fails_negative_beta`: the same instance at `β = −1` has `E_{f+h↑}φ > E_{f+g}φ`.

### 2.3 Lemma R6.1 (`Referee.lean`, section `Excess`) [V]

`X` any finite type, `g₀, T : X → ℝ` arbitrary; `twinMin g₀ T = min(g₀, T)`,
`partSum g = Σe^{−g}`, `enSum g = Σ g e^{−g}`, `meanEn g = enSum g/partSum g`,
`excessMass g₀ T = Σ max(e^{−T} − e^{−g₀}, 0)`,
`excessEnergy g₀ T = Σ_x [T x < g₀ x](T e^{−T} − g₀ e^{−g₀})`.
`partSum_twinMin`: `Z′ = Z₀ + E`.  `meanEn_twinMin_sub`: `U′ − U₀ = (D − U₀E)/(Z₀+E)`.
`excess_identity`: for `E ≠ 0`, `U′ − U₀ = (E/(Z₀+E))·(D/E − U₀)`.
`meanEn_twinMin_eq_iff`: for `E ≠ 0`, `U′ = U₀ ⇔ D/E = U₀`.
`excessMass_eq_zero_iff`: `E = 0 ⇔ g₀ ≤ T` everywhere, and then `g′ = g₀`.

### 2.4 R5(2) (`Referee.lean`, sections `Centres`, `BinaryCube`) [V]

Abstract: a finite type `X`, a non-empty finite set `C` of centres, profiles `dist c : X → ℝ`,
`distTo x = min_{c∈C} dist c x`.
`sum_sub_pair_min_le_sup'`: for `a_i ≥ 0`,
`Σ_i a_i − ½Σ_i Σ_{j≠i} min(a_i,a_j) ≤ max_i a_i` (`sum_sub_pair_min_lt_le_sup'`: the same with
`Σ_{i<j}`).  `flat_distTo_le`: `Σ_x e^{−u·max(distTo x, R)} ≤ Σ_{c∈C} Σ_x e^{−u·max(dist c x, R)}`
for all real `u, R`.  `cone_distTo_ge`: for `u ≥ 0`,
`Σ_x e^{−u·distTo x} ≥ Σ_c Σ_x e^{−u·dist c x} − ½Σ_c Σ_{c′≠c} Σ_x e^{−u(dist c x + dist c′ x)/2}`.
`r5_2_abstract`: if every `Σ_x e^{−u·dist c x} = A₁`, every `Σ_x e^{−u·max(dist c x,R)} = F₁`, every
pair sum is `≤ κA₁`, and `γ = ½(|C|−1)κ < 1`, then
`log A₁ − log F₁ + log(1−γ) ≤ log Z(cone^C) − log Z(flat^C)`.

Binary cube (`Fin n → ZMod 2`, `dist c x = d_H(x,c)`): `cone_sum_binary`
(`Z(cone) = (1+e^{−u})ⁿ`), `pair_sum_binary`
(`Σ_x e^{−u(d(x,c)+d(x,c′))/2} = (1+e^{−u})ⁿ ρ^{d_H(c,c′)}`, `ρ = 2e^{−u/2}/(1+e^{−u})`),
`rho_eq_inv_cosh` (`ρ = 1/cosh(u/2)`), and

**`r5_2_binary_cube`**: for any non-empty finite `C ⊂ F₂ⁿ` with pairwise distances `≥ δ`, `u ≥ 0`,
real `R`, and `γ = ½(|C|−1)cosh(u/2)^{−δ} < 1`:

    n·log(1+e^{−u}) − log Σ_j C(n,j) e^{−u·max(j,R)} + log(1−γ)  ≤  log Z(cone^C) − log Z(flat^C).

This is statement (2) of Theorem R5 with the referee's `D_R` in closed form.  Linearity of the code
and `R ≥ 1` are not used; the coset `a + C` of the report is the set of centres.

### 2.5 Lemma R6.2 (`Referee.lean`, sections `Signs`, `BinaryCube`) [V]

**Abstraction chosen.**  A finite non-empty type `X`; two ℕ-valued "distance profiles"
`d₀, d′ : X → ℕ` that are *equidistributed through a bijection* (`σ : X ≃ X`, `d′(σx) = d₀x`);
`u > 0`; `r₁ ≥ 1`.  `basin u ρ d = −u(ρ − d)₊`; `g₀ = basin u r₁ d₀`; `T_s = basin u (r₁+s) d′`;
`g′_s = min(g₀,T_s)`; `W = Σ_{d₀<r₁} e^{u(r₁−d₀)}`; `ω_s = Σ_{g₀<0, T_s<0} e^{−T_s}`; `|X|` in
the place of `2ⁿ`.  This covers the cube with two centres (`σ` = translation; `r6_2_binary_cube`
states the result with `2ⁿ` and `W = Σ_j C(n,j)[j<r₁]e^{u(r₁−j)}`), and the coset profiles of
Corollary R6′.

**`r6_2_signs`.**  If (i) `8 r₁ e^u |X| ≤ W` and (ii) `ω_{+1} ≤ e^{−u}W/(2(r₁+1))`, then
`U′_{+1} < U₀ < U′_{−1}`.
**`r6_2_root`.**  Under the same hypotheses there is `s* ∈ (−1,1)` with `U′_{s*} = U₀`,
`log Z′_{s*} − log Z₀ ≥ log(1 + e^{−u}(1 − 1/r₁))`, and `g′_{s*}(x) = g₀(x)` whenever `d′(x) > r₁`.
**`r6_2_nonvacuous`.**  For `n = 4`, `r₁ = 2`, `u = 6`, `a₀ = 0000`, `a′ = 1111` both hypotheses
hold ((i) is `256e⁶ ≤ e¹² + 4e⁶`; `ω_{+1} = 0`).

**The inequalities used, isolated** (what the proof consists of):
*Layer A* (any `g₀, T ≤ 0`; `E^f = Σ(e^{−T}−1)`, `D^f = ΣTe^{−T}` the sums "if `g₀` were `0`"):
`E^f − ω ≤ E ≤ E^f` (`freeMass_sub_overlapW_le`, `excessMass_le_freeMass`) and
`D^f ≤ D ≤ D^f + Mω` when `T ≥ −M` (`enSum_le_excessEnergy`, `excessEnergy_le`).
*Layer B*: `Z₀ = |X| + W − V`, `Σg₀e^{−g₀} = −A′`, `A′ ≤ u r₁ W`;
`E^f_{+1} = e^u(W+c) − (V+c)`, `D^f_{+1} = −e^u(A′ + u(W+c))` with `c = #{d₀ = r₁}`;
`E^f_{−1} = e^{−u}W − V`, `D^f_{−1} = −e^{−u}(A′ − uW)` (`partSum_basin`, …, `enSum_basin_pred`).
*Layer C* (real arithmetic, `q = A′/Z₀ = −U₀`): `sign_plus_arith` (`D + qE < 0`),
`sign_minus_arith` (`D + qE > 0`), `gain_arith` (`e^{−u}(1−1/r₁)Z₀ ≤ e^{−u}W − V − ω`).
*Root*: `s ↦ U′_s` is continuous (`fun_prop`), `intermediate_value_Icc'`; `Z′_s ≥ Z′_{−1}`
(`partSum_twinMin_mono`).

### 2.6 Proposition A1.2, items 1–3 (`Window.lean`)

`gibbsLaw π γ a = π a e^{−γ a}/Σ_b π b e^{−γ b}`;
`window π d = {p : p ≥ 0, Σp = 1, π a·p b ≤ e^{d a b}·π b·p a ∀a,b}`;
`klDivFin p q = Σ p(log p − log q)`.

**Item 1 [V, except vertices].**  `window_eq_gibbs_image`: for `π > 0`,
`window π d = {gibbsLaw π γ : γ a − γ b ≤ d a b}` (`⊆` with `γ = log π − log p`; members of the
window are strictly positive, `window_pos`).  `window_convex`.  The class
`L = {γ : γ a − γ b ≤ d a b}` has **no extreme points** (`lipClass_extremePoints_eq_empty`), so
"its vertices are the Gibbs laws of the vertices of the Lipschitz polytope" must be read with `L`
taken modulo constants (or normalised at a base point).  With that reading the statement is true
**[P, not machine-checked, not checked numerically]**: for `p = π_γ` call a pair `(a,b)` *tight*
if `π a·p b = e^{d a b}π b·p a`, equivalently `γ a − γ b = d a b`.  If `p = ½(p₁+p₂)` in the
window, tight pairs are tight for `p₁, p₂`, so `η = (p₁−p₂)/p` is constant along tight pairs and
not constant; then `γ ± ε(η − η(a₀))` stay in the class for small `ε` (finitely many slack
constraints), so `γ` is not extreme.  The converse is the same computation backwards.  Both
directions say: extreme ⇔ the graph of tight pairs is connected.

**Item 2 [V].**  `condLaw_mem_window`: on `∏_i S_i` (finite alphabets, `π_i > 0`), for every `ψ`
with `ψ(x) − ψ(x^{i←b}) ≤ d(x_i,b)` (true for every `ψ ∈ 𝒞` when the envelopes vanish on the
diagonal: `single_site_of_admissible`), every site `i`, every set `P ∌ i` of sites and every
pattern `y` on `P`: the conditional law of `x_i` given `x_P = y_P` under `ν_ψ` lies in
`window (π i) d`.  "Every order of the sites and every prefix" is the case `P = {sites before i}`.
The proof is the bijection `x ↦ x^{i←b}` between cylinders (`cylinder_cross_le`).
`site_conditional_mem_window` is the two-factor form asked for in the brief.

**Item 3 [V, in the following form].**
`kl_gibbs_prod_eq` (chain rule, two factors): for positive `π₁, π₂, Q₁, Q₂` and any `ψ` on `α×β`,

    KL(ν_ψ ‖ Q₁⊗Q₂) = KL(ν_{ψ₂} ‖ Q₂) + Σ_r ν_{ψ₂}(r)·KL(π₁-Gibbs law of ψ(·,r) ‖ Q₁),
    ψ₂(r) = −log Σ_a π₁(a) e^{−ψ(a,r)}   (the soft minimum; admissible by `softMin_admissible`).

`klBound_pi`: for alphabets `S_i`, `i < n`, positive `π_i`, positive `Q_i` (not necessarily
normalised), envelopes with `d_i(s,s) ≤ 0`: if `KL(π_γ‖Q_i) ≤ M_i` for all `γ ∈ L_i`, then
`KL(ν_ψ ‖ ⊗Q_i) ≤ Σ_i M_i` for every `ψ` with `ψ x − ψ y ≤ Σ_i d_i(x_i,y_i)`.
`kl_additive_pi`: `KL(ν_ψ‖⊗Q_i) = Σ_i KL(π_{γ_i}‖Q_i)` for `ψ = Σ_i γ_i(x_i)`.
`kl_pi_isGreatest`: if every site has a greatest value `M_i` of `KL(π_γ‖Q_i)` over `L_i`, then
`Σ_i M_i` is the greatest value of `KL(ν_ψ‖⊗Q_i)` over `𝒞`.
The proof is induction on `n` through `Fin.consEquiv` (`klBound_equiv`, `klDivFin_gibbs_equiv`
transport along the equivalence).  No relative-entropy theory from Mathlib is used.
Remaining on paper: existence of the site maximum (compactness), its location at a vertex
(convexity of `KL(·‖Q)` + item 1), and `Σ_i M_i = n·a` for the Shannon centres (the minimax
characterisation of capacity, [K]).

### 2.7 Discrepancies between the formal statements and the texts

1. **A1.2: the hypotheses on the site envelopes are the wrong ones as listed.**  The proposition
   assumes "envelopes `d_j ≥ 0` with the triangle inequality".  Neither is used in items 1–3.
   What is used is `d_j(a,a) = 0` (`single_site_of_admissible`, `klBound_prod`), and it does not
   follow from the two listed properties (`d ≡ 1` has both).  Without it item 2 is false **[V]**
   (`window_needs_diag_zero`: two binary sites, uniform `π`, `d₁ ≡ 0`, `d₂ ≡ 1`, `ψ(a,r) = [a]`
   is in the class, and the law of the first letter is not in the window of `d₁`).  If "envelope"
   is read as a quasi-metric (the programme's convention), the proposition stands; the formal
   statement needs `d_j(a,a) ≤ 0` and nothing else.
2. **A1.2 item 1, "vertices of the Lipschitz polytope `L_j`".**  `L_j` is invariant under adding
   constants and has no extreme points **[V]**.  The statement is about `L_j` modulo constants
   (§2.6, [P]).
3. **A11 needs `β ≥ 0`** (not stated; for `β < 0` the order reverses, **[V]**
   `cube_sandwich_fails_negative_beta`).  "Every value in between" is formalised for `β > 0`
   (for `β = 0` the interval is a point).
4. **A11 needs no sign condition on `c↑, c↓`.**  The brief asks for non-negative constants; the
   sandwich holds for arbitrary real constants, and attainment needs exactly `c↑_i + c↓_i ≥ 0`,
   which is equivalent to the class being non-empty **[V]** (`add_nonneg_of_admissible`,
   `field_admissible`).  Likewise `φ ≥ 0` (brief) is not needed.
5. **Corollary A11.1 is stated for `A = X∖B`, "both non-empty".**  It holds, with the same two
   extremal fields, for *any* lower set `A` and *any* upper set `B` (e.g. two macrostates
   separated by a transition region); only `B ≠ ∅` is needed, for the ratio to make sense
   **[V]**.
6. **A11, Remark (1) is a theorem**, and the proof never uses the cube: the abstract statement of
   §2.2 isolates what is used (a finite distributive lattice and two functions that saturate the
   envelope) **[V]**.
7. **R6.1 divides by `E`.**  The identity is stated for `E ≠ 0`; `E = 0` iff the twin is nowhere
   below `g₀`, and then `g′ = g₀` **[V]**.  The division-free form `U′ − U₀ = (D − U₀E)/(Z₀+E)`
   needs no condition.
8. **R6.2: implicit hypotheses and an unused one.**  `u > 0` and `r₁ ≥ 1` are needed and explicit
   in Lean; `r₁ < n/2` (stated before the lemma) is not used; the step at `s = −1` uses
   `ω_{−1} ≤ ω_{+1}` (`overlapW_mono`), which the report's proof does not mention; the proof
   needs only `r₁(|X| + ω) ≤ ⅝·e^{−u}W`, so the constant 8 in (i) has room.  The lemma itself is
   correct as stated.
9. **R5(2): weaker hypotheses suffice.**  Any finite set of centres with pairwise distances
   `≥ δ` (no linearity, no coset structure), any real `R`; `Z(flat^C) ≤ |C|Z(flat)` for every real
   `u`.  Non-negativity in "max ≥ sum − pairwise minima" is needed for three or more terms
   (`(0,0,−1)`, **[V]**); the referee states it.

## 3. Numerics

`experiments/science/ws_L2/sanity_numerics.py` (seed fixed; 45–95 s depending on machine load;
output in `sanity_numerics_output.txt`).  Purpose: to try to falsify the *formal statements*, with
the hypotheses exactly as in the Lean files, before proving them.  Nothing below is evidence for a
theorem; the theorems are proved.  All **[N]**:

| check | sizes | result |
|---|---|---|
| A11: admissibility of the fields, both Holley conditions, sandwich for a monotone `φ` of mixed sign, macrostate products | 400 instances, `n ≤ 4`, random submodular `f`, random admissible `g` (McShane form), half with *signed* constants (`c↑+c↓ ≥ 0`) | worst violation `3.5e−15` (relative); strict inequality in 400/400 |
| A11 at `β = −1` | two sites, `f = g = 0` | `E_{f+h↑}φ = 1.354 > 1 = E_{f+g}φ` |
| A11 Remark (1), chains | 200 instances, ≤ 3 sites, ≤ 3 levels, signed costs | worst violation `2.4e−15` |
| R6.1 | 2 000 pairs `(g₀,T)`, ≤ 8 points, with ties and with `E = 0` | identity error `≤ 2.7e−15` |
| R5(2) | 3 000 non-negative families; cubes `n = 3…8` with random centre sets | least slack `≥ −4.4e−16`; pair-sum closed form to `1e−9` relative |
| R6.2, exact sums by distance classes | 2 622 instances, `n = 12…40`, all `r₁ < n/2`, `u ∈ [0.5,6]`, 7 distances | hypotheses hold in 465; conclusion violated in 0; each hypothesis alone does not give both signs |
| R6.2, the Lean witness | `n = 4`, `r₁ = 2`, `u = 6`, antipodal | `W/(8r₁e^u2ⁿ) = 1.59`, `ω_{+1} = 0`, `U′_{±1} − U₀ = −5.986, +0.0145`, `s* = −1.94e−4`, `ln Z′_{s*} − ln Z₀ = 0.6925 ≥ 0.0012` |
| A1.2 items 2, 3 | 300 instances, ≤ 3 sites, 2–3 letters, asymmetric envelopes; all sites, all conditioning sets; window maxima by LP in random directions | window violation `≤ 3.3e−16`; chain-rule identity `≤ 8.9e−16`; `Σ` window maxima `− KL ≥ −6.7e−16` |

## 4. Prior art and search log

This workstream formalises; it makes no novelty claim for any proof (all are textbook
arguments), and no literature search was made.  Facts about the library, from the local copy
(`.lake/packages/mathlib`):
`Mathlib/Combinatorics/SetFamily/FourFunctions.lean` **[full text read]** has
`four_functions_theorem`, `four_functions_theorem_univ`, `holley`, `fkg` on a finite distributive
lattice; `holley` is stated for `Σf = Σg`; the file has no stochastic-domination statement for
unnormalised weights and no statement for up-sets/down-sets (both are a few lines from
`four_functions_theorem`, §2.2).  `Mathlib/InformationTheory/Hamming.lean` **[declaration list
read]**: `hammingDist_comp`, `hammingDist_eq_hammingNorm` used.  The chain rule for relative
entropy in `Mathlib/InformationTheory/KullbackLeibler/ChainRule.lean` **[not opened]** is
measure-theoretic and was not needed.  Two lemmas (`supportEquiv`, `sum_hammingNorm_binary`) are
copied from workstream L1 (`experiments/science/ws_L1/MarginalOracle.lean`).

## 5. Not done, and why

* **A11**: Corollary A11.2 (the width formula is an integral over `t`; the non-negativity of its
  summands is one application of Mathlib's `fkg` and was not written); Corollary A11.3;
  "the hypotheses are needed" (numerical in the note); Remark (2) (symmetry).
* **R5**: (1) (membership of the class, Lemma 1 — the latter is in L1), (3) (the query bound;
  L1 has the corresponding assembly for Theorem 4′), (4) (random codes).
* **R6**: Lemma R6.3 (Hoeffding for sampling without replacement — not in Mathlib as far as I
  saw; not searched systematically), Theorem R6 (needs R6.3 and the indistinguishability
  argument), Corollary R6′ beyond the remark that the abstract `r6_2_*` apply to coset profiles.
* **A1.2**: the vertex correspondence of item 1 ([P] in §2.6); "a convex function on the window is
  maximal at a vertex"; existence of the site maximum; `Σ_i M_i = n·a`; items 4 (Azuma) and 5.
* For `β = 0` the "fills exactly" statements are true and trivial but are not covered by
  `cube_mean_range_eq_Icc` / `cube_ratio_range_eq_Icc` (they assume `β > 0`).

## 6. Three next steps

1. The vertex correspondence of A1.2 item 1 (extreme points of `window π d` ⇔ extreme points of
   the normalised Lipschitz class ⇔ connected tight graph), then `kl_pi_isGreatest` with
   `M_i = max over finitely many vertex laws` — this would make item 3 hypothesis-free.
2. Lemma R6.3 and Theorem R6: with R6.2 machine-checked, what is missing is the hypergeometric
   tail bound and the assembly with L1's oracle model (`theorem4_adaptive_marginal_oracle`).
3. Corollary A11.2's sign statement via Mathlib's `fkg`, and the closed form
   `E_{h}|x|/n = 1/(1+e^{u})` on the uniform cube (the `½ tanh(u/2)` remark).

## 7. Requests

**To the theory division.**
(a) The abstract sandwich (`ScienceL2.sandwich_mean`, `mean_range_eq_Icc`, `ratio_range_eq_Icc`
in `experiments/science/ws_L2/Sandwich.lean`) depends only on Mathlib and on two inequalities
between the envelope and two functions.  If robust macrostate ratios are taken up in the theory
report, the file can be moved under `proofs/` as it is; it would answer THY-RES-0003 ("no closed
form for ratios") in the setting: finite distributive lattice, submodular known part, envelope
saturated by two admissible functions, lower set against upper set.
(b) `softMin_admissible` in `Window.lean` re-proves the closure of the class under soft minima
for a weight `π₁` and an envelope acting on the other coordinate; if the theory library's
`softmin_admissible` is stated for the uniform weight only, the weighted form is what the chain
rule needs.

**To the engineering division.**  None.

## Appendix: files

| file | lines | theorems | definitions | content |
|---|---|---|---|---|
| `Sandwich.lean` | 1 110 | 59 | 12 | A11: abstract lattice, convexity in the weights, cube, chains, witnesses |
| `Referee.lean` | 1 373 | 62 | 15 | R6.1; R5(2) abstract and binary cube; R6.2 abstract, binary cube, witness |
| `Window.lean` | 777 | 27 | 8 | A1.2 items 1–3, counterexample for the diagonal |
| `check_all.sh`, `check_log.txt` | | | | the check of the three files, one at a time |
| `sanity_numerics.py`, `sanity_numerics_output.txt` | 569 | | | §3 |
| `NOTES.md` | | | | chronological log |
