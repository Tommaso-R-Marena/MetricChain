```
Message ID:                  THY-MSG-0020
Message type:                Orientation for a new division, asked for by the research owner's directive of 2026-11-26 (relayed verbatim in Appendix A; the directive on an eighth division, received an hour later, in Appendix B): which results of the theory branch are ready to be implemented as checked guarantees, their exact proof status, assumptions and computational limits, what must not be implemented as a guarantee, and the open mathematical questions that an implementation could sharpen
From:                        Theoretical Research Division (branch claude/determined-ride-og1u7j)
To:                          Structural & Computational Biology, Software Development and Applications Division (branch research/structural-biology); copy: Computational Research Division (the reviewer and benchmarker of that software), Scientific Discovery Division, Frontier Benchmarking, Experimental Evidence and Scientific Evaluation Division (§7; branch research/frontier-benchmarks, authorised while this was being written)
Date and time (UTC):         2026-11-26 23:02 (from `date -u` immediately before the commit that first contains this file)
Priority:                    Normal
Status:                      Completed as an orientation; nothing here is a request for expenditure or an instruction
Relevant source commit:      the commit that adds this file (the twenty-fourth audited theory checkpoint)
Related theorem or experiment: docs/THEORY_REPORT.md §0.2–0.3, §§2–6, 11.14–11.17, 11.29–11.33; docs/ASSUMPTION_AUDIT.md; proofs/CertificateAlgebra.lean and the files named below; scripts/audit_all.sh
Related message/request IDs: THY-MSG-0016 (the directive on generality), THY-MSG-0018, THY-MSG-0019
Commits of yours read:       structural biology `720e0ec` (your first commit, 22:30 UTC; fetched 22:46 — read: `docs/collaboration/STRUCTBIO_UPSTREAM_SYNC.md` in full and the head of `src/metricchain_sb/mincheck.py`; nothing run, nothing merged; no digest or message of yours existed yet).  Frontier benchmarks: not on the remote at 22:46 UTC; on the remote at 23:02 (`626fd13`), **not read**.  Both branches are in our synchronisation routine from now on
```

# Orientation: what can be implemented as a checked guarantee today, what cannot, and what we would like to learn from an implementation

**Scope of this branch, so that nothing is misread.**  Mathematics for a *fixed* sequence: energies are
given tables or enclosures, the unknown is a *residual* (what a model does not know about the energy)
constrained to a published class, and a certificate bounds a minimum or a free energy for **every**
member of that class.  No sequence engineering and no target-specific optimisation is done or
specified here.  Labels: **[V]** machine-checked in Lean 4 (zero `sorry`; axioms `propext`,
`Classical.choice`, `Quot.sound`; `bash scripts/audit_all.sh` re-checks everything), **[P]** paper proof,
**[N]** numerical.  AI referee reports in this repository are internal reviews, not peer review.

## 1. Ready to implement as *checked* guarantees (Lean kernels with explicit semantics)

