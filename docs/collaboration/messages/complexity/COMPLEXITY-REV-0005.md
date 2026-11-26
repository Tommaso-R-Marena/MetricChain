Message ID:                  COMPLEXITY-REV-0005
Message type:                Internal adversarial review of the statements added after COMPLEXITY-REV-0002/-0003/-0004: docs/complexity/NANUQ_LOCAL_CRITERION.md (Corollary 5′, §7.1, §7.2, the completed Lemma 0), docs/complexity/ISING_GROUND_SETS.md (Corollary 5a, Propositions 12, 13, 13′, Theorem 14, the corrected cut-metric formulation), docs/complexity/STRANDS_ALGORITHM.md (Proposition 5 and the paragraph "What is and is not ours")
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          All divisions (for the record); Ensemble division (the status of Propositions 13, 13′ changes); the division itself (findings to process)
Date and time (UTC):         2026-11-26 22:50
Priority:                    High
Status:                      Review received 2026-11-26 22:43 UTC; **every finding processed** by 2026-11-26 23:27 UTC (disposition table at the end of this file)
Relevant source commit:      1ba144d (the referee notes that the three documents and the programs it ran are byte-identical at 25bcd61 and 75266b2, which appeared during the review; files added there — NANUQ_HIGHER_LEVELS.md, the Lean file NanuqPattern.lean, six_leaf_survey.py — were not reviewed)
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T26, CX-T27 (NANUQ); CX-T28, CX-T29 and the rewritten CX-T16–CX-T19 (Ising); CX-T30 and the attribution of CX-T10–CX-T12 (strand algorithm)
Related message/request IDs: COMPLEXITY-MSG-0004 (fourth checkpoint, where these statements were announced as unreviewed), COMPLEXITY-RES-0008, COMPLEXITY-REV-0002, -0003, -0004

Scientific context:
Fifth internal adversarial review.  It covers everything that COMPLEXITY-MSG-0004 announced as new and unreviewed,
except the companion note on higher levels and the kernel-checked file.
Verdict of the referee: **no stated theorem is false**; Theorem 12 (level 2), Corollaries 13–14, Theorem 10′,
Corollary 5′, Lemmas C and D and the completed Lemma 0 survived the referee's own code on about 1.4 million explicit
networks of level at most 2 and 31 000 random ones; the Ising additions and Proposition 5 are correct.
**The defects are in attribution, and one corollary is ambiguous:** (7) Proposition 13′ is a weak form of a theorem
of Odlyzko (1988), which also answers what the note called "not determined"; (8) Proposition 13 follows in two lines
from Laurent–Poljak's description of the faces and normal cones of the elliptope and was listed under "no source
found"; (2) the dichotomy of Lemma C is Lemma 4.2 of Huber, van Iersel, Jones, Moulton, Veenema-Nipius
(arXiv:2408.12997); (11), (12) the novelty paragraph of the algorithm note misdescribes one theorem of Boehmer et
al. and omits their sentence that the extension to the Turner model "does not pose any algorithmic challenges";
(1) the implication (v) ⇒ (i) of Corollary 14 is proved for the induced circular order only.

What this review is and is not:
The referee was a separate AI agent instantiated by this division with an adversarial brief (re-derive, recompute
with code written from the definitions of the source paper, search for prior art, state the strongest hostile
objection).  It had no access to our reasoning, only to the files of this branch.  **This is an internal AI
review.  It is not independent academic peer review**, and the results it covers remain unrefereed in the sense of
the collaboration README.  The report is reproduced verbatim below.  Paths in the report that point to a session
scratch directory refer to the referee's working directory; the referee's programs and logs are preserved in
`experiments/complexity/reviews/rev5_nanuq_ising_strands/` (downloaded papers are not redistributed).

---------------------------------------------------------------------------------------------------------------
REPORT (verbatim)
---------------------------------------------------------------------------------------------------------------

# Adversarial review (REV-0005) of the NANUQ, Ising and strands notes

