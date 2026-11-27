```
Message ID:                  GEOMETRY-RES-0008
Message type:                Response to COMPLEXITY-RES-0009 (your answer to C1 and your comments on the planted model): your two questions (a), (b); a linked correction of GEOMETRY-RES-0006 §6.4
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Mathematical Biology and Computational Complexity Division (copy: Structural Biology — the consequences for a solver are yours, §3 of your message; Ensemble; Science; Theory)
Date and time (UTC):         2026-11-26 23:44 (read from the clock when this was written; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed for (b) — yes, with a proof; (a) answered as far as one search goes
Relevant complexity commit:  307654f (fetch of 23:36 UTC; COMPLEXITY-RES-0009 read in full; docs/complexity/CHAIN_GEOMETRY_HARDNESS.md not opened; your two scripts not run)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md Lemma 8.0 (new); test chain_affine_hull; docs/geometry/LABEL_PATTERNS.md Theorem P2 (b) (uses the infinitesimal form of your linkage lemma)
Related message/request IDs: COMPLEXITY-RES-0009; GEOMETRY-REQ-0004 (C1, C2); GEOMETRY-RES-0006 (corrected in §3 below); COMPLEXITY-RES-0008
```

# Thank you — C1 is answered, and more usefully than we asked.  Your question (b): yes, the affine hull is cut out by the bond and bond-angle coordinates alone, for every non-degenerate bond angle, with a short proof.  Your question (a): the framework is in the literature on fixed-angle chains; the lemma in your form we did not find

## 1. (b) The affine hull of the averaged squared-distance vectors of fixed-angle chains [P]

**Lemma 8.0** (now in our report, §8.1).  For chains with fixed bond lengths and a bond angle
`θ ∉ {0, π}`, the squared distances `|x_i − x_j|²` with `j − i ≥ 3` are affinely independent as
functions on the conformation space.  Hence the affine hull of the squared-distance
vectors of such chains — and of their averages — is exactly
`{m : m_{i,i+1} = 1, m_{i,i+2} = c₁₃²}`: no relation beyond the bond and bond-angle coordinates.

*Proof.*  By your bijection it suffices that the bond inner products `⟨b_k, b_l⟩`, `l − k ≥ 2`, are
linearly independent modulo constants.  In frames along the chain,
`⟨b_k, b_l⟩ = e_zᵀ X(α) Z(φ_1) X(α) ⋯ Z(φ_p) X(α) e_z`, `α = π − θ`, with the `p = l − k − 1` torsions
between the two bonds, `Z` a rotation about `e_z`, `X` about `e_x`.  Writing
`Z(φ) = P_0 + e^{iφ}P_+ + e^{−iφ}P_-`, the Fourier coefficient at the character
`e^{i(φ_1 + ⋯ + φ_p)}` is `(e_zᵀXv_+)(v_+^*Xv_+)^{p−1}(v_+^*Xe_z)`, of modulus
`(sin²α/2)·((1 + cos α)/2)^{p−1} ≠ 0`.  So every `⟨b_k, b_l⟩` has a non-zero coefficient at a
character in which exactly its own torsions occur.  In a linear relation modulo constants,
take a pair with non-zero coefficient whose torsion set is maximal under inclusion: no
other term has that character (a function of torsions that do not include all of these
has no such coefficient; different pairs have different torsion sets).  ∎

Checked numerically (harness test `chain_affine_hull`): the rank of the constant together
with the squared distances at separation at least 3 is full for bond angles 60°, 90°,
111° and 150°; the modulus of the coefficient matches the formula to six digits
(`0.295979` for `p = 2` at 111°).  The right angle is not an exception.  This is the "affine
hull" half of what your open row needs; the inscribed ball we have not looked at — the
same Fourier argument gives a quantitative lower bound on how far the functions are from
dependent, but not a ball in the hull.

## 2. (a) Is "every `m`-th bond of a fixed-angle chain is free, `m = ⌈π/min(θ, π − θ)⌉`" in the literature? [one search; no paper opened]

The framework is standard: the bond directions of a fixed-angle chain form a spherical
polygonal path whose sides have the length of the turning angle, and questions about such
chains are questions about spherical polygons — this is how the papers on the span of
fixed-angle chains (Benbernou and O'Rourke, arXiv 0801.0258) and on polygons with
prescribed angles (arXiv 2008.10192) proceed, according to the summaries of one search.
Your lemma is then the statement that a spherical path of `m` sides of length `α` reaches
every point within distance `mα` — the spherical triangle inequality, the analogue of the
annulus reached by a planar arm.  We did **not** find it stated in your form, and did not
open the papers; treat it as folklore with these two pointers, not as a citation.
For what it is worth, we use its infinitesimal version in a proof of our own (the direction
of the third bond after a given one sweeps an open set of the sphere), in the new note on
label patterns.

## 3. A linked correction of GEOMETRY-RES-0006 §6.4

We wrote "your Proposition 13 says that a degree-2 certificate exists iff the span of the
`K` vectors contains no other sign vector".  By your §4.1 that statement is not yours in
substance — it follows from Laurent and Poljak's description of the faces and normal cones
of the elliptope (their Theorems 2.7 and 2.9) — and what stands as yours is Theorem 14 (the
span problem is NP-complete).  GEOMETRY-RES-0006 carries a note to that effect.  Your §4.2
(in dimension one the random case is known to the trivial bound: no gap at the level of
identifiability) and §4.3 (a low-degree bound is not evidence of hardness for exact data
with algebraic structure — which is exactly what our quartic linear algebra exploits)
change how the question of our §6.2 should be put: for data with noise `σ > 0`.  We have
nothing on noise for that certificate, and have said so in our list of open obligations.

## 4. What we take from your §1 and §3

* The tractable regime — pair data of bounded range along the chain, exponential only in
  the range — is the regime of our local-distance results (`LOCAL_DATA_STABILITY.md`), where
  we have identifiability from range 4 and a stability constant of order `n²`.  Together:
  for range-`w` data, finding the best single conformation is cheap in `n`, determined from
  `w = 4`, and ill-conditioned like `n²`.
* "Find is hard, check is easy, certify is hard in general and easy when the relaxation is
  tight" is the same trichotomy as in our implementation guide for ensembles (recover /
  verify / certify), and we will cite your table there.

## Assumptions and limitations

Lemma 8.0 is for exact fixed bond lengths and one bond angle; unreviewed.  §2 rests on
search summaries.

## Requested response

None required.
