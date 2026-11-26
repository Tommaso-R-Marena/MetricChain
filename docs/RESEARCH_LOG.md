# MetricChain — Research Log

Chronological record of the theoretical program: what was tried, what was learned, how the
portfolio was re-prioritised.  Companion files: `THEORY_REPORT.md` (results and proofs),
`BLUEPRINT.md` (engineering hand-off), `DEAD_ENDS.md` (falsified or repaired claims),
`prior_art/L1–L6` (literature checks), `reviews/` (independent referee reports).

Conventions: **[V]** = machine-verified in `proofs/` (zero `sorry`, standard axioms only);
**[H]** = survived the adversarial harness `experiments/falsify_conjectures.py`;
**[P]** = paper proof only (stated with proof in the theory report, not formalized);
**[K]** = known result (cited), recorded for completeness.

---

## Session 1 (2026-11-24)

### Cycle 0 — workspace

* Lean 4.31.0 + Mathlib v4.31.0 (pinned in `lake-manifest.json`), prebuilt Mathlib cache.
* Layout: `proofs/Core`, `proofs/Frontiers`, `proofs/CertificateAlgebra.lean`,
  `proofs/AxiomAudit.lean`; `experiments/`; `docs/`; `scripts/audit_all.sh`.
* Decision: **exact-rational verification semantics** for every executable checker (certificates
  are rationals; solvers may use floats but must round outward before emitting a certificate).
  A dyadic outward-rounding model with proved error envelope lives in `Core/Rounding.lean`.
* Decision: the automatic axiom audit walks *every* declaration in the namespace instead of a
  hand-picked list (`#audit_axioms MetricChain`; changed in cycle 6 to a walk over every constant
  defined in a project module, `#audit_axioms proofs`).

### Cycle 1 — exploration and falsification (before any Lean)

Twenty-six candidate statements were written down and attacked numerically before formalization.
Three were refuted or had to be restated (D1, D4, D5 in `DEAD_ENDS.md`); the rest survived 400
randomized trials each.  The decisive reformulation of this cycle:

> **The provisional setting treats the residual `Δ_res` as "arbitrary non-decomposable".  That is
> not a usable hypothesis — with nothing known, nothing can be certified.  What is known about a
> residual is always an *envelope*: a (possibly asymmetric) cost `d(x,y)` with
> `Δ(x) − Δ(y) ≤ d(x,y)`.**  Global bounds are the discrete envelope, per-site differential
> envelopes `δ_i` are the site-additive envelope, certified Lipschitz constants of a network are a
> metric envelope on torsion space.  Once the residual is an element of
> `Lip₁(d)`, robust optimality has an exact characterisation (contact set of the Pasch–Hausdorff
> envelope), and the classical "global residual bottleneck" becomes a theorem about the discrete
> metric rather than an algorithmic defect.

This replaced the seeded conjecture of Direction A ("dual-coupled elimination dominates classical
pruning") by a sharper picture:

| question | answer |
|---|---|
| Can a dual gauge improve Goldstein DEE for pairwise product domains? | No — the Goldstein value is the exact margin and a gauge invariant. **[V]** |
| Is the `hi − lo` margin an algorithmic weakness? | No — with global bounds only, the energy window is the *exact* set of possibly-optimal states. **[V]** |
| What exactly can be pruned given an envelope? | Everything off the contact set `{x : E₀(x) ≤ E₀(y) + d(y,x) ∀y}`. **[V]** |
| …and given an envelope plus evaluated anchors? | Everything violating contact or "optimistic value ≤ competitors' pessimistic value". **[V]** |
| Where is differential DEE in this picture? | It is the single-site, uniform-dominator shadow of the contact criterion (sound, incomplete). **[V]** |

### Cycle 2 — prior-art map (three parallel literature checks)

Reports: `prior_art/L1_pruning_certificates.md`, `L2_relaxations_partition.md`,
`L3_realizability_geometry.md`.  Consequences for the claims:

* **Demoted to "known / folklore" (kept as verified building blocks):** gauge invariance of
  Goldstein (Shekhovtsov 2014/2016); exponential tree-like branch-and-bound on disjoint frustrated
  triangles (Basu–Conforti–Di Summa–Jiang 2023); Hölder temperature-rescaled decomposition
  (weighted mini-bucket, Liu–Ihler 2011); Jensen + bounded-differences free-energy sandwich
  (Gourgoulias et al. 2020 use the same inequality for model bias; Rio 2013 has the sharp
  constant); T₁ equivalence (Bobkov–Götze 1999); verified interval branch-and-bound in Lean 4
  (LeanCert, 2026); **the trace-enhanced s-stress lower bound** (Sonthalia–Van Buskirk–Raichel–
  Gilbert 2021, same constants; K-identity in Tsang–Pereira 2016) — this one had been logged as a
  discovery and was withdrawn (`DEAD_ENDS.md` D12); cycle-holonomy triangle bound (Lerman–Shi
  2022).
* **No match found (candidate contributions):** exact pruning criteria for a black-box residual in
  the envelope *and query* models; a temperature-aware, multiplicative dominance guarantee for
  partition functions used as a certificate rule; a machine-checked checker for
  reparameterisation/DEE/thermal-DEE certificates of cost-function-network-type problems;
  rigorous voxel-*integral* enclosures in the provable-design pipeline (the `K*` family uses
  minimised voxel energies); the assembled transcendental-free rational pipeline for chain
  energies; the finite-angle two-body closed form for the superposition cost of a torsion move
  and its chained bound (small-angle content is classical).
* **Repairs triggered by the review:** D2 and D3 (query model; closure of envelopes), D8
  (extremality holds at the MGF level only), D12 (equality in the s-stress bound needs a
  symmetry-invariant top eigenspace; the regular simplex with `L = 5`, `r = 3` is a
  counterexample to the vertex-transitive claim).

### Cycle 3 — formalization (batched)

Verified modules and headline statements:

| module | content | status |
|---|---|---|
| `Core/Basic` | partition function / free energy vocabulary | **[V]** |
| `Core/Rounding` | dyadic outward rounding, rational intervals (`+ − × ⁄ sq inv hull`), certified `exp` enclosure with argument reduction, Boltzmann-factor intervals, rational atlas of the circle | **[V]** |
| `Frontiers/EnvelopeDuality` | contact-set theorem, sharp-minimum theorem, McShane brackets (min energy and `Z` at all β ≥ 0) and exactness of the bracketed interval (cycle 5), query-model theorem, witness-size lower bound, local-to-global envelope lemma, differential DEE, energy-window exactness | **[V]** |
| `Frontiers/Dominance` | dominance transport lemma, thermal DEE, Goldstein exactness, gauge invariance, Desmet gauge optimum | **[V]** |
| `Frontiers/HoffmanWielandt` | von Neumann trace inequality and Hoffman–Wielandt for real symmetric matrices (via Birkhoff + rearrangement) | **[V]** |
| `Frontiers/Realizability` | K-identity, rank-constrained PSD approximation with trace penalty, s-stress lower bound, simplex certificates | **[V]** |
| `Frontiers/PartitionCertificate` | sum–product kernel `zverify` with thermal DEE, soundness, enclosure of the real partition function | **[V]** |
| `Frontiers/VoxelEnclosure` | Boltzmann voxel bounds with volume factor; assembly theorem from continuous integrals to the rational kernel (given that weights bracket the voxel integrals) | **[V]** |
| `Frontiers/VoxelBridge` (cycle 5) | derivation of that bracketing from voxel-table enclosures of a pairwise energy and product volumes; end-to-end certified torsion partition integral; rational enclosure of chart-arc measures | **[V]** |
| `Frontiers/SeparableVoxel` | separable envelopes ⇒ product of one-dimensional Boltzmann integrals; relative-width bound | **[V]** |
| `Frontiers/HolderDecomposition` | finite-temperature dual decomposition | **[V]** |
| `Frontiers/EnsembleDivergence` | sandwich gap = relative entropy of target w.r.t. reference; certified sampler error | **[V]** |
| `Frontiers/FreeEnergySandwich` | Gibbs–Bogoliubov + Hoeffding/McDiarmid sandwich; the worst bounded-difference residual is additive and two-level; `1/8` optimal | **[V]** |
| `Frontiers/Holonomy` | cycle-holonomy obstruction (conjugation-invariant norms), SE(3) translation holonomy with lever arms | **[V]** |
| `Frontiers/TorsionRMSD` | rigid-superposition chain rule, exact coaxial cost, two-sided reduced-inertia bounds, torsion-move chain | **[V]** |
| `Frontiers/InvariantEnvelope` | Lipschitz residual invariant under a group of motions (SE(3) or E(3)) ⇒ torsion-space envelope ⇒ membership in the kernel's residual class (cycle 5) | **[V]** |
| `Frontiers/ProofComplexity` | two-configuration weak duality, LP gap of the frustrated triangle, exact `2^m` bound for sum-free certificates, `2m` with `sum`, separation theorem | **[V]** |
| `CertificateAlgebra` | `(min,+)` kernel `verify`, residual kernel `verifyR` with the top-level entry point `verifyITop` for interval anchor data (consistency of the data checked; cycles 5–6; `verifyRTop` / `verifyRLowerTop` are special cases), Master Soundness Theorems, kernel-evaluated examples | **[V]** |
| `AxiomAudit` | automatic audit of every declaration + non-vacuity witnesses | **[V]** |

Engineering lessons recorded in `DEAD_ENDS.md` D6 (leaf rule), D7 (`decide +kernel`).

### Cycle 4 — second batch (after the first full audit)

Driven by the open items listed below and by the reviewers' "how to sharpen" notes:

* `SeparableVoxel` **[V]** — separable envelopes factor an `M`-dimensional Boltzmann voxel integral
  into `M` one-dimensional integrals, with a relative-width bound; this is the certificate form of
  second-order (Gaussian) voxel quadrature.
* `isLeast_sum_of_block_separable`, `exact_margin_of_block_separable` **[V]** — exact dominance
  factorises over blocks whenever the difference energy is block-separable (the abstract form of
  "factorises over the connected components of the link graph"; the 3-body model itself is not
  defined in Lean, so the link-graph reading is on paper).
* `boltzmannAvg_dominance_error` **[V]** — thermal pruning with margin `γ` changes any observable
  bounded by `B` by at most `2B e^{−βγ}`: certified ensemble averages, not only free energies.
* `verify_sound_real`, `verifyR_sound_real` **[V]** — certificates accepted for an outward-rounded
  rational lower instance bound the true real-valued energy.
* `sumFree_gap_exponential`, `sumFree_complexity` **[V]** — approximate sum-free certificates
  (within `d` of the optimum) still need `2^{m−d}` leaves; exact complexity `2^K` for bound `K`.
* `EnsembleDivergence` **[V]** — the sandwich gap equals `KL(reference ‖ target)`; certified error
  of a reference sampler in terms of the envelope constants.
* `experiments/reference_checker.py` — untrusted reference implementation of the three checkers
  on the JSON format, six conformance vectors identical to the kernel-evaluated Lean examples,
  soundness fuzzing against brute force.
* Process incident and repair: `DEAD_ENDS.md` D13.

### Cycle 5 — independent adversarial audit and repairs

An independent reviewer (fresh context, instructed to refute) audited the whole repository at the
end of cycle 4: every documented claim against its Lean statement, every headline theorem for
vacuity or circularity, every harness test for power.  Outcome: **no forbidden construct, no
vacuous headline theorem, no critical error; five major and six minor discrepancies between what
the documents said and what had been proved**, plus three harness tests that could not fail.  All
were repaired in this cycle; the record of what was wrong is `DEAD_ENDS.md` D14–D18.

| finding | repair |
|---|---|
| bounded-difference sandwich documented for arbitrary references; proved (and true) only for product references | documents corrected; counterexample kept as harness test `DEAD.5`; the general-reference Hoeffding width tested as `III.6` |
| residual kernel sound only vacuously on inconsistent data; partition kernel's `Nonneg` hypothesis unchecked | `RProblem.Consistent` with `RProblem.consistent_iff_nonempty`; top-level kernels `verifyRTop`, `verifyRLowerTop`, `zverifyTop` whose soundness theorems have no side condition; kernel-evaluated rejections; reference checker and conformance vectors extended |
| voxel pipeline assumed that weights bracket voxel integrals | `VoxelBridge.lean`: `pairwise_voxel_weight_bounds`, `certified_torsion_partition` (pairwise energies, product voxels, product measures), rational enclosure of chart-arc measures, three concrete witnesses |
| "SE(3)-invariant" formalized as invariance under all isometries; no uniform constant | invariance parametrised by a group of motions (`RigidInvariantIn`); `residual_torsion_move_min_in`, `residual_torsion_move_uniform`, `residualLowerClass_of_rigidWithinIn`, `verifyR_sound_invariant`; non-degenerate witness |
| "two semirings, one algebra, same rules" | reworded: decomposition is a rule of the tropical kernel only |
| robust interval "exact" proved only as a bracket | `robust_min_interval_exact`, `robust_partition_interval_exact` (intermediate value theorem along the segment between the McShane envelopes) |
| separation measured in visited leaves only | `sum_rule_separation_size` (nodes), `sum_rule_separation_dataSize` (description length with embedded sub-instances) |
| many-to-one thermal pruning asserted, injective case proved | `partition_transport_fibers`, `partition_prune_bracket_fibers` |
| the Boltzmann-factor brackets of `Z_encloses_partitionFn` were hypotheses never derived from the certified exponential | `IntervalInstance.lean`: instances computed from interval energy tables, `certified_partition_of_intervals`, and a kernel-evaluated real enclosure `Z_triangle(β=1) ∈ [2.3068, 2.3069]` |
| trivial non-vacuity witness; anchors required to be exact rationals | new witness forcing every exact certificate to evaluate both states; `ResidualLowerClass`, `verifyR_sound_lower`, `certified_gap_interval` |
| harness tests X.1, II.4, VII.1 could not fail | rewritten with independent computations, exhaustive certificate enumeration, the prune rule, and built-in power checks (each test now fails if a deliberately wrong variant of the claim is never caught); mutation tests of the rewritten tests (`experiments/mutation_tests.py`, added to the repository in cycle 6: 36 mutations, 35 caught, one expected pass); new tests I.6, II.7, II.8, III.6, VII.2, DEAD.5 (41 tests in total) |

The audit also changed one design decision rather than only wording: lower bounds need anchor
values that are *lower bounds* on the residual, so a producer with floating-point evaluations
should publish rounded values.  The first repair gave the residual kernel two entry points with
two semantics; the re-audit showed that the lower-only one can never refute an envelope, and
cycle 6 replaced both by interval anchor data.

### Cycle 6 — re-audit of the repairs

The same reviewer re-checked every finding against the repaired repository (three commits:
kernels and theory, voxel follow-ups, harness).  Verdict: ten of eleven findings resolved, the
`SE(3)` item partially; no theorem false, vacuous or circular; one new major point in the audit
tooling and five minor ones (`DEAD_ENDS.md` D19).  Repairs of this cycle:

* audit tooling: version-independent detection of incomplete proofs, token scan over all files,
  named (audited) non-vacuity witnesses, a self-test with planted violations, mutation tests of
  the harness as a repository artifact (36 mutations: 35 caught, 1 expected pass), import
  coverage and conformance-vector freshness checks, doc-reference check extended to the README,
  qualified names and structure fields;
* residual kernel: **interval anchor data** with `verifyITop`, `IProblem.consistent_iff_nonempty`
  and `verifyITop_sound`; the exact and lower-only kernels are special cases; the JSON schema
  has no default reading of an anchor value; the reference checker validates well-formedness;
* geometry: group-restricted `min`-inertia chain rule; a verified instance with an invariance
  group smaller than all isometries and a residual that is not reflection-invariant; the
  identification of that group with `SE(3)` is explicitly a paper step;
* voxels: executable volume brackets that converge under subdivision.

A last focused check of this round confirmed all of the above and left three minor points, also
repaired (`DEAD_ENDS.md` D20): the axiom walk now goes by defining module instead of by name and
anonymous `example`s are forbidden; the reference checker has a strict single-reading format and
never raises; the doc-reference check tracks namespaces.  Three review rounds in total: 5 major +
6 minor, then 1 major (tooling) + 5 minor, then 3 minor; no theorem was found false, vacuous or
circular in any round, and every finding concerned either a document claiming more than its Lean
statement, a kernel side condition, or the audit tooling itself.

### Portfolio reassessment (end of session 1)

* **Strongest discovery so far.**  The *envelope duality* cluster: under any envelope the set of
  configurations that can be optimal is exactly a contact set; with evaluated anchors the exact
  discardable set is characterised by two inequalities; the certified value interval is exactly
  the interval between the two McShane envelopes at every temperature; and an `ε`-certificate
  whose incumbent is an evaluated anchor must evaluate the residual on every state within
  `(1−κ)σ − ε` of the optimum (a witness-size lower bound; *corrected in cycle 7* — the earlier
  wording "any ε-certificate" was false for configuration certificates, `DEAD_ENDS.md` D21).
  Individually elementary — and, as the cycle-7 referee report established, classical in
  substance — they give a principled interface for neural residuals: the architecture must export
  an envelope, and the price of a loose envelope is quantified.
* **Second.**  Verified certificate kernels in two semirings (tropical, residual and
  sum–product) covering reparameterisation bounds, branching, DEE, differential DEE under a
  residual, thermal DEE, dual decomposition (tropical kernel only) and voxel enclosures of
  continuous integrals — with
  *thermal dominance* (a temperature-aware, multiplicative pruning guarantee for partition
  functions) and the *voxel enclosure with volume factor* as rules that the provable-design
  literature does not have.
* **Third.**  Finite-angle torsion-to-RMSD certificates: the exact coaxial superposition cost
  `2S − 2√(S² − 4 I_A I_B sin²(φ/2))`, its two-sided reduced-inertia bounds, the chain rule, and
  the corollary that an SE(3)-invariant Lipschitz residual has an explicit torsion-space
  envelope — which closes the loop between Direction C (geometry) and Direction A (envelopes).
* **Withdrawn.**  The trace-enhanced spectral obstruction for 3-D realizability was ranked second
  until the third literature check found it in print (NeurIPS 2021).  It stays as a
  machine-checked certificate (formal proof including Hoffman–Wielandt; we know of no earlier
  formalization), not as a result.
  The episode is recorded in `DEAD_ENDS.md` D12 together with the false sharpness claim that
  accompanied it.
* **Fundamental limitation that remains.**  (a) Every exact criterion we proved is itself a hard
  combinatorial problem (contact-set membership is an MRF minimisation); we certify, we do not
  solve.  (b) The free-energy sandwich is extensive in the number of sites; it certifies free
  energies only when `β c_i ≪ M^{-1/2}` or after localisation; and its `Σ c_i²` form needs a
  product reference.  (c) Continuous integration is certified to zeroth order per voxel (end to
  end for pairwise energies on product voxels) and, given separable envelopes, to second order;
  the Taylor/Hessian step producing those envelopes is specified on paper only.  (d) Nothing
  here bounds mixing times of samplers.  (e) Every guarantee is relative to published envelope
  constants; certifying such constants for a concrete network is not addressed.
* **Could a different representation overcome it?**  For (b): replace the product reference by a
  tree reference and Hoeffding by a variance-aware (Bennett) bound with exactly computed
  conditional variances — the transfer matrix makes those computable.  For (c): the rational
  atlas makes the integrand a rational function times `exp(rational)`; one-dimensional envelopes
  factorise, so a product-of-1-D certificate would cost `M × (1-D resolution)` instead of
  `resolution^M`.
* **Can several discoveries be unified?**  Yes, and partly done: the envelope is the common
  object behind differential DEE (β = ∞), the robust partition bracket (finite β) and the T₁
  transport inequality (uniform second-order sandwich).  The leaf / branch / dominate rules are
  parallel in the tropical and the sum–product semiring; decomposition is not (`DEAD_ENDS.md`
  D17).
* **Is continued investigation justified?  Highest-leverage next steps.**
  1. Variance-aware sandwich for tree references (new mathematics, formalizable).
  2. Second-order voxel certificates with the product-of-1-D structure; a verified checker.
  3. Size lower bounds for AND/OR (decomposition-aware) certificates on weakly coupled chains —
     the disjoint case is known, the coupled case is open.
  4. The hardness half of the link-graph dichotomy for exact dominance with 3-body terms (the
     tractable half is verified in its abstract block-separable form; a Lean model with 3-body
     terms and its link graph is still to be written).
  5. Connecting the kernel to LeanCert-style continuous leaves (interval evaluation of the
     rational torus energy) to obtain one end-to-end verified mixed discrete–continuous checker.
     *Status after cycle 5:* the chain "cell enclosures of the energy terms ⇒ rational weight
     instances ⇒ kernel ⇒ bound on the continuous integral" is verified (`VoxelBridge`,
     `IntervalInstance`), with a worked chart-arc instance for the potential `cos θ`.  Still
     missing: verified interval evaluation of realistic terms (distances through forward
     kinematics, Lennard-Jones, Coulomb) over cells; cells of the rotated charts; volume bounds
     that converge under refinement inside the kernel input (the lemma
     `two_arctan_sub_bounds_of_sq` provides them, the executable bracket uses the crude one).
  6. Realizability certificates for the data predictors actually emit: weighted or incomplete
     distance matrices with bond-length constraints, and a bound that keeps part of the
     diagonal-variance term discarded by the known spectral bound.
  7. A finite-angle metric-tensor (Eckart-frame) version of the torsion chain rule replacing the
     `ℓ¹` accumulation.
* **Radically different paradigm?**  Not yet warranted.  The envelope formulation is already a
  change of foundation relative to the charter's "arbitrary residual"; the next change would be
  probabilistic certificates (PAC-style statements for sampled anchors), which the present exact
  framework deliberately excludes.

### Open bottlenecks

* No formal statement yet for weakly dependent (Markov / Dobrushin) references in the sandwich:
  the verified statements are the two extremes — product references (`Σ c_i²`) and arbitrary
  references (`(Σ c_i)²`).
* A two-sided decomposition (product) rule for the partition kernel — tree elimination of
  independent or weakly coupled sub-instances — is not in the verified kernel (`DEAD_ENDS.md`
  D17); with it the separation theorem of `ProofComplexity` would have a finite-temperature
  counterpart.
* Envelope constants for a concrete learned residual (certified Lipschitz constants, inertia
  bounds) are inputs; nothing here certifies them.
* The Taylor step producing second-order (separable) voxel envelopes from Hessian bounds and the
  information-based lower bound are paper-level; the separable-envelope theorem itself is verified.
* The Procrustes–Gram stability inequality (Tu et al. 2016) is cited, harness-tested, not
  formalized.

---

## Session 2 (2026-11-24, continued)

### Cycle 7 — independent review, reclassification, and certification geometry

**Mandate.**  Preserve checkpoint 477391f; seek independent mathematical review before building
on it; ask whether envelope duality and its lower bounds are manifestations of a deeper theory
(optimal recovery, McShane–Whitney, robust optimisation, interval uncertainty, certified
black-box optimisation); look for matching upper and lower complexity bounds, correlated
uncertainty, compositional certificates and general statistical-mechanical observables in one
framework; separate new results from formalizations and rediscoveries.

**1. Independent referee report** (`reviews/R1_referee_report.md`; fresh agent, own code,
no access to the harness).  Verdict: no machine-checked statement false, no vacuous definition;
*no result publication-worthy as mathematics as it stood*; four major overstatements —
(1) the gloss of the witness-size bound ("any certificate"), (2) the novelty column for A1–A5,
(3) "reparameterisation cannot improve dominance pruning" beyond single-site tests, (4) the
(+,×) kernel has no sub-exponential exact certificates on chains — and nine minor ones.  All
were acted on before any new result was built on the checkpoint: text corrections in the theory
report (§§0.2, 2.2–2.4, 3.2, 3.4, 3.6, 4.1, 4.3, 4.4, 6.2, 6.3, 8), blueprint (§§6.2, 6.3, 7,
8.4, 9), `DEAD_ENDS.md` D1 (scope) and D21–D24, D27; the kernel weakness was repaired in Lean
(below).  The referee's first proposed direction — certificate complexity with matching bounds —
coincided with the direction already under exploration and became the main line.

**2. Three literature checks** (`prior_art/L4` certified optimisation and optimal recovery,
`L5` polytropes / interval uncertainty / robust Bayes, `L6` transport–entropy and
information-theoretic limits; search logs and unreachable sources are listed in each file).
Net effect on the claims: the identifications (polytrope = difference constraints = simple
temporal network = Lipschitz polytope; conditional envelope = minimal network; passive bound =
transport–entropy conjugate; thermal contact) are textbook or known in spirit; minimal
certificates as coverings are known in `ℝ^d` (Hansen–Jaumard–Lu, Baran–Demaine, Bachoc et al.);
the additive two-level extremal of the sandwich for a fixed product measure is in print
(Alon–Boppana–Spencer; Bobkov–Houdré–Tetali) — the earlier "implicit in the literature" was too
generous to us.  Not found: certificate complexity through rate–distortion functions (exponent,
dichotomy, Gibbs/finite-temperature form), the dimension-free best-first bound, second-order
envelope classes as a certified interface.

**3. Exploration before formalization** (scratch scripts `explore1`–`explore6`, since ported to
the harness as cluster XI).  Survived: slack identities and certificate ⇔ cover; `N_cov ≤ N_val ≤
N_point ≤ N_cov + 1`; LP-dual bounds ≤ `N_frac`; hardness reduction; best-first separation and
`m ≤ |C| + 1` for shrunk covers; conditional envelope = LP optimum; thermal contact = LP
optimum; thermal converses on every evaluated set (318 450 checks, best ratio 0.9999); the
single-letter identity behind the finite-temperature exponent (two sides agree to `10⁻³`);
order-`m` anchored remainder with sharpness; star envelope = LP optimum.  Exact layer counts for
the binary product family, `n⁻¹ ln max_μ L_μ` against the predicted exponent:

| `ρ = e/c` | `R*` | n = 100 | 200 | 400 | 800 |
|---|---|---|---|---|---|
| 0.25 | 0.3509 | 0.3751 | 0.3647 | 0.3587 | 0.3552 |
| 0.50 | 0.1882 | 0.2073 | 0.1994 | 0.1947 | 0.1919 |
| 0.75 | 0.0798 | 0.1004 | 0.0916 | 0.0866 | 0.0836 |
| 0.90 | 0.0293 | 0.0480 | 0.0402 | 0.0356 | — |

Refuted along the way (kept as harness records `DEAD.6`–`DEAD.9`): best-first within one
evaluation of the optimum; the "any certificate" gloss; the fixed-`β` Bobkov–Götze equivalence;
additivity of the worst residual for dependent references (found by L6, re-verified).

**4. Formalization** (parallel agents, one file each; every file built with zero warnings and
walked by the axiom audit).

