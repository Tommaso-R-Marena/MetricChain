# Handoff (complexity division)

*Updated 2026-11-26 23:28 UTC, session 1 (after the fifth internal review; fifth checkpoint in preparation).*

## State in a few lines

* Branch `research/biological-complexity`, based on theory checkpoint `a844b5a`.  Only files under
  `docs/complexity/`, `docs/collaboration/**/complexity*`, `docs/collaboration/README.md` (our copy of the
  protocol), `experiments/complexity/` are ours.
* **Five internal reviews** (COMPLEXITY-REV-0001 to -0005, verbatim with dispositions in
  `docs/collaboration/messages/complexity/`), plus the science division's SCI-REV-0019.  **No theorem was ever
  found false.  What the reviews corrected, three times over, are statements about novelty and attribution**
  (`ASSUMPTION_AUDIT.md` §6).  Internal AI reviews are not peer review.
* **Strands, hardness** (`STRANDS_NN_HARDNESS.md`; CX-T1–T4, T14, T15, T20, T24): multi-strand MFE is strongly
  NP-hard, #SSEL #P-hard, in the nearest-neighbour model with exterior loops 0, for every fixed energy function
  with (H1), (H2′); flush coaxial stacking, dangles, several complexes; ETH bound.  Reviewed three times: correct.
* **Strands, algorithm** (`STRANDS_ALGORITHM.md`; CX-T10–T12, T30): magnified partition function, MFE and level
  counts over all orderings with symmetry, `O(N⁴3^c)`, polynomial for bounded species.  Reviewed (REV-0003,
  REV-0005): correct.  **Novelty is modest:** for the base-pair model this is Boehmer et al. (journal version
  2025), who also write that the extension to the Turner model "does not pose any algorithmic challenges"; ours
  is that extension written out and tested, and it answers a question Shalaby and Woods list as open.
* **Phylogenetic networks** (`NANUQ_LOCAL_CRITERION.md`; CX-T5–T9, T13, T26, T27, T34; Lean CX-V3, V5): local
  criterion; all galled outer-labeled planar networks (probable rediscovery of an unreviewed third-party claim);
  "galled" is necessary; the sharp classes for exact support (`𝒦`, 127 six-point systems) and for "Kalmanson"
  alone (`𝒦′`, 133; a forbidden six-leaf pattern); **level 2 completely** — one critical split per nested blob,
  weight `β_1G + ξ_1R − Σβ_jβ_l` (reviewed in REV-0005 on 1.4 million explicit networks); and, **new and
  unreviewed, Theorem 12′ (CX-T34): a negative critical weight excludes every circular order**, so for level 2
  "`d_N` is circular decomposable" is decided by the critical weights.  The dichotomy of blobs with two hybrid
  nodes is known (Huber et al., arXiv:2408.12997).
* **Beyond level 2** (`NANUQ_HIGHER_LEVELS.md`; unreviewed): blob-locality at every level (Theorem A); a survey of
  six-leaf outer-labeled planar networks by hybrid insertion (three hybrid nodes: only the 108 systems of `𝒞_6`
  and the six images of "all but one 2-split"; four: see the note).  A survey, not a classification.
* **Ising ground sets** (`ISING_GROUND_SETS.md`; CX-T16–T19, T25, T28, T29): the Ensemble division's E-C1 — linear
  time for fixed `K`, `2^{O(K)}·poly(n)` in general, **open for `K ≫ log n`**.  Mostly known mathematics
  (Laurent–Poljak; Tropp; Odlyzko for random states); ours with no source found: the criterion in `K` dimensions,
  the singleton family as stated, the Sidon criterion, and the NP-completeness of the span problem (the fourth
  referee's reduction).  Reviewed (REV-0004, REV-0005).
* **Chain geometry** (`CHAIN_GEOMETRY_HARDNESS.md`; CX-T32, T33; **unreviewed**): the Geometry division's C1.
  Optimising pair data over one chain conformation is the Heisenberg ground-state problem; NP-hard and hard to
  approximate — **known** (Kallaugher et al. 2024; Piddock 2025), two short proofs of ours; fixed bond angles do
  not help; realizability of averaged data is weakly NP-hard; tractable for short-range data.
* **Penalised models** (`PENALTY_THRESHOLD.md`; CX-T21–T23): answers to the theory and science divisions.
  **Unreviewed by us**; the science division commented (SCI-RES-0034, two sentences corrected); no new
  mathematics claimed.
* The two starting problems of the brief changed status when verified: A2 solved elsewhere; B1/B2
  claimed elsewhere.  See `OPEN_PROBLEMS.md`.
* Next steps: `RESEARCH_LOG.md`, "Resume here".

## Directives in force (from the research owner)

1. The founding mandate (re-sent 2026-11-26 about 20:45 UTC, unchanged): open problems in mathematical biology /
   complexity; write only to `research/biological-complexity`; no merges, force pushes, pull requests or changes
   to other divisions' branches; abstract models and synthetic instances only (no sequence engineering,
   target-specific optimisation or experiments); labels [V]/[P]/[K]/[N]/[C]; no `sorry`, no new axioms;
   consolidation when about $2,000 of credits remain (directive not yet received); **hard stop 30 November
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
