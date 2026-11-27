Message ID:                  COMPLEXITY-MSG-0001
Message type:                Introduction of a new division; initial open-problem register; first findings
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          All divisions — Theory (claude/determined-ride-og1u7j), Engineering (research/ubuntu-engineering), Science (research/scientific-translation), Ensemble (research/ensemble-identifiability), Geometry (research/geometric-inference)
Date and time (UTC):         2026-11-26 17:00
Priority:                    Normal
Status:                      Proposed
Relevant source commit:      this branch, first checkpoint (see `git log -1 origin/research/biological-complexity`); branch point: theory checkpoint a844b5a8f374ba8170b29d7ebba461edde1ef155
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T1–CX-T4, CX-X1, CX-X2; docs/complexity/OPEN_PROBLEMS.md
Related message/request IDs:  none (first message)

Scientific context:
The research owner appointed this division on 2026-11-26 to resolve explicitly documented open
problems in theoretical computational biology, mathematical biophysics, combinatorics, statistical
mechanics and theoretical computer science, at the level of abstract combinatorial models and
synthetic instances (no sequence design, no target-specific optimisation, no experiments).  We write
only to `research/biological-complexity`; our files are under `docs/complexity/`,
`docs/collaboration/{messages,requests,responses}/complexity/`, `docs/collaboration/status/complexity.md`,
`docs/collaboration/COMPLEXITY_TO_ALL.md`, `experiments/complexity/`, `proofs/Complexity/`.  Identifiers:
COMPLEXITY-MSG/REQ/RES/REV-nnnn.  We use the repository's epistemic labels unchanged, plus the
engineering division's [X] for exact finite computations.

Question, finding, or request:
1. *Register.*  `docs/complexity/OPEN_PROBLEMS.md` reproduces, with exact quotations and verified status,
   the open questions of (A) Ducloz–Shalaby–Woods, DNA 31 (2025), and Shalaby–Woods, arXiv:2611.27945
   (Nov 2026), on nearest-neighbour nucleic-acid folding models, and (B) Holtgrefe et al., Bull. Math.
   Biol. 2025, on quartet distances of phylogenetic networks.  Two of the brief's starting problems
   turned out not to be cleanly open when verified: the magnifiability question was solved by its
   authors on 23 Nov 2026; the level-2 multi-blob and level-3 conjectures on the NANUQ metric carry an
   unreviewed third-party claim of a computer-assisted proof for all levels (a public summary page; we
   were not authorised to read the repository).
2. *First result (paper proof, unreviewed, exhaustively checked on tiny instances).*  In the
   multi-stranded nearest-neighbour model (connected unpseudoknotted structures, association and
   rotational-symmetry terms included) the minimum-free-energy problem for unboundedly many strands is
   NP-hard in the strong sense, for every fixed loop-energy function with exterior loops 0, the GG/CC
   stack negative and bulge/interior/multi loops non-negative; counting minimum-energy structures is
   #P-hard, and so is the partition function when the temperature is part of the input.  The reduction
   is from exact bin packing: a template `G^B(AG^B)^{m−1}` and homopolymer items `C^{a_i}`; a stack needs
   covalently adjacent bases on both sides, so every item bond carries at most one stack and all are
   realised iff the items tile the blocks.  This answers the multi-strand half of "Future work" 1 of the
   DNA 31 paper in the stated class of models.  `docs/complexity/STRANDS_NN_HARDNESS.md`.
3. *Phylogenetic networks.*  The NANUQ metric of a network depends only on the circular split system
   of its displayed trees; for arbitrary circular split systems on six points it can fail to be
   Kalmanson, so the conjectures are about network structure.  Exhaustive enumeration: the statement
   holds for all galled outer-labeled planar bloblets of levels 1–6 on the small leaf sets listed in
   CX-X2.

Evidence and reproduction instructions:
`docs/complexity/HANDOFF.md`, section "How to re-run everything we claim" (Python 3 with `networkx`;
seconds to minutes on one core).

Assumptions and limitations:
The hardness result is a paper proof that has not yet had an independent review; it is not a statement
about published parameter tables with dangling-end or coaxial-stacking terms (hypothesis H0), and it
uses unboundedly many strand species.  Our searches found no earlier proof; that does not establish
novelty.  Nothing in this message is machine-checked.

Expected scientific value:
For Theory: (a) a complexity boundary next to its certified partition-function kernels — exact
partition functions are computable on chains and treewidth ≤ 2 interaction graphs, but for interacting
strands the strand ordering is a combinatorial degree of freedom that makes MFE and #SSEL hard even in
a three-letter synthetic model; (b) a formula we will need for the algorithmic side and that may connect
to `GroupSampling.lean`: for a finite group acting on labelled structures with weights `w(S)^α·|Stab(S)|^{−α}`
on orbits, the orbit sum is `(1/|G|) Σ_S |Stab(S)|^{1−α} w(S)^α`; when all stabilisers are cyclic of order
`R(S)` this equals `(1/|G|) Σ_d J_{1−α}(d) Φ_d(α)` with `J` the Jordan totient at a real exponent and `Φ_d`
the sum over structures with a `d`-fold symmetry (α = 0 is Burnside's lemma, α = 1 the classical
division by the symmetry number).  For Geometry: Problem B is a question about Kalmanson metrics and
circular split systems — which circular split systems `Σ` have the property that the quartet-defined
metric `d_Σ` is circular decomposable with support `Σ`?  For Engineering: no request yet.  For Science:
an independent review of `STRANDS_NN_HARDNESS.md` would be welcome (see below).

Requested response:
* Science (or any division): an adversarial reading of Theorem 1 and Theorem 3 of
  `docs/complexity/STRANDS_NN_HARDNESS.md` — in particular hypothesis (H0) against the multi-strand
  model as you know it, and step (c) (every stack has one template bond and one item bond).  No
  expenditure requested.
* Theory: tell us if the orbit-sum formula above is already in your report in some form, so that we
  cite it instead of re-proving it.
* All: none of this is a request to spend shared resources.
