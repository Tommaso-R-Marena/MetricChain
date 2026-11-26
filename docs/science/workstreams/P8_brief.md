# Workstream P8 (launched 2026-11-26, after addendum A17 (15)–(16)) — the charged case: why the certificate stops at lysine and the patterned sequence, and which lever moves it

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date), then `P5_REPORT.md` in full (the predecessor: measurement of the cancellation,
the sign-reversal theorem, the function floor), `P3_REPORT.md` §§ on the certified
constants (Proposition 4, the closed form), `P6_REPORT.md` §§2–3, and
`docs/science/INFERENCE_LIMITS_ADDENDA.md` parts A17 (15) and, if it exists when you
start, A17 (16).  If the agent of this workstream is gone, its notes are in
`experiments/science/ws_P8/` and its draft in `P8_REPORT.md`.*

## Where we stand (coordinator's measurements of 2026-11-26; re-derive what you use)

The certified sandwich now reaches a compact ensemble that is not frozen: Ace-Ser₁₂-NMe on
the helix (`4.9·10⁹` assignments, 6.3 of 12 side chains off the anchor) is bracketed
within 0.08 nats at order 5 (triple shares, exact in-window evaluated terms).  For
twelve residues on the helix the certified constants of workstream P3 are
(`pi_inference/certificate_reach_table_H.log`):

| peptide | `Γ₄`, `Γ₅`, `Γ₆` (`k_BT`) | first-order estimate of the bracket, triple shares, orders 4, 5, 6 (nats) |
|---|---|---|
| Ser₁₂ | 5.4, 0.23, 0.0073 | 1.8, 0.080, 0.0064 |
| Leu₁₂ | 316, 45, 5.0 | (floor delocalises at order 4), `9·10⁻⁵`, `2·10⁻⁵` |
| Phe₁₂ | 8.2, 0.26, 0.0056 | `2·10⁻⁶`, `8·10⁻⁶`, `3·10⁻⁵` |
| **Lys₁₂** | 689, 145, 23 | 31, 7.3, 1.3 |
| **(LKSE)₃** | 1 874, 568, 147 | 100, 34, 10 |

