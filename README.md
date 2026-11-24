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
| the independent referee report on the first phase | [`docs/reviews/R1_referee_report.md`](docs/reviews/R1_referee_report.md) |

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
                        thermal robustness), second-order envelopes, and the partition
                        kernel with cut and elimination rules
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
rules, which make it exact on chains, trees and interaction graphs of treewidth at most two),
with voxel enclosures of continuous integrals.

**Theory, first phase.**  Exact characterisations of robust optimality under an envelope
(contact-set, sharp-minimum and query-model theorems), the necessity of decomposition rules
(exponential separations), sharp free-energy sandwiches for product references, torsion-to-RMSD
certificates.  An independent referee report (`docs/reviews/`) found no machine-checked statement
false but classified this mathematics as elementary or classical in substance, and four prose
claims as overstated; the corrections are in the report and in `docs/DEAD_ENDS.md` (D21–D27).

**Theory, second phase (theory report §§10–12).**  *What can residual evaluations certify?*
Certificates are coverings in a slack quasi-metric with radii equal to the points' own
optimality gaps; with only a first-order envelope, on product landscapes one evaluation suffices
iff every site is sharp and otherwise exponentially many are needed, with an exact exponent
(a rate–distortion function); at finite temperature, for accuracies that are not exponentially
small, the same formula holds with the energy gap replaced by the free-energy gap of a
macrostate (a corollary of a known source-coding theorem on exponential moments of distortion),
and the count is at least the exponential of the entropy; minimal certificates are NP-hard to find and best-first search is competitive only
with covers at shrunk radii.  The way out is the order of the envelope: with bounded mixed
second differences, `n(k−1)+1` evaluations give an exact reduction to the pairwise kernel.  The
one-shot lower bounds, the search guarantee and the second-order reduction are machine-checked;
the matching upper bounds of the two exponent theorems are paper proofs (type covering) checked
numerically.  The tools are standard and the proofs short; §12 of the report says what a
publication would still need.

What is *not* established: the guarantees are relative to published inputs (rational tables,
envelope constants, anchor values); certifying envelope constants for a concrete learned residual,
interval evaluation of force-field terms over voxels, and any claim of practical solver
performance are outside the development.
