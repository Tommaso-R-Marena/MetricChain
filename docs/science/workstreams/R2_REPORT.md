# R2 — independent review SCI-REV-0002: theory report §11.22 (limit shape of profile sets, limit of certificate sizes)

Reviewer: workstream R2 of the science division (first independent referee of this section).
Object: `docs/THEORY_REPORT.md` §11.22 at theory commit `5ed4072` (Lemma 11.67 – Conjecture 11.75),
the workstream report behind it (`docs/workstreams/S_REPORT.md`), `proofs/Frontiers/SetLimit.lean`,
`proofs/Frontiers/CoverStability.lean`, and the engineering data (`ENG-RES-0002`, class tables at
`db56d05`).  All my code and outputs: `experiments/science/ws_R2/` (log: `NOTES.md`; outputs: `out/`).
Nothing else in the repository was modified; no git state was changed.

Labels (COMMON.md rule 6): **[V]** machine-checked, **[P]** paper proof, **[K]** known and cited,
**[N]** numerical evidence, **[C]** conjecture, **[H]** heuristic.  *Review* = I read and re-derived;
*replication* = I re-computed with my own code written before reading the authors' code.

---

## 1. Verdicts

**In one paragraph.**  I found **no false theorem** in §11.22.  The lattice lemmas (11.67, 11.68),
which were the unverified core, are correct: I re-derived both by hand, re-derived the constants
`(1, 9, 14)`, `β = 60`, `β′ = 28`, `168 = 60 + 3·36` by counting lattice sites, and tested the
concatenation lemma **exhaustively on all 270 997 444 ordered pairs of bridges with at most 13 beads**
(308 million concatenations, zero failures) with an enumerator written before I read anyone else's
code; that enumerator reproduces the engineering division's class tables **exactly** for every chain
length from 4 to 23 beads (`2.1·10⁹` conformations at the largest size) and the authors' bridge
tables for 4 to 21 beads.  All computer-assisted *bounds* were replicated with independent code:
both linear programmes were re-formulated from scratch and every row was certified with **my own**
exact dual certificates; the volume bounds `26 437`, `3 719`, `3 627` (and the other nine) come out
to the digit; I found my own packings of 51, 158, 7, 15 points in `T₀` (claimed 50, 157, 7, 14) and
my own lamella families give the finite-`N` lower bounds `26` at 1 000 beads and `32` at 2 000
(claimed 26, 31).  The machine-checked abstract theorems say what the report says they say, but
their hypotheses are **not literally** what Lemma 11.68 delivers (index range, normalisation); the
gap is bookkeeping and I give the patch.  What does **not** survive as written is the *practical
headline*: "the plateau lies between 50 and 3 627 evaluations … and is reached at `10³`–`10⁵` beads"
(and "the plateau is real, it is in the hundreds").  The bracket is a theorem about `liminf` and
`limsup`; the existence of a plateau for the chains that were measured is conjectural, and is not
proved at the accuracy `ε₁ = ½` even for bridges; "hundreds" and "`10³`–`10⁵` beads" are estimates,
and the second has no theorem behind it in either direction.  In the other direction the report
*understates* what its own tools prove: with the explicit bridges that the authors built (I
regenerated and verified them with my code) and the convexity theorem, the lower bound for the
`liminf` at `(L, ε₁) = (1, ½)` is **at least 116**, not 50, and the body of profile densities has
volume **at least 1.56** (proved), where the report's "2.2" rests on an unproved sketch.

**Per statement.**

| statement | verdict | basis |
|---|---|---|
| Lemma 11.67 (site-set reduction, local counting) | **proved** | re-derived; replicated on all walks with `N ≤ 12` from the `O(N²)` definition and on 3 000 random site sets |
| Lemma 11.68 (concatenation; `δ ∈ [0,1]×[0,9]×[0,14]×{0,1}`, `β = 60`, `β′ = 28`) | **proved** | re-derived incl. constants; exhaustive on `2.7·10⁸` pairs (`N₁, N₂ ≤ 13`), `4.2·10⁷` pairs with `N₁ ≤ 16`, `N₂ ≤ 8` and the reverse; `δ₃ = 1` is attained |
| Theorem 11.69 (limit shape for bridges, rate `168/(N+3)`) | **proved, with a bookkeeping gap** between the Lean hypotheses and the application (minor finding m1) | abstract part [V] (axioms checked: see §3.9), application re-derived |
| Lemma 11.70 (stability of covering numbers) | **proved** | (a), (b) [V]; (c), (d) re-derived |
| Theorem 11.71(a) (limit of certificate sizes, bridges) | **proved; weaker than the headline** (limit only off an unidentified countable set of accuracies; nothing shows that `ε₁ = ½` or `¼` is not exceptional) | re-derived |
| Theorem 11.71(b) (walks: sub-sequential limits, lower and upper bound principles) | **proved** | re-derived |
| Theorem 11.71(c), columns "every `N`", "limsup", "liminf", "proved at `N`" | **proved (computer-assisted); replicated**; the `liminf` column can be raised (116 at `(1, ½)`) | own code throughout |
| Theorem 11.71(c), column "estimate of the plateau" (150–350, …) | **estimate, not a theorem** (labelled [N] in the table, stated as fact in the text below it) | only read |
| Proposition 11.72(a) (by-hand inequalities) | **proved** (the one-line justification in the report is incomplete; S_REPORT has the full proof) | re-derived; checked on all classes `N ≤ 27` |
| Proposition 11.72(b) (eleven inequalities, all finite site sets) | **proved** | own LP formulation, own exact certificates; direct test on 65 535 + 7 000 site sets |
| Proposition 11.72(c) (marked programme: `𝒦₂`, three gauche bounds) | **proved as a statement about limit points** | own formulation (340 configurations), own exact certificates |
| Proposition 11.72(d) (rod, row of stems, crystal in `K^{br}`; `γ = 0` on `T₀`) | **proved** | own lamella construction to 60 548 beads; rod-pair counts verified |
| Proposition 11.72(e) (`γ ≥ 0.22` somewhere) | **proved** | bridge regenerated with the authors' builder, verified with my code: exact match |
| Proposition 11.72, paragraph "how much of the body is known" (`2.2 ≲ vol 𝒦`, "five vertices settled") | **weaker than advertised** (rests on the routing sketch; proved: `1.56 ≤ vol 𝒦 ≤ 3.125`, three vertices) | new computation |
| Proposition 11.73 (surface law, rate `N^{-1/3}` at the compact end) | **proved** | re-derived; tested on site sets and tables; `k_N ∈ [1.710, 1.862]` replicated |
| Proposition 11.74 (single-flip constants) | **proved** (its use in Theorem 11.37 was not examined) | hairpins `3 ≤ a, b ≤ 40` replicated; upper bound re-derived |
| Conjecture 11.75 | **conjecture**; (i)–(iv) proved as stated; evidence replicated | re-derived (iii), (iv); tables replicated |
| headline "the plateau is between 50 and 3 627 and is reached at `10³`–`10⁵` beads" | **mixes theorem, conjecture and estimate** (major finding M1) | §5 |

---

## 2. Claim examined, method, evidence

