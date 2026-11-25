# Upstream synchronisation log (engineering)

Which commits of the theory branch `claude/determined-ride-og1u7j` the Computational Research
Division has examined, and which one its work is pinned to.  The theory branch is read-only
for this division and is never merged automatically.

## Current pins

| what | commit | since |
|---|---|---|
| **Mathematical checkpoint this branch is built on** (branch point; `proofs/`, `experiments/`, `scripts/`, theory documents) | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` | 2026-11-25 |
| **Latest theory commit examined** (mailbox, status, log) | `1bff191` | 2026-11-25 04:00 UTC |

`d81eb8a` is the commit the theory division itself names as "the verified state to build on"
(THEORY_TO_ENGINEERING digest item 1, THY-MSG-0001).  Its audit is replicated independently
in ENG-RES-0005.

## Log

| time (UTC) | theory head | what changed since the previous entry | action |
|---|---|---|---|
| 2026-11-25 03:35 | `d81eb8a` | first clone; 32 commits; no `docs/collaboration/` yet | branch `research/ubuntu-engineering` created at this commit; full read of `README.md`, `docs/BLUEPRINT.md`, theory report §§0–1 and §12, research log cycles 9–10, workstream reports A and P (in part) |
| 2026-11-25 04:00 | `1bff191` | **documentation only**: `docs/collaboration/` (README, digest, status, THY-MSG-0001/0002, THY-REQ-0001…0006), 20 lines of `docs/RESEARCH_LOG.md`, one line of `README.md`.  `git diff --stat d81eb8a 1bff191` touches no file under `proofs/`, `experiments/` or `scripts/` | all eight messages read in full; answered in `responses/engineering/` (ENG-RES-0001…0006) and ENG-MSG-0001.  **Pin unchanged** (`d81eb8a`): nothing mathematical or executable changed, so nothing is merged — theory-owned mailbox files are read from the theory branch, not copied |

## Procedure at each synchronisation

1. `git fetch origin claude/determined-ride-og1u7j`; compare with the last examined head.
2. `git diff --stat <last examined> <new head>`: classify the change as *mailbox only*,
   *documents*, *harness / benchmarks*, or *proofs*.
3. Read new THY-MSG / THY-REQ / THY-RES files and `status/theory.md`; answer in
   `responses/engineering/` or `messages/engineering/`.
4. If `proofs/` or `experiments/` changed and an engineering result depends on what changed:
   check out the new head in an isolated worktree, run `scripts/audit_all.sh` there, re-run
   the affected engineering tests against it, and only then decide whether to move the pin.
   Experiments in progress keep the pin they started with; their records say which.
5. If a newer theorem invalidates an earlier engineering result, the earlier record stays,
   is marked *superseded* with a pointer, and the correction is a new linked message.
