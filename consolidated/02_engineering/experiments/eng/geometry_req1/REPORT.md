# GEOMETRY-REQ-0001, items 1 and 3 — exact elimination and replication of exact ranks

*Computational Research Division.  The work and the report below are by an independent
subagent of this division (an AI agent briefed with the request and nothing else of ours);
the coordinator's note at the end says what the coordinator checked.  All paths are relative
to the repository root.  Labels: **[EXACT]** exact computation over ℚ that is a proof;
**[EXACT+p]** a proof whose computed part is a rank modulo a prime, used only in the valid
direction `rank_p ≤ rank_ℚ`, plus an exact bound the other way; **[BALL]** rigorous ball
arithmetic (Arb, 400 bits) on exact rational data; **[MOD p]** established modulo the stated
primes only; **[NUM]** floating point, used only to produce candidates; **[PAPER]** paper
argument.*

## 0. Pin, scope, outcome

- Pinned commit of the geometry branch: **`d84a43b`**, the newest when the work started.  The
  branch moved during the work; nothing after `d84a43b` was read by the subagent — in
  particular not GEOMETRY-MSG-0003, in which the geometry division reports its own
  computation of item 1.  The two computations are therefore independent.
- Item 2 was not actionable at that commit (it has since become GEOMETRY-REQ-0006).  Items 1
  and 3: done.
- A machine restart killed the runs in flight once; all four result files come from
  complete runs made after it.
- Installed for this work: `python-flint` 0.9.0 (FLINT 3.6.0) in the division's virtual
  environment.  Nothing else.

Outcome:

1. **`n = 10`, the system as posed (affine): yes.**  There are exactly two solutions over ℂ,
   `P = E_1/w_1` and `E_2/w_2`, each reduced.  Proved exactly over ℚ for the request's
   `witness(2, 10, "rational", 0)` and for seven further rational witnesses; it holds for
   all two-state ensembles outside a proper algebraic subset.
2. **The homogenised system has one more solution, at infinity, for every ensemble with
   `n ≤ 10`.**  It is an explicit real quadric `N_∞ ∈ 𝒩(z)` of rank 2 and signature `(1, 1)`,
   with multiplicity 5.  The projective scheme has degree `7 = 1 + 1 + 5`.  So the projective
   formulation in the geometry division's `PROOF_OBLIGATIONS.md` O-2 is false as written,
   and "properness" has to be replaced (§4).
3. **`n = 9`:** exactly 46 further affine complex solutions, of which 2 to 8 are real
   positive semidefinite depending on the witness.  **`n = 11`:** two reduced points, nothing
   at infinity.  **`n = 12`:** linear rank 20, only the trivial line.
4. **Item 3:** every rank confirmed for `K = 2, 3, 4` over ℚ.  No number differs.

## 1. Definitions as implemented (own code, `experiments/eng/geometry_req1/enslib.py`)

**Chain.**  `x_0 = 0`; unit bonds `u_i = x_{i+1} − x_i` with `u_{i−1}·u_i = 5/13` (bond-angle
cosine `−5/13`, squared one-three distance `36/13`).  Torsion `φ_m` is the dihedral of atoms
`m..m+3` (cis = 0), given by `t_m = tan(φ_m/2) ∈ ℚ`.  Recursion: `u_0 = (1, 0, 0)`,
`u_1 = (5/13, 12/13, 0)`, and with `p = u_{i−2}`, `q = u_{i−1}`:

    u_i = (5/13) q + cos φ·((5/13) q − p) + sin φ·(p × q),   cos φ = (1 − t²)/(1 + t²),  sin φ = 2t/(1 + t²).

Bond lengths, angles and the dihedrals recomputed from coordinates are checked exactly.

**Stack.**  Unweighted `z_i = (x_i^(1), …, x_i^(K)) ∈ ℚ^{3K}`; weighted `z_i D` with
`D = diag(√w_k I_3)`.  Constrained edge vectors: `n − 1` bond vectors and `n − 2` one-three
vectors.

**System of item 1 (`K = 2`).**  `P ∈ Sym_6(ℂ)`, `rank P ≤ 3`, `e_wᵀ P e_w = |e_w|²` on the `2n − 3`
weighted edge vectors.  With `P̃ = D P D` this becomes `eᵀ P̃ e = ℓ_e²` (1 or `36/13`) on the
unweighted edge vectors, and `E_k/w_k ↦ E_k`.  The map `P ↦ DPD` is linear, invertible, and
preserves rank, reality and semidefiniteness, so the solution scheme does not depend on
the weights.  Everything is computed for `P̃` over ℚ and translates to `w = (1/3, 2/3)` by
`P = D⁻¹ P̃ D⁻¹`.

