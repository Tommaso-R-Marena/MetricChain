# Prior-art register (complexity division)

For every source: what it is, **how it was inspected**, and what we take from it.  "Read in full"
means the complete text was read by the division (from a PDF converted with `pdftotext`); "sections
read" names them; "abstract only" and "search snippet only" mean exactly that.  A failure to find a
result is recorded as a failed search, not as evidence of novelty.

## §A  Nucleic-acid folding complexity

| # | source | how inspected (date) | what it establishes for us |
|---|---|---|---|
| A-I | Ducloz, Shalaby, Woods, *Algorithmic Hardness of the Partition Function for Nucleic Acid Strands*, DNA 31 (2025), doi:10.4230/LIPIcs.DNA.31.1 | conference PDF from drops.dagstuhl.de, **read in full** (2026-11-26); arXiv:2506.19756v1: Definition 9, Note 10, Appendix A.2 (loop energies; "∆G_exterior = 0") and Appendix B.3 (Lemma 31, Theorem 32) **read** (2026-11-26, after REV-0001) | definitions; reduction map; #P-hardness of PF in BPS (1 strand, pseudoknots) and BPM (unbounded strands) **with the temperature/magnification as part of the oracle's input**; five open questions (A1–A5) |
| A-II | Shalaby, Woods, *One partition function call to rule them all*, arXiv:2611.27945v2 (23 Nov 2026) | arXiv PDF, **§§1–3 read** (2026-11-26); §§4–7 skimmed for statements only | resolves A2 (magnifiable PF with rotational symmetry, `O(N³(c−1)!)`); MFE and #SSEL from one call; four new open questions (A5–A7) |
| A-III(j) | the **journal version** of A-III: Boehmer, Berkemer, Will, Ponty, Algorithms Mol. Biol. 21:4, doi:10.1186/s13015-025-00292-8 (first published 2025-12-10; this is reference [3] of A-II) | full text downloaded from Europe PMC by the referee of COMPLEXITY-REV-0003; **the section "Translation to partition function" read by us in full (2026-11-26, after the review): Lemmas 8–14, Theorem 4, Remarks 3–4; the statements of Theorems 5 and 6**; the rest by the referee | **for the base-pair model**: partition functions of `r`-symmetric structures "without iterating over all circular permutations"; a bijection with structures carrying one marked base pair on the strand set with every sequence `r` times less often (Lemma 12); a recursion over symmetry degrees (Lemma 14); Theorem 4: the partition function over `m` strands in `O(3^m n³ m²)`; Remark 3 (the `kT log r` correction can be added); Remark 4 and Theorem 5 (count-indexed, bounded number of different strands); Theorem 6 (NP-complete for unboundedly many).  **We had not read this version when CX-T10–T12 were first registered, and their prior-art statements were wrong as worded** (COMPLEXITY-REV-0003, finding 1)  **Added after COMPLEXITY-REV-0005 (findings 11, 12; read by that referee through the Europe PMC XML, not by us):** the journal version also has a section "Incorporating a simple nearest-neighbor energy model" (strand-soup minimum free energy, `O(n⁴m²p³)`), Theorem 8 (strand soup, polynomial in `m` and `p`), and the sentence in the conclusion "While the extension to the Turner model does not pose any algorithmic challenges, …"; and its Theorem 6 ("Unary Triplet Repeat Multi-Strand MFE is NP-complete") is proved in a model with base-pair reward `−m³`, a multiloop penalty, an association reward and minimum hairpin size 3, with several complexes — the authors write "Our reduction requires more than the naive base pair maximization model".  Our earlier summary ("NP-complete for unboundedly many strands in the base-pair model, Theorem 6") was wrong |
| A-III | Boehmer, Berkemer, Will, Ponty, *RNA Triplet Repeats: Improved Algorithms for Structure Prediction and Interactions*, WABI 2024, doi:10.4230/LIPIcs.WABI.2024.18 | conference PDF, **§§1, 2, 4, 6 read** (2026-11-26); appendix not read | subset dynamic programme `O(3^m n³)` for multi-strand MFE in a base-pair model without symmetry (Thm 14); remark on PF with per-symmetry terms (Rem. 15); XP algorithm in the number of distinct strands (Thm 16); NP-completeness for triplet repeats (Thm 19); polynomial "strand soup" algorithm (Thm 20) |
| A-IV | Shalaby, Woods, *An efficient algorithm to compute the minimum free energy of interacting nucleic acid strands*, ICALP 2025, arXiv:2407.09676 | arXiv PDF downloaded; **not yet read** beyond what A-I/A-II quote | MFE with rotational symmetry in `O(N⁴(c−1)!)` |
| A-V | Condon, Hajiaghayi, Thachuk, *Predicting minimum free energy structures of multi-stranded nucleic acid complexes is APX-hard*, DNA 27 (2021), doi:10.4230/LIPIcs.DNA.27.9 | conference PDF, **§1, §2 (first page), §7 read** (2026-11-26); the reduction itself not read | NP-/APX-hardness of multi-strand unpseudoknotted MFE in the base-pair model ("with at least k base pairs"), "whether or not rotational symmetries are accounted for"; about richer models only the sentence "it would seem unlikely that the prediction problem becomes easier if the energy model is more sophisticated" — no stacking or loop-based multi-strand reduction |
| A-VI | Lyngsø, *Complexity of pseudoknot prediction in simple models*, ICALP 2004 | **not read**; known through A-I App. B.3, which reproduces its strand `C^{w(a_1)}A…AAA G^B A G^B…` ("We proceed exactly as Lyngsø") | NP-hardness of pseudoknotted single-strand MFE in BPS by a reduction from BIN PACKING; **the template/item gadget of our CX-T1 is this gadget with the `C`-runs cut into separate strands** |
| A-VII | Dirks, Bois, Schaeffer, Winfree, Pierce, *Thermodynamic analysis of interacting nucleic acid strands*, SIAM Review 49 (2007) | **not read**; known through A-I, A-II | multi-strand PF, representation theorem, symmetry correction `Q(π) = Q̃(π)/v(π)` |
| A-VIII | Demaine, Gomez, Grizzell, Hecher, Lynch, Schweller, Shalaby, Woods, *Domain-based nucleic-acid minimum free energy: algorithmic hardness and parameterized bounds*, DNA 30 (2024), doi:10.4230/LIPIcs.DNA.30.2 | conference PDF, **abstract, §1 and Table 1 read** (2026-11-26); proofs not read | domain-level results only: NP-completeness for 2-domain strands, ETH lower bounds `2^{Ω(|S|)}` in the number of strands at the domain level (their Thms 16, 17), P/P-hardness for 1-domain strands; nothing on base-level stacking/NN energies |
| A-IX | Bansal, Oosterwijk, Vredeveld, van der Zwaan, *Approximating vector scheduling: almost matching upper and lower bounds*, Algorithmica 76 (2016) | **not read by us**; read by the referee (REV-0001, finding 4, PMC version) | states a `2^{o(q)}` ETH lower bound for 3DM with the number of triples of Garey–Johnson's reduction; the linear bound on the triples is only a parenthetical remark there.  We no longer rely on it (Appendix A of the hardness note) |
| A-X | Impagliazzo, Paturi, Zane, *Which problems have strongly exponential complexity?*, JCSS 63 (2001) | **not read**; the sparsification lemma is cited from memory as a standard fact | under ETH, 3-SAT has no `2^{o(m)}` algorithm in the number `m` of clauses — the only cited ingredient of CX-T14 |
| A-XI | Garey, Johnson, *Computers and Intractability* (1979), Theorems 3.2, 4.3, 4.4 | **not at hand**; Theorem 4.3 known through the overview in A-I App. B.3; the sizes of the 4-PARTITION instance were written down from memory and **the reduction re-proved** in Appendix A of the hardness note (and tested) | strong NP-completeness of 3DM-based 4-PARTITION / 3-PARTITION |
| A-XII | NNDB Turner-2004 bulge-loop rules; ViennaRNA parameter files (`rna_turner2004.par` etc.) | **inspected by the referee only** (REV-0001 finding 1) | hypothesis (H2) fails for the Turner-2004 single-nucleotide bulge rule; (H2′) holds on the loop types of our instances according to the referee's computation |
| A-XIII | Shalaby, PhD thesis, cited in A-II as [43] "Defended Nov. 2026. To appear" | **not public, not inspectable** | an uninspectable risk for the novelty of CX-T1–T4 |

