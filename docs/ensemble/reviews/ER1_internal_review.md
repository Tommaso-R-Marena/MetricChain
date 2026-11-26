# ER1 — internal adversarial review of `ENSEMBLE_REPORT.md`, Theorems E1–E12

**Kind of review.**  Internal review by an independent AI session acting as an adversarial
referee.  It is not academic peer review.  Date: 2026-11-26.

**Object.**  Version 1 of the report (commit `a570520`), Parts I–III, statements E1–E12.  The
report was being edited while it was reviewed; every finding was re-checked against the
working tree at 17:42 UTC (`sha256 bc8e7165…`, "Version 2"; "working tree" line numbers
below are of that state).  There the statements and proofs of E1–E10 and E12 are unchanged
(a `diff` against `a570520` touches only the title of E7 and one sentence after E1.3), and
E11 has a new part (a).  Each finding says whether the working tree already answers it.
Material new in version 2 (E2.2, E2.3, E7′, §4.4, E13–E17, E15T) was **not reviewed**; §7
below has three remarks made in passing.

**Method.**  Every proof re-derived by hand.  Every statement attacked with independent
scripts (numpy/scipy, own code paths; listed in §5 with their outputs).  The two Lean files
type-checked (`lake env lean`, exit 0, no output) and their axioms printed.  Five citations
checked against secondary sources by web search (§4, §6).

---

## 0. Bottom line

* **No CRITICAL finding.**  None of the numbered statements E1–E12 is false, and no script
  found a counterexample to any of them.
* **Five MAJOR findings.**  Three are sentences of the summary and of the "reading"
  paragraphs that are false as written (F1, F2, F3), with explicit counterexamples.  One is
  the capacity bound of E11 (F4), which the working tree has already repaired.  One is a
  cited statement that does not say what the report makes it say (F5, E10(c)).
* **Thirteen MINOR findings** (F6–F18): a stale number, wording, unstated hypotheses,
  novelty classes, citations, three weak script checks.
* The part the authors flagged as most fragile — Part II, real algebraic geometry and
  genericity — is correct.  The errors are in the slogans drawn from it.

---

## 1. Verdict per statement

| statement | verdict | what was checked; remarks |
|---|---|---|
| E1(a) | **correct** | Cone argument, Stiemke step and the factorisation through `F → ℝ^S` re-derived.  3 000 random integer instances: direct fibre LP = certificate LP = cone test in 3 000/3 000; identification never depended on the weights |
| E1(b) | **correct** | Iterated exposure ends at `Φ^{-1}(G)`; "only if" (every point of `X_G` is an atom, hence `≤ m+1` points) is complete.  The paraphrase in the summary table is wrong: F7 |
| E1.1 | **correct** | Both bounds; 1 500 instances, two norm pairs, never violated |
| E1.2 | **correct** | `ω(τ)/√τ → 2.825` at `τ = 10⁻⁵` on a grid (claim `2√2 = 2.828`).  Only the lower bound is in the text: F9 |
| E1.3(a) | **correct** | |
| E1.3(b) | **correct** | `P_ν(Q=0) = ½ + ½P_μ(Q=0)` is right.  Wording and scope: F8 |
| E2(a) | **correct** | Sion applies (compact convex side is `P(X)`; affine continuous in `ν`, convex in `λ`); attainment for `τ > 0` by coercivity.  Gap `4·10⁻¹⁵` on 600 instances, `ℓ^∞` and `ℓ¹` data norms, `τ = 0` included |
| E2(b) | **correct** | Limit argument for `κ` is complete, including `κ = ∞`.  With a well-scaled LP: `ω(τ)/τ ≤ κ`, non-increasing, `= κ` at `τ = 10⁻⁶` to `2·10⁻¹⁴` on 2 370 cases |
| E2(c) | **correct**, small gaps | F10: continuity of `d(x⋆,·)`; "identify" needs `d(x⋆,y) > 0` |
| E3(a),(b),(c) | **correct** | `T₁` compact iff identified (its recession cone is the cone `T` of E1).  `H_τ = τT₁` for `τ ≤ τ₀` is true.  `ω_μ` computed directly from the vertices of the feasible set of `ν` (not through `T₁`): equality to `2·10⁻¹⁴` for `τ ≤ τ₀`, strict inequality in 301 of 320 cases with `τ > τ₀`; sup–min formula to `10⁻¹⁵`; no dependence on weights |
| E4 | **correct** | No measure-theoretic gap: `B ⊆ S` holds pointwise, not almost everywhere.  0 counterexamples in 729 searches at `m = K(r−1)+1`; non-uniqueness in 229/470 at `m = K(r−1)` |
| E4, sharpness | **correct** | Any `r` of the functionals are independent for generic `v_{k,i}` (the determinant is a non-zero polynomial as soon as two classes `k` occur).  Checked for ten `(K, r)` up to `(3, 5)`, and the explicit case `K=2, r=3` |
| E5(a) | **correct** | Real Zariski closures of polynomial images are irreducible (ideal = kernel of a map into a domain) with dimension the generic Jacobian rank; `B_K` is defined over the coefficient field |
| E5(b) | **correct** | Product of closures = closure of the product map, so irreducible over `ℝ`.  Local argument needs three neighbourhoods: F13 |
| E6 | **correct** | Again pointwise on a set of full `ν`-measure; no gap |
| E7 | **correct**, given the two citations | The cited connectivity theorem is confirmed (published abstract of Garamvölgyi–Gortler–Jordán).  `d = 1` is fine: the algebraic matroid of `(p_u−p_v)²` is the graphic matroid; the loss of signs is already in the variety.  20 graphs, exact ranks mod a prime, brute-force connectivity: no globally rigid graph on `≥ d+2` vertices with a disconnected matroid |
| E8 | **correct** | `f` has degree `2K` in each `ℓ_e²`; finiteness of the moments follows from the hypothesis; moments `0…K−1` on `K` distinct atoms fix the weights |
| E8.1 | **correct**, given Vitushkin–Henkin as quoted | Hahn–Banach step is right.  The original was not read by the authors or by me (§6) |
| E9 | **correct** (known) | All triples through a fixed vertex are simplicial faces for `n = 4…7` (LP); the Hadamard 4-set is not a face |
| E10(a) | **correct** | Also covers sub-supports (the Lean theorem has `supp μ ⊆ S`) |
| E10(b) | **correct** | Lemma 1 (Sperner on `B₃`, the three coefficients are non-zero by choice), Lemma 2, independence of the last `n−K'` rows: all right.  The bound exceeds 1 at the sizes simulated (`n ≤ 16`), so the simulation only checks the lemmas |
| E10(c) | **correct with gaps** | F5 |
| E11 (version 1) | **correct**; understated | F4.  Version 2's E11(a) checked: correct |
| E12(a) | **correct** | Also for `n = 2` (both ensembles are then single conformers) |
| E12(b) | **correct** | Count exact for any pivot rule; exact rational arithmetic on four ensembles including "soft" ones |
| E12(c) | **correct** | Cover's bound holds for points not in general position (cells of a central arrangement); a neighbourhood of size `< D` embeds in one of size `D`; exponent and `β(¼) ≥ 0.08` verified.  Remarks: F16 |

