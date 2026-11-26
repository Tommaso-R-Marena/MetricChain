# The NANUQ metric: a local criterion, all galled planar networks, and why "galled" cannot be dropped

Working paper of the complexity division, first version 2026-11-26.  Register: `THEOREMS.md` CX-T5–CX-T8.
Problem: `OPEN_PROBLEMS.md` B (Holtgrefe, Allman, Baños, van Iersel, Moulton, Rhodes, Wicke, *Distinguishing
Phylogenetic Level-2 Networks with Quartets and Inter-Taxon Quartet Distances*, Bull. Math. Biol. 2025;
cited as [HABIMRW] by section number of arXiv:2507.17308v2).

## 0. What is here, and how it relates to what others have claimed

[HABIMRW] prove that the NANUQ metric of an outer-labeled planar, galled, level-2 *bloblet* is circular
decomposable with support the displayed splits (Theorem 4.7), and conjecture the same for all level-2
networks of the class (B1) and circular decomposability for level-3 bloblets (B2).

1. **Theorem 4 (local criterion)** [P + X].  The split weights of the NANUQ metric decompose into terms
   that depend on at most six leaves.  If the 6-point terms of a tree-generated circular split system are
   non-negative and vanish when they should, its NANUQ metric is circular decomposable with support
   exactly the system.  Network-free; the 5-point terms are automatically right.
2. **Theorem 7 (all galled outer-labeled planar networks)** [P + X].  Every network of the class of
   [HABIMRW] — any level, any number of blobs — satisfies the criterion.  This contains B1 and B2.
   *An all-level statement of this kind was claimed on 2026-09-29 in an unreviewed third-party repository
   (`PRIOR_ART.md` B-II).  We have not seen that proof and could not inspect it; ours was derived
   independently on 2026-11-26.  If theirs is correct, priority for the statement is theirs.*
3. **Theorem 9 (galled cannot be dropped)** [X].  An explicit outer-labeled planar level-2 bloblet on
   seven leaves that is not galled, whose NANUQ metric is Kalmanson for none of the 360 circular orders;
   and a family in which one displayed split has weight tending to `−∞`.  We found no such example in
   the literature (search recorded in `PRIOR_ART.md` §B).
4. **Theorem 10 (the criterion is sharp)** [X].  Among classes of tree-generated circular split systems
   closed under restriction and under replacing a leaf by a cherry, the class defined by the criterion is
   the largest one on which the NANUQ metric is circular decomposable (for the given order) with exact
   support: each of the 23 six-point systems it excludes is, or becomes after doubling a few leaves, a
   system whose metric fails.
5. **Theorem 11 (the parametric family, problem B3)** [P + X].  For the four-parameter family of quartet
   distances of NANUQ⁺ the conclusion holds on the whole class exactly when `ρ_o = ρ_s` and
   `ρ_c + ρ_s ≤ 2ρ_a < 2ρ_s`; the *Modified NANUQ* distance is outside this set and fails on an explicit
   level-1 network with eight leaves, but it works when every hybrid node has a leaf child.

Labels: [P] paper proof (ours, internally reviewed only), [X] exact finite computation with integer
arithmetic (programs in `experiments/complexity/nanuq/`, listed in §9).  Nothing here is machine-checked.

---

## 1. Definitions

**Circular orders and splits.**  `X = {x_1,…,x_n}`, `n ≥ 4`, with the circular order `C = (x_1,…,x_n)`
(indices mod `n`).  The *gap* `g_i` lies between `x_i` and `x_{i+1}`.  For `i ≠ j` the circular split
`S_ij = U_ij | V_ij` has `U_ij = {x_{i+1},…,x_j}`.  A split is trivial if a side is a singleton.  A set `Σ` of
circular splits is *tree-generated* if it is a union of split systems of binary trees with leaf set `X`
whose splits are circular for `C` (it then contains all trivial splits).  For `Y ⊆ X`, `|Y| ≥ 4`, the
restriction `Σ|_Y` is the set of non-empty splits `A∩Y | B∩Y`; it is tree-generated for `C|_Y`.

**Displayed quartets.**  For four leaves `a,b,c,d` in this circular order, `Σ` *displays* `ab|cd` if some
split of `Σ` separates `{a,b}` from `{c,d}`, and `ad|bc` likewise (a circular split never separates `{a,c}`
from `{b,d}`).  If `Σ` is tree-generated every 4-set displays one or both.  The *weight* `w(ab|cd)` is
`1` if only `ab|cd` is displayed, `1/2` if both are, `0` if only `ad|bc` is.

**NANUQ metric of a split system.**  For `x ≠ y` and `z,w ∉ {x,y}`, let `ρ_xy(z,w)` be the average, over the
displayed quartets `t` of `{x,y,z,w}`, of `[x,y` is not a cherry of `t]`, and

```
d_Σ(x,y) = 2n − 4 + 2 Σ_{ {z,w} ⊆ X∖{x,y} } ρ_xy(z,w),        d_Σ(x,x) = 0.
```

