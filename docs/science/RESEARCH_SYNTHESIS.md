# Research synthesis and handoff — science division

*Scientific Discovery, Translation & Independent Validation Division of MetricChain.
Branch `research/scientific-translation`.  Written 2026-11-25 at checkpoint 20, last
revised at checkpoint 28, for an
investigator who has none of the conversation that produced the branch.  Read this file
first; it points to everything else.  The digest for the other two divisions is
`docs/collaboration/SCIENCE_TO_ALL.md`; the state table is `docs/collaboration/status/science.md`.*

---

## 0. Resume here

1. `git fetch origin claude/determined-ride-og1u7j research/ubuntu-engineering` and read the two
   heads.  **Last read (checkpoint 28, 21:31 UTC on 2026-11-25): theory `dcdfea6`** (their
   thirteenth checkpoint: THY-RES-0006 with theory report §§11.28, 11.29 — answers to our
   SCI-REQ-0001 Q1 and Q2 — read in full, §11.28 reviewed and replicated and answered by
   SCI-RES-0005; `SCIENCE_UPSTREAM_SYNC.md` says what was not read), **engineering
   `a2f6dc7`**.  If either moved, read its digest (`docs/collaboration/THEORY_TO_ENGINEERING.md`,
   `ENGINEERING_TO_THEORY.md` on their branches) and any `THY-*` / `ENG-*` file that
   mentions `SCI-`; record the reading in `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`;
   answer under `responses/science/`.
   State of the exchange: the theory division had seen our branch at `ae32bc9` (checkpoint
   25); it says our reviews SCI-REV-0001, -0002, -0003, -0005, -0006 "will be applied at
   the next checkpoint" and that our other messages were "seen in the digest, not yet
   read" — so expect replies to SCI-MSG-0005 … -0013, SCI-RES-0002 … -0005.  **One thing
   to watch:** the first paragraph of its §11.28 quotes a sentence we withdrew
   (SCI-MSG-0008 §1(b)); we asked for a rewording in SCI-RES-0005 §4.  The engineering
   division had not yet mentioned this branch.
2. Three workstreams were running when this was last revised (§5): R6, R7 and the
   referee R8 of addendum A16 (L2, F and P2 finished and are published: SCI-MSG-0014,
   SCI-RES-0006, SCI-MSG-0015).  Their report files exist as drafts under `docs/science/workstreams/`
   (`R6_REPORT.md`, `P2_REPORT.md`, `L2_REPORT.md`, `SF_REPORT.md`, `R7_REPORT.md`); **a draft is
   not a statement of the division**.  When a report is final: read it, re-run one
   script or re-derive one key step, and publish as described in §5.  F was asked to
   position its report against theory report §11.29; R7's working copy of engineering
   files (`experiments/science/ws_R7/eng_copy/`) is deliberately git-ignored.
3. Then take the top item of §7.

Rules that bind the division (from the research owner's charter; none may be relaxed
without the owner): write only to `research/scientific-translation`; never modify, merge
from, or push to the other two branches or `main`; no force-push, no pull request, no
history rewriting; no direct use of Modal — computational needs go to the engineering
division as specifications, and a request authorises nothing; shared budgets (Claude API
credits, Modal) are not visible from here and must not be increased; expensive workloads
end 2026-11-30 15:00 ET, credits expire 2026-11-30 19:00 ET; no manuscript, preprint or
external contact; biological sequence engineering, target-specific optimisation and
experiments are out of scope; never fabricate a citation or a number; corrections of
published statements are linked messages, never silent rewrites.

## 1. What exists, and where

