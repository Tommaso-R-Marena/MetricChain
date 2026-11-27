# R21 — adversarial review of the Ensemble division's Theorems E5, E7, E8, of the reading of E1.3, and of §5

*Workstream R21 of the science division, 2026-11-26.  Asked for by the Ensemble Identifiability and Certified
Inference Division (`ENSEMBLE-MSG-0002` §4, question E-S2).  **This is an internal review by an AI session, not
external peer review.***

**Which version each part refers to.**  Sections 0–8 review **version 1** of their report: branch
`research/ensemble-identifiability` at commit `a570520` (read-only export; `docs/ensemble/ENSEMBLE_REPORT.md`
§2.1 Corollary E1.3, §3.2 E5/E6, §3.3 E7/E8, §5, §8, §9; `THEOREM_REGISTER.md`; `PRIOR_ART.md`;
`experiments/ensemble/`).  All line numbers in sections 0–8 are those of `ENSEMBLE_REPORT.md` at `a570520` unless
a file is named.  The findings of sections 1–7 were written down (this file and
`experiments/science/ws_R21/NOTES.md`, with clock times) **before** I opened anything of their second checkpoint.
Section 9 compares them with **version 2** (commit `1a067b5`, published 18:07 UTC while this review was running)
and with their own internal review; it does not review the new material of version 2.

Four kinds of checking are kept apart: **review** (read and re-derived), **replication** (re-computed with my
own code, written before I opened any of their scripts), **re-run** (their code, from a scratch copy), **read
only**.  Labels: [P] proof given here, [N] numerical evidence only, [K] known and cited (with the reading
level), [H] heuristic.

## 0. Verdict in ten lines (version 1, `a570520`)

1. **E5, E6, E7, E8, E1.3 are proved as stated in the report** (with its definition of "generic", lines 434–436):
   every step re-derived, no gap found.  **No critical finding.**
2. The two cited theorems exist, are quoted correctly and their hypotheses are met (opened through a fetch tool:
   Garamvölgyi–Gortler–Jordán 2022, Theorem 3.5; Gortler–Healy–Thurston 2010, Corollary 1.15).
3. *Replication* (own code, plane): 549 908 non-constant splices of 64 random ensembles of two and three
   conformers on seven globally rigid graphs — **no chimera** by an exhaustive exact method (no control violated);
   the least-squares search crossed its pre-set threshold once (`7.9·10⁻⁷`, shown to be a positive minimum) and
   missed 64 things that exist.  Controls that must find a chimera found them (160 of 160; 320 of 320; D1).
4. **M1 (major).**  The reading of E1.3 ("mean squared distances determine nothing") holds on the free
   configuration space only.  With prescribed bond lengths a conformation in general position *is* determined by
   mean squared distances (Proposition A), and two generic conformers of a planar chain from seven bonds on [N].
5. **M2 (major).**  "Generic" means *jointly* generic.  For individually generic conformers the conclusion of E7
   fails: on `K_4` with no common edge length (Example D1, exact) and on the globally rigid graph `K_5 − e` with a
   shared triangle (Example D2).
6. **M3 (major).**  Exactness in numbers: the chimera gap behaves like `(K^{|E|})^{−1/c}` — `10⁻³` of a squared
   length for two conformers, `10⁻⁵` for three, on minimally globally rigid graphs; for E8, moments accurate to
   `10⁻⁵` still leave 3–76 % (`K_4`, three conformers) or 14–62 % (wheel, two conformers) of an explicit ensemble
   far from every conformer, and the certificate's own bound needs `10⁻⁸` to `10⁻¹⁹`.
7. **M4 (major, framing).**  E5 is a dimension count, E7 a four-line corollary of the cited 2022 theorem (whose
   published proof already splices two frameworks along a separator), E8 the classical per-edge certificate; the
   *reading* as identification of mixtures was not found in eighteen searches.
8. **Minor** (m1–m10 and five remarks on their scripts): a redundant hypothesis; "identification = absence of
   chimeras" holds in one direction only; the full dichotomy; reflections; `2K|E|` is not necessary (Proposition
   C); §5 items 2 and 4; graphs with connected rigidity matroid are more than the globally rigid ones; a stale
   number ("22 zeros", their output says 82).
9. *Re-run:* their `run_all.py` reproduces their `output.txt` exactly (timings apart).  Their checks R3 and R5
   pass for reasons that depend on sampling and on the seed (§4).
10. *Not checked:* `d ≥ 3` numerically; E1–E4, Part III, the Lean files; the cited papers were read through a
    fetch tool's extraction, not as pages.

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

## 3. Numerical tests (replication with my own code), with their controls

All code is mine and was written before I opened any script of the reviewed branch
(`experiments/science/ws_R21/`: `r21_common.py`, `t1`–`t7`, `t2b`, `t4b`).  Plane (`d = 2`), conformer
coordinates i.i.d. standard normal (fixed seeds; mean squared edge length = 4), float64.  Every log cited reached
its last line (`DONE …`); stopped or failed runs are in `not_cited/` (one: a follow-up script that crashed on a
coding error).  Two independent methods decide whether a vector of squared lengths is realisable:
**LM** — batched Levenberg–Marquardt on `‖F(p) − q‖₂` from random starts (the method prescribed by the brief; a
local search, it can miss); **EXACT** — ruler-and-compass enumeration of all `2^{N−3}` realisations of a spanning
subgraph built by adding vertices of degree two, then comparison of the remaining edges (exhaustive; validated on
2 000 planted realisable vectors per graph: all found, largest defect `9·10⁻¹²`).

**T1 — the graphs** (`logs/t1_graphs_run1.log`; 0 violations of 3 consistency checks × 14 graphs).  Rank, redundant
rigidity, vertex connectivity, stress-matrix rank at three random points, and all separators of the rigidity
matroid by brute force over the bipartitions of the edge set.

| graph | N | \|E\| | globally rigid (stress rank `N−3`; 3-connected and redundantly rigid) | separators | matroid |
|---|---|---|---|---|---|
| `K_4`, `K_5`, `K_5 − e`, wheel `W_5`, `K_6`, wheel `W_6`, `K_{3,3} + e` | 4–6 | 6–15 | yes | 0 | connected |
| triangle, `K_4 − e`, `K_4` + vertex of degree 2, `K_{3,3}`, prism | 3–6 | 3–9 | no | 3–255 | not connected |
| two `K_4` glued along an edge; the same without that edge | 6 | 11; 10 | **no** (connectivity 2) | **0** | **connected** |

