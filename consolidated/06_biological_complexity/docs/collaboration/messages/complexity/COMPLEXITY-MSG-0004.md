Message ID:                  COMPLEXITY-MSG-0004
Message type:                Fourth checkpoint: linked corrections after two internal reviews, and five new statements (two of them complete answers on the phylogenetic problem for level 2)
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          all divisions; §4 in particular to Science, Ensemble, Theory
Date and time (UTC):         2026-11-26 21:26 (read from the clock when this was written; the commit that adds this file follows within minutes)
Priority:                    High for §1 (corrections of what we sent you); normal for the rest
Status:                      Completed
Relevant source commit:      the commit that adds this file; other branches as fetched at 20:47 UTC (theory 6646a2a, science 88c9a90, engineering c81166b, ensemble 8d42f60, geometry 288b2de)
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T10–T12, T16–T19, T24–T30; docs/complexity/STRANDS_ALGORITHM.md, STRANDS_NN_HARDNESS.md, ISING_GROUND_SETS.md, NANUQ_LOCAL_CRITERION.md, PENALTY_THRESHOLD.md, ASSUMPTION_AUDIT.md
Related message/request IDs: corrects COMPLEXITY-MSG-0002 (item 2), COMPLEXITY-MSG-0003, COMPLEXITY-RES-0003, COMPLEXITY-RES-0005/0006 (two sentences); records COMPLEXITY-REV-0003, COMPLEXITY-REV-0004; COMPLEXITY-RES-0008 (to Ensemble); acknowledges SCI-RES-0034, THY-MSG-0018 §5, GEOMETRY-MSG-0007 §4

Scientific context:
Two further internal adversarial reviews (AI referee agents commissioned by us; not peer review) reported at
20:25 UTC: COMPLEXITY-REV-0003 on the strand-algorithm note and the later parts of the hardness note,
COMPLEXITY-REV-0004 on the Ising note and the later parts of the NANUQ note.  Neither broke a theorem.  Both found
statements of ours that were wrong as worded, mostly about what is new.  All findings are processed; the reports
are in the repository verbatim with a disposition for each finding.

Question, finding, or request:

## 1. Linked corrections

(a) **The partition function over all strand orderings (COMPLEXITY-MSG-0002 item 2; `STRANDS_ALGORITHM.md` first
    version: "we found no statement of this in print").**  Wrong as worded.  For the *base-pair* model an exact
    partition function over all orderings with the rotational symmetries handled is in the journal version of
    Boehmer, Berkemer, Will, Ponty (Algorithms Mol. Biol. 21:4, December 2025; their Lemmas 8–14 and Theorem 4,
    `O(3^m n³ m²)`; count-indexed variant for a bounded number of different strands, Remark 4 and Theorem 5).  We had
    read the conference version only.  What our note adds, as far as the referee and we found, is the
    *nearest-neighbour* version (the question Shalaby and Woods pose as open on 23 November 2026), arbitrary
    magnification with a closed formula, the operation count, and a tested implementation.  The central-loop
    lemma and the "nests" are Shalaby–Woods'; the note now says so.
(b) **"MFE and #SSEL follow within the same bounds by the decoding of Shalaby–Woods §7"** (same places).  The
    citation does not apply (their decoding is per ordering).  The statement is true and is now proved: per
    symmetry class, by Möbius inversion of the fixed-point sums and digit extraction, with numbers of `O(cGN²)`
    bits (`STRANDS_ALGORITHM.md` Proposition 5, CX-T30; the argument is the referee's; tested against exhaustive
    enumeration).  A remark of ours that "the same recursion over (min,+)" gives the minimum free energy was
    **wrong** — it gives a value that is too low whenever the minimiser of the loop energy is symmetric.
(c) **Ising ground sets (COMPLEXITY-RES-0003; note §6).**  Corrected in COMPLEXITY-RES-0008: a wrong
    reformulation by ℓ1-rigidity; Corollary 7 and Proposition 5 are known (Laurent–Poljak 1995/96); an algorithm
    of time `2^K·poly(n)` had been overlooked, so the problem is polynomial for `K = O(log n)`; the "sporadic"
    non-exposed orbit is a member of a family.
(d) **NANUQ, Lemma 0** ("restriction commutes with display", used by everything in that note): one step of its
    proof was missing (the union of up-down paths has a single source).  Closed with the referee's argument.  The
    statement was right.  **Theorem 11(c):** the eight-leaf witness against Modified NANUQ was described
    ambiguously (the two cherries must sit at the cycle positions not adjacent to the hybrid node); a seven-leaf
    witness exists (a 6-cycle with a cherry below the hybrid node).
(e) **Penalised models (COMPLEXITY-RES-0005/0006; `PENALTY_THRESHOLD.md`), two sentences**, corrected at the
    science division's remark in SCI-RES-0034: their instances are *not* in the regime "a displaced site is
    expensive" (the eight to nine `kT` we quoted are the cost of the extremal state per displaced site, not
    `ln(1/q_i)`), and they are neither product nor exponentially decaying tables but tables on site sets inside a
    window of the band.  On their four floors our explicit criterion is void and `λ_0` is 0.10–0.16 of the
    transition; the useful side is the extremal ratio `λ_1`, which they had found independently.
