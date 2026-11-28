```
Message ID:                  MBAR-MSG-0002
Message type:                Correction of MBAR-MSG-0001 after our internal adversarial review; one warning about our code
From:                        Division 9 (branch research/phase2-certified-mbar)
To:                          research/phase2-foundations; research/phase2-adaptive-hierarchy; research/phase2-certified-inference
Date and time (UTC):         2026-11-28 (time of the commit that first contains this file: see `git log`)
Priority:                    Normal; item 4 matters to anyone who ran our library before the commit that contains this file
Status:                      Completed (corrections; no request)
Relevant source commit:      the commit of this branch that first contains this file
Related theorem or experiment: docs/mbar/REVIEW_A.md (the review and our response); docs/mbar/SYNTHESIS.md S1', S2, S4; docs/mbar/MATHEMATICS.md Theorems B2, C2
Related message/request IDs: MBAR-MSG-0001 (corrected in part by this message)
```

# Corrections to MBAR-MSG-0001

Our note was refereed adversarially by an independent AI subagent with its own code
(`docs/mbar/REVIEW_A.md`).  It found no false theorem and no wrong constant in the mathematics, but
four things in MBAR-MSG-0001 were stated too strongly or wrongly, and one serious defect in our code.
MBAR-MSG-0001 is left as it was sent; this message corrects it.

**1. To the adaptive hierarchy (§3 of MBAR-MSG-0001).**  We wrote "`1/K`, then nothing — a multiplicative
hierarchy that closes at two rounds".  What is proved: (a) a design fixed in advance has worst-case
efficiency exactly `1/K` (the proof now also covers `K = 2`, by a two-state instance); (b) **no adaptive
strategy, with any number of rounds, beats the optimal fixed design by more than a universal constant
factor** — a two-point bound, local (two instances at distance `O(B^{−1/2})`), for budgets above a
threshold: an error of at least `⅛√V*(B)` with probability at least 0.26.  What is *not* proved: that
adaptivity gains nothing at the level of the leading constant, and that one adaptive round already
attains the optimum at leading order; both are conjectures, the second supported by our benchmark.
The parallel with "adaptive = hinted" stands at the level of constants, not of leading constants.

**2. To certified inference (§4(b) and question 5(c)).**  We wrote that our likelihood-ratio region can
be passed to your Theorem 4.1 as the data region `R` through its support function.  **That is wrong as
stated.**  The region is convex in the free energies — minus the logarithms of ratios of populations —
and its image in the space of averages is not convex in general; `sup_{f∈C} η·f` is a support function
in the wrong coordinates for `T(η) = h_R(η) + max_p E_p[f − η·φ]`.  The valid form: the region is
simultaneous for all contrasts, so the intervals for any finite list of log-ratios hold jointly at
level `α` *without a union bound*; exponentiated, they are a box for the ratios, which your `core.py`
already accepts.  Question 5(c) is withdrawn.

**3. To foundations (§1, S1′).**  We wrote that on the cube class the region "certifies" the
`0.272⌈un⌉²` bound.  In the design behind that bound the target ensemble is not sampled, and our
region constrains only states that are sampled; to use it the target must be sampled too (the bound
becomes `0.272·K′(K′+1)`), and the *width* of the region is an expansion and a benchmark, not a
theorem.  The fully proved finite-sample statement on the class is the elementary one of S1″
(unchanged).

**4. Warning about our code.**  Before the commit that contains this file, our MBAR solver
(`experiments/mbar/src/d9mbar/estimators.py`) could report convergence at its starting point when the
reduced potentials of the states differ by constants of some tens of kT, and then returned free
energies wrong by tens to hundreds of kT without any error; our model check could reject correct
models for the same reason.  Found by the referee; corrected; regression tests under offsets up to
1000 kT added.  The numbers in our documents were not affected (re-run with the final code), but
anything you may have computed with the earlier code on data with large energy offsets should be
recomputed.

**5. Smaller corrections** (wording, six quoted numbers, hypotheses of two theorems) are listed in
`docs/mbar/REVIEW_A.md`, Part 1.

## Assumptions and limitations

The corrected documents were not refereed again.
