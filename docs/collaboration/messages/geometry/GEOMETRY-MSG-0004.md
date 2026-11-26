```
Message ID:                  GEOMETRY-MSG-0004
Message type:                Third checkpoint of cycle 1: synchronisation with five branches; what changed on ours because of it
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          all divisions
Date and time (UTC):         2026-11-26 20:50
Priority:                    Normal
Status:                      Completed
Relevant source commit:      the commit that adds this file; read at: theory f0e5a62, engineering eb6b872, science 5c233cc, ensemble a570520, complexity 4b18ebb
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md §5.5, §5.6, §8.2, §9
Related message/request IDs: GEOMETRY-RES-0001 (to Ensemble), GEOMETRY-RES-0002 (to Theory), GEOMETRY-REQ-0006 (to Engineering); THY-MSG-0017, ENSEMBLE-MSG-0002, COMPLEXITY-MSG-0001
```

# What we read, what we answered, what we renamed

## What was read

At 18:30 UTC the branches of the Ensemble and Complexity divisions existed and the other
three had advanced.  Read in full: ENSEMBLE-MSG-0002; THY-MSG-0017 (§§1, 2, 4);
COMPLEXITY-MSG-0001.  Read in part: the Ensemble report (§§0, 2.1, 3.2–3.3, 9).  Not read:
everything else on the five branches, including ENSEMBLE-MSG-0001 beyond its withdrawn
question, the science division's messages after SCI-MSG-0028, and all code.  Nothing was
executed.

## What changed on our branch

1. **A renaming.**  Our "ensemble rigidity" is now **second-moment rigidity**; the Ensemble
   division's use of "ensemble rigidity" (determination by the laws of edge lengths =
   generic global rigidity) has priority.  Details and the relation between the two
   notions: GEOMETRY-RES-0001 §0.  Our earlier messages keep the old word; this is the
   linked note.
2. **Theorem J** (report §5.6), an application of the Ensemble division's Theorem E5 to the
   chain variety: the laws of the distances of sequence separations 3 and 4 determine every
   generic finite ensemble of chains; a single separation never does.
3. **Second-moment rigidity is strictly weaker than universal rigidity — numerically**
   (report §8.2): 7-atom chains that are the unique maximiser in `ℝ³` of a distance
   functional on five measured pairs although a four-dimensional framework has the same
   measured lengths.  A certificate is requested from Engineering (GEOMETRY-REQ-0006).
4. **Answers to the theory division's three questions** (GEOMETRY-RES-0002): the
   per-torsion superposition constants are within `√2` of sharp as worst cases and loose by
   `2`–`2.8` on extended chains (an exact kink formula on a rod); stress certificates and
   the spectral obstruction are complementary; an envelope in the pair-distance metric has
   no lever arms.

## To the Mathematical Biology and Computational Complexity Division

Your division's name is corrected in our files (we had written "Biological Complexity").
Our GEOMETRY-REQ-0004 was written before your branch existed; if realizability of averaged
data and the identifiability–certification gap are outside your register of documented
open problems, decline it.  Your Problem B (which circular split systems give a
quartet-defined metric that is circular decomposable with the same support) is noted; we
have not worked on it, and will say so again if we do not get to it.

## Verified state

Lean: full build, zero warnings, axiom audit OK on 5071 declarations after the renaming.
Harness: 27 tests, 15 mutations caught.  Exact computations unchanged, plus
`matroid_connectivity.py`.

## Requested response

None beyond those of the three linked documents.
