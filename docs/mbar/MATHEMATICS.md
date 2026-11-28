# Division 9 — mathematics of certified multistate free-energy estimation

*Written by the coordinating AI session of Division 9 (branch `research/phase2-certified-mbar`).
Status of every statement is given by a label: **[V]** machine-checked in Lean 4 for finite supports
(declaration named; file under `experiments/mbar/lean/MBAR/`), **[P]** paper proof given here,
**[K]** known (cited), **[X]** external theorem assumed with its statement, **[N]** numerical check
(script named), **[C]** conjecture or unproved claim.  Internal review: `docs/mbar/REVIEW_A.md`.
No statement here has been read by a human expert.  Prior art: `docs/mbar/PRIOR_ART.md`.*

The handoff package (`experiments/mbar/handoff/MBAR_strengthened/proofs/MAIN_RESULTS.md`) is cited as
"the handoff"; its labels A1, A2, B1–B5, C1–C3, D1, D2, E1–E3, G1, G2 are kept.  New statements of
this division are numbered A1–A13, B1–B8, C1–C4 **within this note** ("Theorem A5 of this note").
Where both carry the same label the text says which is meant.

## 0. Model, notation, and what is new

**Model.**  `(X, 𝒜)` measurable, `G` a σ-finite measure, `q_1, …, q_K ≥ 0` measurable with
`Z_k = ∫ q_k dG ∈ (0, ∞)`; `P_k` has density `p_k = q_k/Z_k` with respect to `G`; `f_k = −log Z_k`;
`E_k`, `Var_k` are taken under `P_k`.  Data: `n_k` independent draws from `P_k`, independent across
states ("stratified sampling"); `N = Σ n_k`, `s_k = n_k/N`.  For `s ∈ [0,∞)^K`: `m_s = Σ s_k p_k`,
`π_k = s_k p_k/m_s`, `L(s) = S − ∫ m_s ππᵀ dG` (the overlap Laplacian; `S = diag s`).  A *contrast* is
`c ∈ ℝ^K` with `Σ c_k = 0`; the estimand is `θ = cᵀf`.  For a function `h`:
`ℓ_c(h) = Σ_k c_k E_k h` and `Q(s, h) = Σ_k s_k Var_k(h)`.

**The statistical experiment.**  An estimator that uses a sample point `x` only through the vector of
energies `u(x) = (−log q_j(x))_j` sees, under state `k`, a draw from the law with density
`e^{−u_k}/Z_k` with respect to the image measure `Γ = G∘u^{−1}` on `ℝ^K`.  The unknown of the problem is
then `Γ` alone: this is Vardi's biased sampling model with known weights `e^{−u_k}` [K: Vardi 1985;
Gill–Vardi–Wellner 1988], and MBAR is its nonparametric maximum likelihood estimator.  All optimality
statements below are statements about this experiment (§C4).

**Summary of results.**

| | statement | status |
|---|---|---|
| handoff A1, A2, E2 | variance = minimum over an allocation-independent affine set; convex; gradient | **verified**; [V] finite support |
| A2–A4 (this note) | dual formula; closed orthant and unsampled states; a cancellation-free formula for any smooth functional; precision `1/V` concave and superadditive | [P]; [V] cores; [N] |
| A5–A8 | Elfving-type identity for the optimal budgeted allocation; equivalence theorem; certified efficiency bound of any allocation; monotone algorithm; rounding | [P]; [V] cores; [N] |
| A9–A10 | pilot-based allocation: deterministic safeguard; several targets | [P]; consistency of the two-stage estimator [C] |
| A11–A12 | correlated sampling: MBAR's variance is **not** convex in the allocation (counterexample); what remains true | [N] counterexample; [P] |
| handoff B1–B5, C1–C3, G1, G2, E1, E3 | audited: no error found; C1 and C2 are valid but far from sharp | §B0; [V] deterministic cores of B1, C1, E3 |
| B1–B3 | the reverse-logistic likelihood ratio is an e-value under stratified sampling; confidence region = sublevel set of the MBAR objective; valid at every sample size, at every round, under adaptive allocation | [P]; [V] fixed-sample finite support; Ville [X]; [N] |
| B5 | model check: a rejection certifies inconsistency with equilibrium sampling | [P]; [N] |
| B7 | what no certificate can do: consistent trapping; estimated mixing | [P]; [N] |
| handoff D1, D2 | D1 verified ([V] cores); D2 read, not reconstructed | §C0 |
| C1–C2 | finite-sample two-point bound `≍ √(V_c/N)` at every instance; adaptive allocation cannot beat the optimal static allocation | [P]; [V] cores; chain rule and Pinsker [X]; [N] |

---

# Part A — allocation (design) theory

## A1. The primal characterisation (handoff A1) — verified

**Theorem A1** [P; V].  Let `s ∈ (0,∞)^K` and assume connected overlap (`L(s)` has kernel `span 1`).
For a contrast `c` let `F_c` be the set of tuples `r = (r_k)`, `r_k ∈ L²(P_k)`, with `E_k r_k = 0` and
`Σ_k p_k r_k = −Σ_k c_k p_k` `G`-a.e.  `F_c` does not depend on `s`, and

    V_c(s) := cᵀL(s)^+c − Σ_k c_k²/s_k  =  min_{r ∈ F_c} Σ_k E_k[r_k²]/s_k ,

attained at `r*_k = s_k(E_k z − z)`, `z = Σ_k π_k v_k`, `v = L(s)^+c`.  Hence `V_c` is convex on the
open orthant.  `V_c(s)/N` at `s = n/N` is the asymptotic variance of MBAR.

*Proof.*  As in the handoff; re-derived independently.  `(Lv)_k = s_k(v_k − E_k z) = c_k`, so
`E_k z = v_k − c_k/s_k`.  Feasibility of `r*`: `E_k r*_k = 0`, and
`Σ_k p_k r*_k = Σ_k s_k p_k(v_k − c_k/s_k) − m_s z = −Σ_k c_k p_k`.  For feasible `r`, `d = r − r*`
satisfies `E_k d_k = 0`, `Σ_k p_k d_k = 0`, so `Σ_k E_k[r*_k d_k]/s_k = Σ_k E_k z·E_k d_k − ∫ z Σ_k p_k d_k dG = 0`
and `Σ_k E_k r_k²/s_k = Σ_k E_k r*_k²/s_k + Σ_k E_k d_k²/s_k`.  The value is `Σ_k s_k Var_k(z) = cᵀv − Σ c_k²/s_k`.
Convexity: `(r, s) ↦ Σ_k E_k r_k²/s_k` is jointly convex (perspective of the square) and `F_c` is a
convex set that does not move with `s`.  ∎