---

## 2. Findings

### F1 — MAJOR.  The "one sentence" of the summary is false in both directions

**Where.**  §0, "The thread through the three parts…" (v1 line 36; working tree line 43):
"an ensemble is determined by a family of observables **exactly when** it is *exposed* by a
non-negative function in their span".  Repeated in §5 item 2 (v1 line 704; working tree
1152): "what averaged data can determine is **exactly** the ensembles carried by the ground
states of an energy in the span".

**Why.**
1. *Exposed does not imply identified.*  `X = {a, b, c}`, `Φ = (0, 0, 1)`.  `f = Φ ≥ 0` has zero
   set `{a, b}`; `½δ_a + ½δ_b` has the data of `δ_a`.  Condition (i) of E1(a) is missing.
2. *Identified does not imply exposed on a compact `X`.*  The report's own Example E1.2:
   `δ₀` is identified and no non-negative function in the span has zero set `{0}`.
3. *"Carried by the ground states"* says nothing: every ensemble is carried by the ground
   states of `E = 0`.  The support must be the *whole* ground-state set.

**Correction.**  "On a finite `X` an ensemble is determined exactly when its support is the
whole zero set of a non-negative function in `span{1, Φ}` and the features are affinely
independent on it.  On a compact `X` the zero set is replaced by the minimal face, reached
by iterated exposure, and the stability is linear only in the exposed case."  Same edit in
§5 item 2.

**Working tree.**  Not answered.

### F2 — MAJOR.  "Identification = absence of chimeras" and "identified exactly when the zero set of `f` contains nothing but the conformers" are false

**Where.**  §3.2, last paragraph (v1 line 417; working tree 470).  §3.3, paragraph after
Corollary E8 (v1 line 484; working tree 552): "for marginal-law data the exposing function
is **always** [`f`], its zero set is the set of all splices that are realisable, and the
ensemble is identified **exactly when** that set contains nothing but the conformers".

**Why.**  Only "no realisable non-constant splice ⇒ identified" is proved (E6).  The
converse is false.  A chimera breaks identification only if chimeras can be combined into
a non-negative table with the right one-dimensional marginals — for instance two
complementary ones.

