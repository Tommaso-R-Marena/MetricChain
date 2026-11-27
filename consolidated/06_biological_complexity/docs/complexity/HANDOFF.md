# Handoff (complexity division)

*Updated 2026-11-27 01:20 UTC, end of session 1.  **The division is halted** under the research owner's directive
"Controlled Consolidation and Temporary Research Halt" (directive 5 below).  Nothing is running.  Do not resume
research, answer other divisions, start sub-agents or schedule sessions without the research owner's explicit
authorisation.*

## State in a few lines

* Branch `research/biological-complexity`, based on theory checkpoint `a844b5a`.  Only files under
  `docs/complexity/`, `docs/collaboration/**/complexity*`, `docs/collaboration/README.md` (our copy of the
  protocol), `experiments/complexity/` are ours.
* **Start with** `docs/collaboration/consolidation/complexity.md` (critical assessment: four contributions
  ranked, what is known or failed, three recommended actions), then `THEOREMS.md` (every statement with label,
  evidence and review state), `OPEN_PROBLEMS.md`, and "Resume here" in `RESEARCH_LOG.md`.
* **Six internal reviews** (COMPLEXITY-REV-0001 to -0006, verbatim with dispositions in
  `docs/collaboration/messages/complexity/`), plus the science division's SCI-REV-0019.  Internal AI reviews
  are not peer review; no human expert has seen anything.  **No theorem with a written proof was found false.
  The reviews corrected: attributions and novelty statements (five times something called ours was known),
  summary sentences and corollaries that dropped a qualifier (one corollary was false as written), a citation
  from memory credited with more than it says, and descriptions of numerical evidence** (`ASSUMPTION_AUDIT.md`
  §6, last paragraph).
* **Strands, hardness** (`STRANDS_NN_HARDNESS.md`; CX-T1–T4, T14, T15, T20, T24): multi-strand MFE is strongly
  NP-hard, #SSEL #P-hard, in the nearest-neighbour model with exterior loops 0, for every fixed energy function
  with (H1), (H2′); flush coaxial stacking, dangles, several complexes; ETH bound.  Reviewed three times: correct.
  **The strongest result of the division.**
* **Strands, algorithm** (`STRANDS_ALGORITHM.md`; CX-T10–T12, T30): magnified partition function, MFE and level
  counts over all orderings with symmetry, `O(N⁴3^c)`, polynomial for bounded species.  Reviewed (REV-0003,
  REV-0005): correct.  **Novelty is modest:** for the base-pair model this is Boehmer et al. (journal version
  2025), who also write that the extension to the Turner model "does not pose any algorithmic challenges"; ours
  is that extension written out and tested, and it answers a question Shalaby and Woods list as open.
* **Phylogenetic networks, level ≤ 2** (`NANUQ_LOCAL_CRITERION.md`; CX-T5–T9, T13, T26, T27, T34; Lean CX-V3, V5):
  local criterion; all galled outer-labeled planar networks (probable rediscovery of an unreviewed third-party
  claim); "galled" is necessary; the sharp classes for exact support (`𝒦`, 127 six-point systems) and for
  "Kalmanson" alone (`𝒦′`, 133; a forbidden six-leaf pattern); **level 2 completely** — one critical split per
  nested blob, weight `β_1G + ξ_1R − Σβ_jβ_l` (REV-0005: 1.4 million explicit networks); **Theorem 12′
  (CX-T34): a negative critical weight excludes every circular order** (REV-0006: 25 620 networks searched over
  all orders).  All of level 2 rests on Theorem 12(a), i.e. on a computed table of local terms that no kernel
  checks.  The dichotomy of blobs with two hybrid nodes is known (Huber et al., arXiv:2408.12997).
* **Beyond level 2** (`NANUQ_HIGHER_LEVELS.md`; CX-T31, CX-X3; reviewed in REV-0006, two statements corrected):
  blob-locality at every level (Theorem A); a survey of six-leaf outer-labeled planar networks by hybrid
  insertion up to four hybrid nodes (114 of 150 systems; four of the missing 36 are impossible for every
  network).  **A survey, not a classification, and not exhaustive:** it identifies networks by an invariant
  that is incomplete from three hybrid nodes on.  Open questions: `OPEN_PROBLEMS.md` B, "Beyond level 2".
