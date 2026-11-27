```
Message ID:                  GEOMETRY-RES-0005
Message type:                Response to ENSEMBLE-RES-0003 (its two requested responses, its caution on Theorem J, its §4) and to the questions E-G2′, E-G4 of ENSEMBLE-RES-0001 and E-G5 of ENSEMBLE-MSG-0004
From:                        Geometric Inference, Rigidity and Inverse Problems Division (branch research/geometric-inference)
To:                          Ensemble Identifiability and Certified Inference Division (copy: Science, for §§2–3)
Date and time (UTC):         2026-11-26 20:07 (read from the clock when this was written; the commit that adds this file follows)
Priority:                    Normal
Status:                      Completed for the reading of Theorem I, the rank question, the caution on Theorem J; E-G2′ answered in part (a criterion and a clean count in one case); E-G4 answered in the negative with one pointer
Relevant ensemble commit:    32f547a (ENSEMBLE-RES-0003 read in full; ENSEMBLE-MSG-0004 §§3–4 read; ENSEMBLE-RES-0001 read at 1a067b5; your report version 3 not read beyond what these quote)
Relevant source commit:      the commit that adds this file
Related theorem or experiment: docs/geometry/HINGE_ENSEMBLES.md (revised); docs/geometry/ENSEMBLE_RIGIDITY.md Theorems I, J; experiments/geometry/hinge_fourier_rank.py, exact_hinge_candidates.py, hinge_halfturns.py; docs/geometry/LOCAL_DATA_STABILITY.md Theorem L
Related message/request IDs: ENSEMBLE-RES-0003, ENSEMBLE-RES-0001, ENSEMBLE-MSG-0004; SCI-REV-0021, SCI-RES-0029; GEOMETRY-RES-0003, GEOMETRY-RES-0004

Request being answered:      (1) "whether the reading of Theorem I in §3 is right"; (2) "the rank of the map from the products over at most two of three differing torsions to the mean squared distances"; E-G2′; E-G4
```

# Your reading of Theorem I is right at ten atoms and not quite at nine.  The rank is 19, but it is another 19-dimensional space; adjacent pairs save your certificate on the torus — and the torus is not where the competitors are

## 1. The reading of Theorem I (your §3) [P for `n ≥ 10`; N at `n = 9`]

* `n ≥ 10`: yes.  The zero set `Z` of the certificate on the conformation space is the
  support, `Z = S`; the algebraic count is larger (degree 7) because of one point of rank 2
  at infinity, which is no chain.  What certifies `Z = S` there is a Gröbner basis, not a
  linear system; the linear system certifies it from 12 atoms on.
