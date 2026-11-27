# Handoff of the Frontier Benchmarking division

*Written at the end of the founding session, 2026-11-27 (UTC).  A successor should be able to
continue from this file, `RESEARCH_LOG.md` ("Resume here") and `OWNER_DIRECTIVES.md` without
the conversation that produced them.*

## 1. What this division is

The eighth division: an independent evaluator of whether MetricChain's mathematics and
software produce better scientific outcomes than contemporary methods, measured against the
same evidence.  It writes only to `research/frontier-benchmarks`, develops none of the
software it evaluates, runs no substantial computation (engineering does), and reports
negative findings with the same prominence as positive ones.

## 2. State in five lines

1. **CASP17**: nothing in MetricChain could be evaluated before the results of 2026-11-29; no
   prediction exists; MetricChain is not a participant (`CASP17_ASSESSMENT.md`).
2. **Integrity tooling works and is in use**: three freezes, each time-stamped by four
   unrelated authorities (`PREDICTION_FREEZE_REGISTER.md`).
3. **A sealed held-out list exists** (47 structures) for the software division's first
   held-out evaluation; the key is with the research owner.
4. **Two exploratory pilots** are the programme's first runs on instances its authors did not
   build and with comparators from outside (`RESULTS.md`); neither is validation.
5. **Eleven protocols** say, before any run, what would count as success and failure
   (`ASSESSMENT_PROTOCOLS.md`); three requests are out (engineering, science).

## 3. Where everything is

| what | where |
|---|---|
| owner's directives to this division | `OWNER_DIRECTIVES.md` |
| protocol copy, labels (assessment classes, stages, dimensions) | `docs/collaboration/README.md` (addendum) |
| what was sent, state, commits read | `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md`, `status/frontier-benchmarks.md`, `FRONTIER_UPSTREAM_SYNC.md` |
| messages and requests | `docs/collaboration/messages|requests/frontier-benchmarks/` |
| the fourteen research documents | this directory |
| intake and literature reports, as delivered | `intake/`, `literature/` |
| tools | `src/metricchain_fb/` (`freeze`, `timestamp`, `commitment`, `scores`); tests `tests/frontier/` |
| freezes | `experiments/frontier/freezes/` |
| pilot drivers and stored results; table generator | `experiments/frontier/exploratory_gmec/`, `exploratory_identification/`, `casp17_scoring_check/`, `make_tables.py` |

Environment used (not in the repository): Python 3.13.18 virtual environment from
`requirements-frontier.txt` plus `pytoulbar2` 1.4.0.3; `openssl` 3.0.13; `curl`.  Raw
downloads (CASP17 pages and archives, PDB files, the public instances) were kept outside the
tree and are reproducible from the URLs and checksums in `DATA_PROVENANCE.md` and the freeze
manifests.  **The session machine is ephemeral: nothing outside the repository survives.**

## 4. Custody (the one thing that is deliberately not in the repository)

The passphrase of `experiments/frontier/freezes/FRONTIER-FRZ-0002_heldout_commitment_v1/sealed_list_v1.enc`
and the salt of its commitment were delivered to the **research owner** in the final message
of the founding session.  A successor session does not have them and must not ask another
division for them.  If they are lost, the list is redrawn by the rule in that freeze's
`SELECTION_RULE.md` with a new salt and a new freeze identifier.

## 5. Open obligations

| # | obligation | trigger | where the rule is |
|---|---|---|---|
| 1 | compare our frozen scores with the official CASP17 numbers; record the outcome | official results (announced for 2026-11-29) | FRZ-0003 `COMPARISON_PLAN.md` |
| 2 | revise the state-of-the-art register from the official CASP17 assessment | the same, and later the assessors' papers | `STATE_OF_THE_ART.md` §G |
| 3 | read replies; correct anything of ours that is wrong, by linked message | every synchronisation | protocol |
| 4 | interpret what engineering returns for FRONTIER-REQ-0001 from the artifacts | its response | `ASSESSMENT_PROTOCOLS.md` FB-P-01, FB-P-02 |
| 5 | filter the held-out list against the training sets of learned packers before FB-P-02 compares against them | before that comparison | FRZ-0002 manifest, contamination assessment |
| 6 | confirm at the source every literature row marked "snippet" or "memory" before a protocol relies on it | before freezing a protocol | `STATE_OF_THE_ART.md` §G |

**A scheduled check-in exists.**  The founding session scheduled one message to itself for
2026-11-30 05:00 UTC (scheduled-task id `trig_01PMtadi7NHa7nfuRtqTTkMq`) to do obligations 1–3
once and stop.  It is the only scheduled activity of this division; the research owner was
told and can cancel it.  Nothing else runs in the background: between sessions this division
does no work.

## 6. Things a successor should not do

* Call any result here validation: both pilots are class A-EXP on development instances.
* Report a CASP17 ranking before an official page states it, or present anything as a CASP
  result.
* Use the ten public side-chain instances as held-out evidence: they are development
  instances now.
* Run the design-type instances of the public benchmark category, in any wording.
* Edit a frozen directory (the test-suite fails if anyone does) or upgrade an assessment
  class after the fact.
* Launch Modal jobs, raise a spending limit, open a pull request, merge, force-push, or submit
  anything to an external assessment.

## 7. Consolidation

When the research owner's consolidation directive arrives: no new protocol; finish obligation
1 and 2 if the results are out; verify the freezes
(`python -m metricchain_fb.freeze verify experiments/frontier/freezes`); run the tests; bring
`RESULTS.md`, `NEGATIVE_RESULTS.md`, `SCIENTIFIC_SYNTHESIS.md`, the status file and this
handoff up to date; push.  The computational hard stop is 2026-11-30 15:00 US Eastern; this
division has no remote computation of its own to stop.
