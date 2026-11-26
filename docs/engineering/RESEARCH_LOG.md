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
   evaluator and agrees with it; job M-011: 585 000 runs with the theorem's `K` without a
   single failure of any kind, and 468 000 runs with `K` divided by 4 … 256 — the good event
   starts to fail at `K/4`, the first invalid brackets appear at `K/64`.
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

## Session 3 — 2026-11-26 (UTC), 03:00 onwards

### 3.1 Authorisation and limits (research owner, this session)

* The owner answered the open question of session 2: the workspace's usage limit cannot be
  changed for this programme; the credit line is to be respected as it stands (`$1,990.63`
  left of `$2,030.00` on the billing page the owner showed), and whether this division's own
  stop line should be lower or higher is left to this division.
* What followed (`COMPUTE_LEDGER.md`, "Policy", rule 3): the stop line stays at `$1,500` of
  workspace usage and now *includes* the worst case of the job about to be launched, checked
  immediately before every launch.  Nothing was changed on the platform; the Modal CLI has
  no command that changes a budget, and none was looked for beyond `modal billing --help`.

### 3.2 Synchronisation: the theory head `9408e33` and a third division

* The theory branch had moved nine checkpoints (`63efc69 → 9408e33`).  Its protocol file now
  describes **three divisions**: a "Scientific Discovery, Translation & Independent
  Validation Division" on `research/scientific-translation`, introduced by the research
  owner on 2026-11-25 according to that file.  The instructions of this division name one
  collaborator; the third was adopted as described in ENG-MSG-0004 §5 — same rules, more
  mail.  Its branch had 46 messages, among them two reviews of engineering work
  (SCI-REV-0007 in part, SCI-REV-0008 in full) and about thirty requests to engineering.
* What was read and what was not: ENG-MSG-0004 §1.  The audit of `9408e33` on this machine:
  ENG-MSG-0004 §2.
* The theory division had answered checkpoint 3 (THY-RES-0004): the flat-instance cost
  table is now labelled as a best case in its report, with the engineering numbers; the
  sample cap `M̄` can be lowered to `2·max{e^λM†, M‡}` (their proof); the reduction of
  ENG-RES-0008 §5 was checked and stands.

### 3.3 What was done, in order

1. **The sampler** (highest priority: a published frequency depended on it).  The science
   division's report that numpy's binomial sampler is biased for counts drawn from `10¹⁷`
   trials and more was reproduced, and found to start near `10¹⁵` and to affect the variance
   before the mean (`binomial_bias.py`).  The stored runs of X-006 were shown to have drawn
   from blocks of up to `2.7·10¹⁷` points in two of three sizes.  An exact sampler was
   written (`sampling.py`: Poissonisation with collision thinning), tested against exact
   laws, and all 585 cases were run again (X-006b, job M-012, $1.01): **no statistic
   changes beyond sampling error.**
2. Folded into the same job: an **invalid inner behaviour** (the science division's R6-E2).
   The cost stays below `C_max` in all 78 000 runs; the abort rule fires in one
   configuration of twelve.
3. **The lowered cap** tested on every stored instance of X-005 and on the literal runs:
   no sample reaches half of it.
4. **The science division's finite-size separation table** (`C_max` against the
   non-adaptive lower bound) recomputed from the definitions: identical in all 72 numbers;
   on a finer grid the crossover is not monotone in `n` (X-009).
5. **THY-REQ-0010, question 2** (X-008): exact values to `n = 10 000`; the limits are
   approached from above with excess `≈ 0.45·ln n/n`; for `κ ≠ ½` the best centre is outside
   the class at every size from 40 on.
6. **The record** — five corrections, each found by the science division and verified here
   (ENG-MSG-0004 §4): the sampler; the two-solver validation (withdrawn); "certified lower
   bound" (10 of 25 open brackets are solver bounds); "about like `1/√n`" (the effective
   exponent is 0.63–0.76); three numbers computed from rounded entries.
7. Requests answered: THY-REQ-0009 (ENG-RES-0011, accepted, not started), THY-REQ-0010
   (ENG-RES-0012), the two reviews (ENG-RES-0013), THY-RES-0004 and the synchronisation
   (ENG-MSG-0004).
8. Job M-013: the convergence control at the two largest sizes of X-005 that the science
   division asked for (R7-ENG-4).  Outcome: ENG-RES-0014 §5.

*After checkpoint 4 (`c2ad4f8`), towards checkpoint 5:*

9. The audit of theory `9408e33` finished: `AUDIT PASSED` (ENG-MSG-0005).
10. **The evaluator generalised** for what three levels need: where each rung's bracket
    puts the value (`positions`), the exact classification threshold
    `c = max_l min(b − A_l, B_l)`, `θ` and `δ` as logarithms.  Validated against literal runs.
    On the way a suspected modelling error (item 3.4 below) turned out to be unreachable:
    all 2 624 stored maximisers of X-005 evaluate identically.
