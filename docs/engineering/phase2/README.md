# Phase II of the Computational Research Division — index

Branch `research/phase2-certified-inference`, created from `research/ubuntu-engineering` at `67b6bc2` on
2026-11-28 under the research owner's directive D-11 (`../DIRECTIVES.md`).  Baseline for everything
taken from other divisions: the consolidated archive at `fe9f58c1f0bfe5de8c6434c3490a33cd1d94023f`.
**The phase was completed on 2026-11-28** (D-11: "Stop at completion or the resource ceiling.  Do not
automatically resume."); start with `FINAL_REPORT.md`.  **Since the owner's directive D-12 of the same day**
(a fourth division on multistate free-energy estimation; "Continue your existing bounded research cycles")
the division works in bounded cycles on that collaboration only: `MBAR_INTEGRATION.md`.

| file | what |
|---|---|
| `FINAL_REPORT.md` | the seven deliverables of D-11: results, artifacts, evidence, capabilities, negative results, resources, recommendation |
| `CERTIFIED_INFERENCE.md` | the mathematics, second version: S3 re-derived with its hidden assumptions; improved and replacing statements; the lower bound and what escapes it; bounded-influence classes; relation to the archive and to the literature; §13: what changed after the review |
| `REVIEW_A.md` | independent adversarial review of the first version of that note and of the library, by a subagent (three critical, eight major findings) |
| `PROTOCOL.md` | validation protocol with hypotheses, committed before any run; its last section records the deviations |
| `RESULTS.md` | outcomes of the hypotheses (seven hold, six refuted), the comparative tables, the supplementary experiments |
| `MBAR_INTEGRATION.md` | addendum under D-12: compositions with multistate free-energy estimation — uncertainty of the free energies as an envelope (Theorem M1), an energy error shared by two states (Proposition M2), which sampling laws need free energies (Proposition M3), the seven sources of uncertainty, evidence, limits |
| `VERIFICATION_GAPS.md` | Workstream C: the later structural-biology certificates, the old floating-point exploit and its repair, the memoised kernel, referee R29's concerns, certified computation against evaluated formulas |
| `../../collaboration/messages/engineering/ENG-MSG-0009.md`, `ENG-MSG-0010.md` | opening message to the other two Phase II divisions; its correction after the review, with replies |
| `../../collaboration/responses/engineering/ENG-RES-0020.md` | answer to the adaptive-hierarchy division's request for an independent replication |
| `../../collaboration/messages/engineering/ENG-MSG-0011.md` | to the certified-MBAR division (and for the record of the other two): what composes, what we measured, what we would need |

Software: `src/metricchain_eng/certinf/` (`core.py`, `certify.py`, `metric.py`, and since D-12
`multistate.py`); tests `tests/eng/test_certinf.py` (20), `tests/eng/test_certinf_review.py` (12, one per
finding of the review that concerns the library, and Theorem 5.4) and `tests/eng/test_certinf_multistate.py`
(14):

    source "$HOME/.venvs/metricchain/bin/activate"
    python -m pytest tests/eng/test_certinf.py tests/eng/test_certinf_review.py tests/eng/test_certinf_multistate.py -q

Experiments, each with its scripts and stored outputs:

| directory under `experiments/eng/` | what |
|---|---|
| `certinf/` | the validation campaign under `PROTOCOL.md` (`REPORT.md`: full tables) |
| `phase2_coord_checks/` | the coordinator's own checks of the campaign |
| `phase2_tilt/` | supplementary S1: draws from the extremal ensemble against reference draws |
| `phase2_nonproduct/` | supplementary S2: the outer bound for references that are not products |
| `phase2_seq/` | the sequential bound against the exact programme |
| `phase2_review/` | the referee's scripts and outputs |
| `phase2_gaps/` | Workstream C |
| `phase2_digest/` | digest of the archive; prior art on the web |
| `phase2_hie_req/` | the replication for HIE-REQ-0001 |
| `phase2_mbar/` | D-12: Theorem M1 on enumerable models (`PREDICTIONS.md` written before the runs), the shared energy error, the tail-event diagnostic |

## Subagents used in this phase

D-11: "Use subagents selectively for independent verification or well-defined research tasks.  Do not
launch a new wave of broadly exploratory agents."  Six were used, each with one written deliverable in
its own directory and no authority to commit, to run remote jobs or to touch another division's branch.
What a subagent reports is not a result of this division until the coordinator has checked it; the
column says what was checked.  (The harness does not let a subagent write a report file; three of the six
returned their report as text or as the output of their own script, and the coordinator saved it.)

| purpose | deliverable | checked by the coordinator |
|---|---|---|
| digest of what the archive already contains for S3; referee R29's concerns; kinds of engineering results | `experiments/eng/phase2_digest/DIGEST.md` | the items the note relies on were read in the archive itself: science item 89(d) and its corrections, theory Proposition 11.113 and Theorem 11.105 as quoted, the definition of the class `L_u`, the constants of workstream Z in the theory tree; the rest is the subagent's reading |
| prior art on the web | `experiments/eng/phase2_digest/PRIOR_ART_WEB.md` | nothing was re-searched; the subagent read abstracts and index records only and says so entry by entry; no reference was read in full by anyone |
| verification of structural-biology certificates, exploit and repair, memoised kernel | `experiments/eng/phase2_gaps/REPORT.md` | four certificate checks and the exploit's reproducer repeated; see `VERIFICATION_GAPS.md` |
| validation campaign under `PROTOCOL.md` | `experiments/eng/certinf/REPORT.md` | its code read against the protocol; the verdict numbers of five hypotheses recomputed from the raw rows with separate code (one count corrected); the exact reference on the ellipsoid family verified independently; see `RESULTS.md` §1 |
| adversarial review of the mathematical note and of the code's soundness | `REVIEW_A.md` | every finding answered (`CERTIFIED_INFERENCE.md` §13); the counterexample to Proposition 9.6 reproduced with the library; the others accepted on the referee's computations and kept as tests where they concern code |
| independent replication for the adaptive-hierarchy division (HIE-REQ-0001, Q1 and Q2) | `experiments/eng/phase2_hie_req/REPORT.md` | two cross-check scripts re-run (outputs reproduced line for line); summary lines read; the mathematics of the other division not read; see ENG-RES-0020 §2 |

## Resources

Claude: ceiling $500 for this phase, read as the increase of the account's usage counter (account-wide:
an upper bound for this division).  Modal: ceiling $25; **nothing launched** — everything in this
phase ran locally.  Figures: `FINAL_REPORT.md` §6, `../COMPUTE_LEDGER.md`.
