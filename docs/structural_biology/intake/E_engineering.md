# STRUCTBIO intake: the Engineering ("Ubuntu") division

**What was reviewed.** A read-only worktree of branch `research/ubuntu-engineering` at head `96c4fd22258646fd7500cbe50eb6450ae011afcf`, committed 2026-11-26 21:55 UTC. Its "Resume here" state is dated about 21:45 UTC. Paths below are relative to the worktree root. The worktree was not modified. I ran the leafcert API and its test file outside the tree, with `METRICCHAIN_ENG_BUILD` and `-p no:cacheprovider` set so that nothing was written inside it; `git status` stayed clean.

**The short version.** Engineering already has an exact, independently written checker for a GMEC-style lower-bound certificate on pairwise integer instances (`leafcert`). Its own agenda item E-2 plans "public fixed-sequence side-chain-positioning cost-function networks", which is STRUCTBIO's lead project. Several things do not exist on this branch: a certificate producer, a partition-function checker, a baseline specification for BM-2, and any allocation or mention of a seventh division.

---

## A. How to submit work to Ubuntu

### A.1 Channel and request format

Requests go through the mailbox, not the registry. A request is a message in *your own* division's mailbox, addressed to engineering. The protocol is in `docs/collaboration/README.md`, under "Shared computation" and "Message format". Engineering then enters a row in its queue. The required header is:

```
Message ID / Message type / From / To / Date and time (UTC) / Priority /
Status: Proposed | Acknowledged | Accepted | In progress | Completed | Deferred | Blocked | Declined | Superseded
Relevant source commit / Related theorem or experiment / Related message/request IDs
```

The required body sections are: Scientific context; Question, finding, or request; Evidence and reproduction instructions; Assumptions and limitations; Expected scientific value; Requested response.

**Computational requests add:** proposed computational approach; suggested inputs; expected outputs; resource requirements; estimated runtime or complexity; suggested validation protocol; stopping conditions.

The shared-computation paragraph (D-4 §6, D-5) says a request must state "the mathematical claim, the exact source commit, the assumptions, the proposed method, baselines, correctness criteria, expected outputs, a resource estimate and a stopping condition."

The unpublished draft `docs/engineering/drafts/ENG-MSG-0007.draft.md` §2 cites GEOMETRY-REQ-0001 as "a good example of the form". It also says: "What it costs you: nothing … a request authorises no spending … Please do not start substantial Modal workloads of your own. Local computation of minutes to hours needs none of this: ask."

### A.2 Readiness criteria

These are quoted from `docs/engineering/benchmarks/BENCHMARK_READINESS.md`, which follows D-5 §4. A result is benchmark-ready, and so "may enter stage D or E, i.e. may cost real money", when all of the following exist:

| # | requirement | how it is checked |
|---|---|---|
| R1 | exact mathematical definitions | the benchmark's code is written from them, not from the originating code (stage A) |
| R2 | explicit assumptions | listed in the registry entry; stage C tests inside and outside them separately |
| R3 | a precisely stated theorem, conjecture or algorithm | cited by document, section and commit |
| R4 | a pinned source commit | in the registry entry and in every result row |
| R5 | a reference implementation or a complete algorithm description | named; if only an implementation exists, the description is reconstructed and sent back for confirmation |
| R6 | correctness and performance criteria | fixed before the run |
| R7 | known limitations | copied into `BENCHMARK_LIMITATIONS.md` |
| R8 | a meaningful baseline | `BASELINE_SPECIFICATIONS.md` |
| R9 | a credible validation protocol | exact ground truth on a subset, negative controls, a stopping condition |

Two further rules from the same file:

- "A result that fails R1–R5 gets stages A–C only: small exact examples, falsification attempts, and a message to its authors saying what is missing."
- "'The specification changes daily' is a failure of R3/R4 unless the computation is itself the tool of discovery, in which case it is entered as an *investigation*, not a benchmark."

### A.3 Stage hierarchy (D-5 §5; `BENCHMARK_MASTER_PLAN.md` §1.2)

The stages are taken in order: "A stage is entered only when the one before it has a recorded result."

- **A** – independent reproduction from the definitions.
- **B** – exact ground truth (enumeration, exact or interval arithmetic, closed forms, an independent reference algorithm, a checked certificate), with edge cases and negative controls.
- **C** – adversarial and assumption-stress instances, separating failures inside the hypotheses from behaviour outside them.
- **D** – fair baselines "at equal accuracy, equal information access and honestly counted cost".
- **E** – Modal scaling campaigns.
- **F** – independent replication.

### A.4 Queue file and columns

The queue is `docs/engineering/benchmarks/BENCHMARK_REGISTRY.md`. Its columns are:

`# | request | from | objective (the claim evaluated) | source commit | readiness | expected value | cost estimate / max cost | run time | validation | status | results, limitations`

It has four sections: "Active and next" (Q-01 … Q-14), "Accepted, lower priority", "Not decided or deferred" and "Closed". "Max cost" is the sum of the worst cases of the entry's ledger jobs; "—" means local only.

### A.5 Identifier conventions

