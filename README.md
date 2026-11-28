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
| **Phase II (28 November 2026, branch `research/phase2-foundations`): what observational information is worth to a certified free energy** — noisy means of arbitrary observables cost at most a factor `τ^{−2} ln M` (both exponents unchanged until the precision or the logarithm of the number of observables is exponential), exact means cost at most the size of their Walsh spectrum, the law of a block of `θn` sites gives exactly `(1 − θ)h`, samples at least a birthday bound; machine-checked cores; the review R29 resolved | final report [`docs/phase2/FINAL_REPORT.md`](docs/phase2/FINAL_REPORT.md); [`docs/phase2/PHASE2_REPORT.md`](docs/phase2/PHASE2_REPORT.md), manuscript [`docs/phase2/MANUSCRIPT.md`](docs/phase2/MANUSCRIPT.md), [`docs/phase2/R29_RESOLUTION.md`](docs/phase2/R29_RESOLUTION.md), `proofs/Frontiers/ObservationInvariance.lean` |
| **the critical assessment at the consolidation halt of 27 November 2026** — what is established, what is conjectural or unrefereed, the strongest contributions with the evidence for and against their originality, negative results, what to do next | [`docs/collaboration/consolidation/theory.md`](docs/collaboration/consolidation/theory.md) |
| the results, proofs, and an honest known-vs-new table | [`docs/THEORY_REPORT.md`](docs/THEORY_REPORT.md) |
| to implement the checkers / solvers | [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md) |
| how the program evolved and what is open | [`docs/RESEARCH_LOG.md`](docs/RESEARCH_LOG.md) |
| what turned out false, weaker, or already known | [`docs/DEAD_ENDS.md`](docs/DEAD_ENDS.md) |
| which assumption of which theorem is essential, an artefact of the proof, or a convenience; the hierarchy from the most tractable model outwards; statements whose guarantees are computationally vacuous | [`docs/ASSUMPTION_AUDIT.md`](docs/ASSUMPTION_AUDIT.md) (synthesis), [`docs/audit/`](docs/audit) (theorem by theorem; the record of the 61 corrections it led to) |
| the literature checks behind the novelty assessments | [`docs/prior_art/`](docs/prior_art) |
| the independent referee reports on the theory report (twelve so far) | [`docs/reviews/R1_referee_report.md`](docs/reviews/R1_referee_report.md), [`R2`](docs/reviews/R2_referee_report.md), [`R3`](docs/reviews/R3_referee_report.md), [`R4`](docs/reviews/R4_referee_report.md), [`R5`](docs/reviews/R5_referee_report.md), [`R6`](docs/reviews/R6_referee_report.md), [`R7`](docs/reviews/R7_referee_report.md), [`R8`](docs/reviews/R8_referee_report.md), [`R9`](docs/reviews/R9_referee_report.md), [`R10`](docs/reviews/R10_referee_report.md), [`R11`](docs/reviews/R11_referee_report.md), [`R12`](docs/reviews/R12_referee_report.md) |
| the independent reviews of the workstream reports | [`docs/reviews/`](docs/reviews) (`R_B_review.md`, `R_C_review.md`, `R_D_review.md`, `R_E_review.md`, `R_G_review.md`, `R_P_review.md`) |
| collaboration between eight research divisions on eight branches — this one (theory), the Computational Research Division (`research/ubuntu-engineering`), the Scientific Discovery, Translation & Independent Validation Division (`research/scientific-translation`), and, since 26 November 2026, Ensemble Identifiability and Certified Inference (`research/ensemble-identifiability`), Geometric Inference, Rigidity and Inverse Problems (`research/geometric-inference`) and Mathematical Biology and Computational Complexity (`research/biological-complexity`), and, authorised on 26 November 2026 at night, Structural & Computational Biology, Software Development and Applications (`research/structural-biology`; our orientation for it: THY-MSG-0020) and Frontier Benchmarking, Experimental Evidence and Scientific Evaluation (`research/frontier-benchmarks`); the other branches are read-only from here and are never merged: protocol, status, messages, requests and responses | [`docs/collaboration/`](docs/collaboration/README.md), digest in [`THEORY_TO_ENGINEERING.md`](docs/collaboration/THEORY_TO_ENGINEERING.md), state in [`status/theory.md`](docs/collaboration/status/theory.md) |
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
                        second-order dip (dense second-order classes), the residual-
                        independence of the soft-gap sampler's constant; cycle 10:
                        algorithms without a hint (non-adaptive lower bounds, the level
                        recursion of adaptive algorithms and its convergence — for the
                        cube and for every game function — the algebra of the two-level
                        brackets), the shift identity with a field, residual classes that
                        are linear in features and the profile kernel, and the abstract
                        limit theorems behind the limit shape of chains (Fekete's lemma
                        for sets; stability of covering numbers)
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
integrals.  What distinguishes the second kernel from proof logging as practised (one
certificate, one instance) is its quantifier: an accepted certificate bounds the energy for
*every* residual of the class, and the kernel itself checks that the class is not empty.  For
the first kernel the ingredients have verified checkers in the pseudo-Boolean setting, and
whether the native format is cheaper has not been measured (theory report §6.4, rewritten
after the Scientific Discovery Division's review of prior art, SCI-REV-0006).

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
only a first-order envelope, on product landscapes (independent sites of finitely many types
that are fixed as the system grows, and an additive residual that stays strictly inside the
envelope) one evaluation suffices iff every site is
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
threshold, which an independent referee checked.  For minima and their certificates — not for
free energies — a known part turns out to be nothing but the
gradient part of an asymmetric envelope (normal form, machine-checked).  Second-order
structure does not rescue certification when its constants are dense: around a residual
whose second differences vanish, the uncertainty left by any set of evaluations grows
quadratically with the distance to it (machine-checked), so the price is exponential unless
the excitation energies are of the order of `c·n` (for a residual with second differences
up to `κc`, `κ < 1`, the same with the constants `(1 ∓ κ)c`; at a residual on the boundary of
the class it fails — theory report, the remark after Theorem 11.32).
The exponential price is a property of the *class*, not of a certificate format and not
of worst-case reasoning as such: every instance has its own lower bound, which holds for
every procedure that is correct on the first-order class, so no such procedure can be cheap
at an instance whose own bound is large, in whatever subclass that instance lies (the bound
can be small: one evaluation for the minimum at a sharp instance, two at a cone given as a
hint, and a
class-correct procedure costs `n + 3` on every cone — theory report, Theorem 11.45(d)), and a
paradigm that is cheaper there must say which members it gives up.  Two classes with other geometry are
treated next to it — a Hilbert ball, in which evaluations combine linearly (the
hypercircle band, machine-checked: `HilbertBall.lean`; proposed by the Scientific
Discovery Division), and a box around a known part that can be sampled (below).
Minimal certificates are NP-hard to find and best-first search is
competitive only with covers at shrunk radii.  Under weak second-order coupling, `n(k−1)+1`
evaluations give an exact reduction to the pairwise kernel; *when* the coupling is weak
enough is now an exact, cheaply checked condition for independent known parts — the
pair constants must be splittable between their two sites so that no site carries more
than its excitation energy (a maximum-flow certificate; the older "row-sum" rule is the
split in halves; machine-checked in the sound direction, `ShareCertificates.lean`).  With
third-order constants the values on a Hamming ball of radius two give a pairwise lower
model that the same kernel certifies (`ThirdOrderModel.lean`), and — unlike the
second-order reduction — it does not depend on how the energy is divided between known
part and residual.  On domains with forbidden pairs of states these reductions hold on
the part of the domain that is closed under resetting sites to the reference, and
connectivity is not enough.  (The last three statements answer questions of the
Scientific Discovery Division, which measured such constants for a solvent term on
fixed synthetic model peptides; measured constants are not certified ones.)  The one-shot lower bounds (for
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
for the original goal is negative: the verified per-torsion constants are square roots of
moments of inertia of the lighter arm and therefore grow like the power 3/2 of the distance
to the chain end (per-joint lever-arm bounds of this kind are standard in robot motion
planning; new is the consequence), so the weighted-Hamming route cannot certify long chains
(proved at the zero residual of an additive known part on a product domain; D42).  §12 of the
report says what a publication would still need.

**Cycle 10 (refereed: `docs/reviews/R5_referee_report.md`, `R6_referee_report.md`,
`R7_referee_report.md`; the workstream on chains reviewed in `R_P_review.md`).**  Three
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
the number of evaluations of a certificate in the profile format is bounded independently of
the chain length — a partial answer to D42, for a class of residuals that is much smaller than
the one D42 was about (functionals of pair-distance statistics; no chirality, no
sequence-specific terms), with an existence bound that is numerically vacuous and a regime
that exact enumeration by the Computational Research Division does not reach (the smallest
certificates still grow at 27 beads on a lattice chain and grow geometrically off-lattice
through 15 beads; they are orders of magnitude smaller than per-torsion ones, not constant:
`docs/DEAD_ENDS.md` D46), and with a
remainder outside the class costing an accuracy floor if it is bounded in the supremum norm
and the old exponential price if it is only bounded in a per-torsion first-order envelope.
(iii) *Adaptivity replaces the hint* (theory report §11.18; refereed in
`docs/reviews/R7_referee_report.md`: "proved with gaps", the gaps — an abort rule, the induction
over levels, prior art — now written into the text; the referee found no error in the cost
accounting beyond one closure rule, which the harness had found as well).  On the cube
class, adaptive randomised algorithms without a hint have, in the worst case, exactly the
exponent `KL((Λ₁+ε₁)/u ‖ ½)` that Theorem 11.25 gives for algorithms with a hint, while
non-adaptive ones have the larger exponent of (i): at the exponential scale, in the worst
case over the cube class, a hint is worth
nothing to an adaptive algorithm (with a field the hinted exponent at the zero residual is
strictly below the worst case without a hint, (v)).
The upper bound is a nested "layer-cake" algorithm (an
independent workstream's): a uniform sample of an outer block of coordinates, brackets of
the fibre averages refined only as far as a one-sided test against a ladder of levels
requires, and the tail lemma once at the top.  One level maps an exponent function `T` to
`R[T]`; by the identity `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁` the hinted exponent is a fixed point of
`R`, and every other solution of `T ≤ R[T]` lies below it, so the iteration from the
non-adaptive exponent converges to it (machine-checked, abstractly and for the exponent
functions of the cube themselves, together with the validity and the width of the bracket;
the count of
evaluations of the algorithm is a paper proof, re-derived by the referee and supported by an
evaluation in expectation up to `n = 10⁶`).  This is a statement about exponents: at the sizes
that can be simulated the algorithm is worse than plain Monte Carlo, and five wrong
accountings and one gap in the algorithm preceded the proof (`docs/DEAD_ENDS.md` D45).  That
adaption can break an exponential barrier of non-adaptive methods is known for a
log-concave class (Mathé–Novak 2007); the exact exponent on this class and its coincidence
with the hinted one were not found in print.
(iv) *Every bounded accuracy* (theory report §11.19; workstream K, `docs/workstreams/K_REPORT.md`;
**a paper proof, refereed** — `docs/reviews/R8_referee_report.md`: "proved", no critical or major
finding, ten minor points corrected; the referee also ran three nested levels with real
inner brackets on small cubes and computed the exact three-level cost at the flat
instance).  The same holds
at every fixed accuracy and down to accuracies `e^{-o(n)}`: adaptive algorithms without a hint
have the exponent `h = KL(Λ₁/u ‖ ½)` of algorithms with a hint, non-adaptive ones the larger
`KL(p_u ‖ ½)`.  The two-level algorithm is modified so that a level costs an arbitrarily small
constant of accuracy instead of a factor `O(n)`: the lower end of the bracket is a layer-cake
sum, and the *lower* isoperimetric bound (Harper again) is used inside the closure test,
which is what certifies a bounded ratio where the outer sample is cheapest.  Machine-checked
(`BoundedAccuracy.lean`): the level recursion of (iii) defined in Lean, the facts that it never
undercuts and converges to the hinted exponent, the contraction at accuracy zero, and the
algebra of the bracket and of the count; simulated with the constants of the theorem without
a violation (scripts in `experiments/workstreams/K/`).  The coordinator's own sketch of this
step was wrong in its mechanism (D46).
(v) *With a known part* (theory report §11.20; workstream F, `docs/workstreams/F_REPORT.md`;
**paper proofs, refereed** — `docs/reviews/R9_referee_report.md`: no critical finding; the new
isoperimetric theorem and the non-adaptive exponent proved; the adaptive exponent proved
after two gaps in the written proof of the algorithmic part were closed, one of them a
real parameter change for strong fields).  The first step
beyond the uniform cube: a field as known part, i.e. a `p`-biased product reference measure.
The exponents are again single-letter, and "adaptive = hinted" persists in the form *the
worst case without a hint is the hardest case with a hint* — but three things that look
obvious on the uniform cube are false with a field (D47): the hardest instance is not the
zero residual but an additive residual that partly cancels the field; the right sample is
not the Gibbs measure of the known part but uniform on every type class (a flat histogram
in the magnetisation — plain Monte Carlo from the Gibbs measure is worse by up to a factor
2.9 in the exponent, by an elementary lower bound; the best single tilted product measure
is worse by 0.5–3 % in the examples computed, all at extensive accuracies — at bounded
accuracy a product measure with the right marginal, which is not the Gibbs measure's,
ties with the flat histogram in that lower bound, as the Scientific Discovery Division
pointed out: capacity equals information radius); and the isoperimetric input is not that of
a fixed product measure but a new asymptotic statement for a "flat-histogram" reference
instance, proved by the method of types.  For two-state sites a field always helps: every
exponent decreases
with the strength of the field (proved by the coordinator, refereed; with three or more
states it does not always help, (xi)).  Machine-checked: the
identity between the three rates (`FieldShift.lean`) and the convergence of the exact
recursion for any pair of exponent functions with the abstract properties; the central
formulas were re-computed by the coordinator and, independently, by the referee
(`experiments/coordinator_checks/`, `experiments/reviews/R9/`).  One half of it is not
specific to a field: for *every* known part that is a function of the order parameter
(mean-field models, with or without a phase transition) the flat-histogram sample is
optimal among fixed samples up to a polynomial factor, for every `n` — the truncation
lemma and the lower bound are machine-checked (`TypeQuantiles.lean`,
`SymmetricSampling.lean`), the matching upper bound is a paper proof; the exponents for
such known parts are item (viii).
(vi) *The common structure* (theory report §11.21; workstream M; the theorem about game
functions is machine-checked, the statements about algorithms are the paper proofs of (i),
(iii)–(v)).  In both
cases the non-adaptive curve is the hinted curve sheared by its own height — with a budget
of `e^{nθ}` evaluations a non-adaptive algorithm certifies an accuracy rate that is worse by
exactly `θ` — and the analytic core is one theorem about arbitrary game functions `F` on
`[0,1]`: the transform `R(e) = max_{t≤1}[F(t) − te]` and its sheared partner form a pair to
which the convergence theorem applies, and the exact level recursion converges to `R`
(`GamePair.lean`).  What a problem must supply beyond that — a lower bound of this form, a
reference instance with the matching isoperimetric exponent, and fibres — is listed there.
(vii) *Chains in the thermodynamic limit* (theory report §11.22; workstream S,
`docs/workstreams/S_REPORT.md`; **paper proofs with computer-assisted parts, checked by the
coordinator with independent code and reviewed by the Scientific Discovery Division —
SCI-REV-0002: no false theorem; the headline below reworded, the lower bound raised**).  The
Computational Research
Division measured that certificates in the profile format grow with the chain at every
size that can be enumerated and asked what the limit is.  For the lattice chain: the
normalised sets of (pair-count profile, number of gauche torsions) of *bridges* converge to
a compact convex **limit shape**, and their certificate sizes converge to a covering number
of it off a countable, unidentified set of accuracies.  In the three parts the review asked
for: **for every limit point of the certificate sizes of all walks at `(L, ε₁) = (1, ½)`:
between 116 and 3 627 [P, computer-assisted], where the earlier existence bound gave
`10^{1387}`**; that the sizes converge is proved for bridges off that set of accuracies and
is a conjecture for all walks [C]; our estimate of the limit is a few hundred and of the
chain length at which it is approached `10³`–`10⁵` beads or more [N, an estimate] — the shape
converges with a surface correction of exact order `N^{-1/3}` at its compact end, but no
theorem says when the certificate sizes are near their limit points.  (The first version
of this paragraph said "the plateau is between 50 and 3 627 evaluations … and it is reached
only at `10³`–`10⁵` beads".)  Bridges whose two ends are "clean" concatenate *exactly*, so the
limit shape is the convex body of an exact semigroup of lattice points (a classical
object; a question of the Scientific Discovery Division): in its interior the finite
sets fill in at rate `1/N`, and eventually every integer profile with an interior density
is attained by some bridge.  The
coordinator's brief for this workstream had the profile distance wrong (D48).  Machine-checked:
the two abstract theorems behind it — Fekete's lemma for sets and the stability of covering
numbers (`SetLimit.lean`, `CoverStability.lean`); the lattice lemmas that feed them are paper
proofs checked numerically.
(viii) *A known part with interactions: mean-field models* (theory report §11.23; workstream
T, `docs/workstreams/T_REPORT.md`; **paper proofs, re-derived in part and re-computed by the
coordinator with independent solvers; refereed (R10, `docs/reviews/R10_referee_report.md`): no
critical finding; two major and fifteen minor corrections, all applied — the claim that a
shallow barrier is invisible up to one explicit coupling for every slope was false at
large slopes, and an interval for one non-adaptive exponent had an unproved end**).  The
first known part that is not a product measure: a function of the order parameter, with
one phase or two.  By permutation symmetry alone, for every system size: the
flat-histogram ("multicanonical") sample is optimal among fixed samples up to a polynomial
factor, and the flat-histogram instance is the hardest instance among those that are
functions of the order parameter.  (The lower halves are machine-checked, and not only for
permutations: for any finite symmetry group with an invariant envelope, sampling
uniformly in every orbit cannot be beaten by a fixed sample by more than the number of
orbits — `GroupSampling.lean`.)  The exponents are again single-letter, for every rate
function, by the method of types applied inside a type class.  With one phase everything
of (v) carries over except the nested algorithm.  **With two phases the perturbations that
are hardest to exclude are shells of configurations in the barrier region — not cones
around a point, which miss the exponent by more than a factor two, and, beyond a small
accuracy, not even sets built around one centre: the extremal sets constrain only part of
the system** (found by the workstream against the coordinator's brief; D49).  A
ferromagnetic interaction of this mean-field kind never makes the problem harder than no
interaction (a ferromagnetic coupling along the chain can: item (xviii)), and a shallow
barrier can be invisible to the exponents: in zero field and at moderate slopes they equal
the uniform cube's up to a coupling beyond the critical one — proved as a local statement,
numerical beyond that, and at large slopes and small accuracies the junction comes earlier.
Open: what adaptive algorithms can do
(the nested algorithm does not transfer; see (x)), and the value of the exponent with two
phases beyond small accuracies.
(ix) *Rounds of adaptivity* (theory report §11.24; workstream U,
`docs/workstreams/U_REPORT.md`; **paper proofs, checked against the proof they build on and
re-computed by the coordinator; refereed by the Scientific Discovery Division with
independent code (SCI-REV-0003): no critical finding; one major correction — the cost
bound of the re-scheduled algorithm held on the good event only, and a stopping rule was
added — and nine minor ones, all applied**).  How much adaptivity does the adaptive
exponent need?  *Theorem (paper proof, on top of the refereed nested algorithms):* for
every `η > 0` a number of rounds that does not depend on the system size comes within `η` of
the adaptive exponent (the nested algorithms can be re-scheduled: a ladder with `L` rungs
is `L` rounds); whether a fixed number of rounds reaches it is open.  *Theorem (paper
proof):* two rounds already beat every fixed sample.  *Theorem (paper proof; the
indistinguishability lemma behind it machine-checked for two rounds and finite mixtures,
`TwoRounds.lean`; its application re-derived by the referee):* two rounds provably do
**not** reach the adaptive exponent — at every fixed accuracy, for randomised two-batch
algorithms that are correct on the whole Lipschitz class of the uniform cube,
asymptotically in the system size; and, by the referee's strengthening (machine-checked;
its file is now in this repository), already for the expected cost at one instance, the
flat histogram of a block of coordinates.  *Numbers (values of the proved formulas at
slope 1):* the two-round exponent is at least `0.359a` and at most `0.624a` — a `liminf` and a
`limsup`: the limit is not shown to exist — where a fixed sample costs `a` and full
adaptivity `0.263a` (item (iv)).  *Not a theorem and not shown:* a separation at any finite
size — at the sizes computed, the known adaptive algorithms cost more than the two-round
lower bound.  The hard instances are not nested basins, as the coordinator had expected
(D50), but a flat histogram in one block of coordinates that dilutes the first batch.
Whether three rounds suffice is open.  All of it is relative to the model: exact
evaluations of a residual known only to be Hamming–Lipschitz, uniform reference measure,
worst case over the class.
(x) *One value of the order parameter at a time* (theory report §11.25; **the coordinator's
paper proofs, checked numerically; reviewed by the Scientific Discovery Division
(SCI-REV-0001): the mathematics is sound, the headline below was too broad and has been
narrowed, and one proof step was missing and has been supplied**).  Inside a level set of the
order parameter the known part is a constant, and there are only `n + 1` level sets.  Two
consequences.  First, an elementary inequality — among pairs of binary variables with a
given odds ratio the mutual information is largest when both marginals are uniform; it
is **known** (Hasenclever and Scholz 2013, found for us by the Scientific Discovery
Division; our first version said "may be folklore") —
shows that on every level set sets around one centre are extremal and the exponents are
at most the uniform cube's, with equality at half filling.  Hence, **for fixed samples, and
for algorithms that are told the instance when the instance is a function of the order
parameter, no known part that depends on the configuration only through one order
parameter — ferromagnetic or antiferromagnetic, with any number of phases — has a larger
exponent than no known part at all, and without a field and with one phase these two
exponents are exactly the uniform cube's** (this settles what (viii) had left numerical).
For adaptive algorithms without a hint — the third exponent, the small one on the cube —
the comparison is proved for ferromagnets and for fields only ((viii), (v)); otherwise it
is a conjecture: an antiferromagnet without a field is proved to be at least as hard as
the cube, and at most as hard as the cube is for fixed samples.  (Our first version said
"makes certification harder than no known part at all … changes no exponent" without
these restrictions; pointed out by the Scientific Discovery Division in its review
SCI-REV-0001.)  This is a statement about two-letter alphabets: with three
or more letters it fails at small slopes — a known part that removes letters can make
the problem harder (numerical, given §11.26: below the slope `ln 2` the two-letter site has
the larger exponent at vanishing accuracy; which known part is the hardest is open — not
always a uniformly weighted sub-alphabet, by an example of the Scientific Discovery
Division).  Second, algorithms reduce to level sets: keep a bracket per
level set and always refine the one with the largest weighted upper end; a level set is
then examined only as closely as its distance from the maximum requires (deterministic
core machine-checked, `SliceRefinement.lean`).  Still open: the adaptive exponent on a
single level set (conjectured to be the hinted one, as on the cube), and the exact
adaptive exponent when perturbations that change the order parameter matter.
(xi) *Heteropolymer product landscapes* (theory report §11.26; workstream W,
`docs/workstreams/W_REPORT.md`; **paper proofs — the upper bounds by transfer of the
two-letter proofs — re-computed by the coordinator with an own implementation; the two
main theorems reviewed by the Scientific Discovery Division with independent
replication (SCI-REV-0005): nothing false; two gaps in the written proof of the adaptive
upper bound — the isoperimetric statement it rests on was stated in the workstream's
report only, and a uniformity over compositions was asserted, not proved — both closed
in the theory report; its twelve minor findings corrected; the nested algorithm has
never been simulated**).  The setting the certificate formats were built for, except
that the known part is restricted to single-site terms (the formats allow pairwise
ones): a fixed
sequence of
site types, any number of states per site, envelopes that need
not be symmetric.  All three exponents come from one function, and the kinds of sites
combine through a common *slope*, not at a common accuracy (their exponents do not add).
**The single-site ingredient is a classical object: a Rényi capacity of the channel that
sends an extreme allowed perturbation of the site to the site law it produces.
Asymptotically, at extensive accuracy and in the worst case over the class, a fixed
sample of `e^{nθ}` evaluations certifies the accuracy rate given by the sphere-packing
exponent of that channel at rate `θ`; adaptivity — or a hint, at the hardest instance —
gains exactly `θ`, for rates `θ` below the fixed point `h` of that exponent** (beyond it an
adaptive algorithm reaches every extensive accuracy; the range and the mode were missing
in our first version — a correction of the review).  Three
things that hold for two states fail beyond: the site function need not be concave, a
field does not always help, and the uniform site law is not always the hardest — a
uniform site with many equivalent states behaves, at vanishing accuracy, like one with
about `e^{u/2}` states; and at small slopes a three-state site with one rare state is
harder than the two-state cube (by `0.03 %` at slope `0.5`; found by the reviewers), although
no site law exceeds a universal ceiling — `u²/32` at vanishing accuracy, for slope `u` —
which the two-state cube attains to leading order.  Machine-checked here: the general
inequalities behind the every-`n` lower bounds (the product step for several kinds of
sites is on paper) and the two
elementary steps behind "the hardest instance is the Rényi centre" (`RenyiCentre.lean`).
(xii) *Evaluations together with local ensemble-averaged data* (exact low-order marginals
of the ensemble — an idealisation of local experimental data; theory report §11.27; a question
of the Scientific Discovery Division, which proved the adaptive case).  On the cube class,
knowing all `k`-body marginals of the true ensemble exactly changes neither the adaptive
nor the non-adaptive exponent, for every fixed `k`: the hard instances can be symmetrised
over a code so that no `k`-body statistic sees them.
(xiii) *Observable free energies* (theory report §11.28; a question of the Scientific
Discovery Division; **the coordinator's paper proofs, the certificate half machine-checked;
reviewed and replicated by that division — it stands; for envelopes of a special
("separable") form it is the classical range of a posterior odds in robust Bayesian
analysis, and the theorem extends that to envelopes with the triangle inequality**).  Everything above is about the total `ln Z`, which
no experiment compares with; what is measured are free-energy differences between
macrostates, `−ln[Z(A)/Z(B)]`.  Their exact range over the residual class has a dual
description: the largest ratio is the least factor by which the weight of `B` must be
scaled so that it can be *shipped* to `A`, when delivering a unit from a state `z` to a state
`y` costs `e^{d(z,y)}` units — and any such shipping plan is a certificate (`MacroRatio.lean`).
Only the envelope constraints from `B` to `A` matter.  Closed forms: for the two sides of
a threshold of an order parameter the extremal perturbation is the strongest uniform
field, so the free-energy difference between the two halves of the cube is uncertain by
`±n·ln cosh(u/2)`; a macrostate defined by one coordinate reduces to that site for
independent sites and has a site-by-site certificate for pairwise known parts; and at
large sizes the range is a max–min of transport costs and rate functions.  For known
parts without frustration (submodular ones) and macrostates that are monotone in the
state, the two extreme uniform fields are extremal for every such pair of macrostates —
the Scientific Discovery Division's theorem, machine-checked by it, its Lean file adopted
here (`MonotoneSandwich.lean`).  Nothing is said yet about how many evaluations narrow the
range.
(xiv) *Evaluations together with local data when there is a field* (theory report §11.29;
**the theorems are the Scientific Discovery Division's; our first version had two
conjectures in their place, one true for a different reason and one with a wrong formula
and two wrong numbers — `docs/DEAD_ENDS.md` D56**).  Knowing all one-body averages of the true
ensemble exactly changes neither class exponent (the lower bounds hold for every system
size): the hard instance
is a mixture of two simple ensembles whose averages already equal those of the same
mixture with a hidden well.  At a *given* instance — the known part itself — the same data
do exclude wells: a few per cent of the exponent for weak fields, most of it for strong
ones (a bracket; the exact value is open).
(xv) *When the remainder is small in a typical norm* (theory report §11.30; a request of
the Scientific Discovery Division after its measurements on force-field terms;
**elementary, partly machine-checked in `BoxClass.lean`, not refereed, no novelty claimed
beyond the placement**).  If the energy is a known function whose ensemble can be sampled
exactly plus a remainder with pointwise bounds, the number of evaluations that certifies
the free energy, with the instance as a hint, is the Boltzmann factor of *how far below the
known function the truth
may lie* — a free-energy distance in `k_BT` — divided by the accuracy (without a hint the
worst case is of the order of the Boltzmann factor of the width of the class divided by the
square of the accuracy).  **The system enters
only through that distance, not through its number of states or variables**; for a
remainder that is a sum over a growing system the distance grows with it, so the
exponential is moved into the right coordinate, not removed (our first statement of this
result said "does not depend on the size of the system", which the Scientific Discovery
Division rightly criticised).  The upper side of the free energy (a mean) is cheap.
Inside such a class the floor is the one assumption that sampling cannot replace — a
constant fitted on samples is not one, and the usual "mean plus two standard errors" is
not a certificate; ground states do not share the benefit.  Two additions are that
division's (re-derived and tested here, not machine-checked): with a certified *variance*
of the remainder next to a one-sided floor the free energy is bracketed with no
exponential bill at all (Bennett's inequality), and the floor is the end of a family —
an a-priori bound on a Rényi or Kullback–Leibler divergence of the true ensemble from the
model can take its place at a price in the accuracy, while the root-mean-square error
that a fit reports certifies nothing on its own.  On that division's enumerated
force-field instances the prices range from negligible to astronomically large and are
not predicted by fit quality; none of those numbers is a certificate.  Its search of the
literature then showed that every ingredient of this item is in print (Hoeffding's
inequalities of 1963; the stopping criterion of provable partition-function algorithms;
a paper of 2026 on partition functions under divergence bounds) and that the
statement with a hint, as a theorem, was not found; and it exposed a gap of ours — near
the floor of the class the cost comes from the *ceiling*, a term our first statement
lacked and which is now machine-checked.  Three additions of our own followed: at a flat
instance a hint is worth nothing, in general it removes a variance term; for an energy
sandwiched between two models that can be sampled, sampling in proportion to the width
of the sandwich certifies the free energy without a hint; and a free-energy *difference*
between two macrostates costs the larger of the two macrostates' own distances to the
floor — independent of how rare they are, possibly far more than the free energy of the
whole.
(xvi) *What a certificate of a real free energy looks like* (theory report Theorems 11.18a,
11.18d; the Scientific Discovery Division's workstreams P2 and P3).  That division measured
that a solvent term in rotamer variables is pairwise up to small remainders and then
built, for a twenty-residue model peptide on an extended backbone, a bracket for the
free energy from 87 441 evaluations out of `3.5·10⁹` states: evaluate the many-body term on
a Hamming ball around an anchor, bound what lies beyond by proved constants, and sandwich
the energy between two chain models.  Our part is the combinatorial core, machine-checked
at its request: the error of the anchored expansion of any order is an explicit sum of
mixed differences anchored at the reference, site penalties cover it, and — a negative
result — no deterministic procedure can do with fewer evaluations than the ball contains
unless the lower-order terms are bounded in advance.  Everything else in that certificate
is the division's paper proofs and unreviewed code, it is relative to a force-field
model, and it fails for helices and charged side chains.
(xvii) *Barriers* (theory report §11.31; the Scientific Discovery Division's idea and
statements, its Lean file adopted, a tree checker of ours machine-checked).  A lower
bound on the barrier between two configurations is a cut whose wall is certified by the
kernels that already exist; the same cut with partition sums bounds how long a sampler
stays trapped.  Negative results of that division come with it: no transfer matrix for
barriers exists, and discrete rates are relative to the move set.
(xviii) *When the known part itself has interactions along the chain* (theory report
§11.32; our workstream Y, examined by our referee R11 and by the Scientific Discovery
Division).  Everything above about exponents is for known parts whose sites are
independent.  For a nearest-neighbour chain as known part two exact reductions to products
of blocks give a limit with monotone brackets, and a lower bound holds for every
algorithm at every length.  For the simplest such chain the cost exponents are **not**
those of independent sites, in either direction: where the uncertainty per site is weak
they are larger — to second order by the structure factor of the chain, i.e. by its
cooperative response — and where it is strong two of the three are smaller, because the
coupling removes hiding places; the accuracy threshold rises throughout.  Our own first
summary said "an interaction raises the exponents"; the direction at strong envelopes
was found by the other division's review.  One synthetic two-state model, brackets
rather than formulas, paper proofs re-derived by two reviewers; machine-checked is the
lower bound for every algorithm around an arbitrary reference measure, nothing else.
(xix) *Certificates as dual solutions* (theory report Proposition 11.18b(e); proposed and
measured by the Scientific Discovery Division, soundness machine-checked here).  The
row-sum condition for "the reference is the minimum for every admissible remainder" has
a sharper form in which every site, in every state, takes a share of each pair it belongs
to; such shares exist exactly when the reference solves the pairwise linear relaxation —
they are its dual solution — and checking them is additions and comparisons on tables.
On that division's instances they certify every case in which the exact criterion holds.
One of our statements about domains with excluded pairs of states was false and was
corrected by its review (completeness of shares needs a product domain).
(xx) *What the evaluations of a certificate from a Hamming ball are paid for* (theory
report Theorem 11.18d, Propositions 11.18e, 11.18f, 11.113a; the questions, the share
forms and a decisive correction are the Scientific Discovery Division's).  Constants of
order `m` can be charged to the sites of each subset, to its pairs, to its triples, and
so on down to the subset itself — each level a smaller penalty than the one before,
state by state — and at each level they may be allocated freely: all machine-checked.
Which level and which allocation give the narrowest bracket *without sampling* depends on
the ensemble (charge every constant to the sub-pattern that is least often off its
anchor).  But in *evaluations* none of this matters: proposing states from any solvable
share model and evaluating the energy only with the ratio of the inner to the outer
width as probability reaches the bracket of the innermost level at that level's own
price.  The ball itself cannot be undercut by a deterministic certificate; our claim
that it cannot be undercut by a randomised one either was **false as written** — a
handful of random evaluations give a valid but useless bound, as that division's review
showed with a machine-checked core — and survives only on one site and, as a
conjecture, for a bracket of prescribed width.  Paper proofs and small synthetic tests
for the sampler and the allocation; nothing run on a real energy term by us.

(xxi) *Nesting by certified cost; a rate machine-checked by a reviewer; one side of a
sandwich at a time* (theory report §11.19 remark (1b); the remark after Theorem 11.53;
Propositions 11.113b and 11.18b(e)).  The cost bound of the nested adaptive algorithm
is monotone in the cost bounds of the procedures it calls, so if every step is served by
the procedure with the smallest *certified* cost, a further level can never raise the
certified bound — and with that rule three levels are certified below the worst case
found for two levels from four thousand sites on (exact evaluations of the bound by the
coordinator; a design chosen on the benign instance had shown no certified gain;
reviewed and replicated since — item (xxii), which corrects what that comparison is).  The rate `τ_k − h ≤ c₁/(k + c₂)` at which the level recursion approaches the
hinted exponent is machine-checked for the cube — by the Scientific Discovery Division,
whose review also found one proposition of ours false as worded (the small-slope law
for chains needs a symmetric envelope; a hypothesis lost when its statement was
adopted) and twelve errors of record, all corrected.  What a floor alone and a ceiling
alone certify is a proposition now: without evaluations the ceiling is the safe bound
and the floor the one that can lose arbitrarily much; as samplers it is the reverse —
from the floor both sides can be bought, at the price of the floor's own loss, and
from the ceiling the upper side cannot be bought at all.  The certificate kernel has a
domain-split rule and a soundness theorem for instances that store each pair table
once, both asked for by that division for its "shares at the leaves" certificates.

(xxii) *The sub-exponential term of the adaptive cost; two reviews applied; one order of
the sites per term* (theory report Theorem 11.58a and Lemma 11.55(d); §11.19 remark (1b);
Propositions 11.18f, 11.113a; Theorem 11.18d(a″), (d′)).  Without a hint, adaptive
algorithms on the cube class need between `exp(n·h − O(1))` and
`exp(n·h + O(√(n ln n)))` evaluations at every bounded accuracy: an explicit schedule of
about `√(n/ln n)` nested levels, chosen by certified cost, whose levels are of two kinds —
most of them run at a large accuracy with an exponentially large closure threshold and
lose only a polynomial factor (a new lemma), and the few that work at a bounded
threshold lose `e^{O(√n)}` with summable constants.  Our earlier text had called `n^{3/4}` the
heuristic limit of the method; that was wrong.  A paper proof by a workstream,
re-derived by the coordinator and refereed (R12: no major finding; every statement
re-derived and tested with independent code); it rests on the refereed but not
machine-checked level theorem, used far from where that theorem was simulated, and its
design is not competitive at any size where it can be evaluated.  The Scientific Discovery Division reviewed and replicated the
certified third level of item (xxi) — the rule holds, all 159 certified numbers were
reproduced with independent code — and found that five of the two-level numbers it was
compared with belonged to another design; **the comparison that needs neither a search
nor a model shows three levels certified below the exact cost of two levels from
sixteen thousand sites on, not four thousand.**  Its second review found nothing false
in our statements on randomised certificates, allocations and nested samplers, and
twelve conditions to add; the sampler's bound lost a factor two, and the allocation
rule "charge the most frozen site" now has its range of validity (safe for one end of
the bracket, and for the other only while a penalty stays below the free-energy cost of
its site), the structure behind it (the core of a convex game; its greedy vertex is
machine-checked by that division) and a lower bound that no site allocation can beat.
At that division's request the remainder identity of the anchored expansion is
machine-checked with a separate order of the sites for every term — which removes a
maximum over the states of a term's host sites, for at most `m` hosts and not for
`m + 1` — together with the anchored split of a pair table; and a lemma bounds what a
bound that ignores the signs of charges loses on a cluster with a net charge.
(xxiii) *The rate of the nested levels; what the nested algorithm needs in general; an
audit of every assumption* (theory report Theorems 11.53a, 11.53b, §11.33;
`docs/ASSUMPTION_AUDIT.md`; under the research owner's directive on generality of
26 November 2026).  **The exponent of `k` nested levels at accuracy zero is
`h + (2π²h²θ_hint″(0) + o(1))/k²`** — `0.641·a/k²` on the cube at `u = 1` — for every convex
non-adaptive exponent function with a smooth, strictly convex fixed point; with a kink
there the rate is `1/k`, so the general bound cannot be improved over all convex pairs.
One level acts on *lines* through a one-dimensional map that is jointly convex and has
a saddle-node exactly at the hinted exponent; the lower bound is the slow passage of an
orbit through that bottleneck (line lemma machine-checked); the upper bound needs a
minimax theorem — a *convex* family of lines moves line by line, a non-convex one does
not — and a convex sub-solution cut from the orbit curves.  For exponent functions with
slope at most one at zero the recursion is solved exactly by those curves; for the
Gaussian pair the lower bound is `1/(4cos²(π/(2k+1)))` in closed form.  A paper proof by
the coordinator (the workstream commissioned for it produced nothing), refereed
internally by two independent referees with their own code — no error of substance; a
statement about the *analysis* of nested algorithms at the level of exponents: no cost
at finite size follows from it yet.  **What the nested algorithm needs** was extracted
by a workstream and refereed: it works for an integrand on any probability space with
two *tail functions* (the cube's constants are reproduced exactly), and under a
certified bound on the influence between the blocks of a dependent known part
(dependence costs slope); it **provably gains nothing** on Gauss space with
Euclidean-Lipschitz functions when the coordinates are split into fixed blocks — the
dividing line is whether the envelope is additive over independent parts, not whether
the space is discrete — and with unbounded influence it **returns a false certificate**
(reproduced by the referee in every one of 120 runs).  **The audit**: two independent
readers classified the assumptions of 156 numbered statements with 513 tags (one in five is
load-bearing in the sense that a counterexample exists without it, one in seven is of
unknown status); it found one theorem that had lost a hypothesis when it was adopted
from its workstream (second-order classes below the Curie–Weiss coupling are cheap only
for an *additive* known part: restored, with counterexamples), eight stale sentences
and 47 sentences — almost all in summaries, this file included — that stated more than
is proved; all are corrected and recorded one by one.  The Scientific Discovery
Division's review of the sub-exponential term (item (xxii)) found it proved as stated,
reproduced its numbers from the text alone, and ran the outer loop of its main level
for the first time; its nine minor points are applied.
(xxiv) *The `1/k²` law at finite size; certified exponents of `k` levels; extensive
accuracies; the audit audited* (theory report Lemma 11.58b – Theorem 11.58e, the remarks
after Theorem 11.32 and in Theorems 11.116(e), 11.117(d); `docs/workstreams/Q2_REPORT.md`,
`Z_REPORT.md`, `Z_ADDENDUM.md` with their three internal reviews; `docs/ASSUMPTION_AUDIT.md`
§1a).  **Without a hint, adaptive algorithms on the cube class need at most
`exp(n·h + O(n^{1/3}(ln n)^{2/3}))` evaluations at every bounded accuracy** — the rate `1/k²` of
item (xxiii) turned into a cost — **and at most `exp(n·θ_hint(g) + O((ln n)²))` at an accuracy
`g·n`** (the hinted exponents; lower bounds `n·h − O(1)` and the hinted one).  Three steps.
A workstream removed the `√n` of item (xxii): one level over a family whose certified
cost is a maximum of lines moves every line with an error of five logarithms, and a
chain of levels with short outer blocks returns from a logarithmic to a bounded accuracy
for an additive term that is paid once.  Then every level hands down a *convex family
of lines* instead of one line, and the minimax step of the rate proof makes the family
move line by line; the best such sequence — cap the slopes at one, take the lower
convex envelope of the image — starts at the non-adaptive exponent, needs no restart,
and its top values bound the exponent of `k` nested levels **at every `k`**: exactly at
`k = 2`, by half a per cent too much from `k = 3` on (the true recursion gains from a
positive inner tolerance, which lines handed down one by one do not carry), with the
same limit constant.  Those bounds are computed with interval and exact rational
arithmetic: `0.500411·a`, `0.363301·a`, `0.312792·a`, …, `0.262652·a` at `k = 2, 3, 4, …, 400` for
`u = 1`, against `h = 0.262647·a`.  At a positive accuracy rate the bottleneck of the slope
map is out of reach of the lines that matter, and the exponent converges geometrically
in the number of levels.  As formulas at `u = 1` the new bound is above the non-adaptive
cost at `n = 10⁴` and below every earlier bound from about `3·10⁴` on; evaluated exactly
(certified cost, no run), two levels of the new schedule over the real base at
`n = 50 000` cost `e^{2818}` against `e^{5547}` non-adaptive, with `n·h = 1457`.  Paper proofs —
the workstream's and the coordinator's — refereed internally by three referees with
independent code (no error of substance; 23 findings of wording and numbers applied);
the certified computation and the equality at two levels were added afterwards and are
unrefereed; nothing is machine-checked; the constant in `O(n^{1/3}(ln n)^{2/3})` is about `10.9`
at `u = 1` and the schedule is not a practical algorithm.  **The audit of item (xxiii) was
itself reviewed on a sample** by the Scientific Discovery Division: its tag "false when
removed" can be trusted, its tag "needed only by the proof" could not — two such
hypotheses are needed by the statements (an additive true residual in the covering
sandwich for dense second-order classes, where a boundary member is certified by
`n + 1` evaluations against a bound of `2ⁿ`; homogeneity for the limit along a chain, which
need not exist), four more are of unknown status, and one statement of ignorance
contradicted our own report (the adaptive exponent *is* determined for one family of
interacting known parts).  All corrected; the first was replicated here with a linear
programme of our own.  That division also derived the weak-coupling coefficient of the
chain exponents — the direction in which a nearest-neighbour coupling moves the
non-adaptive exponent changes sign at the slope `1.5055` — which we confirmed by a
brute-force capacity computation and record as its result and an open question.
(xxv) *Consolidation checkpoint (27 November 2026): tail functions beyond the uniform cube;
the nesting section corrected by an outside review; general elimination; halt* (theory
report Proposition 11.124 and §11.33 as corrected; `docs/workstreams/I_REPORT.md`;
`proofs/Frontiers/FactorElimination.lean`; `docs/collaboration/consolidation/theory.md`).  **The
level theorem can be supplied with valid tail functions on any product of sites with a
product measure and an additive envelope**: a two-point recursion over the sites bounds
the measure of neighbourhoods from below (it reproduces Harper's theorem at ball sizes
and, on a biased cube, the balls around the rare vertex; it is attained on exhaustively
enumerated instances), both tail functions follow, the lower one in closed form by an
exact tensorisation, and for a fixed number of slopes on the uniform cube products of
balls are extremal up to polynomial factors — the coordinator's own, **unrefereed**, with
a conjecture (the single-letter potential is inductive up to a constant over `n`) and
four negative results (no Harper theorem for the biased cube in the concentration
regime, exhaustively for at most four sites; D69).  **Three sentences of the nesting
section were wrong** (the Scientific Discovery Division's review with replication,
SCI-REV-0027; the theorems stand): the false certificate under an uncertified influence
has two mechanisms; an influence confined to one hub site already breaks validity at
finite size; for band models the usable rule is to condition on the boundary layer
(D70).  The identity behind bucket elimination and the relaxation of a factor are
machine-checked for arbitrary summands, at the request of the software division.  The
last three unrefereed sections behind item (xxiv) were refereed: one closed form (the
second level of the cube) holds for slopes up to `4.65` only and is corrected; the
certificate script is sound.  **The division then halted under the research owner's
consolidation directive**; nothing is running.

What is *not* established: the guarantees are relative to published inputs (rational tables,
envelope constants, anchor values); certifying envelope constants for a concrete learned residual,
interval evaluation of force-field terms over voxels, and any claim of practical solver
performance are outside the development.  The complexity results are exponents on idealised
classes (product landscapes; for algorithms without a hint only the cube, with a zero known
part, a field, or — with an adaptive algorithm only for ferromagnets, and exact only up
to the junction with the uniform cube — a mean-field known
part, where the comparison with the uniform cube of item (x) is the coordinator's own
proof, reviewed by another division, and covers fixed samples and hinted algorithms
only), with paper proofs wherever the theory report does not name a Lean declaration; the
newest of them — the adaptive exponent — has a machine-checked recursion and bracket but a
paper proof for the number of evaluations, its extension to bounded accuracies is refereed
but has been run with three nested levels only at toy sizes; evaluated at the level of
expectations by the Computational Research Division, a third level as our referee
designed it — its servers chosen at the flat instance — gains little beyond the flat
instance and nothing that is certified, while with every server chosen by its certified
cost the certified bound of three levels is below the exact cost of the two-level
algorithm at the flat instance from sixteen thousand sites on, and below the worst case
found for two levels — a search in a mean-run model, in part for a neighbouring design —
from four thousand (theory report §11.19, remarks (1) and (1b); the coordinator's
computation, reviewed and replicated by the Scientific Discovery Division); the explicit
sub-exponential term `O(√(n ln n))` of Theorem 11.58a is a refereed paper proof for a
schedule that has been evaluated exactly only at depths and sizes where it is not yet
better than the plain bracket; the rate `1/k²` of the nested levels (Theorem 11.53b) is a
refereed paper proof about exponents, asymptotic in the number of levels; the bound
`n·h + O(n^{1/3}(ln n)^{2/3})` built on it (Theorem 11.58e) is a refereed paper proof whose
constants are not effective, whose tops are certified only given two of its own paper
statements, and whose schedule has been evaluated exactly only up to two levels over
the real base and seven over idealised ones; the level theorem on general probability spaces (§11.33)
is a refereed paper proof whose cost guarantee is vacuous wherever no sharp tail
function is known — everywhere but the uniform cube and Gauss space at bounded
accuracy; its
extension to a field as known part is refereed but its nested algorithm has never been
simulated end to end, and its
algorithms are
not practical at any size that can be simulated.  The chain-length independence of profile certificates is a bound, not an
observation: at every enumerated size the certificates grow; the limit theorem of §11.22 is
proved for bridges only and only off an unidentified countable set of accuracies, is a
conjecture for unrestricted walks, concerns one synthetic lattice model, and has been
reviewed by one other division (SCI-REV-0002: no false theorem; its headline reworded).
`docs/THEORY_REPORT.md` §8 lists the limitations, §10 ends with a
one-table summary of what each kind of knowledge about the residual costs, and
`docs/DEAD_ENDS.md` records every claim that was made and withdrawn.
