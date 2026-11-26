Message ID:                  COMPLEXITY-REV-0003
Message type:                Internal adversarial review of docs/complexity/STRANDS_ALGORITHM.md and of the post-review additions to docs/complexity/STRANDS_NN_HARDNESS.md
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          All divisions (for the record); the division itself (findings to process)
Date and time (UTC):         2026-11-26 20:29
Priority:                    High
Status:                      Review received 2026-11-26 20:25 UTC; **every finding processed** by 2026-11-26 21:24 UTC (disposition table at the end of this file)
Relevant source commit:      36d86cc (start of the review) to 89114ea (the referee notes that the algorithm note and multiset_dp.py did not change in between; in the hardness note only Theorem 1e and test counts changed)
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T10, CX-T11, CX-T12 (algorithm); CX-T1, CX-T4, CX-T14, CX-T15, CX-T20, CX-T24 (hardness additions)
Related message/request IDs: COMPLEXITY-MSG-0002, COMPLEXITY-MSG-0003, COMPLEXITY-REV-0001

Scientific context:
First internal adversarial review of the algorithm note (magnified nearest-neighbour partition function over all
strand orderings with symmetry, by a sub-multiset dynamic programme) and second look at the hardness note
(Theorems 1c, 1d, 1e, Remark 5, Corollaries 4(ii) and 5, Appendix A, written after COMPLEXITY-REV-0001).
Verdict of the referee: no stated theorem broken; no critical finding; **two major findings** —
(1) the novelty paragraph of the algorithm note is wrong as worded: the journal version of Boehmer, Berkemer,
Will, Ponty (Algorithms Mol. Biol. 21:4, first published 2025-12-10) already contains an exact partition function
over all orderings with rotational symmetries for the base-pair model (their Theorem 4, Lemma 12, Remarks 3-4);
we had read only the WABI 2024 version;
(2) the clause of Theorem 1 of the algorithm note on minimum free energy and level counts is not proved (the
conclusion is true; the referee gives the argument) — and six groups of minor findings.

