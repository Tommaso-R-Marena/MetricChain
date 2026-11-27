> **Repository note (added by the coordinator).**  Report of the independent referee R8 on
> workstream K (`docs/workstreams/K_REPORT.md`; brief: `docs/reviews/R8_brief.md`), as delivered,
> with the scratch path replaced.  The referee's scripts and outputs are in
> `experiments/reviews/R8/` (run from that directory).  What was done with the findings:
> theory report §11.19 ("What the referee checked"), `docs/DEAD_ENDS.md` D46 (items 5, 6), and the
> errata note at the head of `K_REPORT.md`.  The files that the referee says it did not review
> because they were added during the review — `proofs/Frontiers/BoundedAccuracy.lean` and the
> repository copy of the report — are the four Lean files it compiled, merged, plus the
> coordinator's `exactRec_ge_hint`, `exactRec_tendsto_hint`, `exactRec_reaches_hint_of_pair`.

# R8 — Referee report on workstream K ("the adaptive exponent at every bounded accuracy")

Object reviewed: `scratchpad/ws/K/REPORT.md` (965 lines; Theorem K3 and its chain K.1 – K5), the four Lean files
`KBounded.lean`, `KBoundedLink.lean`, `KBoundedCube.lean`, `KExactRecursion.lean`, and as context the theory report
§11.10, §11.16, §11.18, `docs/reviews/R7_referee_report.md`, `docs/DEAD_ENDS.md` D45, `proofs/Frontiers/HintRecursion.lean`,
`proofs/Frontiers/CubeHintPair.lean`, `proofs/Frontiers/QueryRefinements.lean` (statement of the lower bound) at commit `4cef47e`.
`scratchpad` = the session's scratch directory (the referee's scripts and outputs are reproduced in `experiments/reviews/R8/` of the repository).

