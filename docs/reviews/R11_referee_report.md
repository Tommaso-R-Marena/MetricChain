# Referee report R11 — Workstream Y (`docs/workstreams/Y_REPORT.md`)

**Known parts with interactions along the chain (Markov chains): reductions to block landscapes, a regularised formula, and what a nearest-neighbour interaction does to the exponents.**

Referee R11, 26 November 2026.  Object: `docs/workstreams/Y_REPORT.md` (612 lines; all line numbers below refer to it), its brief, its outputs in `experiments/workstreams/Y/out/`.  Background used: `docs/THEORY_REPORT.md`, Theorems 11.22, 11.24–11.28, §11.19 (Theorem 11.54), §11.20 (Theorem 11.59), §11.23, §11.25 (Corollary 11.91), §11.26 (Theorems 11.95–11.103) — cited by name, because the file was being edited while I worked and its line numbers moved.

How to read the three modes used below: **[H]** re-derived by hand, line by line; **[N]** replicated numerically with my own code, written from the statements (no code of the workstream or of the repository imported or copied; I opened `y07_block_labels.py` and three output files of the workstream only *after* my own runs, to locate two discrepancies — findings m1, m2); **[R]** read only.

---

## 0. Verdict in one paragraph

**No critical finding.**  Every statement labelled *[proved]* that I re-derived is proved (Theorems Y1–Y3, Lemmas A–C, Proposition D, Theorem E(a), Propositions F, G, H, I, J(a)); small hypotheses are unstated in two places (m6, m7).  Every number I recomputed agrees with the report to the digits printed, with these exceptions: the four headline lower ends are reproduced only when an unstated stopping rule is imitated, and the `p = 0.1` upper ends come from a scan that ended at its edge — all are valid bounds and can be improved (m1, m2); one sentence of §7 and one list of counts in §6.4 are off (m11, m12).  **The headline's direction is correct and does not depend on any unrefereed input or on the report's Lyapunov numerics:** I obtained it a second time by a route that uses only the exact embedding (L′), Lemma A and the enumeration of one block of at most 16 sites (§4.4 below): for every `n = k(L+m) − m` the cost of every correct algorithm at an explicit instance of the class is at least `(1−2δ)·exp(n·r − tε)` with `r ≥ 0.0317, 0.0358, 0.0386, 0.0347` for `p = 0.4, 0.3, 0.2, 0.1`, against the uniform cube's exact exponent `0.029139`.  **Two major findings concern what the brackets are brackets *of*, and the wording of the contrast with §11.25** (M1, M2); neither changes a number.

---

## 1. Verdict table

