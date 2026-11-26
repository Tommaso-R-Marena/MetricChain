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
