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
* **A check that could not fail.**  Between jobs, "no engineering app is running" was read from
  `modal app list --json` with the key names `State` and `Description`; the keys are `state` and
  `description`, so the filter matched nothing and the answer was always "none".  The check
  at the start of the session and the one at its end were written correctly (the last one
  also counts containers: 0); in between, the statement rested on each job's own
  completion line and on the billing report.  Nothing was running that should not have
  been — but the check did not show it.  Rule: a negative result is recorded only from a
  check that has been seen to give a positive one (here: run it while a job is up).
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
* **Three levels: the flat instance is the cheap case twice.**  Against the worst outer
  landscape a third level changes nothing above the balance point (the cost is the outer
  sample) and keeps its advantage below it; on cone fibres, with the base bracket's own
  answers, most of the advantage goes (three over two levels: 0.94, 0.92, 0.96 at
  `n = 1000, 4000, 16 000`, against 1.00, 0.82, 0.76 at the flat instance) and the flat
  instance understates the three-level cost by a factor near 1.4 that does not decay over
  this range.  The cause is in the table of ENG-RES-0014 §3: on a flat fibre the base
  bracket returns a bracket many times narrower than promised, on a cone it uses most of
  the promised ratio, and the referee's design chooses servers and splits at the flat
  fibre.  **Not known:** whether a middle level designed against wide brackets restores
  the advantage at these sizes; what a fibre landscape searched in full would add.
* The base bracket's answer on a general fibre is a functional of the fibre's weight law
  (`t̂` = a quantile, `Â = E min(w, t̂)`), so the two-level evaluator could carry it for any
  radial fibre, not only cones; then the two extreme placements "bottom"/"top" would be
  needed only for reading (A).

---

## Session 4 — 2026-11-26 (UTC), 15:11 onwards (in progress)

### 4.1 Directives of the research owner received in this session

Four, recorded in `docs/engineering/DIRECTIVES.md` (D-2 … D-5): mathematical generality
(relayed to all divisions in ENG-MSG-0006, complete text); a continuous research loop for
this division, with "the apparent deterioration of adaptive algorithm performance on
non-flat fibres" named in particular; six divisions; this division coordinates shared
Modal computation and benchmarking, with **$1,750 of additional Modal expenditure
authorised and $200 of credit to be preserved** (ledger, "Policy").

### 4.2 Synchronisation

Theory `8ff0667` → `020e990` (checkpoints 19–22 and work on the rate of the level
recursion; THY-RES-0012 … -0015 read as far as ENG-MSG-0006 §3 says); science `2b4ccdf` →
`af689cc` (SCI-RES-0015 read in full).  **Three new branches appeared at about 16:50 UTC**:
`research/ensemble-identifiability` (`a570520`), `research/geometric-inference` (`d84a43b`),
`research/biological-complexity` (`9a35d2f`); of them only GEOMETRY-REQ-0001 (addressed to
us) was read in full, and the lines of the three digests that mention engineering.

### 4.3 What was done, in order

1. ENG-MSG-0006 (the relay; replies; order of work).  Protocol copy, directives file,
   ledger policy rewritten for the new authorisation.
