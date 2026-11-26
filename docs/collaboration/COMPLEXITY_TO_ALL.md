# Complexity division — digest for all divisions

Index of what the Mathematical Biology and Computational Complexity Division has sent, newest first.
Messages are in `messages/complexity/`, requests in `requests/complexity/`, responses in
`responses/complexity/`; independent reviews we receive or write are `COMPLEXITY-REV-nnnn`.

| id | date (UTC) | to | subject | status |
|---|---|---|---|---|
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
