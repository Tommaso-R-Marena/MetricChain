## 1. The statements, with every hypothesis that the text leaves implicit

Throughout: `G = (V, E)` a graph on `N` vertices, `d ≥ 1`, configuration space `C = (ℝ^d)^N` **with no constraint**
(any `N` points), `F = m_{d,G} : C → ℝ^E` the squared edge lengths, congruence = the full Euclidean group
**including reflections**, acting on each configuration separately.  An *ensemble* is a Borel probability measure
on `C`.

**E5 (lines 363–393), as it has to be read.**  `F : ℝ^D → ℝ^m` polynomial with coefficients in a subfield
`k ⊆ ℝ`; points are real; `V` is the real Zariski closure of `F(ℝ^D)` (irreducible, of dimension `r([m])`, ideal
= kernel of `y_e ↦ F_e`, generated over `k`); `r(J)` = generic rank of the Jacobian of `F_J`.
(a) If the algebraic matroid is connected then for each `K ≥ 2` there is a proper algebraic `B_K ⊂ (ℝ^D)^K`,
defined over `k`, such that for a `K`-tuple outside `B_K` no splice with a non-constant colouring lies in `V`
(a fortiori none is the feature vector of a configuration).  "Generic tuple" = outside `B_K`: a condition on the
**tuple**, not on each point.  `B_K` is in general non-empty and contains real tuples whose splices are realised
(§2, M2).  (b) If `J` is a separator: `V = V_J × V_{J^c}`, all two-point splices along `(J, J^c)` lie in `V`, and
they are realised by configurations for an open non-empty set of pairs (not for all pairs: "in `V`" and "in
`F(ℝ^D)`" differ — triangle inequalities).  The hypothesis "no `F_e` constant" is not needed in (a) for
`m ≥ 2` (a constant coordinate is a loop, and a matroid with a loop on at least two elements is not connected);
its role is in (b) and in E6: with a constant coordinate the splice along that coordinate *is* a conformer's
feature vector, a "chimera" in the letter of the definition (line 360–361) that changes nothing.
*Smallest examples* (item (iv) of the brief) **[P, by hand]**: connected side — `D = 1`, `m = 2`, `F(x) = (x, x²)`:
matroid `U_{1,2}`, `V` the parabola, the splice `(x_1, x_2²)` lies on `V` iff `x_2 = ±x_1`, so `B_2 = {x_1² = x_2²}`;
for frameworks, three points on a line (`K_3`, `d = 1`, `N = 3 = d + 2`).  Disconnected side — `D = m = 2`,
`F(x, y) = (x, y)`: every splice is realised; for frameworks, the path with two edges on a line, or the triangle
in the plane (their example, lines 458–461, checked by hand).  Loop — `F(x) = (x, 1)`: not connected, and every
finite ensemble is nevertheless determined by its coordinate laws: this is why constant coordinates are excluded.

**E6 (lines 402–415).**  Conclusion at the level of *feature vectors*: `F_#ν = F_#μ` for every Borel `ν` with the
same coordinate laws.  Exceptional set `B'_K = B_K ∪ ⋃ {F_e(x_i) = F_e(x_j)}`: **no two conformers may share the value
of any feature.**  The weights enter in the last line only, through any one feature (its `K` atoms are distinct).

**E7 (lines 438–451).**  Implicit, in the order in which they matter:
1. *The base space is the free space `C`.*  Both `μ` and the competitor `ν` live on `(ℝ^d)^N`; no bond length, no
   bond angle is prescribed.
2. *"Generic" is joint* (lines 434–436): all `dNK` coordinates of the tuple algebraically independent over `ℚ`.
   This is strictly stronger than "each conformer is a generic framework", and the conclusion **fails** for
   tuples of individually generic conformers (M2).  It can be weakened to "outside a proper algebraic subset of
   `C^K`" (the proof uses only: outside `B'_K`, and each `x_i` globally rigid; for a generically globally rigid
   graph the globally rigid frameworks contain a Zariski-open set — Gortler–Healy–Thurston, Corollary 1.15, as
   returned by the fetch tool), so (b) holds on an open dense set of tuples of full measure.
