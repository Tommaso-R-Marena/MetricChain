# Independent numerical check of the rate of the level recursion (the theory division's Theorem R = Theorems 11.53a, 11.53b)

*Computational Research Division.  The work and the report below are by an independent
subagent of this division (an AI agent), written from the statements of the theory
division's `R_REPORT.md`; the coordinator's note at the end says what the coordinator
checked.  Paths are relative to the repository root.  Not external peer review.*

## 0. Bottom line

- **The limit `lim k²(τ_k − h) = 2π²h²ϑ` is reproduced** for the two validation pairs, for all
  six two-type products asked for, for the biased cube (`p = 0.3`, `u = 1`) and for seven
  stress instances.  In every case with (H1): the proved lower bound (lines) extrapolates
  to ratio `1.00000` (`k` up to 5120), and an upper bound of `τ_k` derived and computed
  independently extrapolates to `1.0000 ± 0.0002` (`k ≤ 160`).  No counterexample to the
  theorem was found.
- **Both validations reproduce.**  Gaussian exact bounds: identical integers.  Cube constant
  `0.0711473 = 0.64129·a`, `τ₂ = 0.50041a`, `τ₃ = 0.36118a`: confirmed.
- **A new tool, not in the theory division's report at the pinned commit:** a
  convex-majorant scheme that gives *upper bounds of `τ_k` at every finite `k`* (proof in
  §3; floating point, not interval arithmetic).
- **Discrepancies found (none touches the theorem):** the theory division's "grid
  recursion" values lie above these upper bounds at every `k` compared; its biased-cube
  constants are off by −0.6 % to +0.3 %; `τ₄₀/a = 0.2631` should read `0.2630`; the correction
  "`c ≈ 0.15–0.25`" is not universal.  Details in §7.
- **Where the hypothesis fails:** not in any product of binary symmetric sites (calculus),
  but for the uniform four-letter Hamming site at `u = ln 3` (outside the binary family).
  There (H1) fails exactly and the rate is `1/k` (§6).

## 1. Pin and sources

- Pinned theory commit: `fc3f5d989846ff5900034a5b072c24d9c4fd35b8`.  The theory branch has
  since moved (workstream Z: certified upper bounds of the same exponents); it was not
  read.
- Read as text only, nothing executed: `docs/workstreams/R_REPORT.md` (all);
  `docs/THEORY_REPORT.md` §11.16, §11.18, §11.19 remark (1), §11.20 (setting, Theorem 11.59,
  Lemma 11.60, Proposition 11.65), §11.21, §11.26;
  `experiments/coordinator_checks/level_rate/`: `README.md`, `pairs.py`, the first 150 lines
  of `iterate_exact.py`, `out_lines_lb.txt`, `out_lines_lb_general.txt`;
  `experiments/workstreams/R/out_r3_gauss_exact_lb.txt`.
- Not read: `rlib.py`, `r1_checks.py`, `r2_chain.py`, `r3_gauss_exact_lb.py`, `lines_lb*.py`,
  `dual_ub_*.py`, `ub_subsolution.py`, `epochs.py`, `ode_f0.py`, the other output files, the
  Lean files.
- One thing to add to the brief: for products, Theorem 11.101 starts the recursion from
  complete enumeration `T₁ ≡ Σλ_j ln q_j`, not from `θ_na`.  `T₁ = θ_na` was run as instructed.
  By hand, `R[b] = θ_na` for a constant `b ≥ a`, so that start is exactly one level behind
  and the limit is the same.

## 2. Mathematics implemented

**Pair from a game function.**  `F` concave on `[0, 1]`, `F(0) = F(1) = 0`.

- `θ_hint(e) = R̂(e) = max_t [F(t) − te]`, `S(e) = e + R̂(e)`, `θ_na = R̂∘S⁻¹`.
- Parametrically, for `t ∈ (0, 1)`: `x = F(t) + (1−t)F′(t)`, `θ_na(x) = F(t) − tF′(t)`, slope
  `−t/(1−t)`.
