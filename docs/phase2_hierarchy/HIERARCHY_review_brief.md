# Brief for the adversarial review of `HIERARCHY_REPORT.md`

You are an independent, adversarial mathematical referee.  Your job is to **find errors**, not to
confirm.  The report under review is `docs/phase2_hierarchy/HIERARCHY_REPORT.md` on the branch
`research/phase2-adaptive-hierarchy` of this repository (working directory `/home/user/MetricChain`).
Its author is another AI session; nothing in it has been checked by anyone else.

## What to review (in this order of priority)

1. **Lemma B (§3)** — the relaxation lemma, including the elementary facts (F1)–(F4), (R) of §1.
   Check every inequality of the proof, the choice of the anchor (in particular case (ii): the choice
   of the level `τ`, the claim `T(κ) ≤ Θ₂`, the size of the jumps), the use of the hypotheses (H1), (H2)
   with parities, the reflection argument, and the final bookkeeping of constants.
   *Try to refute the lemma numerically with your own code*: for small block sizes compute the
   pointwise largest `−F` satisfying the hypotheses exactly as the lemma states them (including the
   parity version: `F` may depend on the parities of the non-revealed coordinates) and compare with the
   claimed bound with its explicit constant `m(u + 5 ln(n+1))`.  Use exact binomial costs
   `t_j(d) = ln P_j(mode) − ln P_j(d)`.  The author's script `experiments/phase2_hierarchy/
   h1_relaxation_lemma_check.py` does **not** include parity-dependent profiles; yours should.
2. **Theorem H1 (§4)** — the three-round algorithm R3 and its proof: the reveal step and the centre
   candidates; the passage from "no sampled point reveals block `j`" to "`F` sees only `S` on `V(Θ)`" (the
   path argument); the events `E₁..E₄` and their probabilities; the estimate; the cost.
   *Implement R3 literally on real cubes* (`n ≤ 20`, two or three blocks, energy as a table on all `2^n`
   points, random admissible profiles including 2-periodic ones, profiles constant on large regions,
   profiles revealed only at rare types) and test: candidates are the centre or its antipode;
   `E Â = A` (unbiasedness) for every `M`; `Â = A` when all blocks are revealed.
3. **Lemma A2 and Theorem H2 (§5)** — the two anchors and the case analysis; the claim that
   `Ξ(θ, φ₁)` is decreasing in `θ`; the use of the archive's Theorem 11.86 for the lower bound
   (`docs/workstreams/U_REPORT.md` §2.2 — read only that section).
4. **Corollary H4, Propositions G and C (§§6–7)** — are the statements what the proofs give?  For G check
   the algebra (the anchor is in `D`; the monotonicity in `θ`; the polynomial identity).  For C check the
   two cases.
5. Anything in §0, §8, §10 that overstates what is proved.

## Rules

* Read `docs/phase2_hierarchy/HIERARCHY_REPORT.md` in full.  Do **not** read `docs/THEORY_REPORT.md`
  (1.2 MB) — everything needed is in the report under review and in `docs/workstreams/U_REPORT.md` §2.
* Write own code; do not import the author's scripts (you may read them to find errors in them).
  Python 3 with numpy/scipy is available.  Keep every run under ten minutes; no external computation.
* Do not run any state-changing git command and do not modify existing files.  Write your report to
  `docs/phase2_hierarchy/HIERARCHY_REVIEW.md` and your scripts and outputs to
  `experiments/phase2_hierarchy/review/`.
* Report findings by severity: **critical** (a stated theorem is false or its proof has a gap that you
  cannot close), **major** (a gap you can close, or a wrong constant/hypothesis), **minor**.  For each
  finding give the exact place, the reason, and — if you can — the repair.  State explicitly what you
  did **not** check.  If you find no error in an item, say what you tried.
* Be economical: this is a bounded review.  Stop when the five items are covered once.