Everything below is my own work in `scratchpad/referee8/` (scripts at the top level, outputs in `out/`).  Nothing under
`/home/user/MetricChain` was modified, no state-changing git command and no `lake build` was run, nothing was delegated.  The
author's scripts were not run and not used; I read the report's §6 and §9 to see what had been tested (and eleven comment/code
lines of `stable_multinomial.py`, to see which numpy sampler the report's remark in §6.8 refers to).  Python: `ulimit -v 4000000`,
one process at a time, every run under ten minutes.  While I worked, another process changed the repository
(`docs/THEORY_REPORT.md`, `docs/BLUEPRINT.md`, `proofs/AxiomAudit.lean` modified; `proofs/Frontiers/BoundedAccuracy.lean`,
`docs/workstreams/K_REPORT.md` new; seven commits, HEAD `88468ad` when I finished).  I read the context files before those
changes (or through `git show 4cef47e:`) and did **not** review the new files.  The Lean files I compiled against
(`HintRecursion.lean`, `CubeHintPair.lean`, `QueryLowerBound.lean`, `QueryRefinements.lean`) are unchanged since `4cef47e`
(`git diff` empty).

## 0. Summary

**Verdict on Theorem K3: proved** — a paper proof which I re-derived line by line and could not break, given
(a) the two machine-checked inputs (LB) = Theorem 11.25(a) and (R) = convergence of the exact level recursion (both compile
against the repository with axioms `propext, Classical.choice, Quot.sound` only; statements read, no hidden hypothesis), and
(b) three quoted classical facts: Harper's vertex-isoperimetric theorem, the Chernoff/Hoeffding bounds, and the binomial-median
fact of Kaas–Buhrman.  I found **no critical and no major error**.  The proof of Theorem K3 itself has no gap; two of its
ingredients (Theorem K1 as a "bracket procedure", Theorem K2) have minor gaps, which are closed in §2.
The chain K1 → K.4 → K0 → K1.b → E → K2 → K3 is sound;
the accounting of Theorem K1 (the part with the bad history) is right, including the Harper term, the closing radius, the sample
sizes and the count ("the two factors `e^b` cancel").  All defects found are minor (wording of the abort rule, an inconsistency
between "exponent functions are nonincreasing" and "`T′(ξ) = T(ξ)`", a few labels that say more than is machine-checked, two
false side remarks); each has a one-line repair, given in §2.

What supports the verdict, beyond re-derivation:

* **Lemma K.4 in exact arithmetic** (`e^u` rational): all of (a)–(d) and (Me) for 5 values of `e^u`, 4 of `η`, 6 of `θ`,
  `m ≤ 4000`: 0 violations; (Me) in 48 120 further exact cases; Harper's theorem in the form used, exhaustively for `m ≤ 4`.
* **Own implementation of Algorithm 2L⁺** from the text of §2.2: about 15 000 runs with a simulated adversarial inner oracle
  and the constants of the theorem (enumerated non-radial cubes, radial landscapes with every point individual, radial
  landscapes with `n_o ≤ 520` and exact samples up to `2·10^18` points, the regime of Corollary K1.b with `θ` up to `e^40`, the
  regime of Theorem K2 with all four constants down to `0.025`): **no claim (i)–(vi) of Theorem K1 violated**, the good event
  never failed; about 7 500 further runs with `K` divided by 8–40, where the good event fails in up to 31 % of the runs: **no
  claim violated on any run on which the events used by the proof hold**, false certificates only off them; five mutations
  (the four required and one more) **all detected**, on all three engines.
* **Real inner brackets**: 475 runs of the two-level algorithm with `3.6·10^7` real two-sample brackets (Proposition K0) on
  `Q_12, Q_13`: every final bracket valid and within `x_out`; and — not done before by anybody — **three nested levels**
  (2L⁺ inside 2L⁺ inside K0) on `Q_9, Q_10` with the constants of the theorems: 16 outer and 9 920 middle runs,
  `2.3·10^8` bottom brackets, no invalid bracket, no violated claim.
* **Exact cost at the flat instance**, two levels (`n ≤ 64 000`, `u = ½, 1, 2`) and three levels (`n ≤ 64 000`, `u = 1`): never
  below the hinted lower bound (two levels: never above `C_max`); three levels cost `e^{0.379·na}` at `n = 64 000` against
  `e^{0.514·na}` for two levels (limits `τ₃/a = 0.361`, `τ₂/a = 0.500`; `h/a = 0.263`): the gain of a further level at bounded
  accuracy that Theorem K2 asserts is visible in actual costs.  The same at target accuracies down to `0.05`.
* The recursion with the point `g = 0` re-computed with my own discretisation: the table of §6.1 reproduced to `10^{-4}`
  (`k ≤ 8`), `τ_k ≥ h` and `T_k ≥ θ_hint` throughout; Proposition K5(b) could not be broken by a search over `(φ, ξ)` and over
  60 000 random ladders for seven slopes.
* The exponent of the hinted lower bound is `h` in all three regimes of the brief (fixed `ε`; `ε_n → 0`, `ln(1/ε_n) = o(n)`;
  `ε_n → ∞`, `ε_n = o(n)`), checked from the statement of Theorem 11.25(a) and numerically up to `n = 10^6`.

## 1. Verdict per statement

"proved" = I re-derived every step and agree; inputs are named.  Gaps are listed with their status.

| statement | verdict | remarks |
|---|---|---|
| **Lemma K.1(a)** (mass above a threshold) | **proved**, given Harper (H) | complement trick `|Dᶜ| ≥ |B(m, m−r−1)|`, erosions `D_i = (N^{i−1}(Dᶜ))ᶜ`, `|D_i| ≤ |B(m, r+1−i)|`, Abel summation: all re-derived; needs `r ≤ m−1` exactly as stated.  (H) is quoted from memory; the form used (`|S| ≥ |B(m,k)| ⇒ |N^i(S)| ≥ |B(m,k+i)|`) is the standard corollary of "initial segments of the simplicial order minimise the neighbourhood"; checked exhaustively on all 65 808 nonempty subsets of `Q_1…Q_4` and on 200 000 random/structured subsets of `Q_5, Q_6`; (a) at 56 814 thresholds of 672 `u`-Lipschitz functions, equality attained (`r8_tail.py`) |
| **Lemma K.1(b)** (mass below a threshold) | **proved**, given (H) | same checks; needs `S ≠ ∅`, `k ≥ 0` as stated |
| **Lemma K.2** | **proved** | term by term |
| **Theorem K1, the good event** `P(𝒢) ≥ 1 − δ` | **proved** | Chernoff constants compatible with `K`; number of events `(J+1)(m_max+1)(L+2)` right; thresholds depend on `ψ₀` only; union bound over *potential* inner calls legitimate (deterministic index set `i ≤ K2^{m_max}`, inner randomness independent of the outer points); `M̄ ≤ K2^{m_max} < 2M̄`; no circularity (`J → ν₀ → r†, π† → m_max → K → ν, M†, M̄ → δ′`) |
| **K1 (i)** no abort, stop at a level `≤ J` | **proved** | Step 9 re-derived (level `J`: nothing is high, `M_J^neg > K2^{n_o}/(1−η)`, tail `0` before (e)) |
| **K1 (ii)** validity and certificates | **proved** | including the Harper term (`k` well defined, `0 ≤ k ≤ n_o − 1`, `|{W ≥ t}| ≥ max(1, 2^{n_o}p̲) ≥ |B(n_o,k)|`), the sum-form lower end (disjoint intervals `(t_{i−1}, t_i]`, the current level may be added when populated), the upper end (`r ≤ n_o − 1`; `2^{n_o}q < 1 ⇒ {W > s_j} = ∅`) |
| **K1 (iii)** closing radius `> r†` | **proved**; holds **deterministically** (on and off `𝒢`) | edge cases checked: `q = 1` (`r = n_o`), `r = 0` (`2^{n_o}q = 1` exactly), `r† = −1`, level populated at `M = K` (`q = 1`), `2^{n_o}q < 1` (test passes) |
| **K1 (iv)** sample sizes | **proved**; deterministic as well | so the abort "`M` would exceed `K2^{m_max}`" can never fire, even off `𝒢` (the report only says "on `𝒢`") |
| **K1 (v)** the count | **proved** | both cases (`s_je^{−x} < s₀`; largest `i` with `s_i ≤ s_je^{−x}`), populated and negligible predecessor; (V3) at the last size suffices; in simulation the bound is reached to 98 % |
| **K1 (vi)** calls and cost | **proved** | a point's rung persists, one call per point and rung in the whole run |
| **K1** width `U ≤ e^{x_out}L` on and off `𝒢` | **proved** | term by term; no width violation in any simulated run, also off the good event |
| **K1** "is a bracket procedure with cost `C_max`" | **proved with a gap (closed)** | the abort test must be made *before* an inner call ("would exceed"), and off `𝒢` the returned pair can have `L > U`; both harmless, repairs in §2 (m1) |
| **Lemma K.4(a)** | **proved** | exact arithmetic: `max Γ̃/(2e^u m) ≤ 0.93` |
| **Lemma K.4(b)** | **proved**, given (Me) | (Me) quoted from memory: confirmed (Kaas–Buhrman 1980, as cited in the standard references; exact check in 48 120 cases, smallest value `0.50998`); only *some* constant in place of `½` is needed |
| **Lemma K.4(c)** | **proved** | exact tables of `r†` against `r₊`: `r† − r₊ ≥ 0`, equality occurs |
| **Lemma K.4(d)** | **proved** | `max(lhs − rhs) = −4.2` |
| **Proposition K0** | **proved** | three events, `t⁺, t⁻` with ties, validity, ratio, family; cost at fixed accuracy, at accuracy `→ 0` (E0′) re-derived; the extensive regime (`T₁ = θ_na`) is only sketched in the report ("exactly as in the proof of Corollary K1.b") — I carried it out, it is right.  Simulation: 40 320 brackets, none invalid, none wider than certified |
| **Corollary K1.b** | **proved** | accuracy exactly `Gn`; `r† ≥ min(n_o − 1, ⌊ρ‡n_o⌋)`; all parameters inside the hypotheses of K1 for large `n` |
| **Proposition E(a)** | **proved** | induction complete: the family of step `k+1` is needed at step `k+2` only at single rates `ξ_l`, one family per rung, and Corollary K1.b uses `T` at the rungs only; the shift `ι`, the case `y_L = u < β/(1−φ)`, `μ′ ≤ μ` all right |
| **Proposition E(b)** | **proved**, given (R) | |
| **Theorem K2** (incl. (a), (b), uniform version) | **proved with a gap (closed)** | "`T′(ξ) = T(ξ)` for `ξ > 0`" contradicts "exponent functions are nonincreasing" when `T′(0) < T(ξ)`; replace by `min(T(ξ), T′(0))` (m2).  Accuracy budget, hypothesis of K.4(c), `n ↦ n_i` all checked |
| **Theorem K3** | **proved**, given (LB), (R), (H), (C)/(Ho), (Me) | iteration, `φ = min(½, η/a)`, `ξ = min(ε*/2, φη)`, accuracies `ε/2^j`, failure probabilities, worst-case and expected cost |
| **Corollary K3′(i)** | **proved** | |
| **Corollary K3′(ii)** | **proved** | uniform bookkeeping of §3.2/§3.4 re-derived; numerically (§4.6): cost of the base bracket at `x_d = d^{-2}` is `e^{1.03·da}` at `d = 10^6`; the two-level algorithm at target accuracy `0.05` (all four constants `0.0042`) at the flat instance is valid, within its width, between the hinted bound and `C_max`, and costs `e^{0.547·na}` against `e^{0.513·na}` at accuracy `0.87` (`n = 16 000`) |
| **Proposition K5(a)** | **proved** | |
| **Proposition K5(b)** | **proved** | convexity argument re-derived, both cases; numerical attack failed (`min(bound − h)/h = +2·10^{-10}`, attained only as `φ → 0`) |
| **Proposition K5(c)** | **proved** (machine-checked core + two paper steps) | `T_k ≤ τ_k` and the step at zero verified by hand |
| K5(d), §6.1 | numerical, **reproduced** for `k ≤ 8`, `u = ½, 1, 2` | |

## 2. Errors and gaps by severity

### Critical
None.

### Major
None.

### Minor

* **m1. Abort rule and output format off the good event** (REPORT lines 207–208, 332; definition lines 139–141).
  (a) "Abort … if the number of queries exceeds `C_max`" bounds the cost by `C_max + max_l C_l`, not `C_max`, if read literally.
  *Repair:* test before every inner call whether `(queries so far) + C_l > C_max`.  (b) Off `𝒢` a stop through the closure
  test can return `L > U` (e.g. a pass that is populated although `2^{n_o}q < 1`: then `tail = 0` and the current level enters
  `L` but not `U`); the definition says "returns `L ≤ U`".  Harmless for every use made (an outer level counts such a call as a
  failure of (V1), and its own cost is capped), but either say "returns a pair" or return the trivial bracket when `L > U`.
* **m2. Exponent functions** (lines 143–151, 478).  An exponent function is required to be nonincreasing on `[0,∞)`; Theorem
  K2 defines `T′(ξ) = T(ξ)` for `ξ > 0` and `T′(0) ≤` (3.1), which is not nonincreasing when (3.1) is below `T(0+)` (this is the
  typical case: base family, `T(0+) = a`).  *Repair:* `T′(ξ) := min(T(ξ), T′(0))`; legitimate because a procedure of bounded
  accuracy `x` serves the accuracy `ξd` for `d ≥ x/ξ`.  Monotonicity of a family's exponent function is in fact never used in
  §3–§4 (only that of the `T_k` of the exact recursion, which is machine-checked).
* **m3. Hypotheses of Theorem K1 that the proof does not use.**  `λ ≤ 1` and `η′ ≤ 1` are not used; `ν₁ ≥ 1` is used only for
  `(1−η)ν₀ ≥ 1`.  Conversely claims (iii), (iv) and Steps 5, 6 use no probability at all (cf. §1).  Not an error.
* **m4. (H) and (Me) "from memory"** (lines 92–99).  Both statements are correct as used.  Kaas–Buhrman: every median lies in
  `[⌊mp⌋, ⌈mp⌉]`, hence `P(Bin(m,p) ≥ k) ≥ ½` for integers `k ≤ mp`.  I confirmed the attribution through secondary sources
  only (not the 1980 paper itself) and by exact computation.
* **m5. False side remark on the one-sided ratio** (lines 69–71, 410–413, 638–640): "`Γ̃` … never below `4e^u(e^u−1)`" and
  "`3 + 12Γ(r)` is never below `3 + 48e^u(e^u−1)`".  With the report's own convention `Γ̃(0) = e^u − 1` this fails at `r = 0`,
  and for `r ≥ 1` the minimum is slightly *below* the limit at finite `n` (`18.672 < 18.683` at `n = 12 800`, `u = 1` — the
  report's own number in §6.3).  Correct statement: `min_{r≥1} Γ̃(r) = 4e^u(e^u−1)(1 − o(1))`.  Likewise "the window is empty
  unless `G − b ≥ ln(16e^u(e^u−1))`" ignores `r = 0`, where the sketch's test holds from `G − b ≥ ln(4(e^u−1))` on (a sample of
  `2^{n_o}K` points — useless, but not "empty").  Immaterial for the theorems.
* **m6. False remark on numpy** (lines 818–826): "numpy's `binomial` returns `0` for `p < 10^{-16}` whatever `n`".  In this
  environment (numpy 2.5.3) `Generator.binomial` is correct down to `p = 10^{-20}` (`n = 2^59`); only the legacy
  `RandomState.binomial` fails, and only in its inversion branch (`np ≤ 30`), not "whatever `n`".  The statement about
  `multinomial` is true (upper-tail cells lose their mass: shell 219 of `Q_300` gets 80 instead of 144 points at `n = 2^59`,
  shells `≥ 222` none) — `r8_numpy_tail.py`.
* **m7. Non-adaptive row of the table in §7** (line 847): "`→ 0`, `ln(1/ε) = o(n)`: `a` (… lower bound Theorem 11.45)".  True,
  but the lower bound needs one line that is not there: `D_R > ε_n` as soon as `KL(R/n‖p_u) < ln(1/ε_n)/n + o(1)`, so `R/n → p_u`.
* **m8. Last sentence of Corollary K3′** (lines 553–556): "the adaptive exponent … is `θ_hint(lim ε_n/n)` for every accuracy with
  `ln(1/ε_n) = o(n)`" presupposes that the limit exists.  (The upper bound of (ii) in fact holds for every sequence with
  `ln(1/min(ε_n, 1)) = o(n)`, convergent or not, because (E0′) is stated for arbitrary sequences `x_d ≤ 1`.)