| statement (lines) | verdict | basis |
|---|---|---|
| **Theorem Y1 (U)** (124–143) | **proved as stated** | [H]; [N] 36 random chains (27 binary with 8–10 sites, 9 ternary with 6), 432 residuals: identity to `2.7·10⁻¹⁵`, `ψ+g ∈ 𝒞_{d⁺}` (largest violation `1.4·10⁻¹⁴`), `d⁺` attained |
| **Theorem Y2 (L)** (150–161) | **proved as stated** | [H]; [N] marginal identity `8.9·10⁻¹⁶`, two-sided bound never violated (432 residuals) |
| **Theorem Y3 (L′)** (163–175) | **proved as stated** (the remark on negative entries is a sufficient condition: m8) | [H]; [N] 216 residuals: membership `3.8·10⁻¹⁵`, identity `1.3·10⁻¹⁵`; end-to-end on the binary symmetric chain, `n = 16` |
| **Lemma A** (199–208) | **proved** (uses 11.27(a) *and* (b); the sentence on "the threshold of the `n`-chain" needs three more lines: m6) | [H] incl. the identity `Σ_φ Mπ_φ^t/π_{γ*}^t ≡ e^{−G_t(M)}`; [N] end-to-end at `n = 16`: `γ*` and all 256 alternatives are members (all edges), smallest gain in `ln A` `0.8076 > ε = 0.5`, coverage identity to `10⁻⁹` |
| **Lemma B** (210–216) | **proved** (strong duality for each factor is Sion's theorem; I checked it) | [H]; [N] with *all* vertices of a product space: 4 cases, `≤ 8·10⁻⁹` |
| **Lemma C** (218–221) | **proved** | [H] |
| **Proposition D** (225–252) | **proved for a stationary chain**; unstated: stationarity, and `F⁻_1 = −∞` when `u < 2κ₀` (Fekete from `L ≥ 2`): m7 | [H] all four parts incl. the gap version; [N] all vertices, `L ≤ 3` (`n ≤ 4` for the plain function): the numbers of lines 247 and 249–250 reproduced |
| **Theorem E(a)** (258–260) | **proved**, and with the constant `C = 2(u+K)` for *every* `p` (m5) | [H] |
| **Theorem E(b), (c)** (261–269) | **proved given** Theorems 11.95, 11.98(d), 11.101(b) for super-sites; **only for extensive accuracies and in the iterated limit** — see **M1** | [H] for the reductions and the arithmetic of the limits; the three theorems themselves [R] |
| Theorem E(d), (e) (270–279) | correct as statements of scope; inhomogeneous chains are a sketch, as labelled | [R] |
| **Proposition F** (287–305) | **proved** | [H]; [N] 150 random inhomogeneous chains with asymmetric envelopes (smallest ratio `1.076 ≥ 1`), Lipschitz claim for `−ln V_i` (`1·10⁻¹⁵`); all 28 DP entries of §6.3 reproduced |
| **Proposition G** (311–338) | **proved** (the relaxation); the report's discretisation not audited, but an independent safe scheme of mine gives bounds that are `≤` the report's (one exception at a coarser grid, §4.5) | [H] with an own closed form of (★); [N] (★), `|λ_i| ≤ u*` and the chain rule on 60 random members; safe recursion `≥` exact maximum over all vertices (`n = 3`: 27 cases; rewards `n = 3, 4`: 8 cases) |
| **Proposition H** (345–358) | **proved** | [H]; [N] 63 cases `n = 6, 8, 10`: `4.4·10⁻¹⁵`; limit values and optimisers identical to the report |
| **Proposition I** (360–369) | **proved** | [H]; [N] 5 cases with random non-symmetric `M_L`: `1.0·10⁻¹⁵`; headline values: see §4.3 and m1 |
| **Proposition J(a)** (373–376) | **proved**; "every `n`" belongs to `E_n ≥ ln Z_n(h)/Z_n(0)` (m9) | [H]; [N] |
| Proposition J(b)–(d), conjecture (377–386) | numerical, as labelled; (c) **confirmed and sharpened** (m4) | [N] `E_n = ln Z_n(h)/Z_n(0)` over all vertices for `n ≤ 4`, to the 7–9 digits printed (`p = 0.4, 0.3, 0.1`); ascent search by successive linear programmes, `n = 8, 10`: nothing above the uniform field |
| **Headline, direction** (35–47; §6.5) | **established**: lower bounds for every algorithm (proved, replicated, and re-obtained independently) against the cube's exact exponent | §4.3, §4.4 |
| **Headline, brackets** (38–44) | lower ends: valid and replicated; upper ends: valid upper bounds for `h_∞ = sup_t F_∞(t)`, replicated with an own safe scheme; **as bounds on a cost exponent they are conditional and not at bounded accuracy (M1)**; at `p = 0.1` improvable (m2) | §4.3, §4.5 |
| §7 structure (480–498) | numerical; `n ≤ 4` reproduced exactly (990 vertices); one sentence wrong for `p = 0.4` (m11); `n = 5` not checked | [N] |
| §8 fixed sample (502–518) | items 1, 2: [R]; item 3: example verified by hand, but it shows less than the text says (m13); brute force reproduced | [H], [N] |
| §9 beyond chains (522–538) | sketch, as labelled | [R] |

---

## 2. Findings

### CRITICAL

None.

### MAJOR

**M1.  What the bracket for `h` is a bracket of; "at bounded accuracy" holds for the lower ends only.**
*Where:* summary table and "What the brackets are", lines 38–52; Theorem E(b), lines 261–264; the coordinator's wording of the headline ("the hinted exponent per site at bounded accuracy lies in the brackets …").
*What is proved.*  (i) Lower ends: for every `n`, every `ε ≥ 0`, every `(ε/2, δ)`-correct algorithm (any hint, adaptive or not) makes at least `(1−2δ)·exp(G_t^{(n)}(M) − tε)` evaluations at the member `γ*(M)` of the class, and `G_t^{(n)}(M) = n·(lower end) − O(1)`.  This is a statement about cost at *every* accuracy `ε = o(n)`, bounded accuracy included, and it is unconditional.  (ii) Upper ends: upper bounds for the number `h_∞ := sup_t F_∞(t)` (Propositions F, G; weak duality).  That `h_∞` bounds a *cost* exponent from above is Theorem E(b), which (α) rests on Theorem 11.101(b) applied to super-sites with `q^L` letters, (β) is stated — like 11.101(b) — for extensive accuracies `ε = ε₁n`, `0 < ε₁ < E_∞`, where the exponent is `R̂_∞(ε₁) ≤ h_∞`, and (γ) is an iterated limit, `n → ∞` at fixed `L`, then `L → ∞`.  The report says (α) and (γ) (lines 27, 270–272), and Theorem E(b) carries the range of `ε₁`; but nowhere does it say that the `h` of its summary is therefore only the limit `ε₁ ↓ 0` of extensive exponents on the upper side, and its table header "`h` (hinted at the hardest instance = adaptive)" names no regime.  For the uniform cube the value `0.029139` is *both* the limit `ε₁ ↓ 0` of the extensive exponents (Theorem 11.54) and the exponent at every bounded accuracy (Theorem 11.25(c),(d) with a hint at the zero residual; Theorem 11.58 for adaptive algorithms without a hint); for the chain **no upper bound on the cost of any algorithm at bounded accuracy is proved** — that would need the analogue of Theorem 11.58 (or of the isoperimetric step of Theorem 11.25(c)) for block landscapes.
*Consequence.*  The comparison that carries the headline — chain lower bound against cube exact value — is like with like in both regimes and is unaffected.  The sentence "the hinted exponent at bounded accuracy lies in `[0.034026, 0.036163]`" is not proved in its upper half.
*Corrected wording* (for lines 48–52 and for any citation):
> "Lower ends of `h`: for every `n` and every accuracy `ε ≥ 0`, every correct algorithm, with any hint, makes at least `(1−2δ)exp(n·h_low − tε − 2t(u+K))` evaluations at an explicit member of the class (Theorem 11.27(a),(b) [V] and algebra); so the hinted exponent at the hardest instance is at least `h_low`, at bounded and at vanishing extensive accuracy.  Upper ends of `h`: upper bounds for the game-function quantity `h_∞ = sup_t F_∞(t)`.  That the cost exponent of adaptive algorithms without a hint (hence of hinted ones at every instance) is at most `R̂_∞(ε₁) ≤ h_∞` is proved only for extensive accuracies `0 < ε₁ < E_∞`, given Theorem 11.101(b) for super-sites, and in the iterated limit `n → ∞`, then `L → ∞`; at bounded accuracy no upper bound is proved."

**M2.  The contrast with §11.25 is stated more broadly than §11.25 proves.**
*Where:* lines 35–36 ("For interactions that are functions of the type it does not: Corollary 11.91(ii)"); the same contrast in the brief (line 112–113) and in the coordinator's headline ("unlike a known part that is a function of the type").
*What is wrong.*  Corollary 11.91 covers two of the three exponents — the hinted exponent of *symmetric* instances (those that are functions of the type) and the exponent of non-adaptive algorithms — at extensive accuracies, and its item (ii) (equality with the cube) needs a symmetric convex rate function.  The exponent of adaptive algorithms without a hint is *not* covered for general function-of-type known parts (Conjecture 11.94; the theory report corrected exactly this over-statement after SCI-REV-0001, M1: "changes no exponent").  The report repeats the uncorrected form.
*Corrected wording:*
> "For a known part that is a function of the type, without a field and with one phase, the hinted exponent of the hardest symmetric instance and the exponent of fixed samples equal the uniform cube's (Corollary 11.91(ii), given Theorems 11.78, 11.79); the lower bound that Lemma A gives for such a known part is attained at a symmetric instance (the problem is `S_n`-invariant and `Q ↦ max_φ(1−t)D_t(π_φ‖Q)` is convex, so the optimal centre is exchangeable) and is therefore, in the exponent, never above the cube's.  For a nearest-neighbour chain without a field the same lower bound is strictly above the cube's exponent, and so is the threshold."
*Why there is no contradiction* — see §5; with the same code the two cases separate cleanly (`r11_11`).

### MINOR

**m1.  The block label law `M_L` behind the four headline lower ends is not specified, not optimal, and not reproducible from the text** (Proposition I, lines 360–369; table, lines 439–444; `y16` output).  Any `M_L` gives a valid bound, so the four numbers stand.  But `M_L` is an Arimoto iterate for `G_L` stopped by an iteration cap (`y07_block_labels.py`: `itmax = min(40000, 300 + 3·10⁸/size)`, i.e. 399 iterations at `L = 14`).  Its `G_L` (`0.408732, 0.564819, 0.638252, 0.669310` in `y16_recheck_lower.txt`) is below the maximum over the same labels (`0.408903, 0.565252, 0.638522, 0.669413`, my duality brackets `< 4·10⁻⁹`), and the bound it gives is neither that of the `G_L`-optimum (`0.034040, 0.040143, 0.044618, 0.044346`) nor the best over `M_L` (`0.034040, 0.040143, 0.044622, 0.044513`, exponentiated-gradient ascent of the bound itself, re-evaluated from scratch).  At `p = 0.1` the converged `G_L`-optimum gives *less* (`0.044346`) than the report's unconverged iterate (`0.044378`): the fifth decimal of the headline depends on a stopping rule.  Confirmation (`r11_04d_iteration_cap.py`): plain Arimoto from the uniform law, stopped at that cap (399 iterations at `L = 14`, 846 at `L = 12`), gives `G_L = 0.408732, 0.564821, 0.638253, 0.669311`, the bounds **`0.034026, 0.040116, 0.044599, 0.044378`** and the support sizes `110, 132, 78, 40` of `y16` — the report's four headline numbers to one unit of the last digit.  *Fix:* say "`M_L` any symmetric law; we use …", and either print the optimised values or store `M_L`.

**m2.  At `p = 0.1` the reference chain of the tilt-state bounds was not optimised; "optimal `q̃ < p`" is not true for `p ≤ 0.2`** (lines 423–432; `y13_upper_p0.1.txt`).  The workstream's scan ends at `q̃ ≈ 0.11–0.12` with the bound still decreasing (`a`: "scan: 0.24926 … 0.19722 0.19277"; `h`: `qt = 0.115` at every `t`).  With my safe scheme: at `p = 0.1` the best symmetric Markov reference has `q̃ ≈ 0.15 > p` and gives `h_∞ ≤ 0.062993` (certified over all `t`, `G = 401`; `0.062740` with `G = 601`) against the report's `0.066765`, and `a_∞ ≤ 0.172914` against `0.192774`.  At `p = 0.2` the optimum is at `q̃ = p` exactly (a kink: `0.054127, 0.053955, 0.055022` at `q̃ = 0.195, 0.200, 0.205`, `t = 0.419`, `G = 801`), where the bound tends to the closed form of m3.  The printed brackets are valid; line 430–431 should read "optimal `q̃ < p` for `p = 0.4, 0.3`; `q̃ = p` for `p = 0.2`; `q̃ ≈ 0.15 > p` for `p = 0.1`", and the `p = 0.1` row can be replaced by `h ∈ [0.0444, 0.0628]`, `a ∈ [0.1166, 0.1730]` (ratios to the cube `×[1.52, 2.16]`, `×[1.05, 1.56]`).

**m3.  An unlabelled claim** (lines 434–435): "With `Q = π` the worst label is the uniform field and the bound is the closed form `tE_F(u) − E_F(tu)`."  No proof; status is [numerical], and only for `p ≥ 0.2`: my safe values at `q̃ = p` decrease to the closed form like the grid spacing (`p = 0.2`, `t = 0.419`: `0.054880, 0.054217, 0.053955, 0.053903` for `G = 201…1601`, closed form `0.053851`; similarly `p = 0.3, 0.4`).  At `p = 0.1` the relaxed value at `Q = π` is `0.0711` against the closed form `0.0436`: there the relaxation does not support the claim.

**m4.  Proposition J(c) can be stated without margins** (lines 380–382, 577).  With grid cells that end exactly at `±u*` (the uniform field has the constant tilt `±u*`, the corner of the state space), my safe recursion returns `E_∞ ≤ E_F + 7·10⁻¹¹` for `p = 0.4, 0.3, 0.2, 0.15` at `G = 201, 401, 801` alike (and for `p = 0.14` at `G = 401`); the report's excess (`1–2·10⁻⁴`, halving with the spacing) is, as far as I can tell from lines 329–336 (I did not read `ydp3.py`), an artefact of cells centred on grid points and of the enlargement by `1.5D`, both of which reach beyond `±u*`.  So **`E_∞ = E_F` for `p ≥ 0.14` at `u = 1`** [numerical evaluation of the proved bound; floating point not controlled].  For `p ≤ 0.13` the relaxed value exceeds `E_F` (`0.3771` against `0.3734` at `p = 0.13`; `0.4282` against `0.4017` at `p = 0.1`, `G = 801`, consistent with the report's `[0.42389, 0.42631]`).

