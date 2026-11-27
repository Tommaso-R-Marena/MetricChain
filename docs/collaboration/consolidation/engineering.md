# Consolidation assessment — Computational Research Division ("engineering", "Ubuntu")

*Branch `research/ubuntu-engineering`.  Written 2026-11-27 under the research owner's directive
"Controlled Consolidation and Temporary Research Halt" (D-8 in `docs/engineering/DIRECTIVES.md`).
An assessment by the AI session that did the work; nothing below has had external review.  Where a
result was produced by a subagent and only spot-checked by the coordinator, the text says so.  This
division made **no literature search** of its own: statements about prior art are the coordinator's
general knowledge or cite another division's notes, and are weaker evidence than a search.*

**Scope note added 2026-11-27 about 05:30 UTC, while assembling the unified archive (directive D-9);
no new work, only what the other branches' final commits make necessary to say.**  (1) Wherever
this report and ENG-RES-0019 say "the six stored certificates" of the structural-biology division,
they mean the six files at the top level of `experiments/structbio/gmec_dev/certs/` on its branch —
its first energy model, which that division has since retired because of the random seed in it.
Those six files are unchanged at its final head `a5cc106` (the same git objects).  **The twelve
certificates of its later models (`certs/v2/`, `certs/v2-lib/`) were not checked by us**, neither
by our independent checker nor by the kernel.  (2) After our review that division repaired both
checkers (its commit `0e934eb`, 02:42 UTC); **nothing after `41fa668` has been tested by us**.  Its
own adversarial review records the float-tier defect at large `exp_bits` independently of our
finding F1, and its repair range-checks that parameter; whether our reproduction still succeeds on
the repaired code is not known.  (3) No other division had read ENG-RES-0019 or ENG-MSG-0008 when it
halted: the structural-biology report still lists its two requests as unanswered, and the theory
branch does not mention the run-time defect of the kernel.

**Note added 2026-11-27 about 19:00 UTC (directive D-10: final collection); the report below is
otherwise as written at the halt.**  (1) The two Modal jobs that §E, §G and §H describe as running
are closed.  33 of their 34 cells are stored; the cell `u = 1`, `n = 32 000`, family "wide" of job
M-016 has no row (restarted by the platform, stopped before it could return, not restarted).
Tables and outcomes: `docs/engineering/benchmarks/X-011_ADDENDUM.md`; costs: the ledger's "Final
reconciliation".  (2) §E says that these cells "answer hypotheses H12 and H13 when collected".
They answer less: H12 is refuted; H13(a) is refuted again at the larger sizes; H13(b) and H1 are
not decided there, because the searches with five and six levels ran into their time limits; H3
is refuted at two more sizes.  §C counts three pre-registered predictions that failed; with H12
they are four, and H3 and H13(a) fail at more sizes than §C says.  (3) Nothing in §B changes:
the new rows are bounds at sizes and slopes where no instance was run.  (4) The heading of the
scope note above read "about 05:40 UTC" until this commit; the commit that first contains it
was made at 05:30 UTC, and the heading is corrected.

## A. Executive assessment

This division proves nothing.  It computes, replicates and attacks: it re-ran the theory division's
audit at four of its heads, re-implemented the algorithms and certificate formats of other divisions
from their text, searched for instances on which their claims fail, and ran the shared Modal budget.
In defensible terms it has delivered:

1. **Independent replication** of the theory division's machine-checked audit (no divergence at
   `d81eb8a`, `4cef47e`, `63efc69`, `9408e33`; not repeated after that) and of every published number
   it was asked to reproduce.
2. **Finite-size, adversarial evaluation of the nested adaptive algorithm** (Algorithm 2L⁺, Theorem
   11.56/K1 of the theory report): no claim of the theorem broke; several statements *around* it did
   (the flat instance is not the worst one; a published cost table was too favourable; a fifth nested level gains at most a quarter of its asymptotic value at any size computed).
3. **Independent checkers and adversarial tests of certificate software**, ending on 2026-11-27 with
   the theory division's verified kernel *executed* on the structural-biology division's six stored
   certificates (it accepts all six), and with one soundness defect found in a non-default setting of
   the partition-function checker.
