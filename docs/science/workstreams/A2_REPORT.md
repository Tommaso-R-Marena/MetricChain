# Workstream A2 — prior art and originality: certificate kernels, certification geometry, chains

Science division, MetricChain.  Author: workstream A2 (independent researcher).  Date: 2026-11-25.
Repository read at the theory head `5ed4072`.  Working files, scripts and the running notes with the complete
search log: `experiments/science/ws_A2/` (`NOTES.md`, `homometry_saw.py`, `torsion_checks.py`,
`lever_constant.py`, `scattering_bound.py`, outputs `out_*.txt`).

Reading-level tags (COMMON rule 5): `[full text]` = I read the passages quoted in the paper's own text (usually
a downloaded PDF converted with `pdftotext`; the parts read are named); `[abstract]`; `[fetch-tool]` = read
through an automated fetch-and-answer tool, quotations short; `[search snippet]`; `[from memory — unverified]`.
Epistemic labels (rule 6): **[V]** machine-checked in the repository, **[P]** paper proof given here,
**[K]** known and cited, **[N]** numerical evidence, **[C]** conjecture, **[H]** heuristic.
"Not found" always means: not found by the searches of §4, not "new".

---

## 1. Verdicts in one paragraph

**Kernels (E1, D3, D4).**  As of 2026-11-25 I still find no proof logging and no verified checker for
cost-function networks / weighted CSP / MAP lower bounds or dead-end elimination (eleven searches, the arXiv API,
the toulbar2 1.0.0 user guide read today, a code search of the toulbar2 repository): the repository's sentence
about E1 **stands**.  But the sentence "verified checkers exist for exact model counting only" (D3) is **false
as a description of the field**: a formally verified checker for *approximate* (PAC) model counting exists since
2024 (Tan–Yang–Soos–Myreen–Meel), formally verified *enumeration* proofs since 2026 (McCreesh–Nordström–Oertel–
Tan), and a two-sided certificate scheme with pruning for a weighted count (stochastic SAT) since 2024
(Cheng–Luo–Jiang); and the "native witness / checking cost" argument for E1 is weaker than written, because
formally verified pseudo-Boolean optimisation, *including LP bounds with Farkas certificates*, now checks within
a factor 20 of solving time (median 1.4; Koops et al. 2025) and certificates in the form of sequences of
equivalence-preserving transformations with a checker exist for MaxSAT (Py–Cherif–Habet 2022).  What I found no
counterpart of anywhere in proof logging is a certificate that is valid **for every member of an uncertainty
class** (the residual kernel) and a deterministic two-sided kernel for **weighted sums with a thermal prune
rule**.  **Certification geometry (G1, G4, G7).**  No prior art from 2022–2026 changes the verdicts of `L4`/`L6`;
the attribution of the finite-temperature exponent to Merhav (2011) is now verified in the full text (it is an
example in his §4, eq. (37), not a numbered theorem).  **Normal form (G13).**  A reformulation of a classical
correspondence that the repository does not name: for symmetric `d` the reduced envelope is a *weightable
quasi-metric* (Matthews; Künzi–Vajner) with weight `−2f^d`, i.e. a partial metric whose self-distance is the
regularised known part.  **Lever arm (G16).**  The law itself is immediate from classical formulas and its
weighted-`ℓ¹` displacement form is a standard *certificate* in robot motion planning (Schwarzer–Saha–Latombe
2005, Lemma 2); the consequences for certification were not found.  I replicated the exponent `3/2` with own
code and find the sharp asymptotic constant `2√2/3 = 0.943` at the central torsion (the report states `≥ 0.824`).
**[Note added at checkpoint 38 — this sentence is wrong as a claim of sharpening: the theory division's workstream G report, §2.1(c)–(d), has the bound, its proof, the extremal arm and the general constant `(2/√3) sin(δ/2) sin(θ/2)`, of which `0.824` and `0.943` are the values at two parameter sets.  Corrections: SCI-RES-0007 §2, SCI-REV-0009 §2; `DEAD_ENDS.md` SD38.]**
**Profile classes (G19).**  The profile envelope is, up to normalisation, the *second lower bound of the
Gromov–Wasserstein distance* (Mémoli 2011) — the Wasserstein distance between global distance distributions —
whose zero set is exactly Patterson homometry.  What the literature answers about identifiability: generic
uniqueness (Boutin–Kemper 2004), local uniqueness at every spanning configuration, and counterexamples; what it
does **not** answer is everything that matters for chains — the generic test vanishes identically when two
distances coincide (their Lemma 1.8), which is always the case for chains with equal bond lengths and for
lattice chains.  By exhaustive enumeration I find non-congruent lattice chains with *identical complete distance
multisets* already at 6 beads (square lattice), and 19 % of all site sets of 9-bead chains on the cubic lattice
are homometric to another one.  New here: the Debye scattering intensity at wave number `q` lies in the
pair-additive Lipschitz class with `L = q²/6` per pair, so the profile envelope bounds what orientationally
averaged scattering can distinguish (Proposition A2.1, proved and checked).  **Limit shape (G24).**  "Fekete's
lemma for sets" is the approximate-semigroup form of a classical fact (the Newton–Okounkov body of a graded
semigroup of lattice points: Khovanskii; Kaveh–Khovanskii 2012, whose approximation theorem is *stronger* for
exact semigroups); the limit shape is **not** a rotation set of a subshift of finite type with a locally
constant potential (those are polytopes attained at rate `1/N`, which the `N^{-1/3}` law excludes); half of the
surface law (the bound on second-neighbour pairs) is implied, with a better constant, by Bezdek's theorem on
contact numbers of lattice sphere packings (2012); and the abstract hypotheses give more than is stated — an
`O(N^{-1/2})` filling rate at interior points (Proposition A2.2).  **C4.**  Still not found as a bound on the
Kabsch cost of a torsion move; the closed form is the planar weighted Procrustes residual; replicated
numerically (20 000 instances, no violation).

