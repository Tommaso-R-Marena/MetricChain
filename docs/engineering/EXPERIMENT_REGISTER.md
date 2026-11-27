# Experiment register (Computational Research Division)

One entry per experiment.  "Source commit" is the theory commit whose definitions the
experiment uses; "implementation" is the engineering commit that contains the code (the
commit that adds or last changes the files named).  Costs are in
`docs/engineering/COMPUTE_LEDGER.md`.

---

## X-001  Independent replication of the theory audit

| field | value |
|---|---|
| Scientific purpose | Is the verified state of the theory branch reproducible on another machine, by another agent, under other seeds?  (THY-REQ-0005) |
| Source commit | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` (worktree = this branch; `proofs/`, `experiments/*.py`, `scripts/` unmodified) |
| Mathematical dependencies | none (this *is* the check of the dependencies) |
| Execution environment | local: Ubuntu 26.04 LTS under WSL2, x86-64, 8 threads, 7.6 GiB; Lean 4.31.0 (commit `68218e8`), Mathlib `v4.31.0` (`fabf563`) from the cache; Python 3.12.16, NumPy 2.5.5, SciPy 1.18.1, mpmath 1.3.0.  Remote (harness seeds): Modal, Debian (gVisor), Python 3.12.10, same NumPy/SciPy/mpmath |
| Inputs | the repository at the source commit |
| Configuration | `scripts/audit_all.sh --full`; `experiments/falsify_conjectures.py --seed {101,202,303}` (full mode); `experiments/mutation_tests.py`; `experiments/separation_benchmarks.py` |
| Random seeds | harness: default `20261124` (inside the audit) and `101`, `202`, `303`; benchmarks: the script's own seed 7 |
| Outputs | `experiments/eng/audit_replication/` |
| Validation | the audit script's self-test (planted violations must be detected) ran and passed |
| Later checkpoint | the same audit (`--full`) was repeated on a read-only worktree of the theory head `4cef47e` (46 Lean files, 3101 declarations): `AUDIT PASSED`; log `audit_all_full_4cef47e.log`; reported in ENG-MSG-0002 |
| Result, interpretation, limitations | ENG-RES-0005 |

## X-002  Lattice chains: exact covering numbers in the profile format, 1–24 torsions

| field | value |
|---|---|
| Scientific purpose | Does the chain-length independence of certificate sizes at extensive accuracy (theory report Proposition 11.49(a)) become visible at sizes that can be enumerated?  Entropy of profile sets; realisability of trans/gauche patterns.  (THY-REQ-0002, questions 1, 2, 3(a), lattice part) |
| Source commit | `d81eb8a`; definitions from `docs/workstreams/P_REPORT.md` §§0, 2.2, 3.2, 3.3 and theory report §11.17 |
| Mathematical dependencies | `isCertificate_iff_cover` [V]; `pairRes_sub_le` [V]; Proposition 11.49(a) [P, refereed] — see `docs/engineering/DEPENDENCY_MAP.md` |
| Execution environment | enumeration `n ≤ 20`: local, single core, `cc -O3 -march=native`; `n = 21…24`: Modal, 64 single-core containers per length, `cc -O3` (job M-002).  Covers: Modal, 4 cores per length (jobs M-004 for `n ≤ 18`, M-005 for `n = 19…24`), HiGHS (SciPy 1.18.1) and, for `n ≤ 18`, CP-SAT (OR-Tools 9.15.6755).  Single-flip constants and the envelope test: local, single core (`build/dia_flip`; 456 s for mode A at `n = 16`) |
| Inputs | none external: the diamond-lattice chain model is generated from its definition (tetrahedral angle, torsions 180°/±60°, self-avoidance, pairs with `q − p ≥ 3`, cutoff `S_c = 12`); known part `#gauche`; zero residual |
| Configuration | `L ∈ {1, 1/5}`; `ε ∈ {0, 1, N/20, N/10, N/4, N/2}`; entropy radii `δN`, `δ ∈ {4, 2, 1, 1/2, 1/4}`; net time limit 60 s per radius; for `n ≥ 19` 300 s per cover programme and rigorous brackets where not proved |
| Random seeds | none (exhaustive, deterministic) |
| Outputs | class tables `experiments/eng/chain_cover/data/dia_Sc12_n*.txt` (the complete enumeration result: every profile class with its number of conformations, fewest and most gauche torsions); `results/lattice_Sc12.json`, `results/lattice_Sc12_flip.json`, `results/lattice_Sc12_patterns.json`; `data/flip/` |
| Validation | (i) class tables equal an independent internal-coordinate construction for `n ≤ 7`; (ii) conformation and class counts equal the published sequences for `n = 5…13`; (iii) all 24 published covering numbers reproduced; (iv) mirror reduction and prefix splitting verified to be exact; (v) the Modal-merged table at `n = 14` equals the local one; (vi) two solvers agree on every cover; (vii) negative control: no pair inside the cutoff ⇒ one class, covering number 1.  `python -m pytest tests/eng -q` (69 tests); `python experiments/eng/chain_cover/run_lattice.py --check` |
| Correction (checkpoint 4) | Validation (vi), "two solvers agree on every cover", is **withdrawn** (ENG-MSG-0004 §4, item 2; SCI-REV-0008, M1): the rows `n = 1…18` were written by the driver of job M-004, which was replaced; the committed code stops at the first proof and stores no second one.  What holds: proved optimal by HiGHS; 254 of the 263 optima certified independently of any solver by the Scientific Discovery Division |
| Result, interpretation, limitations | ENG-RES-0002 (updated in place for `n = 20…24`; change note in ENG-RES-0007) |

## X-003  Exact hitting numbers on the uniform cube (closed form via Harper's theorem)

| field | value |
|---|---|
| Scientific purpose | What is the exact fractional hitting number over *all* sensitive sets on the uniform cube, and how far is the single-dip value from it?  (THY-REQ-0006, the part that needs no linear programme) |
| Source commit | `d81eb8a`; definitions from `docs/workstreams/A_REPORT.md` §2.0 |
| Mathematical dependencies | theory report Theorem 11.22 [V core]; Harper's theorem [K] |
| Execution environment | local, seconds |
| Inputs / seeds | none |
| Configuration | `(u, ε) ∈ {(1, 0.3), (1, 1), (2, 0.3), (0.5, 0.3)}`, `n ≤ 14`; brute force over all subsets for `n ≤ 4`, 72 parameter cases |
| Outputs | `experiments/eng/fc_uniform_cube/harper_fc_table.json` |
| Validation | brute force over all `2^{2ⁿ} − 2` proper nonempty subsets for `n = 2, 3, 4`; consistency with the ratio 2 at `n = 3, 6` reported in `A_REPORT.md` §3 |
| Result, interpretation, limitations | ENG-RES-0006 |

## X-004  Generic (off-lattice) chain: covering numbers in the profile format, 5–12 torsions

| field | value |
|---|---|
| Scientific purpose | THY-REQ-0002 question 1 for the model "gen": does the growth of the profile-format covering numbers level off at extensive accuracy? |
| Source commit | `d81eb8a`; definitions from `docs/workstreams/P_REPORT.md` §§0, 2.1 (Proposition 2), 3.3 |
| Mathematical dependencies | as X-002; in addition the identity `‖N^x − N^y‖₁ = ‖sort(s̃^x) − sort(s̃^y)‖_{ℓ¹}` (P_REPORT Proposition 2, [P]), checked numerically in `tests/eng/test_chains.py` |
| Execution environment | enumeration and covers on Modal, 8 cores and 24 GiB per chain length (jobs M-006 for `n ≤ 9`, M-007 for `n = 10…12`); tie analysis local |
| Inputs | none external: bond length 1, bond angle 111°, torsions 180°/±60°, hard core `s ≥ 3` for `q − p ≥ 3`, cutoff 16, known part `#gauche`, zero residual |
| Configuration | `L ∈ {1, 1/5}`; `ε ∈ {0, 1, N/20, N/10, N/4, N/2}`; classes = sorted truncated squared distances rounded to 8 decimals; cover relation with tolerance `10⁻⁹`; HiGHS 300 s per programme (`n ≤ 9`), 90 s (`n = 10…12`) |
| Random seeds | none |
| Outputs | `experiments/eng/chain_cover/results/generic_Sc16.json`, `generic_Sc16_ties.json` |
| Validation | 1–4 distances, conformation and class counts (`n = 5…10`, `n = 12`), and 16 covering numbers of P_REPORT §3.3 reproduced; two published brackets at `n = 10` closed; mirror reduction exact; tie analysis (five exact ties at `n = 11`, none elsewhere; nearest non-tie ≥ `2.9·10⁻⁸`) |
| Result, interpretation, limitations | ENG-RES-0007 |

## X-005  Algorithm 2L⁺ on adversarial instances: number of evaluations and every claim of Theorem 11.56 (mean runs)

| field | value |
|---|---|
| Scientific purpose | Is there a `u`-Lipschitz instance on which the two-level algorithm of theory report §11.19 needs more evaluations than its theorem claims, or violates one of the theorem's claims?  Which instance is the worst one at finite `n`, and where does the algorithm overtake the plain two-sample bracket on it?  (THY-REQ-0001, Parts B and C, as redirected to Algorithm 2L⁺ by THY-MSG-0005 §4 and THY-MSG-0007 §3) |
| Source commit | theory `63efc69` — the *text* of `docs/workstreams/K_REPORT.md` §§2.1–2.3, 3.2, 3.4 with the errata of referee R8 listed at its head; audited on the engineering machine (ENG-MSG-0003 §2) |
| Mathematical dependencies | Theorem 11.56 (= K1) **[P], refereed (R8)**: this is the statement under test, not a dependency.  Used as given: the definitions of the tables `Γ̃, κ, Γ″, r†`; Proposition 11.57(a) (= K0) for the cost of the base family **[P]**; Harper's theorem **[K]** for the reduction of ENG-RES-0008 §5 (an engineering argument, unrefereed) |
| Execution environment | local: as X-001, plus a C kernel compiled with gcc 15.2.  Remote: Modal, Debian (gVisor), Python 3.12, NumPy 2.5.5, SciPy 1.18.1, gcc of the image; one core and 1 GiB per task |
| Inputs | none (synthetic instances) |
| Configuration | design parameters of the theory division's own table: `b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `ν₁ = 2e^u n_o/θ`, `δ = 0.05`, ladder `ε*·0.85^i`; cells `u ∈ {½, 1, 2}` × 13 sizes (250 … 128 000) × 12 outer fractions (0.30 … 0.85); per cell: flat instance, then differential evolution over 19 instance parameters for {monotone, general} profiles × {bottom, top} inner behaviour; budgets in `run_search.tasks` |
| Random seeds | differential evolution: seed 1 (jobs M-008, M-009), seeds 2 and 3 (M-010) |
| Outputs | `experiments/eng/twolevel/results/x005_cost.jsonl`, `x005_claims.jsonl`, `x005_converge.jsonl`, `x005_seeds.json`, `x005_recheck.json` |
| Validation | (i) tables against brute force with exact integers; (ii) C kernel against the Python reference on random instances; (iii) 324 + 18 published rows of workstream K reproduced; (iv) a literal sampled implementation (X-006) agrees with the mean run; (v) mutation without the Harper term is detected; (vi) remote results bit-identical to local ones on the cases compared; (vii) every stored maximiser re-evaluated with the final code.  `tests/eng/test_twolevel.py` |
| Code | `src/metricchain_eng/twolevel/` (`tables.py`, `alg2l.py`, `meanrun.py`, `meanrun_kernel.c`, `ckernel.py`, `adversary.py`); `experiments/eng/twolevel/` (`controls.py`, `run_search.py`, `recheck.py`, `seed_analysis.py`, `make_tables.py`); `modal_jobs/twolevel_app.py` |
| Result, interpretation, limitations | ENG-RES-0008 |

## X-006  Algorithm 2L⁺ with real fluctuations of the outer sample (literal runs)

| field | value |
|---|---|
| Scientific purpose | Does any claim of Theorem 11.56 fail on a run on which the good event (V2)–(V3) holds?  How often do the good event and the validity of the bracket fail as `K` is scaled down from the theorem's value?  (THY-REQ-0001, Part A, outer loop only) |
| Source commit | as X-005 |
| Mathematical dependencies | as X-005 |
| Execution environment | as X-005 (pure Python on the remote side) |
| Configuration | `(u, n_o, n_i) ∈ {(½, 300, 6), (1, 120, 6), (2, 48, 6)}`; `b = 0.5`, `λ = 0.5`, `η = ¼`, `η′ = θ = 0.1`, `ν₁ = 2e^u n_o/θ`, `δ = 0.05`, inner rates `(0.9, 0.45, 0.2)`; 13 radial landscapes; inner behaviour bottom / top / random (one bracket per (block, shell) group); `K` scaled by 1, ¼, 1/16, 1/64, 1/256 |
| Random seeds | `numpy.random.default_rng([seed, …case…])` with `seed = 1`; the case enters the seed, so every case has its own stream |
| Outputs | `experiments/eng/twolevel/results/x006_sampled.jsonl` |
| Validation | `stable_multinomial` against exact tail masses; agreement of literal runs with the mean run at the theorem's `K` (`tests/eng/test_twolevel.py`) |
| Code | `src/metricchain_eng/twolevel/simulate.py`; `experiments/eng/twolevel/run_sampled.py`; `modal_jobs/twolevel_app.py::sampled` |
| Limitation stated up front | inner procedures are oracles: the event (V1) of the proof (validity of real inner brackets) is true by construction and is **not** tested |
| Correction (checkpoint 4) | **Superseded by X-006b**: the shell counts were drawn with numpy's binomial sampler, which is biased from about `10¹⁵` trials on (SCI-REV-0007 §4); two of the three sizes drew from such blocks.  The file stays as produced; `--sampler numpy` reproduces it |
| Result, interpretation, limitations | ENG-RES-0008 §6 |

## X-006b  Algorithm 2L⁺ with real fluctuations — the cases of X-006 with an exact sampler; an invalid inner behaviour

| field | value |
|---|---|
| Scientific purpose | (i) Do the statistics of X-006 survive when the shell counts are drawn exactly?  numpy's binomial sampler is biased for counts drawn from about `10¹⁵` trials and more (reported by the Scientific Discovery Division, SCI-REV-0007 §4, request R6-E3), and X-006 drew from blocks of up to `2.7·10¹⁷` points.  (ii) Does the cost stay below `C_max` in every run when the inner procedure misbehaves (their request R6-E2)?  (iii) Does any run reach the lowered sample cap of THY-RES-0004 §3? |
| Source commit | engineering `26029c9` (stored in every row, with the job id); algorithm text as X-005 (`K_REPORT.md` §§2–3 at theory `63efc69`, errata m1, m10); the cap: THY-RES-0004 §3 at theory `9408e33` |
| Mathematical dependencies | Theorem 11.56 **[P; refereed R8; reviewed SCI-REV-0007]** (statement under test); the remark after it (lowered cap) **[P; unrefereed, reviewed SCI-REV-0007 §2]**; exactness of the sampler: the Poissonisation argument in the docstring of `sampling.py` **[P; ours; unrefereed]** |
| Execution environment | Modal job M-012 (741 tasks, one core each, numpy 2.5.5, 16.9 core-hours, $1.01); the sampler measurement locally (2 minutes) |
| Configuration | the 585 cases of X-006 unchanged (sizes, design, landscapes, valid inner behaviours, values of `K`, runs per case, seeds); in addition 156 cases with the invalid inner behaviour "dear" (every refined point is sent to the last rung by brackets that ignore the fibre) at the theorem's `K`, inner dimensions 6, 20, 40, 80, 500 runs each |
| Random seeds | as X-006 (`numpy.random.default_rng([1, …case…])`; for `n_i ≠ 6` the inner dimension enters the seed).  The streams are consumed differently by the two samplers, so runs are not comparable one by one |
| Outputs | `experiments/eng/twolevel/results/x006b_sampled.jsonl` (741 rows), `x006b_binomial_bias.json` (the sampler grid), `x005_lowered_cap.json` (the cap on the stored instances of X-005) |
| Validation | the exact sampler: chi-square against the exact law in the three regimes of its collision step (8 cases, `n = 12 … 2⁶¹`), mean and variance on a grid of 92 cells, a regression test that documents numpy's defect; `--sampler numpy` reproduces three stored rows of X-006 bit for bit; the invalid behaviour triggers the abort rule in a unit test |
| Code | `src/metricchain_eng/twolevel/sampling.py`, `simulate.py`; `experiments/eng/twolevel/binomial_bias.py`, `run_sampled.py`, `lowered_cap.py`; `modal_jobs/twolevel_app.py::sampled`; blocks `binomial_*`, `exposure`, `sampledb*`, `sampled_compare*`, `lowered_cap_x005` of `make_tables.py` |
| Limitation stated up front | as X-006: oracle inner brackets, so the event (V1) is not tested; one design; three sizes.  One branch of the sampler (means above `10⁹` at more than `2³¹` trials) still uses numpy and is not exact.  The invalid behaviour makes the budget bind in one of twelve configurations only |
| Result, interpretation, limitations | ENG-RES-0013 §§1, 2, 4 |

## X-008  Smallest sensitive balls on a type class of the cube, exactly, up to `n = 10 000`

| field | value |
|---|---|
| Scientific purpose | THY-REQ-0010, question 2: do the exact finite-`n` values of `−ln q*_ball(1)/n` on the type classes `κ = 0.5, 0.4, 0.3` approach the theory division's limits, and at which rate?  Is the best centre outside the class for `κ ≠ ½` at accessible sizes? |
| Source commit | theory `9408e33` (THY-REQ-0010; the limits `0.029139`, `0.028005`, `0.024588` are quoted from it, not recomputed) |
| Mathematical dependencies | the definitions of the request; the distance of a point of a ball to its complement inside the class, `2(i − i₀ + 1)` **[P; ours; checked by brute force on five small classes]** |
| Execution environment | local, single core, five seconds |
| Configuration | `u = 1`, `ε = 1`, `n ∈ {20, …, 10 000}` (10 sizes), all centre types `0 ≤ m ≤ n`, all radii |
| Outputs | `experiments/eng/slices/results/ball_exponents.json` |
| Validation | the request's target (`n = 8`, `k = 4`: 17 points, `Φ = ((e⁴−1) + 16(e²−1))/70`); for `n ≤ 400` (18 cases) the optimum recomputed with exact integer weights and a 60-digit comparison selects the same ball |
| Code | `experiments/eng/slices/ball_exponents.py`, `make_tables.py`; `tests/eng/test_slices.py` |
| Result, interpretation, limitations | ENG-RES-0012 |

## X-009  `C_max` of Theorem 11.56 against the non-adaptive lower bound: from which size on is two-level adaptivity certified to win?

| field | value |
|---|---|
| Scientific purpose | Independent recomputation of the Scientific Discovery Division's table (SCI-REV-0007 §5; request R6-E1), with and without the lowered sample cap, on a finer grid around each crossover |
| Source commit | science `d45ad56` (their numbers; definitions from `R6_REPORT.md` §7); theory `9408e33` (Theorem 11.45(b), THY-RES-0004 §3) |
| Mathematical dependencies | Theorem 11.56 **[P]**, Theorem 11.45(b) **[V given two finite sums]**, the lowered cap **[P; unrefereed]** |
| Execution environment | local, three seconds |
| Configuration | the design of X-005; `u ∈ {½, 1, 2}`; windows of 49, 36 and 37 sizes around the crossovers and 5–8 sizes beyond; outer fractions 0.35 … 0.70 |
| Outputs | `experiments/eng/twolevel/results/x009_separation.json` |
| Validation | the 60 + 12 numbers of their two tables, reproduced to the digit given |
| Code | `experiments/eng/twolevel/separation.py`; blocks `separation_*` of `make_tables.py` |
| Result, interpretation, limitations | ENG-RES-0013 §3 |

## X-005b  Algorithm 2L⁺: instances that are not products; the classification rule rechecked; convergence at the two largest sizes

| field | value |
|---|---|
| Scientific purpose | Three doubts about X-005, two of them raised by the Scientific Discovery Division (SCI-REV-0008 §4 (1), (2)).  (i) Its search family has one place `t₀` for all fibres: can an instance whose fibres sit at different places of their trivial brackets cost more?  (ii) Its mean runs classified sample points by a convention (`W > s e^{−b}` or `W > s`): does the exact rule of the algorithm give the same runs?  (iii) Were the searches at `n = 64 000` and `128 000`, which had the smallest budgets, converged? |
| Source commit | engineering `f0c8375` for the generalised evaluator and the local scripts; jobs M-013 (`909751b`) and M-014 (in the rows); algorithm text as X-005 |
| Mathematical dependencies | the classification threshold `c = max_l min(b − A_l, B_l)` and the union-of-windows bound **[P; ours; unrefereed]** (`meanrun.rung_positions`; ENG-RES-0014 §§1, 4) |
| Execution environment | local for (i) at the stored maximisers and for (ii) (2 minutes each, single core); Modal job M-014 for (i) as a search objective; Modal job M-013 for (iii) |
| Configuration | (i) every stored maximiser of job M-008 with `t₀` ranging over `[n_i(u − Λ₁), n_i(2u − Λ₁)]`; then the searches of M-008 for `n ≤ 16 000` with the bound as objective.  (ii) all 2 624 stored maximisers.  (iii) `n ∈ {64 000, 128 000}`, `u ∈ {½, 1, 2}`, `φ = 0.5`, seeds 2 and 3, three times the budgets of M-008 |
| Outputs | `experiments/eng/twolevel/results/x005_nonproduct_bound.json`, `x005_anyplacement.jsonl`, `x005_recheck_classification.json`, `x005_converge2.jsonl` |
| Validation | the generalised evaluator (Python reference and C kernel) against literal step-by-step runs for centred and off-centre brackets and in both corners of the rule; the convention of the published runs reproduces 2 615 of 2 624 stored values (the rest are the rounding-decided ties of ENG-MSG-0003 §5) |
| Code | `src/metricchain_eng/twolevel/meanrun.py` (`rung_positions`), `meanrun_kernel.c`, `ckernel.py`, `adversary.py` (objective `cost_any_placement`); `experiments/eng/twolevel/nonproduct_bound.py`, `recheck_classification.py`, `run_search.py` (jobs `anyplacement`, `converge2`) |
| Limitation stated up front | uniform inner behaviours "bottom" and "top"; ball level sets; expectation level.  Point-dependent inner behaviours are not covered |
| Result, interpretation, limitations | ENG-RES-0014 §§1, 4, 5 |

## X-010  Three nested levels of Algorithm 2L⁺: the flat instance and the worst outer landscape

| field | value |
|---|---|
| Scientific purpose | THY-RES-0004 §7 (1): does the gap between the flat instance and the worst instance, found for two levels in X-005, compound when a third level is nested?  And: does an independent implementation reproduce the referee's exact three-level numbers at the flat instance (THY-MSG-0007 §3)? |
| Source commit | engineering `f0c8375`; theory `9408e33` for the design (docstring of `experiments/reviews/R8/r8_flat3.py`, `r8_flat.py`) and the numbers to reproduce (`experiments/reviews/R8/out/flat3_a.txt`) |
| Mathematical dependencies | Theorem 11.56 applied to itself (the middle level is Algorithm 2L⁺ with base brackets inside) **[P]**; Proposition K0 **[P]**; the extensive-regime constants of theory report §11.18 **[P]**; the positions rule of X-005b **[P; ours]** |
| Execution environment | local: the flat table in 5 seconds; the worst-case grid in a process pool of 6 |
| Configuration | `u = 1`; outer level `b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `δ = 0.05`, geometric ladder of 40 rungs; middle level as in the referee's script (30 rungs; two designs, for `x ≥ 8` and `x < 8`); `n ∈ {1000, 4000, 16 000}`, twelve outer fractions 0.25 … 0.80; searches over the two profile families of X-005, budgets 4 000 + 2 000 (2 500 + 1 250 at `n = 16 000`), seed 1 |
| Outputs | `experiments/eng/twolevel/results/x010_three_levels_flat.json`, `x010_three_levels.jsonl` |
| Validation | 48 published numbers of the referee (two levels, three levels, the cost bound, rungs served by the middle level; 12 rows) reproduced to the digit given |
| Code | `experiments/eng/twolevel/three_levels.py`, `run_three_levels.py`; blocks `three_*` of `make_tables.py` |
| Limitation stated up front | **no fibre landscape is searched**: fibres are flat (a lower bound on the worst case) or represented by the middle level's cost bound (not a certified bound: it is itself searched over outer landscapes); the choice of server per rung is tuned at the flat fibre; one slope; expectation level |
| Result, interpretation, limitations | ENG-RES-0014 §§2, 3 |

## X-007  Off-lattice chain: distance entropy of profile classes, 5–14 torsions; single-flip constants against Proposition 11.74

| field | value |
|---|---|
| Scientific purpose | Is the growth of off-lattice certificate sizes per torsion the growth of the number of classes divided by `e^σ` with a size-independent distance entropy `σ`?  Do the exact single-flip constants satisfy the two-sided bound of theory report Proposition 11.74?  (THY-REQ-0008, items 5 and 6) |
| Source commit | theory `63efc69` (statement of Proposition 11.74; definitions of THY-REQ-0008); chain definitions as X-002 / X-004 (`d81eb8a`) |
| Mathematical dependencies | Proposition 11.74 **[P]** (statement under test); `P_REPORT.md` Proposition 2 for the profile distance **[P]** |
| Execution environment | local, single core |
| Inputs | `experiments/eng/chain_cover/results/lattice_Sc12_flip.json` (X-002); enumeration of the generic chain by `generic_chain.enumerate_generic` (X-004) |
| Outputs | `experiments/eng/chain_cover/results/generic_Sc16_entropy.json` |
| Validation | 113 587 conformations and 13 012 classes at 13 torsions, the two numbers published in `P_REPORT.md` |
| Code | `experiments/eng/chain_cover/generic_entropy.py`; blocks `flip_bounds`, `flip_scaling`, `generic_entropy`, `generic_entropy_growth` of `experiments/eng/chain_cover/make_tables.py` |
| Result, interpretation, limitations | ENG-RES-0009 |

## X-011  Nested runs of Algorithm 2L⁺ designed by certified cost: the bound, the best case, the worst case found; literal nested runs

| field | value |
|---|---|
| Scientific purpose | The research owner's question (directive D-3): why do the nested algorithms deteriorate on non-flat fibres, and do designs tuned against the worst case improve on designs tuned at the flat instance?  THY-RES-0013 §4 items 2, 3; THY-RES-0015 §6 (R16-THY-1(b)).  Campaign BM-1 |
| Source commit | theory `dd067f1` (remark (1b) of §11.19: the rule "servers by certified cost"; `experiments/coordinator_checks/three_levels_certified/` read as text for the candidate designs), `63efc69` (the text of Theorem 11.56 implemented); engineering: the commit stored in every result row (`55bec29` for M-016, M-017) |
| Mathematical dependencies | Theorem 11.56 applied to itself to any depth **[P; theory; the rule reviewed by the science division, SCI-REV-0016]**; Proposition K0 **[P]**; Theorem 11.25(a) for the lower bound **[V on the theory branch]**; Proposition P of ENG-RES-0015 §5 (dovetailing) **[P; ours; not refereed]** |
| Parts | (a) the certified bound to six levels, two design families, nine sizes — job M-016; (b) the designs selected at ten outer fractions run in the mean-run model at the flat instance and on searched outer landscapes with flat and cone fibres, and two levels at three more sizes — job M-017; (c) designs against global cones as a game, local; (d) per-rung anatomy of two runs, local; (e) cone fibres of intermediate slope for the selected designs, local; (f) three nested levels run literally end to end on 15-site cubes — job M-019 |
| Protocol | `docs/engineering/benchmarks/protocols/BM-1_X-011.md`: hypotheses H1–H7 committed before M-016/M-017, H8 before M-019 |
| Configuration | `u = 1`; top level `b = 0.5`, `λ = 0.2`, `η = η′ = θ = 0.05`, `δ = 0.05`, 40 rungs (certified accuracy `0.8715`); families "theory" and "wide" of `certified.py`; searches as in X-010 (differential evolution over monotone and general radial outer landscapes, 4000 + 2000 evaluations, 2500 + 1250 from `n = 8000`), seed 1 |
| Outputs | `experiments/eng/twolevel/results/x011_certified1.jsonl`, `x011_instances1.jsonl`, `x011_portfolio.json`, `x011_rungs.json`, `x011_fibre_slopes.jsonl`, `x011f_nested1.jsonl` |
| Validation | seven published numbers of the theory division's table reproduced to four digits; the pruned search equals the plain recursion to nine digits; two-level cells reproduce ENG-RES-0014 (`0.9839`, `1.0114`, `1.0461` at `n = 1000`); the flat-tuned trees reproduce the referee's flat costs and served-rung counts (`portfolio.py --check`); `tests/eng/test_certified.py` |
| Code | `src/metricchain_eng/twolevel/certified.py`; `experiments/eng/twolevel/nested_bench.py`, `portfolio.py`, `rung_anatomy.py`, `fibre_slopes.py`, `nested_literal.py`, `make_tables_x011.py`; `modal_jobs/bench_app.py`, `bench_collect.py` |
| Limitation stated up front | costs on instances are in the mean-run model (literal nested runs only at 15 sites); searched worst cases are lower bounds within radial outer landscapes and cone fibres; finite design families; one slope and one accuracy |
| Result, interpretation, limitations | ENG-RES-0015 (and its addendum for `n ≥ 32 000`) |

## X-012  An exact checker for "shares at the leaves" certificates

| field | value |
|---|---|
| Scientific purpose | Request P7-E2 of the science division (SCI-RES-0014 §7): a compiled exact checker of the certificate format of its workstream P7 — the rule `leaf`/`branch` of the Lean `verify` — where the Lean kernel cannot evaluate.  Campaign BM-2, stages A and B |
| Source commit | science `2b4ccdf` (`docs/science/workstreams/P7_REPORT.md` §§2.1, 5.1–5.4; nine certificate files and their checksums) |
| Mathematical dependencies | none beyond integer arithmetic; the soundness argument is `REPORT.md` §3.1 (the argument of `leaf_sound`/`verify_sound` **[V on the theory branch]**) |
| How it was made | by an independent subagent of this division from the text, without opening the science division's code before the checker was frozen; checked by the coordinator (a third thirty-line checker; tests re-run; core read) |
| Outputs | `src/metricchain_eng/leafcert/`; `experiments/eng/leafcert/REPORT.md`, `results/vectors.json` |
| Validation | nine files accepted by both engines with matching checksums; 27 controls and 472 exchanges rejected on an inequality; counts equal the published table in every cell; enumeration of all nine domains; 24 092 fuzz certificates with no unsound acceptance; 26 865 integer mutants; 41 broken copies of the checkers all detected; `tests/eng/test_leafcert.py` (182 tests) |
| Limitation stated up front | tested, not verified; says nothing about the link between the published integer instance and a real-valued model; no producer on this branch |
| Result, interpretation, limitations | `experiments/eng/leafcert/REPORT.md`; reported to the science division in ENG-MSG-0007 |

## X-014  Site-dependent slopes at finite `n`: type-aligned nesting, an exact lower bound, literal runs

| field | value |
|---|---|
| Scientific purpose | The research owner's directive on generality (D-2, first item): what do the two-level theorem and its nestings give, with finite-size constants, when the sites of the cube have different slopes?  Own initiative; campaign BM-6 |
| Source commit | theory `8ff0667` (theory report §11.26, Theorems 11.95–11.101, for the asymptotic exponent; `K_REPORT.md` §§1.2, 2.2–2.4 for the proof that is transferred) |
| Mathematical dependencies | **Theorem K1 with an outer block of one site type [P; ours; ENG-RES-0016 §2; not refereed]**; the lower bound by weighted dips **[P; ours, by the argument of Theorem 11.25(a)]**; `h = max_t Σλ_jF_j(t)` **[P; theory, Theorems 11.98, 11.99]** |
| Parts | (a) bounds on 75 mixtures of two site types — job M-018; (b) literal runs of the algorithm with the transferred constants on cubes of 11–16 sites, with two negative controls — local; (c) end to end with three slopes inside X-011(f) |
| Protocol | `docs/engineering/benchmarks/protocols/BM-6_X-014.md` (hypotheses H1–H4, written after five preliminary cells and before M-018) |
| Outputs | `experiments/eng/twolevel/results/x014_hetero1.jsonl`, `x014_literal.json` |
| Validation | with one site type the module returns the constants, the bounds and the lower bound of the homogeneous module to the last digit; the lower bound against a brute-force scan on eleven sites; the dip is in the class and has the stated excess (exhaustive on six sites); `tests/eng/test_hetero.py` |
| Code | `src/metricchain_eng/twolevel/hetero.py`; `experiments/eng/twolevel/hetero_bench.py`, `hetero_literal.py` |
| Limitation stated up front | the certified status of (a) is conditional on a proof transfer by one author; two site types, binary sites; no mixed outer blocks; bounds, not runs |
| Result, interpretation, limitations | ENG-RES-0016 |

## X-013  Exact vertex enumeration of the weighted cubes of workstream Y (R10-E1)

| field | value |
|---|---|
| Scientific purpose | The science division's request R10-E1 (SCI-REV-0010 §7), serving the theory division's question R10-T2: at which slope does a two-state chain as known part stop being harder than independent sites?  Block bounds from the vertices of the Lipschitz polytope of the weighted cubes `(u, …, u, u*)` |
| Source commit | science `2b4ccdf` (the request; R10 §5, the map); theory `8ff0667` (workstream Y, Proposition F) |
| Mathematical dependencies | Proposition F of workstream Y **[P; theory]** for "below the cube"; everything else is exact enumeration and interval arithmetic |
| Outputs | `experiments/eng/weighted_cube/results/`, report `experiments/eng/weighted_cube/REPORT.md` |
| Validation | four enumeration methods and, for `L ≤ 4`, the Parma Polyhedra Library; the request's validation value `0.495806` enclosed by `[0.495805524594, 0.495805524595]`; the three-site count by the coordinator by brute force; **re-run and replicated by the science division on a machine without the Parma library (SCI-RES-0033)** |
| Code | `src/metricchain_eng/weighted_cube/` (independent subagent), `tests/eng/test_weighted_cube.py` |
| Result | vertices: three sites 96 / 72; four sites 21 472, 21 184, 3 160, 2 888 in four chambers; five sites 1 965 480 and 1 960 200 above `r = 3`.  Blocks of four decide one of the six cells named in R10-T2; blocks of five provably cannot decide the other five.  Closed on both sides (SCI-RES-0033; theory report Proposition 11.117(d)) |
| Found later | **importing the Parma binding (`pplpy`) switches the whole process to upward floating-point rounding** (checkpoint 6).  The certified values use software interval arithmetic and exact rationals and are not affected; the module now restores round-to-nearest after the import and after every call, and the test suite guards the rounding mode before and after every test |

## X-005c  The worst product instance re-examined after the science division's review (R18)

| field | value |
|---|---|
| Scientific purpose | SCI-REV-0018, finding M1: where the searched placement-free bound of X-005b lay above the product search, a product instance costs the bound — the excess was the shortfall of the product search, and a conclusion of ENG-RES-0014 §4 is false as worded.  Requests R18-ENG-1 … -5 |
| Source commit | science `59e88bc`; ours `1cc4e1c` as reviewed |
| Protocol | the request's own correctness criteria (SCI-REV-0018 §5); no hypothesis of ours |
| Parts | (i) all 1 440 stored maximisers of the bound as the product instances they are — local; the review's stored product instances with the compiled kernel; (ii), (iii) the product search and the bound search at `n ≤ 500` with the review's starting points, three rounds — jobs M-023, M-024, M-025; cross-evaluation of every maximiser under both objectives; a control at `n = 1000, 4000` — local |
| Outputs | `experiments/eng/twolevel/results/x005c_*.json|jsonl` |
| Code | `experiments/eng/twolevel/r18_products.py`, `make_tables_x005c.py`; the guard and the sparse table in `src/metricchain_eng/twolevel/meanrun.py`; tests in `tests/eng/test_twolevel.py` |
| Result | M1 confirmed with the compiled kernel to nine decimals.  The worst product instance known at `n ≤ 500` exceeds that of job M-008 in 81 of 108 cells, by up to `0.026·na`; bound and product instance coincide in 107 cells after cross-evaluation.  **The search is not converged to the review's `10⁻⁴·na`** after three rounds (each still moves 20 to 37 cells by more than `10⁻⁴`).  ENG-RES-0017 (a linked correction of ENG-RES-0014 and of ENG-RES-0008 at three sizes) |
| Rule adopted | when two searches over equal or nested families are compared, the maximiser of each is evaluated under the other objective before the difference is read (`benchmarks/BENCHMARK_LIMITATIONS.md`) |

## X-015  The theory division's false certificate under unbounded influence, by a third implementation

| field | value |
|---|---|
| Scientific purpose | Stage A/C for the theory division's Proposition 11.121 (workstream N, N12; candidate E-C3 of THY-MSG-0018 §6): with a dependent known part of unbounded influence, Algorithm 2L⁺ run with the tail function of the assumed class certifies a false bracket |
| Source commit | theory `eb88823` (theory report §11.33; the instance from the statement alone; the workstream's scripts were not read) |
| Outputs | `experiments/eng/twolevel/results/x015_false_certificate.json` |
| Code | `experiments/eng/twolevel/false_certificate.py`; `hetero_literal.run_2l_fibres` (our literal simulator of X-014, with the tie rule) |
| Result | instance facts reproduced (`A = 1.0747·10⁻³`; 99.986 % of it on 13 outer points; jump `e^{11.765}`; (TU) violated by `1.747·10⁵`); assumed class: an invalid bracket in 360 of 360 runs (three parameter sets, three inner behaviours), upper end below `A` by factors 111 to 185, every sampling certificate true; true class: valid in 72 of 72 runs at 1 056 to 1 882 times the outer cube.  ENG-MSG-0007 §4 |
| Limitation | the algorithm's parameters are ours, so the factors differ from the workstream's (294; 3 680); one instance |

## X-016  First independent review of the structural-biology division's software (BM-7)

| field | value |
|---|---|
| Scientific purpose | The research owner's directive D-6: independent verification of that division's research software.  Its first commit: an exact pairwise model, a "min" certificate format with a checker, a GMEC producer |
| Source commit | structural biology `720e0ec` (read in full; run from a pinned, read-only worktree; nothing copied) |
| Parts | re-run of its nine tests; an independent checker with a strict loader written from the format description; A random certificate trees (22 472 claims, three checkers, enumeration); B traps; C limits of the fixed-width arithmetic; D malformed documents; E the producer against enumeration and dynamic programming; F nesting depth in a fresh interpreter |
| Outputs | `experiments/eng/sb_review/results/mincert_part_{a..f}.json` |
| Code | `experiments/eng/sb_review/indep_mincheck.py`, `attack_mincert.py`, `make_tables.py` |
| Result | the checker and the producer survive every test (no false acceptance; no wrong optimum).  Three findings as software: the nested format cannot hold more than about a thousand eliminations (`dumps`, `loads`, the conversion: `RecursionError`); the loader repairs malformed documents instead of rejecting them; the model checksum is never compared.  ENG-RES-0018 |
| Limitation | no molecular layer, no benchmark and no file-format note existed at that commit; nothing about physics; the checker was compared with the theory division's Python reference checker, not with the Lean kernel |

## X-016 (continued)  The structural-biology software at its commit `0544ff4` (BM-7, stages S0–S3)

| | |
|---|---|
| Date | 2026-11-27 |
| Parts | their tests and `run.py --check` re-run in a separate environment from a copy of a read-only worktree (also at `41fa668`); parts A–E of X-016 repeated; an independent strict parser and checker of *detached* certificate files (`check_files.py`); toulbar2 through our own call; six boxes for `full_box`; their OpenMM validation on more configurations |
| Outputs | `experiments/eng/sb_review/results/head_0544ff4/`, `dev_certificates_0544ff4.json`, `probe_head_0544ff4.json` |
| Code | `experiments/eng/sb_review/check_files.py`, `export_tables.py`, `probe_head.py`, `depth_head.py` |
| Result | the three findings of ENG-RES-0018 are repaired; claims K1–K4, K6–K8 survive; the six instance checksums reproduce bit for bit on a second machine; all six stored certificates accepted by our checker; six optima equal toulbar2's.  ENG-RES-0019 |
| Limitation | development instances only; claim K5 rests on one author's code on both sides except OpenMM; model v1 has since been withdrawn by its authors |

## X-017  The theory division's machine-checked kernel executed on the structural-biology certificates

| | |
|---|---|
| Date | 2026-11-27 |
| Question | does the verified function `verify` itself (not a Python mirror of it) accept the six stored certificates for the published integer tables? |
| Method | a Lean program reads an instance and a certificate (our parser and translator; their conversion is not used), builds the kernel's objects and evaluates the kernel; digests of the instance as the kernel reads it are compared with the Python side; negative controls |
| Finding about the kernel | `verify` takes time exponential in the length of an elimination chain (30 ms, 179 ms, 1.4 s, 6.2 s, 34 s for 9 … 21 eliminations): its domains are nested function updates that are re-evaluated at every lookup.  `verifyM` (domains copied into an array after every step) is **proved equal to `verify`** (`verifyM_eq`, checked by Lean at every run) |
| Outputs | `experiments/eng/sb_review/results/kernel_0544ff4.json`, `kernel_small.json`, `kernel_run_*.log` |
| Code | `experiments/eng/sb_review/lean_kernel/RunKernel.lean`, `export_for_kernel.py`, `make_small.py`, `collect.py` |
| Result | all six accepted at exactly the witness's energy (3.3 to 44.9 s each), the bound plus one unit refused in all six, three corrupted inputs refused; on eight small cases `verify` and `verifyM` were both executed and agree.  ENG-RES-0019 §3 |
| Limitation | an execution by Lean's interpreter, not a proof term; the reader is trusted up to the digests; token files and exported tables are not committed (regenerable; identified by checksums) |

## X-018  An independent checker of the structural-biology division's partition-function certificates (subagent)

| | |
|---|---|
| Date | 2026-11-27; stopped at the step in progress by the consolidation directive |
| Method | a checker written from the docstrings and frozen before the implementation was read; differential testing on enumerable instances against a truth in ball arithmetic; adversarial variants; the certified exponential against two references |
| Outputs | `experiments/eng/sb_zcheck/results/` |
| Code | `experiments/eng/sb_zcheck/` (`indep_zcheck.py` frozen; `campaign_z5.py` **never run**), `tests/eng/test_sb_zcheck.py` |
| Result | 96 559 certificates on 3 000 instances: no accepted interval misses the truth at default settings.  **F1: the float tier at `exp_bits` 990–991 accepts an interval 0.31 nats off** (reproduced by the coordinator: `f1_direct.py`).  Claim Z3 false as worded; loader exceptions; a certificate that exhausts the checker.  `experiments/eng/sb_zcheck/REPORT.md`; ENG-RES-0019 §4 |
| Limitation | the checker (982 lines) is unread by the coordinator; claim Z5, rounding-mode and magnitude experiments not run |

## X-019  GEOMETRY-REQ-0006: a certified global maximum on the 4-torus and a certified realisation in four dimensions (subagent)

| | |
|---|---|
| Date | 2026-11-27 |
| Method | Arb ball arithmetic (python-flint): branch and bound with vertex bounds for multi-affine forms, Krawczyk for the local step, a second certificate by reduction to two angles; Krawczyk on the 16 length equations; seven controls; 18 mutants |
| Outputs | `experiments/eng/geometry_req6/results/` |
| Code | `experiments/eng/geometry_req6/`, `tests/eng/test_geometry_req6.py` |
| Result | instance A (couplings rounded to six decimals): the maximum `1.170178163968538…` is attained exactly at `±θ̂`; a realisation in `ℝ⁴` with fourth singular value `≥ 0.238`; controls as expected; 17 of 18 mutants killed, the survivor equivalent.  `experiments/eng/geometry_req6/REPORT.md`; ENG-MSG-0008 §4 |
| Limitation | the coordinator re-ran tests and drivers and did not read the trusted core; the model identity at 111° is tested, not proved; instance B not examined |
