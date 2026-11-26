# Workstream Q — the sub-exponential term of the adaptive exponent without a hint

> **Repository note (added by the coordinator at integration, twenty-second checkpoint of
> cycle 10; the report below is otherwise as delivered).**  Status: **paper proofs,
> re-derived line by line by the coordinator and refereed after delivery (R12,
> `docs/reviews/R12_referee_report.md`: "the main claim survives, with the constants as
> stated"; no major finding; every new statement re-derived; with independent code,
> `experiments/reviews/R12/`, about 220 million node checks of the nested design, 523 000
> one-level checks and 0.9 million checks in exact arithmetic, without a violation).**  The integrated
> statements and their labels are in `docs/THEORY_REPORT.md` §11.19: Lemma 11.55(c), (d)
> (= Lemmas Q3, Q4), Theorem 11.58a (= Theorems Q8, Q9) and remark (2).  Harness XVI.5 tests
> the two lemmas on exact tables, the epoch arithmetic and the accuracies of the two kinds
> of level.  The scripts of §10 were re-run by the coordinator: every number of the stored
> outputs is reproduced (the outputs differ in their timing fields only; the long run
> `q3_scheme_exact.py` was not repeated).
>
> **Errata after the referee report R12** (the text below is unchanged).
> (m1) *Theorem Q(c) and §1.2, the lower bound.*  "`n·h − O(ln n) ≤ ln N`" is stated for
> `0 < δ < 1` and attributed to Theorem 11.25(a),(d), which states neither: Theorem 11.25(a)
> is the finite inequality `E|Q(0)| ≥ (1 − 2δ)·2ⁿ/|B(n, k*)|`, void for `δ ≥ ½`, and (d) gives the
> exponent only.  What holds, by three lines from (a) (the referee's; in the theory
> report): for `δ < ½`, `ln N ≥ n·h − max{1, (ε + ln 2)/u}·ln((1−ρ_h)/ρ_h) − ln(1/(1 − 2δ))`, i.e.
> `n·h − O(1)` (the maximum can be dropped when `(ρ_h − p_u)n ≥ 1 − (ε + ln 2)/u`, and
> numerically always).  The upper bound holds for every `δ < 1`.
> (m2) *§1.2 (T) and the proof of Theorem Q8, "the cost bound holding in every run (abort
> rule)".*  The rule that the nesting needs is: a level counts each of its own queries as
> `1` and each call of an inner procedure with its **certified** bound `C_l`, whatever the
> call uses, and tests **before every query and before every inner call** that the count
> stays at most `C_max`.  With it a nested run costs at most its certified bound in every
> run, and on the good event the test never fires.  The theory report's Theorem 11.56 has
> this wording since this checkpoint (it had "before every inner call", which proves
> `C_max + M̄`; with that wording Theorem Q(a) would lose `ln(1 + k_M/2)` nats and (b), (c)
> nothing).
> (m3) *§0 and §7.4(i), "below `n·a` from `n ≈ 3·10⁴` on":* the crossover of the formula is at
> `n ≈ 2.07·10⁴`.
> (m4) *§7.4(v):* the numbers `1.72, 0.655` are not the closed form of Theorem Q9(b) with the
> `M` of its proof, which gives `1.813, 0.663, 0.3055, 0.2673`.
> (m5) *§7.1, part C:* the column "`Err` proved (2.3)" uses the refined bound of Lemma Q3;
> Corollary Q4a as stated (with `c̄_π`) gives `143.47, 161.56, 246.22, 412.66`.
> (m6) *Wording.*  "`1.83·√n_o` proved" (§0 table, §7.1) is the leading term of Lemma Q3, not
> a bound (the proved bound is `3.64 … 2.08` times `√n_o` in the report's own column, and at
> other parameters the measured value exceeds the leading constant alone); in Lemma
> Q4(b) read "`(1−η)ν₀ ≥ 1`" for "`ν₁ ≥ 1`"; and the constant `C(u, ε, δ)` of Theorem Q(c) is not
> `C_*`, which bounds the limsup only — over `2 ≤ n ≤ 10^{12}` the referee finds
> `sup (bound − nh)/√(n ln n) = 3.8` at `u = 1` and `32` at `u = 4`.

Independent report on the brief `docs/workstreams/Q_brief.md` (twenty-first checkpoint of cycle 10,
2026-11-26).  Paper proofs with numerical checks; no Lean.  Nothing in the repository was edited;
the only files created are this report and the scripts and outputs in `experiments/workstreams/Q/`
(§10).  No git command that changes state was run, nothing was delegated.

Status labels.  **[proved here]** complete proof in this report (paper proof, unrefereed);
**[quoted]** taken from a named statement of the repository, not re-proved (its own status is given);
**[V, quoted]** machine-checked in the repository, statement read, proof not audited;
**[numerical]**; **[heuristic]**; **[conjecture]**.

Notation (theory report §11.16–§11.19, `K_REPORT.md`): `Q_n` the cube, `L_u(Q_n)` the `u`-Lipschitz `ψ`,
`A = 2^{-n}Σ_x e^{-ψ(x)}`; `p = p_u = 1/(1+e^u)`, `Λ₁ = ln(2/(1+e^{-u}))`, `ε* = ln cosh(u/2)`,
`a = KL(p_u‖½)`, `ρ_h = Λ₁/u`, `h = KL(ρ_h‖½)`, `H` the binary entropy;
`θ_na(e) = KL(ρ_e‖½)` with `ρ_e ∈ [p_u, ½]` the solution of `KL(ρ‖p_u) = min(e, ε*)`;
`B(m,r)` Hamming ball, `E_r(m) = Σ_{j≤r} C(m,j)(e^{u(r+1−j)} − 1)`, `T_m(k) = Σ_j C(m,j)e^{-u(j−k)₊}`,
`Γ̃`, `κ`, `Γ″`, `r†`, `π†` as in `K_REPORT.md` §2.1.  `N(n; ε, δ)` is the least `C` such that some randomised
adaptive algorithm without a hint makes at most `C` evaluations in every run on every `ψ ∈ L_u(Q_n)` and is
`(ε/2, δ)`-correct on the class.  All logarithms are natural; "nats" are units of `ln(cost)`.

---

## 0. The result in one page

> **Theorem Q [proved here, given Theorem 11.56 (paper proof, refereed), Lemma 11.55(a)–(c), Proposition 11.57(a)
> (paper proofs) and the arithmetic of `RateFull.lean` (machine-checked)].**  Fix `u > 0`.  Let
> `d_0 = h/(a−h)`, `J_m = ⌈d_m⌉`, `d_{m+1} = d_m(J_m a + h)/(J_m a − h d_m)`, `k_0 = 1`, `k_{m+1} = k_m + J_m + 1`
> (the epoch sequences of the machine-checked rate) and `B_m = h(1 + 1/d_m)`, so that
> `B_m − h ≤ c₁/(k_m + c₂)`, `c₁ = h(1+κ)/κ`, `c₂ = (a+h)(2a−h)/(ha) − 2`.
>
> (a) *Explicit, every `n`.*  For every `n ≥ 1`, `ε > 0`, `0 < δ < 1` and every number of epochs `M ≥ 0` there is
> an explicit design with `k_M` nested levels of Algorithm 2L⁺ over the two-sample bracket — every parameter
> a closed formula in `(u, n, ε, δ, M)`, and where two admissible procedures are on offer the one with the smaller
> certified bound — which returns a bracket of ratio at most `e^ε` around `A` with probability at least `1 − δ` and
> makes, in every run and at every member of `L_u(Q_n)`, at most
>
>     exp( n·B_M + 𝓔_M(n, ε, δ) )         evaluations,
>
> where `𝓔_M` is the explicit error term (5.2).  As long as `(k_M − 1)·O(ln n) ≤ n` it satisfies (Proposition Q9a)
> `𝓔_M ≤ C₁(u, ε)·√n + (k_M − 1)·ℓ_S(n, δ) + M·ℓ_D + ℓ_B`, with `ℓ_S(n, δ) = (a/h + 4)·ln n + O_{u,δ}(1)`,
> `ℓ_D, ℓ_B = O(ln n + ln(1/ε) + ln M)` and `C₁ = u·[√(ℓ⁰/2) + Σ_m √(φ_m ℓ_m/2)·B_{m+1}/a]` a convergent series
> (`C₁ ≈ 5.5` at `u = 1`, `ε = 1`).
>
> (b) *The order.*  For every fixed `ε > 0` and `0 < δ < 1`
>
>     limsup_{n→∞}  ( ln N(n; ε, δ) − n·h ) / √(n·ln n)   ≤   C_*(u) := 2·√( (1 + r̄)·c₁·(a/h + 4) ),     r̄ = (2a−h)/(a−h)
>
> (`C_* = 4.65, 8.64, 13.5` for `u = ½, 1, 2`), and the same holds for accuracies `ε_n ≥ n^{-A}` with a constant
> that depends on `A`.
>
> (c) Hence for every `u > 0`, `ε > 0`, `0 < δ < 1` there is `C` with
> `N(n; ε, δ) ≤ exp( n·h + C·√(n·ln n) )` for all `n ≥ 2`; with the lower bound of Theorem 11.25(a),
> `n·h − O(ln n) ≤ ln N(n; ε, δ) ≤ n·h + O(√(n ln n))`.

So the goal of the brief is met with room to spare: the method gives the exponent **`½`** of `n` (not `¾`)
and `½` of `ln n`.  Evaluated from the formula (5.2) at `u = 1`, `ε = 1`, `δ = 0.05`, the bound of (a) at the
best `M` is `0.71·na` at `n = 6.4·10⁴` (13 levels), `0.37·na` at `10⁶` (43 levels), `0.273·na` at `10⁸` and
`0.2637·na` at `10^{10}` (`h = 0.2626·a`); it is below the non-adaptive exponent `n·a` from `n ≈ 3·10⁴` on;
`(bound − nh)/√(n ln n)` lies between `2.4` and `3.8` for `1.6·10⁴ ≤ n ≤ 10^{12}`, while `(bound − nh)/n^{3/4}` falls
from `1.0` to `0.013` (§7.4).  The exact certified cost of the design was evaluated for three nested levels up
to `n = 6.4·10⁴`, five up to `1.6·10⁴` and seven up to `4·10³`; on the `3.8·10⁶` nodes of these nests every inequality
of the induction holds (§7.3).

**Why the heuristic `n^{3/4}` of §11.19(2) is too pessimistic.**  It assumed that each of the `≈ 1/η` levels
is a *bounded* level and loses `e^{O(√n)}`.  In the recursion whose rate is proved — the epochs of the remark
after Theorem 11.53 — there are two kinds of level:

* the **slope steps** (step (i) of that proof: outer fraction `g/h` at the accuracy rate `g`) are run at an
  accuracy `x ≫ ln n`, on an outer block of only `≈ x/h` coordinates, with the closure threshold
  `θ = e^{x − O(1)}`.  At such a `θ` the closing radius is `ρ_h·n_o` (Lemma Q4), *not* `p_u n_o − Θ(√n_o)`, and the
  outer sample costs `e^{n_o h}` up to a factor `n_o + 1`: a slope step loses a **polynomial** factor,
  `(a/h + 4)·ln n + O(1)` nats (Proposition Q6);
* the **drops** (step (ii): a fixed outer fraction) are the only levels that work at a bounded `θ` and lose
  `e^{O(√n_o)}` (Proposition Q7) — but there is one drop per epoch, the number of epochs up to level `k` is
  `O(ln k)`, and their outer fractions decrease geometrically, so that all the `√`-losses together are
  `C₁√n` with `C₁` *independent of the number of levels*.

Hence `E_k = C₁√n + O(k·ln n)` instead of `O(k·√(n ln n))`, and `n·c₁/k + k·ln n` is optimised at
`k ≈ √(n/ln n)`.  Nothing is non-uniform in `k`; the three places where a careless schedule would lose
uniformity (accuracies halved at every bounded level, failure probabilities, ladders of a fixed number of
rungs) and their repairs are listed in §5.3.

**Answers to the questions of the brief** (details in the sections named).

| question | answer |
|---|---|
| finite-`n` form of one level | Corollary Q4a: `ln C_max ≤ max{n_o·ω, max_l[min(n_o·ω, x_{l−1}) + ln C_l]} + ln(L+2) + max{P_M + c_π, P_cnt}`, with `(ω, c_π) = (a, u√((n_o/2)ln(2e^{u(m₀+2)}/θ)) + O(1))` at a bounded `θ` and `(θ_na(e), ln(n_o+1))` at an extensive one; `P_M`, `P_cnt` explicit polynomial factors (§2) |
| how large is the `O(√d)` of `M̄` | proved: `u·√((n_o/2)·ln(2e^{u(m₀+2)}/θ))` (Lemma Q3; the constant `u + ln 4` of Lemma K.4(d) improved to `u`); at `u = 1`, `θ = η = 0.05`: `1.83·√n_o` proved, `1.30…1.53·√n_o` measured (`n_o = 3.2·10⁴ … 500`) |
| what the failure probability `δ′ = δ/(4LM̄)` costs the levels below | only a factor `≈ ln(1/δ′)/ln(1/δ)` in their `K`, i.e. at most `ln n + O(1)` nats per level, whatever the depth: along a chain of nested levels `Σ ln M̄ ≤ n ln 2 + k·O(ln n)`, because the outer blocks are disjoint (Lemma Q2(d), §5.3) |
| the base family | `ln cost ≤ d·a + u√((d/2)·ln(2e^{3u+x/2}/(e^{x/2}−1))) + O(ln(d/x) + ln ln(1/δ))` for every `x > 0`, `δ`; and `≤ d·θ_na((x − c′_d)/d) + O(ln d)`, `c′_d = 2 ln(d+1) + O(1)`, at extensive accuracies (Proposition Q5) |
| the ladder | an arithmetic ladder of step `1`, capped at the level's own accuracy, loses at most `1` nat and has `≤ hn + 2` rungs (their number enters only through `ln L`); a ladder of ratio `ρ` loses its gap `(ρ − 1)x_l` at the rung that carries the maximum (§2.5, §7.1) |
| is `E_k = O(k·√(d ln d))`; anything not uniform in `k` | better: `E_k ≤ C₁√d + (k−1)(a/h + 4)·ln d·(1 + o(1))`; uniform in `k` (Theorem Q8, Proposition Q9a) |
| which exponent with which rate | with the **proved** rate `c₁/(k + c₂)`: `n·h + O(√(n ln n))` (**proved**, Theorem Q9); with a rate `C/k²` *for an explicit schedule whose levels lose `O(ln n)`* the level term would drop to `O(n^{1/3}(ln n)^{2/3})` and the bound would be `n·h + O(√n)` (**conjecture**; the `0.65a/k²` is numerical and concerns the exact recursion, for which no such schedule is known) |
| the route of the brief (induction on the exact `T_k`) | not needed and not carried out; why it would give `n^{3/4}` at best is explained in §6.3 **[heuristic]** |

