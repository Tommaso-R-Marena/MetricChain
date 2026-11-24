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

## Layout

```
lakefile.lean, lean-toolchain, lake-manifest.json   Lean 4.31.0 + Mathlib v4.31.0 (pinned)
proofs/Core/            partition-function vocabulary; outward rounding, rational intervals,
                        certified exp, rational atlas of the circle
proofs/Frontiers/       envelope duality, dominance calculus, free-energy sandwich, Hölder
                        decomposition, partition-function kernel, voxel enclosures and the
                        voxel bridge, Hoffman–Wielandt, realizability, holonomy,
                        torsion-to-RMSD, invariant-residual envelopes,
                        proof complexity of certificates
proofs/CertificateAlgebra.lean   executable verification kernels + Master Soundness Theorems
proofs/AxiomAudit.lean           automatic axiom audit of every declaration + non-vacuity witnesses
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

The audit fails if any file under `proofs/` contains `sorry`/`admit`/`native_decide`/a user axiom
or produces Lean's incomplete-proof warning, if a module is not imported by the axiom audit, if
any declaration in the `MetricChain` namespace (the non-vacuity witnesses included) depends on an
axiom other than `propext`, `Classical.choice`, `Quot.sound`, if a registered conjecture is
falsified (or a documented dead end unexpectedly survives), if a mutation of the harness goes
undetected, if the stored conformance vectors differ from the reference checker's, or if the
documentation cites a Lean declaration that does not exist.  The script first checks itself:
planted violations must be detected.

## Status in one paragraph

Three verified certificate kernels with exact rational arithmetic — lower bounds on minimum
energies (reparameterisation bounds, branching, dead-end elimination, dual decomposition), the
same under an unknown non-decomposable residual known only through an envelope and evaluated
anchors, and two-sided bounds on partition functions including thermal dead-end elimination and
voxel enclosures of continuous integrals — together with the theory that says what such
certificates can and cannot achieve: exact characterisations of robust optimality (contact-set,
sharp-minimum and query-model theorems), a witness-size lower bound, the necessity of the
decomposition rule (exponential separation), and sharp free-energy sandwiches for product
references.  Several classical or recently published results are formalized along the way and
are labelled as such; an independent adversarial audit of the whole development, a re-audit of
the repairs, and the corrections both triggered are recorded in `docs/DEAD_ENDS.md` (D14–D19).

What is *not* established: the guarantees are relative to published inputs (rational tables,
envelope constants, anchor values); certifying envelope constants for a concrete learned residual,
interval evaluation of force-field terms over voxels, and any claim of practical solver
performance are outside the development.
