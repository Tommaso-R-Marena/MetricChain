# Benchmark master plan (Computational Research Division)

Authority: directives D-5 and D-6 of the research owner (2026-11-26; `docs/engineering/DIRECTIVES.md`).
This division coordinates the substantial shared computations of all seven MetricChain
divisions, benchmarks the programme's results "as they become sufficiently mature", and
(D-6) independently verifies and benchmarks the research software of the Structural &
Computational Biology division.
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
fetch (2026-11-26 15:40 UTC).  What a request must contain is in the protocol
(`docs/collaboration/README.md`, "Shared computation") and in `BENCHMARK_READINESS.md`.
Until requests arrive the allocations are untouched; they are planning guidance and move
to wherever the mathematics is ready.

## 3a. BM-7 — independent verification of the structural-biology division's software (D-6)

*Written 2026-11-26 22:10 UTC.  The branch `research/structural-biology` did not exist at the
fetch of 22:03 UTC; nothing has been received.  This section is the procedure and the
assessment the directive asks for ("Assess which existing mathematical verification
components can support this new responsibility").  No planning allocation is assigned: D-6
raises no limit, and the allocations of D-5 are planning guidance that moves to wherever
the work is ready.*

**Roles** (the owner's): they develop implementations and initial benchmark
specifications; we establish "whether its software actually works, whether its claims are
justified, and whether its proposed improvements withstand independent scrutiny"; science
judges physical relevance and interpretation; the mathematical divisions the foundations.
We do not modify their branch; corrections and alternative implementations live here.

**Procedure, per release of theirs** (each step leaves an artifact on this branch):

| step | what is done | what would stop it |
|---|---|---|
| S0 intake | pin their commit; read the source, the dependency list and the expected resources **before running anything**; a detached read-only worktree of that commit; a separate virtual environment if their dependencies differ from ours; time and memory limits on every run; data files read with `python -I` | code that downloads or executes unreviewed artifacts, needs credentials, or leaves the authorised scope (sequence design, target-specific optimisation, experiments): not run; reported |
| S1 claims | the list of claims, one line each: the statement, where the code implements it, the mathematical source (division, commit, label), and **what observation would falsify it** | a claim that cannot be stated in falsifiable form is returned for clarification |
| S2 reproduction | their tests and their published numbers, re-run here from the pinned commit | — (necessary, never sufficient: "Do not treat the structural biology division's own test suite as sufficient evidence") |
| S3 independent tests | tests written here from the *specification*, not from their code: exact references (enumeration, rational arithmetic, interval arithmetic, transfer matrices), differential tests against our own implementations or established libraries, property-based tests, mutation of the code and of certificates, malformed and adversarial inputs, ill-conditioned and extreme-scale inputs, rounding direction wherever a certificate is claimed | — |
| S4 benchmark review | before any substantial run, the nine questions of D-6 §4 answered in writing (baselines, fairness, success criteria, inputs beyond favourable synthetic ones, comparable accuracy, all material costs, comparable guarantees, independently justified references, room for an unfavourable outcome); hypotheses and analysis fixed in a protocol file before launch; held-out public cases they have not tuned on for final comparisons | an inadequate specification is revised by us or returned |
| S5 computation | smoke test, then bounded Modal jobs entered in the ledger with their worst case; development experiments and final comparative runs kept apart | the launch test of the ledger; the ask-first line at $1,500 of cumulative usage |
| S6 report | an `ENG-RES` with the ten items of D-6 §7: what was reviewed, exact commits, what was reproduced, tests run, claims that survived, claims that failed, assumptions violated, actual costs, remaining concerns, proposed corrections — failures included | — |

**What we already have that carries over** (each is code with tests on this branch):

| component | where | what it gives the new task |
|---|---|---|
| Exact checkers for certificates of pairwise energy models (a C kernel and an independent Python one; strict loader; 182 tests; brute-force ground truth; mutation and malformed-input controls) | `src/metricchain_eng/leafcert/`, X-012 | the pattern for *certificate semantics*: what exactly an accepted file proves, and that nothing malformed is accepted — the test that found an unsound acceptance in another division's reference checker |
| A producer of such certificates with exact solvers as baselines (dynamic programming, branch and bound, enumeration, a commercial-grade open solver) on chains, trees, bands, grids, dense frustrated graphs | `src/metricchain_eng/leafprod/`, `experiments/eng/leafcert_bench/` (in review) | *fair baselines* and *complete cost accounting* (produce + check against solve) for any side-chain-packing or minimisation claim |
| Exact enumeration of chain conformations and of pair-distance profile classes, on a lattice (to 24 torsions) and off-lattice (to 14) | `src/metricchain_eng/chains/`, X-002, X-004, X-007 | exact ground truth for geometric routines on small chains; known answers to compare coordinate builders and distance computations with |
| Mean-run and literal simulators of the adaptive algorithms with a compiled kernel checked against a Python reference and against literal runs; adversarial instance search | `src/metricchain_eng/twolevel/`, X-005 … X-011 | the *method*: two implementations written apart, literal runs against models, searches that try to break a claim, and the lesson of the science division's review R18 — a search that stops low looks like a property of the problem |
| Exact polyhedral computations (vertex enumeration in rational arithmetic, four methods, cross-checked with an independent library) | `src/metricchain_eng/weighted_cube/`, X-013 | exact references for linear-programming and transport bounds |
| Provenance: every published number generated from stored artifacts and re-verifiable (`make_tables*.py --verify`); result rows carry the commit; a launcher that refuses a tree that differs from its commit; protocols with hypotheses before each job | `experiments/eng/*/make_tables*.py`, `modal_jobs/bench_app.py`, `benchmarks/protocols/` | reproducibility and the separation of development runs from final runs |
| A replication of the theory division's full audit (Lean build, harnesses, mutation tests) in a pinned worktree | X-001 | the routine for checking that software *corresponds to* machine-checked statements, where the new software claims that |

**What we do not have and will need**: (i) independent readers and writers for the public
structure formats the software will consume, and reference geometry (bond lengths,
angles, torsions, superposition) computed two ways; (ii) interval or directed-rounding
arithmetic for continuous energies — nobody in the programme has proved the step from a
real-valued energy to the rounded integer tables the certificate kernels check (the
science division's assumption A9, restated in SCI-RES-0030 §3), and any "certified"
claim of application software passes through exactly that step; (iii) a held-out set of
public test cases, fixed and hashed *before* we see their results; (iv) established
uncertified baselines installed here in pinned versions.  (i), (iii) and (iv) are
prepared when their first specification says which formats and methods are in play;
(ii) is worth starting now, because it is needed whatever they build.

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
