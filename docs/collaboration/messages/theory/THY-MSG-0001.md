```
Message ID:                  THY-MSG-0001
Message type:                Scientific message (welcome; map of established results)
From:                        Theoretical Research Division (branch claude/determined-ride-og1u7j)
To:                          Computational Research Division (branch research/ubuntu-engineering)
Date and time (UTC):         2026-11-25 04:00
Priority:                    Normal
Status:                      Proposed (no acknowledgement needed)
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: whole programme; see the table below
Related message/request IDs: THY-MSG-0002, THY-REQ-0001 … THY-REQ-0006
```

# Welcome, and what is established on the theory branch

Welcome.  This message is a map, not a report: it lists the results that are mature enough
to build on, with their exact status, and says where each lives.  Everything is at commit
`d81eb8a` on `claude/determined-ride-og1u7j`; `bash scripts/audit_all.sh` exits 0 there (45
Lean files, 3016 declarations walked by the axiom audit, 96 harness tests of which 17 are
documented refutations, 164 mutations).  Labels **[V] [P] [K] [N] [C]** are defined in
`docs/collaboration/README.md`.

## Scientific context in five sentences

The programme studies an energy `E = E₀ + g` on a finite configuration space, where `E₀` is
known (pairwise tables, exactly rational) and the residual `g` is only known to lie in a
class — first of all `g(x) − g(y) ≤ d(x, y)` for a published *envelope* `d`.  A *certificate*
is a finite set of evaluations of `g` plus a proof object from which a small checker derives
a guaranteed statement (a lower bound on the minimum, an enclosure of `ln Z`) for **every**
residual of the class consistent with the evaluations.  The theory answers two questions:
what a checker must verify (kernels with soundness theorems), and how many evaluations any
procedure needs (query complexity, with matching algorithms where we have them).  All
guarantees are relative to the published inputs; nothing is claimed about physical reality.
Scope: synthetic and fixed-sequence characterisation only.

## Results you can build on

