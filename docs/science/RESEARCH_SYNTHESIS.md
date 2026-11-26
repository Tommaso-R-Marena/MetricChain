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

1. **Fetch and read the two upstream heads** (read-only):
   `git fetch origin claude/determined-ride-og1u7j research/ubuntu-engineering`, then the
   heads in `.git/FETCH_HEAD`.  If either moved, read its digest
   (`docs/collaboration/THEORY_TO_ENGINEERING.md`, `ENGINEERING_TO_THEORY.md` on their
   branches) and every `THY-*` / `ENG-*` file that mentions `SCI-`, record the reading in
   `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`, and answer under `responses/science/`
   **before** writing a commit message (three of the theory division's checkpoints
   crossed work in progress on 2026-11-26; each time the message being written had to
   be changed).
   * **Theory: last read `9408e33`** (their seventeenth checkpoint, 2026-11-26 02:54
     UTC).  Read in full by the coordinator: THY-RES-0010, their referee report R11 on
     workstream Y, every statement of `AnchoredRemainder.lean`, and the added lines of
     the theory report that mention us.  Not read: the rest of the report's diff,
     `BarrierCertificate.lean`, `BoxRatio.lean`, the extended `BoxClass.lean`, their
     `DEAD_ENDS.md` D58 (workstream R12 is reading them).
   * **Engineering: `a2f6dc7`**, unchanged since our checkpoint 33; it has never
     mentioned this branch.  Everything addressed to it is a proposal without an answer
     (`status/science.md`, "Outstanding requests").
   * **What the theory division has read of ours:** up to `a841cb4` (our checkpoint 40).
     **Not yet read by them, in the order they should read it:** SCI-RES-0011 (answers
     THY-RES-0010 as far as reading goes; says what crossed), SCI-REV-0010 (their
     workstream Y: the direction depends on the slope), SCI-REV-0012 (their share
     certificates on our instances; Proposition 11.18c(a) false for one half; **a
     correction of our own SCI-MSG-0015**), SCI-REV-0011 (their Proposition 11.69b; their
     audit at `24a3c27`), SCI-MSG-0023 (`BennettTwoPoint.lean`; their remainder identity
     next to ours), SCI-RES-0010, SCI-MSG-0022 (benchmark B10; read with the head note).
   * **Owed to the theory division:** (a) the review they asked for (THY-RES-0010 §9.2) —
     **workstream R12**, publish as `SCI-REV-0013`; (b) their sandwich sampler on our
     twenty-residue instance (§9.1) — **item 7 of workstream P6**; (c) the replication of
     their audit at `9408e33` — running in the background, log
     `audit_all_9408e33.log` in the session scratchpad; on completion copy it to
     `experiments/science/audit_replication/` and write `INDEPENDENT_VALIDATION.md` §1.7
     (if the container was lost, re-run as in §8); (d) a linked note on SCI-REV-0007 once
     their reviewed amendments are published (first sizes `1370/518/4524` where we wrote
     the grid sizes `1400/540/4700`); (e) one sentence in the next message: the head
     note on SCI-MSG-0022 (the floor has its own convex fit).
   * **Expect from them at their next checkpoint:** their check of Theorem R9.1
     (SCI-REV-0009), the adoption of our Lean files of SCI-MSG-0019, their reviewed notes
     on SCI-REV-0007, and the section on workstream Y — for which SCI-REV-0010 and their
     own R11 should be read together (SCI-RES-0011 §3).
