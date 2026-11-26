# R22 — Review for the Geometry division: second-moment rigidity of conformational ensembles (their Theorems B, B′, G), prior art, assumption table

> **Coordinator's status note, superseded 2026-11-26 19:11 UTC.**  This report was first committed as handed back, unread (checkpoint 58).  It has since been read in full and checked; see the coordinator's note at its end and SCI-REV-0021.

*Workstream R22 of the science division, 2026-11-26 17:16–18:30 UTC.  **This is an internal review by an AI session,
not external peer review.**  Object: `docs/geometry/ENSEMBLE_RIGIDITY.md` of the branch `research/geometric-inference`
at commit `d84a43b` (read-only export `geo_ro_d84a43b`; all line numbers "l.…" refer to that file).  §2 (Lemma 2.2),
§4.2 (Theorems B, B′, Corollary 4.2) and §7.2 (Theorem G) are unchanged at their later checkpoints `7c2a3d1` and
`f7eed26`, except for the title of Theorem G at `f7eed26` (my own check: identical sha256 of the three sections at
`7c2a3d1`; one-line diff at `f7eed26`).  Their notion "ensemble rigidity" has since been renamed **second-moment
rigidity** (formerly "ensemble rigidity"); it is not an object of this review.  Their Theorems I, J (later
checkpoints) were not reviewed.*

*Four kinds of checking are kept apart: **review** (I read and re-derived on paper), **replication** (my own code,
written from their definitions before I opened theirs: `experiments/science/ws_R22/`), **re-run** (their code from a
scratch copy), **read only**.  Labels: [V] machine-checked, [P] paper proof (here or theirs, re-derived), [K] known
(with what I opened), [N] numerical only, [C] conjecture.  Working notes: `experiments/science/ws_R22/NOTES.md`.*

---

## 0. Verdict

1. **Lemma 2.2, Theorem B, Theorem B′, Corollary 4.2 and Theorem G (a)–(e) are proved as stated** [P; review, every
   step re-derived; the algebra of G(b) and the bracketed proof of G(d) redone in full].  **No critical finding.**
2. Three **major** findings, none of which makes a theorem false: **F1** the scope of the conic condition (CC) —
   it is equivalent to a stronger property than identifiability (the simplex of the states is a face of the
   *semidefinite relaxation*), and it fails on every pair of states that share rigid segments with at most three
   differing torsions, where the truth (decided here by Theorem B′) is mixed; **F2** Theorem G (c)–(d) is a
   qualitative statement: `κ` is not computed, it is *not* the local eigenvalue (numerically up to 6.6 times
   smaller, attained far from the states), and with the values found the bound is informative only below a
   relative data error of 0.03–0.4 %; **F3** prior art: Theorem B with Corollary 4.2 is the rank-`d`,
   general-constraint extension of a 1996 theorem of Laurent and Poljak on simplicial faces of the elliptope (for
   `d = 1` it *is* that theorem), and Theorem G (b)–(c) is the dual-certificate localisation bound of
   sparse-measure recovery.
3. Seven **minor** findings (F4–F10): a shorter proof of Lemma 2.2 that removes the measurability question;
   implicit hypotheses; the Lean core is a two-block lemma; compactness of `𝒫(z)`; one false constant; weaker
   hypotheses under which G (a)–(c) hold; four numbers quoted that the re-runs do not reproduce.
4. **States that share rigid segments (Item 3 (c)), `K = 2`:** one differing torsion — never identifiable
   (coordinator; control passes).  **Two differing torsions with segments of at least five atoms — identifiable,
   although (CC) fails** [P here, N: 8 of 8 and 4 of 4 instances by two routes]; exactly eight conformations are
   linear images of the stacked pair, six of them with mirrored segments.  **Exception: two half-turn flips
   (`θ₁ = θ₂ = π`) are *not* identifiable** — an exact identity `D(X₁) + D(X₂) = D(Y_v) + D(Y_vi)` [P, N to `3·10⁻¹⁴`].
   **Three differing torsions with long segments — identifiable**: the two states are the only linear images
   [P up to six explicit non-zero numbers per instance; N: 8 of 8, 2 of 2].  With a four-atom segment between the
   hinges, or three consecutive torsions, the answer depends on the instance [N].
5. Re-runs of their harness reproduce what the report quotes for Theorems B, B′, G; four small discrepancies
   elsewhere (F10).

---

## 1. The statements, with every implicit hypothesis

**Standing hypotheses used and not always stated.** (H-a) `E₀` connected, `𝒞 = 𝒞_d(E₀, ℓ) ≠ ∅` — gives bounded
`|x_i − x_j|` on `𝒞`, hence `M(ν)` finite and `ζ_i ∈ L²`; also needed for the compactness of `𝒫(z)` (F6).
(H-b) An ensemble is a Borel probability measure on `𝒞`; **congruence includes reflections**, and `𝒞` contains the
mirror image of every segment of a chain (no chirality constraint) — this is what produces the competitors of §3.3.
(H-c) The datum is `M(ν)_ij` for **all** pairs, constrained pairs included (there `M_ij = ℓ_ij²` automatically).
(H-d) `w_k > 0`, `Σ w_k = 1`, `X_k ∈ 𝒞`.  (H-e) `z` spans `ℝ^m` affinely (stated in Lemma 2.2 and Theorem B′; derived
from (CC) in Theorem B).  (H-f) the constraints hold *exactly* in every state (no spread of bond lengths or angles).

**Lemma 2.2** (l.125–143) — holds [P].  With (H-a), (H-c), (H-e).  The map `A` is in fact a *linear* function of
`x` on `supp ν` (F4), so nothing has to be chosen almost everywhere.

**Theorem B** (l.222–240) — holds [P; the step "one block" is [V] only pairwise, F5].  Complete statement: *Let
`d ≥ 1`, (H-a), (H-d), `μ = Σ w_k δ_{X_k}`, `z` its stacked configuration, and `𝒩(z) = 𝒯`.  Then `z` spans `ℝ^{dK}`
affinely, the `X_k` are pairwise non-congruent, and every Borel probability measure `ν` on `𝒞` with
`M(ν)_ij = M(μ)_ij` for all `i, j` has `ν({x ≅ X_k}) = w_k` for every `k`.*  Steps: (CC) ⇒ spanning — holds (for
`d = 1` too: a rank-one block-scalar matrix has one non-zero `s_k`, contradicting `Σ w_k s_k = 0`); `P = Σ c_k E_k`,
`Σ w_k c_k = 1` — holds (uses `Σ w_k = 1`); `c_k ≥ 0`, at most one non-zero, hence exactly one `c_κ = 1/w_κ` — holds;
`√w_κ·A|_κ ∈ O(d)` — holds; weights from `∫AᵀA dν = I` and linear independence of the `E_k` — holds; pairwise
non-congruence (needed for "the class of `X_k` has probability `w_k`") — holds, because two congruent states make
the blocks of `z` linearly dependent modulo `𝟙`.

**Theorem B′** (l.246–262) — holds [P], with one condition to add: `𝒫(z)` is compact (F6).  (⇐) holds.  (⇒): the
finitely supported measure keeps the barycentre exactly — holds (it is Carathéodory applied to the two normalised
barycentres); `Y_j ∈ 𝒞` — holds; "congruent iff `P_j = E_k/w_k`" — holds, uses (H-e).  The theorem does not cover
mixtures whose `z` does not span (two states that differ in one torsion have `z` of affine rank 5): there the
criterion must be read in the span (F6).

**Corollary 4.2** (l.264–274) — holds [P]; its converse and two consequences are in F7.

**Theorem G** (l.487–532) — holds [P].  (a) holds.  (b) holds; **smoothness of `𝒞` is not used**, `n − 1 > dK` only
makes `Π^⊥ ≠ 0` and follows from (CC) for chains in `ℝ³` (`2n − 3 ≥ D_K` gives `n ≥ (9K² + K + 8)/4 > 3K + 1`).
(c) holds.  (d) holds, uses that `𝒞` is a `C²` submanifold near each `X_k`; `C_μ` depends on `κ`, on the smallest
singular value of the linear map of l.522, on a second-order constant of `𝒞` at the states (valid on the whole
nearest-state cell), on `‖L_k‖` and on the diameter of the set of states — nothing else.  (e) holds.  Details in
§2, F8.  *For chains there is no singular state*: the rigidity matrix of `E₀^{BA}` has full row rank `2n − 3` at
every conformation with bond angles in `(0, π)` (each atom is attached to its two predecessors by two non-parallel
edges), and that of the path `E₀^B` always; so `𝒞` is a smooth manifold everywhere and its tangent space is the
flex space (checked on random, planar and helical chains at three bond angles: rank `2n − 3` in 39 of 39 cases,
`t2_rigidity_rank.py`; control with a bond angle of `π − 10⁻⁹`: the smallest singular value collapses).  For
constraint graphs with singular points, (a)–(c) survive unchanged and (d) can lose its exponent (secants need not
be tangent to second order).

