# Workstream F — algorithms without a hint when there is a KNOWN PART

You are an independent research workstream of a mathematics project.  You have real
intellectual freedom: the goal below is a direction, not a prescription.  Prove what is
true, refute what is false, and say plainly what you could not decide.

## Setting (repository `/home/user/MetricChain`, read-only for you, commit 1bff191)

The project studies an energy `E = f + g` on a configuration space, `f` known, the residual `g`
only known to lie in a class.  Read in `docs/THEORY_REPORT.md`: §11.10 Theorems 11.25, 11.27,
11.28 (hinted bounds on the cube and at additive instances; the "game formula"); §11.16
(algorithms WITHOUT a hint, non-adaptive: tail lemmas 11.43, Monte Carlo 11.44, lower bound
11.45, two-sample bracket 11.46); §11.18 (adaptive algorithms without a hint reach the hinted
exponent: two-level layer-cake algorithm 11.52, recursion and its convergence 11.53, the
identity `θ_na(e + θ_hint(e)) = θ_hint(e)`, Theorem 11.54); `docs/DEAD_ENDS.md` D45 (five wrong cost
accountings — read before counting anything); `docs/workstreams/H_REPORT.md` §2.9 (among
additive instances the flat one is the hardest with a hint; a closed form for two-state
sites).  Lean: `proofs/Frontiers/HintRecursion.lean` — the convergence theorem
`superSolution_le_hint` is ABSTRACT: it holds for any pair of exponent functions satisfying the
structure `HintPair` (identity, monotonicity, continuity).  Executable readings: functions
`na_*`, `lv_*`, `LvRecursion` in `experiments/falsify_conjectures.py`.

All of §§11.16 and 11.18 assume a ZERO known part: the reference measure is uniform on the
cube `Q_n`, the class is `{ψ : u-Lipschitz in Hamming distance}`, the target is `ln 2^{-n} Σ e^{-ψ}`.

## The question

**Generalise to a known part.**  First case: binary sites, additive known part
`f(x) = θ·|x|` (a field), i.e. the reference measure is the `p`-biased product measure
`π_f ∝ e^{-f}` on `Q_n`, the class is `{f + g : g u-Lipschitz}`, the target is `ln Σ_x e^{-f(x)-g(x)}` (or
`ln E_{π_f} e^{-g}`), algorithms know `f` and query `g`.  Then, if it works: `k`-state sites, sites of
several types, general single-site known parts.

For this setting determine, with proofs or precise conjectures:

1. the exponent of algorithms WITH a hint at the instance `g = 0` (Theorems 11.25/11.27 give it;
   restate it in a form comparable with 2 and 3);
2. the exponent of NON-ADAPTIVE algorithms without a hint (what replaces `θ_na`?  what is the
   right sampling distribution — `π_f` itself, or a tilted one?  what replaces the tail lemma:
   Harper's theorem is for the uniform measure; for product measures only asymptotic
   isoperimetry is available — Ahlswede–Gács–Körner, Ahlswede–Zhang, Bollobás–Leader for
   monotone sets — check what is actually true and usable; maybe the tail lemma can be
   proved at the exponential scale by types, without exact isoperimetry);
3. the exponent of ADAPTIVE algorithms without a hint: does the two-level construction go
   through (it needs: fibre averages Lipschitz — fine; a tail lemma on the outer block;
   additivity of the distance over blocks — fine), does the identity
   "non-adaptive accuracy = hinted accuracy + exponent of the sample" hold, and does the
   abstract convergence theorem then give "adaptive = hinted" again?
4. whether the answer to 3 is INSTANCE-OPTIMAL in the field: is the adaptive exponent without
   a hint equal to the hinted exponent of the instance `(f, g = 0)` for every `θ`, which by the
   workstream H formula is SMALLER than at `θ = 0`?

## Method

Derive, then try to break.  Before believing a formula test it numerically at finite `n` with
exact binomial/multinomial sums (your own code; numpy/scipy; `ulimit -v 4000000`; runs under
ten minutes).  For any recursion of exponents use the necessary condition of D45: no level
may fall below the hinted exponent.  If a step needs an isoperimetric statement, state it
exactly, say whether it is a theorem in the literature (and how you read the source) or a
conjecture, and whether an exponential-scale version suffices.

## Rules

* Do not modify anything under `/home/user/MetricChain`; no git commands that change state.
  Work in `scratch:ws/F/`.
* Lean is available to check a statement:
  `cd /home/user/MetricChain && export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH" && lake env lean <absolute path>`
  (do not run `lake build`).  Not required.
* Web search is allowed for prior art; say how each source was read (full text / abstract /
  search summary / memory); put no personal or project-identifying information into queries.
* Do not delegate to further agents.
* Label every statement: [proved], [sketch] (missing steps named), [numerical],
  [conjecture], [known].

## Required return

Write `REPORT.md` in your directory and end with a summary of at most 40 lines: the formulas
for the three exponents in the biased case with their status; whether "adaptive = hinted"
holds with a known part and whether it is instance-optimal in the field; the isoperimetric
input used and its status; numerical checks (commands, sizes, outcomes); negative findings;
what you did not settle.