Searches (2026-11-26, web search, "extended" mode):
1. `"partition function" nucleic acid strands "rotational symmetry" "magnification" OR "magnifiable" polynomial time "#SSEL" OR "density of states" multi-stranded 2026` → found A-II.
2. `Boehmer Berkemer Will Ponty "RNA triplet repeats" …` → found A-III and its journal version.

3. `NP-hard minimum free energy multiple strands pseudoknot-free "stacking" model "3-partition" OR "bin packing" nucleic acid "nearest neighbor" unbounded strands hardness`
   → A-IV, A-V, A-VIII, A-I and a 2023 DNA 29 paper on scaffolded systems (title only); **no** bin-packing /
   3-partition reduction for multi-strand stacking or nearest-neighbour energies.
4. `"nearest neighbour model" OR "nearest neighbor model" multi-stranded MFE "NP-hard" OR "NP-complete" unpseudoknotted unbounded number of strands proof 2026 Shalaby Woods hardness nearest neighbour`
   → A-II ("Positive results are proven in the nearest neighbour model studied here, negative/hardness
   results in the simpler base pair matching (BPM) model"), A-IV, A-V, A-III; **no** proof of hardness in the
   nearest-neighbour model found.

Searches by the referee (REV-0001, Task 4; ten web searches, a Consensus search, and the contents of the
DNA 32 (2026) proceedings volume): no proof of hardness in the nearest-neighbour model found; [DSW] Table 1
says the hardness results "are conjectured to hold in the more complex NN model", and A-II (23 Nov 2026)
still describes them as BPM-only.

Consequence for CX-T1–T4, CX-T15: the result is **apparently unpublished**.  The question is listed as open in
A-I (2025) and the hardness results are still described as BPM-only in A-II (Nov 2026).  The reduction is
Lyngsø's bin-packing reduction for single-strand pseudoknotted BPS (A-VI), which A-I adapts for counting (its
Theorem 32), with the `C`-runs cut into separate strands; that the idea then works without pseudoknots, for
every nearest-neighbour energy function satisfying (H0), (H1), (H2′), is the step we add.  The closest
multi-strand precedent is A-III Theorem 19 (triplet repeats, a base-pair/multiloop/association model, several
complexes).  A failure to find the result is not proof of novelty; A-XIII could not be inspected.

