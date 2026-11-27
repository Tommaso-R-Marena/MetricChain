# Consolidation assessment — Theoretical Research Division

*Branch `claude/determined-ride-og1u7j`.  Written 2026-11-27 under the research owner's directive
"Controlled Consolidation and Temporary Research Halt".  Everything said to be verified here refers
to the tree whose audit passed on 2026-11-27 01:00 UTC (`bash scripts/audit_all.sh`: "AUDIT PASSED";
92 Lean files, 49 334 lines, 5068 declarations and 696 headline theorems on the three standard axioms;
192 harness tests; 618 mutations, 617 caught and one expected pass).  All reviews named are internal
AI reviews or reviews by other AI divisions of this programme — **none is external peer review**, and
no human mathematician has read any proof.  Labels: **[V]** machine-checked in Lean; **[P]** paper
proof; **[N]** numerical; **[M]** measured by another division.*

## A. Executive assessment

The division produced two things of different kinds.

1. **A machine-checked library of certificate kernels** (Lean 4 with Mathlib): executable checkers,
   with soundness theorems, for lower bounds on the minimum energy of a discrete pairwise model, for
   two-sided enclosures of its partition function, and for barriers — in versions that hold *for
   every member of a stated class of unknown residuals*.  This part is solid as mathematics about the
   stated objects; its rules are classical (dead-end elimination, branch and bound, bucket
   elimination, cuts), and what is plausibly new is narrow: the class-robust form and the fact that
   the kernel's semantics are machine-checked.
2. **A worst-case theory of how many energy evaluations a certified free energy costs** when the
   energy is known only up to a Lipschitz-type residual: exact exponents for sampling fixed in
   advance, for verification with a hint, and for adaptive algorithms without a hint (which reach the
   hinted exponent through a recursion of nested levels with a sharp `1/k²` law); extensions to
   fields, mean-field and chain known parts, several site types and rounds of adaptivity; and the
   boundary of the method (where nesting gains nothing, and where it returns false certificates).
   This part is a body of paper proofs that survived repeated adversarial AI review, with machine-
   checked lower bounds and recursions.  **It is mathematics about an idealised class** (a product of
   binary sites, a Hamming-Lipschitz residual, exact evaluations, the worst case).

