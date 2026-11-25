# Workstream P2 — running notes

(Second wave, continues workstream P.  Measurement of class constants of a real residual
— GBn2 polarisation energy against Amber ff14SB — in ROTAMER variables on a FIXED backbone.)

Started 2026-11-25 19:59 UTC.

## Step 0 — orientation (19:59)

* Read `docs/science/workstreams/COMMON.md` and `P2_brief.md` in full.
* Directory `experiments/science/ws_P2/` existed and was empty; this file is the first thing written.
* Hard constraints noted: write only here and `docs/science/workstreams/P2_REPORT.md`; no
  state-changing git; no `lake build`; no subagents; fixed sequences stated in advance; controls first;
  OMP_NUM_THREADS=1 etc.; computations < ~20 min, < ~5 GB; grid data goes into `data/` (git-ignored `*.npz`, `*.npy`).
* Next: read SP_REPORT §1, §2, §2.B, §3.1, §5, §6 and PHYSICAL_APPLICABILITY.md; then P's code.

## Step 1 — reading done; control 1 (P's end-to-end check) reproduced (20:05)

* Read SP_REPORT §1, §2 (Statements 1–9), §2.B, §3.1, §3.2, §5, §6, §7 (E-1 is this workstream's
  specification), PHYSICAL_APPLICABILITY.md (all), theory report §11.7 (Thm 11.16–11.18 and the
  row-sum condition), §11.12 (Thm 11.31–11.32), §11.13 (Thm 11.33).  Read P's code: pepbuild.py,
  fastff.py, enumerate_grid.py, analysis_lib.py, an1/an2/an3/an7/an10, verify_openmm_direct.py,
  validate_fast.py, test_build.py.
* What the second-order interface needs (my reading of §11.7):
  - class: |g(x^{i->a,j->b}) - g(x^{i->a}) - g(x^{j->b}) + g(x)| <= c_ij for all x, i != j, a, b;
  - Thm 11.16 [V]: star of 1 + sum_i (k_i - 1) evaluations at x0; |g - g_star| <= sum_{i<j changed} c_ij;
  - Thm 11.17 [V]: x0 is a minimiser for every consistent residual iff x0 minimises the lower
    pairwise model  f + g_star - sum_{i<j changed} c_ij  (exact criterion);
  - row-sum condition [P] (sufficient, stated for an additive known part):
    (1/2) sum_{j != i} c_ij <= measured single-site excitation energy at site i, every state;
  - Thm 11.33(a) [P]: free energies, polynomial cost if Dobrushin-type sum_j tanh(beta c_ij/4) < 1
    (stated for the cube with uniform c2: w = beta c2 n <= 4).
* **Control 1 done**: `ws_P/verify_openmm_direct.py` run from my directory with `python3 -B`
  (no bytecode written into ws_P; `ws_P/__pycache__` timestamps unchanged):
  `clash-free conformations: 508 of 729`, `c_i = [16.09 12.41 18.63 16.43 15.14 11.19]` kcal/mol.
  Identical to SP_REPORT Statement 1 / PHYSICAL_APPLICABILITY §8.  Log: `logs/control_P_verify.log`.
* Machine: 4 cores, 14 GB free, load 0.03 at start.  OpenMM 8.6.1, numpy 2.5.3, scipy 1.18.1,
  numexpr 2.14.2, Python 3.13.18.

## Step 2 — design fixed IN ADVANCE of any measurement (20:15)

Everything below was written before any constant of any side-chain system was computed.

**Sequences (fixed; nothing is varied, compared for a property, or optimised).**
* Homopolymers Ace-(X)_n-NMe with X = Val, Leu, Ser, Phe, Lys (apolar beta-branched; apolar;
  polar neutral with a rotatable hydroxyl; aromatic; charged +1).
* One heteropolymer: Ace-(Leu-Lys-Ser-Glu)_m-NMe, i.e. the pattern `L K S E` of the brief
  repeated and truncated to n residues (first residue Leu).
