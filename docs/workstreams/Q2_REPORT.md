# Workstream Q2 — the bounded levels without their `√n`; the slope step at a general outer rate

> **Coordinator's note (2026-11-26, after the internal review `Q2_REVIEW.md`).**  The referee
> (brief `Q2_review_brief.md`; own evaluator; code under `experiments/workstreams/Q2/review/`)
> re-derived every statement and found **no substantive error or gap**: Lemma U, Corollary
> U1, Propositions D′, T, A′, N, Q6(e) with its corollary, and Theorems A, B are correct as
> stated.  The text below is the workstream's as delivered.  **Errata — its six findings of
> wording, none of which changes a statement:**
> 1. *(C3) and Lemma U.*  The exclusion "all `σ_i = 0` if `R = ∞`" is not needed: Lemma U holds
>    with the same proof and constants for lines valid at all accuracies, provided the
>    maximum is nonnegative at the one accuracy `max(G, b)` in dimension `n_i` (a flat line,
>    or (C2)); the cap may be any `Ξ` with `n_o·θ_na(e) ≤ Ξ ≤ n`.  Without the range condition
>    `Ξ ≤ R·n_i` the proof gives `ln C_max ≤ max_i[n_iB_i + n_oϑ − σ_i·min(n_oϑ, R_in_i)] + ℓ₀^b + E`.  What the
>    proof uses of the inner majorant `T` is only that it is nonincreasing with `x + T(x)`
>    nondecreasing: `ln C_max ≤ ℓ₀^b + E₁ + Y + T(Y)`, `Y = max(n_oϑ, b)`.  (Used in `Z_REPORT.md`.)
> 2. *Proposition A′, the parenthesis after the display of `ℓ̄_T`:* the condition should read
>    `9(ln 2/a − 1) + (ln 2 − a)/u ≤ 8(ln 2/h − 1) + ln 2/(2u)` (the base chain has `𝒳_B/(2u) ≈ 2 ln n/(2u)`); it
>    holds with a factor `3.5`–`5` at `u = ½, 1, 2`.
> 3. *Proposition D′, remark (2) (`R > 1`):* `q^b` changes as well (`ln 4L ≤ ln 4A_n^b`), and the
>    hypothesis "`Ξ ≤ n`" of Lemma U has to be dropped with it.  The remark is not used.
> 4. *§4.3, remark 2:* the least block of (4.1) always exists, but for small `N` it is `≥ N`;
>    the chain then has no level and the family is the base bracket at `α̲` (covered by
>    the proposition with `j ≡ 0`, error `e₀`).
> 5. *§6.2, remark 2:* "`σ_i′ < 0` … (possible for `e < h`)" presupposes `B_i ≥ h`; "a type with
>    range `R′` is also a type with any smaller range" needs `σ ≥ 0`.
> 6. *Wording:* Lemma U needs "`Ξ ≤ n`" only for `L ≤ n` in the constants; (C2) is used in two
>    proofs (Lemma U: the outer sample; Proposition T: `ln C₁ ≥ 0`), at one point each.
>
> The referee also confirms the report's criticism of `Q_REPORT.md` §6.2 ("a `√n` remains in
> any case" is wrong: the design with `M = 0` delivers a bounded accuracy at a certified
> cost *below* `e^{n·a}`).  Not checked by the referee: Theorem 11.56 itself; the nest beyond
> three epochs and `n = 8·10³`; simulated runs.

Independent report on the brief `docs/workstreams/Q2_brief.md` (after the twenty-second checkpoint of cycle 10,
2026-11-26) and on the coordinator's addition to it of the same day (the drop for an inner family of any slope
`0 ≤ σ ≤ 1` and for maxima of lines).  Paper proofs with exact numerical checks; no Lean.  Nothing in the
repository was edited; the only files created are this report and the scripts and stored outputs in
`experiments/workstreams/Q2/` (§10).  No git command that changes state was run, `lake` and the audit script were
not run, nothing was delegated.

Status labels.  **[proved here]** complete proof in this report (paper proof, unrefereed);
**[quoted]** taken from a named statement of the repository, not re-proved (its own status is given);
**[numerical]**; **[heuristic]**; **[conjecture]**.

Notation: that of `docs/workstreams/Q_REPORT.md` ("Q" below; its statements are cited as Q1, …, Q9a, its formulas as
(2.1), (5.2)): `Q_n`, `L_u(Q_n)`, `p_u = 1/(1+e^u)`, `a = KL(p_u‖½)`, `ρ_h = Λ₁/u`, `h = KL(ρ_h‖½)`, `ε* = ln cosh(u/2)`,
`θ_na(t) = KL(ρ_t‖½)` with `KL(ρ_t‖p_u) = min(t, ε*)`, `H` the binary entropy; `Γ̃`, `Γ″`, `r†`, `π†` and Algorithm 2L⁺ as in
`K_REPORT.md` §2; `N(n; ε, δ)` the least `C` such that some randomised adaptive algorithm without a hint makes at
most `C` evaluations in every run on every `ψ ∈ L_u(Q_n)` and is `(ε/2, δ)`-correct.  All logarithms are natural.
**The bare letter `e` is an outer accuracy rate** (as in the brief: `θ_na(e)`, "Q6(e)"); `e^{y}` with an exponent is the
exponential function, and Euler's number never occurs bare: the constants in which Q writes it are

    c₃ := 3·exp(1) + 1 ≈ 9.155,   c₁₂ := 12·exp(1)·(exp(1) − 1) ≈ 56.05,   c₁₈ := ln(18·exp(1)·(exp(1) − 1)) ≈ 4.432,   c₂₄ := ln(24·exp(1)·(exp(1) − 1)) ≈ 4.719.

---

## 0. The result in one page

**The coordinator's sketch is right: the `C₁√n` of Theorem 11.58a is not needed.**  Part A of the brief is complete
(propositions with complete proofs, explicit error terms, exact checks without a violation); so is the
coordinator's addition (the drop for any slope and for maxima of lines); so is Part B (the slope step at a general
outer rate, with its corollary for maxima of lines).  The optional part (extensive accuracies) is not done.

> **Theorems A, B [proved here, given Theorem 11.56 with the abort rule "before every query, every inner call
> counted with its certified bound" (paper proof, refereed R8), Lemma 11.55(c), (d) and Propositions Q1, Q2, Q5, Q6
> of `Q_REPORT.md` (paper proofs, refereed R12), and the epoch arithmetic of `RateFull.lean` (machine-checked)].**
> Fix `u > 0`; epoch sequences `d_m, J_m, k_m, B_m` as in Theorem 11.58a.
>
> (a) *Explicit, every `n`.*  For every `n ≥ 1`, `ε > 0`, `0 < δ < 1` and `M ≥ 0` there is an explicit nested design of
> levels of Algorithm 2L⁺ — per epoch `J_m` slope steps (Proposition Q6, unchanged), one drop `D′` run at the accuracy
> `𝒳 = ln(φ_m n + 1) + O(1)` with a polynomial closure threshold, and one chain of at most `n/m` levels whose outer
> blocks have `m = Θ(ln n)` sites and which brings the accuracy back to `1` (to `min(ε, 1)` at the top); the base family
> is used at the accuracy `2 ln(n+1) + O(1)`, under a chain — which returns a bracket of ratio at most `e^ε` with
> probability at least `1 − δ` and makes, in every run and at every member of `L_u(Q_n)`, at most
>
>     exp( n·B_M + 𝓔′_M(n, ε, δ) )        evaluations,
>
> where `𝓔′_M` is the explicit sum (A.1): one term per slope step, per drop and per chain, **none of the order `√n`**.
> If `(k_M − 1)·q_S(n, (M+3)Λ̄_0) ≤ Λ̄_0 = ln(1/δ) + n ln 2` (Proposition A′):
>
>     𝓔′_M  ≤  (k_M − 1 − M)·ℓ̄_S + M·ℓ̄_D + (M + 1)·ℓ̄_T + ℓ_𝔅,
>     ℓ̄_S = (9/2)·ln n + O(ln ln n),    ℓ̄_D = (a/h + 4)·ln n + O(ln ln n),    ℓ̄_T = O(ln n + ln(1/min(ε,1))),    ℓ_𝔅 = 2 ln n + O(ln ln n),
>
> all four explicit (`ℓ̄_T ≈ [8(ln 2/h − 1) + 5 + ln 2/(2u)]·ln n` in its crude closed form; `230`–`1 000` nats per chain in
> the designs evaluated at `u = 1`, `n = 10⁶ … 10^{12}`).
>
> (b) *The order.*  There are `n₀(u, δ)`, `C′(u, δ)` such that for all `n ≥ n₀` and all `0 < ε ≤ 1`
>
>     ln N(n; ε, δ)  ≤  n·h + 2·√( (1 + r̄)·c₁·n·ℓ̄_S ) + C′·( (ln n)² + ln(1/ε) ),
>
> hence `limsup_n (ln N(n; ε_n, δ) − n·h)/√(n ln n) ≤ C_*′(u) := 3·√(2(1 + r̄)c₁)` (`3.50, 6.56, 10.57` at `u = ½, 1, 2`; Theorem 11.58a
> has `C_* = 4.65, 8.64, 13.52`) for every fixed `ε` and for every sequence `ε_n` with `ln(1/ε_n) = o(√(n ln n))`.
>
> **Proposition Q6(e) (Part B) [proved here, same inputs].**  For a family of type `(B, σ, R; E)`, `0 ≤ σ ≤ 1`, and every
> outer rate `0 < e ≤ 2u`, the level with the outer block `n_o = ⌊(x̂ − 1 − c_log(n))/e⌋`, the threshold of accuracy
> exactly `x̂ = min(x, R′n)` and a unit ladder below `n_o·θ_na(e)` gives a family of type
> `(B, σ′ = [B − (1−σ)θ_na(e)]/e, R′ = R·e/(θ_na(e) + R); E + ℓ_S(n; e))`,
> `ℓ_S(n; e) = σ′₊·(1 + c_log(n) + e) + ℓ₀(n, Λ) ≤ (B/e + 4)·ln n + O(1)`, uniformly on compact subintervals of `(0, ε*]`; for a
> type that is a maximum of finitely many lines on a common range the same level maps every line `(B_i, σ_i)` to
> `(B_i, σ_i′)` with one loss `max_i σ′_{i,+}·(1 + c_log(n) + e) + ℓ₀` for all lines.

**How it is proved.**  One lemma (Lemma U, §2) evaluates the level "`λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, unit ladder below a
cap" for *any* outer block and outer rate: `ln C_max ≤ max_i[n_iB_i + (1−σ_i)·n_o·θ_na(e)] + ℓ₀ + E`, `ℓ₀ = 4 ln n + O(1)`.  The
slope step of Q (`e = h`), the drop `D′` (`e = 0`, `n_o = ⌊φn⌋`) and the slope step at a rate `e` are three choices of the
block.  The chain (Proposition T, §4) is a separate induction on the dimension: each level puts all outer points on
the coarse rung `𝒳` — at the cost `ϖ(m) − mB′ + O(ln n)` over `e^{dB′}`, once — and `e^{𝒳 + P_cnt}` of them on the next level of
the chain, which lives in dimension `d − m` and is cheaper by `e^{mB′}`; with `mB′ ≥ 𝒳 + P_cnt + ln 4` the chain costs
`A_T = max{ϖ(m) − mB′ + P_M + ln 4, e₀}` in all, whatever its length.

**The answers to the questions of the brief.**

| question | answer |
|---|---|
| Proposition D′ | §3: for an inner family of any slope `0 ≤ σ ≤ 1` on `(0, R]`, any outer fraction `φ ≤ R/(a+R)`, maxima of lines, any tolerance: accuracy exactly `𝒳 ≥ 1 + ln(c₃ + 1 + 3(φN+1)e^{2u+e^u})`; `ln(1/π†) ≤ n_o a + ln(n_o+1)`; new flat exponent `max_i[(1−φ)B_i + (1−σ_i)φa]` (`B·a/(a+R)` in the displayed case); error `c_D′ = B̃ + ℓ₀ ≈ 4 ln n` |
| Proposition T | §4: blocks `m` = the least with (4.1) (`m ≈ (𝒳 + P̄_cnt + ln 4)/B′`), uniform `c = α/(13⌈N/m⌉)`, base bracket below `d₀`; error `A_T + j(d)·Δ_T`, `Δ_T = 0` for the block of the design; `Λ` grows by less than `d·B′` over a chain |
| the theorem; closed form; limsup; all `n ≥ 2` | Theorem A with (A.1); Proposition A′; Theorem B (§5) |
| does `C_*` change? | not through the bounded levels; it drops to `C_*′ = C_*·√(4.5/(a/h+4))` because Lemma U gives the slope step of Q a smaller error term (Corollary U1) |
| which term is now second? | `O((ln n)²)`: `M + 1` chains, `M` drops, `M = O(ln n)` — in place of `C₁√n`; and the accuracy enters as `O(ln(1/ε))`, additively |
| the trap (drops without chains) | Proposition N (§5.4): admissible, `n·h + O(√n·ln n)`; better than Theorem A up to `n ≈ 1.3·10⁶` at `u = 1`, worse beyond |
| exact checks (i) | `D′`: 28 137 levels, least slack `2.3` nats; chain step: 56 360 levels, least slack `3.9` (§7.1); with tolerances: 47 154 levels, `2.5` (§7.6) |
| (ii) the chain exactly | 11 169 chains (1.58 million levels) by recursion: no violation, least slack `41.6` nats; a chain of 909 levels costs `127` nats at `N = 10⁶`, `u = 1`, `B′ = a` (bound `231`) (§7.2) |
| (iii) the formula | below the old bound at every scanned `n > 10⁵`; `0.358·na` at `10⁶` (old `0.371`), `0.2690` at `10⁸` (`0.2731`); `(bound − nh)/√(n ln n) = 1.29` at `10^{12}` (old `2.41`); the gain is `47 %` of `old − nh` from `10^{10}` on (§7.3) |
| (iv) the exact nest | `M ≤ 2`: 66 designs, `u ∈ {½, 1, 2}`, `n = 10³ … 6.4·10⁴`, "proof" and "min" variants: 1 567 187 node checks; and `M = 2` at `n = 16 000` ("proof"): 8 875 094 node checks; no violation, least slack of the induction `56` nats (§7.4) |
| Part B | Proposition Q6(e) and Corollary Q6(e)-max (§6); 297 330 levels at eight rates on both sides of `h`, `u ∈ {½, 1, 2}`: no violation, least slack `3.3` nats (§7.5) |

**What had to be changed in the sketch** (details in §9): the chain needs a uniform `c` (or the constants of its
deepest level) and the term `e₀` for its bottom; below `d₀` the base bracket, not enumeration, or the gain of
Lemma 11.55(c) on the blocks is lost; `D′` needs a fixed accuracy `𝒳` and families "up to a horizon"; and types whose
line is negative on its range are vacuous (they are the type of no family), which matters for tests.


---

## 1. What is quoted, and three conventions

### 1.1 Quoted statements

* **(T) Theorem 11.56 = Theorem K1 [quoted; paper proof, refereed R8, not machine-checked], with the constants of
  `K_REPORT.md` §2.2 as restated in Q §1.2, and with the abort rule in the form (P) of referee R12 (m2) and of the
  theory report:** a level counts each of its own queries as `1` and each call of an inner procedure with its
  certified bound `C_l`, and tests *before every query and before every inner call* that the count stays at most
  `C_max`.  Hypotheses, numbered for the checklists below:
  **(H1)** `n ≥ 2`, `1 ≤ n_o ≤ n−1` (`n_i = n − n_o`); **(H2)** `0 < λ ≤ 1`; **(H3)** `0 < η ≤ ½`; **(H4)** `0 < η′ ≤ 1`; **(H5)** `θ > 0`;
  **(H6)** `ν₁ ≥ 1`; **(H7)** tolerance `b > 0`; **(H8)** a ladder `x₀ := 2un_i > x₁ > … > x_L`, `L ≥ 1`, `x_L ≤ b`;
  **(H9)** for `1 ≤ l ≤ L` a bracket procedure `I_l` for dimension `n_i` of accuracy `x_l`, failure probability at most
  `δ′ = δ/(4LM̄)` and cost at most `C_l` in every run.  Conclusion: Algorithm 2L⁺ is a bracket procedure for dimension `n`
  with failure probability `δ`, accuracy `x_out = ln[(2p_u)^n + e^b(e^λ(1+η)/(1−η) + η′ + θ)]` and cost
  `C_max = 1 + 2M̄ + Σ_l min{2M̄, (J+1)cnt(x_{l−1})}·C_l` in every run; `C_max` is nondecreasing in every `C_l`.
* **(Q1) Proposition Q1 [quoted; Q, refereed R12].**  With `Λ_lev := ln 2M̄`, `P_M := ln(4(1+η)e^λ/(1−η)) + ln ν₀ + ln K`,
  `P_cnt := ln(J+1) + ln(2(1+η)²e^λ/(1−η)) + ln ν₀ + ln K` and `t_l := min{Λ_lev, x_{l−1} + P_cnt} + ln C_l`:
  `Λ_lev = P_M + ln(1/π†)`, `P_M ≤ P_cnt`, and `ln C_max ≤ ln(L+2) + max{Λ_lev, max_l t_l}`.
* **(Q2) Lemma Q2 [quoted; as (Q1)].**  `J ≤ (2un + b + n_o ln 2)/λ + 1`; `π† ≥ 2^{-n_o−1}`, hence
  `m_max ≤ log₂(2(1+η)e^λν₀/(1−η)) + n_o + 2`; `K ≤ 3(1+η)η^{-2}[ln(1/δ) + ln(2(J+1)(m_max+1)(L+2))] + 1`; and
  **(2.1)** `ln(1/δ′) + n_i ln 2 ≤ [ln(1/δ) + n ln 2] + ln(4L) + P_M`.