**m5.  Theorem E(a): the constant** (lines 237–238, 258–260).  `F*_n(t) ≥ nF_∞(t) − 2t(u+K)` holds for every `p`, with no gap and no enlargement "by `m·max F⁺_1`": `F⁺_n ≤ F*_n + tΔ` (the function `φ⁻` of the proof of D(c) ignores the two end letters and is a member of the *plain* class `𝒞_d`; Lemma C(iv)), and `nF_∞ ≤ F⁺_n` (sub-additivity).  The enlargement is needed only for the other direction.

**m6.  "The threshold of the `n`-chain is exactly `E_n`"** (lines 206–208).  Theorem 11.28(d), remark (i), gives the width `ε*_n = min_Q[max F_Q − min F_Q]`, and in general only `ε*_n ≤ min_Q max_φ KL(Q‖π_φ)`.  Equality holds because the minimiser of `max_φ KL(Q‖π_φ)` is the normalised geometric mean `∝ Π_φ π_φ^{M*(φ)}`, the Gibbs law of the member `Σ_φ M*(φ)φ` of the class (minimax in `(M, Q)`), for which `min_ψ F_Q(ψ) = −KL(Q‖π)`.  Add these lines.  Also: at fixed `n` nothing is sharp; the sharp statement is for `E_∞ = lim E_n/n` (bounded cost above, exponent `R̂_∞(ε₁) > 0` below), and that one is correct and unconditional.

**m7.  Proposition D, hypotheses** (lines 225–238).  "A segment of `L` consecutive sites of a homogeneous chain" presupposes a *stationary* chain (otherwise `π_L` depends on the position); and for `2κ₀ > u` (at `u = 1`: `p = 0.3, 0.2, 0.1`) `F⁻_1` is the value of an empty class — read `−∞` and apply Fekete's lemma from `L ≥ 2`.  The parenthesis at lines 237–238 covers `u ≤ K` only.

**m8.  Theorem Y3, parenthesis** (lines 170–171).  "It must have no negative entries" is what §11.26 needs of an envelope; the embedding itself needs only a non-empty class (no negative cycles of `d⁻`).

**m9.  "`E ≥ E_F` (proved, every `n`)"** (lines 57, 373–374).  The every-`n` statement is `E_n ≥ ln Z_n(h)/Z_n(0) = nE_F − c₀(p,u)` with `c₀ > 0`: per site `0.161, 0.182, 0.194, 0.213, 0.217` for `n = 2, 3, 4, 8, 10` at `p = 0.3`, against `E_F = 0.2324`.  Write "`E_n ≥ ln Z_n(h)/Z_n(0)` for every `n`, hence `E_∞ ≥ E_F`".

