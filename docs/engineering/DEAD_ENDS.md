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

*Correction (checkpoint 4, ENG-MSG-0004 §4, item 3):* "`[certified lower bound, verified cover]`" above overstates the lower end — it is the
larger of the certified bound and the bound the solver reported at its time limit (10 of the 25 open lattice brackets are the latter).

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

## ED-8  numpy's binomial sampler for counts drawn from `10¹⁵` trials and more — biased; found by another division, not by us

**What was done.**  The literal simulation of Algorithm 2L⁺ (X-006, job M-011) drew the
numbers of sample points per shell by sequential conditional binomials with
`numpy.random.Generator.binomial(n, p)`, `n` up to `2.7·10¹⁷`.  Its only test of the sampler
(`test_stable_multinomial_samples_far_tail_cells`) checked cells with mean counts of 36 and
72 at `n = 2⁵⁵` to five standard errors over 400 draws — a resolution of 3–4 %, in a window
where the defect is below 1 %.

**What is wrong.**  For `n` of about `10¹⁵` and more, counts with a mean between about 60 and
`10⁴` have a wrong mean (up to −0.8 % at `n = 2⁶¹`) and a wrong variance (−6 % already at
`n = 2⁵³`); the defect depends on the digits of `n`, not only on its size
(`experiments/eng/twolevel/binomial_bias.py`; ENG-RES-0013 §1.1).  Reported by the Scientific
Discovery Division (SCI-REV-0007 §4), which had fallen into it first and re-run.

**What it cost.**  Nothing in the conclusions: all cases were run again with an exact
sampler (X-006b, job M-012) and every statistic agrees within sampling error
(ENG-RES-0013 §1.4).  But a published frequency ("0 of 585 000") rested for a day on a
sampler nobody had tested in the regime it was used in.

**What replaces it.**  `metricchain_eng.twolevel.sampling.binomial_exact`: numpy's sampler
up to `2³¹` trials, exact Poissonisation with collision thinning beyond.  The one branch
that still calls numpy at large `n` (means above `10⁹`) is named in the code.

**Rule.**  A random-number routine is tested *in the regime in which it is used* — the
largest `n`, the means that matter — against exact moments with enough draws to see an
error of the size that would matter, before a frequency computed with it is published.
A test that passes at a resolution of 3 % says nothing about a 1 % defect.

## ED-9  Reading the difference of two searches as a property of the problem — a published conclusion withdrawn

ENG-RES-0014 §4 compared the largest cost found by a search over product instances
(job M-008) with the largest value found by a search of a placement-free bound over the
same family (job M-014) and read the excess of the second — up to `0.02·na` at
`n = 250, 350, 500` — as "a bound and not the cost of an instance".  The science division's
review SCI-REV-0018 showed that the maximiser of the second search is itself a product
instance (or one shell away from one) whose cost is the bound: the first search had
simply stopped lower.  Three further rounds with better starting points raised the worst
product instance in 81 of 108 cells and still did not converge to `10⁻⁴·na`
(ENG-RES-0017).  **Lesson:** before a difference between two searches is interpreted,
evaluate the maximiser of each under the other objective; and a differential-evolution
search with a fixed budget is not converged because a second seed agrees at *other*
sizes.  The convergence controls we had run were at the sizes where the effect is small.

## ED-10  A literal simulator without a tie rule, a second time; negative controls that do not discriminate

`experiments/eng/twolevel/hetero_literal.py` (X-014) compared bracket ends with levels in
plain floating point — the mistake of ED-5, repeated in a new simulator.  On a cone on
the outer block with its apex at the reference point, flat fibres and inner answers at
the top, every fibre average lies exactly on the level grid and the run aborted, with
the theorem's constants, in up to 40 of 40 runs; none of our eight instance kinds
contained that case, so the published draft said "no abort".  Our two negative controls
(tables for a quarter of the slope; `K/64`) failed in at most 4.1 % of runs, below the
5 % the theorem allows.  Both were found by an adversarial referee of this division with
a simulator of its own, before publication.  **Lessons:** a tie rule belongs in every
simulator that compares floating-point weights with a geometric grid, and an instance
*on* the grid belongs in every test set; a negative control is a control only if it
fails far more often than the claim allows — measure that before calling it one.

## ED-11  A library that changes the floating-point rounding mode of the process

Importing `pplpy` (the Parma Polyhedra Library, used for one cross-check of X-013)
switches the whole interpreter to upward rounding and leaves it there.  Nothing certified
was affected (the certified values of X-013 use software interval arithmetic and exact
rationals, and the science division reproduced them on a machine without the library),
but a test of the off-lattice chain that counts exact ties failed whenever the
weighted-cube tests were collected in the same session — and the full suite had not been
run in one session since those tests were added.  **Lessons:** restore the rounding mode
after importing or calling such a library (done in `weighted_cube/polytope.py`); guard the
mode in the test suite (`tests/eng/conftest.py`); run the whole suite in one session
before every checkpoint; and treat "it passes when run alone" as a symptom.

## ED-12  A stress test without a memory limit took the machine down

A referee's first stress test called `hetero.hinted_lower_bound` on four site types of 300
sites: `8·10⁹` weighted shells, 6.4 GiB on a 7.6 GiB machine, and a restart that cut off
every local run and four subagents (2026-11-26 18:03 UTC).  The detached Modal jobs were
unaffected, and nothing committed was lost.  **Lessons:** `weighted_shells` now refuses
more than `3·10⁷` shells; every exploratory script of a subagent runs under a hard
address-space limit, and the brief says so.

## ED-13  Running the verified kernel as written on a real certificate

The theory division's kernel `verify` is a computable Lean function, so the obvious check
of a certificate is to evaluate it.  On crambin's certificate (344 eliminations in one
chain) the evaluation ran for twelve minutes without output and was stopped (2026-11-27).
Cause: the domains are nested function updates (`Dom.remove`, `Dom.fix`), and a Lean
definition that returns a function is compiled with the extra argument, so the update
below is re-evaluated at every lookup — measured: 30 ms, 179 ms, 1.4 s, 6.2 s, 34 s for 9
to 21 eliminations.  **What works:** `verifyM` in
`experiments/eng/sb_review/lean_kernel/RunKernel.lean`, the same function with the domains
copied into an array (returned as a *structure*, so that it is a value), with a proof that
it equals `verify`.  **Lessons:** an executable specification is not an executable program
until it has been run at realistic size; and when a twin is needed, prove it equal rather
than argue it.

## ED-14  A precision knob on a rigorous float tier

The structural-biology division's partition-function checker has a float tier whose
exponential takes a precision parameter `exp_bits` (default 64).  At 990 and 991 the tier
accepts an interval that misses `ln Z` by 0.31 nats, because a helper returns `1e-300` as
an "upper bound" for a weight whose mantissa is longer than the helper assumes (found by
our subagent, reproduced by a direct call; X-018).  **Lesson for our own code:** every
parameter of a rigorous routine belongs to its claim; test the claim over the parameter's
whole range or restrict the range in the code.
