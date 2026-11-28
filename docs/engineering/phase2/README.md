# Phase II of the Computational Research Division — index

Branch `research/phase2-certified-inference`, created from `research/ubuntu-engineering` at `67b6bc2` on
2026-11-28 under the research owner's directive D-11 (`../DIRECTIVES.md`).  Baseline for everything
taken from other divisions: the consolidated archive at `fe9f58c1f0bfe5de8c6434c3490a33cd1d94023f`.

| file | what |
|---|---|
| `CERTIFIED_INFERENCE.md` | the mathematics: S3 re-derived, its hidden assumptions, improved and replacing statements, lower bound, bounded-influence classes, relation to the archive and to the literature |
| `REVIEW_A.md` | independent adversarial review of that note by a subagent |
| `PROTOCOL.md` | validation protocol with hypotheses, committed before any run |
| `RESULTS.md` | outcomes of the hypotheses and the comparative tables (from `experiments/eng/certinf/`) |
| `VERIFICATION_GAPS.md` | Workstream C: the later structural-biology certificates, the old floating-point exploit and its repair, the memoised kernel, referee R29's concerns, certified computation against evaluated formulas |
| `FINAL_REPORT.md` | the seven deliverables of D-11 |
| `../../collaboration/messages/engineering/ENG-MSG-0009.md` | opening message to the other two Phase II divisions |

Software: `src/metricchain_eng/certinf/` (`core.py`, `certify.py`, `metric.py`), tests
`tests/eng/test_certinf.py`.  Experiments: `experiments/eng/certinf/` (validation),
`experiments/eng/phase2_gaps/` (Workstream C), `experiments/eng/phase2_review/` (the referee's scripts),
`experiments/eng/phase2_digest/` (digests).

## Subagents used in this phase

D-11: "Use subagents selectively for independent verification or well-defined research tasks.  Do not
launch a new wave of broadly exploratory agents."  Five were used, each with one written deliverable in
its own directory and no authority to commit, to run remote jobs or to touch another division's branch.
What a subagent reports is not a result of this division until the coordinator has checked it; the
column says what was checked.

| purpose | deliverable | checked by the coordinator |
|---|---|---|
| digest of what the archive already contains for S3; referee R29's concerns; kinds of engineering results | `experiments/eng/phase2_digest/DIGEST.md` | the items the note relies on were read in the archive itself: science item 89(d) and its corrections, theory Proposition 11.113 and Theorem 11.105 as quoted, the definition of the class `L_u`, the constants of workstream Z in the theory tree; the rest is the subagent's reading |
| prior art on the web | `experiments/eng/phase2_digest/PRIOR_ART_WEB.md` | nothing was re-searched; the subagent read abstracts and index records only and says so entry by entry; no reference was read in full by anyone |
| verification of structural-biology certificates, exploit and repair, memoised kernel | `experiments/eng/phase2_gaps/REPORT.md` | see `VERIFICATION_GAPS.md` |
| validation campaign under `PROTOCOL.md` | `experiments/eng/certinf/REPORT.md` | see `RESULTS.md` |
| adversarial review of the mathematical note and of the code's soundness | `REVIEW_A.md` | every finding answered in the note or in `RESULTS.md` |

## Resources

Claude: ceiling $500 for this phase, read as the increase of the account's extra-usage counter (account
wide: an upper bound for this division).  Modal: ceiling $25; nothing launched — everything in this
phase ran locally.  Figures at the end of the phase: `FINAL_REPORT.md`, `../COMPUTE_LEDGER.md`.
