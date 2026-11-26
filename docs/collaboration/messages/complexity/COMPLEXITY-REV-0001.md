Message ID:                  COMPLEXITY-REV-0001
Message type:                Internal adversarial review of docs/complexity/STRANDS_NN_HARDNESS.md (NP-/#P-hardness of multi-strand folding in the nearest-neighbour model)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          All divisions (for the record); the division itself (findings to process)
Date and time (UTC):         2026-11-26 18:40
Priority:                    High
Status:                      Review received; disposition of every finding recorded at the end of this file
Relevant source commit:      22cf1a6 (the reviewed file as of that commit)
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T1–CX-T4, CX-T14, CX-V1
Related message/request IDs: COMPLEXITY-MSG-0001, COMPLEXITY-MSG-0002

Scientific context:
First internal adversarial review of the hardness note (problem A1 of docs/complexity/OPEN_PROBLEMS.md).
Verdict of the referee: "correct with gaps" — no critical finding; four major findings (a false framing sentence
about physical parameter sets, a false remark on coaxial stacking, missing attribution, an unsupported step in the
conditional ETH corollary) and eight minor ones.

What this review is and is not:
The referee was a separate AI agent instantiated by this division with an adversarial brief ("try to break the
claimed theorems"; re-derive, recompute with code that imports nothing of ours, search for prior art).  It had no
access to our reasoning, only to the files of this branch.  **This is an internal AI review.  It is not
independent academic peer review**, and the results it covers remain unrefereed in the sense of the collaboration
README.  The report is reproduced verbatim below; the referee's code and logs are preserved in
`experiments/complexity/reviews/` (paths in the report that point to a session scratch directory refer to those
copies).

---------------------------------------------------------------------------------------------------------------
REPORT (verbatim)
---------------------------------------------------------------------------------------------------------------

# Referee report: `/home/user/MetricChain/docs/complexity/STRANDS_NN_HARDNESS.md`

Reviewed at HEAD `22cf1a6`. The file changed during the review: §5 gained "Corollary 5" (ETH bound), which I audited too. I wrote nothing under `/home/user/MetricChain/`.

## Verdict: correct with gaps

- **Theorem 1, Corollary 2 (hardness), Theorem 3, Corollary 4(i): correct.** I could not break them by hand or by computation.
- **Corollary 4(ii):** correct at the rigour of DSW Thm 22 (exact real-valued oracle).
- **Corollary 5 (new):** its cited fact (i) is not established at the cited source in the form used.
- No CRITICAL finding. The gaps are a false framing sentence, a false remark, missing attribution, and unargued membership claims.

## Findings

1. **MAJOR, lines 12–15, 81, 268: "(H0)–(H2) is the sign pattern of every physical parameter set" is false.**
   - (H2) fails for the Turner-2004 single-nucleotide bulge rule as documented in NNDB (initiation 3.81, special C bulge −0.9, plus the base-pair stack, minus RT ln(states)). Between G–C pairs in homopolymer runs this gives about −1.0 kcal/mol (C bulge) and −0.1 (G bulge). Both loops occur in `I(a,m,B)`.
   - It also fails for the Andronescu-2007 file shipped with ViennaRNA: the 1×1 loop G/C between G–C pairs is −0.04.
   - (H0) fails for any table used with dangles or coaxial stacking, which §6 concedes.
   - Fix: replace (H2) by (H2′): there is δ>0 with g(f) ≥ σ·ι(f) + δ for every bulge/interior loop f, where ι(f) ≥ 1 is the number of item covalent bonds on f. g(f) ≥ σ + δ suffices.
   - Proof is two lines: Σ_f ι(f) = M, so Σ_f g(f) − σM = Σ_f (g(f) − σι(f)); stacks give 0, exterior loops |σ|ι ≥ 0, the rest ≥ δ. Part 2 becomes MFE ≥ σM + min(δ,|σ|) + nΔG_assoc.
   - Checked: the thresholds are exact. Bulge −0.99|σ| works, −|σ| ties, −1.01|σ| fails; item-side bulges and interior loops work at −1.99|σ| and fail at −2.01|σ|.
   - All five ViennaRNA parameter files satisfy (H2′) with margin ≥ 2.9 kcal/mol on the 210 loop types that occur.

2. **MAJOR, lines 178–180 (Remark 3) and 265–266 (§6.1): "with coaxial stacking as strong as stacking the reduction fails" is false in general.**
   - It holds only when bulges over the separator A are free (e.g. stack-only).
   - My claim: let flush nicked stacks (two chords, template bond, nick, no unpaired base) have energy x, other exterior loops 0, and all bulge/interior loops ≥ γ ≥ 0. For B ≥ 2 and n ≥ m, tilings have E_til = σM + x(n−m), and MFE = E_til iff packable whenever x > σ − min(|σ|, γ).
   - Proof sketch: E − E_til = |σ|L + P − (|x|−|σ|)(m−1−z), with L the template GG bonds not on a stack or flush face, P the bulge/interior energy, z the item–item nicks on non-flush faces. Each separator A either has its own nicked face, costs a fully unpaired block (≥ 1 loose bond), or sits in a bulge/interior loop (≥ γ).
   - Checked: threshold exactly x > σ − min(|σ|,γ) for γ/|σ| ∈ {0, .1, .3, .6, .99, 1, 1.5} on 112 instances. The sketch is mine and not written out in full.
   - Fix: restrict Remark 3 to γ = 0, or add the extension with threshold k = σM + x(n−m) + nΔG_assoc.

3. **MAJOR (attribution), lines 24–26: the paper never says whose gadget this is.**
   - The instance is Lyngsø's 2004 bin-packing strand, as reused in DSW Thm 32 / App. B.3 ("We proceed exactly as Lyngsø": `C^{w(a_1)}A…AAA G^B A G^B…`), with the C-runs cut into separate strands. Only `PRIOR_ART.md` mentions this, and it records Lyngsø as unread.
   - Boehmer et al. WABI 2024 Thm 19 is the closest multi-strand precedent and is not discussed: a strongly NP-hard number problem ("Summing Triples") mapped to unary strands `(CAG)^{s_i}` in a non-BPM model with several complexes.
   - Fix: cite both in the paper and word novelty as "apparently unpublished".

4. **MAJOR for Corollary 5 only, lines 243–256: fact (i) is not what the source proves.**
   - Bansal et al. (Algorithmica 2016) state only "no O(2^{o(q)}|T|^{O(1)}) algorithm for 3-DM", with |T| = 2MN+3M+2M²N(N−1) from Garey–Johnson's reduction. The linear bound is an unproved parenthetical: "using better bookkeeping you can prove that |T|=17M suffices".
   - With |T| = Θ(q⁴) the chain gives only 2^{Ω(c^{1/4})}.
   - Fix: supply a linear-size chain (bounded-occurrence 3-SAT to 3DM with at most three occurrences per element), or weaken or relabel as [C].
   - Step (ii) is fine: 4|T| items, sizes poly(q).

5. **MINOR, lines 165–170: NP membership is unargued.**
   - ΔG contains k_BT·ln R, irrational for R ≥ 2, so "ΔG ≤ k" needs an argument or a restriction to the symmetry-free model. The hardness instances have R = 1.
   - k = σM + nΔG_assoc must be representable; any rational in the gap of width |σ| works.

6. **MINOR, lines 211–222 and 20–22: Corollary 4.**
   - (i) #P membership needs canonical representatives of physical structures. Lemma 31's weights must be polynomially bounded, since strands are unary. This is true for the Garey–Johnson reduction but should be stated.
   - (ii) The Vandermonde step is legitimate but unnecessary: one evaluation at x larger than the number of structures gives N_M = ⌊Z/x^M⌋.
   - The summary sentence claims partition-function hardness more broadly than 4(ii), which is stack-only.

7. **MINOR, lines 81–83: the multiloop hypothesis is vacuous.** All chords of `I(a,m,B)` are pairwise nested, so no face has three or more chords and there are no hairpins. Confirmed: only exterior, stack, bulge and interior faces occur.

8. **MINOR, lines 72–74: cite the question's own source for ΔG_ext = 0.** The DSW full version (arXiv:2506.19756, App. A.2) says "Exterior loops do not contribute to the free energy because by definition [8], ΔG_exterior = 0". Dirks et al. App. B n.3 says the same and adds "We omit details of dangle free energies". `PRIOR_ART.md` lists that appendix as unread.

9. **MINOR, lines 55–57 and 230–239: verification claims are not backed by the committed scripts.**
   - No script passes `check=True`, so Fact 1 was never tested.
   - "Up to 513 120 structures" is wrong; `big_run.log` shows 1 887 888.
   - The physical-ensemble count and R = 1 are untested, and `symmetry_orbits` is unused.
   - Coverage is 18 instances, with no m = 1, no B ≤ 2 and no item longer than a block.
   - "Lean: not formalised yet" is stale. `StackPacking.lean` exists; I compiled a scratch copy without errors, and its axioms are propext, Classical.choice, Quot.sound.

10. **MINOR, lines 138–140:** add one sentence that distinct partners with unit steps cannot reverse.

11. **MINOR, lines 174–177:** DSW Def. 9 read literally (indices in the concatenated strand) counts a stack across a nick. Under that reading with free bulges the instances are trivial. State which reading is used.

12. **MINOR, lines 257–258:** "expected to be polynomial for boundedly many species" is unsupported; label it [C].

## Task 1: definitions audit

- **(a) Nicked loop is a zero-energy exterior loop: yes**, in the formal model of all four papers.
  - Dirks et al.: "all loops containing one nick are exterior loops"; the pseudocode guards interior and multiloop cases by zero nicks.
  - DSW App. A.2, Shalaby–Woods 2611.27945 footnote 19, and the ICALP 2025 paper's Algorithm 1 agree. A stack across a nick is therefore not a stack.
  - Caveat: Dirks and NUPACK add dangles and terminal penalties, omitted from the printed recursions.
- **(b) Connected iff no face has two or more nicks: yes.** Stated by Dirks, proved by me via the dual-graph argument, and 0 mismatches against union-find over all 563.6 M pair sets of the full-enumeration instances.
- **(c) R(S) = 1: yes.** The template species is unique. The maximum R observed was 1 on every instance; my code finds R = 2 and 3 on homodimer and homotrimer controls. #SSEL in Shalaby–Woods is over the physical ensemble, matching Thm 3(2).
- **(d) Fairness of (H0)–(H2):** (H0) is exactly the cited papers' formal model, so the theorem is not about a weaker model in that respect. (H2) as worded excludes NNDB Turner-2004 (finding 1). The energy model is fixed, so "model as input" does not trivialise it.

## Task 2: proof audit

Every step checked; no errors found in:
- stack links are one template bond and one item bond;
- each link lies on exactly one face;
- the a_i = 1 case;
- antiparallel is forced by non-crossing;
- S* is non-crossing and connected, with exactly M stacks, n−m flush faces, m−1 A-faces and 2 terminal faces (0 deviations over 12 842 tilings);
- the NO bound;
- Til, the division by Πμ_s!, and the factors m!·6^m and m!·24^m (e.g. (2,2,3,2,2,3): 432 = 6·2·36; (3,3,3,4,3,3,3,4): 23 040 = 20·2·576).

## Task 3: computation

All code is my own, in `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review1/`; `run_all.sh` reproduces everything.

**Brute force (`enum.cpp`, `test_main.py`): 134 instances, 0 failures.**
- All circular orderings and all non-crossing pair sets (pruned for the 12 starred instances); 413.5 M connected labelled structures; 14 models satisfying (H0)–(H2) each.
- Confirmed: MFE = σM iff packable; MFE ≥ σ(M−1) otherwise; minima are exactly the tilings and number Til; no labelled structure occurs under two orderings.
- Physical count = Til/Πμ_s! on the 131 instances with physical bookkeeping (the three `**` runs skip it).
- Instances as item digits (`*` pruned, `**` pruned without physical-ensemble bookkeeping):

| m, B | YES | NO |
|---|---|---|
| 1, 1–6 | 1; 2 11; 21 111 3; 22 13 112 1111 4; 23 122 11111; 222 123 33 1122 | none |
| 2, 1 | 11 | 2 |
| 2, 2 | 22 112 1111 | 31 4 |
| 2, 3 | 33 1212 111111 321 2211 3111 21111 | 222 42 51 411 6 |
| 2, 4 | 2222 3122 3131 422 44 11222 3311 111122 3221 | 332 53 5111 62 71 521 |
| 2, 5 | 2323 1423 55 4411 12223 22123 11323 3322 4321 111223* 222211* 111133* | 22222 442 334 3331 2224 64 622 73 4222 |
| 2, 6 | 66 3333* 4422* 5133* | 444 552 543 75 |
| 3, 1 | 111 | 21 3 |
| 3, 2 | 222 2211 21111 111111 | 33 321 3111 42 411 |
| 3, 3 | 333 121212 32121 3321 222111 1111122** 2211111** | 22221 2223 441 423 4221 522 3222 |
| 3, 4 | 444 2244* | 543 84 66 3333* |
| 4, 1 | 1111 | 31 22 |
| 4, 2 | 2222 22211 221111 | 332 3311 3221 |
| 4, 3 | 3333* | 444 633 |
| 5, 1 | 11111 | 2111 |
| 5, 2 | 22222 222211 1111222** | 3322 3331 |
| 6, 2 | none | 66 444 |

**Second method (`dp.cpp`, `test_dp.py`): 0 failures.**
- A transfer-matrix DP per ordering agrees with brute force on all 134 instances.
- A further 867 instances (703 YES, 164 NO) pass under 6 models: 71 structured plus 796 random.
- These include 3-PARTITION-shaped (n = 6, 9, 12) and 4-PARTITION-shaped (n = 8, 12) YES and NO cases, e.g. NO (4,4,4,4,4,6; m=2, B=13) and NO (4,4,4,4,4,6,6,6; m=2, B=19).

**Fragility (`fragility.py`, `coax_grid.py`, `fragility_real.py`), 112 instances with mB ≤ 10, threshold E_til.**

| Violation | Result |
|---|---|
| Constant exterior energy | harmless |
| Negative bulge/interior | valid iff g > σ·ι |
| Flush coax x, free bulges | valid iff \|x\| < \|σ\| |
| Flush coax x, bulges ≥ γ | valid iff \|x\| < \|σ\| + min(\|σ\|, γ) |
| Dangles d per adjacency | valid at \|d\| ≤ 0.30\|σ\|, fails at 0.34\|σ\| |

- Published tables (Turner 2004 and 1999, Andronescu 2007, DNA Mathews 2004 and 1999): valid on all 112 instances with free exterior loops, with dangles in two conventions, with flush coax equal to the stack, and with both. NO-instance gaps range from 0.4 to 3.3 kcal/mol.
- The NNDB bulge rule was tested on Turner 2004 only, in three exterior-loop settings: free, dangles "all", and coax plus dangles "some". All valid.
- Caveat: small instances only, and my dangle and coax conventions are simplified re-implementations. This is evidence, not proof.

## Task 4: prior-art search

I found no existing proof. That is not proof of novelty.

**Web searches (10) and what they returned:**
1. NP-hard MFE, unbounded strands, "nearest neighbour model", 2026: the known papers only.
2. Multi-strand stacking model with 3-PARTITION or bin packing: CHT and Alkan et al. 2006 (two strands); no such reduction.
3. DNA 32 (2026) accepted papers: nothing; I then read the LIPIcs vol. 387 contents, 14 papers, none relevant.
4. arXiv 2026 answers to the DSW question: only 2611.27945, which gives positive results.
5. Lyngsø 2004: paper identity only; the gadget is confirmed via DSW App. B.3.
6. Hajiaghayi thesis: nothing beyond CHT.
7. "Base pair stacking", multiple strands, pseudoknot-free: single-strand pseudoknotted literature only.
8. Shalaby PhD thesis: not public.
9. Bin packing or 3-partition with homopolymer or template strands: nothing.
10. Papers citing DSW 2025: none resolving the question.

**Consensus search:** returned only Condon et al. 2021 [1], Ducloz et al. 2025 [2] and Shalaby–Woods ICALP [3].

**Read from PDFs:** DSW DNA 31 and the arXiv full version; Shalaby–Woods 2611.27945 (§§1–3, 6.1, references); arXiv 2407.09676; Dirks et al. 2007; CHT DNA 27; Boehmer et al. §4.3; Demaine et al. DNA 30; Shalaby–Thachuk–Woods DNA 29 (keyword scan).

**Status of the question:** DSW Table 1 says hardness results "are conjectured to hold in the more complex NN model". Shalaby–Woods (23 Nov 2026) still says they are "in the simpler base pair matching (BPM) model".

**Uninspectable risk:** Shalaby's PhD thesis, cited in 2611.27945 as [43], "Defended Nov. 2026. To appear".

## Task 5: significance

- **It answers the question in the model the question's authors define.** Their Def. 11 plus App. A.2 has ΔG_exterior = 0, the energy function is fixed, and the association and symmetry terms are included. It does not dodge on those counts.
- **It is not a theorem about NUPACK-style models with dangles or coaxial stacking.** The file says so. My numerics suggest the same instances still work there, and the coax case is provable when bulges cost something (finding 2).
- **Strongest hostile objection:** this is Lyngsø's 2004 reduction with the C-blocks cut into strands. Only the GG/CC stack parameter matters, so it is a multi-strand stacking-model result presented as an NN result. It exploits the one feature (a nick costs a stack) that real coaxial stacking largely removes. It also needs one long template and unboundedly many species, with c = Θ(N/B) = o(N).
- **My assessment:** valid and worth a short note, with modest depth. It should be presented as an elementary observation with full attribution, the weakened (H2′), and the corrected coax statement. Without those, a referee would reject the framing, not the theorem.

## Files are in the scratchpad

- Code and outputs: `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review1/` (`enum.cpp`, `dp.cpp`, `lib.py`, `params.py`, `test_main.py`, `test_dp.py`, `fragility.py`, `coax_grid.py`, `fragility_real.py`, `run_all.sh`, `out_*.txt`)
- Downloaded sources: `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review1_dl/`
- Parameter files: `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review1_params/`
- Lean scratch copy: `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review1_lean/StackPackingCheck.lean`

## Sources

- [DSW, DNA 31](https://drops.dagstuhl.de/storage/00lipics/lipics-vol347-dna31/LIPIcs.DNA.31.1/LIPIcs.DNA.31.1.pdf) and [full version](https://arxiv.org/pdf/2506.19756)
- [Shalaby–Woods 2611.27945](https://arxiv.org/pdf/2611.27945) and [ICALP paper](https://arxiv.org/pdf/2407.09676)
- [Dirks et al. 2007](https://resolver.caltech.edu/CaltechAUTHORS:DIRsiamrev07)
- [CHT, DNA 27](https://drops.dagstuhl.de/storage/00lipics/lipics-vol205-dna27/LIPIcs.DNA.27.9/LIPIcs.DNA.27.9.pdf)
- [Boehmer et al., WABI 2024](https://drops.dagstuhl.de/storage/00lipics/lipics-vol312-wabi2024/LIPIcs.WABI.2024.18/LIPIcs.WABI.2024.18.pdf)
- [Demaine et al., DNA 30](https://drops.dagstuhl.de/storage/00lipics/lipics-vol314-dna30/LIPIcs.DNA.30.2/LIPIcs.DNA.30.2.pdf)
- [DNA 32 volume](https://drops.dagstuhl.de/entities/volume/LIPIcs-volume-387)
- [NNDB Turner 2004 bulge loops](https://rna.urmc.rochester.edu/NNDB/rna_2004/rna_2004_bulge_loops.html)
- [Bansal et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC7175655/)
- [ViennaRNA parameter files](https://github.com/ViennaRNA/ViennaRNA/tree/master/misc)

Consensus references:
- [1] [Predicting Minimum Free Energy Structures of Multi-Stranded Nucleic Acid Complexes Is APX-Hard](https://consensus.app/papers/details/w:e12a6aa8-510d-4eda-98a1-aef7acaaae85/?utm_source=claude_code) (Condon et al., 2021, DROPS, 7 citations)
- [2] [Algorithmic Hardness of the Partition Function for Nucleic Acid Strands](https://consensus.app/papers/details/w:2de4039f-5d6d-4782-887b-06ccb2c8dafd/?utm_source=claude_code) (Ducloz et al., 2025, DROPS, 1 citation)
- [3] [An Efficient Algorithm to Compute the Minimum Free Energy of Interacting Nucleic Acid Strands](https://consensus.app/papers/details/w:34aabde3-34da-4c84-960d-1c4c88f30840/?utm_source=claude_code) (Shalaby et al., 2024, DROPS, 4 citations)

Create or connect a free Consensus account to return more than 3 results per search in Claude Code.: https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
