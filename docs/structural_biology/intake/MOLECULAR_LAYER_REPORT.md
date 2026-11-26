# STRUCTBIO molecular model layer — implementation report

Date: 2026-11-26.  Branch `research/structural-biology` (working tree, uncommitted).  Code:
`src/metricchain_sb/molecular/` (`prepare.py`, `chi.py`, `rotamers.py`, `tables.py`,
`reference.py`, `__init__.py`).  Tests: `tests/structbio/test_molecular.py`.  Data:
`benchmarks/structbio/pdb/` (+ `MANIFEST.json`).

**What this is.** A fixed-backbone, fixed-sequence discrete side-chain model built from a
deposited structure, with an energy that is pairwise decomposable *by construction*, and an
independent check that the tables reproduce a full-system OpenMM energy of the same model.  It
is a model conditional on Amber ff14SB, a distance-dependent dielectric, in vacuo, an idealised
rotamer library and rigid chi rotation.  It is **not** a model of the protein in water, and
nothing in this report is a statement about nature.

## 1. The model (complete definition; sufficient for re-implementation)

### 1.1 Structure preparation (`prepare.py`)
1. Read with `openmm.app.PDBFile` (OpenMM 8.6.1): first model, first alternate location
   (verified: 2IGD Glu20 CG takes the `A` coordinates).  OpenMM renames atoms to PDB v3 names.
2. Keep one protein chain (`chain_id`, default: the first chain containing a standard amino
   acid).  Keep only residues of that chain with one of the 20 standard names; drop waters,
   ligands, ions and other chains.
3. Fail closed (`StructureRejected`) if: an ATOM-record residue of the chain, or a SEQRES
   entry, is not one of the 20 standard residues; the SEQRES length differs from the number of
   residues observed (missing residues, terminal or internal); a C(i)–N(i+1) distance exceeds
   2.0 Å (chain break); any expected heavy atom is missing (backbone N, CA, C, O; the standard
   side chain; OXT on the last residue) or an unexpected heavy atom is present.
4. Delete every hydrogen/deuterium in the input, then
   `Modeller.addHydrogens(ForceField('amber14-all.xml'), pH=7.0, platform=Reference)`.  This
   sets termini (NH3+, COO−), histidine tautomers (from OpenMM's H-bond heuristic) and
   protonation states.  **Note:** `addHydrogens` itself places the new hydrogens at random
   positions (Python `random`) and then minimises *only the added hydrogens*
   (`LocalEnergyMinimizer`, tolerance 1.0 kJ/mol/nm, 50 iterations, heavy atoms immobile,
   ff14SB with CutoffNonPeriodic).  We seed Python's `random` with the `seed` argument (global
   state restored afterwards) and force the Reference platform, so preparation is bit-for-bit
   reproducible (tested).  Before seeding was added, two builds of 1CRN gave different
   hydrogen positions and unary energies differing by up to ~70 kcal/mol for the same library
   state — this was a real reproducibility defect, now fixed.
5. Heavy-atom coordinates are checked to be bit-identical before and after hydrogen addition.
   No minimisation of heavy atoms, no other coordinate change.
6. `repair_with_pdbfixer=True` (off by default; pdbfixer 1.12.0 installed) lets PDBFixer add
   missing heavy atoms only (never residues, never residue replacement); the added atoms are
   listed in `meta.preparation.pdbfixer_added_atoms` and `repaired_with_pdbfixer` is set.  Not
   used for any structure in this report.
7. ff14SB System: `createSystem(NoCutoff, constraints=None, rigidWater=False,
   removeCMMotion=False)`.  The table builder requires exactly the force set {HarmonicBond,
   HarmonicAngle, PeriodicTorsion, NonbondedForce(NoCutoff)} and raises otherwise.

