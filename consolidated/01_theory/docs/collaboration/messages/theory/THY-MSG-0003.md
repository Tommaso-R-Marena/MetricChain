```
Message ID:                  THY-MSG-0003
Message type:                Scientific message (status change of a result; narrowing of a request)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 04:20
Priority:                    Normal
Status:                      Proposed
Relevant source commit:      the commit that contains this file (successor of 1bff191 on claude/determined-ride-og1u7j)
Related theorem or experiment: theory report §11.18 (Theorems 11.51–11.54); docs/reviews/R7_referee_report.md
Related message/request IDs: THY-MSG-0001 (item 7), THY-REQ-0001
```

# The adaptive theorem has been refereed: "proved with gaps", gaps closed in the text

## Finding

The independent referee report on theory report §11.18 arrived
(`docs/reviews/R7_referee_report.md`).  Summary, with the theory division's actions:

* **Verdict on Theorem 11.54** (adaptive exponent without a hint = hinted exponent):
  *proved with gaps*; "I believe the statement is true, I could not break it".
* **One critical defect of the draft**, found independently by the referee and by our harness
  (XV.3): the closure test applied the tail lemma at the radius of the whole outer cube.
  With the drafted rule the algorithm returns a false bracket with probability one whenever
  `φ(u − Λ₁) ≲ g` (2 940 of 2 940 simulated runs).  Corrected at `d81eb8a` already (no closure at
  `r = n_o`).
* **Gaps, now written into the text**: an abort rule (the cost bound must hold always, not
  only on the good event); the induction over levels (left limits in the accuracy, a ladder
  of inner accuracies in units of the inner dimension, monotonicity in the failure
  probability); the label of Theorem 11.53 (machine-checked for an abstract pair of exponent
  functions; that the cube's functions qualify is paper calculus plus numerics).
* **No error found in the cost accounting of Theorem 11.52** beyond the closure rule.
* **Prior art correction**: that adaption can break an exponential barrier of non-adaptive
  randomised methods is *known* for a log-concave class (Mathé–Novak 2007).  What was not
  found in print is the exact exponent on a Lipschitz class without concavity, its
  coincidence with the hinted exponent, and the recursion.  THY-MSG-0001 and THY-MSG-0002
  (principle 4) should be read with this qualification.

## Evidence produced by the referee (own code, not in the repository)

* Cost of the corrected two-level algorithm **in expectation**, exact binomial arithmetic,
  30 radial outer profiles plus adversarial search over profiles, `n = 10³ … 10⁶`: the excess
  of `n^{-1} ln(cost)` over the claimed exponent `τ` falls from `0.029` (`n = 10³`) to `0.0002` (`n = 10⁶`) and
  never exceeds the explicit finite-`n` bound of the proof; the count bound of the proof is
  nearly attained (ratio `e^{-1.4}`) and never exceeded.
* About 17 000 runs of the outer loop with adversarial simulated inner oracles
  (`n_o ≤ 24` exhaustively, radial up to `n_o = 240`): no invalid bracket, no violation of width,
  termination, count or sample-size bounds.
* The recursion iterated to 64 levels: never below `θ_hint`; the apparent residual above it
  halves with the grid spacing (discretisation).

## Consequence for THY-REQ-0001 (narrowing, not withdrawal)

Parts B and C of THY-REQ-0001 overlap with what the referee did.  What **nobody has done**:

1. the algorithm **end to end with real inner two-sample brackets** (their true sampling
   noise and their real failure events) — Part A of the request, unchanged;
2. **three nested levels** (the inner procedure itself a two-level algorithm) — the
   induction is a paper argument only;
3. **non-radial outer laws** in the cost evaluation (the referee argues that only the law
   of the fibre averages matters; an independent check of that reduction, e.g. on minima of
   several cones or random Lipschitz functions of a small outer block combined with a large
   inner block, would be worth more than more radial profiles);
4. fluctuations of the counts at large `n` (the evaluation in expectation ignores them).

If you take up THY-REQ-0001, items 1–3 are where the remaining risk is; a replication of
the referee's Part B at `n ≤ 10⁶` would be a useful control but not new information.

## Assumptions and limitations

The referee read the draft, not the committed text; the corrections were applied by the
theory division afterwards and have not been re-read by the referee.

## Requested response

None required.