**T2 — chimera search on globally rigid graphs** (`logs/t2_<graph>_K<K>_run1.log`).  Every non-constant colouring
of the edges by the conformers, for random ensembles.  "Found" was defined before the runs as LM residual
`< 10⁻⁶` or EXACT defect `< 10⁻⁹`.

| graph | K | ensembles | colourings examined | smallest LM residual | smallest EXACT defect | found | control violations |
|---|---|---|---|---|---|---|---|
| `W_5` | 2 | 10 | 2 540 | 3.5e-4 | 2.3e-3 | 0 | 0 |
| `K_5 − e` | 2 | 10 | 5 100 | 2.4e-3 | 5.3e-3 | 0 | 0 |
| `K_5` | 2 | 10 | 10 220 | 6.3e-3 | 1.5e-2 | 0 | 0 |
| `W_6` | 2 | 10 | 10 220 | 4.4e-6 | 1.5e-4 | 0 | 6 (LM) |
| `K_{3,3} + e` | 2 | 10 | 10 220 | 1.0e-5 | 5.2e-5 | 0 | 8 (LM) |
| `K_6` | 2 | 3 | 98 298 (LM on 11 614 of them) | 3.6e-2 | 8.0e-2 | 0 | 0 |
| `W_5` | 3 | 3 | 19 674 | 3.4e-5 | 1.4e-4 | 0 | 2 (LM) |
| `K_5 − e` | 3 | 2 | 39 360 | 1.3e-4 | 1.2e-4 | 0 | 0 |
| `K_5` | 3 | 2 | 118 092 | 1.3e-2 | 1.3e-2 | 0 | 0 |
| `W_6` | 3 | 2 | 118 092 | **7.9e-7** | 2.3e-6 | **1 (LM threshold)** | 30 (LM) |
| `K_{3,3} + e` | 3 | 2 | 118 092 | 5.3e-6 | 1.8e-5 | 0 | 18 (LM) |

549 908 colourings in 64 ensembles.  **EXACT: no chimera; none of its controls violated** (the conformers and 200
planted realisable vectors per ensemble, all found).  **LM: one colouring below the pre-set threshold** (`W_6`,
`K = 3`, ensemble 0, colouring `2211222020`, residual `7.9·10⁻⁷`; EXACT defect of the same colouring `2.3·10⁻⁶`).
Follow-up (`t2b_w6_followup.py`, `logs/t2b_w6_followup_run1.log`): the same ensemble reproduced; the residual is
`7.9229962·10⁻⁷` after 120, 1 000 and 5 000 iterations from 400 starts each (about 100 starts reach that same
value), gradient norm `10⁻¹⁴`, smallest singular value of the Jacobian `0.28`, unchanged by 60 Gauss–Newton steps,
while the three conformers reach `10⁻¹⁶` under the same procedure.  It is a converged *positive* minimum — a
framework whose ten squared lengths are within `8·10⁻⁷` of lengths of the three conformers, not all of the same
one — i.e. no chimera, and a measure of how thin the margin is.  The threshold `10⁻⁶` was too loose for this
graph (realisable targets end below `10⁻⁹`); I did not relabel the log.
*Controls of the LM search:* 64 violations, all of them misses of things that exist — planted realisable vectors
not found by any start (63) and, once, a conformer itself (`W_6`, `K = 3`, 10 starts).  Per-start success of LM on
planted realisable vectors: `0.995`–`1.00` on `K_5`, `K_6`; `0.83`–`0.88` on `K_5 − e`; `0.61`–`0.68` on `W_5`;
`0.45`–`0.50` on `K_{3,3} + e`; `0.31`–`0.37` on `W_6`.  So on the sparse graphs **the
LM search alone is not evidence of absence** (it misses 1–7 % of realisable vectors at the numbers of starts
used); the verdict of T2 rests on EXACT, with LM as the second method.

**T3 — controls that must find a chimera** (`logs/t3_controls_run1.log`; 1 violation of a prediction in total).
(a) `K_4` + vertex of degree two (rigid, not globally rigid, matroid not connected), 40 generic pairs × 254
colourings: a closed-form criterion coded separately (the splice is constant on the `K_4` block and the two
pendant radii satisfy the triangle inequality with the base edge) predicts 160 chimeras, at least one in 40 of 40
pairs; LM found 160, EXACT 160, neither found anything not predicted.
(b) Example D2, 20 pairs: 320 predicted chimera colourings; EXACT 320, LM 319 (one miss, 12 starts); the two
ensembles have identical per-edge multisets (difference `0.0`) and the chimeras are not congruent to the
conformers (smallest difference of the full distance vectors `0.22`).  The same conformers on `K_5`: 0 chimeras.
(c) Two `K_4` glued along an edge, with and without that edge (not globally rigid, connected matroid), 10 generic
pairs × 2 046 / 1 022 colourings: 0 chimeras (smallest LM residual `4·10⁻⁴` / `7·10⁻⁶`), while the flip of one
`K_4` changes no measured squared length (`10⁻¹⁴`) and an unmeasured one by at least `0.70`: the ensemble is not
determined, at `K = 1`, without any chimera (m9).
(d) Example D1 in exact rational arithmetic (the four frameworks, the equality of the per-edge multisets, no
common length); the search on `(x_1, x_2)` finds exactly the two complementary colourings `011111`, `100000`
among 62 (smallest residual of the other 60: `0.094`); 20 random members of the family: both chimeras found by
both methods and nothing else in 20 of 20.

