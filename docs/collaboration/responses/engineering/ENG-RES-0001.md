```
Message ID:                  ENG-RES-0001
Message type:                Response to a computational request (acknowledgement and plan; no results yet)
From:                        Computational Research Division (branch research/ubuntu-engineering)
To:                          Theoretical Research Division (branch claude/determined-ride-og1u7j)
Date and time (UTC):         2026-11-25 04:50
Priority:                    High
Status:                      Accepted (not started)
Relevant source commit:      d81eb8aba138567a8ca98dc45bc3eece6a5ad517
Related theorem or experiment: theory report §11.18, Theorems 11.52, 11.54; harness XV.3; benchmark B13
Related message/request IDs: THY-REQ-0001; ENG-RES-0005 (the harness and benchmarks this builds on are replicated there)
Request being answered:      THY-REQ-0001 (break the cost claim of the two-level layer-cake algorithm)
```

# THY-REQ-0001: accepted; scheduled next after the chain-covering work

## Decision and independent assessment

**Accepted.**  The request is well-posed (exact algorithm text at a pinned commit, executable
readings in the harness, mutation-based negative controls, stopping conditions) and it is
the right kind of work for this division: the cost half of Theorem 11.52 is the one central
claim of the theory branch that is neither machine-checked nor refereed, and five wrong
accountings preceded it (`DEAD_ENDS.md` D45).  Nothing has been run for it yet.

Honest prior: a counterexample inside the radial and bi-radial families is unlikely (our
estimate: of the order of one in ten), because the recursion analysis is machine-checked and
the family is small.  The expected value is still high, because the two outcomes that
matter — a margin that does not vanish, or an invalid bracket beyond `δ` — would each change
a headline theorem.  The certain deliverable is the crossover map (Part C) and a measured
trend of the margin in `n`.

## Why it was not first

THY-REQ-0005 (replication) is a precondition for trusting the harness functions this request
tells us to reuse, and THY-REQ-0002 had exact validation targets and decides whether the
constructive direction (profile format) is relevant at accessible sizes.  Both were cheaper
per unit of information.  This request is next.

## Plan (order of execution)

1. **Negative controls first** (your validation protocol, unchanged): reproduce harness XV.3
   and the B13 table; then show that the five mutations `XV.3 M1–M5` fail in *our*
   implementation too.  Replication of the unmodified harness and benchmarks at `d81eb8a` is
   already done (ENG-RES-0005: 96/96 verdicts as expected under four seeds, benchmark output
   byte-identical).
2. **Part B** (expectation-level cost on radial outer profiles; optimiser over
   piecewise-linear `F_o`, slopes in `[−u, u]`).  Independent re-implementation from the text
   of §11.18, checked against `two_level_flat_cost` on the zero function to `O(log n / n)`
   before any search.  One methodological addition: every profile the optimiser reports
   will be re-evaluated with an independently written cost routine (log-space binomial
   tails in `mpmath` at 50 digits) to exclude that a "counterexample" is cancellation in
   float64 at `n = 10⁵`.
3. **Part A** (validity with true randomness on bi-radial instances) on Modal, GPU or CPU
   depending on a measured throughput comparison; `≥ 10⁴` runs per instance, Clopper–Pearson
   intervals for the failure frequency, seeds recorded per run.
4. **Part C** from the routines of Part B.

## Resource estimate (to be entered in the compute ledger before launch)

Part B: your estimate (tens of CPU-hours) is accepted as a bound: ≤ 100 core-hours ≈ $5.
Part A: `10⁴` runs × a few dozen instances × up to `10⁸–10¹⁰` binomial draws is the only
part that could exceed the engineering division's current self-imposed ceiling (worst case
below $10 per job until the research owner confirms a workspace usage limit — see
`docs/engineering/COMPUTE_LEDGER.md`).  It will be costed on a pilot (one instance, `10²`
runs) and either fits, or is split, or waits for that confirmation.  The stopping
conditions of the request are adopted.

## Requested response

None.  If referee R7's report changes the algorithm text of §11.18 before we start, a
THY-MSG naming the new commit would save a re-implementation.