**Claim.**  For the diamond-lattice chain (profile `h = (h₃, h₈, h₁₁)`, gauche count `g`, envelope
`L‖Δh‖_c`, known part `e·g`, zero residual): bridges have a compact convex limit shape `K^{br} ⊂ ℝ⁴`
with one-sided rate `168/(N+3)`; certificate sizes of bridges converge to a covering number of it;
for all walks an outer polytope, `50 ≤ liminf`, `limsup ≤ 3 627` at `(L, ε₁) = (1, ½)`, `26 437` for
every length; rate `N^{-1/3}` at the compact end; Conjecture 11.75.

**Method.**  (1) Read §11.22, §11.17, S_REPORT, D46/D48, the two Lean files, the engineering messages —
but **not** any enumerator or checking code.  (2) Wrote my own enumerator (`r2_enum.c`: the pair
counts are accumulated from the definition by look-up of *all* integer vectors of squared norm 3, 8,
11; gauche torsions by the 1–4 distance) and a pure-Python one (`r2_lemma67.py`, `O(N²)` definition),
and compared with the engineering tables.  (3) Re-derived each lemma by hand, then wrote an
independent test for each finite statement.  (4) Re-formulated both linear programmes from my own
derivation (oriented bonds, `μ = ν/4N`), validated the modelling exactly on random site sets and
random walks, and searched for my own dual certificates, verified in rational arithmetic.
(5) Re-computed every number of the table of Theorem 11.71(c) that is a bound.  (6) Only then read
the authors' code (`experiments/workstreams/S/code`) and the coordinator's outputs
(`experiments/coordinator_checks/out_s_check*.txt`) and compared.  (7) Read the Lean statements
against their use.

**Evidence inspected.**  Full text of §11.22 (lines 4692–5083), §11.17, S_REPORT (all), D46, D48,
`SetLimit.lean`, `CoverStability.lean`, ENG-REQ-0001, ENG-RES-0002, THY-RES-0002 (first 150 lines), the
24 engineering class tables, the authors' stored outputs, `build.py`, `lat.py`, `g3_compare.py`
(parts), the seven coordinator outputs.  Not read: `pchain.c`, `periodic.c`, `g5_estimate.py`,
ENG-RES-0007, THY-RES-0001.

---

## 3. Established findings (statements, proofs, numerics)

### 3.1 The data both divisions rely on — independent replication

* **[N, replicated]** `r2_enum walk N`, `N = 4 … 23`: for every `N` the class table (pair counts,
  number of conformations, `gmin`, number at `gmin`, `gmax`) is **identical** to
  `eng_ro/experiments/eng/chain_cover/data/dia_Sc12_n{N−3}.txt` (`cmp_tables.py`).  Conformations
  `3, 9, 27, 79, 233, …, 738 087 517, 2 139 332 335`; classes `2, 4, 7, 13, 22, …, 1 911, 2 328`.  Run time
  323 s for `N = 23`.  **Not replicated:** `N = 24 … 27` (`6·10⁹ … 1.5·10¹¹` conformations) — those four
  tables I only read; everything below that uses them says so.
* **[N, replicated]** `r2_enum bridge N`: `N = 3 … 23` (`2.6·10⁸` canonical bridges at 23; 24 running at
  the time of writing).  The sets of realised `(h, g)`, `gmin`, `gmax` are identical to the authors'
  stored tables for `N = 4 … 21` (their counts are exactly twice mine: a convention).
* **[N, replicated]** Exact covering numbers by integer programming (`r2_cover.py`, cover relations
  in exact integers): walks, `L = 1`, `ε = N/2`: `3, 5, 5, 8, 9, 11, 13` at `N = 8, 11, 12, 15, 18, 21, 23`
  (the report's "8 and 11 at 15 and 21 beads"; ENG-RES-0002's column); `N = 15`: `21` at `ε = 0`, `13` at
  `N/4`, `2` at `L = ⅕`, and `10` with the weighted norm of the coordinator's brief (D48 confirmed);
  `N = 21`, `ε = N/4`: `19`.  Bridges: `5, 6, 8, 10, 11` at `N = 12, 15, 18, 21, 23` (`ε = N/2`) and
  `7, 11, 14, 17` at `N = 12, 15, 18, 21` (`ε = N/4`) — the table of S_REPORT §5.4.

### 3.2 Lemma 11.67 — proved

Re-derivation: consecutive bonds are `s·a_i, −s·a_j, s·a_k` with `j ≠ i`, `k ≠ j`; `|a_i − a_j|² = 8`,
`|a_i − a_j + a_k|² = 13 + 2a_i·a_k ∈ {19, 11}`; every unordered pair of occupied sites is a unique pair
`p < q` of beads; two sites at squared distance 8 have exactly one common neighbour, two at 11 are
joined by exactly two three-bond paths.  **[P; replicated]** `r2_lemma67.py`: for every walk with
`N ≤ 12` (17 107 at `N = 12`) the profile from the `O(N²)` definition equals `e(S) −` chain pairs, the three
local formulas hold, the bond-index rule and the distance rule for gauche agree; local formulas
also on 3 000 random finite site sets.

### 3.3 Lemma 11.68 — proved; what I checked item by item

* *Definition of bridge used:* first bead strictly lowest, last bead weakly highest in `y`.  With
  `N₁, N₂ ≥ 3` the bonds `b′, b` of `x¹` and `u₁, u₂` of `x²` exist; `b`, `u₁`, `u₂` are up-bonds.
* *Lattice validity of the linker:* `c₁` is an up-bond out of the sublattice of `P` (if `b′` is an
  up-bond it starts on that sublattice), `b` an up-bond out of the other; so `P, ℓ₁, ℓ₂, ℓ₃, Q` is an
  all-trans zigzag at heights `H, …, H+4`, and `φ(x²)` continues it by `(c₁, b)`.
* *The symmetry:* the eight ordered pairs (up-bond, up-bond out of its end point) are the eight
  directed edges of the square `(±1, ±1)` in the `(x, z)` plane; the stabiliser of the `y`-direction in
  the point group has order 8 and acts simply transitively on them.  In the exhaustive test I search
  all 48 signed permutation matrices; exactly one qualifies in every case.
* *Self-avoidance after concatenation:* heights `≤ H`, `H+1 … H+3`, `≥ H+4` (only `Q` at `H+4`).
* *Cross terms between the two pieces:* none — squared distances below 12 are 3, 8, 11 and have
  height differences at most 3 (`r2_concat_bounds.py`: shells by relative height `{±1: 2}`,
  `{0, ±2: 4}`, `{±1: 4, ±3: 2}`).
* *Bookkeeping* (mine): with `e₃(Λ) = 2`, `e₈(Λ) = 1`, `e₁₁(Λ) = 0`:
  `δ₃ = [e₃(Λ,S₁) − 1] + [e₃(Λ,S₂) − 1]`, `δ₈ = [e₈(Λ,S₁) − 2] + [e₈(Λ,S₂) − 2]`, `δ₁₁ = e₁₁(Λ,S₁) + e₁₁(Λ,S₂)`;
  all brackets are counts of pairs minus the chain neighbours across a junction, hence `≥ 0`.