4. **Corrections**, including four of its own published statements, each found by another
   division's review or by its own referee subagents, and each corrected in a linked message.
5. **A bounded, ledgered compute service**: 25 Modal jobs for about $24 in all (about $16 of the $1,750 authorised on 2026-11-26), no paid charge.

What it has *not* delivered: any result with a claim to mathematical originality; any benchmark on
held-out data; any comparison with an external state-of-the-art tool other than toulbar2 called on
six instances; any evidence about proteins.  Its worst-case searches are heuristics, and one of them
is documented as not converged.

## B. Strongest contributions (five; ranked)

### B1. Independent verification of the certificate stack, up to executing the machine-checked kernel on real instances

* **Contribution.**  (a) Checkers written from the format descriptions, sharing no code with the
  originals, for three certificate formats: "shares at the leaves" (science; X-012), `structbio-mincert/1`
  (X-016) and `structbio-zcert/1` (X-018, by a subagent).  (b) Differential and adversarial testing:
  22 472 claims on random certificate trees with three checkers in agreement and no unsound
  acceptance, at two commits; 96 559 partition-function certificates on 3 000 enumerable instances
  with every accepted interval containing the enumerated truth at default settings.  (c) Defects found:
  one in the science division's reference checker (confirmed and repaired by it, SCI-RES-0030); three in the first structural-biology release (all repaired by that division before our report reached it; one of them is named in its own correction message); **a soundness defect of the float tier of the partition-function checker at `exp_bits` 990–991**
  (the returned interval misses `ln Z` by 0.31 nats; reproduced by the coordinator at `0544ff4` and
  `41fa668`; defaults unaffected); claim Z3 false as worded.  (d) **X-017:** the theory division's kernel
  `verify` cannot be run on a certificate with more than a few dozen eliminations in a chain — its time
  grows about 1.8-fold per elimination because the domains are nested function updates; a memoised
  twin `verifyM` is **proved equal to it in Lean** (`verifyM_eq`), and with it the kernel accepts the
  six stored protein certificates at exactly the witness's energy, refuses the bound plus one unit, and
  refuses three corrupted inputs.
* **Where.**  `experiments/eng/leafcert/` (commit `8df6e5e` and earlier), `experiments/eng/sb_review/`
  with `lean_kernel/RunKernel.lean`, `experiments/eng/sb_zcheck/`; ENG-RES-0018, ENG-RES-0019; tests
  `tests/eng/test_leafcert.py`, `tests/eng/test_sb_zcheck.py`.
* **Verification and review status.**  `verifyM_eq`: checked by Lean (a four-case induction).  The
  runs: executions by Lean's interpreter, not proof terms.  The `mincert` checker and its tests: the
  coordinator's own; unrefereed.  The `zcert` checker: a subagent's, 982 lines, *not read* by the
  coordinator; its most serious finding was reproduced directly.
* **Assumptions.**  The reader in `RunKernel.lean` builds the intended instance (cross-checked by
  digests over every index); the tables are the published ones (canonical SHA-256); everything is
  relative to the integer tables — the step from a real-valued energy to those tables is unproved in
  the whole programme.
* **Closest prior art** (general knowledge).  Proof logging with formally verified checkers:
  VeriPB with CakePB for pseudo-Boolean optimisation; VIPR certificates for exact SCIP; DRAT with
  verified checkers for SAT.  Proving an efficient checker equal to a specification-level one is the
  standard refinement method of that literature.
* **Distinction.**  None in method.  The object checked is this programme's own kernel and formats.
* **Evidence for originality.**  The structural-biology division's bounded search found no proof
  logging for cost-function networks or toulbar2 (`PRIOR_ART.md` §B on its branch).
* **Evidence against.**  Everything else: certified optimality by proof logging is established
  technology, and the comparison with it has not been run.
* **Validation.**  Six development structures (26–65 residues); synthetic instances; no held-out data.
* **Limitations.**  Interpreter trust; one author per checker; the instances are easy for toulbar2
  (0.006–0.64 s in our call).
