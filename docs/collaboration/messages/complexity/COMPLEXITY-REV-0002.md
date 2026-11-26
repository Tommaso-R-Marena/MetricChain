Message ID:                  COMPLEXITY-REV-0002
Message type:                Internal adversarial review of docs/complexity/NANUQ_LOCAL_CRITERION.md (NANUQ metric of galled outer-labeled planar networks)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          All divisions (for the record); the division itself (findings to process)
Date and time (UTC):         2026-11-26 18:40
Priority:                    High
Status:                      Review received; disposition of every finding recorded at the end of this file
Relevant source commit:      9a35d2f (§§0–7), with spot checks of §8 as of c2ef506
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T5–CX-T9, CX-T13, CX-X2
Related message/request IDs: COMPLEXITY-MSG-0001, COMPLEXITY-MSG-0002

Scientific context:
First internal adversarial review of the NANUQ note (problem B of docs/complexity/OPEN_PROBLEMS.md).
Verdict of the referee: no claim broken; no critical finding; two major findings (the direct tests of Theorem 7 were
not independent of its structure lemmas; the method probably coincides with that of the earlier third-party claim)
and twelve minor ones.

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

# Referee report: NANUQ_LOCAL_CRITERION.md

**Bottom line.** I could not break any of the reviewed claims. No CRITICAL finding, two MAJOR findings (evidence independence, novelty), twelve MINOR. All numbers were reproduced with my own code.

**Version reviewed.** Commit 9a35d2f (399 lines). The file was edited during the review (c2ef506 added §8 / Theorem 11 and renumbered §§8–9). §§0–7 are unchanged apart from a four-line insertion; line numbers below refer to the current file. Theorem 11 was not in my brief and got a sanity check only.

## Verdicts

| Claim | Verdict |
|---|---|
| Lemma 1 (`d_N = d_Σ`) | Correct; justification mis-cited (finding 3) |
| Prop. 2, Lemma 3, Lemma 4, Thm 4 | Correct. I re-derived Prop. 2 by hand, including the trivial-split formula |
| Lemma 5, Prop. 6 | Correct; one imprecise sentence (finding 7) |
| Lemma 7, Lemma 8, Thm 6′ | Correct; 3/16/102 and 3/16/108 reproduced, all 108 systems 6-locally good |
| Lemma A | Correct, including coinciding parents (twin cherry) and a hybrid edge through the suppressed root |
| Lemma B | Correct; the cut-edge fact is true (proof in finding 6); the remark on the pieces is wrong but harmless |
| Thm 7 | Correct with minor gaps (findings 4–6); not falsified |
| Thm 9 (a), (b), (c) | Correct; N* is in the class and all values reproduced |
| Thm 10 | Correct as stated; "sharp" needs a qualifier (finding 10) |
| Thm 11 | Not audited; headline claims pass spot checks |

## Findings

1. **MAJOR — evidence independence** (§10 table, line 472; THEOREMS.md CX-T6, CX-X2). The paper's "direct tests" of Theorem 7 (`test_bloblets.py`, `test_multiblob.py`) build networks from the twin-tree and substitution description, so they presuppose Lemmas A and B. `netcalc.py` (explicit DAGs) is used only for the non-galled examples. As submitted, the two structural lemmas had no independent computational support. This review supplies it. Fix: add an explicit-DAG generator test to the repository and say which tests are independent of the structure lemmas.

2. **MAJOR — novelty** (§0 item 2, lines 18–22; THEOREMS.md CX-T5, CX-T9). The VibeMathed entry of 30 Sep 2026 claims the same all-level statement by "a six-label reduction, exact finite certificate and composition identity". Its summary mentions "plane-tree and duplication instances" and "122 distinct quartet systems". By my count `|𝒜_3|+|𝒜_4|+|𝒜_5|+|𝒜_6| = 1+3+16+102 = 122`. The method, not just the statement, probably coincides; this is inferred from the public summary only. Fix: say so, and drop "not found in print" for CX-T5/CX-T9 until that repository is inspected. I found no prior art for Theorems 9 and 10.

