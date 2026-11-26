# ER2 — internal adversarial review of `ENSEMBLE_REPORT.md`: the material new in version 2

**Kind of review.**  Internal review by an independent AI session acting as an adversarial
referee.  It is not academic peer review.  Date: 2026-11-26.

**Object.**  Version 2 of the report, commit `1a067b5` (every line number below is of that
commit): Proposition E2.2 and Remark E2.3 (§2.2); Theorem E7′ (§3.3); §4.4 with Conjecture
C2; Part IV (§4a: E13, E15, E15T, E16); Part V (§4b: E17); the Lean file
`proofs/Ensemble/ThermalUnionBound.lean` and its witness in `proofs/AxiomAudit.lean`; the
scripts `finite_temperature_checks.py`, `platform_checks.py`, `capacity_cutting_plane.py` and
the stored outputs `output.txt`, `output_threshold.txt`.  Nobody but the author had read
these parts.  The report was being edited while it was reviewed, and two further commits
were made (`32f547a`, "Version 3", Part VI; `8d42f60`).  Re-checked at 20:36 UTC against the
working tree (`sha256 6b1dc930…`): the reviewed passages (l. 293–324, 631–677, 945–985,
989–1251 and the summary rows E7′, E13–E17) are byte-identical to `1a067b5`; all changes lie
elsewhere (header, Parts I–III, the new Part VI, §6–§9).  The three scripts and the Lean
file are unchanged; the blocks F1–F6 and P1–P3 of `output.txt` are unchanged;
`output_threshold.txt` has gained an `n = 22` run and the Part VI runs and lost nothing.
Part VI (E18–E21) was **not reviewed**.

**Method.**  Every proof re-derived by hand.  Every statement attacked with my own code
(numpy/scipy/mpmath; nothing from `experiments/ensemble` is used in the attacks): exact
maximisation over class polytopes by one linear programme per subset of the state space;
vertices of class polytopes by brute force over bases; exact real-root counts for planar
platforms; evaluation at 40 digits at the vertices for one counterexample.  The repository
scripts were re-run and compared with the stored outputs, and the two face-decision
functions of §4.4 were compared instance by instance with mine.  The Lean file was
type-checked, its axioms printed and its statements instantiated.  Prior art by web search,
with the reading level stated for each source (§4).  "Exact" below means exact up to the
tolerances of the LP solver (HiGHS, `10⁻⁷` feasibility).

**Naming.**  "F1, F2, …" are the findings of this review.  The checks of
`finite_temperature_checks.py`, which have the same letters, are written "check F1", …,
"check F6".

---

## 0. Bottom line

* **No CRITICAL finding.**  None of the numbered statements E2.2(a),(b), E7′(a)–(c),
  E13(a)–(c), E15(a)–(d), E15T(a),(b), E16(a),(b), E17(a)–(c) is false.  The excess of every
  claimed inequality, maximised exactly over the class polytope, is `0` to `2·10⁻¹⁴` on
  every instance tried; no enumeration found a counterexample.
* **Four MAJOR findings**, of the kind ER1 found: false sentences *around* correct
  statements, and one check that does not print what the text quotes.
  F1: E15T's "and only then" — a triangle with a violated bond for which the bound holds
  exactly.  F2: the numbers quoted for check F6 are not the script's, and one quoted claim
  is not checked.  F3: "on a continuum the modulus is a square root" — it is `τ^{1/4}` for
  the observable `t⁴`.  F4: the last sentence of Remark E2.3 is false, and the remark is off
  by a factor two in one natural reading.
* **Twelve MINOR findings** (F5–F16): one mis-justified step in the proof of E7′(b); what
  "generic" excludes in E7′ (planar bodies: every pose has a mirror twin, for every number
  of legs); an unneeded hypothesis; wording; constants; script coverage; a missing Lean
  witness.
* The step the author flagged as most fragile — the dimension count on the incidence set
  in E7′(b) — is correct, except that the sentence giving the finiteness of the generic
  fibre proves less than it says (F5).
* **Novelty.**  The thermal union bound E15(c) and the second bound of E15T(a) follow in
  two lines from textbook facts: a monotone density with respect to a positively
  associated measure gives stochastic domination, a monotone coupling exists (Strassen),
  and a union bound over the coupling is the inequality (F11).  "New (not found)" should
  read "formulation".  The single-pose half of E7′(b) is known; the constants of E17 are
  weaker than those of the theory it cites.

---

## 1. Verdict per statement

| statement | verdict | what was checked; remarks |
|---|---|---|
| E2.2(a) | **correct** | A `C¹` energy with a minimum at an interior point has zero differential there, so no `λ` is feasible for `κ`; lower bound `c√τ` by the two-point ensemble.  LP on a grid of `[−1,1]`: `ω(10⁻⁵)/10⁻⁵ = 315` (`Φ = t²`), `5 623` (`t⁴`) |
| E2.2(b) | **correct** | Theorem E2(b) with `ρ = d²`.  `Φ = t²`: `ω(τ) = √τ` to four digits |
| E2.2, title and gloss | **false as written** | F3 |
| E2.3 | inequality **correct**; last sentence **false** | F4 |
| E7′(a) | **correct** | Line vectors of generic legs; fibre argument over the attachment points.  Ranks of all subsets, `d = 2` (`m = 1…5`), `d = 3` (`m = 1, 2, 5…8`), three instances each: uniform; connected iff `m = 1` or `m ≥ D_d + 1` |
| E7′(b) | **correct**; one step mis-justified | F5.  Semialgebraicity, the fibres of the bad set and the projection are right.  Plane, exact root count: the pose is the only one with its four leg lengths in 300/300 generic instances; 840 non-constant splices, none realised (smallest residual `3.9·10⁻³`, 1 % quantile `1.5·10⁻²`).  Space: no second pose and no splice found |
| E7′(c) | **correct**; says less than is true | F7.  Both complementary splices realised for 107 of 200 independent random pairs (`d = 2`, `m = 3`); explicit twin ensemble in §5 |
| E7′, non-generic attachment points | outside the statement; it **fails** there | F6 |
| E13(a) | **correct** | 66 random envelopes on 4 and 5 states (symmetric, asymmetric, with zero entries, without triangle inequality): 966 vertices by brute force over bases, all with connected tight graph; no proper mixture has one; 3 392 members built from spanning trees of tight constraints are all vertices |
| E13(b) | **correct** | Proof is a statement about any polytope.  10 464 (member, `Φ`) cases — vertices, midpoints, mixtures, centres; integer and Gaussian `Φ`, `m = 1…3`: fibre LP = exposed-face criterion in all (2 723 identified) |
| E13(c) | **correct** | LP duality; dual system feasible at `t ≥ max`, infeasible at `max − 10⁻³`, 330/330 |
| E15(a) | **correct** | Exact: `max_μ μ(x_i = a_i) − σ_i ≤ 4·10⁻¹⁶` |
| E15(b) | **correct**; not sharp | Exact on 30 instances (3 to 12 states, alphabets of 2–4 letters, general metrics): largest excess `+2.7·10⁻¹⁵`; local search up to 48 states.  F10 |
| E15(c) | **correct**, sharp | Exact on 87 instances, `n = 1…4`, heterogeneous slopes, non-uniform references: excess between `−1·10⁻¹⁶` and `+2·10⁻¹⁵`; equality at `μ*_{a'}` to `6·10⁻¹⁶`; local search on 5 and 6 sites |
| E15(d) | **correct** | 4 065 members for `n = 2, 3, 4` (all vertices for `n = 2, 3`, midpoints, mixtures, products, saturated × vertex): fibre LP agrees with "at most one unsaturated marginal" in all; every identified member is a product |
| E15, edge cases | **correct** | one site; a one-letter site; `b = 0`; `b = 30`; slopes `(0, 1, 12)`; zero distances; ties; `b = ∞` (the union bound).  Symmetry: F9 |
| E15T(a) | **correct**; hypothesis stronger than needed | 33 log-supermodular references (`n = 2, 3, 4`; chains, triangles, `K₄`, a three-body term): population bound, summed bound, and the ordered bound for all orderings (`n ≤ 3`): `≤ 3·10⁻¹⁵`.  Tree sentence: 194 (tree, order) pairs, `6·10⁻¹⁶`.  F1 |
| E15T(b) | **correct** as stated ("can fail") | Two-site counterexample in closed form (F1).  The converse in the title and the summary is false: F1 |
| E16(a) | **correct** | `n = 2, 4, 6`, three slopes, random gauges: LP optimum `= E_D[M²]` to nine digits; optimal face of dimension 0; tight graph of `D_a` connected |
| E16(b) | **correct** | `n = 3, 5, 7`: optimal face of dimension 1; every point found on it is `D(1 + θ sign M)`; `E[sign M]` ranges over `[−tanh(b/2), tanh(b/2)]`; `D_θ` just beyond is not a member |
| E17(a) | **correct** | Sion applies as in E2(a).  With the `ℓ²` norm (the repository checks `ℓ^∞` only), all ensembles and an envelope class: `|primal − dual| ≤ 1·10⁻¹⁵` (`m = 1`), `7·10⁻⁸` (`m = 2`), `1·10⁻⁶` (`m = 3`; solver accuracy) |
| E17(b) | **correct** | Risk `= σ²‖λ‖² + R²/4` exactly (attained at a vertex), `≤ ω(2σ)²/4`; simulated to 0.3 % |
| E17(c) | **correct**; weaker than the cited theory | `Φ_N(−1)/4 = 1/25.21 ≥ 1/25.3`; `√Φ_N(−1)/2 = 0.19916`.  F13 |
| §4.4, numbers | **all in `output_threshold.txt`** | Every entry of the table and every number of the text; the `n = 10` row reproduced exactly.  F14 |
| `capacity_cutting_plane.py` | **decides what it says** on every instance tested | 490 instances (`n = 10, 12, 14`): same answer as a float64 LP over all states, each answer certified from both sides.  F14 |
| Conjecture C2 | not examined beyond the data | F14 |
| Lean statements | **match the report** | §3; F16 |
| checks F1–F6, P1–P3 | reproduce the stored output exactly | F2, F8, F15 |