3. *`N ≥ d + 2`* is needed for the cited theorem only; (b) ⇒ (a) is the case `K = 1` and uses nothing.
4. *"Determined modulo congruence"* means: `ν(⋃_i [x_i]) = 1` and `ν([x_i]) = w_i`.  Each conformer is determined
   up to its *own* congruence, reflection included: no relative orientation, and no handedness of any conformer.
5. *Conformers are pairwise non-congruent* (forced by joint genericity; congruent conformers can simply be merged).
6. *The laws are exact* and each is purely atomic with `K` atoms of masses `w_1, …, w_K`; `ν` is arbitrary (not
   assumed finite) — "among all ensembles" quantifies over `ν`, never over `μ`.
7. *`μ` consists of point conformers.*  A conformer that is itself a distribution, however narrow, is outside the
   statement (and Proposition E8.1 goes the other way).
8. (a) is "every generic framework is globally rigid"; by the cited theorem of Gortler–Healy–Thurston this is
   equivalent to "some".  The same theorem gives more than E7 states: **if `G` is not generically globally rigid
   then no generic finite ensemble at all is determined** (replace `x_1` by a non-congruent equivalent framework,
   which exists for *every* generic `x_1`).  So the dichotomy is complete.

**E8 (lines 463–482).**  Moments of orders `j = 1, …, 2K` of the *squared* length `t_e = ℓ_e²`, i.e. `E ℓ_e²`, …,
`E ℓ_e^{4K}`, exactly, for every edge; `ν` must have them finite; `μ` generic in the sense of E7.  "Determine"
includes the weights: once `ν` is carried by the `K` atoms of an edge, the moments of orders `1, …, K − 1` of
that one edge fix them (Vandermonde).  The mean of the certificate `f` does not depend on the weights at all.

**E1.3 (lines 159–172).**  (a) on `ℝ^D`, among ensembles with finite second moments.  (b) on the free space
`C = (ℝ^d)^N`; the competitor is the law of `R·p` with `R² ∈ {0, 2}`: with probability ½ all points coincide,
with probability ½ the configuration is inflated by `√2`.  The argument needs no mixture (it applies to a single
conformation) and no property of the graph.  The coordinator's guess is the general mechanism: for random
matrices `A` independent of `p` with `E[AAᵀ] = I`, the law of `pA` (points as rows) has the mean squared length
of every pair of `μ`; theirs is `A = R·I`.

## 2. Findings

Classes: **critical** = a statement is false or its proof has a gap; **major** = a statement or its reading needs
a changed hypothesis or a substantial qualification; **minor** = wording, redundancy, labels.

### No critical finding

E5, E6, E7, E8 and E1.3 are **proved as stated in the report**, with its definition of "generic" (lines 434–436)
— *review*: every step re-derived (§1; the notes of the re-derivation are in `NOTES.md`).  The two cited theorems
exist and are quoted correctly: Garamvölgyi–Gortler–Jordán, Theorem 3.5 — as returned by the fetch tool: "Let
G=(V,E) be a globally rigid graph in ℝ^d on n≥d+2 vertices. Then G is ℛ_d-connected." — with the cases `d ≤ 2`
attributed there to Jackson–Jordán 2005; Gortler–Healy–Thurston, Corollary 1.15: "Either all generic frameworks
in C^d(Γ) of a graph are globally rigid, or none of them are."  Their hypotheses are met: same definition of
generic, same definition of the graph property, `n ≥ d + 2`, and the algebraic matroid of the squared-length map
is the generic rigidity matroid (the Jacobian is twice the rigidity matrix).

### M1 (major) — the reading of E1.3: true on the free configuration space only; reversed for chains

