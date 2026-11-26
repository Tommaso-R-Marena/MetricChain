# Research log (complexity division)

## 2026-11-26 — session 1

**Setup.**  Branch `research/biological-complexity` created from the theory checkpoint `a844b5a` and
pushed.  Other branches at that moment: theory `a844b5a8`, science `2b4ccdf7`, engineering `88feab94`;
`research/ensemble-identifiability` and `research/geometric-inference` did not exist yet.

**Reading.**  README, collaboration protocol, theory report headings; the two starting papers in full
(DNA 31 hardness paper; Holtgrefe et al.).

**Status verification (the brief asked for it; it changed the plan).**
* A2 (magnifiability of the NN model) was solved three days ago by Shalaby–Woods (arXiv:2611.27945v2).
  Our own sketch of the same idea is not claimed (CX-D1).  That preprint poses new questions (A5–A7).
* B1/B2 (NANUQ circular decomposability beyond level-2 bloblets) carry an unreviewed third-party claim
  of a computer-assisted all-level proof (vibemathed.com entry of 30 Sep 2026).  Its repository could
  not be read from this session (attach request denied); only the public summary was read.

**Problem B, first computations.**
* Observation: `d_N` depends only on `Σ = Split(T(N))` (a 4-set displays `ab|cd` iff a displayed split
  separates `ab` from `cd`).  So the conjectures are statements about a family of circular split systems.
* Exhaustive: all circular split systems on ≤ 6 points; all tree-generated ones on ≤ 7 points.  The
  statement fails outside the network family (CX-D2).
* Structure: a galled outer-labeled planar bloblet with `k` hybrids on `n` leaves is a binary tree on
  `n + k` circularly ordered positions with `k` disjoint adjacent pairs merged into hybrids (derivation
  in the log below); generator `experiments/complexity/nanuq/networks.py`.
* Exhaustive: levels 1–6 on small leaf sets, all pass (CX-X2).  The number of distinct displayed split
  systems on `n` labelled leaves stabilises in the level: 1, 6, 34, 203 for `n = 4,…,7` (levels ≥ 3).
* Structural lemma (to be written up and checked): every edge `e` of the backbone tree `T0*` has at
  most two straddling hybrids, one per adjacent face, so the displayed splits are
  `⋃_e P_e × Q_e` with `P_e`, `Q_e` a gap or the two gaps flanking a hybrid leaf.

**Problem A.**
* A6: Boehmer et al. (WABI 2024) already have the subset dynamic programme (`3^m n³`) and an XP
  algorithm in the number of distinct strands, both for MFE in a base-pair model without the symmetry
  term.  What is open is the NN model with symmetry and magnification.  Plan: generalised Burnside
  formula `Q_α = (1/Π n_i!) Σ_{d | gcd} J_{1−α}(d) Φ_d(α)` (`J` = Jordan totient with real exponent,
  `Φ_d` = magnified sum over labelled structures with a `d`-fold symmetry) + slice DP over
  sub-multisets + subset/multiset convolution.  Not started.
* **A1: a reduction found and checked.**  Exact bin packing → multi-strand NN MFE with a template
  `G^B(AG^B)^{m−1}` and items `C^{a_i}`: a stack needs covalently adjacent bases on both sides, so every
  item bond can carry at most one stack and all `Σ(a_i−1)` are realised iff the items tile the blocks.
  Works for every NN energy function with exterior loops 0, `GG/CC` stack negative, other loops
  non-negative; connectedness and `R = 1` come for free from the template.  Counting version gives
  #P-hardness of #SSEL and (temperature as input) of PF.  Exhaustive check on tiny instances passes.
  Written up in `STRANDS_NN_HARDNESS.md`.  Elementary; the open question is whether it is really new —
  two extended web searches found no proof of NN hardness for many strands, and the Nov 2026 preprint
  of the question's authors still lists the unbounded-strand hardness results as BPM-only.

**Tooling.**  `experiments/complexity/strands/ref_enum.py`: exhaustive enumerator of multi-strand
unpseudoknotted structures with loop decomposition (ground truth for everything in Problem A).

### Resume here

1. Commission an adversarial review of `STRANDS_NN_HARDNESS.md` (COMPLEXITY-REV-0001); fix what it finds.
2. A1 follow-ups: (i) ETH chain for CX-C1 (find a linear reduction 3SAT → 3DM → 4-PARTITION with
   polynomially bounded numbers, or cite one); (ii) robustness of the reduction to non-zero exterior-loop
   energies; (iii) Lean formalisation of the counting core of Theorem 1.
3. A6: implement the sub-multiset DP for the magnified NN partition function with symmetry, validate
   against `ref_enum.py`, write the theorem.
4. B: write the structural lemma; enumerate all galled planar networks (multi-blob) on ≤ 6 leaves; try
   the local (six-point) positivity argument; test non-galled planar networks.
5. A3′ (fixed-temperature #P-hardness): no approach yet beyond "probe strands" (see session notes in
   the working paper to come).
