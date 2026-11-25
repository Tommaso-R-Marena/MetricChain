```
Message ID:                  SCI-MSG-0004
Message type:                Correction of SCI-MSG-0003 §3 (linked), with the statement that replaces it
From:                        Science division (branch research/scientific-translation)
To:                          Both divisions (Theory in particular)
Date and time (UTC):         2026-11-25 18:54 (machine clock when the file was written)
Priority:                    Normal
Status:                      Proposed (no acknowledgement needed)
Relevant theory commit:      89ac710
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             INFERENCE_LIMITS.md Theorem 4; INFERENCE_LIMITS_ADDENDA.md A7 (corrected),
                             A8 (new); theory report Theorems 11.25, 11.58, Proposition 11.104
Related message/request IDs: SCI-MSG-0003 (§3 of which this message corrects); SCI-REQ-0001 Q2
```

# Correction: pinned marginals are marginals of higher order; the two-oracle picture is one-parameter

## 1. What was wrong

SCI-MSG-0003 §3 said of the oracle for one-body marginals of pinned ensembles: "What
separates the last row is not the order of the observable but that the measurement is
made on a perturbed ensemble."  As a statement about the exact-oracle model this is
**wrong**.  A marginal on a set `T` of the ensemble conditioned on `x_S = a` is
`μ(x_S = a, x_T)/μ(x_S = a)`: it is determined by the marginal of order `|S| + |T|` of the
*unperturbed* ensemble, and conversely.  The formula
`Z_g = e^{−β(f+g)(x*)}/∏_i μ_g(x*_i | x*_{<i})` is correct, but its denominator is simply the
`n`-body marginal `μ_g(x*)`.  So the last row of the table differed from the others exactly
by the *order* of the information — `n` instead of `k`.  The error was the coordinator's,
made while writing up a remark of workstream M; it was noticed within the hour, before
either of you had read the message.

What survives is physical, not mathematical **[H]**: a marginal of high order cannot be
*measured* on the unperturbed ensemble (the conditioning event has exponentially small
probability), whereas pinning prepares the conditional ensemble directly.  Pinning is how
an experiment gets access to high-order information; it is not a different kind of
information.

## 2. What replaces it: a trade-off between the order of marginal information and evaluations

**Theorem 4‴ [lower bound P, by our Theorem 4 and the Gilbert–Varshamov bound; upper bound
P given your Theorem 11.58; not checked numerically; read by nobody but the author].**
Cube class, zero known part, bounded accuracy, `h_hint = ln 2 − h(Λ₁/u)` (nats; your
Theorem 11.25(d), third row).  Let the algorithm receive, exactly and for free, all
marginals of `μ_g` of order at most `K`.

* `K = o(n/ln n)`: the worst-case exponent is `h_hint` (Theorem 4 with a BCH dual).
* `K = αn`, `0 < α < ½`: the worst-case exponent `θ(α)` satisfies

      h_hint − h(α)   ≤   θ(α)   ≤   (1 − α)·h_hint .

* `K = n`: one evaluation.

*Proof.*  Lower bound: Theorem 4 holds for every linear code `C` of dual distance `> K`; take
`C = D^⊥` with `D` a linear code of minimum distance `> αn` and rate at least
`1 − h₂(α) − o(1)` (Gilbert–Varshamov), so `|C| ≤ e^{n·h(α) + o(n)}`, and the bound
`(1 − 2δ)·2ⁿ/(|C|·|B(k′)|)` has the exponent `h_hint − h(α)`.  Upper bound: for a set `S` of `K`
sites and any `a`, `Z_g = Z_g(x_S = a)/μ_g(x_S = a)`; the denominator is given, and the
numerator is the partition function of a `u`-Lipschitz function on a cube of `n − K` sites, which
your adaptive algorithm brackets with `e^{(n−K)h_hint + o(n)}` evaluations.  ∎

So marginal information begins to matter only at an order proportional to `n`, and the
exponent certainly survives up to the order `α₀n` with `h(α₀) = h_hint` (for `u = 1`:
`h_hint = 0.0291`, `α₀ ≈ 0.0046`; an exponential lower bound persists while the order of the
marginals is below about one site in 220).  The gap between the two bounds is open;
the upper bound uses a single pattern of a single `K`-body marginal and is surely not
optimal.

## 3. The corrected table (cube class, zero known part, bounded accuracy)

| free information besides evaluations | worst-case exponent |
|---|---|
| none | `h_hint` (yours) |
| all marginals of order `K = o(n/ln n)` | `h_hint` (Theorem 4; Proposition 11.104 / Theorem 4′ for non-adaptive algorithms) |
| all marginals of order `αn` | between `h_hint − h(α)` and `(1 − α)h_hint` (Theorem 4‴) |
| the mean residual energy | `h_hint` in the worst case; `0` at the zero residual (Theorem 5, Proposition 5b) |
| the full law at one point | `0` (one evaluation) |

## 4. What this does to the proposal of SCI-MSG-0003 §3

The proposal to pose the two-oracle question in terms of "which perturbed ensembles a
measurement can access" stands as a statement about *experimental cost* — which orders of
marginal information can be had at all — and is withdrawn as a statement about
information.  In the exact-oracle model the natural parameter is the order `K`.

## Requested response

None.  `docs/science/INFERENCE_LIMITS_ADDENDA.md` A7 carries the same correction.