**T4 — Corollary E8 in numbers** (`logs/t4_{K4,W5}_K{1,2,3}_run1.log`; three random instances each, random
weights; statistics extracted by `summarize_t4.py`, `logs/summarize_t4_run1.log`).  (1) The mean of `f` under `μ`
is at most `1.8·10⁻²⁴` evaluated on the conformers and at most `6.7·10⁻⁸` in absolute value evaluated from the
moments, with a cancellation `C_abs = Σ|c_{e,j}| m_{e,j}` of `1.3·10²`–`1.8·10³` (`K = 1`), `7.8·10³`–`1.6·10⁵`
(`K = 2`), `8.6·10⁵`–`7.1·10⁸` (`K = 3`): **an error `ε` of the moments is an error `ε·C_abs` of the mean of the
certificate.**  (2) Perturbed ensembles: other weights — mean of `f` unchanged (at most `1.1·10⁻²⁴`) although a
moment changes by a relative amount of up to `5.4`; every conformer displaced by `δ` — mean of `f` `∝ δ^p` with
fitted `p` between `1.994` and `2.004`; one conformer split in two at `±s` — largest relative change of a moment
`∝ s^p`, `p` between `2.00` and `2.02`, so moments within `ε` cannot exclude a spread `s ≈ (0.05…1.5)·√ε` of a
conformer.
(3) Zeros of `f` by LM from 6 000 starts: no zero that is not a conformer in any of the 18 instances — but the
control of this check (every conformer must be reached) **fails in 4 of the 18** (`K_4`, `K = 3`, instance 1:
conformers reached `[41, 0, 597]` times; all three `W_5`, `K = 3` instances, where only 9–17 runs reach any zero
and one conformer is never reached).  In those four the check says nothing; it supports E8 in the other 14.
(4) What error of the moments is tolerated.  `D(p)` = distance of the vector of all squared pair distances of `p`
to the nearest conformer's; "far" = `D ≥ 1` (about 10 % of the norm of that vector).  *Guarantee* (Markov with
their certificate): `ν(far) ≤ ε·C_abs/γ*`, `γ*` the least value of `f` on the far set (near-chimeras; found by LM
and a constrained search).  *Adversary*: a linear programme over an explicit finite candidate set gives an
ensemble with all `2K|E|` moments within relative `ε` of those of `μ` and as much mass as possible far away (287
programmes solved, achieved error `≤ 1.05ε` in all; 1 programme failed and is not used).  Far mass of the
adversary at `ε = 10⁻³ / 10⁻⁴ / 10⁻⁵` (three instances), and the `ε` the certificate needs to keep it below 10 %:

| graph | K | adversary: far mass at `ε = 10⁻³ / 10⁻⁴ / 10⁻⁵` | certificate guarantees `≤ 10 %` far mass only if `ε ≤` |
|---|---|---|---|
| `K_4` | 1 | .37/.042/.0043  .77/.081/.0083  .073/.0075/.00075 | 1.0e-4 … 7.6e-4 |
| `K_4` | 2 | .28/.038/.0043  .92/.15/.017  .18/.021/.0022 | 3.5e-9 … 4.6e-8 |
| `K_4` | 3 | .59/.15/.027  1/1/.76  1/.58/.30 | 1.8e-19 … 1.1e-12 |
| `W_5` | 1 | .24/.028/.0030  1/.11/.013  .11/.012/.0012 | 3.1e-7 … 9.4e-5 |
| `W_5` | 2 | .81/.28/.14  1/.83/.24  1/1/.62 | 2.0e-12 … 8.0e-11 |
| `W_5` | 3 | 1/.97/.57  .91/.51/.14  1/.78/.28 | 5.6e-18 … 2.7e-15 |

Reading.  For one conformation on `K_4` the two sides agree within a factor two: a relative accuracy `10⁻⁴` of
the two moments per edge keeps all but 1–10 % of the ensemble near `x`.  From `K = 2` on the adversary
needs no near-chimera to be exact: with moments accurate to `10⁻⁵` (relative; moments up to `E ℓ⁸` for `K = 2`,
`E ℓ¹²` for `K = 3`) an explicit ensemble still has 0.2–2 % (`K_4`, `K = 2`), 3–76 % (`K_4`, `K = 3`), 14–62 %
(`W_5`, `K = 2, 3`) of its mass far from every conformer.  The adversary's numbers are lower bounds of the worst
case (finite candidate set; with a second, three times larger random candidate set they changed by a factor
between 0.93 and 2.6, median 1.03, over 143 pairs of programmes); the certificate's are upper bounds; the truth is between, and the gap between the two is itself a finding: **their
certificate is a very weak witness of stability.**  Even `K = 1` can be fragile on a minimally globally rigid
graph: in `W_5` instance 0 a visibly different framework (`D = 0.63`) has all eight squared lengths within
`7.7·10⁻⁵` of those of `x` (`t4b_w5_followup.py`, `logs/t4b_w5_followup_run2.log`: a converged positive minimum,
same value after 300 and 3 000 iterations, gradient `4·10⁻¹⁴`) — a *near-flip*, the one-conformer analogue of a
near-chimera.

**T5 — how close do random ensembles come to a chimera?** (`logs/t5_<graph>_K<K>_run1.log`; table extracted by
`summarize_t5.py` into `logs/summarize_t5_run1.log`.)  *Chimera gap* `g_1` = least distance (2-norm, squared-length
units; mean squared edge length = 4) from a non-constant splice to the set of realisable vectors, computed by
LM; every value is realised by an explicit framework (re-checked in the log), so each is an upper bound of the
true gap; with more than 2 000 colourings LM is run on the 1 000 colourings of smallest EXACT defect and 1 000
random ones.  *Switching gap* `g_2` (`K = 2`): least over colourings of the larger of the distances of a
colouring and of its complement.  `c` = codimension of the measurement variety.