### 1.2 Flexible sites
A residue is a site iff it has ≥ 1 chi (table below) and it is not PRO (ring closes on the
backbone N) and not a cysteine whose SG is bonded to another residue's SG (CYX).  GLY/ALA have
no chi.  **Judgement call:** chain-terminal residues are sites like any other — their
terminal groups (H1/H2/H3, OXT) are backbone atoms, never move, and need no special template
handling.  Everything else is background.

Moving atoms S_i: all atoms reachable from CB in the bond graph without passing through CA,
excluding CB (CB's hydrogens do move).  For chi k with atoms (a,b,c,d), the atoms rotated are
those reachable from c without passing through b, excluding c; if b is reachable another way
(a ring) the code raises.  A state is made from the prepared coordinates by, for k = 1, 2, …,
measuring chi_k and rotating its distal atoms about the axis b→c by (target − measured)
(Rodrigues, right-hand rule; positive rotation increases the IUPAC dihedral).  Rotating chi_k
leaves chi_<k unchanged (the four atoms of an earlier chi move rigidly together or lie on the
axis), so all targets are met exactly.  Bond lengths/angles are those of the prepared structure.

Chi definitions (`chi.py`, IUPAC; dihedral positive = clockwise viewed along b→c):

| res | chi1 | chi2 | chi3 | chi4 |
|---|---|---|---|---|
| SER | N-CA-CB-OG | | | |
| CYS | N-CA-CB-SG | | | |
| THR | N-CA-CB-OG1 | | | |
| VAL | N-CA-CB-CG1 | | | |
| ILE | N-CA-CB-CG1 | CA-CB-CG1-CD1 | | |
| LEU | N-CA-CB-CG | CA-CB-CG-CD1 | | |
| ASP | N-CA-CB-CG | CA-CB-CG-OD1 | | |
| ASN | N-CA-CB-CG | CA-CB-CG-OD1 | | |
| HIS | N-CA-CB-CG | CA-CB-CG-ND1 | | |
| PHE, TYR, TRP | N-CA-CB-CG | CA-CB-CG-CD1 | | |
| MET | N-CA-CB-CG | CA-CB-CG-SD | CB-CG-SD-CE | |
| GLU, GLN | N-CA-CB-CG | CA-CB-CG-CD | CB-CG-CD-OE1 | |
| LYS | N-CA-CB-CG | CA-CB-CG-CD | CB-CG-CD-CE | CG-CD-CE-NZ |
| ARG | N-CA-CB-CG | CA-CB-CG-CD | CB-CG-CD-NE | CG-CD-NE-CZ |
| PRO (not a site) | N-CA-CB-CG | CA-CB-CG-CD | | |
| GLY, ALA | — | | | |

Hydroxyl, thiol and amine hydrogen orientations (Ser HG, Lys HZ*, …) are not degrees of
freedom: they move rigidly with the last chi, as placed by `addHydrogens`.

### 1.3 Rotamer states ("idealised staggered library", `rotamers.py`)
sp3–sp3 chi: {−60, 180, +60}°.  Other values (°):

| chi | values | rationale |
|---|---|---|
| PHE, TYR chi2 | {90, 0} | ring flip: period 180, values distinct mod 180 |
| TRP chi2 | {−90, 0, 90} | as specified |
| HIS chi2 | {−90, 90, 0} | as specified |
| ASN chi2, GLN chi3 | {−120, −60, 0, 60, 120, 180} | amide has no symmetry (O vs N): full circle, 60° grid |
| ASP chi2, GLU chi3 | {−60, 0, 60} | carboxylate: OD1/OD2 (OE1/OE2) have identical ff14SB types and charges, so period 180; values distinct mod 180 |
| ARG chi4 | {−90, 90, 180} | NE is sp2; 0 omitted (eclipsed CG/CZ) |
| MET chi3 | staggered | S treated as sp3 |

States of a site = [native] + Cartesian product over chis in chi order (values in the order
above).  Native = prepared coordinates, chi angles as measured, always index 0.  Resulting
state counts: SER/CYS/THR/VAL 4; PHE/TYR 7; ILE/LEU/ASP/HIS/TRP 10; ASN 19; MET/GLU 28;
GLN 55; LYS/ARG 82.  A library state may coincide geometrically with the native one; no
de-duplication is done.  `max_states_per_site=m` keeps **m states in total**: the native state
plus the m−1 library states of lowest *unclipped* self energy U_i (stable sort, ties by library
order), then kept in library order; recorded in `meta.max_states_per_site`.
`include_native=False` omits the native state (then `max_states_per_site` keeps the m lowest).

### 1.4 Energy (kcal/mol, `tables.py`)
Parameters: whatever OpenMM's ForceField assigns to the hydrogenated structure (per-atom q, σ,
ε; NonbondedForce exceptions; PeriodicTorsionForce terms, propers and impropers).  For atoms
p, q at distance r (Å):

    e_pq(r) = 4 ε_pq [(σ_pq/r)^12 − (σ_pq/r)^6] + C · qq_pq / (ε0 · r²)