* Ace-(Ala)_n-NMe only as a regression test against P's builder (Ala has no rotamer).

**Backbones (fixed, uniform (phi, psi), omega = 180, rigid ff14SB equilibrium geometry, P's builder).**
* H  = (-57, -47)   "ideal alpha-helix"        (textbook values, quoted from memory; they are
* E  = (-139, +135) "ideal extended strand"     parameters of a synthetic model, nothing depends
* P2 = (-75, +145)  "ideal polyproline II"      on their provenance)
* sensitivity: P's own grid basins H' = (-70, -40), E' = (-150, +150), P2' = (-70, +150).
  A backbone is used only if its own clash score (fixed atoms) exceeds 0.70.

**Site variables.**  One site per residue; the state of a site is the tuple of all its side-chain
dihedrals ("rotamer").  Dihedrals: chi1 = N-CA-CB-XG, chi2 = CA-CB-XG-XD, ...; for Ser the
hydroxyl torsion CA-CB-OG-HG counts as chi2.  Methyl and ammonium rotors are fixed staggered
(180, +60, -60), as in P.
* Grid R3: every chi in {-60, 180, +60} degrees.  States per site: Val 3, Leu 9, Ser 9, Phe 9,
  Lys 81, Glu 27.  (For the two-fold symmetric planar groups — Phe ring about CB-CG, Glu
  carboxylate about CG-CD — these are the three orientations 0, 60, 120 mod 180.)
* Grid R2 (secondary, only to reach longer chains exactly): chi1 in {-60, 180}, all further
  chi = 180.  Two states per site.
* Per-chi sites (chi2 moves with chi1) are used only to show that the known part is then NOT
  pairwise.

**Domain / clash filter (P's score and threshold).**  s = min r_pq/(R_p + R_q) over atom pairs
four or more bonds apart, R = Amber R_min/2.  tau = 0.70 primary; sensitivity tau in {0.60, 0.80}.
On a fixed backbone the score decomposes: s(x) = min(s_fixed, min_i s_i(x_i), min_{i<j} s_ij(x_i, x_j)).
* D_i = {states of site i with s_i > tau};  X = prod_i D_i  ("product domain": every rotamer
  compatible with the backbone);  X_tau = {x in X : s_ij(x_i, x_j) > tau for all i<j}
  ("clash-free domain", P's definition restricted to my variables).

**Energies.**  f = ff14SB vacuum energy (torsions + Lennard-Jones + Coulomb; bonds and angles
are constant by construction); g_GB = GBn2 polarisation energy (OpenMM implicit/gbn2.xml,
sasaMethod=None), exactly P's g_GB; force-field differences at identical coordinates:
g_03 = ff03 - ff14SB (primary, for comparison with P's Statement 4), g_ipq = ff15ipq - ff14SB,
g_99 = ff99SB - ff14SB; alternative split "coul+GB".  beta = 1/0.596161 (300 K).

**Constants.**  c_i, c_ij as in SP_REPORT §2; c_ijk = max |third mixed difference| (new here).
Second-order theorems are applied on product domains only (the star sandwich needs the hybrid
configurations); on X_tau I report the measured star remainder next to the bound.

**Plan of code.**  `scbuild.py` (topology from OpenMM templates + Z-matrix with side chains,
subclass of P's `Peptide`; P's `FastFF` is used unchanged as the validated evaluator);
`fbmodel.py` (fixed-backbone tables: coordinates per site state, clash tables, exact pair tables
of every pair-additive energy component by anchored decomposition, GB by pre-tabulated
descreening integrals — a second implementation validated against FastFF and OpenMM);
`anlib.py` (constants of order 1, 2, 3 on masked non-uniform grids, fits, covers).

## Step 3 — side-chain builder written and validated (control 2) (20:35)

* `scbuild.py`: `SCPeptide(seq)` subclasses P's `Peptide` (imported from `../ws_P`, with
  `sys.dont_write_bytecode`): topology from the ff14SB residue templates of OpenMM (atom order and
  bonds read from the XML; only the side-chain internal coordinates are typed by hand, table
  `SIDECHAIN`); Z-matrix = P's backbone + side chains (chi-driven atoms, siblings at offsets
  solved from three equilibrium angles, rotors staggered, planar groups at 0/180).
  Residues: ALA VAL LEU SER LYS PHE GLU.
* **Found and fixed before any measurement:** OpenMM's ff14SB gives the hydroxyl hydrogen (type
  HO, epsilon = 0) a placeholder sigma = 1 nm, i.e. "R_min/2" = 5.61 A.  With that value P's clash
  score marks every serine conformation as a clash (score 0.3-0.5).  Amber's own parameter file has
  R = 0 for HO [from memory].  Decision: atoms with epsilon = 0 get radius 0 in the clash score
  (a pair involving HO is then judged by the other atom's radius alone; HO-HO pairs never clash).
  This is the only deviation from P's clash criterion and it cannot affect P's alanine numbers
  (no epsilon = 0 atom there).
* `test_scbuild.py` (log `logs/test_scbuild.log`), systems VVV LLL SSS FFF KKK EEE LKSE LKSELKSE,
  120 states each (random backbone + random chi; ideal backbones + grid chi; ideal + random chi):
  - regression: poly-Ala coordinates identical to P's builder (difference 0.0e+00 A, n = 1, 3);
  - bond lengths: max deviation 7e-15 A over ALL force-field bonds, including the ring-closure
    bond of Phe (the ring closes exactly at the ff14SB equilibrium values);
  - bond angles: constant over conformations to 4e-13 deg; 40-136 of the force-field angles are
    off equilibrium by up to 2.6 deg (5.1 deg in Phe), constant -> angle energy constant
    (spread <= 5e-14 kcal/mol), bond energy < 1e-25;
  - phi, psi, chi recovered to 4e-15 rad; chiral volume at CA +2.508 A^3 (L) everywhere;
  - **FastFF vs OpenMM Reference platform (double precision), clash-free conformations:**
    worst deviation over all systems: tors 2.8e-14, lj 3.4e-12, coul 5.9e-12, GBn2 1.2e-11,
    ACE-SA 1.8e-12, OBC2 1.1e-11, ff99SB/ff03/ff15ipq torsions <= 2.1e-14, nonbonded <= 5.0e-12
    kcal/mol; bond+angle energy of the other force fields constant to <= 2.6e-13 (the first
    run compared against a clashing reference conformation and showed 1e-4 of subtraction
    noise -> test fixed).
  - net charges: KKK +3, EEE -3, LKSE 0 (exact to 1e-4).
* Timing: OpenMM Reference 6-28 ms/conf; FastFF 0.35-4.0 ms/conf (146 atoms: 4 ms) -> too slow
  for 5e5-conformation grids of 100-200 atoms; hence the table-based evaluator below.

## Step 4 — fixed-backbone table model written and validated (control 2, second half) (21:05)

* `fbmodel.py`: `FBModel(seq, bb, grid)`.  Site = residue; every atom depends on at most one
  site (asserted when the coordinates of each site's states are built: all other atoms unchanged
  to 1e-10 A; measured 0.0).  Tables: clash scores (fixed / one-site / two-site), exact one- and
  two-site tables of every pair-additive component (coul, lj by direct atom-pair sums with the
  parameter arrays FastFF read from OpenMM; torsions: every torsion term is asserted to involve
  atoms of at most one site), GBn2 descreening integrals (tables) -> exact Born radii of an
  assignment by table look-ups; GB energy by a block pair sum (`gb_energy`) or the straightforward
  all-pairs sum (`gb_energy_simple`).
* `test_fbmodel.py` (log `logs/test_fbmodel.log`), 12 systems (V4, L3, S3, F3, K3, LKSE, LKSE x 2,
  L6; backbones H, E, P2, Hp), 200 random assignments each:
  - assembled coordinates == full internal-coordinate build: difference 0.0 A;
  - clash(tables) == clash(FastFF) to 6e-16;
  - **every pair-additive component from the tables == FastFF on the full conformation**:
    worst over systems, clash-free conformations: tors 8.5e-14, lj 1.1e-12, coul 3.4e-13;
    ff99SB/ff03/ff15ipq components <= 1.0e-12 kcal/mol; relative deviation on ALL assignments
    (clashing included) <= 4e-13.  => numerical proof of concept for Q1: the vacuum energy is
    c0 + sum_i h_i + sum_{i<j} J_ij in residue-rotamer variables (exact test of third-order
    differences follows on full grids);
  - GBn2(tables) vs FastFF: <= 4.5e-13 kcal/mol; vs OpenMM's own CustomGBForce on the Reference
    platform: <= 8.9e-12 kcal/mol; f(tables) vs OpenMM (torsion + nonbonded groups) <= 1.9e-12.
  - block GB == simple GB to 1.4e-11 (relative 5e-13).
* Speed: block GB 75 us/conf (78 atoms), 116 us (100 atoms), 275 us (146), 570 us (204),
  1.3 ms (316 atoms); 24 ns per atom pair (numexpr exp/sqrt, one thread).  f from tables < 2 us.
* `enum_fb.py`: exact enumeration over the product of one-site-clash-free states; stores gb, tors,
  lj, coul, the other force fields, and the clash scores s1min / s2min so that tau and the pair
  filter are applied afterwards.  Each run spot-checks 24 assignments against FastFF (double)
  and 4 against OpenMM's CPU platform (single precision, deviations ~1.5e-5 as in P).

### Geometry finding that constrains the design (found before any constant was measured)

One-site clash scores of the R3 states (middle residue of a tripeptide; `logs/test_fbmodel.log`
and the inspection run):

| residue | states | score > 0.70 (H / E / P2) | score > 0.60 | score > 0.80 | best states |
|---|---|---|---|---|---|
| Val | 3 | 1 / 3 / 3 | 3 | 0 | chi1 = 180 (0.75); +-60 at 0.66 (H) or 0.72 (E) |
| Leu | 9 | **0 / 0 / 0** | 2 (1 on Ep) | 0 | (180, 60) 0.645 and (-60, 180) 0.633 — the two rotamers known as dominant ("tp", "mt"); limited by an intra-residue H...H contact HD-HA at 1.82-1.85 A |
| Ser | 9 | 9 / 9 / 9 | 9 | 9 | all |
| Phe | 9 | 2 / 2 / 2 | 6 / 5 / 6 | 0 | two at 0.79 |
| Lys | 81 | 14 / 21 / 21 | 31 | 0 | |
| Glu | 27 | 8 / 10 / 11 | 18 / 16 / 18 | 0 | |

Fixed-atom (backbone + CB) scores: H 0.804, E 0.783, P2 0.858, Hp 0.806 -> all backbones usable.

Consequences (decided now, before measuring):
1. At P's threshold tau = 0.70 **Leu has no admissible rotamer** in the rigid ideal geometry, on
   any backbone; poly-Val on the helix has a single state per site (trivial).  The pre-registered
   sensitivity threshold 0.60 keeps exactly the two dominant Leu rotamers and all three Val states.
   I therefore report BOTH thresholds throughout: tau = 0.70 ("P's threshold") where the domain is
   non-trivial (Ser, Lys, Phe, Glu; Val on E and P2) and tau = 0.60 ("relaxed") for everything,
   including Leu and the heteropolymer LKSE (whose Leu sites are empty at 0.70).  tau = 0.80 is
   meaningful only for Ser (every other residue type is empty there).
2. Exact enumeration limits (product of one-site domains): S 9^n (n <= 6); V 3^n (n <= 12);
   F 2^n at 0.70 / 6^n at 0.60; L 2^n at 0.60; K 14^n-21^n at 0.70 (n <= 4-5), 31^n at 0.60
   (n <= 4); LKSE at 0.60: 2*31*9*18 ~ 1e4 per repeat (n <= 6).
