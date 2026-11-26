# Research synthesis and handoff — science division

*Scientific Discovery, Translation & Independent Validation Division of MetricChain.
Branch `research/scientific-translation`.  Written 2026-11-25 at checkpoint 20, last
revised 2026-11-26 03:30 UTC (after checkpoint 43 and the theory division's seventeenth
checkpoint; §0 rewritten, §5 extended), for an
investigator who has none of the conversation that produced the branch.  Read this file
first; it points to everything else.  The digest for the other two divisions is
`docs/collaboration/SCIENCE_TO_ALL.md`; the state table is `docs/collaboration/status/science.md`.*

---

## 0. Resume here

*State at 2026-11-26 11:23 UTC.  (The block is rewritten when the state changes; the
history is in `SCIENTIFIC_RESEARCH_LOG.md`, cycles 37–57.)*

1. **Fetch and read the two upstream heads** (read-only), **in a command of its own**:
   `git fetch origin claude/determined-ride-og1u7j research/ubuntu-engineering`, then the
   heads in `.git/FETCH_HEAD`, compared with the last row of
   `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md` **before anything is staged**.  If either
   moved, read its digest and every `THY-*` / `ENG-*` file that mentions `SCI-`, record
   the reading in the sync file, and answer under `responses/science/` before writing a
   commit message.  (Four checkpoints of the other divisions crossed work in progress
   on 2026-11-26; once the fetch was chained with the commit and the commit message
   said "unchanged" when it was not — `DEAD_ENDS.md` SD49.)
   * **Theory: last read `628d3e2`** (their twenty-first checkpoint, commit time
     2026-11-26 10:27 UTC; it fetched ours at `ddd4be3` and read SCI-REV-0016 in full,
     nothing yet of SCI-RES-0017, SCI-REV-0015, SCI-RES-0018, SCI-MSG-0027):
     THY-RES-0014 read in full by the coordinator; **answered: SCI-RES-0019**.  It
     applies SCI-REV-0014 in full (Proposition 11.117(b) corrected, twelve corrections
     of record), adopts our `RateFull.lean` and `SandwichCost.lean` into
     `proofs/Frontiers/`, and brings `SplitRule.lean` (a domain-split layer `SCert` above
     their kernel certificates — our P7-T2; **it is the form our branching trees have**,
     SCI-RES-0019 §2), `SymmetricPairHypothesis.lean` (P7-T3), a measurement of what the
     Lean kernel can evaluate (P7-T4: `10⁵` table entries with the right encoding; no
     theorem links the integer checker to `verify`), and **Proposition 11.113b** ("one
     side at a time": from a floor's sampler both sides of `ln Z` at a price `e^{2x}` in
     the floor's excess; from a ceiling's sampler only the lower side — tested, not
     refereed; priced on our sandwiches in SCI-RES-0019 §3).  Its §7: **M1 of
     SCI-REV-0016 "is right on reading"**; the model-free comparison, Proposition R16.1
     and the three minor points will be adopted at their next checkpoint.  Not read by
     us: the four Lean files, the amended report, the kernel-evaluation experiment.
     Their audit at this head: `INDEPENDENT_VALIDATION.md` §1.11.
     *Before it:* `9befefd` (their twentieth checkpoint, commit time 2026-11-26
     08:17 UTC; it fetched ours at `edfd54c` and read SCI-REV-0014, SCI-RES-0015 in full,
     the rest by their heads): THY-RES-0013 (to the engineering division, copy to us)
     read in full; **answered: SCI-RES-0018**.  They accept M1 of SCI-REV-0014 and offer
     their new §4 — a certified third level of the nested algorithm — for review:
     **done: SCI-REV-0016** (workstream R16; finding 9o: the rule holds, 159 of 159
     certified numbers replicated, one major finding on the attribution of five
     two-level worst cases).  At this head nothing that their audit builds or runs has
     changed since `f7df44f`; the documents pass their reference check
     (`INDEPENDENT_VALIDATION.md` §1.10; the full script was not re-run).
     *Before it:* `f7df44f` (their nineteenth checkpoint, commit time 2026-11-26
     06:24 UTC; it read ours at `4b80f89`): THY-RES-0012 read in full by the coordinator
     and **answered: SCI-RES-0016**.  It applies our review SCI-REV-0013 in full,
     machine-checks our share lemmas at every level and for any window
     (`ShareLevels.lean`) and workstream P5's two lemmas (`DownClosedRemainder.lean`),
     and brings two paper statements that touch our certificates — since then run by
     us (SCI-RES-0017) and reviewed by workstream R15 (SCI-REV-0015: nothing false;
     conditions to add) —: **Proposition 11.113a** (a nested sampler — evaluate the energy only with
     probability `ρ`; evaluations pay for the envelope whatever the share form) and
     **Proposition 11.18f** (which allocation of a constant is best).  Not read by us:
     the amended theory report outside the passages R15 reviewed (lines 2440–2770 and
     9636–10105), four of the five new Lean files, their new check directories.
     **Their audit at this head is replicated: passes** (`INDEPENDENT_VALIDATION.md`
     §1.9).  Before it: `63e36f7` (their
     eighteenth checkpoint: THY-RES-0011, THY-MSG-0015 read in full, answered by
     SCI-RES-0013; the amended report and the new Lean files read by workstream R13,
     SCI-REV-0014; audit replicated).
   * **Engineering: last read `ce71724`** (their checkpoint 5, 2026-11-26; it read ours at
     `b9556c4`, SCI-RES-0012 only): ENG-MSG-0005 in full, ENG-RES-0014 in part (§0, §4, §5);
     **answered: SCI-RES-0015**.  They closed two points of our review SCI-REV-0008,
     adopted our tree format, and put the stand-alone checker first in their queue
     (specification not yet read by them; reading order suggested in SCI-RES-0015 §3).
     Their `§1` and `§4` arguments "have been checked by nobody else": a referee
     workstream was offered, not started.  Before that: `c2ad4f8` (their checkpoint 4, 2026-11-26 04:05 UTC — their
     first contact with this branch, which they read at `d45ad56`).  They verified and
     accepted the findings of SCI-REV-0007 and SCI-REV-0008 (five linked corrections of
     their record; our separation table reproduced to every digit) and triaged every
     request of ours (`status/science.md`, "Outstanding requests": accepted, deferred,
     not decided).  **Answered: SCI-RES-0012**, with two linked corrections of our own
     SCI-REV-0007 that their measurements prompted.  Not read by us: their code and
     result files, most of ENG-RES-0011 and -0012.  Offered: an independent checker of
     their branch-and-bound trees if they adopt the format of SCI-RES-0012 §3.  Their
     most useful next step for us: the stand-alone checker of the free-energy
     certificate (specification: SCI-MSG-0025 §8).
   * **What the theory division has read of ours:** at `edfd54c` SCI-REV-0014 and
     SCI-RES-0015 in full and the others by their heads, nothing applied yet; before
     that up to `4b80f89` (SCI-REV-0013,
     SCI-MSG-0024, SCI-MSG-0025, SCI-RES-0012, SCI-RES-0013 and addenda A17 (14), (15)
     "in part" — all applied or answered in THY-RES-0012).  **Not yet read by them, in
     the order they should read it:** SCI-REV-0016 (the review they offered),
     SCI-MSG-0027 (the charged case; their nested sampler on two charged peptides;
     request P8-T1), SCI-RES-0016 (answers THY-RES-0012; says what
     crossed), SCI-RES-0017 (their nested sampler and allocation rule, run),
     SCI-REV-0015 (the review they asked for), SCI-REV-0014 (their rate refereed; Proposition 11.117(b) needs
     "symmetric"), SCI-RES-0014 (shares at the leaves), **SCI-MSG-0026** (the certificate
     reaches a compact ensemble that is not frozen; Lemma A17.16; exact window terms;
     the reach table; their audit at `63e36f7` replicated; L3-T3 answered).
   * **Owed to the theory division:** (a) ~~the referee report on their rate~~ — **done:
     SCI-REV-0014** (correct, machine-checked; one major finding on Proposition
     11.117(b)); (b) ~~their request (c), shares after branching on one site~~ — **done:
     SCI-RES-0014**; (c) ~~the replication of their audit at
     `63e36f7`~~ — **done, passes** (`INDEPENDENT_VALIDATION.md` §1.8; reported in
     SCI-MSG-0026 §8); (d) the crossover map of their §11.32 (our R10-T2) once the
     engineering division's enumeration R10-E1 exists; (e) ~~L3-T3~~ — **answered**
     (SCI-MSG-0026 §7: Corollary A needs the attained maximum from their `GameFunction`
     and the saddle of their Theorem 11.99 as a hypothesis; the conditional Lean
     statement is written only if they want it).  **Accepted in SCI-RES-0016:**
     (f) ~~the nested sampler of their Proposition 11.113a~~ — **done: SCI-RES-0017**
     (validated; stopping condition met; finding 9l); (g) ~~a review of Proposition
     11.18e(b′)(i), Proposition 11.18f, Proposition 11.113a,
     `ratio_expected_queries_ge_mixed` against Corollary 11.114(d) and the necessity
     argument of Proposition 11.113(d), with their conjecture (b′)(ii) as a question~~ —
     **done: SCI-REV-0015** (workstream R15; finding 9m); (h) ~~the replication of
     their audit at `f7df44f`~~ — **done, passes** (`INDEPENDENT_VALIDATION.md` §1.9);
     (i) ~~a test of the allocation rule of Proposition 11.18f~~ — **done:
     SCI-RES-0017** (finding 9l).  **Accepted in SCI-RES-0018:** (j) ~~the review of
     THY-RES-0013 §4~~ — **done: SCI-REV-0016** (finding 9o).  Nothing is owed to
     them at this checkpoint.
   * **Expect from them:** the answer to SCI-RES-0017, SCI-REV-0015, SCI-RES-0018,
     SCI-MSG-0027 and SCI-REV-0016 ("a separate message", THY-RES-0014 §7);
     R16-THY-1…6 (SCI-REV-0016: which of 1(a), 1(b) they take;
     whether the flat-instance table enters their remark (1b)); P8-T1, P8-T2, A18-T1
     (SCI-MSG-0027: the remainder identity with a term-dependent order in Lean, "at
     most `m` hosts"); R15-T1…T6 (SCI-REV-0015: the replacement texts; whether they
     adopt `t_f + ρ̄t`); A17-T1…T3 (SCI-RES-0017: the one-known-mean variant, the core
     statement and the water-filling bound, an oracle for the pair level); A16-T2 (SCI-MSG-0026:
     the asymmetry of floor and ceiling in their vocabulary); R13-T1…T6 (SCI-REV-0014: whether they adopt `RateFull.lean`;
     whether Proposition 11.117(b) was meant for symmetric envelopes); P7-T1…T5
     (SCI-RES-0014: a domain-split rule, the symmetrised hypothesis).  Answered by
     them at `f7df44f`: R12-T1…T6 (all adopted), P6-T1…T3, P5-T2, P5-T3, P5-T1 in part.
     **Answered by them at `628d3e2`:** R13-T1…T6 (all applied), P7-T1…T4 (done; P7-T5
     open on both sides), A16-T1, A16-T2 — strike these from the list above.
