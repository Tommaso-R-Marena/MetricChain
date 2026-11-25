# Workstream W — scripts and outputs

Scripts and outputs of workstream W (the heteropolymer product landscape: several site types,
larger alphabets, general single-site known parts and site envelopes), as delivered; the report
is `docs/workstreams/W_REPORT.md` (§12 lists every command with sizes, run times and outputs),
the integrated statements are theory report §11.26.  They are **not** part of the audit
(`scripts/audit_all.sh`); they are kept so that the numerical statements can be re-run.  The
coordinator's independent re-computation is in `experiments/coordinator_checks/sites_W/`.

Layout: `code/` (Python: numpy, scipy), `out/` (stored outputs).  Run from `code/` as
`ulimit -v 4000000; timeout 590 python3 <script> <args>`, one at a time; the scripts write to
standard output (the stored outputs were produced by redirecting it to `../out/<name>.txt`).
