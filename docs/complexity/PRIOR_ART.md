# Prior-art register (complexity division)

For every source: what it is, **how it was inspected**, and what we take from it.  "Read in full"
means the complete text was read by the division (from a PDF converted with `pdftotext`); "sections
read" names them; "abstract only" and "search snippet only" mean exactly that.  A failure to find a
result is recorded as a failed search, not as evidence of novelty.

## §A  Nucleic-acid folding complexity

| # | source | how inspected (date) | what it establishes for us |
|---|---|---|---|
| A-I | Ducloz, Shalaby, Woods, *Algorithmic Hardness of the Partition Function for Nucleic Acid Strands*, DNA 31 (2025), doi:10.4230/LIPIcs.DNA.31.1 | conference PDF from drops.dagstuhl.de, **read in full** (2026-11-26); arXiv:2506.19756v1 downloaded, appendix A not yet read | definitions; reduction map; #P-hardness of PF in BPS (1 strand, pseudoknots) and BPM (unbounded strands) **with the temperature/magnification as part of the oracle's input**; five open questions (A1–A5) |
| A-II | Shalaby, Woods, *One partition function call to rule them all*, arXiv:2611.27945v2 (23 Nov 2026) | arXiv PDF, **§§1–3 read** (2026-11-26); §§4–7 skimmed for statements only | resolves A2 (magnifiable PF with rotational symmetry, `O(N³(c−1)!)`); MFE and #SSEL from one call; four new open questions (A5–A7) |
| A-III | Boehmer, Berkemer, Will, Ponty, *RNA Triplet Repeats: Improved Algorithms for Structure Prediction and Interactions*, WABI 2024, doi:10.4230/LIPIcs.WABI.2024.18 | conference PDF, **§§1, 2, 4, 6 read** (2026-11-26); appendix not read | subset dynamic programme `O(3^m n³)` for multi-strand MFE in a base-pair model without symmetry (Thm 14); remark on PF with per-symmetry terms (Rem. 15); XP algorithm in the number of distinct strands (Thm 16); NP-completeness for triplet repeats (Thm 19); polynomial "strand soup" algorithm (Thm 20) |
| A-IV | Shalaby, Woods, *An efficient algorithm to compute the minimum free energy of interacting nucleic acid strands*, ICALP 2025, arXiv:2407.09676 | arXiv PDF downloaded; **not yet read** beyond what A-I/A-II quote | MFE with rotational symmetry in `O(N⁴(c−1)!)` |
| A-V | Condon, Hajiaghayi, Thachuk, *Predicting minimum free energy structures of multi-stranded nucleic acid complexes is APX-hard*, DNA 27 (2021), doi:10.4230/LIPIcs.DNA.27.9 | conference PDF, **§1, §2 (first page), §7 read** (2026-11-26); the reduction itself not read | NP-/APX-hardness of multi-strand unpseudoknotted MFE in the base-pair model ("with at least k base pairs"), "whether or not rotational symmetries are accounted for"; about richer models only the sentence "it would seem unlikely that the prediction problem becomes easier if the energy model is more sophisticated" — no stacking or loop-based multi-strand reduction |
| A-VI | Lyngsø, *Complexity of pseudoknot prediction in simple models*, ICALP 2004 | **not read**; known through A-I App. B.3 | NP-hardness of pseudoknotted single-strand MFE in BPS |
| A-VII | Dirks, Bois, Schaeffer, Winfree, Pierce, *Thermodynamic analysis of interacting nucleic acid strands*, SIAM Review 49 (2007) | **not read**; known through A-I, A-II | multi-strand PF, representation theorem, symmetry correction `Q(π) = Q̃(π)/v(π)` |
| A-VIII | Demaine, Gomez, Grizzell, Hecher, Lynch, Schweller, Shalaby, Woods, *Domain-based nucleic-acid minimum free energy: algorithmic hardness and parameterized bounds*, DNA 30 (2024), doi:10.4230/LIPIcs.DNA.30.2 | conference PDF, **abstract, §1 and Table 1 read** (2026-11-26); proofs not read | domain-level results only: NP-completeness for 2-domain strands, ETH lower bounds `2^{Ω(|S|)}` in the number of strands at the domain level (their Thms 16, 17), P/P-hardness for 1-domain strands; nothing on base-level stacking/NN energies |

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