---

## 1. Setting and what is quoted

### 1.1 Four facts about the functions of the cube **[proved here; (F1) is (11.18.1)]**

* **(F1)** `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁` for `0 ≤ ρ ≤ 1` (expand `−ln p_u = u + ln(1+e^{-u})`,
  `−ln(1−p_u) = ln(1+e^{-u})`); equivalently `uρ + ln(1+e^{-u}) − H(ρ) = KL(ρ‖p_u)`.
* **(F2)** `p_u < ρ_h < ½`, `KL(ρ_h‖p_u) = KL(ρ_h‖½) = h`, hence `θ_na(h) = h`.  (By (F1) at `ρ = ρ_h`, where
  `uρ − Λ₁ = 0`; `ρ_h < ½` because `2 < e^{u/2} + e^{-u/2}`; `ρ_h > p_u` because (F1) at `ρ = p_u` gives
  `Λ₁ − u p_u = a > 0`; `KL(·‖p_u)` is increasing on `[p_u, ½]`.)
* **(F3)** `0 < h < a < ln 2` (`KL(·‖½)` is strictly decreasing on `[0, ½]`) and `h ≤ u²/16`, hence `h ≤ u`.
  (`½ − ρ_h = ε*/u ≤ u/8` and `KL(ρ‖½) ≤ χ²(ρ‖½) = 4(ρ−½)²`; for `u > 16` use `h < ln 2`.)
* **(F4)** `θ_na` is convex and nonincreasing on `[0, ∞)`, and `a − θ_na(t) ≤ u·√(t/2)`.  (On `(0, ε*)`:
  `θ_na′(e) = z/(z + u)` with `z = ln(ρ_e/(1−ρ_e)) ∈ (−u, 0)` increasing in `e`; the slope of `KL(·‖½)` on `[p_u, ½]` is at
  least `−u`, so `a − θ_na(t) ≤ u(ρ_t − p_u)`, and `2(ρ_t − p_u)² ≤ KL(ρ_t‖p_u) ≤ t` by Pinsker.)

Two elementary bounds used repeatedly: `C(m,r) ≥ (m+1)^{-1}e^{m H(r/m)}`, and `KL(q‖p) ≤ χ²(q‖p) = (q−p)²/(p(1−p))`.

### 1.2 What is quoted

* **(T) Theorem 11.56 = Theorem K1 [quoted; paper proof, refereed R8, not machine-checked], with the constants
  of `K_REPORT.md` §2.2.**  For `n ≥ 2`, `1 ≤ n_o ≤ n−1`, `n_i = n − n_o`, `0 < λ ≤ 1`, `0 < η ≤ ½`, `0 < η′ ≤ 1`, `θ > 0`, `ν₁ ≥ 1`,
  tolerance `b > 0`, failure probability `δ`, and a ladder `x₀ := 2un_i > x₁ > … > x_L`, `L ≥ 1`, `x_L ≤ b`, put

      J = ⌈(2un + b + n_o ln 2)/λ⌉,      ν₀ = (1−η)^{-1}·max{(J+1)(e^λ−1)/η′, ν₁},      c_η = (1−η)/(1+η),
      m_max = ⌈log₂(2(1+η)e^λν₀/((1−η)π†))⌉,      K = ⌈3(1+η)η^{-2}·ln(2(J+1)(m_max+1)(L+2)/δ)⌉,
      ν = Kν₀,   M† = K/((1−η)π†),   M̄ = 2(1+η)e^λν₀M†,   δ′ = δ/(4LM̄),   cnt(x) = max{K, 2(1+η)²(1−η)^{-1}e^λ ν e^x},

  where `π† = 2^{-n_o}|B(n_o, r†)|` (`2^{-n_o−1}` if `r† = −1`) and `r†` is the largest `r ∈ {0,…,n_o−1}` such that
  `[N] Γ̃(r′) ≤ θ(1−η)ν₀` and `[P] min{Γ̃(r′)/c_η, Γ″(r′)} ≤ θ` for all `0 ≤ r′ ≤ r` (`−1` if none), all on `Q_{n_o}`.  If
  `I_1,…,I_L` are bracket procedures for dimension `n_i`, `I_l` of accuracy `x_l`, failure probability at most `δ′`
  and cost at most `C_l` in every run, then Algorithm 2L⁺ is a bracket procedure for dimension `n` with failure
  probability `δ`,

      accuracy  x_out = ln[(2p_u)^n + e^b(e^λ(1+η)/(1−η) + η′ + θ)],        cost  C_max = 1 + 2M̄ + Σ_{l=1}^{L} min{2M̄, (J+1)·cnt(x_{l−1})}·C_l,

  the cost bound holding in every run (abort rule).  *Nesting* (§11.19, remark (1b)): such a run is itself an
  admissible inner procedure with cost `C_max`, and `C_max` is nondecreasing in every `C_l`.
* **(L) Lemma 11.55 = Lemma K.4(a),(b),(c) [quoted; paper proof, checked on exact tables for `m ≤ 12 800`].**
  With `m₀ = ⌈u^{-1}ln(1/c_η)⌉`: (a) `Γ̃(r) ≤ 2e^u m` for `0 ≤ r ≤ p_u(m+1)`; (b) `Γ″(r) ≤ 2e^{u(m₀+2)}·exp(−2(p_u m − r)²/m)` for
  `0 ≤ r ≤ p_u m`; (c) if `0 < θ ≤ 2e^{u(m₀+2)}` and `ν₀ ≥ 2e^u m/(θ(1−η))`, then `r† ≥ ⌊p_u m − √((m/2)ln(2e^{u(m₀+2)}/θ))⌋` if this
  is `≥ 0`.  (Their proofs rest on Harper's theorem, the binomial median and Hoeffding's inequality.)
* **(B) Proposition 11.57(a) = Proposition K0 [quoted; paper proof].**  For `d ≥ 1`, `x > 0`, `0 < δ < 1` let
  `η = min(½, tanh(x/4))`, `K = ⌈3(1+η)η^{-2} ln(4/δ)⌉`, `r*` the largest radius `≤ d−1` with
  `ln(1 + Γ″_d(r′)) ≤ x − ln((1+η)/(1−η))` for all `r′ ≤ r*`, `M = ⌈K2^d/((1−η)|B(d,r*)|)⌉`.  The two-sample bracket with two
  samples of size `M` is a bracket procedure of accuracy `x`, failure probability `δ` and cost `2M`.
* **(R) The epoch arithmetic [V, quoted: `ScienceR13.closed_form`, `epoch_gain` in `proofs/Frontiers/RateFull.lean`].**
  For the sequences of Theorem Q: `d_m ≤ J_m < d_m + 1`, `J_m a − h d_m > 0`, `d_{m+1} − d_m ≥ (J_m + 1)κ`,
  `κ = h²a/((a−h)(a+h)(2a−h))`, and `h/d_m ≤ c₁/(k + c₂)` for `k_m ≤ k < k_{m+1}`.  (Only this arithmetic is used, not
  the theorems about the recursion; `qlib.selftest` re-checks it numerically for 40 epochs at `u = ½, 1, 2, 5`.)
  With `B_m = h(1 + 1/d_m)`: `B_0 = a` and `B_{m+1} = B_m·J_m a/(J_m a + h)` (one line of algebra).
* The lower bound `ln N ≥ n·h − O(ln n)` is Theorem 11.25(a),(d) **[V, quoted]**; it is not used for the upper bound.

### 1.3 Certified families

A *certified family* `𝔉` with least accuracy `x_min > 0` assigns to every `d ≥ 1`, `x ≥ x_min`, `0 < δ < 1` a bracket
procedure `𝔉(d, x, δ)` for `L_u(Q_d)` of accuracy at most `x` and failure probability at most `δ`, together with a
number `b_𝔉(d, x, δ)` such that the procedure makes at most `exp(b_𝔉(d, x, δ))` evaluations in every run.  All
designs below are fixed before any evaluation; "the cheaper of two procedures" always means: the one with the
smaller certified bound `b`.

---

## 2. One level at finite `n`

Throughout this section the setting and constants are those of (T).  Write

    Λ := ln(2M̄),     P_M := ln(4(1+η)e^λ/(1−η)) + ln ν₀ + ln K,     P_cnt := ln(J+1) + ln(2(1+η)²e^λ/(1−η)) + ln ν₀ + ln K.

### 2.1 The decomposition

**Proposition Q1 [proved here].**  `Λ = P_M + ln(1/π†)`, `ln((J+1)·cnt(x)) = x + P_cnt` for every `x ≥ 0`,
`P_M = P_cnt − ln(J+1) − ln((1+η)/2) ≤ P_cnt`, and with `t_l := min{Λ, x_{l−1} + P_cnt} + ln C_l`

    max{Λ, max_l t_l}  ≤  ln C_max  ≤  ln(L+2) + max{Λ, max_{1≤l≤L} t_l}.

*Proof.*  `2M̄ = 4(1+η)e^λν₀K/((1−η)π†)`.  In `cnt` the second entry is at least `K` for `x ≥ 0`, because `ν = Kν₀`,
`ν₀ ≥ ν₁/(1−η) > 1` and `2(1+η)²e^λ/(1−η) > 2`.  `J ≥ 1` and `(1+η)/2 ≥ ½` give `P_M ≤ P_cnt`.  `C_max` is a sum of `L + 2` terms,
`1 ≤ 2M̄` and `e^{t_l}`.  ∎

So the whole dependence of a level on the instance class is in `ln(1/π†)`; the "error" of a level is
`ln(L+2)`, the two polynomial factors `P_M`, `P_cnt`, and the excess of `ln(1/π†)` over its exponent.

### 2.2 The polynomial factors and the failure probability handed down

**Lemma Q2 [proved here].**
(a) `J ≤ (2un + b + n_o ln 2)/λ + 1`.
(b) `π† ≥ 2^{-n_o−1}`, hence `m_max ≤ log₂(2(1+η)e^λν₀/(1−η)) + n_o + 2`.
(c) `K ≤ 3(1+η)η^{-2}·[ln(1/δ) + ln(2(J+1)(m_max+1)(L+2))] + 1`.
(d) `ln(1/δ′) = ln(1/δ) + ln(2L) + Λ ≤ ln(1/δ) + ln(4L) + P_M + n_o ln 2`; equivalently

    ln(1/δ′) + n_i·ln 2  ≤  [ ln(1/δ) + n·ln 2 ]  +  ln(4L) + P_M.                                          (2.1)

*Proof.*  (b) `r† ≥ −1` by definition.  (d) `ln M̄ = Λ − ln 2 = P_M + ln(1/π†) − ln 2 ≤ P_M + n_o ln 2`.  ∎

*Reading.*  `P_cnt ≈ ln(J·ν₀·K)` with `J ≈ (2u + φ ln 2)n/λ`, `ν₀ ≈ max{J(e^λ−1)/η′, ν₁}/(1−η)` and
`K ≈ 3(1+η)η^{-2}(ln(1/δ) + ln(n²L/λ))`: the factors `1/λ`, `1/η²`, `1/η′`, `ν₁` (which is `2e^u n_o/θ` at a bounded `θ`) enter
`ln C_max` through logarithms only, and `δ` through `ln ln(1/δ)`.  The failure probability that is handed down is
exponentially small, `ln(1/δ′) ≈ ln(1/δ) + ln M̄`, and all it costs the level below is the factor
`ln(1/δ′)/ln(1/δ)` in *its* `K`.  The form (2.1) is what makes this uniform over nested levels: the quantity
`ln(1/δ) + (dimension)·ln 2` increases by `ln(4L) + P_M = O(ln n)` per level and by nothing else, because the
`n_o ln 2` that the outer sample adds to `ln(1/δ′)` is taken out of the dimension.  At depth `k` therefore
`ln(1/δ) ≤ ln(1/δ_top) + n ln 2 + k·O(ln n)`, and every `K` in the nest is `O(n + k ln n + ln(1/δ_top))`.

### 2.3 The outer sample at a bounded `θ`