**Split weights.**  `α_ij(d) = d(x_i,x_j) + d(x_{i+1},x_{j+1}) − d(x_i,x_{j+1}) − d(x_{i+1},x_j)`.  By Chepoi–Fichet
([HABIMRW] Prop. 2.8; [K]) a symmetric `d` with zero diagonal equals `½ Σ α_ij δ_{S_ij}`; `d` is circular
decomposable for `C` iff all `α_ij ≥ 0`, and then its support is `{S_ij : α_ij > 0}`.

**Networks.**  For a semi-directed network `N` on `X`, `T(N)` is the set of its displayed trees and
`Split(T(N))` the union of their split systems; the displayed quartets of `N` are the quartets of its
displayed trees ([HABIMRW] §5: `Q(N) = Q(T(N))`).  `d_N` is the NANUQ metric of [HABIMRW] Def. 4.1.

**Lemma 1 [P].**  If `N` is outer-labeled planar with induced circular order `C`, then `Σ = Split(T(N))` is a
tree-generated circular split system for `C` and `d_N = d_Σ`.

*Proof.*  Every displayed tree is planar for `C`, so its splits are circular ([HABIMRW] Prop. 2.9), and
the displayed trees are binary: tree-generated.  A tree displays `ab|cd` iff one of its splits separates
`{a,b}` from `{c,d}`; so the set of displayed quartets on each 4-set is the same for `N` and `Σ`, and the
two metrics are defined from these sets by the same formula.  ∎

So the conjectures are statements about a family of circular split systems.  They are *not* true for
all tree-generated systems: on six points 9 of the 150 tree-generated systems fail (CX-D2).

---

## 2. The split weights are sums of terms on at most six leaves

Fix a non-trivial split `S_ij = U|V`, write `U = (u_1,…,u_p)`, `V = (v_1,…,v_q)` in circular order
`u_1 … u_p v_1 … v_q` (so `u_1 = x_{i+1}`, `u_p = x_j`, `v_1 = x_{j+1}`, `v_q = x_i`; `p,q ≥ 2`), and
`Y = {u_1,u_p,v_1,v_q}`.  Then `α_ij = d(v_q,u_p) + d(u_1,v_1) − d(v_q,v_1) − d(u_1,u_p)`.

**Proposition 2 (decomposition) [P; identity re-checked [X] on arbitrary systems].**  For every
tree-generated `Σ`,

```
α_ij(d_Σ)/2  =  Φ4  +  Σ_{z ∈ X∖Y} Φ5(z)  +  Σ_{ {z,w} ⊆ U∖Y }  Φ6(z,w)  +  Σ_{ {z,w} ⊆ V∖Y }  Φ6'(z,w)
```

with, for `z` (resp. `z` before `w`) in `U∖Y`,

```
Φ4       = 2·w(u_1 u_p | v_1 v_q)
Φ5(z)    = w(u_1 z | v_1 v_q) + w(z u_p | v_1 v_q) − w(z u_p | v_1 u_1) − w(u_1 z | u_p v_q)
Φ6(z,w)  = w(z w | v_1 v_q) + w(z w | u_1 u_p) − w(z w | v_q u_p) − w(z w | u_1 v_1)
```

and the mirror-image expressions (exchange `u_1 ↔ v_1`, `u_p ↔ v_q`) for points of `V∖Y`.  For a trivial
split `{u} | X∖{u}` with `a`, `b` the leaves before and after `u`,

```
α/2 = n − 2 + Σ_{ {z,w} ⊆ X∖{a,u,b} } Ψ(z,w),     Ψ(z,w) = 1 − w(a u | z w) − w(u b | z w) + w(a b | z w).
```

*Proof.*  The constant `2n−4` cancels in `α_ij` when the four leaves of `Y` are distinct.  Write
`d(x,y) − (2n−4) = 2 Σ_{q ∋ x,y} ρ^q_{xy}` over 4-sets `q`, so `α_ij/2 = Σ_q c(q)` with
`c(q) = ρ^q(v_q,u_p) + ρ^q(u_1,v_1) − ρ^q(v_q,v_1) − ρ^q(u_1,u_p)`, a term being present iff its pair lies in
`q`.  Sort the 4-sets by `q ∩ Y`.  If `q ∩ Y` contains none of the four pairs, `c(q) = 0`.

*`q = Y`.*  Its planar quartets are `u_1u_p|v_1v_q`, for which `c = 1+1−0−0 = 2`, and `u_1v_q|u_pv_1`, for
which `c = 1+1−1−1 = 0`.  So `c(Y) = 2w(u_1u_p|v_1v_q) = Φ4`.

