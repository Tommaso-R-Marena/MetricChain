# Consolidation report — Mathematical Biology and Computational Complexity Division

Branch `research/biological-complexity`.  Written 2026-11-27 under the research owner's directive "Controlled
Consolidation and Temporary Research Halt".  One session, 26–27 November 2026, 46 commits before this report.
Everything cited is on this branch; commands to re-run every claim are in `docs/complexity/HANDOFF.md`; the
register of statements with labels and review state is `docs/complexity/THEOREMS.md`.

**Reading rule.**  "Reviewed" below means reviewed by AI referee agents commissioned inside this programme (six
reports, `COMPLEXITY-REV-0001` … `-0006`, verbatim in `docs/collaboration/messages/complexity/`, plus the science
division's `SCI-REV-0019`).  **No result of this division has been seen by an external human expert.**  "No source
found" means that our searches and the referees' found none; it is not evidence of novelty.

## A. Executive assessment

What the division did, in defensible terms:

1. **It proved that folding many interacting nucleic-acid strands is NP-hard in the nearest-neighbour energy
   model** — the model with stacking energies that the field uses, not only the base-pair-counting models for
   which hardness was in print — for every fixed energy function in a class given by two sign conditions, and
   it located the source of the hardness: the number of *different* strands, not the number of strands.  This
   answers, for that class, a question two recent papers list as open.  It has survived three internal reviews,
   one of them by another division.
2. **For a published problem on phylogenetic networks** (when is the NANUQ quartet metric circular
   decomposable?) it found the local mechanism, showed by a seven-leaf counterexample that the hypothesis
   "galled" in the source paper's conjecture is necessary, and classified the outer-labeled planar networks of
   level at most 2 completely, with an explicit formula for the one weight that can go wrong.  The part of this
   that coincides with the source paper's conjecture (galled networks) is, in all likelihood, a rediscovery of
   an unreviewed third-party claim we could not read.
3. **It wrote out and tested an exact algorithm** for the partition function of interacting strands over all
   strand orderings with rotational symmetry — an extension of a published scheme that its originators call
   routine.
4. **It answered complexity questions of five other divisions.**  After review, most of these answers are
   correct assemblies of known mathematics with corrected attributions; a few statements in them have no source
   that anyone here found.

What it did not do.  It produced no computational-biology capability and no evidence about any molecule.  Its
results are worst-case classifications, counterexamples and exact small-scale reference code.  Both problems
the founding brief named had moved before work began (one solved elsewhere, one claimed elsewhere).  **Three
times in one day an internal review or a late search showed that something we had called ours was known** —
the partition function over all orderings (base-pair model), the degree-2 criterion and the random-state bound
for Ising ground sets, the hardness of the chain problem.  In six reviews no theorem with a written proof was
found false.  But the sixth review, of the notes written in the last hours, found one corollary false as
written (a dropped qualifier), one summary sentence asserting a direction that is not proved, and one accuracy
claim that its citation — made from memory — does not cover (§G).  The novelty statements were wrong
repeatedly, and the ones that remain should be read with that record in mind.

## B. Strongest contributions, ranked

Four deserve inclusion.  Nothing else does: the chain note, the certified-brackets note and the penalty note
assemble known results for other divisions; blob-locality is a re-reading of two steps of an existing proof,
and the six-leaf survey is evidence, not a classification.

### B1. Multi-strand folding in the nearest-neighbour model is strongly NP-hard; the hard parameter is the number of species

* **Contribution.**  In the multi-stranded unpseudoknotted nearest-neighbour model in the formal sense of the
  DNA 31 paper (connected structures; association and rotational-symmetry terms; a loop with a nick is an
  exterior loop of energy 0), for **every fixed** loop-energy function with (H1) a negative `GG/CC` stack and
  (H2′) bulge and interior loops between `G–C` pairs less favourable than the stacks they displace: deciding the
  minimum free energy is strongly NP-hard, already for one template strand and homopolymer item strands;
  counting minimum-energy structures is #P-hard; the partition function is #P-hard when the magnification
  (temperature) is part of the input; under ETH there is no `2^{o(c)}·poly(N)` algorithm in the number `c` of
  strands.  The statements persist with a reward for flush coaxial stacks, with dangles of total strength
  below the stack, with both under an explicit inequality, and for several complexes.  With B3: polynomial
  time for a bounded number of species, NP-hard for unboundedly many.
* **Where.**  `docs/complexity/STRANDS_NN_HARDNESS.md` (added `fc4b238`, last changed `680053a`); `THEOREMS.md`
  CX-T1–T4, T14, T15, T20, T24; programs `experiments/complexity/strands/test_partition_reduction*.py`,
  `test_generalised_hypotheses.py`, `test_eth_chain.py`; Lean `experiments/complexity/lean/StackPacking.lean`,
  `FourPartition.lean` (CX-V1, CX-V4).
* **Verification and review.**  Paper proofs.  Three internal reviews (REV-0001; SCI-REV-0019 by the science
  division, independent of the first; REV-0003 for the later theorems): no theorem broken; one hypothesis
  restated ((H2) → (H2′)), the framing corrected.  Lean covers the counting step of the packing argument and
  the arithmetic of the 4-PARTITION reduction only — not the model of secondary structures.
* **Essential assumptions.**  (H0) exterior loops have energy 0 — a property of the formal model, not of
  software that adds dangle and coaxial terms; (H1); (H2′).  Unboundedly many species.
* **Closest prior art.**  Condon, Hajiaghayi, Thachuk (DNA 27, 2021): APX-hardness for unboundedly many strands in
  the base-pair model.  Lyngsø (2004): the gadget, for one strand with pseudoknots in a stacking model.  The
  DNA 31 paper (doi 10.4230/LIPIcs.DNA.31.1): #P-hardness in the base-pair and stacking models, and the open
  question.  Boehmer, Berkemer, Will, Ponty (journal version, 2025), Theorem 6: NP-completeness for triplet
  repeats in a model with a base-pair reward, a multiloop penalty and an association reward.
* **Distinction.**  Energy functions with stacking terms, fixed, in a class defined by inequalities — including,
  on the loop types that occur, the five parameter files distributed with ViennaRNA (the first referee's
  computation, not repeated by us) — rather than base-pair counting or a model built for the reduction; strong
  NP-hardness with homopolymer strands; the counting and ETH statements.
* **For originality.**  The DNA 31 paper (2025) asks "Is MFE NP-hard for … NN O(n)-strands unpseudoknotted?";
  Shalaby and Woods (arXiv:2611.27945, 23 November 2026) still list the unbounded-strand hardness results as
  being "in the simpler base pair matching (BPM) model".  Three referees' searches found no proof for a
  nearest-neighbour model.
* **Against originality.**  The gadget is Lyngsø's, cut into strands; a specialist may regard the step as
  expected.  Boehmer et al.'s Theorem 6 is closer than the base-pair results and we know it only through a
  referee's reading.  The area is active (the preprint that still calls it open is days older than our note).
  Our record on novelty statements is poor (§C).
* **Validation.**  Exact enumeration of all structures on small instances (ours; the referees' own enumerators on
  about a thousand instances); Lean cores.
* **Limitations.**  Not a statement about published parameter tables "as implemented" (with dangles and coaxial
  stacking together beyond the inequality of Theorem 1e); nothing about the partition function at a fixed
  temperature; nothing about one strand with pseudoknots; worst case only.
* **Before publication.**  A human expert in nucleic-acid computation must check the reduction.  Read the
  journal version of Boehmer et al. and Lyngsø's paper ourselves.  State exactly which energy conventions of
  NUPACK and ViennaRNA satisfy the hypotheses.  Rewrite as a paper.

### B2. The NANUQ metric of outer-labeled planar networks: why it works, where it fails, and level 2 completely

* **Contribution.**  (i) The split weights of the NANUQ metric are sums of terms on at most six leaves, which
  gives a local criterion.  (ii) "Galled" cannot be dropped from the statement that the metric is circular
  decomposable with the displayed splits as support: an explicit outer-labeled planar level-2 network on seven
  leaves has a negative weight, and exact weights in a family.  (iii) The sharp classes of split systems: 127
  of the 150 tree-generated six-point systems for exact support, 133 for "Kalmanson" alone, the latter given by
  one forbidden six-leaf pattern.  (iv) **Level 2 completely:** in an outer-labeled planar network of level at
  most 2 the only weights that can have the wrong sign belong to one *critical split* per nested blob, with
  weight `β_1G + ξ_1R − Σβ_jβ_l` in the numbers of leaves at the positions; not monotone in the number of
  leaves.  (v) A negative critical weight excludes *every* circular order (Theorem 12′), so for level 2 the
  property is decided by these weights.
* **Where.**  `docs/complexity/NANUQ_LOCAL_CRITERION.md` (added `9a35d2f`; Theorem 12′ in `0cd9992`);
  CX-T5, T7, T8, T26, T27, T34; programs in `experiments/complexity/nanuq/`; Lean `NanuqFinite.lean`,
  `NanuqPattern.lean` (CX-V3, CX-V5: the finite facts on six points).
* **Verification and review.**  Paper proofs plus exact finite computations.  REV-0002, REV-0004, REV-0005: no
  false statement; the third referee tested (iv) with its own code, written from the definitions of the source
  paper, on about 1.4 million explicit networks, and caught four deliberately wrong variants of the formula.
  (v) was reviewed in REV-0006: every step re-derived, and an exact search over all circular orders on 25 620
  explicit networks with a negative critical weight (the referee's own code) found no Kalmanson order.  (v) is
  a short corollary of (iv) and exactly as reliable as (iv).
* **Essential assumptions.**  Binary semi-directed networks, outer-labeled planar; level at most 2 for (iv), (v).
* **Closest prior art.**  Holtgrefe, Allman, Baños, van Iersel, Moulton, Rhodes, Wicke (Bull. Math. Biol. 2025):
  the statement for level-2 bloblets and the question for larger classes of *galled* networks.  A third-party
  entry (vibemathed.com, 30 September 2026) claiming the statement for all galled networks, unreviewed, whose
  repository this session was not allowed to read.  Huber, van Iersel, Jones, Moulton, Veenema-Nipius
  (arXiv:2408.12997): the two kinds of blob with two hybrid nodes.
* **Distinction.**  Everything about networks that are *not* galled — the counterexample, the two sharp classes,
  the classification with its formula, the statement for all circular orders.  For galled networks of every
  level (our Theorem 7) we claim nothing: probable rediscovery.
* **For originality.**  No source on non-galled networks found by us or by two referees (some twenty queries);
  the MathWorld page on the NANUQ distance (updated 25 November 2026) mentions none.
* **Against originality.**  The third-party claim names a "six-label reduction" that we have not seen and that
  may contain our local criterion.  The published question is about galled networks, so (ii)–(v) answer a
  question that nobody posed in print; a specialist may find the level-2 case a natural exercise once the
  local criterion is known.
* **Validation.**  Exact integer computation; independent code of two referees; kernel checks of the six-point
  facts.
* **Limitations.**  The proof of (iv) rests on a computed table of local terms that no kernel checks (a referee
  reproduced it from explicit networks).  Nothing beyond level 2 except blob-locality and a survey
  (`NANUQ_HIGHER_LEVELS.md`; REV-0006 corrected two statements of it): six-leaf networks with up to four hybrid
  nodes display only 114 of the 150 systems in a search that is not exhaustive (it identifies networks by an
  invariant that is incomplete from three hybrid nodes on), and whether that holds at every level is open.  No connection to data: whether the
  failure matters for network inference from gene trees needs a coalescent simulation that nobody here ran.
* **Before publication.**  Read the third-party repository (needs the owner's authorisation) and delimit what
  remains; a specialist in mathematical phylogenetics must check the proofs of Theorem 12 and 12′.

### B3. Partition function, minimum free energy and level counts of interacting strands over all orderings, with symmetry

* **Contribution.**  For a multiset of strands in the nearest-neighbour model: the magnified partition function
  over all circular orderings, with indistinguishable strands and the rotational-symmetry correction, in
  `O(L_0⁴ Σ_d Π_i C(n_i/d + 2, 2))` operations — `3^c` instead of `(c−1)!` for distinct strands, polynomial for
  a bounded number of species — and, from the same tables, the minimum free energy and the number of
  structures at every energy level for every degree of symmetry (Möbius inversion and digit extraction).  A
  symmetry-blind `(min,+)` recursion is shown to be wrong.
* **Where.**  `docs/complexity/STRANDS_ALGORITHM.md` (added `e8824ed`, last changed `13b582b`); CX-T10–T12, T30;
  `experiments/complexity/strands/multiset_dp.py`, `level_counts.py`, tests; Lean `JordanOrbit.lean` (CX-V2, the
  orbit formula).
* **Review.**  REV-0003 and REV-0005: correct; exact agreement with exhaustive enumeration on 280 systems
  (ours) and about 740 runs with the referees' enumerators.
* **Closest prior art and distinction.**  Boehmer, Berkemer, Will, Ponty (Algorithms Mol. Biol. 21:4, 2025): the
  same scheme for the base-pair model (their Theorem 4), count-indexing for few species (Theorem 5), and the
  sentence that the extension to the Turner model "does not pose any algorithmic challenges".  Shalaby and
  Woods: the nearest-neighbour model for a fixed ordering, and the question (their "Future work" 3 and 4).
  **Ours is the extension written out, proved and tested — not the idea.**
* **For / against originality.**  For: the question is listed as open on 23 November 2026.  Against: the
  originators of the method call it routine; our first novelty paragraph was wrong.
* **Limitations.**  Unoptimised Python, validated for `N ≤ 16`; exterior loops without dangles or coaxial
  stacking; `L_0⁴` where `L_0³` may be possible; numbers of `O(N·E_max/ε)` bits.
* **Before use or publication.**  A comparison with an established implementation on small systems (§E1); as a
  paper it is at most a short note beside B1.

### B4. Recognising exact ground-state sets of pair energies (the Ensemble division's question)

* **Contribution.**  "Are `K` given spin configurations exactly the ground states of some pair energy?" depends
  only on the set of column types, so it is linear-time for fixed `K`; it is decidable in `2^{O(K)}·poly(n)`;
  a criterion in `K` dimensions; for sets of characters, a Sidon criterion; and the variant with a certificate
  of degree 2 is co-NP-complete, because "does the span of `K` sign vectors contain another sign vector?" is
  NP-complete (the fourth referee's reduction).  **The question itself for `K ≫ log n` is open.**
* **Where.**  `docs/complexity/ISING_GROUND_SETS.md` (added `21161f4`, last changed `13b582b`); CX-T16–T19, T25,
  T28, T29; `experiments/complexity/ising_faces/`.
* **Review.**  REV-0004, REV-0005: correct; **mostly known** — the object is the face lattice of the cut
  polytope; the sufficient conditions and the degree-2 criterion are Laurent–Poljak's, the random case is
  Odlyzko's (1988).  No source found for the `K`-dimensional criterion, the Sidon criterion, the singleton
  family as stated and the NP-completeness of the span problem, which a referee called "a routine
  Partition-style reduction".
* **Utility.**  Two independent exact programs for the same verdicts; a checkable certificate when it exists.
  ±1 spins and complete pair data only — it does not transfer to rotamer models as it stands.

## C. Negative results, rediscoveries, and what to drop

| what | status |
|---|---|
| "Is the nearest-neighbour model magnifiable?" (first candidate of the brief) | **solved elsewhere** before we began (Shalaby–Woods, 23 November 2026); `DEAD_ENDS.md` CX-D1 |
| NANUQ metric of all galled outer-labeled planar networks (second candidate) | **claimed elsewhere** (unreviewed third-party entry); our Theorem 7 is a probable rediscovery; CX-D5 |
| Partition function over all strand orderings | the scheme is Boehmer et al.'s; our first novelty paragraph was wrong (REV-0003), and wrong again in two details (REV-0005) |
| Degree-2 certificates ⇔ no other sign vector in the span; random states | Laurent–Poljak; Odlyzko 1988 — listed by us under "no source found" until REV-0005 |
| Hardness of optimising pair data over chain conformations | known (Kallaugher et al. 2024; Piddock 2025).  For an hour a second proof of ours looked like a proof of open cases of a conjecture of Lovász; a search under the classical name ended that before anything was committed (`PRIOR_ART.md` §D) |
| "Realizability of averaged chain data is NP-hard to accuracy `1/poly`" (sent to Geometry in COMPLEXITY-RES-0009) | **claimed on a citation from memory that gives only accuracy in binary** (REV-0006); the stronger form rests on a theorem (Liu 2007, via Gharibian 2010) that nobody here has read; restated as conditional |
| Fixed-angle chains | a literature exists that our search missed (Soss–Toussaint; Demaine–Eisenstat; Borcea–Streinu; found by the sixth referee from summaries).  It is not reported to contain our Theorem 3, but it shows the single-pair problem is polynomial: the hardness comes from many pairs with data of both signs, and the instances are unphysical |
| "The robust criterion holds at every level" (higher-levels note, first version) | **overstated** (REV-0006): one direction is proved only when subnetworks are included; the level-2 corollary was misquoted and false as written; both corrected |
| Co-NP-hardness of the Ensemble division's question | **failed**: the span condition is NP-hard but its instances are all exposed; symmetrisation destroys the solutions; two referees found nothing either (CX-D6) |
| "The NANUQ metric of every circular split system is circular decomposable" | false (33 systems on six points); CX-D2 |
| Seven sentences of our first versions | false or too broad, e.g. that the hypotheses are "the sign pattern of every physical parameter set" (false for a Turner-2004 bulge rule); CX-D4 |
| Certified second-order bounds for many weak pair terms | valid, and loose: 2–6 times the true excess on toy models; the influence-matrix form can be worse than the trivial bound (`CERTIFIED_BRACKETS.md`) |
| Six-leaf survey beyond level 2 | a survey, not a classification, and not exhaustive even at its own levels (incomplete invariant from three hybrid nodes on).  Four of the 36 systems that never occur are impossible for every network; for the other 32, neither connectivity of the displayed tree set nor any implication between displayed splits with up to three premises explains their absence |

**Deprioritise or abandon.**  (1) Further attempts on the hardness of the Ensemble division's question (E-C1 for
`K ≫ log n`): three parties failed; no new idea.  (2) #P-hardness of the partition function at a fixed
temperature: no approach; the standard thickening identities are not available for these models.  (3) The
NANUQ problem beyond level 2: mathematically clean, remote from the programme's objective.  (4) Any further
"self-contained proofs" of known hardness results.  (5) Novelty claims without a search under the classical
name of the problem and a reading of the journal version of the nearest source.

## D. Practical opportunities

Evidence levels: M = mathematical possibility; S = implemented software; V = validated on synthetic instances;
R = validated in a realistic computation; X = experimental evidence.  **Nothing of ours is at R or X.**

| opportunity | level | what exists | what is missing |
|---|---|---|---|
| A reference oracle for multi-strand thermodynamics: exact partition function, minimum free energy and level counts with the symmetry correction, for small systems with repeated strands | S, V | `multiset_dp.py`, `level_counts.py`; exact agreement with exhaustive enumeration on about a thousand small systems | alignment with the energy conventions of established software; a comparison with it; any performance work |
| Stress tests for heuristic multi-strand structure prediction: instance families with a planted optimum (exact packings) | M, V (small) | the families `I(a,m,B)` of the hardness note, enumerated for small sizes | a generator at realistic sizes with the conventions of a target program; a run |
| Guidance for certified computation on rotamer models (the Structural Biology division): which regime no certificate format can cover; closure without search = tightness of the basic linear relaxation, checkable in advance | M | `CERTIFIED_BRACKETS.md` (unreviewed; known mathematics), COMPLEXITY-RES-0010 | the two numbers on their instances (`max_i β·c_i`; the integrality gap); a certified second-order bound that is actually tight |
| Exact recognition and certificates for ground-state sets of ±1 pair models (the Ensemble division) | S, V | `span_algorithm.py`, `faces.py` | a `q`-state, sparse-graph analogue before it means anything for rotamers |
| What a chain-fitting routine can and cannot guarantee (Geometry, Structural Biology) | M | `CHAIN_GEOMETRY_HARDNESS.md`: hard also with fixed bond angles when many pairs carry data of both signs (a single end-to-end distance is polynomial); exponential only in the range of the data | the dynamic programme for short-range data is described, not implemented; the hard instances are artificial, so this is a statement about guarantees, not about typical data |

The honest summary for the programme's objective — new mathematics leading to better structural-biology
methods: this division's contribution is mostly *negative guidance* (what cannot be optimised or certified in
the worst case, and which parameter decides it) and one reference oracle in a neighbouring field.

## E. Recommended next actions (three)

**E1. Make the strand results externally defensible and test the reference algorithm against established
software.**
*Objective:* decide whether B1 (with B3) stands before a specialist, and whether B3 agrees with a mainstream
implementation.  *Prerequisites:* the two notes, the tested Python code, three internal reviews.  *Missing:* our
own reading of Boehmer et al. (journal version) and of Lyngsø; a precise statement of which conventions of
NUPACK and ViennaRNA meet (H0), (H1), (H2′); an adapter between our loop-energy interface and a published
parameter file.  *Baselines:* NUPACK (Dirks et al. 2007 and its current version), ViennaRNA's multi-strand
routines — named from the literature, not read by us.  *Benchmark:* partition function, minimum free energy and
symmetry corrections on small synthetic multisets including repeated strands (fixed sequences given by the
test, no design); and the hard families as a stress test of heuristic minimum-free-energy search.  *Success:*
agreement to numerical precision on all systems small enough for our code, every disagreement traced to a
documented convention; a specialist finds no error in the reduction.  *Failure:* an unexplained disagreement,
or the hardness statement found in print.  *Claude reasoning:* small to moderate, not estimated more precisely.
*Computation:* local CPU; no Modal.  *Dependencies:* Engineering (independent run), Frontier (design of the
comparison), Science (model conventions).  *Model:* Opus suffices for the adapter and the comparison; the final
check of the reduction should be a human's.

**E2. Settle the status of the NANUQ classification.**
*Objective:* know whether B2 is new and correct.  *Prerequisites:* the note, four reviews, the kernel-checked
six-point facts.  *Missing:* the content of the third-party repository (reading it needs the owner's
authorisation; one request was denied in this session); a specialist's reading of Theorems 12 and 12′.
*Baseline:* the theorem of Holtgrefe et al. for level-2 bloblets.  *Benchmark:* none — this is mathematics; a
simulation of whether the failure affects inferred splits graphs would need a coalescent model and is not
recommended now.  *Success:* the non-galled results are not in the third-party work and a specialist finds no
error.  *Failure:* either.  *Claude reasoning:* small.  *Computation:* none.  *Dependencies:* none.  *Model:* Opus
suffices for the reading.

**E3. Put the certification theory to work on the one piece of software that exists.**
*Objective:* decide whether certified enclosures of `ln Z` (and populations) are attainable for the Structural
Biology division's rotamer instances, or provably out of reach by the route tried.  *Prerequisites:* their
software and instances; `CERTIFIED_BRACKETS.md` (unreviewed); the theory division's certificate rules.
*Missing:* the two instance numbers named in §D; a certified third-order remainder, or a certified variance
with exact elimination, to make a second-order bound tight; a review of `CERTIFIED_BRACKETS.md`.  *Baselines:*
toulbar2 for the minimum (already used by that division); published partition-function bounds for protein
design (the K*-family in OSPREY) — named from memory, to be verified by whoever takes this up.  *Benchmark:*
width of the certified enclosure of `ln Z` and time, on their six structures, against the uncertified value.
*Success:* width below 0.1 nat on at least the smallest structure at a stated cost.  *Failure:* width above
1 nat with every bound tried, together with `max_i β·c_i` above the threshold where Theorem 2 of the note
applies — which would itself be a result.  *Claude reasoning and computation:* not estimable by us; the
computation belongs to Engineering.  *Dependencies:* Structural Biology, Engineering, Theory.  *Model:* the
bound needs careful mathematics (Fable or a human); the implementation can continue with Opus.

Not recommended: more work on E-C1, on fixed-temperature hardness, on higher levels of the NANUQ problem.

## F. Publication readiness

* **B1 (with B3 as a companion section)** is the one candidate for a standalone paper in a venue on nucleic-acid
  computation.  Before an external expert it needs: the checks of §E1; an honest positioning against Condon et
  al., Lyngsø and Boehmer et al.; a statement of the model that a user of NUPACK recognises; and the removal of
  everything that reads as a claim about real parameter tables.  Formal verification covers two arithmetic
  cores and proves nothing about novelty.
* **B2** could be a note in mathematical phylogenetics *if* E2 succeeds.  Its weakest points before a
  specialist: the unseen third-party claim; a table of local terms that is computed, not proved by hand; and
  the fact that the networks concerned lie outside the class about which the source paper conjectures.
* **B4, the chain note, the certified-brackets note, the penalty note:** not publishable as they stand; they are
  answers to colleagues, largely known mathematics.

## G. State of review, incomplete items, and what is still running

| item | state |
|---|---|
| CX-T1–T4, T14, T15, T20, T24 (hardness) | reviewed three times; correct |
| CX-T10–T12, T30 (algorithm) | reviewed twice; correct |
| CX-T5–T9, T13, T26, T27, T34 (NANUQ, level ≤ 2) | reviewed (REV-0002, -0004, -0005; Theorem 12′ in -0006); correct; T6 probably a rediscovery |
| CX-T16–T19, T28, T29 (Ising) | reviewed twice; correct; largely known |
| CX-T31, CX-X3 (NANUQ beyond level 2) | reviewed once (REV-0006): Theorem A correct; two derived statements were wrong or unproved and are corrected; the survey is incomplete at four hybrid nodes (remedy not carried out) |
| CX-T32, T33 (chains) | reviewed once (REV-0006): derivations correct; hardness **known**; the realizability corollary is conditional on an unread theorem for accuracy `1/poly` |
| CX-T21–T23 (penalised product reference) | reviewed once (REV-0006): correct after a misprint; standard inequalities, no novelty claimed |
| CX-T35, T36 (certified brackets), CX-T25 (interpolation bound), Proposition 11 of the Ising note | **unreviewed** |
| Lean | CX-V1–V6: finite or arithmetic cores only; no model of structures or of networks is formalised |
| Open, documented, not pursued | E-C1 for `K ≫ log n`; #P-hardness at a fixed temperature; fixed-parameter tractability in the number of species; whether every six-leaf outer-labeled planar network displays one of 114 systems; realizability of averaged distances for chains with fixed bond angles; the Geometry division's planted model; the Theory division's open problem 1 (never started) |

**The sixth review (COMPLEXITY-REV-0006), received during the wind-down.**  It had been commissioned before the
directive; it was asked to wrap up, reported, and was stopped.  Sixteen findings, three major, all with a
disposition in the review file:

1. *Chain note, Corollary 5* — the accuracy claim exceeded its citation; restated, one half conditional on a
   source nobody here has read.  **Open:** read the two sources.
2. *Higher-levels note, Corollary C* — false as written (dropped qualifier); corrected.
3. *Higher-levels note, the robust criterion* — one direction unproved without subnetworks; the definition now
   includes them; the stronger statement is recorded as open beyond level 2.
4. *Minor, with consequences for what the survey shows* — networks are identified by an invariant that is not
   complete from three hybrid nodes on, so the four-hybrid level did not extend every network.  **Open:** a
   re-run with a complete canonical form (not done: a code change and about 90 minutes of computation, for a
   survey that is not a classification either way).
5. *Minor* — the description of the evidence for Theorem 12′ overstated its independence and coverage
   (corrected; the referee's own search supplies the missing coverage); a literature on fixed-angle chains was
   missing (added, from the referee's summaries); a misprinted inequality chain in the penalty note
   (corrected); attribution details.

**What is active.**  Nothing.  The sixth referee agent delivered its report and was stopped; there are no other
sub-agents, no background processes, no Modal or other remote jobs (this division never launched one), and no
scheduled task created by this division.  The division holds no credentials and opened no held-out dataset.

**How to resume.**  `docs/complexity/HANDOFF.md` (state, commands, warnings) and the section "Resume here" of
`docs/complexity/RESEARCH_LOG.md`.  Nothing is to be resumed without the research owner's explicit
authorisation.