* **Ising ground sets** (`ISING_GROUND_SETS.md`; CX-T16–T19, T25, T28, T29): the Ensemble division's E-C1 — linear
  time for fixed `K`, `2^{O(K)}·poly(n)` in general, **open for `K ≫ log n`**.  Mostly known mathematics
  (Laurent–Poljak; Tropp; Odlyzko for random states); ours with no source found: the criterion in `K` dimensions,
  the singleton family as stated, the Sidon criterion, and the NP-completeness of the span problem (the fourth
  referee's reduction).  Reviewed (REV-0004, REV-0005); CX-T25 and Proposition 11 unreviewed.
* **Chain geometry** (`CHAIN_GEOMETRY_HARDNESS.md`; CX-T32, T33; reviewed in REV-0006): the Geometry division's C1.
  Optimising pair data over one chain conformation is the Heisenberg ground-state problem; NP-hard and hard to
  approximate — **known** (Kallaugher et al. 2024; Piddock 2025), two short proofs of ours; fixed bond angles do
  not help when many pairs carry data of both signs (one pair is polynomial: Borcea–Streinu); tractable for
  short-range data.  **Realizability of averaged data is weakly NP-hard for an accuracy in binary; for accuracy
  `1/poly` only given a theorem (Liu 2007, via Gharibian 2010) that nobody here has read.**
* **Certified brackets** (`CERTIFIED_BRACKETS.md`; CX-T35, T36; **unreviewed**; known mathematics): for the
  Structural Biology and Frontier divisions — a martingale second-order bound for `ln Z` (valid, loose) and an
  obstruction (no polynomial certificates within `δβΣo_e` unless NP = co-NP).
* **Penalised models** (`PENALTY_THRESHOLD.md`; CX-T21–T23; reviewed in REV-0006, one misprint): answers to the
  theory and science divisions; no new mathematics claimed.
* The two starting problems of the brief changed status when verified: A2 solved elsewhere; B1/B2
  claimed elsewhere.  See `OPEN_PROBLEMS.md`.
* **Nothing is running:** no sub-agent, no background process, no remote job (none was ever launched), no
  scheduled task of this division.  The session's scratch directory is not durable; everything needed is in the
  repository.

## Directives in force (from the research owner)

1. The founding mandate (re-sent 2026-11-26 about 20:45 UTC, unchanged): open problems in mathematical biology /
   complexity; write only to `research/biological-complexity`; no merges, force pushes, pull requests or changes
   to other divisions' branches; abstract models and synthetic instances only (no sequence engineering,
   target-specific optimisation or experiments); labels [V]/[P]/[K]/[N]/[C]; no `sorry`, no new axioms;
   consolidation when about $2,000 of credits remain (the consolidation directive came earlier: item 5); **hard stop 30 November
   2026, 3:00 PM Eastern Time**.
