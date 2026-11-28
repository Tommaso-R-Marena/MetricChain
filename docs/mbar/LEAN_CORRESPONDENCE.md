# Division 9 — Lean formalisation: pins, audit, and correspondence with the paper statements

## 1. Project, pins, how to build

| | |
|---|---|
| location | `experiments/mbar/lean/` — a standalone Lake project (package `mbar`, library `MBAR`); nothing under the theory division's `proofs/` is touched and its audit is unaffected |
| Lean | `leanprover/lean4:v4.31.0` (`lean-toolchain`), commit `68218e876d2a38b1985b8590fff244a83c321783` |
| Mathlib | tag `v4.31.0`, revision `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (`lake-manifest.json`, copied from the repository root: the programme's pin) |
| sources | `MBAR/Allocation.lean` (610 lines), `MBAR/EValue.lean` (213), `MBAR/LowerBound.lean` (248), `MBAR/Localization.lean` (341), `MBAR/AxiomAudit.lean` (64), `MBAR.lean` (4) |
| build | `cd experiments/mbar/lean && lake exe cache get && ./audit.sh`  (on this machine `.lake/packages` is a link to the repository root's fetched packages) |
| logs | `experiments/mbar/lean/logs/build.log`, `logs/axioms.log` |

`audit.sh` does three things and fails if any does: (1) a scan of every source for `sorry`, `admit`,
`axiom`, native evaluation, `implemented_by`, `unsafe`, debugging tactics, `#guard_msgs` and anonymous
`example`s (the theory division's list); (2) `lake build MBAR` with no error and no warning; (3)
`#print axioms` for the 50 headline declarations, each of which must depend on `propext`,
`Classical.choice`, `Quot.sound` only.  **Result on 2026-11-28: AUDIT PASSED** — 50 declarations, 1476
lines in `MBAR/*.lean` (1480 with the four-line root file), no warning.  The internal referee read 11
declarations against this table and did not run the build.

## 2. What is and is not formalised

Everything is for **finite supports** (`Fintype` index sets, real arithmetic).  The formal `Model ι α`
is a family of probability vectors `p k : α → ℝ`.  Statements that involve probability are statements
about finite sums of products (`Model.prob`, `Model.stat`): expectation = sum against the product
weights.  Not formalised, and labelled [X] or [P] in `MATHEMATICS.md`:

* existence of a solution `v` of the Laplacian equation under connected overlap (the formal theorems
  take `v` as a hypothesis: `∀ k, s k * (v k − E_k z) = c k`);
* measure-theoretic generality (σ-finite base measures, `L²` spaces), the closed-orthant theorem A3,
  Sion's minimax theorem (A5), necessity in the equivalence theorem (A6 iii);
* Ville's inequality (B3), Pinsker's inequality and the chain rule for adaptively chosen states
  (C1, C2), the Hoeffding/Bernstein/Berry–Esseen inequalities of the handoff (B3–B5, C1–C3, G1);
* any statement about floating-point computation or about the Python code.

No imported concentration inequality is presented as machine-checked.

## 3. Correspondence

`M : Model ι α`; `M.E k h = Σ_x p k x · h x`; `M.Var k h`; `M.J s r = Σ_k E_k[r_k²]/s_k`;
`M.Feasible c r` = the affine set `F_c`; `M.ell c h = Σ_k c_k E_k h`; `M.Q s h = Σ_k s_k Var_k h`;
`M.D c s h = 2ℓ − Q`; `M.zfun s v`, `M.rstar s v` = `z`, `r*`; `M.V c s = sInf (J s '' F_c)`.

| paper statement (`MATHEMATICS.md`) | Lean declaration (`MBAR.`) | formal statement, in words |
|---|---|---|
| A1: `r*` feasible | `Model.rstar_feasible` | if `s > 0` and `v` solves the Laplacian equation then `r* ∈ F_c` |
| A1: orthogonality | `Model.pythagoras` | `J s r = J s r* + J s (r − r*)` for every feasible `r` |
| A1: minimiser | `Model.rstar_optimal`, `Model.V_eq_J_rstar` | `J s r* ≤ J s r`; the infimum `V c s` equals `J s r*` |
| A1: value | `Model.J_rstar`, `Model.J_rstar_formula`, `Model.V_eq_formula` | `J s r* = Σ s_k Var_k z = Σ c_k v_k − Σ c_k²/s_k` |
| A1: perspective | `Model.perspective_ineq`, `Model.J_convex` | joint convexity of `(s, r) ↦ J s r` on `s > 0` |
| A1: `F_c` convex, allocation-free | `Model.Feasible.combo` | convex combinations stay in `F_c` (the set has no `s` in its definition) |
| A1: convexity of `V` | `Model.V_convex`, `Model.V_convex_of_solutions` | `V c (λs + (1−λ)t) ≤ λ V c s + (1−λ) V c t` when the minima at `s`, `t` are attained (in particular when the Laplacian equation is solvable at both) |
| A2: weak duality | `Model.weak_duality` | `D c s h ≤ J s r` for all `h`, feasible `r` |
| A2: strong duality, maximiser | `Model.strong_duality`, `Model.zfun_maximises`, `Model.ell_zfun` | `D c s z = J s r*`; `D c s h ≤ D c s z`; `ℓ_c(z) = Q(s, z)` |
| A2/A4: information inequality | `Model.cs_form` | `ℓ_c(h)² ≤ Q(s, h) · J s r` |
| A4: superadditive precision | `Model.precision_superadditive` | for `s, t > 0`: `V(s+t)·(J s r + J t r′) ≤ J s r · J t r′` for feasible `r, r′` (with the minimisers: `1/V(s+t) ≥ 1/V(s) + 1/V(t)`); the closed orthant and general targets are paper proofs |
| A4/A8: monotone, homogeneous | `Model.J_anti`, `Model.J_smul` | `J t r ≤ J s r` if `s ≤ t`; `J (a·s) r = J s r / a` |
| A5: Cauchy–Schwarz step (E2) | `neyman_lower`, `neyman_attained` | `(Σ ra_k σ_k)² ≤ (Σ ra_k² s_k)(Σ σ_k²/s_k)`; equality data for `s_k = Bσ_k/(ra_k T)` |
| A6(i): efficiency bound | `Model.efficiency_bound` | for `s > 0`, `t > 0` (strictly) and a contrast: if `Var_k(z_s) ≤ G a_k` for all `k` and `Σ a_k t_k = B` then `V(s)² ≤ B·G·J t r` |
| A6(ii): sufficiency | `Model.equivalence_sufficient` | for `s > 0`, `t > 0`, `B > 0`: if `Var_k(z_s)/a_k ≤ V(s)/B` for all `k` then `V(s) ≤ J t r` for every `t` of cost `B`.  Designs on the boundary (zeros in `s` or `t`) are **not** covered by the formal statements |
| A8: rounding | `Model.rounding_bound` | `n ≥ ρ s` ⇒ `J n r ≤ J s r / ρ` |
| B1: independence | `Model.expect_stat` | `Σ_x prob(x) Π_k Π_i g_k(x_{k,i}) = Π_k (E_k g_k)^{n_k}` |
| B1: weighted AM–GM | `Model.prod_pow_le_one` | `Σ n_k b_k ≤ Σ n_k` ⇒ `Π b_k^{n_k} ≤ 1` |
| B1: e-value | `Model.stratified_evalue`, `Model.lr_family_evalue` | expectation `≤ 1` for the family `g_k = λ_k m_w/(s_k p_k)`, any predictor `λ ≥ 0` with `Σ_k λ_k ≤ 1`, any tilt `w ≥ 0` with `Σ w ≤ 1`, `Σ n_k > 0`.  The identity `E = exp(−N·KL(s‖a))` is not formalised |
| B2: fixed-sample coverage | `Model.markov_finite`, `Model.lr_region_coverage` | the probability that the statistic is `≥ 1/a` is `≤ a` |
| handoff B1: third moment | `Softmax.kappa_ge` | `κ₃ ≥ −ρ·Var` when `osc h ≤ ρ` (constant 1) |
| handoff B1: derivatives | `Softmax.hasDerivAt_m`, `Softmax.hasDerivAt_Vr` | tilted mean and variance have derivatives `Var`, `κ₃` |
| handoff B1: Hessian comparison | `Softmax.Vr_ge` | `Var_t ≥ e^{−ρt} Var_0` |
| handoff B1: integrated curvature | `Softmax.curvature_integrated`, `curvature_sum` | `m(1) − m(0) ≥ Var_0 (1 − e^{−ρ})/ρ`, summed over samples |
| handoff C1: cut norm | `pairing_le` | `|Σ y_i h_i| ≤ (ρ/2)Σ|y_i|` for zero-sum `y` |
| handoff C1: localisation | `cut_localization` | `ρ ≤ −log(1 − Rε)` from the three inequalities |
| handoff E3 | `free_energy_envelope`, `contrast_composition` | envelope `ε` ⇒ free energy within `ε`; radii add |
| handoff D1: least squares | `weighted_ls_identity`, `edge_energy_identity` | the divergence budget equals the Laplacian energy |
| handoff D1: χ² with private category | `chisq_categorical` | `Σ Δ²/w + (ΣΔ)²/(1−W) ≤ (Σ Δ²/w)/(1−W)` |
| handoff D1: exponential | `abs_exp_sub_one_le_mul_exp` | `|e^z − 1| ≤ |z|e^{|z|}` |
| handoff D1 / C1: `KL ≤ χ²` | `kl_le_chisq` | finite laws, reference law strictly positive, `0·log 0 = 0` |
| handoff D1: maximum principle | `max_principle`, `harmonic_extremes` | harmonic away from source and sink on a connected network ⇒ extremes at sink and source |
| C1, D1: two-point testing | `le_cam` | `P₀(A) + P₁(Aᶜ) ≥ 1 − TV` |
| C1: submodel | `Model.tilt_sum_one`, `Model.chisq_tilt`, `Model.chisq_budget` | the tilted law is normalised; its χ² is `t² Var_k h/(1 + tE_k h)²` |
| C1: separation | `log_one_add_le`, `log_one_add_ge` | `u − 2u² ≤ log(1+u) ≤ u` for `u ≥ −½` |
| C2: budget of information | `Model.Q_le_budget` | for every `h` with `Var_k h ≤ G a_k` and every allocation `t ≥ 0` (zeros allowed) of cost `B`: `Σ t_k Var_k h ≤ B·G` |

## 4. Reading the formal statements against the paper ones

* The formal `V c s` is an infimum over all real-valued tuples `r` on a finite support; the paper's
  `r_k ∈ L²(P_k)` is automatic there.  Values of `r_k` at points of probability zero do not enter `J`
  or `Feasible`.
* `Model.lrFactor` is defined to be `0` where `p_k(x) = 0` or `n_k = 0`; such points have probability
  zero under state `k`, and a state with `n_k = 0` contributes an empty product.
* `Softmax.S a h p t` takes arbitrary nonnegative weights `a_j`, not all zero: this covers states with
  `q_j(x) = 0` at the sample point.
* `le_cam` and `markov_finite` are stated with real-valued weights that sum to one; they are used with
  the product weights `Model.prob`.