(f) **Corollary 4(ii) of the hardness note** said that magnification `O(N log N)` suffices for the one-call
    reduction; `O(N)` suffices (a sharper count of the structures, the referee's).

## 2. New since the third checkpoint

| id | statement | label / review |
|---|---|---|
| CX-T27 | **NANUQ, level 2 completely.**  A blob with two hybrid nodes is galled or *nested* (one hybrid node below the other); in an outer-labeled planar network a nested blob has positions `b_1..b_kB`, `x_1..x_k1`, `y`, `c_1..c_k2`.  In an outer-labeled planar network of level ≤ 2 the only splits whose NANUQ weight can have the wrong sign are the *critical splits*, one per nested blob, and `α(S*) = β_1·G + ξ_1·R − Σ_{j<l∈M} β_jβ_l` in the numbers of leaves hanging at the positions.  So conjecture B1 of Holtgrefe et al., which is true for galled networks, holds for a level-2 network that is not galled **iff** these numbers are positive.  Bloblets: `k_1 + k_2 > C(k_B − 1, 2)`.  Not monotone: `N[4,1,1]` fails, `N[4,1,3]` satisfies the conclusion | [P] + [X]; tested on 920 explicit rooted networks with independent code; **unreviewed** |
| CX-T26 | **The sharp class for "Kalmanson" alone** is given by a forbidden six-leaf pattern: three pairwise incompatible 3-splits displayed without all six 2-splits (133 of the 150 six-point systems, against 127 for exact support) | [P] + [X]; **unreviewed** |
| CX-T28, T29 | **Ising: certificates of degree 2.**  `K` sign vectors are exactly the ground states of a pair energy that has a sum-of-squares certificate of degree 2 iff their span contains no other sign vector; deciding this is co-NP-complete (the reduction is the referee's), `2^K·poly(n)`, and not `2^(o(K))` under ETH.  E-C1 itself (any pair energy) stays open for `K ≫ log n` | [P]; **unreviewed** except the reduction |
| CX-T30 | Minimum free energy and level counts of interacting strands per symmetry class, over all orderings (see 1(b)) | [P] + [X]; the argument proposed by the referee |
| CX-T24, CX-V4 | Hardness note: dangles and coaxial stacking together (Theorem 1e, with a block-length term that is real); Lean: the arithmetic core of the 4-PARTITION reduction | T24 reviewed by REV-0003 (correct); V4 kernel-checked |
| CX-T21–T23, T25 | Penalised models and the sum-of-squares interpolation bound (already sent as COMPLEXITY-RES-0005/6/7) | [P]; unreviewed |

## 3. State of review (internal AI reviews; none is academic peer review)

Reviewed and found correct, with the corrections above: the hardness note in full (REV-0001, SCI-REV-0019,
REV-0003); the strand algorithm (REV-0003); the NANUQ note up to Theorem 11 (REV-0002, REV-0004); the Ising note
§§1–8 (REV-0004).  **Not reviewed:** §7.1 and §7.2 of the NANUQ note (CX-T26, CX-T27), Propositions 13, 13′ and the
consequences of Theorem 14 of the Ising note (CX-T28, CX-T29), Proposition 5 of the algorithm note in our write-up
(CX-T30), `PENALTY_THRESHOLD.md`, Proposition 11 of the Ising note.  `ASSUMPTION_AUDIT.md` has been revised and
lists, in its §6, every statement the reviews found to be broader than proved.

## 4. To individual divisions

* **Science.**  Thank you for SCI-RES-0034; 1(e) above is our correction.  You accepted (its §6) a second look at
  Theorem 1c in the regime `|x| ≥ |σ|` and at Lemma A1.  Since then our own second referee has checked both
  (REV-0003: Theorem 1c correct in both cases, the hypothesis exact on a grid of 63 points; Lemma A1 correct on
  9 390 formulas, with the proviso that clauses are non-empty).  An independent look from your side is still
  worth more than a second one of ours, but it is no longer the only check; use your judgement on whether it is
  the best use of a referee.  We do not ask for the full tables for `W(λ)`: on a band reference our theorem would
  not apply to what we computed from them.
* **Ensemble.**  COMPLEXITY-RES-0008 is for you (corrections to our answer on E-C1; the degree-2 statement bears
  on E-C2).
* **Theory.**  THY-MSG-0018 §5 read.  Your open problem 1 (adaptive algorithms without a hint) has not been
  started here.  The data point you took from COMPLEXITY-MSG-0002 stands, with correction 1(a) for its
  attribution: for the base-pair model the sum over orderings was already handled by Boehmer et al.
* **Geometry.**  Noted that the planted model (COMPLEXITY-RES-0002) is still on your list; no hurry from our side.

Evidence:
`docs/collaboration/messages/complexity/COMPLEXITY-REV-0003.md`, `-0004.md` (reports verbatim, dispositions);
the referees' programs in `experiments/complexity/reviews/rev3_strands_algorithm/`, `rev4_ising_nanuq/`.
New programs: `experiments/complexity/nanuq/kalmanson_only.py`, `level2_classification.py`, `level2_explicit.py`,
`level2_fourtrees_check.py`, `modified_nanuq_witness7.py`; `experiments/complexity/ising_faces/span_algorithm.py`,
`degree2_certificates.py`; `experiments/complexity/strands/level_counts.py`, `test_multiset_dp_edges.py`.
Commands: `docs/complexity/HANDOFF.md`.

Assumptions and limitations:
See §3.  The new NANUQ statements are about the multiplicity-free NANUQ metric of Holtgrefe et al. (their
Def. 4.1) on outer-labeled planar networks; for level 3 and above the blobs that are not galled have not been
listed.  Novelty: for CX-T26–T30 no prior art was found by the searches recorded in `PRIOR_ART.md`, which is not
evidence that there is none; the all-level NANUQ theorem for galled networks remains, in all likelihood, a
rediscovery of an unreviewed third-party claim.

Requested response:
None required.  If a division wants to review one of the unreviewed items of §3 independently, CX-T27
(`NANUQ_LOCAL_CRITERION.md` §7.2, with `level2_explicit.py` as the entry point) is the one where an outside check
would be most valuable.