*`|q ∩ Y| = 3`, `q = (Y∖{y}) ∪ {z}`, `z ∈ U`.*  For each of the four choices of `y` exactly two of the four
pairs lie in `q`, and evaluating `c` on the two planar quartets of `q` gives:
`y = v_q`: `−w(z u_p | v_1 u_1)`;  `y = v_1`: `−w(u_1 z | u_p v_q)`;  `y = u_p`: `+w(u_1 z | v_1 v_q)`;
`y = u_1`: `+w(z u_p | v_1 v_q)`.  Their sum is `Φ5(z)`.  (Example, `y = v_q`: `q = {u_1,z,u_p,v_1}` in this
circular order, `c = ρ(u_1,v_1) − ρ(u_1,u_p)`; on `u_1z|u_pv_1` this is `1 − 1`, on `zu_p|v_1u_1` it is `0 − 1`.)

*`|q ∩ Y| = 2`, `q = {s,t,z,w}` with `{s,t}` one of the four pairs and `z,w ∉ Y`.*  If `z ∈ U`, `w ∈ V`, then
`z,w` separate `s` from `t` on the circle for each of the four pairs, so all four `ρ` equal `1` and the
total is `0`.  If `z,w ∈ U` (`z` before `w`), then in `{v_q,z,w,u_p}` the pair `v_q,u_p` is a cherry exactly in
the quartet `zw|v_qu_p`, so `ρ(v_q,u_p) = 1 − w(zw|v_qu_p)`, and likewise for the other three pairs; the
total is `Φ6(z,w)`.

For a trivial split the constant contributes `(2n−4)(1+1−1) `, i.e. `n − 2` to `α/2`; a 4-set containing
`a,u,b` contributes `0` (on both planar quartets of `{a,u,b,z}` the three values are `0,1,1` or `1,0,1`);
a 4-set `{s,t,z,w}` with `{s,t} ⊂ {a,u,b}` and `z,w` elsewhere contributes `1 − w(st|zw)` with sign `+` for
`au`, `ub` and `−` for `ab`.  ∎

`check_decomposition.py` confirms both identities, with exact integers, on every network system on at
most 7 leaves and on about a thousand random circular split systems on 5–8 points.

**Lemma 3 [P].**  For tree-generated `Σ` and a non-trivial `S_ij`:  `S_ij ∈ Σ` iff `Σ` displays
`u_1u_p|v_1v_q` iff `Φ4 > 0`.

*Proof.*  A circular split separating `{u_1,u_p}` from `{v_1,v_q}` has a side that is an interval
containing `u_1`, `u_p` and neither `v_q` (the predecessor of `u_1`) nor `v_1` (the successor of `u_p`): it is
`U`.  ∎

---

## 3. The local criterion

**Definition.**  A tree-generated `Σ` on `(X,C)` is *locally NANUQ-positive* if for every non-trivial
`S_ij = U|V` and all `z,w` on one side of it other than its four end leaves, the corresponding `Φ6` (or
`Φ6'`) is `≥ 0`, and is `= 0` whenever `S_ij ∉ Σ`.  It is *6-locally good* if every restriction of `Σ` to six
leaves, in each of its twelve dihedral labellings `y_1,…,y_6`, satisfies
`Φ6(y_1; y_2,y_3; y_4; y_5,y_6) ≥ 0` with equality if `y_1y_4|y_5y_6` is not displayed.  A 6-locally good
system is locally NANUQ-positive (take `(u_1,z,w,u_p,v_1,v_q) = (y_1,…,y_6)`; by Lemma 3, `S_ij ∉ Σ` iff
`u_1u_p|v_1v_q` is not displayed, a property of the restriction).

**Lemma 4 (the 5-point terms take care of themselves) [X].**  For *every* tree-generated system on five
points, in every placement: `Φ5 ∈ {0, ½, 1}`, `Φ5 = 0` if `u_1u_p|v_1v_q` is not displayed, and
`Ψ ∈ {0, ½, 1}`.  (16 systems × 10 placements; `five_point_facts.py`.)

**Theorem 4 (local criterion) [P, using Lemma 4].**  If a tree-generated circular split system `Σ` on
`n ≥ 4` points is locally NANUQ-positive, then `d_Σ` is circular decomposable for `C` and its support is
exactly `Σ`:  `α_ij ≥ 0` for all `i ≠ j`, and `α_ij > 0` iff `S_ij ∈ Σ`.

*Proof.*  Trivial splits belong to `Σ`, and by Proposition 2 and Lemma 4 their weight is
`2(n−2) + 2ΣΨ ≥ 2(n−2) > 0`.  Let `S_ij` be non-trivial.  Every `Φ5(z)` is a function of the restriction of
`Σ` to the five leaves `Y ∪ {z}`, which is tree-generated; by Lemma 4 it is `≥ 0`, and `= 0` if `S_ij ∉ Σ`
(Lemma 3).  The `Φ6` are `≥ 0`, and `= 0` if `S_ij ∉ Σ`, by hypothesis.  `Φ4 ≥ 0`.  Hence `α_ij ≥ 0`; if
`S_ij ∉ Σ` every term vanishes (`Φ4 = 0` by Lemma 3) and `α_ij = 0`; if `S_ij ∈ Σ` then
`α_ij ≥ 2Φ4 > 0`.  ∎

