# The NANUQ metric: a local criterion, all galled planar networks, and why "galled" cannot be dropped

Working paper of the complexity division, first version 2026-11-26; **revised 2026-11-26 after the internal
adversarial reviews `COMPLEXITY-REV-0002` and `COMPLEXITY-REV-0004`** (what changed: §11); §7.1 and §7.2 are
later additions that no referee has seen.  Register: `THEOREMS.md` CX-T5–CX-T9, CX-T13,
CX-V3.  Problem: `OPEN_PROBLEMS.md` B (Holtgrefe, Allman, Baños, van Iersel, Moulton, Rhodes, Wicke,
*Distinguishing Phylogenetic Level-2 Networks with Quartets and Inter-Taxon Quartet Distances*, Bull. Math.
Biol. 2025; cited as [HABIMRW] by the numbering of arXiv:2507.17308v2).  References are listed in §12.

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
   **This is in all likelihood a rediscovery.**  The same all-level statement was posted on 2026-09-30 in
   an unreviewed third-party entry (`PRIOR_ART.md` B-II), whose public summary names "a six-label
   reduction, exact finite certificate and composition identity" and counts "plane-tree and duplication
   instances" and "122 distinct quartet systems" — and `122 = 1 + 3 + 16 + 102` is the number of systems of
   our class 𝒜 on 3, 4, 5 and 6 leaves (observation of the referee).  So not only the statement but
   probably the method (a six-leaf criterion, planar trees with duplicated leaves, composition along cut
   edges) coincides.  We have not seen that proof — this session could not read the repository — and
   derived ours independently on 2026-11-26; neither is peer reviewed.  If theirs is correct, priority is
   theirs.
3. **Theorem 9 (galled cannot be dropped)** [X + P].  An explicit outer-labeled planar level-2 bloblet on
   seven leaves that is not galled, whose NANUQ metric is Kalmanson for none of the 360 circular orders;
   and a two-parameter family in which a displayed split has weight exactly `2 − C(s+t, 2)`.  This concerns
   the NANUQ metric of [HABIMRW] Def. 4.1; the multiplicity-weighted "displayed quartet metric" of their
   §3 is circular decomposable for every outer-labeled planar network (their Corollary 3.4).  We and the
   referee found no such example in the literature (searches recorded in `PRIOR_ART.md` §B).
4. **Theorem 10 (the criterion is sharp)** [X].  Among classes of tree-generated circular split systems
   closed under restriction and under replacing a leaf by a cherry, the class defined by the criterion is
   the largest one on which the NANUQ metric is circular decomposable (for the given order) **with exact
   support**: each of the 23 six-point systems it excludes is, or becomes after doubling a few leaves, a
   system whose metric fails — in most cases by having the wrong support while remaining Kalmanson.  This
   is a statement about classes of split systems, not about classes of networks (§7).
   **Theorem 10′ (added after the review, unreviewed)** [P + X] gives the sharp class for "Kalmanson" alone:
   the systems none of whose six-point restrictions contains its three 3-splits without containing all
   six 2-splits (133 of the 150 six-point systems instead of 127); each of the 17 excluded six-point
   systems becomes, after two of its leaves are replaced by clades of at most three leaves, a system whose
   metric is Kalmanson for no circular order (§7.1).
5. **Theorem 11 (the parametric family, problem B3)** [P + X].  For the four-parameter family of quartet
   distances of NANUQ⁺ the conclusion holds on the whole class exactly when `ρ_o = ρ_s` and
   `ρ_c + ρ_s ≤ 2ρ_a < 2ρ_s`; the *Modified NANUQ* distance is outside this set and fails on an explicit
   level-1 network with eight leaves, but it works when every hybrid node has a leaf child.
6. **Theorem 12 (level 2 completely; added after the review, unreviewed)** [P + X].  An outer-labeled planar
   blob with two hybrid nodes is galled or *nested* (one hybrid node below the other), and a nested blob
   has a three-parameter list of positions.  In an outer-labeled planar network of level at most 2 the only
   splits whose weight can have the wrong sign are the *critical splits*, one per nested blob, and the
   weight of a critical split is `β_1·G + ξ_1·R − Σ β_jβ_l`, an explicit polynomial in the numbers of leaves
   hanging at the positions.  So for level 2 the statement of B1 holds for a network **if and only if** these
   numbers are positive; for bloblets: `k_1 + k_2 > C(k_B − 1, 2)`, resp. `k_1 + 1 > C(k_B − 2, 2)` when no leaf
   hangs between the lower hybrid node and the far branch node (§7.2).  This contains both formulas of
   Theorem 9.

Labels: [P] paper proof (ours; internally reviewed only), [X] exact finite computation with integer
arithmetic (programs in `experiments/complexity/nanuq/`, listed in §10), [V] checked by the Lean kernel
(`experiments/complexity/lean/NanuqFinite.lean`: the finite facts of Lemma 4, of Lemma 8 for a given list
of systems, of Proposition 2 on five and six points, and the numbers 150 / 141 / 127 of §7 — not the
general proofs), [K] a known result that we cite.

Numbering.  Lemmas and propositions are numbered 1–8, A, B, 0, B0, C, D (and Corollary 5′); theorems 4, 6,
7, 9, 10, 10′, 11, 12 (with Corollaries 13, 14).  The theorem
numbers are kept from the first version because other files cite them ("Theorem 6" was "Theorem 6′").

---

## 1. Definitions

**Circular orders and splits.**  `X = {x_1,…,x_n}` with the circular order `C = (x_1,…,x_n)`
(indices mod `n`).  Metrics and split weights are considered for `n ≥ 4`; split systems, restrictions and
the classes of §4 for `n ≥ 2` (they occur as pieces in §5).  The *gap* `g_i` lies between `x_i` and `x_{i+1}`.  For `i ≠ j` the circular split
`S_ij = U_ij | V_ij` has `U_ij = {x_{i+1},…,x_j}`.  A split is trivial if a side is a singleton.  A set `Σ` of
circular splits is *tree-generated* if it is a union of split systems of binary trees with leaf set `X`
whose splits are circular for `C` (it then contains all trivial splits; for `n ≤ 3` it consists of them).
For `Y ⊆ X`, `|Y| ≥ 2`, the restriction `Σ|_Y` is the set of non-empty splits `A∩Y | B∩Y`; it is
tree-generated for `C|_Y`.

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
([HABIMRW] Prop. 2.8; a known result, [K]) a symmetric `d` with zero diagonal equals `½ Σ α_ij δ_{S_ij}`; `d` is circular
decomposable for `C` iff all `α_ij ≥ 0`, and then its support is `{S_ij : α_ij > 0}`.

**Networks** (definitions of [HABIMRW] §2).  A binary *semi-directed network* `N` on `X` is obtained from
a rooted binary network whose root is the least stable ancestor of `X` (a *rooted partner*) by undirecting
the non-hybrid edges and suppressing the root; it may have parallel edges.  `T(N)` is the set of trees
*displayed* by `N` (delete one hybrid edge per hybrid node — a *switching* — then clean up) and
`Split(T(N))` the union of their split systems.  For `Y ⊆ X`, `|Y| ≥ 2`, the *subnetwork* `N|_Y` is the
union of all up-down paths between leaves of `Y`, with degree-2 nodes suppressed (Def. 2.5); for `|Y| = 4`
it is a *quarnet*.  The NANUQ metric `d_N` (Def. 4.1) is `d_N(x,y) = Σ_{z,w} 2ρ_xy(N|_{xyzw}) + 2n − 4`,
where `ρ_xy` of a quarnet is the **unweighted** average of `ρ_xy(T)` over the quartet trees `T` that the
quarnet displays (their Eq. (10)).

**Lemma 0 (restriction commutes with display) [P].**  For a semi-directed network `N` on `X` and `Y ⊆ X`,
`|Y| ≥ 2`:  `T(N|_Y) = { T|_Y : T ∈ T(N) }`.

This is used, with multiplicities and without separate proof, in the proof of [HABIMRW] Lemma 3.2.

*Proof.*  Work in a rooted partner.  In a switching every node other than the root has exactly one parent,
so a switching is a spanning tree, and its path between two leaves goes up to their last common ancestor
and down again: it is an up-down path.  Let `U` be the union of the up-down paths of `N` between leaves of
`Y`, with the orientation of the rooted partner; `N|_Y` is `U` with degree-2 nodes suppressed.

