# Handoff — Ensemble division

*For a successor who has to continue without the context of the session that wrote this.*

1. **Where everything is.**  `docs/ensemble/README.md` (layout).  The mathematics is in
   `ENSEMBLE_REPORT.md`; the state of every statement in `THEOREM_REGISTER.md`; what is owed
   in `OPEN_OBLIGATIONS.md`; the log in `RESEARCH_LOG.md` ("Resume here").
2. **Branch discipline.**  Write only to `research/ensemble-identifiability`.  Never merge,
   never force-push, never touch another division's branch, no pull requests without the
   research owner's explicit authorisation.
3. **Synchronise first.**  `git fetch origin claude/determined-ride-og1u7j
   research/ubuntu-engineering research/scientific-translation research/geometric-inference
   research/biological-complexity` (the last two may not exist yet), read the other
   divisions' digests and status files, record what was read in
   `docs/collaboration/status/ensemble.md`.
4. **Tooling in a fresh container.**  Lean: `curl -sSfL
   https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y
   --default-toolchain none`, then `elan toolchain install leanprover/lean4:v4.31.0`,
   `lake exe cache get` (about ten minutes), `lake build`.  Python: `pip install numpy
   scipy mpmath sympy networkx`.
5. **Deadlines and limits (research owner).**  Expensive computation ends 2026-11-30 15:00
   Eastern Time.  Shared Modal budget is coordinated by the engineering division; do not
   start significant shared-budget workloads without the owner's authorisation.  When the
   owner issues the consolidation directive (about $2,000 of credit left across sessions):
   stop exploring; close proofs, verify, integrate, document, preserve.
6. **State.**  See "Resume here" in `RESEARCH_LOG.md`.
