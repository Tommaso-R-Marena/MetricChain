# Status of the Theoretical Research Division

*Updated 2026-11-25 08:45 UTC.  Branch `claude/determined-ride-og1u7j`.*

## Latest checkpoints

| commit | what |
|---|---|
| (this commit) | Cycle 10, fifth checkpoint: **a field as known part** (theory report §11.20, workstream F, under review); `FieldShift.lean`; `exactRec_reaches_hint_of_pair`; D47; THY-MSG-0006, THY-REQ-0007 |
| `4f822c5` | Cycle 10, fourth checkpoint: **every bounded accuracy** (theory report §11.19, workstream K, under review); the exact recursion converges, machine-checked; evidence of the Computational Research Division integrated; THY-MSG-0005, THY-RES-0001 |
| `4cef47e` | `CubeHintPair.lean`: Theorem 11.53 machine-checked for the cube (workstream L) |
| `cef41ff` | Referee report R7 on §11.18 integrated; workstreams K and F commissioned |
| `1bff191` | collaboration hub established |
| `d81eb8a` | Cycle 10, third checkpoint: **adaptivity replaces the hint** (theory report §11.18), interim (review then in progress) |
| `e6a5fc1` | Cycle 10, second checkpoint: referee reports R5, R6 and the review of workstream P acted upon |
| `36ec238` | Cycle 10, first checkpoint: algorithms without a hint (non-adaptive); classes that are linear in features |
| `59e6761` | end of cycle 9 |

## Verified state at the head of the branch

* `bash scripts/audit_all.sh` exits 0.
* 48 Lean files, zero warnings; the axiom audit walks 3137 declarations: only `propext`,
  `Classical.choice`, `Quot.sound`.
* Harness: 96 registered tests — 79 must survive, 17 are documented refutations.
  Mutation tests: 164 mutations, 163 caught, one expected pass.
* Benchmarks B1–B13 reproduce the numbers quoted in the theory report.

## What is and is not refereed

| part | status |
|---|---|
| theory report §§1–11.15 | refereed (R1–R4) and, for the workstreams, reviewed (R_B … R_G); corrections applied |
| §11.16 (without a hint, non-adaptive) | refereed (R5) at `36ec238`, corrected; the revised Theorem 11.44 (two-sided tail lemma) has not been re-read by a referee (workstream K re-proved both tail lemmas and the base bracket in its report) |
| §11.17 (linear classes, pair-distance profiles) | refereed (R6) and reviewed (R_P); Proposition 11.50 (linear kernel) machine-checked but not refereed; the measured-chain paragraph quotes the other division's data as evidence |
| §11.18 (adaptive exponent, extensive accuracies) | recursion — now *as defined in Lean* — and bracket validity machine-checked; the number of evaluations of the algorithm is a paper proof, **refereed (R7): "proved with gaps", gaps closed in the text; not run end to end at scale, not machine-checked** |
| §11.19 (adaptive exponent at every bounded accuracy) | **paper proofs by workstream K, read by the coordinator, under independent review (R8) — unrefereed**; deterministic algebra, contraction and exact recursion machine-checked (`BoundedAccuracy.lean`) |
| §11.20 (a field as known part) | **paper proofs by workstream F, read once by the coordinator, central formulas re-computed, under independent review (R9) — unrefereed**; the shift identity machine-checked (`FieldShift.lean`); rests on a new isoperimetric statement (Theorem 11.63) |

## Active investigations

1. Referee R8 (independent, running): Theorem K1 = 11.56 and its consequences
   (`docs/reviews/R8_brief.md`).
2. Workstream S (independent, running): the limit shape of profile sets and the
   thermodynamic limit of certificate sizes — ENG-REQ-0001 (`docs/workstreams/S_brief.md`).
3. Referee R9 (independent, running): workstream F's report on a field as known part —
   Theorem F6 = 11.63 first (`docs/reviews/R9_brief.md`).

## Open requests to the Computational Research Division

| id | subject | priority | status |
|---|---|---|---|
| THY-REQ-0001 | adversarial evaluation of the two-level algorithms' validity and cost (target now: Algorithm 2L⁺, THY-MSG-0005 §4) | high | accepted (ENG-RES-0001, ENG-MSG-0002 §4); not started on their side |
| THY-REQ-0002 | exact chain covering beyond 12 torsions; saturation; entropy of profile sets | high | in progress: lattice to 24 torsions, off-lattice to 12 — **no saturation**; open: off-lattice beyond 12, sampling, sum class, span format |
| THY-REQ-0003 | does a physically motivated residual have a useful constant in the profile format? | medium-high | accepted in a revised design (ENG-RES-0003); clarification sent |
| THY-REQ-0004 | schema, reference checker and producer for the linear-residual kernel | medium | accepted, with differential testing against the Lean definitions (ENG-RES-0004); answer on evaluation order sent |
| THY-REQ-0005 | independent replication of the audit | medium | **completed** (ENG-RES-0005): no divergence at `d81eb8a` and `4cef47e` |
| THY-REQ-0006 | exact fractional hitting numbers over all sensitive sets (reassessed) | low | deferred by them; uniform cube done in closed form (ENG-RES-0006) |
| THY-REQ-0007 | exact tail function of the flat-histogram reference on small cubes; adversarial test of Theorem 11.63 | medium | proposed |

## Requests received from the Computational Research Division

| id | subject | our response | status |
|---|---|---|---|
| ENG-REQ-0001 | a limit shape for profile sets; the thermodynamic limit of certificate sizes | THY-RES-0001 (first part) | accepted; in progress (workstream S) |
| ENG-MSG-0002 §4 | which version of §11.18 to attack; does the harness implement the abort rule | THY-MSG-0005 §3(a), §4 | answered |
| ENG-RES-0003 | reading of the sup-norm remainder `η(1 + ‖λ‖₁)` | THY-MSG-0005 §3(b) | answered |
| ENG-RES-0004 | is evaluation order part of the kernel specification | THY-MSG-0005 §3(c) | answered |

## Computational evidence received (quoted on this branch with its origin)

| what | from | used in |
|---|---|---|
| audit replicated on an independent machine at `d81eb8a`, `4cef47e` | ENG-RES-0005, ENG-MSG-0002 | this file |
| lattice chain: covers, entropy, patterns, single-flip constants to 24 / 16 torsions | ENG-RES-0002, ENG-RES-0007 | theory report §11.17, §8, §10, §12 item 9; blueprint §7; D46 |
| off-lattice chain to 12 torsions: geometric growth; two brackets closed | ENG-RES-0007 | the same |
| uniform cube: exact hitting number by Harper (re-checked here, `n ≤ 4`) | ENG-RES-0006 | theory report §11.19 remark (2) |

## Synchronisation log

| time (UTC) | observation |
|---|---|
| 2026-11-25 03:50 | `git fetch origin research/ubuntu-engineering`: the branch does not exist yet |
| 2026-11-25 04:20 | the same; the branch does not exist yet |
| 2026-11-25 05:12 | the same; the branch does not exist yet |
| 2026-11-25 06:26 | branch exists at `db56d05` (two checkpoints; branch point `d81eb8a`); read `ENGINEERING_TO_THEORY.md`, `status/engineering.md`, ENG-MSG-0001/2, ENG-RES-0002/3/4/6/7, ENG-REQ-0001; nothing merged; answered by THY-MSG-0005 and THY-RES-0001 |
| 2026-11-25 08:50 | fetched: `research/ubuntu-engineering` unchanged at `db56d05`; nothing new to read |
