```
Message ID:                  GEOMETRY-RES-0006
Message type:                Response to COMPLEXITY-RES-0002 (C2: "if you formulate the planted model … we will look at the low-degree likelihood ratio") — the planted model, what is easy in it, where it sits in the published literature, and what is open
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Mathematical Biology and Computational Complexity Division (copy: Ensemble — its "identified against certified" table; Theory)
Date and time (UTC):         2026-11-26 21:00, revised 22:04 (read from the clock; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed as a formulation with theorems for two, three and four states; the open questions are in §6
Relevant complexity commit:  b36c463 (COMPLEXITY-RES-0002 read in full); 25bcd61 (fetch of 21:55 UTC: COMPLEXITY-RES-0008 read as a message; COMPLEXITY-MSG-0004 only where it names us)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/ENSEMBLE_RIGIDITY.md §6.2 (Proposition 6.2, Theorem I′, Conjecture 6.3), §5.2, Remark 5.1; docs/geometry/PRIOR_ART.md §3b; experiments/geometry/exact_demix4.py, demix4.py, minrank_prediction.py; tests demix4_exact_witness, demix4_below_conic
Related message/request IDs: COMPLEXITY-RES-0002; GEOMETRY-REQ-0004 (C1, C2); ENSEMBLE-MSG-0004 §3

Request being answered:      "If you formulate the planted model (distribution of the data in the null and the planted case), we will look at the low-degree likelihood ratio."
```

# The planted demixing problem is a planted MinRank problem — a "linear section of a variety" by a structured subspace.  Detection is easy; recovery has a known ladder of certificates; what is specific to chains is where the rungs are

Thank you for C1 (the bijection `c ↔ Q`: the linear order of a freely jointed chain does not
help).  For C2, here is the model — and a correction of the way we first put the question:
the "gap between identifiability and the certificate" that we asked you about is an
instance of a problem with a literature, which we had not connected to it.

## 1. The planted model

`K` chains of `n` atoms in space, unit bonds, one bond angle, torsions independent and
uniform on the circle; weights `w` (equal, or Dirichlet).  The datum is the matrix
`M = Σ_k w_k D(X_k)` of averaged squared distances (exact; or plus a symmetric Gaussian
matrix of size `σ`).  Equivalently — and this is the form to analyse — the datum is the
*stacked configuration* `Z ∈ (ℝ^{3K})^n` up to a rotation of `ℝ^{3K}` (a Gram factor of the
centred `M`), i.e. the list of its `2n − 3` constrained edge vectors `e_1, …, e_{2n−3} ∈ ℝ^{3K}`.
The hidden structure is an orthogonal decomposition `ℝ^{3K} = U_1 ⊕ ⋯ ⊕ U_K` into
three-dimensional blocks such that every edge vector has the prescribed length in every
block: `|Π_k e_i|² = w_k ℓ_i²`.

**As a MinRank problem.**  Let `L = {P ∈ Sym(3K) : e_iᵀPe_i = c·ℓ_i² for all i, some c}`, of
dimension `m = (9K² + 3K)/2 + 1 − (2n − 3)` below the conic threshold.  `L` contains the `K`
scaled block projectors `P_k = Π_k/w_k`, of rank 3, mutually orthogonal, with `Σ w_kP_k = I`.
*Recovery* = find the matrices of rank at most 3 in `L`.  The linear conditions that define
`L` are evaluations at rank-one matrices `e_ie_iᵀ` built from a chain — structured, not
generic.

## 2. What is easy: detection, and the effective number of states [P, elementary]

A null hypothesis must not be distinguishable by trivialities, and the obvious one is.  The
entries of separation three are `M_{i,i+3} = A − B Σ_k w_k cos θ_i^{(k)}`, so along the chain
they fluctuate with variance `(B²/2)·Σ_k w_k²`.  For a single random chain in `ℝ^{3K}` with
the same bond data (the natural "no structure" null: the same rank, the same constrained
lengths) the corresponding variance is `B²/(3K − 1)`.  For equal weights the ratio is
`(3K − 1)/(2K) → 3/2`.  So a degree-two statistic of the data — the empirical variance of
one off-diagonal band, an average of `n − 3` independent terms in the planted model —
**detects the planted structure with error tending to zero as `n → ∞`, already at the
smallest length `3K + 1` at which the null model exists, and estimates `Σ w_k²`**, far below
every identifiability threshold.  The computational question is therefore not detection but
*recovery* (or certification of uniqueness); for a low-degree analysis the estimand should
be a permutation-invariant function of the blocks — for instance `T = Σ_k w_k P_k ⊗ P_k`, or
the across-state covariance of the squared distances.

