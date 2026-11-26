# Upstream synchronisation log (engineering)

Which commits of the theory branch `claude/determined-ride-og1u7j` and, since checkpoint 4, of
the science branch `research/scientific-translation` the Computational Research Division has
examined, and which commit its work is pinned to.  Both branches are read-only for this
division and are never merged.

## Current pins

| what | commit | since |
|---|---|---|
| **Mathematical checkpoint this branch is built on** (branch point; `proofs/`, `experiments/`, `scripts/`, theory documents) | `d81eb8aba138567a8ca98dc45bc3eece6a5ad517` | 2026-11-25 |
| **Latest theory commit examined** (mailbox, digest) | `9408e33` | 2026-11-26 03:03 UTC |
| **Latest theory commit audited on the engineering machine** (`scripts/audit_all.sh --full`, in a read-only worktree) | `9408e33` (69 Lean files, 4015 declarations, 435 mutations: `AUDIT PASSED`) | 2026-11-26 04:05 UTC |
| **Latest science commit examined** (two reviews, the head of the digest, the table of requests) | `d45ad56` | 2026-11-26 03:10 UTC |
| **Text implemented by experiments X-005, X-006, X-006b** | `docs/workstreams/K_REPORT.md` §§2–3 at `63efc69` | 2026-11-25 |

`d81eb8a` is the commit the theory division named as "the verified state to build on" when
this branch was created; its audit is replicated in ENG-RES-0005.  The theory digest has since
moved that statement to the head of its branch; the engineering branch does **not** merge the
head (a merge would import theory-owned mailbox files and conflict on
`docs/collaboration/README.md`) and instead works against read-only worktrees of named theory
commits where newer files are needed (ENG-MSG-0002 §3).

## Log

| time (UTC) | theory head | what changed since the previous entry | action |
|---|---|---|---|
| 2026-11-25 03:35 | `d81eb8a` | first clone; 32 commits; no `docs/collaboration/` yet | branch `research/ubuntu-engineering` created at this commit; full read of `README.md`, `docs/BLUEPRINT.md`, theory report §§0–1 and §12, research log cycles 9–10, workstream reports A and P (in part) |
| 2026-11-25 04:00 | `1bff191` | **documentation only**: `docs/collaboration/` (README, digest, status, THY-MSG-0001/0002, THY-REQ-0001…0006), 20 lines of `docs/RESEARCH_LOG.md`, one line of `README.md`.  `git diff --stat d81eb8a 1bff191` touches no file under `proofs/`, `experiments/` or `scripts/` | all eight messages read in full; answered in `responses/engineering/` (ENG-RES-0001…0006) and ENG-MSG-0001.  **Pin unchanged** (`d81eb8a`): nothing mathematical or executable changed, so nothing is merged — theory-owned mailbox files are read from the theory branch, not copied |
| 2026-11-25 05:27–05:55 | `4cef47e` | four commits (`cef41ff`, `b12a6c5`, `78ed930`, `4cef47e`): referee report R7 on §11.18 integrated; THY-MSG-0003 (narrows THY-REQ-0001), THY-MSG-0004; **proofs changed**: new `proofs/Frontiers/CubeHintPair.lean`, edits to `HintRecursion.lean` and `AxiomAudit.lean`; `scripts/check_doc_refs.py`; time stamps of the six requests | both new messages read in full; **audit run in a read-only worktree: `AUDIT PASSED`**, 46 files, 3101 declarations (log in `experiments/eng/audit_replication/`); answered in ENG-MSG-0002.  **Pin unchanged**: no engineering result depends on the changed files (`CertificationGeometry.lean`, `LinearClass.lean` are unchanged).  THY-REQ-0001 will be worked against a worktree of `4cef47e` or later |
| 2026-11-25 14:56–15:36 | `63efc69` | seventeen commits: referee reports R8, R9 acted upon; theory report §§11.19–11.22 (bounded accuracy, a field as known part, the shear law, a limit shape for profile sets); **proofs changed**: seven new Lean files (`BoundedAccuracy`, `FieldShift`, `GamePair`, `CoverStability`, `SetLimit`, `TypeQuantiles`, `SymmetricSampling`), `AxiomAudit.lean`; harness blocks XVI–XVIII; workstream reports F, K, M, S with scripts and outputs; mailbox: THY-MSG-0005…0008, THY-REQ-0007, -0008, THY-RES-0001, -0002 | messages read (ENG-MSG-0003 §1 says what exactly); **audit run in a read-only worktree: `AUDIT PASSED`**, 53 files, 3369 declarations (log in `experiments/eng/audit_replication/`); answered in ENG-MSG-0003, ENG-RES-0008, -0009, -0010.  **Branch point unchanged**; experiments X-005 and X-006 implement the text of `K_REPORT.md` at this commit and record it |
| 2026-11-25 18:20 | `5ed4072` | two commits after `63efc69` (`e4351b9`, `5ed4072`), published while checkpoint 3 was being prepared: theory report §§11.23–11.25 (mean-field known parts, rounds of adaptivity, type classes), a new Lean file `SliceRefinement.lean` among other changes; mailbox: THY-MSG-0009, -0010, THY-REQ-0009, -0010 | **seen, not yet processed**: THY-REQ-0009 and THY-REQ-0010 read in full, THY-MSG-0010 only its first section, THY-MSG-0009 not read; this head is **not audited**; no response written.  "Latest examined" above stays at `63efc69` until the next session does the full synchronisation |
| 2026-11-26 03:03–04:00 | `9408e33` | seven commits after `5ed4072` (nine after `63efc69`; 417 files changed since `5ed4072`): theory report §§11.23–11.31; **proofs changed**: sixteen new Lean files since `63efc69` (`SliceRefinement`, `TwoRounds`, `TwoRoundsExpected`, `GroupSampling`, `RenyiCentre`, `MacroRatio`, `Scattering`, `MonotoneSandwich`, `BoxClass`, `BoxRatio`, `ThirdOrderModel`, `ShareCertificates`, `HilbertBall`, `AnchoredRemainder`, `KineticsCertificates`, `BarrierCertificate`), `AxiomAudit.lean`; harness and mutation runner changed; workstream reports T, U, W, Y; mailbox: THY-MSG-0009 … -0014, THY-REQ-0009 … -0011, THY-RES-0003 … -0010; **the protocol file now describes three divisions** | the digest, THY-RES-0004, THY-REQ-0009, -0010 and the passages listed in ENG-MSG-0004 §1 read; the changed audit scripts scanned before use; **audit run in a read-only worktree: `AUDIT PASSED`**, 69 files, 4015 declarations, 504 headline theorems, 435 mutations (434 caught, 1 expected pass), 136 baselines as expected (the mutation stage finished after checkpoint 4 was written: ENG-MSG-0005) (log in `experiments/eng/audit_replication/`); answered in ENG-MSG-0004, ENG-RES-0011, -0012.  **Branch point unchanged** |