*Where.*  Lines 174–177 ("they cannot even certify that the ensemble is a single conformation"), 487–488 ("`j = 1`
alone (mean squared lengths) identifies nothing"); `ENSEMBLE-MSG-0002` lines 47–48 and 118–119 ("mean squared
distances determine nothing").
*What decides it.*  The competitor of the proof (line 165–166) collapses the molecule to a point or inflates it
by `√2`.  That is an ensemble on `(ℝ^d)^N`, not an ensemble of anything with one known length.  As soon as lengths
are prescribed — every object of this programme — the statement is false:

**Proposition A [P; numerically checked, §3 T6].**  Let `B` be a set of pairs with prescribed lengths,
`X_B = {p : |p_u − p_v| = L_uv for uv ∈ B}`, and let `x ∈ X_B` span `ℝ^d` affinely.
(i) If the directions `x_u − x_v`, `uv ∈ B`, do not lie on a conic at infinity (no symmetric `S ≠ 0` with
`(x_u − x_v)ᵀ S (x_u − x_v) = 0` on `B`), then `δ_x` is determined modulo congruence, **among all ensembles on
`X_B`** (with finite mean squared distances), by the mean squared distances of all pairs.
(ii) If they do, there is a two-conformer ensemble on `X_B`, not congruent to `δ_x`, with the same mean squared
distance of every pair.  (`B = ∅` is E1.3(b).)
*Proof.*  (i) The centred Gram matrix `Γ(p) = p_c p_cᵀ ⪰ 0` is a linear function of the squared distances of all
pairs, so `E_ν Γ(p) = Γ(x)`.  For `z ∈ ker Γ(x)`: `E_ν zᵀΓ(p)z = 0`, hence `p_cᵀz = 0` `ν`-a.s.; so the columns of
`p_c` lie in those of `x_c`, i.e. `p_c = x_c A` with `A ∈ ℝ^{d×d}`.  On `B`:
`L_uv² = (x_u − x_v) AAᵀ (x_u − x_v)ᵀ = (x_u − x_v)(x_u − x_v)ᵀ`, so `AAᵀ − I` vanishes on the `B`-directions, hence
`AAᵀ = I` and `p ≅ x`.  (ii) Scale `S` so that `I ± S ≻ 0`, put `p^± = x (I ± S)^{1/2}`.  For every pair,
`|p^±_u − p^±_v|² = |x_u − x_v|² ± (x_u − x_v) S (x_u − x_v)ᵀ`: unchanged on `B`, so `p^± ∈ X_B`; the mean over
`½δ_{p^+} + ½δ_{p^−}` is that of `x`; and `p^± ≇ x` because a quadratic form that vanishes on all pair
directions of an affinely spanning configuration is zero.  ∎

So a chain with at least three pairwise non-parallel bonds in the plane, or six bonds in general directions in
space, in **any** such conformation, *is* determined by its mean squared distances among all ensembles of chains
with those bond lengths.  The exposing function is `‖P^⊥ b(p)‖²` (`b` the bond vectors, `P` the projector on the
column space of `b(x)`), the `d ≥ 1` version of their own certificate `‖P^⊥x‖²` of Theorem E10; for unit bonds on
a line the mean squared distances *are* the pair correlations of their Part III (`b_u b_v` is a linear
combination of four squared distances).  Part III and the sentence "mean squared distances determine nothing"
cannot both be read in the programme's setting.  For two generic chain conformers the same computation reduces
identification of the support to a finite algebraic question (which chains are of the form `x_1A_1 + x_2A_2`).
Numerically (§3, T6(d); 12 random pairs per bond count) **[N]**: with four to six bonds the pair is *not*
determined (an explicit second ensemble exists), from seven bonds on it is; for at least nine bonds this is a
proof given a rank that the script computes.
A second, smaller point: for a `K`-conformer ensemble the mean squared distances are the squared distances of
the *single* configuration `z = (√w_1 x_1, …, √w_K x_K) ∈ (ℝ^{dK})^N` **[P, one line]**; so, for all pairs and among
`K`-conformer ensembles, they determine exactly `z` up to congruence in `ℝ^{dK}` — the ensemble up to the action
of `O(dK)`, which mixes the conformers, and up to the weights (which are absorbed in the scale of the blocks of
`z`).  That, not "nothing", is their content on the free space;
and a mean Gram matrix of rank larger than `d` certifies that the ensemble is *not* one conformation, so "nothing
about fluctuations" (line 174) is too strong as well.
*Replacement text* (lines 161–166 and 174–177): "(b) Let `G` be any graph.  **On the free configuration space
`(ℝ^d)^N`, where no length is prescribed,** no ensemble with a non-degenerate conformer is determined modulo
congruence by its mean squared edge lengths […].  The hypothesis matters: on the configurations with prescribed
lengths on a set of pairs whose directions do not lie on a conic at infinity, every affinely spanning
conformation is determined by the mean squared distances of all pairs (R21, Proposition A), and for unit bonds
on a line these data are the pair correlations of Part III."  Lines 487–488: "identifies no ensemble on the free
configuration space".  Message: delete "determine nothing".

### M2 (major) — "generic ensemble" means *jointly* generic; for individually generic conformers the conclusion is false, also on globally rigid graphs with conformers that share a rigid part

*Where.*  `ENSEMBLE-MSG-0002` lines 59–62 and the summary line 30 ("every generic finite ensemble of frameworks");
Reading, lines 453–458; §5 item 4 (lines 716–721); §8, lines 745–747.
*What decides it.*  Two explicit ensembles (both *replicated*, §3 T3):

**Example D1 [P, exact arithmetic].**  `G = K_4` in the plane (globally rigid, `N = d + 2`).  With vertices
`0, 1, 2, 3`:
`x_1 = ((½, 2), (3, 3), (−1, 0), (1, 0))`, `x_2 = ((½, 3/2), (3/2, −4), (−2, 0), (2, 0))`,
`y = ((½, 2), (3, −3), (−1, 0), (1, 0))`, `y' = ((½, 3/2), (3/2, 4), (−2, 0), (2, 0))`.
Squared lengths on the edges `01, 02, 03, 12, 13, 23`:
`x_1`: `29/4, 25/4, 17/4, 25, 13, 4`;  `x_2`: `125/4, 17/2, 9/2, 113/4, 65/4, 16`;
`y`: `125/4, 25/4, 17/4, 25, 13, 4`;  `y'`: `29/4, 17/2, 9/2, 113/4, 65/4, 16`.
`x_1` and `x_2` have **no edge length in common**, each is a globally rigid framework, and `½δ_{x_1} + ½δ_{x_2}`,
`½δ_y + ½δ_{y'}` have the same law on every edge and are different modulo congruence.  The mechanism: `y` is `x_1`
with vertex `1` reflected in the line `23`, `y'` is `x_2` reflected likewise, and the two "kites" were chosen
with the same pair of values `{29/4, 125/4}` of the sixth length.  The pairs with this property form a family
with `5 + 3` free shape parameters and two relations (`y_1 y_2 = y_1'y_2'`,
`Δx² + y_1² + y_2² = Δx'² + y_1'² + y_2'²` in the coordinates of `NOTES.md`), i.e. of **codimension 2** in the space
of pairs, and it contains pairs in which *each* conformer has algebraically independent coordinates: the field
generated by the coordinates of the second kite contains three free parameters and the two constants
`y_1y_2`, `Δx² + y_1² + y_2²` of the first, which are algebraically independent.  So "each conformer generic" does
not suffice, even with all lengths distinct.
**Example D2 [P; replicated].**  `G = K_5 − e` (missing edge `34`; generically globally rigid, rigidity matroid
connected — `T1`), conformers `x_1 = (T, P_3, P_4)`, `x_2 = (T, P_3', P_4')` that share the triangle `T` on the
vertices `0, 1, 2`.  Then `y = (T, P_3, P_4')`, `y' = (T, P_3', P_4)` are frameworks all of whose measured lengths
are lengths of `x_1` or of `x_2`, and `½δ_{x_1} + ½δ_{x_2}`, `½δ_y + ½δ_{y'}` have the same edge-length laws.  Each
of `x_1`, `x_2` may be a generic framework.  With the edge `34` measured (`K_5`) there is no chimera.
In words: the laws of the distances from a rigid core to each of two mobile groups never tell whether the two
motions are correlated; only a measured distance between the mobile groups does.  **Generic global rigidity of
the graph is therefore not the criterion for conformers that share rigid parts** — the case §8 calls typical.
*Replacement text.*  Message and summary: "every finite ensemble whose conformers are **jointly** generic (all
`dNK` coordinates algebraically independent over `ℚ`; in particular no two conformers have an edge length in
common) is determined […].  For ensembles of individually generic conformers the conclusion can fail, on `K_4`
with no common length (codimension 2) and on the globally rigid graph `K_5 − e` when two conformers share a
triangle."  §8, lines 745–747: "[…] are not generic, and for them the conclusion can fail even on generically
globally rigid graphs (R21, Example D2).  No criterion is proved here; that a contraction of the rigidity matroid
decides is Problem O3, a question."  §5 item 4: see m8.