What this review is and is not:
The referee was a separate AI agent instantiated by this division with an adversarial brief ("try to break the
claimed theorems"; re-derive, recompute with code written from the definitions, search for prior art).  It had no
access to our reasoning, only to the files of this branch.  **This is an internal AI review.  It is not
independent academic peer review**, and the results it covers remain unrefereed in the sense of the collaboration
README.  The report is reproduced verbatim below.  Paths in the report that point to a session scratch directory
refer to the referee's working directory; the referee's programs and outputs are preserved in
`experiments/complexity/reviews/rev3_strands_algorithm/` (downloaded papers, caches and the compiled binary are not).

---------------------------------------------------------------------------------------------------------------
REPORT (verbatim)
---------------------------------------------------------------------------------------------------------------

# Referee report (review 3): STRANDS_ALGORITHM.md and the post-review additions to STRANDS_NN_HARDNESS.md

## Bottom line

I could not break any stated theorem. In `docs/complexity/STRANDS_ALGORITHM.md` the orbit formula (1), the central-loop lemma, the bijection and the recursions are correct, and the operation count is right. `multiset_dp.magnified_pf` (and separately `G1` and every `Gd`) agreed with my own enumerator, written from the definitions before I opened the author's code, with 0 mismatches in about 17,800 comparisons of `Q_α` over 740 system runs. These covered 2–10 identical copies; 2–4 species with gcd of the copy numbers 2, 3, 4, 5, 6; palindromes; hairpin-forming and length-1 strands; α ∈ {−2,…,5, 40}; and non-integer α to 8·10⁻¹⁵. My own re-implementation of the document's algorithm with letter-dependent weights, which the author's code lacks, agreed with brute force in about 5,600 further comparisons. The quantity computed is the α-magnified partition function of Shalaby–Woods Definition 17. Two MAJOR findings concern what is claimed around the mathematics. First, the novelty paragraph is wrong as worded: the journal version of Boehmer–Berkemer–Will–Ponty (Dec 2025, the version Shalaby–Woods cite) already has an exact partition function over all orderings with rotational symmetries for the base-pair model, and the author read only the WABI 2024 version. Second, the MFE / density-of-states clause of Theorem 1 is not proved; the conclusion is true but needs a per-symmetry-class argument. The post-review additions to `STRANDS_NN_HARDNESS.md` are correct line by line and in my enumerations (2,380,760 structures, models at and beyond the hypotheses); only minor remarks. This is an internal AI review, not academic peer review.

The repository moved during the review (HEAD 36d86cc → 89114ea). `STRANDS_ALGORITHM.md` and `multiset_dp.py` did not change (sha256 da30943b…). In the hardness note only Theorem 1e and test counts changed.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | `Q_α` of §1 = Shalaby–Woods Def. 17 (physical ensemble, connected, unpseudoknotted, weight `w^α R^(−α)`); = Dirks et al. Eq. (2.2)–(2.3) at α = 1 | correct (notation `Ω̄` reversed, finding 7) |
| 2 | Lemma 2, formula (1) | correct |
| 3 | Lemma 3 (central loop) | correct; not new (finding 3) |
| 4 | Proposition 4 (bijection), weight formula | correct; formula (2) misprinted (finding 4) |
| 5 | §4 recursions and `multiset_dp.py` | correct with gaps (no written proof; no mismatch found) |
| 6 | Theorem 1: PF in `O(L_0⁴ Σ_{d∣gcd} Π C(n_i/d+2,2))` operations | correct |
| 7 | "polynomial for a bounded number of species" | correct (unit cost; also polynomial bit cost for rational weights) |
| 8 | Theorem 1: MFE and #SSEL "within the same bounds" | correct with gaps (finding 2) |
| 9 | §0 "What is and is not ours" | wrong as worded (finding 1) |
| 10 | §5 validation on 280 systems | reproduced; narrower than the theorem (finding 5) |
| 11 | §6 Remark 5 (interior loops are the only source of `N⁴`) | wrong (finding 6) |
| 12 | Hardness Theorem 1 with (H2′), steps (a′)–(e) | correct |
| 13 | Theorem 1c, both cases, identity (2), separator count, final claim using `B ≥ 2` | correct; hypothesis exact on my grid |
| 14 | Theorem 1d | correct |
| 15 | Remark 5 (several complexes) | correct |
| 16 | Corollary 4(ii) | correct (`U` loose, finding 8b) |
| 17 | Corollary 5 | correct given ETH and the sparsification lemma (the latter not checked) |
| 18 | Lemma A1 | correct (needs `ℓ_C ≥ 1`, finding 8a) |
| 19 | Lemma A2, sizes strictly between `B/5` and `B/3` | correct |
| 20 | Theorem 1e, both forms (added during the review, outside the brief) | proof read, correct; 0 violations |

## Findings

No CRITICAL finding.

**1. MAJOR (novelty / prior art).**
- **Place:** `STRANDS_ALGORITHM.md` lines 30–39; `THEOREMS.md` CX-T10 ("closed form over all orderings not found in print") and CX-T12 ("subset DP for a base-pair model without symmetry is Boehmer et al. (WABI 2024)"); `PRIOR_ART.md` A-III; `OPEN_PROBLEMS.md` lines 24–26 (journal version named, WABI PDF §§1, 2, 4, 6 read).
- **What is wrong:** The journal version (Algorithms Mol. Biol. 21:4, DOI 10.1186/s13015-025-00292-8, PMC13014723, first published 2025-12-10) replaces the WABI Remark 15 by a full section "Translation to partition function". Shalaby–Woods cite this version as [3]. It contains:
  - partition functions `Z_r` of r-symmetric structures, computed "without iterating over all circular permutations";
  - Lemma 12, a bijection `f: Ω_r(R) → Ω̄(R_/r)` between r-symmetric structures and "extended" structures on the strand set with every sequence r times less often, with one marked base pair and energy multiplied by r;
  - Lemma 14, a descending recursion over symmetry degrees;
  - Theorem 4: "The partition function Z over m strands can be computed in time O(3^m · n³ · m²)";
  - Remark 3 (the `kT log r` correction of Dirks et al. can be added) and Remark 4 (the technique carries over to the count-indexed triplet-repeat setting).
- **Consequence:** For the base-pair model, items (i) and (ii) of "Ours", and the species bound for the partition function in outline, are in print. The marked base pair there and the designated nest plus marked nick here encode the same quotient construction.
- **What remains new, as far as I found:** the nearest-neighbour version (central face charged as `m_a^α (m_b^k m_c^u)^{dα}` or as a two-pair loop for `d = 2, k = 1`; nick-free top levels; exterior loops over sub-multisets), arbitrary α with the closed form `J_{1−α}`, the explicit operation count, and a tested implementation. Shalaby–Woods v2 (23 Nov 2026) lists exactly this as open.
- **Fix:** Read and cite the journal version. Reword §0 to "we extend Theorem 4 / Lemma 12 of Boehmer et al. from the base-pair model to loop energies and to magnification α". Correct CX-T10/T12 and `PRIOR_ART.md` A-III. Credit the dichotomy "bounded number of distinct strands: XP; unbounded: NP-hard" to their Theorems 5 and 6 for their model.

**2. MAJOR (gap).**
- **Place:** `STRANDS_ALGORITHM.md` lines 26–28 and §6 Remark 3; `THEOREMS.md` CX-T12; `STRANDS_NN_HARDNESS.md` lines 525–537.
- **What is wrong:**
  - (a) Shalaby–Woods decode one ordering at a time (Algorithm 4: `for π ∈ Π: Z = Q_α(π)`; Lemma 39, Theorem 41 and Algorithm 7 take "strand ordering π"). The multiset algorithm never has `Q_α(π)`.
  - (b) Their decoding assumes all energy differences are multiples of ε (Remark 36) and fewer than `e^N` structures per ordering (Note 38). `ΔG` contains `kT ln R`, so levels of different symmetry classes are not ε-separated, and the classes cannot be separated from the single number `Q_α`. Their own Theorem 43 decodes per symmetry class. `e^N` also fails for the sum over orderings, and for this note's model, where hairpins with 0 unpaired bases are allowed (Motzkin numbers, about `3^N`).
  - (c) The hardness note's alternative, "the same recursion over (min,+)", yields `min_d (m_d + kT ln d)` with `m_d = min{E : d ∣ R}`. This lies below the true MFE whenever the loop-energy minimiser is symmetric. That is the difficulty Shalaby–Woods (ICALP 2025) handle by backtracking.
- **The conclusion is nevertheless true. Fix (half a page):**
  - Use `T_R(α) = Σ_{R∣d∣gcd} μ(d/R) F_d(α)`, the sum over pairs `(Y,S)` with symmetry exactly `R`; all `F_d` are already computed.
  - The number of pairs is at most `8^N · 3^N = 24^N` (letter string × nick positions × Motzkin). So for loop energies in `εℤ`, one evaluation at `e^{−ε/kT} := 2^{−K}`, `K = ⌈N log₂ 24⌉ + 1`, gives the level counts of each class exactly (Kronecker substitution, `O(N²)`-bit numbers). This is `α = Θ(N)` with constant `ln 24`, not 1.
  - Physical structures at `(E,R)` number `R/c` times the coefficient; MFE `= min_R (E_min(R) + kT ln R) + (c−1)ΔG_assoc`.
  - State the bit cost, and delete the (min,+) alternative or restrict it to the symmetry-naive MFE.

**3. MINOR (attribution inside the paper).**
- **Place:** `STRANDS_ALGORITHM.md` line 104 (Lemma 3) and lines 115–149 (nests, Proposition 4).
- **What is wrong:** Lemma 3, including the stack/interior case for `d = 2`, is Lemma 18 of Shalaby–Woods ICALP 2025 (arXiv:2407.09676), quoted in Shalaby–Woods 2026 Remark 29. "Nest" and "every nick lies in a nest" are their 2026 Def. 25 and Remark 26. The designated nest crossing the period border, with the cases one nest per slice / several, is their Lemma 31, Eqs. (39)–(40) and Algorithm 6 for a fixed ordering. `THEOREMS.md` CX-T11 says so; the paper does not.
- **Fix:** Cite at Lemma 3 and Proposition 4. The paper's own parts are the tree-automorphism proof, the marked nick (factor `|A|+1`) and the multiset tables.

**4. MINOR (formula (2); recursions unproved).**
- **Place:** `STRANDS_ALGORITHM.md` line 154 and §4.
- **What is wrong:** Read literally, `W(F)^α · … · B^{dα} · TOP^{(dα)}` counts the `m_b`, `m_c` factors of `F` twice. The implemented and correct formula is:
  - `m_a^α · m_b^{dα} · QM^{(dα)}(top)` when the top segment has at least one further nest;
  - `m_a^α · m_b^{dα} · m_c^{dαu}` for `k = 1, d ≥ 3`;
  - `il(u,u)^α` (exponent α, not dα) for `k = 1, d = 2`.

  §4 also omits the "at least 2 branches" table, the conventions (a stretch ending at `(t,0)` contributes 0 unless `A` is empty; `i < ℓ_s` for a nick after a strand of `A`), and any proof that each decomposition is unique.
- **Fix:** Write the exact formulas (about ten lines) and the uniqueness argument.

**5. MINOR (validation narrower than the statement; implementation edges).**
- **Place:** `STRANDS_ALGORITHM.md` line 15 and §5; `multiset_dp.py`.
- **What is wrong:**
  - Theorem 1 and §1 allow letter-dependent hairpin and two-pair weights; `multiset_dp.py` accepts only `hp(u)`, `il(l1,l2)`. The 280 systems also have `N ≤ 16`, at most 6 strands, and multi-species gcd ≤ 3. My runs close this gap, including the central two-pair loop `il(u; s_j, s_i; u; s_j, s_i)`: 0 mismatches.
  - No check that species are pairwise distinct: `magnified_pf(['GC','GC'],[1,1],…)` returns 3 for every α instead of 2, 3/2, 5/4.
  - A forbidden loop encoded as weight 0 is counted at α = 0 (`0**0 == 1`; single strand `GCGC`: 7 instead of 1) and raises `ZeroDivisionError` for α < 0. A minimum hairpin size must be a pairing constraint, which the code does not have.
  - Non-integer α silently switches to floats.
- **Fix:** State the tested scope in §5; add a distinctness assertion and a pairing predicate.

**6. MINOR (complexity remark).**
- **Place:** `STRANDS_ALGORITHM.md` §6 Remark 5 (line 219); `ASSUMPTION_AUDIT.md` §2 ("a restricted form would give `L_0³`").
- **What is wrong:** `Q`, `QM`, `Qs`, `QMs` are decomposed by the rightmost top-level pair with both ends free, costing `Θ(ℓ_t · L_0)` per entry regardless of interior loops. On one poly-A strand of length 16 / 32 / 64, `Tables.Qs` alone makes 3,060 / 46,376 / 720,720 pair tests (≈ ℓ⁴/24). Separately, `Rstart` is recomputed inside the exterior-loop sum (`O(k)` each); this is harmless since `k ≤ L_0`.
- **Fix:** Use last-base recursions (`Q(…;t,j) = Q(…;t,j−1) + Σ_d …`) together with the usual interior-loop treatment, or drop the remark. The stated bound itself holds: (pair tests + multiset splits) / bound ≤ 0.58 in all 33 instrumented runs, up to `(GGC)×64`, `(GGC,GCC)×(16,16)` and 8 distinct strands.

**7. MINOR (small inaccuracies).**
- (a) `Ω̄` is the physical ensemble here but the algorithmic one in Shalaby–Woods (their physical ensemble is `Ω`).
- (b) §6 Remark 2 "conditionally on two cited facts" is stale; after Appendix A only the sparsification lemma is cited.
- (c) "α = Θ(N)" needs the constant of finding 2.

**8. MINOR (hardness note).**
- (a) Lemma A1 (line 653): "at most three literals" must read "between one and three". An empty clause gives `ℓ_C − 1 = −1` garbage pairs and `|X| ≠ |W|`.
- (b) Corollary 4(ii) (lines 491–494): `U = n!·3^N` is valid but loose. The physical ensemble of `I` has at most `2^{mB−1}` distinct item orders times `C(2mB, mB)` nested chord sets, so `j = O(N)` suffices instead of `O(N log N)`.
- (c) Lines 535–537: see finding 2(c).

## What I computed

**Part 1 (`STRANDS_ALGORITHM.md`).**
- **Own enumerator** (`bf.py`, exact rationals): labelled strands, all `(c−1)!` orderings, faces by boundary walk, `R` as the number of slot rotations, physical ensemble as orbits under the full group of permutations of equal strands. On every structure these held: a unique non-crossing ordering; "≤ 1 nick per face" ⇔ union–find connectivity; `w` and `R` constant on orbits; `|orbit|·R = |G|`.
- **C++ enumerator** (`bfmod.cpp`, weights mod 2⁶¹−1), validated against `bf.py` on 19 systems × 4 models. In total about 1.1·10⁹ pairs `(Y,S)` were enumerated per model.
- **Author's DP against these references:**

| Run | Systems | Models | α | Mismatches |
|---|---|---|---|---|
| Definition-level (orbits) | 40 | 4 | 0, 1, 2, 3, −1, −2 | 0 |
| Fixed sweep (`G1`, each `Gd`, `Q`) | 375 (274 non-empty, 196 with symmetric structures, orders 2–10) | 4 | 0, 1, 2, 3, −1, −2, 5 | 0 |
| Random sweep | 299 | 4 | 0, 1, 2, 3, −1, 40 | 0 |
| Larger gcd 4 / 6 systems | 7 of 8 | 2 | 0, 1, 2, 3, −1 | 0 |
| Miscellaneous | 19 | 2 | 0, 1, 2, 3, −1 | 0 |

  The larger systems were `(GCC,GG)`, `(GGC,CC)`, `(GCG,C)`, `(GAC,GTC)` × (6,6) (the last with 4.47·10⁸ pairs), `(GA,TC,GC)` × (6,6,6), `(G,C,GCGC)` × (4,4,4), `(GA,TC,GC,AT)` × (4,4,4,4). `(GC,GGCC)` × (6,6) exceeded my 18-minute limit and was not checked.
- **Other checks:** α = 200 exact on one system; non-integer α (8 values, 11 systems, 3 models) agreed to 8.3·10⁻¹⁵. Models: unit; size-dependent with all of `m_a, m_b, m_c` non-trivial; a distinct prime ratio per loop size; hairpins below 3 forbidden by weight 0.
- **Own DP** (`mydp.py`, written from the document, letter-dependent `hp(u,a,b)` and `il(l1,a1,b1,l2,a2,b2)`): 228 + 120 + 19 systems against brute force with pseudo-random letter-dependent models, 0 mismatches; 338 comparisons with the author's DP on letter-independent models, all equal.
- The author's own tests reproduce (copies run in my directory).

**Part 2 (`STRANDS_NN_HARDNESS.md`).**
- **Enumeration:** 54 instances `I(a,m,B)` (`m ≤ 4`, `B ≤ 5`, including `B = 1`, `m = 1`, items longer than a block), 2,380,760 connected structures. "Tiling" was decided from the definition. No hairpin or multiloop occurred; the tiling count equals `Til/Π μ_s!` in all 54.
- **Theorem 1:** 7 models inside (H2′) × 2 values of σ, 0 failures; the gap `min(δ,|σ|)` is attained. With δ = 0 or −1/10 the conclusion fails on 40 instances (smallest: `a=(2), m=2, B=1`).
- **Theorem 1c:** 63 points `(x,γ)`. The 40 satisfying `|x| < |σ| + min(|σ|,γ)` had 0 failures on the 46 instances with `B ≥ 2`; the 23 others each fail on at least 13 instances. With `B = 1` there is no failure for `|x| < |σ|` and failure for every tested `|x| ≥ |σ|`.
- **Theorem 1d:** 140 models. The 70 with `D_G + D_C < |σ|` had 0 failures and the gap is attained; the 70 others each fail on some instance.
- **Theorem 1e:** first form 300 parameter sets, 0 violations. Second form (commit 89114ea) 12,329 (instance, model) pairs inside the hypotheses, 0 violations; the claimed failures at `x = σ, D_G = 0, D_C = ⅔|σ|, ⅚|σ|, B = 2` are confirmed.
- **Remark 5:** 15 instances × 2 models × 7 values of `ΔG_assoc`, 0 violations under its condition; the stated counterexample is confirmed.
- **Corollary 4(ii):** `⌊e^{βE_0} Z_j⌋ = N*` in 154 instance/model pairs.
- **Lemma A1:** all 7,140 formulas with 1–2 clauses on 2 variables (repeats allowed), 2,100 random and 150 larger ones; satisfiable ⇔ perfect matching, sizes as stated.
- **Lemma A2:** 860 random 3DM instances plus 300 without a perfect matching, checked with a generic packing search (no assumption of four items per bin); always equivalent. The chain A1∘A2 was checked on 9 tiny formulas.

## What I searched and read

**Read:**
- **Shalaby–Woods, arXiv:2611.27945v2** (PDF): §§1–7, Appendix B.2 (Algorithm 6) and B.3 (Algorithm 7); pages 12–13 rendered to see the over-bars. Not read: Appendix A, B.1, proof of Lemma 33.
- **Boehmer et al., WABI 2024** (LIPIcs PDF): abstract, §2.2, §4.1 (Theorem 14, Remark 15), §4.2 (Theorem 16), start of §4.3. Not the appendix.
- **Boehmer et al., Algorithms Mol. Biol. 21:4** (full-text XML from Europe PMC): the section "Translation to partition function" in full (Lemmas 8–14, Theorem 4, Remarks 3–4), the text around Theorems 3 and 5, the first paragraph of "Computational hardness". Not the supplement.
- **Dirks et al. 2007** (PDF): §2.1–2.2 (Theorems 2.1, 2.2, Eqs. 2.1–2.3) and the appendix note on exterior loops and dangles.
- **Shalaby–Woods ICALP 2025, arXiv:2407.09676:** Lemmas 15–18.
- **Ducloz–Shalaby–Woods, arXiv:2506.19756:** §1.3, Theorem 22 (statement and outline), Defs 25, 29, 30, Lemma 31 with proof.

**Web searches (7, results as snippets only):**
1. partition function, all strand orderings / circular permutations, subsets of strands, `3^c`, nearest neighbour, rotational symmetry
2. the Shalaby–Woods title with "3^c" and "follow-up"
3. indistinguishable strands with Burnside / necklaces / Pólya
4. Lorenz–Flamm–Hofacker–Stadler, co-folding of multiple RNAs
5. Boehmer et al., journal version
6. SoupFold, strand soup, Turner model
7. "magnified / magnifiable partition function", strand species

I found no nearest-neighbour version and no follow-up to Shalaby–Woods. Springer's page for the journal article was not reachable; I used Europe PMC.

## Strongest hostile objection

**Algorithm note.** "Given Boehmer et al. 2025 (Theorem 4, Lemma 12) and Shalaby–Woods 2026 (Lemma 31, Eqs. 39–40, central loop), this is the expected merger, and Shalaby–Woods ask for exactly it. The manuscript does not cite the journal version and claims two of its ideas. It gives no proof of its recursions and tests only letter-independent weights. It asserts the MFE consequence by a citation that does not apply. It counts unit-cost operations on Θ(N²)-bit rationals with alternating-sign coefficients (`J_{1−α}(d) < 0` for α > 1, so no floating-point version), with an `N⁴` that does not come from interior loops alone. What is the bit complexity, and is the species bound not already Remark 4 of Boehmer et al.?"

**Hardness note.** "The hardness is for an abstraction in which a nicked flush stack is worth 0, or less than the hypotheses of 1c/1e allow. In the parameter sets people run, coaxial stacking is about as strong as a stack and one-nucleotide bulges can be favourable — exactly the boundary `x = σ, γ ≤ 0` where the reduction fails. The instances also need one strand of length Θ(N) and unary sizes."

## Files

Everything is in `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3`; nothing under `/home/user/MetricChain` was touched. The main files:

- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/bf.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/bfmod.cpp
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/mydp.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/cmp2.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/cmp4_letters.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/complexity_qs.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/hard_test.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/hard_models.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/hard_1e_v2.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/eth_chain_test.py
- /tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review3/dl_bbwp/amb_tex.txt

The same directory holds the remaining drivers (`cmp1.py`, `cmp3_random.py`, `cmp5_frac.py`, `cmp6_big.py`, `cmp7_misc.py`, `val_cpp.py`, `drv.py`, `complexity_count.py`, `api_edge.py`, `api_edge2.py`, `hard_remark5.py`, `hard_1e.py`, `cor4_check.py`, `eth_no_instances.py`), all `*.out` and `*.log` outputs, `hard_cache.pkl`, the downloaded sources in `dl_*`, and verbatim copies of the author's files in `author_copy`.


---------------------------------------------------------------------------------------------------------------
DISPOSITION (completed 2026-11-26 21:24 UTC)
---------------------------------------------------------------------------------------------------------------

| # | finding | disposition |
|---|---|---|
| 1 | MAJOR (novelty): the journal version of Boehmer–Berkemer–Will–Ponty has an exact partition function over all orderings with rotational symmetries for the base-pair model; our "not found in print" was wrong as worded | **Accepted.**  We read the section "Translation to partition function" of the journal version in full (Lemmas 8–14, Theorem 4, Remarks 3–4) and the statements of its Theorems 5 and 6.  `STRANDS_ALGORITHM.md` §0 "What is and is not ours" rewritten: in print for the base-pair model (theirs); in print for a fixed ordering in the nearest-neighbour model (Shalaby–Woods); what this note adds (the nearest-neighbour version over all orderings, arbitrary magnification with the closed formula, the operation count, the decoding per symmetry class, a tested implementation).  The dichotomy "bounded number of distinct strands / unbounded" is credited to their Theorems 5 and 6 for their model.  `THEOREMS.md` CX-T10–T12, `PRIOR_ART.md` A-III(j), `OPEN_PROBLEMS.md` A6, `ASSUMPTION_AUDIT.md` §6 |
| 2 | MAJOR (gap): the clause on minimum free energy and level counts is not proved; [SW26, §7] decodes per ordering; the `(min,+)` alternative is wrong | **Accepted.**  New §4a with Proposition 5 (the referee's argument: `T_R = Σ μ(d/R) F_d`, at most `24^N` pairs, digits in base `2^K`, physical counts `N_R(m)·R/c`, the formula for the MFE, bit cost `O(cGN²)`); implemented with exact integers and compared with exhaustive enumeration on 17 systems (`level_counts.py`: all agree; the symmetry-naive value is too low in 11).  The `(min,+)` alternative is withdrawn in the hardness note as well.  Registered as CX-T30 |
| 3 | MINOR (attribution): Lemma 3 is Lemma 18 of Shalaby–Woods (ICALP 2025); nests and the crossing nest are [SW26] Def. 25, Remark 26, Lemma 31 | **Accepted**, after checking both texts: attributions at Lemma 3 and before Proposition 4; CX-T11 marked [P]/[K] |
| 4 | MINOR: formula (2) misprinted; §4 omits a table and conventions and has no uniqueness argument | **Accepted.**  Formula (2) replaced by the four implemented cases; conventions (a)–(d) and the paragraph "Why every pair (ordering, structure) is counted exactly once" added to §4 |
| 5 | MINOR: validation narrower than the theorem; no check of distinct species; weight 0 at `α ≤ 0`; non-integer `α` | **Accepted.**  §5 states the scope of our tests and reports the referee's; `multiset_dp.py` refuses duplicated species and weight 0 at magnification `≤ 0`, has a minimum hairpin size as a pairing constraint (`Model(min_hairpin=…)`), and documents the float behaviour; `test_multiset_dp_edges.py`.  Letter-dependent weights are still not implemented by us (the referee's `mydp.py` has them) |
| 6 | MINOR: Remark 5 on the source of `N⁴` is wrong | **Accepted.**  Remark 5 rewritten with the referee's counts; `ASSUMPTION_AUDIT.md` §2 corrected.  Last-base recursions not implemented |
| 7 | MINOR: (a) `Ω̄` reversed with respect to [SW26]; (b) a stale remark; (c) the constant in `α = Θ(N)` | **Accepted**: note in §1; Remark 2 updated; the constant `ln 24` in Proposition 5 |
| 8 | MINOR (hardness note): (a) Lemma A1 needs non-empty clauses; (b) `U = n!·3^N` is loose, `j = O(N)` suffices; (c) see 2(c) | **Accepted**: statement of Lemma A1; proof of Corollary 4(ii) (`U' = 2^(mB−1)·C(2mB, mB)`); "Further remarks" of §5; new §9a of the hardness note with the referee's verification counts |

The referee's "strongest hostile objection" to the algorithm note — given Boehmer et al. 2025 and
Shalaby–Woods 2026 this is the expected merger; the manuscript does not cite the journal version and claims
two of its ideas; no proof of the recursions; only letter-independent weights tested; the MFE consequence
asserted by a citation that does not apply; unit-cost operations on `Θ(N²)`-bit rationals; an `N⁴` that does
not come from interior loops alone — is accepted point by point; each item is now stated in the note
itself (§0, §4, §4a, §5, Remark 5).  "Is the species bound not already Remark 4 of Boehmer et al.?" — for the
base-pair model, yes; we say so.  To the hardness note — the hardness is for an abstraction at whose
boundary (`x = σ`, `γ ≤ 0`) the parameter sets in use sit — accepted as a limitation and stated in §8 and §9a.
