# Benchmark registry — the shared queue of computations

One row per request for computation or benchmark, from any division, in the order of
priority.  A request is a proposal: this division accepts, defers, revises or declines
it by readiness (`BENCHMARK_READINESS.md`), value and budget, and the row says which and
why.  "Max cost" is the worst case this division has authorised for the entry (the sum
of its jobs' worst cases in `../COMPUTE_LEDGER.md`); "—" means local computation only.
Source commits are those at which the request was read.

How to send a request: `docs/collaboration/README.md`, "Shared computation" — the claim,
the exact source commit, assumptions, method, baselines, correctness criteria, expected
outputs, a resource estimate, a stopping condition.

## Active and next

| # | request | from | objective (the claim evaluated) | source commit | readiness | expected value | cost estimate / max cost | run time | validation | status | results, limitations |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q-01 | X-011a; THY-RES-0013 §4 item 3 | theory; research owner (D-3: "worst-case-tuned adaptive algorithm designs") | the certified cost bound of nested runs of Algorithm 2L⁺ with every server chosen by certified cost, for 2 … 6 levels and two families of designs: where a further level stops paying at finite `n`, and how far the bound stays from `nh` | theory `dd067f1` (remark (1b)), `63efc69` (Theorem 11.56) | **ready** (a bound computation; BM-1) | high: the finite-size content of Theorem 11.58a; tells which design to benchmark | see ledger M-015 | minutes to hours per size on one core | seven published numbers of the theory division reproduced to four digits (`nested_bench.py --check`); plain recursion against pruned search | **in progress** | — |
| Q-02 | X-011b; THY-RES-0013 §4 item 2 | theory; research owner (D-5 §6: tuned against worst cases or at the flat instance?) | the designs of Q-01 *run* in the mean-run model: flat instance, worst outer landscape found with flat and cone fibres (readings (B), (A)); against the referee's flat-tuned design (ENG-RES-0014: `0.625`, `0.553`) and against the certified bound | as Q-01; ours `ce71724` | **ready** (BM-1) | high: the owner's question | see ledger M-016 | ≤ 1 h per cell | two-level numbers of ENG-RES-0014 reproduced (`0.9839`, `1.0114`, `1.0461` at `n = 1000`) | **in progress** | searched values are lower bounds on the worst case; mean-run model |
| Q-03 | THY-RES-0015 §6, R16-THY-1(b) | theory | the two-level worst case of the design of ENG-RES-0014 at `n = 8 000, 32 000, 64 000`, minimised over the outer fraction | theory `dd067f1` | **ready** | medium: removes a mixed-design comparison from the theory report's table | inside M-016 | ≤ 3 h per cell | as Q-02 | **in progress** (inside Q-02's job) | — |
| Q-04 | X-012; SCI-RES-0014 §7, P7-E2 | science | a compiled exact checker of "shares at the leaves", written from the text; accept nine files, reject 27 controls; soundness fuzz against brute force | science `2b4ccdf` | **ready** for stages A, B | high for the kernel campaign BM-2: it is what runs where the Lean kernel cannot | — | minutes | brute force on enumerable boxes; two engines cross-checked; mutation test | **in progress** (independent subagent) | — |
| Q-05 | X-013; SCI-REV-0010 §7, R10-E1 | science (serves theory's R10-T2) | exact vertex enumeration of the weighted cubes `(u,u,u,u*)`, `(u,u,u,u,u*)`; decides the crossover slope of the chain's exponents against the uniform cube's | science `2b4ccdf`, theory `8ff0667` | **ready** for stage A | medium: the one computed case of a reference measure that is not a product | — (local, ≤ 2 h per run) | minutes for `L = 4`; `L = 5` uncertain | `L = 3`: 96 vertices and `a ≤ 3 × 0.495806` at `(0.3, 3)` | **in progress** (independent subagent) | — |
| Q-06 | SCI-REV-0008 R7-ENG-3 | science | the off-lattice chain in exact arithmetic over `ℚ[cos θ]` (precondition of every off-lattice number beyond 12 torsions) | science `d45ad56` (specification `R7_REPORT.md` §7, not read) | not assessed | high for BM-4 | — | unknown | published counts and covers reproduced exactly | **accepted, not started** | — |
| Q-07 | SCI-MSG-0011 S-E1; SCI-MSG-0008 R3-E1, R3-E2; SCI-REV-0006 E-2; THY-REQ-0008 items 1–4 | science, theory | one enumeration job: class tables of bridges, full pair-distance histograms for 13–24 torsions, joint gauche counts, homometry counts | theory `63efc69`, science `d45ad56` | lattice part ready; specification of outputs to be fixed in one message before launch | medium–high (limit shape, scattering identifiability) | to be bounded (first stage ≤ $60) | hours × tens of cores | X-002's published tables are sub-tables of the output | **accepted, not started** | — |
| Q-08 | SCI-MSG-0025 §8, P6-E1 (= P3-E1); SCI-MSG-0026 §9, A16-E1 | science | a stand-alone checker of the sandwich certificate for `ln Z`, exact or interval arithmetic | science `2b4ccdf` | **not ready here**: specification not read | high for BM-3 | — | — | their validation instance and stopping condition | **accepted in principle; after Q-04** | — |
| Q-09 | THY-REQ-0003 | theory | useful constants in the profile format (remainder `η(1 + ‖λ‖₁)`), revised design of ENG-RES-0003 | theory `d81eb8a` | design fixed in ENG-RES-0003 | medium | — | — | — | **accepted, not started** | — |
| Q-10 | THY-RES-0013 §4 item 4 | theory | slopes `u = ½, 2` for Q-01/Q-02 | as Q-01 | ready after Q-01 at `u = 1` | medium | part of BM-1 stage E | — | — | **accepted, after Q-01 … Q-03** | — |

## Accepted, lower priority (no cost assigned)

| request | from | subject | status |
|---|---|---|---|
| SCI-REV-0008 R7-ENG-2, R7-ENG-5 | science | both lower ends of open brackets, stored covers; certified branch and bound for nine optima (tree format of SCI-RES-0012 §3) | after Q-06 |
| SCI-REV-0004 §6 | science | importance-sampling sample sizes for three proposals at the cone with a field | small; not started |
| SCI-REV-0007 R6-E1 (rest) | science | design search for the separation table at fixed accuracy | superseded in part by Q-01 (the certified recursion is that search) |
| THY-REQ-0009; THY-REQ-0010 Q1, Q3; THY-REQ-0007; THY-REQ-0004 with E-1 | theory | two-phase known parts; type classes; tail functions; the linear kernel with differential testing | not started |
| SCI-RES-0014 §7, P7-E1 | science | a producer for "shares at the leaves" | wanted by BM-2 stage D; after Q-04 |

## Not decided or deferred

| request | from | subject | why |
|---|---|---|---|
| SCI-RES-0002 P-E1…E3; SCI-MSG-0015 P2-E1, -E2; SCI-MSG-0020 P3-E2; SCI-MSG-0005 K-E1…E3; SCI-MSG-0007 X-E1, -E2; SCI-MSG-0024 P5-E1; SCI-MSG-0025 P6-E2; SCI-MSG-0027 P8-E2…E4, A18-E1, -E2; SCI-RES-0019 A18-E3; SCI-MSG-0028 A19-E1…E3, P9-E2, P9-E4 | science | constants, certificates, evaluators and enumerations on synthetic homopeptides with force-field energies | inside the authorised scope as fixed-sequence structural characterisation; **none has been read in full**; each needs the readiness test (in particular R5: an evaluator of the energy this division can run and check).  A18-E3 states its own cost (about 40 CPU-hours) and a registered prediction — the best-specified of them; to be assessed first |
| SCI-REV-0001 R1-E1; SCI-REV-0005 R5-E1; SCI-REV-0003 R4-E1, R4-E2; SCI-MSG-0016 E-R8-1; SCI-REV-0006 E-3; THY-REQ-0006 | science, theory | various | deferred in ENG-RES-0013 §6; not assessed in detail |
| (none yet) | ensemble, geometry, complexity | — | branches not yet published at the last fetch |

## Closed

See `BENCHMARK_RESULTS.md` and `docs/collaboration/status/engineering.md` (completed
requests of sessions 1–3: THY-REQ-0005, R6-E1 … E3, R7-ENG-1, R7-ENG-4, THY-REQ-0010 Q2, …).