* **(Q3) Lemma Q3, refined form (= Lemma 11.55(c)) [quoted; as (Q1); in exact arithmetic by R12].**  Let `m ≥ 1`,
  `0 < η ≤ ½`, `0 < θ ≤ 2e^{u(m₀+2)}` (`m₀ = ⌈u^{-1}ln((1+η)/(1−η))⌉`), `ν₀ ≥ 2e^u m/(θ(1−η))`, `ℓ ≥ ln(2e^{u(m₀+2)}/θ)` and
  `√(mℓ/2) ≤ p_u m/2 − 1`, i.e. `m ≥ m*(ℓ) := ((√(ℓ/2) + √(ℓ/2 + 2p_u))/p_u)²`.  Then on `Q_m`:
  `ln(1/π†) ≤ m·a + u(1 + √(mℓ/2)) + (4/(3p_u))(ℓ + 2) + ln(m+1)`.
* **(Q4) Lemma Q4(b) (= Lemma 11.55(d)) [quoted; as (Q3)], with the hypothesis as corrected by R12 (m6):** let `m ≥ 1`,
  `t ≥ 0`, `η = ½`, `(1−η)ν₀ ≥ 1` and `θ ≥ 3(m+1)·e^{2u + e^u + m·t}`.  Then on `Q_m`: `r† ≥ min{m−1, ⌊ρ_t m⌋ + 1}` and
  `ln(1/π†) ≤ m·θ_na(t) + ln(m+1)`.
* **(Q5) Proposition Q5 [quoted; as (Q1)]: the base family `𝔊_0`** (two-sample bracket of Proposition 11.57(a), or
  enumeration; `b_{𝔊_0} = ln min(2M, 2^d)`).  (a) For all `d ≥ 1`, `x > 0`, `δ` and `Λ ≥ ln(1/δ)`:
  `b_{𝔊_0}(d, x, δ) ≤ min{d ln 2, d·a + E_base(d, x; Λ)}`.  (b) at `t = 0`: if `x ≥ c′_d := ln 12 + 2 ln(d+1) + 2u + e^u`, then
  `b_{𝔊_0}(d, x, δ) ≤ d·a + ln(8K) + ln(d+1)`, `K = ⌈18 ln(4/δ)⌉`.
* **(Q6), (Q7) Propositions Q6 (slope step), Q7 (drop) and the functions `A_n := (2u + ln 2)n + 3`,
  `c_log(n) := ln(n+1) + ln 6 + 2u + e^u`, `K̄_S`, `m̄_S`, `q_S`, `c_S`, `ν̄_D`, `m̄_D`, `K̄_D`, `P̄_cnt`, `P̄_M`, `ℓ_c`, `w(c)` of Q §4
  [quoted; as (Q1)].**
* **(R) the epoch arithmetic [quoted; machine-checked in `RateFull.lean`, as restated in Q §1.2]:** `d_0 = h/(a−h)`,
  `J_m = ⌈d_m⌉`, `d_{m+1} = d_m(J_m a + h)/(J_m a − h d_m)`, `k_0 = 1`, `k_{m+1} = k_m + J_m + 1`, `B_m = h(1 + 1/d_m)`,
  `R_m = h/J_m`, `φ_m = R_m/(a + R_m)`; `B_{m+1} = (1 − φ_m)B_m`, `B_m − h ≤ c₁/(k_m + c₂)`, `d_m ≤ J_m < d_m + 1`,
  `k_{m+1} < (1 + r̄)k_m`, `M ≤ 1 + ln(k_M + 1)/ln(1 + κ)`.

### 1.2 Three conventions

**(C1) A horizon.**  The designs below fix parameters (an accuracy `≈ ln N`, a block of `Θ(ln N)` sites) that depend on
the largest dimension `N` in which a family is used.  A *certified family up to `N`* with least accuracy `x_min` assigns
to every `1 ≤ d ≤ N`, `x ≥ x_min`, `0 < δ < 1` a bracket procedure for `L_u(Q_d)` of accuracy at most `x` and failure
probability at most `δ`, with a certified bound `exp(b_𝔉(d, x, δ))` on its evaluations in every run.  It has the type
`𝓗_N(B, σ, R; E)` if the inequality of Q's definition holds for all `1 ≤ d ≤ N`.  Every proof of Q §§2–5 uses a family
only in dimensions at most that of the level under construction, so Q5, Q6, Q7 hold verbatim for `𝓗_N` (with `n ≤ N`),
and a family of Q is a family up to every `N`.  In the final design `N` is the top dimension `n`.

**(C2) Certified bounds are at least one evaluation:** `b_𝔉 ≥ 0`.  (All bounds that occur are: `C_max ≥ 1 + 2M̄`,
`min(2M, 2^d) ≥ 1`; in general replace `b` by `max(b, 0)`.)  Consequently a type whose majorant
`d·B − σ·min(x, R·d) + E` is negative somewhere is the type of no family — the saturating families of §7 are
`max(0, majorant)`, and the tests use only lines that are nonnegative on their range (`B ≥ σR`).  (C2) is used in
the proofs below in one place: to bound the outer sample by the terms of the rungs.

**(C3) Maxima of lines.**  For a finite set `𝔏 = {(B_i, σ_i)}_{i∈I}` with `B_i > 0`, `0 ≤ σ_i ≤ 1`, a range `R ∈ (0, ∞]`
(all `σ_i = 0` if `R = ∞`) and an error function `E(d, x; Λ) ≥ 0`, nondecreasing in `d` and `Λ` and nonincreasing in `x`,
a family up to `N` has the type `𝓗_N(𝔏, R; E)` if for all `1 ≤ d ≤ N`, `x ≥ x_min`, `δ` and `Λ ≥ ln(1/δ) + d ln 2`

    b_𝔉(d, x, δ)  ≤  max_{i∈I} [ d·B_i − σ_i·min(x, R·d) ] + E(d, x; Λ).

One line is Q's `𝓗(B, σ, R; E)`.  Since `C_max` is nondecreasing in the inner costs and `max` commutes with adding the
multiplier of a rung, every bound below is proved for one line and holds for the maximum, line by line.

---

## 2. Lemma U: the level with `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, in one statement

The slope step of Q, the new drop `D′` and the slope step at a general outer rate are the same level with
different outer blocks.  The following lemma is the finite-`n` form of the exponent-level line
"`γ + (1−φ)T(γ/(1−φ)) ≤ (1−φ)B + (1−σ)φθ_na(e)` for `γ ≤ φθ_na(e)`" (`StepLE.of_limit`), with an explicit error.

For a tolerance `b ≥ 1` put

    A_n^b := (2u + ln 2)·n + 2 + b,      m̄^b(n) := n + 2 + log₂(c₁₂·A_n^b),      K̄^b(n, Λ) := 18·[Λ + ln(2·A_n^b·m̄^b(n)·(n+3))] + 1,
    q^b(n, Λ) := ln(4(n+1)) + ln A_n^b + c₂₄ + ln K̄^b(n, Λ),
    ℓ₀^b(n, Λ) := 1 + 2 ln A_n^b + c₁₈ + ln K̄^b(n, Λ) + ln(n+3).

At `b = 1` these are `A_n`, `m̄_S`, `K̄_S`, `q_S` of Q, and `ℓ₀ := ℓ₀¹ = c_S(n, Λ; B) − (1 + c_log(n) + h)·B/h`: the part of Q's
slope-step error that does not come from the dimension.  For fixed `u` and `b = O(n)`:
`ℓ₀^b(n, Λ) = 3 ln n + ln(Λ + ln n) + O(1)`, i.e. `4 ln n + O(1)` for `Λ = O(n)`.

**Lemma U [proved here from (T), (Q1), (Q2), (Q4), (C2)].**  Let `N ≥ n ≥ 2`, and let `𝔉` be a certified family up to
`N` of type `𝓗_N(𝔏, R; E)`, `𝔏 = {(B_i, σ_i)}` (`0 ≤ σ_i ≤ 1`), with least accuracy `x_min`.  Let

* a tolerance `b ≥ max(1, x_min)`;
* an outer block `1 ≤ n_o ≤ n − 1` with `2u·n_i > b` (`n_i = n − n_o`);
* a rate `e ≥ 0`, `ϑ := θ_na(e)`, and a threshold `θ ≥ 3(n_o + 1)·e^{2u + e^u + n_o·e}`;
* a cap `Ξ` with `n_o·ϑ ≤ Ξ ≤ n`, and `Ξ ≤ R·n_i` if `R < ∞`.

The **level** `𝖫` is Algorithm 2L⁺ in dimension `n` with this `n_o`, `θ` and `b`, with `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`,
the ladder

    x₀ = 2un_i  >  x₁ := b + k₁  >  b + k₁ − 1  >  …  >  b + 1  >  b = x_L,        k₁ := min{ max(⌈Ξ − b⌉, 0) ,  ⌈2un_i − b⌉ − 1 },   L = k₁ + 1

(for `b = 1`: `x₁ = min{max(⌈Ξ⌉, 1), ⌈2un_i⌉ − 1}` and the rungs are `x₁, x₁ − 1, …, 1`), and `I_l := 𝔉(n_i, x_l, δ′)`.  Then

(a) `𝖫` is admissible for (T); its accuracy is `ln[(2p_u)^n + e^b(c₃ + θ)]`.

(b) `J + 1 ≤ A_n^b`, `ν₀ = 2(exp(1) − 1)(J+1)`, `P_cnt = 2 ln(J+1) + c₁₈ + ln K`, `P_M = ln(J+1) + c₂₄ + ln K`,
`m_max + 1 ≤ m̄^b(n)`, `L + 2 ≤ n + 3`, `K ≤ K̄^b(n, ln(1/δ))`, `P_M + ln(n_o + 1) ≤ 1 + P_cnt`, and for every
`Λ ≥ ln(1/δ) + n ln 2`:   `ln(1/δ′) + n_i ln 2 ≤ Λ + q^b(n, Λ)`.

(c) `ln(1/π†) ≤ n_o·ϑ + ln(n_o + 1)`; hence `G := (Λ_lev − 1 − P_cnt)₊ ≤ n_o·ϑ`.

(d) For every `Λ ≥ ln(1/δ) + n ln 2`:

    ln C_max  ≤  max_i [ n_i·B_i + (1 − σ_i)·n_o·ϑ ]  +  ℓ₀^b(n, Λ)  +  E(n, b; Λ + q^b(n, Λ)).                              (U)

*Checklist of the hypotheses of (T).*  (H1) is assumed.  (H2)–(H4), (H6): `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`.
(H5): `θ ≥ 3(n_o+1)e^{2u+e^u} > 0`.  (H7): `b ≥ 1`.  (H8): `2un_i > b` gives `⌈2un_i − b⌉ − 1 ≥ 0`, so `k₁ ≥ 0` and `L ≥ 1`;
`k₁ ≤ ⌈2un_i − b⌉ − 1 < 2un_i − b`, so `x₁ < x₀`; the rungs decrease by one and end at `x_L = b`.  (H9): `1 ≤ n_i ≤ N`, and
`x_l ≥ b ≥ x_min`, so `𝔉(n_i, x_l, δ′)` is defined, has accuracy at most `x_l`, failure probability at most `δ′`, and
makes at most `C_l := exp(b_𝔉(n_i, x_l, δ′))` evaluations in every run.  The accuracy in (a) is the formula of (T) with
`e^λ(1+η)/(1−η) + η′ = c₃`.

*Proof.*  (b) `J = ⌈2un + b + n_o ln 2⌉ ≤ 2un + b + n_o ln 2 + 1`, and `n_o ≤ n`.  `ν₀ = 2·max{(J+1)(exp(1)−1), 1}`.  The two
formulas are the definitions of `P_cnt`, `P_M` at `λ = 1`, `η = ½` (`2(1+η)²e^λ/(1−η) = 9exp(1)`, `4(1+η)e^λ/(1−η) = 12exp(1)`).
By (Q2), `m_max + 1 ≤ log₂(6exp(1)·ν₀) + n_o + 3 ≤ m̄^b(n)` because `n_o ≤ n − 1`.  `L = k₁ + 1 ≤ max(⌈Ξ − b⌉, 0) + 1 ≤ ⌈Ξ⌉ ≤ n`
(as `b ≥ 1`, `Ξ ≥ 0`; if `Ξ ≤ b` then `L = 1`).  `K ≤ 18[ln(1/δ) + ln(2(J+1)(m_max+1)(L+2))] + 1` by (Q2).
`P_cnt − P_M = ln(J+1) + ln(3/4)` and `J + 1 ≥ n_o ln 2 + 2`, so `(3exp(1)/4)(J+1) ≥ 1.41·n_o + 4 ≥ n_o + 1`.  The last
inequality is (2.1) with `ln(4L) ≤ ln(4(n+1))`, `P_M ≤ ln A_n^b + c₂₄ + ln K̄^b(n, Λ)` (`K̄^b` is increasing in `Λ ≥ ln(1/δ)`).
(c) (Q4) with `m = n_o`, `t = e`: its hypotheses are `η = ½`, `(1−η)ν₀ = (exp(1)−1)(J+1) ≥ 1` and the threshold.  Then
`Λ_lev − 1 − P_cnt = P_M + ln(1/π†) − 1 − P_cnt ≤ n_o ϑ` by (b).
(d) Fix `Λ`, put `Λ′ := Λ + q^b(n, Λ)` and `E₁ := E(n, b; Λ′)`.  By (b), `Λ′ ≥ ln(1/δ′) + n_i ln 2`, so the type of `𝔉`
applies to every inner call: `ln C_l ≤ max_i[n_iB_i − σ_i·min(x_l, Rn_i)] + E(n_i, x_l; Λ′)`, and `E(n_i, x_l; Λ′) ≤ E₁`
(`n_i ≤ n`, `x_l ≥ b`).  Fix a line `(B, σ)` of `𝔏` and put `V := n_iB + (1−σ)G + 1 + P_cnt + E₁`.  We show
`min{Λ_lev, x_{l−1} + P_cnt} + n_iB − σ·min(x_l, Rn_i) + E₁ ≤ V` for every rung; taking the maximum over the lines then
gives `t_l ≤ max_i V_i`.

*An auxiliary inequality.*  For every `y ≥ 0`:  `f(y) := min{Λ_lev, y + 1 + P_cnt} − σy ≤ (1−σ)G + 1 + P_cnt`.
(If `y ≤ Λ_lev − 1 − P_cnt`, then `G ≥ y` and `f(y) = (1−σ)y + 1 + P_cnt`.  If `y > Λ_lev − 1 − P_cnt ≥ 0`, then
`f(y) = Λ_lev − σy < Λ_lev − σG = (1−σ)G + 1 + P_cnt`.  If `Λ_lev − 1 − P_cnt < 0`, then `G = 0` and `f(y) ≤ Λ_lev < 1 + P_cnt`.
Here `0 ≤ σ ≤ 1` is used.)

*Rungs with `x_{l−1} ≤ x_l + 1` and `x_l ≤ R·n_i`.*  The left-hand side is at most `f(x_l) + n_iB + E₁ ≤ V`.  These are:
all rungs `l ≥ 2` (the step is one; and `x_l ≤ x₁ − 1 = b + k₁ − 1` with `k₁ ≥ 1`, hence `k₁ ≤ ⌈Ξ − b⌉` and
`x_l < Ξ ≤ Rn_i`); and the rung `l = 1` when the cap `⌈2un_i − b⌉ − 1` is active, i.e. `k₁ = ⌈2un_i − b⌉ − 1 < max(⌈Ξ − b⌉, 0)`
(then `x₀ = 2un_i ≤ x₁ + 1`, and `x₁ ≤ b + ⌈Ξ − b⌉ − 1 < Ξ ≤ Rn_i`).

*The rung `l = 1` otherwise:* `x₁ = b + max(⌈Ξ − b⌉, 0) ≥ max(Ξ, b) ≥ G` by (c), and `Rn_i ≥ Ξ ≥ G`; so
`min(x₁, Rn_i) ≥ G`, and with the multiplier `Λ_lev ≤ G + 1 + P_cnt` the left-hand side is at most
`G + 1 + P_cnt − σG + n_iB + E₁ = V`.

*The outer sample.*  `Λ_lev ≤ G + 1 + P_cnt`, and we need a line with `σ_iG ≤ n_iB_i + E₁`.  Let `y* := max(G, b) ≥ x_min`.
By (C2) and the type of `𝔉` at `(n_i, y*, δ′)`: `0 ≤ max_i[n_iB_i − σ_i·min(y*, Rn_i)] + E(n_i, y*; Λ′)`, so some line
has `σ_i·min(y*, Rn_i) ≤ n_iB_i + E₁`; and `G ≤ min(y*, Rn_i)` because `G ≤ n_oϑ ≤ Ξ ≤ Rn_i`.  For that line
`Λ_lev ≤ V_i`.

So by (Q1), `ln C_max ≤ ln(L+2) + max_i V_i`; with `G ≤ n_oϑ`, `L + 2 ≤ n + 3` and
`1 + P_cnt ≤ 1 + 2 ln A_n^b + c₁₈ + ln K̄^b(n, Λ)` this is (U).  (If `R = ∞`, all `σ_i = 0`, the conditions on `Rn_i` are void
and the argument is the same.)  ∎

*Reading.*  The outer sample costs `e^{n_oϑ}` up to `n_o + 1`; rungs finer than `G ≈ n_oϑ` are needed by `e^{x_l + 1 + P_cnt}`
points only and cost `(1−σ)x_l` more than `n_iB`; rungs coarser than `G` are needed by all `2M̄` points and their term
*decreases* with slope `σ`.  The maximum sits at the rung `≈ n_oϑ` — the "dominant rung" — and equals
`n_iB + (1−σ)n_oϑ` up to `ℓ₀^b`.  Nothing else about the level enters.

