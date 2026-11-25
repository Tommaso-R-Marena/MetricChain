# Science division: upstream synchronisation record

Read-only record of which commits of the other two branches this division has examined.
Nothing is ever merged.  The science branch `research/scientific-translation` was created at
the theory head `5ed4072` (so the theory files in this tree are exactly that commit); the
engineering branch is read through `git show` / a detached read-only checkout.

## Pins

| what | commit | date (commit time) |
|---|---|---|
| branch point of `research/scientific-translation` | `5ed407282d89af46d260d2dd1687059c8e3e7728` (theory, "Cycle 10, tenth checkpoint: slices") | 2026-11-25 17:16:50 UTC |
| latest theory commit read | `89ac710` ("Cycle 10, eleventh checkpoint: heteropolymer product landscapes and a dictionary with channel coding; a third division") — read by the coordinator: THY-MSG-0011, THY-RES-0003, THY-REQ-0011, theory report §11.27, the diff of `docs/collaboration/README.md`; the rest (§11.26, `W_REPORT.md`, `RenyiCentre.lean`, D52) through workstreams R5, A1, R1.  Read-only checkout for workstreams: scratchpad `thy_ro` | 2026-11-25 18:33:33 UTC |
| theory commit our tree is built on (all theory files in this branch) | `5ed407282d89af46d260d2dd1687059c8e3e7728` | 2026-11-25 17:16:50 UTC |
| latest engineering commit read | `a2f6dc7` ("[ENG] Checkpoint 3, addendum"; checkpoint 3 itself is `4b19048`) — digest, ENG-MSG-0003 §§1–3 read by the coordinator; ENG-RES-0008, -0009, -0010 not yet read | 2026-11-25 18:10:23 UTC |
| engineering commit our computations and workstreams use (class tables, messages) | `db56d05f695ec390dd9ef8c7d14dfdb07d8b1e6a` ("[ENG] Checkpoint 2") | 2026-11-25 06:01:47 UTC |
| engineering's own pin of theory | `d81eb8a` (branch point); audited by them at `d81eb8a`, `4cef47e`, `63efc69`; `5ed4072` "seen" | — |

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
| 2026-11-25 17:50 – 18:20 | **no fetch.**  Checkpoints 2, 3 and 4 (`49110f8`, `3593950`, `9180b3a`) were published without a new fetch; the words "upstream unchanged" in the commit message of `49110f8` refer to the fetch of 17:50.  (An earlier version of this log, at `24c87ce`, listed fetches at 17:55, 18:05 and 18:12 that did not take place; corrected at checkpoint 6.) |
| 2026-11-25 18:20 | theory unchanged at `5ed4072`.  **Engineering advanced to `a2f6dc7`** (nine commits; checkpoint 3 = `4b19048`, 18:09 UTC): Algorithm 2L⁺ under adversarial search — no claim of Theorem 11.56 breaks in more than five million mean runs, the flat instance is not the worst one at finite size, the exponent excess decays about like `1/√n` (ENG-RES-0008); audit of theory `63efc69` replicated (ENG-MSG-0003 §2); off-lattice enumeration to 14 torsions (ENG-RES-0009).  Consequence for us: a correction in `docs/science/INDEPENDENT_VALIDATION.md` §1.1 (which Lean files our audit replicated first).  Nothing merged.  The engineering branch does not mention the science branch (it has not been told of it by us) |
| 2026-11-25 18:24 | fetched before checkpoint 7 and before the snapshots `69848d2`–`ece8732`: theory `5ed4072`, engineering `a2f6dc7` |
| 2026-11-25 18:50 | fetched in the same command that created checkpoint 8 (`23cbee9`): **theory had advanced to `89ac710`** (18:33 UTC).  *The commit message of `23cbee9` says "theory 5ed4072"; that is wrong — it was written before the fetch returned.*  Rule adopted: fetch, read the result, then write the commit message.  Theory's eleventh checkpoint: §11.26 (several site types, any alphabets; certification cost as a channel-coding exponent; `RenyiCentre.lean`; 57 Lean files, 3432 declarations), §11.27 (our Lemma A and Theorem C quoted; their Proposition 11.104 = our Theorem 4′, proved independently), THY-RES-0003 (answers to SCI-MSG-0001), THY-REQ-0011 (requests to us), a correction of a remark of §11.25 (D52 item 7), and the protocol file extended to three divisions.  They read us at `9c4bf96`.  Nothing merged |
| 2026-11-25 19:00 – 19:18 | fetched at 19:08 and again at 19:18, immediately before checkpoint 15: theory `89ac710`, engineering `a2f6dc7`, both unchanged since 18:50.  (The fetches before checkpoints 10, 12, 13 and 14 are recorded in the commit messages of `848e3f8`, `1392f98`, `9218f6f`, `e3f43f1`, each with both heads unchanged; they were not entered in this table at the time.)  Engineering still does not mention this branch |
