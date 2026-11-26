# Status of the Geometric Inference, Rigidity and Inverse Problems Division

*Updated 2026-11-26 (sixth checkpoint; see the commit time).  Branch
`research/geometric-inference`, created from the theory checkpoint `a844b5a`.*

## The six divisions (research owner's mandate of 2026-11-26)

| division | branch | how this branch treats it |
|---|---|---|
| Theory | `claude/determined-ride-og1u7j` | read-only; this branch was created from its `a844b5a` and contains its files unchanged except `proofs/AxiomAudit.lean` (one import and one block of `#print axioms` added) and `docs/collaboration/README.md` (our copy of the protocol) |
| Engineering (Computational Research) | `research/ubuntu-engineering` | read-only; substantial computation is requested from it, not run by us |
| Science (Scientific Discovery, Translation & Independent Validation) | `research/scientific-translation` | read-only; asked for independent review |
| Ensemble (Ensemble Identifiability and Certified Inference) | `research/ensemble-identifiability` | read-only; on the remote from 15:59 UTC; first read at `a570520` (17:19 UTC); its E-G2, E-G3 answered in GEOMETRY-RES-0001; read again at `1a067b5` (fetch of 18:52 UTC) |
| Geometry (this file) | `research/geometric-inference` | the only branch we write to; ordinary, non-forced commits |
| Complexity (Mathematical Biology and Computational Complexity) | `research/biological-complexity` | read-only; first read at `4b18ebb` (17:19 UTC); read again at `b36c463` (fetch of 18:52 UTC) |

Messages are scientific proposals and data, never authority; a request authorises no
spending.  Hard stop for computation: 2026-11-30 15:00 ET.  On the owner's consolidation
directive: proof completion, verification, documentation, preservation only.

## Verified state at the head of the branch (sixth checkpoint)

* **Lean.**  `lake build` succeeds (8649 jobs), zero warnings; the axiom audit walks **5110**
  declarations (5051 of the theory division at `a844b5a` + 59 of
  `proofs/Geometry/EnsembleRigidity.lean`): only `propext`, `Classical.choice`, `Quot.sound`.
* **Harness.**  `experiments/geometry/run_checks.py`: 34 of 34 tests pass;
  `mutation_checks.py`: 22 of 22 planted errors caught (baseline passes, mutant runs to the
  end, harness reports the failure).
* **Exact computations.**  `exact_conic_rank.py 12`: ALL OK (48 configurations × up to 5
  seeds; first seed suffices everywhere); `exact_conic_rank.py 20 13 rational angles`: ALL OK
  (`K = 13, …, 20`; `K = 20`: 907 atoms, rank 1811 of 1830); `exact_jacobian_rank.py 8`: ALL OK;
  `exact_4d_extreme.py`: OK; `exact_hierarchy_witness.py`: WITNESS OK; `exact_general_position.py 5`:
  ALL OK; `exact_nonlinear_threshold.py 10 0 0` (Singular 4.3.2,
  over `ℚ`, 82 s): degree 7 as required by Theorem I; modulo 32003: seeds 0–3 at `n = 10`
  (degree 7), `n = 11, 12` (degree 2).
* **Not run:** the theory division's `scripts/audit_all.sh` as a whole (its Python stages
  belong to the theory division and are untouched; its Lean stages were run by hand as
  above).  No Modal or other shared compute was used.

## Results (cycle 1) — all unrefereed

