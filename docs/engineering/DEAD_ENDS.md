# Engineering dead ends and negative findings

Numbered `ED-n`.  Each entry says what was tried or believed, what showed it wrong or
useless, and what replaces it.  Process mistakes (as opposed to scientific ones) are in
`RESEARCH_LOG.md` §1.5.

## ED-1  "Dualise the sensitivity constraint to bound the hitting number from above" — useless

*Idea.*  The pricing problem for exact fractional hitting numbers is a maximum-weight
closure problem plus one budget row (ENG-RES-0006 §2).  Dualising the budget row gives a
bound computable by min-cuts for every `n`.

*Why it fails.*  The Lagrangian dual lets the adversary randomise over sets that are
sensitive only on average.  On the uniform cube, mixing `D = ∅` with the complement of a
single point is admissible and forces the relaxed value to `((1+e^u)/2)ⁿ/(e^ε − 1)`: exponent
`ln((1+e^u)/2) = 0.62` at `u = 1` against the true `0.029`.  Derived by hand; not computed.

*What replaces it.*  Branch on the budget row; use the closure structure only inside the
nodes.  On the uniform cube nothing is needed: Harper's theorem gives the exact value.

## ED-2  The farthest-point traversal count as a measure of metric entropy — not well defined, and a poor estimator

*Belief.*  `m(δ)` (number of points of a farthest-point traversal that brings the covering
radius below `δ`), used in `P_REPORT.md` §3.2, can be reproduced and extended.

*Finding.*  It depends on the starting point and on tie-breaking, which are not specified;
our values differ from the published ones (e.g. 125 against 88 at 13 torsions, `δ = ¼`).
Exact covering numbers at the same radius are up to 2.3 times smaller than our traversal
counts, so trends in `m(δ)` say little about the entropy.

*What replaces it.*  Covering numbers at a closed radius with a rigorous bracket (certified
dual lower bound, verified cover): `net_bracket` in `src/metricchain_eng/chains/profile_cover.py`.

## ED-3  "Exact set cover on profile classes stays easy as the chain grows" — false beyond 18 torsions at `L = 1`

*Belief.*  Dominance reductions shrink the cover instances to a few dozen rows (true up to
12 torsions: 356 classes → 50 × 48), so exact integer programming needs no time limit.

*Finding.*  At 18 torsions and `L = 1` the reduced instance is 1 037 × 623; at 19–24 torsions
six containers did not finish in 22 minutes and were stopped (job M-004).

*What replaces it.*  Time limits on every integer programme and a bracket
`[certified lower bound, verified cover]` when optimality is not proved (job M-005).  A
geometric algorithm that exploits the three-dimensional structure of the profile set has
not been tried.

## ED-4  Reading a plateau off a short range of sizes

The covering number at `ε = N/2`, `L = 1`, is 5 for four consecutive sizes (6 to 9
torsions) — the stopping rule of THY-REQ-0002 — and then resumes growing.  With integer
distances and gaps, covering numbers are step functions of the accuracy; a plateau over a
handful of sizes is not evidence of saturation.  The request's small accuracy rates
(`N/20`, `N/10`) coincide with fixed accuracies 0 and 1 for all `N < 20`.

## ED-5  Plain floating-point comparisons of weights with levels — a literal run aborts on the good event

The levels of Algorithm 2L⁺ are `s_j = s₀e^{jλ}` with `s₀ = e^{−ψ₀−un}`; the weight of the
reference shell is `s₀e^{un}` when its fibre is flat.  With `un/λ` an integer the two coincide
*exactly*, and `ln s_j = (−ψ₀ − un) + jλ` computed in floating point is off by rounding.  A
literal implementation then finds a point with "`U > s_j`" and "`L ≤ s_je^{−b}`" at the last rung
and aborts (step 3 of the algorithm), on a run on which the good event holds.  This is the
pitfall referee R8 recorded as m10; the cause is structural, not a coincidence of the test
instance.  Remedy in this branch: logarithms within `10⁻⁹` are equal (`tables.TIE`), and a point
at the last rung is classified by its upper end alone.  Consequence for controls: two
published rows of the workstream's radial table are decided by rounding
(`experiments/eng/twolevel/controls.py` shows both conventions).

## ED-6  Describing the worst instances by classifying what the optimiser returns — uninformative

Differential evolution returns profiles whose relevant part (a cone up to some radius, a
flat continuation) is overlaid with irregular slopes where the profile does not matter; a
classifier of the returned profiles labelled 404 of 468 maximisers "other".  What works:
evaluate a small labelled set of structured instances on their own and report which one is
best and how much the search gains over it (`seed_analysis.py`).

## ED-7  Part A of THY-REQ-0001 with real inner brackets at `n_o, n_i ∈ [20, 60]` and `10⁴` runs per instance — not run

Every sampled outer point receives at least one real inner bracket (its trivial bracket
straddles the levels below it), so a run costs about one simulated bracket per outer point:
`10⁶`–`10¹¹` brackets per run at these sizes with the theorem's constants, each `O(n_i)` binomial
draws.  `10⁴` runs on a few dozen instances would be thousands of core-hours for a failure
frequency that the union bound of the proof puts far below anything `10⁴` runs can resolve.
Run instead (X-006): the outer loop with real fluctuations and oracle brackets, with `K`
scaled down until the events of the proof do fail.  Real inner brackets beyond 13
coordinates remain undone; the honest way to do them is a small outer cube (`n_o ≤ 18`) with
a large inner one, a few hundred runs per instance.
