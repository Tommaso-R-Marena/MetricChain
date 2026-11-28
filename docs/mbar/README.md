# Division 9 — Certified Statistical Thermodynamics and Optimal Molecular Simulation

*Branch `research/phase2-certified-mbar`.  Everything here was produced by AI sessions and reviewed by
an AI session; **no human has read any of it**, and nothing has been compared with an experiment.
The work is bounded and has stopped; it does not resume without authorisation.*

## Read in this order

| | file | what it is |
|---|---|---|
| 1 | [`FINAL_REPORT.md`](FINAL_REPORT.md) | the ten deliverables of the directive, in order; resources; recommendations |
| 2 | [`MATHEMATICS.md`](MATHEMATICS.md) | every statement with its proof and status: A (allocation), B (certificates), C (information limits); audit of the handoff |
| 3 | [`REVIEW_A.md`](REVIEW_A.md) | the internal adversarial review and what was changed because of it |
| 4 | [`VALIDATION.md`](VALIDATION.md), [`VALIDATION_TABLES.md`](VALIDATION_TABLES.md) | what was run and what it shows; tables generated from stored results |
| 5 | [`SYNTHESIS.md`](SYNTHESIS.md) | mathematical links with the three other Phase II divisions; §S8: what they sent, what was checked, what it changes |
| 6 | [`DEAD_ENDS.md`](DEAD_ENDS.md) | negative results, limitations, our own errors |
| 7 | [`PRIOR_ART.md`](PRIOR_ART.md) | bounded prior-art search and novelty matrix |
| 8 | [`LEAN_CORRESPONDENCE.md`](LEAN_CORRESPONDENCE.md) | pins, audit, statement-by-statement correspondence |
| 9 | [`PROVENANCE.md`](PROVENANCE.md), [`RESEARCH_LOG.md`](RESEARCH_LOG.md) | base commit, imported package, chronology |
| 10 | [`PROTOCOL_LOCAL_CONTROLS.md`](PROTOCOL_LOCAL_CONTROLS.md) | frozen protocol of the recommended next experiment (correlated samplers with exact answers); **not run** |

Mailbox: `docs/collaboration/messages/mbar/` (MBAR-MSG-0001, its corrections MBAR-MSG-0002, the reply
to the other divisions MBAR-MSG-0003), `requests/mbar/` (MBAR-REQ-0001: answered, superseded),
`status/mbar.md`, `MBAR_TO_ALL.md`.

## Layout of the code

```
experiments/mbar/
  handoff/                  the uploaded package, byte for byte (never edited); nested original handoff zipped
  src/d9mbar/               population.py   exact population quantities, optimal design, certificates of optimality
                            estimators.py   MBAR solver, fitted distributions, plug-in variance, pilot_allocation
                            certificates.py likelihood-ratio region, restricted intervals, observables, model check, baselines
  tests/                    test_population.py, test_certificates.py
  bench/                    bench_certificates.py, bench_allocation.py, bench_robustness.py,
                            bench_public_umbrella.py, check_lower_bounds_and_chains.py, check_synthesis.py,
                            check_inbound.py (statements exchanged with the other divisions), make_tables.py
  results/                  stored outputs (json, logs), including one run kept as INVALID and the first allocation run
  data/pymbar_umbrella/     public data used in VALIDATION.md section 6 (MIT licence; provenance in its README)
  lean/                     standalone Lake project: MBAR/{Allocation,EValue,LowerBound,Localization,AxiomAudit}.lean, audit.sh, logs/
  review/                   the referee's scripts and raw report
  build_zip.sh              builds the consolidated archive of this division (ZIP_MANIFEST.sha256: hashes of its files;
                            zip_root/README.md: the README placed at the root of the archive)
```

## Reproduce

Python 3.13, NumPy 2.5.3, SciPy 1.18.1, CVXPY 1.9.3 (tests of the conic identities only), PyMBAR 4.0.3
(baseline and cross-check only).  Seeds are fixed in every script.

