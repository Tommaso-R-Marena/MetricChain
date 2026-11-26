# Handoff (complexity division)

*Updated 2026-11-26, session 1.*

## State in five lines

* Branch `research/biological-complexity`, based on theory checkpoint `a844b5a`.  Only files under
  `docs/complexity/`, `docs/collaboration/**/complexity*`, `experiments/complexity/`, `proofs/Complexity/`
  are ours.
* One paper-proof result so far: NP-hardness of multi-strand MFE (and #P-hardness of #SSEL) in the
  nearest-neighbour model, `STRANDS_NN_HARDNESS.md` — **unreviewed**, exhaustively checked on tiny instances.
* The two starting problems of the brief changed status when verified: A2 solved elsewhere; B1/B2
  claimed elsewhere (unreviewed, proof not accessible to us).  See `OPEN_PROBLEMS.md`.
* Exhaustive evidence that the NANUQ statement holds for galled planar bloblets of levels ≤ 6 on small
  leaf sets, and fails for general circular split systems.
* Next steps: `RESEARCH_LOG.md`, "Resume here".

## How to re-run everything we claim

```
pip install networkx                                  # only dependency beyond the standard library
cd experiments/complexity/nanuq
python3 exhaust_all_systems.py 4 5 6                  # CX-D2 / CX-X1
python3 exhaust_tree_generated.py 5 6 7               # CX-X1
python3 test_bloblets.py 3 4 5 6 7 8                  # CX-X2, level 3 (about 90 s)
cd ../strands
python3 test_partition_reduction.py                   # CX-T1/T3 on tiny instances (seconds)
python3 test_partition_reduction_big.py               # larger instances (minutes)
```

## Things a successor must not do

* Do not cite B1/B2 as "open" or as "proved by us" without the qualification in `OPEN_PROBLEMS.md` B.
* Do not edit files inherited from the theory branch.
* Do not attach or read third-party repositories without the research owner's authorisation (one such
  request was denied in session 1).
