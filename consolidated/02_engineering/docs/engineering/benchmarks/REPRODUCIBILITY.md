# Reproducibility

How a successor re-runs anything this division reports.  Paths are relative to the
repository root; the branch is `research/ubuntu-engineering`.

## Environment

| item | value |
|---|---|
| machine of record | Ubuntu 26.04 LTS under WSL2, 8 threads, 7.6 GiB RAM (local); Modal containers: Debian slim, Python 3.12, one core, 1–4 GiB per task |
| Python | 3.12 in a virtual environment; NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0, mpmath 1.3.0, CVXPY 1.9.3, OR-tools 9.15, pytest 9.2, Hypothesis 6.170, Modal SDK 1.6.4 |
| C | gcc 15.2 (local), Debian's gcc (Modal); the C kernels are compiled on demand into a cache directory (`METRICCHAIN_ENG_BUILD`), never committed |
| Lean | toolchain `leanprover/lean4:v4.31.0` with the Mathlib cache of that tag — needed only for the audit replication of the theory branch |
| container image of the Modal jobs | defined in code: `modal_jobs/bench_app.py`, `modal_jobs/twolevel_app.py` (pinned NumPy and SciPy; the source tree is mounted from the commit that launches the job) |

A known defect of the numerical library matters for anyone who re-implements the
literal simulations: NumPy's `Generator.binomial` is biased for more than about `2·10¹⁴`
trials at means between about 40 and `10⁵` (`DEAD_ENDS.md` ED-8); the samplers here use
`metricchain_eng.twolevel.sampling.binomial_exact`.

## Tests

    python -m pytest tests/eng -q

## Tables and numbers in messages

Every table and summary sentence of a published message is a block
`<!-- TABLE:name --> … <!-- /TABLE:name -->` generated from stored artifacts:

    python experiments/eng/<experiment>/make_tables.py --verify <message.md>     # fails if a block differs from the artifacts
    python experiments/eng/<experiment>/make_tables.py --write  <message.md>     # regenerates the blocks

The addendum `X-011_ADDENDUM.md` (rows of jobs M-016 and M-021 collected after the halt) is verified the
same way with `experiments/eng/twolevel/make_tables_x011.py`; the integrity of its rows with
`python experiments/eng/twolevel/check_late_rows.py --recompute` (output stored in
`experiments/eng/twolevel/results/x011_late_rows_check.txt`).

Numbers in running prose are checked against the generated tables before publication;
arithmetic by hand on rounded entries has produced published errors twice
(ENG-MSG-0004 §4) and is not done.

## Remote jobs

    modal run modal_jobs/bench_app.py::main --driver <driver> --job <job> --dry            # task list and worst-case cost; starts nothing
    modal run modal_jobs/bench_app.py::main --driver <driver> --job <job> --ledger M-0xx

* The launcher refuses to start from a working tree that differs from its commit, without
  a ledger number, or above `--max-usd` (default $60, the first-stage limit).
* Results are appended to `experiments/eng/<dir>/results/<prefix>_<job>.jsonl`, one JSON
  object per task, with `task_id`, `commit` (the code that ran), `job` (the ledger entry)
  and `task_seconds`; a re-run skips the task ids already stored.
* Job logs contain the Modal run URL, which contains the workspace name: they are kept
  outside the repository and never committed.
* Seeds are task parameters and are stored in the rows.  A search is deterministic given
  its seed and budget; a literal simulation is deterministic given its seed and sampler.

## Provenance of what is compared with

Other divisions' numbers are cited with branch and commit in the experiment register and
in the message that uses them; their code is read as text and is not executed or copied
(`docs/collaboration/UPSTREAM_SYNC.md`).  Where a published number of another division
is reproduced, the reproduction is a function with a `--check` flag
(`three_levels.py --check`, `nested_bench.py --check`, `separation.py`).

## Where things are

| what | where |
|---|---|
| experiments, by number | `docs/engineering/EXPERIMENT_REGISTER.md` |
| remote jobs with bounds and measured costs | `docs/engineering/COMPUTE_LEDGER.md` |
| the queue of requests | `docs/engineering/benchmarks/BENCHMARK_REGISTRY.md` |
| failures and withdrawn claims | `docs/engineering/DEAD_ENDS.md`, `BENCHMARK_LIMITATIONS.md` |
| what to do next | `docs/engineering/RESEARCH_LOG.md`, "Resume here" |