* ordinary pairs: qq = q_p q_q, σ = (σ_p+σ_q)/2, ε = √(ε_p ε_q) (Lorentz–Berthelot);
* pairs in the NonbondedForce exception list: the exception's (chargeProd, σ, ε) — for 1-2 and
  1-3 pairs these are zero (excluded); for 1-4 pairs ff14SB gives chargeProd = q_p q_q/1.2 and
  ε scaled by 0.5;
* C = ONE_4PI_EPS0 · 10 / 4.184 with ONE_4PI_EPS0 = **138.93545764438198 kJ mol⁻¹ nm e⁻²**,
  read at run time from a two-charge OpenMM NonbondedForce, so C = **332.0637132991921
  kcal mol⁻¹ Å e⁻²**; ε(r) = ε0 · r/Å, ε0 = 4.0 by default (argument);
* no cutoff, no solvent, no periodicity.

Decomposition, with B = all atoms in no S_i:

    E(x) = E_const + Σ_i U_i(x_i) + Σ_{i<j} P_ij(x_i, x_j)
    U_i(a)   = Σ torsion terms k(1+cos(nφ−φ0)) with ≥ 1 atom in S_i
             + Σ_{p<q ∈ S_i(a)} e_pq + Σ_{p∈S_i(a), q∈B} e_pq
    P_ij(a,b)= Σ_{p∈S_i(a), q∈S_j(b)} e_pq

E_const (fixed-atom torsions, bonds, angles, B–B nonbonded) is not computed and is stored as
0.0.  The builder raises if a torsion or an exception couples moving atoms of two sites (never
happened: sites are ≥ 4 bonds apart once CYX and PRO are fixed).  Bonds and angles are
invariant under chi rotation; checked numerically (§3: spread ≤ 6.3e−12 kcal/mol) and omitted.
All pairs i<j are stored as dense float64 tables (no distance cutoff).  Distances are computed
as direct coordinate differences (not the |a|²+|b|²−2ab expansion) to keep precision.

**Clipping.** With `e_clip` (default 1000 kcal/mol), `unary`/`pair` = min(entry, e_clip) after
construction; `unary_unclipped`/`pair_unclipped` keep the model values and are the ones
validated.  Clipping changes the model (it is no longer the ff14SB energy for clashing
states); counts in `meta.clipping`.

## 2. API
`build_energy_tables(pdb_path, chain_id=None, eps0=4.0, e_clip=1000.0,
max_states_per_site=None, include_native=True, seed=0, repair_with_pdbfixer=False)` →
`EnergyTables(unary, pair, unary_unclipped, pair_unclipped, meta, model)`;
`table_energy(x, clipped=True)`; `save_energy_tables(t, prefix)` writes `<prefix>.json`
(meta, `format: structbio-energy-tables/1`) and `<prefix>.npz` (`unary_<i>`,
`unary_unclipped_<i>`, `pair_<i>_<j>`, `pair_unclipped_<i>_<j>`); `load_energy_tables(prefix)`.
`openmm_reference_energy(model, configs, group=0, platform='Reference')` → kcal/mol;
`validate_against_openmm(t, n_random=20, seed=0, n_clash_free=20, window=10.0)`.

