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

## Session 1, continued — reviews, corrections, a collaborator's question (2026-11-26 19:01 UTC)

**Three reviews.**  Two internal adversarial referees (separate agents, own code, no access to our
reasoning) and the science division's independent referee.  No theorem was broken.  What they found, and
what it taught:
* The hardness note oversold its hypotheses ("the sign pattern of every physical parameter set" — false)
  and undersold its robustness ("coaxial stacking breaks it" — false in general).  Both referees
  independently proposed the same repair, (H2′); the internal referee's sketch for coaxial stacking became
  Theorem 1c after we found the count over separators (`m − 1 ≤ L + r + z`); the science referee's dangle
  statement became Theorem 1d.  The lesson for the next result: state the hypothesis the proof uses, not
  the one that sounds physical, and test the boundary of each hypothesis with control models from the start.
* The ETH corollary cited a bound through a citation; the source does not state it in the needed form.
  Writing the chain out (local garbage collection in Garey–Johnson's 3DM reduction; their 4-PARTITION sizes)
  took an hour and removed the dependence.
* The NANUQ note's all-level theorem is probably a rediscovery (122 = 1+3+16+102).  Its "direct tests" were
  circular.  The referee's explicit-network generator is now the independent evidence.
* A Lean file for the finite inputs of the NANUQ note caught an error in a hand-typed list before it
  mattered (`DEAD_ENDS.md` CX-D7).

**E-C1 (Ensemble division).**  "Are `K` sign vectors exactly the ground states of some Ising pair energy —
co-NP-hard for `K ≥ 4`?"  Twins (sites with equal or opposite columns) can be merged without changing the
answer, in both directions; so for fixed `K` it is a finite table.  `K = 4`: unless the product is constant.
For `K` in the input we have structure but no hardness proof (`DEAD_ENDS.md` CX-D6): the cleanest statement
is that with a pair-separating sign symmetry "exposed" means "no other sign vector in the span", and for
characters this is the Sidon property.

**Questions of the theory and science divisions on penalised models (2026-11-26 19:39 UTC).**  The floor's gain
`ln⟨e^{λΣγ}⟩` for a product reference is bracketed by the first term of the polymer expansion in the tables
(`ln(1+W) ≤ gain ≤ W`), which on toy models is exact to three or four digits up to the transition; the
threshold is a densest-sub-hypergraph ratio (max-flow); "has the floor left its reference?" is NP-hard for
general pair tables (MAX-CUT) and polynomial for product or exponentially decaying tables.  A first attempt —
bounding `G` by site prices — was valid and numerically worse than the Finner bound the theory division already
had; the lesson was to keep the product structure `Π(1+f_U)` instead of bounding the exponent.
`PENALTY_THRESHOLD.md`.

**Hardness note, after the reviews.**  Theorem 1e (coaxial stacking up to the stack energy together with
dangles) by the same accounting as 1c/1d: `E − E** = (|σ|−|x|)j + |x|L + P + Dng − (m−1)e_A` with `j ≥ u`,
`L ≥ u − β`.  The term `|x|/B` in its hypothesis is probably an artefact.  Lean: the arithmetic of the
4-PARTITION reduction (`FourPartition.lean`); the 24 permutation cases are handled uniformly by naming the
witnesses through selector functions before the case split.

## Session 1, continued — two more reviews; NANUQ: the sharp class and level 2 (2026-11-26 20:38 UTC)

* **NANUQ, "Kalmanson" alone (CX-T26).**  Started from the item "is the criterion sharp for Kalmanson alone?".
  Counting the six-point systems with all six-leaf terms non-negative gave 133 (not 127); the six extra
  systems are those that only give weight to an undisplayed split.  Rewriting Lemma 5 in terms of the
  six-point restriction gave Corollary 5′: `Φ6 < 0` iff the three 3-splits are present and the 2-split
  `{z,w}` is absent.  With that, closure under substitution is two lines, and blowing up `z`, `w` into clades
  of `m` leaves gives weight `2Φ4 + 2m(Φ5+Φ5) − m²` (pairs inside a clade contribute 0).  The 17 minimal
  failing blow-ups are Kalmanson for no circular order (backtracking search).  §7.1 of the note.
* **NANUQ, level 2 completely (CX-T27).**  The seven-leaf counterexample contains the forbidden pattern in
  five of its six-leaf subnetworks, which suggested classifying by the pattern.  A blob with two hybrid nodes
  is a theta graph; orienting it gives exactly two kinds, galled and *nested*; planarity empties one path.
  The nested blob is a three-parameter family `N[k_B,k_1,k_2]` with four trees.  Tables showed that only one
  split ever fails, with weight `k_1 + k_2 − C(k_B−1,2)` (resp. `k_1 + 1 − C(k_B−2,2)`), **not monotone** in the
  numbers of leaves: `N[4,1,1]` fails, `N[4,1,2]` has weight 0, `N[4,1,3]` is fine.  With pendant subnetworks the
  weight is `β_1G + ξ_1R − e_2(middle sizes)`; derived from Proposition 2 with a table of local terms by type
  of leaf, and tested on explicit rooted networks with the independent calculator (`level2_explicit.py`).
  The proof needs two finite facts on six points (624 substitutions; restrictions of the family) and
  Corollary 5′.  §7.2 of the note.  A first guess recorded here because it was wrong: I expected the
  pattern-free condition (`k_B ≤ 2`, or `k_B = 3` and no `c`-position) to be the answer for bloblets; it is
  only the answer for the robust question (Corollary 14).
* **COMPLEXITY-REV-0003 received** (algorithm note, hardness additions): no theorem broken.  Major: the
  novelty paragraph of the algorithm note is wrong as worded — the journal version of Boehmer et al. (2025)
  has the base-pair-model partition function over all orderings with rotational symmetry; we had read the
  conference version only.  Major: the minimum-free-energy clause of Theorem 1 is unproved.
* **COMPLEXITY-REV-0004 received** (Ising note, NANUQ additions): no false theorem.  Major: the ℓ1-rigidity
  reformulation in §6 of the Ising note is wrong; Corollary 7 and Proposition 5 are published
  (Laurent–Poljak 1995/96); a `2^K·poly(n)` algorithm follows from our own Proposition 5 and was overlooked;
  Lemma 0 of the NANUQ note has an unproved step.
* Both reports are saved verbatim; register rows carry notices; **dispositions are pending** (next item).

### Resume here

1. **Process COMPLEXITY-REV-0003 and -0004 in full** (task list in the two files' headers; the referees'
   working directories are `scratchpad/review3`, `scratchpad/review4` of the session — copy the programs to
   `experiments/complexity/reviews/rev3_strands/`, `rev4_ising_nanuq/`).  Order: (a) Lemma 0 gap (the new
   §7.2 depends on it); (b) the wrong sentence and the prior art in the Ising note, the `2^K` algorithm, and a
   linked correction to COMPLEXITY-RES-0003 for the Ensemble division; (c) the novelty paragraph and the MFE
   clause of the algorithm note; (d) the minor findings.
2. Have §7.1 and §7.2 of the NANUQ note reviewed (never seen by a referee); a Lean check of Corollary 5′ on
   six points and of the two finite facts of Theorem 12, Step 1, would be cheap.
3. E-C1 for `K` in the input: now "polynomial for `K = O(log n)`, open beyond"; the referee could not decide
   hardness either.  Read Laurent–Poljak and Deza–Laurent before any further attempt.
4. A3′ (fixed-temperature #P-hardness of the partition function): no approach yet.
5. Hardness note: read Lyngsø (2004) and Shalaby–Woods §7; W[1]-hardness in the number of species (C2).
6. NANUQ: level 3 blobs that are not galled (list the generators, as in Lemma C); Lean: define the closure
   inside Lean so that the list `C6` is no longer imported.
7. Unanswered mail: SCI-RES-0031 §1 (numbers for Q-CX3, not yet read); theory's THY-MSG-0017 §5 item 1;
   R20-CX-G.
