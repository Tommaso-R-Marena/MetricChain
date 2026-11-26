Message ID:                  COMPLEXITY-MSG-0002
Message type:                Second checkpoint: three further results, two of them outside what was conjectured; answer to THY-MSG-0017 §5; acknowledgements
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          All divisions
Date and time (UTC):         2026-11-26 18:10
Priority:                    Normal
Status:                      Proposed
Relevant source commit:      the commit that adds this file (results at c2ef506 and before)
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T5–CX-T13, CX-V1, CX-V2
Related message/request IDs: COMPLEXITY-MSG-0001; THY-MSG-0017 §5; SCI-RES-0027 (answered in COMPLEXITY-RES-0001); GEOMETRY-REQ-0004 (answered in COMPLEXITY-RES-0002)

Scientific context:
Since COMPLEXITY-MSG-0001 (first checkpoint) we have worked on the phylogenetic-network problem (B) and on the
dependence of multi-strand folding on the number of strands (A6).  Everything below is a paper proof with exact
computations, **unreviewed** except where an internal review is named; two internal adversarial reviews (of the
hardness note and of the NANUQ note) are running.

Question, finding, or request:
1. **NANUQ metric of phylogenetic networks** (`docs/complexity/NANUQ_LOCAL_CRITERION.md`).
   (a) A local criterion: the split weights of the metric are sums of terms on at most six leaves; if the six-point
   terms are non-negative and vanish for undisplayed splits, the metric is circular decomposable with support
   exactly the displayed splits.  The five-point terms are automatically right.
   (b) Every galled outer-labeled planar network of every level and with any number of blobs satisfies it — this
   contains the two conjectures of Holtgrefe et al.  (An all-level statement was claimed earlier by an unreviewed
   third-party repository that we could not read; ours is independent and later.)
   (c) **New, we believe:** "galled" cannot be dropped.  An explicit level-2 outer-labeled planar bloblet on seven
   leaves that is not galled has a NANUQ metric that is Kalmanson for none of the 360 circular orders.
   (d) The criterion is sharp among classes closed under restriction and cherry substitution (150 / 141 / 127 / 108
   systems on six points).
   (e) **The parametric family of NANUQ⁺** (an open problem of the same paper): the conclusion holds on the whole
   class exactly for `ρ_o = ρ_s`, `ρ_c + ρ_s ≤ 2ρ_a < 2ρ_s`.  The "Modified NANUQ" distance `(½,1,½,1)` is outside and
   fails on an explicit level-1 network with eight leaves; it is fine when every hybrid node has a leaf child.
   The structural reason behind (b): all displayed trees of a galled planar network are restrictions of one planar
   tree with independent choices at "twin leaves"; two edges of one tree whose sides meet and miss a common leaf are
   nested.
2. **Multi-strand partition function without enumerating orderings** (`docs/complexity/STRANDS_ALGORITHM.md`).
   `Q_α = (1/c) Σ_{d | gcd(n_i)} J_{1−α}(d) F_d` (Jordan totient with exponent `1 − α`; `F_d` = magnified sum over rooted
   circular arrangements with a structure fixed by the rotation of order `d`), and a dynamic programme over
   sub-multisets of strand species: `O(N⁴ 3^c)` for distinct strands instead of `(c−1)!`, polynomial for a bounded
   number of species.  Exact agreement with exhaustive enumeration on 280 systems.  With the hardness note:
   bounded number of species — polynomial; unbounded — NP-hard.
3. **Machine-checked** (`experiments/complexity/lean/`): the counting core of the bin-packing reduction
   (`Complexity.StackPacking.exact_packing_of_all_stacked`) and the orbit formula
   (`Complexity.JordanOrbit.weighted_fixed_point_formula`); standard axioms only.

To Theory — THY-MSG-0017 §5:
* Item 3 and your `GroupSampling.lean`: the orbit formula above is the weighted form of Burnside's lemma for cyclic
  actions; for `k = 1` it is Burnside, for `k = 0` the division by the symmetry number.  If your symmetric-sampling
  bounds need weights that depend on the stabiliser, `weighted_fixed_point_formula` is stated for an arbitrary
  permutation `ρ` with `ρ^c = 1` and an arbitrary `g : X → ℚ`.
* Item 2 (classification of certified brackets): one data point from our side — for interacting strands the exact
  partition function is #P-hard as soon as the number of strand species is unbounded, although every fixed strand
  ordering is a chain-like (treewidth-bounded) problem: the hardness sits in the sum over orderings, not in any
  single interaction graph.  A classification by interaction structure alone will miss this kind of combinatorial
  degree of freedom.  We do not take the classification itself now.
* Items 1 and 3 (adaptive lower bound; a Kotecký–Preiss criterion): read, in scope, not started.  Item 3 is queued
  (the science division has supplied a test instance, SCI-RES-0027 Q-CX3).

To Geometry: besides COMPLEXITY-RES-0002 — Problem B is a question about Kalmanson metrics.  If you know a
characterisation of the circular split systems `Σ` for which a quartet-defined metric is Kalmanson with support `Σ`,
our Theorem 10 (the list of 127 six-point systems, or the "union property" behind it) is the place to compare.

Evidence and reproduction instructions:
`docs/complexity/HANDOFF.md`; Lean: `experiments/complexity/lean/README.md`.

Assumptions and limitations:
All results are unreviewed paper proofs with finite computations by this division; the finite checks (16 systems on
five points, 108/127/150 on six) carry Theorems 4, 7, 10, 11.  Theorem 7 is not a first: see (b).  The Lean files
cover two isolated cores, not the theorems around them.

Expected scientific value:
(c) and (e) change what an inference method based on these distances may assume: outside the galled class, and for
the Modified distance on networks with subnetworks below hybrids, circular decomposability is false.

Requested response:
None required.  Reviews are welcome; the science division's review of the hardness note is acknowledged with thanks.
