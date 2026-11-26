# Workstream R20 — NOTES (adversarial reading of the Complexity division's STRANDS_NN_HARDNESS.md, Theorems 1 and 3)

Internal review, not external peer review.  Kept from the first minute; every time below is read from the clock (`date -u`).

Object: `<CX>` = `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/cx_ro_fc4b238/` (read-only export of
`research/biological-complexity` at `fc4b238`).  Never written into.

Write area: `experiments/science/ws_R20/` and `docs/science/workstreams/R20_REPORT.md` only.

Four kinds of checking, kept apart everywhere: **review** (re-derived by me), **replication** (my own code), **re-run** (their code), **read only**.

## Log

* 2026-11-26T16:20Z — started.  Read `COMMON.md` and `R20_brief.md`.  Created `ws_R20/`.  Listed `<CX>` (docs/complexity: 8 files; strands: `ref_enum.py`,
  `test_partition_reduction.py`, `test_partition_reduction_big.py`, `big_run.log`; a `nanuq/` directory that is not the object of this workstream).
  Plan: (1) read MSG-0001 and the note in full; (2) re-derive Theorem 1 and 3 on paper BEFORE opening their code; (3) write my own enumerator
  (their `ref_enum.py` stays unopened until mine is final); (4) control that must fail; (5) re-run their two scripts from `rerun_copy/`;
  (6) literature (three papers) with generic queries; (7) report.

(The list "Tool actions declined" is kept at the very end of this file.)

* 2026-11-26T16:28Z — READ ONLY: `COMPLEXITY-MSG-0001.md`, `STRANDS_NN_HARDNESS.md` (all 263 lines), `THEOREMS.md`, `PRIOR_ART.md`, `OPEN_PROBLEMS.md`,
  `HANDOFF.md`, `README.md`, `RESEARCH_LOG.md`, `DEAD_ENDS.md`, `COMPLEXITY_TO_ALL.md`, `status/complexity.md`.  Their code (`ref_enum.py`, the two
  tests, `big_run.log`) NOT opened yet (brief: mine first).

### First-pass REVIEW (paper re-derivation, before any code) — to be confirmed by replication

Setting as in the note §1: bases on a circle per cyclic strand order π, chords = pairs, faces of the disc; face with exactly one nick = exterior
loop; nick-free face with k chords = hairpin (k=1) / stack, bulge, interior (k=2) / multiloop (k≥3).

1. Fact 1 (connected ⇔ no face with ≥2 nicks) — re-derived by planar duality: the polymer graph with all N links is a cycle with non-crossing
   chords; deleting the set F of nick edges leaves it connected iff F contains no bond (minimal cut), iff the dual edges F* contain no cycle;
   every nick is dual to an edge (outer face)–(inner face containing it), so F* has a cycle iff two nicks lie on one inner face.  HOLDS.
2. Uniqueness of π for connected S — re-derived: the face of the nick after the 3'-end of strand t has no other nick, so walking its boundary
   backwards from that 3'-end uses only chords and covalent bonds (data of S and the strands, not of π) and ends at the 5'-end of the successor
   strand.  So succ(t) is a function of S.  HOLDS.
3. (a) pairs: with letters {A,C,G} only and any rule in which the only complementary pair among these letters is {C,G} (Watson–Crick, or
   Watson–Crick + G·T/G·U wobble: there is no T/U in the instance), every pair joins a template G and an item C.  HOLDS; the note fixes
   Watson–Crick in §1, the theorem does not say what it needs — MINOR (state: "needs only: among A,C,G the only pair is C–G").
4. (b) R(S)=1: the template is the only strand of its sequence; a rotation mapping it to itself is the identity.  HOLDS.
5. (c) st(S) ≤ M: stack = nick-free, 2 chords, no unpaired base ⇒ boundary = chord, covalent bond, chord, covalent bond; chords join template
   and item, a bond stays in a strand ⇒ exactly one template bond and one item bond; a link is on exactly one face ⇒ st ≤ #item bonds = M.
   Antiparallel orientation is automatic from non-crossing.  HOLDS.  Lower bound (1) needs: every face of a connected S is exterior (H0: 0), a
   stack (=σ by H1, since every stack here is GG/CC), or bulge/interior/multi (H2: ≥0); no hairpin by (a).  HOLDS.
6. (d) equality: st=M ⇒ every item bond on a stack ⇒ partners of an item form a run of consecutive template positions joined by covalent bonds,
   all G ⇒ inside one block; single-base items paired by connectedness; mB item bases onto mB G's ⇒ runs partition the G's ⇒ each block exactly
   filled.  HOLDS.
7. (e) tiling structure: nested chords in the order "template, items in reverse run order"; faces: M stacks + (n−1) faces between consecutive
   items (each one nick) + innermost + outer face = mB+1 = |S|+1 faces, n+1 of them with exactly one nick.  HOLDS.
