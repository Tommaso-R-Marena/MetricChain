# The NANUQ metric beyond level 2: blob-locality, and what six leaves can show

Companion to `NANUQ_LOCAL_CRITERION.md` (cited as [LC]; its §7.2 defines blobs, positions, pendant
subnetworks, the bloblet `𝔅°` and its split system `Σ(𝔅)`, and proves Lemma D).  Complexity division,
2026-11-26.  **Unreviewed.**  Register: `THEOREMS.md` CX-T31, CX-X3.  Labels as in [LC]: [P] paper proof,
[X] exact finite computation.

The source paper (Holtgrefe, Allman, Baños, van Iersel, Moulton, Rhodes, Wicke, Bull. Math. Biol. 2025) asks
for which networks the NANUQ metric is circular decomposable with the displayed splits as its support.
[LC] answers this for galled outer-labeled planar networks of every level (Theorem 7; probably a
rediscovery) and, completely, for outer-labeled planar networks of level at most 2 (Theorem 12).  This note
records what the same method gives **without a bound on the level**.

## 1. Blob-locality

`𝒦` is the class of tree-generated circular split systems all of whose six-point restrictions are
6-locally good (127 of the 150 six-point systems), `𝒦′` the class of those none of whose six-point
restrictions contains its three 3-splits without all six 2-splits (133 of 150); [LC] Theorems 4, 10, 10′.

**Theorem A (blob-locality, every level) [P + X].**  Let `N` be a binary semi-directed network on `n ≥ 4`
leaves that is outer-labeled planar with circular order `C`; no bound on the level.  Let
`Σ = Split(T(N))`.

(a) For six leaves `Y`: either `Σ|_Y` is 6-locally good, or `Y` meets six different positions of one blob
`𝔅` of `N`, and then `Σ|_Y = Σ(𝔅)|_Y`.

(b) `Σ ∈ 𝒦` if and only if `Σ(𝔅) ∈ 𝒦` for every blob `𝔅` of `N`; and `Σ ∈ 𝒦′` if and only if `Σ(𝔅) ∈ 𝒦′` for
every blob.

(c) If `Σ(𝔅) ∈ 𝒦` for every blob, `d_N` is circular decomposable with support exactly `Split(T(N))`; if
`Σ(𝔅) ∈ 𝒦′` for every blob, `d_N` is Kalmanson for `C`.  Conversely, if `Σ(𝔅) ∉ 𝒦` for some blob, then some
network obtained from a subnetwork of `N` by replacing leaves by clades violates the first conclusion; if
`Σ(𝔅) ∉ 𝒦′`, some such network has a NANUQ metric that is Kalmanson for no circular order.

(d) Let `S` be a circular split with end leaves `u_1, u_p, v_1, v_q` and `z, w` two further leaves on one side.
If the term `Φ6(z,w)` of `S` ([LC] Proposition 2) is negative, or is non-zero although `S` is not displayed,
then these six leaves lie at six different positions of one blob.  For a given split there is at most one
blob for which this can happen: the blob at four different positions of which its end leaves lie.

*Proof.*  (a) is Step 1 of the proof of [LC] Theorem 12, which nowhere uses the level: if some cut edge has
at least two leaves of `Y` on each side, `Σ|_Y` is a substitution of two tree-generated systems with at
least three leaves each ([LC] Lemma D(i), Lemma 7(ii)), and the 624 such systems on six points are all
6-locally good [X]; otherwise every cut edge has at most one leaf of `Y` on one side, the cut edges
directed towards the other side point to one blob, each pendant subnetwork of which contains at most one
leaf of `Y`, and [LC] Lemma D(ii) applies.
(b) "Only if": `Σ(𝔅)` is the restriction of `Σ` to one leaf per position (Lemma D(ii)), and both classes are
closed under restriction.  "If": by (a) a six-point restriction of `Σ` is 6-locally good or is a six-point
restriction of some `Σ(𝔅)`; for `𝒦′` note that a 6-locally good system does not have the forbidden pattern
([LC] Corollary 5′).
(c) [LC] Theorem 4 and Theorem 10′(a) with Lemma 1.  For the converse let `Y` be six positions of `𝔅` with
`Σ(𝔅)|_Y` outside the class; `Σ|_Y` is the system of the subnetwork `N|_Y` ([LC] Lemma 0), the blow-ups used in
the proofs of [LC] Theorem 10 and Theorem 10′ are the systems of the networks obtained from `N|_Y` by
replacing leaves by clades, and one of them fails as stated.
(d) The first sentence is (a) with the definition of "6-locally good".  If the end leaves of `S` lie at four
different positions of `𝔅` and `𝔅'` is another blob, then `𝔅'` lies in one pendant subnetwork `P` of `𝔅`, and all
leaves outside `P` — at least three of the four end leaves — lie in one pendant subnetwork of `𝔅'`.  ∎

So the question "for which outer-labeled planar networks does the conclusion hold, and keep holding when
leaves are replaced by clades" is, at every level, a question about **single blobs with six positions**:

> the conclusion holds robustly for `N` if and only if no blob of `N` has six positions on which its
> bloblet displays one of the 23 excluded six-point systems.

**Corollary B (Theorem 7 of [LC] again) [P].**  In a galled network the edge below a hybrid node is a cut
edge ([LC] Lemma B0), so every hybrid node of a blob is a position, `𝔅°` is a network all of whose hybrid
nodes have a leaf child, `Σ(𝔅) ∈ 𝒜 ⊆ 𝒦` ([LC] Lemma A, Lemma 8), and Theorem A(c) gives the conclusion for
galled outer-labeled planar networks of every level.  This is a second proof of [LC] Theorem 7; it uses
Lemma D instead of Lemma B and no induction.

**Corollary C (level 2).**  [LC] Corollary 14: a blob with two hybrid nodes has `Σ(𝔅) ∈ 𝒦` (equivalently
`∈ 𝒦′`) iff it is galled, or nested with at most one middle position.

**Remark (what Theorem A does not give).**  It decides the robust question.  For a single network a blob
outside `𝒦` does not imply failure: the weight of each affected split is a polynomial of degree two in the
sizes of the positions of its blob, with coefficients that are local terms of the blob's bloblet on at
most six positions, and its sign has to be computed — as [LC] Theorem 12 does for the nested blob with two
hybrid nodes, where the answer is not monotone in the number of leaves.

## 2. Six leaves and three hybrid nodes

Which of the 150 tree-generated six-point systems are displayed by outer-labeled planar networks?  By
Theorem A only the answer for networks on six leaves matters for the robust question, and by [LC] §7 the
150 systems fall into: the 108 systems of `𝒞_6` (those of galled networks); 19 further 6-locally good
systems; and 23 excluded systems — 14 that contain the three 3-splits, miss one, two or three 2-splits and
still have a good metric at six leaves; 3 with a negative split weight (two antipodal 2-splits missing); 6
with a positive weight on an undisplayed split (a 2-split and the 3-split incompatible with it missing).

`experiments/complexity/nanuq/six_leaf_survey.py` enumerates rooted binary networks on six leaves that are
outer-labeled planar for a fixed circular order, by repeated hybrid insertion into the 126 rooted planar
trees, and records the systems they display.

*(Results: §2.1, filled in from the logs of the program.)*
