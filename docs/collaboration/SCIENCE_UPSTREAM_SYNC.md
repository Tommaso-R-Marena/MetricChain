# Science division: upstream synchronisation record

Read-only record of which commits of the other two branches this division has examined.
Nothing is ever merged.  The science branch `research/scientific-translation` was created at
the theory head `5ed4072` (so the theory files in this tree are exactly that commit); the
engineering branch is read through `git show` / a detached read-only checkout.

## Pins

| what | commit | date (commit time) |
|---|---|---|
| branch point of `research/scientific-translation` | `5ed407282d89af46d260d2dd1687059c8e3e7728` (theory, "Cycle 10, tenth checkpoint: slices") | 2026-11-25 17:16:50 UTC |
| latest theory commit read | `5ed407282d89af46d260d2dd1687059c8e3e7728` | 2026-11-25 17:16:50 UTC |
| latest engineering commit read | `db56d05f695ec390dd9ef8c7d14dfdb07d8b1e6a` ("[ENG] Checkpoint 2") | 2026-11-25 06:01:47 UTC |
| engineering's own pin of theory | `d81eb8a` (branch point), `4cef47e` (latest read and audited by them) | — |

## What was read at each pin, and at what depth

| commit | read in full | read in part | not yet read by the coordinator (assigned to a workstream) |
|---|---|---|---|
| theory `5ed4072` | `README.md`; `docs/collaboration/README.md`, `status/theory.md`, THY-MSG-0001 (first half); theory report §§0, 1, 8, 10, 12, §11.6 (start); `DEAD_ENDS.md` D28, D42 and all headings; research log "Resume here"; `docs/workstreams/COMMON.md`; `scripts/audit_all.sh` (structure) | theory report §11 headings; `prior_art/L5`, `L6`, `L8` (the lines on density-ratio classes and Henderson) | theory report §11.2–11.25 in detail (A1, A2, R1, R2, P, K, X); referee reports R1–R9; workstream reports; `proofs/` |
| engineering `db56d05` | `ENGINEERING_TO_THEORY.md`, `status/engineering.md`, ENG-MSG-0001 | file list | ENG-RES-0001…0007, ENG-REQ-0001, `experiments/eng/` (R2, P) |

## Dependencies of science results on upstream statements

| our statement | depends on (theory, at `5ed4072`) | nature of the dependence |
|---|---|---|
| SCI-MSG-0001 §4, Theorem B(a) | `admissible_iff_weights` (**[V]**, `ThermalRobustness.lean`; theory report Theorem 11.12, remark) | the class is a convex cone in the weights — used as stated; re-derived, not re-compiled |
| SCI-MSG-0001 §4, Theorem C | theory report Theorem 11.22 (sensitive alternatives must be detected) and the dip bounds on the cube | our proof repeats the indistinguishability argument with a symmetrised alternative; the *value* of the exponent it leaves unchanged (`θ_hint`) and its attainment by adaptive algorithms are the theory division's Theorems 11.25, 11.54, 11.58 (**[P]**, refereed R3/R4, R7, R8), which we have not independently reviewed |

## Synchronisation log

| time (UTC) | observation |
|---|---|
| 2026-11-25 17:27 | first fetch of all branches: theory head `5ed4072` (17:16:50 UTC), engineering head `db56d05` (06:01:47 UTC); `research/scientific-translation` did not exist; no `main` branch on the remote |
| 2026-11-25 17:33 | `research/scientific-translation` created at `5ed4072` and pushed (no content of our own yet) |
| 2026-11-25 17:50 | before checkpoint 1: both upstream heads unchanged |