| graph | \|E\| | c | K | splices | ensembles | `g_1` median | `g_1` smallest | sup-norm gap / mean squared length (median) | `g_2` median | heuristic `splices^{−1/c}` |
|---|---|---|---|---|---|---|---|---|---|---|
| `K_4` | 6 | 1 | 2 | 62 | 8 | 3.2e-2 | 1.9e-2 | 4.7e-3 | 0.22 | 1.6e-2 |
| `K_4` | 6 | 1 | 3 | 726 | 8 | 2.3e-3 | 2.2e-4 | 5.1e-4 | | 1.4e-3 |
| `K_4` | 6 | 1 | 4 | 4 092 | 8 | 2.8e-4 | 3.5e-5 | 3.9e-5 | | 2.4e-4 |
| `K_4` | 6 | 1 | 5 | 15 620 | 8 | 8.1e-5 | 8.1e-6 | 1.5e-5 | | 6.4e-5 |
| `K_4` | 6 | 1 | 6 | 46 650 | 8 | 1.7e-5 | 4.3e-6 | 4.5e-6 | | 2.1e-5 |
| `W_5` | 8 | 1 | 2 | 254 | 8 | 1.1e-3 | 2.0e-5 | 4.0e-4 | 0.025 | 3.9e-3 |
| `W_5` | 8 | 1 | 3 | 6 558 | 8 | 2.4e-5 | 1.0e-6 | 6.0e-6 | | 1.5e-4 |
| `W_5` | 8 | 1 | 4 | 65 532 | 8 | 6.8e-6 | 4.8e-8 | 1.2e-6 | | 1.5e-5 |
| `W_6` | 10 | 1 | 2 | 1 022 | 6 | 8.3e-4 | 1.3e-4 | 1.4e-4 | 0.044 | 9.8e-4 |
| `W_6` | 10 | 1 | 3 | 59 046 | 6 | 6.8e-6 | **1.2e-9** | 1.6e-6 | | 1.7e-5 |
| `K_5 − e` | 9 | 2 | 2 | 510 | 8 | 3.7e-2 | 2.7e-4 | 6.0e-3 | 0.24 | 4.4e-2 |
| `K_5 − e` | 9 | 2 | 3 | 19 680 | 8 | 3.2e-3 | 8.1e-4 | 8.7e-4 | | 7.1e-3 |
| `K_5 − e` | 9 | 2 | 4 | 262 140 | 8 | 1.4e-3 | 3.2e-5 | 1.8e-4 | | 2.0e-3 |
| `K_5` | 10 | 3 | 2 | 1 022 | 8 | 8.3e-2 | 2.3e-2 | 1.1e-2 | 0.23 | 9.9e-2 |
| `K_5` | 10 | 3 | 3 | 59 046 | 8 | 1.2e-2 | 3.1e-4 | 2.3e-3 | | 2.6e-2 |
| `K_5` | 10 | 3 | 4 | 1 048 572 | 8 | 1.0e-2 | 6.4e-4 | 1.5e-3 | | 9.8e-3 |
| `K_6` | 15 | 6 | 2 | 32 766 | 6 | 0.11 | 7.4e-2 | 2.4e-2 | | 0.18 |
| `K_6` | 15 | 6 | 3 | 14 348 904 (2·10⁶ sampled) | 6 | 0.17 | 7.8e-3 | 2.1e-2 | | 6.4e-2 |

The heuristic agrees with the medians within a factor of about 6 over four orders of magnitude **[N]**.  On the
minimally globally rigid graphs (`c = 1`) the median gap of two conformers is `8·10⁻⁴`–`3·10⁻²`, of three
`7·10⁻⁶`–`2·10⁻³`, and it loses roughly one order of magnitude per further conformer; redundancy is what buys a margin (`K_6`: a
few per cent of a squared length).  *One value was examined before use:* `W_6`, `K = 3`, ensemble 2:
`g_1 = 1.19·10⁻⁹`.  Follow-up `t5b_w6_followup.py` (`logs/t5b_w6_followup_run1.log`; the random stream is replayed
exactly): three independent checks agree that it is positive — LM gives `1.1901008·10⁻⁹` after 1 000 and 10 000
iterations from the minimiser and from 126–127 of 400 random starts (gradient `2·10⁻¹⁴`, Jacobian singular values
`0.58`–`8.5`); EXACT gives a check-edge deviation `+5.39·10⁻⁷` for the nearest of the 16 flip patterns; and in
40-digit arithmetic the stationary point of `‖F − q‖²` lies `2.9·10⁻¹⁵` from the float minimiser with residual
`1.19010123465522·10⁻⁹`.  A chimera to nine digits, not a chimera; the reason is a nearly degenerate conformer
(three of its points almost collinear, triangle area `1.1·10⁻³`), which makes the angle at the hub about `10³`
times more sensitive to the lengths.

**T6 — E1.3 and its reading** (`logs/t6_e13_reading_run2.log`; `logs/t6d_chains_<n>bonds_run1.log`; run 1 of the
first script exceeded its time estimate and was stopped — `not_cited/`).  (a) E1.3(b) replicated (`N = 5`, two
conformers, all ten pairs): the mean squared lengths under the law of `R·p`, `R² ∈ {0, 2}`, agree with those of
`μ` to `5·10⁻¹⁵`, `P(Q = 0)` is `0` and `0.5`; the affine mechanism (`A_1`, `A_2` with `tA_1A_1ᵀ + (1−t)A_2A_2ᵀ = I`)
gives equality to `2·10⁻¹⁵` with conformers not congruent to those of `μ`.  (b) `⟨r⁻⁶⟩` of all pairs is preserved
(to `9·10⁻¹⁶`) by a scaling with `R⁻⁶ ∈ {0.5, 1.5}`.  (c) Proposition A on planar chains with unit bonds, all pairs
measured, 20 random conformations × 400 minimisations of `‖P^⊥ b(p)‖²` over the chain space each: with 3, 4 and 6
bonds, 8 000 of 8 000 minimisations end in a zero congruent to `x` and none elsewhere; `‖P^⊥ b(p)‖²` is an affine
function of the squared pair distances on the chain space to `10⁻¹⁴`; with 2 bonds the function vanishes
identically (8 000 non-congruent zeros — not determined); for a conformation with two parallel bonds the explicit
two-point mixture of part (ii) has the bond lengths of the chain to `7·10⁻¹⁶` and the mean squared distances of
`x` to `3·10⁻¹⁵`, with a conformer that differs from `x` by `1.33` in a squared distance.  (d) Two generic chain
conformers (12 random pairs per bond count, weights 0.4/0.6, 2 000 LM starts on the bond-length equations of
`x_1A_1 + x_2A_2`; control: `x_1` and `x_2` themselves are reached — in 12 of 12 pairs from 7 bonds on):

