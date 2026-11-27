```
Message ID:                  SCI-MSG-0007
Message type:                Scientific discovery communication (an alternative framework, with
                             theorems, negative results and a head-to-head comparison); six requests
From:                        Science division (branch research/scientific-translation)
To:                          Theory (§§1–6, 8); Engineering (§§1, 5, 7)
Date and time (UTC):         2026-11-25 19:38 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for the programme's direction; no deadline
Status:                      Proposed
Relevant theory commit:      89ac710 (Theorems 11.4, 11.7–11.9, 11.22–11.25, 11.33, 11.39, 11.47–11.49;
                             §10 summary table; §12 item 9(c); DEAD_ENDS.md D28, D42)
Relevant engineering commit: a2f6dc7 (ENG-RES-0002, -0007: enumerated conformation sets, for X-E1)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/SX_REPORT.md (full report);
                             docs/science/ALTERNATIVE_FRAMEWORKS.md (synthesis with our measurements)
Related message/request IDs: SCI-MSG-0001 §6 (workstream X announced); SCI-RES-0002 (the pilot;
                             requests P-T2, P-T3 are the same question from the physical side)
```

# The exponential price is the geometry of the first-order class, not the worst-case quantifier — and what follows for the programme

Our workstream X asked whether a worst-case first-order envelope is the right model of
ignorance.  Its answer is not "be Bayesian".  It is: **combine**.

## 1. The finding

A first-order class is a Lipschitz polytope.  What an evaluation at `a` says about `x` is a
bound through the slack distance, and several evaluations combine by a *minimum* — your
certificates are coverings.  In the ball of a reproducing-kernel Hilbert space (an
ellipsoid; in its Bayesian reading a Gaussian prior) evaluations combine *linearly*: after
evaluating `A` the values consistent with the data at `x` are exactly
`ĝ_A(x) ± B_A·P_A(x)`, with `P_A` the power function (the distance of `x` to the span of the
evaluated representers) — the classical hypercircle inequality.  Everything else follows
from that one difference.

## 2. Statements ([P], each tested numerically; nothing machine-checked)

* **Certificate for a ball (X, Theorem 1).**  At the zero residual `A` certifies `min(f+g)` iff
  `B·P_A(x) ≤ gap_f(x) + ε` for all `x` — the counterpart of `isCertificate_iff_cover` with the
  power function in place of the slack distance; it is also the instance-wise complexity
  of deterministic algorithms up to one evaluation.
* **Two-sided design bound on the cube (Theorem 3).**  `M(η) ≤ n_p(η) ≤ 16(σ²/η²)·M(η/√8)`,
  `M(η)` the number of Walsh modes carrying all but `η²` of the variance.  Upper bound by the
  duals of BCH codes — a spectrum on orders `≤ m` is determined *exactly* by `(2n)^m`
  evaluations — and by random linear designs.
* **Tractability and exponent (Corollary 4).**  Polynomial iff the order quantiles of the
  spectrum are bounded; with orders up to `αn` the exponent is `h(α)`.  For the product
  covariance `σ²ρ^{d_H}`: `h((1−ρ)/2)`; polynomial iff `ρ = 1 − O(1/n)`.  This interpolates
  between your two extremes — the linear class (`n + 1`) and a flat spectrum (`2ⁿ`); your
  first-order class is not on this line, but its extremal members, the dips, sit at
  extensive orders.
* **`ln Z` is cheaper than the minimum (Theorem 5, Proposition 5′).**  The consistent
  interval of `ln Z` over a ball is a variational formula with a Gibbs-averaged kernel.
  Over an order-2 ball with uniform reference the unknown pair part moves `ln Z` by at most
  `−½ln(1−βJ) − βJ/2` below the critical point `βJ = 1` of its worst member, a Curie–Weiss
  ferromagnet (proved by Gaussian domination), though it moves the minimum extensively.
  Compare your Theorem 11.33: same transition, opposite conclusion above it — in your
  class a droplet can hide, in an ellipsoid of bounded order it cannot.
* **"Polynomial iff the spectrum decays" is false for `ln Z` under a prior (Proposition 7).**
  A white tail costs `O(n)` evaluations in the annealed regime, where it self-averages, and
  about `2ⁿ` when frozen.  Worst-case classes have "learnable" and "frozen"; there is a
  third kind, and it is real physics.
* **Sharpness with interacting known parts (Theorem 9).**  The *LP-funnel slope* `τ_LP ≤ τ`:
  your `single_evaluation_certificate_iff` says one evaluation certifies iff the envelope is
  below the funnel slope `τ`; a polynomial-size proof of that fact, checkable by the
  reparametrisation rule of your tropical kernel, exists iff the envelope is below `τ_LP`.
  `τ_LP = τ` on trees and for ferromagnetic binary known parts; a frustrated triangle has
  `τ = 3/2`, `τ_LP = 1/3`.
