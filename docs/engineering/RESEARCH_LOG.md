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

## Resume here

State at the end of session 1: see `docs/collaboration/status/engineering.md` for the table
of requests and their status; the list below is the order of work.

1. **Finish THY-REQ-0002** (status table in ENG-RES-0007 §4): (a) generic chain beyond 12
   torsions — published targets 113 587 conformations and 13 012 classes at `n = 13`; the
   distance matrix needs about 1.4 GB at `n = 13` and the covers need a primal heuristic
   with the certified dual bound (`profile_cover.certified_lower_bound`), not exact branch
   and bound; a C port of the enumerator for `n ≥ 15`; (b) its questions 3(a) (all patterns
   realised? the directed-walk proof does not transfer, because the hard core removes
   `g⁺g⁻`) and 3(b) (single-flip constants); (c) question 4 (sum class `P_L + Lip(η·d_H)` on
   the 683-conformation lattice chain, `L = 1/5`, `η ∈ {0.5, 0.75, 1}`, known brackets `[2,2]`,
   `[2,6]`, `[2,17]`); (d) question 5 (span format off-lattice, `n = 10`, bracket `[3, 10]`);
   (e) question 2 by sampling, reported as entropy of sampled sets with the bias stated.
2. **THY-REQ-0001**, in the order of ENG-MSG-0002 §4 (real inner brackets end to end;
   non-radial outer laws; three levels; fluctuations; a small control of Part B).  Work
   against a read-only worktree of the theory branch at `4cef47e` or later:
   `git worktree add --detach ../MetricChain-theory-<sha> <sha>`, then inside it
   `mkdir .lake && ln -s ../../MetricChain/.lake/packages .lake/packages && cp -a ../MetricChain/.lake/build .lake/build`
   (the copy lets Lake rebuild only what changed), `LEAN_NUM_THREADS=4 lake build`,
   `bash scripts/audit_all.sh --full`.  First read: `docs/reviews/R7_referee_report.md`, the
   revised §11.18, and the harness functions `lv_two_level`, `lv_check_run`,
   `two_level_flat_cost` at that commit.
3. **THY-REQ-0003** in the revised design of ENG-RES-0003.
4. **E-1 / THY-REQ-0004**: Lean evaluator front-end for the kernels and the differential
   fuzzer; then the linear-kernel schema, checker and producer.
5. **E-2**: producer for `min` certificates and measurements at realistic sizes.
6. At every session start: `git fetch origin claude/determined-ride-og1u7j`, follow
   `docs/collaboration/UPSTREAM_SYNC.md`, read new THY-MSG/REQ/RES, update the digest and
   status.

Build and test from a clean clone:

```
source "$HOME/.venvs/metricchain/bin/activate"; export PATH="$HOME/.elan/bin:$PATH"
lake exe cache get && lake build                     # theory proofs (about 50 min on 8 threads / 7.6 GiB)
mkdir -p build && cc -O3 -o build/dia_enum src/metricchain_eng/chains/dia_enum.c \
                && cc -O3 -o build/dia_flip src/metricchain_eng/chains/dia_flip.c
python -m pytest tests/eng -q
python experiments/eng/chain_cover/run_lattice.py --check
python experiments/eng/chain_cover/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0002.md
```
