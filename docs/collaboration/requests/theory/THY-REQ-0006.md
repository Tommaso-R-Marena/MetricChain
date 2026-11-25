```
Message ID:                  THY-REQ-0006
Message type:                Request for computational research (exact small-size computation; exploratory)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 03:55
Priority:                    Low (reassessed; see below)
Status:                      Proposed
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: theory report Theorems 11.22, 11.23, 11.26–11.28, §12 item 2(b); DEAD_ENDS D38 (harness DEAD.14, DEAD.16)
Related message/request IDs: THY-MSG-0001 (item 5)
```

# Exact fractional hitting numbers over all sensitive sets (reassessed)

## Scientific context and reassessment

The lower bound for every randomised algorithm is `(1 − 2δ)` times a fractional packing
number of *sensitive sets* — the sets on which an admissible perturbation that moves the
answer by more than the accuracy differs from the instance (`expected_queries_ge_packing`
**[V]**).  The theory evaluates this bound with special perturbations (dips, generalised
dips), and it is known that these are **not** always extremal: unions of shallow dips are
sensitive where no single dip is (D38; harness `DEAD.14`), and on product landscapes dips
centred at boxes beat single dips exponentially (`DEAD.16`).  An earlier checkpoint proposed
to compute the exact fractional hitting number over *all* sensitive sets on small
instances.

Since then the exponents on the cube were settled in every accuracy regime, with a hint
(Theorem 11.25) and without (§§11.16, 11.18), and at additive instances of identical sites
(Theorems 11.27, 11.28).  The computation is therefore **no longer on the critical path**.
What it could still decide is open question 2(b): *at non-additive instances and with an
interacting known part, is the black-box bound equal to the value of the single-letter
game, or do unions and box-centred perturbations move the exponent?*

## Request (only if cheaper investigations are done)

For small instances — `k`-state sites with `k ∈ {2, 3}`, `n ≤ 8–10` sites, known parts that are
(i) additive, (ii) a nearest-neighbour chain, (iii) random pairwise; weighted Hamming
envelope; zero and non-zero residuals; `β ∈ {0.5, 1, 4}` and three accuracies — compute

    τ*(ε)  =  min { Σ_x q(x) :  q ≥ 0,  q(S) ≥ 1 for every sensitive set S }

exactly, by column generation: the pricing problem "find an admissible perturbation with
`|Δ ln Z| > ε` whose difference set has the least `q`-mass" is a concave maximisation over the
Lipschitz polytope and can be attacked by enumeration of difference sets for these sizes.
Compare with the values obtained from single dips, from generalised dips
(`genDip_expected_queries_ge`) and from the game formula of Theorem 11.27.

## Expected outputs

For each instance: `τ*`, the three comparison values, and the support structure of an
optimal dual solution (which sensitive sets are tight).

## Resource requirements and runtime

The number of candidate difference sets is doubly exponential in `n` in principle; with
symmetry (cube, identical sites) and column generation `n ≤ 8` should be feasible in
CPU-hours.  Stop where it is not.

## Suggested validation protocol

On the cube at the zero residual the exact value must equal the hinted bound of Theorem
11.25(a) (`2ⁿ/|B(n, k*)|` up to rounding); on the uniform metric it must equal the value of
harness XII.2.

## Stopping conditions

A budget of a few tens of CPU-hours; no extension without a specific question.

## What the possible outcomes would mean

Equality with the game value on all instances: evidence that the single-letter formula is
the truth beyond additive instances, worth a theorem.  A gap that grows with `n`: the
known lower-bound technique is not sharp for interacting known parts, and the structure
of the tight sets would say what perturbation family is missing.

## Assumptions and limitations

Tiny sizes; exponents cannot be read off, only whether the families agree.

## Requested response

Optional.  A decline ("not worth the compute now") would be a reasonable answer.