**m10.  "Domains of about `2K/u` sites"** (lines 53–54, 453).  The best fixed domain lengths are `3, 4, 4–5, 5` for `p = 0.4, 0.3, 0.2, 0.1` (reproduced), while `2K/u = 0.8, 1.7, 2.8, 4.4`: not a fit for `p ≥ 0.3`.  Say "3 to 5 sites at `u = 1`".

**m11.  §7, item 2** (lines 489–491): "For short chains (`n = 4`, `t = 0.45`) the optimal labels are the two uniform fields" is true for `p = 0.3, 0.1`; at `p = 0.4` the optimum has four labels — the uniform fields (weight `0.4165` each) and the two labels with a wall at the middle bond (`0.0835` each) — with `F*_4 = 0.134142` against `0.133237` for the uniform fields alone.  The quoted `I(x₁;x₃|x₂) = 2.9·10⁻³` at `p = 0.4` is that of the four-label optimum (reproduced: `2.90, 5.73, 1.15·10⁻³`).

**m12.  Support sizes** (line 451): for the converged optimum the labels with weight above `10⁻⁶` number `4, 8, 18` at `n = 6, 8, 10`, not `8, 12, 18`.

**m13.  §8, item 3** (lines 512–517).  The example shows that the class-wise quantile *levels* are not Lipschitz across Markov-type classes (the hypothesis of `lowDens_shift`); in it `ψ^{tr,q}` coincides with `ψ` at `x` and `y`, so it does not show that `ψ^{tr,q}` leaves the class (line 511: "need not be in the class").  That is nevertheless true: in my brute force (`n = 8`, 58 Markov-type classes, 100 residuals × 3 quantiles) the levels fail in 299 of 300 cases and `ψ^{tr,q}` itself is inadmissible in 188, with an excess of up to 4 flips (0 and 0 for type classes).  Add one such case, or the count.

**m14.  "All three exponents are multiplied by `(1−p)/p`" at small slopes** (lines 60–61, 471–472).  Shown for `h` (bracket `[2.271, 2.331]` at `u = 0.05`, reproduced) and for `E` (`E_F`/cube `2.332`, DP upper bound `2.333`); for `a` the report has only the upper bound (`y09`: `0.000728/0.000312 = 2.33`), no lower bound at small slopes.

**m15.  Status lines** (lines 27, 90–91, 570–572).  Lemma A uses Theorem 11.27(a) as well as (b).  Theorems 11.99 and 11.101 are, in the theory report, reviewed (SCI-REV-0005: 11.99 proved, 11.101(b) proved after two gaps were closed); "unrefereed" is out of date for them (it stands for 11.95, 11.98(d) as far as I can see).

**m16.  A summary sentence that is not the report's** (`docs/workstreams/README.md`, row Y; the coordinator's headline): "the hardest instances are constant over domains".  Constant over domains are the *labels* — the centres `σ` of the cones `u·d(·, σ) = φ_σ + const` that serve as alternatives.  The hardest instance `γ*` is their soft minimum; in the Markov-label family it is a function of the bond pattern `(s_is_{i+1})_i` alone (my check at `n = 8`: spread `6·10⁻¹⁵` within bond patterns, oscillation `1.34`), with multi-body terms; it is neither additive nor constant over domains (the report says this correctly at lines 493–494).  Likewise "the threshold nearly doubles" is the value at `p = 0.3` (`×1.935`, as line 46–47 says); the ratios are `1.408`, `1.935`, `2.587`, `[3.344, 3.480]` for `p = 0.4, 0.3, 0.2, 0.1`.

**m17.  The lower ends of `a` as exponents of algorithms** (lines 47–52).  "All twelve lower ends lie above the cube" is true of the numbers.  For `h` and `E` they are unconditional cost statements.  For `a` they are lower bounds for `a_∞ = sup_τF_∞(τ)/(1−τ)` (replicated: `0.116817, 0.126444, 0.129797, 0.116632`); that the cost of *non-adaptive* algorithms has an exponent at least `θ_∞(ε₁) → a_∞` uses Theorem Y3 together with the every-`n` lower bound of Theorem 11.98(d) for block landscapes (a paper proof in the theory report) and the limit `L → ∞` (Theorem E(c)).  Line 49 lists only `h` and `E` as unconditional, correctly; say explicitly that the `a`-column is conditional on both sides.

**m18.  Floating point.**  As the report says (line 573), nothing is interval arithmetic; the same holds for my replication.  The margins of the headline (lower ends 17–53 % above the cube) are five orders of magnitude above any rounding.

---

## 3. Re-derivations [H]

Notation as in the report.  `π_φ ∝ πe^{−φ}`, `φ̃ = φ + ln E_πe^{−φ}`.