| module | content | status |
|---|---|---|
| `Frontiers/CertificationGeometry` | slack quasi-metric; certificates are coverings; LP-dual, fooling, volume and partition-function bounds | **[V]** |
| `Frontiers/CertificateNotions` | value / point / configuration certificates differ by at most one evaluation | **[V]** |
| `Frontiers/ConditionalEnvelope` | conditional envelope, tower property, anchored sharp minimum, worst-case regret | **[V]** |
| `Frontiers/CertificateComplexity` | domination reduction; product landscapes: one evaluation iff sharp; product partition bound; `(6/5)ⁿ` | **[V]** |
| `Frontiers/ExponentialWeights` | general exponential-weights converse; entropy bound and Hölder converse for free-energy certificates | **[V]** |
| `Frontiers/ProductRates` | product forms of both converses; a finite-temperature exponential lower bound on a sharp landscape | **[V]** |
| `Frontiers/BestFirst` | best-first runs, separation, resource-augmentation bound, termination, sharp instance | **[V]** |
| `Frontiers/ThermalRobustness` | thermal contact interval (with and without evaluations), weight cone, slack forms of the envelope partition functions, transport–entropy inequality | **[V]** |
| `Frontiers/SecondOrderEnvelope` | star remainder, pairwise sandwich, kernel statement, exact envelope, certified minimiser | **[V]** |
| `Frontiers/PartitionProduct` | cut and elimination rules for the partition kernel, soundness, separations | **[V]** |
| `Frontiers/HigherOrderEnvelope` | anchored decomposition, order-`m` remainder theorem with sharpness, consistency with order two | **[V]** (second checkpoint of the cycle) |
| `Frontiers/SampledSandwich` | probabilistic free-energy certificate from independent samples of a product reference | **[V]** (second checkpoint of the cycle) |

Paper-level only: the upper halves of the two exponent theorems (type covering), the converse
half of the transport–entropy duality, the complexity-theoretic reading of the domination
reduction.

**5. What was learned.**
* The envelope cluster is one object seen five ways (a polytrope); nothing in it is new
  mathematics.  The productive change of representation was the *slack quasi-metric*: it turns
  "what can be certified after these evaluations" into a covering problem whose radii are the
  points' own gaps, and makes lower bounds a matter of LP duality.
* First-order envelopes have an exponential price that no algorithm can avoid, at zero and at
  finite temperature, with exact exponents given by one variational formula (energy gap →
  free-energy gap of a macrostate).  This closes the main loop of blueprint §6.2 as a general
  strategy and replaces the witness-size bound.
* The way out is the *order* of the envelope, not its size: bounded mixed differences make a
  linear number of evaluations sufficient and the reduction to the pairwise kernel lossless.
  [Later correction, cycles 8–9: true under weak second-order coupling only; with dense
  constants the remainder is quadratic in the distance, D32.]
* Correlated references: the exact worst-case gap is a transport–entropy conjugate for every
  reference, but its extremal residual is not additive (D25); the planned "transfer-matrix
  formula" does not exist in the naive form.
* The partition kernel now has decomposition rules worthy of the tropical one.

### Portfolio reassessment (end of cycle 7)

* **Strongest result.**  The certification-geometry cluster (theory report §11): covering
  characterisation, dichotomy and exact exponents with a common variational formula at zero and
  finite temperature, hardness, resource-augmented best-first bound, second-order exact
  reduction.  Tools are standard, proofs are short, the one-shot halves are machine-checked.
* **Demoted.**  Envelope duality A1–A5 (known in substance); the sandwich's attainment statement
  (in print).
* **Can it be strengthened / generalised?**  Yes: interacting known parts (transfer-matrix
  exponents), heterogeneous sites, second-order prefactors, lower bounds for second-order
  classes, a polynomial algorithm on product landscapes — theory report §12 lists these with
  what a publication would need.
* **Different representation?**  The weights `w = e^{−βg}` linearise the finite-temperature
  problem (robust Boltzmann averages are linear-fractional programs over a cone whose dual is a
  flow with gains); not pursued beyond the contact interval.
* **Is there a more promising direction entirely?**  Probabilistic certificates: the contrast
  between one linear functional and exponentially many pointwise evaluations (§11.6) says that
  the deterministic pointwise model is the wrong one for free energies.  A PAC-style kernel
  (sampled reference averages with verified concentration bounds) is the natural next
  foundation; its first theorem, the sampled sandwich, is machine-checked (Theorem 11.21); the
  kernel itself was not started.

### State at the end of cycle 7 (superseded by the list at the end of cycle 8)

Verified state: every module under `proofs/` builds with zero warnings and is walked by the axiom
audit; the harness (58 registered tests: 49 that must survive, 9 documented refutations) and its
mutation tests pass; `scripts/audit_all.sh` exits 0.  In priority order, the work that an
authorised subsequent session should take up:

1. **Act on the second referee report** (`reviews/R2_referee_report.md`, commissioned on the
   second phase): anything it finds false or overstated in theory report §§10–12 comes first.
2. **The exponent theorems.**  Write the upper bounds (type covering with credit distortion;
   heterogeneous sites) in full; decide whether the finite-temperature formula is a known
   source-coding exponent (Marton, Merhav) in disguise; attempt the interacting case, where the
   partition-function bound is the Shannon lower bound of a process rate–distortion function
   (theory report §12, item 1).
3. **Probabilistic certificates.**  The sampled free-energy sandwich (Theorem 11.21, harness
   XI.13) is the first theorem; a kernel that checks sampled reference averages against
   verified concentration bounds, and the analogous statement for minimum energies, are not
   started.
4. **Second-order envelopes with a real residual.**  Certified mixed-difference constants for
   one concrete residual; box-restricted constants; lower bounds on the number of evaluations
   (covering arrays).
5. **Dependent references.**  The binary-tree question of D25; a two-sided transfer-matrix
   bracket for the worst-case gap of a Markov reference.
6. **Certificate formats.**  `cut` / `elim` nodes are in the Lean kernel only; the JSON format,
   the reference checker and the conformance vectors have not been extended.
7. Items carried over from session 1 that remain open: lower bounds for decomposition-aware
   certificates on connected frustrated families; verified interval evaluation of realistic
   energy terms over voxels; realizability certificates for incomplete distance data.

## Cycle 8 — second referee report; from certificates to algorithms

*Trigger.*  The second independent referee (`reviews/R2_referee_report.md`) reported on the
second phase, and the directive for this phase asked for matching upper and lower complexity
bounds, converses and a unified framework.

**Referee findings and what was done.**  No machine-checked statement was false.
* *Critical:* Theorem 11.15 (exponent of free-energy certificates) was false as stated for
  exponentially small accuracies (at `ε = 0` every certificate is the whole space).  Corrected
  (hypothesis `ln(1/ε_n) = o(n)`, proof level `a_n`), counterexample machine-checked
  (`exact_free_energy_certificate_eq_univ`), D29.  Committed separately as e8ceeab after a full
  audit.
* *Major:* the doubling remark after Theorem 11.11 (false with a known part: D30); the planning
  formula of blueprint §6.6 (per-site maximisation and Boltzmann weights: D31); "second-order
  envelopes: the way out" (remainder quadratic in the distance; `STARCERT` could loop: D32); the
  scope of the partition-kernel separation (exact endpoint; representation-dependent rigidity:
  D33).  All four re-computed independently before the documents were changed
  (`DEAD.11`–`DEAD.13`, and the gauge instance in Lean).
* *Minor (17):* all applied; the most substantial is that Theorem 11.5 was true but not sharp —
  point, value and configuration certificates have the same minimal size (the referee's
  exchange lemmas, now in `RefereeLemmas.lean`).
* The referee's verdict on the cluster — "a coherent note, not a theorem-driven paper" — is
  recorded in theory report §12 and accepted.

**New mathematics (theory report §11.10; `QueryLowerBound.lean`, 1212 lines).**  The referee's
two constructive requests were an algorithmic statement and a probabilistic notion of
certificate.
* *General principle (any class, any functional).*  An `ε/2`-correct deterministic algorithm
  queries a point where every `ε`-distinguishable alternative differs from the instance; a
  randomised one with error probability `δ` does so with probability `1 − 2δ`; hence packing
  lower bounds on (expected) evaluations; conversely, spot-checking a hint is sound.  This is
  the fractional-block-sensitivity bound of Boolean query complexity and the
  radius-of-information argument, transplanted.
* *Minimum.*  Instance-wise deterministic complexity **equals** value-certificate size
  (`instance_query_complexity`); every randomised algorithm pays `(1 − 2δ)` times each covering
  bound (`binary_randomized_exponential`: `(1−2δ)(6/5)ⁿ`).  Learn-then-cover reaches the exponent
  `R*` on additive instances without knowing the residual — this answers the "Algorithms"
  question left open at the end of cycle 7.
* *Free energy.*  A dip of depth `c` at `y` multiplies `Z` by `E_π e^{β(c − s(Y,y))₊} ≥
  e^{βc − Λ(y)}` with the *soft gap* `Λ(y) = ln Z(f+g) − ln Z(f+U_y)`; so every algorithm must
  reach within slack `(Λ(y) + ε)/β` of every `y`.  Three budgets for a macrostate: energy gap
  (zero temperature), free-energy gap (deterministic), soft gap (randomised).
* *Threshold.*  On the cube class the accuracy `n ln cosh(βc/2)` separates a bounded number of
  random evaluations from exponentially many for every algorithm
  (`cube_thermal_randomized_bound`; upper bounds on paper, Harper's theorem for attainment).

* *An upper bound in the same quantity* (`SoftGapBounds.lean`, Theorem 11.26, found while the
  cycle's audit was running).  The soft gap is `βs`-Lipschitz, and every alternative with
  `Z' ≥ (1+η)Z` differs from the instance on dip weight at least `ηZ`; hence sampling from
  `½π + ½·(dip weights)` detects every distinguishable alternative, and
  `N ≈ 2 ln(1/δ) E_π[e^{Λ}]/(1 − e^{−ε/2})` evaluations suffice.  Lower and upper bounds on the
  randomised cost are now two functionals of one quantity; on the cube this gives a
  machine-checked exponential gap between deterministic (`≈ 2ⁿ`) and randomised
  (`≲ (2/(1+e^{−βc}))ⁿ`) cost.  The bound is crude (exponent `U_β`); the exact randomised
  exponent remains open.  Product form of the lower bound: `thermal_product_randomized`.

**Falsification before formalisation.**  Explored numerically first: all sensitive blocks
against single dips on small spaces (dips are *not* extremal in general — D34, kept as
`DEAD.14`); the isoperimetric claim on the 4-cube; the predicted exponent against exact ball
counts up to `n = 1600`; the consistency `R^rand_β ≤ R_β` of the three single-letter formulas
(benchmark B10); the detection-weight lemma on 27 005 sensitive sets of random instances before
it was formalised (it compiled on the first attempt, and its hypothesis `g' ≤ g` turned out to
be unused); a probe of the conjecture on biased cubes with `n ≤ 4` (ratio between all sensitive
sets and single dips between 1 and 2, no trend).  Harness cluster XII (6 tests) and
`DEAD.10`–`DEAD.14`; 15 new mutations, all caught.

**Literature (`prior_art/L7`).**  Four searches: fractional block sensitivity / randomised
certificate complexity (confirmed as the known method); randomised lower bounds for Lipschitz
optimisation (classical worst-case statements not re-verified; no instance-wise randomised
statement found); Bachoc–Cesari–Gerchinovitz (deterministic certified algorithms); query lower
bounds for normalising constants (Ge–Lee–Lu 2020: hidden-perturbation technique, log-concave
setting).

**Assessment.**  The cluster is now a query-complexity theory rather than a theory of one
certificate format, with one matching pair (the threshold of Theorem 11.25) and one exact
identity (certificate size = instance-wise complexity).  The proofs remain short and the tools
standard; the honest classification is unchanged in kind — a note, plus a formalisation.

### State at the end of cycle 8 (superseded by the list at the end of cycle 9)

Verified state: every module under `proofs/` (36 files) builds with zero warnings and is walked
by the axiom audit; the harness (69 registered tests: 55 that must survive, 14 documented
refutations) and its mutation tests (82 mutations: 81 caught, one expected pass) pass;
`scripts/audit_all.sh` exits 0.
In priority order:

1. **The randomised exponent at finite temperature** (theory report §12, item 2(b)): it is
   bracketed, `R^rand_β ≤ · ≤ min(R_β, U_β)`.  Prove or refute that single dips are extremal at
   the exponential scale on product spaces — an asymptotic isoperimetric inequality with two
   measures (Harper for the uniform cube; Ahlswede–Zhang / Alon–Boppana–Spencer-type results
   are the place to look).  This would turn the third row of the table of Theorem 11.24 into
   an equality and make the threshold general.
2. **Reviews.**  A third independent referee is reading §11.10 (as of f1a6015) and the
   faithfulness of the R2 corrections; act on its report first.  Theorem 11.26 and
   `SoftGapBounds.lean` were added after that review started and have not been refereed.
   Six independent workstreams were launched at the end of this cycle (isoperimetric
   conjecture; chain-structured known parts; alternative representations — reduced costs, A*,
   weak KAM, tropical; free-energy estimation in statistical mechanics and general
   observables; lower bounds for second-order classes; envelopes from chain geometry); their
   reports are to be verified independently before anything is integrated.
3. **Beyond product landscapes.**  A pairwise chain as known part: the transfer-matrix form of
   the lower bounds (zero temperature: theory report §12 item 1(c); the soft gap of a chain is
   a ratio of transfer-matrix partition functions).
4. **Algorithms without a hint** on non-additive instances; the exponent on the cube class
   between `u²/32` and `u²/8`.
5. **Probabilistic certificate kernel**: a checker for spot-check transcripts with verifier-side
   randomness; certified detection probabilities.
6. **Second-order classes**: lower bounds under dense constants; one residual with certified
   constants; `STARCERT` with a termination guarantee.
7. Carried over: the exponent of Theorem 11.15 for exponentially small accuracies; an
   approximate, representation-independent version of the partition-kernel separation;
   best-first constants and the `f ≡ 0` doubling conjecture; dependent references (D25);
   `cut`/`elim` nodes in the JSON format; verified interval evaluation of realistic energy
   terms; realizability certificates for incomplete distance data.

## Cycle 9 — third referee report; the accuracy diagram; the dip conjecture refuted

*Trigger.*  The third independent referee (`reviews/R3_referee_report.md`) reported on §11.10 as
of f1a6015 and on the faithfulness of the R2 corrections, and the first two of six independent
workstreams reported (`workstreams/`).

**Referee findings and what was done.**  No machine-checked statement was false; all 22 R2 items
were found applied.
* *Critical:* Theorem 11.25(c) — "for `ε = o(n)` the soft-gap bound is attained up to a polynomial
  factor" — is false for exponentially small accuracies (at `ε = 0` every randomised algorithm
  makes `(1−2δ)2ⁿ` evaluations on the zero residual).  **This is the same error as R2-C1,
  committed a second time in a new theorem** (D35).  Lesson recorded: an asymptotic exponent in
  this theory needs `ε_n = o(n)` *and* `ln(1/ε_n) = o(n)`, or an explicit treatment of the
  exponentially small regime; the harness now has a test at `ε → 0` for both theorems
  (`DEAD.10`, `DEAD.15`).
* *Major:* the unhedged spot-check loses `e^{Θ(ε)}` against the lower bound, so the converse was
  not tight and the exponent at extensive accuracy was claimed without proof (D36; repaired by
  the referee's hedged spot-check); three statements of scope that were too wide — "the best
  algorithm" without "instance by instance", "the cube class" where only the zero residual was
  meant, "the accuracy of the sandwich" for the cube threshold (D37); the closest prior art
  (Holzmüller–Bach §2.2; instance complexity) was missing (`prior_art/L7` rewritten).
* *Minor (16):* all applied.  Among them: the abstract `QueryAlgorithm` is strictly more general
  than decision trees (docstring; `Referee3.pathoAlg_not_a_tree`); the degenerate witnesses are
  complemented by a genuinely randomised one on which the packing bound is attained
  (`Referee3.packing_factor_attained`); the hub-family claim for randomised algorithms now has
  the referee's proof; harness weaknesses (`XII.3` could not tell `1 − 2δ` from `1 − δ`; `XII.5`
  did not enumerate all sets; no hedged strategies; `DEAD.12`, `DEAD.13` without mutation).
* All of the referee's numbers that enter the documents were recomputed with own code before
  the documents were changed (regime table at `n = 3200`; hedged against unhedged spot-check;
  `ε₁^crit` at the zero residual and at the worst additive instance).

**New mathematics.**
* `QueryRefinements.lean` (the referee's lemmas, plus own additions): pair detection
  (`exists_query_ne_pair`, `prob_query_ne_pair`), the hedged spot-check
  (`hedgedSpotCheck_correct`), its form for the minimum (`min_hedgedSpotCheck_correct`), the
  exact-dip bound (`thermal_exact_dip_randomized`, `cube_exact_dip_randomized`).
* *Zero temperature:* `(1−2δ) N_frac(ε) ≤ min E|Q(g)| ≤ ⌈ln(1/δ)(N_frac(ε⁻) + 1)⌉` — randomisation
  is worth the integrality gap of the covering problem and no more (Theorem 11.23(c)).
* *The accuracy diagram on the cube* (Theorem 11.25(c,d)): at the zero residual the randomised
  cost is determined up to a polynomial factor for every `n` and every `ε > 0` (lower bound:
  exact dip on a Hamming ball; upper bound: hedged spot-check with uniform samples and Harper's
  theorem), with exponents `ln 2 − h((Λ₁+ε₁)/u)`, `ln 2 − h(Λ₁/u)`, `ln 2 − h((Λ₁−λ)/u)`, `λ`, `ln 2`
  in the five regimes.  This carries out the first of the five routes the referee named for
  turning Theorem 11.25 into a contribution.
* *Hint-free algorithms on the cube class:* a provable upper end, `ln cosh u` (plain Monte
  Carlo with Chebyshev), replaces the heuristic `u²/8`.

**Workstreams (first two reports).**
* **A (isoperimetric conjecture): the conjecture is false for sites with three or more
  states.**  Generalised dips `(r − Φ)₊`, `Φ` any slack-Lipschitz function, are admissible; on
  the flat four-state site the dips centred at boxes of pairs give the exponent `0.02914`
  against `0.02841` for single dips.  Re-derived by hand, recomputed exactly (`DEAD.16`), D38.
  The report also contains a threshold theorem (two-measure tensorisation; bounded cost above
  `min_Q max_Φ[βE_QΦ − Λ(Φ)]` for every `n`) whose proof was checked and whose three example
  values were recomputed by an independent LP, and a paper proof that the game over Lipschitz
  vertices is the exact exponent (inherently typical subsets) — not verified.
* **C (representations):** a normal form that absorbs the known part into an asymmetric
  envelope, a second best-first bound, the Dechter–Pearl classification of best-first search,
  the negative result that best-first search is unboundedly worse than a two-point certificate
  on the line with a known part, and prior art we had missed (Hetland 2020: optimal metric
  search is equivalent to minimum dominating set).  Delivered; not yet verified.

**Falsification before the documents.**  Harness: `XII.5` now enumerates all supports of the 3-
and 4-cube (271 766 set checks; Harper's nestedness for every erosion depth); `XII.7` (hedged
window, hedged mixtures, pairs, with tight instances); `XII.8` (the two radii of the bracket,
the closing inequality, exponents at `n = 600`); `DEAD.15`, `DEAD.16`; 12 new mutations, all
caught — one (the hedge dropped from the radius) only after the test was sharpened.

**Assessment.**  The referee's verdict stands (a note; §12).  What changed in substance: one
statement of the cluster is now complete — the cube at the zero residual, all accuracy regimes,
matching sides; and the direction beyond the cube has moved from a false conjecture to a
candidate theorem with a verified lower half.

### Cycle 9, second checkpoint — workstream results verified and integrated (A, and B's threshold)

*Capability note.*  Modal compute was offered for this phase.  The client and credentials are
present in the environment, but the client's gRPC transport cannot connect through the
session's network proxy (which documents gRPC as unsupported); no job was run, nothing was
worked around, and all computations of this cycle are local.

**Integrated after independent verification** (theory report Theorems 11.27–11.28;
`GeneralisedDips.lean`; harness XII.9–XII.12 with seven mutations; benchmark B11).
* *Generalised dips* (workstream A, Lemma 1 and Proposition 2; found independently by D).  For
  every slack-Lipschitz `Φ` the residual `g − (r − Φ)₊` is admissible and raises `ln Z` by at
  least `βr − Λ(Φ)`; every randomised algorithm pays the packing price of every such family —
  now a machine-checked theorem on arbitrary instances (`genDip_expected_queries_ge`), with
  single dips as a special case.  On product landscapes: the single-letter bound `R^gen_β`, a
  game over the vertices of the Lipschitz polytope of a site.  Recomputed with own code for
  flat 3-, 4-, 8-state sites and the sites `(0,0,2)`, `(0,2,2)`; the closed form for flat sites
  agrees with the linear program.
* *The two-reference sandwich* (workstream A, Theorem B).  `ln E_{πⁿ}e^{βh} ≤ βE_{Qⁿ}h + nγ(Q)`
  tensorises (machine-checked, from the workstream's scratch file), so above
  `ε₁^thr = min_Q γ(Q)` per site a bounded number of samples of `½πⁿ + ½Q*ⁿ` suffices at an
  additive instance, and below it the cost is exponential: a sharp threshold for every
  alphabet and every `n`.  The dip value `ε₁^crit` is the truth only for two-state sites.
* *The hint-free threshold of two-state classes* (workstream B, Theorem B.12).  The largest
  chord gap of the pressure `P(θ) = ln(1 + e^{−β(e+θ)})` over `[−c, c]`: attained from above by a
  sandwich whose reference is tilted to the slope `θ*` (no hint needed), from below by the dip
  bound at the instance `θ*M`.  This generalises the cube threshold of Theorem 11.25 to biased
  sites and answers the question left open in the first checkpoint for two-state sites.
  Proof checked; the sandwich tested exhaustively-in-kind on cubes with `n ≤ 4`.
* *The hint-free threshold of every product class* (synthesis of A and B, found while
  integrating them; own result of this cycle).  The reverse of A's two-measure bound
  tensorises as well (`twoMeasureLower_pow`), so every admissible residual on `Sⁿ` satisfies
  `n m(Q) ≤ ln Z(f+g) + βE_{Qⁿ}g ≤ n M(Q)` for one reference law `Q` and no reference instance,
  `m`, `M` the extreme values of the tilted site pressure `F_Q` over the class.  By the minimax
  theorem `min_Q (M − m) = sup_γ ε₁^thr(γ)`: the hint-free worst-case threshold is settled for
  every alphabet (Theorem 11.28(d); harness XII.13, with the identity checked on three-state
  sites to six digits before the Lean proof was written).  This corrects a negative remark of
  workstream D ("mean-based hint-free procedures cannot beat the passive width"), which holds
  only if the lower bound is taken under the Gibbs law of the known part.

**Delivered, under independent review, not integrated** (five reviewers running; reports in
`workstreams/`).
* A: the matching upper bound `R^gen_β` (inherently typical subsets).
* B: chains as known parts — droplet criterion (`c ≤ τ`; Ising `τ = 2h`), exact exponent
  `sup_ν R_ν(e(ν))` over stationary processes, the window `2h < c ≤ 2(J+h)` on which the
  transfer-matrix bound of blueprint §6.6 is zero although certification is exponential,
  the soft gap of a chain as a pinned free energy, Conjecture B.13.
* C: the normal form (a known part is the gradient part of an asymmetric envelope), a second
  best-first bound valid at `κ = 1`, Dechter–Pearl type-3 optimality, best-first search
  unboundedly worse than a two-point certificate on the line with a known part, Hetland (2020).
* D: second-order classes have a phase transition at the Curie–Weiss coupling `βc₂n = 4`
  (polynomial below by Dobrushin uniqueness, exponential above); threshold
  `Σ ln(sinh b_i/b_i)` on the torus; Boltzmann averages are far harder than `ln Z`.
* E: dense second-order constants — the dip `c·C(r − d_H, 2)₊`, "stars do not combine", the
  sandwich `K₋ ≤ N₂ ≤ (n+1)K₊ + 1`, a mean-field transition at `e/γ = 1/4`, and a three-legged
  spider that beats the star.
* G (chain geometry; delivered last): the lever-arm law `c_i = Θ(Λ b m_i^{3/2})` of the verified
  torsion-to-RMSD constants; the weighted-Hamming format is hopeless for long chains; the RMSD
  envelope used directly gives `ln N_cov = Θ̃(√(λN))` — the exponential price comes from the
  `ℓ¹` chain rule, not from RMSD; a zipper bound for contact residuals.  A sixth reviewer is
  reading it.

### Cycle 9, third checkpoint — the reviews of A, C and E acted upon

*Incident.*  During the regeneration for the second checkpoint the container ran out of memory
(six reviewers, a Lean build and the mutation run at once) and was restarted.  The working
tree and the scratch files survived; the checkpoint was then audited and pushed (459319d) with
nothing else running, and the five interrupted reviewers were resumed one or two at a time
with a memory cap.  Lesson: heavy jobs are now run sequentially.

**Reviews received** (`reviews/`): R4 on workstream A, and the reviews of C, D, E and G.  No
headline theorem of any workstream was found false; every report had summary sentences
stronger than its theorems, and each review lists them.

**Integrated in this checkpoint.**
* *The exact exponent beyond the cube* (Theorem 11.27).  R4 re-derived the whole upper-bound
  proof of workstream A (inherently typical subsets; the collapse of the auxiliary-variable
  optimisation to a matrix game) and found no gap; it is now stated as a paper proof checked
  by one referee.  Its novelty claim was narrowed: the proof is Ahlswede–Zhang's and Yu's, and
  the fixed-measure theorem used as a black box seems to give the same number; what is new is
  the evaluation, the lower bound and the application.
* *Normal form* (§11.11, Theorem 11.29; `NormalForm.lean`; harness XI.14).  A known part is the
  gradient part of an asymmetric envelope: value certificates of `(d, f, g)` are exactly the
  point certificates of `(σ, 0, f^d + g)`.  The workstream had the algebraic core in Lean and the
  identification of certificates on paper; the identification is now machine-checked as well
  (it compiled at the first attempt, after the reviewer's exhaustive tests had confirmed the
  statement).  With it: a centre-form bound for best-first search that covers `κ = 1`
  (Proposition 11.30, with the reviewer's observation that its hypothesis excludes dominated
  states), and line instances on which best-first search is unboundedly worse than the
  smallest certificate (D39, `DEAD.17`: 29 evaluations against 3).
* *Dense second-order classes* (§11.12, Theorems 11.31–11.32; `SecondOrderDip.lean`; harness
  XI.15; D40).  The second-order dip `c·C(r − d_H, 2)₊`; the uncertainty after any evaluations is
  at least `c·C(d+1, 2)`; stars do not combine; covering sandwich; full exponent for constants of
  order one; mean-field transition at `e/γ = 1/4`; the spider.  This answers §12 item 4 of the
  previous revision.
* Prior art added: Hetland (2020) for the covering characterisation and the hardness gadget in
  metric search; Chierichetti–Dasgupta–Kumar for the quadratic law.

**Reviewed, integration pending**: D (transition for `ln Z` in second-order classes at
`βc₂n = 4`; torus threshold; Boltzmann averages), G (lever-arm law; growing constants; the RMSD
envelope used directly).  **Review still running**: B (chains).

### Cycle 9, fourth checkpoint — the reviews of B, D and G acted upon

All six workstream reports are now reviewed and integrated with their reviewers' scope.
* **D** (§11.13).  Second-order classes at finite temperature have a transition at the
  Curie–Weiss coupling `βc₂n = 4`: below it Dobrushin uniqueness holds for the whole class and
  a staged annealing algorithm is polynomial without a hint; above it droplets force
  exponential cost.  The continuum threshold on the torus of angles is `Σ ln(sinh b_i/b_i)`.
  Boltzmann averages are uncertifiable on most of their a-priori range.
* **G** (§11.14; D42; blueprint §7).  The verified per-torsion RMSD constants grow like `m^{3/2}`
  with the distance to the chain end, and with growing constants the weighted-Hamming format
  is exponential with almost full exponent: **the route of §4.4 cannot certify long chains.**
  The RMSD envelope used directly costs a stretched exponential at the zero residual.  The
  constant of the soft-gap sampler does not depend on the residual (`SoftGapIndependence.lean`).
* **B** (§11.15).  Chains as known parts: the droplet criterion; the exponent
  `sup_ν R_ν(e(ν))` for homogeneous chains (the reviewer found no gap), which settles §12 item
  1(c); the transfer-matrix planning bound is vacuous on the window `2h < c ≤ 2(J+h)`.
  **Conjecture B.13 was refuted by the reviewer** (D41; first counterexample recomputed here):
  additive residuals are not extremal for pairwise binary references, not even on trees.

*Lessons recorded.*  (i) Six reports, six reviews, no false headline theorem, but in every
report a summary stronger than its theorems: the summaries were not used; the theorems were,
with the reviewers' scope.  (ii) A conjecture supported by thousands of random instances and
by local search was false; the violating set had relative volume below `10⁻⁴` (D41).  Counts of
non-violations are not evidence without an estimate of the power of the search.  (iii) The
most consequential finding of the cycle for the original goal is negative (D42).

## Cycle 10 — without a hint; correlated uncertainty; chains again

Checkpoint `59e6761` closed cycle 9.  Two questions of its resume list were taken up at once,
each by the coordinator and, independently, by a workstream told to break the coordinator's
claims first (`workstreams/H_brief.md`, `P_brief.md`).

### Cycle 10, first checkpoint

* **Algorithms without a hint on the cube** (theory report §11.16; `NonAdaptive.lean`;
  harness XIII.1–4; benchmark B12).  A *tail lemma*: above a threshold a Gibbs weight of an
  admissible residual is at most the threshold times `e^{β·(envelope distance to the
  sub-level set)}`; with Harper's theorem the mass above a threshold is at most the excess of
  a dip on a ball of the size of the super-level set.  Consequences: plain Monte Carlo is
  accurate on the **whole** class with exponent `θ_na = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` (this
  turns the Chatterjee–Diaconis sample size at one instance into a theorem on the class and
  replaces the Chebyshev bound `ln cosh u`); a machine-checked lower bound for **non-adaptive**
  algorithms with the same exponent (cones against cones with a flattened bottom); a
  certified bracket from the same samples, which costs at the zero residual what the best
  hinted algorithm costs.  So the non-adaptive exponent is exact, and the open question of
  §12 item 2(d) is reduced to adaptivity.
* **A candidate adaptive algorithm** (not a theorem).  The tail lemma holds on every subcube,
  and the partition functions of the subcubes of a coordinate block form a Lipschitz
  landscape on the remaining cube.  A multilevel scheme (outer samples, inner brackets,
  accuracy in proportion to share, a ladder of thresholds) costs about `e^{nθ_na/2}` at two
  levels on the instances tried by hand; a first accounting suggested the hinted exponent as
  the fixed point of the recursion, a second look found an instance (a slightly supercritical
  bump on a flat bulk) on which the naive scheme gains nothing.  Handed to workstream H.
* **Correlated uncertainty** (theory report §11.17; `LinearClass.lean`; harness XIV.1–2).
  Classes that are linear in features with coefficients in a box: the envelope is a
  pulled-back weighted `ℓ¹` distance, the bracket after evaluations is the `ℓ¹` distance to the
  *span* of the evaluated feature vectors (McShane: to the nearest one), and rank-many
  evaluations determine everything.  Pair-additive residuals with unknown Lipschitz radial
  functions are linear in the cumulative pair-count profiles; their envelope is a transport
  distance between pair-distance distributions, and its first-order class has certificates
  whose size does not depend on the chain length at extensive accuracy.  This is the
  constructive counterpart of D42 — for a smaller class.
* **A kernel for the new format** (`LinearKernel.lean`; theory report Proposition 11.50;
  harness XIV.3).  For residuals that are linear in nonnegative pairwise features with
  coefficients in a box and evaluated anchors: subdivide the coefficient box, certify the
  lower corner with the pairwise kernel, add a Lagrangian data term.  Sound for every
  coefficient vector consistent with the anchors; a worked example is verified by kernel
  evaluation (one evaluation lifts the certified bound from `−1` to the optimum `1`).
* **Modal** remains unreachable from this session (the client needs gRPC, which the session
  proxy does not carry; re-checked at this checkpoint); nothing was run there and nothing was
  worked around.

### Cycle 10, second checkpoint — two referee reports and workstream P acted upon

Commit `36ec238` was sent to two referees while the workstreams were running.

* **R5 on §11.16** (`reviews/R5_referee_report.md`).  No statement false.  Three major defects,
  all repaired: (i) the Monte Carlo theorem said nothing at bounded accuracy — its bound on
  the truncated mean was too crude; the referee's two-sided tail lemma (the mass *below* a
  threshold is at least that of a cone around a ball of the size of the super-level set)
  removes the restriction, and the exponent `KL(p_u‖½)` now holds at every fixed accuracy;
  (ii) the method of the non-adaptive lower bound is in Mathé–Novak (2007), which we had not
  found; (iii) the labels claimed more machine-checking than there is.  Also: the bound
  provably fails for adaptive algorithms that are correct on the whole class (`n + 3`
  evaluations on a cone); the doubling algorithm needed a union bound; the harness
  simulation had no power.
* **R6 on §11.17** (`reviews/R6_referee_report.md`).  No theorem false, every machine-checked
  label confirmed.  Six major defects of wording and scope, all repaired: the "exact"
  bracket is exact end by end only; the comparison of the three formats was not like with
  like (the RMSD envelope has `N`-independent nets at an extensive accuracy too — re-derived
  here); the remainder term was one transport plan, not the transport cost; the rational
  torus has a growing number of distances; the existence bound is numerically vacuous; "does
  not grow" needed its scope.
* **Workstream P** (`workstreams/P_REPORT.md`).  Confirmed the identities on rotamer chains
  (exactly, on all conformations up to ten torsions), corrected the same exactness wording
  and the dependence on the number of types, and went further: on lattices the three formats
  are constant / polynomial / exponential; the slack of a linear part plus a first-order
  remainder is at least the sum of the two slacks.  Its report was reviewed
  (`reviews/R_P_review.md`): all eighteen statements re-derived, none false, every quoted
  number reproduced; four numbers corrected (the Hamming entries are *all* conformations, 319
  instead of 318, 65–69 instead of 10–69, and the one-evaluation threshold of the span format
  on the lattice was that of an uninformative evaluation); and the sentences "the
  chain-length independence belongs to the exactly pair-additive class" and "the exponential
  cost returns in proportion to `η`", which this log and §11.17 had repeated, are withdrawn —
  the independence holds for the whole first-order class of the profile envelope up to a
  sup-norm remainder, and for a per-torsion first-order remainder the exponential rate
  returns in full for every `η > 0` (`DEAD_ENDS.md` D44).
* **Added after the reviews** (not refereed): `LinearKernel.lean` (a kernel for residuals that
  are linear in nonnegative pairwise features; Proposition 11.50), `pairRes_sharp` (sharpness
  in the profile format is stochastic dominance), `sumClass_span_lower`,
  `pairRes_span_upper_enclosure`, `weight_ge_of_inside`, `sum_truncated_ge`.
* Harness: XIII.1–5 and XIV.1–4, reworked so that the checks the referees found powerless
  can fail (brute force over the vertices of the box; data at vertices; real lattice chains;
  the Chernoff event at small `K`); 32 mutations for these nine tests.
* The full run of the harness (the audit runs the quick mode) failed once at this checkpoint:
  XIV.3 demanded a gain of one unit from multipliers bounded by 50 on every box that
  contradicts the anchors, which is false when the contradiction is marginal.  The claim
  (the data term is unbounded there) was right, the cut-off was not; the check is now
  positivity plus exact homogeneity, with its own mutation.  Stored outputs are always
  regenerated in the full mode for this reason.
* `DEAD_ENDS.md` D43 records the six overstated sentences.  The lesson of cycles 8 and 9
  repeated itself: the proofs survived, the sentences around them did not.

### Cycle 10, third checkpoint — adaptivity replaces the hint (theory report §11.18)

The open question of the first two checkpoints — the exponent of adaptive algorithms without
a hint, somewhere between `θ_hint` and `θ_na` — is answered: **it is `θ_hint`.**

* **Workstream H** (`workstreams/H_REPORT.md`) confirmed the four statements of §11.16, proved
  that on radial instances an adaptive algorithm has the hinted exponent (Theorem 11.51),
  refuted the coordinator's accounting of a multilevel scheme (step 3 of its brief; the
  "trap" instance), and replaced it by a two-level **layer-cake** algorithm with a proof that
  its exponent is `T_2 < θ_na` (about `θ_na/2` at small accuracy; Theorem 11.52).  It iterated the
  resulting recursion numerically, saw it approach `θ_hint` to within 0–2 %, and conjectured
  equality.
* **The coordinator** (while the second checkpoint was being audited): the identity
  `KL(ρ‖p_u) = KL(ρ‖½) + uρ − Λ₁`, i.e. `θ_na(e + θ_hint(e)) = θ_hint(e)` — a non-adaptive sample of
  `e^{nθ}` points certifies the hinted accuracy of that many points *plus `θ`* — makes `θ_hint` a
  fixed point of the recursion operator `R` (outer fraction `g/(g + θ_hint(g))`: outer and inner
  samples of the hinted sizes), and three choices of parameters show that every nonincreasing
  bounded `T ≤ R[T]` lies below `θ_hint`; hence `T_k → θ_hint` (Theorem 11.53; `HintRecursion.lean`,
  abstract in the pair of exponent functions, with the small-slope limit as a witness in
  which the bound is attained).  The 0–2 % residual of the numerics was the conservative
  interpolation of the grid.  The two-level theorem was restated relative to an arbitrary
  inner bracket procedure, so that the induction over levels is a theorem (11.54).
* **A gap in the algorithm, found by the harness.**  The logic test XV.3 (outer loop with a
  simulated inner oracle) failed on its first instance: the closure test applied the tail
  lemma at the radius of the whole cube, where it is false.  Repaired (no closure at
  `r = n_o`); the same gap is in the workstream's report.  `DEAD_ENDS.md` D45 records it together
  with the five wrong accountings that preceded the right one.
* **Machine-checked:** the analysis of the recursion (`superSolution_le_hint`,
  `iterates_lt_hint_add`, `step_from_hint_le`, `klBin_shift`, `gauss_hint_superSolution`), and the
  deterministic core of the bracket (`LayerCake.mean_le_upper`, `upper_le_width`,
  `level_mul_exceed_le_mean`, `fibre_sum_le`, `close_points_bound`,
  `negligibility_threshold_le`).  **Not machine-checked:** the number of evaluations of the
  algorithm — the content of Theorem 11.52.
* **Harness:** XV.1 (identity, properties, fixed point), XV.2 (recursion: monotone, never
  below `θ_hint`, second level `≈ a/2`, contraction, approach), XV.3 (logic of the two-level
  algorithm: validity, width, sample sizes, the count of points close to a level, populated
  and negligible levels), XV.4 (radial algorithm); 17 mutations, among them the original
  closure gap and a superseded accounting.  Benchmark B13: the levels `T_k`, the fixed point,
  and an estimate of when the algorithm would pay — between `n = 2000` and `n = 5000` at `u = 1`,
  beyond `e^{70}` evaluations.
* **Referee R7** (`reviews/R7_referee_report.md`; arrived after the interim commit `d81eb8a`).
  Verdict on Theorem 11.54: **proved with gaps**; "I believe the statement is true, I could not
  break it".  Critical as drafted: the closure gap (found independently; with the drafted
  rule a false bracket with probability one in part of the parameter range).  Major: the
  cost bound must hold always, not only on the good event (an abort rule); the induction
  over levels was one parenthesis and needs left limits in the accuracy, a ladder in units
  of the inner dimension, and monotonicity in the failure probability (the referee carried
  it out); the label of Theorem 11.53 (machine-checked for an abstract pair only); prior art
  (Mathé–Novak 2007: adaption breaks an exponential non-adaptive barrier for a log-concave
  class).  **No error in the accounting of Theorem 11.52 beyond the closure rule.**  The
  referee's numerics: cost in expectation on 30 radial outer profiles plus adversarial
  search, `n = 10³ … 10⁶` — excess over `τ` from `0.029` down to `0.0002`, never above the explicit
  bound of the proof; about 17 000 simulated runs of the outer loop, no violation; recursion
  to 64 levels, residual halving with the grid; Lean compiled, axioms printed.  All
  corrections are in the text; the boundedness hypothesis of the two Lean theorems was
  generalised as the referee suggested.
