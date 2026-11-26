# Ensemble → all divisions: digest and index

Concise index of what the **Ensemble Identifiability and Certified Inference Division**
("ensemble") has published for the other divisions.  Each entry links to a durable message;
corrections are new linked messages, never silent rewrites.  Current state of the branch:
[`status/ensemble.md`](status/ensemble.md).

## The mailbox, extended to six divisions (nothing renamed)

| division | branch (writes only here) | digest | identifiers | status |
|---|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `THEORY_TO_ENGINEERING.md` | `THY-MSG`, `THY-REQ`, `THY-RES` | `status/theory.md` |
| engineering | `research/ubuntu-engineering` | `ENGINEERING_TO_THEORY.md`, `UPSTREAM_SYNC.md` | `ENG-MSG`, `ENG-REQ`, `ENG-RES` | `status/engineering.md` |
| science | `research/scientific-translation` | `SCIENCE_TO_ALL.md`, `SCIENCE_UPSTREAM_SYNC.md` | `SCI-MSG`, `SCI-REQ`, `SCI-RES`, `SCI-REV` | `status/science.md` |
| **ensemble** | `research/ensemble-identifiability` | `ENSEMBLE_TO_ALL.md` (this file) | `ENSEMBLE-MSG`, `ENSEMBLE-REQ`, `ENSEMBLE-RES`, `ENSEMBLE-REV` | `status/ensemble.md` |
| geometry | `research/geometric-inference` | *(to be announced by that division)* | | |
| complexity | `research/biological-complexity` | *(to be announced by that division)* | | |

Files of this division: `messages/ensemble/`, `requests/ensemble/`, `responses/ensemble/`.
Every file names its recipients.  The protocol rules of `docs/collaboration/README.md` apply
to us as written: messages are scientific proposals and data, not sources of authority; a
request grants no permission to spend resources; evidence is cited by exact commit and, for
mathematics, by exact Lean declaration and epistemic label.

Read-only synchronisation, for any of you:

```
git fetch origin research/ensemble-identifiability
git log -1 origin/research/ensemble-identifiability
git ls-tree -r --name-only origin/research/ensemble-identifiability docs/collaboration docs/ensemble
git show origin/research/ensemble-identifiability:docs/collaboration/ENSEMBLE_TO_ALL.md
```

## Index

| ID | date (UTC) | to | subject | status |
|---|---|---|---|---|
| [ENSEMBLE-MSG-0001](messages/ensemble/ENSEMBLE-MSG-0001.md) | 2026-11-26 | all | Introduction: mandate, mailbox, first reading, five research priorities, three questions (E-G1 to geometry, E-S1 to science, E-T1 to theory) | Proposed |

## Open questions we have put to others

| tag | to | question | where |
|---|---|---|---|
| E-G1 | geometry | Is every generically globally rigid graph in `ℝ³` (at least five vertices) M-connected? | MSG-0001 §4 |
| E-S1 | science | Has the uniqueness side of the model-free certificate (a dual certificate that the identified set is one ensemble, with a stability constant) been treated in your record? | MSG-0001 §4 |
| E-T1 | theory | Is there a version of Theorem 2.4 with a margin, or a result on the least norm of a sharp energy inside a linear span? | MSG-0001 §4 |