3. **MINOR, must fix** (line 69, Lemma 1). "[HABIMRW] §5: `Q(N) = Q(T(N))`" is a notation, not a statement. The source defines displayed quartets through quarnets `N|xyzw` built from up-down paths (Def. 2.5). The identity needed is the one used, unproved, in the proof of their Lemma 3.2. Fix: cite that, or add the short argument (an up-down path uses at most one hybrid edge per hybrid node, so it lies in a switching; the converse is immediate). A literal implementation of Def. 2.5 gave 0 mismatches on 9,155 four-sets.

4. **MINOR** (lines 285–287, 294–297). The "marked networks" class is never defined, and the remark that `N_2` may lack a rooted partner is wrong. `N_1` keeps the root; `N_2` is rooted on the pendant edge of `r`. In 4,000 explicit cuts both pieces were valid binary LSA networks, galled and outer-labeled planar. Fix: run the induction inside the class of networks on at least 2 leaves.

5. **MINOR** (line 44, §4, Lemma 7(iii)). The standing `n ≥ 4` conflicts with pieces that do occur: `N_1` had 2 leaves in 159 of 4,000 cuts and 3 leaves in 304; `N_2` had 3 leaves in 2,098. Fix: define `𝒜_n` and `∘` for `n ≥ 2` and apply Theorem 4 only to the final system.

6. **MINOR** (line 272). The cut-edge fact rests on an unproved remark of the source. A proof:
   - Let `D` be the descendants of the child `c` of `h`. If `(h,c)` lay on a cycle, some edge `(a,b) ≠ (h,c)` would enter `D`.
   - `b = c` makes `c` a hybrid below `h`, contradicting Def. 2.3(vi) for `c`.
   - Otherwise `b` is a hybrid with parents `a ∉ D` and `a′ ∈ D`. Its hybrid-edge-free cycle rises from `a′` by tree edges to an apex. That path cannot leave `D`, because above `c` sits `h`, whose other edges are hybrid edges. So the apex, and hence `a`, lies in `D`: contradiction.

   The three galled criteria (Def. 2.3(vi), articulation, ancestor) agreed on all 134,571 generated networks, 55,342 of them non-galled.

7. **MINOR** (line 213). "Both contain the positions lying between those of `a_2` and of `a_3`" is empty when the two leaves are adjacent. Correct statement: each interval contains the arc between its chosen positions of `a_2` and `a_3`, since the complementary arc contains every position of `z`; so both contain the last position of `a_2`.

8. **MINOR** (lines 223–226). "All displayed trees … restrictions of one planar tree, with independent choices" holds only for class 𝒜; 6 of the 108 six-leaf systems are not in `𝒜_6`. "So does the theorem" overgeneralises: most non-galled planar networks satisfy the conclusion (finding 11).

9. **MINOR** (lines 344–348, line 25). "There are `st` of them" fits the clade version, where `α = 2 − st`. The numbers quoted in (c) are for the bloblet version, where every pair of `A∪D` leaves gives `Φ6 = −½`, with `Φ4 = 1` and all `Φ5 = 0`, so `α = 2 − C(s+t,2)`. Both formulas matched 11 parameter pairs each. "Tending to −∞" is stated from tested values; it follows from Prop. 2 and should be proved.

10. **MINOR** (§7, §0 item 4). Sharpness holds only for "Kalmanson and exact support" together. Six of the 9 six-point failures and 12 of the 14 minimal blow-ups stay Kalmanson, with only the support wrong. With larger blow-ups, 17 of the 23 excluded systems reach a negative weight. The 6 systems missing a 2-split and its crossing 3-split do not, within multiplicities ≤ 3 and ≤ 11 leaves. Also, 19 of the 127 systems are displayed by no network of the class, so nothing sharp is said about network classes.