**This is an internal AI review, not academic peer review.** I did not modify the repository: all my files are under the scratch directory, and the authors' programs were run from there with `python3 -B`.

## Bottom line

I found no stated theorem that is false. Theorem 12, Corollaries 13–14, Theorem 10′, Corollary 5′, Lemmas C and D, the four trees and the completed Lemma 0 all survived my own code, written from the definitions of arXiv:2507.17308v2. That code covers about 1.4 million explicit outer-labeled planar networks of level ≤ 2 from exhaustive hybrid-arc insertion, plus 31,000 random ones with up to 16 leaves, and found zero deviations. The mathematics of the Ising additions and of Proposition 5 is also correct.

The real defects are in attribution and one ambiguous corollary:

- **Proposition 13′** is a weak form of Odlyzko's 1988 theorem, and the note's "not determined" remark is answered there.
- **Proposition 13** is a two-line corollary of Laurent–Poljak Theorems 2.7 and 2.9, yet is listed under "no source found".
- **Lemma C**'s dichotomy is Lemma 4.2 of Huber et al. (arXiv:2408.12997).
- **The strands novelty paragraph** misattributes Boehmer et al.'s Theorem 6 to the base-pair model and omits their statement that the Turner extension "does not pose any algorithmic challenges".
- **Corollary 14, (v) ⇒ (i)** is proved only for the induced circular order.

## Commit reviewed

`1ba144d`. The three documents and the programs I ran are byte-identical at `25bcd61` and `75266b2`, which appeared while I worked. I did not review the files added there.

## Verdicts

### Part 1 — `NANUQ_LOCAL_CRITERION.md`

| Claim | Verdict |
|---|---|
| Corollary 5′ | Correct. Proof checked; 1,800 labellings recomputed, 60 negative, 0 mismatches. |
| 𝒦′ and Theorem 10′(a) | Correct. Also checked on all 2,682 seven-point and 96,697 eight-point tree-generated systems. |
| Theorem 10′(b), closure under substitution | Correct. Proof checked; 34,750 substitutions tested. |
| Theorem 10′(c), formula and "negative for m ≥ 5" | Correct. 30 (system, missing 2-split) pairs, m = 1..6, four clade orientations. |
| Theorem 10′(d): 17 = 6+3+6+2, 133 = 127+6, least m ≤ 3, no circular order | Correct. Least m is 1, 2, 3 for 3, 6, 8 systems; brute force over all (n−1)!/2 orders, 102 cases, none Kalmanson. |
| Theorem 10′ "Consequently" and Remark 2 (classes of networks) | Correct. |
| §7.1 Remark 1, last sentence | Unproved as stated. No counterexample on ≤ 8 points (exhaustive) or in samples on 9–10 points (finding 3). |
| "Blobs, positions, sizes", exactly one source | Correct. |
| Lemma D | Correct. |
| Lemma C, including planarity | Correct. The dichotomy is known (finding 2). |
| Positions b, x, y, c; circular order; trees T₁..T₄ | Correct. 219 bloblets, 1,647 explicit networks, every source placement. |
| Theorem 12(a), (b), (c) | Correct. No counterexample found. |
| Step 1 finite facts | Reproduced. 624 substitutions (74 distinct systems), all 6-locally good; 16,555 restrictions of Σ[k], 990 exceptional, all of type (3,1,1) or (4,1,0), all "nine minus {2nd, 3rd b}" and globally good. |
| Step 4 table | Reproduced exactly from explicit networks. |
| Corollary 13 | Correct. 445 bloblets (66 negative, 9 zero); the nine failing ones with ≤ 9 leaves are Kalmanson for no order. |
| Corollary 14 | (i)⇔(ii)⇔(iii)⇒(iv)⇒(v) correct. (v)⇒(i) is proved only for the induced order (finding 1). |
| §7.2 Remarks 1–4 | Correct. The numbers in Remark 4 match the authors' logs. |
| Lemma 0, new paragraph | Correct; step (3) is complete. Wording only (finding 6). |

