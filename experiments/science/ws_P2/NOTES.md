# Workstream P2 — running notes

(Second wave, continues workstream P.  Measurement of class constants of a real residual
— GBn2 polarisation energy against Amber ff14SB — in ROTAMER variables on a FIXED backbone.)

Started 2026-11-25 19:59 UTC.  (Clock: Steps 0-6 below all took place between 19:59 and 20:34 UTC;
from Step 7 on the headings carry the time printed by `date -u`.)

## Step 0 — orientation (19:59)

* Read `docs/science/workstreams/COMMON.md` and `P2_brief.md` in full.
* Directory `experiments/science/ws_P2/` existed and was empty; this file is the first thing written.
* Hard constraints noted: write only here and `docs/science/workstreams/P2_REPORT.md`; no
  state-changing git; no `lake build`; no subagents; fixed sequences stated in advance; controls first;
  OMP_NUM_THREADS=1 etc.; computations < ~20 min, < ~5 GB; grid data goes into `data/` (git-ignored `*.npz`, `*.npy`).
* Next: read SP_REPORT §1, §2, §2.B, §3.1, §5, §6 and PHYSICAL_APPLICABILITY.md; then P's code.

## Step 1 — reading done; control 1 (P's end-to-end check) reproduced

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

## Step 2 — design fixed IN ADVANCE of any measurement

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

## Step 3 — side-chain builder written and validated (control 2)

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

## Step 4 — fixed-backbone table model written and validated (control 2, second half)

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

## Step 5 — control 3 (synthetic residuals) passed; analysis library; enumerations launched

* `anlib.py`: constants of order 1, 2, 3 on masked grids with non-uniform state counts
  (`mixed`: all state pairs at each involved site, all base points, every evaluation point in the
  domain), star and anchored order-2 expansions, ANOVA / least-squares / Chebyshev-LP fits.
* **Control 3** (`test_controls.py`, log `logs/test_controls.log`):
  - anlib against brute-force loops on random masked grids: identical (<= 7e-16), orders 1, 2, 3;
  - exactly pairwise synthetic residual: max c_ijk = 3e-15 … 2e-14, two-site fit remainder
    3e-15 (full grid) / <= 3e-11 (masked, LSQR), Chebyshev remainder 0.0;
  - iid random residual: c_ijk = 24-52 (function std 2.5-4.7), two-site remainder rms ~0.8-0.97 std;
  - planted third-order term 0.37*[x0=1][x1=0][x2=2] on top of a pairwise function: c_ijk = 0.3700
    exactly; Chebyshev two-site remainder 0.0463 = 0.37/8;
  - Thm 11.16 bound |g - g_star| <= sum c_ij and Thm 11.18 (m = 3) bound |g - I_2 g| <= sum c_ijk hold
    on all random instances (checks my c_ij, c_ijk and the expansions).
* Amendment to the design (before any long-chain constant was measured): the secondary grid "R2"
  (chi1 in {-60, 180}, rest trans) leaves Leu and Phe with <= 1 admissible state, so it is dropped.
  Long chains are reached instead by (i) the R3 domain itself where it is small (Val 3 states;
  Leu at 0.60 and Phe at 0.70: 2 states), (ii) grid "T3" = chi1 staggered, further chi trans
  (3 states) for Ser and Lys.
* `enum_fb.py` runs launched 20:22 for H, E, P2 in parallel (`run_enum_R3.sh`): homopolymers
  S, V, F, L, K for n = 1.. until the product exceeds 1.1e6, then LKSE:n.  One-site threshold
  0.60 (0.70 by restriction).  Logs `logs/enum_R3_<BB>.log`.
* In the helix the one-site domains depend on the position (contacts with the backbone of
  residues i-3, i-4): e.g. poly-Val on H at 0.60 has state counts [3, 3, 1, 1, 1, ...] — only
  the first two residues have any freedom (at 0.70 the helix is empty from n = 4); poly-Phe on H
  [6, 6, 4, 3, 3, 3, ...].