Deviations from the requested API, both additive: (i) `EnergyTables.model` (default `None`,
not persisted, `None` after `load_energy_tables`) holds the prepared structure and the state
coordinates needed by the validation; (ii) the keyword `repair_with_pdbfixer`.  `seed` seeds
the hydrogen placement (§1.1.4); nothing else is random.

## 3. Independent validation (`reference.py`)
Reference System built from OpenMM force objects only, evaluated by OpenMM on the Reference
platform (double precision) on full coordinates: group 0 = a copy of the PeriodicTorsionForce
(all torsions) + CustomNonbondedForce `4*eps*((sig/r)^12-(sig/r)^6) + C*q1*q2/(eps0*10*r^2)`
(r in nm; LB combining; NoCutoff; every exception excluded) + CustomBondForce with the same
expression and per-bond (chargeProd, σ, ε) for each exception with nonzero chargeProd or ε;
group 1 = copies of HarmonicBond/HarmonicAngle forces.  No table code is used; only the
parameters and the constant C are shared.  Reference configuration x_ref = all-native.
Compared: ΔE_OpenMM(x) = E(x) − E(x_ref) vs ΔE_table (unclipped).

Configurations per structure (seed 0): 21 "random" (x_ref + 20 uniform random states per
site) and 21 "clash-free" (ICM descent on the unclipped tables from native, then 20 distinct
configurations of a seeded single-site random walk from the ICM minimum restricted to
E_table ≤ E_table(native) + 10 kcal/mol).  "Clash-free" here means low table energy; the
minimum r/σ_pq over LJ-active non-excluded pairs with a moving atom is reported as a
diagnostic (the native structures themselves have 0.67–0.79, i.e. some 1-4/H-bond-type contacts
are below σ in ff14SB).

Mutation checks (1CRN, clash-free set): giving the reference ε0 = 8 instead of 4 yields
max |diff| = 1.95 kcal/mol; dropping the 1-4 CustomBondForce yields 4.79 kcal/mol.  The test
therefore detects errors of the kinds that matter.

| PDB | random: max abs diff | max rel diff | max ‖ΔE‖ | max |diff|/(1e−9‖ΔE‖+1e−6) | clash-free: max abs diff | clash-free ΔE range | min r/σ (clash-free) | bonded spread |
|---|---|---|---|---|---|---|---|---|
| 1CRN | 17.2 | 1.9e−13 | 9.0e13 | 1.9e−4 | 5.4e−12 | −2.3 … 9.9 | 0.759 | 1.4e−12 |
| 1UBQ | 7.7e6 | 1.9e−13 | 5.9e20 | 1.9e−4 | 3.6e−11 | −129.7 … 9.9 | 0.575 | 3.5e−12 |
| 2IGD | 3.6e3 | 2.2e−13 | 3.7e16 | 2.2e−4 | 7.6e−12 | −11.6 … 9.6 | 0.672 | 2.0e−12 |
| 5PTI | 8.8e4 | 9.1e−14 | 2.7e18 | 9.1e−5 | 1.1e−11 | −28.8 … 8.6 | 0.717 | 3.1e−12 |
| 1PGA | 3.6e4 | 4.6e−13 | 7.8e16 | 4.6e−4 | 1.2e−11 | −35.7 … 9.9 | 0.643 | 2.8e−12 |
| 1BPI | 144 | 2.1e−13 | 1.7e15 | 2.1e−4 | 5.0e−12 | −24.0 … 9.3 | 0.630 | 6.3e−12 |