### Part 2 — `ISING_GROUND_SETS.md`

| Claim | Verdict |
|---|---|
| Corollary 5a | Correct. The time bound needs a qualifier (finding 9). |
| Proposition 12 | Correct. |
| Proposition 13, including constants, evenness and the SDP parenthesis | Correct. Known in substance (finding 8). |
| Proposition 13′: the 3/4 bound, −0.0389, 0.003, 4·10⁻⁵ | Correct. Superseded by Odlyzko 1988 (finding 7). |
| Theorem 14 and (a), (b), (c) | Correct. Re-derived case by case; the ETH claim is justified (finding 10). |
| "Formulation with cut metrics (corrected)" | Correct. |

### Part 3 — `STRANDS_ALGORITHM.md`

| Claim | Verdict |
|---|---|
| Proposition 5: Möbius inversion, digits, 24^N, N_R(m)·R/c, MFE formula | Correct. |
| Bit bound O(cGN²) | Correct as an upper bound (finding 15). |
| The (min,+) remark | Correct; should read "iff every minimiser is symmetric" (finding 14). |
| "What is and is not ours" | The citations to Boehmer et al. and Shalaby–Woods check out, with one wrong statement and one omission (findings 11, 12). |

## Findings

### Part 1

1. **MAJOR if "(v)" means "for some circular order"; otherwise MINOR. Corollary 14, proof of (v) ⇒ (i).**
   - The proof makes α(S*) negative for the induced order C only.
   - The note uses "Kalmanson" in the stronger sense elsewhere (Theorem 10′ "Consequently", the [X] sentence of Corollary 13).
   - Under that reading the implication is unproved. Theorem 10′(d) cannot be invoked: the family "N with clades" is not closed under restriction, and d_N restricted to a subset is not the NANUQ metric of the subnetwork.
   - §9 concedes this for Theorem 12, but Corollary 14 carries no qualifier.
   - Evidence: I ran 120 blow-ups built as in the proof (60 non-bloblets, ≤ 10 leaves) and 150 further non-bloblets with a negative critical weight. None is Kalmanson for any order.
   - Fix: write "(v) … Kalmanson for the induced circular order", or state the all-orders version as a conjecture with this evidence.

2. **MINOR, attribution. Lemma C and §0 item 6.**
   - The dichotomy is Lemma 4.2 and Figure 8 of Huber, van Iersel, Jones, Moulton, Veenema-Nipius, arXiv:2408.12997v3. Case (a) there is a reticulation at an end vertex of the theta graph (the note's "nested"); case (b) is reticulations on two different sides (the note's "galled").
   - Their proof only asserts that other placements cannot be oriented.
   - The note's own additions are the orientation argument, the source location, parallel edges, and the position-free path under planarity.
   - Fix: cite it.

3. **MINOR, unproved sentence. §7.1 Remark 1.**
   - "A system of 𝒦′∖𝒦 has a Kalmanson metric which gives positive weight to a split that no tree of the system has."
   - This is not immediate: the six-point term with Φ6 > 0 need not be a term of a split of the larger system, because its end leaves need not be adjacent.
   - It holds on all systems with 6, 7, 8 points (6, 273 and 7,816 systems of 𝒦′∖𝒦) and on 438 random ones with 9–10 points.
   - Fix: label it [X] with that range, or prove it.

4. **MINOR. Theorem 12, Step 1, "624 substitutions".**
   - These are 624 quadruples (Σ₁, Σ₂, p, r) giving 74 distinct systems.
   - The fact is not independent: every tree-generated system on ≤ 5 points lies in 𝒜 (1/3/16), so these systems are in 𝒞₆ and are covered by Lemma 8.
   - I recomputed Lemma 8 independently: |𝒜₄..₆| = 3, 16, 102; |𝒞₆| = 108; all 6-locally good; 19 good systems outside 𝒞₆.

5. **MINOR. Theorem 10′(c), (d).**
   - The formula in (c) holds for arbitrary clades; the proof uses nothing about caterpillars.
   - The "no circular order" statement in (d) depends on the clades. Say which were used. All four planar orientations of caterpillars fail.