**What the 6-point condition says.**  Fix `z,w` and four further leaves `a_1,a_2,a_3,a_4` met in this
order when going from `w` to `z` (in the theorem `a_1 = u_p`, `a_2 = v_1`, `a_3 = v_q`, `a_4 = u_1`).  For a
binary tree `T` in `Σ` let `π_T(a)` be the point of the path from `z` to `w` at which `a` branches off; along
the path, `π_T(a_1),…,π_T(a_4)` is monotone, and `T` displays `zw|a_ia_k` iff `π_T(a_i) = π_T(a_k)`.  Let `E_ik` be
the set of trees of `Σ` with `π_T(a_i) = π_T(a_k)` and `φ(E) ∈ {0,½,1}` according as `E` is empty, proper, or
everything.  Then `E_14 = E_13 ∩ E_24`, `E_13 ∪ E_24 ⊆ E_23`, and
`Φ6 = φ(E_14) + φ(E_23) − φ(E_13) − φ(E_24)`.  A case distinction gives:

**Lemma 5 [P].**  `Φ6 ∈ {−½, 0, ½, 1}`, and `Φ6 < 0` iff simultaneously: some tree of `Σ` has a split
separating `{z,w}` from `{a_1,a_2,a_3}`; some tree has one separating `{z,w}` from `{a_2,a_3,a_4}`; no tree has
one separating `{z,w}` from `{a_1,a_2,a_3,a_4}`; and some tree displays `wa_2|a_3z`.

*Proof.*  If `E_13` is everything, so is `E_23`, and `E_14 = E_24`: `Φ6 = 0`; same for `E_24`.  If `E_13 = ∅`:
`Φ6 = φ(E_23) − φ(E_24) ≥ 0`; same for `E_24 = ∅`.  Otherwise `φ(E_13) = φ(E_24) = ½` and
`Φ6 = φ(E_14) + φ(E_23) − 1`, which is negative iff `E_14 = ∅` and `E_23` is not everything.  ∎

So negativity is the failure of a *union property*: two displayed splits that both cut `{z,w}` off, from
`a_1a_2a_3` and from `a_2a_3a_4`, without any displayed split cutting `{z,w}` off from all four.

---

## 4. Planar trees with twin leaves (class 𝒜) and substitution

**Class 𝒜.**  An *𝒜-structure* is a binary tree `T` whose leaves are a circularly ordered set `P` of
*positions* (the splits of `T` circular), with pairwise disjoint pairs of circularly adjacent positions
(*twins*).  Its leaves are the unpaired positions and the pairs, in the induced circular order; its
*displayed trees* are obtained from `T` by deleting one position of each pair; its split system `Σ(T)` is
the union of their split systems.  `𝒜_n` is the set of such systems on `n` leaves (so at most `n` pairs,
`|P| ≤ 2n`).

**Proposition 6 (union property in 𝒜) [P].**  In an 𝒜-system: if a displayed split separates `{z,w}` from
`{a_1,a_2,a_3}` and a displayed split separates `{z,w}` from `{a_2,a_3,a_4}` (leaves in the circular order
`w,a_1,a_2,a_3,a_4,z`), then a displayed split separates `{z,w}` from `{a_1,a_2,a_3,a_4}`.  Hence `Φ6 ≥ 0`
everywhere in 𝒜 (Lemma 5).

*Proof.*  A displayed split comes from an edge of the one tree `T`, i.e. from a set `I` of positions that is
an interval of `P`, together with a choice of one position per pair: a leaf lies on the side of `I` iff its
chosen position is in `I`.  Let `I_1`, `I_2` be the intervals of the two given splits: `I_1` contains a
position of each of `a_1,a_2,a_3` and misses a position of `z` and one of `w`; `I_2` likewise for `a_2,a_3,a_4`.
Both contain the positions lying between those of `a_2` and of `a_3`, so they intersect.  We claim that some
position lies in neither.  Otherwise every position missed by `I_1` lies in `I_2` and conversely, so `z` and
`w` are twin pairs and each of `I_1`, `I_2` contains exactly one position of `z` and one of `w`.  An interval
containing a position of `a_2`, exactly one position of `w` and exactly one of `z` is the interval from the
second position of `w` to the first position of `z`; so `I_1 = I_2`, and they miss common positions — a
contradiction.  Two edges of a tree whose sides `I_1`, `I_2` intersect and miss a common leaf are nested, say
`I_1 ⊆ I_2`.  Then `I_2` contains a position of each of `a_1,…,a_4` and misses positions of `z` and `w`;
choosing these positions (the choices at different pairs are independent) gives a displayed tree with a
split separating `{z,w}` from `{a_1,a_2,a_3,a_4}`.  ∎

This is the structural reason behind the theorem of [HABIMRW] and its extension: *all displayed trees of
a galled planar network are restrictions of one planar tree, with independent choices*.  In a network
that is not galled the choices are not independent, the union property fails, and so does the theorem
(§6).