| item | convention |
|---|---|
| Engineering messages | `ENG-MSG-nnnn`, `ENG-REQ-nnnn` (requests to theory), `ENG-RES-nnnn` (answers) |
| Other divisions | `THY-…`, `SCI-MSG/SCI-REV/SCI-RES`, `GEOMETRY-REQ-0001`, `ENSEMBLE-MSG-…`, `COMPLEXITY-MSG-…` (new divisions choose their own prefixes) |
| Sub-items inside a message | e.g. `P7-E2`, `R7-ENG-3` |
| Experiments | `X-nnn` (with letter suffixes, e.g. X-005b, X-011f) |
| Modal jobs | `M-nnn` |
| Queue rows | `Q-nn` |
| Campaigns | `BM-n` |
| Dead ends | `ED-n` |
| Owner directives | `D-n` |
| Hypotheses | `Hn`, written before launch in `benchmarks/protocols/BM-x_X-yyy.md` |

A STRUCTBIO prefix has not been assigned anywhere. My inference: it is ours to choose, as it was for the other new divisions (README line 28–30).

### A.6 How accept / defer / decline is decided

Requests are decided by readiness, value and budget, and engineering says which (README "Shared computation"; registry header). The money rules are in `COMPUTE_LEDGER.md` "Policy" and the master plan §1.4:

- the first stage of a campaign is at most $60 worst case;
- a larger stage runs only after a smaller one predicted its own cost within a factor of 2;
- no single job has a worst case above $250;
- the billed cost must stay $0.00.

The engineering launcher `modal_jobs/bench_app.py` enforces part of this. It refuses a dirty tree, a missing ledger number, or a cost above `--max-usd`, which defaults to 60.

Other division-specific rules:

- **Inputs from outside are reviewed before use.** In ENG-RES-0013 §6 the science division's peptide requests ("a fixed backbone, a rotamer library, an implicit-solvent energy") were "within the scope … but not decided: each needs external inputs … that this division must review before using."
- **Other divisions' code is read as text and is not executed or copied** (`REPRODUCIBILITY.md`, "Provenance").
- **Scope.** "Fixed-sequence structural characterisation" is in scope. "Biological sequence engineering, target-specific functional optimisation and experimental execution" are out of scope.

### A.7 Artifacts they expect and produce

- Pinned commits everywhere.
- Result rows in JSONL carrying `task_id`, `commit`, `job` and `task_seconds`.
- Tables in messages generated by `make_tables.py --verify`. Arithmetic on rounded entries is banned after two published errors.
- A `--check` flag on every reproduction.
- A protocol file with hypotheses committed before launch.
- A `REPORT.md` next to the code.
- For checkers: files with sha256 checksums, negative controls, and published counts.

### A.8 Turnaround implied by the log

- **P7-E2** (the leafcert checker): read at about 15:11 UTC, committed as `0e5103b` at 16:59 UTC on 2026-11-26. That is about 2 hours for a local stage A/B task done by a subagent.
- **GEOMETRY-REQ-0001**: arrived about 16:50 UTC and was in progress by a subagent the same evening.
- **Modal jobs**: launched within hours of their protocols.
- **Science division's peptide requests**: still "not decided … none has been read in full" more than a day after they arrived.

Expect same-day turnaround for small, exactly specified, local tasks. Underspecified requests, or requests that need external inputs, can sit in the queue.

### A.9 What engineering has said about new divisions

- `BENCHMARK_MASTER_PLAN.md` §3: "Nothing is specified yet … Until requests arrive the allocations are untouched; they are planning guidance and move to wherever the mathematics is ready."
- `BENCHMARK_READINESS.md`: "ensemble / geometry / complexity — no request received".
- Draft ENG-MSG-0007 §6 offers "exact enumeration and counterexample search on small instances of any statement you can write as a finite check; and an independent re-implementation of any algorithm whose description fits on a page".
- D-4 §4 tells engineering: "Do not shift your entire research agenda toward supervising the new divisions."
- **Nothing anywhere mentions a seventh division or STRUCTBIO** (searched in `docs/`, `src/`, `experiments/eng/` and `modal_jobs/`).

### A.10 Skeleton of an ideal STRUCTBIO request

