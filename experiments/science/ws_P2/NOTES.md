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