**Counterexample 1 (three points).**  `X = {x₁, x₂, y}`, two features, `F(x₁) = (0,0)`,
`F(x₂) = (1,1)`, `F(y) = (0,1)`.  `y` is a chimera.  Any `ν` with the laws of
`w₁δ_{x₁} + w₂δ_{x₂}` has `ν(x₂) = w₂` (feature 1) and `ν(x₂) + ν(y) = w₂` (feature 2), so
`ν(y) = 0`: identified.

**Counterexample 2 (frameworks, an open set of pairs).**  `G = K₄` on vertices `0…3` plus
vertex `4` joined to `0` and `1`, in the plane.

    x¹: (0,0), (2,0), (0.6,1.1), (1.6,−0.9), (1, 1.1180)       lengths 4–0, 4–1: 1.5, 1.5
    x²: (0,0), (5,0), (1.5,1.1), (4,−0.9),  (2.775, 1.1399)    lengths 4–0, 4–1: 3, 2.5

Index a splice by (conformer of the `K₄` block, of edge 4–0, of edge 4–1).  Realisable:
`(1,1,1)`, `(2,2,2)` and the three chimeras `(1,1,2)`, `(1,2,1)`, `(1,2,2)` (two circles
about `x¹₀, x¹₁` meet).  Not realisable: every splice with the block of `x²` and a pendant
length of `x¹` (`1.5+1.5`, `1.5+2.5`, `3+1.5 < 5`), and every mixed `K₄` block
(`|Cayley–Menger| ≥ 16`).  For a `ν` with the same eight edge-length laws: the block laws
give `v₂₂₂ = w₂`; the law of edge 4–0 gives `v₂₂₂ + v₁₂₁ + v₁₂₂ = w₂`; the law of 4–1 gives
`v₂₂₂ + v₁₁₂ + v₁₂₂ = w₂`.  So no mass on any chimera: `F_#ν = F_#μ`, for all weights.  All
inequalities are strict, so this holds on an open set of pairs (LP: 0 chimera mass for 20
perturbed pairs × 3 weightings; least squares realises the three chimeras to `2·10⁻¹⁵`).
Here `f` vanishes at the three chimeras, so `f` is *not* an exposing function, while
`1[ℓ₄₀ = ℓ₄₀(x²)] + 1[ℓ₄₁ = ℓ₄₁(x²)] − 2·1[ℓ₀₁ = ℓ₀₁(x²)]` (plus a penalty off the
conformers' values) is one.

**Correction.**  Replace both sentences by: "No realisable non-constant splice ⇒
identified.  Precisely, when the conformers have distinct values of every feature, `μ` is
identified (at the level of feature vectors) iff the only `v ≥ 0` on the realisable
colourings whose marginal on every feature is `(w_i)` is the diagonal one.  For a connected matroid and generic tuples there is no realisable splice
and `f` is an exposing function.  For a disconnected matroid identification fails on a
non-empty open set of pairs (E5(b)) and can hold on another."  The table row for E5 is
correct as it stands (it is about splices on the variety, for all generic tuples).

**Working tree.**  Not answered.

### F3 — MAJOR.  §5 item 3: "an identified `K`-conformer ensemble has correlation rank `K`" is false

**Where.**  §5 item 3 (v1 lines 710–715; working tree 1158–1163).

**Counterexamples (LP-verified).**  `n = 3`: `CUT₃` is a simplex, so the uniform ensemble on
all four conformers is identified; rank 3.  `n = 4`: the six vertices of the triangle facet
`x₁x₂ + x₁x₃ + x₂x₃ ≥ −1` (`+−−−, +−−+, +−+−, +−++, ++−−, ++−+`) form a simplex; `K = 6`,
rank 4.  `n = 5`: an identified 8-conformer ensemble, rank 5.

**Correction.**  "…has correlation rank `min(K, n)` at most, and exactly `K` on the event `𝓔`
of Theorem E10."  In the same item "fail beyond `6.34n`" contradicts the new E11(a): write
`2n`.

**Working tree.**  Not answered (both sentences still there).

### F4 — MAJOR for version 1; repaired in the working tree.  E11 and Problem O1

**Where.**  Theorem E11, the sentence after it, §8 "Asymptotics", §9 O1 (version 1).

**Why.**
1. Version 1 proves non-identification beyond `6.34n` "for equal populations".  By E1(a)
   identification depends on the support only, so the restriction was never needed.
2. The report's own argument for E12(c), used at one site with the full neighbourhood
   (`D = n−1`), gives much more: if `S` is the zero set of a non-negative pair function and
   no two elements of `±S` are neighbours, the labels `−x^a_1` of the points `x^a_{2..n}` are
   separable through the origin; probability at most `P(Bin(K−1, ½) ≤ n−2)`.  So beyond
   `(2+ε)n` nothing with full support on the conformers is identified.  O1's "known now"
   was `[1, 6.338]` and should have been `[1, 2]`.

**Working tree.**  Version 2 states exactly this as E11(a).  I checked its proof: correct.
Remaining edits:
* E11(b) and §8 still say "equal populations".  Drop it: if the uniform ensemble on `S` has a
  full-support twin, its data are in the interior of `CUT_n`, and so are the data of every
  ensemble with positive weights on `S` (a proper convex combination of an interior point
  and a point of the polytope).  LP check, `n = 6`: largest `t` with a representation
  `ν ≥ t` on the whole cube is `0.011` (uniform) and `0.005` (skewed weights), `K = 40`.
* Novelty class of E11(a): it is the classical capacity bound `α ≤ 2` of pair-interaction
  associative memories (Cover 1965; Gardner 1988) read through E1 — "synthesis", not "new".
* §5 item 3: see F3.

Face frequencies on small cubes (my LP, 60 trials each), consistent with §4.4:

| `n` | `K/n = 0.75` | `1.0` | `1.25` | `1.5` | `≥ 2` |
|---|---|---|---|---|---|
| 9 | 0.92 | 0.62 | 0.20 | 0.00 | 0.00 |
| 10 | 0.85 | 0.70 | 0.17 | 0.00 | 0.00 |
| 11 | 0.97 | 0.62 | 0.03 | 0.00 | 0.00 |

### F5 — MAJOR (easily repaired).  E10(c) is not what Odlyzko's theorem says

**Where.**  E10(c) (v1 line 567; working tree 675): "for `K ≤ n − 10n/ln n`,
`P(𝓔^c) = (1 + o(1))·4·C(K,3)·(¾)ⁿ`".

**Why.**
1. *Different event.*  Odlyzko's probability is that the span contains a `±1` vector other
   than `±v_j` (restated so by Irmatov, arXiv 2405.05082, Theorem 1.1).  `𝓔^c` also contains
   linear dependence, e.g. `x¹ = ±x²`, which is not in Odlyzko's event.
2. *Wrong form for small `K`.*  The theorem is additive:
   `4C(p,3)(¾)ⁿ + O(p⁴(5/8)ⁿ) + O((7/10)ⁿ)`.  For `K = 2`, `P(𝓔^c) = 2^{1−n}` exactly while the
   stated right-hand side is `0`.  A hypothesis `K ≥ 3` is missing.

**Missing step.**  Let `j` be the first index with `x^j ∈ span(x¹,…,x^{j−1})`.  Either
`x^j = ±x^i` (total probability `≤ K²2^{−n}`), or `x^j` is one of the spurious sign vectors
of that span, of which there are at most `2^{j−1}`; probability
`≤ 2^{j−1−n}·P(the span has a spurious vector) ≤ 2^{−10n/ln n}·O(K³(¾)ⁿ)`.  So
`P(dependent) = O(K²2^{−n}) + o(K³(¾)ⁿ)` and (c) holds for `3 ≤ K ≤ n − 10n/ln n`.

**Correction.**  "(c) [K + two lines] for `3 ≤ K ≤ n − 10n/ln n`,
`P(𝓔^c) = 4C(K,3)(¾)ⁿ(1 + o(1))`; for `K ≤ 2`, `P(𝓔^c) ≤ 2^{1−n}`."  The summary's
`1 − O(K³(¾)ⁿ)` stays true.  Simulation (3 000 trials): `(n,K) = (12,3)`: 0.137 against
0.127; `(14,3)`: 0.067 / 0.071; `(14,4)`: 0.221 / 0.285; `(16,4)`: 0.149 / 0.160.

**Working tree.**  Not answered.

### F6 — MINOR.  Check R5 quotes a number the script does not produce

§3.3 numerical checks: "all **22** zeros of the certificate".  `rigidity_checks.py`
(re-run by me, and `output.txt`) prints "**82** zeros found in 400 starts; 1 at conformer
1, 81 at conformer 2".  Fix the number.  The check is also lopsided — one hit at conformer
1; start some runs near each conformer.

### F7 — MINOR.  Summary row E1, compact case

"iff the minimal face … is a simplex with one configuration over each vertex" forgets
configurations over non-vertex points of the face.  `X = {a,b,c}`, `Φ = 0, 1, ½`: the face
`[0,1]` is a simplex with one configuration over each vertex, and `½δ_a + ½δ_b` has the
data of `δ_c`.  Use the wording of E1(b): "`Φ^{-1}(G)` is finite with affinely independent
features".

### F8 — MINOR.  E1.3(b) and "determine no ensemble at all"

* Exception: the ensemble with all edge lengths zero almost surely (for connected `G` it is
  determined).  The proof says so; the summary row does not.
* The twin `R·p` contains the collapsed framework (`R = 0`).  If degenerate frameworks are
  excluded, take `R² ∈ {½, 3/2}`: then `E_νQ² = 1.25·E_μQ²`, which needs `0 < E_μQ² < ∞`.
* Say once that "modulo congruence" means equality of the push-forwards to
  `(ℝ^d)^N / E(d)`.

### F9 — MINOR.  E1.2: exponent `½` is asserted, only `≥` is shown

Upper bound in one line (`ℓ^∞` errors): `∫_{t>0} t² dν ≤ τ/c` with `c = 4/π²`, so
`∫_{t>0} t dν ≤ √(τ/c)`, and `∫_{t≤0} |t| dν ≤ τ + ∫_{t>0} sin t dν`.  Hence
`ω(τ) ≤ τ + 2√(τ/c)`.

### F10 — MINOR.  E2(c): two unstated hypotheses

* For compact `X`, `ρ = d(x⋆,·)` must be continuous (upper semicontinuous suffices); an
  envelope need not be.  Add the hypothesis or state (c) for finite `X`.
* "Identify the conformation" needs `d(x⋆, y) > 0` for `y ≠ x⋆`; otherwise the conclusion is
  identification modulo `{d(x⋆,·) = 0}`.

### F11 — MINOR.  E3: degenerate case and novelty class

* If `T₁ = {0}` (one configuration), `τ₀` is `0/0`.  Say "`τ₀ = ∞` if `T₁ = {0}`".
* "New (not found)" is too strong.  `1/κ_μ` is the *minimum conic gain* of `A` on the
  tangent cone of the simplex at `μ` (Chandrasekaran–Recht–Parrilo–Willsky 2012,
  Proposition 2.2 gives `error ≤ 2δ/ε` under `‖Az‖ ≥ ε‖z‖` on the tangent cone; from
  memory), equivalently a Hoffman/calmness constant of a polyhedral system; that it depends
  on the active set only is standard there.  Suggested class: "formulation".

### F12 — MINOR.  §3.1: Heppes misquoted; the closing remark

* "Heppes (1956): the same in `ℝ^d`" reads as `K+1` *lines* in `ℝ^d`, which is false for
  `d ≥ 3`.  Heppes: `K+1` subspaces `H_j` with `H_i^⊥ ∩ H_j^⊥ = {0}`, i.e. any two projections
  determine the point (`r = 2` in E4).  The search confirms "`k+1` subspaces"
  (Fraiman–Moreno–Ransford, Theorem 1.1); the transversality condition is from memory.
* "`K(r−1)+1 ≤ |E|` forces `K = 1`": for frameworks modulo congruence two non-congruent
  configurations can agree on *all* edges, so `r ≥ |E|+1` and E4 gives nothing, not even
  `K = 1`.

### F13 — MINOR.  E5(b), local argument

"A neighbourhood `U`" cannot in general be one rank-chart box for the three maps.  Take
boxes `U₁, U₂` for `F_J`, `F_{J^c}` and a box `U ⊆ U₁ ∩ U₂` for `F`; then
`N = F(U) ⊆ N_J × N_{J^c}`, same dimension, so `N` is open in the product; conclude by
continuity of `(x, x') ↦ (F_J(x), F_{J^c}(x'))` at `(x₀, x₀)`.

### F14 — MINOR.  E7/E8: genericity is essential already for `d = 1`; a classical citation

* Non-generic counterexample (found by search): `C₄` on the line, `x = (8,0,3,5)`,
  `x' = (8,3,5,0)`: lengths `(8,3,2,3)` and `(5,2,5,8)`; the splices `(8,2,2,8)` and
  `(5,3,5,3)` both close up, so `½δ_y + ½δ_{y'}` has the four edge-length laws of
  `½δ_x + ½δ_{x'}`.  Worth one line next to the triangle example: the exceptional set is
  where conformers share arithmetic relations, not only shared lengths.
* E8, first step: "a `K`-atomic measure is the only non-negative measure with its moments
  up to order `2K`" is classical (Gauss quadrature; Karlin–Studden).  Cite it.

### F15 — MINOR.  E9: cite the right theorem

3-neighbourliness is stated in Ziegler, *Lectures on 0/1-polytopes* (for `COR(n) ≅
CUT(n+1)`, "best possible"; search summary).  The result of Deza–Laurent–Poljak (1992), as
far as the search summary and my memory of its abstract go, is about sets of cuts
"satisfying some additional assumption".  Obligation OB3 stands.

### F16 — MINOR.  E12: three remarks

* *The reading needs one more line.*  (b) says the pivot columns determine `C`; (c) bounds
  designs that carry a certificate.  "Certified identification costs `Θ(Kn)`" follows only
  with: the design `H` read by pivoted Cholesky determines `C` among all positive
  semidefinite unit-diagonal matrices, so on `𝓔` the `H`-data identify `μ`, so by E1(a)
  ("only if") a certificate supported on `H` exists.  LP check: 73/73 supports.
* `D = βK` must be an integer; state `D = ⌊βK⌋`.
* `β(¼) ≥ 0.08` is right but tight: the bracket is `−0.0214` at `β = 0.08` and changes sign
  at `β = 0.0834`.  With exact binomials the union bound is `e^{−1.9}` at `K = 100`,
  `e^{−21.9}` at `K = 1000`.

### F17 — MINOR.  §5 items 1 and 4 say more than is proved

* Item 1 (version 1): "the gap that the `(min,+)` kernel certifies is the stability
  constant".  E1.1 needs `γ`, `‖λ‖_*`, `σ` and `R`; the gap is one of four.  (The working
  tree restricts the item to finite spaces; the sentence about the gap is still there.)