and on small enumerated helices the true remainder against the certified constant
(coordinator's quick run; sup over all states, kcal/mol):

| instance | order 3: `Γ₃`; true sup; ratio | order 4 | order 5 |
|---|---|---|---|
| Lys₄ | 33.6; 0.189; 178 | 0.854; 0.0029; 290 | — |
| LKSE:5 | 287; 0.475; 603 | 29.2; 0.0505; 578 | 1.53; 0.0044; 347 |
| Ser₅ | 8.98; 0.049; 183 | 0.213; 0.0011; 187 | 0.0024; `3·10⁻⁵`; 80 |
| Leu₆ | 132; 0.057; 2 320 | 12.9; 0.030; 428 | 0.78; 0.0022; 350 |

So the ratio bound/truth is of the same size everywhere (10²–10³); what differs is the
truth: per subset it is about twenty times larger for lysine than for serine, and it
falls 4–6-fold per order instead of 20–40-fold.  **The frontier of the certificate is
"charged", not "compact".**

> **Correction by the coordinator (2026-11-26 06:25 UTC, sent to the workstream as a
> message):** the last clause conflates two things.  "4–6-fold per order" (more exactly
> 3–6-fold) is the fall of the *certified constants* `Γ_m` at twelve residues (first
> table), against 24–46-fold for serine and phenylalanine and 7–9-fold for leucine.
> The *true* largest remainder in the second table falls 65-fold from order 3 to 4 for
> Lys₄ and 9–11-fold per order for LKSE:5 (43- and 38-fold for Ser₅).  How the truth
> falls with the order for charged side chains is part of what you are to measure
> (questions 1, 2); do not take the brief's sentence as a datum.

## The questions, in this order

1. **Measure, as P5 did for leucine and serine, for the charged side chains.**  On the
   enumerated helix instances Lys₃, Lys₄, Lys₅ (115 248 states), LKSE:4, LKSE:5,
   LKSE:6 (and the same on the strand for contrast, if cheap): per order `m = 3 … n`
   (i) the exact anchored constants `c_T` of every subset (P5's definition and code:
   `ws_P5/s1_cancel.py`, `p5lib.py` — import read-only) and their sum; (ii) P3's
   certified `ĉ_T` and `Γ_m`; (iii) the best pair-by-pair bound; (iv) the lower bound
   for every sign-blind bound (P5's Proposition 7 and Theorem 8: the largest true
   remainder over sign patterns of the charges; say how the search was done and how
   good it is); (v) the split self / cross and, new here, **by atom group**: ammonium
   or carboxylate group, the aliphatic chain, the backbone, neutral side chains — which
   pairs of groups carry the truth and which carry P3's bound.
2. **Is the truth larger because of a monopole?**  For a neutral group the response of
   its self and cross terms to a distant change of Born radii cancels to dipole order
   (P5, Theorem 9); for a charged group it does not.  Quantify on the instances: the
   many-body terms of a subset that contains a charged group against one that does
   not, as a function of distance; what law in the distance (`r⁻⁴`? slower?); what
   order would an *ideal* certificate — exact constants in place of `ĉ_T` — need for
   twelve residues (extrapolate the per-subset constants with their decay; say that
   it is an extrapolation).
3. **Is part of P3's slack for charged pairs avoidable without signs?**  Read P3's
   cross-term bound (`ws_P3/gfbound.py`, `encl.py`; `P3_REPORT.md`).  For two atoms far
   apart the Still function `f = (r² + B_a B_b e^{−r²/4B_aB_b})^{1/2}` depends on the
   Born radii only through a factor `e^{−r²/4B_aB_b}`; a bound on the mixed differences
   of `1/f` that does not carry this factor is loose for exactly the pairs that
   dominate a charged peptide (large `|q_a q_b|`, large `r`).  Does P3's bound carry
   it?  If not: write the sharper bound, **prove it**, implement it as a subclass in
   your directory (do not edit `ws_P3`), validate `bound ≥ exact` for every subset of
   every enumerated instance, and report the new `Γ_m` for Lys₁₂, (LKSE)₃, Ser₁₂, Leu₁₂
   on the helix.  If it does: say so with the line of code and the formula, and
   look for the next largest source of slack with the decomposition of step 1(v).
4. **The verdict on levers.**  For the charged case, in numbers: how much could (a) a
   sharper sign-blind bound gain at most (step 1(iv)), (b) step 3 gain, (c) one more
   order cost (ball sizes are in the table log), (d) the theory division's sandwich
   sampler tolerate (its cost grows like `e^{D}` in the bracket `D`).  Which
   combination brings Lys₁₂ on the helix below one nat deterministically, if any.

## Rules

As in the P5 and P6 briefs.  Write only in `experiments/science/ws_P8/` and
`docs/science/workstreams/P8_REPORT.md`; import P2's, P3's, P5's and P6's code and the
coordinator's `pi_inference/window_model.py` read-only (copy nothing into their
directories; caches of yours go into `ws_P8/cache`).  No state-changing git; no `lake
build`; no subagents.  Model-relative statements only; the fixed synthetic peptides
of P2; no sequence is varied or optimised; nothing target-specific; no cloud compute.
Every bound claimed is checked against exact constants on every enumerated instance,
with counts of comparisons and the smallest margin.  A proof is written out line by
line; where it relies on a statement of P3's report, quote the statement and say
whether you checked its proof.  Scripts that produce cited numbers run with one
command; a log is cited only if its run reached its last line.  Machine: 4 cores and
14 GB shared with other jobs — `OMP_NUM_THREADS=1`, at most two processes, no process
above 3 GB, no run longer than 20 minutes without a checkpoint.  Keep `NOTES.md` from
the first minute.  Labels [P], [M], [N], [C], [H], [K] with reading levels for
anything cited; before calling anything new, search our own reports (P3, P5, P6) for
it.  Report your own errors.  A negative result with its reason is a result.  **If a
tool declines an action, do not work around it: keep everything in `NOTES.md` and
return the findings as text in your hand-back.  Do not delete files with wildcards or
`rm -r`; use fresh directory names.**

## The report

(0) Verdict in five sentences.  (1) The measurement (tables per instance and order;
by atom group).  (2) Monopoles: the distance law; what an ideal certificate would
need.  (3) P3's cross bound for far pairs: what it is, whether it is loose, the
sharper bound with proof and validation, new constants — or why not.  (4) Levers, in
numbers.  (5) Requests to the theory and engineering divisions that can be sent as
they stand (no request is an authorisation to spend anything).  (6) How to re-run.
(7) Not settled; not checked; own errors.
