# Internal review of `docs/workstreams/N_REPORT.md` (the nesting theorem in abstract form; instances; obstructions) — brief

*Coordinator, 2026-11-26.  The report is the unrefereed work of one independent
workstream.  It is to become a section of the theory report under the research owner's
directive on generality ("establish precisely where generalisations are possible, where
additional structure is required, and where fundamental obstructions arise"), so its
theorems and its counterexamples both have to be right.  Treat it as possibly wrong.
AI referee reports are internal reviews, not external peer review.*

## What to review, in this order of priority

1. **Theorem N1** (§2.2–2.4): the abstract level theorem.  Check the proof step by step
   (good event; Steps 1–9), in particular: that (TU) and (TL) are used with the right
   quantifiers (the certified `q` is random — is the Chernoff event enough to apply (TU) at
   it?); Step 4 (width) and Step 5 (closing level: the two conditions [N], [P]); Step 6;
   the abort rule; the claim that with the cube's conventions the constants of Theorem
   11.56 of the theory report are reproduced.  Compare with the proof it abstracts
   (`docs/workstreams/K_REPORT.md` §§2–3; theory report Theorem 11.56).
2. **The obstructions** (§5) — these are claims that something *fails*, and are as important
   as the theorems:
   * Theorem N9 and Proposition N10 (Euclidean Gauss space: exact dimension-free tail
     functions; the level operator is the identity for a fixed coordinate split; the
     lower bound on the outer sample of the algorithm).  Is the formula for `Ξ_L`, `Θ_L`
     right (derive it; check numerically)?  Is the computation of the level operator
     "without factors `φ`, `1 − φ`" right, and is the conclusion `R_G[T] ≥ max(T, Θ_na)` a statement
     about the algorithm's analysis only, or about the algorithm (part (b))?  Does part (b)
     hold as stated?
   * Proposition N11 (the hinted lower bound on Gauss space with ball-shaped dips).
   * **Proposition N12 (unbounded influence: the algorithm returns a false bracket).**
     Reproduce the instance with your own code from the description alone (`m = 12`, `k = 16`,
     `u = 1`, `J = 4`, `τ = 10.5`): the value of `A`, the edge ratios of `V`, the violation of (TU),
     and — with your own implementation of the outer loop or a careful reading of the
     workstream's — that the returned upper end is below `A`.  Is this a failure of the
     theorem's hypothesis (as claimed) and not of the implementation?
   * Proposition N13 (exponential moment necessary and sufficient).
3. **Theorem N4** (§2.7, dependence under a class-relative bounded influence `ι`): the
   definition of `ι`, the proof that fibre averages are in the class with envelope `d_o + ι`,
   the claim that it is attained, the requirement on inner procedures.
4. **Theorem N1′, Theorem N3, Proposition N2, Corollary N5, Proposition N6** (§§2.5–2.8) and
   **Proposition N7, N8** (§3): statements and proofs; the report itself names the assembly
   over the levels (Proposition N6) as its weakest link — say whether it is a proof.
5. **§4 (instances)**: spot-check two — the sum-metric Gauss space (exact tail functions for
   every `n`) and the nearest-neighbour chain (one-sided slack at the boundary site).
6. **§6 (the assumption table)**: for each of the 25 rows, is the category supported by the
   evidence cited?  List rows you would classify differently.
7. Literature quoted "from memory" (Gaussian isoperimetry; the spherical cap bound;
   McDiarmid): are the statements used correct as stated?  (Standard knowledge is enough;
   no web access is needed.)

## Rules

* **Write early, write often.**  Create your review file with a skeleton in your first few
  tool calls and append findings as you go.  Never spend a whole answer thinking without a
  tool call (an earlier agent of this project produced nothing because its answers were
  cut off at the output limit).
* Do not edit any existing file.  Create only `docs/workstreams/N_REVIEW.md` and scripts with
  outputs under `experiments/workstreams/N/review/`.  Do not run `lake`, `scripts/audit_all.sh`,
  or state-changing git commands.  Keep memory small and single runs under five minutes.
* The workstream's code (`experiments/workstreams/N/nlib.py`, `n1`–`n5`) may be read and run,
  but anything you assert must rest on your own derivation or your own code.
* Verdict per statement: **correct as stated** / **correct after a repair (give it)** /
  **gap (what is missing)** / **wrong (counterexample)**.  Separate substance from wording.
* Final answer (hand-back): at most 60 lines — verdicts, errors found (most serious first),
  what you verified numerically (scripts, key numbers), what you did not check.