8. Theorem 3: tiling structures ↔ (solution β, order in each block): injective both ways; free action of Π Sym(μ_s).  HOLDS on paper.
9. Things to press (candidate findings, all to be checked against sources / by enumeration):
   F-a  (H2) "the sign pattern of every physical parameter set" (note l.14) — I recall (FROM MEMORY, to verify) that the 2004 RNA rules give
        single-nucleotide bulges an energy  initiation + stack of the flanking pairs (+ special-C bonus − RT ln(states)), which can be < 0;
        if so the sentence is false and §6.2 ("hypothetical parameter sets") too.  The theorem itself survives: see F-b.
   F-b  (H2) is stronger than needed.  With b(f) := number of item bonds on the boundary of a nick-free face f (b ≥ 1 always, because the
        boundary of a nick-free face alternates template segments and item segments): the proof only needs
        (H2*)  ∃δ>0: g(f) ≥ σ·b(f) + δ for every nick-free non-stack face f;   then MFE(no-instance) ≥ σM + nΔG_assoc + min(|σ|,δ).
        Proof: Σ_f g(f) ≥ σ·(M − e(S)) + δ·ns(S), e = #item bonds on exterior faces, ns = #non-stack nick-free faces; S not tiling ⇒ e≥1 or ns≥1.
        To test with my enumerator (negative bulge between σ and 0: must still pass; bulge ≤ σ·b: must fail).
   F-c  (H0): exact zero is used only on the four kinds of exterior loops of a tiling structure (flush nick over a template bond; nick + the
        unpaired A; the two blunt ends) and "≥ 0" on all others.  Dangles (negative) break "≥ 0"; coaxial stacking breaks the flush-nick zero.
   F-d  association term: constant (c−1)ΔG_assoc only because the problem is posed for ONE complex containing all strands; if sub-complexes
        may be left out, an item with (a_i−1)|σ| < ΔG_assoc prefers to leave ⇒ condition to add (scale a_i).
   F-e  Corollary 4(ii): "temperature as part of the input" — encoding of T and exactness of Z not stated (Z is irrational for rational T);
        one evaluation at x = e^{1/kT} > #structures would do instead of M+1 (digits in base x).  Check against DSW Thm 22.
   F-f  NP membership (Cor. 2): k_BT ln R(S) is irrational for R ≥ 2; "the energy is computable in polynomial time" is not literally true.
   F-g  attribution: the construction (G^B blocks separated by A, items C^{a_i}, bin packing) is, as far as I remember, Lyngsø's 2004
        reduction for single-strand pseudoknotted BPS; `PRIOR_ART.md` says so, the note itself does not cite it.  Verify by opening.

* 2026-11-26T16:34Z–16:36Z — REPLICATION, step 1: wrote `r20_enum.py` (own enumerator from the note's §1: circle per cyclic order, open/close
  word enumeration of non-crossing matchings, face tracing as cycles of the link permutation, union-find, successor walk, R(S)) and
  `r20_validate.py` (brute force over ALL matchings, direct pairwise crossing test).
  - First run FAILED check V5 (135 violations): **my bug** — the pruned enumeration counted the wrap-around nick twice (at p = N), so it
    produced nothing.  Log kept in `not_cited/validate_seed20261126_run1_FAIL_bug_in_pruning.log`.  Fixed (`0 < p < N`).
  - After the fix, with controls C1–C5 added: `logs/validate_with_controls_seed20261126.log`, `logs/validate_with_controls_seed7.log`
    (each reached its last line): 189 systems, 48 034 / 47 546 matchings, checks V1–V5: 0 violations; controls C1–C5: 108 / 466 114 /
    29 845 / 9 406 / 157 violations (seed 20261126) — every control fails as it must.
    V1 enumeration = brute force; V2 Euler; V3 Fact 1 (union-find = DFS = "no face with two nicks", c exterior faces); V4 unique cyclic order
    and it equals the order computed from S alone; V5 pruned enumeration = connected structures.
* 2026-11-26T16:39Z — step 2: `r20_theorem.py` (Theorem 1 and 3 on packing instances; Til, solvability, L by independent brute force; 5 loop
  functions inside (H0)–(H2), 6 "GEN" functions outside (H0)–(H2) testing MY weaker hypotheses, 5 controls that must fail).
  - `logs/theorem_tiny_run1.log` (7 instances, 5 564 structures, complete): H and GEN 0 violations; all 5 controls violated.
  - `logs/theorem_small_run1.log` (43 instances: 24 solvable, 19 not; N ≤ 20; 2 526 779 connected labelled structures; with `--crosscheck`
    (unpruned enumeration + union-find gives the same number of connected structures in all 43) and `--orbits`; complete, 391.9 s):
    U1–U5 0 violations; H1–H5: S1–S5 0 violations, 0 wrong decisions; GEN1–GEN6: 0 violations;
    CTRL1 (flush nick rewarded like a stack, bulges 0): S1=18 S2=16 S3=34 S4=34 S5=18, wrong decisions 16 of 19 no-instances;
    CTRL2 (bulge = σ): S2=19, S3=31; CTRL3 (σ=0): S3=41; CTRL4 (H2* at δ=0): S2=19; CTRL5 (large dangles): S1=22, S2=17.
  - **My procedural error:** this run took 6.5 min and I had not written its cost into NOTES before starting (I expected < 5 min).
* Cost note BEFORE the next run (16:46Z): counting-only pass over the candidate "medium" instances, capped at 60 s each (≤ 21 min in
  total if all hit the cap; run as ONE process, single thread, memory negligible) — to decide which of them fit the 20-minute limit.