**Pencil.**  `𝒩 = {S : eᵀ S e = 0 for all constrained e}`.  `L = ℚ·E_1 ⊕ 𝒩` (their `ℝI + 𝒩(z)`),
`v = dim L = 22 − rank`.  Integer basis `B_0 = E_1, B_1 = E_2, B_2, … ∈ 𝒩` with coordinates
`x`.  On `L`, `eᵀ P e = (x_0 + x_1) ℓ_e²`, so `h = x_0 + x_1` is the homogenising coordinate:
affine part `h = 1`, "infinity" `h = 0 = ℙ(𝒩)`.  `J` is the ideal of the 120 minors of order 4
of `Σ x_i B_i` (integer quartic forms in `v` variables).  `HF(d) = dim S_d / J_d`.

## 2. Item 1, `n = 10`

**Witness W0** = the request's `witness(2, 10, "rational", 0)`, re-derived from the text of the
geometry division's script (same Mersenne-twister calls; the script was never executed).

- Tangents, chain 1: `3/7, −8/5, 7/8, 3/5, 1, 9/4, 7/3`.
- Tangents, chain 2: `0, −6/5, 8/3, 0, −7/6, 2/3, −1`.
- Rational coordinates of all 20 atoms: `results/item1_pencil.json` (record `geometry_seed_0`,
  `n = 10`, key `chains`).  Example: atom 3 of chain 1 is `(4631/4901, 7464/4901, 252/377)`.

**Theorem [EXACT].**  For W0 and any weights:

- (a) The 17 linear equations have rank 17; `L ≅ ℙ⁴`.
- (b) In the coordinates `x_0..x_4` of the basis `(E_1, E_2, N_∞, B_3, B_4)`, the ideal `J` is the
  monomial ideal generated by all quartic monomials except `x_0⁴, x_1⁴, x_2⁴, x_2³x_0,
  x_2³x_1, x_2³x_3, x_2³x_4`.  Its saturation is `I(E_1) ∩ I(E_2) ∩ I(N_∞)² =
  (x_0x_1, x_0x_3, x_0x_4, x_1x_3, x_1x_4, x_3², x_3x_4, x_4², x_0²x_2, x_1²x_2)`.  `HF(d) = 7`
  for all `d ≥ 4`.
- (c) Affine ideal (`x_0 = 1 − x_1`): `(x_2, x_3, x_4, x_1² − x_1)`.  It is radical, of
  dimension 0 and degree 2; this generating set is its reduced Gröbner basis.  The
  solutions over ℂ are exactly `E_1/w_1` and `E_2/w_2`, each of multiplicity 1.
- (d) Homogenised system: dimension 0, degree 7, three points.  The third is `[N_∞]` at
  infinity with local ring `ℂ[q_1..q_4]/m²` (multiplicity 5).  `N_∞ = λμᵀ + μλᵀ`, where `λ`
  (resp. `μ`) is the normal of the hyperplane through the first (resp. last) six stacked
  atoms.  `N_∞` is real, of rank 2, signature `(1, 1)`, and not semidefinite.  In unweighted
  coordinates (divide block `k` by `√w_k` for the weighted stack):
  - `λ = (−3191017875, −1334777916, 1042362360, 3191017875, 1334777916, 112129160)`
  - `μ = (−4119799506937597372839637, 6401294510823882813984300, 144166563758967081813624,
    2481972580433888338941589, 6172692047866984979883000, 3245371514930811828221868)`

**Method and kind of proof.**  No Gröbner engine and no modular lifting were needed: exact
linear algebra over ℚ on the degree-4 Macaulay matrix (120 minors as vectors in the
70-dimensional space of quartics; integer coefficients up to 457 digits).

- (i) All 120 minors have zero coefficient on the seven monomials above — checked exactly,
  and true a priori: minors vanish at the rank-3 points `E_1`, `E_2` and to second order at
  the rank-2 point `N_∞`, because their first derivatives are combinations of `3 × 3` minors.
- (ii) The span of the minors has dimension `63 = 70 − 7` over ℚ (FLINT `fmpz_mat.rank`).
  Independently, without FLINT: rank 63 modulo each of `2⁶¹ − 1`, `2⁶² − 57`, `2⁶³ − 25`,
  `2⁶⁴ − 59` gives `≥ 63`, and (i) gives `≤ 63` **[EXACT+p]**.  This version is re-run in pure
  Python in the tests.
