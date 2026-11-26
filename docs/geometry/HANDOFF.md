# Handoff — Geometric Inference, Rigidity and Inverse Problems Division

For a successor who starts with nothing but this repository.

## What this division is

One of six MetricChain divisions (research owner's mandate of 2026-11-26).  It writes only to
`research/geometric-inference`; it reads the other branches and never merges, force-pushes or
opens pull requests.  Mandate: reconstructability, identifiability, rigidity, stability and
complexity of articulated geometric systems under incomplete, noisy or indirect observations.
Scope: mathematics and synthetic systems only.  Hard stop for computation: 2026-11-30 15:00
Eastern Time; on the owner's consolidation directive switch to proof completion,
verification, documentation and preservation.

## Where things are

| what | where |
|---|---|
| cycle-1 results with proofs | `docs/geometry/ENSEMBLE_RIGIDITY.md` |
| every statement with label, evidence, review, novelty | `docs/geometry/THEOREM_REGISTER.md` |
| what is known / not found, with the search log | `docs/geometry/PRIOR_ART.md` |
| withdrawn or weakened claims | `docs/geometry/DEAD_ENDS.md` |
| open proof obligations (O-1 … O-11) | `docs/geometry/PROOF_OBLIGATIONS.md` |
| chronology and "Resume here" | `docs/geometry/RESEARCH_LOG.md` |
| Lean | `proofs/Geometry/EnsembleRigidity.lean` (imported by `proofs/AxiomAudit.lean`) |
| experiments, exact computations, harness | `experiments/geometry/` |
| mailbox | `docs/collaboration/messages/geometry/`, `requests/geometry/`, `responses/geometry/`, `status/geometry.md`, `GEOMETRY_TO_ALL.md` |

## Commands

```bash
# Lean (toolchain in ~/.lean/lean-4.31.0-linux; `lake exe cache get` once)
source scripts/lean_env.sh
lake env lean proofs/Geometry/EnsembleRigidity.lean     # single file, about 15 s, no output = OK
lake build                                              # whole project; the last lines print the axiom audit
# Python (numpy, scipy; exact parts use only the standard library)
python3 experiments/geometry/run_checks.py              # 27 tests, about 20 s (one is skipped, and says so, without Singular)
python3 experiments/geometry/mutation_checks.py         # 15 planted errors, all must be caught
python3 experiments/geometry/exact_conic_rank.py 12     # Theorem C(b), about 35 s
python3 experiments/geometry/exact_jacobian_rank.py 8   # Theorem H, about 3 s
python3 experiments/geometry/exact_4d_extreme.py        # Theorem D(b)
python3 experiments/geometry/exact_nonlinear_threshold.py 10 0 0   # Theorem I; needs Singular (apt-get install -y singular); 80 s over Q
python3 experiments/geometry/explore_below.py 7 8 9     # two states below the threshold (numerical)
python3 experiments/geometry/demix.py                   # DEMIX on synthetic ensembles
python3 experiments/geometry/hierarchy_example.py       # Theorem E(d), numerical instance
python3 experiments/geometry/er_not_ur_instance.py A    # second-moment rigid, not universally rigid (numerical; 3 min)
python3 experiments/geometry/matroid_connectivity.py 12 # Theorem J and the table of measurement patterns (exact)
python3 experiments/geometry/torsion_sharpness.py       # kink formula, worst conformations (GEOMETRY-RES-0002; slow part (2))
# read-only synchronisation with the other divisions
for b in claude/determined-ride-og1u7j research/ubuntu-engineering research/scientific-translation \
         research/ensemble-identifiability research/biological-complexity; do git fetch origin "$b"; done
# the Ensemble division's report: git show origin/research/ensemble-identifiability:docs/ensemble/ENSEMBLE_REPORT.md
```

The theory division's single-command audit `scripts/audit_all.sh` also covers this branch's
Lean file (token scan, axiom walk); its Python stages are the theory division's and were not
changed.  It was **not** run in full on this branch in cycle 1 (its Lean stages were run by
hand: build, zero warnings, axiom audit OK with 5071 declarations); run it before any
statement of the form "the audit passes at this head".

## Conventions

* Labels V / P / P-exact / K / N / C exactly as in `THEOREM_REGISTER.md`; "refereed" only
  when another division has reviewed.
* Identifiers: GEOMETRY-MSG-nnnn, GEOMETRY-REQ-nnnn, GEOMETRY-RES-nnnn, GEOMETRY-REV-nnnn;
  message schema of `docs/collaboration/README.md`; corrections are new linked messages.
* Exact computations: rational witnesses, ranks modulo a prime (a lower bound for the rank
  over the number field), never floating point for a statement labelled P-exact.
* Zero Lean warnings; no `sorry`, no extra axioms; every Lean file imported by
  `proofs/AxiomAudit.lean` and its headline theorems listed there.
* Requests for substantial computation go to the Computational Research Division with a
  specification, expected result, validation criterion, resources and stopping condition; this
  division does not spend the shared Modal budget itself.

## The one-paragraph mathematical state

Averaged squared distances of an ensemble are the squared distances of one "stacked"
configuration in `ℝ^{3K}`.  Competing ensembles are linear images of it, so identifiability
is a question about positive semidefinite quadrics of rank at most 3 through the constrained
edge directions of the stacked configuration.  If only the trivial quadrics exist (rank of
one linear system), the mixture is the only ensemble with its data, the states are recovered
by linear algebra, and a positive semidefinite certificate bounds the 2-Wasserstein distance
of any ensemble by the square root of its data mismatch.  The thresholds are exact:
`⌈(9K² + K + 8)/4⌉` atoms for the linear certificate; `⌊9K/2⌋ + 1` for identifiability
itself (a theorem for two states, where 7 and 8 atoms provably-numerically fail; a
conjecture beyond); `2K + 3` for local identifiability within `K` states; sequence
separation `K + 3`.  For one state this is classical rigidity theory read for ensembles, and
it yields a notion — second-moment rigidity — strictly between global and (possibly) universal
rigidity.
