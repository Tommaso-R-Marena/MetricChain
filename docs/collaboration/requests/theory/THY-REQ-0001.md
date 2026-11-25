```
Message ID:                  THY-REQ-0001
Message type:                Request for computational research (adversarial verification)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 04:20
Priority:                    High
Status:                      Proposed
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: theory report §11.18, Theorems 11.52 and 11.54; harness XV.3; benchmark B13
Related message/request IDs: THY-MSG-0001 (item 7)
```

# Try to break the cost claim of the two-level "layer-cake" algorithm

## Scientific context

Theorem 11.54 says that adaptive randomised algorithms without a hint estimate
`ln A`, `A = 2^{-n} Σ_x e^{-ψ(x)}`, for every `u`-Lipschitz `ψ` on the Hamming cube `Q_n`, to accuracy
`ε₁ n` with `exp(n θ_hint(ε₁) + o(n))` evaluations, where `θ_hint(ε₁) = KL((Λ₁+ε₁)/u ‖ ½)` is the exponent
known for algorithms *with* a hint.  The proof has three parts:

1. lower bound — machine-checked in its one-shot form;
2. the recursion `T ↦ R[T]` and its convergence to `θ_hint` — machine-checked
   (`superSolution_le_hint`, `iterates_lt_hint_add`);
3. **Theorem 11.52: a two-level algorithm built on an inner bracket procedure with exponent
   function `T` has, on every instance, at most `exp(n τ + o(n))` evaluations**,
   `τ(φ, β, g) = sup_{γ ≥ β} [ min(γ, φ θ_na((g−β)/φ)) + (1−φ) T(γ/(1−φ)) ]`.

Part 3 is a paper proof.  Its validity half (the bracket contains `A`; width) is
machine-checked in its deterministic core (`LayerCake.mean_le_upper`, `upper_le_width`) and
tested (harness XV.3).  Its **cost half** rests on one count — "at most `32KJe²·e^x + 4K` of the
points sampled at a level lie within a factor `e^x` of it" — and on the bound `M ≤ 8Je² M†` for
the sample sizes.  Five wrong versions of this accounting preceded the current one
(`docs/DEAD_ENDS.md` D45), and an independent referee is reading it now.  The theory division
cannot test exponents: at simulable sizes the algorithm is dominated by constants.

## Question

Is there a `u`-Lipschitz instance on which the two-level algorithm (i) returns a bracket that
does not contain `A` with probability above its stated `δ`, or (ii) needs more evaluations
than `exp(n(τ + η))` for an `η > 0` that does not shrink as `n` grows?

## Exact definitions

* Algorithm: theory report §11.18, "The algorithm" under Theorem 11.52, at `d81eb8a`
  (parameters `φ, β, g`; `b = βn`, `G = gn`, levels `s_j = s₀e^j`, `K`, `J`, populated / negligible
  levels, closure test **not applied at radius `n_o`**).  Executable reading of the outer loop:
  `lv_two_level` and `lv_check_run` in `experiments/falsify_conjectures.py` (the inner procedure
  is simulated there by a valid bracket of the requested accuracy).  Inner procedure with
  `T = θ_na`: the two-sample bracket of Proposition 11.46 (formula in `docs/BLUEPRINT.md`, Step 5,
  "Without a model"; harness XIII.5).
* Expectation-level cost model on the zero function: `two_level_flat_cost` and `LevelCube` in
  `experiments/separation_benchmarks.py` (table "when would it pay?" of benchmark B13).
* `θ_na`, `θ_hint`: `na_theta_na`, `na_theta_hint` in the harness.

## Proposed computational approach

**Part A — validity with true randomness (no simulated oracle).**  On *bi-radial product
instances* `ψ(a, b) = F_o(dist(a, s_o)) + F_i(dist(b, s_i))` with `u`-Lipschitz profiles the whole
algorithm can be run exactly without enumerating the cube: an outer point is a draw of its
distance from `Binomial(n_o, ½)`, an inner evaluation is a draw from `Binomial(n_i, ½)`, the true
fibre averages and `A` are binomial sums.  Run the full algorithm (two-sample inner brackets
with their real sampling noise) for `n_o, n_i ∈ [20, 60]`, several `u ∈ {0.5, 1, 2, 4}`, profiles from
{flat, cone, flattened cone, dip of near-critical radius, flat bulk + bump, 2-periodic,
random Lipschitz walk}, and at least `10⁴` independent runs per instance.  Record: bracket
valid or not, width, number of evaluations, numbers of populated and negligible levels,
any violation of the events (V2), (V3) of the proof.

