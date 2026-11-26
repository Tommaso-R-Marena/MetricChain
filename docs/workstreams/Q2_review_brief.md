# Internal review of `docs/workstreams/Q2_REPORT.md` (bounded levels without their `√n`; one level for maxima of lines) — brief

*Coordinator, 2026-11-26.  The report is the unrefereed work of one workstream.  It claims
that the `C₁√n` term of Theorem 11.58a of the theory report is not needed (Theorems A, B),
and it proves a one-level lemma (Lemma U) for inner families whose certified cost is a
maximum of finitely many lines — the finite-`n` counterpart of the exponent-level lemma on
which the rate of the level recursion rests (theory report, Theorems 11.53a, 11.53b).  The
coordinator intends to build a sharper bound on Lemma U and on the chain of Proposition
T, so these two are the priority.  Treat the report as possibly wrong.  AI referee
reports are internal reviews, not external peer review.*

## What to review, in this order

1. **Lemma U** (§2): the statement, the checklist of the hypotheses of Theorem 11.56 (the
   report's "(T)"), and the proof — the auxiliary inequality, the three kinds of rung,
   the bound on the outer sample through (C2), and the final display (U).  Read it against
   what it quotes (`docs/workstreams/Q_REPORT.md`: Propositions Q1, Q2, Lemma Q4; theory
   report, Theorem 11.56 and Lemma 11.55).  **A question the coordinator needs answered:**
   does Lemma U hold, with the same proof, for an inner type that is a maximum of finitely
   many lines with slopes `0 ≤ σ_i ≤ 1` *valid at all accuracies* `x ≥ x_min` — range `R = ∞`
   with positive slopes — provided the maximum is nonnegative there (for instance because
   one of the lines is flat)?  Convention (C3) of the report excludes this case ("all
   `σ_i = 0` if `R = ∞`"); say whether the exclusion is needed, and if the lemma holds, with
   which cap `Ξ`.
2. **Proposition T** (§4): the design rule for the block, the induction over a chain of
   unbounded length, the bookkeeping of `Λ` and of the failure probabilities, the term for
   the bottom of the chain; the claim that the chain costs `A_T` *once*, whatever its
   length.  The report names this its weakest link.
3. **Proposition D′** (§3) and **Proposition Q6(e)** with its corollary for maxima of lines
   (§6): statements, checklists, proofs; the remarks of §6.2 (images that leave the class
   `0 ≤ σ ≤ 1`).
4. **Theorems A and B** (§5): the schedule, the explicit sum (A.1), Proposition A′, the new
   constant `C_*′ = 3√(2(1 + r̄)c₁)`, the `O((ln n)²)` term, the claim for accuracies `ε_n`.
5. **Replication.**  With your own code (the constants of Theorem 11.56 from the theory
   report's formulas; you may read `experiments/workstreams/Q/qlib.py` and
   `experiments/reviews/R12/` but anything you assert must rest on your own
   implementation): (i) inequality (U) on a few hundred levels with saturating inner
   families, including maxima of several lines and the case `R = ∞` with positive slopes of
   item 1; (ii) a chain of Proposition T by exact recursion for two parameter sets;
   (iii) three rows of the table of §7.3 from formula (A.1).
6. The report's §9 ("what I found wrong elsewhere"): is the criticism of `Q_REPORT.md` §6.2
   right?

## Rules

* **Write early, write often.**  Create your review file with a skeleton in your first few
  tool calls; append findings as you go; never spend a whole answer thinking without a
  tool call (an earlier agent of this project produced nothing for that reason).
* Do not edit any existing file.  Create only `docs/workstreams/Q2_REVIEW.md` and scripts
  with outputs under `experiments/workstreams/Q2/review/`.  Do not run `lake`,
  `scripts/audit_all.sh` or state-changing git commands.  **Memory: all processes of this
  session share one limit — keep every process below 1 GB** (the workstream's own scripts
  once exceeded it through a cache; do not re-run `q2_02_chain.py` parts B, C or
  `q2_04_nest.py` in full) and single runs under five minutes.
* Verdict per statement: **correct as stated** / **correct after a repair (give it)** /
  **gap (what is missing)** / **wrong (counterexample)**.  Separate substance from wording.
* Final answer (hand-back): at most 60 lines — verdicts, errors found (most serious
  first), the answer to the question of item 1, what you verified numerically (scripts,
  key numbers), what you did not check.