---

## 2. Findings

### F1 — MAJOR.  E15T: "the bound holds without frustration, **and only then**"

**Where.**  Title of Theorem E15T (l. 1108).  Summary row E15T (l. 41): "if the centre
violates a bond the bound is false (exact counterexamples on chains).  Frustration is the
obstruction".  `THEOREM_REGISTER.md`, row E15T(b): "with a violated bond both bounds fail".

**Why.**  Item (b) of the theorem says "can fail", which is true.  The title, the summary
and the register state the converse of (a), which is false.

**Counterexample.**  Three sites, `π ∝ exp(x₁x₂ + x₂x₃ − ½x₁x₃)`, no fields, centre
`a = (+,+,+)`, slopes `b₁ = b₂ = b₃ = 1`.  The bond `{1,3}` is violated (`J₁₃a₁a₃ = −½`), so
`π` and `μ*_a` are not log-supermodular in `e`.  Nevertheless

    max_{μ∈𝒫} { TV(μ, μ*_a) − Σ_i [μ*_a(x_i = a_i) − μ(x_i = a_i)] } = 0 ,
    max_{μ∈𝒫} max_i { μ(x_i = a_i) − μ*_a(x_i = a_i) } = 0 .

Both functionals are convex in `μ`, so the maxima are attained at vertices of the class
polytope.  For equal slopes these are `μ_g ∝ π e^{−bg}`, `g` one of the 38 integer height
functions on the 3-cube with `|g(x) − g(y)| ≤ 1` on edges and a connected set of tight
edges (enumerated by brute force; the same 38 points come out of a brute-force search over
bases).  Evaluated at 40 digits at the 38 vertices: both maxima are `0`, attained at `μ*_a`
only (`e15t_triangle_exact.py`); the exact LP over all 256 subsets agrees (`−1·10⁻¹⁶`,
`+9·10⁻¹⁶`; `e15t_interacting.py`, U4).  The same holds for `J₁₃ = −0.05, −0.1, −0.25` with
`J₁₂ = J₂₃ = 1`; for `(2, 2, −0.25)`; for `(½, ½, −0.1)` with `b = 1` and `b = 2`; for
`(1, 1, −0.1)` with `b = ½`.  In this example the intermediate, ordered bound of (a) holds
for four of the six orderings and fails by `5·10⁻⁴` for the two that begin with site 2.

*A second example in which everything in (a) holds.*
`π ∝ exp(x₁x₂ + x₂x₃ − 0.05x₁x₃ + 0.05x₁ − x₂ + 0.05x₃)` (in the disagreement variables:
`log π = 4e₁e₂ + 4e₂e₃ − 0.2e₁e₃ − 2(e₁ + e₂ + e₃)`), same `a` and `b`: the bond `{1,3}` is
violated, and the population bound, the ordered bound for all six orderings and the
summed bound hold to `2·10⁻¹⁵` (exact LP; U3).  Of six such triangles with fields, the
summed bound holds in six and the population bound in five.

**Reason.**  For the first reference `μ*_a` is positively associated in `e` although it is not
log-supermodular: `Cov(1_U, 1_W) ≥ 0` for all pairs of the 20 up-sets of `{0,1}³`, and it is
conditionally increasing in sequence for the ordering `(1, 3, 2)` (`e15t_association.py`).
Positive association is all that the population bound and the summed bound need (proof in
F11).  The induction in the report's proof needs only that, for the ordering used, the
conditional probability `q_i(e_{<i})` is non-decreasing — again weaker than
log-supermodularity.  The two satisfied bonds `1–2–3` induce an effective attraction between
`1` and `3` that outweighs the direct repulsion.

**What fails, in closed form** (so (b) can be **[P]**, not **[N]**).  Two sites,
`π ∝ exp(−½x₁x₂)`, `a = (+,+)`, `b = 1`.  In the order `e = (00, 01, 10, 11)`:
`μ*_a = (1, 1, 1, e^{−2})/(3 + e^{−2}) = (0.31894, 0.31894, 0.31894, 0.04317)`, and the member
with weights `w = e^{−e₁+e₂}` is `μ = (1, e², 1, 1)/(3 + e²) = (0.09626, 0.71124, 0.09626,
0.09626)`.  Then `μ(x₁ = a₁) = 0.80749 > μ*_a(x₁ = a₁) = 0.63789`, `TV = 0.44538`,
`Σ_i[…] = −0.16960 + 0.44538`, excess `+0.16960`; this is the exact maximum over the class.

**A third behaviour.**  `log π = e₁e₂ + e₂e₃ − ½e₁e₃`, `b = 1`: the population bound fails
(`+0.0257`) while the total-variation bound holds (maximal excess `1·10⁻¹⁵`).  So neither
"all bonds satisfied" nor positive association is necessary for the summed bound.