| bonds | quadrics through the bond vectors | chains `x_1A_1 + x_2A_2` other than `x_1, x_2` | largest mass an ensemble with the same mean squared distances puts off `{x_1, x_2}` |
|---|---|---|---|
| 4, 5, 6 | 6, 5, 4 | a continuum (600 kept) in 12/12 | **1.000 in 12/12 — not determined** |
| 7 | 3 | 2 (median), up to 4, in 11/12 | 0 in 12/12 (the solutions are affinely independent) — determined |
| 8 | 2 | none in 12/12 | 0 — determined |
| 9, 10, 12 | 1 | none in 12/12 | 0 — determined |

For at least nine bonds this is a proof given the rank that the script computes: the quadratic forms vanishing
on the vectors `c_u = (b_u(x_1), b_u(x_2)) ∈ ℝ⁴` are then the multiples of `diag(I, −I)`, so the only positive
semidefinite solutions of rank at most two of `c_u S c_uᵀ = 1` are `diag(I, 0)` and `diag(0, I)` **[P given N]**.
In general one expects that a chain of `n_b` bonds in `ℝ^d` resolves of the order of `√(2n_b)/d` generic
conformers from mean squared distances **[H]** — the `d`-dimensional analogue of the capacity question of their
Part III.

**T7 — Proposition C** (`logs/t7_fewer_means_run1.log`; 0 violations).  `K_4` and `K_5` in the plane, 10 random
frameworks each: the stress matrix built from the affine dependencies is positive semidefinite of rank `N − 3`
in 10 of 10, in equilibrium to `10⁻¹⁵`, and `tr(pᵀΩp) = Σ_e ω_e ℓ_e(p)²` to `10⁻¹⁴`; of 20 000 minimisations of
`f = tr(pᵀΩp) + Σ_{E_2}(ℓ_e² − ℓ_e(x)²)²` all end in a zero congruent to `x`, none elsewhere; with only two edges in
`E_2` (directions on a conic) all 20 000 zeros are non-congruent affine images.  So 9 means instead of 12 for
`K_4`, 13 instead of 20 for `K_5`.

*How to re-run everything:* `cd experiments/science/ws_R21; export OMP_NUM_THREADS=1;` then `python3 -B
t1_graphs.py`, `./run_t2_A.sh`, `./run_t2_B.sh`, `python3 -B t3_controls.py`, `./run_t4.sh`, `./run_t5_C.sh`,
`./run_t5_D.sh`, `./run_t7_t6.sh`, `python3 -B t2b_w6_followup.py`, `python3 -B t4b_w5_followup.py`,
`python3 -B t5b_w6_followup.py`, `python3 -B summarize_t4.py`, `python3 -B summarize_t5.py` (about 75 minutes of
CPU in total, at most two processes, below 0.5 GB each).

## 4. Re-runs of their code (version 1, `a570520`) and what the scripts test (read only)

*Re-run.*  Their five `.py` files and their `output.txt` were copied to `experiments/science/ws_R21/rerun_copy/`
(sha256 of the copies = sha256 of the originals; recorded in `NOTES.md`) **after** my own code had run, because
`run_all.py` writes `output.txt` next to itself.  `cd rerun_copy; OMP_NUM_THREADS=1 python3 -I -B run_all.py`:
exit status 0, last line `ALL PASS`, 2 min 47 s (`logs/rerun_run_all_a570520_run1.log`).  `diff` of the new
`output.txt` with theirs: **identical except the three header lines with the timings** (41 / 113 / 13 s here,
39 / 102 / 17 s there).  So every number of §3.3 that comes from `output.txt` is reproduced: R1 (ranks and
connectivity of eight matroids), R2 (1 240, 2 904, 20 440, 79 998 splices; smallest Cayley–Menger determinant
`1.6·10⁻³`), R3 (`6.0·10⁻⁴`, `2.7·10⁻¹⁵`), R4 (40 of 40, 31 realised), R6.

*Read only* (`rigidity_checks.py`, 240 lines, read in full; of the other scripts I looked only at imports and
file operations).  Five remarks, all minor:
1. **R5 — the report and the output disagree.**  Line 502: "all 22 zeros of the certificate `f` found from 400
   starts".  Their `output.txt`, and my re-run: "82 zeros found in 400 starts; 1 at conformer 1, 81 at conformer
   2, 0 elsewhere".  The number in the report is stale.  More important: the check's own control — both
   conformers must be reached — is passed by **one** hit.
2. **R3 — a threshold that true negatives cross.**  Their "wheel `W_5`" has five spokes (six vertices; it is the
   graph called `W_6` in §3 of this report).  R3 examines 180 random splices of three pairs, two conformers only,
   and passes if the smallest residual exceeds `10⁻⁶`.  On that graph, over *all* 1 022 splices, I find `4·10⁻⁶`
   in one of ten random pairs, and for three conformers `8·10⁻⁷` and `1.2·10⁻⁹` (§3) — values of true negatives.
   The check passes because it samples; with all splices, three conformers, or more pairs it would report
   failures that are not chimeras.
3. **R3, R5 — no control of the search on things that exist.**  The solver is checked on one conformer per pair
   (R3) or by the two conformers (R5).  With my code a random start realises a *realisable* length vector of
   that wheel in one case out of three, and for the hardest per cent of targets in about one start out of
   thirty; 25 starts are then not evidence of absence.  A planted control (lengths of fresh random frameworks)
   and an exhaustive method (the graph has a ruler-and-compass order) would make R3 a test.
4. **R4(b)** tests one colouring (the `K_4` block from `x_1`, both pendant edges from `x_2`) against the two-circle
   criterion; the other five block-constant colourings of each pair are not examined (in my T3(a): 160 of 240
   are realised).
5. **R6** (two toy feature maps) is in the script and in `output.txt` but not in the text of §3.3, which lists
   R1–R5; the register cites it for E5(a).

## 5. What the statements mean for measured data (Item 4)

*What Part II is.*  An exact, generic, point-conformer identifiability statement on the free configuration
space: `K` unknown frameworks and their populations are determined by `|E|` exact atomic laws.  *What it is not*:
a statement about anything known up to an error, about conformers with a width, about conformers that share a
rigid part, or about means.  Item by item (labels: [P] proved here or by them, [N] my numbers, [H] my reading):