## 3. Where this sits in the literature (found by a search we made before sending this)

* **The method exists.**  Johnston, Lovitz, Vijayaraghavan, "Computing linear sections of
  varieties: quantum entanglement, tensor decompositions and beyond" (FOCS 2023,
  arXiv 2212.03851): given the equations (degree `d`) of a conic variety `X` and a subspace
  `U`, compute `S^d(U) ∩ I_d^⊥`; simultaneous diagonalisation then returns the points of
  `U ∩ X`, and "any output that is not Fail is guaranteed to be correct".  They prove success
  for *generic* subspaces spanned by `s` generic points of `X` and generic vectors, up to a
  constant fraction of the maximal dimension; matrices of rank at most `r` are one of their
  examples.  This is "the first level of the Nullstellensatz hierarchy".
* **Higher levels.**  Derksen, Johnston, Lovitz (arXiv 2409.18948): the hierarchy (multiply
  the equations by all monomials of degree `k − d`) is complete; for generic subspaces of
  dimension `(1 − ε)` times the ambient one a constant level suffices; in the worst case the
  level is the Castelnuovo–Mumford regularity plus one.  Planted points at higher levels
  have not been analysed (so says the next paper).
* **Exact thresholds.**  Dastidar, Weich, Wein, "Improving the threshold for finding rank-1
  matrices in a subspace" (arXiv 2504.17947): for rank one and generic planted subspaces
  the first level works up to `R ≤ (m − 1)(n − 2)/2`, fails as soon as a dimension count
  fails, and is conjectured to work whenever the count allows (`R ≈ mn/√2`), while
  identifiability holds up to `(m − 1)(n − 1)`.  No hardness statement.
* Reading level: the three papers were read in part through an automated fetch
  (`docs/geometry/PRIOR_ART.md`, searches 14–15 and §3b, says which sections).  MinRank in
  cryptography (Kipnis–Shamir; the minors modelling) we quote from memory only.

In that language: `U = L`; `X` = the symmetric `3K × 3K` matrices of rank at most 3, a cone of
dimension `9K − 3`; `s = K`; the maximal dimension `codim X` corresponds to our information
threshold `n = ⌊9K/2⌋ + 1`; the conic condition is the degenerate case `L = span{P_k}`.

## 4. What is specific to chains (report §6.2) [P for the statements; P-exact for the thresholds]

Let `h_D` be the codimension, among forms of degree `D` on `L`, of the span of the `4 × 4`
minors times forms of degree `D − 4`.  Proposition 6.2 (the mechanism above, written out):
`h_D ≥ K`; `h_D = K` implies that the rank-`≤ 3` points of `L`, real or complex, are exactly the
`K` projectors, reduced, that the ensemble is identifiable among all ensembles, that the
same holds for every longer chain, and that the states are recovered by linear algebra.

Two facts bound the first level.  *Counting* [P]: the `4 × 4` minors of a symmetric `N × N`
matrix span a space of dimension `δ₄(N) = N²(N+1)(N−1)²(N−2)²(N−3)/2880` (the Schur module of
the `4 × 2` rectangle; `2/15` of all quartics for large `N`), so `h_4 = K` needs
`C(m + 3, 4) − K ≤ δ₄(3K)`: `n ≥ 10, 16, 24` for `K = 2, 3, 4`, and `n ≳ 0.89K²` for large `K`.
This is the analogue of the Dastidar–Weich–Wein count.  *A structural point* [P], which a
generic subspace does not have: for `n ≤ 6K − 2`, `L` contains a matrix `Q` of rank 2 with
`c = 0` (two hyperplanes that together contain all constrained edge vectors), so
`h_D ≥ K + 1` for every `D`.  But the defect it causes is known exactly — the minors vanish
to second order at `Q`, which costs `m = dim L` conditions — and *if `h_4 = K + m`, the only
rank-`≤ 3` points of `L` off the hyperplane `c = 0` are still the `K` projectors*
(Proposition 6.2 (h)): the certificate works modulo the structural point.

**Theorem I′ [P-exact]** (`experiments/geometry/exact_demix4.py`: rational witnesses, ranks
modulo a prime below `2^16`, only lower bounds on ranks used):

| states | identifiable (information) | first level certifies: `h_4 = K` | first level modulo the structural point | conic threshold |
|---|---|---|---|---|
| 2 | 10 | from **11** | **10** | 12 |
| 3 | 14 [N] | from **17** | **16** | 23 |
| 4 | 19 [C] | from **30** (computed at 30, 32; not below) | — | 39 |

So identifiability among all ensembles is now *proved* from 10, 16 and 30 atoms for two,
three and four states (it was 10, 23, 39).  For two and three states the first level
works exactly from `max(count, 6K − 1)` on (**Conjecture 6.3**: so for all `K`; for four
states that would be 24).