* Item 4: "any rigidity result … is an ensemble theorem by Corollary E6".  E6 needs a
  polynomial (version 2: rational) parametrisation, *generic* conformers — no shared
  feature values — and concludes only `F_#ν = F_#μ`.

### F18 — MINOR.  Three checks in the repository scripts that check less than they say

* `exposedness_checks.py`, T2, the branch `κ = ∞`: `assert omega_primal(…, 0.0) > 1e-9 or True`
  can never fail.  Remove `or True` (on a finite `X`, `κ = ∞` does force `ω(0) > 0`; my
  version of the test passed on 600 instances).
* `pair_capacity_checks.py`, C2: the tolerance `max(0.5·pred, …)` accepts `0.278` against
  `0.401` (`n = 16`, `K = 5`).  The agreement is good only at the two sizes the report
  quotes (`n = 30, 36`), where the probability is small; say so, or tighten the test there.
* `rigidity_checks.py`, R5: see F6.

---

## 3. Lean statements against the report

Both files type-check with no output; all seven theorems depend on `propext`,
`Classical.choice`, `Quot.sound` only.

| declaration | matches the report? |
|---|---|
| `eq_of_exposing_certificate` | Yes: E1(a) "if".  Slightly more general (`supp μ ⊆ S`), which is what E10(a) uses for sub-supports |
| `mass_off_support_le` | Yes; needs no `γ > 0`.  Bound in the form `Σ|λ_i||Δ_i|` |
| `transport_le_of_sharp`, `identification_of_robust_certificate`, `robust_certificate_of_sharp`, `residual_advantage_le` | Yes for what the text of E2(c) claims.  Two qualifiers missing in the summary table and the register: **finite `X` only**, and the bound is `Σ|λ_i||Δ_i|`, which gives `‖λ‖_*‖Δ‖` for absolute norms only (the general-norm proof is the same line but is not what is checked) |
| `renyi_heppes` | Yes.  More general: `μ` need not be non-negative or normalised.  `r − 1` is natural subtraction; `r = 0` makes `hdet` unsatisfiable unless `X` is a subsingleton — harmless |
| `IsEnvelope` | Has no `d ≥ 0`; the report's definition has.  Harmless |