* *Constants by counting lattice sites by height* (`r2_concat_bounds.py`, all eight `(c₁, b)`): pairs
  linker–`S₁` at most `2, 8, 10`, linker–`S₂` at most `1, 5, 4`, `|ℓ₁ − Q|² = 19`: `δ ≤ (1, 9, 14)`; all `δ ≥ 0`,
  so `‖δ‖_c = 9δ₃ + 4δ₈ + δ₁₁` and the norm is at most `9 + 36 + 14 + 1 = 60`.  One bead: `(1, 3, 6)`, `28`.
* *Gauche count at the junction:* six new torsions `(b′,b,c₁), (b,c₁,b), (c₁,b,c₁), (b,c₁,b), (c₁,b,c₁),
  (b,c₁,b)`; only the first can be gauche, iff `b′` is a down-bond.
* **[N, replicated, exhaustive]** `r2_concat.c` builds every concatenation from coordinates and
  recounts from scratch (`O(N²)` definition):

  | sizes | ordered pairs | concatenations (both `c₁` where free) | failures | observed maxima `(δ₃, δ₈, δ₁₁, δ_g)` | largest norm |
  |---|---|---|---|---|---|
  | `3 ≤ N₁, N₂ ≤ 10` | 746 496 | 856 224 | 0 | `(0, 3, 6, 1)` | 19 |
  | `3 ≤ N₁, N₂ ≤ 13` | 270 997 444 | 307 987 558 | 0 | `(1, 6, 8, 1)` | 41 |
  | `N₁ ≤ 16`, `N₂ ≤ 8` | 41 871 265 | 47 380 017 | 0 | `(1, 6, 9, 1)` | 43 |
  | `N₁ ≤ 8`, `N₂ ≤ 16` | 41 871 265 | 48 465 165 | 0 | `(0, 3, 5, 1)` | 18 |

  `δ_g = [b′ down]` without exception.  `δ₃ = 1` occurs (460 936 times for `N ≤ 13`): the constant is
  attained, contrary to what the quoted maxima `(0, 2, 4, 1)` suggest (minor finding m3).
  Set-level check on the complete tables (`r2_bridge_tables.py`): condition (C) on 13 069 pairs of
  points of `P_{N₁} × P_{N₂}` with `N₁ + N₂ + 3 ≤ 21`, condition (E) on 17 971 points: no failure.

### 3.4 Theorem 11.69 — proved; the Lean hypotheses versus the application

Application re-derived: `Q_M := P_{M−3}`, `M ≥ 6`; (C): `(M₁−3) + (M₂−3) + 3 = M₁ + M₂ − 3`; (B) with `R = 36`
because `9h₃ + 4h₈ + h₁₁ ≤ 9(N−1) + 4(5N−2) + 6N ≤ 35N` and `g ≤ N − 3`; `|q/N − q/(N+3)| ≤ 3R/(N+3)`;
`168 = 60 + 108`.  The truncated-epigraph map is 1-Lipschitz for `d_H` (I checked both for the max and
for the sum metric).

What the machine-checked theorems require and what the lattice delivers:

1. `SuperAdditive Q β β′ R` quantifies `add`, `succ`, `bound` over **all** `M : ℕ`, and
   `SuperAdditive.hausdorff_limit`, `cover_sandwich` assume `(Q M).Nonempty` for **all** `M ≥ 1`.  Lemma
   11.68 gives `Q_M` only for `M ≥ 6`.  With `Q_M := ∅` for `M < 6` the non-emptiness hypothesis fails;
   so the cited declarations do not apply as they stand.  **Patch [P, checked by counting]:** put
   `Q_M := {0}` for `0 ≤ M ≤ 5`.  Then (C) holds with the same `β = 60`: for `M₁ ≤ 5 < 6 ≤ M₂` append `M₁ ≤ 5`
   beads in the zigzag of the linker — the same height count gives a cost of at most `(1, 6, 10; 1)`,
   norm `≤ 44` (`r2_concat_bounds.py`, "appending k = 1..5 beads": `28, 42, 44, 44, 44`); for `M₁, M₂ ≤ 5`
   with `M₁ + M₂ ≥ 6` the rod has `(h, g) = 0`; (E) and (B) are immediate.  (S_REPORT Lemma 3.3 states
   the abstract lemma for `M ≥ M₀`, so the *paper* proof has no gap; only the link to Lean does.)
2. `scaled Q M = Q_M / M` is the set `(h, g)/(N+3)`, not `𝒟_N^{br} = (h, g)/N`.  The conversion (the `3R/(N+3)`
   of the rate, and for covers the accuracy `ε₁N/(N+3)` instead of `ε₁`) is a paper step.
3. `cover_sandwich` lives in `V × ℝ` with the product (max) norm; the constants `β, β′, R` were computed
   for the sum norm `‖p‖_c + |g|` — harmless, max `≤` sum.
4. `HasCover` is the covering problem with internal centres, as in the text.  Lemma 11.70(c)
   (right-continuity, countably many jumps) and the limit statement (d) are not in Lean (the report
   says so).  The "for every `N`" inequality of Theorem 11.71(a) is `hasCover_sandwich` with `η = d_N`.
5. The norm of D48 plays no role in the abstract theorems (any norm); the numbers use `‖·‖_c`
   throughout, which I confirmed against published covering numbers (8 with `‖·‖_c`, 10 with the
   weighted form, at 15 beads).

### 3.5 Lemma 11.70, Theorem 11.71 — proved; what the limit statement does and does not say

(c): finiteness for `ε > 0` uses `e·g ≥ 0`; right-continuity by compactness of `π(F)^k` — re-derived.
(d) from (b) and (c): `N(F, ε) ≤ liminf ≤ limsup ≤ N(F, ε−)`.  Theorem 11.71(b): if a centre covered
two clients near `(p_i, g_i)`, `(p_j, g_j)` the triangle inequality would give
`L‖p_i − p_j‖_c ≤ e(g_i + g_j) + 2ε₁ + o(1)`; the clients exist for all large `N` because `𝒟_N^{br} → K^{br}`.
Upper bound: a maximal `ε₁/L`-separated set is an internal net because `e·γ ≥ 0`.

**What is not proved** (and the text sometimes suggests): the limit `lim_N N^{P,br}_cov(ε₁N)` exists
for all `ε₁` outside an at most countable set **that is not identified**.  Since `K^{br}` is not known,
nothing excludes that `ε₁ = ½` (or `¼`), the accuracies of the table, are jumps of `N_∞`.  So at the
accuracies of the table convergence is not proved even for bridges; what is proved there is the
two-sided inequality.

### 3.6 Proposition 11.72 — the outer bounds, replicated with my own certificates

*(a)* True on every class for `N = 4 … 27` (`r2_tables.py`; own tables to 23, engineering 24–27):
`min[h₈ − (4h₃ − 2)] = 0`, `min[h₈ − (6h₃ − N − 4)] ≥ 6`, `min[(2h₃ + 3N + 3) − h₈] ≥ 15`.