11. **Three nested levels at the flat instance**: the referee's 48 published numbers
    reproduced to the digit, on the first run of new code (X-010).
12. **Three levels at the worst outer landscape** (`u = 1`, three sizes): flat fibres (a real
    instance), cone fibres (real, adversarial, and a product instance for every split), and
    the middle level charged its own cost bound.  ENG-RES-0014 §3.
13. **Instances that are not products** (the first objection of SCI-REV-0008 §4): a bound by
    the union of refinement windows over all places of a fibre, evaluated at the stored
    maximisers and used as a search objective (job M-014).  ENG-RES-0014 §4.

### 3.4 Mistakes made and what they changed (kept on purpose)

* **A random-number routine used outside the regime in which it had been tested**
  (`DEAD_ENDS.md` ED-8).  The only test of the sampler had a resolution of 3–4 % where the
  defect is below 1 %.  Found by another division.  Rule: test a sampler at the largest `n`
  and at the means that matter, against exact moments, before publishing a frequency.
* **A validation claim that the committed code could not regenerate** (the two-solver
  sentence).  The rows had been written by a driver that was replaced after job M-004 was
  stopped; the sentence survived the replacement.  Rule adopted: result rows carry the
  commit and the job that produced them (from X-006b on), and a validation claim is
  re-derived from the stored files when the code that produced them changes.
* **A lower end described as "certified" that was the larger of two bounds.**  The table
  generator took the maximum; the prose described one of the two.
* **The digest said "about like `1/√n`" where the message it indexed did not.**  A digest
  line is prose with numbers and gets no generated table; it is now checked against a
  generated block (`trend_fit`) like any other sentence.
* **Three numbers computed from rounded table entries**, although session 2 had made the
  rule that numbers in prose come from artifacts.  The rule was followed for tables and
  summary sentences and not for arithmetic done on them by hand.
* **A false alarm that cost an hour and was worth it.**  While generalising the evaluator
  it became clear that the published mean runs classified sample points by a convention
  (`W > s e^{−b}` or `W > s`) and not by the brackets the algorithm holds, and that the two
  differ when a fibre's value lies within the tolerance of an end of its trivial bracket.
  A first count said 825 of the 2 624 stored maximisers sat in that corner — because the
  stored field `c_in` had been read as `t₀` (it is `t₀ − u n_i`).  Read correctly, none does,
  and none can: a Lipschitz fibre has `t₀ ∈ [n_i(u − Λ₁), n_i(2u − Λ₁)]`.  The literal runs
  that "disagreed with the old convention" had used infeasible `t₀`.  What remains: the
  exact rule in the code, a test that the search family cannot reach the corners, and a
  recheck file.  Lesson: before announcing a defect in published numbers, re-evaluate the
  stored instances — it took two minutes and was done second instead of first.
* **`pkill -f <script name>` killed the shell that issued it** (the pattern occurs in its own
  command line), although the memory of session 2 says exactly this.  Processes are now
  stopped by PID.
* **Local runs started from an uncommitted tree** would have stored a commit that does not
  contain their code; they were stopped after six minutes, the code committed, and the
  runs restarted.  Rule: commit before launching anything whose rows carry a commit.
* **An estimate off by a factor five**: the local placement-free search was planned at 17
  minutes and was heading for 90; it went to Modal instead.
* In this session: a factorial table off by one (`gammaln(j)` for `ln j!`), caught at once by
  the exact cross-check; `resolution of 12 %` typed into ED-8 before computing it (3–4 %);
  a first draft of ENG-RES-0013 that said the exposed cells went "down to `K/64`" before
  the exposure table existed (it is every value of `K` at one size and down to `K/16` at
  the other); `modal run` on an app with two entry points without naming one.

### 3.5 Open observations that are not yet results

* The exact values of X-008 exceed the limits by `c·ln n/n` with `c` between 0.44 and 0.47 for
  `n ≥ 1000`, as a density `q* ≈ C·n^{−1/2}e^{−nθ}` would give; whether the power is ½ is open.
  The best centre type at `κ = 0.4` and `0.3` is near `0.455` and `0.405`: numbers the theory's
  closed form can be held against.
* At `u = 1`, `n = 64 000` and `128 000`, `φ = 0.5`, the optimiser gains `0.0035` and `0.0031·na` over
  the best structured instance, against `0.0005` and `0.0004` at `n = 16 000` and `32 000`
  (`x005_seeds.json`).  Either the structured family misses something at these sizes or
  the reduced budgets did not converge; job M-013 was launched to tell.
