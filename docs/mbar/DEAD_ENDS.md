# Division 9 — negative results, limitations, and corrections of our own errors

*Every item is kept with its evidence.  "N" = negative result or limitation of a method; "E" = an error
of this division found during the work (by a test, a benchmark or the internal review), with its
correction.  Review findings are added at the end as they arrive.*

## Negative results and limitations

**N1.  The handoff's variance formula cannot be used near the boundary of the simplex.**
`V_c = cᵀL^+c − Σ c_k²/s_k` subtracts two quantities of size `1/s_k`; for `s_k ≤ 10⁻⁶` the result is
wrong in the second digit, and at `10⁻⁸` in the first (`0.800` against the true `0.8676` on a five-state
example; table in `RESEARCH_LOG.md`, cycle 1).  Optimal designs do sit on the boundary (N7), so this
matters.  The formula of Theorem A3(c) — a sum of two nonnegative terms — has no cancellation.

**N2.  Under correlated sampling the variance of MBAR is not convex in the allocation.**
768 of 3000 random segments violate convexity, the worst by 35 % (`results/lower_bounds_and_chains.json`
stores the instance).  The convexity theorem is a theorem about independent samples, or about the
optimally weighted estimator, or about a scalar inefficiency model (`MATHEMATICS.md` A11, A12).

**N3.  The handoff's cut-score certificate C1 has the wrong rate.**  Its radius scales like
`R/√N`; the right scale is `√(R/N)`.  It returns `+∞` in 4 of our 11 benchmark regimes (all with weak
overlap or many states) and is 1.4–5.8 times wider than the likelihood-ratio region elsewhere.  It is
valid; it is not useful where a certificate is most needed.

**N4.  The handoff's bridge certificate C2 is conservative by a factor 2.4–8.3** against the
likelihood-ratio region (union bound over `4|E|` tails; path sums that ignore cycles).

**N5.  The likelihood-ratio region is not sharp either: the price of `K`.**  It is 2.0–3.1 times wider
than the asymptotic interval `±1.96·se` for `K ≤ 10` in the synthetic benchmark, and 4.6–7.1 times wider
for the 26 umbrellas of the public data set.  Two causes: (a) it is simultaneous for all contrasts,
with a threshold `2(log(1/α) + ρ)` whose regret `ρ` grows like `(K−1)` times a logarithm (measured
`ρ ≈ 32` at `K = 26`); against the asymptotic *simultaneous* region (`χ²_{K−1}`) the ratio is about
1.4; (b) it is built on the retrospective information `L` rather than the efficient information, a
factor `√(R_c/V_c)` of 1.02–1.9.  A certified interval for a single contrast without the `K`-dependent
threshold is open (O3).  Partial remedy that is valid and implemented: restriction to a sub-ladder
chosen from the design (`restricted_interval`), which brings adjacent-umbrella contrasts on the public
data to 1.9–2.2 times the asymptotic width.

**N6.  The efficient ("tilted") region was analysed but not built.**  The tilt that recovers the
efficient information depends on the candidate `f`; the region stops being a convex sublevel set and
its exact computation is not a convex programme (`MATHEMATICS.md` B4).

