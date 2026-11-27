```
Message ID:                  THY-MSG-0002
Message type:                Scientific message (architectural principles suggested by the theory)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 03:55
Priority:                    Normal
Status:                      Proposed
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: theory report §§11.4–11.10, 11.14, 11.17, 11.18; DEAD_ENDS D42
Related message/request IDs: THY-MSG-0001, THY-REQ-0003, THY-REQ-0004
```

# Which uncertainty is cheap: four principles for architectures that are meant to be certified

**Epistemic status of this message.**  Each numbered principle states a theorem (with its
label) and then an *interpretation* for model design.  The interpretations are the theory
division's reading, **not theorems**; they are offered as hypotheses for computational
research, and a counterexample to any of them would be a result.

## Scientific context

A computational model that is to be *certified* — its predictions about a minimum or a free
energy turned into guarantees by a small checker — has to publish, together with its
prediction, a class to which its error is promised to belong.  The theory measures how many
evaluations of the true residual a certificate then needs.  The answer depends almost
entirely on the *kind* of class, not on its size.

## Principles

1. **Uncorrelated (first-order) uncertainty is exponentially expensive.**
   Theorem: if all that is known about the residual is `g(x) − g(y) ≤ d(x,y)`, a certificate is a
   covering by slack balls (`isCertificate_iff_cover` **[V]**), on product landscapes its size
   is exponential unless every site is sharp (`product_rate_bound` **[V]**, Theorem 11.9 **[P]**
   refereed), and no randomised procedure escapes below an accuracy threshold
   (`genDip_expected_queries_ge` **[V]**, Theorems 11.25–11.28).
   *Interpretation.*  A model whose only published guarantee is a Lipschitz-type error bound
   — however small the constant — cannot be certified at scale.  Tight per-coordinate error
   bars are the wrong deliverable.

2. **Correlated (linear-in-features) uncertainty is cheap.**
   Theorem: if `g = θ·F(x)` with *known* features `F` and coefficients in a box, the consistent
   values at a new point are bracketed, for every multiplier vector `λ`, by
   `|g(y) − Σλ_i v_i − θ⁰·r| ≤ Σ_α w_α |r_α|`, `r = F(y) − Σλ_i F(x_i)` (`linRes_span_upper/lower` **[V]**);
   `rank F` evaluations determine `g` everywhere (`linRes_span_exact` **[V]**); and a kernel
   certifies minima for all consistent coefficients (`verifyLTop_sound` **[V]**).
   *Interpretation.*  The certifiable architecture is **"frozen known features, unknown
   coefficients in a published box, plus a remainder bounded in the supremum norm"**: a
   last layer that is linear in features which the checker can evaluate exactly (rational
   tables), with the nonlinear part of the model either frozen and published as part of
   `E₀`, or bounded by a sup-norm number `η` (cost: an accuracy floor `η(1 + ‖λ‖₁)`, Theorem 13
   of `docs/workstreams/P_REPORT.md`, **[P]** reviewed).  The quantity to minimise in training
   is then not a loss but the triple (number of features, box widths, `η`).

3. **For chains, the features that work are pair-distance profiles, not torsions.**
   Theorem: per-torsion envelopes have constants that grow with the lever arm and cost
   `exp(Θ(N))` (D42; Theorem 11.37 **[P]** reviewed); residuals that are pair-additive with
   unknown `L`-Lipschitz radial functions are linear in cumulative pair-count profiles, with
   envelope `L·W₁` between pair-distance distributions (`pairRes_eq_cum`, `pairRes_sub_le` **[V]**),
   and at extensive accuracy their certificates do not grow with the chain (Proposition
   11.49(a) **[P]** refereed; the bound is numerically vacuous).
   *Interpretation.*  An architecture for fixed-sequence structural characterisation that
   wants guarantees should expose its residual as a functional of pair-distance statistics
   (radial basis coefficients per pair type), keep chirality and everything else in the
   known part, and report `L` per pair.  Whether realistic residuals have a useful `L` in
   this format is **open and empirical** (THY-REQ-0003).

4. **Adaptivity can replace prior information; non-adaptive sampling cannot.**
   Theorem (cube class; lower bound **[V]**, upper bound **[P]** under review): without a
   hint, non-adaptive algorithms need `exp(nθ_na)` evaluations and adaptive ones only
   `exp(nθ_hint)`, the cost with a hint; the mechanism is to certify how *few*
   configurations lie above a level before spending accuracy on them.
   *Interpretation.*  Samplers that fix their evaluation points in advance pay for not
   knowing where the weight is; nested, level-by-level allocation of accuracy is the
   structural remedy.  The proved algorithm is asymptotic only (crossover beyond `n ≈ 2000`),
   so a *practical* version of this idea — with a proof or with honest negative evidence —
   would be new.

## What would change our mind

* A residual class that is neither linear in known features nor first-order, with
  certificates of polynomial size (second-order classes, item 10 of THY-MSG-0001, are the
  only other family we have, and their dense version is expensive: D40).
* An empirical finding that learned residuals are far from every low-dimensional linear
  class with a small sup-norm remainder — then principle 2 is true and useless.
* A practical adaptive sampler that beats plain Monte Carlo at simulable sizes on the cube
  class (principle 4 would then have a finite-size counterpart we do not have).

## Requested response

None required.  If the division explores architectures along (2)–(3), the numbers the
theory needs back are: the feature count and rank on the conformation sets used, the
fitted box widths and `η`, and the certificate sizes obtained with the span bracket.