Not yet searched: follow-ups to A-II (it is three days old); approximation complexity of the multi-strand
partition function.

## §B  Phylogenetic networks and quartet distances

| # | source | how inspected (date) | what it establishes for us |
|---|---|---|---|
| B-I | Holtgrefe, Allman, Baños, van Iersel, Moulton, Rhodes, Wicke, *Distinguishing Phylogenetic Level-2 Networks with Quartets and Inter-Taxon Quartet Distances*, Bull. Math. Biol. 2025, doi:10.1007/s11538-025-01549-4 | arXiv:2507.17308v2, **read in full** (2026-11-26) | definitions; Theorem 4.7 (level-2 bloblets); conjectures B1, B2; open problem B3 |
| B-II | VibeMathed entry "All-level NANUQ circularity and exact displayed-split support" (https://vibemathed.com/problem/all-level-nanuq-circularity-and-exact-displayed-split-support), submitted 30 Sep 2026 | public HTML page fetched and **read in full** (2026-11-26).  The linked repository (github.com/Sodelin/…, commit `cba23504…`, directory `research/nanuq-all-level-2026-09-29/`) was **not inspected**: this session is not authorised to read third-party repositories (attach request denied 2026-11-26) | an *unreviewed* claim of a computer-assisted proof of B1 and B2 at every level and for any number of blobs, with exact support; mentions a "six-label reduction", "exact finite certificate", "composition identity", a parameter domain for a "four-score family" (relevant to B3), and that "planarity cannot be dropped for exact support".  Its verification paragraph says that "two implementations cover 84,076 plane-tree and duplication instances, 122 distinct quartet systems and 24,667 anchor coefficients"; **`122 = 1 + 3 + 16 + 102 = |𝒜_3| + |𝒜_4| + |𝒜_5| + |𝒜_6|`** (noticed by our referee, REV-0002 finding 2; the sentence re-read by us in the saved page).  So the method — a six-leaf reduction, plane trees with duplicated leaves, composition — very probably coincides with ours (CX-T5, CX-T6, CX-T9).  Nothing on the page concerns non-galled networks (our CX-T7) or sharpness (CX-T8) |
| B-III | *Encoding level-3 semi-directed phylogenetic networks by quarnets and quinnets*, arXiv:2610.07855 | PDF downloaded; **not yet read** | — |
| B-IV | Chepoi, Fichet, *A note on circular decomposable metrics*, Geom. Dedicata 69 (1998) | **not read**; used through B-I Prop. 2.8 | Kalmanson ⇔ circular decomposable; split weights `α_ij` |
| B-V | Allman, Baños, Rhodes, *NANUQ*, Algorithms Mol. Biol. 14 (2019) | **not read**; known through B-I | level-1 case |
| B-VII | Weisstein, E. W., "NANUQ Distance", MathWorld, https://mathworld.wolfram.com/NANUQDistance.html ("Last Updated: Wed Nov 25 2026") | page fetched on 2026-11-26 through a page-reading sub-agent; **its report read, not the page itself** (short quotations only) | a secondary source: the definition of B-I; the theorem of B-I for level-2 networks with one non-trivial blob; the claim B-II, described as a "computer-assisted project" whose "complete theorem had not been formalized in Lean or independently reviewed by a specialist" as of 1 Oct 2026.  Three references (B-V, B-I, B-II).  According to the report the page says nothing on networks that are not galled, on counterexamples, on the necessity of a hypothesis, on "Kalmanson", on sharpness or forbidden configurations, or on the parametric family |
| B-VIII | K. T. Huber, L. van Iersel, M. Jones, V. Moulton, L. Veenema-Nipius, *When are quarnets sufficient to reconstruct semi-directed phylogenetic networks?*, arXiv:2408.12997 (v1 of 23 Aug 2024 titled *Encoding Semi-Directed Phylogenetic Networks with Quarnets*; v3 of 3 Aug 2025) | **found by the referee of COMPLEXITY-REV-0005**, who read §4 and Lemma 4.2 with its proof (v3); abstract page and HTML of v3 fetched by a page-reading sub-agent of ours on 2026-11-26 (its report read: title, authors, Lemma 4.2 verbatim, the case distinction of the proof; the figure not seen) | Lemma 4.2: "The semi-directed level-2 generators are as pictured in Figure 8" — (a) one reticulation at an end vertex of the theta graph and one at an interior vertex of a path, (b) two reticulations at interior vertices of two different paths.  This is the dichotomy of our Lemma C (nested / galled kind), which we had stated without a source.  The paper proves that semi-directed binary level-2 networks are encoded by their quarnets and level-3 networks are not; nothing on the NANUQ metric |
| B-VI | Allman, Baños, Rhodes, Wicke, *NANUQ⁺: A divide-and-conquer approach to network estimation*, Algorithms Mol. Biol. 20:14 (2025), doi:10.1186/s13015-025-00274-w | published HTML fetched (2026-11-26); **read: the section "Quartet distances" (Definition 3.1, Lemmas 3.2–3.3, Definition 3.11, Theorem 3.14) and the appendix paragraph on the NANUQ distance**; the rest skimmed | the parametric family `ρ = (ρ_c,ρ_s,ρ_a,ρ_o)`; Modified NANUQ `(½,1,½,1)`; the authors state that they "do not make claims as to whether distances other than the NANUQ one fit any particular combinatorial structure in a precise sense" |

Searches (2026-11-26, "extended" mode):
1. `"NANUQ" metric "circular decomposable" level-3 OR "level-2" outer-labeled planar galled networks conjecture 2026` → B-I, B-II, B-III; no peer-reviewed or arXiv resolution of B1/B2 found.

2. `NANUQ distance "not circular decomposable" OR "fails" non-galled "outer-labeled planar" level-2 network counterexample quartet distance Kalmanson "galled" necessary`
   → B-I (arXiv, journal, PMC), a *Correction* to B-I dated 2026-01-14 (a figure; PMC12804282, title only),
   the NANUQ and NANUQ⁺ papers; **nothing** on whether "galled" is necessary and no non-galled example.

3. (2026-11-26, about 20:15 UTC, "standard" mode; done before registering CX-T26)
   `NANUQ metric circular decomposable Kalmanson outer-labeled planar network conjecture level-2 quartet distance split weights`
   and `"NANUQ" distance "circular decomposable" OR "Kalmanson" phylogenetic network non-galled counterexample 2026`
   → B-I (arXiv v1, v2, journal, a university repository copy), the Correction, the NANUQ papers, and a
   MathWorld page (B-VII below).  **Nothing** on a sharp class, on forbidden six-leaf configurations, on
   3-splits, or on networks that are not galled.

Searches by the referee (REV-0002; nine web searches and four page fetches, 2026-11-26): (i) no proof or
disproof of the Section 6 conjectures of B-I other than B-II — nothing on arXiv or in a journal, no follow-up
in the first author's publication list, B-III only cites NANUQ⁺; (ii) nothing on the necessity of "galled" or
on a non-galled counterexample; (iii) NANUQ⁺ proves statements for sunlets only; the 2026 Correction to B-I
concerns an omitted figure panel.

Consequences for novelty statements: CX-T6 (and with it the method, CX-T5, CX-T9) is to be described as **an
independent rediscovery, in all likelihood, of the unreviewed claim B-II, whose proof we have not seen**; no
priority is claimed for it.  For CX-T7 (galled cannot be dropped), CX-T8 (sharpness), CX-T26 (the sharp
class for "Kalmanson" alone, as a forbidden six-leaf pattern), CX-T27 (the classification for level 2:
nested blobs, critical splits and their weights — **except** the dichotomy of Lemma C, which is B-VIII,
Lemma 4.2) and CX-T13 (parametric family, in our extension) no prior art was found, by us or by the referee
of COMPLEXITY-REV-0005 (13 further queries on NANUQ / quartet distances for non-galled networks, follow-ups of
B-I in 2026, classifications of outer-labeled planar level-2 networks, forbidden six-taxon configurations for
Kalmanson metrics); a failure to find it is not proof of novelty.  Since B-II names a
"six-label reduction" and we have not seen its text, a statement like Corollary 5′ may well be in it.

---

## §C  Ising ground sets = faces of the cut polytope (question E-C1 of the Ensemble division)

All texts were downloaded by the referee of COMPLEXITY-REV-0004 on 2026-11-26; "we" read the pages named
from those downloads on the same day.

| # | source | how inspected | what it establishes for us |
|---|---|---|---|
| C-I | M. Laurent, S. Poljak, *On the facial structure of the set of correlation matrices*, CWI report BS-R9501 (1995); journal version SIAM J. Matrix Anal. Appl. 17 (1996) (reference as given by the referee) | **pp. 13–14 of the report read by us** as page images (Theorem 4.1 with proof; Theorem 4.2 with proof up to Claim 4.3); abstract and p. 15 by the referee | Theorem 4.2 is our Corollary 7 (CX-T18): `f_h` linearly independent and `{f_h∘f_h'} ∪ {𝟙}` linearly independent ⇒ `conv{f_h f_h^T}` is a face of the elliptope, hence of the cut polytope.  Theorem 4.1: such a face is a simplex and `C(k,2) ≤ n − 1`.  Faces of the elliptope are given by kernels ⇒ our Proposition 5 |
| C-II | J. Tropp, *Simplicial faces of the set of correlation matrices*, arXiv:1801.00749v1 | **pp. 1–6 read by us** (abstract, §1, §2: Facts 2.5–2.8, 2.12, Theorems 2.9–2.11); §§1–3 by the referee | `r` uniformly random sign vectors generate a simplicial face of the elliptope with probability `≥ 1 − r² exp(−n/r²)`; no simplicial face of the elliptope is generated by more than about `√(2n)` vertices; "Fact 3.1", a sufficient condition "due to Laurent & Poljak", is the engine |
| C-III | M. Deza, M. Laurent, *Applications of cut polyhedra*, LIENS-92-18 | by the referee (§2.5, rigidity examples, Table 1, equidistant metric); **not by us** | ℓ1-rigidity = lying on a simplicial face of the cut cone; the path metric of `K_4` is not rigid; isometric subgraphs of the hypercube are rigid |
| C-IV | A. Deza, M. Deza, LIENS-95-1 | by the referee (§1, §3); **not by us** | face numbers of the cut polytope on five nodes; `f_3 = 1780` (we recomputed that number) |
| C-V | N. Wang, J. Rauh, H. Massam, arXiv:1603.04843 | by the referee (introduction, §2.2); **not by us** | the decision problem as recognition of facial sets (existence of the MLE); no hardness statement |
| C-VI | positive 1-in-3-SAT is NP-complete (Schaefer 1978; Garey–Johnson LO4) | **from memory**, no text consulted | used in CX-T29 |
| C-VII | projection (pseudo-inverse) rule of associative memories (Personnaz–Guyon–Dreyfus 1985; I. Kanter, H. Sompolinsky, *Associative recall of memory without errors*, Phys. Rev. A 35 (1987) 380) | **from memory**, no text consulted; the reference to Kanter–Sompolinsky as given by the referee of REV-0005 and by C-IX | the energy of CX-T28; "the sign vectors of the span are ground states"; origin of the question answered by C-VIII |
| C-VIII | A. M. Odlyzko, *On subspaces spanned by random selections of ±1 vectors*, J. Combin. Theory Ser. A 47 (1988) 124–133 | **not opened**: the author's PDF returned HTTP 503 and the publisher's page 403, for the referee of REV-0005 and for our page-reading sub-agent (2026-11-26); title and pages as given by the referee; the statement as quoted in C-IX, Theorem 1.1 | the probability that the span of `p` uniform sign vectors in dimension `n` contains another sign vector is `4·C(p,3)(3/4)^n + O(p⁴(5/8)^n) + O((7/10)^n)` for `p ≤ n − 10n/ln n`.  **Supersedes our Proposition 13′** (CX-T28) |
| C-IX | A. A. Irmatov, *On linear-combinatorial problems associated with subspaces spanned by {±1}-vectors*, arXiv:2405.05082v1 (8 May 2024) | abstract and pp. 1–2 by the referee of REV-0005; abstract page and HTML fetched by a page-reading sub-agent of ours (its report read: Theorems 1.1 and 1.2 verbatim) | Theorem 1.2: the same asymptotics for all `p ≤ n − 1`, with error `O((5/8 + o(1))^n)` uniformly in `p`; says the question comes from Kanter and Sompolinsky |
| C-I (addition) | Laurent–Poljak, the report of C-I, Theorems 2.7 and 2.9, Example 3.8 | pp. 1–7 and 12–15 as page images **by the referee of REV-0005; not by us** | Theorem 2.7: the faces of the elliptope are `{X : ker X ⊇ W}`; Theorem 2.9: the normal cone is `{D − M : D diagonal, M ⪰ 0, ⟨M, A⟩ = 0}`.  Together they give our Proposition 13 (CX-T28) in two lines |

Searches by the referee without usable results beyond snippets: complexity of ℓ1-rigidity; complexity of
recognising faces of the cut polytope; Hopfield projection rule; design of Ising ground sets.  Our own
single search before the review is recorded in the first version of `ISING_GROUND_SETS.md` §7.

Consequences for novelty statements: CX-T16 (twin reduction, fixed `K`) answers the division's question and
is elementary; CX-T17 is **known** apart from the singleton family as stated; in CX-T18, Proposition 5 and
Corollary 7 are **known**; **CX-T28 is known in substance** (Proposition 13 from C-I, Theorems 2.7 and 2.9;
Proposition 13′ is superseded by C-VIII and C-IX) — until COMPLEXITY-REV-0005 we listed it under "no source
found"; for Theorem 6, Lemma 9, CX-T19 and CX-T29 no source was found, which is not evidence of novelty.

---

## §D  Unit vectors in a fixed dimension maximising a quadratic form (vector Max-Cut; chain geometry, question C1 of the Geometry division)

Searches and readings of 2026-11-26.  **Order of events, recorded because it matters:** the proofs of
`CHAIN_GEOMETRY_HARDNESS.md` §2 (about 21:30 UTC) and §2a (about 22:35 UTC) were found first; searches 1–2 (before
§2) found nothing; searches 3–4 (after §2a, before anything was written into the repository) found D-I and D-II,
which contain the hardness statements.  For about an hour the lifting of §2a was taken for a possible proof of
an open conjecture of Lovász.

| # | source | how inspected | what it establishes for us |
|---|---|---|---|
| D-I | J. Kallaugher, O. Parekh, K. Thompson, Y. Wang, J. Yirka, *Complexity classification of product state problems for local Hamiltonians*, arXiv:2401.06725v2 (6 Jan 2025; conference version reported as ITCS 2025) | abstract page and ar5iv HTML through a page-reading sub-agent; **its report read, not the paper**; the HTML was truncated after about 40 000 of 169 000 characters (abstract and §1 covered; quotations of at most 125 characters) | Theorem 1.5 "MC_3 is NP-complete" (vector Max-Cut in `ℝ^3`, unit weights, by a reduction from 3-colouring); "it has been conjectured by Lovász that MC_k is NP-complete for all constants k≥1, in [Lov19, p. 236] and earlier, no proof has been given for any k>1"; "the first published proof that MC_k is NP-complete for some k>1"; open question "Can our proof be generalized to other values of k?"; a complete classification of product-state problems for 2-local Hamiltonians with couplings of both signs (the Heisenberg interaction gives exactly the classical Heisenberg ground-state problem); a footnote that an unpublished proof by Wright existed earlier.  **Contains our Theorem 1 (CX-T32)** |
| D-II | S. Piddock, *Quantum Max-Cut is NP hard to approximate*, arXiv:2510.07995v1 (9 Oct 2025; 19 pages; no journal reference) | abstract page and HTML of v1 through a page-reading sub-agent, which reports having read the full text; **its report read, not the paper** | Theorem 3: "There is a PTAS reduction from Max-Cut_k to Max-Cut_{k+1}.  Therefore Max-Cut_k is APX-complete for all (constant) k≥1" (unweighted graphs); gadgets: for every vertex and every incident edge copy a unit triangle with the vertex, and a constant-degree bipartite expander that pins the reference vectors; the triangle forces the angle `2π/3`, not a right angle ("almost any gadget will do, as long as it is not a bipartite graph"); "no other hardness results are known for k≠1,3".  **Contains the hardness statement of our Proposition 1a, with approximation.**  Our lifting uses a different gadget (a triangle with multiplicities 3, 4, 5, which forces a right angle; a blow-up; many parallel poles) and gives an exact identity instead of an approximation-preserving reduction |
| D-III | M. E.-Nagy, M. Laurent, A. Varvitsiotis, *Complexity of the positive semidefinite matrix completion problem with a rank constraint*, arXiv:1203.6602 | ar5iv HTML through a page-reading sub-agent (about 40 000 of 61 000 characters: abstract, §§1–3; Theorem 4.2 and §5 from a summary only); **its report read** | membership in the rank-`k` elliptope `E_k(G)` is NP-hard for every fixed `k ≥ 2` (Theorems 3.2, 3.3), also in its convex hull; "It is believed that linear optimization over conv E_k(G) is also hard for any fixed k (cf., e.g., the quote of Lovász …)"; the hardness of linear optimisation was open there.  This is the source the Geometry division cited in GEOMETRY-REQ-0004 |
| D-IV | L. Lovász, *Graphs and Geometry*, AMS Colloquium Publications 65 (2019), p. 236 | **not read**; known through D-I and D-II | the conjecture |
| D-V | J. Briët, F. de Oliveira Filho, F. Vallentin, *The positive semidefinite Grothendieck problem with rank constraint* (2010) and *Grothendieck inequalities for semidefinite programs with rank constraint* (2014) | **from memory** (as in COMPLEXITY-RES-0002); the first is cited by D-I and D-II for the approximation algorithm of vector Max-Cut | constant approximation ratios for positive semidefinite objectives; unique-games hardness of doing better |
| D-VI | M. Grötschel, L. Lovász, A. Schrijver, *Geometric Algorithms and Combinatorial Optimization* (1988) | **from memory**, no text consulted | the polynomial-time equivalence of weak membership and weak optimisation for centred well-bounded convex bodies — used for Corollary 5 of the chain note.  **It is polynomial in the encoding length of the accuracy and therefore gives Corollary 5 only for an accuracy written in binary** (REV-0006, finding 1; we had claimed accuracy `1/poly` on it) |
| D-VIa | Y.-K. Liu, thesis (2007), Proposition 2.8, as used by S. Gharibian, *Strong NP-hardness of the quantum separability problem*, Quantum Inf. Comput. 10 (2010) 343–360, arXiv:0810.4507 | **not read by us**; the referee of REV-0006 read a model-written summary of the ar5iv HTML of Gharibian's paper (abstract, the proposition with its formula, the remark on the Yudin–Nemirovskii link); neither the thesis nor the book D-VI was opened by anyone | for `B(p,r) ⊆ K ⊆ B(0,R) ⊂ ℝ^m`: weak optimisation with error `ε` reduces to weak membership with error `r³ε³/(2¹³·3³·m⁵·R⁴(R+r))` — a polynomial loss, which gives Corollary 5 for accuracy `1/poly`.  Until someone reads the source, that half of Corollary 5 is conditional on a statement known at second hand |
| D-VII | distance geometry of protein-like chains: J. Saxe (1979); C. Lavor, L. Liberti, N. Maculan and co-authors (the discretizable molecular distance geometry problem) | search summaries only | NP-hardness of the *feasibility* problem for exact distances; a different problem |
| D-VIII | **fixed-angle chains ("freely rotating chains")**: M. Soss, G. Toussaint, *Geometric and computational aspects of polymer reconfiguration*, J. Math. Chem. 27 (2000) 303–318; E. Demaine, S. Eisenstat, *Flattening fixed-angle chains is strongly NP-hard*, WADS 2011; E. Demaine, H. Ito, J. Lynch, R. Uehara, arXiv:2212.12450; N. Benbernou, J. O'Rourke, *On the maximum span of fixed-angle chains*, CCCG 2006, arXiv:0801.0258; C. Borcea, I. Streinu, *Extremal reaches in polynomial time*, SoCG 2011 | **found by the referee of REV-0006, not by us**; search summaries and one abstract page (arXiv:2212.12450); full texts opened by nobody | flattening and the minimum / maximum flat span of a fixed-angle chain are NP-hard (strongly; also for equal lengths); the maximum span in space is polynomial for equal angles; the largest and smallest end-to-end distance of a chain in space with fixed lengths and angles are polynomial (Borcea–Streinu) — this is CHAIN(θ) with the single datum `c_{1n} = ±1`.  According to the referee none contains Theorem 3 of the chain note (they treat planar configurations, or a single pair) |

Searches (WebSearch, 2026-11-26): (1) classical Heisenberg / vector spin glass ground state NP-hard — the Ising case
(Barahona; Bachas 1984 by title) only; (2) chain conformation, squared distances, fixed bond angle, NP-hard —
distance-geometry feasibility only; (3) `"rank constraint" Grothendieck problem unit vectors fixed dimension NP-hard`
— the thesis chapter of Briët and D-I among the results; (4) `"rank-constrained" elliptope NP-hard linear
optimization fixed rank` — D-III; (5) `"Vector Max-Cut" OR "rank-k Max-Cut" NP-hard every fixed k Lovász conjecture`
(extended mode) — D-II.

Consequences for novelty statements: **CX-T32 is known** as a hardness statement (D-I for dimension 3, D-II for
every dimension and with approximation); ours are the translation to chains (elementary), two short proofs, and
the corollary on realizability, for which no search was made beyond the above.  For CX-T33 (fixed bond angles;
short range) no source was found in a search that was not aimed at it; both statements are elementary.

*Added after REV-0006 (2026-11-27).*  The referee's additional searches (results read as summaries): Bachas 1984
(three-dimensional Ising only; no older hardness result for vector spins found); the rank-constrained
Grothendieck problem (nothing further); the fixed-angle chain literature (D-VIII — **which our search (2) had
missed**: it is filed under "fixed-angle chain", "polymer reconfiguration", "linkage", not under "bond angle");
Kapovich–Millson on spherical polygonal linkages (abstract only; the closing condition for spherical polygons, of
which the lemma of §3 is a special case, is quoted by the referee from memory); the lifting `k → k+1`, the
3-4-5 right angle and the exact identity (nothing found); membership in the convex hull of the rank-constrained
elliptope (D-III only).  Details the referee read on the arXiv pages of D-I and D-II: D-I's Theorem 1.5 is a
promise version (completeness `m(11+2√3)`, gap of order `m^{-2}`), with a footnote crediting an earlier
unpublished proof for product states of Quantum Max-Cut to J. Wright (2022); D-II proves inequalities only, no
exact identity, one arXiv version, no journal reference.  CX-T33 remains without a located source; a search
that fails proves nothing.

**Lesson (the same as in §A-III(j) and §C, for the third time in one day):** search for the nearest classical
formulation of a statement — here "vector Max-Cut", "rank-constrained Grothendieck problem" — *before* working
on a proof, not after.

