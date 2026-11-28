# Review brief — addendum on hidden partitions

You are an adversarial referee.  The document under review is
`docs/phase2_hierarchy/HIERARCHY_ADDENDUM.md` (self-contained; about 430 lines).  It claims two results that
are stronger than anything in the main report and were found late, by a short argument.  Short arguments
that prove much deserve suspicion.  Your job is to find what is wrong with them, not to confirm them.

## What to attack

1. **Theorem P (§A2).**  Read the proof line by line against the definitions of §A1.
   * Is each of (C1)–(C4) true as stated (including at the boundary values `0`, `1`, and for cells with
     classes on both sides of `½`)?
   * Step 1: does an `s` with `Φ(s) = θ` exist; do the levels `λ_g` exist; is `‖e − e′‖ = ‖m − m′‖`; is
     `T(e′) ≤ T(e)` really a consequence of (C4)?
   * Step 2: is `cost₁(e′) = T(e′) + Q(m′)`; are (H1), (H2) applied only where they are assumed?
   * Step 4: the per-cell price inequality in all cases (`ℓ < p_u`, `ℓ ≥ p_u`; mean central, deep, mirror).
   * Is the theorem consistent with the two-round separation (`c_2 > h`)?  With the one-round exponent?
     Try to derive a contradiction with a known lower bound.
2. **Falsify Theorem P numerically with your own code** (do not reuse the author's functions).  Suggested:
   exact extremal profiles on small lattices of types (2–4 classes, your own choice of nested partitions,
   including ones the author did not try: three classes in one cell; a class of weight below 5 %; a
   partition `𝒢₂` that splits a cell into three), and/or direct search for a `u`-Lipschitz `F` satisfying
   (H1), (H2) and violating the bound.  Report the largest excess over `h − θ` you find, in units of one
   lattice step `u`.
3. **Theorem H6 (§A4).**  Check the algorithm and the proof:
   * unbiasedness for an arbitrary `𝒢₂`; the count of evaluations; three rounds really are three batches;
   * the events `E₁`, `E₂`, `E₃` and their probabilities (conditioning, independence, the factor `n^{−2}`);
   * the exchange identities (X1), (X2): availability of the bits, which round's samples are used, that the
     partitions were chosen after the samples (no circularity);
   * inequalities (1), (2) and the bounds (S), (U);
   * step (e): the rounding, the two paths, each use of (X1)/(X2), the final arithmetic and constants;
   * step (d): `A_vis ≥ (n+1)^{−D} e^{ν₀}`.
   * Is the lower bound `c_r(HP_m) ≥ h` correctly attributed (the hidden dips of the archive's Theorem 11.25
     are functions of the distance to one centre)?
4. **Corollaries H7, H8 and the remarks** — is anything claimed that the theorems do not give?  In
   particular Remark 1 of §A4 (`m⁵ log n = o(n)`).
5. **The checks reported in §A3 and §A6** — do the outputs in `experiments/phase2_hierarchy/out/h11_*`,
   `h12_*` say what the text says?

## Rules

* Work only inside the repository at `/home/user/MetricChain`; local CPU only; no network; do not edit
  `HIERARCHY_ADDENDUM.md`, `HIERARCHY_REPORT.md` or anything outside
  `docs/phase2_hierarchy/HIERARCHY_ADDENDUM_REVIEW.md` and `experiments/phase2_hierarchy/review_addendum/`.
* Do not commit or push.  Do not spawn agents.
* Keep it bounded: at most about 40 tool calls; any single computation under 5 minutes.
* Classify findings as CRITICAL (a claimed result is false or unproved), MAJOR (a gap that needs a real
  argument), MINOR (fixable wording or constants), and say for each claimed result whether you believe it,
  and why.  If you find nothing wrong, say exactly what you checked and what you did not.

## Output

`docs/phase2_hierarchy/HIERARCHY_ADDENDUM_REVIEW.md`, and your scripts with outputs under
`experiments/phase2_hierarchy/review_addendum/`.  End your final message with a five-line summary:
verdict on Theorem P, verdict on Theorem H6, the most serious finding, the largest numerical excess found,
what was not checked.