**Correction.**  Title: "…: the bound holds when the centre satisfies every bond; a violated
bond can break it".  Summary and register: "can fail (two-site example)", and drop
"Frustration is the obstruction" or replace it by the true statement: *the bound holds for
every reference for which `μ*_a` is positively associated in the disagreement variables —
in particular for log-supermodular ones — and can fail otherwise*.  Optionally restate
(a) with that hypothesis (and "conditionally increasing in sequence for the ordering" for
the first, ordered, bound).

### F2 — MAJOR.  Check F6: the numbers in the text are not the script's; one claim is not checked

**Where.**  §4a.2, last paragraph (l. 1155–1160): "the maximum …, computed exactly, is `0` to
`10⁻¹⁵` (six cases) … chains of three sites with one violated bond: `+0.23` to `+0.47`, and
there the population bound fails as well".

**Why.**  `finite_temperature_checks.py` (re-run by me: identical to `output.txt`) prints

    three sites, … every bond satisfied (6 cases, exact): max of TV - sum of deficits = +2.84e-14
    chains of three sites with one bond violated … (5 cases, exact): … = +0.965, +0.522, +0.024, +0.062, +0.294

1. The range is `+0.024` to `+0.965`, not `+0.23` to `+0.47`.  No script prints the quoted
   numbers.
2. "`0` to `10⁻¹⁵`" is `3·10⁻¹⁴`.
3. "There the population bound fails as well": the script computes the population excess
   and throws it away (`ising_reference_case(…)[0]`); it is neither printed nor asserted.
   The assertion of part (iii) is `max(wv) > 1e-3` on the total-variation excess only.

The claim itself is true: replaying the script's random stream and printing the second
return value gives `+0.560, +0.426, +0.186, +0.057, +0.173` for the five chains
(`repo_f6_population.py`).

**Correction.**  Quote the printed numbers; print the population excess in (iii) and assert
that it is positive.  This is the same defect as ER1 F6 and F18.

### F3 — MAJOR.  E2.2: "on a continuum the modulus is a square root"

**Where.**  Title of Proposition E2.2 (l. 293).  The paragraph after the proof (l. 309–312):
"on a continuous one it is Hölder of exponent `½` and certified by *quadratic growth*".  §5
item 1 (l. 1267–1269): "with a square-root modulus".

**Why.**  Items (a) and (b) are correct and say less: for `C²` observables the modulus is
*at least* `c√τ`; it is *at most* `√(κ₂τ)` when an energy in the span has quadratic growth
(`κ₂ < ∞`).  Without that the exponent is not `½`.

**Counterexamples** (LP on a grid of 4 001 points, `e22_e23_checks.py`).  `X = [−1, 1]`,
`x⋆ = 0`, `ρ = |t|`.
* `Φ(t) = t⁴` (`C^∞`; `δ₀` is identified; `κ₂ = ∞`): `ω(τ) = τ^{1/4}` exactly (Jensen, attained by
  `δ_{τ^{1/4}}`); computed `0.3162, 0.1778, 0.1000, 0.0562` at `τ = 10⁻², …, 10⁻⁵`.
* `Φ(t) = |t|^{3/2}` (`C¹`, not `C²`): `ω(τ) = τ^{2/3}`; computed exponent `0.68`.  So for `C¹`
  observables the modulus can be *better* than a square root, and "`ω ≥ c√τ`" does need `C²`.

**Correction.**  Title: "on a continuum the modulus is at best a square root, and the
certificate is a curvature".  Sentence: "on a continuous one it is at best Hölder of
exponent `½` for `C²` observables, exactly `½` when an energy in the span has quadratic growth
(`κ₂ < ∞`), and worse otherwise (`Φ = t⁴`: exponent `¼`)".  §5 item 1 likewise.

### F4 — MAJOR.  Remark E2.3: the last sentence is false; a factor two

**Where.**  Remark E2.3 (l. 317–324): "every statement of this part holds for data generated
by `Φ̃` with `τ` replaced by `τ + η` … a certificate cannot use that the ensemble avoids the
configurations where the model of the measurement is poor, because it does not know the
ensemble".

**Why.**
1. *The certificate can use it.*  A certificate bounds the mass off the support
   (Proposition E1.1), so the model error off the support enters multiplied by that mass.
   With `η_S = sup_S ‖Φ̃ − Φ‖`, `p = ν(X ∖ S)` and data generated by `Φ̃` within `τ` of `Aμ`:
   `γp ≤ λ·(Aν − Aμ) ≤ ‖λ‖_*(τ + η_S + (η − η_S)p)`, hence

       ν(X ∖ S) ≤ ‖λ‖_* (τ + η_S) / (γ − ‖λ‖_*(η − η_S))      when the denominator is positive.

   *Example.*  `X = {x⋆, y}`, model `Φ = (0, 1)`, certificate `λ = 1`, `γ = 1`; the truth is exact
   at `x⋆` and `|Φ̃(y) − 1| ≤ η = 0.5`.  Data within `τ = 0.01` of `Φ(x⋆)` force
   `p ≤ τ/(1 − η) = 0.02`.  The remark gives `p ≤ τ + η = 0.51`.  The error of the forward model
   enters through its supremum over the *certified support*, plus its supremum elsewhere
   times a mass that the certificate controls — not through its supremum over the
   configuration space.
2. *`τ + η` or `τ + 2η`.*  `τ + η` is right when the datum generated by `Φ̃` is compared with
   data *computed from the model* (`Φ(x⋆)`, `Aμ`).  If two ensembles are both seen through
   `Φ̃` — the reading of "identified" — the replacement is `τ + 2η`, and `2η` is attained:
   `X = {x⋆, y}`, `Φ = (0, 2η)`, `Φ̃ = (η, η)`.  Then `δ_y` and `δ_{x⋆}` have the same true data
   (`τ = 0`), `κ = 1/(2η)`, and `∫ρ dδ_y = 1 = κ·2η > κ(τ + η) = ½`.

**Correction.**  State which comparison is meant (and `2η` for the other); replace the last
sentence by the displayed bound.

### F5 — MINOR.  E7′(b): "a Jacobian of full rank at `g`, so the fibre through `g` is finite"

**Where.**  Proof of (b), l. 656–657.

**Why.**  Full rank at `g` shows that `g` is an isolated point of its fibre, not that the
fibre is finite: other components could have positive dimension.  The conclusion is true
for generic (legs, `g`), by either of:
* the map `Ψ : (legs, g) ↦ (legs, F(g))` is a dominant polynomial map between irreducible
  varieties of the same dimension, so its fibres are finite outside a proper algebraic
  subset of the source (dimension of fibres, on the complexification);
* the critical set `C` has smaller dimension, and so has the set of regular points mapped
  into `Ψ(C)` (a local diffeomorphism preserves dimension, and `dim Ψ(C) < dim` by Sard); off
  both sets every point of the fibre is regular, so the fibre is discrete, and it is
  compact (the leg lengths bound the translation).

The rest of the argument checks line by line: `B` is a projection of a semialgebraic set
(Tarski–Seidenberg); for `g' ≠ g` the legs with `|u − gv| = |u − g'v|` form a proper algebraic
set (the witness `u = gv`, `gv ≠ g'v` is right); the fibre of `B` over a generic (first `D_d`
legs, `g`) is a finite union of such sets; so `dim B < dim`, the attachment points over
which the slice of `B` has full dimension form a semialgebraic set of smaller dimension, and
its Zariski closure is proper.  The quantifier order now matches the statement.

**Correction.**  One sentence, as above.

### F6 — MINOR.  E7′: what "generic attachment points" excludes

