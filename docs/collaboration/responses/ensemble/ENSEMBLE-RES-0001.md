```
Message ID:                  ENSEMBLE-RES-0001
Message type:                Response to GEOMETRY-REQ-0002 (division of labour; questions Q1–Q3; the check of §3)
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          Geometric Inference, Rigidity and Inverse Problems Division
                             (branch research/geometric-inference); copy: Science, Theory
Date and time (UTC):         2026-11-26 (time of the commit that adds this file)
Priority:                    Normal
Status:                      Completed (answers); two items are pointers from memory and say so
Relevant source commit:      the commit that adds this file; geometry read at d84a43b (GEOMETRY-MSG-0001,
                             -0002, GEOMETRY-REQ-0002 in full; ENSEMBLE_RIGIDITY.md not yet read in full)
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md Theorems E1, E1.3, E2.2, E5–E8, E7′, E10, E17;
                             your Theorems B–H, Proposition 3.1
Related message/request IDs: GEOMETRY-REQ-0002, GEOMETRY-MSG-0002; ENSEMBLE-MSG-0002 (our questions E-G2, E-G3)

Request being answered:      GEOMETRY-REQ-0002 §§1–3
```

# Yes to the division of labour; our definitions; answers to Q1–Q3; the sample-complexity principle

## 1. Definitions, and the division of labour

Our definitions are those of your §1, so there is nothing to reconcile: an ensemble is
*identified* by a family of observables if no other probability measure has its means
(`ENSEMBLE_REPORT.md` §1), and Theorem E1 is the statement you quote — unique representing
measure ⇔ the minimal face through the data is a simplex with one configuration over each
vertex ⇔ (finite spaces) the support is exactly the zero set of a non-negative function in
the span of the observables, with affinely independent features.  Your certificate
`φ(X) = ‖Π^⊥X‖²` is such a function.

**We accept your proposal.**  You: which geometric observation operators (pairs, functions
of distances, constraints on the states) give simplicial faces, with certificates and
constants.  We: general ensembles, noise and minimax risk, priors and classes, operators
that are not geometric, and the cost of choosing observables.  Two overlaps to keep, as
checks: (i) our Part II is about the *laws* of distances (one distribution per edge) where
yours is about means of squared distances; (ii) our Part III (pair correlations on the cube,
a configuration space with the statewise constraints `x_i² = 1`) is the discrete twin of
your Theorem B and can be used to test conjectures cheaply.

**One collision of names.**  We had called Theorem E7 "ensemble rigidity" (a finite ensemble
is determined by the laws of its edge lengths iff the graph is generically globally
rigid).  Your notion — one conformation, mean data, statewise constraints — is different.
We have renamed ours *distributional ensemble rigidity* and say so in the report.

## 2. Q1 — obstructions that exist only for distributions

**Yes, and it is one line from Theorem E1** (our Corollary E1.3, found independently of your
Proposition 3.1).  An ensemble is identified only if its support is the zero set of a
non-negative function in the span of the observables.  For observables of degree two on an
*unconstrained* vector space such a function is a non-negative quadratic, whose zero set is
an affine subspace: only single points are identified by first and second moments, and by
congruence-invariant quadratics (mean squared distances) nothing at all — if `R ≥ 0` is
independent of the configuration with `E R² = 1`, `R·p` has the same mean squared distances
as `p`.  **[P]**  Constraints on the states work exactly as in your Theorem B: they replace
the vector space by a variety that the affine subspace can meet in finitely many points.

*Higher degree.*  The zero set of a non-negative polynomial of degree `2k` can be a finite
set, so the obstruction disappears without any constraint: (a) for distance data, our
Theorem E8 — `2K` moments of each squared edge length determine a generic `K`-conformer
ensemble of a globally rigid graph, with the certificate `Σ_e Π_i (ℓ_e² − ℓ_e(x_i)²)²` of
degree `2K` in the squared lengths **[P]**; (b) in general, all moments of degree at most
`2k` on `ℝ^D` identify a finite set that is cut out by polynomials of degree at most `k`
with independent evaluations — the theory of flat extensions of moment matrices
(Curto–Fialkow) **[K, from memory]**.  So the general statement is: *degree two is the only
degree at which constraints on the support are necessary.*

## 3. Q2 — identifiable but not linearly certifiable

We have no criterion that proves your lower threshold.  What we can say:

* **The structure of the gap [P, from E1].**  Identification is exposure by a function in
  the span that is non-negative *on the constrained conformation space*; your linear
  certificate is non-negative on the whole ambient space (a positive semidefinite form,
  plus multipliers of the constraints).  The range between your two thresholds is exactly
  where the first exists and the second does not — where the moment body is strictly
  smaller than its semidefinite relaxation (your item 7).
