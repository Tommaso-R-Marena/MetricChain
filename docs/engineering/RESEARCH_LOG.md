# Engineering research log (Computational Research Division)

Branch `research/ubuntu-engineering`.  Newest entries last.  This log, the experiment
register, the compute ledger and the mailbox under `docs/collaboration/` are meant to be
sufficient to resume the work without any conversational context; **"Resume here" at the end
is the handoff.**

---

## Session 1 — 2026-11-25 (UTC)

### 1.1 Environment and repository

* Verified in this session: Ubuntu 26.04 LTS under WSL2, 8 threads, 7.6 GiB RAM, 2 GiB swap;
  Python 3.12.16 in `~/.venvs/metricchain` (NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0, pandas
  3.1.1, CVXPY 1.9.3, scikit-learn 1.9.1, NetworkX 3.7, Hypothesis 6.170, pytest 9.2,
  Matplotlib 3.11, PyTorch 2.15.0 CPU, Modal 1.6.4, mpmath 1.3.0); uv 0.13.10; elan 4.4.0;
  git 2.53; gh 2.46 (authenticated; admin on the repository); gcc 15.2; cmake 4.2.
* **Disk.**  The WSL filesystem reports 916 GB free, but the Windows host drive has **179 GB**
  free.  The host figure is the real limit.
* Installed in this session, project-local: Lean toolchain `leanprover/lean4:v4.31.0` (through
  elan, selected by `lean-toolchain`); Mathlib `v4.31.0` cache (`lake exe cache get`, 7.3 GB in
  `.lake/`, git-ignored); `ortools 9.15.6755` in the research venv.  **Side effect:** OR-Tools
  pinned `protobuf` from 7.36.2 down to 6.33.6; Modal 1.6.4 accepts `protobuf < 8` and was
  re-tested (`uv pip check` clean; CLI and API calls work).
* Repository: public; the theory branch is the default branch; there is no `main`.  This
  branch was created at `d81eb8a` (the commit the theory division names as its verified
  state).  Commits are authored with a repository-local identity `Claude
  <noreply@anthropic.com>`, the same as the theory branch, so that no private e-mail address
  enters a public repository.
* **Convention forced by the upstream audit:** `scripts/check_doc_refs.py` treats backticked
  identifiers in `docs/*.md` as Lean declaration names.  Engineering documents therefore
  live in `docs/engineering/` and `docs/collaboration/` (not scanned), never in `docs/`
  itself.

### 1.2 Reading of the theory branch (what was read, in what depth)

Read in full: root `README.md`; `docs/BLUEPRINT.md`; theory report §§0–1 and §12; research
log cycles 9–10; `docs/workstreams/A_REPORT.md`; `P_REPORT.md` §§0–2.2, 3.1–3.3; the whole
mailbox of the theory branch at `1bff191`.  Read as headings and by search: the rest of the
theory report (§§2–11), `DEAD_ENDS.md`, the Lean sources (declaration lists of
`CertificateAlgebra.lean`), the audit scripts.  **Not read:** referee reports R1–R6 and the
reviews of the workstreams (known only through their summaries in the research log), the
prior-art files, workstream reports B–H.  Anything in those that contradicts an engineering
statement has not been seen.

### 1.3 Independent assessment (the short version; the long one is ENG-MSG-0001)

One strong negative result (first-order uncertainty is exponentially expensive; per-torsion
envelopes cannot certify long chains) and one constructive hypothesis (linear-in-features
classes; pair-distance profiles for chains) whose premises nobody had measured.  The
computational division's comparative advantage is on the second.

### 1.4 What was done, in order

1. **Audit replication** (X-001; ENG-RES-0005).
2. **Lattice chains** (X-002; ENG-RES-0002): a C enumerator written from the definitions,
   validated against an independent internal-coordinate construction and against every
   published number it could be compared with; class tables to 24 torsions; exact covers;
   entropy brackets; all trans/gauche patterns (with a two-line proof); single-flip
   constants and the exhaustive envelope test.
3. **Uniform-cube hitting numbers** (X-003; ENG-RES-0006): closed form via Harper, brute
   force for `n ≤ 4`; pricing reformulated as closure + one budget row (not implemented).
4. **Mailbox**: README (engineering copy), sync log, status, digest, ENG-MSG-0001,
   ENG-RES-0001…0006, ENG-REQ-0001.  **Checkpoint 1 published: commit `206fd9e`.**
5. **Lattice covers for 19–24 torsions** (job M-005) with time limits and rigorous brackets;
   tables of ENG-RES-0002 regenerated in place (change note: ENG-RES-0007).
