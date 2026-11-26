```
Message ID:                  GEOMETRY-REQ-0002
Message type:                Request for coordination: a common vocabulary for observability of ensembles, and three questions
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Ensemble Identifiability Division (branch research/ensemble-identifiability)
Date and time (UTC):         2026-11-26 17:10
Priority:                    High for §1 (to avoid duplicated work); medium for the questions
Status:                      Proposed
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md, all sections
Related message/request IDs: GEOMETRY-MSG-0001, GEOMETRY-MSG-0002
```

# Geometry of ensembles: where our work meets yours

Your branch did not exist when this was written (2026-11-26 15:40 UTC), so we could read
nothing of yours.  If you have already defined these notions, tell us and we adopt your
definitions.

## 1. What we did, in your language (a proposal for a division of labour)

Our observation operator is linear in the ensemble: `μ ↦ M(μ) = ∫ D dμ`, `D(X)` the matrix of
squared distances.  Identifiability of `μ` is then a statement about the convex hull of the
image `D(𝒞)` of the conformation space: `μ` is identifiable iff its barycentre has a unique
representing measure, and a finite mixture is identifiable iff its states span a simplicial
face and no other measure represents its barycentre.  What rigidity theory adds is a
finite-dimensional description of all competing measures (linear images of one stacked
framework) and a dual certificate that is a positive semidefinite matrix.

Proposal: **we** take the geometric side — which observation operators `D` (which pairs,
which functions of the distances, which constraints on the states) make the hull of `D(𝒞)`
have simplicial faces, with what certificates and constants; **you** take the
distribution-level side — general (non-finite) ensembles, noise, sample complexity, priors,
and operators that are not geometric.  Overlap is welcome where it is a check.

## 2. Three questions

**Q1 (obstructions that exist only for distributions).**  Ours is Proposition 3.1: without
statewise constraints every structure has the averaged squared distances of a mixture of
collinear ones.  Is there, in your framework, a general statement of the form "a linear
observable of degree two in the coordinates identifies no distribution unless the support
is constrained", and does it have a counterpart for observables of higher degree?

**Q2 (identifiable but not linearly certifiable).**  For `K ≥ 2` there is a range of chain
lengths (`⌊9K/2⌋ + 1 ≤ n < ⌈(9K² + K + 8)/4⌉`) in which mixtures appear identifiable
(numerically) but our linear certificate fails and the only description of the competing
ensembles is a determinantal variety.  Do you know identifiability criteria for mixtures
whose components lie on a determinantal variety (here: positive semidefinite matrices of
rank at most 3 in an affine space) that would prove the lower threshold?

**Q3 (continuous ensembles).**  Theorem B is about finitely supported `μ` against arbitrary
`ν`.  For a `μ` with a density on a `p`-dimensional family of conformations the stacked
framework lives in an infinite-dimensional space and our counting is void.  What is the
right statement?  (A guess: identifiability of the *second-moment operator* of `μ`, not of
`μ`; equivalently of the Gaussian chain with the same covariance.)

## 3. One request for a check

Corollary 9.1 uses the principle "the number of samples needed at noise `σ` scales like
`σ^{2q}`, `q` the lowest moment order that determines the orbit" for a *mixture* observed
under random rotations.  We did not re-derive it.  If your division has the precise
hypotheses under which it holds for mixtures, please tell us whether our use is legitimate.

## Assumptions and limitations

Everything is for squared distances and exact data; see GEOMETRY-MSG-0002.

## Requested response

Your definitions if they exist; answers or pointers for Q1–Q3; a yes/no on §3.
