# Referee brief R12 — adversarial review of workstream Q

*Written by the coordinator (theoretical division) on 2026-11-26, after the twenty-first
checkpoint of cycle 10.  You are an independent referee.  Your job is to find what is
wrong, not to confirm.*

## 1. What is under review

`docs/workstreams/Q_REPORT.md` (878 lines, unrefereed, not committed) claims:

    for every u > 0, ε > 0, 0 < δ < 1 there is C such that for all n ≥ 2 the least number of
    evaluations of an adaptive randomised algorithm without a hint that returns ln Z on the
    class L_u(Q_n) within ± ε/2 with probability ≥ 1 − δ is at most   exp( n·h + C·√(n ln n) ),

with an explicit design (Theorem Q8: `k_M` nested levels of "Algorithm 2L⁺", cost at most
`exp(n·B_M + 𝓔_M)`), an explicit error term `𝓔_M` (its (5.2)), and
`limsup (ln N − nh)/√(n ln n) ≤ C_*(u) = 2√((1 + r̄)c₁(a/h + 4))` (Theorem Q9).

If this is right it replaces a sentence of the theory report that said the term was
"heuristically not better than `n^{3/4}`" — so it must be checked hard before it is stated.

Background, all in this repository (read what you need, statements first):

* `docs/workstreams/Q_brief.md` — the question that was put to the author.
* `docs/workstreams/K_REPORT.md` §2 (Algorithm 2L⁺ in full, all constants, the proof in nine
  steps; errata at the head) and `docs/THEORY_REPORT.md` §11.19 ("### 11.19": Lemma 11.55,
  Theorem 11.56, Proposition 11.57, Theorem 11.58, remarks (1), (1a), (1b), (2)) and §11.18
  (Theorems 11.52, 11.53 with the remark on the rate, 11.54).
* `proofs/Frontiers/RateFull.lean` — the machine-checked epoch arithmetic (`d_m`, `J_m`, `k_m`,
  `c₁`, `c₂`, `κ`); read the statements only.
* `experiments/reviews/R8/r8_flat.py` — an exact evaluator of `C_max` and all constants of
  Theorem 11.56 written by an earlier referee (independent of the author of Q).
* `experiments/workstreams/Q/` — the author's scripts (`qlib.py`, `qscheme.py`, `q1…q4`) and
  stored outputs.  **Do not trust them and do not import them in your own checks.**

One known issue you should carry through (found by another division's review of Theorem
11.56, not yet applied to the text): the abort rule of Theorem 11.56 as worded in the
theory report ("once `C_max` evaluations have been made") lets a run exceed `C_max` by up
to `M̄` unless the test is made *before every query, including inside inner procedures*;
`K_REPORT.md` §2.2 step 3 is the precise version.  Check whether the nesting argument of Q
(a `k`-level run charged exactly its certified bound as an inner procedure) is affected.

## 2. What to check — in this order of priority

1. **Lemma Q4** (closing radius at an *extensive* threshold `θ ≥ c_η^{-1}(m+1)e^{2u+e^u+me}`):
   re-derive `r† ≥ min{m−1, ⌊ρ_e m⌋+1}` and `ln(1/π†) ≤ m·θ_na(e) + ln(m+1)` from the
   definitions of `Γ̃`, `Γ″`, `[N]`, `[P]`, `r†`, `π†` in `K_REPORT.md` §2.1–2.2.  Then test it
   numerically with **your own** exact code (big integers / mpmath; `m` from 5 to 5000, several
   `u`, `e` across `(0, ε*]` and beyond): compute `r†` from the definition and compare.  Look
   for off-by-one errors at the ends (`r† = m − 1`, `e ≥ ε*`, tiny `m`).
2. **Lemma Q3** (bounded `θ`): the claimed constant `u` (instead of `u + ln 4`) and the
   claim that two hypotheses of Lemma K.4 can be dropped.  Re-derive; test numerically.