Consequence for CX-T1–T4: "we found no proof in print of NP-hardness of multi-strand MFE for stacking or
nearest-neighbour energies; the question is listed as open in A-I (2025) and the hardness results are still
described as BPM-only in A-II (Nov 2026)".  The reduction is a variant of Lyngsø's bin-packing reduction for
single-strand pseudoknotted BPS (A-VI), which A-I adapts for counting (its Theorem 32); that the same idea
works without pseudoknots once the items are separate strands is the (small) step we add.  Not yet done:
reading A-VI itself and Dirks et al. (A-VII) for the exact loop conventions; a search of the 2022–2026
DNA/ICALP/WABI proceedings by title.

Not yet searched: follow-ups to A-II (it is three days old); approximation complexity of the multi-strand
partition function.

## §B  Phylogenetic networks and quartet distances

| # | source | how inspected (date) | what it establishes for us |
|---|---|---|---|
| B-I | Holtgrefe, Allman, Baños, van Iersel, Moulton, Rhodes, Wicke, *Distinguishing Phylogenetic Level-2 Networks with Quartets and Inter-Taxon Quartet Distances*, Bull. Math. Biol. 2025, doi:10.1007/s11538-025-01549-4 | arXiv:2507.17308v2, **read in full** (2026-11-26) | definitions; Theorem 4.7 (level-2 bloblets); conjectures B1, B2; open problem B3 |
| B-II | VibeMathed entry "All-level NANUQ circularity and exact displayed-split support" (https://vibemathed.com/problem/all-level-nanuq-circularity-and-exact-displayed-split-support), submitted 30 Sep 2026 | public HTML page fetched and **read in full** (2026-11-26).  The linked repository (github.com/Sodelin/…, commit `cba23504…`, directory `research/nanuq-all-level-2026-09-29/`) was **not inspected**: this session is not authorised to read third-party repositories (attach request denied 2026-11-26) | an *unreviewed* claim of a computer-assisted proof of B1 and B2 at every level and for any number of blobs, with exact support; mentions a "six-label reduction", "exact finite certificate", "composition identity", a parameter domain for a "four-score family" (relevant to B3), and that "planarity cannot be dropped for exact support" |
| B-III | *Encoding level-3 semi-directed phylogenetic networks by quarnets and quinnets*, arXiv:2610.07855 | PDF downloaded; **not yet read** | — |
| B-IV | Chepoi, Fichet, *A note on circular decomposable metrics*, Geom. Dedicata 69 (1998) | **not read**; used through B-I Prop. 2.8 | Kalmanson ⇔ circular decomposable; split weights `α_ij` |
| B-V | Allman, Baños, Rhodes, *NANUQ*, Algorithms Mol. Biol. 14 (2019); Allman, Baños, Rhodes, Wicke, *NANUQ⁺*, Algorithms Mol. Biol. 20 (2025) | **not read**; known through B-I | level-1 case; the parametric family of B3 |

Searches (2026-11-26, "extended" mode):
1. `"NANUQ" metric "circular decomposable" level-3 OR "level-2" outer-labeled planar galled networks conjecture 2026` → B-I, B-II, B-III; no peer-reviewed or arXiv resolution of B1/B2 found.

2. `NANUQ distance "not circular decomposable" OR "fails" non-galled "outer-labeled planar" level-2 network counterexample quartet distance Kalmanson "galled" necessary`
   → B-I (arXiv, journal, PMC), a *Correction* to B-I dated 2026-01-14 (a figure; PMC12804282, title only),
   the NANUQ and NANUQ⁺ papers; **nothing** on whether "galled" is necessary and no non-galled example.

Consequences for novelty statements: any statement of ours about B1/B2 must say "independently of,
and after, the unreviewed claim B-II, whose proof we have not seen".
