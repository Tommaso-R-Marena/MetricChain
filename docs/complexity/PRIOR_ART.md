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
nested blobs, critical splits and their weights) and CX-T13 (parametric family, in our extension) no prior
art was found; a failure to find it is not proof of novelty.  Since B-II names a
"six-label reduction" and we have not seen its text, a statement like Corollary 5′ may well be in it.
