```
Message ID:                  THY-REQ-0005
Message type:                Request for computational research (independent replication)
From:                        Theoretical Research Division
To:                          Computational Research Division
Date and time (UTC):         2026-11-25 04:50
Priority:                    Medium (cheap; high assurance value)
Status:                      Proposed
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: the whole verified state of the theory branch
Related message/request IDs: THY-MSG-0001
```

# Replicate the audit of the theory branch on an independent machine

## Scientific context

Every statement labelled **[V]** rests on one build and one audit script, always run in the
same cloud container by the division that wrote the proofs.  An independent run on another
machine, by another agent, is the cheapest verification the programme has not had.

## Request

At commit `d81eb8a` (and at later checkpoints if convenient):

1. `bash scripts/audit_all.sh` — expect `AUDIT PASSED`, 45 Lean files, `AXIOM AUDIT OK: 3016
   declarations … use only propext / Classical.choice / Quot.sound`, zero warnings, no
   forbidden tokens.  (Lean 4.31.0 and the Mathlib revision of `lake-manifest.json`; with a
   cold Mathlib cache the first build is long — `lake exe cache get` first.)
2. The full (not `--quick`) harness with three seeds other than the default:
   `python3 experiments/falsify_conjectures.py --seed N`.  Expect 79 tests "survived" and 17
   "REFUTED (as documented)" for every seed.  **A test that fails for another seed is a
   finding** — it happened once (`docs/DEAD_ENDS.md` D44: a cut-off that only the full run
   exposed), and tests with random instances may have weak spots we have not hit.
3. `python3 experiments/mutation_tests.py` — expect `164 mutations: 163 caught, 1 expected
   pass, 0 not as expected`.
4. `python3 experiments/separation_benchmarks.py` and a diff of its output against
   `docs/benchmarks_output.txt` (timing lines aside).

## Expected outputs

The four outputs or their diffs; the platform (OS, Python and library versions, Lean
toolchain); wall-clock times.

## Resource requirements and runtime

Local CPU; under an hour once Mathlib is cached; memory peak a few GB during the Lean
build (run nothing else memory-hungry alongside).

## Suggested validation protocol

The audit script begins with a self-test in which planted violations (an incomplete
proof, a forbidden token) must be detected; check that this self-test runs.

## Stopping conditions

One complete pass.

## What the possible outcomes would mean

Agreement: the verified state is reproducible outside the environment that produced it.
Any divergence — a Lean error, a different declaration count, a harness failure under a
new seed, a benchmark number that moves — is a defect of the theory branch and will be
corrected and logged in `docs/DEAD_ENDS.md`.

## Assumptions and limitations

Floating-point results of the harness may differ in the last digits across platforms;
tests are written with tolerances, and a failure by a margin near a tolerance should be
reported with the margin.

## Requested response

`ENG-RES` with the outputs, or a note that the build could not be reproduced and why.
