# Workstream P2 (science division) — class constants of a real residual in rotamer variables on a fixed backbone

> **Coordinator's note added 2026-11-26 (workstream P4; linked correction SCI-REV-0012 §5).**  Statement 5 is
> "all on `X′`".  For the instances whose clash-free domain `X_τ` is not a product (Phe, Lys, LKSE) workstream
> P4 found — and the coordinator recomputed for Phe₄…Phe₈ on the strand — that in 14 of 40 analyses the
> minimum of the energy over `X_τ` is **not in `X′`** (Phe on the strand: 1.9–13.3 kcal/mol lower).  "One star
> is an exact certificate for poly-Phe on the strand" (Statement 5(b)) and "exact in all but three poly-Lys
> instances" (5(c)) are statements about `X′`; Statement 9(iii) says so in general terms but the report does
> not say where the minimum is.  With the minimiser of `X_τ` as reference and the largest reset-closed
> domain around it the star certifies 13 of the 40 and the third-order pair model 30 of 34
> (`P4_REPORT.md` §2.5).  Val, Leu and Ser instances (`X = X_τ = X′`) are unaffected; no number below changes.


Report of an independent workstream of the Scientific Discovery, Translation & Independent
Validation Division (second wave; continues workstream P, `SP_REPORT.md`).  Branch
`research/scientific-translation`.  All scripts, logs and outputs:
`experiments/science/ws_P2/` (running notes: `NOTES.md`).  Written 2026-11-25.

Epistemic labels as in `COMMON.md`: **[V]** machine-checked by the theory division (I cite the
Lean name as given in the theory report at `5ed4072`; I did not re-run Lean), **[P]** paper
argument given here, **[K]** known and cited (with reading level), **[N]** numerical evidence,
**[C]** conjecture, **[H]** heuristic/physical argument, and **[M]** = *measured on the named
model with the stated protocol* (exact enumeration unless a number is explicitly called a lower
bound).  Units: kcal/mol; `k_BT = 0.596161 kcal/mol` at 300 K; free energies in nats.

**What kind of numbers these are.**  Every constant below is an exact maximum over an
*enumerated finite set of rotamer assignments of a rigid synthetic model peptide* (or, where
stated, a rigorous lower bound obtained from evaluated pairs of assignments).  It is a lower
bound for the same constant of any larger domain (finer rotamer grids, continuous χ, relaxed
geometry) and an upper bound for nothing.  No sequence was varied, compared or optimised for a
property; sequences, backbones, grid and thresholds were fixed before any constant was computed
(`NOTES.md`, Step 2; two amendments forced by geometry are recorded there and in §3.1).

---

## 1. Verdicts in one paragraph

On a fixed backbone with one site per residue and the rotamer as site variable, the theory's
known part **exists exactly** for a real force field: the ff14SB vacuum energy is a sum of
one-site and two-site tables to `2·10⁻¹²` kcal/mol in all 217 non-empty instance analyses (it
is *not* pairwise with one site per χ angle: third-order mixed differences of 4–6 kcal/mol).
For the real residual of the brief — the GBn2 polarisation energy `g_GB` — **the second-order interface
(star + the exact criterion of Theorem 11.17) has real instances, but only the easy ones**: one
star of `1 + Σ(k_i − 1)` evaluations is an exact certificate of the minimum for the apolar
homopolymers (poly-Val on the strand and on PPII at every enumerated length up to 12: 25
evaluations of 531 441 assignments; poly-Leu on helix, strand and PPII at every enumerated
length up to 16: 17 of 65 536, of which the PPII instances are ones where the first-order one-evaluation criterion fails, `λ* = 0.45`;
poly-Phe on the strand), with free-energy brackets of `10⁻³–0.2` nats — and **it fails for every
polar or charged instance beyond two residues**: for poly-Ser the half row sums `½Σ_j c_ij` are
3.5–4.9 kcal/mol against single-site excitation energies of 0.13–1.0 (a factor 4–40), and the
accuracy one star certifies degrades by about 3–6 kcal/mol per residue (1.7 → 10.6 kcal/mol on
the strand, `n = 3 → 6`); for poly-Lys the row sums are 17–41 kcal/mol (lower bounds 49–68 at
12–16 residues: a factor 20 in the median, up to 160) and the star is off by 10–204 kcal/mol;
for the heteropolymer (LKSE)ₘ by 13–170.  **The reason is not that the solvent term is
many-body.**  In rotamer variables `g_GB` is pairwise up to third-order constants `c_ijk` of
0.003–0.2 kcal/mol for the neutral peptides (best two-site fit: RMS `2·10⁻⁴–5·10⁻²`, maximum `2·10⁻³–0.2` kcal/mol over up
to 531 441 assignments — against RMS 2.1 / max 13 for torsion pairs in P's variables); for
the charged ones the typical remainder is as small (RMS ≤ 0.12) but `c_ijk` reaches 0.1–2.4
kcal/mol at P's clash threshold and 10 kcal/mol at the relaxed one (three lysines on PPII).
What defeats the star is the size of the *pair* part: direct solvent-screening cross terms between polar and charged side chains
(`c_ij` up to 3.0 for Ser–Ser, 18–51 for Lys–Lys, 78 for Lys–Glu), which are pairwise by
construction and nearly cancel the vacuum Coulomb term of the known part, plus a
Born-radius-mediated pair coupling of 0.35–2.4 kcal/mol for the neutral peptides (6 and more
for Lys).  Consequently **the interface of the theory that has a real instance for the
solvent term is the third-order one** (Theorem 11.18 with `m = 3`: `g_GB` on the Hamming ball of radius 2, i.e.
`1 + Σ(k_i−1) + Σ_{i<j}(k_i−1)(k_j−1)` evaluations): it is an exact certificate of the minimum in
every enumerated instance of three to eight sites at P's clash threshold (e.g. 1 009 evaluations of 531 441 for Ser₆,
2 481 of 194 481 for Lys₄) with free-energy brackets of `10⁻³–0.2` nats; at the relaxed
threshold it is exact in all but three poly-Lys instances, where it is off by 0.14, 0.19 and —
for Lys₄ on PPII — 6.7 kcal/mol.  **P's prediction that the first-order constants do not grow with chain length is confirmed for neutral side chains**
(max `c_i`: Val 0.44–0.84, Leu 0.96–1.56, Phe 1.6–4.5, Ser 5.0–5.3 / 7.7–8.0 / 9.4–10 kcal/mol
on strand / PPII / helix; no growth between 6–12 residues and the lower bounds at 24–32) **and
refuted for charged ones**: for poly-Lys `max c_i = 10, 37, 52, 56` kcal/mol at `n = 1…4`
(exact) and `≥ 85, 110, 124, 138` at `n = 8, 12, 16, 24` — the unscreened long-range
charge–charge term that the split "vacuum force field + GB" puts into the residual.  A
force-field difference with another charge model (ff03 − ff14SB) is *exactly* in the pairwise
class in these variables and the star certifies it exactly for the apolar peptides, for
serine on strand and PPII and for the heteropolymer on helix and PPII, but not for poly-Lys
(off by 0.5–17 kcal/mol in 15 of 18 analyses); a same-lineage torsion refit
(ff99SB − ff14SB) is exactly additive (`c_ij = 0`, `c_i` = 0–2.9 kcal/mol by residue type,
independent of length).  Everything is a property of small exposed model peptides with rigid
ideal geometry (in which leucine has *no* rotamer at P's threshold 0.70); no protein interior
was measured, where the third-order constants must be expected to be larger.

---

## 2. Precise statements

### 2.0 Setting

**Molecules.**  Ace-X₁…Xₙ-NMe with X = Ser, Val, Leu, Phe, Lys (homopolymers) and the
heteropolymer `LKSE:n` = the pattern Leu-Lys-Ser-Glu repeated and truncated to `n` residues
(Lys +1, Glu −1; standard Amber protonation).  **Backbones** (uniform `(φ, ψ)`, ω = 180°):
`H = (−57°, −47°)` (ideal α-helix), `E = (−139°, +135°)` (ideal extended strand),
`P2 = (−75°, +145°)` (ideal polyproline II) — textbook values quoted from memory; they are
parameters of the synthetic model and nothing depends on their provenance.  **Geometry**: P's
internal-coordinate builder extended by side chains (`scbuild.py`): all bond lengths and
angles at their ff14SB equilibrium values, methyl and ammonium rotors staggered, rings and
carboxylates planar; the only degrees of freedom are the side-chain dihedrals.

**Site variables.**  One site per residue; the state of a site is the tuple of *all* its
side-chain dihedrals (a rotamer): Val χ₁; Leu, Phe χ₁χ₂; Ser χ₁ and the hydroxyl torsion; Glu
χ₁χ₂χ₃; Lys χ₁…χ₄.  Grid **R3**: every dihedral ∈ {−60°, 180°, +60°} (3 states for Val, 9 for
Leu, Phe and Ser, 27 for Glu, 81 for Lys).

**Domains.**  P's clash score `s = min r_pq/(R_p + R_q)` over atom pairs four or more bonds
apart, `R` = Amber `R_min/2` (with `R = 0` for the hydroxyl hydrogen, whose OpenMM placeholder
radius of 5.6 Å would otherwise mark every serine as a clash — the only deviation from P's
criterion, §3.1).  On a fixed backbone the score is a minimum of a fixed, a one-site and a
two-site part, so for a threshold τ:

* `D_i(τ)` = states of site `i` whose one-site score exceeds τ; `X = ∏ D_i` (raw product);
* `X_τ = {x ∈ X : all two-site scores > τ}` — P's clash-free domain in these variables; it is
  not a product when two rotamers can clash;
* `X′` = a product sub-domain of `X_τ` obtained by greedily deleting the state involved in the
  largest number of two-site clashes until none is left (`an_main.pruned_product`).  If no two
  rotamers clash, `X = X_τ = X′` (all Ser, Val and Leu instances).

The theorems for product spaces (star sandwich etc.) are applied on `X′` only — on the raw
product `X` overlapping atoms make every number meaningless (`f` up to `10¹⁶` kcal/mol), and on
the non-product `X_τ` the star bound is not valid; constants and fits are reported on `X_τ`
and on `X′`.  Thresholds: τ = 0.70 (P's) and τ = 0.60 (P's sensitivity value; "relaxed").
Both are needed because of a geometric fact of the rigid model [M]: **at τ = 0.70 leucine has
no admissible rotamer on any backbone** (its two best R3 states, `(180°, 60°)` and
`(−60°, 180°)` — the two rotamers known as dominant — score 0.645 and 0.633, limited by an
intra-residue H···H contact of 1.82–1.85 Å), valine has a single state in the helix interior
(none from the fourth residue on), the heteropolymer is empty because of its leucines, and at
τ = 0.80 every residue type except serine is empty (§3.1, Table A).

**Energies.**  Known part `f` = ff14SB vacuum energy (torsions + Lennard-Jones + Coulomb; bond
and angle terms are constant by construction).  Residuals:

| symbol | definition |
|---|---|
| `g_GB` | GBn2 polarisation energy (`ε_in = 1`, `ε_out = 78.5`, no salt, no surface term) — P's `g_GB` |
| `g_03`, `g_ipq`, `g_99` | vacuum energy of ff03, ff15ipq, ff99SB minus that of ff14SB at identical coordinates |
| `coul + g_GB` | alternative split: residual = vacuum Coulomb + GB ("solvated electrostatics"), known part = torsions + Lennard-Jones |
| `g_frozen`, `g_fluct` | `g_GB` evaluated with the Born radii frozen at their values in `argmin f`; `g_fluct = g_GB − g_frozen` (Statement 8) |

**Constants** (as in `SP_REPORT.md` §2, on a domain `D`): `c_i(g)` = max `|g(x) − g(x′)|` over
pairs in `D` differing in site `i` only; `c_ij(g)` = max of the mixed second difference
`|g(x^{ab}) − g(x^{a′b}) − g(x^{ab′}) + g(x^{a′b′})|` over quadruples in `D`; new here:
`c_ijk(g)` = max of the mixed third difference over octuples in `D`.  Half row sum:
`½Σ_{j≠i} c_ij`; Dobrushin-type sum: `Σ_{j≠i} tanh(βc_ij/4)`.

**The interfaces of the theory that are tested** (theory report §11.7, read at `5ed4072`):

* *First order* (Theorem 11.7 [V], `CertificateComplexity.lean`): the single evaluation at
  `x₀ = argmin f` certifies `min E` iff `λ* := min_y (f(y) − f(x₀))/d(x₀, y) ≥ 1`,
  `d = Σ c_i[x_i ≠ y_i]`; otherwise certificates are covers (Theorems 11.4, 11.6 [V]).
* *Second order — "the star"* (Theorems 11.16–11.17 [V], `SecondOrderEnvelope.lean`:
  `secondOrder_remainder`, `pairwise_sandwich`, `secondOrder_certified_minimizer_iff`): with
  `g` evaluated on the star of `x₀` (`1 + Σ(k_i − 1)` evaluations) and
  `g_star(x) = g(x₀) + Σ_i [g(x₀^{i→x_i}) − g(x₀)]`, on a product domain
  `|g − g_star| ≤ W(x) := Σ_{i<j both changed} c_ij`, so `L = f + g_star − W ≤ E ≤ f + g_star + W = U`
  are pairwise models, and `x₀` is certified iff it minimises `L`.  Sufficient for an additive
  known part: the **row-sum condition** `½Σ_j c_ij ≤` single-site excitation energies of `E` at
  `x₀` [P, theory report].  I evaluate the *exact* criterion by enumerating `L`, report
  `ε* := min(E on the star) − min L` (the accuracy one star certifies; `ε* = 0` ⇔ exact
  certificate when `x₀ = argmin E`) and the free-energy bracket `ln Z(L) − ln Z(U)`.
* *Third order — "the ball"* (Theorem 11.18 [V], `HigherOrderEnvelope.lean`:
  `higherOrder_remainder`): with `g` on the Hamming ball of radius 2 and the anchored
  interpolant `I₂g`, `|g − I₂g| ≤ Σ_{T ⊆ changed, |T| = 3} c_T`.
* *Free energies under weak coupling* (Theorem 11.33(a) [P, theory report]; stated there for
  the binary cube with uniform constants): polynomial cost when the Dobrushin-type sums are
  below 1.

### Statement 1 [P; checked numerically to rounding] — the known part is exactly pairwise in residue rotamers, and only there

(a) With one site per residue, `f(x) = c₀ + Σ_i h_i(x_i) + Σ_{i<j} J_ij(x_i, x_j)` exactly.
*Proof.*  With rigid bond lengths and angles and a fixed backbone the position of every atom
is a function of the state of at most one site (the atoms beyond Cβ of residue `i`).
Lennard-Jones and Coulomb terms, including the scaled 1–4 terms, involve two atoms; every
torsion term involves atoms of at most one site; bonds and angles are constant. ∎
*Checks [N].*  (i) Rebuilding one site leaves all other atoms where they were (difference
0.0 Å; asserted at `10⁻¹⁰` for every model built).  (ii) Every torsion term of every force
field used is asserted to touch at most one site.  (iii) Tables built by direct atom-pair
summation agree with P's evaluator on the full conformation to `1.1·10⁻¹²` kcal/mol and with
OpenMM's Reference platform to `1.9·10⁻¹²` (12 systems × 200 random assignments,
`test_fbmodel.py`).  (iv) On all 217 non-empty instance analyses
`max_{ijk} c_ijk(f) ≤ 1.6·10⁻¹²` kcal/mol (ranges of `f` up to 306 kcal/mol).

