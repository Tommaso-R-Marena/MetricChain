# Handoff (complexity division)

*Updated 2026-11-26, session 1.*

## State in five lines

* Branch `research/biological-complexity`, based on theory checkpoint `a844b5a`.  Only files under
  `docs/complexity/`, `docs/collaboration/**/complexity*`, `experiments/complexity/`, `proofs/Complexity/`
  are ours.
* Strands, hardness: NP-hardness of multi-strand MFE (and #P-hardness of #SSEL) in the nearest-neighbour
  model, `STRANDS_NN_HARDNESS.md` — **under review**, exhaustively checked on tiny instances.
* Strands, algorithm: magnified partition function over all orderings with symmetry by a sub-multiset
  dynamic programme, `STRANDS_ALGORITHM.md` — **unreviewed**, agrees exactly with exhaustive enumeration
  on 280 systems.
* The two starting problems of the brief changed status when verified: A2 solved elsewhere; B1/B2
  claimed elsewhere (unreviewed, proof not accessible to us).  See `OPEN_PROBLEMS.md`.
* Phylogenetic networks (`NANUQ_LOCAL_CRITERION.md`, **unreviewed**): a local criterion for circular
  decomposability of the NANUQ metric; all galled outer-labeled planar networks of every level satisfy it
  (independent proof of a statement claimed earlier by a third party); an explicit 7-leaf non-galled
  level-2 counterexample; sharpness of the criterion.
* Next steps: `RESEARCH_LOG.md`, "Resume here".

## How to re-run everything we claim

```
pip install networkx                                  # only dependency beyond the standard library
cd experiments/complexity/nanuq
python3 exhaust_all_systems.py 4 5 6                  # CX-D2 / CX-X1
python3 exhaust_tree_generated.py 5 6 7               # CX-X1
python3 test_bloblets.py 3 4 5 6 7 8                  # CX-X2, level 3 (about 90 s)
python3 five_point_facts.py                           # CX-T5, Lemma 4
python3 check_decomposition.py                        # CX-T5, Proposition 2 (minutes)
python3 verify_class.py                               # CX-T6, Lemma 8 (about 1 min)
python3 characterize6.py                              # CX-T8 (about 2 min)
python3 counterexample7.py                            # CX-T7: the 7-leaf non-galled network
python3 verify_nongalled.py; python3 verify_nongalled2.py
cd ../strands
python3 test_partition_reduction.py                   # CX-T1/T3 on tiny instances (seconds)
python3 test_partition_reduction_big.py               # larger instances (minutes)
python3 test_multiset_dp.py                           # CX-T10..T12 on 20 systems (seconds)
python3 test_multiset_dp_random.py 1 200 13           # 200 random systems (seconds)
python3 test_multiset_dp_random.py 2 60 16            # 60 larger random systems (about a minute)
```

## Things a successor must not do

* Do not cite B1/B2 as "open" or as "proved by us" without the qualification in `OPEN_PROBLEMS.md` B.
* Do not edit files inherited from the theory branch.
* Do not attach or read third-party repositories without the research owner's authorisation (one such
  request was denied in session 1).