11. **MINOR** (§6, context). By Cor. 3.4 of the source, the multiplicity-weighted metric is circular decomposable for every outer-labeled planar network. For N* it gives α = 5 on `{x,y}|rest` with exact support. The failure is specific to the multiplicity-free ρ of Eq. (10) and should be described that way. Two facts worth adding:
    - Seven leaves is minimal for two hybrids. An exhaustive pass over planar two-hybrid networks on 4, 5 and 6 leaves found no violation.
    - On 7 leaves, 664 of 60,196 non-galled insertion sequences give a negative weight (all bloblets) and 1,252 give a support mismatch only (all non-bloblets).

12. **MINOR** (Lemma 8). `𝒞_6` has 17 dihedral classes, 16 of them in `𝒜_6`. Printing them with their Φ6 values would make the only computer step of Theorem 7 checkable by hand.

13. **MINOR, editorial.** "[K]" (line 64) and "CX-D2" (line 80) are undefined. Lemma 4 / Theorem 4 and Lemma 7 / Theorem 7 share numbers; there is a Theorem 6′ but no Theorem 6; there is no bibliography.

14. **MINOR** (Theorem 11). Reading "4-cycle" as "both planar quartets displayed" above level 1 is the author's own extension and should be labelled as such.

## What I computed

- **N\*.** It is a valid binary LSA network with 7 pendant cut edges and one 9-node blob with 2 hybrids, so a level-2 bloblet. It is planar with order `(a1,a2,b,x,y,c,d)` and not galled by all three criteria. It has 4 distinct displayed trees; the matrix is identical to the paper's; α = −1; Kalmanson for 0 of 360 orders, in both the α form and the direct four-point form.
- **External anchor.** My code reproduces all five NANUQ matrices of Table 1 of the source.
- **Random search for a counterexample to Theorem 7.** Networks were grown by hybrid insertion into random trees, then filtered by Def. 2.3(vi), a planarity test with an apex, and the LSA condition. All 74,661 distinct networks passed.

  | Leaves 6–10 (72,161 networks) | Count |
  |---|---|
  | Level 1 / 2 / 3 / 4 / 5 / 6–7 | 22,039 / 21,049 / 14,358 / 8,914 / 4,487 / 1,314 |
  | Bloblets / one blob plus internal cut edges / multi-blob | 11,591 / 28,122 / 32,448 |
  | At least one hybrid with a non-leaf child | 36,958 |
  | Root with a hybrid child | 19,196 |
  | Level-3 bloblets (B2) / level-2 non-bloblets (B1) | 2,651 / 18,978 |

  A further 2,500 networks had 11–13 leaves and levels 1–8. Across the 74,500 networks in the four main batches, 3,772 have parallel edges after root suppression.
- **Exhaustive small cases** (insertion sequences, with repetition), all passing: 4 leaves ≤ 3 hybrids (9,476 at the last step), 5 leaves ≤ 3 (76,752), 6 leaves ≤ 2 (19,668), 7 leaves ≤ 2 (74,314).
- **Lemmas A, B, 7(iii).** 1,422,762 six-leaf restrictions were all in my `𝒞_6`; those from the 35,240 leaf-child networks were all in my `𝒜_6`. The substitution identity held on 4,000 cuts. The six-leaf systems realised are exactly the 108.
- **Counts.** 16 systems on 5 points, all 5-point facts hold (Φ5 and Ψ in {0, ½, 1}). On 6 points: 150 / 141 / 127 / 108. On 7 points: 2,682 tree-generated, 1,807 good, 1,254 satisfying the Theorem 4 hypothesis, none violating its conclusion. The Prop. 2 identity held on 3,943 systems; Lemma 5 on 1,800 labelled instances.
- **Theorem 10(b).** Six blow-ups from the author's output were recomputed; my own search finds the same minimal blow-ups for all 14 systems.
- **Theorem 11 spot checks.**
  - The 8-leaf level-1 witness gives −2 under Modified NANUQ and is Kalmanson for 0 of 2,520 orders.
  - Five parameter points in cone (a) pass on 12,000 networks.
  - Modified NANUQ passes on 6,000 leaf-child networks and fails on 1,006 of 12,000 general ones.
  - The sunlet formula matches at n = 10 and 14.