```
Message ID:            STRUCTBIO-REQ-0001
Message type:          Request for computational research (benchmark, stages A–B; stage D later)
From:                  Structural & Computational Biology, Software Development and Applications (branch <ours>)
To:                    Computational Research Division (research/ubuntu-engineering)
Date and time (UTC):   …
Priority:              Medium
Status:                Proposed
Relevant source commit: <our commit> (producer + instance files); engineering 96c4fd2 (leafcert); science 2b4ccdf (P7 format)
Related theorem or experiment: verify_sound / leaf_sound (proofs/CertificateAlgebra.lean, [V]); P7_REPORT.md §5.1–5.3; X-012; BM-2; registry Q-14
Related message/request IDs: ENG-MSG-0001 (E-2), SCI-RES-0014 P7-E1, SCI-REV-0006 §7 E-1

Scientific context: certified fixed-backbone side-chain GMEC lower bounds on real protein structures (fixed sequence; no design).
Question/claim: for instances I_1..I_k (published files, sha256 listed), the certificate C_k proves min E ≥ L_k on the integer
  instance; the integer instance is a sound outward-rounded lower model of the float energy (lemma, section, status [P]/[V]).
Proposed approach: (A) run leafcert (both engines) on our files; (B) brute force on enumerable sub-boxes; negative controls
  (L+1, swapped children, one perturbed integer); (D) baseline: exact solver without proof (toulbar2/CP-SAT/DP), same instance.
Suggested inputs: N files (names, sizes, n sites, Σk_i, pairs), generator commit, rounding unit 2^-k kcal/mol.
Expected outputs: accept/reject per file; counts; check time; production time; solver time; certificate integers.
Baselines: as above, charged run time + "no checkable proof".
Correctness criteria: all accepted; all controls rejected on an inequality; brute force agrees where enumerable; bound ≤ solver optimum.
Resource requirements: local CPU, ≤ X core-hours; Modal stage E only after A–B, first stage ≤ $60 worst case.
Estimated runtime/complexity: O(Σ_leaves Σ_{i<j} |D_i||D_j|) integer ops per check.
Validation protocol: as R9; files frozen before run; hypotheses H1… written in advance.
Stopping conditions: first unsound acceptance → stop and report; any instance exceeding format limits → report, do not truncate.
Assumptions and limitations: integer instance only; full product domain; dense pair tables; real-valued link outside the checker.
Requested response: accept / defer / revise / decline with reasons; registry row.
```

---

## B. Budget state (`docs/engineering/COMPUTE_LEDGER.md`, `DIRECTIVES.md`)

### B.1 Owner authorisations

| directive | content |
|---|---|
| **D-1** (11-25/26) | Do not exceed the Modal credit (about $2,000, workspace shared with other projects). Engineering's own stop line was $1,500 of workspace usage per month, worst case included. |
| **D-2** | Mathematical generality, assumption audit, computational consequences. Scope unchanged; "application-specific benchmarking will be undertaken during a subsequent research phase". |
| **D-3** | Science division authorised; continuous loop; Modal "when justified" under the $1,500 line; consolidation directive "when approximately $2,000 in aggregate Claude promotional credits remain"; Claude credits expire 2026-11-30 19:00 Eastern. |
| **D-4** | Six divisions; one mailbox; "Ubuntu will coordinate substantial shared Modal computations"; other divisions must not "independently consume the shared Modal budget through substantial new workloads without authorization". |
| **D-5** | Owner's snapshot: credits $2,030.00, consumed $41.41, remaining $1,988.59, billed $0.00. **"I authorize up to $1,750 in additional justified Modal expenditure across the research program"**: preserve at least $200; never pay a charge; count the worst cases of active, queued and proposed jobs. The $1,500 line is superseded only as far as needed. "The available compute budget is not a spending quota." |

### B.2 Launch test

From ledger "Policy" rule 2:

- (a) the billed cost is $0.00;
- (b) workspace credits consumed + worst cases of running, queued and new jobs ≤ **$1,791.41**;
- (c) the same sum ≤ **$1,830.00**;
- at most 50 containers at a time, and no GPU without a reason in the ledger.

### B.3 Provisional allocations and what has been used

The allocations are D-5 §3 "flexible planning guidance", "not entitlements".

| bucket | provisional | committed (worst case) | spent |
|---|---|---|---|
| existing certificate and algorithm benchmarks | $600 | **$41.6** (M-016 $6.66, M-020 tier 2 $27.36, M-021 $7.23, M-022 $0.38) | **$9.01** since the snapshot (credits consumed $50.42 − $41.41, as of 2026-11-26 21:32 UTC) |
| ensemble | $350 | $0 | $0 |
| geometry | $350 | $0 | $0 |
| complexity | $250 | $0 | $0 |
| replication and final verification | $200 | $0 | $0 |

Engineering spent $8.73 before the authorisation (M-001…M-014). Measured costs for M-016, M-020, M-021 and M-022 are still "(to be entered)".

**Internal inconsistency.** The "total authorised" row still reads committed $0 and spent $0.07, which is stale compared with the first row.

### B.4 What remains, by their own accounting (my arithmetic)

- **Against the authorisation:** $1,750 − $9.01 spent − $41.6 committed ≈ **$1,699 uncommitted**.
- **Against ceiling (b):** $1,791.41 − ($50.42 + $41.6) ≈ $1,699.
- **Inside the $600 bucket:** about $549 uncommitted.

### B.5 Hard stop

- All computation must stop by **2026-11-30 15:00 US Eastern** (20:00 UTC).
- Claude credits expire at 19:00 Eastern the same day.
- The expiry of the Modal credit is "not visible to the CLI … not assume they coincide".

### B.6 Seventh division

**There is no allocation, mention, queue row or readiness row for a seventh division.** The $1,750 is split across five buckets for six divisions. Any STRUCTBIO Modal spend would need either a re-purposing of the guidance — the closest fit is "$600 existing MetricChain certificate and algorithm benchmarking" (BM-2 and BM-3 are in it), or "$200 replication" — or a new decision by the owner.

---

