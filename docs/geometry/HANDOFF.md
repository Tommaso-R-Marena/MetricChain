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
| cycle 2, first note: sequence-local distance data | `docs/geometry/LOCAL_DATA_STABILITY.md` |
| third note: states that share rigid segments (hinges, reflections, interval moments) | `docs/geometry/HINGE_ENSEMBLES.md` |
| every statement with label, evidence, review, novelty | `docs/geometry/THEOREM_REGISTER.md` |
| what is known / not found, with the search log | `docs/geometry/PRIOR_ART.md` |
| withdrawn or weakened claims | `docs/geometry/DEAD_ENDS.md` |
| the internal review, verbatim, with our response | `docs/collaboration/messages/geometry/GEOMETRY-REV-0001.md`; the referee's code: `experiments/geometry/review1/` |
| open proof obligations (O-1 … O-14) | `docs/geometry/PROOF_OBLIGATIONS.md` |
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
python3 experiments/geometry/run_checks.py              # 43 tests, about 70 s (one is skipped, and says so, without Singular)
python3 experiments/geometry/mutation_checks.py         # 31 planted errors, all must be caught
python3 experiments/geometry/exact_conic_rank.py 12     # Theorem C(b), about 35 s
python3 experiments/geometry/exact_conic_rank.py 20 13 rational angles   # Theorem C(b), K = 13..20, about 3 min
python3 experiments/geometry/exact_jacobian_rank.py 8   # Theorem H, about 3 s
python3 experiments/geometry/exact_4d_extreme.py        # Theorem D(b)
python3 experiments/geometry/exact_hierarchy_witness.py # Theorem E(d), exact witness
python3 experiments/geometry/exact_general_position.py 5  # hypothesis of Theorem F', exact
python3 experiments/geometry/exact_nonlinear_threshold.py 10 0 0   # Theorem I; needs Singular (apt-get install -y singular); 80 s over Q
python3 experiments/geometry/exact_demix4.py            # Theorem I' for K = 2, 3 (both bond angles), about 6 min
python3 experiments/geometry/exact_demix4.py --verify 3 17   # the same rank on the pivot rows in integer arithmetic at a second prime (4 min)
python3 experiments/geometry/exact_demix4.py 4 30       # Theorem I' for four states, 27 min, 1.5 GB
python3 experiments/geometry/exact_demix4.py --mutate   # two planted errors; exit status 1 = both caught
python3 experiments/geometry/demix4.py                  # DEMIX-4 in floating point: certificate and recovery below the conic threshold
python3 experiments/geometry/minrank_prediction.py 10 10   # Hilbert function, regularity, heuristic thresholds of the higher levels
python3 experiments/geometry/explore_below.py 7 8 9     # two states below the threshold (numerical)
python3 experiments/geometry/demix.py                   # DEMIX on synthetic ensembles
python3 experiments/geometry/hierarchy_example.py       # Theorem E(d), numerical instance
python3 experiments/geometry/er_not_ur_instance.py A    # second-moment rigid, not universally rigid (numerical; 3 min)
python3 experiments/geometry/matroid_connectivity.py 12 # Theorem J and the table of measurement patterns (exact)
python3 experiments/geometry/hinge_pairs.py 0 150       # Theorem M: the cube of eight candidates, LP, search (2 to 3 min)
python3 experiments/geometry/hinge_multistate.py 0 150  # three states at two to four hinges (exploration, 2 min)
python3 experiments/geometry/exact_hinge_candidates.py  # hinge candidates over Q: degree 8 / 2 (needs Singular)
python3 experiments/geometry/hinge_halfturns.py         # the half-turn exceptions of Theorem M
python3 experiments/geometry/hinge_fourier_rank.py      # what the squared distances see of three hinge angles (rank 19)
python3 experiments/geometry/local_data_upper.py        # Theorem L and the tube bound on instances
python3 experiments/geometry/torsion_sharpness.py       # kink formula, worst conformations (GEOMETRY-RES-0002; slow part (2))
# read-only synchronisation with the other divisions
for b in claude/determined-ride-og1u7j research/ubuntu-engineering research/scientific-translation \
         research/ensemble-identifiability research/biological-complexity research/structural-biology; do git fetch origin "$b"; done