**Part B — the cost exponent, in expectation, at `n = 10³ … 10⁵`.**  Generalise
`two_level_flat_cost` from the zero function to an arbitrary radial outer profile `F_o` (the
fibre average of an outer point then depends on its distance only; exceedance
probabilities are binomial tails; inner cost charged either at the worst case `θ_na` or for
an actual inner profile).  Then **maximise** `n^{-1} ln(cost) − τ(φ, β, g)` over instances:
piecewise-linear `F_o` with slopes in `[−u, u]` (8–32 knots), plus products of two radial blocks
(to imitate several centres), with the algorithm's parameters fixed at the values that
minimise `τ` for the given `g`.  Any global optimiser will do (CMA-ES, differential evolution).
Report the supremum found as a function of `n` and the maximising profiles.

**Part C — a crossover map.**  For `u ∈ {0.5, 1, 2}` and `g/ε* ∈ {0.1, 0.25, 0.5}`: the least `n` at which
the two-level algorithm needs fewer evaluations than the two-sample bracket at the same
certified width, on the zero function and on the worst instance of Part B.

## Suggested inputs

Seeds and parameter grids as above; `δ = 0.05`; `K` from the proof,
`K = ⌈24 ln(2^{n+6} n³/δ)⌉`, and additionally a smaller `K` (e.g. 200) to see where the events
start to fail.

## Expected outputs

A table per part; for Part A the empirical failure frequency with a confidence interval;
for Part B the largest margin found at each `n` and the profile that attains it; raw
results as JSON; scripts under your branch.

## Resource requirements and runtime

Part B is CPU-only: one evaluation costs `O(n · levels)` log-binomial operations — seconds at
`n = 10⁵` when vectorised; an optimiser with `10³–10⁴` evaluations per configuration is tens of
CPU-hours in total.  Part A is dominated by inner sampling: a run needs up to
`M · m ≈ 10⁸–10¹⁰` binomial draws; `10⁴` runs per instance on a few dozen instances is a job for
Modal CPU workers or a GPU (binomial sampling vectorises trivially).  Part C is negligible.
A sensible budget is a few hundred CPU-hours; nothing here needs more.

## Suggested validation protocol (negative controls)

1. Reproduce harness XV.3 (`python3 experiments/falsify_conjectures.py --only XV.3`) and the
   B13 crossover table (`…separation_benchmarks.py --quick`) before changing anything.
2. The five mutations `XV.3 M1–M5` of `experiments/mutation_tests.py` (negligibility threshold
   without `e^b`; lower end without `e^{-b}`; closure at the whole-cube radius; upper end with
   the level itself; no tolerance in "high") must produce failures in your implementation
   too.  If closure at radius `n_o` does *not* fail in Part A on an instance with a small
   outer block and a constant far above the lowest level, the implementation is not testing
   what it should.
3. On the zero function the expectation-level cost must reproduce
   `sup_{γ∈[β, μ]} [γ + (1−φ) θ_na(γ/(1−φ))]` to within `O(log n / n)`.

## Stopping conditions

Stop Part A at the first reproducible invalid bracket on the good event and report the
seed.  Stop Part B when a margin above `0.01` (in the exponent) persists from `n = 10⁴` to
`n = 10⁵`, or when the budget is spent.  Do not scale Part A beyond the stated sizes: larger
sizes add cost, not information.

## What the possible outcomes would mean

* *A valid counterexample to the cost bound* (margin that does not vanish with `n`): Theorem
  11.52 as stated is false or its proof has a gap; Theorem 11.54 loses its upper bound and
  the adaptive exponent is open again between `θ_hint` and `θ_na`.  This would be the most
  valuable outcome and should be sent at once.
* *An invalid bracket beyond the stated failure probability*: an error in the validity
  argument that the machine-checked core does not cover (probabilistic events, the
  classification rule).
* *No violation*: evidence, not proof.  The theory division would then quote the largest
  margin found and its trend in `n`.
* *Part C*: quantifies "asymptotic only"; if the worst instance moves the crossover far
  below `n = 2000`, a practical variant becomes worth designing.

## Assumptions and limitations

Radial and bi-radial instances are a small subfamily of the class; the proof claims the
bound for all `u`-Lipschitz functions.  A search over this family cannot confirm the theorem.
Expectation-level evaluation ignores fluctuations of the counts.

## Requested response

`ENG-RES` with the tables, or a reasoned decline.  Partial results are welcome; Part B alone
would already be useful.
