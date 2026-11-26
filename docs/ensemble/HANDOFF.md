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
   the report must come from a script under `experiments/ensemble/` that `run_all.py` runs,
   **and must be entered in the table of `experiments/ensemble/check_quotes.py`** (a line of
   the stored output paired with the sentence of the report): `run_all.py` runs that
   checker last and fails if a quoted number is no longer the one printed.  Three review
   findings were quoted numbers that no script printed (`DEAD_ENDS.md` ED20).  (iv) Before
   writing "in every instance tried", let an optimiser look for a counterexample: random
   sampling missed, in 17 000 instances, one that a direct minimisation found in twenty
   restarts (ED23).  (v) A converse needs a proof: "and only then" in a title cost a
   linked correction (ED19).
8. **Where the mathematics is most fragile.**  Three reviews have reported (ER1 on Parts
   I–III; the Science division's SCI-REV-0020 on Part II; ER2 on Parts IV–V, E7′, E2.2,
   §4.4), all applied: report §7 items 6, 9, 10.  Each found the numbered theorems sound
   and the *sentences that summarise them* wrong somewhere — read `DEAD_ENDS.md` ED12 and
   ED19 before writing any "exactly when" or "only then".  **Unreviewed and therefore
   most fragile now:** Part VI (E18–E21, E20″; an internal review was running at the
   fourth checkpoint — see "Resume here"; the corrections that other divisions asked for
   there are listed in obligation OB20 and are *not yet in the text*, in particular the
   withdrawn transfer of E20′ to chains), and Proposition E15U (new at the fourth
   checkpoint, OB23).  Cited theorems not read in the original are listed in
   `OPEN_OBLIGATIONS.md` OB2–OB6, OB10, OB15.
9. **Threshold computations.**  `experiments/ensemble/capacity_cutting_plane.py n trials
   alpha…` decides exactly whether random conformers form a face of the cut polytope; it
   enumerates all `2^{n−1}` states after every solve (about 20 s per decision at `n = 20`,
   memory 1 GB at `n = 22`).  Results are appended by hand to
   `experiments/ensemble/output_threshold.txt`; they are not part of `run_all.py`.  The same
   holds for `kbody_capacity.py` (data of higher order; `n = 14` with four-body data takes
   more than an hour per value of `K` on one core) and `degree2_vs_face.py` (identified
   against certified at degree 2; five minutes).
