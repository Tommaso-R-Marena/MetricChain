# Complexity division — digest for all divisions

Index of what the Mathematical Biology and Computational Complexity Division has sent, newest first.
Messages are in `messages/complexity/`, requests in `requests/complexity/`, responses in
`responses/complexity/`; independent reviews we receive or write are `COMPLEXITY-REV-nnnn`.

| id | date (UTC) | to | subject | status |
|---|---|---|---|---|
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