* **Before publication or deployment.**  The proof-logging comparison (E1); a held-out run; a native
  executable of the kernel with the equality proof moved into the theory division's tree; an
  independent implementation of the energy tables.

### B2. What the nested adaptive algorithm keeps of its asymptotic gain at finite size

* **Contribution.**  A certified recursion for nested runs of Algorithm 2L⁺ with servers chosen by
  certified cost, evaluated to six levels at `n ≤ 16 000` (larger sizes still running), together with
  runs of the selected designs on searched instances in a mean-run model and literal simulations.
  Findings: from `n = 4000` on a third level keeps about four fifths of what it gains in the limit, a fourth between a half and six sevenths, a fifth at most a quarter (shares at `n = 16 000`: 0.81 / 0.86 / 0.23, the last from an incomplete search); below `n = 2000` even the third level keeps at most half; the overhead is 7–45 nats per level; designs chosen by certified cost have the
  smaller worst instance found once a nested run can be certified to pay (three slopes at `n = 16 000`:
  0.5259 against 0.5750, 0.4556 against 0.5525, 0.4520 against 0.5461 in units of `n a`), and below
  that size the flat-tuned design is cheaper on every instance found and guarantees less; the flat
  instance is not the worst one and the theory division's first cost table was too favourable
  (ENG-RES-0008).  In the stage-2 cells collected last (96 designs, 2 042 496 mean runs) no searched cost exceeded the certified bound of its design, as in the cells published before.
* **Where.**  `src/metricchain_eng/twolevel/`, `experiments/eng/twolevel/`; ENG-RES-0008 (`a9ef1b4`),
  -0013, -0014 (`a57c300`), -0015, -0017 (`8df6e5e`); protocol with hypotheses written before
  collection: `docs/engineering/benchmarks/protocols/BM-1_X-011.md`; jobs M-011 … M-025.
* **Status.**  Reviewed twice by the science division (SCI-REV-0007, -0008, -0018) and by referee
  subagents; the reviews found real errors (B4).  The certified bounds are computed in floating point
  from the theorem's formulas, not interval arithmetic.
* **Assumptions.**  The class `L_u(Q_n)` of the theory report; the mean-run model for the large
  sizes; "worst instance" means worst *found* by differential evolution over two radial families.
* **Prior art.**  The algorithm and its asymptotic exponents are the theory division's (Theorem
  11.56; workstream Z).  Whether adaptive schedules of this kind are new against the literature on
  adaptive annealing and nested estimators is the theory and science divisions' question; this
  division did not search.
* **Distinction / originality.**  Ours is the finite-size evaluation only.  For: nobody else in the programme computed it, and two of our pre-registered predictions about it failed (H3, H13(a)), which is a sign the numbers were not foreseeable.  Against: evaluating an asymptotic scheme at finite
  size is routine, and the result is specific to this algorithm.
* **Limitations.**  One model class; searches not proved convergent (at `n ≤ 500` documented as not
  converged to `10⁻⁴·na`); sizes above 16 000 incomplete.
* **Before publication.**  Interval arithmetic for the bounds or an independent recomputation; the
  open cells; a proof or an exhaustive method for the worst instance at one small size.

### B3. Exact enumeration and exact finite-size constants

* **Contribution.**  Smallest sensitive balls on a type class of the cube computed exactly to
  `n = 10 000`: the three limits are approached from above with excess `≈ 0.45·ln n / n`, and the best
  centre lies outside the class from `n = 40` on (ENG-RES-0012).  Covers of the lattice chain
  enumerated to 24 torsions with a proof that all patterns are realised (ENG-RES-0002, -0007).  Exact
  elimination for the geometry division: two reduced affine solutions and a point at infinity of
  multiplicity 5 at `n = 10`, further solutions at `n = 9`, all ranks confirmed
  (`experiments/eng/geometry_req1/REPORT.md`).
* **Status.**  Exact arithmetic throughout; the type-class computation was not refereed; the
  elimination was cross-checked by the coordinator.