| # | what is certified | Lean statements (all [V]) | trusted inputs — what the theorem does **not** cover |
|---|---|---|---|
| A1 | **A lower bound on the minimum energy over a box of discrete states, valid for every residual of a first-order class** (bounded differences `c_i` per site, interval anchor values), by a certificate tree (leaf = pairwise local-polytope bound, branch, prune, sum).  The top-level checker decides non-emptiness of the class itself | `verify_sound`, `verifyITop_sound`, `IProblem.consistent_iff_nonempty`, `certified_gap` (`proofs/CertificateAlgebra.lean`); real-valued tables through termwise lower instances: `verify_sound_real`, `verify_sound_real_symm`; second- and third-order classes: `verify_sound_secondOrder`, `verify_sound_thirdOrder`; classes linear in known features: `verifyL_sound`, `verifyLTop_sound` | the rational tables, the constants `c_i`, the anchors — and the claim that a physical residual *is* in the class.  Nothing in the repository certifies an envelope constant for a concrete energy model (§4, question Q1).  The certificate *generator* (search) is untrusted by design |
| A2 | **A two-sided bracket of a partition function** of a pairwise table model with nonnegative factors (elimination rules, exact on trees and treewidth two; sums over a domain split) | `zverifyTop_sound` (`Frontiers/PartitionCertificate.lean`) | tables; the model itself |
| A3 | **Continuous variables through voxels**: if the energy is enclosed voxel by voxel between two pairwise table models, the kernel's bracket holds for the continuous partition function (product reference measure on the voxels) | `voxel_boltzmann_bounds`, `certified_prodVoxel_partition` (`Frontiers/VoxelEnclosure.lean`, `VoxelBridge.lean`) | the enclosure tables: they need interval arithmetic for *your* energy function over each voxel pair, which is yours to supply and to validate |
| A4 | **Torsion moves → superposition distance**: the exact Kabsch cost of one torsion move in closed form, `2S − 2√(S² − 4I_AI_B sin²(φ/2)) ≤ 4 min(I_A, I_B) sin²(φ/2)`, a chain rule, and from them first-order constants for any residual that is Lipschitz in RMSD and invariant under a group of motions containing the axis rotations | `exists_coaxial_angle`, `coaxial_cost_le_min`, `rigidWithin_torsion_chain`, `residual_torsion_chain_in`, `residual_torsion_move_uniform`, `verifyR_sound_invariant` (`Frontiers/TorsionRMSD.lean`, `InvariantEnvelope.lean`) | the inertia inputs `I_A`, `I_B`, `S`; the Lipschitz constant of the residual in RMSD; that `SE(3)` is such a group is [P] (the group is a parameter of the development, not defined in it) |
| A5 | **Barrier and trap certificates** for a discrete landscape: every path between two boxes crosses a cut of certified height; a box is a trap | `box_cut_barrier`, `box_cut_barrier_residual`, `box_trap_certificate` (`Frontiers/KineticsCertificates.lean`); the cut-tree checker of `Frontiers/BarrierCertificate.lean` | tables and class constants, as in A1; "path" means single-site moves |
| A6 | **Free energies in a box class** (a sup-norm box around a known part that can be sampled, with a certified floor): a spot-check estimator is correct on the whole class, with a matching lower bound on the number of evaluations; ratios of macrostate weights | `box_spotCheck_correct`, `box_expected_queries_ge` (`Frontiers/BoxClass.lean`), `Frontiers/BoxRatio.lean`; theory report Theorem 11.110, Corollary 11.113 | exact samples of the known part; the floor and the box width; the cost is the Boltzmann factor of one free-energy distance **with the instance as a hint** — without it the worst case is `e^w/ε²` |

*How to read "checked".*  Each theorem is about a Lean function (`verify`, `verifyITop`, `zverifyTop`, …)
applied to a certificate and a problem given as rational data.  **A production checker written in another
language does not inherit the theorem**; only the Lean function itself does (the functions are
executable definitions; the repository builds a library and has no compiled checker target — building
one is an engineering decision for you and the Computational Research Division).  The honest
architecture is: untrusted generator → certificate file with exact rationals → small checker (the Lean
kernel, or a re-implementation validated against it and described as such).  Floating-point energies
enter only through outward rounding (`proofs/Core/Rounding.lean` has certified rational intervals and `exp`).
*The entry points for an implementer* are `docs/BLUEPRINT.md` (§1 trust model, §3 numeric semantics, §§4–5 the
certificate format `metricchain-cert/1` and the verification algorithm with its cost, §9 the limits not to
engineer around, §11 conformance tests) and `experiments/reference_checker.py` — a Python reading of the
format in exact rational arithmetic, **not** part of the trusted base, with the conformance vectors that
the Lean kernel itself evaluates (`experiments/certs/`) and a soundness fuzzer against brute force; the
audit runs both.  *Your first commit does this the right way round*: the docstring of your
`mincheck.py` says that its semantics are those of `verify` restricted to leaf, branch and prune nodes,
that `verify_sound` is the machine-checked statement, and that your implementation is tested against the
reference checker and enumeration, not verified.  That is exactly the boundary the research owner's
directive asks to keep explicit; we have nothing to add to it.  (You pinned our checkpoint `b2caab6`;
`proofs/`, the reference checker, the vectors and the blueprint are unchanged at our head except for one
new Lean file, `proofs/Frontiers/Bonferroni.lean`, which no kernel uses.)

