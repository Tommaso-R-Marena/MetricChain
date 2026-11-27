# Workstream K — adaptive algorithms without a hint at a BOUNDED accuracy

You are an independent research workstream of a mathematics project.  You have real
intellectual freedom: prove, refute, or replace the conjecture below.  A refutation or a
precise obstruction is as valuable as a proof.  Do not soften negative findings.

## Setting (all in the repository `/home/user/MetricChain`, read-only for you, commit 1bff191)

* `docs/THEORY_REPORT.md` §11.16 (search "### 11.16") and §11.18 (search "### 11.18"): class `L_u` of
  `u`-Lipschitz `ψ` on the Hamming cube `Q_n`; target `ln A`, `A = 2^{-n} Σ_x e^{-ψ(x)}`; an algorithm is
  correct at accuracy `ε` if `|output − ln A| ≤ ε/2` with probability `≥ 1 − δ` on every member of the
  class; cost = number of evaluations, worst case over the class.  Notation: `p_u = 1/(1+e^u)`,
  `Λ₁ = ln(2/(1+e^{-u}))`, `ε* = ln cosh(u/2)`, `a = KL(p_u‖½)`, `h = KL(Λ₁/u‖½)`,
  `θ_na(ε₁) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}`, `θ_hint(ε₁) = KL((Λ₁+ε₁)/u‖½)`; tail lemma 11.43; two-sample
  bracket (Proposition 11.46); Theorem 11.25(a) (lower bound with a hint).
* Known at EXTENSIVE accuracy `ε = ε₁n`: non-adaptive exponent `θ_na(ε₁)`; adaptive exponent
  `θ_hint(ε₁)` (Theorem 11.54: two-level "layer-cake" algorithm of Theorem 11.52, recursion
  `T ↦ R[T]`, convergence Theorem 11.53; Lean: `proofs/Frontiers/HintRecursion.lean`).  The paper
  proof of Theorem 11.52 is under independent review; treat it as probably right.
* Known at BOUNDED accuracy `ε = O(1)`: the non-adaptive exponent is `a` (Theorem 11.44); with a
  hint the lower bound has exponent `h` for every fixed `ε` (Theorem 11.25(a)).
* `docs/DEAD_ENDS.md` D45: five wrong cost accountings preceded the proof of Theorem 11.52.
  Read it before you count anything.
* Executable readings: `experiments/falsify_conjectures.py` — `lv_two_level`, `lv_check_run` (outer
  loop of the two-level algorithm with a simulated inner oracle), `LvRecursion` (the
  recursion), `na_theta_na`, `na_theta_hint`; `experiments/separation_benchmarks.py` — `LevelCube`,
  `two_level_flat_cost`.

## The question

**What is the exponent of adaptive randomised algorithms without a hint at a fixed accuracy
`ε` (independent of `n`)?**  It lies in `[h, a]`.

Conjecture K (coordinator; unproved): for every `η > 0` there is `ε(η, u) < ∞` such that adaptive
algorithms without a hint reach accuracy `ε(η, u)` with `exp(n(h + η) + o(n))` evaluations; i.e. the
adaptive exponent at fixed accuracy tends to `h` as the accuracy grows.  Stronger form: it
equals `h` for every fixed `ε > 0`.

## Coordinator's sketch — UNVERIFIED, written quickly, to be attacked

The two-level algorithm of Theorem 11.52 has accuracy `gn + O(log n)`, not `O(1)`, for two reasons.
(1) Its lower end is the MAXIMUM over populated levels of `s_j e^{-b} N/(2M)`, and the upper end sums
up to `J = O(n)` levels, each of which may contribute `4e^{b+1}` times that maximum.  Proposed
repair: a layer-cake SUM for the lower end, `A ≥ (1 − 1/e) Σ_{populated j} s_j e^{-b} N_j/(2M_j)` (levels
`s_j e^{-b}` form a geometric ladder and `p(s_j e^{-b}) ≥ N_j/(2M_j)` on the good event), against which
the populated part of the upper end is a constant factor.  (2) The closure test compares the
tail-lemma bound `s_j 2^{-n_o} E_r(n_o)` with `e^G ℓ`; with `G − b = O(1)` one needs
`Γ̃(r) = E_r/|B(r−1)|` to be `O(1)` at the radius `r = r(q)`, while `Γ̃(r) ≈ (e^u − 1)·n/r` for small `r` and
`Γ̃(r) = e^{n KL(ρ‖p_u)}` above `p_u n`: there is a window of radii, and the doubling of the sample size
moves `r` through all radii, so the window is entered — but does every level close inside it?
(3) The recursion at vanishing accuracy rate would be
`τ_{k+1} = min_φ max( (1−φ) τ_k ,  sup_{0<x≤φa/(1−φ)} (1−φ)(x + T_k(x)) )` with `T_k` the extensive
exponent functions and `τ_k` the bounded-accuracy exponent of level `k`; since `T_k → θ_hint` this
tends to `h` (Step I of the proof of Theorem 11.53 is this computation).  (4) Each level adds
`O(1)` to the accuracy (tolerance `b` at least the inner accuracy; `G > b`; ladder ratio `e`; factors
2 from Chernoff), so `k` levels give accuracy `≈ k·C(u)`: hence "`ε(η, u)`" in the conjecture.
(5) The base family at bounded accuracy: the two-sample bracket has ratio `≤ 3 + 12Γ(r)`, bounded
for `r ≤ p_u n + O(√n)`, cost exponent `a`.

## What to deliver

1. A precise theorem with a complete proof, or a precise obstruction/counterexample, for
   Conjecture K (weak form first).  State every constant; the accounting must be explicit
   enough to be checked line by line.  Use the necessary condition of D45: no claimed
   exponent may fall below `h`.
2. Your verdict on each step (1)–(5) of the sketch.
3. Numerical checks with your own code (numpy/scipy; cap memory `ulimit -v 4000000`; each run
   under ten minutes): at least (i) the recursion for `τ_k` together with `T_k`; (ii) a small-size
   simulation of the modified outer loop with a simulated inner oracle, checking validity
   and an `O(1)` width; (iii) the closure window.
4. If the weak form holds: what is needed for the strong form (every fixed `ε > 0`)?
5. Anything you find about a LOWER bound above `h` at bounded accuracy for adaptive
   algorithms (none is known).

## Rules

* Do not modify anything under `/home/user/MetricChain`; no git commands that change state.
  Work in `scratch:ws/K/`.
* Lean is available if you want to check a statement:
  `cd /home/user/MetricChain && export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH" && lake env lean <absolute path>`
  (about a minute per file; do not run `lake build`).  Not required.
* Web search is allowed for prior art; say how each source was read; put no personal or
  project-identifying information into queries.
* Do not delegate to further agents.
* Label every statement: [proved] (complete proof in your report), [sketch] (missing steps
  named), [numerical], [conjecture], [known].

## Required return

Write `REPORT.md` in your directory and end with a summary of at most 40 lines: the theorem
or obstruction; verdicts on (1)–(5); what was checked numerically (commands, sizes,
outcomes); what remains open; what you did not check.