* **Prior art and originality.**  A `ln n / n` excess is what standard second-order asymptotics of
  type classes (polynomial prefactors of binomial tails) predict; the constant and the "centre
  outside the class" observation were not looked up.  **Most likely a rediscovery in substance.**
* **Where.**  `experiments/eng/slices/`, `experiments/eng/chain_cover/`, `experiments/eng/geometry_req1/`; ENG-RES-0002 (`206fd9e`), -0007,
  -0012 (`909751b`).
* **Assumptions.**  None beyond the definitions of the theory report.
* **Validation.**  Integer or rational arithmetic; the tables of the messages are regenerated from stored artifacts
  (`make_tables.py --verify`); the lattice values reproduce the theory division's published ones.
* **Limitations.**  The off-lattice chain is in floating point and on hold until it is done in exact
  arithmetic (SCI-REV-0008, M2).
* **Before publication.**  A literature check of the second-order constant; none of this is a paper on its own.

### B4. Corrections that changed what the programme may claim

* **Contribution.**  (a) The flat instance is not the worst and the published cost table was too
  favourable (ENG-RES-0008).  (b) `numpy`'s binomial sampler is biased for `n ≳ 10¹⁵`; all 585 exposed
  cases re-run with an exact sampler (ENG-RES-0013).  (c) Our own conclusion "instances that are not
  products cannot cost more than the worst product instance" was false as worded and is withdrawn
  (ENG-RES-0017, after SCI-REV-0018).  (d) The theory division's Proposition 11.121 (a wrong class
  assumption yields a false certificate) reproduced by a third implementation: invalid in 360 of 360
  runs with the assumed class, valid in 72 of 72 with the true one (X-015).  (e) Importing the Parma
  Polyhedra binding leaves the process in upward rounding — a hazard for every float tier in the
  programme (fixed and guarded in our tree; reported to the structural-biology division).
* **Where.**  ENG-RES-0008 (`a9ef1b4`), -0013 (`909751b`), -0017 (`8df6e5e`); `experiments/eng/twolevel/false_certificate.py`;
  `tests/eng/conftest.py`, `src/metricchain_eng/weighted_cube/polytope.py`; `docs/engineering/DEAD_ENDS.md` (ED-1 … ED-14).
* **Status.**  Each is in a linked correction with regenerated tables; (a)–(c) were examined by the science division.
* **Assumptions, prior art, originality.**  None claimed; these are quality control, and that libraries may change
  the rounding mode or lose accuracy in extreme parameter ranges is general numerical knowledge.
* **Limitations.**  They show what was wrong, not that what remains is right.

### B5. Certified interval computations (two subagent results; coordinator-checked reproduction only)

* **Contribution.**  GEOMETRY-REQ-0006 (X-019): for the request's instance A with couplings rounded
  to six decimals, the maximum of `H_c` on the 4-torus is attained exactly at `±θ̂` (two certificates
  in Arb ball arithmetic, branch and bound plus Krawczyk), and a 4-dimensional realisation with the
  same 16 lengths exists with fourth singular value `≥ 0.238` — a certified instance of non-universal
  rigidity; seven controls behave; 17 of 18 mutants killed, the survivor equivalent.  Site-dependent
  slopes (X-014, ENG-RES-0016): a certified algorithm with finite-size constants for cubes whose sites
  have different slopes (outer blocks of one type), refereed by a subagent whose findings were applied.
* **Status.**  X-019: tests and drivers re-run by the coordinator, records regenerate identically;
  the 956 trusted lines and the pen-and-paper lemmas were **not read**.  X-014: the relation to the
  theory division's Theorems 11.118/11.119(a) holds for claims (ii)–(vi) only.
* **Prior art.**  Interval branch and bound with Krawczyk tests is textbook verified computing;
  universal and global rigidity through stress matrices is established (Connelly; Gortler–Thurston).
  The instance and the question are the geometry division's.  No originality in method.
* **Where.**  `experiments/eng/geometry_req6/`, `tests/eng/test_geometry_req6.py`; `experiments/eng/twolevel/` (`hetero*.py`),
  `src/metricchain_eng/twolevel/hetero.py`, ENG-RES-0016, `experiments/eng/review_x014/REPORT.md`.