**The Lean core** (read only; not compiled — `lake` is excluded by the brief).  `block_rigidity`
(`proofs/Geometry/EnsembleRigidity.lean` l.206–245): two orthogonal subspaces of dimension `d ≥ 1`, a linear map
into a space of dimension `≤ d` with `‖A(u + u′)‖² = c₁‖u‖² + c₂‖u′‖²` ⇒ `c₁ = 0 ∨ c₂ = 0`; `block_coeff_nonneg`
gives `c ≥ 0`.  This is the paper's step for **two** blocks, in the equivalent form `P = AᵀA`; the `K`-block step
is its application to every pair plus the normalisation `Σ w_k c_k = 1`, and is not machine-checked (their §10
says so; l.242–244 reads as if it were).  `stacked_sqdist` is Lemma 2.1 for finite mixtures as stated.

---

## 2. Findings

### F1 (major) — what (CC) is, and how large the set is on which it fails

*Deciding lines:* l.33–39 (summary item 3), l.222–231 (Theorem B), l.722–723 ("Planar and other symmetric
conformations can violate (CC) at any length"), and the row "genericity" of the assumption table.

(i) **(CC) characterises a face of the relaxation, not identifiability** [P].  For `z` spanning, the smallest
face of the spectrahedron `𝒮` (their §8.1) that contains `M(μ)` is `{D(zP^{1/2}) : P ⪰ 0, P ∈ I + 𝒩(z)}`, of
dimension `dim 𝒩(z)`; it contains the simplex `conv{D(X_k)}`, of dimension `K − 1`.  Hence
**(CC) ⇔ `conv{D(X_k)}` is a face of `𝒮`**, whereas identifiability ⇔ the smallest face of `𝒦 = conv D(𝒞)` at `M(μ)`
meets `D(𝒞)` exactly in the affinely independent points `D(X_k)` (Corollary 4.2 and its converse, F7).  The gap
between the two is the gap between `𝒦` and `𝒮` — their finding 10 — and it is the rank-`d` version of the classical
gap between the cut polytope and the elliptope (F3).

(ii) **The excluded set contains every pair of states that share rigid segments with at most three differing
torsions** (coordinator, `hinge_pair.py`), i.e. the commonest two-state motions, at every chain length.  What is
true there (§3.3; `K = 2`, each shared segment with edge directions on no conic — five atoms in general position —
and consecutive hinge bonds not parallel):

| differing torsions | `dim 𝒩(z)` | conformations that are linear images of `z` | identifiable? | status |
|---|---|---|---|---|
| one | 10 (`z` has affine rank 5) | two circles (rotations and reflections about the hinge) | never | [P] coordinator; control here |
| two, at least 3 apart | 6 | exactly 8: the two states and 6 with mirrored segments | **yes**, unless both are half-turns | [P] §3.3; [N] 8/8, 4/4 |
| two, both half-turns | 6 | the same 8 | **no** | [P] exact identity; [N] `3·10⁻¹⁴` |
| three, long segments | 3 | the two states | **yes** | [P] up to six explicit numbers per instance; [N] 8/8, 2/2 |
| two, `j` and `j+1` | 9 (`z` has affine rank 5) | 4 | yes in 4 of 4 instances | [N] |
| two, `j` and `j+2` (4-atom segment) | 7 | a curve | instance-dependent: yes in 5, no in 1 of 6 | [N] |
| three consecutive | 7 | a curve | instance-dependent: no in 3, yes in 1 of 4 | [N] |
| four consecutive | 5 | the two states | yes in 2 of 2 instances | [N] |
| four or more with long enough segments (coordinator), or unrelated states with `n ≥ 12` | 1 | the two states | yes (Theorem B) | [P] theirs |

*Replacement text for l.722–723:* "Generic statements exclude a proper analytic subset.  It contains every pair of
states that share rigid segments and differ in at most three torsions (the stacked edge vectors of a shared
segment span only three dimensions), at every chain length, besides planar conformations.  On that set the linear
certificate is unavailable and identifiability itself varies: it fails for one differing torsion and for two
half-turn flips, and holds — by Theorem B′, not by (CC) — for two torsions in general position and for three
torsions with long segments."  *For the summary (l.33–39):* add "for `K`-tuples of conformations in general position".

### F2 (major) — Theorem G (c)–(d) is qualitative; `κ` is not its local value

*Deciding lines:* l.493–497 (statement of (b)–(d)), l.536–539 ("its local value at `X_k` … is a linear-algebra
quantity"), l.49–51 ("a global quantitative theorem").

The proof is correct; the constant is a global infimum that nobody has bounded from below, so (c)–(d) assert the
existence of constants.  In the research owner's terms this is **a general theorem whose guarantee is
computationally vacuous until `κ` has a certified lower bound**.  What is explicit and computable today is one
line of (c): `∫φ dν = −½⟨Π^⊥, M(ν) − M(μ)⟩ ≤ ½√(n − 1 − dK)·‖M(ν) − M(μ)‖_F` — a bound on the `φ`-energy, not on a
distance.  My numerics (§3.2, [N]; generic pairs, `n = 12…20`, weights 0.4/0.6):

* the local values (softest eigenvalue of `Π^⊥` on flexes modulo isometries) are `6·10⁻³ … 3·10⁻²`;
* a global search finds **smaller ratios far from the states** (`d_P² = 2.4 … 29` from the nearer state):
  `1.2·10⁻², 9.3·10⁻⁴` (`n = 12`), `7.2·10⁻³` (13), `3.8·10⁻³, 3.4·10⁻³` (14), `2.7·10⁻³` (16), `5.9·10⁻³` (20) — between
  1.1 and 6.6 times below the smallest local value.  These are upper estimates of `κ`;
* with them the constant `√(n − 7)/(2κ)` is at least `97 … 1200` (bond length 1), and (c) is below the trivial
  bound (the largest `min_k d_P²` over `𝒞`) only for `‖M(ν) − M(μ)‖_F ≤ 0.02 … 0.64`, i.e. `0.025 % … 0.41 %` of
  `‖M(μ)‖_F`; on 200 random ensembles the left side is `5·10⁻⁵ … 5·10⁻³` of the right side.

*Replacement text for l.536–539:* "`κ` is a global infimum that we have not bounded from below; (c) and (d) are
therefore existence statements for the constants.  The local value at `X_k` is an eigenvalue and only an upper
bound for `κ`: in numerical searches the infimum is attained far from the states at values several times smaller."

### F3 (major, novelty) — where Theorems B and G already exist

*Deciding lines:* l.656–661 ("Not found in print: Theorem B and B′ …; Theorem G …"), l.639–642 ("relatives … not
consequences"), `PRIOR_ART.md` rows for Theorems B, B′, G.  Details and reading levels in §6.

* **Theorem B and Corollary 4.2 at `d = 1` with unit-diagonal ("star") constraints are a theorem of Laurent and
  Poljak (1996)**, as quoted by Tropp (2018, Fact 3.1) [K; Tropp read in full text, Laurent–Poljak not opened]:
  for sign vectors `c_1, …, c_r`, if `W = [c_1 … c_r]` and `Z = [𝟙 | c_i ⊙ c_j (i < j)]` have full column rank, then
  `conv{c_i c_iᵀ}` is a simplicial face of the elliptope.  In the language of the report the states are the
  one-dimensional configurations `c_k`, the stacked rows are `z_i = (√w_k c_k(i))_k`, the conditions
  `z_iᵀ S z_i = 0` read `Σ_k w_k S_kk·𝟙 + 2Σ_{k<l} √(w_k w_l) S_kl·c_k ⊙ c_l = 0`, and **(CC) ⇔ `Z` has full column
  rank** [P; two lines; checked on 20 of 20 random families of sign vectors, `t6_d1_dictionary.py`:
  `dim 𝒩(z) = r(r+1)/2 − rank Z`].  The trivial quadrics are the single column `𝟙`; the realizable set `𝒦` is the cut
  polytope, the relaxation `𝒮` the elliptope; and a simplicial face of the elliptope spanned by cut matrices is
  exactly unique representability by cut matrices, the conclusion of Theorem B.  (The report assumes `d ≥ 2`, so
  the case `d = 1` is formally outside it; its proof covers it.)  Theorem B is the extension to rank-`d` states and
  an arbitrary connected constraint graph, with the same mechanism (the minimal face of a spectrahedron); what is
  new as far as I can see is that extension, the reading for ensembles, and the chain thresholds.
* **Theorem G (b)–(c)** is, in mechanism and in the form of its conclusion, the localisation bound of
  super-resolution: a dual certificate that is linear in the data, saturates on the true support and has quadratic
  growth gives `Σ |â_k|·dist(t̂_k, T)² ≤ C·δ` and `Σ_far |â_k| ≤ C·δ` (Fernandez-Granda 2013, Theorem 1.2 (ii), (iii),
  Lemma 2.1; read in full) [K].  What is specific here: the certificate `φ` is explicit, and `κ > 0` under (CC).
* **Theorem B′** is the general fact "a point of the convex hull of a compact set has a unique representing
  probability measure iff its minimal face meets the set in affinely independent points", composed with
  Lemma 2.2.  The same question for another averaged observable is the "maximal allowed probability" of an
  orientation (Longinetti, Sgheri, Sottile, arXiv 0712.3777) [K; through a full-text fetch].

*Replacement text for l.656–661:* "Theorem B and Corollary 4.2 extend the Laurent–Poljak sufficient condition for
simplicial faces of the elliptope (the case `d = 1` with unit-diagonal constraints, where (CC) is the full column
rank of their matrix `Z`) to rank-`d` states and general statewise constraints; Theorem G (b)–(c) is the
dual-certificate localisation bound of sparse-measure recovery with the explicit certificate `φ`.  Not found in
print: the extension itself, the thresholds of Theorem C, DEMIX, the non-degeneracy `κ > 0` under (CC), …".

### F4 (minor) — Lemma 2.2: a proof without `L²` representatives; `A` is linear

*Deciding lines:* l.127 ("a measurable `A`"), l.138–141.  *Replacement proof:* "Let `Π^⊥` be the orthogonal
projector of `ℝⁿ` onto `span(𝟙, columns of z)^⊥` and `φ(x) = tr(xᵀΠ^⊥x) = −½⟨Π^⊥, D(x)⟩ ≥ 0`.  Then
`∫φ dν = −½⟨Π^⊥, M(ν)⟩ = −½⟨Π^⊥, D(z)⟩ = tr(zᵀΠ^⊥z) = 0`, so `φ = 0` on `supp ν` (`φ` is continuous): every
`x ∈ supp ν` is `𝟙tᵀ + zA(x)ᵀ` with `A(x) = (Z₀⁺X₀(x))ᵀ`, `Z₀ = z − 𝟙z_1ᵀ`, `X₀ = x − 𝟙x_1ᵀ`, a linear function of
`x`.  On `E₀`, `eᵀA(x)ᵀA(x)e = ℓ_e² = |e|²`.  For all `i, j`,
`(z_i − z_j)ᵀ(∫AᵀA dν − I)(z_i − z_j) = M(ν)_ij − |z_i − z_j|² = 0`, and a quadratic form that vanishes on all
differences of an affinely spanning set is zero."  This is Theorem G (c) with zero data error; it settles item (i)
of the request (no null sets, no measurable selection) [P].

### F5 (minor) — Theorem B: hypotheses; what the Lean core is

*Deciding lines:* l.223 (`Σ w_k = 1` is used at l.236 and not stated), l.233–234 ("rank `0` or `≥ d ≥ 2`" — the
argument also works for `d = 1`), l.242–244.  *Replacement for l.223:* "`w_k > 0`, `Σ_k w_k = 1`, `X_k ∈ 𝒞`".
*Replacement for l.242–244:* "The step is machine-checked for two
blocks (`block_rigidity`, `block_coeff_nonneg`); for `K` blocks apply it to every pair, then `Σ w_k c_k = 1` leaves
exactly one coefficient."

### F6 (minor) — Theorem B′: compactness; Tchakaloff; non-spanning `z`

*Deciding lines:* l.253–258.  `𝒫(z)` is closed; it is bounded because the `E₀`-edge vectors of `z` span `ℝ^m`
(`E₀` connected, `z` spanning): `λ_min(Σ_e eeᵀ)·tr P ≤ Σ_e eᵀPe = Σ_e ℓ_e²`.  This is needed for the barycentre to
exist and for the reduction to a finite measure.  *Replacement for "by Tchakaloff's theorem (…)":* "`𝒫(z)` is
compact; the barycentres of the normalised restrictions of `ρ′` to `B` and to its complement lie in
`conv(𝒫(z) ∩ B)` and `conv 𝒫(z)`; by Carathéodory".  *Add:* "If `z` spans only an `m`-dimensional affine space,
replace `z` by an isometric copy in `ℝ^m`; the criterion is the uniqueness of the representing measure of `I_m` on
`𝒫` of that copy (the states are then points `P_k` that need not be linearly independent).  The same statement
holds for an arbitrary ensemble `μ`, with `z` a Gram factor of its centred `M`."

### F7 (minor) — Corollary 4.2: the converse, a bound on `K`, and "finitely many states"

*Deciding lines:* l.264–274.  [P] (a) Converse: if the smallest face of `𝒦` containing `M(μ)` meets `D(𝒞)` exactly
in the affinely independent points `D(X_k)`, then `μ` is identifiable.  ("Face" alone is not enough: a point of
`D(𝒞)` need not be extreme — Example 3.3.)  (b) `K ≤ 1 + dim aff 𝒦 ≤ 1 + (n − 2)(n − 3)/2` for chains with bond
angles; under (CC), `K ≲ (2/3)√n`.  (c) By Carathéodory every `M(μ)` is the datum of an ensemble with at most
`1 + (n − 2)(n − 3)/2` states, so **an ensemble with more shapes than that — in particular any ensemble with a
continuous part — is never identifiable.**

### F8 (minor) — Theorem G: slips, and the hypotheses the proof actually uses

*Deciding lines:* l.488–489, l.505–506, l.519, l.517–518, l.532.
* l.519 "`‖D(Δ)‖ ≤ 4‖Δ‖²`" is false in the Frobenius norm for `n > 10` (`Δ_1 = u`, `Δ_2 = −u`, the rest 0:
  `‖D(Δ)‖_F = √(4n + 24)`, `4‖Δ‖² = 8`).  *Replace by* "`‖D(Δ)‖_F ≤ 4√n·‖Δ‖_F²`".  No consequence.
* l.505–506: first-order optimality gives orthogonality to the infinitesimal isometries at `X_j`; it holds at
  `X_k` as well because `⟨V_j, V_jΞᵀ⟩ = tr(V_jᵀV_jΞᵀ) = 0` for skew `Ξ`.  *Add that line.*
* l.532: `|∂_vX|` must be the norm of the component of `∂_vX` orthogonal to the infinitesimal isometries.
* l.517–518: the nearest-state cell and the optimal alignment need a measurable selection (ties).  Routine.
* l.488–489: say where each hypothesis is used (§1).  *Replacement for the hypotheses:* "Let `z` span `ℝ^{dK}`
  affinely and `n − 1 > dK`.  Assume (H1) and (H2) below (both follow from (CC)).  Then (a)–(c).  If moreover `𝒞` is
  a `C²` submanifold near each `X_k` and the linear map of l.522 is injective (which follows from (CC)), then (d).
  (e) needs only the smoothness."
* **A strengthening** [P]: (a)–(c) hold under (H1) *the only conformations that are affine images of `z` are the
  states* (`𝒫(z) = {E_k/w_k}`) and (H2) *every flex of `(E₀, X_k)` of the form `zBᵀ + 𝟙tᵀ` is an infinitesimal
  isometry* — the compactness proof uses nothing else, and (CC) ⇒ (H1), (H2).  Numerically (H1), (H2) hold for
  three differing torsions where `dim 𝒩 = 3` (§3.2 (w)).  Conversely, for two differing torsions the mixture is
  identifiable but `φ` vanishes on six further classes: there `κ = 0` and `φ` certifies nothing — another
  certificate is needed, and one exists numerically on the re-hinging family (§3.3; §7, request 5).

### F9 (minor; outside the three theorems) — l.573–574

"(a) is the statement that the extreme Gram dimension of the constraint pattern is at most `d`" is not accurate.
The extreme Gram dimension (E.-Nagy, Laurent, Varvitsiotis) concerns *projections*: every partial matrix on the
edges of `G` that is completable to a correlation matrix has a completion in the convex hull of correlation
matrices of rank `≤ r` — the rank-`r` pieces need not match the partial matrix.  Theorem D (a) is fibre-wise (every
piece satisfies the statewise constraints) and is exactly the Barvinok–Pataki bound.  In their language `egd ≤ d`
is the statement "`π_F(𝒦) = π_F(𝒮)`" for star-shaped `E₀` and averaged pairs `F`, i.e. the hypothesis of
Theorem E (c) in projected form — this answers question 2 of their `PRIOR_ART.md` §4: the cited results cover the
star pattern only; for chain patterns I found nothing.  *Replacement text:* "(a) is the Barvinok–Pataki bound
applied to the fibre of the statewise constraints; the extreme Gram dimension is the corresponding notion for
projections onto a pair set under unit-diagonal constraints."

### F10 (minor; outside the three theorems) — four quoted numbers the re-runs do not reproduce

`THEOREM_REGISTER.md` "96 witnesses for `K ≤ 12`": the script prints 48 (2 geometries × 2 edge sets × 12).  l.443–444
"weights to `10⁻¹³`": `5.8·10⁻¹²` at `K = 4`, `n = 39`.  l.446 "`9·10⁻²` at `n = 16`": `7.8·10⁻²`.  l.705 "about one
minute": 8 s (HANDOFF says 10 s).

---

## 3. Replication and tests (own code), with controls

All scripts in `experiments/science/ws_R22/`, run as `OMP_NUM_THREADS=1 python3 -B <script> > <log>`; every log
cited reached its last line.  Library `r22lib.py` (transfer-frame chain, exact rational chain, conic system,
fraction-free rank, Procrustes distance with reflections, analytic torsion tangents); self-test
`r22lib_selftest_v2.log`: 0 violations.

### 3.1 (CC) at and below the thresholds — `t3a_cc_thresholds.py`, 12 s

* **Exact (ℚ, bond-angle cosine −5/13):** rank of the conic system `= min(2n − 3, D_K)` in all 22 cases
  (`K = 1`: `n = 4, 5, 6`; `K = 2`: `n = 10…13`; `K = 3`: `n = 21…24`; two rational tuples each).  (CC) holds exactly
  from `n = 5, 12, 23`.  This replicates Theorem C (b) for `K ≤ 3` at that geometry [P-exact, replication].
* **Floating point:** 20 random tuples per cell, three bond angles (cosines −1/3, −5/13, cos 111°): `dim 𝒩` as
  predicted in every cell; at the thresholds `n = 12` and `n = 23` the smallest retained singular value is
  `7·10⁻⁶ … 6·10⁻⁴` of the largest: the certificate is badly conditioned exactly where it starts to exist.
* **Controls (0 violations):** trivial quadrics lie in `𝒩(z)` (`8·10⁻¹⁶`); a congruent pair gives `dim 𝒩 = 15`;
  planar chains give `dim 𝒩 = 3`; the dimension does not depend on the weights.
* **Below the threshold, generic pairs** (`t3a_below_threshold_images.py`, 68 s, [N]): `n = 8` — a continuum of
  linear images and verified competing ensembles of 9 states (residual `3·10⁻¹²`); `n = 9` — 6, 6, 8 further
  images, none can carry mass; `n = 10, 11, 12` — only the two states.  This agrees with their §5.2 and with their
  later Theorem I, and validates my enumeration against their exact computation at `n = 10`.

### 3.2 Theorem G — `t3b_theorem_G.py`, 311 s, 0 violations of its controls

Generic pairs, cosine −1/3, weights 0.4/0.6; 20 000 (10 000) random chains and 48 (32) local minimisations each.

| `n` | local value at `X₁`, `X₂` | smallest ratio found (`d_P²` to the nearer state) | constant `√(n−7)/(2κ)` ≥ | bound beats the trivial one for `‖ΔM‖_F ≤` (relative to `‖M(μ)‖_F`) |
|---|---|---|---|---|
| 12 | `1.32·10⁻²`, `2.20·10⁻²` | `1.15·10⁻²` (2.4) | 97 | 0.35 (`2.6·10⁻³`) |
| 12 | `6.19·10⁻³`, `6.34·10⁻³` | `9.32·10⁻⁴` (8.0) | 1199 | 0.023 (`2.5·10⁻⁴`) |
| 13 | `8.03·10⁻³`, `1.72·10⁻²` | `7.24·10⁻³` (10) | 169 | 0.20 (`1.6·10⁻³`) |
| 14 | `1.94·10⁻²`, `2.92·10⁻²` | `3.76·10⁻³` (18) | 352 | 0.17 (`2.4·10⁻³`) |
| 14 | `3.09·10⁻²`, `1.85·10⁻²` | `3.41·10⁻³` (4.0) | 388 | 0.11 (`8.9·10⁻⁴`) |
| 16 | `8.21·10⁻³`, `2.73·10⁻²` | `2.69·10⁻³` (15) | 557 | 0.26 (`2.9·10⁻³`) |
| 20 | `1.48·10⁻²`, `1.50·10⁻²` | `5.88·10⁻³` (29) | 307 | 0.64 (`4.1·10⁻³`) |

* (a): `φ` at the states `≤ 2·10⁻²⁸`; `φ = −½⟨Π^⊥, D⟩` to `2·10⁻¹³`; `φ > 0.6` on 200 random chains.
* (b): each local value is reproduced by the ratio on a step of `10⁻⁴` along the soft direction (control).
* (c): `∫φ dν = −½⟨Π^⊥, ΔM⟩` to `2·10⁻¹³` on 200 random ensembles (control); slack of (c): `5·10⁻⁵ … 5·10⁻³` on random
  ensembles, at most `8·10⁻³` on symmetric broadenings along the softest flex.
* (d): the map of l.522 is injective: smallest singular value (columns normalised) `0.026 … 0.052`.
* (e): `‖ΔM‖ ∝ ε^{2.000}`, `W₂² ∝ ε^{2.000}`, `W₂²/‖ΔM‖ → 0.3116`; control, a one-sided shift: `‖ΔM‖ ∝ ε^{0.997}`.
* (w), where (CC) fails: two torsions — local values `2.7·10⁻²`, `1.6·10⁻²` but the global search reaches `9·10⁻¹⁴`
  at `d_P² = 20` (a mirrored linear image): `κ = 0`; three torsions — local `3.6·10⁻³ … 1.8·10⁻²`, global
  `8.5·10⁻⁴`, `1.9·10⁻³`: (a)–(c) hold numerically without (CC).

### 3.3 States that share rigid segments (Item 3 (c))

**Which route decides.**  Route A — Theorem B′: enumerate the conformations that are linear images of `z`, then a
linear programme over them (minimise the mass on the two true states subject to equal `M`).  This is the route of
their §5.2 and Theorem I; my code is independent (multi-start Levenberg–Marquardt on `|Ae|² = |e|²`, unknown
`A ∈ ℝ^{3×6}`).  Route B — the brief's programme over a grid of the differing torsions, extended to **all**
re-hingings: the components in which segments are mirrored must be included; a grid over the torsions alone misses
the competitor of the half-turn case (shown below).  Route A decides, with the paper proof; route B confirms.

**Proposition R22-1 (two differing torsions) [P; checked numerically].**  Let `X₂` arise from `X₁` by rotations
`R_j = rot(b_j, θ_j)`, `θ_j ∉ 2πℤ`, about two hinge bonds `b₁ ∦ b₂`, so that three segments `S₁, S₂, S₃` are shared
(consecutive ones share a hinge bond); assume each segment is non-planar with edge directions on no conic.  Let
`e = b₁ × b₂/|b₁ × b₂|` and `σ = I − 2eeᵀ` (the reflection in the plane of the two hinge directions).  Write a
re-hinged conformation as `(ρ₁, ρ₂)`: `S₂` is moved by `ρ₁`, `S₃` by `ρ₁ρ₂`, `ρ_j ∈ O(3)` fixing `b_j`.
(a) The conformations that are affine images of `z` are exactly the eight

    X₁ = (I, I),  X₂ = (R₁, R₂),  Y_i = (R₁, σ),  Y_ii = (I, σR₂),  Y_iii = (σ, R₂),  Y_iv = (R₁σ, I),
    Y_v = (R₁σ, σR₂),  Y_vi = (σ, σ);

so `φ` vanishes on six classes besides the states and Theorem G (a) fails.
(b) `D(X₁) − D(X₂) + D(Y_i) − D(Y_ii) + D(Y_iii) − D(Y_iv) + D(Y_v) − D(Y_vi) = 0`.
(c) If `R₁R₂` is not an involution and `(θ₁, θ₂) ≠ (π, π)`, the mixture `w₁δ_{X₁} + w₂δ_{X₂}` is identifiable for all
weights.
(d) If `θ₁ = θ₂ = π`, then `D(X₁) + D(X₂) = D(Y_v) + D(Y_vi)` and the mixture is **not** identifiable:
`(w₁ − t)δ_{X₁} + (w₂ − t)δ_{X₂} + tδ_{Y_v} + tδ_{Y_vi}`, `0 < t ≤ min w`, has the same `M`.  (`Y_vi` is `X₁` with its middle
segment mirrored, `Y_v` the same for `X₂`.)

*Proof.*  By Lemma 2.2 a competing state is `x = Az + t`, `A = [A₁ A₂]`.  On `S_j` the second state is `Q_j` times
the first (`Q₁ = I`, `Q₂ = R₁`, `Q₃ = R₁R₂`), so the edge vectors of `x` on `S_j` are `B_j v` with
`B_j = √w₁A₁ + √w₂A₂Q_j`, and `x ∈ 𝒞` iff `B_jᵀB_j − I` vanishes on the edge directions of `S_j`, i.e. `B_j ∈ O(3)`
(every `E₀`-edge lies in one segment).  Normalise `B₁ = I`, put `G = √w₂A₂`: `B_j = I + G(Q_j − I)`, `ρ₁ = B₂`,
`ρ₂ = B₂⁻¹B₃`.  Then `G(R₁ − I) = ρ₁ − I` fixes `G` on `b₁^⊥`, and `GR₁(R₂ − I) = ρ₁(ρ₂ − I)` fixes `G` on `R₁b₂^⊥`; the two
planes meet in the line through `R₁e`, on which the prescriptions must agree:
`(ρ₁ − I)α₁ = ρ₁(ρ₂ − I)β₂`, with `α₁ = 1/(1 − e^{−iθ₁})` in `b₁^⊥ ≅ ℂ` and `β₂ = 1/(e^{iθ₂} − 1)` in `b₂^⊥ ≅ ℂ` (`e ↔ 1`;
`Re α₁ = ½`, `Re β₂ = −½`).  The left side lies in `b₁^⊥`, and `ρ₁(b̂₂ × e)` has a non-zero component along `b₁`.
Going through the four components (`ρ_j` a rotation `e^{iφ_j}` or a reflection with normal `n_j ⊥ b_j`) gives two
solutions in each: rotation–rotation: `(e^{iφ₂} − 1)/(e^{iθ₂} − 1)` must be real, hence 0 or 1, and then `φ₁ = 0` or `θ₁`;
rotation–reflection: `n₂ ⊥ β₂` with `φ₁ = 0`, or `n₂ = e` with `φ₁ = θ₁`; reflection–rotation: `n₁ ⊥ α₁` with `φ₂ = 0`, or
`n₁ = e` with `φ₂ = θ₂`; reflection–reflection: `n₁ ⊥ α₁` and `n₂ ⊥ β₂`, or `n₁ = n₂ = e`.  The reflection with normal
`⊥ α₁` is `R₁σ`, that with normal `⊥ β₂` is `σR₂`.  This is (a).  With origins on the hinges, every squared distance
is affine in the triple `(ρ₁, ρ₂, ρ₁ρ₂)` (`|p − ρ₁q|²`, `|q − h − ρ₂r|²`, `|p − ρ₁h − ρ₁ρ₂r|²`), and the alternating sum
of the eight triples vanishes termwise: (b).  For (c), a competing `ν` is carried by the eight classes, with
weights `c ≥ 0`; equality of `M` is equality of the three averaged matrices (the segments are non-planar).  From
`E[ρ₁ρ₂]`: `aI + bR₁R₂ + γR₁σ + δσR₂ = 0` with `a = c₁ + c_vi − w₁`, `b = c₂ + c_v − w₂`, `γ = c_i + c_iv ≥ 0`,
`δ = c_ii + c_iii ≥ 0`.  `R₁σ = I − 2n₁n₁ᵀ` and `σR₂ = I − 2n₂n₂ᵀ` are symmetric, so the antisymmetric part gives `b = 0`
(`R₁R₂` is not symmetric); then `(a + γ + δ)I = 2γ·n₁n₁ᵀ + 2δ·n₂n₂ᵀ` has rank at most 2, so both sides vanish and
`γ = δ = 0`, i.e. `c_i = c_ii = c_iii = c_iv = 0`, `c₁ + c_vi = w₁`, `c₂ + c_v = w₂`.  From `E[ρ₁]`:
`(c_vi I + c_v R₁)e = 0`, so `c_v = c_vi = 0` unless `R₁e = −e`; in that case `E[ρ₂]` gives `(c_vi I + c_v R₂ᵀ)e = 0`,
impossible unless `R₂ᵀe = −e`.  (d) is the same computation read backwards:
`(I + R₁)(I − σ) = 0`, `(I − σ)(I + R₂) = 0`.  ∎

*Checks* (`t3c_linear_images.py`, 25 s; `probe_7of8.py`; `t3c_three_torsion_candidates.py`): in 8 instances
(`n = 14…26`) the eight predicted conformations are chains (edge errors `≤ 4·10⁻¹⁵`) and linear images
(`φ ≤ 5·10⁻²⁸`); the identity (b) holds to `5·10⁻¹⁴`; every image found by the enumeration is one of the eight
(3 200 + 9 000 starts; never an image outside the list); **the programme returns `1.000000000`** (all mass on the
true states) in 8 of 8.  In one instance the enumeration found 7 of the 8 — a small basin of attraction (in
1 500 starts some predicted points are hit 0–2 times); the missing point is verified directly.  Half-turns
(3 instances): identity (d) to `3·10⁻¹⁴`, `Y_v, Y_vi` at `d_P² ≥ 7.3` from the true states, programme
`0.260000000 = 1 − 2 min w`; at `θ = π − 0.01` it is 1 again.  **Control:** one torsion — 300 of 300 starts give
distinct images, programme 0 (a competitor, as it must be); generic pair at `n = 12` — only the two states.

**Three differing torsions [P up to a non-degeneracy that is six explicit numbers; N].**  The restriction of a
linear image to the first three segments is one of the eight of R22-1, which fixes `G`; it is a chain on the
fourth segment iff `I + G(Q₄ − I)` is orthogonal.  For the six spurious candidates the defect
`‖B₄ᵀB₄ − I‖_F` is `0.63 … 48` in five generic instances (and `≥ 0.73` when all three are half-turns); for the two
states `≤ 4·10⁻¹⁵`.  So `𝒫(z)` consists of the two states and the mixture is identifiable by Theorem B′ with
`dim 𝒩(z) = 3`.  The enumeration agrees: only the two states in 8 of 8 instances (`n = 18…32`).

**Route B** (`t3c_grid_lp.py`, 169 s; true states on the grid; LP1 = minimal mass on the two true states with
equal `M`; LP2 = minimal mass within one grid step of them with `|ΔM| ≤ ε` entrywise):

| case | grid, components, columns | rank of the data on the columns | LP1 | LP2 at `ε = 10⁻², 10⁻³, 10⁻⁴` |
|---|---|---|---|---|
| one torsion (control), 2 instances | 72, 2, 144 | 5 | **0** | 0, 0, 0 |
| two torsions, 4 instances | 24², 4, 2304 | 13 | **1.000000** | 0.89–0.94, 0.989–0.994, 0.9989–0.9994 |
| two torsions, proper component only | 24², 1, 576 | 9 | 1.000000 | 0.92, 0.992, 0.9992 |
| two half-turns | 24², 4, 2304 | 13 | **0.260000** (support: the two nodes `Y_v`, `Y_vi`, 0.37 each) | 0.18, 0.25, 0.26 |
| two half-turns, proper component only | 24², 1, 576 | 9 | 1.000000 — **misses the competitor** | |
| three torsions, 2 instances | 12³, 8, 13824 | 25 | **1.000000** | 0.971–0.978, 0.997–0.998, — |
| three torsions, all half-turns | 12³, 8, 13824 | 25 | 1.000000 | 0.956, —, — |

**The dual side: a linear certificate beyond `φ` exists on the re-hinging family [N]** (`t3c_dual_certificate.py`,
10 s).  Maximise `t` subject to `f = c₀ + ⟨Λ, D(·)⟩`, `f(X₁) = f(X₂) = 0`, `f(x_g) ≥ t·min_k d_P(x_g, X_k)²` on every grid
conformation, `|Λ_ij| ≤ 1`.  Two torsions (3 instances): `t* = 0.31, 0.64, 1.13`, whereas `φ`, normalised in the same
way, has growth `0` (`−2·10⁻¹⁴ … −4·10⁻¹⁴`: it vanishes at the mirrored images); three torsions: `t* = 0.75` against
`0.055` for `φ`.  **Controls:** one torsion and two half-turns give `t* = 0` (no certificate can exist).  With such
a `Λ`, every grid ensemble satisfies `∫ min_k d_P² dν ≤ (‖Λ‖₁/t*)·max_ij |M(ν) − M(μ)|_ij`, with `‖Λ‖₁/t* = 240 … 480` in
these instances.  This is a statement on the grid of re-hingings only; for inexact data the segments may deform
(request 5).

**Short segments [N]** (`t3c_short_segments.py`, 55 s; two instances per arrangement and chain length; every
competitor verified: residual `≤ 3·10⁻¹³`, edge errors `≤ 5·10⁻¹⁵`, its states at `d_P² ≥ 1.3` from the true ones):
see the table of F1.  In two "yes" instances of `(j, j+2)` the programme put a mass below `10⁻⁶` on two images at
`d_P² < 10⁻³` from the true states — the curve of linear images passes through the states.

**What `M` sees of `h` differing torsions** (`t3c_fourier_rank.py`; takes the coordinator's item (5) further)
[P for the count, N for the equality]: `M` depends on the distribution of the hinge angles only through
`E[ρ_a ⋯ ρ_b]` for runs of consecutive hinges; on the proper component the rank is `2h² + 1` — 3, 9, 19, 33 for
`h = 1, 2, 3, 4`, observed in 7 of 7 cases.  So `M` is a linear image of the `3^h` Fourier coefficients with indices
in `{−1, 0, 1}`, **and for `h ≥ 3` it does not see all of them** (19 of 27, 33 of 81).  With mirrored components
the ranks are 5, 13, 25.  Underlying fact [K]: the mean of a distribution of rotations lies in `conv SO(3)`, whose
proper faces have dimensions 0, 2, 5 — there are no edges, so a mean rotation never identifies a two-point mixture
(the hinge mechanism is the two-dimensional face).

---

## 4. Re-runs of their code

Scratch copy `ws_R22/rerun_copy/` (13 files; sha256 identical to the export; not committed).
`python3 -I -B rerun_copy/run_checks.py` fails with `ModuleNotFoundError: geomlib` — isolated mode does not put the
script directory on the path; this is not a defect of their code.  I used `rerun_launcher.py`, which adds exactly
the copy directory and runs the script as `__main__`, still with `-I -B`.  `mutation_checks.py` starts its children
itself (not isolated; bytecode writing disabled through the environment).

| script | result | their text |
|---|---|---|
| `run_checks.py` | 23 of 23 pass, 8 s | 23 tests ✓; "about one minute" (l.705) ✗ |
| `mutation_checks.py` | 11 of 11 caught, 13 s | ✓ |
| `hierarchy_example.py` | OK; deviation on `F` `1.8·10⁻¹⁵` | "to `10⁻¹⁵`" ✓ |
| `exact_conic_rank.py 12` | ALL OK, 32 s, 48 lines; `n₀ = 5, 12, 23, 39, 60, 85, 114, 148, 187, 230, 277, 329` | Theorem C (b) ✓; "96 witnesses" ✗ |
| `exact_jacobian_rank.py 8` | ALL OK, 30 witnesses, 2 s | ✓ |
| `exact_4d_extreme.py` | OK (rank 10, bond vectors span `ℝ⁴`) | ✓ |
| `demix.py` | state RMSD `≤ 7.7·10⁻⁸`; weights `1·10⁻¹⁵ … 5.8·10⁻¹²`; `s* = 6.9·10⁻³` (`n = 12`), `7.8·10⁻²` (`n = 16`) | "`≤ 2·10⁻⁷`" ✓; "weights to `10⁻¹³`" ✗; "`7·10⁻³`" ✓; "`9·10⁻²`" ✗ |

Their tests of Theorem G cover (a), the linearity, the **local** part of (b) (`quadratic_growth_local`: constants
0.040, 0.053 at `n = 14`, 111° — the same order as mine), the rank in (d) and the order `ε²` of `ΔM` in (e).  There
is no test of the global infimum.

---

## 5. The assumption table (AA1), row by row

Classes of the directive: essential / proof technique / computational convenience / replaceable by a weaker
quantitative condition / removal changes the complexity / removal makes the result false.

| assumption | their class | my class, and why |
|---|---|---|
| observable = average of the **squared** distance | essential (method void) | **Essential for the certificate and the algorithm; removal changes the complexity, not the form of the theory.**  For any continuous observable `Φ` the set of realizable data is `conv Φ(𝒞)`, identifiability is the face criterion of F7, and the stability bound holds with any non-negative certificate `c₀ + λ·Φ` that vanishes on the states with quadratic growth.  Lost: Lemma 2.2 (competitors are linear images), hence the rank test and DEMIX; the face test becomes a non-convex global problem.  The answer changes, and not only for the worse: adding the mean **fourth** powers `⟨d_ij⁴⟩` makes the one-torsion pair identifiable (the second harmonic of the hinge angle enters; programme over both circles: 1.000000 in 3 of 3, control with `⟨d²⟩` alone: 0; `t4_fourth_moment.py`) [N] |
| statewise constraints | essential | **Essential — removal makes the result false** (Proposition 3.1).  Hidden with it: the constraints are *exact* in every state (H-f); a thermal spread of bond lengths or angles re-admits the competitors of Proposition 3.1 at that scale [H], and no theorem here controls it.  Adding constraints (sterics) can only help: Theorem B holds on every subset of `𝒞` |
| exact data | convenience; replaced by Theorem G | **Replaceable by a weaker quantitative condition in principle; at present a theorem with a computationally vacuous guarantee** (F2): the constant is a global infimum; with the values found it is `≥ 10²–10³` and the bound is informative below `0.03–0.4 %` relative error.  It exists only under (CC) (or (H1), (H2)); for identifiable mixtures with further linear images (two torsions) the certificate gives nothing |
| finitely many states | proof technique? | **Essential — removal makes the result false** (F7): more than `1 + (n − 2)(n − 3)/2` shapes, or any continuous part, is never identified; a symmetric broadening is invisible at first order; under (CC) `K ≲ (2/3)√n` |
| genericity of the conformations | weaker quantitative condition available (a rank) | **Split it.**  As a certificate the rank is a correct, checkable, sufficient condition.  As a hypothesis of the *result* it is neither necessary nor harmless: the excluded set contains all states sharing rigid segments with at most three differing torsions; there the result is false (one torsion; two half-turns), true without the certificate (two torsions, three torsions with long segments), or instance-dependent (four-atom segment, three consecutive torsions).  The necessary and sufficient condition is Theorem B′, which is not a rank.  The headline should read "for conformations in general position" and name the hinge pairs as excluded |
| homogeneous bond geometry | convenience | **Agreed** (proof technique in Theorem C (c)); the sharp threshold is exact for two geometries and replicated here for `K ≤ 3` at one of them |
| complete averaged data | replaceable by a PSD stress on the measured pairs (Theorem F) | **Replaceable, by a condition whose availability is not characterised**: Theorem F needs a positive semidefinite stress of rank `n − 1 − dK` supported on `F ∪ E₀`; existence is shown only through trilateration bands (Theorem F′).  Removal changes the complexity (membership is NP-hard for general pair sets, their §8.1).  The experimental form — block sums `⟨C, M⟩` (SCI-RES-0029) — is not covered |
| labelled atoms | essential | **Agreed** |

Not in their table: (H-b) reflections of segments belong to `𝒞` — the six spurious images and the half-turn
competitor are mirrored conformations, so a chirality constraint would change §3.3; (H-c), (H-d), (H-f) of §1.
On physical relevance I add nothing to SCI-RES-0029: I opened no experimental source.

---

## 6. Prior art (A1)

Searches of 2026-11-26, 17:57–18:12 UTC; generic queries only (the twelve queries are in `NOTES.md`); nothing of
this project was put into a query and nothing was uploaded.  Reading levels: **[full text]** = I read the pages;
**[fetch]** = the page-fetching tool read the full text and returned quotations and a summary to me;
**[abstract]**; **[summary]** = search-engine summary only; **[memory]**.

| their statement | assessment | basis |
|---|---|---|
| Lemma 2.2, Theorem A | a formulation of known rigidity theory: edge directions on a conic at infinity ⇔ non-trivial affine flex; dimensionally rigid and not universally rigid ⇔ conic at infinity; super stability ⇒ universal rigidity; (equivalent frameworks of a dimensionally rigid framework are affine images — Alfakih [summary only]) | Connelly–Gortler–Theran, *Affine rigidity and conics at infinity* (arXiv 1605.07911) [fetch]: Definition 1.1, Proposition 1.4, the citation of Alfakih 2014, Theorem 4.2 |
| **Theorem B, Corollary 4.2** | **extension of a known theorem**; identical to it for `d = 1` with unit-diagonal constraints | Tropp, *Simplicial faces of the set of correlation matrices* (arXiv 1801.00749) [full text, pp. 1–8]: Fact 3.1 = Laurent–Poljak 1996, Theorem 4.2 [not opened]; Facts 2.6–2.8.  My two-line algebra for "(CC) ⇔ `Z` has full column rank" |
| Theorem B′ | a corollary of Lemma 2.2 and a standard face criterion; the question "how much weight can a state carry in any ensemble with the same averages" is studied for other averaged observables | Longinetti–Sgheri–Sottile, *Convex hulls of orbits and orientations of a moving protein domain* (arXiv 0712.3777) [fetch]: `p_max(R)`; "maximum occurrence" methods [summary] |
| Theorem C (thresholds), DEMIX | new as far as I can see | no match in searches S2, S4, S12 [summary] |
| Theorem D (a) | a corollary of the Barvinok–Pataki bound [memory]; **not** an extreme-Gram-dimension statement (F9) | E.-Nagy–Laurent–Varvitsiotis (arXiv 1205.2040) [abstract]: definition of the parameter |
| Theorem D (b) | new witness; the criterion "extreme ⇔ the dyads of the edge vectors span `Sym(r)`" is the classical one for correlation matrices | [summary]: quoted from Gribling–de Laat–Laurent (arXiv 1605.00988), Theorem 3.5 |
| Theorem F (`K ≥ 2`) | extension of super stability; singularity degree one ⇔ exposed minimal face | Drusvyatskiy–Pataki–Wolkowicz (arXiv 1405.2037) [fetch]: Theorem 4.1, Corollary 4.3; Connelly–Gortler (1401.7029), Gortler–Thurston (1001.0172) [abstracts] |
| **Theorem G (b)–(c)** | **a formulation of something known** (the localisation bound from a non-degenerate dual certificate); (a), `κ > 0` under (CC), (d), (e) specific | Fernandez-Granda, *Support detection in super-resolution* (arXiv 1302.3921) [full text]: Theorem 1.2, Lemmas 2.1, 2.3 |
| Theorem H | nothing found; identifiability thresholds of the type `2K − 1` exist for mixtures of products and grouped samples, a different problem | [summary] only |
| diploid-genome line | different model, correctly described by them: two copies in **one** frame, data = sums over the four copy pairs of **squared** distances; not identifiable from pairwise data; neighbouring-bead distances give uniqueness in 2D, not in 3D; three-way contacts give uniqueness in 3D | Belyaeva–Kubjas–Sun–Uhler (arXiv 2101.05336) [fetch]; Cifuentes et al., *Bull. Math. Biol.* 86:33 (2024) [abstract] |
| what `M` sees of relative orientations (§3.3) | the tautological orbitope `conv SO(3)` is the free spectrahedron of order 4; proper faces of dimension 0, 2, 5; the four-dimensional Carathéodory orbitope is 2-neighbourly | Sanyal–Sottile–Sturmfels, *Orbitopes* (arXiv 0911.5436) [fetch, first 100 000 characters]: Proposition 4.1, §4.1, Example 1.1 |
| Remark 2.3 | relative, as they say | Saunderson–Chandrasekaran–Parrilo–Willsky (arXiv 1204.1220) [abstract] |

Answers to their three questions (`PRIOR_ART.md` §4): (1) yes for `d = 1` — Laurent–Poljak; for `d ≥ 2` and chain
constraints I found nothing; (2) no — the cited theory covers star constraints and projections (F9); (3) nothing
found.  **Not opened:** Laurent–Poljak 1996; Alfakih 2007/2014; Connelly 1982, 2005; Barvinok 1995; Pataki 1998;
Li–Tam 1994; Saunderson–Parrilo–Willsky 2015; the maximum-occurrence papers; anything on trigonometric moment
problems.  An absence in twelve searches is not a proof of novelty.

Pointer (one line, not my object): the Ensemble division's Corollary E1.3 (b) — a random scaling, which breaks bond
lengths — is the unconstrained case of Proposition 3.1 here.

**Every URL opened** (page fetch; the two PDFs were then read page by page):
<https://arxiv.org/abs/1302.3921>, <https://arxiv.org/pdf/1302.3921>, <https://arxiv.org/abs/1801.00749>,
<https://arxiv.org/pdf/1801.00749>, <https://ar5iv.labs.arxiv.org/html/1605.07911>,
<https://ar5iv.labs.arxiv.org/html/0712.3777>, <https://ar5iv.labs.arxiv.org/html/2101.05336>,
<https://ar5iv.labs.arxiv.org/html/0911.5436>, <https://ar5iv.labs.arxiv.org/html/1405.2037>,
<https://arxiv.org/abs/1401.7029>, <https://arxiv.org/abs/1205.2040>, <https://arxiv.org/abs/2301.11764>,
<https://arxiv.org/abs/1204.1220>, <https://arxiv.org/abs/1001.0172>.

**A remark on their Theorem I** (`7c2a3d1`; not reviewed).  Its conclusion agrees with my enumeration for generic
pairs (§3.1).  Its genericity set excludes every hinge pair with at most two differing torsions — there the
linear images are 8, or infinitely many, at every `n` — so "a generic two-state ensemble is identifiable from
`n = 10`" does not cover them; for three differing torsions with long segments its conclusion holds numerically.

---

## 7. Requests to the Geometry division (can be sent as they stand)

1. **State the scope.**  Replace l.722–723 by the text of F1 and add "in general position" to summary item 3.
   Expected: a statement of which pairs of states are outside Theorem B.
2. **Prove or refute Proposition R22-1 and the three-torsion statement exactly**, with your Gröbner method on the
   structured family (two states that share segments; unknown `G ∈ ℝ^{3×3}` with `I + G(Q_j − I) ∈ O(3)`).
   Expected: degree 8 for two hinges, 2 for three hinges with long segments.  Validation: the eight explicit
   points of §3.3; the identity (b).  Stop if the scheme is positive-dimensional.
3. **Classify the short-segment cases** (differing torsions `j, j+2`; three consecutive): there the linear images
   form a curve and identifiability is instance-dependent in my runs (1 of 6, 3 of 4 non-identifiable).  Expected:
   a criterion (a sign condition on the curvature of the curve at the two forced points?) or a counterexample.
4. **Give Theorem G the hypotheses its proof uses** ((H1), (H2) of F8) and label (c)–(d) as existence statements
   (F2).  Then compute a certified lower bound of `κ` for one instance (`K = 2`, `n = 12`): interval
   branch-and-bound on the 9-torus of `φ(X) − κ₀·min_k d_P(X, X_k)² ≥ 0` outside balls around the states, eigenvalue
   bound inside.  Expected value: of order `10⁻³` (my search: `9.3·10⁻⁴` and `1.2·10⁻²` for two instances).
   Validation: the minimisers of `t3b_theorem_G.py`.
5. **A certificate beyond `φ`.**  For two differing torsions the mixture is identifiable but `φ` has six further
   zero classes.  A linear certificate `c₀ + ⟨Λ, D(x)⟩ ≥ 0` with quadratic growth exists numerically on the grid of
   re-hingings (`t3c_dual_certificate.py`: growth `0.3 … 1.1` at `|Λ_ij| ≤ 1`).  Prove a stability theorem for states
   that share segments.  Suggested route: Theorem G with `K = 1` on each shared segment (its restricted datum is
   one conformation with no conic, so `Σ_j φ_{S_j}` controls the deformation of the segments) plus a certificate of
   this kind on the re-hinging family.  Expected: `∫ min_k d_P² dν ≤ C‖ΔM‖` without (CC); it must fail for one
   torsion and for two half-turns (our controls give growth 0 there).
6. **Prior art:** cite Laurent–Poljak 1996 (Theorem 4.2) through Tropp 2018 (Fact 3.1) as the case `d = 1` of
   Theorem B and Corollary 4.2; cite the dual-certificate localisation bounds of super-resolution for
   Theorem G (b)–(c); correct l.573–574 (F9).
7. **Small corrections:** F4–F8, F10; the `K`-block step of Theorem B in Lean.

---

## 8. What I did not check; my own errors; files

**Not checked.**  The proofs of Theorems A (beyond the two implications used), C, D, E, F, F′, H, Proposition 6.1,
Corollary 9.1; Theorems I, J and everything else of the later checkpoints; their internal review
(`GEOMETRY-REV-0001`, not in the export).  The Lean file was read, not compiled.  `κ` was estimated from above
only; no lower bound.  "Exactly eight" and "exactly two" linear images rest on my paper derivation and on
floating-point enumeration with random starts, not on an exact elimination.  The short-segment outcomes are from
2–6 instances per arrangement.  The exceptional set of R22-1 (c) (`R₁R₂` an involution) was not analysed.  `K ≥ 3`
with shared segments was not studied.  Only one bond angle (cosine −1/3) in §3.2–3.3.  No experimental source
was opened.  Two sources were read only through the fetch tool's summary of the full text (marked [fetch]).

**My own errors.**  (1) The library self-test first compared a floating-point Procrustes residual with `10⁻²⁰`
(log in `not_cited/`).  (2) The first version of `t4_fourth_moment.py` measured the mass within 2° of the states,
which registers broadening, not competitors (log in `not_cited/`; window set to 15°).  (3) My enumeration misses
linear images with small basins (7 of 8 in one instance); without the paper prediction I would have reported 7.
(4) I first expected the grid programme alone to decide Item 3 (c); with exact equality it cannot see isolated
competitors off the grid — the linear images had to be put on the grid, and the mirrored components added.

**Files** (all in `experiments/science/ws_R22/` unless stated).
`NOTES.md`; `r22lib.py`, `r22lib_selftest_v2.log`; `t2_rigidity_rank.py/.log`; `t3a_cc_thresholds.py/.log`;
`t3a_below_threshold_images.py/.log`; `t3b_theorem_G.py`, `t3b_theorem_G_run1.log`; `t3c_linear_images.py`,
`t3c_linear_images_run1.log`; `probe_7of8.py/.log`; `t3c_short_segments.py/.log`; `t3c_grid_lp.py`,
`t3c_grid_lp_run1.log`; `t3c_dual_certificate.py/.log`; `t3c_fourier_rank.py/.log`;
`t3c_three_torsion_candidates.py/.log`;
`t4_fourth_moment.py`, `t4_fourth_moment_v2.log`; `t6_d1_dictionary.py/.log`; `rerun_launcher.py`,
`rerun_run_checks.log`,
`rerun_mutation_checks.log`, `rerun_hierarchy_example.log`, `rerun_exact_conic_rank_12.log`,
`rerun_exact_jacobian_rank_8.log`, `rerun_exact_4d_extreme.log`, `rerun_demix.log`,
`rerun_copy_sha256_original.txt`, `rerun_copy_sha256_copy.txt`; `rerun_copy/` (scratch copy, not committed);
`not_cited/` (two superseded logs).  Report: `docs/science/workstreams/R22_REPORT.md`.

**Tool actions declined:** none.

---

## Coordinator's note (2026-11-26 19:11 UTC)

*What I read.*  This report in full (582 lines).  Of the Geometry division's branch: GEOMETRY-MSG-0005 in full
and the diff of `docs/geometry/ENSEMBLE_RIGIDITY.md` between the commit reviewed (`d84a43b`) and their head
`e8e2582` — 27 hunks; inside §2, §4.2 and §7.2 only the label of Theorem B (a new machine-checked statement,
`mixture_state_of_conic`, for the `K`-block step — which settles the second half of finding F5 at their head),
the title of Theorem G and the title of §8 changed.

*What I checked myself.*  **Proposition R22-1 with code of my own**
(`experiments/science/geometry_checks/two_hinges.py`, log next to it; the chain builder of my earlier
`hinge_pair.py`, none of the referee's code; six random instances with 22 to 29 atoms, then four with two
half-turns): the eight conformations of (a) are chains (`3·10⁻¹⁵`) and affine images of the stacked pair
(`9·10⁻²⁸`); a search over all re-hingings — rotation or reflection at each hinge, a grid of 4°, every local
minimum of the residual refined to convergence — finds those eight and no other zero in six of six; the
alternating identity (b) holds to `9·10⁻¹⁴` (control: the unsigned sum is 55 to 403); the linear programme over the
eight classes returns `1.000000000` in general position, `0.260000 = 1 − 2 min w` for two half-turns (identity (d)
to `8·10⁻¹⁴`; the two competitors differ from both states by at least 12 in a squared distance), and 1 again at
`π − 0.3` (control).  The proof of (a) I read and did not redo line by line; my search is evidence, not a proof,
that the list is complete.  *Not checked by me:* the three-torsion statement, the short-segment table, the
numbers of F2 (`κ`), the prior-art readings, the re-runs of their harness.

*Their sixth checkpoint crossed the review (found at the fetch of 19:22 UTC).*  GEOMETRY-MSG-0006 (19:11 UTC, head
`cd4a2ec`) reports their own internal review (GEOMETRY-REV-0001; I read its list of findings and their response
table, not its 704 lines).  It found, independently of this referee, that `κ` lies 2 to 12 times below its local
value (F2 here), the wrong constant in the proof of G (d) (F8), and the hypothesis Corollary 4.2 was using; their
new Theorem G′ has as its hypothesis (H) the referee's (H1).  At their head these are repaired; still open there
are F1 (they count "at most 8 candidate chains" for two hinges and call the programme "not yet run"), F3 (prior
art at `d = 1`), F4, F6, F7 (c), F9, F10 — checked by me in their text at `cd4a2ec`.  SCI-REV-0021 §0 says this.

*Where this leaves our own SCI-RES-0029 §3.*  Part (a) there (one differing torsion: never identified) stands
and is used by the referee as a control.  Part (b) said that (CC) fails for two and three differing torsions and
that we did not know whether identifiability fails, expecting it to hold for two: **it holds for two torsions in
general position and for three with long segments, and fails for two half-turns** — the last we had not
expected.  Nothing there needs a correction; the open question is closed by this review.

*Process.*  The referee reports no declined tool action.  Its sources were opened through page fetches (two
papers read page by page); nothing of the project was put into a query.  It lists four errors of its own (§8),
among them that its enumeration alone would have reported seven of the eight images.

*Verdict.*  I accept the review: no critical finding; three major findings (the scope of the conic condition;
Theorem G (c)–(d) as an existence statement; prior art at `d = 1`), seven minor.  Published as **SCI-REV-0021**.
Proposition R22-1 and the hypotheses (H1), (H2) are the referee's own and are sent as proposals with their proofs.

*Not in the repository:* `ws_R22/rerun_copy/` (the Geometry division's scripts), `ws_R22/not_cited/`.
