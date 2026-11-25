# Workstream U — scripts and outputs

Scripts and outputs of workstream U (rounds of adaptivity on the cube class), as delivered;
the report is `docs/workstreams/U_REPORT.md` (§9 lists every command with sizes, run times and
outputs), the integrated statements are theory report §11.24.  They are **not** part of the
audit (`scripts/audit_all.sh`); they are kept so that the numerical statements can be re-run.
The coordinator's independent re-computation is in `experiments/coordinator_checks/rounds_U/`.

Layout: `code/` (Python: numpy, scipy), `out/` (stored outputs).  Run from `code/` as
`ulimit -v 4000000; python3 <script> <args>`; the scripts write to standard output (the stored
outputs were produced by redirecting it to `../out/<name>.txt`).