(b) Hence the difference of two fixed-charge force fields at identical coordinates is exactly
pairwise in these variables (`c_ijk(g_03), c_ijk(g_ipq) ≤ 2.1·10⁻¹²` [N]), and a same-lineage
torsion refit is exactly additive: `c_ij(g_99) ≤ 8·10⁻¹⁰` everywhere, with
`c_i(g_99) = 2.77` (Ser), `1.24` (Leu), `1.21` (Val), `0.35–1.18` (Phe, by threshold),
`< 10⁻⁶` (Lys), `2.93` (max over the heteropolymer) kcal/mol, the same for every chain length
and backbone [M].

(c) With one site per χ angle (χ₂ moves with χ₁) `f` is **not** pairwise [M, Ser₃, full grid of
729 assignments re-indexed as six three-state χ-sites, `an_perchi.py`]: third-order mixed
differences vanish (`4·10⁻¹⁴`) iff the three χ's lie in three different residues and reach 4.4
(strand) / 5.5 (helix) kcal/mol for two χ's of one residue and one of another; fourth order
(both χ's of two residues) 6.5 / 5.6; fifth order zero.  In per-χ variables the energy is
"pairwise per residue" only; all statements below use residue sites.

### Statement 2 [M] — first-order constants of the polarisation energy; dependence on chain length

`max_i c_i(g_GB)` on `X′` in kcal/mol; in brackets the value on `X_τ` where it differs; "≥" =
rigorous lower bound from `an_long.py` (true GB difference at a pair of assignments of `X′`).

| residue, backbone, τ | n = 1 | 2 | 3 | 4 | 5 | 6 | 8 | 12 | 16 | longer (lower bounds) |
|---|---|---|---|---|---|---|---|---|---|---|
| Val, E, .70 | 0.31 | 0.37 | 0.42 | 0.43 | 0.44 | 0.44 | 0.44 | 0.44 | ≥ 0.44 | ≥ 0.44 (24) |
| Val, P2, .70 | 0.34 | 0.68 | 0.79 | 0.83 | 0.84 | 0.84 | 0.84 | 0.84 | | ≥ 0.84 (24) |
| Leu, H, .60 | 0.55 | 0.69 | 0.96 | 0.86 | 1.07 | 1.08 | 0.97 | 1.12 | 1.15 | ≥ 1.15 (24), ≥ 1.14 (32) |
| Leu, E, .60 | 0.61 | 0.80 | 0.96 | 0.96 | 0.96 | 0.96 | 0.96 | 0.96 | 0.96 | ≥ 0.95 (32) |
| Leu, P2, .60 | 0.29 | 1.24 | 1.43 | 1.54 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | ≥ 1.56 (32) |
| Phe, H, .60 | 2.57 | 3.21 | 3.01 [3.66] | 3.00 [3.62] | 2.92 [3.11] | 2.60 [3.14] | 1.58 [2.94] | | ≥ 1.55 | |
| Phe, E, .60 | 2.33 | 2.15 | 2.60 | 2.66 | 2.68 | 2.69 | 2.69 | | | |
| Phe, P2, .60 | 2.30 | 3.28 | 3.78 | 3.72 [4.18] | 3.65 [4.50] | 3.63 [4.51] | | | | |
| Ser, E, .70 | 4.20 | 4.53 | 4.81 | 4.90 | 4.93 | 5.02 | | ≥ 5.18 | | ≥ 5.25 (24) |
| Ser, P2, .70 | 4.74 | 6.67 | 6.76 | 7.12 | 7.35 | 7.69 | | ≥ 7.97 | | ≥ 8.04 (24) |
| Ser, H, .70 | 6.76 | 8.58 | 10.09 | 9.80 | 9.04 | 9.37 | | ≥ 9.84 | | ≥ 9.98 (24) |
| Ser, H, .60 | 6.76 | 8.58 | 10.09 | 11.24 | 11.42 | 12.37 | | | | |
| **Lys, H, .70** | 9.96 | 37.25 | 51.50 | 55.66 | | | ≥ 85.5 | ≥ 110.1 | ≥ 123.6 | ≥ 137.9 (24) |
| Lys, H, .60 | 18.63 | 45.24 | 62.84 | 77.89 | | | | | | |
| Lys, E, .70 | 6.30 | 13.86 | 39.29 [44.66] | 47.04 [52.83] | | | ≥ 73.5 | ≥ 81.9 | ≥ 86.0 | |
| Lys, E, .60 | 16.36 | 26.13 | 57.23 [59.60] | 63.46 [71.10] | | | | | | |
| Lys, P2, .70 | 6.73 | 27.51 | 28.61 | 58.28 | | | ≥ 93.8 | ≥ 108.4 | | |
| Lys, P2, .60 | 7.18 | 33.46 | 40.96 [42.69] | 71.68 [74.07] | | | | | | |
| LKSE, H, .60 | 0.55 | 20.30 | 25.79 | 32.24 | 32.93 | 47.66 [61.15] | ≥ 60.0 | ≥ 60.0 | ≥ 65.1 | |
| LKSE, E, .60 | 0.61 | 14.45 | 15.76 | 64.66 [67.97] | 65.84 [69.15] | 63.19 [76.86] | ≥ 72.8 | | | |
| LKSE, P2, .60 | 0.29 | 16.10 | 24.18 | 58.96 | 64.07 | 74.02 | ≥ 71.7 | | | |

(Exact enumerations: Val at `n` = 1–8, 10, 12 and Leu at `n` = 1–8, 10, 12, 14, 16, of which the
table shows a selection; all values are in `out/tables.md`, Table B.  Poly-Val on the helix is trivial: only
the first two residues have more than one state.  The lower bounds were validated where the
exact value exists: Lys₄/H `[34.723 55.665 49.606 36.787]` against exact
`[34.72 55.66 49.61 36.79]`.)

*Findings.*  (i) **Neutral side chains: the constants saturate**, at a value set by the
residue type and the backbone — Val 0.44 (E), 0.84 (P2); Leu 0.96 (E), 1.15 (H), 1.56 (P2);
Phe 1.6–4.5; Ser 5.0–5.3 (E), 7.7–8.0 (P2), 9.4–10 (H; 12.4 at τ = 0.60) kcal/mol, i.e.
`βc = 0.7–17` — from 3–6 residues on, and remain there in the lower bounds at 24–32
residues.  P's prediction ("bounded by the solvation of one side chain") holds.
(ii) **Charged side chains: the constants grow with the chain.**  Poly-Lys on the helix:
10 → 56 kcal/mol exactly for `n = 1 → 4`, and at least 85, 110, 124, 138 for `n = 8, 12, 16, 24`
(`βc ≥ 231`); the growth decelerates (+30, +25, +13, +14 per 4, 4, 4, 8 residues) but has not
stopped at 24 residues.  Along the chain the constants are largest at the ends (Lys₂₄/H: 138,
130, 126 for the first three sites, 75–85 in the interior, 93–95 for the last three).
Strand: 47 at `n = 4`, ≥ 73, 82, 86 at 8, 12, 16; PPII: 58 at `n = 4`, ≥ 94, 108 at 8, 12.  The heteropolymer with alternating charges saturates near
60–75 kcal/mol by eight residues.  (iii) The mechanism of (ii) is the pair term between net
charges, `−(1 − 1/ε_out)·q_iq_j/f_GB(r)`, whose change under a displacement of one charge
decays as `r⁻²` and has one sign for all charges on one side of the moving one [H; consistent
with the end effect and with `c_ij` by separation in Statement 3].  The vacuum Coulomb term
of `f` cancels it: for `coul + g_GB` the same constants are 5.3, 11.9, 15.1, 15.4 (Lys/H,
τ = 0.70, `n = 1…4`).  (iv) *Typical* single-site changes are a third to a tenth of the
constants: sup/RMS = 1.7–3.0 (Val, Leu, Phe, Ser), 4.4–5.7 (Lys), 5.7–11 (LKSE).
(v) Threshold: relaxing τ from 0.70 to 0.60 changes nothing for Ser on E and P2 (all nine
states pass at 0.80 as well) and raises the other values by 15–40 % (Ser on the helix 9.4 → 12.4;
Lys₄ 55.7 → 77.9 on the helix, 47 → 63 on the strand, 58 → 72 on PPII).

### Statement 3 [M] — second-order constants: size, decay, row sums

(a) *Size.*  Largest `c_ij(g_GB)` on `X′` (longest enumerated chain): Val 0.11–0.12; Leu 0.12
(P2), 0.14 (E), 0.51 (H); Phe 0.5 (H, E), 1.7 (P2); Ser 2.42 (E), 2.14 (P2), 2.81 (H, 3.05 at
τ = 0.60); Lys 19–41 (τ = 0.70), 30–51 (τ = 0.60); LKSE 32 (H), 41–51 (P2), 78 (E, the
Lys–Glu pair two residues apart on the same side of the strand).

(b) *Decay with sequence separation `s` and Cβ–Cβ distance* (max over pairs; kcal/mol):

| system | `s`: distance (Å) → max `c_ij` |
|---|---|
| Ser₆, E | 1: 5.7 → 1.31; 2: 6.9 → 2.42; 3: 11.3 → 0.33; 4: 13.8 → 0.19; 5: 17.9 → 0.07 (lower bounds at `n = 24`: 0.05, 0.03, 0.02, 0.01 for `s = 6…9`) |
| Ser₆, H | 1: 5.3 → 2.81; 2: 7.2 → 0.70; 3: 5.6 → 1.34; 4: 6.5 → 2.30; 5: 9.8 → 0.45 (then ≥ 0.24, 0.43, 0.21, 0.11, 0.12, 0.11 for `s = 6…11`) |
| Val₁₂, E | 1: 5.7 → 0.115; 2: 6.9 → 0.049; 3: 11.3 → 0.0044; 4: 13.8 → 0.0011; 6: 20.7 → 6·10⁻⁵; 8: 27.6 → 5·10⁻⁶; 11: 38.2 → 7·10⁻⁷ |
| Leu₁₆, H | 1: 5.3 → 0.19; 3: 5.6 → 0.18; 4: 6.5 → 0.51; 5: 9.8 → 0.17; 8: 12.9 → 0.05; 10: 15.8 → 0.037; 12: 19.1 → 0.024; 15: 23.0 → 0.008 |
| Lys₄, H (τ .70) | 1: 17.6; 2: 7.3; 3: 19.1; lower bounds at `n = 16`: 17.6, 7.2, 18.9, 17.6, 2.8, 2.9, 7.9, 3.2, 0.9, 1.8, 2.2, 1.0, 0.6, 1.0, 0.9 for `s = 1…15` |
| Lys₁₂, E (lower bounds) | 12.2, 41.4, 5.4, 5.7, 2.0, 1.6, 0.9, 0.7, 0.5, 0.4, 0.3 for `s = 1…11` |

Neutral, apolar: steep decay (Val on the strand roughly `r⁻⁷`).  Neutral, polar: about `r⁻⁴`.
In the helix the decay follows the three-dimensional distance, not the separation.  Charged:
a slow tail (≈ 1 kcal/mol at 22 Å).  For Leu the pair coupling is absent from the known part
beyond `s = 4` (`c_ij(f) ≤ 0.014`) and from the frozen-radius GB (Statement 8): its tail is
the long-range part of the descreening integrals.

(c) *Row sums against excitation energies* (`X′`; excitation = smallest single-site
excitation energy of `E = f + g_GB` at `argmin E`, min over sites; kcal/mol):

| system | max half row sum `½Σ_j c_ij` | min excitation | max Dobrushin-type sum | row-sum condition |
|---|---|---|---|---|
| Val₁₂, E / P2 (.70) | 0.16 / 0.21 | 2.47 / 0.89 | 0.14 / 0.18 | holds |
| Leu₁₆, E / P2 (.60) | 0.20 / 0.32 | 18.2 / 1.56 | 0.17 / 0.27 | holds |
| Leu₁₆, H (.60) | 1.15 (0.89 at `n = 12`) | 0.52 | 0.96 | holds for `n ≤ 12` (except `n = 5`), fails at one N-terminal site for `n = 14, 16` |
| Phe₈, E (.60) | 0.80 | 0.62 | 0.66 | holds site by site at `n = 8`; fails at `n = 4–7`, where one excitation energy is 0.03–0.04 |
| Phe₁₀, H / Phe₇, P2 (.60) | 0.80 / 2.25 | 0.21 / 0.03 | 0.67 / 1.67 | fails |
| Ser₂, E | 0.65 | 1.03 | 0.50 | holds |
| Ser₆, E / P2 / H (.70) | 3.89 / 3.50 / 4.86 | 1.02 / 0.42 / 0.13 | 2.67 / 2.52 / 3.16 | fails by ×4 / ×8 / ×37 |
| Lys₄, H / P2 (.70) | 22.0 / 35.6 | 0.46 / 0.97 | 3.0 (= n − 1, saturated) | fails by ×48 / ×37 |
| Lys₁₆, H (lower bounds) | ≥ 52.6 | — | ≥ 13.5 | fails at 16 of 16 sites; median ratio ≥ 20 |
| LKSE:6, H / P2 (.60) | 28.5 / 52.5 | 0.16 / 0.01 | 4.7 / 4.4 | fails |

For an interior site of a long poly-Ser strand the half row sum converges (lower bounds 4.34
at `n = 12` and 4.45 at `n = 24`; exact value 3.89 at `n = 6`); for poly-Lys it does not converge within 16 residues.

### Statement 4 [M] — third order: `g_GB` is close to pairwise in the rotamers — in supremum norm for neutral side chains, in RMS only for charged ones

`X′`, longest enumerated chain of each kind; `c_ijk`: max over triples and sum over all
triples; fit: best approximation of `g_GB` by a sum of one-site and two-site tables (least
squares; "Cheb." = sup-optimal by linear programme where the domain is small enough).

| system | assignments | max `c_ijk` | Σ `c_ijk` | one-site fit RMS / max | two-site fit RMS / max / Cheb. | std of `g_GB` |
|---|---|---|---|---|---|---|
| Ser₆, E (.70) | 531 441 | 0.0043 | 0.022 | 0.61 / 3.5 | 0.0003 / 0.0030 / — (Ser₄: 0.0002 / 0.0015 / 0.0008) | 2.65 |
| Ser₆, P2 (.70) | 531 441 | 0.0027 | 0.017 | 0.57 / 3.2 | 0.0002 / 0.0019 / — | 4.32 |
| Ser₆, H (.70) | 104 976 | 0.054 | 0.23 | 0.75 / 4.1 | 0.0028 / 0.030 / — (Ser₄: 0.0019 / 0.017 / 0.0075) | 5.02 |
| Ser₆, H (.60) | 531 441 | 0.20 | 1.75 | 0.93 / 4.8 | 0.014 / 0.21 / — | 5.46 |
| Val₁₂, E (.70) | 531 441 | 0.0059 | 0.083 | 0.079 / 0.40 | 0.0015 / 0.0071 / — | 0.51 |
| Val₁₂, P2 (.70) | 531 441 | 0.0064 | 0.16 | 0.083 / 0.33 | 0.0023 / 0.013 / — | 0.86 |
| Leu₁₆, E (.60) | 65 536 | 0.0054 | 0.18 | 0.13 / 0.67 | 0.0021 / 0.0073 / — | 0.85 |
| Leu₁₆, P2 (.60) | 65 536 | 0.016 | 0.49 | 0.14 / 0.52 | 0.0086 / 0.028 / — | 1.86 |
| Leu₁₆, H (.60) | 65 536 | 0.086 | 7.4 | 0.25 / 0.99 | 0.047 / 0.21 / — | 0.82 |
| Phe₁₀, H (.60) | 19 200 | 0.096 | 0.41 | 0.19 / 0.76 | 0.0088 / 0.041 / — | 1.26 |
| Phe₇, P2 (.60) | 112 500 | 0.088 | 1.01 | 0.44 / 2.0 | 0.013 / 0.076 / — | 2.38 |
| Lys₄, H (.70) | 16 464 | 0.14 | 0.25 | 3.6 / 20 | 0.0042 / 0.082 / — (Lys₃: 0.0034 / 0.069 / 0.018) | 16.3 |
| Lys₃, E (.70) | 5 733 | 0.15 | 0.15 | 3.2 / 19 | 0.0031 / 0.070 / 0.018 | 11.1 |
| Lys₄, E (.70) | 74 529 | 0.19 | 0.53 | 4.5 / 38 | 0.0048 / 0.18 / — | 16.1 |
| Lys₄, P2 (.70) | 194 481 | **2.39** | 2.97 | 4.6 / 28 | 0.036 / **1.65** / — | 15.5 |
| Lys₄, H (.60) | 353 220 | **1.90** | 4.08 | 5.2 / 35 | 0.026 / **1.30** / — | 18.3 |
| Lys₄, E (.60) | 450 225 | 1.05 | 2.6 | 6.1 / 60 | 0.026 / 0.67 / — | 16.8 |
| Lys₄, P2 (.60) | 783 000 | **10.2** | 13.4 | 6.0 / 40 | 0.12 / **7.8** / — | 17.1 |
| LKSE:6, H (.60) | 217 152 | 0.71 | 3.4 | 3.2 / 20 | 0.041 / 0.36 / — | 12.2 |
| LKSE:6, P2 (.60) | 622 728 | 0.45 | 2.2 | 4.8 / 42 | 0.019 / 0.30 / — | 12.4 |
| LKSE:6, E (.60) | 341 172 | 0.15 | 0.58 | 7.4 / 39 | 0.0073 / 0.12 / — | 13.4 |

On the non-product `X_τ` the values are the same or somewhat larger (LKSE:6/H: max `c_ijk`
4.1, two-site fit 0.087 / 2.2).  Lower bounds for the central triples of long chains
(`an_long.py`): Ser₂₄/E 0.004, Ser₂₄/H 0.019, Leu₃₂/H 0.035, Lys₂₄/H 0.58, Lys₈/P2 2.4.

*Reading.*  For the neutral peptides the solvent term is within `0.002–0.2` kcal/mol of the
pairwise class **in supremum norm over the whole enumerated domain** (`βη_sup ≤ 0.35`; `≤ 0.05`
for Ser, Val and Leu on strand and PPII), and `Σ c_ijk` grows about linearly with the chain
(Ser/E: 0.004, 0.010, 0.016, 0.022 for `n = 3…6`, i.e. 0.006 kcal/mol per residue; Ser/H at
τ = 0.70: 0.05, 0.08, 0.15, 0.23, i.e. 0.06–0.08 per residue; for Leu on the helix the sum
over the 560 triples of the 16-mer is 7.4 although no single `c_ijk` exceeds 0.09).  For charged side chains the typical remainder is as small (RMS ≤ 0.04 at
τ = 0.70, ≤ 0.12 at 0.60) but its maximum is not: 0.07–0.18 kcal/mol for Lys on helix and
strand at τ = 0.70, 1.65 for Lys₄ on PPII, and 0.7–7.8 at τ = 0.60 — the largest `c_ijk`, 2.4
(τ = 0.70) and 10.2 (τ = 0.60) kcal/mol, belongs to the triple of residues 1, 2, 4 of Lys₄ on
PPII, three long charged side chains that can converge.  The sup/typical gap that P found
at first order reappears here at third order, for charged side chains only.  This is the opposite of P's finding in backbone torsions (all
torsion pairs: RMS 2.10, max 13.4 kcal/mol at five residues).  The one-site (additive) class
is far in every polar case (max 3–42 kcal/mol).

