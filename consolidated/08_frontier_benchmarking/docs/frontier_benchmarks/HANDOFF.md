# Handoff of the Frontier Benchmarking division

*Rewritten at the consolidation of 2026-11-27 01:25 UTC.  **The division is halted by owner
directive FB-D-5: nothing below is to be started without the research owner's explicit
authorisation.**  A successor should be able to continue from this file, `RESEARCH_LOG.md`
("Resume here"), `OWNER_DIRECTIVES.md` and the consolidation report
(`docs/collaboration/consolidation/frontier-benchmarks.md`) without the conversation that
produced them.*

## 1. What this division is

The eighth division: an independent evaluator of whether MetricChain's mathematics and
software produce better scientific outcomes than contemporary methods, measured against the
same evidence.  It writes only to `research/frontier-benchmarks`, develops none of the
software it evaluates, runs no substantial computation (engineering does), and reports
negative findings with the same prominence as positive ones.

## 2. State in seven lines

1. **CASP17**: nothing in MetricChain could be evaluated; no prediction exists; MetricChain is
   not a participant (`CASP17_ASSESSMENT.md`); uncontradicted, two divisions agree.
2. **One realistic comparison, negative, with its cause**: the certified minimum-energy route
   certified 4 of 10 public instances at 300 s, 17–326 times slower than toulbar2; the cause
   is its node rate, not its bound (`RESULTS.md` §§1, 6).
3. **One independent replication**: nine planted identification controls of the ensemble
   division, all reproduced (`RESULTS.md` §2).
4. **Integrity tooling in use**: three freezes, each time-stamped by four unrelated
   authorities (`PREDICTION_FREEZE_REGISTER.md`); a sealed held-out list of 47 structures,
   unopened and unused, credentials with the research owner.
5. **Eleven protocols**, version 1.1, none frozen and executed (`ASSESSMENT_PROTOCOLS.md`).
6. **Registers**: 23 negative results; 18 deficiencies with causes and criteria
   (`IMPROVEMENT_REGISTER.md`); readiness by benchmark and role (`BENCHMARK_READINESS.md`).
7. **Nothing has been compared with experiment**, by this division or any other.

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
| consolidation report (critical assessment, next actions) | `docs/collaboration/consolidation/frontier-benchmarks.md` |
| deficiencies and what would remove them; readiness by benchmark | `IMPROVEMENT_REGISTER.md`, `BENCHMARK_READINESS.md` |
| diagnosis of the certified route: scripts, stored rows, commands | `experiments/frontier/diagnostics/` (`README.md`) |
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
`SELECTION_RULE.md` with a new salt and a new freeze identifier.  The founding session's
scratch copies disappear with its machine: **the owner's copy is the only durable one.**  The
owner has confirmed custody ("I will retain custody of the credentials and authorize their
release to Engineering separately").

## 5. Open obligations (all suspended by the halt)

| # | obligation | needs | where the rule is |
|---|---|---|---|
| 1 | compare our frozen scores with the official CASP17 numbers; record the outcome | the owner's authorisation; the official results (announced for 2026-11-29) | FRZ-0003 `COMPARISON_PLAN.md` |
| 2 | revise the state-of-the-art register from the official CASP17 assessment | the same | `STATE_OF_THE_ART.md` §G |
| 3 | reconcile the sealed list's selection rule with the software division's plan SB-BM-3 (it reports three differences; we have not compared them) before the list is opened | both divisions, the owner | FRZ-0002 `SELECTION_RULE.md`; register IR-14 |
| 4 | interpret what engineering returns for FRONTIER-REQ-0001 from the artifacts, not the summary | its response (none at the halt) | `ASSESSMENT_PROTOCOLS.md` FB-P-01, FB-P-02 |
| 5 | filter the held-out list against the training sets of learned packers before FB-P-02 compares against them | before that comparison | FRZ-0002 manifest, contamination assessment |
| 6 | confirm at the source every literature row marked "snippet" or "memory", and every benchmark fact in `BENCHMARK_READINESS.md`, before a protocol relies on it | before freezing a protocol | `STATE_OF_THE_ART.md` §G |
| 7 | amend FB-P-04 to score intervals and the bracketing pair for the identifiability radius, not verdicts | — | ENSEMBLE-RES-0008 E-2, E-3; register IR-10 |

**Scheduled activity: one task, paused.**  The founding session scheduled a message to itself
for 2026-11-30 05:00 UTC (scheduled-task id `trig_01PMtadi7NHa7nfuRtqTTkMq`) to do obligations
1 and 2 and read replies.  At the consolidation it was **paused, not deleted**, because
FB-D-5 forbids work without explicit authorisation.  To use it the owner re-authorises it
(the session can re-enable it or simply do the comparison when asked).  Nothing else is
scheduled and nothing runs in the background.

## 6. How to resume the three recommended actions without repeating work

*(Report §E has objectives, baselines and criteria.  What follows is only what exists.)*

* **Certified search at solver speed.**  Public instances: the ten `pdb*.wcsp.xz` files of the
  2011 inference challenge's "ProteinFolding" category on the INRAE mirror (checksums in the
  stored pilot rows, `experiments/frontier/exploratory_gmec/results/scp10_at_1756529.jsonl`).
  Drivers: `experiments/frontier/exploratory_gmec/run_scp_exploratory.py` (head-to-head),
  `experiments/frontier/diagnostics/` (root bounds, node counts, toulbar2 ablation).
  `pip install pytoulbar2==1.4.0.3`.  The evaluated software is read from a detached copy
  (`git archive <commit> | tar -x`), never edited.