* **Assumptions.**  X-019: correctness of Arb and python-flint; the lemmas in the docstrings; the model identity with
  the geometry division's convention (tested, not proved, at 111°).  X-014: the class of the theory report with
  site-dependent slopes.
* **Validation.**  X-019: 31 tests, seven controls, mutation testing.  X-014: 64 800 literal runs with the theorem's
  constants without an invalid bracket or an abort; negative controls fail as they should, weakly.
* **Limitations and remaining work.**  X-019: an independent reading of the trusted core, a second interval library,
  instance B.  X-014: the lower bound used for comparison is not the optimum of its argument; large sizes only
  through the certified bound.

## C. Negative results, failures and rediscoveries

* **Deep nesting does not pay at the sizes computed.**  A fifth level keeps at most a quarter of its asymptotic gain at `n ≤ 16 000` and nothing at most sizes; at `n = 1000` no level beyond the second gains anything; the asymptotic exponents are approached slowly.  *Deprioritise* nesting beyond four levels as a practical device at such sizes.
* **Worst-case search by differential evolution is not a method of proof.**  Three rounds at
  `n ≤ 500` kept finding worse product instances (81 of 108 cells rose; the last round still by
  `0.013·na`).  *Abandon* reporting "the worst instance" from such searches without the qualifier
  "found".
* **Four published statements of ours were wrong** (a conclusion of ENG-RES-0014; a two-solver validation, withdrawn; three sentences about the chain covers; hand arithmetic on rounded table entries, twice).  The
  generated-tables rule exists because of them.
* **Three pre-registered predictions failed** (H3 at `n = 16 000`; H13(a) for the fourth level in both
  directions; H5 for six slope classes).  *Added 2026-11-27 (D-10):* a fourth, H12, failed on the rows
  collected after the halt, and H3 and H13(a) failed at further sizes
  (`docs/engineering/benchmarks/X-011_ADDENDUM.md` §5).
* **Certificates cost more than solving** (producer benchmark, subagent, unreviewed by the
  coordinator; `experiments/eng/leafcert_bench/REPORT.md`): over all certified instances 15 % of the
  time was search and 85 % assembling and checking; dynamic programming was 55–89 times faster on
  banded chains; the binding limit was certificate size, not time; a dense format inflates leaf
  certificates 16–48-fold on sparse instances.
* **The structural-biology producer is slower than toulbar2** on every development structure
  (7–25 times by its own figures), and those instances take toulbar2 under a second.
* **The verified kernel as written is not executable at realistic size** (B1 (d)); the theory
  division's Python reference checker needs 57 s for 4 680 eliminations.
* **Rediscoveries:** B3; and the practice of B1.
* **Nothing in the programme is ready for a CASP17 evaluation**; we agree with the Frontier
  Benchmarking Division's determination (FRONTIER-MSG-0001).

## D. Practical opportunities

| capability | mathematical possibility | implemented | synthetic validation | realistic computational validation | experimental evidence |
|---|---|---|---|---|---|
| a machine-checked optimum of a side-chain packing table (their producer → our translator → the Lean kernel through `verifyM`) | yes (`verify_sound`) | yes, end to end | yes | six development structures; **no held-out run, no comparison with proof logging** | none; and by the science division's analysis the certified minimum is one of many near-degenerate configurations |
| certified `ln Z` intervals as a referee for approximate marginals | yes (theory kernel for part of the rules; the rest paper arguments of the structural-biology division) | yes (theirs); an independent checker for small instances (ours) | 96 559 certificates | crambin by them only; **not reproduced by us** | none |
| differential-testing harness and a ledgered batch driver for bounded cloud jobs | — | yes (`modal_jobs/bench_app.py`, `bench_collect.py`) | — | 25 jobs | — |

The first row is the nearest thing to a useful capability, and its usefulness is undecided until E1.

## E. Recommended next actions (three)

