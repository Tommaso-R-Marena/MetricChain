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
   research/biological-complexity research/structural-biology`, and separately
   `research/frontier-benchmarks` (the eighth division; fetch it on its own so that its
   absence does not abort the others), read the other divisions'
   digests and status files, record what was read in
   `docs/collaboration/status/ensemble.md`.
3b. **Standing instructions of the second supplementary directive (2026-11-26, about 22:40
   UTC): an eighth division,** Frontier Benchmarking, Experimental Evidence and Scientific
   Evaluation (branch `research/frontier-benchmarks`, digest
   `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md`; founded at 22:54 UTC, nothing sent
   yet at 23:07 UTC).
   Read its findings at every synchronisation; answer its questions within our
   responsibilities; when an evaluation exposes a mathematical limitation, look for a
   stronger theorem, a constructive algorithm, a generalisation or a rigorous obstruction;
   **do not duplicate its evaluation mandate** (we propose mathematical controls with
   ground truth; it designs evaluations and guards their integrity); substantial
   computation stays with the engineering division; keep blind, pre-leaderboard and
   retrospective evaluation strictly apart and never use held-out reference data in
   developing anything (the official CASP17 results are due on 2026-11-29; this division
   makes no predictions and has no part in that).  Our protocol copy lists all eight
   divisions (`docs/collaboration/README.md`, third addendum).
3a. **Standing instructions of the research owner's supplementary directive (2026-11-26).**
   Keep doing fundamental mathematics; in addition (i) give results constructive forms —
   what an algorithm must establish, whether certificates are efficiently computable,
   whether checking is easier than constructing; (ii) widen the observation models
   (noise, incompleteness, imperfect or nonlinear observation functions, unknown ensemble
   complexity); (iii) pursue partial identification and impossibility results; (iv) tell
   the Structural Biology division exactly what is implementable (`SOFTWARE_INTERFACE.md`,
   readiness levels R3–R0) and never present an unreviewed statement as an implementable
   guarantee; (v) propose synthetic controls (`BENCHMARK_CONTROLS.md`) — execution and
   substantial computation go to the engineering division, no harness of our own; (vi)
   read `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md` at every synchronisation and
   answer its obstacles with a more general theorem, an effective certificate, or a
   precise impossibility statement.
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
8. **Where the mathematics is most fragile.**  Every Part has had one review (ER1 on Parts
   I–III; the Science division's SCI-REV-0020 on Part II; ER2 on Parts IV–V, E7′, E2.2,
   §4.4; ER3 on Part VI), all applied: report §7 items 6, 9, 10, 14.  Each found the
   numbered theorems sound and the *sentences that summarise or extend them* wrong
   somewhere — read `DEAD_ENDS.md` ED12, ED19, ED24 before writing any "exactly when",
   "only then", or any count of conditions.  **Unreviewed and therefore most fragile
   now:** Proposition E15U beyond its main statement (which the Science division
   re-derived and replicated), Proposition E17.1, and the statements taken into Part VI
   from the review ER3 (E20a, E22, two constants of E20″) — obligations OB23, OB25, OB26;
   **and the whole of Part VII** (E23–E26, data that are not linear in the ensemble:
   written after the fifth checkpoint, read by nobody but its author — OB27; its
   software cards N1–N3 are at readiness R1 for that reason); **and Theorem E20b with
   Propositions E20c, E20d** (the torus of three angles: OB28 lists the six points a
   reviewer should attack first).  Exact computer algebra (sympy rationals; ranks modulo
   a prime) is not a kernel check: do not label such a step [V].
   Cited theorems not read in the original by us: `OPEN_OBLIGATIONS.md` OB2–OB6, OB10,
   OB15, OB16 (Kahle's theorem and Johnston–Lovitz–Vijayaraghavan among them).  On
   continuous spaces never test non-identification on a product grid (ED24).
9. **Threshold computations.**  `experiments/ensemble/capacity_cutting_plane.py n trials
   alpha…` decides exactly whether random conformers form a face of the cut polytope; it
   enumerates all `2^{n−1}` states after every solve (about 20 s per decision at `n = 20`,
   memory 1 GB at `n = 22`).  Results are appended by hand to
   `experiments/ensemble/output_threshold.txt`; they are not part of `run_all.py`.  The same
   holds for `kbody_capacity.py` (data of higher order; `n = 14` with four-body data takes
   more than an hour per value of `K` on one core) and `degree2_vs_face.py` (identified
   against certified at degree 2; five minutes).