- (iii) Monomial combinatorics, enumerated in the tests, gives (b).
- (iv) `h³x_2, h³x_3, h³x_4, h²x_0x_1` lie in `J_4` (also verified directly as an exact rank
  over ℚ), which gives (c).
- Reducedness of `E_1`, `E_2` is confirmed two more ways: `N → N_22` and `N → N_11` are injective
  on `𝒩` (exact), and the Jacobian of the minors has rank 4 at both points.

Time: 3.3 s on a quiet machine for the whole `n = 10` analysis; the request's one-hour
stopping condition was never approached.  General-purpose engines on the raw generators
did not finish and are not used: sympy `groebner` mod `2³¹ − 1` was stopped after 300 s, FLINT
`buchberger_naive` over ℚ after 250 s.

**Second, independent proof for W0 [EXACT+p, BALL, PAPER].**  W0 without its last atom is a
9-atom ensemble.  Its affine solutions are exactly 48 points (§3).  Each of the 46
non-forced ones violates an equation of the tenth atom: the residual ball excludes 0,
with smallest certified `|residual|` `0.3705`.

**Why the point at infinity exists.**  `(λ·v)(μ·v)` vanishes on every constrained edge vector
as soon as two windows of `3K` consecutive stacked atoms overlapping in two atoms cover the
chain, i.e. for `n ≤ 6K − 2`.  That is `n ≤ 10` for `K = 2` and `n ≤ 16` for `K = 3`; for `K = 1`,
`n = 4` it is the geometry division's Example 3.3.  Any point of rank `≤ 2` on a
`(v − 1)`-dimensional linear section has multiplicity `≥ v`, hence 5 here.

- Checked exactly by exhaustion for `K = 2`, `n = 9..12`, on 8 witnesses: 2 lines + 2 points; 1
  point; none; none.
- Checked for `K = 3` on one witness: `n = 15` gives 2 lines + 5 points; `n = 16` one point;
  `n = 17` none.
- Consequence for the `K = 3` conjecture (threshold 14): at `n = 14, 15` the scheme at infinity
  is positive-dimensional, so an elimination there must saturate by `h`.

## 3. Validations: `n = 9, 11, 12` (witness `geometry_seed_0` unless stated)

| `n` | linear rank / `dim 𝒩` | quartic monomials | rank of the span of the minors over ℚ | `HF` | rank-2 locus at infinity | verdict |
|---|---|---|---|---|---|---|
| 9 | 15 / 6 | 210 | 104 | `HF_ℚ(4) = 106`; mod `p`: `106, 118, 130, 142 = 12d + 58` for `d = 4..7` | 2 lines + 2 points | one-dimensional at infinity; 48 affine points |
| 10 | 17 / 4 | 70 | 63 | 7 for all `d ≥ 4` | 1 point | 2 reduced affine points + `N_∞` (×5) |
| 11 | 19 / 2 | 15 | 13 | 2 | none | exactly two reduced points, nothing at infinity |
| 12 | 20 / 1 | 5 | 3 | 2 | none | the linear equations leave the trivial line; the minors cut `E_1`, `E_2`, reduced |

- Ranks over ℚ and the rank-2 lists are **[EXACT]**.  For `n = 11, 12`, `J_4 = I({E_1, E_2})_4`
  exactly.
- The `n = 9` Hilbert function beyond degree 4 is **[MOD p]** (two primes).  Over ℚ only "`≤`"
  follows, except `HF_ℚ(7) = 142`, which follows from the proof below.

**`n = 9`, affine solutions.**  The same pipeline is used at `n = 9, 10, 11`.  The image of
`h^k S_{7−k}` in `S_7/J_7` has ranks `65, 50, 48, 48` for `k = 1..4` at `n = 9` and `3, 2, 2, 2` at
`n = 10` **[MOD p]**.  So there are 48 affine points at `n = 9`, reduced and all of rank 3; 2 at
`n = 10` and 11.

The 46 non-forced solutions at `n = 9` were found in floating point **[NUM]**.  Each was then
certified by a Krawczyk test on the square system `(a_e + B b_e)ᵀ S (a_e + B b_e) = ℓ_e²` (15
equations, 15 unknowns), with boxes pairwise disjoint and excluding `E_1`, `E_2` **[BALL]**.
Reality, non-reality, rank 3 and inertia are decided on the boxes **[BALL]**.

