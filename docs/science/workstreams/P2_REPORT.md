# Workstream P2 (science division) — class constants of a real residual in rotamer variables on a fixed backbone

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
property; the sequences were fixed before any constant was computed (`NOTES.md`, Step 2).

---

## 1. Verdicts in one paragraph

*(written last; see the end of §2 for the comparison table with P)*

VERDICT_PLACEHOLDER

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
χ₁χ₂χ₃; Lys χ₁…χ₄.  Grid **R3**: every dihedral ∈ {−60°, 180°, +60°} (3, 9, 9, 9, 27, 81
states for Val, Leu/Phe, Ser, —, Glu, Lys).

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

The theorems for product spaces (star sandwich etc.) are applied on `X′` only; constants and
fits are reported on `X_τ` and on `X′`.  Thresholds: τ = 0.70 (P's) and τ = 0.60 (P's
sensitivity value; "relaxed").  Both are needed because of a geometric fact of the rigid model
[M]: **at τ = 0.70 leucine has no admissible rotamer on any backbone** (its two best R3 states,
`(180°, 60°)` and `(−60°, 180°)` — the two rotamers known as dominant — score 0.645 and 0.633,
limited by an intra-residue H···H contact of 1.82–1.85 Å), valine has a single state in the
helix interior, and at τ = 0.80 every residue type except serine is empty (§3.1, Table A).

**Energies.**  Known part `f` = ff14SB vacuum energy (torsions + Lennard-Jones + Coulomb; bond
and angle terms are constant by construction).  Residuals:

| symbol | definition |
|---|---|
| `g_GB` | GBn2 polarisation energy (`ε_in = 1`, `ε_out = 78.5`, no salt, no surface term) — P's `g_GB` |
| `g_03`, `g_ipq`, `g_99` | vacuum energy of ff03, ff15ipq, ff99SB minus that of ff14SB at identical coordinates |
| `coul + g_GB` | alternative split: residual = vacuum Coulomb + GB ("solvated electrostatics"), known part = torsions + Lennard-Jones |
| `g_frozen`, `g_fluct` | `g_GB` evaluated with the Born radii frozen at their values in `argmin f`; `g_fluct = g_GB − g_frozen` (§2, Statement 8) |

**Constants** (as in `SP_REPORT.md` §2, on a domain `D`): `c_i(g)` = max `|g(x) − g(x′)|` over
pairs in `D` differing in site `i` only; `c_ij(g)` = max of the mixed second difference
`|g(x^{ab}) − g(x^{a′b}) − g(x^{ab′}) + g(x^{a′b′})|` over quadruples in `D`; new here:
`c_ijk(g)` = max of the mixed third difference over octuples in `D`.

STATEMENTS_PLACEHOLDER