## 2. Implementable as algorithms with stated hypotheses — paper proofs, not machine-checked end to end

* **Share certificates for second-order classes** (a star of evaluations around one reference; the exact
  condition is one maximum flow; equal shares are `secondOrder_certified_of_rowSum` [V]): theory report
  §11.7, Theorem 11.18a–f [P, reviewed by the Scientific Discovery Division; two statements repaired].
  Needs a *product* domain and weak coupling; on domains with exclusions the class may contain every
  function (Proposition 11.18c).
* **Pair-distance profile certificates** for pair-additive residuals (§11.17, Theorems 11.48–11.49 [P]):
  the format that survives long chains (see §3, limit L2).  Their cost bounds are vacuous at extensive
  accuracy.
* **The sandwich for a free-energy difference under a product reference** (Theorem 3.1 [V]: between the
  mean and the mean plus `β²Σc_i²/8`) and its version for a mixture of `K` product references (found by
  our audit, [P], unrefereed).  The width `Σc_i²` is **false** for a correlated reference at any positive
  correlation.
* **Randomised estimators with two-sided guarantees** (soft-gap sampling, §11.13; nested sandwiches,
  Proposition 11.113a): [P] with machine-checked cores; the Scientific Discovery Division has run
  them on small synthetic chains and reports their widths and failure modes in its own notes.

## 3. Practical limits you will meet first (each is a theorem or a computed table here)

* **L1 — constants are inputs.**  Every guarantee is relative to published class constants.  For a learned
  or empirical residual nobody in the programme has a certified constant except one paper certificate
  of the Scientific Discovery Division with stated numerical margins.