1. **Weak and strong duality; vertices.**  `Σ_φ M(φ)Σ_xπ_φ^tQ^{1−t} = Σ_x m^tQ^{1−t} ≤ (Σ_x m)^t` with `m = (Σ_φMπ_φ^t)^{1/t}` (Hölder): `G_t(M) ≤ max_φ(1−t)D_t(π_φ‖Q)`.  Equality of `max_M` and `min_Q` by Sion (linear in `M`, concave in `Q`).  The maximum over the polytope is at a vertex: on a face the tangent directions are the functions constant on the components of the tight graph; a critical point of `t ln Σ_cA_ce^{−η_c} − ln Σ_cB_ce^{−tη_c}` has equal component laws and second derivative `t(1−t)Var(η) > 0`, so no interior local maximum.  Monotonicity of `F*/t` and `F*/(1−t)`: `(1−t)D_t(P‖Q) = tD_{1−t}(Q‖P)` and Rényi divergences increase with the order.
2. **Theorems Y1–Y3.**  As in the report; for Y1 I also checked that every entry of `δ^±` is attained by a cone (the two neighbours across the two cuts of a one-site block can be chosen independently).  Binary symmetric chain: `δ^± = K`, `ρ_m = 1 ± λ^{m+1}`, `κ_m`, and the admissible gaps of line 174 — all confirmed.
3. **Lemma A.**  `γ* ∈ 𝒞_d` (soft minimum); `Φ_φ := φ̃ − γ̃*` satisfies `γ* + Φ_φ ∈ 𝒞_d` (this *is* "Lipschitz for the slack of `γ*`") and `E_{π_{γ*}}e^{−Φ_φ} = E_πe^{−φ̃} = 1`, so `Λ(Φ_φ) = 0` and every `r > ε` is sensitive (11.27(a)); `Σ_φM e^{−tΦ_φ(a)} = Σ_φMπ_φ(a)^t/π_{γ*}(a)^t = (Σ_xm)^t = e^{−G_t(M)}` for *every* `a`; 11.27(b) and `r ↓ ε`.  The alternatives `min(γ*, φ̃ − r − const)` are minima of two members, differ from `γ*` on `{Φ_φ < r}` only, and raise `ln A` by `ln E_{π_{γ*}}e^{(r−Φ_φ)₊} ≥ r`.
4. **Lemma B, C.**  As in the report; in B the step `−ln W ∈ 𝒞_{d₁}` and `E_{π₁}W = Z_φ` uses the product law, as marked.
5. **Proposition D.**  (a) the Gibbs family of the long slack block is a sub-family of that of the product of the two slack blocks; (b) the long reduced class contains `φ₁ + φ₂ + ln ρ₀(cut)` — checked site by site, including one-site blocks — with product Gibbs laws; with a gap the Gibbs law on the full segment is (block marginal) × (unchanged conditional law of the gap), so the power-mean sum is the same; (c) with `φ⁻` = minimum over the two end letters; (d) Fekete twice; `F⁻_L/L ≤ F_∞` follows from (c) and needs no direct comparison of `F⁻_L` with `F⁺_L`.  The side remark of line 248 (`|F*_{n₁+n₂} − F*_{n₁} − F*_{n₂}| ≤ tK`) is Lemma C(iii) with `osc ln ρ₀ = K` plus Lemma B — a second, shorter proof that the limit exists.
6. **Theorem E.**  (a) from Lemma A and D; (b), (c): the reductions and the per-site normalisations (`ε₁L` per super-site in (U); `ε₁(L+m)` in (L′)) are right; the maximiser bound `τ ≤ a/(a+ε₁)` and the rates are right; "above `E_∞` a bounded number of evaluations suffices" follows from the sandwich of 11.28(d)(i) with `D = nu` and `Δ = n(ε₁ − E_n/n)` and is unconditional.
7. **Proposition F.**  Steps (1)–(3) as written; for binary letters the extremal `w` in `G_i` and the extremal `γ` in `c_i` are at the ends of their segments (tested).  Sub-additivity of `F^{DP}_L` (asserted) follows from the same recursion inside the block.
8. **Proposition G.**  With `a(μ) = ln((1−p)e^μ + p)`, `c(μ) = ln(pe^μ + 1−p)`: `θ₋ = λ − a(μ₊) + c(μ₋)`, `θ₊ = θ₋ + μ₊ − μ₋`, equivalent to (★).  The relaxation keeps `|θ_±| ≤ u` and `|tilts| ≤ u*`; `F_∞(t) ≤ −ln min(TW/W)` for every positive bounded `W` (no continuity needed — I use piecewise constant `W`).
9. **Proposition H, I.**  Gauge `τ_i = σ_is_i` in both partition functions; the tilt `Z(σ)^t` (resp. `c_φ^t`) cancels the normalisation; `E_{⊗Q}[Πρ₀] = 1` exactly for flip-symmetric `M_L` (`B_Qρ₀` is stochastic).  `G_∞(t;0) ≤` cube by Jensen, as stated.
10. **Proposition J(a)** and the "iff" of line 376: as stated.

---

## 4. Replication [N]

All scripts in `code/` (own library `r11lib.py`: enumeration, Rényi/Arimoto solvers with duality brackets and an SLSQP polish, moment-Lyapunov operator by Chebyshev collocation on the invariant interval, vertex enumeration by spanning trees and by height functions).  Outputs in `out/`.  The machine was shared; times are wall-clock under load.

### 4.1 Controls and the cube value (`r11_00_controls.py`)

`0.029139` is, three ways: `max_t[t ln cosh(u/2) − ln cosh(tu/2)] = 0.0291391` at `t* = 0.4900`; `ln 2 − h(Λ₁/u) = 0.0291391` (Theorem 11.25(d), third row, `Λ₁ = ln(2/(1+e^{−u}))`); my Rényi solver for one site `[0.0291391, 0.0291391]`.  **Which quantity:** the exponent of the least expected number of evaluations *at the zero residual* among algorithms that are correct on the whole class and may be tailored to that instance (hinted), for accuracies `ε_n = o(n)`, `ln(1/ε_n) = o(n)` — bounded accuracy included (Theorem 11.25(a),(c),(d)); it equals `h = R^max(0) = R_0(0) = max_tF(0,t)` of Theorem 11.59 at `p = ½` (the closed form 11.59(b) reduces to `t ln cosh(u/2) − ln cosh(tu/2)`), and by Theorems 11.54 and 11.58 it is also the worst-case exponent over the class of adaptive algorithms without a hint (as `ε₁ ↓ 0`, and at every bounded accuracy), so no instance of the cube is harder than the zero residual.  `a = 0.1109441`, `E = 0.1201145`; field control `(0.7, 0.3)`: `0.0250335, 0.0953005, 0.1031310` — all as in the report.

### 4.2 Reductions, blocks, DP (`r11_01`, `r11_06`, `r11_06b`, `r11_07`)

| quantity | report | mine |
|---|---|---|
| (U), (L), (L′) identities | `≤ 3·10⁻¹⁵` | `≤ 2.7·10⁻¹⁵` (§1) |
| `κ_m`, `p = 0.3` | `0.847, 0.323, 0.128, 0.051, 0.021, 0.008` | identical |
| `F⁺_{1,2,3}`, `F⁻_{1,2,3}` at `p = 0.4`, `t = 0.45` | `0.082877 0.116072 0.148407`; `0.001103 0.025085 0.061313` | identical; sub-/super-additivity defects identical |
| plain `F*_n(0.45)/n`, `p = 0.4`, `n = 1..4` | `0.02895, 0.03280, 0.03359, 0.03354` | identical (990 vertices at `n = 4`) |
| §6.1 (U) `h ≤`, all 12 entries | e.g. `0.15031, 0.09387, 0.07428` (`p = 0.3`) | identical |
| §6.2 (L′) `h ≥` (5 entries), (L) `h ≥` (4), `a ≥` (4), `E ≥` (4) | e.g. `0.02088`, `0.01629`, `0.06978`, `0.09375` | identical |
| §6.3 DP `h ≤` (12), `E ≤` (12), `a ≤` (4), `u*` (4) | e.g. `0.05484, 0.05180, 0.04902`; `0.23419, 0.23324, 0.23285`; `0.15401`; `1.526` | identical (one last digit: `0.16916` for `0.16917`) |

### 4.3 The lower ends (`r11_03`, `r11_04`, `r11_04b`, `r11_04c`, `r11_04d`, `r11_09`)