```bash
export OPENBLAS_NUM_THREADS=1
B=experiments/mbar/bench; R=experiments/mbar/results
python experiments/mbar/tests/test_population.py            # ~2 min   allocation theory, exact
python experiments/mbar/tests/test_certificates.py          # ~2 min   estimators and certificates, incl. equivariance under energy offsets
python $B/check_lower_bounds_and_chains.py                  # ~2 min   T9
python $B/check_synthesis.py                                # ~1 min   T10
python $B/check_inbound.py                                  # seconds  T11
python $B/bench_certificates.py --trials 200 --boot-trials 40 --out $R/certificates_coverage_v3.json > $R/certificates_coverage_v3.log   # T1, ~25 min on 3 cores
python $B/bench_allocation.py --reps 2000 --first-run-stream --out $R/allocation_benchmark_2000.json > $R/allocation_benchmark_2000.log   # T2, ~80 min on 3 cores
python $B/bench_allocation.py --reps 2000 --only costly_ends,costly_middle --out $R/allocation_benchmark_costpilot2.json > $R/allocation_benchmark_costpilot2.log   # T3
python $B/bench_allocation.py --reps 400 --first-run-stream --out $R/allocation_benchmark_regression400_firststream.json                  # T4 / T4b
python $B/bench_robustness.py --trials 300 --parts AB --out $R/robustness_final_AB.json > $R/robustness_final_AB.log                      # T5, T6
python $B/bench_robustness.py --trials 300 --parts C  --out $R/robustness_final_C.json  > $R/robustness_final_C.log                       # T7, ~30 min on 2 cores
python $B/bench_public_umbrella.py > $R/public_umbrella.log                                                                               # T8, ~1 min
python $B/make_tables.py --check                            # the tables match the stored results
(cd experiments/mbar/lean && lake exe cache get && ./audit.sh)   # Lean 4.31.0 / Mathlib fabf563
```

Seeds are fixed per repetition, so the numbers do not depend on `--procs`.  `--first-run-stream` skips
the two post hoc variants of the allocation benchmark, so that the remaining seven methods see exactly
the random numbers of the stored runs T2 and T4, which were made before those variants existed
(`VALIDATION_TABLES.md` T4b); without it the one-step Neyman rule and the resistance criterion are
drawn later in the stream and their numbers differ within noise.  The timing columns depend on the
load of the machine.

## One-paragraph summary

The strengthened handoff's mathematics was re-derived and no error was found; its two observable
certificates are valid but far from sharp.  Three things were added.  (1) A complete optimal-design
theory for how to divide samples among thermodynamic states — dual formula, unsampled states, an
Elfving-type identity with costs, an equivalence theorem, a computable efficiency certificate — with
a pilot-based rule that realises the predicted gains in actual error on synthetic systems (largest
where costs or overlaps are unbalanced, nil on a well-designed ladder).  (2) A finite-sample
confidence region for free energies that is valid at every sample size, simultaneously for all
contrasts, at every round of an adaptive simulation, with no condition on the energies: a sublevel
set of the MBAR objective, justified by a new e-value identity for stratified samples; it is 2–3
times wider than the usual asymptotic interval for up to ten states, 1.4–8 times narrower than the
handoff's certificates, and it comes with a model check that detects a sampler that disagrees with
its neighbours.  (3) Finite-sample lower bounds at every instance, and a proof that adaptive
allocation cannot beat the optimal fixed allocation by more than a constant factor.  An internal
adversarial review found no false theorem but one serious defect in the first version of the solver
(wrong free energies, without warning, when the states' energies differ by tens of kT) and several
overstatements; all are corrected and documented (`REVIEW_A.md`).  The three other divisions replicated
two of the statements with their own code, found the correlated-sampling counterexample independently,
and set three limits that are accepted (`SYNTHESIS.md` §S8).  The limits are stated as plainly: everything
assumes independent equilibrium samples; consistent trapping is undetectable from samples (a
theorem); nothing is certified for Markov-chain data without an assumed mixing rate; and nothing here
has been tested on a real sampler; the optimality statements are central-limit-scale statements; and
the next experiment (correlated samplers with exact answers) is specified but not run.