**Substitution.**  For circular split systems `Σ_1` on `X_1 ∋ p` and `Σ_2` on `X_2 ∋ r`, the system
`Σ_1 ∘_{p,r} Σ_2` on `(X_1∖p) ∪ (X_2∖r)` (circular order: that of `X_1` with `p` replaced by `X_2∖r` in the
order following `r`) consists of the splits of `Σ_1` with `p` replaced by `X_2∖r` and the splits of `Σ_2` with
`r` replaced by `X_1∖p`.  Let `𝒞` be the smallest class of systems containing all `𝒜_n` and closed under `∘`.

**Lemma 7 (restrictions) [P].**  (i) The restriction of an 𝒜-system to `Y` is an 𝒜-system on `Y`
(restrict `T` to the positions of the leaves of `Y`; twins stay adjacent).  (ii) For `Y` meeting both
`X_1∖p` and `X_2∖r`,  `(Σ_1 ∘ Σ_2)|_Y = Σ_1|_{(Y∩X_1)∪p} ∘ Σ_2|_{(Y∩X_2)∪r}`; if `Y` misses one of them the
restriction is a restriction of the other factor.  (iii) Consequently every restriction of a system of
`𝒞` to `m ≤ 6` leaves lies in `𝒞_m`, the set of systems on `m` leaves obtained from `𝒜_{≤ 6}` by
substitutions all of whose intermediate systems have at most 6 leaves.

