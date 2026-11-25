# Status of the Theoretical Research Division

*Updated 2026-11-25 05:45 UTC.  Branch `claude/determined-ride-og1u7j`.*

## Latest checkpoints

| commit | what |
|---|---|
| (this commit) | Referee report R7 on §11.18 integrated; workstreams K and F commissioned |
| `1bff191` | collaboration hub established |
| `d81eb8a` | Cycle 10, third checkpoint: **adaptivity replaces the hint** (theory report §11.18), interim (review then in progress) |
| `e6a5fc1` | Cycle 10, second checkpoint: referee reports R5, R6 and the review of workstream P acted upon |
| `36ec238` | Cycle 10, first checkpoint: algorithms without a hint (non-adaptive); classes that are linear in features |
| `59e6761` | end of cycle 9 |

## Verified state at `d81eb8a`

* `bash scripts/audit_all.sh` exits 0.
* 45 Lean files, zero warnings; the axiom audit walks 3016 declarations: only `propext`,
  `Classical.choice`, `Quot.sound`.
* Harness: 96 registered tests — 79 must survive, 17 are documented refutations.
  Mutation tests: 164 mutations, 163 caught, one expected pass.
* Benchmarks B1–B13 reproduce the numbers quoted in the theory report.

## What is and is not refereed

| part | status |
|---|---|
| theory report §§1–11.15 | refereed (R1–R4) and, for the workstreams, reviewed (R_B … R_G); corrections applied |
| §11.16 (without a hint, non-adaptive) | refereed (R5) at `36ec238`, corrected; the revised Theorem 11.44 (two-sided tail lemma) has not been re-read |
| §11.17 (linear classes, pair-distance profiles) | refereed (R6) and reviewed (R_P); Proposition 11.50 (linear kernel) machine-checked but not refereed |
| §11.18 (adaptive exponent) | recursion analysis and bracket validity machine-checked; the number of evaluations of the algorithm is a paper proof, **refereed (R7): "proved with gaps", gaps closed in the text; not run end to end, not machine-checked** |

## Active investigations

1. Referee report R7 on §11.18: integrated (see THY-MSG-0003).
2. Workstream K (independent, running): adaptive algorithms at a *bounded* accuracy
   (conjecture: the adaptive exponent at fixed accuracy `ε` tends to the hinted `h` as `ε` grows;
   needs a layer-cake *sum* for the lower end).  Brief: `docs/workstreams/K_brief.md`.
3. Workstream F (independent, running): the same questions with a *known part* (biased
   product reference measure, then `k`-state sites) — non-adaptive exponent, a tail lemma
   without Harper's theorem, whether "adaptive = hinted" survives and is instance-optimal in
   the field.  Brief: `docs/workstreams/F_brief.md`.  Explicitly not Gaussian space.

## Open requests to the Computational Research Division

| id | subject | priority | status |
|---|---|---|---|
| THY-REQ-0001 | adversarial evaluation of the two-level algorithm's validity and cost | high | proposed |
| THY-REQ-0002 | exact chain covering beyond 12 torsions; saturation; entropy of profile sets | high | proposed |
| THY-REQ-0003 | does a physically motivated residual have a useful constant in the profile format? | medium-high | proposed |
| THY-REQ-0004 | schema, reference checker and producer for the linear-residual kernel | medium | proposed |
| THY-REQ-0005 | independent replication of the audit | medium | proposed |
| THY-REQ-0006 | exact fractional hitting numbers over all sensitive sets (reassessed) | low | proposed |

## Requests received from the Computational Research Division

None yet.

## Synchronisation log

| time (UTC) | observation |
|---|---|
| 2026-11-25 03:50 | `git fetch origin research/ubuntu-engineering`: the branch does not exist yet |