- `a = θ_na(0+) = −F′(1)`, `E = F′(0)`, `h = max F = F(L)` with `θ_na(h) = h`.
- Dual function `J(t) = inf_e [(1−t)θ_na(e) + te] = F(t)`.
- `ϑ = −1/J″(L) = θ_hint″(0) = θ_na″(h)/(1 + |θ_na′(h)|)³`.  The three forms were checked
  against each other by finite differences of `θ_na` and `θ_hint`.

**Instances.**  Gaussian: `F = t(1−t)`.  Cube: `F = Λ(tu) − tΛ(u)`; cross-checked against the
KL formulas of §11.16 and (11.18.1).  Products: `F = Σλ_j[(1−t) ln 2 − ln(p_j^t + q_j^t)]`.
Biased cube: `F = (1−t)·C_t` (Rényi capacity of the two vertex Gibbs laws, Theorem 11.99),
put in closed form; it agrees to `10⁻¹²` with the cosh form of Theorem 11.59(b) maximised
over `γ`.

**Recursion.**  `T₁ = θ_na`, `T_{k+1} = min(T_k, R[T_k])`, `τ_k = sup T_k = T_k(0+)`, with
`R[T](g) = inf_{0<φ<1, 0<β<g} sup_{γ≥β}[min(γ, φθ_na((g−β)/φ)) + (1−φ)T(γ/(1−φ))]`.

**Slope map.**  `Σ(B, s) = sup_e [B − (1−s)θ_na(e)]/e = t′(1−s)/(1−t′)`, where `t′` is the least
`t` with `J(t)/(1−t) ≥ B/(1−s)`; infinite iff `B/(1−s) ≥ a`.  Orbit: `p₀ = 0`,
`p_{j+1}(B) = Σ(B, p_j(B))`.  Two routes (definition and dual form) agree to `10⁻⁹`.

**Hypotheses.**  (H0): `θ` convex, nonincreasing, `a < ∞`, `h < a`.  (H1): `J` has a unique
maximiser `L ∈ (0, 1)` and `J = h − (t−L)²/(2ϑ) + o(·)`, `0 < ϑ < ∞`.

**Claim.**  `lim k²(τ_k − h) = 2π²h²ϑ =: C`.

## 3. Methods and the status of each number

Write `r_k = k²(x_k − h)/C`.

**(b) Lines: lower bound `LB_k = B_∞(k) = sup{B : p_k(B) < ∞}`.**

- What is proved: Proposition A of `R_REPORT.md`.  If `p_k(B) < ∞` then `T_k(x) ≥ B − p_k(B)x`
  for all `x`, hence `τ_k ≥ B_∞(k)`.  It is the theory division's proof; they label Lemma L
  machine-checked.  Lemma L (two cases at `γ₀ = max(β, μ)`) and the induction were
  re-derived by hand; the Lean was not compiled.
- Numbers are a double-precision evaluation of that bound.  They agree with 30-digit
  mpmath to `≤ 10⁻¹¹` relative in the excess `B − h` (`k = 2, 3, 10, 40, 160`).
- Certified: by interval arithmetic for the cube and all symmetric products at
  `k = 2, 3, 10, 40, 160` (12 decimals, rounded down, proved; value `+ 3·10⁻¹²` not provable).
  By rational arithmetic for the Gaussian pair.
- `k > 160`: floating point only.

**(a2) Convex majorants: upper bound `UB_k ≥ τ_k`.**  This derivation is the subagent's and
is not refereed.

- *Setup.*  For `T` nonincreasing, `c = 1−φ`, `μ = φθ((g−β)/φ)`, `S = x + T`: the supremum over
  `γ` is `c·max_{[β/c, μ/c]} S` if `β ≤ μ` ("regime 1") and `μ + cT(β/c)` otherwise ("regime 2").