**Lemma Q3 [(c) of (L) quoted; the bound proved here — it replaces the constant `u + ln 4` of Lemma K.4(d) by `u`].**
Let `m ≥ 1`, `0 < η ≤ ½`, `0 < θ ≤ 2e^{u(m₀+2)}`, `ν₀ ≥ 2e^u m/(θ(1−η))`, `ℓ ≥ ln(2e^{u(m₀+2)}/θ)` and
`m*(ℓ) := ((√(ℓ/2) + √(ℓ/2 + 2p_u))/p_u)²`.  Then on `Q_m`

    ln(1/π†)  ≤  m·a + c̄_π(m; ℓ),      c̄_π(m; ℓ) := max{ ln 2 + m*(ℓ)·H(p_u) ,  u(1 + √(mℓ/2)) + (4/(3p_u))(ℓ + 2) + ln(m+1) }.

More precisely, if `s := √((m/2)·ln(2e^{u(m₀+2)}/θ)) ≤ p_u m/2 − 1`, then
`ln(1/π†) ≤ m·a + u(1+s) + (4/(3p_u))(ln(2e^{u(m₀+2)}/θ) + 2/m) + ln(m+1)`.

*Proof.*  Let `ℓ₁ = ln(2e^{u(m₀+2)}/θ) ≤ ℓ` and `s = √(mℓ₁/2)`.  *Case `s ≤ p_u m/2 − 1`* (true whenever `m ≥ m*(ℓ)`: the
inequality `(p_u/2)y² − √(ℓ/2)·y − 1 ≥ 0` in `y = √m` holds from its positive root on).  Then
`r₊ := ⌊p_u m − s⌋ ≥ p_u m − s − 1 ≥ p_u m/2 ≥ 0`, so `r† ≥ r₊` by (L)(c) and
`π† ≥ 2^{-m}C(m, r₊) ≥ (m+1)^{-1}exp(−m·KL(ρ₊‖½))`, `ρ₊ = r₊/m ∈ [p_u/2, p_u]`.  For `f = KL(·‖½)`: `f′(p_u) = −u`,
`f″(ξ) = 1/(ξ(1−ξ)) ≤ 8/(3p_u)` on `[p_u/2, p_u]` (`ξ(1−ξ) ≥ (p_u/2)(1 − p_u/2) ≥ 3p_u/8`), so by Taylor's formula
`f(ρ₊) ≤ a + u(p_u − ρ₊) + (4/(3p_u))(p_u − ρ₊)²`; and `0 ≤ m(p_u − ρ₊) ≤ s + 1`, `(s+1)² ≤ 2s² + 2 = mℓ₁ + 2`.
*Case `s > p_u m/2 − 1`:* then `m < m*(ℓ)` and, by Lemma Q2(b), `ln(1/π†) ≤ (m+1)ln 2 = m·a + m·H(p_u) + ln 2`.  ∎

`c̄_π(m; ℓ)` is nondecreasing in `m` and in `ℓ`.  At `u = 1`, `η = θ = 0.05` (`m₀ = 1`, `ℓ₁ = 6.69`) the leading term is
`1.83·√m`; exact tables give `ln(1/π†) − m·a = 1.53·√m` at `m = 500` and `1.30·√m` at `m = 32 000` (§7.1, parts B, B′).  So
a term of order `√m` is really there at a bounded `θ` **[numerical]**: `Γ″(r)` is of the order of
`P(Bin(m, p_u) ≤ r)`, which is below a small `θ` only for `r ≤ p_u m − Θ(√(m ln(1/θ)))`.

### 2.4 The outer sample at an extensive `θ`

**Lemma Q4 [proved here].**  Let `m ≥ 1`, `e ≥ 0`, and `ρ_e ∈ [p_u, ½]` as in the notation.
(a) For every integer `0 ≤ r ≤ min(m, ρ_e m + 1)`:  `Γ̃_m(r) ≤ (m+1)·e^{2u + e^u}·e^{m·e}`.
(b) Let `0 < η ≤ ½`, `ν₁ ≥ 1` and `θ ≥ c_η^{-1}·(m+1)·e^{2u + e^u + m·e}`.  Then on `Q_m`

    r† ≥ min{m − 1, ⌊ρ_e m⌋ + 1}      and      ln(1/π†) ≤ m·θ_na(e) + ln(m+1).

*Proof.*  (a) `Γ̃(0) = e^u − 1`.  For `1 ≤ r ≤ p_u(m+1)`, (L)(a) gives `Γ̃(r) ≤ 2e^u m ≤ (m+1)e^{2u+e^u}` (`2 < e ≤ e^{u+e^u}`).
For `r > p_u(m+1)` put `ρ′ = (r−1)/m`, so `p_u − (1−p_u)/m < ρ′ ≤ ρ_e`.  As `E_r(m) ≤ e^{u(r+1)}Σ_j C(m,j)e^{-uj} = e^{u(r+1)}(1+e^{-u})^m`
and `|B(m, r−1)| ≥ C(m, r−1) ≥ (m+1)^{-1}e^{mH(ρ′)}`, (F1) gives

    Γ̃(r) ≤ (m+1)·e^{2u}·exp(m·KL(ρ′‖p_u))                                                                 (2.2)

(this is (3.0) of `K_REPORT.md`).  If `ρ′ ≥ p_u`, then `KL(ρ′‖p_u) ≤ KL(ρ_e‖p_u) ≤ e`.  If `ρ′ < p_u`, then
`KL(ρ′‖p_u) ≤ (p_u − ρ′)²/(p_u(1−p_u)) < (1−p_u)/(p_u m²) = e^u/m²`, so `m·KL(ρ′‖p_u) ≤ e^u`.
(b) Let `r₁ = min{m−1, ⌊ρ_e m⌋ + 1}`.  For `r′ ≤ r₁`, (a) gives `Γ̃(r′) ≤ c_η θ`: [P] holds through its first entry, and
[N] holds because `(1−η)ν₀ ≥ ν₁ ≥ 1 ≥ c_η`.  So `r† ≥ r₁`.  If `r₁ = m − 1` or `r₁ > m/2`, then `|B(m, r₁)| ≥ 2^{m−1}` and
`ln(1/π†) ≤ ln 2 ≤ ln(m+1)`.  Otherwise `ρ_e ≤ r₁/m ≤ ½`, `|B(m, r₁)| ≥ C(m, r₁) ≥ (m+1)^{-1}e^{mH(ρ_e)}`, and
`ln(1/π†) ≤ m(ln 2 − H(ρ_e)) + ln(m+1)`.  ∎

So at `θ = e^{Θ(m)}` the outer sample costs `exp(m·θ_na(e))` up to the factor `m + 1`, with
`e = (ln(c_η θ) − ln(m+1) − 2u − e^u)/m`: the polynomial slack `(m+1)e^{2u+e^u}` in `θ` is the whole loss.  The lemma is
sharp at `m = 1` (slack `0.0000` in the table of §7.1, part D) and has a slack of `5`–`18` nats at `m = 64 000`.
For the slope steps `e = h`, and `θ_na(h) = h` by (F2).

### 2.5 The one-level inequality in the form of the brief

**Corollary Q4a [proved here from (T), Q1, Q3, Q4].**  For every level of Algorithm 2L⁺

    ln C_max  ≤  max{ n_o·ω ,  max_{1≤l≤L} [ min(n_o·ω, x_{l−1}) + ln C_l ] }  +  ln(L+2)  +  max{ P_M + c_π , P_cnt },          (2.3)

where
* *bounded `θ`* (hypotheses of Lemma Q3 with `m = n_o`):  `ω = a`, `c_π = c̄_π(n_o; ln(2e^{u(m₀+2)}/θ))`;
* *extensive `θ`* (`θ ≥ c_η^{-1}(n_o+1)e^{2u+e^u+n_o e}`, `e ≥ 0`):  `ω = θ_na(e)`, `c_π = ln(n_o+1)`.

*Proof.*  `Λ = P_M + ln(1/π†) ≤ n_o ω + P_M + c_π` and `min(Λ, x_{l−1} + P_cnt) ≤ min(n_o ω, x_{l−1}) + max{P_M + c_π, P_cnt}`; then
Proposition Q1.  ∎

*The ladder.*  If the costs obey `ln C_l ≤ n_i·T(x_l/n_i)` for a nonincreasing `T`, then
`min(n_oω, x_{l−1}) + ln C_l ≤ (x_{l−1} − x_l) + [min(n_oω, x_l) + n_i T(x_l/n_i)]`: a rung costs its **gap** on top of the
bracket of (11.18.2) at `γ = x_l/n` — no continuity of `T` is needed for this.  A geometric ladder of ratio `ρ` has the gap
`(ρ − 1)x_l`, which is extensive at the rung that carries the maximum once that rung is extensive (in the design
of §7.1 the gap there is `68 … 1160` nats, and the maximum sits at such a rung from `n = 4000` on); an arithmetic
ladder of step `1` below a cap `X` has `L ≤ X + 1` rungs, gap `1`, and `L` enters (2.3) only through `ln(L+2)` and
through `ln L` inside `K` and `δ′`.  The designs of §4 use such ladders, with the cap at the level's own accuracy
(slope step) or at the end `R·n_i` of the range of slope one (drop), where the multiplier `min{2M̄, ·}` has already
changed to the sample cap.

---

## 3. The base family

`𝔊_0(d, x, δ)` is the two-sample bracket of (B), or the enumeration of the cube (`2^d` evaluations, an exact
bracket) if no radius qualifies or if `2M ≥ 2^d`; `b_{𝔊_0} = ln min(2M, 2^d)`.

**Proposition Q5 [proved here from (B), (L)(b) and Lemma Q4(a)].**
(a) *Every accuracy.*  For all `d ≥ 1`, `x > 0`, `0 < δ < 1` and every `Λ ≥ ln(1/δ)`:

    b_{𝔊_0}(d, x, δ)  ≤  d·a + E_base(d, x; Λ),
    E_base(d, x; Λ) := ln(8K̄₀(x, Λ)) + max{ m*(ℓ⁰_x)·H(p_u) ,  u(1 + √(dℓ⁰_x/2)) + (4/(3p_u))(ℓ⁰_x + 2) + ln(d+1) },
    K̄₀(x, Λ) := 3(1+η_x)η_x^{-2}(ln 4 + Λ) + 1,   η_x = min(½, tanh(x/4)),   ℓ⁰_x := ln₊( 2e^{3u + min(x/2, ln 3)}/(e^{x/2} − 1) ).

`E_base` is nondecreasing in `d` and `Λ` and nonincreasing in `x`; for `x ≤ 1`:
`E_base ≤ u√((d/2)(ln(4/x) + 3u + ½)) + O(ln(d/x) + ln(1 + Λ))`.
(b) *Extensive accuracies.*  Let `x ≥ 2 ln 3`, `e ≥ 0` and `x ≥ ln 12 + 2 ln(d+1) + 2u + e^u + d·e`.  Then
`b_{𝔊_0}(d, x, δ) ≤ d·θ_na(e) + ln(8K) + ln(d+1)`, `K = ⌈18 ln(4/δ)⌉`.  Consequently, with `c′_d := ln 12 + 2 ln(d+1) + 2u + e^u`
and all `x ≥ max(c′_d, 2 ln 3)`:  `b_{𝔊_0}(d, x, δ) ≤ d·θ_na(x/d) + u√(d·c′_d/2) + ln(8K(d+1))`.

*Proof.*  (a) Put `y = x − ln((1+η)/(1−η))` and `θ_x = e^y − 1`.  As `ln((1+η)/(1−η)) = min(x/2, ln 3)`, `y ≥ x/2` and
`θ_x ≥ e^{x/2} − 1`; `m₀ < u^{-1}min(x/2, ln 3) + 1`, so `ℓ₁ := ln₊(2e^{u(m₀+2)}/θ_x) ≤ ℓ⁰_x`.  If `d ≥ m*(ℓ⁰_x)`, then
`s := √(dℓ₁/2) ≤ p_u d/2 − 1` and `r₊ := ⌊p_u d − s⌋ ∈ [p_u d/2, d−1]`; for `r′ ≤ r₊`, (L)(b) gives
`Γ″(r′) ≤ 2e^{u(m₀+2)}e^{-2s²/d} = 2e^{u(m₀+2)}e^{-ℓ₁} ≤ θ_x`, i.e. `ln(1 + Γ″(r′)) ≤ y`: `r* ≥ r₊`.  As in the proof of Lemma Q3,
`2^d/|B(d, r₊)| ≤ exp(d·a + u(1+s) + (4/(3p_u))(ℓ₁ + 2/d) + ln(d+1))`.  Finally `M ≤ K2^d/((1−η)|B(d,r*)|) + 1 ≤ 4K·2^d/|B(d, r₊)|`
(the fraction is at least `K ≥ 1`, and `η ≤ ½`) and `K ≤ K̄₀(x, ln(1/δ))`.  If `d < m*(ℓ⁰_x)`: the cost is at most
`2^d = e^{d·a + d·H(p_u)}`.  The bound for `x ≤ 1` uses `e^{x/2} − 1 ≥ x/2`, i.e. `ℓ⁰_x ≤ ln(4/x) + 3u + ½`.
(b) `η = ½`, `c_η = ⅓`.  For `r ≥ 1`, `T_d(k) ≥ |B(d,k)|` and `|B(d, κ(r))| ≥ |B(d, κ(r)+1)|/(d+1) > c_η|B(d, r−1)|/(d+1)` give
`Γ″(r) ≤ 3(d+1)Γ̃(r)`, and `Γ″(0) ≤ e^u − 1`.  By Lemma Q4(a), for `r′ ≤ min(d−1, ⌊ρ_e d⌋ + 1)`:
`ln(1 + Γ″(r′)) ≤ ln(4(d+1)²e^{2u+e^u+de}) ≤ x − ln 3`.  So `r* ≥ min(d−1, ⌊ρ_e d⌋+1)`, `2^d/|B(d, r*)| ≤ (d+1)e^{dθ_na(e)}` as in
Lemma Q4(b), and `2M ≤ 8K·2^d/|B(d, r*)|`.  For the consequence take `e = (x − c′_d)/d` and use (F4):
`θ_na(y − t) − θ_na(y) ≤ θ_na(0) − θ_na(t) ≤ u√(t/2)` with `t = c′_d/d`.  ∎