| witness (`n = 9`) | non-forced, certified | real | real PSD (rank 3) | real with a negative eigenvalue | non-real | "exactly 46" |
|---|---|---|---|---|---|---|
| `geometry_seed_0` | 46 | 28 | 4 | 24 | 18 | proved |
| W0 minus its last atom | 46 | 28 | 4 | 24 | 18 | proved |
| `geometry_seed_1` | 46 | 24 | 8 | 16 | 22 | proved |
| `geometry_seed_2` | 46 | 26 | 6 | 20 | 20 | `≥ 46` [BALL]; `= 46` [MOD p] |
| `eng_0` | 46 | 16 | 2 | 14 | 30 | `≥ 46` [BALL]; `= 46` [MOD p] |
| `eng_1` | 46 | 32 | 6 | 26 | 14 | `≥ 46` [BALL]; `= 46` [MOD p] |

**"Proved" (`item1_n9_exact_count.py`) means:**

- (1) The degree-7 Macaulay matrix has rank 1574 mod `p`, so `dim (S_7/J_7)* ≤ 142` **[EXACT+p]**.
- (2) 130 explicit rational functionals from the rank-2 locus at infinity vanish on `J_7` and
  on `h³S_4`; their rank is 94 mod `p`, so `≥ 94` over ℚ.  They are restrictions and first
  normal derivatives along the two lines, and second-order operators at the two isolated
  points, whose coefficient vectors are computed exactly (Hessian kernels of dimension
  `8 = 28 − 20`).
- (3) The 48 certified points give evaluations that are independent on cubics (ball
  determinant `≠ 0`) **[BALL]**.
- (4) A short argument **[PAPER, written in the script header]** then shows that the
  evaluation at any affine solution lies in the span, which forces it to be one of the 48.

Result: the affine solution set over ℂ is exactly the 48 points, all reduced.  The
multiplicities at infinity at `n = 9` (two double lines, two points of multiplicity 8) are
inferred from this bookkeeping (`48 + 94 = 142`); they are not proved separately.

## 4. Further witnesses at `n = 10`, and genericity

Eight witnesses in total: the request's seeds 0–4 (re-derived) and three of ours
(`eng_0..2`; tangents `a/b` with `a ≠ 0`, `|a| ≠ b`, no repeats; listed in the JSON).  All give
the identical result **[EXACT]**: rank 17; the seven vanishing columns; rank 63 over ℚ and
mod four primes; targets in the ℚ-span; forced points reduced; one rank-2 point at
infinity.  All eight also give the table of §3 for `n = 9, 11, 12`.

**Does genericity of the witness matter?  No.**  The right argument is semicontinuity of a
rank, not properness **[PAPER on top of EXACT]**.  Let `G` be the set of ensembles satisfying:

- (a) the linear rank is 17;
- (b) the first six and the last six stacked atoms are affinely independent, with
  non-proportional normals;
- (c) the minors span a 63-dimensional space.

For every ensemble satisfying (a) and (b) the span has dimension `≤ 63`, by the seven
a-priori conditions.  So (c) is an open condition, and `G` is the complement of a proper
algebraic subset of the torus of torsions.  `G` is non-empty by any one witness.  On `G` the
whole theorem of §2 holds verbatim.

For `n > 10`, restrict to the first ten atoms: `solutions(n) ⊂ solutions(10)`.  With the
geometry division's Theorem B′ (not checked here) this gives identifiability among all
ensembles for `K = 2`, `n ≥ 10`, generically and for these witnesses.

W0 itself is not "generic": it has torsions 0 (twice) and ±90° (twice).  It still lies in `G`.

## 5. Item 3: replication (`K = 2, 3, 4`; cosine `−5/13`)

**Arithmetic.**  Entries are exact rationals.  Ranks are over ℚ (FLINT `fmpz_mat.rank` on
row-scaled integer matrices; pure-Python Bareiss in the tests for `K = 2, 3`).  Each rank was
also recomputed mod `2⁶¹ − 1` and mod the geometry division's prime `2147483629`; all agree.

**Witnesses.**  Three of ours per case, and their seeds `0..4` re-derived.

**Definitions as implemented.**

- (a) Conic matrix: one row per constrained edge vector `e` of the unweighted stack, columns
  `(i ≤ j)`, entry `e_i²` or `2e_ie_j`.