- *Claim A.*  For convex nonincreasing `M ≥ T_k`, with `x_m = argmin S_M` and
  `S̃(x) = S_M(max(x, x_m))`, put `H₁ = max(β + cM(β/c), c·S̃(μ/c))`.  Then `H ≤ H₁` pointwise,
  with equality in regime 1 because `S_M` is convex.
- *Claim B.*  `H₁` is jointly convex in `(φ, β, g)`: perspectives of the convex functions `M`,
  `S̃` (nondecreasing) and `θ`.  So `R₁[M](g) = inf H₁` is convex in `g` and `T_{k+1} ≤ R₁[M]`.
  Hence the lower convex hull of points `(g_i, v_i)`, with `v_i` the value of `H₁` at any
  feasible `(φ, β)`, is a convex majorant of `T_{k+1}`.  At `g → 0`,
  `τ_{k+1} ≤ inf_φ max(cM(0), cS̃(φa/c))`.
- *Claim C.*  If `T_k` is convex and `≤ θ`, regime 2 never helps: there
  `H = φθ(x₁) + cT_k(x₂) ≥ T_k(g)`.  So `T_{k+1} = min(T_k, R₁[T_k])` exactly.
- *Consequence.*  The scheme is an upper bound unconditionally.  It converges to the
  recursion itself as the grid is refined, provided `R₁[T_k] ≤ T_k`.  That condition is
  monitored: it held at every node and level of every run (`n_above = 0`).
- *Errors.*  Every approximation is on the safe side (restricted infimum, chords of `M`,
  chords of `θ`).  Evaluation is IEEE double with a margin of `10⁻¹³·a` per level, not
  interval arithmetic.  Error estimate: `N = 16000` against `8000` (validation) or `4000` (new
  instances).

**(a1) Recursion with no structural assumption: approximation `GEN_k`.**  Linear
interpolation in `√x`; exact supremum over `γ` for the interpolant (range maximum); infimum
by a blind two-dimensional scan in (logit `φ`, logit `β/g`) plus refinement, and by a search
along the balance curve.  Neither an upper nor a lower bound; its interpolation bias is
negative and second order (about `−2·10⁻⁶·a` at `N = 1000` after 40 levels).  A check of
structure, not of digits (§4).

## 4. Validation

All numbers are in `results/summary.json` and `results/extras.json`.

**Gaussian pair** (`C = π²/16 = 0.6168502751`).

- Exact lower bounds (rational arithmetic): `N/10⁹ = 381966011, 307978528, 255679562,
  250376448, 250023947` at `k = 2, 3, 10, 40, 160`.  Identical to the theory division's.
- `(k + ½)²(B − ¼)/(π²/16) = 1.015111, 1.001003, 1.000049` at `k = 10, 40, 160`.  Theirs:
  `≥ 1.0151, 1.0010, 1.00005`.
- The closed form `(k−1)ψ + φ₀ = π` agrees with the orbit to `10⁻¹³` (`k ≤ 160`).
- Passage times `0.764, 0.906, 0.968, 0.990, 0.997`: reproduced.
- (C2) of Lemma RC: `0.3005` against `0.45`, and `0.481` against `0.35`: reproduced.

| `k` | LB | UB (`N = 16000`) | `r_LB` | `r_UB` | the theory division's grid `r` |
|---|---|---|---|---|---|
| 2 | 0.381966011250 | 0.500000000000 | 0.85574 | 1.62114 | 1.62330 |
| 3 | 0.307978528370 | 0.355232778414 | 0.84592 | 1.53537 | 1.54558 |
| 10 | 0.255679562796 | 0.255994759004 | 0.92074 | 0.97183 | 0.97631 |
| 40 | 0.250376448355 | 0.250381095215 | 0.97644 | 0.98849 | 0.98985 |
| 80 | 0.250095213439 | 0.250095799459 | 0.98787 | 0.99395 | 0.99490 |
| 160 | 0.250023947348 | 0.250024021486 | 0.99384 | 0.99692 | 0.99818 |