# (research/structural-biology: the seventh division, authorised 2026-11-26; not on the remote at 22:02 UTC)
# the Ensemble division's report: git show origin/research/ensemble-identifiability:docs/ensemble/ENSEMBLE_REPORT.md
```

The theory division's single-command audit `scripts/audit_all.sh` also covers this branch's
Lean file (token scan, axiom walk); its Python stages are the theory division's and were not
changed.  It was **not** run in full on this branch in cycle 1 (its Lean stages were run by
hand: build, zero warnings, axiom audit OK with 5110 declarations at the sixth checkpoint); run it before any
statement of the form "the audit passes at this head".

## Conventions

* Labels V / P / P-exact / K / N / C exactly as in `THEOREM_REGISTER.md`; "refereed" only
  when another division has reviewed.  A review column is filled from a review that exists,
  never in advance (`DEAD_ENDS.md` DG-17); a summary sentence carries the hypotheses of the
  theorem it summarises (DG-13).
* Identifiers: GEOMETRY-MSG-nnnn, GEOMETRY-REQ-nnnn, GEOMETRY-RES-nnnn, GEOMETRY-REV-nnnn;
  message schema of `docs/collaboration/README.md`; corrections are new linked messages.
* Exact computations: rational witnesses, ranks modulo a prime (a lower bound for the rank
  over the number field), never floating point for a statement labelled P-exact.
* Zero Lean warnings; no `sorry`, no extra axioms; every Lean file imported by
  `proofs/AxiomAudit.lean` and its headline theorems listed there.
* **Fetch all five branches immediately before committing a result, and always before
  answering another division's question** (`DEAD_ENDS.md` DG-20); open a paper returned by a
  search before classifying it as not containing the result.
* Times: a header time is `date -u` at the moment of writing or "the commit that adds this
  file" — never an estimate (`DEAD_ENDS.md` DG-12); a statement about another branch names
  the fetch it rests on.
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
`⌈(9K² + K + 8)/4⌉` atoms for the linear certificate (exact for `K ≤ 20`; for every `K` a
proof from `(9K² − 5K + 6)/2` atoms on, by concavity of the generic rank); `⌊9K/2⌋ + 1` for identifiability
itself (a theorem for two states, where 7 and 8 atoms provably-numerically fail; a
conjecture beyond — **proved from 16 atoms for three states and from 30 for four**, by a
second, quartic linear certificate whose mechanism is the published one for linear
sections of varieties: `ENSEMBLE_RIGIDITY.md` §6.2, Theorem I′); `2K + 3` for local
identifiability within `K` states; sequence separation `K + 3`.  For one state this is classical rigidity theory read for ensembles, and
it yields a notion — second-moment rigidity — implied by universal rigidity together with
the conic condition and implying global rigidity together with it (not by universal
rigidity alone: `DEAD_ENDS.md` DG-13).  The conic condition is sufficient, not necessary, and
Theorem B is known in dimension one (Laurent–Poljak 1996; `PRIOR_ART.md` §3a).  For states
that share rigid segments (hinges) the conic condition fails and identifiability is decided
by a finite list of mirrored assemblies (`HINGE_ENSEMBLES.md`; first by the Science
division).  Second topic: distances between points close along the chain determine a thick
chain with a stability constant of order `n²` — a global upper bound (Theorem L) and a
matching lower bound on rods (`LOCAL_DATA_STABILITY.md`).  Mechanism and exponent are those
of the thin-rod rigidity estimate (SCI-REV-0023), and with its present threshold and
constants Theorem L is a statement about the exponent; a threshold-free version is sketched
in `RESEARCH_LOG.md` ("Resume here", item 2) and not yet written or checked.
