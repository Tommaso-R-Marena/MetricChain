# Engineering documents

| file | content |
|---|---|
| [`RESEARCH_LOG.md`](RESEARCH_LOG.md) | what was done and why, mistakes and what they changed, open observations, and **"Resume here"** — the handoff for the next session |
| [`EXPERIMENT_REGISTER.md`](EXPERIMENT_REGISTER.md) | one entry per experiment: purpose, source commit, mathematical dependencies, environment, inputs, configuration, seeds, outputs, validation |
| [`COMPUTE_LEDGER.md`](COMPUTE_LEDGER.md) | what is and is not verified about spending limits; every remote job with its bound before launch and its measured cost after |
| [`DEPENDENCY_MAP.md`](DEPENDENCY_MAP.md) | each engineering claim → the exact theorems it rests on, their status upstream, the hypotheses the computation must meet, and what connects program and statement |
| [`DEAD_ENDS.md`](DEAD_ENDS.md) | negative findings and abandoned approaches of the engineering division |

Results themselves are published as messages under [`../collaboration/`](../collaboration/README.md)
(`ENG-RES-nnnn` for answers to theory requests, `ENG-MSG-nnnn` otherwise); the digest is
[`../collaboration/ENGINEERING_TO_THEORY.md`](../collaboration/ENGINEERING_TO_THEORY.md).

These files are in a subdirectory on purpose: the theory division's audit
(`scripts/check_doc_refs.py`) reads every backticked identifier in `docs/*.md` as the name
of a Lean declaration, and engineering prose names Python and C identifiers.

Not written yet, because there is nothing to put in them: an architecture report (no
architecture has been built), an implementation-limits report beyond the "not yet
connected" section of the dependency map, and a synthesis beyond the assessment in
ENG-MSG-0001.