*(b)* My derivation (`r2_lp_site.py`): for oriented bonds `(v → w)` with cluster pattern
`σ = (v, w, u₁, u₂, u₃, z₁, z₂, z₃)` and `μ = ν/4N`: `μ(v) = 1`, `e₃/N = 2μ(vw)`, `e₈/N = μ(C(d_v, 2))`,
`e₁₁/N = μ(Σ_{j≠k} u_j z_k)`; after averaging over the 48 point-group images, `μ` is invariant under the 12
cluster symmetries and its star marginal under `S₄`; `μ(forbidden) ≤ 2n_E/N`.  All of this is checked
**exactly** on 60 random finite site sets.  HiGHS gives LP values `b + c₃ + c₈` for the eleven rows.
For each row I found my own multipliers (integers, one row with denominators 48) and verified in
rational arithmetic on all 45 orbits of non-empty patterns: `≤ 0` on the 31 allowed orbits, `≤ M_mine`
on the 14 forbidden ones, with `M_mine ≤` the table's `M` in every row (smaller in five rows: `0`
instead of `5, 6, 6, 1`, and `247/288` instead of `3` — the table's `M` are valid, not optimal).
Direct test of the finite inequality with `n_E` (`r2_finite_sets.py`): all 65 535 non-empty subsets
of a 16-site piece, 4 000 random subsets of a box, 3 000 random animals, balls/cubes/octahedra up to
3 059 sites — no violation.  Walk form `c·h ≤ bN + 4M + c₃ + 2c₈` on every class, `N ≤ 27`: holds.
Polytope (`r2_volumes.py`, exact rationals): `𝒦₁` has the 12 listed vertices and volume
`697/216 = 3.2269`.

*(c)* My formulation (`r2_lp_marked.py`): 340 configurations (339 non-empty), 47 orbits, 13 star
relations.  The modelling (`g/N = 2μ(vw` marked, continued with different indices`)`, symmetry, star
invariance with marks, at most 16 oriented bonds with a chain end as a centre) is checked exactly on
25 random walks.  LP values: the claimed `b` for the twelve rows of `𝒦₂`, and `8, 7, 7` for the three
gauche functionals; own integer certificates verified exactly on all orbits for all fifteen
statements.  `𝒦₂` has the 12 listed vertices and volume `25/8 = 3.125` exactly, `𝒦₂ ⊂ 𝒦₁`.
The statement is about limit points (the two chain ends carry mass `O(1/N)`); no finite-`N` constants
are claimed, and I computed none.

*(d)* Own construction (`r2_lamella.py`), every walk verified from coordinates (lattice walk,
injective, bridge), `(h, g)` three ways:

| lamella | `N` | `(h, g)/N` | |
|---|---|---|---|
| one row, `M = 151`, `ℓ = 160` | 48 174 | `(0.4920, 1.9710, 1.4821; 0.0093)` | `g = 3(M−1)` exactly |
| crystal `25 × 25 × 26` | 31 880 | `(0.9215, 4.6088, 5.4768; 0.0587)` | identical to the authors' value |
| crystal `31 × 31 × 32` | 60 548 | `(0.9364, 4.6832, 5.5756; 0.0476)` | distance to `(1,5,6;0)`: `90.7·N^{-1/3}` |

`|h −` formula of S Prop. 4.3`|/(MQ)` stays bounded (`≈ 2.9, 12.6, 14.3`); pairs per period between
parallel rods are `(1,4,3)`, `(0,2,4)`, `(0,0,2)` at the stated offsets and none elsewhere
(`r2_rodpairs.py`).

*(e)* `r2_verify_witness.py big`: the bridge is regenerated with the authors' builder (imported
read-only) and verified by **my** code: 166 199 beads, self-avoiding lattice bridge,
`(h₃, h₈, h₁₁, g) = (1 717, 376 013, 687 789, 131 710)`, `2h₁₁ − 5h₃ − 8N = 37 401 = 0.22504N`; the functional
`2p₁₁ − 5p₃` is 2-Lipschitz for `‖·‖_c` (I checked: `2|s₃| + 2|s₂| + 5|p₃| ≤ 2‖p‖_c`), so `γ(p*) ≥ 0.2230`.

### 3.7 Proposition 11.73 — proved

Re-derived: `3∂ ≥ 2Σ_f ρ_f` (an `a₀`-bond lies on three rods), Loomis–Whitney on the larger sublattice
part, `e₃ = (4N − ∂)/2`; the fcc line count for `e₈`; `9·2^{-2/3} + 12 = 17.67`, `9 + 8 = 17`.
**[N]** The isoperimetric bounds hold on every site set of §3.6(b) and on every class; they are far
from tight (observed `min (2N − e₃)/N^{2/3} = 1.66` against the proved `0.63`).  `k_N ∈ [1.710, 1.862]` for
`N = 8 … 27` (claimed `[1.71, 1.86]`), `38.7 %` of the bulk extent at 27 beads; lamellae: `k = 2.43 … 2.54`.
The numbers "47, 730, 5 800 beads for 50, 80, 90 %" are an extrapolation of the empirical `k ≈ 1.8`
(the report labels them [N]); what is *proved* is that 90 % of the bulk extent is reached somewhere
between `N ≈ 125` (upper bound) and `N ≈ 1.6·10⁴` (lamellae).

### 3.8 Proposition 11.74, Conjecture 11.75

