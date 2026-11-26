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

* **Both reviews processed** (2026-11-26 21:26 UTC).  REV-0004: Lemma 0 completed; Theorem 11(c) restated (seven-leaf
  witness recomputed); Ising note: wrong ℓ1-rigidity sentence corrected, Laurent–Poljak and Tropp read and
  cited, the referee's `2^K` algorithm implemented exactly, singleton family.  While reading Laurent–Poljak's
  kernel description of elliptope faces I noticed that our Proposition 5 has an exact converse at degree 2:
  the projector energy `x^T(I − Π_L)x` exposes `V` iff the span has no other sign vector (Proposition 13);
  with the referee's reduction this makes the degree-2 variant co-NP-complete (Theorem 14).  A guess recorded
  because the simulation refuted it: I expected "no other sign vector in the span" to be typical for random
  states with `K ≪ n`; at `n = 12–16` it fails in 12–85 % of the cases (triples `±x^a ± x^b ± x^c`), in line with
  the bound but not with the intuition.  REV-0003: the journal version of Boehmer et al. read and cited —
  our novelty paragraph was wrong; Proposition 5 (MFE per symmetry class) written, implemented and tested;
  the `(min,+)` remark withdrawn; implementation edges fixed.
* Fourth checkpoint COMPLEXITY-MSG-0004 (six linked corrections; five new statements); COMPLEXITY-RES-0008 to
  the Ensemble division.  SCI-RES-0034 read: two sentences of the penalty note corrected.

## Session 1, continued — the fifth review; two directives; chain geometry and a near miss (2026-11-26 23:09 UTC)

* **Two supplementary directives from the research owner.**  About 22:02 UTC: a seventh division (Structural &
  Computational Biology) and seven tasks on algorithmic feasibility — answered first by COMPLEXITY-MSG-0005 (written
  before their branch existed).  About 22:40 UTC: an eighth division (Frontier Benchmarking); our copy of the
  collaboration protocol (`docs/collaboration/README.md`) now names all eight.  Recorded in `HANDOFF.md`,
  "Directives in force".
* **NANUQ beyond level 2.**  Blob-locality holds at every level (`NANUQ_HIGHER_LEVELS.md`, Theorem A: a six-leaf
  restriction that is not 6-locally good comes from six positions of one blob; the weight of a split that cuts a
  blob is a quadratic polynomial in the sizes of the positions).  Survey of six-leaf outer-labeled planar
  networks by hybrid insertion: with at most three hybrid nodes exactly 114 of the 150 tree-generated systems
  occur — the 108 of `𝒞_6` and the six images of "all but one 2-split"; no system with a negative weight or a
  wrong support beyond these.  Four hybrid nodes: running.
* **Chain geometry (CX-T32, CX-T33).**  The directive asks for tractability of articulated systems, and the
  Geometry division's C1 was only half answered.  Found: an orthogonality gadget (two auxiliary spins with
  couplings `3Λ, ±4Λ` give `Λ(|3p+4q| + |3p−4q|) ≤ Λ(10 − t²)`), hence a reduction from Max-Cut to the Heisenberg
  ground-state problem in `ℝ^3` with an exact optimum; fixed bond angles do not help (every `m`-th bond is free);
  short-range data are tractable by dynamic programming over torsions.
* **A near miss, recorded in full.**  A search then showed that the hardness of linear optimisation over the
  rank-constrained elliptope was called "believed" in 2012 and that Lovász conjectured NP-hardness of vector
  Max-Cut in every dimension, proved for dimension 3 only in 2024 (Kallaugher et al.).  Thinking about
  antiferromagnetic couplings only, I found the triangle with multiplicities 3, 4, 5 (a right angle), the blow-up
  argument and an exact lifting `OPT_{k+1}(H') = 25nL + 9·OPT_k(H)` — a proof for every dimension on unweighted
  graphs — and for about an hour took it for a proof of the open cases of the conjecture.  One more search, with
  the name "vector Max-Cut", found Piddock's preprint of October 2025, which proves the statement for every
  dimension with hardness of approximation.  Nothing had been written into the repository.  The note presents
  the statement as known and the two proofs as self-contained derivations.  **This is the third time today that
  a search after a proof changed its status; the search has to come first, and it has to use the classical name
  of the problem, not ours.**
* **COMPLEXITY-REV-0005** (22:43 UTC): no stated theorem false; Theorem 12 survived the referee's own code on 1.4
  million explicit networks.  Five attribution findings: Proposition 13 of the Ising note is Laurent–Poljak in
  two lines; Proposition 13′ is a weak form of Odlyzko (1988), which also answers "up to which `K`" (every
  `K ≤ n − 1`, with Irmatov 2024); the dichotomy of Lemma C is Huber et al. (arXiv:2408.12997, Lemma 4.2);
  Theorem 6 of Boehmer et al. is not about the base-pair model, and they call the Turner extension free of
  algorithmic challenges.  One narrowing: Corollary 14(v) is about the induced circular order.  All processed
  the same hour (dispositions in the file); three citations re-checked by a page-reading agent.
* **GEOMETRY-RES-0006 read** (the planted model for C2: a planted MinRank problem for rank 3 along a chain).
  Answered in COMPLEXITY-RES-0009 together with C1: corrections of what they quote from us, the dimension-one
  random case (Odlyzko), a caution on low-degree analyses of noiseless problems (lattice methods), the worst
  case for dimension 3 is open.  Not taken up.

