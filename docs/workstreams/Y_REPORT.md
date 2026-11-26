> **Repository note (coordinator, fourteenth checkpoint of cycle 10, 2026-11-25).**  This is the report of
> workstream Y **as delivered, unchanged below this note**.  It has **not yet been verified** by the
> coordinator: no proof in it has been re-derived, no number re-computed with independent code, and
> **nothing of it is in the theory report**.  It is stored here, with its scripts and outputs in
> `experiments/workstreams/Y/` (paths made relative; `Y_notes.md` there is the workstream's running log), so
> that the verification does not depend on a session's scratch directory.  Its brief is
> `docs/workstreams/Y_brief.md`.  Until it is verified, cite nothing from it.

> **Errata after two independent reviews (coordinator, eighteenth checkpoint, 2026-11-26).**  The
> report has been refereed by R11 (`docs/reviews/R11_referee_report.md`, replication in
> `experiments/reviews/R11/`) and reviewed and replicated by the Scientific Discovery Division
> (SCI-REV-0010; its report `docs/science/workstreams/R10_REPORT.md` on the branch
> `research/scientific-translation`).  Both re-derived every statement labelled *[proved]* and
> found none false; both reproduced the numbers.  **The text below is unchanged; read it with
> these corrections, and cite the theory report, §11.32, not this file.**
> (e1) **§0.2, first line, "Yes — upwards": not the answer to the question.**  It holds at
> `u = 1`.  By Proposition F of this report with blocks of three sites the capacity exponent `a`
> is *below* the cube's at `u = 3, 4, 6` (`p = 0.3, 0.2, 0.1`), at `u = 2.5` (`p = 0.2, 0.1`) and at
> `u = 2` (`p = 0.1`), and `h` at `u = 4, 6` (`p = 0.2, 0.1`); only the threshold rises at every
> slope (SCI-REV-0010, finding M1; re-computed by the coordinator with `ylib.py`).  The last
> sentence of the slope paragraph of §6.5 ("not decided") is superseded accordingly.
> (e2) **What the brackets are brackets of** (R11, M1).  Lower ends of `h`, `E`: unconditional
> lower bounds for every algorithm at every `n` and every accuracy.  Upper ends: bounds for the
> game-function numbers `h_∞`, `a_∞`, `E_∞`; as bounds on costs they are conditional on Theorems
> 11.95, 11.98(d), 11.101(b) for super-sites, hold for extensive accuracies only and in the
> iterated limit; at bounded accuracy no upper bound on a cost is proved.  The `a`-column is
> conditional on both sides (R11, m17).
> (e3) **The contrast with §11.25** (R11, M2): Corollary 11.91 covers the hinted exponent of
> symmetric instances and fixed samples, not adaptive algorithms without a hint.
> (e4) **Small slopes** (§0.2, §6.5): "multiplied by `(1−p)/p`" is a theorem at second order for
> finite chains — the largest variance of a Lipschitz function, which for an associated law is
> that of the magnetisation (SCI-REV-0010, R10.1, R10.2) — and "the susceptibility" is right
> for this chain only; for `a` the report had an upper bound only (R11, m14).
> (e5) **Numbers.**  The four headline lower ends of `h` depend in the fifth decimal on an
> unstated iteration cap (R11, m1: any `M_L` is valid; best found `0.034040, 0.040143, 0.044622,
> 0.044513`).  At `p = 0.1` the upper ends were not optimised: `h ≤ 0.0628`, `a ≤ 0.1730` (R11, m2;
> SCI-REV-0010, m6).  `E_∞ = E_F` for `p ≥ 0.14` at `u = 1` without the margins `1–2·10⁻⁴` of §5.4(c)
> (an artefact of the end cells), and `E_∞ ∈ [0.401719, 0.403619]` at `p = 0.1` (R11, m4;
> SCI-REV-0010, m7, m8).  §6.3: the "restricted" value `0.04435` is the open end of a bracket
> that closes at `0.044357`.  §7.1 compares an upper with a lower bound; the exact `F*_5` over all
> 395 094 vertices is `0.1965988` (SCI-REV-0010, m9).  "Nothing is decided for `p ≤ 0.05`":
> `h ≥ 0.0375` at `p = 0.05` and `≥ 0.0300` at `p = 0.02` are above the cube (its m10).
> (e6) **Sentences.**  §7.2, "for short chains the optimal labels are the two uniform fields":
> false at `p = 0.4` (four labels; R11, m11; SCI-REV-0010, m1); the support sizes of §6.4 are
> `4, 8, 18` (R11, m12).  "Domains of about `2K/u` sites": 3 to 5 sites at `u = 1` (R11, m10).
> §8.3: the example shows that the quantile *levels* are not Lipschitz; that the truncated
> residual leaves the class is shown by the example of SCI-REV-0010, m2 (theory report,
> Proposition 11.117(e)).  Lemma A uses Theorem 11.27(a) as well as (b); "the threshold of the
> `n`-chain is exactly `E_n`" needs three more lines (R11, m6); Proposition D presupposes a
> stationary chain and, where `u < 2κ₀`, starts at `L = 2` (R11, m7); Theorem E(a) holds with
> `C = 2(u + K)` for every `p` (R11, m5); `E_n ≥ ln Z_n(h)/Z_n(0)` is the every-`n` statement and
> `E_∞ ≥ E_F` its limit (R11, m9); Theorems 11.99 and 11.101 have since been reviewed
> (SCI-REV-0005), so "unrefereed" stands for 11.95 and 11.98(d) only (R11, m15).

# Workstream Y — known parts with interactions along the chain (Markov chains): reduction to product landscapes of blocks, a regularised formula, and what a nearest-neighbour interaction does to the exponents

Independent workstream of the MetricChain theory programme; synthetic models only.  Everything here was written in
`<session scratch directory>/ws/Y/` (`Y_report.md`, `Y_notes.md`, `code/`, `out/`); the repository was only read.
Labels: **[proved]** = complete proof in this report (paper proof by one author, **not refereed**; inputs from the theory
report are named with their status there), **[sketch]**, **[numerical]**, **[conjecture]**, **[known]**.
"[V]" = machine-checked in the repository, "[P]" = paper proof in the theory report.

---

## 0. Summary

### 0.1 Verdicts per step

| step | verdict |
|---|---|
| **0 controls** | **Reproduced** with own code (`ylib.py`): cube `u = 1`: `h = 0.0291391`, `a = 0.1109441`, `E = 0.1201145`; a block of 2 (3) independent uniform sites as one super-site with 6 (38) vertices gives the same per-site values to `10⁻⁷`; the 2 (30) non-additive vertices carry no weight for a product law (weight `10⁻¹¹`; additive labels alone give the same value). |
| **1 reductions** | **[proved]**, exact for every `n`, inhomogeneous chains, any alphabets, asymmetric envelopes; brute force on 36 chains (8–10 binary, 6 ternary sites), 432 + 432 + 252 random residuals: identities to `3·10⁻¹⁵`, no violation.  (U) as in the brief, with the slack `δ^±` written out and shown to be attained.  (L) as in the brief with the centred constant `Σ_j osc ln ρ_j`.  **New (L′):** an exact embedding with a *reduced envelope* instead of a loss of accuracy.  All three preserve the kind of algorithm (non-adaptive, hinted, adaptive). |
| **2 sandwich and limit** | **[proved]** that the limit exists, with monotone brackets: `F⁺_L` (free-boundary block, slack at both ends) is exactly **sub-additive**, `F⁻_L` (block marginal, reduced envelope) exactly **super-additive**, `F⁻_L/L ≤ F_∞ ≤ F⁺_L/L`, gap `≤ tC/L`.  Lower bounds for all algorithms hold for **every `n`** and use only Theorem 11.27(b) [V] (the chain as *one* super-site; no product structure needed).  Upper bounds for algorithms and the non-adaptive exponent are **[proved given Theorems 11.95, 11.98(d), 11.101(b) for block landscapes, which are unrefereed]**; the limits are iterated (`n → ∞` at fixed `L`, then `L → ∞`), nothing is uniform in `L`. |
| **3 numbers** | Done, `p = 0.5 … 0.1`, `u = 1` (§6).  The block reductions with `L ≤ 3` alone give brackets that are a factor 2–10 wide and **do not decide the question**.  Three sharper tools decide it: a Markov-recursion bound, a tilt-state recursion (both upper bounds on the game function, **[proved]**, evaluated numerically, the second with a conservative discretisation), and Lyapunov-type lower bounds for site-wise labels (**[proved]** formulas, numerical evaluation, every `n`). |
| **4 structure** | **[numerical, exact enumeration]** Site-wise labels are optimal in every case computed for `p ≥ 0.3` (`n ≤ 5`, all 395 094 vertices at `n = 5`), but **not in general**: at `p = 0.1` non-additive vertices carry weight (capacity at `n = 4`: weight `0.092` on `−dist(x, {0000, 1111})`; `t ≥ 0.65` at `n = 5`).  The hardest instance is **not** the zero residual and **not additive**: it has no site terms and has pair terms; the Rényi centre is **not a Markov chain** (`I(x₁;x₃|x₂) = 6·10⁻³` at `p = 0.3`).  A Lyapunov-exponent form exists as a lower bound (moment Lyapunov exponents of products of random `2×2` matrices) — **[proved]**. |
| **5 fixed sample** | Every-`n` statements with losses `e^{O(n/L)}` from (U)/(L′) **[proved given 11.95]**.  The pair-type-stratified sample is unbiased and has the usual guarantee, but **the symmetry argument fails concretely**: class-wise quantiles of an admissible residual are *not* admissible for Markov-type classes (598 violations in 600 brute-force cases, 0 for type classes of the cube; explicit example) — **negative result [proved by example]**.  Optimality with polynomial losses: open. |
| **6 beyond chains** | **[sketch]** Strips are chains with column alphabets: everything transfers.  In `ℤ^d` both reductions lose a surface term, so the regularised limit exists along boxes *with or without* decay of correlations; the gap argument is only an accelerator, and at phase coexistence it fails (`ρ_m ↛ 1`) while the crude surface bound still works.  On trees (surface ∝ volume) the sandwich does not close. |

### 0.2 The question of the brief: does a nearest-neighbour interaction without a field change the exponents?

**Yes — upwards, for every `p ∈ {0.4, 0.3, 0.2, 0.1}` at `u = 1`, and substantially.**  (For interactions that are functions
of the type it does not: Corollary 11.91(ii).)  Per site, binary symmetric chain with flip probability `p`:

| `p` | `h` (hinted at the hardest instance = adaptive) | `a` (non-adaptive, vanishing accuracy) | `E` (threshold) |
|---|---|---|---|
| `0.5` (cube) | `0.029139` | `0.110944` | `0.120115` |
| `0.4` | `[0.034026, 0.036163]` | `[0.116817, 0.121446]` | `[0.169127, 0.169165]` |
| `0.3` | `[0.040115, 0.044995]` | `[0.126444, 0.140860]` | `[0.232400, 0.232538]` |
| `0.2` | `[0.044599, 0.054353]` | `[0.129797, 0.160745]` | `[0.310766, 0.310956]` |
| `0.1` | `[0.044378, 0.066765]` | `[0.116632, 0.192774]` | `[0.401719, 0.417991]` |

*At `p = 0.3`:* `h` rises by `+38 %` to `+54 %` (best estimate `≈ 0.0405–0.041`, `+40 %`, §6.4), `a` by `+14 %` to `+27 %`, and the
threshold almost doubles: `E = 0.2324` (`×1.935`).  All twelve lower ends lie above the cube.
*What the brackets are.*  Lower ends of `h`, `E`: lower bounds for **every algorithm and every `n`** (they use Theorem 11.27(b)
[V], elementary algebra and a numerical evaluation; nothing unrefereed).  Upper ends, and the reading of `a` as the
non-adaptive exponent: bounds on the limit game function `F_∞`, which is the chain's game function by the regularised
theorem (unrefereed inputs, §4).  Upper ends are numerical evaluations of proved bounds on a grid whose error is on the safe
side by construction (floating-point rounding not controlled).
*Mechanism.*  The hard perturbations are no longer independent from site to site: labels (local fields) that are
**constant over domains of about `2K/u` sites** (`K = ln((1−p)/p)`) exploit the cooperative response of the chain.  With
independent labels — the family whose Rényi centre is the zero residual — the bound is *below* the cube (`0.0282` at `p = 0.3`;
Jensen); the hinted exponent of the zero residual itself was not computed.
*Closed form for the threshold:* `E ≥ E_F := ln[(1−p)cosh(u/2) + √((1−p)²sinh²(u/2) + p²)]` (**[proved]**, every `n`), and
`E = E_F` for `p = 0.4, 0.3, 0.2` up to certified margins `1–2·10⁻⁴` (**[numerical evaluation of a proved bound]**); for
`p = 0.1` only `E ∈ [E_F, 1.04·E_F]`.
*Slope dependence (lower bounds only, §6.5):* for small slopes all three exponents are multiplied by `(1−p)/p` (`2.33` at
`p = 0.3`; bracket `[2.27, 2.33]` at `u = 0.05`); at `u ≥ 2` my lower bound for `h` drops below the cube and the direction for `h`
is **not decided** there.  As `p → 0` at `u = 1` nothing is decided for `p ≤ 0.05` (§6.5; my first guess about that regime
was wrong, §10).

---

## 1. Setting, conventions, inputs

Sites `i = 1..n`, alphabets `𝒮_i`, site envelopes `d_i ≥ 0` (zero diagonal, triangle inequality, not necessarily symmetric),
`d(x,y) = Σ_i d_i(x_i,y_i)`, class `𝒞_d = {ψ : ψ(x) − ψ(y) ≤ d(x,y)}` (orientation of §11.26), `A_π(ψ) = E_π e^{−ψ}`, accuracy
`ε = ε₁n`, cost = evaluations of `ψ`, algorithms as in §11.10.  **Reference measure**

    π(x) ∝ exp( −Σ_i f_i(x_i) − Σ_{i<n} J_i(x_i, x_{i+1}) )        (a nearest-neighbour Gibbs measure = a Markov chain; f_i, J_i known).

For `φ ∈ 𝒞_d`: `π_φ ∝ π e^{−φ}` (Gibbs law), `φ̃ = φ + ln E_π e^{−φ}`.
*Running example.*  `𝒮 = {±1}`, `π(s) ∝ exp(K′ Σ s_i s_{i+1})`, `K′ = K/2`, `e^K = (1−p)/p`, transition matrix `P = [[1−p, p],[p, 1−p]]`,
`λ = 1 − 2p`, Hamming envelope of slope `u`, `h := u/2`.  A **site-wise label** is `φ_σ(s) = −h Σ_i σ_i s_i`, `σ ∈ {±1}ⁿ`; its
Gibbs law is the Ising chain in the field `hσ_i`; `Z(σ)` its partition function, `Z_n(h)` that of the uniform field.

*The site function of a finite space* `(X, π, d)` (a "super-site"), `0 < t < 1`:

    F*_X(t) := max_M G_t(M),   G_t(M) := −t ln Σ_x ( Σ_φ M(φ) π_φ(x)^t )^{1/t}      (M a probability vector on vertices of 𝒞_d/ℝ)
             = min_Q max_{φ∈𝒞_d} (1−t) D_t(π_φ ‖ Q),      (1−t)D_t(P‖Q) = −ln Σ_x P(x)^t Q(x)^{1−t},

`E_X = lim_{t↓0} F*_X(t)/t = min_Q max_φ KL(Q‖π_φ)`, `a_X = lim_{t↑1} F*_X(t)/(1−t) = min_Q max_φ KL(π_φ‖Q)`; `F*_X(t)/t` is
nonincreasing and `F*_X(t)/(1−t)` nondecreasing (Theorem 11.99 and workstream W, Theorem W3(c): [P], re-derived by the
coordinator; the proofs are for a "site" with any alphabet and any law, hence for any finite `(X, π, d)`).  Weak duality
(`G_t(M) ≤ max_φ(1−t)D_t(π_φ‖Q)` for all `M`, `Q`) is Hölder's inequality and is all that the *bounds* below use.

*Inputs from the theory report and their status.*  Theorem 11.22, Theorem 11.27(a), (b) **[V]**; Theorem 11.28, remark (i) [P];
§11.26: Theorems 11.95, 11.98(d), 11.99, 11.101 (**[P], unrefereed**), applied to product landscapes whose sites are blocks.
*Reused file:* `experiments/coordinator_checks/sites_W/wv_lib.py` only in `y00` as an independent check of my vertex
enumeration for four letters; no other code of the repository is used.

---

## 2. Step 0 — controls  (`code/y00_controls.py`, `out/y00_controls.txt`)

Own solvers: Arimoto iteration for `G_t` with the duality bracket `[G_t(M), max_φ(1−t)D_t(π_φ‖Q_M)]`; exponentiated gradient for
`E`, Blahut–Arimoto for `a` (both with duality brackets); independent inner solvers used at optima: SLSQP on the simplex, and
the linear-programming value of the game at the Rényi centre.  Vertices of the Lipschitz polytope of a cube `Q_L` with
weights `w_i`: (i) all spanning trees of tight edges with signs (complete; `L ≤ 3`); (ii) for a uniform slope the vertices are
exactly the integer height functions (`|f(x) − f(x^i)| = 1` on *every* edge — a parity argument: a connected tight graph forces
`f(x) ≡ |x| mod 2`), counts `2, 6, 38, 990, 395 094` for `L = 1..5`.

| control | `h` (`t*`) | `a` | `E` |
|---|---|---|---|
| cube, one site, `u = 1` | `0.0291391` (`0.4900`) | `0.1109441` | `0.1201145` |
| 2 independent sites as one super-site (6 vertices) | `0.0291391` | `0.1109441` | `0.1201145` |
| 3 independent sites as one super-site (38 vertices) | `0.0291391` | `0.1109441` | `0.1201145` |
| the same with the 4 (8) additive vertices only | identical to `10⁻⁷` | | |
| with the 2 (30) non-additive vertices only | `0.01457` (`0.01943`) | `0.0555` (`0.0763`) | `0.0601` (`0.0801`) |
| field control `bin` `(0.7, 0.3)` | `0.0250335` | `0.0953005` | `0.1031310` |

The non-additive vertices of the square are `±u·1[x₁ ≠ x₂]` — a **pair term**.  For a product law they get weight `10⁻¹¹` in the
optimal `M`; this is Lemma B below.  With unequal weights there are more vertices (`(1.847, 1, 1.847)`: 120).

---

## 3. Step 1 — the two reductions, exact for every `n`

### 3.1 (U): cut interactions move into the residual

**Theorem Y1 (upper reduction) [proved].**  Let `𝒦 ⊂ {1..n−1}` be a set of cuts (between `c` and `c+1`); for every cut choose a
gauge `J_c(a,b) = r_c(a) + s_c(b) + J°_c(a,b)` (e.g. `r = s = 0`).  Let `ρ = ⊗_B ρ_B` be the product over the blocks of the
free-boundary Gibbs laws of the blocks, with `r_c` added to the field of the last site of the block left of `c` and `s_c` to the
field of the first site right of `c`; `g(x) := Σ_{c∈𝒦} J°_c(x_c, x_{c+1})`.  Then

    π = ρ e^{−g} / E_ρ e^{−g},        A_π(ψ) = A_ρ(ψ + g) / A_ρ(g)        (the denominator is a known number),
    ψ ∈ 𝒞_d  ⟹  ψ + g ∈ 𝒞_{d⁺},     d⁺_c = d_c + δ⁻_c,   d⁺_{c+1} = d_{c+1} + δ⁺_c,   d⁺_i = d_i otherwise,
    δ⁻_c(a,a′) = max_b [J°_c(a,b) − J°_c(a′,b)],        δ⁺_c(b,b′) = max_a [J°_c(a,b) − J°_c(a,b′)].

`δ^±` have zero diagonal and satisfy the triangle inequality; they are attained (for a cone `ψ = d(·,y₀)` no slack is left), so
`d⁺` cannot be improved for a product envelope.  Consequently every `(ε/2, δ)`-correct algorithm for the block-product
landscape `(ρ, d⁺)` is one for the chain `(π, d)` with **the same evaluation points** (evaluate `ψ + g`, subtract `ln A_ρ(g)`):
non-adaptive algorithms stay non-adaptive, a hint `ψ` becomes the hint `ψ + g`, randomisation and cost are unchanged.
*Proof.*  `π ∝ ρ e^{−g}` by definition of the gauge.  `J°(a,b) − J°(a′,b′) = [J°(a,b) − J°(a′,b)] + [J°(a′,b) − J°(a′,b′)] ≤ δ⁻(a,a′) + δ⁺(b,b′)`,
so `g(x) − g(y) ≤ Σ_c [δ⁻_c(x_c,y_c) + δ⁺_c(x_{c+1},y_{c+1})]`.  ∎
*Remarks.*  (i) `δ^±` may be negative when `J°` has row or column parts; then `d⁺` is brought to a nonnegative envelope by the
normal form of §11.11 (move the gradient part into the block law) or one uses `max_b|…|`, a pseudo-metric.  (ii) *When
`osc J` exceeds the site envelope* nothing breaks: `d⁺` is still an envelope, the reduction is exact, only the bound is weak
(the end sites of every block carry slopes `≫ u`).  (iii) Binary symmetric chain: `δ^± = K·1[a ≠ a′]`, block law = stationary
`L`-marginal, slopes `(u+K, u, …, u, u+K)` (`u + 2K` for `L = 1`).

### 3.2 (L) and (L′): blocks with gaps

Blocks `B_1 < … < B_k` with gaps of `m_j ≥ 0` sites; `e_j` the last site of `B_j`, `s_{j+1}` the first of `B_{j+1}`;
`π_{B_j}` the marginal law of block `j`; `ρ_j(a,b) := P(x_{e_j} = a, x_{s_{j+1}} = b) / (P(x_{e_j} = a) P(x_{s_{j+1}} = b))`.

**Theorem Y2 (lower reduction, accuracy version) [proved].**  The marginal of `π` on the block sites is
`π_B = ⊗_j π_{B_j} · Π_j ρ_j(x_{e_j}, x_{s_{j+1}})`.  The members of `𝒞_d` that do not depend on the gap letters are exactly
`ψ′∘proj`, `ψ′ ∈ 𝒞_{d_B}` (`d_B` = the envelope on the block sites), and

    Σ_j min ln ρ_j  ≤  ln A_π(ψ′∘proj) − ln A_{⊗π_{B_j}}(ψ′)  ≤  Σ_j max ln ρ_j .

Hence an `(ε/2, δ)`-correct algorithm for the chain, run on the subclass with its output shifted by `½Σ_j(min + max) ln ρ_j`, is
`((ε + η)/2, δ)`-correct for the block product `(⊗π_{B_j}, d_B)`, `η := Σ_j osc ln ρ_j`, with the same evaluations and of the same
kind.  For a homogeneous ergodic chain `osc ln ρ_j ≤ C|λ₂|^{m_j+1}`.
*Proof.*  Markov property: `π_B(x) = π_{B_1}(x_{B_1}) Π_j P(x_{B_{j+1}} | x_{e_j})` and
`P(x_{B_{j+1}} | x_{e_j}) = π_{B_{j+1}}(x_{B_{j+1}}) · P(x_{s_{j+1}} | x_{e_j})/P(x_{s_{j+1}})`.  A function that ignores the gap letters is
in `𝒞_d` iff it is in `𝒞_{d_B}` (take equal gap letters).  ∎

**Theorem Y3 (lower reduction, envelope version — exact, no loss of accuracy) [proved; new].**  Let
`ε⁻_j(a,a′) = max_b[ln ρ_j(a,b) − ln ρ_j(a′,b)]`, `ε⁺_j(b,b′) = max_a[ln ρ_j(a,b) − ln ρ_j(a,b′)]` and
`d⁻ := d_B − ε⁻_j` at `e_j`, `− ε⁺_j` at `s_{j+1}`.  For every `ψ′` with `ψ′(x) − ψ′(y) ≤ d⁻(x,y)`,

    ψ := ψ′∘proj + Σ_j ln ρ_j(x_{e_j}, x_{s_{j+1}})  ∈ 𝒞_d        and        A_π(ψ) = A_{⊗π_{B_j}}(ψ′)   exactly.

So the block-product landscape `(⊗π_{B_j}, d⁻)` sits inside the chain's problem at the *same* accuracy: every algorithm for the
chain is one for it, of the same kind and cost.  (If `d − ε` violates the triangle inequality, its shortest-path closure
defines the same class; it must have no negative entries, i.e. the gap must be large enough.)
*Proof.*  `A_π(ψ) = E_{π_B}[e^{−ψ′}/Πρ_j] = E_{⊗π_{B_j}} e^{−ψ′}`; `ψ(x) − ψ(y) ≤ d⁻(x,y) + Σ_j[ε⁻_j + ε⁺_j] = d_B(x,y)`.  ∎
*Binary symmetric chain:* `ρ_m(a,b) = 1 ± λ^{m+1}`, `ε^± = κ_m·1[a ≠ a′]`, `κ_m = ln[(1+λ^{m+1})/(1−λ^{m+1})]` (`κ_0 = K`); block slopes
`(u−κ_m, u, …, u, u−κ_m)`.  (L′) needs `u > κ_m` (`u > 2κ_m` for `L = 1`): `m ≥ 0` at `p = 0.4`, `m ≥ 0` at `0.3` (`K = 0.847`),
`m ≥ 1` at `0.2`, `m ≥ 3` at `0.1`; (L) always works.  `κ_m` at `p = 0.3`: `0.847, 0.323, 0.128, 0.051, 0.021, 0.008`.

### 3.3 Brute force  (`code/y01_reductions.py`, `out/y01_reductions.txt`, 6.5 s)

36 random inhomogeneous chains (27 with 8, 9, 10 binary sites, 9 with 6 ternary sites), random fields, couplings with standard
deviation up to `2.5`, random asymmetric envelopes, random cuts, gaps and gauges; residuals: inf-convolutions of random
functions, their maxima, minima and convex combinations, all pairs `(x,y)` checked.

| statement | cases | result |
|---|---|---|
| (U) identity `ln A_π(ψ) = ln A_ρ(ψ+g) − ln A_ρ(g)` | 432 | `≤ 1.3·10⁻¹⁵` |
| (U) `ψ + g ∈ 𝒞_{d⁺}` | 432 | largest violation `7·10⁻¹⁵`; `d⁺` attained (slack left by cones `4·10⁻¹⁵`) |
| control: `ψ + g ∈ 𝒞_d` (no slack) | 432 | violated in 432 |
| (L) marginal `= ⊗π_{B_j}·Πρ_j` | 36 | `6·10⁻¹⁶` |
| (L) two-sided bound | 432 | never violated |
| (L′) `ψ ∈ 𝒞_d` and `A_π(ψ) = A_⊗(ψ′)` | 252 | `2·10⁻¹⁵`, `3·10⁻¹⁵` |
| control: `ψ′ ∈ 𝒞_d` instead of `𝒞_{d⁻}` | 252 | violated in 225 |

---

## 4. Step 2 — the sandwich, the limit, the regularised theorem

### 4.1 The whole chain is one super-site: lower bounds need no product structure

**Lemma A (every algorithm, every `n`, any reference measure) [proved from Theorem 11.27(a), (b) [V]].**  Let `(X, π, d)` be
any finite space with a law of full support and an envelope.  For every probability vector `M` on finitely many members of
`𝒞_d` and `0 < t < 1` let `γ*(x) := −t⁻¹ ln Σ_φ M(φ) e^{−tφ̃(x)}`.  Then `γ* ∈ 𝒞_d`, `π_{γ*} ∝ (Σ_φ M π_φ^t)^{1/t}`, and every randomised
`(ε/2, δ)`-correct algorithm — adaptive or not, with any hint — makes at least `(1 − 2δ)·exp(G_t(M) − tε)` evaluations at `γ*`.
*Proof.*  `𝒞_d` is closed under soft minima.  `Φ_φ := φ̃ − γ̃*` is Lipschitz for the slack of `γ*` and `E_{π_{γ*}}e^{−Φ_φ} = 1`, so
`γ* − (r − Φ_φ)₊ ∈ 𝒞_d` raises `ln A` by at least `r` (11.27(a)).  By 11.27(b) with the weights `M` and `r ↓ ε`:
`(1−2δ) ≤ E|Q|·e^{tε}·max_x Σ_φ M(φ)(π_φ(x)/π_{γ*}(x))^t`, and `Σ_φ M(φ)π_φ(x)^t/π_{γ*}(x)^t = (Σ_x(ΣMπ_φ^t)^{1/t})^t = e^{−G_t(M)}` for every `x`.  ∎
For the chain: `X = Π𝒮_i`.  With `F*_n := F*_X`, the exponent of every algorithm is at least `sup_t[F*_n(t) − tε]/n` **for every `n`**,
and the threshold of the `n`-chain is exactly `E_n = min_Q max_φ KL(Q‖π_φ)` (Theorem 11.28(d) with its remark (i), and Theorem 11.99
for the identification; [P]).

**Lemma B (product theorem) [proved, given strong duality for each factor].**  If `X = X₁ × X₂`, `π = π₁ ⊗ π₂`, `d = d₁ + d₂`, then
`F*_X(t) = F*_{X₁}(t) + F*_{X₂}(t)` for `0 < t < 1` (hence also `E` and `a` add).
*Proof.*  `≥`: product labels with `M₁ ⊗ M₂`.  `≤`: let `Q_i` attain `c_i := min_Q max_{φ_i}(1−t)D_t(π_{i,φ_i}‖Q) = F*_{X_i}(t)`.  For `φ ∈ 𝒞_d`,
`Σ_x π_φ^t (Q₁⊗Q₂)^{1−t} = Z_φ^{−t} Σ_{x₁} π₁^t Q₁^{1−t} Σ_{x₂} (π₂ e^{−φ(x₁,·)})^t Q₂^{1−t} ≥ Z_φ^{−t} e^{−c₂} Σ_{x₁} π₁^t Q₁^{1−t} W(x₁)^t ≥ e^{−c₁−c₂}`,
`W(x₁) := E_{π₂}e^{−φ(x₁,·)}`: first because `φ(x₁,·) ∈ 𝒞_{d₂}`, then because `−ln W ∈ 𝒞_{d₁}` **(this uses the product structure of `π`)**
and `E_{π₁}W = Z_φ`.  Weak duality.  ∎  (This is "one common `t`" of Theorem 11.98(b) for two super-sites, with a
three-line proof; numerically: §2.)

**Lemma C (monotonicity; bounded changes of the law) [proved].**  (i) A larger envelope gives a larger `F*`.  (ii) If
`π′ = π e^{−g}/Z`, the family of Gibbs laws of `(π′, 𝒞)` is that of `(π, 𝒞 + g)`.  (iii) If `osc ln(dπ′/dπ) ≤ c`, then
`|F*[π′](t) − F*[π](t)| ≤ tc` and `|E[π′] − E[π]| ≤ c`.  (iv) If `φ′ ≤ φ ≤ φ′ + c`, then `(1−t)D_t(π_φ‖Q) ≤ (1−t)D_t(π_{φ′}‖Q) + tc` for all `Q`.
*Proof of (iii), (iv).*  `π′_φ/π_φ` resp. `π_φ/π_{φ′}` lies in `[e^{−c}, e^{c}]` pointwise; insert into `Σ P^t Q^{1−t}`.  ∎

### 4.2 Exact sub- and super-additivity

For a segment of `L` consecutive sites of a homogeneous chain let (per segment, not per site)

    F⁺_L(t) := F*[ free-boundary Gibbs law of the segment (with the gauge fields);  d⁺ = d + δ⁺ at its first site, + δ⁻ at its last site ],
    F⁻_L(t) := F*[ marginal law π_L of the segment;  d⁻ = d − ε⁺ at its first site, − ε⁻ at its last site ]      (ε^± from ρ₀, i.e. m = 0),
    F⁻_{L,m}(t) := the same with ε^± from ρ_m,        F_L(t) := F*[π_L; d]   ("plain").

**Proposition D [proved].**  (a) `F⁺_{L₁+L₂} ≤ F⁺_{L₁} + F⁺_{L₂}` for all `t ∈ (0,1)`: **exactly sub-additive**.
(b) `F⁻_{L₁+L₂} ≥ F⁻_{L₁} + F⁻_{L₂}` and `F⁻_{L₁+m+L₂, (outer ends)} ≥ F⁻_{L₁,m} + F⁻_{L₂,m}`: **exactly super-additive**.
(c) `F⁺_L(t) − F⁻_L(t) ≤ t·C` with `C = Δ + c_bd`, `Δ` the `d⁺`-diameter of the two end sites, `c_bd` the oscillation of the log-density
between the free-boundary law and the marginal law of a segment (`0` for the symmetric chain; `C = 2(u + K)` there).
(d) Hence `F_∞(t) := lim_L F⁺_L(t)/L = inf_L F⁺_L(t)/L = sup_L F⁻_L(t)/L` exists, `F⁻_L/L ≤ F_∞ ≤ F⁺_L/L` **for every `L`**, also
`F⁻_{L,m}(t)/(L+m) ≤ F_∞(t)`, `|F*_n(t) − nF_∞(t)| ≤ tC`, `E_∞ := lim_{t↓0}F_∞(t)/t = lim E_n/n`, and `F_∞(t)/t` is nonincreasing,
`F_∞(t)/(1−t)` nondecreasing.  (If `d − ε^±` has negative entries at `m = 0` — for the symmetric chain if `u ≤ K` — read `F⁻_L` as
`F⁻_{L,m}` with the smallest admissible gap and `L` as `L + m` in the lower bracket; (c), (d) hold with `C` enlarged by `m·max F⁺_1`.)
*Proof.*  (a) The free-boundary law of the long segment is `ρ_{L₁}⊗ρ_{L₂}e^{−J°(cut)}/Z`.  For `φ` in its class, `φ + J°(cut)` is in the
class of the product landscape with slack at the outer ends *and* at the cut (Theorem Y1), and the Gibbs laws coincide
(Lemma C(ii)).  So the family of the long segment is a sub-family of that of the product landscape; Lemma C(i) and Lemma B.
(b) `π_{L₁+L₂} = π_{L₁}⊗π_{L₂}·ρ₀(cut)`.  For `φ_i` in the `d⁻`-classes, `φ₁ + φ₂ + ln ρ₀(cut)` is in the class of the long segment
(Theorem Y3) with Gibbs law `π_{φ₁}⊗π_{φ₂}`: the long family contains all products; the easy direction of Lemma B.  With a gap,
marginalise the gap (Rényi divergences decrease).  (c) For `φ` in the `d⁺`-class let `φ⁻` be its minimum over the two end
letters: it ignores them, is Lipschitz with `d` in the interior, hence lies in the `d⁻`-class, and `0 ≤ φ − φ⁻ ≤ Δ`; Lemma C(iv),
(iii).  (d) Fekete's lemma twice; `F⁻_L ≤ F*_L`-type comparisons by Lemma C; the monotonicities are inherited from finite `L`.  ∎
*The plain `F_L/L` is neither monotone nor a bound* (`F*_n(0.45)/n` at `p = 0.4`: `0.02895, 0.03280, 0.03359, 0.03354` for `n = 1..4`); it
is within `tK/L` of `F_∞` (measured: `|F*_{n₁+n₂} − F*_{n₁} − F*_{n₂}|/(tK) ≤ 0.09` for `n₁ + n₂ ≤ 4`, `y04`).  Numerical check of (a)–(c) at
`t = 0.3, 0.45, 0.7` (`y08`): `F⁺_2 − 2F⁺_1 = −0.041…−0.114`, `F⁺_3 − F⁺_1 − F⁺_2 = −0.039…−0.115` (`p = 0.4, 0.3`);
`F⁻_2 − 2F⁻_1 = +0.019…+0.023`, `F⁻_3 − F⁻_1 − F⁻_2 = +0.027…+0.035`, `(F⁺_3 − F⁻_3)/(tC) ≤ 0.096` (`p = 0.4`, where `u > 2K`).
*Open side question:* whether `inf_L a⁺_L/L` (capacities of the slack blocks) equals `a_∞ := sup_t F_∞(t)/(1−t) = sup_L a⁻_L/L`; the
bound (c) degenerates as `t → 1` (**not proved**; it is not needed below, where accuracies are positive).

### 4.3 The regularised theorem

**Theorem E (regularised formula for a homogeneous nearest-neighbour chain).**  Let `R̂_∞(e) := max_{0≤t≤1}[F_∞(t) − te]`,
`θ_∞(x) := max_{0≤τ<1}(F_∞(τ) − τx)/(1−τ)`, `h_∞ := R̂_∞(0)`, `a_∞ := sup_τ F_∞(τ)/(1−τ)`, `E_∞ := lim_{t↓0}F_∞(t)/t`.
(a) **[proved; every `n`; only Theorem 11.27(b) [V]]** Every `(ε₁n/2, δ)`-correct algorithm makes at least
`(1−2δ)exp(F*_n(t) − tε₁n) ≥ (1−2δ)exp(n[F_∞(t) − tε₁] − tC)` evaluations at the instance `γ*_{n,t}` (the Rényi centre of the
whole chain), for every `t`: the exponent of every algorithm — hinted, adaptive or not — is at least `R̂_∞(ε₁)`.
(b) **[proved given Theorem 11.101(b), unrefereed]** For fixed `L`, `n = kL → ∞` and `0 < ε₁ < E⁺_L/L`, the least worst-case cost of
adaptive algorithms without a hint is at most `exp(n·max_t[F⁺_L(t)/L − tε₁] + o(n))` (Theorem Y1, then 11.101(b) for the
landscape of `k` super-sites with alphabet `𝒮^L`).  Since `0 ≤ F⁺_L/L − F_∞ ≤ tC/L`: `lim_L lim_k n⁻¹ ln(cost) = R̂_∞(ε₁)` for
`0 < ε₁ < E_∞`; above `E_∞` a bounded number of evaluations suffices (11.28(i)).  The hardest instance with a hint has the same exponent.
(c) **[proved given Theorems 11.95, 11.98(d), unrefereed]** Non-adaptive algorithms: for all `L, m` and `ε₁ > 0`,
`max_τ(F⁻_{L,m}(τ)/(L+m) − τε₁)/(1−τ) ≤ liminf n⁻¹ ln(cost) ≤ limsup ≤ max_τ(F⁺_L(τ)/L − τε₁)/(1−τ)` (lower: Theorem Y3 and the
every-`n` bound of 11.98(d); upper: Theorem Y1 and the joint-type-stratified sample of the block landscape), and both sides
tend to `θ_∞(ε₁)` as `L → ∞` at fixed `m` (the maximiser stays below `τ = a⁺_1/(a⁺_1 + ε₁)`, `a⁺_1` the capacity of the slack block of one
site, so the upper side is within `a⁺_1 C/(ε₁L)` and the lower side within `O((C + m)a⁺_1/(ε₁L))`).  `a_∞ = lim_{ε₁↓0}θ_∞(ε₁)`.
(d) *Uniformity.*  The lower bound (a) is for every `n`.  The `o(n)` of (b), (c) depends on `L` through the alphabet `q^L`
(the error term of Theorem 11.97 is `n^{−1/(2q^L+2)}`, `N_orb` is a polynomial of degree `q^L − 1`): **the limits are iterated,
`n → ∞` at fixed `L`, then `L → ∞`; nothing is uniform in `L` and no finite-`n` upper bound follows.**  If `n` is not a multiple
of `L`, condition on the `r < L` remaining letters: each of the `q^r` conditional problems embeds into the same block landscape
(the boundary coupling goes into the slack of the last block), at `q^r` times the cost.
(e) *Regularised (multi-letter) form.*  `F_∞(t) = lim_L L⁻¹(1−t)·C_t(vertex channel of the L-block)` with either choice of the
boundary treatment; the capacity is not single-letter: the optimal label laws are correlated along the chain (§6.4, §7).
*Inhomogeneous chains* **[sketch]**: Theorems Y1–Y3, Lemmas A–C and the two-block inequalities of Proposition D hold verbatim;
for a periodic sequence take `L` a multiple of the period; for a stationary ergodic sequence of finitely many site types and
couplings `F^±` are sub-/super-additive processes (Kingman) and the blocks have finitely many types with frequencies, as §11.26 requires.

---

## 5. Sharper bounds on the game function (beyond the brief; needed to answer its question)

### 5.1 The Markov recursion ("DP"): one-sided slack

**Proposition F [proved].**  Let `π(x) = π₁(x₁)Π_{i≥2}P_i(x_{i−1},x_i)`, `φ ∈ 𝒞_d`, `Q` any Markov chain with kernels `q_i`, `0 < t < 1`.  Define
envelopes backwards: `d*_n := d_n`, `d*_i := d_i + G_i`,
`G_i(a,a′) := max{ ln[Σ_b P_{i+1}(a′,b)w(b)/Σ_b P_{i+1}(a,b)w(b)] : w > 0, w(b′) ≤ w(b)e^{d*_{i+1}(b,b′)} }`.  Then

    Σ_x π_φ(x)^t Q(x)^{1−t} ≥ Π_i c_i,     c_i := min_b min_{γ∈Lip(d*_i)} Σ_a q_i(b,a)^{1−t} ( P_i(b,a)e^{−γ(a)}/Z )^t,
    F*_n(t) ≤ Σ_i max_b F*[ site law P_i(b,·); envelope d*_i ](t).

*Proof.*  `V_i(x_{≤i}) := E_π[e^{−φ} | x_{≤i}]`.  (1) `−ln V_i` is Lipschitz in the coordinate `x_i` with `d*_i` and in earlier
coordinates with `d_j`: `V_i(…,a′) = Σ_b P_{i+1}(a′,b)V_{i+1}(…,a′,b) ≤ e^{d_i(a,a′)}Σ_b P_{i+1}(a′,b)V_{i+1}(…,a,b)`, and
`w := V_{i+1}(…,a,·)` satisfies the constraint of `G_i` by induction.  (2) `U_i(x_{≤i}) := E_Q[Π_{j>i}(P_j/q_j)^t e^{−tφ} | x_{≤i}]` satisfies
`U_{i−1} = Σ_a q_i^{1−t}P_i^t U_i ≥ c_{i+1}⋯c_n Σ_a q_i^{1−t}(P_iV_i)^t ≥ c_i⋯c_n V_{i−1}^t` (the conditional law of `x_i` under `π_φ` is
`P_i(b,·)V_i/V_{i−1}`, a Gibbs law of a member of `Lip(d*_i)`).  (3) `Σπ_φ^tQ^{1−t} = U_0/V_0^t`; minimise `−ln c_i` over `q_i(b,·)`; weak duality.  ∎
*Block version.*  The chain of `L`-blocks is a Markov chain; the same proof gives, for the homogeneous chain,
`F_∞(t) ≤ F^{DP}_L(t)/L`, `F^{DP}_L := max_b F*[ P^{(L)}(· | previous letter b); envelope (d, …, d, d*) ]`, with `d*` the fixed point of the
site recursion, and `F^{DP}_L` is sub-additive.  Binary symmetric chain: `d*` is the slope `u* = u + g(u*)`,
`g(x) = ln[((1−p)eˣ + p)/(peˣ + 1−p)] < K`: **slack `g(u*)` at one end** instead of `K` at both
(`u* = 1.218, 1.526, 1.981, 2.750` for `p = 0.4, 0.3, 0.2, 0.1`).  It is a bound on the game function, not an algorithmic reduction.
*Tests (`y04`, `y08`):* the finite-`n` form holds for the exact `F*_n` (`n ≤ 4`, 60 cases); the inequality itself on 300 random
inhomogeneous binary chains with random members (not only vertices) and random Markov `Q`: smallest ratio `1.129 ≥ 1`.

### 5.2 The tilt-state recursion

Binary symmetric chain; `τ_λ(b,·)` := the law `P(b,·)` tilted by `λ` (`τ_λ(b,±) ∝ P(b,±)e^{±λ/2}`).

**Proposition G [proved].**  For `φ ∈ 𝒞_d` let `λ_i(x_{<i}) := ln V_i(x_{<i},+)/V_i(x_{<i},−)`.  Then `π_φ(x_i = · | x_{<i}) = τ_{λ_i(x_{<i})}(x_{i−1},·)`,
`Σ_x π_φ^t Q^{1−t} = Σ_x Π_i τ_{λ_i(x_{<i})}(x_{i−1},x_i)^t q(x_{i−1},x_i)^{1−t}`, `|λ_i| ≤ u*`, and for every prefix there are `θ_± ∈ [−u, u]` with
(`μ_a := λ_{i+1}(x_{<i},a)`)

    μ₊ = μ₋ + θ₊ − θ₋,        λ_i = ln[(1−p)e^{θ₊+μ₋} + pe^{θ₋}] − ln[pe^{μ₋} + 1 − p].                                        (★)

Consequently, with `(TW)(b,λ) := min{ Σ_a τ_λ(b,a)^t q(b,a)^{1−t} W(a,μ_a) : (λ,μ₊,μ₋) satisfies (★) }` on functions of (previous letter,
tilt): `F*_n(t) ≤ max_φ(1−t)D_t(π_φ‖Q) ≤ −ln min_{b,λ}(Tⁿ1)(b,λ) + O(1)`, and **for every positive `W`**
`F_∞(t) ≤ −ln min_{b,λ}(TW/W)(b,λ)` (`T` is monotone and positively homogeneous).  The analogues with rewards: `E_∞ ≤` the growth of
`W ↦ k_b(λ) + max Σ_a P(b,a)W(a,μ_a)`, `k_b(λ) = KL(P(b,·)‖τ_λ(b,·))` (reference `Q = π`), and `a_∞ ≤` the growth of
`W ↦ KL(τ_λ(b,·)‖q(b,·)) + max Σ_a τ_λ(b,a)W(a,μ_a)`.
*Proof.*  `θ_c := ln V_{i+1}(x_{<i},+,c)/V_{i+1}(x_{<i},−,c) ∈ [−u,u]`, because given `x_{i+1} = c` the law of the future does not depend
on `x_i` and `φ` changes by at most `u`; (★) is `V_i(…,a) = Σ_c P(a,c)V_{i+1}(…,a,c)` written in these ratios.  The set of all tilt
processes with (★) contains those of members of `𝒞_d`; over that set the minimum has the tree-recursive form `Tⁿ1`.  ∎
*It is a relaxation* (only one-step consistency is kept).  **[numerical]** For `n = 3, 4` and symmetric Markov `Q` with `q̃ ≥ p` its
value (adversary's controls on a grid of 41 × 41 values of `θ_±`, which can only underestimate it) equals the exact maximum over
*all* vertices to 6 digits in 36 cases, and for `KL(π‖π_φ)` to 7 digits in 6 cases (`y10`, part 1).  No such test was made for
`q̃ < p`, where the optimal controls are not at the ends of `[−u, u]`; at `p = 0.1` and large `n` the relaxation is *not* tight (§5.4(d)).
*Conservative discretisation* **[proved]** (`ydp3.py`).  Tilt grid of spacing `D` on `[−u*, u*]`; children's tilts on the grid; the
feasible set (★) enlarged by `1.5D` in `θ_±` (these are 1-Lipschitz in `λ, μ₊, μ₋`); stage factors replaced by their minimum
(maximum, for rewards) over the cell of `λ`.  By induction over the levels the grid value bounds the relaxed value on the safe
side for every `λ` of the cell, so `−ln min(T̂W/W)` is an upper bound for `F_∞(t)` for any grid; it converges like `D`.  The
restriction of the adversary to grid tilts gives the bracket's other end.  Range-minimum queries make a sweep `O(G²)`.
(Rewards: `k_b` is convex in `λ`, so its maximum over a cell is at the ends; for `a`, the reward gets a curvature slack `2D²` and the
transition weights are the minima over the cell, applied to a value function normalised to be `≤ 0`; the resulting operator is
monotone and commutes with adding constants, so `max(T̂W − W)` bounds the growth for every `W`, converged or not.)
*Controls (`y15`):* for `p = ½` the restricted mode returns the cube exactly (`0.0291391`, `0.1201145`, `0.1109441`) and the safe mode
approaches it from above (`G = 3201`: `0.0292072`, `0.1201867`, `0.1110063`); `n = 4`: exact maxima `≤ 4×` safe rate in 18 cases.

### 5.3 Lower bounds: the Lyapunov form for site-wise labels

`Ξ_{κ,η}(b) := Σ_τ exp(κΣ_i b_iτ_iτ_{i+1} + ηΣ_iτ_i)` (an Ising chain with bonds `κb_i`, `b_i = ±1`, in the uniform field `η`; a product
of `2×2` matrices), `L_q(κ,η;r) := lim n⁻¹ ln E[Ξ_{κ,η}(b)^r]` for i.i.d. bonds with `P(b = −1) = q` (a moment Lyapunov exponent).

**Proposition H (site-wise labels with a tilted Markov law) [proved].**  Let `M_c(σ) ∝ M₀(σ)Z(σ)^t`, `M₀` the symmetric Markov
chain on label sequences with coupling `c` (`P(σ_iσ_{i+1} = −1) = p_c := 1/(1+e^{2c})`).  For every `n`

    G_t(M_c) = ln E_{β∼p_c}[Ξ_{K′,h}(β)^t] − t ln E_{b∼p}[Ξ_{c,th}(b)^{1/t}] − t ln Z₀(K′) + ln Z₀(c),      Z₀(x) = 2(2cosh x)^{n−1},
    F_∞(t) ≥ G_∞(t;c) := L_{p_c}(K′,h;t) − t·L_p(c,th;1/t) − t ln(2cosh K′) + ln(2cosh c),

and by Lemma A every algorithm makes at least `(1−2δ)exp(G_t(M_c) − tε)` evaluations at the instance with Gibbs law
`∝ π·E_{M₀}[e^{thσ·s}]^{1/t}`.  For `c = 0` that instance is the **zero residual**, and
`G_∞(t;0) = L_{½}(K′,h;t) − t ln(2cosh K′) − ln cosh(th) ≤ t ln cosh h − ln cosh(th)` (the cube; Jensen, strict for `K ≠ 0`).
*Proof.*  `Σ_σ M_c π_σ^t = π^t·E_{M₀}e^{thσ·s}·(Z₀(K′)^t/N)`, `N = E_{M₀}Z(σ)^t`; gauge `τ_i = σ_is_i`: `Z(σ) = Ξ_{K′,h}(σ_iσ_{i+1})` and
`E_{M₀}e^{thσ·s} = Ξ_{c,th}(s_is_{i+1})/Z₀(c)`; the bonds `σ_iσ_{i+1}` are i.i.d. under `M₀`, the bonds `s_is_{i+1}` under `π`.  ∎
(A duality `(K′, h, t; p_c) ↔ (c, th, 1/t; p)`.)  *Numerics* (`ylyap.py`): transfer operator on the direction of the partial
partition vector, Chebyshev collocation; `N = 32, 48, 64` agree to `10⁻¹²`; exact increments of `ln E[Ξ^r]` converge geometrically to
it (`y08`(d)); the formula against the brute-force Rényi form on `n = 8` (256 × 256), 27 cases: `2·10⁻¹⁵`.

**Proposition I (label laws i.i.d. over blocks, exact boundary term) [proved].**  Let `M_L` be any law on labels of an `L`-block
(plain slopes), `Q` its Rényi centre, `B_φ(a,b) := π_{L,φ}(first letter a, last letter b)`, `ρ₀ = 2P`.  For the law
`M ∝ M_L^{⊗k}·c_φ^t` on block-wise labels, `c_φ = 1ᵀB_{φ₁}ρ₀B_{φ₂}ρ₀⋯B_{φ_k}1`:

    G_t^{(kL)}(M) = k·G_t^{(L)}(M_L) + ln E_{M_L^{⊗k}}[c_φ^t] − t ln E_{⊗Q}[Πρ₀],        F_∞(t) ≥ [ G_t^{(L)}(M_L) + Λ_blk(t) − t ln λ_max(B_Qρ₀) ]/L,

`Λ_blk(t)` the moment Lyapunov exponent of order `t` of the i.i.d. product of the matrices `B_φρ₀`, `φ ∼ M_L` (`λ_max(B_Qρ₀) = 1` for
symmetric `M_L`).  *Proof:* `π_φ = Ππ_{L,φ_j}·Πρ₀/c_φ`; the tilt cancels `c_φ`.  ∎  *Checks:* brute-force Rényi form on `n = 6` (64 labels)
and `n = 9` (512 labels): `10⁻¹²`; headline values re-evaluated independently (`y16`): `G_L` from `M_L` without a solver, `Λ_blk` with
`N = 40, 80` and against exact increments of `ln E[c^t]` over `k = 1, 2, 3` blocks (agreement `10⁻⁷…10⁻⁵`).

### 5.4 The threshold

**Proposition J.**  (a) **[proved, every `n`]** `E_n ≥ ln Z_n(h)/Z_n(0)`, hence
`E_∞ ≥ E_F := ln[(1−p)cosh(u/2) + √((1−p)²sinh²(u/2) + p²)]` (`> ln cosh(u/2)` for `p ≠ ½`).
*Proof.*  For the two uniform-field labels, `½[KL(Q‖π₊) + KL(Q‖π₋)] = KL(Q‖π) + ln E_πe^{hm} ≥ ln Z_n(h)/Z_n(0)` for every `Q`.  ∎
Equality `E_n = ln Z_n(h)/Z_n(0)` holds iff the uniform field maximises `KL(π‖π_φ)` over `𝒞_d` (then `Q* = π`).
(b) **[numerical, exact enumeration]** `E_n = ln Z_n(h)/Z_n(0)` to `10⁻¹¹` for `n ≤ 4` (`p = 0.4, 0.3, 0.1`) and `n = 5` (`p = 0.3`, dual
certificate over all 395 094 vertices).  Successive linearisation of `KL(π‖π_φ)` (LP ascent) on `n = 8, 10, 12`, `p = 0.3, 0.2, 0.1, 0.05`,
8–12 starts each: no member of `𝒞_d` above the uniform field (`y14`).
(c) **[numerical evaluation of the proved bound of Proposition G]** the relaxed growth of `max KL(π‖π_φ)` in the grid-restricted
mode equals `E_F` to 7 digits for `p = 0.4, 0.3, 0.2`; the safe value exceeds `E_F` by `1.0, 1.4, 1.9·10⁻⁴` at `G = 3201` and halves
with the spacing.  So **`E_∞ = E_F` for `p = 0.4, 0.3, 0.2` up to these margins.**
(d) For `p = 0.1` the relaxed problem has the value `≥ 0.42389 > E_F = 0.40172`: the relaxation is not tight (or the uniform field
stops being optimal for long chains); `E_∞ ∈ [0.40172, 0.41799]` (upper end: Proposition F, `L = 3`).
**Conjecture:** `E_n = ln Z_n(u/2)/Z_n(0)` for every `n` and `p`.  (Second order in `u` this is Newman's covariance inequality for
associated spins — [known], recalled from memory, not looked up; I have no proof of the exponential statement.)

---

## 6. Step 3 — numbers (binary symmetric chain, `u = 1`, per site)

Cube: `h = 0.029139`, `a = 0.110944`, `E = 0.120115`.  Every entry of §§6.1–6.2 is a duality bracket of width `≤ 3·10⁻⁸`
(`h`: bracket at the maximising `t`, located by a coarse scan and golden section; one local maximum in all scans).

### 6.1 (a) Upper bounds from (U), `L = 1, 2, 3`, all vertices  (`y02`)

Block law = stationary `L`-marginal, slopes `(u+K, u, u+K)` etc.; `|𝒱| = 2, 6, 120`.

| `p` | `h ≤` (`L = 1, 2, 3`) | `a ≤` | `E ≤` |
|---|---|---|---|
| `0.4` | `0.08302, 0.05804, 0.04948` | `0.28723, 0.19792, 0.17181` | `0.36375, 0.26437, 0.23243` |
| `0.3` | `0.15031, 0.09387, 0.07428` | `0.45721, 0.28620, 0.23680` | `0.71954, 0.47295, 0.39226` |
| `0.2` | `0.22525, 0.13205, 0.10025` | `0.58562, 0.35982, 0.29177` | `1.21588, 0.76151, 0.61087` |
| `0.1` | `0.31125, 0.17250, 0.12692` | `0.66423, 0.41025, 0.32951` | `2.00861, 1.20471, 0.93694` |

### 6.2 (b) Lower bounds from (L′), (L) with small `L`, `m`, all vertices  (`y02`)

Best over `m ≤ 5` (the best `m` in brackets); (L) = accuracy version `max_t[F_L(t) − tκ_m]/(L+m)`.

| `p` | `h ≥` (L′), `L = 1, 2, 3` | `h ≥` (L), `L = 3` | `a ≥` (L′), `L = 3` | `E ≥` (L′), `L = 3` |
|---|---|---|---|---|
| `0.4` | `0.01049 (1), 0.01891 (1), 0.02307 (1)` | `0.01873 (2)` | `0.07987` | `0.10199` |
| `0.3` | `0.00595 (3), 0.01465 (2), 0.02088 (2)` | `0.01629 (3)` | `0.06978` | `0.09375` |
| `0.2` | `0.00329 (5), 0.01031 (4), 0.01742 (3)` | `0.01251 (5)` | `0.05681` | `0.07830` |
| `0.1` | `— (needs m ≥ 6), 0.00327 (5), 0.01020 (5)` | `0.00153 (5)` | `0.03518` | `0.04459` |

(L′) beats (L) at small gaps and coincides with it at large gaps.  **These brackets contain the cube's values and are a factor
2–10 wide: block reductions with `L ≤ 3` do not decide the question** — the boundary terms are `O(1)` per block against
`F_∞ ≈ 0.04` per site.  (All entries: `out/y02_blocks_a.txt`, `_b.txt`; for `p = 0.1` and `L = 1` the reduced slope `u − 2κ_m` is negative for all `m ≤ 5`.)

### 6.3 Upper bounds from the Markov recursion (Proposition F) and the tilt-state recursion (Proposition G)

| `p` | DP: `h ≤` (`L = 1, 2, 3`) | DP: `a ≤` (`L = 3`) | DP: `E ≤` (`L = 1, 2, 3`) | tilt-state, safe, `G = 801`: `h ≤` | `a ≤` | `E ≤` (`G = 3201`) |
|---|---|---|---|---|---|---|
| `0.4` | `0.04053, 0.03889, 0.03736` | `0.12970` | `0.16935, 0.16921, 0.16917` | **`0.036163`** | **`0.121446`** | `0.169228` |
| `0.3` | `0.05484, 0.05180, 0.04902` | `0.15401` | `0.23419, 0.23324, 0.23285` | **`0.044995`** | **`0.140860`** | **`0.232538`** |
| `0.2` | `0.07202, 0.06672, 0.06197` | `0.17747` | `0.31886, 0.31554, 0.31376` | **`0.054353`** | **`0.160745`** | **`0.310956`** |
| `0.1` | `0.09157, 0.08299, 0.07542` | `0.19678` | `0.43245, 0.42378, 0.41799` | **`0.066765`** | **`0.192774`** | `0.426314` |

Tilt-state: symmetric Markov reference with flip probability `q̃` optimised on a grid for every `t` (optimal `q̃ < p`: a *more
ferromagnetic* centre, e.g. `q̃ ≈ 0.255–0.26` at `p = 0.3`); `h ≤` is a bound over **all** `t ∈ (0,1)`: on every interval `[t₁,t₂]` of an
adaptively refined grid, `F_∞(t) ≤ min(B(t₁)t₂/t₁, B(t₂)(1−t₁)/(1−t₂))`; largest grid values `0.036030, 0.044821, 0.054138, 0.066539`.
At `p = 0.3`, `t = 0.43`, `q̃ = 0.255` the two ends of the discretisation are `0.04468` (safe, `G = 1601`) and `0.04435` (restricted): finer
grids would lower the `h`-bound to about `0.0446`.  With `Q = π` the worst label is the uniform field and the bound is the closed
form `tE_F(u) − E_F(tu)` (`0.04886` at `t = 0.43`, `p = 0.3`).

### 6.4 Lower bounds from site-wise labels on long chains  (`y03`, `y06`, `y07`, `y16`)

| `p` | tilted Markov labels, `n → ∞` (Prop. H): `h ≥` (`t*`, `c*`) | i.i.d. labels (`c = 0`) | block-wise labels, `≤ 2` walls per block (Prop. I): `h ≥` (`L`, `t`) | `a ≥` (best of both) | `E ≥ E_F` |
|---|---|---|---|---|---|
| `0.4` | `0.033503` (`0.458`, `0.774`) | `0.028907` | **`0.034026`** (`12`, `0.459`) | **`0.116817`** | **`0.169127`** |
| `0.3` | `0.038695` (`0.431`, `0.859`) | `0.028151` | **`0.040115`** (`14`, `0.434`) | **`0.126444`** | **`0.232400`** |
| `0.2` | `0.041770` (`0.402`, `0.861`) | `0.026626` | **`0.044599`** (`14`, `0.409`) | **`0.129797`** | **`0.310766`** |
| `0.1` | `0.039608` (`0.364`, `0.833`) | `0.023418` | **`0.044378`** (`14`, `0.380`) | **`0.116632`** | **`0.401719`** |

*How the normalisation `Z(φ⃗)^{−t}` inside the power mean is handled.*  For `L ≤ 12` exactly, by enumeration over all `2^L` label
sequences and all `2^L` configurations with the optimal label law (Arimoto; `p = 0.3`, `t = 0.431`: `0.039856, 0.040183, 0.040243,
0.040328` per site for `n = 6, 8, 10, 12`, increments `(F_n − F_{n−2})/2 = 0.04117, 0.04048, 0.04075`).  Beyond: the label law is tilted
by `Z^t` (resp. `c_φ^t`), which cancels the normalisation and turns both sums into moment Lyapunov exponents of `2×2` matrix
products (Propositions H, I) — exact in the limit `n → ∞`, no block-boundary loss.
*Reading.*  The optimal label law is **sparse and slowly varying** (8, 12, 18, 40 labels of `2ⁿ` at `n = 6..12`; a label flips at the
middle bond with probability `0.085` at `n = 12`), not a first-order Markov law (which loses `≈ 4 %`); the best fixed domain length
is `3, 4, 5, 5` sites for `p = 0.4, 0.3, 0.2, 0.1` (`≈ 2K/u`).  **Best estimate** of `h` at `p = 0.3` **[numerical, not a bound]**:
`0.0405–0.041`, from the increments, under the assumption — true for `n ≤ 5` at `p = 0.3` — that site-wise labels are optimal.

### 6.5 Brackets, the answer, slope dependence, strong coupling

Final brackets: the table of §0.2 (lower ends: bold entries of §6.4; upper ends: bold entries of §6.3, for `E` at `p = 0.4, 0.1` the
DP value).  Ratios to the cube: `p = 0.4`: `h ×[1.168, 1.241]`, `a ×[1.053, 1.095]`, `E ×1.408`; `p = 0.3`: `h ×[1.377, 1.544]`,
`a ×[1.140, 1.270]`, `E ×1.935`; `p = 0.2`: `h ×[1.531, 1.865]`, `a ×[1.170, 1.449]`, `E ×2.587`; `p = 0.1`: `h ×[1.523, 2.291]`,
`a ×[1.051, 1.738]`, `E ×[3.344, 3.480]`.

*Slope dependence at `p = 0.3`* (`y09`; lower bound = tilted Markov labels, upper bound = DP with `L = 1`; `χ := (1−p)/p = 2.333`):

| `u` | `0.05` | `0.1` | `0.25` | `0.5` | `1` | `2` | `3` | `4` |
|---|---|---|---|---|---|---|---|---|
| `h`: lower bound / cube | `2.271` | `2.209` | `2.022` | `1.736` | `1.328` | `0.994` | `0.925` | `0.928` |
| `h`: upper bound / cube | `2.33` | `2.33` | `2.29` | `2.17` | `1.88` | `1.46` | `1.26` | `1.16` |
| `E_F`/cube | `2.332` | `2.327` | `2.294` | `2.194` | `1.935` | `1.546` | `1.348` | `1.243` |

**Small slopes: the exponents are multiplied by `χ = (1−p)/p`** (the susceptibility of the chain; labels constant over domains
much longer than the correlation length and much shorter than `1/u²`) — **[numerical]**, bracket `[2.27, 2.33]` at `u = 0.05`.
For `u ≥ 2` the lower bound is below the cube: **the direction for `h` at large slopes is not decided.**  `E_F > E_cube` for all `u`.
*Strong coupling at `u = 1`* (`y09`): `E_F → u/2` (`0.499` at `p = 0.001`).  The DP bound with `L = 1` saturates (`h ≤ 0.116`, `a ≤ 0.302`)
and the Markov-label lower bound for `h` falls below the cube at `p = 0.02` (`0.0274`): **nothing is decided for `p ≤ 0.05`**; label
domains of length `≈ 2K/u` still steer the chain, so the cost exponents can only decay like `u/K = u/ln(1/p)` **[heuristic]**.

---

## 7. Step 4 — structure

1. **Site-wise labels are not optimal in general** **[numerical, exact]**.  `n ≤ 4`, all vertices, `t = 0.25, 0.45, 0.65` and `E`,
`p = 0.4, 0.3, 0.1`: optimal weight on non-additive vertices `< 10⁻⁸`.  `n = 5`, `p = 0.3`: the site-wise centre is a dual certificate over
all 395 094 vertices for `t = 0.45`, for `E` and for `a`.  **But** `p = 0.1`: `a_4 = 0.5726559` against `0.5626014` with site-wise labels
only, weight `0.092` on the vertex `f(x) = −min(|x|, 4−|x|)` (minus the distance to the two ground states — a "paramagnetic" third
label next to "up" and "down"); and at `n = 5`, `t = 0.65` (`0.85`) the dual value of the site-wise centre over all vertices is
`0.25009` (`0.10662`) against the site-wise optimum `0.19396` (`0.09283`).  So at strong coupling and `t → 1` vertices that are
functions of the domain structure carry weight; all lower bounds of §6.4 remain valid, the true values at `p = 0.1` may be larger.
2. **The hardest instance is not additive, and the Rényi centre is not a Markov chain** **[numerical]**.  For short chains
(`n = 4`, `t = 0.45`) the optimal labels are the two uniform fields and `γ* = −t⁻¹ ln cosh(th·m)`, `m` the magnetisation: a function
of the type with no site terms; Walsh norms by order: `0, 0.245, 0, 0.009`; nearest-neighbour pair coefficient `−0.100`;
`I(x₁;x₃|x₂) = 2.9·10⁻³, 5.7·10⁻³, 1.2·10⁻³` under `Q*` for `p = 0.4, 0.3, 0.1` (zero under `π`); still `2·10⁻³` at `n = 12` (site-wise
optimum).  In the Markov-label family `γ* = −t⁻¹ ln Ξ_{c,th}(s_is_{i+1}) + const`: a function of the bonds with exponentially
decaying multi-body terms; it is the zero residual only for `c = 0`, which is not optimal.
3. **A Lyapunov-exponent form exists as a lower bound** (Propositions H, I) **[proved]**; whether `F_∞` itself has one is open
(it would need the optimal label process, which is neither Markov nor, at strong coupling, site-wise).
4. **Two-letter intuitions that fail here:** "the zero residual is the hardest instance without a field"; "labels are
independent from site to site"; "the centre inherits the Markov property".

---

## 8. Step 5 — the fixed sample

1. *What (U) and (L′) give for every `n`* **[proved given Theorem 11.95]**.  For `n = kL` the sample stratified by the joint type of
the `k` blocks (uniform in each class of the block landscape `(ρ, d⁺)`, `M = ⌈8 ln(2N_orb/δ)/q⌉` points per class,
`N_orb = C(k + q^L − 1, q^L − 1)`) is `(ε/2, δ)`-correct on the chain's class for `ε ≥ ε^{tr}_{(ρ,d⁺)}(q) + ln(4/δ)`; conversely every
non-adaptive algorithm for the chain needs `(1−2δ)/q` evaluations when `ε < ε^{tr}_{(⊗π_B, d⁻)}(q)`.  The two truncation functions
have the exponents of `F⁺_L/L` and `F⁻_{L,m}/(L+m)`: the loss is `e^{O(n/L)}`, not polynomial.
2. *The pair-type-stratified sample.*  `π` is uniform on Markov-type classes (first letter and pair counts), so
`A(ψ) = Σ_T π(T)·E_{unif(T)}e^{−ψ}`: the estimator is unbiased, and the proof of Theorem 11.95(a)(iii) gives its guarantee with
`ε^{tr}_{pair}(q) := sup_ψ ln[A(ψ)/A(ψ^{tr,q})]` (class-wise quantile truncation) — **[proved, same proof]**; `ψ^{tr,q}` need not be in the class.
3. **Negative [proved by example; brute force]:** the step that made the stratified sample *optimal* — class-wise upper
quantiles of an admissible residual are admissible (`lowDens_shift`) — **fails for Markov-type classes**.  Example (`u = 1`,
`n ≥ 5`, `q < 1/(n−2)`): `ψ = d(·, 0…010)`, `x = 110…0` (a singleton class, level `e^{−3}`), `y = 010…0` (in the class of `0…010`, level `1`),
`d(x,y) = 1`: `t_y = 1 > t_x·e = e^{−2}`.  Brute force (`n = 9`, 74 classes, 200 residuals × 3 quantiles): 598 violations of 600 for
Markov types (largest excess 6 flips), 0 for the type classes of the cube.  Reason: no group acts; a point of a class can be far
from every point of an adjacent class.
4. *Open:* an every-`n` optimality statement with polynomial losses; whether `ε^{tr}_{pair}` has the exponent `θ_∞`.

---

## 9. Step 6 — beyond chains  **[sketch]**

* *Strips of width `w`* are chains over the column alphabet `𝒮^w` with a nearest-neighbour column coupling: Theorems Y1–Y3,
Lemma A, Propositions D, F and Theorem E hold verbatim (slack `K` per cut bond; `ρ_m → 1` at the rate of the column transfer
matrix).
* *Boxes in `ℤ^d`, finite range.*  (U): cut bonds across block faces; slack on boundary sites only.  The argument of
Proposition D gives `F⁺_B` sub-additive, `F⁻_B` super-additive and `F⁺_B − F⁻_B ≤ t·C·|∂B|`, so **`F_∞ = lim F^±_B/|B|` exists along
boxes whatever the correlations** — the accuracy version (L) with `m = 0` only needs `|ln ρ| ≤ C|∂B|`, which is the energy
across the faces.  Decay of correlations is needed only to make the loss smaller than surface order.
* *Where the gap argument fails.*  At phase coexistence the marginal on distant blocks is a mixture of products
(`½⊗μ⁺_B + ½⊗μ⁻_B`), its density with respect to the product of the marginals is of order `2^{±k}` on `k` blocks and `ρ_m ↛ 1` for any
gap; the loss per block does not vanish but is `O(1)`, still negligible against `|B|`.  At a critical point `ln ρ_m` decays
like a power of `m`.
* *Trees and other non-amenable graphs.*  Theorems Y1–Y3 hold, but every block has boundary proportional to its volume, the
slack never becomes negligible, and the sandwich does not close; whether a regularised formula exists there is open.
* The Markov recursion (Proposition F) and the tilt-state recursion are one-dimensional (they use the Markov property along
a line); for strips they apply with column alphabets (state = a vector of tilts).

---

## 10. Negative results, refuted guesses, and errors of my own

1. **The coordinator's sandwich with small blocks does not decide the question** (§6.2): brackets a factor 2–10 wide.
2. **"Site-wise labels are optimal for chains"**: refuted at `p = 0.1` (§7.1).  **"The centre is Markov / the hardest instance
is additive or the zero residual"**: refuted (§7.2).  **"Class-wise quantiles are admissible for pair types"**: refuted (§8.3).
3. **My first guess for strong coupling** ("the cost exponents tend to 0 like `p`", written down before any computation) was wrong in rate and is not supported by
any bound of mine at `p ≥ 0.001` (§6.5).
4. **A threshold claim made too early.**  The first version of the tilt-state recursion (controls on a grid of `θ_±`,
`ydp2.py`) returned `E_F` also for `p = 0.1`, and bounds `h ≲ 0.0430` at `p = 0.3`.  A grid study (`y12`) showed the "safe end" *growing*
with the control resolution (`0.04288 → 0.0446 → 0.0451`): discretising the adversary's controls errs on the unsafe side.  The
conservative scheme (`ydp3.py`) replaced it; it gives `h ≤ 0.0450` at `p = 0.3` and shows that at `p = 0.1` the relaxed value is
`≥ 0.4239 > E_F`.  The numbers of `out/y11_dp2_p0.3.txt` are superseded and must not be used.
5. A damped value iteration destroyed the monotone bracket (`min(TW/W)` is nondecreasing only for the plain iteration); reverted.
6. First finite-`n` version of the recursion interpolated across the boundary of the feasible tilt interval; fixed by
level-dependent grids before any number was used.
7. `y02`, first version: `h` "certified" by a grid rule with coarse intervals next to a fine window — `3 %` too large
(`0.030108` for the cube); tolerances `10⁻¹²` with `4·10⁵` iterations made it exceed ten minutes twice; an SLSQP active-set solver
was slower than the multiplicative solvers (kept as an independent check: agreement `10⁻⁹` on 10 cases).
8. One run (`y05`, `n = 5`) was started with `ulimit -v 6000000` instead of `4000000`; killed after seconds and restarted.
9. Two rows of the (L′) table of §6.2 (`p = 0.2, 0.1`, `L = 1, 2`) were first written from memory and were wrong; found by checking
every table entry of this report against the output files, corrected.
10. Three scripts ran into the ten-minute limit (`y02` twice, `y10` part 2 at `p = 0.1`, `y11`); their partial outputs are kept
only where stated.

---

## 11. What I did not check

* **No referee.**  All proofs are by one author in one session.  Theorems 11.95, 11.98(d), 11.101(b), on which the *upper* bounds
for algorithms and the non-adaptive exponent rest, are unrefereed and were not re-derived here; nothing of any algorithm
was simulated.
* Floating-point rounding is not controlled anywhere; "safe" refers to the discretisation only.  The conservative recursion
was validated by three controls (§5.2), not by a second implementation.
* The upper bounds use symmetric first-order Markov references; the true centre is not Markov, so they are not tight
(gap `6–50 %` in `h`).  The lower bounds for `p = 0.1` ignore non-additive labels.
* `E_∞ = E_F`: certified margins `≤ 2·10⁻⁴` for `p = 0.4, 0.3, 0.2` only; no analytic proof; open at `p = 0.1`.
* `inf_L a⁺_L/L = a_∞` (interchange of `t → 1` and `L → ∞`).
* Alphabets with more than two letters and chains with a field: only the reductions (brute force, ternary and random
fields); no exponents computed.  Inhomogeneous chains: reductions only.  Steps 5, 6: sketches and one negative result.
* Slopes other than `u = 1`: lower bounds and the `L = 1` Markov recursion only (§6.5).
* The identification "Newman's inequality" in Proposition J is from memory.  **No prior-art search was made.**

---

## 12. Scripts: commands, sizes, run times

All in `<session scratch directory>/ws/Y/code/`, outputs in `…/out/`; `ulimit -v 4000000`; one process at a time; fixed seeds.
Libraries: `ylib.py` (solvers, vertices), `ylyap.py` (moment Lyapunov exponents, `G_∞`, `E_F`), `ydp2.py` (tilt-state recursion,
`θ`-grid; used only for the finite-chain test of `y10`), `ydp3.py` (conservative tilt-state recursion).

| script (arguments) | what | sizes | time | output |
|---|---|---|---|---|
| `y00_controls.py` | Step 0 | `≤ 38` vertices | 108 s | `y00_controls.txt` |
| `y01_reductions.py` | Step 1 brute force | 36 chains, `≤ 1024` configurations | 6.5 s | `y01_reductions.txt` |
| `y02_blocks.py 0.5 0.4 0.3` / `0.2 0.1` | (U), DP, (L′), (L), `L ≤ 3` | `≤ 120` vertices × 8 letters | 353 s / 209 s | `y02_blocks_a.txt`, `_b.txt` |
| `y03_lyapunov.py` | Prop. H: validation and scan | operator `N ≤ 96`; `2¹⁴` bond patterns | 26 s | `y03_lyapunov.txt` |
| `y04_exact_small_n.py 4` | exact `F*_n`, `E_n`, `a_n`, `n ≤ 4` | 990 vertices | 339 s | `y04_exact_n4.txt` |
| `y05_structure.py` / `… 5` | structure; `n = 5` | 990 / 395 094 vertices | 43 s / 88 s | `y05_structure_n4.txt`, `_n5.txt` |
| `y06_sitewise_long.py 0.3 0.431` | site-wise optimum, `n ≤ 12` | 4096 × 4096 | 404 s | `y06_sitewise_p0.3.txt` |
| `y07_block_labels.py 0.3` / `0.4 0.2 0.1` | Prop. I | `≤ 184` labels × `2¹⁴`; 2 labels × `2¹⁸` | 134 s / 359 s | `y07_block_labels_*.txt` |
| `y08_validate.py` | DP inequality; `F^±`; quantiles; operator | `n ≤ 9` | 12 s | `y08_validate.txt` |
| `y09_slopes_and_strong_coupling.py` | §6.5 | — | 77 s | `y09_slopes_strong.txt` |
| `y10_dp2.py 1` | tilt-state recursion (finite chains, `θ`-grid) against exact maxima, `n = 3, 4` | 990 vertices | 4 s | `y10_dp2_part1.txt` (`y10_dp2_parts12.txt`: first run, with a `θ`-grid threshold part that is superseded by `y13`) |
| `y11_dp2_bounds.py 0.3 101 11` | **superseded** (`θ`-grid, unsafe) | | 87 s | `y11_dp2_p0.3.txt` |
| `y12_dp2_grid.py 0.3 0.40 0.2413` | grid study that exposed item 4 of §10 | `G ≤ 801`, `C ≤ 81` | 580 s | `y12_dp2_grid_p0.3.txt` |
| `y13_certified_upper.py p` (`0.4, 0.3, 0.2`; `0.1 801 40`) | Prop. G, safe: `E`, `h`, `a` | `G = 801` (`E`: 3201) | 103, 135, 191, 424 s | `y13_upper_p*.txt` |
| `y14_threshold_test.py` | LP ascent of `KL(π‖π_φ)` | `n ≤ 12` (4096 variables, 49 152 constraints) | 43 s | `y14_threshold_test.txt` |
| `y15_dp3_controls.py` | controls of the safe recursion | `G ≤ 3201` | 256 s | `y15_dp3_controls.txt` |
| `y16_recheck_lower.py` | independent re-evaluation of the headline lower bounds | 184 labels | 16 s | `y16_recheck_lower.txt` |

`out/y02_rows_*.pkl` hold the rows of the tables of §§6.1–6.3.  `Y_notes.md` is the running log (including the wrong turns).