Lean (finite support): `Model.rstar_feasible`, `Model.pythagoras`, `Model.rstar_optimal`,
`Model.J_rstar_formula`, `Model.V_eq_J_rstar`, `Model.V_eq_formula`, `Model.perspective_ineq`,
`Model.J_convex`, `Model.V_convex`, `Model.V_convex_of_solutions`.  The hypothesis of these theorems is a
solution `v` of the Laplacian equation; its existence under connected overlap is linear algebra and is
not formalised.  Numerics: four independent routes to `V` agree to `3·10⁻¹²` on 400 random models
(`tests/test_population.py`), one of them a direct solve of the constrained least-squares problem
with no reference to `L`.

*What this is.*  `F_c` is, after the scaling `r_k = s_k φ_k`, the set of all influence functions
(gradients) of regular estimators in the biased sampling model, and `r*` is the efficient one; the
theorem is the statement that MBAR is efficient [K: Gill–Vardi–Wellner 1988] *plus* the observation
that in this scaling the set of gradients does not depend on the allocation.  For `K = 2` convexity
and the gradient formula are Hahn & Then 2009.

## A2. The dual characterisation and the gradient

**Theorem A2** [P; V].  Under the assumptions of A1, for bounded measurable `h`,

    V_c(s) = max_h { 2 ℓ_c(h) − Q(s, h) } = max_h ℓ_c(h)²/Q(s, h) ,

attained at `h = z` (unique up to an additive constant and `m_s`-null sets).  Consequently
`∂V_c/∂s_k = −Var_k(z)` (handoff A2) and `Σ_k s_k Var_k(z) = V_c(s)`.

*Proof.*  Weak duality: for `r ∈ F_c`, `ℓ_c(h) = ∫ h Σ_k c_k p_k = −Σ_k E_k[h r_k] = −Σ_k E_k[(h − E_k h) r_k]`,
and `−2ab ≤ s a² + b²/s` gives `2ℓ_c(h) − Q(s,h) ≤ Σ_k E_k r_k²/s_k`.  Equality at `h = z`, `r = r*`:
`ℓ_c(z) = Σ_k c_k E_k z = cᵀv − Σ c_k²/s_k`, and `Q(s, z) = V_c(s)` by A1.  The second form follows by
scaling `h`.  The gradient: `V_c` is a supremum of functions affine in `s`, differentiable by A1's
smoothness, so its gradient is that of the active affine function (envelope theorem); the handoff's
direct differentiation gives the same.  ∎

Lean: `Model.weak_duality`, `Model.strong_duality`, `Model.zfun_maximises`, `Model.ell_zfun`,
`Model.cs_form` (`ℓ_c(h)² ≤ Q(s,h)·Σ_k E_k r_k²/s_k`).  Numerics: gradient against finite differences,
relative error `2·10⁻⁸`.

The dual form makes convexity immediate (a supremum of affine functions) and is the semiparametric
information bound: `Q(s, h)` is the Fisher information of the one-dimensional submodel
`dG_t = (1 + t h) dG`, additive over independent samples, and `ℓ_c(h)` is the derivative of the
estimand along it (up to sign).

## A3. The closed orthant: unsampled states, general targets, a stable formula

Let `ν` be a finite signed measure with `ν(X) = 0`, `ℓ_ν(h) = ∫ h dν` (a contrast is `ν = Σ c_k P_k`;
the expectation `E_k[A]` is `ν = (A − E_k A) P_k`, whose derivative along `h` is `Cov_k(A, h)`).  For
`s ∈ [0,∞)^K∖{0}` define

    V_ν(s) := sup_h { 2 ℓ_ν(h) − Q(s, h) } ∈ [0, ∞],        A = {k : s_k > 0},  m = Σ_{k∈A} s_k p_k .

**Theorem A3** [P; N].
(a) `V_ν` is convex, lower semicontinuous, nonincreasing in every `s_k` and homogeneous of degree `−1`
on the closed orthant, and `V_ν(s) = lim_{t↓0} V_ν(s + t u)` for every `u` in the open orthant.
(b) `V_ν(s) < ∞` iff `ν ≪ m`, `ρ := dν/dm ∈ L²(m)`, and `ν(C) = 0` for the support `C` of every
connected component of the overlap graph of the sampled states.
(c) In that case, with `ρ̄_k = E_k ρ` (`k ∈ A`) and `L_A` the overlap Laplacian of the sampled states,

    V_ν(s) = ∫ ρ² dm + (Sρ̄)ᵀ L_A^+ (Sρ̄) ,     maximiser  h = ρ + Σ_{k∈A} π_k β_k ,  β = L_A^+ Sρ̄ .

Both terms are nonnegative: no cancellation.  For a contrast supported on sampled states this equals
`cᵀL^+c − Σ c_k²/s_k`.  For an unsampled state (`s_k = 0`) the value is finite iff the state is
covered by the sampled ones in the `χ²` sense of (b); this is MBAR with unsampled target states.

*Proof.*  (a) A supremum of functions that are affine, continuous and nonincreasing in `s`; degree `−1`
by the substitution `h → h/a`.  The radial limit is the continuity of a closed convex function along a
segment into the interior of its domain [K: Rockafellar, *Convex Analysis*, Cor. 7.5.1].
(b), (c) If `ν` charges a set where `m = 0`, or `ρ ∉ L²(m)`, take `h` concentrated accordingly: since
`Q(s,h) ≤ ∫h² dm`, the supremum is `≥ sup_h 2∫ρh dm − ∫h² dm = ∫ρ² dm`.  Otherwise write
`Q(s,h) = ⟨h, (I − T)h⟩_{L²(m)}` with `Th = Σ_{k∈A} π_k E_k h`, a self-adjoint Markov operator of finite
rank; `I − T` has closed range `(ker(I−T))^⊥`, and its kernel is the set of functions constant
`P_k`-a.s. for every `k ∈ A`, i.e. constant on component supports.  The supremum is finite iff
`ρ ⊥ ker(I − T)`, i.e. `ν(C) = 0`.  The maximiser solves `(I − T)h = ρ`, i.e. `h = ρ + Σ_k π_k E_k h`;
taking `E_j` gives `L_A β = Sρ̄` for `β_j = E_j h`, and `V = ∫ hρ dm = ∫ρ² dm + Σ_k s_k ρ̄_k β_k`.  The
reduction to the handoff formula is a direct substitution (`ρ = Σ_k (c_k/s_k)π_k`).  ∎

Numerics: `population.solve_dual` implements (c); it agrees with the `J × J` dual solve at exact
zeros and with the limit of the primal problem (`3·10⁻⁶`); single-state sampling gives `Var_k(A)` and
importance sampling from another state gives the delta-method variance of self-normalised importance
sampling.  **Numerical caveat (negative result N1, `DEAD_ENDS.md`):** the subtraction formula
`cᵀL^+c − Σ c_k²/s_k` loses all accuracy as `s_k → 0` (condition number `∼ 1/s_k`); optimal designs do
sit on the boundary (§A6), so (c) is the formula to use.