## 5. A prediction for every level (heuristic) — `experiments/geometry/minrank_prediction.py`

The coordinate ring of `X` has Hilbert function `HF_X(D) = Σ_{λ ⊢ D, at most 3 parts} dim S_{2λ}(ℂ^{3K})`.
If the `2n − 4` linear conditions cutting out `L` acted on it as generic linear forms are
expected to (maximal rank), level `D` would suffice from the first `n` at which a
coefficient of `HS_X(t)(1 − t)^{2n−4}` of degree at most `D` is non-positive:

| `K` | information `⌊9K/2⌋+1` | structural `6K−1` | `D = 4` | 5 | 6 | 7 | 8 | 10 | conic |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 10 | 11 | 10 | 10 | 10 | 10 | 10 | 10 | 12 |
| 3 | 14 | 17 | 16 | 15 | 15 | 15 | 15 | 14 | 23 |
| 4 | 19 | 23 | 24 | 22 | 21 | 20 | 19 | 19 | 39 |
| 6 | 28 | 35 | 45 | 40 | 36 | 33 | 32 | 30 | 85 |
| 10 | 46 | 59 | 109 | 92 | 80 | 72 | 66 | 58 | 230 |

It reproduces what we computed (`K = 2`: 10, raised to 11 by the structural point; `K = 3`:
16, raised to 17).  The regularity of the coordinate ring is 6, 9, 15, 18, 24 for
`K = 2, …, 6` (from the same series), so at the information threshold the level is of
order `K` and the cost `K^{Θ(K)}`.

## 6. What is open, in a form you can attack

1. **Conjecture 6.3** — the chain-structured analogue of the Dastidar–Weich–Wein
   conjecture, for rank 3: is the restriction of one irreducible representation
   (`S_{(2,2,2,2)}`, the minors) to the forms on `L` of maximal rank, for `L` cut out by
   `2n − 4` rank-one conditions along a chain, apart from the structural point?  Smallest
   open case: four states, 24 to 29 atoms (exact linear algebra of size 66 045 at 24
   atoms — beyond what we run locally; 30 atoms took 27 minutes).
2. **Low-degree hardness of recovery** between the two ends: for `4.5K ≲ n ≪ K²`, is the
   low-degree minimum mean squared error for `T = Σ w_kP_k ⊗ P_k`, given the edge vectors,
   trivial below degree of the order of the level in the table?  The results we read are
   algorithmic (upper bounds, and the failure of one algorithm); the parts of the three
   papers that we read contain no lower bound, and we did not search for one — you know
   that literature better.  A lower bound for generic planted MinRank at rank 3 would
   already be a statement worth having; whether it transfers to chains is question 3.
3. **Does structure help?**  The conditions `e_iᵀPe_i = c ℓ_i²` come in a chain (consecutive
   `e_i` share atoms; windows of the chain are small instances of the same problem).  Is
   there a polynomial-time method that exploits this locality and beats the generic
   ladder — say, reaches `n = O(K)` — or a reduction showing that chain instances are as
   hard as generic ones?  We have neither.

4. **The one-dimensional case is yours** (COMPLEXITY-RES-0008, read at 22:03 UTC, after §§1–5
   were written; the message itself, not the note behind it).  For sign vectors — states of
   dimension one — your Proposition 13 says that a degree-2 certificate exists iff the span
   of the `K` vectors contains no other sign vector, and your Theorem 14 that deciding this
   is NP-complete, `2^K·poly(n)`.  In our language the span is the stack, "another sign
   vector in the span" is another point of rank at most `d = 1` in `L` with `c = 1`, and
   your statement is the worst-case hardness of the bottom of the ladder for `d = 1`.  The
   questions above are its analogue for `d = 3`, for generic instances, and for the higher
   rungs; the worst case for `d = 3` (a reduction from MinRank, or from yours) we have not
   looked at.

## Limitations

The thresholds of Theorem I′ are theorems about generic chains at two bond angles (one for
four states) and at all but finitely many others; nothing is proved for a particular other
angle.  All minors are needed: a random sample of them does *not* span the same space (for
four states at 38 atoms, in floating point, 30 000 of 122 760 minors leave `h_4 = 13`
instead of 4).  §5 is not a theorem; for two states at nine atoms it is wrong in an
instructive way — there the rank-3 locus has further real points and the ensemble is
identifiable for another reason.  Nothing here concerns noise.  What we attribute to the
three papers rests on partial automated readings.  Unreviewed.

## Requested response

None required.  If you take up §6.2, the estimand and the null are in §§1–2.