## C. Software inventory

### C.1 Environment and dependencies

- There is **no pyproject, requirements or environment file**. Dependencies are documented in prose (`REPRODUCIBILITY.md`; research log §1.1).
- **Python 3.12.16** in `~/.venvs/metricchain`: NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0, mpmath 1.3.0, CVXPY 1.9.3, OR-tools 9.15 (CP-SAT), pytest 9.2, Hypothesis 6.170, Modal SDK 1.6.4, plus pandas, scikit-learn, NetworkX and PyTorch-CPU.
- **C:** gcc 15.2. Kernels are compiled on first use with `cc -std=c11 -O2 -Wall -Wextra -Werror -shared -fPIC` into `$METRICCHAIN_ENG_BUILD` (default `<repo>/build`, git-ignored). File names carry a hash of source and flags. Loaded through `ctypes`.
- **Modal image:** Debian slim, Python 3.12, `gcc`, `libc6-dev`, `numpy==2.5.5`, `scipy==1.18.1`.
- **Tests:** `tests/eng/` has 129 test functions, many parametrised. `status/engineering.md` says "153 tests pass" at checkpoint 5, which predates leafcert's 182.

### C.2 `leafcert` (X-012; registry Q-04; campaign BM-2) — the component most relevant to us

**Files**

| file | lines | role |
|---|---|---|
| `src/metricchain_eng/leafcert/leafcert.c` | 689 | C checker |
| `loader.py` | 394 | strict JSON parsing, validation, encoder for C |
| `pycheck.py` | 247 | independent Python checker |
| `ckernel.py` | 114 | ctypes front end |
| `__init__.py` | — | `check`, `Result` |
| `__main__.py` | — | command line |

Tests: `tests/eng/test_leafcert.py` (2,495 lines). Driver: `experiments/eng/leafcert/run_vectors.py`; results: `results/vectors.json`; report: `experiments/eng/leafcert/REPORT.md`.

**What a "shares at the leaves" certificate is.** It is the science division's format from P7 (`P7_REPORT.md` §5.1–5.3 at science `2b4ccdf`). It implements the `leaf`/`branch` rule of the Lean `verify` (`leaf_sound`, `verify_sound`, `proofs/CertificateAlgebra.lean`, [V] on theory).

- **The instance:** integer tables `H_i(a)` and `J_ij(a,b)` for i<j. The energy is `E(x)=Σ H_i(x_i)+Σ_{i<j} J_ij(x_i,x_j)`; the domain is the full product of alphabets.
- **The claimed bound:** an integer `L`.
- **The tree:** a branching tree whose nodes are `{"leaf":t}` or `{"site":i,"children":{"0".."k_i-1"}}`.
- **Leaf certificates `(U, P2, m)`:** unary shares `U_i`, pair shares `P2_ij`, and messages `m_ij(a)` for every ordered pair.

In other words it is a reparametrisation (dual, message-passing, Lagrangian) lower bound per box, with branching. My inference: this is the same object as soft-arc-consistency / LP-dual bounds in cost-function-network GMEC solvers.

At every leaf box `D`, the checker verifies:

```
(S) U_i  ≤ H_i(a) + Σ_{j≠i} m_ij(a)        ∀i, a∈D_i
(P) P2_ij ≤ J_ij(a,b) − m_ij(a) − m_ji(b)  ∀i<j, a∈D_i, b∈D_j
(T) L ≤ Σ U_i + Σ P2_ij
```

Acceptance implies `E(x) ≥ L` for every x. The proof is in the `leafcert.c` header and in REPORT §3.1.

**Exact vs floating point**

- **Everything in both engines is exact.** The C engine takes 64-bit input integers, sums in `__int128` with `__builtin_add_overflow`, and contains no floating point (it compiles with `-mgeneral-regs-only`; a test asserts this). An integer outside 64 bits gives `kind="range"` and the Python engine decides. The Python engine uses arbitrary-precision ints.
- **The JSON loader is strict.** It rejects duplicate keys, fractions, exponents and NaN.
- **Floating point appears only in the test-file producer.** `lp_messages` proposes messages with SciPy/HiGHS `linprog`; `leaf_from_messages` then computes `U` and `P2` exactly; `dp_messages` is an exact tree DP. This "float proposes, exact certifies" pattern is directly reusable.

**API**

```
check(path_or_obj, engine="c"|"python") -> Result
  Result fields: accepted, kind ∈ {None, "inequality", "format", "range", "limit"}, reason,
                 failure (first failing inequality with site, state and both sides), bound, engine, notes
  counts: leaf_certificates, leaf_boxes, depth, cert_integers, instance_integers, additions, comparisons
```

From the command line: `PYTHONPATH=src python -m metricchain_eng.leafcert [--engine c|python|both] FILE.json`, and `--encode` to produce the text format for the standalone binary. That binary is built with `cc -std=c11 -O2 -DLEAFCERT_MAIN`; exit codes are 0 accept, 1 reject, 2 unreadable.

**Validation (REPORT §1, §6)**

