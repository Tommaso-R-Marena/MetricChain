# Workstream X — is worst-case envelope uncertainty the right model?  Alternatives and tractability

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_X/`; your report: `docs/science/workstreams/SX_REPORT.md`.

## The situation

The theory division's central negative result (`docs/DEAD_ENDS.md` D28; theory report §§11.4,
11.10, 11.16–11.19): if all that is known about the residual `g` is a first-order
(Lipschitz-type) envelope, certifying `min(f+g)` or `ln Z(f+g)` costs exponentially many
evaluations of `g`, for every algorithm, with exact exponents.  The hard instances are
adversarial **dips**: a residual that vanishes everywhere except on a small ball the
algorithm did not query.  The division's own conclusion — "the kind of class decides, not its
size" — points at the modelling assumption rather than at algorithms: classes that are linear
in a few known features are cheap; weakly coupled second-order classes are cheap; dense
first- or second-order classes are not.

That leaves the question nobody in the programme has asked head-on: **is a worst-case
(adversarial, set-membership) class the right representation of what is not known about a
molecular energy function — and if not, what replaces it, with which guarantees?**  A
physical residual (solvation, polarisation, a quantum correction, the error of a fitted
potential) is not an adversary; but "it is not an adversary" is not a theorem.  You are asked
to find the formulations in which it becomes one.

## Directions (choose, combine, or replace; depth over breadth)

1. **Average-case / Bayesian residuals.**  Let `g` be a random field on the product space —
   e.g. a centred Gaussian process on `{0,1}ⁿ` with a product (tensor) covariance
   `k(x,y) = σ² ρ^{d_H(x,y)}`, or with a general ANOVA spectrum `(σ_m²)` over interaction orders
   `m` (the Hamming-scheme eigenbasis), or a random energy model as the opposite extreme.
   What is the number of evaluations needed to output `min(f+g)` or `ln Z(f+g)` within `ε`
   with probability `1 − δ` *over the prior and the algorithm* (the average-case setting of
   information-based complexity; Bayesian optimisation; Bayesian quadrature)?  Is there a
   clean theorem of the form "polynomial iff the ANOVA spectrum decays (effective interaction
   order bounded)", with the exponent a function of the spectrum?  How does the answer
   interpolate between the theory division's cheap linear classes and the exponential
   first-order class?  What is the *certificate* in a Bayesian setting, and what is it worth
   if the prior is wrong (prior-robustness; calibration)?  Compare honestly: a
   prior-relative probabilistic guarantee versus a class-relative deterministic one.
2. **Weighted and finite-order classes (tractability theory).**  Information-based complexity
   knows exactly when high-dimensional problems escape the curse: product weights with
   `Σ γ_j < ∞`, finite-order weights (Sloan–Woźniakowski; Novak–Woźniakowski vols. I–III;
   Kuo–Sloan–Wasilkowski–Woźniakowski on anchored/ANOVA decompositions).  Map the theory
   division's classes onto that theory precisely: which of their results are instances of
   known tractability/intractability theorems (curse of dimensionality for Lipschitz
   classes; polynomial tractability for finite-order weights), which are not (their targets
   are `min` and `ln Z`, not integrals or `L²` approximation; their costs are instance-wise
   and adaptive)?  The lever-arm law (per-torsion constants *growing* like `m^{3/2}` along the
   chain) is the opposite of decaying product weights: is there a change of variables
   (local frames, internal vs Cartesian, multi-scale / hierarchical coordinates) in which a
   physically reasonable residual has summable weights?  State and, if possible, prove a
   tractability theorem for `ln Z` or `min` over a finite-order-weighted class with
   position-dependent weights that a chain molecule could plausibly satisfy.
3. **Structural conditions on the instance rather than the class.**  Perturbation stability
   (Bilu–Linial; Makarychev–Makarychev–Vijayaraghavan; Lang–Sontag–Vijayaraghavan for MAP
   inference), sharp minima / funnels (the theory report's "sharp site" condition is a
   funnel condition `E(y) − E(x*) ≥ d(x*,y)`; energy-landscape theory's minimal-frustration
   principle of Bryngelson–Wolynes–Onuchic is its statistical cousin), the empirical ease of
   side-chain placement instances (Kingsford–Chazelle–Singh; Sontag et al.), certifiable
   vs. non-certifiable regimes for random instances (Bandeira–Kunisky–Wein; Montanari–Sen).
   Is there a theorem "a funnelled (minimally frustrated) pairwise landscape has a
   polynomial-size certificate of its minimum, also under envelope uncertainty of slope
   below the funnel slope" that goes beyond the product case the theory division proved
   (§11.4: one evaluation suffices iff every site is sharp), e.g. for *interacting* known
   parts with a sharp-minimum condition, where the certificate must also prove the sharpness
   (a `(min,+)` problem `min_y [f(y) − d(x*,y)] ≥ f(x*)` — when is its LP relaxation tight)?
4. **Something else** that you judge to be a stronger paradigm (smoothed analysis;
   PAC-Bayes; conformal / distribution-free guarantees over a population of molecules
   instead of a class of functions; game-theoretic probability …).  If you take this route,
   formulate it precisely, examine prior art, derive consequences, look for counterexamples,
   and compare with the envelope paradigm on the same toy problem.

## Standards specific to this workstream

* At least one **theorem with proof** (or a precise refutation) and one **numerical
  experiment on the same toy problem under both paradigms** (worst-case class vs your
  alternative), with the cost in evaluations as a function of `n`.
* Say what each paradigm's guarantee *means* to a user who must decide whether to trust a
  predicted ground state or free energy: what is assumed, what can be checked independently,
  what happens when the assumption fails.
* Prior art with reading levels.  Bayesian optimisation regret bounds (Srinivas et al.;
  Bull), Bayesian quadrature, average-case IBC (Ritter; Wasilkowski), probabilistic
  numerics, and the tractability literature are large: position your statements against
  them precisely.
