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
| Result, interpretation, limitations | ENG-RES-0008 §6 |

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