### First look (Ser4 on E, tau = 0.70, product domain = clash-free domain, 6561 assignments)
`an_main.py fb_S4_E_R3_t0.60 0.70` — exact numbers, kcal/mol:
* f: c_ijk = 5e-14 (rounding) -> pairwise, as it must be.  ff03-ff14SB: c_ijk = 5e-14;
  ff99SB-ff14SB: c_ij = 0.
* **g_GB: c_i = 4.3-4.9 (8 kT); c_ij up to 2.42 (i,i+2), 1.31 (i,i+1), 0.33 (i,i+3); half row
  sums 2.0-2.5; but c_ijk <= 0.0042 and the best two-site fit has remainder rms 0.0002 / max
  0.0015 / Chebyshev 0.0008.**  So g_GB is pairwise in rotamer variables to 1e-3 kcal/mol in SUP
  norm, with pair couplings that are not weak: excitation energies at the minimum are 1.0-1.1,
  the row-sum condition fails by a factor ~2, one star certifies only to 4.4 kcal/mol;
  the Hamming-2 ball (417 evaluations) certifies to < 1e-4 kcal/mol and brackets ln Z to 5e-4 nats.
* coul+GB (alternative split): c_ij <= 0.68, half row sums 0.39-0.43 < excitations 1.3-1.8:
  row-sum condition HOLDS, one star (33 evaluations) is an exact certificate; bracket 0.13 nats.
* ff03-ff14SB: exactly pairwise, half row sums 0.28-0.35 < excitations 0.41-0.93 at argmin E:
  exact certificate by one star at the true minimiser (which differs from argmin f).
=> working hypothesis to test on all systems: in rotamer variables the obstacle is not many-body
   character (third order is tiny) but the size of the PAIR part of the residual; the right
   interface is order three (Thm 11.18) / "pair part into the model", not the star.

## Step 6 — prior-art search (while the enumerations run)

Search log (PubMed through the literature tool; reading level of every item: **[abstract]**):
| # | query (PubMed syntax) | hits | kept |
|---|---|---|---|
| 1 | `generalized Born pairwise protein design` | 13 | 16853951, 28749575, 24854675, 26948696, 28886244, 17348031, 41055950 |
| 2 | `pairwise decomposable Poisson-Boltzmann protein design` | 2 | 15802649, 18074340 |
| 3 | `residue-pairwise generalized Born` | 4 | (same as 1) |
| 4 | `LUTE local unpruned tuple expansion` | 1 | 27681371 |
| 5 | `cost function network protein design guaranteed discrete energy optimization` | 0 | — |
| 6 | `partition function provable approximation side-chain rotamer K* algorithm` | 0 | — |
| 7 | `Simoncini Schiex guaranteed discrete energy optimization` | 1 | 26610100 |
| 8 | `Donald BR[Author] partition function provable approximation` | 2 | 31855059 (32511232 not used: about design of a specific interface) |

What the abstracts say (my paraphrase; quotes are from the abstracts):
* Archontis & Simonson, J Phys Chem B 109:22667 (2005), doi 10.1021/jp055282+ : a GB approximation
  "in which the interaction energy between two amino acids depends on the whole protein structure,
  but can be accurately computed from residue-pairwise information" (residue Born radii; a
  parabolic fit in their product).
* Gaillard & Simonson, J Comput Chem 35:1371 (2014), doi 10.1002/jcc.23637 : pairwise decomposition
  of an MMGBSA function; the GB term's "many-body character is overcome using an effective
  dielectric environment"; "the error remains reasonable, compared to other uncertainties".
* Villa, Mignon, Polydorides & Simonson, J Comput Chem 38:2396 (2017), doi 10.1002/jcc.24898 : "GB
  is a many-body potential"; common simplification "a mean, native-like protein/solvent boundary,
  which removes the many-body property"; their "fluctuating dielectric boundary" treatment is
  "numerically exact (within the GB framework)" while "retaining the residue-pairwise complexity".
* Gaillard, Panel & Simonson, Proteins 84:803 (2016), doi 10.1002/prot.25030 : side-chain
  prediction with a pairwise-additive MMGBSA function; "For the prediction of all side chains,
  however, errors due to the pairwise additive approximation overcome the improvement brought by
  these terms."
