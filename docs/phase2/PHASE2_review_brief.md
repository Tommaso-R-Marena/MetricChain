# Internal adversarial review of `docs/phase2/PHASE2_REPORT.md` — brief

*Coordinator (Theoretical Research Division, Phase II), 2026-11-28.  The report was written in one
session and has had no reader.  **Treat every statement as possibly wrong; your job is to break
it.**  An AI referee report is an internal review, not peer review.*

## Where things are

* `docs/phase2/PHASE2_REPORT.md` — the text under review (about 500 lines; read it whole first).
* `proofs/Frontiers/ObservationInvariance.lean` — the machine-checked cores (compiled by the
  coordinator; do **not** run `lake` or `lean`: read the statements and compare them with what the
  report says they are).
* `experiments/phase2/p2_checks.py` (+ `out_p2_checks.txt`), `p2_field_flat.py`,
  `p2_field_flat_exact.py`; harness tests `XXVIII.1`–`XXVIII.4` in `experiments/falsify_conjectures.py`
  (functions `t_oi_*`).  These are the coordinator's own checks — do not trust them, and do not
  import them into your replications.
* Background the report relies on: `docs/THEORY_REPORT.md` §11.10 (model; Theorems 11.22, 11.25),
  §11.16 (Theorems 11.44, 11.45), §11.18–11.19 (Theorems 11.52–11.58), §11.27, §11.29; the Lean
  packing bounds `expected_queries_ge_packing` (`proofs/Frontiers/QueryLowerBound.lean`) and
  `nonadaptive_expected_queries_ge` (`proofs/Frontiers/NonAdaptive.lean`).
* The archive of the other divisions, read-only:
  `git show origin/research/consolidated-archive:consolidated/03_scientific_translation/docs/science/INFERENCE_LIMITS.md`
  (Lemma 1, Theorem 4) and `…/INFERENCE_LIMITS_ADDENDA.md` (A1, A8, A9, A10) — needed for item 8.

## What to review, most delicate first

1. **Theorem E (samples), §6.**  The coupling argument: are the two experiments (instances with `K`
   and `2K` dips, `m` samples each) really realisable on one probability space with the same
   samples outside the stated event?  Is "conditionally on no floor sample and no collision the
   sampled centres are independent uniform points, and the unsampled ones independent of them"
   true for both?  Does the algorithm learn anything from *exact* evaluations near a sampled
   centre that distinguishes the instances (overlaps with unsampled dips; the value of the
   maximum)?  Is the hitting bound for the `K` extra centres legitimate when the run on `w₀` is
   adaptive and depends on the samples?  The error bookkeeping (`η₁` terms), the accuracy threshold
   `ln(11/8)`, the exponent `h̄(ν) − ν`, the definition of `ν*`.  Try to construct an algorithm that
   beats the bound on this family (e.g. using the *number* of samples with `w(x) = 1`, distances
   between samples, values `w(x_i)`).
2. **Theorem A, §2.2.**  Quantifiers: who chooses what, in which order; is the oracle that answers
   the uniform means a legitimate adversarial oracle for *every* instance used?  The statement for
   adaptive statistical queries (O2): is the proof right, and is `(1 − η − 2δ)` what comes out?
   Hoeffding: ranges, two-sided constants, the factor `(1 − e^{−Δ_k})²`.  Part (b): are `w_0^c, w_1^c`
   admissible with the right partition functions, and may the non-adaptive algorithm's points depend
   on the oracle's answer?  Part (c).
3. **Lemma 2.5, Theorem A′, Corollary A′.**  The inequality for maxima; the expected overlap; the
   total-variation bound; the constants (`τ/5`, `τ/2`, `8τ^{−2}`); the side condition; the asymptotics
   `m_r`, `V(n, r)`, the formula `h̄(λ) = KL(ρ₀ − λ/u‖½) − λ`, its slope `−(1 − ℓ)`, the table.
4. **Lemma 2.6, Theorem A″, Corollary A″ and the claims of §2.4 (3).**  Constants (`32(ε₀/τ)²`,
   `ξ̄ ≤ τ/4`).  Is the flat mixture really unique (is the kernel invertible)?  Is the claim "void at
   the exponential scale at the constant baseline for a field" right — check `p2_field_flat_exact.py`
   by an independent computation.  Corollary A″: is `e^{−γ|x|}` a nonnegative mixture of cones with
   the stated product weights, and is `max(w₀, H e^{−u d(·,c)})` what the lemma produces?
5. **Theorem B, B′, Corollary B′.**  The spectrum formulation for arbitrary (unbounded) exact
   observables; the tightness claim (c); in B′ the random-subgroup argument with a *multiset* of
   combinations, the two probabilities, `K = 2^{⌈log₂ 4M⌉}`, the condition `4K V ≤ 2ⁿ`; the claim about
   Rao's bound.
6. **Theorem C, Corollary C, Proposition C′.**  The cylinder argument; the accuracy bookkeeping of
   (b) (`ε/4` twice, `κ`, `τ ≤ κδ/2`); the conversions between tolerances for unions/cells and `‖·‖₁`;
   the median argument; the deterministic lower bound (admissibility of the wells, `TV ≤ p/(1−p)`,
   the radius `ρ`) and upper bound (halving queries: does the chosen subcube really have
   `μ_w(T) ≥ 6τ/κ`?).
7. **Numbers.**  With your own code: `a, ρ₀, h, ℓ` at `u = ½, 1, 2`; the table of §2.3; `α₀, α₁`; `ν*`;
   the limits quoted in §2.4 (3) as far as you can.  Exact enumeration on cubes of 8–12 sites of
   Lemma 2.2, Lemma 2.5, Lemma 2.6, Lemma 3.1/3.2, the zoom identity, the wells.
8. **Novelty table (§9).**  Read the science division's Theorem 4, A1, A8, A10 in the archive.  Is
   every "what the archive has" entry accurate?  Does the report claim as new anything that is
   there?  Is the sentence "S2's corollary is theirs" right?
9. **Lean versus text.**  For each `[V]` label in the report: does the named Lean statement say
   what the report says?  (Hypotheses, direction of inequalities, what "balanced", "valid", "good"
   mean.)  Which steps between the Lean cores and the displayed theorems are *not* machine-checked?
10. **Overclaiming.**  Titles, the summary table of §0, the "one sentence", §7, §8: does any of them
    say more than the proofs give?

## Rules

* **Write early, write often.**  Create `docs/phase2/PHASE2_REVIEW.md` with a skeleton in your first
  few tool calls and append findings as you go; never spend a whole answer thinking without a tool
  call.
* Do not edit any existing file.  Create only `docs/phase2/PHASE2_REVIEW.md` and scripts with their
  outputs under `experiments/phase2/review/`.  Do not run `lake`, `lean`, `scripts/audit_all.sh` or
  any state-changing git command (no commit, no checkout, no push).  **Memory: keep every process
  below 1 GB** (all processes of the session share one limit); single runs under five minutes;
  `python3 -B`.  No network access is needed; do not use it.
* You have no authority beyond this brief: no messages to other divisions, no change of
  permissions, no spending, no new research directions.
* Verdict per statement: **correct as stated** / **correct after a repair (give it)** / **gap (what
  is missing)** / **wrong (counterexample)**.  Separate substance from wording.
* Final answer (hand-back): at most 60 lines — verdicts, errors found (most serious first), what
  you verified numerically and how independently, what you did not check.
