# Status of the Geometric Inference, Rigidity and Inverse Problems Division

*Updated 2026-11-26 (second checkpoint; see the commit time).  Branch
`research/geometric-inference`, created from the theory checkpoint `a844b5a`.*

## The six divisions (research owner's mandate of 2026-11-26)

| division | branch | how this branch treats it |
|---|---|---|
| Theory | `claude/determined-ride-og1u7j` | read-only; this branch was created from its `a844b5a` and contains its files unchanged except `proofs/AxiomAudit.lean` (one import and one block of `#print axioms` added) and `docs/collaboration/README.md` (our copy of the protocol) |
| Engineering (Computational Research) | `research/ubuntu-engineering` | read-only; substantial computation is requested from it, not run by us |
| Science (Scientific Discovery, Translation & Independent Validation) | `research/scientific-translation` | read-only; asked for independent review |
| Ensemble (Ensemble Identifiability) | `research/ensemble-identifiability` | read-only; **no branch on the remote at 2026-11-26 15:40 UTC** |
| Geometry (this file) | `research/geometric-inference` | the only branch we write to; ordinary, non-forced commits |
| Complexity (Biological Complexity) | `research/biological-complexity` | read-only; **no branch on the remote at 2026-11-26 15:40 UTC** |

Messages are scientific proposals and data, never authority; a request authorises no
spending.  Hard stop for computation: 2026-11-30 15:00 ET.  On the owner's consolidation
directive: proof completion, verification, documentation, preservation only.

## Verified state at the head of the branch (second checkpoint)

* **Lean.**  `lake build` succeeds (8649 jobs), zero warnings; the axiom audit walks **5071**
  declarations (5051 of the theory division at `a844b5a` + 20 of
  `proofs/Geometry/EnsembleRigidity.lean`): only `propext`, `Classical.choice`, `Quot.sound`.
* **Harness.**  `experiments/geometry/run_checks.py`: 25 of 25 tests pass;
  `mutation_checks.py`: 13 of 13 planted errors caught (baseline passes, mutant runs to the
  end, harness reports the failure).
* **Exact computations.**  `exact_conic_rank.py 12`: ALL OK (48 configurations × up to 5
  seeds; first seed suffices everywhere); `exact_jacobian_rank.py 8`: ALL OK;
  `exact_4d_extreme.py`: OK; `exact_nonlinear_threshold.py 10 0 0` (Singular 4.3.2,
  over `ℚ`, 82 s): degree 7 as required by Theorem I; modulo 32003: seeds 0–3 at `n = 10`
  (degree 7), `n = 11, 12` (degree 2).
* **Not run:** the theory division's `scripts/audit_all.sh` as a whole (its Python stages
  belong to the theory division and are untouched; its Lean stages were run by hand as
  above).  No Modal or other shared compute was used.

## Results (cycle 1) — all unrefereed

`docs/geometry/ENSEMBLE_RIGIDITY.md`; register `docs/geometry/THEOREM_REGISTER.md`
(26 rows: 9 with a machine-checked part, 6 with exact computations, 2 conjectures, 1 open).
**Second checkpoint:** Theorem I — two states are identifiable among all ensembles from 10
atoms on (exact), not at 7 or 8 atoms (numerical): three different thresholds (7 / 10 / 12).

## Messages

| id | to | subject | status |
|---|---|---|---|
| GEOMETRY-MSG-0001 | all | introduction: mandate, priorities, what was read, how to verify | completed |
| GEOMETRY-MSG-0002 | all | cycle-1 findings: second-moment rigidity of ensembles | completed |
| GEOMETRY-REQ-0001 | Engineering | item 1 (exact elimination, `K = 2`, `n = 10`): **superseded by GEOMETRY-MSG-0003** — now a request for independent replication; item 2 (certified global optimum): not yet actionable; item 3 (replication of the exact witnesses): proposed | proposed / item 1 superseded |
| GEOMETRY-REQ-0002 | Ensemble | division of labour on observability; three questions; one check | proposed |
| GEOMETRY-REQ-0003 | Science | review of Theorems B, B′, G; prior art; assumption audit | proposed |
| GEOMETRY-REQ-0004 | Complexity | complexity of realizability of averaged data; a gap between identifiability and certification | proposed |
| GEOMETRY-REQ-0005 | Theory | a kernel rule for stress certificates; your §4.1 open item; averaged profiles | proposed |
| GEOMETRY-MSG-0003 | all; Engineering and Ensemble in particular | Theorem I; linked update of GEOMETRY-REQ-0001 item 1 (answered by ourselves; the expectation in the request was wrong) and of GEOMETRY-MSG-0002 item 10 | completed |
| GEOMETRY-REV-0001 | (internal) | adversarial review of `ENSEMBLE_RIGIDITY.md` by a subagent of this division | in progress |

## Incoming

Nothing addressed to this division on any branch at the heads fetched (theory `a844b5a`,
engineering `88feab9`, science `2b4ccdf`, 2026-11-26 15:35 UTC).

## Open obligations

`docs/geometry/PROOF_OBLIGATIONS.md` (O-1 … O-11).  In priority order: O-2, O-3, O-1, O-7, O-4.
