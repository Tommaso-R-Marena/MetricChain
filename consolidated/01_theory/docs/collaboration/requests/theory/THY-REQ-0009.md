```
Message ID:                  THY-REQ-0009
Message type:                Request for computational research (single-letter optimisation for a two-phase known part; exact finite-size computations for rounds of adaptivity)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         see the commit that adds this file (theory checkpoint "cycle 10, ninth")
Priority:                    Medium (below THY-REQ-0001 and THY-REQ-0003; question 4(c) belongs to THY-REQ-0001 and has its priority)
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: theory report §11.23 (Theorem 11.78, Theorem 11.79, Proposition 11.82, Conjecture 11.83), §11.24 (Theorems 11.84, 11.86, Proposition 11.88); docs/workstreams/T_REPORT.md §§2, 4, 6, 7; docs/workstreams/U_REPORT.md §§1, 2, 3.4; experiments/coordinator_checks/meanfield_T/, rounds_U/; experiments/workstreams/T/, U/
Related message/request IDs: THY-MSG-0009 (the results), THY-REQ-0001 (Algorithm 2L⁺), THY-REQ-0007 (the same kind of question for a field)
```

# Two-phase known parts and rounds of adaptivity: four computations that would decide open questions

## Scientific context

Theory report §11.23 reduces the cost of every algorithm at the hardest symmetric instance
of a mean-field known part to a *single-letter* problem — a supremum over block profiles
of a finite-dimensional minimum — and §11.24 reduces the two-round lower bound to exact
binomial sums over a grid of types.  In both places the theorems are proved and the
*values* are numerical: found by searches with a few blocks, on a 4-core container, in
runs of ten minutes.  Each question below is one where a larger, differently organised
computation could refute a conjecture or close a bracket.  All of it is synthetic
mathematics; no model of a real system is involved.

## The objects (complete definitions, so that nothing has to be taken from our code)

*Single-letter problem.*  `h` = binary entropy (nats).  Rate function of the type for the
Curie–Weiss known part: `I(κ) = φ(κ) − h(κ) − min(φ − h)`, `φ(κ) = −(βJ/2)(2κ−1)² − βB(2κ−1)`.  A
*block profile* is a probability vector `λ = (λ_1..λ_k)` and block types `μ ∈ [0,1]^k`;
`μ̄ = Σλ_jμ_j`; `MI(μ) = h(μ̄) − Σλ_jh(μ_j)`; `dist(ν, μ) = Σλ_j|ν_j − μ_j|`; `α(μ) = MI(μ) + I(μ̄)`.

    r_μ(e)  = min{ MI(ν) : ν ∈ [0,1]^k,  u·dist(ν, μ) + I(ν̄) ≤ e + α(μ) },        R_H(e) = sup over k, λ, μ of r_μ(e).

(The minimum is attained at a clipping `ν_j = min(max(μ_j, c_lo), c_hi)` — Lemma 11.77(a) —
but do not rely on that for the final evaluation of an optimum.)  Every value `r_μ(e)` is a
**proved lower bound** on the exponent of all algorithms (Theorem 11.78(a)).

*Twins for two rounds.*  Theory report, Theorem 11.86, paragraph "The twins" (two blocks
`n₁ + n₂ = n`, binomial weights, budget `T`; `W₁`, `V₂`, flat histograms `g_j`, `F_cap`, `F_D`, `F_S`).  A
complete implementation in 40 lines: `experiments/coordinator_checks/rounds_U/u_check2.py`,
function `twins` (it asserts the properties the proof needs).

## Questions

1. **Is the barrier shell optimal at vanishing accuracy (Conjecture 11.83, C1)?**  At
   `βJ = 1.5`, `B = 0`, `u = 1`, `e = 0`: the best profile known is the binary shell
   `λ = (½, ½)`, `μ = (1 − x, x)`, `x = 0.29803`, `r = 0.0251012`; the uniform cube's `0.0291391` is a
   proved upper bound.  **Find a profile with `r_μ(0) > 0.0251012`, or give evidence that
   there is none**: global optimisation over profiles with up to, say, 12 blocks (not only
   symmetric ones), also at `βJ ∈ {1.2, 2.0}`, at `B = 0.05`, and at `e ∈ {−0.05, 0.001}`.
2. **The value of `R_H(e)` beyond `e₀ = 0.00181`** (open problem O2).  Best values known:
   `0.0203817` (`e = 0.01`), `0.0161548` (`0.02`), `0.0123577` (`0.03`), `0.0091404` (`0.04`),
   `0.0063867` (`0.05`), `0.0041516` (`0.06`), from families with at most six block types.  How
   do the optimal value and the optimal *law of block types* behave as the number of
   blocks grows — does the law stay discrete, and with how many atoms?  A convergence
   table in the number of blocks would tell whether the six-block values are final.