* 2026-11-26T16:47Z–16:54Z — LITERATURE (opened = downloaded the PDF with `curl` through the session proxy into a scratch directory outside the
  repository, converted with `pdftotext -layout`, read the passages named; queries were titles/authors/standard terms only; nothing uploaded).
  1. **Ducloz, Shalaby, Woods**, "Algorithmic hardness of the partition function for nucleic acid strands", arXiv:2506.19756v1 (24 Jun 2025),
     29 pp. — FULL TEXT READ (all 1706 lines of the text conversion, incl. Appendix A).  Proceedings version (DNA 31, LIPIcs 347, Article 1,
     pp. 1:1–1:23, https://drops.dagstuhl.de/...LIPIcs.DNA.31.1.pdf) opened for numbering only: Lemma 31, Thm 22, 32, 33, 38, Def. 11, 25 have
     the SAME numbers in both; in the proceedings the proofs of Lemma 31/Thm 32 are in App. B.3.
     - "1.3 Future work 1. MFE hardness in two settings is still an open question: Is MFE NP-hard for NN single-strand pseudoknotted, or NN
       O(n)-strands unpseudoknotted? If so, can the reduction map be leveraged to show hardness results for PF and #SSEL in the NN model?"
       — the note's quotation is VERBATIM.  ✔
     - Table 1 caption: "Negative, or hardness, results are proven in the simple BPM or BPS models and are conjectured [5] to hold in the more
       complex NN model."  ✔ (coordinator's statement 2).  Unbounded strands: MFE "NP-hard [5]; BPM model", PF "#P-hard [Theorem 38]; BPM model".
     - Def. 11 = NN model: connected unpseudoknotted S, ΔG = Σ_loops ΔG(l) + (c−1)ΔG_assoc + k_BT log R, R "the maximum degree of rotational
       symmetry"; footnote 4: "In the NN model, unlike the BPM and BPS models, multi-stranded secondary structures must be connected [8]".  ✔
     - **Appendix A.2 (arXiv version only): "Exterior loops: An exterior loop contains a nick (see Figure 1) between strands and any number of
       closing base pairs. Exterior loops do not contribute to the free energy because by definition [8], ∆G^exterior = 0."**  → (H0) IS the
       convention of the paper that poses the question.  The Complexity division had not read this appendix (their PRIOR_ART A-I) and attributes
       ΔG_ext = 0 only to the 2026 preprint.
     - Defs 14–18: problems take "a temperature T ≥ 0, and an energy model M" as input; k ∈ ℝ.  Thm 22 (#SSEL ≤_T PF): N oracle calls
       b_j = PF(s,T,M_j), ΔG^{M_j} = j·ΔG^M, Vandermonde system in the real numbers e^{−βg_i}; §3.5.2: for a temperature-independent model the
       magnification α is obtained by calling the oracle at T' = T/α.  No encoding of real numbers is specified there either.
     - Def. 29 (#4-PARTITION): weights strictly between B/5 and B/3; output "the number of partitions of A into 4-tuples such that the sum of the
       weights of the elements in each tuple is equal to B".  Lemma 31: "#4-PARTITION is #P-complete" (weakly parsimonious from #3DM through
       Garey–Johnson's reduction, factor Π_a (N(a)−1)!).  Not stated: that the weights are polynomially bounded (needed for a unary encoding;
       true for the Garey–Johnson reduction — FROM MEMORY).
     - **Thm 32 (#BPS is #P-complete): "In 2004, Lyngsø [20] proved that the decision problem BPS is NP-complete, with a reduction from
       BIN-PACKING. We adapt his reduction from 4-PARTITION to BPS. […] We proceed exactly as Lyngsø, constructing the following DNA strand s:
       s = C^{w(a1)} A C^{w(a2)} A ··· A C^{w(ak)} AAA G^B A G^B A ··· A G^B (k/4 substrings of G's) and setting the target K = Σ w(a_i) − k."
       and "(k/4)! (4!)^{k/4} secondary structures of s having K BPS map to the same 4-PARTITION solution".**  → the note's template
       G^B(AG^B)^{m−1}, items C^{a_i}, target M = Σa_i − n and factor m!·24^m are EXACTLY this construction with the single strand cut at the
       A's between the C-runs.  The note itself does not cite Lyngsø or DSW Thm 32 for the construction (only `PRIOR_ART.md` does).  FINDING.
     - footnote 2: "The BPS model is a special case of the NN model, so any algorithm in the NN model can be modified for the BPS model by easily
       ignoring all loops except stacks and setting ∆Gstack = −1."  Def. 9: BPS(S) = |{(i,j) ∈ S | (i+1,j−1) ∈ S}| (single strand; for several
       strands the indices are those of the concatenation, Def. 5 — a "stack" across a nick would then count, unlike in Def. 11).
     - intro §1.2 says "(a) … pseudoknots under the BPM model, and (b) in the multi-stranded case … under the BPS model", which contradicts
       Table 1 and §§4–5 (BPS for one strand with pseudoknots, BPM for many strands): a slip in the paper, not in the note.
  2. **Condon, Hajiaghayi, Thachuk**, DNA 27 (2021), LIPIcs 205, 9:1–9:21, doi 10.4230/LIPIcs.DNA.27.9 — §§1, 2.1, 2.2, end of §5, §§6–7 READ.
     - abstract: "we prove that for a simple energy model, the problem of predicting the MFE pseudoknot-free secondary structure formed from
       multiple interacting nucleic acid strands is NP-hard and also APX-hard."  ✔ (coordinator's statement 1)
     - model (§2.1): E(S) = p(−1) + (m − l)K_assoc for m strands in l complexes with p base pairs: **several complexes are allowed**; "it would
       seem unlikely that the prediction problem becomes easier if the energy model is more sophisticated" (§1) — the "conjecture" DSW cite.
     - K_assoc > 0 is handled by scaling domain lengths "to ensure that a single domain binding is always favourable".  (My F-d is the analogue.)
  3. **Shalaby, Woods**, ICALP 2025, LIPIcs 334, 130:1–130:20, doi 10.4230/LIPIcs.ICALP.2025.130 — abstract, Table 1, §1 footnotes, §1.4,
     §2.1–2.2 READ.  Table 1 caption: "Results are proven in the nearest neighbour energy model studied here, except the APX-hardness result
     which is proven in the maximum matching model [9], and still open for nearest neighbour model."  ✔ (coordinator's statement 3; this sentence
     is NOT in arXiv:2407.09676v1, which I also opened: there Table 1 lists only "Partition function: Open problem" for unbounded strands).
     §1.4: "We know “not by much”, since the problem is NP-complete when c = O(N) in a simpler energy model that merely maximises the count of
     base pairs [9]."  Model: Eq. (2) as above; Remark 5 "only interested in connected unpseudoknotted secondary structures"; MFE = min over Ω.
     arXiv v1 Remark 6 cites the representation theorem as Dirks et al. Theorem 2.1.  Exterior loop term in the recursions: no energy.
  4. **Shalaby, Woods**, arXiv:2611.27945v2 (23 Nov 2026; v1 20 Nov 2026) — Table 1 + caption, §1.5, Def. 7, Def. 11, Remark 12, footnote 19
     READ.  All quotations of it in the Complexity division's files that I checked are accurate: Table 1 caption ("…negative/hardness results in
     the simpler base pair matching (BPM) model [5, 16]…"), Future work 3 and 4, Def. 7 (NN model, connected, indistinguishable strands,
     R_max), Def. 11, footnote 19 in §6.2 ("∆G^ext = 0 for the energy contribution of an exterior loop or equivalently in the case of having
     empty substructure").  Footnote 9: "hardness results in such simple settings intuitively suggest hardness should carry over to the more
     realistic nearest neighbour model".
  5. **Dirks, Bois, Schaeffer, Winfree, Pierce**, SIAM Review 49 (2007) 65–88 (Caltech repository copy) — §2.1, §2.2 (start), Fig. A.1
     caption, Appendix B notes 3, 5, 13 READ.  "all loops containing one nick are exterior loops.  A secondary structure is connected if no loop
     contains more than one nick" (= the note's Fact 1); Theorem 2.1 (Representation) = the note's uniqueness of π; ΔG(s) = (L−1)ΔG^assoc +
     Σ ΔG(loop), symmetry correction kT log R (2.1); Note 3: "Exterior loops do not contribute to the free energy because by definition
     ∆G^empty = 0.  We omit details of dangle free energies [34] (corresponding to the energetic contributions of any unpaired bases adjacent to
     a base pair) and penalties for helices not ending in G-C pairs."; Fig. A.1: "the implementation details for incorporating dangle free
     energies [34] and penalties for helices not ending in C-G pairs are omitted".  → (H0) = the model as WRITTEN in Dirks et al.; the model as
     IMPLEMENTED adds dangles and terminal penalties.  Indistinguishable structures: "a permutation of the strand identifiers that maps
     indistinguishable strands onto each other while preserving all base pairs" (= the note's physical ensemble).
  6. **Lyngsø**, ICALP 2004 (LNCS 3142, 919–931) — NOT OPENED: the publisher's PDF link answered with a JavaScript "client challenge" page
     (not worked around); known only through DSW Thm 32 (above) and a search summary of its abstract.
  7. Garey–Johnson 1979 (Theorems 4.3/4.4) — NOT OPENED (book); from memory: Thm 4.3 = 4-PARTITION, Thm 4.4 = 3-PARTITION, both strongly
     NP-complete.
* Counting pass `logs/count_medium_cap45.log` (still running at 16:54Z): m=2,B=5 instances have 0.73–4.36 million connected structures
  (feasible); m=3,B=4 and m=2,B=6 instances 3·10^7–3·10^8 (not feasible in pure Python with face decomposition inside 20 min — not run).

* 2026-11-26T16:58Z — counting pass complete (`logs/count_medium_cap45.log`, reached "END").  Added `--reduce-orders` to `r20_theorem.py`
  (one cyclic order per class under permutations of equal items; counts × Π μ_s!); on the tiny set it reproduces the full enumeration exactly
  (`logs/theorem_tiny_reduced_run1.log`: same 5 564 labelled structures, same violation table).
* MY ENUMERATOR IS FINAL at this point (before I open the reviewed division's code).  sha256:
    a1d3a90120cffb277b1f3f352633903cb33d87d8f1f23365e8f1d4e8183e286c  r20_enum.py
    452247c5721c49c456a24e3585e97069038d79acd72a13126010cae464f6c389  r20_validate.py
    00cf8cd95a29e4c2c108b46be8c950ca7f037da0f02d5040f73f1c8921258fdf  r20_theorem.py
    f02c64fa30dcff9c9019863516006ed5488202d6f99ba09b5360dec493d8f5d8  r20_count.py
* Cost note BEFORE the next runs: `medium_a` (5 instances, 5.1 M structures) and `medium_b` (4 instances, 4.4 M structures), full enumeration
  over all orders, two processes in parallel, single thread each, expected ≈ 8–11 min each (≈110 µs per structure), memory < 200 MB each.
  Then `medium_c` (4.36 M, ≈ 8 min) and `medium_d` (3.32 M, ≈ 6 min).

* 2026-11-26T17:02Z — the machine is loaded (load average ≈ 6 on 4 cores; my two processes got ≈ 36 % CPU each, as if this session shares one
  core).  At that rate `medium_a` would need ≈ 26 min wall-clock (> the 20-minute limit).  STOPPED `medium_b` (pid 1055, `kill`) after 3.5 min
  with no output; its empty log moved to `not_cited/theorem_medium_b_run1_STOPPED_by_me_cpu_share.log`.  `medium_a` continues alone.  From now
  on ONE compute process at a time, and batches sized for ≤ ~8 CPU-minutes.
* 2026-11-26T16:59Z — READ their code (`ref_enum.py`, `test_partition_reduction.py`, `test_partition_reduction_big.py`, `big_run.log`) for the
  first time, AFTER fixing my enumerator (hashes above).  First observations (READ ONLY, before re-running):
  - their counts of connected structures in `big_run.log` agree with mine wherever both exist: (3,2,2,1|2,4) 66 552; (3,3,2|2,4) 46 002;
    (3,3,1,1|2,4) 50 568; (2,2,2,2|2,4) 87 576; (3,2,2,2|3,3) 409 488; (2,2,2,2,1|3,3) 676 920; (4,4,2|2,5) 762 294; (4,3,3|2,5) 836 544;
    and their "#MFE-structures" of no-instances in the stack model equal my "#min" of H1 (70; 300; 2400).
  - `big_run.log` is TRUNCATED: `test_partition_reduction_big.py` lists 12 cases, the log holds 10 (20 lines), the last two cases
    ([3,2,3,2],2,5) and ([4,3,3],2,5) and the final line "ALL OK" are missing.  The note (§4) cites this log.  ([3,3,4] and [4,3,3] are the
    same multiset.)  The note's "up to 513 120 structures per instance" is not the maximum in its own log (836 544).
  - the note says Fact 1 is "re-checked exhaustively by the enumerator's `check=True` mode against a union–find computation"; neither test
    script passes `check=True` (default False), so the shipped re-run instructions do not exercise that check.
  - their test checks: min = σM iff tilings exist; min ≥ σ(M−1) otherwise; #min = #labelled tilings (count only, not the set); each labelled
    structure under one order.  NOT checked by their scripts: that the minimisers ARE the tiling structures (only their number), R(S) = 1
    (no symmetry code is called), Theorem 3.2 (`symmetry_orbits` exists but is never called), Corollary 4, any ΔG_assoc.  Two loop functions
    only (stack-only; one random table with values 0..3 keyed by loop type and segment lengths).
  - their `seen` set stores every labelled structure as a frozenset of tuples: memory will be large for the 1.9 M-structure case (probable
    cause of the truncated log).  Re-run must be done under a 2 GB cap.

* 2026-11-26T17:07Z — `logs/theorem_medium_a_run1.log` COMPLETE (5 instances m=2,B=5: 3 solvable, 2 not; 5 125 260 structures; 519 s):
  U1–U4 0; H1–H5 and GEN1–GEN6 0 violations; controls violated (CTRL1 S1=3 S2=2 S3=5; CTRL2 S2=2; CTRL3 S3=5; CTRL4 S2=2; CTRL5 S1=3 S2=2).
* RE-RUN of their small test, unmodified, from `rerun_copy/` (sha256 identical to `<CX>`), via `r20_rerun_driver.py` (python3 -I -B, runpy,
  2 GB address-space cap): `logs/rerun_their_small_test_run1.log` — 12 lines "OK", final "ALL OK", 1.4 s, max RSS 16 MB.  Counts agree with
  my enumeration: (2,2,1,1|2,3) 2040 structures/16 tilings; (2,2,2|2,3) 2262, 102 minimisers; (3,1,1,1|2,3) 1536/12; (3,3|2,3) 1514/2.
* Cost note BEFORE the next run: their `test_partition_reduction_big.py` (12 cases × 2 models).  Their own log shows ≈ 310 s for the first 10
  cases; the two missing cases add an estimated 120–200 s; here ≈ 8–14 min wall-clock on one shared core.  Memory unknown (their `seen` set
  keeps every structure): run under the 2 GB cap and under `timeout 1140` (19 min).  One process.

* 2026-11-26T17:09Z — LITERATURE for hypothesis (H2) and for Remark 3 (definitions of a published parameter set; pages of the Nearest
  Neighbor Database, RNA "Turner 2004" rules):
  8. https://rna.urmc.rochester.edu/NNDB/rna_2004/rna_2004_bulge_loops.html — PAGE TEXT READ (downloaded, tags stripped):
     "ΔG°37 bulge (n=1) = ΔG°37 bulge initiation(n) + ΔG°37 (special C bulge) + ΔG°37 (base pair stack) – RT ln(number of states)";
     "a special C bulge is a bulged C adjacent to at least one paired C, the base pair stack is the stack of the closing pairs as though there
     is no bulge"; worked example "Single C bulge with multiple states": "ΔG°37 = –3.42 kcal/mol – 3.26 kcal/mol + 4.09 kcal/mol + 3.81 kcal/mol
     – 0.9 kcal/mol – 2.36 kcal/mol – 0.616×1.099 kcal/mol", where the last four terms are the bulge loop: 3.81 − 0.9 − 2.36 − 0.677 =
     **−0.13 kcal/mol < 0**.  ("CG followed by CG" = −3.26 is the GG/CC stack.)  ⇒ the note's "(H2) … the sign pattern of every physical
     parameter set" (l.14) is FALSE for this published rule set, and §6.2 ("hypothetical parameter sets with favourable bulges") with it.
     In the instance the analogous loop is a bulged C of an item between two G–C pairs: 3.81 − 0.9 − 3.26 = −0.35 kcal/mol before the
     degeneracy term.
  9. https://rna.urmc.rochester.edu/NNDB/rna_2004/rna_2004_coaxial_stacking.html — read THROUGH THE FETCH TOOL'S SUMMARY ONLY (short quotes):
     flush coaxial stack approximated by the helical nearest-neighbour parameters "as though there was no break in the backbone";
     mismatch-mediated coaxial stacking when exactly one unpaired nucleotide separates the helices; "In unimolecular secondary structures,
     coaxial stacking occurs in multibranch and exterior loops."  ⇒ in rule sets with coaxial stacking a flush nick is rewarded EXACTLY like
     the stack (κ = σ), the case of the note's Remark 3.
  10. Two generic web searches for a published NP-hardness proof of multi-strand folding in a stacking / nearest-neighbour model (queries in
      the report §5): nothing beyond the papers above [search summaries only].
* Read-only git: commit `fc4b238` has committer date 2026-11-26T16:17:10+00:00, while `COMPLEXITY-MSG-0001.md` and `status/complexity.md`
  inside it are dated "2026-11-26 17:00 UTC" (43 minutes after the commit that contains them).

* 2026-11-26T17:12Z — `r20_packing_identities.py` (packing side only, brute force): Til = L·m!·6^m on 14 3-PARTITION-shaped instances (m = 2, 3)
  and Til = L·m!·24^m on 6 4-PARTITION-shaped instances (m = 2); Π μ_s! divides Til; 0 violations; control (the other factor) fails on 17 of 20
  (it cannot fail where L = 0).  `logs/packing_identities_run2.log` (complete).
  **My error:** the first run aborted on my own assertion — I had put (6,5,4,4,4,3 | 2,13) in the list, which is not 3-PARTITION-shaped
  (3 < 13/4).  Log in `not_cited/packing_identities_run1_FAILED_my_bad_instance.log`.
* 2026-11-26T17:13Z — changes to `r20_theorem.py` AFTER I had read their code (none of them taken from their code; `r20_enum.py` unchanged,
  sha256 a1d3a901…): (i) instance sets `edge` (B = 1, a single item, all items of length 1, an item longer than a block) and `their_extra`;
  (ii) model GEN7 (flush nick = σ, ONLY the bulge "G A G over C C" costs +1); (iii) GEN4/GEN7 are not evaluated for B = 1 (my statement is for
  B ≥ 2).  New sha256 1c232e6e….
  - `logs/theorem_edge_run2.log` (complete; 14 instances: 8 solvable, 6 not; 15 013 structures; crosscheck + orbits): U1–U5 0; H1–H5 and
    GEN1–GEN7 0 violations; all controls violated.
    **My error:** the first run aborted on my assertion (I had listed (7 | 2,3), sum ≠ mB); `not_cited/theorem_edge_run1_FAILED_my_bad_instance.log`.
* Reviewer's observation (to check and put in the report, §5): on the connected ensemble the base-pair model is a loop model:
  |S| = #(nick-free faces) + c − 1 (Euler + Fact 1), so "−|S|" = Σ_loops g with g ≡ −1 on every non-exterior loop, exterior loops 0, and a
  constant.  Hence, with the loop function as part of the input and NO sign condition, hardness of the "NN framework" for unboundedly many
  strands already follows from Condon–Hajiaghayi–Thachuk (their yes-instances have a single-complex optimum: "Our construction has the property
  that structure Opt(I′) is a single complex when I has a perfect matching" — read; the reduction itself not read).  What the note adds is
  hardness under the PHYSICAL sign pattern (stacks favourable, loops with unpaired bases not as favourable), for every FIXED such function.

* 2026-11-26T17:17Z — RE-RUN of their big test as a whole (`r20_rerun_driver.py test_partition_reduction_big.py 2`): the first 10 cases × 2
  models printed "OK" with exactly the numbers of their `big_run.log`; at the 11th case ([3,2,3,2],2,5; 1 887 888 structures) the process
  hit **MemoryError under my 2 GB cap** (max RSS 1997 MB, 501.9 s) — exactly where their own `big_run.log` ends.  The run did not complete,
  so its log is in `not_cited/rerun_their_big_test_run1_STOPPED_MemoryError_at_case11_under_2GB_cap.log` and is not cited as evidence.
  (Not worked around inside that process.  A per-case re-run in separate processes follows; the 11th case needs > 2 GB with their `seen`
  set and is NOT re-run; my own enumeration covers that instance: (3,3,2,2|2,5), 1 887 888 structures, Til = 16, 0 violations.)
* RE-RUN of their enumerator with `check=True` (which their scripts never pass): `logs/rerun_their_enum_check_true_run1.log` (complete):
  10 cases, 1 099 956 non-crossing (order, structure) pairs, no assertion failed; their counts of all / connected structures equal mine
  (e.g. (2,2,2|2,3): 5544 / 2262; (2,2,2,2|2,4): 308 880 / 87 576).
* Cost note BEFORE the next runs (sequential, ONE process): `their_extra` (513 120 structures, ≈ 1 min), then `r20_assoc.py` (22 instances, all
  sub-multisets, canonical orders; ≈ 1.5 M structures, ≈ 3–5 min), then `large_reduced_a` with `--reduce-orders` (≈ 2.5 M visited, ≈ 4–5 min).

* 2026-11-26T17:22Z — results of the chain so far:
  - `logs/theorem_their_extra_run1.log` (complete): (3,2,2,1,1|3,3) = their case [2,1,2,1,3]: 513 120 structures, Til = 48, #min = 48 —
    equal to their log; 0 violations (17 loop functions incl. GEN7).
  - `logs/assoc_run1.log` (complete; 22 instances; 2 036 774 structures over all sub-multisets; 94 s): claim (P4) with Δ > 0: 245
    (instance, model, A) cases, 0 violations; control Δ ≤ 0: 217 cases, 68 wrong decisions (must be > 0).
  - `large_reduced_a` running: (2,2,2,2,2,2|2,6) [3-PARTITION-shaped] and (2,2,2,2,2,2|3,4): 369 305 structures visited in 1 of 720 orders
    each = 265 899 600 labelled; Til = 720; U1–U4 0.  (Same count for both templates, as it must be: the A's never pair, so the set of
    structures does not depend on where they sit.)
* Cost note BEFORE the next chain (sequential, ONE process at a time, started when the current chain ends): (1) `small` again with the final
  list of 17 loop functions, no crosscheck/orbits (2.5 M structures, ≈ 4–6 min); (2) `r20_rerun_cases.py` — their `run()` on the 12 cases of
  their big test, one process per case under the 2 GB cap (≈ 8–10 min; the 11th case is expected to stop with MemoryError);
  (3) `medium_b` (4.4 M structures, ≈ 8–10 min).

* 2026-11-26T17:26Z — `logs/theorem_large_reduced_a_run1.log` COMPLETE (3 instances with one order per class: (2,2,2,2,2,2|2,6),
  (2,2,2,2,2,2|3,4), (3,3,3,3|3,4) [not solvable; 1 638 001 visited × 24]; 2 376 611 structures visited = 571 111 224 labelled; 245 s):
  U1–U4 0; H and GEN (incl. GEN7) 0 violations; all controls violated.
* `r20_aggregate.py` over the complete logs so far (small run1, edge, medium_a, their_extra, large_reduced_a): 66 instances (38 solvable, 28
  not); H1–H5, GEN1–GEN6: 0 violations on 66; GEN7: 0 on 18; CTRL1: S1=26 S2=19 S3=45, wrong decisions 19 of 28 not-solvable instances;
  CTRL2: S2=28, 28/28 wrong; CTRL3: S3=58, 28/28; CTRL4: S2=28, 28/28; CTRL5: S1=30 S2=20, 20/28.
* REPORT: body written into `docs/science/workstreams/R20_REPORT.md` (sections 1, 2, 5, 6, 7); sections 0, 3, 4 wait for the last runs.

### (interim copy of the list "Tool actions declined", 17:26Z — the current list is at the very end of this file)

* By the permission system: none.
* The page-fetch tool (its summariser) declined twice to reproduce an abstract verbatim ("exceeds the 125-character limit on quotations",
  arXiv abstract pages of 2506.19756 and 2407.09676).  Not asked again.  To read the papers I downloaded the open-access PDFs with `curl`
  through the session proxy into the scratchpad (outside the repository) and converted them with `pdftotext`.  Recorded in the report (§7.3)
  for the coordinator to judge.
* The publisher's PDF link for Lyngsø (ICALP 2004) returned a script "client challenge" page; not pursued; the paper is unopened.

* 2026-11-26T17:36Z — second chain:
  - `logs/theorem_small_run2_17models.log` COMPLETE (204 s): same 43 instances and 2 526 779 structures as run 1, now with 17 loop functions
    (GEN7 included): H and GEN 0 violations; controls as in run 1 (CTRL1 S1=18 S2=16 S3=34; CTRL2 S2=19; CTRL3 S3=41; CTRL4 S2=19; CTRL5 S1=22 S2=17).
  - `logs/rerun_their_big_cases_one_process_each_run1.log` COMPLETE (462 s): their `run()` on the 12 cases of their big test, one process
    per case under the 2 GB cap: 11 cases OK in both models (22 "OK" lines; max RSS up to 1399 MB for 836 544 structures), **case 11
    ([3,2,3,2],2,5) MemoryError under 2 GB**.  All their numbers equal mine (table in the report §4).
  - `medium_b` running.
* Cost note BEFORE the last chain (sequential, ONE process, starts when `medium_b` ends): `medium_c` and `medium_d` with `--reduce-orders`
  (≈ 36 000 and ≈ 553 000 structures visited; ≈ 1–2 min together) and `large_reduced_b` with `--reduce-orders` ((3,3,3,3|2,6) ≈ 1.9 M and
  (4,4,4|2,6) ≈ 2.6 M visited; ≈ 6–8 min).

* 2026-11-26T17:42Z — `logs/theorem_medium_b_run2.log` COMPLETE (4 instances: (3,3,3,1|2,5) no, (4,2,2,2|2,5) no, (2,2,2,1,1,1|3,3) yes
  [720 orders, Til = 288, 8 orbits], (3,3,1,1,1|3,3) yes; 4 379 304 structures): U1–U4 0; H and GEN (17 functions) 0 violations; all controls
  violated.  Last chain (reduced orders) running.

* 2026-11-26T17:47Z — COORDINATOR'S NOTE received (their branch moved to 22cf1a6, 17:33 UTC; my object stays fc4b238; a new
  "Corollary 5" (ETH) outside the review; the pairing rule and "one complex" already promised in their COMPLEXITY-RES-0001).  Done:
  read the new hunk with read-only `git diff fc4b238 22cf1a6 -- docs/complexity/STRANDS_NN_HARDNESS.md` (only l.243–247 replaced) and
  `git show 22cf1a6:docs/collaboration/responses/complexity/COMPLEXITY-RES-0001.md`; added to the report: "already promised" under F8 and
  F9, and §2.5 (one paragraph, marked outside the review): the Garey–Johnson transformation as summarised in [DSW] gives 3|T| + |T| = 4|T|
  items, so c = 4|T| + 1 strands — linear in the number of triples, linear in q only with |T| = O(q); sizes and step (i) not checked.
  (Their RES-0001 is again dated ahead of its commit: "18:05 UTC" in a commit of 17:33:36 UTC.)

* 2026-11-26T17:49Z — ALL RUNS COMPLETE.
  - `logs/theorem_medium_c_reduced_run1.log`, `theorem_medium_d_reduced_run1.log`, `theorem_large_reduced_b_run1.log` complete (one order per
    class): (2,2,2,2,2|2,5) no — 36 365 visited = 4 363 800 labelled; (3,2,2,2,1|2,5) yes — 553 280 visited = 3 319 680 labelled (both totals
    equal the counting pass over all orders); (3,3,3,3|2,6) yes — 1 638 001 × 24; (4,4,4|2,6) no — 2 331 705 × 6.  0 violations for H and GEN;
    controls violated.
  - Final totals (`logs/aggregate_full_enumeration.txt`, `aggregate_reduced_orders.txt`, `aggregate_all.txt`): all orders 67 instances
    (38 solvable, 29 not), 12 559 476 structures; one order per class 7 instances (4/3), 6 935 962 visited = 632 096 958 labelled; together
    74 instances (42/32).  U1–U4 0 on all; U5 0 on small+edge (57).  H1–H5, GEN1–GEN6 0 violations on 74 (GEN4 evaluated on the 67 with
    B ≥ 2); GEN7 0 on 62.  Controls over the 74: CTRL1 S1=30 S2=23 S3=53 wrong 23/32; CTRL2 S2=32 S3=51 wrong 32/32; CTRL3 S3=66 wrong 32/32;
    CTRL4 S2=32 S3=57 wrong 32/32; CTRL5 S1=34 S2=24 S3=52 wrong 24/32.
  - REPORT complete: `docs/science/workstreams/R20_REPORT.md` (sections 0–7; §2.5 = the paragraph asked by the coordinator's note, outside
    the review).
  - No compute process of mine is left running.  Nothing was written outside `experiments/science/ws_R20/` and the report file, except
    downloaded papers in the session scratchpad (`…/scratchpad/r20_lit/`, outside the repository) and one debug script there.
* 2026-11-26T17:50Z — report finalised (two last wording edits); hand-back sent next.

## If this agent is gone — where things stand

Everything is finished: the report is complete, every cited log reached its last line, stopped/failed runs are in `not_cited/`.  To
re-run: the commands at the end of §7.3 of the report.  Open ends are listed in §6.2 and §7.1 of the report.

## Tool actions declined (current list; this section is kept at the very end of the file)

* By the permission system: none.
* The page-fetch tool (its summariser) declined twice to reproduce an abstract verbatim ("exceeds the 125-character limit on quotations";
  arXiv abstract pages of 2506.19756 and 2407.09676).  Not asked again.  To READ the papers I downloaded the open-access PDFs with `curl`
  through the session proxy into the scratchpad (outside the repository) and converted them with `pdftotext`; the quotations in the report
  are short passages.  Reported in §7.3 of the report and in the hand-back for the coordinator to judge.
* The publisher's PDF link for Lyngsø (ICALP 2004) returned a script "client challenge" page; not pursued; the paper is unopened.