## What I searched

Nine web searches (wording abbreviated) and four page fetches:
- NANUQ metric, circular decomposable, level-2/level-3, conjecture, proof.
- NANUQ distance, non-galled counterexample, "galled necessary", Kalmanson.
- Holtgrefe 2026 follow-up, level-2 inference algorithm.
- "Not circular decomposable" / "not Kalmanson" for non-galled level-2 networks.
- NANUQ outside level-1, splits graph not circular.
- NANUQ+ parametric family (two searches).
- All-levels / level-3 circular decomposability, 2026 arXiv.
- The 2026 Correction to the source paper.

Results:
- **(i) Proof or disproof of the Section 6 conjectures:** only the unreviewed VibeMathed entry; nothing on arXiv or in a journal. Holtgrefe's publication list has no follow-up. arXiv:2610.07855 only cites NANUQ+.
- **(ii) Necessity of "galled" or a non-galled counterexample:** nothing found.
- **(iii) NANUQ+:** Def. 3.1 gives ρ = (ρc, ρs, ρa, ρo), with NANUQ (0, 1, ½, 1) and Modified NANUQ (½, 1, ½, 1); its theorems cover sunlets only.
- The 2026 Correction to the source concerns an omitted figure panel.

I did not inspect the third-party GitHub repository, because repository access had been denied to this session. A failure to find something is not proof of novelty.

## Strongest hostile objection

Theorem 7 is probably a rediscovery: the same statement, with apparently the same three ingredients and a matching system count, was posted two months earlier. Neither proof is peer reviewed. The proof also has no conceptual argument for its key step. The vanishing of Φ6 on undisplayed splits, and positivity on `𝒞∖𝒜`, are established only by checking 108 cases. A second line of attack: Theorem 9 shows one multiplicity-free distance failing outside the class it was designed for, and Theorem 10 is sharp only relative to an ad hoc closure on abstract split systems.

## What a sceptic must re-run for Theorem 7

Two things, about 30 seconds in my implementation:
- Lemma 4: 16 systems × 10 placements.
- Lemma 8: 148,925 twin-tree structures on up to 12 positions give 1/3/16/102 systems; the closure gives 108; then Φ6 in 12 labellings each.

Everything else is a paper proof.

## Files

Everything is in `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review2/`; logs are in its `out/` subfolder. Nothing under `/home/user/MetricChain/` was modified.
- `rnet.py`, `gen.py`, `css.py`, `quarnet.py` — libraries
- `t3a_nstar.py` — N*
- `t3b_random.py`, `t3b_random_big.py`, `t_exhaust.py`, `t_exhaust_ng.py` — counterexample search
- `t_lemmaAB.py` — Lemmas A, B, 7(iii)
- `t3c_counts.py`, `t3d_blowups.py`, `t_extra.py`, `t9c_family.py` — counts, blow-ups, family
- `t1_defs.py`, `t_anchor.py` — definitions audit and Table 1
- `t11_param.py`, `t11_param2.py` — Theorem 11 spot checks

## Sources

- https://arxiv.org/pdf/2507.17308
- https://link.springer.com/article/10.1007/s11538-025-01549-4
- https://vibemathed.com/problem/all-level-nanuq-circularity-and-exact-displayed-split-support
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12297685/
- https://www.nielsholtgrefe.nl/publications/
- https://arxiv.org/pdf/2610.07855
- https://link.springer.com/article/10.1007/s11538-025-01564-5
- https://arxiv.org/pdf/1905.07050
