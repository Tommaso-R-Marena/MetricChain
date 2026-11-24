# MetricChain — Research Log

Chronological record of the theoretical program: what was tried, what was learned, how the
portfolio was re-prioritised.  Companion files: `THEORY_REPORT.md` (results and proofs),
`BLUEPRINT.md` (engineering hand-off), `DEAD_ENDS.md` (falsified or repaired claims),
`prior_art/L1–L3` (literature checks).

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
  hand-picked list (`#audit_axioms MetricChain`).

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
| `CertificateAlgebra` | `(min,+)` kernel `verify`, residual kernel `verifyR` with top-level entry points `verifyRTop` / `verifyRLowerTop` (consistency of the data checked; cycle 5), Master Soundness Theorems, kernel-evaluated examples | **[V]** |
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
| harness tests X.1, II.4, VII.1 could not fail | rewritten with independent computations, exhaustive certificate enumeration, the prune rule, and built-in power checks; new tests II.7, II.8, III.6, DEAD.5 |

The audit also changed one design decision rather than only wording: lower bounds need anchor
values that are *lower bounds* on the residual, so a producer with floating-point evaluations
should publish rounded-down values — and for those the pairwise consistency check is neither
sound to demand nor needed.  The residual kernel therefore has two entry points with two stated
semantics.

### Portfolio reassessment (end of session 1)

* **Strongest discovery so far.**  The *envelope duality* cluster: under any envelope the set of
  configurations that can be optimal is exactly a contact set; with evaluated anchors the exact
  discardable set is characterised by two inequalities; the certified value interval is exactly
  the interval between the two McShane envelopes at every temperature; and any `ε`-certificate
  must evaluate the residual on every state within `(1−κ)σ − ε` of the optimum (an entropy-type
  witness-size lower bound).  Individually elementary, together they *close* the question the
  charter posed for Direction A and give a principled interface for neural residuals: the
  architecture must export an envelope, and the price of a loose envelope is quantified.
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

* No formal statement yet for dependent (Markov / Dobrushin) references in the sandwich.
* The Taylor step producing second-order (separable) voxel envelopes from Hessian bounds and the
  information-based lower bound are paper-level; the separable-envelope theorem itself is verified.
* The Procrustes–Gram stability inequality (Tu et al. 2016) is cited, harness-tested, not
  formalized.