**Corollary U1 (the slope step of Q with a smaller error term) [proved here].**  The level as built of Proposition
Q6 is the level of Lemma U with `b = 1`, `e = h` (`ϑ = h`), `n_o = ⌊(x̂ − 1 − c_log(n))/h⌋`, `θ = e^{x̂−1} − c₃ − (2p_u)^n e^{-1}`
and the cap `Ξ = x̂` (`n_oh ≤ x̂ ≤ R·n_i` by step (4) of its proof; `θ ≥ e^{x̂−1}/2 ≥ 3(n_o+1)e^{2u+e^u+n_oh}` by its steps
(1), (2)).  Hence Proposition Q6 holds with

    c_S′(n, Λ; σ′) := σ′·(1 + c_log(n) + h) + ℓ₀(n, Λ),        σ′ = σ + B/h − 1,

in place of `c_S(n, Λ; B) = (B/h)(1 + c_log(n) + h) + ℓ₀(n, Λ)`: the error is smaller by `(1 − σ)(1 + c_log(n) + h)`.
(*Proof.*  (U) gives `ln C_max ≤ n_iB + (1−σ)n_oh + ℓ₀ + E₁ = nB − σ′·n_oh + ℓ₀ + E₁`, and `n_oh ≥ x̂ − 1 − c_log(n) − h`.
The pass-through, `x̂ < X₀(n)`: `b_𝔉 ≤ nB − σ·min(x, Rn) + E ≤ nB − σ′x̂ + (σ′ − σ)x̂ + E` and `(σ′−σ)x̂ ≤ σ′X₀(n)`.  ∎)
Q's proof charges every rung between `n_oh` and `x̂` with the count `e^{x_l + P_cnt}`; these rungs are in fact capped
by the sample.  In the epoch schedule `σ′ = j/d_m` at the `j`-th step of epoch `m`, so the steps of an epoch lose
`ℓ₀ + (1 + c_log + h)·(J_m + 1)/(2d_m)` on average — `(9/2)·ln n` for the late epochs instead of `5·ln n`, and instead of
the `(a/h + 4)·ln n` that Theorem Q9 charges every step.  This lowers the constant of the limsup (Theorem B).
Tested on the levels of Q6 themselves in §7.5, part C.

---

## 3. Proposition D′: the drop at a logarithmic accuracy

Let `N ≥ 1`; let `𝔉` be a certified family up to `N` of type `𝓗_N(𝔏, R; E)`, `𝔏 = {(B_i, σ_i)}` with `0 ≤ σ_i ≤ 1`, with a
range `0 < R ≤ 1` and least accuracy `x_min`.  Let

    a tolerance  b ≥ max(1, x_min)   (b = 1 in the schedule of §5),        an outer fraction  0 < φ ≤ R/(a + R),
    an accuracy  𝒳 ≥ 𝒳_D^b(N; φ) := b + ln( c₃ + 1 + 3(φN + 1)·e^{2u + e^u} )        (= b + ln(φN + 1) + ln 3 + 2u + e^u + o(1)).

The family `D′[𝔉; φ, 𝒳]` (up to `N`) has least accuracy `𝒳` and is accuracy-blind: for every `x ≥ 𝒳` it delivers `𝒳`.
The **level as built** at `(n, δ)`, `n ≤ N`, is defined if `n_o := ⌊φn⌋ ≥ 1` and `2u(n − n_o) > b`; it is the level of
Lemma U with this `n_o`, the rate `e = 0` (`ϑ = a`), the cap `Ξ = R·n_i` and the threshold

    θ = e^{𝒳−b} − c₃ − (2p_u)^n·e^{−b}