## A4. Precision is concave and superadditive

**Theorem A4** [P; V].  On `{0 < V_ν < ∞}`, `I_ν(s) := 1/V_ν(s) = inf { Q(s, h) : ℓ_ν(h) = 1 }`.  Hence
`I_ν` is concave, positively homogeneous of degree 1, nondecreasing, and superadditive:
`I_ν(s + t) ≥ I_ν(s) + I_ν(t)`.  In particular `V(γs + (1−γ)t) ≤ [γ/V(s) + (1−γ)/V(t)]^{−1}`.

*Proof.*  `V_ν = sup_h ℓ_ν(h)²/Q(s,h)` (A2/A3), so `1/V_ν` is an infimum of functions linear in `s`.  ∎

Lean: `Model.precision_superadditive` (multiplicative form
`V(s+t)·(V(s) + V(t)) ≤ V(s)·V(t)`), `Model.J_anti`, `Model.J_smul`.  Numerics: 600 random pairs, no
violation above `3·10⁻¹⁵`.  This is the classical concavity of the information for `cᵀθ` in design
theory [K: Pukelsheim], here for the information operator of the biased sampling model.  It is
strictly stronger than convexity of `V`: *the samples of two batches are worth at least the sum of
what each is worth alone.*

## A5. The optimal budgeted allocation: an Elfving-type identity

Costs `a_k > 0` per sample of state `k`, budget `B > 0`, `𝒮_B = {s ≥ 0 : Σ a_k s_k = B}`.

**Theorem A5** [P; N].

    V*_ν(B) := min_{s ∈ 𝒮_B} V_ν(s)
             = (1/B) · sup_h  ℓ_ν(h)² / max_k (Var_k(h)/a_k)
             = (1/B) · ( inf_{r ∈ F_ν} Σ_k √a_k ‖r_k‖_{L²(P_k)} )² ,

the last for contrasts (`F_ν = F_c`); the minimum is attained.

*Proof.*  `Φ(s, h) = 2ℓ_ν(h) − Q(s, h)` is linear and continuous in `s` on the compact convex set `𝒮_B`
and concave and sup-norm continuous in `h` on the convex set of bounded functions; by Sion's minimax
theorem [X] `min_s sup_h Φ = sup_h min_s Φ`, and `min_{s∈𝒮_B} Φ(s,h) = 2ℓ_ν(h) − B max_k Var_k(h)/a_k`;
scaling `h` gives the second expression.  The minimum over `s` is attained because `V_ν` is lower
semicontinuous (A3a).  Third expression: by A3(a) the minimum equals the infimum over `s > 0`; by A1,
`inf_{s>0} inf_r = inf_r inf_{s>0}`, and for fixed `r` Cauchy–Schwarz gives
`inf_{s>0, a·s=B} Σ_k ‖r_k‖²/s_k = (Σ_k √a_k‖r_k‖)²/B` (handoff E2).  ∎

Lean: `neyman_lower`, `neyman_attained` (the Cauchy–Schwarz step and its attainment);
`Model.efficiency_bound` (the inequality `≥` between the first two expressions).  Sion's theorem is
not formalised.  Numerics: the three expressions computed by three unrelated solvers (multiplicative
iteration; second-order cone programme for the group norm; cone programme for the dual) agree to
`2.4·10⁻⁷` on 40 random models with random costs.

This is the analogue of Elfving's theorem [K] for the biased sampling model: the optimal variance is
the square of a gauge of the target — the mixed `(1,2)` norm of its cheapest representation by
state-wise influence functions.  Gill–Vardi–Wellner posed the design question for this model
(Problem 6.1) and solved two examples; we did not find the general statement.

## A6. Equivalence theorem and a certified efficiency bound

**Theorem A6** [P; V for (i),(ii); N].  Let `V_ν(s) < ∞`, `h_s` its dual maximiser, and suppose `h_s` is
defined `P_k`-a.s. for every `k` (e.g. all states have the same support); `g_k = Var_k(h_s)`.
(i) *Efficiency bound.*  `V*_ν(B)/V_ν(s) ≥ [V_ν(s)/B] / max_k (g_k/a_k)` for every `s ∈ 𝒮_B`.
(ii) *Sufficiency.*  If `g_k/a_k ≤ V_ν(s)/B` for all `k`, then `s` is optimal in `𝒮_B`.
(iii) *Necessity (finite support).*  If `s` is optimal there is a dual maximiser `h` of `Φ(s,·)` with
`Var_k(h)/a_k ≤ V_ν(s)/B` for all `k`; equality holds wherever `s_k > 0`.
With lower bounds `s ≥ s^{lo}`: `V*/V(s) ≥ 2 − [g·s^{lo} + (B − a·s^{lo}) max_k g_k/a_k]/V(s)`.

*Proof.*  (i) Insert `h_s` in the second expression of A5: `ℓ_ν(h_s) = V_ν(s)`.  (ii) from (i).
(iii) In finite support the outer supremum of A5 is attained (the objective is invariant under
adding functions constant on the union of supports and coercive modulo those); with A5 this gives a saddle point `(s, h)`: `h` maximises `Φ(s,·)` and `s` minimises
`Φ(·,h)` over `𝒮_B`, which is the stated condition; equality on the support by Euler's identity
`Σ_k s_k g_k = V`.  The bound with lower bounds is convexity plus Euler:
`V(t) ≥ V(s) − g·(t − s) = 2V(s) − g·t`.  ∎

Lean: `Model.efficiency_bound`, `Model.equivalence_sufficient`.

(i) is a certificate computable at *any* allocation: **uniform allocation loses at most the factor
`mean_k g_k / max_k g_k`** (unit costs).  From pilot data it is an estimate, not a certificate.
Optimal designs are often on the boundary: in the benchmark system "costly ends"
(`results/allocation_benchmark.json`) the optimal design gives **no samples to the two end states
whose free-energy difference is the target** — they are reweighted from their cheap neighbours — and
none to the middle state.

## A7. Iterated Neyman allocation

**Proposition A7** [P].  For `s ∈ 𝒮_B` with `V(s) < ∞` let `s⁺_k ∝ s_k √(g_k(s)/a_k)`, normalised to
`𝒮_B`.  Then `V(s⁺) ≤ V(s)`, with equality iff `s⁺ = s`, and the fixed points are the points satisfying
the conditions of A6(ii) on their support.

*Proof.*  With `r = r*(s)`, `‖r_k‖² = s_k² g_k`.  For this fixed `r`, `s⁺` minimises `Σ_k ‖r_k‖²/s_k`
over `𝒮_B` (A5), so `V(s⁺) ≤ Σ_k ‖r_k‖²/s⁺_k ≤ Σ_k ‖r_k‖²/s_k = V(s)` (states with `r_k = 0` drop out;
the boundary case by A3a).  ∎