(b) answers item 2 of the brief: at an extensive accuracy the base bracket costs `exp(d·θ_na(x/d) + O(ln d))`
after a shift of the accuracy by `2 ln d + O(1)`, hence `exp(d·θ_na(x/d) + O(√(d ln d)))` uniformly in `x ≥ c′_d`, and
`exp(d·a + O(√(d·ln(1/x))))` at bounded accuracies; a failure probability `e^{-cd}` costs `ln K = ln d + O(1)`.
(Measured at `u = 1`, `δ = e^{-da}`: `ln cost − d·θ_na(x/d) = 12 … 35` nats for `d = 10³ … 6.4·10⁴` and
`x/d ∈ [0.1, 0.75]·ε*`, i.e. `≈ ln K + 2 ln d` at most: §7.1, part E′.  Only `T₁ ≤ a`, i.e. (a), is used below.)

---

## 4. Majorants and the two inductive steps

The induction does not use the exact recursion `T_k`.  It uses the piecewise-linear **majorants** through which
the rate is proved: "`T ≤ B − σx` on `(0, R)`".  Their virtue at finite `n` is that every parameter of a level is
then an explicit number, and that a shift of an accuracy by `c` costs `σc ≤ c` nats and nothing else.  The slope
step of §4.1 is the finite-`n` form of `ScienceR13.lemma1` / `lemma1_top` (`StepLE.of_limit` at the outer fraction `g/h`:
step (i) of the proof of Theorem 11.53(c)); the drop of §4.2 is that of `lemma2` (`StepLE.of_macro` with the outer
fraction `x₀/(a + x₀)`: step (ii)) and, at the same time, of the step at accuracy zero (`hstep0` of `rate_zero`, i.e.
Proposition 11.57(b)).

**Definition.**  Let `B > 0`, `σ ≥ 0`, `R ∈ (0, ∞]` (with `σ = 0` if `R = ∞`), and let `E(d, x; Λ) ≥ 0` be nondecreasing in `d`
and `Λ` and nonincreasing in `x`.  A certified family `𝔉` with least accuracy `x_min` has the property
`𝓗(B, σ, R; E)` if for all `d ≥ 1`, `x ≥ x_min`, `0 < δ < 1` and all `Λ ≥ ln(1/δ) + d·ln 2`

    b_𝔉(d, x, δ)  ≤  d·B − σ·min(x, R·d) + E(d, x; Λ).

By Proposition Q5(a), `𝔊_0` has `𝓗(a, 0, ∞; E_base)` with any `x_min > 0`.  The following functions of the
dimension are used: `A_n := (2u + ln 2)n + 3`, `c_log(n) := ln(n+1) + ln 6 + 2u + e^u`, `X₀(n) := 1 + c_log(n) + h`.

### 4.1 The slope step

Let `𝔉` have `𝓗(B, σ, R; E)` with `B ≥ h`, `0 ≤ σ ≤ 1`, `x_min ≤ 1`, and either `R = ∞` (then `σ = 0`) or `0 < R ≤ h`.  Put
`R′ := h` if `R = ∞` and `R′ := Rh/(h + R)` otherwise.  The family `S[𝔉]` (same `x_min`) is defined as follows.  For
`(n, x, δ)` let `x̂ := min(x, R′n)`.

* If `x̂ < X₀(n)`: `S[𝔉](n, x, δ) := 𝔉(n, x, δ)` (*pass-through*).
* Otherwise the **level as built** is Algorithm 2L⁺ with

      n_o = ⌊(x̂ − 1 − c_log(n))/h⌋,   n_i = n − n_o,   λ = 1,  η = ½,  η′ = 1,  ν₁ = 1,  b = 1,
      θ = e^{x̂−1} − (3e + 1) − (2p_u)^n/e,
      ladder  x₀ = 2un_i  >  x₁ := min(⌈x̂⌉, ⌈2un_i⌉ − 1)  >  x₁ − 1  >  …  >  2  >  1 = x_L        (L = x₁),
      inner procedures  I_l = 𝔉(n_i, x_l, δ′),

  and `S[𝔉](n, x, δ)` is the cheaper of this level and of `𝔉(n, x, δ)`.

**Proposition Q6 (slope step) [proved here from (T), Q1, Q2, Q4].**  The level as built is admissible for (T) and
has accuracy exactly `x̂ ≤ x`; and `S[𝔉]` has `𝓗(B, σ + B/h − 1, R′; E′)` with

    E′(n, x; Λ) := E(n, min(x, 1); Λ + q_S(n, Λ)) + c_S(n, Λ; B),
    c_S(n, Λ; B) := (1 + c_log(n) + h)·B/h + 1 + 2 ln A_n + ln(18e(e−1)) + ln K̄_S(n, Λ) + ln(n+3),
    q_S(n, Λ)    := ln(4(n+1)) + ln A_n + ln(24e(e−1)) + ln K̄_S(n, Λ),
    K̄_S(n, Λ)   := 18·[Λ + ln(2A_n·m̄_S(n)·(n+3))] + 1,      m̄_S(n) := n + 2 + log₂(12e(e−1)A_n).

For fixed `u`: `c_S(n, Λ; B) = (B/h + 3)·ln n + ln(Λ + ln n) + O(1)`, i.e. `(B/h + 4) ln n + O(1)` when `Λ = O(n)`.

*Proof.*  Let `n, x, δ, Λ ≥ ln(1/δ) + n ln 2` be given, `x̂ = min(x, R′n)`, `σ′ = σ + B/h − 1`.  Note `R′ ≤ R`, `R′ ≤ h`, and
`R′ ≤ h/2` unless `R = ∞`.

*Pass-through, `x̂ < X₀(n)`.*  `b_𝔉(n, x, δ) ≤ nB − σ·min(x, Rn) + E(n, x; Λ) ≤ nB − σ′x̂ + (B/h − 1)x̂ + E(n, x; Λ)`, since
`min(x, Rn) ≥ x̂`; and `(B/h − 1)x̂ < (B/h)X₀(n) = (1 + c_log(n) + h)B/h ≤ c_S`, `E(n, x; Λ) ≤ E(n, min(x,1); Λ + q_S)`.

*The level as built, `x̂ ≥ X₀(n)`.*
(1) *Admissibility.*  `n_o ≥ 1` because `x̂ ≥ X₀(n)`; `n_o < x̂/h ≤ n`, so `n_o ≤ n − 1` and `n ≥ 2`; moreover
`n_i ≥ n − (x̂ − 1 − c_log(n))/h ≥ (1 + c_log(n))/h`, so `2un_i > 1` (by (F3), `h ≤ u < 2u(1 + c_log)`) and `1 ≤ x₁ < x₀`.
`x̂ − 1 ≥ c_log(n) ≥ ln 12 + 1 > ln(2(3e+2))`, so `θ ≥ e^{x̂−1} − (3e+2) ≥ e^{x̂−1}/2 > 0`.  The accuracy is
`ln[(2p_u)^n + e(3e + 1 + θ)] = x̂` (`e^λ(1+η)/(1−η) = 3e`, `η′ = 1`).  The inner accuracies are `≥ 1 ≥ x_min`.
(2) *The outer sample.*  `n_o h ≤ x̂ − 1 − c_log(n)` gives
`3(n_o+1)e^{2u+e^u+n_o h} ≤ 3(n+1)e^{2u+e^u}·e^{x̂−1}/(6(n+1)e^{2u+e^u}) = e^{x̂−1}/2 ≤ θ`, so Lemma Q4(b) applies with `m = n_o`, `e = h`,
`c_η = ⅓`: `ln(1/π†) ≤ n_o h + ln(n_o+1)` by (F2).  Hence, with Proposition Q1,

    Λ_lev := ln 2M̄ ≤ P_M + (x̂ − 1 − c_log(n)) + ln(n_o+1) ≤ x̂ − 1 + P_M ≤ x̂ − 1 + P_cnt.                     (4.1)

(3) *The constants.*  `J = ⌈2un + 1 + n_o ln 2⌉`, so `J + 1 ≤ A_n`; `ν₀ = 2(e−1)(J+1)`;
`P_cnt = 2 ln(J+1) + ln(18e(e−1)) + ln K`, `P_M = ln(J+1) + ln(24e(e−1)) + ln K`; `m_max + 1 ≤ m̄_S(n)` by Lemma Q2(b)
(`n_o ≤ n − 1`); `L = x₁ ≤ ⌈x̂⌉ ≤ hn + 1 < n + 1`; so `K ≤ K̄_S(n, ln(1/δ)) ≤ K̄_S(n, Λ)` by Lemma Q2(c), and by (2.1)

    ln(1/δ′) + n_i ln 2 ≤ Λ + ln(4L) + P_M ≤ Λ + q_S(n, Λ) =: Λ′.

So the hypothesis on `𝔉` applies to every inner call with `Λ′`:
`ln C_l ≤ n_i B − σ·min(x_l, Rn_i) + E(n_i, x_l; Λ′)`, and `E(n_i, x_l; Λ′) ≤ E(n, 1; Λ′) =: E₁` (monotonicity; `x_l ≥ 1`).
(4) *`R n_i ≥ x̂` if `R < ∞`:*  `n_i > n − x̂/h` and `R(n − x̂/h) ≥ x̂` is `x̂ ≤ R′n`.  So `min(x_l, Rn_i) ≥ min(x_l, x̂)` in all cases
(for `R = ∞` the term is absent, `σ = 0`).
(5) *The terms of Proposition Q1.*  Let `V := n_i B + (1−σ)x̂ + 1 + P_cnt + E₁`.
 `l = 1`, `x₁ ≥ x̂`:  `t₁ ≤ Λ_lev + n_i B − σx̂ + E₁ ≤ V − 2` by (4.1).
 `l = 1`, `x₁ < x̂`:  then `x₁ = ⌈2un_i⌉ − 1`, so `x₀ ≤ x₁ + 1` and `t₁ ≤ x₁ + 1 + P_cnt + n_i B − σx₁ + E₁ ≤ V`.
 `l ≥ 2`:  `x_{l−1} ≤ x₁ ≤ ⌈x̂⌉ < x̂ + 1` and `x_l = x_{l−1} − 1 < x̂`, so `t_l ≤ x_l + 1 + P_cnt + n_i B − σx_l + E₁ ≤ V`.
 The outer sample:  `Λ_lev ≤ x̂ − 1 + P_cnt ≤ V` because `n_i B ≥ σx̂` (trivial for `σ = 0`; otherwise `x̂ ≤ hn/2`, hence
 `n_i > n/2` and `n_i B ≥ nh/2 ≥ x̂`).
 So `ln C_max ≤ ln(L+2) + V`.
(6) *The dimension.*  `n_o ≥ (x̂ − 1 − c_log(n))/h − 1`, so `n_i B ≤ nB − x̂B/h + (1 + c_log(n) + h)B/h`, and

    ln C_max ≤ nB − σ′x̂ + (1 + c_log(n) + h)B/h + 1 + P_cnt + ln(L+2) + E₁ ≤ nB − σ′·min(x, R′n) + c_S(n, Λ; B) + E(n, 1; Λ′),

with `P_cnt ≤ 2 ln A_n + ln(18e(e−1)) + ln K̄_S(n, Λ)` and `L + 2 ≤ n + 3`.  The cheaper of two procedures obeys the bound of
either.  ∎

*What the step does.*  The outer block has `n_o ≈ x/h` coordinates and is sampled `e^{n_o h} ≈ e^x` times: with a
hint this is what the accuracy `x` costs on `n_o` coordinates, and by `θ_na(h) = h` it is also what the plain bracket
needs there *at the accuracy rate `h`*.  The remaining `n − x/h` coordinates are served by `𝔉`, and of the sampled
points only `e^{x_{l−1}}` need an inner bracket of accuracy `x_l`.  The whole error is: the shortfall
`(1 + c_log)/h` of the outer block (it buys the factor `6(n+1)e^{2u+e^u}` in `θ` that Lemma Q4 needs), the factor
`e^{P_cnt} ≈ J²K`, the ladder gap `1` and the number of terms.

### 4.2 The drop

Let `𝔉` have `𝓗(B, 1, R; E)` with `0 < R ≤ h ≤ B` and least accuracy `x_min`; let `0 < c ≤ ⅓`, `0 < α ≤ 1`, and

    w(c) := ln(e^c(1+c)/(1−c) + 2c) + c   (≤ 6.25c),        β := α − w(c)  ≥  x_min   (assumed; note β < α ≤ 1),
    φ := R/(a + R),      B′ := (1 − φ)B = B·a/(a + R),      ℓ_c := ln 2 + 3u + 2.25c + ln(1/c),
    ς(n) := c̄_π(⌊φn⌋; ℓ_c)/(a + R)   ("shift"),      n_D′(c) := max{ 2/u + 2 ,  ln(6/(5c))/ln((1+e^u)/2) }.