*Proof.*  (i), (ii) are immediate from the definitions (displayed trees restrict to displayed trees; a
restricted tree's splits are the restricted splits).  (iii) by induction on the construction of the
system: in (ii) both factors have at most `|Y| − 1 + 1 ≤ 6` leaves.  ∎

**Lemma 8 (finite check) [X].**  `|𝒜_4| = 3`, `|𝒜_5| = 16`, `|𝒜_6| = 102`;  `|𝒞_4| = 3`, `|𝒞_5| = 16`,
`|𝒞_6| = 108`; every system of `𝒞_6` is 6-locally good (and satisfies the 5-point facts on all its
5-subsets).  Programs: `twin_trees.py`, `verify_class.py`, `characterize6.py`.  (`𝒜_6` is computed from all
binary trees on `6 + k` circular positions, `k ≤ 6`, with all choices of `k` disjoint adjacent pairs.)

**Theorem 6′ (class 𝒞) [P + X].**  Every system of `𝒞` is 6-locally good; hence, by Theorem 4, its
NANUQ metric is circular decomposable with support exactly the system.

*Proof.*  Lemma 7(iii) and Lemma 8.  ∎

---

## 5. All galled outer-labeled planar networks

**Lemma A (hybrids with a leaf child) [P].**  Let `N` be a binary semi-directed network with an
outer-labeled planar embedding inducing `C`, in which every hybrid node is adjacent to a leaf.  Then
`Split(T(N)) ∈ 𝒜_n`.

*Proof.*  For each hybrid node `h` with parents `p_h`, `p'_h` and leaf `x_h`, delete `h` and `x_h` and attach
two new leaves `x_h^-` to `p_h` and `x_h^+` to `p'_h`.  The result `T` is a tree: the switching of `N` that keeps
all edges `p_h h` is a spanning tree of `N` (in a rooted partner every non-root node keeps exactly one
parent), and `T` is this tree with `h` suppressed and one pendant leaf `x_h^+` added per hybrid.  All its
internal nodes have degree 3.  In the embedding, `h` and `x_h` can be replaced by two leaves drawn along
the two sides of the path `h x_h`, so `T` is planar with `x_h^-`, `x_h^+` adjacent on the outer face in the
place of `x_h`.  Deleting the hybrid edge `p'_h h` of `N` corresponds to deleting `x_h^+` of `T`.  So the
displayed trees of `N` are those of the 𝒜-structure.  ∎

**Lemma B (cutting below a hybrid) [P].**  Let `N` be binary, semi-directed, outer-labeled planar and
galled, and `h` a hybrid node whose child is not a leaf.  The edge `e` from `h` to its child is a cut
edge ([HABIMRW] §2.1: in a binary galled network every hybrid node is an articulation node; the two
hybrid edges lie on a cycle).  Cut `e` and cap both ends with new leaves `p` (at `h`) and `r`.  The two
pieces `N_1 ∋ p`, `N_2 ∋ r` are again outer-labeled planar with the induced circular orders, each of their
hybrid nodes has its third edge a cut edge, every switching of a piece is a tree, and
`Split(T(N)) = Split(T(N_1)) ∘_{p,r} Split(T(N_2))`.

*Proof.*  A switching of `N` is a spanning tree containing the bridge `e`; removing `e` leaves spanning
trees of the two sides, and conversely switchings of the pieces combine.  So the displayed trees of `N`
are exactly the trees obtained by joining a displayed tree of `N_1` and one of `N_2` at `p`, `r`, and the
splits of a joined tree are those described in the definition of `∘`.  Bridges of `N` other than `e` remain
bridges of the pieces; planarity and the outer face are inherited.  ∎

(The pieces need not be semi-directed networks in the sense of [HABIMRW] — a rooted partner may not
exist for `N_2` — but only the properties listed in Lemma B are used: Lemma A needs only that the
switchings are trees.)

**Theorem 7 (all levels, any number of blobs) [P + X].**  Let `N` be a binary semi-directed network on
`n ≥ 4` leaves that is outer-labeled planar and galled (no bound on the level, any number of blobs).
Then `d_N` is circular decomposable, for every circular order induced by `N`, and its support is exactly
`Split(T(N))`.

*Proof.*  Induct on the number `μ` of hybrid nodes whose child is not a leaf, in the class of planar
"marked" networks described in Lemma B.  If `μ = 0`, `Split(T(N)) ∈ 𝒜 ⊆ 𝒞` by Lemma A.  Otherwise cut
below such a hybrid: both pieces have smaller `μ` (in `N_1` the node `h` now has the leaf `p`; `N_2` does not
contain `h`), their systems are in `𝒞` by induction, and so is the substitution.  Theorem 6′ and Lemma 1
finish the proof.  ∎

In particular: Conjecture B1 (all of `N_2`) and Conjecture B2 (level-3 bloblets, with the exact support)
hold, as special cases of a statement for all levels.

---

## 6. "Galled" cannot be dropped

**The network `N*`.**  Rooted partner, children lists (`h1`, `h2` hybrid):

```
rho: w1, w3      w1: a1, w2      w2: a2, p1      p1: b, h1
w3: d, q1        q1: h1, q2      q2: h2, c       h1: u       u: x, h2       h2: y
```

Seven leaves; one blob containing both hybrid nodes (a level-2 bloblet); outer-labeled planar with
circular order `(a1, a2, b, x, y, c, d)`; **not galled**: `h1` is an ancestor of `h2` inside the blob (every
cycle through the two hybrid edges of `h2` uses a hybrid edge of `h1`).  Displayed trees:

```
((((x,y),c),d),((a2,b),a1))      ((((c,y),x),d),((a2,b),a1))
(((((x,y),b),a2),a1),(c,d))      ((((b,x),a2),a1),((c,y),d))
```

NANUQ metric (order `a1,a2,b,x,y,c,d`):

```
 0 21 23 26 26 23 21
21  0 17 24 26 27 25
23 17  0 20 24 29 27
26 24 20  0 20 24 26
26 26 24 20  0 20 24
23 27 29 24 20  0 17
21 25 27 26 24 17  0
```

**Theorem 9 [X].**  (a) For the planar order, the displayed split `{x,y} | {a1,a2,b,c,d}` has weight
`α = d(b,y) + d(x,c) − d(b,c) − d(x,y) = 24 + 24 − 29 − 20 = −1`.  (b) `d_{N*}` is not circular decomposable:
for each of the 360 circular orders of the seven leaves some `α_ij` is negative.  (c) In the family
`N(s,t)` (the same blob with `t` leaves `a_i` and `s` leaves `d_i`, attached along the cycle or as pendant
clades) the weight of `{x,y} | rest` is negative for all tested `s + t ≥ 3` (bloblet version) and decreases
quadratically (`−13` at `s = t = 3`).  Programs: `counterexample7.py`, `verify_nongalled.py`,
`verify_nongalled2.py` (built on `netcalc.py`, which works from the explicit rooted network and shares
no code with the split-system programs), `nongalled_family.py`.

*Why.*  The restriction of `Split(T(N*))` to `{d, a_i, b, x, y, c}` contains every circular split of these six
leaves except `{d,a_i} | {b,x,y,c}`.  With `z = d`, `w = a_i`, `(a_1,…,a_4) = (b,x,y,c)`: the displayed trees
cut `{d,a_i}` off from `{b,x,y}` (when `x,y` hang on the `b` side) and from `{x,y,c}` (when they hang on the `c`
side) but never from all four — the union property fails because `y` follows `x` when `h1` switches.  Each
such pair contributes `Φ6 = −½`; there are `st` of them, against `O(s+t)` positive terms.

So Theorem 4.7 of [HABIMRW] does not extend to outer-labeled planar level-2 networks that are not
galled, not even for bloblets, and not even with the weaker conclusion "circular decomposable for some
order".

---

## 7. The criterion is sharp

On six points there are 150 tree-generated systems; 141 have a NANUQ metric that is Kalmanson with exact
support; 127 are 6-locally good; 108 are in `𝒞` (`characterize6.py`).

**Theorem 10 [X + P].**  (a) The 9 systems that fail globally are, up to rotation and reflection, two:
all nine non-trivial splits except two antipodal 2-splits (negative weight), and all except a 2-split
`{x_k,x_{k+1}}` together with the 3-split that separates `x_k` from `x_{k+1}` (a weight on a split that is not
displayed).  (b) Each of the other 14 systems that are not 6-locally good — all nine splits except one
2-split, except two 2-splits at distance two, or except three alternate 2-splits — has a blow-up, in
which some leaves are replaced by cherries or 3-leaf caterpillars (at most 10 leaves in total), whose
NANUQ metric fails; for six of them (those missing a single 2-split) doubling a single leaf suffices.  (c) The class `𝒦` of
tree-generated systems all of whose 6-point restrictions are 6-locally good is closed under restriction
and under replacing a leaf by a cherry (every 5-point tree-generated system with one leaf doubled is
6-locally good).  Consequently: *a class of tree-generated circular split systems that is closed under
restriction and under replacing a leaf by a cherry has, for all its members, a NANUQ metric that is
Kalmanson for the given order with support exactly the system, if and only if it is contained in `𝒦`.*

*Proof of the last sentence.*  "If": Theorem 4.  "Only if": a member with a 6-point restriction outside
the 127 has that restriction, and its blow-ups, in the class; by (a), (b) one of them fails.  ∎

By §5 the galled outer-labeled planar networks on six leaves give systems of `𝒞_6`, hence at most 108 of the
127 (and exactly 108 according to a second generator, `multiblob.py`, which builds networks blob by blob and
respects the existence of a rooted partner); the remaining 19 systems satisfy the criterion and are not
displayed by any network of that class on six leaves.

---

## 8. The parametric family of quartet distances (problem B3)

Allman, Baños, Rhodes and Wicke (NANUQ⁺, Algorithms Mol. Biol. 2025, Def. 3.1; read in the published HTML
version) define, for `ρ = (ρ_c, ρ_s, ρ_a, ρ_o) ∈ (ℝ_{≥0})^4`,
`d_ρ(x,y) = 2 Σ_{z,w} ρ_xy(Q_xyzw) + 2n − 4`, where `ρ_xy` is `ρ_c` if the quarnet is a tree with cherry `xy`,
`ρ_s` if it is a tree separating `x` from `y`, `ρ_a` if it has a 4-cycle with `x,y` adjacent, `ρ_o` if it has a
4-cycle with `x,y` opposite.  NANUQ is `(0, 1, ½, 1)`; their *Modified NANUQ* distance is `(½, 1, ½, 1)`.
[HABIMRW] §6 asks "whether some of our results can be extended to a parametric family of distances, as
introduced in [All+25a]".  For planar quartet systems we read "4-cycle" as "both planar quartets are
displayed" (for level-1 networks this is the original definition).

**Theorem 11 [P + X].**  Let `ρ ∈ (ℝ_{≥0})^4`.

(a) `d_ρ` is circular decomposable, for the induced circular order, with support exactly `Split(T(N))`, for
**every** binary semi-directed outer-labeled planar galled network `N` (all levels, any number of blobs)
**if and only if**

```
ρ_o = ρ_s     and     ρ_c + ρ_s ≤ 2 ρ_a < 2 ρ_s .
```

(b) The same holds for every such network **whose hybrid nodes all have a leaf child** (class 𝒜; it
contains all bloblets) if and only if  `ρ_o = ρ_s`,  `ρ_c ≤ ρ_a`  and  `ρ_s ≤ 2ρ_a < 2ρ_s`.

(c) NANUQ satisfies (a), on its boundary (`ρ_c + ρ_s = 2ρ_a`).  Modified NANUQ satisfies (b) (on its
boundary, `ρ_c = ρ_a`) but **not** (a): for the level-1 network on eight leaves consisting of a 5-cycle whose
hybrid node has a cherry below it and which carries cherries at two of its other four positions, the
Modified NANUQ distance gives the displayed split "hybrid cherry | rest" the weight `−2`, and is Kalmanson
for none of the 2520 circular orders (`modified_nanuq_witness.py`, from the explicit rooted network).

*Proof.*  The decomposition of Proposition 2 holds verbatim with `ρ_xy` in place of the NANUQ values
(`α/2 = T4 + ΣT5 + ΣT6 + ΣTM`, where `TM` is the term of a mixed pair `z ∈ U`, `w ∈ V`, which no longer
vanishes; for a trivial split `α/2 = n − 2 + ΣTQ + ΣTP`, `TQ` being the term of the 4-sets through the three
leaves `a,u,b`); checked [X] on 2122 split weights of blow-ups with up to 18 leaves.  Every local term is a
linear form in `ρ` determined by the restriction to at most six leaves, hence (Lemma 7) by a system of
`𝒞_{≤6}`, resp. `𝒜_{≤6}`.  The forms that occur are [X]:

| term | forms on `𝒞_{≤6}` (the forms on `𝒜_{≤6}` are the same except the one marked †) |
|---|---|
| `T4`, split displayed | `2(ρ_s − ρ_c)`, `2(ρ_o − ρ_a)` |
| `T5` | `0`, `ρ_s − ρ_c`, `ρ_o − ρ_a`, `(ρ_s − ρ_c) − (ρ_o − ρ_a)`, twice the latter |
| `T6` | `0`, `ρ_s − ρ_c`, `ρ_a − ρ_c`, `ρ_s − ρ_a`, `2ρ_a − ρ_c − ρ_s` † |
| `TM` | `0`, `ρ_o − ρ_s`, `ρ_s − ρ_o`, `2(ρ_s − ρ_o)` |
| `TP`, `TQ` (trivial splits) | `ρ_c`, `ρ_s`, `ρ_a`, `2ρ_a − ρ_s`, `2ρ_a − ρ_o` |
| every term of a split that is not displayed | `0`, identically in `ρ` |

*Sufficiency.*  Under the conditions of (a), resp. (b), every form is `≥ 0` and both `T4` forms are `> 0`;
so `α > 0` on displayed splits, `α = 0` on the others (for **every** `ρ`), and trivial splits have
`α/2 ≥ n − 2 > 0`.

*Necessity.*  `ρ_a < ρ_o`: the 4-cycle network has `α = 4(ρ_o − ρ_a)` on its two non-trivial splits.  For
each of the forms `F ∈ {ρ_s − ρ_o, ρ_o − ρ_s, ρ_a − ρ_c}`, and `2ρ_a − ρ_c − ρ_s` in case (a), there is a
structure of the class on six leaves with a displayed split and a pair `z,w` of **non-hybrid** leaves
whose local term is `F` (`parametric_witnesses_A.py`, `parametric_theorem.py`).  Replacing `z` and `w` by
clades of `m` leaves stays in the class; the `m²` pairs `(z',w')` all have local term `F`, pairs inside a
clade have local term `0`, and all other terms number `O(m)`.  So the weight of that split is
`2m²F(ρ) + O(m)`, negative for large `m` if `F(ρ) < 0`.  `ρ_s ≤ 2ρ_a` (given `ρ_o = ρ_s`): in the `n`-sunlet
the trivial split of the hybrid leaf has `α/2 = n − 2 + ((n−3) + C(n−3,2))·(2ρ_a − ρ_s)`.  ∎

So the question of [HABIMRW] has a sharp answer for the class of that paper: the conclusion of its
Theorem 4.7 extends to exactly a three-dimensional cone in the four-dimensional parameter space
(`ρ_s = ρ_o`, `ρ_c ≥ 0`, `ρ_a ∈ [(ρ_c+ρ_s)/2, ρ_s)`; two free parameters after normalising `ρ_s = 1`),
of which NANUQ is the vertex `(ρ_c, ρ_a) = (0, ½)`.

*Relation to the third-party summary (B-II).*  That page states, for a "local four-score family", the
domain "s = o = 1, 1/2 ≤ a ≤ 1, 0 ≤ c ≤ a" of an "anchor-positivity" property.  We cannot tell from the
summary what property that is.  For circular decomposability with exact support, that domain (with
`a < 1`) is our condition (b) for networks whose hybrids have leaf children; for the full class with any
number of blobs it is not sufficient — Modified NANUQ lies in it and fails on a level-1 network.

## 9. What is not shown

* Nothing about networks that are not outer-labeled planar.
* Theorem 9 gives one family; we have not classified the non-galled planar networks for which the
  statement survives (it does on six leaves for `N(1,1)`).
* For the class of bloblets alone the exact parameter domain is not determined (condition (b) of Theorem 11
  is sufficient; our necessity witnesses use pendant clades).
* The finite checks are computations by this division; the proofs are internally reviewed only.
* Theorem 7 was reached independently, but after a third-party claim of the same statement.

## 10. Reproduction (`experiments/complexity/nanuq/`, Python 3 + `networkx`)

| program | what it establishes | time |
|---|---|---|
| `five_point_facts.py` | Lemma 4 | seconds |
| `check_decomposition.py` | Proposition 2 (identity), non-negativity of all local terms on network systems with ≤ 7 leaves | minutes |
| `verify_class.py` | Lemma 8: `𝒜_n`, `𝒞_n` for `n ≤ 6`; agreement with a second generator (`multiblob.py`) | ≈ 1 min |
| `characterize6.py` | the numbers 150 / 141 / 127 / 108, Theorem 10 | ≈ 2 min |
| `test_bloblets.py k n…`, `test_multiblob.py n` | direct test of the conclusion of Theorem 7 on all bloblets of level `k` / all networks with `n` leaves | minutes |
| `counterexample7.py`, `verify_nongalled.py`, `verify_nongalled2.py`, `nongalled_family.py` | Theorem 9 | seconds–minutes |
| `exhaust_all_systems.py`, `exhaust_tree_generated.py` | CX-D2 | seconds |
| `parametric_theorem.py` | Theorem 11(a): parametric decomposition identity, local forms on `𝒞_{≤6}`, witnesses | ≈ 2 min |
| `parametric_classA.py`, `parametric_witnesses_A.py`, `parametric_o_gt_s_witness.py` | Theorem 11(b): local forms on `𝒜_{≤6}`, witnesses with non-hybrid `z,w` | minutes |
| `modified_nanuq_witness.py` | Theorem 11(c), from the explicit rooted network | seconds |
