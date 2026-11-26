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
7. **Conventions that are easy to break.**  (i) `scripts/audit_all.sh` scans `proofs/` for
   forbidden tokens: do not write the words for an incomplete proof, the tactic that gives
   up a goal, or an anonymous example, even in comments; every module must be imported by
   `proofs/AxiomAudit.lean`, with `#print axioms` lines for its headline theorems and named
   non-vacuity witnesses; the build must be free of warnings (unused section variables
   need `omit … in`, unused `simp` arguments must be removed, `push_neg` is deprecated in
   this Mathlib — use `push Not`).  (ii) A single Lean file is checked with
   `lake env lean proofs/Ensemble/<File>.lean` after `lake build` of its imports; the full
   build of the branch takes tens of minutes on four cores.  (iii) Every number quoted in
   the report must come from a script under `experiments/ensemble/` that `run_all.py` runs.
8. **Where the mathematics is most fragile.**  Parts I–III have had one internal
   adversarial review (`reviews/ER1_internal_review.md`, applied: report §7 item 6); it
   found the theorems sound and the *sentences that summarise them* wrong in five places —
   read `DEAD_ENDS.md` ED12 before writing any "exactly when".  Unreviewed and therefore
   most fragile now: Part IV (the thermal union bound and its FKG extension, E15/E15T),
   Part V (E17), Theorem E7′ (two quantifier/edge-case errors were already found in
   passing), and §4.4 (numerics only).  Cited theorems not read in the original are listed
   in `OPEN_OBLIGATIONS.md` OB2–OB6.
9. **Threshold computations.**  `experiments/ensemble/capacity_cutting_plane.py n trials
   alpha…` decides exactly whether random conformers form a face of the cut polytope; it
   enumerates all `2^{n−1}` states after every solve (about 20 s per decision at `n = 20`,
   memory 1 GB at `n = 22`).  Results are appended by hand to
   `experiments/ensemble/output_threshold.txt`; they are not part of `run_all.py`.