Not machine-checked, as the report says: E1(a) "only if", E1(b), E2(a),(b), E3, E4 for
general `X`.

---

## 4. Novelty classes

| item | report | assessment |
|---|---|---|
| E1 | known in substance | Agreed.  Donoho–Tanner (2005) is now in `PRIOR_ART.md` |
| E2(a),(b) | formulation | Agreed (duality for generalised moment problems) |
| E2(c) | "new as a statement" | Two lines; "formulation" as in the summary table is the right class |
| E3 | new (not found) | **Too strong**: F11.  "Formulation" |
| E4 | generalisation of a known theorem | Agreed, with a missing neighbour.  The support step is the standard lemma on **frameproof codes**: a code of length `ℓ` and minimum distance `d > ℓ − ℓ/c` is `c`-frameproof (Boneh–Shaw 1998, proof of Lemma III.2, as cited by Fernandez–Urroz, arXiv 2103.02341, §3; definitions in Staddon–Stinson–Wei 2001).  With `d = m − r + 1`, `c = K` this is exactly `m > K(r−1)`.  A splice is a *descendant*; "no chimera" is *frameproof*.  The statement about weights and measures is not in that literature as far as I know |
| E5(a), E6, E7 | new (not found) | I know no source.  In the vocabulary above: generic point sets of a variety with connected algebraic matroid are frameproof for every coalition size.  E5(a) is a dimension count |
| E8 | new (not found) | First step classical (F14); the rest is E7 |
| E8.1 | corollary | Agreed |
| E9 | known | Agreed |
| E10 | synthesis | Agreed.  Add Personnaz–Guyon–Dreyfus (1985) and Kanter–Sompolinsky (1987): the certificate is their projection-rule energy (from memory) |
| E11 | new; elementary | (a): classical capacity bound through E1, "synthesis" (F4).  (b): I know no source; the inner approximation `(2/π)arcsin` of the elliptope inside the cut polytope is standard |
| E12 | formulation / synthesis | Agreed |

