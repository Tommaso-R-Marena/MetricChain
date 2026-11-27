# Workstream P (science division) — physical applicability: do the envelope classes describe a real residual?

Report of an independent workstream of the Scientific Discovery, Translation & Independent
Validation Division.  Branch `research/scientific-translation` (theory files read at `5ed4072`).
All scripts, data and logs: `experiments/science/ws_P/` (running notes: `NOTES.md`).
Written 2026-11-25.  Named `SP_REPORT.md` because the theory division has a `P_REPORT.md`.

Epistemic labels as in `COMMON.md`: **[V]** machine-checked by the theory division (I cite the
Lean name as given in the theory report; I did not re-run Lean), **[P]** paper argument given
here, **[K]** known and cited, **[N]** numerical evidence produced here, **[C]** conjecture,
**[H]** heuristic/physical argument.  Everything in §3 is **independent replication of nothing**
— these are new measurements; what I took from the theory report I *read*, I did not re-derive
its proofs.  Units: kcal/mol and `k_BT = 0.596161 kcal/mol` at 300 K (`1 kcal/mol = 1.677 k_BT`).

---

## 1. Verdicts in one paragraph

On a real, public molecular-mechanics model (Amber ff14SB with GBn2 implicit solvent, as shipped
in OpenMM 8.6.1; capped alanine peptides Ace-(Ala)ₙ-NMe on rigid-geometry torsion grids,
enumerated exactly up to 531 441 conformations) the residual "implicit-solvent polarisation
energy relative to the vacuum force field" is **not near the first-order (per-torsion
bounded-difference) class in any useful sense**: its exact constants are `c_i = 7–32 kcal/mol
= 12–53 k_BT`; they grow with chain length (largest constant `≈ 4.8 + 4.5·n` kcal/mol for
`n = 1…6` residues on the three-state grid; slower, possibly saturating near 20 kcal/mol, on a
two-state grid without turn states, `n ≤ 9`) and on the three-state grid are a third lower at the chain
ends than in the interior (on the two-state grid this holds for φ but not for ψ) — the
predicted lever-arm effect is present as "growth with length", not as a law in the distance
to the nearer chain end; **no torsion is sharp in
any enumerated instance** (ratio of site gap to constant 0.03–0.47 in the extended basins;
collective cost-to-distance ratio `λ* = 0.038 … 0.0026` for two to six residues, where one
evaluation would need `λ* ≥ 1`); the mixed second differences are dense and as large as the
first-order constants (`c_ij` up to 29 kcal/mol at five residues, half row sums 52–89 kcal/mol);
and on the real instance a certificate of the global minimum in the per-torsion format needs
between 3 042 and 5 357 of the 28 843 clash-free conformations at five residues (447–782 of
3 844 at four, 94–139 of 508 at three): a fixed fraction of the domain.  The theory's formulas
with these numbers give an uncertifiable free-energy width of 43–48 nats per residue and
certificates of at least `10⁵` (10 residues) and `10⁵⁶` (100 residues) evaluations — while the
*actual* residual has a Jensen gap of 2–3 nats: it is the class that is expensive, not this
function.  **The same residual is close, in root-mean-square but not in supremum norm, to the
class the theory identifies as cheap** — pair-additive in atoms with unknown radial functions
("profile class", theory report §11.17): an explicit, exactly pair-additive function is within
`0.10–0.52 kcal/mol` RMS (`0.2–0.9 k_BT`) of it for two to eight residues, but only within
`0.2–9 kcal/mol` (up to `16 k_BT`) in the maximum, both growing with the chain; a fitted model
with 36 Amber-atom-type pairs has held-out remainder `0.26 / 2.2 kcal/mol` (RMS / max) at five
and `0.43 / 3.9` at eight residues, with slopes `≤ 0.9 kcal/mol/Å²`; one pair type is useless
(remainder = the whole variance), "pairwise GB" with frozen Born radii is useless (RMS 5
kcal/mol), and low-order expansions in the *torsion* variables are poor (all torsion pairs:
RMS 2.1, max 13 kcal/mol at five residues).  A sup-norm remainder estimated on a sample is not
a bound (held-out maxima were up to ten times the fitted ones).  **Differences between force
fields of one lineage lie exactly in the cheapest classes**: ff99SB − ff14SB is a sum of
single-φ terms (`c_i = 0.64 kcal/mol` on the grid, 1.115 on the full circle, independent of
length, all `c_ij = 0`; one evaluation certifies), ff19SB − ff14SB is one table per residue
(`c_i ≤ 2.6 kcal/mol`, `c_ij = 0` beyond the residue; two or three evaluations); a change of
charge model (ff03, ff15ipq) gives `βc_i ≈ 2–10`, slowly growing, half of the sites sharp in
the extended basin, certificates of at most 12–28 evaluations at four and five residues.  Yet even the
cheapest of these decides the answer: at five residues ff14SB prefers the helix and ff99SB
the β-strand, 0.64 kcal/mol per residue being enough to reorder two cooperative basins 0.9
kcal/mol apart.  So the answer to "which class do residuals live in" is: *model-to-model
corrections inside one functional form — additive or residue-local; a continuum-solvent term —
linear in pair-distance features of typed atom pairs up to a remainder that is sub-`k_BT` on
average and several `k_BT` in the worst case; nothing measured is a per-torsion envelope with
`βc ∼ 1`.*  The pilot is small (alanine only, ≤ 6 residues exact on the richer grid, rigid
bond geometry, grids of basins), all sup-norm numbers are properties of these finite domains,
and nothing here certifies a constant for a continuous conformation space.

---

## 2. Precise statements

Setting for all statements: the molecule Ace-(Ala)ₙ-NMe; conformations
`x = (φ₁, ψ₁, …, φₙ, ψₙ)` with all bond lengths, bond angles, ω = 180° and methyl rotations
fixed (§3.1); a **site** is one backbone torsion (`m = 2n` sites); grid **A3** has the states
φ ∈ {−150°, −70°, +60°}, ψ ∈ {−40°, +60°, +150°}, grid **A2** the states φ ∈ {−150°, −70°},
ψ ∈ {−40°, +150°}; the **clash-free domain** `X_τ` consists of the grid conformations in which
no two atoms separated by four or more bonds are closer than `τ = 0.70` times the sum of their
Amber Lennard-Jones radii `R_min/2`.  Known part `f` = ff14SB vacuum energy (torsion +
Lennard-Jones + Coulomb terms; bond and angle terms are constant by construction).  Residuals:

| symbol | definition | physical meaning |
|---|---|---|
| `g_GB` | GBn2 polarisation energy (`ε_in = 1`, `ε_out = 78.5`, no salt, no surface term) | solvent polarisation, many-body through the Born radii |
| `g_GBSA` | `g_GB` + ACE surface-area term | the default OpenMM `implicit/gbn2.xml` |
| `g_99`, `g_19`, `g_03`, `g_ipq` | vacuum energy of ff99SB, ff19SB, ff03, ff15ipq minus that of ff14SB, at identical coordinates | "model error" between force fields |
| `g_solv` | OBC2 polarisation energy minus GBn2 | difference between two solvent models |

`c_i(g) = max{|g(x) − g(x′)| : x, x′ ∈ X_τ differ in site i only}`;
`c_ij(g) = max |g(x^{ab}) − g(x^{a′b}) − g(x^{ab′}) + g(x^{a′b′})|` over quadruples in `X_τ`.

**Statement 1 [N, exact enumeration] (first-order constants of the polarisation energy).**
On A3 the exact constants of `g_GB` are, in kcal/mol:

| `n` | clash-free conf. | `c_i`, sites φ₁ ψ₁ … φₙ ψₙ | `max_i c_i` | `β·max` | RMS single flip |
|---|---|---|---|---|---|
| 1 | 8 | 9.0 7.0 | 8.96 | 15.0 | 5.7 |
| 2 | 64 | 14.0 10.5 12.4 9.2 | 14.02 | 23.5 | 6.1 |
| 3 | 508 | 16.1 12.4 18.6 16.4 15.1 11.2 | 18.63 | 31.2 | 6.5 |
| 4 | 3 844 | 17.3 13.4 22.9 20.0 22.9 20.5 16.3 12.8 | 22.90 | 38.4 | 6.5 |
| 5 | 28 843 | 18.8 16.9 25.9 22.0 27.5 25.2 25.6 22.6 19.8 16.0 | 27.48 | 46.1 | 6.5 |
| 6 | 215 409 | 20.1 17.5 27.4 25.1 31.6 29.3 27.2 27.0 31.2 26.2 19.8 17.4 | 31.62 | 53.0 | 6.4 |

and on A2 `max_i c_i = 3.7, 5.7, 9.1, 14.3, 14.6, 16.0, 17.7, 18.4, 19.0` for `n = 1…9`
(125 696 clash-free conformations at `n = 9`).  Least-squares summaries: A3
`max_i c_i = 4.81 + 4.51 n`, `mean_i c_i = 4.65 + 3.42 n`; A2 `max_i c_i ≈ 3.9 n^{0.78}`
(visibly sub-linear from `n = 4`); pooled over sites and lengths
`c_i = 3.60 + 2.31 m_i + 1.12·(2n)` on A3 (rms residual 2.3), `m_i = min(i, 2n + 1 − i)` the
distance to the nearer chain end in torsions; a pure power law in `m_i` has exponent 0.45 (A3)
and 0.36 (A2) and fits worse.  Within one chain on A3 the constants are lower for the two torsions
next to each end and flat in the interior (`n = 6`, by `m`: 18.7, 18.7, 26.8, 28.2, 29.3,
28.2); on A2 this holds for the φ torsions only (§3.3).  The root-mean-square change under a single-torsion flip does **not** grow (6.4–6.5
kcal/mol on A3, 3.6–3.7 on A2): the growth is in the extreme pairs, i.e. in what a sup-norm
envelope must cover.  Lower bounds by local search for longer chains are in §3.3.