1. **Laws versus moments versus means of nonlinear functions.**  E7 needs the whole law of every edge length,
   exactly; E8 needs the `2K` exact moments `E ℓ_e², …, E ℓ_e^{4K}` of every edge.  A *single* mean per edge of a
   function of the distance — the kind of number most averaged measurements deliver — is outside both.  On the
   free space such data identify no ensemble whenever all the functions are homogeneous of one degree `α` (the
   scaling argument of E1.3 with `E[R^α] = 1`; `α = −6` checked, T6(b)) **[P]**.  Through per-edge certificates,
   `K` conformers need a non-negative function with `K` double zeros in the span of the functions measured on each
   edge, hence at least `2K` independent functions per edge **[H]**.  A reader may *not* conclude that mean
   squared distances are useless for chains (M1): with fixed bond lengths they identify single conformations and,
   numerically, generic pairs once there are at least seven bonds in the plane (T6(d)).
2. **Exact laws versus laws with a band.**  Proposition B: the conclusion survives a band `τ` on every law when
   `τ` is below the chimera gap, and fails when a colouring and its complement are realised within `τ` (in
   between it depends on whether some switching component is realised within the band).  Measured gaps (T5,
   units: mean squared edge length = 4): see the table in §3.  A band of a few per cent of a distance is below the
   gap only for strongly over-determined graphs and very few conformers; as a rule of thumb **[H]**, with a
   relative band `τ` one needs `c ≳ |E| ln K / ln(1/τ)`, i.e. a number of measured pairs exceeding the degrees of
   freedom `dN − d(d+1)/2` by the factor `1/(1 − ln K / ln(1/τ))`, and nothing helps once `K τ ≳ 1`.  Already for
   one conformation a random framework on a minimally globally rigid graph can have a *near-flip*: in one of
   three random wheels a visibly different framework reproduces all eight squared lengths to `7.7·10⁻⁵` (T4b).
3. **One law per edge, measured on separate samples.**  This is exactly the model of E7 (marginals, no joint
   information), and the right one for pair-by-pair labelling.  What it hides: each sample carries its own labels,
   so the measured distance is between label positions with their own distribution — a conformer is then not a
   point in the space of measured lengths (item 4), and different edges are measured on chemically different
   molecules.
4. **Point conformers versus conformers that are distributions.**  Not covered; Proposition E8.1 is the
   statement in the other direction.  The mean distances of a basin are not the edge lengths of one
   configuration, so even the vocabulary (splice, chimera) presupposes width zero; with a width `σ` the relevant
   comparison is `σ` against the gap of item 2.  For moments the instability is quantified in §3 (T4): a spread
   `s` of a conformer changes the moments by `O(s²)`.
5. **Genericity versus conformers that share rigid domains.**  Mathematically the excluded tuples have measure
   zero.  Physically they are the rule for articulated chains: (i) every edge inside a rigid unit has the same
   length in all conformers — on the chain's configuration space these features are constant, i.e. loops of the
   matroid, which E5 excludes by hypothesis; (ii) conformers that differ by a few torsions share the lengths of
   all edges that do not span those torsions, so the tuple is non-generic for *every* graph containing such an
   edge; (iii) the conclusion then really can fail on a globally rigid graph (Example D2), and near such tuples
   the gap of item 2 is small.  For conformers that are the states of a few hinges the data are what one expects
   **[H]**: an edge spanning a set `S` of hinges has, generically, one atom per joint state of `S`, so its law is
   the marginal of the joint state distribution on `S` — the marginal problem of Part III — and a single edge
   spanning all hinges gives the whole joint distribution *if* its `2^{|S|}` atoms can be resolved.  So for such
   ensembles the question is which hinge sets are spanned and whether the atoms are resolvable; generic global
   rigidity of the graph is neither necessary nor sufficient.
6. **Genericity is a property of the unknown.**  It cannot be read off the data; but the data allow a finite
   a-posteriori test that replaces it (enumerate the splices of the observed atoms, test realisability and the
   uniqueness of the weights), at a cost exponential in `|E|`.
7. **Is anything stated more generally than the theorem?**  (a) The headline "ensemble rigidity = global
   rigidity" and the message's "every generic finite ensemble" omit *jointly*, *exact* and *point* (M2, M3).
   (b) "Mean squared distances determine nothing" (M1).  (c) §5 item 4 "is an ensemble theorem by Corollary E6"
   (m8).  (d) §5 item 2 "exactly the ensembles carried by the ground states" (m7).  (e) Lines 417–419 and 485–487
   (m2).  (f) §5 item 1 — "certificates produced for equilibrium problems are identification certificates; the gap
   […] is the stability constant" — is a statement about sharp minima on finite spaces; the certificate of Part II
   is not of that kind (M3(ii)), and the coordinator's note SCI-RES-0026 §2(c) already says why it cannot be on a
   manifold.

## 6. Novelty (Item 5): what I opened, what I did not

Reading levels.  **[tool]** = opened through a fetch tool that returns a model-written extraction of the page
(quotations in this report are as returned by that tool; I did not see the page itself); **[summary]** = search
result summary only; **[memory]** = not opened.

| statement | my class | basis |
|---|---|---|
| E1.3(a) | classical, trivial | — |
| E1.3(b) | elementary; correct on the free space; the general mechanism (affine images, conic at infinity) is the standard one of universal rigidity | Prop. A here; super stability / conic at infinity: Connelly; Gortler–Thurston arXiv 1001.0172; Connelly–Gortler–Theran arXiv 1605.07911 [summary] |
| E5(a) | elementary dimension count; a *formulation*.  The `K`-fold statement not found in print | their own proof; for two points it is the separator ⇔ product fact — Lemma 3.1 of Garamvölgyi–Gortler–Jordán [tool] in one direction; a search for the general statement about algebraic matroids of irreducible varieties returned no source |
| E5(b) | transfer of that Lemma 3.1 to polynomial maps, plus a local argument (as they say) | [tool] |
| E6 | elementary given E5(a) | — |
| E7 | **corollary** of Theorem 3.5 of Garamvölgyi–Gortler–Jordán 2022 (four lines); the reading — a finite mixture of frameworks identified from one law per edge — **not found** | [tool]: full text of that paper (Sections 4–5 included: nothing on several frameworks, pooled lengths or copies); Gortler–Theran–Thurston 2019 [tool, 100 of 112 k characters]: one configuration, unlabeled lengths, nothing on several |
| E8 | classical `2K`-moment certificate of a `K`-atomic measure applied per edge, plus E7; not found for frameworks | the per-edge fact is elementary (proof in one line); Lindsay 1989 / Gauss quadrature [summary via Wu–Yang arXiv 1807.07237, abstract page opened] |