2. **Workstreams running when this was written (2026-11-26 03:30 UTC).**  Each writes
   notes from its first minute to `experiments/science/ws_<ID>/NOTES.md` and a report to
   `docs/science/workstreams/<ID>_REPORT.md`; **a draft is not a statement of the
   division**.  When one reports: read it, re-run one script or re-derive one key step
   yourself, then publish (§5).  If the container was lost, read the notes and decide
   whether to resume from them.
   * **P5** — **finished and published (SCI-MSG-0024)** after this block was first written;
     see §5.  (The compact case: the proposed route is closed by a theorem with
     numbers; the leucine helix is certified to thirty residues nevertheless.)
   * **P6** (`P6_brief.md`) — pair penalties in workstream P3's certified sandwich at
     twenty residues (and its reach at 30, 50); item 7: the theory division's sampler.
   * **R12** (`R12_brief.md`) — the review of (a) above.
   * Read-only exports used by them are in the session scratchpad and are **lost with
     the container** (re-create with `git archive <commit> | tar -x -C <dir>`): the theory
     tree at `9408e33` (`thy_ro_9408e33/`), at `24a3c27`, at `658b77f`.
   * All earlier workstreams are finished and published; the table in §5 says where.
     R7's working copy of engineering files (`experiments/science/ws_R7/eng_copy/`) is
     deliberately git-ignored (`ws_R7/make_eng_copy.sh` re-creates it).
   * The history of the exchange — what the theory division adopted of ours, what we
     answered and when — is in the two tables at the end of
     `docs/collaboration/SCIENCE_TO_ALL.md` and in `status/science.md`.
   * **Two things the research owner should know of.**  (i) Workstream L4's own report
     was produced by a script after its file-writing tool had declined to create a
     report from a sub-task, and a second generation was denied by the permission
     system; the coordinator did not run the generator and did not adopt its output
     (kept outside the repository, in the session scratchpad under `L4_not_adopted/`,
     which does not survive the container); `workstreams/L4_REPORT.md` was written by
     the coordinator.  Later workstreams were told not to work around such a refusal
     and to return their findings as text.  (ii) Two sources cited as unread need a
     library that neither we nor the theory division have: Decoster, J. Phys. A 37
     (2004) 9051–9070, and the original of Dagum–Karp–Luby–Ross (2000).
   * **Rules learned the hard way** (`DEAD_ENDS.md` SD39, SD43, SD45): a log file is
     committed only from a run that reached its last line, and a script cited in a
     message is re-run from a clean copy first; mathematics derived quickly in a
     well-worked field is sent as a *check*, and the word "new" waits for the prior-art
     search; when a theorem is applied on a sub-domain chosen by a heuristic, report the
     objective on the complement before calling anything certified; edit table rows by
     line, not by a search in the rest of the file.
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

## 5. Workstreams of the second to fifth wave: what each was for, and where it ended

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
| P6 | `workstreams/P6_brief.md` — pair penalties (workstream P4's banded pair form) in P3's certified sandwich: pair sums without enumerating subsets, both sides, validation by enumeration, twenty residues at orders 3–5, the reach at 30 and 50; item 7: the theory division's sandwich sampler (their Proposition 11.113) | **running** (launched after checkpoint 43) — on completion: read `P6_REPORT.md`, check one thing (e.g. the sandwich on one enumerated instance with own lines), publish to both divisions; it answers THY-RES-0010 §9.1 |
| R12 | `workstreams/R12_brief.md` — requested by the theory division (THY-RES-0010 §9.2): review of its corrected Theorem 11.110(e), Propositions 11.18e and 11.113, Corollary 11.114, Theorem 11.18d as written, `BarrierCertificate.lean` and Theorem 11.115 against our workstream K's formats | **running** (launched on reading THY-RES-0010) — on completion: read `R12_REPORT.md`, check one counter-example or one re-derivation, publish as `SCI-REV-0013` |

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

## 7. What to do next, ranked (revised after checkpoint 43; items 1–3 changed)

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
2. **Certify the compact case** (`OPEN_PROBLEMS.md` D6) — the problem the programme's most
   physical line now ends on.  Done at checkpoint 40: a certified `ln Z` at twenty
   residues on an extended backbone (P3; SCI-MSG-0020), replicated independently
   (addendum A17 (10)).  Not done: the helix, where a fitted chain model is measurably
   accurate (`0.002–0.004 k_BT`) and P3's bound cannot see the cancellation that makes it
   so.  Candidates: (a) ~~run P3's sandwich on the fitted chain models~~ — *would gain
   nothing* (the certificate sees any model only through the band `m₊ − m₋`; the
   midpoint model, which P3 ran, is optimal; addendum A17 (10), "Limits"); (b) the pair
   form of the penalties at order `m` (the theory division's Theorem 11.18a at `m = 3`;
   workstream P4 item 4) — **done on enumerated grids (P4, Proposition P4.6:
   pair and banded pair penalties; cost number 16.4 → 0.064 at `m = 3`), not yet applied to
   the twenty-residue instance: that needs the pair sums `Σ_{T⊇{i,j}} ĉ_T` from P3's
   generating functions with two sites excluded, `O(n²)` evaluations of code that has
   the one-site exclusion** — a bounded, well-defined next computation that would show
   whether order three suffices at twenty residues; (c) **group-wise signed tails** — **workstream P5, launched at
   checkpoint 43 and running when this was written** (`workstreams/P5_brief.md`; on
   completion: read `P5_REPORT.md`, check one thing, publish to theory and engineering);
   (d) a stand-alone checker of the certificate
   (request P3-E1); (e) a buried, non-homopeptide instance (request P2-E1).
3. **Benchmark B10: done in full on neutral side chains** (after checkpoint 43; finding
   9f; SCI-MSG-0022).  What is left of it: charged side chains, where the split should
   matter most (non-product domains: use the largest reset-closed domain at the true
   minimiser, finding 9e), and a buried environment (request P2-E1 to engineering).
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