- `UB(8000) − UB(16000) ≤ 2.6·10⁻⁹` at every `k` (`8.5·10⁻⁵` of the excess at `k = 160`).
- Richardson limit from `k = 40, 80, 160`: LB `0.99999`, UB `1.00006`, grid-extrapolated UB
  `0.99999`.  LB from `k = 1280, 2560, 5120`: `1.00000`.
- `τ₂ = ½` exactly.
- `τ₃` computed with no grid for `T₂` (closed-form `T₁`, then the balance equation):
  **`0.3552327782`**.  `UB₃` exceeds it by `2·10⁻¹⁰`.

**Cube `u = 1`.**  `a = 0.1109440717`, `h = 0.0291391385`, `L = 0.4900342764`, `ϑ = 4.2449775668`,
`C = 0.0711473217 = 0.641290·a`.  All the theory division's constants are confirmed, and
their lines values are reproduced to all printed digits.

| `k` | LB | UB (`N = 16000`) | `r_LB` | `r_UB` | the theory division's grid `r` |
|---|---|---|---|---|---|
| 2 | 0.044184665340 | 0.055517524922 | 0.84588 | 1.48303 | 1.48348 |
| 3 | 0.035786649711 | 0.040071198438 | 0.84090 | 1.38288 | 1.39841 |
| 10 | 0.029793415913 | 0.029819259296 | 0.91961 | 0.95593 | 0.95956 |
| 40 | 0.029182546348 | 0.029182939623 | 0.97618 | 0.98502 | 0.98643 |
| 80 | 0.029150118960 | 0.029150168725 | 0.98774 | 0.99221 | 0.99320 |
| 160 | 0.029141900404 | 0.029141906726 | 0.99378 | 0.99605 | — |

- `UB(8000) − UB(16000) ≤ 3.1·10⁻¹⁰`.
- `τ₂` closed form `= 0.055517524915 =` **`0.50041a`**; `UB₂` agrees to `6·10⁻¹¹·a`.
- `τ₃` grid-free `= 0.0400711984 =` **`0.36118a`**.  The theory division's "`0.500a`" and
  "`0.361a`" are confirmed.
- Upper bounds `τ_k/a ≤ 0.31069, 0.28975, 0.28017` at `k = 4, 5, 6` (theirs: `0.311, 0.290, 0.280`).
- Richardson limits: LB `0.99999` / `1.00000`, UB `1.00005`, extrapolated UB `0.99999`.

**(a1) against (a2).**  Gaussian, `N = 1000` and `2000`, `K = 40`: `S` quasi-convex at every
level; largest concave corner `5.5·10⁻⁸·a`, falling to `8.5·10⁻⁹·a`; regime 2 never optimal;
the blind scan never gets lower than the balance search by more than `5.8·10⁻⁸·a`, and
misses narrow valleys by up to `1.4·10⁻³·a`.  On the same grid
`GEN − UB ∈ [−2.2·10⁻⁶, 0]·a` at `N = 1000` and `[−5.5·10⁻⁷, 0]·a` at `N = 2000`; the error ratio
is about 4; the extrapolated GEN agrees with UB to `6.6·10⁻⁵` of the excess at `k = 40`.
Cube at `N = 1000` and product `(4, 1; ¼)` at `N = 1000`, `K = 24`: the same picture.
**Limitation, stated plainly:** for the product `(4, 1; ¼)`, where the sandwich is tightest,
GEN at `N = 1000` falls *below* the proved lower bound from `k ≈ 15` on (by `1.2·10⁻⁶·a` at
`k = 20`).  This is its interpolation bias; it is why the one-sided scheme carries the
conclusions.

## 5. New instances

Upper bounds at `N = 16000`, `K = 160`, with `N = 4000` as the coarse check.  The difference
between the two grids is `3.7·10⁻⁴` to `5.3·10⁻⁴` of the excess at `k = 160`, so the error at
`N = 16000` is about `3·10⁻⁵` if second order.