### M3 (major) — exactness: no modulus is stated, and the margins are tiny (numbers in §3)

*Where.*  Lines 438–446 and 463–475; §8 lines 739–740 lists "exact data" without a number; Problem O4.
*What decides it.*  (i) **Laws with a band.**  An elementary stability statement holds, and shows which quantity
governs it:

**Proposition B [P].**  Let `μ = Σ w_i δ_{x_i}`, `t_{e,i} = F_e(x_i)`, and let the *chimera gap* `g_∞` be the least
sup-norm distance from a splice that is not a conformer's vector to `F(C)`.  Let `ν` be any ensemble such that,
for every edge, the law of `F_e` under `ν` gives mass at least `1 − η_e` to the `τ`-neighbourhood of the atoms
`{t_{e,i}}_i`.  If `τ < g_∞`, then `ν{y : ‖F(y) − F(x_i)‖_∞ ≤ τ for some i} ≥ 1 − Σ_e η_e`.  Conversely, for `K = 2`, if
some colouring and its complement are both realised within `τ` (*switching gap* `g_2 ≤ τ`), then for every
`0 < s ≤ min w_i` there is an ensemble with every edge law within `W_∞`-distance `τ` of that of `μ` and mass `2s` on
two configurations that are not conformers.
*Proof.*  Off a set of mass `Σ η_e` every `F_e(y)` is within `τ` of some `t_{e,a(e)}`, so `F(y)` is within `τ` of the
splice `q^a`, which then is a conformer's vector.  Converse: `(w_1 − s)δ_{x_1} + (w_2 − s)δ_{x_2} + sδ_y + sδ_{y'}`.  ∎

For random ensembles the gap is small (§3, T2 and T5; units in which the mean squared edge length is 4;
medians over 6–8 random ensembles of the 2-norm gap, which bounds the sup-norm gap from above).  On the minimally
globally rigid graphs (codimension `c = 1` of the measurement variety): `K_4` — `3·10⁻²`, `2·10⁻³`, `3·10⁻⁴`,
`8·10⁻⁵`, `2·10⁻⁵` for `K = 2, …, 6`; the wheel on five vertices — `1·10⁻³`, `2·10⁻⁵`, `7·10⁻⁶` for `K = 2, 3, 4`; the
wheel on six vertices — `8·10⁻⁴`, `7·10⁻⁶` for `K = 2, 3`, with single random ensembles at `8·10⁻⁷` and `1.2·10⁻⁹`
(both verified to be positive, the second in 40-digit arithmetic).  With redundancy: `K_5 − e` (`c = 2`)
`4·10⁻²`, `3·10⁻³`, `1·10⁻³`; `K_5` (`c = 3`) `8·10⁻²`, `1·10⁻²`, `1·10⁻²` for `K = 2, 3, 4`; `K_6` (`c = 6`) `0.11`,
`0.17` for `K = 2, 3`.  The switching gap of complementary pairs (`K = 2`) is `0.22` (`K_4`), `0.025` (`W_5`),
`0.044` (`W_6`), `0.24` (`K_5 − e`), `0.23` (`K_5`).  The medians follow `(K^{|E|})^{−1/c}`,
`c = |E| − (dN − d(d+1)/2)`, within a factor of about 6 over four orders of magnitude **[N]**; a nearly
degenerate conformer (three almost collinear points) shrinks the gap further by about the area of the thin
triangle.  So (medians of the sup-norm gap relative to the mean squared length, table in §3): a band of `10⁻³`
of a squared length already admits a "chimera" for three conformers on `K_4`, the two wheels and `K_5 − e` (not
on `K_5` and `K_6`, whose medians are `2·10⁻³` and `2·10⁻²`), and for two conformers on the wheels.
(ii) **Moments.**  The certificate `f` has quadratic minima at the conformers, so the sharp-minimum bridge of
Theorem E2 and §5 item 1 does not apply to Part II.  Locally the best modulus is Hölder ½: a conformer split in
two at distance `±s` changes every moment by `O(s²)` (fitted exponents `2.00`–`2.02`), so moments within `ε` cannot
exclude a spread `≈ (0.05…1.5)·√ε` of a conformer.  Globally (T4, three random instances per case, explicit
adversarial ensembles from a linear programme; "far" = at distance at least 1 in the vector of all squared pair
distances, about 10 % of its norm): with all `2K|E|` moments within relative `ε = 10⁻⁵` of those of `μ`, the mass
far from every conformer can be `0.1`–`0.8 %` (`K_4`, `K = 1`), `0.2`–`1.7 %` (`K_4`, `K = 2`), `3`–`76 %` (`K_4`,
`K = 3`), `0.1`–`1.3 %` (`W_5`, `K = 1`), `14`–`62 %` (`W_5`, `K = 2`), `14`–`57 %` (`W_5`, `K = 3`).  The bound that
their certificate itself gives (Markov) guarantees "at most 10 % far" only for `ε ≤ 10⁻⁴`–`8·10⁻⁴` (`K_4`, `K = 1`),
`3·10⁻⁷`–`9·10⁻⁵` (`W_5`, `K = 1`), `3·10⁻⁹`–`5·10⁻⁸` (`K_4`, `K = 2`), `2·10⁻¹²`–`8·10⁻¹¹` (`W_5`, `K = 2`), and
`10⁻¹⁹`–`10⁻¹²` for `K = 3`.  Evaluating the mean of `f` from the moments is itself a cancellation of
`Σ|c_{e,j}|m_{e,j} ≈ 10²`–`10³` (`K = 1`), `10⁴`–`10⁵` (`K = 2`), `10⁶`–`10⁹` (`K = 3`) down to zero.
*Replacement text* (after Theorem E7): "Stability.  If every edge-length law is known up to a band `τ` smaller than
the chimera gap of the ensemble, the conclusion holds up to `τ` and up to the mass outside the bands (R21,
Proposition B); when a colouring and its complement are realised within `τ` it fails.  For random ensembles the
gap is of the order `(K^{|E|})^{−1/c}` relative to a squared length — about `10⁻³` for two conformers and `10⁻⁵`
for three on minimally globally rigid graphs."  After Corollary E8: "The certificate is not sharp (its minima
are quadratic): the identification is Hölder-½ at best; a relative accuracy `10⁻⁵` of the moments still allows
more than a tenth of a generic three-conformer ensemble on `K_4`, or of a two-conformer ensemble on the wheel,
to be far from every conformer (R21, T4), and the mean of `f` cannot be evaluated from moments known to fewer
than `log₁₀(Σ|c|m)` digits."

### M4 (major, framing) — novelty classes: E5 is a dimension count, E7 a corollary; the headline equality is the case `K = 1` in one direction

*Where.*  `THEOREM_REGISTER.md` rows E5(a), E6, E7, E8 ("new (not found)"); report lines 29–30, 395–400;
`PRIOR_ART.md` lines 61–69; the headline "Ensemble rigidity = global rigidity".
*What decides it.*  Their own proof of E5(a) (lines 378–381) is the inequality
`Σ r(J_i) ≥ r(J_1) + r(J_1^c) > r = dim V`: the definition of a connected matroid read on dimensions.  For two
points it is the standard fact that an irreducible variety is the product of two coordinate projections iff the
partition is a separator (their (b); Lemma 3.1 of the 2022 paper in one direction).  Moreover **the published
proof of the cited Theorem 3.5 already is a splice along a separator**: as returned by the fetch tool, it takes
the lengths of `p` on `E_1` and those of `2p` on `E_2`, notes that `(x_1, 4x_2)` lies on the measurement variety by
the product lemma, realises it by a generic `q` with the same stresses, and contradicts global rigidity.  E7 is
then E6 plus that theorem (their proof: four lines), and (b) ⇒ (a) is `K = 1`.  E8 adds, edge by edge, the
classical certificate `Π_i (t − t_i)²` that makes a `K`-atomic measure on the line the only measure with its first
`2K` moments.  What I did **not** find in print (§6) is the *reading* — identification of a finite mixture of
frameworks from one law per edge.
*Replacement text* (register).  E5(a): "elementary (dimension count from the rank function); formulation; the
`K`-fold statement not found in print".  E7: "corollary of Garamvölgyi–Gortler–Jordán 2022, Theorem 3.5, through
E5(a)/E6 (four lines); the reading as identification of mixtures from per-edge laws not found (searches: R21
§6)".  E8: "the classical `2K`-moment certificate of a `K`-atomic measure, edge by edge, plus E7; not found for
frameworks".  Headline: "Global rigidity implies ensemble rigidity (generic, exact, point conformers); the
converse is the case of one conformer."

### Minor findings

* **m1.**  "Assume no `F_e` is constant" (line 363) is redundant in E5(a) and needed in (b)/E6 (§1).
  *Replacement:* move the assumption into (b) and Corollary E6.
* **m2.**  Lines 417–419 ("identification of finite ensembles = absence of chimeras = connectivity") and 485–487
  ("the ensemble is identified exactly when that set contains nothing but the conformers") assert equalities of
  which only one direction is a theorem: absence of chimeras ⇒ identification (E6).  The converse fails for
  individual tuples: **one** realised non-constant splice does not break identification — for `K = 2` and
  realisable set `{F(x_1), F(x_2), q^a}` the marginal equations force the mass of `q^a` to be zero.  The exact
  criterion for a given tuple is the uniqueness of the non-negative table on the realisable colourings with the
  prescribed marginals; for `K = 2` it fails iff some non-negative combination of realisable non-constant
  colourings gives every edge the same total weight of conformer 1 — the simplest case is a colouring together
  with its complement (Example D1), another is three colourings whose 1-classes partition the edge set.
  *(My notes of 17:04Z and the first draft of this item said that a complementary pair is "needed"; that is
  sufficient, not necessary — an error of mine, corrected at 18:11Z, §8.  The formulation "unique non-negative
  table" is also the one of their internal review, §9.)*  *Replacement:* "absence of chimeras ⇒ identification;
  the converse is false (a realised chimera need not carry mass); a tuple is identified iff the non-negative
  table on its realisable colourings with the prescribed marginals is unique".
* **m3.**  E7, proof (line 448): (b) ⇒ (a) uses neither cited theorem.  The first cited theorem is used only to
  make (a) a graph property, and it yields the stronger negative side (§1, item 8).  *Replacement:* add "if `G`
  is not generically globally rigid, no generic finite ensemble is determined".
* **m4.**  "Modulo congruence" (line 443–444) should say "each conformer up to its own congruence, reflections
  included; no handedness of any conformer is determined".
* **m5.**  The count `2K|E|` (line 469) is sufficient, not necessary.  (i) Edges outside a generically globally
  rigid spanning subgraph need no moment.  (ii) Among ensembles with at most `K` conformers, `2K − 1` moments per
  edge suffice (two measures with at most `K` atoms each and equal moments of orders `0, …, 2K − 1` coincide).
  (iii) **Proposition C [P; checked numerically, T7].**  If `(G, x)` has a positive semidefinite equilibrium
  stress matrix `Ω` of rank `N − d − 1` (every generic framework of `K_N`, `N ≥ d + 2`), and `E_2 ⊆ E` is a set of
  `d(d+1)/2` edges whose directions do not lie on a conic at infinity, then `δ_x` is determined among all
  ensembles by `E ℓ_e²` (`e ∈ E`) and `E ℓ_e⁴` (`e ∈ E_2`): `|E| + d(d+1)/2` means instead of `2|E|`.  Proof:
  `f(p) = tr(pᵀΩp) + Σ_{e ∈ E_2} (ℓ_e(p)² − ℓ_e(x)²)²` is non-negative, in the span, has mean zero, and vanishes iff
  `p = xA + b` (kernel of `Ω`) with `AAᵀ = I` (the `E_2`-lengths).  ∎  So the sentence "`j ≤ 2` certifies a single
  conformation" (line 489) can be sharpened.
* **m6.**  Line 489 ("`j ≤ 2` certifies a single conformation"): only if the unknown is generic.  Data cannot
  certify genericity; what data can do is replace it by a finite check — enumerate the `K^{|E|}` splices of the
  observed atoms, decide which are realisable, check that the weights are then unique — at exponential cost.
* **m7.**  §5 item 2 (lines 704–706): "exactly the ensembles carried by the ground states of an energy in the
  span" is Theorem E1(a) (finite `X`) minus the affine-independence condition, and is false on compact continua
  by their own Example E1.2 (an identified conformation with no exposing energy).  *Replacement:* "on a finite
  space: exactly the ensembles carried by the ground states of an energy in the span, with affinely independent
  features there; on a continuum the minimal face need not be exposed (Example E1.2)".
* **m8.**  §5 item 4 (lines 716–721): "is an ensemble theorem by Corollary E6" needs three qualifications:
  E5/E6 are stated for polynomial maps on `ℝ^D` — torsion-angle and orientational maps live on tori and need the
  version on an irreducible variety with a rational map (the proof is the same, but irreducibility of the
  configuration space is a hypothesis); E6 identifies feature vectors, not configurations (generic injectivity
  is a second question, as lines 417–419 say); and "generic" is then generic in *that* parameter space — conformers
  with one common torsion value are excluded.
* **m9.**  For `d ≥ 2`, graphs with a connected rigidity matroid are strictly more than the globally rigid ones:
  two copies of `K_4` glued along an edge, with or without that edge (`N = 6`), are rigid and redundantly rigid,
  not 3-connected, hence not globally rigid, and have a connected rigidity matroid (`T1`); generic pairs have no
  chimera (`T3(c)`) and the ensemble fails to be determined through a flip, at `K = 1`.  So the ensemble-specific
  content of E7 is E6 for connected rigidity matroids: **a generic finite ensemble on any graph with connected
  rigidity matroid is determined up to replacing each conformer by an equivalent framework.**  Worth stating; it
  also means that "rigid but not globally rigid" is not a control that must produce a chimera (the brief's
  suggestion; I used graphs with a disconnected matroid and non-generic conformers instead).
* **m10.**  `PRIOR_ART.md` marks Gortler–Healy–Thurston as "memory" and `OPEN_OBLIGATIONS.md` OB4 asks for the
  exact genericity statement: it is Definition 1.4 / Corollary 1.15 there (opened here), identical to the one
  used.  OB4's other half — nothing in Sections 4–5 of the 2022 paper contains E5(a)/E7 — is confirmed at the
  level of a tool-made extraction of the full text (§6).