3. **Proposition Q6 (the slope step)** — the heart of the improvement.  Is it true that a
   level run at accuracy `x ≫ ln n` on an outer block of `≈ x/h` coordinates with
   `θ = e^{x − O(1)}` loses only `(B/h + 4)·ln n + O(1)` nats relative to the affine majorant?
   Check every hypothesis of Theorem 11.56 for these parameters (`λ = 1`, `η = ½`, `η′ = 1`,
   `ν₁ = 1`, the tolerance `b`, the ladder with `x_L ≤ b`, `x₀ = 2un_i`), the accuracy
   bookkeeping (what bracket ratio the level actually returns), the failure probabilities
   handed down (`δ′ = δ/(4LM̄)`), and the claim that the ladder of step 1 costs at most 1 nat.
   In particular: the majorant must hold **for all accuracies and all dimensions at which
   the level below is called**, not only at the top — look for a quantifier that was lost.
4. **Proposition Q7 (the drop)** and the claim that all `√`-losses add up to `C₁√n` with `C₁`
   independent of the number of levels (geometric decrease of the outer fractions across
   epochs).  Is the series really convergent with the stated value (≈ 5.5 at `u = 1`, `ε = 1`)?
5. **Theorem Q8 / Proposition Q9a / Theorem Q9** — the induction over levels and epochs:
   the invariant ("`ln(1/δ) + dimension·ln 2` grows by `O(ln n)` per level"), the accuracy
   schedule `c_m = ε/(13(m+1)(m+2))`, the claim `Σ ln M̄ ≤ n ln 2 + k·O(ln n)` along a chain
   because the outer blocks are disjoint, the condition `(k_M − 1)·O(ln n) ≤ n`, the choice
   `k ≈ √(n/ln n)`, small dimensions at the bottom of the nest (what happens when an inner
   dimension is `O(1)` or the inner block is empty?), integrality of `n_o`, `J_m = ⌈d_m⌉`.
   Recompute `C_*(u)` at `u = ½, 1, 2` from the formula (claimed 4.65, 8.64, 13.5).
6. **Numerics.**  Write your own evaluator of the *formula* (5.2) and, independently, an
   exact evaluation of the certified cost of the design for small depth (you may reuse the
   referee code `experiments/reviews/R8/r8_flat.py`; do not reuse `experiments/workstreams/Q`).
   Compare with the author's stored tables (`out_q4_bound_table.txt`, `out_q3_scheme_exact.txt`):
   does "exact certified cost ≤ formula" hold at every node you can afford?  Does the bound
   at `n = 6.4·10⁴`, `u = 1`, `ε = 1`, `δ = 0.05` come out as `0.71·na` (13 levels)?  Try to break
   the inequalities at awkward sizes (`n` from 2 to 200; `ε` very small or very large; `δ` near 1
   and near 0; `u = 0.1` and `u = 4`).
7. **The statement itself.**  Is "for all `n ≥ 2`" justified (small `n`: is the trivial bound
   `2^n` used, and is `C` then finite)?  Is the lower bound quoted in (c) (`n·h − O(ln n)`)
   stated in the theory report in the form used?  Does the definition of `N(n; ε, δ)` (cost in
   *every* run) match what the nested design delivers?

## 3. Deliverables

* `docs/reviews/R12_referee_report.md`: findings by severity — **Major** (a statement is
  false or a proof step fails; say whether the main claim survives and with what
  constants), **Minor** (wrong constants, missing hypotheses, off-by-ones, wording that
  claims more than is proved), **Observations**.  For each finding: the place (section /
  line of the report), what is wrong, a counter-computation or the missing argument, and
  the repaired statement if you have one.  End with: the list of statements you
  re-derived completely, those you checked only numerically, and those you did not check.
* Your scripts under `experiments/reviews/R12/` (Python 3, numpy/mpmath only) with their
  stored outputs and the commands to re-run them.

## 4. Rules

* Create only the files named in §3.  Do not edit any existing file.  Do not run `lake build`
  or `scripts/audit_all.sh`.  Do not commit or push or run any git command that changes
  state.  Do not start further agents.  No network access is needed.
* Memory: one Python process at a time, nothing above ~1.5 GB; other work shares the
  machine.  Prefer exact integer arithmetic and `mpmath` over large numpy arrays.
* Label every statement of yours as re-derived, numerical, or not checked.  A finding
  that the claim is correct is acceptable only with the list of what was actually done.

## 5. What to report back (your final message)

At most 40 lines: the verdict on the main claim (survives / survives with changed
constants / fails at step …), the Major and Minor findings one line each, the three
weakest links that remain, and the files you created.