| `p` | Prop. H (`t*`, `c*`) report / mine | i.i.d. labels report / mine | Prop. I, `≤ 2` walls: report | mine, `G_L`-optimal `M_L` | mine, bound-optimal `M_L` | mine, Arimoto stopped at the report's cap |
|---|---|---|---|---|---|---|
| `0.4` | `0.033503 (0.458, 0.774)` / identical | `0.028907` / identical | **`0.034026`** (`L=12`, `t=0.459`) | `0.034040` | `0.034040` | `0.034026` |
| `0.3` | `0.038695 (0.431, 0.859)` / identical | `0.028151` / identical | **`0.040115`** (`L=14`, `t=0.434`) | `0.040143` | `0.040143` | `0.040116` |
| `0.2` | `0.041770 (0.402, 0.861)` / identical | `0.026626` / identical | **`0.044599`** (`L=14`, `t=0.409`) | `0.044618` | `0.044622` | `0.044599` |
| `0.1` | `0.039608 (0.364, 0.833)` / identical | `0.023418` / identical | **`0.044378`** (`L=14`, `t=0.380`) | `0.044346` | `0.044513` | `0.044378` |

`Λ_blk` checked two ways (operator with `N = 64, 128`; exact increments of `ln E[c^t]` over `k = 1 → 2 → 3` blocks, agreement `10⁻⁷…10⁻⁵`).  So all four lower ends are reproduced (last column) and confirmed as valid bounds; their last digits depend on `M_L` (m1).  Further: `a ≥ 0.116817, 0.123875, 0.122445, 0.101876` (Prop. H, `t = 0.999`) and `0.116547, 0.126444, 0.129797, 0.116632` (Prop. I, `t = 0.99`) — identical; `E_F = 0.169127, 0.232400, 0.310766, 0.401719` — identical; site-wise optimum on the plain chain `0.039856, 0.040183, 0.040243` per site (`n = 6, 8, 10`, `p = 0.3`, `t = 0.431`) — identical; slope table of §6.5 (lower/cube `2.271 … 0.928`, upper/cube `2.331 … 1.159`, `E_F`/cube) — identical; `p = 0.02`: `0.027390`.
**`p → ½`** (`r11_03`, part 3a): `max_{t,c}G_∞ = 0.0308515, 0.0295439, 0.0292554, 0.0291404, 0.0291392` for `p = 0.45, 0.48, 0.49, 0.499, 0.4999` (`c* → 0`), and exactly the cube `0.0291391` with `c* = 0` at `p = ½`, where `c > 0` gives less (`0.0289785` at `c = 0.3`).  The excess is of second order in `K`.  My safe upper bounds at `p = ½` return `E = 0.120115`, `a = 0.110944` exactly and `F(0.49) ≤ 0.029343` (`G = 801`, from above, error of the order of the spacing) (`r11_08e`).

### 4.4 An independent route to the headline (`r11_05_certificate.py`) — no Lyapunov exponents, no Propositions H, I, no unrefereed input

Chain of `k` blocks of `L` sites separated by gaps of `m` sites.  For block labels `φ_j(x_B) = −Σ_i h_iσ_ix_i` with `h_i = u/2` inside and `(u − κ_m)/2` at the two ends, `ψ = Σ_jφ_j + Σ_j ln ρ_m(x_{e_j}, x_{s_{j+1}})` is a member of `𝒞_d` whose Gibbs law on the blocks is the *product* of the block Gibbs laws (Theorem Y3).  Hence `G_t^{(n)}(M_L^{⊗k}) = k·G_t^{(L)}(M_L)` **exactly**, and Lemma A gives, for every `k`, at least `(1−2δ)exp(k·G_t^{(L)}(M_L) − tε)` evaluations at an explicit instance.  The only computation is `G_t^{(L)}(M_L)` on one block (`2^L` configurations, labels with at most two walls; duality brackets `< 10⁻⁶`).  Per site, `G_t^{(L)}/(L+m)`:

| `p` | `m` (end slope) | `L = 8` | `10` | `12` | `14` | `16` | cube |
|---|---|---|---|---|---|---|---|
| `0.4` | `0` (`0.595`) | `0.029142` | `0.030179` | `0.030874` | `0.031353` | **`0.031684`** | `0.029139` |
| `0.3` | `0` (`0.153`) | `0.030872` | `0.032923` | `0.034186` | `0.035124` | **`0.035812`** | |
| `0.2` | `1` (`0.246`) | `0.032213` | `0.034813` | `0.036502` | `0.037680` | **`0.038631`** | |
| `0.1` | `3` (`0.130`) | `0.028569` | `0.030287` | `0.032929` | **`0.034700`** | — | |

All four rows increase with `L`, are above the cube from `L = 10` on (`p = 0.4, 0.3, 0.2` from `L = 8`), and stay below the report's lower ends (as they must: the reduced end slopes cost a boundary term that Proposition I avoids).  End-to-end check on the chain of `n = 16 = 2 × 8` sites at `p = 0.3` (Part B): all 256 residuals `φ_a + φ_b + ln ρ₀` are in the class (largest edge violation `4·10⁻¹⁶`), their Gibbs laws are products (`7·10⁻¹⁵`), `G^{(16)} = 2G^{(8)} = 0.493892` (cube: `16F_c = 0.459402`), `γ*` and all alternatives are members, the smallest gain in `ln A` is `0.8076 > ε = 0.5`, and `max_x Σ_φMe^{−t(Φ_φ−r)} = min_x = e^{tr−G}` to nine digits.  The same with gaps (`r11_05b_certificate_gap.py`; `n = 9, 10, 11`; `m = 1, 2, 3`): members (edge violation `≤ 7·10⁻¹⁶`), block marginals are products (`≤ 3·10⁻¹⁶`), and `G^{(n)}` computed on the *full* chain, gap letters included, equals `2G^{(L)}` to ten digits.

### 4.5 The upper ends (`r11_07`, `r11_08*`)

My safe scheme: `W` piecewise constant on `G` cells of `[−u*, u*]`; for each pair (cell of `λ`, cell of `μ₋`) the admissible interval of `μ₊` is replaced by the union over the two cells (monotonicity of `a, ā, c, c̄`), stage factors by their minima over the cell.  Tests: against the exact maximum over all 38 vertices at `n = 3` (27 cases, safe `≥` exact, excess shrinking with the spacing), the same for rewards at `n = 3, 4` (8 cases).

| `p` | report: `h ≤` (certified, `G = 801`) | mine: certified over all `t`, `G = 401` | mine: one `t`, `G = 1601` | report `a ≤` | mine `a ≤` (`G = 401`) | report `E ≤` | mine `E ≤` |
|---|---|---|---|---|---|---|---|
| `0.4` | `0.036163` | `0.036156` | `0.035801` (`t = 0.452`) | `0.121446` | `0.121324` | `0.169165` (DP) | `0.169127 = E_F` |
| `0.3` | `0.044995` | `0.044849` (`G = 801`: **`0.044607`**) | `0.044617` (`t = 0.43`, `q̃ = 0.255`; report `0.04468`) | `0.140860` | `0.140574` | `0.232538` | `0.232400 = E_F` |
| `0.2` | `0.054353` | `0.054292` | `0.053903` (`t = 0.419`, `q̃ = p`) | `0.160745` | `0.161035` | `0.310956` | `0.310766 = E_F` |
| `0.1` | `0.066765` | **`0.062993`** (`q̃ ≈ 0.152`; `G = 601`: **`0.062740`**) | `0.062844` (`t = 0.398`) | `0.192774` | **`0.172914`** (`q̃ ≈ 0.162`) | `0.417991` (DP, `L = 3`) | `0.41799` (DP); tilt-state `0.4282` |