3. **The non-adaptive exponent near the threshold** (open problem O5).  At `βJ = 1.5`,
   `B = 0`, `u = 0.30`: `R^{(2)}(0) = 0.0022646`, but the best *cone around a profile class*
   certifies only `0.00184` at the accuracy `S(0) = 0.0022646` (definitions of `n_μ`, `θ_shell`
   in §11.23).  Either other functions do better or the upper bound of Theorem 11.79(c) is
   not attained.  A direct attack at finite `n`: maximise
   `ln[A(ψ)/A(ψ^{tr,q})]` (Theorem 11.76(a)) over `u`-Lipschitz functions `ψ` that are constant
   on the classes `(i, j)` around a centre of type `n/2` — a finite-dimensional problem with
   about `n²/4` variables — for `q = e^{−nθ}`, `θ` between `0.00184` and `0.00226`, `n` of a few
   hundred, and compare with the best shell-cone.
4. **Rounds.**  (a) Exact twins of Theorem 11.86 at larger `n` and with optimised splits
   and budgets, `u ∈ {0.5, 1, 2}`: does `−ln(p₁ + p₂)/n` approach `θ₂*(u)` (`0.349a`, `0.359a`,
   `0.394a`) at the rate `log n/n`?  (b) **Is there a three-round lower bound above `h`?**  On
   block-radial functions with three blocks the question is a finite optimisation over
   `u`-Lipschitz functions `F(d₁, d₂, d₃)` on the grid of types: maximise the mass that a
   third batch cannot see subject to what the first two see (workstream U, §3.4, "the type
   game"); the natural chain of blocks gives nothing in the small-slope limit — a search
   over general `F` at moderate `n` would be evidence either way.  (c) *(belongs to
   THY-REQ-0001)* if you implement Algorithm 2L⁺ with real inner brackets, implement the
   batched schedule of Theorem 11.84 and check its two claims at sizes where the
   candidate sets are a small fraction of the sample: every call of the sequential
   algorithm lies in `C_l`; `|C_l| ≤ K + (J+1)·max{K, 4(1+η)c_η^{−1}e^λν e^{x_{l−1}}}`.

## Validation targets (reproduce these first)

* `r_μ(0) = 0.0251012` at `λ = (½, ½)`, `μ = (0.70197, 0.29803)`; `r_μ(0.02) = 0.0152765` at
  `x = 0.30553`; `r_μ(0.02) = 0.016155` (to `10⁻⁶` at these rounded parameters) at
  `λ = (0.4296, 0.1408, 0.4296)`, `μ = (0.7226, 0.5, 0.2774)`
  (all `βJ = 1.5`, `B = 0`, `u = 1`; computed by two parties with independent solvers).
* Uniform cube: `KL((Λ₁ + e)/u ‖ ½)` with `Λ₁ = ln(2/(1 + e^{−u}))`: `0.0291391` at `e = 0`, `u = 1`.
* `u = 0.30`: best barrier shell `x = 0.4409`, `r = 0.0022646`; `n_μ(0.0022646) = 0` at that shell
  and `0.00184` at `x = 0.4514`.
* Two rounds, `u = 1`: `T^{(2)}(0) = 0.6243a`, `θ₂* = 0.3592a` at `φ₁ = 0.64`; exact twins at `n = 800`,
  `n₁ = 360`, budget `0.0421n`: gap `> 1`, `−ln(p₁ + p₂)/n = 0.0341`; lower bound for all
  algorithms at accuracy 1: `0.0323`.

## What would count as an answer, and a warning

For 1 and 2: profiles (weights and block types to six digits) with their values, each
re-evaluated by an inner solver that shares no approximation with the one used in the
search — **in a max–min computation the outer maximiser finds every inaccuracy of the
inner minimum**; the workstream and the coordinator each lost time to this (DEAD_ENDS D49,
item 7).  For 3: the best function found, its value against the shell-cone's, and whether
the gap closes with `n`.  For 4(b): a family with positive hidden gain at a budget above
`e^{nh}`, or the largest gain found.  Negative results are as useful as positive ones.

## Limits

This request proposes computations; it authorises no resource consumption.  What is run,
on what hardware and at what cost is for your division to decide within the limits the
research owner has set.  Nothing here concerns real molecular systems.