(kcal/mol.)  Random configurations reach 1e13–6e20 kcal/mol (near-coincident atoms, min r/σ
down to 0.017), far above the 1e3–1e9 anticipated; agreement is at the double-precision
round-off level (relative ≤ 4.6e−13), every configuration passes |diff| ≤ 1e−9|ΔE| + 1e−6 with
a margin ≥ 2000×, and the clash-free sets agree to ≤ 3.6e−11 kcal/mol absolute.  No tolerance
was loosened.  The 1UBQ ICM minimum lies 130 kcal/mol below native in this model (in vacuo with
ε0 = 4, charged side chains collapse onto each other); this is a property of the model.

## 4. Structures and table statistics
All four requested structures were prepared under rule 1 without repair; 1PGA and 1BPI were
added as cross-checks.  Chain A in all cases.

| PDB | notes on preparation | residues / atoms (with H) | sites | fixed (no chi / PRO / CYX) | states min / median / max | Σ states | log10 #configs | pairs |
|---|---|---|---|---|---|---|---|---|
| 1CRN | clean | 46 / 642 | 26 | 9 / 5 / 6 | 4 / 8.5 / 82 | 380 | 24.7 | 325 |
| 1UBQ | waters dropped; HIS68 → HID; residues 73–76 have occupancy < 1 without altloc (taken as is) | 76 / 1231 | 65 | 8 / 3 / 0 | 4 / 10 / 82 | 1763 | 77.1 | 2080 |
| 2IGD | 9 residues with altlocs → A; waters dropped | 61 / 927 | 49 | 11 / 1 / 0 | 4 / 10 / 82 | 1027 | 50.9 | 1176 |
| 5PTI | joint X-ray/neutron: all H and D deleted and re-added; Glu7, Met52 altlocs → A; DOD, PO4, UNX dropped | 58 / 892 | 36 | 12 / 4 / 6 | 4 / 10 / 82 | 1152 | 44.8 | 630 |
| 1PGA | waters dropped | 56 / 855 | 46 | 10 / 0 / 0 | 4 / 10 / 82 | 967 | 49.0 | 1035 |
| 1BPI | Glu7, Arg53 altlocs → A; PO4, waters dropped | 58 / 892 | 36 | 12 / 4 / 6 | 4 / 10 / 82 | 1152 | 44.8 | 630 |

Pair-table oscillation (max − min over the unclipped k_i × k_j table, kcal/mol; number of pairs):

| PDB | > 1 | 0.1–1 | 0.01–0.1 | ≤ 0.01 | largest | clipped entries (unary / pair, e_clip 1000) |
|---|---|---|---|---|---|---|
| 1CRN | 57 | 65 | 106 | 97 | 4.7e14 | 144 / 1173 |
| 1UBQ | 317 | 526 | 781 | 456 | 8.6e19 | 662 / 12241 |
| 2IGD | 165 | 303 | 479 | 229 | 4.6e19 | 346 / 3707 |
| 5PTI | 161 | 198 | 188 | 83 | 2.7e18 | 534 / 4834 |
| 1PGA | 171 | 312 | 420 | 132 | 7.8e16 | 324 / 3744 |
| 1BPI | 163 | 200 | 189 | 78 | 1.1e19 | 498 / 5376 |

With no cutoff and Coulomb ∝ 1/r², most long-range pairs still oscillate by 0.01–1 kcal/mol;
only 15–30 % of pairs are below 0.01.  Any sparsification downstream is therefore a model
change and must be stated as such.

Timings (single process, numpy, 4-core container; build = prepare + states + unary + pair):
1CRN 1.1 s (pairs 0.46 s); 1UBQ 14.4 s (prepare+states 1.5 s, unary 0.8 s, pairs 12.1 s);
2IGD 5.1 s; 5PTI 8.7 s; 1PGA 4.0 s; 1BPI 8.0 s.  OpenMM validation (42 configurations):
2.2–6.2 s.  Full test file: 16 tests in ~32 s (1UBQ slow test 21 s).

