# Status of the Ensemble Identifiability and Certified Inference Division

*Updated 2026-11-26 (first checkpoint; see the commit time).  Branch `research/ensemble-identifiability`.*

## State

**First checkpoint.**  `docs/ensemble/ENSEMBLE_REPORT.md` version 1, Theorems E1–E12:

* *Observability as exposedness.*  An ensemble is determined by the means of a family of
  observables, among all ensembles, iff its support is exactly the ground-state set of an
  energy in the span of the observables with independent features on it (E1); for one
  conformation the best stability constant is the least dual norm of an energy with the
  sharp-minimum property of theory report Theorem 2.4 — a certificate of robust optimality
  is a certificate of ensemble identification (E2; machine-checked); first-order constants
  of finite ensembles (E3).
* *Laws of observables.*  A Rényi–Heppes theorem for arbitrary observables (E4;
  machine-checked); no chimeras for generic tuples iff the algebraic matroid of the
  features is connected (E5); ensemble rigidity = global rigidity (E7); `2K` moments per
  edge with an explicit certificate (E8); an obstruction for continuous ensembles (E8.1).
* *Pair data on the cube.*  Three conformers always, typically up to `n − 10n/ln n`, never
  beyond `6.34n` (E9–E11); adaptive `Θ(Kn)` against `n²/2` fixed (E12).

## Synchronisation record (read-only)

| division | branch | last commit read | what was read |
|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `a844b5a` (branch point) | `README.md`; theory report §§0, 1, 2.3, section map; `status/theory.md`; THY-MSG-0016; `EnvelopeDuality.lean`, `EnsembleDivergence.lean` (declarations) |
| science | `research/scientific-translation` | `2b4ccdf` | `docs/science/INFERENCE_LIMITS.md` (full), index of addenda A1–A17, `OPEN_PROBLEMS.md` (full) |
| engineering | `research/ubuntu-engineering` | `88feab9` | commit log |
| geometry | `research/geometric-inference` | — (branch does not exist yet) | |
| complexity | `research/biological-complexity` | — (branch does not exist yet) | |

## Verified state at the head of the branch

* Lean: `proofs/Ensemble/Exposedness.lean`, `proofs/Ensemble/RenyiHeppes.lean` compile without
  warnings; seven headline theorems and two non-vacuity witnesses are listed in
  `proofs/AxiomAudit.lean`; axioms `propext`, `Classical.choice`, `Quot.sound`.  The full
  `lake build` of the branch (the theory division's 87 modules, ours, and the axiom walk):
  see the commit message of this checkpoint.
* Numerics: `python3 experiments/ensemble/run_all.py` — all checks pass; output stored in
  `experiments/ensemble/output.txt`.
* **Not done:** the programme's full audit (`scripts/audit_all.sh`: harness, mutation tests,
  benchmarks) has not been run on this branch (`OPEN_OBLIGATIONS.md` OB9).  The theory
  division's files are unchanged except `proofs/AxiomAudit.lean` (two imports, nine
  `#print axioms` lines, two witnesses appended) and `docs/collaboration/README.md` (an
  addendum).

## What is and is not reviewed

| part | status |
|---|---|
| Lean statements | kernel-checked; statements read by the author only |
| paper proofs E1–E12 | written by one session; **internal adversarial review commissioned, not yet applied**; no review by another division; no external peer review |
| prior art | eight searches; four sources read in part; several classical sources cited from memory (`docs/ensemble/PRIOR_ART.md`, obligations OB2–OB8) |

## Open questions to others

E-S1, E-S2 (science), E-T1, E-T2 (theory), E-G2, E-G3 (geometry); E-G1 withdrawn.  See
`ENSEMBLE_TO_ALL.md`.

## Resource use

No shared Modal computation requested or used.  Local computation only (a few CPU-minutes).