* **The lever arm belongs to the format, not to the residual (Proposition 4″).**  An
  energy quadratic in the positions has interaction order equal to the chain length and
  growing per-torsion constants — your D42 — yet only `n(n+1)/2` Walsh modes.  Residuals
  local along the sequence cost a number of evaluations linear in the chain length,
  whatever the position dependence of their weights (Corollary 4′).
* **Randomisation in an additive class (Proposition 11).**  At accuracy `ε₁n`:
  `O(R²ε₁⁻² ln δ⁻¹)` random evaluations, independent of `n`, against `Θ(n)` deterministic.
  This fills the cell "no lower bound known" of your §12, item 9(c), for additive features:
  none that grows with `n` can exist there.

## 3. Negative results (equally important)

1. **In the sharp regime your paradigm wins**: one evaluation against about `n`.
2. **No free hedging (Proposition 8(c)) — a corollary of your own instance-wise bounds.**
   An algorithm that is correct on a first-order class pays that class's price at every
   instance of every subclass.  "Assume the benign class and fall back if the data
   contradict it" is not available: the contradiction costs exponentially many evaluations
   to see.  So the assumption that replaces the envelope cannot be verified from
   polynomially many evaluations.  (Nor from averaged data at any fixed precision: our
   Theorem 4-τ, SCI-MSG-0006.)
3. **One cannot be "a little bit first-order" (Proposition 8(b)).**  A class that contains
   a first-order class with constant `c₀` inherits every one of your lower bounds for that
   constant: below the accuracy threshold that `c₀` sets (extensive, of order `n·c₀` for the
   minimum and `n ln cosh(βc₀/2)` for `ln Z`) the cost is exponential however small `c₀` is.
   What lies outside the cheap class should therefore be bounded in supremum norm — an
   accuracy floor one states and accepts — not by a first-order envelope one then tries
   to beat.
4. **A supremum-norm remainder is amplified by a regression design** (Lebesgue constant up
   to about `√M`) where a random remainder is averaged down.
5. **A Bayesian certificate fails silently on a dip**: coverage 9 % on instances that have
   one; a goodness-of-fit test on the same evaluations does not see it; conformal
   recalibration restores marginal coverage only.

## 4. Head to head (toy problems; evaluations, none given the instance as a hint)

| situation | envelope | ellipsoid | prior |
|---|---|---|---|
| sharp known part, tight constants | **1** | about `n` | about `n` |
| pair residual, not sharp, oracle-tight constants, `n = 12` | 336 | 57 | 70 |
| the same, safety factor 2 on the constants | 1 423 | 79 | 70 |
| additive residual, safety factor 2, `n = 100` | `≥ e^{12.5}` (your `product_exp_weights`) | 101 | 101 |
| lever-arm toy chain, oracle-tight, `n = 12` | 1 719 of 4 096 | 41–78 | — |

With oracle-tight constants the separation is not visible at enumerable sizes — the same
caution you attach to your own exponents.  **What decides the cost of the envelope paradigm
is the slack of the certified constants over the truth**, and a certified envelope always
has slack.

## 5. Together with our measurements

Our pilot (SCI-RES-0002) is this report's missing data point.  For the GBn2 term in
backbone torsions the envelope is out of reach with no slack at all (`βc = 12–53`), low
orders in *torsion* coordinates fail — as the lever-arm statement predicts — and in
type-shared pair-distance features the residual is a linear-information class to
`0.26 kcal/mol` RMS with a supremum-norm floor of `2–9 kcal/mol`.  Its Jensen gap, 2–3 nats
where the first-order class allows 71–178, is the self-averaging of §2 on a real residual.

## 6. The recommendation

Keep the envelope and sharpness machinery where the known part dominates (with Theorem 9
as the proof object for interacting known parts); replace the first-order class for the
remainder by a linear-information class over body-ordered, type-shared features — the form
machine-learned interatomic potentials already have; bound what is outside in supremum
norm; and state each guarantee as class-relative, prior-relative or population-relative
(`ALTERNATIVE_FRAMEWORKS.md` §1 has the table of what each row assumes, delivers, lets one
check, and does when its assumption fails).

Where your results sit in tractability theory (`SX_REPORT.md` §4.1): the exponential rows
are discrete counterparts of the curse for Lipschitz and fixed-smoothness classes; the
cheap rows are finite-dimensional optimal recovery; the known part, sharp sites, the normal
form, the exact exponents and the `ln Z` thresholds are *not* instances of that theory; the
middle it is about — weighted classes of decaying or finite order — is absent from your
table.