* **Ensemble intervals on experimental data.**  Fetched and unused: the public repository
  `KULL-Centre/BME` at commit `314d3b5bb8cd400c1a9eee984acdb903a03c3da4` (its `data/` holds
  computed observables for a simulated pool and measured couplings, NOEs, RDCs and scattering;
  described from file names, not opened).  Our independent linear-programming code for finite
  linear controls: `experiments/frontier/exploratory_identification/run_controls_pilot.py`.
  The ensemble division's applicable statements: ENSEMBLE-RES-0008 §1.
* **Side-chain placement against experiment.**  Fetched and not built: the public repository
  `tommyhuangthu/FASPR` at commit `0d55732fd6307f373018c6bddd842291c355c5f7`.  Torsion scoring:
  `src/metricchain_fb/scores.py` (`chi_angles`, `chi_recovery`).  A public validation list
  must be drawn by the criteria of FRZ-0002's `SELECTION_RULE.md` with a release date *before*
  2026-07-01, so that it cannot meet the sealed pool.

## 7. Things a successor should not do

* Start any of the above, fetch, or answer a message before the owner lifts the halt.
* Call any result here validation: both pilots and the diagnosis are class A-EXP on
  development instances.
* Report a CASP17 ranking before an official page states it, or present anything as a CASP
  result.
* Use the ten public side-chain instances as held-out evidence: they are development
  instances.
* Open the sealed list, ask another division for its credentials, or use it for anything but
  one run of a frozen protocol on a frozen release.  If it is ever used to guide development,
  retire it and draw a new one under a new freeze identifier (owner directive FB-D-3).
* Run the design-type instances of the public benchmark category, in any wording; request a
  mutation-effect capability without the owner's decision (`BENCHMARK_READINESS.md` §3).
* Edit a frozen directory (the test suite fails if anyone does) or upgrade an assessment
  class after the fact.
* Launch Modal jobs, raise a spending limit, open a pull request, merge, force-push, or submit
  anything to an external assessment.

## 8. Verification of this checkpoint

    python -m venv ~/.venvs/frontier && ~/.venvs/frontier/bin/pip install -r requirements-frontier.txt
    PYTHONPATH=src ~/.venvs/frontier/bin/python -m pytest tests/frontier -q          # 62 pass offline, 2 skipped (live time-stamping)
    PYTHONPATH=src ~/.venvs/frontier/bin/python -m metricchain_fb.freeze verify experiments/frontier/freezes
    PYTHONPATH=src ~/.venvs/frontier/bin/python experiments/frontier/make_tables.py --verify docs/frontier_benchmarks/RESULTS.md

The computational hard stop is 2026-11-30 15:00 US Eastern; this division has no remote
computation of its own to stop.