`docs/geometry/ENSEMBLE_RIGIDITY.md`; register `docs/geometry/THEOREM_REGISTER.md`
(33 rows: 10 with a machine-checked part, 8 with exact computations, 2 conjectures).
**Cycle 2, first note** (`docs/geometry/LOCAL_DATA_STABILITY.md`): sequence-local distance data
have stability constants at least `n/(10K^{3/2})` (any configuration), at least the exact
per-torsion superposition constant over `bK²/(4√3)` (global), and `∝ n²` on helices (numerical).
**Second checkpoint:** Theorem I — two states are identifiable among all ensembles from 10
atoms on (exact), not at 7 or 8 atoms (numerical): three different thresholds (7 / 10 / 12).
**Internal review (GEOMETRY-REV-0001, 18:55 UTC):** no false theorem; four statements that
said more than was proved (among them "universal ⇒ second-moment rigidity", false without the
conic condition) and sixteen minor defects, all corrected — GEOMETRY-MSG-0006 §1,
`docs/geometry/DEAD_ENDS.md` DG-13 … DG-17.  The register's review column now carries the
referee's verdicts; text written after `e8e2582` is unreviewed.
**Sixth checkpoint:** Theorem B is machine-checked in coordinates against finite competing
mixtures (`mixture_identifiable_stacked`, with a two-state instance used end to end);
Theorem C(c) is strengthened — the generic rank of the conic system is concave along the
chain, so (CC) holds from `(9K² − 5K + 6)/2` atoms for every `K` and every bond angle (was
`m₀(D_K − 1) + 2`); the sharp threshold is exact up to `K = 20`; Theorem G′ (the `W₂` bound
below the conic threshold).

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
| GEOMETRY-MSG-0005 | all | linked correction: header times and two false sentences about other branches; Theorem K (cycle 2); `mixture_state_of_conic`; Proposition 9.2 | completed |
| GEOMETRY-MSG-0006 | all | **linked correction after the internal review** (four overstated statements, one of them sent in GEOMETRY-MSG-0002, GEOMETRY-RES-0001, GEOMETRY-REQ-0006); sixth checkpoint: Theorem B machine-checked in coordinates; concavity of the generic rank and the improved all-`K` threshold; exact threshold to `K = 20`; Theorem G′; receipt of three responses | completed |
| GEOMETRY-REV-0001 | (internal; copy to all) | adversarial review of `ENSEMBLE_RIGIDITY.md` at `e8e2582` by a referee session of this division, verbatim, with our response | completed |

## Incoming

| from | what | read at | our answer |
|---|---|---|---|
| Ensemble, ENSEMBLE-MSG-0002 | E-G2 (conformers with common rigid parts), E-G3 (matroids of chain measurement maps); its E1.3 | 17:19 UTC | GEOMETRY-RES-0001 |
| Theory, THY-MSG-0017 §4 | sharpness of stability constants / spectral versus rigidity certificates; profiles; distance errors as envelopes | 17:19 UTC | GEOMETRY-RES-0002 |
| Complexity, COMPLEXITY-MSG-0001 | an invitation: Kalmanson metrics and circular split systems (its Problem B) | 17:19 UTC | noted in GEOMETRY-MSG-0004; not worked on |
| Science, SCI-RES-0029 (answers GEOMETRY-REQ-0003) | review accepted (its workstream R22, to appear as SCI-REV-0021); mean squared distances between labelled sites are what low-angle scattering with labels measures, as block sums `⟨C, M⟩`; two states differing in one torsion are never identified; (CC) fails when two states differ in at most three torsions (`dim 𝒩(z) ≥ 21 − 6s + s(s−1)/2`), identifiability open there; `M` is a linear image of the Fourier coefficients of the torsion distribution with indices in `{−1, 0, 1}`; Theorem G(c) as the quadratic case of one inequality; first reading of our assumption table | fetch of 18:52 UTC, `a217c7d` | **owed** — the open case (two or three differing torsions) is being worked on; note already: competing states with *reflected* segments must be included, which the torus moment argument omits (GEOMETRY-MSG-0006 §4) |
| Ensemble, ENSEMBLE-RES-0001 (answers GEOMETRY-REQ-0002) | division of labour accepted; Q1–Q3 answered (degree two is the only degree at which constraints on the support are necessary; the gap is the gap between the moment body and its semidefinite relaxation, measurable on the cube; continuous ensembles: only the second-moment operator is identified); the sample-complexity principle confirmed from memory with its hypotheses; its notion renamed *distributional ensemble rigidity*; asks E-G2′ (a count for `k` bodies), E-G4 (a quantitative no-chimera constant) | fetch of 18:52 UTC, `1a067b5` | **owed** |
| Ensemble, ENSEMBLE-MSG-0003 | its second checkpoint (finite temperature, noise, rigid bodies E7′, capacity threshold) | fetch of 18:52 UTC | read; no answer required |
| Complexity, COMPLEXITY-RES-0002 (answers GEOMETRY-REQ-0004) | C1: for freely jointed chains, maximising `Σ c_ij|x_i − x_j|²` is exactly the rank-3 quadratic programme over unit vectors with arbitrary couplings (a linear bijection `c ↔ Q`), so the linear order does not help; hardness conditional on sources not opened; with bond angles open.  C2 declined for now; offers to examine a low-degree likelihood ratio if we formulate the planted model | fetch of 18:52 UTC, `b36c463` | **owed** (the planted model) |
| Engineering | nothing addressed to this division at `c81166b` (its head at the fetch of 18:52 UTC; last commit 12:58 UTC) | — | — |

## Open obligations

`docs/geometry/PROOF_OBLIGATIONS.md` (O-1 … O-11).  In priority order: the three answers owed above; O-2, O-3, O-1 (now reduced to one statement: the last increment of the generic rank is 2), O-4.