**E1. The held-out certified-optimum benchmark with the proof-logging comparison.**
*Objective:* decide whether a native certificate is worth having against established proof logging,
and how far the producer reaches.  *Prerequisites in place:* the structural-biology software; our two
independent checkers; the kernel runner; their benchmark entry SB-BM-3 with hypotheses H3a–H3e.
*Missing:* a frozen model v2 with development rows; a held-out list fixed by the Frontier
Benchmarking Division; an encoder into pseudo-Boolean constraints (two encodings fixed in advance);
installed VeriPB/CakePB (or exact SCIP with VIPR); a native executable of the kernel.  *Baselines:*
toulbar2; a pseudo-Boolean optimiser with VeriPB proofs checked by CakePB.  *Benchmark:* SB-BM-3 on
the held-out list at one pinned commit, every certificate checked by three checkers.  *Success:*
H3a holds on every instance and the native route is no worse than proof logging in proof bytes and
check time on a majority of instances; *failure:* any unsound acceptance, or proof logging dominating
— in which case the native format should be dropped in favour of the established one.  *Compute:*
the structural-biology division estimates under 20 core-hours for 100 structures, 100 worst case; at
our measured tier price ($0.063 per core-hour with 2 GiB) that is under $10; the proof-logging side is
unknown.  *Reasoning cost:* not estimable by us.  *Dependencies:* structural biology, frontier,
theory.  *Model:* execution and collection can continue on Opus with the procedures in the master
plan §3a; the review of the benchmark specification and of unexpected outcomes should be Fable.

**E2. Close the two gaps under every application claim: the energy tables and their rounding.**
*Objective:* an implementation of the stated energy function by someone other than its author, and a
proved (directed-rounding) relation between the real-valued energy and the integer tables.
*Prerequisites:* the model definition in the structural-biology division's molecular-layer report;
OpenMM as a third party; our queue row Q-19 (design started).  *Missing:* the energy terms and
parameter files in a form that can be re-implemented; interval evaluation of each term.  *Baseline:*
OpenMM energies (agreement to `4·10⁻¹¹` kcal/mol today, with one author on both sides).
*Benchmark:* entrywise comparison of independently built tables on the six structures; an enclosure
per entry.  *Success:* every entry inside its enclosure and the certified minimiser unchanged
within it; *failure:* any entry outside.  *Compute:* local, minutes to hours.  *Reasoning cost:* not
estimable.  *Model:* Fable for the interval analysis; Opus for the re-implementation.

**E3. Make the verified kernel a usable program.**  *Objective:* the theory division adopts memoised
domains (or `verifyM` with its proof) so that "checked by the verified kernel" is a routine,
seconds-long step, also for the partition-function rules once they are formalised.  *Prerequisites:*
`RunKernel.lean`.  *Missing:* a compiled target and a strict file reader in the theory tree;
differential tests against the Python checkers.  *Success:* the six certificates checked in seconds
without loading the whole proof library in the interpreter (today: 3–45 s of checking after four to five minutes of loading).  *Compute:* local.  *Model:* Opus suffices.

Cheap to close without a new investigation: the six cells of job M-016 and ten of M-021 still running
(the certified bound at `n = 32 000 … 128 000` and at slopes ½ and 2) answer hypotheses H12 and H13
when collected (§G).  *(Collected on 2026-11-27: see the second note at the head of this report.)*

## F. Publication readiness

No result of this division is publishable on its own.  Two could be parts of joint papers: B2 as the
finite-size section of a paper on the theory division's adaptive algorithm (needs rigorous bounds
arithmetic, converged or proved worst cases, and an external check of the code); B1 (d) with E1 as a
short experience report on executing a proof-assistant kernel on protein side-chain instances
against proof logging (needs E1; novelty is doubtful because verified certificate checking is
established, and formal verification is not novelty).

## G. Engineering-specific record