| instance | `h` | `ϑ` | `C = 2π²h²ϑ` | `r_LB / r_UB` at `k = 10` | `k = 40` | `k = 160` | `k²(τ − h)` at 160, LB / UB |
|---|---|---|---|---|---|---|---|
| `(2, 0.5)`, `λ₁ = 0.25` | 0.0300545461 | 4.030446 | 0.071862647 | 0.91745 / 0.93665 | 0.97568 / 0.98063 | 0.99366 / 0.99495 | 0.07140683 / 0.07149973 |
| `(2, 0.5)`, `λ₁ = 0.5` | 0.0524614168 | 2.293963 | 0.124622407 | 0.91686 / 0.93343 | 0.97555 / 0.97980 | 0.99362 / 0.99474 | 0.12382774 / 0.12396665 |
| `(1, 0.5)`, `λ₁ = 0.25` | 0.0130387278 | 9.522328 | 0.031955332 | 0.91999 / 0.96076 | 0.97627 / 0.98606 | 0.99380 / 0.99631 | 0.03175721 / 0.03183752 |
| `(1, 0.5)`, `λ₁ = 0.5` | 0.0184053361 | 6.732845 | 0.045021073 | 0.91979 / 0.95816 | 0.97622 / 0.98550 | 0.99379 / 0.99617 | 0.04474145 / 0.04484878 |
| `(4, 1)`, `λ₁ = 0.25` | 0.0811058733 | 1.413605 | 0.183553421 | 0.91326 / 0.91351 | 0.97481 / 0.97484 | 0.99345 / 0.99349 | 0.18235162 / 0.18235888 |
| `(4, 1)`, `λ₁ = 0.5` | 0.1337468548 | 0.822415 | 0.290394118 | 0.91000 / 0.91000 | 0.97402 / 0.97403 | 0.99326 / 0.99329 | 0.28843558 / 0.28844505 |
| biased `p = 0.3`, `u = 1` | 0.0250335375 | 4.939435 | 0.061101448 | 0.91965 / 0.95598 | 0.97619 / 0.98504 | 0.99378 / 0.99606 | 0.06072150 / 0.06086056 |

- **Verdict for all seven: consistent with the theorem's limit.**  Richardson limits
  (`k = 40, 80, 160`): LB `0.99999`; UB `1.00005–1.00007`; grid-extrapolated UB
  `0.99999–1.00000`.  LB from `k = 1280, 2560, 5120`: `1.000000`.  `r_LB(5120) = 0.99979–0.99980`.
- `n_above = 0` and all raw values convex in every run.  `UB₂` equals the closed-form `τ₂` to
  `≤ 3·10⁻¹⁰·a`.
- Interval-certified lower bounds at `k = 2, 3, 10, 40, 160` for the six products.
- For `(4, 1)` the lines lower bound is essentially the truth: `UB − LB` is `4·10⁻⁵` of the
  excess at `k = 160`.

**Biased cube: what the theory division computed and what is reproduced.**  Their
`out_lines_lb_general.txt` gives four biased cubes, lower-bound side only.  Their `B` values
are reproduced to `6·10⁻⁸` and are slightly low; their `h` is low by `1–2·10⁻⁸`; their `ϑ` is
off (§7).  With accurate constants all four give `r_LB(160) = 0.99366–0.99379`, against the
cube's `0.99378`.  So "biased cubes obey the same law" holds, more cleanly than their
table shows.

**(H1) for these pairs.**  Products of symmetric sites:
`F*″(t) = −Σλ_j u_j² e^{tu_j}/(1 + e^{tu_j})² < 0` everywhere, so (H0) and (H1) hold exactly —
calculus on the formula of Theorem 11.98, not a numerical statement.  Numerical checks,
all nine pairs: `J` evaluated from `θ_na` itself equals `F` to `≤ 10⁻¹⁶`; second differences of
`J` at `L` match `F″(L)` to five digits; `F` is concave on a 20001-point grid; `L < 1 − h/a`.
Biased cube: (H1) is numerical only (two closed forms agree; concave on the grid;
`J″(L) = −0.202452`).  Lemma PT: `√δ·N_t/c* = 0.9966–0.9971` at `δ/h = 10⁻⁶` for all nine.
(Σ6): ratio `1.004` at `(δ/h, v) = (10⁻⁶, 10⁻³)`.