2. **X-011** (campaign BM-1): the certified-cost recursion as an exact pruned search
   (`certified.py`), seven published numbers of the theory division reproduced; a generic
   bounded Modal app with a detached mode whose results wait in a `modal.Dict`
   (`modal_jobs/bench_app.py`, `bench_collect.py`); jobs M-015 (smoke), **M-016** (bounds, nine
   sizes, up to six levels), **M-017** (the selected designs run on flat and adversarial
   instances; the theory division's R16-THY-1(b)); local: the design-versus-cone game
   (`portfolio.py`) and the per-rung anatomy (`rung_anatomy.py`).  Protocol with hypotheses
   committed before launch.  Draft: `docs/engineering/drafts/ENG-RES-0015.draft.md`.
3. **X-012** (BM-2): an exact checker of the science division's "shares at the leaves"
   certificates, by an independent subagent, checked by the coordinator (third
   implementation; tests re-run); `experiments/eng/leafcert/REPORT.md`.  One finding for the
   science division: their reference checker accepts a false bound on malformed input.
4. **X-014** (BM-6): site-dependent slopes — a transfer of Theorem K1 to outer blocks of one
   site type (`hetero.py`), exact lower bound, literal runs on small cubes
   (`hetero_literal.py`), job **M-018** (75 mixtures).  Draft:
   `docs/engineering/drafts/ENG-RES-0016.draft.md`.
5. Benchmark documents: `docs/engineering/benchmarks/` (master plan, registry = the shared
   queue, readiness, results, baselines, reproducibility, limitations, protocols).

### 4.4 Mistakes made and what they changed

* **Unbounded caches**: the first deep recursion kept every table and every node in memory
  (4.5 GB after ten minutes, on a machine with 7.6 GB shared with two subagents).  Killed;
  caches bounded; a test forces evictions and compares results.
* **`pgrep -f` / `kill` by pattern killed my own shell twice more** (the pattern also occurred
  elsewhere in the same command line).  Rule, again: find the PID in one command, kill it
  in another that does not contain the pattern.
* **The first lower bound of the literal simulator was wrong** (a wrong closed form for
  `Π(1 + e^{−u})/2`), then **its lower end dropped the certified sum** — the second error
  made brackets wider than certified, which the theorem forbids deterministically, and
  that is how it was found (ENG-RES-0016 §6).  Both were mine, in test code; the equality
  case (cone at the reference point) is now among the instances.
* **Times of day**: three documents carried times an hour late; corrected from the commit
  log.  ENG-MSG-0006's header says "written 15:15–16:15"; it was committed at 15:25.
* A draft sentence said the bounded design costs "within 0.05" on cone and flat fibres at
  every rung; the table says up to `0.13`.  Caught before publication by generating the
  table first.

## Resume here

**State at 2026-11-26 about 17:45 UTC (session 4 in progress).**  Read
`docs/engineering/DIRECTIVES.md` first: the research owner asked for a *continuous*
research loop; a finished checkpoint is not a reason to stop.

0. **At the start of every session:** `git fetch origin` (six branches now); follow
   `docs/collaboration/UPSTREAM_SYNC.md`; read new messages addressed to engineering in all
   five other mailboxes (`THEORY_TO_ENGINEERING.md`, `SCIENCE_TO_ALL.md`, `ENSEMBLE_TO_ALL.md`,
   `GEOMETRY_TO_ALL.md`, `COMPLEXITY_TO_ALL.md` on their branches); read `COMPUTE_LEDGER.md`
   ("Policy": the launch test) before any remote job.  Commit before launching anything
   whose rows store a commit; stop processes by PID.
1. **Remote jobs that may still be running or uncollected** (detached; results wait in a
   `modal.Dict` for seven days; the apps end by themselves):

       python modal_jobs/bench_collect.py --driver nested_bench --job certified1+instances1+instances2+certified2   # M-016, M-017, M-020, M-021
       python modal_jobs/bench_collect.py --driver hetero_bench --job hetero1+profile1          # M-018, M-022
       python modal_jobs/bench_collect.py --driver nested_literal --job nested1                 # M-019 (complete)
       modal app list --json      # keys state, description, tasks; ours are named metricchain-eng-*
       modal container list --json

   M-016's largest sizes (`n ≥ 32 000`) can run until 2026-11-27 04:20 UTC.  **Not yet
   launched (ledger says so):** the 3-hour tier of M-020 (`--job instances2 --tiers l`, after
   M-018 and M-022 have ended) and M-021 (`--job certified2`), each only while the total of
   running containers stays below 50.  After the last
   collection: enter the measured costs in the ledger (`modal billing report`), set the
   jobs to "done", update the allocation table, and check `modal billing summary` shows
   **Billed Cost $0.00**.
2. **Publish** `ENG-RES-0015` and `ENG-RES-0016`: move the drafts from
   `docs/engineering/drafts/` to `docs/collaboration/responses/engineering/`, run
   `python experiments/eng/twolevel/make_tables_x011.py --write <file>`, check every number
   in the prose against the generated tables (the drafts were written from partial data —
   the list of sentences to re-check is at the head of each draft's history in this log,
   §4.4), then `--verify`.  ENG-RES-0015 covers sizes up to 16 000; larger sizes go into a
   linked addendum.  Then a message ENG-MSG-0007: synchronisation with all five branches;
   to the science division the checker (X-012) and the finding about its reference
   checker; to the geometry division the answer to GEOMETRY-REQ-0001; to the three new
   divisions how to request computation (`docs/collaboration/README.md`, "Shared
   computation"; `benchmarks/BENCHMARK_REGISTRY.md`).
3. **Subagents** (their output is reviewed, then filed and committed by the coordinator —
   they do not commit; their reports come back as text and are filed as `REPORT.md` next
   to their code).  **Done and filed:** X-012 the leaf-certificate checker
   (`experiments/eng/leafcert/REPORT.md`); X-013 weighted cubes (R10-E1;
   `experiments/eng/weighted_cube/REPORT.md`).  **In flight at 2026-11-26 17:45 UTC:**
   (a) GEOMETRY-REQ-0001 items 1 and 3 (`experiments/eng/geometry_req1/`,
   `tests/eng/test_geometry_req1.py`); (b) a numerical check of the theory division's
   Theorem R on products of two site types (`experiments/eng/level_rate/`,
   `tests/eng/test_level_rate.py`); (c) an adversarial referee of ENG-RES-0016 §2
   (`experiments/eng/review_x014/`); (d) a producer of leaf certificates and its benchmark
   against exact solvers (`src/metricchain_eng/leafprod/`, `tests/eng/test_leafprod.py`,
   `experiments/eng/leafcert_bench/`).  If a session ends before they report, their files
   are in the working tree, untracked: review them like any contribution (run the tests,
   read the core, write the report from their code) or delete them.
4. **Then, in this order** (the registry `benchmarks/BENCHMARK_REGISTRY.md` is the queue):
   (a) X-011 continued — slopes `u = ½, 2` (Q-10); fibres that are hard for the *bounded*
   middle design (ENG-RES-0015 §7); a literal simulation of a nested run at small `n`
   (none exists);
   (b) the sandwich certificate checker (SCI-MSG-0025 §8; Q-08), now that the leaf checker
   exists, and a *producer* for leaf certificates so that BM-2 can reach stage D;
   (c) the off-lattice chain in exact arithmetic (R7-ENG-3; Q-06), then the enumeration
   job (Q-07);
   (d) X-014 continued — if §2 of ENG-RES-0016 survives its referee: alphabets of
   different sizes; an exact extremal function of small weighted cubes;
   (e) THY-REQ-0003 (profile constants; Q-09);
   (f) requests of the three new divisions as they arrive, by the readiness test.
5. Not done and not started: the audit of any theory head after `9408e33` (the science
   division reports passes up to `3cf14b9`); the theory division's report on the rate of
   the level recursion (`020e990`) and Theorem 11.58a are unread beyond summaries.

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
python experiments/eng/twolevel/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0008.md    # likewise -0013, -0014
python experiments/eng/slices/make_tables.py --verify docs/collaboration/responses/engineering/ENG-RES-0012.md
python experiments/eng/twolevel/three_levels.py --check                                 # the referee's three-level numbers
```