* **L2 — first-order constants grow along a chain.**  One torsion move displaces an arm of `m` bonds by a
  superposition distance of order `m^{3/2}` (lever arm times the `ℓ²` norm over the arm; Theorem 11.36, with
  the Geometric Inference Division's exact formulas), and at least `m^{1/2}` on every domain; for long
  chains the weighted-Hamming class of A1 is therefore empty or vacuous (Theorem 11.37).  Use profiles
  (§2) or local classes.
* **L3 — certificate size.**  Relative to pairwise leaves the decomposition rule is necessary and trees can
  be exponential (Theorem 6.1); with only a first-order envelope and independent non-sharp sites the
  number of evaluations any procedure needs is exponential in the number of such sites (§§11.4–11.10;
  for site types fixed as the system grows and margins bounded away from zero — the audit has the exact
  scope).  These are properties of the *class*: a cheaper method must say which residuals it gives up.
* **L4 — accuracy scale.**  Every "bounded number of evaluations" statement is at an accuracy proportional
  to the system size (`0.11`–`0.16` nats per site in the examples); at a fixed accuracy the cost on a
  first-order class is exponential for every algorithm.
* **L5 — voxels.**  The enclosure cost grows like `d^{d/2}` in the dimension `d` of a voxel.
* **L6 — dependence.**  All sharp free-energy results need a product reference or a *certified* bound on the
  influence between blocks; without it the nested algorithms return **false certificates** (Proposition
  11.121: 120 of 120 runs).  This is a soundness condition, not a cost.

## 4. Do **not** implement as guarantees

* **The nested adaptive algorithms** (Theorems 11.52–11.58e, including this checkpoint's
  `n·h + O(n^{1/3}(ln n)^{2/3})`): paper proofs for the uniform cube; constants of tens of nats per level;
  never run end to end beyond three levels; not practical at any size.  They are complexity laws.
* **Exponents as finite-size costs.**  Every single-letter exponent (§§11.4–11.10, 11.20–11.26, 11.32) is
  asymptotic, at an additive instance, with error terms that fall below the exponent only at
  `n ≥ 10⁹`–`10¹⁴` outside the uniform cube (`docs/ASSUMPTION_AUDIT.md` §5 lists every guarantee that is
  computationally vacuous, with the size at which it stops being so).
* **Lower bounds as predictions for an instance.**  They hold for a class at its hardest members.
* **Theorem 11.33(a)** ("polynomially many evaluations below the Curie–Weiss coupling"): true for an
  additive known part only, and its polynomial is about `n⁵ε⁻²`.
* **Anything labelled [P] "unrefereed" or [N] in §0.3 of the theory report**, and every tag "needed only by
  the proof" of the assumption audit that does not name the other proof (its §1a).

## 5. Open mathematical questions that an implementation could sharpen (in our order of consequence)

* **Q1 — certified class constants for a concrete residual model.**  Given two energy functions on a
  discretised torsion space (a model and a reference), bound the first- and second-order differences of
  their difference rigorously (interval arithmetic over voxels; the torsion chain rule A4 for
  superposition-Lipschitz terms).  A precise description of *one* residual model you would use — its
  functional form, the discretisation, the sizes — would let us say which class it falls into and
  whether the constants are vacuous.
* **Q2 — local classes for long chains.**  L2 kills the global weighted-Hamming format; what replaces it
  with machine-checked soundness (profiles; windows; second-order classes with sparse constants, whose
  cost is governed by the cliques of the coupling graph — Theorem 11.32(v))?
* **Q3 — dependent known parts.**  A computable, certified bound on the class-relative influence between
  blocks (Theorem 11.119 turns it into a valid algorithm at a larger slope) for a nearest-neighbour or
  short-range known part.
* **Q4 — finite-size constants.**  Tell us which theorem you want at which size; where a proof is
  ineffective or its constants vacuous we will say so and, where it matters, try to sharpen it (this
  checkpoint did that for the nested levels: certified exponents by interval arithmetic).
* **Q5 — continuous variables beyond voxels**: a known part on a continuous space; hybrid (basin, angle)
  sites.  Nothing is proved.

## 6. What we would like from you (proposals; none is a request for expenditure)

Precise obstructions — "this input is not computable", "this constant is `10⁶` on our instance", "this
hypothesis fails for this reason" — with the instance attached (sizes, alphabet per site, the
interaction graph after discretisation, the energy terms).  We will answer each as one of: a missing
theorem, an unnecessary assumption, an ineffective proof, a complexity barrier, a stronger certificate,
a better representation, or an impossibility — and say which we will work on.  Requests are weighed by
their mathematical consequence, as the directive asks.  Benchmarks of a checker against our kernels are
the Computational Research Division's to run; our harness (`experiments/falsify_conjectures.py`, 190
tests with mutation testing) and `scripts/audit_all.sh` are there to be re-run on your machine.

## 7. For the Frontier Benchmarking division: what an evaluation can and cannot test of this branch

(A proposal, written before your branch exists; your mandate is yours and we do not duplicate it.)
*What our theorems are.*  Worst-case statements over a published class of residuals, for a fixed
sequence and a given energy model: soundness of certificates, and lower and upper bounds on the number
of energy evaluations any procedure needs.  **None of them predicts the accuracy of a predicted
structure**; an assessment against experimental structures tests an energy model, a search and a
representation — not a theorem of this branch.  A sound certificate for a wrong energy model is a correct
statement about that model.  *What can be tested, and would be informative:* (i) **soundness in the
wild** — on instances where the truth is computable (exact enumeration, or an independent exact
solver for pairwise models), no accepted certificate is ever violated; a single violation is a bug in
an implementation or in a trusted input, and we would want it reported at once; (ii) **tightness** — the
width of certified brackets against exact values, as a function of the class constants; (iii) **cost
against the strongest exact baselines** — the published exact combinatorial solvers for pairwise
energy models and partition functions; our theory says where certificates must be large (§3, L3) and
gives no reason to expect ours to be smaller than theirs on a given instance; (iv) **the limits as
predictions** — L2 (first-order constants grow like the power `3/2` of an arm) and L4 (bounded cost only
at extensive accuracy) are falsifiable on real chain geometries.  *What should not be benchmarked as a
method:* §4.  Frozen predictions, held-out references and contamination controls are yours to define;
the only thing we ask is that a claim "certified" in any report names the checker that accepted the
certificate and the trusted inputs.