Three explicit situations, none covered by the theorem, two of them the common ones
(`e7p_platform.py`, G6, G7).

1. **Planar bodies: (b) fails for every `m`, although (a) holds.**  If all `u_e` lie in a
   hyperplane `H` and all `v_e` in a hyperplane of the second body, let `S` be the reflection
   in `H` (coordinates with `H = {x_d = 0}` in both frames).  The pose `g' = (SRS, St)` is
   proper (`det = +1`), differs from `g = (R, t)`, and has the same leg lengths:
   `|u − SRSv − St| = |S(u − Rv − t)|` because `Su = u`, `Sv = v`.  Checked: `d = 2`, `m = 6`,
   collinear points; `d = 3`, `m = 9`, coplanar points: difference of the squared lengths
   `0`; the leg matroid is still uniform of rank `D_d`, hence connected.  This is the
   standard geometry of a Stewart–Gough platform (planar base, planar platform).  So no
   number of legs between two planar bodies determines one pose.  The matroid still gives
   the ensemble of leg-length vectors (Corollary E6); what fails is the second step, from
   leg lengths to poses.  **Connectivity of the matroid is not the whole criterion** — to
   be kept in mind for Problem O3, which is phrased in terms of connectivity alone.
2. **`d + 1` legs at one attachment point: the matroid disconnects.**  `d = 2`, `m = 4`,
   `u₁ = u₂ = u₃ = (0,0)`, `u₄ = (2, 0.5)`, `v = (1,0), (0,1), (−0.7,−0.4), (0.3,1.5)`: ranks
   `2 + 1 = 3`.  Poses `(θ, t)`: `g₁ = (0.3, 0.8, −0.4)`, `g₂ = (−0.9, −0.6, 1.1)`,
   `h₁ = (−1.543798, −0.600885, −0.662523)`, `h₂ = (−1.065024, −0.411145, 1.183621)`; squared leg
   lengths `g₁: (3.092122, 0.562898, 1.040355, 2.227041)`, `g₂: (0.100749, 2.99755, 3.777456,
   3.217239)`, `h₁`: the first three of `g₁` and the fourth of `g₂`, `h₂`: the reverse.  So
   `½δ_{g₁} + ½δ_{g₂}` and `½δ_{h₁} + ½δ_{h₂}` have the same four laws with `m = D₂ + 1`.  Both
   splices are realised for 47 of 100 random pairs.  `d = 3`, `m = 7`, four legs at one
   point: ranks `3 + 3 = 6`; both splices realised for 6 of 10 pairs of poses at distance
   `0.05`.
3. **Sharing that keeps the matroid uniform is harmless** in the cases tried (`u₁ = u₂`;
   `u₁ = u₂` and `v₃ = v₄`, 40 instances each: pose unique in 40/40, no splice realised among
   560; three pairs of legs sharing base points in space: matroid uniform, no second pose
   with the seven lengths).

**Correction.**  One sentence after the theorem: genericity excludes two planar bodies
(mirror pose, any `m`) and `d + 1` legs at a point.

### F7 — MINOR.  E7′(c): "(for `m = 1` not even one pose is determined)"

**Where.**  l. 643.

**Why.**  The parenthesis suggests that for `2 ≤ m ≤ D_d` single poses are determined and only
pairs fail.  For every `m ≤ D_d` no generic pose is determined: for `m < D_d` its fibre has
positive dimension; for `m = D_d` the fibre of a generic pose has an *even* number of real
points, hence at least two.  Plane, `m = 3`, exact count on 300 generic instances: 2 poses
in 143, 4 in 140, 6 in 17, never 1.  Space, `m = 6`: 4, 6, 4, 2 poses found by multi-start
(lower bounds).  This is the parity of the degrees 6 and 40 of the forward kinematics
(**[K]**, search summary and memory): non-real solutions come in conjugate pairs.  What
E5(b) adds for `2 ≤ m ≤ D_d` is that the ensemble of *leg-length vectors* is not determined
either, for all positive weights (take masses `(w − ε, 1 − w − ε, ε, ε)` on `x, x'` and the
two chimeras).

**Correction.**  "(for `m ≤ D_d` not even one generic pose is determined; for `2 ≤ m ≤ D_d` the
ensemble of leg-length vectors is not determined either)".

### F8 — MINOR.  E7′: the rewritten step has no check in the repository

P1–P3 test the matroid and the absence of splices — the half of (b) that is Theorem E5(a).
They do not test that a generic pose is the only pose with its `m` leg lengths, which is
the step whose proof was rewritten.  My G2 and G5 do (§5).  The text describes P1–P3
accurately; the register lists them as the evidence for E7′ without this caveat.  The
assertions of P2, P3 (`worst > 1e-5`, `worst > 1e5·sanity`) are not vacuous; the observed
minimum `1.9·10⁻³` is a sample from a distribution with positive density at `0` (mine, exact
in the plane: minimum `3.9·10⁻³`, 1 % quantile `1.5·10⁻²` over 840 splices), not a gap.

### F9 — MINOR.  E15: symmetry of the site envelopes is an artefact of the notation

**Where.**  §4a.2: "every `δ_i` a metric on `A_i` (symmetric)"; `μ*_{a,i}(s) ∝ π_i(s)e^{−δ_i(a_i,s)}`.

**Why.**  Symmetry is used once, to write `δ_i(a_i, s)` for `δ_i(s, a_i)`.  The class bounds
`w(a_i, ·) ≤ e^{δ_i(s, a_i)} w(s, ·)`, so the member most polarised towards `a` is
`∝ π e^{−d(·, a)}`.  With `μ*_{a,i}(s) ∝ π_i(s) e^{−δ_i(s, a_i)}`, (a) and (b) hold for arbitrary
site envelopes with the triangle inequality: exact on 30 non-symmetric instances (member
30/30, excesses `≤ 2·10⁻¹⁵`).  With the formula as written they fail: member in 3/30,
(a)-excess up to `+0.40`.  *Example:* one binary site, `δ(0,1) = 2`, `δ(1,0) = 0.5`, uniform
reference, `a = 0`: the written `μ*` has `μ*(a) = 0.8808` and is not in the class; the largest
`μ(a)` over the class is `1/(1 + e^{−0.5}) = 0.6225`.

**Correction.**  Define `μ*_a ∝ π e^{−d(·, a)}` and drop "(symmetric)", or keep the hypothesis
and say that it is only notational.

### F10 — MINOR (remarks on sharpness; data for Problem O7)

* (b) is not sharp.  The best constant `c` in `TV ≤ c Σ_i[1 − μ_i(a_i)/σ_i]`, by bisection on
  exact maxima: two binary sites `0.7042 = max_i σ_i` (this is (c)); one ternary site
  `0.9690`; two ternary sites `0.9153`; binary × ternary `0.8481`.
* The form (c) is false for sites with three letters (it is not claimed).  One site, three
  letters, uniform reference, discrete metric with `δ = 1`, `a = 0`: `μ*_a = (0.5761, 0.2119,
  0.2119)`; the member `μ = (0.4223, 0.4223, 0.1554)` has `TV = 0.2104 > σ − μ(a) = 0.1538`.
  Over 30 instances the maximal excess of the (c)-form ranges from `+0.013` to `+0.353`.
* A sharper form of (b) comes out of the proof in F11: at one site with density
  `ρ ≥ ρ(a)`, `TV = Σ_s μ*(s)(1 − ρ(s))₊ ≤ (1 − ρ(a))·μ*{ρ < 1}`.

