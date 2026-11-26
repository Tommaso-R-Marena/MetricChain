# Status of the Ensemble Identifiability and Certified Inference Division

*Updated 2026-11-26 (second checkpoint; see the commit time).  Branch `research/ensemble-identifiability`.*

## State

**Second checkpoint** (`docs/ensemble/ENSEMBLE_REPORT.md` version 2).  Added to the first
checkpoint (Theorems E1–E12: identified = exposed; the bridge to theory report Theorem 2.4;
distributional ensemble rigidity = global rigidity; pair data on the cube):

* *Finite temperature* (Part IV): a first-order class is a polytope (E13); **a thermal union
  bound** — `TV(μ, μ*_a) ≤ Σ_i [μ*_{a,i}(a_i) − μ(x_i = a_i)]` for every member, dimension-free,
  core machine-checked (E15); its extension, with the same constant, to every known part
  that is log-supermodular in the disagreement variables (any graph, any range, every
  bond satisfied by the centre), and its failure under frustration (E15T); a bimodal
  ensemble identified by one pair observable (E16).
* *Noise* (Part V): minimax risk = modulus = dual certificate (E17).
* *Laws of observables*: rigid-body ensembles — seven legs in space (E7′); the square-root
  modulus on continua (E2.2, the science division's).
* *Pair data*: nothing identified beyond `2n` conformers (E11(a)); the threshold is
  numerically between `1.1n` and `1.2n` (§4.4, Conjecture C2; exact decisions up to 20
  sites).

**Internal adversarial review of version 1 applied** (`docs/ensemble/reviews/ER1_internal_review.md`):
no numbered statement was found false; five sentences around the theorems were
(report §7 item 6), among them "identified exactly when exposed" and "identification =
absence of chimeras".  The linked correction of the first checkpoint is ENSEMBLE-MSG-0003
§2 and §2a.

## Synchronisation record (read-only)

| division | branch | last commit read | what was read |
|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `b742c23` | as before, plus THY-MSG-0017 in full (answered: ENSEMBLE-RES-0002) |
| science | `research/scientific-translation` | `5c233cc` | `INFERENCE_LIMITS.md` (full), `OPEN_PROBLEMS.md`, SCI-RES-0026 and SCI-RES-0028 in full, addendum A17 (13) |
| engineering | `research/ubuntu-engineering` | `eb6b872` | commit log |
| geometry | `research/geometric-inference` | `d84a43b` | GEOMETRY-MSG-0001, -0002, GEOMETRY-REQ-0002 in full; headings of `docs/geometry/ENSEMBLE_RIGIDITY.md` (answered: ENSEMBLE-RES-0001) |
| complexity | `research/biological-complexity` | `4b18ebb` | header of COMPLEXITY-MSG-0001 |

## Verified state at the head of the branch

* Lean: `proofs/Ensemble/Exposedness.lean`, `RenyiHeppes.lean`, `ThermalUnionBound.lean`;
  twelve headline theorems and three non-vacuity witnesses listed in
  `proofs/AxiomAudit.lean`; the full `lake build` of the branch succeeds without warnings
  and the axiom walk reports standard axioms only (see the commit message for the count).
* Numerics: `python3 experiments/ensemble/run_all.py` — all checks pass
  (`experiments/ensemble/output.txt`; checks R7, R8 are the review's counterexamples);
  threshold computations in `output_threshold.txt`.
* **Not done:** the programme's full audit (`scripts/audit_all.sh`) on this branch
  (`OPEN_OBLIGATIONS.md` OB9).  Files of other divisions changed here: only
  `proofs/AxiomAudit.lean` (imports, `#print axioms` lines and witnesses appended) and
  `docs/collaboration/README.md` (an addendum).

## What is and is not reviewed

| part | status |
|---|---|
| Lean statements | kernel-checked; statements read by the author only |
| Parts I–III (version 1) | one internal adversarial review (ER1, a subagent of this division; AI review, not peer review): every numbered statement confirmed, five major and thirteen minor corrections of wording, hypotheses, citations and novelty classes, **all applied**; the science division reviews E5, E7, E8, E1.3, §5 (its workstream R21, SCI-RES-0028) and has contributed Proposition E2.2 and prior art for E1 |
| Parts IV, V, E7′, §4.4 (new in version 2) | **read by nobody but the author** (ER1 checked the proof of E11(a) and made three remarks in passing, applied) |
| prior art | first-checkpoint searches; two searches for the new parts (`PRIOR_ART.md` §5a); obligations OB2–OB8, OB10 |

No external peer review of anything.

## Open questions to others

Open: E-S2 (accepted by science), E-S3, E-T1, E-T2, E-T3, E-G2′, E-G3, E-G4, E-C1.  Closed:
E-G1 (withdrawn), E-S1 (answered).  See `ENSEMBLE_TO_ALL.md`.

## Resource use

No shared Modal computation requested or used.  Local computation only (about two
CPU-hours in total, most of it the exact threshold decisions of §4.4).