What it has *not* produced: any statement about a molecule; any algorithm that is competitive at a
size where it can be run (the nested algorithm is worse than plain Monte Carlo up to about `2·10⁴`
sites by the Computational Research Division's exact recursion); any externally confirmed novelty.
Early claims of novelty were withdrawn after review several times (D11, D12, D24: the "certification
geometry" is polytrope and tropical geometry and Lipschitz extension; realizability and
torsion-to-RMSD bounds are classical).  The cheap residual classes for which the theory is sharp do
not contain the physics measured so far (the Scientific Discovery Division: an implicit-solvent term
has class constants of 12 to 53 `kT` per site).  The practically consequential use of the theory to
date is indirect: its share and sandwich lemmas are what the science division's certified free
energies of small rotamer models run on.

## B. Strongest contributions, ranked

### B1. The adaptive query complexity of a certified partition function on the cube class

* **Contribution.**  For `A(ψ) = 2^{−n}Σ_x e^{−ψ(x)}` with `ψ` any `u`-Lipschitz function on the `n`-cube, and
  randomised algorithms that return a bracket of ratio `e^ε` with probability `1 − δ` from evaluations of
  `ψ`: (i) sampling fixed in advance costs `exp(n·a + o(n))`, `a = KL(p_u‖½)`, `p_u = 1/(1 + e^u)` (Theorems 11.44,
  11.45); (ii) no algorithm, adaptive or hinted, beats `exp(n·h)`, `h` the exponent of the critical dip
  (Theorem 11.25); (iii) an adaptive algorithm without a hint reaches `exp(n·h + o(n))` by nested levels,
  and the exponent `τ_k` of `k` levels obeys a recursion that converges to `h` (Theorems 11.52–11.58);
  (iv) **`k²(τ_k − h) → 2π²h²θ_hint″(0)`** — a saddle-node bottleneck of a convex slope map (Theorems 11.53a,
  11.53b); (v) at finite `n`, `ln N ≤ n·h + O(n^{1/3}(ln n)^{2/3})`, with certified upper bounds for `τ_k` at
  every `k` (interval arithmetic) and `n·θ_hint(g) + O((ln n)²)` at an accuracy `g·n` (Theorem 11.58e).  At
  `u = 1`: `a = 0.1109`, `h = 0.0291`.
* **Where.**  `docs/THEORY_REPORT.md` §§11.16–11.19; `docs/workstreams/{H,K,Q,Q2,R,Z}_REPORT.md`, `Z_ADDENDUM.md` and
  their reviews; Lean: `nonadaptive_expected_queries_ge`, `cube_nonadaptive_bound`, `HintRecursion.lean`,
  `CubeHintPair.lean`, `LineDynamics.lean`, `BoundedAccuracy.lean`; `experiments/workstreams/Z/`; harness XVI.1–XVI.11.
  Audited checkpoints `07cde81` (twenty-fourth) and the consolidation commit.
* **Verification and review.**  Lower bounds and the convergence of the recursion **[V]**; the rate `O(1/k)`
  **[V]** by the Scientific Discovery Division on its branch (`RateFull.lean`); the algorithms, the sharp
  rate and the finite-`n` bound **[P]**, each refereed by one to three internal AI referees with independent
  code and three times by the science division (SCI-REV-0007, -0014, -0017) — final versions: no error of
  substance; many corrections of wording, constants and one closed form on the way (D63, D66, D68, and
  the errata of `Z_ADDENDUM.md`).
* **Assumptions.**  Uniform product measure on binary sites; one Hamming slope; exact evaluations; worst
  case over the class; bounded accuracy (or an accuracy `g·n`); `(ε, δ)`-correctness.
* **Closest prior art.**  Information-based complexity of integration (Bakhvalov; Novak — adaption does
  not help on convex symmetric classes, and can help otherwise); relative-error sequential Monte Carlo
  (Dagum–Karp–Luby–Ross); multilevel splitting, subset simulation and nested sampling; solvable
  integration problems (Kunsch–Novak–Rudolf 2019); Block and Shetty (arXiv 2602.23535) on certifying
  free energies by sampling from a model under a divergence bound; Harper's theorem.
* **Distinction.**  A worst-case statement over a Lipschitz class with *no sampler given*: exact
  exponents for the three regimes, the exact size of the gain from adaptivity (`h/a ≈ ¼` at small
  slopes), and a level recursion with a sharp rate.
* **Evidence for originality.**  Two prior-art sweeps (ours; the science division's SCI-REV-0004, -0006)
  found no statement of these exponents; the one cost table that was found in print (Block–Shetty)
  concerns another oracle model.
* **Evidence against.**  Every ingredient is classical (isoperimetry, Chernoff bounds, hidden-set lower
  bounds, splitting).  The literature was read by AI, mostly at the level of abstracts and
  introductions.  A specialist in information-based complexity may know the exponents as folklore.
* **Validation.**  Exact evaluation of the cost formulas (nests of two to seven levels, about six
  million node checks; two levels over the real base at `n = 50 000`); the engineering division's literal
  runs on cubes of 8 to 16 sites and its exact recursion to six levels at `n ≤ 8000`; replications by the
  science division.
* **Limitations.**  Not competitive at any size at which it has been run.  The constants of the
  finite-`n` theorem are far from what the exact recursion shows (47–50 `ln n` per level in the proof,
  one to two and a half measured).  Not transferred beyond the uniform cube at finite `n`.  The upper
  bounds are not machine-checked.
* **Before publication.**  A human expert in information-based complexity or rare-event simulation must
  read the level theorem (Theorem 11.56, about fifteen pages) and place the result against that
  literature; a self-contained manuscript of the exponent theorem and the rate (the finite-`n` theorem
  is a second paper, if at all).

### B2. Machine-checked certificate kernels for a class of residuals

* **Contribution.**  Executable checkers with soundness theorems: `verify_sound` (a certified lower
  bound on the minimum of a pairwise integer model: branch, leaf, prune); `verifyITop_sound` and
  `IProblem.consistent_iff_nonempty` (the same for every residual of an envelope class, with a check
  that the class is not empty); `verify_sound_real`, `verify_sound_real_symm` (transfer to real-valued
  tables that the rationals bound from below); second- and third-order classes
  (`verify_sound_secondOrder`, `verify_sound_thirdOrder`); linear classes (`verifyL_sound`);
  two-sided partition-function enclosures (`zverifyTop_sound`, `zverify2Top_sound`, `zprune_sound`,
  `exp_enclosure`; elimination of sites with one or two neighbours, cuts, thermal pruning) and, since
  this checkpoint, elimination for arbitrary summands (`sum_boxFinset_elim`); barrier certificates
  (`box_cut_barrier`, `box_trap_certificate`); the sharp-minimum theorem (Theorem 2.4,
  `robust_certified_iff`).
* **Where.**  `proofs/CertificateAlgebra.lean`, `proofs/Frontiers/Partition*.lean`, `BarrierCertificate.lean`,
  `BoxRatio.lean`, `FactorElimination.lean`; `docs/BLUEPRINT.md`; `experiments/reference_checker.py` with
  `experiments/certs/` (conformance vectors); THY-MSG-0020 (what is ready to implement, and what is not).
* **Verification and review.**  **[V]**; the axiom audit walks every declaration; an early independent
  adversarial audit; the science division re-ran the audit on its machine.  Implemented independently
  by the engineering division (an exact checker) and by the Structural & Computational Biology
  division (producer and checker; certificates on six structures).
* **Assumptions.**  Finite alphabets; integer or rational tables; the class constants (envelopes,
  anchors, shares) are *inputs*.
* **Closest prior art.**  Dead-end elimination, A* and branch and bound in protein design (OSPREY,
  toulbar2); pseudo-Boolean proof logging with a verified checker (VeriPB, CakePB); exact rational
  duals of the linear relaxation; min-max regret and interval-data optimisation; tropical and
  polytrope descriptions of sharp minima.
* **Distinction.**  One certificate for a whole class of residuals; kernel semantics machine-checked;
  partition functions two-sided in exact arithmetic.
* **Evidence for originality.**  The Frontier Benchmarking division's literature assessment found no
  published proof logging for cost-function-network or MAP solvers; the science division classes the
  class-robust certificate as "plausibly new, narrow".
* **Evidence against.**  The rules are classical.  A certified alternative exists (a pseudo-Boolean
  encoding with VeriPB and CakePB), and an exact dual of the linear relaxation is reported tight on
  most fixed-backbone side-chain instances.  Published evidence says an exact optimum improves
  side-chain accuracy by less than a tenth of a per cent over a heuristic one: **the expected value is
  auditability, not accuracy**.
* **Validation.**  Conformance vectors and a soundness fuzz in every audit; the software division's
  certificates (zero gap on six structures after dead-end elimination, by its account).
* **Limitations.**  A Lean theorem about a Lean function does not verify a production checker.  The
  step from a real energy function to the checked integers is proved only *given* entrywise lower
  bounds; no evaluator's rounding is verified.  Class constants for a concrete residual model are not
  certified by anything here.
* **Before publication or deployment.**  A measured comparison with the pseudo-Boolean pipeline on the
  same instances; a statement of the trusted computing base of a real checker; certified rounding.

### B3. Share certificates, sandwiches and the envelope sampler (the lemmas under the science division's certified free energies)

* **Contribution.**  (i) The remainder of an anchored expansion as an identity, and the allocation of
  a many-body term to tables on sub-tuples at every order (Theorems 11.18, 11.18a–11.18f): a term
  evaluated on a Hamming ball about an anchor and bounded elsewhere gives a sandwich of two tractable
  models.  (ii) Sampling where the bracket is (Propositions 11.113, 11.113a): with a sandwich of two
  sampleable models, the evaluations needed for a certified `ln Z` are governed by the width of the
  bracket, in a variance-sensitive form, and nest.  (iii) Costs and ratios in box classes (Theorems
  11.110–11.115).
* **Where.**  Theory report §§11.6, 11.30, 11.31; Lean: `HigherOrderEnvelope.lean`, `ShareLevels.lean`,
  `StateShares.lean`, `DownClosedRemainder.lean`, `BoxRatio.lean`, `GibbsRecovery.lean`, `Bonferroni.lean`.
* **Verification and review.**  The share lemmas and remainder identities **[V]**; the sampler bounds **[P]**,
  reviewed by the science division (SCI-REV-0012, -0013, -0015: two sentences of ours were wrong and were
  replaced).
* **Use [M, the science division's].**  Twenty valines (`3.5·10⁹` assignments) within `0.055` nats from
  9 921 evaluations; Lys₁₂: `ln Z` in an interval of `3·10⁻⁵` nats with 19 to 60 further evaluations.
* **Prior art and distinction.**  K\* approximations with provable ratios, tuple expansions, pairwise
  decompositions of generalized-Born energies, Hoeffding and Bennett stopping rules (the science
  division found that the K\* stopping criterion is one of these brackets, and that the cost table is in
  print).  What is ours is the machine-checked allocation at every order and the nested bracket; the
  combination into a certificate is the science division's.
* **Limitations.**  Fixed backbone; small or weakly charged instances; the certificate removes
  sampling error only — by four to five orders of magnitude more than the model's accuracy warrants.
* **Before publication.**  This is a component of the science division's result, not a standalone one.

### B4. Where the method works and where it cannot: the abstract level theorem and its boundary

* **Contribution.**  The level theorem needs four facts about an outer integrand on a probability
  space and nothing else (Theorem 11.118); it applies to products with an additive envelope, to
  dependence under a class-relative influence (11.119), and **not** to a Euclidean envelope on Gauss
  space, where nesting over a fixed split provably gains nothing (11.120); under an influence that is
  not certified it returns **false certificates** (11.121).  Known parts: with a field the worst case
  without a hint equals the hardest case with a hint, which is not the zero residual (11.61–11.65);
  several site types and larger alphabets (a Rényi-capacity form; 11.95–11.101); chains (11.116–11.117);
  two rounds of adaptivity lie strictly between a fixed sample and full adaptivity (11.86,
  `TwoRounds.lean`).
* **Verification and review.**  **[P]**, refereed internally and by the science division (SCI-REV-0001,
  -0002, -0003, -0005, -0010, -0027); parts **[V]** (`TwoRounds.lean`, Theorem 11.116(a)–(c), the science
  division's files for Theorem 11.109a).  SCI-REV-0027 found three sentences of §11.33 wrong (applied;
  D70) and supplied the usable rule for band models: condition on the boundary layer.
* **Prior art.**  Ahlswede–Zhang and Yu (exponents of isoperimetry in product spaces); Gaussian
  isoperimetry; channel coding; rounds of adaptivity for partition functions in the sampling-oracle
  model (2026 preprints, with the opposite conclusion at polynomial scale).
* **Limitations.**  Asymptotic; nothing with a field or a chain has been run end to end; for band
  models nesting is valid in the conditioned form and worth nothing at the lengths certified so far.

### B5. (newest, unrefereed) Tail functions beyond the uniform cube by induction over the sites

* **Contribution.**  A two-point recursion over the sites gives valid growth bounds and both tail
  functions of the level theorem on any finite product with a product measure and an additive cost;
  it reproduces Harper's theorem numerically and is attained on exhaustive small instances; the
  lower tail function has a closed form by an exact tensorisation; negative results (no Harper
  theorem for the biased cube in the concentration regime); a conjecture with numerical support
  (Proposition 11.124; `docs/workstreams/I_REPORT.md`; harness XXVII.1, DEAD.29).
* **Status.**  **[P]** for validity, the coordinator's own, **unrefereed**, one day old; the induction and
  the tensorisation are classical methods (Bollobás–Leader; Marton; Yu) and no novelty is claimed for
  them.  Listed fifth because it is the only item here that removes a standing restriction (the
  uniform cube), not because it is established.

## C. Negative results and rediscoveries

* **Rediscoveries, withdrawn.**  The geometry of robust certification (sharp minima as polytropes,
  Lipschitz extension, tropical convexity): D11, D12, D24.  Realizability and torsion-to-RMSD bounds:
  classical, and loose (a bound of `19.6` against an actual `2.0`).  The cost table for sampling under a
  divergence bound: Block–Shetty.  Theorem I3 of workstream I: Marton's coupling.
* **False statements of ours, found by review** (all recorded in `docs/DEAD_ENDS.md`, D1–D70): among the
  consequential ones — completeness of shares on non-product domains (D-entry with SCI-REV-0012); a
  wrong dependence in the box-class ratio (SCI-REV-0013); "a hub is not a counterexample" and the
  single mechanism of the false certificate (D70); two "needed only by the proof" tags of the
  assumption audit that are needed by the statements (D67); a "Harper theorem for the biased cube"
  (D69); a closed form for the second level that fails for large slopes (the last referee).
* **Unfavourable comparisons.**  The nested adaptive algorithm is not competitive at any size at which
  it can be evaluated.  For Lipschitz classes on Gauss space with a Euclidean envelope nesting gains
  nothing.  On band models nesting needs conditioning and then pays only beyond roughly a hundred
  sites (the science division's estimate).  A second-order certified bound for many weak pair terms
  loses at first order beyond a constant oscillation per site (the Complexity division).
* **Deprioritise or abandon.**  Further second-order refinements of the cube theory (the uniformity
  in the accuracy; effective constants; the exact recursion with an inner tolerance); rounds of
  adaptivity beyond two; machine-checking the algorithmic upper bounds; realizability and RMSD
  bounds; nesting on Gauss space; anything that presents an exponent as a cost prediction for a
  molecule.

## D. Practical opportunities

| capability | mathematical possibility | implemented | synthetic validation | realistic computation | experimental evidence |
|---|---|---|---|---|---|
| certified minimum-energy conformation of a rotamer model, with a checkable certificate | yes **[V]** | reference checker here; producers and checkers at the engineering and software divisions | conformance vectors, fuzz | six structures (software division) | none; published evidence says exactness does not improve accuracy |
| certified two-sided `ln Z` and populations of a rotamer model | yes **[V]** for trees, width two, cuts, pruning; general elimination as an identity **[V]** | kernel in Lean; table-level elimination not implemented here | small instances | crambin plausible at a 1 kcal/mol threshold, ubiquitin not (software division's measurement) | none |
| certified free energy with an expensive many-body term (sandwich and envelope sampler) | yes (**[V]** shares, **[P]** sampler) | by the science division | enumerable instances | peptides of 12 to 30 residues, fixed backbone **[M]** | none |
| certified barriers on a discretised landscape | yes **[V]** | reference only | lattice and voxel models | none | none |
| adaptive nested estimation of a free energy | yes **[P]** | simulators at engineering and science | cubes of 8 to 16 sites | not competitive | none |

The shortest credible path to something demonstrably useful is the second row joined to the first:
an end-to-end certified enclosure of `ln Z` for one small protein in a standard energy model, with
every hypothesis of the certificate checked by a program — its value being auditability.

## E. Recommended next actions (at most three)

**E1. An external human review of the adaptive-complexity theorem, and a manuscript.**
*Objective:* decide whether B1 is correct and new.  *Prerequisites:* the theory report §§11.16–11.19
and the workstream reports with their reviews.  *Missing:* a self-contained text of about thirty
pages (the exponent theorem, the level theorem, the rate), and a reader who knows information-based
complexity.  *Baselines:* the literature named in B1.  *Success:* an expert finds no error and no
prior statement of the exponents; *failure:* either.  *Reasoning:* moderate — drafting can be done by
Opus from the existing texts; checking a proof step against an objection needs the stronger model.
*Computation:* none.  *Dependencies:* none.

**E2. One end-to-end certified `ln Z` on a small protein, with the chain of trust closed** (with the
software, engineering and science divisions).  *Objective:* a certificate for crambin in a fixed
energy model whose every hypothesis — rounding of the energies, pruning, elimination, the final
enclosure — is checked by an independent exact program.  *Prerequisites:* `zprune_sound`,
`sum_boxFinset_elim`, `sum_boxFinset_relax`, `exp_enclosure`, the software division's producer.
*Missing:* a table-level elimination checker tested against enumeration; a rounding step with a
proved direction for the energy evaluator in use; the kernel type for factors of bounded arity if a
Lean-executable checker is wanted.  *Baselines:* K\* (OSPREY), toulbar2 with a pseudo-Boolean proof
log, exact enumeration on sub-systems.  *Benchmark:* crambin (26 flexible sites after pruning), then
the instances of the software division's table.  *Success:* a two-sided enclosure of `ln Z` within
`0.1` nat accepted by a checker that shares no code with the producer; *failure:* no decomposition
with tables below about `10⁸` entries, or a width above one nat.  *Reasoning and computation:* not
estimable here — the software and engineering divisions hold the measurements.  *Model:* the software
work can continue on Opus; mathematical obstructions (a missing rule, a bound that fails) are where
the stronger model pays.

**E3. Only if the theory line is continued: prove or refute Conjecture I6.**  *Objective:* a
closed-form growth bound with polynomial precision on every finite product space (tail functions
for heterogeneous sites).  *Prerequisites:* `docs/workstreams/I_REPORT.md` (the exact step for a fixed
dual variable; the defect as a Bregman gap; numerics to `n = 1000`).  *Missing:* a bound of the defect
that is uniform at the corners.  *Baselines:* Harper's theorem (the cube); Yu's exponents.
*Success:* a proof with an explicit constant, or a counterexample from the search in
`i5_defect_corners.py`; *failure criterion:* no proof after one focused attempt with a referee.
*Reasoning:* one focused session of the stronger model plus one referee.  *Computation:* local.
*Dependencies:* none.  This is the one open problem of the division with a clear path and standalone
interest; it does not by itself make anything useful for a molecule.

Not recommended: more levels, more exponents, more Lean for the algorithmic upper bounds.

## F. Publication readiness

* **B1 (adaptive complexity).**  The only candidate for a mathematics paper.  Needs E1: a human
  expert, a literature placement that an AI reading cannot give, and a decision whether the
  machine-checked parts (lower bounds, recursion, the rate `O(1/k)`) are presented as such.  Formal
  verification covers the lower bounds and the recursion, not the algorithm; it says nothing about
  novelty.
* **B2 (kernels).**  A tool or formal-methods paper is defensible only with a measured comparison
  against pseudo-Boolean proof logging and a real checker's trusted base; the class-robust
  certificate is the distinguishing feature and needs one worked instance with *certified* class
  constants.
* **Two rounds of adaptivity (Theorem 11.86).**  A short note, conditional on B1.
* **Workstream I.**  Not ready: unrefereed; prior art not searched for its two open statements.
* Nothing else is standalone.

## State at the halt

Strongest unresolved problems: (1) is `n·h + Θ(n^{1/3})` the true second-order cost, or an artefact of
block nesting (nothing is known for all algorithms between `n·h − O(1)` and the upper bound);
(2) Conjecture I6; (3) certified class constants for one real residual model; (4) a certified
third-order remainder for many weak pair terms on a correlated reference.  The handoff is
`docs/RESEARCH_LOG.md` ("Resume here"), `docs/collaboration/status/theory.md`, `docs/DEAD_ENDS.md` and
`docs/ASSUMPTION_AUDIT.md`.  No subagent, background process, scheduled session or computational job
of this division remains active after the consolidation commit.