* **m9. Remark (2) after Theorem K3** (lines 538–542) presents `bounded_iterates_lt`, `levels_reach_hint_at_zero`,
  `cube_levels_reach_hint_at_zero` as the machine-checked "contraction"; they formalise Proposition K5(c), not the iteration of
  Theorem K3, which is `two_rung_bound` (§6.7 of the report says this correctly).
* **m10. A point for implementers** (Step 1).  "`L ≥ Ue^{−x_L} > s_je^{−b}`" is exact arithmetic.  With `x_L = b` and a fibre
  average exactly on the ladder of tolerance thresholds, a floating-point bracket `[W, We^b]` can satisfy `U > s_j` and
  `L ≤ s_je^{−b}` simultaneously, and the algorithm as written aborts ("unclassified at rung `L`").  I met this once
  (`λ` a divisor of `b`, flat profile); a generic `λ` or a tie rule removes it.

## 3. Statements in the report that say more than is proved

1. **§0 and line 27, "Theorem K3 [proved, given Theorem 11.25(a) … and Theorem 11.53 …, both machine-checked in the
   repository]"**.  The theorem rests in addition on Harper's theorem, on the binomial median and Chernoff/Hoeffding bounds
   (quoted), and on ten pages of paper proof (K1, K.4, K0, K1.b, E, K2) that had not been refereed.  Moreover the second input
   is "machine-checked in the repository" only up to `cube_iterates_lt_hint_add`; that the *defined* sequence satisfies its
   hypotheses is in the workstream's scratch file `KExactRecursion.lean` (correct, see §5), not in the repository at `4cef47e`.
2. **Line 217, "Theorem K1 [proved; deterministic core machine-checked (`KBounded.lean`); …]"**.  `KBounded.lean` contains four
   algebraic lemmas (lower Riemann sum, populated part, the algebra of the count, the algebra of the width).  The new
   deterministic content of the theorem — the Harper term and its validity, the closing radius (Step 5), the sample sizes
   (Step 6), termination (Step 9) — is not formalised.  "The algebra of the width and of the count is machine-checked" would
   be accurate (this is how §9 puts it).
3. **Line 217, "every step checked in simulation (§6.2)"**: with a simulated oracle (V1) holds by construction, and the cost
   of the inner procedures is not simulated (the report says so in §6.2); only §6.5 (84 runs, `n ≤ 14`) has real brackets.
4. **§6.8** (numpy `binomial`), **§0/§3.2/§5** (`Γ̃` "never below"): false as stated (m5, m6).
5. **§7 table and Corollary K3′, last sentence**: see m7, m8.
6. **Proposition K5 header, "(c) machine-checked for the cube"**: the Lean theorem is about abstract sequences `T_k, τ_k`;
   that the recursion at accuracy zero satisfies its two hypotheses about `τ` is on paper (the body of K5(c) says so).