---

## 5. Scripts and key outputs

Written in a session scratch directory (ephemeral; the counterexamples above are given
explicitly so that they do not depend on it).  *Note added by the division when the review
was filed:* the scripts and their output files were copied unchanged to
`docs/ensemble/reviews/ER1_scripts/`.  The lines below are condensed from the outputs; the
numbers are verbatim.

`part1_checks.py`, `part1_e2_rescaled.py`

    E1(a): direct LP == certificate == cone test in 3000/3000; identified 1524; cases where identification depended on the weights: 0
    E1.1: 1500 instances; max (lhs - rhs) mass bound: -6.08e-12; TV bound: -1.32e-07  (both must be <= 0)
    E1.2: tau, omega/sqrt(tau): 1e-02 2.7193 | 1e-03 2.7959 | 1e-04 2.8183 | 1e-05 2.8252   [2*sqrt(2) = 2.828]
    E2: duality gap 4.11e-15; dual infeasible at tau>0: 0; (kappa finite) != (delta identified): 0
    E2 rescaled: kappa finite 2370; omega/tau > kappa: 0; not non-increasing: 0; max rel |omega(1e-6)/1e-6 - kappa|: 1.62e-14
    E2.1: cube n=4: kappa (l_inf errors) = 4.000; kappa (l_1 errors) = 1.000
    E3: 80 identified supports; max rel |omega - kappa tau| for tau <= tau0: 1.88e-14; max (omega - kappa tau): 1.55e-15;
        sup-min at KR potential: 8.52e-16; random g exceeding kappa_mu: 0; weight dependence: 2.94e-14; strict beyond tau0: 301