## 6. Attempts to break it

**1. Hypotheses inside the family.**  They cannot fail for products of binary symmetric
sites (above).  Biased binary sites: numerically concave.

**2. Extreme products** (boundary layers of `F`, three types, steep and shallow cubes).  LB
to `k = 5120`, UB at `N = 4000` to `k = 80`.

| instance | `r_LB` at `k = 10 / 80 / 160 / 5120` | `r_UB` at 80 |
|---|---|---|
| `(12, 0.3)`, `λ₁ = 0.03` | 0.95527 / 0.99470 / 0.99737 / 0.99992 | 0.99491 |
| `(20, 1)`, `λ₁ = 0.01` | 0.90550 / 0.98612 / 0.99298 / 0.99978 | 0.98879 |
| `(30, 0.05)`, `λ₁ = 0.002` | **1.03525 / 1.00593 / 1.00301 / 1.00010** | 1.00632 |
| three types `(0.3, 3, 12)`, ⅓ each | 0.91122 / 0.98786 / 0.99389 / 0.99981 | 0.98806 |
| cube `u = 20` | 0.83673 / 0.97633 / 0.98803 / 0.99962 | 0.97667 |
| cube `u = 0.05` | 0.92073 / 0.98787 / 0.99384 / 0.99980 | 0.99403 |
| biased `p = 0.02`, `u = 2` | — / 0.98756 / 0.99369 / — | 0.98992 |

- All have Richardson limit `1.0000` (LB); none breaks.
- `(30, 0.05; 0.002)` approaches the constant **from above**: `k²(τ_k − h) > C` for all `k`
  computed.  So `τ_k ≤ h + C/k²` is false in general at finite `k`.
- The `1/k` correction is pair-dependent in size and sign.  Writing `τ_k ≈ h + C/(k + c)²` at
  `k = 160`, `c` from the lower bound runs from `−0.24` to `+0.97` over the stress set.

**3. Proposition U.**  150 random convex `W` for each of three pairs, 9 accuracies each.  The
convex-programme value exceeds the bound `U` by `≤ 1.8·10⁻⁴·a` at `N = 3000` and `≤ 3.8·10⁻⁵·a`
at `N = 12000` (discretisation, shrinking), and is never below the Lemma L bound.
Equality with `U` holds also when `W` is not a sub-solution.  Not broken.

**4. Negative controls (their §9).**  Kinked pair: `k(τ_k − ¼) ∈ [0.0635, 0.0649]` at `k = 80`;
local exponent `−1.02` to `−1.04`: rate `1/k` with the coefficient `1/16` of Proposition K.
`F = h(1 − |2t−1|⁴)`: LB local exponent `−1.388` falling to `−1.3341` (`k = 2560–5120`),
consistent with their heuristic `−4/3`; UB `−1.44` at `k = 40–80`.

**5. Outside the binary family: (H1) fails for a product landscape.**  This is the only
place where the hypothesis was found to fail.  It rests on the theory division's Theorem
11.99 and vertex description, plus a symmetry reduction that is the subagent's.

- For `q` equally likely letters with the Hamming envelope,
  `F*(t) = max_{1≤s≤q−1} Φ_s(t)`,
  `Φ_s = (1−t) ln q + t·ln(se^u + q − s) − ln(se^{tu} + q − s)`.  The Rényi programme is convex
  and permutation-invariant, and linear in the weights of the size classes.
- Checks: reproduces their `q = 3, 4` numbers (`h, a, E` at `u = 1`) to all printed digits;
  agrees with a direct solution over all vertices to `5·10⁻¹⁵`.
