# MetricChain

Theory and certificate kernels for fixed-sequence articulated chain molecules: certified
conformational energy minimisation, certified partition functions, realizability and geometric
stability.  The theorems marked **[V]** in the theory report — including the soundness theorems
of the three certificate kernels — are machine-checked in Lean 4 + Mathlib; statements marked
**[P]** (paper proof) or **[K]** (cited) are not, and the report says which is which.

Scope: mathematics, statistical physics, general-purpose certified computation and synthetic
evaluation only.

## Where to start

| you want | read |
|---|---|
| the results, proofs, and an honest known-vs-new table | [`docs/THEORY_REPORT.md`](docs/THEORY_REPORT.md) |
| to implement the checkers / solvers | [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md) |
| how the program evolved and what is open | [`docs/RESEARCH_LOG.md`](docs/RESEARCH_LOG.md) |
| what turned out false, weaker, or already known | [`docs/DEAD_ENDS.md`](docs/DEAD_ENDS.md) |
| the literature checks behind the novelty assessments | [`docs/prior_art/`](docs/prior_art) |
| the independent referee reports on the theory report (six so far; a seventh, on §11.18, in progress) | [`docs/reviews/R1_referee_report.md`](docs/reviews/R1_referee_report.md), [`R2`](docs/reviews/R2_referee_report.md), [`R3`](docs/reviews/R3_referee_report.md), [`R4`](docs/reviews/R4_referee_report.md), [`R5`](docs/reviews/R5_referee_report.md), [`R6`](docs/reviews/R6_referee_report.md) |
| the independent reviews of the workstream reports | [`docs/reviews/`](docs/reviews) (`R_B_review.md`, `R_C_review.md`, `R_D_review.md`, `R_E_review.md`, `R_G_review.md`, `R_P_review.md`) |
| collaboration with the Computational Research Division (branch `research/ubuntu-engineering`): protocol, status, messages and computational requests | [`docs/collaboration/`](docs/collaboration/README.md), digest in [`THEORY_TO_ENGINEERING.md`](docs/collaboration/THEORY_TO_ENGINEERING.md) |
| reports of independent exploratory workstreams (as delivered; not part of the theory report unless it says so) | [`docs/workstreams/`](docs/workstreams) |

## Layout

```
lakefile.lean, lean-toolchain, lake-manifest.json   Lean 4.31.0 + Mathlib v4.31.0 (pinned)
proofs/Core/            partition-function vocabulary; outward rounding, rational intervals,
                        certified exp, rational atlas of the circle
proofs/Frontiers/       envelope duality, dominance calculus, free-energy sandwich, Hölder
                        decomposition, partition-function kernel, voxel enclosures and the
                        voxel bridge, Hoffman–Wielandt, realizability, holonomy,
                        torsion-to-RMSD, invariant-residual envelopes,
                        proof complexity of certificates;
                        second phase: certification geometry (slack coverings, certificate
                        notions, conditional envelope, complexity on product landscapes,
                        exponential-weights converses, product rates, best-first search,
                        thermal robustness), second- and higher-order envelopes, the sampled
                        free-energy sandwich, the partition kernel with cut and elimination
                        rules, the lemmas of the second referee, query-complexity bounds
                        for every algorithm, deterministic or randomised, two-sided
                        soft-gap bounds for randomised free-energy estimation, the
                        refinements after the third referee report (pair detection, hedged
                        spot-check, exact-dip bounds on the cube), generalised dips with
                        the two-measure sandwich (thresholds beyond the cube), the normal
                        form that absorbs the known part into the envelope, the
                        second-order dip (dense second-order classes), and the residual-
                        independence of the soft-gap sampler's constant
proofs/CertificateAlgebra.lean   executable verification kernels + Master Soundness Theorems
proofs/AuditCommand.lean         the axiom walk (by defining module)
proofs/AxiomAudit.lean           axiom audit of every project constant + non-vacuity witnesses
experiments/            adversarial counterexample harness and its mutation tests, separation
                        benchmarks, reference JSON certificate checker + conformance
                        vectors (certs/)
scripts/audit_all.sh    single-command audit (begins with a self-test on planted violations)
```

## Reproducing the audit

```bash
scripts/audit_all.sh          # self-test, lake build, token scan, axiom audit, harness + mutation
                              # tests, benchmarks, reference checker, doc refs
scripts/audit_all.sh --full   # same with the long falsification pass
```

Requirements: the pinned Lean toolchain (via `elan`, or the release archive unpacked in
`~/.lean/`; see `scripts/lean_env.sh`), `lake exe cache get` for the Mathlib cache, and Python 3
with `numpy`, `scipy`, `mpmath`.

The audit fails if any file under `proofs/` contains `sorry`/`admit`/native evaluation/an
anonymous `example` or produces Lean's incomplete-proof warning, if a module is not imported by
the axiom audit, if any constant defined in a project module — whatever its namespace or
visibility, the non-vacuity witnesses included — depends on an axiom other than `propext`,
`Classical.choice`, `Quot.sound`, if a registered conjecture is
falsified (or a documented dead end unexpectedly survives), if a mutation of the harness goes
undetected, if the stored conformance vectors differ from the reference checker's, or if the
documentation cites a Lean declaration that does not exist.  The script first checks itself:
planted violations must be detected.