| artifact | what it is |
|---|---|
| `docs/collaboration/SCIENCE_TO_ALL.md` | digest (27 items) and index of every message sent |
| `docs/collaboration/messages/science/` | `SCI-MSG-0001…0013` (findings, corrections, prioritisation), `SCI-REV-0001…0006` (reviews) |
| `docs/collaboration/requests/science/SCI-REQ-0001.md` | four theoretical questions to the theory division |
| `docs/collaboration/responses/science/SCI-RES-0001…0005` | answers to the theory division: THY-REQ-0011 (in full), THY-RES-0005, THY-RES-0006 §5 (§11.29 still owed, with workstream F) |
| `docs/collaboration/status/science.md` | investigations, findings S1–S36 with status, outstanding requests |
| `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md` | what was read upstream, at which commit, how deeply; dependencies; sync log |
| `docs/science/INFERENCE_LIMITS.md` (v3) and `INFERENCE_LIMITS_ADDENDA.md` (A1–A16) | our own mathematics: what evaluations, averaged data and thermodynamic data determine |
| `docs/science/PHYSICAL_APPLICABILITY.md` | what the mathematics means for molecules; the measured class constants |
| `docs/science/ALTERNATIVE_FRAMEWORKS.md` | polytope against ellipsoid; four models of ignorance |
| `docs/science/SCIENTIFIC_FRONTIER_MAP.md` (v4) | twelve limitations of the science, their kind, where the programme stands |
| `docs/science/OPEN_PROBLEMS.md` (v3) | every open problem we made precise, with owner |
| `docs/science/BENCHMARK_DESIGN.md` (v2) | eight hypotheses, eight benchmarks, refutation criteria, what was run |
| `docs/science/PUBLICATION_OPPORTUNITIES.md` (v2+) | thirteen candidates judged as a hostile referee would |
| `docs/science/INDEPENDENT_VALIDATION.md` | what we replicated, re-ran, reviewed — and what we did not |
| `docs/science/SCIENTIFIC_RESEARCH_LOG.md` | chronological log, with every error of ours |
| `docs/science/DEAD_ENDS.md` | our own refuted statements and negative results |
| `docs/science/PRIOR_ART_MATRIX.md` | one table: every claim of the three branches, its originality class, where the evidence is |
| `docs/science/workstreams/` | briefs and reports of the independent workstreams (`COMMON.md` has their rules) |
| `experiments/science/` | all code: `pi_inference/`, `pi_chain/` (coordinator), `ws_*/` (workstreams), `audit_replication/` |

## 2. The findings that matter (status in brackets; details at the pointer)

**About the programme's foundations**

1. **Which class a real residual lives in — measured [M]** (`PHYSICAL_APPLICABILITY.md` §2;
   SCI-RES-0002).  Alanine peptides, ff14SB as known part.  Same-lineage force-field
   differences: *exactly* additive or residue-local.  Charge-model changes: `βc ≈ 2–10`.
   GBn2 solvent term in backbone torsions: `βc = 12–53`, growing with length, dense second
   order, no sharp site; near the pair-additive class in RMS (`0.2–0.9 k_BT`), not in sup
   norm (`2–16 k_BT`); Jensen gap 2–3 nats against a class bound of 71–178.  *A pilot: one
   amino acid, rigid geometry, exact on finite grids.*
   **In residue-rotamer variables on a fixed backbone (workstream P2, checkpoint 31;
   SCI-MSG-0015):** the known part is exactly pairwise; the solvent term is pairwise to
   `0.003–0.2 kcal/mol` (third-order constants) for neutral side chains; the second-order
   interface is an exact certificate for apolar side chains and fails for polar and
   charged ones (large pair part); the third-order interface is exact in every
   enumerated instance; first-order constants saturate for neutral and grow for charged
   side chains.  *Exposed synthetic peptides; constants by enumeration; no buried
   environment.*
2. **The exponential price is the geometry of the first-order class, not the worst-case
   quantifier [P]** (`ALTERNATIVE_FRAMEWORKS.md`; SCI-MSG-0007).  Kernel-ball classes of
   bounded interaction order cost `≈ n^m` with matching lower bounds; the envelope wins
   where the known part is sharp; nothing cheap can stay valid on a first-order class.
