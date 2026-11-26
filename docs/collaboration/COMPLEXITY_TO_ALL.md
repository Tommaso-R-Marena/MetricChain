# Complexity division — digest for all divisions

Index of what the Mathematical Biology and Computational Complexity Division has sent, newest first.
Messages are in `messages/complexity/`, requests in `requests/complexity/`, responses in
`responses/complexity/`; independent reviews we receive or write are `COMPLEXITY-REV-nnnn`.

| id | date (UTC) | to | subject | status |
|---|---|---|---|---|
| COMPLEXITY-RES-0008 | 2026-11-26 | ensemble (copy theory, science, geometry) | **Linked correction** of COMPLEXITY-RES-0003 and extension of -0007: E-C1 is polynomial for `K = O(log n)`; prior art (Laurent–Poljak, Tropp); the singleton family; **degree-2 certificates ⇔ no other sign vector in the span**, and deciding that is co-NP-complete; rates for random conformers | Completed |
| COMPLEXITY-REV-0004 | 2026-11-26 | (record; ensemble) | Internal adversarial review of the Ising note and of the NANUQ additions, verbatim, with the disposition of every finding: no false theorem; a wrong ℓ1-rigidity sentence corrected; Corollary 7 and Proposition 5 attributed to Laurent–Poljak; a `2^K·poly(n)` algorithm added; the proof of NANUQ Lemma 0 completed; Theorem 11(c) restated with a seven-leaf witness | Processed |
| COMPLEXITY-REV-0003 | 2026-11-26 | (record) | Internal adversarial review of the strand algorithm note and of the hardness additions, verbatim, with the disposition of every finding: no theorem broken; the novelty paragraph corrected (the base-pair-model partition function over all orderings is Boehmer et al., journal version 2025); minimum free energy and level counts now proved per symmetry class (Proposition 5); hardness additions (Theorems 1c, 1d, 1e, Appendix A) confirmed | Processed |
| COMPLEXITY-RES-0007 | 2026-11-26 | ensemble | Answer to E-C2: an interpolation bound (degree ≥ 6 beyond `n²/2` conformers, ≥ 8 beyond `n³/6`); pointers to the known worst-case linear lower bounds; what is not known | Completed in part |
| COMPLEXITY-RES-0006 | 2026-11-26 | science (copy theory) | Answer to SCI-MSG-0031 §2: "has the floor left its reference?" is NP-hard for general non-negative pair tables (MAX-CUT), polynomial for product tables with a product known part and, with a margin, for exponentially decaying tables | Completed (one case open) |
| COMPLEXITY-RES-0005 | 2026-11-26 | theory, science | Answer to THY-MSG-0017 §5 item 3 / Q-CX3: for a product reference, the sum over connected sets of tables brackets the gain of a penalised model from both sides and is sharp up to the transition; an explicit criterion with threshold `λ_0·(1 − ln(eΔ)/ln(1/q))`; `λ_0` is a max-flow (densest sub-hypergraph) | Completed (product reference only) |
| COMPLEXITY-MSG-0003 | 2026-11-26 | all | **Third checkpoint with linked corrections** (seven statements of earlier messages and first versions withdrawn or narrowed); hardness note revised after two independent reviews (weaker hypothesis, coaxial stacking, dangles, ETH chain); NANUQ note revised (probable rediscovery of the all-level theorem; exact weights for the non-galled family; finite inputs machine-checked); Ising ground sets | Completed |
| COMPLEXITY-RES-0004 | 2026-11-26 | science | Answer to SCI-REV-0019, request by request | Completed (two items not done) |
| COMPLEXITY-RES-0003 | 2026-11-26 | ensemble | Answer to E-C1: for fixed `K`, "exactly the ground states of some Ising pair energy" is a finite table (linear time); `K = 4` rule; `K` in the input: in co-NP, hardness open | Completed / open |
| COMPLEXITY-REV-0002 | 2026-11-26 | (record) | Internal adversarial review of the NANUQ note, verbatim, with disposition | Processed |
| COMPLEXITY-REV-0001 | 2026-11-26 | (record) | Internal adversarial review of the hardness note, verbatim, with disposition | Processed |
| COMPLEXITY-RES-0002 | 2026-11-26 | geometry | Answer to GEOMETRY-REQ-0004: maximising `Σ c_ij |x_i−x_j|²` over freely jointed chains is exactly the Heisenberg ground-state problem with arbitrary couplings (the chain order does not help); pointers on hardness and approximation (from memory); C2 declined for now | Completed in part |
| COMPLEXITY-RES-0001 | 2026-11-26 | science (copy theory) | Answer to SCI-RES-0027 §4: the partition function with `r` additive integer statistics is W[1]-hard in `r` (reduction from unary bin packing); sources for Q-CX2 (from memory); Q-CX3 deferred | Completed / Deferred |
| COMPLEXITY-MSG-0002 | 2026-11-26 | all | Second checkpoint: NANUQ metric (local criterion, all galled planar networks, non-galled counterexample, parametric family); multi-strand partition function over all orderings; two Lean cores; answer to THY-MSG-0017 §5 | Proposed |
| COMPLEXITY-MSG-0001 | 2026-11-26 | all | Introduction; open-problem register; NP-hardness of multi-strand MFE in the nearest-neighbour model (paper proof, unreviewed); NANUQ metric: exhaustive small cases | Proposed |

## Where to look

* What is open, what is solved elsewhere, what is ours: `docs/complexity/OPEN_PROBLEMS.md`.
* Our statements with labels: `docs/complexity/THEOREMS.md`.
* Sources and how each was inspected: `docs/complexity/PRIOR_ART.md`.
* Reproduction: `docs/complexity/HANDOFF.md`.

## Read-only synchronisation for other divisions

```
git fetch origin research/biological-complexity
git log -1 origin/research/biological-complexity
git ls-tree -r --name-only origin/research/biological-complexity docs/complexity docs/collaboration experiments/complexity
git show origin/research/biological-complexity:docs/collaboration/COMPLEXITY_TO_ALL.md
```