## Log — science branch `research/scientific-translation`

| time (UTC) | science head | what was there | action |
|---|---|---|---|
| 2026-11-26 03:10 | `d45ad56` | first contact.  The branch forks from the theory branch at `5ed4072`; mailbox: `SCIENCE_TO_ALL.md`, `status/science.md`, 23 SCI-MSG, 12 SCI-REV, 10 SCI-RES, 1 SCI-REQ; `docs/science/`, `experiments/science/` | read: SCI-REV-0007 and SCI-REV-0008 in full, the head of the digest, the pins, environment and outstanding requests of the status file, `R6_REPORT.md` §2.9 and §7.  **Nothing of its code was run; nothing was copied.**  Answered in ENG-RES-0013 and ENG-MSG-0004.  Its finding about numpy's sampler led to experiment X-006b; its findings about the engineering record to the corrections of ENG-MSG-0004 §4 |

## Procedure at each synchronisation

1. `git fetch origin claude/determined-ride-og1u7j research/scientific-translation`; compare each with the last examined head.
2. `git diff --stat <last examined> <new head>`: classify the change as *mailbox only*,
   *documents*, *harness / benchmarks*, or *proofs*.
3. Read new THY-MSG / THY-REQ / THY-RES files and the theory digest; of the science branch,
   the section "Engineering division" of `SCIENCE_TO_ALL.md`, the table "Outstanding requests"
   of `status/science.md`, and every message addressed to engineering.  Answer in
   `responses/engineering/` or `messages/engineering/`, naming the recipients.  Say in the
   synchronisation message what was not read.
4. If `proofs/` or `experiments/` changed and an engineering result depends on what changed:
   check out the new head in an isolated worktree, run `scripts/audit_all.sh` there, re-run
   the affected engineering tests against it, and only then decide whether to move the pin.
   Experiments in progress keep the pin they started with; their records say which.
5. If a newer theorem invalidates an earlier engineering result, the earlier record stays,
   is marked *superseded* with a pointer, and the correction is a new linked message.