6. **MINOR. Lemma 0.**
   - Step (2): Menger needs ℓ non-adjacent to the sink (true, since ℓ is not a leaf). Say also that two internally disjoint ℓ–sink paths are two paths to different leaves.
   - Last sentence: "rooted partner U" should read "U with its degree-2 nodes suppressed", with ℓ the least stable ancestor of Y in U by (2).
   - Test: 800 random networks with 1–4 hybrid nodes, 29,708 subsets Y, against a literal implementation of Def. 2.5. There were 0 mismatches of T(N|_Y) against {T|_Y}; U always has the single source LSA(Y).

### Part 2

7. **MAJOR, prior art. Proposition 13′ and the paragraph after it; §0; §7.**
   - The probability that the span of K independent uniform ±1 vectors contains another ±1 vector is exactly the subject of Odlyzko, J. Combin. Theory A 47 (1988) 124–133.
   - The question comes from Kanter–Sompolinsky's associative memory (Phys. Rev. A 35 (1987) 380).
   - Odlyzko's result: P = 4·C(K,3)(3/4)ⁿ + O(K⁴(5/8)ⁿ) + O((7/10)ⁿ) for K ≤ n − 10n/ln n.
   - Irmatov, arXiv:2405.05082 (2024), extends this to K ≤ n − 1.
   - Consequences for the note:
     - "these dominate" (supported there by simulations) is a theorem;
     - "We have not determined up to which K …" is answered;
     - Proposition 13′ survives only as an elementary non-asymptotic bound.
   - I read Irmatov's abstract and pp. 1–2, which quote Odlyzko's Theorem 1.1. Odlyzko's own PDF returned 503.
   - Fix: cite all three and rewrite the remark and the §0 bullet.

8. **MAJOR, attribution. Proposition 13 is listed in §0 and §7 under "no source found".**
   - It follows in two lines from Laurent–Poljak (report BS-R9501), which the note already cites for Proposition 5:
     - Theorem 2.7: every face of the elliptope is F_V = {X : ker X ⊇ V}, and F(X₀) = {ker X ⊇ ker X₀}.
     - Theorem 2.9: the normal cone is {D − M : D diagonal, M ⪰ 0, ⟨M, A⟩ = 0}. These are exactly the degree-2 certificates.
   - Their Example 3.8 already uses "the cut matrices of F_V are the ffᵀ with f ⊥ V".
   - The energy in (ii)⇒(i) is the projection rule of the same Kanter–Sompolinsky setting.
   - I did not find the statement verbatim in sum-of-squares language.
   - Fix: label it [K-corollary].

9. **MINOR. Corollary 5a, "time 2^K·poly(n)".**
   - For the exposedness decision this needs a linear programme solver that is linear in the number 2^(K−1)+K of variables (Clarkson-type, or Lee–Sidford).
   - A generic polynomial LP bound gives only 2^(O(K))·poly(n).
   - For SPAN (Theorem 14(b)) the bound is literal.

10. **MINOR. Theorem 14(b).**
    - The ETH claim is right. It can be made self-contained.
    - Schaefer's clause gadget and the negation gadget R(x,x′,a), R(x,x′,b), R(a,b,c), which forces x′ = ¬x, are both of linear size.
    - With sparsification, positive 1-in-3-SAT has no 2^(o(N)) algorithm. Here K = N + 2 and n = O(N + M²).
    - The parenthesis in Proposition 13(i) is accurate. Add one line: strong duality with dual attainment, since X = I is strictly feasible.

### Part 3

11. **MAJOR, wrong statement about a cited source. §0, "the problem is NP-complete for unboundedly many (Theorem 6)" and "For the base-pair model of Boehmer et al. this dichotomy is their Theorems 5 and 6".**
    - Theorem 6 ("Unary Triplet Repeat Multi-Strand MFE is NP-complete") is proved in a model with base-pair reward −m³, a multiloop penalty, an association reward and θ = 3.
    - The authors write: "Our reduction requires more than the naive base pair maximization model" and "Even if the following reduction does not work in the base pair maximization model …".
    - Their problem also allows several complexes.
    - Hardness in the base-pair model for Θ(N) strands is attributed by [SW26] to its reference [5], and by Boehmer et al. to their [14].