## 5. Tests (`tests/structbio/test_molecular.py`, written before the code)
Chi table shape for the 20 types; dihedral on known geometry; chi atoms form bonded chains and
the measured chi equals an independent arccos/triple-product formula (1L2Y model 1); library
symmetry-awareness; native state reproduces the deposited heavy atoms and the prepared
coordinates to 1e−9 Å; every library state of 1L2Y preserves all bond lengths (1e−9 Å) and
bond angles (1e−7°) and hits its chi targets (1e−9°); site selection on 1CRN (CYX 3, 4, 16,
26, 32, 40 fixed); rejection of a missing heavy atom and of a non-standard residue; pdbfixer
repair only behind the flag and recorded; reproducible preparation of 5PTI with input H/D
replaced; clipping and counts; save/load round trip; `max_states_per_site`; the §6 acceptance
test on 1CRN and (slow) 1UBQ.  Tests skip with a reason if the PDB files are not cached.

## 6. Judgement calls (all recorded in `meta` where applicable)
1. Terminal residues are sites. 2. Input hydrogens/deuteriums are deleted and re-added for every
structure (uniform protocol; deposited neutron/NMR H positions are discarded). 3. `seed` seeds
`addHydrogens`' random initial H placement; Reference platform for its minimiser. 4. Library
values for ASN/GLN amide (6), ASP/GLU carboxylate (3, mod 180), ARG chi4 (3), MET chi3
(staggered). 5. `max_states_per_site` counts the native state. 6. Non-standard detection uses
ATOM records and SEQRES of the chain; HETATM residues not in SEQRES are treated as ligands and
dropped. 7. Missing-residue detection: SEQRES count and a 2.0 Å peptide-bond check. 8. Partial
occupancies without altloc (1UBQ 73–76) are used as deposited. 9. Clash-free validation set
from ICM + a windowed random walk (§3). 10. Alternate locations: the spec lists altlocs both as
"keep the first" and as a possible rejection reason; we keep the first and report it.

## 7. Known limitations
In vacuo, no solvation/desolvation, no polarisation; ε(r) = 4r is a crude screening model.
Rigid rotation about chi bonds only, idealised library, no hydrogen-orientation degrees of
freedom (hydroxyl H do not re-optimise), fixed protonation and His tautomers (chosen once by
OpenMM's heuristic on the native structure).  Native-state hydrogens were minimised by
`addHydrogens` and library states were not, which biases comparisons between native and
library states.  Clipping at 1000 kcal/mol changes the model.  E_const is not computed, so
absolute table energies are only meaningful as differences.

## 8. Environment and what failed
The venv `/home/user/.venvs/structbio` did **not** exist at start; it was created with
`python3 -m venv` (CPython 3.13.18) and `pip install openmm==8.6.1 numpy scipy pytest pdbfixer`:
OpenMM 8.6.1, numpy 2.5.5, scipy 1.18.1, pytest 9.2.0, pdbfixer 1.12.0 (pulls legacy-cgi
2.6.4).  Failures during development, all resolved: the ring-detection BFS initially treated
the chi bond itself as a ring; the dihedral sign convention was initially inverted (caught by
the known-geometry test); non-reproducible hydrogen placement (§1.1.4); and an initial claim
that 5PTI lacks OXT, caused by a truncated grep — 5PTI does contain OXT and prepares cleanly.

## 9. Reproduce
    cd /home/user/MetricChain
    PYTHONPATH=src /home/user/.venvs/structbio/bin/python -m pytest tests/structbio/test_molecular.py -q            # all, incl. slow
    PYTHONPATH=src /home/user/.venvs/structbio/bin/python -m pytest tests/structbio/test_molecular.py -q -m "not slow"
    PYTHONPATH=src /home/user/.venvs/structbio/bin/python -c "from metricchain_sb.molecular import *; \
      t=build_energy_tables('benchmarks/structbio/pdb/1UBQ.pdb','A'); r=validate_against_openmm(t); \
      print(r['random']['max_rel_diff'], r['clash_free']['max_abs_diff'])"