7. **§5(2), header "[proved: Lemma K.4, Theorem K1(iii); numerical: §6.3]"**: what is proved is the repair.  The negative
   statement about the sketch ("populated levels do not close in that window at all") is a [sketch] with numerics, as the
   body says; it is not used in any theorem.

Nothing in the report claims a *theorem* that is not proved.

## 4. Numerical work (own code; none of the author's)

All commands are run from `scratchpad/referee8/` as `ulimit -v 4000000; python3 <script> <args>`; outputs in `out/`.
Runs with a time limit stop after the stated number of seconds, so the number of completed runs depends on the machine.

### 4.1 Exact arithmetic for §3.1 and §1.2

| command (run time) | what | outcome |
|---|---|---|
| `r8_k4_exact.py` (65 s) → `out/k4_exact.txt` | Lemma K.4(a)–(d) and (Me) with `e^u ∈ {5/4, 3/2, 2, 3, 8}`, `η ∈ {½, ¼, 1/10, 1/50}`, `θ ∈ {1/100, 1/20, ⅓, 1, 5, 40}`, `ν₀` the smallest allowed, all `m ≤ 160` and `m ∈ {200, …, 4000}`; tables of `E_r`, `T_k`, `κ`, `Γ̃`, `Γ″`, `r†` as exact rationals (self-test against the definitions); Hoeffding, `r₊`, the right side of (d) at 60 digits (distance of the argument of the floor from an integer `≥ 3·10^{-5}`) | **0 violations** in (a), (b: both parts and Hoeffding), (Me), (c) (up to 816 cases per line, `min(r† − r₊) = 0`), (d) (up to 675 cases per line, `max(lhs − rhs) = −4.2`); `max Γ̃/(2e^um) = 0.93`, `max Γ″/bound = 0.91`; `(ln(1/π†) − ma)/√m` up to `2.9`: the `O(√m)` is real |
| `r8_median.py` (118 s) → `out/median.txt` | `P(Bin(m,p) ≥ ⌊mp⌋) ≥ ½` and `P(Bin(m,p) ≤ ⌈mp⌉) ≥ ½`, exact integers, `p = i/D`, `D ∈ {30, 64, 97}`, `m ≤ 240`, and 3000 random `(m ≤ 1500, p)` | 48 120 cases, 0 violations, smallest value `0.509977` |
| `r8_tail.py` (11 s) → `out/tail.txt` | (H) and Lemma K.1 | see §1 |
| `r8_sampler_test.py` (1 s) → `out/sampler_test.txt`; `r8_numpy_tail.py` (2 s) → `out/numpy_tail.txt` | own tail-safe multinomial sampler (binary splitting over the shells with exact conditional probabilities; inversion with `log1p` for small means) at `N = 2^59` on the shells of `Q_300`; numpy's own samplers there | own sampler: totals preserved, 46 tail shells with expected counts `10^{-3} … 10^7`: largest `|z|` of the means 3.1, variance/mean ≈ 1; numpy: see m6 |
| `r8_gamma.py` (3 s) → `out/gamma.txt` | side claims of §5(2), §6.3 | reproduced: `min_{r≥1}Γ̃ = 18.672` (`n = 12 800`, `u = 1`); `Γ̃(⌊p_un⌋)/√n = 0.64, 2.58, 19.1`; `r† = 3313 ≥ r₊ = 3246` (`p_un = 3442`), `ln(2ⁿ/|B(n,r†)|)/(na) = 1.097`; window `KL(ρ₊‖½)/a = 1.0896, 1.0112, 1.0015`; thresholds `2.84, 4.31, 6.63` |

### 4.2 Algorithm 2L⁺ with a simulated inner oracle (`r8_core.py`, `r8_pops.py`, `r8_sim.py`)

Implementation from §2.1–§2.3 only.  `q`, `p̲` and all radii are exact (Fractions against integer ball sizes; `q = 1` gives
`r = n_o` exactly); levels, `ℓ`, tails in logarithms.  The inner oracle returns a valid bracket of ratio `e^{x_l}` placed by
one of seven rules (random; value at the top / bottom / middle; two adversaries that keep a point unclassified at the current
level as long as a valid bracket allows and then make it high, resp. low; a mixture).  Random parameters:
`λ ∈ [0.2, 1]`, `η ∈ {½, ⅓, ¼}`, `η′ ∈ {0.1, 0.5, 1}`, `θ ∈ {0.05, …, 50}`, `b ∈ {0.2, …, 2.5}`, `ν₁ ∈ {1, 2e^un_o/θ}`, `L ∈ {1, 2, 3}`
with random ladders, `x_L ≤ b`, `δ = 0.05`; all constants from the formulas of §2.2.

*Checked on every run:* the good event — (V2), (V3) exactly on the realised sample, both "all levels `0..J` × all realised
sizes" and "exactly the events the proof uses on this run" —; (i) stop at a level `≤ J`, no abort; (ii) `L ≤ A ≤ U`,
`p(s_j) ≤ q` and `p̲ ≤ p(s_je^{−b})` at *every pass*, `ℓ ≤ A` at every update; the width and its four components; (iii) `q_j > π†`
and `r(q_j) > r†` at every level left; (iv) `M ≤ max(K, 2M_j^neg)`, `M_j^neg ≤ (1+η)e^λν₀M†`, `M ≤ M̄`; (v) the count for a grid of
`x` and all rungs, and the sampled count against `cnt(x)`; (vi) calls per level and rung, total calls, number of points.

