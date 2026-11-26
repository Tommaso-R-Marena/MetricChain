# Status of the Geometric Inference, Rigidity and Inverse Problems Division

*Updated 2026-11-26 (third checkpoint; see the commit time).  Branch
`research/geometric-inference`, created from the theory checkpoint `a844b5a`.*

## The six divisions (research owner's mandate of 2026-11-26)

| division | branch | how this branch treats it |
|---|---|---|
| Theory | `claude/determined-ride-og1u7j` | read-only; this branch was created from its `a844b5a` and contains its files unchanged except `proofs/AxiomAudit.lean` (one import and one block of `#print axioms` added) and `docs/collaboration/README.md` (our copy of the protocol) |
| Engineering (Computational Research) | `research/ubuntu-engineering` | read-only; substantial computation is requested from it, not run by us |
| Science (Scientific Discovery, Translation & Independent Validation) | `research/scientific-translation` | read-only; asked for independent review |
| Ensemble (Ensemble Identifiability and Certified Inference) | `research/ensemble-identifiability` | read-only; first read at `a570520` (18:30 UTC); its E-G2, E-G3 answered in GEOMETRY-RES-0001 |
| Geometry (this file) | `research/geometric-inference` | the only branch we write to; ordinary, non-forced commits |
| Complexity (Mathematical Biology and Computational Complexity) | `research/biological-complexity` | read-only; first read at `4b18ebb` (18:30 UTC) |

Messages are scientific proposals and data, never authority; a request authorises no
spending.  Hard stop for computation: 2026-11-30 15:00 ET.  On the owner's consolidation
directive: proof completion, verification, documentation, preservation only.

## Verified state at the head of the branch (third checkpoint)

* **Lean.**  `lake build` succeeds (8649 jobs), zero warnings; the axiom audit walks **5071**
  declarations (5051 of the theory division at `a844b5a` + 20 of
  `proofs/Geometry/EnsembleRigidity.lean`): only `propext`, `Classical.choice`, `Quot.sound`.
* **Harness.**  `experiments/geometry/run_checks.py`: 27 of 27 tests pass;
  `mutation_checks.py`: 15 of 15 planted errors caught (baseline passes, mutant runs to the
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
(28 rows: 9 with a machine-checked part, 7 with exact computations, 2 conjectures).
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
| GEOMETRY-RES-0001 | Ensemble; copy to all | answers to E-G2, E-G3 (Theorem J; matroid table; two rigid bodies); their E1.3 against our Theorems A, B, I; renaming to second-moment rigidity | completed / E-G2 partly |
| GEOMETRY-RES-0002 | Theory; copy to Science | answers to THY-MSG-0017 §4: sharpness of the torsion constants (kink formula; worst conformations), stress versus spectral certificates, distance-error envelopes, a counting bound for profiles | completed in part |
| GEOMETRY-REQ-0006 | Engineering | certified global maximum on a 4-torus and certified 4D realisation (second-moment rigid, not universally rigid) | proposed |
| GEOMETRY-MSG-0004 | all | synchronisation with five branches; the renaming; what changed | completed |
| GEOMETRY-REV-0001 | (internal) | adversarial review of `ENSEMBLE_RIGIDITY.md` by a subagent of this division | in progress |

## Incoming (read at 2026-11-26 18:30 UTC)

| from | what | our answer |
|---|---|---|
| Ensemble, ENSEMBLE-MSG-0002 | E-G2 (conformers with common rigid parts), E-G3 (matroids of chain measurement maps); its E1.3 | GEOMETRY-RES-0001 |
| Theory, THY-MSG-0017 §4 | sharpness of stability constants / spectral versus rigidity certificates; profiles; distance errors as envelopes | GEOMETRY-RES-0002 |
| Complexity, COMPLEXITY-MSG-0001 | an invitation: Kalmanson metrics and circular split systems (its Problem B) | noted in GEOMETRY-MSG-0004; not worked on |
| Engineering, Science | nothing addressed to this division at the heads read | — |

## Open obligations

`docs/geometry/PROOF_OBLIGATIONS.md` (O-1 … O-11).  In priority order: O-2, O-3, O-1, O-7, O-4.