— Algorithm 2L⁺ with `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, tolerance `b` and a ladder of step one from `≈ ⌈R·n_i⌉` down to `b`
(for `b = 1`: `2un_i > min{⌈Rn_i⌉, ⌈2un_i⌉ − 1} > … > 2 > 1`), served by `𝔉`.  `D′[𝔉; φ, 𝒳](n, x, δ)` is the cheaper of this
level (if defined) and of `𝔉(n, 𝒳, δ)` (pass-through).

**Proposition D′ [proved here from Lemma U].**  (i) The level as built is admissible for (T) and has accuracy
exactly `𝒳`; on its outer block `ln(1/π†) ≤ n_o·a + ln(n_o + 1)` — **no `√`** — and
`ln(1/δ′) + n_i ln 2 ≤ Λ + q^b(n, Λ)` for `Λ ≥ ln(1/δ) + n ln 2`.
(ii) `D′[𝔉; φ, 𝒳]` has the type `𝓗_N(B′, 0, ∞; E′)` with

    B′ := max_i [ (1 − φ)·B_i + (1 − σ_i)·φ·a ],
    E′(n, x; Λ) := E(n, b; Λ + q^b(n, Λ)) + c_D′(n, Λ),        c_D′(n, Λ) := B̃ + ℓ₀^b(n, Λ),
    B̃ := max{1, bφ/(2u(1−φ))} · max_i (B_i − (1 − σ_i)·a)₊ .

*The displayed case* (one line of slope one, `φ = R/(a + R)`, `b = 1`; the drop of the epoch schedule):
`B′ = B·a/(a + R)`, `B̃ = max{1, R/(2ua)}·B`, `c_D′ = B̃ + ℓ₀(n, Λ) = 3 ln n + ln(Λ + ln n) + O(1)`.
*One line of slope `σ`, `φ = R/(a + R)`:* `B′ = [a/(a + R)]·(B + (1 − σ)R)` — the exponent `(1−φ)(B + (1−σ)X)` at
`X = φa/(1−φ) = R` of the coordinator's addition.

*Checklist of (T).*  That of Lemma U, whose hypotheses hold: `n_o ≥ 1` and `n_o ≤ φn < n`, so `n ≥ 2` and `n_o ≤ n − 1` (H1);
`2un_i > b` by definition; the threshold: `(2p_u)^n e^{−b} ≤ 1`, so
`θ ≥ e^{𝒳−b} − (c₃ + 1) ≥ 3(φN + 1)e^{2u+e^u} ≥ 3(n_o + 1)e^{2u+e^u}` — the hypothesis of (Q4) at the rate `0` (H5); the cap:
`n_o·a ≤ φna ≤ R(1−φ)n ≤ R·n_i` because `φ ≤ R/(a + R)`, and `Ξ = Rn_i ≤ n` because `R ≤ 1`; inner calls at accuracies
`≥ b ≥ x_min` in the dimension `n_i ≤ N` (H9).

*Proof.*  (i) Lemma U(a)–(c); the accuracy is `ln[(2p_u)^n + e^b(c₃ + θ)] = 𝒳`.  (ii) *The level.*  By (U),
`ln C_max ≤ max_i[n_iB_i + (1−σ_i)n_o a] + ℓ₀^b(n, Λ) + E(n, b; Λ + q^b)`.  With `τ := φn − n_o ∈ [0, 1)`:
`n_iB_i + (1−σ_i)n_o a = n[(1−φ)B_i + (1−σ_i)φa] + τ[B_i − (1−σ_i)a] ≤ nB′ + (B_i − (1−σ_i)a)₊`.
*The pass-through* (`𝒳 ≥ b ≥ x_min`): `b_𝔉(n, 𝒳, δ) ≤ max_i[nB_i − σ_i·min(𝒳, Rn)] + E(n, 𝒳; Λ) ≤ max_i nB_i + E(n, b; Λ + q^b)`,
and `nB_i = n[(1−φ)B_i + (1−σ_i)φa] + nφ[B_i − (1−σ_i)a]`.  The proof needs it only where the level is not defined:
`n < 1/φ`, or `2u(n − n_o) ≤ b`, which with `n − n_o ≥ (1−φ)n` gives `n ≤ b/(2u(1−φ))`; in both cases
`nφ ≤ max{1, bφ/(2u(1−φ))}`.  The cheaper of two procedures obeys the bound of either; `E′` is nonnegative,
nondecreasing in `n` and `Λ` and constant in `x`.  ∎

*What the drop does, and why there is no `√`.*  As in Q7 the outer fraction is the one at which the outer
sample `e^{φna}` reaches the end `R·n_i` of the range of the inner line, so that the dominant rung has the exponent
`n_iB + (1−σ)n_o a`.  Q's drop asks its outer block for a *bounded* accuracy (`θ = c`); then the closure test stops
at `p_u n_o − Θ(√n_o)` and the block costs `e^{n_o a + Θ(√n_o)}` (Lemma Q3).  Here the block is asked for the accuracy
`𝒳 ≈ ln n`: with `θ ≥ 3(n_o+1)e^{2u+e^u}` the test passes at every radius up to `⌊p_u n_o⌋ + 1` through its one-sided
entry `Γ̃(r)/c_η ≤ θ` (Lemma 11.55(a), (d)), and the block costs `e^{n_o a}` up to the factor `n_o + 1`.  (In fact less: on
exact tables the radius is far above `p_u n_o` and `ln(1/π†) − n_o a` is `−959` at `n = 10⁶`, `u = 1`, `φ = φ_0` — the
polynomial threshold buys a *negative* `√`-term, which the proposition does not use; §7.1.)  The price is the accuracy:
the family delivers `𝒳`, not a bounded accuracy.  §4 repairs that.

*Remarks.*  (1) Nothing but the range condition `φ ≤ R/(a + R)` restricts `φ`; for a maximum of lines the drop is
applied with one `φ` and one ladder to all lines — its parameters do not depend on `𝔏` — and the new exponent is
the maximum of the images `(1−φ)B_i + (1−σ_i)φa`.  A line with `B_i ≤ (1−σ_i)a` is not lowered by any drop
(`B_i′ ≥ B_i`).  (2) The hypothesis `R ≤ 1` is used only for `L ≤ n` in the constants; for `R > 1` read `A_n^b` for `n + 3`
in `K̄^b`, `ℓ₀^b` (the cap `⌈2un_i − b⌉ − 1` gives `L + 2 ≤ A_n^b`).  (3) The threshold can be lowered: by Lemma 11.55(a),
`θ ≥ 6e^u n_o` already gives `r† ≥ ⌊p_u(n_o + 1)⌋` and `ln(1/π†) ≤ n_o a + u + e^u/n_o + ln(n_o+1)`, which would lower `𝒳` by
`u + e^u − ln 2` **[not used; a sketch: the ball below `p_u n_o` is compared by (F1) and the `χ²`-bound of Lemma Q4's
proof]**.

---

## 4. Proposition T: back to a bounded accuracy by a chain of levels with outer blocks of `Θ(ln N)` sites

### 4.1 The design

Let `𝔊′` be a certified family up to `N` of flat type `𝓗_N(B′, 0, ∞; E)`, `0 < B′ ≤ ln 2`, with least accuracy `𝒳 > 1`
(in the schedule: `D′[·]` with `𝒳 = 𝒳_D`, or the base family at the accuracies `≥ 𝒳_B`; for a maximum of lines `B′` is the
maximum after the drop, so nothing changes).  Let `0 < α ≤ 1` be the accuracy wanted and `m ≥ 1` a block.  Put

    N_T := ⌈N/m⌉,     c := α/(13·N_T)   (≤ 1/13),     w := w(c) = ln(e^c(1+c)/(1−c) + 2c) + c  ≤ 6.25c,     α̲ := α − N_T·w  ≥ 0.519·α,
    d₀ := max{ m + ⌊𝒳/(2u)⌋ + 1 ,  ⌈ln(6/(5c))/ln((1+e^u)/2)⌉ },
    j(d) := 0  (d < d₀),      j(d) := ⌊(d − d₀)/m⌋ + 1  (d₀ ≤ d ≤ N),          a_d := α̲ + j(d)·w,      b_d := a_d − w.

`j(d)` is the number of levels of the chain that starts in dimension `d`: `j(d) = j(d − m) + 1` for `d ≥ d₀`, and
`j(d) ≤ (N − d₀ + m)/m < N_T`, so `α̲ ≤ b_d < a_d ≤ α`.  The procedure `𝒯(d, δ)`, `1 ≤ d ≤ N`:

* `d < d₀`: the base family `𝔊_0(d, α̲, δ)` of Q §3 (two-sample bracket or enumeration, whichever has the smaller
  certified bound);
* `d ≥ d₀`: Algorithm 2L⁺ in dimension `d` with

      n_o = m,   n_i = d − m,   λ = η = η′ = θ = c,   ν₁ = 2e^u m/c,   tolerance b_d,
      ladder  x₀ = 2u(d − m)  >  x₁ = 𝒳  >  x₂ = b_d      (L = 2),
      I_1 = 𝔊′(d − m, 𝒳, δ′),        I_2 = 𝒯(d − m, δ′).

The family `𝒯[𝔊′; α, m]` has least accuracy `α` and is accuracy-blind: `𝒯[𝔊′; α, m](d, x, δ) := 𝒯(d, δ)` for `x ≥ α`.
A level of the chain is Q's drop (Proposition Q7) with a *short* outer block and a two-rung ladder; the difference
is in who serves the fine rung: the next level of the same chain, in the dimension `d − m`.

*Checklist of (T) for the level in dimension `d ≥ d₀`.*  (H1) `d ≥ d₀ ≥ m + 1 ≥ 2`, `1 ≤ m ≤ d − 1`.  (H2)–(H4)
`0 < c ≤ 1/13`.  (H5) `θ = c > 0`.  (H6) `ν₁ = 2e^u m/c ≥ 1`.  (H7) `b_d ≥ α̲ > 0`.  (H8) `2u(d − m) > 𝒳` because
`d − m ≥ ⌊𝒳/(2u)⌋ + 1`; `𝒳 > 1 ≥ α > b_d`; `x_L = b_d = b`.  (H9) `I_1`: `1 ≤ d − m ≤ N` and `𝒳` is an accuracy of `𝔊′`;
`I_2`: for `d − m ≥ d₀` the level in dimension `d − m`, of accuracy at most `a_{d−m} = b_d` by (i) below (induction on `d`);
for `d − m < d₀` the base procedure of accuracy `α̲ ≤ b_d`.  Both have failure probability at most `δ′` and a certified
cost in every run.

### 4.2 The statement

With the functions of Q7 (`P̄_cnt(d, Λ; c) = ln(A_d/c) + ln 7.45 + ln ν̄_D + ln K̄_D`, `P̄_M(d, Λ; c) = ln 11.17 + ln ν̄_D + ln K̄_D`,
`ℓ_c = ln 2 + 3u + 2.25c + ln(1/c)`) put

    ϖ(m; c) := min{ (m+1)·ln 2 ,  ϖ₃ },     ϖ₃ := m·a + u(1 + √(mℓ_c/2)) + (4/(3p_u))(ℓ_c + 2) + ln(m+1)  if m ≥ m*(ℓ_c),   ϖ₃ := ∞ otherwise,
    q_T(d, Λ) := ln 8 + P̄_M(d, Λ; c),          F_d(Λ) := Λ + q_T(d, Λ),          Λ*(d, Λ) := F_d^{j(d)}(Λ)   (the j(d)-fold iterate),
    a_T(d, Λ) := ϖ(m; c) − m·B′ + P̄_M(d, Λ; c) + ln 4,
    e₀(Λ)     := min{ (d₀ − 1)(ln 2 − B′) ,  (d₀ − 1)(a − B′)₊ + E_base(d₀ − 1, α̲; Λ) },
    A_T(d, Λ) := max{ a_T(d, Λ), e₀(Λ) },          Δ_T(d, Λ) := [ 𝒳 + P̄_cnt(d, Λ; c) + ln 4 − m·B′ ]₊ .

**Proposition T [proved here from (T), (Q1), (Q2), (Q3), (Q5a), (C2)].**
(i) Every level of the chain is admissible for (T), and `𝒯(d, δ)` has accuracy at most `a_d ≤ α` (`α̲` for `d < d₀`).
(ii) For the level in dimension `d ≥ d₀` with failure probability `δ`, and every `Λ ≥ ln(1/δ) + d ln 2`:
`ln(1/π†) ≤ ϖ(m; c)`, `P_cnt ≤ P̄_cnt(d, Λ; c)`, `P_M ≤ P̄_M(d, Λ; c)`, and `ln(1/δ′) + (d − m) ln 2 ≤ Λ + q_T(d, Λ)`.
(iii) `𝒯[𝔊′; α, m]` has the type `𝓗_N(B′, 0, ∞; E_T)` with

    E_T(d, x; Λ) := E(d, 𝒳; Λ*) + A_T(d, Λ*) + j(d)·Δ_T(d, Λ*),        Λ* = Λ*(d, Λ),

which is nonnegative, nondecreasing in `d` and `Λ` and constant in `x`.
(iv) If `m·B′ ≥ 𝒳 + P̄_cnt(d, Λ + dB′; c) + ln 4`, then `Δ_T(d, Λ*(d, Λ)) = 0` and
`Λ*(d, Λ) ≤ Λ + j(d)·q_T(d, Λ + dB′) < Λ + d·B′`.

So if the block is long enough for (iv), **a chain of any length costs `A_T` in all**:

    b_𝒯(d, x, δ)  ≤  d·B′ + E(d, 𝒳; Λ*) + max{ ϖ(m; c) − m·B′ + P̄_M + ln 4 ,  e₀ }.

With the trivial `ϖ = (m+1) ln 2` this is the `A = n_o(ln 2 − B′) + P_M + ln 8` of the brief.

*Proof.*  (i) By the checklist, (T) applies; the accuracy of the level is
`ln[(2p_u)^d + e^{b_d}(e^c(1+c)/(1−c) + 2c)] = ln[(2p_u)^d + e^{a_d − c}]`, and `(2p_u)^d ≤ 5c/6 ≤ 1 − e^{-c} ≤ e^{a_d}(1 − e^{-c})`
because `d ≥ d₀ ≥ ln(6/(5c))/ln((1+e^u)/2)` and `a_d > 0` (the computation of Q7(1)).
(ii) The outer block: `π† ≥ 2^{-m-1}` (Q2); and (Q3) applies with `η = θ = c ≤ 2`, `ν₀ ≥ ν₁/(1−η) = 2e^u m/(θ(1−η))` and
`ℓ = ℓ_c ≥ ln(2e^{u(m₀+2)}/c)` (Q7(2)) whenever `m ≥ m*(ℓ_c)`.  The constants: as in Q7(3), with `n = d`, `n_o = m ≤ d`,
`β = b_d ≤ 1` and `L + 2 = 4 ≤ d + 4`:  `J + 1 ≤ A_d/c`, `ν₀ ≤ ν̄_D`, `m_max + 1 ≤ m̄_D`, `K ≤ K̄_D(d, ln(1/δ); c)`.  The last
inequality is (2.1) with `ln(4L) = ln 8`.
(iii) Write `t(d, δ) := b_𝒯(d, ·, δ)` and

    U(d, Λ) := max{ E(d, 𝒳; Λ*) + a_T(d, Λ*) ,  e₀(Λ*) } + j(d)·Δ_T(d, Λ*),        Λ* = Λ*(d, Λ);

`U ≤ E_T` because `E ≥ 0`.  *Monotonicity.*  `q_T`, `a_T`, `e₀`, `Δ_T`, `E` are nondecreasing in `d` and `Λ` (`P̄_cnt`, `P̄_M`,
`E_base` are), `F_d` is increasing in `Λ` and nondecreasing in `d`, and `j(d)` is nondecreasing; so `Λ*(d, Λ)` and `U(d, Λ)`
are nondecreasing in `d` and in `Λ`, and `Λ*(d, Λ) ≥ Λ`.  Moreover, for `d ≥ d₀` and `Λ₁ := F_d(Λ)`:
`Λ*(d − m, Λ₁) = F_{d−m}^{j(d)−1}(F_d(Λ)) ≤ F_d^{j(d)}(Λ) = Λ*(d, Λ)`.
*Claim:* `t(d, δ) ≤ d·B′ + U(d, Λ)` for all `1 ≤ d ≤ N`, `δ`, `Λ ≥ ln(1/δ) + d ln 2`.  Induction on `d`.
For `d < d₀`: `j(d) = 0`, `Λ* = Λ ≥ ln(1/δ)`, and by (Q5a)
`t(d, δ) ≤ min{d ln 2, d·a + E_base(d, α̲; Λ)} ≤ d·B′ + e₀(Λ)` (`d ≤ d₀ − 1`; `E_base` is nondecreasing in `d`).
For `d ≥ d₀`: let `Λ₁ := Λ + q_T(d, Λ)`; by (ii), `Λ₁ ≥ ln(1/δ′) + (d − m) ln 2`.  By (Q1) with `L = 2`, and `ln C_1 ≥ 0` (C2),

    t(d, δ) ≤ ln 4 + max{ Λ_lev + ln C_1 ,  𝒳 + P_cnt + ln C_2 }

(the outer sample `Λ_lev ≤ Λ_lev + ln C_1`; the first rung has the multiplier `min{Λ_lev, x₀ + P_cnt} ≤ Λ_lev`, the second
`min{Λ_lev, 𝒳 + P_cnt} ≤ 𝒳 + P_cnt`).  *First term:* `Λ_lev = P_M + ln(1/π†) ≤ P̄_M(d, Λ; c) + ϖ(m; c)` and
`ln C_1 ≤ (d − m)B′ + E(d − m, 𝒳; Λ₁)`, so

    ln 4 + Λ_lev + ln C_1 ≤ d·B′ + E(d, 𝒳; Λ*) + [ϖ(m; c) − mB′ + P̄_M(d, Λ*; c) + ln 4] = d·B′ + E(d, 𝒳; Λ*) + a_T(d, Λ*).

*Second term:* by the induction hypothesis at `(d − m, δ′, Λ₁)` and the monotonicity,

    ln 4 + 𝒳 + P_cnt + ln C_2 ≤ d·B′ + [𝒳 + P̄_cnt(d, Λ; c) + ln 4 − mB′] + U(d − m, Λ₁)
                               ≤ d·B′ + Δ_T(d, Λ*) + max{E(d, 𝒳; Λ*) + a_T(d, Λ*), e₀(Λ*)} + (j(d) − 1)·Δ_T(d, Λ*) = d·B′ + U(d, Λ).

(iv) `q_T(d, Λ̂) = ln 8 + P̄_M < 𝒳 + P̄_cnt + ln 4` for every `Λ̂`, because
`P̄_cnt − P̄_M = ln(A_d/c) + ln(7.45/11.17) ≥ ln 39 − 0.41` and `𝒳 > 1`.  With `Λ̂ := Λ + dB′` the hypothesis gives
`q_T(d, Λ̂) < mB′`; and `j(d)·m ≤ d − d₀ + m < d`.  By induction on `i ≤ j(d)`, `F_d^{i}(Λ) ≤ Λ + i·q_T(d, Λ̂) ≤ Λ̂`.
Finally `Δ_T(d, Λ*) ≤ Δ_T(d, Λ̂) = 0`.  ∎

### 4.3 Remarks

1. **Why a chain adds `A_T` once.**  At every level the coarse rung `𝒳` is needed by all `2M̄ ≈ e^{ϖ + P_M}` outer points
   and costs `e^{(d−m)B′}` each: `ϖ − mB′ + P_M` nats more than `e^{dB′}` — the block is enumerated or sampled
   non-adaptively at a bounded threshold, at the rate `ln 2` or `a + O(√(ℓ_c/m))` instead of `B′`.  The fine rung is needed
   by only `e^{𝒳 + P_cnt}` points, and the procedure that serves it lives in dimension `d − m`: its `e^{(d−m)B′ + A}` is
   `e^{dB′ + A}` times `e^{−mB′}`, which pays for `e^{𝒳 + P_cnt + ln 4}` as soon as `mB′ ≥ 𝒳 + P̄_cnt + ln 4`.  So the maximum over
   the chain is the first term of the *first* level.  If the block is shorter, every level adds the deficit `Δ_T`.
2. **The block of the design.**  For an entry value `Λ_in` (the `Λ` with which the family is entered in the
   unrolling of §5) the design takes the least `m ≥ 1` with

       m·B′  ≥  𝒳 + P̄_cnt(N, Λ_in + N·B′; α/(13⌈N/m⌉)) + ln 4.                                                    (4.1)

   The right-hand side is nonincreasing in `m`, so the least `m` exists and every larger one also satisfies (4.1); by (iv)
   then `Δ_T = 0` and `Λ* < Λ + dB′` for all `d ≤ N`, `Λ ≤ Λ_in + (N − d)B′`.  `m = Θ((ln N + ln(1/α))/B′)`: at `u = 1`,
   `N = 10⁶`, `α = 1`: `m = 1 102` at `B′ = a` and `3 030` at `B′ = B_9 = 0.30a` (§7.3).
3. **How large `A_T` is.**  `mB′ ≈ 𝒳 + P̄_cnt + ln 4`, and `ϖ − mB′ ≈ m(a − B′) + u√(mℓ_c/2) + (4/(3p_u))ℓ_c` when (Q3)
   applies (`u = ½, 1`), `m(ln 2 − B′)` otherwise (`u = 2`, where `m*(ℓ_c) > m`).  So
   `A_T ≈ (a/B′ − 1)(𝒳 + P̄_cnt) + O(ln N)` resp. `(ln 2/B′ − 1)(𝒳 + P̄_cnt)`: `O(ln N + ln(1/α))` with a constant that grows
   like `1/B′ ≤ 1/h`.  With `P̄_cnt ≈ 3 ln N + 4 ln(1/c)`, `c ≈ αm/(13N)`: about `8 ln N` times the factor.  In numbers
   (`u = 1`, `α = 1`): `A_T = 231 … 510` nats at `N = 10⁶` for `B′ = a … B_9`, `376 … 937` at `10^{10}` (§7.3).  This is the
   price of a bounded accuracy now; it is not optimised — see §8, item 5.
4. **Below `d₀`.**  The brief enumerates below `d₀`.  That costs `(d₀ − 1)(ln 2 − B′) ≥ m(ln 2 − B′)`, as much as the
   trivial bound of the top level, and would cancel what (Q3) gains; the base bracket at the bounded accuracy `α̲` on
   `d₀ − 1 = O(ln N)` sites costs `(d₀−1)a + O(√(ln N·ln(1/α)) + ln N)` (Q5a), which is what `e₀` records.
5. **The uniform `c`.**  The brief takes `c_j ∝ 1/((j+1)(j+2))` along the chain, as Q does along the epochs.  The
   induction then needs `P̄_cnt` at the *deepest* level in (4.1) (and `P̄_M` uniform, or the increments
   `P_M^{(j+1)} − P_M^{(j)}` paid by the slack): `4 ln(1/c_j) = 8 ln j + O(1)` at depth `j`, against `4 ln N_T` for the uniform
   `c = α/(13N_T)`; since `N_T` enters `A_T` mainly through `m`, the uniform choice is the better one.
6. **The bookkeeping of `Λ` through a chain.**  A level of the chain adds `q_T = O(ln N)` to `ln(1/δ) + d ln 2`, a chain
   of `j(d) ≈ d/m` levels adds `j(d)·q_T < d·B′` by (iv): the invariant (2.1) grows by less than `N·B′ ≤ N·a` over a
   chain, so every `K` inside is `O(N)` times the `K` at the top.  (Along one path through a nest the blocks of *all*
   chain levels are disjoint, so the true growth over all chains together is below `N·max(q_T/m)`; the unrolled
   bound of §5 counts `N·B′` for each of the `M + 1` chains.  Replacing `d·ln 2` by `d·κ`, `κ = ln 2 + max q_T/m`, in the
   definition of the types would remove this over-count; it costs `ln(M+3)` in the logarithms and is not done.)
7. **Maxima of lines.**  The inner type of the chain is flat, so there is nothing to add: after a drop of a maximum
   of lines (§3, remark 1) the chain is applied with `B′ = max_i B_i′`.

---

## 5. The schedule and the theorems

### 5.1 The design

Fix `u`, the dimension `n ≥ 1` — it is the horizon of every family below —, `ε > 0`, `0 < δ < 1` and a number of epochs
`M ≥ 0`; `ε̂ := min(ε, 1)`; the epoch sequences are those of (R).  Put

    α^{(m)} := 1  (m < M),    α^{(M)} := ε̂;        𝒳_B := c′_n = ln 12 + 2 ln(n+1) + 2u + e^u,        𝒳_m := 𝒳_D¹(n; φ_m)  (m < M).

    𝔅       := the base family 𝔊_0 of Q, used at the accuracies x ≥ 𝒳_B only;
    𝔊_0     := 𝒯[𝔅; α^{(0)}, m_0];
    for m = 0, …, M−1:
        𝔊_{m,0} := 𝔊_m,     𝔊_{m,j} := S[𝔊_{m,j−1}]   (1 ≤ j ≤ J_m; the slope step of Proposition Q6, unchanged, with B = B_m),
        𝔊′_{m+1} := D′[𝔊_{m,J_m}; φ_m, 𝒳_m]   (tolerance b = 1),
        𝔊_{m+1}  := 𝒯[𝔊′_{m+1}; α^{(m+1)}, m_{m+1}].

The design returns the bracket of `𝔊_M(n, ε̂, δ)`.  The blocks `m_e` of the `M + 1` chains are fixed by (4.1) in the
unrolling below.  Compared with Q's schedule: each drop `D` is replaced by `D′` followed by a chain, and the base
family at a bounded accuracy by the base family at the accuracy `𝒳_B` followed by a chain.

*The least accuracies fit* (this is the trap of the brief avoided: every chain returns the accuracy to `≤ 1`):

| family | its least accuracy | accuracies at which it calls its inner families |
|---|---|---|
| `𝔅` | `𝒳_B ≈ 2 ln n + O(1)` | — |
| `𝔊_m = 𝒯[·]`, `m < M` (`𝔊_M`) | `1` (`ε̂`) | the coarse rung: `𝒳_B` resp. `𝒳_{m−1}`, exactly the least accuracy of `𝔅` resp. `𝔊′_m`; the fine rung: itself, in the dimension `d − m_m`, at `b_d ∈ [0.519α, α)`; below `d₀`: the base bracket at `α̲ ≥ 0.519α` |
| `𝔊_{m,j} = S[·]` | that of `𝔊_m` (`≤ 1`) | `≥ 1` (ladder down to the tolerance `1`), or the accuracy asked for (pass-through) |
| `𝔊′_{m+1} = D′[·]` | `𝒳_m ≈ ln(φ_m n) + O(1)` | `≥ 1` (ladder down to the tolerance `1`); pass-through at `𝒳_m` |

### 5.2 The theorem

*The unrolled error term.*  Start with `Λ̄ := Λ̄_0 := ln(1/δ) + n ln 2` and `𝓔 := 0`, and go down from the top:

    for e = M, M−1, …, 0:
        the chain on the exponent B′ = B_e (B_0 = a), with 𝒳 = 𝒳_{e−1} (𝒳_B for e = 0), α = α^{(e)}:
            m_e := the least block with (4.1) for Λ_in = Λ̄, N = n;      Λ̄ ← Λ̄ + j(n)·q_T(n, Λ̄ + n·B_e);      𝓔 ← 𝓔 + A_T(n, Λ̄);
        if e ≥ 1, epoch e − 1:
            the drop D′:     𝓔 ← 𝓔 + c_D′(n, Λ̄)   (B̃ = max{1, R_{e−1}/(2ua)}·B_{e−1});      Λ̄ ← Λ̄ + q_S(n, Λ̄);
            for j = J_{e−1}, …, 1 (slope steps):     𝓔 ← 𝓔 + c_S′(n, Λ̄; j/d_{e−1});      Λ̄ ← Λ̄ + q_S(n, Λ̄);
    𝓔′_M(n, ε, δ) := 𝓔 + E_𝔅(n; Λ̄),        E_𝔅(d; Λ) := ln( 8·(18(ln 4 + Λ) + 1) ) + ln(d+1).                                  (A.1)

(`c_S′(n, Λ; σ′) = σ′(1 + c_log(n) + h) + ℓ₀(n, Λ)` is the slope-step error of Corollary U1; with Q's `c_S(n, Λ; B_{e−1})`
in its place the theorem is "Q6 unchanged" to the letter and (A.1) is larger.  `q2lib.E_new` is this formula.)

**Theorem A [proved here: Propositions D′, T, Corollary U1; (Q5), (Q6), (R); given (T) with rule (P)].**  For all
`n ≥ 1`, `ε > 0`, `0 < δ < 1`, `M ≥ 0`: `𝔊_M(n, ε̂, δ)` returns `L ≤ U` with `L ≤ A ≤ U ≤ e^ε L` except with probability `δ` and
makes, in every run and at every `ψ ∈ L_u(Q_n)`, at most

    exp( n·B_M + 𝓔′_M(n, ε, δ) ),        B_M = h(1 + 1/d_M) ≤ h + c₁/(k_M + c₂),

evaluations.  Consequently `ln N(n; ε, δ) ≤ n·B_M + 𝓔′_M(n, ε, δ)`.  **No term of `𝓔′_M` is of the order `√n`:** it is a
sum of `k_M − 1 − M` slope-step terms, `M` drop terms and `M + 1` chain terms and `E_𝔅`, each `O(ln n + ln ln(1/δ))` (the
top chain: `O(ln n + ln ln(1/δ) + ln(1/ε̂))`) under the hypothesis of Proposition A′.

*Proof.*  *Types.*  By (Q5b), for `d ≤ n` and `x ≥ 𝒳_B = c′_n ≥ c′_d`: `b_{𝔊_0}(d, x, δ) ≤ d·a + ln(8K) + ln(d+1)` with
`K ≤ 18(ln 4 + ln(1/δ)) + 1`; so `𝔅` has `𝓗_n(a, 0, ∞; E_𝔅)` with least accuracy `𝒳_B > 1`.  Claim: `𝔊_m` has
`𝓗_n(B_m, 0, ∞; ·)` with least accuracy `α^{(m)} ≤ 1`.  For `m = 0`: Proposition T (`B′ = a ≤ ln 2`).  Step `m → m+1`: as in the
proof of Theorem Q8, `𝔊_{m,j}` has `𝓗_n(B_m, j/d_m, h/j; ·)` — the hypotheses of Q6 are `B_m ≥ h`, `σ = j/d_m ≤ 1` for
`j ≤ J_m − 1`, `R = h/j ≤ h` (or `R = ∞`, `σ = 0`), and least accuracy `≤ 1`, which holds because `𝔊_m` is a chain with
`α ≤ 1`; at `j = J_m` the slope is at least one on the range `R_m`, so `𝔊_{m,J_m}` has `𝓗_n(B_m, 1, R_m; ·)`.  Proposition D′
(`b = 1 ≥ x_min`, `R_m ≤ h < 1`, `φ_m = R_m/(a + R_m)`, `𝒳_m = 𝒳_D¹(n; φ_m)`) gives `𝓗_n(B_m a/(a + R_m), 0, ∞; ·) = 𝓗_n(B_{m+1}, 0, ∞; ·)`
for `𝔊′_{m+1}`, with least accuracy `𝒳_m > 1`; and Proposition T (`B_{m+1} ≤ a ≤ ln 2`) gives the claim for `𝔊_{m+1}`.
*Errors.*  The error functions that the propositions produce are, downwards from the family in question to its
inner family: `E(d, min(x,1); Λ + q_S(d, Λ)) + c_S′(d, Λ; σ′)` (slope step), `E(d, 1; Λ + q_S(d, Λ)) + c_D′(d, Λ)` (drop),
`E(d, 𝒳; Λ*(d, Λ)) + A_T(d, Λ*) + j(d)Δ_T(d, Λ*)` (chain); each is nondecreasing in `d` and `Λ` and nonincreasing in
`x` if `E` is.  The top family is called at `(n, ε̂, δ)` with `Λ = Λ̄_0`; unrolling at `d = n`, a chain is entered with
`Λ = Λ̄`, the value for which its block satisfies (4.1), so by Proposition T(iv) `Δ_T = 0` and
`Λ*(n, Λ̄) ≤ Λ̄ + j(n)q_T(n, Λ̄ + nB_e)`; with the monotonicity in `Λ` the total is at most (A.1).  The accuracy
delivered is at most `α^{(M)} = ε̂ ≤ ε`; the cost bound holds in every run by (T) with the abort rule (P), level by
level.  `B_M − h ≤ c₁/(k_M + c₂)` is (R).  ∎

*Remarks.*  (1) At every node the design may take the cheaper, by certified cost, of the procedure constructed
here and any other admissible one — e.g. Q's drop `D[·; c, α]` in place of `D′` and its chain in an epoch where
`u√(φ_m n ℓ_c/2)·B_{m+1}/a` is smaller than `A_T` (the late epochs at moderate `n`), or the base bracket at the accuracy
asked for; the accuracies fit for any such mixture, because a chain resets the accuracy that the inner epochs
must deliver to `1`, while a drop of Q passes the requirement `α − w(c)` down.  The bound is then the smaller one.
**[By the same propositions — the least accuracies are the only link between epochs —; not written out, and not
used in the formulas of §7.3.]**
(2) `M = 0`: the design is the chain on the base family, `ln N ≤ n·a + A_T + E_𝔅` — already without `√n`:
`exp(n·a + O(ln n + ln(1/ε̂)))` for the non-adaptive exponent, by nested levels with bounded outer blocks.

### 5.3 The closed form and the order

For `Λ̂ > 0`, an exponent `B′`, an accuracy `𝒳` and `0 < α ≤ 1` put `c̲ := α/(13n)` and

    ℓ_T(n, Λ̂; B′, 𝒳, α) := (ln 2 − B′)·max{ m̄ + 𝒳/(2u) ,  ln(78n/(5α))/ln((1+e^u)/2) } + P̄_M(n, Λ̂; c̲) + ln 8,
    m̄ := 1 + ( 𝒳 + P̄_cnt(n, Λ̂; c̲) + ln 4 )/B′ .

**Proposition A′ (closed form of (A.1)) [proved here].**  Let `Λ̂ ≥ (M + 3)·Λ̄_0` (e.g. `Λ̂ = (M+3)Λ̄_0`) and suppose
`(k_M − 1)·q_S(n, Λ̂) ≤ Λ̄_0`.  Then every `Λ̄` in (A.1) is at most `Λ̂`, and with `ℓ₀ := ℓ₀(n, Λ̂)`

    𝓔′_M  ≤  Σ_{m<M} [ J_m·ℓ₀ + (1 + c_log(n) + h)·J_m(J_m+1)/(2d_m) ]  +  Σ_{m<M} [ max{1, R_m/(2ua)}·B_m + ℓ₀ ]  +  Σ_{e=0}^{M} ℓ_T(n, Λ̂; B_e, 𝒳_{e−1}, α^{(e)})  +  E_𝔅(n; Λ̂)
          ≤  (k_M − 1 − M)·ℓ̄_S  +  M·ℓ̄_D  +  (M + 1)·ℓ̄_T  +  ℓ_𝔅,

    ℓ̄_S := ℓ₀ + ½(1 + c_log(n) + h),      ℓ̄_D := ℓ₀ + (a/h)(1 + c_log(n) + h) + max{1, h/(2ua)}·a,
    ℓ̄_T := max_{0≤e≤M} ℓ_T(n, Λ̂; B_e, 𝒳_{e−1}, α^{(e)}),      ℓ_𝔅 := E_𝔅(n; Λ̂)

(`𝒳_{−1} := 𝒳_B`).  For fixed `u`, `ln(1/δ) = O(n)` and `Λ̂ = (M+3)Λ̄_0`: `ℓ₀ = 4 ln n + ln(M+3) + O(1)`, hence

    ℓ̄_S = (9/2)·ln n + ln(M+3) + O(1),        ℓ̄_D = (a/h + 4)·ln n + ln(M+3) + O(1),        ℓ_𝔅 = 2 ln n + ln(M+3) + O(1),
    ℓ̄_T ≤ [8(ln 2/h − 1) + 5 + ln 2/(2u)]·ln n + [4(ln 2/h − 1) + 3]·ln(1/ε̂) + O(ln ln n)

(the last line when the first entry of the maximum in `ℓ_T` is the larger one and `9(ln 2/a − 1) ≤ 8(ln 2/h − 1)`, as for
`u ∈ {½, 1, 2}` and in every case evaluated; in general `ℓ̄_T = O(ln n + ln(1/ε̂))` by the same computation).

*Proof.*  *The growth of `Λ̄`.*  A slope step or a drop adds `q_S(n, Λ̄) ≤ q_S(n, Λ̂)` as long as `Λ̄ ≤ Λ̂`; a chain adds
`j(n)q_T(n, Λ̄ + nB_e) < n·B_e ≤ n·a` by Proposition T(iv), whatever `Λ̄`.  There are `k_M − 1` of the former and
`M + 1` chains, so by induction along (A.1) `Λ̄ ≤ Λ̄_0 + (k_M − 1)q_S(n, Λ̂) + (M+1)·n·a ≤ (2 + (M+1)a/ln 2)·Λ̄_0 ≤ (M+3)Λ̄_0 ≤ Λ̂`.
*The terms* are nondecreasing in `Λ`.  Slope steps of epoch `m`: `Σ_{j=1}^{J_m} j/d_m = J_m(J_m+1)/(2d_m)`, and with
`J_m < d_m + 1`, `d_m ≥ d_0 = h/(a−h)`: `J_m(J_m+1)/(2d_m) < J_m/2 + J_m/d_m ≤ J_m/2 + 1 + 1/d_0 = J_m/2 + a/h`; the
`a/h` is moved to `ℓ̄_D`.  Drops: `R_m ≤ h`, `B_m ≤ a`.  Chains: the block `m_e` of (4.1) is at most `m̄`, because every
`m ≥ (𝒳 + P̄_cnt(n, Λ̂; c̲) + ln 4)/B′` satisfies (4.1) (`c ≥ c̲`, `Λ̄ + nB′ ≤ Λ̂`, and `P̄_cnt` is nonincreasing in `c`);
`a_T ≤ (m+1) ln 2 − mB′ + P̄_M + ln 4`, `e₀ ≤ (d₀ − 1)(ln 2 − B′)` and
`d₀ − 1 ≤ max{m + 𝒳/(2u), ln(6/(5c))/ln((1+e^u)/2)}`; so `A_T(n, Λ̄) ≤ ℓ_T`.  *The orders:*
`ℓ₀(n, Λ̂) = 3 ln n + ln(Λ̂ + ln n) + O(1)`; `𝒳_m ≤ ln n + O(1)`, `𝒳_B = 2 ln n + O(1)`;
`P̄_cnt(n, Λ̂; c̲) = ln(A_n/c̲) + ln ν̄_D + ln K̄_D + O(1) = 7 ln n + 4 ln(1/α) + ln(M+3) + O(1)` and
`P̄_M = P̄_cnt − ln(A_n/c̲) + O(1) = 5 ln n + 3 ln(1/α) + ln(M+3) + O(1)`; `B_e ≥ h`.  ∎

**Theorem B [proved here from Theorem A, Proposition A′ and (R)].**  Fix `u > 0` and `0 < δ < 1`.
(a) For all `n ≥ 1`, `ε > 0`, `M ≥ 0`:  `ln N(n; ε, δ) ≤ n·h + n·c₁/(k_M + c₂) + 𝓔′_M(n, ε, δ)`.
(b) There are `n₀(u, δ)` and `C′(u, δ)` such that for all `n ≥ n₀` and all `0 < ε ≤ 1`

    ln N(n; ε, δ)  ≤  n·h + 2·√( (1 + r̄)·c₁·n·ℓ̄_S ) + C′·( (ln n)² + ln(1/ε) ),        ℓ̄_S = (9/2)·ln n + O(ln ln n),

more precisely with `M·ℓ̄_D + M·ℓ̄_T|_{α=1} + ℓ_T(n, Λ̂; B_M, 𝒳_{M−1}, ε) + ℓ_𝔅`, `M = O(ln n)`, in place of the last term.
Hence for every fixed `ε`, and for every sequence `ε_n ∈ (0, 1]` with `ln(1/ε_n) = o(√(n ln n))`,

    limsup_{n→∞} ( ln N(n; ε_n, δ) − n·h ) / √(n ln n)   ≤   C_*′(u) := 2·√( (9/2)·(1 + r̄)·c₁ )  =  3·√( 2(1 + r̄)c₁ )

(`C_*′ = 3.50, 6.56, 10.57` for `u = ½, 1, 2`, against `C_* = 4.65, 8.64, 13.52`; `C_*′/C_* = √(4.5/(a/h + 4))`).
(c) For every `ε > 0` there is `C(u, ε, δ)` with `ln N(n; ε, δ) ≤ n·h + C·√(n ln n)` for all `n ≥ 2` (as in Q; `C` is not `C_*′`).

*Proof.*  (a) Theorem A and (R).  (b) As in the proof of Theorem Q9(b), with `ℓ̄_S` for `ℓ_S`.  (So that the choice of `M`
is not circular, `ℓ̄_S`, `ℓ̄_D`, `ℓ̄_T`, `ℓ_𝔅` are evaluated here at `Λ̂ := (M̄_n + 3)Λ̄_0`, `M̄_n := 1 + ln(n+1)/ln(1+κ)`; Proposition A′ holds
with every `Λ̂ ≥ (M+3)Λ̄_0` that satisfies its hypothesis, and `M ≤ M̄_n` whenever `k_M ≤ n`.)  Let
`k† := √((1 + r̄)c₁n/ℓ̄_S)` and `M := max{m : k_m ≤ k†}`; then `k†/(1 + r̄) < k_M ≤ k†`, `n(B_M − h) < (1 + r̄)c₁n/k†`,
`(k_M − 1 − M)ℓ̄_S ≤ k†ℓ̄_S`, and `M ≤ 1 + ln(k_M + 1)/ln(1 + κ) = O(ln n)`.  The hypothesis of Proposition A′ holds for
large `n` — `k† = O(√(n/ln n))`, `q_S(n, Λ̂) = O(ln n)`, `Λ̄_0 ≥ n ln 2` — and does not involve `ε`.  `ε` enters (A.1) only
through the top chain, whose term is at most `ℓ_T(n, Λ̂; B_M, 𝒳_{M−1}, ε̂)`, linear in `ln(1/ε̂)` up to `O(ln n)`; all
other chains have `α = 1`.  So the terms beyond the level term are `O(M·ln n + ln(1/ε)) = O((ln n)² + ln(1/ε))`.
(c) For `n < n₀` use `N ≤ 2ⁿ`.  ∎

**Answers to the brief.**  *Does `C_*` change?*  The bounded levels never entered it.  It does change, for another
reason: Lemma U charges a slope step `σ′(1 + c_log + h)` instead of `(B/h)(1 + c_log + h)`, the slopes `σ′ = j/d_m` average
`½` over a late epoch, and `C_*` drops to `C_*′ = C_*·√(4.5/(a/h + 4))` (`0.76·C_*` at `u = 1`).  *Which term is now
second?*  After `n·h` and the level term `2√((1+r̄)c₁nℓ̄_S) = Θ(√(n ln n))`, the next term is `O((ln n)²)`: `M + 1` chains and
`M` drops at `O(ln n)` each, `M = O(ln n)` — where Theorem 11.58a has `C₁√n`.  *The accuracy:* it enters additively,
`O(ln(1/ε))` (one chain), where Q has `√(n·ln(1/ε))` inside `C₁√n` (the hinted lower bound of Theorem 11.25(a) is linear
in `ln(1/ε)` as well, by the computation of R12 (m1) with `k*(ε) ≈ ρ_h n − ln(1/ε)/u` — **[heuristic, not written out]**).
*What limits the method* is now the rate `c₁/k` alone, as the coordinator's sketch says.

### 5.4 The trap of the brief, made precise: drops `D′` without chains

If `D′` is not followed by a chain, the families of the next epoch have the least accuracy `𝒳`, and their levels
must be built with the tolerance `b = 𝒳`.  Lemma U and Proposition D′ are stated with a tolerance for this purpose,
and so is the slope step of §6 (Proposition Q6(e) with tolerance `b`; at `e = h` it is the slope step of Q with
`n_o = ⌊(x̂ − b − c_log(n))/h⌋`, `θ = e^{x̂−b} − c₃ − (2p_u)^n e^{−b}`, the ladder ending at `b`, pass-through below
`b + c_log(n) + h`, and the error `σ′(b + c_log(n) + h) + ℓ₀^b`).  The variant:

    b_0 := 𝒳_B,     b_{m+1} := 𝒳_D^{b_m}(n; φ_m) = b_m + ln( c₃ + 1 + 3(φ_m n + 1)e^{2u + e^u} );
    𝔑_0 := 𝔅;     𝔑_{m,j} := S^{b_m}[𝔑_{m,j−1}]  (j ≤ J_m),     𝔑_{m+1} := D′[𝔑_{m,J_m}; φ_m, b_{m+1}]  (tolerance b_m);     output 𝒯[𝔑_M; ε̂, m](n, ε̂, δ).

**Proposition N [proved here: the induction of Theorem A with Lemma U, Proposition D′ and Proposition Q6(h) at
the tolerances `b_m`, and one chain].**  This design is admissible and costs at most `exp(n·B_M + 𝓔^N_M)`,

    𝓔^N_M := A_T(top chain, 𝒳 = b_M) + Σ_{m<M} [ c_D′^{b_m}(n, Λ̄) + Σ_{j=1}^{J_m} ( (j/d_m)(b_m + c_log(n) + h) + ℓ₀^{b_m}(n, Λ̄) ) ] + E_𝔅(n; Λ̄)

(unrolled as (A.1), with `q^{b_m}` for `q_S`; `q2lib.E_trap`).  Compared with (A.1): one chain instead of `M + 1`, and
every slope step of epoch `m` loses `(j/d_m)(b_m − 1)` more, in total `≈ ½ Σ_m J_m·b_m`, where

    b_m = 2 ln(n+1) + Σ_{i<m} ln(φ_i n + 1) + O(m)  ≤  (m + 2)·ln(n+1) + O(m).

*What it gives.*  **[the order: proved up to the bookkeeping of `Λ̄`, which is that of Proposition A′ with
`q^{b_m} = O(ln n)` and is not written out; the constants: heuristic]**  Since `b_m ≤ (m+2) ln(n+1) + O(m)` and
`M = O(ln n)`, the level term is at most `(k_M − 1)·O((ln n)²)` and the bound is `n·h + O(√n·ln n)` — worse than
Theorem B by a factor `√(ln n)`, as the brief says.  The majority of the slope steps are in the last epochs, where
`b_m` is largest: with `φ_i ≈ h/(J_i a)`, `J_i ≈ ρ^i` (`ρ ≈ a/(a−h)` numerically) and `M ≈ ln n/(2 ln ρ)` one gets
`b_M ≈ (3/8)(ln n)²/ln ρ`.  In numbers the variant is *better* than Theorem A as long as there are few epochs
(up to `n ≈ 1.3·10⁶` at `u = 1`: the tolerance costs less than a chain per epoch) and worse beyond (§7.3).  A design with a
chain every few epochs interpolates; choosing where to put the chains is a finite optimisation over (A.1)-type
formulas and is not done here.

---

## 6. Part B: Proposition Q6(e) — the slope step at a general outer rate

### 6.1 The family and the statement

Let `N ≥ 1`; let `𝔉` be a certified family up to `N` of type `𝓗_N(B, σ, R; E)` with `0 ≤ σ ≤ 1`, `R ∈ (0, ∞]` (`σ = 0` if
`R = ∞`), least accuracy `x_min`.  Let `b ≥ max(1, x_min)` be a tolerance (`b = 1` is the standard case; `b > 1` is the
case of §5.4) and `e` an outer rate with `0 < e ≤ 2u` (every `e ≤ ε* < u/2` is admitted).  Put

    ϑ := θ_na(e),        σ′ := [ B − (1 − σ)·ϑ ]/e,        R′ := R·e/(ϑ + R)   (R′ := e if R = ∞),        X₀^e(n) := b + c_log(n) + e.

The family `S_e[𝔉]` (up to `N`, least accuracy `x_min`): for `(n, x, δ)` let `x̂ := min(x, R′n)`.

* If `x̂ < X₀^e(n)`: `S_e[𝔉](n, x, δ) := 𝔉(n, x, δ)` (pass-through).
* Otherwise the **level as built** is the level of Lemma U with

      n_o = ⌊(x̂ − b − c_log(n))/e⌋,      the rate e,      θ = e^{x̂−b} − c₃ − (2p_u)^n·e^{−b},      the cap Ξ = n_o·ϑ,

  i.e. Algorithm 2L⁺ with `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, tolerance `b`, and the ladder of step one from
  `min{b + ⌈n_oϑ − b⌉₊, b + ⌈2un_i − b⌉ − 1}` down to `b` (for `b = 1`: `2un_i > min{max(⌈n_oϑ⌉, 1), ⌈2un_i⌉ − 1} > … > 2 > 1`),
  served by `𝔉`; and `S_e[𝔉](n, x, δ)` is the cheaper of this level and of `𝔉(n, x, δ)`.