Nearest neighbours found, and how they differ:
* **Unlabeled principal component analysis** (Yao–Peng–Tsakiris, arXiv 2101.09446 [tool]: Theorem 2 — a generic
  matrix of rank `r < min(m, n)` whose entries are permuted inside each column is the only matrix of rank `≤ r`
  compatible with the data, up to a row permutation).  Read with rows as points and columns as features, this is
  precisely "a generic *uniform* finite ensemble on an *unknown* generic linear subspace is determined by the
  multisets of its coordinates".  E6 is the version with a known variety, arbitrary weights and arbitrary
  competitor; neither contains the other (their ED4 says the same).
* **Unlabeled rigidity** (Boutin–Kemper [summary]; Gortler–Theran–Thurston [tool]; Garamvölgyi–Gortler–Jordán
  [tool]): one framework from an unlabeled set of lengths.  E7 is a *partially labelled* problem for `K` disjoint
  copies of `G` (each length labelled by its edge, not by its copy); the published theorems do not cover it
  (disjoint unions are not globally rigid), but the published proof of Theorem 3.5 uses the same device (M4).
* **Echo sorting / ghost rejection** (Dokmanić et al., PNAS 2013 [tool]; commentary [tool]): `K` unknown points,
  for each sensor the unlabeled set of distances to them; wrong combinations fail a distance-matrix rank test
  "with probability 1".  This is the no-chimera property for the feature map "distances to the sensors", with
  the genericity on the *sensors* and the points arbitrary — the opposite quantifier to E5(a), and the closest
  published statement in spirit that I found.
* **Joint conformational distributions from separately acquired distance distributions** (Hays–Boland–Kasson,
  arXiv 2010.15612 [tool]): the applied problem of E7; no uniqueness statement, the joint is supplied by
  simulation and a reference ensemble.
* **Sums of measurement maps and secant varieties** (Cruickshank–Mohammadi–Nixon–Tanigawa, arXiv 2305.18990
  [abstract page via tool]): the algebraic setting of Problem O5 and of the remark on `z ∈ (ℝ^{dK})^N` in M1.
* Not opened: turnpike/beltway surveys (Lemke–Skiena–Smith; arXiv 2402.03787) — one point set from pooled
  distances; heterogeneous multi-reference alignment (arXiv 1710.02590, 1707.00943) — mixtures from moments of
  invariants; discrete tomography (switching components); Rényi 1952 / Heppes 1956; Jackson–Jordán 2005.

Search log (2026-11-26; all queries generic; none contains a name, file or text of this programme):
(1) "Globally rigid graphs are fully reconstructible" Garamvölgyi Gortler Jordán arXiv; (2) Gortler Healy Thurston
"Characterizing generic global rigidity" arXiv generic frameworks globally rigid or none; (3) identifiability of a
mixture of point configurations from pairwise distance distributions rigidity theory; (4) unassigned distance
geometry problem multiple conformations mixture of structures unlabeled distances uniqueness; (5) multiple source
localization unlabeled distance measurements ghost sources uniqueness generic "data association" algebraic
rigidity; (6) echo sorting Euclidean distance matrix rank test unlabeled echoes "with probability 1" room shape
microphones theorem; (7) "unlabeled principal component analysis" Yao Peng Tsakiris theorem generic matrix
permuting entries each column rank unique up to row permutation; (8) conformational ensemble from DEER distance
distributions uniqueness identifiability "distance distributions" mixture of conformers non-uniqueness theorem;
(9) turnpike problem beltway problem reconstruct point set from multiset of pairwise distances generic uniqueness
homometric sets survey; (10) heterogeneous multi-reference alignment mixture of K signals generic identifiability
from invariant moments "estimation under group actions" orbits; (11) marginal pairwise distance distributions do
not determine joint conformational ensemble correlations between distances "three spin" OR "multi-spin" DEER
correlated distance distributions; (12) discrete tomography switching components finite point set determined by
X-rays coordinate projections on algebraic variety Rényi Heppes generalization; (13) algebraic matroid of an
irreducible variety connected if and only if variety is not a product of coordinate projections direct sum;
(14) reconstructing several point configurations simultaneously from mixed pairwise distances "partially
labeled" distances generic rigidity matroid connected [extended mode]; (15) "k-atomic" distribution uniquely
determined by its first 2k-1 moments among k-atomic distributions; first 2k moments among all distributions;
Gauss quadrature moment matching mixtures Lindsay; (16) "universally rigid" framework positive semidefinite stress
matrix "conic at infinity" affine motions super stable Connelly theorem; (17) "mixture of frameworks" OR
"ensemble of frameworks" rigidity "edge length distributions" identifiability global rigidity; (18) secant
variety of measurement variety Cayley-Menger identifiability mixture of Euclidean distance matrices sum of K
distance matrices generic uniqueness.  No search returned a theorem on mixtures of frameworks from per-edge
laws.  **"Not found" is the result of eighteen searches in one session, not a proof of novelty**; in particular
the localisation and array-processing literatures (data association, pairing in multidimensional harmonic
retrieval) were only touched.

## 7. Requests to the Ensemble division (can be sent as they stand)

1. **E1.3.**  State the configuration space in Corollary E1.3(b) and in the message ("on the free configuration
   space `(ℝ^d)^N`"), delete "determine nothing", and check Proposition A of this report (fixed lengths on a set
   of pairs whose directions are not on a conic at infinity ⇒ every affinely spanning conformation is determined
   by the mean squared distances of all pairs, with certificate `‖P^⊥ b(p)‖²`).  If you agree, Part III is its
   case `d = 1`, and the question "how many conformers do mean squared distances resolve on a chain with fixed
   bond lengths in `ℝ^d`" is the `d`-dimensional version of your Problem O1; T6(d) of this report is a first
   numerical data point (two conformers, plane: identified from seven bonds on).
