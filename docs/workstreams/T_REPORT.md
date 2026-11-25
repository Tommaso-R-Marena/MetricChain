# Workstream T — known parts with interactions, first case: a function of the type (mean-field models)

> **Repository note (added by the coordinator at integration; the report below is otherwise as
> delivered).**  Status: **paper proofs by one author; re-derived in part and re-computed by
> the coordinator; refereed by R10** (`docs/reviews/R10_brief.md`, `R10_referee_report.md`; see
> the errata below).
> The coordinator re-derived the proofs of T1, T2, T4, T5, T6, T7, T3(a), T8, T8′, T9(a), T9(e),
> read T3(b), T9(b), (c) without re-deriving them in full, and re-computed with independent
> solvers (`experiments/coordinator_checks/meanfield_T/`, `tv_check1.py` … `tv_check4.py`,
> `slice_check.py`, `e_threshold.py`; no discrepancy): the binary optima at five accuracies,
> the free-block profiles at four accuracies and three couplings, the junction `βJ*`, the pair
> identity, cones against shell-cones, a one-phase case with a field, ferromagnets against
> the uniform cube, the threshold `u_top` and the failure of the pair identity at `u = 0.30`.
> The integrated statements and their labels are in `docs/THEORY_REPORT.md` §11.23: T1, T2, T4,
> T10 = Theorem 11.76; T6, T7 = Lemma 11.77; T3 = Theorem 11.78; T5, T8, T8′ = Theorem 11.79;
> T9(a)–(d) = Theorem 11.80; T9(e), §6.6, T12 = Proposition 11.81; §§6.2–6.7 = Proposition
> 11.82; C1, O2–O5 = Conjecture 11.83.  T1(a), (b)(i) and T2 are machine-checked
> (`proofs/Frontiers/TypeQuantiles.lean`, `SymmetricSampling.lean`; the report's "nothing
> formalised" refers to its own work).  Harness: block XIX, DEAD.19, DEAD.20 of
> `experiments/falsify_conjectures.py`.  The author's scripts and outputs are in
> `experiments/workstreams/T/` (`code/`, `out/`; the report's `scratchpad/ws/T/` is that directory).
> §14 of the report lists what changed against earlier drafts; the theory report was written
> from the final version.  The statement of the brief that the report corrects ("the dip
> exponent from its definition around one centre") is recorded in `docs/DEAD_ENDS.md` D49.
>
> **Errata (referee R10, `docs/reviews/R10_referee_report.md`; added by the coordinator at the
> twelfth checkpoint of cycle 10; the text below is unchanged).**  The referee's line numbers
> refer to the report as delivered, which starts at the line "Independent report (25 Nov
> 2026)" below, counted so that the title is line 1.  **Verdict: no critical finding; every
> statement labelled [proved] is proved, some after small repairs; two major and fifteen
> minor findings.**
> *Major.*  **(M1) §6.6, Statement (iii), and §0, row G3(e)** — "for `1 < βJ ≤ βJ*(e,u)` that
> local minimum is global, so `R_H(e) = R_unif(e)`" — is **false as a general statement**:
> true at the parameters computed (`u = 1`) and on the referee's grid for `u ≤ 2`, but for
> large slopes at small or negative accuracies the constant exit at a well becomes
> feasible for the uniform cube's profile below `βJ*` (`u = 8`, `e = 0`, `βJ = 8.2632 < 8.3366`:
> `r_{μ*} = 0`, best profile found `0.36742 < R_unif = 0.39854`; `u = 4`, `e = 0.6e_c`,
> `βJ = 4.9578 < 4.9978`: `0.41763 < 0.41857`); on the grid the junction is at
> `min{βJ*, βJ_w}`.  Statement (ii) and the formula for `βJ*` are correct.  The corollary of
> T12 ("for `1 < βJ ≤ βJ*(ε₁,u)` the adaptive exponent is `R_unif`") inherits the restriction.
> **(M2) §6.5 (4), §0 row G3(d), §7.1 (O5), §12 item 7a** — "only known to lie in
> `[0.00184, 0.00226]`": the upper end is `R^{(2)}(0)`, a *lower* bound of `R_H(0)`; proved is
> `[0.00184, 0.00338]`.
> *Minor.*  (m1) T1, summary display: `ε_n^{tr}(q)` is non**de**creasing in `q`,
> `q*(ε) := inf{q : ε_n^{tr}(q) > ε}`, and the upper bound holds for every `q < q*`.  (m2) (2.1) and
> `Z ≤ (n+1)^{1+c_φ}` need a Lipschitz `φ`; for a continuous one the error is
> `3ln(n+1)/n + ω_φ(1/n)`.  (m3) T3(b), last line: use "`R̄_λ` is nonincreasing and
> `r_μ(x) ≤ R̄_λ(e′)` for `x ≥ e′`", not "`R_λ` is nonincreasing"; the trivial `ω_n` for small `n`.
> (m4) T8(b): `N(X) ≤ min{R̄_H(e) : e + R̄_H(e) ≤ X}` (admissibility at `e < 0`).  (m5) T8(c): left
> limit at jumps of `R̄_H^{−1}`.  (m6) `ψ_H = −V_n(|x|)` against `−n·v(|x|/n)`: they differ by `O(log n)`.
> (m7) T9(c), `E > 0`: the sentence "every constant `ν` is at distance `≥ η`" is not an argument
> (repair: `MI(ν) ≥ ½(ν₁−ν₂)²`, `dist ≥ η − ½|ν₁−ν₂|`); the theorem holds as `R̄_H = R̂` for every real
> `e`.  (m8) T9(e): statements about `θ_na` need the comparison of the game functions, which
> holds by the same argument applied to the Lagrangian; the case "not admissible for the
> field problem" is one line.  (m9) §4.2, last paragraph: an assertion; completed by the
> referee with uniform continuity; not used.  (m10) `e₀ = 0.001804`, not `0.00181`.  (m11) §7.2:
> "`Φ_H⁺(D) < 1` for most sets" is not right on `Q_3`, `Q_4`; the test is void because every set
> with `Φ_H⁺ > 1` has `maxdens = 1`.  (m12) `a_cone = 0.04435`, not `0.0446` (the latter is the
> metastable shell at `m ≈ 0.5025`; confirmed by the coordinator).  (m13) "`e^{0.02509n}`"
> rounds the certified `0.025087` up: read `e^{0.02508n}`; in §6.2 (A) the value at `e = −0.07`
> belongs to the shell `x = 0.2770`.  (m14) T3(a)/T8′: `D ≠ Q_n`, lattice approximations, left
> limits.  (m15) T9(a): "sup" over `γ`, not "max".
> *Not findings.*  T9(d) "`=`" can be proved for differentiable `φ` along the report's sketch;
> **T12 can be completed without uniformity in `p`** (a finite net of fields; the variation
> of the field inside a cell is absorbed into the residual at the price `u → u + 2Δ`) — this
> is now Proposition 11.81(c) of the theory report; new data: a seven-atom profile at
> `e = 0.05` (`0.0063875`), and the free block also with a field `βB = 0.05` at `e = 0.02`
> (`0.0160758` against `0.0152121`).

Independent report (25 Nov 2026).  Directory: `scratchpad/ws/T/` (`T_report.md`, scripts `code/`, outputs `out/`).  The
repository was read at commit `36613b9` and not modified (no state-changing git command, no subagent, no Lean).  All numerics:
own Python (numpy/scipy), fixed seeds, `ulimit -v 4000000`, every run under ten minutes, one heavy process at a time (three
short checks — `t15`, `t16` and an early version of `t17` — overlapped with a queued job); commands, sizes and run times in §13.  Nothing was imported from the repository; the coordinator's exploratory scripts were
read and not used.  Labels on every statement: **[proved]**, **[sketch]**, **[numerical]**, **[conjecture]**, **[known]**.
The repository advanced during the work; §14 lists what was corrected or added late, for readers of an earlier draft.

## 0. Summary of verdicts

| goal | verdict |
|---|---|
| **G1(a)** O1 | **Confirmed, [proved], every `n`, every exchangeable `π`** (Theorem T1): Theorem 11.61(a) uses no property of `π` at all, (b) only its permutation symmetry.  The type-stratified (flat-histogram) sample is optimal among non-adaptive algorithms up to the factor `8(n+1)ln(2(n+1)/δ)/(1−2δ)` and `ln(4/δ)` in the accuracy, with the extremal function `ε_n^{tr}(q)`. |
| **G1(b)** | **[proved]** Every algorithm (adaptive, hinted) needs `(1−2δ)/maxdens(D)` evaluations at a symmetric instance for every sensitive `D` (Theorem T2 = Theorem 11.22(c) applied to the permuted dips; its hypotheses involve no product structure); type level: `(1−2δ)(n+1)^{−2}e^{n·min MI}` (T2′, T3(a)); non-adaptive: truncated cones around shells (T5).  Exact hypergeometric sums for `n ≤ 4000` (§6.3), checked against brute force (`722 + 45` checks). |
| **G1, extra** | **[proved], every `n`:** the flat-histogram instance is the hardest symmetric instance, `Φ_g⁺(D) ≤ (n+1)Φ_H⁺(D)` for every set (Theorem T4) — convex or not. |
| **G2** convex `I` | **Everything of §11.20 except the nested algorithm carries over.**  [proved]: the single-letter formula for the hinted exponent of every symmetric instance (T3; the proof of Theorem 11.63 with Lemma T inside a type class); `H` = hardest additive instance (Sion); binary centres suffice; `F*` is a `GameFunction`, so Theorem 11.66 applies and the pair identity holds; non-adaptive exponent `R_H∘S^{−1}`.  [numerical, `10⁻¹¹`] the brief's cone formulas equal the sup–min (`≤` proved).  **Fails:** the closed form of `F` (no 2×2 game), the clean every-`n` product bound, and **Theorem 11.64 (F7): fibre averages are not Lipschitz relative to a reference** — the adaptive exponent is open.  [proved, given Prop. 11.65(b)]: for a ferromagnet without a field above `T_c` all exponents are those of the uniform cube; for every ferromagnet `R_H ≤ R_unif`.  [sketch]: for ferromagnets an adaptive algorithm with exponent `R_unif` exists (mixture of fields). |
| **G3(a)** numbers | `βJ = 1.5`, `B = 0`, `u = 1`: dip exponent of `H` around one centre `R^{(2)}(0) = 0.0251012` (three methods; the coordinator's `0.026` was a grid value); cone formula `0.0107007`; zero residual `= ` best additive instance `0.0087471`; uniform cube `0.0291391` (a proved upper bound).  `H` is the hardest symmetric instance (theorem; confirmed on 23 landscapes).  Non-adaptive: cones around self-consistent shells give exactly the partner of the dip exponent (a theorem, T8(a)); pair identity to `7·10⁻⁹` for `−0.108 ≤ e ≤ 0.064`; `a = θ_na(0⁺) = 0.110944 = a_unif` (cones: `0.0446`). |
| **G3, new** | **For `e > e₀ = 0.00181` one centre is not enough:** profiles with a *free block* (`≈ 14 %` of the coordinates unconstrained) give larger exponents — `0.016155` against `0.015276` at `e = 0.02`, `0.006387` against `0.004626` at `e = 0.05` — so the brief's "`R_H` from its definition" is not the exponent of `H` there.  I do not know the supremum; brackets in §6.2. |
| **G3(b)** | Lower bounds **[proved]** for every `n` (T2, T3(a), T5); exact sums approach the formulas (§6.3). |
| **G3(c)** | The isoperimetric statement for `H` is **[proved] for every `I`** with the exponent function `R_H = sup` over all block profiles (T3(b)); `R_H` is 1-Lipschitz and the shear `e + R_H(e)` is nondecreasing for every `I` (Lemma T8′).  What is conjectural is the *value* of that supremum (C1: binary for `e ≤ e₀`; open for `e > e₀`), strict monotonicity of the shear, and the adaptive upper bound.  Small cubes and seven families of sets at `n ≤ 144`: no counterexample (§7). |
| **G3(d)** | Barrier steeper than `u`: all theorems hold unchanged; numbers in §6.5.  While the top of the barrier is a wide contact piece (`u ≥ 0.35` at `βJ = 1.5`) nothing changes (ratio to the uniform cube `≈ 0.82`, pair identity to `2·10⁻⁹`); when it leaves the contact set (`u < u_top = 0.2815`) the optimal dips move to the wells (ratio `0.27`, pair identity again); **in between (`u = 0.30`, a narrow piece at the top) the pair identity fails for cones around profile classes** (`0.00184` against `0.00226`) and the non-adaptive exponent is open there. |
| **G3(e)** | **Yes, and more:** for `1 < βJ ≤ βJ*(e,u) = 1 + u·c₂/(2L)` (`= 1.125` at `u = 1`, `e = 0`) the two-phase exponents are *equal* to those of the uniform cube; beyond, they decrease continuously (§6.6).  At a fixed accuracy `e > 0` there is a second coupling `βJ**(e,u) > βJ*` at which the free block sets in, continuously (`≈ 1.124` at `e = 0.02`, `≈ 1.10` at `e = 0.04`; local formula and estimate in §6.7); at `e = 0` none was found. |
| **G4** | No statement of the form "the flat-histogram ensemble is minimax-optimal for a certified estimate over a class of perturbations" found (ten searches, abstracts only); closest: worst-case optimal importance proposals (Cérou–Héas–Rousset), minimax mixtures (He–Owen); in the physics literature the flat ensemble is *not* optimal for the dynamics (Trebst–Huse–Troyer).  §9. |
| **G5** | Immediate: all of G1 (orbit-stratified sampling, hardest symmetric instance) for two order parameters and for mean-field Potts; by the same proof (sketch): the single-letter theorem; not immediate: its evaluation. §10. |

**The three things to take away.**  (1) *Type-uniform sampling and the flat-histogram instance are optimal and extremal for
every known part that is a function of the type, at every `n`, by symmetry alone* — non-adaptive optimality up to a polynomial
factor, and hardest-symmetric-instance.  (2) *The exponent of that instance is a single-letter supremum over block profiles,
for every rate function*; for convex `I` it reduces to §11.20 (binary centres, cones, additive instances, game function, pair
identity).  (3) *With two phases the supremum is attained neither by cones (O3: confirmed) nor, beyond a small accuracy `e₀`, by
any set built around one centre (new)*; the extremal perturbations are shells in the barrier type class, and then shells that
constrain only part of the coordinates.  What remains open is the value of the supremum beyond `e₀`, and — also for one phase
— the adaptive exponent without a hint, because the nested algorithm needs a product structure.


## 1. Controls: the field case of §11.20, reproduced before anything else was believed

`t01_control.py` (closed cosh form of Theorem 11.59(b) against the single-letter sup–min of this report, the cone formula, the
pair identity), and exact sums (§6.3):

| quantity (`p = 0.1`, `u = 2`) | value of the brief | closed form (mine) | sup–min over binary centres | cone formula |
|---|---|---|---|---|
| `R^max(0)` | `0.048130` | `0.0481300` | `0.0481300` (`m = 0.5065`, `a = 0.5491`, `b = 0.0148`) | `0.0481300` |
| `E` | `0.21227` | **`0.212295`** | — | — |
| `R^max(0.3E)` | `0.023273` | `0.0232703` (`0.0232727` at `0.3·0.21227`) | `0.0232703` | `0.0232703` |
| `R_0(0.3E)` | `0.019497` | `0.0194967` | `0.0194967` | `0.0194967` |
| `θ_na(0.3E)` | `0.036246` | `0.0362459` | — | `0.0362447` (truncated cone, best of nine centre types, not polished) |
| `θ_na(e + R^max(e)) = R^max(e)`, `e = 0`, `0.3E` | | holds to `10⁻¹³` | `n_{μ*}`: holds to `10⁻¹²` | |
| `p = ½`, `u = 1`: `R^max(0)` | `0.029139` | `0.0291391` | `0.0291391` | `0.0291391` |

The hinted quantities agree to `2·10⁻¹²` between the three methods.  One remark on the brief: `0.21227` is `F*(t)/t` at `t = 10⁻⁴`; the threshold
is the limit `t → 0`, the largest chord gap of `ln 2cosh(x/2)` over the window of fields, `E = 0.212295` (`R^max(0.21229) = 2·10⁻¹¹ > 0`,
`R^max(0.2123) = 0`).  `R_0(0.3E)` and `θ_na(0.3E)` of the brief are for this `E`, `R^max(0.3E) = 0.023273` for
`0.3·0.21227` (the theory report's own table has `0.023270`).  The pair identity fails with `R_0` in place of `R^max`
(`θ_na(R_0(0)) = 0.053144` against `R_0(0) = 0.042692`), as in D47.

## 2. Setting, notation, and the objects of this report

**Setting (brief §2).**  `Q_n = {0,1}ⁿ`, Hamming distance `d`, `L_u = {ψ : |ψ(x) − ψ(y)| ≤ u·d(x,y)}`, `w = e^{−ψ}`,
`A(ψ) = E_π e^{−ψ}`, target `ln A(ψ)`, accuracy `ε = ε₁n`; an algorithm is `(ε/2, δ)`-correct if its output is within `ε/2` of
`ln A(ψ)` with probability `≥ 1 − δ` for **every** `ψ ∈ L_u`; cost = expected number of evaluations of `ψ`.
`T_t = {|x| = t}`, `dens_t(D) = |D ∩ T_t|/|T_t|`, `maxdens(D) = max_t dens_t(D)`.

**Known part.**  `π` is *exchangeable*: `π(x) = p_{|x|}/C(n,|x|)`, `p_t = π(T_t) > 0`; `J_t := −ln p_t`.  For
`f(x) = nφ(|x|/n)` with `φ` continuous on `[0,1]`: `p_t = C(n,t)e^{−nφ(t/n)}/Z_n` and, with
`I := φ − h − min_{[0,1]}(φ − h)` (`h` the binary entropy, nats),

    | J_t/n − I(t/n) | ≤ c_φ·ln(n+1)/n      for all t                                                        (2.1)

(`(n+1)^{−1}e^{nh(t/n)} ≤ C(n,t) ≤ e^{nh(t/n)}`; the lattice minimum of `φ − h` is within `ω_φ(1/n) + h(1/n)` of the continuous one;
for Lipschitz `φ`, `c_φ ≤ 3 + Lip(φ)`).  `v` := the largest `u`-Lipschitz minorant of `I`, `v(κ) = min_{κ′}[I(κ′) + u|κ − κ′|]`;
its lattice version `V_n(t) := min_{t′}[J_{t′} + u|t − t′|]`.  The *contact set* (the brief's window) is `{v = I}`.  Curie–Weiss:
`φ(κ) = −(βJ/2)(2κ−1)² − βB(2κ−1)`; the field of §11.20: `φ = θκ`, `I = KL(·‖p)`.

**Symmetric instances and their landscapes.**  `ψ_g(x) = g(|x|)` with `|g(t+1) − g(t)| ≤ u`.  Put
`Λ_g(t) := −g(t) + min_{t′}[J_{t′} + g(t′)]` — the **exit landscape** of the instance: it is `u`-Lipschitz on the lattice, `Λ_g ≤ J`
with equality somewhere, and it determines the instance up to an additive constant.  Conversely every such `Λ` is the
landscape of the instance `−Λ(|x|)`.  Since `V_n` is the largest `u`-Lipschitz minorant of `J`:

    Λ_g ≤ V_n   for every symmetric instance,   with equality for the flat-histogram instance  ψ_H(x) = −V_n(|x|).          (2.2)

Zero residual: `Λ ≡ min J`.  Additive instance `γ|x|`: `Λ(t) = −γt − max_{t′}[−γt′ − J_{t′}]`.  In the limit: a landscape is a
`u`-Lipschitz function `λ ≤ I` on `[0,1]` touching `I`; `λ = v` for `H`, `λ ≡ 0` for the zero residual,
`λ_γ(κ) = −γκ − I*(−γ)` (`I*` the Legendre transform, which replaces `ln Z_γ` of §11.20) for `γ|x|`.
Gibbs law `μ_g ∝ π e^{−g}`: type weights `e^{−(J_t − Λ_g(t))}/Z_g`, `Z_g := Σ_t e^{−(J_t − Λ_g(t))} ∈ [1, n+1]`;
slack `s_g(x,y) = u·d(x,y) + g(|x|) − g(|y|) ≥ 0`; for `D ⊊ Q_n` the deepest dip `ψ_g^D = max_{y∉D}[ψ_g(y) − u·d(·,y)]` on `D`
(`= ψ_g` off `D`) is in `L_u`, and

    A(ψ_g^D)/A(ψ_g) = 1 + Φ_g(D),   Φ_g(D) = Σ_{x∈D} μ_g(x)(e^{s_g(x→Dᶜ)} − 1),   Φ_g⁺(D) = Φ_g(D) + μ_g(D)
                                                                  = Z_g^{−1} Σ_{x∈D} π(x)·exp( min_{y∉D}[u·d(x,y) + Λ_g(|y|)] ).   (2.3)

**Block profiles.**  Let the coordinates be partitioned into `k` blocks of fractions `λ_j` (the letter `U` of a coordinate is its
block).  A point has the *block profile* `μ = (μ_j)`, `μ_j = P(X = 1 | U = j)` = fraction of ones in block `j`.  Functions of a
profile (`μ̄ := Σ_j λ_jμ_j` the type):

    MI(μ)   = I(U;X) = h(μ̄) − Σ_j λ_j h(μ_j)          (density exponent of the profile class in its type class),
    dist(ν, μ) = Σ_j λ_j |ν_j − μ_j|                    (n·dist = Hamming distance between a point of one class and the other class),
    α(μ)    = MI(μ) + I(μ̄)                             (−n⁻¹ ln π(class), up to O(k·ln n/n)).

A **binary centre** `s` of type `m` is the case of two blocks (`S = 1`: `λ = m`, `μ = 1 − a`; `S = 0`: `λ = 1 − m`, `μ = b`), with the
brief's profile `z = (a, b)`, `κ_z = m(1−a) + (1−m)b`, `ρ(z) = ma + (1−m)b = dist(z, (0,0))`.

**The single-letter functions of this report.**  For a landscape `λ`, a profile `μ` and a budget `B ≥ λ(μ̄)`:

    V(μ, B; λ) := min{ MI(ν) : u·dist(ν, μ) + λ(ν̄) ≤ B }             (ν over the profiles with the same blocks),
    r_μ(e)     := V(μ, e + α(μ); λ)      (defined for e ≥ λ(μ̄) − α(μ); every e ≥ 0 qualifies),
    R_λ(e)     := sup_μ r_μ(e)           (supremum over all finite block structures and profiles),      R_H := R_v,
    R_λ^{(2)}(e) := the same supremum over binary centres only,
    n_μ(X)     := min{ MI(ν) : MI(ν) + u·dist(ν, μ) + λ(ν̄) − α(μ) ≤ X },        N(X) := sup_μ n_μ(X)       (λ = v),
    G_μ(ν)     := MI(ν) + I(ν̄) + u·dist(ν, μ),   𝒱(μ) := min_ν G_μ(ν),
    θ_shell(X; μ₀) := min{ MI(ν) : G_{μ₀}(ν) − 𝒱(μ₀) ≤ X }.

`G_μ − 𝒱(μ)` is the rate of the Gibbs law of the **shell-cone** `ψ = u·d(·, C_μ)` (`C_μ` the class of profile `μ`); `μ₀ = (1, 0)`
(the centre itself) gives the cone, `Λ_m = 𝒱((1,0))`, `J_m = G_{(1,0)} − Λ_m`, and the brief's formulas
`R_cone(e) := max_m min{MI(z) : uρ(z) + λ(κ_z) − Λ_m ≤ e}`, `θ_na^{cone}(x) := max_m min{MI : J_m ≤ x}`.  A profile `μ` is
*self-consistent* if it is its own Gibbs shell: `𝒱(μ) = G_μ(μ) = α(μ)`.

Labels: **[proved]** = complete proof in this report (finite computations named); **[sketch]**; **[numerical]**;
**[conjecture]**; **[known]** (source, and how much of it I read).

## 3. G1 — every-`n` statements that use only the permutation symmetry of `π`

Throughout this section `n` is arbitrary and `π` is an arbitrary exchangeable probability measure on `Q_n` (every known part
that is a function of the type; one phase or two; also the uniform measure on a slice).  No limit is taken.

### 3.1 Observation O1 is correct: Theorem 11.61(a), (b) verified line by line

**Theorem T1 [proved].**  For `ψ ∈ L_u` and `0 < q < 1` let `t_t(ψ, q)` be the smallest value `τ` of `w` on `T_t` with
`dens_t{w > τ} ≤ q`, `ψ^{tr,q}(x) := max(ψ(x), −ln t_{|x|})`, `ε_n^{tr}(q) := sup_{ψ∈L_u} ln[A(ψ)/A(ψ^{tr,q})]` (nonincreasing in `q`).
(a) `t_{t±1} ≤ e^u t_t`; hence `ψ^{tr,q} ∈ L_u`, it differs from `ψ` only on `D = {w > t_{|x|}}`, and `maxdens(D) ≤ q`.
(b) (i) If `ε < ε_n^{tr}(q)`, every randomised **non-adaptive** `(ε/2, δ)`-correct algorithm makes at least `(1 − 2δ)/q` evaluations.
(ii) The type-stratified sample — `M = ⌈8 ln(2(n+1)/δ)/q⌉` uniform points from **each** type class, `(n+1)M` evaluations,
`Â = Σ_t p_t·(mean of w over the sample of T_t)` — with the output `ln Â + ½[ε_n^{tr}(q) + ln 2 − ln(2/δ)]` is `(ε/2, δ)`-correct on `L_u`
for every `ε ≥ ε_n^{tr}(q) + ln(4/δ)`.
So, with `q*(ε) := sup{q : ε_n^{tr}(q) > ε}`, the least cost `N_na(ε, δ)` of non-adaptive algorithms satisfies, for every `n`,

    (1 − 2δ)/q*(ε)   ≤   N_na(ε, δ),          N_na(ε + ln(4/δ), δ)   ≤   (n+1)·⌈ 8 ln(2(n+1)/δ)/q*(ε)⁺ ⌉ :

**the type-stratified ("multicanonical", flat-histogram) sample is optimal among non-adaptive algorithms up to the factor
`8(n+1)ln(2(n+1)/δ)/(1−2δ)` and an additive `ln(4/δ)` in the accuracy, for every exchangeable `π` and every `n`; the extremal
function is `ε_n^{tr}`, and no isoperimetry is used.**

*Proof — what each line uses.*
(a) Let `X` be uniform on `T_t` and `Y` be `X` with a uniformly chosen `0` flipped to `1`.  Each `y ∈ T_{t+1}` arises from `t+1`
points `x`, each with probability `1/(n−t)`, so `P(Y = y) = (t+1)/(C(n,t)(n−t)) = 1/C(n,t+1)`: `Y` is uniform on `T_{t+1}`; and
`w(Y) ≤ e^u w(X)`.  Hence `dens_{t+1}{w > e^u t_t} ≤ dens_t{w > t_t} ≤ q`.  Not all values of `w` on `T_{t+1}` exceed `e^u t_t` (the
density would be `1 > q`); let `τ′` be the largest value of `w` on `T_{t+1}` that is `≤ e^u t_t`; then `{w > τ′} = {w > e^u t_t}` on
`T_{t+1}`, so `t_{t+1} ≤ τ′ ≤ e^u t_t`.  Symmetrically downwards.  So `x ↦ −ln t_{|x|}` is `u`-Lipschitz and `ψ^{tr,q}` is a maximum
of two members of `L_u`.  *Uses:* counting in adjacent type classes only — **not even `π`**.
(b)(i) `A(ψ∘σ) = A(ψ)` for every coordinate permutation `σ` — *this is the exchangeability of `π`, and the only place where
`π` enters* — and `(ψ∘σ)^{tr,q} = ψ^{tr,q}∘σ`.  Choose `ψ` with `ln[A(ψ)/A(ψ^{tr,q})] > ε` and the `n!` pairs `(ψ∘σ, ψ^{tr,q}∘σ)` with weights
`1/n!`.  A point `x` lies in the difference set of the pair `σ` iff `σx ∈ D`; for uniform `σ`, `σx` is uniform on `T_{|x|}`, so this has
probability `dens_{|x|}(D) ≤ q`.  Theorem 11.45(a) (`nonadaptive_expected_queries_ge`: any class, any functional, pairs of members
whose values differ by more than `ε`, every point in difference sets of total weight `≤ B`) gives `(1−2δ)/q`.
(ii) `A(ψ) = Σ_t p_t E_{T_t} w` (exchangeability; the `p_t` — the density of states of the known part — are assumed known), so
`E Â = A` and `Â ≤ A/δ₂` outside probability `δ₂` (Markov).  `dens_t{w ≥ t_t} ≥ q` by the choice of `t_t` (if `t_t` is not the least
value of `w` on `T_t`, the next smaller value `τ⁻` has `dens{w > τ⁻} > q` and `{w > τ⁻} = {w ≥ t_t}`).  So the variables
`min(w(X_i), t_t)/t_t ∈ [0,1]` of class `t` have total mean `≥ Mq =: K`, and the multiplicative Chernoff bound gives a class mean of at
least `½E_{T_t} min(w, t_t)` outside probability `e^{−K/8}`.  On the intersection, `Â ≥ ½A(ψ^{tr,q}) ≥ ½e^{−ε_n^{tr}(q)}A(ψ)`.  With
`K ≥ 8 ln(2(n+1)/δ)` and `δ₂ = δ/2`: `ln A ∈ [ln Â − ln(2/δ), ln Â + ε_n^{tr}(q) + ln 2]`, an interval of length `ε_n^{tr}(q) + ln(4/δ)`. ∎
(Brute force, `t05`: for random members of `L_u` and shell-cones on full cubes `n ≤ 12` with two-phase, one-phase-with-field and
field measures, `ψ^{tr,q} ∈ L_u` and `maxdens(D) ≤ q` in all 72 cases.)

### 3.2 Lower bounds for all algorithms at a symmetric instance

**Theorem T2 [proved].**  Let `ψ_g` be a symmetric instance, `D ⊊ Q_n` nonempty, and `ε < ln(1 + Φ_g(D))`.  Then every randomised
algorithm that is `(ε/2, δ)`-correct on `L_u` — adaptive or not, with any hint, e.g. told that the instance is `ψ_g` — makes at
least

    (1 − 2δ)/maxdens(D)

evaluations in expectation on the instance `ψ_g`.  More generally, for any probability law on sets `D` with
`ε < ln(1 + Φ_g(D))` almost surely, at least `(1 − 2δ)/max_x P(x ∈ D)`.
*Proof.*  Theorem 11.22(c) (`expected_queries_ge_packing`) with the instance `g = ψ_g`, the class `G = L_u`, the functional `ln A`,
the alternatives `g_σ := ψ_g^{σD}` (`σ` over the `n!` coordinate permutations) and the weights `1/n!`.  Its hypotheses: (1) `g_σ ∈ G`
— the lower McShane extension is in `L_u`; (2) `|ln A(g_σ) − ln A(g)| > ε` — because `ψ_g∘σ = ψ_g`, `d` and `π` are invariant,
`g_σ = ψ_g^D∘σ^{−1}` and `A(g_σ) = A(ψ_g^D) = A(ψ_g)(1 + Φ_g(D))` by (2.3); (3) every point `x` detects (`g_σ(x) ≠ g(x)`)
alternatives of total weight at most `B`: `g_σ ≠ g` only inside `σD`, and `P_σ(x ∈ σD) = dens_{|x|}(D) ≤ maxdens(D) =: B`.  The theorem
is stated for an arbitrary class, an arbitrary functional and a finite family of alternatives; **nothing in it refers to a product
structure** (that enters Theorem 11.27(c) only, where it produces the clean form `e^{−tε + nF}`).  ∎

**Corollary T2′ (type level, binary centre) [proved].**  Let `s` have type `k`, let `P` be a set of profile classes
`(i, j)` (`i` zeros of `x` on the ones of `s`, `j` ones of `x` on the zeros of `s`) and `D_P` their union.  Then, exactly,

    dens_t(D_P) = Σ_{(i,j)∈P, k−i+j=t} C(k,i)C(n−k,j)/C(n,t),
    Φ_g⁺(D_P) = Z_g^{−1} Σ_{(i,j)∈P} C(k,i)C(n−k,j)·e^{−J_t}/C(n,t)·e^{T(i,j)},     T(i,j) = min_{(i′,j′)∉P}[u(|i−i′| + |j−j′|) + Λ_g(k−i′+j′)]

(the Hamming distance from a point of class `(i,j)` to the class `(i′,j′)` is `|i−i′| + |j−j′|`), and since
`C(k,i)C(n−k,j)/C(n,t) ≤ (n+1)e^{−n·MI(z)}`, `maxdens(D_P) ≤ (n+1)² e^{−n·min_{z∈P} MI(z)}`:

    E#evaluations at ψ_g   ≥   (1 − 2δ)·(n+1)^{−2}·exp( n·min_{z∈P} MI(z) )        whenever   ε < ln(1 + Φ_g(D_P)).

The same holds with `k` blocks and `(n+1)^k` (Theorem T3(a)).  The exact sums are implemented in `tfin.py`/`kfin.py`, checked
against brute force (`t05`: 722 checks, `n ≤ 12`, worst relative error `3·10⁻¹⁵`; `t08` part 0), and evaluated for `n ≤ 4000` in §6.3.

### 3.3 The flat-histogram instance is the hardest symmetric instance — for every `n`, convex or not

**Theorem T4 [proved].**  For every symmetric instance `ψ_g`, every `n` and every `D ⊊ Q_n`:

    Φ_g⁺(D) ≤ (n+1)·Φ_H⁺(D),        hence        ln(1 + Φ_g(D)) > ε   ⟹   ln(1 + Φ_H(D)) > ε − ln(n+2).

So every lower bound that Theorem T2 gives at a symmetric instance at accuracy `ε` holds at `H` at accuracy `ε − ln(n+2)`;
in the limit `R_λ ≤ R_H` for every landscape (pointwise in the single-letter problem: `λ ≤ v` enlarges the feasible set).
*Proof.*  By (2.3), `Φ_g⁺(D) = Z_g^{−1}Σ_{x∈D}π(x)e^{min_y[u·d(x,y) + Λ_g(|y|)]}` with `Z_g ≥ 1`, and `Λ_g ≤ V_n` by (2.2); for `H` the same
expression with `V_n` and `Z_H ≤ n+1`.  Then `1 + Φ_g ≤ 1 + Φ_g⁺ ≤ 1 + (n+1)(Φ_H + μ_H(D)) ≤ (n+2)(1 + Φ_H)`.  ∎
(Not a statement about non-symmetric instances; see §8.)

### 3.4 Non-adaptive algorithms: truncated shell-cones

**Theorem T5 [proved].**  For every nonempty `C ⊂ Q_n`, `ψ_C := u·d(·, C) ∈ L_u`; by Theorem T1(b)(i), if
`ε < ln[A(ψ_C)/A(ψ_C^{tr,q})]` every non-adaptive algorithm needs `(1 − 2δ)/q` evaluations.  For `C = C_μ`, the class of a block
profile `μ` with `k` blocks, and `q = e^{−nθ}`:

    ln[A(ψ_C)/A(ψ_C^{tr,q})]  ≥  n·[ min{ G_μ(ν) : MI(ν) ≤ θ + (k+1)ln(n+1)/n } − 𝒱(μ) ]  −  c_k ln(n+1) − c_φ′,

so non-adaptive algorithms have an exponent at least `θ_shell(ε₁⁺; μ)` for every `μ`.  (`C` a single point: the truncated cones of
Theorem 11.61(c).)
*Proof.*  `w = e^{−u·d(·,C)}` is constant on the profile classes ("cells") `c`; write `d_c` for the density of `c` in its type class
and `ν_c` for its profile; `(n+1)^{−k}e^{−n·MI(ν_c)} ≤ d_c ≤ (n+1)e^{−n·MI(ν_c)}`, at most `(n+1)^{k−1}` cells per type, and
`π(c)w(c) = p_t d_c w(c) = exp(−nG_μ(ν_c) + O(k ln n))` by (2.1).  Fix a type `t` and put `θ″ := θ + (k+1)ln(n+1)/n`; call a cell *seen*
if `MI(ν_c) ≤ θ″`.  (1) The cells with `w ≥ t_t` have total density `≥ q`, so one of them, `c*`, has `d_{c*} ≥ q/(n+1)^{k−1}`; it is
seen, and `q·t_t ≤ (n+1)^{k−1}d_{c*}w(c*)`.  (2) `E_{T_t}min(w, t_t) = Σ_c d_c min(w(c), t_t)`; a seen cell contributes at most `d_cw(c)`; a
cell that is not seen has `d_c ≤ (n+1)e^{−nθ″} ≤ q` and contributes at most `q·t_t`.  Hence
`E_{T_t}min(w,t_t) ≤ 2(n+1)^{2(k−1)}·max_{c seen, in T_t} d_cw(c)`, and
`A(ψ_C^{tr,q}) ≤ 2(n+1)^{2k−1}·max_{c seen} π(c)w(c)`, while `A(ψ_C) ≥ max_c π(c)w(c)`.  ∎  No unimodality is needed (the proof of
Theorem 11.61(c) uses the log-concavity of hypergeometric shells; here every level is compared with the densest cell above the
quantile).  Exact sums: `tfin.py` (`shell_cone`), checked against brute force (`t05`), evaluated in §6.3.

## 4. The single-letter theory for an arbitrary rate function `I` (convex or not)

From here on `f = nφ(|x|/n)`, `φ` continuous, and (2.1) holds.  Exponents are limits `n → ∞` at accuracy `ε = ε₁n`.

### 4.1 Two lemmas about the inner problem

**Lemma T6 (clipping) [proved].**  For fixed `κ′` and `r`, the minimum of `MI(ν)` over `{ν : ν̄ = κ′, dist(ν, μ) ≤ r}` is attained at a
*clipping* of `μ`: `ν_j = min(max(μ_j, c_lo), c_hi)` for some `0 ≤ c_lo ≤ c_hi ≤ 1`.  Consequently, for every landscape `λ`,
`V(μ, B; λ) = min{ MI(clip(μ; c_lo, c_hi)) : u·dist + λ(type) ≤ B }` — a two-parameter problem for every number of blocks; and if `λ`
is `u`-Lipschitz, the constraint is nondecreasing and `MI(clip)` nonincreasing in `c_lo` (and the reverse in `c_hi`), so the
minimum lies on the boundary curve of the feasible set (a one-dimensional search).
*Proof.*  For fixed `ν̄ = κ′`, minimising `MI = h(κ′) − Σλ_jh(ν_j)` is maximising the strictly concave `Σλ_jh(ν_j)` over a polytope.
KKT with multipliers `η` (mean) and `τ ≥ 0` (distance): `h′(ν_j) = η + τ` if `ν_j > μ_j`, `h′(ν_j) = η − τ` if `ν_j < μ_j`, and
`h′(μ_j) ∈ [η − τ, η + τ]` if `ν_j = μ_j`.  `h′` is strictly decreasing, so all raised blocks take the value
`c_lo := (h′)^{−1}(η+τ)`, all lowered ones `c_hi := (h′)^{−1}(η−τ) ≥ c_lo`, and the unchanged ones have `μ_j ∈ [c_lo, c_hi]`.
Monotonicity: raising `c_lo` moves mass `Λ_↑ := Σ_{μ_j<c_lo}λ_j` upwards, `d(u·dist + λ(type)) = Λ_↑(u + λ′)dc_lo ≥ 0` and
`dMI = Λ_↑(h′(type) − h′(c_lo))dc_lo ≤ 0` because `c_lo ≤` type.  ∎

**Lemma T7 (`v` or `I` in the constraint; exits lie in the contact set) [proved].**  For every `μ`, `B`:

    min{ MI(ν) : u·dist(ν,μ) + v(ν̄) ≤ B }  =  min{ MI(ν) : u·dist(ν,μ) + I(ν̄) ≤ B },

and the minimiser can be taken with `ν̄` in the contact set `{v = I}`; the same with `MI(ν) + u·dist + v` and `MI(ν) + u·dist + I`
(in `n_μ`), and with `min_ν[MI + v + u·dist(·,μ₀)] = 𝒱(μ₀)`.
*Proof.*  "`≤`" since `v ≤ I`.  Let `ν` be feasible on the left, `κ′ = ν̄`, and `κ*` with `v(κ′) = I(κ*) + u|κ′ − κ*|`.  If `κ* < κ′`
let `X″ = X′·B`, `B ∼` Bernoulli(`κ*/κ′`) independent ("thinning"; if `κ* > κ′`, `X″ = X′ ∨ B`): `ν″_j = ν_jκ*/κ′`, `ν̄″ = κ*`,
`dist(ν″, ν) = |κ′ − κ*|`, and `MI(ν″) = I(X″;U) ≤ I(X′;U) = MI(ν)` (data processing).  Then
`u·dist(ν″,μ) + I(κ*) ≤ u·dist(ν,μ) + u|κ′−κ*| + I(κ*) = u·dist(ν,μ) + v(κ′) ≤ B`.  ∎  (This replaces the "window step" of
Lemma SL; it needs no convexity.)

### 4.2 The main theorem: the hinted exponent of every symmetric instance

**Theorem T3 [proved; (a) for every `n`, (b) by the method of types — the proof of Theorem 11.63 with one change].**
Let `λ` be a landscape (`u`-Lipschitz, `λ ≤ I`, touching `I`) and `ψ_n = −nλ(|x|/n) ∈ L_u` its instance.
(a) *Lower bound, every `n`.*  Let `μ` be a block profile with `k` blocks on the lattice of `n` (block sizes `n_j`, `i_j` ones in block
`j`), `C` its class, `B > λ(μ̄) + ln 2/n`, and `D := ∪{classes c′ : u·ℓ¹(c′, c)/n + λ(type(c′)/n) < B}`.  Then

    ln(1 + Φ(D)) ≥ n(B − α_n(μ)) − ln 2 − ln Z,        maxdens(D) ≤ (n+1)^k·exp(−n·V(μ, B; λ)),

(`α_n(μ) := −n⁻¹ln π(C) = α(μ) + O(k ln n/n)`, `Z ≤ (n+1)^{1+c_φ}`), so by Theorem T2 every algorithm makes at least
`(1 − 2δ)(n+1)^{−k}e^{n·V(μ,B;λ)}` evaluations at `ψ_n` whenever `ε < n(B − α_n(μ)) − ln 2 − ln Z`.  Hence the hinted exponent of the
instance is at least `R_λ(ε₁⁺)`.
(b) *Upper bound (isoperimetry for the type-uniform measure).*  There is `ω_n → 0`, depending on `(φ, u)` only, such that for all `n`,
all real `e` and all `D ⊊ Q_n`:

    Φ⁺(D) ≥ e^{ne}      ⟹      maxdens(D) ≥ exp( −n[ R̄_λ(e − ω_n) + ω_n ] ),        R̄_λ(e) := max(R_λ(e), −e).

(`R̄_λ = R_λ` for `e ≥ 0`; for `H`, `R_H(e) ≥ −e` at least for `−e ≤ h(κ₀)`, `κ₀` a global minimum of `I` — take `μ̄ = κ₀`, `MI(μ) = −e`,
where the feasible set is `{μ}` — and in all computations.)  Consequently the hedged spot-check of Theorem 11.22(e) with samples
from `½μ_n + ½·(uniform over types, uniform inside each type class)` costs `exp(nR_λ(ε₁) + o(n))` at `ψ_n` (at continuity points of
`R_λ`): **the hinted exponent of every symmetric instance of every function-of-type known part is `R_λ(ε₁)`.**
*Proof of (a).*  For `x ∈ C` and `y ∉ D`: `u·d(x,y)/n + λ(κ_y) ≥ u·ℓ¹(cell(y), c)/n + λ(κ_y) ≥ B` (the block profile distance bounds the
Hamming distance from below).  By (2.3), `Φ⁺(D) ≥ π(C)e^{nB}/Z` and `C ⊂ D` with slack `≥ n(B − λ(μ̄)) > ln 2`, so
`Φ(D) ≥ ½π(C)e^{nB}/Z`.  Every class of `D` satisfies the (closed) constraint of `V(μ, B; λ)`, has density `≤ (n+1)e^{−n·MI}` in its
type class, and there are at most `(n+1)^{k−1}` classes per type.  ∎
*Proof of (b).*  Steps 1–6 of the proof of Theorem 11.63 (F6), with `δ = n^{−1/4}`, `δ₁ = δ/(2u)`, `m = ⌈n^{1/8}⌉`.
*Step 1.*  `Φ⁺(D) = Z^{−1}Σ_{x∈D}π(x)e^{nB(x)}`, `B(x) := min_{y∉D}[λ(κ_y) + u·d(x,y)/n]` (at most `(n+1)²` values); split `D` by the value
of `B` **and by the type of `x`** (at most `(n+1)³` classes) and fix the class `C ⊂ T_k` with the largest `π(C)e^{nB}`.  With
`α_C := h(κ) − n⁻¹ln|C|` (`κ = k/n`): `e ≤ B − I(κ) − α_C + c₁ln(n+1)/n`, and (∗): every `y` with `λ(κ_y) + u·d(x,y)/n < B` for some
`x ∈ C` lies in `D`.  (If `k ∈ {0, n}`, `C` is a whole type class and `maxdens(D) = 1`.)
*Step 2 — the one change.*  Apply Lemma T (inherently typical subsets; a statement about an arbitrary **product** measure and an
arbitrary set) to `C` with the product measure `Bernoulli(κ)^{⊗n}`, **which is uniform on `T_k`, as `π` is**: `−n⁻¹ln Ber(κ)ⁿ(C) = α_C`.
It gives `C̃ ⊂ C`, labels `u_i(x^{i−1}) ∈ 𝒰` (`|𝒰| ≤ (m+1)²`) and a joint type `P_{UX}` with `P_X = Ber(κ)` exactly, so that
`α := D(P_{X|U}‖Ber(κ)|P_U) = I(X;U)`, `α_C − 2/m ≤ α ≤ α_{C̃} ≤ α_C + 2(m+1)²ln(n+1)/n`, and `I(X_I;V|U_I) ≤ η_{m,n}` under the uniform law
on `C̃`.  (This is where §11.20 used `α = D(P_{X|U}‖π|P_U)` for the product measure `π`; here the `π`-exponent of the class is
`I(X;U) + I(P_X) = α(μ)` with `μ_u = P(X=1|U=u)`.)  `λ(κ) ≤ B` because `λ` is `u`-Lipschitz.
*Step 3 (shallow case, `B < λ(κ) + 3δ`).*  `maxdens(D) ≥ dens_κ(C̃) ≥ e^{−nα_{C̃}}`, and
`α_{C̃} ≤ B − I(κ) − e + o(1) ≤ (λ − I)(κ) + 3δ − e + o(1) ≤ −e + o(1)` — this is the term `−e` in `R̄`.
*Step 4 (deep case).*  By the definition of `V` there is a kernel `W(x′|x,u)` with `u·P(X′≠X) + λ(P_{X′}) ≤ B − 2δ` and
`I(X′;U) = V(μ, B − 2δ; λ) ≤ R_λ(B − 2δ − α − I(κ))` — **the definition of `R_λ` as a supremum over all `P_{UX}` replaces Lemma SL** (its
evaluation is a separate question, §§5–6).  Draw `Xⁿ` uniformly from `C̃` and `X′_i ∼ W(·|x_i, u_i(x^{i−1}))` independently; by Hoeffding,
outside probability `θ_n = 3e^{−2nδ₁²}`, `λ(κ_{X′ⁿ}) + u·d(X′ⁿ,x)/n ≤ B − δ < B`, so `X′ⁿ ∈ D` by (∗).
*Step 5 (chain rule).*  With `Q := P_{X′}`: `n⁻¹D(P_{X′ⁿ}‖Qⁿ) ≤ I(X′;U) + η_{m,n}` — verbatim (it uses that `Qⁿ` is a product measure
and Lemma T(4); `π` does not occur).
*Step 6 — simpler than in §11.20.*  Data processing for the event `D`: `(1 − θ_n)ln(1/Qⁿ(D)) − ln 2 ≤ D(P_{X′ⁿ}‖Qⁿ)`.  For **every**
`y` and every `Q`, `Qⁿ(y) ≤ e^{−nh(κ_y)} ≤ 1/|T_{|y|}|`, so `Qⁿ(D) ≤ Σ_t dens_t(D) ≤ (n+1)·maxdens(D)`.  (No typical set of `Q`, no window,
no continuity of `I − v`: the type-uniform measure dominates every product measure up to `n+1`.)  Altogether

    −n⁻¹ln maxdens(D) ≤ [R_λ(B − 2δ − α − I(κ)) + η_{m,n} + ln 2/n]/(1 − θ_n) + ln(n+1)/n,     B − α − I(κ) ≥ e − [2(m+1)² + c₁]ln(n+1)/n,

and `R_λ` is nonincreasing and bounded by `ln 2`.  ∎
*What the proof uses of `π`:* exchangeability and (2.1), in Step 1 only.  *What it does not give:* the value of `R_λ` — in §11.20
Lemma SL showed `sup_{P_{UX}} V = max_γ R_γ` with the closed 2×2 game; here the supremum over block profiles is the object.
For `H` and `μ_H` in place of the type-uniform measure: `μ_H ≥` (type-uniform) on the contact set, and by Lemma T7 the
kernel can be chosen with `P_{X′}` in the contact set; then Step 6 as in §11.20 gives `μ_H(D) ≥ e^{−n[R̄_H(e−ω_n)+ω_n]}` as well
(with `I − v` Lipschitz near the contact set, since `|I′| ≤ u` there).

### 4.3 Non-adaptive algorithms: the exponent, the shear law, and why shells

**Theorem T8 [proved].**  (a) *Shell-cones against dips.*  For every block structure,

    sup_{μ₀} θ_shell(X; μ₀)  =  sup_μ n_μ(X),

the suprema over profiles with these blocks; the left supremum may be restricted to self-consistent shells.
(b) `n_μ(X) = min{ r_μ(e) : e + r_μ(e) ≤ X }`, and therefore, for `R = R_H`, `S(e) := e + R(e)`,

    N(X) ≤ min{ R(e) : S(e) ≤ X },

with equality whenever, for `e₀` with `S(e₀) = X`, there are profiles `μ` with `r_μ(e₀) → R(e₀)` and `e + r_μ(e) > X` for all `e > e₀`
(the *witness condition*; it is checked at every point computed — the columns `n_{μ*}` of the tables).

(c) *Upper bound.*  `n⁻¹ε_n^{tr}(e^{−nθ}) ≤ θ + R̄_H^{−1}(θ) + o(1)` (`R̄_H^{−1}(θ) := inf{e : R̄_H(e) < θ}`), so `e^{n(θ+o(1))}` points per type class
certify the accuracy rate `θ + R̄_H^{−1}(θ)`: the shear law of §11.21 as an upper bound.  Hence the exponent `θ_na` of
non-adaptive algorithms satisfies `N(ε₁⁺) ≤ θ_na(ε₁) ≤ inf{θ : θ + R̄_H^{−1}(θ) < ε₁}`, and if `S` is strictly increasing where it is
positive, `R_H` is continuous and equality holds in (b), then **`θ_na = R_H ∘ S^{−1}`: the pair identity
`θ_na(e + R_H(e)) = R_H(e)`** — with `R_H` the full supremum, whatever its value.
*Proof.*  (a) "`≤`": let `μ*` minimise `G_{μ₀}`.  For every `ν`, by the triangle inequality,
`G_{μ₀}(ν) − 𝒱(μ₀) = MI(ν) + I(ν̄) + u·dist(ν,μ₀) − α(μ*) − u·dist(μ*,μ₀) ≤ MI(ν) + [u·dist(ν,μ*) + I(ν̄) − α(μ*)]`,
so `{MI + u·dist(·,μ*) + I − α(μ*) ≤ X} ⊂ {G_{μ₀} − 𝒱(μ₀) ≤ X}` and `θ_shell(X; μ₀) ≤ n_{μ*}(X)` (Lemma T7 for `I` against `v`).
"`≥`": for every `μ`, `𝒱(μ) ≤ G_μ(μ) = α(μ)`, so `G_μ(ν) − 𝒱(μ) ≥ MI(ν) + u·dist(ν,μ) + I(ν̄) − α(μ)` and `θ_shell(X; μ) ≥ n_μ(X)`.
Applying "`≤`" and then "`≥`" to `μ*`: `θ_shell(X; μ₀) ≤ n_{μ*}(X) ≤ θ_shell(X; μ*)`, and `μ*` is self-consistent
(`G_{μ*}(ν) ≥ G_{μ₀}(ν) − u·dist(μ*,μ₀) ≥ G_{μ₀}(μ*) − u·dist(μ*,μ₀) = α(μ*)`).
(b) If `ν` attains `n_μ(X)` and `e* := u·dist(ν,μ) + v(ν̄) − α(μ)`, then `r_μ(e*) ≤ MI(ν)` and `e* + r_μ(e*) ≤ X`; conversely a minimiser
of `r_μ(e)` with `e + r_μ(e) ≤ X` is feasible for `n_μ(X)`.  For `e` with `S(e) ≤ X`: `e + r_μ(e) ≤ S(e) ≤ X`, so `n_μ(X) ≤ r_μ(e) ≤ R(e)`.
(c) The proof of Theorem 11.61(d), verbatim: `A(ψ^{tr}) ≥ qT` with `T = max_t p_t t_t`; `t_t ≤ T·min_{t′}e^{u|t−t′|}/p_{t′} = T·e^{V_n(t)}` by
T1(a); for `x ∈ D`, `y ∉ D`: `w(x) ≤ t_{|y|}e^{u·d(x,y)}`; so `A(ψ) − A(ψ^{tr}) ≤ T·Z_H·Φ_H⁺(D)` with `maxdens(D) ≤ q`, and T3(b) bounds `Φ_H⁺(D)`.
(`V_n` is the lattice inf-convolution by definition, so no convexity enters.)  ∎

**Lemma T8′ (the shear is monotone; `R̄_H` is 1-Lipschitz — for every `I`) [proved].**  For all `e′ < e`:
`R̄_H(e) ≥ R_H(e′) − (e − e′)`.  Hence `R̄_H` is nonincreasing and 1-Lipschitz (in particular continuous), `S̄(e) := e + R̄_H(e)` is
nondecreasing, and `θ ↦ θ + R̄_H^{−1}(θ)` is nonincreasing: no convexity is needed for the slope condition of a `HintPair`.
*Proof.*  Let `D` be a set with `Φ_H⁺(D) ≥ e^{ne′}` and `maxdens(D) = q = e^{−nθ′}`, `θ′` close to `R_H(e′)` (T3(a)), `N := ⌈e^{n(e−e′)}⌉` with
`Nq ≤ 1`, and `D′ := ∪_{i≤N}σ_iD` for independent uniform permutations `σ_i`.  Then `maxdens(D′) ≤ Nq`.  A point lies in `σ_iD` with
probability `≤ q`, independently in `i`, so `P(x lies in ≥ k copies) ≤ (Nq)^k/k! ≤ 1/k!`, and with positive probability no point
lies in more than `n` copies.  Since `s_H(x → D′ᶜ) ≥ s_H(x → (σ_iD)ᶜ)` for `x ∈ σ_iD`,
`Φ_H⁺(D′) ≥ Σ_{x∈D′}μ_H(x)·max_{i: x∈σ_iD}e^{s_H(x→(σ_iD)ᶜ)} ≥ n^{−1}Σ_iΦ_H⁺(σ_iD) = (N/n)Φ_H⁺(D) ≥ e^{ne}/n`.  By T3(b),
`θ′ − (e − e′) ≤ −n^{−1}ln maxdens(D′) ≤ R̄_H(e − ln n/n − ω_n) + ω_n`.  Let `n → ∞`; a nonincreasing function that satisfies the
inequality for left limits has no jumps.  ∎
(Unions of permuted copies of a sensitive set are the mechanism; in the single-letter supremum they appear as profiles with a
smaller `MI` — for example a cylinder over a free block is the union of the `2^{λ_fn}` shells whose centres differ on that block.
This is why the supremum over **all** block structures, and not the binary one, is the right exponent function: for a single
profile `e ↦ r_μ(e)` can fall faster than with slope `−1` (the marginal shells of §6.5 (4), `u = 0.3`), and the argument gives nothing
for the binary `R_H^{(2)}` (whose computed slopes are all in `[−1, 0]`); `R_H` cannot.)  What the lemma does not give is that `S̄` is *strictly*
increasing where it is positive: on an interval where `R_H(e) = R_H(e′) − (e − e′)` the shear is flat and `θ_na` jumps there
(then `θ_na(X) = R_H(e)` at the right end of the flat piece, and `θ_na(e + R_H(e)) = R_H(e)` fails inside it).

*Reading.*  (a) explains observation O3 in one line: **a truncated cone around a point centre is the shell-cone with
`μ₀ = (1, 0)`; it is as good as the dip whose Gibbs shell `μ*` it has, and only if `μ*` lies between the centre and the
truncation shell.  When the cone's Gibbs measure sits in a well while the hard dips sit on the barrier, the cone is the wrong
function — the right one is the cone around a self-consistent shell, which is its own Gibbs shell.**  Self-consistency has a
local form: `|φ′(μ̄) + logit(μ_j)| ≤ u` for every block (first-order condition of `G_μ` at `μ`; `−φ′(μ̄)` is the mean-field
effective log-odds), so the largest `MI` of a locally self-consistent profile with type `μ̄` is attained by the two-block profile
with `logit(μ_j) = −φ′(μ̄) ± u` — the cone law in the effective field of its own type.

## 5. G2 — convex `I` (one phase): what carries over, step by step

### 5.1 Statements

**Theorem T9 (convex `I`).**  Let `I` be convex on `[0,1]` (Curie–Weiss with `βJ ≤ 1`, any field; every antiferromagnet).
(a) **[proved]** *The flat-histogram instance is exactly as hard as the hardest additive instance.*  For every profile `μ` and
`B ≥ v(μ̄)`: `V(μ, B; v) = max_{|γ|≤u} V(μ, B; λ_γ)`, hence `R_H(e) = max_{|γ|≤u} R_γ(e)`.
(b) **[proved]** *Binary centres suffice:* `R_γ = R_γ^{(2)}` and `R_H = R_H^{(2)}` (for `e ≥ 0`; in the Lagrangian form for every `τ ∈ (0,1)`).
(c) **[proved]** *There is a game function.*  With `φ_{μ,γ}(t) := min_ν[MI(ν) + t(u·dist(ν,μ) + λ_γ(ν̄) − α(μ))]` put
`F*(t) := max_{|γ|≤u} sup_μ φ_{μ,γ}(t)`.  Then `F*` is continuous on `[0,1]`, `F*(0) = F*(1) = 0`, `F*(t) ≤ L(1−t)`, `F*(t) ≤ E·t` with
`E := sup_{t>0}F*(t)/t ∈ (0, ∞)` — the hypotheses of `GameFunction` (`GamePair.lean`) — and

    R̂(e) := max_{0≤t≤1}[F*(t) − te]  (all real e),     R_H = R̂ on e ≥ 0,   R̄_H ≤ R̂ everywhere,     N(x) = max_{0≤τ<1}(F*(τ) − τx)/(1 − τ) = R̂(Ŝ^{−1}(x))   (x > 0),

`Ŝ(e) := e + R̂(e)`.  So Theorem 11.66 applies to `F*`: `R̂` is convex, nonincreasing, with slopes in `[−1, 0]`; `(N, R̂)` is a `HintPair`; the
pair identity `N(e + R̂(e)) = R̂(e)` holds; and with Theorems T3, T8 (lower bound `N`; upper bound through `R̄_H ≤ R̂`): **the exponent of
non-adaptive algorithms is `θ_na = R̂∘Ŝ^{−1}`, attained by the type-stratified sample, and the hinted exponent of `H` and of the
hardest additive instance `γ*|x|` is `R_H = R̂` (`e ≥ 0`).**
(d) **[`≤` proved; `=` numerical, `10⁻¹¹`; sketch]** *The brief's cone formulas are right:* `R_cone(e) ≤ R_λ^{(2)}(e)` for every `I` and
every landscape, with equality for convex `I` (ten cases, `t02`).  So for convex `I`:
`R_H(e) = max_m min{MI(z) : uρ(z) + v(κ_z) − Λ_m ≤ e}`, `θ_na(x) = max_m min{MI(z) : J_m(z) ≤ x}`, `Λ_m = min_z[MI + I(κ_z) + uρ]`.
(e) **[proved, given Proposition 11.65(b) and Lemma SL of §11.20 (both refereed)]** *Ferromagnets are never harder than the uniform
cube; without a field and above the critical temperature they are exactly the uniform cube.*  If `φ` is concave (ferromagnetic
interaction, any strength — **also below the critical temperature**), then for all `e`

    R_H(e) ≤ sup_κ R^max_{field p₀(κ)}(e) ≤ R^max_{p=½}(e) = KL((Λ₁+e)/u ‖ ½),        logit p₀(κ) = −φ′(κ)

(`p₀(κ)` is the mean-field effective site law at type `κ`).  If moreover `I` is convex and symmetric (`B = 0`, `0 ≤ βJ ≤ 1`), then
`R_H(e) = KL((Λ₁+e)/u‖½)`, `γ* = 0`, `θ_na(x) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ x}`: **an interaction without a field changes nothing.**
For a symmetric convex `I` that is not ferromagnetic only `R_H ≥ R_unif` is proved; numerically there is equality
(`βJ = −1, −2, −8, −40`, §5.3).

*Proof of (a).*  `v` is convex (inf-convolution of convex functions) and `u`-Lipschitz, so it is the supremum of its affine
minorants, which have slopes in `[−u, u]` and are minorants of `I`; the largest affine minorant of `I` with slope `−γ` is `λ_γ`, and
`λ_γ ≤ v`: `v = max_{|γ|≤u}λ_γ`.  `g(ν) := u·dist(ν,μ) + v(ν̄) − B` is convex, so by Sion's theorem (the set of `ν` is compact)
`V = sup_{τ≥0}min_ν[MI + τg]`, and for fixed `τ`, `min_ν max_γ[MI(ν) + τ(u·dist + λ_γ(ν̄) − B)] = max_γ min_ν[…]` (convex in `ν`; concave in
`γ`, since `λ_γ(κ) = −γκ − I*(−γ)` and `I*` is convex; both sets compact).  The inner problem is the Lagrangian of `V(μ, B; λ_γ)`. ∎
*Proof of (b).*  Fix `γ` and `0 < τ < 1`.  Everything depends on `μ` through the law `ρ` of `M := μ_U` on `[0,1]`:
`MI(ν) = min_Q Σ_jλ_jKL(ν_j‖Q)`, the minimisation over `ν` separates over blocks for fixed `Q`, and
`α(μ) = h(E_ρM) − E_ρh(M) + I(E_ρM)`, so

    φ_{μ,γ}(τ) + τI*(−γ) = min_Q E_ρ[ G_Q(M) + τh(M) ] − τ(h + I)(E_ρM),        G_Q(μ) := min_ν[KL(ν‖Q) + τu|ν − μ| − τγν].

For a fixed mean the laws `ρ` form a convex compact set, the bracket is linear in `ρ` and convex in `Q`: by Sion there is a saddle
point `(ρ*, Q*)`, and `ρ*` maximises `E_ρ g`, `g := G_{Q*} + τh`, among the laws with that mean, so it is carried by the points where
`g` touches a supporting line of its concave envelope.  `G_Q` is the `τu`-Lipschitz regularisation of the convex function
`KL(·‖Q) − τγ·`: affine with slope `−τu` on `[0, ν_−]`, equal to it on `[ν_−, ν_+]`, affine with slope `+τu` on `[ν_+, 1]`.  Hence `g` is
strictly concave on the two outer pieces and strictly convex on the middle one (`−(1−τ)h +` affine): a line touches its
envelope in at most two points.  So the supremum over all block profiles is attained with at most two block types.  (`τ ≥ 1`
contributes at most `−e ≤ 0`, see (c).)  With (a) and `R_γ^{(2)} ≤ R_H^{(2)} ≤ R_H = max_γR_γ`: `R_H = R_H^{(2)}`.  ∎
*Remark.*  The argument for one `γ` uses that `λ_γ` is affine and nothing about `I` (the term `(h+I)(E_ρM)` is constant at fixed mean):
**for additive instances binary centres suffice for every rate function, convex or not** — only the step from the
additive instances to `H` needs a convex `I`.
(At the saddle the tangency conditions read `logit μ_hi − logit μ_lo = 2u` and (optimal mean) slope `= τφ′(m̄)`: the optimal
profile is the cone law in the effective field `−φ′` of its own type — the stationary point of the convex cone functional
`MI + I + uρ`.  This, and the fact that the optimal exit is coordinatewise beyond it, is the sketch of "`=`" in (d).)
*Proof of (c).*  Each `φ_{μ,γ}` is concave in `t` (a minimum of affine functions), `φ(0) = 0` (take `ν` constant), and Lipschitz
with the constant `L₀ := u + sup|λ_γ| + ln 2 + sup I`; `φ_{μ,γ}(1) ≤ MI(μ) + λ_γ(μ̄) − α(μ) = (λ_γ − I)(μ̄) ≤ 0` (take `ν = μ`).  So
`F*(0) = 0`, `F*(1) ≤ 0`, `F* ≤ L₀(1 − t)`, `F* ≤ L₀t`, and `F*` is continuous (supremum of an equi-Lipschitz family).  `F*(1) ≥ 0`: a
one-block profile at the type where `λ_γ` touches `I` has `φ(1) = min_κ′[u|κ′ − μ̄| + λ_γ(κ′)] − I(μ̄) = 0`.  `E > 0`: two equal blocks
with types `κ₀ ± η` around a minimum `κ₀` of `I` have `α = O(η²)` while every constant `ν` is at distance `≥ η`, so
`φ(t) ≥ t(uη − O(η²))`.  `R_H(e) = sup_μ V(μ, e + α; v) = sup_μ sup_{τ≥0}max_γ[φ_{μ,γ}(τ) − τe]` by (a), the supremum over the admissible profiles
(`e + α(μ) ≥ v(μ̄)`; all of them if `e ≥ 0`); for `τ ≥ 1` and an admissible profile the bracket is at most
`MI(μ) + (λ_γ(μ̄) − e − α(μ)) ≤ −e = F*(1) − e` (take `ν = μ`; `λ_γ(μ̄) − e − α(μ) ≤ 0`).  Hence `R_H ≤ R̂`, `−e ≤ R̂`, and `R_H = R̂` for `e ≥ 0`.  Non-adaptive side: `MI(ν) + u·dist + v − α(μ) ≤ X` is strictly feasible at `ν = μ`
(`= −(I − v)(μ̄) ≤ 0 < X`), so `n_μ(X) = sup_{t≥0}min_ν[(1+t)MI + t(u·dist + v − α − X)] = sup_{0≤τ<1}(max_γφ_{μ,γ}(τ) − τX)/(1−τ)` with
`τ = t/(1+t)`, and `N(X) = sup_{τ<1}(F*(τ) − τX)/(1−τ) =: θ*`, attained at some `τ* < 1`; then `F*(τ) − τ(X − θ*) ≤ θ*` on `[0,1]` with
equality at `τ*`, i.e. `R̂(X − θ*) = θ*` and `Ŝ(X − θ*) = X` — the argument of Theorem F2(e).  ∎
*Proof of (d), "`≤`".*  Let `z*` minimise the cone functional for the centre type `m` (`Λ_m = α(z*) + uρ(z*)`).  By the triangle
inequality `u·dist(ν, z*) − α(z*) ≥ uρ(ν) − Λ_m`, so `{u·dist(·,z*) + λ − α(z*) ≤ e} ⊂ {uρ + λ − Λ_m ≤ e}` and `r_{z*}(e)` is at least the
`m`-th term of `R_cone(e)`.  ∎
*Proof of (e).*  Concave `φ` is the lower envelope of its tangents, `φ(κ) = min_θ[θκ − φ_*(θ)]`, and
`θκ − h(κ) = KL(κ‖p_θ) − ln(1+e^{−θ})` (`logit p_θ = −θ`): `I = min_θ[KL(·‖p_θ) + c(θ)]`, with equality at `θ = φ′(κ)`.  Hence for every
`μ, ν` and `p₀ := p₀(μ̄)`: `I(ν̄) − I(μ̄) ≤ KL(ν̄‖p₀) − KL(μ̄‖p₀)`, so the feasible set of `r_μ(e)` contains that of the field `p₀` and
`r_μ(e) ≤ r_μ^{field p₀}(e) ≤ R^max_{p₀}(e)` (Lemma SL of Theorem 11.63: in the field case the supremum over all `P_{UX}` is `R^max`);
`R^max_p ≤ R^max_{½}` by Proposition 11.65(b).  Conversely let `I` be convex and symmetric and `μ*` the optimal profile of the
uniform cube (`m = ½`, `a = b = p_u`).  The feasible set `{u·dist(ν,μ*) + I(ν̄) ≤ e + α(μ*)}` is convex and invariant under the
reflection `(ν₁, ν₀) ↦ (1 − ν₀, 1 − ν₁)` (which fixes `μ*`, `dist`, `MI` and maps `ν̄ ↦ 1 − ν̄`), and `MI` is convex, so there is a
minimiser of type `½`; on type `½` the constraint is `u·dist(ν,μ*) ≤ e + MI(μ*)`, the uniform cube's; the same holds on the
uniform cube.  So `r_{μ*}(e) = R_unif(e)` and `R_H ≥ R_unif`.  ∎

**Proposition T10 [proved] (Proposition 11.65(c) carries over verbatim).**  The type-stratified two-sample bracket (per type
class: threshold at the `K`-th largest weight of one sample, truncated mean over a second, tail = maximum over sets of bounded
type-wise density) is valid on all of `L_u`, and with doubling and adaptive stopping its cost at **every symmetric instance** is
within `16(n+1)K/(1−2δ)` of the least cost of any correct algorithm at that instance at accuracy `ε − ln 3`.  (Its proof uses
`A = Σ_t p_tE_{T_t}w` and Theorem T2 only.)  In particular an algorithm without a hint reaches the exponent `R_H` at `H` and `R_λ`
at every symmetric instance, for every exchangeable `π` — one phase or two.

### 5.2 Step of §11.20 → what it uses → verdict for a function-of-type known part with convex `I`

| step of §11.20 | what it uses | verdict |
|---|---|---|
| 11.59(a) lower bound `(1−2δ)e^{−tε+nF(γ,t)}`, every `n` | Theorem 11.27(c): random product centre, `Λ(Φ) = 0`, `ρ_t(M)ⁿ` — **product structure** | **needs change**: every-`n` bound with a polynomial factor, `(1−2δ)(n+1)^{−2}e^{n·min MI}` (Theorems T2, T3(a)); the clean product form is lost |
| 11.59(a) hinted cost `e^{nR_γ+o(n)}` | Theorem A of workstream A (types, product `π`) | **carries over** (Theorem T3(b), sampler `½μ + ½`type-uniform) |
| 11.59(b) closed form of `F(γ,t)` (2×2 game, cosh form) | additivity of the soft gap `Λ_m` in the sites | **fails**: `Λ_m` is not affine in `m`; `F*(t)` is a supremum over two-point profiles (variational; computed numerically) |
| 11.59(c) max–min forms | minimax in the centre law (`F2(a)`) | **hold** as the cone formulas with `Λ_m := min_z[MI + I + uρ]`: `≤` proved, `=` numerical (T9(d)); the sup–min forms are proved |
| 11.59(d) `R^max > R_0` for `p ≠ ½` | derivative of the closed form | **not re-proved**; numerically `R_H > R_0` whenever `B ≠ 0`, `=` at `B = 0` |
| Lemma 11.60 (shift identity) | `π_s` is a product measure | **replaced** by the definition `J_m = MI + I + uρ − Λ_m` and the triangle inequality of Theorem T8(a): non-adaptive rate `= MI +` hinted accuracy at `H`, along geodesics through the Gibbs shell |
| 11.61(a), (b) | permutation symmetry only | **carry over verbatim**, every `n` (Theorem T1) |
| 11.61(c) truncated cones | counting; log-concavity of hypergeometric shells | **carries over**, with a shorter proof and for cones around shells (Theorem T5) |
| 11.61(d) upper bound | Theorem 11.63; `nv` = inf-convolution | **carries over** (Theorem T8(c)) |
| 11.61 product samplers are worse | product samplers | **not examined** |
| Lemma 11.62 (tail lemma relative to a reference) | nothing about `π` | **carries over verbatim** |
| 11.63: Lemma T | a product measure | **needs change**: applied inside one type class with `Bernoulli(κ)ⁿ` (T3(b), Step 2) |
| 11.63: Lemma SL | `v = max_γ v_γ`, Sion; Donsker–Varadhan against the product law `π_γ`; vertices; window step | **replaced**: collapse to additive instances by Sion (T9(a)); the Donsker–Varadhan/vertex step by the concave-envelope argument (T9(b)); the window step by Lemma T7 (no convexity) |
| 11.63: Steps 1–6 | `π` only through `α = D(P_{X\|U}‖π\|P_U)` and `μ_H ≥ Qⁿ` on a typical set | **carry over**; Step 6 is simpler for the type-uniform measure |
| 11.64, lower bound | 11.59(a) at `γ*` | **carries over** (T3(a) at `H` or `γ*`) |
| 11.64 (i): one more level relative to `H` (F7) | `π = π_o ⊗ π_i`; fibres stay in the class; fibre averages Lipschitz relative to the reference; additivity of `d` over blocks | **fails as it stands** (§8.1): the conditional law of a block depends on the type of the other block, and fibre averages are Lipschitz only with a larger constant |
| 11.64 (ii): the pair (F8) | convex analysis of a game function | **carries over** (T9(c)); Theorem 11.66 applies |
| 11.64 (iii): levels | abstract recursion | would carry over given (i) |
| 11.65(a) | closed form | numerical |
| 11.65(b) a field always helps | closed form, ODE | **not re-proved**; used as an input in T9(e), which extends "the uniform cube is the hardest case" from fields to all ferromagnets; for antiferromagnets numerical (§5.3: never above the uniform cube) |
| 11.65(c) stratified bracket, instance-optimal at symmetric instances | permutation symmetry only | **carries over verbatim** (T10) |

So for convex `I`: Theorems 11.59 (without the closed form), 11.61, 11.62, 11.63 hold with `KL(·‖p)` replaced by `I` and `ln Z_γ` by
the Legendre transform `I*(−γ)`; additive instances are still the hardest (among symmetric ones, and equal to `H`); there is a
game function, so Theorem 11.66 applies.  **Theorem 11.64 — the adaptive exponent without a hint — is not obtained:** the lower
bound `R_H` holds, the nested algorithm does not transfer.  For ferromagnets there is a way round it (Proposition T12, §8.2).


### 5.3 Numbers for Curie–Weiss with one phase (`u = 1`; `t02`)

*Checks* (`t02 check`; `(βJ, βB, u) = (0.5, 0, 1), (0.5, 0.3, 1), (0.9, 0.2, 2), (−1, 0.3, 1), (1, 0.1, 1)`, each at `e = 0` and `e = 0.3E`):
sup–min over binary centres `=` cone formula `=` `max_γ R_γ` (cone formula with `λ_γ`; and the sup–min at `γ*`) to `≤ 6·10⁻¹²` in all ten
cases; pair identity `n_{μ*}(e + R_H) = R_H` to `≤ 3·10⁻¹³`; the truncated cone at the centre type of the dip within `4·10⁻⁶`
(it is not re-optimised over the centre type); **with `R_0` in place of `R_H` the identity fails** whenever `B ≠ 0`
(e.g. `(0.5, 0.3, 1)`, `e = 0`: `θ_na(R_0) = 0.025286` against `R_0 = 0.022659`; `(1, 0.1, 1)`: `0.036508` against `0.020271`).

*Table* (cone formulas; `R_H(0⁺)` = exponent of `H` = of the hardest additive instance `γ*|x|` = hinted exponent of the class at
vanishing extensive accuracy; `R_0` at the zero residual; `E` the thresholds; `a = θ_na(0⁺)`; uniform cube: `0.029139`, `0.120115`,
`0.110944`; `max_γ R_γ − R_H` between `−6·10⁻¹²` and `2·10⁻¹²` in all 24 rows):

| `βJ` | `βB` | minimum of `I` | `R_H(0⁺)` | `γ*` | `R_0(0⁺)` | `E_H` | `E_0` | `a` |
|---|---|---|---|---|---|---|---|---|
| `−2` | `0` | `0.5000` | `0.029139` | `0` | `0.029139` | `0.120115` | `0.120115` | `0.110944` |
| `−2` | `0.1` | `0.5167` | `0.029107` | `−0.0023` | `0.029107` | `0.119980` | `0.119976` | `0.110825` |
| `−2` | `0.3` | `0.5499` | `0.028853` | `−0.0067` | `0.028852` | `0.118903` | `0.118873` | `0.109879` |
| `−2` | `0.6` | `0.5996` | `0.028004` | `−0.0128` | `0.027999` | `0.115305` | `0.115198` | `0.106707` |
| `−1` | `0` | `0.5000` | `0.029139` | `0` | `0.029139` | `0.120115` | `0.120115` | `0.110944` |
| `−1` | `0.1` | `0.5250` | `0.029069` | `+0.0006` | `0.029069` | `0.119817` | `0.119816` | `0.110680` |
| `−1` | `0.3` | `0.5747` | `0.028509` | `+0.0023` | `0.028509` | `0.117461` | `0.117448` | `0.108581` |
| `−1` | `0.6` | `0.6477` | `0.026676` | `+0.0068` | `0.026675` | `0.109760` | `0.109725` | `0.101691` |
| `0` (field) | `0` | `0.5000` | `0.029139` | `0` | `0.029139` | `0.120115` | `0.120115` | `0.110944` |
| `0` | `0.1` | `0.5498` | `0.028889` | `+0.0224` | `0.028874` | `0.119081` | `0.119053` | `0.109993` |
| `0` | `0.3` | `0.6457` | `0.026984` | `+0.0658` | `0.026859` | `0.111197` | `0.110970` | `0.102732` |
| `0` | `0.6` | `0.7685` | `0.021603` | `+0.1227` | `0.021258` | `0.088956` | `0.088329` | `0.082233` |
| `0.5` | `0` | `0.5000` | `0.029139` | `0` | `0.029139` | `0.120115` | `0.120115` | `0.110944` |
| `0.5` | `0.1` | `0.5975` | `0.028497` | `+0.0831` | `0.028214` | `0.117508` | `0.116706` | `0.108450` |
| `0.5` | `0.3` | `0.7504` | `0.023983` | `+0.2147` | `0.022659` | `0.099123` | `0.095345` | `0.091019` |
| `0.5` | `0.6` | `0.8756` | `0.014766` | `+0.2756` | `0.013600` | `0.061115` | `0.058034` | `0.055897` |
| `0.9` | `0` | `0.5000` | `0.029139` | `0` | `0.029139` | `0.120115` | `0.120115` | `0.110944` |
| `0.9` | `0.1` | `0.7508` | `0.027960` | `+0.1911` | `0.023512` | `0.115301` | `0.101575` | `0.106395` |
| `0.9` | `0.3` | `0.8757` | `0.018824` | `+0.5496` | `0.013946` | `0.078260` | `0.061194` | `0.071099` |
| `0.9` | `0.6` | `0.9422` | `0.007850` | `+0.3377` | `0.006977` | `0.032584` | `0.030209` | `0.029622` |
| `1.0` | `0` | `0.5000` | `0.029139` | `0` | `0.029139` | `0.120115` | `0.120115` | `0.110944` |
| `1.0` | `0.1` | `0.8059` | `0.027964` | `+0.2000` | `0.020271` | `0.115250` | `0.090246` | `0.106465` |
| `1.0` | `0.3` | `0.9004` | `0.018578` | `+0.6000` | `0.011587` | `0.076438` | `0.051103` | `0.070711` |
| `1.0` | `0.6` | `0.9531` | `0.006441` | `+0.3333` | `0.005742` | `0.026718` | `0.024860` | `0.024313` |

Reading.  (1) **`B = 0`: every row is the uniform cube**, for all couplings `−2 ≤ βJ ≤ 1` (proved for `0 ≤ βJ ≤ 1`; numerical for
the antiferromagnets, also at `βJ = −8, −40`, with the maximum over centre types at `m = ½`: `t18`): *an interaction without a field changes no exponent.*  (2) **With a field every
exponent is below the uniform cube's** (proved for `βJ ≥ 0`), `R_H > R_0` strictly, and the hardest additive residual works against
the field (`γ* > 0` for `B > 0`, i.e. it penalises the favoured letter; the exception in sign is `βJ = −2`, where `|γ*| ≤ 0.013` and
`R_H − R_0 ≤ 5·10⁻⁶`).  The row `βJ = 0` is the field case of §11.20 (`θ = −2βB`) and agrees with the table of F_REPORT §3.7.
(3) **Near the critical coupling the gap between `H` and the zero residual becomes large**: at `βJ = 1`, `βB = 0.1` the zero residual
has `0.0203`, the class `0.0280`, and `γ* = 0.2000 = 2βB` — *the hardest additive residual cancels the field exactly* (also at
`βB = 0.3`: `γ* = 0.6000`; at `βB = 0.6` it cannot, `2βB > u`), which brings the instance back to the critical zero-field model; it is
then not the uniform cube (`0.02796 < 0.02914`) only because the slack around `γ*|x|` is asymmetric (`u ∓ γ*`).  A known part with
a strong susceptibility makes "instance-optimal at `g = 0`" and "worst case over the class" differ by 38 % here.
(4) Ferromagnetic coupling at fixed field lowers the exponents (the field is amplified), antiferromagnetic coupling raises
them towards the uniform cube.

## 6. G3 — non-convex `I` (two phases)

Main example: Curie–Weiss, `βJ = 1.5`, `B = 0`, `u = 1`: wells at `κ = 0.07072` and `0.92928`, barrier `I(½) = 0.115194`, largest slope of
the barrier `0.4151 < u`, contact set `{v = I} = [0.0203, 0.9797]` (one piece: the flat-histogram instance lifts the whole barrier).
Uniform cube for comparison (`u = 1`): `R_unif(e) = KL((Λ₁+e)/u‖½)`, `R_unif(0) = 0.0291391`, `a_unif = KL(p_u‖½) = 0.110944`,
`E_unif = ln cosh(½) = 0.120115`.

### 6.1 What is proved at type level, for every `I`

Everything of §§3–4: (i) the dip exponent of `H` — the exponent of *all* algorithms at `H`, hinted or not — is `R_H(e) = sup_μ r_μ(e)`
over all block profiles (Theorem T3: lower bound for every `n`, upper bound by types); (ii) `H` is the hardest symmetric
instance (Theorem T4, every `n`); (iii) non-adaptive algorithms: the type-stratified sample is optimal up to a polynomial
factor for every `n` (T1); their exponent is squeezed between `N` (truncated shell-cones, T5, T8(a)) and the sheared tail
function of `H` (T8(c)), and equals `R_H∘S^{−1}` where the witness condition of T8(b) holds — numerically at every point computed
with `u ≥ 0.35` (the exception, `u = 0.3`, is discussed in §6.5); `R_H` is 1-Lipschitz with a nondecreasing shear (Lemma T8′);
(iv) for ferromagnets `R_H ≤ R_unif` (T9(e)).  What the theorems do **not** give is the value of the supremum in (i).  For convex
`I` it is attained at a binary centre and equals the cone formula (T9).  For two phases neither is true:

### 6.2 Numbers: cones fail, shells at the barrier restore the pair identity, and beyond `e₀` not even one centre suffices

*The brief's quantity.*  The dip exponent of `H` "from its definition" in O3 — `max_m sup{θ : max_{z∈𝒫_θ}min_{z′∉𝒫_θ}G(z,z′) ≥ e}`,
`G(z,z′) = −MI(z) − I(κ_z) + u·dist(z,z′) + v(κ_{z′})`, `𝒫_θ = {MI ≥ θ}` — is `R_H^{(2)}(e)` for `e ≥ 0`: both are
`sup{θ : ∃z ∀z′ [MI(z′) < θ ⟹ G(z,z′) ≥ e]}` up to closure (for `e ≥ 0` the requirement `z ∈ 𝒫_θ` is automatic, because `G(z,z) ≤ 0`);
the sets `{MI ≥ θ}` are the largest sets of a given density exponent around a centre, the single-letter sets `{u·dist(·,μ) + v < B}`
are the neighbourhoods of the Gibbs shell inside them, and the two have the same exponents (numerically: cross-check (ii) below).

**(A) Binary centres** (`t04`, `t09`; inner solver by clipping, outer by Nelder–Mead from 8–12 starts that agree to `10⁻⁹`;
cross-checks at the end of this subsection and in §6.3).  `R^{(2)} := R_H^{(2)}`; the optimal profile is always the symmetric shell `m = ½`, `a = b = x` in the
barrier type class.

| `e` | `R^{(2)}(e)` | shell `x` | `R_cone(e)` | `R_0(e)` (zero residual) | `S = e + R^{(2)}` | `n_{μ*}(S)` | shell-cone at `S`, direct | cone at `S` | `R_unif(e)` |
|---|---|---|---|---|---|---|---|---|---|
| `−0.100` | `0.1002547` | `0.2707` | | | `0.0002547` | `0.1002547` | | | `0.1003020` |
| `−0.070` | `0.0734665` | `0.2762` | | | `0.0034665` | `0.0734665` | `0.0734665` | `0.0224380` | `0.0741382` |
| `−0.050` | `0.0575961` | `0.2821` | | | `0.0075961` | `0.0575961` | `0.0575961` | `0.0145149` | `0.0590497` |
| `−0.030` | `0.0433283` | `0.2880` | | | `0.0133283` | `0.0433283` | `0.0433283` | `0.0082501` | `0.0457715` |
| `−0.010` | `0.0307336` | `0.2945` | | | `0.0207336` | `0.0307336` | `0.0307336` | `0.0036716` | `0.0342525` |
| `0` | **`0.0251012`** | `0.29803` | `0.0107007` | `0.0087471` | `0.0251012` | `0.0251012` | `0.0251012` | `0.0020379` | `0.0291391` |
| `0.005` | `0.0224601` | `0.29984` | `0.0082856` | `0.0065951` | `0.0274601` | `0.0224601` | `0.0224601` | `0.0013924` | `0.0267419` |
| `0.010` | `0.0199399` | `0.30170` | `0.0061622` | `0.0047744` | `0.0299399` | `0.0199399` | `0.0199399` | `0.0008645` | `0.0244503` |
| `0.020` | `0.0152765` | `0.30553` | `0.0028153` | `0.0020627` | `0.0352765` | `0.0152765` | `0.0152765` | `0.0001771` | `0.0201820` |
| `0.030` | `0.0111431` | `0.30951` | `0.0007265` | `0.0005013` | `0.0411431` | `0.0111431` | `0.0111431` | `0` | `0.0163303` |
| `0.040` | `0.0075779` | `0.31365` | `0` | `0` | `0.0475779` | `0.0075779` | `0.0075779` | `0` | `0.0128922` |
| `0.050` | `0.0046265` | `0.31795` | `0` | `0` | `0.0546265` | `0.0046265` | `0.0046265` | `0` | `0.0098646` |
| `0.064` | `0.0016308` | `0.32422` | | | `0.0656308` | `0.0016308` | | | `0.0063110` |

Reading.  (1) **O3 confirmed and made precise:** at `e = 0` the cone formula gives `0.01070`, the best dip around a single centre
`0.025101` (the coordinator's `0.026` was a grid value; mine is accurate to `10⁻⁷` by three methods), the zero residual `0.00875`.
The optimal dips have their Gibbs shell in the barrier type class at distance `xn ≈ 0.30n` from the centre — slightly outside the
uniform cube's `p_u n = 0.269n` — and their two cheapest exits are *asymmetric*: only the coordinates on one side of the centre
are moved, towards one well (exit type `κ′ = 0.407` or `0.593`).  The cone's own Gibbs shell sits in a well (`κ = 0.139`), which
is why the cone formula describes a different, much less effective, dip.  (2) **Pair identity:** `n_{μ*}(e + R^{(2)}(e)) = R^{(2)}(e)`
to `≤ 7·10⁻⁹` at all 44 accuracies of the table file (`−0.108 ≤ e ≤ 0.064`), and the direct two-dimensional evaluation of the
truncated shell-cone around `μ*` gives the same numbers; the truncated *cone* gives `0.0020` at `S(0)` — a factor 12 off.  On the table
`R^{(2)}` is convex with slopes between `−0.98` and `−0.18`, and `S` is increasing — the properties of a `HintPair`, here numerical.
(For `e > e₀` the rows are those of the binary family — lower bounds; the larger values of (B) come with their own shells and
satisfy the identity as well.)  (3) `a = θ_na(0⁺)`: the shells `(½; x, x)` are globally
self-consistent for every `x ≥ p_u` (`𝒱 = α` to `10⁻¹⁵`), so `a ≥ KL(p_u‖½) = 0.110944`, and `a ≤ a_unif` by T9(e): **`a = a_unif = 0.110944`**,
against `0.0446` from cones.  At vanishing accuracy a non-adaptive sample needs the uniform cube's exponent; the function that
shows it is the cone around the sphere-in-the-barrier-slice of radius `p_un`.

**(B) More than one block is needed for `e > e₀`** (`t03`, `t13`, `t15`).  Searches over profiles with 3, 4, 5 blocks (differential
evolution and Nelder–Mead from split and perturbed binary optima; the symmetric families `S3 = {1−x, ½, x}` with a *free block*
of weight `λ_f` at type `½`, `S4 = {1−x, ½±d, x}`, `S5`, `S6` with 5 and 6 atoms; general asymmetric refinements):

| `e` | binary `S2` | `S3` | `S4` | `S5` | `S6` | best found | gain | structure of the best | `R_unif(e)` |
|---|---|---|---|---|---|---|---|---|---|
| `≤ 0` | optimum | — | — | — | — | binary | `0` | all searches collapse to the binary shell | |
| `0` | `0.02510117` | `0.02499323` (local) | `=S2` | `=S2` | | `0.02510117` | `0` | binary | `0.0291391` |
| `0.002` | `0.02403044` | `0.02404192` | `=S3` | `=S3` | | `0.02404192` | `+0.05 %` | `λ_f = 0.140`, `x = 0.2715` | `0.0281676` |
| `0.004` | `0.02297873` | `0.02310502` | `=S3` | `=S3` | `=S3` | `0.02310502` | `+0.55 %` | `λ_f = 0.140` | `0.0272129` |
| `0.010` | `0.01993989` | `0.02038167` | `=S3` | `=S3` | `=S3` | `0.02038167` | `+2.2 %` | `λ_f = 0.140`, `x = 0.2744` | `0.0244503` |
| `0.020` | `0.01527650` | `0.01615476` | `=S3` | `=S3` | `=S3` | `0.01615476` | `+5.7 %` | `λ_f = 0.141`, `x = 0.2774` | `0.0201820` |
| `0.030` | `0.01114307` | `0.01235769` | `=S3` | `0.01235416` | `=S3` | `0.01235769` | `+10.9 %` | `λ_f = 0.144`, `x = 0.2798` | `0.0163303` |
| `0.040` | `0.00757788` | `0.00902000` | `0.00914040` | `0.00906937` | `0.00914026` | `0.00914040` | `+20.6 %` | atoms `0.273, 0.430, 0.570, 0.727`, weights `0.396, 0.104, 0.104, 0.396` | `0.0128922` |
| `0.050` | `0.00462647` | `0.00616685` | `0.00638210` | `0.00638667` | `0.00638206` | `0.00638667` | `+38 %` | atoms `0.270, 0.388, ½, 0.612, 0.730` | `0.0098646` |
| `0.060` | `0.00234304` | `0.00382224` | `0.00408808` | `0.00415064` | `0.00415156` | `0.00415156` | `+77 %` | six atoms `0.270 … 0.730` | `0.0072450` |

(`=S3`: the larger family returns the `S3` optimum.)  The binary branch and the diluted branch are two local maxima that cross
at **`e₀ = 0.00181`** (`t15`); the free block appears with a finite weight (`λ_f ≈ 0.14`), not continuously.  Every entry is a proved
lower bound for every algorithm at `H` (T3(a)); the inner minima at four of the optima (`e = 0`, `0.02`, `0.04`, `0.05`; 2, 3, 4, 5 blocks) were confirmed by a random
search over *all* exit profiles with `I` in the constraint (no clipping lemma, no table of `v`; `t17`): `0.0251013`, `0.0161556`,
`0.0091401`, `0.0063885` (upper bounds of the minimum) against the clipping values `0.0251012`, `0.0161545`, `0.0091397`, `0.0063860`.
The pair identity holds at the multi-block optima as well (`n_μ(e+R) − R ≤ 3·10⁻⁸`; the shells are then cones around the class
"profile `x` on 86 % of the coordinates, anything of density `½` on the rest").
*Mechanism* **[local computation proved, §6.7; the rest a sketch]**.  Take the uniform cube's dip on a fraction `1 − λ_f` of the
coordinates and leave the rest free.  (i) Its symmetric exit has the value `(1−λ_f)R_unif(e/(1−λ_f)) ≤ R_unif(e)` — the loss from
convexity.  (ii) A shift `t` of the constrained type moves the total type by `(1−λ_f)t` only, so the destabilising curvature
`2(βJ − 1)` of the landscape is multiplied by `1 − λ_f`; and (iii) the density exponent of type-shifted exits gains `2λ_ft²`
(concavity of the entropy of mixing).  Together: the symmetric exit of the diluted dip is locally stable up to the coupling
`βJ_stab(λ_f) = 1 + u(c₂ + 2λ_f)/(2L(1−λ_f))` instead of `βJ* = 1 + uc₂/(2L)` (§6.7).  At `βJ = 1.5`, `e = 0.02` the weight that makes the
symmetric exit marginal is `0.132`; the optimum found has `λ_f = 0.141` and the value `0.016155`, against
`(1−λ_f)R_unif(e/(1−λ_f)) = 0.01621`: the diluted centre is, up to the tie with exits far from the symmetric one, a uniform-cube dip
on 86 % of the coordinates.
*Consequences.*  **For `e > e₀` the exponent of `H` is not the brief's `R_H` "from its definition" (sets `{MI ≥ θ}` around one centre)
but larger; I do not know its value**, only `best found ≤ R_H(e) ≤ R_unif(e)` (last column).  The gains from the fifth and sixth
atom are `10⁻⁵`–`10⁻⁶`, which suggests — and does not prove — that the best found values are within about `10⁻⁵` of the supremum
for `e ≤ 0.05`.  At vanishing accuracy (`e → 0⁺`, and for the whole tail function at `e ≤ 0`) the binary shell is optimal in every
search (3 blocks: differential evolution and six Nelder–Mead starts; 4 blocks: the same; the structured families with up to
6 atoms and their asymmetric refinements with up to 5 blocks), and I state `R_H(0⁺) = 0.0251012`
as **[numerical]** with the bracket `[0.0251012, 0.0291391]` **[proved]**.

*Cross-checks of (A), (B)* (`t12`, `t04` with differential evolution, exact sums in §6.3).  (i) The inner minimum on full grids
of exit profiles (`2001²` for two blocks, `181³` for three; with `v` and with `I` in the constraint — identical, Lemma T7): the
grid value is never below the clipping value and within the grid resolution of it (`≤ 10⁻⁴`, `≤ 3·10⁻⁴`).  (ii) The brief's
definition of the dip exponent (sets `{MI ≥ θ}` around a centre of type `m`, `ℓ¹` distance transform on a `1001²` grid of `(a,b)`):
`0.02527` at `m = ½` and `0.02443` at `m = 0.45`, against the sup–min `0.0251012` and `0.0243744` — the grid values decrease towards
the sup–min as the grid is refined (the coordinator's `0.0261`, `0.0255` are the same quantity at `161²`, `241²`).  (iii) `n_μ` by the
two solvers at ten random profiles: `3·10⁻⁹`.  (iv) Differential evolution over `(m, a, b)` (Sobol start, 60 generations): `0.0251012` at `(0.5000, 0.2979, 0.2981)` for `e = 0` and
`0.0152765` at `(0.4999, 0.3054, 0.3056)` for `e = 0.02` — the Nelder–Mead values.

### 6.3 G1(b)/G3(b) — exact finite-`n` sums (every number is a certified bound on a cost)

`t06` (two blocks, `tfin.py`), `t14` (2–4 blocks, `kfin.py`).  *Dips:* for a centre of type `k`, the density-capped set `D_q` (in every
type class the rarest profile classes on the side of the centre, as long as their cumulative density stays `≤ q`) with the
smallest `q` such that `ln(1 + Φ(D_q)) > ε`; then **every** algorithm that is `(ε/2, δ)`-correct on `L_u` makes at least
`(1 − 2δ)/maxdens(D_q)` evaluations at the instance (Theorem T2); reported `θ_n = ln(1/maxdens)/n`.  *Non-adaptive:* the smallest `q`
with `ln[A(ψ)/A(ψ^{tr,q})] > ε` for the shell-cone `ψ = u·d(·, C)`; then every non-adaptive algorithm makes at least `(1 − 2δ)/q`
evaluations (Theorems T1, T5); reported `θ_n = ln(1/q)/n`.

*Two phases* (`βJ = 1.5`, `B = 0`, `u = 1`, centre type `n/2`):

| quantity (limit) | `n = 250` | `500` | `1000` | `2000` | `4000` | single-letter value |
|---|---|---|---|---|---|---|
| dips of `H`, `ε = 1` (`e → 0`) | `0.025153` | `0.025159` | `0.025092` | `0.025084` | `0.025087` | `R^{(2)}(0) = 0.025101` |
| dips of `H`, `ε = 0.01n` | `0.021496` | `0.020648` | `0.020290` | `0.020125` | `0.020032` | `R^{(2)}(0.01) = 0.019940` |
| shell-cone `x = 0.298`, `ε = 0.0251012n` (pair identity at `e = 0`) | `0.031466` | `0.029510` | `0.027977` | `0.026820` | `0.026060` | `N(S(0)) = 0.025101` |
| cone around the centre, same accuracy | `0.009928` | `0.006401` | `0.004471` | `0.003405` | `0.002813` | `0.002038` |
| shell-cone `x = 0.2847`, `ε = 0.01n` | `0.057110` | `0.055362` | `0.053970` | `0.052906` | `0.052181` | `N(0.01) = 0.050929` |
| shell-cone `x = p_u`, `ε = 1` (vanishing accuracy) | `0.080237` | `0.088650` | `0.094517` | `0.098416` | `0.101742` | `a = 0.110944` |
| cone around the centre, `ε = 1` | `0.044316` | `0.043780` | `0.043490` | `0.043401` | `0.043512` | `a_cone = 0.0446` |

So at `n = 4000` and bounded accuracy every algorithm needs `(1−2δ)e^{0.02509n}` evaluations at `H`, and every non-adaptive
algorithm `(1−2δ)e^{0.1017n}` — the second number certified by a cone around a shell; cones around points certify `e^{0.0435n}`.
The sums approach the single-letter values with differences between `0.05` and `0.6·ln n/n`, except at bounded accuracy for the
non-adaptive bound, where the difference is still `4.4·ln n/n` at `n = 4000` (slow, as in §11.16).

*Beyond one centre* (`ε = 0.05n + 1`; single-letter values `R^{(2)} = 0.004626`, `S3`: `0.006167`, `S4`: `0.006382`):

| family of sets | `n = 150` | `300` | `600` | `1200` | limit |
|---|---|---|---|---|---|
| best density-capped set around one centre of type `n/2` | `0.005588` | `0.005382` | `0.005197` | `0.005027` | `0.004626` |
| budget neighbourhood of the binary optimum `S2` (`x = 0.318`) | `0.003754` | `0.004350` | `0.004638` | `0.004607` | `0.004626` |
| budget neighbourhood of the three-block class `S3` (`λ_f = 0.155`, `x = 0.284`) | `0.004372` | `0.005436` | `0.005730` | | `0.006167` |
| budget neighbourhood of the four-block class `S4` | `0.005091` | `0.005593` | | | `0.006382` |

From `n = 300` on the three-block set certifies more than the best capped set around one centre (`e^{0.00573·600}` against
`e^{0.00520·600}` at `n = 600`), and the two sequences move apart, as the single-letter values say.  (This is not a certified
*separation*: the capped family is the natural maximal family around one centre, not provably the best one at finite `n`.)

*One phase with a field* (`βJ = 0.5`, `βB = 0.3`, `u = 1`, `ε₁ = 0.3E = 0.029737`, centre type `0.4282`) and the *field control* of §11.20
(`p = 0.1`, `u = 2`, `ε₁ = 0.3E = 0.0636884`):

| quantity | `n = 500` | `1000` | `2000` | `4000` | formula |
|---|---|---|---|---|---|
| CW one phase: dips of `H` | `0.014009` | `0.013038` | `0.012458` | `0.012138` | `R_H = 0.011685` |
| CW one phase: truncated cone at `ε₁ = e + R_H = 0.041422` | `0.018046` | `0.015286` | `0.013722` | `0.012825` | `θ_na = 0.011685` (pair identity) |
| field: dips of `H`, centre type `0.5373` | `0.025566` | `0.024697` | `0.024068` | `0.023734` | `R^max = 0.023270` |
| field: dips of `0`, centre type `0.3994` | `0.023324` | `0.021964` | `0.020949` | `0.020255` | `R_0 = 0.019497` |
| field: truncated cone, centre type `0.517` | `0.044177` | `0.040732` | `0.038758` | `0.037646` | `θ_na = 0.036246` |

The field rows reproduce the exact sums of workstream F to all printed digits where the sets coincide (`0.024697`/`0.024068`
against its `.024696`/`.024068`; `0.021964`, `0.020949`, `0.020255` against `.021964`, `.020949`, `.020254`) — with independent code.

### 6.4 G3(a) — other instances: `H` is the hardest symmetric one, and at coexistence no additive instance comes near it

Theorem T4 settles the question for symmetric instances at every `n`; `t11` is the numerical side (binary sup–min, `e = 0`,
`βJ = 1.5`, `u = 1`; `R_H = 0.0251012`):

| family of landscapes `λ ≤ v` | members and their `R_λ(0)` | largest `R_λ − R_H` |
|---|---|---|
| additive instances `γ\|x\|` | `γ = 0`: `0.0087471`; `±0.05`: `0.0082822`; `±0.1`: `0.0078255`; `±0.2`: `0.0069257`; `±0.7`: `0.0025320`; `±1 = ±u`: `0` | `−0.0164` |
| barrier flattened at a level, `λ = min(v, c·max v)` | `c = 0` (zero residual): `0.0087471`; `0.25`: `0.0119733`; `0.5`: `0.0146268`; `0.75`: `0.0175282`; `0.9`: `0.0237693`; `1` (`= H`): `0.0251012` | `−2·10⁻⁹` |
| instances concentrated on the barrier top, `λ = min(v, I(½) − s·u\|κ − ½\|)` | `s = 0.25`: `0.0198907`; `0.5`: `0.0106712`; `0.75`: `0.0040297`; `1`: `0` | `−0.0052` |
| `v` cut by three upward cones with random apices (seed 5), renormalised | `0.0230597`, `0.0248359`, `0.0233942`, and three equal to `R_H` (cuts away from the optimal dip) | `−2·10⁻⁹` |

(i) **The hardest additive instance is the zero residual, with `0.0087471` — 35 % of `R_H(0)`.**  For additive instances binary
centres suffice for every `I` (remark after T9(b)), so this number is the exponent of the best additive instance, and by Sion
`max_γ R_γ = R_{v**}`, the exponent of the landscape `v** = max_γ λ_γ` (the convex envelope: zero between the wells).  The tilted
Gibbs measures `π_γ` of a two-phase known part never concentrate on the barrier, so the "normalised-maximum-likelihood
mixture of the tilted measures" of §11.20, remark (3), is **not** the flat-histogram ensemble here: `μ_H ∝ π·e^{nv}` is flat on the
barrier, `max_γ π_γ` is exponentially small there.  The conjecture of that remark ("an ensemble that is flat in the order
parameter") is right; its derivation from tilted measures is right only for convex `I`.
(ii) Flattening the barrier at a lower level interpolates monotonically between the zero residual and `H`; sharpening the
instance around the barrier top lowers the exponent to zero at the full slope `u` (the roof `u·||x| − n/2|` is determined by
`O(1)` evaluations, §8.3).
(iii) No landscape exceeds `R_H`, as Theorem T4 says.

### 6.5 G3(d) — the slope of the barrier exceeds `u`: the contact set breaks into pieces

At `βJ = 1.5`, `B = 0` the largest slope of `I` on the barrier is `0.41509`, and the largest slope of a chord from the top of
the barrier is `u_top = 0.28153` (the chord to `κ = 0.1183`; the mean slope to the bottom of the well is `0.26834`).  For
`u < 0.41509` the largest `u`-Lipschitz minorant `v` leaves `I` on the flanks (two "roofs" of slope `±u`); for `u < u_top` it leaves
`I` at the top as well: the flat-histogram instance no longer lifts the barrier to the level of the wells, and the barrier
types have `μ_H`-weight `e^{−n(I−v)}`.  **Nothing in Theorems T1–T8 uses the shape of the contact set**, so the statements are
unchanged: `ψ_H = −nv` is the hardest symmetric instance, its exponent is the single-letter supremum, the type-stratified
sample is optimal non-adaptively, shell-cones give the partner.  The numbers (`e = 0`; `t10`, mode U):

| `u` | contact set `{v = I}` | `R_H(0)` | `R_unif(0)` | ratio | optimal Gibbs shell `(m; a, b)` | cone formula | pair residual | `a` from barrier shells / `a_unif` |
|---|---|---|---|---|---|---|---|---|
| `1.00` | `[0.020, 0.980]` | `0.02510117` | `0.02913914` | `0.861` | `(½; 0.2980, 0.2980)` barrier | `0.01070066` | `−3·10⁻¹¹` | `0.110944 / 0.110944` |
| `0.60` | `[0.032, 0.968]` | `0.00907144` | `0.01096292` | `0.827` | `(½; 0.3780, 0.3780)` | `0.00321748` | `2·10⁻⁹` | `0.043053 / 0.043053` |
| `0.45` | `[0.038, 0.962]` | `0.00510767` | `0.00623617` | `0.819` | `(½; 0.4084, 0.4084)` | `0.00174234` | `2·10⁻⁹` | `0.024686 / 0.024686` |
| `0.40` | `[0.041, 0.176] ∪ [0.294, 0.706] ∪ [0.824, 0.959]` | `0.00403676` | `0.00494240` | `0.817` | `(½; 0.4185, 0.4185)` | `0.00136304` | `2·10⁻⁹` | `0.019607 / 0.019607` |
| `0.35` | `[0.044, 0.142] ∪ [0.398, 0.602] ∪ [0.858, 0.956]` | `0.00309137` | `0.00379426` | `0.815` | `(½; 0.4287, 0.4287)` | `0.00103457` | `1·10⁻⁹` | `0.015081 / 0.015081` |
| `0.30` | `[0.047, 0.124] ∪ [0.4745, 0.5255] ∪ [0.876, 0.954]` | `0.00226457` | `0.00279417` | `0.810` | `(½; 0.4409, 0.4409)` | `0.00075446` | **`−2.3·10⁻³`** (see (4)) | `0.006999 / 0.011125` |
| `0.25` | `[0.050, 0.110] ∪ [0.890, 0.950]` | `0.00052346` | `0.00194427` | `0.269` | `(0.537; 0.9085, 0.0576)` in a well | `0.00052067` | `1·10⁻¹³` | none `/ 0.007752` |
| `0.20` | `[0.053, 0.100] ∪ [0.901, 0.947]` | `0.00033264` | `0.00124637` | `0.267` | `(0.529; 0.9135, 0.0597)` in a well | `0.00033154` | `2·10⁻¹⁴` | none `/ 0.004975` |

Reading.  (1) **As long as the top of the barrier is a contact point (`u ≥ u_top = 0.2815`), breaking the window on the flanks changes
nothing qualitative:** the optimal dips are still shells in the barrier type class, the ratio to the uniform cube stays near
`0.81`–`0.83`, the pair identity holds (`≤ 2·10⁻⁹`).  What changes first is the non-adaptive exponent at vanishing accuracy:
barrier shells `(½; x, x)` are self-consistent only for `x ≥ 0.4409` at `u = 0.30` (`a ≥ 0.0070`, against `a_unif = 0.0111`), because a
shell-cone of radius `p_un` now has its Gibbs measure pulled over the roof.  (2) **When the top leaves the contact set
(`u < u_top`) the barrier disappears from the problem:** no profile in the barrier class has a positive value, the optimal dips
sit in a well (centre of type `≈ 0.53`, Gibbs shell at type `≈ 0.08`), the cone formula is correct again to `1 %`, and the exponent
drops to `27 %` of the uniform cube's.  The flat-histogram ensemble is then flat on two pieces around the wells only — the
multicanonical ensemble restricted to what a `u`-Lipschitz residual can make relevant.  (3) The pair identity (in the form: the best shell-cone gives `R^{(2)}` at the accuracy `e + R^{(2)}(e)`) holds in rows 1–5
and in rows 7–8, where it is the one-phase identity around the wells.
(4) **It fails at `u = 0.30`, where the piece of the contact set at the top of the barrier is narrow (`[0.4745, 0.5255]`).**
There the optimal dip profiles are *marginal* shells: `x*(e) = 0.4409, 0.4413, 0.4422, 0.4435, 0.4453` at
`e = 0, 0.0001, 0.0003, 0.0006, 0.001` (`R^{(2)} = 0.0022646, 0.0022079, 0.0020955, 0.0019294, 0.0017129`; slope `≈ −0.56`, nothing
unusual), but `x = 0.4409` is the smallest self-consistent barrier shell: the Gibbs measure of the cone around it is on the
verge of escaping over the roof into a well (`𝒱(μ) = α(μ)` with a second minimiser of `G_μ` in the well).  For such a profile
`r_μ(e′)` drops to zero just above `e` — once a one-sided exit reaches the edge of the piece it slides down the roof at no cost
(`u·dist + v` is constant along a pure change of type where `v` has slope `u`) until the profile is independent of the centre —
so `e′ + r_μ(e′)` is not monotone, `n_{μ*}(e + R^{(2)}(e)) = 0`, and the truncated shell-cone certifies nothing: its truncation
is dominated by the bulk of the well.  The best shell for the non-adaptive bound is a different one (`x = 0.4514`), and
`sup_μ n_μ(S(0)) = 0.0018400 = 0.81·R^{(2)}(0)` over symmetric shells, over general binary profiles and over profiles with a free
block alike (`t16`; `0.0015517` against `0.0019294` at `e = 0.0006`).  So at `u = 0.30` **the non-adaptive exponent at the accuracy
`e + R(e)` is only known to lie in `[0.00184, 0.00226]`**: either functions other than cones around profile classes do better,
or the shear law fails there — the upper bound of T8(c) uses `A(ψ^{tr}) ≥ q·max_t p_tt_t`, which is lossy when a second phase carries
more weight than the classes at the quantile.  I could not decide which (open O5).  At `e = 0.2·ln cosh(u/2)` the same pattern:

| `u` | `e` | binary centre | with a free block | `R_unif(e)` | `n_{μ*}(e + R^{(2)}) − R^{(2)}` |
|---|---|---|---|---|---|
| `1.00` | `0.024023` | `0.0135479` | `0.0145737` (`λ_f = 0.142`) | `0.0185826` | `3·10⁻⁹` |
| `0.45` | `0.005020` | `0.0026726` | `0.0029253` (`λ_f = 0.174`) | `0.0039882` | `1·10⁻⁹` |
| `0.30` | `0.002242` | `0.0010833` | `0.0011083` (`λ_f = 0.142`) | `0.0017877` | `−1.1·10⁻³` |
| `0.25` | `0.001558` | `0.0000348` (in a well) | — | `0.0012440` | `1·10⁻¹⁴` |
(Bookkeeping: at `u = 0.30` the first run of this sweep reported `0.00076` — the well optimum: the multi-start search had no start on the
narrow range of barrier shells with a positive value; the symmetric family found `0.00226`.  The search now includes shells
`(m; x, x)`; the three lowest rows were re-run.)

### 6.6 G3(e) — through the critical coupling: the two-phase exponents do not merely join the convex ones, they coincide with them on an interval

`B = 0`, `u = 1`, `e = 0` (`t10`, mode J; binary sup–min, the symmetric families `S3`, `S4` return the same values at `e = 0`):

| `βJ` | barrier `I(½) − min I` | `R_H(0)` | `R_H/R_unif` | shell `x` | cone formula | `a` from shells |
|---|---|---|---|---|---|---|
| `0.90` | `0` (one phase) | `0.0291391` | `1.00000` | `0.2689` | `0.0291391` | `0.110944` |
| `1.00` | `0` | `0.0291391` | `1.00000` | `0.2689` | `0.0291391` | `0.110944` |
| `1.05` | `0.001768` | `0.0291391` | `1.00000` | `0.2689` | `0.0291391` | `0.110944` |
| `1.10` | `0.006689` | `0.0291391` | `1.00000` | `0.2689` | `0.0291391` | `0.110944` |
| `1.12` | `0.009426` | `0.0291391` | `1.00000` | `0.2689` | `0.0291391` | `0.110944` |
| `1.14` | `0.012560` | `0.0290694` | `0.99761` | `0.2689` | `0.0290694` | `0.110944` |
| `1.15` | `0.014267` | `0.0289496` | `0.99350` | `0.2693` | `0.0289452` | `0.110944` |
| `1.16` | `0.016065` | `0.0288187` | `0.98900` | `0.2703` | `0.0287583` | `0.110944` |
| `1.17` | `0.017950` | `0.0286893` | `0.98456` | `0.2713` | `0.0285086` | `0.110944` |
| `1.18` | `0.019919` | `0.0285614` | `0.98017` | `0.2723` | `0.0281959` | `0.110944` |
| `1.20` | `0.024100` | `0.0283097` | `0.97154` | `0.2742` | `0.0273828` | `0.110944` |
| `1.30` | `0.049250` | `0.0271307` | `0.93107` | `0.2831` | `0.0202239` | `0.110944` |
| `1.40` | `0.080095` | `0.0260672` | `0.89458` | `0.2910` | `0.0144431` | `0.110944` |
| `1.50` | `0.115194` | `0.0251012` | `0.86142` | `0.2980` | `0.0107007` | `0.110944` |
| `1.75` | `0.215442` | `0.0230260` | `0.79021` | `0.3129` | `0.0054940` | `0.110944` |

**Statement.**  Let `ρ := (Λ₁ + e)/u` be the exit radius of the uniform cube, `c₂ := 1/(2ρ(1−ρ)) − 2`, `L := ln((1−ρ)/ρ)` and
`βJ*(e, u) := 1 + u·c₂/(2L)` (`= 1.1250` at `u = 1`, `e = 0`; `→ 1.27` as `e ↓ e_c`).  For the Curie–Weiss model with `B = 0`:
(i) **[proved]** `R_H(e) ≤ R_unif(e)` for every `βJ ≥ 0` (T9(e)), with equality for `βJ ≤ 1`;
(ii) **[proved, local]** at the uniform cube's optimal profile the symmetric exit `(ρ, ρ)` is a strict local minimum of `MI` on
the boundary of the feasible set iff `c₂ + 2(1 − βJ)L/u > 0`, i.e. iff `βJ < βJ*`: along `(a′, b′) = (ρ̄ − t, ρ̄ + t)` the exit type is
`½ + t`, the constraint `(u/2)(a′+b′) + I(½+t) − I(½) = const` with `I(½+t) − I(½) = 2(1−βJ)t² + O(t⁴)` gives
`ρ̄ = ρ − 2(1−βJ)t²/u`, and `MI = MI₀ + t²[c₂ + 2(1−βJ)L/u] + O(t⁴)`;
(iii) **[numerical]** for `1 < βJ ≤ βJ*` that local minimum is global, so **`R_H(e) = R_unif(e)` although there are two phases**
(table: `1.05, 1.10, 1.12`; the first deviation, `0.24 %`, at `1.14`); beyond `βJ*` the symmetric exit is a saddle, the cheapest
exits tilt towards the wells, `R_H < R_unif`, and the optimal shell moves outwards (`x` from `0.269` to `0.313`).
So **the two-phase exponents join the convex ones continuously, and the junction is not at the critical coupling but at
`βJ*(e,u) > 1`**: a barrier that is shallow compared with what a dip gains by staying symmetric is invisible to every exponent.
The transition at `βJ*` is continuous in the value.  At vanishing accuracy the non-adaptive exponent does not change at all:
`a = a_unif` for every `βJ` in the table (the shell `(½; p_u, p_u)` stays globally self-consistent), while the cone formula
degrades to `0.0055`.  Continuity in general: `R_I(e + 2η) ≤ R_{I′}(e) ≤ R_I(e − 2η)` whenever `‖I − I′‖_∞ ≤ η` (the constraint of `r_μ`
moves by at most `2η`) **[proved]**, so the exponents are continuous in the parameters wherever `R_I` is continuous in `e`.

### 6.7 Other couplings, positive accuracy, and a field at coexistence

*The free block as a function of the coupling* (`u = 1`, `B = 0`; `t10` mode J, `t19`).  At `e = 0.02` (`R_unif = 0.0201820`,
`βJ*(0.02, 1) = 1.1029`):

| `βJ` | binary centre | its shell `x` | cone formula | with a free block (`S3`/`S4`) | `λ_f` found | shell of the diluted profile | marginal weight `λ_stab` | best`/R_unif` |
|---|---|---|---|---|---|---|---|---|
| `1.0`, `1.1` | `0.0201820` | `0.2689` | `0.0201820` | `=` | `0` | | — | `1.000` |
| `1.105` | `0.0201808` | `0.2689` | `0.0201808` | `=` | `0` | | `0.0008` | `0.99994` |
| `1.12` | `0.0201047` | `0.2689` | `0.0201047` | `=` | `0` | | `0.0067` | `0.9962` |
| `1.125` | `0.0200527` | `0.2689` | `0.0200527` | `0.0200528` | `< 0.001` | `0.269` | `0.0086` | `0.9936` |
| `1.13` | `0.0199875` | `0.2689` | `0.0199875` | `0.0199960` | `0.002` | `0.269` | `0.0105` | `0.9908` |
| `1.14` | `0.0198350` | `0.2699` | `0.0198170` | `0.0198832` | `0.008` | `0.269` | `0.0143` | `0.9852` |
| `1.15` | `0.0196833` | `0.2711` | `0.0195933` | `0.0197716` | `0.012` | `0.269` | `0.0181` | `0.9797` |
| `1.2` | `0.0189503` | `0.2769` | `0.0176913` | `0.0192108` | `0.034` | `0.269` | `0.0365` | `0.952` |
| `1.3` | `0.0175999` | `0.2875` | `0.0108824` | `0.0181202` | `0.072` | `0.272` | `0.0709` | `0.898` |
| `1.5` | `0.0152765` | `0.3055` | `0.0028153` | `0.0161548` | `0.141` | `0.277` | `0.1316` | `0.800` |

At `e = 0.04` (`R_unif = 0.0128922`, `βJ* = 1.0815`): `1.07`: `= R_unif`; `1.09`: `0.0128766`, no free block; `1.11`: `0.0127162 → 0.0127276`
(`λ_f = 0.004`; `λ_stab = 0.0090`); `1.125`: `0.0124894 → 0.0125908` (`0.010`; `0.0136`); `1.14`: `0.0122477 → 0.0124530` (`0.016`; `0.0182`).

**Where the free block sets in.**
(i) **[proved, local computation]**  For the diluted uniform-cube profile `S3(λ_f, p_u)` the symmetric exit has the value
`(1−λ_f)·R_unif(e/(1−λ_f))`, and along the exits tilted by `t` in the constrained blocks (the free block unmoved — moving it by `s` costs
`uλ_f|s|`, linear)

    MI = MI₀ + (1−λ_f)·t²·A(λ_f) + O(t⁴),      A(λ_f) = c₂ + 2λ_f − 2L(βJ − 1)(1 − λ_f)/u      (c₂, L of §6.6 at the radius ρ(e/(1−λ_f))),

so the symmetric exit is a strict local minimum iff `βJ < βJ_stab(λ_f) := 1 + u(c₂ + 2λ_f)/(2L(1−λ_f))`; `βJ_stab(0) = βJ*`.  The free
block multiplies the destabilising curvature `2(βJ−1)` of the landscape by `1 − λ_f` and adds `2λ_f` from the entropy of mixing
(finite differences on the explicit boundary curve agree with `A` to `10⁻⁶`; at `λ_f = 0.03`, `e = 0.02` the solver returns the diluted
value to `10⁻¹³` up to `βJ_stab` and less beyond; for larger `λ_f` or `e` exits far from the symmetric one undercut it already
slightly below `βJ_stab` — the local minimum is then not the global one; `t19`).  `λ_stab(βJ)` in the table is the weight with `βJ_stab(λ_stab) = βJ`: what it takes to keep a
uniform-cube-like dip on the remaining coordinates from tilting towards a well.
(ii) **[numerical]**  **The free block does not set in at `βJ*` but at a larger coupling `βJ**(e, u)`**: between `1.12` and `1.13` at
`e = 0.02` (no gain at `1.12`, `10⁻⁷` at `1.125`, `λ_f = 0.002` at `1.13`), between `1.09` and `1.11` at `e = 0.04`; it then grows
continuously, roughly linearly, stays below the marginal weight near the onset (the dip is diluted *and* tilted), reaches it
near `βJ = 1.3` and exceeds it beyond (`0.141` against `0.132` at `1.5`; at `βJ = 2`: `0.271` against `0.269` at `e = 0.01`, `0.274` against
`0.227` at `e = 0.03`), where exits far from the symmetric one bind — the regime in which the block appears by a jump as a function of the accuracy (§6.2: `e₀ = 0.00181` at
`βJ = 1.5`).  Between `βJ*` and `βJ**` the uniform cube's profile is still the best one found (the cone formula is still exact there, column 4) but its value is below the uniform
cube's.
(iii) **[sketch]**  Why not at `βJ*`: just beyond it the binary branch loses only `κ(βJ − βJ*)²` (`κ = 0.264` at `e = 0.02`, from four
couplings; `0.217` at `e = 0.04`), while a free block costs `c·λ_f` to first order, `c = R_unif(e) − e·R′_unif(e)` (`0.0283`; `0.0258`), and
moves the stability threshold by `k·λ_f`, `k = ∂βJ_stab/∂λ_f` (`2.54`; `3.13`).  Maximising `−cλ − κ(βJ − βJ* − kλ)²` over `λ ≥ 0` gives the onset
`βJ** = βJ* + c/(2κk)` = **`1.124`** at `e = 0.02` and **`1.100`** at `e = 0.04` — both inside the observed brackets — and
`λ_f = (βJ − βJ**)/k` beyond (`0.002` at `1.13`, as found).  (That `βJ**(0.02, 1)` is close to `βJ*(0, 1) = 1.125` is a coincidence.)
The estimate presupposes exits that are tilted in both blocks and a binary branch that stays at the uniform cube's shell; when
the tilt reaches `ρ − p_u = (KL(p_u‖½) + e)/u` (`0.111` at `e = 0`) the cheapest exits become one-sided, the best binary profile
leaves the uniform cube's shell (column 3) and the estimate no longer applies.  **At `e = 0` the binary shell has left `p_u`
at `βJ = 1.15` (not yet at `1.14`; §6.6) — about where the estimate alone would put the onset, `1.147` — and no free block was
found at any coupling tried** (`βJ = 1.15, 1.16, 1.17, 1.18, 1.2, 1.5, 2.0`: the families with a free block return the binary value
to all digits).
So with two phases there are three regimes in the coupling at a fixed accuracy `e > 0`: **invisible barrier** (`βJ ≤ βJ*`: the
uniform cube's exponents), **tilted dips around one centre** (`βJ* < βJ ≤ βJ**`), **diluted dips** (`βJ > βJ**`); at vanishing
accuracy only the first two were found.

*A field at coexistence* (`βJ = 1.5`, `βB = 0.05`, `u = 1`: stable well at `κ = 0.939`, metastable well at `0.083` with `I = 0.0858`, barrier
top at `κ ≈ 0.483`, contact set `[0.023, 0.982]`; `t04`, `t03`):

| `e` | `R^{(2)}(e)` | Gibbs shell `(m; a, b)` | cone formula | zero residual | `n_{μ*}(e + R^{(2)}) − R^{(2)}` | truncated cone at `e + R^{(2)}` |
|---|---|---|---|---|---|---|
| `0` | `0.0250232` | `(0.4761; 0.3260, 0.2707)` | `0.0115296` | `0.0075630` | `4·10⁻⁹` | `0.0010456` |
| `0.01` | `0.0198677` | `(0.4777; 0.3319, 0.2722)` | `0.0068812` | `0.0036644` | `4·10⁻⁹` | `0.0002731` |
| `0.02` | `0.0152121` | `(0.4794; 0.3382, 0.2736)` | `0.0033556` | `0.0012178` | `3·10⁻⁹` | `0` |

The picture of §6.2 is unchanged by a field that keeps two wells: the optimal dips sit on an (asymmetric) shell in the barrier
type classes, the exponent at `e = 0` is almost that of `B = 0` (`0.02502` against `0.02510`) although the zero residual is much
easier (`0.0076`), and the pair identity holds with shells and fails with cones.  A search with three blocks at `e = 0` returns
the binary shell (as at `B = 0`); free blocks at `e > 0` were not searched for `B ≠ 0`.  The same search at `u = 0.3`, `B = 0`, `e = 0`
(contact set in three pieces) also returns the binary barrier shell (`0.0022646`).

*Other couplings* (`u = 1`, `B = 0`; `t13`): at `e = 0` the binary shell is optimal in every search; at positive accuracy the free
block appears, larger for stronger coupling.

| `βJ` | `e` | binary centre | best found | structure | `R_unif(e)` |
|---|---|---|---|---|---|
| `1.2` | `0` | `0.0283097` | `=` | binary, `x = 0.2742` | `0.0291391` |
| `1.2` | `0.02` | `0.0189503` | `0.0192108` | `S3`, `λ_f = 0.034`, `x = 0.2694` | `0.0201820` |
| `1.2` | `0.04` | `0.0113257` | `0.0118373` | `S4`: atoms `0.269, 0.442, 0.558, 0.731`, weights `0.475, 0.025, 0.025, 0.475` | `0.0128922` |
| `2.0` | `0` | `0.0213210` | `=` | binary, `x = 0.3249` | `0.0291391` |
| `2.0` | `0.01` | `0.0158308` | `0.0163911` | `S3`, `λ_f = 0.271`, `x = 0.2863` | `0.0244503` |
| `2.0` | `0.03` | `0.0068042` | `0.0084996` | `S3`, `λ_f = 0.274`, `x = 0.3002` | `0.0163303` |

(At `βJ = 2` the contact set is `[0.007, 0.099] ∪ [0.271, 0.729] ∪ [0.901, 0.993]`: the flanks of the barrier are already steeper
than `u = 1`.)  The pair identity residual at the best profiles is below `10⁻¹²` in all rows.

## 7. G3(c) — what exactly is conjectural about the upper bounds, and the tests on sets

### 7.1 The isoperimetric statement for `H` is proved for every `I`; what is open is the value of a single-letter supremum

The brief asks about "the isoperimetric statement for `H` when `v` is not convex (the proof of F6 uses `v = max_γ v_γ`)".  The
record of the referee (R9, §2 A) and the proof show that `v = max_γ v_γ` is used in **Lemma SL only** — the evaluation of the
single-letter problem as `max_γ R_γ` — and in no other step.  Theorem T3(b) keeps Steps 1–6 (with Lemma T inside a type class)
and takes the supremum over block profiles as the definition of the exponent function.  So, for every continuous `φ`:

* **[proved]** every set that is `e`-sensitive for `H` has `maxdens ≥ e^{−n[R̄_H(e−ω_n)+ω_n]}` (and `μ_H`-measure at least that), with
  `R_H = sup` over **all** block profiles; the hinted exponent of `H` is `R_H(ε₁)`; the tail function of `H` has the exponent `R̄_H^{−1}`;
  non-adaptive algorithms have the exponent `≤ inf{θ : θ + R̄_H^{−1}(θ) < ε₁}`.
* **[refuted]** "the supremum is attained at a binary centre" — false for `e > e₀` with two phases (§6.2 (B)); true for convex `I`
  (T9(b)).
* **[conjecture C1]** for `e ≤ e₀` (in particular at vanishing accuracy) the supremum is attained at the binary barrier shell:
  `R_H(0⁺) = R_H^{(2)}(0) = 0.0251012` at `βJ = 1.5`, `u = 1`.  Evidence: all searches with up to 5 blocks; the families of §7.3.
* **[open O2]** the value of `R_H(e)` for `e > e₀`: is the supremum attained by finitely many blocks?  (The optimal law of the
  block types gains an atom at `½` at `e₀`, splits it between `e = 0.03` and `0.04`, and the best found profiles have 5–6 atoms at `e ≥ 0.05`.)
* **[proved]** regularity (Lemma T8′): `R̄_H` is nonincreasing and 1-Lipschitz and the shear `e + R̄_H(e)` is nondecreasing, for every `I`.
  **[open O3]** whether the shear is *strictly* increasing where it is positive (no flat pieces, so that the pair identity is an
  identity of functions): proved for convex `I` (T9(c)), observed on every branch computed at `u = 1`, **doubtful at `u = 0.3`** (§6.5).
* **[open O4]** the adaptive upper bound (§8).
* **[open O5]** the non-adaptive exponent when the optimal dip profiles are marginal shells (`u = 0.30` at `βJ = 1.5`, §6.5 (4)):
  cones around profile classes give only `81 %` of `R_H∘S^{−1}` there.

*A proof strategy for C1/O2.*  For a fixed exit **type** `κ′` the inner value `g(ρ; κ′) := min{MI(ν) : ν̄ = κ′, u·dist(ν,μ) ≤ (B − v(κ′))/u}`
is, by Lagrangian duality, `max_{τ≥0,η}{h(κ′) − ηκ′ + (τ/u)(v(κ′) − e − (h+I)(m̄)) + E_ρ[(τ/u)h(M) − Γ_{τ,η}(M)]}`,
`Γ_{τ,η}(μ) := max_ν[h(ν) − τ|ν−μ| − ην]` — **convex in the law `ρ` of the block types at fixed mean**.  Against any *one* exit type two
atoms are therefore optimal (this is the mechanism of T9(b)); the number of atoms is driven by the number of exit types that
tie at the optimum: two (left/right) on the binary branch, three (left/right/symmetric) on the `S3` branch, more beyond.  A proof
would show that `k` tied exit types need at most `k` (or `k+1`) atoms — a semi-infinite max–min problem in which the minimum
over exit types cannot be convexified, because `v` is not convex.  I did not find such an argument, and the appearance of the
free block by a jump (two local maxima crossing) shows that no local argument at the binary optimum can decide it.
*What would count as a counterexample to C1:* a block profile with `r_μ(0) > 0.0251012`, or a family of sets with
`liminf_n ω(D_n) > 0` in §7.3 at `e_D ≤ e₀`.

### 7.2 Small cubes (`t07`)

For the two-phase model (`βJ = 1.5`, `u = 1`; at these sizes all types are contact types) and **all** proper nonempty subsets `D`
of `Q_3` (254) and `Q_4` (65 534), with `e_D := ln Φ_H⁺(D)/n`, `θ_D := −ln maxdens(D)/n` and `ω(D) :=` the least `ω ≥ 0` with
`θ_D ≤ R̄(e_D − ω) + ω` (`R̄` from the binary table, continued by `−e`): **`ω(D) = 0` for every subset** — but the test is almost void
at these sizes: `Φ_H⁺(D) < 1` for most sets, so `e_D < 0` lies in the volume regime where `R̄ ≥ −e`.  With `−ln μ_H(D)/n` in place of
`θ_D` (the `μ_H` form of the theorem, which carries the factor `Z_H = n+1`): `max ω = 0.317` (`n = 3`), `0.233` (`n = 4`), i.e.
`0.87` and `0.67` times `ln n/n`.  Annealing over subsets (fixed seeds; 12 × 6000 steps on `Q_5`, 8 × 5000 on `Q_6`), maximising
`ω(D)` in the `maxdens` form: `0.0019` and `0.0126`.  *Exact tail function:* `Ξ_md(q) := max{Φ_H(D) : maxdens(D) ≤ q}` over all
subsets against its restriction to unions of profile classes around one centre: ratio `1.000` on `Q_3`, at most `1.473` on `Q_4`
(at `q = ¼`) — the same order as in the field case (`2.08` there).  No counterexample; no information about exponents.

### 7.3 Families of sets at larger `n` that are not profile sets around one centre (`t08`; exact sums, `n = 96` and `144`)

For each set the pair `(e_D, θ_D)` is exact; `ω(D)` is computed against the **binary** table `R^{(2)}`.  By Theorem T3(b) with the
full supremum, `ω → 0`; a family with `ω` bounded away from zero at `e_D > e₀` would be a set-level view of §6.2 (B), at `e_D ≤ e₀`
a counterexample to C1.

| family (number of sets at `n = 96` / `144`) | max `ω`, `n = 96` | max `ω`, `n = 144` | in units of `ln n/n` |
|---|---|---|---|
| control: neighbourhoods of the binary optimum of the table (45 / 45) | `0.00066` | `0.00044` | `0.014` / `0.013` |
| neighbourhoods `{u·d(x,C) + V_n(\|x\|) < nB}` of a random 3-block class (752 / 719) | `0.00113` | `0.00134` | `0.024` / `0.039` |
| the same with 4 blocks (267 / 265) | `0.00251` | `0.00180` | `0.053` / `0.052` |
| cylinders: Hamming neighbourhoods of "a shell on 50–85 % of the coordinates, the rest free" (108) | `0.00069` | `0.00006` | `0.015` / `0.002` |
| budget neighbourhoods of one class of such a cylinder (81) | `0` | `0.00051` | `0` / `0.015` |
| unions of two shell-neighbourhoods around two centres with overlap `0.1, 0.25, 0.4` (18) | `0` | `0` | `0` |
| slabs and half-spaces in a 3-block grid, `n = 48` (199 / 197) | `0.00355` | `0.00402` | `0.044` / `0.050` |

No set exceeds the binary curve by more than `0.05·ln n/n`.  This test did **not** see the free-block gain of §6.2 (B) — the
random and hand-made families contain no profile near the diluted optimum, whose advantage at `n = 144` (`≈ 0.001`) is below the
finite-size terms; the single-letter search found it, the exact sums of §6.3 confirm it at fixed profiles.  The profiles with
the largest finite-`n` excess have single-letter values far below the binary one (`0.0035`, `0.0071`, `0.0110` against `0.0251` at
`e = 0`): the excess is a polynomial prefactor.  So this table supports the isoperimetric theorem, and says little about C1.

## 8. Adaptive algorithms without a hint: what fails, what remains, and a way round it for ferromagnets

### 8.1 The nested algorithm of Theorem 11.64 does not transfer to an interacting known part — where exactly

The lower bound transfers: every algorithm needs `e^{nR_H(ε₁) − o(n)}` evaluations at `H` (Theorem T3(a); every `n`).  So does the
analysis of the level recursion *if* a one-level theorem with the outer exponent `θ_na` were available (convex `I`: Theorem
T9(c) and Theorem 11.66).  The one-level theorem (Theorem 11.52 / F7) uses three properties of the split `Q_n = Q_o × Q_i`; with
`f = nφ(|x|/n)`:
(F1) *Fibres stay in the class* — **holds in a weaker form.**  For fixed outer point `a` the inner problem has the known part
`b ↦ nφ((|a| + |b|)/n)`: again a function of the type, but a different one for every outer type (Curie–Weiss: coupling
`βJ·n_i/n`, field `βB + βJ(2|a| − n_o)/n`).  A family of bracket procedures for *all* functions of the type would be needed,
with exponents that depend on the outer point.
(F2) *Fibre averages are Lipschitz relative to the reference* — **fails.**  `W(a) = E_{π(·|a)}e^{−ψ(a,·)} = N(a)/D(a)`,
`N(a) = Σ_b e^{−f(a,b)−ψ(a,b)}`.  For neighbours `a, a′`: `N(a′)/N(a) = e^{±u}·⟨e^{−n[φ(κ+1/n)−φ(κ)]}⟩`, the average over the **inner Gibbs law
of the instance**, i.e. `≈ e^{−φ′(κ_ψ)}` at the total type `κ_ψ` that `ψ` selects on the fibre, while `D(a′)/D(a) ≈ e^{−φ′(κ_π)}`.
Already for a residual that does not depend on `a` at all (`ψ(a,b) = g(|b|)`) the outer function `−ln W` changes by
`φ′(κ_ψ) − φ′(κ_π)` per outer flip.  For a field `φ′` is constant and the term cancels — this is the product structure.  With an
interaction, `−ln W` is Lipschitz only with the constant `u + osc(φ′)` over the types reachable on a fibre, and the excess
cannot be put into a reference instance because it depends on `ψ`.  The tail lemma on the outer block then holds with a larger
constant, and the recursion no longer has `R_H` as a fixed point (a valid upper bound, not the exponent).
(F2′) *Working slice by slice does not repair it.*  `A = Σ_t p_tA_t`, `A_t` the uniform mean over `T_t`, and for fixed total type the
fibre average over the inner slice is a function of `a` that is `u`-Lipschitz inside outer type classes but only `2u`-Lipschitz
across them (the residual `u(|b| − |a|)` attains `2u`): the outer problem carries the quotient metric
`d(a,a′) + ||a| − |a′||`, a different class.
(F3) the layer cake — measure-free, holds.
So **Theorem 11.64 (adaptive exponent = hinted exponent of the hardest instance) is open for every interacting known part,
convex or not.**  What is proved: the lower bound `R_H`; the non-adaptive upper bound `θ_na` (convex `I`: `= R_H∘S^{−1}`); and
instance-optimality at *symmetric* instances without a hint (Proposition T10).

### 8.2 Ferromagnets: a mixture of fields

**Proposition T12 [sketch — the missing step is the uniformity in `p` of the `o(n)` of Theorem 11.64].**  Let the known part be
a ferromagnetic Curie–Weiss model (`J > 0`, any `β`, any field; one phase or two).  Then adaptive algorithms without a hint have
a worst-case exponent at most

    max_{y} R^max_{field p_y}(ε₁)  =  R^max_{p=½}(ε₁)  =  KL((Λ₁ + ε₁)/u ‖ ½),

the adaptive exponent of the **uniform cube**.  Hence for `B = 0`, `βJ ≤ 1` (and for `1 < βJ ≤ βJ*(ε₁, u)`, §6.6) the adaptive
exponent is exactly `R_H(ε₁) = R_unif(ε₁)`: there "adaptive = hinted" holds with an interaction.  In the two-phase regime it
leaves the interval `[R_H(ε₁), R_unif(ε₁)]` (`[0.02510, 0.02914]` at `βJ = 1.5`, `u = 1`, `ε₁ → 0`).
*Argument.*  Hubbard–Stratonovich: `e^{(βJ/2n)M²} = √(n/2πβJ)∫e^{−ny²/(2βJ) + yM}dy` (`M = Σσ_i`), so
`π = ∫ν(dy)·Bernoulli(p_y)^{⊗n}`, `p_y = e^{y+βB}/(2cosh(y+βB))`, with the explicit positive density
`ν(dy) ∝ exp(−n[y²/(2βJ) − ln 2cosh(y+βB)])dy`, and `A(ψ) = ∫ν(dy)A_y(ψ)`, `A_y(ψ) = E_{Ber(p_y)ⁿ}e^{−ψ}` — the field problem of §11.20
for the **same** residual.  `|∂_y ln A_y| ≤ 2n`, and all `A_y` lie within `e^{un}` of each other, so a grid of `O(n³)` values of
`y` in a fixed compact interval represents `A` up to a factor `1 + O(1/n)`.  Run the adaptive algorithm of Theorem 11.64 for each
grid field at accuracy `ε − 1` and failure probability `δ/O(n³)` and combine the outputs with the weights `ν`.  The cost is
`poly(n)·max_y e^{nR^max_{p_y}(ε₁)+o(n)}`, and `R^max_p ≤ R^max_{½}` by Proposition 11.65(b).  ∎  (The same decomposition gives nothing
for non-adaptive algorithms beyond Theorem T1, and nothing for antiferromagnets: for convex `φ` the transform has an imaginary
field.)
*Why it is not tight in general.*  Component `y` needs only the accuracy `ε₁ +` (its deficit at the instance), but the cost
`R^max_{p_y}` is a worst case over the residual *as an instance of the field problem*, and the residuals for which the barrier
component matters are not worst-case instances of the uniform cube (`H` restricted to the uniform component has the landscape
`I − I(½) ≤ KL(·‖½)`).  An instance-optimal field algorithm would be needed; none is known for non-symmetric instances
(Proposition 11.65, last sentence).

### 8.3 Is `H` the hardest instance among all instances?

Among symmetric instances: yes, for every `n` (Theorem T4).  Among all: in §11.20 this follows from the adaptive upper bound
(an algorithm with a hint may ignore it); here that argument is available only where Proposition T12 is tight.  Instances whose
weights decay at the full rate `u` away from a set (cones, shell-cones, the roof `u·||x| − n/2|`) are *easy* with a hint: a
lowering at `x` propagates to every point radially outward from `x` (`ψ′(y) ≤ ψ′(x) + u·d(x,y) = ψ(y) − δ`), so `O(1)` extreme
points detect it — the slack vanishes in those directions.  A harder instance than `H` would have to keep slack in all
directions without being symmetric.  **[conjecture]** `sup_ψ`(hinted exponent of `ψ`) `= R_H` for every function-of-type known
part; equivalently (given a one-level theorem) the adaptive exponent without a hint is `R_H`.  For ferromagnets the truth lies
in `[R_H, R_unif]`.

## 9. G4 — interpretation and prior art

**What the results say.**  For a known part that is a function of an order parameter, with the density of states of the known
part available, the ensemble that is *uniform inside every level set of the order parameter and flat over the levels of a window*
— the multicanonical ensemble of Berg and Neuhaus, the target of Wang–Landau sampling, the reference law `μ_H` of §11.20 — is
(i) the sampling law of an optimal **non-adaptive** certified estimator of `ln A` over the Lipschitz class, up to a polynomial
factor, for every `n` (Theorem T1; in the stratified form: equal sample sizes in **all** level sets, importance weights `p_t` — that
the levels outside the window may be dropped at the exponential scale, as in §11.20, is not re-proved here);
(ii) the Gibbs law of the **hardest symmetric instance** (Theorem T4), whose exponent `R_H` is the single-letter value of
Theorem T3; and (iii) at phase coexistence the configurations that decide both exponents are *shells* in the level set at the
top of the barrier (§6): the perturbations that are hardest to exclude live on a macroscopic set of barrier configurations,
and the functions that defeat a non-adaptive sample are cones around such shells — at positive accuracy rates, shells that
constrain only part of the coordinates.

**What they do not say** (to be read with every number in this report).
1. The class is an idealised Hamming–Lipschitz class with one constant `u`; real residuals are not worst-case members of it.
2. The density of states of the known part (`p_t`) is **assumed known**, and the type-uniform sample is assumed free.  The
practical difficulty of flat-histogram methods — *producing* the flat ensemble by a Markov chain, tunnelling times, the
convergence of Wang–Landau — is not touched: the model counts evaluations of the residual only.  In that literature the flat
histogram is known **not** to be the optimal ensemble for the dynamics (Trebst–Huse–Troyer below); the two notions of
optimality answer different questions.
3. Exponents only (`e^{o(n)}` factors of the poor, typical-subset kind in every upper bound that uses Theorem T3(b)), extensive
accuracies only.
4. "Hardest instance" is proved among **permutation-symmetric** instances.  For ferromagnets every instance costs an adaptive
algorithm at most `e^{nR_unif}` (Proposition T12, sketch); whether a non-symmetric instance is harder than `H` when
`R_H < R_unif` is open (§8).
5. Nothing is said about sampling *from* a two-phase Gibbs measure, about dynamics, or about the mixing of any chain.

**Prior art** (searches of 25 Nov 2026 with generic queries; no project names, paths or personal data; what was read is stated).

| source | what it says that is relevant | how read |
|---|---|---|
| B. A. Berg, T. Neuhaus, *Multicanonical ensemble: a new approach to simulate first-order phase transitions*, PRL 68 (1992) 9; arXiv:hep-lat/9202004 | the multicanonical ensemble (flat energy histogram) for the 2d 10-state Potts model; purpose: overcome the exponential suppression of mixed-phase configurations | search summary of the arXiv abstract; paper not read |
| F. Wang, D. P. Landau, *Efficient, multiple-range random walk algorithm to calculate the density of states*, PRL 86 (2001) 2050; arXiv:cond-mat/0011174 | random walk in energy with on-the-fly estimate of the density of states until the histogram is flat | search summary; not read |
| P. Dayal et al., *Performance limitations of flat-histogram methods* (and optimality of Wang–Landau sampling), PRL 92 (2004) 097201; arXiv:cond-mat/0306108 | with the exact density of states ("perfect flat-histogram") the tunnelling time of local-update flat-histogram simulations still grows faster than the ideal random-walk scaling, exponentially for a spin glass; Wang–Landau "optimal" means: same scaling as the perfect flat-histogram scheme | search summary of abstract and snippets; not read |
| S. Trebst, D. A. Huse, M. Troyer, *Optimizing the ensemble for equilibration in broad-histogram Monte Carlo simulations*, PRE 70 (2004) 046701; arXiv:cond-mat/0401195 | the ensemble that minimises round-trip times is **not** flat (feedback from the local diffusivity puts more weight at bottlenecks); "substantially outperforms flat-histogram methods" | arXiv abstract page (machine summary); not read |
| F. Cérou, P. Héas, M. Rousset, *Entropy minimizing distributions are worst-case optimal importance proposals*, arXiv:2212.04292 | for a convex class of target distributions and cost = relative entropy of target w.r.t. proposal, the worst-case optimal importance proposal is the entropy minimiser in the class — the nearest statement of the form "this proposal is minimax-optimal over a class" that I found | arXiv abstract page (machine summary); not read |
| H. Y. He, A. B. Owen, *Optimal mixture weights in multiple importance sampling*, arXiv:1411.3954; T. Hesterberg, *Weighted average importance sampling and defensive mixture distributions*, Technometrics 37 (1995) | uniform mixtures of proposals are minimax for regret; defensive mixtures bound the weights — the mixture/NML reading of §11.20 remark (3) in importance-sampling language | search summaries; not read |
| A. Hinrichs, *Optimal importance sampling for the approximation of integrals*, J. Complexity 26 (2010) 125 | existence of sampling densities with worst-case error `O(n^{−1/2})` for integration in reproducing-kernel Hilbert spaces (randomised setting) | search summary; not read |
| P. Mathé, E. Novak, *Simple Monte Carlo and the Metropolis algorithm*, J. Complexity 23 (2007); arXiv:math/0611285 | lower bounds for non-adaptive methods on classes of densities with Lipschitz logarithm; adaption breaks the curse for log-concave densities — the method behind Theorem 11.45 (already cited in the theory report) | search summary of the abstract; not re-read |
| R. Ge, H. Lee, J. Lu, *Estimating normalizing constants for log-concave distributions: algorithms and lower bounds*, STOC 2020; arXiv:1911.03043 | query lower bounds for estimating a normalising constant (log-concave, gradient oracle) by an information-theoretic cell construction | search summary; not read |
| normalised maximum likelihood / Shtarkov distribution | name for `μ_H ∝ max_γ π_γ`; in the mean-field case `μ_H` is the flat ensemble on the contact set, which is the NML mixture of the field-tilted Gibbs measures **only if `I` is convex** (for two phases the tilted measures never sit on the barrier, `max_γ λ_γ` is the convex envelope and misses it — §6.4) | from memory |

Search log (queries): "multicanonical ensemble flat histogram optimality minimax worst-case importance sampling proof";
"Trebst Huse Troyer optimizing the ensemble for equilibration in broad-histogram Monte Carlo simulations flat histogram not
optimal round-trip"; "Hinrichs 'Optimal importance sampling for the approximation of integrals' worst case error randomized
algorithms sampling density"; "Dayal … 'Performance limitations of flat histogram methods' optimality of Wang-Landau sampling
abstract"; "Berg Neuhaus multicanonical ensemble first-order phase transitions flat energy histogram interface tension 1992
abstract"; "optimal importance sampling distribution minimax over a class of integrands mixture proposal 'defensive' worst-case
relative error Lipschitz log-density lower bound adaptive nonadaptive"; "Mathé Novak 'Simple Monte Carlo and the Metropolis
algorithm' …"; "Wang Landau 'Efficient, multiple-range random walk algorithm …' flat histogram abstract"; "Ge Lee Lu 'Estimating
normalizing constants for log-concave distributions: algorithms and lower bounds' query complexity lower bound"; "minimax
optimal sampling distribution over macrostates free energy estimation worst-case flat histogram 'minimax' umbrella sampling
order parameter optimal bias theory"; two page fetches (arXiv abstract pages of 2212.04292 and cond-mat/0401195).
**Not found** (ten searches, abstracts and machine summaries only — "not found", not "new"): a statement that the
flat-histogram/multicanonical ensemble is minimax-optimal for a *certified* estimate of a partition function over a class of
perturbations of a known part; exact non-adaptive or hinted exponents for such a class; the role of shells of barrier
configurations as extremal perturbations.  The physics literature treats optimality of the flat ensemble dynamically
(tunnelling/round-trip times) and finds it sub-optimal there; the statistics literature has minimax statements for proposals
with relative-entropy or regret criteria (Cérou–Héas–Rousset; He–Owen), which are the closest in form.

## 10. G5 (optional) — two order parameters; the mean-field Potts model

*Immediate (the proofs of §3 use only a group of coordinate permutations under which `π` is invariant, and a coupling of
adjacent orbits by changing one coordinate):* Theorems T1, T2, T4, T5 hold verbatim with "type class" replaced by "orbit":
(i) **two groups of sites** `A, B` and `f = n·φ(κ_A, κ_B)` (sublattice magnetisations): orbits `T_{t_A,t_B}`, at most `(n+1)²` of
them; the stratified sample is uniform on every orbit; the flat-histogram landscape is the largest minorant of `J` that is
`u`-Lipschitz for `|Δt_A| + |Δt_B|`; (ii) **`q`-state Potts**, `f = n·φ(`empirical distribution`)`: orbits = type classes of `[q]ⁿ`
(`≤ (n+1)^{q−1}`), adjacent classes coupled by re-colouring one site, landscape `u`-Lipschitz for the transport distance
`½‖τ − τ′‖₁`.  In both cases: the orbit-stratified sample is optimal among non-adaptive algorithms up to a polynomial factor,
every `n`; the flat-histogram instance is the hardest orbit-symmetric instance, every `n`.
*By the same proof, not written out* **[sketch]**: Theorem T3 — Lemma T holds for every finite alphabet (it is stated so in
workstream A) and is applied inside an orbit with a product measure that is uniform on it (for two site groups: the group of a
site is part of the label, and "density in the type class" becomes `I(X;U|G)`, `G` the group); the type-uniform measure
dominates every product measure up to the number of orbits.  The single-letter value is then
`sup_{P_{UX}} min{ I(X′;U) : u·P(X′≠X) + λ(P_{X′}) ≤ e + I(X;U) + I(P_X) }` with `X ∈ [q]`, and with `I(·;U|G)` and laws given `G`
for two groups.  Theorem T8(a), (b) (shell-cones against dips; the triangle inequality) is alphabet-free.
*Not immediate:* the clipping lemma T6 (binary; for `q ≥ 3` the inner problem is a transport problem); binary centres
(Theorem 11.27 already shows that for `q ≥ 3` the product case needs the vertices of the Lipschitz polytope — boxes — so the
number of blocks needed is not two); the collapse to additive instances and the game function need a **convex** rate function,
which a first-order transition does not have: the Potts model at its transition has the disordered well and `q` ordered wells,
the contact set contains the barriers between them when `u` exceeds their slopes, and by the reasoning of §6 the extremal
perturbations should be shells in barrier type classes — with `q − 1` order-parameter directions in which exits can slide
towards a well.  No number was computed for either extension.

## 11. Negative results, refuted guesses, and errors of my own that the tests caught

1. **"The dip exponent of `H` from its definition around one centre (`≈ 0.026`) is the exponent of `H` at phase coexistence"
(brief, O3) — refuted for positive accuracy rates.**  The precise value of that quantity at `e = 0` is `0.025101` (the coarse grid
gave `0.0255`–`0.0261`), and at `e → 0⁺` it is the exponent as far as I can tell.  But for `e > e₀ ≈ 0.0018` (at `βJ = 1.5`, `u = 1`)
profiles with a **free block** — sets that constrain only about 86 % of the coordinates — are sensitive at a smaller density:
`0.016155` against `0.015276` at `e = 0.02`, `0.006387` against `0.004626` at `e = 0.05` (§6.2).  The searches with three
and four blocks at `e = 0` (differential evolution, twelve Nelder–Mead starts) had found nothing — nothing is there at `e = 0`;
the gain was found by the next search, at `e = 0.02`, and I had already drafted "binary centres suffice numerically".
"Binary centres suffice" is true for convex `I` (proved, T9(b)) and false in general.
2. **"Single cones are extremal" — false with two phases** (O3 confirmed): the cone formula gives `0.01070` at `e = 0` against
`0.025101`, and the truncated cone fails the pair identity by a factor 12 (`0.00204` against `0.025101`).
3. **"With the zero residual's exponent the pair identity holds" — false** whenever `H ≠ 0` (D47 again; convex case with a field:
`0.02529` against `0.02266`; two phases: `R_0(0) = 0.00875`).
4. **"An antiferromagnetic interaction should make the problem harder than the uniform cube"** (my guess: for a symmetric
convex `I` only `R_H ≥ R_unif` is proved, and the exits to other types cost more) — **not seen**: `R_H(0) = 0.0291391 = R_unif(0)`
for `βJ = −1, −2, −8, −40` at `B = 0`, `u = 1` (the last is almost the uniform measure on the middle slice), with the maximum over
centre types at `m = ½` (§5.3).  With a field the exponents are below the uniform cube's in every row of §5.3.
5. **A certificate that binary centres suffice (mixing two exit types and using convexity in the profile law) — not
obtained**, and by item 1 it cannot exist for `e > e₀`.
6. **Shell-cone instances as candidates for "harder than `H`"** — they are easy with a hint (§8.3).
7. **The nested algorithm**: three ways of saving property (F2) were examined (§8.1) and none works; the mixture argument
(T12) gives a bound that is tight only where `R_H = R_unif`.
8. **Small cubes say almost nothing here**: on `Q_3`, `Q_4` every one of the 254 and 65 534 subsets satisfies the inequality of
Theorem T3(b) with `ω = 0` in the `maxdens` form, because `Φ⁺(D) < 1` puts `e_D` in the volume regime `R̄ ≥ −e` (§7.2).
9. **"With shells the pair identity holds whenever there are two phases"** — refuted at `u = 0.30` (`βJ = 1.5`): the optimal dips
are marginal shells whose cones cannot be truncated profitably; the best cone around a profile class gives `0.00184` at the
accuracy where the identity asks for `0.00226` (§6.5 (4)).  Whether the non-adaptive exponent is really smaller there is open.
10. **Errors of mine caught by tests, not by reading.**  (i) The first inner solver ranked the local minima of the boundary
scan by value; a plateau of equal values (no clipping from below) filled all three slots, the other exit was dropped, and the
*outer maximiser found and exploited exactly the profiles where that happened* (`0.025256` at an asymmetric profile instead of
`0.025101`).  Found by re-evaluating the optimum with a fine scan.  (ii) A two-dimensional grid search for `n_μ` missed thin
feasible slivers and the outer maximisation again climbed onto the error (`0.0254` instead of `0.0248` at one profile, which
looked like a violation of the pair identity in the direction that Theorem T8(b) forbids); replaced by the solver through
`r_μ` and cross-checked.  (iii) Cumulative densities per type class were computed as a global cumulative sum minus offsets:
absolute error `10⁻¹³`, fatal for caps `q = e^{−nθ}` at `n ≥ 2000` (the certified exponent collapsed from `0.0251` to `0.0149`);
now restarted per type.  (iv) Levels of a shell-cone inside a type class can contain many classes, not two (a plateau of
`|i − i₀| + |j − j₀|`); found by the brute-force test at `q = ½`.  (v) My first claim "one phase without a field is the uniform cube
because `I(ν̄) ≥ I(½)`" used `I ≡ 0` for the uniform cube; the correct argument is the symmetric-minimiser argument of T9(e).
(vi) In the sweep over `u` the multi-start search missed the barrier optimum at `u = 0.30` (no start in the narrow range of
shells with a positive value; the symmetric family found it), and I first took the mean slope of the barrier (`0.268`) for the
value of `u` below which its top leaves the contact set — it is the largest chord slope from the top, `0.2815`.  (vii) A first
run of the multi-block script at `u = 0.3` returned zeros (starts tuned to `u = 1`); discarded.  (viii) The control value "`E = 0.21227`" of the brief is `F*(t)/t` at `t = 10⁻⁴`; the threshold is `E = 0.212295` (chord gap of
`ln 2cosh(x/2)`), and `R^max(0.3E) = 0.023270` (it is `0.023273` at `0.3·0.21227`); `R_0(0.3E) = 0.019497` and
`θ_na(0.3E) = 0.036246` are reproduced with the correct `E`.
*Lesson (for the dead-ends file):* in a max–min computation every inaccuracy of the inner minimum is found by the outer
maximiser; an optimum must be re-evaluated with an inner solver that shares no approximation with the one used in the search.

## 12. What I did not check

1. **Nothing here is refereed.**  The proofs of Theorems T1–T9 are mine, written out above; the proof of T3(b) is the proof of
   Theorem 11.63 with Lemma T applied inside a type class and Lemma SL replaced by a definition — I re-derived every step but
   did not re-verify Lemma T itself (I rely on R9's check) nor Theorem 11.22/11.45 (machine-checked statements, read as stated).
2. **The value of `R_H(e)` for `e > e₀` in the two-phase case** (only lower bounds from profiles with at most 6 atoms, symmetric
   families plus general refinements; no proof that the supremum is attained).  **C1** (binary optimality for `e ≤ e₀`) is
   numerical.  Asymmetric two-phase models (`B ≠ 0`) were searched with three blocks at `e = 0` only.
3. **The equality "cone formula = sup–min" for convex `I`** is numerical (ten cases, `10⁻¹¹`) plus a sketch.
4. **Proposition T12** (ferromagnets via a mixture of fields) is a sketch: the uniformity in `p` of the `o(n)` of Theorem 11.64 was
   not checked in its proof; nothing was simulated.
5. **Antiferromagnets**: that their exponents never exceed the uniform cube's is numerical (cone formula; sup–min at one
   point with a field and on the symmetric family without); only `R_H ≥ R_unif` at `B = 0` is proved.
6. **The `o(n)` terms**: of the typical-subset kind (`n^{−1/8}`) in every upper bound; the exact sums suggest `c·ln n/n`.
7. **Strict monotonicity of the shear** `e + R_H(e)` for non-convex `I` (no flat pieces): not proved; Lemma T8′ gives only
   "nondecreasing".
7a. **The non-adaptive exponent where the optimal dips are marginal shells** (`u = 0.30`, §6.5 (4)): only the bracket
   `[0.00184, 0.00226]`; functions other than cones around profile classes were not tried.  Exact finite-`n` sums for
   *non-adaptive* bounds were computed for binary shells only (dips: also for 3 and 4 blocks).
7b. **The line in the plane (coupling, accuracy) on which the free block sets in** was located at two accuracies only (`e = 0.02`,
   `0.04`, `u = 1`, §6.7), and at `e = 0` its absence was checked at seven couplings; the first-order condition for adding a free
   block to a binary optimum was not derived in general, so C1 rests on searches.
8. **Product samplers, single tilted measures, plain Monte Carlo from `π`** for interacting known parts: not examined (in the
   two-phase case plain Monte Carlo from `π` never sees the barrier class, so it is exponentially worse; no number computed).
9. **Bounded accuracies** (`ε = O(1)`): only the lower bounds (`a` for non-adaptive algorithms, `R_H(0⁺)` for all).
10. **G5**: no proof written, no number computed.
11. **Lean**: nothing formalised.  The hypotheses of `GameFunction` for `F*` (T9(c)) are a paper proof.
12. **Prior art**: abstracts and machine summaries only (§9).

## 13. Scripts: commands, sizes, run times

All in `code/`, run from that directory as `python3 <script> <args>` under `ulimit -v 4000000`, one at a time (`queue1.sh`, `queue3.sh`, `queue4.sh`,
`queue5.sh` run them in sequence with `timeout 595`; `queue1.sh` was stopped after its fifth job and its remaining jobs moved to `queue3.sh`; their logs `out/queue*.log` list every command with its run time; the longest
run took 585 s; the runs added at the end — four `t10` sweeps (`out/t10_sweep_J_u1_e0.02_{b,c}.txt`, `…_e0.04.txt`, `…_e0_c.txt`), `t17`, `t18`, `t19` — were started by hand, one at a time); outputs in `out/` under the names given.  Own code throughout; seeds fixed in the scripts.

| script | what | sizes | run time |
|---|---|---|---|
| `tlib.py` | library: rate function `I`, minorant `v` (table of `4·10⁵` points, error `O(h²) ≈ 5·10⁻¹¹`), block profiles, the inner problem `V` by clipping (scan of 161 points + 5 batched zooms; fine version 2001 + 6), `R_bin` (multi-start Nelder–Mead over binary centres), symmetric multi-block families `S2…S6`, cone formulas, `n_μ` (through `r_μ`, and by direct 2-d search), shell-cones, closed forms of the field case | — | — |
| `tfin.py`, `kfin.py` | exact finite-`n` sums on profile grids (2 blocks around a centre; `k` blocks): dips of symmetric instances (`ℓ¹` distance transform), `maxdens`, density-capped families, shell-cones truncated at type-wise quantiles | up to `4·10⁶` (2 blocks, `n = 4000`), `6·10⁶` cells (3 blocks, `n = 600`) | — |
| `t01_control.py` → `t01_control.txt` | field control of §11.20: closed forms against the sup–min, cone formula, pair identity | `p = 0.1, u = 2`; `p = ½, u = 1` | 125 s |
| `t02_convex.py check` → `t02_convex_check.txt` | convex `I`: cone formula = sup–min = `max_γ R_γ`; pair identity; fails with `R_0` | 5 parameter sets × 2 accuracies | 424 s |
| `t02_convex.py table 1.0 <bJ list>` → `t02_convex_table_u1_{a,b,c}.txt` | table of §5.3 | 24 parameter sets | 176 + 185 + 198 s |
| `t03_blocks.py bJ bB u e k seed maxiter` → `t03_blocks_*.txt` | search over `k`-block profiles: differential evolution (Sobol, popsize 14) + Nelder–Mead from split binary optima | `k = 3` (`e = 0`, `0.02`), `k = 4` (`e = 0`), `B = 0.05`, `u = 0.3` | 191–263 s each |
| `t04_table.py` → `t04_table_*.txt` | tables of §6.2 (A): `R^{(2)}`, cone formula, zero residual, pair identity three ways | 13 accuracies; `B = 0.05`; `u = 0.3`; with differential evolution | 111–207 s each |
| `t05_bruteforce.py` → `t05_bruteforce.txt` | brute force on full cubes `n ≤ 12` against `tfin.py`; dips in `L_u`; `A(dip)/A = 1 + Φ`; truncation in `L_u` | 6 models, 722 checks | 16 s |
| `t06_finite.py` → `t06_finite_*.txt` | exact finite-`n` certified bounds (dips of `H`, of `0`; truncated shell-cone and cone) | `n ≤ 4000` (`n ≤ 1200` at `e = 0.05`); nine runs | 4–57 s each |
| `t07_smallcubes.py` → `t07_smallcubes_bJ1.5_u1.txt` | all subsets of `Q_3`, `Q_4`; annealing on `Q_5`, `Q_6` | 254; 65 534; 12×6000; 8×5000 | 129 s |
| `t08_families.py` → `t08_families_bJ1.5_u1_n{96,144}.txt` | brute-force check of `kfin.py` (45 checks); seven families of sets | about 1500 sets per `n` | 10 s; 41 s |
| `t09_Rtable.py`, `t09b_merge.py` → `Rtable_bJ1.5_u1.txt` | table of `R^{(2)}(e)` with `n_{μ*}(e + R)` | 44 accuracies | 222 s + 345 s |
| `t10_sweeps.py J …` / `U …` → `t10_sweep_*.txt` | sweeps of §6.5, §6.6, §6.7 | 16 couplings at `e = 0`, 11 at `e = 0.02`, 5 at `e = 0.04`; 9 values of `u` at `e = 0`, 4 at `e = 0.2·ln cosh(u/2)` | 107–270 s each (twelve runs) |
| `t11_instances.py` → `t11_instances_{add,flat,roof,rand}.txt` | other symmetric instances against `H` | 23 landscapes | 64 + 139 + 126 + 180 s |
| `t12_crosscheck.py` → `t12_crosscheck_bJ1.5_u1_e0.txt` | inner problem on full grids (2 and 3 blocks, `v` and `I`); the brief's set definition on a `1001²` grid; `n_μ` two ways | 12 + 6 + 2 + 10 cases | 43 s |
| `t13_multiblock.py` → `t13_multiblock_*.txt` | symmetric families `S2…S6` and general 3–5-block refinements; pair identity at the best profile | 11 accuracies at `βJ = 1.5` (three runs: 466, 585, 158 s); `βJ = 1.2` (173 s), `2.0` (240 s) | see left |
| `t14_finite3.py` → `t14_finite3_S{2,3,4}_e0.05.txt` | exact finite-`n` bounds from neighbourhoods of 2-, 3-, 4-block classes | `n ≤ 1200` / `600` / `300` | 1 s / 13 s / 45 s |
| `t15_e0.py` → `t15_e0_bJ1.5_u1.txt` | crossing of the binary and the diluted branch | 11 accuracies | 58 s |
| `t16_u03_na.py 1.5 0.3 0 0.0022646` → `t16_u03_na_e0.txt` | `u = 0.3`: best shell for the non-adaptive bound (symmetric, general binary, free block) | 40 + 3 + 3 searches | 261 s |
| `t17_random_inner.py` → `t17_random_inner.txt` | inner minima at four optima by random search over all exit profiles (`4·10⁶` points × 6 rounds × 3 runs) | 2–5 blocks | 75 s |
| `t18_antiferro.py` → `t18_antiferro.txt` | antiferromagnets without a field (`βJ = −1 … −40`); the threshold `u_top` | 4 couplings | 15 s |
| `t19_onset.py 1 0.02 <bJ:value …>`, `… 1 0.04 …` → `t19_onset_u1_e0.0{2,4}.txt` | onset of the free block in the coupling: the local formula `A(λ_f)` against finite differences and against the solver; marginal weights; the estimate of `βJ**` | 6 + 8 checks per accuracy | 1 s each |

Accuracy of the single-letter numbers: the inner solver agrees with brute force (full grids, random search) to the resolution
of the latter (`10⁻⁶`–`10⁻⁷`); outer optima from different starts agree to `10⁻⁹`; the field control is reproduced to `10⁻¹³`.  The
stated digits of `R^{(2)}` and of the multi-block *values at the profiles given* are reliable to `10⁻⁷`; that a profile is the
maximiser of its family is reliable to the search (§6.2).

## 14. For readers of an earlier draft of this report

The repository advanced while this work was done (read at `36613b9`; `63efc69` at the end, when its working tree also contained a
draft section on the present topic written from an earlier draft of this report — I did not use it and did not check it line by
line).  The following statements were corrected or added late; an earlier draft differs in these points:

1. **§6.5, the threshold.**  The top of the barrier leaves the contact set at `u_top = 0.28153` (largest slope of a chord from the
   top), not at the mean slope `0.268`.
2. **§6.5, `u = 0.30`.**  `R^{(2)}(0) = 0.00226457`, a barrier shell (the first table had the value of a dip in a well, `0.00076`: the
   search had missed the barrier optimum).  **The pair identity fails there for cones around profile classes** (best shell-cone
   `0.00184`), and the non-adaptive exponent is open (O5).  "The pair identity holds as long as the top of the barrier is a contact
   point" is therefore wrong; it holds in the rows `u ≥ 0.35` and `u ≤ 0.25` of the table.
3. **Lemma T8′ is new**: `R̄_H` is 1-Lipschitz and the shear is nondecreasing for every `I`.  Continuity of `R_H` and "slopes `≥ −1`"
   are no longer hypotheses of T8(c), nor open; what remains open is strict monotonicity of the shear and the witness condition
   (equality in `N ≤ R_H∘S^{−1}`) — the thing that fails at `u = 0.30`.
4. **§6.7, the onset of the free block in the coupling** (corrected last, with four more runs of `t10` and with `t19`): it is not at
   `βJ*(e, u)`, as an earlier sentence said, but at a larger coupling `βJ**` (`≈ 1.124` at `e = 0.02`, `≈ 1.10` at `e = 0.04`; `u = 1`), and at
   `e = 0` there is none at any coupling tried.  The mechanism paragraph of §6.2 now has the exact local formula `βJ_stab(λ_f)`
   in place of "the coupling is effectively `βJ(1 − λ_f)`".
5. **T9(c)** is stated with the transform `R̂` (`R_H = R̂` for `e ≥ 0`, `R̄_H ≤ R̂` in general).
6. **Antiferromagnets without a field** have the uniform cube's exponents numerically ("`≥`" is proved) — not larger ones.
7. **§6.2**: the inner minima at four optima were confirmed by a random search over all exit profiles (`t17`); the gain from
   multi-block profiles at `e = 0.05` is `38 %`.