*11.74.*  Lower bound (`r2_flip.py`): the fold word read off my own lamella is `(+, −, +)`; for all
`3 ≤ a, b ≤ 40` (1 444 hairpins, both conformations self-avoiding) `D − 14d ∈ [−15, −5]`, with the
periodicity `D(a+2, b+2) = D(a, b) + 28` and `D(a, b+2) = D(a, b)` for `b ≥ a + 6`.  Upper bound re-derived:
the shorter arm has `d_j` beads; cumulative counts change by at most `2, 12, 24` per moved bead, and by
at most `4, 16, 28` for the two exceptional beads (the arm's end, the bead next to the hinge), which
the `+3` absorbs.  The engineering constants (`n ≤ 16`) lie between the two bounds for every `d_j ≥ 5`.
I did not examine the claim that Theorem 11.37 needs only `c_j ≥ κd_j`.

*11.75.*  (iii): `(168k + η)/N′ + 36η/N′ ≤ (168k + 37η)/(N − η)` — re-derived.  (iv): re-derived the
parity argument (between levels `2j` and `2j+1` the strip has exactly two bonds, both forced; a walk
from below to a highest bead crosses an odd number of times; one changed site spoils at most two
values of `j`).  (ii): "about two thirds of all directions" is `0.670` with the authors' measure on
directions and `0.77` with two other natural ones (`r2_directions.py`) — measure-dependent, and it
concerns directions with `u_g ≤ 0` only.  Evidence: `r2_walk_vs_bridge.py` reproduces the table of
S_REPORT §5.4 entry by entry where I have data (`N ≤ 23` walks, `N ≤ 23` bridges), once the
lower-boundary distance is taken one-sided as in their code; walks(`N`) → bridges(`N+1`) is 3–6 units
for `N = 11 … 22`.

### 3.9 The machine-checked part

`R2Axioms.lean` (in my directory; `lake env lean`, nothing built): see `out/lean_axioms.txt` for the
axioms of `SuperAdditive.hausdorff_limit`, `dist_limit_le`, `convex_limit`, `cover_sandwich`,
`hasCover_sandwich`, `hasCover_upper_iff`, `hasCover_limit_point`, `not_hasCover_shifted`
(result recorded in §6).

### 3.10 New statements found during the review

**N1 [P, checked numerically] (a fourth exact point of `K^{br}`).**  The walk with bond indices
`0, 1, 2, 3, 0, 1, …` (the all-gauche `4₁` helix along `y`) is a bridge for every `N` — all its bonds are
up-bonds — with `h = (0, 0, N−3)`, `g = N − 3` (the 1–5 distance is `|(0,4,0)|² = 16 > 12`).  Hence
`(0, 0, 1; 1) ∈ K^{br}`, off the plane of `T₀`: `𝒦` has non-empty interior ("body") by an elementary
argument, with `vol 𝒦 ≥ 1/12` from exact points alone.

**N2 [P, computer-assisted; witnesses generated by the authors' builder, verified by my code]
(a proved inner volume).**  Let `C` be the hull of the four exact points and of the profile
densities of ten explicit bridges (the nine systems of S_REPORT §4.2 in a box of side 64, and the
166 199-bead bridge), and `δ = max_i 168/(N_i + 3) = 0.01395`.  By Theorem 11.69 and a support-function
argument, `𝒦 ⊇ C ⊖ δ𝔹_c` (erosion).  `r2_inner_volume.py`: `vol(C ⊖ δ𝔹_c) = 1.563`.  So

    1.56  ≤  vol 𝒦  ≤  3.125        (5.2 % to 10.4 % of the bulk box),   proved,

where the report has `2.2 ≲ vol 𝒦`, which needs the missing routing lemma.

**N3 [P, computer-assisted, exact rational verification] (a stronger lower bound for the liminf).**
In the hull of the same fourteen proved points — with the gauche coordinate, and with the margin
`max(L, e)(d_i + d_j)`, `d = Σλδ`, for the uncertainty of the ten approximate points — there are
`k` points that satisfy the hypothesis of Theorem 11.71(b) pairwise (`r2_rigorous_packing.py`,
packings stored in `out/rigorous_packing_*.txt`):

| `(L, ε₁)` | report: lower bound for the liminf | this review |
|---|---|---|
| `(1, ½)` | 50 (52) | **≥ 116** |
| `(1, ¼)` | 157 (162) | see §6 |
| `(⅕, ½)` | 7 | see §6 |
| `(⅕, ¼)` | 14 | see §6 |

Hence `116 ≤ liminf_N N^P_cov(N/2) ≤ limsup ≤ 3 626` for all walks at `L = e = 1` (the first inequality
also for bridges).  The proof uses Lemma 11.68, the abstract theorem (convexity, `β/M`), Proposition
11.72(d), fact N1 and the ten verified bridges; nothing about periodic systems or routing.

**N4 [P] (when the shape is resolved).**  From Proposition 11.73 and `(1,5,6;0) ∈ K^{br}`:
`d_H(𝒟_N^{br}, K^{br}) ≥ 17.6N^{-1/3} − 17/N ≥ ε₁/L = ½` for every `N ≤ 43 512` (and `≥ ¼` for every
`N ≤ 3.4·10⁵`).  So for all chains shorter than `4·10⁴` beads the finite profile set misses a part of
the limit body by more than one covering radius.  This is a statement about the shape, not about
the covering number (covering numbers with internal centres are not monotone under inclusion).

---

## 4. Critical, major and minor findings

### Critical

None.  No statement labelled as proved was found false.

### Major

**M1.  The practical headline mixes a theorem, a conjecture and an estimate.**
*Where:* §11.22, first paragraph ("the plateau lies between 50 and 3 627 evaluations at
`(L, ε₁) = (1, ½)` and is reached at chain lengths of `10³`–`10⁵` beads"); after Theorem 11.71 ("The
plateau is real, it is in the hundreds, and it is 10 to 40 times the values at 27 beads"); "What
this changes in §11.17"; §11.17, last sentence before *Prior art*; title and summary of THY-RES-0002.
*What is wrong:* three different epistemic levels are joined in one unqualified sentence.
(i) **Theorem** (verified here): for all walks `50 ≤ liminf_N N^P_cov(N/2)` and `limsup ≤ 3 627`
(in fact `116 ≤` and `≤ 3 626`), `N^P_cov(N/2) ≤ 26 437` for every `N`, `≥ 26` at 1 000 beads.
(ii) **Conjecture-dependent:** that there is a plateau at all for the chains that were measured —
a limit of `N^P_cov(ε₁N)` — needs Conjecture 11.75 (epigraph form) *and* that `ε₁ = ½` is not a jump of
`N_∞`; for bridges it needs the second of these, which is also unknown.  "The plateau is real" is
not a theorem for either class at this accuracy.
(iii) **Estimate:** "in the hundreds", "150–350", "10 to 40 times": covering numbers of an inner model
that rests on an unproved sketch, computed by a greedy heuristic on a grid; the proved ratio to the
value at 27 beads is between `116/15 ≈ 8` and `3 627/15 ≈ 240`.  "Reached at `10³`–`10⁵` beads": no
theorem bounds, from above or from below, the length at which `N^P_cov(ε₁N)` is near its limit points.
The supporting argument in S_REPORT §7.2 ("half of the proved plateau is reached at `N ≈ 10³`, 70 % at
`5·10³`") compares finite-`N` lower bounds from one family (crystalline lamellae) with the limit bound
from the same family (50); against the bound of N3 the same numbers are 22 % and 30 %.  What is
proved about "when": the value at 27 beads (15) is below every limit point (≥ 116); the lower bounds
26, 32, 35 at `10³`, `2·10³`, `5·10³` beads; and N4.
*Why it matters:* this sentence is the answer that went to the engineering division and that §11.17
now quotes; a reader takes away a location of a plateau that nobody has proved to exist for
unrestricted chains and a chain length that is an order-of-magnitude guess.
*Suggested correction:* "for every limit point of the certificate sizes of all walks at
`(L, ε₁) = (1, ½)`: between 116 and 3 627 **[P, computer-assisted]**; that the sizes converge is
proved for bridges off a countable, unidentified set of accuracies and is a conjecture for all
walks **[C]**; our estimate of the limit is a few hundred and of the chain length at which it is
approached `10³`–`10⁵` beads or more **[N/H]**."

**M2.  The section understates its own lower bound and overstates how much of the body is known.**
*Where:* Theorem 11.71(c), column "lower bound for the liminf"; Proposition 11.72, "How much of the
body is known".
*What:* the lower bounds use only the triangle `T₀`, although the explicit bridges that the
workstream built — together with Theorem 11.69, which is exactly the tool that turns one finite
bridge into a point of `K^{br}` — prove much more (N2, N3).  Conversely "`2.2 ≲ vol 𝒦`", "five
vertices settled" and the table's "estimate of the plateau" rest on the routing lemma that is
missing (the report says so in a parenthesis and then drops the qualification).  Proved: three
vertices (`(0,0,0)`, `(½,2,3/2)`, `(1,5,6)`), `vol 𝒦 ≥ 1.56`.
*Why it matters:* the bracket for the limit points is the quantitative content of the section; the
correct proved bracket is `[116, 3 627]` at `(1, ½)`, a factor 31 instead of 73.
*Suggested correction:* replace the column by the bounds of N3 (or better ones: larger boxes and a
better packing will raise them), and write "`1.56 ≤ vol 𝒦 ≤ 3.125` proved; `≈ 2.2` expected".

### Minor

**m1.  Lean hypotheses versus use** (§3.4, items 1–3).  *Where:* status paragraph and the labels of
Theorems 11.69, 11.71(a).  The declarations need `Q_M` non-empty with (C), (E), (B) for all `M ≥ 1`;
the lattice gives `M ≥ 6`; normalisation by `N + 3`.  *Correction:* state the extension `Q_M := {0}`
(`M ≤ 5`) with the one-line verification (cost of appending at most five beads `≤ 44 ≤ β`), or restate
the Lean theorem for families indexed from `M₀`; say that the passage from `N + 3` to `N` and the
exceptional set are paper steps.

**m2.  The exceptional set of accuracies** (§3.5).  *Where:* Theorem 11.71(a), table (c).  Say
explicitly that the table's accuracies are not known to be non-exceptional.

**m3.  Understated numerical check of Lemma 11.68.**  *Where:* "(Own check: … the observed maxima
are `(0, 2, 4, 1)` …)".  Exhaustively, `δ₃ = 1` is attained already at `N ≤ 13` and the maxima are
`(1, 6, 8, 1)` (norm 41), `(1, 6, 9, 1)` with `N₁ ≤ 16`.  No consequence for the lemma; the sentence
"worst cases that need many beads near the top level" should not suggest that `δ₃ = 1` is exotic.

**m4.  Incomplete justification of Proposition 11.72(a).**  The report's parenthesis
"`C(d,2) ≤ 3d/2`" gives only `e₈ ≤ 6N`; the bound `h₈ ≤ 2h₃ + 3N + 3` needs `C(d,2) ≤ (5d − 8)/2` on occupied
sites with `d ≥ 2` (and `+3/2` for the at most two sites with `d = 1`), as in S_REPORT Prop. 4.1.

**m5.  Rounding in the table of Theorem 11.71(c).**  The volume ratios are `26 437.00`, `3 626.50`,
`2 194.60`, `92.50`, `392.80`, …; the table rounds to nearest (`3 627`, `2 195`, `93`, `393`).  As bounds
on integers the floors are valid and slightly better; nothing is wrong.

**m6.  "A compact convex body".**  Non-empty interior of `𝒦` is not argued in the text (it follows
from (e), or more simply from N1).

**m7.  Wording.**  "Proposition 11.49(a) promises a plateau" — it gives a bound independent of `N`,
not a limit.  "The covering numbers of bridges equal those of walks two to three beads shorter" —
in my tables zero to three (bridges at 21 beads: 10 = walks at 19 and 20).  "About two thirds of all
directions" — for one particular measure on directions.

**m8.  The last sentence of the section** ("what governs the cost is the dimensionless ratio
`L·S_c·M/ε₁`, polynomially on a lattice, exponentially off it") is unlabelled.  On a lattice the
bound is a polynomial in `L/ε₁` whose *degree is the number of distances below the cutoff*, which
grows with `S_c`; off-lattice "exponentially" is an upper bound (Proposition 11.49(a)) plus the
observed growth to 15 beads; no lower bound of that form is proved at extensive accuracy.  Label [H].

---

## 5. Scientific reading

**The sentence "the plateau is between 50 and 3 627 evaluations and is reached only at `10³`–`10⁵`
beads".**

| part | status |
|---|---|
| every limit point of `N^P_cov(N/2)`, all walks, lies in `[50, 3 627]` | **theorem** [P, computer-assisted; replicated]; improved here to `[116, 3 626]` |
| `N^P_cov(N/2) ≤ 26 437` for every `N` | **theorem** [P; replicated] |
| there is a plateau (the sizes converge) — bridges | **theorem only off a countable unidentified set of accuracies**; open at `ε₁ = ½` |
| there is a plateau — all walks (the chains that were enumerated) | **conjecture-dependent** (Conjecture 11.75, epigraph form) and subject to the same exceptional set |
| the plateau is "in the hundreds" / "150–350" | **estimate** [N]; the inner model behind it uses an unproved sketch |
| not reached at enumerable sizes | **theorem** in the sense: the value at 27 beads (15, engineering, replicated by me to 23 beads: 13) is below every limit point |
| at least 26 / 32 / 35 evaluations at `10³` / `2·10³` / `5·10³` beads | **theorem** [P, exact counts; replicated at `10³` and `2·10³`] |
| "reached at `10³`–`10⁵` beads" | **estimate** [H]; no theorem in either direction.  Proved in the neighbourhood of this claim: N4 (the shape is not within one covering radius of its limit before `4·10⁴` beads) |

**Is the model representative of anything?**  It is one lattice (the tetrahedral lattice of the
rotational-isomeric-state picture of a saturated chain), one cutoff (three shells), one known part
(a stiffness energy `e` per gauche torsion, whose minimum is the trivial all-trans rod), the zero
residual, and two points `(L, ε₁)`.  In these units `L = 1` allows the unknown pair potential to
differ by up to `9e` between a first-shell contact and no contact, with up to one contact per bead:
the class is an order of magnitude wider than the whole range `[0, eN]` of the known part, and the
accuracy `N/2` is half the range of the known part.  So the instance sits in the regime where the
known part is almost irrelevant and a certificate must in effect learn the residual on the whole
profile body to resolution `ε₁/L`: the covering number is essentially the metric entropy of the body
`𝒦` (which is why `γ` barely matters: the bounds ignore it).  That regime is legitimate for a
query-complexity statement, but the numbers `50 … 3 627` say nothing about a system in which the
known part discriminates (large `e/L`), where the covering problem is concentrated near the minimum.
What is model-independent is the *structure*: on any lattice with finitely many distances below the
cutoff the normalised profile sets of concatenable chains have a convex limit, the limiting
certificate size is a covering number of it — a polynomial in `L/ε₁` of degree equal to the number
of shells — and finite sizes approach it with surface corrections of order `N^{-1/3}`.
**Every guarantee is model-relative**: no physical observable and no certified physical input
appears.

**Does the conclusion transfer off-lattice in any proved sense?**  No.  Three ingredients would
have to be redone.  (i) The abstract theorems are proved in a proper (finite-dimensional) normed
space; off-lattice the profile is a monotone function and the natural space is `L¹[0, S_c]`.  The
normalised profile sets are still relatively compact there (monotone functions of bounded mass),
so a version for compact subsets of a Banach space looks routine, but it is not what is
machine-checked.  (ii) The concatenation lemma uses that every bond changes the height by exactly
`±1` and that pairs within the cutoff have height difference at most 3 — lattice facts; an
off-lattice analogue needs its own geometric argument and constants.  (iii) The outer polytope and
the volume counts are finite-dimensional.  Off-lattice only Proposition 11.49(a) (an `N`-independent
upper bound of the order `exp(c·zLS_c/ε₁)`) is proved; the statement that the off-lattice plateau *is*
exponential in `L·S_c·M/ε₁` is a heuristic [H], consistent with geometric growth up to 15 beads.

---

## 6. Reproduction status

| item of §11.22 | status | my code / output |
|---|---|---|
| class tables of walks, `N = 4 … 23` | **replicated** (identical to engineering) | `r2_enum.c`, `cmp_tables.py`, `out/walk_N*.txt` |
| class tables of walks, `N = 24 … 27` | **read only** (too large for my budget: `6·10⁹ … 1.5·10¹¹`) | — |
| bridge tables `N = 4 … 21` (authors') | **replicated** | `r2_bridge_tables.py` |
| covering numbers 8, 11 (15, 21 beads); 10 with the wrong norm | **replicated** | `r2_cover.py`, `out/cover.txt` |
| covering number 15 at 27 beads | see below | `out/cover.txt` |
| Lemma 11.67 on all walks `n ≤ 9` | **replicated** (and extended to `N = 12`) | `r2_lemma67.py` |
| Lemma 11.68 numerically (48 058 / 90 688 concatenations) | **replicated and extended** (`3.1·10⁸`, exhaustive) | `r2_concat.c`, `out/concat_*.txt` |
| constants `(1, 9, 14)`, `60`, `28`, `168`, `R = 36` | **re-derived** | `r2_concat_bounds.py` |
| eleven rows of 11.72(b), exact certificates | **replicated with own certificates** | `r2_lp_site.py`, `out/lp_site.txt` |
| twelve rows + three gauche bounds of 11.72(c) | **replicated with own certificates** | `r2_lp_marked.py`, `out/lp_marked.txt` |
| vertices and volumes of `𝒦₁` (`3.2269`), `𝒦₂` (`3.125`) | **replicated** (exact: `697/216`, `25/8`) | `r2_volumes.py` |
| `26 437`, `191 833`, `392`, `2 195` (bulk box) | **replicated** (`26 437.00`, `191 833.00`, `392.20`, `2 194.60`) | `out/volumes.txt` |
| `3 627`, `23 272`, `93`, `393` (`𝒦₂`); `3 719 …` (`𝒦₁`); `4 673 …`, `3 809 …` (`𝒦₁^{(N)}`) | **replicated** (`3 626.50`, `23 272.00`, `92.50`, `392.80`; `3 719.33 …`; `4 673.16 …`; `3 809.31 …`) | `out/volumes.txt` |
| packings in `T₀`: 50 (52), 157 (162), 7, 14 | **replicated**: 51, 158, 7, 15 (exact rational check) | `r2_packing.py A`, `r2_packing_fine.py` |
| "proved at `N`": 3, 6, 10, 17, 22, 26, 31, 35 at 27 … 5 000 beads (`(1, ½)`) | **replicated to 2 000**: 3, 6, 10, 18, 22, 26, 32 (5 000: see below); other three rows likewise | `r2_packing.py B` |
| lamellae (densities, `k ≈ 2.5`) | **replicated** (own construction) | `r2_lamella.py` |
| the 166 199-bead bridge | **regenerated with the authors' builder, verified with my code** (exact match) | `r2_verify_witness.py` |
| the nine finite bridges at box 64 | same (all nine identical) | `out/witness_nine_W64.txt` |
| surface law, `k_N ∈ [1.71, 1.86]`, 38 % at 27 beads | **replicated** (`N ≤ 23` own tables; 24–27 engineering) | `r2_tables.py` |
| hairpins, `D − 14d ∈ [−15, −5]` | **replicated** (`a, b ≤ 40`) | `r2_flip.py` |
| walks against bridges (distances 3–6) | **replicated** for `N = 8 … 22` | `r2_walk_vs_bridge.py` |
| "two thirds of all directions" | **replicated** (`0.670`) with the authors' measure | `r2_directions.py` |
| periodic chain systems (`1.2·10⁹` systems, 5 680 densities, hull `2.22`), `γ_LP` values, "seven vertices not attained" | **read only** | — |
| estimates of the plateau (150–350, …) | **read only** | — |
| off-lattice estimates (S_REPORT §7.3) | **read only** | — |
| Lean: the abstract theorems compile and their axioms | see below | `R2Axioms.lean`, `out/lean_axioms.txt` |

Pending entries are completed in §6.1.

### 6.1 Late results

(filled in at the end of the review; see the end of this file)

### 6.2 How to re-run (from `experiments/science/ws_R2/`)

```
gcc -O3 -march=native -o bin/r2_enum r2_enum.c ; gcc -O3 -march=native -o bin/r2_concat r2_concat.c
for N in $(seq 4 23); do bin/r2_enum walk $N > out/walk_N$N.txt; done        # 323 s for N = 23
for N in $(seq 3 23); do bin/r2_enum bridge $N > out/bridge_N$N.txt; done    # 160 s for N = 23
python3 cmp_tables.py 4 23 ; python3 r2_lemma67.py 12 3000 ; python3 r2_tables.py
bin/r2_concat 13 ; bin/r2_concat 16 8 ; bin/r2_concat 8 16 ; python3 r2_concat_bounds.py
python3 r2_bridge_tables.py ; python3 r2_walk_vs_bridge.py
python3 r2_lp_site.py ; python3 r2_lp_marked.py ; python3 r2_volumes.py ; python3 r2_finite_sets.py
python3 r2_lamella.py ; python3 r2_rodpairs.py ; python3 r2_packing.py A ; python3 r2_packing_fine.py
python3 r2_packing.py B 27 60 120 250 500 1000 2000 5000
python3 r2_cover.py walk 21 1 1 1 2 ; python3 r2_cover.py bridge 21 1 1 1 2
python3 r2_flip.py 40 ; python3 r2_directions.py
python3 r2_verify_witness.py big ; python3 r2_verify_witness.py nine 64      # use the authors' build.py
python3 r2_inner_volume.py ; python3 r2_rigorous_packing.py
```

No random seeds matter for the verdicts (random tests use fixed seeds).  Largest memory: 1.4 GB
(`r2_packing.py B 5000`, `r2_cover.py eng 27`).

---

## 7. Originality (one paragraph; workstream A2 does the deep search)

The *type* of object is classical.  By Lemma 11.67 the profile part is the vector of interaction
energies of a three-shell lattice gas, and the set of attainable energy densities of a lattice
system is the set of expectation values of a local vector-valued function over translation-invariant
states — in dynamical language a **generalised rotation set** (Kucherenko–Wolf, *Geometry and entropy
of generalized rotation sets*, arXiv:1210.0135 **[abstract]**: the set of integrals of an
`m`-dimensional potential over invariant measures is compact and convex; every compact convex set
occurs for a subshift of finite type), whose extreme points are ground states; here the density is
per occupied site (a ratio of two such averages, i.e. a projective image, still convex) and the
configurations are chain systems rather than arbitrary site sets, which is where traceability and
the bridge/walk question enter.  The outer polytopes are the cluster ("configuration polytope")
method for ground states (Kanamori; Kaburagi–Kanamori **[from memory — unverified]**; Huang et al.,
arXiv:1606.07429 **[search snippet]**: "basic polytope method" = LP over cluster probabilities with
compatibility constraints).  **Fekete's lemma for sets exists in print** in the exact (not
approximate) form: Permuter–Weissman, *Capacity region of the finite-state multiple access channel
with and without feedback*, arXiv:0708.0271v1, Appendix IV, Lemma 23 and Corollary 24 **[full text
of the lemma and its proof]**: a bounded sequence of sets in `ℝ²` containing the origin with
`N·A_N ⊇ n·A_n + (N − n)·A_{N−n}` converges to `cl ∪_n A_n`, and the limit is convex.  Theorem 11.69's
abstract part is the version with a bounded additive error, increments in place of "contains the
origin", arbitrary finite dimension and an explicit one-sided rate — a routine extension; the
density-function theory of supermultiplicative models of walks (Janse van Rensburg **[cited by the
authors from abstracts; not read by me]**) is the same idea with entropy.  I did **not** find the
specific object (the body of (pair counts, gauche count) densities of diamond-lattice bridges), its
inequalities, or the identification of a limiting certificate size with a covering number of it;
"not found" after four generic searches, not "new".  In more than one dimension rotation sets of
subshifts of finite type need not be polytopes and ground-state energies of finite-range lattice
models are not computable in general (domino problem) **[from memory — unverified]**, so "the exact
shape of `𝒦`" is not guaranteed to have a finite description.

*Search log* (generic queries, 2026-11-25; search tool, then one abstract page and one PDF):
(1) "generalized rotation set multidimensional subshift of finite type ergodic averages
vector-valued function convex compact computability" → arXiv:1210.0135 (abstract read),
arXiv:1706.07973 (snippet: rotation sets of one-dimensional SFTs are computable).
(2) "set-valued Fekete lemma superadditive sequence of sets Hausdorff convergence convex limit" →
arXiv:0708.0271 (PDF read: Lemma 23, Corollary 24, their proofs).
(3) "configurational polytope ground states lattice gas cluster probabilities linear programming
Kanamori Kaburagi" → arXiv:1606.07429, arXiv:cond-mat/0010323 (snippets only; the Kanamori papers
did not surface).

---

## 8. Limitations of this review

* I did not re-enumerate walks with 24–27 beads; statements about those sizes use the engineering
  tables as data.  My enumeration agrees with theirs on the twenty sizes I did.
* The explicit bridges of N2, N3 and Proposition 11.72(e) come from the authors' generator; what is
  independent is their verification (coordinates → lattice walk, bridge, `(h, g)`).
* I did not check the periodic-system enumeration, the inner model, the estimates of the plateau,
  or anything off-lattice; nor Theorem 11.37 (used by the remark after Proposition 11.74).
* Volumes of Minkowski sums and of the eroded hull are floating-point (Qhull), cross-checked by the
  Steiner polynomial (`46.875 + 105ρ + 38.5ρ² + (4/3)ρ³` for `𝒦₂`); the vertex lists and the volumes
  of `𝒦₁`, `𝒦₂` are exact.  Certificates, packings and cover relations are exact.
* The parity argument of Conjecture 11.75(iv) was re-derived, not brute-forced.
* Prior art: three searches; one lemma read in full, one abstract; the rest snippets or memory.

---

## 9. Recommended corrective action

1. Rewrite the headline sentence in the five places of M1 with labels (theorem for `liminf`/`limsup`;
   convergence proved for bridges off an unidentified countable set; conjecture for walks; estimates
   for "hundreds" and for the chain length).
2. Replace the `liminf` column of Theorem 11.71(c) by bounds obtained from *all* proved points of
   `K^{br}` (N3: at least 116 at `(1, ½)`), and the volume statement by `1.56 ≤ vol 𝒦 ≤ 3.125` (N2);
   say "three vertices proved, two supported numerically".
3. Add the extension `Q_M = {0}`, `M ≤ 5`, to the application of the Lean theorem (m1), or restate the
   Lean theorem from an index `M₀`.
4. Corrections m2–m8 (wording).
5. Add the exhaustive concatenation test (`N ≤ 13`) to the falsification harness; it costs four
   minutes and found that `δ₃ = 1` is attained.

## 10. Unresolved questions

* Conjecture 11.75 (walks versus bridges) — untouched by this review.
* Is `ε₁ = ½` (or `¼`) a jump of `N_∞`?  Unknown as long as `K^{br}` is unknown.
* The routing lemma (periodic chain systems are limits of bridges); the true shape of `𝒦` between
  the proved `1.56` and `3.125`; whether the seven doubtful vertices of `𝒦₂` are artefacts.
* Finite-`N` constants for the marked programme (my certificates are `≤ 0` on all regular
  configurations, so only the at most 16 end configurations have to be bounded — an afternoon).
* Any rigorous statement about *when* the covering number is near its limit points.

## 11. The three most promising next steps

1. **Raise the proved lower bound further and compute an honest upper estimate from the same data.**
   Larger boxes (`W = 96, 128`: `δ ≈ 0.002`, gauche densities of the zero-gauche systems `≈ 0.05`) and an
   exact packing (integer programme on the conflict graph) in the hull of proved points.  The bracket
   `[116, 3 627]` should close to within a factor of about 10 without any new theory.
2. **Settle the routing lemma for the two simple structures** (woodpile `W₃`, crossed rods): both
   are stacks of layers of parallel rods and should admit an explicit snake construction like the
   lamella, which would prove the vertices `(0,3,4)` and `(½,4,9/2)` and enlarge the `γ = 0` region.
3. **A second-level linear programme** (the six-ring or the 17-site two-shell cluster) with exact
   certificates, to decide which of the seven unattained vertices of `𝒦₂` are artefacts.

## 12. Requests

**To the theory division.**  (a) Adopt corrections 1–5 of §9.  (b) State in §11.22 which accuracies
are known to be non-exceptional (none) and remove "the plateau is real".  (c) Either prove the
routing lemma for `W₃` and the crossed rods or label the corresponding vertices [N].  (d) Record N1
(the helix point) and N4.

**To the engineering division** (precise specification).  *Motivation:* tighten the proved bracket
for the limit points of `N^P_cov(ε₁N)` at `(L, ε₁) ∈ {(1, ½), (1, ¼), (⅕, ½), (⅕, ¼)}`.  *Formulation:*
(i) for each of the nine witnesses of `experiments/workstreams/S/out/witnesses.txt` build the finite
bridge in boxes of side 96, 128, 160 (the authors' `build.py` or an own builder), verify it
independently from coordinates, and store `(N, h₃, h₈, h₁₁, g)`; (ii) with the four exact points
`(0,0,0;0)`, `(½,2,3/2;0)`, `(1,5,6;0)`, `(0,0,1;1)` form the 4-dimensional hull, and solve the maximum
packing problem "points `Σλ_i q_i` of the hull with `L‖p_k − p_l‖_c > e(g_k + g_l) + 2ε₁ + max(L,e)(d_k + d_l)`,
`d = Σλ_iδ_i`, `δ_i = 168/(N_i + 3)`" on a grid of step `ε₁/(4L)` in the coordinates `u`, by integer
programming with a certified bound.  *Inputs:* the witnesses.  *Expected output:* integers `k(L, ε₁)`
with the packings in exact rationals; each is a proved lower bound for the `liminf`.  *Validation:*
`r2_rigorous_packing.py` gives 116 at `(1, ½)` with box 64 and a greedy packing; the result must be at
least that.  *Stopping condition:* optimality gap below 10 % or one hour per instance.  *Resources:*
bridges of up to `3·10⁵` beads (minutes each), integer programmes with about `10⁵` binaries
(conflict graph of bounded degree).  (iii) Independently of (ii): class tables of **bridges** for
`N = 24 … 27` with the full set of gauche counts per class, to extend the walk-versus-bridge comparison.

---

## 13. Late results (completing §6)

(see below)
