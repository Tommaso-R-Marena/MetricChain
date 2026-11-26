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

(e) Let the end leaves of `S` lie at four different positions `π_1, π_2 | π_3, π_4` of a blob `𝔅` ("`S` cuts
`𝔅`").  Then

```
α_S / 2  =  Φ4  +  Σ_π  m_π · Φ5(π)  +  Σ_{π < ρ}  m_π m_ρ · Φ6(π, ρ) ,
```

where `π`, `ρ` run over the positions of `𝔅` on either side of `S`, `m_π` is the size of `π` minus the number
of end leaves at `π`, the last sum is over pairs of *different* positions on the same side, and `Φ4`, `Φ5(π)`,
`Φ6(π,ρ)` are the local terms of the bloblet `𝔅°` in which the positions `π_1,…,π_4` carry cherries (one leaf
of each cherry being the end leaf).  So the weight of a split that cuts a blob is a polynomial of degree at
most two in the sizes of the positions, with coefficients determined by the blob alone; a split that cuts
no blob has weight `≥ 0`, positive iff it is displayed.

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
leaves outside `P` — at least three of the four end leaves — lie in one pendant subnetwork of `𝔅'`.
(e) is Step 4 of the proof of [LC] Theorem 12, which uses only Lemma D: two further leaves at one position
contribute `Φ6 = 0` (at most one end leaf lies at that position, and the two terms containing it cancel);
in every other term each position is met at most twice, so by Lemma D(iii) the term is a local term of
`Σ(𝔅)` with cherries at the positions met twice, and it depends only on the positions of the further
leaves.  The last sentence of (e) is (d) together with [LC] Lemmas 3 and 4.  ∎

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

**Remark (what Theorem A gives and does not give).**  (b)–(c) decide the robust question.  For a single
network a blob outside `𝒦` does not imply failure: by (e) the weight of each split that cuts the blob is a
polynomial of degree two in the sizes of its positions, and its sign has to be computed — as [LC]
Theorem 12 does for the nested blob with two hybrid nodes, where the answer is not monotone in the number
of leaves.  (e) makes this a finite procedure for every blob: a blob with `p` positions has `p(p−3)/2`
splits to examine, and each polynomial needs the local terms of the bloblet with at most two leaves per
position.  What is missing beyond level 2 is the list of blobs.

## 2. Six leaves and up to four hybrid nodes

Which of the 150 tree-generated six-point systems are displayed by outer-labeled planar networks?  By
Theorem A only the answer for networks on six leaves matters for the robust question, and by [LC] §7 the
150 systems fall into: the 108 systems of `𝒞_6` (those of galled networks); 19 further 6-locally good
systems; and 23 excluded systems — 14 that contain the three 3-splits, miss one, two or three 2-splits and
still have a good metric at six leaves; 3 with a negative split weight (two antipodal 2-splits missing); 6
with a positive weight on an undisplayed split (a 2-split and the 3-split incompatible with it missing).

`experiments/complexity/nanuq/six_leaf_survey.py` enumerates rooted binary networks on six leaves that are
outer-labeled planar for a fixed circular order, by repeated hybrid insertion into the 126 rooted planar
trees, and records the systems they display.

### 2.1 What is enumerated

Rooted binary networks on the leaves `0,…,5`, built from a rooted planar tree (all 126 of them, i.e. all root
positions) by `k` successive *insertions*: choose two different edges `a→b`, `c→d` of the current network with `d`
not an ancestor of `a`, subdivide the first by a tree node `p` and the second by a hybrid node `h`, and add the
edge `p→h`.  A network is kept if it is outer-labeled planar for the circular order `(0,…,5)` — tested as
planarity of the underlying graph together with the hexagon through the leaves and an apex joined to all
leaves (the wheel has one embedding, and the network must lie in its hexagonal face).  Networks are identified by
their unfolding, with the option `sym` up to the twelve rotations and reflections of the labels.  For every
network the union of the split systems of the trees of its switchings is recorded.

*What this does and does not cover.*  The networks have no parallel edges at any stage, and the root is never
moved (a root with a hybrid child is obtained by inserting the hybrid node on an edge leaving the root).  A network
all of whose reductions by one hybrid edge produce parallel edges — for instance one containing a blob with only
two incident cut edges, such as two nested triangles — is not generated; such blobs do not change the displayed
trees, but we have not proved that every outer-labeled planar network on six leaves with `k` hybrid nodes has the
split system of a generated one.  The enumeration is therefore **a survey [X], not a classification**.  For
`k ≤ 2` it agrees with the theorems of [LC] (galled networks give `𝒞_6`; a nested blob gives in addition exactly the
six images of one system, Theorem 12, Step 1).

### 2.2 Results

| hybrid nodes | rooted labelled networks | up to rotation and reflection | systems found so far |
|---|---|---|---|
| 0 | 126 | 12 | 14, all in `𝒞_6` |
| 1 | 2 988 | 253 | 71, all in `𝒞_6` |
| 2 | 59 706 | 5 000 | 113 = 107 of `𝒞_6` + 6 |
| 3 | 1 151 442 | 96 095 | **114 = all 108 of `𝒞_6` + the same 6** |
| 4 | not run | 1 846 320 | **114 — nothing new** |

The six systems outside `𝒞_6` are the six images of one system: **all nine non-trivial circular splits except one
2-split** — the system of the nested blob with six positions (`N[3,1,1]`, `N[4,1,0]`).  It contains the forbidden
pattern of [LC] Corollary 5′, so it is outside `𝒦′`, and its own metric at six leaves is still circular
decomposable with the right support (it is one of the 14 systems of that kind).  With at most three hybrid nodes
the survey finds **none** of the 19 six-locally good systems outside `𝒞_6`, none of the other 8 systems that
contain the pattern but are good at six leaves, none of the 3 systems with a negative weight and none of the 6
with a wrong support — and the same holds with four hybrid nodes.  Among the 1 151 442 labelled networks with
three hybrid nodes, 11 400 display one of the six systems; among the 1 846 320 classes with four, 28 091.

The 36 systems that never occur form eight classes under rotation and reflection (2-splits and 3-splits of a
representative, leaves `1,…,6`):

| status at six leaves | class size | 2-splits | 3-splits |
|---|---|---|---|
| negative weight | 3 | 12 23 45 56 | 123 234 345 |
| wrong support | 6 | 12 23 34 45 61 | 123 234 |
| good | 12 | 12 23 34 56 | 123 345 |
| good | 3 | 12 23 45 56 | 234 345 |
| good | 1 | all six | none |
| good | 3 | all six | 123 |
| pattern, good at six leaves | 2 | 12 34 56 | 123 234 345 |
| pattern, good at six leaves | 6 | 12 23 34 56 | 123 234 345 |

(`six_leaf_survey.py 3`, 27 minutes: log `six_leaf_survey_k3.log`; `six_leaf_survey.py 4 sym`, 90 minutes: log
`six_leaf_survey_k4_sym.log`; the two runs agree on the systems for `k ≤ 3`.  `six_leaf_examples.py` re-derives the
example networks printed in a log from the explicit network with `netcalc.py`.)

### 2.3 What follows, and what does not

1. **[X] For every outer-labeled planar network on six leaves that the survey generates with at most four hybrid
   nodes, the NANUQ metric is circular decomposable with support exactly the displayed splits.**  (All 114
   systems are globally good at six leaves.)  The smallest known failure has seven leaves ([LC] §6).
2. **[P + X] For blobs with at most four hybrid nodes the robust criterion would be the one of level 2.**
   By Theorem A(b), `Σ ∈ 𝒦` iff no six positions of a blob carry a system outside the 127 six-locally good ones.
   *If the six-position systems of blobs with at most four hybrid nodes are those found by the survey*, the only
   such system is "all nine splits except one 2-split", and membership in `𝒦` and in `𝒦′` coincide — as for
   level 2 ([LC] Corollary 14).  The hypothesis in italics is what the survey supports and does not prove (§2.1).
   **Open question:** is every tree-generated system displayed by an outer-labeled planar network on six leaves,
   of any level, one of these 114?  We do not state it as a conjecture; four levels of a survey are the evidence.
3. **Not shown.**  Whether a network of level 5 or more — or one not generated by the survey — can display, on
   six of its leaves, a system with a negative weight or a wrong support (which would give a six-leaf
   counterexample, impossible for level at most 2);
   whether the 19 good systems outside `𝒞_6` occur at all; a list of the blobs of level 3 that are not galled,
   with their critical splits — by Theorem A(e) each critical weight is again a quadratic polynomial in the sizes
   of the positions, but we have not computed these polynomials.