* The inequality `C_max < LB_na` is not monotone in `n` near its crossover (integer effects
  of `R` and `⌊φn⌋`).  Any statement "from `n₀` on" for it needs a proof or a grid without
  gaps.
* numpy's defect depends on the bits of `n` (nothing at `2⁵⁰`, `2⁵²`; present at `10¹⁵`, `2⁵³`):
  consistent with a cancellation in the acceptance test of its rejection sampler; not
  confirmed in the source.
* Three levels: on a cone fibre the middle level can cost `e^{30}` times what it costs on a
  flat fibre at the same rung (`n = 1000`), yet the three-level total moves little, because
  the rungs where that happens are not the ones that dominate.  Which rung dominates, as
  a function of the outer fraction, is the thing to understand before designing the
  middle level against the worst case instead of at the flat fibre.
* For the base bracket K0 on a non-flat fibre the evaluator uses the two extreme valid
  placements; K0's own placement at the level of expectations is computable and would
  remove an adversarial freedom the real procedure does not have.

---

## Resume here

State at the end of session 3: see `docs/collaboration/status/engineering.md` for the table
of requests (two other divisions now); the list below is the order of work
(ENG-MSG-0004 §6).

0. **At the start of every session:** `git fetch origin claude/determined-ride-og1u7j
   research/scientific-translation`; follow `docs/collaboration/UPSTREAM_SYNC.md` for both;
   read new THY-/SCI- messages addressed to engineering (the science digest
   `SCIENCE_TO_ALL.md` has a section "Engineering division"); read `COMPUTE_LEDGER.md`
   ("Policy") before any remote job; `modal app list` must show no engineering app
   running.  If job M-013 is not marked completed in the ledger, its rows are in
   `experiments/eng/twolevel/results/x005_converge2.jsonl` (the job resumes from that file)
   and its outcome still has to be written up (table block `converge` takes them once
   `make_tables.py` reads the file).
1. **THY-REQ-0001, what is left** (the theory division's first wish, THY-RES-0004 §7):
   (a) **three levels at the worst instance.**  Design: a nested mean run in which, at
   every rung, the cost of an inner call and the position of the fibre average inside
   the returned bracket come from a two-level mean run on the fibre.  First deliverable:
   the sandwich "inner cost = flat instance" / "inner cost = worst instance per rung"
   at one slope and three sizes; read `experiments/reviews/R8/r8_flat3.py` on the theory
   branch for the design of the middle level first.  The evaluator needs a per-rung
   position `t_l` instead of the two oracles "bottom"/"top" (Python reference first, then
   the C kernel).  (b) **Instances that are not products**: fibres at different places of
   their trivial brackets (per-atom `t0` in the law of the outer landscape) — the first
   thing a hostile referee would attack (SCI-REV-0008 §4).  (c) the extensive regime of
   §11.18 (`Params.theta` must become a logarithm first).  (d) real inner brackets
   (`DEAD_ENDS.md` ED-7) with the batched schedule of Theorem 11.84 **and its stopping
   rule** (THY-MSG-0013 §3).
2. **The off-lattice chain in exact arithmetic over `ℚ[cos θ]`** (SCI-REV-0008, R7-ENG-3;
   specification in the science branch, `docs/science/workstreams/R7_REPORT.md` §7, not
   read yet).  Nothing off-lattice at 13 torsions or beyond before it.  Then what is left
   of THY-REQ-0002, with both lower ends printed and the covers stored (R7-ENG-2), and a
   certified branch and bound for the nine optima that rest on one solver (R7-ENG-5).
3. **THY-REQ-0003** in the revised design of ENG-RES-0003, remainder `η(1 + ‖λ‖₁)`.
4. Small accepted items: SCI-REV-0004 §6 (three proposals at the cone with a field);
   SCI-REV-0010 R10-E1 (vertices of two weighted cubes); the design search of
   ENG-RES-0013 §3 if the science division wants it.  None of the three messages has
   been read beyond its request line.
5. THY-REQ-0009 (plan in ENG-RES-0011); THY-REQ-0010 questions 1 and 3; THY-REQ-0007
   (ENG-RES-0010); THY-REQ-0008 items 1–4 together with the science division's
   enumeration requests (class tables of bridges, full pair-distance histograms: one
   remote job, to be bounded in the ledger first).
6. **E-1** in the form the science division gave it (the native kernel against
   pseudo-Boolean proof logging), with THY-REQ-0004; then the checker of SCI-MSG-0020 §6.
7. The science division's requests on real peptides (rotamers, an implicit-solvent
   energy): inside the scope the research owner authorised (fixed-sequence structural
   characterisation; no sequence design, no optimisation of function), but each needs
   external inputs that must be reviewed before use; none has been read.  Decide per
   request after reading.

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
