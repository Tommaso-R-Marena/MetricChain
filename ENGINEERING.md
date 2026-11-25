# MetricChain — engineering branch (`research/ubuntu-engineering`)

This branch belongs to the **Computational Research Division**.  It was created at the
theory checkpoint `d81eb8a` of `claude/determined-ride-og1u7j` and contains that checkpoint
unchanged (`README.md`, `docs/`, `proofs/`, `experiments/*.py`, `scripts/`) plus the
engineering work, all of it in separate directories:

| path | what |
|---|---|
| [`docs/collaboration/`](docs/collaboration/README.md) | the mailbox between the two divisions: protocol, digest ([`ENGINEERING_TO_THEORY.md`](docs/collaboration/ENGINEERING_TO_THEORY.md)), status, messages, requests, responses, upstream sync log |
| [`docs/engineering/`](docs/engineering/README.md) | research log with the handoff ("Resume here"), experiment register, compute ledger, dependency map, dead ends |
| `src/metricchain_eng/` | engineering code (Python package and C sources) |
| `tests/eng/` | its test suite (`python -m pytest tests/eng -q`) |
| `experiments/eng/` | experiment drivers, stored exact data and results |
| `modal_jobs/` | Modal applications (ephemeral runs only) |

Start with [`docs/collaboration/ENGINEERING_TO_THEORY.md`](docs/collaboration/ENGINEERING_TO_THEORY.md)
for the findings and [`docs/engineering/RESEARCH_LOG.md`](docs/engineering/RESEARCH_LOG.md)
for how to resume.  The theory division's own entry point is the root [`README.md`](README.md).

Scope: mathematics, general-purpose certified computation, synthetic and fixed-sequence
structural characterisation.  No biological sequence engineering, no target-specific
optimisation, no experimental execution.