- (b) Jacobian of (torsions of `K` chains, `w_1..w_{K−1}`) `↦ M_ij = Σ_k w_k |x_i^(k) − x_j^(k)|²`,
  with `w_K = 1 − Σ` of the others, differentiated with respect to the half-angle tangents
  by differentiating the bond recursion exactly; tested against the closed formula
  `(2/(1 + t²))·u_{m+1} × (x_j − x_{m+2})` and against exact difference quotients.  Since
  `dφ/dt ≠ 0`, the rank equals that for angles.  Weight columns are `D(X_k) − D(X_K)`.
  Complete data = all pairs; `F_w = {3 ≤ |i − j| ≤ w}`.

All 8 witnesses give the same rank in every row below.

| claim | `K = 2` | `K = 3` | `K = 4` | the geometry division's value |
|---|---|---|---|---|
| conic rank at `n_0` (target `D_K`) | `n = 12`: 20 (21 × 21) | `n = 23`: 43 (43 × 45) | `n = 39`: 75 (75 × 78) | 20, 43, 75 — same |
| conic rank at `n_0 − 1` | `n = 11`: 19 | `n = 22`: 41 | `n = 38`: 73 | deficient — same (full row rank) |
| complete data, `n = 2K + 3`: rank / parameters | 9 / 9 (`n = 7`) | 20 / 20 (`n = 9`) | 35 / 35 (`n = 11`) | full column rank — same |
| complete data, `n = 2K + 2`: rank / parameters | 6 / 7 | 15 / 17 | 28 / 31 | deficient — same |
| `F_{K+3}`, `n = (K² + 3K + 4)/2`: rank / parameters | 9 / 9 (`n = 7`) | 26 / 26 (`n = 11`) | 55 / 55 (`n = 16`) | full column rank — same |
| `F_{K+3}` at `n − 1`: rank / parameters | 6 / 7 | 22 / 23 | 50 / 51 | (count) |
| `F_{K+2}`, at `n, n + 1, n + 4, n + 12` | 7/9, 9/11, 15/17, 31/33 | 21/26, 24/29, 33/38, 57/62 | 46/55, 50/59, 62/71, 94/103 | deficient — same |

The deficiency at separation `K + 2` is `(K + 2)(K − 1)/2 = 2, 5, 9` at every `n` tested (full row
rank).  **No number differs.**

## 6. Discrepancies and ambiguities in the geometry division's text and scripts (at `d84a43b`)

1. **`PROOF_OBLIGATIONS.md` O-2** asks to show that "the projective variety
   `{P ∈ ℝI + 𝒩(z) : rank P ≤ 3}` consists of the two forced points, reduced", then
   "properness gives the generic statement".  The projective variety has a third point
   `N_∞ ∈ 𝒩(z)` for every ensemble with `n ≤ 10`.  The affine statement is true; the generic
   statement follows by rank semicontinuity (§4).  (The geometry division found the same
   point by its own computation and withdrew the sentence in GEOMETRY-MSG-0003.)
2. **`ENSEMBLE_RIGIDITY.md` §5.2**, "for `K = 2`, `n = 9` there are 4–6 further real chains": on
   six exact witnesses the certified numbers of further real PSD solutions are 2, 4, 4, 6,
   6, 8.  The total is always 46 complex, 16 to 32 of them real.  (Corrected on their side in
   GEOMETRY-MSG-0006 to "2 to 10 in the referee's instances".)
3. **The request does not fix the seed** of `witness(2, 10, "rational", seed)`; seed 0 was used
   as primary and 1–4 as extras.  `witness()` returns residues modulo `p` of the unweighted
   stack, not rationals; the rational chain had to be rebuilt from the tangents.  With the
   same seed, the `n = 9` and `n = 10` witnesses are different ensembles, because the second
   chain starts later in the random stream — hence "W0 minus its last atom".
4. **The proof of Theorem C(b)** says the rank is computed "modulo a prime after an exact
   evaluation in ℚ"; the script evaluates the chain directly in `F_p`.  Equivalent, because
   no denominator vanishes: a wording issue only.
5. **Item 3**: the deficiencies "at `n − 1`" and "at separation `K + 2`" are forced by counting.
   Their scripts do not compute those ranks; ours do, and find full row rank.
6. Their `check()` accepts the first of seeds `0..4` without recording it; by our
   re-derivation it is seed 0 for all `K ≤ 4`.
7. No error was found in the four scripts read.

## 7. Files of the geometry division read (as text, at `d84a43b`; none executed)