* Gaillard & Simonson, JCTC 13:4932 (2017), doi 10.1021/acs.jctc.7b00202 : the GB term "is affected
  by pairwise decomposition errors when all positions are designed together" (cited only for this
  sentence; the paper's subject, sequence design, is outside our scope).
* Gaillard, J Phys Chem B 129:10699 (2025), doi 10.1021/acs.jpcb.5c03662 : extension of the
  fluctuating-dielectric-boundary approach "allowing an exact decomposition of the GB term" to the
  whole protein (again cited only for the decomposition statement).
* Lopes, Alexandrov, Bathelt, Archontis & Simonson, Proteins 67:853 (2007), doi 10.1002/prot.21379 :
  side-chain placement for 29 proteins with implicit solvent; "the electrostatic model is not
  important for sidechain placement"; mentions "the recent discovery of efficient, pairwise
  implementations of GB".
* Marshall, Vizcarra & Mayo, Protein Sci 14:1293 (2005), doi 10.1110/ps.041259105 : one- and
  two-body decomposable finite-difference Poisson-Boltzmann; for desolvation of polar side chains
  "the two-body model has a 0.64 kcal/mol RMSD" against the full calculation; screened Coulomb
  interactions between side chains "approximated with an RMSD of 0.13 kcal/mol".
* Vizcarra, Zhang, Marshall, Wingreen, Zeng & Mayo, J Comput Chem 29:1153 (2008),
  doi 10.1002/jcc.20878 : improved pairwise decomposable FDPB ("generic sidechains", "two-body
  perturbations to the dielectric environment"; "two to threefold increase in accuracy").
* Hallen, Jou & Donald, J Comput Biol 24:536 (2017), doi 10.1089/cmb.2016.0136 (LUTE): represents
  "general, possibly nonpairwise energy functions to an arbitrary level of accuracy using a discrete
  energy matrix" by a local tuple expansion (fitted, not an anchored expansion with a bound).
* Simoncini, Allouche, de Givry, Delmas, Barbe & Schiex, JCTC 11:5980 (2015),
  doi 10.1021/acs.jctc.5b00594 : exact global minimum of pairwise-decomposable rotamer models by
  cost-function-network methods on spaces "of size up to 10^234" (for the statement that exact
  solvers for the pairwise problem exist at scale; the application is design).
* Jou, Holt, Lowegard & Donald, J Comput Biol 27:550 (2020), doi 10.1089/cmb.2019.0315 (MARK*):
  "provable epsilon-approximations to partition functions" over rotamer ensembles for pairwise
  energy bounds.
Not found by these queries and therefore NOT claimed absent: a sup-norm (worst-case over an
enumerated domain) measurement of the non-pairwise part of GB in rotamer variables, or mixed
third-difference constants.  The literature above reports RMS / mean errors of specific pairwise
constructions on folded proteins; mine are exact maxima on small exposed model peptides.

## Step 7 — first full results; a domain problem found and fixed (21:07 UTC)

* Enumerations (grid R3, one-site threshold 0.60): H finished (S1-6, V1-16, F1-10, L1-16, K1-4,
  LKSE:1-6); E and P2 still running (machine load 10-13 from other workstreams; my jobs run 3-4x
  slower than on an idle machine).  Largest: S6 531 441, K4 465 124, LKSE:6 319 176 (H), V12 531 441.
* `an_perchi.py` (Q1, second half), Ser3 on E / H, exact: with residue sites the third-order mixed
  differences of f are 4e-14 / 6e-14 kcal/mol; with one site per chi they vanish (4e-14) iff the
  three chi's lie in three different residues and are 4.4 / 5.5 kcal/mol for two chi's of one
  residue and one of another; order 4 (two residues, both chi's each): 6.5 / 5.6; order 5: zero.
  So in per-chi variables f is "pairwise per residue" only.
* **Problem found.**  First version of `an_main.py` computed the second-order interface on the raw
  product X.  For Phe (and partly Lys, LKSE) X contains assignments with two-site clashes, i.e.
  overlapping atoms: f up to 1.65e16 kcal/mol, "ff03 - ff14SB" up to 2.3e5, and all constants on
  X are garbage (c_ijk of a pairwise function 3.5 = rounding of 1e16).  P's warning ("without the
  filter the numbers are meaningless") applies to X.  But the product-space theorems (star
  sandwich) need a product domain: on the non-product X_tau the bound sum c_ij is not valid
  (the hybrids of x and x0 used in the proof may clash).
  **Fix (an_main.pruned_product):** X' = a product sub-domain of X_tau obtained by greedily
  removing the state involved in most two-site clashes until none is left.  If there is no pair
  clash, X = X_tau = X'.  Reported from now on: constants and fits on X_tau (P's domain) AND on X';
  interfaces (star, ball, first-order sharpness) on X' only.  Old outputs moved to `out_old/`.