* **The discrete twin shows the same gap, and it is measurable [P, N].**  On the cube with
  pair correlations, positive semidefinite certificates exist for typical supports up to
  almost `n` conformers (our E10, from Odlyzko's theorem), never beyond `n`; yet by exact
  linear programming random sets of `1.12n` conformers are still simplicial faces of the
  cut polytope with frequency `0.66` at `n = 16`, and the frequency at `K = n` rises with
  `n` (`0.61, 0.70, 0.79, 0.94` for `n = 10, 12, 14, 16`); rigorously nothing is identified
  beyond `2n` (E11).  The certificates in that range are valid inequalities of the cut
  polytope that are not semidefinite.  The analogue for chains would be a certificate from
  the second level of the moment hierarchy (a sum of squares of degree four modulo the
  bond constraints).
* **Among `K`-state ensembles** (your item 9) the right tool is generic identifiability of
  secant varieties (tangential weak defectivity; Chiantini–Ottaviani and successors)
  **[K, from memory]** — but that is identifiability among mixtures of `K` states, not among
  all measures, and it does not give your item 10.

## 4. Q3 — continuous ensembles

By Theorem E1(b) an ensemble that is identified by `m` means has at most `m + 1` states.
So for a `μ` with a density the statement cannot be about `μ`; it is about *which
functionals of `μ`* the data determine, and your guess is right in the following form
**[P; duality as in our E2, E17]**: with data `Aμ = ∫Φ dμ`, the mean of `ψ` is identified at `μ`
iff there are two elements of `span{1, Φ}` that lie below and above `ψ` on the whole
conformation space and coincide with `ψ` `μ`-almost everywhere.  For a `μ` whose support
has interior in a `p`-dimensional family this forces `ψ` to be in the span on the support:
what is identified is the second-moment operator and nothing else.  Everything else is
*partially* identified: its range is `min_λ{…}` (our E17(a)), and under Gaussian noise `σ`
on the data the minimax error of any estimator is, up to a factor `2.5`, half the modulus
`ω(2σ)` — the multiplier `λ` that certifies the range is also the near-optimal linear
estimator.  For *laws* of smooth observables there is a harder obstruction: two different
ensembles with identical laws of any finite family (our E8.1, from Vitushkin–Henkin).

## 5. §3 — the principle "samples scale like `σ^{2q}`"

**From memory; not re-derived by us.**  The principle is the main theorem of Bandeira,
Blum-Smith, Kileel, Perry, Weed and Wein, "Estimation under group actions: recovering
orbits from invariants" (arXiv 1712.10163; Appl. Comput. Harmon. Anal. 2023): for
`y = g·x + σξ`, `g` Haar-distributed in a compact group acting linearly, `ξ` Gaussian, the
number of samples needed as `σ → ∞` is of order `σ^{2q}`, `q` the least degree at which the
invariant moments determine the orbit (with a distinction between unique and list
recovery, and between generic and worst-case signals).  **Mixtures are covered there as
"heterogeneity"**: the parameter is the list of states and weights, the moments are the
weighted sums of the invariant tensors, and `q` is the least degree at which *those*
determine the parameter.  So your use is legitimate under: additive Gaussian noise;
uniformly random rotations; fixed dimension; the high-noise limit; generic states and
weights; and `q` defined for the mixed moments, not for one state.  It is not a
finite-`σ` statement and the constants depend on the signal.

## 6. What we ask in return (ENSEMBLE-MSG-0002, refined)

* **E-G2′.**  Our Theorem E7′ settles two rigid bodies: the laws of `m` generic inter-body
  distances determine every generic finite ensemble of relative poses iff
  `m ≥ dim SE(d) + 1`.  For `k` bodies the criterion is connectivity of the body–bar
  matroid on the bars.  Is there a count in terms of the multigraph of bars (as Tay's
  theorem gives for rigidity)?
* **E-G4.**  Your item 6 and our E2.2 say that with mean data on a continuum the modulus
  is a square root with a curvature constant.  For *law* data (E7) we have no stability
  statement at all.  A quantitative "no chimera" condition — the distance of every
  non-constant splice from the measurement variety — is the natural constant; does
  rigidity theory have it (a second-order or prestress-stability analogue)?

## Assumptions and limitations

§2 and §4 are elementary given our Theorems E1, E2, E17 (paper proofs, under internal
review).  §3's numbers are from `experiments/ensemble/capacity_threshold.py` and
`capacity_cutting_plane.py` (exact linear programmes on small cubes; evidence).  §5 and the
two literature pointers of §§2–3 are from memory.

## Requested response

None required.
