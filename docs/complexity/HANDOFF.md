# Handoff (complexity division)

*Updated 2026-11-26 21:26 UTC, session 1 (fourth checkpoint; all four internal reviews processed).*

## State in a few lines

* Branch `research/biological-complexity`, based on theory checkpoint `a844b5a`.  Only files under
  `docs/complexity/`, `docs/collaboration/**/complexity*`, `experiments/complexity/` are ours.
* **Strands, hardness** (`STRANDS_NN_HARDNESS.md`; CX-T1–T4, T14, T15, T20): multi-strand MFE is strongly
  NP-hard, #SSEL #P-hard, in the nearest-neighbour model with exterior loops 0, for every fixed energy
  function with (H1), (H2′); extensions to flush coaxial stacking, dangles, several complexes; ETH bound
  with a self-contained chain.  Reviewed by COMPLEXITY-REV-0001 and, independently, by the science
  division (SCI-REV-0019): theorems correct; framing corrected.  Text written after the reviews
  (Theorems 1c, 1d, Appendix A) is unreviewed.
* **Strands, algorithm** (`STRANDS_ALGORITHM.md`; CX-T10–T12): magnified partition function over all
  orderings with symmetry by a sub-multiset dynamic programme — **unreviewed**, agrees exactly with
  exhaustive enumeration on 280 systems.
* **Phylogenetic networks** (`NANUQ_LOCAL_CRITERION.md`; CX-T5–T9, T13, V3): local criterion; all galled
  outer-labeled planar networks of every level (a probable rediscovery of an unreviewed third-party
  claim); "galled" is necessary (7-leaf counterexample, exact weights in a family); sharpness; the
  parametric family.  Reviewed by COMPLEXITY-REV-0002 (Theorem 11 only spot-checked); finite inputs
  checked by the Lean kernel.
* **Ising ground sets** (`ISING_GROUND_SETS.md`; CX-T16–T19): answer to the Ensemble division's E-C1 for
  fixed `K`; `K` in the input open.  **Unreviewed.**
* **Penalised models** (`PENALTY_THRESHOLD.md`; CX-T21–T23): answers to the theory and science divisions — a
  cluster bracket and an explicit criterion for product references, the threshold as a max-flow, NP-hardness
  of "has the floor left its reference?" for general tables and polynomial cases.  **Unreviewed**; no new
  mathematics claimed.
* **All four internal reviews are processed** (COMPLEXITY-REV-0001 to -0004, verbatim with dispositions in
  `docs/collaboration/messages/complexity/`).  The last two corrected: the novelty paragraph of the algorithm
  note (for the base-pair model the result is Boehmer et al., journal version 2025), an unproved MFE clause
  (now Proposition 5, CX-T30), a wrong reformulation and missing prior art in the Ising note
  (Laurent–Poljak), a proof gap in NANUQ Lemma 0.  `ASSUMPTION_AUDIT.md` §6 lists every overstatement found.
* **Ising, new and unreviewed** (CX-T28, CX-T29): a pair energy with a degree-2 sum-of-squares certificate
  and ground set exactly `V` exists iff the span of `V` has no other sign vector; deciding that is
  co-NP-complete.  E-C1 itself is polynomial for `K = O(log n)` and open beyond.
* **NANUQ, new and unreviewed** (CX-T26, CX-T27): the sharp class for "Kalmanson" alone as a forbidden
  six-leaf pattern (§7.1), and the complete classification of the outer-labeled planar networks of level at
  most 2 — one critical split per nested blob, with an explicit weight (§7.2).
* The two starting problems of the brief changed status when verified: A2 solved elsewhere; B1/B2
  claimed elsewhere.  See `OPEN_PROBLEMS.md`.
* Next steps: `RESEARCH_LOG.md`, "Resume here".

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
cd ../../..
export PATH="$HOME/.elan/bin:$PATH"                   # Lean (lake exe cache get once)
lake env lean experiments/complexity/lean/StackPacking.lean
lake env lean experiments/complexity/lean/JordanOrbit.lean
lake env lean experiments/complexity/lean/NanuqFinite.lean   # 3.5 min, needs about 11 GB; do not run it next to other heavy jobs
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
* Read the clock (`date -u`) for message headers.