| command (time) | instances | runs | outcome |
|---|---|---|---|
| `r8_sim.py enum 4000 101 none 1 500` (about 100 s) | 15 families of `u`-Lipschitz functions (McShane extensions, inf-convolutions of noise, mixtures, additive, dips, cones, cliffs, …; 12 non-radial) on enumerated `Q_{n_o} × Q_{n_i}`, `n_o ∈ 6..9`, `n_i ∈ 3..5`, `u ∈ {½, 1, 1.5, 2}`; every point its own bracket | 4000 | **0 violations; good event never failed**; 142 323 levels left as populated, 71 as negligible (29 runs); closures: 1959 empty tail, 439 at a populated pass, 1602 at an unpopulated one, 1277 at a radius `≤ r†`; widest bracket 6.45, closest to the width bound 0.034; count/bound `≤ 0.79` |
| `r8_sim.py radial 1500 102 none 1 520` (520 s, time limit) | 12 radial profiles (flat, cones, dips, mesa, walk, periodic, staircase `W ∝ 1/|B(d)|`, critical slope, dip at the hinted radius), `n_o ∈ 10..26`, points individual, up to `8·10^6` points | 1128 (290 skipped: more than `2^23` points; an earlier execution of the same command completed 1161) | **0 violations**, good event never failed; 222 negligible levels (39 runs) |
| `r8_sim.py grouped 4000 103 none 1 500` (about 200 s) | the same profiles, bounded regime `ν₁ = 2e^un_o/θ`, `(u, n_o) ∈ {½}×{240, 380, 520} ∪ {1}×{90, 130, 170} ∪ {2}×{34, 44, 54}`; the sample is exact but stored as counts per shell and block (own tail-safe sampler, `r8_sampler_test.py`), one bracket per (block, shell) | 3786 (214 skipped: more than `2^61` points) | **0 violations**, good event never failed; 2429 negligible levels (245 runs); 521 closures at a populated pass (Harper term); largest sample `2.2·10^18`; closest to the width bound 0.020 |
| `r8_sim.py neg 2000 104 none 1 300` (about 50 s) | `ν₁ = 1`, `u ∈ {1, 1.5, 2}`, `n_o ∈ 34..60`, aimed at the negligible branch | 2000 | **0 violations**; 1545 negligible levels (230 runs) |
| `r8_sim.py k1b 3000 51 none 1 300` (41 s) | parameters of Corollary K1.b: `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, `θ ∈ {e², …, e^40}` | 3000 | **0 violations**; 1717 closures at a radius `≤ r†`; widest bracket 44.7 (bound 44.8) |
| `r8_sim.py unif 2000 52 none 1 420` (420 s) | parameters of Theorem K2: `λ ≈ η = η′ = θ = c₀ ∈ {0.1, 0.05, 0.025}`, `b = 6c₀`, `ν₁ = 2e^un_o/θ` | 1061 (101 skipped) | **0 violations**; 13 712 negligible levels; widest bracket 0.965; count/bound up to 0.978 |
| `r8_sim.py enum 3000 208 none 8 200`, `… enum 3000 2040 none 40 200`, `… grouped 1500 301 none 16 200` (about 30 s, 25 s, 80 s) → `out/sim_Kdiv.txt` | `K` of the theorem divided by 8, 40, 16 | 3000, 3000, 1489 | events used by the proof fail in 29, 942, 442 runs; **on the runs where they hold: 0 violations**; off them: false certificates in 19, 613, 303 runs (`p̲`, `q`, once an invalid `L`), never a width violation |

*Negative controls* (`out/sim_mutations.txt`; `r8_sim.py <engine> <600|150> 41 <mutation> 1 100` for the engines `enum`,
`radial`, `grouped`; each under 62 s): every mutation is detected by the check it should break, on every engine.

| mutation | detected as | `enum` (600 runs) | `radial` (≈120) | `grouped` (≈570) |
|---|---|---|---|---|
| lower end without the sum (`maxform`) | width / populated part of the width | 111 / 240 | 22 / 49 | 262 / 338 |
| no Harper term (`noharper`) | level left with `r ≤ r†` (iii) | 12 | 2 | 88 |
| tail lemma at `r = n_o` (`close_at_no`) | upper end below `A` | 536 | 127 | 418 |
| negligibility threshold without `e^{−b}` (`neg_tol`) | the count (v) | 386 | 71 | 316 |
| `q` without `1/(1−η)` (`q_plain`) | certificate `p(s_j) ≤ q` | 262 | 41 | 350 |

*What these runs do not exercise:* (V1) (the simulated oracle is always valid); the cost of inner procedures; non-radial outer
landscapes beyond `n_o = 9`; in the `grouped` engine the points of one (block, shell) share a bracket, so the oracle is valid
but correlated.  With the constants of the theorem the good event never failed in about 15 000 runs: the Chernoff/union bound
is very loose, and the frequency `δ` is not tested from below.

### 4.3 Real inner brackets (`r8_e2e.py`, `r8_three.py`)

| command (time) | what | outcome |
|---|---|---|
| `r8_e2e.py A 7` (12 s) → `out/e2e_A.txt` | Proposition K0 on 18 functions × 40 repetitions per parameter set, `d ∈ {9, 10, 11}`, `u ∈ {½, 1, 2}`, `x ∈ {0.5, 1, 2, 4}`, `δ′ ∈ {0.3, 0.02}` | 40 320 brackets (16 parameter sets served by enumeration): **none invalid, none wider than certified**; one of the three events of the proof failed 6 times (all at `δ′ = 0.3`, bound `0.29–0.30`) |
| `r8_e2e.py B 600 9 520` (522 s) → `out/e2e_B.txt` | Algorithm 2L⁺ with the bracket of Proposition K0 on every fibre, `(n_o, n_i) ∈ {(6,6), (7,6), (6,7), (7,5), (8,5), (5,7)}`, 15 families, `u ∈ {½, 1, 2}`, `b ∈ {0.6, 1, 2}`, `L ≤ 3`, constants of the theorems, `δ′ = δ/(4LM̄)` | 475 runs, `3.64·10^7` real inner brackets (771 of 965 rungs by a real two-sample bracket): **every final bracket valid and within `x_out`**, no abort, no inner bracket invalid, all claims of Theorem K1 hold; evaluations `≤ 0.6 %` of `C_max` |
| `r8_three.py 40 6 510` (534 s) → `out/three_levels.txt` | **three nested levels**: outer 2L⁺ on `Q_{n_o}×Q_{n_i}`, middle 2L⁺ on each fibre `Q_{n_i} = Q_{n_o′}×Q_{n_i′}` (Corollary-K1.b style or Theorem-K2 style parameters so that its certified accuracy is at most the rung's), bottom K0; `(n_o, n_o′, n_i′) ∈ {(3,3,3), (3,3,4), (4,3,3), (3,4,3)}`, `u ∈ {½, 1}`; all constants from the theorems, the middle failure probability is the outer `δ′`.  For run time the outer points draw their bracket from a pool of 40 independent middle runs per (fibre, rung) | 16 outer runs, 9 920 middle runs, `2.3·10^8` bottom brackets (all 25 bottom rungs by real two-sample brackets): **no invalid or too wide bracket at any level, no claim of Theorem K1 violated at the middle or outer level, no abort**; evaluations `≤ 1.1·10^{-5}·C_max` (with `C_l = C_max` of the middle algorithm) |

Limits: the cubes are tiny (`n ≤ 13`); these runs test the logic of the nesting and of the interface "bracket procedure", not
costs.  The pool makes the inner randomness of different outer points dependent.

### 4.4 The flat instance: exact cost against the hinted lower bound (`r8_flat.py`, `r8_flat3.py`)

At `ψ ≡ 0` every fibre average is `1` and the two-sample bracket of a flat fibre is deterministic, so the whole run — with
*real* inner brackets — is deterministic and its number of evaluations can be computed exactly.  `r8_flat.py cross` (< 1 s):
the closed-form run agrees with the pass-by-pass implementation with real brackets in 6 of 6 parameter sets (stop level, last
`M`, closing radius, numbers of populated/negligible levels, number of evaluations, width).

`r8_flat.py table 1.0` (42 s) → `out/flat_u1.txt`, `r8_flat.py table 2.0,0.5` (112 s) → `out/flat_u2_u05.txt`: parameters of the
report's §6.4 (`b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `δ = 0.05`, 40 rungs, `ν₁ = 2e^un_o/θ`), nine values of `φ`.
Entries `ln(cost)/(na)`, best `φ`:

| `n` | `u = 1`: two levels | hinted lower bound | `C_max` | `u = 2`: two levels / bound | `u = ½`: two levels / bound |
|---|---|---|---|---|---|
| 250 | 1.574 | 0.332 | 2.90 | 0.826 / 0.334 | 4.06 / 0.436 |
| 1 000 | 0.712 | 0.286 | 1.49 | 0.592 / 0.306 | 1.35 / 0.324 |
| 4 000 | 0.552 | 0.271 | 0.89 | 0.542 / 0.300 | 0.666 / 0.275 |
| 16 000 | 0.513 | 0.265 | 0.64 | 0.523 / 0.298 | 0.530 / 0.261 |
| 64 000 | 0.514 | 0.263 | 0.59 | 0.518 / 0.297 | 0.500 / 0.255 |

In all 135 runs: bracket valid, width `≤ x_out`, **cost `≥` hinted lower bound, cost `≤ C_max`**.  The lower-bound column
agrees with the report's (0.332, 0.286, 0.271, 0.265, 0.263); the report's cost column (1.698, 0.701, 0.548, 0.522, 0.512)
is for a modelled inner behaviour, mine for the real brackets — the same within the differences of the models and grids.

`r8_flat3.py 1.0 1000 0.3,0.5,0.7,0.8` (4 s), `r8_flat3.py 1.0 4000 0.3,0.4,0.5,0.65` (13 s),
`r8_flat3.py 1.0 16000 0.25,0.35,0.45,0.55` (65 s) → `out/flat3_a.txt`; `r8_flat3.py 1.0 64000 0.2,0.28,0.36` (262 s) →
`out/flat3_b.txt`: **three levels at the flat instance** — the inner family of the outer algorithm is, rung by rung, the cheaper
of Proposition K0 and Algorithm 2L⁺ (itself with K0 inside; again deterministic, hence exact; the middle algorithm has
Corollary-K1.b style parameters for rungs of accuracy `≥ 8` and Theorem-K2 style parameters below, see the header of the script).

| `n` (`u = 1`) | two levels (best `φ`) | three levels (best `φ₁` tried) | hinted lower bound |
|---|---|---|---|
| 1 000 | 0.712 | 0.712 (no gain) | 0.286 |
| 4 000 | 0.552 | 0.460 | 0.271 |
| 16 000 | 0.513 | 0.405 | 0.265 |
| 64 000 | 0.514 | **0.379** | 0.263 |
| limit | `τ₂/a = 0.5004` | `τ₃/a = 0.361` | `h/a = 0.2626` |

All 15 three-level runs: valid, within the width bound, above the hinted lower bound, and below the `C_max` formula evaluated
with the middle algorithm's *actual* cost at a flat fibre as `C_l` (a smaller number than the `C_max` of Theorem K1).  This is the first
numerical evidence at large `n` that one more level lowers the cost at a bounded accuracy as Theorem K2 says; it is evidence at
one instance (the instance on which the lower bound is proved), not a test of the worst case over the class.

### 4.5 The recursion, K5(b), the lower bound

* `r8_recursion.py 0.5 1.0 2.0` (53 s) → `out/recursion.txt`: own discretisation (180 grid points, exact `sup_γ` for the
  interpolant, grid search with one refinement; modes `linear` and `step` = upper bounds).  `τ₂` from the closed form:
  `0.50003a, 0.50041a, 0.50562a` (`u = ½, 1, 2`).  `τ_k/a`, `k = 2..8`, linear mode: `u = 1`: 0.5005, 0.3613, 0.3108, 0.2898,
  0.2802, 0.2753, 0.2723 (report: 0.5006, 0.3613, 0.3108, 0.2898, 0.2803, …, 0.2723 at `k = 8`); `u = ½`: 0.5001, 0.3568, 0.3037,
  0.2813, 0.2710; `u = 2`: 0.5057, 0.3814, 0.3394, 0.3225, 0.3145.  Step mode (upper bounds): `u = 1`: 0.5015, 0.3639, 0.3156,
  0.2951, 0.2859.  Nonincreasing in `k` and `g`; `T_k ≥ θ_hint` on the grid and `τ_k ≥ h` at every level.  (My grid search at
  `g > 0` is coarser than at `g = 0`, so `τ_k − T_k(g_min)` comes out between `−3·10^{-4}a` and `+9·10^{-4}a`; the negative values
  are search error, not a violation of `T_k ≤ τ_k`.)  Not recomputed: `k > 8`.
* `r8_k5b.py` (47 s) → `out/k5b.txt`: with the smallest admissible `T = θ_hint`, `T(0) = h`, and `u ∈ {0.1, 0.3, 0.5, 1, 2, 4, 8}`:
  minimum over `(φ, ξ)` of the two-rung bound, minimum over `φ` of `R_φ[θ_hint](0)`, minimum of (3.1) over 60 000 random ladders:
  all `≥ h`; the smallest excess is `2·10^{-10}h`, at `φ ≈ 10^{-9}`.  Proposition K5(b) stands.
* `r8_lowerbound.py` (1 s) → `out/lowerbound.txt`: `k*(ε)` from exact integers (`e^u = 2`, `n ≤ 3000`) agrees with the floating
  tables in 25 of 25 cases; `n^{-1}ln[(1−2δ)2ⁿ/|B(n,k*)|]/h` for `n = 10³ … 10⁶`, `u = 1`: fixed `ε = 0.01, 1, 30`: `→ 1.0003,
  1.0002, 0.9997`; `ε_n = n^{-3}`: 1.0009; `e^{−√n}`: 1.017; `e^{−n^{0.8}}`: 2.36 and falling (8.6, 5.4, 3.4, 2.4): slow, as
  `ln(1/ε_n)/n → 0` slowly; `ε_n = √n`: 0.984; `n/ln²n`: 0.914 and rising; outside the theorem, `ε_n = e^{−0.02n}`: `→ 1.366 ≠ 1`.

### 4.6 Accuracies that tend to zero (the uniform statements (E0′))

`r8_uniform.py` (148 s) → `out/uniform.txt`.  (a) Proposition K0, `u = 1`, `δ′ = e^{−d}`: `ln(cost)/(da)` for
`d = 10³, 10⁴, 10⁵, 10⁶`: at `x = 1`: 1.386, 1.093, 1.026, 1.008; at `x = 0.01`: 1.702, 1.169, 1.047, 1.014; at `x_d = d^{−2}`:
2.19, 1.31, 1.095, 1.031; at `x_d = e^{−√d}`: 2.94, 1.83, 1.40 (`d ≤ 10⁵`) — towards 1, the more slowly the faster `x_d → 0`,
as (E0′) says.  (b) Theorem K2 with a small target accuracy `x` (`b = x/2`, `λ = η = η′ = θ = x/12`, `ν₁ = 2e^un_o/θ`, 40 rungs,
K0 inside) at `ψ ≡ 0`, exact number of evaluations: `n = 16 000`, `φ = 0.55`: `ln(cost)/(na) = 0.513` (`x_out = 0.87`), `0.533`
(`x = 0.2`), `0.547` (`x = 0.05`; `K = 5.4·10⁶`, `9·10⁶` levels); `n = 4000`, `φ = 0.65`: `0.552, 0.558, 0.590`.  In all ten runs
the bracket is valid, its width at most `x`, the cost above the hinted lower bound for `ε = x` and below `C_max`.  Not done:
a sequence `x_n → 0` along `n → ∞`, and anything but the flat instance.