- All 9 science files are accepted by both engines; their sha256 sums match.
- All 27 controls and all 472 child exchanges are rejected on an inequality.
- Counts equal the P7 table.
- Brute force over 18,270–531,441 states gives min 0 = L at `ref`.
- Fuzzing found 0 unsound acceptances in 24,092 certificates (246,842 in the long run), and none among 26,865 mutants.
- 41 deliberately broken copies of the checkers were all caught.
- The coordinator wrote an independent 30-line third checker that agrees with both.

**Performance:** 0.05–0.3 ms per real file in C, 0.7–3 ms through `check(...,"c")` (JSON parsing dominates), 1.3–5.2 ms in Python.

**Sizes of the nine files** (from `vectors.json`)

| file group | sites × states | depth | leaf certificates | certificate integers | instance integers | additions |
|---|---|---|---|---|---|---|
| Ser₆ (ff03) | 531,441 states | 1 | 9 / 2 shared | 2,619 / 582 | 1,269 | 17,640 |
| Lys₃ (ff99SB) | 30×29×21 | 1 | 21 / 2 | 3,486 / 332 | 2,189 | 41,643 |
| LKSE:6 | 341,172 states | 1 | 13 / 3 | 5,473 / 1,263 | 2,422 | 44,668 / 59,886 |
| Leu₁₆ | 16 binary sites | 2 | 3 | 1,848 | 512 | 4,354 |

These are toy-scale certificates for synthetic homopeptides made by the science division's own code with public force-field parameters (status file; SCI-RES-0012 §4). **Nine files are seven certificates**: the Ser₆ files at τ 0.70 equal those at 0.60 apart from `label` and `tau`.

**Limitations relevant to real proteins** (REPORT §3.2, §8, and my reading of the code)

1. The certificate covers only the integer instance in the file. The "rounded down to 2⁻⁴⁰ kcal/mol" link to a real-valued model is a separate lemma of the science division (P7.7, `pairwise_sandwich_of_class`) and is not checked.
2. The domain must be the full product. "a restricted, clash-free domain cannot be expressed in this format". No pruning or DEE domains, other than through large H entries (my inference).
3. **The format is dense** (my inference from `pycheck.Tables` and `loader.validate`). `J` must have exactly every key `i<j`, and each leaf's `m` must cover every ordered pair with a full vector. Per leaf that is `n + n(n−1)/2 + (n−1)Σk_i` integers, and (P) costs `Σ_{i<j}|D_i||D_j|`.
4. The C limits are `n ≤ 4096`, `k_i ≤ 2²⁰`, and at most 2²⁶ (about 6.7·10⁷) instance integers and 2²⁶ leaf integers. My estimate for a 300-residue protein with about 50 rotamers per site: about 1.1·10⁸ dense pair entries, which is **above the limit**, and about 4.5·10⁶ message integers per leaf. A sparse-graph format is needed for realistic sizes.
5. Only gcc/clang on x86-64 (`__int128`). Tested, not verified. No formal link to Lean `verify` beyond reading.
6. **No producer exists on the branch.** A producer was "in flight" as an untracked subagent job (`src/metricchain_eng/leafprod/`, `experiments/eng/leafcert_bench/`) and is **absent from this commit**.

**Finding about the science reference checker.** `p7_06_check.py` can return True for a false bound on malformed input: an extra `U` entry or `P2` key is added to the total without being bounded. Example: `H=[[5,7]], U=[5,100], L=100`.

**Reuse potential: high.** The checker can be used unchanged as an independent exact backstop for STRUCTBIO certificates at small to medium sizes. For real proteins it needs a sparse extension (an absent pair means J≡0 with no messages) and probably restricted domains. The extension would have to keep the two-engine, enumeration-fuzz discipline. We could use the test-file producers (`dp_messages`, `lp_messages`, `assemble`) as seeds for our own producer.

### C.3 `twolevel` (X-005 … X-011, X-014; campaigns BM-1 and BM-6)

**Modules:** `alg2l.py`, `certified.py`, `meanrun.py` + `meanrun_kernel.c`, `simulate.py`, `adversary.py`, `hetero.py`, `sampling.py`, `tables.py` (log-domain Hamming tables), `ckernel.py`.

**What it does:** evaluates Algorithm 2L⁺ (theory Theorem 11.56) and its nesting on binary cubes `L_u(Q_n)`. It computes certified cost bounds `C_max`, does mean runs, literal runs, and differential-evolution adversaries, and handles site-dependent slopes.