This is Fellman's multiplicative rule for c-optimality [K], obtained here as alternating minimisation
of the jointly convex function of A1.  `population.optimal_allocation` implements it with lower bounds
(water-filling), a floor that lets a coordinate return from zero, and stops on the certificate A6(i).
One step from the pilot allocation is the Neyman rule used for EMUS, whose influence functions do not
move with the allocation; for MBAR the iteration is needed.

## A8. Integer allocations

**Proposition A8** [P; V].  Let `s* ∈ 𝒮_B` be optimal and `B > Σ_k a_k`.  The counts
`n_k = ⌈s*_k (B − Σ a)/B⌉` cost at most `B` and satisfy
`V*(B) ≤ min_{n ∈ ℕ^K, a·n ≤ B} V(n) ≤ V(n) ≤ V*(B) · B/(B − Σ_k a_k)`.

*Proof.*  `a·n ≤ (B − Σa) + Σa`; `n ≥ s*(B − Σa)/B` coordinatewise; monotonicity and degree `−1`.  ∎
Lean: `Model.rounding_bound`.  With unit costs the loss is at most the factor `N/(N − K)`.

## A9. Pilot-based allocation: what is proved and what is not

Procedure (`estimators.pilot_allocation`): (1) a pilot with counts `n⁰`; (2) fit MBAR; the fitted
distributions `P̂_k` live on the pooled pilot points; (3) minimise the plug-in `V̂_ν(s) = V_ν(s; P̂)`
over `{s ≥ n⁰, a·s = B}`; (4) extra samples `= (1−γ)·(plug-in) + γ·(cost-uniform)`; (5) MBAR on all
samples.  At `s = n⁰` the plug-in variance is the usual MBAR variance estimate (it reproduces PyMBAR's
standard errors to 13 digits).