## 5. The Lean files (item 11 of the brief)

`cd /home/user/MetricChain && export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH" && lake env lean <absolute path>`, one file
at a time, after another process's `lake build` had finished (`out/lean_*.txt`): `KBounded.lean` (12 s), `KBoundedLink.lean` (11 s), `KBoundedCube.lean` (11 s), `KExactRecursion.lean`
(6 s) — all exit 0, no `sorry`; every printed theorem depends on `[propext, Classical.choice, Quot.sound]` only.  My scratch
file `R8Axioms.lean` (5 s): the same three axioms for the repository's `cube_exact_dip_randomized` (= (LB)) and
`cube_iterates_lt_hint_add`, `cube_hint_superSolution`.

* **`exactRec` is the recursion of (11.18.2).**  `admissible θna T g` is the set of `B` for which some `0 < β < g`, `0 < φ < 1`
  has `min(γ, φθ_na((g−β)/φ)) + (1−φ)T(γ/(1−φ)) ≤ B` for all `γ ≥ β`; `Rstep = sInf admissible`; `exactRec θna 0 = θna`,
  `exactRec θna (k+1) g = min(exactRec θna k g, Rstep θna (exactRec θna k) g)` — index shifted by one against the paper, domains
  of `φ, β, γ` as in the paper.  *Junk values:* for `g > 0` the set is nonempty (proved inside `Rstep_anti`, from `T ≤ C`) and
  bounded below by `0` (`admissible_nonneg`), so `sInf` is the true infimum of the suprema — a pair `(φ, β)` with infinite
  supremum simply contributes nothing; for `g ≤ 0` the set is empty and `Rstep = 0` (junk), but no statement evaluates `T` or
  `θ_na` at a nonpositive argument (`γ/(1−φ) > 0`, `(g−β)/φ > 0`), and `cubeNa` is the paper's `θ_na` on `[0, ∞)`
  (`cubeNa_isLeast_allRadii`).
* **`exactRec_reaches_hint` is statement (R)**: `0 < u`, `0 < g < cubeEstar u`, `0 < η ⊢ ∃ k, exactRec (cubeNa u) k g <
  cubeHint u g + η`.  No hypothesis about the sequence; nothing hidden.  This is exactly what Proposition E(b) uses.
* **`two_rung_bound` is the iteration of Theorem K3** (with the fixed number `Tξ := h + η`, which suffices because
  `T_m(ξ) ≤ h + η` for all `m`).  `bounded_iterates_lt`, `levels_reach_hint_at_zero`, `cube_levels_reach_hint_at_zero` are
  **not** the iteration of Theorem K3; they are Proposition K5(c) for abstract sequences (hypotheses `hTτ: T_k ≤ τ_k` and
  `hstep0`, which encodes `τ_{k+1} ≤ inf_φ max((1−φ)τ_k, sup_{0<γ≤φa}[γ + (1−φ)T_k(γ/(1−φ))])`).  That the sequences of
  Proposition K5 satisfy `hTτ`, `hstep0` is on paper (correct: `R[T](g) ≤ R_φ[T](0)` for every `φ` because `φθ_na(·) ≤ φa` and
  `{γ ≥ β} ⊂ {γ ≥ 0}`; for `γ > φa` the bracket is at most its value at `γ = φa`).
* `certified_lower_sum_le_mean` is (2.2) with the index shift `t(i+1) = s_ie^{−b}`, `t(0) = s₀e^{−λ−b}` and strict exceedance, as in
  the paper; `populated_part_le`, `close_points_bound'`, `width_le` are the algebra of Steps 4 and 7.
* The proof of `bounded_iterates_lt` is repeated verbatim in three files (cosmetic).
* **Paper statements without a Lean counterpart:** Lemma K.1 and Harper's theorem; Lemma K.2 (the repository has
  `fibre_sum_le`); the algorithm, the good event and its probability; Steps 1, 2, 5, 6, 8, 9 of Theorem K1 (in particular the
  Harper term, the closing radius, the sample sizes, termination) and the summation of the cost; Lemma K.4; Proposition K0;
  Corollary K1.b; Proposition E; Theorem K2; Theorem K3 except its iteration; Corollary K3′; Proposition K5(a), (b), and the
  two paper steps of (c); the definitions of §1.3.  On the lower-bound side the closed forms of the two finite sums in
  `cube_exact_dip_randomized` and the asymptotics of Theorem 11.25(d).

## 6. The lower bound (item 9), independently

`cube_exact_dip_randomized` (statement read; axioms printed): for a finite mixture of deterministic adaptive query algorithms
(a class slightly larger than decision trees) that is `(ε/2, δ)`-correct for `ln Z` on all `c`-Lipschitz residuals, with
`u = βc`: if `ε < Δ_k` then the expected number of *distinct* evaluations at the zero function is at least
`(1−2δ)2ⁿ/|B(k)|` (with `r = c(k+1)`: the open ball is `B(k)`, the hypothesis is `ε < Δ_k`).  This is the statement (LB) of the
report, with the same accuracy convention as the upper bound and for every `δ < ½`; an algorithm without a hint is one with a
hint; expected cost at one instance bounds both the worst-case and the worst-case expected cost from below.
Exponent: `2^{−n}E_k(n) = e^{u(k+1) − nΛ₁}(1 − o(1))` for `k/n > p_u`, so `k*(ε_n)/n → Λ₁/u` as soon as `ln(e^{ε_n} − 1) = o(n)`,
i.e. `ε_n = o(n)` and `ln(1/ε_n) = o(n)`: the exponent is `h` in the regimes (i) fixed `ε`, (ii) `ε_n → 0` with
`ln(1/ε_n) = o(n)`, (iii) `ε_n → ∞`, `ε_n = o(n)` — as Theorem 11.25(d), third row, says.  Numerics in §4.5.

## 7. Prior art (item 15)

Web searches on 25 Nov 2026, generic queries only (no project or personal information); **search summaries and one abstract
page only, no full text**.  Queries: the binomial median (Kaas–Buhrman); Dagum–Karp–Luby–Ross; adaptive query complexity of
partition functions of Lipschitz functions on the cube with Harper; nested sampling / multilevel splitting with certified
relative error from bracketed samples; Mathé–Novak; mean estimation from samples known up to a refinable multiplicative
bracket; adaption in information-based complexity; isoperimetric lower bound for the mass below a level set; multilevel
nested simulation with adaptive inner sampling; layer-cake Monte Carlo with an isoperimetric tail bound; extremal Lipschitz
functions on the cube.

* *Related, already known to the project:* Dagum–Karp–Luby–Ross (2000; relative-error stopping rule for exactly observed
  `[0,1]` samples; according to a search summary a later preprint, arXiv 0711.2801, states that the proof of its stopping-rule
  theorem is incomplete — not verified by me); Mathé–Novak (2007); nested sampling and multilevel splitting (asymptotic or
  heuristic error analysis).
