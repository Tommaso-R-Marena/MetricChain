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
* **Referee R7**: commissioned on the draft of §11.18 (brief: break the accounting of Theorem
  11.52; check the Lean file and the chain of quantifiers of Theorem 11.54; evaluate the cost
  of the algorithm in expectation at large `n`).  **Still running at this checkpoint** — the
  report is to be copied to `reviews/R7_referee_report.md` and acted upon first thing.

### Resume here (cycle 10, third checkpoint)

Verified state: every module under `proofs/` (45 files) builds with zero warnings and is walked
by the axiom audit (3016 declarations); the harness (96 registered tests: 79 that must survive,
17 documented refutations) and its mutation tests (164 mutations: 163 caught, one expected
pass) pass; `scripts/audit_all.sh` exits 0.  Refereed: theory report §§11.16–11.17 at commit
`36ec238` (corrected).  **Not refereed**: §11.18 (review in progress), the revised Theorem 11.44
and Lemma 11.43(c), Proposition 11.50.  In priority order:

0. **Integrate the report of referee R7 on §11.18** (if this session ends first: the brief is
   in the cycle-10 entry above; re-commission with the same brief on the committed text).

1. **Adaptive algorithms at a bounded accuracy.**  Theorem 11.54 is for `ε = ε₁n`.  At `ε = O(1)`
   the non-adaptive exponent is `a`, the hinted one `h`.  A version of the two-level algorithm
   with tolerances of order one seems possible — the lower end must then be a layer-cake
   *sum* over the populated levels instead of their maximum (the maximum loses a factor of
   the number of levels), and the closure must cope with `Γ̃(r) ≈ (e^u − 1)n/r` at small radii —
   and its recursion at vanishing accuracy rate is `τ_{k+1} = min_φ max((1−φ)τ_k, φa + (1−φ)T_k(φa/(1−φ)))`,
   which tends to `h`.  Conjecture: the adaptive exponent at fixed accuracy `ε` tends to `h` as
   `ε → ∞`, and is `h` already for `ε` above a constant.  Not started.
2. **Other spaces.**  The convergence theorem is abstract (`HintPair`): it applies wherever a
   two-level construction gives the same recursion and the identity "non-adaptive accuracy =
   hinted accuracy + exponent of the sample" holds.  For product reference measures and
   larger alphabets the tail lemma is available at the exponential scale (the asymptotic
   isoperimetric problem of Ahlswede–Zhang, the blowing-up lemma — from memory, not read);
   this would cover a known part `f ≠ 0` and `k`-state sites.  *Not* Gaussian space, although
   the small-slope limit of the exponents suggests it: there blocks of coordinates are not
   cheaper (Euclidean Lipschitz constant) and half-space dips are detected by a few
   evaluations far from the bulk, so that even the hinted lower bound fails (a claim to the
   contrary was in a draft of §11.18 for an hour and was removed before any checkpoint).
3. **A machine-checked count** for Theorem 11.52, or at least a mechanised statement of the
   cost summation; and a quantified `o(n)`.
4. **Have the revised §11.16 read once more** (Theorem 11.44 with the two-sided tail lemma).
5. **Chains** (theory report §12 item 9): unchanged from the second checkpoint — the size at
   which chain-length independence sets in and a limit theorem; an upper bound for
   "pair-additive plus a small remainder" (no lower bound above two evaluations is proved
   for the sum class); randomised algorithms for linear classes; the cost of checking in the
   profile format; a JSON schema and reference checker for the linear kernel.
6. The list of the earlier checkpoints, below, is otherwise unchanged.

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