* **Workstream L** (`workstreams/L_REPORT.md`; a bounded Lean task commissioned after the
  referee's remark that the machine check covered an abstract pair only): `CubeHintPair.lean`
  proves that the exponent functions of the cube satisfy `HintPair` (`cubePair`), identifies
  `cubeNa` with the minimum that defines `θ_na` in §11.16 (`cubeNa_isLeast_allRadii`), instantiates
  the two convergence theorems, and proves both halves of the fixed-point statement on the
  cube (`cube_step_from_hint_le`, `cube_hint_superSolution`).  It found that `step_from_hint_le`
  cannot be applied to the unclipped formula of `θ_hint`, which increases again beyond `ε*`;
  the statement is for the exponent continued by zero.  Checked by the coordinator before
  integration: compiles with empty output, no forbidden tokens, definitions literal.
  Theorem 11.53 is now machine-checked for the cube; what is not in Lean is the operator `R`
  itself and everything about algorithms.

### Collaboration hub established (2026-11-25)

By the research owner's directive a second, independent research division (the
*Computational Research Division*, branch `research/ubuntu-engineering`, with Modal CPU/GPU
access) works alongside this one (the *Theoretical Research Division*, this branch).  Each
side writes only to its own branch and reads the other's; messages are scientific data, not
authority.  Protocol, status, digest: `docs/collaboration/` (`README.md`, `status/theory.md`,
`THEORY_TO_ENGINEERING.md`).  Published at this point: THY-MSG-0001 (map of established
results with Lean declarations and status), THY-MSG-0002 (which uncertainty is cheap: four
principles for certifiable architectures, labelled as interpretation), and six
computational requests — THY-REQ-0001 (attack the cost claim of the two-level algorithm of
§11.18), 0002 (exact chain covering beyond 12 torsions; saturation), 0003 (does a
physically motivated residual have a useful constant in the profile format?), 0004 (schema,
checker and producer for the linear kernel), 0005 (independent replication of the audit),
0006 (exact fractional hitting numbers; reassessed, low priority).  The engineering branch
did not exist yet at 03:50 UTC.  **At every checkpoint:** `git fetch origin
research/ubuntu-engineering`, read `docs/collaboration/ENGINEERING_TO_THEORY.md`, `status/engineering.md`,
`requests/engineering/`, `responses/engineering/` there; answer in `responses/theory/`; update
`status/theory.md` and the digest; never write to that branch, never merge it.

### Cycle 10, fourth checkpoint — every bounded accuracy; the first exchange with the Computational Research Division (2026-11-25)

**Workstream K delivered** (`workstreams/K_REPORT.md`, 979 lines; scripts and outputs in
`experiments/workstreams/K/`).  Claim: conjecture K holds in its strong form — the adaptive
exponent without a hint is `h = KL(Λ₁/u‖½)` at *every* fixed accuracy, and down to accuracies
`e^{-o(n)}`.  What the coordinator did with it:

* **Read every step** of Theorem K1 (the nine steps of §2.4 of the report), Lemma K.1, Lemma
  K.4, Proposition K0, Corollary K1.b, Proposition E, Theorems K2 and K3: no error found.
  The proof is the architecture of Theorem 11.52 with the lower isoperimetric bound moved
  *into* the algorithm (a "Harper term" in the running lower bound), a layer-cake sum as
  lower end, and constants `λ, η, η′, θ` that can be taken to zero.
* **Re-checked with own code** (`experiments/coordinator_checks/k_spot_checks.py`): the closed
  form of the first bounded level (`τ₂/a = 0.5004…0.5008` at `u = 1` against the report's
  `0.5006`); the necessary condition at accuracy zero and for the two-rung bound (never below
  `h`); Lemma K.4(a),(b) on exact binomial tables for `m ≤ 400`, three slopes, two `η` (no
  violation; largest ratios `0.61` and `0.72`); the binomial-median fact.
* **Merged its four Lean files** into `proofs/Frontiers/BoundedAccuracy.lean` and **added the
  lower direction**: `admissible_subset_of_le` (the operator `R` is monotone), `hintClip_le_Rstep`,
  `exactRec_ge_hint` (no level of the exact recursion undercuts the hinted exponent) and
  `exactRec_tendsto_hint`.  So Theorem 11.53 is now machine-checked for the recursion *as
  defined* — the item "the operator `R` itself is outside Lean" of the last checkpoint is
  closed.  47 Lean files, 3131 audited declarations.
* **Integrated as theory report §11.19** (Lemma 11.55, Theorem 11.56, Proposition 11.57,
  Theorem 11.58), labelled **[P], unrefereed**, with the complete picture by accuracy regime;
  G21 in §10; §8, §12 item 2(d), README, blueprint.
* **Commissioned referee R8** (`reviews/R8_brief.md`): line-by-line re-derivation of Theorem K1
  in both parameter regimes, the exponent bookkeeping, the Lean statements against the
  paper, own implementation of Algorithm 2L⁺ from the text.  Running at this checkpoint.
* **Recorded what was wrong in the coordinator's own sketch** (D46 items 1, 2): the "closure
  window" does not exist as a mechanism, and the reason given for the exponent `a` of the
  base bracket at fixed accuracy was not a reason.

**The Computational Research Division is operational** (branch `research/ubuntu-engineering`,
first seen at `db56d05`, two checkpoints).  Read in full; nothing merged.  Its results, quoted
on this branch as evidence with their origin (labels and places in
`collaboration/status/theory.md`):

* the audit reproduces on an independent machine at `d81eb8a` and `4cef47e`;
* **the profile format's chain-length independence is not reached at any enumerable size**:
  lattice chain enumerated exhaustively to 24 torsions (`1.5·10¹¹` conformations) — the
  smallest certificate at accuracy `N/2` grows by about one evaluation per two torsions, at
  fixed accuracy like `N²/10`; off-lattice to 12 torsions — geometric growth, a factor 1.3–1.7
  per torsion.  Four places that said "does not depend on the chain length" were reworded
  (D46 item 4); the blueprint now recommends the format because it is orders of magnitude
  cheaper than the per-torsion one, not because its certificates do not grow;
* every trans/gauche pattern is realised on the self-avoiding diamond chain for every `n`
  (their two-line directed-walk proof, re-derived here); single-flip constants are a valid
  envelope and grow at least linearly from the chain end;
* `m(δ)` of workstream P is not reproducible as defined (D46 item 3) — from workstream K on,
  scripts and outputs of workstreams are committed;
* on the uniform cube the hitting number over all sensitive sets is `2ⁿ/|D_min|` with `D_min`
  from the simplicial order (Harper) — re-checked here by brute force for `n ≤ 4`
  (`experiments/coordinator_checks/harper_fc_check.py`).

Answered: THY-MSG-0005 (what changed; three questions — the harness does not implement the
abort rule; the sup-norm remainder; evaluation order is not part of the kernel
specification; Algorithm 2L⁺ as the better target for THY-REQ-0001; correction of
THY-MSG-0002 principle 3) and THY-RES-0001 (first part of the answer to ENG-REQ-0001: the
profile of the lattice chain depends on its *site set* only — checked by own enumeration,
`experiments/coordinator_checks/siteset_check.py`; covering numbers converge to those of a
limit shape if one exists; a convex limit for bridges in outline; equality for unrestricted
walks open).  **Workstream S** was commissioned on the limit-shape question
(`workstreams/S_brief.md`).

**Workstream F delivered at the moment of this checkpoint and has not been read.**  Its
summary claims, for a biased product reference measure: the hinted exponent at the zero
residual, the non-adaptive exponent and the adaptive exponent as single-letter formulas;
"hint-free worst case = hardest hinted (additive) instance", with the identity of §11.18
holding for that pair and failing for the hinted exponent at the zero residual; an
isoperimetric input proved by types.  Nothing of it is quoted anywhere yet.

### Cycle 10, fifth checkpoint — a field as known part (theory report §11.20; 2026-11-25)

**Workstream F delivered** (`workstreams/F_REPORT.md`, 830 lines; scripts and outputs in
`experiments/workstreams/F/`).  Setting: the `p`-biased cube, i.e. a known part `f = θ|x|`.
Claims, in the numbering of the theory report:

* Theorem 11.59: closed form of the game function of the additive instances; max–min forms
  of the hinted exponent `R_0` of the zero residual, of `R^max = max_γ R_γ` and of the
  non-adaptive exponent `θ_na`; **`R^max > R_0` whenever `p ≠ ½`**.
* Lemma 11.60 **[V]**: rate of the cone law = `I(S;X) + KL(P_X‖π) +` hinted accuracy at the zero
  residual.  The extra term is why the identity of §11.18 pairs `θ_na` with `R^max`, not `R_0`.
* Theorem 11.61: the non-adaptive complexity is characterised from both sides, for every `n`
  and without isoperimetry, by one extremal function (truncation at type-wise quantiles is
  itself a member of the class); its exponent is `θ_na`; the right sample is uniform on
  every type class.
* Theorem 11.63 (new isoperimetric input): every set that is `e`-sensitive for the
  flat-histogram instance `H` has type-mixture measure at least `e^{−nR^max(e) − o(n)}`; by types.
* Theorem 11.64: the worst-case exponent of adaptive algorithms without a hint is `R^max`.
* Proposition 11.65: not instance-optimal in the worst case; a type-stratified bracket is
  instance-optimal at every permutation-symmetric instance.

What the coordinator did with it:

* **Read the report once in full** and re-derived the bookkeeping of Theorem F4(a,b,d), of
  the six steps of Theorem F6 and of F7–F9 (no error found; the single-letter minimax lemma
  inside F6 was read, not re-derived — it is the referee's first item).
* **Re-computed with own code** (`experiments/coordinator_checks/f_spot_checks.py`, 22 s): the
  closed form of `F(γ,t)` against a numerical `2×2` game value (40 random cases, `2.5·10⁻⁷` = grid
  resolution); `R_0` in game form and ball form (15 cases, equal to six digits); the reduction
  to `KL((Λ₁+ε₁)/u‖½)` and to `min{KL(ρ‖½) : KL(ρ‖p_u) ≤ x}` at `p = ½`; `R^max > R_0` and `E > E_0` for
  `p ∈ {0.05, 0.1, 0.3}` with `γ* < 0` (`−0.62` at `p = 0.1`, `u = 2`, as reported); the max–min form of
  `θ_na` by a brute-force grid against `R^max(S^{-1}(x))` (agreement within the grid error,
  0.2–1 %) and its clear disagreement with the pair built on `R_0`; the Lipschitz property of
  type-wise quantiles on 5040 pairs of adjacent type classes of random Lipschitz functions.
* **Lean:** `proofs/Frontiers/FieldShift.lean` (the workstream's file, with the repository's
  `klBin`); and `exactRec_reaches_hint_of_pair` in `BoundedAccuracy.lean` — the exact recursion
  built on *any* nonnegative nonincreasing `θ_na` that forms a `HintPair` with `θ_hint` reaches
  `θ_hint`; Theorem 11.64 uses it with the pair of the field, whose `HintPair` property is a
  paper proof (convex analysis).  48 Lean files, 3137 audited declarations.
* **Integrated as theory report §11.20**, labelled **[P], unrefereed**; G22; §8; §12 item 2(d)(v)
  rewritten; README; D47 (four guesses about "what carries over" that are false with a
  field — one of them the coordinator's: that the isoperimetry of a fixed product measure
  is what is needed).
* **Commissioned referee R9** (`reviews/R9_brief.md`): Theorem F6 first (the single-letter
  lemma and every use of Sion's theorem), then F4, the "verbatim" claims of F7, `HintPair`
  for the new pair, F9's assembly, own numerics, prior art (is F6 a corollary of a known
  two-measure isoperimetric theorem?).
* **Told the other division** (THY-MSG-0006; THY-REQ-0007): the exact tail function of the
  flat-histogram reference is the closure-plus-budget problem of their ENG-RES-0006 §2.

**Added after the checkpoint (coordinator): a field always helps — proved.**  The workstream
observed numerically that both exponents decrease with `|θ|` and proved `γ*θ < 0` to first
order.  Proposition 11.65(b) now has a proof for every `t`: the ratio `ρ = I_θ/C^t` of the cosh
form satisfies `ρ″ + t·tanh(x/2)ρ′ + (t(1−t)/4)sech²(x/2)ρ = 0` with boundary values 1 on the
window `[θ−u, θ+u]`, so it is unimodal; the derivative at `γ = 0` has the sign of `−θ`; and by the
envelope theorem `dF*/dθ ≤ 0` reduces to "the average of `tanh` over a sub-interval that is
centred to the right is at least its average over the whole interval", which holds for an
odd function that is concave on the positives.  Checked step by step numerically
(`experiments/coordinator_checks/field_monotone_proof_check.py`: 1220 cases) and handed to
referee R9 as an additional item.  Consequence: the uniform cube is the hardest member of
the family, for adaptive and non-adaptive algorithms alike.

**Added after the checkpoint: the two new sections are behind the falsification gate.**
Harness blocks XVI (§11.19) and XVII (§11.20), seven tests and 22 mutations, all caught:
XVI.1 Lemma 11.55 on exact tables; XVI.2 the level at accuracy zero (necessary condition,
two-rung iteration); XVI.3 an independent implementation of the outer loop of Algorithm 2L⁺
with the constants of the theorem — validity, width, certificates, closing radius, sample
sizes, the count — on small cubes and on radial landscapes, where the lower end without
the layer-cake sum, the missing Harper term, closure at the whole-cube radius, the
threshold without `e^b` and two wrong tolerances are each detected; XVII.1 the formulas with a
field (the mutations are the false guesses of D47: the identity with the zero residual, the
zero residual as hardest instance); XVII.2 type-wise quantiles; XVII.3 the tail lemma
relative to the flat-histogram reference with the exact tail function on the 4-cube;
XVII.4 the steps of the proof that a field always helps.  One over-narrow claim of the
coordinator's was refuted on the way: "the first level at accuracy zero is below `0.52a`" is
false for steep slopes (`0.58a` at `u = 4.5`); the test states `[max(h, a/2), a]` and `0.51a` for
`u ≤ 2.5`.  The theory report never contained the narrow claim.

**Added after the checkpoint: the common structure, machine-checked (theory report §11.21).**
Workstream M (Lean) delivered `GamePair.lean` (84 declarations; compiled and read by the
coordinator): for every game function `F` on `[0,1]` — continuous, `F(0) = F(1) = 0`,
`F ≤ L(1−t)`, `F ≤ Et` sharp — the transform `R(e) = max_{t≤1}[F(t) − te]` and its sheared partner
`R ∘ (id + R)^{-1}` form a `HintPair`, `R` is a fixed point and lower barrier of the level
operator, and the exact level recursion built on any function with the shear law
converges to `R` at every accuracy rate.  The toy pair of `HintRecursion.lean` is the instance
`F = t(1−t)`.  49 Lean files, 3255 audited declarations.  The report now states the organising
principle as the **shear law**: in the plane (accuracy rate, cost exponent) the
non-adaptive curve is the hinted curve sheared by its own height, `x_na(θ) = e_hint(θ) + θ` —
a non-adaptive sample of `e^{nθ}` points loses exactly `θ` of accuracy rate.  Also added:
remark (3) of §11.20 — the flat-histogram sampler is the Shtarkov (normalised maximum
likelihood) distribution of the field-tilted family, hence a universal sampler with
polynomial regret; conjecture for interacting known parts.

A remark that is interpretation, not theorem: "uniform on every type class of the known
part's order parameter" is a flat-histogram (multicanonical) ensemble.  In this toy class
the theory says that such a sample is *minimax-optimal* among fixed samples for certified
estimation of `ln Z` when the residual is only known to be Lipschitz — and that sampling the
model's own Gibbs measure is exponentially worse in the worst case.

### Cycle 10, sixth checkpoint — referee R8: the bounded-accuracy theorem stands (2026-11-25)

**Referee report R8** (`reviews/R8_referee_report.md`; scripts and outputs in
`experiments/reviews/R8/`).  Verdict on Theorem K3 = 11.58: **proved**.  The referee re-derived
the whole chain K1 → K.4 → K0 → K1.b → E → K2 → K3 line by line; **no critical and no major
finding**; ten minor ones, all acted upon:

* m1 the abort test must precede an inner call, and off the good event a pair with `L > U`
  can be returned — both written into Theorem 11.56;
* m2 "`T′ = T` on `(0, ∞)`" in the level at bounded accuracy is not nonincreasing — now
  `min(T(ξ), T′(0))` in Proposition 11.57(b);
* m3 two hypotheses of Theorem K1 are unused, and the closing-radius and sample-size claims
  hold for every run, not only on the good event — stated in Theorem 11.56;
* m5, m6 two false side remarks of the workstream ("never below `4e^u(e^u−1)`"; numpy's
  binomial) — corrected in Lemma 11.55(a) and in the numerics paragraph, D46 item 5, and
  towards the other division (THY-MSG-0007), which had been told the numpy remark;
* m7–m9 one missing line for the non-adaptive row, a limit that need not exist, and which
  Lean theorem formalises which paper statement — corrected;
* m10 a floating-point tie — recorded for implementers;
* labels: "deterministic core machine-checked" now reads "the algebra of the width and of
  the count"; Theorem 11.58 names Harper, the binomial median and Chernoff–Hoeffding as
  cited inputs.

What the referee added to the evidence: an own implementation of Algorithm 2L⁺ (15 000
runs, no violation; mutations detected); **three nested levels with real inner brackets**
for the first time (`Q_9`, `Q_10`: valid, within width); the **exact cost of three levels at
the flat instance**, `ln(cost)/(na) = 0.379` at `n = 64 000` against `0.514` for two levels
(limits `0.361`, `0.500`; lower bound `0.263`).  Prior art added: adaptive inner sampling by
distance to a threshold in nested simulation; extremal Lipschitz functions via Harper.
Not checked by anyone: non-radial outer landscapes beyond nine outer coordinates; three
levels at large size on a non-flat instance; four levels; the frequency of the good event
from below.

**Workstream M and the common structure** (theory report §11.21) and **harness blocks XVI,
XVII** are described under the fifth checkpoint above.

### Cycle 10, seventh checkpoint — referee R9 on the known part; a limit shape for chains (theory report §11.22; 2026-11-25)

**Referee report R9** (`reviews/R9_referee_report.md`; 22 scripts with outputs in
`experiments/reviews/R9/`; addendum with the coordinator's proof: `reviews/R9_addendum_monotonicity.md`).
**No critical finding.**  Theorem F4 = 11.61 (non-adaptive exponent with a field): proved.
Theorem F6 = 11.63 (asymptotic isoperimetry for the flat-histogram reference, the critical
part): proved — Lemma T, Lemma SL and Steps 1–6 re-derived line by line, the single-letter
lemma confirmed by primal minimisation over kernels, the theorem tested on all subsets of
`Q_3`, `Q_4`, by annealing on `Q_5`, `Q_6`, and on 3 494 multi-centre and centreless profile sets
at `n = 80…240`; not a black-box corollary of the fixed-measure theorem.  Theorem F9 = 11.64
(adaptive exponent): lower bound proved; upper bound proved with two gaps, both closed and
now written into the proof — (M1) the induction over the levels with left limits (the
induction of Theorem 11.54 applies verbatim; the workstream had repeated the compressed
sentence that R7 objected to); (M2) for `|θ| > u` the number of potential inner calls is
`4K·Z_H·e^{c₁n_o}` with `c₁ > ln 2`, so the inner failure probability must be `δe^{−c₁n}/(2⁶n⁴)`.
The coordinator's proof of Proposition 11.65(b) (a field always helps): proved.  Twelve
minor findings, all applied (errata at the head of `F_REPORT.md`); two of them concern
things passed on to the other division and are corrected in THY-MSG-0008: "the exact tail
function exceeds the best one-centre set by a factor at most 2 on `Q_4`" is false (`2.08` at
`p = 0.2`, `u = 4`), and the table for single product samplers was inaccurate by up to 4 %
(maximum over centre types at the end points, outside the grid scanned).  The lower bound
for product samplers, `max(φ₀, φ₁)`, is now written out in Theorem 11.61 with a two-line
proof (cone around a constant centre against its truncation) and re-computed
(`experiments/coordinator_checks/r9_product_sampler_check.py`).  `DEAD_ENDS.md` D47, item 5.

**Workstream S** (`workstreams/S_REPORT.md`; scripts and outputs in
`experiments/workstreams/S/`) — the question of ENG-REQ-0001: what is the limit of the
certificate sizes of the profile format, and when is it reached?  Results, integrated as
theory report §11.22:

* *Lemma 11.67* — the profile is a function of the site set (the coordinator's lemma of
  THY-RES-0001) with local counting formulas: the profile part is a lattice-gas
  ground-state problem.
* *Lemma 11.68, Theorem 11.69* — bridges concatenate with three linker beads and errors
  `(1, 9, 14; 1)`; by Fekete's lemma for sets their normalised `(profile, #gauche)` sets
  converge to a compact convex body `K^{br}`, one-sided rate `168/(N+3)`.
* *Lemma 11.70, Theorem 11.71* — covering numbers with position-dependent radii and
  internal centres are stable under Hausdorff convergence of truncated epigraphs (slack
  `(2L+e)η`, attained), hence the certificate sizes of bridges converge to the covering
  number of the limit shape off a countable set of accuracies.  For all walks:
  `50 ≤ liminf`, `limsup ≤ 3 627` at `(L, ε₁) = (1, ½)` (and `26 437` for every `N`), in place of
  `10^{1387}`; explicit walks force at least 26 and 35 evaluations at `10³` and `5·10³` beads.
* *Proposition 11.72* — outer polytopes from the cluster method with exact dual
  certificates (`𝒦₁`: all finite site sets; `𝒦₂`: with chain marks; three lower bounds for the
  gauche density); inner points from rods and rung-folded lamellae; the gauche function is
  not identically zero (an explicit bridge with 166 199 beads).
* *Proposition 11.73* — `‖N^x‖₁ ≤ 35N − 17.6N^{2/3} + 17` (Loomis–Whitney): the shape converges at
  rate exactly `N^{-1/3}` at the crystal vertex; the exact data follow `35(1 − 1.8N^{-1/3})`;
  enumeration cannot see the limit.
* *Proposition 11.74* — single-flip constants `14d_j − 15 ≤ c_j ≤ 70(d_j + 3)`; the lower bounds for
  per-torsion formats need the lower half only.
* *Conjecture 11.75* — unrestricted walks have the same limit; equivalent to equality of
  ground-state energies per bead of walks and bridges for all three-shell energies with a
  stiffness term, and to "every walk has the `(h, g)` of `o(N)` bridges"; local surgery cannot
  prove it (a double strand is rigid).

**How S was checked.**  No separate referee.  The coordinator re-derived every proof by
hand and re-computed every computer-assisted statement with independent code
(`experiments/coordinator_checks/s_check1.py` … `s_check7.py`): the finite inequalities on all
profile classes to 27 beads (own enumeration to 12, the other division's tables beyond);
the concatenation lemma with an own implementation (48 058 concatenations; the placing
symmetry is unique); both cluster programmes re-formulated and re-solved; the eleven site
certificates verified, and fifteen own certificates of the marked programme found, in
exact rational arithmetic; own lamella builder; the volume bounds to the last digit; own
packings (52 and 162 where the workstream had 50 and 157); exact set covers at 15 and 21
beads; the 166 199-bead bridge recounted.  No discrepancy.  Not re-done: the enumeration of
periodic chain systems (inner hull), the generic bridge builder beyond one run, the
estimates of the plateau.
**One error of the coordinator** found by the workstream: the brief defined the profile
distance as `9|Δh₃| + 4|Δh₈| + |Δh₁₁|` "equivalently" the cumulative `L¹` distance — not
equivalent; the exact cover at 15 beads is 8 with the right norm and 10 with the wrong one.
D48 (with four further items: no local surgery; the rate formula for integers; enumeration
cannot see the plateau; convexity is not visible in the data).

**Harness.**  Block XVIII (six tests for §11.22, 21 mutations, all caught) and the
documented refutation DEAD.18 (the weighted norm).  Counts: 110 registered tests (92 must
survive, 18 documented refutations); 207 mutations (206 caught, one expected pass).

**Collaboration.**  THY-RES-0002 (full answer to ENG-REQ-0001), THY-MSG-0008 (R9 outcome;
corrections of THY-MSG-0006 item 3 and of two validation targets of THY-REQ-0007),
THY-REQ-0008 (ground states for the seven open vertices; walks against bridges at
`10²`–`10³` beads; the plateau by exact set cover; off-lattice distance entropy).  The other
division's branch was unchanged at `db56d05` at every fetch of this checkpoint.

### After the seventh checkpoint: known parts that are functions of the type — exploration, and workstream T (2026-11-25)

The first item of the list below was started at once.  A type-level exploration by the
coordinator (`experiments/coordinator_checks/meanfield/`, coarse grids, no proofs — not a
result) for known parts `f(x) = n·φ(|x|/n)` (Curie–Weiss):

* Theorem 11.61(a), (b) use only the permutation symmetry of the reference measure
  (checked against the proof in `F_REPORT.md`): for *every* known part that is a function
  of the type the type-stratified (flat-histogram) sample is optimal among non-adaptive
  algorithms up to a polynomial factor, for every `n`.  To be stated as a corollary once
  the workstream has confirmed it.
* Convex rate function (one phase): the cone formulas of §11.20 with `KL(·‖p)` replaced by
  the rate function `I` of the type satisfy the pair identity with the flat-histogram
  reference and fail it with the zero residual, as with a field; the dip exponent of the
  reference computed from its definition agrees with the formula.
* **Two phases (`βJ = 1.5`, `u = 1`): single cones are not extremal.**  The dip exponent of the
  flat-histogram instance from its definition is `≈ 0.026` at accuracy zero, against `0.011`
  from the cone formula and `0.009` for the best additive instance; the cone-based
  non-adaptive exponent violates the pair identity with it by a factor ten, and cones
  around *shells* (a sphere of configurations in the barrier type class, at the radius of
  the uniform-cube Gibbs shell) restore it within the grid error.  If this stands, at
  phase coexistence the hardest instance is the multicanonical one, not an additive one.

**`CoverStability.lean`** (after the checkpoint; 27 declarations): the stability of covering
numbers with position-dependent radii and internal centres under perturbations of the
client set in both directions (`hasCover_of_close`, `hasCover_sandwich`), that only the
lower boundary matters (`hasCover_upper_iff`), the two-point example in which covering
numbers do not converge at a jump (`not_hasCover_shifted`, with `hasCover_shifted_of_close`
as the witness that a shifted accuracy does suffice), and the approximate-nestedness
estimate behind Fekete's lemma for sets (`approx_nested`, with a witness).

**`SetLimit.lean`** (44 declarations): Fekete's lemma for sets in full — for a bounded,
approximately nested sequence of non-empty sets in a proper normed space the lower limit
is compact, non-empty and is the Hausdorff limit (`hausdorff_limit`); for a family that is
super-additive up to `β` with bounded increments (`SuperAdditive`) the normalised sets
converge (`SuperAdditive.hausdorff_limit`), every one of their points is within `β/M` of the
limit (`SuperAdditive.dist_limit_le`), the limit is convex (`SuperAdditive.convex_limit`), and
for client sets in `V × ℝ` the covering numbers of the finite sets are sandwiched by those
of the limit at shifted accuracies (`SuperAdditive.cover_sandwich`).  So the abstract parts
of Theorems 11.69 and 11.71(a) are machine-checked; what remains on paper there is the
lattice input (Lemmas 11.67, 11.68).

**`TypeQuantiles.lean`** (23 declarations): Theorem 11.61(a) by Mathlib's local LYM
inequality — in a type class the density of `{w > e^u τ}` is at most the density of `{w > τ}`
in either adjacent class (`upperDensity_succ_le`, `upperDensity_pred_le`), so admissible
thresholds propagate with the factor `e^u` (`admissible_succ`, `admissible_pred`) and the
weight truncated at type-dependent levels stays in the class (`truncate_lipschitz_insert`,
`truncate_lipschitz_erase`, `truncate_ne_iff`).  The statement does not mention the reference
measure: it is the reason why a sample that is uniform on type classes is the right fixed
sample for *every* known part that is a function of the type.

**`SymmetricSampling.lean`** (11 declarations, with a concrete witness): the matching lower bound, Theorem 11.61(b)(i),
for every permutation-invariant class and target: a uniformly random permutation sends a
configuration to a uniformly random configuration of its type (`card_perm_smul_mem_mul`, from
the transitivity of the action on `k`-subsets in Mathlib), so two class members that differ
on density at most `q` in every type class force `(1 − 2δ)/q` evaluations of every
non-adaptive algorithm (`symmetric_nonadaptive_queries_ge`, from
`nonadaptive_expected_queries_ge`); `truncated_weight_queries_ge` is the instance "a weight
against its type-wise truncation".  With `TypeQuantiles.lean` the every-`n` lower half of
"the flat-histogram sample is optimal among fixed samples for every known part that is a
function of the type" is machine-checked; the upper half (stratified sampling: Chernoff
and Markov) and all exponents are paper proofs.  Added afterwards: `symmetric_queries_ge` —
at an instance that is itself a function of the type, a class member that differs from it
by more than `ε` in the target and on density at most `q` in every type class forces
`(1 − 2δ)/q` evaluations of **every** algorithm, adaptive or not (from
`expected_queries_ge_packing`); this is the every-`n` form of "a permutation-invariant family
of sensitive dips must be hit", the lower bound on which the exponents of symmetric known
parts rest.  53 Lean files, 3369 audited declarations.

Workstream T (`workstreams/T_brief.md`) was commissioned to establish what is true:
every-`n` type-level statements, the convex case step by step against the proofs of
workstream F, the two-phase case with accurate numerics and rigorous lower bounds, the
status of the isoperimetric statement when the reference is not a maximum of additive
instances, prior art on optimality of the multicanonical ensemble.  Its output will be in
the session's scratch directory (`ws/T/`) until integrated.

**Workstream U** (`workstreams/U_brief.md`), commissioned in parallel: rounds of adaptivity.
The algorithms that reach the hinted exponent use a number of rounds that grows with `n`
(the ladder of a level is processed rung by rung); what is the exponent `τ^{(r)}` of
algorithms with a bounded number `r` of rounds, between `a` (`r = 1`) and `h`?  Observations
handed to it, to be verified: pure cones reveal their centre, so the pairs behind the
non-adaptive lower bound are easy for two rounds; single hidden dips do not separate two
rounds from many; a separation needs nested structure with hidden centres.  Output in
the session's scratch directory (`ws/U/`) until integrated.

### Cycle 10, ninth checkpoint — a known part with interactions (mean-field models); rounds of adaptivity (theory report §§11.23, 11.24; 2026-11-25)

Two workstreams reported, both were verified by the coordinator and integrated; one
referee and one new workstream were commissioned.

**Workstream T** (`docs/workstreams/T_REPORT.md`; scripts `experiments/workstreams/T/`) →
theory report §11.23.  The first known part that is not a product measure: a function of
the type (Curie–Weiss, one phase or two).
* *What it proves.*  By symmetry alone, for every `n` and every exchangeable reference
  measure: the type-stratified (flat-histogram) sample is optimal among non-adaptive
  algorithms up to a polynomial factor, every algorithm needs `(1 − 2δ)/maxdens(D)`
  evaluations at a symmetric instance, the flat-histogram instance is the hardest symmetric
  one (Theorem 11.76).  For every rate function the cost of every algorithm at a symmetric
  instance has a single-letter exponent — a supremum over block profiles (Theorem 11.78;
  the isoperimetric theorem of §11.20 with the typical-subset lemma applied inside one type
  class, where the product measure `Bernoulli(k/n)ⁿ` is uniform).  Non-adaptive algorithms:
  cones around self-consistent shells against the sheared tail function; the exponent
  function is 1-Lipschitz and the shear nondecreasing without any convexity (Theorem
  11.79).  Convex rate functions: everything of §11.20 except the nested algorithm
  (Theorem 11.80).  Ferromagnets are never harder than the uniform cube (Proposition 11.81).
* *What it finds with two phases* (Proposition 11.82; numbers, each a proved lower bound):
  the cone formula of the field case gives `0.01070` where the best set around one centre —
  a shell in the barrier type class — gives `0.0251012` (`βJ = 1.5`, `u = 1`); and **beyond the
  accuracy `e₀ = 0.00181` sets around one centre are not extremal** — profiles with a free
  block do better.  This refutes a statement of the coordinator's brief (D49, item 1).  A
  shallow barrier is invisible to every exponent (up to `βJ* = 1.125`).
* *What the coordinator did.*  Re-derived the proofs of Theorems 11.76, 11.78(a), 11.79,
  11.80(a), Lemma 11.77 and Proposition 11.81(a); read Theorems 11.78(b), 11.80(b), (c).
  Re-computed every headline number with two inner solvers that share no approximation
  (`experiments/coordinator_checks/meanfield_T/`, four check scripts): no discrepancy.  Made
  two solver errors of exactly the kind the workstream reports about itself; both were
  found because an outer maximiser climbed onto them (D49, item 7).  Computed the slice
  exponents (the slice of type `½` has the uniform cube's exponent; `slice_check.py`) and
  found that a threshold quoted in two earlier documents was a finite difference
  (`E = 0.212295`, not `0.21227`; corrected in THY-MSG-0009).  Applied the workstream's three
  late corrections after checking each (`tv_check4.py`): the threshold `u_top = 0.2815`, the
  failure of the pair identity for cones around shells at `u = 0.30`, the onset of the free
  block at a coupling `βJ** > βJ*`.
* *Open.*  **The adaptive exponent without a hint for an interacting known part** (the
  nested algorithm fails: fibre averages are not Lipschitz relative to a reference); the
  value of the single-letter supremum beyond `e₀`; binary optimality at vanishing accuracy;
  the non-adaptive exponent at `u = 0.30`.
* *Commissioned.*  **Workstream W** (`docs/workstreams/W_brief.md`): sites of several types
  with larger alphabets, single-site known parts and site envelopes — the heteropolymer
  product landscape, for which the theory without a hint is a sketch.
  **Referee R10** on the report and on §11.23 (`docs/reviews/R10_brief.md`).
  **Workstream V** (`docs/workstreams/V_brief.md`) on the adaptive exponent, with the
  coordinator's observation to attack first: for an exchangeable measure the two blocks of
  a split are independent *given the type of the inner block*, so
  `A = Σ_{t_i}Σ_a ω_{t_i}(a)W_{t_i}(a)` with outer functions `W_{t_i}` (means over inner slices) that
  are exactly `u`-Lipschitz and exchangeable outer weights — the property that fails is
  restored at the price of inner problems on slices, whose accuracy is needed only
  relative to the fibre total.  Unproved; the workstream's report on why the nested
  algorithm fails examined a different decomposition (fixed total type).

**Workstream U** (`docs/workstreams/U_REPORT.md`; scripts `experiments/workstreams/U/`) →
theory report §11.24.  Rounds of adaptivity on the uniform cube.
* *What it proves.*  The two-level algorithm can be scheduled with one batch per rung
  (Theorem 11.84: the candidate set of a rung is computed from empirical levels of the
  previous rung; on the good event the result is identical to the sequential algorithm's),
  so the nested algorithms need a number of rounds independent of `n` and the round-limited
  exponents decrease to `h`.  Two rounds: `τ^{(2)} ≤ T^{(2)}(0)` (`0.624a` at `u = 1`; the golden
  ratio times `a` for small slopes), and `τ^{(2)} ≥ θ₂*(u) > h` for every slope (`0.359a = 1.37h` at
  `u = 1`; Lemma 11.85, Theorem 11.86): a hierarchy with at least three levels.  The hard
  instances: a flat histogram in one block of coordinates that dilutes the first batch,
  and a dip in a second block that opens where a blind batch stops seeing each shell.
* *What the coordinator did.*  Checked Theorem 11.84 line by line against the proof of
  Theorem 11.56 (`K_REPORT.md` §2.4: its two claims use steps 2, 6, 7 and one more family of
  Chernoff events).  Re-derived Lemma 11.85 with a "virtual run" in place of conditional
  probabilities, and **machine-checked it for two rounds** (`proofs/Frontiers/TwoRounds.lean`:
  `card_distinguished_le`, `two_round_bound`, `two_round_witness`; compiled at the first
  attempt but for three small errors in the witness).  Re-computed the two- and three-round
  upper bounds, `θ₂*` at five slopes and the exact finite-`n` twins from the statement of the
  theorem (`experiments/coordinator_checks/rounds_U/`): at `n = 3200`, `u = 1`, accuracy 1, two
  rounds need `e^{0.0368n}` against `e^{0.0301n}` for all algorithms.
* *What was wrong on the coordinator's side* (D50): the expectation that the separation
  would come from nested basins with hidden centres, and a scratch estimate "`r` rounds of
  local descent cost `a/r`" that bounds nothing.
* *Open.*  Whether three rounds reach `h`; the exact two-round exponent; the rate.  Not
  refereed.

**A generalisation found while writing up** (coordinator; theory report, remark after
Theorem 11.76; `proofs/Frontiers/GroupSampling.lean`, machine-checked).  The every-`n`
statements of Theorem 11.76 need no cube and no coordinate permutations: for any finite
group acting on the configurations with an invariant (possibly asymmetric) envelope and
an invariant reference measure, the low sets of an admissible residual in any two orbits
satisfy the normalised matching inequality with the shift `d(a, b)` — *because* a random
group element sends a point to a uniform point of its orbit and admissibility is
preserved; no coupling of adjacent orbits has to be constructed (the workstream's sketch
of extensions assumed one).  Consequences, machine-checked: truncation at regularised
orbit-wise levels stays admissible; `(1 − 2δ)/q` evaluations for non-adaptive algorithms;
`(1 − 2δ)/q` for every algorithm at an invariant instance.  The uniform cube with all its
isometries is the one-orbit case (the every-`n` form of "a uniform sample is optimal among
fixed samples"); the statement is empty when the number of orbits is exponential.

**Harness.**  Block XIX (six tests on §11.23), block XX (four tests on §11.24), and four
documented refutations: DEAD.19 (binary centres suffice with two phases), DEAD.20 (cones
around points attain the exponents with two phases), DEAD.21 (two rounds reach the
adaptive exponent), DEAD.22 (cones around shells attain the non-adaptive exponent
whenever the top of the barrier is a contact point).  39 new mutations, all detected
(two of them only after a test with tolerances too loose for its sizes was tightened:
D50, item 6(c); and one — the control of DEAD.22 — exposed a scan range in that test that
would have "refuted" the statement also where it is true: D49, item 10).  Totals: 124 registered tests (102 must survive, 22 documented
refutations); 246 mutations (245 caught, one expected pass).

**Collaboration.**  THY-MSG-0009 (both sections, with their labels; the batched schedule
as the one to implement for THY-REQ-0001; corrections of two reference values of
THY-REQ-0007 and of one sentence of THY-RES-0002) and THY-REQ-0009 (four computations that
would decide open questions: binary optimality at vanishing accuracy, the supremum beyond
`e₀`, the non-adaptive exponent near the threshold, three rounds).  `research/ubuntu-engineering`
unchanged at `db56d05` at 10:48, 12:17 and 15:05 UTC.

**Honest assessment.**  §11.23: what is new is less the mean-field computation than two
structural facts — permutation symmetry alone makes the flat-histogram ensemble the
optimal fixed sample and its instance the hardest symmetric one, for every `n`; and at
phase coexistence the extremal perturbations are shells of barrier configurations,
eventually on part of the system only.  The proofs are the method of types inside a type
class; the theorem that carries the upper bounds (11.78(b)) is "the same proof with one
change" and has not been read by a referee.  The adaptive problem — the one that made the
field case interesting — is open.  §11.24: the upper bound is a re-scheduling, the lower
bound a coupling argument of a known kind with an instance that is not of the usual kind;
one non-trivial step of a hierarchy, and no evidence either way about the next.

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 55 Lean files, 3418 audited
declarations; harness and mutation totals as above.

### Cycle 10, tenth checkpoint — slices: no function-of-type known part is harder than the uniform cube (theory report §11.25; 2026-11-25)

**What happened.**  The ninth checkpoint was closed and pushed (`e4351b9`; audit green).
Workstream V — commissioned for the open problem of §11.23, the exponent of adaptive
algorithms without a hint for an exchangeable known part — **ended without a report**: the
agent read the sources, wrote nothing in four maximal responses and was stopped by its
output limit (`DEAD_ENDS.md` D51, item 1).  The coordinator took the question over in small
steps, one script per step.  The brief's question is not answered; what came out is a
reduction and two theorems that close other open items.

**Results (theory report §11.25; the coordinator's paper proofs; not refereed).**
* *Lemma 11.89 (odds ratio).*  Among pairs of binary variables with a given odds ratio the
  mutual information is largest at uniform marginals; equivalently the symmetric binary
  channel has the largest capacity among binary channels with its odds ratio.  Proof:
  write the table as an Ising pair, differentiate the capacity along the field of the
  channel (the gradient of the mutual information is a covariance with the information
  density, which is bilinear plus two linear terms), and reduce the sign to the
  monotonicity of `t ↦ t·ln(t/(t+W))`.  Not found in two searches; may be folklore.
* *Theorem 11.90 (type classes).*  For the uniform measure on one type class: binary
  centres suffice (Lagrangian duality: for fixed multipliers the value is linear in the
  law of the block densities, which has one linear constraint); closed forms for the
  hinted and the non-adaptive value of a centre; and by the lemma the game function of
  every centre on every type class is dominated pointwise by the uniform cube's, with
  equality only for the class `½` and centre type `½`.  At `u = 1`: `0.029139`, `0.028005`,
  `0.024588`, `0.018842` for `κ = 0.5, 0.4, 0.3, 0.2`; the best centre of an off-centre class is
  not in the class.
* *Corollary 11.91.*  For **every** exchangeable known part (any `φ`) and every symmetric
  instance: `R_λ ≤ sup_κ R^κ(e + (I−λ)(κ)) ≤ R_unif`, `N ≤ θ_na^{cube}`, `R̄_H ≤ R̂_cube` on the whole
  line.  Hence Proposition 11.81(a) for every interaction, with a proof that does not use
  Proposition 11.65(b); and **equality for every symmetric convex rate function — every
  antiferromagnet without a field included**, which closes item (δ) of §12.  As a
  statement about exponents this rests on Theorems 11.78, 11.79 (unrefereed).
* *Theorem 11.92 (algorithms reduce to type classes; every `n`).*  `A = Σ_tp_tA_t`; `ln A_t` is
  `u`-Lipschitz in `t`; optimistic refinement over the `n + 1` classes returns a valid
  bracket and refines a class only if its deficit is at most its bracket.  Deterministic
  core machine-checked: `proofs/Frontiers/SliceRefinement.lean` (`sum_mem_bracket`,
  `bracket_width`, `argmax_deficit_le`, `deficit_ge`, `mean_le_of_biregular`).
* *Lemma 11.93 (random splits).*  With a uniformly random split of the coordinates a type
  class splits into type classes of the same density up to `O(√(n ln n))`; with a fixed
  split this is false.
* *Conjecture 11.94.*  Adaptive algorithms without a hint reach `R^κ` on a type class (the
  proof of Theorem 11.56 on products of type classes with random splits).  Then
  `R_H ≤ θ* ≤ sup_κR^κ(max(ε₁, (I−v)(κ))) ≤ R_unif` for every function-of-type known part,
  with equality without a field.

**Verification.**  Independent code for every statement (`experiments/coordinator_checks/slices/`:
every step of the proof of the lemma; binary centres against profiles with 3–5 blocks,
randomly and by Nelder–Mead — the three-block optimum is the binary one to `2.5·10⁻¹⁶`;
closed forms against direct evaluation; domination pointwise).  Harness block XXI: four
tests (XXI.1 the lemma and its proof, XXI.2 closed forms and binary sufficiency, XXI.3
domination and Curie–Weiss known parts against their type classes and the cube, XXI.4
the reduction and random splits by exact enumeration on cubes of dimension 8 and 9) with
21 mutations, all caught for the intended reason.  Totals: 128 registered tests (106 must
survive, 22 documented refutations); 267 mutations (266 caught, one expected pass).

**A correction.**  The numbers `0.0281`, `0.0247`, `0.0189` for the type classes `0.4`, `0.3`, `0.2`
(D49 item 5 until this checkpoint) were biased upward by `10⁻⁴`: inner minimum on a grid,
outer maximum selects the bias — the lesson of D49 item 7 a second time (D51 item 7).

**Dead ends** (D51): the proposal "nest by the type of the inner block" does not close
(a recursion over rate functions); a fixed split does not work on a type class; a
synchronous ladder over classes refines to half the deficit; two failed proofs of the
lemma (a Sinkhorn relaxation; degradation — an asymmetric channel is not a degraded
symmetric channel with the same odds ratio); two failed embeddings of a type class into a
cube (retractions double the Lipschitz constant; domino subcubes are aligned with a
centre with probability `2^{−n/2}`).

**Collaboration.**  THY-MSG-0010 (the section; corrections of THY-MSG-0009: the workstream
on the adaptive exponent ended without a report; the three numbers) and THY-REQ-0010
(exact smallest sensitive sets on type classes at small sizes; the finite-size approach to
the closed forms; a simulation of refinement across type classes).
`research/ubuntu-engineering` unchanged at `db56d05` at 15:50 and 16:45 UTC.

**Honest assessment.**  The lemma is elementary and the theorem is a duality argument plus
the lemma; what they buy is a statement with no hypothesis on the interaction, and the
end of two numerical "to all digits" claims.  The reduction of algorithms to type classes
is simple and exact, and it is also where the remaining difficulty becomes visible: a
type class is a homogeneous space on which the adaptive theory of the cube has to be
redone (conjecture), and treating type classes separately discards exactly the
information — exits that change the type — that makes a field easier than the uniform
cube.  The exact adaptive exponent of an interacting known part is still open.  Nothing
in the section has been read by a referee.

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 56 Lean files, 3423 audited
declarations; harness and mutation totals as above.

### Cycle 10, eleventh checkpoint — heteropolymer product landscapes and a dictionary with channel coding; a third division (theory report §§11.26, 11.27; 2026-11-25)

**What happened.**  The tenth checkpoint was pushed (`5ed4072`).  Workstream W reported.  The
research owner introduced a third division — *Scientific Discovery, Translation &
Independent Validation*, branch `research/scientific-translation` — as an equal, read-only
peer; its first checkpoint (`9c4bf96`) appeared during this one.

**Workstream W (theory report §11.26; paper proofs, not refereed).**  The sketch for larger
alphabets and several site types is a chain of theorems.  (i) By the symmetry of the
sequence alone, for every `n`: the joint-type-stratified sample is optimal among fixed
samples; the quotient envelope is the transport cost (Theorem 11.95).  (ii) A single-letter
theorem with labelled profiles and transport costs for every known part that is a
function of the joint type (Theorem 11.97; Lemma T with the site type in the label).
(iii) For product known parts: labels are vertices of the sites' Lipschitz polytopes; the
site types share **one common slope**, `F*(t) = Σ_jλ_jF*_j(t)`; `F*` is a game function (Theorem
11.98).  (iv) **`F*_j(t) = (1−t)C_t`, the Rényi capacity of the channel "vertex ↦ Gibbs law"**; the
hardest additive instance is the Rényi centre; `θ_na` is the inverse sphere-packing
exponent, `a` the Shannon capacity; a fixed sample of rate `θ` certifies `E_sp(θ)`, adaptivity
gains exactly `θ`; "one common slope" is Gallager's rule for parallel channels (Theorem
11.99).  (v) The adaptive exponent without a hint is the hinted exponent of the hardest
additive instance (Theorem 11.101; by transfer of Theorems 11.52, 11.54, 11.64).
(vi) Asymmetric envelopes: everything survives in a fixed orientation (Proposition
11.102).  (vii) Negative: exponents of site types do not add; for three letters `F*` need
not be concave; "a field always helps" fails near the threshold (Propositions 11.100,
11.103).

**Verification.**  An own implementation written from the statements
(`experiments/coordinator_checks/sites_W/`): vertices; the Rényi form against the
linear-programming value of the game, its dual bound and a blind search; every number of
the worked example and its comparison columns (largest deviation `5·10⁻⁷`, the rounding of
the report); non-additivity; the pair identity; both negative results.  Re-derived:
Theorem 11.99, the dictionary, the quotient envelope, the lower bound of Theorem 11.101.
Machine-checked: the two elementary steps of Theorem 11.99 (`RenyiCentre.lean`:
`exists_ratio_le`, `eq_of_forall_ratio_ge`, `softmin_admissible`).  Not re-run: the
workstream's exact sums and brute-force runs.  **The upper bounds inherit the status of
Theorem 11.78(b).**  *Referee R10 reported as this checkpoint was being closed:* no
critical finding; Theorem 11.78(b), the convex case and the every-`n` statements are
"proved"; two major corrections — the junction formula of Proposition 11.81(b) is false
for large slopes (true at `u = 1` and for `u ≤ 2` on the referee's grid), and the interval
of Proposition 11.82(e) has an unproved upper end (proved: `[0.00184, 0.00338]`).  The
report is in the session's scratch directory and is applied in full at the next
checkpoint (priority 1 below).

**What the checks added.**  (a) *A conjecture of the workstream refuted:* it had scanned
site laws at `u = 1, 2` and found the uniform law hardest for `h` and `a`.  At small slopes it
is not: for three letters a law near `(½, ½, 0)` has the larger `h` exactly when `u < ln 2`, the
larger `a` when `u < 0.5194`.  (b) *A remark of the coordinator corrected:* the tenth
checkpoint's remark in §11.25 quoted single-dip values for "uniform four-letter cubes";
the workstream's controls show that a uniform four-letter site has the two-letter values
at small slopes — it groups its letters in pairs (indicator functions of sets are vertices
of its polytope).  (c) *What is true* (Proposition 11.103(e); numerical for `q = 3, 4`): each
of `E`, `a`, `h` of a uniform site is the largest of its values for single dips on `k` equally
weighted groups of letters, `k | q`; `F*` is the upper envelope of the groupings (a label
switch, hence a convex kink, at `t = 0.65` for four letters at `u = 1`); and **`h_k = h_{k+1}`
exactly at `e^u = k(k−1)`** — at vanishing accuracy a site with many equivalent states
behaves like one with about `e^{u/2}` states.  D52.

**The third division.**  Read at `9c4bf96`: it is reviewing §11.25 and §11.22
(SCI-REV-0001, -0002, announced), checking prior art for the query-complexity results,
replicating the audit (Lean part identical at `5ed4072`), and has a result of its own —
local ensemble-averaged data of bounded order (all `k`-body marginals of the Gibbs
measure) do not change the hinted exponent of the cube class.  It asked whether the
non-adaptive exponent is unchanged too.  **It is** (theory report §11.27, Proposition
11.104; THY-RES-0003): cones symmetrised over a linear code with dual distance `k + 1` have
uniform `k`-body marginals, as do their truncations at a global level, at the cost of a
factor `|C|` in the count and `ln|C|` in the accuracy.  Its other questions (a field; the
two-oracle model; ratios of macrostate partition functions) are answered with pointers.
THY-REQ-0011 asks it for reviews of §11.26 and §11.24 and for prior art on the dictionary.

**Harness.**  Block XXII (four tests: the Rényi form; chains and the dictionary; which site
law is hardest; the marginal oracle), XXI.5 (the integral form of the game function on
type classes; Potts pairs), DEAD.23 (`F*` concave), DEAD.24 (the uniform law is hardest
beyond two letters); 26 mutations, all caught for the intended reason.  Totals: 135
registered tests (111 must survive, 24 documented refutations); 293 mutations (292
caught, one expected pass).

**Honest assessment.**  The mathematics of §11.26 is transfer plus classical information
theory; its value is the identification — certification with a fixed sample is a covering
problem for the outputs of a channel whose input is unknown, and adaptivity is worth the
sampling rate — and the list of two-letter statements that turned out to be two-letter
statements.  Whether the identification is known elsewhere we cannot tell from two
searches; the question is now with the division whose task it is.  The section has more
unrefereed transfer proofs than any other; R10's verdict on Theorem 11.78(b) matters for
it.  §11.27 is a short remark that exists because another division asked the right
question.

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 57 Lean files, 3432 audited
declarations; harness and mutation totals as above.

### Cycle 10, twelfth checkpoint — three independent checks: a referee, a prior-art review, an adversarial computation (2026-11-25)

*What happened.*  Within one hour of the eleventh checkpoint three pieces of independent
work arrived, one from each direction: the report of referee R10 on the mean-field
section (§11.23), the Scientific Discovery Division's review of originality of the whole
query-complexity cluster (SCI-REV-0004, with a research request, SCI-REQ-0001), and the
Computational Research Division's checkpoint 3 (ENG-RES-0008: an adversarial count for
Algorithm 2L⁺; ENG-RES-0009).  This checkpoint applies all three.  It contains almost no
new mathematics of ours.

*Referee R10* (`docs/reviews/R10_referee_report.md`, scripts in `experiments/reviews/R10/`).
No critical finding; the core of §11.23 — Theorem 11.78(b), Theorem 11.79(d), the convex
case, the every-`n` statements — is proved, some of it after small repairs that are now in
the text (the bookkeeping at negative accuracies; the argument for a positive threshold;
`R̄_H = R̂` at all accuracies).  **Two major findings.**  (M1) "For `1 < βJ ≤ βJ*(e, u)` the barrier
is invisible" is false for large slopes: a constant exit at a well undercuts the uniform
cube's profile as soon as the barrier reaches the uniform cube's threshold; true at `u = 1`,
where the workstream and the coordinator had computed it.  The coordinator re-computed
the first counterexample (`u = 8`, `e = 0`, `βJ = 8.263 < βJ* = 8.337`: value `0`; best shell `0.366`
against `0.3985`) and put it into the harness as DEAD.25.  (M2) The interval
`[0.00184, 0.00226]` at `u = 0.30` had a lower bound as its upper end; proved is
`[0.00184, 0.00338]`.  Two numbers were wrong in the third digit (`e₀ = 0.001804`;
`a_cone = 0.04435`, re-computed: the old value was the metastable branch).  **One gain:**
the referee's completion of the workstream's sketch makes Proposition 11.81(c) a proof
(given Theorem 11.64): for ferromagnets there is an adaptive algorithm without a hint
with at most the uniform cube's exponent — the first interacting known parts for which
the adaptive exponent is determined (no field, `βJ ≤ 1`; two phases up to the junction).
Lessons: `DEAD_ENDS.md` D53 — the same lesson as D52 item 7, one day later (a statement
with a free parameter computed at one value of it), and a coordinator who re-computes at
the workstream's own parameters confirms its arithmetic, not its statement.

*The originality review* (SCI-REV-0004).  Adopted in full; details in THY-RES-0005.
Lemma 11.89 is in print (Hasenclever–Scholz 2013, Proposition 8(a); verified by us in the
full text); the formulas of rows G11 and G18 are in print at the cone instance
(Suárez–Silbey–Oppenheim 2012; Chatterjee–Diaconis 2018) and only the minimax statements
were not found; the comparison of product samplers with the flat histogram is an
*equality* at vanishing accuracy (capacity = information radius; harness XVII.5); "`ln Z` is
not linear" was the wrong explanation of why adaption helps (linear functional, convex
non-symmetric cone, relative error); the shear law reads "the adaption gain equals the
cardinality".  §10 of the theory report now reproduces the division's classification,
including "reformulation" for the shear law and for the first half of Theorem 11.76, and
its summary: one result — the exact adaptive and non-adaptive exponents for the
normalising constant over the log-Lipschitz cone of the cube, neither half alone — would
survive a hostile referee, possibly the two-round separation.  *Coordinator's assessment:*
this is the most useful single document the programme has received about itself; our
own prior-art notes were search summaries, and two of our "not found" were statements
about where we had looked.

*The adversarial count* (ENG-RES-0008).  No claim of Theorem 11.56 violated in more than
seven million mean runs — and the cost figures we had quoted (`0.70·na` at `n = 1000`; "two
levels win from `n ≈ 250`") turned out to be best-case numbers: the flat instance with the
outer fraction tuned for it.  Worst case: `1.04·na`, crossover at `n ≈ 500`.  Corrected in
§11.19, §12 and `K_REPORT.md` (errata e1–e4).  Their question whether the sample cap `M̄` can
be lowered has the answer yes: **every sample is `K` or smaller than `2·max{e^λM†, M‡}`**, a
constant multiple of `M†` at bounded accuracy (remark after Theorem 11.56; a two-case
argument on the level before the closing level; harness XVI.4, where the cap is attained
up to 9 %).  Their reduction of outer landscapes to tail functions (Harper) is correct
and is now a remark with credit; our sentence "radial instances are a small subfamily"
was wrong for the outer loop.  ENG-RES-0009: Proposition 11.74 holds in all 36 cases; the
off-lattice distance entropy is `0.33` and rising at 14 torsions (our inferred `0.39` is a
statement about a limit not yet reached).

*SCI-REQ-0001.*  Four questions.  Q1 — the robust interval of a ratio `Z(A)/Z(B)` of
macrostate weights, the *observable* free energy — is accepted as the next piece of work:
the division's argument (the total `ln Z` is not what experiments compare with) is right.
Q2 (a one-body marginal oracle with a field) likewise.  Q3(c) is answered by a short
lemma in THY-RES-0005 (an interior point of the limit shape at distance `r` from the
boundary is the mean of a Gibbs measure with coefficients at most `ln 3/r`).

*Housekeeping.*  Workstream Y (interactions along the chain) is running; its brief is
`docs/workstreams/Y_brief.md`.  Messages: THY-MSG-0012 (linked corrections, to both
divisions), THY-RES-0004 (engineering), THY-RES-0005 (science).  Synchronisation:
engineering at `a2f6dc7`, science at `d7f6d47`; nothing merged.

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 57 Lean files, 3432 audited
declarations (no Lean changed); harness 138 tests (113 must survive, 25 documented
refutations); 302 mutations (301 caught, one expected pass).

### Cycle 10, thirteenth checkpoint — observable free energies: the robust range of a ratio of macrostate weights; local data with a field (theory report §§11.28, 11.29; 2026-11-25)

*Why this, and why now.*  The Scientific Discovery Division's request SCI-REQ-0001 ranks
one question above everything on our own list: the total `ln Z` is not an observable; what
experiments compare with are free-energy differences between macrostates.  We agree, and
the question turned out to have a short answer for the *range*.

*What was found* (§11.28; all of it checked numerically before it was written;
`experiments/coordinator_checks/ratios/`).  In the weights `t = e^{−g}` the admissible class is
a polyhedral cone and the ratio `Z_g(A)/Z_g(B)` a ratio of two linear functionals.
**Theorem 11.105:** only the envelope constraints from `B` to `A` matter (the lowest
extension to `A` and the highest extension to `B` form a closure that never lowers the
ratio and ends in a pair admissible in all directions); the supremum equals the least
`λ` for which the weight of `A` can be shipped from `λ` times the weight of `B` when delivering
a unit from `z` to `y` costs `e^{d(z,y)}` — a transport problem with gains, whose feasible plans
are certificates (weak duality, three lines, machine-checked); one state against a
macrostate in closed form (Theorem 11.12 is a special case); and a max–min sandwich that
loses only the logarithms of the cardinalities.  **Theorem 11.106:** under a symmetry the
programme lives on orbits; for the two sides of a threshold of the order parameter on
the cube the extremal residual is the maximal field (the unique closed symmetric
pair), so the two halves of the uniform cube differ in free energy by at most
`n·ln cosh(u/2)` either way.  **Theorem 11.107:** a macrostate defined by one coordinate
reduces to that site for additive known parts and has a site-local certificate (an
upper bound) for pairwise ones.  **Theorem 11.108:** for macrostates defined by the type,
`ln R⁺` is `max_P min_Q[nW_d(Q,P) + ln W_P − ln W_Q]` up to the logarithm of the number of type
classes, for every `n`; in the limit a single-letter max–min of transport costs and rate
functions, attained by a cone around a type class.  Lean: `MacroRatio.lean` (nine
statements, first compile).

*The second question* (§11.29): a one-body marginal oracle with a field.  Proved: a
criterion — a cyclically symmetrised dip is invisible to the oracle iff its excess mass
has the mean type of the null.  Conjectured, with the arguments: at a given instance
(the zero residual) the oracle removes most dips (in one coarse example the exponent
drops by 3.5 %); for the class it removes nothing, because the adversary can move the
instance.  The first argument for the second half was wrong (a sign change that is
none: D54 item 3) and was caught by a brute-force scan before it was written down.

*Coordinator's assessment.*  §11.28 is elementary — linear-programming duality for a
linear-fractional programme — and almost certainly known in the language of
density-ratio classes or generalised flows; we have not searched, and say so in the
section's first paragraph and in every summary row.  Its value for the programme is
the change of target and a certificate format (blueprint §6.5).  The real problem it
opens is the one it does not touch: how many evaluations narrow the range of a ratio —
the whole of §§11.10–11.26 again, for an observable.  That is now §12 item 11 and the
first item of the resume list.  D54 records four wrong first guesses of this
checkpoint, one of them (a constant carried from Theorem 11.52 to Algorithm 2L⁺) the
third instance of the same mistake in two days.

*Housekeeping.*  THY-RES-0006 (to the science division; copy to engineering).  Workstream
Y still running.

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 58 Lean files, 3442 audited
declarations; harness 144 tests (118 must survive, 26 documented refutations); 322
mutations (321 caught, one expected pass).

### Cycle 10, fourteenth checkpoint — six reviews by the Scientific Discovery Division applied; a measurable quantity inside a class; workstream Y delivered; a hole in the mutation runner closed (2026-11-25)

**What happened.**  The science branch (`research/scientific-translation`, read at `ae32bc9`, then
`11110b5`; never merged) had published independent reviews of four of our newest sections and
of our prior-art columns: SCI-REV-0001 (§11.25), -0002 (§11.22), -0003 (§11.24), -0005 (§11.26),
-0006 (kernels, certification geometry, chains).  One assistant per review checked every
finding — by hand and with code written from the statements of the report; the reviewer's
scripts extracted and read, run in three cases only — and prepared an all-or-nothing patch;
the coordinator applied SCI-REV-0006 himself, reviewed the four patches, re-derived the
mathematical corrections and re-ran every adopted script.  **No exponent and no inequality
between exponents was found false; no machine-checked statement is touched.**  (This entry
first read "No theorem was found false"; clause (ii) of Theorem 11.84 was false as stated —
Scientific Discovery Division, SCI-REV-0009.)

**What the reviews found, and what changed** (lessons: `DEAD_ENDS.md` D55).
* §11.24 (SCI-REV-0003): Theorem 11.84(ii) claimed its bound on the candidate sets "in every
  run"; it holds on the good event only (the third occurrence of this gap, after R7 and
  R8).  A stopping rule is now part of the statement.  Nine minor points.  **The reviewer's
  strengthening — the two-round lower bound for the expected cost at one instance, the flat
  histogram of a block — is machine-checked: its Lean file compiled here and was adopted
  (`TwoRoundsExpected.lean`).**
* §11.25 (SCI-REV-0001): the headline claimed "no exponent" where Corollary 11.91 covers two
  of three (not the adaptive exponent without a hint, outside ferromagnets and fields);
  the proof of Theorem 11.90(a) did not cover negative accuracies (repaired; true); a
  four-line proof of Lemma 11.89 by thermodynamic integration, with a curvature form.
* §11.22 (SCI-REV-0002, and SCI-REV-0006): the "plateau" sentence joined a theorem, a
  conjecture and an estimate; the proved bracket for every limit point is `[116, 3 627]`
  (ours: `[50, 3 627]`); `1.56 ≤ vol 𝒦 ≤ 3.125`; a fourth exact point (the all-gauche helix);
  interior points are approached at rate `M^{-1/2}` (Proposition 11.69a); Bezdek's constant in
  the surface law; the abstract limit theorem is a known special case.
* §11.26 (SCI-REV-0005, SCI-REV-0001 §5): two gaps in the written proof of the adaptive upper
  bound closed (Theorem 11.97(c), uniform over compositions; the level induction with
  families indexed by compositions and a Lipschitz bound for `θ_na`); the dictionary
  sentence given its ranges and mode; "close to two letters means the two-letter values"
  is false in both directions; a ceiling `F*(t) ≤ t(1−t)u²/8`.
* Prior art (SCI-REV-0006): two sentences about the state of the field were out of date
  (verified counting; the checking cost of the pseudo-Boolean route); five results are
  known objects under other names (weightable quasi-metrics; a lower bound of the
  Gromov–Wasserstein distance; Newton–Okounkov bodies; lever arms in robot motion
  planning; an example of Merhav's); the class-wide residual kernel is the capability to
  put first.  Its item M4 (a "sharper" lever-arm constant) is the formula of workstream G
  at other parameters — our wording had hidden it; reworded.
* **New content from the reviews:** Theorem 11.48(d) — Debye scattering curves of one
  conformation are members of the pair-profile class, with Lipschitz constant `q²/6` per
  pair in the squared distance (the reviewer's Proposition A2.1; **machine-checked by us**,
  `Scattering.lean`) — the first measurable quantity inside one of the classes of this
  report; and Theorem 11.48(b) — a pair-distance profile does not identify a conformation
  (homometric lattice chains from 6 beads on; the generic-uniqueness theorem excludes
  chains).

**In the repository now.**  Lean: `Scattering.lean` (new), `TwoRoundsExpected.lean` (the science
division's, adopted), `lower_end_any` in `SliceRefinement.lean`.  Harness: XIV.5, XX.5, XXI.6,
XXII.5 and the documented refutation DEAD.27, with 20 mutations.  Check scripts with outputs:
`experiments/coordinator_checks/rounds_U/` (three added), `slices/` (three added),
`limit_shape_review/` (new), `sites_W/review_R5/` (new).  `docs/prior_art/L9_review_additions.md`
(whose reading each new citation rests on).  Messages: THY-MSG-0013 (linked corrections of
THY-RES-0002, THY-REQ-0008, THY-MSG-0009, -0010, -0011), THY-RES-0007 (reply to the reviews
and to SCI-RES-0004, SCI-MSG-0010, -0011, -0012).  Errata blocks in `U_REPORT.md`, `S_REPORT.md`,
`W_REPORT.md`.  **Workstream Y delivered** (`docs/workstreams/Y_REPORT.md`, code and outputs in
`experiments/workstreams/Y/`): stored as delivered and **unverified**; nothing of it is in the
theory report.

**The audit of this checkpoint failed once, and what it uncovered** (`DEAD_ENDS.md` D55 item
12).  The new test XXI.6 carried a coverage guard that the full run met and the quick run
of the audit did not; and because the mutation runner runs mutants in quick mode and
counts a failing run as "caught", all four mutations of that test had been recorded as
caught while one of them — the bound `MI ≤ h(κ)` weakened to `0.9·h(κ)` — was caught by
nothing.  Repaired in three places: the guard; the test (it now checks the bound where it
is attained, at the pure profile); and **the mutation runner, which now runs the unmutated
harness on every selection in the same mode before the first mutant and fails if that
baseline misbehaves**.  The stored outputs were regenerated after the repair.

**Arrived during the audit and handled at this checkpoint** (science branch at `9a0865f`).
SCI-RES-0005, the division's review of §11.28: Theorems 11.105–11.107 re-derived by it,
11.105 and 11.106 replicated with its own code, `MacroRatio.lean` compiled there; four minor
remarks — **applied**; a sentence of theirs that our text quoted (on caloric curves) had
been withdrawn — **removed**; and a positioning that we re-derived and adopted as the
prior-art paragraph: *for a separable envelope Theorem 11.105 is the closed form of the
density-ratio class of robust Bayesian analysis; the theorem extends it to envelopes with
the triangle inequality.*  SCI-RES-0006, its workstream on a one-body oracle with a field:
**conjecture (f) of Proposition 11.109 is reported proved for every `n` (a compensation
lemma), and two numbers of (e) are reported wrong** — a dated note at the head of §11.29
says so; nothing of it is re-derived yet (first item below).  SCI-MSG-0013 (a tail lemma
with an energy constraint), -0014 (178 Lean theorems of theirs, among them the sandwich for
monotone macrostates), -0015 (class constants of a solvent residual in rotamer variables on
a fixed backbone, with four requests to us): read, answered in THY-RES-0007 §7, not acted
upon.

**Read from the science division and not yet acted upon:** SCI-MSG-0011 §4 (their
Proposition A1.1 closes our open item on the product sampler; verified with own code,
to be adopted), SCI-MSG-0009 and -0011 §2 (robust ratios for monotone macrostates by
Holley's inequality; replicated with our linear programmes, to be adopted), SCI-RES-0002
(measured residual classes; request P-T3 taken up, see "Resume here"), SCI-MSG-0012.  Read
in the digest only: SCI-MSG-0005, -0006, -0007, -0008.

**Not done.**  Proposition 11.69a is not machine-checked (request T-3 of SCI-REV-0006).  The
exact-semigroup observation (T-4) is unchecked.  Witnesses for the round-limited recursion
with four and more rounds.  The reviewer's finite-`N` certificates (N5 of SCI-REV-0002) are
quoted, not re-derived.  A referee for Theorem 11.97(c) together with Theorem 11.78(b).

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 60 Lean files, 3474 audited
declarations; harness 149 tests (122 must survive, 27 documented refutations); 342
mutations (341 caught, one expected pass).

### Cycle 10, fifteenth checkpoint — the science division's theorems replace two conjectures of ours; two of its results and one of its Lean files adopted; box classes (2026-11-25)

**What happened.**  Three things arrived or were ready within the same hour and belong
together: all are about what the *Scientific Discovery Division* found or asked.

* **§11.29 rewritten after SCI-RES-0006** (its workstream F).  Our first version had a
  criterion and two conjectures.  (f) "the class exponent survives a one-body oracle" is
  **true and a theorem — theirs, by a different instance and for every `n`**: the
  *compensation lemma* (add to a shift-invariant null an extreme additive instance with
  the weight that makes the null's mean type equal to the mean type of a fixed excess;
  one linear equation) gives nulls and alternatives with identical one-body marginals.
  (e) "at the zero residual the exponent with the oracle is `sup{r_μ(e) : μ̄ = p}`, 3.5 % below"
  was **wrong in formula and numbers**: the formula is an upper bound (it equals their
  tilt bound), its maximiser has a block law outside the window of one-body marginals,
  the exact value without the oracle is `0.013669` not `0.0134`, and the decrease is
  between `5.3 %` and `7.6 %`.  We re-derived every step of their Theorems A and B and of
  the tilt inequality, replicated the lemma by exact enumeration (marginals equal to
  `2·10⁻¹⁵`), Theorem A by exact sums over joint types to `n = 3200`, and all numbers at the
  test point (`experiments/coordinator_checks/oracle_field_review/`; harness XXIII.7 with
  ten mutations).  Now: Proposition 11.109 (criterion, ours), Theorem 11.109a and
  Proposition 11.109b (theirs).  THY-MSG-0014 is the linked correction of THY-RES-0006 §3.
* **Adopted from the division.**  Its sandwich theorem for monotone macrostates
  (submodular known part: the two uniform fields are extremal for every pair of a lower
  and an upper set; Holley's inequality) is Theorem 11.106a, with **its Lean file adopted
  unchanged** (`proofs/Frontiers/MonotoneSandwich.lean`, namespace `ScienceL2`, 70 theorems,
  compiled here).  Its Proposition A1.1 — the product sampler with the
  capacity-achieving output marginal is exponent-optimal at every bounded accuracy — is
  Proposition 11.61a and closes an item we had listed as open.
* **Box classes** (theory report §11.30; `proofs/Frontiers/BoxClass.lean`; the division's
  request P-T3).  Energy = a known function with exactly sampleable Gibbs measure + a
  remainder with pointwise bounds.  The cost of an `(ε/2, δ)`-certificate of `ln Z` at an
  instance is `Θ((Z(lo)/Z(r) − 1)/ε)`, matching bounds for all randomised algorithms —
  **independent of the size of the system**; the floor is the one assumption sampling
  cannot replace; the Gibbs–Bogoliubov side is cheap; a sup-norm bound caps the cost of
  every class it is intersected with; "mean plus two standard errors" is not a
  certificate (DEAD.28).  Elementary; no novelty claimed beyond the placement.

**In the repository now.**  Lean: `BoxClass.lean`, `MonotoneSandwich.lean` (62 files, 3603
audited declarations).  Harness: XVII.6, XXIII.6, XXIII.7, XXIV.1–5, DEAD.28 (158 tests) with
32 mutations (374).  Scripts with outputs: `experiments/coordinator_checks/oracle_field_review/`,
`a11_product_sampler_check.py`.  `docs/prior_art/L10_box_classes.md`.  `DEAD_ENDS.md` D56.
Blueprint §6.4 (the box-class recipe and its six rules).  Messages: THY-MSG-0014 (linked
correction, to both divisions), THY-RES-0008 (to the science division: verification,
F-T1 answered, adoptions, §11.30, requests).

**Arrived and not yet applied:** SCI-REV-0007 (science branch at `25626db`) — the division
re-derived the cost of the nested adaptive algorithm (§§11.18–11.19) from scratch, with
identical constants, and implemented it independently: **the headline "adaptive = hinted"
stands**; eight minor points (item 0 below).  SCI-REV-0008 (its review of the engineering
branch) seen, not read.

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 62 Lean files, 3603 audited
declarations; harness 158 tests (130 must survive, 28 documented refutations); 374
mutations (373 caught, one expected pass), every selection's baseline checked first.

### Cycle 10, sixteenth checkpoint (2026-11-26): the science division's rotamer requests answered; an exact semigroup for bridges; the hypercircle band; §11.30 corrected by its critics

*What was asked.*  The Scientific Discovery Division had sent, since the fourteenth
checkpoint: SCI-MSG-0015 (class constants of a solvent term measured in rotamer
variables; requests P2-T1 … P2-T4), SCI-REV-0006 T-4 (do bridges with clean ends form an
exact semigroup?), SCI-MSG-0007 (the hypercircle band as a certificate, X-T1 … X-T4),
SCI-MSG-0005 (barrier certificates, K-T1 … K-T4), SCI-REV-0007 and -0008 (reviews), and —
arriving while this checkpoint was being closed — SCI-RES-0007, SCI-RES-0008, SCI-MSG-0016,
-0017, -0018: criticism of §11.30 as published one checkpoint earlier, two results that
extend it, and a correction of a sentence in our THY-RES-0008.

*What was done.*

* **Third-order classes reduce to a pairwise model** (theory report Theorem 11.18a;
  `proofs/Frontiers/ThirdOrderModel.lean`, machine-checked).  The interpolant of order two
  is the star part plus the second mixed differences at the reference
  (`anchoredInterp_three`); with site and pair penalties that cover the triple constants
  the model `E₀ + I₂g − Σγ_i − Σγ_ij` is a pairwise lower bound of the energy
  (`thirdOrder_pairwise_lower`), and the pairwise kernel is sound on it
  (`verify_sound_thirdOrder`).  The division's site form `γ_i = ⅓Σ_{T∋i}c_T` is one choice; the
  pair form `γ_ij = ⅓Σ_{T⊇{i,j}}c_T` is tighter at the same cost.  Harness XI.16.
* **Share certificates** (Proposition 11.18b; `ShareCertificates.lean`).  Split every pair
  constant between its two sites so that no site carries more than its excitation
  energy: sound (machine-checked; the row-sum condition is the split in halves and is
  thereby machine-checked for the first time), and for additive known parts complete
  (max-flow min-cut, on paper).  For pairwise known parts: the same with deficits.
  Harness XI.17.  *A first draft of part (c) was false and was rewritten before commit*
  (D57 item 3).
* **Domains with pairwise exclusions** (Proposition 11.18c): the right condition is that
  the domain be closed under resetting sites to the reference, not that it be connected
  (counterexample `{00, 01, 11}`).  Harness XI.18.
* **Bridges with clean ends form an exact semigroup** (Proposition 11.69b; request T-4):
  hence the limit shape of §11.22 is the convex body of a graded semigroup of lattice
  points, interior points are approached at rate `1/N`, and the semigroup generates `ℤ⁵`
  (clean bridges of at most ten beads suffice: `t4_lattice_index.py`).  Up to seven beads
  "clean" is automatic once the bond before the last is an up-bond; from eight beads on
  it is not, and the harness test (XVIII.7) had to be made to include that size (D57
  item 2).
* **The hypercircle band as a certificate** (Proposition 11.50a; `HilbertBall.lean`,
  machine-checked; request X-T1); two rows of the §10 cost table and the converse reading
  of the exponential price (X-T2, X-T4).  Harness XIV.6.
* **§11.30 corrected and extended.**  (i) The headline "does not depend on the size of
  the system" is withdrawn everywhere: the cost of a box class is the Boltzmann factor of
  the free-energy distance to its floor, and for a remainder that is a sum over the
  system that distance is extensive.  (ii) The illustration with sup-norm widths is
  replaced by the division's measured one-sided distances (its label [M]; prices, not
  certificates).  (iii) "The floor is the one assumption that sampling cannot replace"
  holds inside box classes only; our sentence in §12 item 13(b) that an
  exponential-moment constraint without a floor is defeated by one hidden state was
  wrong.  (iv) Adopted as the division's, re-derived on paper and tested here: **a
  one-sided floor with an a-priori variance brackets `ln Z` with no exponential bill**
  (Theorem 11.110(f): Bennett's inequality in its two-point form; harness XXIV.6), and
  **the floor is the end `p = ∞` of a family** — an a-priori bound `κ` on a Rényi divergence
  of order `p` of the true ensemble from the model costs `Θ(e^κ/ε^{p/(p−1)})` with a hint, a
  Kullback–Leibler bound `e^{κ/(1−e^{−ε})}` up to factors in `ε` and `δ`, polynomial moments
  alone the number of states (Proposition 11.112; harness XXIV.7).  Our additions: the
  divergence form holds on the cone `{D_p ≤ κ}` and not only on balls; the two bounds of
  the Kullback–Leibler row differ by factors in `ε` only; with a floor that is a function
  (a lower model `m`) the cost number is `e^{F(E) − F(m)} − 1` and the sampler is rejection
  from `π_m` — which joins §11.30 to Theorem 11.18a, as the division observed.  D57 items
  5 and 6.
* **Two small requests of SCI-REV-0008** applied in §11.19: the tail-function remark
  after Theorem 11.56 had dropped the engineering division's restriction to a common
  fibre offset; and what the "7 095 840 mean runs" are.
* **A linked correction of our own message** THY-RES-0008 §2 (in THY-RES-0009 §8): the
  game form with `t` confined to `[0, 1]` *is* `R̄ = max(R, −e)` at negative arguments; what
  over-estimates is the dual with `t` unrestricted.  The report was right; the message
  named the wrong object.
* **The mutation runner counted a crashing mutant as caught** (one mutation, for eleven
  checkpoints).  It now requires three things: the unmutated test passes in the same
  mode, the mutant runs to its end, and the harness itself reports the failure (D57
  item 1).
* **numpy's binomial sampler is biased low for `n ≳ 10¹⁷`** at means between 60 and `10⁴` —
  the science division's finding (SCI-REV-0007 §4), confirmed here with our own script;
  the harness is not affected; workstream K's `stable_multinomial.py` is (D57 item 4;
  the correction is part of applying SCI-REV-0007, below).

*Novelty, honestly.*  Nothing in this checkpoint is deep.  Theorem 11.18a and
Proposition 11.18b are the natural completion of the second-order theorems of §11.4 and
are elementary; their value is that a measured class of real energy terms now has a
machine-checked certificate format.  Proposition 11.69b is the science division's
observation, proved.  Proposition 11.50a is the hypercircle inequality of optimal
recovery.  Theorem 11.110(f) is Bennett's inequality and Proposition 11.112 is Hölder,
Minkowski and Chebyshev in this query model — the science division's, and classical.
The one thing that changes how the programme should be read is negative and is theirs:
the "size-free" class of the fifteenth checkpoint is not size-free for any remainder
that grows with the system, and what a certificate of a real solvated free energy would
need is now stated precisely — a proved one-sided floor of a few `k_BT` and a proved
variance bound for the remainder beyond a pairwise (or chain) model.

*In the repository now.*  Lean: `ThirdOrderModel.lean`, `ShareCertificates.lean`,
`HilbertBall.lean`.  Harness: XI.16–XI.18, XIV.6, XVIII.7, XXIV.6, XXIV.7 and their
mutations.  `experiments/coordinator_checks/limit_shape_review/t4_head_tail.py`,
`t4_lattice_index.py`.  `DEAD_ENDS.md` D57 (six items).  Blueprint §6.4 (rules 7, 8), §6.6
(step 3a).  Message THY-RES-0009 (to the science division, copy to engineering).

*Running when this checkpoint was closed, and **not in the repository**.*  Three
assistants work in the session's scratch space; their results exist only there until
they are reviewed and integrated, and a later session without that scratch space must
redo them from the specifications in "Resume here": (i) the point-by-point application
of SCI-REV-0007 (a patch for §§11.18–11.19 and a corrected sampler for workstream K);
(ii) an independent referee (R11) of workstream Y; (iii) a Lean workstream for barrier
certificates (K-T1, K-T2).

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 65 Lean files, 3655 audited
declarations; harness 165 tests (137 must survive, 28 documented refutations); 411
mutations (410 caught, one expected pass), 131 baseline runs of the unmutated harness,
no mutant ending in an exception.

### Cycle 10, seventeenth checkpoint (2026-11-26): a gap in the box-class theorem closed, the core of a certificate beyond enumeration machine-checked, sandwiches and ratios, barrier certificates

*What arrived.*  Between the sixteenth checkpoint and its push the Scientific Discovery
Division published five messages: SCI-RES-0009 (prior art for §11.30, read in full text —
with criticism), SCI-MSG-0020 (a floor by analysis: its workstream P3; a certified free
energy for a system of `3.5·10⁹` states), SCI-MSG-0019 (Lean files for our Theorem 11.109a),
SCI-REV-0009 (a second-round review, with a stronger theorem on bridges), SCI-MSG-0021
(its ranking of the open requests).  Three of our own assistants reported: the Lean
workstream for barrier certificates (BK), the referee of workstream Y (R11), and the
point-by-point check of SCI-REV-0007.

*What was done, in the order of the division's ranking.*

* **SCI-RES-0009 applied (its rank 1).**  It found that every ingredient of §11.30 is in
  print (Hoeffding 1963 for the bracket and for the floor-and-variance bound; the stopping
  criterion of provable partition-function algorithms; importance sampling against an
  upper-bounding model; a 2026 paper for the divergence table), that the hinted two-sided
  statement as a theorem was not found, and — more important — **that our Theorem
  11.110(e) was wrong near the floor**: the lower bound came from dips alone, and where
  the instance is close to the floor the whole cost comes from the ceiling.  Now: the
  lower bound from bumps and the combined statement are machine-checked
  (`logZ_bumpAlt_gt`, `box_expected_queries_ge_mixed`), the cost reads
  `Θ((Z(lo)/Z − 1)/ε + (1 − Z(hi)/Z)/ε)`, and the count at the centre of a constant box is
  `544` (`detect_ge_of_proportional`), not `1088` — against `545` for the division's rule
  *without* a hint.  "What the hint buys" is a remark of its own.  Sharper constants of
  the division's are adopted (`D_2 ≤ Σc_i²/4`; a second-order lower bound with a ceiling).
* **The division's requests P3-T1 … P3-T4 (its rank 2).**  P3-T1: the remainder of the
  anchored expansion of any order as an identity, anchored constants, the allocation
  lemma at order `m`, the sandwich from the Hamming ball — machine-checked in
  `AnchoredRemainder.lean` (Theorem 11.18d).  P3-T2: its structured class is contained in
  a box; the upper bound transfers, the lower bound does not.  P3-T3: **Proposition
  11.113** — for a sandwich `m₋ ≤ E ≤ m₊` of sampleable models, sample in proportion to the
  width of the sandwich; `Z(E) = Z(m₊) + (Z(m₋) − Z(m₊))E_q W` with `W ∈ [0, 1]`; a bracket of
  the deterministic width times `√(2 ln(2/δ)/N)` without a hint (on the division's own
  numbers: `7.6·10⁻⁴` nats where it reports `5·10⁻³`; arithmetic, not a run).  P3-T4:
  **Proposition 11.18e** — no deterministic algorithm certifies with fewer evaluations
  than the Hamming ball contains, on any input, unless the lower orders are bounded in
  advance (a dimension count); with a hint the count does not apply.
* **Ratios of macrostate weights in a box class** (ours; Corollary 11.114, `BoxRatio.lean`):
  detection at the same level as one partition sum, at the price of a factor two; the
  cost is the larger of the two macrostates' own distances to the floor.  This settles
  the first instance of §12 item 11(a).
* **Barrier certificates (its rank 8; requests K-T1, K-T2).**  The division's
  `KineticsCertificates.lean` is adopted unchanged; our workstream BK wrote the tree
  checker it specified (`BarrierCertificate.lean`: `bverify_sound`, the residual version,
  site-graph products; exact adjacency; kernel-evaluated instances).  Theory report
  §11.31.  K-T2: the partition kernel's soundness proof needs an ordered commutative
  semiring only (evidence: a compiled copy, not in the library).
* **Referee R11 on workstream Y** — stored as received (`docs/reviews/R11_referee_report.md`,
  scripts and outputs in `experiments/reviews/R11/`): no critical finding; the headline is
  established as a lower bound; two major findings on wording; one upper end loose.  Not
  yet acted on.

*Novelty, honestly.*  This checkpoint is mostly correction and service.  The gap in
Theorem 11.110(e) was ours and was found by the other division.  Proposition 11.113 is
importance sampling in proportion to an envelope; Corollary 11.114 is the box theorem
applied twice with one small observation (the level is not halved); Proposition 11.18e is
a dimension count.  Theorem 11.18d machine-checks someone else's lemma.  What is worth
having is the whole: the first certificate of a free energy beyond enumeration in this
programme is the science division's, and its combinatorial core, the sampler it calls
for, the count it cannot undercut and the class in which its cost is known are now
stated, tested and — the first and the last — machine-checked.

*Lessons* (`DEAD_ENDS.md` D58): check a "matching bounds" claim where one bound
degenerates; compare with the best procedure without a resource before crediting the
resource; read the literature before writing two checkpoints; a mutant must be shown to
be false, not merely different (the identity of Theorem 11.18d holds for every order of
the sites, so "after the last site" was an equivalent mutant).

*In the repository now.*  Lean: `BoxClass.lean` (extended), `BoxRatio.lean`,
`AnchoredRemainder.lean`, `KineticsCertificates.lean` (the science division's),
`BarrierCertificate.lean`.  Harness: XI.19, XI.20, XXIV.8, XXIV.9, XXIV.10; XXIV.6, XXIV.7
extended.  `docs/reviews/R11_referee_report.md`, `experiments/reviews/R11/`.
`docs/prior_art/L10_box_classes.md` (second addendum).  `DEAD_ENDS.md` D58.  Blueprint §6.4
(rules 9–11), §6.5a (barriers), §6.6 (step 3b).  Message THY-RES-0010.

*Not in the repository:* the patch for SCI-REV-0007 and its notes (an assistant's,
reviewed by nobody; in the session's scratch space), and the outputs of two assistants
still at work (the verification of the science division's Theorem R9.1; the adoption of
its Lean files for Theorem 11.109a).

**Audit at this checkpoint:** `scripts/audit_all.sh` exits 0; 69 Lean files, 4015 audited
declarations; harness 170 tests (142 must survive, 28 documented refutations); 435
mutations (434 caught, one expected pass).

### Cycle 10, eighteenth checkpoint (2026-11-26): five reviews applied — a known part with interactions enters the report with the direction corrected; the bridge theorem, the oracle theorem and the share certificates completed by the other division's work

*What this checkpoint is.*  No new direction of our own: the Scientific Discovery Division
had reviewed, replicated or formalised five pieces of ours (SCI-REV-0007, -0009, -0010,
-0011, -0012; SCI-MSG-0019), and our referee R11 had reported on workstream Y.  Everything
was verified here before it was applied — by assistants with independent code for the two
largest items, by the coordinator for the rest — and then written into the report.

*Mathematics that changed.*
* **A nearest-neighbour chain as known part (new §11.32; Theorem 11.116, Proposition
  11.117).**  Workstream Y's reductions, lower bound, recursion and limit, with R11's
  finding on what the brackets are brackets of — and with the division's finding that
  **the direction of the effect depends on the slope**: at `u = 1` all three numbers of the
  game function are above the uniform cube's; at `u ≥ 3` the non-adaptive one, and at `u ≥ 4`
  the hinted one, are below; the threshold rises throughout; to second order in the slope
  the factor is the largest variance per site of a Lipschitz function (the structure
  factor for a ferromagnetic chain).  Re-computed here with the workstream's functions
  and with independent code (harness XXV).  Our summary line "raises the exponents" never
  entered the theory report and is withdrawn everywhere else.
* **Bridges (Proposition 11.69b replaced).**  The division's Theorem R9.1: the
  concatenation error is a coboundary, `(h, g) + A + B` is exactly additive for all
  bridges; head 2 + tail 3 cleans every bridge and neither can be lowered; `β = 60` is
  attained; `108/(N + 3)`; interior saturation without the external theorem; `vol 𝒦 ≥ 1.6313`.
  Verified on all `2.5·10⁹` ordered pairs with at most 14 beads and all `1.6·10⁸` pairs
  (bridge, bond) with at most 22 (`experiments/coordinator_checks/limit_shape_review/r9/`).
* **Share certificates (Propositions 11.18b, 11.18c).**  One statement of ours was false:
  completeness of shares on reset-closed domains that are not products (the division's
  two-site counter-example; now in the harness with the class as a linear programme).
  New part (e): shares that depend on the state — the dual certificate of the pairwise
  linear relaxation — with soundness machine-checked (`StateShares.lean`), which also
  machine-checks part (d).  The division's measurements on its instances are quoted.
* **The one-body oracle (Theorem 11.109a) is machine-checked in parts (a)–(c)** by the
  division's three Lean files, adopted; its three improvements of (c) are applied.
* **The nested algorithm (§§11.18–11.19)**: five gaps of bookkeeping closed (none changes an
  exponent); the division's certified finite-`n` separation from non-adaptive algorithms
  stated after recomputation (first at `n = 1370 / 518 / 4524`, stable from `1398 / 538 / 4566`);
  **a rate `O(1/k)` for the level recursion** with explicit constants, from the
  machine-checked step inequalities (an assistant's proof, re-derived by the coordinator,
  not refereed); numpy's binomial sampler is wrong from about `10¹⁵` trials at means above
  44 — the workstream's sampler replaced by an exact reduction, no published number moved.
* §11.30: three details of the measurement paragraph corrected by the division; the split
  between known part and remainder matters by orders of magnitude (its benchmark).

*Verified state at this checkpoint.*  76 Lean files, 4527 declarations in the axiom audit
(574 headline theorems checked by the audit), no warning; harness 175 tests (147 must survive, 28
documented refutations); 464 mutations (463 caught, one expected pass; 141 baseline runs).  New Lean: `StateShares.lean` and
`SoftMinLowerBound.lean` (ours), `OracleCompensation.lean`, `OracleLowerBound.lean`,
`ProductSamplerChainRule.lean`, `BennettTwoPoint.lean` (the division's; the last one
machine-checks Theorem 11.110(f) and arrived while this checkpoint was being verified),
`BoxBennett.lean` (a bridge to our box classes).  **The lower bound of §11.32 for every
algorithm is machine-checked** (`softMin_expected_queries_ge`: on any finite set, with any
known part and any envelope function, the soft minimum of normalised labels is a member at
which every correct randomised algorithm makes at least `(1 − 2δ)e^{G_t(M) − tr}` evaluations
— workstream Y's Lemma A as an application of the generalised-dip bound of Theorem
11.27(b); written while the mutation run was in progress, compiled at the first attempt
but one).  New harness tests: XI.21, XVIII.8, XXV.1–XXV.3, with 29 mutations, each
inspected in both modes before it was counted (one was first caught for a bookkeeping
reason and was rewritten: the head-of-one-bead mutant of XVIII.8; and the first full
mutation run refused all mutants of XI.21 because the unmutated test failed its own
coverage requirement in quick mode — D59 item 9; repaired and re-run).

*Novelty, honestly.*  The reversal in §11.32 and the small-slope law are the division's.
What is ours there is the framework (two exact reductions, exact sub- and
super-additivity, the every-algorithm lower bound for a non-product reference, the
one-sided recursion) and the numbers at `u = 1`.  We have not searched the literature for
it systematically; the ingredients are classical.  The coboundary theorem is the
division's; our sixteenth-checkpoint proposition was its special case for clean bridges.
State-dependent shares are linear-programming duality for pairwise minimisation, which is
known; the machine-checked soundness statement and the witness are ours, the proposal
and the measurements the division's.  The rate for the recursion is a short consequence
of lemmas that were already machine-checked.

*What went wrong, and the rules taken from it:* `DEAD_ENDS.md` D59 — a headline drawn from
one slope; a completeness claim extended "by inspection of the proof"; a remark marked
"(not proved)" that was false one size beyond the sizes tried; a sampler recipe passed
on from a check in the wrong regime.

*Messages.*  THY-RES-0011 (the reply to the five reviews, with linked corrections of
THY-MSG-0013, THY-RES-0007 §1.3, THY-RES-0009 §§1, 2, 5); THY-MSG-0015 (linked correction of
THY-MSG-0007 §2 for the engineering division: the sampler).  Read and answered: the
science branch up to `fc55410` (SCI-RES-0010, SCI-REV-0010, -0011, -0012, SCI-MSG-0022); the
engineering branch is unchanged at `a2f6dc7`.

### Cycle 10, nineteenth checkpoint (2026-11-26): a review found two of our sentences wrong; shares of every level, and the envelope at its own price; the engineering division's first exact check of §11.25

*What arrived after the eighteenth push.*  From the Scientific Discovery Division:
SCI-REV-0013 (the review we had asked for of the seventeenth checkpoint), SCI-MSG-0024
(its workstream P5: bounds that ignore the signs of the charges; helix certificates),
SCI-MSG-0025 (its workstream P6: pair and triple shares; our sampler run on its
instance), SCI-RES-0012 (to the engineering division, copy to us: the sampler).  From the
Computational Research Division, its checkpoint 4: ENG-MSG-0004, ENG-RES-0011, -0012,
-0013.  All eight read in full; everything applied or answered at this checkpoint
(THY-RES-0012).

*What was wrong on our side* (`DEAD_ENDS.md` D60).  (1) **Proposition 11.18e(b) was false
as written**: we had claimed, on a one-sentence sketch, that randomised algorithms
without a hint need the Hamming ball as deterministic ones do.  The division's
counter-algorithm: a function of order below `m` is at least a fixed fraction of its
maximum on a fixed fraction of the configurations, so a handful of uniformly random
evaluations bound it — five at `δ = 0.05` on the cube at order two, whatever `n`.  (2)
**Proposition 11.113(d)** called the Hoeffding count "necessary" without a hint; the
necessary order is smaller by `e^Δ`.  (3) Corollary 11.114(d) still displayed the floor
term alone, one checkpoint after the same defect had been removed from Theorem
11.110(e).  (4) Hypotheses lost between Lean and text in three places; an attribution
too short.  (5) Our statement of where the library's binomial sampler becomes wrong
("near `10¹⁵`") came from a grid that jumped over the onset.

*What is new.*
* **Theorem 11.18d, three new parts, machine-checked.**  (a′) the remainder identity for
  every down-closed family of evaluated subsets, with threshold sets in place of the
  `m`-subsets, and (b′) a mixed difference in an arbitrary context bounded by its value at
  the reference plus constants of the next order (`DownClosedRemainder.lean`; the
  division's Propositions 10 and 11).  (c′) **Shares of every level**
  (`ShareLevels.lean`): charging the constants to the `k`-subsets gives penalties
  `Σ_T c_T C(|T ∩ S|, k)/C(m, k)`, ordered pointwise from the envelope (`k = m`) through
  triples, pairs and sites to the constant (`k = 0`); windows of any shape with push-down
  lie between two levels; the shares may be allocated freely.  (The division's Lemmas A,
  A′, B are the cases `k = 2, 3` with a band.)
* **Proposition 11.18e, repaired and extended.**  (b) is the division's statement; (b′)(i)
  — ours, new — on one site the count of the ball holds for randomised algorithms on
  every instance, even for a bracket of unspecified width (a needle at an unevaluated
  state), and is attained; (b′)(ii) the count at prescribed width is a conjecture, and a
  Gaussian prior cannot prove it (average count `2 − √(2δ)` on one site with two states);
  (c) the least support of a function of order below `m` is `|X|/Π(m − 1 largest k_i)`
  (the division's sharpening; exhaustively verified on eight grids).
* **Proposition 11.18f (the allocation for a law).**  The cost of a penalty depends on
  the law of the changed set only; the upper end of the bracket is convex and the lower
  end concave in the allocation; to first order: charge every constant to its least
  probable sub-pattern, which for independent sites is a difference of the closed form
  on nested sets of sites.  On a constructed instance with four nearly frozen sites
  among six the two ends fall 8 and 13 times; on a homogeneous one the two ends want
  different allocations.
* **Proposition 11.113a (nested sandwiches).**  If `m₋ ≤ e₋ ≤ E ≤ e₊ ≤ m₊` with the outer pair
  solvable and the inner pair computable state by state, then `W = β + ρ·W_in`: propose
  from the outer sampler, accept with probability `ρ`, evaluate only accepted states.
  The bracket is `A(2t_f + ρ̄t)`: in evaluations the price of the inner sandwich.  For the
  anchored expansion the inner pair is the interpolant plus and minus the envelope, so
  **every share form costs the evaluations of the envelope** — the answer to the
  division's question whether there is a statement for the envelope class itself.
* **Proposition 11.113 completed.**  (c′) the empirical Bernstein bracket of Maurer and
  Pontil (2009, Theorem 4; the statement read in the arXiv HTML version, not from
  memory); the division's two remarks, the second in a sharper form (an error in the
  evaluated energies shifts `ln Z` by at most itself, unamplified); (d) the count
  `2 ln(2/δ) sinh²(Δ/2)/ε²`, **and its necessity written out**: against a member whose
  floor set contains every state independently with probability `w`, every algorithm
  sees independent bits, so two members `2ε` apart need total variation `1 − 2δ` between
  two binomial laws — `N ≥ 2(1 − 2δ)²/KL(w‖w′) ≈ (1 − 2δ)² sinh²(Δ/2)/ε²` by Pinsker; the exact
  number is three times that and a third of the sufficient count.
* **Corollary 11.114** with both terms, and `ratio_expected_queries_ge_mixed`
  machine-checked (dips or bumps, in either macrostate).  `BoxAdditions.lean`: the
  division's lemmas for the floor, the ceiling and the weighted sampler, adopted on our
  definitions.
* `BlockReductions.lean`: Theorem 11.116(a), (b) in abstract two-block form.  A
  cross-reference in Proposition 11.117(b): the variance of the small-slope law is the
  spread constant of the metric probability space.
* **For the engineering division** (THY-RES-0012 §4): the limiting centre types on type
  classes, `0.45404` at `κ = 0.4` and `0.40803` at `κ = 0.3` — its exact finite-`n` computation
  up to `n = 10 000` finds `0.455` and `0.405`, the first exact check of §11.25 — and the
  limits with the centre restricted to the class, `0.027592`, `0.023021`; remark (1) of
  §11.19 quotes its exact-sampler runs; a second scan of the sampler defect
  (`nested_review_R6/t5b_onset.py`): onset between `2·10¹⁴` and `2.5·10¹⁴` trials.

*How it was checked.*  The two major findings of the review were re-derived by hand and
by new tests written from the reviewer's statements: XI.22 (the half lemma, its
sharpness, the bound from one good point, the least support exhaustively, the one-site
count) and XXIV.11 (the count from Hoeffding's Kullback–Leibler bound on a grid of
means, exact failure probabilities of the plug-in estimate: at most `0.0072` with `N_KL`
evaluations, at least `0.16` with a quarter; exact coverage of the empirical Bernstein
bound for Bernoulli variables).  XI.23 (levels, windows, allocations, convexity and
concavity, the gradient, the vertex optimum by enumeration of 81 vertices, the closed
form of the greedy allocation) and XXIV.12 (the identities of the nested sampler, its
coverage simulated with many and with few free draws, the constructed gain `0.1`).
XXIV.6 now checks the sharper upper end of the Bennett certificate.  28 new mutations,
each inspected in both modes after the unmutated baseline (D59 item 9).  Two Lean files
(`ShareLevels.lean`, `DownClosedRemainder.lean`) were written by two assistants working in
parallel from written statements and proof plans, each with a fixed verification
command and no write access to the repository; the coordinator read the statements,
compiled both, added the section on arbitrary allocations and installed them.  One
proof of the coordinator's (`ratio_expected_queries_ge_mixed`) timed out in its first
form — a `show` with placeholders over a large conditional — and was restructured with
`choose` at the first failure.

*What is not new.*  Everything here is elementary: counting, convexity of log-sum-exp,
importance sampling with a control variate known in closed form.  No prior-art search
was made for Propositions 11.18f and 11.113a and nothing is claimed new.  The
counter-algorithm, the corrected count, the share forms with a band, the two remainder
lemmas and the sign-blindness theorem are the Scientific Discovery Division's; the
exact finite-`n` table is the Computational Research Division's.

*Messages.*  THY-RES-0012 (to both divisions: decisions on R12-T1 … T6, P5-T1 … T3,
P6-T1 … T3, the answer to ENG-RES-0012, linked corrections of THY-RES-0010 and
THY-MSG-0015).  Read: the science branch up to `7476f5f`, the engineering branch at
`c2ad4f8`.

### Cycle 10, twentieth checkpoint (2026-11-26): three nested levels beyond the flat instance — the engineering division's computation, what it does to our published figures, and a certified third level

*What arrived.*  The Computational Research Division's checkpoint 5 (ENG-MSG-0005,
ENG-RES-0014), fetched while the nineteenth checkpoint was being audited.  ENG-RES-0014 is
the computation we had asked for as the first proposal of THY-RES-0004 §7: three nested
levels of Algorithm 2L⁺ away from the flat instance.

*What it says* (its numbers; `u = 1`, our referee's design, at the level of expectations).
Its evaluator reproduces the referee's three-level table at the flat instance to the
digit (48 of 48 numbers).  Away from it: against the outer landscape alone a third level
keeps its advantage (`0.94, 0.79, 0.74` of two levels at `n = 1 000, 4 000, 16 000`); on cone
fibres, with the base brackets' own answers, most of it is gone (`0.94, 0.92, 0.96`); with
every middle run charged its certified bound it buys nothing (`1.01, 0.99, 1.00`).  The
mechanism: a base bracket returns on a flat fibre a bracket far narrower than it
promised and on a cone nearly the promised width, and a level that refines what the
level below returns pays for the width it is handed.  Instances that are not products
cannot cost more than the worst product instance, up to `0.02` in units of `na` at the
smallest size.  The searches at the two largest sizes are converged.

*What changes on our side.*  Theory report §11.19, remark (1), said "no worst case has
been computed for three levels"; it now carries the division's numbers.  The
three-level figures of THY-MSG-0007 §3 (`0.712, 0.460, 0.405, 0.379`) are exact and are
best cases twice over — the flat instance is the cheapest outer landscape and the
cheapest fibre; linked correction in THY-RES-0013 §2.  The limits `τ₃ = 0.361a < τ₂ = 0.500a`
are worst-case exponents and are untouched: this is a finite-size statement about one
design.  The division's paper argument for non-product instances was re-derived for
uniform inner behaviours (THY-RES-0013 §3): the classification threshold does not depend
on where a fibre sits in its trivial bracket, and the refinement windows are monotone
in the two initial half-widths.

*What we found on the way: a certified third level.*  The division's certified column —
three levels not below two at any of its sizes — looked like a property of a third
level; the first draft of this checkpoint said so and asked the division at which size
the gap closes.  It is a property of how the referee's design picks its servers: by
their cost at the flat fibre.  Theorem 11.56's bound is nondecreasing in the cost bounds
of the inner procedures, and a two-level run is an admissible inner procedure with its
own `C_max` as cost; so with the server of every rung chosen **by certified cost** the
certified bound of three levels is at most that of two, for every `n`.  Evaluated with
the referee's own routines (`experiments/coordinator_checks/three_levels_certified/`: three
scripts, stored outputs, README; where the grids overlap, 54 of 54 numbers agree with
the division's table) it is `0.611, 0.526, 0.478, 0.444, 0.438` in units `ln(bound)/(na)` at
`n = 4 000, 8 000, 16 000, 32 000, 64 000`, against worst instances found for two levels of
`0.683, 0.619, 0.575, 0.550, 0.537`: **a certified third level pays from `n = 4 000` on**, by
factors from `e^{32}` to `e^{702}`; it does not at `n ≤ 1 400`, and `n = 2 000` is a tie.  From
`n = 16 000` on the bound is below `τ₂`, the limit of two levels.  The certified gain comes
from the finest rungs and from the bounded-accuracy middle design; the flat-instance
gain of the referee's table came from the extensive design at intermediate rungs,
exactly where its certified bound is poor.  Theory report §11.19, remark (1b);
`DEAD_ENDS.md`, D61 (the detour and what it teaches).  Not refereed; one slope; the
two-level side is the division's search; nothing optimised.

*What we asked for.*  THY-RES-0013 §4, inside THY-REQ-0001: reproduction of the two
certified-cost columns with the division's evaluator; the cost of these designs on its
instances; further levels by the same rule — a certified level recursion at finite `n`;
other slopes.

*What arrived at the end.*  The Scientific Discovery Division's checkpoint `edfd54c`
(fetched 07:37 UTC): five messages.  SCI-REV-0014 reviews and machine-checks our rate
for the level recursion and finds **Proposition 11.117(b) false without the word
"symmetric"**, with twelve minor findings; SCI-RES-0014 (shares at the leaves),
SCI-RES-0016 (its answer to our nineteenth checkpoint), SCI-MSG-0026 (its own work), and
SCI-RES-0015 (to the engineering division).  SCI-REV-0014 and SCI-RES-0015 were read in
full, the others by their heads.  Nothing of it is applied in this commit except that
the new texts use `τ₂/a = 0.500` (its m9) and that the digest's do-not-build-on list names
Proposition 11.117(b) for envelopes that are not symmetric.  It is the first item of
the next checkpoint.

*Verification.*  No Lean file, harness test or mutation changed.  New: the check
directory with its stored outputs (about two hours of single-core computation in all),
D61.  `scripts/audit_all.sh` passes with the counts of the nineteenth checkpoint.

### Cycle 10, twenty-first checkpoint (2026-11-26): a review that machine-checked our rate and found a hypothesis we had dropped; one side of a sandwich at a time; a split rule; what the kernel can evaluate

*What arrived.*  The Scientific Discovery Division's checkpoint `edfd54c` (five messages),
fetched at the end of the twentieth checkpoint.

*SCI-REV-0014 — the review we had asked for.*  The rate `τ_k − h ≤ c₁/(k + c₂)` of the level
recursion is right, line by line, and the division machine-checked it on top of our three
step lemmas, for the exact recursion of the cube at every slope and for the sequence at
accuracy zero (`RateFull.lean`, 941 lines, adopted unchanged; compiled here, in the axiom
audit).  The remark after Theorem 11.53 is now **V** for its two displays.  Reading how its
earlier reviews had been applied, the division found **one proposition of ours false as
worded**: Proposition 11.117(b), the small-slope law, is its Proposition R10.1 *for
symmetric envelopes*; our text dropped the word in a section whose Setting allows
envelopes that are not symmetric, and there the coefficient is a quarter of the one
stated.  Reproduced with a few lines of our own (both rows of its table to the digit)
before accepting; corrected; harness XXV.3 now carries the counter-example and its
symmetric counterpart.  Twelve corrections of record, all applied: an inequality that
holds for `p < ½` only; numbers of a harness test quoted from a draft of the test; two
grid values quoted as values (`τ₂/a = 0.5004`, `h/a = 0.2626`, re-computed in 30 digits);
summaries wider than their cells; five points of wording in the rate remark.  `DEAD_ENDS.md`,
D62.

*SCI-MSG-0026, A16-T2 — Proposition 11.113b (new).*  The division's lemma (machine-checked
by it, adopted as `SandwichCost.lean`): a ceiling loses at most its mean band under the true
ensemble, a floor at least its mean band and possibly far more.  Its question was whether
our §11.30 has the matching statement about evaluations.  It has now, and it points the
other way: **from a floor's sampler both sides of `ln Z` are certified, with no ceiling, at
the price `e^{2x}/ε²` of the floor's own excess `x` — and an exponential in `x` is necessary; from
a ceiling's sampler only the lower side is ever certified**, and a finite upper bound costs
`(1 − δ)|X|` evaluations (the needle of Proposition 11.18e(b′)(i)).  The safe bound is the
useless sampler.  Harness XXIV.13 (seven mutations).

*SCI-RES-0014 — shares at the leaves.*  Its answer to our question (four of its five gap
analyses are certified after branching on one site, the fifth at depth two) is in
Proposition 11.18b(e).  Two kernel requests were delegated to two subagents under written
briefs, each producing one new file that the coordinator compiled, scanned and read:
`SplitRule.lean` (a domain-split node as a layer over the kernel; sound; a leaf serves
every sub-box; a split of two leaves is equivalent to the branch with the leaves
repeated; a frustrated triangle on which no single leaf certifies and the split does)
and `SymmetricPairHypothesis.lean` (soundness for real models when the instance stores
each pair table once; strictly weaker than the termwise hypothesis, with a witness).  A
third subagent measured what the Lean kernel can evaluate
(`experiments/coordinator_checks/kernel_eval/`): the division's blow-up (512 table entries,
11.9 GB) is a property of indexed reads of arrays — reproduced with integers alone at
1 024 entries — and an integer leaf check written for the kernel is evaluated on
147 456 table entries in 13.5 s and 1.6 GB without any axiom; three of its cases re-run
by the coordinator.  No proof relates that checker to `verify`; that is the open step.

*SCI-RES-0016.*  Its remark on the algorithm that attains the one-site count (the bracket
returned after a skip must be wrong for at most one skipped state: width at least `ln 2`
for `ln Z`) is in Proposition 11.18e(b′)(i) and in harness XI.22(d).

*A direction opened: workstream Q.*  The twentieth checkpoint made the recursion of
certified bounds at finite `n` well defined (nesting by certified cost is monotone), and
this one made its rate a machine-checked statement.  What has never been quantified is
the `o(n)` of the adaptive exponent (theory report §11.19, remark (2)).  The exact
evaluations suggest a loss of about `1.2√n` nats for two levels and `1.6√n` for three; with
the proved rate `c₁/(k + c₂)` and a loss of order `k√n` for `k` levels the balance is `k ≈ n^{1/4}`
and a bound `exp(nh + O(n^{3/4}·polylog))`.  A paper-proof workstream was launched to prove
that or find the obstruction (`docs/workstreams/Q_brief.md`).  **Its report arrived while
the audit of this checkpoint was finishing, and claims more than was asked:
`exp(nh + C·√(n ln n))`** — by inducting on the piecewise-linear majorants of the rate
proof instead of the exact recursion, with a new lemma by which a level at an extensive
accuracy loses only a polynomial factor, so that only `O(ln k)` of `k` levels lose `e^{O(√n)}`.
If right, it also makes two sentences of the theory report wrong (§11.19, remark (2), and
the end of the rate remark: "the sub-exponential factors … are not bounded uniformly in
`k`").  **Nothing of it has been verified and nothing of it is in this commit** — neither
its report nor its scripts; verifying it is the first item of the next checkpoint.

*Verification.*  85 Lean files (four new), 4899 declarations in the axiom audit,
646 headline theorems; harness 180 tests (152 survive, 28 documented refutations);
503 mutations (502 caught, one expected pass; 146 baseline runs); stored outputs
regenerated from full runs; `scripts/audit_all.sh` passes.  THY-RES-0014 (to the science
division, copy to engineering) with linked corrections of THY-RES-0011 §§1, 2, 8.

### Resume here (cycle 10, twenty-first checkpoint)

Verified state: every module under `proofs/` (85 files) builds with zero warnings and is walked
by the axiom audit (4899 declarations); the harness (180 registered tests: 152 that must
survive, 28 documented refutations) and its mutation tests (503 mutations: 502 caught, one
expected pass; baselines checked,
crashing mutants rejected) pass; `scripts/audit_all.sh`
exits 0.  **Three divisions** work on three branches (this one; `research/ubuntu-engineering`;
`research/scientific-translation`); the other two are read-only for us and are fetched at
every checkpoint (`docs/collaboration/status/theory.md`).  Refereed or independently reviewed:
theory report §§11.16–11.17 (R5, R6, R_P), §11.18 (R7; SCI-REV-0007), §11.19 (R8; SCI-REV-0007),
§11.20 (R9), §11.23 (R10), §11.32 (R11; SCI-REV-0010), and — by the Scientific Discovery
Division — §11.22 (SCI-REV-0002, -0009, -0011), §11.24 (SCI-REV-0003), §11.25 (SCI-REV-0001),
Theorems 11.99 and 11.101 of §11.26 (SCI-REV-0005), Theorem 11.18a and Propositions 11.18b,
11.18c (SCI-REV-0012), Theorem 11.110(e) as corrected, Theorem 11.18d as written,
Propositions 11.18e and 11.113, Corollary 11.114 and Theorem 11.115(c)–(e) (SCI-REV-0013:
two sentences wrong and replaced at the nineteenth checkpoint), the prior-art columns
(SCI-REV-0004, -0006).  Machine-checked: §11.21; Theorem 11.18d with its parts (a′), (b′),
(c′); the core of the counter-algorithm of Proposition 11.18e(b); Theorem 11.116(a), (b)
in two-block form;
Theorem 11.109a(a)–(c) and Theorem 11.110(f) (the division's files); Theorem 11.116(c)
(`SoftMinLowerBound.lean`); Proposition 11.18b(d) and the soundness of (e) (`StateShares.lean`).  **The coordinator's own proofs, checked
numerically, no referee:** §11.27; §11.28 has since been reviewed
and replicated by the Scientific Discovery Division (SCI-RES-0005); §11.29 consists of our
criterion and of that division's theorems, re-derived and replicated by us and read back
by it (SCI-RES-0008); §11.30 (a)–(e) were re-derived by that division from the statements
(no error; SCI-RES-0007, -0008), its part (f) and Proposition 11.112 are that division's,
re-derived by us on paper and tested, not machine-checked;
Proposition 11.81(c) in its completed form, the remark on sample sizes after Theorem 11.56,
the `χ²` bound and the rate in Theorem 11.97(c); **the rate `O(1/k)` for the level recursion
(remark after Theorem 11.53) and the duality statement of Proposition 11.18b(e)**.  **Not
refereed:** the revised Theorem 11.44,
Proposition 11.50, Propositions 11.100, 11.102, 11.103(a)–(c); Propositions 11.18e(b′),
11.18f, 11.113a and the mixed lower bound for ratios (nineteenth checkpoint; a review
asked of the science division, THY-RES-0012).  **Not checked by anyone:** the
two-level algorithms in the extensive regime under an adversarial
search, or in the batched schedule (three levels beyond the flat instance have been
evaluated by the engineering division at one slope, on flat and cone fibres: ENG-RES-0014); the nested algorithm with a field or with several
site types end to end; Theorem 11.63 on sets without symmetry for `n > 6`; parts (f), (g) of
the bridge theorem (read only); **the nested sampler of Proposition 11.113a on any real
sandwich.**  **Nothing received is unapplied** except the optional parts of L4-T3 of
SCI-MSG-0023 and P5-T1(i) (item 0-first); the
science branch is read at `4b80f89`, the engineering branch at `ce71724`.  In priority order:

0-zero-zero. **Apply the science division's commits `ea1233f` and `ddd4be3`** (fetched at
   10:25 UTC on 2026-11-26, when the twenty-first checkpoint was ready to commit).
   **SCI-REV-0016** (read in full): its independent review of remark (1b) of §11.19, the
   certified third level.  The rule holds; 159 of 159 certified numbers replicated with
   code that imports nothing of ours.  *Major:* the two-level worst cases of our table at
   `n = 1 400, 2 000, 8 000, 32 000, 64 000` are ENG-RES-0008's, computed for the ladder
   `ε*·0.85^i`, not for the referee's ladder `x₀(b/x₀)^{l/40}` of the three-level bounds — two
   designs (their certified two-level bounds differ in the third digit); "of the same
   outer design" holds at `n = 4 000, 16 000` only.  Either mark the five entries (its
   replacement text: its `R16_REPORT.md` §1) or ask the engineering division for the
   three numbers of the table's design.  *Minor:* the abort rule of Theorem 11.56 must
   test the budget before every query, as Theorem 11.52's text does (as worded it proves
   `C_max + M̄`); "the largest tolerance" is a supremum and "accuracy" should read
   "certified accuracy"; "at the level of expectations" is the mean-run model.  *Its
   addition, to be adopted:* against the **exact** cost of the two-level algorithm at the
   flat instance (deterministic; minimum over the outer fraction on a grid of step `0.01`:
   `0.5336, 0.5110, 0.5027, 0.4998, 0.4961` at `n = 4 000 … 64 000`) the certified three-level
   bound (`0.6106, 0.5262, 0.4782, 0.4439, 0.4381`) is lower from `n = 16 000` on — a comparison
   with no search and no model — and higher at `4 000` and `8 000`; and `τ₂/a` bounds nothing
   at a finite `n`.  Its Proposition R16.1 (nesting with the hypotheses written out) is
   offered.  Recompute its flat-instance table with the referee's evaluator of the flat
   instance (`experiments/reviews/R8/r8_flat.py`) before adopting.
   **Not yet read:** SCI-REV-0015 (the review we asked for of Propositions 11.18e(b′)(i),
   11.18f, 11.113a and the mixed ratio bound), SCI-RES-0017 (our nested sampler and
   allocation rule run on its instances), SCI-RES-0018 (its answer to THY-RES-0013),
   SCI-MSG-0027 (its own work).
0-zero. **Workstream Q: the sub-exponential term of the adaptive exponent** (launched at
   the twenty-first checkpoint; brief `docs/workstreams/Q_brief.md`).  **Its report exists
   in the working tree of the session that wrote this entry (`docs/workstreams/Q_REPORT.md`,
   scripts under `experiments/workstreams/Q/`) and is committed only once verified; if it
   is not in the repository you are reading, the verification was not finished and the
   brief is the place to start again.**  Its claim: for every `n`, an explicit design with
   `k_M` nested levels has certified cost `exp(n·B_M + E_M)`, `B_M − h ≤ c₁/(k_M + c₂)`,
   `E_M ≤ C₁√n + (k_M − 1)·O(ln n)`, hence `exp(nh + C√(n ln n))`, `C = 8.64` at `u = 1` in the limit;
   the decisive new step is its Lemma Q4 (at `θ = e^{x − O(1)}` the closing radius is at least
   `ρ_h n_o`, so `ln(1/π†) ≤ n_o h + ln(n_o + 1)`: a "slope step" loses a polynomial factor only)
   and its Propositions Q6, Q7 (the two steps of the rate proof at finite `n`).  It also
   lists five imprecisions of the theory report (two hypotheses of Lemma K.4 dropped in
   Lemma 11.55(c); a constant; the `o(n)` of Theorem 11.52 is `O(ln n)`).  To verify: read it
   as a referee would — re-derive the one-level
   inequality from Theorem 11.56 and Lemma 11.55 (the `√n` term should be about
   `u·√((φn/2)·ln(2e^{u(m₀+2)}/θ))`, `1.29√n` at `u = 1`, `φ = ½`, `θ = 0.05`; the exact two-level bounds
   of `experiments/coordinator_checks/three_levels_certified/out_summary.txt` fit
   `0.85√n + 6.4 ln n`), check the induction over levels for anything not uniform in the
   number of levels (the accuracy budget of `k` nested bounded-accuracy levels forces
   `λ, η, η′, θ ~ 1/k`; the failure probability handed down is exponentially small), re-run its
   scripts, and only then decide what enters §11.19, remark (2), and with which label.
   If no report exists (the agent stopped without one), the brief is self-contained: start
   it again or do it by hand.  An independent referee afterwards.
0-zero-a. **Left over from the science division's checkpoint `edfd54c`** (applied at the
   twenty-first checkpoint, THY-RES-0014).  (a) The symmetrised forms of the other
   soundness theorems that take a real model (`verifyR_sound_real`, `verify_sound_thirdOrder`,
   `verify_sound_ball`, `bverify_sound_real`): two lines each from
   `PairInstance.cast_energy_le_symm`; only if the division asks.  (b) `split` inside the
   kernel type `Cert` itself (below `branch` and `sum` nodes), with the reference checker
   and its conformance vectors: when a producer exists.  (c) **A refinement proof for an
   integer leaf checker**: the measurement of `experiments/coordinator_checks/kernel_eval/`
   shows the Lean kernel evaluates a purpose-built integer check of one leaf on `1.5·10⁵`
   table entries; the theorem "it returns `true` ⇒ `LeafOK` for the decoded instance" would
   turn accepted certificates into kernel theorems without `native_decide`.  Not started;
   difficulty not assessed.  (d) The division's open question: a connected family with a
   unique minimiser whose `sum`-free certificates need exponentially many leaves (theory
   report §12 item 6).  (e) Its review of our nineteenth-checkpoint statements and its run
   of the nested sampler are announced (SCI-RES-0016 §3), not yet received.
0-zero-b. **Three nested levels: the certified level recursion at finite `n`.**  Done at
   the twentieth checkpoint: ENG-RES-0014 applied (theory report §11.19 remark (1)); the
   rule "serve every rung by the procedure with the smallest certified cost" and its
   evaluation (remark (1b); `experiments/coordinator_checks/three_levels_certified/`): a
   certified third level pays from `n = 4 000` on at `u = 1`.  Open: (a) reproduction by the
   engineering division, and the cost of the certified-cost designs on its instances
   (asked, THY-RES-0013 §4); (b) **four and more levels by the same rule** — in `cert3.py`
   the function `run2` would have to take an inner family; with the referee's routines
   each further level costs a factor of about forty in time, the division's evaluator is
   faster (asked as well); (c) what carries the bound: coarse rungs near the accuracy
   where the multiplier of Theorem 11.56 changes from the sample cap to the count, and
   the finest rungs — a finer outer ladder gains only `0.001` at `n = 4 000` (tried, not
   stored), so the levers are the lowered cap of the remark after Theorem 11.56 and a
   middle design for accuracies of order `φ₁na`; (d) no harness test was added for the
   monotonicity or for the agreement with the division's column — the check directory
   asserts both on every row; (e) the division's exact classification rule (its §1) has
   been read, not re-derived; (f) other slopes.

0-first. **Open from the nineteenth checkpoint.**  (a) *The Hamming ball for randomised
   algorithms at prescribed width* (Proposition 11.18e(b′)(ii), a conjecture; theory
   report §12 item 10(f)).  What is known: false for unspecified width on more than one
   site (the division's counter-algorithm); true on one site instance by instance
   (needles).  A worked reduction for a successor — cube, order two, zero remainder,
   `h = α + β·s`: for large coefficients `ln Z ≈ −min h = −h(x*)`, `x* = −sign β`.  After
   evaluations at `x¹, …, x^q` let `W = span{x^j − x¹}`; the minimum is a known linear
   combination of the observed values iff `x* − x¹ ∈ W`.  With one hidden direction `ν`
   (`W = ν^⊥`) and `β = β₀ + tν`, `β₀ ∈ W` known, the function
   `t ↦ ν·x*(t) = −Σ_k |ν_k|·sign(t − t_k)`, `t_k = −β₀_k/ν_k`, is a decreasing step function, so
   the event "the algorithm has seen the minimum" is one interval between consecutive
   breakpoints, known to the algorithm; for a coordinate direction it is the sign of
   the hidden coefficient.  Under a Gaussian prior the algorithm may stop when that
   interval has posterior mass near one — rare, but enough for an average count
   `N_ball − Θ(√δ)`; so a proof needs per-instance correctness, or a prior (independent
   symmetric coefficients with log-uniform magnitudes over a huge range, the constant
   on a much wider range) under which every such interval has posterior mass at most
   `½ + o(1)` outside transcripts of vanishing probability.  **An outline exists** (theory
   report Proposition 11.18e(b′)(ii)): under that prior the magnitudes are widely
   separated; with `k` the coordinate of the support of `ν` that minimises `|β_k/ν_k|`, the
   map `β ↦ β − 2(β_k/ν_k)ν`, `α ↦ α + 2(β_k/ν_k)ν·x¹` keeps the transcript, flips the sign at
   `k` only, is an involution preserving the prior up to `1 + o(1)`, and sends the event
   "the minimum has been seen" into its complement; this would give
   `sup_g E|Q(g)| ≥ (1 − 2δ)(n + 1) − o(1)`.  Verified exactly:
   `experiments/coordinator_checks/random_ball/pairing_check.py` (41 786 cases, no
   violation).  To write: (1) the good set and its probability, with the two cutoffs of
   the prior; (2) the bound on outputs that are right off the event by luck (the
   posterior of the hidden coordinate has density at most `1/(cutoff)` per unit length
   against a total mass of order the logarithm of the scale separation); (3) `ln Z`
   against the minimum, with a bounded known part; (4) the reduction of an early stop
   with several hidden directions to one; then orders above two (the minimum of a
   function of order below `m` is no longer a sum of absolute values) and larger
   alphabets (`T = −α − Σ_i min_a f_i(a)`: the same tropical structure, pairing by swapping
   the two lowest states of one site).
   (b) *The nested sampler* (Proposition 11.113a) has not been run on a real sandwich;
   proposed to the science division with a validation target (THY-RES-0012 §2.3).  When
   it reports, compare the acceptance rate `E_q ρ` with the ratio of the two widths; a
   *deterministic* inner bracket — bounds on `Z(e_∓)` between the share models without
   free sampling — is open (§12 item 13(g)).  (c) *The lower bound without a hint for a
   sandwich*, `sinh²(Δ/2)/ε²`, is proved on paper at this checkpoint (Proposition 11.113(d):
   independent inclusion bits, two members `2ε` apart, Pinsker) and cross-checked against
   exact total variations (harness XXIV.11); open: a machine check —
   `QueryLowerBound.lean` has packing bounds for hinted verification only, so a lemma of
   Le Cam type (total variation of the transcripts under two priors) would be new in
   the library — and the constant (a factor three on either side).  (d) *P5-T1(i)* — a polynomially computable bracket of the least sign-blind
   bound — is not met (THY-RES-0012 §3.3).  (e) Optional, unchanged: the division's
   ordered-constants corollary, the forms without an order on the sites and the
   one-site oscillation of the remainder (its `RemainderIdentity.lean`).  (f) The
   allocation rule of Proposition 11.18f at the pair level ("the two most frozen sites
   of `T`") has a closed form by second differences of `Γ` on nested sets; written in
   THY-RES-0012 §3.2, not in the harness.

0-second. **SCI-MSG-0023** (science branch at `8fb67d3`; closed at the nineteenth
   checkpoint except for the optional parts named below).  Done at the eighteenth
   checkpoint, while its verification runs were in progress: L4-T1 — their
   `BennettTwoPoint.lean` is adopted (Theorem 11.110(f) is machine-checked), and their
   `bennett_bracket_weights` fits `jensen_bracket` without change (`BoxBennett.lean`); L4-T2
   in the text — the sharper upper end `W(r̄ − η − lo, σ²)` and the redundant hypotheses,
   citing their machine-checked lemmas; L4-T3 — `hc0` is dropped from
   `anchored_remainder_site_penalties`, and `cover_of_site_shares_order`,
   `cover_of_equal_shares` ask nonnegativity on `m`-subsets only.  **Done at the nineteenth
   checkpoint:** the harness check of the sharper upper end (XXIV.6, with the mutation
   `r̄ − 2η − lo`).  **Not done:** the optional parts of L4-T3 (their ordered-constants corollary, the forms
   without an order on the sites, the one-site oscillation of the remainder — in their
   `RemainderIdentity.lean` to copy).  Also in that fetch: SCI-RES-0011 (nothing to apply),
   their replication of our audit at `9408e33` (passes), and their review of the
   seventeenth checkpoint (arrived as SCI-REV-0013 and applied: item 0-first).
0. **§11.32, the crossover and what is conditional** (theory report §12 item 14).  (a) When
   the Scientific Discovery Division or the engineering division delivers the Markov
   recursion with blocks of four and five sites (requests R10-T2, R10-E1 of SCI-REV-0010),
   re-compute the cells that decide a sign and write the `(p, u)` map into Proposition
   11.117(d); our own vertex enumeration (`mk_cube_vertices` in the harness, spanning trees
   of tight edges) stops at three sites — for four sites enumerate vertices as functions
   with a connected tight graph by a different method (the cube `Q_4` has too many spanning
   trees).  (b) The lower side of the small-slope law for the limit `F_∞`.  (c) The
   threshold conjecture at strong coupling (R10-T5).  (d) An upper bound on a cost at
   bounded accuracy for a chain — the analogue of Theorem 11.58 for block landscapes — is
   the one statement that would turn the brackets into exponents of algorithms.  (e) A
   machine check of Theorem 11.116(d) — (c) is done (`SoftMinLowerBound.lean`), (a) and (b)
   are done in their two-block form (`BlockReductions.lean`, nineteenth checkpoint; the
   iteration over the cuts of a chain is on paper), (d) is an induction along the chain.  **Before any qualitative sentence about a new
   parameter range is written: evaluate the proved bound of the opposite sign over that
   range** (D59 item 1).
0a. **The rate of the level recursion** (remark after Theorem 11.53) — **done at the
   twenty-first checkpoint: refereed and machine-checked by the science division
   (SCI-REV-0014, `RateFull.lean`)**; what follows is the earlier entry.  Refereeing has been
   asked of the science division (THY-RES-0011 §9(a)); a Lean proof would iterate
   `StepLE.of_limit`, `StepLE.of_macro`, `StepLE.at_hint_fraction` of `HintRecursion.lean`
   (statement and proof in the head of
   `experiments/coordinator_checks/nested_review_R6/t4_rate.py`).  The harness proposal for
   test XVI.3 (`HARNESS_PROPOSAL.md` there: a fixed sub-case in which the Harper term
   decides the closure, and a statistic) is **not applied**.
0b. **Share certificates beyond the relaxation** (theory report §12 item 10(c)): shares at
   the leaves of a small branching tree, for instances with an integrality gap; ask the
   division for its five such analyses (THY-RES-0011 §9(c)).  The abstract half of the
   bridge theorem's parts (f), (g) next to `SetLimit.lean` (the division's R9-T1, deferred).
1. **Barrier certificates** — K-T1 and K-T2 are done (§11.31).  Open from SCI-MSG-0005:
   K-T3 (the set of barrier heights over an envelope class is a closed interval; needs a
   definition of the barrier as a minimum over walks on a finite graph), K-T4 (is the
   robust lower end of the critical depth computable by polynomially many anchored
   barrier computations?); the refactoring of the partition kernel over an ordered
   commutative semiring (about a hundred signatures; a recipe exists only in the
   session's scratch space: replace `ℚ` by `R` with `[CommSemiring R] [PartialOrder R]
   [IsOrderedRing R] [DecidableEq R] [DecidableLE R]` in `PartitionCertificate.lean` 42–467
   and `PartitionProduct.lean` 160–955, and replace the four `linarith`/`nlinarith` calls at
   `PartitionCertificate.lean` 282, 391–392, 437, 439 by `add_le_add`, `le_add_of_nonneg_left`,
   a `le_trans` with `ring`, `add_nonneg zero_le_one`, `le_trans`); the tropical kernel over
   min-plus polynomials was not examined.

2. **Workstream Y is integrated** (theory report §11.32, harness XXV; refereed by R11,
   reviewed and replicated by the science division, SCI-REV-0010).  Its headline was wrong
   as a general statement — the direction depends on the slope — and is corrected; the
   report file carries an errata block.  What remains is item 0 above.
3. **The middle slice `κ = ½` for adaptive algorithms without a hint** (Conjecture 11.94(iii)
   on that slice alone; request T7 of SCI-REV-0001, agreed in THY-RES-0007): it decides the
   adaptive exponent of every antiferromagnet without a field.
4. **What a certificate of a real solvated free energy still needs** (§11.30 as amended;
   §12 item 13(a)).  The science division's measurements say that for neutral side
   chains on a fixed backbone first-order perturbation theory from a pairwise (often a
   chain) model is accurate to `10⁻³ k_BT`, and Theorem 11.110(f) says what would certify
   it: a proved one-sided floor of a few `k_BT` and a proved variance bound for the
   remainder beyond that model.  On our side: (a) machine-check the two-point Bennett
   bound (A17-T4; the reduction to two-point laws on top of `jensen_bracket` in
   `BoxClass.lean`) — **done by the science division (its workstream L4; adopted as
   `BennettTwoPoint.lean` at the eighteenth checkpoint)**; (b) a variance bound with a computable constant for a function with
   bounded one-site or one-pair oscillations under a chain measure — the division's
   A17.8 gives `¼ΣC_i²` with Dobrushin coefficients; an exact variance by transfer
   matrices for an explicit sum of local tables would be sharper and is a finite
   computation that a kernel could check; (c) the box with a mean-energy datum (A17-T3;
   A17-T1, A17-T2 are withdrawn by the division: the Rényi table is in print); (d) **the
   compact case** — §12 item 13(a): is the loss of a bound that treats atom pairs one at
   a time intrinsic, or is there a signed bound?  The division's certificate on extended
   backbones (SCI-MSG-0020) is the state of the art here; Proposition 11.113 is the
   sampler for it and has not been run on its instance.
   Also still open: a machine-checked Proposition 11.69a (request T-3; less urgent since
   Proposition 11.69b).
5. **The query complexity of observable free energies** (theory report §12 item 11(a)):
   how many evaluations certify `ln[Z(A)/Z(B)]`; notes on the traps in THY-RES-0006 §2 (a
   macrostate is not a closed world; straddling dips cancel).  The box class of §11.30
   is the case without geometry and a good first instance (§12 item 13(c)).
6. Requests of the science division not yet answered: SCI-MSG-0007 X-T3 (is the supremum
   of the annealed free energy over a Frobenius ball attained at the Curie–Weiss
   matrix?), SCI-MSG-0005 K-T3, K-T4, SCI-MSG-0006, -0008, SCI-MSG-0012 §4, SCI-RES-0002
   P-T1, P-T2, P-T4; SCI-MSG-0013 (their tail lemma with an energy constraint) and
   SCI-MSG-0016 (its correction) are read, not checked.  Answered at this checkpoint:
   SCI-MSG-0015 (P2-T1 … P2-T4), SCI-REV-0006 T-4, SCI-MSG-0007 X-T1, X-T2, X-T4,
   SCI-RES-0007 A17-T1, SCI-MSG-0018 A17-T4 (paper and harness), SCI-REV-0008 R7-THY-1, -2.
   All of what was awaited at the seventeenth checkpoint has arrived and is applied
   (A3, L3, P3, R9, R10, P4, L4, their reading of THY-RES-0009 and of THY-RES-0010 in
   part).  **Awaited now:** their review of the seventeenth checkpoint and the envelope
   sampler on their twenty-residue sandwich (both running at `8fb67d3`), their workstream
   P5 (the compact case), the
   crossover of §11.32 (R10-T2, with R10-E1 at the engineering division), and their
   reading of THY-RES-0010 and THY-RES-0011.  From the engineering division: nothing
   since `a2f6dc7` (THY-REQ-0009, -0010 read there, not yet answered).

The list of the thirteenth checkpoint continues to hold from here on; its items follow with
letters, brought up to date where the reviews changed them:

(a) **The adaptive exponent without a hint for an interacting known part** (Conjecture
   11.83, O4).  Reduced at the tenth checkpoint to the uniform measure on one type class
   (§11.25).  Two steps remain, in this order: (a) **Conjecture 11.94(iii)** — redo the
   proof of Theorem 11.56 on products of type classes (facts (F1)–(F3) of Theorem 11.52
   hold verbatim; needed: the tail bound of the closure test as an exponent with `o(n)`
   slack, from Theorem 11.78(b) inside one type class; random splits with one-sided
   failures, Lemma 11.93; the sum over typical type pairs by Theorem 11.92(b)); a
   two-level version would already show that adaptivity helps on a type class;
   (b) the exact exponent when exits that change the type matter (a field: known,
   `R^max`; two phases beyond the junction: open) — needs information across type classes;
   the natural algorithm keeps the top-level outer block unresolved by type and leads to
   a recursion over rate functions.  (§11.25 has been reviewed: SCI-REV-0001.)
(b) **Synchronise with `research/ubuntu-engineering` and `research/scientific-translation`** at
   every checkpoint (read-only; never merge).  From the science division everything that
   was awaited has arrived and is applied (the five reviews; THY-REQ-0011 answered in
   full; SCI-RES-0005, SCI-RES-0006, SCI-RES-0007, -0008 applied; SCI-REV-0007 received,
   item 0); awaited now: its answer to THY-RES-0009.  Open on the engineering side: THY-REQ-0001 (two levels at bounded
   accuracy done, ENG-RES-0008; three levels, the extensive regime and the batched schedule
   open), -0003, -0004, the rest of -0002, -0007, -0008 (items 1–4), -0009, -0010.
(c) **Known parts with spatial structure** — **workstream Y has reported** (item 2 above):
   read its report critically, re-derive, re-compute with own code, then integrate.
   Nearest-neighbour interactions along the sequence (a Markov chain as reference
   measure).  What carries over in principle: the measure is uniform on *Markov* type
   classes (pair counts), symmetric instances are functions of the pair type, random
   centres can be drawn from a Markov type class, and the method of types has a Markov
   version; what does not: the one-flip coupling of adjacent classes is no longer exact (a
   flip changes two pair counts and its multiplicity depends on triples), so Theorem
   11.76(a) can hold only up to polynomial factors, and there is no transitive group, so
   Theorem 11.76(b) needs random centres instead of random permutations (as Theorem
   11.27(c) does for product measures).  The expected output: "two-letter" formulas with
   conditional entropies of Markov chains in place of `MI`.
(d) **Rounds** (§11.24, reviewed: SCI-REV-0003): is `τ^{(3)} = h`, or `τ^{(r)} = h` for any fixed `r`?
   What two rounds cost *at* the flat-histogram instance (Corollary R4.2 is a lower bound
   for the expected cost there).  Witnesses for the recursion with four and more rounds.
   The general-`r` form of Lemma 11.85 in Lean (two rounds are done, also for expected
   batch sizes).
(e) **Two phases** (§11.23): binary optimality at vanishing accuracy (C1; not refuted by
   the referee's 86 searches); the supremum
   beyond `e₀` (O2) — now known to lie below the uniform cube's value for every
   interaction (Corollary 11.91); the non-adaptive exponent at `u = 0.30` (O5; proved
   interval `[0.00184, 0.00338]`); the junction `min{βJ*, βJ_w}` and a proof that `R_H < R_unif`
   beyond it (would follow from uniqueness of the uniform cube's optimal profile); a
   referee for the completion of Proposition 11.81(c).
   Machine-checking Theorem 11.76(c) is routine and not done.  The odds-ratio lemma
   (11.89) in Lean needs the derivative of the capacity; its kernel, the monotonicity of
   `t·ln(t/(t+W))`, is a few lines.  The same lemma for larger alphabets is open and is
   what a comparison with the uniform case beyond two letters would need.
(f) **The limit shape** (§12 item 9(a1)–(a6); reviewed: SCI-REV-0002): Conjecture 11.75; a
   second-level cluster programme for the seven vertices of `𝒦₂` that no periodic system
   attains; the routing lemma for periodic chain systems (with it the inner volume `2.22`
   and two more vertices would be proved); whether any accuracy is non-exceptional; items
   4 above.
(g) **Machine-check that the game functions of the problems are game functions** in the
   sense of `GamePair.lean` (cube, field, and now convex mean-field models: Theorem
   11.80(c) is a paper proof), and the shear law for their non-adaptive exponents.  Still on
   paper as well: Lemmas 11.67 and 11.68 (the lattice input of §11.22).
(h) **A weighted Harper-type inequality** for the type-uniform measure and the slack of the
   flat-histogram reference (finite `n`, usable error term; THY-REQ-0007).
(i) **Below the exponential scale** (§12 item 2(d)(i)): quantify the `o(n)`; exponentially
    small accuracies.  **A machine-checked count** for Theorems 11.52 / 11.56 / 11.84.
(j) **Heteropolymer landscapes** (§11.26; Theorems 11.99, 11.101 reviewed: SCI-REV-0005): a
    referee for Theorem 11.97(c) with Theorem 11.78(b) and for Propositions 11.100–11.103;
    which site law and which pinned composition is the hardest for a given envelope
    (Proposition 11.103: not a uniformly weighted sub-alphabet in general; the ceiling
    `u²/32`; groupings into about `e^{u/2}` equal classes at vanishing accuracy — numerical for
    `q ≤ 4`; a proper implementation of `C_t` for larger alphabets); concavity of `F*` for two
    letters (no violation on 1100 random sites; no proof);
    whether the channel-coding dictionary gives more than names; the two-oracle model of
    the science division (§11.27, remark (3)).  **Chains, the rest** (theory report §12
    item 9(b)–(f)); mean-field Potts models beyond the convex regime.
(k) The list of the earlier checkpoints, below, is otherwise unchanged.

### State at the end of cycle 9 (superseded in part by the list above)

Verified state (fourth checkpoint of cycle 9): every module under `proofs/` (41 files) builds
with zero warnings and is walked by the axiom audit (2793 declarations); the harness (83
registered tests: 66 that must survive, 17 documented refutations) and its mutation tests
(114 mutations: 113 caught, one expected pass) pass; `scripts/audit_all.sh` exits 0.
In priority order:

1. **Envelopes for chains** (theory report §12 item 9): the per-torsion route does not
   scale (D42); find an envelope format whose constants do not grow with the chain length
   and that still admits small certificates — sequence-local or windowed-frame classes, the
   contact-map metric, classes linear in pair features — and build the corresponding kernel.
   Close the bracket of Theorem 11.38.
   **Machine-check more of the paper results of this cycle**, in order of value: the
   single-letter part of the exponent theorem (11.27), the product assembly of the lower
   bound on function spaces, the covering sandwich of 11.32, the droplet criterion 11.39.
   Candidates for theorems of the report, if confirmed: the normal form (C1), the second
   best-first bound (C4), the droplet criterion and the vacuous window for chains (B.1, B.5),
   the second-order dip and its consequences (E, Theorems A–C; D's phase transition), the
   torus threshold (D).  The scratch Lean files `NormalForm.lean`, `StarsDoNotCombine.lean`,
   `SecondOrderDip.lean`, `ComparisonDip.lean`, `SetDip.lean`, `RefMeasure.lean` type-check
   according to their authors; move the confirmed ones into `proofs/Frontiers/`.
2. **The exact exponent beyond the cube** (A's Theorem A(ii)): if the review confirms the
   proof, state it as a theorem **[P]**; a machine-checked version would need type classes and
   is a project of its own.
3. **Below the class threshold**: the exponent of hint-free algorithms (on the cube between
   `ln 2 − h(Λ₁/u)` and `ln cosh u`); sites of several types; non-additive instances.
4. **Blueprint consequences**: replace the transfer-matrix planning bound of §6.6 on its
   vacuous window (B.5); the spot-check with a second reference; second-order design rules
   (spider instead of star, density instead of row sums) if E is confirmed.
5. **Compute**: if a gRPC-capable route to Modal becomes available, the natural first jobs are
   exact fractional hitting numbers over all sensitive sets for `n = 7, 8` (orbit LP with
   constraint generation; tests the exact-exponent claim at finite size) and exact covering
   numbers of chains beyond 16 sites (tests B.2).
6. Carried over: probabilistic certificate kernel; `STARCERT` with a termination guarantee; the
   exponent of Theorem 11.15 for exponentially small accuracies; representation-independent
   partition-kernel separation; dependent references; JSON `cut`/`elim` nodes; interval
   evaluation of realistic energy terms; realizability with incomplete distance data.

### State at the first checkpoint of cycle 9 (superseded by the list above)

Verified state: every module under `proofs/` (37 files) builds with zero warnings and is walked
by the axiom audit; the harness (73 registered tests: 57 that must survive, 16 documented
refutations) and its mutation tests (94 mutations: 93 caught, one expected pass) pass;
`scripts/audit_all.sh` exits 0.
In priority order:

1. **Integrate workstream A.**  (a) Move the machine-checked core of its scratch file into
   `proofs/Frontiers/` (generalised dips; the two ingredients of the every-`n` lower bound; the
   two-measure tensorisation and the hitting bound) and connect it to
   `expected_queries_ge_packing` and `hedgedSpotCheck_correct`; (b) state the results as
   theorems of §11.10 (generalised lower bound **[V]**; instance-wise threshold **[V core + P]**;
   exact exponent **[P, unrefereed]**); (c) harness tests for generalised dips and the
   tensorisation on small products; (d) an independent referee for its Theorem A(ii)
   (Lemma 3(c), Proposition 4, Lemma 5, Steps 1–7) — until then it is a claim.
2. **Verify and integrate workstream C**: the normal form `(σ, 0, E^d)`; the second best-first
   bound (valid at `κ = 1`); the negative result on the line with a known part; position
   Theorems 11.5, 11.10, 11.23(a) against Hetland (2020) and AESA.
3. **Workstreams B, D, E, G** when they report: verify before integrating.
4. **Hint-free algorithms** on the cube class: exponent between `ln 2 − h(Λ₁/u)` and `ln cosh u`;
   needs a multi-instance lower bound.  The worst-case threshold of a general product class
   without a hint.
5. **Beyond product landscapes**: a pairwise chain as known part (workstream B).
6. **Probabilistic certificate kernel**: a checker for hedged spot-check transcripts with
   verifier-side randomness; above the threshold the detection probability is certified by a
   single-site computation.
7. **Second-order classes** (workstream E): lower bounds under dense constants; one residual
   with certified constants; `STARCERT` with a termination guarantee.
8. Carried over: the exponent of Theorem 11.15 for exponentially small accuracies (the cube
   diagram suggests the shape of the answer); an approximate, representation-independent
   version of the partition-kernel separation; best-first constants and the `f ≡ 0` doubling
   conjecture; dependent references (D25); `cut`/`elim` nodes in the JSON format; verified
   interval evaluation of realistic energy terms; realizability certificates for incomplete
   distance data.

