# Workstream L3 — Lean: the compensation lemma and Theorem A of workstream F (requested by the theory division), and two cores of addendum A16

*Brief written by the coordinator after checkpoint 33 (2026-11-25).  Read `COMMON.md`
first (commit pins there are out of date; nothing in this brief depends on them).*

## Why

The theory division asked for it (THY-RES-0007 §7.2, request F-T2 of our SCI-RES-0006):
"please do formalise the lemma and Theorem A if you are willing — … an independent
formal statement is worth more than ours; we will adopt the file as we adopted
`TwoRoundsExpected.lean`."  Their Proposition 11.109 will be rewritten on the strength of
workstream F's results, which so far are paper proofs checked by enumeration.

## What to formalise (Lean 4.31.0 + the pinned Mathlib; files that import Mathlib only, or
our own earlier files — say which)

Source: `docs/science/workstreams/SF_REPORT.md` §2.0–§2.2 (setting; Lemmas 0–3; Theorem A).
Style and reusable material: `experiments/science/ws_L1/MarginalOracle.lean` (the
oracle-indexed model of an algorithm; `theorem4_adaptive_marginal_oracle`),
`experiments/science/ws_L2/Sandwich.lean`, `Window.lean`, `Referee.lean`; reports
`docs/science/workstreams/L1_REPORT.md`, `L2_REPORT.md` (read their "discrepancies between
the paper statement and the formal statement" sections — produce the same for yours).

In order of value:

1. **Lemma 3 (compensation), complete.**  (i) For a weight on `{0,1}ⁿ` (any positive
   reference weight `π` that is invariant under a group `G` of coordinate permutations
   transitive on the sites — or state it directly for invariant measures) all one-body
   marginals equal the density; the marginals of a sum are the mass-weighted average.
   (ii) The linear equation: with `b = A_w (c_Δ − c_w)/(p₂ − c_Δ)` the two weights
   `w + b·w̃` and `w + Δ + b·w̃` have all one-body marginals equal to `c_Δ`, differ exactly
   where `Δ > 0`, and the ratio of their masses is `1 + (A_Δ/A_w)(p₂ − c_Δ)/(p₂ − c_w)`.
   Membership in the class: the cone `𝒲_u` is closed under sums and positive multiples
   (if L2 already has the cone, reuse it).
2. **Lemma 1(a)** in the oracle-indexed model: alternatives with the same oracle answer
   and overlap at most `m` force `(1 − 2δ)|J|/m` evaluations in expectation.  (L1's
   `theorem4_adaptive_marginal_oracle` may already contain the needed core — then derive
   the statement from it and say so.)
3. **Lemma 0 (window)**: every one-body marginal of a member of the class lies in
   `[p₋, p₊]`.  (`Window.lean` of L2 has the window of conditional laws — connect.)
4. **Theorem A, as far as it goes**: the every-`n` statement
   `E|Q(ψ₀)| ≥ (1 − 2δ)/(n·H_{k,r})` assembled from 1–3 and Lemma 2.  Lemma 2's two
   bounds (`e^r − 1 ≤ E_{k,r} ≤ e^r`, `|c_{k,r} − c₀| ≤ 1/(e^r − 1)`) are short algebra from
   `π·Δ = e^r π_s − min(e^r π_s, π_γⁿ)`; prove them, or — if the product-measure
   bookkeeping is too heavy — take them as explicit hypotheses and say so in the
   statement.  The Markov/Chernoff form with `ρ_t` is optional.
5. **If time remains — the algebraic core of Lemma A16.5** (`docs/science/INFERENCE_LIMITS_ADDENDA.md`,
   addendum A16; first look at `experiments/science/ws_R8/` — the referee of A16 was told
   that a Lean lemma is welcome; do not duplicate what is there).  On a finite type with
   positive weights `t`: (a) with `φ(t) = Σ t ln t + U₀ Σ t` and `f_η(s) = (1 − ηU₀)s − η s ln s`,
   `Σ t = Σ f_η(t) + η φ(t)`, hence `Σ t ≤ Σ f_η(t)` when `φ(t) ≤ 0`, `η ≥ 0`; (b) `f_η` is concave
   on `(0, ∞)` with its maximum at `ln s = 1/η − 1 − U₀`; (c) `F_η(ρ) = max{f_η(s) : e^{−uρ} ≤ s ≤ e^{uρ}}`
   is nondecreasing in `ρ`, and the maximiser is the clipped level; (d) the assembly
   `Σ_x t(x) ≤ Σ_x F_η(ρ(x))` for weights with `t(x) ∈ [e^{−uρ(x)}, e^{uρ(x)}]`.  Harper's theorem
   (the comparison of `#{x : ρ(x) ≥ k}` with the ball) stays a hypothesis; say so.
6. **If time remains — what the theory division asked in its §6.3:** items 1–2 of our
   Proposition A1.1 (`docs/science/workstreams/A1_REPORT.md` §2.5): conditional laws in the
   window (done in `Window.lean`?) and the chain-rule bound
   `KL(ν_ψ ‖ Q^{⊗n}) ≤ n·max_{a ∈ [a₀,a₁]} KL(Bern(a)‖Q)`.  Say exactly which items are
   formal after your work and in which file.

## Rules

Write only in `experiments/science/ws_L3/` (create it) and `docs/science/workstreams/L3_REPORT.md`.
Compile single files only:
`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path>`
— never `lake build`, `lake update`, `lake clean`.  **A long Lean build of another job is
running on this machine for the next hour; compile times will be slow at first.**  No
`sorry`, no `admit`, no `native_decide`, no new axioms; end every file with `#print axioms`
for each headline theorem and report the output.  If a statement turns out false as
written in the report (L2 found two such in Proposition A1.2), that is a finding: state
the corrected version, prove it, and list the discrepancy.  Keep `NOTES.md` from the
first minute.  The report must contain, per headline theorem: the Lean statement, the
paper statement it formalises, and every difference between them (conventions,
hypotheses added or dropped, generality).