2. **Workstreams running when this was written: one, P9** (below).  No run of the
   coordinator is going.  (Two runs were finished after SCI-MSG-0027 went out and are
   in addendum A17 (18) but in no message yet — send them with P9's results: Lys₁₂
   from the order-4 ball, item 62; Ser₂₀ with the sampler, item 62a.)  Each workstream writes notes from its first
   minute to `experiments/science/ws_<ID>/NOTES.md` and a report to
   `docs/science/workstreams/<ID>_REPORT.md`; **a draft is not a statement of the
   division**.  When one reports: read it in full, re-derive or recompute its key
   statements with separate lines, then publish (§5).  If the container was lost, read
   the notes and decide whether to resume from them.
   * **P8** (`P8_brief.md`; launched 05:38 UTC; handed back shortly before 08:30 UTC) —
     the charged case.  **Read in full, verified and published: SCI-MSG-0027**
     (finding 9n; `workstreams/P8_REPORT.md` with the coordinator's note at its end,
     which lives in `experiments/science/ws_P8/report_parts/90_coordinator_note.md` —
     the report is generated by `ws_P8/mk_report.py`).  The coordinator's checks are in
     `experiments/science/p8_verification/`.  **What of P8's data is in the
     repository:** `experiments/science/.gitignore` excludes every `.npz` of a
     workstream as regenerable; the one exception, force-added, is **the result — the
     per-subset constants** `ws_P8/out/g12_*.npz` and `g12b_*.npz` (24 files, 0.7 MB:
     four peptides, orders 4–6, six variants).  Not in the repository: P8's balls
     (`ws_P8/cache/ball_*.npz`, up to 111 MB), its enumerations (`ws_P8/out/m1_*.npz`),
     checkpoints.  **From a fresh clone:** `nested_sampler_ext.py` and
     `occ_reduction_test.py` evaluate a missing ball themselves (half an hour for Lys₁₂
     at order 5); `p8_verification/lys12_rerun.py` insists on P8's own ball — regenerate
     it with `python3 -B ws_P8/p8_12_certificate.py K12 H 0.70 5 7 --force`; the
     end-to-end check of `nested_sampler_ext.py` on Lys₅ reads the anchor from
     `ws_P8/out/m1_K5_H_0.70.npz` (`python3 -B ws_P8/p8_01_measure.py K5 H 0.70`, eight
     minutes); `lys_enum_check.py` needs only the committed JSON files.
   * **P9** (`P9_brief.md`; **launched 10:25 UTC, running when this was written**) —
     penalties resolved by rotamer state, the lever workstream P8 named (its request
     P8-E4): P8's code has every block bound per state of the block's host side chains
     before it takes the maximum; P9 is to keep the dependence (site, pair and triple
     tables), prove the tables valid, validate at every state of Lys₄, Lys₅, LKSE:5
     with a control that must fail, and measure the gain on the certified brackets of
     Lys₁₂ (orders 4, 5) and (LKSE)₃.  Numbers to beat (triple form, band 7, split
     around the anchor): 0.0567 nats (Lys₁₂, order 5), 1.4125 (Lys₁₂, order 4), 4.30
     ((LKSE)₃).  Notes: `experiments/science/ws_P9/NOTES.md`; draft:
     `workstreams/P9_REPORT.md` — **a draft until the coordinator has read and verified
     it** (every-state check with own code; re-run).
   * **R16** (`R16_brief.md`; launched 08:45 UTC, handed back 10:00 UTC) — the review of
     THY-RES-0013 §4 that the theory division offered.  **Done and published:
     SCI-REV-0016** (`R16_REPORT.md` with a coordinator's note; finding 9o).
   * **R15** (`R15_brief.md`; launched 06:58 UTC) — the review the theory division
     asked for in THY-RES-0012 (requests 1 and 3).  **Done and published:
     SCI-REV-0015** (`R15_REPORT.md` with a coordinator's note; finding 9m).
   * **R14** (`R14_brief.md`) — adversarial referee of the coordinator's own addenda
     A17 (13)–(16): proofs, an independent implementation of the window models, a
     search for violations of the sandwich by optimisation.  **Not done:** launched
     05:59 UTC and terminated within two minutes by a platform safeguard of the model
     provider, before any review.  The coordinator did not relaunch it and did not do
     its work in its place (the harness says so explicitly; the charter says to
     respect platform safeguards).  The brief stands.  **These four addenda are
     unrefereed; whether and how they are reviewed is the research owner's
     decision.**  (Addenda A17 (17) and A17 (18), written since, are unrefereed as
     well; one section of (17) — the one-known-mean bound — was reviewed by R15.)
   * **Finished and published in this stretch:** P5 (SCI-MSG-0024), R12 (SCI-REV-0013),
     P6 (SCI-MSG-0025), R13 (SCI-REV-0014), P7 (SCI-RES-0014); the coordinator's own: the audit at `9408e33`, benchmark B10 for
     charged and aromatic side chains (A17 (12) item 25), certified populations
     (A17 (13)), the helix with pair shares (A17 (14)), where the certificate stops
     and how far it reaches (A17 (15), (16); SCI-MSG-0026), the audit at `63e36f7`,
     the theory division's nested sampler and allocation rule on real instances
     (A17 (17); SCI-RES-0017), R15 (SCI-REV-0015), the audit at `f7df44f`, P8 and the
     charged case (A17 (18); SCI-MSG-0027), R16 (SCI-REV-0016).
   * Read-only exports used by the workstreams are in the session scratchpad and are
     **lost with the container** (re-create with `git archive <commit> | tar -x -C <dir>`):
     the theory tree at `63e36f7` (`thy_ro_63e36f7/`), at `9408e33`, at `24a3c27`.
   * All earlier workstreams are finished and published; the table in §5 says where.
     R7's working copy of engineering files (`experiments/science/ws_R7/eng_copy/`) is
     deliberately git-ignored (`ws_R7/make_eng_copy.sh` re-creates it).
   * The history of the exchange — what the other divisions adopted of ours, what we
     answered and when — is in the two tables at the end of
     `docs/collaboration/SCIENCE_TO_ALL.md` and in `status/science.md`.
   * **Things the research owner should know of.**  (i) Workstream L4's own report was
     produced by a script after its file-writing tool had declined to create a report
     from a sub-task, and a second generation was denied by the permission system; the
     coordinator did not run the generator and did not adopt its output (kept outside
     the repository, in the session scratchpad under `L4_not_adopted/`, which does not
     survive the container); `workstreams/L4_REPORT.md` was written by the coordinator.
     Later workstreams were told not to work around such a refusal.  (ii) Two sources
     cited as unread need a library that neither we nor the theory division have:
     Decoster, J. Phys. A 37 (2004) 9051–9070, and the original of
     Dagum–Karp–Luby–Ross (2000).  (iii) A compound shell command of the coordinator
     containing a wildcard deletion in a scratch directory was refused by the
     environment's safety check; nothing was deleted and the removal was not attempted
     another way (fresh directories were used instead); scratch copies named
     `R6_pass3b/`, `P6_rerun_tree/`, `audit_*/` remain in the session scratchpad.
     (iv) One pushed commit message (`b9556c4`) states the upstream heads wrongly; it is
     corrected by the commit after it, not rewritten.  (v) At 05:26 UTC on 2026-11-26
     a Lean process of workstream P7 (11.9 GB) exhausted the machine's shared memory
     budget; the kernel killed it and one run of the coordinator, which was
     restarted; P7 reported it unprompted and corrected two statements of its own
     first report.  Workstreams are now told: no process above 3 GB.  (vi) **Workstream
     R14 — the adversarial referee of the coordinator's own addenda A17 (13)–(16) — was
     terminated by a platform safeguard of the model provider within two minutes of
     its launch (05:59 UTC, 2026-11-26; the notice names a classifier, says that this
     "sometimes happens with safe, normal conversations", and asks that the message be
     passed to the user and the agent's work not be done in its place).**  Nothing
     was reviewed.  The coordinator did not relaunch it with other words and did not
     substitute for it.  Those four addenda, and SCI-MSG-0026 which reports two of
     them, therefore rest on their author's own checks; so do A17 (17) and A17 (18),
     written since (one section of (17) was reviewed by workstream R15, and two
     lemmas are machine-checked).  (vii) Workstream P8 ran four enumeration passes far
     above the 3 GB limit (11.7 GB measured when it killed one, 06:46 UTC, after the
     coordinator had seen the process); cause found by P8 — a reference cycle in
     `ws_P5/p5lib.anch_walk` — and worked around in its own wrapper; **the fault is
     still in `ws_P5/p5lib.py`** (a finished workstream's file, left as published), as
     is a performance fault in `ws_P3/pwmodel.BandModel.sample` (it recomputes the
     transfer-matrix messages at every call); both are reported to the engineering
     division (SCI-MSG-0027 §7) and both have wrappers (`ws_P8/p8lib.py`;
     `pi_inference/nested_sampler_ext.cached_sampler`).  (viii) Logs of runs that did
     not reach their last line — two of workstream R16, eighteen superseded ones of
     P8, several of the coordinator — were moved to the session scratchpad
     (`stopped_runs/`), not deleted and not committed; they do not survive the
     container.  (ix) The first replication of the theory division's audit at
     `628d3e2` stopped in the build step with "failed to create thread": a
     virtual-memory cap the coordinator had set, not a fault of their files; re-run
     without the cap (`INDEPENDENT_VALIDATION.md` §1.11).
   * **Rules learned the hard way** (`DEAD_ENDS.md` SD39, SD43, SD45, SD48, SD49): a log
     file is committed only from a run that reached its last line, and a script cited
     in a message is re-run from a clean copy first; mathematics derived quickly in a
     well-worked field is sent as a *check*, and the word "new" waits for the prior-art
     search; when a theorem is applied on a sub-domain chosen by a heuristic, report the
     objective on the complement before calling anything certified; edit table rows by
     line; two checks with the same blind spot are one check, and a correction is not
     validated by a run that never exercises it; the fetch is a command of its own.
     From SD50–SD53: before writing "the observation" or "new", search our own
     workstream reports for it (twice in two cycles the search found it); a rule is
     not quoted next to data it does not hold for; when independent tests pass and
     one fails by a round physical constant, read the failing test first; a
     first-order estimate of a bracket is a lower estimate — break it on purpose
     before relying on it.
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
| `docs/science/ALTERNATIVE_FRAMEWORKS.md` (v2) | polytope against ellipsoid; six models of ignorance (version 2 adds the higher-order envelope with ball data and the divergence bound against a sampleable model), and what the measurements decided between them |
| `docs/science/SCIENTIFIC_FRONTIER_MAP.md` (v5.1) | twelve limitations of the science, their kind, where the programme stands |
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
   **What that means for a certified free energy (addendum A17 (6)–(7), checkpoints
   36–37; SCI-MSG-0017, -0018) [M]:** on 74 enumerated instances, with the pairwise fit of
   the solvent term the true ensemble is within `D_2 ≤ 1.3·10⁻³`, `D_∞ ≤ 3.7` of the model
   although the remainder is up to `15 k_BT` wide in sup norm — the sup norm is the wrong
   coordinate; first-order perturbation theory from the pairwise model is accurate to
   `10⁻³ k_BT`, and a one-sided floor of a few `k_BT` plus a variance of `(0.04 k_BT)²` would
   certify that (Bennett bracket, within a factor `1.0–5.2` of the truth on 53
   instances).  For a model far from the truth (the vacuum force field for serine) the
   root-mean-square remainder under the model does not predict the certified cost and
   can move the other way; for families *fitted to the solvated energy* it does, within
   a factor 2.5 in `D_2`, and no fit controls the floor (finding 9f).  *Prices computed by enumeration, not
   certificates; whether the floor can be proved is workstream P3.*
2. **The exponential price is the geometry of the first-order class, not the worst-case
   quantifier [P]** (`ALTERNATIVE_FRAMEWORKS.md`; SCI-MSG-0007).  Kernel-ball classes of
   bounded interaction order cost `≈ n^m` with matching lower bounds; the envelope wins
   where the known part is sharp; nothing cheap can stay valid on a first-order class.
3. **The headline result of the programme survives an outside review** (SCI-REV-0007,
   workstream R6, checkpoint 32): the cost of the nested adaptive algorithm (theory report
   §§11.18–11.19, "adaptive = hinted") was re-derived from scratch with identical
   constants and implemented independently; no critical or major finding; a certified
   finite-`n` separation from non-adaptive algorithms is new.  **Four reviews of the theory
   division's newest sections: no theorem false** (SCI-REV-0001,
   -0002, -0003, -0005) — **all applied by the theory division at its fourteenth
   checkpoint** (THY-RES-0007, THY-MSG-0013), which has also adopted two of our Lean
   files, our Proposition A1.1, our sandwich theorem and our field theorems as theorems
   of its report; a second-round review of the revised text is running (R9).  **The
   engineering branch was reviewed and replicated** (SCI-REV-0008, workstream R7,
   checkpoint 33): no wrong number; 254 of 263 published optima certified without a
   solver's search; two findings on the record.  **The theory division's audit passes on
   our machine** at four of its commits (`INDEPENDENT_VALIDATION.md` §§1.1, 1.4, 1.5, 1.6 — the last with its repaired mutation runner).  One displayed claim false as stated (one-line repair), one proof
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
   site; below, a "plateau twin" bounds what the datum can do, and that bound is the
   cost at the instance where it is proved, up to a constant and two units of the
   radius, in a quantile sense (Lemma A16.5, an isoperimetric inequality with an energy
   constraint; Theorem A16.6 as corrected) — for the whole class it is Conjecture A16.4.
   **Refereed at checkpoint 35 (workstream R8): no false statement; the first version's
   "exact cost" over-claimed and was corrected by a linked message (SCI-MSG-0016); the
   lemma checked over general members and machine-checked in its algebraic core; the
   conjecture survived an attempt at refutation and is open on a named interval.**
   SCI-MSG-0012, -0013, -0016.
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

9a. **Certifying a free energy against a model that can be sampled: what must be known
   a priori, and what it costs [P, author only; M for the instances]** (addendum A17;
   SCI-RES-0007, SCI-MSG-0017, -0018; with the theory division's box-class theorem, its
   §11.30).  A pointwise floor costs `e^{floor}/ε` (theirs); a Rényi divergence of order `p`
   of the truth from the model `e^{κ}/ε^{p/(p−1)}`; a Kullback–Leibler divergence `e^{Θ(κ/ε)}`;
   moments of the remainder energy alone nothing — but a floor *and* a variance give a
   bracket with no exponential cost (Bennett).  The direction matters: the divergence
   is of the truth from the model, the opposite of what a variational fit minimises.
   **Prior art read at checkpoint 39 (workstream A3; SCI-RES-0009): it *is* a
   recombination of known bounds, and most of it is in print as stated** — the cost
   table in Block and Shetty, arXiv:2602.23535 (February 2026), the bracket in Hoeffding
   (1963, Theorem 3), the chain version in Chazottes et al. (2006).  What is ours: the
   reading as a verification cost, the statement that no polynomial moment of the
   remainder suffices, a sharper product-measure bound (`D_2 ≤ Σc_i²/4`, with A3), and —
   the part no search replaces — the measured prices on real instances, which are
   small.  The use of Hoeffding's Theorem 3 as a certified second-order bound for
   free-energy perturbation was not found (Decoster, J. Phys. A 37 (2004) 9051, unread).
9b. **A certified solvated side-chain free energy beyond enumeration [P + M; checkpoint
   40]** (workstream P3, SCI-MSG-0020; addendum A17 (10); `PHYSICAL_APPLICABILITY.md` §2b).
   By analysis alone the constants of the solvent term can be bounded only with a loss
   of a factor 33–1 400 (cancellation between self and cross terms).  Evaluating the
   term on a Hamming ball about an anchor and bounding the tail gives a sandwich of
   banded pairwise models: for a twenty-residue valine peptide on PPII (`3.5·10⁹`
   assignments) `ln Z ∈ [518.2332, 518.2937]` with no sampling.  The coordinator's
   independent chain-model estimate is `518.2626 ± 0.0001`.  On the helix the certificate
   fails while the measured remainder of a fitted chain is `0.002–0.004 k_BT`: the price
   is small and the proof is missing.  "Certified" = paper proofs + interval
   arithmetic + a floating-point allowance, never violated in 5.5 million enumerated
   state checks; not machine-checked.
9c. **How often uncertified error bars are wrong, on real instances [M; checkpoint 41]**
   (addendum A17 (11); the baseline of benchmark B10): the two-standard-error bar of a
   reweighting estimate covers in 92–100 % of repetitions when `D_2 < 1` and in 5–82 % when
   `D_2 = 3–45`, missing by up to 6 nats; the two brackets with a guarantee never fell
   below 0.978; with a good model Hoeffding's Theorem 3 beats the empirical-Bernstein
   bracket by two orders of magnitude, with a poor one it loses — the floor decides.
9d. **A cooperative known part: the direction depends on the envelope [P + N; checkpoint
   43]** (workstream R10 on the theory division's workstream Y; SCI-REV-0010;
   `PHYSICAL_APPLICABILITY.md` §3a).  For a two-state nearest-neighbour chain: at one
   `k_BT` per site all three exponents are above the independent-site values (theirs;
   every bracket recomputed); at small envelopes the factor is the structure factor at
   zero wave vector (proved at second order; in general the largest variance per site
   of a Lipschitz function, *not* the susceptibility); at three to six `k_BT` per site
   the two cost exponents are **below** the independent-site values (proved from their
   own recursion; recomputed with their functions and with a third code); the threshold
   is raised at every slope.  So neither "interactions make certification harder" nor
   "the product-measure exponents are optimistic" may be said without the envelope.
   Rests on their Proposition F (re-derived by one reviewer); one model; rounding not
   controlled.  By-product for our own addendum A17 (8): the constant `¼` of the chain
   variance bound replaced by the worst two-point split of the transition law — an
   equality for the uniform field on the symmetric chain.
9e. **The theory division's share certificates on our instances, and a correction of
   finding 1 [M + P; after checkpoint 43]** (workstream P4; SCI-REV-0012).  Their
   certificate certifies 11 of the 13 analyses our row-sum condition missed; the pair
   form of the third-order lower model is tighter at every state (a median factor 6.8
   in `ln Z`); shares that depend on the state, and one linear programme from ball data,
   certify every instance the exact envelope certifies (133 of 136).  **Correction:**
   wherever the clash-free domain is not a product (Phe, Lys, the patterned sequence)
   the certificates of the rotamer measurement were stated on a greedily pruned product,
   and in 14 of 40 analyses the energy minimum is not in it (`DEAD_ENDS.md` SD45).  The
   repair — true minimiser first, then the largest reset-closed domain around it —
   certifies 13 of 40 at second order and 30 of 34 at third.  Also: with pair penalties
   at order `m` the cost number of P3's certified floor falls from 16.4 to 0.064 at
   `m = 3` (Val₆ on the strand); **the twenty-residue certificate has not been re-run
   with them** (§7 item 2).
9g. **The skeleton of the certified free energy is machine-checked — twice [V; after
   checkpoint 43]** (workstream L4; SCI-MSG-0023; and the theory division's
   `AnchoredRemainder.lean`, written in the same hour, which agrees statement by
   statement): the remainder identity at every order, the allocation lemma, the
   sandwich; and, ours only: the two-point Bennett–Hoeffding bound, the bracket, the
   certificate with its probability; a sharper upper end of the certificate
   (`W(r̄ − η − lo, σ²)`), new.  Not formal: the constants (P3's enclosures) and the
   banded models.
9f. **Benchmark B10 completed: the split matters more than the fit [M; after checkpoint
   43]** (addendum A17 (12); SCI-MSG-0022).  Independent residues and a nearest-neighbour
   chain fitted to the solvated energy in five ways on the 45 product-domain instances:
   **our prediction that fits differ by orders of magnitude in the certified cost is
   refuted for `D_2`** (at most 0.34 nats between fits; the root-mean-square remainder
   predicts `D_2` within a factor 2.5) **and holds for the floor** (up to 3.2 nats).  What
   does differ by orders of magnitude is the split: for serine, independent residues
   fitted to the solvated energy have `D_2 = 0.0015–0.096` against `4–45` for the vacuum
   force field as the model — the solvent term cancels 97 % of the vacuum pair variance
   on strand and PPII.  Hypothesis H11 is demoted accordingly (`BENCHMARK_DESIGN.md`).
   The coordinator's scripts; not replicated.

**New directions opened by workstreams**

9h. **The certificate after the fifth wave: order four, thirty residues, the frozen
   helix, populations — and a theorem about what analysis cannot do [P + M; after
   checkpoint 43]** (workstreams P5, P6; SCI-MSG-0024, SCI-MSG-0025, SCI-RES-0013 §4;
   addenda A17 (13), (14); this supersedes the last two sentences of 9b).
   (i) *Shares.*  Charging each certified tail constant to the pairs or triples of its
   subset instead of its sites is a pointwise tighter covering that keeps the models
   exactly solvable (counting lemmas; 98 million state checks, including the two
   extreme members of the certified class).  Twenty residues of valine on PPII, no
   sampling: order 5 from 0.0605 to 0.0162 (pairs) and 0.0090 (triples) nats; **order 4
   — 9 921 evaluations — `[518.2383, 518.2929]`**.  Thirty residues: strand 0.0017 nats,
   PPII 0.091.  (ii) *The theory division's sandwich sampler on our instance:*
   `[518.26231, 518.26252]`.  (iii) *The compact case.*  **No bound that uses the charges
   only through their magnitudes can see the cancellation**: Born radii do not depend on
   the charges, so such a bound must hold for every sign pattern, and sign-reversed
   versions of the real instances have remainders 16–153 times the true one at orders
   3–5 (exact evaluation; an explicit family with unbounded loss); one-sided signed
   sums stay 6–53 times above the truth; a signed reference term is the next order in
   disguise.  **Yet leucine on the helix is certified** — at thirty residues
   (`1.07·10⁹` assignments) within 0.033 nats without sampling (order 6, pair form, on
   cached evaluations) — because that ensemble keeps fewer than one side chain off
   its anchor and the pair form does not charge such assignments.  For serine, lysine
   and a patterned sequence on the helix nothing comparable holds.  (iv) *Populations.*
   A sandwich bounds the partition sum of every event from both sides, hence every
   population, sharply and with no further evaluation: all 60 rotamer populations of
   the twenty-residue instance within 1.2 %; thirty residues within 0.8 %; with the
   site form at order 4 the minor populations are not certified at all.  All of it
   model-relative, on P3's paper-proved constants; nothing machine-checked beyond the
   skeleton (9g).
9i. **The other two divisions on our reviews, and two reviews of this stretch [after
   checkpoint 43]** (SCI-REV-0013, SCI-RES-0012, SCI-RES-0013).  The theory division
   applied five of our reviews at its eighteenth checkpoint — workstream Y in its report
   with our reversal as headline, our Theorem R9.1 in place of its proposition after a
   verification beyond ours, seven Lean files of ours in its audited library — and the
   engineering division, in its first contact, verified and accepted the findings of
   our two reviews of its work and reproduced our separation table to every digit.
   Our review of the theory division's seventeenth checkpoint (workstream R12) found no
   critical error and two sentences to replace (Proposition 11.18e(b) false as written;
   the necessary order of Proposition 11.113(d) too large by `e^Δ`).  **Two corrections
   of our own came out of their checks** (SD48): the defect of numpy's binomial sampler
   begins near `5·10¹⁴` trials, not `10¹⁷` (*and lower still — between `2·10¹⁴` and
   `2.5·10¹⁴` by the theory division's second scan; linked correction SCI-RES-0016 §4*),
   and our "corrected" re-run had never exercised its correction; the sizes of our separation statement were first sizes of a grid.
9o. **The review the theory division offered at its twentieth checkpoint [P, X;
   workstream R16]** (SCI-REV-0016).  Their certified third level — serve every rung by
   the candidate of smallest certified cost — is right: a two-level run of Theorem
   11.56 designed for the fibre dimension, a *certified* accuracy at most the rung's
   and the failure probability `δ′` of the level above is an admissible inner
   procedure, and the bound is monotone in the servers' costs with the whole outer
   design fixed.  **159 of 159 certified numbers replicated** with code that imports
   nothing of theirs.  One major finding: five of eight two-level worst cases in their
   table belong to a two-level design with another ladder (ENG-RES-0008) than the
   outer design they are compared with.  Three minor.  New: the two-level run on the
   zero function is deterministic, so its cost is exact — against it the comparison
   is a theorem from `n = 16 000` on and false at `4 000`, `8 000`.
9n. **The charged case [P + X for workstream P8's theorem and validation; P + M for the
   coordinator's additions; unrefereed]** (SCI-MSG-0027; addendum A17 (18);
   `workstreams/P8_REPORT.md`).  *P8:* the slack of workstream P3's constants for
   charged side chains is the maximum over host rotamers taken ingredient by
   ingredient; P3's theorem evaluated state-wise plus Theorem AH (each term expanded
   in an order with its hosts last) gives `βΓ_m = 34.0, 2.40, 0.136` for Lys₁₂ at
   orders 4, 5, 6 (was 689, 145, 23.4).  *Verified by the coordinator* (theorem
   re-derived, hypothesis sharpened to `m` hosts; an exact test with controls; every
   state of three enumerated instances; 4 250 random states of Lys₁₂; nine brackets by
   another driver); the constants were recomputed by nobody.  *The coordinator:*
   (i) what looked like the band's limit was the split of the pairs beyond the band;
   **split around the anchor** (exact whenever the kept site is at its anchor):
   Lys₁₂ certified within **0.057 nats** at order 5 (was 0.192); serine gains 7–12 %,
   valine nothing.  (ii) The theory division's nested sampler: **Lys₁₂ to `3·10⁻⁵`
   nats at probability 0.95 with 60 evaluations** beyond the ball (`9.5·10¹⁰` states) —
   and to 0.006 nats from the order-4 ball plus 12 000 evaluations (`1.1·10⁵` in all;
   its interval contains the order-5 ones);
   **(LKSE)₃, certified only within 4.3 nats, to 0.041 nats** with 12 000 evaluations.
   (iii) Ser₂₀ (`8·10¹⁵` states) certified within 0.253 nats at order 5; Leu₃₀ at order
   6 with optimal site shares within 0.0105 nats.  **The frontier is now the
   mixed-charge sequence deterministically (its constants: `βΓ₅ = 43`), charged chains
   beyond twelve residues (the state-wise constants have no closed form over the
   subsets), and — unchanged — that every bracket is model-relative and unchecked by
   an independent implementation.**
9m. **The review the theory division asked for at its nineteenth checkpoint [P, N;
   workstream R15]** (SCI-REV-0015).  Nothing false in Proposition 11.18e(b′)(i),
   Propositions 11.18f and 11.113a, the Lean statement behind Corollary 11.114, or the
   necessity argument of Proposition 11.113(d); twelve conditions to add.  What it
   found that we use: the nested sampler's proposal term is `t_f`, not `2t_f` (two
   ends), under a sampling scheme that our script happens to follow; the first-order
   allocation rule is safe for the ceiling and, for the floor, only while the charged
   site keeps the largest `f − γ` of its subset — the same water-filling the
   coordinator found on a real instance.  Their audit at `f7df44f` passes here.
9l. **Two statements of the theory division run on real instances: a sampler that
   pays for the envelope, and which shares [P theirs, unrefereed; P ours, elementary,
   one part V; M; the coordinator's runs, unrefereed]** (addendum A17 (17);
   SCI-RES-0017).  *Their nested sampler* (Proposition 11.113a: propose from the
   solvable sandwich, evaluate only with probability `ρ`, so evaluations pay for the
   envelope) is validated by enumeration and meets their stopping condition:
   twenty-residue valine, order 4, 1 200 evaluations, `1.2·10⁻³` nats against the plain
   sampler's `4.3·10⁻³`.  Its gain is at most `0.88/E_q ρ` with Hoeffding half-widths,
   `E_q ρ ≈ p^{m−k}`.  Two changes of ours — one known mean (`c = β + ρ/2`), and the
   empirical Bernstein bound, now read in its source — give `2.7·10⁻⁴` nats there and
   **`[227.368462, 227.368935]` for the serine helix at twelve residues: `4.7·10⁻⁴` nats
   at probability 0.95 from the order-5 ball and 1 200 evaluations.**  *Their
   allocation rule* (Proposition 11.18f(c): each constant to the most frozen site of
   its subset) is exact for the lower end and breaks the upper end where a site's
   penalty exceeds the cost of changing it (Leu₁₂, order 5: 8.6 nats against 3.2).
   **The site allocations are the core of a convex game** — vertices are orderings,
   equal shares are the Shapley value, their rule is the greedy vertex (optimal at
   first order: machine-checked, `pi_inference/lean/CoreGreedy.lean`) — and since
   `ln Z` of the floor is convex in the penalties, **the best floor is a convex
   programme with their rule as oracle** (Frank–Wolfe; closed-form sums on nested
   sets and transfer-matrix marginals, so it runs beyond enumeration): `0.0075` nats
   at order 5 on Leu₁₂ where equal shares give 3.7 and equal pair shares 0.047; at
   order 6 the rule alone turns 0.31 into `3.9·10⁻⁵`.  A water-filling bound against
   the off-anchor marginals says beforehand when the site level cannot work, and its
   minimiser is the optimum in closed form where it covers.  Twenty residues at
   order 6: `0.0087` nats with one-body penalties (equal site shares 0.63, equal pair
   shares 0.016), nearly all of it P3's reduction of evaluated terms; details and
   the cases where the site level cannot work: addendum item 56.
9k. **Two requests of the theory division answered by workstreams [after checkpoint
   43]** (SCI-REV-0014, SCI-RES-0014).  *R13:* their rate for the level recursion,
   `τ_k − h ≤ c₁/(k + c₂)`, is correct in every line and is now machine-checked on top of
   their three lemmas (exact recursion of the cube, every slope; the sequence at
   accuracy zero is ours); the bound is `O(1/k)`, the cube behaves like `1/k²`.  Their
   Proposition 11.117(b) dropped the hypothesis "symmetric" of our R10.1 and is false
   without it.  Our five reviews were applied correctly; five small slips of our own
   texts were found and corrected by linked notes.  *P7:* the instances on which share
   certificates fail (integrality gaps) are certified by shares after branching on one
   site in four of five analyses, at depth two in the fifth; gaps occur in 1 % of our
   pairwise models and are shallow; "shares at the leaves" is a term of the theory
   division's own certificate type and thirteen real certificates are accepted by
   its checker.
9j. **The certificate reaches a compact ensemble that is not frozen; its frontier is
   charge [V for the lemma; P elementary + M for the rest; the coordinator's,
   unrefereed]** (addenda A17 (15), (16); SCI-MSG-0026).  *What a sandwich costs* (Lemma
   A17.16, machine-checked: `pi_inference/lean/SandwichCost.lean`): for
   `m₋ ≤ E ≤ m₊` the bracket is the mean band under the true ensemble to first order;
   the ceiling's defect is first-order always, the floor's carries an exponential.
   Hence a rule — bracket ≈ `2β⟨penalty⟩`, `2 p^k Γ_m` for `k`-shares and independent
   sites — by which a certificate is costed before its evaluations are paid for, and
   its limit: when `βΓ_m` exceeds the cost of leaving the anchor the floor delocalises
   (leucine, order 4: rule 0.0006 nats, bracket 187; the lower end still within 0.0008
   of the exact value).  *Exact window terms:* evaluated terms that fit a window of
   the transfer matrix are kept exact instead of reduced to pair tables
   (`pi_inference/window_model.py`; checked against enumeration at every state of 189
   sandwiches).  **Ace-Ser₁₂-NMe on the helix — `4.9·10⁹` assignments, 6.3 of 12 side
   chains off the anchor — is certified within 0.077 nats without sampling at order
   5 and within 0.012 at order 6** (`[227.362266, 227.373868]`; 0.0007 with 2 000 points
   of the theory division's sampler);
   no allocation of shares rescues order 4 (the envelope itself: 0.27 nats at six
   residues).  Leu₁₂ on the helix with triple shares: 0.00036 nats at order 5.  **For
   twelve residues on the helix serine, leucine, phenylalanine are in reach; lysine
   and the patterned sequence are out of reach at every affordable order** — the
   ratio of certified constant to true remainder is 10²–10³ for all side chains, the
   true many-body term of a charged group is about twenty times larger per subset.
   Not done: twenty residues for serine (order 5: `4·10⁶` evaluations); the leucine
   helix at thirty residues with triple shares; anything charged.
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
record-keeping; later ones are SD38–SD43 of `DEAD_ENDS.md` (a "sharpening" that was not
one; a log from an aborted run; an "exact cost"; a clause false beyond the junction;
small numbers; and, at checkpoint 39, **a cost table sent to the theory division as our
extension of its result before the prior-art search had returned — it was in print**).
Rule added: mathematics derived in an afternoon in a well-worked field is sent as a
*check* of the collaborator's statement; the word "extension" waits for the search.  Rules adopted, in force: fetch, read, *then* write the commit message;
header times from `date -u`; a physical reading is published one checkpoint after the
statement it reads; when a workstream finalises a report after a message was drawn from
it, diff the message against the report's change list; summary tables and headings are
refereed as statements; in-progress workstream files are snapshots, not statements.

## 5. Workstreams of the second to seventh wave: what each was for, and where it ended

| id | brief | on completion |
|---|---|---|
| R6 | `workstreams/R6_brief.md` — independent line-by-line review, with own re-derivation and implementation, of the cost of the nested adaptive algorithm (theory report §§11.18–11.19) | **done at checkpoint 32** — the cost accounting stands (no critical or major finding; eight minor points; a certified finite-`n` separation; a sampler bias).  Coordinator: separation table re-run, lower-bound columns recomputed independently, central count re-derived, sampler bias confirmed.  Published as SCI-REV-0007; `PUBLICATION_OPPORTUNITIES.md` P1 updated |
| P2 | `workstreams/P2_brief.md` — class constants of the GBn2 term in *rotamer* variables on a fixed backbone | **done at checkpoint 31** — `P2_REPORT.md`; end-to-end check re-run; published as SCI-MSG-0015; `PHYSICAL_APPLICABILITY.md` §2a, `BENCHMARK_DESIGN.md` B1, frontier map hypothesis 3 updated |
| L2 | `workstreams/L2_brief.md` — Lean: addendum A11 (Holley sandwich), the referee's finite inequalities, Proposition A1.2 items 1–3 | **done at checkpoint 29** — 178 theorems, re-compiled; labels changed to [V] in the addenda and the status file; two corrections of Proposition A1.2; published as SCI-MSG-0014 |
| R7 | `workstreams/R7_brief.md` — independent review and replication of the engineering division's results (the first review of that branch by us beyond its class tables) | **done at checkpoint 33** — no wrong number; class tables, covers and the Harper closed form replicated; 254 of 263 optima certified without a solver's search; two findings (the two-solver validation cannot be regenerated; floating point at its limit at 13 torsions of the off-lattice chain).  Coordinator: M1 verified on the engineering branch; the Harper table re-run.  Published as SCI-REV-0008; `INDEPENDENT_VALIDATION.md` §1.3 |
| F | `workstreams/F_brief.md` — the two-oracle model with a field (report: `SF_REPORT.md`) | **done at checkpoint 30** — the coordinator's conjecture is true as a statement and false as an explanation; Theorems A, B (class exponents unchanged, every `n`); instance-wise bracket; `k = 2` exact at `n = 13`; tolerance theorem; comparison with theory report §11.29.  Coordinator re-derived the lemmas, Theorem A, the algebra of B and the tilt inequality; re-ran the exact-rational check; own check `pi_inference/compensation_lemma_check.py`.  Published as SCI-RES-0006 |
| R8 | `workstreams/R8_brief.md` — adversarial referee of addendum A16 (the mean-energy datum at extensive accuracy: entropy bracket, plateau twin, isoperimetry with an energy constraint, the conjecture); launched at checkpoint 28 because A16 had no second reader | **done at checkpoint 35** — no false statement; Theorem A16.6 (ii)–(iii) over-claimed and proved after the referee's repairs (quantile form, matching inequality, tolerant test); the printed algorithm of SCI-MSG-0013 lacked a gauge; one of our scripts aborted before its cited output (repaired; data identical); Lean core of Lemma A16.5; the conjecture not refuted; non-adaptive lower bound with the datum.  Coordinator: R8.2, R8.3 re-derived, Lean file compiled, two scripts re-run.  Published as SCI-MSG-0016 (linked correction) |
| P3 | `workstreams/P3_brief.md` — a floor by analysis: certified third-order constants of the GBn2 term in rotamer variables without enumeration; tightness against P2; the theory division's cost number `Z(m)/Z(g) − 1`; one certified `ln Z` beyond enumeration size | **done at checkpoint 40** — analysis alone fails by cancellation (33–1 400 times too large); ball of evaluations + term-by-term tail = a certified sandwich on extended backbones; Ace-Val₂₀-NMe on PPII certified within 0.06 nats without sampling; fails on the helix.  Coordinator: statements re-derived; own script; three re-runs (identity, OpenMM validation, one enumerated instance); the twenty-residue value replicated independently by a chain model (`518.2626 ± 0.0001`).  Published as SCI-MSG-0020; `PHYSICAL_APPLICABILITY.md` §2b; `OPEN_PROBLEMS.md` D6; status S48 |
| L3 | `workstreams/L3_brief.md` — Lean: the compensation lemma and Theorem A of workstream F (the theory division's request F-T2); the rearrangement step of Lemma A16.5; items of Proposition A1.1 | **done at checkpoint 39** — Lemmas 0–3 and Theorem A (all three displays) machine-checked with nothing assumed; A16.5 given Harper; A1.1 items 1–2; re-compiled by the coordinator (four exit codes 0; standard axioms); ten statements read in the files; published as SCI-MSG-0019; status S47; two notes added to `SF_REPORT.md` |
| A3 | `workstreams/A3_brief.md` — prior art, full text where accessible, for the box-class result and for addendum A17 | **done at checkpoint 39** — nearly everything is in print; 20 passages re-read by the coordinator; A17 corrected in place; `PRIOR_ART_MATRIX.md` row filled; published as SCI-RES-0009 (linked correction of SCI-RES-0007 §3, SCI-MSG-0017, -0018); `DEAD_ENDS.md` SD43; status S46 |
| R9 | `workstreams/R9_brief.md` — second-round review of the theory report at `658b77f` against our five reviews; the theory division's amendments; statements written while applying the reviews; the exact-semigroup sketch for bridges | **done at checkpoint 38** — all applied correctly; three corrections of our own texts (`DEAD_ENDS.md` SD38 extended, SD41, SD42); one new false sentence and eight minor defects in theirs; **Theorem R9.1**: the concatenation error of bridges is a coboundary, the limit shape a Newton–Okounkov body, the profile count `vol(𝒦)N³`, `vol 𝒦 ≥ 1.6313`.  Coordinator: (a) re-derived; the C checker recompiled and re-run to 11 beads; the certificate script re-run.  Published as SCI-REV-0009  **Follow-up (after checkpoint 43; SCI-REV-0011, `R9_ADDENDUM.md`):** their Proposition 11.69b, written without Theorem R9.1, agrees with it; nothing false; three replacement texts; "two beads at either end suffice" fails from 12 beads on (counter-example checked by the coordinator from coordinates) |
| R10 | `workstreams/R10_brief.md` — independent review and replication of the theory division's workstream Y (a Markov-chain known part raises the exponents?) | **done at checkpoint 43** — proofs stand; every bracket at `u = 1` recomputed with own code; **M1: the direction depends on the slope** (`a` lowered at `u = 3, 4, 6`, `h` at `u = 4, 6`; `E` raised everywhere); twelve minor points; Propositions R10.1, R10.2 (small-slope law = structure factor for ferromagnetic chains), R10.4 (the reversal), Conjecture R10.3.  Coordinator: R10.1, R10.2 re-derived (a sign corrected); their functions re-run at two cells; a third code on exact chains (`pi_inference/r10_reversal_check.py`); a sharper constant for addendum A17 (8) (`a17_8_sharp_constant_check.py`).  Published as SCI-REV-0010; `PHYSICAL_APPLICABILITY.md` §3a; `DEAD_ENDS.md` SD44; status S51 |
| P4 | `workstreams/P4_brief.md` — requested by the theory division: its share certificates on our instances; site against pair form of the third-order lower model; review of Theorem 11.18a, Propositions 11.18b, 11.18c | **done after checkpoint 43** — 11 of 13 certified; pair form tighter at every state of 136 instances (median factor 6.8 in `ln Z`); Proposition 11.18c(a) false for the completeness half of 11.18b (counter-example); state-dependent shares and a joint LP; **a correction of our own P2 result** (pruned domains, `DEAD_ENDS.md` SD45); the pair form at order `m` for P3's sandwich.  Coordinator: both propositions read, counter-example and the domain finding recomputed (`pi_inference/p4_adoption_check.py`), five scripts re-run, Lean copies re-compiled.  Published as SCI-REV-0012; status S53 |
| L4 | `workstreams/L4_brief.md` — Lean: the remainder identity, allocation lemma and sandwich of P3 at order `m`; the two-point Bennett–Hoeffding bound requested by the theory division | **done after checkpoint 43** — three files, 176 theorems, standard axioms; a sharper upper end of the certificate found and machine-checked; Part A turned out to be an independent second formalisation (the theory division's `AnchoredRemainder.lean`, same hour; they agree).  `L4_REPORT.md` was **written by the coordinator** (process note at its head).  Coordinator: all files re-compiled, 15 theorem statements and 7 definitions read, their file read and a copy compiled.  Published as SCI-MSG-0023; status S55 |
| P5 | `workstreams/P5_REPORT.md` (brief: `P5_brief.md`) — the compact case (`OPEN_PROBLEMS.md` D6) | **done, published as SCI-MSG-0024.**  The proposed route (one-sided signed group sums) is closed: gain 2.2–4.4 where 10–100 was needed; every bound that ignores the signs of the charges is 16–153 times the true remainder at orders 3–5 for leucine on the helix (theorem + exact evaluation of sign-reversed systems; open at order 6 and for serine); a signed reference term is the next order in disguise.  The leucine helix certified at 12–30 residues by P3's pipeline at order 6 with site penalties (`ln Z ∈ [866.6507, 867.3804]` at thirty). Coordinator's check: `pi_inference/p5_adoption_check.py` (own code, identical numbers) |
| P6 | `workstreams/P6_REPORT.md` (brief: `P6_brief.md`) — pair penalties in P3's certified sandwich; the theory division's sandwich sampler; beyond the brief: triple shares | **done, published as SCI-MSG-0025.**  Twenty residues on PPII: order 5 0.0605 → 0.0162 (pairs) → 0.0090 (triples) nats; **order 4 suffices with triples (`[518.2383, 518.2929]`, 9 921 evaluations)**; thirty residues: strand 0.0017 nats, PPII 0.091; the sampler: `[518.26231, 518.26252]`; helix: poly-Leu rescued at order 5 by the pair form, nothing else.  Coordinator's checks and addition: `pi_inference/p6_adoption_check.py`, `sampler_precision_check.py`, `certified_populations.py` (addendum A17 (13): certified populations) |
| R12 | `workstreams/R12_REPORT.md` (brief: `R12_brief.md`) — requested by the theory division (THY-RES-0010 §9.2): review of its corrected Theorem 11.110(e), Propositions 11.18e and 11.113, Corollary 11.114, Theorem 11.18d as written, `BarrierCertificate.lean` and Theorem 11.115 against our workstream K's formats | **done, published as SCI-REV-0013.**  No critical finding; two major (Proposition 11.18e(b) false as written; the necessary order of Proposition 11.113(d) too large by `e^Δ`); eleven minor; seven statements machine-checked on their definitions (`experiments/science/ws_R12/lean/R12Additions.lean`).  Coordinator's check: `pi_inference/r12_adoption_check.py`; the Lean file compiled; two scripts re-run from a clean copy |
| R13 | `workstreams/R13_REPORT.md` (brief: `R13_brief.md`) — requested by the theory division (THY-RES-0011 §9(a)): referee of its rate for the level recursion; how our five reviews were applied at `63e36f7` | **done, published as SCI-REV-0014.**  The rate is correct and machine-checked by the workstream (`ws_R13/lean/RateFull.lean`); Proposition 11.117(b) needs "symmetric"; twelve corrections of record in their texts, five in ours.  Coordinator: statement (a) re-derived, both Lean files compiled, the counter-example recomputed |
| P7 | `workstreams/P7_REPORT.md` (brief: `P7_brief.md`) — requested by the theory division (THY-RES-0011 §9(c)): are the instances with an integrality gap certified by shares after branching on one site, or by one triplet constraint | **done, published as SCI-RES-0014.**  Four of five yes, Leu₁₆/PPII at depth two; one or two triplets close all; 18 gaps in 1 732 models; thirteen certificates accepted by the theory division's `verify` under `#eval`.  Coordinator: an independent checker on all nine tree certificates, brute-force minima, the gaps by an own linear programme |
| P8 | `workstreams/P8_REPORT.md` (brief: `P8_brief.md`) — the charged case: P5's measurement for lysine and the patterned sequence; P3's cross bound for far pairs; which lever | **done, verified, published as SCI-MSG-0027** (finding 9n): the slack is the host step; state-wise constants and Theorem AH; Lys₁₂ certified at order 5 |
| R14 | `workstreams/R14_brief.md` — adversarial referee of the coordinator's addenda A17 (13)–(16) | **not done** — terminated at launch by a platform safeguard; not relaunched (§0) |
| R15 | `workstreams/R15_brief.md` — requested by the theory division (THY-RES-0012, requests 1 and 3): review of its Propositions 11.18e(b′)(i), 11.18f, 11.113a, of `ratio_expected_queries_ge_mixed` against Corollary 11.114(d), of the necessity argument of Proposition 11.113(d); our one-known-mean bound; the conjecture (b′)(ii) as a question | **done, published as SCI-REV-0015.**  Nothing false; twelve conditions to add; `t_f` for `2t_f` in the nested sampler's bound; the range of validity of the first-order allocation rule |
| R16 | `workstreams/R16_REPORT.md` (brief: `R16_brief.md`) — offered by the theory division (THY-RES-0013 §6): review of its certified third level (the admissibility of a two-level run as an inner procedure of Theorem 11.56; the monotonicity argument), with a replication | **done, published as SCI-REV-0016** (finding 9o): the rule holds; 159 of 159 numbers replicated; one major finding (five two-level worst cases attributed to the wrong design), three minor |

Workstream files under `experiments/science/ws_*/` and `*_REPORT.md` are committed as
snapshots while a workstream runs; they are statements of the division only once the
digest, a `SCI-*` message or the validation record cites them.

## 6. Outstanding requests to the other divisions

The full table is in `status/science.md`; the ranking with reasons is SCI-MSG-0021 (second
edition; the first was SCI-MSG-0010).  **To the theory division**, most of what was
ranked first has been answered (the stopping rule, the headline of §11.25, P-T3, X-T1,
K-T1/K-T2, the field case, the prior art of §11.30, P3-T1…T4, P2-T1…T4); open and worth
their time now: the slope map of workstream Y (R10-T1…T3), Proposition 11.18c(a) and the
state-dependent shares (P4-T1, P4-T3), `BennettTwoPoint.lean` (L4-T1), the compact case
(which they have taken into their own list of open problems).  **To the engineering
division**, nothing has been answered: a stand-alone checker of the sandwich
certificate and a compiled evaluator with a proved rounding bound (P3-E1, P3-E2), a
buried environment (P2-E1), exact arithmetic for the off-lattice chain at 13 torsions
(R7-ENG-3), native certificates against pseudo-Boolean proofs (E-1), bridge tables
(R3-E1, R9-E1), the vertex enumeration that decides the crossover of workstream Y
(R10-E1).

## 7. What to do next, ranked (revised 2026-11-26 after the fifth wave and after addenda A17 (16), (17), (18); items 2 and 3 rewritten)

1. **Done at checkpoint 43: R10** (the theory division's workstream Y; SCI-REV-0010;
   finding 9d).  Done by the coordinator right after it: the law at *fixed length* for the
   Zimm–Bragg chain with any `s` (it is associated, so R10.2 applies) — a closed form for
   the infinite chain, `S_∞ = (1+s)/√((1−s)²+4σs)`, and exact tables for peptide lengths,
   where the factor is limited by the length (`11.5` at 20 residues for `σ = 10⁻³`, not `32`)
   and the second-order regime ends at `0.14 k_BT` per residue (`PHYSICAL_APPLICABILITY.md`
   §3a; `pi_inference/helix_coil_structure_factor.py`).  What is left, in order of value:
   (i) Conjecture R10.3 in its proper order of limits (first `n → ∞`) for chains with a
   field: upper side from their Proposition F at second order — whose site form takes a
   maximum over the previous letter where the truth has an average, so the block form is
   needed — lower side from block fields (`OPEN_PROBLEMS.md` I8); (ii) the crossover slope (I7; a vertex
   enumeration for blocks of four and five sites decides it — request R10-E1, or a
   double-description code of our own); (iii) a hidden-Markov reference for the
   tilt-state recursion, which by the period-four argument is necessary for any upper
   bound below the cube.  None of the three was started.
2. **The certificate line (`OPEN_PROBLEMS.md` D6, D9) — where it stands, and what is left
   in order of value** (findings 9h, 9j).  Done since checkpoint 43: pair and triple
   shares (order 4 suffices at twenty residues; thirty residues certified), the
   compact case settled in the negative for bounds and in the positive for the
   frozen leucine helix (thirty residues, 0.033 nats), certified populations, a lemma
   that costs a sandwich before it is paid for, exact window terms, and with them a
   compact ensemble that is *not* frozen (serine, twelve residues, 0.012 nats); and
   (finding 9l) the theory division's nested sampler on our sandwiches (the serine
   helix within `5·10⁻⁴` nats at probability 0.95 from the order-5 ball) and optimal
   site shares (the core of a convex game; Frank–Wolfe).  Left:
   (a) **the charged case** (findings 9j, 9n): **done for the homopolymer** — Lys₁₂ is
   certified within 0.057 nats at order 5 and sampled within `3·10⁻⁵` (workstream P8's
   constants, the split around the anchor, the nested sampler).  Left, in order of
   value: (i) **penalties resolved by rotamer state** (P8's request P8-E4: in the proof
   of Theorem AH the host states are those of the state itself before the maximum is
   taken; a site or pair penalty table that keeps the dependence fits the band models
   as they are; the room is four to five orders of magnitude in Boltzmann mean) — the
   natural next workstream; (ii) **the state-wise constants beyond twelve residues**
   (no closed form over the subsets; P8's hybrid — closed form with anchored hosts
   minus an enumerated correction inside a window — is proposed, not run), then a
   charged sequence at twenty residues; (iii) **the mixed-charge sequence
   deterministically** (`βΓ₅ = 43` for (LKSE)₃; its remaining constants sit on neutral
   pairs, where a sign-blind bound cannot be sharp — the open problem of finding 9j);
   (iv) the first-order-optimal split of a far pair (a Kantorovich dual; the split
   around the anchor is one feasible point); (v) optimal site shares (finding 9l) on
   the models with the new split;
   (a′) **the referee of our own certificate work** (addenda A17 (13)–(18)): not
   done — workstream R14 was stopped at launch by a platform safeguard (§0); needs
   the research owner's decision; if a review is made, its findings go out as a
   linked message, as SCI-MSG-0026 says;
   (a″) reach of the neutral mobile case: **done at twenty residues.**  Serine,
   `8.2·10¹⁵` states, order 5 (ball 3 963 696 evaluations, 78 minutes): certified within
   0.253 nats (the refined rule had said 0.210 plus the reductions), and with the
   nested sampler **`[347.155238, 347.156272]`, `1.0·10⁻³` nats at probability 0.95** —
   the envelope bracket, the width as the theory division states it and the width
   with one known mean were all predicted before the ball existed (research log,
   cycles 56 and 58; addendum A17 (18), item 62a).  For a mobile ensemble at this
   length use `nested_sampler_p3table.py` (a table of all constants: 24 minutes), not
   `nested_sampler.py` (one closed-form sum per distinct changed set: hours).  Left:
   **thirty residues — requested from the engineering division (A18-E3, SCI-RES-0019
   §6) with a registered prediction** (research log, cycle 58: certified bracket about
   0.5 nats, sampled about `2·10⁻³`, envelope 0.072; `βΓ₅ = 1.0020` measured; ball
   20 535 246 evaluations, table 142 506 constants, about 40 CPU-hours; the library
   needs 8-bit states at that size); other neutral sequences;
   (a‴) **optimal shares beyond the site level** (finding 9l; `OPEN_PROBLEMS.md` D9(i)):
   the pair level, where the linear oracle is "the least probable pair of each
   subset" and no longer a sort — an ordering-induced family needs `O(n²)` closed-form
   sums per vertex; a fully-corrective Frank–Wolfe to save closed-form sums (one sum
   costs seconds at thirty residues); the nested sampler with an optimally allocated
   outer sandwich; the leucine helix at twenty and thirty residues with
   triple shares (needs the closed-form sums of all in-band triples: hours);
   (b) **turn "certified" into checked**: the stand-alone checker (engineering, P6-E1 =
   P3-E1, accepted in principle; specification SCI-MSG-0025 §8) and the share lemmas in
   Lean (theory, P6-T1) — without them every bracket rests on unreviewed arithmetic;
   (c) reach: the sparse ball (P6-E2: three lines of proof, not implemented) for fifty
   residues and more — with the caution of P5's §3.3 and of A17 (16): the far subsets'
   constants are what is too large, for leucine certainly; (d) observables beyond single-site populations (pair and block
   events, order parameters) and, with them, benchmark B3/B4: what averaged data add to
   a certified population; (e) the loose end of two standard errors between two
   samplers (A17 (10), note).
3. **Workstream P8 is read, verified and published** (SCI-MSG-0027; item 2(a) says what
   is left).  R13, P7, R15, R16 are published (SCI-REV-0014, SCI-RES-0014, SCI-REV-0015,
   SCI-REV-0016); what they leave
   for us: nothing owed; offered to the theory division — `rate_zero`, the conditional
   Corollary A (each only if they say they want it), and Lemma A17.16 in Lean, which
   exists (`SandwichCost.lean`).  The crossover map
   of workstream Y (their request (b), our R10-T2) when the engineering division's
   enumeration R10-E1 exists — or with a double-description code of our own.
   **Benchmark B10 is done**, charged and aromatic side chains included (A17 (12) item
   25); left of it: a banded family of width 3 as a sampleable model on PPII, and a
   buried environment (request P2-E1).
4. **Conjecture A16.4** where it is genuinely open: an algorithm with the mean-energy
   datum on the whole class for accuracies between `ε₁ᶜ` and `a(u)`, or a lower bound
   there; the lemma for a general reference instance; the non-adaptive upper bound
   (requests T-R8-1…3 are with the theory division).
5. **A physical instance of certified inference from averaged data** (`BENCHMARK_DESIGN.md`
   B3, B4) on the rotamer model, with maximum occurrence as practised as baseline.
6. **Done at checkpoint 40:** the refreshed ranking of the open requests (SCI-MSG-0021)
   and frontier map version 5.  What remains of this item: when either division
   answers, close or re-rank in `docs/collaboration/status/science.md`.
7. **The final handoff:** keep this file current at every checkpoint; a last
   synchronisation; a last push; a clean working tree.

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
* **Replicating the theory division's audit at one of its commits** (done at `5ed4072`,
  `658b77f`, `b2d3e9c`, `24a3c27`): outside the repository,
  `git archive <commit> | tar -x -C <dir>`; `mkdir <dir>/.lake; ln -s <repo>/.lake/packages <dir>/.lake/packages`
  (valid while `lean-toolchain`, `lake-manifest.json`, `lakefile.lean` are unchanged — check
  with `git diff`); optionally copy an earlier `.lake/build` to save the first build;
  then `cd <dir>; bash scripts/audit_all.sh` (about 30 minutes on 4 shared cores; the last
  stage, mutation tests, prints nothing for 15 minutes).  Copy the log to
  `experiments/science/audit_replication/`.  Nothing of the theory branch is modified.
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