* `an_long.py` (chains beyond enumeration): exact c_i, c_ij for pair-additive residuals from the
  tables; for GB the anchored order-2 expansion at a reference gives rigorous LOWER bounds on c_ij
  and — by evaluating true GB at the pair of assignments that maximises the pairwise surrogate —
  on c_i.  Validation on K4/H/0.70 (exact enumeration available): lower bounds
  [34.723 55.665 49.606 36.787] vs exact [34.72 55.66 49.61 36.79]; c_ij by separation
  [17.592 7.276 19.091] vs exact [17.60 7.28 19.10]; 868 GB evaluations instead of 16 464.
  Long runs launched (`run_long.sh`, log `logs/long.log`).

### Headline numbers so far (helix H; exact; kcal/mol; from `make_tables.py`)
* g_GB, max_i c_i by n:  Leu (tau .60, 2 states/site): 0.55 0.69 0.96 0.86 1.07 1.08 0.97 0.97
  1.04 1.12 1.14 1.15 for n = 1,2,3,4,5,6,7,8,10,12,14,16 -> saturates;  Ser (tau .70): 6.8 8.6 10.1
  9.8 9.0 9.4 (n = 1..6) -> saturates;  Phe (tau .60, X'): 2.6 3.2 3.0 3.0 2.9 2.6 1.9 1.6 1.6;
  Lys (tau .70): 10.0 37.3 51.5 55.7 (n = 1..4); (tau .60): 18.6 45.2 62.8 77.9 -> GROWS.
* c_ij(g_GB): Leu <= 0.51 (i,i+4), tail 0.04 at separation 9-11 (not present in f: it is the r^-4
  descreening tail); Ser <= 2.8; Lys 17.7-38.6 (charge-charge cross terms).
* c_ijk(g_GB): Ser/E 0.004; Ser/H 0.05 (tau .70), 0.19 (tau .60); Leu 0.09; Phe 0.10; Lys 0.14
  (tau .70), 1.9 (tau .60); LKSE 0.2-0.5.  Two-site fit remainder (rms / max): Ser6/E 0.0003 /
  0.003; Ser6/H 0.003 / 0.03; Leu16/H 0.047 / 0.21; Lys4/H 0.004 / 0.08 (tau .70), 0.026 / 1.3 (tau .60).
* Star (Thm 11.17 exact criterion, enumeration): Leu/H: EXACT certificate for every n <= 16
  (17 evaluations of 65 536; bracket 0.015 nats) — and lambda* = 1.18 > 1, so even one evaluation
  certifies; Phe/H: eps* 0.06-0.43; Ser: eps* 1.7 -> 10.6 (E), 6.4 -> 22.6 (H) growing with n;
  Lys: 18 -> 79 (tau .70), 34 -> 178 (tau .60); LKSE 13-33.
* Hamming-2 ball (Thm 11.18, m = 3): exact certificate in every instance at tau .70; Lys at .60:
  eps 0.14-0.19; free-energy bracket <= 0.19 nats except Lys/.60 (0.5-1.1 nats).
* ff03 - ff14SB: exactly pairwise (c_ijk ~ 1e-13); star exact for Leu, Phe, LKSE:4-5; fails for
  Lys (eps* 0.5-11.6).  ff99SB - ff14SB: additive (c_ij = 0), zero for Lys.

## Step 8 — mechanism, long chains, covers (21:36 UTC)

* `an_mech.py` (log `logs/mech.log`, JSON `out/mech_*.json`), on X':
  - Ser5/E (tau .70): GB c_ij max 2.42, half row 3.73; GBfrozen (radii frozen at argmin f; exactly
    pairwise) c_ij 2.74; GBfluct = GB - GBfrozen: c_i 1.33, c_ij 0.35, half row 0.42, c_ijk 0.0043.
    Born radii vary by <= 14 % (mean 4 %).  coul+GB: c_ij 0.69; coul+GBfrozen 0.36.
  - Ser5/H (.70): GBfluct c_i 3.7, c_ij 1.76, half row 1.69 (radii vary up to 44 %); (.60): c_ij 2.4,
    half row 3.2 (radii up to 145 %).
  - Leu12/H (.60): GB c_ij 0.52 but GBfrozen c_ij 0.024: for the apolar side chain the pair
    coupling is ENTIRELY Born-radius mediated (GBfluct c_ij 0.53); self and cross parts have
    ranges 91 and 89 kcal/mol that cancel to 3.95.
  - Phe8/H (.60): GBfrozen c_ij 0.35, GBfluct 0.50.
  - Lys3/H (.70): GB c_i 51.5, c_ij 17.7; GBfrozen c_ij 21.6 (charge-charge cross terms);
    GBfluct c_i 13.1, c_ij 6.1; coul+GBfrozen: c_i 2.2, c_ij 1.25; coul+GB c_ij 6.9.
    (.60): GBfluct c_ij 61 (radii vary up to 227 %) — compact states.
  - LKSE:5/H (.60): GBfrozen c_ij 10.7, GBfluct 8.8, coul+GBfrozen 4.6.
  => the pair part of g_GB = (direct screening cross terms, pairwise by construction, ~ minus the
     vacuum Coulomb interaction) + (Born-radius response, which appears already at second order
     in the sites because two side chains descreen the same atoms).  Third order is small.
* `an_long.py` (log `logs/long.log`, JSON `out/long_*.json`), X', lower bounds for GB:
  max_i c_i(GB) >=  Lys/H (.70): 55.7 (n=4, = exact), 85.5 (8), 110.1 (12), 123.6 (16), 137.9 (24)
  -> still growing at 24 residues (end residues largest; interior ~75-85);
  Ser/E: 5.18 (12), 5.25 (24); Ser/H: 9.84 (12), 9.98 (24); Leu/H (.60): 1.15 (24), 1.14 (32);
  LKSE/H (.60): 60.0 (8), 60.0 (12).  Exact for pair-additive residuals: ff03-ff14SB max c_i
  Lys/H 9.2, 9.5, 8.7, 8.6, 9.0 (n = 4..24) saturated; Ser 4.8-5.2; Leu 0.85.
  c_ij(GB) lower bounds by separation, Lys16/H: 17.6 7.2 18.9 17.6 2.8 2.9 7.9 3.2 0.9 1.8 2.2 1.0
  0.6 1.0 0.9 (helical periodicity, slow decay); Ser24/E: 1.31 2.42 0.33 0.19 0.07 0.05 0.03 0.02 0.01.
  Third-order lower bounds for central triples: Lys 0.57, Ser/E 0.004, Ser/H 0.019, Leu 0.036.
* `an_cover.py` (log `logs/cover.log`): first-order (per-site) certificates of min E on X_tau,
  [lower, greedy upper] at eps = 0:  GB: Ser4/E [53, 156] of 6561; Ser4/H [455, 582] of 2916;
  Ser5/H [1361, 2172] of 17 496; Lys3/H (.70) [2128, 2128] of 2352; Lys3/H (.60) [15 721, 15 725] of
  20 718; LKSE:4/H [78, 754] of 7254; LKSE:5/H [68, 800] of 14 508; Phe8/H [2, 4] of 14 014;
  Leu12/H, Leu14/H, Val8/E: 1 (one evaluation certifies).  ff03: Ser4/E [7, 85]; Ser4/H [2, 24];
  Lys3/H [28, 30]; LKSE:4/H [2, 8]; Leu12/H 1; Val8/E 1.  Envelope validity kappa_max = 1.0000 in all.
