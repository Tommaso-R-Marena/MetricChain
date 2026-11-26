# Internal review of `docs/workstreams/Z_ADDENDUM.md` (the envelope sequence; extensive accuracies) — brief

*Coordinator, 2026-11-26.  The addendum is the coordinator's own and unrefereed.  It was
written while `Z_REPORT.md` was under review, and it changes what the main theorem rests
on: the schedule of the report (cut orbit curves over a base of several epochs) is
replaced by the **envelope sequence** started at the non-adaptive exponent, with three new
claims — (i) the envelope sequence is admissible with no restart and no range condition,
has the smallest tops among admissible sequences, and its tops decrease to `h` at the sharp
rate; (ii) `τ_j ≤ b_j` for every `j ≥ 1` at the exponent level; (iii) at a positive accuracy
rate `g` the exponent of the schedule converges to `θ_hint(g)` geometrically, whence
`ln N(n; g·n, δ) ≤ n·θ_hint(g) + O((ln n)²)` at extensive accuracies.  **Treat it as possibly
wrong; your job is to break it.**  AI referee reports are internal reviews, not external
peer review.*

## What to review, in this order

1. **A1 (admissible sequences), Lemma A1, Lemma A2.**  Is Lemma A1 what the proof of
   Proposition U and Corollary U′ of `R_REPORT.md` give — in particular with a top `b_{j+1}`
   that may be *larger* than `b⁺(W_j, b_j)`, and with (S2) required only on `[0, b_{j+1}]`?
2. **A2, Lemma A3 (the envelope step).**  Is `𝖤(W, b)` a family (convex, nondecreasing,
   continuous on the *closed* interval, zero at zero, values in `[0, 1]`)?  The value at
   the right end; the case where `Σ(B, W(B))` is finite up to `b` (pairs with finite slope
   at zero); `f(0) = 0`.
3. **Corollary A4 (comparison)** — the induction, the domains, the end points.
4. **Proposition A5, Proposition A6 (the tops converge to `h`)**: the fixed-rate sequence —
   is it admissible ((S1), (S2), values in `[0, 1]`, convexity)?  Is `Σ(B, s) ≥ s + B/h − 1` right?
   The argument that the tops reach `ah/(a − h)` in finitely many steps (both cases
   `G_∞ > 1`, `G_∞ = 1`); the bound `c − h ≤ h(1 − h/a)/(i + h/a)` afterwards.
5. **Proposition A7 (sharp rate), Proposition A8 (`τ_j ≤ b_j`)**: the transfer from the cut
   curves (is the cut sequence admissible in the sense of A1; is Corollary A4 applied
   in the right direction); the base case `T_1 = θ ≤ M_{W₁, a}`.
6. **A9 (extensive accuracies)** — new and the most consequential:
   * the hypotheses (which pairs satisfy them; what is used of `J`);
   * Lemma A9: the subgradient `θ(e₁)/e₁` of `s ↦ Σ(B, s)` at the fixed point, the formula
     `κ = 1 − J′/(B + (1 − t₁)J′)`, the bound `J′(t₁) ≥ η/L`, hence `λ_η = hL/(hL + η)`;
   * Lemma A10: the structure of the lower convex envelope of `min(1, H)` (is the
     description right; is the tangency point beyond `h − η` under the stated
     condition); "`W_{k(η)+i} ≥ p_{i+1}` on `[0, h − η]`";
   * Proposition A11: the margin `m = θ_hint(g) − (h − Lg) > 0`, the two regions of
     intercepts, the choice of `η` and `k₁`;
   * Theorem Z″: does Proposition Z4 of `Z_REPORT.md` really give the type at an
     extensive accuracy `x̂ = g·n` (range of validity of Proposition Z3: `x̂ ≥ 𝒳` only?);
     the count `k = O(ln n)`; is the claim "`exp(n·θ_hint(g) + O((ln n)²))`" then right, and
     for which `g` (what happens for `g ≥ ε*`, where `θ_hint(g) = 0`)?
7. **Replication with your own code** (floating point is fine; say what is and is not
   certified): the envelope sequence for the cube at two slopes and for the Gaussian
   pair from the definitions (your own slope map and your own convex-envelope
   routine); its tops against the table of A6 and against the lower bound
   `1/(4cos²(π/(2j + 1)))` for the Gaussian pair; the comparison of A4 with the fixed-rate
   sequence and with a cut chain; the geometric convergence of A9 (the table of A9;
   the predicted `2ζ²e^{−ζ}/(2π²)`); Lemma A1 on envelope curves.
8. **Numbers of A8**: two rows of the table from `experiments/workstreams/Z/z2_formula.py`
   (mode `env`) — is the formula what Theorem Z′ says; and the claim "below every earlier
   bound from `n ≈ 3·10⁴` on" as a statement about formulas.

## Rules

* **Write early, write often.**  Create your review file with a skeleton in your first few
  tool calls; append findings as you go; never spend a whole answer thinking without a
  tool call.
* Do not edit any existing file.  Create only `docs/workstreams/Z_ADDENDUM_REVIEW.md` and
  scripts with outputs under `experiments/workstreams/Z/review_addendum/`.  Do not run `lake`,
  `scripts/audit_all.sh` or state-changing git commands.  **Memory: keep every process below
  1 GB**; single runs under five minutes; `python3 -B`.
* Verdict per statement: **correct as stated** / **correct after a repair (give it)** /
  **gap (what is missing)** / **wrong (counterexample)**.  Separate substance from wording.
* Final answer (hand-back): at most 60 lines — verdicts, errors found (most serious
  first), what you verified numerically, what you did not check.