- For `q = 4` at **`u = ln 3`**, `Φ₁(t) = Φ₂(1−t)` identically (algebra).  So `F*` has two
  maximisers, `L = 0.488077` and `0.511923`; `J` is flat between them; `θ_na` has a kink at
  `h = 0.0346881852` (slopes `−1.0489` and `−0.9534`).  (H1) fails.
- Numerically at `u = ln 3`: `k(B_∞ − h)/h = 0.0518, 0.0354, 0.0291` at `k = 160, 640, 2560`
  (Proposition K floor `0.0239`).  `k²(B_∞ − h)/C_branch = 3.4, 9.3, 30.6`.  UB agrees (`0.0698`
  against `0.0694` at `k = 80`).  The rate is `1/k`.
- At `u = ln 3 ± 0.02` the law is back: ratio `1.017–1.019` at `k = 160`, `1.002` at `1280`.  At
  `± 0.1` and `± 0.3` it behaves like the cube (`0.995` at 160, `0.999` at 1280), although `F*` is
  non-concave there.

## 7. Discrepancies and ambiguities in the theory division's material (at `fc3f5d9`)

1. **Grid recursion** (`iterate_exact.py`; `R_REPORT.md` §11, README).  Its values are above
   the upper bounds of §3 at every `k` compared.  Gaussian: `0.99818` against `≤ 0.99692` at
   `k = 160`; `τ₃ = 0.35593` against `0.355233`.  Cube: `0.99585` against `≤ 0.99475` at `k = 120`;
   `τ₃ = 0.0401939` against `0.0400712`.  They label it "not one-sided"; from the part read,
   its grids of `e` and `β` fractions and its interpolation in `x` all bias upward.
2. **"`c ≈ 0.15–0.25`"** (`R_REPORT.md` §8).  At `k = 160` the upper bound gives `c = 0.247`
   (Gaussian), `0.317` (cube `u = 1`), `0.30–0.42` for the `(1, 0.5)` and `(2, 0.5)` products,
   `0.52–0.54` for `(4, 1)`.  In the stress set the lower bound alone gives `c` from `−0.24` to
   `0.97`.  The lower bound's "`c = ½`" is exact only for the Gaussian pair.
3. **"The exact dynamics of the best convex majorant"** (`R_REPORT.md` §5 remark (1)) is not
   the recursion: it gives `τ₃ = 5/14 = 0.357143` for the Gaussian pair, where
   `τ₃ = 0.3552328`.  The tolerance `β > 0` matters for majorants with slopes steeper than 1
   near 0.  The README's "`τ₃ = 0.3573`" disagrees with their own grid value as well.
4. **Theory report §11.19 remark (1): `τ₄₀/a = 0.2631`.**  Here
   `τ₄₀/a ∈ [0.263038, 0.263042]` (certified LB, convex UB), so `0.2630`.
5. **Biased cubes** (`out_lines_lb_general.txt`).  From two independent closed forms,
   `ϑ = 4.939435, 10.714893, 2.490334, 9.407514` for
   `(p, u) = (0.3, 1), (0.1, 1), (0.1, 2), (0.02, 2)`.  Theirs:
   `4.954673, 10.649336, 2.492315, 9.426415` (`+0.31 %, −0.61 %, +0.08 %, +0.20 %`).  Their
   printed ratios at `k = 160` (`0.992, 0.998, 0.993, 0.993`) are artefacts of this; here
   `0.99378, 0.99379, 0.99366, 0.99369`.
6. **Hypothesis scope.**  "The law depends on the pair through `h` and the curvature of its
   dual at the maximum only" needs (H1).  By their own Proposition 11.100, `F*` need not be
   concave for three or more letters, and (H1) then fails on a codimension-one set (§6,
   item 5).
7. **Start of the recursion for products:** see §1.
8. No error was found in the statements of Proposition A, Lemma L, Lemma M or Proposition
   U as read; the reading of Proposition U's proof (Sion plus the three cases) found no
   gap.  Lemma T, Proposition C and Lemma RC were not refereed.

## 8. Deliverables, commands, run times