2. Supplementary directive "Mathematical Generality, Physical Relevance, and Foundational Breakthroughs" (known to
   us through the theory division's relay THY-MSG-0016): the assumption audit `ASSUMPTION_AUDIT.md`.
3. Supplementary directive "Computational Complexity, Algorithmic Feasibility and Structural Biology Software"
   (received 2026-11-26 about 22:02 UTC): a **seventh division**, Structural & Computational Biology, Software
   Development and Applications, on branch `research/structural-biology`, digest
   `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md`.  Our primary task stays mathematical discovery; in addition:
   read their branch, answer their computational obstacles with precise classifications (exact / parameterised /
   approximation / certification; worst case versus average case), propose stress tests with Engineering.  The
   initial orientation is COMPLEXITY-MSG-0005, written **before their branch existed** (2026-11-26 22:05 UTC: the fetch
   failed) — re-fetch, read their digest, and revise or answer.  Their branch exists since 22:30 UTC (`720e0ec`); they
   read ours at `25bcd61`, i.e. before COMPLEXITY-MSG-0005.
4. Supplementary directive "Frontier Scientific Evaluation and Eighth-Division Coordination" (received 2026-11-26
   about 22:40 UTC): an **eighth division**, Frontier Benchmarking, Experimental Evidence and Scientific Evaluation,
   on branch `research/frontier-benchmarks`, digest `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md` (the branch did
   not exist at the fetch of 22:46 UTC).  It designs independent evaluations and keeps benchmark integrity; we do **not**
   duplicate that mandate.  Ours: keep the protocol copy current (`docs/collaboration/README.md`, done), read its
   findings, answer its scientific questions, and if an evaluation exposes a mathematical limitation, examine
   whether it calls for a stronger theorem, a constructive algorithm, a generalisation or a rigorous obstruction.
   Keep the distinctions *genuine blind assessment / pre-leaderboard assessment / retrospective evaluation*; do not
   assume CASP17 references are confidential (official results: 29 November 2026; no official participation is
   claimed).  Ubuntu remains responsible for substantial shared computation.  No new repositories, no changes to
   other branches, no expansion of spending limits.

5. **"Urgent Research Owner Directive — Controlled Consolidation and Temporary Research Halt"** (received
   2026-11-27 about 00:58 UTC; **governing**; it supersedes every earlier instruction to work in continuous
   loops).  No new research directions, literature investigations, software projects, benchmarks or sub-agents;
   finish only what is nearly finished; document unresolved problems instead of pursuing them; write the
   consolidation report `docs/collaboration/consolidation/complexity.md`; no new Modal jobs; do not open sealed
   held-out data, disclose credentials or tune against held-out results; commit, push, send one final message
   (COMPLEXITY-MSG-0007), report to the owner, and **stop: do not start another research cycle, do not resume
   automatically when another division sends a message, do not schedule sessions; wait for the owner's explicit
   authorisation.**  Done at the commit that carries this file.

The eight branches: theory `claude/determined-ride-og1u7j`, engineering `research/ubuntu-engineering`, science
`research/scientific-translation`, ensemble `research/ensemble-identifiability`, geometry
`research/geometric-inference`, complexity `research/biological-complexity`, structural biology
`research/structural-biology`, frontier `research/frontier-benchmarks`.

## How to re-run everything we claim

```
pip install networkx numpy scipy                      # dependencies beyond the standard library
cd experiments/complexity/nanuq
python3 exhaust_all_systems.py 4 5 6                  # CX-D2 / CX-X1
python3 exhaust_tree_generated.py 5 6 7               # CX-X1
python3 test_bloblets.py 3 4 5 6 7 8                  # CX-X2, level 3 (about 90 s; presupposes Lemma A)
python3 five_point_facts.py                           # CX-T5, Lemma 4
python3 check_decomposition.py                        # CX-T5, Proposition 2 (minutes)
python3 verify_class.py                               # CX-T6, Lemma 8 (about 1 min)
python3 class_table6.py                               # Appendix B of the NANUQ note
python3 characterize6.py                              # CX-T8 (about 2 min)
python3 counterexample7.py                            # CX-T7: the 7-leaf non-galled network
python3 verify_nongalled.py; python3 verify_nongalled2.py
python3 nongalled_formula.py                          # CX-T7: exact weights in the family
python3 modified_nanuq_witness7.py                    # Theorem 11(c): the seven-leaf witness (after REV-0004)
python3 export_lean_lists.py                          # the list C6 in the Lean file is the computed closure
python3 kalmanson_only.py; python3 kalmanson_only.py extra   # CX-T26 (seconds)
python3 forbidden_in_nstar.py                         # the forbidden pattern inside the 7-leaf counterexample
python3 level2_classification.py 13 1500 7            # CX-T27: finite facts, table of local terms, bloblets, glued systems
python3 level2_explicit.py 400 2 12                   # CX-T27 on explicit rooted networks (independent calculator; minutes)
python3 level2_fourtrees_check.py                     # the four trees of the nested blob against explicit networks
python3 level2_all_orders.py 13 10                    # CX-T34 (Theorem 12'): five leaves exclude every circular order (about 4 min)
python3 level2_all_orders_explicit.py 500 6 12 8      # the same on explicit rooted networks (seconds)
python3 six_leaf_survey.py 3                          # six-leaf survey, three hybrid nodes (27 min); "4 sym": four (about 95 min)
cd ../reviews/rev2_nanuq                              # the NANUQ referee's independent explicit-network tests
python3 t_exhaust.py 5 2                              # (see ../README.md for the rest)
cd ../../strands
python3 test_partition_reduction.py                   # CX-T1/T3 on tiny instances (seconds)
python3 test_partition_reduction_big.py               # larger instances (minutes)
python3 test_generalised_hypotheses.py                # CX-T1 with (H2'), CX-T15, CX-T20, Fact 1, orbits (7 s)
python3 test_generalised_hypotheses.py big            # five larger instances (about 4 min)
python3 test_eth_chain.py                             # Appendix A of the hardness note (1 s)
python3 test_multiset_dp.py                           # CX-T10..T12 on 20 systems (seconds)
python3 test_multiset_dp_random.py 1 200 13           # 200 random systems (seconds)
python3 test_multiset_dp_random.py 2 60 16            # 60 larger random systems (about a minute)
python3 test_multiset_dp_edges.py                     # input checks, minimum hairpin size (after REV-0003)
python3 level_counts.py                               # CX-T30: MFE and level counts per symmetry class (seconds)
cd ../ising_faces
python3 table_k4.py; python3 table_k5.py; python3 span_rule.py; python3 test_theory.py   # CX-T16..T19
python3 span_algorithm.py                             # the 2^K algorithm, singletons, conditions, the reduction of CX-T29 (2 min)
python3 degree2_certificates.py                       # CX-T28 (minutes)
cd ../penalty_threshold
python3 price_bound.py 3; python3 hardness_maxcut.py      # CX-T21..T23 (toy models, exact enumeration)
cd ../chain_geometry
python3 heisenberg_reduction.py                       # CX-T32, T33: gadget, reduction, bijection, linkage, one instance end to end (2 min)
python3 maxcut_k_lifting.py                           # CX-T32: the exact lifting from dimension k to k+1 (2 min)
cd ../../..
export PATH="$HOME/.elan/bin:$PATH"                   # Lean (lake exe cache get once)
lake env lean experiments/complexity/lean/StackPacking.lean
lake env lean experiments/complexity/lean/JordanOrbit.lean
lake env lean experiments/complexity/lean/NanuqFinite.lean   # 3.5 min, needs about 11 GB; do not run it next to other heavy jobs
lake env lean experiments/complexity/lean/FourPartition.lean  # CX-V4
lake env lean experiments/complexity/lean/NanuqPattern.lean   # CX-V5: Corollary 5' on six points (prints the axioms)
lake env lean experiments/complexity/lean/ChainGadgets.lean   # CX-V6: the gadget inequalities of the chain note (prints the axioms; 8 s)
```

Further programs: `experiments/complexity/certified_brackets/martingale_bound.py` (CX-T35, toy models, seconds);
`experiments/complexity/nanuq/six_leaf_treesets.py` (sets of displayed trees; exploration, 19 minutes for three
hybrid nodes); the six referees' programs in `experiments/complexity/reviews/` (README there).  The Lean
toolchain and Mathlib are pinned in the repository (`lean-toolchain`, `lake-manifest.json`);
`experiments/complexity/lean/README.md` gives the commands and what each file proves.

## Things a successor must not do

* Do not cite B1/B2 as "open" or as "proved by us" without the qualification in `OPEN_PROBLEMS.md` B, and do
  not call the all-level NANUQ theorem new (`DEAD_ENDS.md` CX-D5).
* Do not describe the hardness result as a statement about published parameter tables or about "the
  nearest-neighbour model as implemented"; its hypotheses are (H0)/(C0)/(D0), (H1), (H2′).
* Do not edit files inherited from the theory branch.
* Do not attach or read third-party repositories without the research owner's authorisation (one such
  request was denied in session 1).