### F11 — MINOR (novelty; the remark with the most consequence for the presentation).  E15(c) and E15T(a) in two lines

Write `e_i = 1[x_i ≠ a_i]`; `r = μ/μ*_a` is non-decreasing in `e` (the report's first step).

*Summed bound and population bound.*  If `μ*_a` is positively associated in `e` — Harris'
inequality for a product reference, the FKG inequality for a log-supermodular one — then
`E_μ g = E_{μ*}[rg] ≥ E_{μ*}g` for every non-decreasing `g`: `μ` dominates `μ*_a`
stochastically (`g = e_i` is the population bound).  By Strassen's theorem there is a
coupling `(Y, X)` of `(μ*_a, μ)` with `Y ≤ X`.  Then

    TV(μ, μ*_a) ≤ P(X ≠ Y) ≤ Σ_i P(Y_i = 0, X_i = 1) = Σ_i [μ(e_i = 1) − μ*_a(e_i = 1)] .

The "thermal union bound" *is* a union bound, over a monotone coupling.  In other words:
for stochastically ordered measures on `{0,1}ⁿ`, total variation is at most the Hamming
transport distance, which equals the sum of the differences of the one-site marginals.

*Ordered bound of E15T(a), and E15(b).*  For any two measures,
`TV(μ, ν) ≤ Σ_i E_{x_{<i}∼μ} TV(μ(x_i ∈ · | x_{<i}), ν(x_i ∈ · | x_{<i}))` (chain rule; sequential
coupling).  With monotone conditional densities the `i`-th term is
`E_μ h_i − μ(x_i = a_i)`; for a product `μ*_a` and any alphabets it is at most
`1 − μ(x_i = a_i)/σ_i` (F10, third item).

*The Lean statement* `E|r − Er| ≤ 2Σ_i Cov(r, e_i)` for monotone `r` is the same fact; it is
also the `L¹` Efron–Stein inequality with "influence = covariance for monotone functions"
(for indicators: the Poincaré inequality `Var f ≤ I[f]` with `Inf_i[f] = f̂(i)`; layer-cake
for general `r`).

So the analytic content is textbook, and the hypothesis that the proof needs is positive
association, not log-supermodularity (F1).  What the report adds is the observation that
the members of a first-order class have a monotone density with respect to the most
polarised member — i.e. that the class lies stochastically above `μ*_a` — and the reading.
I did not find the combined inequality stated in print (searches in §4), but I would not
class two standard steps as "new (not found)".  Suggested class: **formulation**; and give
the coupling proof, which is shorter than the martingale one and explains the name.

### F12 — MINOR.  Part IV: three sentences that say more than E13 does

* Summary row E13 (l. 39): "a member is extreme iff its tight graph is connected" omits
  "for a finite envelope" (ER1's remark was applied in the theorem only).
* Reading of Part IV (l. 1201–1205): "the ensembles that averaged data can identify are
  again the *exposed* ones, and at finite temperature these are the members whose residual
  is as steep as the envelope allows along a connected set of pairs".  By E13(a) the
  second clause describes *extreme* members; identified members need not be extreme.
  `n = 2`, `b = 1`, `μ = μ*_{+,1} ⊗ uniform`: one unsaturated marginal, identified by one-body
  data (E15(d)); its tight graph has the two components `{x₂ = +}`, `{x₂ = −}`.  Likewise
  `D_{a,θ}` with `|θ| < tanh(b/2)` in E16(b).  Correct wording: "members of exposed faces on
  which the data are injective".
* "What cannot be identified are members in the interior of the class" (l. 1205–1206)
  holds for fewer than `|X| − 1` independent observables; say so.

### F13 — MINOR.  E17: the constants, and what check F5 covers

* The cited theory gives a better lower bound than (c).  In the notation of the lecture
  notes I read (§4): `R*_A(σ) = sup_ε (ω(ε)²/4)·σ²/(σ² + ε²/4)`, so `R*_A ≥ ω(2σ)²/8`, and
  `R*_A ≤ 1.25 R*_N`.  Hence the minimax risk is at least `ω(2σ)²/10`: root-mean-square error
  at least `0.316·ω(2σ)`, against the report's `0.199`.
* The elementary two-point argument also gives more if the Bayes risk is computed instead
  of bounded by a test: the minimax risk of the pair `(μ₀, μ₁)` with `‖A(μ₁ − μ₀)‖ = 2σ` is
  `(Δ²/4)·E sech²(1 + Z) = 0.4496·Δ²/4` (`Z` standard normal; quadrature, and simulation of
  the Bayes rule to 1 %), i.e. `0.335·ω(2σ)`, against `Φ_N(−1) = 0.1587`.
* The statement "between `0.199·ω(2σ)` and `0.5·ω(2σ)`" is correct as it stands.  In the toy
  model `X = {0,1}`, `T = p`, the upper end is attained as `σ → ∞` (`0.4975·ω` at `σ = 5`).
* Check F5 tests (a) only, with the `ℓ^∞` norm and for the class of all ensembles; the text
  says "with the `ℓ^∞` data norm", correctly.  (b) and (c) have no check in the repository
  (the register says so).  Mine: §5, N2–N5.

### F14 — MINOR.  §4.4: the script is sound in practice; remarks on the text

* **Soundness.**  "Not a face" is returned when the optimum of a relaxation is `t ≤ 10⁻⁷`;
  "face" when every non-conformer energy exceeds `c` by `10⁻⁵`, energies in `float32`.  Both
  are sound if true margins are far from these thresholds, and they are: over 171 faces
  at `n = 10, 12, 14` the optimal margin (with `|Q_ij| ≤ 1`) is at least `1.7·10⁻²`; at the
  moment the script answers "face" (`n = 12`, 91 answers) the `float64` gap between the
  lowest non-conformer and the highest conformer is at least `5.0·10⁻³` and the conformers'
  energies agree to `6·10⁻¹⁴`; the `float32` error is `≤ 2·10⁻⁶`.  On 490 instances the script
  agrees with a `float64` LP over all states, and on each instance exactly one of the two
  certificates exists (margin `> 0`, or a signed measure orthogonal to `span{1, Φ}` and
  non-negative off the support — Theorem E1(a)).  The function of
  `capacity_threshold.py` agrees with mine on 400/400 instances.
* **Two soft spots** that never fired: `res.status != 0` is counted as "not a face" (0 of
  1 264 solves; the LP is always feasible and bounded, so any other status is a solver
  failure and should be "undecided"); the `float32` threshold `10⁻⁵` would be marginal for
  a certificate with a margin of that size (use `float64` at acceptance).
* **"Validated against the first at `n = 12`"** (l. 952–953) is a comparison of two
  frequencies on *different* instances (`0.733` on 60 against `0.677` on 300).  The
  instance-wise validation is the one above.
* **Reproducibility.**  The rows `n = 10, 12, 14` and the stability runs `n = 40, 60` come
  from drivers that the output file describes in words ("driver below") but that are not
  in the repository.  The obvious driver reproduces the `n = 10` row exactly
  (`0.875, 0.787, 0.613, 0.383, 0.253, 0.072, 0.022`); store it.
* **Wording.**  "The threshold is **not** `1`" (l. 969) is an extrapolation from `n ≤ 20`; at
  `K ≈ 1.1n` the frequency is flat (`0.66, 0.62, 0.63`, and `0.58` at `n = 22`), which supports
  it but is not a proof — the section says "neither is a proof", the sentence does not.
  The point of frequency one half is not monotone in `n`: about `1.05, 1.10, 1.13, 1.15,
  1.14, 1.12` for `n = 10, …, 20` and `1.10–1.11` at `n = 22` (the run added to the output
  after version 2); "moves from … to …" should not be read as a trend.  "No positive
  semidefinite certificate can exist" beyond `n` means: no certificate that is a sum of
  squares of linear forms vanishing on the conformers; on the cube every pair certificate
  is a positive semidefinite form minus a constant.

Every number of the table and of the text of §4.4 is in `output_threshold.txt`; my own LP
on fresh instances reproduces the rows `n = 10, 12` within `2.3` standard errors (14
entries).

### F15 — MINOR.  Checks F1, F3, F4 test less than a reader would assume

* Check F3 ((d), 60 members) tests product measures and products times
  `1 + 0.02x_ix_j` only: no vertex of the class and no other non-product member.  A
  non-product member identified by its marginals would not be seen.  (Mine: 4 065 members
  including all vertices for `n = 2, 3`.)
* Check F4, odd `n`: the assertion is `spread > 1e-4` plus "the two end points are optimal
  members".  It does not test that the optimal face *is* the segment; a larger face
  containing it would pass.  The text's "exactly the predicted spread `0.1102`" rests on a
  printed `1.10e-01`.  (Mine: dimension of the face `= 1` and every face point on the
  segment, `n = 3, 5, 7`.)
* Check F1, sampled part: the 360 pairs have excess `≤ −0.10`; they are nowhere near the
  extremal members.  Only the `n = 3` part is a test of sharpness; heterogeneous slopes and
  non-uniform references, which (c) claims, are not tested.  (Mine: exact for `n ≤ 4`.)
* The text of check F1 uses `P_a` and `τ_i`, the script's names, which the report does not
  define (`P_a = μ*_a`, `τ_i = σ_i − μ(x_i = a_i)`).
* No assertion ends in `or True`; no tolerance is loose enough to pass a false statement
  of the kind tested.

### F16 — MINOR.  Lean: `thermal_union_bound_density` has no witness

The witness `ensemble_thermal_union_bound_witness` instantiates `thermal_union_bound`
(`r` = number of excited sites, `E r = 5/6`).  The density form has the extra hypothesis
`prodE ps r = 1`, which the witness does not satisfy.  It is satisfiable non-trivially
(`r = (6/5)·count`; checked in `ER2_lean_audit.lean`, `er2_density_witness`); add it.
The monotonicity hypothesis quantifies over lists of every length; this costs nothing
(extend by a constant on other lengths) but is worth a line in the docstring.

---

## 3. Lean statements against the report

`lake env lean proofs/Ensemble/ThermalUnionBound.lean`: exit 0, no output.  An audit file
that imports the module, prints axioms and adds instances (`ER2_scripts/ER2_lean_audit.lean`;
exit 0): `thermal_union_bound`, `thermal_union_bound_density`, `thermal_union_bound_sharp`
and the witness depend on `propext`, `Classical.choice`, `Quot.sound` only.

| declaration | matches the report? |
|---|---|
| `prodE` | Expectation under the product measure on `{false,true}ⁿ`, by recursion on the list of probabilities; evaluates the function on lists of length exactly `n`.  Not vacuous, not trivialising (`prodE [p] f = (1−p) f[false] + p f[true]`) |
| `siteInd`, `deficit` | `deficit ps r = Σ_{i<n} (E[r·1{x_i}] − p_i·E r)`: the sum of the covariances.  As the docstring says |
| `thermal_union_bound` | Yes: for `0 ≤ p_i ≤ 1` and `r` non-decreasing in every site, `E|r − Er| ≤ 2·deficit`.  More general than the report needs (`r` need not be non-negative; `p_i ∈ {0, 1}` allowed) |
| `thermal_union_bound_density` | Yes, word for word what the report says is machine-checked for E15(c): with `E r = 1`, `E|r − 1| ≤ 2Σ_i (E[r·1{x_i}] − p_i)`.  No witness: F16 |
| `thermal_union_bound_sharp` | Yes: equality on one site for `r = 2·1{excited}`, every `p ∈ [0,1]`.  The report's equality case (`μ*_{a'}`, `n` sites) is on paper |
| `ensemble_thermal_union_bound_witness` | A real instance: `ps = [1/2, 1/3]`, `r = count`; `E r = 5/6`, left side `5/9`, right side `2·17/36 = 17/18` (computed in Lean); strict |

Not machine-checked, as the report says: that the density of a class member with respect
to `μ*_a` is monotone; the identification of the two sides with `2·TV` and the one-body
deficits; E15(a), (b), (d); everything else in Parts IV and V.  The summary table labels
E15 "P" only, which understates rather than overstates.

---

## 4. Novelty classes

Reading levels: **read** (the statement read in the source or in notes restating it),
**summary** (search-engine summary only), **memory**.

| item | report | assessment |
|---|---|---|
| E2.2 | science division's; not in the table | Known in substance: no sharp minimum of a smooth function at an interior point; quadratic growth gives a Hölder-`½` bound (second-order growth conditions in perturbation analysis; non-degenerate certificates in sparse recovery — **memory**, not searched).  Formulation |
| E2.3 | immediate | Agreed; and see F4 |
| E7′ | new (not found) | The single-pose half of (b) is **known**: a body–bar framework is generically globally rigid iff it is redundantly rigid (Connelly–Jordán–Whiteley 2013; **summary**), which for two bodies is `m ≥ D_d + 1`; in kinematics, seven transducers determine the pose by linear equations (Innocenti 1998; **summary** of the abstract).  "Up to 40 poses for six legs", all 40 can be real (Raghavan 1993; Dietmaier 1998; **summary**): correct as cited.  The ensemble statement is E5/E6 applied to this map: **new (not found)** for `K ≥ 2`, a corollary |
| E13(a) | formulation | Agreed.  It is the criterion for extreme points of the Lipschitz unit ball on a finite metric space (Farmer 1994; Smarzewski 1997, as cited by arXiv 1905.07547; **summary**) carried from `g` to `w = e^{−g}`.  Cite it |
| E13(b), (c) | formulation | Agreed: a fact about polytopes; LP duality |
| E15(a)–(c) | new (not found) | **Too generous**: F11.  Formulation.  Sources for the ingredients: Harris / FKG, Strassen (**memory**; Strassen's theorem and Holley's inequality confirmed in a **summary**); "monotone likelihood ratio ⇒ stochastic domination" and "the indicator of `{ν > π}` is increasing" are Lemmas 2.2–2.4 of Peres–Winkler (**read**, arXiv 1112.0603, pp. 8–9); Poincaré inequality and `Inf_i[f] = f̂(i)` for monotone `f` (**summary**).  The combined inequality "`TV ≤ Σ_i` marginal gaps for ordered measures" was **not found stated** in three searches; I believe it is standard in mixing-time arguments for monotone chains (**memory**) |
| E15(d) | new; elementary | Agreed |
| E15T | new (not found) | **Too generous**, as E15: FKG + Strassen + union bound; the ordered bound is the chain rule of total variation.  Formulation / synthesis.  Its title is false (F1) |
| E16 | new (not found); elementary | Agreed; one search for extremal log-Lipschitz densities on the cube found nothing.  The argument is monotone likelihood ratio plus symmetrisation |
| E17 | formulation of a known theory | Agreed.  "Within a factor `1.25`" and "determined by the modulus" are Corollaries 1 and 2 of Donoho (1994) as restated in P. B. Stark's lecture notes (**read**; the original not read).  The constants: F13 |
| C2 | conjecture | — |

---

## 5. Scripts and key outputs

In `docs/ensemble/reviews/ER2_scripts/` (scripts, `run_all.sh`, outputs in `out/`).  Run from
that directory; `er2_common.py` locates the repository.  Seeds are fixed; the stored outputs
are those of the final versions of the scripts.  Lines below are condensed; the numbers are
verbatim.

`e13_polytope.py` (7 min)

    instances 66, vertices found by brute force over bases 966
    (a) vertices with a DISCONNECTED tight graph: 0;  proper mixtures with a CONNECTED tight graph: 0
    (a) members built from a spanning tree of tight constraints: 3392; of these NOT in the vertex list: 0
    (b) (member, Phi) cases 10464; identified by the fibre LP 2723; disagreements with the exposed-face criterion: 0
    (b) vertices: 4764 cases; disagreements 'identified <=> unique maximiser of some f in the span': 0
    (c) flow certificate feasible at t >= max and infeasible at max - 1e-3: failures 0 of 330

`e15_union_bound.py` (7 min), `e15_local_search.py`

    T1 87 instances (n = 1..4): max over the class of TV - sum_i [sigma_i - mu_i(a_i)]: largest +1.78e-15, smallest -1.11e-16
       equality at mu*_(a'), a' one flip from a: largest |TV - rhs| = 5.55e-16
    T2 30 instances with 3..12 states: max over the class of TV - sum_i [1 - mu_i(a_i)/sigma_i]: largest +2.66e-15
       the (c)-form for NON-binary sites: max over the class from +0.013 to +0.353; positive in 30/30
    T3 mu* from delta_i(a_i, s): member in 3/30; (a)-excess +3.969e-01; (b)-excess +1.709e+00
       mu* from delta_i(s, a_i): member in 30/30; (a)-excess +3.331e-16; (b)-excess +1.332e-15
    T4 b = 0; b = 30; a one-letter site; slopes (0, 1, 12); zero distances; ties: all excesses <= 9e-16
    T5 n = 2 (b = 0.3, 1, 2.5): 6 vertices; 291 members each; criterion agrees in 291/291
       n = 3 (b = 0.4, 1, 2): 38 vertices; 768 members each; agrees in 768/768
       n = 4 (b = 1): 158 LP vertices; 888 members; agrees in 888/888; identified non-product members: 0
    local search, 5 and 6 sites, alphabets (3,3,3), (2,3,2,3), (4,4,3), Ising chains/rings/complete graphs: largest excess +1.91e-14
       control (chain of 5 sites, first bond violated): +0.000, +0.295, +0.057, +0.051

`e15t_interacting.py`, `e15t_triangle_exact.py`, `e15t_association.py`, `e15t_tree_parent.py`

    U1 33 log-supermodular references: population excess +2.22e-16; TV excess +3.28e-15; ordered bound, all orderings: +2.55e-15
    U2 two sites, pi ~ exp(-x1 x2/2), b = 1: mu* = [0.318945 0.318945 0.318945 0.043165]
       max population excess +0.169599; max TV excess +0.169599 at mu = [0.096255 0.711235 0.096255 0.096255]
       three-site chains, first bond violated: (+0.354, +0.239), (+0.035, +0.129), (+0.044, +0.056), (+0.051, +0.046), (+0.189, +0.124), (+0.332, +0.201)
    U3 triangles K12 = K23 = K, K13 = -kappa in e, field, b:
       (4, 0.2, -2, 1): population +2.22e-16; TV +1.33e-15      (3, 0.1, -1.5, 0.7): +1.11e-16; +1.33e-15
       (6, 0.5, -3, 1.5): -2.22e-16; -4.44e-16                  (2, 0.05, -1, 1): +0.00e+00; +8.88e-16
       (4, 1.5, -2, 1): +2.22e-16; +4.44e-16                    (1, 0.5, 0, 1): +2.57e-02; +1.33e-15
    U4 pi ~ exp(x1 x2 + x2 x3 - x1 x3/2), b = (1,1,1): population -1.11e-16; TV +8.88e-16; ordered bound by ordering:
       (1,2,3): +5.55e-17, (1,3,2): +0.00e+00, (2,1,3): +5.33e-04, (2,3,1): +5.33e-04, (3,1,2): +0.00e+00, (3,2,1): +5.55e-17
    exact, 38 vertices, 40 digits, pi ~ exp(J12 x1x2 + J23 x2x3 + J13 x1x3), b = 1:
       (1, 1, -0.5): 0.0 / 0.0     (1, 1, -0.25): 0.0 / 0.0     (2, 2, -0.25): 0.0 / 0.0
       (0, 0, -0.5): 0.169599 / 0.169599                        (1, -0.5, 0): 0.187466 / 0.260288
    J = (1, 1, -0.5): log-supermodular False; smallest Cov(1_U, 1_W) over up-sets +0.0000; CIS for (1,2,3), (1,3,2), (2,1,3): False, True, False
    trees: 194 (tree, parents-first order) pairs: largest variation of h_i at a fixed state of the parent = 5.55e-16 (control 7.91e-01)

`e16_double_cone.py`

    n = 4, b = 1.0: LP max = 7.605870183, E_D[M^2] = 7.605870183; optimal face: dimension 0, spread 2.776e-17
    n = 6, b = 2.5: LP max = 27.693176560, E_D[M^2] = 27.693176560; dimension 0, spread 3.363e-15
    n = 5, b = 1.0: LP max = 10.233838720 = E_D[M^2]; tight-graph components of D: 2; dimension 1, spread 1.102e-01
          E[sign M] on the face in [-0.462117, 0.462117] = +-tanh(b/2); D_(theta) just beyond is a member: False
    n = 7, b = 1.0: LP max = 17.243164826 = E_D[M^2]; dimension 1; deviation of a face point from D(1 + theta sign M): 3.7e-13

`e17_noise.py`

    N1 Phi_N(-1) = 0.158655; Phi_N(-1)/4 = 1/25.212; sqrt(Phi_N(-1))/2 = 0.19916
    N2 l2 duality: 148 pairs, m = 1..3: dual - primal <= 9.62e-07 (cutting planes + SLSQP);
       second method: m = 1 (48 cases) 1.22e-15; m = 2 (48 cases) 7.01e-08
    N3/N4 12 instances: sup risk of T^ formula = exact (vertices), simulated within 0.3 %, <= omega^2/4;
       two-point minimax (quadrature / simulated Bayes rule) >= Phi(-1) omega^2/4;  E sech^2(1 + Z) = 0.4496
    N5 X = {0,1}:  sigma = 0.5: Phi(-1)w^2/4 = 0.039664 <= two-point 0.112400 <= affine minimax 0.125000 <= risk of T^ 0.250000 = w^2/4
                   sigma = 5:   0.039664 <= 0.247525 <= 0.247525 <= 0.250000

`e7p_platform.py` (1 min)

    G1 d = 2 (m = 1..5), d = 3 (m = 1, 2, 5..8): uniform of rank min(m, D); connected iff m = 1 or m >= D + 1
    G2 d = 2, m = 3, 300 generic instances: real poses in the fibre -> {2: 143, 4: 140, 6: 17}
       m = 4: poses matching the fourth leg -> {1: 300}; smallest fourth-leg mismatch at another pose: 4.278e-03
    G3 d = 2, m = 4: 840 splices; first three legs have no real pose in 198; otherwise smallest |F_4 - q_4|:
       min 3.920e-03, 1% 1.497e-02, 10% 1.194e-01; below 1e-6: 0
    G4 d = 2, m = 3: both complementary splices realised in 107 of 200 pairs; twin ensemble:
       u = (-0.807274, 1.326010), (0.878919, -0.963718), (1.293926, 0.070845)
       v = (0.800606, -0.999195), (-1.056454, -1.859430), (0.831426, -0.367137)
       g1 = (-1.273617, -0.278889, -0.177958), g2 = (-1.345372, -0.462861, 0.217065)
       h1 = (-1.06211, 2.231389, 2.773907),    h2 = (-1.609879, -0.117137, -0.046323)
       squared lengths g1 (6.601283, 12.096645, 4.149206), g2 (4.666223, 14.715787, 4.277115);
                       h1 (6.601283, 14.715787, 4.277115), h2 (4.666223, 12.096645, 4.149206)
    G5 d = 3, m = 6, 4 instances, 250 starts: distinct real poses found: 4, 6, 4, 2; m = 7: seventh-leg mismatch at
       another pose of the six-leg fibre >= 5.77e-01; 36 non-constant splices, 40 starts: smallest residual 9.009e-03
    G6, G7: see F6

`e22_e23_checks.py`

    t^2: 0.10000 0.03162 0.01000 0.00315 (exponent 0.501)      t^4: 0.31623 0.17783 0.10000 0.05623 (0.250)
    |t|^1.5: 0.04642 0.01000 0.00215 0.00045 (0.682)           kappa: omega(1e-5)/1e-5 = 315, 315, 5623, 45

`c44_cutting_plane_validation.py`, `c44_accept_margins.py`, `c44_full_lp_instancewise.py`,
`c44_replicate_rows.py` (imports of the repository's functions, read-only)

    n = 10: 240 instances: agreement script / full LP in 240; certificates inconsistent in 0; margins of 86 faces: min 5.195e-02
    n = 12: 210 instances: agreement in 210; inconsistent 0; margins of 70 faces: min 1.717e-02
    n = 14:  40 instances: agreement in 40;  inconsistent 0; margins of 15 faces: min 3.774e-02
    LP solves inside the script: 513 + 567 + 184; with status != 0: 0;  float32 energies: largest error 9.2e-07, 9.9e-07, 1.8e-06
    n = 12: 91 'face' answers: float64 gap at acceptance: min 5.038e-03; spread of the conformers' energies: max 6.04e-14
    capacity_threshold.is_simplicial_face against my max-margin LP: 400 instances, disagreements 0
    my LP, fresh instances: n = 10, K = 8..14: 0.890 0.812 0.618 0.388 0.185 0.077 0.028  (stored 0.875 0.787 0.613 0.383 0.253 0.072 0.022)
    guessed driver, n = 10: 0.875, 0.787, 0.613, 0.383, 0.253, 0.072, 0.022  = stored

`repo_f6_population.py` (replays the random stream of the repository script)

    (iii) TV excess (printed by the script): +0.965, +0.522, +0.024, +0.062, +0.294
          population excess (NOT printed)  : +0.560, +0.426, +0.186, +0.057, +0.173

Repository scripts re-run: `finite_temperature_checks.py` (exit 0, 16 s) and
`platform_checks.py` (exit 0) reproduce their blocks of `output.txt` character for
character.  Every number quoted in the report for checks F1–F5 and P1–P3 is in
`output.txt` (F1: `6.7·10⁻¹⁶, 4.4·10⁻¹⁶, 1.3·10⁻¹⁵`, 360 pairs; F2: 96 cases; F3: 60/60; F4:
`7.605870`, `11.060055`, `10.233839`, spreads `1.9·10⁻¹⁶`, `9.3·10⁻¹⁶`, `1.10·10⁻¹`; F5:
`4.88·10⁻¹⁵`; P1; P2: 84 + 180 splices, `1.946·10⁻³`; P3: 80 splices, `2.366·10⁻³`; 20/20
twice).  Check F6: F2.

---

## 6. Not settled

* **The exact hypothesis of the thermal union bound.**  Positive association of `μ*_a` is
  sufficient; it is not necessary for the summed bound (third example of F1).  I have no
  characterisation.
* **The sharp constant of E15(b)** for sites with more than two letters: numbers only (F10).
* **E7′ in space.**  Uniqueness with seven legs and the absence of splices were tested on
  few instances, by multi-start least squares, which can miss solutions; the parity
  argument of F7 rests on the degree 40, which I did not re-derive.  The plane is exact.
* **Conjecture C2.**  Not examined beyond the stored numbers and my replication at
  `n = 10, 12`.
* **Sources not read in the original:** Donoho (1994) — read through lecture notes;
  Connelly–Jordán–Whiteley, Innocenti, Dietmaier, Raghavan, Farmer, Smarzewski, O'Donnell —
  search summaries only.  The inequality of F11 was not located in print.
* **Cross-division attributions** in E2.2 (SCI-RES-0026, SCI-RES-0028; GEOMETRY-MSG-0002,
  item 6) are on other branches and were not checked.
* **Part VI** (E18–E21, §4c, added during the review) was not read.

---

## Sources consulted by search

* [P. B. Stark, Statistics 210B lecture notes 6 (restates Donoho 1994, Theorems 1–2, Corollaries 1–2) — read](https://www.stat.berkeley.edu/~stark/Teach/S210b/Notes/Lec6/lec6.pdf)
* [Donoho, "Statistical estimation and optimal recovery", Ann. Statist. 22 (1994) — abstract, summary](https://projecteuclid.org/journals/annals-of-statistics/volume-22/issue-1/Statistical-Estimation-and-Optimal-Recovery/10.1214/aos/1176325367.short)
* [Peres–Winkler, "Can extra updates delay mixing?", arXiv 1112.0603 — pp. 2–9 read](https://arxiv.org/pdf/1112.0603)
* [Connelly–Jordán–Whiteley, "Generic global rigidity of body–bar frameworks" — summary](https://pi.math.cornell.edu/~connelly/Connelly-Jordan-Whiteley.pdf)
* [Innocenti, "Closed-form determination of the location of a rigid body by seven in-parallel linear transducers" (1998) — summary of the abstract](https://iris.unimore.it/handle/11380/1247373)
* [Certification of Dietmaier's Stewart platform with 40 real positions (Hauenstein–Sottile) — summary](https://www.math.tamu.edu/~sottile/research/stories/alphaCertified/Stewart/index.html)
* [Wampler, forward displacement analysis of general Stewart platforms (at most 40 solutions) — summary](https://academicweb.nd.edu/~cwample1/Preprints/MMT1996%20Stewart%20platform%20in%20soma%20coords.pdf)
* [Kantorovich distance on a finite metric space, arXiv 1905.07547 (extreme Lipschitz functions; cites Farmer, Smarzewski) — summary](https://arxiv.org/pdf/1905.07547)
* [Bredies–Chirinos Rodriguez–Naldi, extreme points of the Lipschitz unit ball on finite metric spaces, arXiv 2304.14039 — summary](https://arxiv.org/pdf/2304.14039)
* [O'Donnell, *Analysis of Boolean Functions* — summary](https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf)
* [Lecture notes on the analysis of Boolean functions, arXiv 1205.0314 (monotone functions: influence = degree-one coefficient; Poincaré inequality) — summary](https://arxiv.org/pdf/1205.0314)
* [S. Roch, *Modern Discrete Probability*, ch. 4 (coupling, Strassen, Holley) — summary](https://web.math.wisc.edu/~roch/mdp/roch-mdp-chap4.pdf)