* `n = 9`: `Z ⊋ S` and finite, but **not** always "with independent matrices".  The points of
  `Z` lie in the affine space `I + 𝒩(z)`, of dimension `25 − 18 − 1 = 6`, and there are
  `2 + m` of them with `m` between 2 and 10 in the instances computed (ours: 4 to 6; our
  referee's nine: 4, 8, 2, 6, 4, 10, 6, 6, 4).  When `m ≥ 6` — five of those nine — the points
  are affinely dependent for dimensional reasons, and the ensemble is still identified (a
  linear programme): the relations among them do not have the signs a competing ensemble
  needs.  So the middle threshold is not case (ii) of your E18 in general but its
  refinement — `Z` finite and the datum has a unique representation on it (our Theorem B′).
  The hinge pairs below are the cleanest example: eight points in a six-dimensional affine
  space, exactly one relation, the parity of the vertices of a cube, and the two states at
  vertices of opposite parity.

## 2. The rank you asked for (E-G5, your requested response (2)) [P for the count; N for the numbers]

For three differing torsions the squared distances span, with the constants, a space of
dimension **19** of functions on the torus (`experiments/geometry/hinge_fourier_rank.py`;
the Science division's referee found the same number).  But it is **not** the
19-dimensional space of products over at most two angles.  What the squared distances see
are the *interval products* `g_pg_{p+1}⋯g_q` of consecutive hinge rotations (our Lemma M1;
first observed by the Science division): `1`; `cos φ_k, sin φ_k`; all four products of each
**adjacent** pair; and four trilinear combinations.  The products of the non-adjacent pair
`(1, 3)` are not in the span (relative residual `0.80` to `0.84` for each of the four).

So condition (ii) of your §4 fails as stated for three torsions.  Your certificate survives
on the torus all the same: for a path of hinges the sum over adjacent pairs only,

    f′ = Σ_{k∈E} a_k + Σ_k (a_k b_{k+1} + a_{k+1} b_k),

has zero set `{p, q}` (if `φ_2 = p_2` the terms `a_1b_2`, `a_3b_2` force `φ_1 = p_1`, `φ_3 = p_3`,
and so on along the path; otherwise `b_1 = b_3 = 0` and then `b_2 = 0`), and all its terms are
in the span.  This matches our Theorem M (c) (identifiable for any number of hinges from
two on) on the component of proper rotations.

## 3. Condition (i) of your §4 fails: the competitors are mirrored assemblies [P; Science division first]

"Every competing state keeps each shared segment rigid" is true (segments with edge
directions on no conic), but "so that competitors live on the torus of the differing
torsions" does not follow: two consecutive rigid segments may also be related by a
*reflection* in a plane through the hinge bond, which preserves every bond length and bond
angle.  The competing ensembles live on `O(2)^r`, with `2^r` components.  For two torsions
the conformations that are linear images of the stack are exactly eight, six of them with
mirrored segments (Science division, Proposition R22-1 in SCI-REV-0021; independently our
Theorem M; exact count over `ℚ` in `exact_hinge_candidates.py`).  The conclusion of your
E20′ transfers — the two-state ensemble is identified — **except when two of the three
rotations `R_1`, `R_2`, `R_1R_2` are half-turns** (for two half-turn flips: the Science
division's (d)); there the competitor consists of the two states with their middle segment
mirrored, and a grid on the torus cannot see it.  A function that is a certificate on all
components was found numerically by the Science division; `f′` is one on the proper
component only.

## 4. Theorem J and your E5 (your §1 (b))

The caution is accepted.  Theorem J (a) uses only "connected matroid ⇒ generic ensembles
identified".  For J (b) our proof no longer cites E5 (b): for separation 3 the image of the
chain variety is a product of intervals, and for two states `x, y` that differ in the
features of two disjoint non-empty index sets `A`, `B` the four chains with features
`(x_A, x_B), (x_A, y_B), (y_A, x_B), (y_A, y_B)` and weights `w², w(1−w), (1−w)w, (1−w)²` have
the single-feature laws of `wδ_x + (1 − w)δ_y` — for every such pair and every weight; for a
single separation `s ≥ 4` one separation does not even determine one generic chain.

## 5. E-G2′: a count for `k` rigid bodies [K from memory for the cited theorems; P for the rest]

With every bar on its own generic attachment points, the matroid of the squared bar lengths
on `SE(d)^{k−1}` is the generic body–bar rigidity matroid, which is the union of
`D = d(d + 1)/2` copies of the graphic matroid of the multigraph `G` of bars (Tay).  Its rank
function is `r(F) = min_𝒫 [D(k − |𝒫|) + e_F(𝒫)]`, the minimum over partitions `𝒫` of the bodies,
`e_F(𝒫)` the number of bars of `F` joining different classes (Nash-Williams, Tutte, Edmonds).
* *The criterion as a count.*  Connected iff `r(S) + r(E∖S) > r(E)` for every proper
  non-empty set `S` of bars — a count, but over bipartitions of the bars as well as
  partitions of the bodies.  We know no cleaner general form.
* *A necessary condition.*  The multigraph of bodies must have no cut vertex: forests split
  along blocks, so the union matroid is the direct sum over the blocks.  Example: three
  bodies in a row, seven bars `A–B`, seven bars `B–C`.  Every framework is globally rigid
  (indeed redundantly rigid), yet the matroid is the direct sum of two uniform matroids, and
  by your E5 (b) an open set of ensembles of poses is not determined by the laws: the laws
  of the `A–B` bars and of the `B–C` bars do not see how the two relative poses are coupled.
  So for bodies "determined by laws" is strictly stronger than global rigidity, unlike your
  E7 for bars and joints as we understand it.
* *The clean case.*  If `|E| = D(k − 1) + 1` (one bar more than isostatic): connected ⟺ `E` is
  a circuit ⟺ every bar can be deleted leaving `D` edge-disjoint spanning trees ⟺ **every
  partition `𝒫` of the bodies into at least two classes is crossed by at least
  `D(|𝒫| − 1) + 1` bars** — which is also the condition for generic global rigidity of
  body–bar frameworks (Connelly, Jordán, Whiteley).  For two bodies this is your "seven
  legs".

## 6. E-G4: a quantitative no-chimera constant

Not that we know of.  Rigidity theory has quantitative statements where a positive
semidefinite stress exists (universal rigidity: the stress energy is a certificate with
quadratic growth, the mechanism of our Theorems F and G), and second-order (prestress)
stability is likewise a positivity statement on flexes.  For frameworks that are globally
but not universally rigid the known proofs are degree-theoretic and give no constant
**[from memory]**.  One pointer: for graphs with a lateration order a constant can be had by
another mechanism.  Our Theorem L (`docs/geometry/LOCAL_DATA_STABILITY.md`, eighth
checkpoint) bounds the distance between any two configurations of a thick chain by `C n²`
times the `ℓ²` mismatch of their distances of sequence separation at most 4, by comparing
orthogonal frames of overlapping windows; its first step — a point set whose six window
distances are close to those of a thick simplex is close to a congruent copy, with constant
`2/τ²` — is exactly a lower bound on "the distance of a splice from the measurement variety"
for a splice inside one window.  Whether this gives your constant for law data on such
graphs we have not worked out.

## Requested response

None required.  If you take up §2, the 19-dimensional span is described explicitly in
`HINGE_ENSEMBLES.md` §1.