**Proposition Q6(e) [proved here from Lemma U].**  The level as built is admissible for (T) and has accuracy
exactly `x̂ ≤ x`; on its outer block `ln(1/π†) ≤ n_o·θ_na(e) + ln(n_o + 1)`; and `S_e[𝔉]` has the type `𝓗_N(B, σ′, R′; E′)` —
i.e. `b_{S_e[𝔉]}(n, x, δ) ≤ n·B − σ′·min(x, R′n) + E′(n, x; Λ)` for all `n ≤ N`, `x ≥ x_min`, `δ`, `Λ ≥ ln(1/δ) + n ln 2` — with

    E′(n, x; Λ) := E(n, min(x, b); Λ + q^b(n, Λ)) + c_S^e(n, Λ),        c_S^e(n, Λ) := σ′₊·(b + c_log(n) + e) + ℓ₀^b(n, Λ).

The type map is that of the brief: `(B, σ, R) ↦ (B, [B − (1−σ)θ_na(e)]/e, R·e/(θ_na(e) + R))`; the least accuracy of the
new family is that of `𝔉`; the inner family is called at accuracies `≥ b`, or at the accuracy asked for.
*The error term.*  `σ′ ≤ B/e`, so for `b = 1` and `e` in a compact interval `[e₀, e₁] ⊂ (0, ε*]`, uniformly in `e`:

    ℓ_S(n; e) := c_S^e(n, Λ)  ≤  (B/e₀)·(1 + c_log(n) + e₁) + ℓ₀(n, Λ)  =  (B/e + 4)·ln n + O(1)      (Λ = O(n)),