Classifications (one per claim, from the brief's list):

| claim | classification | change relative to the repository's own assessment |
|---|---|---|
| E1 pairwise kernel + DEE, machine-checked | **plausibly original capability** (narrow: nativeness and Lean 4; every rule is known) | gap statement stands; supporting argument about checking cost must be weakened |
| E1 residual kernel (valid for a whole envelope class with anchors) | **plausibly original capability** | stated too modestly: no proof-logging system certifies statements about classes of instances |
| D3 partition-function kernel (leaf / branch / thermal prune / cut / elimination) | **new combination** (rules individually known; a verified two-sided checker for weighted sums not found) | the sentence "exact model counting only" is wrong and must go |
| D1 thermal prune as a certificate rule | **unresolved** (not re-searched by me; `L1`: inequality folklore, rule not found) | unchanged |
| D4 voxel-integral enclosures in a provable pipeline | **plausibly original capability** (elementary mathematics) | unchanged; "provable" in the OSPREY literature means a paper proof relative to the model, floating point not discussed |
| G1 certificates = coverings in the slack quasi-metric | **reformulation** | unchanged |
| G4 dichotomy and rate–distortion exponent on product landscapes | **plausibly original theorem** (an application of type covering) | unchanged |
| G7 finite-temperature exponent | **known special case** for the formula (Merhav 2011, §4); **plausibly original** identification with certificate size | attribution upgraded to "full text read" |
| G13 normal form | **reformulation** of the weightable-quasi-metric / partial-metric correspondence; the certificate statement not found | name the classical structure |
| G16 lever-arm law (Thm 11.36) | **known special case** (immediate from reduced moments of inertia; standard in robotics) | "law" should not be presented as a finding |
| G16 consequences for certification (Thms 11.37–11.38) | **plausibly original theorem** (application of G4-type bounds) | unchanged |
| G19 linear classes | **established prior art** | unchanged |
| G19 profile envelope as a transport distance | **reformulation** of a named object (Gromov–Wasserstein second lower bound) | name it; the kernel/zero-set literature must be cited |
| G19 consequences for certificates; linear kernel | **new combination** | unchanged ("none of it is deep" is fair) |
| G24 Fekete's lemma for sets | **known special case / reformulation** (Newton–Okounkov bodies; one-variable version in Janse van Rensburg) | cite; the classical theorem is stronger for exact semigroups |
| G24 limit shape of diamond-lattice bridges, outer polytopes, numbers | **plausibly original generalisation** (application of two known methods to a new object) | unchanged; one constant improvable from the literature |
| G24 stability of covering numbers | **unresolved** (elementary; not found) | unchanged |
| C4 finite-angle closed form as a bound on the Kabsch cost; chained bound | **plausibly original theorem** (elementary), medium confidence | unchanged; the unsuperposed chained bound is standard in motion planning |

---

## 2. Precise statements, with proofs or counterexamples

Statements A2.1–A2.6 are mine; each says what was checked.  Nothing here is machine-checked.

### A2.1 The profile envelope bounds differences of scattering intensities  [P; checked numerically]

Setting of Theorem 11.48 of the theory report with one pair type, no cutoff (`S_c = ∞`), squared distances
`s_pq`.  For `N` identical point scatterers the orientationally averaged (Debye) intensity of a conformation `x`
is `I_x(q) = N + 2 Σ_{p<p'} sinc(q r_pp'(x))`, `sinc t = sin t / t`, `r = √s`.

**Proposition A2.1.**  For all conformations `x, y` with `N` beads and all `q ≥ 0`,

    |I_x(q) − I_y(q)|  ≤  (q²/3) · W(x, y),        W(x,y) = Σ_k |s^x_(k) − s^y_(k)|

(sorted squared distances of the `C(N,2)` unordered pairs), i.e. `W = d_P(x,y)/L` in the notation of Theorem
11.48(b).  Equivalently: for every fixed `q` the functional `x ↦ ½(I_x(q) − N)` is a member of the pair-additive
class of Theorem 11.48 with radial function `φ_q(s) = sinc(q√s)`, whose Lipschitz constant in `s` is exactly
`q²/6`.  With scattering lengths `f_p` the same holds per pair type `(f_p f_p')`.

*Proof.*  `d/ds sinc(q√s) = (q²/2)·(t cos t − sin t)/t³` with `t = q√s`, and `|sin t − t cos t| ≤ t³/3` for
`t ≥ 0`, because the derivative of `sin t − t cos t` is `t sin t` and `|t sin t| ≤ t²` (the constant `1/3` is
attained as `t → 0`; checked numerically on `(0, 60]`).  The sum over pairs is invariant under permutations of
the pairs, so pair the sorted lists and apply the Lipschitz bound termwise.  ∎

*Consequences* **[P]**.  (i) Two conformations with equal (untruncated) profiles have identical scattering
curves at every `q` — the classical statement that scattering sees only the pair-distance distribution; the
fibres of the full profile map are exactly the sets of conformations that no orientationally averaged
scattering experiment (kinematic approximation, `q`-independent form factors) can tell apart.  (ii) Conversely a
profile distance `W` cannot produce an intensity difference larger than `q²W/3`; the bound is attained to within
`2·10⁻⁴` in the numerics (small `q`: it is the Guinier regime, `I(q) ≈ N² − (q²/3)Σ_{p<p'} s_pp'`, and
`|Σ s^x − Σ s^y| ≤ W`).  (iii) *Scope.*  This is a statement about one conformation, not about an ensemble
average; for an ensemble the intensity is the Gibbs average of a member of the class, to which the theory
report's results on Boltzmann averages (Theorem 11.34) apply, not Theorem 11.48.  It uses squared distances and
no cutoff; with a cutoff `S_c` the truncated profile is not what a scattering experiment measures.

*Numerics.*  `scattering_bound.py`: 4 000 pairs of freely jointed chains, `4 ≤ N < 40`, six values of `q` in
`[0.05, 5]`: no violation, largest ratio `0.9998`; the 6-bead homometric pair of A2.6 has `I_A ≡ I_B` on a grid
of 500 values of `q`.

### A2.2 Interior points of a set-valued Fekete limit are approached at rate `M^{-1/2}`  [P; not checked numerically]

Setting of the proof of Theorem 11.69: non-empty `Q_M ⊂ ℝ^d` with (C) `∀q₁ ∈ Q_{M₁}, q₂ ∈ Q_{M₂} ∃q ∈ Q_{M₁+M₂}:
|q − q₁ − q₂| ≤ β`; (E) `∀q ∈ Q_M ∃q′ ∈ Q_{M+1}: |q′ − q| ≤ β′`; (B) `|q| ≤ RM`; `E_M = Q_M/M → K`.

**Proposition A2.2.**  Let `p` be an interior point of `K`.  There are `M₀(p)` and a constant
`c = 2√(β(d+1)(β′+R))` such that `dist(p, E_M) ≤ c·M^{-1/2}` for all `M ≥ M₀(p)`; `M₀` can be chosen uniformly on
compact subsets of the interior.  For the bridges of Theorem 11.69 (`β = 60`, `β′ = 28`, `R = 36`, `d = 4`,
`M = N + 3`, norm `‖·‖_c + |g|`): `c ≈ 277`.

*Proof.*  Fix a simplex with vertices `w₀,…,w_d ∈ K` that contains a ball around `p`.  Since `E_m → K` in the
Hausdorff metric, for all `m ≥ m₀(p)` there are `v_i = q_i/m ∈ E_m` so close to `w_i` that `p = Σ λ_i v_i` with
`λ_i ≥ 0`, `Σλ_i = 1`.  For `M ≥ (d+1)m` put `k_i = ⌊λ_i M/m⌋`.  Concatenating `k_i` copies of each `q_i` by (C)
gives a point of `Q_{M′}`, `M′ = mΣk_i ≥ M − (d+1)m`, within `β(Σk_i − 1)` of `Σ k_i q_i`; (E) applied `M − M′`
times gives `q′ ∈ Q_M` within a further `(d+1)mβ′`.  Since `|k_i m/M − λ_i| ≤ m/M` and `|v_i| ≤ R`,

    |q′/M − p|  ≤  β/m + (d+1)(β′ + R)·m/M .

Choose `m = max(m₀(p), ⌈√(βM/((d+1)(β′+R)))⌉)`; for `M ≥ (d+1)(β′+R)m₀²/β` the bound is `≤ c·M^{-1/2}` up to
rounding.  ∎

*Reading.*  Theorem 11.69 states only the one-sided rate `168/(N+3)` and says that "nothing in this argument says
how fast they fill it".  The same hypotheses do say something: the slow rate `N^{-1/3}` of Proposition 11.73 is a
**boundary** effect (it is proved at the crystal vertex, an extreme point); in the interior the finite profile
sets fill the limit shape at least at rate `N^{-1/2}`.  For an *exact* semigroup (`β = 0`, integer points) the
classical statement is stronger still: every lattice point of the group generated by the semigroup that lies in
a closed cone interior to the cone of the semigroup, far enough from the origin, is attained (Kaveh–Khovanskii
2012, Theorem 1.6 **[K, full text of the statement]**), i.e. rate `1/M` in the interior.  Whether the bridge
statistics can be re-bookkept as an exact semigroup (constant, not merely bounded, concatenation error) is open;
see §6.  `M₀(p)` is not effective here: it depends on how fast `E_m` approaches `K` near the vertices of the
simplex.  For certificate sizes the relevant consequence is qualitative: the accuracy shift `(2L+e)d_N` of
Theorem 11.71(a) is dominated by a neighbourhood of the compact end of the shape.

### A2.3 Half of the surface law is in the sphere-packing literature, with a better constant  [P from K]

**Proposition A2.3.**  For every finite set `S` of `N ≥ 2` sites of the diamond lattice,
`e₈(S) < 6N − 3.665·N^{2/3}`; if `S` is the site set of a walk, `e₈(S) < 6N − 4.617·N^{2/3} + 3.1`.
(Proposition 11.73 of the theory report has `e₈(S) ≤ 6N − 3N^{2/3}`.)

*Proof.*  Two sites of the diamond lattice (bond vectors `±(1,1,1), ±(1,−1,−1), …`) are at squared distance 8
iff they belong to the same face-centred cubic sublattice and are nearest neighbours in it (differences inside
a sublattice have even coordinates, of squared length `8, 16, 24, …`; differences between the sublattices have
odd coordinates, squared length `3, 11, 19, …`).  Hence `e₈(S) = C_fcc(S_A) + C_fcc(S_B)`, the contact numbers of
the two parts as finite subsets of a lattice sphere packing.  Bezdek (2012), Theorem 1.1(ii)
**[K, full text of the statement]**: for every lattice `Λ ⊂ E³` with shortest vector 2,
`C_Λ(n) < 6n − (3·(18π)^{1/3}/π)·n^{2/3} = 6n − 3.665…n^{2/3}` for all `n ≥ 2`.  Subadditivity of `t ↦ t^{2/3}`
gives the first claim (a part with at most one point has no contact, and `0 ≤ 6n − 3.665n^{2/3}` for
`n ∈ {0, 1}`).  Along a walk the sublattices alternate, so `|S_A|, |S_B| ≥ (N−1)/2`, and
`2·3.665·((N−1)/2)^{2/3} = 4.617·(N−1)^{2/3} ≥ 4.617·N^{2/3} − 3.1` (mean value theorem).  ∎

*Consequence* **[P]**.  With `e₃(S) ≤ 2N − 2^{-2/3}N^{2/3}` (the report's own Loomis–Whitney bound, not re-derived
by me) the surface law becomes `‖N^x‖₁ = 9h₃ + 4h₈ + h₁₁ ≤ 35N − (9·2^{-2/3} + 4·4.617)N^{2/3} + O(1) = 35N −
24.1·N^{2/3} + O(1)` for walks: the proved constant of "`max‖N^x‖₁/N = 35(1 − k_N N^{-1/3})`" improves from
`k ≥ 0.50` to `k ≥ 0.69` (the exact data have `1.71 ≤ k_N ≤ 1.86`).  Not checked numerically by me beyond the
arithmetic.  Bezdek's Theorem 1.1(iii), `C_fcc(n) > 6n − 486^{1/3}n^{2/3}` for octahedral numbers `n`, shows that
the order `N^{2/3}` of this term is sharp.

### A2.4 The normal form is the weightable-quasi-metric correspondence  [P, one line; K for the correspondence]

For a symmetric envelope `d` and the Pasch–Hausdorff envelope `f^d` of the known part, the reduced envelope of
Theorem 11.29, `σ(a,y) = d(a,y) + f^d(a) − f^d(y)`, satisfies `σ(a,y) + w(a) = σ(y,a) + w(y)` with
`w = −2f^d + const`.  A quasi-(semi)metric with this property is called **weightable** (Matthews; Künzi–Vajner
1994; definition read in Deza–Deza–Vidali 2011 **[K, full text of §§1–2]**: "A quasi-semimetric `f` is weightable
if there exist a (weight) function `w` … such that `f_ij + w_i = f_ji + w_j`"), and weightable quasi-semimetrics
correspond bijectively and linearly to weighted semimetrics by their map `Q`: `q_ij = (D_ij − w_i + w_j)/2`,
`D_ij = q_ij + q_ji`.  Here `σ = 2q` with `D = 2d`; their "down-weighted" condition `D_ij ≥ w_i − w_j` is exactly
"`f^d` is 1-Lipschitz for `d`", which is what makes `σ ≥ 0` (`reduce_phEnv_nonneg`).  Through the companion map
`P` the same data are a *partial metric* `p(a,y) = d(a,y) − f^d(a) − f^d(y) + const` whose self-distance is
`−2f^d + const`.  So Theorem 11.29(b)–(d) reads: *certification with a symmetric envelope and a known part is
certification without a known part on a weightable quasi-metric space; the weight is (minus twice) the
regularised known part.*  For an asymmetric `d` the reduction adds an exact (gradient) term to the
antisymmetric part of `d`.  The continuous analogue is a Randers-type distance `α + df` with an exact one-form
(`d_F(x,y) = d_α(x,y) + f(y) − f(x)`: same geodesics, same symmetrised distance **[search snippet for the
geodesic statement; the formula is the integral of `df` along a curve]**).  What I did not find in that
literature is the certificate statement itself (`isValueCertificate_iff_normalForm`).

### A2.5 The limit shape is not a rotation set of a subshift of finite type with a locally constant potential  [P from K and from the report's Proposition 11.73]

For a transitive subshift of finite type and a vector potential that is constant on cylinders of length two,
the rotation set `{∫Φ dμ}` is a polytope whose vertices are the averages over elementary periodic orbits
(Ziemian 1995, as reported by Kucherenko–Wolf **[K: abstract and introduction of Kucherenko–Wolf read; Ziemian
not read]**); hence every exposed face contains a point that finite orbit segments reach exactly along
multiples of a period, and within `O(1/N)` for all `N`: the maximum of any linear functional over the
finite-length averages is within `O(1/N)` of its maximum over the rotation set.  By Proposition 11.73 the
functional `9p₃ + 4p₈ + p₁₁`, whose maximum over `K^{br}` is 35 (crystal vertex), stays below
`35 − 17.6·N^{-1/3} + 17/N` on the profile densities of all walks and bridges with `N` beads.  So
`K^{br}` is not such a rotation set in any coding in which chain length is orbit length.  The reason is visible
in Lemma 11.67: in sequence coordinates the profile is a *long-range, superadditive* observable (contacts
between beads far apart along the chain), additive only across bridge junctions; in space coordinates it is a
local observable of a lattice gas, and the limit shape is a set of mean values of a local vector observable
over finite configurations with a connectivity constraint.  What survives of the rotation-set picture is the
general fact that the set of invariant-measure averages of a continuous vector observable is compact and
convex ("easy to see", Kucherenko–Wolf) and equals the set of limits of finite-orbit averages under
specification; bridges are what supplies a specification-like gluing property.  The answer to the brief's
question "is the limit shape just a rotation set — if so, name the theorem" is therefore: **no for the classical
(finite-range) theory; the theorem to name for the mechanism is the Newton–Okounkov body of a graded semigroup**
(§4.6).

### A2.6 Lattice chains are not identifiable from their complete distance distribution  [N, exhaustive; smallest example checked by hand]

**Counterexample.**  On the square lattice the 6-bead chains with site sets

    A = {(0,0),(0,1),(0,2),(1,2),(1,3),(2,3)},     B = {(0,0),(0,1),(1,1),(1,2),(1,3),(2,3)}

have the same multiset of all 15 squared pair distances, `1⁵ 2³ 4¹ 5³ 8¹ 10¹ 13¹`, and are not congruent (the
collinear triple of `A` is at an end of the staircase, that of `B` in the middle).  Six beads is the smallest
size at which this happens on the square lattice, and on the cubic lattice.

**Counts** (own exhaustive enumeration; classes up to the point group of the lattice *including reflections*
and translations; a "homometric group" is a set of ≥ 2 pairwise non-congruent site sets with equal complete
distance multisets):

| lattice | beads | walk classes | site sets | distinct complete distance multisets | homometric groups | truncated profiles, `S_c = 5`, pairs with chain separation ≥ 3 |
|---|---|---|---|---|---|---|
| `ℤ²` | 6 | 36 | 18 | 17 | 1 | 9 |
| `ℤ²` | 10 | 2 034 | 781 | 744 | 34 | 73 |
| `ℤ²` | 14 | 110 188 | 39 592 | 39 036 | 536 | 295 |
| `ℤ²` | 15 | 296 806 | 106 630 | 105 971 | 649 (1 308 site sets) | 376 |
| `ℤ²` | 16 | 802 075 | 283 409 | 281 086 | 2 252 (4 575 site sets) | 507 (541 with all pairs) |
| `ℤ³` | 6 | 92 | 47 | 43 | 4 | 22 |
| `ℤ³` | 8 | 1 832 | 768 | 679 | 69 | 138 |
| `ℤ³` | 9 | 8 453 | 3 411 | 3 047 | 276 (640 site sets = 19 %) | 285 |

Three layers of non-identifiability are thus separated: (1) *labels*: different chains through the same site
set (factor `W/S ≈ 2.5–2.8`); (2) *homometry*: non-congruent site sets with all distances equal — on `ℤ²` a
fraction of the site sets that decreases with the length (11, 10, 9, 6, 3, 2 % at 6, 8, 10, 12, 14, 16 beads;
3, 3, 2, 1 % at 9, 11, 13, 15), on `ℤ³` a fraction that does not (17, 14, 21, 19 % at 6, 7, 8, 9 beads);
(3) *truncation and counting*: the profile of the theory report keeps only the numbers of pairs below a cutoff,
and then `8 453` conformations share `285` profiles (`ℤ³`, 9 beads) and `802 075` share `507` (`ℤ²`, 16 beads).  Mirror images are identified
throughout (no distance data can separate them).  The generic-uniqueness theorem of Boutin–Kemper does not
contradict this: its hypothesis fails for every configuration with two equal distances (§4.5).

---

## 3. Numerics (what, sizes, results, how to re-run)

All scripts are mine, in `experiments/science/ws_A2/`, pure Python + numpy; nothing is imported from the
repository.  "Independent replication" below means: re-computed with this code.

| script | what | sizes | result | CPU time |
|---|---|---|---|---|
| `homometry_saw.py 2 14 5`, `… 2 16 5 15`, `… 3 9 5` | exhaustive enumeration of self-avoiding walks on `ℤ²`, `ℤ³` up to lattice symmetries (reflections included); site sets; complete squared-distance multisets; truncated profiles | `ℤ²`: 4–16 beads (1 604 149 walks with fixed first step at 16); `ℤ³`: 4–9 beads (64 661) | table in A2.6; first homometric pair at 6 beads; sanity: 5 and 6 walk classes at 4 beads (Burnside), 802 075 at 16 beads | 70 s (`ℤ²`, ≤ 14), ≈ 15 min and 2 GB (15 and 16), 42 s (`ℤ³`) |
| `torsion_checks.py` (seed fixed) | C4: closed form vs direct minimisation over the re-superposition angle; Kabsch (proper rotation) cost vs coaxial cost; two-sided reduced-inertia bounds | 20 000 random two-body torsion moves, 1–11 atoms per side | formula = direct minimum (relative deviation `7·10⁻⁶`, grid error) `= 2(S − |I_A + I_B e^{iφ}|)`; Kabsch ≤ coaxial in all cases, largest ratio `0.9983`; bounds of Theorem 4.6(c) never violated — **independent replication of Theorem 4.6(b),(c)** (the earlier reviewer of `L3` also reports `0.998`) | 17 s |
| same | G16: `2√min(I_A,I_B)` about a torsion axis at distance `m` from the end of an all-trans tetrahedral chain; regular helices; phantom random-rotamer coils | `m = 10 … 640`, `N` up to 2003 | `value/m^{3/2} = 0.625, 0.585, 0.565, 0.554, 0.549, 0.547, 0.546`; fitted exponent `1.47 → 3/2` — **independent replication of the power in Theorem 11.36**; random coils: `2√min I ≈ 1.17·m` (median, `m = 200`) | (same run) |
| `lever_constant.py` | sup over arm orientations (three torsions next to the central bond on each side, 20° grid, all-trans arms) of `2√(2I_red)/m^{3/2}` | `m = 20, 40, 80` | `1.013, 0.978, 0.961`, attained with a gauche torsion next to the central bond; `sup I_arm/m³ → 2/9` | 80 s |
| `scattering_bound.py` | Proposition A2.1 | 4 000 pairs of chains × 6 values of `q` | no violation; max ratio `0.9998` | 5 s |

*Independent replication of a number of the theory report* **[N]**.  The 16-bead run on `ℤ²` (1 604 149 walks
with fixed first step) gives **802 075 walk classes and 541 truncated profiles at `S_c = 5`** when all pairs
`p < q` with squared distance `< 5` are counted — exactly the two numbers quoted in §11.17 from the sixth referee
("the 802 075 self-avoiding walks with 16 beads on the square lattice have 541 profiles at `S_c = 5`"); with
the convention of §11.22 (chain separation ≥ 3) there are 507.  At 16 beads there are 283 409 site sets,
281 086 complete distance multisets and 2 252 homometric groups containing 4 575 site sets (1.6 %).  Output:
`out_homometry_z2_n15_16.txt`; about 9 minutes of CPU and 2 GB for this size.

*What the lever-arm numerics add* **[N + P sketch]**.  For a chain with bond length `b` and bond angle `θ` an atom
`j` bonds away from the torsion bond is at distance at most `j·b·sin(θ/2) + O(b)` from the axis (the largest
end-to-end distance of `j` bonds, attained by the all-trans zigzag), so `I_arm ≤ (b² sin²(θ/2)/3)·m³(1 + o(1))`
`= (2/9)b²m³` for the tetrahedral angle; an all-trans arm joined through one gauche torsion is perpendicular to
the axis and attains it (numerics: `0.2264` at `m = 80`).  Hence, for uniform constants over all conformations,
`sup_x 2√(2I_red) = (2√2/3)·b·m^{3/2}(1 + o(1)) = 0.943·b m^{3/2}` at the central torsion and `(4/3)·b·m^{3/2}` for
a torsion much closer to one end than to the other.  Theorem 11.36's "`c_i ≥ 0.824·Λ b m_i^{3/2}` for every
position" is confirmed and is not sharp in the constant.  **[Note added at checkpoint 38 — "not sharp in the constant" is false: `0.824 = (2/√3) sin 60° sin 55.5°` is the limit of `c_i^ver/(Λ b m_i^{3/2})` at the report's parameters; and the `4/3` "far from the centre" above is the looser form `2√(2I_red)`, a weaker bound than theirs, not a second sharp constant.  The three-line argument and the extremal arm of this paragraph are in workstream G §2.1(c).  SCI-REV-0009 §2.]**  *A physical caveat on the word "law"* **[N for coils,
H for globules]**: `m^{3/2}` is the worst case over conformations and is forced by extended arms.  For typical
ideal-coil conformations `√I_arm ∝ m` (median `1.17·m` in my sample), and for compact conformations of radius
`∝ m^{1/3}` one expects `√I_arm ∝ m^{5/6}`.  Any positive power suffices for Theorem 11.37, so its conclusion
does not depend on this; but a statement such as "the constants grow like `m^{3/2}`" is a statement about
envelopes that must hold uniformly on a domain containing extended conformations, not about the sensitivity of
a compact state.

---

## 4. Prior art, claim by claim (with reading levels), and the search log

The complete log (40 searches S1–S40, with outcomes) is in `experiments/science/ws_A2/NOTES.md`; the table at
the end of this section lists them in abridged form.  I extend, and do not repeat, `docs/prior_art/L1…L8`.

*Exact statements and locations of the claims tested* (theory report at `5ed4072`; the kernel claims are quoted
in §4.1):

| claim | where | statement, and the repository's own novelty sentence |
|---|---|---|
| G1 | §11.2, Thms 11.3–11.5; `isCertificate_iff_cover` | `A` is a point `ε`-certificate iff every `y` has an evaluated point within slack distance `E(y) − UB(A) + ε`, `s(a,y) = d(a,y) − g(a) + g(y)`; `N_cov ≤ N_point ≤ N_cov + 1`.  "reformulation of a known notion …; the slack form with a known part and an asymmetric envelope was not found" |
| G4 | §11.4, Thms 11.7–11.9 | one evaluation certifies iff every site is sharp; otherwise `n⁻¹ ln N_cov → R* = max_P R(P; s − gap, 0)`.  "no match found; an application of the type covering lemma" |
| G7 | §11.6, Thms 11.12–11.15 | `n⁻¹ ln N_Z → R_β = max_Q R(Q; s, KL(Q‖π)/β)` for accuracies neither extensive nor exponentially small.  "the exponent formula is a corollary of Merhav's (2011) theorem …; the identification … and the one-shot converses: no match found" |
| G13 | §11.11, Thm 11.29; `isValueCertificate_iff_normalForm` | value certificates of `(d, f, g)` = point certificates of `(σ, 0, f^d + g)`, `σ` the reduced cost of `d` under the Pasch–Hausdorff envelope `f^d`.  "elementary (Johnson reweighting, min-plus adjointness); the packaging for certification apparently new" |
| G16 | §11.14, Thms 11.36–11.38 | `c_i ≥ 0.824·Λ b m_i^{3/2}`; with `c_i ≥ c₀m_i^γ` the weighted-Hamming format costs `ln N_cov ≥ n ln k − C((G+ε)/c₀)^{1/(1+γ)}`; RMSD used directly: `exp(Θ̃(√N))`.  "lever-arm effects are folklore in molecular modelling, the quantitative consequences for certification were not found (no literature search was possible in the review)" |
| G19 | §11.17, Thms 11.47–11.48, Props 11.49–11.50 | linear classes: bracket = unexplained part of the feature vector; pair-additive Lipschitz residuals: `d_P(x,y) = L Σ_τ‖N^x_τ − N^y_τ‖_{L¹}` = Wasserstein-1 distance of truncated squared-distance multisets.  "the linear theory is known …; its reading as the exact envelope of a residual class next to a known part, and the consequences for certificates, were not found; none of it is deep" |
| G24 | §11.22, Lemmas 11.67–11.68, 11.70, Thms 11.69, 11.71, Props 11.72–11.74 | normalised `(profile, #gauche)` sets of diamond-lattice bridges converge in the Hausdorff metric to a compact convex body; certificate sizes converge to its covering number; outer polytopes; `N^{-1/3}` law.  "limits of supermultiplicative models and the cluster method … are known; … the limit shape for this model, the stability lemma and the numbers were not found" |
| C4 | §4.4, Thm 4.6, Cor 4.7 | coaxial cost `2S − 2√(S² − 4I_AI_B sin²(φ/2)) ≤ 4 min(I_A,I_B) sin²(φ/2)`; chain rule.  "small-angle content classical …; finite-angle closed form and chained bound: no match found" |

### 4.1 Kernels (E1, D3, D4; theory report §0.2, §3.4, §6.1–6.4, §11.8)

*Exact statements under test.*  E1: "no *native* verified checker for cost-function-network / MAP / DEE
certificates found; such runs can in principle be encoded as pseudo-Boolean proofs and checked with existing
verified checkers, so the gap concerns native witnesses and their checking cost".  §6.4: "Neither OSPREY nor
toulbar2 emits checkable proofs, and no verified checker for cost-function-network / MAP lower bounds, DEE
steps or approximate partition-function bounds was found."  D3: "verified checkers exist for exact model
counting only; this rule set: no match found".  D4: "rigorous voxel-*integral* bounds inside a provable design
algorithm: no match found".

*What I read.*

1. **toulbar2** — user guide for version 1.0.0 `[fetch-tool, whole page in two parts, 2026-11-25]`: the only
   "certificate" is option `-x` ("read from default file "sol" taken as a certificate": an initial solution);
   no proof, VeriPB or checker option; `-logz`; `-epsilon=[float]` "approximation factor for computing the
   partition function"; `-dee` "restricted dead-end elimination".  GitHub code search of `toulbar2/toulbar2`
   for `veripb` and for `"proof log"`: 0 hits.  arXiv API, `"proof logging"` with `"cost function"`/`WCSP`/
   `"weighted constraint"`: 0 hits; `toulbar2` with `certif*`/`proof`: 0 hits; all 20 preprints matching
   `"proof logging"` listed in the notes — none on cost-function networks, MAP or partition functions.
   **Conclusion: the E1 gap statement is still true.**
2. **W. Koops, D. Le Berre, M. O. Myreen, J. Nordström, A. Oertel, Y. K. Tan, M. Vinyals, "Practically feasible
   proof logging for pseudo-Boolean optimization", CP 2025, LIPIcs 340, paper 21** `[fetch-tool: abstract in
   full, sentences of the introduction and of the experiments]`: "an efficient toolchain based on VeriPB and
   CakePB for formally verified pseudo-Boolean optimization … including core-guided search and linear
   programming integration with Farkas certificates and cut generation"; "formally verified conclusions within a
   factor 20 of the solving time"; for RoundingSat the median checking factor is 1.43, the worst 19.17.
   *Comparison.*  A local-polytope (reparameterisation) bound of a cost-function network is an LP bound of its
   0–1 encoding, i.e. exactly the kind of statement a Farkas certificate proves, and dead-end elimination has
   the form of the dominance rule of VeriPB (Bogaerts et al. 2023; described in `L1` from memory and not re-read
   by me) — both sentences are my inference, nobody has written such a proof for a cost-function network.  So
   the route "encode as pseudo-Boolean proofs" is not only possible "in principle": every ingredient has a
   formally verified checker with measured, moderate overhead.  `L1`'s "the 43-times figure … is the number to beat" (from certified
   branch-and-bound MaxSAT) is no longer the right benchmark.
3. **M. Py, M. S. Cherif, D. Habet, "Proofs and certificates for Max-SAT", J. Artif. Intell. Res. 75 (2022)
   1373–1400; extended abstract IJCAI 2023, pp. 6942–6947** `[full text of the abstract and introduction of the
   IJCAI version; the JAIR page returned an error]`: "MS-Builder … generates certificates for the Max-SAT problem
   in the particular form of a sequence of equivalence-preserving transformations"; "MS-Checker, able to verify
   the validity of any Max-SAT certificate using Max-SAT inference rules".  *Comparison.*  Max-SAT is the Boolean
   special case of a cost-function network and equivalence-preserving transformations are reparameterisations:
   the *idea* of the `leaf` rule — a reparameterisation as a native, independently checkable witness of a lower
   bound — is in print.  Not there: non-Boolean domains, branching and DEE rules in one certificate tree, a
   machine-checked soundness proof (the checker is an ordinary program).
4. **R. van Doren, T. Antonopoulos, R. Piskac, "Efficient and verifiable proof logging for MaxSAT solving",
   ASE 2025** `[full text of abstract and introduction, from the authors' PDF]`: "the first MaxSAT-specific
   proof-logging framework for core-guided OLL solvers … native inference rules for cores, cliques, hardenings,
   totalizer updates, and bound adjustments"; existing approaches "reduce MaxSAT reasoning to heavyweight
   pseudo-Boolean proofs"; "median verification overhead under 2% of solve time".  No proof assistant is
   mentioned.  *Comparison.*  Same motivation as the repository's "native" kernels (avoid the pseudo-Boolean
   detour), another problem class, unverified checker.
