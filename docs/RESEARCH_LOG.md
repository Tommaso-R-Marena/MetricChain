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

### Resume here (state at the end of cycle 8)

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

