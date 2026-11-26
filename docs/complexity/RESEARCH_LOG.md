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

**Problem B, the same day: a local-to-global proof, and a counterexample without "galled".**
* Decomposition: for a non-trivial split, `α/2 = Φ4 + Σ_z Φ5(z) + Σ_{z,w} Φ6(z,w)`, each term a function of
  the displayed quartets on at most six leaves (for trivial splits `α/2 = n − 2 + ΣΨ`).  The 5-point terms
  are non-negative for *every* tree-generated system.  So everything hinges on `Φ6`.
* `Φ6 < 0` iff a "union property" fails (Lemma 5).  For planar trees with twin leaves (class 𝒜 — exactly
  the galled planar networks whose hybrids have leaf children) the union property has a five-line proof:
  all displayed trees are restrictions of ONE tree with independent choices, and two edges of a tree
  whose sides meet and miss a common leaf are nested.
* General galled planar networks are substitutions of 𝒜-systems; restrictions of substitutions are
  substitutions of restrictions; on six leaves the closure has 108 systems, all satisfying the criterion.
  Hence the theorem for all levels and any number of blobs (`NANUQ_LOCAL_CRITERION.md`).
* Looking at which six-point systems violate the criterion while being fine on their own (14 of them),
  one — all nine splits except one 2-split — turned out to be displayed by a level-2 planar network that
  is NOT galled.  Doubling leaves makes the negative `Φ6` terms win: a 7-leaf non-galled level-2 bloblet
  whose NANUQ metric is not Kalmanson for any circular order (checked from the explicit DAG by a second
  program).  So "galled" is necessary — a question the paper does not raise and the third-party summary
  does not mention.
* Sharpness: 150 tree-generated / 141 globally good / 127 locally good / 108 network systems on six
  points; every excluded system fails after a small blow-up.
* A first attempt to explain the level-2 theorem by a single correlated measure on hybrid choices
  (so that `d_N` would be an average of tree metrics) cannot work: for the level-2 bloblet the required
  probabilities sum to 3/2 (three quarnets each need probability ½ on mutually exclusive choice patterns).

**Problem A6: done as a validated paper proof.**  `Q_α = (1/c) Σ_{d|gcd} J_{1−α}(d) F_d`; `F_1` by a
dynamic programme over sub-multisets of species; `F_d` by a bijection (designated nest containing the
marked nick, top segment) that counts every symmetric structure of every rooted period once; tables at
magnification `dα`.  The first implementation agreed with exhaustive enumeration on all 280 test systems
(exact rationals, `α = 0..3`, symmetric structures of orders 2–6).  `STRANDS_ALGORITHM.md`.  Remaining
doubt: the decoding of MFE/#SSEL from `Q_α` is cited from [SW26], not checked.

**Problem B3 (parametric family): settled for the class of the paper.**  With `ρ_xy ∈ {ρ_c,ρ_s,ρ_a,ρ_o}`
every local term is a linear form in `ρ`; only eleven forms occur on `𝒞_{≤6}`; those of undisplayed splits
vanish identically.  Sufficiency = all forms non-negative; necessity = blow up a pair of non-hybrid leaves
carrying the form (weight `2m²F(ρ) + O(m)`), plus sunlets and the 4-cycle.  Result: `ρ_o = ρ_s`,
`ρ_c + ρ_s ≤ 2ρ_a < 2ρ_s`.  The Modified NANUQ distance of NANUQ⁺ fails on a level-1 network with a cherry
below the hybrid (checked from the explicit DAG, all 2520 orders).  A first version of the trivial-split
formula omitted the 4-sets through the three leaves `a,u,b` (they contribute 0 for NANUQ but not in
general); the identity check caught it.

### Resume here

1. Commission an adversarial review of `STRANDS_NN_HARDNESS.md` (COMPLEXITY-REV-0001); fix what it finds.
2. A1 follow-ups: (i) ETH chain: now CX-T14, conditional on two citations to be verified at the source (was: find a linear reduction 3SAT → 3DM → 4-PARTITION with
   polynomially bounded numbers, or cite one); (ii) robustness of the reduction to non-zero exterior-loop
   energies; (iii) Lean formalisation of the counting core of Theorem 1.
3. A6: adversarial review of `STRANDS_ALGORITHM.md` (COMPLEXITY-REV-0003); optionally fast subset
   convolution; read [SW26] §7 properly before relying on the MFE/#SSEL corollary.
4. B: (i) adversarial review of `NANUQ_LOCAL_CRITERION.md` (COMPLEXITY-REV-0002), in particular Lemma A,
   Lemma B and the completeness of the enumeration of `𝒜_6`; (ii) Lean: the finite check of Lemma 8 and
   Theorem 4 as an abstract statement; (iii) B3, the parametric family — read NANUQ⁺ first; (iv) which
   non-galled planar networks still satisfy the criterion?
5. A3′ (fixed-temperature #P-hardness): no approach yet beyond "probe strands" (see session notes in
   the working paper to come).