* **Theorem 12′ (23:15 UTC), in answer to finding 1 of REV-0005.**  The referee had found no circular order in 270
  instances but no proof.  Idea: a Kalmanson order must make the strictly largest pair sum of every four leaves
  the crossing one, and by the four-point identity `d(p,r)+d(q,s) − d(p,q) − d(r,s) = 2w(pq|rs)` the signs of the
  quartet weights are read off from the split weights.  With `B_1`, `C_c` the two leaves next to the block of `x`- and
  `y`-leaves, only `S*` separates `{Y,X_1}` from `{B_1,C_c}`, so that four-set has the "wrong" largest sum; a leaf `Z` at a
  middle position gives two four-sets with the "right" one, and the three are incompatible.  Checked on 120 838
  choices of the five leaves (blow-ups) and on 1 400 explicit networks; the first version of the check had the
  unit wrong by a factor two (the note's `α` is twice the split weight), which the first run caught.  CX-T34,
  unreviewed.  Corollary 14(v) is "for some circular order" again.

* **The two new divisions published** (structural biology `1756529`, frontier `60a71d1`, both read at 23:36 UTC).
  Structural biology has working software (certified global minimum of a fixed-backbone rotamer model on six
  structures; a first certified enclosure of `ln Z`) and an open question copied to us (Q-5: a certified
  second-order bound for many weak pair terms on a correlated reference, or a proof that certificates must lose
  first order).  Answered in both directions (`CERTIFIED_BRACKETS.md`, COMPLEXITY-RES-0010): the martingale bound with
  an influence matrix computable by elimination exists; on toy models (exhaustive enumeration) its naive form is
  no better than the trivial bound, exact ranges gain a factor 6–9 and remain 2–6 times above the truth; and no
  certificate format can stay within a constant fraction of first order on all instances unless NP = co-NP.  A
  first version of the test flagged "violations" that were my own wrong expectation (that the influence form is
  always the smaller bound); it is not, and that is now the main caveat sent.  Frontier: C-1 (tightness of the
  basic relaxation), C-2 (threshold `K = n` by Odlyzko), C-3 (open); corrections to their intake record of us.
* **Six-leaf survey, four hybrid nodes** (90 minutes): 1 846 320 classes, still the same 114 systems.
* **Fifth checkpoint COMPLEXITY-MSG-0006** (2026-11-26 23:49 UTC): seven linked corrections, four new statements.  A sixth internal
  review (Theorem 12′, chain note, higher-levels note, penalty note) was started at 23:36 UTC on commit `307654f`.

### Resume here

1. *(done)* All five internal reviews are processed; dispositions in the five `COMPLEXITY-REV` files; the
   referees' programs are in `experiments/complexity/reviews/`.
2. *(done)* Fifth checkpoint COMPLEXITY-MSG-0006 published; survey written up (CX-T31, CX-X3).
3. **A sixth internal review is running** (started 23:36 UTC on commit `307654f`; task output arrives as a hand-back
   message; scratch directory `…/scratchpad/review6/`): Theorem 12′ (CX-T34), `CHAIN_GEOMETRY_HARDNESS.md`,
   `NANUQ_HIGHER_LEVELS.md`, `PENALTY_THRESHOLD.md`.  **Do not start a second one; do not edit those four files
   until it reports.**  Then: `COMPLEXITY-REV-0006.md` verbatim, the referee's programs to
   `experiments/complexity/reviews/rev6_…/`, a disposition for every finding, registers, a linked correction if
   anything sent to another division changes.  `CERTIFIED_BRACKETS.md` (CX-T35, T36) is not in that review.
4. **Open question with evidence** (`NANUQ_HIGHER_LEVELS.md` §2.3): is every six-leaf system displayed by an
   outer-labeled planar network, of any level, one of the 114?  A proof would make the robust criterion of
   Corollary 14 a theorem for every level.  Eight dihedral classes would have to be excluded (listed there);
   the mechanism to exploit is that the trees of a network are connected by single switchings.
5. **Other divisions.**  Structural biology and frontier: answered (COMPLEXITY-RES-0010); both have documents about
   us that we have only partly read (`docs/structural_biology/intake/C_complexity.md`,
   `THEOREM_TO_SOFTWARE_REGISTER.md`; `docs/frontier_benchmarks/RESEARCH_INTAKE.md`) — read them and correct what
   is wrong.  ENSEMBLE-MSG-0008 names us (data not linear in the ensemble): not read.  Geometry: C2 /
   GEOMETRY-RES-0006 §6 (low-degree hardness of recovery; worst case for dimension 3) — not started.  Theory:
   THY-MSG-0017 §5 item 1 still unanswered.
6. E-C1 for `K` in the input: "polynomial for `K = O(log n)`, open beyond".  A hardness proof has to make the
   diagonal-combination condition of Theorem 6 hard; the span condition alone cannot do it (Theorem 14(c)).
7. A3′ (fixed-temperature #P-hardness of the partition function): no approach yet.  W[1]-hardness in the number of
   species (C2 of `OPEN_PROBLEMS.md`).  NANUQ: generators of level 3 that are not galled; whether a network that
   violates Corollary 14(i) has a blow-up that is Kalmanson for no circular order (270 instances say yes).
8. **Before any novelty statement:** search under the classical name of the nearest known problem, and read the
   journal version of every source (`ASSUMPTION_AUDIT.md` §6, the rule adopted after REV-0005).