3. **Four reviews of the theory division's newest sections: no theorem false** (SCI-REV-0001,
   -0002, -0003, -0005).  One displayed claim false as stated (one-line repair), one proof
   step missing (supplied), two gaps in a written proof (closed), a proved bracket
   improvable with the section's own tools, and in every section a headline that outruns
   its theorems — for §11.25 materially (two of three exponents).
4. **Prior art** (SCI-REV-0004, -0006; SCI-RES-0003; SCI-MSG-0002, -0003).  In print: the
   odds-ratio lemma; the non-adaptive exponent formulas at the cone; the dictionary's
   identities and mechanism; the identified-set framework under four names.  Not found:
   "adaptive = hinted" with exact exponents and a matching algorithm without
   log-concavity (the result that would survive a hostile referee); the two-round
   separation; a verified checker for cost-function-network certificates valid for a
   whole class of residuals.

**Our own mathematics** (`INFERENCE_LIMITS.md` v3 — refereed, short cores machine-checked)

5. **What averaged data are worth to a certified computation in a first-order class
   [P; cores V]**: exact marginals of bounded order change neither exponent (three
   independent proofs of the non-adaptive half); with error bars, correlations of *every*
   order change nothing (Theorem 4-τ); exact marginals of order `αn` do lower it (Theorem
   4‴); pinned ensembles determine `ln Z`; a mean-energy datum changes the hardest
   instance, not the exponent at bounded accuracy (hidden twin; root proved by our
   referee).  *All on the cube with zero known part* — **except that the field case for
   one-body data is now settled (workstream F, checkpoint 30; SCI-RES-0006): neither class
   exponent changes, by a compensation lemma; instance-wise the oracle helps.**
   **And where a datum does help (addendum A16, checkpoint 26; author only):** with a
   mean-energy datum `ln Z = S − βU`, and the class confines the entropy to
   `[n·h(σ_u), n ln 2]` — so the datum alone gives `ln Z` within `n·KL(σ_u‖½)/2`, which removes
   an exponential cost for accuracies between `KL(σ_u‖½)` and `KL(½‖σ_u) = ln cosh(u/2)` per
   site; below, a "plateau twin" bounds what the datum can do, and **that bound is the
   exact cost at the instance where it is proved** (Lemma A16.5, an isoperimetric
   inequality with an energy constraint; Theorem A16.6) — for the whole class it is
   Conjecture A16.4.  SCI-MSG-0012, -0013.
6. **Observable free-energy differences have a closed-form robust range in one setting
   [V since checkpoint 29]** (addenda A11, A13; SCI-MSG-0009, -0014): a submodular known
   part and monotone macrostates (any lower set against any upper set; binary sites or
   ordered alphabets; any finite distributive lattice) — sandwich between two fields
   (Holley); common uncertainty cancels.  The general problem was solved by the theory
   division as a transport problem with gains (its §11.28; reviewed and replicated by
   us, SCI-RES-0005).
7. **Certified inference from averaged data** (`INFERENCE_LIMITS.md` §§8, 9, 11): identified
   sets with dual certificates; data certify a *lower* bound on model error.  Exact
   numbers on lattice chains (to 10 beads with a model; 27 beads model-free).  The
   framework is known; a physical instance does not exist.

**New directions opened by workstreams**

8. **Certified kinetics [cores V]** (SCI-MSG-0005): barrier lower bounds and escape-rate
   upper bounds are cut certificates on the existing kernels; PSPACE obstruction on
   chains; no physical instance.
9. **Homometric chains; scattering data and the profile class** (SCI-REV-0006): Debye
   intensities lie in the profile class; chains are not identifiable from complete
   distance distributions.

## 3. What was and was not independently checked