**Reuse for side chains: low**, because the setting is binary cubes with Lipschitz residuals under a uniform reference measure. The exception is **`sampling.binomial_exact`**: binomial sampling that is exact up to 2⁶¹ trials (numpy's sampler up to 2³¹ trials, Poissonisation with collision thinning beyond). It is reusable in any Monte Carlo estimator with huge counts.

### C.4 `chains` (X-002, X-004, X-007)

**Modules:** `dia_enum.c` and `dia_flip.c` (exhaustive diamond-lattice rotamer chains up to 24 torsions, with trans/gauche bitmaps), `profile_cover.py` (pair-distance profile classes, exact covers via HiGHS/CP-SAT, certified dual lower bounds `net_bracket`), `generic_chain.py` (off-lattice, 111° bond angle, floating point with tolerance `TOL`).

**Reuse: low to medium.** These are synthetic chains with energy `#gauche`. The off-lattice part is frozen beyond 12 torsions until it is redone in exact arithmetic over ℚ[cos θ] (Q-06; SCI-REV-0008 M2).

### C.5 `weighted_cube` (X-013)

**Modules:** `polytope.py` (four exact vertex enumerators), `chambers.py`, `wcube_kernel.c`, `exponents.py` (interval-arithmetic certificates, with mpmath at my guess).

**Method worth copying:** floating-point scans only propose candidates, and every reported bound is re-evaluated exactly or in intervals. **Reuse: low**, apart from that method.

### C.6 `modal_jobs/`

- `bench_app.py`: a generic driver whitelist (`DRIVERS`); tiers s/m/l/xl/xxl with timeouts of 20 min to 12 h and 1–4 GiB; caps summing to 50; `retries=0`; results appended to JSONL with the commit; detached mode with a `modal.Dict` store; `--dry` prints the worst case.
- `bench_collect.py` collects results.
- Older single-purpose apps: `chain_enum_app.py`, `chain_cover_app.py`, `harness_app.py`, `twolevel_app.py`.

**Reuse:** this is the framework STRUCTBIO benchmarks would be run in. A STRUCTBIO driver would have to be added to `DRIVERS` by engineering.

---

## D. Outstanding engineering items that overlap STRUCTBIO

| item | status | design written? | STRUCTBIO doing it would… |
|---|---|---|---|
| **E-1** "what is actually trusted": Lean definitions run on generated certificates vs the Python reference checker (ENG-MSG-0001; ENG-RES-0004) | "planned"; not started | yes, ENG-RES-0004: a small Lean file importing `proofs.CertificateAlgebra`, `proofs.Frontiers.PartitionCertificate` and `proofs.Frontiers.LinearKernel` unchanged; it parses JSON into `PairInstance/Cert/RCert/IProblem/ZCert/LCert`, prints `verify/verifyITop/zverifyTop/verifyLTop` via `lake env lean --run`, and a differential fuzzer compares it with the Python checker on 10⁴–10⁵ inputs. They note it "is not kernel evaluation: the trusted base grows by Lean's compiler/evaluator and by the parser" | **help**, if coordinated. STRUCTBIO needs exactly this trust argument. Building it alone would duplicate a stated engineering plan. Best split (my inference): we provide certificate files and a sparse format; engineering does the differential test |
| **E-2** "what a native `min` certificate costs at realistic sizes" | "planned" | ENG-MSG-0001: a producer (DEE, dual bounds, branching, `sum`), an independent fast checker, size and check time against solver time; "synthetic chain instances first, then on public fixed-sequence side-chain-positioning cost-function networks (fixed sequence only; no design instances). The comparison that matters is with solvers that emit no proof at all." | **direct overlap with the STRUCTBIO lead project.** It would duplicate their plan unless the work is split: we build the producer and the real-protein pipeline, they do the independent checking and benchmarking (stages A/B/D/F) |
| **Q-14 / BM-2 stages C–E** | "planned; **not ready**: needs a producer and a written baseline specification" | `BASELINE_SPECIFICATIONS.md` BM-2 lists candidate baselines (enumeration, DP on chains/trees, B&B with the same LP bound and no certificate output, CP-SAT with a proof log our kernel cannot check) and the quantities to compare (time to produce, size, time to check, time to solve without a certificate) | **help**: a STRUCTBIO producer plus a baseline specification makes BM-2 ready (R5, R8) |
| **SCI-RES-0014 P7-E1** producer for shares-at-the-leaves | "wanted by BM-2 stage D; after Q-04". Subagent job (d) was in flight and **is not in this commit** | no | Ask before duplicating: the untracked `leafprod` may surface in a later commit |
| **THY-REQ-0004** schema, exact rational checker (`verifyLTop` literally), producer (box splitting plus a per-leaf LP), fuzz for the linear-residual kernel (`proofs/Frontiers/LinearKernel.lean`, `verifyL_sound` [V]) | accepted, **not started** (registry: lower priority, "with E-1") | ENG-RES-0004 adds differential testing against Lean | neutral or help. Relevant only if STRUCTBIO uses uncertain-coefficient (robust) energies |
| **SCI-REV-0006 §7 E-1** native kernel vs pseudo-Boolean proof logging | accepted "= engineering agenda E-1, E-2"; not started | none beyond the label | **help**. A VeriPB-style comparison is a natural STRUCTBIO baseline (my inference) |
| **SCI P3-E1 / P6-E1 (Q-08)** stand-alone sandwich-certificate checker for `ln Z`; A16-E1 | readiness verdict: **"not ready for an independent checker"**. The certificate does not exist as a file, and step A recomputes class constants by unspecified closed forms | yes, two stages (draft ENG-MSG-0007 §3): (1) the science division publishes files for Val₆ and Val₂₀; engineering checks the covering inequalities and an **interval transfer matrix** for `ln Z(m_∓)`; (2) the closed-form sums recomputed in outward-rounded arithmetic from geometry, which needs P3 Theorem 3 as a specification and is where a proved rounding bound would replace (H3) | **help**. STRUCTBIO's partition-function intervals need the same file-based format. Supplying a written specification and files is what unblocks it; writing our own checker would duplicate |
| **Real-peptide requests** (SCI-RES-0002 P-E1…E3; SCI-MSG-0015 P2-E1, -E2; SCI-MSG-0020 P3-E2; SCI-MSG-0005 K-E1…E3; SCI-MSG-0007 X-E1, -E2; SCI-MSG-0024 P5-E1; SCI-MSG-0025 P6-E2; SCI-MSG-0027 P8-E2…E4, A18-E1, -E2; SCI-RES-0019 A18-E3; SCI-MSG-0028 A19-E1…E3, P9-E2, P9-E4) | **"Not decided or deferred"**; "none has been read in full"; the blocker is R5 ("an evaluator of the energy this division can run and check"). A18-E3 (about 40 CPU-hours, registered prediction) is "the best-specified … to be assessed first" | no | **STRUCTBIO is the natural owner** of the energy evaluator, rotamer library and structure ingestion that R5 asks for. This helps rather than duplicates, but coordinate with the science division, which owns the requests |

---

## E. Epistemic labels and conventions to adopt

**Theory labels** (used unchanged by engineering when citing theory):

| label | meaning |
|---|---|
| **[V]** | Lean-verified; only `propext`, `Classical.choice`, `Quot.sound`; the declaration is named |
| **[P]** | paper proof, refereed or unrefereed |
| **[K]** | known result, cited |
| **[N]** | numerical evidence only |
| **[C]** | conjecture |

**Engineering labels** (`docs/collaboration/README.md`):

| label | meaning |
|---|---|
| **[X]** | exact computation (exhaustive and/or integer or rational arithmetic, program and inputs named). An optimisation is [X] "only if optimality is certified (an exact solver's proof of optimality, or matching exact lower and upper bounds)" |
| **[X\*]** | exact enumeration combined with a floating-point LP/MILP; tolerance and margin stated |
| **[R]** | independent replication of another division's number; source and agreement stated |
| **[S]** | statistical estimate; sample size, seeds and confidence statement given |
| **[E]** | engineering observation (timing, memory, cost); platform stated |

The drafts ENG-RES-0015/16 also use **[N]** (the mean-run model), **[L]** (literal runs with exact truth) and **[P; ours; not refereed]**.

The governing rule: "A computational result never upgrades the epistemic status of a mathematical statement."

**Conventions STRUCTBIO should adopt**

- Cite by exact commit and Lean declaration.
- Messages are durable. Corrections are new linked messages; only `Status:` and a pointer may be edited in place.
- Imported results are "checked, not accepted", cited with branch, commit, assumptions and status.
- Each division writes only to its own branch, with no copies of other divisions' files; read them with `git show origin/<branch>:<path>`.
- Put hypotheses in a protocol file committed before launch.
- Store JSONL result rows with the commit, job id and seeds.
- Generate tables with `make_tables.py --verify`.
- Add a `--check` flag to every reproduction.
- Write subagent output up as a `REPORT.md` and review it before committing.
- AI reviews are "internal reviews, not external academic peer review".
- **Directory constraint:** `scripts/check_doc_refs.py` treats backticked identifiers in `docs/*.md` as Lean names, so division documents go in a subdirectory such as `docs/engineering/`.

---

## F. Results bearing on certification cost; pitfalls and dead ends

### F.1 Certification cost

- The leafcert timings and sizes in C.2 are the **only** certificate-cost measurements on the branch. They are checking cost only, on toy peptide instances.
- There are no production-cost numbers ("no producer on this branch, hence no statement about production cost").
- `DEPENDENCY_MAP.md` "Not yet connected" (stale relative to X-012): "No engineering result so far uses the certificate kernels (`verify`, `verifyITop`, `zverifyTop`, `verifyLTop`) … established upstream on 16 conformance vectors only."

### F.2 Exact-vs-float pitfalls

- **ED-8: numpy `Generator.binomial` is biased from about 10¹⁵ trials** (onset at or below 5·10¹⁴ per the science division). Means between about 60 and 10⁴ are off by up to −0.8%, and the variance by −6% at 2⁵³. A published "0 of 585,000" rested on it for a day; everything was re-run (X-006b, M-012, $1.01) and the conclusions were unchanged.
  - The theory division's THY-MSG-0015, "sequential numpy binomials are not tail-safe", withdrew its own recipe.
  - Rule: "A random-number routine is tested *in the regime in which it is used* … A test that passes at a resolution of 3 % says nothing about a 1 % defect."
  - **Relevance to STRUCTBIO:** any sampling-based Z or free-energy estimator with huge counts.
- **ED-5: floating-point equality of log weights and levels** aborted a literal run on the good event. The fix was a tie tolerance of 10⁻⁹ (`tables.TIE`). Two published rows were "decided by rounding".
- **Off-lattice chains:** results rest on float comparisons with a tie analysis. They are frozen beyond 12 torsions until exact ℚ[cos θ] arithmetic exists (SCI-REV-0008 M2). This is the same issue STRUCTBIO's rounding of a float energy into integers faces.
- **leafcert 64-bit edge:** "arithmetic modulo 2⁶⁴ would have accepted 235 [2,222] false bounds" in edge-of-range tests. Use 128-bit or unbounded sums.

### F.3 Dead ends and corrections

- **ED-3:** exact set cover "stays easy" is false beyond 18 torsions; exact integer programs need time limits and brackets.
- **ED-2, ED-4, ED-6, ED-7:** estimator, plateau and simulation-cost pitfalls.
- **ED-1:** the Lagrangian dual of the budget row is uselessly loose on the cube.
- **Five corrections of their own record** (ENG-MSG-0004 §4), including a withdrawn "two solvers agree" claim and "certified lower bound" ends that were actually solver bounds in 10 of 25 brackets.
- **Lesson for STRUCTBIO:** label solver-reported bounds separately from certified ones.

---

## G. Environment facts

| item | value |
|---|---|
| Machine | Ubuntu 26.04 under WSL2, 8 threads, 7.6 GiB RAM, about 179 GB real disk |
| Python venv | `$HOME/.venvs/metricchain` (Python 3.12.16; versions in C.1), activated with `source "$HOME/.venvs/metricchain/bin/activate"` |
| Tests | `python -m pytest tests/eng -q`; experiments `python experiments/eng/<exp>/….py --check` |
| leafcert | `python experiments/eng/leafcert/run_vectors.py` (3 s); `python -m pytest tests/eng/test_leafcert.py -q` (182 tests, under a minute); `LEAFCERT_FUZZ=10` (9 min) |
| Lean | `leanprover/lean4:v4.31.0` via elan 4.4.0; Mathlib v4.31.0 cache (7.3 GB in `.lake/`); full `lake build` about 50 min on 8 threads; peak about 4.1 GB per `lean` process |
| Audit (`bash scripts/audit_all.sh --full`, read-only worktree, `LEAN_NUM_THREADS=4`) | 39 min at `63efc69`; 60 min at `9408e33` (69 files, 4,015 declarations, 435 mutations, `AUDIT PASSED`) |
| Audit status | Latest theory head audited by engineering: `9408e33` (`d81eb8a` is the branch point). The science division reports passes up to `3cf14b9` |
| Modal | workspace "main"; ephemeral `modal run` only; limits of 100 containers and 10 GPUs |

**What I reproduced in this sandbox** (Python 3.13, numpy 2.5.3, no SciPy): the leafcert test file gave **176 passed; 4 failed and 2 errors, all `ModuleNotFoundError: scipy`** (the LP-proposal producer and the mutation and broken-copy tests that use it). A hand-made 2-site certificate was accepted by both engines, and rejected with `L+1` on (T).

---

## Provenance cards for reusable results

**1. X-012 `leafcert` exact checker**

| field | value |
|---|---|
| Origin | Engineering (an independent subagent, checked by the coordinator) |
| Commit | code `0e5103b` (2026-11-26 16:59 UTC), present at head `96c4fd2`; specification science `2b4ccdf` |
| Identifier | X-012 / Q-04 / BM-2; no ENG-RES. It was to be announced in ENG-MSG-0007, still a draft |
| Assumptions | integer pairwise instance; full product domain; dense pair tables; 64-bit inputs (C) |
| Evidence | [X] on the nine files (enumeration); soundness by paper argument = [V] `verify_sound` upstream (correspondence by reading); fuzz is testing |
| Review | internal (third checker); no review by the science division yet |
| Limitations | C.2 |
| Application | independent exact backstop for STRUCTBIO GMEC certificates |
| Ready? | **yes for small and medium dense instances; no for realistic protein sizes** without a sparse/restricted-domain extension |

**2. `sampling.binomial_exact`**

| field | value |
|---|---|
| Origin | Engineering |
| Commit | `26029c9` |
| Identifier | ED-8 / X-006b / ENG-RES-0013 §1 |
| Assumptions | double-precision probabilities; numpy's sampler is used when n ≤ 2³¹ and for means above 10⁹ |
| Evidence | [S] / [E] |
| Review | cross-checked against independent samplers from theory and science |
| Application | MC estimators with huge counts |
| Ready? | **yes**, as a utility |

**3. `bench_app.py` framework**

| field | value |
|---|---|
| Origin | Engineering |
| Commit | `0a91763` and later |
| Evidence | [E]; M-015 smoke test |
| Application | the vehicle for any STRUCTBIO Modal benchmark |
| Ready? | yes, but only engineering adds drivers and launches |

**4. Audit replication**

| field | value |
|---|---|
| Identifier | X-001 / ENG-RES-0005 / ENG-MSG-0005 |
| Evidence | [R] at four theory heads |
| Note | does not review proofs; "of the sixteen Lean files added since `63efc69` this division has read none" |

**5. ENG-RES-0015 / ENG-RES-0016**

Drafts only, not published, on adaptive cube algorithms. They are not relevant to side chains, and ENG-RES-0016 §2 is an unrefereed [P].