So every upper end of the report is confirmed as a valid bound on the corresponding game-function quantity (mine are `≤` the report's except `a` at `p = 0.2`, where my coarser grid gives `0.1610` against `0.1607`); the `p = 0.1` row is improvable (m2).

### 4.6 The small-`n` packing test asked for in the task (`r11_02_packing_small_n.py`) — **not decisive, and it cannot be**

Fractional packing numbers `V` (Theorem 11.22(c): `E|Q| ≥ (1−2δ)V`) by exact enumeration and LP; every instance and every alternative checked to be a member (all edges), gains in `ln A` above `ε`.  Cube: `g = 0`, balls, `V = 2ⁿ/|B(k*)|` (reproduced by the same code path at `n = 10`).  Markov chain: soft-minimum instance, cones around centres with at most two walls.

| `n`, `ε` | cube | `p = 0.4` | `p = 0.3` |
|---|---|---|---|
| `12`, `0.25` | `5.16` | `5.42` | `6.05` |
| `12`, `0.5` | `5.16` | `3.60` | `4.08` |
| `14`, `0.5` | `4.72` | `3.73` | `4.65` |
| `16`, `0.25` | `9.52` | `5.93` | `7.38` |
| `16`, `0.5` | `4.40` | `4.15` | `4.96` |
| `16`, `1.0` | `4.40` | `2.71` | `3.20` |

No consistent sign.  This is expected: the exponents differ by `0.005–0.011` per site, a factor `≤ 1.2` at `n = 16`, while the cube's packing number jumps by factors of two with the integer radius `k*`, and the polynomial prefactors of the cube's own upper bound (`ln(1/δ)`·poly) are larger still.  No enumeration at `n ≤ 16` can decide the sign of a difference of exponents of this size.  What *is* decisive at finite size is the quantity that tensorises: the exact game function over site-wise labels is `0.3211` against `0.2316` (`n = 8`, `p = 0.3`, `t = 0.45`), and §4.4 turns one block into a statement for every `n`.

---

## 5. Task C — §11.25 says function-of-type known parts are never harder than the cube; the report says a Markov chain is.  No contradiction

1. **Scope.**  §11.25 (Lemma 11.89, Theorem 11.90, Corollary 11.91) is about *exchangeable* reference measures — uniform on every type class — and its proof is the decomposition "inside a type class the known part is constant, across type classes there are only `n + 1` terms".  The nearest-neighbour energy is not a function of the type for any `K ≠ 0` (inside a type class it ranges over all numbers of domain walls).  The two families of known parts meet only in the uniform cube, where both reports give the cube (`c* = 0`, `0.0291391`).
2. **What §11.25 covers even inside its scope:** the hinted exponent of symmetric instances and the exponent of fixed samples, at extensive accuracies; not adaptive algorithms without a hint (Conjecture 11.94).  The report's statements are about the hinted exponent at the hardest instance of the chain's class, which is not a symmetric instance in any sense — no group with polynomially many orbits acts.
3. **The same method cannot contradict §11.25.**  For an exchangeable `π` the problem is `S_n`-invariant and `Q ↦ max_φ(1−t)D_t(π_φ‖Q)` is convex, so the optimal centre is exchangeable and Lemma A's bound is one "that symmetric instances give" — exactly the kind Corollary 11.91 caps.  Checked with the *same* code (`r11_11_contrast_meanfield.py`; all `2ⁿ` site-wise labels, `u = 1`, `t = 0.45`): ratio of `G_t/n` to the cube for `n = 8, 10, 12`:

   | known part | `n = 8` | `10` | `12` | `Var(m)/n` (`n = 12`) | largest spread of `ln Q*` inside a type class |
   |---|---|---|---|---|---|
   | chain `p = 0.4` | `1.172` | `1.175` | `1.177` | `1.45` | `5.7` |
   | chain `p = 0.3` | `1.387` | `1.389` | `1.392` | `2.15` | `10` |
   | Curie–Weiss `βJ = 0.5` | `1.132` | `1.105` | `1.087` | `1.75` | `≤ 7·10⁻⁶` (solver tolerance) |
   | Curie–Weiss `βJ = 0.9` | `1.305` | `1.223` | `1.168` | `3.23` | `≤ 10⁻⁶` |
   | Curie–Weiss `βJ = 1.5` (two phases) | `1.464` | `1.272` | `1.138` | `7.74` | `≤ 10⁻⁷` |
   | mean-field antiferromagnet `βJ = −1` | `1.061` | `1.048` | `1.039` | `0.51` | `≤ 10⁻⁶` |

   For the function-of-type known parts the excess over the cube is `O(1)` in total — it decays like `1/n` per site (`n ×` excess `≈ 1.06, 1.05, 1.04` for `βJ = 0.5`) — and the centre is a function of the type; for the chain the excess per site is constant and grows slightly with `n`.  (Finite-`n` values above the cube do not contradict Corollary 11.91, which is a statement about exponents with polynomial factors.)
4. **Mechanism (heuristic).**  For small slopes the game function is `t(1−t)u²/8` times the variance per site that a label can couple to.  In a mean-field model the enhanced variance sits in one collective mode — the type — and one mode contributes `O(1)`, not `O(n)`, to `G_t`; the `n − 1` directions inside a type class see the uniform measure of the slice (the comparison of a slice with the cube, Theorem 11.90, rests on the two-by-two inequality of Lemma 11.89).  In a chain every block of more than a correlation length has an enhanced variance of its own magnetisation, `≈ χ·|B|`, `χ = (1−p)/p`, and the blocks are nearly independent: `n/ℓ` enhanced modes.  Labels constant over domains couple to exactly these.  This is also why the small-slope ratio is `χ` (reproduced: `2.271 … 2.331` at `u = 0.05`, `χ = 2.333`), and why the sign of the coupling does not matter: the sublattice flip `s_i → (−1)^is_i` is an isometry of the Hamming cube that maps `p` to `1 − p`, so a nearest-neighbour *anti*ferromagnet raises the exponents by the same amount — while a mean-field antiferromagnet has the cube's values in the two exponents that Corollary 11.91(ii) covers.
5. **Other statements of the theory report that could be read against the result** — "a field always helps" (Proposition 11.65(b)): in bond variables the chain *is* a biased product measure, but the Hamming envelope on spins is not a product envelope in bonds (one bond flip moves a whole tail of spins), so the class is far larger than the `u`-Lipschitz class of the bond cube; the universal ceiling `F*(t) ≤ t(1−t)D²/8` (Proposition 11.103(f)): it holds per site of a *product* landscape with site diameter `D`; for a block it is `(Lu + 2K)²`, no constraint.  §11.15 (chains as known parts) concerns the minimum, not `ln A`.  I found no statement of the theory report that the result contradicts.

---

## 6. Task D — the report's own lists (§10, §11)

* §11, "No referee": this report.  "Theorems 11.95, 11.98(d), 11.101(b) … unrefereed and not re-derived": still true of my review; it limits the *upper* halves only (M1).
* §11, "The conservative recursion was validated by three controls, not by a second implementation": now it has one (§4.5); the two agree (mine `≤` theirs).
* §11, "The upper bounds use symmetric first-order Markov references … not tight (gap 6–50 % in `h`)": with the reference optimised at `p = 0.1` the gap there is about `41 %`, not `50 %` (m2).
* §11, "The lower bounds for `p = 0.1` ignore non-additive labels": reproduced at `n = 4` (`a_4 = 0.5726559` against `0.5626014`, weight `0.0920` on `±min(|x|, 4−|x|)`); it can only raise the true values.
* §11, "`E_∞ = E_F`: certified margins `≤ 2·10⁻⁴`": sharpened to `10⁻¹⁰` for `p ≥ 0.14` (m4).
* §10, item 4 (a threshold claim made too early; discretising the adversary errs on the unsafe side): I confirm the lesson and that the superseded numbers are not used in the final tables; the final tilt-state numbers are consistent with my safe scheme.
* §10, item 9 (two rows of the (L′) table written from memory): the corrected rows agree with my recomputation.
* Nothing in §10 or §11 undermines the headline.  The one thing those lists omit is the accuracy regime of the upper halves (M1(β)).

---

## 7. What I did not check

* Theorems 11.22, 11.27 (machine-checked) and their Lean files: not opened; I re-derived only how they are applied.  Theorems 11.95, 11.97, 11.98(d), 11.101(b), 11.54, 11.58: read, not re-derived; everything in the report that is "given" these stays "given".
* The workstream's code: not audited.  I read `y07_block_labels.py` (after my own runs) and the outputs `y00, y01, y03, y06, y07, y08, y09, y13, y16`.  `ylib.py`, `ylyap.py`, `ydp2.py`, `ydp3.py` unread.
* Exact enumerations at `n = 5` (395 094 vertices), the site-wise optimum at `n = 12` at `t = 0.431`, the label statistics of line 452, the controls of `y15`, the strong-coupling DP numbers for `p ≤ 0.05`, the `a`, `E` columns of §6.1.
* The report's safe discretisation (`ydp3.py`) itself; I only compared its outputs with my own scheme.  My tilt-state `a`-bounds are at `G = 401` only; my certified `h`-bounds at `G = 401` (`G = 801` for `p = 0.3`, `G = 601` for `p = 0.1`; single values of `t` up to `G = 1601`).
* §8, items 1, 2 and §9: read only.
* Floating-point rounding: not controlled (neither in the report nor here).  No prior-art search.
* The hinted exponent of the zero residual of the chain (the report did not compute it either); slopes other than `u = 1` beyond the table of §6.5; alphabets with more than two letters; chains with a field.

---

## 8. Scripts (run each with `python3 <script>` in `code/`)

| script | what | output | time |
|---|---|---|---|
| `r11lib.py` | library (see §4) | — | — |
| `r11_00_controls.py` | cube value three ways; field control; Lyapunov operator against exact increments | `r11_00_controls.txt` | 2 s |
| `r11_01_reductions.py` | (U), (L), (L′) brute force | `r11_01_reductions.txt` | 5 s |
| `r11_02_packing_small_n.py` | hard packing at `n = 10…16`, Markov against cube | `r11_02_packing_small_n.txt` | 330 s |
| `r11_03_propH.py` | Proposition H: formula, limit, `p → ½`, finite `n` | `r11_03_propH.txt` | 6 s |
| `r11_04_propI.py` | Proposition I: formula; headline lower ends (`G_L`-optimal `M_L`) | `r11_04_propI.txt` (`_p0.4.txt`: first, slower run) | 225 s |
| `r11_04b_propI_optimised.py` | the same with the bound maximised over `M_L` | `r11_04b_propI_optimised.txt` | 25 s |
| `r11_04c_a_lower.py` | lower ends of `a` from Proposition I | `r11_04c_a_lower.txt` | 2 s |
| `r11_04d_iteration_cap.py` | the headline lower ends with Arimoto stopped at the report's iteration cap (m1) | `r11_04d_iteration_cap.txt` | 3 s |
| `r11_05_certificate.py` with `A [p …] [L16]` or `B` | the independent certificate; end-to-end `n = 16` | `r11_05_certificate_A_*.txt`, `r11_05_certificate_B.txt`; `r11_05_certificate.txt` is the first run, with `L = 16`, stopped by my time limit after `p = 0.2, m = 1` — it holds the `L = 16` values of `p = 0.3, 0.2` | 25 s (`L ≤ 14`); 5–8 minutes per `p` with `L = 16` on the loaded machine |
| `r11_05b_certificate_gap.py` | the certificate with gaps, end to end (`n ≤ 11`) | `r11_05b_certificate_gap.txt` | 1 s |
| `r11_06_propD.py`, `r11_06b_L_accuracy.py` | Proposition D, tables of §§6.1, 6.2, all vertices | `r11_06_propD.txt`, `r11_06b_L_accuracy.txt` | 195 s, 25 s |
| `r11_07_propF.py` | Proposition F: inequality, DP tables | `r11_07_propF.txt` | 40 s |
| `r11_08_propG.py` with the argument `test`, or `h p G`, `E p [G]`, `a p [G]` | Proposition G: tests; safe bounds for `h`, `E`, `a` | `r11_08_propG_*.txt` | 5 s; 25–140 s per `p` at `G = 401`; 185 s (`p = 0.3`, `G = 801`), 290 s (`p = 0.1`, `G = 601`) |
| `r11_08b…e` | `Q = π` remark; grid convergence; reward test; cube control | `r11_08b…e_*.txt` | `≤ 30` s each |
| `r11_09_misc.py [a b c d e f]` | slopes, `a` from Prop. H, site-wise optimum, strong coupling, §8.3, Prop. J | `r11_09_misc_*.txt` | 25 s |
| `r11_10_structure.py` | vertices, `F*_n`, `a_4`, centre not Markov, Lemma B | `r11_10_structure.txt` | 3 s |
| `r11_11_contrast_meanfield.py` | chain against function-of-type known parts | `r11_11_contrast_meanfield.txt` | 115 s |