## Status

**Kernels.**  Three verified certificate kernels with exact rational arithmetic — lower bounds
on minimum energies (reparameterisation bounds, branching, dead-end elimination, dual
decomposition), the same under an unknown non-decomposable residual known only through an
envelope and evaluated anchors, and two-sided bounds on partition functions (factorised leaves,
branching, thermal dead-end elimination, and — since the second phase — cut and elimination
rules: exact on every chain (machine-checked) and on tree and ring instances, and by a paper
argument on interaction graphs of treewidth at most two), with voxel enclosures of continuous
integrals.

**Theory, first phase.**  Exact characterisations of robust optimality under an envelope
(contact-set, sharp-minimum and query-model theorems), the necessity of decomposition rules
(exponential separations), sharp free-energy sandwiches for product references, torsion-to-RMSD
certificates.  An independent referee report (`docs/reviews/`) found no machine-checked statement
false but classified this mathematics as elementary or classical in substance, and four prose
claims as overstated; the corrections are in the report and in `docs/DEAD_ENDS.md` (D21–D27).

**Theory, second phase (theory report §§10–12).**  *What can residual evaluations certify, and
at what cost?*  Certificates are coverings in a slack quasi-metric with radii equal to the
points' own optimality gaps.  The size of the smallest one equals, instance by instance, the
number of evaluations of the best deterministic algorithm that is correct on the whole class
*and may be tailored to that instance*; no single algorithm achieves it on all instances.  With
only a first-order envelope, on product landscapes one evaluation suffices iff every site is
sharp; otherwise the number is exponential in the number of non-sharp sites, with an exact
exponent (a rate–distortion function).  At finite temperature, for accuracies that are neither
extensive nor exponentially small, the same formula holds with the energy gap replaced by the
free-energy gap of a macrostate (a corollary of a known source-coding theorem on exponential
moments of distortion), and the count is at least the exponential of the entropy.  These bounds
hold for every algorithm (formally: every finite mixture of deterministic query algorithms).
At zero temperature randomisation gains at most a factor `1 − 2δ` against each fractional
(LP-dual) covering bound, and a hedged spot-check of a hint attains these bounds up to
`ln(1/δ)`: randomisation is worth the integrality gap and no more.  For free energies it
provably lowers the exponent — machine-checked at the zero residual of the cube, with the
instance as a hint: about `(2/(1+e^{−βc}))ⁿ` random evaluations against almost `2ⁿ` deterministic
ones — but not to zero: every algorithm must reach within a *soft-gap* radius of every state,
and the same soft gaps bound the randomised cost from above.  On the uniform cube class the
accuracy `n ln cosh(βc/2)` is a sharp threshold for the worst case over instances: above it a
bounded number of random evaluations suffices on every instance, below it every algorithm
needs exponentially many on the zero residual, where the exponent is now determined in every
accuracy regime, down to exponentially small accuracies (lower bounds machine-checked; upper
bounds by Harper's theorem).  Beyond the cube, every slack-Lipschitz function is the centre of
a perturbation that must be detected (generalised dips; single dips are not enough when sites
have three or more states), every additive instance of a product landscape has a sharp
accuracy threshold — the value of a single-site game with a second reference measure — and the
threshold of the whole class, for algorithms that are given nothing, is the smallest
oscillation of a tilted site pressure, for every alphabet (for two-state sites: the largest
chord gap of the pressure).  The lower bounds and both tensorisations are machine-checked;
the rest are paper proofs, among them the matching upper bound of the exponent below the
threshold, which an independent referee checked.  A known part turns out to be nothing but the
gradient part of an asymmetric envelope (normal form, machine-checked).  Second-order
structure does not rescue certification when its constants are dense: the uncertainty left by
any set of evaluations grows quadratically with the distance to it (machine-checked), so the
price is exponential unless the excitation energies are of the order of `c·n`.
Minimal certificates are NP-hard to find and best-first search is
competitive only with covers at shrunk radii.  Under weak second-order coupling, `n(k−1)+1`
evaluations give an exact reduction to the pairwise kernel.  The one-shot lower bounds (for
certificates and for all algorithms), the search guarantee and the second-order reduction are
machine-checked; the matching upper bounds are paper proofs (type covering, Harper's theorem),
for which the single-letter identities and exact counts were checked numerically.

**Independent review.**  The second referee found one paper theorem false as stated and four
overstatements (`docs/DEAD_ENDS.md` D29–D33) and judged the cluster "a coherent note, not a
theorem-driven paper"; the tools are standard and the proofs short.  The third referee, on the
query-complexity section, found no machine-checked statement false, the same error a second
time (an exponent claimed for all accuracies `ε = o(n)` that fails for exponentially small
ones), a converse that was not tight, and four statements of scope that were too wide
(D35–D37); all are corrected, and the verdict stands.  Independent workstreams then refuted
the conjecture this README's previous version relied on for finite-temperature exponents
beyond the cube — single dips are not the extremal perturbations on product landscapes with
three or more states per site (D38) — and supplied what replaces it (theory report Theorems
11.27–11.28).  Every workstream report was then reviewed independently (`docs/reviews/`): no
headline theorem was found false, several summaries were found stronger than their theorems,
and what has been integrated — the exact exponent beyond the cube, the normal form, dense
second-order classes, second-order classes at finite temperature, the torus of angles,
Boltzmann averages, chains as known parts, and what the theory predicts for chain geometry
(theory report §§11.10–11.15) — is integrated with the reviewers' scope; one conjecture of a
workstream was refuted by its reviewer (D41).  The finding with the most direct consequence
for the original goal is negative: the verified per-torsion constants grow with the distance
to the chain end, so the weighted-Hamming route cannot certify long chains (D42).  §12 of the
report says what a publication would still need.

**Cycle 10 (refereed: `docs/reviews/R5_referee_report.md`, `R6_referee_report.md`; the
workstream on chains reviewed in `R_P_review.md`; the third addition is under review).**  Three
additions, theory report §§11.16–11.18; no referee found a false theorem in the first two,
all found sentences that said more than was proved and some numbers that said less
(`docs/DEAD_ENDS.md` D43, D44), and the text below is the corrected one.  (i) *Without a hint on the cube.*  For every member of the class, the Gibbs
mass above a threshold `t` satisfies `E(w − t)₊ ≤ t(e^{Δ_r} − 1)`, the excess of a dip on a ball of
the size of the super-level set, and the mass below it is at least that of a cone around
such a ball (tail lemmas: the pointwise and summed inequalities are machine-checked, their
comparison with Hamming balls is a paper reduction to Harper's theorem).  Hence plain Monte
Carlo is accurate on the whole class with the exponent `min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` at
extensive accuracies and `KL(p_u‖½)` at every fixed accuracy, and no non-adaptive algorithm has
a smaller exponent (the lower bound is machine-checked given two finite sums; its method is
that of Mathé–Novak 2007).  Two independent samples give a certified bracket that needs no
hint at the zero residual for accuracies above 2.  An adaptive algorithm that is correct on
the class needs only `n + 3` evaluations on a cone, the hard instance of non-adaptive ones;
adaptive algorithms are the subject of (iii).  (ii) *Correlated uncertainty.*  A residual that is linear in known features with
coefficients in a box is determined by rank-many evaluations; every linear combination of
evaluations brackets the value at a new point by the part of its feature vector that the
evaluated ones do not explain — in the worst case over the data the weighted `ℓ¹` distance to
their *span*, where the first-order class of the same envelope has the distance to the
nearest one (machine-checked; exactness is linear-programming duality, and the mathematics
is classical optimal recovery).  Pair-additive residuals with unknown Lipschitz radial
functions are of this kind, with the cumulative pair-count profiles as features; their
envelope is a transport distance between pair-distance distributions, sharpness in this
format is stochastic dominance of profiles, and a small verified kernel certifies minima for
every coefficient vector that is consistent with evaluated anchors.  At an extensive accuracy
certificates in the profile format exist whose number of evaluations does not depend on the
chain length — a partial answer to D42, for a class of residuals that is much smaller than
the one D42 was about (functionals of pair-distance statistics; no chirality, no
sequence-specific terms), with an existence bound that is numerically vacuous, and with a
remainder outside the class costing an accuracy floor if it is bounded in the supremum norm
and the old exponential price if it is only bounded in a per-torsion first-order envelope.
(iii) *Adaptivity replaces the hint* (theory report §11.18; **independent review in progress
at this checkpoint — until it is integrated, treat the paper proofs of this item as
unrefereed**).  On the cube
class, adaptive randomised algorithms without a hint have, in the worst case, exactly the
exponent `KL((Λ₁+ε₁)/u ‖ ½)` that Theorem 11.25 gives for algorithms with a hint, while
non-adaptive ones have the larger exponent of (i): at the exponential scale a hint is worth
nothing to an adaptive algorithm.  The upper bound is a nested "layer-cake" algorithm (an
independent workstream's): a uniform sample of an outer block of coordinates, brackets of
the fibre averages refined only as far as a one-sided test against a ladder of levels
requires, and the tail lemma once at the top.  One level maps an exponent function `T` to
`R[T]`; by the identity `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁` the hinted exponent is a fixed point of
`R`, and every other solution of `T ≤ R[T]` lies below it, so the iteration from the
non-adaptive exponent converges to it (machine-checked for an abstract pair of exponent
functions, together with the validity and the width of the bracket; the count of
evaluations of the algorithm is a paper proof).  This is a statement about exponents: at
the sizes that can be simulated the algorithm is worse than plain Monte Carlo, and five
wrong accountings and one gap in the algorithm preceded the proof (`docs/DEAD_ENDS.md` D45).

What is *not* established: the guarantees are relative to published inputs (rational tables,
envelope constants, anchor values); certifying envelope constants for a concrete learned residual,
interval evaluation of force-field terms over voxels, and any claim of practical solver
performance are outside the development.
