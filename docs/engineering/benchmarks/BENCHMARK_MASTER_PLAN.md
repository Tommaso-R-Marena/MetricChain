# Benchmark master plan (Computational Research Division)

Authority: directive D-5 of the research owner (2026-11-26; `docs/engineering/DIRECTIVES.md`).
This division coordinates the substantial shared computations of all six MetricChain
divisions and benchmarks the programme's results "as they become sufficiently mature".
Budget, launch test and staging rule: `docs/engineering/COMPUTE_LEDGER.md` ("Policy").

The sibling files:

| file | what it holds |
|---|---|
| `BENCHMARK_REGISTRY.md` | the shared queue: every request for computation, from any division, with its readiness, cost bound and status |
| `BENCHMARK_READINESS.md` | the readiness test and, per campaign, what is and is not yet specified |
| `BENCHMARK_RESULTS.md` | what was measured: one entry per finished stage, pointing to the artifact and the message that reports it |
| `BASELINE_SPECIFICATIONS.md` | what each campaign is compared with, and why that is a fair comparison |
| `REPRODUCIBILITY.md` | environment, commands, seeds, provenance fields, where raw outputs live |
| `BENCHMARK_LIMITATIONS.md` | what the benchmarks do not show |
| `../COMPUTE_LEDGER.md` | every remote job, entered before launch and closed after it |
| `../EXPERIMENT_REGISTER.md` | the experiments (X-001 …) the campaigns consist of; not duplicated here |

## 1. Rules of the game

1. **A benchmark tests a stated claim.**  Every campaign names the statement (theorem,
   conjecture or algorithm), the commit that states it, its assumptions, and the
   hypotheses to be tested — written into the registry *before* the computation, so that a
   result cannot choose its own question.
2. **Stages, in order** (D-5 §5): **A** independent reproduction from the mathematical
   definitions → **B** exact ground truth (enumeration, exact or interval arithmetic,
   closed forms, an independent reference algorithm, a checked certificate) with edge
   cases and negative controls → **C** adversarial and assumption-stress instances,
   separating failures *inside* a theorem's hypotheses from behaviour *outside* them →
   **D** comparison with fair baselines at equal accuracy, equal information access and
   honestly counted cost → **E** scaling campaigns on Modal → **F** independent
   replication (other seeds, another implementation, exact methods where they exist).
   A stage is entered only when the one before it has a recorded result.
3. **Readiness gate** (`BENCHMARK_READINESS.md`): no stage E for a statement whose
   specification is still moving; such statements get small exact examples and
   falsification attempts instead (stages A–C), which is also what helps a proof.
4. **Money** follows the ledger: every job bounded and entered before launch; first
   stages at most $60 worst case; larger stages only after a smaller one predicted its
   own cost within a factor two; billed cost must stay $0.00.
5. **Reporting**: every number in a message is generated from a stored artifact
   (`make_tables.py --verify`); failed and negative results are reported with the same
   prominence; tuning and test instances are kept apart where tuning is involved; a
   benchmark "cannot independently prove a general mathematical theorem" and no report
   says it does.

## 2. Campaigns on existing MetricChain results (planning allocation $600)

| id | subject (D-5 §6 item) | claim under test | stage reached | next |
|---|---|---|---|---|
| **BM-1** | nested adaptive algorithms on the cube class `L_u(Q_n)`: finite-size cost against the asymptotic exponents; designs tuned by certified cost against designs tuned at the flat instance | theory report §11.19: Theorem 11.56 (cost bound and validity of Algorithm 2L⁺), remarks (1), (1b) (a certified third level), Theorem 11.58a (`ln N = nh + O(√(n ln n))`) | A, B, C done for two levels (X-005, X-006b, X-009) and for three levels of one flat-tuned design (X-010); **X-011 in progress**: the certified recursion to five levels and the worst cases of the designs it selects | stage E: sizes `10³ … 1.28·10⁵`, slopes `½, 1, 2` |
| **BM-2** | certificate kernel for energy minimisation ("shares at the leaves" of a branching tree; the Lean `verify`) | `verify_sound` (machine-checked) and the science division's P7 format: an accepted certificate proves the bound; what producing and checking costs against an exact solver | A in progress (independent compiled checker, X-012) | B (brute force, mutation and soundness fuzz), then C/D: a producer, heterogeneous alphabets, frustrated and dense instances, exact branch-and-bound as the non-certified baseline |
| **BM-3** | certificate for partition functions (the science division's sandwich certificate, SCI-MSG-0025 §8) | an accepted certificate brackets `ln Z`; tightness and cost against uncertified estimators | not started (specification read only as far as ENG-MSG-0006 §3 says) | A: checker from the specification; B: transfer-matrix ground truth on synthetic chains |
| **BM-4** | articulated chains: covering numbers of pair-distance profile classes, limit shape | theory report §11.22 (limit shape), THY-REQ-0002, -0008; the science division's enumeration requests | A, B done on the lattice to 24 torsions (X-002) and off-lattice to 12 (X-004) | the off-lattice chain in exact arithmetic (R7-ENG-3) first; then one enumeration job (bridges, histograms) |
| **BM-5** | adaptive against non-adaptive query complexity at finite size | Theorem 11.45(b) against Theorem 11.56: the size from which the certified adaptive cost is below the non-adaptive lower bound | A done (X-009: 72 numbers reproduced; crossover not monotone) | folded into BM-1 (the certified recursion moves the crossover) |
| **BM-6** | beyond product measures and one slope | workstream Y (a two-state chain as known part) and its review R10; site-dependent slopes | A in progress (X-013: exact vertex enumeration of weighted cubes, R10-E1) | exact small-block exponents; then statements for site-dependent slopes, if the theory division makes one |

## 3. Campaigns for the three new divisions (planning allocations $350, $350, $250)

Nothing is specified yet: the branches `research/ensemble-identifiability`,
`research/geometric-inference`, `research/biological-complexity` did not exist at the last
fetch (2026-11-26 17:00 UTC).  What a request must contain is in the protocol
(`docs/collaboration/README.md`, "Shared computation") and in `BENCHMARK_READINESS.md`.
Until requests arrive the allocations are untouched; they are planning guidance and move
to wherever the mathematics is ready.

## 4. Replication and final verification (planning allocation $200)

Reserved for stage F of whatever campaigns produce headline numbers, and for one
complete audit replication of the theory head at consolidation (`scripts/audit_all.sh
--full` in a pinned read-only worktree; local, no Modal cost so far).

## 5. Order of work (revised at every checkpoint)

1. BM-1 / X-011 (the research owner's "in particular": the deterioration on non-flat
   fibres; "whether algorithms tuned against worst-case instances improve upon designs
   tuned primarily against flat reference instances").
2. BM-2 / X-012 and BM-6 / X-013 (running in parallel, by independent subagents).
3. BM-4: the exact-arithmetic chain, then the enumeration job.
4. BM-3.
5. Requests of the new divisions as they become ready.
