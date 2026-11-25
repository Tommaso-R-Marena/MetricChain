# Workstream R7 — notes (kept from the first minute)

Referee: independent review + replication of the ENGINEERING division
(branch `research/ubuntu-engineering` at `a2f6dc7`).

Conventions in these notes:
* "OWN" = my own code written before reading engineering's implementation.
* "RERUN" = their code exported into `eng_copy/` and run here.
* "READ" = read only.
* Times are UTC from `date`.

## Log

### 2026-11-25 20:21 — start
* Read COMMON.md and R7_brief.md in full.
* Created `experiments/science/ws_R7/` and `eng_copy/`.
* `git rev-parse origin/research/ubuntu-engineering` = a2f6dc781de05b642189a51d2ed88f94e8ed7026 (matches brief).
* Plan (order of the brief):
  1. X-004 generic chain: read the MODEL DEFINITION ONLY (theory P_REPORT §§0, 2.1, 3.3), write own enumerator,
     then read ENG-RES-0007/-0009 numbers, compare, THEN read their code.
  2. X-002 lattice covers as certificates.
  3. X-003 Harper closed form.
  4. X-005 statistics/claims.
  5. Record traceability.
  6. What is missing.