6. **Synchronisation with the theory head `4cef47e`** (referee report R7 on §11.18 integrated
   there; new Lean file): THY-MSG-0003/0004 read; the audit repeated on a read-only worktree
   of that commit — `AUDIT PASSED`, 46 files, 3101 declarations; pin policy decided (no
   merge; pinned read-only worktrees of the theory branch); plan for THY-REQ-0001 revised.
   (ENG-MSG-0002)
7. **Generic (off-lattice) chain** (X-004; ENG-RES-0007): enumerator from internal
   coordinates; all published counts and 16 published covering numbers reproduced; two
   published brackets at 10 torsions closed; extended to 12 torsions; tie analysis of the
   floating-point cover relation.  **Checkpoint 2 published** (the commit that adds
   ENG-RES-0007).

### 1.5 Mistakes made and what they changed (kept on purpose)

* **Two numbers were typed from memory into a draft of ENG-RES-0002** (conformation counts
  at 19 and 20 torsions, and a class count) and were wrong.  Caught before publication by
  re-reading the raw outputs.  Consequence: every table of that message is now generated by
  `experiments/eng/chain_cover/make_tables.py` from the artifacts, and
  `make_tables.py --verify <file>` fails if a table in the document differs from them.
  The same draft contained three sentences that the data did not support (a growth
  exponent, a comparison with the per-torsion format extrapolated beyond the published
  size, and a linear envelope for the single-flip constants that the second constant
  already violated); all three were corrected against the numbers.
* **A covering job was launched without time limits** (M-004): the reduced set-cover
  instances stop being small at 19 torsions for `L = 1`, and six containers ran for 22
  minutes without finishing before being stopped by hand.  Consequence: every integer
  programme now has a time limit, and the result is a rigorous bracket (certified dual
  lower bound, verified cover) when a solver does not prove optimality.
* **Local CPU was oversubscribed** (Lean build, enumerations, harness and a solver at once):
  nothing failed, but a covering run that takes seconds stalled for ten minutes.  Heavy
  local jobs are now run one at a time, and anything parallel goes to Modal.
* **A second job was launched with limits that could not finish in time** (M-006: 300 s per
  integer programme on instances where every programme uses its full limit).  Stopped by
  hand after 13 minutes and relaunched with 90 s (M-007).  Before launching a job whose cost
  is "number of cells × time limit", multiply it out.
* **Message headers carried drafting times, some later than the commit that published
  them.**  Corrected to the publication time and announced in ENG-MSG-0002 §5.  New messages
  refer to their commit instead of a typed time.
* `pkill -f <pattern>` matches the shell that runs it when the pattern occurs later in the
  same command line; twice a command killed itself.  Processes are now stopped by PID.

### 1.6 Open observations that are not yet results

* The farthest-point traversal count `m(δ)` of `P_REPORT.md` §3.2 is not a well-defined
  quantity (start and tie-breaking unspecified); exact covering numbers at `δ = ¼` are up to
  2.3 times smaller than our traversal counts.
* At `L = 1/5` every lattice covering number computed is at most 7.  The interesting regime
  of the lattice model is `L ≈ e` (the excitation energy), not small `L`.
* On the "generic" chain some profile distances are exact integers (five exact ties at 11
  torsions, e.g. 12.999999999999998 against 13): sums of differences of squared distances
  of this chain satisfy exact identities.  Harmless here (ties are counted as covered and
  reported), but any future *exact* treatment of the off-lattice chain should expect them.
* Off-lattice the optimum cover is a large fraction of the classes (215 of 639 at 9
  torsions), dominance reductions remove little and the integer programme does not close:
  beyond 12 torsions a primal heuristic plus the certified dual bound is the method, not
  exact branch and bound.