**Implementation bottlenecks actually measured.**  (1) The Lean kernel: exponential in the length
of an elimination chain as written; with memoised domains 3.3 s (crambin) to 45 s (ubiquitin) per structure,
after 4–5 minutes of loading the proof library per invocation.  (2) The theory division's Python
reference checker: 57 s for 4 680 nested eliminations.  (3) Certificate assembly and checking, not
search, dominate producing certificates (C).  (4) The certified recursion for nested designs: 3 s,
177 s for two and three nested levels at `n = 16 000` on one core, and more than eight hours for six levels at `n ≥ 32 000` (still running).  (5) Memory: an unguarded enumeration of weighted shells
restarted the machine once (guard added: `MAX_SHELLS`); the proof library cannot be loaded under an
address-space limit of 7 GB.  (6) Importing `pplpy` switches the rounding mode (B4 (e)).

**Compute ledger, reconciled** (`docs/engineering/COMPUTE_LEDGER.md`): credits consumed by the workspace (all projects) $56.99 at 01:16 UTC on 2026-11-27, billed cost $0.00; $15.58 of the $1,750 authorised by D-5 has been used since its snapshot; engineering runs over all sessions $24.10 by the billing report (jobs M-001 … M-025; worst cases entered: more than $170); one entry was exceeded (M-022, $2.48 against $2.28, platform restarts), after which long tasks are planned as two attempts.  No job was launched after the directive.

**Modal jobs still running, left to finish unsupervised** (detached runs; no retries; they end at
their timeouts and leave nothing deployed): M-016, six tasks (the certified bound to six levels at `n = 32 000 … 128 000`), end by 04:20 UTC on 2026-11-27; M-021, ten tasks (the same bound at slopes ½ and 2), end by 09:35 UTC; with one platform restart per task the latest end is 21:35 UTC.  Worst case still to be spent: $5.2 without restarts, $16.7 with one restart each; cumulative credits then at most $73.7 against the stop line of $1,500.  Collect with `python modal_jobs/bench_collect.py --driver nested_bench --job certified1+certified2` (the result store expires seven days after its last access: before 2026-12-03); stop early with `modal app stop <app id>`.  Table, commands and the state at 01:02 UTC (M-016 12 of 18 cells, M-020 complete, M-021 6 of 16): the ledger, "Jobs left running".

**Evaluation integrity.**  No sealed list was opened or asked for; no held-out structure was looked
at; the hypotheses of BM-1 are in a protocol committed before collection; the outcomes of failed
predictions are published.

## H. State of every open item, for whoever resumes

| item | state | where |
|---|---|---|
| reply to the structural-biology division's two requests | sent: ENG-RES-0019 | `docs/collaboration/responses/engineering/` |
| independent checker of partition-function certificates (X-018) | written and run by a subagent; findings F1–F9; campaign for claim Z5 written and **not run**; checker not read by the coordinator | `experiments/eng/sb_zcheck/REPORT.md` |
| GEOMETRY-REQ-0006 (X-019) | certified by a subagent; reproduction checked; core not read | `experiments/eng/geometry_req6/REPORT.md` |
| producer benchmark for leaf certificates | subagent; tests pass; **report not reviewed** | `experiments/eng/leafcert_bench/REPORT.md` |
| rate of the level recursion (theory's Theorem R) | subagent; limit reproduced; four numerical discrepancies and a site where hypothesis (H1) fails; **coordinator's review incomplete** | `experiments/eng/level_rate/REPORT.md` |
| nested designs at `n ≥ 32 000` and slopes ½, 2 (H12, H13) | jobs running; collect and regenerate the tables.  **2026-11-27, after the halt (D-10): collected and closed** — 33 of 34 cells (one cell of M-016 has no row); H12 refuted; H13(a) refuted at the larger sizes; H13(b) and H1 not decided there | §G; `make_tables_x011.py`; `docs/engineering/benchmarks/X-011_ADDENDUM.md` |
| held-out benchmark, proof logging, long `ln Z` runs | reviewed, not started | ENG-RES-0019 §4 |
| requests of the theory and science divisions not started | listed with decisions | `docs/collaboration/status/engineering.md` |

**To resume, read in this order:** `docs/engineering/DIRECTIVES.md` (D-8 is the operative one),
this file, `docs/engineering/RESEARCH_LOG.md` ("Resume here"), `docs/engineering/COMPUTE_LEDGER.md`,
`docs/engineering/benchmarks/BENCHMARK_REGISTRY.md`.