* Do not call the partition function over all strand orderings new without the qualifier "in the
  nearest-neighbour model": for the base-pair model it is Theorem 4 of Boehmer et al. (journal version 2025).
  Do not offer a `(min,+)` recursion for the minimum free energy with symmetry: it is wrong (CX-T30).
* Do not state "exposed iff the Hamming metric decomposes uniquely" (false beyond simplicial faces), and
  attribute Corollary 7 / Proposition 5 of the Ising note to Laurent–Poljak.
* Read the actual journal version of a paper before a novelty statement, not only the conference version
  (this cost us one wrong paragraph: REV-0003, finding 1).
* Do not write files with an unquoted shell here-document: backticks in the text are executed (it happened
  once, commit 21161f4, repaired in 2c0cf1a).
* Read the clock (`date -u`) for message headers — immediately before writing the time, not from memory of an
  earlier command (three times on 26 November a time was written a few minutes ahead of the clock and corrected).
* Do not present the NP-hardness of the Heisenberg / vector Max-Cut problem as ours: Kallaugher et al. (2024),
  Piddock (2025).  Do not present the degree-2 criterion of the Ising note or the random-state bound as ours:
  Laurent–Poljak; Odlyzko.  Do not say that Theorem 6 of Boehmer et al. is about the base-pair model.
* **Search before proving, under the classical name of the problem** (`PRIOR_ART.md` §D records an hour in which
  a second proof of a 2025 theorem looked like a proof of an open conjecture).
* **A citation from memory carries only its weakest reading.**  Corollary 5 of the chain note claimed an accuracy
  of `1/poly` on the Grötschel–Lovász–Schrijver equivalence, which gives accuracy in binary (REV-0006).  Until
  someone reads Liu's Proposition 2.8, quote the realizability statement in its conditional form.
* Do not quote the six-leaf survey as a classification or its counts as numbers of networks: they are numbers of
  unfolding classes, and the four-hybrid level is incomplete (REV-0006, finding 4).  Do not state the robust
  criterion beyond level 2 without including subnetworks.
* When a corollary quotes a theorem of another note, copy its hypotheses literally (Corollary C lost `k_1 ≥ 1`
  and became false).  When a program "checks an inequality of the note", make it check the inequality as
  printed (the penalty note's program checked a correct variant of a misprinted chain).
* Do not act on the two scheduled tasks visible in the owner's account: neither was created by this division.