* *Related, not in the report's list:* (1) **Giles–Haji-Ali, "Multilevel nested simulation for efficient risk estimation"
  (2019), and Haji-Ali et al., "Adaptive multilevel Monte Carlo for probabilities"**, following Broadie–Du–Moallemi: the
  number of inner samples of an outer sample is chosen adaptively from its distance to a threshold — the idea "refine a sample
  only as far as its distance to the level requires", for `E[H(E[X|Y])]`, with mean-square complexity, not certified brackets
  or worst-case exponents.  (2) **Extremal Lipschitz functions via isoperimetry** (Dzindzalieta, "Extremal Lipschitz functions
  in the deviation inequalities from the mean", arXiv 1205.6300, abstract read; Bobkov–Houdré–Tetali 2006): for the cube with
  the Hamming distance the extremal Lipschitz functions of deviation problems are distance functions to Harper's extremal
  sets — the mechanism of the tail lemmas 11.43(b),(c) (which the report labels [known] anyway).  (3) Sequential mean
  estimation from threshold (1-bit) queries (Lau–Scarlett and others): adaptive thresholds, a different model.
* *Not found at this depth:* a certified bounded-ratio estimator of a mean from bracketed samples with a ladder of levels; the
  use of a *lower* isoperimetric bound (mass below a level set of given size) to close such a ladder at constant relative
  accuracy; the exponent `h` at bounded accuracy for adaptive algorithms on a Lipschitz class of the cube.  "Not found", not "new".

## 8. What I did not check

* The Lean proofs line by line (statements, structure, compilation and axioms only), and the repository's proofs of
  Theorem 11.25(a) and 11.53 beyond that; the closed forms of the two sums in the lower bound beyond numerics (§4.5).
* Harper's theorem and the Kaas–Buhrman theorem in the original papers (secondary sources and computation only); the Chernoff
  and Hoeffding bounds (standard forms, not re-proved).
* The author's code and logs: not run, not audited.  The report's §6.6 (outer loop in expectation, `n_o ≤ 16 000`, additive
  landscapes) was not reproduced; my largest simulated outer cubes are `n_o = 520` (radial) and `n_o = 9` (non-radial).
* Three nested levels with real brackets only on `Q_9, Q_10` and, at large `n`, only at the flat instance; no run with four
  levels; no three-level run on a non-flat instance at large size.  Corollary K3′(ii) (accuracies tending to zero) and the
  uniform versions (E0′) were checked on paper and, numerically, only for the cost of the base bracket and at the flat
  instance (§4.6); the smallest constants in a simulation with random samples are `0.025`.
* `τ_k` for `k > 8`, the "rigorous one-sided" value `τ_40 ≤ 1.027h`, and the statement on populated levels in §5(2) ([sketch]).
* The frequency of failure of the good event from below (it never failed with the constants of the theorem).
* Floating point: my simulations use exact rationals for `q`, `p̲` and radii but floating-point logarithms for levels and
  tails; comparisons have tolerance `10^{-9}`.  The flat-instance computations for large `n` are entirely in floating point
  (cross-checked against exact integers at small `n`).
* Prior art beyond search summaries.  The files added to the repository's working tree during the review
  (`proofs/Frontiers/BoundedAccuracy.lean`, `docs/workstreams/K_REPORT.md`, the modified theory report).

## Appendix. Theorem K1 in my own order (what uses what)

Notation: at the pass that ends level `j`: `(M_j, N_j, q_j, p̲_j)`; `ℓ_j` the value of `ℓ` when level `j` is entered;
`c = c_η = (1−η)/(1+η)`.

*Facts that use no probability* (they hold for any sequence of points and any inner answers, valid or not):
(D1) at a populated pass `q ≤ p̲/c`, and after step (b) `ℓ ≥ s_je^{−b}p̲` and `ℓ ≥ s_je^{−b}2^{−n_o}T_{n_o}(k)`, `k ≥ κ(r)` if `q < 1`;
(D2) at a negligible exit `s_jq_j ≤ e^bℓ_j/((1−η)ν₀)`;
(D3) a failed test has `2^{n_o}q ≥ 1`; if `r ≤ n_o − 1`, `tail ≤ s_jqΓ̃(r)` (minimality of `r`; `r = 0` forces `2^{n_o}q = 1`), so by
(D1) `tail ≤ min(Γ̃(r)/c, Γ″(r))·e^bℓ` at a populated pass and by (D2) `tail ≤ Γ̃(r)e^bℓ/((1−η)ν₀)` at a negligible exit: [P] resp.
[N] fails at `r`, hence `r > r†` and `q_j > π†` — claim (iii);
(D4) `M_0^neg < ν ≤ ν₀M†`; negligible predecessor: `M_j^neg ≤ e^λM_{j−1}^neg ≤ e^λM_{j−1} < e^λM†`; populated predecessor:
`ℓ_j ≥ c·s_{j−1}e^{−b}q_{j−1} > c·s_{j−1}e^{−b}π†`, so `M_j^neg < e^λν/(cπ†) = (1+η)e^λν₀M†`; doubling stops at `2M_j^neg` — claim (iv), and
the number of points is at most `M̄` always;
(D5) the width, term by term, whenever the run stops through the test.

*Facts on the good event.*  (V1): `X_{s_j}(M) ≤ N ≤ X_{s_je^{−b}}(M)` and classification ends at rung `L`.  (V2): `p(s_j) ≤ q` at every
pass.  (V3) at `s_je^{−b}`: `p̲ ≤ p(s_je^{−b})` at every populated pass; then `ℓ ≤ A` (Markov, and Lemma K.1(b) with
`|{W ≥ t}| ≥ max(1, 2^{n_o}p̲) ≥ |B(n_o,k)|`), the lower end (disjoint intervals `(s_{i−1}e^{−b}, s_ie^{−b}]`), the upper end (layer cake and
Lemma K.1(a) with `r ≤ n_o − 1`, or an empty super-level set).  The count: for `s_i ≤ s_je^{−x} < s_{i+1}`,
`M_j^neg p(s_je^{−x}) ≤ (νs_j/(ℓ_je^b))·q_i ≤ νs_j/(c·s_i) < c^{−1}e^{λ+x}ν` by (D1)/(D2) for level `i` — the same `ℓ_j e^b` in numerator and
denominator; with (V3) at `s_je^{−x_l}` and the last size, at most `cnt(x_l)` points; a call of `I_l` at level `j` needs
`W > s_je^{−x_{l−1}}`.  Termination: `ℓ ≤ A < s₀e^{2un}` gives `M_J^neg > K2^{n_o}/(1−η)`, nothing is high at level `J`, and the
first pass with `M ≥ M_J^neg` has an empty tail.

I found nothing to add or to correct in these steps.

## 9. Files (all in `scratchpad/referee8/`)

`r8_core.py` (tables, constants, Algorithm 2L⁺, checks) · `r8_pops.py` (instances, populations, tail-safe sampler) ·
`r8_sim.py` · `r8_e2e.py` · `r8_three.py` · `r8_flat.py`, `r8_flat3.py`, `r8_uniform.py` · `r8_recursion.py` · `r8_k5b.py` · `r8_lowerbound.py` ·
`r8_k4_exact.py` · `r8_median.py` · `r8_tail.py` · `r8_gamma.py` · `r8_sampler_test.py`, `r8_numpy_tail.py` · `R8Axioms.lean` ·
outputs in `out/`.
