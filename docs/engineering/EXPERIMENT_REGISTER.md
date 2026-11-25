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
| Result, interpretation, limitations | ENG-RES-0005 |

## X-002  Lattice chains: exact covering numbers in the profile format, 1–24 torsions

| field | value |
|---|---|
| Scientific purpose | Does the chain-length independence of certificate sizes at extensive accuracy (theory report Proposition 11.49(a)) become visible at sizes that can be enumerated?  Entropy of profile sets; realisability of trans/gauche patterns.  (THY-REQ-0002, questions 1, 2, 3(a), lattice part) |
| Source commit | `d81eb8a`; definitions from `docs/workstreams/P_REPORT.md` §§0, 2.2, 3.2, 3.3 and theory report §11.17 |
| Mathematical dependencies | `isCertificate_iff_cover` [V]; `pairRes_sub_le` [V]; Proposition 11.49(a) [P, refereed] — see `docs/engineering/DEPENDENCY_MAP.md` |
| Execution environment | enumeration `n ≤ 20`: local, single core, `cc -O3 -march=native`; `n = 21…24`: Modal, 64 single-core containers per length, `cc -O3` (job M-002).  Covers: Modal, 4 cores per length (job M-004), HiGHS (SciPy 1.18.1) and CP-SAT (OR-Tools 9.15.6755) |
| Inputs | none external: the diamond-lattice chain model is generated from its definition (tetrahedral angle, torsions 180°/±60°, self-avoidance, pairs with `q − p ≥ 3`, cutoff `S_c = 12`); known part `#gauche`; zero residual |
| Configuration | `L ∈ {1, 1/5}`; `ε ∈ {0, 1, N/20, N/10, N/4, N/2}`; entropy radii `δN`, `δ ∈ {4, 2, 1, 1/2, 1/4}`; net time limit 60 s per radius |
| Random seeds | none (exhaustive, deterministic) |
| Outputs | class tables `experiments/eng/chain_cover/data/dia_Sc12_n*.txt` (the complete enumeration result: every profile class with its number of conformations, fewest and most gauche torsions); `results/lattice_Sc12.json`, `results/lattice_Sc12_flip.json`, `results/lattice_Sc12_patterns.json`; `data/flip/` |
| Validation | (i) class tables equal an independent internal-coordinate construction for `n ≤ 7`; (ii) conformation and class counts equal the published sequences for `n = 5…13`; (iii) all 24 published covering numbers reproduced; (iv) mirror reduction and prefix splitting verified to be exact; (v) the Modal-merged table at `n = 14` equals the local one; (vi) two solvers agree on every cover; (vii) negative control: no pair inside the cutoff ⇒ one class, covering number 1.  `python -m pytest tests/eng -q` (69 tests); `python experiments/eng/chain_cover/run_lattice.py --check` |
| Result, interpretation, limitations | ENG-RES-0002 |

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
