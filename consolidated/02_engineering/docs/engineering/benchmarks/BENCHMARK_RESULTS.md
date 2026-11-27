# Benchmark results — index

One entry per finished stage of a campaign: what was tested, the outcome in one or two
sentences, and where the numbers are (artifact and reporting message).  Numbers are
*not* repeated here beyond the headline — the generated tables in the messages are the
record.  Negative results are entries like any other.

## BM-1 — nested adaptive algorithms on `L_u(Q_n)`

| stage | experiment | what was tested | outcome | artifacts; message |
|---|---|---|---|---|
| A | X-005 | the mean-run evaluator of Algorithm 2L⁺ written from the report's text; the theory division's flat-instance table | reproduced | `experiments/eng/twolevel/results/x005_*`; ENG-RES-0008 |
| B | X-006b | literal runs with real fluctuations and an exact sampler: validity, the good event, "cost ≤ `C_max` in every run", an invalid inner behaviour as negative control | 585 000 runs with the theorem's constant: no failure; with the constant divided by 4: 190 good-event failures in 117 000; the invalid behaviour is stopped by the budget and never exceeds `C_max` | `results/x006b_sampled.jsonl`; ENG-RES-0013 §§1–2 |
| C | X-005, X-005b | adversarial outer landscapes for two levels; instances that are not products; convergence of the searches | the flat instance is the best case; the worst case found exceeds it by a factor `1.46`, `1.24`, `1.12` in the exponent at `n = 1000, 4000, 16 000`; non-product instances add at most `0.0015·na`; three times the budget changes nothing | ENG-RES-0008, ENG-RES-0014 §§4–5 |
| A, C | X-010 | three nested levels (the referee's flat-tuned design): its 48 flat numbers; the worst outer landscape with flat and cone fibres | flat numbers reproduced to the digit; on cone fibres the third level keeps little of its flat-instance advantage (`0.94`, `0.92`, `0.96` of two levels); charged its certified bound it gains nothing | `results/x010_*`; ENG-RES-0014 §§2–3 |
| D | X-009 | adaptive certified cost against the non-adaptive lower bound (separation table) | 72 published numbers reproduced; the crossover size is not monotone in `n` at the first crossing | `results/x009_separation.json`; ENG-RES-0013 §3 |
| A | X-011 (first part) | the certified-cost recursion | seven published numbers of the theory division reproduced to four digits; a pruned exact search agrees with the plain recursion to six digits | `nested_bench.py --check`; this checkpoint |

## BM-4 — chain covers

| stage | experiment | what was tested | outcome | artifacts; message |
|---|---|---|---|---|
| A, B | X-002 | lattice chains to 24 torsions: class tables, exact covers, entropy brackets | every published number it could be compared with reproduced; 15 of 25 open brackets certified at both ends | ENG-RES-0002, ENG-RES-0007, ENG-MSG-0004 §4 |
| A | X-004 | the off-lattice chain to 12 torsions in floating point | published counts and 16 covering numbers reproduced; two published brackets closed; on hold beyond 12 torsions (exact arithmetic first) | ENG-RES-0007 |

## Other finished computations (not campaigns)

X-001 (audit replication of the theory branch at four heads: `AUDIT PASSED` each time),
X-003 (uniform-cube hitting numbers), ED-8 (the defect of NumPy's binomial
sampler, measured inside X-006b), X-008 (type-class ball exponents to `n = 10 000`): see
`../EXPERIMENT_REGISTER.md`.


## Results of checkpoint 6 (2026-11-26/27)

| campaign, stage | what was measured | where |
|---|---|---|
| BM-1, stages B–E (X-011) | the certified recursion to six levels at `n ≤ 16 000`; the share of each level's asymptotic gain that the certified designs keep (`0.81 / 0.86 / 0.23` for levels 3 / 4 / 5 at `n = 16 000`); designs chosen by certified cost against flat-tuned designs on searched instances at three slopes; literal three-level runs; a portfolio.  Fourteen hypotheses fixed in advance; H3 and part of H13 failed, H9 was refuted at one slope and size, H5 in its lower half | ENG-RES-0015; `benchmarks/protocols/BM-1_X-011.md` |
| BM-1, a correction (X-005c) | the worst product instance at `n ≤ 500` after the science division's review: 81 of 108 cells higher, up to `0.026·na`; three rounds, not converged to `10⁻⁴·na`; bound and product instance coincide in 107 cells after cross-evaluation | ENG-RES-0017 |
| BM-2, stages A–B (X-012) | an independent exact checker of "shares at the leaves": nine files, 27 controls, no unsound acceptance; a defect found in another division's reference checker | `experiments/eng/leafcert/REPORT.md`; SCI-RES-0030 |
| BM-6, stage A–B (X-013) | exact vertex enumeration of weighted cubes; what blocks of four and five decide | `experiments/eng/weighted_cube/REPORT.md`; SCI-RES-0033 |
| BM-6, stages A–C (X-014) | site-dependent slopes: certified bounds on 75 mixtures, mixed blocks, a binned profile; literal runs; an adversarial review inside the division (224 577 runs of the referee's simulator, no violation) | ENG-RES-0016; `experiments/eng/review_x014/REPORT.md` |
| BM-7, first review (X-016) | the structural-biology division's certificate core at its first commit: 22 472 adversarial claims, three checkers in agreement, no false acceptance; the producer exact on every instance solved independently; three findings as software | ENG-RES-0018 |
| replication for the theory division (X-015) | Proposition 11.121 (a false certificate under unbounded influence) by a third implementation: invalid in 360 of 360 runs with the assumed class, valid in 72 of 72 with the true class | ENG-MSG-0007 §4 |
| replication for the geometry division | GEOMETRY-REQ-0001 items 1, 3: the exact elimination and the exact ranks | `experiments/eng/geometry_req1/REPORT.md` |
| in review | the rate of the level recursion on new instances (Q-13) | `experiments/eng/level_rate/REPORT.md` |

Failed or negative outcomes of this checkpoint, in one place: a published conclusion
withdrawn (ENG-RES-0014 §4); a search that did not converge (X-005c); two of our own
predictions wrong (H3, H13) and one refuted at one slope (H9); weak negative controls
and a simulator without a tie rule (found by our referee before publication); a job that
cost more than its stated worst case (M-022); a library that changes the rounding mode
of the process (found by a failing test).

## Added at the consolidation halt (2026-11-27)

| benchmark | result | status | where |
|---|---|---|---|
| BM-7, stages S0–S3: the structural-biology `min` certificates at `0544ff4` | 22 472 adversarial claims, three checkers agree, no unsound acceptance; the six stored certificates accepted by an independent checker and by the theory division's kernel executed on them (3.3–44.9 s each); six optima equal toulbar2's (0.006–0.64 s) | development instances only; held-out stage **not run** | ENG-RES-0019; X-016, X-017 |
| the kernel `verify` as an executable | time grows about 1.8-fold per elimination in a chain (34 s at 21 eliminations); a memoised twin proved equal runs real certificates in seconds | a defect of performance, reported to the theory division | ENG-MSG-0008 §2 |
| partition-function certificates (capability C2), small enumerable instances | 96 559 certificates: no accepted interval misses the truth at default settings; **the float tier at `exp_bits` 990–991 accepts an interval 0.31 nats off**; claim Z3 false as worded | subagent; one finding reproduced by the coordinator; claim Z5 untested | X-018 |
| BM-1, stage 2 (X-011): both rules of design, three slopes | complete (288 cells); H14 holds at `u = ½, 1, 2` at `n = 16 000`; no searched cost above a certified bound | published | ENG-RES-0015; ENG-MSG-0008 §2 |
| BM-6 (X-014): literal runs with the tie rule | 64 800 runs with the theorem's constants: 0 invalid, 0 aborted | published | ENG-MSG-0008 §2 |
| GEOMETRY-REQ-0006 | instance A certified in ball arithmetic | subagent; reproduction checked | X-019 |
| producing leaf certificates against exact solvers | 15 % of the time is search, 85 % certificate; dynamic programming 55–89 times faster on banded chains; the limit is certificate size | subagent; **unreviewed** | `experiments/eng/leafcert_bench/REPORT.md` |
| not run | the held-out benchmark SB-BM-3; proof logging (VeriPB/CakePB); the long `ln Z` runs; anything for CASP17 | — | ENG-RES-0019 §4 |