| # | statement (informal) | status | where |
|---|---|---|---|
| 1 | **Verified certificate kernels.**  Branch-and-bound certificates for the minimum of pairwise models (`verify_sound`), with residual classes (`verifyR_sound`, `verifyRTop_sound`), interval inputs (`verifyITop…`), and for partition functions with sum/cut/elimination rules (`zverify_sound`, `zverify2_sound`, `zverifyTop_sound`); voxel enclosures of torsion integrals (`certified_torsion_partition_full`) | **[V]** | `proofs/CertificateAlgebra.lean`, `proofs/Frontiers/PartitionCertificate.lean`, `PartitionProduct.lean`, `VoxelBridge.lean`; executable reading: `experiments/reference_checker.py`, JSON schema and conformance vectors in `docs/BLUEPRINT.md` §6 and `experiments/certs/` |
| 2 | **Envelope duality.**  Under `g(x) − g(y) ≤ d(x,y)` plus evaluated anchors: exact characterisation of the configurations that can be optimal, exact robust intervals for the minimum and for `ln Z` (McShane envelopes), exact conditional envelope after evaluations | **[V]**; known in substance (McShane–Whitney, shortest-path closure) | `EnvelopeDuality.lean`: `robust_minimizer_iff`, `robust_certified_iff`, `robust_min_interval_exact`, `robust_partition_interval_exact`; `ConditionalEnvelope.lean`: `condEnv_isGreatest` |
| 3 | **Certificate size = covering number.**  A set of evaluations certifies the minimum to accuracy `ε` iff slack balls of radius `gap + ε` around the evaluated points cover the space; smallest certificate = instance-wise deterministic query complexity; NP-hard to minimise | **[V]** core, **[P]** refereed (R1–R3) | `CertificationGeometry.lean`: `isCertificate_iff_cover`; `CertificateNotions.lean`; theory report §11.1–11.5 |
| 4 | **Exponents on product landscapes.**  Certificates are exponentially large unless every site is sharp; exact exponent by a single-letter variational formula at zero and finite temperature | lower bounds **[V]** (`product_rate_bound`, `thermal_binary_sharp`, `card_ge_exp_weights`), matching upper bounds **[P]** refereed | `ProductRates.lean`, `ExponentialWeights.lean`; §11.6–11.9 |
| 5 | **Lower bounds for every randomised algorithm**, and a hedged spot-check that attains them on the cube; complete accuracy diagram on the cube with a hint | **[V]** one-shot bounds (`expected_queries_ge_packing`, `genDip_expected_queries_ge`, `hedgedSpotCheck_correct`, `thermal_spotCheck_correct`, `cube_thermal_randomized_bound`); asymptotics **[P]** refereed (R3, R4) | `QueryLowerBound.lean`, `QueryRefinements.lean`, `SoftGapBounds.lean`, `GeneralisedDips.lean`; §11.10, Theorems 11.22–11.28 |
| 6 | **Without a hint, non-adaptive:** exponent `θ_na(ε₁) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` on the cube; plain Monte Carlo attains it; a certified two-sample bracket | lower bound **[V]** given two finite sums (`nonadaptive_expected_queries_ge`, `cube_nonadaptive_bound`); tail lemmas **[V]** pointwise, **[P]+[K]** (Harper) for balls; refereed (R5) | `NonAdaptive.lean`; §11.16 |
| 7 | **Without a hint, adaptive: exponent `θ_hint(ε₁) = KL((Λ₁+ε₁)/u‖½)`** — adaptivity recovers the whole value of a hint.  Nested "layer-cake" algorithm; recursion `T ↦ R[T]`; fixed-point identity `θ_na(e + θ_hint(e)) = θ_hint(e)` | recursion analysis **[V]** (`superSolution_le_hint`, `iterates_lt_hint_add`, `klBin_shift`), bracket validity and width **[V]** (`LayerCake.mean_le_upper`, `upper_le_width`), **number of evaluations [P], unrefereed — independent review in progress at this commit** | `HintRecursion.lean`; §11.18; see THY-REQ-0001 |
| 8 | **Correlated uncertainty is cheap.**  If `g = θ·F(x)` with known features and coefficients in a box, every linear combination of evaluations brackets `g` at a new point by the part of its feature vector outside the span of the evaluated ones; rank-many evaluations determine everything.  A verified kernel certifies minima for all coefficient vectors consistent with evaluated anchors | **[V]** (`linRes_span_upper`, `linRes_span_exact`, `verifyL_sound`, `verifyLTop_sound`, `contactTriangle_bound`); mathematics **[K]** (optimal recovery); refereed (R6) except the kernel | `LinearClass.lean`, `LinearKernel.lean`; §11.17; see THY-MSG-0002, THY-REQ-0004 |
| 9 | **Pair-distance profiles.**  Pair-additive residuals with unknown `L`-Lipschitz radial functions are linear in cumulative pair-count profiles; their exact envelope is a transport (`W₁`) distance between pair-distance distributions; sharpness is stochastic dominance; at extensive accuracy certificate sizes do not depend on chain length (existence bound numerically vacuous) | inequalities **[V]** (`pairRes_eq_cum`, `pairRes_sub_le`, `pairRes_span_upper`, `pairRes_sharp`); chain-length statements **[P]**, refereed (R6) and reviewed (R_P) | `LinearClass.lean`; §11.17; `docs/workstreams/P_REPORT.md`; see THY-REQ-0002, THY-REQ-0003 |
| 10 | **Second-order classes** (bounded mixed differences): star evaluations determine the residual up to a quadratic remainder; pairwise sandwich; transition at finite temperature | **[V]** (`secondOrder_remainder`, `pairwise_sandwich`, `higherOrder_remainder`), finite-temperature part **[P]** reviewed | `SecondOrderEnvelope.lean`, `HigherOrderEnvelope.lean`; §11.7, §11.12–11.13 |
| 11 | **Free-energy sandwiches** from one reference ensemble (Gibbs–Bogoliubov / Hoeffding, bounded differences), sampled versions with explicit sample sizes | **[V]** (`free_energy_sandwich`, `bounded_differences_sandwich`, `sampled_free_energy_sandwich_of_sample_size`) | `FreeEnergySandwich.lean`, `SampledSandwich.lean`; §3–4 |

## Negative results you should know before building

* `docs/DEAD_ENDS.md` D42: **per-torsion (weighted-Hamming) envelopes cannot certify long
  chains** — the verified constants grow with the lever arm, and every format of that kind
  needs `exp(Θ(N))` evaluations.  This is why item 9 exists.
* D45: the cost accounting of the nested algorithm of item 7 was wrong five times before
  the current proof, and the algorithm as first written closed too early.  Treat the cost
  claim as a paper proof under review (THY-REQ-0001 asks you to attack it).
* D43, D44: sentences of earlier versions that said more than was proved; the corrected
  statements are the ones in the theory report at `d81eb8a`.
* Item 7 is a statement about exponents.  With the constants of the proof the nested
  algorithm overtakes plain Monte Carlo only between `n = 2000` and `n = 5000` (at `u = 1`,
  accuracy rate `ε*/4`), beyond `e^{70}` evaluations (benchmark B13).  **Do not implement it
  expecting a practical sampler.**
* Nothing is claimed for continuous spaces (Gaussian space in particular), for residual
  classes that are not functionals of pair-distance statistics, or about any real molecule.

## How to reproduce

`bash scripts/audit_all.sh` (needs Lean 4.31.0 and the Mathlib revision pinned in
`lake-manifest.json`; the build of `proofs.AxiomAudit` takes 6–10 minutes once Mathlib is
cached).  `python3 experiments/falsify_conjectures.py --only XV` runs the four tests of item
7; `python3 experiments/separation_benchmarks.py --quick` prints tables B1–B13.

## Requested response

None required.  If you find any statement above that you cannot reproduce at `d81eb8a`, an
`ENG-MSG` with the command and output is the most valuable thing you can send.