(The first E2 run reported one violation at `τ = 10⁻⁵` and a 17 % slope error at
`τ = 10⁻⁶`.  Both were the solver's `10⁻⁷` feasibility tolerance; they vanish in the
rescaled programme.)

`part2_e4.py`

    r=2 (affine planes F_3^2, F_5^2): m = K+1: 0 counterexamples in 420; m = K: non-unique in 197/420
    r=3 (moment curve in F_5^3): m = 2K+1: 0 counterexamples in 50; m = 2K: non-unique in 32/50
    random r-determining codes, m = K(r-1)+1: 0 counterexamples in 259
    sharpness, explicit K=2, r=3: 3x3 minors of (1,0,1),(1,0,-1),(0,1,2),(0,1,.5): [2.0, 2.0, -1.5, -1.5]; all four laws equal
    sharpness K=3,r=3: min |det| over all 3-subsets 1.25e-02; K=3,r=4: 8.16e-04; K=3,r=5: 2.19e-03; law mismatch <= 4e-16

`part2_rigidity.py`

    K4, K5, W4, W6, K_{4,4} (d=2); K5, K6-e (d=3); C3, C4 (d=1): globally rigid, connected
    K_{3,3}, prism (d=2), octahedron (d=3), P4 (d=1): free matroid, not globally rigid
    two K4 glued along an edge (d=2), K_{5,5}, double banana (d=3): connected, NOT globally rigid
    K4 + degree-2 vertex: components [1, 1, 6]; two triangles sharing a vertex (d=1): [3, 3]
    violations of 'globally rigid on >= d+2 vertices => connected': 0
    connected matroids, 75 random splices each, smallest residual: W4 8.7e-03, two K4 1.9e-01, K_{4,4} 3.7e-01,
        K6-e 2.3e-01, double banana 1.3e-01  (true conformer: 3e-15); realised: 0
    separators, nearby pairs, both splices realised: K_{3,3} 34/40, prism 40/40, K4+vertex 40/40, octahedron 36/40
    C_3, C_4, C_5 on the line, Gaussian conformers: realisable non-constant splice in 0/2000
    C_4, integer conformers: realisable splice in 375, same-law twin ensemble in 300

(For the three graphs that are connected but not globally rigid, E6 applies and E7 does
not: the feature-vector ensemble is determined, the conformers only up to the fibres of
`F`.  That is what the report says.)

`chimera_vs_identification.py`

    toy: max chimera mass with the same laws, w=(.5,.5) and (.3,.7): [0, 0]
    K4 + degree-2 vertex, 20 pairs in an open set: realisable chimeras per pair: [3]; max chimera mass 0 in all cases
       chimeras realised to 1.9e-15, 2.3e-15, 1.8e-15; a non-realisable splice: residual 5.4
    control (nearby conformers): 6 realisable chimeras; max chimera mass, w = (0.5,0.5): 1.000