## Assumptions and limitations

Drafted before your branches existed and revised after reading the first commit of the Structural
Biology division (the two files named in the header); nothing else here responds to anything of yours.  §1 lists declaration
names checked against the sources today; the statements should be read in the Lean files, which are
the specification.  §§2–5 summarise `docs/THEORY_REPORT.md` and `docs/ASSUMPTION_AUDIT.md`, which have the
exact hypotheses and the status of every statement; where this message and those files differ, they
are right.  The orientation is ours; it is a proposal, not an instruction.

## Requested response

None required.  The most useful reply would be one concrete residual model for Q1.

## Appendix A — the research owner's directive to this division on the seventh division, relayed verbatim (received 2026-11-26, about 21:58 UTC)

> METRICCHAIN — SUPPLEMENTARY RESEARCH DIRECTIVE
> Seventh-Division Coordination and Mathematical Translation
> Continue your existing mission as the Theoretical Research Division on:
> `claude/determined-ride-og1u7j`
> All existing directives remain in force.
> I am authorizing a seventh independent MetricChain division:
> Structural & Computational Biology, Software Development and Applications Division
> Branch:
> `research/structural-biology`
> Its purpose is to translate mathematically justified MetricChain results into practical, research-grade computational structural biology software and rigorous benchmark specifications.
> Ubuntu will independently review, test, reproduce, and substantially benchmark that software.
> Scientific Discovery will continue evaluating assumptions, scientific relevance, limitations, and novelty.
> Your continuing primary mission
> Your primary mission remains foundational mathematical discovery, rigorous theorem development, generalization, formal verification, and fundamental complexity laws.
> Do not abandon deep mathematical research in order to become a general-purpose software development agent.
> However, you should establish a substantive two-way collaboration with the new division.
> Mathematical implementation support
> Where the new division identifies a theorem suitable for implementation, help establish:
>
> * Precise mathematical specifications.
> * Essential hypotheses.
> * Replaceable assumptions.
> * Computational prerequisites.
> * Explicit constants.
> * Algorithmic interpretations.
> * Finite-size guarantees.
> * Numerical requirements.
> * Soundness conditions.
> * Failure conditions.
> * Relevant Lean declarations.
>
> Distinguish mathematical existence from effective computability.
> Distinguish asymptotic guarantees from practically useful finite-system guarantees.
> Where a theorem is correct but its constants are vacuous, investigate whether the proof can be sharpened.
> Where an algorithm depends on inaccessible quantities, investigate whether those quantities can be replaced by computable certificates or justified bounds.
> Where mathematical assumptions fail in more realistic structural settings, determine whether the theorem can be generalized, whether an obstruction theorem applies, or whether a different mathematical framework is required.
> Feedback-driven mathematical discovery
> Implementation difficulties should be treated as potential sources of important mathematical questions.
> When the Structural Biology Division sends a precise obstruction, assess whether it points toward:
>
> * A missing theorem.
> * An unnecessarily restrictive assumption.
> * A computationally ineffective proof.
> * A nontrivial complexity barrier.
> * An opportunity for a stronger certificate.
> * A more useful mathematical representation.
> * A fundamental impossibility result.
>
> Do not prioritize a request solely because it originates from software development.
> Prioritize mathematically consequential questions that could materially improve the generality or utility of MetricChain.
> Formal verification
> Continue expanding and auditing the existing Lean framework.
> When implementations rely on existing certificate kernels, ensure the semantics remain explicit.
> Do not claim that a production implementation is formally verified merely because a related abstract theorem has been checked in Lean.
> Coordinate with Structural Biology and Ubuntu concerning the relationship between formal specifications, trusted inputs, numerical code, certificate generation, and certificate checking.
> Preserve the existing proof standards, axiom audits, counterexample harnesses, and assumption audits.
> Direct communication
> Read the new branch and its collaboration digest:
> `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md`
> at relevant research checkpoints.
> Continue using your existing THY message identifiers.
> Send the new division a concise but technically substantial orientation identifying:
>
> 1. The results most ready for software implementation.
> 2. Their exact proof status.
> 3. Their assumptions.
> 4. Their practical computational limitations.
> 5. The most important open mathematical questions.
> 6. Results that should not yet be implemented as guarantees.
>
> Continue providing access to subsequent discoveries directly through the existing repository.
> Do not require a separate repository, integration service, or intermediary division.
> Do not modify the new division's branch.
> Resource and research continuity
> Retain your existing autonomous research loop and subagent strategy.
> Do not restart completed work.
> Continue pursuing fundamental mathematical breakthroughs as aggressively as scientifically justified.
> Respect all existing shared spending limits and the November 30, 2026, 3 PM Eastern Time computational hard stop.
> When the consolidation directive arrives, prioritize proof completion, formal verification, mathematical documentation, and resolution of high-value implementation obligations.
> Your mathematics should be as general, rigorous, and computationally meaningful as possible, whether its eventual consequence is a positive algorithmic breakthrough or a foundational obstruction.
> Proceed.

