# MetricChain

Machine-verified theory and certificate kernels for fixed-sequence articulated chain molecules:
certified conformational energy minimisation, certified partition functions, realizability and
geometric stability — with every guarantee checked in Lean 4 + Mathlib.

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
                        decomposition, partition-function kernel, voxel enclosures,
                        Hoffman–Wielandt, realizability, holonomy, torsion-to-RMSD,
                        proof complexity of certificates
proofs/CertificateAlgebra.lean   executable verification kernels + Master Soundness Theorems
proofs/AxiomAudit.lean           automatic axiom audit of every declaration + non-vacuity witnesses
experiments/            adversarial counterexample harness, separation benchmarks
scripts/audit_all.sh    single-command audit
```

## Reproducing the audit

```bash
scripts/audit_all.sh          # lake build, token scan, axiom audit, harness, benchmarks, doc refs
scripts/audit_all.sh --full   # same with the long falsification pass
```

Requirements: the pinned Lean toolchain (via `elan`, or the release archive unpacked in
`~/.lean/`; see `scripts/lean_env.sh`), `lake exe cache get` for the Mathlib cache, and Python 3
with `numpy`, `scipy`, `mpmath`.

The audit fails if any module contains `sorry`/`admit`/`native_decide`/a user axiom, if any
declaration in the `MetricChain` namespace depends on an axiom other than `propext`,
`Classical.choice`, `Quot.sound`, if a registered conjecture is falsified (or a documented dead end
unexpectedly survives), or if the documentation cites a Lean declaration that does not exist.

## Status in one paragraph

Three verified certificate kernels with exact rational arithmetic — lower bounds on minimum
energies (reparameterisation bounds, branching, dead-end elimination, dual decomposition), the
same under an unknown non-decomposable residual known only through an envelope and evaluated
anchors, and two-sided bounds on partition functions including thermal dead-end elimination and
voxel enclosures of continuous integrals — together with the theory that says what such
certificates can and cannot achieve: exact characterisations of robust optimality (contact-set,
sharp-minimum and query-model theorems), a witness-size lower bound, the necessity of the
decomposition rule (exponential separation), and sharp free-energy sandwiches.  Several classical
or recently published results are formalized along the way and are labelled as such.
