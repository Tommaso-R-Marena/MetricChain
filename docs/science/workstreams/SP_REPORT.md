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
bounded-difference) class in any useful sense**: its exact constants are `c_i = 9–32 kcal/mol
= 15–53 k_BT`, they grow with chain length (largest constant `≈ 4.8 + 4.5·n` kcal/mol for
`n = 1…6` residues on the three-state grid) and are lower at the chain ends than in the interior
— the predicted lever-arm effect is present, though as "growth with length plus an end effect",
not as a clean power law in the distance to the chain end; no torsion is sharp in the
extended basins (`e_i/c_i = 0.03–0.47`); the mixed second differences are dense and as large as
the first-order constants (`c_ij` up to 23 kcal/mol at four residues, half row sums 37–60
kcal/mol); and on the real instance a certificate of the global minimum in the per-torsion
format needs between 3 042 and 5 357 of the 28 843 clash-free conformations at five residues
(447–782 of 3 844 at four, 94–139 of 508 at three): it grows almost as fast as the domain.
The theory's formulas with these numbers give an uncertifiable free-energy width of 43–48
nats per residue and certificates of at least `10⁵` (10 residues) and `10⁵⁶` (100 residues)
evaluations.  **The same residual is close, in root-mean-square but not in supremum norm, to
the class the theory identifies as cheap** — pair-additive with unknown radial functions
("profile class", theory report §11.17) — *provided* the pairs are typed by Amber atom type
(36 pair types): on off-grid conformations of the pentapeptide the held-out remainder is
`0.26 kcal/mol = 0.43 k_BT` RMS and `2.2 kcal/mol = 3.7 k_BT` in the maximum, with fitted
slopes `≤ 0.9 kcal/mol/Å²`; with one pair type the class is useless (remainder = the whole
variance), and low-order expansions in the *torsion* variables are poor (best pairwise-in-torsions
fit: RMS 2.1, max 13 kcal/mol at five residues).  **Differences between force fields of one
lineage lie exactly in the cheapest classes**: ff99SB − ff14SB is a sum of single-torsion terms
(`c_i = 0.64 kcal/mol` on φ, 0 on ψ, independent of length, all `c_ij = 0`; every site sharp,
one evaluation certifies), ff19SB − ff14SB is a sum of one table per residue (`c_i ≤ 2.6
kcal/mol`, `c_ij = 0` beyond the residue); a change of charge model (ff03, ff15ipq) gives
`βc_i ≈ 2–10`, slowly growing, half of the sites sharp, certificates of about ten evaluations
at four residues.  So the answer to "which class do residuals live in" is: *model-to-model
corrections inside one functional form — additive or residue-local; a continuum-solvent term —
linear in typed pair-distance features up to a few `k_BT` in sup norm, and nowhere near a
per-torsion envelope with `βc ∼ 1`.*  The pilot is small (alanine only, ≤ 6 residues exact,
rigid bond geometry, a grid of basins), all sup-norm numbers are properties of these finite
domains, and nothing here certifies a constant for a continuous conformation space.

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
and 0.36 (A2) and fits worse.  Within one chain the constants are lower for the two torsions
next to each end and flat in the interior (A3, `n = 6`, by `m`: 18.7, 18.7, 26.8, 28.2, 29.3,
28.2).  The root-mean-square change under a single-torsion flip does **not** grow (6.4–6.5
kcal/mol on A3, 3.6–3.7 on A2): the growth is in the extreme pairs, i.e. in what a sup-norm
envelope must cover.  Lower bounds by local search for longer chains are in §3.3.