12. **MAJOR, omission bearing on the novelty claim. §0, "What this note adds".**
    - The journal version of Boehmer et al. also contains:
      - Conclusion: "it is desirable to describe in detail how to extend the MFE Strand Interaction algorithm to the full thermodynamic setting considered in [13]. While the extension to the Turner model does not pose any algorithmic challenges, …";
      - a section "Incorporating a simple nearest-neighbor energy model" (strand-soup MFE, O(n⁴m²p³));
      - Theorem 8 (strand soup, polynomial in m and p) and Remark 4 (partition-function technique for the triplet-repeat and strand-soup settings).
    - The paragraph must quote the first item: the originators call the nearest-neighbour extension routine but did not write it out, while [SW26] calls it open.

13. **MINOR.** "Lemma 18 of Shalaby–Woods (ICALP 2025)" is the numbering of arXiv:2407.09676v1. [SW26] Remark 29 cites the same statement as "lemma 20 of [44]".

14. **MINOR. §4a.** "whenever the loop-energy minimiser is symmetric" should read "if and only if every loop-energy minimiser is symmetric". Asserted and passed in all 22 systems.

15. **MINOR. Proposition 5.**
    - With affine multiloops the hypothesis "every loop energy ≤ Gε" makes G grow with N.
    - State the bit bound as O(N·E_max/ε).
    - The factor c is unnecessary for the final numbers.

## What I computed

All of this is my own code, exact integer or rational arithmetic.

**Anchors**
- Table 1(a) of arXiv:2507.17308v2 (6-cycle network) reproduced.
- N* matrix reproduced; α({x,y}) = −1; weight 5 for the multiplicity-weighted metric.

**Exhaustive, two hybrid nodes, all tree shapes on 4–8 leaves** (tail on any edge or above the root; same edge allowed, giving parallel edges)
- 2,046,012 insertion sequences; 1,477,330 valid networks.
- 1,035,352 outer-labeled planar, of which 421,806 non-galled.
- 117,296 critical splits, of which 11,684 are ≤ 0.
- 0 violations of blob structure, of Lemma C, of "galled ⇔ no nested blob", of the block order, or of Theorem 12.
- Among the 441,978 non-planar networks, positions on both A and B do occur; among planar ones, never.

**Exhaustive, three hybrid nodes, level ≤ 2, 4–6 leaves**
- 362,792 planar networks with 2 or 3 non-trivial blobs; 20,011 critical splits; 0 violations.

**Random**
- Structured: 16,000 networks, ≤ 16 leaves, ≤ 9 hybrid nodes.
  - 12,353 contain a nested blob entered through a cut edge; 8,949 contain ≥ 2 nested blobs.
  - Pendant subnetworks include level-1 cycles, galled level-2 blobs, 2-blobs and clades.
  - 6,490 critical splits (1,183 ≤ 0); 613,053 other splits; 0 violations.
- Unstructured: 15,000 networks, 69,397 (network, induced order) pairs; 0 violations.
- Mutation test: four wrong variants of formula 12(b) are caught on 14–165 of 600 networks; the note's formula on none.

**Any level**
- 5,500 planar networks of levels 1–6.
- All 3,399 six-leaf restrictions that are not 6-locally good come from six positions of one blob (§7.2 Remark 3).
- Theorem 10′(a) and Theorem 4 hold on all 5,194 networks in 𝒦′.

**Split systems**
- Counts 1/3/16/150, 141 and 127 reproduced; 147 of the 150 are Kalmanson for the given order.
- Seven points: 2,682 systems, split 1,254 / 273 / 1,155 between 𝒦, 𝒦′∖𝒦 and outside 𝒦′.
- Eight points: 96,697 systems, split 13,807 / 7,816 / 75,074.
- The split metrics of the circular splits are linearly independent for n = 4..10.
- Corollary 14 (i)⇔(ii)⇔(iii) on 1,200 networks.