`INDEPENDENT_VALIDATION.md` is authoritative.  In short: the theory division's audit
replicated at `5ed4072` (56 Lean files, 3423 declarations); engineering's class tables
replicated for 1–10 torsions (coordinator) and 4–23 beads (R2); four sections reviewed with
independent code; every workstream's Lean file re-compiled by the coordinator; one or two
scripts of every workstream re-run.  **Not checked by anyone outside the theory division:
the cost of the nested adaptive algorithm (Theorems 11.52, 11.56) — workstream R6 is on
it.**  Not replicated: most of workstream P's measurements (two numbers re-run).  Nothing
in any branch has been compared with a measurement.

## 4. Our own errors (all corrected with linked messages; `DEAD_ENDS.md` has the list)

Five published sentences were wrong — a scope, a quantifier, a physical gloss, an
attribution, a kind — each written beside a correct theorem; plus four errors of
record-keeping.  Rules adopted, in force: fetch, read, *then* write the commit message;
header times from `date -u`; a physical reading is published one checkpoint after the
statement it reads; when a workstream finalises a report after a message was drawn from
it, diff the message against the report's change list; summary tables and headings are
refereed as statements; in-progress workstream files are snapshots, not statements.

## 5. Running when this was written (second wave)

| id | brief | on completion |
|---|---|---|
| R6 | `workstreams/R6_brief.md` — independent line-by-line review, with own re-derivation and implementation, of the cost of the nested adaptive algorithm (theory report §§11.18–11.19) | read `R6_REPORT.md`; re-run one script; publish as `SCI-REV-0007` to theory; update `PUBLICATION_OPPORTUNITIES.md` P1 — this is the check on which the programme's headline depends |
| P2 | `workstreams/P2_brief.md` — class constants of the GBn2 term in *rotamer* variables on a fixed backbone | **done at checkpoint 31** — `P2_REPORT.md`; end-to-end check re-run; published as SCI-MSG-0015; `PHYSICAL_APPLICABILITY.md` §2a, `BENCHMARK_DESIGN.md` B1, frontier map hypothesis 3 updated |
| L2 | `workstreams/L2_brief.md` — Lean: addendum A11 (Holley sandwich), the referee's finite inequalities, Proposition A1.2 items 1–3 | **done at checkpoint 29** — 178 theorems, re-compiled; labels changed to [V] in the addenda and the status file; two corrections of Proposition A1.2; published as SCI-MSG-0014 |
| R7 | `workstreams/R7_brief.md` — independent review and replication of the engineering division's results (the first review of that branch by us beyond its class tables) | read `R7_REPORT.md`; re-run one script; publish as `SCI-REV-0008` to engineering, copy theory; update `INDEPENDENT_VALIDATION.md` |
| F | `workstreams/F_brief.md` — the two-oracle model with a field (report: `SF_REPORT.md`) | **done at checkpoint 30** — the coordinator's conjecture is true as a statement and false as an explanation; Theorems A, B (class exponents unchanged, every `n`); instance-wise bracket; `k = 2` exact at `n = 13`; tolerance theorem; comparison with theory report §11.29.  Coordinator re-derived the lemmas, Theorem A, the algebra of B and the tilt inequality; re-ran the exact-rational check; own check `pi_inference/compensation_lemma_check.py`.  Published as SCI-RES-0006 |
| R8 | `workstreams/R8_brief.md` — adversarial referee of addendum A16 (the mean-energy datum at extensive accuracy: entropy bracket, plateau twin, isoperimetry with an energy constraint, the conjecture); launched at checkpoint 28 because A16 had no second reader | read `R8_REPORT.md`; apply its findings to A16 with linked corrections of SCI-MSG-0012/-0013 if any sentence falls; change "author only" to "refereed" in status rows S34, S36 only for the statements it confirms |

Workstream files under `experiments/science/ws_*/` and `*_REPORT.md` are committed as
snapshots while a workstream runs; they are statements of the division only once the
digest, a `SCI-*` message or the validation record cites them.

## 6. Outstanding requests to the other divisions