Files in `experiments/eng/level_rate/`: libraries `lr_pairs.py`, `lr_lines.py`,
`lr_recursion.py`, `lr_multiletter.py`, `lr_cases.py`; scripts `run_lines.py`, `run_upper.py`,
`run_general.py`, `run_extras.py`, `run_propU.py`, `run_fourletter.py`, `make_tables.py`;
`results/` (53 JSON files; `summary.json` holds every table entry).  Tests:
`tests/eng/test_level_rate.py` — 24 tests, 12 s on an idle machine.

| command (`python experiments/eng/level_rate/…`) | time per run |
|---|---|
| `run_lines.py <case>` (16 smooth cases, `powertop4`, `kinked --K 80 --no-large`) | 40–930 s |
| `run_upper.py <case> --N 16000 --K 160` (9 cases) | 206–571 s |
| `run_upper.py <case> --N 8000 --K 160` (gauss, cube_u1) | 276, 212 s |
| `run_upper.py <case> --N 4000 --K 160` (7 new) | 112–212 s |
| `run_upper.py <case> --N 4000 --K 80` (stress, negative) | 29–80 s |
| `run_general.py gauss --N 1000 --K 40 --compare` / `--N 2000` | 510 / 519 s |
| `run_general.py cube_u1 --N 1000 --K 40 --compare` | 320 s |
| `run_general.py prod_4_1_l0.25 --N 1000 --K 24 --compare` | 177 s |
| `run_extras.py` | 281 s |
| `run_propU.py --cases 150` | about 4 min |
| `run_fourletter.py` | 184 s |
| `make_tables.py --verify` | 29 s |

About 3.3 CPU-hours recorded in the result files; at most two single-threaded processes
at a time; under 100 MB each.

## 9. Not checked

- The Lean files: not compiled.  Lemma L was re-derived by hand; Lemma M and Proposition U
  were read, not formalised.
- The proof of the upper half of Theorem R (Lemma T, Proposition C, Lemma RC, the
  restart): not refereed.  The evidence is numerical: upper bounds to `k = 160`.
- That `R` is the right recursion for the algorithms (Theorems 11.52, 11.101), and the
  product formulas of Theorems 11.98/11.99.  The only checks were two formulas for biased
  sites and the symmetric reduction for uniform Hamming sites.
- Interval arithmetic for the upper bounds.  Claims A–C have not been read by anyone else.
- The recursion itself beyond `k = 160` (stress and negative cases: `k = 80`, `N = 4000`);
  positive-accuracy profiles; finite `n`.
- For the biased cube, (H1) is numerical only.
- The newer commits of the theory branch.

---

## Coordinator's note (2026-11-27, at checkpoint 6)

**The coordinator's review of this report is not complete.**  Done so far: the test file
run here (24 passed, 11 s); no absolute path, name or address in the delivered files; and
one independent check, of the finding that matters most if true — for four equally likely
letters at `u = ln 3`, `Φ₁(t) = Φ₂(1 − t)` holds identically (verified by hand: the difference
is `t ln 2 + (1 − t) ln 2 − ln 2 = 0`; and numerically to `9·10⁻¹⁶` on a grid), and
`max(Φ₁, Φ₂, Φ₃)` has two maximisers, `0.48808` and `0.51192`, with value `0.0346881852` against
`0.0346682` at `t = ½`.  So the dual function of that product landscape has no unique
maximiser, as the report says.  Not yet done: reading Claims A–C of §3; re-running any of
the campaigns; comparing with the theory division's workstream Z, which has since
certified upper bounds of the same exponents by interval arithmetic (its `c₂ … c₆ =
0.5004, 0.3633, 0.3128, 0.2914, 0.2813` in units of `a` at `u = 1`; this report's
`0.50041, 0.36118` and upper bounds `0.31069, 0.28975, 0.28017` are below them, as two
correct sets of numbers must be: theirs are certified upper bounds, these are
floating-point values and bounds).  The report is filed now so that it is preserved; a
message to the theory division with its findings follows when the review is done.
