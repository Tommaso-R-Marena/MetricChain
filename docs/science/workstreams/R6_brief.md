# Workstream R6 — independent line-by-line review of the cost of the nested adaptive algorithm (theory report §§11.18–11.19: Theorems 11.52, 11.54, 11.56, Proposition 11.57, Theorem 11.58)

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_R6/`; your report: `docs/science/workstreams/R6_REPORT.md`.
(Second wave of workstreams.  The first wave is finished; its reports are in
`docs/science/workstreams/`.  Useful for you: `R4_REPORT.md` — a review of §11.24 that built
its own harness for the batched variant of this algorithm and found that a cost bound
"in every run" held on the good event only; `A1_REPORT.md` §8 — why this theorem is the one
result of the programme that would survive a hostile referee.)

## Why this review is the most valuable one we can commission

Our publication-level assessment (`docs/science/PUBLICATION_OPPORTUNITIES.md`, P1) concludes:
the strongest result of the whole programme is the pair of exact exponents for adaptive
and non-adaptive randomised algorithms on the cube class, and its non-trivial half is the
**adaptive upper bound** — a nested ("layer-cake") algorithm whose cost is a paper proof
with a history of **five repaired accountings** (`docs/DEAD_ENDS.md` D45), refereed twice by
the theory division's own referees (`docs/reviews/R7_referee_report.md`,
`R8_referee_report.md`), tested by the engineering division's adversarial search (no
violation in `7·10⁶` mean runs: read it with
`git show origin/research/ubuntu-engineering:docs/collaboration/responses/engineering/ENG-RES-0008.md`;
their implementation: `git show origin/research/ubuntu-engineering:src/metricchain_eng/twolevel/alg2l.py`),
and **never re-derived by anyone outside the theory division**.  Everything else in
§§11.19–11.26 (bounded accuracy, fields, rounds, several site types) is built on it by
"transfer".  If its cost accounting has a hole, the headline of the programme falls; if it
stands under an independent line-by-line derivation, the headline has what it lacked.

## The object

Theory report §11.18 and §11.19 (commit `5ed4072`: `grep -n '^### 11.18\|^### 11.19' docs/THEORY_REPORT.md`,
lines 3528–4196), the workstream reports behind them — `docs/workstreams/H_REPORT.md` (the
one-level algorithm, Theorem 11.52/11.54) and `docs/workstreams/K_REPORT.md` (Algorithm 2L⁺,
Theorem K1 = 11.56, Proposition K0 = 11.57(a), Proposition E, Theorem 11.58) — the Lean files
they cite (find them with `grep -rn "11.52\|11.56\|LayerCake\|HintRecursion\|GamePair" proofs/ docs/THEORY_REPORT.md | head`),
`docs/DEAD_ENDS.md` D45 (and D50), the two referee reports, and harness blocks in
`experiments/` that test the algorithm (`grep -rn "2L\|two_level\|twolevel\|layer" experiments/ --include=*.py -l`).

Background: §11.10 (the hinted problem; `h = KL(Λ₁/u‖½)`), §11.16 (non-adaptive exponent
`a = KL(p_u‖½)`, `θ_na`), Theorem 11.25.

## What a review here means

1. **Restate.**  Write down Algorithm 2L (one level, two samples) and Algorithm 2L⁺ exactly
   as specified — inputs, constants (`K`, `ν`, `η`, `b`, `J`, `m_max`, the ladder), every step,
   the stopping and abort rules, what is random, what is stored — and the statements of
   Theorems 11.52, 11.54, 11.56, Proposition 11.57 and Theorem 11.58 with all quantifiers:
   which class, which accuracy regime (extensive / bounded), validity "with probability
   `1 − δ`" against cost "in every run" or "in expectation", what `o(n)` hides.
2. **Re-derive, line by line, on your own paper**: (a) *validity* — the returned bracket
   contains the target on the good event; list every event in the good event and its
   probability; (b) *width* — the bracket has the claimed ratio; (c) **cost** — the number
   of evaluations, in every run or in expectation as claimed, with explicit constants.
   For (c) write your own accounting from scratch *before* reading theirs in detail, then
   compare term by term.  Where their proof has a step you cannot reproduce, say exactly
   which inequality and what would be needed.  D45 lists five earlier wrong accountings:
   for each, state in one sentence what was wrong and verify that the final proof does
   not repeat it in another guise.
3. **The assembly into exponents.**  How does the one-level cost become `θ_hint`
   (Theorem 11.54) and the multi-level cost `h` at bounded accuracy (Theorems 11.56–11.58)?
   Check the optimisation over the ladder and the level recursion (the Lean part: which
   declarations, what exactly do they state, is the paper step from the abstract recursion
   to the algorithm's exponent filled?).  Is the result "for every `η > 0` an algorithm with
   exponent `≤ h + η`" or "an algorithm with exponent `h`"?  What depends on `n`?
4. **Implement it yourself**, from the specification, before reading any implementation of
   the authors or of the engineering division: at sizes where exact reference values are
   computable (radial instances by shell sums; product instances; planted dips and cones;
   the flat-histogram instance; instances designed against each step of the accounting —
   e.g. many populated levels, a level exactly at a threshold, inner brackets that return
   their trivial bracket).  Measure validity and **cost against the claimed bound, run by
   run**, and search adversarially for an instance or a random seed on which the cost
   exceeds the bound or the bracket is invalid outside the stated failure probability.
   Then compare with the engineering division's findings in ENG-RES-0008 (do not re-run
   their code; state whether your instances overlap with theirs).
5. **An every-`n` statement.**  Is there a sub-class (radial functions; the zero residual)
   on which you can state and prove the cost with *explicit* constants for every `n` — no
   `o(n)`?  If yes, write it out; if the proof resists, say where.
6. **Verdict per statement** (proved / proved with a gap that you close / proved with a gap
   that you cannot close / false / not examined), with locations (file, line) for every
   finding, classified critical / major / minor as in the earlier reports of this
   repository; and a paragraph "what a hostile referee would attack first".

## Scope and honesty

This is a hard, long proof; you may not finish.  A partial review that is exact about
which lines were re-derived and which were only read is worth more than a complete one
that is not.  State at the top of the report how far you got.  Do not soften a finding and
do not inflate one: a gap is a gap only if you tried to close it and say what is missing.

## Deliverable

`docs/science/workstreams/R6_REPORT.md` in the format of COMMON, plus the sections: "the
algorithm as I understand it", "my accounting", "term-by-term comparison", "the five
earlier accountings", "what a hostile referee would attack first".  Final message: at most
600 words.