*Reading.*  The lever-arm prediction of theory report §11.14 ("for contact-type residuals every
envelope in torsion-Hamming format has `c_i ≥ u₀⌊(m_i − 1)/2⌋`") is qualitatively confirmed for
a real residual in one respect — constants grow with the length of the chain — and only
partly in the other (they are smallest at the ends on A3, not uniformly on A2);
quantitatively the scale is `u₀ ≈ 2–5 kcal/mol` per residue, i.e. `β u₀ ≈ 4–8`.  The
regime `u = βc ∼ 1` in which the theory report evaluates its exponents (e.g. `0.029` at
`u = 1`, Theorem 11.25) is one to two orders of magnitude away from this residual.

**Statement 2 [N, exact] (second-order constants).**  For `g_GB` on A3 the matrix `c_ij` is
dense, with entries of the size of the first-order constants and slow decay in `|i − j|`: at
`n = 4`, by separation `|i − j| = 1…7`, the largest entries are 23.1, 22.4, 18.9, 12.2, 11.9,
7.2, 7.0 kcal/mol; half row sums `½Σ_j c_ij` are 37–60 kcal/mol; the Dobrushin-type row sums
`Σ_j tanh(βc_ij/4)` are ≈ 7 (Theorem 11.33(a) needs `< 1`).  At `n = 5`: largest entry 28.8
kcal/mol, by separation 28.8, 28.8, 24.9, 19.2, 17.0, 11.5, 10.4, 6.0, 8.1; half row sums 52–89.
On A2 at `n = 8`: largest entry 16.2, still 6.8 kcal/mol at separation 15; half row sums 37–70.  The row-sum condition of theory
report §11.7 (`½Σ_j c_ij ≤` single-site excitation energy) fails by one to two orders of
magnitude.  `g_GB` in torsion coordinates is a *dense second-order class with large constants*,
the case of Theorem 11.32(i), not the weakly coupled case of Theorems 11.16–11.17.

**Statement 3 [P, checked numerically to rounding] (same-lineage force-field differences are
exactly low-order).**
(a) `g_99 = E_ff99SB − E_ff14SB` is, on every conformation with fixed bond geometry, a sum of
functions of single φ torsions, up to `2·10⁻⁵ kcal/mol`: `c_i = 0.64 kcal/mol` on φ sites, `0`
on ψ sites, for every `n`, and `c_ij = 0`.
(b) `g_19 = E_ff19SB − E_ff14SB = Σ_k t(φ_k, ψ_k)`: `c_i = 1.54` (φ), `2.59` (ψ) kcal/mol on A3,
independent of `n`; `c_ij = 2.48` for the two torsions of one residue and exactly `0` otherwise.
*Proof.*  ff99SB, ff14SB and ff19SB share Lennard-Jones parameters and partial charges (the
OpenMM files differ in the fourth decimal of one charge, which is the `2·10⁻⁵`); they differ in
torsion terms about the N–Cα and Cα–C bonds and, for ff19SB, in a CMAP term on `(φ_k, ψ_k)`.
With rigid bond lengths and angles every proper torsion about N–Cα is a function of `φ_k`
alone, every one about Cα–C of `ψ_k` alone, and all other bonded terms are constant.  For
alanine the ff99SB→ff14SB change touches only terms about N–Cα.  ∎  (Numerically: the measured
`c_ij` are zero to the printed precision and the constants do not depend on `n`; §3.3.)
So the "model error" between two generations of one force-field family is a *linear class
with `n(k−1)+1` (resp. `n(k²−1)+1`) coefficients* — Theorem 11.47(c) applies literally: that
many evaluations determine it on the whole grid — and a first-order class with `βc ≤ 4.3`.
This is special to changes that leave the non-bonded model untouched.

**Statement 4 [N, exact] (force fields with different charges; two solvent models).**
`max_i c_i` in kcal/mol on A3, `n = 1…6`: `g_03`: 2.6, 3.0, 3.9, 4.6, 4.6, 4.9; `g_ipq`: 2.8, 3.4,
4.2, 5.0, 5.0, 6.1; `g_solv` (`n = 1…5`): 1.3, 1.7, 2.1, 3.0, 5.8.  On A2, `n = 1…9`: `g_03`:
1.0, 1.1, 1.5, 1.7, 2.0, 2.0, 2.1, 2.2, 2.3.  These grow slowly (0.1–0.6 kcal/mol per residue).
`c_ij(g_03)` at `n = 4` by separation: 3.9, 2.6, 2.0, 1.1, 0.9, 0.7, 0.7 — neither sparse nor
large.  In `k_BT`: `βc_i ≈ 2–10`.

**Statement 5 [N] (best approximations of `g_GB` in linear classes).**  Remainders in kcal/mol;
"max" is the largest absolute remainder.
(a) *Functions of few torsions* (A3, `n = 5`, all 28 843 clash-free conformations, least
squares; standard deviation of `g_GB` 7.61):

| class | parameters | RMS | max |
|---|---|---|---|
| sum of single-torsion terms | 31 | 3.94 | 17.8 |
| one table per residue `(φ_k, ψ_k)` | 41 | 2.63 | 16.2 |
| all torsion pairs | 431 | 2.10 | 13.4 |
| all residue pairs (functions of four torsions) | 681 | 1.13 | 9.1 |
| residue triples in a window of three residues | 1 961 | 0.58 | 7.3 |

Sup-optimal (Chebyshev, linear programme) remainders at `n = 4` (3 844 conformations): single
torsions `η = 10.3`, torsion pairs `5.0`, residue pairs `2.7` kcal/mol (`17`, `8.4`, `4.5 k_BT`).
Restricting pairs to a window of `w` torsions hardly matters beyond `w = 3` (RMS 2.13 at
`w = 3` against 2.10 for all pairs): the pair part is local, the remainder is not pairwise.
(b) *Profile class of theory report §11.17* — `g ≈ c₀ + Σ_{p<q} φ_{τ(p,q)}(s_pq)`, `s = r²`, `φ_τ`
continuous and piecewise linear in `s` with 44 knots between 1.5 and 40 Å, all atom pairs
separated by three or more bonds, no cutoff — fitted on 8 000 **off-grid** conformations
(ensemble C, §3.1) and tested on 8 000 others (standard deviation of `g_GB`: 5.47 at `n = 5`,
6.89 at `n = 8`):

| pair types | parameters | held-out RMS / max, `n = 5` | `n = 8` | largest fitted slope `L_s` |
|---|---|---|---|---|
| one type | 37 | 5.11 / 25.0 | 6.57 / 32.0 | 0.12 kcal/mol/Å² |
| element pairs (10 types) | 321–365 | 0.56 / 3.45 | 1.04 / 5.74 | 0.72 |
| Amber atom-type pairs (36 types) | 1 101–1 268 | **0.26 / 2.19** | **0.43 / 3.94** | 0.89 |

The radial functions fitted at eight residues describe the shorter chains with only the
constant refitted (RMS 0.25–0.36 for `n = 3…6`); those fitted at five residues fail at eight
(RMS 4.8) because distances beyond 22 Å were never seen — the exactly pair-additive Coulomb
energy fails the same way.  Control: the vacuum Coulomb energy — exactly pair-additive, but
with pair-specific coefficients — has the same remainder in the typed class (0.30 / 2.1 and
0.74 / 4.5), so with typed pairs the remainder is dominated by the typing.  A sup-norm fit
with a uniform slope bound `|φ′| ≤ L_s` (linear programme, element types, 2 500 training
conformations, `n = 5`) has training remainder `η*(L_s) = 1.06, 1.06, 1.48, 4.0, 8.7` kcal/mol
at `L_s = ∞, 1, 0.3, 0.1, 0.03` kcal/mol/Å² and held-out maxima of 6–21 kcal/mol: **a sup-norm
remainder estimated on a sample is not a bound.**
(c) *Distance to the exactly pair-additive class* (every atom pair its own radial function).
The explicit function `S = Σ_{p<q} e_pair(r_pq; B̄_p, B̄_q) + w₀ + Σ_p w_p I_p` of §3.4 — GB cross
terms with frozen mean Born radii plus a linear function of the pair-additive descreening
sums `I_p`, `N + 1` fitted weights — is exactly pair-additive, and `g_GB − S` has (RMS / max,
kcal/mol): on held-out conformations of ensemble C 0.10 / 0.9, 0.21 / 2.6, 0.30 / 4.1,
0.34 / 3.5, 0.43 / 5.4, 0.52 / 6.1 for `n = 2, 3, 4, 5, 6, 8`; on **all** clash-free
conformations of the A3 grids 0.14 / 0.5, 0.27 / 1.0, 0.39 / 2.3, 0.48 / 4.8 for `n = 2…5`; on all
35 478 of the A2 grid at `n = 8` 0.47 / 9.3.  Freezing the Born radii *without* the linear term
— the naive pairwise GB — leaves RMS 2.1–7.2 kcal/mol, although the radii fluctuate by only
2–4 % on average.  Hence the sup-norm distance of `g_GB` to the pair-additive class is **at
most** 0.5, 1.0, 2.3, 4.8 kcal/mol on the A3 domains of two to five residues (I have no lower
bound), `βη_RMS ≈ 0.2–0.9` and `βη_sup ≲ 1–16`, both growing with the chain.

**Statement 6 [N, exact on the grids] (sharpness; certificates on the real instance).**
Instance: `X = X_τ` (A3), `f`, `g`, `E = f + g`, envelope `d = Σ_i c_i(g)[x_i ≠ y_i]` with the
exact constants (checked to be a valid envelope on the non-product domain:
`max_{x≠y} |g(x) − g(y)|/d(x,y) = 1.0000`).
(a) For `g_GB`, `n = 3, 4`: the minimiser of `f` is the all-β conformation, the minimiser of `E`
the all-PPII one (the residual moves the minimum; `E(argmin f) − min E = 1.57, 2.13` kcal/mol);
the single-site excitation energies of `f` at its minimiser are 0.7–1.4 (φ) and 4.6–5.3 (ψ)
kcal/mol against `c_i = 11–23`: **no site is sharp** (`e_i/c_i = 0.03–0.47`), and the criterion
of Theorem 11.7 [V] fails for 486 of 507 and 3 824 of 3 843 competitors.  At `n = 5` the
minimiser of `f` is the α-helix and that of `E` is PPII, 0.46 kcal/mol apart; at `n = 6` the
helix minimises both (PPII is 0.37 kcal/mol above it with GBn2, 9.3 in vacuum), and 8 of 12
single flips out of it are sterically excluded in the rigid geometry; the remaining ones
cost 8–20 kcal/mol and are still below their constants.  The collective criterion (Theorem
11.7 for all competitors at once) is `λ* := min_y (E(y) − E(x*))/d(x*, y) ≥ 1`; measured:
`λ* = 0.038, 0.031, 0.020, 0.0045, 0.0026` for `n = 2…6` (§3.5).
(b) Smallest certificates of `min E` in the per-torsion format (set cover with radii
`gap(y) + ε`, Theorem 11.4 [V]); lower bound = the larger of the number of conformations that
only themselves cover and the volume bound `Σ_y 1/M(y)` (both Theorem 11.6(a) [V]), upper bound
= greedy cover:

| residual, `n` | conformations | `ε = 0` | `ε = k_BT` | `ε = 2` kcal/mol |
|---|---|---|---|---|
| `g_GB`, 3 | 508 | [94, 139] | [85, 130] | [61, 112] |
| `g_GB`, 4 | 3 844 | [447, 782] | [378, 717] | [261, 609] |
| `g_GB`, 5 | 28 843 | [3 042, 5 357] | [2 668, 5 033] | [1 947, 4 307] |
| `g_GB`, 8 (grid A2) | 35 478 | [4 061, 8 041] | — | — |
| `g_99`, 5 | 28 843 | 1 | 1 | 1 |
| `g_19`, 5 | 28 843 | [2, 3] | [2, 3] | [2, 3] |
| `g_03`, 5 | 28 843 | [2, 28] | [2, 22] | [2, 10] |
| `g_99`, 4 | 3 844 | 1 | 1 | 1 |
| `g_19`, 4 | 3 844 | [2, 11] | [2, 8] | [2, 4] |
| `g_03`, 4 | 3 844 | [2, 12] | [2, 9] | [2, 7] |
| `g_ipq`, 4 | 3 844 | [2, 21] | [2, 18] | [2, 11] |
| `g_solv`, 4 | 3 844 | [6, 21] | [2, 15] | [2, 6] |

The lower bound for `g_GB` grows by factors 4.8 and 6.8 per residue while the domain grows by
7.6 and 7.5: the certificate is a fixed fraction (10–19 %) of the domain.
(c) The exact Jensen gap `ln Z(f+g) − ln Z(f) + β⟨g⟩_f` on these grids is 2.1, 2.6, 2.3 nats for
`g_GB` at `n = 3, 4, 5`, whereas the worst case over the first-order class with the same
constants, `Σ_i ln cosh(βc_i/2)` (Theorems 3.1(e), 11.25), is 71, 117, 178 nats: **the physical
residual is nowhere near the extremal member of its own first-order class**; what makes the
class expensive is the class, not this function.

**Statement 7 [N + V-formulas] (what the theory's formulas give for 10 and 100 residues).**
Inputs: constants extrapolated from Statement 1 in three ways — *plateau* (no growth beyond the
enumerated lengths), *linear* (`c_i = 10.34 + 3.43 m_i`, the pooled fit) and *power*
(`12.72 m_i^{0.45}`); site tables of the known part taken from the all-β star at `n = 6`
(φ: 0, 0.8, 21.6; ψ: 0, 4.8, 5.2 kcal/mol).  Formulas: `Σ_i ln cosh(βc_i/2)` and the product
bound `ln N_cov ≥ max_t Σ_i [ln Σ_s e^{−tφ_i(s)} − ln(1 + (k−1)e^{−tc_i})] − tε`
(`product_partition_bound` [V], valid for an additive known part and the zero residual).

| chain | scenario | `c_i` (kcal/mol) | sharp sites | `Σ ln cosh(βc_i/2)` | `ln N_cov ≥` (`ε = 0`) | of `ln|X|` |
|---|---|---|---|---|---|---|
| 10 residues | plateau | 19–29 | 0 / 20 | 427 nats = 255 kcal/mol | 12.5 (`N ≥ 10^{5.4}`) | 22.0 |
| | linear | 14–45 | 0 / 20 | 476 nats | 12.3 | 22.0 |
| | power | 13–36 | 0 / 20 | 428 nats | 12.0 | 22.0 |
| 100 residues | plateau | 19–29 | 0 / 200 | 4 567 nats = 2 722 kcal/mol | 129 (`N ≥ 10^{56}`) | 219.7 |
| | linear | 14–353 | 0 / 200 | 30 640 nats | 171 (`10^{74}`) | 219.7 |
| | power | 13–102 | 0 / 200 | 11 738 nats | 157 (`10^{68}`) | 219.7 |

These are *model-relative* numbers: they say what a certifier that knows only the per-torsion
constants must pay, on a product landscape with the measured single-site numbers.  They are
not statements about the peptide (its landscape is not a product, §3.5), and by Statement
6(c) they are wildly pessimistic about the actual residual.  The measured instances are
consistent with them: the product formula predicts `N ≥ 15` and `60` at `n = 3, 4`, the real
covers need at least 94 and 447.

**Statement 8 [N] (continuous torsions).**  Along one torsion, with the others fixed at
off-grid conformations of ensemble C (10° scans; maxima over 80–200 sampled bases, hence lower
bounds on the suprema): `g_GB` oscillates by up to 13–16 kcal/mol at `n = 2`, 14–24 at `n = 5`
and 12–20 at `n = 8` (median 6.2–6.7 at every length); its torsion-space Lipschitz constants
reach 9–11, 9–21 and 9–27 kcal/mol/rad (median 4.1–4.7).  With these `L_i` the threshold of
Theorem 11.34 for the torus, `J = Σ_i ln(sinh b_i/b_i)`, `b_i = βL_iπ/2`, is 85, 295 and 566 nats
at `n = 2, 5, 8`.  For `g_03`: oscillation ≤ 5.5 kcal/mol, `L_i ≤ 5.9 kcal/mol/rad`, `J = 31, 83,
128` nats.

**Statement 9 [P] (what the measured numbers do and do not license).**  (i) Every number in
Statements 1–6 is an exact property of a finite domain (a grid with a clash filter) and of the
OpenMM implementation of the force field; it is a *lower bound* for the corresponding constant
of any superset of that domain, in particular of the continuous torsion space, and no upper
bound for it.  (ii) A certified envelope constant for the continuous space needs an upper
bound, i.e. interval arithmetic or a Lipschitz bound of `g` over torsion voxels; the sampled
Lipschitz constants of Statement 8 show that such a bound cannot be below
`≈ 20 kcal/mol/rad` for the pentapeptide.  (iii) Because the constants are maxima, they are
controlled by the most compact and the most extended conformations of the domain; restricting
the domain lowers them: on the pentapeptide grid, among the 52 conformations within 5 kcal/mol
of the minimum of `f` the polarisation energy varies by 6.0 kcal/mol in all (55.6 over the
whole domain), and among the 5 378 within 20 kcal/mol the largest constant is 14.6 instead of
27.5 kcal/mol.  But a window of the known part contains the minimiser of `f + g` for certain
only if its width exceeds the range of `g` outside it — the envelope is needed to justify the
restriction that would make the envelope small (request T-1).

---
## 2.B The physical reading of the mathematics

One row per mathematical object.  "Pilot" refers to the measurements of §§2–3.

| # | mathematical object | physical counterpart | the identification is valid when | what is lost | what must be measured or certified to use it |
|---|---|---|---|---|---|
| 1 | finite configuration space `X = ∏ D_i` (sites × states; theory report §1) | a discretised conformation space: rotamers of side chains on a fixed backbone; torsion wells (rotational-isomeric-state models); voxels of torsion space; lattice walks | every state is a cell of the continuous space on which the energy can be *enclosed* (`voxel_boltzmann_bounds` [V] needs `E_lo ≤ E ≤ E_hi` on the cell and its measure), the cells are products over sites (`certified_torsion_partition` [V]), and bond lengths/angles are either rigid or integrated out into the known part | vibrational entropy and relaxation inside a cell; bond-angle flexibility (in the rigid geometry 58 % of the `(φ,ψ)` plane of the dipeptide is a steric clash and the α_L region lies 6–10 kcal/mol above the minimum; relaxed maps put it much lower **[K, from memory]**); the Jacobian of rigid constraints; kinetics | interval enclosures of every energy term over every cell — these widen with the lever arm (cell width × arm length); pilot: along one torsion `g_GB` changes by up to 20 kcal/mol/rad, so a cell must be ≲ 2° wide for `k_BT` resolution of the residual alone; the excluded (clash) cells; the product structure — pilot: only 41 % of the A3 grid of the hexapeptide is clash-free, the domain is not a product |
| 2 | known part `f = Σ h_i(x_i) + Σ J_ij(x_i, x_j)` | a molecular-mechanics energy.  It is pairwise in *atoms*; it is pairwise in the *site variables* exactly when each atom's position depends on one site: fixed-backbone side-chain placement (every side-chain atom depends on its own rotamer), rigid-body pose tables, lattice or contact models written in bead positions | fixed backbone (or a finite set of backbones treated as one extra site); force field without many-body terms; then `h_i`, `J_ij` are sums of atom–atom terms and exact | for a flexible backbone nothing is pairwise in torsions: the distance of two atoms depends on every torsion between them.  Pilot: the vacuum ff14SB energy of the tetrapeptide has `c_ij(f)` up to 28 kcal/mol (12 kcal/mol at separation seven), and its best pairwise-in-torsions approximation leaves RMS 2.1 and sup-optimal 6.1 kcal/mol — the "known part" of the theory does not exist in backbone torsion variables | rational tables with outward rounding (straightforward at rotamer *points*); over voxels, interval evaluation of Lennard-Jones and Coulomb terms; a statement of which terms were moved into the residual |
| 3 | residual `g = E − f` | continuum-solvent polarisation (GB, PB: many-body through the dielectric boundary); explicit polarisation; quantum-chemical minus force-field energy; a learned correction; backbone-relaxation energy; the difference of two force fields | the split is a *choice*: `g` should be the part that is expensive, non-decomposable, or uncertain | the theory treats `g` as a black box known through class membership and point evaluations; all structure of the functional form (pair-additivity in atoms, locality in space, the anticorrelation of polarisation with Coulomb energy — pilot: `c_i(Coulomb + GB)` is half of `c_i(GB)`) is lost unless it is put into the class | which class, with which constants (this report: Statements 1–5); the split itself can be optimised (screened Coulomb in `f`) |
| 4 | envelope `d` / class: bounded differences `c_i`; torsion-space Lipschitz constants; mixed differences `c_ij`; profile slope `L` | an a-priori worst-case bound on how much the correction can change when one degree of freedom changes — a *sup-norm* error bar | the bound holds for **all** pairs of configurations of the domain | typicality and correlation: force-field accuracy is quoted as RMS error; pilot: sup/RMS is 4.2 for single flips of `g_GB` at five residues (27.5 against 6.5 kcal/mol) and 8.4 for the profile remainder (2.19 against 0.26); the exact Jensen gap is 2.3 nats where the class allows 178 | an *upper* bound: interval arithmetic over the domain or a proved Lipschitz property of the functional form, plus (for Corollary 4.7) inertia bounds.  None exists for a production force field.  For torsion-refit differences the bound is elementary: `g_99` is a trigonometric polynomial of φ with range 1.115 kcal/mol on the whole circle (§3.6) |
| 5 | anchors `(a, g(a))` | single-point evaluations of the expensive model at chosen conformations: a GB/PB solve, a quantum-chemical single point, an inference of a learned potential.  No experiment measures `g` at a chosen conformation | the evaluation is exact at exactly that configuration (or comes with an interval: the kernels accept interval anchors) | convergence and discretisation error of the expensive calculation; for voxels a point value is not an enclosure | the number of evaluations is the theory's cost; the search over `f` (NP-hard, theory report §8) is not counted |
| 6 | `min E` | the global minimum-energy conformation of the *model* on the discretised space | it predicts a structure only if (a) the Gibbs weight of its basin dominates and (b) the model error is below the gap to competing basins — which is the theory's own sharpness condition (Theorems 2.4, 11.7 [V]) | pilot: for the pentapeptide the helix is the minimum in vacuum and PPII with GBn2, 0.46 kcal/mol apart; for the hexapeptide the helix wins in both — with GBn2 by 0.37 kcal/mol over PPII, in vacuum by 5.5 kcal/mol over the β-strand; the uncertainty constants are 16–32 kcal/mol for the solvent term and 1.4–5 kcal/mol between charge models: the minimiser is not a model-robust object for a flexible peptide (7 grid conformations lie within 1 kcal/mol of the minimum, 38 within 2, at `n = 6`) | the gaps of the known part against the constants, site by site or droplet by droplet (Theorem 11.39) |
| 7 | `ln Z_β` | conformational free energies | **observable**: differences between macrostates of one model (populations of basins; binding constants as ratios of partition functions) and between thermodynamic states (temperature, and gas phase → solvent: if `f` is the gas-phase energy and `g` a solvation potential of mean force, `ln Z(f+g) − ln Z(f)` is `−β` times a hydration free energy).  **Not observable**: the absolute `ln Z` of a discretised model (depends on cell volumes and the energy zero), and `ln Z(f+g) − ln Z(f)` when `g` is a model correction (force field → better force field): a model-to-model free energy | in differences, correlated errors cancel physically, but not in a first-order class ("the sum of the two thresholds, no cancellation", theory report §11.13) | the accuracy that matters is ≈ 1 kcal/mol = 1.7 `k_BT` on differences; the class threshold measured here is 43–48 nats per residue |
| 8 | inverse temperature `β`; the scale `u = βc` | at 300 K, `1 kcal/mol = 1.68 k_BT` | — | the theory report tabulates exponents at `u = 0.5–2.8`, i.e. `c = 0.3–1.7 kcal/mol` | pilot: `βc_i = 12–53` for the solvent term (the theory's zero-temperature regime: `ln cosh(u/2) ≈ u/2 − ln 2`), `2–10` between charge models, `1.1–4.3` between force fields of one lineage |
| 9 | the hint (an instance handed to an algorithm that must still be correct on the class; §11.10) | a surrogate of the residual: a cheaper solvent model, a fitted pair-additive approximation, a learned potential, or the output of a heuristic search, which expensive evaluations then spot-check | the surrogate is free and correctness is demanded on the class, not on the surrogate | — | pilot: a fitted typed pair model predicts `g_GB` to 0.26 kcal/mol RMS (max 2.2) — a good hint; the theory's price for checking it is set by the class, not by the quality of the hint |
| 10 | product landscapes (additive `f`, independent sites); the cube | independent degrees of freedom: side chains that do not interact (far apart on a fixed backbone), independent rotors on a stiff scaffold, independent two-state titration or tautomer sites (the cube), the reference system of a mean-field theory | couplings small against site gaps (a Dobrushin-type condition) | cooperativity, excluded volume, phase transitions.  Pilot: a peptide backbone is not product-like — in the helix basin of the hexapeptide 8 of 12 torsions have no clash-free single-flip neighbour at all and the others cost 8–20 kcal/mol, while the collective excitation to PPII (six torsions changed) costs 0.37 kcal/mol in total | the exponents `R*`, `R_β` are properties of this idealisation; for a chain the relevant theorems are 11.39–11.40 (droplets) and the general Theorem 11.6 |
| 11 | the lattice chain of §11.22 (diamond lattice, trans/gauche, pair counts at three distances, known part `e·#gauche`) | a rotational-isomeric-state homopolymer with excluded volume and a three-shell contact energy: a coarse-grained model of collapse and of stiff attractive chains | questions about scaling and the thermodynamic limit of a homopolymer | chirality, sequence, hydrogen-bond directionality, continuous distances (off-lattice the profile is a function and the number of features grows with the chain) | whether a real residual depends on the conformation through pair-count profiles: pilot — with one pair type, as in the lattice model, not at all (remainder = total variance); with 36 atom-type pairs and ≈ 40 distance bins, to 0.26 kcal/mol RMS |
| 12 | second-order class (`c_ij`), sparse or dense (§§11.7, 11.12) | "the correction is pairwise in the site variables up to `c_ij`" | sparse or weak: corrections that are local in the sequence (pilot: `g_19`, exactly one table per residue) | — | pilot: for the solvent term in backbone torsions the constants are dense and large (Statement 2) — the unfavourable case of Theorem 11.32 |
| 13 | linear class `g = θ·F`, `θ` in a box (Theorem 11.47); profile class (Theorem 11.48) | an energy model that is linear in its parameters with parameter uncertainty: torsion Fourier amplitudes, CMAP grid values, products of partial charges, Lennard-Jones coefficients; contact potentials; linear machine-learned potentials | the features are known and the remainder is small in sup norm | steep short-range terms (a Lipschitz bound in `s = r²` must depend on distance); many-body terms | pilot: same-lineage force-field differences are exactly of this kind (Statement 3); the solvent term is so up to `η_RMS = 0.26`, `η_sup ≈ 2–6 kcal/mol` at five residues with ≈ 10³ coefficients; the sup remainder must be *bounded*, not sampled (Statement 5) |
| 14 | certificate and kernel (rational arithmetic, soundness theorem) | a proof-carrying computation about the model | always — it is mathematics | it certifies nothing about nature: every input (tables, constants, anchors) is a modelling statement | the inputs |

### Three questions of the brief

**(i) For which physical question, system size and accuracy could a certificate be produced
today, with constants one could actually certify?**
*(a) Fixed-backbone side-chain placement with a pairwise force field and no residual.*  Here
row 2 holds exactly, the tables are evaluated at rotamer points (no voxel enclosure, no lever
arm), and the certified statement is "this assignment is the global minimum of this rotamer
model".  The sizes are those of the kernel, not of the physics: the theory report (§12 item 7)
states that kernel evaluation does not scale and that no certificate producer at realistic
sizes exists; the comparison to make is with existing exact solvers for this problem (dead-end
elimination with A*, cost-function networks, integer programming), which routinely solve
instances with tens to hundreds of positions **[K, from memory — unverified in this
workstream]**.  *(b) Robustness of a minimiser against a same-lineage reparametrisation.*  The
constants of `g_99` are certifiable today and for every chain length — a one-dimensional
trigonometric polynomial with range 1.115 kcal/mol (§3.6) — and Theorem 11.7 then decides,
site by site, whether the minimiser can change.  With the *grid* constant (`c = 0.64` kcal/mol on the three
A3 states) every site is sharp for `n ≤ 4` (gaps `≥ 0.68`), by 0.04 kcal/mol at the tightest
site, and at `n = 4` the exact criterion still fails for one multi-site competitor by 0.06
kcal/mol because `f` is not additive (zero evaluations do not certify; one does, Statement
6(b)).  With the certified *circle* constant 1.115 the φ sites (gaps 0.7–1.4) are not all
sharp.  A true but fragile certificate.  *(c) Conformer ranking of a small molecule with an expensive
correction.*  This is the regime of Statement 4: `βc_i ≈ 2–10`, about half of the torsions
sharp, certificates of about ten evaluations among 3 844 conformations at eight torsions —
*given* the constants.  That is the first-order format doing something useful, and it is the
provable version of what conformer workflows do by hand (re-rank everything within an energy
window by the expensive method; the theory says the window is the envelope distance to the
incumbent, not a fixed number of kcal/mol).  The constants are not certified for any
quantum-chemical residual; the pilot's stand-in is a second force field.  *(d) Coarse-grained
chains with contact potentials of unknown strength.*  The class is exact by construction and
rank-many evaluations suffice; this is synthetic.  **In short: today a certificate with
certified inputs exists only where there is no residual, or where the residual has an explicit
analytic form (torsion refits, parameter boxes).  For a continuum-solvent term nobody has a
certified constant, and the measured ones put the per-torsion format out of reach beyond three
or four residues.**

**(ii) Which results are resolution statements about models rather than algorithms, and what
do the measured numbers say?**
Resolution statements: the sharp-minimum and contact-set theorems (2.3, 2.4, 11.2, 11.7: with
uncertainty `c_i` per site the model determines its own minimiser iff every site — on a chain,
every droplet — is sharp); thermal contact (11.12: the interval of Gibbs probabilities of a
state over the class); the free-energy sandwich and its exact constant (3.1: `Σ ln cosh(βc_i/2)`
is the largest free-energy shift the class allows at a given reference average); Theorem 11.35
(Boltzmann averages are uncertain over most of their a-priori range).  These say what *any*
user of the model can conclude from class membership, whatever they compute.  The lower bounds
on evaluations (11.6, 11.8, 11.13, 11.23–11.25) are information statements of the same kind:
they bound every algorithm.  Algorithms proper are the kernels, learn-then-cover, the hedged
spot-check and the nested samplers.  The measured numbers say: for the solvent residual
**typical sites are not sharp** (ratio of gap to constant 0.03–0.47 in the extended basins,
and the minimiser itself changes between `f` and `f + g` at `n = 3, 4, 5`); for a change of
charge model about half the torsions are sharp (the ψ torsions, whose second well lies 4.7
kcal/mol up; the φ torsions, where the β and PPII wells differ by 0.7–1.4 kcal/mol, are not);
for a same-lineage torsion refit all are — site by site; collectively not: at `n = 5` the
minimiser changes between ff14SB and ff99SB (§3.5).  In the helix basin most single-site excitations are sterically
excluded and the relevant quantity is collective: the cost-to-distance ratio
`λ* = min_y (E(y) − E(x*))/d(x*, y)` (the factor by which all constants would have to shrink
for one evaluation to certify; cf. Theorem 11.39) is 0.038, 0.031, 0.020, 0.0045, 0.0026 for
`n = 2…6` (§3.5): **no torsion is sharp in any enumerated instance, in any basin, and the
constants are 26–380 times too large.**

**(iii) What is the smallest set of additional physical assumptions under which the
exponential lower bounds stop applying, and does the real residual satisfy them?**
The lower bounds are theorems about first-order classes, in which an evaluation informs only
about a neighbourhood.  They stop applying as soon as the class is *finite-dimensional in
known features with a small sup-norm remainder* (Theorem 11.47(c),(d)).  Physical assumptions
that give this: (A1) finite interaction order in the site variables with known supports;
(A2) pair-additivity in atoms with radial functions from a controlled family; (A3) locality
along the chain.  Not sufficient alone: smoothness (Theorem 11.34 is exponential on the torus)
and weak coupling unless it is weak in the sense of Theorem 11.33 (`Σ_j tanh(βc_ij/4) < 1`).

| assumption | `g_99` | `g_19` | `g_03`, `g_ipq` | `g_GB` |
|---|---|---|---|---|
| (A1) low order in torsions | exact, order 1 | exact, order 2 inside a residue | approximately: pairs of residues leave RMS 0.12, max 1.4 kcal/mol (`n = 5`) | no: torsion pairs leave RMS 2.1, max 13; residue pairs RMS 1.1, max 9 |
| (A2) typed pair-additivity in atoms | yes (at rigid geometry a cosine torsion term is a function of one 1–4 distance) | not tested | yes to RMS 0.11, max 1.3 (36 types, `n = 5`) | in RMS yes (0.26), in sup norm to 2–6 kcal/mol; the remainder grows with the chain (§3.4) |
| (A3) locality along the chain | yes | yes | no (`c_ij` decays to 0.7 kcal/mol but not to zero) | no (`c_ij = 7` kcal/mol at separation 7) |
| weak coupling, `Σ_j tanh(βc_ij/4) < 1` | 0 | 0.78 | 4.1 | 7.0 |

So the real solvent residual leaves the first-order world only through (A2), and there the
theory's replacement guarantee carries an accuracy floor of at least `2η_sup ≈ 4–12 kcal/mol`
at five residues (Theorem 13 of the theory division's workstream P: `η(1 + ‖λ‖₁)`), far above
`k_BT`.  The statement "GB is close to pair-additive" is true in the sense in which force
fields are judged (RMS) and false in the sense in which certificates need it (sup norm, with
a *proved* bound).

---
## 3. Numerics: what was computed, sizes, results, how to re-run

All files are in `experiments/science/ws_P/`.  Run from that directory with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1`.  Requirements: Python 3.13,
numpy, scipy, `pip install openmm numexpr` (OpenMM 8.6.1 and numexpr 2.14.2 were installed for
this workstream; nothing else).

### 3.1 Model and modelling choices (every one of them)

* **Molecules.**  Ace-(Ala)ₙ-NMe, `n = 1…6` (three-state grid), `1…9` (two-state grid), up to 20
  by search.  Fixed sequences; no sequence was varied or optimised.  No side-chain torsion
  beyond the alanine methyl (fixed staggered) — peptides with rotatable side chains were not
  done.
* **Force fields** (files shipped with OpenMM 8.6.1): `amber14/protein.ff14SB.xml` (known part);
  `implicit/gbn2.xml` = `GBSAGBn2Force` (Amber `igb=8`, mbondi3 radii, `ε_in = 1`, `ε_out = 78.5`,
  no salt) with `sasaMethod=None` for the polarisation term alone and with the default ACE term
  for `g_GBSA`; `implicit/obc2.xml` (`igb=5`); `amber99sb.xml`, `amber19/protein.ff19SB.xml` (CMAP),
  `amber03.xml`, `amber14/protein.ff15ipq.xml`.  No cutoff, no constraints.  CHARMM36 was not
  used: its OpenMM file has no ACE/NME residue templates (terminal patches), and I did not
  build them.  ff19SB was parametrised for use with OPC water; its vacuum difference to ff14SB
  is used here only as an example of a CMAP-type correction.
* **Geometry** (`pepbuild.py`).  Internal-coordinate (NeRF) builder.  Bond lengths and bond
  angles are the ff14SB equilibrium values read from the OpenMM `System`; ω = 180°; methyl
  hydrogens staggered; the substituent offsets at Cα are solved from three equilibrium angles;
  peptide groups exactly planar.  The only degrees of freedom are `φ_k, ψ_k`.  Checked
  (`test_build.py`): bond-length error `10⁻¹⁵ Å`, torsion error `10⁻¹⁵` rad, chiral volume
  `+2.508 Å³` (L), bond energy 0 and angle energy `0.1052 kcal/mol` per residue *independent of
  the conformation* (28 of 72 angles are off equilibrium by up to 2.6° because a Z-matrix
  cannot satisfy all angles at a tetrahedral centre; they are constant).  Sign convention
  checked on the dipeptide map: vacuum minima at C5/β `(−150°, 150°)` and C7eq `(−75°, 75°)`,
  with GBn2 the minimum moves to PPII `(−75°, 150°)`, α_R at `+1.3 kcal/mol`.
  **Rigid geometry is a real limitation**: it makes 58 % of the dipeptide map a steric clash
  and overestimates strain; relaxed-geometry constants would differ.
* **Energies** (`fastff.py`).  OpenMM is the ground truth, but its `CustomGBForce` costs 1.2 ms
  per conformation, so I re-implemented *exactly* OpenMM's functional forms in numpy/numexpr
  (NonbondedForce without cutoff, PeriodicTorsionForce, the GBn2 and OBC2 expressions including
  the neck tables), reading **every parameter from the OpenMM System objects**.
  `validate_fast.py`: largest deviation from OpenMM's double-precision Reference platform over
  750 conformations of `n = 1, 2, 3, 5, 8`: `5·10⁻¹² kcal/mol` on every component.  The CMAP term
  of ff19SB is taken from OpenMM itself.  Every enumeration also spot-checks two conformations
  per 8 192 against OpenMM's CPU platform (largest deviation `1.3·10⁻⁴ kcal/mol`, its
  single-precision noise).
* **Grids** (`enumerate_grid.py`).  A3: φ ∈ {−150°, −70°, +60°}, ψ ∈ {−40°, +60°, +150°};
  A2: φ ∈ {−150°, −70°}, ψ ∈ {−40°, +150°}.  Chosen to sit in the basins (β, PPII, α_R, C7eq,
  α_L); they are not the minima of any force field.  Sizes: A3 `9ⁿ` up to 531 441 (`n = 6`),
  A2 `4ⁿ` up to 262 144 (`n = 9`).
* **Clashes.**  Score `s(x) = min r_pq/(R_p + R_q)` over atom pairs four or more bonds apart,
  `R` = Amber `R_min/2`.  Domain `X_τ = {s > 0.70}`.  Local states have scores 0.72–0.86 except
  `(60°, −40°)` (0.57, Lennard-Jones energy 86 kcal/mol), which is therefore excluded; non-local
  clashes (chain passing through itself, scores down to 0.04) appear from `n = 3`.  Clash-free
  fractions: A3 89, 79, 70, 59, 49, 41 % (`n = 1…6`); A2 100, 100, 98, 86, 77, 69, 61, 54, 48 %
  (`n = 1…9`).  **Without the filter the numbers are meaningless** from `n = 4` (overlapping
  atoms: `c_i(g_99) = 329 kcal/mol` from a fourth-decimal charge difference at `r → 0`).
  Sensitivity (`out/an1_constants.json` has every constant for `τ ∈ {0, 0.6, 0.7, 0.8}`): loosening
  the threshold to 0.60 leaves `max_i c_i(g_GB)` unchanged for `n ≤ 4` and raises it by 8–15 %
  beyond (A3 `n = 6`: 35.0 instead of 31.6; A2 `n = 9`: 21.8 instead of 19.0 kcal/mol);
  tightening to 0.80 removes the states φ = +60° and ψ = +60° of A3 altogether (they score
  0.72–0.73), so that A3 at 0.80 reproduces the A2 numbers exactly (3.69, 5.69, 7.87, 14.31,
  14.57, 15.99 for `n = 1…6`).  The difference between the two grids is therefore the presence
  of the C7eq-like and left-handed states.
* **Off-grid ensemble C** (`sample_continuous.py`).  Each residue's `(φ, ψ)` uniform on the
  clash-free 42 % of the dipeptide map (5° cells plus jitter), conformations with a non-local
  clash rejected (acceptance 95 % at `n = 2`, 54 % at `n = 8`).  It is *not* a Boltzmann ensemble;
  it is a broad sample of sterically possible conformations.  Sizes 2 000–16 000.
* **Temperature.**  300 K, `k_BT = 0.596161 kcal/mol`.

### 3.2 Scripts and outputs

| script | what | output |
|---|---|---|
| `test_build.py`, `validate_fast.py` | geometry and energy validation | stdout |
| `verify_openmm_direct.py` | end-to-end check without the fast evaluator and without the analysis library: `c_i(g_GB)` on the A3 tripeptide grid from OpenMM's own `CustomGBForce` and a brute-force loop; reproduces 16.09 12.41 18.63 16.43 15.14 11.19 and 508 clash-free conformations | stdout |
| `enumerate_grid.py n A3|A2` | exact enumeration | `data/grid_*.npz` (all energy components) |
| `sample_continuous.py ens|scan` | ensemble C; single-torsion scans | `data/cont_n*.npz`, `data/scan_n*.npz` |
| `an1_constants.py` | `c_i`, residue constants, four clash thresholds | `out/an1_constants.json`, `logs/an1_all.log` |
| `an2_second_order.py` | `c_ij`, row sums | `out/an2_second_order.json`, `logs/an2_big.log` |
| `an3_loworder.py` | low-order torsion fits (LS and Chebyshev LP) | `out/an3_loworder.json`, `logs/an3_*.log` |
| `an4_profile.py` | profile class on the grids | `out/an4_profile.json` |
| `an5_profile_transfer.py` | profile class off-grid, transfer, `η*(L)` | `out/an5_profile_transfer.json`, `logs/an5_*.log` |
| `an6_scaling.py` | scaling fits, extrapolated formulas | `out/an6_scaling_*.json` |
| `an7_sharpness.py` | sharpness, envelope validity, covers, Jensen gaps | `out/an7_*.json`, `logs/an7_*.log` |
| `an8_scans.py` | continuous oscillation and Lipschitz constants | `out/an8_scans.json` |
| `an9_torsion_refits.py` | circle constants of `g_99`, `g_19` | stdout |
| `an10_basins.py` | helix/β/PPII energies, `λ*` | `out/an10_basins.json` |
| `an11_manybody.py` | distance of `g_GB` to the exactly pair-additive class | `out/an11_manybody.json`, `logs/an11.log` |
| `long_chain_ci.py` | lower bounds on `c_i` for long chains | `out/long_ci_*.json`, `logs/long_*.log` |

The grid files (161 MB in `data/`, not under version control) can be regenerated with
`enumerate_grid.py`.  Total compute: about 40 CPU-minutes of enumeration (A3 `n = 6`: 15 min; A2 `n = 9`: 16 min, on
a machine with load 15–18) and about as much analysis.

### 3.3 Constants versus chain length and position (Statements 1, 3, 4)

Exact, clash-free, kcal/mol.  `max_i c_i` by `n`:

| residual | grid | `n=1` | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| `g_GB` | A3 | 8.96 | 14.02 | 18.63 | 22.90 | 27.48 | 31.62 | | | |
| `g_GB` | A2 | 3.69 | 5.69 | 9.09 | 14.31 | 14.57 | 15.99 | 17.69 | 18.35 | 19.04 |
| `g_GBSA` | A3 | 8.90 | 14.01 | 18.53 | 22.82 | 27.40 | 30.65 | | | |
| Coulomb + `g_GB` | A3 | 4.79 | 6.33 | 8.07 | 12.24 | 15.52 | 23.53 | | | |
| `g_solv` | A3 | 1.29 | 1.72 | 2.12 | 2.96 | 5.78 | | | | |
| `g_99` | A3, A2 | 0.64 | 0.64 | 0.64 | 0.64 | 0.64 | 0.64 | 0.64 | 0.64 | 0.64 |
| `g_19` | A3 | 2.59 | 2.59 | 2.59 | 2.59 | 2.59 | 2.59 | | | |
| `g_19` | A2 | 1.40 | 1.40 | 1.40 | 1.40 | 1.40 | 1.40 | 1.40 | 1.40 | 1.40 |
| `g_03` | A3 | 2.61 | 3.00 | 3.88 | 4.64 | 4.64 | 4.94 | | | |
| `g_03` | A2 | 0.99 | 1.11 | 1.50 | 1.74 | 1.99 | 1.98 | 2.06 | 2.18 | 2.32 |
| `g_ipq` | A3 | 2.81 | 3.35 | 4.24 | 5.00 | 5.00 | 6.11 | | | |
| `g_ipq` | A2 | 0.93 | 1.53 | 3.46 | 5.00 | 4.96 | 5.20 | 5.51 | 5.59 | 5.62 |
| known part `f` (for scale) | A3 | 24.8 | 29.7 | 33.3 | 35.7 | 42.3 | 45.1 | | | |

Position dependence of `c_i(g_GB)`.  A3, `n = 6`: φ sites 20.1, 27.4, 31.6, 27.2, 31.2, 19.8 and
ψ sites 17.5, 25.1, 29.3, 27.0, 26.2, 17.4 — both dome-shaped, the two torsions next to each end
about a third lower.  A2, `n = 9`: φ sites 8.1, 13.6, 16.2, 16.0, 13.3, 12.9, 12.9, 12.0, 9.6
(dome), but ψ sites 12.0, 11.7, 16.1, 15.8, 17.6, 16.8, 17.4, 18.6, 19.0 — increasing towards the
C-terminus, the largest constant of the chain being the *last* ψ, which moves only the
N-methylamide cap.  So "smallest at the ends" is true on A3 and for φ on A2, and false for ψ
on A2: a cap rotating against a preformed helix changes the polarisation energy as much as an
interior torsion does.  The distance to the nearer chain end is not the controlling variable.

*Longer chains, lower bounds* (`long_chain_ci.py`: 400 random conformations, then multi-start
coordinate ascent over the other torsions of the spread of `g` over the states of torsion
`i`; each value is attained by an explicit pair of clash-free conformations.  Validation
against the exact A3 `n = 5` constants: exact at 6 of 10 sites, within 20 % at the others.)

| chain | sites searched | largest lower bound | exact law extrapolated |
|---|---|---|---|
| A3, `n = 8` | 16 of 16 | 34.6 kcal/mol = 58 `k_BT` | `4.81 + 4.51 n` = 40.9 |
| A2, `n = 12` | 24 of 24 | 19.7 kcal/mol = 33 `k_BT` | exact at `n = 9`: 19.0 |
| A3, `n = 10` | 8 of 20 (6 starts) | 35.2 kcal/mol = 59 `k_BT` | 49.9 |
| A2, `n = 16` | 9 of 32 (6 starts) | 19.2 kcal/mol = 32 `k_BT` | — |
| A2, `n = 20` | 6 of 40 (6 starts) | 14.6 kcal/mol = 25 `k_BT` | — |

The searches at 10, 16 and 20 residues use few starts in spaces of `3²⁰`–`2⁴⁰` conformations and
find *less* than the exact values of shorter chains on the same grid (which are themselves
lower bounds for the longer chain only heuristically): they show that constants of 15–35
kcal/mol persist, and nothing about growth.

**What this says about the lever arm.**  (1) Constants grow with chain length in every
enumerated case; they are smallest at the chain ends on A3 but not for the ψ torsions on A2.  (2) On the three-state grid, which
contains the left-handed states needed for tight turns, the largest constant grows linearly up
to six residues and the eight-residue lower bound is compatible with the same line.  (3) On
the two-state grid (β, PPII, α_R only) the growth slows from four residues on, and nothing
measured excludes saturation near 20 kcal/mol.  (4) The *typical* single-flip change does not
grow at all.  A physical reading **[H]**: a single torsion changes the polarisation energy by
re-arranging the mutual desolvation of the two arms of the chain; if the arms can fold back
onto each other (turn states available) the number of affected groups grows with the arm, as
in the hairpin argument of theory report §11.14; if they cannot, the effect is local.  The
theory's `m^{3/2}` law (Theorem 11.36) concerns a different object — the *verified* constants
obtained from an RMSD-Lipschitz assumption through the chain rule — and is not tested here.

### 3.4 Approximation in linear classes (Statement 5)

*Torsion-variable models* (`an3_loworder.py`; A3, clash-free; LS = least squares on all
conformations, `η` = Chebyshev optimum by linear programming; kcal/mol):

| `g_GB` | `n = 3` (508 conf.) | | `n = 4` (3 844) | | `n = 5` (28 843) | |
|---|---|---|---|---|---|---|
| class | LS RMS | `η` | LS RMS | `η` | LS RMS | LS max |
| single torsions | 2.84 | 6.87 | 3.45 | 10.34 | 3.94 | 17.8 |
| residue tables | 1.76 | 4.39 | 2.25 | 7.24 | 2.63 | 16.2 |
| torsion pairs, window 3 | 1.39 | 3.20 | 1.80 | 5.22 | 2.13 | 14.7 |
| all torsion pairs | 1.37 | 2.99 | 1.78 | 5.03 | 2.10 | 13.4 |
| all residue pairs | 0.58 | 1.52 | 0.90 | 2.67 | 1.13 | 9.1 |
| residue triples, window 3 | — | — | 0.38 | 1.85 | 0.58 | 7.3 |

(The last rows have 200–2 000 parameters; at `n = 3, 4` they overfit — held-out RMS 0.7–1.5 —
and their `η` is optimistic.)  The remainder of every fixed-order class grows with `n`.  For
comparison at `n = 5`: `g_03` — single torsions 0.58 / 2.1, residue pairs 0.12 / 1.4;
Coulomb + `g_GB` — torsion pairs 0.73 / 10.1.

*Profile class, off-grid* (`an5_profile_transfer.py`; ensemble C; half for fitting, half held
out; least squares with a `10⁻⁹` ridge; 44 knots: 0.25 Å spacing to 6 Å, 0.5 Å to 12 Å, 2 Å to
40 Å; pairs three or more bonds apart; held-out RMS / max in kcal/mol):

| trained on | types (parameters) | `g_GB` | Coulomb (control) | `g_03` | `g_ipq` | `g_solv` |
|---|---|---|---|---|---|---|
| `n = 5`, 8 000 conf. | one (37) | 5.11 / 25.0 | 6.48 / 31.7 | 1.99 / 8.8 | 1.81 / 7.7 | 0.67 / 4.4 |
| | element pairs (321) | 0.56 / 3.45 | 0.88 / 6.5 | 0.41 / 2.7 | 0.41 / 2.4 | 0.19 / 1.6 |
| | Amber types (1 101) | 0.26 / 2.19 | 0.30 / 2.1 | 0.11 / 1.3 | 0.16 / 1.9 | 0.14 / 1.4 |
| `n = 8`, 8 000 conf. | element pairs (365) | 1.04 / 5.74 | 1.65 / 9.6 | 0.67 / 4.4 | 0.65 / 3.2 | 0.33 / 3.3 |
| | Amber types (1 268) | 0.43 / 3.94 | 0.74 / 4.5 | 0.20 / 2.5 | 0.26 / 2.0 | 0.22 / 3.0 |

Transfer with the constant refitted (Amber types, `g_GB`): trained at `n = 8` → `n = 3, 4, 5, 6`
of ensemble C: RMS 0.25, 0.29, 0.33, 0.36 (max 2.6–4.4); → 6 000 random clash-free conformations
of the A3 grid at `n = 5`: 0.49 / 3.0; → 6 000 of the A2 grid at `n = 8`: 0.57 / **8.8**.
Trained at `n = 5` → `n = 8`: RMS 4.8 — but the exactly pair-additive Coulomb control fails
the same way (8.4): distances beyond 22 Å were never seen in training; this is extrapolation
in the distance variable, not a many-body effect.  Three observations: (1) the remainder grows
with the chain (RMS 0.26 → 0.43 from five to eight residues); (2) on grid conformations, which include the most compact states of the chain, the maximum
(8.8) is more than twice that on held-out conformations of the broad ensemble (3.9); (3) the Coulomb control is no better than `g_GB`, so with
typed pairs the remainder is dominated by the typing and the piecewise-linear resolution.

*How far is `g_GB` from an exactly pair-additive function?* (`an11_manybody.py`.)  To remove the
typing from the question I built an explicit member of the class in which **every atom pair
has its own radial function**: `S(x) = Σ_{p<q} e_pair(r_pq; B̄_p, B̄_q) + w₀ + Σ_p w_p I_p(x)`, where
`e_pair` is the GB cross term with the Born radii frozen at their ensemble means, `I_p = Σ_q
H_pq(r_pq)` is the descreening sum of atom `p` (pair-additive by construction of the GB model)
and the `N + 1` weights are fitted by least squares on half of ensemble C.  `g_GB − S` is an
upper bound on the distance of `g_GB` to that class (kcal/mol, RMS / max, constant refitted):

| `n` | ensemble C held-out | A3 grid, all clash-free | A2 grid, all clash-free | frozen radii alone (RMS) |
|---|---|---|---|---|
| 2 | 0.10 / 0.9 | 0.14 / 0.5 | 0.08 / 0.2 | 2.1 |
| 3 | 0.21 / 2.6 | 0.27 / 1.0 | 0.22 / 1.0 | 3.4 |
| 4 | 0.30 / 4.1 | 0.39 / 2.3 | 0.31 / 2.3 | 4.4 |
| 5 | 0.34 / 3.5 | 0.48 / 4.8 | 0.37 / 4.1 | 5.2 |
| 6 | 0.43 / 5.4 | 0.56 / 8.8 (40 000 sampled) | 0.43 / 6.3 | 5.8 |
| 8 | 0.52 / 6.1 | — | 0.47 / 9.3 (all 35 478) | 7.2 |

So: (a) freezing the Born radii — the textbook "pairwise GB" — is useless here (RMS 5 kcal/mol
although the radii fluctuate by only 4 % on average, 11 % at most), because the cross terms of
bonded neighbours act as self-energies and respond to the radii at first order; (b) with the
first-order response included, `g_GB` is within 0.1–0.5 kcal/mol RMS of an exactly
pair-additive function, growing roughly linearly with the chain; (c) the supremum of the
remainder is 0.2–9 kcal/mol (up to `16 k_BT`) and grows faster than the RMS.  This is the cleanest
answer the pilot has to "is `βη` small compared with 1": **in RMS yes for these sizes
(`βη_RMS = 0.2–0.9`), in sup norm no from three residues on (`βη_sup = 2–16`).**

*Slope bound.*  The fitted radial functions have slopes up to `L_s = 0.6–0.9 kcal/mol/Å²`
(`L_r = 3.7–4.4 kcal/mol/Å`) for `g_GB`, at short range; for a `q_p·q_q/r` tail the slope in
`s = r²` decays like `r⁻³`.  A uniform bound `L` in `s` up to the largest distance
(`S_c ≈ 10³ Å²`, no cutoff exists for electrostatics) makes the dimensionless ratio `zLS_c/ε₁`
of Proposition 11.49 of order `10⁴–10⁵` for `ε₁ ∼ 0.1 kcal/mol` per atom: its bounds are vacuous
here, and a distance-dependent slope bound is necessary, as the engineering division
anticipated (ENG-RES-0003, revision 3).  `η*(L_s)` for a uniform bound is in Statement 5.

### 3.5 Sharpness, collective gaps, certificates (Statement 6)

Reference conformations on the A3 grids (`an10_basins.py`; kcal/mol above the respective
minimum):

| `n` | argmin `f` | argmin `E = f + g_GB` | helix (`f` / `E`) | all-β | all-PPII | `λ*(E)` | Gibbs weight of argmin `E` | conf. within 1 / 2 / 5 kcal/mol |
|---|---|---|---|---|---|---|---|---|
| 2 | β | PPII | 8.79 / 2.75 | 0 / 1.01 | 1.96 / 0 | 0.038 | 0.44 | 3 / 7 / 18 |
| 3 | β | PPII | 6.48 / 1.97 | 0 / 1.57 | 2.47 / 0 | 0.031 | 0.29 | 4 / 15 / 51 |
| 4 | β | PPII | 3.08 / 1.30 | 0 / 2.13 | 2.92 / 0 | 0.020 | 0.20 | 5 / 25 / 117 |
| 5 | helix | PPII | 0 / 0.46 | 0.89 / 2.69 | 4.23 / 0 | 0.0045 | 0.13 | 7 / 41 / 260 |
| 6 | helix | helix | 0 / 0 | 5.48 / 3.63 | 9.27 / 0.37 | 0.0026 | 0.14 | 7 / 38 / 512 |

`λ* = min_y (E(y) − E(x*))/d(x*, y)` with `d` the per-torsion envelope of `g_GB`: one evaluation
certifies iff `λ* ≥ 1`.  Clash-free single-flip neighbours exist at every site of the β and
PPII minimisers (`n ≤ 5`) and at 4 of 10 and 4 of 12 sites of the helix (minimiser of `f` at
`n = 5`, of both at `n = 6`); no site with a neighbour is sharp.
For the force-field differences at `n = 5` (minimum of `f`: helix): `λ*(f) = 0.275` (`g_99`),
0.043 (`g_19`), 0.029 (`g_03`), all attained by the all-β conformation, ten torsions and 0.89
kcal/mol away — and the minimiser does change: **ff99SB puts the all-β conformation 2.33
kcal/mol below the helix that ff14SB prefers**, although the two force fields differ by at
most 0.64 kcal/mol per residue.  A torsion refit that is exactly in the cheapest class and
"sharp" site by site still decides between two cooperative basins.

Covers (`an7_sharpness.py`): Statement 6(b).  Lower bounds are forced points, the volume bound
`Σ_y 1/M(y)` and the partition-function bound of Theorem 11.6(c) (the first is by far the
strongest: 3 042 against 915 and 204 at `n = 5`); upper bounds are greedy covers.  The covers of the force-field differences at `n = 5` are dense (a single centre covers up to
28 828 of the 28 843 conformations) and were computed by a greedy cover over a candidate pool.  A2, `n = 8`, `g_GB`
(35 478 conformations), `ε = 0`: between 4 061 (volume bound) and 8 041 (greedy).

Exact free-energy quantities on the grids, `g_GB`: `ln Z(f+g) − ln Z(f)` = 48.4, 58.9, 68.5
nats (`n = 3, 4, 5`), of which first-order perturbation `−β⟨g⟩_f` gives 46.3, 56.4, 66.2; Jensen
gap 2.1, 2.6, 2.3 nats; class bound 71, 117, 178 nats.

### 3.6 Certifiable constants for torsion refits (`an9_torsion_refits.py`)

`g_99(φ)` on a 1° scan of the dipeptide: range 1.1147 kcal/mol (`1.87 k_BT`), largest slope
1.55 kcal/mol/rad; independent of ψ to `3·10⁻⁷` and of the non-bonded model to `2·10⁻⁵`.
`g_19(φ, ψ)` on a 5° map: range 14.1 kcal/mol over the whole torus but 5.0 kcal/mol over its
clash-free 41 % (`c_φ = 3.7`, `c_ψ = 4.4`): CMAP corrections are large where the map is
sterically forbidden.  Both are explicit low-dimensional functions (a trigonometric
polynomial; a bicubic spline), so rigorous bounds over the continuous domain are elementary —
the one case in this report where an envelope constant of a real residual could be
*certified*, for every chain length.

---
## 4. Prior art, with a search log

Reading levels: `[full text]`, `[abstract]`, `[search snippet]`, `[from memory — unverified]`.
I searched PubMed (through the bio-research connector) on 2026-11-25 with the queries
"generalized Born pairwise decomposable protein design", "LUTE local unpruned tuple expansion
protein design", "Nguyen Roe Simmerling generalized Born neck model protein simulations 2013",
"ff14SB improving accuracy protein side chain backbone parameters ff99SB", "ff19SB
amino-acid-specific protein backbone parameters trained against quantum mechanics energy
surfaces", "residue-pairwise generalized Born scheme protein design Archontis Simonson", and
read the abstracts returned.  No other database was searched; I did not open any full text.
This is a thin search: enough to place the measurements, not enough to claim novelty.

*The models used.*
* Nguyen, Roe, Simmerling, "Improved Generalized Born Solvent Model Parameters for Protein
  Simulations", J. Chem. Theory Comput. 9 (2013) 2020–2034,
  [doi:10.1021/ct3010485](https://doi.org/10.1021/ct3010485) `[abstract]` — GB-Neck2, the
  model called GBn2 in OpenMM.
* Maier, Martinez, Kasavajhala, Wickstrom, Hauser, Simmerling, "ff14SB: Improving the Accuracy
  of Protein Side Chain and Backbone Parameters from ff99SB", J. Chem. Theory Comput. 11 (2015)
  3696–3713, [doi:10.1021/acs.jctc.5b00255](https://doi.org/10.1021/acs.jctc.5b00255)
  `[abstract]`.  The abstract says the backbone change is "a physically motivated adjustment
  to the φ rotational profile that compensates for lack of ff99SB QM training data in the
  β-ppII transition region" — which is exactly what Statement 3(a) measures: for alanine the
  difference is a function of φ alone (range 1.115 kcal/mol), and its largest effect on the
  A3 grid is on the β/PPII gap.  **[K]** for the nature of the change; the numbers are mine.
* Tian, Kasavajhala, Belfon, Raguette, Huang, Migues, Bickel, Wang, Pincay, Wu, Simmerling,
  "ff19SB: Amino-Acid-Specific Protein Backbone Parameters Trained against Quantum Mechanics
  Energy Surfaces in Solution", J. Chem. Theory Comput. 16 (2020) 528–552,
  [doi:10.1021/acs.jctc.9b00591](https://doi.org/10.1021/acs.jctc.9b00591) `[abstract]` —
  "coupled φ/ψ parameters" (CMAP), recommended with OPC water; Statement 3(b) is the
  class-theoretic reading of "coupled φ/ψ".
* ff99SB (Hornak et al. 2006), ff03 (Duan et al. 2003), ff15ipq (Debiec et al. 2016), OBC
  (Onufriev, Bashford, Case 2004), OpenMM (Eastman et al. 2017): `[from memory — unverified]`;
  I used the parameter files shipped with OpenMM 8.6.1 and did not check them against the
  papers.

*What is known about the non-pairwise character of GB.*
* Archontis, Simonson, "A residue-pairwise generalized Born scheme suitable for protein design
  calculations", J. Phys. Chem. B 109 (2005) 22667–22673,
  [doi:10.1021/jp055282+](https://doi.org/10.1021/jp055282+) `[abstract]`: the interaction
  energy of two residues "depends on the whole protein structure" but is "accurately fitted by
  a parabolic function" of the product of their residue Born radii, with coefficients that
  depend only on the pair.  This is the same mechanism as the surrogate of §3.4 (a low-order
  expansion in the Born radii makes GB pairwise); mine is first order, per atom, and is used
  only to *measure* the distance to the pair-additive class.  That GB is not pairwise and that
  an expansion in Born radii repairs most of it is therefore **[K]**; the sizes of the
  remainder for these peptides, and in particular their sup-norm values, are **[N]**.
* Gaillard, "Improved Physics-Based Single-Position Protein Sequence Redesign with a
  Residue-Pairwise Generalized Born Model", J. Phys. Chem. B 129 (2025) 10699–10710,
  [doi:10.1021/acs.jpcb.5c03662](https://doi.org/10.1021/acs.jpcb.5c03662) `[abstract]`:
  mentions "errors due to the pairwise decomposition of the solvation terms" and a
  "fluctuating dielectric boundary" approach "allowing an exact decomposition of the GB term".
  I cite it only as evidence that the pairwise approximation of GB is an active, known issue;
  its application (sequence redesign) is outside the scope of this programme and nothing of
  it is used here.
* Hallen, Jou, Donald, "LUTE (Local Unpruned Tuple Expansion): Accurate Continuously Flexible
  Protein Design with General Energy Functions and Rigid Rotamer-Like Efficiency", J. Comput.
  Biol. 24 (2017) 536–546, [doi:10.1089/cmb.2016.0136](https://doi.org/10.1089/cmb.2016.0136)
  `[abstract]`: represents "general, possibly nonpairwise energy functions to an arbitrary
  level of accuracy using a discrete energy matrix" by fitting low-order tuple expansions.
  This is the closest prior art to Statement 5(a) in *method* (least-squares expansions of a
  non-pairwise energy in discrete conformational variables), in a different setting (side
  chains on a fixed or locally flexible backbone, where the variables are rotamers).  I could
  not read which residuals they report; the comparison "tuple expansions are accurate in
  rotamer variables on a fixed backbone but not in backbone torsion variables" is my
  conjecture **[C]** from row 2 of the table in §2.B, not a documented fact.

*What I did not find and did not search for properly:* measurements of sup-norm
bounded-difference constants of a solvation term per torsion; the lever-arm growth of such
constants; certified (interval) bounds for GB energies over conformational cells.  Absence in
six PubMed queries means nothing.  The theory division's own prior-art files
(`docs/prior_art/L1…L8`) cover the mathematics; I did not re-read them.

---

## 5. What I did not settle

1. **Asymptotics of the constants.**  Six (three-state) or nine (two-state) residues exactly,
   local-search lower bounds beyond.  Linear growth, slower growth and saturation are all
   compatible with the two-state data; the three-state data are linear up to six residues.
   Whether a real (continuous, relaxed) chain behaves like the three-state grid — because it
   has turn conformations — is a physical argument, not a measurement.
2. **Upper bounds.**  Every constant in this report is a maximum over a finite set.  No
   constant for the continuous torsion space was bounded from above; the scans (Statement 8)
   only show that the continuous constants are not smaller.
3. **Rigid geometry.**  Relaxing bond angles (or minimising the hard degrees of freedom at
   each grid point) would change `f`, the clash-free domain and probably the constants; not
   done.  The helix becoming the minimum at five residues, and the 0.4–0.9 kcal/mol
   differences between helix, β and PPII, are properties of this rigid model.
4. **Side chains.**  Alanine only.  Fixed-backbone side-chain placement — the setting in which
   the known part *is* pairwise (row 2) — was not measured at all; the conjecture that `g_GB`
   has small `c_ij` in rotamer variables there is untested here.
5. **Explicit solvent, Poisson–Boltzmann, quantum chemistry, learned potentials** as residuals:
   not done.  GBn2 is itself a pairwise-descreening approximation of a dielectric-boundary
   problem; a Poisson–Boltzmann residual may be further from the pair-additive class.
6. **The best approximation in the profile class.**  I report least-squares and (for element
   types) Chebyshev fits on samples and one explicit pair-specific surrogate.  The true
   sup-norm distance of `g_GB` to the pair-additive class on a full domain is bracketed only
   from above (≤ 4.8 kcal/mol on the A3 pentapeptide grid, ≤ 9.3 on the A2 octapeptide grid);
   a lower bound would need a dual certificate (a signed measure on conformations annihilating
   all pair functions), which I did not compute.
7. **Certificate sizes in the span format on the real instance.**  The theory's alternative to
   the per-torsion format (Theorems 11.47–11.48 with a sup-norm remainder) was not run as a
   certificate; only its inputs (`η`, `L`, rank) were measured.
8. **Free energies.**  Only grid sums at 300 K; no continuous integral, no basin free energy.
9. **The domain.**  All sup-norm numbers depend on the clash threshold through the most
   compact conformations; I report one threshold (0.70) with a sensitivity check at 0.60.
10. The local-search lower bounds for 16 and 20 residues used few starts in a space of
    `2³²`–`2⁴⁰` conformations and are weak.

---

## 6. The three most promising next steps

1. **Measure the same constants where the theory's known part exists: fixed-backbone
   side-chain placement.**  Take a small folded peptide or mini-protein of fixed sequence
   and fixed backbone, a standard rotamer library, ff14SB pairwise tables as `f` and GBn2 as
   `g`; enumerate or sample; measure `c_i`, `c_ij`, sharpness and the cover.  There the site
   variables move only their own atoms, so no lever arm exists, the constants are bounded by
   the solvation of one side chain, and the row-sum condition of §11.7 has a chance.  This is
   the experiment that decides whether the second-order interface (Theorems 11.16–11.17) has
   a real instance.  (Fixed sequence, no design.)
2. **Replace "typed pair functions fitted on a sample" by a provable class for GB.**  The
   structure found in §3.4 — `g_GB = Σ_{p<q} e(r_pq) + Σ_p w_p I_p(x) + remainder`, with `I_p` an
   explicit pair sum and the remainder second order in the Born-radius fluctuations — suggests
   a class in which the *features are known* (`I_p` and the frozen-radius pair terms are
   computable, not fitted) and only a remainder with an *analytic* bound is uncertain:
   `|remainder| ≤ ½ Σ_p K_p (δ(1/B_p))²` with `K_p` from the explicit second derivatives of the
   GB formula.  An interval-arithmetic bound on that remainder over a conformational cell would
   be the first certified envelope for a real many-body term.
3. **Collective sharpness.**  The measured landscapes are decided by cooperative basins
   (helix, β, PPII within 0.4–2.7 kcal/mol; single-site excitations excluded in the helix).
   The right resolution statement for chains is therefore Theorem 11.39 (droplets), not
   site-wise sharpness.  Measure, for the real `f` and each residual, the droplet ratio `λ*`
   as a function of chain length and compare with a transfer-matrix (helix–coil-type) model
   whose parameters are fitted to the grid energies; this would turn "the minimiser is not
   model-robust" into a quantitative statement about which basins a given model uncertainty
   can and cannot order.

---

## 7. Requests

### To the theory division

**T-1 (envelopes with a domain).**  All measured constants are suprema over a domain, and
they are dominated by its most compact and most extended members.  The theorems are stated
for a fixed `X`.  Please state the monotonicity explicitly — if `X′ ⊂ X` then `c_i(X′) ≤ c_i(X)`
and a certificate over `X′` plus a certified exclusion of `X ∖ X′` (by the known part alone)
is a certificate over `X` — and say what the exclusion step costs when it must itself use the
envelope (`E ≥ f − (residual range)`).  Measured input: on the pentapeptide grid the range of
`g_GB` is 55.6 kcal/mol and that of `f` 118 kcal/mol; a window of 20 kcal/mol in `f` contains
5 378 of the 28 843 conformations and on it `max_i c_i(g_GB)` is 14.6 instead of 27.5 kcal/mol; a
window of 5 kcal/mol contains 52 conformations, on which `g_GB` varies by 6.0 kcal/mol in all.

**T-2 (a class with known features and a quadratic remainder).**  Is there a version of
Theorem 11.47(d) for `g = θ⁰·F + ρ` where `F` is known, `θ⁰` is *known* (not in a box), and
`|ρ(x)| ≤ Σ_p K_p u_p(x)²` with known nonnegative functions `u_p` (here: the deviation of the
inverse Born radius from its reference)?  Then the uncertainty at `x` is a computable function
of `x`, not a constant `η`, and it vanishes at the reference state.  What is the certificate
cost?  (This is the form the GB residual actually has, §3.4.)

**T-3 (sup norm versus typical error).**  The measured residual is within `0.4 k_BT` RMS of the
profile class and `4–15 k_BT` in sup norm, and its exact Jensen gap is 2.3 nats where the
first-order class allows 178.  Is there a theorem in which the remainder is bounded in
`L²(π_f)` or in an exponential moment under the Gibbs measure of the known part, for `ln Z`
(not for the minimum)?  By the Gibbs variational principle `|ln Z(f+g) − ln Z(f+ĝ)| ≤
ln E_π e^{β|g−ĝ|}`; with a certified exponential-moment bound instead of a sup bound the
accuracy floor would be the *typical* remainder.  What must be certified, and can it be
estimated by sampling with a guarantee?

**T-4 (droplet criterion for long-range known parts).**  Theorem 11.39 is for
nearest-neighbour chains.  The real known part has `c_ij(f)` decaying slowly (12 kcal/mol at
separation seven).  Is `λ* = min_y gap(y)/d(x̂, y)` still the exact criterion (it is, by Theorem
11.7), and is there a transfer-matrix-like bound for it under a decay assumption on the
couplings?

### To the engineering division

**E-1 (specification: constants of a solvation residual in rotamer variables on a fixed
backbone).**
*Motivation.*  §6 item 1: the one setting in which the theory's known part is exact.
*Formulation.*  Fixed sequence and fixed backbone coordinates of a small public structure
(any capped peptide of 10–20 residues with side chains; sequence taken as is); rotamers from a
public library, 3–9 per residue; `f` = ff14SB intra- and inter-residue energies (pairwise
tables); `g` = GBn2 polarisation energy of the whole molecule (OpenMM `implicit/gbn2.xml`,
`sasaMethod=None`); domain = clash-free assignments (threshold 0.70 on `r/(R_p+R_q)`).
*Inputs.*  `pepbuild.py` and `fastff.py` of this workstream can be extended (side-chain
Z-matrices); `fastff.py` reproduces OpenMM to `5·10⁻¹²` kcal/mol.
*Outputs.*  `c_i`, `c_ij` (matrix and row sums), single-site excitation energies of `f` at its
minimiser, number of sharp sites, `λ*`, smallest cover brackets for `ε ∈ {0, k_BT, 2 kcal/mol}`,
low-order fit remainders (RMS and Chebyshev), all with units.
*Validation.*  Reproduce the alanine numbers of this report first (e.g. A3, `n = 4`:
`c = 17.27 13.35 22.88 20.05 22.90 20.49 16.29 12.77`; cover at `ε = 0` in [447, 782]).
*Stopping conditions.*  Stop if the row-sum condition fails at every site by more than a
factor 3 at 8 residues (then the second-order interface has no instance here either), or as
soon as one instance satisfies it (then certify that instance end to end).
*Resources.*  `10⁵–10⁶` conformations × 1 ms: CPU-minutes to an hour; covers by integer
programming as in ENG-RES-0002.

**E-2 (extend THY-REQ-0003 with the real residual).**  Your accepted design asks "which class"
for synthetic and learned residuals on lattice chains.  The data of this workstream
(`data/grid_*.npz`: every energy component for up to 531 441 conformations, with states and
clash scores) can be dropped into the same pipeline as a fourth case, "a real implicit-solvent
term off-lattice".  Two things your design should take from the pilot: (a) a sup-norm
remainder fitted on a sample is not a bound — the unconstrained Chebyshev fit had held-out
maximum 10.2 kcal/mol at training `η = 1.06`, and on exhaustively enumerated grids the
maximum remainder of the explicit pair-additive surrogate was 1.4–1.5 times that on a random
held-out sample of the same chain length (4.8 against 3.5, 9.3 against 6.1 kcal/mol); report
maxima over *enumerated* domains only; (b) one pair type is useless for electrostatics — the type set must at least
separate the signs of the partial charges (Amber types: 36 pairs), and the slope bound must
depend on distance.

**E-3 (exact covers for the real instances).**  The cover brackets of Statement 6(b) come
from forced points and a greedy heuristic.  Your integer-programming cover code with certified
dual bounds (ENG-RES-0002) would close them: the inputs are `data/grid_*.npz` (energies, clash
scores) and the constants in `out/an7_*.json`; the largest instance has 28 843 points with mean
set size 35 (sparse).  Expected outcome: the exact
certificate size of a real solvation residual in the per-torsion format for 3, 4, 5 residues.