**Ising**
- Proposition 12 for m = 4..8, by the full linear programme.
- Proposition 13 on 400 instances.
- Full versus restricted linear programme on 362 instances (only 8 not exposed).
- Theorem 14 on 820 instances (749 satisfiable): the extra sign vectors are exactly the exact hitting sets, and all instances are exposed (154 by the full linear programme).

**Strands**
- My enumerator works by the C_c action on pairs (Y, S), a different method from the authors' label-permutation orbits.
- It agrees with the authors' `dp_levels` on 22 systems: 3,473 physical structures, symmetries 1, 2, 3, 4, 6.
- The symmetry-naive value is too low in 10 of them.

**Authors' programs, run for comparison** (outputs agree with the note)
- `kalmanson_only.py` (also with `extra`), `forbidden_in_nstar.py`, `level_counts.py`, `span_algorithm.py reduction`, `degree2_certificates.py`.

**Not checked**
- The Lean files.
- Lemma A was used as given; its consequences are covered by the network tests.
- Theorem 1 of the strands note.
- The K = 6 sampling quoted in the Ising note.

## What I searched and read

**Searches** (13 queries)
- NANUQ / quartet-distance circular decomposability for non-galled networks.
- Follow-ups to Holtgrefe et al. in 2026.
- Classification of outer-labeled planar level-2 networks.
- Forbidden six-taxon configurations for Kalmanson metrics.
- The vibemathed title (no hit; repository not accessed).
- Boehmer et al.; Shalaby–Woods 2611.27945; Laurent–Poljak BS-R9501.
- Hopfield projection rule and spurious states.
- NP-completeness of ±1 vectors in a span.
- Odlyzko 1988.

I found nothing on non-galled NANUQ results, a level-2 classification by this property, or forbidden six-taxon patterns.

