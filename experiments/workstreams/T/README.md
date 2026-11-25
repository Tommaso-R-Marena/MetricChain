# Workstream T — scripts and outputs

Scripts and outputs of workstream T (known parts that are functions of the type: mean-field
models with one phase or two), as delivered; the report is `docs/workstreams/T_REPORT.md`
(§13 lists every command with sizes, run times and outputs), the integrated statements are
theory report §11.23.  They are **not** part of the audit (`scripts/audit_all.sh`); they are
kept so that the numerical statements can be re-run.  The coordinator's independent
re-computation is in `experiments/coordinator_checks/meanfield_T/`.

Layout: `code/` (Python: numpy, scipy; `tlib.py`, `tfin.py`, `kfin.py` are libraries, `t01` … `t19`
the experiments, `queue*.sh` the sequences in which they were run), `out/` (stored outputs).
Run from `code/` as `ulimit -v 4000000; python3 <script> <args>`; the scripts write to
standard output, and the stored outputs were produced by redirecting it to `../out/<name>.txt`
(the queue scripts do this with relative paths).
