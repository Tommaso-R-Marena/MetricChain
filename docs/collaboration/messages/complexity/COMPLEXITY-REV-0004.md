Message ID:                  COMPLEXITY-REV-0004
Message type:                Internal adversarial review of docs/complexity/ISING_GROUND_SETS.md and of the post-review additions to docs/complexity/NANUQ_LOCAL_CRITERION.md (including Theorem 11, never reviewed before)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          All divisions (for the record); Ensemble division (E-C1: several statements of COMPLEXITY-RES-0003 are affected); the division itself (findings to process)
Date and time (UTC):         2026-11-26 20:29
Priority:                    High
Status:                      Review received 2026-11-26 20:27 UTC; **every finding processed** by 2026-11-26 21:09 UTC (disposition table at the end of this file)
Relevant source commit:      36d86cc (Ising note §§0–8; NANUQ note at 704 lines).  The referee notes that HEAD moved to 89114ea and that uncommitted edits existed during the review (§9 / Proposition 11 of the Ising note; Corollary 5′, Theorem 10′, §7.1 of the NANUQ note): these are outside the report except for the incidental checks it lists
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T16–CX-T19 (Ising ground sets); CX-T5–CX-T9, CX-T13 (NANUQ: Lemma 0, Lemma B0, Lemma B, Theorem 9(c), Theorem 11)
Related message/request IDs: COMPLEXITY-RES-0003 (answer to E-C1), COMPLEXITY-MSG-0003, COMPLEXITY-REV-0002