the expected form — and more precisely `(σ′ + 3)·ln n + ln(Λ + ln n) + O(1)` with the new slope `σ′` itself in place of `B/e`.
At `e = h`, `b = 1` the proposition is Q6 with the error term of Corollary U1 (the ladder is capped at `⌈n_oh⌉`
instead of `⌈x̂⌉`, which changes nothing in the bound).

*Checklist of (T).*  That of Lemma U, whose hypotheses hold for `x̂ ≥ X₀^e(n)`:
`n_o ≥ 1`; `n_o ≤ (x̂ − b − c_log(n))/e < x̂/e ≤ R′n/e ≤ n`, so `n_o ≤ n − 1` and `n ≥ 2` (H1); `n_i ≥ n − (en − b − c_log(n))/e
= (b + c_log(n))/e`, hence `2un_i ≥ 2u(b + c_log(n))/e > b` for `e ≤ 2u` (H8); the threshold: `x̂ − b ≥ c_log(n) + e` and
`e^{c_log(n)} ≥ 12·e^{1+2u} > 2(c₃ + 1)`, so `θ ≥ e^{x̂−b} − (c₃ + 1) ≥ e^{x̂−b}/2`, and `n_o·e ≤ x̂ − b − c_log(n)` gives
`3(n_o+1)e^{2u+e^u+n_oe} ≤ 3(n+1)e^{2u+e^u}·e^{x̂−b}/(6(n+1)e^{2u+e^u}) = e^{x̂−b}/2 ≤ θ` (H5, and the hypothesis of (Q4) at the
rate `e`); the cap: `Ξ = n_oϑ ≤ n_o ≤ n` (`ϑ < a < 1`), and if `R < ∞`, **the range condition**
`n_o·ϑ ≤ (x̂/e)·ϑ ≤ R·(n − x̂/e) ≤ R·n_i`, where the middle inequality is `x̂ ≤ R′n`; inner calls at accuracies `≥ b ≥ x_min`
in the dimension `n_i ≤ N` (H9).  The accuracy is `ln[(2p_u)^n + e^b(c₃ + θ)] = x̂`.

*Proof.*  Let `n ≤ N`, `x ≥ x_min`, `δ`, `Λ ≥ ln(1/δ) + n ln 2`, `x̂ = min(x, R′n)`.
*The level as built* (`x̂ ≥ X₀^e(n)`).  By (U): `ln C_max ≤ n_iB + (1−σ)n_oϑ + ℓ₀^b(n, Λ) + E(n, b; Λ + q^b(n, Λ))`, and
`n_iB + (1−σ)n_oϑ = nB − n_o·e·σ′`.  If `σ′ ≥ 0`: `n_o·e ≥ x̂ − b − c_log(n) − e`, so `−n_o e σ′ ≤ −σ′x̂ + σ′(b + c_log(n) + e)`.
If `σ′ < 0`: `n_o·e ≤ x̂`, so `−n_o e σ′ ≤ −σ′x̂`.  And `E(n, b; ·) ≤ E(n, min(x, b); ·)`.
*The pass-through* (`x̂ < X₀^e(n)`): `b_𝔉(n, x, δ) ≤ nB − σ·min(x, Rn) + E(n, x; Λ) ≤ nB + E(n, x; Λ)
≤ nB − σ′x̂ + σ′₊·X₀^e(n) + E(n, min(x, b); Λ + q^b(n, Λ))`.
The cheaper of two procedures obeys the bound of either.  `E′` is nonnegative, nondecreasing in `n` and `Λ` and
nonincreasing in `x`.  ∎

**Corollary Q6(e)-max (maxima of finitely many lines) [proved here].**  Let `𝔉` have the type `𝓗_N(𝔏, R; E)`,
`𝔏 = {(B_i, σ_i)}_{i∈I}`, `0 ≤ σ_i ≤ 1` — that is, `b_𝔉(d, x, δ) ≤ max_i[d·B_i − σ_i·x] + E` for `x_min ≤ x ≤ R·d`, and the value at
`R·d` beyond.  Then `S_e[𝔉]` — the *same* family: the level's parameters `n_o`, `θ`, the ladder do not depend on `𝔏` — has
the type `𝓗_N(𝔏′, R′; E′)` with

    𝔏′ := { (B_i, σ_i′) }_{i∈I},      σ_i′ := [ B_i − (1 − σ_i)·θ_na(e) ]/e,      R′ = R·e/(θ_na(e) + R),
    E′(n, x; Λ) := E(n, min(x, b); Λ + q^b(n, Λ)) + ℓ_S(n; e),      ℓ_S(n; e) := max_i σ′_{i,+}·(b + c_log(n) + e) + ℓ₀^b(n, Λ):

`b(n, x, δ) ≤ max_i[n·B_i − σ_i′·min(x, R′n)] + E′(n, x; Λ)` — **one loss `ℓ_S(n; e) ≤ (max_i B_i/e)(b + c_log(n) + e) + ℓ₀^b` for
all lines**, on the range `x_min ≤ x ≤ R′·n` (and the value at `R′n` beyond).
(*Proof.*  The checklist is the same.  (U) holds for the maximum:
`ln C_max ≤ max_i[n_iB_i + (1−σ_i)n_oϑ] + ℓ₀^b + E₁ = max_i[nB_i − n_o e σ_i′] + ℓ₀^b + E₁`, and line by line
`−n_o e σ_i′ ≤ −σ_i′x̂ + σ′_{i,+}(b + c_log(n) + e)`.  Pass-through: `max_i nB_i ≤ max_i[nB_i − σ_i′x̂] + max_i σ′_{i,+}·x̂`.  ∎)

### 6.2 Remarks for the user of the corollary  [elementary consequences of §6.1 and of Lemma U; proved here]

1. **Where the hypotheses are used.**  `σ_i ≤ 1`: the term of a rung finer than the dominant one is
   `(1−σ)x_l + n_iB + …`, nondecreasing in `x_l` only then (the auxiliary inequality of Lemma U).  `σ_i ≥ 0`: the
   pass-through, and the first rung.  The range `R`: the dominant rung `n_oθ_na(e)` must lie in the range of the inner
   majorant, which is exactly `x̂ ≤ R′n`.  (C2): one line must be nonnegative at the dominant rung (it is, for the
   type of an actual family).