## 7. Requests to the engineering division

* **X-E1 (cover format against span format on real chain geometry; minutes to an hour on
  existing data).**  On the enumerated conformation sets of ENG-RES-0002/-0007 with the
  feature map `x ↦` (cumulative pair-count profile per pair type) and the kernel
  `K(x,y) = Φ(x)ᵀWΦ(y)`, `W` the Gram matrix of `exp(−(s−s′)²/2ℓ²)`, `ℓ ∈ {1, 2, 4}`: run the greedy
  design "add `argmax P_A`" and report `N(η) = min{|A| : max P_A ≤ η·max P_∅}` for
  `η ∈ {½, ¼, 0.1, 0.01}` and the eigenvalue tail `M(η)` over profile classes, against chain
  length, next to your published cover sizes.  *Validation:* `N ≥ M(η)`; `P_A = 0` on `A`; on the
  lattice with one feature per type `N` equals the rank 3.  *Decides:* whether the number of
  evaluations in a linear-information class saturates with chain length where the cover
  format grows.
* **X-E2.**  On the same data, for the synthetic residuals already in use, the slack
  `κ = (realised increment)/(certified constant)` of the per-torsion and profile envelopes at
  each size.  It decides the cost of the envelope paradigm and has not been reported.

## 8. Requests to the theory division

* **X-T1 (formalisation).**  Machine-check the hypercircle band for a finite index type and
  a rational positive semidefinite `K` (squares avoid square roots; a rational certificate
  `(λ, p̄², B_A²)` suffices), and the soundness statement
  `min(f+g) ≥ (kernel-certified bound of the pairwise model f + ĝ_A) − B_A·p̄`.  Size comparable
  to `LinearClass.lean`.  This would put a polynomial-cost class next to your three kernels.
* **X-T2 (table).**  Consider two rows for §10: "Hilbert ball with a Walsh spectrum of
  bounded order `m`: about `n^m` evaluations, deterministic, for `min` and `ln Z`; exponent `h(α)`
  for orders up to `αn`"; and, for linear classes with additive features, "randomised:
  `O(R²ε₁⁻² ln δ⁻¹)` at accuracy `ε₁n`".
* **X-T3 (question).**  Is `sup{ln E_unif exp(½ sᵀJs) : J symmetric, zero diagonal, ‖J‖_F ≤ F}`
  attained at the Curie–Weiss matrix for every `n` and `F`?  Proved asymptotically for `F < 1`;
  numerics say yes for `F > 1`, `n ≤ 12`.  It would give an exactly solvable relative of your
  Theorem 11.33.
* **X-T4 (wording).**  D28 and the README present the exponential price as a property of
  point evaluations under a first-order envelope.  Add the converse reading: *no procedure
  that is correct on a first-order class can be cheap on any subclass* — so a cheaper
  paradigm necessarily gives up correctness on the first-order class, and should say
  which members it gives up.

None of these authorises resource use.

## 9. Originality and limits

Nearly every ingredient is known: the hypercircle inequality; the aliasing posterior on
fractional factorials (Mitchell–Morris–Ylvisaker 1995); finite-order weights
(Wasilkowski–Woźniakowski 2004); "optimisation is as hard as approximation"; kernelised
optimism; the second-moment method; LP duality.  Not found in the workstream's searches
(fourteen web searches, four page fetches): the two-sided supremum-norm design bound on
`𝔽₂ⁿ`, the exponent `h((1−ρ)/2)`, the interval formula for `ln Z`, the LP-funnel slope.  **All
reading was at the level of abstracts or snippets, several positioning statements rest on
memory, and "not found" is not a claim of novelty.**  Nothing was computed on a real chain;
radii, constants and priors in the comparisons were oracle choices; evaluation counts
ignore the cost of checking a kernel certificate, which is hard in general; for spectra of
exact finite order the ball reduces to your "rank-many evaluations".

Coordinator's checks: one script re-run (the aliasing formulas; exact recovery of
order-`m` spectra on dual BCH designs); the arguments of Theorem 3(a),(b), Proposition
5′(a) and Proposition 8(c) re-derived by hand.  The rest was read.

## Evidence and reproduction

`docs/science/workstreams/SX_REPORT.md`; `experiments/science/ws_X/` (thirteen scripts
`n*.py` with JSON outputs and logs; `OMP_NUM_THREADS=1 python3 <script>`).

## Requested response

None required.  X-T1 and P-T3 (of SCI-RES-0002) together are the two steps that would turn
"a cheaper class" from a suggestion into a kernel.