Scientific context:
First internal adversarial review of the Ising note (answer to the Ensemble division's question E-C1) and review of
the parts of the NANUQ note written or rewritten after COMPLEXITY-REV-0002, together with Theorem 11.
Verdict of the referee: no false numbered theorem in either document; every table, count and certificate
reproduced.  **Major findings:** (1) the "equivalent formulation" by ℓ1-rigidity in §6 of the Ising note is wrong
for faces that are not simplices; (2) the structural section of the Ising note re-derives published results
(Corollary 7 is Laurent–Poljak 1995/96, Theorem 4.2; Proposition 5 is the facial structure of the elliptope) and
its prior-art section is incomplete; (9) the proof of Lemma 0 of the NANUQ note has an unproved step (the statement
is true; the referee closes the gap).  Among the minor findings, (3) changes the complexity table: the note's own
Proposition 5 gives an algorithm in time 2^K·poly(n), so the problem is polynomial for K = O(log n).

What this review is and is not:
The referee was a separate AI agent instantiated by this division with an adversarial brief ("try to break the
claimed theorems"; re-derive, recompute with code written from the definitions, search for prior art).  It had no
access to our reasoning, only to the files of this branch.  **This is an internal AI review.  It is not
independent academic peer review**, and the results it covers remain unrefereed in the sense of the collaboration
README.  The report is reproduced verbatim below.  Paths in the report that point to a session scratch directory
refer to the referee's working directory; the referee's programs and logs are preserved in
`experiments/complexity/reviews/rev4_ising_nanuq/` (downloaded papers are not redistributed).

---------------------------------------------------------------------------------------------------------------
REPORT (verbatim)
---------------------------------------------------------------------------------------------------------------

# Referee report (review4): ISING_GROUND_SETS.md and the post-review additions to NANUQ_LOCAL_CRITERION.md

**Bottom line.** I found no false numbered theorem in either document. Every table, count and certificate I recomputed with my own code agrees with the author's. Part 1 has two real problems. The "equivalent formulation" by ℓ1-rigidity in §6 is wrong for non-simplex faces. The structural section re-derives published results: Corollary 7 is Laurent–Poljak 1995/96, Theorem 4.2, and Proposition 5 is the facial structure of the elliptope. The note also misses an algorithm that follows from its own Proposition 5 and runs in time 2^K·poly(n). I could not decide hardness for K in the input. I did prove that "does the span contain another sign vector" is NP-complete without the symmetry hypothesis, but those instances are always exposed, so nothing transfers. Part 2 is correct. Lemma 0 has one unproved step, which I close below, and the Theorem 11(c) witness is described ambiguously; a smaller one exists. This is an internal AI review, not academic peer review.

**Version reviewed.** Commit 36d86cc: Ising note §§0–8, NANUQ note at 704 lines. During the review someone else moved HEAD to 89114ea and left uncommitted edits (§9 / Prop. 11 in the Ising note; Corollary 5′, Theorem 10′ and §7.1 in the NANUQ note). Those are outside this report except for the incidental checks listed. I modified nothing in the repository; the author's code was run from a scratch copy only.

## Verdicts

| Claim | Verdict |
|---|---|
| **Part 1** Theorem 1 (criterion, certificate size, co-NP) | correct |
| Theorem 2 (both directions, anti-twins, any c > 0) and Corollary | correct; improvable (finding 3) |
| Theorem 3 (K = 4) | correct; recomputed 255 / 96 / 157 / 2, 15 orbits, group order 192 |
| K = 5 table | correct; 150 orbits, 130 non-degenerate, 6 non-exposed, 746 of 61 719 sets; the printed certificate verifies exactly |
| Proposition 5, Theorem 6 | correct (Prop. 5 known) |
| Corollary 7 | correct, but a published theorem |
| Lemma 8 (including negative coefficients) | correct |
| Lemma 9 | correct; the note gives no proof |
| Proposition 10, Sidon example (both directions, 0 ∈ H) | correct |
| §6 complexity table | correct but incomplete |
| §6 "equivalent formulation" (ℓ1-rigidity) | **wrong as stated** |
| §7 prior art | incomplete |
| **Part 2** Lemma 0 | correct with a gap |
| Lemma 1, Lemma B0, Lemma B, Theorem 7 induction for n ≥ 2, class 𝒜 and substitution for n ≥ 2 | correct |
| Theorem 9(c), both formulas | correct |
| §7 "sharp" paragraph (as of 36d86cc) | correct; all numbers reproduced |
| Theorem 11 (a), (b), table of forms, necessity | correct as far as checked |
| Theorem 11 (c) | correct; witness description ambiguous |
| Remark on the reading beyond level 1 | accurate; at level 1 it matches NANUQ⁺ Def. 3.1 |
| Lean file; Theorem 10′ / Corollary 5′ / Ising §9 | not checked (incidental checks of 5′ and 10′(c) only) |

## Findings, Part 1

1. **MAJOR — §6, last sentence.** "Exposed ⟺ the Hamming metric on T decomposes into cut metrics in exactly one way" is false.
   - Counterexample 1: all 8 states of 4 sites (J = 0, exposed). The metric is 4·𝟙₄, which is the sum of the seven cuts and also twice the four singleton cuts.
   - Counterexample 2: the 12 roots of x₁x₂+x₁x₃+x₂x₃ ≥ −1 on 5 sites. Exposed, 11 cuts of rank 9, and an explicit second decomposition.
   - ℓ1-rigid means lying on a *simplicial* face (Deza–Laurent survey, §2.5).
   - Fix: "V is exposed iff every non-negative decomposition of the Hamming metric uses only the K−1 given cuts; this is ℓ1-rigidity iff in addition P(V) is affinely independent."

2. **MAJOR — §0, §5, §7, registers CX-T16–T19 ("not searched").** Novelty framing.
   - Corollary 7 is Laurent–Poljak, *On the facial structure of the set of correlation matrices* (CWI BS-R9501, 1995; SIAM J. Matrix Anal. Appl. 17, 1996), Theorem 4.2: f_h linearly independent and {f_h∘f_h′} ∪ {e} linearly independent imply Conv(f_h f_hᵀ) is a face of the elliptope. A face of the elliptope with cut-matrix vertices is a face of the cut polytope. Their Corollary 4.5 is the case "all types present"; their Theorem 4.1 gives C(K,2) ≤ n−1.
   - Proposition 5 follows at once from their description of elliptope faces by kernels.
   - Tropp, arXiv:1801.00749: random sets of r ≤ c√n cut vectors generate simplicial faces of the elliptope, hence of the cut polytope, with high probability. This bears directly on the Ensemble division's random-conformer question.
   - The K = 4 obstruction is "the path metric of K₄ is not ℓ1-rigid" (Deza–Laurent, *Applications of cut polyhedra*, LIENS-92-18).
   - All instances with at most 5 types are in the published face lattice of the cut polytope on 5 nodes (A. Deza, M. Deza, LIENS-95-1): f₃ = 1780, so 40 four-sets are not faces, which is exactly what Theorem 3 gives on five sites.
   - A second known polynomial sufficient condition is missing: if the types form an isometric subgraph of the cube relative to some state, V is exposed (Deza–Laurent, "every isometric subgraph of the hypercube is ℓ1-rigid", read in the survey). On the K = 5 table it covers 15 977 type sets against 5 425 for Corollary 7.
   - The decision problem is the recognition of facial sets (MLE existence) in statistics, e.g. Wang–Rauh–Massam, arXiv:1603.04843.
   - My own observation: Theorem 2 is one line in cut-cone language. With x¹ = 𝟙, twins are points at distance 0, and no decomposition uses a cut separating them.
   - Not found in what I read: Theorem 6 in this form, Lemma 9, Proposition 10 with the Sidon criterion, and any complexity result. That is not evidence of novelty.

3. **MINOR, but it changes the complexity table — §3 parenthesis, §6.** "Doubly exponential table; does not help when K grows" overlooks Proposition 5.
   - A K-dimensional span contains at most 2^(K−1) states. Enumerate them and solve the LP on those only. Time 2^K·poly(n), so polynomial for K = O(log n). Hardness can only arise for K ≫ log n.
   - Verified against the full LP on 3 895 instances with 0 mismatches. K = 14, n = 80 runs in 49 s.

4. **MINOR — §4, "the sixth orbit".** It is not sporadic.
   - Flipping site 2 turns it into the five singleton states on five sites; the orbit has size 16 and stabiliser S₅.
   - Two-line proof: average an exposing J over site permutations to get J = λ·(all ones), whose ground set is {𝟙}, everything, or the balanced states.
   - It is the m = 5 member of a family: m singletons on m ≥ 4 sites, with or without 𝟙, are never exposed (checked for m ≤ 10).
   - At K = 6, 465 of 2 046 sampled non-exposed sets have neither a constant-product quadruple nor five singleton-like states. The note does not claim completeness, but should say so.

5. **MINOR — §6, hardness route.**
   - "Does the span of K given sign vectors contain another sign vector?" is NP-complete without symmetry. Reduction from positive 1-in-3-SAT:
     - States: one per variable, one extra state z, and 𝟙.
     - Sites: ∅, {k}, each clause A_i, A_i ∪ {z}, and A_i ∪ A_j ∪ {z}.
     - Extra sign vectors are exactly Σ_{k∈U} x^k − x^z + (2−|U|)𝟙 for exact hitting sets U.
   - Those instances are always exposed, because c_k·c_z ≤ 0 can never cancel. So the hardness lies entirely in the diagonal-combination condition. A necessary condition for non-exposedness: for every pair k ≠ l the products c_k c_l over the certificate must cancel.
   - Any instance becomes pair-separating by x^k ↦ x^k ⊗ χ_{h_k}; with Sidon labels it is always exposed.
   - Verified on 60 instances (34 satisfiable, 0 mismatches, 0 non-exposed).
   - I could not prove hardness or find a polynomial algorithm for K in the input.

6. **MINOR — §7, second bullet.** "With fields the twin argument changes" is inaccurate. Fields are one extra site with constant column, and Theorem 2 applies verbatim.

7. **MINOR — test coverage.**
   - The author's Theorem 2 test has 300 trials: 218 degenerate, 79 exposed, 3 not exposed. Anti-twins are gauged away before solving.
   - Corollary 7 is tested on 3 random cases; the Sidon criterion on 12 subsets of F₂⁴.
   - `other_sign_vectors_in_span` uses floating-point rank although its comment promises an exact confirmation.

8. **MINOR.** Lemma 9 needs its three-line proof: move the flipped states that lie in V to the right-hand side and divide by the remaining weight. In the Sidon example, "non-linear" should read "not ± a character".

## Findings, Part 2

9. **MAJOR by the rubric (an unproved proof step; the statement is true) — Lemma 0.** "N|_Y is … a semi-directed network, so its switchings are trees containing Y" assumes that the union U of up-down paths has a single source, with the inherited orientation.
   - Fix: every apex lies at or below ℓ = LSA(Y). ℓ is an apex by Menger. If b ≠ ℓ were a source, take a path P from ℓ to Y avoiding b and a path R from ℓ to b, and let c be the last node of R on P. Then either one of b's two down-paths misses P, or the first node of P on them gives a simple up-down path with apex c that uses the edge into b.
   - Computation: 14 473 (N, Y) pairs on 1 500 networks, including non-planar and non-galled ones. Always one source; 0 mismatches with a literal Def. 2.5.

10. **MINOR — Theorem 11(c).**
    - "Cherries at two of its other four positions" is ambiguous. Only the placement at the two cycle positions *not adjacent* to the hybrid gives weight −2 and no Kalmanson order among 2520. The other five placements satisfy the full conclusion under Modified NANUQ.
    - A smaller witness exists: 7 leaves, a 6-cycle with a cherry below the hybrid. Weight −1; Kalmanson for none of 360 orders.
    - No failure among 22 960 distinct galled planar networks with at most 6 leaves.
    - Modified NANUQ lies on two boundary faces of (b): ρ_c = ρ_a and ρ_s = 2ρ_a.
    - Say explicitly that NANUQ⁺ disclaims any combinatorial structure for distances other than NANUQ, so (c) contradicts nothing published.

11. **MINOR — Theorem 9(c) evidence.** `nongalled_formula.py` takes the four displayed trees by formula, not from networks. I built the explicit rooted networks; the split systems agree for 0 ≤ s,t ≤ 6 in both versions.

12. **MINOR — Lemma B.** N₂ always has at least 3 leaves. N₁ has 2 leaves in 221 of 1 902 cuts.

## What I computed (own code, exact arithmetic for all certificates)

**Part 1**
- K = 4: all 255 type sets.
- K = 5: 130 orbit representatives by the full LP (up to 32 768 states) and by the span-reduced LP.
- Theorem 2: 185 + 700 instances with true anti-twins, n ≤ 12; 552 non-exposed; 0 mismatches. The proof's construction was checked for c = 1/1000, 1, 1000.
- Random K = 4..7: 1 301 instances, 569 non-exposed. 0 violations of Proposition 5, of Theorem 6 (1 096 independent cases) and of Corollary 7 (120 cases).
- Lemma 8: 225 cases with some y^k outside V, all non-exposed.
- Lemma 9: 148 cases, all non-exposed, certificate verified.
- Sidon: 247 subsets of F₂³, 60 of F₂⁴ (full LP), 200 of F₂⁵.
- Proposition 10: 300 twisted character instances, 112 non-exposed, 0 mismatches.
- K = 6: 3 847 type sets, 0 violations of any general statement.
- External anchor: the face lattice of the cut polytope on 5 nodes, by LP and independently by facet intersections. f = (16, 120, 560, 1780, 3872, 5592, 5060, 2600, 640, 56). It matches the published entries except f₇: the report prints 3080 and an orbit size 960, where its own representatives give 2600 and 480.

**Part 2**
- Tree anchor: Theorem 2.12 of the source paper on 200 trees.
- 2 795 distinct galled outer-labeled planar networks from explicit DAGs (1 407 of level ≥ 3, 224 with a 2-blob at the root): 9 402 hybrid nodes and 1 902 cuts, with no failure of Lemma B0, Lemma B or Theorem 7.
- Lemma B0 without planarity: 1 417 networks, 4 782 hybrid nodes, 0 failures.
- Theorem 9: the N* matrix, α = −1, all 360 orders; 192 values of the two formulas for 0 ≤ s,t ≤ 7.
- §7: 150 / 141 / 9 (3 negative, 6 Kalmanson with wrong support) / 127 / 23. Blow-ups up to 11 leaves: negative weight for 17 of 23, none for the other 6; 12 of 14 minimal blow-ups remain Kalmanson.
- Theorem 11:
  - 2 971 networks checked exactly on the extreme rays of both domains, 0 failures.
  - The table of forms reproduced exactly.
  - Six-leaf witnesses for s−o, o−s, a−c (class 𝒜) and 2a−c−s (general class only).
  - Blow-up second differences equal 4F for m ≤ 6; one direct failure at 24 leaves.
  - Sunlet formula for n = 4..11.
- Incidental: Corollary 5′ on 150 × 12 labellings; the Theorem 10′(c) formula on 68 values.

## What I searched and read

- **Source paper, arXiv:2507.17308v2:** §2.1, Eqs. (4)–(11), Def. 4.1 — full text.
- **NANUQ⁺ (Europe PMC PMC12297685):** Def. 3.1 through Theorem 3.14 — text, formulas stripped.
- **Laurent–Poljak, CWI BS-R9501:** abstract and pp. 13–15, as page images.
- **Tropp, arXiv:1801.00749v1:** §§1–3, full text.
- **Deza–Laurent, LIENS-92-18:** §2.5, the rigidity examples, Table 1, the equidistant-metric section — text.
- **A. Deza–M. Deza, LIENS-95-1:** §1 and §3 — text, not the figures.
- **Deza–Laurent–Poljak, *The cut cone III*:** abstract only.
- **Deza–Laurent, *The cut cone: simplicial faces and linear dependencies*:** bibliographic record only; no full text found. The book *Geometry of Cuts and Metrics* was not accessible.
- **Wang–Rauh–Massam, arXiv:1603.04843:** introduction and §2.2; no hardness statement found.
- **Searches with nothing usable beyond snippets:** complexity of ℓ1-rigidity; complexity of recognising faces of the cut polytope; Hopfield projection rule (the "sign vectors in the span are ground states" fact is from memory, not from a source I read); design of Ising ground sets.

## Strongest hostile objection

- **Part 1.** "The fixed-K answer is a triviality once twins are merged. The real question is left open. The structural section rediscovers Laurent–Poljak without citing them. The only stated reformulation of the open problem is wrong. The complexity discussion overlooks a 2^K algorithm implied by the paper's own Proposition 5."
- **Part 2.** "Theorem 7 is by the authors' own account probably a rediscovery. Theorem 11 is a theorem about the authors' own extension of the family and rests on a computer table that no kernel checks. Its only statement about the published family, (c), refutes a property the NANUQ⁺ authors never claimed."

## Files I wrote

All in `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review4/`:

- `ising_core.py`, `k4_table.py`, `k5_table.py`, `ising_tests.py`, `ising_tests2.py`, `referee_extras.py`
- `anchor_c5.py`, `anchor_c5_hull.py`, `anchor_c5_orbits.py`
- `nanuq_core.py`, `nanuq_tests.py`, `nanuq_param.py`, `nanuq_mod_small.py`, `sharp_check.py`, `sharp_check2.py`, `compare_family.py`
- Logs and data: `k5_table.log`, `k5_results.json`, `k6.log`, `t1.log`, `t2.log`, `t34.log`, `t56.log`, `nB.log`, `nC.log`, `p1.log`, `p4.log`, `sharp.log`, `author_parametric_theorem.log`, `author_parametric_witnesses_A.log`
- `author_copy/` — a copy of the author's code, used only to run it.

Downloaded sources are in `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review4_dl/`.


---------------------------------------------------------------------------------------------------------------
DISPOSITION (completed 2026-11-26 21:09 UTC)
---------------------------------------------------------------------------------------------------------------

Part 1 — `docs/complexity/ISING_GROUND_SETS.md` (section numbers of the revised note; its §10 lists the same changes)

| # | finding | disposition |
|---|---|---|
| 1 | MAJOR: "exposed ⇔ unique decomposition of the Hamming metric" is false for non-simplicial faces | **Accepted.**  §6 "Formulation with cut metrics (corrected)": exposed ⇔ every non-negative decomposition uses only the given cuts; ℓ1-rigidity is this plus linear independence.  Both counterexamples of the referee quoted |
| 2 | MAJOR: Corollary 7 is Laurent–Poljak Theorem 4.2; Proposition 5 follows from the faces of the elliptope; further prior art; a second known sufficient condition; registers said "not searched" | **Accepted.**  We read pp. 13–14 of the Laurent–Poljak report and pp. 1–6 of Tropp's paper ourselves; attributions at Proposition 5 and Corollary 7; the isometric condition added (as reported by the referee; our recount on the `K = 5` table gives the referee's numbers 15 977 and 5 425); §0, §7 rewritten with the way each source was inspected; `PRIOR_ART.md` §C; `THEOREMS.md` CX-T16–T19; `OPEN_PROBLEMS.md` D1 |
| 3 | MINOR (changes the complexity table): an algorithm of time `2^K·poly(n)` follows from Proposition 5 | **Accepted.**  Corollary 5a, credited to the referee; implemented with exact arithmetic (`span_algorithm.py`), agrees with the full linear programme on all type sets for `K = 4` and 900 random ones for `K = 5–7`; complexity table extended (`K = O(log n)`: polynomial) |
| 4 | MINOR: the sixth orbit of the `K = 5` table is the five singletons, a member of a family; the two families are not exhaustive | **Accepted.**  Proposition 12 with the referee's averaging proof; checked for `m ≤ 8`; the referee's `K = 6` sample quoted as a caveat |
| 5 | MINOR: "another sign vector in the span" is NP-complete without symmetry; its instances are exposed; a necessary condition; tensoring with characters | **Accepted and extended.**  Theorem 14 (the referee's reduction, re-derived by us line by line and re-run on 60 instances).  Together with a new Proposition 13 (a pair energy with a sum-of-squares certificate of degree 2 exists ⇔ no other sign vector in the span) this classifies a variant of the question: co-NP-complete, `2^K·poly(n)`, no `2^{o(K)}` under ETH.  Proposition 13, 13′ and consequences (a), (b) of Theorem 14 are **new and unreviewed** |
| 6 | MINOR: "with fields the twin argument changes" is inaccurate | **Accepted.**  Remark in §3 (fields are one more site) |
| 7 | MINOR: thin tests; floating-point rank where an exact test was promised | **Accepted.**  `span_rule.py` uses the exact routine; §8 states the coverage of our tests and of the referee's |
| 8 | MINOR: Lemma 9 lacks a proof; "non-linear" should read "not ± a character" | **Accepted.**  Proof added; wording corrected |

Part 2 — `docs/complexity/NANUQ_LOCAL_CRITERION.md` (its §11 lists the same changes)

| # | finding | disposition |
|---|---|---|
| 9 | MAJOR by the rubric: Lemma 0 assumes that the union of up-down paths has one source | **Accepted.**  Proof completed with the referee's argument, written out in three steps (every node below the least stable ancestor; it is an apex, by Menger; every other node has an entering edge) |
| 10 | MINOR: Theorem 11(c): ambiguous witness; a smaller one exists; boundary faces; NANUQ⁺ disclaims other distances | **Accepted.**  Theorem 11(c) rewritten; the seven-leaf witness and the six placements of two cherries recomputed from explicit rooted networks (`modified_nanuq_witness7.py`: weight −1, 0 of 360 orders; only the placement away from the hybrid node fails) |
| 11 | MINOR: `nongalled_formula.py` takes the trees by formula | **Accepted.**  Said in §6; the referee's explicit networks and our `level2_fourtrees_check.py`, `level2_explicit.py` listed |
| 12 | MINOR: sizes of the pieces in Lemma B | **Recorded** in the remark after Lemma B |

Not covered by this review (the referee says so): the Lean file; §9 / Proposition 11 of the Ising note;
Corollary 5′, Theorem 10′, §7.1 and §7.2 of the NANUQ note (incidental checks of Corollary 5′ and of the
formula of Theorem 10′(c) only).

The referee's "strongest hostile objection" to Part 1 — the fixed-`K` answer is trivial once twins are merged,
the real question is open, the structural section rediscovers Laurent–Poljak, the stated reformulation is
wrong, a `2^K` algorithm is overlooked — is accepted in every point; the revised note says each of these
things itself.  To Part 2 — Theorem 7 is probably a rediscovery; Theorem 11 is about our own extension and
rests on a computed table; (c) refutes a property nobody claimed — likewise: all three are stated in the note.