2. **The image can leave the class** `0 ≤ σ ≤ 1`, as §2.5 of `R_brief.md` says, and the corollary states it as it is:
   `σ_i′ > 1` when `B_i > e + (1−σ_i)θ_na(e)` — then `(B_i, 1)` on `(0, R′]` is a weaker valid line ("a slope larger than
   one implies slope one"); `σ_i′ < 0` when `B_i < (1−σ_i)θ_na(e)` (possible for `e < h`) — then the line *increases*
   with the accuracy, the flat line `(B_i − σ_i′R′, 0)` is a valid replacement, and for a single line the family is no
   better than `𝔉` itself.  The new range `R′` is smaller than `R` iff `e < θ_na(e) + R` (always for `e ≤ h`); a type with
   range `R′` is also a type with any smaller range.
3. **Uniformity in `e`.**  The rate enters the error only through `σ′₊(b + c_log(n) + e)`; the constants `A_n`, `K̄`, `ℓ₀`
   do not depend on `e`.  As `e → 0` the loss `σ′·c_log(n)` grows like `1/e` — the outer block is short by
   `(b + c_log(n))/e` sites; this is why the statement is uniform on compact subintervals of `(0, ε*]` only.  For
   `e ≥ ε*`, `θ_na(e) = 0`, the lemma still applies (`e ≤ 2u`): the block is closed at radius `≈ n_o/2` and `σ′ = B/e`.
4. **Tolerance.**  With `b > 1` the same statement holds with `b + c_log(n)` for `1 + c_log(n)` and `A_n^b` for `A_n`:
   a slope step on a family whose least accuracy is `b` loses `σ′(b − 1)` more.
5. **The drop on a maximum of lines** is Proposition D′ (any slopes in `[0, 1]`); the chain needs a flat type.  So
   "slope step at a rate `e ∈ [e₀, e₁]` on a maximum of lines; drop; chain" are all available at finite `n` with the
   losses `ℓ_S(n; e)`, `c_D′`, `A_T`.

---

## 7. Numerical checks

All numbers are from the scripts of §10.  Every level is evaluated with the exact constants of Theorem 11.56
(`r†`, `π†` from tables of the outer cube; `J`, `ν₀`, `m_max`, `K`, `M̄`, `δ′`, `x_out`, `C_max` by the formulas of
`K_REPORT.md` §2.2) by **two independent evaluators** — `qlib.level_consts/level_cmax` of workstream Q (tables of
referee R8) and `r12lib.level_consts/level_cmax` of referee R12 (own tables); neither is modified.  On the 2.02 million
levels of checks 1, 2A, 5 and 6 they agree to `6·10^{-11}` in `ln C_max`, `ln δ′`, `x_out`, and `r†`, `J`, `K` never differ.
"Saturating" inner families have a certified cost *equal* to the majorant that their type allows,
`max(0, max_i[d·B_i − σ_i·min(x, R·d)]) + E(d, x; ln(1/δ) + d ln 2)`, with `E = 0` or one of `3√d`, `Λ/7`, `5/x + ln Λ`; since
`C_max` is nondecreasing in the inner costs this is the worst case of the hypothesis.
**In the final runs no inequality of this report is violated.**  Two test errors of mine produced "violations" on
the way, and both are instructive: (i) lines that are negative on their range (`B < σR`: the type of no family, (C2))
— there the saturating family `max(0, ·)` does not have the type, and the bound of Proposition D′ fails by up to
`1.7·10⁵` nats; (ii) an inner slope `σ = 1/d_0 = 2.9 > 1` (the slope *after* the last step of an epoch, used as an input
by mistake) — there the bound of Proposition Q6(e) fails by up to `9·10³` nats: the hypothesis `σ ≤ 1` is needed.  Both
kinds of case are excluded from the stored outputs.

### 7.1 Proposition D′ and one level of the chain (`q2_01_levels.py` → `out_q2_01_levels.txt`)

*Part A — Proposition D′ (Lemma U at the rate `0`), tolerance `1`.*  Inner family saturating.  Types: the epoch
schedule `(B_m, 1, R_m)`, `φ_m`, `m ≤ 12`; one line with `B ∈ {h, a, 3a}`, `σ ∈ {0, 0.3, 0.7, 1}`, `R ∈ {h, h/3, h/50, min(1, 6h)}`
(`B ≥ σR`), `φ ∈ {1, ½}·R/(a + R)`; maxima of two to four lines.  Sizes: from the first `n` at which the level exists
(`n = 2 … 400`) and the next ones, to `10⁶`; `δ ∈ {0.5, 0.05, 10^{-12}, e^{-n}}`; horizon `N ∈ {n, 3n}`.

| `u` | types | levels built | violations | least slack of Proposition D′ (nats) | of Lemma U(d) | `c_D′` | pass-through cases |
|---|---|---|---|---|---|---|---|
| ½ | 13 + 86 + 18 | 9 379 | 0 | 4.41 (schedule), 3.65 (one line), 3.66 (maxima) | 3.64 | 16.6 … 65.3 | 66 064 |
| 1 | 13 + 86 + 18 | 9 379 | 0 | 4.84, 3.45, 4.04 | 3.43 | 16.4 … 66.4 | 63 712 |
| 2 | 13 + 86 + 18 | 9 379 | 0 | 3.48, 2.30, 3.35 | 2.21 | 17.2 … 68.2 | 59 552 |

At every level: accuracy `= 𝒳` to `4·10^{-15}`; `r† ≥ min{n_o − 1, ⌊p_u n_o⌋ + 1}` (with equality in some cases) and
`ln(1/π†) ≤ n_o a + ln(n_o+1)` (least slack `a`, at an outer block of one site); every constant of Lemma U(b) and (2.1).
The proposition is close to sharp: the least slack is `2.3`–`4.8` nats against an error term of `16`–`68`.  At the
schedule's own parameters (`u = 1`, `m = 0`, `δ = 0.05`; part A0 of the output): `ln C_max − n·B_1 = 25.2, 36.5, 44.0, 51.1` at
`n = 10³ … 10⁶` against `c_D′ = 37.7 … 65.3` — a drop costs about `3.7·ln n` nats, with **no `√n`**; Q's drop has
`c_D = 89 … 1850` over the cases of its §7.2.

*Part B — the induction step of Proposition T.*  The level in dimension `d` of a chain is evaluated with
`ln C_1 = (d−m)B′ + E` (saturating `𝔊′`) and `ln C_2` *equal to the bound that Proposition T claims for the chain in
dimension `d − m`* at the failure probability `δ′` (the induction hypothesis, saturated), and compared with the claim
`d·B′ + U(d, Λ)`.  Chains: `B′ = B_e`, `e ∈ {0, 1, 2, 4, 8, 12}`, `α ∈ {1, 0.1, 0.001}`, `N = 10³ … 10⁶`; the block of the design
and blocks `2×`, `½×`, `1/7×` as long (the short ones have `Δ_T > 0`: the deficit term is tested); `d` from `d₀` to `N`;
`δ` from `0.5` to `e^{-30d}`.

| `u` | chains | levels | violations | least slack of the step (nats) | levels with `Δ_T > 0` | least `ϖ(m; c) − ln(1/π†)` |
|---|---|---|---|---|---|---|
| ½ | 446 | 16 312 | 0 | 5.28 | 9 959 | 33.1 |
| 1 | 516 | 19 176 | 0 | 3.91 | 11 388 | 25.0 |
| 2 | 560 | 20 872 | 0 | 4.99 | 11 858 | 0.00 (a short block with `r† = −1`: the trivial bound is attained) |

Also at every level: accuracy `≤ a_d ≤ α`; `J + 1 ≤ A_d/c`, `ν₀ ≤ ν̄_D`, `m_max + 1 ≤ m̄_D`, `K ≤ K̄_D`, `P_cnt ≤ P̄_cnt`, `P_M ≤ P̄_M`,
and (2.1) in the form `ln(1/δ′) + (d−m) ln 2 ≤ Λ + q_T(d, Λ)`.

### 7.2 The chain, exactly (`q2_02_chain.py` → `out_q2_02_chain_A.txt`, `out_q2_02_chain_BC.txt`)

*Part A — the recursion over the chain on a saturating `𝔊′`.*  The certified cost of `𝒯(d, δ)` is computed level by
level (top-down for `δ′`, bottom-up for the costs; at the bottom the real base bracket at `α̲`) and compared with
`d·B′ + E_T(d; Λ)`; inside each chain about twenty levels and the last three are also compared with the bound at
their own `(d, δ)`.  11 169 chains with 1 576 974 levels (`u ∈ {½, 1, 2}`, the exponents and accuracies of §7.1 B,
`N = 10³ … 10⁶`, `d ≤ N`, `δ ∈ {0.5, 0.05, e^{-d}}`, the block of the design and `2×`, `½×`): **no violation; least slack
`41.6` nats**.  The block of the design, `d = N`, `δ = 0.05`, `E = 0`, `α = 1`:

| `u` | `B′/a` | `N` | block `m` | levels `j(N)` | `c` | exact `ln cost − N·B′` | `A_T` (bound) | slack |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | `10⁴` | 741 | 13 | `5.5·10^{-3}` | 81.7 | 160.7 | 78.9 |
| 1 | 1 | `10⁶` | 1 099 | 909 | `8.5·10^{-5}` | 126.6 | 230.7 | 104.1 |
| 1 | 0.792 | `10⁶` | 1 204 | 830 | `9.3·10^{-5}` | 156.1 | 261.5 | 105.4 |
| 1 | 0.439 | `10⁶` | 2 112 | 473 | `1.6·10^{-4}` | 278.1 | 387.3 | 109.2 |
| 1 | 0.277 | `10⁴` | 2 098 | 4 | `1.5·10^{-2}` | 269.6 | 355.5 | 86.0 |
| 1 | 0.277 | `10⁶` | 3 236 | 309 | `2.5·10^{-4}` | 423.1 | 537.4 | 114.3 |
| ½ | 1 | `10⁶` | 3 759 | 266 | `2.9·10^{-4}` | 111.7 | 181.1 | 69.4 |
| ½ | 0.266 | `10⁶` | 11 308 | 88 | `8.6·10^{-4}` | 393.9 | 471.1 | 77.2 |
| 2 | 1 | `10⁶` | 410 | 2 438 | `3.2·10^{-5}` | 133.7 | 217.7 | 84.0 |
| 2 | 0.302 | `10⁶` | 1 119 | 893 | `8.6·10^{-5}` | 426.5 | 729.5 | 303.1 |

So **a chain of up to 2 438 nested levels costs `112 … 427` nats in all at `N = 10⁶`** — it does not grow with its
length, only with `ln N` (`u = 1`, `B′ = a`: `61.6, 81.7, 104.4, 126.6` nats for `1, 13, 108, 909` levels at `N = 10³ … 10⁶`,
i.e. about `9·ln N`, through `𝒳`, `P_cnt` and `ln(1/c)`).  The bound is `70`–`300` nats above the exact value: `ϖ(m; c)`
against the exact `ln(1/π†)` (e.g. `289` against `200` at `u = 1`, `m = 1 099`; at `u = 2` only the trivial bound is
available, `285` against `216`), and the bounds `P̄_M`, `P̄_cnt`.  For `α = 0.001` the cost is `50`–`150` nats higher.

*Part B — the real base family under the chain:* `𝔊_0 = 𝒯[𝔅; α]`, the base bracket at the accuracy `𝒳_B(N)` inside.
(`qlib.BaseTable` and `r12lib.Base` agree to `10^{-12}` on 324 cases; the faster one is used.)  `N = 10³ … 10⁶`,
`α ∈ {1, 0.01}`, `δ ∈ {0.05, e^{-N}}`: no violation; least slack of the induction `67` nats, of Proposition Q5(b) at
`e = 0` (the type of `𝔅`) `7.5` nats.  The exact cost is *below* `e^{N·a}` from `N ≈ 8·10³` on:
`ln cost/(N·a) = 1.319, 1.007, 0.938, 0.919, 0.950, 0.972` at `N = 10³, 4·10³, 1.6·10⁴, 6.4·10⁴, 2.56·10⁵, 10⁶` (`u = 1`, `α = 1`) — the
base bracket at the accuracy `≈ 2 ln N` closes above `p_u d`.  A bounded accuracy at the non-adaptive exponent `a`
therefore costs `e^{N·a + O(ln N)}` at most, where Proposition Q5(a) has `e^{N·a + Θ(√N)}` (`1.03√N` measured at `6.4·10⁴`).

*Part C — drop and chain together:* `𝒯[D′[𝔉; φ_m, 𝒳_m]; α]` on a saturating `𝔉` of slope one (cost `d·B_m − min(x, R_m d)`),
`m ∈ {0, 2, 6, 11}`, `α ∈ {1, 0.01}`, `N = 10³ … 10⁵` (and `10⁶` for `m = 6`, `u ∈ {½, 1}`); every `D′` level inside the chain
is built at its own `(d, δ′)`.  No violation; least slack of `D′` as built `3.1` nats, of the induction over the chain
`59.6` nats.  E.g. `u = 1`, `m = 6`, `N = 10⁶`: `ln cost − N·B_7 = 418.0` against `c_D′ + A_T = 542.4` (359 chain levels, 351 `D′`
levels built).

### 7.3 The bound of Theorem A in numbers (`q2_03_formula.py` → `out_q2_03_formula.txt`)

Formula evaluation only.  `u = 1`, `ε = 1`, `δ = 0.05`; every bound minimised over `M`.  "old": (5.2) of Q (its table of
§7.4, reproduced digit by digit).  "new/Q": (A.1) with Q's `c_S` for the slope steps — the effect of the chains alone.
"new": (A.1) (slope steps with `c_S′`).  "no chain": the variant of §5.4.  In units of `n·a` (`h/a = 0.26265`); in
brackets `(bound − nh)/√(n ln n)`.

| `n` | old: `M`, bound | new/Q | new: `M`, `k_M`, bound | no chain: `M`, bound | old − new (nats) | `(old − new)/(old − nh)` | new: `𝓔′_M` = base + slope steps + drops `D′` + chains |
|---|---|---|---|---|---|---|---|
| `10³` | 0, 1.916 [2.21] | 2.320 | 0, 1, 2.320 [2.75] | 0, 2.320 | −45 | −0.24 | `146 = 18 + 0 + 0 + 1×128` |
| `10⁴` | 0, 1.190 [3.39] | 1.166 | 0, 1, 1.166 [3.30] | 0, 1.166 | 26 | 0.03 | `184 = 23 + 0 + 0 + 1×161` |
| `1.6·10⁴` | 2, 1.098 [3.77] | 1.098 | 1, 3, 1.088 [3.73] | 2, 1.025 [3.44] | 17 | 0.01 | `526 = 24 + 1×97 + 1×49 + 2×178` |
| `3.2·10⁴` | 3, 0.858 [3.67] | 0.886 | 3, 7, 0.871 [3.75] | 3, 0.786 [3.23] | −45 | −0.02 | `1 328 = 26 + 3×89 + 3×52 + 4×220` |
| `6.4·10⁴` | 5, 0.707 [3.75] | 0.702 | 3, 7, 0.695 [3.64] | 3, 0.649 [3.26] | 90 | 0.03 | `1 404 = 27 + 3×93 + 3×54 + 4×234` |
| `10⁵` | 5, 0.618 [3.67] | 0.626 | 5, 13, 0.619 [3.68] | 5, 0.576 [3.24] | −12 | −0.00 | `2 557 = 28 + 7×86 + 5×56 + 6×275` |
| `10⁶` | 10, 0.3713 [3.24] | 0.3609 | 9, 34, 0.3581 [2.85] | 9, 0.3559 [2.78] | 1 471 | 0.12 | `6 588 = 33 + 24×86 + 9×65 + 10×390` |
| `10⁷` | 14, 0.2957 [2.89] | 0.2871 | 14, 116, 0.2862 [2.06] | 12, 0.2900 [2.39] | 10 567 | 0.29 | `17 846 = 37 + 101×90 + 14×75 + 15×513` |
| `10⁸` | 17, 0.2731 [2.71] | 0.2693 | 17, 268, 0.2690 [1.64] | 16, 0.2714 [2.27] | 45 982 | 0.40 | `37 122 = 42 + 250×99 + 17×84 + 18×613` |
| `10⁹` | 21, 0.2660 [2.60] | 0.2646 | 21, 863, 0.2645 [1.43] | 19, 0.2656 [2.30] | 167 768 | 0.45 | `108 419 = 47 + 841×108 + 21×93 + 22×719` |
| `10^{10}` | 25, 0.2637 [2.53] | 0.2633 | 25, 2 868, 0.2632 [1.35] | 23, 0.2637 [2.37] | 568 799 | 0.47 | `358 401 = 51 + 2 842×118 + 25×102 + 26×823` |
| `10^{12}` | 32, 0.2628 [2.41] | 0.2627 | 32, 23 995, 0.2627 [1.29] | 30, 0.2628 [2.55] | 5 892 514 | 0.47 | `3.35·10⁶ = 61 + 23 962×138 + 32×121 + 33×1 023` |

Reading.  (i) **Where the new bound is below the old one, and by how much.**  In a scan with ten sizes per decade
the new bound is below the old one at every size above `10⁵` (the last size at which it is not: `n = 10⁵`; with Q's
`c_S`: `2.5·10⁵`); from `10⁴` to `10⁵` the two are within `3 %` of `old − nh` of each other, either way (a chain costs
`160`–`275` nats there; Q's base term is `210`–`566` nats and its drops `180`–`255` each).  The gain is `12 %` of the excess over `n·h` at `10⁶`, `29 %` at `10⁷`, `40 %` at
`10⁸` and `47 %` from `10^{10}` on; the error term itself falls from `9.24·10⁶` to `3.35·10⁶` nats at `n = 10^{12}`.  Both bounds
are below `n·a` from `n ≈ 2.5·10⁴` on (scan); `sup_n (bound − nh)/√(n ln n)` over the scan is `3.77` (old) and `3.83` (new, at
`n ≈ 2·10⁴`).  (ii) **No `√n`:** the "second term" — chains, drops and base together — is `4 517` nats at `10⁶`, `12 500` at
`10⁸`, `23 997` at `10^{10}`, `37 677` at `10^{12}`, i.e. `24 … 49` times `(ln n)²` and `33 … 41` times `(M+1)·ln n`, where the old
formula has `C₁√n`-terms of `6 015`, `55 128`, `549 405`, `5.5·10⁶` nats; `[n(B_M − h) + slope steps]/√(n ln n)` falls from `1.63` to
`1.28` (part F of the output).  (iii) **The chains.**  At `n = 10⁶` (`M = 9`) the ten chains have blocks `m = 1 102 … 3 030`,
`330`–`907` levels, `c ≈ 10^{-4}`, and cost `A_T = 231 … 510` nats (`B′ = a … 0.30a`); at `10^{10}` (`M = 25`): `m = 1 833 … 5 754`,
up to `5.5·10⁶` levels, `c ≈ 4·10^{-8}`, `A_T = 376 … 940`.  `Δ_T = 0` in all, and each chain raises `Λ̄` by `0.018 … 0.06·n`;
`Λ̄` ends at `1.05 … 2.1` times `Λ̄_0` (the cap of Proposition A′ is `(M+3)Λ̄_0`).  A slope step costs `86`–`138` nats (Q:
`97`–`156`), a drop `D′` `49`–`121`.  (iv) **Without chains** (§5.4) the bound is *better* than (A.1) up to `n ≈ 1.3·10⁶` —
`0.576·na` at `10⁵` and `0.649·na` at `6.4·10⁴`, where old and new have `0.62` and `0.70` — and worse beyond; from `n ≈ 10^{11}`
on it is worse than Q's bound.  With few epochs the tolerances `b_m ≈ (m+2) ln n` cost less than one chain per
epoch.  (v) **Other parameters** (old | new, in units of `na`):

| `u`, `ε`, `δ` | `n = 6.4·10⁴` | `10⁶` | `10⁸` | `10^{10}` | `10^{12}`: `(new − nh)/√(n ln n)` |
|---|---|---|---|---|---|
| 1, 1, 0.05 | 0.7072 \| 0.6945 | 0.3713 \| 0.3581 | 0.2731 \| 0.2690 | 0.2637 \| 0.2632 | 1.29 |
| 1, 0.01, 0.05 | 0.7710 \| 0.7060 | 0.3863 \| 0.3591 | 0.2745 \| 0.2690 | 0.2639 \| 0.2632 | 1.29 |
| 1, `10^{-6}`, 0.05 | 0.8643 \| 0.7288 | 0.4104 \| 0.3612 | 0.2765 \| 0.2690 | 0.2641 \| 0.2632 | 1.29 |
| 1, 1, `e^{-n}` | 0.7088 \| 0.6961 | 0.3717 \| 0.3585 | 0.2731 \| 0.2690 | 0.2637 \| 0.2632 | 1.29 |
| ½, 1, 0.05 (`h/a = 0.2532`) | 1.0287 \| 1.0505 | 0.4443 \| 0.4397 | 0.2717 \| 0.2663 | 0.2552 \| 0.2544 | 0.68 |
| 2, 1, 0.05 (`h/a = 0.2968`) | 0.5613 \| 0.5064 | 0.3631 \| 0.3417 | 0.3036 \| 0.3002 | 0.2975 \| 0.2971 | 2.20 |

(vi) **The accuracy enters additively.**  `[bound(ε) − bound(1)]/ln(1/ε)` is `24.7`, `27.0`, `27.5` nats at
`n = 10⁶, 10⁸, 10^{10}` for every `ε` from `10^{-1}` to `10^{-32}` (one chain; `≈ 4(a/B_M − 1) + 3 + …`), where the old formula
has `215 … 376`, `1 750 … 3 380`, `17 000 … 33 600` nats per unit of `ln(1/ε)` (its `√(n·ln(1/ε))`-terms).
(vii) **The constants and the closed form.**  `C_* = 4.646, 8.641, 13.524, 14.789` and `C_*′ = 3.495, 6.560, 10.568, 12.286` at
`u = ½, 1, 2, 4`.  The closed form of Proposition A′ is `≥` (A.1) in all 458 of 486 cases in which its hypothesis holds
(`u ∈ {½, 1, 2}`, `n = 10³ … 10^{10}`, `M ≤ 25`); it is crude (up to 17 times (A.1): the trivial `ϖ` and `c ≥ α/(13n)`).

### 7.4 The nested design, exactly (`q2_04_nest.py` → `out_q2_04_nest.txt`, `out_q2_04_nest_C.txt`, `out_q2_04_nest_S.txt`)

The certified cost of `𝔊_M(n, 0.8715, 0.05)` (the accuracy of Q's §7.3) for `M = 0, 1, 2`: Theorem 11.56 applied level by
level with the exact constants, the real base brackets inside, the slope steps by Q's own class `qscheme.SLevel`
(unchanged level; its error term replaced by `c_S′`), `D′` and the chains by `q2lib`, the blocks of the chains those of
the design.  "proof": every family is the construction of its proposition and nothing else; "min": at every slope
step and drop the cheaper, by certified cost, of the level and the pass-through.  On **every node** the inequality of
the induction, `cost ≤ d·B − σ·min(x, R·d) + E(d, x; ln(1/δ) + d ln 2)` with the error functions of §§2–5, is checked; at
every level built, the bound of its proposition and the lemma for its outer block.  In units of `n·a`:

| `u` | `n` | `M = 0`: exact / bound of Theorem A | `M = 1`: proof / min / bound | `M = 2`: proof / min / bound | Q's design (its §7.3): base; `M = 1` min; `M = 2` min |
|---|---|---|---|---|---|
| 1 | 1 000 | 1.331 / 2.334 | 1.995 / 1.887 / 4.475 | 2.017 / 1.879 / 6.775 | 1.349; 1.349; 1.361 |
| 1 | 2 000 | 1.239 / 1.724 | 1.609 / 1.521 / 2.763 | 1.953 / 1.810 / 3.909 | 1.230; 1.196; 1.196 |
| 1 | 4 000 | 1.011 / 1.382 | 1.263 / 1.196 / 1.844 | 1.526 / 1.414 / 2.377 | 1.152; 1.033; 1.014 |
| 1 | 8 000 | 0.957 / 1.204 | 1.015 / 0.989 / 1.354 | 1.103 / 1.055 / 1.562 | 1.101; 0.938; 0.849 |
| 1 | 16 000 | 0.942 / 1.109 | 0.870 / 0.858 / 1.090 | 0.850 / not run / 1.123 | 1.069; 0.883; 0.756 |
| 2 | 2 000 | 1.034 / 1.228 | 1.106 / 1.075 / 1.454 | 1.290 / 1.215 / 1.789 | |
| 2 | 4 000 | 0.976 / 1.123 | 0.922 / 0.902 / 1.135 | — | |
| 2 | 8 000 | 0.947 / 1.066 | 0.816 / 0.806 / 0.965 | — | |
| ½ | 16 000 | 1.053 / 1.312 | 1.233 / 1.182 / 1.693 | 1.458 / 1.324 / 2.141 | |
| ½ | 64 000 | 0.927 / 1.089 | 0.851 / 0.837 / 1.051 | — | |

(`B_M/a = 1, 0.792, 0.627` at `u = 1`.  All 66 designs of stages A and B are in the output: also `n = 1 400` and `u = 2`,
`n = 1 000`; `u = ½`, `n = 4 000`.)  Reading.  (i) **No violation on 1 567 187 node checks**; least slack of the induction
`56` nats at the chains, `71` at the slope steps, `129` at the drops `D′`; of `ln(1/π†) ≤ ϖ(m; c)` at the chain levels `37`.
(ii) The bound of Theorem A is `96`–`530` nats above the exact value (e.g. `296` at `u = 1`, `n = 16 000`, `M = 0`; `390`
at `M = 1`): as in Q, error terms are worst-case.  (iii) **`M = 0` — the chain on the base bracket — is below `e^{n·a}`
from `n = 8 000` on and below Q's base family from `n = 4 000` on** (`1.011` against `1.152`; `0.942` against `1.069` at
`16 000`): the bounded accuracy no longer costs a `√n`.  (iv) With `M ≥ 1` the design is costlier than Q's at `n ≤ 8 000` — a chain's block
(`570`–`1 000` sites at these sizes) and its `130`–`180` nats are not small against `n·B` there — and cheaper from
`n = 16 000` on (`M = 1`: `0.858` against `0.883`).  At these sizes neither is competitive with the tuned two-level design
of §11.19 (`0.590` at `16 000`); as in Q, the test is of the induction, not of the cost.  (v) Stage C of the script —
`M = 2` at `u = 1`, `n = 16 000`, "proof" variant —: 8 875 094 node checks (1.5 million chain levels, 631 400 slope levels,
11 373 drops built), no violation, least slack of the induction `90` nats; the exact cost is `0.850·na` (Q's "proof"
design with five levels: `0.918`); 24 minutes.  The "min" variant at this size and `M = 2` at `u = 2`, `n = 4 000` were
started and stopped for time.  (vi) Stage S — every `n` from 2 to 200, `M ≤ 2`, `ε ∈ {0.8715, 0.01}`,
`δ ∈ {0.05, e^{-n}}`, both variants, `u ∈ {½, 1, 2}`: 14 328 designs, 207 672 node checks, no violation (least slack `64`
nats).  At these sizes the chains have no level (their blocks are longer than `n`) and the design is the base
bracket at the accuracy `α̲` — never above `2ⁿ` —, so the drop and slope families are also called directly in the
dimension `n`: 7 056 `D′` levels are built and checked (outer blocks of `1, 2, …` sites); no slope level exists yet
(the first one at `n = 202`, `u = 2`).

### 7.5 Proposition Q6(e) (`q2_05_q6e.py` → `out_q2_05_q6e.txt`)

One level with a saturating inner family, tolerance `1`.  Rates `e/h ∈ {0.2, 0.5, 0.8, 1, 1.25, 2, 3}` and `e = 0.97ε*`
(`ε*/h = 4.03, 4.12, 4.46` at `u = ½, 1, 2`; `θ_na(e)/a` from `0.61` down to `2·10^{-4}`).  Types: the epoch schedule
(`(B_m, j/d_m, h/j)`, `m ≤ 8`); one line with `B ∈ {h, 1.5h, a, 3a}` and nine pairs `(σ, R)` (`σ ∈ {0, 0.2, 0.3, 0.5, 0.7, 1}`,
`R ∈ {∞, h/20, h/3, h, 2h}`, `B ≥ σR`); maxima of two to four lines with `R ∈ {h/4, h, 2h}`.  Sizes from the first `n` at
which a level exists to `10⁶`; `x̂` at both ends of `[X₀^e(n), R′n]` and in between; `δ ∈ {0.5, 0.05, 10^{-12}, e^{-n}}`.

| `u` | levels built | violations | least slack of Proposition Q6(e), by rate `e/h = 0.2, 0.5, 0.8, 1, 1.25, 2, 3, 0.97ε*/h` (nats) | error term `c_S^e` | pass-through cases |
|---|---|---|---|---|---|
| ½ | 88 013 | 0 | 6.50, 6.44, 6.53, 6.57, 6.64, 6.99, 8.15, 13.4 | 35.8 … 1 206 | 154 368 |
| 1 | 99 763 | 0 | 4.67, 4.85, 4.86, 4.88, 5.06, 5.57, 6.67, 11.2 | 31.9 … 1 284 | 154 368 |
| 2 | 109 554 | 0 | 3.31, 3.55, 3.56, 3.69, 3.59, 4.23, 5.12, 9.93 | 30.9 … 1 483 | 161 280 |

297 330 levels, no violation, on both sides of `h`.  At every level: accuracy `= x̂` exactly; Lemma Q4(b) at the
rate `e` — `r† ≥ min{n_o − 1, ⌊ρ_e n_o⌋ + 1}`, with equality in some cases, and `ln(1/π†) ≤ n_oθ_na(e) + ln(n_o + 1)`; the
threshold `θ ≥ e^{x̂−1}/2 ≥ 3(n_o+1)e^{2u+e^u+n_oe}`; the range condition `n_oθ_na(e) ≤ R·n_i`; the constants of Lemma U(b);
(2.1); Lemma U(d) (least slack `3.3 … 13.4`).  The proposition is nearly sharp at every rate: the least slack is
`3`–`13` nats against error terms of `31`–`1 483` (the large ones at `e = 0.2h`, where `σ′ ≤ B/e` is large); the worst
cases are lines of slope one at `δ = e^{-n}`.
*Part C — the level of Q6 itself with the smaller error term (Corollary U1).*  The level of Proposition Q6 as built
(ladder capped at `⌈x̂⌉`), types along 13 epochs and off the schedule (`B/h ∈ {1, 1.01, 2, 11}`, `σ ∈ {0, 0.3, 1}`,
`R/h ∈ {1, ⅓, 1/50, ∞}`), `n` up to `10⁶`, `δ` down to `e^{-50n}`: 15 906 levels, no violation of
`ln C_max ≤ nB − σ′x̂ + σ′(1 + c_log(n) + h) + ℓ₀(n, Λ)`; least slack `6.05, 4.55, 3.21` nats at `u = ½, 1, 2` (at `σ = 1`, where the
two error terms coincide; the referee found `2.2` there with other parameters), while Q's `c_S` exceeds the sharper
term by up to `19 … 28` nats (at `σ = 0`).

### 7.6 Tolerances `b > 1` (`q2_06_tolerance.py` → `out_q2_06_tolerance.txt`)

The levels of §5.4.  Proposition D′ with `b ∈ {1, 2.5, 17.3, 45}` (17 types per slope `u`, sizes from the first one to
`10⁶`, `δ` down to `e^{-20n}`): 13 872 levels, no violation; least slack `2.5 … 6.6` nats; accuracy `= 𝒳_D^b` exactly, the
ladder ends at `b`.  Proposition Q6(e) with `b ∈ {2.5, 17.3, 45}`, `e/h ∈ {0.5, 1, 2}` (15 types): 33 282 levels, no
violation; least slack `3.1 … 6.8` nats.  At every level Lemma Q4(b), the constants with `A_n^b`, (2.1) with `q^b`, and
Lemma U(d).

---

## 8. What is not proved; the weakest link

1. **Everything rests on Theorem 11.56 with the abort rule (P)**, on Lemma 11.55(c), (d) = Q3, Q4, on Propositions
   Q1, Q2, Q5, Q6 of Q and on the epoch arithmetic — all quoted.  Theorem 11.56 is used here even farther from the
   parameters at which it was simulated than in Q: a chain is a nest of `n/m ≈ 10²` (at `n = 10⁵`) to `5·10⁶` (at
   `n = 10^{10}`) levels on one path, each with `λ = η = η′ = θ = c ≈ 10^{-3} … 10^{-8}`, a two-rung ladder that ends at
   `x_L = b` exactly, and inner failure probabilities `e^{-Θ(n)}`; the drop `D′` has a polynomial threshold and a ladder
   of `Θ(n)` rungs.  The statement of the theorem covers all of this (its hypotheses are checked item by item in
   §§2–4, 6), and the cost bound "in every run" composes level by level under rule (P) exactly as in the referee's
   argument; but no simulation covers it, and my checks evaluate the *bound* `C_max`, not runs.
2. **The weakest link of the new argument is Proposition T**: the induction over a chain whose length is not
   bounded, with the bookkeeping of `Λ` (the inequality `Λ*(d − m, F_d(Λ)) ≤ Λ*(d, Λ)`, the monotonicity of `U`, the
   deficit term) and the design rule (4.1).  It is tested by the saturated induction step (56 360 levels) and by
   the exact recursion over 11 169 chains — which test the arithmetic at `N ≤ 10⁶`, not the proof.  Second: **Lemma U**,
   on which `D′`, Q6(e), their versions for maxima of lines and with a tolerance, and the sharper constant of Q6 all
   rest; its case analysis (which rungs are capped by the sample) is half a page, unrefereed, and tested on about
   `4·10⁵` levels with saturating families.
3. **The composition at depth is evaluated exactly only for `M ≤ 2`** and `n ≤ 6.4·10⁴` (`M = 2`: `n ≤ 1.6·10⁴`; §7.4), i.e.
   where the design is not yet better than tuned two- or three-level designs.  Where Theorem A says something new (`n ≳ 10⁶`,
   `M = 9 … 32`) it rests on the paper induction and on the one-level and one-chain checks, as in Q.
4. **`n₀` and `C′` of Theorem B are not explicit**, and the constant of its `O((ln n)²)` is crude where it is explicit
   (`M ≤ 1 + ln(k_M + 1)/ln(1+κ)` with the worst-case `κ`; `ℓ̄_T` with the trivial `ϖ` and `c ≥ α/(13n)`).  In numbers
   the second term is `24 … 49` times `(ln n)²` for `n = 10⁶ … 10^{12}` at `u = 1` (§7.3).
5. **The constants of the chain are not optimised.**  `A_T ≈ 230 … 1 000` nats per chain (`u = 1`) is why the new
   bound does not beat Q's below `n ≈ 10⁵` and why the variant without chains is better up to `n ≈ 10⁶`.  Known
   slack: `ϖ(m; c)` against the exact `ln(1/π†)` (`89` nats at `u = 1`, `m = 1 099`; at `u = 2` only the trivial bound
   applies at the block of the design); blocks that grow geometrically along the chain (then `O(ln N)` levels and
   `ln(1/c) = O(ln ln N)`; the induction allows the ratio `ϖ₁/(ϖ₁ − B′)` per level, `ϖ₁` the rate of the block) — not
   written; a non-uniform `c_j ∝ 1/(j+1)` with the slack of the upper levels banked; the smaller threshold of §3,
   remark (3); a chain every few epochs instead of every epoch (§5.4).  None changes the order.
6. **No news on the lower bound and on the true order.**  `√(n ln n)` is an upper bound for this method; what limits
   it now is the rate `c₁/k` of the epoch schedule alone (the business of workstream R).  Between `n·h + ½ ln n`
   (numerical) and `n·h + C_*′√(n ln n)` nothing is known.
7. **Part B gives the levels, not a schedule.**  Proposition Q6(e) and its corollary for maxima of lines are one-level
   statements.  Images that leave the class `0 ≤ σ ≤ 1` are stated, with the two obvious reductions, not resolved;
   Q's drop `D` (bounded threshold) is not extended to maxima of lines — `D′` and the chain are.
8. **The optional part is not done:** the finite-`n` form of step (iii) of the rate proof (outer fraction
   `g/(g + θ_hint(g))`) and the sub-exponential term at extensive accuracies.  (Lemma U would be its tool: the level
   has the form of §2 with an outer rate `g + θ_hint(g) ≥ h`; **[conjecture]** `n·θ_hint(g) + O(√(n ln n))` as in Q §8.)
9. **Not checked:** the Lean proofs behind (R); Harper's theorem, the binomial median, Chernoff–Hoeffding;
   Proposition 11.57(a) (the base bracket: quoted through Q5; its bound at the accuracies `≥ 𝒳_B` is tested at every
   base node of §7.2 B and §7.4, least slack `7.5` nats); slopes other than `u ∈ {½, 1, 2}`; the variant of §5.4 as a
   nest (only its levels, §7.6, and its formula).

---

## 9. What I found wrong or imprecise elsewhere

1. **`Q_REPORT.md` §6.2 (and §8, item 5 in part): "A `√n` remains in any case for this family of algorithms at a
   bounded accuracy [numerical, §2.3]".**  False (Theorem A).  What §2.3 shows is that an outer block of a positive
   fraction of the sites, closed at a bounded threshold, costs `e^{Θ(√n)}` too much.  A bounded accuracy does not
   need such a block: it is reached from the accuracy `≈ ln n` by a chain whose bounded-threshold blocks have
   `Θ(ln n)` sites.  Already at `M = 0`: a bounded accuracy at the non-adaptive exponent costs `e^{n·a + O(ln n)}`
   (measured: *below* `e^{n·a}` from `n ≈ 8·10³` on at `u = 1`, §7.2 B and §7.4), not `e^{n·a + Θ(√n)}` as for the plain
   two-sample bracket.
   The coordinator's sketch in Theorem 11.58a, "What it is not" (ii), is right.
2. **`Q_REPORT.md`, Proposition Q6: the error term is larger than its own level needs** (not an error; Corollary U1):
   `c_S = (B/h)(1 + c_log + h) + ℓ₀` can be replaced by `σ′(1 + c_log + h) + ℓ₀`, `σ′ = σ + B/h − 1`.  With it the limsup
   constant is `C_*′ = 3√(2(1+r̄)c₁) = 0.76·C_*` at `u = 1`.  Independently, **Theorem Q9 does not use what Q6 gives:**
   it charges every slope step `c_S(n, ·; a)`, although `c_S(n, ·; B_m)` with `B_m/h → 1` is what Q6 proves for the late
   epochs, which hold almost all the steps; with Q's own formulas the constant would be `2√(5(1+r̄)c₁) = 0.80·C_*`.
3. **The brief, §2 (T).**  (a) "`c_j` as in Q's schedule" together with "if `n_o·B′ ≥ X + P_cnt + ln 4`, induction gives
   `t_j(d) ≤ d·B′ + E + A`": `P_cnt`, `P_M` depend on the level (through `c_j`, the dimension and `δ`), and the induction
   needs `n_oB′ ≥ X + P_cnt^{(j)} + ln 4 + (P_M^{(j+1)} − P_M^{(j)})` at every level, i.e. `P_cnt` of the *deepest* level
   (`8 ln(n/n_o)` more than at the top with `c_j ∝ 1/j²`) or uniform bounds; §4.3, remark 5.  (b) "below a dimension
   `d₀ = O(ln n)` enumeration": the bottom of the chain then costs `(d₀ − 1)(ln 2 − B′)` with
   `d₀ − 1 ≥ n_o + ⌊X/(2u)⌋`, which is not in the brief's `A = n_o(ln 2 − B′) + P_M + ln 8` and exceeds it when
   `(X/(2u))(ln 2 − B′) > P_M + ln 8` (small `u`); the bound needs `max{A, e₀}`.  (c) `D′` with
   `θ = 3(n_o + 1)e^{2u+e^u}`, `n_o = ⌊φn⌋`, has an accuracy `X(n)` that is not monotone in `n` (`(2p_u)^n` decreases, `n_o`
   jumps), and a family needs one least accuracy for all dimensions below the top: hence the horizon (C1) and
   `θ` computed from a fixed `𝒳`.  (d) The claim itself, the trap and its order are right.
4. **The brief, §3a.**  "`(B/e + 4) ln n + O(1)`" is right and can be read with `σ′ = [B − (1−σ)θ_na(e)]/e` for `B/e`.
   The type map can produce `σ′ > 1` or `σ′ < 0` (§6.2, remark 2), which the one-line derivation in the brief does
   not exclude; and the corollary needs lines that are nonnegative on the range in the sense of (C2) only through
   one line at the dominant rung.
5. **Theory report, Theorem 11.58a.**  Part (b) and "Why `√(n ln n)`": the constant `C_*` is not the best that the
   proof gives (item 2).  "What it is not" (ii): confirmed, with the corrections of item 3; its "levels whose outer
   block … is enumerated" is the trivial bound `π† ≥ 2^{-n_o−1}` — the block is sampled, and Lemma 11.55(c) gives
   less than enumeration once `n_o ≥ m*(ℓ_c)`.
6. **Referee report R12:** nothing found.  Its correction (m6b) of the hypothesis of Lemma Q4(b) is what Lemma U uses.

---

## 10. Files and commands

All in `experiments/workstreams/Q2/`; Python 3 with numpy only; run from that directory, one process at a time.
`experiments/workstreams/Q/qlib.py`, `qscheme.py`, `experiments/reviews/R12/r12lib.py` and (through `qlib`)
`experiments/reviews/R8/r8_flat.py` are imported, nothing in them is changed.  The stored outputs are those of the
final versions of the scripts and of the library: after two late changes of `q2lib.py` that affect no number —
the line `sys.dont_write_bytecode = True`, so that importing the libraries writes no bytecode cache outside this
directory (the cache `experiments/reviews/R12/__pycache__/`, which my first imports had created, was removed), and
a line that empties the referee's cache of base-family arrays (see "Memory") — the scripts were run again (after
the first change all of them; after the second the two that use the base family, `q2_02` B C and `q2_04` A B S) and
reproduced their outputs exactly, apart from the timing fields.  The one exception is `out_q2_04_nest_C.txt`: it is
the first row of a longer run (two designs, both variants) that was stopped after 24 minutes; stage C of the
script now consists of that one design and was not run again.

| file | what | command | time |
|---|---|---|---|
| `q2lib.py` | both evaluators of one level (`Ev`); saturating families; the level of Lemma U; `D′`, the slope step at the rate `e`, the chain (design, exact recursion, bound); families with exact costs for the nest; the formulas (A.1) (`E_new`), (5.2) of Q (`E_old`), §5.4 (`E_trap`), Proposition A′ (`E_new_closed`) | (library) | |
| `q2_01_levels.py` → `out_q2_01_levels.txt` | §7.1: Proposition D′; the induction step of Proposition T | `python3 q2_01_levels.py > out_q2_01_levels.txt` | 2 min |
| `q2_02_chain.py` → `out_q2_02_chain_A.txt`, `out_q2_02_chain_BC.txt` | §7.2: chains by exact recursion (A: saturating; B: the real base family; C: `D′` inside) | `python3 q2_02_chain.py A > out_q2_02_chain_A.txt`; `python3 q2_02_chain.py B C > out_q2_02_chain_BC.txt` | 4 min; 8 min |
| `q2_03_formula.py` → `out_q2_03_formula.txt` | §7.3: the bound of Theorem A against Theorem Q8; the variant without chains; constants; the closed form | `python3 q2_03_formula.py > out_q2_03_formula.txt` | 2 min |
| `q2_04_nest.py` → `out_q2_04_nest.txt`, `out_q2_04_nest_C.txt`, `out_q2_04_nest_S.txt` | §7.4: the nested design exactly, node-by-node checks (stages A: `M ≤ 1`; B: `M = 2`; C: `M = 2` at `n = 16 000`; S: every `n ≤ 200`) | `python3 q2_04_nest.py A B > out_q2_04_nest.txt`; `python3 q2_04_nest.py C > out_q2_04_nest_C.txt`; `python3 q2_04_nest.py S > out_q2_04_nest_S.txt` (`quick` as argument: 10 s) | 6 min; 24 min; 11 s |
| `q2_05_q6e.py` → `out_q2_05_q6e.txt` | §7.5: Proposition Q6(e), maxima of lines; Q6 with the sharper error term | `python3 q2_05_q6e.py > out_q2_05_q6e.txt` | 10 min |
| `q2_06_tolerance.py` → `out_q2_06_tolerance.txt` | §7.6: `D′` and Q6(e) with a tolerance `b > 1` | `python3 q2_06_tolerance.py > out_q2_06_tolerance.txt` | 5 min |

Memory (peak resident size, measured): `0.06` GB (`q2_02` A), `0.15` GB (`q2_01`), `0.20` GB (`q2_06`), `0.26` GB (`q2_05`),
`0.32` GB (`q2_02` B C), `0.07` GB (`q2_04` A B).  The two runs of `q2_02` B C before the second change peaked at `1.7` GB (measured on the
second one) — above the `1.5` GB of the brief, for a few minutes each — because `r12lib.Base` keeps up to 60 arrays of the length of the cube (`1` GB at `10⁶` sites);
`q2lib.HiBase` now empties that cache.  The largest arrays are the tables of one outer cube with up to `10⁶` sites
(float64 logarithms; at most six cached by `qlib`, four by `r12lib`).  Numerical conventions: those of the two evaluators (table
comparisons with tolerance `10^{-12}`); a floor is computed with `+10^{-12}` so that an exact integer is not lost.
