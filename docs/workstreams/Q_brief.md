# Workstream Q — the sub-exponential term of the adaptive exponent without a hint

*Brief written by the coordinator at the twenty-first checkpoint of cycle 10 (2026-11-26).
A paper-proof workstream with numerical checks; no Lean is required.*

## 1. The setting, in one paragraph

`L_u(Q_n)` is the class of functions `ψ` on the cube `{0,1}^n` that are `u`-Lipschitz for the
Hamming distance; an algorithm evaluates `ψ` at points it chooses adaptively and must
return `ln Z`, `Z = 2^{-n}Σ_x e^{−ψ(x)}`, within `±ε/2` with probability at least `1 − δ`; its cost is
the number of evaluations.  With `p_u = 1/(1+e^u)`, `a = KL(p_u‖½)`, `Λ₁ = ln(2/(1+e^{−u}))` and
`h = KL(Λ₁/u‖½)`: every algorithm needs `e^{nh − o(n)}` evaluations (Theorem 11.25(a) of
`docs/THEORY_REPORT.md`, the "hinted" lower bound, which holds even if the algorithm is
told the instance), non-adaptive algorithms need `e^{na − o(n)}` at bounded accuracy, and
**adaptive algorithms without a hint reach `e^{nh + o(n)}` at every bounded accuracy**
(Theorems 11.54 and 11.58) by nesting `k` levels of one two-level construction and
letting `k → ∞`.

## 2. What is known about the `o(n)`

Nothing explicit.  The theory report (§11.19, remark (2)) says: "Without a hint the upper
bound is `e^{nh + o(n)}` with an unquantified `o(n)` (heuristically not better than `n^{3/4}`:
each bounded level loses `e^{O(√n)}`, and `η → 0` needs `≈ 1/η` levels …)".  Since then:

* the level recursion has a proved, machine-checked rate: `τ_k − h ≤ c₁/(k + c₂)`,
  `c₁ = h(1+κ)/κ`, `κ = h²a/((a−h)(a+h)(2a−h))`, `c₂ = (a+h)(2a−h)/(ha) − 2` (remark after Theorem
  11.53; `proofs/Frontiers/RateFull.lean`), and at every accuracy rate `g`:
  `T_k(g) − θ_hint(g) ≤ A(g)/(k + c₂)`; numerically the recursion of the cube converges like
  `0.65a/k²`;
* the one-level tool, Theorem 11.56 ("Algorithm 2L⁺"), has every constant explicit: for
  inner bracket procedures with cost bounds `C_l` at accuracies `x₀ > x₁ > … > x_L`,

      C_max = 1 + 2M̄ + Σ_{l=1}^{L} min{ 2M̄ , (J+1)·cnt(x_{l−1}) }·C_l ,

  with `M̄`, `J`, `cnt`, `K`, `ν₀`, `r†`, `π†`, `δ′ = δ/(4LM̄)` as in the theorem (complete text and
  constants: `docs/workstreams/K_REPORT.md` §2.2, §2.4; the lemma that locates `r†`:
  Lemma 11.55);
* nesting is monotone when every rung is served by the procedure with the smallest
  *certified* cost (§11.19, remark (1b)): the certified bound of `k + 1` levels is at most
  that of `k` levels, and the recursion of certified bounds at finite `n` is well defined;
* exact evaluations of the certified bound exist for two and three levels at
  `n = 10³ … 6.4·10⁴`, `u = 1` (`experiments/coordinator_checks/three_levels_certified/`,
  `out_summary.txt`): in units of `na` (`a = 0.110944`), two levels `1.1384, 0.9933, 0.8721, 0.7262,
  0.6415, 0.5899, 0.5646, 0.5407` at `n = 1000, 1400, 2000, 4000, 8000, 16000, 32000, 64000` against
  the limit `τ₂/a = 0.5004`; three levels `0.6106, 0.5262, 0.4782, 0.4439` at `n = 4000 … 32000`
  against `τ₃/a = 0.361`.  The excess over the limit, in nats, is about `1.2·√n` for two levels
  and `1.6·√n` for three.

## 3. The goal

**Prove an explicit sub-exponential term**: a statement of the form

    for every u > 0 and every bounded accuracy ε and failure probability δ there is C such that
    for all n the least cost of an adaptive algorithm without a hint is at most
    exp( n·h + C·n^{3/4}·(ln n)^{β} )

(with the best exponent of `n` and of `ln n` that the method gives), **with a complete
paper proof**, or else the precise step at which such a proof fails, with a
counter-computation.  The natural route:

1. *A finite-`n` form of one level.*  From Theorem 11.56 and Lemma 11.55 derive, for a level
   with outer fraction `φ` in dimension `d`, tolerance `b`, a ladder of `L` rungs and inner cost
   bounds `C_l`, an inequality

       ln C_max ≤ max{ φ·a·d , max_l [ min(φ·a·d, x_{l−1}) + ln C_l ] } + (an explicit error),

   and say exactly how the error depends on `d`, `L`, `δ`, `λ`, `η`, `η′`, `θ`, `ν₁` — in particular the
   `O(√d)` of `M̄` (how large is the constant?), the polynomial factors `K`, `ν₀`, `J`, `L`, and the
   failure probability `δ′ = δ/(4LM̄)` that is handed down (it becomes exponentially small:
   what does that cost the levels below?).  Do the same for the level at an *extensive*
   accuracy `x = g·d` (Theorem 11.52, and the paragraph before Proposition 11.57: Theorem
   11.56 with `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, `θ = e^{x−b} − (3e+1) − (2p_u)^d e^{−b}`), where the outer
   exponent is not `φa` but a function of the accuracy rate (Theorem 11.52, (11.18.1)).
2. *The base family.*  Proposition 11.57(a) / Lemma 11.55: the two-sample bracket costs
   `exp(d·θ_na(x/d) + O(√d))` — make the error explicit, uniformly in the accuracy and in a
   failure probability `e^{−O(d)}`.
3. *Induction over levels.*  With `b_k(d, x, δ)` the logarithm of the certified cost of `k`
   levels, prove `b_k(d, x, δ) ≤ d·T_k(x/d) + E_k(d, δ)` with `T_k` the exponent functions of the
   level recursion (as in Theorem 11.53 / `exactRec` of `proofs/Frontiers/BoundedAccuracy.lean`;
   at accuracy zero `τ_k`), and an explicit `E_k`: the discretisation of the ladder (a ladder
   of ratio `ρ` loses about `(ρ − 1)·x` at the rung that matters — how many rungs are needed?),
   the per-level `√d` terms, the logarithmic terms, and how they add up over `k` levels in
   shrinking dimensions.  Is `E_k = O(k·√(d·ln d))`?  Is anything not uniform in `k`?
4. *Optimise `k`.*  With the proved rate `c₁/(k + c₂)` this should give `n^{3/4}` up to
   logarithms; with the numerically observed `1/k²` it would give `n^{2/3}` — say which is
   proved and which is conditional.

If the uniformity in `k` fails somewhere (the report's remark (2) of §11.19 suspects the
sub-exponential factors of a family with `k` nested levels), find out where exactly, and
whether a different schedule (accuracies, failure probabilities, ladders) repairs it.

## 4. Sources to read first (all in this repository)

* `docs/THEORY_REPORT.md`: §11.18 (from the heading "### 11.18", about line 4500: Theorems
  11.52, 11.53 and its remark on the rate, 11.54) and §11.19 (from "### 11.19": Lemma 11.55,
  Theorem 11.56 and its remark on the lowered cap, Proposition 11.57, Theorem 11.58,
  remarks (1), (1a), (1b), (2)).
* `docs/workstreams/K_REPORT.md` §2 (Algorithm 2L⁺ in full, all constants, the proof in nine
  steps) and its errata at the head; `docs/workstreams/H_REPORT.md` (the two-level algorithm
  at extensive accuracy, Theorem 11.52).
* `experiments/reviews/R8/r8_flat.py` (`flat_run`: an exact evaluator of `C_max` and of every
  constant of Theorem 11.56 for given parameters — use it to test your error terms),
  `experiments/coordinator_checks/three_levels_certified/` (README, `cert3.py`, `terms.py`:
  which term of `C_max` dominates at which rung; `out_summary.txt`).
* `proofs/Frontiers/HintRecursion.lean`, `BoundedAccuracy.lean`, `RateFull.lean` for the exact
  statements of the recursion and of the rate (read the statements; no Lean work is asked).

## 5. Deliverables

* `docs/workstreams/Q_REPORT.md`: (i) the theorem(s) proved, with every hypothesis and every
  constant or its explicit dependence; (ii) complete proofs, each step labelled as proved
  here, quoted from a named theorem of the report, or numerical; (iii) a table of
  numerical checks of the error terms against exact evaluations of `C_max` (two levels
  via `r8_flat.flat_run`; three levels via `cert3.py` if useful) at `n = 10³ … 6.4·10⁴`, `u = 1`;
  (iv) a section "what is not proved", naming the weakest link; (v) anything in the
  theory report that you found wrong or imprecise on the way.
* Scripts under `experiments/workstreams/Q/` (Python 3, numpy/mpmath only), with their
  outputs stored next to them, and the commands to re-run them in the report.

## 6. Rules

* Create only the files named in §5.  Do not edit any existing file.  Do not run `lake build`.
  Do not commit or push.  Do not start further agents.
* No claim without a proof or an explicit label "conjecture" / "heuristic" / "numerical".
  A clean negative result ("the method cannot give better than … because …", with the
  computation that shows it) is as welcome as a theorem.
* If a statement of the theory report that you need turns out to be weaker than you
  need, or wrong, say so and say what you used instead.
* Keep the memory footprint small (other workers share the machine): no large arrays
  beyond what `r8_flat.py` already allocates; one Python process at a time.

## 7. What to report back

The exact statement proved (or the exact obstruction), the constants or their order,
the weakest link, the numerical table in two or three lines, and the list of files
created.