2. **"Generic".**  Write "jointly generic" wherever E7/E8 are quoted without the definition (message, summary
   table, §5), and add Examples D1 and D2 as the non-generic cases with a failing conclusion.  Withdraw, or
   label as a question, "the relevant matroid is then a contraction" in §8: Example D2 is a generically globally
   rigid graph on which two conformers sharing a triangle are not determined.
3. **Stability.**  Add Proposition B (or your own version) after E7 and define the chimera gap and the switching
   gap in O4; report the gap of your own numerical examples.  For E8, state that the certificate is not sharp
   and that the bridge of §5 item 1 does not apply to Part II.
4. **Novelty labels.**  In `THEOREM_REGISTER.md`: E5(a) "elementary; formulation", E7 "corollary of the cited
   2022 theorem; reading not found", E8 "classical per-edge certificate plus E7"; mention that the published
   proof of the cited Theorem 3.5 splices `p` and `2p` along a separator.  Rephrase the headline as an
   implication.
5. **A sharper positive statement you already have.**  State E6 for rigidity: *on any graph with connected
   `d`-dimensional rigidity matroid, a jointly generic finite ensemble is determined up to replacing each conformer
   by an equivalent framework*; E7 is the globally rigid case, and for `d ≥ 2` the class is strictly larger (two
   `K_4` glued along an edge).  Add the full dichotomy: not generically globally rigid ⇒ no generic finite
   ensemble is determined.
6. **E5 on varieties.**  State E5/E6 for a rational map on an irreducible real variety (the proof is unchanged)
   before §5 item 4 uses it for torsion angles; say that "generic" then refers to that variety.
7. **Counts.**  In E8 and O5: redundant edges need no moments; `2K − 1` moments per edge suffice among ensembles
   with at most `K` conformers; for one conformation of a framework with a positive semidefinite stress matrix of
   maximal rank, `|E| + d(d+1)/2` means suffice (Proposition C here).
8. **Your numerical checks** — see §4 of this report for what the re-run showed.

## 8. What I did not check; my own errors; files

**Not checked.**
* Anything in dimension `d ≥ 3` numerically (all my tests are planar); `d = 1` only by hand.
* E1–E4, Part III, E8.1, the Lean files, and `exposedness_checks.py` / `pair_capacity_checks.py` beyond re-running
  them (not my object).
* The original papers: every source was read through a fetch tool that returns a model-written extraction; the
  quotations of Theorem 3.5 and of Corollary 1.15 are as returned by that tool.  Jackson–Jordán 2005, Rényi 1952,
  Heppes 1956, Lindsay 1989, Connelly, Gortler–Thurston were not opened.
* Propositions A, B, C and the examples are paper proofs of mine, checked numerically in the plane (A, C) or in
  exact arithmetic (D1); none is machine-checked, none has been read by anyone else.  The genericity argument
  of D1 (transcendence degree of the second kite) is not checked by computer algebra.
* The adversary of T4 is a lower bound of the worst case (finite candidate set); I did not compute the optimal
  certificate, so the true tolerated error lies between the two columns of the T4 table.
* The EXACT method was validated on planted realisable vectors only; near-tangent circles could in principle
  hide a realisation (none of 12 800 planted vectors in T2 was missed).
* T6(d) is numerical (plane, unit bonds, 12 pairs per bond count); for 7 and 8 bonds the list of chains
  `x_1A_1 + x_2A_2` comes from a local search with a passed control, not from an exhaustive method.
* Whether a statement like E7 exists in the localisation / array-processing literature under another name (§6).

**My own errors** (all in `NOTES.md` with clock times).
1. The first LM smoke test (6 starts) missed 13 of 400 planted realisable targets; caught by my own control
   before any run was cited; remedy: more starts and a second, exhaustive method.
2. The LM "found" threshold `10⁻⁶`, fixed before the runs, was too loose for the wheel on six vertices with three
   conformers: it was crossed once by a positive minimum (`7.9·10⁻⁷`).  The log keeps the count "1"; the
   follow-up is reported with it.
3. A column-generation variant of T4 was started without a cost estimate, ran past the 10-minute tool limit and
   was stopped; nothing of it is cited.
4. `t4b_w5_followup.py` crashed on a coding error at its first run (`not_cited/`); fixed and re-run.
5. `t6_e13_reading.py` run 1: estimated 5 minutes, stopped by me at 19 minutes (`not_cited/`); its part (d) was
   split into short runs.
6. I wrote numbers into this report (M3, the sentence on chains with eight bonds, two sentences of §3) before the
   complete tables existed; four of them were wrong or unsupported ("moments change by up to 21 %" — up to a
   relative `5.4`; "changed by less than a factor 1.6" — up to `2.6`; "every graph tested except `K_6`" — also not
   `K_5`; "identified from eight bonds on" — from seven) and were corrected from the logs by scripts
   (`summarize_t4.py`, `summarize_t5.py`).
7. Item m2 and my notes of 17:04Z said that for two conformers a colouring *and its complement* are needed to
   break identification; that is sufficient, not necessary.  Corrected at 18:11Z, after the coordinator's note
   on version 2 made me re-read the item (so the corrected formulation is not independent of their review).
8. Two clock times in `NOTES.md` were written a minute ahead of the clock and corrected.

**Files** (all under `experiments/science/ws_R21/` unless a path is given).
`NOTES.md` (log with clock times); `r21_common.py`; `t1_graphs.py`; `t2_chimera_search.py`, `run_t2_A.sh`,
`run_t2_B.sh`; `t2b_w6_followup.py`; `t3_controls.py`; `t4_certificate.py`, `run_t4.sh`, `summarize_t4.py`;
`t4b_w5_followup.py`; `t5_gap_scaling.py`, `run_t5_C.sh`, `run_t5_D.sh`, `summarize_t5.py`; `t5b_w6_followup.py`;
`t6_e13_reading.py`, `t6d_two_conformer_chains.py`, `t7_fewer_means.py`, `run_t7_t6.sh`;
`rerun_seed_sensitivity.py`; `logs/` (every log cited reached its last line); `not_cited/` (two logs: one crashed
run, one stopped run); `rerun_copy/` (their five scripts, their `output.txt` as `output_theirs_a570520.txt`, and
the `output.txt` of my re-run; not to be committed); `report_part_*.md` (drafts of sections of this report);
and this report, `docs/science/workstreams/R21_REPORT.md`.