5. **C. McCreesh, J. Nordström, A. Oertel, Y. K. Tan, "Proof logging for projected enumeration (and counting?)
   problems in VeriPB", CP 2026, LIPIcs 379, 43:1–43:21** `[full text: abstract, §1, start of §2 and §4, §5,
   references]`: VeriPB and "the formally verified CakePB backend" extended to solution enumeration with
   projection; `output EQUIENUMERABLE` for count-preserving transformations; efficient counting proofs are a
   "future possibility"; "specialised certification methods are available for both exact [18] and approximate
   [55] model counting".
6. **Y. K. Tan, J. Yang, M. Soos, M. O. Myreen, K. S. Meel, "Formally certified approximate model counting",
   CAV 2024, LNCS 14681, 153–177 (arXiv:2406.11414)** `[abstract in full, from the arXiv PDF]`: "the first
   certification framework for approximate model counting with formally verified guarantees on the quality of
   its output approximation … (i) a static, once-off, formal proof of the algorithm's PAC guarantee in the
   Isabelle/HOL proof assistant; and (ii) dynamic, per-run, verification of ApproxMC's calls to an external
   CNF-XOR solver using proof certificates"; 84.7 % of instances fully certified.  *Comparison with D3.*
   Unweighted counts, probabilistic `(ε, δ)` guarantee; the repository's kernel is deterministic and weighted.
   But the sentence "verified checkers exist for exact model counting only" is refuted by this paper.
7. **C. Cheng, Y.-R. Luo, J.-H. R. Jiang, "Knowledge compilation for incremental and checkable stochastic
   Boolean satisfiability", IJCAI 2024, pp. 1862–1872** `[full text: abstract, §1, §3.3, §4]`: "we relax the
   logical equivalence checking in CPOG into two logical implication checks to separately certify lower and
   upper bounds of SSAT satisfying probability"; pruned branches are replaced by `⊥` in a lower graph `G_l`;
   Theorem 5: `Pr[Φ] = p` if `(G_l → ϕ) ∧ (ϕ → G_u)` and both graphs evaluate to `p`; clausal proofs checked by
   `cpog-check`.  *Comparison with D3.*  The closest thing found to "a two-sided certificate for a weighted sum
   with a prune rule": two-sided, weighted (probabilities of randomised variables), pruning by dominance at
   maximisation nodes.  Different in what the prune rule is (exact dominance at `max` nodes, not a bound
   `ln(1 + e^{−βγ})` on a discarded part of a sum), in that the certified bounds are meant to coincide, and in
   the absence of a machine-checked soundness theorem for the implication variant.
8. **M. A. Hallen, B. R. Donald, "Protein design by provable algorithms", Commun. ACM 62(10) (2019)**
   `[fetch-tool, full text on PubMed Central]`: guarantees are relative to the input model ("they ensure modeling
   error is the only error in protein design calculations"); a voxel's energy is "generally the continuously
   minimized energy"; "continuous entropy" appears in a footnote only; no mention of floating-point arithmetic,
   rounding, interval arithmetic, proof assistants or independently checkable certificates.  *Answer to the
   brief's question what "provable" means there:* a theorem on paper about the algorithm (exact optimum, or an
   `ε`-approximation of a sum of Boltzmann factors of minimised energies) relative to the model, executed in
   floating point; neither a per-run certificate nor a machine-checked proof.  D4 stands as in `L2` §C8(b).
9. Interval methods for conformational energies: Lin & Stadtherr, J. Comput. Chem. 26 (2005) (interval
   branch-and-bound over dihedral angles with "a mathematical and computational guarantee") and Lavor (2003)
   `[search snippets; Lin–Stadtherr is in `L2`'s query list]`.  They supply what the theory report calls "the
   continuous leaves" (table enclosures over voxels); no checkable certificate, no partition functions.

*Hypotheses and conclusions compared.*  All proof-logging systems read above certify a statement about **one
given instance** ("this solution is optimal for this formula", "these are all solutions", "the count is
`n` / within `(1+ε)` with probability `1−δ`").  The residual kernel certifies `L ≤ E(x) + g(x)` **for every
residual `g` in an envelope class consistent with interval anchor data**, and checks non-emptiness of the class
(`verifyITop_sound`, `IProblem.consistent_iff_nonempty` **[V]**).  I found no counterpart of that quantifier in
the proof-logging literature (it is closer to robust optimisation, where certificates are dual solutions of
robust counterparts; `L5`, `L8`).  This is the most distinctive property of the kernels and the theory report
does not say so.

### 4.2 Certification geometry (G1, G4, G7; §§11.2–11.6)

`L4` and `L6` are thorough (Hansen–Jaumard–Lu; Baran–Demaine(–Katz); Bachoc–Cesari–Gerchinovitz; Bouttier et al.;
de Montbrun–Gerchinovitz; priority k-centre; Csiszár's dual; Kostina–Verdú; Merhav 2025; type covering) and my
searches for 2022–2026 follow-ups found nothing that changes them: the arXiv API returns only the 2021 paper
for `"error certificates" AND Lipschitz`, nothing for `certified` with `"Lipschitz optimization"`, the regret
papers of Gokcesu & Gokcesu (2021–22) for `Piyavskii`, and nothing that joins rate–distortion theory to query
complexity or black-box optimisation.  Two additions:

* **Merhav (2011), arXiv:1103.2882** `[full text of the abstract, of Section 4 pp. 15–17, and of the example on
  p. 22]`.  The exact statement behind G7: if a strategy `s*` satisfies (a) `ℓ(x, s*) ≤ n[λ(Q) + o(1)]` for
  every `x` in every type class `T_Q` and (b) every strategy has `ℓ ≥ n[λ(Q) − o(1)]` on a non-exponentially
  small fraction of `T_Q`, then "it is then a straightforward exercise to show, using the method of types, that
  `s*` is a universal asymptotically optimum strategy … with `E(s*, α, P) = max_Q[αλ(Q) − D(Q‖P)]`" (his eq. 37);
  the first example is fixed-rate lossy coding of a memoryless finite-alphabet source with an additive
  distortion, where `λ(Q) = D_Q(R)` "based on the type covering lemma".  The repository's attribution is
  correct; its tag "[K, not verified in detail]" (§11.6) can be replaced by "[K, the relevant section read in
  full]", and "a corollary of Merhav's (2011) theorem" should read "of an example in Merhav (2011, §4)": it is
  presented there as an exercise, not as a numbered theorem, and for exactly the hypotheses stated above.
* G1 with a known part and symmetric `d` lives on a weightable quasi-metric space (A2.4).  The asymmetric
  nearest-neighbour / similarity-search literature on such spaces (quasi-metric trees; `[search snippet]` only)
  is the natural place where a covering characterisation "with a known part" could already exist; I did not
  find one.

Classification unchanged: G1 reformulation; G4 plausibly original theorem (application of type covering);
G7 known formula, plausibly original identification.

### 4.3 Normal form (G13; §11.11)

See A2.4.  Sources: M. Deza, E. Deza, J. Vidali, "Cones of weighted and partial metrics", arXiv:1101.0517
`[full text of §§1–2]` for the definitions and the maps `P`, `Q` and for the attribution of partial metrics to
Matthews (1992); Künzi–Vajner (1994), "Weighted quasi-metrics" `[search snippet of the abstract page]`; Randers
metrics with an exact one-form `[search snippets]`.  From memory, unverified: potential-based reward shaping
(Ng–Harada–Russell 1999) is the same gauge freedom in sequential decision problems, and A* with a consistent
heuristic is Dijkstra's algorithm on reduced costs (the latter is already in the report).  The min-plus
adjointness `min(f + g) = min(f^d + g)` for `d`-Lipschitz `g` is the classical statement that the
Pasch–Hausdorff (Lipschitz) regularisation does not change infima against Lipschitz perturbations.
Classification: **reformulation**; the certificate equivalence itself not found.

### 4.4 Lever arm (G16; §11.14) and C4 (§4.4)

* **F. Schwarzer, M. Saha, J.-C. Latombe, "Adaptive dynamic collision checking for single and multiple
  articulated robots in complex environments", IEEE Trans. Robotics 21(3) (2005) 338–353** `[full text; the
  formulas are lost in text extraction, the statements were read in words]`.  Lemma 2: for a kinematic chain
  whose configuration is linearly interpolated, "an upper bound on the lengths of the curves traced by the
  points of [a link]" is `Σ_i R_i|Δq_i|`, where for a revolute joint `R_i` "is an upper bound on the distances
  between the points of [the link] and the axis of rotation of joint `i`".  The bound is used to *certify* that
  a path segment is collision-free.  *Comparison.*  This is the weighted-`ℓ¹` envelope format
  `Σ_i c_i|δ_i|` of §§4.4/11.14 with lever-arm constants, in the sup-over-atoms norm and without
  re-superposition ("the naive lever-arm bound" of §4.4), used as a certificate in another field for twenty
  years.  Not there: superposition, reduced inertia, the root-mean-square norm, growth exponents, complexity
  consequences.
* **R. Featherstone, "An empirical study of the joint space inertia matrix", Int. J. Robotics Research 23(9)
  (2004) 859–871** `[abstract only; full text not accessible]`: the joint-space inertia matrix "can be highly
  ill-conditioned", its condition number "grows anywhere from O(N) to O(N⁴) with the number of bodies", and
  this "is not merely a numerical artifact; it is symptomatic of an underlying property of the mechanism".  The
  diagonal entries of that matrix are the moments of inertia of the outboard sub-chains about the joint axes —
  the `I ∝ m³` behind Theorem 11.36 (that the paper states `m³` explicitly is `[from memory — unverified]`).
* Molecular literature: `L3` §C13 (Pitzer–Gwinn; Gō–Scheraga; Noguti–Gō; Popov–Grudinin; DiffDock) stands.
  My two further searches found no quantitative chain-length law for RMSD per unit torsion; Bastolla & Dehouck
  (J. Chem. Inf. Model. 2019) `[search snippet]` discuss the coupling of torsions qualitatively.
* C4: one further search (hinge / two rigid fragments / closed-form RMSD) found only general Kabsch and
  quaternion material.  The closed form `C(φ) = 2(S − |I_A + I_B e^{iφ}|)` is the residual of a *planar* weighted
  Procrustes problem (equivalently `2S` times the weighted circular variance of the two angles `0, φ`), which
  is classical; its use as an upper bound for the three-dimensional Kabsch cost of a torsion move, with the
  chained form, remains not found.

Classification: Theorem 11.36 **known special case** (the content is the growth of a moment of inertia; the
`3/2` for RMSD constants is immediate; replicated here); Theorems 11.37–11.38 **plausibly original** (not found;
searches thin); C4 **plausibly original theorem (elementary)**.

### 4.5 Profile classes (G19; §11.17), and identifiability of a conformation from its distance profile

*The object has a name.*  **F. Mémoli, T. Needham, "Distance distributions and inverse problems for metric
measure spaces", Studies in Applied Mathematics (2022), arXiv:1810.09646v5** `[full text: abstract, the
subsection "Global distance distributions" with the definition of `L_{H,p}`, Examples 2.2/2.5, Propositions
2.7–2.8, the opening of §3 with Theorem 4]`.  For a metric measure space `X` the global distance distribution
is `H_X(r) = μ⊗μ{(x,x′) : d(x,x′) ≤ r}`; `L_{H,p}(X,Y)` is the Wasserstein-`p` distance on the line between
`dH_X` and `dH_Y`; "these pseudometrics serve as lower bounds for Gromov–Wasserstein `p`-distances, as was shown
in [Mémoli 2011]"; Proposition 2.8: `L_{H,p} ≤ L^K_{h,p} ≤ d_{GW,p}`.  With `N` equally weighted beads, `p = 1`
and the dissimilarity `min(|x_p − x_q|², S_c)` in place of the metric (the square is not a metric; in the
variable `r = √s` one has a genuine metric and radial functions that are Lipschitz in `r`), the theory report's
`d_P` is `L·(N²/2)·L_{H,1}` per pair type (`H_X` counts ordered pairs and the diagonal): **the profile envelope
is the "second lower bound" of the Gromov–Wasserstein distance** (that name, from Mémoli 2011, is
`[from memory — unverified]`; the object and its lower-bound property are as quoted).  The repository cites
Osada et al. and the bag of bonds for "a descriptor distance" and does not mention this.  *What is and is not in
that literature:* the distance, its pseudometric property, its computation and its non-injectivity are; the
dual reading used in Theorem 11.48(b) — `d_P(x,y) = sup` over `L`-Lipschitz radial functions of the difference of
pair-additive energies — is Kantorovich–Rubinstein duality applied to `L_{H,1}` and I did not see it stated as a
statement about classes of potentials; the use next to a known part and the certificate counts are not there.

*Identifiability — what is answered.*

1. **M. Boutin, G. Kemper, "On reconstructing n-point configurations from the distribution of distances or
   areas", Adv. Appl. Math. 32 (2004) 709–735, arXiv:math/0304192** `[full text: abstract, introduction,
   Definition 1.1, Theorem 1.6 (statement), Remark 1.7, Lemma 1.8 with proof, Corollary 1.9, Propositions 1.10,
   1.12, 1.13 (statements), Corollaries 1.15–1.16; the proof of 1.6 and Part 2 not read]`.
   * Definition 1.1: an `n`-point configuration in `ℝ^m` is *reconstructible from distances* if every
     configuration with the same distribution of (squared) distances is its image under a permutation and a
     Euclidean transformation — reflections included.
   * Theorem 1.6: for `n ≤ 3` or `n ≥ m + 2` there is a non-zero polynomial `f` such that every configuration
     with `f ≠ 0` is reconstructible.
   * **Lemma 1.8: "If the pairwise distances between the `P_i`'s are not all distinct then `f(P₁,…,P_n) = 0`."**
   * Proposition 1.13: if the Gram matrix has the generic rank `min(n−1, m)` there is `ε > 0` such that every
     configuration within `ε` with the same distribution of distances is congruent to the given one.
   * Counterexamples exist for every `n ≥ 4` ("It is well known that `L_H` does not distinguish elements of
     `C_{N,k}` for any `(N,k)` with `N > 3`", Mémoli–Needham; the one-dimensional pair `{0,1,4,10,12,17}`,
     `{0,1,8,11,13,17}` is their Example 2.2).
2. **Y. Jiao, F. H. Stillinger, S. Torquato, "Geometrical ambiguity of pair statistics. I. Point
   configurations", Phys. Rev. E 81 (2010) 011105, arXiv:0908.1366** `[full text: abstract, parts of the
   introduction]`: "the pair-distance information contained in `g₂` is in general insufficient to uniquely
   determine a point configuration"; the kite and the trapezoid (four points in the plane, the same six
   distances); mirror images are counted as identical; "in general degeneracy is rare"; "no functional of
   `g₂` … can uniquely specify `g₃`".
3. **S. Gortler, L. Theran, D. Thurston, "Generic unlabeled global rigidity", Forum Math. Sigma 7 (2019) e21**
   `[abstract, fetch-tool]`: for `d ≥ 2`, a generic configuration is determined by an *unlabelled* set of
   point-pair lengths (given `d` and `n`) if and only if it is determined by the labelled ones — the result for
   a *subset* of the pairs.
4. Unassigned distance geometry (Duxbury et al., Discrete Appl. Math. 204 (2016) `[search snippet]`; Huang &
   Dokmanić, arXiv:1804.02465 `[abstract]`: turnpike and beltway problems from noisy unassigned distances): the
   algorithmic side, motivated by pair-distribution-function data of nanostructures.
5. Scattering: the measured curve is a linear functional of the pair-distance distribution; the number of
   independent parameters of a curve is finite (Shannon channels: Konarev & Svergun, IUCrJ 2 (2015) 352–360
   `[fetch-tool]`: "the number of meaningful Shannon channels … an estimate of the information content of the
   scattering data"); mirror images and all symmetry operations that leave `p(r)` unchanged are invisible
   `[search snippet]`.  The ambiguity measure of Petoukhov & Svergun (2015) I could not open
   (`[from memory — unverified]`).  Workstream M covers this literature for ensembles; A2.1 is the one statement
   I add.

*Identifiability — what is not answered there, and matters for chains.*

* **Genericity excludes chains.**  By Lemma 1.8 the Boutin–Kemper test vanishes on every configuration with
  two equal distances; Gortler–Theran–Thurston also need genericity.  A chain with equal bond lengths has
  `N − 1` equal distances by construction (and `N − 2` equal 1–3 distances if bond angles are fixed), a lattice
  chain many more.  Proposition 1.10 of Boutin–Kemper (a test relative to the symmetry group of the distance
  pattern) is the available tool; nobody seems to have applied it to chains.  A2.6 shows that the conclusion
  really fails on lattices, from 6 beads on.
* **Local uniqueness survives** (their Proposition 1.13 needs no distinctness): for the *complete, untruncated*
  distance multiset the fibres are discrete modulo congruence at every spanning conformation, also for chains.
  This is a qualitative statement; no stability estimate (how far apart in RMSD can two conformations with
  profiles at `W₁`-distance `δ` be?) was found, and A2.6 shows that globally the answer is "far".
* **A cutoff changes the question** (Observation A2.7, **[P]**, elementary, not checked numerically).  With pairs
  counted only below `S_c` — the format of Theorem 11.48 — let `C(x)` be the set of pairs of `x` below the
  cutoff.  If no squared distance of `x` equals `S_c` and the non-constant distances of the pairs in `C(x)` are
  pairwise distinct (per type), then for all conformations `y` near `x`: `profile(y) = profile(x)` iff
  `s_pq(y) = s_pq(x)` for every pair in `C(x)` (by continuity the same pairs are below the cutoff and the order of
  the distinct values is preserved).  So *locally the fibre of the truncated profile is the set of flexes of the
  contact framework* with bars `C(x)`.  Two regimes follow.  If the cutoff lies below the 1–4 distances, an
  extended chain has no variable distance below the cutoff and a whole open set of torsion space is one fibre.
  If the cutoff covers the 1–4 distances, each torsion is pinned up to sign by its own 1–4 distance, the local
  fibre is a point — but the *global* fibre of an extended conformation (no pair beyond 1–4 below the cutoff)
  contains every re-ordering and every sign change of its torsion values that stays extended: exponentially
  many conformations, far apart in RMSD, with one profile.  On the lattice of §11.22 this is the statement
  that extended conformations with equal gauche counts share a profile.  I found neither statement in the
  literature; the theory report says only that `d_P` "has large fibres".
* **Types.**  With pair types the multiset is partially labelled; I found no reconstruction theorem for
  partially labelled distance multisets.
* **Chirality** is never identifiable from distances; the report says so.

Classification: linear theory **established prior art**; transport form **reformulation of a named object**;
consequences for certificates and the linear kernel **new combination**.

### 4.6 Limit shape (G24; §11.22)

*The abstract theorem.*  **K. Kaveh, A. G. Khovanskii, "Newton–Okounkov bodies, semigroups of integral points,
graded algebras and intersection theory", Ann. of Math. 176 (2012), arXiv:0904.3350** `[full text: the
introduction's Theorem 1, §1.1 Definitions 1.1–1.2, Proposition 1.3, Theorem 1.4 with proof, Corollary 1.5,
Theorem 1.6 (statement), Definitions 1.9–1.10]`.  For an additive semigroup `S ⊂ ℤⁿ` with a grading by a
half-space, the *Newton–Okounkov convex set* `Δ(S, M)` is the slice at level one of the closed cone generated
by `S`; it is a convex body when the pair is strongly admissible; Theorem 1.6 ("approximation of a semigroup
by its regularization"): for a closed strongly convex cone that meets the boundary of `Con(S)` only at the
origin there is a constant `N` such that every point of the group `G(S)` in that cone at distance more than
`N` from the origin belongs to `S`.  *Comparison with Theorem 11.69.*  If (C) held with `β = 0`, the set
`{(q, M) : q ∈ Q_M}` would be a graded semigroup, `K` its Newton–Okounkov body, and Hausdorff convergence and
convexity classical — with the stronger conclusion that interior lattice points are eventually all attained.
The report's "Fekete's lemma for sets" is the version with a bounded error in place of exact additivity, and
with real instead of integer points; its proof is short, and the Lean statement
(`SuperAdditive.hausdorff_limit`) is to my knowledge not in Mathlib.  Related classical forms: sums of finite
sets and Hilbert polynomials (Khovanskii 1992, `[from memory — unverified]`), the Shapley–Folkman
convexification of Minkowski averages, the convex domain of the microcanonical entropy for finite-range
observables (Ruelle 1969; Lanford 1973 — **not accessible**, `[from memory — unverified]`).

*One variable.*  **E. J. Janse van Rensburg, "Supermultiplicative inequalities and limits in the statistical
mechanics of lattice clusters", arXiv:1603.08553v6 (J. Phys. A 54 (2021) 105003)** `[full text of the abstract
and of the statements of Lemma 2.1, Theorems 2.2, 2.4, 2.5, 3.1, 3.2, 4.1]`: for one energy variable,
`p_{n₁}(m₁)p_{n₂}(m₂) ≤ p_{n₁+n₂}(m₁+m₂)` "together with mild assumptions" gives the density function on
`(ε_m, ε_M)` and its concavity; the end points come from Fekete's lemma for the extreme energies.  Theorem 11.69
is the several-variable statement about the *support*, as the report says.

*Rotation sets.*  Kucherenko & Wolf, arXiv:1210.0135 (Israel J. Math. 2014) `[abstract, introduction,
Proposition 3]`; see A2.5.

*Surface law.*  **K. Bezdek, "Contact numbers for congruent sphere packings in Euclidean 3-space", Discrete
Comput. Geom. 48 (2012) 298–309, arXiv:1102.1198v2** `[full text of abstract, introduction and Theorem 1.1]`;
see A2.3.  Edge-isoperimetric results for the cubic lattice (Mainini–Piovano–Schmidt–Stefanelli 2019) and
"edge isoperimetry of lattices" (Strachan–Swanepoel 2025) `[search snippets]` are the natural place to look
for the diamond-lattice nearest-neighbour bound `e₃ ≤ 2N − 2^{-2/3}N^{2/3}`; I did not find it.

*The cluster method* (Kanamori; Kaburagi–Kanamori; "basic polytope" in Huang et al. 2016) is correctly
attributed in the report; not re-searched.

Classification: abstract limit theorem **known special case / reformulation**; the limit shape of
diamond-lattice bridges, its polytopes and numbers **plausibly original generalisation (application)**;
stability of covering numbers **unresolved (elementary, not found)**.

### 4.7 Search log (abridged; details and outcomes in `NOTES.md`)

| # | topic | queries (tool) | outcome |
|---|---|---|---|
| S1–S3, S11 | proof logging for CFN / WCSP / toulbar2 | 4 web searches | nothing CFN-specific; found CP 2026 #43, CP 2025 #21, ASE 2025, Dlask et al. |
| S4–S7 | certified counting, bounds, MAP | 4 web searches | Tan et al. 2024; Py et al. 2022; Cheng et al. 2024; nothing for MAP/MRF |
| S8 | arXiv API | 5 queries | 0 hits for CFN/WCSP/toulbar2 with proof terms; 20 `"proof logging"` preprints listed |
| S9–S10 | toulbar2 | GitHub code search; user guide | no proof logging |
| S12–S15 | Max-SAT certificates; OSPREY; interval methods | 2 fetches, 2 searches | as in §4.1 |
| S16–S23 | distance distributions, homometry, scattering, unassigned distances | 7 searches, 5 PDFs | §4.5 |
| S24–S28 | semigroups, rotation sets, Lanford, supermultiplicative models, contact numbers | 5 searches, 4 PDFs | §4.6 |
| S29–S33 | joint-space inertia, motion planning, lever arm in proteins, systematic search | 4 searches, 1 PDF | §4.4; a remembered "displacement-bounded torsion step" in a conformer generator was **not** confirmed and is not cited |
| S34–S35 | weightable quasi-metrics, Randers metrics | 2 searches, 1 PDF | §4.3 |
| S36–S39 | Merhav 2011; follow-ups of certified Lipschitz optimisation | 1 PDF, 2 searches, 4 arXiv API queries | §4.2 |
| S40 | hinge RMSD closed form | 1 search | nothing |


### 4.8 Claims in the README or the theory report whose novelty wording should be weakened

Each item: where, what it says, the evidence, a replacement that I would accept as a referee.

| # | where | wording now | evidence | suggested wording |
|---|---|---|---|---|
| W1 | theory report §0.2, row D3 | "verified checkers exist for exact model counting only" | Tan et al. CAV 2024 (formally verified approximate counting); McCreesh et al. CP 2026 (formally verified enumeration; count-preserving transformations); Cheng–Luo–Jiang IJCAI 2024 (two-sided bounds of a weighted count with pruning, clausal proofs) — §4.1 items 5–7 | "verified or proof-producing checkers exist for exact weighted and unweighted model counting (CPOG, Lean 4), for approximate counting with probabilistic guarantees (ApproxMC certificates, Isabelle/HOL + CakeML), for solution enumeration (VeriPB/CakePB) and for exact stochastic-SAT values through two-sided implication proofs; a verified checker for *deterministic two-sided bounds on a weighted sum* with this rule set was not found" |
| W2 | §6.4, first two sentences; §0.2 row E1 ("the gap concerns native witnesses and their checking cost"); `L1` §C4(ii) ("the 43-times figure … is the number to beat") | checking cost of the pseudo-Boolean route is presented as the reason for native certificates | Koops et al. CP 2025: formally verified PBO, with LP/Farkas bounds, within a factor 20 of solving, median 1.43; van Doren et al. ASE 2025: native MaxSAT logging with median overhead < 2 %; Py–Cherif–Habet 2022: EPT-sequence certificates with a checker for MaxSAT | "… no proof logging for cost-function-network / MAP solvers was found (toulbar2 1.0.0 has none).  The ingredients have verified checkers in the pseudo-Boolean setting — LP bounds through Farkas certificates and dominance — with checking within a factor 20 of solving time, and certificates made of equivalence-preserving transformations exist for MaxSAT with an unverified checker; whether a native format is cheaper has not been measured.  What has no counterpart there is a certificate valid for a whole class of residuals." |
| W3 | §10 row G19 and §11.17 "Prior art" | "the distance is known as a descriptor distance (Osada et al. 2002; bag of bonds)"; "Not found in print, and immediate once named: the profile distance read as the exact envelope of the class of unknown Lipschitz pair potentials" | Mémoli–Needham 2022 (and Mémoli 2011): the Wasserstein distance between global distance distributions is a named pseudometric, a lower bound of the Gromov–Wasserstein distance, with a literature on its zero set (Boutin–Kemper; homometry) — §4.5 | "the distance is the Wasserstein-1 distance between global distance distributions, a standard lower bound of the Gromov–Wasserstein distance (Mémoli 2011; Mémoli–Needham 2022), whose zero set is Patterson homometry; its reading as the support function of the class of Lipschitz pair potentials is Kantorovich–Rubinstein duality for that distance" |
| W4 | §11.17, Theorem 11.48(b) | "`d_P` is a pseudometric with large fibres … (802 075 walks … 541 profiles)" | the fibres have three distinct sources (labels, homometry, truncation), the second being a classical subject; generic uniqueness (Boutin–Kemper) does *not* apply to chains (their Lemma 1.8) — §4.5, A2.6, A2.7 | add one sentence naming the three sources and citing Boutin–Kemper with the caveat; the count 541 is reproduced (all pairs, squared distance `< 5`) |
| W5 | §10 row G13; §11.11 ("the reviewer judged the packaging new for this problem") | "elementary (Johnson reweighting, min-plus adjointness); the packaging for certification apparently new" | A2.4: for symmetric `d` the reduced envelope is a weightable quasi-metric with weight `−2f^d` — the classical correspondence between weighted semimetrics, weightable quasi-metrics and partial metrics (Matthews; Künzi–Vajner; Deza–Deza–Vidali) | "… the reduced envelope is a weightable quasi-metric (equivalently a partial metric) whose weight is the regularised known part — a classical correspondence; the equivalence of value certificates with point certificates of the reduced instance was not found" |
| W6 | §10 row G16 ("lever-arm effects are folklore in molecular modelling"); README "Status" ("the verified per-torsion constants grow with the distance to the chain end") ; the name "lever-arm law" | the growth law reads as a finding | the weighted-`ℓ¹` displacement bound with lever-arm weights is a published certificate in motion planning (Schwarzer–Saha–Latombe 2005, Lemma 2); the growth of joint-space inertia is documented in robotics (Featherstone 2004); the `m³` of a moment of inertia is a one-line computation — §4.4 | "the constants are (square roots of) reduced moments of inertia and therefore grow like `m^{3/2}` on any domain that contains extended arms (sharp constant `2√2/3` at the centre of a tetrahedral chain); per-joint lever-arm bounds of this kind are standard in robot motion planning.  New here are the consequences for certification (Theorems 11.37–11.38)." |
| W7 | §10 row G7; §11.6 "Attribution" | "a corollary of Merhav's (2011) theorem on exponential moments of distortion"; "[K, not verified in detail]" | Merhav 2011, §4, read in full: an example of a general observation, stated as "a straightforward exercise", for memoryless finite-alphabet sources and additive distortion | "a corollary of an example in Merhav (2011, §4, eq. (37))"; tag "[K, section read in full]" |
| W8 | §10 row G24 and §11.22 "Prior art" ("Fekete's lemma for sets"; "limits of supermultiplicative models … are known") | the abstract theorem is presented without its closest classical relative | Kaveh–Khovanskii 2012 (Newton–Okounkov body of a graded semigroup; approximation theorem 1.6, stronger for exact semigroups) — §4.6 | add: "for an exact semigroup of lattice points this is the Newton–Okounkov body (Khovanskii; Kaveh–Khovanskii 2012), whose approximation theorem gives in addition that interior lattice points are eventually attained; the statement here allows a bounded error" |
| W9 | §11.22, Proposition 11.73 (`e₈(S) ≤ 6N − 3N^{2/3}`; "proved: `k ≥ 0.50`") | presented as new, with the constant 3 | Bezdek 2012, Theorem 1.1(ii): contact numbers of subsets of a lattice packing are `< 6n − 3.665n^{2/3}` — A2.3 | cite Bezdek for the second-neighbour term; constants `3.665` (all site sets) and `4.617` (walks, by sublattice balance); "`k ≥ 0.69`" |
| W10 | §0.2 row C4; §4.4 "Prior art" | "finite-angle closed form and chained bound: no match found" | the closed form is the planar weighted Procrustes residual `2(S − |I_A + I_B e^{iφ}|)`; the chained bound without superposition is Lemma 2 of Schwarzer–Saha–Latombe | keep "not found as a bound on the Kabsch cost"; add the two remarks |

None of W1–W10 touches a machine-checked statement or a theorem; they concern the last column of the two
tables and the prior-art paragraphs.

### 4.9 Claims that are stated too modestly

| # | where | what is stated | what could be stated, and the evidence |
|---|---|---|---|
| M1 | §6.1, §0.2 row E1, README "Kernels" | the residual kernel is listed as one of three kernels, novelty "no native verified checker … found" | Its distinguishing property is the quantifier: one accepted certificate bounds `E + g` for **every** residual of an envelope class consistent with interval anchor data, and the kernel decides non-emptiness of the class (`verifyITop_sound`, `IProblem.consistent_iff_nonempty` **[V]**).  Every proof-logging system I read certifies a statement about one instance (§4.1).  This is the capability to put first.  (Evidence is a comparison of statements for the systems read plus absence in 20 listed preprints — not a proof of novelty.) |
| M2 | §11.22, Theorem 11.69 ("nothing in this argument says how fast they fill it") | only the one-sided rate `168/(N+3)`; the `N^{-1/3}` law is read as the rate of the shape | Proposition A2.2 **[P]**: under the same hypotheses interior points are approached at rate `O(N^{-1/2})`; the `N^{-1/3}` law is a boundary effect.  For exact semigroups the classical theorem gives `O(1/N)`. |
| M3 | §11.22, Proposition 11.73 ("proved: `k ≥ 0.50`") | surface-law constant | `k ≥ 0.69` for walks (A2.3) **[P from K]** |
| M4 | §11.14, Theorem 11.36 ("`c_i ≥ 0.824·Λ b m_i^{3/2}`", "lower constant numerical") | a lower bound with a numerical constant | the sharp asymptotic constant: `sup_x 2√(2I_red) = (2√2/3)·b·m^{3/2}(1+o(1))` at the central torsion, `(4/3)·b·m^{3/2}` far from the centre, by a three-line argument (largest extension of `j` bonds) and attained by an all-trans arm behind one gauche torsion **[P sketch + N]** (§3) |
| M5 | §11.17 and COMMON ("no experimental observable appears anywhere") | the profile class is described as a class of unknown pair potentials | Proposition A2.1 **[P, checked]**: the Debye intensity at wave number `q` is a member of the class with `L = q²/6` per pair, so every statement of Theorem 11.48 and the linear kernel applies verbatim to *scattering curves of a single conformation*, and the fibres of the complete profile are exactly the scattering-indistinguishable conformations.  This is a precise physical reading under stated assumptions (kinematic scattering, `q`-independent form factors, no cutoff, one conformation — not an ensemble). |
| M6 | §11.17 (the referee's "541 profiles") | quoted from a referee, convention unstated | reproduced independently (A2.6, §3) with the convention "all pairs, squared distance `< 5`"; under the convention of §11.22 the number is 507 |
| M7 | §11.6 | Merhav's example "available to us only through an automatic summary" | now read in full; the attribution is correct (W7) |

---

## 5. What I did not settle

* **Absence claims.**  E1 rests on indexed sources and on toulbar2's public documentation and code as of today;
  two 2026 theses that surfaced (Oertel, Lund; McIlree, Glasgow) were not read, and workshop papers are not
  indexed.  D1 (thermal prune as a certificate rule) was not searched beyond `L1`.
* **Not accessed** (cited through others or from memory, and tagged so): Featherstone 2004 beyond the abstract
  (repository copy restricted); Lanford 1973; Ziemian 1995; Mémoli 2011; Matthews 1992/1994 and Künzi–Vajner
  1994 (through Deza–Deza–Vidali and a search snippet); Petoukhov–Svergun 2015; Janse van Rensburg's book;
  Hansen–Jaumard–Lu 1991 (already inaccessible to `L4`); the JAIR version of Py–Cherif–Habet (server error; the
  IJCAI abstract was read); the supplementary material of the K*-family papers; the body of Tan et al. 2024.
* **Read through a fetch tool only** (short quotations, no page images): Koops et al. 2025; Hallen–Donald 2019;
  Konarev–Svergun 2015; the Gortler–Theran–Thurston abstract; the toulbar2 guide.
* **Mathematics.**  A2.2 and A2.7 are not checked numerically; `M₀(p)` in A2.2 is not effective.  A2.3 uses the
  report's bound on `e₃` without re-deriving it.  A2.5 uses Ziemian's theorem through a secondary source.
  Whether the bridge statistics of Lemma 11.68 can be made an exact semigroup is open.  The sharp constant in M4
  is a sketch plus numerics on a 20° grid, not a written proof.
* **Identifiability.**  I did not apply Proposition 1.10 of Boutin–Kemper to chains (is a *generic chain with
  fixed bond lengths* reconstructible from its complete distance multiset?); did not enumerate the diamond
  lattice of §11.22; do not know whether the homometric fraction on `ℤ³` has a positive limit; have no
  stability estimate (RMSD against profile distance) and A2.6 shows none can hold globally.
* **No measurement** supports or refutes "native certificates are cheaper to check" (see §7, request E-1).

## 6. The three most promising next steps

1. **Measure the native-versus-pseudo-Boolean question.**  One cost-function-network run with DEE, logged twice:
   as a certificate of the Lean kernel and as a VeriPB proof (cutting-planes derivation of each reparameterisation
   bound from its dual solution; dominance steps for DEE), checked by CakePB.  Until this exists E1 is a
   statement about absence, not about a capability with an advantage.  The residual kernel has no
   pseudo-Boolean competitor and should be presented first.
2. **Identifiability of chains from distance data, done properly.**  Three precise questions that the literature
   leaves open and that are within reach: (a) *generic chains*: for fixed bond lengths (and angles), is the map
   from torsion space to the complete distance multiset injective modulo the obvious symmetries (isometries,
   chain reversal) on a dense open set?  Boutin–Kemper's Proposition 1.10 with the symmetry group of the bonded
   pattern is the tool; (b) *lattices*: growth rate of the homometric fraction (A2.6) and of the fibres of the
   truncated profile — the latter is the joint density function of Janse van Rensburg's theory, i.e. a concave
   entropy on the limit shape, which nobody has computed for this model; (c) *with a cutoff*: A2.7 reduces
   local identifiability to rigidity of the contact framework and exhibits exponentially large global fibres;
   the right global object is the group of re-orderings and sign changes of torsions that preserve the contact
   framework.  For the science division's agenda the conclusion to date is negative and should be stated
   plainly: **a pair-distance profile with a cutoff does not identify a conformation, not even on small
   lattices, and the theorem usually quoted for the opposite (generic reconstructibility) does not cover
   chains.**
3. **The limit shape as a Newton–Okounkov body.**  If the concatenation error of Lemma 11.68 can be made
   constant by a change of bookkeeping (e.g. recording the linker's own contribution separately, or restricting
   to bridges with a prescribed end pattern), the profile vectors of bridges form a genuine graded semigroup of
   lattice points; then the approximation theorem gives interior convergence at rate `1/N`, the number of
   attained profiles at length `N` is asymptotically `vol(K)·N^d` (Kaveh–Khovanskii, Theorem 1.14 — statement
   seen, not studied), and `vol 𝒦` — which §11.22 brackets by `2.2 ≲ vol ≤ 3.125` — becomes computable from the
   exact class counts of the Computational Research Division (4 532 profile classes at 27 beads).  This is a
   cheap, falsifiable prediction: the number of distinct profiles of bridges should grow like `vol(𝒦)·N³`
   (divided by the index of the lattice they generate in `ℤ³`).  A plausibility check **[H]**: at 27 beads
   `vol(𝒦)·N³ ≈ (4–6)·10⁴`, far above 4 532; but the profile set at that size reaches only 39 % of the bulk
   extent (surface law), and `0.39³·(4–6)·10⁴ ≈ 2 600–3 700` is of the observed order.

## 7. Requests

### To the theory division

* **T-1 (wording; no mathematics).**  Apply W1–W10 of §4.8, in particular replace the D3 sentence and the two
  sentences of §6.4 by the texts given there, and add to `docs/prior_art/` the references of §4 (reading levels
  as stated).  Remove "is the number to beat" from `L1` or date it.
* **T-2.**  Add Proposition A2.1 to §11.17 (or refute it): `|I_x(q) − I_y(q)| ≤ (q²/3)·Σ_k|s^x_(k) − s^y_(k)|` for
  Debye intensities of `N` equal scatterers.  A Lean statement is a three-line consequence of `pairRes_sub_le`
  once `|d/ds sinc(q√s)| ≤ q²/6` is available; say explicitly that it concerns one conformation.
* **T-3.**  Check and, if correct, machine-check Proposition A2.2 in `SetLimit.lean`: under (C), (E), (B), for
  `p` in the interior of the limit, `dist(p, E_M) ≤ β/m + (d+1)(β′+R)m/M` whenever `E_m` contains `d+1` points
  whose convex hull contains `p`.  Then correct the sentence after Theorem 11.69.
* **T-4.**  Decide whether Lemma 11.68 can be sharpened to an exact semigroup (constant error vector for a
  suitable sub-family of bridges).  If yes, state Theorem 11.69 as a Newton–Okounkov body and test the
  prediction of §6 item 3 on the enumeration data.
* **T-5.**  Replace the constant 3 of Proposition 11.73 by Bezdek's, with the citation (A2.3), and state the
  sharp constant of Theorem 11.36 (M4) or say why the present one is preferred.
* **T-6.**  State in §11.17 what the fibres of `d_P` are (labels, homometry, truncation), cite Boutin–Kemper
  with the caveat of their Lemma 1.8, and state the convention behind "541".

### To the engineering division

* **E-1 (benchmark: native kernel against pseudo-Boolean proof logging).**  *Motivation:* §6 item 1.
  *Formulation:* for each instance, (i) a certificate of `verify`/`verifyR` as now; (ii) the same search tree as
  a VeriPB proof for the 0–1 encoding (one indicator per site and state, exactly-one constraints, objective =
  table entries): each `leaf` bound as a cutting-planes derivation whose multipliers are the messages, each
  `prune` as a dominance step with the witness "replace state `r` by `t` at site `i`", each `branch` as case
  splitting.  *Inputs:* the conformance vectors in `experiments/certs/`, the frustrated-triangle families of
  §6.3 for `m ≤ 12`, and ten pairwise instances with 20–60 sites and 3–10 states.  *Outputs:* certificate and
  proof sizes, checking times of the reference checker, of the Lean kernel (`decide +kernel` where feasible)
  and of VeriPB with elaboration to CakePB.  *Validation:* both routes must certify the same bound; a planted
  wrong bound must be rejected by both.  *Stopping:* if the VeriPB route is within a factor 3 in size and time
  on all instances, report that the "native" advantage is not measurable.  *Resources:* a few CPU hours; no
  solver changes (proofs can be generated from existing certificates).
* **E-2 (homometry on the diamond lattice).**  *Motivation:* A2.6 was done on `ℤ²`, `ℤ³`; the theory's model is
  the diamond lattice.  *Formulation:* from the existing exhaustive enumeration (`ENG-RES-0002`, up to 27
  beads) count, per chain length: walk classes, site sets up to the lattice point group with reflections,
  distinct complete squared-distance multisets, homometric groups and their sizes, and profile classes at
  `S_c = 12` — i.e. the columns of the table in A2.6.  *Validation:* my script `homometry_saw.py` reproduces
  802 075 and 541 on `ℤ²` and can be adapted by changing `STEPS` and the point group; agree on 8–12 beads first.
  *Expected output:* the homometric fraction as a function of `N` and the number of profile classes of
  *bridges* (for §6 item 3).  *Stopping:* at the largest size for which the site-set table fits in memory
  (my unoptimised script needs about 2 GB for the 2.8·10⁵ site sets of 16 beads on `ℤ²`; a compact
  implementation is needed beyond ≈ 18 beads).
* **E-3 (optional).**  Tabulate, for the enumerated conformations, the Debye curves `I(q)` on a grid and verify
  A2.1 on the real data; report the largest `|ΔI(q)|/(q²W/3)` per `q`.