The family `D[𝔉; c, α]` has least accuracy `α` and is *accuracy-blind*: for every `x ≥ α` it delivers the accuracy `α`.
The **level as built** at `(n, δ)`, defined if `n ≥ n_D′(c)` and `n_o := ⌊φn − ς(n)⌋ ≥ 1`, is Algorithm 2L⁺ with

    n_o as above,   n_i = n − n_o,   λ = η = η′ = θ = c,   ν₁ = 2e^u n_o/c,   b = β,
    ladder  x₀ = 2un_i  >  x₁ := ⌈R n_i⌉  >  x₁ − 1  >  …  >  1  >  β = x_L        (L = x₁ + 1),      I_l = 𝔉(n_i, x_l, δ′).

`D[𝔉; c, α](n, x, δ)` is the cheapest of: this level (if defined); the same level with `n_o = ⌊φn⌋` instead ("without
shift"; if `n ≥ n_D′(c)` and `⌊φn⌋ ≥ 1`); and `𝔉(n, α, δ)` (pass-through).

**Proposition Q7 (drop) [proved here from (T), (L), Q1, Q2, Q3].**  The level as built is admissible for (T) with
accuracy at most `α`, and `D[𝔉; c, α]` has `𝓗(B′, 0, ∞; E′)` with

    E′(n, x; Λ) := E(n, β; Λ + q_D(n, Λ; c)) + c_D(n, Λ),
    c_D(n, Λ)   := B·(1 + φ·n_D′(c)) + B·ς(n) + ln(n+4) + 1 + P̄_cnt(n, Λ; c),          [B·ς(n) = c̄_π(⌊φn⌋; ℓ_c)·B′/a]
    q_D(n, Λ; c) := ln(4(n+2)) + P̄_M(n, Λ; c),
    P̄_cnt := ln(A_n/c) + ln 7.45 + ln ν̄_D + ln K̄_D,     P̄_M := ln 11.17 + ln ν̄_D + ln K̄_D,
    ν̄_D := (1.8A_n + 3e^u n)/c,     K̄_D := 4c^{-2}·[Λ + ln(2(A_n/c)·m̄_D·(n+4))] + 1,     m̄_D := n + 2 + log₂(5.6ν̄_D).

The level without shift obeys the same bound with `c̄_π(⌊φn⌋; ℓ_c)` in place of `B·ς(n)`.
For fixed `u`: `c_D = u√(φnℓ_c/2)·B′/a + (3 + B′/a)·ln n + 4 ln(1/c) + ln(Λ + ln(n/c)) + O(1 + ℓ_c)`.

*Proof.*  Let `n, δ, Λ ≥ ln(1/δ) + n ln 2`.
*Pass-through.*  `b_𝔉(n, α, δ) ≤ nB − min(α, Rn) + E(n, α; Λ) ≤ nB′ + nφB + E(n, β; Λ + q_D)`.  It is used by the proof only
when the level as built is not defined, i.e. when `n < n_D′(c)` — then `nφB < φ·n_D′(c)·B` — or `φn − ς(n) < 1` — then
`nφB < (1 + ς(n))B`; in both cases `nφB ≤ c_D`.
*The level as built.*  (1) *Admissibility.*  `φ ≤ h/(a+h) < ½`, so `1 ≤ n_o ≤ φn < n/2`, `n ≥ 2`, `n_i > n/2 ≥ 1/u + 1`, hence
`R n_i + 1 ≤ un_i + 1 ≤ 2un_i` by (F3) and `1 ≤ x₁ < x₀`; `x_L = β = b > 0` and the inner accuracies are `≥ β ≥ x_min`.
Accuracy: `e^β(e^c(1+c)/(1−c) + 2c) = e^{α−c}`, and `(2p_u)^n ≤ 5c/6 ≤ 1 − e^{-c} ≤ e^α(1 − e^{-c})` because `n ≥ n_D′(c)`; so
`x_out ≤ α`.
(2) *The outer sample.*  `ν₀ ≥ ν₁/(1−η) = 2e^u n_o/(θ(1−η))`, `θ = c ≤ 2`, and `u m₀ < u + ln((1+c)/(1−c)) ≤ u + 2.25c`, so
`ln(2e^{u(m₀+2)}/θ) ≤ ℓ_c`: Lemma Q3 gives `ln(1/π†) ≤ n_o a + c̄_π(n_o; ℓ_c) ≤ n_o a + c̄_π(⌊φn⌋; ℓ_c)`.  With
`n_o a ≤ (φn − ς)a` and `R n_i ≥ R(n − φn + ς) = φna + Rς` (as `φa = R(1−φ)`):

    Λ_lev = P_M + ln(1/π†) ≤ P_M + φna − ςa + ς(a + R) = P_M + φna + Rς ≤ P_M + R n_i.                          (4.2)

(3) *The constants.*  `J = ⌈(2un + β + n_o ln 2)/c⌉`, so `J + 1 ≤ A_n/c`; `(e^c − 1)/c ≤ 1.2` and `1/(1−c) ≤ 1.5` give
`ν₀ ≤ ν̄_D`; `2(1+c)e^c/(1−c) ≤ 5.6`, `2(1+c)²e^c/(1−c) ≤ 7.45`, `4(1+c)e^c/(1−c) ≤ 11.17`, `3(1+c) ≤ 4`; `L = ⌈Rn_i⌉ + 1 ≤ hn + 2`;
so `m_max + 1 ≤ m̄_D`, `K ≤ K̄_D`, `P_cnt ≤ P̄_cnt`, `P_M ≤ P̄_M`, and by (2.1)
`ln(1/δ′) + n_i ln 2 ≤ Λ + q_D(n, Λ; c) =: Λ′`.  Hence `ln C_l ≤ n_i B − min(x_l, Rn_i) + E₁`, `E₁ := E(n, β; Λ′)`.
(4) *The terms.*  `l = 1`: `x₁ ≥ Rn_i`, so `t₁ ≤ Λ_lev + n_i B − Rn_i + E₁ ≤ n_i B + P_M + E₁` by (4.2).
 `2 ≤ l ≤ L−1`: `x_l = x_{l−1} − 1 ≤ x₁ − 1 < Rn_i`, so `t_l ≤ x_{l−1} + P_cnt + n_i B − x_l + E₁ = n_i B + 1 + P_cnt + E₁`.
 `l = L`: `x_{L−1} = 1` (or `x₁ = 1` if `L = 2`), so `t_L ≤ 1 + P_cnt + n_i B + E₁`.
 The outer sample: `Λ_lev ≤ P_M + Rn_i ≤ P_M + n_i B` (`R ≤ B`).
 So `ln C_max ≤ ln(L+2) + n_i B + 1 + P_cnt + E₁` (`P_M ≤ P_cnt`).
(5) *The dimension.*  `n_i ≤ n − φn + ς + 1`, so `n_i B ≤ nB′ + (1 + ς)B`; `L + 2 ≤ n + 4`.
Without the shift, (4.2) becomes `Λ_lev ≤ P_M + c̄_π + Rn_i` and `n_i B ≤ nB′ + B`.  ∎

*What the drop does.*  It is the bounded level of Proposition 11.57(b) with the outer fraction `R/(a + R)` at which
the outer sample `e^{φna}` equals the largest accuracy `Rn_i` at which the inner family still has slope one — so that
*every* rung has the same exponent `n_i B`.  The shift moves the `√`-overhead `c̄_π` of the outer sample from the
terms into the dimension, where it costs `B/(a + R) = B′/a < 1` per nat.  The drop is the only place where a
bounded accuracy is paid for: `θ = c`, and `w(c)` is taken from the accuracy.

---

## 5. The epoch schedule: `k_M` nested levels with an explicit error term

### 5.1 The design

Fix `u`, `ε > 0`, `M ≥ 0`.  Sequences `d_m, J_m, k_m, B_m` as in Theorem Q; `R_m := h/J_m`, `φ_m := R_m/(a + R_m) = h/(J_m a + h)`,
so that `B_{m+1} = (1 − φ_m)B_m` by (R).  Accuracies: `ε̂ := min(ε, 1)`,

    c_m := ε̂/(13(m+1)(m+2)),      α_M := ε̂,      α_m := α_{m+1} − w(c_m)   (m = M−1, …, 0);

as `w(c) ≤ 6.25c` and `Σ_{m≥0} 1/((m+1)(m+2)) = 1`:  `α_0 ≥ ε̂(1 − 6.25/13) > 0.519·ε̂`.  Families:

    𝔊_0 := the base family (least accuracy α_0);
    for m = 0, …, M−1:    𝔊_{m,0} := 𝔊_m,     𝔊_{m,j} := S[𝔊_{m,j−1}]  (1 ≤ j ≤ J_m, with B = B_m),     𝔊_{m+1} := D[𝔊_{m,J_m}; c_m, α_{m+1}]  (with R = R_m).

`𝔊_M(n, ε̂, δ)` has `k_M` nested levels (the base, `J_m` slope steps and one drop per epoch).  At `u = 1`
(`h/a = 0.2626`; `out_q4_bound_table.txt` has `u = ½, 2` and 44 epochs):

| `m` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 12 | 16 | 20 | 24 | 32 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `d_m` | 0.356 | 0.496 | 0.720 | 1.122 | 1.489 | 2.093 | 2.787 | 5.35 | 9.89 | 18.8 | 64.8 | 220 | 745 | 8533 |
| `J_m` | 1 | 1 | 1 | 2 | 2 | 3 | 3 | 6 | 10 | 19 | 65 | 220 | 746 | 8533 |
| `k_m` | 1 | 3 | 5 | 7 | 10 | 13 | 17 | 27 | 43 | 69 | 202 | 642 | 2121 | 23 995 |
| `B_m/a` | 1 | 0.792 | 0.627 | 0.497 | 0.439 | 0.388 | 0.357 | 0.312 | 0.289 | 0.277 | 0.2667 | 0.2638 | 0.2630 | 0.26268 |
| `φ_m` | 0.208 | 0.208 | 0.208 | 0.116 | 0.116 | 0.081 | 0.081 | 0.042 | 0.026 | 0.014 | 0.0040 | 0.0012 | 0.00035 | 0.00003 |

The least accuracies fit: the families of epoch `m` have least accuracy
`α_m ≤ 1`; a slope step calls its inner family at accuracies `≥ 1` or passes the accuracy through; the drop that ends
epoch `m` calls at accuracies `≥ β = α_{m+1} − w(c_m) = α_m`.

### 5.2 The theorem

Number the constructive levels from the top: `t = 0, …, T−1`, `T = k_M − 1`; level `0` is the drop that ends epoch
`M−1`, then come the `J_{M−1}` slope steps of that epoch, then the drop of epoch `M−2`, and so on down to the `J_0`
slope steps of epoch `0`.  Put

    Λ̄_0 := ln(1/δ) + n ln 2,      Λ̄_{t+1} := Λ̄_t + q_t(n, Λ̄_t),
    𝓔_M(n, ε, δ) := E_base(n, α_0; Λ̄_T) + Σ_{t=0}^{T−1} c_t(n, Λ̄_t),                                                   (5.2)

where for a slope step of epoch `m`: `c_t = c_S(n, ·; B_m)`, `q_t = q_S(n, ·)`, and for the drop that ends epoch `m`:
`c_t = c_D(n, ·)` and `q_t = q_D(n, ·; c_m)` of Proposition Q7 with `B = B_m`, `R = R_m`, `φ = φ_m`, `c = c_m`.
(`qlib.E_total` is this formula.)

**Theorem Q8 [proved here: Propositions Q5, Q6, Q7 and (R)].**  For all `n ≥ 1`, `ε > 0`, `0 < δ < 1`, `M ≥ 0`:
`𝔊_M(n, ε̂, δ)` returns `L ≤ U` with `L ≤ A ≤ U ≤ e^ε L` except with probability `δ`, and makes at most

    exp( n·B_M + 𝓔_M(n, ε, δ) ),        B_M = h(1 + 1/d_M) ≤ h + c₁/(k_M + c₂),

evaluations in every run, at every `ψ ∈ L_u(Q_n)`.  Consequently `ln N(n; ε, δ) ≤ n·B_M + 𝓔_M(n, ε, δ)` (the midpoint
`½(ln L + ln U)` of such a bracket is `(ε/2, δ)`-correct).

*Proof.*  *Slopes.*  Claim: `𝔊_{m,j}` has `𝓗(B_m, j/d_m, h/j; ·)` for `1 ≤ j ≤ J_m`, and `𝔊_m` has `𝓗(B_m, 0, ∞; ·)`.  For `m = 0`,
`j = 0` this is Proposition Q5(a) (`B_0 = a`).  Step `j → j+1 ≤ J_m`: the hypotheses of Proposition Q6 hold — `B_m ≥ h`;
`σ = j/d_m ≤ 1` because `j ≤ J_m − 1 < d_m` by (R); `R = h/j ≤ h` (or `R = ∞`, `σ = 0` for `j = 0`); `α_m ≤ 1` — and it gives the slope
`j/d_m + B_m/h − 1 = (j+1)/d_m` (as `B_m/h − 1 = 1/d_m`) on the range `R′ = (h/j)h/(h + h/j) = h/(j+1)` (`h` for `j = 0`).  At `j = J_m`
the slope `J_m/d_m` is at least `1` on the range `h/J_m = R_m`, so `𝔊_{m,J_m}` has `𝓗(B_m, 1, R_m; ·)` (a slope larger than one
implies slope one), `R_m ≤ h ≤ B_m`, `β = α_m`, and Proposition Q7 gives `𝓗((1−φ_m)B_m, 0, ∞; ·) = 𝓗(B_{m+1}, 0, ∞; ·)` for `𝔊_{m+1}`.
*Errors.*  Define `E^{(T)} := E_base` and, downwards, `E^{(t)}(d, x; Λ) := E^{(t+1)}(d, x↓; Λ + q_t(d, Λ)) + c_t(d, Λ)`, with
`x↓ = min(x, 1)` for a slope step and `x↓ = β` for a drop: these are the error functions that the two propositions
produce, and each is nondecreasing in `d` and `Λ` and nonincreasing in `x`, because `c_t`, `q_t` are nondecreasing in `d`
and `Λ` (each is a sum of nondecreasing terms; `c̄_π(⌊φd⌋; ℓ)` is nondecreasing in `d`).  The top family is called at
`(n, ε̂, δ)` with `Λ = Λ̄_0`; unrolling, the arguments of `E^{(t)}` are `d = n` and `Λ = Λ̄_t`, and the last accuracy is `≥ α_0`,
so the error is at most (5.2).  The accuracy of `𝔊_M(n, ε̂, δ)` is at most `α_M = ε̂ ≤ ε`; the cost bound holds in every
run by (T).  `B_M − h = h/d_M ≤ c₁/(k_M + c₂)` is (R) at `k = k_M`.  ∎

### 5.3 Why the error is uniform in the number of levels

**Proposition Q9a (closed form of (5.2)) [proved here].**  Let `T = k_M − 1`,
`q* := max{q_S(n, 2Λ̄_0), max_{m<M} q_D(n, 2Λ̄_0; c_m)}` and suppose `T·q* ≤ Λ̄_0`.  Then `Λ̄_t ≤ 2Λ̄_0` for all `t ≤ T`, and

    𝓔_M(n, ε, δ)  ≤  C₁·√n + (T − M)·ℓ_S + M·ℓ_D + ℓ_B,
    C₁ := u·[ √(ℓ⁰_{α_0}/2) + Σ_{m<M} √(φ_m ℓ_{c_m}/2)·B_{m+1}/a ]  ≤  u·[ √(ℓ⁰_{α_0}/2) + r̄^{-1/2} Σ_{m≥0} (1+κ)^{-m/2} √((ℓ̄ + 2 ln(m+2))/2) ]  <  ∞,
    ℓ_S := c_S(n, 2Λ̄_0; a) = (a/h + 4)·ln n + O_{u,δ}(1),
    ℓ_D := max_{m<M} [ c_D(n, 2Λ̄_0) − u√(φ_m n ℓ_{c_m}/2)·B_{m+1}/a ] = O(ln n + ln(1/ε̂) + ln(M+1)),
    ℓ_B := E_base(n, α_0; 2Λ̄_0) − u√(nℓ⁰_{α_0}/2) = O(ln n + ln(1/ε̂)),

with `ℓ̄ := ln 2 + 3u + 0.1 + ln(13/ε̂)`, the `O`'s for fixed `u`, and `M ≤ 1 + ln(k_M + 1)/ln(1+κ)`.

*Proof.*  `Λ̄_t = Λ̄_0 + Σ_{t′<t} q_{t′}(n, Λ̄_{t′}) ≤ Λ̄_0 + t·q*` by induction.  The slope steps: `c_S(n, Λ; B_m) ≤ c_S(n, Λ; a)`.
The drops: by Lemma Q3's definition, `c̄_π(m′; ℓ) ≤ u√(m′ℓ/2) + [ln 2 + m*(ℓ)H(p_u) + u + (4/(3p_u))(ℓ+2) + ln(m′+1)]`, and
`m*(ℓ) ≤ (2ℓ + 8p_u)/p_u²`, `ℓ_{c_m} ≤ ℓ̄ + 2 ln(m+2)`, `ln(1/c_m) ≤ ln(13/ε̂) + 2 ln(M+1)`, `n_D′(c_m) = O(ln(M+1) + ln(1/ε̂))`.  The
base: likewise, `ℓ⁰_{α_0} ≤ ln 4 + 3u + ½ + ln(2/ε̂)`.  The series: by (R), `d_{m+1} + 1 ≥ (d_m + 1)(1 + κ)`, so
`d_m + 1 ≥ (1+κ)^m a/(a−h)`, and `φ_m ≤ (h/a)/(d_m + h/a) ≤ (a/(2a−h))/(d_m + 1) ≤ r̄^{-1}(1+κ)^{-m}` (the ratio
`(d+1)/(d + h/a)` is largest at `d = d_0`); `B_{m+1} ≤ a`.  The number of epochs: `(1+κ)^{M−1} ≤ d_{M−1} + 1 ≤ J_{M−1} + 1 ≤ k_M`.  ∎

At `u = 1`, `ε = 1` the series is small: `C₁ = 1.6 + 3.9 = 5.5` (first 44 epochs; §7.4), although the crude geometric
bound with ratio `(1+κ)^{-1/2} = 0.979` is large — numerically the `d_m` grow by a factor `≈ a/(a−h) = 1.36` per epoch,
not `1 + κ = 1.043`.

**Three places where a schedule could lose uniformity in `k`, and how the present one avoids them.**
1. *Accuracies.*  The proof of Theorem 11.58 halves the accuracy at every bounded level (`ε, ε/2, …, ε/2^m`).  With one
   bounded level per epoch that would make the bottom accuracy `ε·2^{-M}` and cost `√(ln(1/α_0)) = √M` in the `√n`-term
   and `2 ln(1/α_0) = O(M)` nats per bounded level.  Here a drop takes `w(c_m) ≤ 6.25c_m` with `Σ c_m < ε̂/13`, the bottom
   accuracy stays above `ε̂/2`, and the price is `4 ln(1/c_m) = O(ln m)` nats per drop.
2. *Failure probabilities.*  `ln(1/δ)` grows by `ln M̄ + ln 4L` per level, up to `≈ n ln 2` in all — but it enters only
   through `K`, linearly, and (2.1) bounds it uniformly (`Λ̄_t ≤ 2Λ̄_0`).
3. *Ladders.*  A ladder with a fixed number of rungs loses a fixed fraction of the accuracy at the rung that
   matters, at every level (§2.5); an arithmetic ladder below a cap loses `1` nat.
The assembly in the proof of Theorem 11.54 (a dense set of tuples, each admissible from a dimension `d₀` on; the
cheapest of the first `d` tuples) has no explicit `n₀` and is the fourth such place; it is not used here.

---

## 6. The optimisation over the number of levels

### 6.1 The theorem

**Theorem Q9 [proved here from Theorem Q8, Proposition Q9a and (R)].**  Fix `u > 0`, `ε > 0`, `0 < δ < 1`.
(a) For every `n ≥ 1` and `M ≥ 0`:  `ln N(n; ε, δ) ≤ n·h + n·c₁/(k_M + c₂) + 𝓔_M(n, ε, δ)`.
(b) There is `n₀(u, ε, δ)` such that for all `n ≥ n₀`

    ln N(n; ε, δ)  ≤  n·h + 2·√( (1 + r̄)·c₁·n·ℓ_S ) + C₁√n + M·ℓ_D + ℓ_B,        ℓ_S = (a/h + 4) ln n + O(1),   M = O(ln n),

so that `limsup_n (ln N(n; ε, δ) − nh)/√(n ln n) ≤ C_* = 2√((1 + r̄)c₁(a/h + 4))`.
(c) There is `C(u, ε, δ)` with `ln N(n; ε, δ) ≤ n·h + C·√(n ln n)` for all `n ≥ 2`.
(d) (b) and (c) hold for accuracies `ε_n ∈ [n^{-A}, 1]` in place of `ε`, with `C₁`, `ℓ_D`, `ℓ_B` evaluated at `ε_n`
(`C₁ = O(√(A ln n))`), hence with a constant `C_* + O(u√A)` in the limsup.

*Proof.*  (a) is Theorem Q8.  (b) The sequence `k_m` does not jump by more than the factor `1 + r̄`:
`d_{m+1}/d_m = (J_m a + h)/(J_m a − h d_m)` is decreasing in `J_m ≥ d_m`, hence at most `(a + h/d_m)/(a − h) ≤ r̄` (as `h/d_m ≤ a − h`);
so for `m ≥ 1`, `k_m ≥ 2 + d_{m−1} ≥ 2 + d_m/r̄` and `k_{m+1} − k_m = J_m + 1 < d_m + 2 ≤ r̄k_m`; and `k_1 < 3 + d_0 = 1 + r̄`.  Let
`k† := √((1 + r̄)c₁n/ℓ_S)` and `M := max{m : k_m ≤ k†}` (`k† ≥ 1` for large `n`).  Then `k†/(1 + r̄) < k_M ≤ k†`, so
`n(B_M − h) ≤ nc₁/k_M < (1 + r̄)c₁n/k†` (here `c₂ ≥ 0`, because `(2a + h)(a − h) ≥ 0`), and `(T − M)ℓ_S ≤ k†ℓ_S`.  The hypothesis of
Proposition Q9a holds for large `n`: `T ≤ k† = O(√(n/ln n))` and `q* = O(ln n)`, while `Λ̄_0 ≥ n ln 2`.  The sum of the two
level terms is `2√((1 + r̄)c₁nℓ_S)`; `M = O(ln k_M) = O(ln n)`.  (c) For `n < n₀` use `N ≤ 2^n`.  (d) The proofs of Theorem Q8
and Proposition Q9a hold for every `ε > 0` with the stated dependence: `ε` enters `ℓ_S` not at all, `C₁` through
`√(ln(1/ε̂))`, and `ℓ_D`, `ℓ_B` through `O(ln(1/ε̂))`.  ∎

*Remarks.*  (1) `C_*` uses the worst-case constants of the rate: `c₁ = 6.4a` at `u = 1`, although along the epoch ends
`(B_m − h)k_m → a − h` **[numerical; `0.745a` at `m = 25`]**, and `1 + r̄` for the granularity of the epochs, although
`k_{m+1}/k_m → a/(a−h) = 1.36` **[numerical]**; with these, and `B_m/h → 1` in `c_S`, the level term would be
`≈ 2√(5(a−h)·n ln n)·(1.36)^{1/2}`, i.e. about `1.5·√(n ln n)` at `u = 1` instead of `8.6` **[heuristic]**.  The bound of
Theorem Q8 itself, minimised over `M` numerically, has `(bound − nh)/√(n ln n) ∈ [2.4, 3.8]` for `n = 6.4·10⁴ … 10^{12}`
(§7.4); there the `√n`-term `C₁√n` is still as large as the level term.
(2) Per level the scheme pays `≈ (B_m/h + 4)·ln n + 20 … 60` nats (`≈ 100` nats at `n = 10⁶`, `u = 1`); this is why the
optimum has only `k ≈ √(n/ln n)/7` levels and why the bound gains nothing below `n ≈ 10⁴`.

### 6.2 What a better rate would give

The level term is `min_k [n·ρ(k) + k·ℓ_S]`, `ρ(k)` the rate.  With the proved `ρ(k) = c₁/(k + c₂)` it is `Θ(√(n ln n))`.
With a rate `ρ(k) = C/k²` it would be `Θ(n^{1/3}(ln n)^{2/3})`, below the `√n` of the bounded levels, and the bound would
be `n·h + O(√n)`.  **[conjecture]**  The observed `(τ_k − h)/a ≈ 0.65/k²` is numerical and is a statement about the exact
recursion; to use it one needs (i) a proof, and (ii) an explicit schedule realising it whose levels lose `O(ln n)`
— for the majorant schedule this is Proposition Q6, and it rests on the outer accuracy rate of every non-bounded
level being bounded away from zero (here it is exactly `h`).  A `√n` remains in any case for this family of
algorithms at a bounded accuracy **[numerical, §2.3]**: the finest rung of the top level calls a
bounded-accuracy procedure on `≈ n·B_M/a` coordinates, and at a bounded `θ` the closing radius is
`p_u m − Θ(√m)`.  Whether `n·h + O(√n)`, or `n·h + O(ln n)` as with a hint, can be
reached without a hint remains open.

### 6.3 The route of the brief, and why it is not taken **[heuristic]**

The brief proposes `b_k(d, x, δ) ≤ d·T_k(x/d) + E_k` for the exact recursion.  Two things stand in the way.
(i) `R[T_k](g)` is an infimum over `(φ, β)` that need not be attained, and the `T_k` are only known to be
nonincreasing: rounding `φ` up to a multiple of `1/n` and `β` up to `1/n` is harmless for the inner part (monotonicity)
but changes the outer exponent `φθ_na((g−β)/φ)` by the modulus of `θ_na`, which is `u√(t/2)` near zero — an error
`O(√(n_o ln n))` whenever the near-optimal outer accuracy rate is small, and nothing is known about where the
optimal `(φ, β)` of the exact recursion lie.  (ii) Even at a rate bounded away from zero each level has the
polynomial slack of Lemma Q4.  So the natural error of that route is `E_k = O(k·√(n ln n))`, which with the proved
rate gives `n^{3/4}(ln n)^{1/4}` — the heuristic of §11.19(2).  The majorant schedule avoids (i) altogether: its
outer rates are `h` (slope steps) or bounded (drops, `O(ln k)` of them), by construction.

---

## 7. Numerical checks

All numbers are from the scripts of §10; the exact side always uses the referee's tables
`experiments/reviews/R8/r8_flat.TablesF` and the constant formulas of `K_REPORT.md` §2.2 as implemented in
`r8_flat.flat_run` (`qlib.selftest`: `level_consts`/`level_cmax` reproduce `flat_run`'s `lCmax`, `lMbar`, `K`, `J`, `r†`, `δ′`,
`x_out` in six designs to `10^{-9}`).  **In all runs no proved inequality is violated.**

### 7.1 One level against `flat_run` (`q1_one_level.py` → `out_q1_one_level.txt`)

The two-level design of `K_REPORT.md` §6.4 (`b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `δ = 0.05`, geometric ladder of 40 rungs,
`n_o = n/2`, `u = 1`; certified accuracy `0.8715`).  `ln C_max/(na)` reproduces the brief: `1.1384, 0.9933, 0.8721, 0.7262,
0.6415, 0.5899, 0.5646, 0.5407`.

*Part A/B — Proposition Q1, Lemma Q2, Lemma Q3.*  `M* = max{Λ, max_l t_l}`; `over = ln(1/π†) − n_o a`.

| `n` | `ln C_max` | `ln C_max − M*` (`≤ ln 42 = 3.74`) | the largest term | `Λ = ln 2M̄` | `P_M` | `P_cnt` | `ln(1/δ′)` | `over` | `over/√n_o` | Lemma Q3 `/√n_o` | K.4(d) `/√n_o` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 000 | 126.30 | 0.91 | finest rung (`0.6 → 0.5`) | 112.65 | 22.86 | 31.59 | 120.0 | 34.32 | 1.535 | 3.64 | 4.75 |
| 4 000 | 322.25 | 2.41 | rung 12 (`338 → 270`) | 309.68 | 24.35 | 34.47 | 317.1 | 63.44 | 1.418 | 2.76 | 4.59 |
| 16 000 | 1047.08 | 1.00 | rung 11 (`1196 → 923`) | 1033.09 | 25.84 | 37.34 | 1040.5 | 119.69 | 1.338 | 2.31 | 4.49 |
| 64 000 | 3839.07 | 0.00 | rung 10 (`4540 → 3384`) | 3809.49 | 27.33 | 40.21 | 3816.9 | 231.95 | 1.297 | 2.08 | 4.44 |

(All eight sizes are in the output.)  The proved `√`-constant is `u√(ℓ/2) = 1.83` (Lemma Q3; the column shows the whole
bound including its `O(ℓ/p_u)` and logarithmic terms) against `4.36` for Lemma K.4(d); measured `1.30 … 1.53`.
`P_cnt = ln(J+1) + ln ν₀ + ln K + 1.13` with `ln(J+1) = 9.4 … 13.5`, `ln ν₀ = 11.0 … 15.1`, `ln K = 10.2 … 10.5`.

*Part B′ — Lemma Q3 on exact tables.*  210 cases (`u ∈ {½, 1, 2}`; `m = 1 … 64 000`; `η = θ = c ∈ {⅓, 0.1, 0.05, 0.01, 0.001}`,
`ν₀` the least value allowed): the uniform bound `m·a + c̄_π(m; ℓ_c)` holds in all, and the refined bound and
`r† ≥ ⌊p_u m − s⌋` wherever `s ≤ p_u m/2 − 1`.  At `u = 1`, `m = 64 000`: `(ln(1/π†) − ma)/√m = 0.98, 1.28, 1.78` for
`c = ⅓, 0.05, 0.001`, against the proved leading constants `u√(ℓ₁/2) = 1.55, 1.83, 2.30`.

*Part C — the inequality (2.3), and the excess over the limit `n·τ₂` (`τ₂ = 0.5004a`).*

| `n` | `ln C_max − max{n_o a, max_l[min(n_o a, x_{l−1}) + ln C_l]}` | `Err` proved (2.3) | `ln C_max − nτ₂` | `/√n` | base bracket of the finest rung, `ln cost − n_i a` | `E_base` proved |
|---|---|---|---|---|---|---|
| 1 000 | 32.49 | 107.89 | 70.78 | 2.24 | 37.73 | 104.46 |
| 4 000 | 37.91 | 151.65 | 100.19 | 1.58 | 61.83 | 129.66 |
| 16 000 | 51.57 | 236.30 | 158.82 | 1.26 | 107.31 | 204.35 |
| 64 000 | 92.35 | 402.74 | 286.02 | 1.13 | 195.85 | 351.29 |

So the "`≈ 1.2√n`" of the brief is `2.24√n` at `n = 10³` and `1.13√n` at `6.4·10⁴`: it is not a multiple of `√n` over this
range (`≈ 30`–`40` nats of it are the polynomial factor `P_cnt`); the rest is the `√`-overhead of the outer sample,
of the base bracket at the finest rung, and — from `n = 4000` on, where the maximum sits at an extensive rung — the
gap of the geometric ladder.

*Part D — Lemma Q4.*  On exact tables, `u ∈ {½, 1, 2}`, 14 sizes `m = 1 … 64 000`, 8 rates `e ∈ [0, 1.5ε*]`, `η ∈ {½, 0.05}`
(672 cases): `r† ≥ min{m−1, ⌊ρ_e m⌋+1}` and `ln(1/π†) ≤ mθ_na(e) + ln(m+1)` always; least slack `0.0000` (at `m = 1`), e.g.
`15.3` at `u = 1`, `m = 64 000`, `e = h`.  Part (a) of the lemma also by direct summation in 40-digit arithmetic
(mpmath; `u ∈ {0.3, 1, 2, 4}`, `m ≤ 120`, six rates, 2380 triples `(u, m, e; r)`): least slack `2.48` in the logarithm; the
referee's float tables agree with the exact `ln Γ̃` to `1.2·10^{-13}`.  Through `flat_run` for the slope-step design at `x = gn` (`n = 10³ … 6.4·10⁴`,
`g/h ∈ {0.1, 0.25, 0.5, 0.9}`): accuracy exactly `x`, `ln(1/π†) ≤ n_o h + ln(n_o+1)` and `ln 2M̄ ≤ x − 1 + P_cnt` in all cases; in
those printed (`g/h ∈ {0.25, 0.5}`) `ln(1/π†) − n_o h ∈ [−6.3, −0.1]` and `ln 2M̄ − (x − 1) ≤ 4.6` against `P_cnt ≈ 25 … 34`.

*Part E — Proposition Q5.*  2016 cases (`u ∈ {½, 1, 2}`, `d = 1 … 64 000`, `x = 0.05 … 3ud`, `ln(1/δ) = 3 … d + 5`): the exact cost
is below `d·a + E_base` in all; least slack `11`.  At `u = 1`, `x = 0.5`: `ln cost − da = 44, 102, 262` for `d = 10³, 8·10³, 6.4·10⁴`
(`1.40, 1.14, 1.03` times `√d`) against `E_base = 104, 199, 465`.  Part E′ (Proposition Q5(b)): 86 cases with `x ≥ c′_d`
(`u ∈ {½, 1, 2}`, `d = 10³ … 6.4·10⁴`, `x/d ∈ [0.1, 0.75]ε*`, `δ ∈ {0.05, e^{-da}}`), no violation, least slack `8.5` nats.

### 7.2 The two inductive steps with a saturating inner family (`q2_step_checks.py` → `out_q2_step_checks.txt`)

The inner family is given the certified cost `d·B − σ·min(x, Rd)` *exactly* (error function `0`): the worst case
that the hypothesis allows.  The exact `ln C_max` of the new level — outer block, `θ`, ladder as in §4; `r†`, `K`, `J`,
`M̄`, `δ′` from the tables — is compared with the bound of Proposition Q6 or Q7.  `(B, σ, R)` run through the epoch
schedule (`m ≤ 8` resp. `12`, all `j`; a selection of five resp. four at `n = 10⁶`), `u ∈ {½, 1, 2}`,
`n ∈ {10³, 10⁴, 10⁵, 10⁶}`, `δ ∈ {0.05, e^{-n}}`, nine accuracies from `X₀(n)` to `2R′n`.

| | cases | violations | least slack `bound − exact` | size of the error term |
|---|---|---|---|---|
| slope step (Q6), `u = 1` | 1 068 | 0 | `6.9 … 24` nats | `c_S = 52 … 147` nats |
| slope step, `u = ½` and `2` | 2 636 | 0 | `7.4 … 28` | `49 … 162` |
| drop with shift (Q7), all `u` | 188 built | 0 | `6.9 … 19` | `c_D = 89 … 1850` |
| drop without shift | 516 built | 0 | `67 … 564` | — |

So both propositions are close to sharp for a saturating family (the least slack is `8`–`36 %` of the error
term), and they hold at `n = 10⁶` with failure probabilities down to `e^{-10⁶}`.

### 7.3 The nested design, exactly (`q3_scheme_exact.py` → `out_q3_scheme_exact.txt`)

The certified cost of `𝔊_M(n, 0.8715, 0.05)` — Theorem 11.56 applied level by level with the exact constants, base
brackets inside — for `M = 0, 1, 2` (`1`, `3`, `5` nested levels at `u = 1`), and for `M = 3` (`7` levels) below.  "proof": every level is the level as built
and nothing else; "min": the cheapest admissible procedure at every node (§4).  On **every node** visited the
inequality of the induction, `cost ≤ d·B − σ·min(x, Rd) + E^{(t)}(d, x; ln(1/δ) + d ln 2)`, is checked, and Lemma Q3 /
Lemma Q4 at every level built.  `u = 1`, in units of `na`:

| `n` | base (`M = 0`): exact | bound | `M = 1` (3 levels): proof | min | bound | `M = 2` (5 levels): proof | min | bound | two tuned levels (§11.19(1b)) |
|---|---|---|---|---|---|---|---|---|---|
| 1 000 | 1.349 | 1.928 | 1.349 | 1.349 | 3.910 | 1.361 | 1.361 | 5.771 | 1.138 |
| 1 400 | 1.287 | 1.725 | 1.287 | 1.287 | 3.107 | 1.288 | 1.288 | 4.413 | 0.993 |
| 2 000 | 1.230 | 1.561 | 1.230 | 1.196 | 2.486 | 1.231 | 1.196 | 3.369 | 0.872 |
| 4 000 | 1.152 | 1.348 | 1.152 | 1.033 | 1.726 | 1.154 | 1.014 | 2.103 | 0.726 |
| 8 000 | 1.101 | 1.221 | 1.093 | 0.938 | 1.322 | 1.120 | 0.849 | 1.437 | 0.642 |
| 16 000 | 1.069 | 1.143 | 0.974 | 0.883 | 1.110 | 0.918 | 0.756 | 1.102 | 0.590 |
| 32 000 | 1.047 | 1.095 | 0.906 | 0.850 | 0.987 | — | — | — | 0.565 |
| 64 000 | 1.033 | 1.064 | 0.864 | 0.830 | 0.915 | — | — | — | 0.541 |

(`B_M/a = 1, 0.792, 0.627`; "bound" is `(n B_M + 𝓔_M)/(na)` of Theorem Q8.  `M = 2` beyond `n = 1.6·10⁴` was not run: that row
alone took 19 minutes and `1.76·10⁶` node checks.  `u = 2` and `u = ½`, `M ≤ 1`: in the output; e.g. `u = 2`, `n = 1.6·10⁴`:
`0.914` / `0.826` / `1.009`.)

*Seven levels* (`q3_scheme_exact.py deep` → `out_q3_deep.txt`): `𝔊_3` (three epochs, `k_3 = 7`) at the sizes where the
direct recursion is feasible:

| `u` | `n` | five levels (`M = 2`): min / bound | seven levels (`M = 3`): min / bound | node checks (`M = 3`) | levels built in the nest of `M = 3`: slope steps; drops without shift; drops passed through |
|---|---|---|---|---|---|
| 1 | 1 000 | 1.361 / 5.771 | 1.361 / 7.489 | 2 035 | 112; 0; 72 |
| 1 | 2 000 | 1.196 / 3.369 | 1.202 / 4.195 | 28 117 | 3 021; 1; 512 |
| 1 | 4 000 | 1.014 / 2.103 | 1.015 / 2.466 | 289 625 | 39 655; 540; 2 066 |
| 2 | 1 000 | 1.113 / 5.208 | 1.113 / 6.379 | 95 449 | 10 661; 203; 1 052 |
| 2 | 2 000 | 0.907 / 2.925 | 0.889 / 3.453 | 1 073 743 | 150 729; 3 589; 3 019 |

(No violation; least slack of the induction `34`–`56` nats.  At these sizes a third epoch gains nothing or little:
the test is of the recursion, not of the cost.)

Reading.  (i) **No violation on `2.25·10⁶` node checks** (the three slopes together), nor on the `1.6·10⁶` of the deep run; the
least slack of the induction is `39`–`57` nats at `u = 1`, of Lemma Q3 `68`–`110`, of Lemma Q4 `0.03` (an outer block of
one coordinate).  (ii) The bound of Theorem Q8 is `280`–`600` nats above the exact value for three levels and
`480`–`610` for five (`9√n` at `n = 10³`, `2.4√n` at `6.4·10⁴`): the base bracket and the drops are bounded with their
worst-case `√`-terms, and the real base family is far cheaper than its linear majorant at extensive accuracies.
(iii) The level as built is not monotone ("proof", `M = 2`, `n = 8000`: `1.120` against `1.101` for the base); with the
choice by certified cost the cost never exceeds that of the inner family, up to the accuracy that the drops take.
(iv) **At these sizes the schedule of the proof is not competitive**: three levels are certified at `0.83·na` at
`n = 6.4·10⁴` and five at `0.76·na` at `1.6·10⁴`, where the tuned two-level design of §11.19 is certified at `0.54·na` and
`0.59·na` (and three tuned levels at `0.44·na` and `0.48·na`).  The epoch schedule copies the proof of the rate, which
is wasteful in levels (`B_1 = 0.79a`, `B_2 = 0.63a`, `B_3 = 0.50a`: seven levels for what the exact recursion does
with two), and its slope steps treat the base family as if it cost `e^{da}` at every accuracy; its purpose is
the order of the error term, not the size of `n` at which nesting pays.

### 7.4 The bound of Theorem Q8 in numbers (`q4_bound_table.py` → `out_q4_bound_table.txt`)

Formula evaluation only.  `u = 1`, `ε = 1`, `δ = 0.05`; best `M` for each `n`:

| `n` | best `M` | levels `k_M` | bound`/(na)` | `B_M/a` | `(bound − nh)/√(n ln n)` | `(bound − nh)/n^{3/4}` | `𝓔_M` in nats `=` base `+` slope steps (number `×` per level) `+` drops (`√`-part `+` rest) |
|---|---|---|---|---|---|---|---|
| `10³` | 0 | 1 | 1.916 | 1.000 | 2.21 | 1.03 | `102` |
| `10⁴` | 0 | 1 | 1.190 | 1.000 | 3.39 | 1.03 | `210` |
| `1.6·10⁴` | 2 | 5 | 1.098 | 0.627 | 3.77 | 1.04 | `836 = 259 + 2×107 + 238 + 124` |
| `3.2·10⁴` | 3 | 7 | 0.858 | 0.497 | 3.67 | 0.88 | `1 283 = 344 + 3×106 + 421 + 199` |
| `6.4·10⁴` | 5 | 13 | 0.707 | 0.388 | 3.75 | 0.78 | `2 266 = 465 + 7×98 + 760 + 357` |
| `10⁵` | 5 | 13 | 0.618 | 0.388 | 3.67 | 0.70 | `2 544 = 566 + 7×100 + 910 + 366` |
| `10⁶` | 10 | 43 | 0.371 | 0.289 | 3.24 | 0.38 | `9 112 = 1 660 + 32×97 + 3 492 + 863` |
| `10⁷` | 14 | 116 | 0.296 | 0.270 | 2.89 | 0.21 | `28 413 = 5 110 + 101×103 + 11 573 + 1 366` |
| `10⁸` | 17 | 268 | 0.2731 | 0.2656 | 2.71 | 0.12 | `83 105 = 16 014 + 250×112 + 37 278 + 1 837` |
| `10⁹` | 21 | 863 | 0.2660 | 0.2635 | 2.60 | 0.066 | `276 187 = 50 506 + 841×122 + 120 603 + 2 492` |
| `10^{10}` | 25 | 2 868 | 0.2637 | 0.2629 | 2.53 | 0.038 | `927 200 = 159 613 + 2 842×133 + 386 564 + 3 227` |
| `10^{12}` | 32 | 23 995 | 0.2628 | 0.2627 | 2.41 | 0.013 | `9.24·10⁶ = 1.60·10⁶ + 23 962×156 + 3.91·10⁶ + 4 776` |

(`h/a = 0.26265`.)  Reading.  (i) The bound is below `n·a` from `n ≈ 3·10⁴` on, and exceeds `n·h` by `0.011·na` at `n = 10⁸` and by
`0.001·na` at `10^{10}`.  (ii) `(bound − nh)/√(n ln n)` decreases slowly from `3.8` to `2.4`; `(bound − nh)/n^{3/4}` tends to
zero.  (iii) Up to `n = 10^{12}` the `√n`-terms (base and drops: `C₁ = 1.60 + 3.93 = 5.5` per `√n`) are as large as the level
term; a slope step costs `97`–`156` nats; the optimal number of levels is `≈ 0.05√n` at `n = 6.4·10⁴` and `≈ 0.024√n` at
`10^{12}`.  (iv) Other parameters: `ε = 0.1` gives `0.741`, `0.379`, `0.2738` at `n = 6.4·10⁴, 10⁶, 10⁸` (`C₁ = 6.3`); `δ = e^{-n}`
gives `0.7088`, `0.3717`, `0.2731` — an exponentially small failure probability costs `0.2 %`.  `u = ½`: `1.029`, `0.444`,
`0.2717` at the same sizes (`h/a = 0.2532`), `(bound − nh)/√(n ln n) ∈ [1.0, 1.8]`; `u = 2`: `0.561`, `0.363`, `0.3036`
(`h/a = 0.2968`), ratio in `[4.6, 8.7]`.  (v) The closed form of Theorem Q9(b), with the worst-case constants `c₁` and
`1 + r̄`, is much weaker at these sizes: `1.72`, `0.655`, `0.305`, `0.2673` (in units of `na`) at `n = 6.4·10⁴, 10⁶, 10⁸, 10^{10}`.

---

## 8. What is not proved; the weakest link

1. **Everything rests on Theorem 11.56** (paper proof, refereed, deterministic algebra machine-checked, the
   algorithm and its events not), on Lemma 11.55(a),(b)/K.4(c), Proposition K0, Harper's theorem, the binomial
   median and Chernoff–Hoeffding bounds, all quoted.  It is used here far from the parameters at which it was
   simulated: `θ = e^{Θ(n)}` together with a ladder of `Θ(n)` rungs, up to `√(n/ln n)` nested levels, inner failure
   probabilities `e^{-Θ(n)}`.  The statement covers these (it is the regime of Corollary K1.b), but no simulation
   does.  My checks evaluate the *bound* `C_max` exactly; they say nothing about the validity of Theorem 11.56.
2. **The weakest link of the new argument is Proposition Q6 (the slope step) with Lemma Q4**: a new statement
   about `r†` at an extensive `θ` and two pages of bookkeeping, unrefereed.  Both are tested on exact tables
   (§7.1 D, §7.2, §7.3), which tests the arithmetic at the sizes tried, not the proof.
3. **The composition is evaluated exactly only for `M ≤ 3` epochs** (three levels up to `n = 6.4·10⁴`, five up to
   `1.6·10⁴`, seven up to `4·10³`), i.e. only where the design is *not yet* better than the base family or than the
   tuned designs of §11.19.  The regime in which Theorem Q says something new (`n ≳ 3·10⁴` with `M ≥ 3`; `M ≈ 10`–`25`
   for `n = 10⁶ … 10^{10}`) is reached only through the single-step checks with saturating families (`n ≤ 10⁶`) and
   the proof: an exact evaluation of a deep design at large `n` is out of reach of the direct recursion (the
   number of distinct `(dimension, accuracy)` nodes multiplies by `≈ hn` per epoch).
4. **The constant.**  `C_*` comes from the worst-case constants `c₁`, `1 + r̄` of the machine-checked rate; the
   sharper asymptotics of the epoch sequences (remark (1) of §6.1) are numerical.  The `n^{1/2}` of Theorem Q9 is
   an upper bound for this method, not shown to be its true order.
5. **`n·h + O(√n)` is not proved** (§6.2): it needs a rate better than `1/k` for an explicit schedule.
6. **No lower bound** beyond Theorem 11.25(a): between `n·h − O(ln n)` and `n·h + O(√(n ln n))` nothing is known.
7. **Extensive accuracies** (the `o(n)` of Theorem 11.54) are not treated.  The rate at an accuracy rate `g`
   uses step (iii) of the proof (outer fraction `g/(g + θ_hint(g))`), a third kind of level; its outer accuracy
   rate `g + θ_hint(g) ≥ h` is again bounded away from zero, so I expect `n·θ_hint(g) + O(√(n ln n))` by the same
   method **[conjecture]**, but I did not write the finite-`n` form of that step.
8. **Dependence on `ε` and `δ`** is explicit in (5.2) but only (d) of Theorem Q9 is stated; for `ln(1/ε_n) = o(n)`
   the bound is `n·h + O(√(n·(ln n + ln(1/ε_n))))` by the same formulas, not written out.
9. Not checked: the Lean proofs behind (R) (statements read; the arithmetic re-checked numerically for 40
   epochs); Harper's theorem and the binomial median in the literature; other slopes than `u = ½, 1, 2` in the
   numerics; three tuned levels (`cert3.py`) against the error terms (Proposition Q1 and Corollary Q4a apply to
   every level of it, but I did not evaluate them there).

---

## 9. What I found wrong or imprecise in the theory report

1. **§11.19, remark (2), and the last sentence of the remark after Theorem 11.53** ("… the sub-exponential factors
   of a family with `k` nested levels would have to be bounded uniformly in `k`, and they are not"; "heuristically
   not better than `n^{3/4}`: each bounded level loses `e^{O(√n)}`, and `η → 0` needs `≈ 1/η` levels").  For the
   recursion whose rate is proved this is wrong on both counts: (i) with an explicit schedule the sub-exponential
   factors of `k` levels *are* bounded uniformly, by `exp(C₁√n + k·O(ln n))` (Proposition Q9a); (ii) of the `≈ 1/η`
   levels only `O(ln(1/η))` are bounded levels — one per epoch — and their `√`-losses are summable; the others close
   at `θ = e^{Θ(x)}` and lose polynomial factors.  The statement is true of the assembly in the proof of Theorem
   11.54 as written (dense tuples, no explicit `n₀`), not of the method.  The same heuristic is in `K_REPORT.md` §7,
   open problem 1, and in the brief.
2. **Theorem 11.52, "`M† = … = exp(nφθ_na((g−β)/φ) + o(n))`", and Corollary K1.b.**  The `o(n)` there is `O(ln n)` with
   an explicit constant (Lemma Q4: a factor `n_o + 1` after a polynomial slack in `θ`); the report never says so, and
   this is exactly the fact that separates a slope step from a bounded level.
3. **Lemma 11.55(c) as stated in the theory report** ("for every constant `θ > 0`: `Γ″(r) ≤ θ` for all
   `r ≤ p_u m − √((m/2)ln(2e^{u(m₀+2)}/θ))`, and the corresponding ball has `2^{-m}|B(m,r)| ≥ exp(−ma − O(√m))`") drops two
   hypotheses of Lemma K.4: `θ ≤ 2e^{u(m₀+2)}` (otherwise the square root is of a negative number; read `ln₊`), and
   `r₊ ≥ p_u m/2` for the size of the ball (for smaller `m` the proof gives nothing; `m ≥ m*(ℓ)` of Lemma Q3 is an
   explicit sufficient condition).  Harmless for the exponent, not for explicit constants.
4. **The constant of Lemma K.4(d)** is `u + ln 4`; the right leading constant is `u` (Lemma Q3), which is also what
   the tables show (`1.30 … 1.53` against `1.83` proved here and `4.36` there, at `u = 1`, `θ = η = 0.05`).
5. **Theorem 11.56, "`K = O(η^{-2} ln(nL/δ))`".**  The exact `K` is `⌈3(1+η)η^{-2} ln(2(J+1)(m_max+1)(L+2)/δ)⌉` with `J ∝ 1/λ` and
   `m_max ≈ n_o + log₂ ν₀`; the shorthand hides `λ` (and, through `ν₀`, `η′`, `θ`, `ν₁` inside a double logarithm).  Harmless.
6. **The brief, §2: "the excess over the limit, in nats, is about `1.2·√n` for two levels".**  It is `2.24√n` at
   `n = 10³` and `1.13√n` at `6.4·10⁴` (§7.1 C): `30`–`40` nats of polynomial factors and, from `n = 4000` on, the gap of
   the 40-rung geometric ladder at the rung that carries the maximum, are not `√n`-terms.
7. **The brief, §3 item 2: "the two-sample bracket costs `exp(d·θ_na(x/d) + O(√d))`"** (not a statement of the theory
   report, whose Proposition 11.57(a) has `O(√d)` at fixed accuracies and an exponent function elsewhere).  What the
   proofs give uniformly in the accuracy is `O(√(d ln d))` for `x ≥ c′_d` (Proposition Q5(b): a shift of the accuracy
   by `2 ln d + O(1)`, paid through the modulus of `θ_na` at zero when `x` is small) and `O(√(d ln(1/x)))` at bounded
   accuracies; a uniform `O(√d)` in the window `1 ≪ x ≲ ln d` would need a sharper bound for `Γ″` than `3(d+1)Γ̃`
   **[not done]**.  At a rate `x/d` bounded away from zero the error is `O(ln d)`.

---

## 10. Files and commands

All in `experiments/workstreams/Q/`; Python 3, numpy (and mpmath in one check); run from that directory, one process at a time; the
referee's `experiments/reviews/R8/r8_flat.py` is imported, nothing in it is changed.

| file | what | command | time |
|---|---|---|---|
| `qlib.py` | constants of the cube and of the rate; epoch sequences; exact constants and `C_max` of one level (formulas of `r8_flat.flat_run`); the base family; every error term of this report (`cS`, `qS`, `cD`, `qD`, `cpi_bar`, `E_base`, `E_total` = (5.2)); self-test against `flat_run` | `python3 qlib.py` | 1 s |
| `qscheme.py` | the families `𝔊_0`, `S[·]`, `D[·]`, `𝔊_M` with their exact certified costs and the node-by-node check of the induction; `Synthetic`: a family whose cost equals a majorant | (library) | |
| `q1_one_level.py` → `out_q1_one_level.txt` | §7.1 (needs mpmath for one part) | `python3 q1_one_level.py > out_q1_one_level.txt` | 20 s |
| `q2_step_checks.py` → `out_q2_step_checks.txt` | §7.2 | `python3 q2_step_checks.py > out_q2_step_checks.txt` | 45 s |
| `q3_scheme_exact.py` → `out_q3_scheme_exact.txt`, `out_q3_deep.txt` | §7.3 | `python3 q3_scheme_exact.py > out_q3_scheme_exact.txt` (`quick` as argument: 4 min); `python3 q3_scheme_exact.py deep > out_q3_deep.txt` | 25 min; `deep`: 2.5 min |
| `q4_bound_table.py` → `out_q4_bound_table.txt` | §7.4 | `python3 q4_bound_table.py > out_q4_bound_table.txt` | 15 s |

Memory: the largest arrays are the referee's tables for one cube (`≤ 10⁶` floats in `q2`, `≤ 6.4·10⁴` otherwise);
at most six tables are cached.