*Reading.*  The lever-arm prediction of theory report §11.14 ("for contact-type residuals every
envelope in torsion-Hamming format has `c_i ≥ u₀⌊(m_i − 1)/2⌋`") is qualitatively confirmed for
a real residual — constants grow with the length of the chain and are smallest at its ends —
and quantitatively the scale is `u₀ ≈ 2–5 kcal/mol` per residue, i.e. `β u₀ ≈ 4–8`.  The
regime `u = βc ∼ 1` in which the theory report evaluates its exponents (e.g. `0.029` at
`u = 1`, Theorem 11.25) is one to two orders of magnitude away from this residual.

**Statement 2 [N, exact] (second-order constants).**  For `g_GB` on A3 the matrix `c_ij` is
dense, with entries of the size of the first-order constants and slow decay in `|i − j|`: at
`n = 4`, by separation `|i − j| = 1…7`, the largest entries are 23.1, 22.4, 18.9, 12.2, 11.9,
7.2, 7.0 kcal/mol; half row sums `½Σ_j c_ij` are 37–60 kcal/mol; the Dobrushin-type row sums
`Σ_j tanh(βc_ij/4)` are ≈ 7 (Theorem 11.33(a) needs `< 1`).  The row-sum condition of theory
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
separated by three or more bonds, no cutoff — fitted on 8 000 **off-grid** conformations of
the pentapeptide (ensemble C, §3.1) and tested on 8 000 others (standard deviation 5.47):

| pair types | parameters | held-out RMS | held-out max | largest fitted slope `L_s` |
|---|---|---|---|---|
| one type | 37 | 5.11 | 25.0 | 0.12 kcal/mol/Å² |
| element pairs (10 types) | 321 | 0.56 | 3.45 | 0.72 |
| Amber atom-type pairs (36 types) | 1 101 | **0.26** | **2.19** | 0.89 |

The same radial functions, with only the constant refitted, describe the tri- and
tetrapeptide (RMS 0.19, 0.22) and the A3 grids (`n = 5`: RMS 0.32, max 3.5).  Control: the
vacuum Coulomb energy — exactly pair-additive, but with pair-specific coefficients — has the
same remainder in this class (0.30 / 2.1), so at this resolution `g_GB` is as close to the
*typed* class as an exactly pair-additive function is.  A sup-norm fit with a slope bound
`|φ′| ≤ L_s` (linear programme, element types, 2 500 training conformations) has training
remainder `η*(L_s) = 1.06, 1.06, 1.48, 4.0, 8.7` kcal/mol at `L_s = ∞, 1, 0.3, 0.1, 0.03`
kcal/mol/Å², and held-out maxima of 6–21: **a sup-norm remainder estimated on a sample is not a
bound** (the unconstrained Chebyshev fit has held-out maximum 10.2 at training `η = 1.06`).
So `βη_RMS ≈ 0.4`, `βη_sup ≈ 4` at five residues, with `≈ 10³` coefficients.

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
helix minimises both, and most single flips out of it are sterically excluded in the rigid
geometry, so "sharpness of a site" is not the right notion there (see §3.5).
(b) Smallest certificates of `min E` in the per-torsion format (set cover with radii
`gap(y) + ε`, Theorem 11.4 [V]); lower bound = number of conformations that only themselves
cover (Theorem 11.6(a) [V]), upper bound = greedy cover:

| residual, `n` | conformations | `ε = 0` | `ε = k_BT` | `ε = 2` kcal/mol |
|---|---|---|---|---|
| `g_GB`, 3 | 508 | [94, 139] | [85, 130] | [61, 112] |
| `g_GB`, 4 | 3 844 | [447, 782] | [378, 717] | [261, 609] |
| `g_GB`, 5 | 28 843 | [3 042, 5 357] | PENDING5a | PENDING5b |
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
off-grid conformations of ensemble C (10° scans; maxima over 150–200 sampled bases, hence lower
bounds on the suprema): `g_GB` oscillates by up to 13–16 kcal/mol at `n = 2` and 14–24 at
`n = 5` (median 6.4–6.7); its torsion-space Lipschitz constants reach 9–21 kcal/mol/rad
(median 4.3).  With these `L_i` the threshold of Theorem 11.34 for the torus,
`J = Σ_i ln(sinh b_i/b_i)`, `b_i = βL_iπ/2`, is 85 nats at `n = 2` and 295 nats at `n = 5`.
For `g_03`: oscillation ≤ 5.5 kcal/mol, `L_i ≤ 5.9 kcal/mol/rad`.

**Statement 9 [P] (what the measured numbers do and do not license).**  (i) Every number in
Statements 1–6 is an exact property of a finite domain (a grid with a clash filter) and of the
OpenMM implementation of the force field; it is a *lower bound* for the corresponding constant
of any superset of that domain, in particular of the continuous torsion space, and no upper
bound for it.  (ii) A certified envelope constant for the continuous space needs an upper
bound, i.e. interval arithmetic or a Lipschitz bound of `g` over torsion voxels; the sampled
Lipschitz constants of Statement 8 show that such a bound cannot be below
`≈ 20 kcal/mol/rad` for the pentapeptide.  (iii) Because the constants are maxima, they are
controlled by the most compact and the most extended conformations of the domain; restricting
the domain (an energy window around the minimum, a single basin) lowers them — the kernels
allow this (dead-end elimination shrinks the domain before the residual is touched) and the
pilot did not explore it.

---
## 2.B The physical reading of the mathematics

One row per mathematical object.  "Pilot" refers to the measurements of §§2–3.

| # | mathematical object | physical counterpart | the identification is valid when | what is lost | what must be measured or certified to use it |
|---|---|---|---|---|---|
| 1 | finite configuration space `X = ∏ D_i` (sites × states; theory report §1) | a discretised conformation space: rotamers of side chains on a fixed backbone; torsion wells (rotational-isomeric-state models); voxels of torsion space; lattice walks | every state is a cell of the continuous space on which the energy can be *enclosed* (`voxel_boltzmann_bounds` [V] needs `E_lo ≤ E ≤ E_hi` on the cell and its measure), the cells are products over sites (`certified_torsion_partition` [V]), and bond lengths/angles are either rigid or integrated out into the known part | vibrational entropy and relaxation inside a cell; bond-angle flexibility (a rigid-geometry map forbids 59 % of the `(φ,ψ)` plane of the dipeptide and puts α_L 6–10 kcal/mol too high); the Jacobian of rigid constraints; kinetics | interval enclosures of every energy term over every cell — these widen with the lever arm (cell width × arm length); pilot: along one torsion `g_GB` changes by up to 20 kcal/mol/rad, so a cell must be ≲ 2° wide for `k_BT` resolution of the residual alone; the excluded (clash) cells; the product structure — pilot: only 41 % of the A3 grid of the hexapeptide is clash-free, the domain is not a product |
| 2 | known part `f = Σ h_i(x_i) + Σ J_ij(x_i, x_j)` | a molecular-mechanics energy.  It is pairwise in *atoms*; it is pairwise in the *site variables* exactly when each atom's position depends on one site: fixed-backbone side-chain placement (every side-chain atom depends on its own rotamer), rigid-body pose tables, lattice or contact models written in bead positions | fixed backbone (or a finite set of backbones treated as one extra site); force field without many-body terms; then `h_i`, `J_ij` are sums of atom–atom terms and exact | for a flexible backbone nothing is pairwise in torsions: the distance of two atoms depends on every torsion between them.  Pilot: the vacuum ff14SB energy of the tetrapeptide has `c_ij(f)` up to 25 kcal/mol, and its best pairwise-in-torsions approximation leaves RMS 2.1 and sup-optimal 6.1 kcal/mol — the "known part" of the theory does not exist in backbone torsion variables | rational tables with outward rounding (straightforward at rotamer *points*); over voxels, interval evaluation of Lennard-Jones and Coulomb terms; a statement of which terms were moved into the residual |
| 3 | residual `g = E − f` | continuum-solvent polarisation (GB, PB: many-body through the dielectric boundary); explicit polarisation; quantum-chemical minus force-field energy; a learned correction; backbone-relaxation energy; the difference of two force fields | the split is a *choice*: `g` should be the part that is expensive, non-decomposable, or uncertain | the theory treats `g` as a black box known through class membership and point evaluations; all structure of the functional form (pair-additivity in atoms, locality in space, the anticorrelation of polarisation with Coulomb energy — pilot: `c_i(Coulomb + GB)` is half of `c_i(GB)`) is lost unless it is put into the class | which class, with which constants (this report: Statements 1–5); the split itself can be optimised (screened Coulomb in `f`) |
| 4 | envelope `d` / class: bounded differences `c_i`; torsion-space Lipschitz constants; mixed differences `c_ij`; profile slope `L` | an a-priori worst-case bound on how much the correction can change when one degree of freedom changes — a *sup-norm* error bar | the bound holds for **all** pairs of configurations of the domain | typicality and correlation: force-field accuracy is quoted as RMS error; pilot: sup/RMS is 4.2 for single flips of `g_GB` at five residues (27.5 against 6.5 kcal/mol) and 8.4 for the profile remainder (2.19 against 0.26); the exact Jensen gap is 2.3 nats where the class allows 178 | an *upper* bound: interval arithmetic over the domain or a proved Lipschitz property of the functional form, plus (for Corollary 4.7) inertia bounds.  None exists for a production force field.  For torsion-refit differences the bound is elementary: `g_99` is a trigonometric polynomial of φ with range 1.115 kcal/mol on the whole circle (§3.6) |
| 5 | anchors `(a, g(a))` | single-point evaluations of the expensive model at chosen conformations: a GB/PB solve, a quantum-chemical single point, an inference of a learned potential.  No experiment measures `g` at a chosen conformation | the evaluation is exact at exactly that configuration (or comes with an interval: the kernels accept interval anchors) | convergence and discretisation error of the expensive calculation; for voxels a point value is not an enclosure | the number of evaluations is the theory's cost; the search over `f` (NP-hard, theory report §8) is not counted |
| 6 | `min E` | the global minimum-energy conformation of the *model* on the discretised space | it predicts a structure only if (a) the Gibbs weight of its basin dominates and (b) the model error is below the gap to competing basins — which is the theory's own sharpness condition (Theorems 2.4, 11.7 [V]) | pilot: for the pentapeptide the helix is the minimum in vacuum and PPII with GBn2, 0.46 kcal/mol apart; the uncertainty constants are 17–27 kcal/mol for the solvent term and 3–5 kcal/mol between charge models: the minimiser is not a model-robust object for a flexible peptide | the gaps of the known part against the constants, site by site or droplet by droplet (Theorem 11.39) |
| 7 | `ln Z_β` | conformational free energies | **observable**: differences between macrostates of one model (populations of basins; binding constants as ratios of partition functions) and between thermodynamic states (temperature, and gas phase → solvent: if `f` is the gas-phase energy and `g` a solvation potential of mean force, `ln Z(f+g) − ln Z(f)` is `−β` times a hydration free energy).  **Not observable**: the absolute `ln Z` of a discretised model (depends on cell volumes and the energy zero), and `ln Z(f+g) − ln Z(f)` when `g` is a model correction (force field → better force field): a model-to-model free energy | in differences, correlated errors cancel physically, but not in a first-order class ("the sum of the two thresholds, no cancellation", theory report §11.13) | the accuracy that matters is ≈ 1 kcal/mol = 1.7 `k_BT` on differences; the class threshold measured here is 43–48 nats per residue |
| 8 | inverse temperature `β`; the scale `u = βc` | at 300 K, `1 kcal/mol = 1.68 k_BT` | — | the theory report tabulates exponents at `u = 0.5–2.8`, i.e. `c = 0.3–1.7 kcal/mol` | pilot: `βc_i = 15–53` for the solvent term (the theory's zero-temperature regime: `ln cosh(u/2) ≈ u/2 − ln 2`), `2–10` between charge models, `1.1–4.3` between force fields of one lineage |
| 9 | the hint (an instance handed to an algorithm that must still be correct on the class; §11.10) | a surrogate of the residual: a cheaper solvent model, a fitted pair-additive approximation, a learned potential, or the output of a heuristic search, which expensive evaluations then spot-check | the surrogate is free and correctness is demanded on the class, not on the surrogate | — | pilot: a fitted typed pair model predicts `g_GB` to 0.26 kcal/mol RMS (max 2.2) — a good hint; the theory's price for checking it is set by the class, not by the quality of the hint |
| 10 | product landscapes (additive `f`, independent sites); the cube | independent degrees of freedom: side chains that do not interact (far apart on a fixed backbone), independent rotors on a stiff scaffold, independent two-state titration or tautomer sites (the cube), the reference system of a mean-field theory | couplings small against site gaps (a Dobrushin-type condition) | cooperativity, excluded volume, phase transitions.  Pilot: a peptide backbone is not product-like — in the helix basin of the hexapeptide 11 of 12 single-torsion excitations are sterically excluded or cost 8–20 kcal/mol, while the collective excitation to PPII costs only a few kcal/mol in total | the exponents `R*`, `R_β` are properties of this idealisation; for a chain the relevant theorems are 11.39–11.40 (droplets) and the general Theorem 11.6 |
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
site by site, whether the minimiser can change.  On the A3 grids every site is sharp for
`n ≤ 4` (`c = 0.64` against gaps `≥ 0.68`), by a margin of 0.04 kcal/mol at the tightest site:
a true but fragile certificate.  *(c) Conformer ranking of a small molecule with an expensive
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
for a same-lineage torsion refit all are.  In the helix basin single-site sharpness is
vacuous and the relevant quantity is collective (§3.5).

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
| (A2) typed pair-additivity in atoms | (trivially) | (no: a torsion term) | yes to RMS 0.11, max 1.3 (36 types, `n = 5`) | in RMS yes (0.26), in sup norm to 2–6 kcal/mol; the remainder grows with the chain (§3.4) |
| (A3) locality along the chain | yes | yes | no (`c_ij` decays to 0.7 kcal/mol but not to zero) | no (`c_ij = 7` kcal/mol at separation 7) |
| weak coupling, `Σ_j tanh(βc_ij/4) < 1` | 0 | 0.78 | 4.1 | 7.0 |

So the real solvent residual leaves the first-order world only through (A2), and there the
theory's replacement guarantee carries an accuracy floor of at least `2η_sup ≈ 4–12 kcal/mol`
at five residues (Theorem 13 of the theory division's workstream P: `η(1 + ‖λ‖₁)`), far above
`k_BT`.  The statement "GB is close to pair-additive" is true in the sense in which force
fields are judged (RMS) and false in the sense in which certificates need it (sup norm, with
a *proved* bound).

---