`docs/collaboration/requests/geometry/GEOMETRY-REQ-0001.md`, `docs/geometry/ENSEMBLE_RIGIDITY.md`,
`docs/geometry/PROOF_OBLIGATIONS.md`, `docs/geometry/THEOREM_REGISTER.md`,
`experiments/geometry/exact_conic_rank.py`, `exact_jacobian_rank.py`, `explore_spurious.py`,
`geomlib.py`.

## 8. Deliverables, commands, run times

`experiments/eng/geometry_req1/`: `enslib.py`, `item1_pencil.py`, `item1_affine_solutions.py`,
`item1_n9_exact_count.py`, `item3_ranks.py`, `results/*.json`; tests: `tests/eng/test_geometry_req1.py`.

| command (from the repository root, virtual environment active) | wall time, final run on a loaded machine | on a quiet machine | peak memory |
|---|---|---|---|
| `python experiments/eng/geometry_req1/item1_pencil.py` | 18 min 26 s | about 7 min | 0.66 GB |
| `python experiments/eng/geometry_req1/item1_affine_solutions.py` | 30 min 37 s | 11 min 31 s | 1.25 GB |
| `python experiments/eng/geometry_req1/item1_n9_exact_count.py` | 9 min 14 s | — | 1.27 GB |
| `python experiments/eng/geometry_req1/item3_ranks.py` | 61 s | 23 s | 0.04 GB |
| `python -m pytest tests/eng/test_geometry_req1.py -q` | about 20 s; 52 passed, 1 skipped | — | — |
| the same with `GEOMREQ1_SLOW=1` | 70 s; 53 passed | — | — |

Test coverage: witness determinism and exact constraints; forced solutions, also in
weighted form with square roots; minors against independently computed determinants; the
`n = 10` certificate as a FLINT-free proof for three witnesses; monomial combinatorics;
reducedness two ways; `n = 9, 11, 12`; a control on generic pencils (h-vector
`1, 6, 21, 56, 21, 6, 1` of the rank-`≤ 3` locus); planted-error tests; item 3 for `K = 2, 3`;
stored JSON against recomputation; re-certification of the stored PSD solutions, and a
non-vacuity test of the Krawczyk certificate.

## 9. What was not checked

- The geometry division's Theorem B′, its Lean files, and all commits after `d84a43b`.
- Other bond geometries (`−1/3`).  Item 1 for `K ≥ 3`: only the remark on rank 2 at infinity,
  on one `K = 3` witness.  Item 3 for `K > 4` and the tetrahedral geometry.
- The exact upper bound "46" at `n = 9` for `geometry_seed_2`, `eng_0`, `eng_1` (certified lower
  bound plus modular count only).  The seeds 3, 4 and `eng_2` at `n = 9` were analysed only up
  to the Hilbert function.
- Whether the real PSD solutions at `n = 9` can carry mass in a representation of `I` (the
  geometry division's linear programme).  Identifiability at `n = 9` is not decided here.
- Which ensembles lie in the exceptional set of §4; only that it is a proper algebraic
  subset.
- The **[BALL]** parts assume FLINT/Arb is correct.  The `n = 10` theorem does not depend on it
  (pure-Python version in the tests).
- No second Gröbner engine confirmed the `n = 10` ideal: both attempts on the raw generators
  timed out.  The certificate is the linear algebra described in §2.

---

## Coordinator's note (2026-11-26, after the hand-back)

Checked by the coordinator: (1) the test file run here — 52 passed, 1 skipped, 16 s;
(2) no absolute path, name or address in the delivered files; (3) **an independent exact
computation, without the subagent's library** (plain rational arithmetic and a nullspace):
the chain of W0 rebuilt from the tangents (atom 3 of chain 1 agrees with the report);
unit bonds and one-three distances `36/13` exactly; both block projectors satisfy the 17
equations; the normals of the hyperplanes through the first six and the last six stacked
atoms, recomputed, are proportional to the report's `λ` and `μ`; `N = λμᵀ + μλᵀ` vanishes on
all 17 edge vectors, has rank 2 and eigenvalues of both signs; and with an eleventh atom
the same construction fails on exactly one edge vector — so the point at infinity is
there at `n = 10` and gone at `n = 11`, as the report says.  Not checked by the coordinator:
the rank 63 of the Macaulay matrix other than through the tests; the `n = 9` count; the
ball-arithmetic certificates; item 3 other than through the tests.  The agreement of this
computation with the geometry division's own (GEOMETRY-MSG-0003: degree 7, components of
lengths 1, 1, 5, the rank-2 quadric of two hyperplanes) is agreement between two
computations that did not see each other; it is evidence, and the linear-algebra
certificate of §2 is the proof.
