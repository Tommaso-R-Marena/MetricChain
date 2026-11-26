# Mathematical Biology and Computational Complexity Division (complexity)

Branch: `research/biological-complexity` (writes only here; created 2026-11-26 from the theory
checkpoint `a844b5a8f374ba8170b29d7ebba461edde1ef155`).  The files inherited from that checkpoint
(`README.md`, `docs/THEORY_REPORT.md`, `proofs/`, …) are the Theoretical Research Division's and are
**not edited here**; their authoritative versions live on `claude/determined-ride-og1u7j`.

Mandate (research owner, 2026-11-26): resolve genuinely open, explicitly documented mathematical
problems in theoretical computational biology, mathematical biophysics, combinatorics, statistical
mechanics and related theoretical computer science — proofs, disproofs, complexity
classifications, algorithms.  Scope: abstract combinatorial models, mathematical reductions and
synthetic instances only.  No biological sequence design, no target-specific optimisation, no
experimental execution.

## Files of this division

| file | content |
|---|---|
| [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) | register of candidate open problems: exact statement, source, verified status, our position |
| [`THEOREMS.md`](THEOREMS.md) | register of our statements with epistemic labels and proof locations |
| [`PRIOR_ART.md`](PRIOR_ART.md) | every source consulted and **how** it was inspected |
| [`DEAD_ENDS.md`](DEAD_ENDS.md) | approaches and claims that failed, were refuted, or turned out known |
| [`RESEARCH_LOG.md`](RESEARCH_LOG.md) | chronological log; ends with "Resume here" |
| [`HANDOFF.md`](HANDOFF.md) | state for whoever continues this work |
| [`ASSUMPTION_AUDIT.md`](ASSUMPTION_AUDIT.md) | every hypothesis of every registered theorem: essential, quantitative, proof artefact, convenience, complexity-changing or unknown — with the evidence |
| `NANUQ_LOCAL_CRITERION.md`, `STRANDS_NN_HARDNESS.md`, `STRANDS_ALGORITHM.md`, `ISING_GROUND_SETS.md`, `PENALTY_THRESHOLD.md` | working papers per problem (the last two answer questions of other divisions) |
| `../../experiments/complexity/` | exact enumeration and verification code (Python, integer/rational arithmetic unless stated) |
| `../../experiments/complexity/lean/` | Lean 4 files of this division, checked file by file (none may contain `sorry`, `admit`, new axioms, native evaluation); `../../experiments/complexity/reviews/` holds the referees' independent code |
| `../collaboration/…/complexity/`, `../collaboration/status/complexity.md`, `../collaboration/COMPLEXITY_TO_ALL.md` | messages (COMPLEXITY-MSG/REQ/RES/REV-nnnn), status, digest |

## Epistemic labels (the repository's, unchanged)

**[V]** machine-checked in Lean 4 (declaration named; only `propext`, `Classical.choice`, `Quot.sound`) ·
**[P]** paper proof (says whether independently reviewed; internal AI review is *not* academic peer review) ·
**[K]** known result, cited (PRIOR_ART.md says how the source was read) ·
**[N]** numerical / exhaustive-computation evidence (program named; "exhaustive up to n = …" is still [N]
for the general statement) · **[C]** conjecture.

Additional label borrowed from the Computational Research Division for finite statements:
**[X]** exact computation (exhaustive enumeration with integer/rational arithmetic; program and inputs named).

## Rules we hold ourselves to

* A problem is not "solved" by changing its assumptions; partial results are called partial.
* A failure to find prior art does not establish originality; every novelty statement names the searches made.
* A claimed counterexample must be an explicit, independently reproducible object with a checker.
* Every row of `THEOREMS.md` says whether the statement has been reviewed and by which
  `COMPLEXITY-REV-nnnn` (or another division's review); a [P] statement without one is marked
  **unreviewed**, and text written after a review is marked as such.  (The first version of this rule
  promised a review before registration; in practice statements were registered first, flagged
  "unreviewed", and reviewed afterwards.)  Before [V], the check command and the axiom audit are recorded.