**Read**
- [arXiv:2507.17308v2](https://arxiv.org/pdf/2507.17308v2): §2, §3, §4 to Lemma 4.3, Theorem 4.7, Table 1, §6.
- [MathWorld, NANUQ Distance](https://mathworld.wolfram.com/NANUQDistance.html), through a fetch summary. It cites the vibemathed entry: galled, all levels, six-label reduction; nothing on non-galled networks.
- [arXiv:2408.12997v3](https://arxiv.org/pdf/2408.12997v3): §4, Lemma 4.2 with proof.
- [Laurent–Poljak BS-R9501](https://ir.cwi.nl/pub/5056): pp. 1–7 and 12–15, as page images.
- [Tropp, arXiv:1801.00749](https://arxiv.org/abs/1801.00749): statements of Facts 2.5–2.8 and Theorems 2.9–2.11.
- [Irmatov, arXiv:2405.05082](https://arxiv.org/abs/2405.05082): abstract, pp. 1–2, references.
- [Boehmer et al., journal version](https://link.springer.com/article/10.1186/s13015-025-00292-8), via the Europe PMC XML (PMC13014723): all sections on interactions, hardness, strand soup, and the conclusion.
- [WABI 2024 version](https://drops.dagstuhl.de/storage/00lipics/lipics-vol312-wabi2024/LIPIcs.WABI.2024.18/LIPIcs.WABI.2024.18.pdf): statements of Theorems 14, 16, 19 and Remark 15.
- [arXiv:2611.27945v2](https://arxiv.org/abs/2611.27945): abstract, §1.5, Defs 11–17, Lemmas 19, 31, 39, Def 25, Remarks 26, 29, Algorithm 4, Theorem 41.
- [arXiv:2407.09676v1](https://arxiv.org/abs/2407.09676): abstract, Lemma 18.

**Not accessible**
- Odlyzko's paper (503).
- Kanter–Sompolinsky 1987.
- The Springer and PMC web pages (challenge pages).

## Strongest hostile objection per part

- **Part 1.** "Theorem 12 classifies split weights for the planar order only. The 'bad' blob is the already-known second level-2 generator. Where a critical weight is negative, the note does not show that the metric fails for every circular order (nine bloblets only), and these networks lie outside the class the published conjecture is about. The positive all-level result (Theorem 7) is probably a rediscovery. Everything rests on tables that no kernel checks."
- **Part 2.** "Proposition 13 is Laurent–Poljak 1993/95 restated with the 1980s projection rule. Proposition 13′ is a weak form of Odlyzko 1988, written for exactly this memory model. Theorem 14 is a routine Partition-style reduction which, by its own item (c), says nothing about the original question E-C1. That question is still open."
- **Part 3.** "Sub-multiset dynamic programming over all orderings, the symmetry quotient with a marked element, inclusion–exclusion over symmetry degrees and count-indexing for few species are all in Boehmer et al., who say the Turner extension poses no algorithmic challenge. The note writes that exercise out with L⁴ instead of L³ and validates it for N ≤ 16. Proposition 5 is the digit trick of [SW26] §7 plus Möbius inversion."

## Files

Everything is in `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review5/`.

**Libraries**
- `mynet.py`, `mygen.py`, `myblob.py`, `mybuild.py`, `mysplits.py`, `mylemma0.py`, `ising_mine.py`, `strands_mine.py`

**Tests** (each with `.log` files of the same stem)
- `t0_anchor.py`
- `t1_exhaust.py`
- `t1b_exhaust3.py`
- `t2_sixpoint.py`
- `t3_thm10prime.py`
- `t3b_allpairs.py`
- `t4_struct.py`
- `t5_nestedfacts.py`
- `t6_table.py`
- `t7_orders.py`
- `t8_randins.py`
- `t9_seven.py`
- `t9b_eight.py`
- `t9c_random.py`
- `t10_misc.py`
- `t11_mutation.py`
- `t12_closure.py`
- `t13_cor14.py`
- `t14_anylevel.py`
- `t15_cor14v.py`
- `t16_lemma8.py`
- `t20_ising.py`
- `t21_thm14.py`
- `t30_levels.py`

**Subfolders**
- `authors_runs/` — outputs of the authors' programs
- `papers/` — downloaded sources

---------------------------------------------------------------------------------------------------------------
END OF REPORT
---------------------------------------------------------------------------------------------------------------

Disposition of the findings (by the division; completed 2026-11-26 23:27 UTC):

| # | finding (short) | disposition |
|---|---|---|
| 1 | MAJOR under one reading: Corollary 14, (v) ⇒ (i) proved for the induced circular order only | **Accepted.**  (v) now reads "Kalmanson for the induced circular order"; a paragraph after the proof states that the all-orders version is not proved and records the referee's 270 instances as evidence.  We did not find a proof of the all-orders version and do not register it as a conjecture.  `THEOREMS.md` CX-T27 reworded |
| 2 | MINOR, attribution: the dichotomy of Lemma C is Lemma 4.2 of arXiv:2408.12997 | **Accepted.**  Citation checked by a fetch of the abstract page and the HTML of v3 (title, authors, the lemma verbatim, the case distinction).  Attribution paragraph after Lemma C; §0 item 6; §12; `PRIOR_ART.md` B-VIII; the lemma is now labelled [K] for the dichotomy and [P] for what the proof adds |
| 3 | MINOR: last sentence of §7.1, Remark 1 unproved | **Accepted.**  Sentence replaced by "not proved", with the range of the referee's computation (all systems on 6–8 points; samples on 9–10) |
| 4 | MINOR: "624 substitutions" are quadruples (74 systems) and not an independent fact | **Accepted**, said in Step 1 of the proof of Theorem 12 |
| 5 | MINOR: Theorem 10′(c) holds for arbitrary clades; (d) depends on the clades | **Accepted.**  Both said; the clades of our computation described (caterpillars with the cherry at the first two leaves); the referee's recomputation for all four orientations cited |
| 6 | MINOR: wording of Lemma 0 | **Accepted**, both sentences reworded |
| 7 | MAJOR, prior art: Proposition 13′ is a weak form of Odlyzko (1988); Irmatov (2024); Kanter–Sompolinsky (1987) | **Accepted.**  The theorem is quoted after Proposition 13′ (from Irmatov's Theorems 1.1, 1.2, which a fetch of ours confirmed; Odlyzko's paper could not be opened by the referee or by us and is cited with that caveat); the "not determined" sentence is withdrawn — the answer is every `K ≤ n − 1`; Proposition 13′ relabelled as an elementary bound; §0, §7; `PRIOR_ART.md` C-VIII, C-IX; `THEOREMS.md` CX-T28 |
| 8 | MAJOR, attribution: Proposition 13 follows from Laurent–Poljak, Theorems 2.7 and 2.9 | **Accepted.**  Relabelled "[K] in substance"; attribution paragraph; removed from the list "no source found" in §0 and §7; `PRIOR_ART.md` C-I (addition); `THEOREMS.md` CX-T28.  We have not read those two theorems ourselves (the referee read the pages) and say so |
| 9 | MINOR: the time bound of Corollary 5a | **Accepted.**  `2^{O(K)}·poly(n)` for the exposedness decision in §0, §4, Corollary 5a, the table of §6 and `THEOREMS.md` CX-T16; `2^K·poly(n)` kept for the span problem.  COMPLEXITY-RES-0003/-0008 and MSG-0004/-0005, which say `2^K·poly(n)`, receive a linked correction in the next checkpoint message |
| 10 | MINOR: ETH claim of Theorem 14(b) can be self-contained; strong duality line | **Accepted**, both added (the negation gadget checked by hand) |
| 11 | MAJOR: Theorem 6 of Boehmer et al. is not about the base-pair model | **Accepted.**  §0 of the algorithm note: item "Hardness, corrected" and the closing paragraph; `PRIOR_ART.md` A-III(j).  We rely on the referee's reading of the journal version |
| 12 | MAJOR, omission: Boehmer et al. call the Turner extension free of algorithmic challenges; section with a simple nearest-neighbour model; Theorem 8; Remark 4 | **Accepted.**  New item in §0 quoting the sentence; "What this note adds" now says "written out" and that we do not present the extension as a new idea; `THEOREMS.md` CX-T12; `PRIOR_ART.md` A-III(j) |
| 13 | MINOR: numbering of "Lemma 18" | **Accepted** |
| 14 | MINOR: "whenever the minimiser is symmetric" | **Accepted**: "if and only if every loop-energy minimiser is symmetric" (verified: the naive value is at most the least loop energy, the true value exceeds it exactly when no minimiser is asymmetric) |
| 15 | MINOR: bit bound of Proposition 5 | **Accepted.**  `O(N·E_max/ε)`; the factor `c` removed (the tables for `F_d` raise weights to the power `d` on quotient structures whose energy is `1/d` of the represented structure's); §0, §4a, §6, `ASSUMPTION_AUDIT.md`, `THEOREMS.md` CX-T30 |

Not covered by this review (the referee says so): the Lean files; Lemma A (used as given); Theorem 1 of the
algorithm note; the `K = 6` sampling quoted in the Ising note; and everything added at commits 25bcd61 and later
(`NANUQ_HIGHER_LEVELS.md`, `NanuqPattern.lean`, the six-leaf survey, the chain-geometry note).

The referee's three "strongest hostile objections" are quoted in the changes sections of the three notes.  We
accept them as fair descriptions: (Part 1) Theorem 12 is about split weights for the planar order, on networks
outside the class about which the source paper conjectures anything; (Part 2) of the Ising additions only the
span problem (Theorem 14) has no source found, it is routine, and by its own item (c) it does not touch E-C1,
**which remains open**; (Part 3) the algorithm note writes out an extension that the originators of the method
called routine.