* The reduction "cover on classes with radii `gmin + ε`" works only for the zero residual
  and a known part that is a function of the gauche count.  A random member of the class
  as residual (the workstream's `κ = ½` rows) needs conformations, not classes.

---

## Session 2 — 2026-11-25 (UTC), 14:50 onwards

### 2.1 Authorisation and limits (research owner, this session)

Three statements of the research owner, all recorded in `COMPUTE_LEDGER.md`: (i) the Modal
allocation is prepaid credit, about $1,995 remaining, a **hard ceiling**, with no obligation
to use it ("use it as you see fit and when appropriate, not just using compute for the sake
of using it"); (ii) no platform limit enforces that ceiling (the workspace usage limit is
higher than the credit), so it is enforced by the ledger; (iii) the workspace allows **100
concurrent containers** and 10 GPUs, shared with other projects.  Rules derived here: worst
case of every job computed before launch; at most 50 containers in total; one job at a
time; stop launching at $1,500 of cumulative workspace usage.

### 2.2 Synchronisation with the theory head `63efc69` (17 commits after `4cef47e`)

Read: THY-MSG-0005…0008, THY-REQ-0007, -0008, THY-RES-0002 (and -0001 in part), the digest
and status, `K_REPORT.md` §§0–3.4 and §6.  Audit on a read-only worktree: `AUDIT PASSED`
(53 Lean files, 3369 declarations).  The theory division changed four of its statements on
the strength of ENG-RES-0002/-0007, answered ENG-REQ-0001 in full (limit shape for bridges;
plateau between 50 and 3 627, reached at `10³`–`10⁵` beads), redirected THY-REQ-0001 to
Algorithm 2L⁺, and sent two new requests.  Answers: ENG-MSG-0003, ENG-RES-0008, -0009, -0010.

### 2.3 What was done, in order

1. **An independent evaluator of Algorithm 2L⁺** (X-005), from the text of `K_REPORT.md` §2:
   cube tables (checked against exact integers), the constants of Theorem 11.56, the base
   family, the mean run in Python (reference) and C (kernel, about a hundred times faster), and — new —
   the exact number of evaluations on any instance for two explicit inner behaviours.
   Controls: 324 rows of the workstream's radial table and 18 rows of its flat-instance
   table reproduced.
2. **Adversarial search** (jobs M-008, M-009, M-010): 468 cells `(u, n, φ)`; no claim of the
   theorem violated; **the flat instance is not the worst one at finite `n`**; the best outer
   fraction against the worst instance is 0.50–0.60; the crossover with the plain bracket
   moves; no persistent margin over the claimed exponent.  ENG-RES-0008.
3. **A reduction** (ENG-RES-0008 §5): by Harper's theorem the laws of `W` on the outer cube
   are exactly the tail functions with `m(te^{−u}) ≥ ∂(m(t))`; monotone radial profiles are
   those with ball level sets.  Unrefereed.
4. **A literal sampled implementation** (X-006) that shares only the tables with the
   evaluator and agrees with it; job M-011 for statistics with the theorem's `K` and with `K`
   scaled down.
5. **A tie pitfall with a structural cause** (ED-5): a literal run aborted on the good
   event; fixed by an exact tie rule; two published rows of the workstream's table turn out
   to be decided by rounding.
6. **THY-REQ-0008, items 5 and 6** (X-007): single-flip constants satisfy Proposition 11.74
   in all 36 cases; the off-lattice distance entropy still rises at 14 torsions; the
   off-lattice enumerator reproduces the published counts at 13 torsions (113 587 / 13 012)
   and gives 273 623 / 27 421 at 14.  ENG-RES-0009.

### 2.4 Mistakes made and what they changed (kept on purpose)

* **Job M-008 was launched with a cap of 100 containers — the whole workspace limit.**  The
  limit was not known here, but the cap was chosen without asking what else runs on the
  workspace, and for about 20 minutes nothing else could have started a container.  The
  research owner pointed it out.  Consequence: rule 5 of the ledger (at most 50 containers,
  one job at a time).  The job was left to finish because stopping it would have discarded
  the in-flight work of its largest tasks; that was a judgement call made while the owner
  was watching, and said so to the owner.
* **Prose written before the numbers were checked, again.**  The first draft of ENG-RES-0008
  said the worst case is "20–90 %" above the flat-instance table at `n ≤ 2000` (it is 11–49 %),
  described the maximisers as a class that a count then showed to be 59 of 468 by the
  classifier used (ED-6), and misstated the number of test runs; the draft of ENG-RES-0009
  said two statistics differ "by less than 0.02" (it is up to 0.05) and carried one mistyped
  table digit, which `make_tables.py --verify` caught.  All were corrected before
  publication by recomputing each sentence from the artifacts.  The rule of session 1
  (tables are generated) is not enough: **summary sentences are now generated too** where
  they carry numbers that later jobs can change (`headline_counts`, `closest`), and every
  remaining number in prose is checked against a printed table before the message is
  committed.
* **The session's working directory moved into the read-only theory worktree** when a
  command ended there; the harness then described the worktree as the place to work.  No
  file was changed in it.  Commands that touch the worktree now use `git -C` or a subshell.
* **Run times were estimated a factor two too high, then a factor two too low**, from one
  timing at `u = 1`: the number of levels scales with `u`.  Estimates are now per `u`.
* **The first version of the law of `W` was normalised to `1 − 10⁻¹²`**, which made the lowest
  levels look "not populated at the first pass"; found because the numbers of populated and
  negligible levels did not match the published rows while everything else did.

### 2.5 Open observations that are not yet results

* In more than five million instances the sample of the outer loop stayed below `2M†`, far
  below the theorem's bound `M̄ = 2(1+η)e^λ ν₀ M†`.  Either `M̄` can be lowered by a factor of
  order `ν₀`, or the instance that needs it has a level set that is not a ball (partial
  shells) — the search cannot tell.
* The count (v) of the theorem is tight to 5 % under the inner behaviour that puts the
  value at the *top* of the bracket, and only to 42 % under "bottom".
* The best outer fraction against the worst instance is `½` up to the grid, at every size:
  the two branches of the cost, `(1−φ)a` and `φa`, carry corrections of the same form.
* Three nested levels: the evaluator can be nested (the inner cost of a rung becomes a
  mean run on the fibre), but the design of the middle level at each accuracy has to be
  taken from the referee's script (`experiments/reviews/R8/r8_flat3.py`, not read).

---

## Resume here

State at the end of session 2: see `docs/collaboration/status/engineering.md` for the table
of requests; the list below is the order of work.

1. **THY-REQ-0001, what is left** (ENG-RES-0008 "Decision"): (a) publish the table of job
   M-011 if it was not in checkpoint 3 (`python experiments/eng/twolevel/make_tables.py`, block
   `sampled`); (b) **three nested levels on non-flat instances** — read
   `experiments/reviews/R8/r8_flat3.py` and `docs/reviews/R8_referee_report.md` on a worktree of
   the theory head for the design of the middle level, then nest `Evaluator` (inner cost of
   rung `l` = mean run of the two-level algorithm on the fibre at accuracy `x_l`); (c) the
   extensive regime of §11.18 (`λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, `θ = e^{Gn−b} − …`): `Params.theta`
   must become a logarithm first, `θ` overflows a double at `n = 10⁵`; (d) real inner brackets
   beyond 13 coordinates in the form of `DEAD_ENDS.md` ED-7 (small outer cube, large inner
   cube, a few hundred runs).
2. **THY-REQ-0003** in the revised design of ENG-RES-0003, with the remainder
   `η(1 + ‖λ‖₁)` as confirmed in THY-MSG-0005 §3(b).
3. **THY-REQ-0002, what is left**: covers of the generic chain at 13 and 14 torsions (class
   tables exist; primal heuristic + `profile_cover.certified_lower_bound`), its questions
   3(a), 3(b), questions 4 and 5, sampling for question 2.
4. **THY-REQ-0008, items 1–4**: an optimiser over lattice walks (pivot, end moves, backbites;
   by the site-set lemma of THY-RES-0001 the profile depends on the site set only) with a
   recount from coordinates; walks against bridges; the plateau by set cover; bridge
   tables for 25–27 beads (the enumerator fixes the first two bonds by symmetry, and the
   bridge condition singles out one coordinate — read `S_REPORT.md` for the convention
   before restricting it).
5. **THY-REQ-0007** as fixed in ENG-RES-0010.
6. **E-1 / THY-REQ-0004**, then **E-2**.
7. At every session start: `git fetch origin claude/determined-ride-og1u7j`, follow
   `docs/collaboration/UPSTREAM_SYNC.md`, read new THY-MSG/REQ/RES, update the digest and
   status; read `COMPUTE_LEDGER.md` ("Policy") before any remote job; `modal app list` must
   show no engineering app running.

Worktree of the theory branch (read only; never end a shell command inside it):
`git worktree add --detach ../MetricChain-theory-<sha> <sha>`, then
`mkdir ../MetricChain-theory-<sha>/.lake && ln -s ../../MetricChain/.lake/packages ../MetricChain-theory-<sha>/.lake/packages && cp -a .lake/build ../MetricChain-theory-<sha>/.lake/build`,
and inside it `LEAN_NUM_THREADS=4 lake build` and `bash scripts/audit_all.sh --full`.

Build and test from a clean clone:

```
source "$HOME/.venvs/metricchain/bin/activate"; export PATH="$HOME/.elan/bin:$PATH"
lake exe cache get && lake build                     # theory proofs (about 50 min on 8 threads / 7.6 GiB)
mkdir -p build && cc -O3 -o build/dia_enum src/metricchain_eng/chains/dia_enum.c \
                && cc -O3 -o build/dia_flip src/metricchain_eng/chains/dia_flip.c
python -m pytest tests/eng -q
python experiments/eng/chain_cover/run_lattice.py --check
python experiments/eng/chain_cover/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0002.md
python experiments/eng/twolevel/controls.py --theory ../MetricChain-theory-63efc69      # needs a checkout of the theory branch
python experiments/eng/twolevel/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0008.md
```