`part3_cube.py`, `e12_star_certificate.py`

    E9(a): n=4,5,6,7: triples through a fixed vertex that are simplicial faces: 21/21, 105/105, 465/465, 1953/1953
    E9(b): Hadamard ensemble: C = I; simplicial face: False
    identified with K > rank: n=3: K=4, rank 3; n=4: K=6, rank 4; n=5: K=8, rank 5
    E10(a): n=8: on E: identified in 55 (two weightings incl. a sub-support), failures 0
    Lemma 1: largest P(|<c,s>| = 1) over 200000 rational c: 0.7500
    Lemma 2: K=3,t=2: 0.180 <= 0.25; K=6,t=3: 0.078 <= 0.125; K=8,t=2: 0.096 <= 0.25
    E11: n=6, K=40: lambda_min(sin(pi C/2)) = +0.185; max |corr(sign g) - C| = 1.8e-03 (MC error 7e-04); 64/64 sign patterns
    E12(a): 56 cases, n = 2..7: failures 0
    E12(b): rank 3 / 5 (soft, 32 states) / 10 (soft, 512 states) / 4 (dependent conformers): entries read 24, 35, 45, 30
            = rn - r(r+1)/2; exact reconstruction with three pivot rules
    E12(c): sign points not in general position: max(count - bound) = 0; bracket at gamma=1/4: beta=0.08: -0.0214, 0.085: +0.0100
    largest admissible beta: gamma=1: 0.109; 0.5: 0.094; 0.25: 0.083; 0.1: 0.073; 0.01: 0.056
    certificate supported on the pairs read by pivoted Cholesky exists: 73/73

(A full-support ensemble on the cube has correlation rank `n`, so "soft and low rank"
means full support on the sign vectors of a subspace.)

Repository script re-run: `rigidity_checks.py` reproduces `output.txt`, including the line
quoted in F6.

---

## 6. Not settled

* **Vitushkin–Henkin (E8.1).**  I confirmed only the secondary statement (arXiv 1712.08286,
  Theorem 3.3: nowhere dense in `C(D)` for a compact connected `D ⊂ ℝⁿ` with non-empty
  interior).  Whether the 1967 text has exactly the hypotheses used (`q_i ∈ C¹` on `D̄`) I
  did not see.
* **Odlyzko (E10(c)).**  Confirmed through Irmatov's restatement, not the original (the PDF
  on the author's page returned an error).
* **3-neighbourliness (E9).**  Confirmed in a search summary of Ziegler's lectures and by LP
  for `n ≤ 7`; the monograph was not read.
* **Garamvölgyi–Gortler–Jordán.**  The statement is in the published abstract; the theorem
  number in the journal version was not checked.
* **Bai–Yin, Gortler–Healy–Thurston, Cover.**  Used as in the standard literature; not
  re-read.
* **Conjecture C1** was not examined.  One sanity remark: for linear `q_i` it is true —
  `g = ρ^{-1}·∂_{a_1}⋯∂_{a_m}ψ` with `a_i` tangent to the level sets of `q_i` and `ψ` a bump.

---

## 7. Remarks in passing on version-2 material (not reviewed)

* **E7′(a).**  "Connected iff `m ≥ D_d + 1`" is false for `m = 1`: `U_{1,1}` is connected.
  Then (c) for `m = 1` does not follow from E5(b) (there is no separator); it holds for the
  trivial reason that one leg length does not determine a pose.
* **E7′(b).**  The proof fixes the pose and then takes the further leg generic; the
  statement fixes generic attachment points first.  The exchange needs the usual
  dimension argument on the incidence set, or "generic" for the joint tuple.
* **E13(a)** needs a finite envelope.  For `d ≡ ∞` off the diagonal (the simplex, invoked
  in the next line for (b)) `δ_x` is extreme and its tight graph has no edge.
* I read the proofs of E13(b) and E17 once and saw no error; that is not a review.

---

## Sources consulted by search

* [Irmatov, arXiv 2405.05082 (restates Odlyzko's theorem)](https://ar5iv.labs.arxiv.org/html/2405.05082)
* [Fernandez–Urroz, arXiv 2103.02341 (frameproof lemma, attributed to Boneh–Shaw)](https://arxiv.org/abs/2103.02341)
* [Garamvölgyi–Gortler–Jordán, arXiv 2105.04363](https://arxiv.org/abs/2105.04363)
* [Ziegler, Lectures on 0/1-polytopes, arXiv math/9909177](https://arxiv.org/pdf/math/9909177)
* [arXiv 1712.08286 (quotes Vitushkin–Henkin as Theorem 3.3)](https://arxiv.org/pdf/1712.08286)
* [Vitushkin–Henkin, Russian Math. Surveys 22 (1967), Math-Net.Ru record](https://www.mathnet.ru/eng/rm5699)
* [Fraiman–Moreno–Ransford, arXiv 2201.07628 (Heppes' theorem)](https://arxiv.org/abs/2201.07628v3)
