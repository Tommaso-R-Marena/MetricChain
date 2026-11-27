# Internal review of `docs/workstreams/R_REPORT.md` (the rate of the level recursion) — brief for two independent referees

*Written by the coordinator on 2026-11-26.  The report under review is a paper proof by
the coordinator, checked by nobody else.  It claims that Conjecture R of `R_brief.md` is a
theorem: `k²(τ_k − h) → 2π²h²θ_hint″(0)`.  Treat it as possibly wrong.  A referee who finds an
error, with a counterexample or a precise missing step, has done the job; a referee who
finds none must say what was checked and how.  AI referee reports are internal reviews,
not external peer review.*

## Common rules

* **Write early, write often.**  Within your first few tool calls create your review file
  with a skeleton (one heading per statement under review), and append each finding as
  soon as you have it.  Never spend a whole answer thinking without a tool call: a
  previous agent on this workstream produced nothing because its answers were cut off at
  the output limit before anything was written.  If an argument is long, write it into
  the file in pieces.
* Do not edit any existing file.  Create only your review file and your scripts
  (locations below).  Do not run `lake`, `scripts/audit_all.sh`, or git commands that
  change state.  Keep memory small (all processes of this session share one limit; no
  arrays above a few hundred megabytes).
* Python: `experiments/workstreams/R/rlib.py` has the pairs (Gaussian, cube, a kinked pair)
  through their dual function `J`; `r1_checks.py`, `r2_chain.py` are the coordinator's checks —
  read them critically, do not rely on them; write your own code for anything you assert.
* Definitions: `docs/workstreams/R_REPORT.md` §1; the operator `R` is `(11.18.2)` of
  `docs/THEORY_REPORT.md` (Theorem 11.52, around line 4781) and `Rstep` in
  `proofs/Frontiers/BoundedAccuracy.lean`; Lemma L and Lemma M are machine-checked in
  `proofs/Frontiers/LineDynamics.lean` (`line_le_Rstep`, `StepLE.monotoneS_step`) — check that
  the report quotes them with the right hypotheses.
* For every numbered statement in your part give a verdict: **correct as stated** /
  **correct after a repair (give the repair)** / **gap (say exactly what is missing)** /
  **wrong (counterexample)**.  Distinguish errors of substance from errors of wording.
* Final answer (your hand-back): at most 60 lines — verdict per statement, the errors
  found (most serious first), what you verified numerically (script names, outputs),
  what you did not check.

## Referee A — the upper bound (§§5, 6, 8 "Upper bound")

Review file: `docs/workstreams/R_REVIEW_A.md`; scripts: `experiments/workstreams/R/review_A/`.

1. **Proposition U** (§5).  Check every step: the use of Lemma M (including the case
   `θ(e) = 0`), the representation `F(e) = max_𝓔 Φ`, the hypotheses of Sion's minimax theorem
   (which set is compact; semicontinuity; quasi-convexity in `e` on `(g, ∞)`;
   quasi-concavity in the line), the three cases (a), (b), (c) of the inner infimum — in
   particular the claim in (c) that `B″ ≤ B` and `(B″, s) ∈ 𝓔` — and the passage from `𝓔` to its
   lower boundary.  Is the statement true for `W` with `W(0) > 0`?  For `θ` with `θ(∞) > 0`, with a
   finite slope at zero, with flat pieces, with kinks?  Test by brute force on the operator
   `R` itself (your own implementation of the infimum over `(φ, β)` and the supremum over `γ`,
   *without* using the shortcut that the supremum over `γ` sits at `max(β, μ)` unless you prove
   it), for convex `W` (expected: `R ≤` the bound) and for non-convex `W` (expected: the
   bound can fail).  Try to find a convex `W` for which it fails.
2. **Corollary U′**, **Lemma T**, **Proposition C** (§§5–6): the well-definedness paragraph
   (continuity of `p_j` at the crossing, `B_t(j + 1) < B_t(j)`, case A/B), convexity of the cut
   curves, the claim that the left derivative of `H_j` at `B_t(j + 1)` is a subgradient of `H_j`
   on all of `[0, b_0]` including where `H_j = ∞`, the induction (domains `[0, b_j]`, the
   requirement `W_j ≤ 1` there, `b_{j+1} ≤ E_j`).
3. **Lemma RC** (§6): every inequality of case (β), the bound on `m_{j+1}/m_j`, the uniformity
   argument as `b_0 ↓ h` (is "uniformly in all such `j`" justified? which quantities depend on
   `j` only through `B_t(j)`, `B_t(j + 1) ∈ (h, b_0)`?), upper hemicontinuity of the maximisers,
   and the claim that (C1), (C2) hold for `s_t` near `L`.
4. **§8, upper bound**: steps (i) and (ii), and the final limit.  Is the a-priori bound
   `τ_k → h` available under (H0) alone as the report says (read "Step I with numbers" in
   the remark after Theorem 11.53 of the theory report, around line 4990, and
   `RateFull.rate_top0`)?
5. Independently of the proof: compute the sequence of the exact dynamics of convex
   majorants (remark (1) of §5) for one pair with your own code and compare with the
   coordinator's numbers in `experiments/coordinator_checks/level_rate/README.md`.

## Referee B — the slope map, the lower bound, the passage time (§§1–4, 7, 8 "Lower bound", 9, 10)

Review file: `docs/workstreams/R_REVIEW_B.md`; scripts: `experiments/workstreams/R/review_B/`.

1. **§1**: the properties of `J` (concavity, `max J = h`, the set of maximisers, the two
   consequences of (H1), the formula `ϑ = θ″(h)/(1 + r)³` for `C²` functions, the identification
   with `θ_hint` through the shear and `θ_hint″(0) = −1/J″(L)`).  Check the numbers for the cube
   at `u = 1` and `u = 2` from the definitions of the theory report (`θ_na` through
   `KL(ρ‖p_u)`, `KL(ρ‖½)`), not from `rlib.py`.
2. **§2**: (Σ1)–(Σ7).  In particular (Σ5) (`Ψ_s`, the formula `D = min{w : Ψ_s(w) ≥ B}`, the bound
   (2.1)), and the proof of (Σ6) line by line (the algebra, the uniformity, where (H1) is
   used, whether `w → 0` uniformly is justified).
3. **§§3–4**: (P1)–(P3) and Proposition A against the Lean file (are the hypotheses of
   `line_le_Rstep` exactly what the report uses? is `σ ≤ σ′` available? the base case).
4. **§7, Lemma PT**: every inequality; the role of the overshoot `Δ̄`; the count outside the
   window; the order of the limits.  Test numerically with your own code on at least one
   pair that is neither the Gaussian pair nor the cube (define `θ` convex, smooth near its
   fixed point, compute `J` numerically).
5. **§8, lower bound**; **§9, Proposition K** (the kinked pair: the exact step `δ/h`, the count,
   regularity) and the heuristic classification (is the claim for `p = 1` plausible? test
   a pair with `θ` affine near `h`); **§10** (the Möbius computation: trace, determinant,
   angle; the closed form against the orbit).
6. One global test of Theorem R that does not use the report's machinery: iterate the
   recursion itself for a pair of your choice (a grid version is in
   `experiments/coordinator_checks/level_rate/iterate_exact.py`; write your own or check that
   one) and compare `k²(τ_k − h)` with the claimed limit and with the kinked pair's `1/k`.