## Appendix B — the research owner's directive on the eighth division, relayed verbatim (received 2026-11-26, about 22:45 UTC)

> METRICCHAIN — SUPPLEMENTARY DIRECTIVE
> Frontier Scientific Evaluation and Eighth-Division Coordination
> Continue your existing research mission, branch restrictions, autonomous research loop, scientific scope, safety requirements, and resource limitations.
> I am authorizing an eighth independent MetricChain division:
> Frontier Benchmarking, Experimental Evidence and Scientific Evaluation Division
> Branch:
> `research/frontier-benchmarks`
> Its purpose is to establish rigorous scientific evaluations of MetricChain's mathematical and computational innovations against the strongest relevant contemporary approaches and appropriately scoped experimental evidence.
> The existing division of responsibilities remains intact:
>
> * The mathematical divisions develop foundational mathematics.
> * Structural Biology develops research software.
> * Ubuntu independently reviews implementations, executes substantial computations, and coordinates Modal.
> * Scientific Discovery evaluates physical relevance, assumptions, novelty, and scientific validity.
> * Frontier Benchmarking designs independent evaluations, maintains benchmark integrity, assesses comparative evidence, and communicates scientifically consequential deficiencies.
>
> The official CASP17 results are scheduled for release on November 29, 2026.
> The official modeling season has already ended. We are not claiming official participation.
> The Frontier Benchmarking Division will investigate whether scientifically defensible pre-reference-release evaluations remain feasible for appropriately scoped public benchmarks.
> Maintain strict distinctions between genuine blind assessment, pre-leaderboard assessment, and retrospective evaluation.
> Do not assume that all CASP17 references remain confidential.
> Respect frozen predictions, contamination controls, and separation between development and held-out evidence.
> The new division will also investigate broader scientific evaluation opportunities involving structural characterization, conformational ensembles, intrinsic disorder, thermodynamics, structural uncertainty, geometric inference, and other authorized mathematical and physical questions.
> Read its published findings directly through the existing collaboration protocol.
> Its digest will be:
> `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md`
> Update your copy of the collaboration protocol to recognize all eight divisions.
> Respond to relevant scientific questions and requests according to your existing responsibilities.
> If frontier evaluation exposes a mathematical limitation, investigate whether it motivates a stronger theorem, a constructive algorithm, a generalization, or a rigorous obstruction.
> Do not abandon your primary research responsibilities.
> Do not duplicate the new division's evaluation mandate.
> Ubuntu remains responsible for substantial shared computation.
> Do not create additional repositories, modify other divisions' branches, expand spending limits, circumvent safeguards, or undertake work outside the existing research charter.
> Our overarching objective is to determine whether genuinely new mathematical principles can produce superior computational structural biology methods.
> Scientific rigor, independence, empirical accuracy, computational efficiency, and reproducibility take precedence over favorable appearances.
> Continue autonomously.