**Proposition A9 (safeguard)** [P].  Whatever the pilot data, the real-valued allocation
`n = n⁰ + (1−γ)·plug-in + γ·u` satisfies `V_ν(n) ≤ V_ν(n⁰ + u)/γ`, where `u` is the naive split of the
whole remaining budget that the plug-in part is mixed with (equal counts, or equal cost per state):
`n ≥ γ(n⁰ + u)` coordinatewise because the plug-in part is nonnegative, and monotonicity and
homogeneity apply; A4 gives the sharper harmonic bound.  The integer counts returned by the code are
at least the floors of these numbers, `n_k ≥ n⁰_k + extra_k − 1`, so the bound holds for them exactly
whenever every pilot count satisfies `(1−γ)n⁰_k ≥ 1` (two samples per state for `γ = ¼`), and can
fail for pilots with a state sampled once or not at all (the referee's enumeration: `REVIEW_A.md`).

Not proved here [C]: that the two-stage estimator is asymptotically normal with variance
`V_ν(s°)/N` when the plug-in allocation converges to an optimal `s°`.  It is the standard conclusion
for sequential designs with independent streams (an Anscombe-type argument), and the benchmark is
consistent with it, but no proof is given, and nothing is claimed about small pilots: with few pilot
samples in weak overlap the plug-in sees no overlap and the procedure falls back to uniform.

## A10. Several targets

For targets `ν_1, …, ν_M`: `Σ_i w_i V_{ν_i}` (`w ≥ 0`) and `max_i V_{ν_i}` are convex in `s` (A3a).  For
the sum the analogue of A6 holds with `g_k = Σ_i w_i Var_k(h_{s,i})` (same proof; `Σ_i w_i V_{ν_i}` is
again a supremum of affine functions, over tuples `(h_i)`).  For the maximum,
`min_s max_i V_{ν_i}(s) = max_{w ∈ Δ} min_s Σ_i w_i V_{ν_i}(s)` [Sion, X].  Implemented (`objective="sum"`,
`"max"`); the max criterion by a damped subgradient iteration without a certificate.

## A11. Correlated sampling: convexity fails for MBAR

Let state `k` be sampled by a stationary Markov chain with invariant law `P_k`, and let
`Γ_k(r) = Var_k(r) + 2Σ_{t≥1} Cov(r(X_0), r(X_t))` be the long-run variance.  MBAR with weights `n_k` is
asymptotically linear with the same influence functions as in the independent case [K: Li et al.
2023], so `N·Var → V^{corr}_c(s) = Σ_k Γ_k(r*_k(s))/s_k`.

**Counterexample A11** [N].  `V^{corr}_c` need not be convex in `s`.  With reversible chains on 4–7
points whose mixing differs between states, 768 of 3000 random segments violate midpoint-type
convexity, the worst by 35 % (`bench/check_lower_bounds_and_chains.py`; the worst instance is stored in
`results/lower_bounds_and_chains.json` with its transition matrices).  The reason is visible in A1:
MBAR minimises `Σ_k Var_k(r_k)/s_k`, not `Σ_k Γ_k(r_k)/s_k`; it is the wrong minimiser for the
correlated objective and the perspective argument does not apply to it.

## A12. Correlated sampling: what remains true

**Proposition A12** [P; N].
(a) *Optimally weighted value.*  `W_c(s) := min_{r∈F_c} Σ_k Γ_k(r_k)/s_k` is convex in `s`, satisfies
`W_c ≤ V^{corr}_c`, and A5–A8 hold for it with `‖r_k‖² := Γ_k(r_k)` (the proofs use only that the
state-wise forms are nonnegative quadratic forms).  It is the variance bound for estimators that are
asymptotically linear with influence functions in `F_c`; an estimator attaining it would need the
operators `Γ_k`, and none is proposed here.
(b) *Scalar inefficiency.*  If `Γ_k = g_k Var_k` on the relevant functions, MBAR applied with weights
`n_k/g_k` (the standard practice of subsampling by the statistical inefficiency) has variance
`V_c(s_1/g_1, …, s_K/g_K)`: convex in `s`, and the whole of part A applies with costs `a_k g_k`.
(c) *Worst case under a certified contraction.*  If `‖P_k‖_{L²_0(P_k)} ≤ ρ_k` for reversible kernels,
then `Γ_k ≤ C_k Var_k`, `C_k = (1+ρ_k)/(1−ρ_k)`, with equality for every function when the kernel is
`ρ_k I + (1−ρ_k)Π_k`.  So `sup_{kernels} V^{corr}` of MBAR with weights `n_k/C_k` is `V_c(s/C)`, attained
simultaneously for all `s` by one family of kernels; the allocation that minimises the worst case is
the cost-aware optimal allocation with costs `a_k C_k`.

*Proof.*  (a) as in A1.  (b) the weights `s_k/g_k` make `r*(s/g)` the minimiser of
`Σ_k g_k Var_k(r_k)/s_k`.  (c) spectral calculus: `Γ_k(r) = ⟨r, (I+P_k)(I−P_k)^{−1} r⟩ ≤ C_k‖r‖²` for
centred `r`, and the lazy independence kernel has the single nontrivial eigenvalue `ρ_k`.  ∎
Numerics: (a) no convexity defect and `W ≤ V^{corr}` on 3000 segments; (b) identity to `10⁻¹⁵`.

The contraction `ρ_k` must be *known*; an estimated integrated autocorrelation time is not a bound
(§B7 and experiment C of `VALIDATION.md`).

## A13. Relation to known theory

A1–A8 are the c-optimal design theory (Elfving, Kiefer–Wolfowitz, Fellman, Pukelsheim) carried to the
information operator of the biased sampling model, which is linear in the sampling fractions
(Gill–Vardi–Wellner 1988).  For two states everything is in Bennett 1976 and Hahn & Then 2009.  What
this note adds is the multistate statement in a form that can be computed and checked: the
allocation-independent feasible set, the closed-orthant formula covering unsampled states and
expectations, the Elfving identity with costs, the certificate A6(i), the failure of convexity under
correlated sampling, and machine-checked finite-support cores.

---

# Part B — finite-sample certificates

## B0. Audit of the handoff's B, C, G, E statements

Each statement was re-derived line by line; constants were recomputed; C1, C2 were run.

| handoff | verdict | remarks |
|---|---|---|
| B1 (deterministic localisation) | **correct** | the third-derivative bound, the Hessian comparison and the localisation were re-derived.  [V]: `Softmax.kappa_ge` (third moment `≥ −osc·variance`, constant 1), `Softmax.Vr_ge`, `Softmax.curvature_integrated`, `curvature_sum`, `cut_localization` |
| B2 (score covariance) | **correct** | `Σ = L − LS^{−1}L`; `d = (K−1) − tr(S^{−1}L)`; the bounds `√R/N` and `R/4` |
| B3 (global bound) | **correct** given [X] | matrix Chernoff lower tail at `ε = ½`: exponent `0.6137·N/R ≥ N/(2R)`; rectangular Bernstein with dimension factor `K`, variance `d/N`; `δ ≤ 1/√6 + 1/12 < ½`; coefficient `4 log 2`.  External: Tropp 2012, Thms 1.1, 1.6 |
| B4 (contrast-sharp bound) | **correct** given [X] | failure budget `α/3 + α/6 + α/3`; `κ` dominates both sides of the inverse perturbation.  Needs the population `R`, `d`, `V_c`: an analysis bound, not a certificate |
| B5 (normal approximation) | **correct** given [X] | Berry–Esseen constant 0.56 for non-identically distributed summands (Shevtsova) |
| C1 (cut-score certificate) | **valid; not sharp** | radius `≈ R_max·√((K log 2 + log 1/α)/(2N))`: it scales like `R/√N`, while the truth is `√(R/N)` (C1 of this note, B2 of this note).  In our benchmark it abstains in 4 of 11 regimes and is 1.4–5.8 times wider than the region of B2 elsewhere |
| C2 (bridge intervals + closure) | **valid; conservative** | the identity `E_i w_j/E_j w_i = e^{a_j − a_i}Z_j/Z_i` and the KL-Chernoff interval were re-derived.  2.4–8.3 times wider than B2 in the benchmark: union bound over `4|E|` tails and path sums that ignore cycles |
| C3 (anytime extension) | **valid** | union bound over prefixes; superseded by B3 of this note |
| G1 (stationary chains, known contraction) | **correct** given [X] | the second-moment argument is elementary; the exponential version uses Fan–Jiang–Sun 2021.  Assumes a *known* contraction |
| G2 (bounded observables) | **correct** | implemented here with the region of B2 in place of C1 (`certificates.observable_interval`) |
| E1 (existence criterion) | **correct; known** | Vardi 1985.  Used by the code to abstain |
| E2 (group norm) | **correct** | Theorem A5 of this note |
| E3 (envelope composition) | **correct** | [V]: `free_energy_envelope`, `contrast_composition` |

No mathematical error was found in the handoff's v2 note.  Its limitation is the one it states: B3–B5
need population quantities, and its two observable certificates are far from the right rate.

## B1. The stratified likelihood-ratio e-value

**Theorem B1** [P; V].  Let `λ : X → [0,1]^K` be measurable with `Σ_k λ_k ≤ 1` (a *label predictor*) and
`w ∈ [0,1]^K` with `Σ_k w_k ≤ 1` (a *tilt*), both independent of the sample, `m_w = Σ_j w_j p_j`.  Under
stratified sampling with `s_k = n_k/N`,

    𝔼 [ Π_k Π_{i ≤ n_k}  λ_k(X_{k,i}) · m_w(X_{k,i}) / (s_k p_k(X_{k,i})) ]  ≤  1 .

For `λ = π(f′; ·)` (any fixed `f′`) and `w = s` the statistic is the reverse-logistic likelihood ratio
`Π_n π_{y_n}(f′; x_n)/π_{y_n}(f*; x_n)`, `π_k(f; x) = s_k e^{f_k}q_k(x)/Σ_j s_j e^{f_j}q_j(x)`, and its
expectation is exactly `exp(−N·KL(s‖a))`, `a_k = E_{m_s}[π_k(f′)]`.

*Proof.*  By independence the expectation is `Π_k b_k^{n_k}` with
`b_k = E_k[λ_k m_w/(s_k p_k)] ≤ s_k^{−1}∫ λ_k m_w dG`.  Then `Σ_k s_k b_k ≤ ∫ (Σ_k λ_k) m_w dG ≤ Σ_j w_j ≤ 1`, and by
the weighted inequality of arithmetic and geometric means `Π_k b_k^{n_k} = (Π_k b_k^{s_k})^N ≤ (Σ_k s_k b_k)^N ≤ 1`.
In the special case `b_k = a_k/s_k` with `Σ a_k = 1`.  ∎

Lean (finite support): `Model.expect_stat`, `Model.prod_pow_le_one`, `Model.stratified_evalue`,
`Model.lr_family_evalue`.  Numerics: exact enumeration of all samples on 286 small models
(`E ≤ 0.9999998` for arbitrary predictors and tilts; the identity to `3·10⁻¹⁵`).

*Remarks.*  With random labels (mixture sampling) the likelihood ratio is an ordinary conditional
likelihood ratio and the statement is universal inference [K: Wasserman–Ramdas–Balakrishnan 2020].
Under stratified sampling the individual factors are **not** e-values (`E_k = a_k/s_k` can exceed 1);
only the product over a batch whose composition equals the weights used in `π` is, and the slack
`exp(−N·KL(s‖a))` is exactly the gap between the retrospective Fisher information `L` and the
efficient information `(L^+ − S^{−1})^+` (§B4).  No moment or boundedness condition on the energies is
used: the factors are ratios of mixture densities.

## B2. The likelihood-ratio confidence region

Split the sample, by index only, into batches `b = 1, …, T` with counts `n^b` and proportions `β^b`.
For batch `b` let `f′_b` be any estimate computed from batches `< b`, and

    Φ_b(f) = Σ_{n ∈ b} [ log Σ_j β^b_j e^{f_j} q_j(x_n) − f_{y_n} ] .

**Theorem B2** [P; V for one batch and fixed `f′`, finite support].  For any set `E` of batches,

    C = { f :  Σ_{b∈E} Φ_b(f)  ≤  log(1/α) + Σ_{b∈E} Φ_b(f′_b) }

satisfies `P(f* ∈ C) ≥ 1 − α` at every sample size, for every `K`, with no condition on the energies.
`C` is convex and invariant under `f → f + const`; for every contrast, `[inf_C cᵀf, sup_C cᵀf]` is a
confidence interval, simultaneously over all contrasts.  `C` is bounded modulo constants iff the
directed support graph of the evaluated samples (handoff E1) is strongly connected; otherwise some
intervals are infinite.

*Proof.*  `exp(Φ_b(f*) − Φ_b(f′_b)) = Π_{n∈b} π^{β^b}_{y_n}(f′_b)/π^{β^b}_{y_n}(f*)` (the terms `log β_y q_y(x)` cancel).
Conditionally on the earlier batches this is the statistic of B1 with `s = β^b`, so its conditional
expectation is `≤ 1`; by the tower property the product over `b ∈ E` has expectation `≤ 1`, and Markov's
inequality gives `P(Σ_b[Φ_b(f*) − Φ_b(f′_b)] > log(1/α)) ≤ α`.  Convexity: each `Φ_b` is a sum of
log-sum-exp functions minus a linear function.  Boundedness: the recession function of `Σ_bΦ_b` is
`h ↦ Σ_n [max_{j: q_j(x_n)>0} h_j − h_{y_n}]`, which vanishes on a nonconstant `h` iff the graph is not
strongly connected.  ∎

Lean: `Model.markov_finite`, `Model.lr_region_coverage`.  Implementation: `certificates.lr_confidence_region`
(default: 8 batches, the first used only for training); the interval of a contrast is obtained from
the convex profile `θ ↦ min_{cᵀf = θ} ΣΦ_b(f)` by root finding, with the endpoint moved outward by the
tolerance.  Two points of the implementation are part of its validity: a profile value from an
unconverged inner minimisation is an *upper* bound of the true minimum and would shrink the interval,
so such a point is counted as inside the region; and a batch is left out only for a reason that
depends on *earlier* batches (its plug-in cannot be computed) — if the plug-in gives probability zero
to an observed label of the batch itself, the batch's e-value is 0 and the code abstains.  Floating
point is not certified.

**Proposition B2′ (restriction to a sub-ladder)** [P].  Let `S` be a set of states chosen without
reference to the samples.  The samples of the states of `S`, with the energies of those states only,
form a multistate experiment of the same kind, so Theorem B2 applied to it gives a region for
`(f_k)_{k∈S}` with `|S| − 1` nuisance directions instead of `K − 1`.  For `m` candidate sets used at
levels `α_1 + … + α_m ≤ α`, the intersection of the resulting intervals of a contrast is valid at level
`α`.  (`certificates.restricted_interval`.)  The restriction discards the samples of the other states;
it pays when the contrast is local (adjacent states of a long ladder) and not otherwise (§B8, O3).

*Size.*  With `f̂` the minimiser of `Φ = Σ_bΦ_b` and `H` its Hessian there, the region is to second order
the ellipsoid `(f − f̂)ᵀH(f − f̂) ≤ 2(log(1/α) + ρ)`, `ρ = Σ_bΦ_b(f′_b) − Φ(f̂)` (the "regret" of the
plug-ins; typically of order `(K−1)` times a logarithmic factor; it can be negative).  The half-width
for a contrast is `≈ √(2(log(1/α) + ρ)·cᵀH^+c)`, and `N_E·cᵀH^+c` is the *observed* effective resistance
of the contrast.  So the interval has the rate `√(R_c/N)` of the lower bound (C1), uses the full
Laplacian (cycles included, no path sums), and is contrast-specific.  Measured
(`results/certificates_coverage.json`, 11 regimes × 200 repetitions): coverage 100 %, always finite,
width 2.0–3.1 times the width of the asymptotic interval `±1.96·se`, and 1.4–8.3 times narrower than
C1 and C2 of the handoff where those are finite.

## B3. Every round, any stopping rule, adaptive allocation

**Theorem B3** [P; Ville's inequality X].  Let sampling proceed in rounds `b = 1, 2, …`; the counts
`n^b` of round `b` and the plug-in `f′_b` may depend on all earlier rounds; given them, the samples of
round `b` are independent draws from the chosen states.  Then `Λ_t = exp(Σ_{b≤t}[Φ_b(f*) − Φ_b(f′_b)])` is a
nonnegative supermartingale with `Λ_0 = 1`, and

    P( f* ∈ C_t for every t ) ≥ 1 − α ,      C_t = { f : Σ_{b≤t} Φ_b(f) ≤ log(1/α) + Σ_{b≤t} Φ_b(f′_b) } .

Hence the region may be recomputed after every round, the allocation of the next round may be chosen
from it, sampling may halt at any data-dependent time, and `∩_{u≤t} C_u` is also valid.

*Proof.*  B1 applied conditionally to round `b` with `s = β^b`; Ville's inequality for nonnegative
supermartingales.  ∎

A round consisting of a single state contributes the factor 1 (its likelihood ratio is identically
1): information comes from *comparing* states within a round, so adaptive rounds must be mixed.
Measured (`results/robustness.json`, experiment A): see `VALIDATION.md`.

## B4. How much is lost, and how to recover it (analysis; not a theorem)

To second order `log Λ(f) ≈ −N g(f*)ᵀδ − (N/2)δᵀLδ` with `δ = f′ − f*`; the score has covariance
`Σ/N`, `Σ = L − LS^{−1}L`, so `𝔼Λ ≈ exp(−(N/2)δᵀLS^{−1}Lδ)`: the region is built on the metric `L` although
the estimator's precision is `(L^+ − S^{−1})^+ ≽ L`.  The loss in squared width is `R_c/V_c`,
`R_c = cᵀL^+c = V_c + Σ c_k²/s_k`: negligible when overlap is weak (the handoff's D1 shows `V_c ≥ 3R_c/4`
in its class) and noticeable when overlap is strong.  In the benchmark models `√(R_c/V_c)` is 1.02 and
1.07 in the two weak-overlap families, 1.31 for the five-state harmonic ladder, and 1.88–1.90 for the
strongly overlapping four-state model and the two-state model; the remaining factor of about 1.4–2.4
between the certified and the asymptotic width is the threshold `2(log(1/α) + ρ)` against `1.96²`.
These are end-to-end contrasts.  For a contrast between *adjacent* states of a ladder `V_c` is small
and the loss is larger: `√(R_c/V_c)` is 3.0 for the first step of the five-state ladder and 4.1 for
the ten-state ladder (computed by the referee) — the restriction B2′ and the tilt address exactly
this case.  The tilt `w` of B1 recovers it: choosing, for each candidate `f`, the tilt
`w(f) ∝ s∘exp(ε)`, `ε = −(S − L)^{−1}L(f′ − f)`, makes the e-value exact to second order with the
efficient information.  Any pilot-measurable choice `f ↦ w(f)` keeps B2 valid, but the region is then
no longer a convex sublevel set; this refinement is **not implemented** (open problem O2).

## B5. A model check

**Theorem B5** [P].  In the setting of B3 let `λ^b` be label predictors computed from rounds `< b` (they
may use any features of `x`).  Under the model (independent equilibrium samples of every state),

    P( ∃ t :  min_f Σ_{b≤t} Σ_{n∈b} [−log π^{β^b}_{y_n}(f; x_n)]  −  Σ_{b≤t} Σ_{n∈b} [−log λ^b_{y_n}(x_n)]  ≥  log(1/α) ) ≤ α .

In words: *no label predictor trained on the past can beat, by more than `log(1/α)` nats of log-loss,
the best MBAR classifier chosen in hindsight*.  A violation is a finite-sample-valid rejection of
"the samples are independent draws from densities proportional to the stated `q_k` on a common base".

*Proof.*  The left side is `min_f log Π λ/π(f) ≤ log Π λ/π(f*)`, the logarithm of the supermartingale of
B1/B3 with `w = β^b`.  ∎

Implementation: `certificates.classifier_evalue`.  It detects samplers that disagree *with each other*
through their overlap (one state trapped in a basin that its neighbours visit); it has no power
against failures that are consistent across states (B7).

## B6. Observables

For `A : X → [0,1]` and a sampled state `k`, handoff G2 with the region of B2: `y(f) = N^{−1}Σ_n π_k(f;x_n)A(x_n)`
has mean `s_k E_k A` at `f*` (independent bounded summands: KL-Chernoff interval), and
`y(f*)/y(f₀) ∈ [e^{−r}, e^{r}]` for `r = sup_{f∈C} osc(f − f₀)`.  The interval has failure probability
`≤ α + α_o` (`certificates.observable_interval`; [P]).  Unbounded observables and unsampled target
states with unbounded importance ratios are not covered and cannot be without further assumptions.

## B7. What cannot be certified from the samples

**Proposition B7** [P].  (a) *Consistent trapping.*  If every state is sampled from `P_k(· | B)` for one
set `B`, the data have exactly the law of equilibrium sampling for the system `(q_k 1_B)`, whose
contrast is `cᵀf − Σ_k c_k log P_k(B)`.  A procedure that is valid for all systems therefore reports,
with probability `≥ 1 − α`, an interval containing the restricted contrast; it misses the true one
whenever it is shorter than `|Σ_k c_k log P_k(B)|`.  No test of any kind distinguishes the two.
(b) *Consequence.*  A certificate for the true system requires an a priori bound on the missing
masses `P_k(B^c)` — a certified envelope in the sense of handoff E3, obtained from outside the samples.
(c) *Dependent samples.*  If the sequence of each state is stationary and β-mixing and every `g`-th
sample is retained, any event has probability within `Σ_k (n′_k − 1) β_k(g)` of its probability under
independent sampling [K: Eberlein; Yu 1994, Lemma 4.1]; so a certificate valid at level `α` for
independent samples is valid at level `α + Σ_k(n′_k − 1)β_k(g)` on the thinned sample.  The
coefficients `β_k` are an assumption; a statistical inefficiency estimated from the same trajectory
is not a bound on them.

Measured (experiments B, C in `VALIDATION.md`): with one trapped state the region of B2 and the
asymptotic interval both exclude the truth in every repetition, and B5 rejects in all repetitions at
1000 samples per state; with all states trapped nothing rejects.

## B8. Open problems of part B

O1.  A certified statement for Markov-chain samples under a contraction assumption that keeps the
`√(R/N)` rate (the e-value of B1 needs a moment-generating-function bound for the tilted transition
operator).  O2.  The tilted, efficient region of B4 with a tractable computation.  O3.  A
variance-sensitive interval for one contrast whose threshold does not grow with `K` (the regret `ρ` of
B2 is the price of estimating `K − 1` nuisance directions).  O4.  Certified floating point for the
profile computation.

---

# Part C — information limits

## C0. Audit of handoff D1, D2

D1 was re-derived in full: the region construction, `Z′_k = e^{θ_k}`, the categorical laws, the χ² bound
with the private category, `|e^z − 1| ≤ e^{1/2}|z|`, the least-squares identity, the maximum principle,
`KL ≤ 1/16`, Pinsker and Le Cam.  **Correct.**  [V]: `weighted_ls_identity`, `edge_energy_identity`,
`chisq_categorical`, `abs_exp_sub_one_le_mul_exp`, `kl_le_chisq`, `max_principle`, `harmonic_extremes`,
`le_cam`; Pinsker is [X].  D2 (randomised coordinates) was read; the coupling argument is sound as
far as it goes, but it was **not reconstructed in detail** and its limiting statements are not checked.
D1 is a bound on one hard family with indicator densities; Theorem C1 below replaces `R_c` by `V_c`
and the family by a neighbourhood of an arbitrary instance.

## C1. A finite-sample bound at every instance

**Theorem C1** [P; V cores; N].  Let `s > 0`, `n = Ns`, connected overlap, `V = V_c(s) > 0`, `h` the dual
maximiser (A2) and `D = sup h − inf h`.  Let `τ ∈ (0,1]` and
`N ≥ N₀ := max( 4τ²D²/V , τ²‖c‖₁²D⁴/V³ )`.  Put `t = τ/√(NV)` and `dG_t = (1 + t(h − h̄)) dG`, `h̄` the
midrange of `h`.  Then `G_t` is a positive measure with `dG_t/dG ∈ [¾, 5/4]`, the functions `q_k` are
the same for `G` and `G_t`, and for every estimator `θ̂` of `cᵀf` (any measurable function of the
stratified sample; it may know the `q_k` and the pair `{G, G_t}`)

    max_{G′ ∈ {G, G_t}}  P_{G′} ( |θ̂ − cᵀf(G′)| ≥ (τ/4)√(V/N) )  ≥  ½ (1 − (2√2/3)τ) .

For `τ = ½`: an error of at least `⅛√(V_c/N)` with probability at least 0.26.  For a pair contrast
`D ≤ R_c`, so in the weak-overlap regime `N₀ = O(R_c)`.

*Proof.*  `Z_k(t) = Z_k(1 + u_k)`, `u_k = t(E_k h − h̄)`, `|u_k| ≤ tD/2 ≤ ¼`.  The contrast moves by
`−Σ_k c_k log(1 + u_k) = −tV + Σ_k c_k(u_k − log(1+u_k))` (using `Σ c_k = 0`, `ℓ_c(h) = V`), and
`0 ≤ u − log(1+u) ≤ 2u²` on `u ≥ −½`, so the separation is at least `tV − ‖c‖₁t²D²/2 ≥ tV/2`.  The state
laws are `p_{k,t} = p_k(1 + t(h − h̄))/(1 + u_k)`, and
`χ²(p_{k,t}‖p_k) = t²Var_k(h)/(1 + u_k)² ≤ (16/9)t²Var_k(h)`, so
`KL(P_t‖P_0) ≤ Σ_k n_k χ²_k ≤ (16/9)Nt²Q(s,h) = (16/9)τ²` since `Q(s,h) = V`.  Pinsker [X] and Le Cam's
two-point inequality.  ∎

Lean: `Model.tilt_sum_one`, `Model.chisq_tilt`, `Model.chisq_budget`, `log_one_add_le`,
`log_one_add_ge`, `kl_le_chisq`, `le_cam`, `Model.ell_zfun`.  Numerics
(`bench/check_lower_bounds_and_chains.py`): on 300 random models the exact divergence is at most
`0.31·(16/9)τ²` and the exact separation is within 5 % of `τ√(V/N)`.

This is the finite-sample form of the local asymptotic minimax bound of the biased sampling model
[K: Gill–Vardi–Wellner 1988 state the convolution theorem and note that the minimax statement
follows].  It is *local*: the two instances are at distance `O(N^{−1/2})`.  It does not answer the
question, left open in Micaletto 2026, of a minimax bound over all estimators uniformly over a
*fixed* class of pairs of distributions.

## C2. Adaptive allocation cannot beat the optimal static allocation

A *strategy* chooses the state of each draw from the earlier draws and internal randomness, with
total cost `Σ_t a_{k_t} ≤ B` almost surely, and then outputs an estimate.

**Theorem C2** [P; chain rule X; N].  Let `V*(B) = min{V_c(n) : n ≥ 0, a·n ≤ B}` (A5; counts, not
fractions).  Let `h°` be bounded with `ℓ_c(h°)²/max_k(Var_k(h°)/a_k) ≥ (1−η)·B·V*(B)` (exists for every
`η > 0`; `η = 0` in finite support), `M° = max_k Var_k(h°)/a_k`, `D° = osc h°`, `τ ∈ (0,1]`,
`t = τ/√(BM°)`, and assume `tD° ≤ ½` and `t ≤ |ℓ_c(h°)|/(‖c‖₁D°²)`.  Then for every strategy and
estimator

    max_{G′ ∈ {G, G_t}}  P_{G′} ( |θ̂ − cᵀf(G′)| ≥ (τ/4)√((1−η)V*(B)) )  ≥  ½ (1 − (2√2/3)τ) .

*Proof.*  For adaptively chosen states the divergence between the laws of the whole transcript is
`Σ_k 𝔼_0[N_k]·KL(p_k‖p_{k,t})` [X: the chain rule; e.g. Lattimore & Szepesvári, Lemma 15.1].  As in
C1, `KL(p_k‖p_{k,t}) ≤ χ²(p_k‖p_{k,t}) = E_k[(tH − u_k)²/((1+u_k)(1+tH))] ≤ (16/9)t²Var_k(h°)` with
`H = h° − h̄`.  Hence the divergence is at most
`(16/9)t² M° Σ_k a_k𝔼_0[N_k] ≤ (16/9)t² M° B = (16/9)τ²` — **for every strategy**, because `h°` is the
least-favourable direction of the *design problem*: it has small variance, relative to cost, in every
state simultaneously.  Separation `≥ t|ℓ_c(h°)|/2 = (τ/2)|ℓ_c(h°)|/√(BM°) ≥ (τ/2)√((1−η)V*(B))`.  ∎

Lean: the inequality `Σ_k n_k Var_k(h) ≤ B·G` for every allocation of cost `B` is inside
`Model.efficiency_bound`.  Numerics: over random allocations the accumulated information never
exceeds `B·M°` (ratio `≤ 1.000000`).

So adaptivity in the choice of states is worth nothing beyond learning the static optimum: in this
experiment "adaptive = oracle design" at the level of the leading constant.  The same conclusion is
known for adaptive treatment assignment [K: Armstrong 2022] and for active estimation in bandit
models; we did not find it for the biased sampling model.

## C3. Upper bounds that match

The handoff's B4 has leading term `√(2V_c log(6M/α)/N)`: with C1, the rate `√(V_c/N)` is the finite-sample
minimax rate at every instance once `N/R ≳ d·log K` (B4's threshold).  The region of B2 is observable
and has the rate `√(R_c/N)`; `R_c/V_c → 1` in weak overlap.  Not settled: the constant in the certified
interval (ratio 2–3 to the asymptotic interval), the regime `N ≲ R_c` (both bounds degenerate; D1's
saturation), and growing `K` (the regret term of B2 and the dimension term of B4 grow with `K`; C1
does not see `K`).

## C4. What the limits are limits of

1. *Evaluation-oracle (biased sampling) experiment.*  C1, C2 and D1 hold for estimators that are
   functions of the sample; the two instances share the energy functions and differ in the base
   measure by a density in `[¾, 5/4]`.  Knowing the energy functions analytically does not help;
   what would help is knowing the base measure.
2. *Unrestricted access.*  In molecular simulation the base measure is Lebesgue measure and is known.
   An algorithm allowed to evaluate the energies at points of its choice is outside the experiment:
   in low dimension quadrature computes `Z_k` without any sample.  The limits above are therefore
   limits of *estimation from equilibrium samples*, not of computation.
3. *Query complexity of MetricChain.*  There the algorithm chooses evaluation points and no sampler is
   given; the costs are exponential in the number of sites and adaptivity changes the exponent.  Here
   samplers are given and adaptivity changes nothing at leading order.  The two statements are about
   different experiments; `docs/mbar/SYNTHESIS.md` states what connects them.

---

# Status of the remaining handoff items

E1 known; E2 = Theorem A5; E3 machine-checked.  The handoff's benchmark of allocation used population
variances at the true distributions; the pilot-based benchmark with actual errors is in
`VALIDATION.md`.  The original manuscript inside `original_handoff.zip` was not used and is not
endorsed.