*`U` has exactly one node without an entering edge, the least stable ancestor `ℓ` of `Y`* (the lowest node
through which every path from the root to a leaf of `Y` passes).  This step was missing in the previous
version (REV-0004, finding 9; the argument is the referee's).  (1) *Every node of `U` is a descendant of
`ℓ`.*  Let `a` be the apex of an up-down path between `y, y' ∈ Y`.  A path from the root to `a` followed by
the down part to `y` passes through `ℓ`, and so does the one continued to `y'`.  If `ℓ` were not on the part
from the root to `a`, it would lie strictly below `a` on both down parts, which have only `a` in common.
(2) *`ℓ` is an apex.*  `ℓ` is not a hybrid node (its child would be a lower stable ancestor) and not a
leaf.  If there were no two paths from `ℓ` to two different leaves of `Y` with only `ℓ` in common, then by
Menger's theorem (join all leaves of `Y` to a new sink) one node other than `ℓ` would lie on all paths from
`ℓ` to `Y`; it is not a leaf since `|Y| ≥ 2`, and it would be a lower stable ancestor.  So `ℓ ∈ U`, and by (1)
no edge of `U` enters `ℓ`.  (3) *Every other node `b` of `U` has an entering edge in `U`.*  This is clear
if `b` lies on an up-down path of which it is not the apex.  Let `b ≠ ℓ` be the apex of an up-down path with down
parts `D_1` to `y_1` and `D_2` to `y_2`.  As `b` is below `ℓ` it is not a stable ancestor, so there is a path
`P` from `ℓ` to some `y ∈ Y` avoiding `b`; let `R` be a path from `ℓ` to `b`, `c` the last node of `R` on `P`
(`c ≠ b`), `R'` the part of `R` from `c` to `b`, which meets `P` only in `c` and ends with an edge `e` entering
`b`, and `P'` the part of `P` from `c` to `y`.  The nodes of `R'` other than `b` are proper ancestors of `b`,
those of `D_1`, `D_2` other than `b` proper descendants.  If some `D_i` is disjoint from `P'`, then `R'D_i` and
`P'` are two paths from `c`, to `y_i ≠ y`, with only `c` in common.  Otherwise let `p` be the first node of
`P'` on `D_1 ∪ D_2`, say on `D_1` (`p ≠ b`, `p ≠ c`); then `P'` up to `p` followed by `D_1` from `p`, and `R'D_2`, are
two paths from `c`, to `y_1 ≠ y_2`, with only `c` in common.  In both cases we have an up-down path with apex
`c` between leaves of `Y` that contains `e`.

Consequently every node of `U` is reached from `ℓ`, a switching of `U` (one entering edge kept at every node
with two entering edges in `U`) is a tree rooted at `ℓ` that contains `Y`, and `N|_Y` is a semi-directed
network with rooted partner `U`.  (⊇) Let `S` be a switching of `N` and `S_Y` the union of its paths between leaves of `Y`.
Then `S_Y ⊆ U`, and `S_Y` contains at most one hybrid edge at each node; a switching of `U` that keeps, at
each of its hybrid nodes, the edge lying in `S_Y` if there is one contains `S_Y`, and being a tree it
displays the same tree on `Y` as `S`.  (⊆) Let `S'` be a switching of `U`.  Choose a switching `S` of `N`
that keeps the edge of `S'` at every node with both hybrid edges in `U`, and the hybrid edge lying in `U`
at every node with exactly one hybrid edge in `U`.  Then `S' ⊆ S`, so the paths of `S` between leaves of `Y`
are those of `S'`.  ∎

**Lemma 1 [P].**  If `N` is outer-labeled planar with induced circular order `C`, then `Σ = Split(T(N))` is a
tree-generated circular split system for `C` and `d_N = d_Σ`.

*Proof.*  Every displayed tree is planar for `C`, so its splits are circular ([HABIMRW] Prop. 2.9), and
the displayed trees are binary: tree-generated.  By Lemma 0 the quartet trees displayed by the quarnet
`N|_{xyzw}` are the restrictions `T|_{xyzw}`, `T ∈ T(N)`; a tree restricts to `ab|cd` iff one of its splits
separates `{a,b}` from `{c,d}`.  So for each 4-set the set of quartet trees over which Eq. (10) averages is
the set of quartets displayed by `Σ`, and the two metrics are defined from these sets by the same
formula.  ∎

So the conjectures are statements about a family of circular split systems.  They are *not* true for
all tree-generated systems: on six points 9 of the 150 tree-generated systems fail (§7; `DEAD_ENDS.md`
CX-D2).

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

**Lemma 4 (the 5-point terms take care of themselves) [X, V].**  For *every* tree-generated system on five
points, in every placement: `Φ5 ∈ {0, ½, 1}`, `Φ5 = 0` if `u_1u_p|v_1v_q` is not displayed, and
`Ψ ∈ {0, ½, 1}`.  (16 systems × 10 placements; `five_point_facts.py`; Lean: `five_point_facts`, with the
trees and the tree-generated systems defined inside Lean, not imported.)

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

**Corollary 5′ (the three-split form) [P; re-checked [X]].**  Let `Σ_6` be the restriction of `Σ` to the six
leaves `w, a_1, a_2, a_3, a_4, z` (this circular order).  Then `Φ6 < 0` if and only if `Σ_6` contains the
three 3-splits of these six leaves and does not contain the 2-split `{z,w} | {a_1,a_2,a_3,a_4}`.

*Proof.*  The splits of `Σ_6` are the restrictions of the splits of the trees of `Σ`.  A circular split of
the six leaves that separates `{z,w}` from `{a_1,a_2,a_3}` is `{z,w}|{a_1,…,a_4}` or
`P_1 = {a_4,z,w}|{a_1,a_2,a_3}`; one that separates `{z,w}` from `{a_2,a_3,a_4}` is `{z,w}|{a_1,…,a_4}` or
`P_2 = {z,w,a_1}|{a_2,a_3,a_4}`; and a tree displays `wa_2|a_3z` iff it has a split that restricts to
`Q = {w,a_1,a_2}|{a_3,a_4,z}`, the only circular split separating `{w,a_2}` from `{a_3,z}`.  So the four
conditions of Lemma 5 say `P_1, P_2, Q ∈ Σ_6` and `{z,w}|{a_1,…,a_4} ∉ Σ_6`; and `P_1, P_2, Q` are the three
3-splits.  ∎

(`kalmanson_only.py extra` confirms the equivalence for all 150 six-point systems in all twelve
labellings.)  The three 3-splits of six points are pairwise incompatible, so they come from three
different trees; the condition says that, in restriction to the six leaves, these three trees exist
while no tree has the cherry `{z,w}`.

---

## 4. Planar trees with twin leaves (class 𝒜) and substitution

**Class 𝒜.**  An *𝒜-structure* is a binary tree `T` whose leaves are a circularly ordered set `P` of
*positions* (the splits of `T` circular), with pairwise disjoint pairs of circularly adjacent positions
(*twins*).  Its leaves are the unpaired positions and the pairs, in the induced circular order; its
*displayed trees* are obtained from `T` by deleting one position of each pair; its split system `Σ(T)` is
the union of their split systems.  `𝒜_n`, `n ≥ 2`, is the set of such systems on `n` leaves (so at most `n`
pairs, `|P| ≤ 2n`); `𝒜_2` and `𝒜_3` consist of the one system of trivial splits.

**Proposition 6 (union property in 𝒜) [P].**  In an 𝒜-system: if a displayed split separates `{z,w}` from
`{a_1,a_2,a_3}` and a displayed split separates `{z,w}` from `{a_2,a_3,a_4}` (leaves in the circular order
`w,a_1,a_2,a_3,a_4,z`), then a displayed split separates `{z,w}` from `{a_1,a_2,a_3,a_4}`.  Hence `Φ6 ≥ 0`
everywhere in 𝒜 (Lemma 5).

*Proof.*  A displayed split comes from an edge of the one tree `T`, i.e. from a set `I` of positions that is
an interval of `P`, together with a choice of one position per pair: a leaf lies on the side of `I` iff its
chosen position is in `I`.  Let `I_1`, `I_2` be the intervals of the two given splits: `I_1` contains a
position of each of `a_1,a_2,a_3` and misses a position of `z` and one of `w`; `I_2` likewise for `a_2,a_3,a_4`.
An interval that contains a position of `a_2` and a position of `a_3` contains one of the two arcs between
them; the arc through `a_4, z, w, a_1` contains every position of `z`, and `I_1`, `I_2` each miss one; so
each of `I_1`, `I_2` contains the short arc between its positions of `a_2` and `a_3`, in particular the
last position of `a_2`: they intersect.  We claim that some position lies in neither.  Otherwise every position missed by `I_1` lies in `I_2` and conversely, so `z` and
`w` are twin pairs and each of `I_1`, `I_2` contains exactly one position of `z` and one of `w`.  An interval
containing a position of `a_2`, exactly one position of `w` and exactly one of `z` is the interval from the
second position of `w` to the first position of `z`; so `I_1 = I_2`, and they miss common positions — a
contradiction.  Two edges of a tree whose sides `I_1`, `I_2` intersect and miss a common leaf are nested, say
`I_1 ⊆ I_2`.  Then `I_2` contains a position of each of `a_1,…,a_4` and misses positions of `z` and `w`;
choosing these positions (the choices at different pairs are independent) gives a displayed tree with a
split separating `{z,w}` from `{a_1,a_2,a_3,a_4}`.  ∎

This is the structural reason behind the theorem of [HABIMRW] and its extension: *when every hybrid node
has a leaf child, all displayed trees are restrictions of one planar tree, with independent choices*
(Lemma A); a general galled planar network is glued from such pieces along cut edges (Lemma B).  In a
network that is not galled the choices need not be independent, the union property can fail, and then so
can the theorem (§6) — although most non-galled planar networks still satisfy its conclusion (§6, Remark 3).

**Substitution.**  For circular split systems `Σ_1` on `X_1 ∋ p` and `Σ_2` on `X_2 ∋ r`, `|X_1|, |X_2| ≥ 2`,
the system `Σ_1 ∘_{p,r} Σ_2` on `(X_1∖p) ∪ (X_2∖r)` (circular order: that of `X_1` with `p` replaced by
`X_2∖r` in the order following `r`) consists of the splits of `Σ_1` with `p` replaced by `X_2∖r` and the
splits of `Σ_2` with `r` replaced by `X_1∖p`.  (A factor with two leaves does nothing: `Σ_1 ∘_{p,r} Σ_2` is
then the other factor with `r`, resp. `p`, renamed.)  Let `𝒞` be the smallest class of systems containing
all `𝒜_n`, `n ≥ 2`, and closed under `∘`.

**Lemma 7 (restrictions) [P].**  (i) The restriction of an 𝒜-system to `Y` is an 𝒜-system on `Y`
(restrict `T` to the positions of the leaves of `Y`; twins stay adjacent).  (ii) For `Y` meeting both
`X_1∖p` and `X_2∖r`,  `(Σ_1 ∘ Σ_2)|_Y = Σ_1|_{(Y∩X_1)∪p} ∘ Σ_2|_{(Y∩X_2)∪r}`; if `Y` misses one of them the
restriction is a restriction of the other factor.  (iii) Consequently every restriction of a system of
`𝒞` to `m` leaves, `2 ≤ m ≤ 6`, lies in `𝒞_m`, the set of systems on `m` leaves obtained from `𝒜_{≤ 6}` by
substitutions all of whose intermediate systems have at most 6 leaves.

*Proof.*  (i), (ii) are immediate from the definitions (displayed trees restrict to displayed trees; a
restricted tree's splits are the restricted splits).  (iii) by induction on the construction of the
system: in (ii) both factors have at least 2 and at most `|Y| − 1 + 1 ≤ 6` leaves.  ∎

**Lemma 8 (finite check) [X; the last assertion also V].**  `|𝒜_4| = 3`, `|𝒜_5| = 16`, `|𝒜_6| = 102`;
`|𝒞_4| = 3`, `|𝒞_5| = 16`, `|𝒞_6| = 108`; every system of `𝒞_6` is 6-locally good (and satisfies the
5-point facts on all its 5-subsets).  Programs: `twin_trees.py`, `verify_class.py`, `characterize6.py`.
(`𝒜_6` is computed from all binary trees on `6 + k` circular positions, `k ≤ 6`, with all choices of `k`
disjoint adjacent pairs; the closure from factors with at least three leaves, two-leaf factors being
trivial.)  The 108 systems fall into 17 classes under rotation and reflection, 16 of them in `𝒜_6`; they
are listed with their values of `Φ6` in Appendix B, so that the last assertion can be checked by hand; it
is also checked by the Lean kernel for the list of 108 systems (`closure_locally_good`;
`export_lean_lists.py` checks that the list in the Lean file is the computed closure).  The referee
recomputed 1 / 3 / 16 / 102 and 108 with independent code.

**Theorem 6 (class 𝒞) [P + X].**  Every system of `𝒞` on `n ≥ 4` leaves is 6-locally good; hence, by
Theorem 4, its NANUQ metric is circular decomposable with support exactly the system.

*Proof.*  Lemma 7(iii) and Lemma 8 (for `n ≤ 5` there is nothing to check).  ∎

---

## 5. All galled outer-labeled planar networks

**Lemma A (hybrids with a leaf child) [P].**  Let `N` be a binary semi-directed network on `n ≥ 2` leaves
with an outer-labeled planar embedding inducing `C`, in which every hybrid node is adjacent to a leaf.
Then `Split(T(N)) ∈ 𝒜_n`.

*Proof.*  For each hybrid node `h` with parents `p_h`, `p'_h` and leaf `x_h`, delete `h` and `x_h` and attach
two new leaves `x_h^-` to `p_h` and `x_h^+` to `p'_h`.  The result `T` is a tree: the switching of `N` that keeps
all edges `p_h h` is a spanning tree of `N` (in a rooted partner every non-root node keeps exactly one
parent), and `T` is this tree with `h` suppressed and one pendant leaf `x_h^+` added per hybrid.  All its
internal nodes have degree 3.  In the embedding, `h` and `x_h` can be replaced by two leaves drawn along
the two sides of the path `h x_h`, so `T` is planar with `x_h^-`, `x_h^+` adjacent on the outer face in the
place of `x_h`.  Deleting the hybrid edge `p'_h h` of `N` corresponds to deleting `x_h^+` of `T`.  So the
displayed trees of `N` are those of the 𝒜-structure.  (The two parents of `h` may coincide — parallel
edges — and a hybrid edge may pass through the suppressed root; the argument is unchanged.)  ∎

**Lemma B0 (the edge below a hybrid node is a cut edge) [P].**  Let `N` be a binary semi-directed galled
network and `h` a hybrid node with child `c`.  Then `c` is not a hybrid node and `e = (h,c)` is a cut edge.

([HABIMRW] state after Def. 2.3, without proof, that in the binary case "galled" is equivalent to every
hybrid node being an articulation node.  The proof below is the referee's.)

*Proof.*  Work in a rooted partner; "galled" is Def. 2.3(vi): for every hybrid node the two hybrid edges
entering it lie on a cycle of the underlying graph that contains no other hybrid edge.  If `c` were a
hybrid node, its cycle would contain the hybrid edge `(h,c)` and a second edge at `h`, which is a hybrid
edge entering `h`: impossible.  Let `D` be the set of descendants of `c`, `c` included.  If `e` lay on a
cycle, some other edge would join `D` to its complement; as `D` is closed under taking children it is
directed from some `a ∉ D` to some `b ∈ D`, and `b ≠ c` because the only parent of `c` is `h`.  Then `b` also
has a parent `a' ∈ D`, so `b` is a hybrid node.  Its cycle, minus `b`, is a path from `a'` to `a` without
hybrid edges.  It leaves `D`; the edges entering `D` are `e` and hybrid edges (the head of any other edge
entering `D` has a second parent in `D`); so the path uses `e`, arrives at `h`, and must continue along one
of the two other edges at `h`, which are hybrid edges (`a ≠ h` because `b ≠ c`): a contradiction.  ∎

**Lemma B (cutting below a hybrid) [P].**  Let `N` be binary, semi-directed, outer-labeled planar and
galled, on at least two leaves, and `h` a hybrid node whose child `c` is not a leaf.  Cut the cut edge
`e = (h,c)` and cap both ends with new leaves `p` (at `h`) and `r` (at `c`).  The two pieces `N_1 ∋ p`,
`N_2 ∋ r` are binary semi-directed networks on at least two leaves each, outer-labeled planar with the
induced circular orders, and galled; each has fewer hybrid nodes with a non-leaf child than `N`; and
`Split(T(N)) = Split(T(N_1)) ∘_{p,r} Split(T(N_2))`.

*Proof.*  Let `D` be the set of descendants of `c` in a rooted partner `N⁺`.  By Lemma B0 no edge other than
`e` joins `D` to the rest.  *`N_1`*: replace `D` by the leaf `p`; this is a rooted binary network whose root
is still the least stable ancestor of its leaves, and it has a leaf other than `p` (otherwise every path
from the root to a leaf of `N⁺` would pass through `h`).  *`N_2`*: a new root with children `r` and `c`,
above the network induced on `D`; the root is the least stable ancestor because `r` is its child, and `c`,
not being a leaf, has a leaf below it.  Suppressing the roots gives the two pieces.  A cycle of `N` does
not contain the cut edge `e`, so the cycle required by Def. 2.3(vi) for a hybrid node of a piece lies in
that piece: the pieces are galled.  A planar embedding of `N` with the leaves on the outer face gives one
of each piece by contracting the other side of `e` to a point (the leaves on one side of a cut edge are
consecutive in the circular order).  In `N_1` the node `h` now has a leaf child and the other hybrid nodes
are unchanged; `N_2` does not contain `h`.  Finally, a switching of `N` is a spanning tree containing the
bridge `e`; removing `e` leaves switchings of the two pieces, and conversely switchings of the pieces
combine.  So the displayed trees of `N` are exactly the trees obtained by joining a displayed tree of `N_1`
and one of `N_2` at `p`, `r`, and the splits of a joined tree are those described in the definition of
`∘`.  ∎

(The first version called the pieces "marked networks" and said that `N_2` might have no rooted partner;
that was wrong and unnecessary — REV-0002, finding 4.  The referee cut 4000 explicit networks: both pieces
were always valid networks of the class; the piece `N_1` had two leaves in 159 cases and three in 304.
The referee of REV-0004 cut 1 902 times in 2 795 explicit networks: `N_1` had two leaves in 221 cuts, `N_2`
always at least three; no failure of Lemma B0, Lemma B or Theorem 7, and none of Lemma B0 on 1 417 networks
that are not planar.)

**Theorem 7 (all levels, any number of blobs) [P + X].**  Let `N` be a binary semi-directed network on
`n ≥ 4` leaves that is outer-labeled planar and galled (no bound on the level, any number of blobs).
Then `d_N` is circular decomposable, for every circular order induced by `N`, and its support is exactly
`Split(T(N))`.

*Proof.*  We show, for all networks of this kind on `n ≥ 2` leaves, that `Split(T(N)) ∈ 𝒞`, by induction on
the number `μ` of hybrid nodes whose child is not a leaf.  If `μ = 0`, `Split(T(N)) ∈ 𝒜_n ⊆ 𝒞` by Lemma A.
Otherwise cut below such a hybrid node: by Lemma B both pieces are networks of the same kind with smaller
`μ`, their systems are in `𝒞` by induction, and so is the substitution.  For `n ≥ 4`, Theorem 6 and Lemma 1
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

**The family `N(s,t)`**, `s,t ≥ 0`.  *Bloblet version*: the same blob with `t` leaves `a_1,…,a_t` hanging
along the path from the root to `p1` and `s` leaves `d_1,…,d_s` along the path from the root to `q1` (`d_1`
nearest to `q1`); `N* = N(1,2)`.  *Clade version*: the `a_i` form one pendant clade and the `d_j` another,
each attached to the cycle at a single point (on the root–`p1` path, resp. the root–`q1` path).  Circular order `(a_1,…,a_t, b, x, y, c, d_1,…,d_s)`.  In both versions the
four displayed trees are obtained from those of `N*` in the obvious way (`nongalled_formula.py` lists them).

**Theorem 9 [X + P].**  (a) For the planar order, the displayed split `{x,y} | {a1,a2,b,c,d}` of `N*` has
weight `α = d(b,y) + d(x,c) − d(b,c) − d(x,y) = 24 + 24 − 29 − 20 = −1`.  (b) `d_{N*}` is not circular
decomposable: for each of the 360 circular orders of the seven leaves some `α_ij` is negative.  (c) For
all `s,t ≥ 0` the weight of the displayed split `{x,y} | rest` of `N(s,t)`, for the planar order, is

```
α = 2 − C(s+t, 2)      (bloblet version),            α = 2 − s·t      (clade version).
```

Programs: `counterexample7.py`, `verify_nongalled.py`, `verify_nongalled2.py` (built on `netcalc.py`, which
works from the explicit rooted network and shares no code with the split-system programs),
`nongalled_family.py`, `nongalled_formula.py`.  The referee recomputed (a), (b) and 11 values of each
formula in (c) with independent code.  `nongalled_formula.py` takes the four displayed trees of the family
by formula, not from networks (REV-0004, finding 11); the second referee built the explicit rooted networks
and found the same split systems for `0 ≤ s,t ≤ 6` in both versions and the same 192 values of the two
formulas for `0 ≤ s,t ≤ 7`; and `level2_fourtrees_check.py`, `level2_explicit.py` (§7.2) do the same for the
larger family that contains this one.

*Proof of (c).*  Here `U = (x,y)` and `V = (c, d_1,…,d_s, a_1,…,a_t, b)`, so by Proposition 2
`α/2 = Φ4 + Σ_z Φ5'(z) + Σ_{z,w} Φ6'(z,w)` with `z, w` running over the `d_j` and the `a_i`.  Each term
depends only on the restriction of the split system to `x, y, c, b` and the one or two leaves `z, w`, which
is the split system of the member of the family having only those leaves (restrict the four displayed
trees).  So six numbers have to be computed, on 4, 5, 5, 6, 6 and 6 leaves [X]: `Φ4 = 1`; `Φ5' = 0` for a
leaf `d` and for a leaf `a`; and `Φ6' = −½` for each of the three kinds of pair in the bloblet version,
while in the clade version `Φ6' = −½` for a pair `(d_j, a_i)` and `0` for two leaves of the same clade.
Hence `α/2 = 1 − ½·C(s+t,2)`, resp. `1 − ½·st`.  ∎

*Why.*  The restriction of `Split(T(N*))` to `{d, a_i, b, x, y, c}` contains every circular split of these six
leaves except `{d,a_i} | {b,x,y,c}`.  With `z = d`, `w = a_i`, `(a_1,…,a_4) = (b,x,y,c)`: the displayed trees
cut `{d,a_i}` off from `{b,x,y}` (when `x,y` hang on the `b` side) and from `{x,y,c}` (when they hang on the `c`
side) but never from all four — the union property fails because `y` follows `x` when `h1` switches.

So Theorem 4.7 of [HABIMRW] does not extend to outer-labeled planar level-2 networks that are not
galled, not even for bloblets, and not even with the weaker conclusion "circular decomposable for some
order" (shown for `N*`).

**Remarks.**
1. *Which metric.*  The statement is about the NANUQ metric of [HABIMRW] Def. 4.1, whose `ρ` ignores the
   multiplicities of displayed quartets (their Eq. (10)) — the metric of their Theorem 4.7 and of their
   conjectures.  Their multiplicity-weighted *displayed quartet metric* is circular decomposable with support
   `Split(T(N))` for **every** outer-labeled planar network (their Corollary 3.4), `N*` included (the
   referee computed weight `5` for `{x,y}|rest` there).  The failure is specific to the multiplicity-free
   averaging outside the galled class.
2. *Seven leaves are needed* for two hybrid nodes: in the bloblet version the weight is negative exactly for
   `s + t ≥ 3`, and according to the referee's exhaustive pass over the outer-labeled planar networks with
   two hybrid nodes on 4, 5 and 6 leaves (obtained by hybrid insertion) none violates the conclusion.
3. *Most non-galled planar networks still satisfy the conclusion.*  In the referee's enumeration on 7
   leaves, of 60 196 non-galled insertion sequences 664 give a negative weight (all bloblets) and 1 252 a
   wrong support only (none of them bloblets).  For level 2 the networks for which the conclusion holds
   are now classified (§7.2, Theorem 12, added after the review); for higher levels they are not.

---

## 7. The criterion is sharp

On six points there are 150 tree-generated systems; 141 have a NANUQ metric that is Kalmanson with exact
support; 127 are 6-locally good; 108 are in `𝒞` (`characterize6.py`; the first three numbers are also
checked by the Lean kernel from definitions inside Lean, `tg6_length`, `tg6_globally_good`,
`tg6_locally_good`, and were recomputed by the referee).

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

*What "sharp" does and does not mean* (REV-0002, finding 10).  (i) The failure in "only if" is a failure of
*Kalmanson with exact support*.  Of the 9 six-point systems that fail, 6 remain Kalmanson and only have a
positive weight on an undisplayed split (the second type in (a)); according to the referee, 12 of the 14
minimal blow-ups in (b) likewise remain Kalmanson with a wrong support, larger blow-ups reach a negative
weight for 17 of the 23 excluded systems, and for the 6 systems missing a 2-split and its crossing 3-split
no blow-up with multiplicities `≤ 3` and at most 11 leaves does.  So for "Kalmanson" alone the criterion is
not sharp; the sharp class for "Kalmanson" alone is the larger class `𝒦′` of §7.1 (Theorem 10′, added after
the review), which explains both observations of the referee.  (ii) The closure operations are those of
abstract split systems.  (iii) The
statement is about classes of split systems: 19 of the 127 systems are not displayed by any network of the
class of [HABIMRW] on six leaves (next paragraph), so nothing sharp is claimed about classes of networks.

By §5 the galled outer-labeled planar networks on six leaves give systems of `𝒞_6`, hence at most 108 of the
127 (and exactly 108 according to a second generator, `multiblob.py`, which builds networks blob by blob and
respects the existence of a rooted partner); the remaining 19 systems satisfy the criterion and are not
displayed by any network of that class on six leaves.

### 7.1 The sharp class for "Kalmanson" alone, as a forbidden six-leaf pattern

*Added 2026-11-26 after the review; not seen by any referee.*

Six points in circular order have nine non-trivial circular splits: six 2-splits `{x_k,x_{k+1}} | rest` and
three 3-splits.  The 3-splits are pairwise incompatible, and a 2-split `{x_k,x_{k+1}}` is incompatible with
exactly one of them, the one that separates `x_k` from `x_{k+1}`.

**Definition.**  `𝒦′` is the class of tree-generated circular split systems `Σ` such that *every six-point
restriction of `Σ` that contains its three 3-splits contains all its 2-splits* (and is then the system of
all circular splits of the six points).  By Corollary 5′ this is the condition "`Φ6 ≥ 0` in every six-point
restriction and every labelling" — the criterion of Theorem 4 without the requirement that the terms
vanish on undisplayed splits.  So `𝒦 ⊆ 𝒦′`.

**Theorem 10′ [P + X].**
(a) If `Σ ∈ 𝒦′` has `n ≥ 4` points, then `d_Σ` is circular decomposable for `C`, and `α_ij > 0` for every
`S_ij ∈ Σ` (the support contains `Σ`; it may be larger).
(b) `𝒦′` contains every tree-generated system on at most five points and the split system of every tree,
and it is closed under restriction and under substitution `∘`; in particular under replacing a leaf by a
cherry, or by any clade.
(c) Let `Σ_6` be a tree-generated system on six points `u_1, z, w, u_p, v_1, v_q` (this circular order) that
contains its three 3-splits and not the 2-split `{z,w}`, and let `Σ_6(m)` be obtained from it by replacing
`z` and `w` by caterpillar clades `Z` and `W` of `m` leaves each.  In `d_{Σ_6(m)}` the split
`S = {u_1} ∪ Z ∪ W ∪ {u_p} | {v_1, v_q}` has weight

```
α_S / 2  =  Φ4 + m·(Φ5(z) + Φ5(w)) − m²/2 ,
```

with `Φ4`, `Φ5(z)`, `Φ5(w)` the terms of `Σ_6`.  It is negative for every `m ≥ 5`.
(d) [X]  Exactly 17 six-point tree-generated systems contain their three 3-splits and miss a 2-split; they
form four classes under rotation and reflection: all nine splits except one 2-split (6 systems), except
two antipodal 2-splits (3), except two 2-splits at distance two (6), except three alternate 2-splits (2).
Hence
`|𝒦′_6| = 150 − 17 = 133 = 127 + 6`; the six systems of `𝒦′_6` that are not 6-locally good are those that
miss a 2-split and the 3-split incompatible with it.  For each of the 17, the weight in (c) is negative
already for some `m ≤ 3` (at most ten leaves; the formula of (c) agrees with the computed weights for
`m = 1,…,6`), and for the least such `m` the metric `d_{Σ_6(m)}` is Kalmanson for **no** circular order of
its leaves.

*Consequently: a class of tree-generated circular split systems that is closed under restriction and under
replacing a leaf by a cherry has, for all its members, a NANUQ metric that is Kalmanson — for the given
order or, equivalently for such a class, for some circular order — if and only if it is contained in `𝒦′`,
i.e. if and only if none of its six-point members contains the three 3-splits without containing all six
2-splits.*

*Proof.*  (a)  By Proposition 2, `α_ij/2` is a sum of `Φ4 ≥ 0`, of terms `Φ5 ≥ 0` (Lemma 4, applied to the
five-point restrictions), and of terms `Φ6`, `Φ6'`, which are `≥ 0` by Corollary 5′ and the definition of
`𝒦′`.  If `S_ij ∈ Σ` then `Φ4 > 0` (Lemma 3).  Trivial splits have `α/2 ≥ n − 2 > 0` (Lemma 4).

(b)  A system on at most five points has no six-point restriction; the splits of a tree are pairwise
compatible, so no restriction of a tree contains two 3-splits; a restriction of a restriction is a
restriction.  Let `Σ = Σ_1 ∘_{p,r} Σ_2` with `Σ_1, Σ_2 ∈ 𝒦′` (it is tree-generated, by the trees `T_1 ∘ T_2`),
and let `Y` be six of its leaves, `Y_1 = Y ∩ X_1`, `Y_2 = Y ∩ X_2`.  If `|Y_1| ≤ 1` or `|Y_2| ≤ 1` then by
Lemma 7(ii) `Σ|_Y` is, up to the name of one leaf, a six-point restriction of a factor, and the condition
holds.  Otherwise `Σ|_Y = Σ_1|_{Y_1 ∪ p} ∘ Σ_2|_{Y_2 ∪ r}` contains the non-trivial split `S_0 = Y_1 | Y_2`, and
every split of `Σ|_Y` has a side that contains `Y_1` or `Y_2`, hence is compatible with `S_0`.  But `S_0` is a
3-split or a 2-split of the six points, and is incompatible with two, respectively one, of the three
3-splits.  So `Σ|_Y` does not contain the three 3-splits, and there is nothing to check.  Replacing a leaf
by a clade is a substitution of a tree.

(c)  Proposition 2 for `Σ_6(m)` and `S` (here `V∖Y = ∅`):
`α_S/2 = Φ4 + Σ_{x ∈ Z∪W} Φ5(x) + Σ_{ {x,y} ⊆ Z∪W } Φ6(x,y)`, each term being a function of the restriction
of `Σ_6(m)` to the leaves involved.  For `x ∈ Z`, `y ∈ W` the restriction to `{u_1,x,y,u_p,v_1,v_q}` is `Σ_6`
with `z, w` renamed, so `Φ6(x,y) = Φ6(z,w)`, which is negative by Corollary 5′ and therefore `−½` (Lemma
5).  Likewise `Φ5(x) = Φ5(z)` for `x ∈ Z`, `Φ5(y) = Φ5(w)` for `y ∈ W`, and `Φ4` is that of `Σ_6`.  For two
leaves `x, y` of the same clade, the splits of `Σ_6(m)` that separate `x` from `y` are splits of the clade,
with one side inside it; so in each of the four 4-sets occurring in `Φ6(x,y)` only the quartet with the
cherry `xy` is displayed, all four weights are `1`, and `Φ6(x,y) = 1 + 1 − 1 − 1 = 0`.  There are `m²`
pairs of the first kind: this is the formula.  Since `Φ4 ≤ 2` and `Φ5 ≤ 1` (Lemma 4),
`α_S/2 ≤ 2 + 2m − m²/2 < 0` for `m ≥ 5`.

(d)  `kalmanson_only.py` (the counts, the formula for `m ≤ 6`, the least `m`) and `kalmanson_only.py extra`
(the search over all circular orders, by backtracking with the four-point conditions; the search is
tested on the 133 metrics of `𝒦′_6` with scrambled labels, for each of which it finds an order).

*The equivalence.*  "If" is (a).  "Only if": a member outside `𝒦′` has a six-point restriction `Σ_6` as in
(c), after a rotation; `Σ_6` and all `Σ_6(m)` belong to the class (a caterpillar clade arises by replacing
leaves by cherries repeatedly); by (d) one of them is Kalmanson for no circular order.  ∎

**Remarks.**  1. *Two sharp classes, both given by forbidden six-point restrictions.*  `𝒦′` forbids the four
dihedral classes of (d); `𝒦` (Theorem 10, exact support) forbids these and a fifth one, "all nine splits
except a 2-split and the 3-split incompatible with it" (`127 = 133 − 6`).  A system of `𝒦′ ∖ 𝒦` has a
Kalmanson metric which gives positive weight to a split that no tree of the system has.

2. *What it says about networks.*  Let `𝒩` be a class of outer-labeled planar binary semi-directed networks
that is closed under passing to subnetworks `N|_Y` and under replacing a leaf by a cherry.  By Lemma 1,
Lemma 0 and Theorem 10′: **`d_N` is Kalmanson for all `N ∈ 𝒩` if and only if no network of `𝒩` on six leaves
displays the three 3-splits of its leaf order without displaying all six 2-splits** (and the support is
exactly the displayed splits for all `N ∈ 𝒩` iff, in addition, no six-leaf network of `𝒩` displays exactly
the nine splits minus a 2-split and the 3-split incompatible with it — Theorem 10).  So the question
"for which outer-labeled planar networks that are not galled does the conclusion survive" (§6, Remark 3)
is, for classes closed under these two operations, a question about six-leaf networks.  For a single
network only the "if" direction holds: a network whose six-leaf subnetworks avoid the pattern has a
Kalmanson metric, and so do all networks obtained from it by attaching clades in place of leaves.  The
seven-leaf network `N*` of §6 has five six-leaf subnetworks with the pattern (`forbidden_in_nstar.py`), as
it must.

3. *What is not shown.*  For a single system outside `𝒦′` we do not show that it, or one of its own
blow-ups, fails: the argument blows up a six-point restriction.  On six points 14 of the 17 systems of (d)
themselves have a Kalmanson metric.

### 7.2 Level 2 completely: one critical split per nested blob

*Added 2026-11-26 after the review; not seen by any referee.*

Theorem 7 settles the galled networks, and §6 gives one family that is not galled and in which the
conclusion fails.  For level 2 the picture can be completed.  There is exactly one further kind of blob;
in a network containing such blobs only one split per blob can go wrong; and the weight of that split is
an explicit polynomial in the numbers of leaves that hang at the positions of the blob.

**Blobs, positions, sizes.**  Let `N` be a binary semi-directed network with rooted partner `N⁺`, and `𝔅` a
blob of `N⁺` containing hybrid nodes (the two edges entering a hybrid node lie on a common cycle, hence in
one blob).  A node of `𝔅` has two or three edges in `𝔅`.  If it has two, it is the root or it has exactly one
further edge, a cut edge; in the latter case the node is a *position* of `𝔅`, the part of the network beyond
the cut edge is its *pendant subnetwork*, and the number of leaves there is its *size* (`≥ 1`).  Every leaf of
`N` lies in the pendant subnetwork of exactly one position.  Exactly one node of `𝔅` has no parent in `𝔅`,
the *source*: the root, or the position whose pendant subnetwork contains the root (two edges entering `𝔅`
from outside would lie on a cycle).  `𝔅°` is the bloblet obtained by replacing every pendant subnetwork by
one leaf (if the source is a position, a new root is placed on its pendant edge), and
`Σ(𝔅) = Split(T(𝔅°))`, a split system on the set of positions.

**Lemma D (cut edges and pendant subnetworks) [P].**  Let `Σ = Split(T(N))`.
(i) If a cut edge separates the leaves into two non-empty sets `X_1 | X_2`, this split belongs to every
displayed tree, and for `x_1 ∈ X_1`, `x_2 ∈ X_2`:  `Σ = Σ|_{X_1 ∪ {x_2}} ∘_{x_2, x_1} Σ|_{X_2 ∪ {x_1}}`.
(ii) If a set `Y` of leaves meets every pendant subnetwork of `𝔅` in at most one leaf, then
`Σ|_Y = Σ(𝔅)|_Y`, each leaf standing for its position.
(iii) If `Y` meets some pendant subnetworks in two leaves and the others in at most one, then `Σ|_Y` is
obtained from the restriction of `Σ(𝔅)` to the positions met by replacing each position met twice by a
cherry.

*Proof.*  (i) A hybrid edge lies on a cycle, so a cut edge is not a hybrid edge and belongs to every
switching, which is a spanning tree (proof of Lemma 0); so every displayed tree has the split `X_1|X_2`.
Splits of one tree are compatible, hence every split `A|B` of `Σ` has a side inside `X_1` or inside `X_2`.
If `A ⊆ X_1`, then `A | (B ∩ X_1) ∪ {x_2}` is its restriction to `X_1 ∪ {x_2}` and replacing `x_2` by `X_2`
gives `A|B` back; likewise for `A ⊆ X_2`: this shows `⊆`.  Conversely a split of `Σ|_{X_1 ∪ {x_2}}` is the
restriction of some `A|B ∈ Σ`; if `A ⊆ X_1` the substitution returns `A|B`; if `A ⊆ X_2` the restriction is
`{x_2} | X_1` (or empty) and the substitution returns `X_2|X_1 ∈ Σ`.  (ii) A switching of `N⁺` contains
exactly one of the two edges entering each hybrid node of `𝔅`, i.e. a switching of `𝔅`, and all of these
occur; a path of the spanning tree between two nodes of `𝔅` stays in `𝔅` (it cannot use a cut edge twice);
and the path from a leaf of a pendant subnetwork to any leaf outside it passes through its cut edge.  So
the tree displayed on `Y` is the tree spanned in the switching of `𝔅` by the positions met, with a leaf hung
at each: the tree that this switching displays in `𝔅°`.  (iii) By (i) the two leaves in the pendant
subnetwork of a position form a cherry in the restriction to `Y` of every displayed tree; apply (i) to this
cherry and (ii) to `Y` minus one leaf of each such pair.  ∎

**Lemma C (the two kinds of blob with two hybrid nodes) [P].**  Let `𝔅` be a blob with exactly two hybrid
nodes.  With its nodes of degree two suppressed it is a *theta graph*: two *branch nodes* joined by three
internally disjoint paths, whose interior nodes are the positions and possibly the root.  Exactly one of
the following holds.

*Galled kind.*  The hybrid nodes are interior nodes of two different paths.  Each of them lies, with its
two entering edges, on a cycle that avoids the hybrid edges of the other.

*Nested kind.*  One hybrid node `h_1` is a branch node; two of the paths, `A` and `B`, enter it and the
third, `C`, leaves it; the other hybrid node `h_2` is an interior node of `C`; the source lies on `A`, on
`B`, or on `C` between `h_2` and the other branch node `t`.  Every cycle through the two edges entering `h_2`
contains `C`, hence an edge entering `h_1`: the blob is not galled, and `h_1` is an ancestor of `h_2`.

If `N` is outer-labeled planar and `𝔅` is of the nested kind, then `A` or `B` has no position.

*Proof.*  Every node of `𝔅` other than the source has one parent in `𝔅`, the hybrid nodes two; so `𝔅` has
`|V(𝔅)| + 1` edges, i.e. two independent cycles.  Suppressing the nodes of degree two leaves a 2-connected
cubic multigraph with two independent cycles; it has two nodes and three edges, and these are parallel
(loops would give cut vertices).  An interior node of a path has its two path edges and a cut edge, or is
the root.  Both path edges enter it if it is a hybrid node, both leave it if it is the source, and
otherwise one enters and one leaves.  So along a path the direction changes exactly at hybrid nodes and at
the source.  A branch node is a hybrid node (two paths enter, one leaves) or a tree node (one enters, two
leave); it is not the source.

(1) *Both hybrid nodes interior, on different paths `P_1`, `P_2`.*  The cycle formed by `P_1` and the third
path contains no edge entering the hybrid node of `P_2`, and symmetrically: the galled kind.
(2) *Both interior on the same path.*  The direction must change between them, so the source lies between
them and the path leaves both branch nodes.  The other two paths contain neither a hybrid node nor the
source, so they are directed; each branch node is a tree node entered by exactly one of them; so one is
directed from the first branch node to the second and the other back: a directed cycle.  Impossible.
(3) *One hybrid node `h_1` at a branch node, the other, `h_2`, interior.*  Let `A`, `B` enter `h_1` and `C`
leave it.  If `h_2` is on `C` we have the nested kind: the part of `C` between `h_1` and `h_2` is directed
from `h_1` to `h_2` and contains no source (a source there would make its first edge enter `h_1`).  If `h_2`
is on `A`, the path `A` enters both `h_2` and `h_1`, so the source lies between them on `A`; then `B` is
directed from `t` to `h_1` and `C` from `h_1` to `t`: a directed cycle.  Impossible.
(4) *Both at the branch nodes.*  The path leaving `h_1` contains neither a hybrid node nor the source (a
source would make it enter `h_1`), so it enters `h_2`; likewise the path leaving `h_2` enters `h_1`; they
form a directed cycle.  Impossible.

*Planarity.*  In a planar embedding the theta graph has three faces, each bounded by two of the paths, and
one path is not on the boundary of the outer face.  A pendant subnetwork is connected, attached at one
node, and contains a leaf; if all leaves are on the outer face it lies there, so the path away from the
outer face has no position.  `C` has the position `h_2`.  ∎

**Positions of a nested blob in an outer-labeled planar network.**  Call `A` the path without positions.
The positions are `b_1,…,b_{k_B}` on `B`, counted from `h_1`; `x_1,…,x_{k_1}` on `C` between `h_1` and `h_2`,
counted from `h_1`; `y = h_2`; and `c_1,…,c_{k_2}` on `C` between `h_2` and `t`, counted from `h_2`.  Around the
outer face the pendant subnetworks appear, each as a block of consecutive leaves, in the order

```
b_1, …, b_{k_B},  c_{k_2}, …, c_1,  y,  x_{k_1}, …, x_1 .
```

Their sizes are denoted `β_j`, `γ_e`, `η`, `ξ_a`.  The bloblet `𝔅°` is called `N[k_B,k_1,k_2]`; it has four
switchings (at `h_1` keep the edge from `B` or the edge `A`; at `h_2` keep the edge from the `x`-side or from
the `c`-side), with the trees

```
T_1 (B, x-side):   caterpillar   c_1 … c_{k_2}   b_{k_B} … b_1   x_1 … x_{k_1}   y
T_2 (A, x-side):   three arms at t:    (b_1 … b_{k_B}),    (c_1 … c_{k_2}),    (y, x_{k_1} … x_1)
T_3 (B, c-side):   caterpillar   y   c_1 … c_{k_2}   b_{k_B} … b_1   x_1 … x_{k_1}
T_4 (A, c-side):   three arms at t:    (b_1 … b_{k_B}),    (y, c_1 … c_{k_2}),    (x_{k_1} … x_1)
```

(an arm is listed from its far end towards `t`; `level2_fourtrees_check.py` compares these trees with the
switchings of the explicit rooted network for all 155 bloblets with at most nine leaves).  `Σ[k_B,k_1,k_2]` is
the union of their split systems.  The
network `N*` of §6 is `N[4,1,1]`, and the bloblet version of `N(s,t)` is `N[s+t+1,1,1]`.  The restriction of
`Σ[k_B,k_1,k_2]` to a set of positions containing `y` is `Σ[k']` for the numbers `k'` of positions kept on the
three sides; a restriction without `y` has only two trees.  For `k_B ≤ 1` one has `T_1 = T_2` and `T_3 = T_4`.

The *critical split* `S*_𝔅` of a nested blob separates the leaves at the positions `x_1,…,x_{k_1}, y` from the
leaves at the positions `b_j` and `c_e`.  It is a split of `T_1` and of `T_2`, so it is displayed.

**Theorem 12 (outer-labeled planar networks of level at most 2) [P + X].**  Let `N` be a binary
semi-directed network of level at most 2 on `n ≥ 4` leaves, outer-labeled planar with circular order `C`.

(a) Every circular split that is not the critical split of a nested blob with `k_1 ≥ 1` and `k_B ≥ 2` has
weight `α ≥ 0`, with `α > 0` if and only if it is displayed.

(b) For a nested blob with `k_1 ≥ 1` and `k_B ≥ 2`,

```
α(S*)  =  β_1·G  +  ξ_1·R  −  Σ_{ j < l in M }  β_j β_l ,          R = η + ξ_2 + … + ξ_{k_1} ,
```

where `G = γ_1 + … + γ_{k_2}` and `M = {2, …, k_B}` if `k_2 ≥ 1`, and `G = β_{k_B}` and `M = {2, …, k_B − 1}` if
`k_2 = 0`.

(c) Consequently `d_N` is circular decomposable with support exactly `Split(T(N))` if and only if
`α(S*_𝔅) > 0` for every nested blob `𝔅` with `k_1 ≥ 1` and `k_B ≥ 2`; and `d_N` is Kalmanson for `C` if and
only if these numbers are `≥ 0`.  (The first property does not depend on a circular order: the split
metrics of the circular splits of `C` are linearly independent, so a metric that is a positive combination
of the splits of `Split(T(N))`, which are circular for `C`, has exactly these weights `α`.)

*Proof.*  Write `Σ = Split(T(N))`; by Lemma 1, `d_N = d_Σ`.

*Step 1: six leaves.*  We claim that for six leaves `Y` the restriction `Σ|_Y` is 6-locally good, **or** `Y`
meets six different positions of a nested blob — three `b`-positions, an `x`-position, `y` and a
`c`-position, or four `b`-positions, an `x`-position and `y` — and then `Σ|_Y` consists of all circular
splits of the six leaves except the 2-split formed by the second and third of the `b`-leaves; such a
system is globally good (one of the 141 of §7).
If some cut edge has at least two leaves of `Y` on each side, `Σ|_Y` is by Lemma D(i) and Lemma 7(ii) a
substitution of two tree-generated systems with at least three leaves each; there are 624 such
substitutions on six points and all are 6-locally good [X].  Otherwise direct every cut edge towards its
side with at least five leaves of `Y`.  The blobs (and the tree nodes outside the blobs) with the cut
edges form a tree, and a directed tree has a node `𝔅` all of whose edges point to it; each of its pendant
subnetworks contains at most one leaf of `Y`; so `𝔅` is not a leaf and not a tree node (three pendant
subnetworks), but a blob with at least six positions, and
`Σ|_Y = Σ(𝔅)|_Y` (Lemma D(ii)).  If `𝔅` has one hybrid node or is of the galled kind, `𝔅°` is an
outer-labeled planar network in which every hybrid node is adjacent to a leaf, so `Σ(𝔅) ∈ 𝒜` (Lemma A),
its restriction is in `𝒜_6` (Lemma 7(i)) and is 6-locally good (Lemma 8).  If `𝔅` is nested, `Σ|_Y` is a
six-point restriction of some `Σ[k']` with at most seven positions, and these were computed [X]: all are
6-locally good except `Σ[3,1,1]` and `Σ[4,1,0]`, which are as described.

*Step 2: which terms can be wrong.*  Let `S = U|V` be a non-trivial circular split with end leaves
`u_1,u_p,v_1,v_q`, and `z,w` two further leaves on one side, say in `U`; let `Σ_6` be the restriction of `Σ` to
these six leaves, in which `S` becomes the 2-split `{v_1,v_q}`.  If `Σ_6` is 6-locally good then `Φ6(z,w) ≥ 0`,
with equality if `S ∉ Σ`.  Otherwise `Σ_6` is all nine splits except one 2-split `D`.  By Corollary 5′,
`Φ6(z,w) < 0` iff `D = {z,w}`.  If `S ∉ Σ` then `{v_1,v_q} ∉ Σ_6` (Lemma 3), so `D = {v_1,v_q}`; as `Σ_6` is
globally good the weight of `D` in `d_{Σ_6}` is `0`, and by Proposition 2 this weight is
`2(Φ4 + Φ5(z) + Φ5(w) + Φ6(z,w))` with `Φ4 = Φ5(z) = Φ5(w) = 0`; so `Φ6(z,w) = 0`.

*Step 3: only the critical split.*  So a term `Φ6(z,w)` is negative only if the six leaves lie at
positions `b_i, b_j, b_l, c_e, y, x_a` or `b_i, b_j, b_l, b_m, y, x_a` of a nested blob (`i < j < l < m`), with `z`,
`w` at `b_j`, `b_l`; then `u_1` is at `b_i`, `u_p` at `c_e` (resp. `b_m`), and `v_1, v_q` at `y, x_a` (or the same with
the two directions of `C` exchanged).  The end leaves `u_p, v_1` are neighbours in `C`, and so are `v_q, u_1`;
since the pendant subnetworks are blocks of `C` in the order displayed above, this forces `e = 1` (resp.
`m = k_B` and `k_2 = 0`), `a = 1`, `i = 1`, and `U` is the set of all leaves at the `b`- and `c`-positions:
`S = S*_𝔅`.  For every other split all terms of Proposition 2 are `≥ 0` (the `Φ5` by Lemma 4), they all vanish
if the split is not displayed, and `Φ4 > 0` if it is (Lemma 3); trivial splits are positive by Lemma 4.
This is (a) — the negative terms need three `b`-positions, so nothing fails for `k_B ≤ 2` either, in
accordance with (b).

*Step 4: the weight of the critical split.*  Let `u_1` be the first leaf at `b_1`, `u_p` the last leaf at `c_1`
(at `b_{k_B}` if `k_2 = 0`), `v_1` the first leaf at `y`, `v_q` the last leaf at `x_1`; these four positions are
different.  A term of Proposition 2 for `S*` involves the four end leaves and one or two further leaves.
*Two further leaves at the same position `P`:* at most one end leaf is in `P`; for `a, b ∉ P` the cut edge of
`P` gives `w(zw|ab) = 1`; if an end leaf `e ∈ P`, the two terms of `Φ6` that contain `e` are `w(zw|e a)` and
`w(zw|e b)` with `a, b ∉ P`, they carry opposite signs, and they are equal because the quartets displayed on
`{z,w,e,o}` do not depend on the leaf `o ∉ P`; the other two terms are `+1` and `−1`.  So `Φ6(z,w) = 0`.  *Otherwise* every position is met at most
twice, and by Lemma D(iii) the term is a term of a system `Σ[k']` with at most six positions in which some
positions are replaced by cherries; it depends only on the *types* of the further leaves: at `b_1`, at `b_j`
with `j ∈ M`, at `c_1`, at `c_e` with `e ≥ 2`, at `b_{k_B}` (if `k_2 = 0`), at `y`, at `x_1`, at `x_a` with `a ≥ 2`.  The
values were computed for every type and every pair of types [X]:

```
Φ4 = 1;      Φ5 = 0 for a leaf at a position of M,     Φ5 = ½ for every other leaf;
Φ6 = −½  for two leaves at different positions of M;
Φ6 = +½  for a leaf at b_1 with a leaf at a c-position (at b_{k_B} if k_2 = 0),
         and for a leaf at x_1 with a leaf at y or at another x-position;
Φ6 = 0   for all other pairs of leaves at different positions.
```

In `U` there are `β_1 − 1` further leaves at `b_1` and `G − 1` at the `c`-positions (resp. at `b_{k_B}`); in `V`
there are `ξ_1 − 1` further leaves at `x_1` and `R − 1` elsewhere.  Hence

```
α(S*)/2 = 1 + ½[(β_1−1) + (G−1) + (β_1−1)(G−1)] + ½[(ξ_1−1) + (R−1) + (ξ_1−1)(R−1)] − ½ Σ_{j<l in M} β_j β_l
        = ½ β_1 G + ½ ξ_1 R − ½ Σ_{j<l in M} β_j β_l .
```

(c) follows from (a) and (b).  ∎

**Corollary 13 (level-2 bloblets) [P + X].**  An outer-labeled planar level-2 bloblet is galled — and then
satisfies the conclusion ([HABIMRW] Theorem 4.7) — or it is some `N[k_B,k_1,k_2]`.  For `k_1 ≥ 1`, `k_B ≥ 2` the
critical split of `N[k_B,k_1,k_2]` has weight

```
α(S*) = k_1 + k_2 − C(k_B − 1, 2)   if k_2 ≥ 1,            α(S*) = k_1 + 1 − C(k_B − 2, 2)   if k_2 = 0,
```

and `d_N` is circular decomposable with support `Split(T(N))` if and only if `k_1 = 0`, or `k_B ≤ 1`, or this
number is positive.  The smallest bloblets with a negative weight are `N[4,1,1] = N*` and `N[5,1,0]` (seven
leaves, weight `−1`); in `N[4,1,2]`, `N[4,2,1]`, `N[5,2,0]` (eight leaves) the weight is `0`: the metric is
Kalmanson but the displayed split `S*` is missing from its support.  Both formulas of Theorem 9(c) are
instances of Theorem 12(b): `N[s+t+1,1,1]` gives `2 − C(s+t,2)`, and three `b`-positions of sizes `1, t, s`
with `k_1 = k_2 = 1` give `2 − st`.  [X] The nine bloblets with at most nine leaves and a negative weight
are Kalmanson for no circular order.

**Corollary 14 (the robust form) [P + X].**  For an outer-labeled planar network `N` of level at most 2 the
following are equivalent.
(i) Every nested blob with `k_1 ≥ 1` has at most one position in `M`: `k_B ≤ 2`, or `k_B = 3` and `k_2 = 0`.
(ii) `Split(T(N)) ∈ 𝒦`.  (iii) `Split(T(N)) ∈ 𝒦′`.
(iv) `N` and every network obtained from `N` by replacing leaves by clades satisfy the conclusion (circular
decomposable, support the displayed splits).
(v) All these networks have a Kalmanson NANUQ metric.

*Proof.*  By Step 1 a six-point restriction that is not 6-locally good needs three `b`-positions and a
`c`-position, or four `b`-positions, of a nested blob with `k_1 ≥ 1`, and such positions exist exactly when
`M` has at least two elements; the two exceptional systems are not in `𝒦′_6` either.  So (i) ⇔ (ii) ⇔ (iii).
(ii) ⇒ (iv): `𝒦` is closed under replacing leaves by clades (Theorem 10(c)), and Theorem 4.  (iv) ⇒ (v) is
trivial.  (v) ⇒ (i): if `j, l ∈ M`, replace one leaf at `b_j` and one at `b_l` by clades of `m` leaves; the
new network is of the same kind, `β_1`, `G`, `ξ_1`, `R` are unchanged, and by Theorem 12(b) the critical weight
is `β_1G + ξ_1R − (β_j + m − 1)(β_l + m − 1) − …`, negative for large `m`.  ∎

**Remarks.**  1. *Why the middle positions.*  Take leaves `z, w` at two different `b`-positions together with
leaves at `b_1`, `c_1` (or `b_{k_B}`), `y`, `x_1`.  The three 3-splits of Corollary 5′ come from `T_2` (the arm of
the `b`-leaves) and from the two caterpillars `T_1`, `T_3`.  The 2-split `{z,w}` would need a tree in which `z`
and `w` form a cherry, and two `b`-leaves form a cherry only at the far end of the arm of `T_2`, `T_4` (one of
them at `b_1`) or, if `k_2 = 0`, at the end of the caterpillar `T_1` (one of them at `b_{k_B}`).  Leaves at one
and the same position form a clade and do not interact; that is why the sizes enter through the second
elementary symmetric function of the middle positions.
2. *Agreement with the survey of §6, Remark 3.*  With seven leaves the formula is negative only for the
bloblets `N[4,1,1]` and `N[5,1,0]`, and it vanishes when one position of `M` in `N[3,1,1]` or `N[4,1,0]` carries
a cherry: negative weights only in bloblets, wrong supports only outside bloblets — which is what the
enumeration of the referee of REV-0002 showed (664 and 1 252 insertion sequences).
3. *Scope.*  Theorem 12 is about level at most 2.  For higher levels the same method applies in principle
(by Step 1 of the proof, a six-leaf restriction that is not 6-locally good comes from six positions of
one blob, for any network), but the blobs that are not galled have not been listed.
4. *Evidence.*  `level2_classification.py`: the two finite facts of Step 1 (624 substitutions; 16 555
six-point restrictions of the systems `Σ[k]` with at most ten leaves), the table of Step 4 with the check
that the type determines the value, all 445 bloblets with at most 13 leaves, 1 500 random systems glued
from nested blobs, trees and systems of `𝒞` (1 045 critical splits, 97 with weight `≤ 0`), and the search
over circular orders.  `level2_explicit.py` does not use the four trees above: it builds **explicit rooted
networks** with nested blobs entered through the root or through a cut edge, level-1 cycles and trees as
pendant subnetworks, and computes the metric from the switchings with `netcalc.py`: 920 networks with
at most 12 leaves (194 with several blobs), 571 critical splits (190 with weight `≤ 0`), about 27 500
other splits: no deviation from Theorem 12.

---

## 8. The parametric family of quartet distances (problem B3)

Allman, Baños, Rhodes and Wicke (NANUQ⁺, Algorithms Mol. Biol. 2025, Def. 3.1; read in the published HTML
version) define, for `ρ = (ρ_c, ρ_s, ρ_a, ρ_o) ∈ (ℝ_{≥0})^4`,
`d_ρ(x,y) = 2 Σ_{z,w} ρ_xy(Q_xyzw) + 2n − 4`, where `ρ_xy` is `ρ_c` if the quarnet is a tree with cherry `xy`,
`ρ_s` if it is a tree separating `x` from `y`, `ρ_a` if it has a 4-cycle with `x,y` adjacent, `ρ_o` if it has a
4-cycle with `x,y` opposite.  NANUQ is `(0, 1, ½, 1)`; their *Modified NANUQ* distance is `(½, 1, ½, 1)`.
[HABIMRW] §6 asks "whether some of our results can be extended to a parametric family of distances, as
introduced in [All+25a]".  NANUQ⁺ defines the family for level-1 networks, where a quarnet is a tree or has
a 4-cycle.  **Beyond level 1 we have to choose an extension, and the choice is ours**: for a quarnet of an
outer-labeled planar network we read "4-cycle" as "both planar quartets are displayed" and "tree" as "one
is" — the reading under which `(0,1,½,1)` is the NANUQ metric of [HABIMRW] Def. 4.1.  Theorem 11 is a theorem
about this extension.

**Theorem 11 [P + X].**  Let `ρ ∈ (ℝ_{≥0})^4`.

(a) `d_ρ` is circular decomposable, for the induced circular order, with support exactly `Split(T(N))`, for
**every** binary semi-directed outer-labeled planar galled network `N` (all levels, any number of blobs)
**if and only if**

```
ρ_o = ρ_s     and     ρ_c + ρ_s ≤ 2 ρ_a < 2 ρ_s .
```

(b) The same holds for every such network **whose hybrid nodes all have a leaf child** (class 𝒜; it
contains all bloblets) if and only if  `ρ_o = ρ_s`,  `ρ_c ≤ ρ_a`  and  `ρ_s ≤ 2ρ_a < 2ρ_s`.

(c) NANUQ satisfies (a), on its boundary (`ρ_c + ρ_s = 2ρ_a`).  Modified NANUQ satisfies (b), on two of
its boundary faces (`ρ_c = ρ_a` and `ρ_s = 2ρ_a`), but **not** (a).  Smallest witness we know (found by the
referee of REV-0004, recomputed in `modified_nanuq_witness7.py` from the explicit rooted network): the
level-1 network on **seven** leaves consisting of a 6-cycle — the hybrid node and five tree nodes with one
leaf each — and a cherry below the hybrid node; the Modified NANUQ distance gives the displayed split
"hybrid cherry | rest" the weight `−1` and is Kalmanson for none of the 360 circular orders.  Our first
witness (`modified_nanuq_witness.py`) has eight leaves: a 5-cycle whose hybrid node has a cherry below it,
with cherries at **the two cycle positions that are not adjacent to the hybrid node**; weight `−2`, Kalmanson
for none of the 2520 circular orders.  (The previous version said "at two of its other four positions",
which was ambiguous: for the other five placements of two cherries the Modified NANUQ distance satisfies
the full conclusion.)  This contradicts nothing published: the authors of NANUQ⁺ state that they make no
claim on whether distances other than NANUQ fit a combinatorial structure in a precise sense
(`PRIOR_ART.md` B-VI).

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
* The non-galled planar networks for which the conclusion survives are classified for level 2 only
  (Theorem 12); for level 3 and above the blobs that are not galled have not been listed.  Theorem 12 says
  nothing about circular orders other than the planar one when a critical weight is negative (checked only
  for the bloblets with at most nine leaves).
* For "Kalmanson" without exact support the sharp class is `𝒦′` (Theorem 10′, §7.1) — for classes closed
  under restriction and cherry replacement; nothing is shown about a single system outside `𝒦′` (§7.1,
  Remark 3), and the six-leaf outer-labeled planar networks that display the forbidden pattern are not
  described in terms of the network (number of hybrids, their positions).
* For the class of bloblets alone the exact parameter domain is not determined (condition (b) of Theorem 11
  is sufficient; our necessity witnesses use pendant clades).
* Theorem 7 was reached independently, but after a third-party claim of the same statement whose method
  probably coincides with ours (§0).
* The proofs are paper proofs by this division with two internal adversarial reviews (REV-0002; REV-0004 for
  Lemma 0, Lemma B0, Lemma B, Theorem 9(c) and Theorem 11), which are not academic peer review.  Theorem 11
  rests on a computed table of local forms that no kernel checks (the second referee reproduced the table
  and checked 2 971 networks on the extreme rays of both parameter domains).  Corollary 5′, §7.1 and §7.2
  were written after both reviews.

## 10. Reproduction

Our programs: `experiments/complexity/nanuq/` (Python 3 + `networkx`).

| program | what it establishes | time |
|---|---|---|
| `five_point_facts.py` | Lemma 4 | seconds |
| `check_decomposition.py` | Proposition 2 (identity), non-negativity of all local terms on network systems with ≤ 7 leaves | minutes |
| `verify_class.py` | Lemma 8: `𝒜_n`, `𝒞_n` for `n ≤ 6`; agreement with a second generator (`multiblob.py`) | ≈ 1 min |
| `class_table6.py` | Appendix B | seconds |
| `characterize6.py` | the numbers 150 / 141 / 127 / 108, Theorem 10 | ≈ 2 min |
| `level2_nongalled.py`, `level2_failures.py` | the family `N[k_B,k_1,k_2]` from its four trees; tables of pattern-freeness and of failing splits | minutes |
| `level2_classification.py 13 1500 7` | Theorem 12: the finite facts of Step 1, the table of Step 4, all bloblets with at most 13 leaves, 1 500 random glued systems, no circular order for the failing bloblets with at most 9 leaves (log: `level2_classification_big.log`) | ≈ 1 min |
| `level2_explicit.py N seed maxleaves` | Theorem 12 on **explicit rooted networks** (only `netcalc.py`; independent of the four trees and of Lemmas C, D); logs for `120 1 10`, `400 2 12`, `400 3 11` | minutes |
| `level2_fourtrees_check.py` | the four trees of §7.2 are the trees displayed by the explicit network, 155 bloblets | seconds |
| `kalmanson_only.py`, `kalmanson_only.py extra`, `forbidden_in_nstar.py` | Corollary 5′ on all six-point systems; Theorem 10′(d): 133 = 127 + 6, the 17 excluded systems, the formula of (c) for `m ≤ 6`, no circular order for the least failing blow-ups; the pattern in `N*` | seconds |
| `test_bloblets.py k n…`, `test_multiblob.py n` | the conclusion of Theorem 7 on all bloblets of level `k` / all networks with `n` leaves, **as generated from twin trees and substitution** | minutes |
| `counterexample7.py`, `verify_nongalled.py`, `verify_nongalled2.py`, `nongalled_family.py`, `nongalled_formula.py` | Theorem 9 | seconds–minutes |
| `exhaust_all_systems.py`, `exhaust_tree_generated.py` | CX-D2 | seconds |
| `parametric_theorem.py` | Theorem 11(a): parametric decomposition identity, local forms on `𝒞_{≤6}`, witnesses | ≈ 2 min |
| `parametric_classA.py`, `parametric_witnesses_A.py`, `parametric_o_gt_s_witness.py` | Theorem 11(b): local forms on `𝒜_{≤6}`, witnesses with non-hybrid `z,w` | minutes |
| `modified_nanuq_witness.py`, `modified_nanuq_witness7.py` | Theorem 11(c), from explicit rooted networks: the eight-leaf and the seven-leaf witness; the six placements of two cherries | seconds |
| `export_lean_lists.py` | the list `C6` in the Lean file is the computed closure | ≈ 30 s |

**Which tests are independent of the structure lemmas** (REV-0002, finding 1).  `test_bloblets.py` and
`test_multiblob.py` build their networks from the twin-tree and substitution description, so they
presuppose Lemmas A and B and test only the split-system part of Theorem 7.  Tests of Theorem 7 that start
from **explicit rooted networks** — generated by inserting hybrid edges into trees and filtered by the
definitions themselves (Def. 2.3(vi) for "galled", a planarity test, the LSA condition) — were written by
the referee with code that shares nothing with ours and are kept in
`experiments/complexity/reviews/rev2_nanuq/`:

| referee's program | what it does | result reported in REV-0002 |
|---|---|---|
| `t3b_random.py`, `t3b_random_big.py` | random galled outer-labeled planar networks, 6–13 leaves, levels 1–8 | 74 661 distinct networks, no failure of Theorem 7 |
| `t_exhaust.py n k` | all networks from all tree shapes on `n` leaves by `≤ k` hybrid insertions | 4 leaves `k ≤ 3`, 5 leaves `k ≤ 3`, 6 and 7 leaves `k ≤ 2`: no failure |
| `t_lemmaAB.py` | Lemmas A, B, 7(iii) on explicit networks | 1 422 762 six-leaf restrictions all in `𝒞_6`; substitution identity on 4000 cuts |
| `t3a_nstar.py`, `t9c_family.py`, `t_exhaust_ng.py` | `N*`, the family, non-galled survey | Theorem 9 confirmed |
| `t3c_counts.py`, `t3d_blowups.py`, `t_extra.py` | counts 16 / 150 / 141 / 127 / 108, blow-ups, 7-point systems | Theorem 10 confirmed as stated |
| `t_anchor.py`, `t1_defs.py`, `quarnet.py` | the five NANUQ matrices of Table 1 of [HABIMRW]; a literal implementation of Def. 2.5 | external anchor reproduced; 0 mismatches on 9 155 four-sets |

We re-ran `t_exhaust.py 5 2` and a 300-network batch of `t3b_random.py` from the repository copy
(2026-11-26): no failure.

Lean: `experiments/complexity/lean/NanuqFinite.lean` (`lake env lean …`, about 3.5 minutes): Lemma 4;
Proposition 2 on all tree-generated systems on five and six points; 150 / 141 / 127; "6-locally good ⇒
Kalmanson with exact support" on six points; doubled five-point systems are 6-locally good (Theorem 10(c));
all 108 systems of the list `C6` are 6-locally good.  Axioms: `propext`, `Quot.sound`.

## 11. Changes after the review COMPLEXITY-REV-0002

| finding | change |
|---|---|
| 1 (major): the direct tests of Theorem 7 presuppose its structure lemmas | §10 says so; the referee's explicit-network tests are in the repository and listed |
| 2 (major): the method probably coincides with the earlier third-party claim (122 systems) | §0 item 2, §9, `PRIOR_ART.md` B-II, `THEOREMS.md` |
| 3: Lemma 1 cited a notation as if it were a statement | Lemma 0 with proof; Lemma 1 rewritten |
| 4, 5: "marked networks" undefined; pieces with 2 or 3 leaves; wrong remark on rooted partners | classes and substitution defined for `n ≥ 2`; Lemma B states and proves that the pieces are networks of the class; induction of Theorem 7 restated |
| 6: the cut-edge fact rested on an unproved remark of the source | Lemma B0 (the referee's proof) |
| 7: a sentence in the proof of Proposition 6 was empty for adjacent leaves | sentence replaced |
| 8: "all displayed trees … one planar tree" only true in class 𝒜; "so does the theorem" too strong | paragraph after Proposition 6 rewritten |
| 9: `st` vs `C(s+t,2)`; "tending to −∞" unproved | Theorem 9(c) with exact formulas for both versions and a proof (`nongalled_formula.py`) |
| 10: "sharp" needs a qualifier | paragraph "What 'sharp' does and does not mean" in §7; §0 item 4 |
| 11: the failure is specific to the multiplicity-free metric; minimality; survey | §6 Remarks 1–3; §0 item 3 |
| 12: print the classes of `𝒞_6` | Appendix B (`class_table6.py`); kernel check of the same fact in Lean |
| 13: undefined labels, numbering, no bibliography | labels and numbering note in §0; "Theorem 6′" renamed; §12 |
| 14: the reading of "4-cycle" above level 1 is ours | stated in §8 |

**Changes after the review COMPLEXITY-REV-0004** (Lemma 0, Lemma B0, Lemma B, Theorem 9(c), Theorem 11):

| finding | change |
|---|---|
| 9 (major by the referee's rubric; the statement is true): the proof of Lemma 0 assumed that the union of up-down paths has a single source | proof completed with the referee's argument (the paragraph "`U` has exactly one node without an entering edge") |
| 10: the witness of Theorem 11(c) was described ambiguously; a smaller one exists | Theorem 11(c) rewritten: seven-leaf witness (`modified_nanuq_witness7.py`), the placement of the cherries stated, the disclaimer of NANUQ⁺ quoted |
| 11: `nongalled_formula.py` takes the trees of the family by formula | said so in §6; explicit-network checks listed |
| 12: sizes of the pieces in Lemma B | numbers added to the remark after Lemma B |

Added later on 2026-11-26 and not seen by the referee of REV-0002: Corollary 5′ (§3) and §7.1 (Theorem 10′),
which settle the question left open in finding 10 ("for Kalmanson alone the criterion is not known to be
sharp") by replacing the class; and §7.2 (Lemmas C, D, Theorem 12, Corollaries 13, 14), which classifies the
outer-labeled planar networks of level at most 2 and so answers, for level 2, the question left open in
§6, Remark 3.  The referee of REV-0004 saw an uncommitted draft of Corollary 5′ and Theorem 10′ and reports
incidental checks only (Corollary 5′ on 150 × 12 labellings; the formula of Theorem 10′(c) on 68 values).

## 12. References

* [HABIMRW] N. Holtgrefe, E. S. Allman, H. Baños, L. van Iersel, V. Moulton, J. A. Rhodes, K. Wicke,
  *Distinguishing Phylogenetic Level-2 Networks with Quartets and Inter-Taxon Quartet Distances*, Bull. Math.
  Biol. (2025), doi:10.1007/s11538-025-01549-4; arXiv:2507.17308v2 (read in full).
* [All+25a] E. S. Allman, H. Baños, J. A. Rhodes, K. Wicke, *NANUQ⁺: A divide-and-conquer approach to network
  estimation*, Algorithms Mol. Biol. 20:14 (2025) (the section on quartet distances read).
* [ABR19] E. S. Allman, H. Baños, J. A. Rhodes, *NANUQ: a method for inferring species networks from gene
  trees under the coalescent model*, Algorithms Mol. Biol. 14 (2019) (not read; known through [HABIMRW]).
* V. Chepoi, B. Fichet, *A note on circular decomposable metrics*, Geom. Dedicata 69 (1998) (not read; used
  through [HABIMRW] Prop. 2.8).
* Third-party entry "All-level NANUQ circularity and exact displayed-split support", vibemathed.com,
  submitted 2026-09-30 (public summary read; the linked repository not inspected) — `PRIOR_ART.md` B-II.
* COMPLEXITY-REV-0002, internal adversarial review of this note
  (`docs/collaboration/messages/complexity/`).

## Appendix B.  The 17 classes of `𝒞_6`

Leaves `1,…,6` in circular order.  A representative of each class under rotation and reflection, given by
its non-trivial splits (the side not containing leaf 1).  The last two columns give the values of `2Φ6` in
the twelve dihedral placements `(y_1,…,y_6)`, according to whether `y_1y_4|y_5y_6` is displayed; the
six-point condition is that no value is negative and that the last column contains only zeros.
(`class_table6.py`.)

| # | non-trivial splits | class size | in 𝒜 | 2Φ6, split displayed | 2Φ6, split not displayed |
|---|---|---|---|---|---|
| 1 | 23 234 2345 | 6 | yes | 0 (×4) | 0 (×8) |
| 2 | 23 56 234 | 6 | yes | 0 (×4) | 0 (×8) |
| 3 | 23 45 2345 | 2 | yes | 2 (×6) | 0 (×6) |
| 4 | 23 34 234 2345 | 12 | yes | 0 (×6) | 0 (×6) |
| 5 | 23 45 234 2345 | 6 | yes | 1 (×6) | 0 (×6) |
| 6 | 23 56 234 456 | 3 | yes | 0 (×4) | 0 (×8) |
| 7 | 23 34 45 234 2345 | 12 | yes | 0 (×2), 1 (×6) | 0 (×4) |
| 8 | 23 34 234 345 2345 | 12 | yes | 0 (×6) | 0 (×6) |
| 9 | 23 34 56 234 2345 | 3 | yes | 0 (×8) | 0 (×4) |
| 10 | 23 45 234 345 2345 | 6 | no | 0 (×6) | 0 (×6) |
| 11 | 23 34 45 234 345 2345 | 6 | yes | 0 (×6), 1 (×2) | 0 (×4) |
| 12 | 23 34 45 56 234 2345 | 6 | yes | 0 (×4), 1 (×6) | 0 (×2) |
| 13 | 23 34 45 56 234 456 | 6 | yes | 0 (×8) | 0 (×4) |
| 14 | 23 34 56 234 345 2345 | 6 | yes | 0 (×8) | 0 (×4) |
| 15 | 23 34 45 56 234 345 2345 | 12 | yes | 0 (×8), 1 (×2) | 0 (×2) |
| 16 | 23 34 45 56 234 345 2345 3456 | 3 | yes | 0 (×8), 1 (×4) | — |
| 17 | 23 34 45 56 234 345 456 2345 3456 | 1 | yes | 0 (×12) | — |