### Statement 5 [M, with the theorems of the theory report] — which interface has a real instance

All on `X′`, by enumeration of the lower models; energies kcal/mol, free energies nats.

(a) **First order.**  The one-evaluation criterion `λ* ≥ 1` (Theorem 11.7 [V]) holds for
`g_GB` in: poly-Val on E (`λ* = 5.67`, all 12 sites sharp, `n ≤ 12`) and on P2 (`λ* = 1.25`);
poly-Leu on E (`λ* = 18`) and on H for every `n ≤ 16` except `n = 5` (`λ* = 1.16–2.4`; 0.88 at
`n = 5`; 15 of 16 sites sharp at `n = 16`); poly-Phe on E at `n = 3`.  It fails in every other
instance: poly-Leu on P2 (`λ* = 0.45–0.75`), Phe at the relaxed threshold (0.01–0.7), Ser
(`λ* = 0.007–0.17`, no site sharp), Lys (`4·10⁻⁴–0.04`), LKSE (0.005–0.16 for `n ≥ 3`).
Smallest certificates in the per-site format on `X_τ` (lower bound = forced points / volume /
partition bound, upper bound = greedy cover; `an_cover.py`, the same computation as P's):

| instance (`X_τ` size) | ε = 0 | ε = k_BT | ε = 2 kcal/mol |
|---|---|---|---|
| `g_GB`, Val₈/E (6 561); Leu₁₂/H (4 096); Leu₁₄/H (16 384) | 1 | 1 | 1 |
| `g_GB`, Phe₈/H, τ .60 (14 014) | [2, 4] | [2, 3] | 1 |
| `g_GB`, Ser₄/E (6 561) | [53, 156] | [30, 116] | [4, 53] |
| `g_GB`, Ser₄/H (2 916) | [455, 582] | [322, 447] | [126, 253] |
| `g_GB`, Ser₅/H (17 496) | [1 361, 2 172] | [911, 1 687] | [267, 927] |
| `g_GB`, Lys₃/H, τ .70 (2 352) | 2 128 | 2 108 | 2 059 |
| `g_GB`, Lys₃/H, τ .60 (20 718) | [15 721, 15 725] | [15 547, 15 553] | [15 120, 15 130] |
| `g_GB`, LKSE:4/H (7 254) | [78, 754] | [47, 707] | [18, 611] |
| `g_GB`, LKSE:5/H (14 508) | [68, 800] | [42, 761] | [16, 660] |
| `g_03`, Val₈/E; Leu₁₂/H | 1 | 1 | 1 |
| `g_03`, Ser₄/E; Ser₄/H | [7, 85]; [2, 24] | [3, 59]; [2, 15] | [2, 24]; [2, 6] |
| `g_03`, Lys₃/H (.70); LKSE:4/H | [28, 30]; [2, 8] | [22, 24]; [2, 5] | [12, 16]; 1 |

(The measured single-flip constants are a valid envelope on these non-product domains:
`max |g(x) − g(y)|/d(x, y) = 1.0000` in all 17 runs.)  The first-order format thus ranges from
"one evaluation" (apolar) through 1–20 % of the domain (Ser) to **76–90 % of the domain**
(poly-Lys).

(b) **Second order: the star.**  `N★ = 1 + Σ(k_i − 1)` evaluations at `x₀ = argmin E`.

| instance | `X′` | `N★` | row-sum condition | measured max `|g − g_star|` (bound max `W`) | `ε*` | bracket `ln Z(L) − ln Z(U)` |
|---|---|---|---|---|---|---|
| Val₁₂, E (.70) | 531 441 | 25 | holds | 1.10 (1.74) | **0** | 0.0006 |
| Val₁₂, P2 (.70) | 531 441 | 25 | holds | 0.51 (2.16) | **0** | 0.21 |
| Leu₁₆, E (.60) | 65 536 | 17 | holds | 2.64 (2.83) | **0** | < 10⁻³ |
| Leu₁₆, P2 (.60) | 65 536 | 17 | holds | 0.82 (4.36) | **0** (while `λ* = 0.45`) | 0.008 |
| Leu₁₆, H (.60) | 65 536 | 17 | fails at one site | 1.27 (13.6) | **0** | 0.015 |
| Phe₈, E (.60) | 1 728 | 15 | holds at `n = 8` | 0.88 (3.26) | **0** (every `n ≤ 8`) | 0.03 (0.13–0.16 at `n = 5–7`) |
| Phe₁₀, H (.60) | 19 200 | 20 | fails | 1.70 (4.97) | 0.06 (0–0.43 over `n`) | 0.34 |
| Phe₇, P2 (.60) | 112 500 | 31 | fails | 2.43 (9.58) | 1.52 | 2.05 |
| Ser₂, E | 81 | 17 | holds | — | **0** | 0.62 |
| Ser₃ … Ser₆, E | 729 … 531 441 | 25 … 49 | fails | 5.90 (17.7) at `n = 6` | 1.70, 4.41, 7.54, 10.65 | 5.0, 10.7, 17.0, 23.4 |
| Ser₆, P2 | 531 441 | 49 | fails | 7.25 (17.4) | 20.3 | 35.8 |
| Ser₆, H (.70 / .60) | 104 976 / 531 441 | 37 / 49 | fails | 6.03 (21.0) / 8.40 (30.8) | 22.6 / 32.4 | 38.2 / 54.8 |
| Lys₂ … Lys₄, H (.70) | 196 … 16 464 | 27 … 44 | fails | 36.0 (74.7) at `n = 4` | 17.7, 43.6, 79.0 | 29.9, 72.7, 132 |
| Lys₄, H (.60); Lys₄, P2 (.70) | 353 220; 194 481 | 96; 81 | fails | 67 (146); 41 (134) | 178; 144 | 297; 242 |
| LKSE:3 … LKSE:6, H (.60) | 558 … 217 152 | 40 … 66 | fails | 25.8 (87.6) at `n = 6` | 12.9, 32.4, 32.6, 82.3 | 20.9, 53.7, 54.2, 138 |
| LKSE:6, P2 / E (.60) | 622 728 / 341 172 | 88 / 75 | fails | 51 (141) / 48 (158) | 161 / 170 | 269 / 285 |
| Lys₄, E (.70) | 74 529 | 65 | fails | 52 (122) | 121 | 204 |
| Lys₄, E / P2 (.60) | 450 225 / 783 000 | 101 / 116 | fails | 74 (190) / 53 (184) | 204 / 195 | 341 / 327 |

So **for `g_GB` the star is an exact certificate in the apolar homopolymers** — in poly-Leu
on PPII (and poly-Phe on the strand at `n = 4–7`, `λ* = 0.14–0.18`) it certifies where the
first-order criterion does not, which makes these genuine instances of Theorems 11.16–11.17:
the theorems then give `min E` exactly from 17 (resp. 11–14) evaluations of `g_GB`, the
minimiser from the pairwise kernel applied to `L`, and `ln Z` to within 0.008 (resp. ≤ 0.16)
nats — **and it fails for every polar or charged instance with more than two residues**, the
certified accuracy degrading linearly in the chain length (the "quadratic law" of theory
report §11.7 seen on a real instance: the envelope half-width `W` is a sum over pairs).
Overall the star is an exact certificate in 110 of the 181 instance analyses with at least
two sites.  The plain row-sum condition (a theorem only for an additive known part; request
T-2) holds in 97 of them and in no instance where the star fails; it is violated in the
other 13 exact ones (e.g. Leu₁₆/H), so it is sufficient in practice and not necessary.  In
all 110 the Dobrushin-type sums are below 1 (0.003–0.96).  The converse fails in 12 instances (Ser₂ on helix and PPII;
Phe on the helix and Phe₂ on PPII, where the star is off by 0.06–0.43 kcal/mol).

(c) **Third order: the Hamming-2 ball.**  `N_ball = 1 + Σ(k_i − 1) + Σ_{i<j}(k_i − 1)(k_j − 1)`
evaluations at `x₀ = argmin E`; lower model `f + I₂g − Σ_{T ⊆ changed} c_T`.

| instance | `X′` | `N_ball` | measured max `|g − I₂g|` (bound max) | certified accuracy ε | bracket | pairwise version (see (d)): ε, bracket |
|---|---|---|---|---|---|---|
| Ser₆, E (.70) | 531 441 | 1 009 | 0.0047 (0.022) | **0** | 0.0011 | 0, 0.018 |
| Ser₆, P2 (.70) | 531 441 | 1 009 | 0.0036 (0.017) | **0** | 0.017 | 0, 0.038 |
| Ser₆, H (.70) | 104 976 | 571 | 0.066 (0.23) | **0** | 0.12 | 0, 0.41 |
| Ser₆, H (.60) | 531 441 | 1 009 | 0.30 (1.75) | **0** | 1.12 | 0.27, 3.2 |
| Val₈, E (.70) | 6 561 | 129 | 0.0062 (0.048) | **0** | 2·10⁻⁷ | 0, 0.0016 |
| Leu₈, H (.60) | 256 | 37 | 0.25 (1.23) | **0** | 3·10⁻⁵ | 0, 0.20 |
| Phe₇, P2 (.60) | 112 500 | 416 | 0.20 (1.01) | **0** | 0.0010 | 0.055, 0.26 |
| Lys₄, H (.70) | 16 464 | 721 | 0.19 (0.25) | **0** | 0.014 | 0, 0.23 |
| Lys₃, E (.70) | 5 733 | 933 | 0.14 (0.15) | **0** | 0.0012 | — |
| Lys₄, E (.70) | 74 529 | 1 569 | 0.33 (0.53) | **0** | 0.0017 | — |
| Lys₄, P2 (.70) | 194 481 | 2 481 | 1.74 (2.97) | **0** | 0.17 | 0, 1.73 |
| Lys₄, H (.60) | 353 220 | 3 444 | 2.11 (4.08) | 0.19 | 1.12 | 1.43, 4.0 |
| Lys₄, E (.60) | 450 225 | 3 841 | 0.74 (2.62) | **0** | 0.036 | — |
| Lys₄, P2 (.60) | 783 000 | 5 075 | 10.2 (13.4) | **6.7** | 14.5 | — |
| LKSE:5, H (.60) | 14 508 | 850 | 0.48 (1.53) | **0** | 0.082 | 0.25, 1.39 |
| LKSE:6, H (.60) | 217 152 | 1 569 | 0.85 (3.41) | **0** | 0.12 | 0.68, 2.76 |
| LKSE:6, P2 (.60) | 622 728 | 2 795 | 0.44 (2.20) | **0** | 0.22 | 0.75, 2.68 |

In all 126 instance analyses with three to eight sites the ball is an exact certificate of
`min E`, except three poly-Lys instances at the relaxed threshold: helix, `n = 3, 4`
(ε = 0.14, 0.19 kcal/mol) and PPII, `n = 4` (ε = 6.7 kcal/mol).  The free-energy bracket is
below 0.18 nats in every instance at τ = 0.70; at 0.60 it is below 0.25 nats except in those
three (0.54, 1.12, 14.5) and for Ser₅, Ser₆ on the helix (0.56, 1.12).  **This is the
interface that has a real instance for the solvent term**: polynomially many evaluations
(`≈ n²k²/2`), a remainder controlled by measured third-order constants, exact certificates
at P's threshold for every residue type — and a clear limit where three charged side chains
meet.  For the charged peptides the ball costs
a few per cent of the domain at these sizes (Lys₄/P2: 1.3 %; Lys₃/E: 16 %) where the
first-order format needs 76–90 %.

(d) *A pairwise form of the third-order interface* **[P; evaluated on the instances, last
column of (c)].**  The lower model of (c) contains three-site terms, so the theory's pairwise
kernel does not apply to it.  But every triple inside the changed set `S` is counted three
times in `Σ_{i∈S} γ_i` with `γ_i := ⅓ Σ_{T ∋ i} c_T`, hence
`|g − I₂g| ≤ Σ_{T ⊆ S} c_T ≤ Σ_{i∈S} γ_i`, and `L₃ = f + I₂g − Σ_i γ_i[x_i ≠ x₀_i]` is a
*pairwise* lower model (`U₃` likewise): Theorem 11.18 with a one-body penalty, so the
pairwise kernel can be applied to it (the corresponding soundness lemma is request T-1).  A sufficient "third-order
row-sum condition" is `γ_i ≤` single-site excitation energy.  Measured: it holds, and `L₃`
certifies exactly, for Ser₆ on all three backbones at τ = 0.70 (`γ_i ≤ 0.011` on E, ≤ 0.06 on
H, against excitations 0.13–1.2), for Val₈, Leu₈, Lys₄/H and Lys₄/P2 at 0.70; with the
relaxed threshold and for the heteropolymer `L₃` certifies to within 0.06–1.4 kcal/mol.

(e) *What these numbers give for long chains* **[model-relative; extrapolation labelled H].**
`N_ball(n, k) = 1 + n(k − 1) + ½n(n − 1)(k − 1)²`: for 100 residues with nine states,
317 601 evaluations for a space of `9¹⁰⁰ ≈ 10⁹⁵` assignments; if `c_ij` is negligible beyond a
few neighbours (Ser/E: < 0.05 beyond `s = 5`) the pairs can be restricted and the count is
`O(nk²)`.  With `Σ_T c_T ≈ 0.006 n` (Ser/E) the constant-shift form of (d) certifies to
`2Σc_T ≈ 1.2` kcal/mol and brackets `ln Z` to `2βΣc_T ≈ 2` nats at 100 residues, i.e. 0.02
nats per residue [H] — to be compared with 43–48 nats per residue for the per-torsion class
(`SP_REPORT.md`, Statement 7).  Whether the *site-wise* condition of (d) persists is governed
by `γ_i`, which stops growing with `n` once `c_ijk` is local; measured, the average `γ_i` of
Ser on the strand is 0.0024, 0.0031, 0.0036 for `n = 4, 5, 6` and on the helix 0.02, 0.03,
0.04 — still rising slowly at six residues.

### Statement 6 [M] — the typical-norm gap

(a) *Sup against RMS of single-site changes*: Statement 2(iv).  (b) *Jensen gap against the
class bound.*  `ln Z(f+g) − ln Z(f) + β⟨g⟩_f` on `X′`, next to `Σ_i ln cosh(βc_i/2)`
(Theorems 3.1(e), 11.25 of the theory report): Ser₆/E 0.99 against 20.0; Ser₆/P2 8.5 / 31.0;
Ser₆/H 4.4 / 36.7; Val₁₂/E 0.02 / 0.7; Leu₁₆/H 0.17 / 2.9; Leu₁₆/P2 1.44 / 6.5; Phe₁₀/H
0.15 / 4.4; Lys₄/H 4.6 / 145.5; Lys₄/P2 4.3 / 167; LKSE:6/H 25.7 / 113.5; LKSE:6/P2
24.6 / 176.6 nats.  As in P's pilot the class allows far more than the function does — by a
factor 4–40 here against 30–80 there; the heteropolymer has by far the largest Jensen gaps
measured in either workstream (11–26 nats at five and six residues): there the residual
genuinely reweights the ensemble, and the minimiser of `f` lies 5–17 kcal/mol above the
minimum of `E`.
(c) *Low-order fits*: Statement 4.  The one-site class is a poor model of `g_GB` (RMS
0.1–5, max 0.3–42 kcal/mol); the two-site class is a good one in RMS *and*, for neutral
side chains, in supremum norm.  The gap between "typical" and "worst case" that dominated
P's findings is, in rotamer variables, confined to first and second order.

### Statement 7 [P for the structure; M for the numbers] — force-field differences

By Statement 1(b), `g_03` and `g_ipq` are exactly pairwise and `g_99` exactly additive.  For
pair-additive residuals the constants are computed exactly for *any* length from the tables
(`an_long.py`: `c_i = max_{a,b}[h_i(a) − h_i(b) + Σ_j max_t (J_ij(a,t) − J_ij(b,t))]`).

| `g_03` on `X′` | max `c_i` by `n` | max `c_ij` | max half row sum | star at `argmin E` |
|---|---|---|---|---|
| Val, E / P2 (.70) | 0.61 / 1.05 (`n = 12`); 0.61 / 1.05 (`n = 24`) | 0.02 | 0.04 | exact at every enumerated `n ≤ 12` |
| Leu, H / E / P2 (.60) | 0.86 / 1.28 / 1.33 (`n = 16`); 0.85 (`n = 32`, H) | 0.01–0.02 | 0.02–0.04 | exact at every enumerated `n ≤ 16` |
| Phe, H / E / P2 (.60) | 1.49 / 1.26 / 2.70 | 0.16–0.19 | 0.17–0.34 | exact |
| Ser, E / P2 / H (.70) | 4.83 / 5.85 / 5.02 (`n = 6`); 4.83 / 5.84 / 5.20 (`n = 24`) | 0.31 / 0.25 / 0.54 | 0.53 / 0.42 / 0.81 (0.61 / 0.54 / 0.92 at `n = 24`) | exact on E and P2 at every `n ≤ 6`; on H off by 0.1–0.6 for `n = 2–5`, exact at `n = 6` |
| Lys, H (.70) | 2.9, 6.0, 8.6, 9.2 (`n = 1…4`); 9.5, 8.7, 8.6, 9.0 (`n = 8, 12, 16, 24`) | 2.2–2.4 | 2.5 (`n = 4`) → 6.9 (`n = 24`) | fails: ε* = 1.7, 2.7, 0.5 (`n = 2, 3, 4`); 3.5–11.6 at τ = 0.60 |
| Lys, E / P2 (.70) | 5.2 (`n = 3`), 7.0–7.5 (`n = 8–16`) / 6.4 (`n = 4`), 9.0–9.9 (`n = 8, 12`) | 4.4 / 3.3 | 2.7 / 3.5 | E: exact at `n = 2, 4`, ε* = 1.9 at `n = 3` (2.6, 3.5 at τ = 0.60); P2: ε* = 0.9, 2.0, 3.6 (4.2, 9.6, 16.8 at τ = 0.60) |
| LKSE, H / P2 (.60) | 9.4 / 12.5 (`n = 5`); 11.4–11.8 (`n = 8–16`, H) | 1.4–2.6 / 2.0 | 1.3–2.4 / 1.9–2.3 | exact at every `n ≤ 6` |
| LKSE, E (.60) | 12.5 (`n = 5`) | 1.9 | 1.5 | ε* = 0.2, 2.1, 3.2, 5.4 at `n = 3…6` |

*Findings.*  (i) The constants of a change of charge model do **not** grow with the chain,
for charged residues either (the net charges are the same in both force fields; the
difference is of dipolar range).  (ii) For neutral peptides the second-order interface works
exactly as the theory describes: `βc_i = 1–10`, half row sums 0.02–0.9 kcal/mol below the
excitation energies, one star certifies, brackets 0.001–2 nats — while the first-order
format needs up to 85 evaluations at four residues (Statement 5(a)) and `λ* < 1` for Ser,
Phe, Lys.  In several of these instances (Ser₆ on strand and helix, Leu₁₆ and Phe₇ on PPII)
the minimiser of `f + g_03` differs from that of `f` (regret 0.2–3.7 kcal/mol), so the
certificate is not a triviality.  The neutral exception is serine on the helix up to five
residues (star off by 0.1–0.6 kcal/mol).  (iii) For poly-Lys the row sums (2.5–6.9) exceed
the excitation energies (0.1–2.3) and the star fails by 0.5–17 kcal/mol in 15 of the 18
poly-Lys analyses; the ball is exact by construction (`c_ijk = 0`).  (iv) `g_ipq` behaves like
`g_03` (max `c_i` 1.0–2.7 neutral, 6.5–10 Lys, 5.9–8.4 LKSE/H; Table B of `out/tables.md`; star
exact in 155 of 180 analyses; `g_03`: 154 of 181).
(v) `g_99`: one star determines the residual completely (`starPart_eq_of_additive` [V]).

### Statement 8 [M] — why: the anatomy of the pair part

`an_mech.py`, on `X′`.  `g_frozen` = the GB expression with the Born radii frozen at their
values in `argmin f` — pair-additive in atoms, hence exactly pairwise in the sites
(`c_ijk ≤ 3·10⁻¹³` measured), and computable without the radii of any other assignment;
`g_fluct = g_GB − g_frozen`.

| instance | Born radii: largest relative range over `X′` | `c_i`, `c_ij` of `g_GB` | of `g_frozen` | of `g_fluct` (half row sum) | `c_ij` of `coul+g_GB` | of `coul+g_frozen` |
|---|---|---|---|---|---|---|
| Ser₅, E (.70) | 14 % | 4.93, 2.42 | 4.60, 2.74 | 1.33, 0.35 (0.42) | 0.69 | 0.36 |
| Ser₅, H (.70) | 44 % | 9.04, 2.81 | 9.41, 3.66 | 3.70, 1.76 (1.69) | 3.22 | 1.46 |
| Ser₅, H (.60) | 145 % | 11.4, 3.04 | 10.0, 3.66 | 4.52, 2.41 (3.15) | 3.54 | 2.41 |
| Leu₁₂, H (.60) | 135 % | 1.12, 0.52 | 0.45, 0.024 | 0.88, 0.53 (0.91) | 0.50 | 0.040 |
| Phe₈, H (.60) | 122 % | 1.58, 0.52 | 1.34, 0.35 | 1.42, 0.50 (0.65) | 0.63 | 0.18 |
| Lys₃, H (.70) | 127 % | 51.5, 17.7 | 62.5, 21.6 | 13.1, 6.1 (5.9) | 6.9 | 1.25 |
| Lys₃, H (.60) | 227 % | 62.8, 29.7 | 100, 58.5 | 58.9, 61.4 (58.2) | 72.7 | 11.3 |
| LKSE:5, H (.60) | 164 % | 32.9, 11.2 | 35.1, 10.7 | 14.6, 8.8 (6.2) | 12.6 | 4.6 |

*Reading.*  (i) For polar and charged side chains the pair constants of `g_GB` are those of
the frozen-radius pair interaction: direct reaction-field cross terms between the partial
charges of two side chains, which are pairwise by construction and are the negative of
(1 − 1/78.5 of) their vacuum Coulomb interaction at long range; adding the Coulomb term
removes most of them (`coul + g_frozen`: 0.36 instead of 2.74 for Ser/E, 1.25 instead of 21.6
for Lys).  (ii) The response of the Born radii to the rotamers — the many-body part of GB —
enters already at *second* order in the sites, because two side chains descreen the same
atoms: `c_ij(g_fluct)` = 0.35–2.4 (Ser), 0.5 (Leu, Phe), 6–61 (Lys).  For leucine this is the
whole pair coupling (the frozen-radius coupling is 0.024), and the self and cross parts of
`g_GB`, each with a range of about 90 kcal/mol over the domain, cancel to 3.9.  (iii) Third
order is what is left after both, and it is small (Statement 4).  (iv) So no split of the
kind tried rescues the star for charged side chains: with `coul + g_GB` as residual the star
is exact for all apolar instances and for serine on strand and PPII at every length (half
row sums 0.54–0.78) and on the helix at τ = 0.70 for `n = 4–6` (it is off by 0.1–5.3 there for
`n = 2, 3` and at τ = 0.60), but fails for Lys and LKSE beyond two residues by 0.2–233
kcal/mol; with the frozen-radius term moved into the known part the remaining `g_fluct` satisfies the
row-sum condition for Ser on the strand (0.42 against 1.02) and not on the helix (1.7–3.2
against 0.13) nor for Lys (5.9–58).

### Statement 9 [P] — what the measured numbers do and do not license

(i) Every number is an exact property of a finite set (a three-state-per-dihedral grid, a
clash filter, a rigid ideal geometry, ideal uniform backbones) and of OpenMM's implementation
of ff14SB and GBn2; it is a lower bound for the corresponding constant on any superset and
no upper bound for it.  (ii) The certificates of Statement 5 are certificates *given the
measured constants*: the constants were obtained by enumerating the whole domain, which no
user of the theory could afford; nobody has an a-priori upper bound on `c_ij` or `c_ijk` of a
GB term.  What the measurement shows is that such bounds, if proved, would not be vacuous:
the true constants are small where the tables say so.  (iii) The product-space theorems
were applied on a pruned product `X′ ⊂ X_τ`; a certificate over `X′` says nothing about
`X_τ ∖ X′` (of `X_τ`, 0–91 % survives pruning in the Phe instances — nothing for Phe on the
strand at τ = 0.70 from five residues on —, 47–97 % for Lys, 67–84 % for LKSE; 100 % for Ser,
Val, Leu).  (iv) The peptides are small and fully solvent-exposed.  In a protein
interior every atom is descreened by many side chains at once; the Born-radius response
(Statement 8(ii)) and with it `c_ijk` must be expected to be larger there — the literature
reports that pairwise treatments of GB lose accuracy precisely when all side chains are
treated together in folded proteins (§4).  That regime is outside this measurement.

### 2.10 Comparison with workstream P

| quantity | P: backbone torsions (Ala₅, grid A3, 28 843 clash-free conformations, unless noted) | P2: residue rotamers on a fixed backbone (`X′`) |
|---|---|---|
| is `f` pairwise in the site variables? | no: `c_ij(f)` up to 28 at `n = 4`; best pairwise approximation RMS 2.1, sup-optimal 6.1 kcal/mol | yes, exactly (`c_ijk(f) ≤ 2·10⁻¹²`) |
| `max_i c_i(g_GB)` | 9.0, 14.0, 18.6, 22.9, 27.5, 31.6 for `n = 1…6` (`≈ 4.8 + 4.5n`; 12–53 `k_BT`) | neutral: saturates — Val 0.44–0.84, Leu 0.96–1.56, Phe 1.6–4.5, Ser 5.0 / 7.7 / 9.4 (E / P2 / H); charged: grows — Lys/H 10, 37, 52, 56 (`n = 1…4`), ≥ 138 at 24 |
| RMS single-site change | 6.4–6.5 | 0.26–1.4 (Val, Leu, Phe); 1.7–3.4 (Ser); 7–14 (Lys); 6–7 (LKSE) |
| `max c_ij(g_GB)` | 28.8 (slow decay: 8.1 at separation 9) | 0.11–0.51 (Val, Leu); 0.5–1.7 (Phe); 2.1–2.8 (Ser); 19–41 (Lys); 32–78 (LKSE) |
| half row sums `½Σ_j c_ij` | 52–89 | 0.16–1.15 (Val, Leu); 0.8–2.3 (Phe); 3.5–4.9 (Ser); 22–36 (Lys₄) |
| Dobrushin-type sums | ≈ 7 (`n = 4`) | 0.14–0.96 (Val, Leu); 0.7–1.7 (Phe); 2.5–3.2 (Ser); `n − 1` (Lys) |
| distance of `g_GB` to "pairwise in the sites" | all torsion pairs: RMS 2.10, max 13.4; sup-optimal 5.0 at `n = 4` | two-site fit RMS / max: `(2–30)·10⁻⁴` / 0.002–0.03 (Ser, Val, Leu on E, P2; Ser/H at .70); 0.009–0.05 / 0.04–0.2 (Leu/H, Phe, Ser/H at .60); 0.003–0.12 / 0.07–7.8 (Lys); 0.02–0.04 / 0.3–0.4 (LKSE) |
| sharp sites; `λ*` | none in any instance; 0.038 … 0.0026 for `n = 2…6` | all (or all but one) sharp, `λ* = 1.2–18`: Val/E, Val/P2, Leu/E, Leu/H; none or one sharp, `λ* = 4·10⁻⁴–0.17`: Ser, Lys, LKSE at three or more residues |
| first-order certificate of `min E`, ε = 0 | [3 042, 5 357] of 28 843 (11–19 %) | 1 (Val, Leu); [53, 156] of 6 561 (Ser₄/E); [1 361, 2 172] of 17 496 (Ser₅/H); 2 128 of 2 352 (Lys₃/H) |
| second-order star | not computed (row-sum condition fails by 1–2 orders of magnitude) | exact for Val, Leu, Phe/E; ε* = 1.7–32 (Ser), 10–204 (Lys), 13–170 (LKSE) |
| third-order ball | — | exact certificate at τ = 0.70 in every instance (571–2 481 evaluations at `n = 4–6`); at τ = 0.60 off by 0.14–6.7 in three poly-Lys instances |
| Jensen gap against `Σ ln cosh(βc_i/2)` | 2.3 against 178 | 0.02 / 0.7 (Val₁₂/E); 0.99 / 20 (Ser₆/E); 4.6 / 146 (Lys₄/H); 25.7 / 114 (LKSE:6/H) |
| `g_03` (other charge model) | `max c_i` 2.6–4.9, slowly growing; `c_ij` 3.9 → 0.7, not exactly low order; certificate [2, 28] | exactly pairwise; `max c_i` 0.6–5.9 neutral, 9–14 Lys, 9–13 LKSE, not growing; star exact for the apolar peptides, Ser on E and P2, LKSE on H and P2 |
| `g_99` (same-lineage refit) | sum of single-φ terms, `c = 0.64` | sum of one-residue terms, `c_i = 0–2.9` by residue type |

The two workstreams measured different molecules (alanine has no rotamer), so the table
compares *variables*, not numbers one for one.

---

## 3. Numerics: what was computed, sizes, results, how to re-run

All files are in `experiments/science/ws_P2/`; P's modules are imported from `../ws_P`
unmodified (with `sys.dont_write_bytecode`, so nothing is written there).  Run from that
directory with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1` and
`python3 -B`.  Requirements as in P: Python 3.13, numpy, scipy, OpenMM 8.6.1, numexpr.

### 3.1 Model and modelling choices (every one of them)

* **Force fields**: the files shipped with OpenMM 8.6.1 — `amber14/protein.ff14SB.xml`,
  `implicit/gbn2.xml` (`sasaMethod=None`), `amber03.xml`, `amber14/protein.ff15ipq.xml`,
  `amber99sb.xml`; no cutoff, no constraints.  Topologies are generated from the residue
  templates of the ff14SB file (atom order and bonds are read, not typed).
* **Geometry** (`scbuild.py`): P's Z-matrix for the backbone; side chains from a hand-written
  internal-coordinate table (`SIDECHAIN`): χ-driven atoms, sibling substituents at dihedral
  offsets solved from three equilibrium angles, rotors at 180°/±60°, planar groups at 0°/180°.
  Validation (`test_scbuild.py`, 8 systems × 120 states): poly-Ala identical to P's builder
  (difference 0.0 Å); all force-field bonds, including the ring-closure bond of Phe, within
  `7·10⁻¹⁵` Å of equilibrium; all bond angles constant over conformations to `4·10⁻¹³` degrees
  (40–136 of them are off equilibrium by up to 2.6°, 5.1° in Phe, as in P: a Z-matrix cannot
  satisfy all angles at a branched centre); dihedrals recovered to `4·10⁻¹⁵` rad; chiral volume
  at Cα +2.508 Å³ (L); bond energy `< 10⁻²⁵`, angle energy constant to `5·10⁻¹⁴` kcal/mol; net
  charges +3, −3, 0 for KKK, EEE, LKSE.
* **Energies.**  P's `FastFF` works unchanged on these systems: against OpenMM's Reference
  (double precision) platform the largest deviation over all systems is `1.2·10⁻¹¹` kcal/mol
  (GBn2; other components `≤ 6·10⁻¹²`).  For enumeration a second evaluator (`fbmodel.py`)
  uses the fixed-backbone structure: exact one- and two-site tables of every pair-additive
  component, and for GBn2 tabulated descreening integrals (exact Born radii of an assignment
  by table look-ups) followed by a block pair sum.  Validation (`test_fbmodel.py`, 12 systems ×
  200 random assignments): tables against FastFF `≤ 1.1·10⁻¹²`; table GB against FastFF
  `≤ 2.0·10⁻¹²` and against OpenMM's own `CustomGBForce` on the Reference platform
  `≤ 9.3·10⁻¹²` kcal/mol (final block version; the first, straightforward version gave
  `4.5·10⁻¹³` and `8.9·10⁻¹²`, `logs/test_fbmodel_v1.log`).  Every enumeration also spot-checks 24 assignments against FastFF and
  4 against OpenMM's CPU platform (worst deviations over the 140 enumerations: `1.8·10⁻¹¹`
  against FastFF, `7·10⁻⁵` against the single-precision CPU platform).
* **Hydroxyl hydrogen.**  OpenMM's ff14SB gives the type HO (`ε = 0`) a placeholder
  `σ = 1 nm`; with the resulting "radius" of 5.61 Å P's clash score marks every serine state as
  a clash (0.3–0.5).  Atoms with `ε = 0` are given radius 0 in the clash score (Amber's own
  value, from memory); nothing else was changed.
* **Rotamer grid, sites, domains, thresholds**: §2.0.  Table A (`out/tables.md`) lists the
  state counts.  One-site domain sizes of an interior site at τ = 0.70 / 0.60: Ser 9 / 9
  (helix interior 6 / 9), Val 3 / 3 on E and P2 (helix 0–1 / 1), Leu 0 / 2, Phe 2 / 5–7 (helix
  1 / 3), Lys 21 / 31 on E and P2 (helix 7–14 / 22–31), Glu 10–11 / 16–18 (helix 4 / 13).
  Fixed-atom scores of the backbones: H 0.804, E 0.783, P2 0.858.
* **Amendments to the pre-registered design, both forced by geometry and made before any
  constant of the affected systems was computed**: (1) both thresholds are reported because
  Leu (and with it the heteropolymer) is empty at 0.70; (2) the planned two-state grid "R2"
  was dropped (it leaves Leu and Phe with one state); long chains are reached with R3 itself
  where it is small (Val, Leu) and by `an_long.py` otherwise; (3) the interfaces are evaluated
  on the pruned product `X′` after the raw product was found to contain overlapping atoms
  (`NOTES.md`, Step 7).  The backbones H′, E′, P2′ of P's grid, announced as a sensitivity
  check, were not analysed (only Leu₆ on H′ was built, in the validation; §5).
* **Temperature** 300 K.

### 3.2 Scripts and outputs

| script | what | output |
|---|---|---|
| `scbuild.py`, `test_scbuild.py` | side-chain builder (subclass of P's `Peptide`); geometry and energy validation | `logs/test_scbuild.log` |
| `fbmodel.py`, `test_fbmodel.py` | fixed-backbone tables, table-based GBn2, clash decomposition; validation | `logs/test_fbmodel.log` |
| `test_controls.py` | control 3: brute-force check of the constants; synthetic pairwise, random and planted-third-order residuals | `logs/test_controls.log` |
| `enum_fb.py`, `run_enum_R3.sh` | exact enumeration over `∏ D_i(0.60)` | `data/fb_*.npz` (not under version control), `logs/enum_R3_*.log` |
| `anlib.py`, `an_main.py`, `an_batch.py` | constants of order 1, 2, 3, fits, all interfaces; batch driver | `out/an_*.json`, `logs/an_batch_*.log` |
| `make_tables.py`, `dump_sel.py` | tables from the JSON files | `out/tables.md` |
| `an_cover.py`, `run_cover.sh` | first-order covers (P's `an7`, generalised) | `out/cover_*.json`, `logs/cover.log` |
| `an_ball_pairwise.py` | Statement 5(d) | `logs/ball_pairwise.log` |
| `an_mech.py`, `run_mech.sh` | Statement 8 | `out/mech_*.json`, `logs/mech.log` |
| `an_long.py`, `run_long.sh`, `run_long2.sh` | long chains: exact constants of pair-additive residuals, lower bounds for GB | `out/long_*.json`, `logs/long*.log` |
| `an_perchi.py` | Statement 1(c) | `logs/an_perchi.log` |
| `verify_openmm_direct_sc.py` | end-to-end check with OpenMM's own forces and explicit loops (§3.3, item 4) | `logs/verify_openmm_direct_sc.log` |

To re-run everything: `python3 -B test_scbuild.py; python3 -B test_fbmodel.py; python3 -B
test_controls.py; python3 -B verify_openmm_direct_sc.py; for b in H E P2; do bash run_enum_R3.sh $b; python3 -B an_batch.py $b R3;
done; bash run_cover.sh; bash run_mech.sh; bash run_long.sh; bash run_long2.sh; python3 -B
make_tables.py R3 > out/tables.md`.

**Sizes.**  140 enumerated models with 8 476 447 assignments in all (each one an exact GB
evaluation), analysed at two thresholds: 280 instance analyses, 217 of them non-empty; largest
enumerations 923 521 (Lys₄ on E and on P2), 622 728 (LKSE:6/P2), 553 536 (LKSE:6/E), 531 441
(Ser₆ on three backbones, Val₁₂ on two), 465 124 (Lys₄/H).  The 29 long-chain runs add
237 929 evaluations, the 12 mechanism runs 431 264.  GB cost: 24 ns per atom pair (75 µs for
78 atoms, 0.6 ms for 204 atoms) on an idle core; the machine was shared (load 8–16 on 4 cores), so wall-clock times in the logs are 3–6
times longer.  Wall-clock time summed over the single-thread jobs (from the logs): 2.4 h of
enumeration, 2.0 h of analysis, 0.8 h of long-chain runs, 0.3 h of covers.  Data: `data/`
(584 MB of `.npz`, not under version control) holds the grids.

### 3.3 Controls (items 1–3 before any measurement; items 4–5 afterwards)

1. **P's end-to-end check reproduced** (`ws_P/verify_openmm_direct.py`, run from my directory
   without writing into `ws_P`): 508 clash-free conformations, `c_i = 16.09 12.41 18.63 16.43
   15.14 11.19` (`logs/control_P_verify.log`).
2. **Builder and evaluators**: §3.1 (`5·10⁻¹²`-level agreement with OpenMM's Reference
   platform, as P reached).
3. **Synthetic residuals** (`test_controls.py`): the routines agree with brute-force loops on
   random masked grids to `7·10⁻¹⁶` at orders 1, 2, 3; an exactly pairwise random residual gives
   `c_ijk = 3·10⁻¹⁵ … 2·10⁻¹⁴` and a two-site remainder of `3·10⁻¹⁵` (full grid), `≤ 3·10⁻¹¹`
   (masked domain, LSQR), Chebyshev remainder 0; an i.i.d. random residual gives `c_ijk` of
   24–52 (function standard deviation 2.5–4.7) and a two-site remainder of 0.8–0.97 standard
   deviations; a planted term `0.37·[x₀=1][x₁=0][x₂=2]` is recovered as `c_ijk = 0.3700` exactly
   (Chebyshev two-site remainder 0.0463 = 0.37/8); the bounds of Theorems 11.16 and 11.18 hold
   on all random instances.
4. **Independent end-to-end check of the central numbers** (`verify_openmm_direct_sc.py`, the
   analogue of P's script): Ser₃ on the strand, all 729 assignments, `g_GB` from OpenMM's own
   `CustomGBForce` on the Reference platform and `f` from OpenMM's torsion and nonbonded force
   groups, coordinates from the full internal-coordinate build, constants by explicit loops —
   without P's evaluator, without my tables and without `anlib`: `c_i(g_GB) = 4.81 4.12 4.32`,
   `c_12, c_13, c_23 = 1.306 2.426 1.308`, `c_123(g_GB) = 4.03·10⁻³`, `c_123(f) = 6·10⁻¹³` kcal/mol.
   The pipeline gives the same numbers to all printed digits.
5. *Internal consistency on the real data*: `c_ijk` of every pair-additive function
   `≤ 2·10⁻¹²`; the measured star and ball remainders never exceed their bounds (2 377
   comparisons over all residuals and both centres, no violation); the lower bounds of
   `an_long.py` reproduce the exact constants in the case where both were computed (Lys₄/H).

### 3.4 Full tables

`out/tables.md`: A (domains), B (`max c_i` by `n` for `g_GB`, `coul+g_GB`, `g_03`, `g_ipq`,
`g_99`), C (second and third order), D (interfaces for four residuals: 722 rows), E (decay
with distance).

---

## 4. Prior art, with a search log

Based on articles retrieved from PubMed.  Reading level of every item: **[abstract]** (the
PubMed record, through the literature tool); nothing was read in full.  Bibliographic details
and DOIs are those of the PubMed records.

| # | query (PubMed) | hits | kept (PMID) |
|---|---|---|---|
| 1 | `generalized Born pairwise protein design` | 13 | 16853951, 28749575, 24854675, 26948696, 28886244, 17348031, 41055950 |
| 2 | `pairwise decomposable Poisson-Boltzmann protein design` | 2 | 15802649, 18074340 |
| 3 | `residue-pairwise generalized Born` | 4 | (subset of 1) |
| 4 | `LUTE local unpruned tuple expansion` | 1 | 27681371 |
| 5 | `cost function network protein design guaranteed discrete energy optimization` | 0 | — |
| 6 | `partition function provable approximation side-chain rotamer K* algorithm` | 0 | — |
| 7 | `Simoncini Schiex guaranteed discrete energy optimization` | 1 | 26610100 |
| 8 | `Donald BR[Author] partition function provable approximation` | 2 | 31855059 |

Most of this literature is about sequence design, which is outside our scope; it is cited
only for what it says about the decomposability of solvation energies and about exact solvers
for pairwise rotamer models.

**What is known about pairwise decomposability of generalized-Born energies [K, abstract].**
* That GB is many-body and that practical side-chain placement needs it pairwise is the
  starting point of a line of work by Simonson, Archontis and co-workers: Archontis &
  Simonson, *J Phys Chem B* 109:22667 (2005), [doi:10.1021/jp055282+](https://doi.org/10.1021/jp055282+) ("the interaction energy
  between two amino acids depends on the whole protein structure, but can be accurately
  computed from residue-pairwise information"); Gaillard & Simonson, *J Comput Chem* 35:1371
  (2014), [doi:10.1002/jcc.23637](https://doi.org/10.1002/jcc.23637) (the GB term's "many-body character is overcome using an
  effective dielectric environment"; "the error remains reasonable, compared to other
  uncertainties"); Villa, Mignon, Polydorides & Simonson, *J Comput Chem* 38:2396 (2017),
  [doi:10.1002/jcc.24898](https://doi.org/10.1002/jcc.24898) ("GB is a many-body potential"; the usual simplification is "a mean,
  native-like protein/solvent boundary, which removes the many-body property"; their
  fluctuating-boundary treatment is "numerically exact (within the GB framework)" at
  "residue-pairwise complexity"); Gaillard, *J Phys Chem B* 129:10699 (2025),
  [doi:10.1021/acs.jpcb.5c03662](https://doi.org/10.1021/acs.jpcb.5c03662) (extension "allowing an exact decomposition of the GB term").
* That the pairwise approximation costs accuracy when all side chains move: Gaillard, Panel &
  Simonson, *Proteins* 84:803 (2016), [doi:10.1002/prot.25030](https://doi.org/10.1002/prot.25030) ("For the prediction of all side
  chains, however, errors due to the pairwise additive approximation overcome the improvement
  brought by these terms"); Gaillard & Simonson, *JCTC* 13:4932 (2017),
  [doi:10.1021/acs.jctc.7b00202](https://doi.org/10.1021/acs.jctc.7b00202) (the GB term "is affected by pairwise decomposition errors when
  all positions are designed together").
* Poisson–Boltzmann: Marshall, Vizcarra & Mayo, *Protein Sci* 14:1293 (2005),
  [doi:10.1110/ps.041259105](https://doi.org/10.1110/ps.041259105) (one- and two-body decomposable finite-difference PB; desolvation of
  polar side chains "0.64 kcal/mol RMSD" against the full calculation, screened Coulomb
  between side chains "0.13 kcal/mol"); Vizcarra et al., *J Comput Chem* 29:1153 (2008),
  [doi:10.1002/jcc.20878](https://doi.org/10.1002/jcc.20878) (explicit "two-body perturbations to the dielectric environment").
* Side-chain placement with implicit solvent: Lopes et al., *Proteins* 67:853 (2007),
  [doi:10.1002/prot.21379](https://doi.org/10.1002/prot.21379) ("the electrostatic model is not important for sidechain placement";
  "the recent discovery of efficient, pairwise implementations of GB").
* General non-pairwise energies as tuple expansions: Hallen, Jou & Donald, *J Comput Biol*
  24:536 (2017), [doi:10.1089/cmb.2016.0136](https://doi.org/10.1089/cmb.2016.0136) (LUTE: a fitted local expansion in tuples of
  rotamers representing "general, possibly nonpairwise energy functions to an arbitrary level
  of accuracy").
* Exact solvers for the pairwise problem and provable partition functions: Simoncini et al.,
  *JCTC* 11:5980 (2015), [doi:10.1021/acs.jctc.5b00594](https://doi.org/10.1021/acs.jctc.5b00594) (proven global minima of
  pairwise-decomposable rotamer models on spaces "of size up to 10²³⁴"); Jou, Holt, Lowegard &
  Donald, *J Comput Biol* 27:550 (2020), [doi:10.1089/cmb.2019.0315](https://doi.org/10.1089/cmb.2019.0315) ("provable ε-approximations
  to partition functions" for pairwise energy bounds).

**How this report relates to it.**  Consistent with the literature: GB is many-body through
the radii; a mean-environment (frozen-radius) pair model is a usable first approximation;
its error is carried by the response of the dielectric boundary (my `g_fluct`).  What I did
not find in these abstracts, and therefore do not claim to be absent from the literature: a
*supremum-norm* measurement, over a completely enumerated domain, of the distance of a GB
energy to the pairwise class in rotamer variables; mixed third-difference constants; or the
observation that the Born-radius response is itself pairwise to high accuracy for exposed
side chains, so that the *best* pairwise function (as opposed to a mean-environment
construction) is far closer than the frozen-radius one (over the domains of Statement 8
`g_fluct` varies by 3–68 kcal/mol where the two-site remainder is at most 0.002–1.1 kcal/mol).
None of this is a claim of novelty: the search was eight queries read at abstract level.  The quoted error figures of the
literature are RMS or mean errors of specific constructions on folded proteins; mine are
exact maxima for small exposed peptides.  The two are not comparable and the difference in
setting (exposure) is the most likely reason why mine are smaller [H].

---

## 5. What I did not settle

1. **Buried environments.**  All peptides are isolated and exposed; the brief's scope
   (homopolymers and one patterned heteropolymer on ideal single-chain backbones) excludes a
   folded core.  Whether `c_ijk(g_GB)` stays at `10⁻²–10⁻¹` kcal/mol where each atom is
   descreened by many side chains is the open question that decides the practical value of
   Statement 5(c).
2. **Upper bounds.**  No constant was bounded from above for a class of molecules or for
   continuous χ.  The long-chain numbers for GB are lower bounds.
3. **Asymptote of the charged case.**  Poly-Lys constants are still rising at 24 residues;
   I have a heuristic `r⁻²` argument for slow saturation in a one-dimensional arrangement, no
   measurement of the plateau, and no three-dimensional arrangement of charges.
4. **Rigid geometry and the grid.**  Three staggered states per dihedral, no relaxation.
   Leucine has no state at τ = 0.70; valine none in the helix interior.  A rotamer library
   with relaxed geometry would change domains and excitation energies; constants are lower
   bounds for finer grids.
5. **Non-product domains.**  The second- and third-order theorems were applied on a greedily
   pruned product; the pruning rule is one of many, and for Phe on the strand at τ = 0.70 it
   leaves nothing from five residues on.  I did not develop a version of the star sandwich
   for the non-product `X_τ`.
6. **Sensitivity backbones.**  P's grid basins H′, E′, P2′ were not analysed; three
   backbones only.  The dependence on the backbone is strong for Ser (5.0 / 7.7 / 9.4).
7. **Other residuals.**  ACE surface term, OBC2, Poisson–Boltzmann, quantum or learned
   corrections: not done.  ff19SB − ff14SB should be constant on a fixed backbone (its CMAP
   terms depend on `(φ, ψ)` only) — not computed.
8. **Per-χ sites, larger alphabets.**  Only shown not to be pairwise; no constants measured.
9. **The ball beyond eight sites** was not evaluated by enumeration (the third-order
   constants are available to `n = 16`, the lower-model minimisation only to `n = 8`).
10. **Prior art** was read at abstract level only.
11. **The large third-order constant of Lys₄ on PPII** (2.4 kcal/mol at τ = 0.70, 10.2 at
    0.60, triple of residues 1, 2, 4) was located but not dissected: which states realise it,
    how much of it is due to the strained states that the relaxed threshold admits, and
    whether it persists with relaxed geometry.

---

## 6. The three most promising next steps

1. **The same third-order measurement in a buried environment** (a small folded
   fixed-sequence structure, public coordinates, backbone fixed, rotamers from a public
   library; exact for windows of 4–6 neighbouring sites with the rest at a reference, plus
   lower bounds as in `an_long.py`).  It decides whether "GB is pairwise in the rotamers to
   `10⁻¹` kcal/mol in sup norm" is a property of exposed peptides or of side-chain placement
   in general; the code needs only a backbone from coordinates instead of from `(φ, ψ)`.
2. **A proved bound on the third-order constants of GB** — the missing input of Statement 9.
   The structure found in Statement 8 suggests the route: `g_GB = g_frozen` (pairwise,
   computable) `+` a function of the Born radii, and the descreening integral `I_p` of every
   atom is *exactly* a sum of one-site tables (backbone atoms: `I_p = I_p⁰ + Σ_i A_i^p(x_i)`) or
   of one- and two-site tables (side-chain atoms) — these are the tables `fbmodel.py` builds;
   the third-order mixed difference of a smooth function of such sums is bounded by its
   derivatives up to third order times products of the tabulated ranges.  An interval evaluation of that expression
   would give certified `c_ijk` (and `c_ij(g_fluct)`) for a given backbone without
   enumeration — the first certified class constants for a real many-body term.
3. **Run the third-order certificate end to end with the existing kernels**: the pairwise
   lower model `L₃` of Statement 5(d) is an ordinary pairwise instance with rational tables;
   feeding it to the theory division's tropical kernel and an exact pairwise solver, with the
   1 009 GB evaluations of Ser₆ as anchors, would be the first certificate in the programme
   whose residual is a real solvation term — conditional only on the third-order constants,
   which step 2 would certify.

---

## 7. Requests

### To the theory division

**T-1 (third order with a pairwise kernel).**  Statement 5(d): for constants `c_T`, `|T| = 3`,
and `γ_i = ⅓Σ_{T∋i} c_T`, the model `f + I₂g − Σ_i γ_i[x_i ≠ x₀_i]` is a pairwise lower bound of
`E`.  Please state and machine-check this corollary of `higherOrder_remainder` together with
soundness of the pairwise kernel on it (the analogue of `verify_sound_secondOrder`).  The
same counting gives a two-body penalty that is never larger and still pairwise:
`Σ_{T ⊆ S} c_T ≤ Σ_{i<j ∈ S} β_ij` with `β_ij = ⅓Σ_k c_ijk` (each triple inside `S` contains three
pairs of `S`) [P, not evaluated numerically here].  Measured input: on Ser₆ (531 441
assignments) `γ_i ≤ 0.011` kcal/mol against excitation energies 1.0–1.1; on Lys₄/PPII
`γ_i = 0.2–0.95` against 1.0–2.1.

**T-2 (the right sufficient condition for a pairwise known part).**  The row-sum condition
of §11.7 is stated for an additive known part.  For pairwise `f` the exact criterion is that
`x₀` minimises `f + g_star − W`; a sufficient site-wise condition must involve the mixed
differences of `f` at `x₀`.  On the measured instances the plain condition is violated while
the exact criterion holds in 13 cases (e.g. Leu₁₆ on the helix: half row sum 0.58 against an
excitation energy of 0.52 at one N-terminal site), and the natural pairwise generalisation
`Δ_i(a) ≥ ½Σ_j max_b (c_ij − M^f_ij(a, b))₊` is far from necessary.  Is there a condition of
maximum-density type (theory report Theorem 11.32(v)) that is checkable in `O(n²k²)` and
tight on such instances?

**T-3 (product-space theorems on domains with pairwise exclusions).**  Real rotamer domains
are products minus pairwise-excluded combinations (two-site clashes).  The star sandwich was
applied here on a pruned product.  Is `|g − g_star| ≤ Σ c_ij` valid on `X_τ` when the constants
are taken over `X_τ` and every hybrid of `x` and `x₀` that the proof visits can be routed
through `X_τ` (a connectivity condition on the conflict graph)?  If not, what is the correct
remainder?

**T-4 (splitting off a known long-range pair term).**  For charged side chains the first-
and second-order constants of `g_GB` are dominated by a pair term that is known in closed
form (Statement 8).  The theory treats the split `E = f + g` as given.  Please record the
trivial but consequential monotonicity: for any pairwise `p`, replacing `(f, g)` by
`(f + p, g − p)` leaves `c_ijk` unchanged and changes `c_i`, `c_ij` — so the cost of the star
depends on the split while that of the ball does not.

### To the engineering division

**E-1 (specification: third-order constants of a solvation residual in a buried
environment).**
*Motivation.*  §6 item 1; decides whether Statement 5(c) survives burial.
*Formulation.*  Fixed sequence and fixed backbone coordinates of a small public folded
structure (taken as is); rotamers from a public library (3–9 per residue, relaxed geometry);
`f` = ff14SB tables, `g` = GBn2 polarisation energy; domain = pruned clash-free product as in
`an_main.pruned_product`.
*Inputs.*  `fbmodel.py` (replace the coordinate builder by a reader; everything downstream —
tables, descreening integrals, `gb_energy`, `anlib.mixed` — is independent of how the
coordinates were made).
*Outputs.*  For every triple of mutually contacting sites (Cβ–Cβ < 8 Å): exact `c_ijk` with
all other sites at the reference, and lower bounds with the others at random states; `c_ij`
by distance; `γ_i`; excitation energies; the ball certificate of a window of 6–8 sites by
enumeration.
*Validation.*  Reproduce Ser₄ on the strand from this report: `c_i = 4.90 4.66 4.65 4.34`,
`c_ij` matrix with entries 1.31, 2.42, 0.33, `max c_ijk = 0.0042`, two-site Chebyshev
remainder 0.0008 kcal/mol.
*Stopping conditions.*  Stop when `γ_i` is known for 20 buried sites; report the fraction
with `γ_i` below the local excitation energy.
*Resources.*  `k³` GB evaluations per triple at 24 ns per atom pair and evaluation (table-based
evaluator of this report): minutes.

**E-2.**  If the kernels accept pairwise instances with 6 sites × 9 states, run Statement
5(d) for Ser₆ end to end (tables from `fbmodel.site_tables`, anchors = the 1 009 ball values,
penalties `γ_i` from `out/an_fb_S6_E_R3_t0.60_tau0.70.json`) and return the certificate size
and checking time.