**N7.  An equal-count pilot wastes budget when costs differ.**  In the system "costly middle" the
optimal design never samples the expensive state; the equal-count pilot spends a third of the budget
on it, and the two-stage rule reaches a mean-square-error ratio `0.292 [0.27, 0.32]` against uniform
where the oracle design reaches `0.205 [0.19, 0.22]`.  The equal-count *safeguard* has the same
defect.  A pilot with equal cost per state (`PILOT2C`: 0.265) and an equal-cost safeguard
(`PILOT2CE`: `0.226 [0.21, 0.25]`; in "costly ends" `0.141 [0.13, 0.15]` against the oracle's 0.124)
were added after seeing this.  Both changes were made after the first results and are labelled post
hoc.

**N8.  Where the ladder is well designed, re-allocation gains little.**  Homogeneous five-state
ladder: predicted ratio 0.94, measured `0.92 [0.85, 1.01]` — not distinguishable from no gain with
2000 replicates.  "Widths": predicted 0.91, measured `0.90 [0.82, 0.98]`.  The large gains are confined
to heterogeneous costs (factors 3–6 against equal counts) and to badly balanced overlap
(Dirichlet models, bottleneck: 24–55 %).  Against the naive *equal-cost* rule the gain of the pilot
rule in the two costly systems is small (0.166 against 0.182; 0.292 against 0.321).

**N9.  The one-step Neyman rule (the rule that is correct for EMUS) is inferior for MBAR** in every
system with a real gain (`0.869` against `0.758`; `0.401` against `0.166`; `0.632` against `0.292`;
`0.621` against `0.480`): MBAR's influence functions move with the allocation, and one step from the
pilot allocation is not the fixed point.

**N10.  Minimising the effective resistance (the earlier programme's criterion) is not minimising the
variance**: `0.816` against `0.758` (bottleneck), `0.335` against `0.166` (costly ends), `0.587`
against `0.480` (Dirichlet 0).

**N11.  The certified efficiency bound A6(i) is weak far from the optimum.**  For the uniform
allocation of the bottleneck system it certifies an efficiency `≥ 0.49` where the truth is `0.76`; on
the public data its plug-in value is `0.07` where the plug-in optimum predicts `0.37`.

**N12.  No sample-based method detects consistent trapping.**  With every state confined to one well
the model check never rejects (0 of 600), the region and the asymptotic interval exclude the true
value in every repetition, and the error is 7.6 kT.  This is a theorem (B7), not a weakness of one
test.  With one trapped state the check rejects in 37 % of the repetitions at 200 samples per state
and in all at 1000.

**N13.  The model check is only as good as its label predictor.**  On the public data (26 states) a
30-bin histogram predictor loses to MBAR's own predictor by hundreds of nats; nothing can be
concluded from the absence of a rejection.

**N14.  An estimated statistical inefficiency is not a certificate.**  AR(1) samplers with
contraction 0.9: after thinning by the estimated inefficiency the asymptotic interval covers in
82.7 % of 300 repetitions (nominal 95 %); untreated, in 36 %.  With contraction 0.99: 69.7 % and
12.3 %.  The likelihood-ratio region covered the contrast in 97.3–100 % of the repetitions, but its
*joint* coverage with untreated samples at contraction 0.99 was 92.3 % — below nominal.  Its apparent
robustness comes from its width; **it is not a guarantee** and is not claimed as one.

**N15.  Handoff D2 was not reconstructed.**  Its coupling argument was read and no error was seen; its
limiting statements (`M → ∞` at fixed `N`) were not re-derived.

**N16.  Asymptotic efficiency of the two-stage estimator is not proved** (`MATHEMATICS.md` A9); the
benchmark is consistent with it.

**N17.  Nothing here is a statement about a molecule.**  All coverage and error statements are on
synthetic systems with exact samplers.  The public data set has no ground truth; the numbers computed
from it are development evidence.

## Errors of this division, found and corrected

**E1.  Convergence flag of the Newton solver.**  A fit that had reached the minimum to machine
precision was reported as failed when the gradient stalled at `1.1·10⁻⁹` (weak overlap makes the
objective flat).  Found when the first allocation benchmark failed in every replicate.  Consequence:
the first certificate benchmark, already running, under-counted finite intervals; its log is kept as
`results/certificates_coverage_run1_INVALID.log` and the run was repeated.  Fix: convergence is
declared on the Newton decrement.

**E2.  A wrong optimum from an ill-conditioned formula.**  The first allocation routine drove one
coordinate to `10⁻³⁰⁰`, where the Laplacian route returned `V = 1.1489` — *below* the true minimum
`1.1853` given by two independent conic solvers.  Found by the test that compares the three solvers.
Fix: Theorem A3(c) as the only evaluation route, exact zeros, a floor that lets coordinates return,
and termination on the certified efficiency bound.

**E3.  Missing constant in the model-check statistic.**  The first version compared the classifier's
log-loss with the MBAR objective without its `f`-independent term; the statistic was `−2500` under
correct sampling.  Found by the smoke test (a correct statistic must be near zero or negative but not
by thousands).  Fixed; the unit test `test_model_check_is_quiet_under_the_model` now covers it.

**E4.  Wrong ranges quoted in the first draft of the mathematics note** (C2 "2.4–5.4 times wider"
where the stored results say 2.4–8.3; an inequality sign for `R_c = V_c + Σc²/s`).  Found on re-reading
against `results/certificates_coverage.json`; corrected before the first commit of the note.

**E5.  Protocol change after seeing results** (N7): the cost-aware pilot and the equal-cost safeguard
were added after the equal-count versions' weakness was observed.  Recorded here because a post hoc
method cannot be judged by the same runs that motivated it.

**E6.  An ambiguous argument in the allocation routine.**  `optimal_allocation` accepted either a
contrast (one entry per state) or a target measure (one entry per support point) and told them apart
by length; when the two lengths coincide a measure was silently re-read as a contrast.  Found by a
new test (the efficiency bound appeared to be violated by 0.50; it was the comparison value that was
computed for the wrong target).  No stored result used equal lengths except some trials of the
synthesis check S1, which was re-run after the fix with the same outcome.  Fix: the reading must be
stated (`kind=`), and the routine refuses to guess.

**E7.  Two ways in which a certified interval could have come out too narrow.**  Found by re-reading
the interval code against Theorem B2 while the review was running.  (a) The profile value at a
candidate endpoint is the result of an inner minimisation; if that had stopped early, its value —
an upper bound of the true minimum — would have moved the endpoint *inward*.  Such points are now
counted as inside the region.  (b) A batch whose plug-in gave probability zero to one of the batch's
own labels was dropped; dropping a batch because of its own data is not licensed by the theorem (the
batch's e-value is 0, not 1).  The code now abstains.  Neither path was exercised by the stored
benchmark: the rerun with the corrected code reproduces every coverage count and median width
(`results/certificates_coverage_v2.json`).