The full table is in `status/science.md`.  The ones we would rank first, with reasons in
`SCI-MSG-0010`: to theory — the stopping rule of Theorem 11.84 (M1 of SCI-REV-0003), the
headline of §11.25 (M1 of SCI-REV-0001), P-T3 (a certified typical-norm remainder), X-T1
(a sharp–soft kernel), K-T1/K-T2 (cut checker; polynomial weights), the field case of the
two-oracle model (SCI-REQ-0001 Q2); to engineering — P-E1 (now also our own P2), X-E1
(cover against span format on chain geometry), E-1 of SCI-REV-0006 (native certificates
against pseudo-Boolean proofs), R3-E1 (bridge tables).

## 7. What to do next, ranked

1. **Publish R6, P2, L2** (§5).  R6 and P2 are the two results that could most change the
   publication assessment and the frontier map.
2. **The oracle-invariance theorem** is assembled in addendum A12 and was sent as
   SCI-MSG-0011 (Corollary R6′ written out).  Its limit at extensive accuracy is addendum
   A16 (SCI-MSG-0012, -0013).  Still owed: L2's machine checks; **a second reader for
   A16** (Lemma A16.5 is five lines and a good candidate for Lean); Conjecture A16.4 for
   instances that are not flat outside a small set (asked of the theory division; a
   good task for a workstream of ours if they do not take it); the non-adaptive
   exponent with the datum (remark (4) of the lemma gives the bracket; its worst case is
   not evaluated).
3. **The field case** (SCI-REQ-0001 Q2): without it "local data are worth nothing" is a
   statement about a symmetric model.  Start numerically: small cubes with a field, exact
   linear programmes for the adversary under a one-body marginal oracle.
4. **A physical instance of certified inference from averaged data**, on whichever model
   P2 shows to have usable constants — synthetic data from a hidden truth first
   (`BENCHMARK_DESIGN.md` B3, B4), with maximum occurrence as practised as baseline.
5. **A11 beyond its hypotheses**: ordered alphabets (done in a remark, write it out);
   frustrated known parts (the linear-fractional programme has a non-additive extremal
   residual — describe it); the range given evaluations.
6. **A class with known features and an analytic remainder for a generalized-Born term**
   (`OPEN_PROBLEMS.md` D4): the route to the first certified envelope of a real many-body
   term.
7. A final handoff update of this file; a last synchronisation; a last push.

## 8. Environment (verified on the machine that produced the branch; a new container starts empty)

* Python 3.13 with numpy, scipy (HiGHS), mpmath, sympy; `pip install openmm numexpr` for
  `ws_P/`, `ws_P2/`.
* Lean 4.31.0 with the Mathlib cache of the theory branch (`lake exe cache get` in the
  repository root after installing the toolchain; the toolchain archive needs `zstd` —
  Python's `zstandard` was used).  Check single files with
  `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd <repo>; lake env lean <file>`.
  Never `lake build` from a workstream.
* Read-only upstream checkouts: `git worktree add --detach <dir>/thy_ro <theory commit>`,
  likewise `eng_ro`; scripts that read the engineering class tables take their directory
  from `MC_ENG_DATA` (`experiments/science/README.md`).
* Solver tolerance trap, met three times in one day: HiGHS defaults produce spurious
  violations of exact identities at the `10⁻⁶ … 10⁻⁹` level; scale variables and set
  tolerances to `10⁻¹⁰` before believing a counterexample.
* Checkpoint procedure: fetch both upstream branches; read the heads; set message header
  times from `date -u`; `git add -A experiments/science docs/science docs/collaboration`;
  commit with the trailer lines used throughout the branch's history; push to
  `research/scientific-translation` only.

## 9. What must not be claimed on the strength of this branch

That anything was compared with an experiment.  That a class constant measured on a grid
is a bound.  That a certified minimum is a predicted structure.  That "local data are
worth nothing" beyond the uniform cube.  That any result here is new — "not found" is the
strongest statement our searches support, and their depth is recorded source by source.
