# Workstream P (science division) — running notes

Report file: `docs/science/workstreams/SP_REPORT.md`.  Directory: `experiments/science/ws_P/`.
All times UTC, 2026-11-25.

## 17:41 start

* Read `COMMON.md` (rules: write only here + SP_REPORT.md; no git state changes; notes from first
  minute; numerics before theory; never fabricate; epistemic labels [V]/[P]/[K]/[N]/[C]/[H];
  model-relative vs physical).
* Read `P_brief.md`: Part 1 = pilot measurement on a real force field (OpenMM, ff14SB + GBn2,
  capped alanine peptides on a torsion grid; residuals (a) GB polarisation relative to vacuum,
  (b) difference of two force fields); measure c_i (per-torsion bounded differences) vs position
  and length, c_ij (mixed second differences), best fit in pair-distance-profile class and in
  1-body / 2-body torsion classes (sup and RMS remainder eta, Lipschitz L), site sharpness; plug
  into theory formulas (R*, sum ln cosh(beta c_i/2)) for 10 and 100 residues.
  Part 2 = table object -> physical counterpart -> validity -> what is lost -> what to certify.
* Read `README.md` (status of the programme).

## Plan (to be revised)

1. Read theory sections (§1, §4.4, §8, §11.4, §11.7, §11.12, §11.14, §11.17, §12; D28, D32, D42),
   ENG-RES-0003 and THY-REQ-0003.
2. Install OpenMM; verify ff14SB + GBn2 available; build Ace-(Ala)_n-NMe with fixed internal
   geometry from a torsion grid (own internal-coordinate builder or OpenMM-minimised template).
3. Enumerate grids, compute E_vac, E_GB, second force field; store arrays.
4. Analyses 1-4; formulas; report.

## 17:42–17:57 reading done; tooling built and validated

Read: THEORY_REPORT §1, §4.4, §8, §11.1–11.4, §11.6–11.7, §11.10 (Thm 11.24, 11.25), §11.12–11.15,
§11.17, §12; DEAD_ENDS D28, D32, D42; THY-REQ-0003; ENG-RES-0003 (engineering plans *synthetic*
chains / learned residuals on enumerated lattice domains; three class families; not started).
My pilot complements it: a real published force field, real many-body residual (GB), real FF–FF
differences, off-lattice torsion grid.

* `pip install openmm` -> OpenMM 8.6.1 (platforms Reference, CPU).  Force fields shipped:
  amber14/protein.ff14SB.xml, implicit/gbn2.xml (GBSAGBn2Force = Amber igb=8, mbondi3 radii),
  implicit/obc2.xml (igb=5), amber99sb.xml, amber19/protein.ff19SB.xml (CMAP), amber03.xml,
  amber14/protein.ff15ipq.xml.  CHARMM36 XML has no ACE/NME residue templates (patches) ->
  not used.  Also installed numexpr 2.14.2 (speed only).
* `pepbuild.py`: topology of Ace-(Ala)_n-NMe by hand; NeRF builder vectorised over
  conformations; bond lengths/angles = ff14SB equilibrium values read from the System; omega=180;
  methyls staggered; CA substituent offsets solved from three equilibrium angles.
  `test_build.py`: bond dev 1e-15 A, torsion error 1e-15 rad, chiral volume +2.508 A^3 (L),
  bond energy 0, angle energy 0.1052 kcal/mol per residue and *constant* over conformations
  (so only torsion + nonbonded + GB terms vary).  28 of 72 force-field angles deviate from
  equilibrium by up to 2.6 deg (those not imposed by the Z-matrix), constant over conformations.
* OpenMM per-conformation cost is dominated by CustomGBForce (~1.2 ms CPU platform, 2.7 ms
  Reference) -> too slow for 10^5–10^6 conformations.  Wrote `fastff.py`: numpy/numexpr
  re-implementation of exactly OpenMM's functional forms (NonbondedForce NoCutoff, PeriodicTorsion,
  GBn2 and OBC2 CustomGB expressions incl. neck tables), all parameters read from the OpenMM
  System objects.  `validate_fast.py`: max |deviation| from OpenMM Reference platform over
  n = 1,2,3,5,8 (750 conformations): <= 5.1e-12 kcal/mol on every component (torsions, LJ,
  Coulomb, GBn2 polar, ACE surface term, OBC2, and nonbonded/torsions of ff99SB/ff19SB/ff03/
  ff15ipq).  CMAP of ff19SB is taken from OpenMM itself (per-residue table over grid states).
  So: OpenMM is the ground truth; numpy is the validated fast path (~0.45 ms/conf at n=5, 1 core).
* `enumerate_grid.py`: exact enumeration on product torsion grids, with a spot check against
  OpenMM (CPU platform) on 2 conformations per block of 8192 (worst deviation ~4e-5 kcal/mol =
  single-precision noise of the CPU platform).
  Alphabets: A3 = phi in {-150,-70,+60} x psi in {-40,+60,+150} (9 states/residue);
  A2 = phi in {-150,-70} x psi in {-40,+150} (4 states/residue).
  Done: A3 n=1..4, A2 n=1..6.  Running: A3 n=5, A2 n=7,8, A3 n=6.

First look (Ace-Ala-NMe, A3, kcal/mol):
* GBn2 polar energy ranges -23.7 … -12.9 over the 9 states (range 10.8 kcal/mol = 18 kT);
  strongly anticorrelated with vacuum Coulomb (-20.1 … -40.4).
* ff99SB - ff14SB depends on phi only (range 0.65); ff19SB - ff14SB range 2.6; ff03 - ff14SB
  range 2.9; ff15ipq - ff14SB: range ~3 except at the one clashing state (LJ parameters differ).
* Clash score s(x) = min over pairs >= 4 bonds apart of r_ij/(Rmin_i/2 + Rmin_j/2):
  local states have 0.72–0.86 except (phi,psi) = (60,-40): 0.57 (LJ 86 kcal/mol; rigid
  geometry).  Non-local clashes (s < 0.6) appear from n=3 (A2: 1.6 % at n=3, 31 % at n=6 with
  threshold 0.7).  Decision: main domain = clash-free with threshold tau = 0.70; report
  sensitivity to tau in {0 (all), 0.6, 0.7, 0.8}.

## 17:57–18:05 first exact results (A3 n<=5, A2 n<=8); analysis scripts an1–an4

Scripts: `analysis_lib.py` (constants, mixed differences, ANOVA, design matrices, LS and
Chebyshev-LP fits, profile features), `an1_constants.py`, `an2_second_order.py`,
`an3_loworder.py`, `an4_profile.py`.  Outputs in `out/*.json`, logs in `logs/`.

**c_i of the GBn2 polarisation energy, clash-free domain (tau=0.7), A3 grid, kcal/mol:**
n=1: [8.96 6.99]; n=2: [14.02 10.53 12.44 9.19]; n=3: [16.09 12.41 18.63 16.43 15.14 11.19];
n=4: [17.27 13.35 22.88 20.05 22.90 20.49 16.29 12.77];
n=5: [18.82 16.95 25.89 22.04 27.48 25.21 25.56 22.63 19.79 15.98].
max_i c_i = 9.0, 14.0, 18.6, 22.9, 27.5 for n = 1..5  (15, 23.5, 31, 38, 46 kT): grows by
~4.6 kcal/mol per residue, dome-shaped along the chain (largest in the middle) -> the lever-arm
prediction shows up in a real residual.  RMS single-flip difference stays ~6.5 kcal/mol.
A2 grid (two common basins per torsion): max c_i = 5.7 (n=2), 14.3 (n=4), 16.0 (n=6).
Without the clash filter the product grid contains atom overlaps from n=4 (clash score 0.05)
and everything is meaningless there (e.g. "ff99SB-ff14SB" = 329 kcal/mol from 1e-4 charge
rounding at r -> 0): the clash-free domain is the one to report.

**Force-field differences (clash-free, A3):** ff99SB-ff14SB: c = 0.64 on phi sites, 0 on psi,
independent of n, all c_ij = 0 (exactly additive in torsions).  ff19SB-ff14SB: c = (1.54, 2.59),
independent of n; c_ij = 2.48 for (phi_r, psi_r), exactly 0 otherwise (sum of residue tables).
ff03-ff14SB (different charge model): max c_i = 2.6, 3.0, 3.9, 4.6, 4.6 (n=1..5), c_ij dense but
decaying (3.9, 2.6, 2.0, 1.1, 0.9, 0.7, 0.7 by separation at n=4).  ff15ipq-ff14SB: 2.8 … 5.0.
OBC2-GBn2: max c_i 1.3 … 3.0.  coul+GB (screened electrostatics): c_i about half of GB alone.

**c_ij of GB (A3, n=4):** dense: max 23.1 kcal/mol (39 kT), by separation 23.1 22.4 18.9 12.2
11.9 7.2 7.0; half row sums 37–60 kcal/mol -> row-sum condition of §11.7 fails by an order of
magnitude; Dobrushin-type row sums ~7 (need < 1).

**Low-order torsion fits of GB (A3 n=5, 28 843 clash-free conformations, std 7.61):**
1-body RMS 3.94 / max 17.8; all torsion pairs RMS 2.10 / max 13.4; residue-pair tables RMS 1.13 /
max 9.1; residue triples (window 2, 1961 parameters) RMS 0.58 / max 7.3 kcal/mol (LS fits; the
sup-optimal LP values for n=3,4 are in logs/an3_A3_n4.log).

**Profile class (A3 n=4, 3844 conformations):** typed pair-additive fit with piecewise-linear
radial functions in s=r^2 (knots every 0.5 A, no cutoff): one type RMS 3.06 / max 16.1;
element-pair types (10 types, 300 parameters) RMS 0.29 / max 2.4 (test 0.32 / 2.9); Amber
atom-type pairs (36 types, 975 parameters) RMS 0.07 / max 0.57 (test 0.12 / 1.02); fitted slopes
L_s ~ 0.5 kcal/mol/A^2 (L_r ~ 3.5 kcal/mol/A).  CAUTION: on a coarse torsion grid a typed
profile model can act as a lookup table for local torsion states (few distinct distances per
pair); the held-out half shares the grid.  Needed: off-grid test and transfer across chain
length before believing "GB is nearly pair-additive".  Control: vacuum Coulomb (exactly
pair-additive but pair-specific, 1-4 scaled) has the same remainder in this class (RMS 0.07,
test max 2.6) -> the remainder is at the resolution of the class, not obviously many-body.

## 18:05–18:28 exact data to A3 n=6 / A2 n=9; off-grid ensemble; sharpness; scaling

Data now on disk: grids A3 n=1..6 (531 441 conformations at n=6, 215 409 clash-free), A2 n=1..9
(262 144 at n=9, 125 696 clash-free); off-grid ensemble C (`sample_continuous.py`: residues
drawn uniformly from the clash-free 42 % of the dipeptide (phi,psi) map, non-local clashes
rejected) for n=2,3,4,5,6,8; single-torsion scans n=2,5.  Machine load 15–18 on 4 cores
(other workstreams): everything slow, single-threaded.

**Exact c_i of GB (clash-free, kcal/mol), max over sites:** A3: 8.96, 14.02, 18.63, 22.90,
27.48, 31.62 (n=1..6) = 15 … 53 kT; fit max c = 4.81 + 4.51 n; mean c = 4.65 + 3.42 n.
A2: 3.69, 5.69, 9.09, 14.31, 14.57, 15.99, 17.69, 18.35, 19.04 (n=1..9); fit 3.30 + 1.97 n but
visibly sub-linear (power fit 3.87 n^0.78).  Position: lower at the two ends (first ~2
torsions), flat in the interior (A3 n=6 by distance m to the nearer end: 18.7 18.7 26.8 28.2
29.3 28.2).  Pooled two-variable fit (A3): c_i = 3.60 + 2.31 m_i + 1.12 (2n).  So: growth with
chain length is clear and roughly linear for the maximum (A3); the dependence on position is
an end effect plus a plateau, not a clean power law in m_i (pooled exponent 0.45 in A3, 0.36
in A2 -- well below the theory's contact-type lower bound exponent 1 and RMSD exponent 3/2,
on m <= 6..9).
RMS (typical) single-flip change does NOT grow: 6.4–6.5 kcal/mol (A3), 3.6–3.7 (A2).

**Local search lower bounds** (`long_chain_ci.py`; validated against exact A3 n=5: recovers
6/10 sites exactly, others within 20 %): A3 n=8: max 34.6 kcal/mol (58 kT) [linear law predicts
40.9; search is a lower bound].  A2 n=12,16,20 and A3 n=10 running.

**Off-grid profile-class fit** (`an5_profile_transfer.py`, ensemble C n=5, 8000 train/8000 test,
GB std 5.47): one type: RMS 5.1 (useless); element-pair types (10 types, 321 parameters):
held-out RMS 0.56 / max 3.45 kcal/mol; Amber atom-type pairs (36 types, 1101 parameters):
held-out RMS 0.26 / max 2.19 kcal/mol (0.43 / 3.7 kT); slopes L_s <= 0.9 kcal/mol/A^2
(L_r <= 4.4 kcal/mol/A).  Transfers to shorter chains (n=3,4: RMS 0.19–0.22) and to the grids
(A3 n=5: RMS 0.32, max 3.5) with only the intercept refitted; does NOT transfer to n=8 (RMS 4.8)
because distances > 22 A were never seen in training -- the exactly pair-additive control
(vacuum Coulomb) fails the same way (RMS 8.3), so this is extrapolation in distance, not
many-body physics.  Fit on n=8 queued.  Control: vacuum Coulomb in the same class has held-out
RMS 0.30 / max 2.1 -> GB is as close to this typed class as an exactly pair-additive function
with pair-specific coefficients is.
Sup-norm LP on 2500 training conformations with unbounded slopes overfits badly (elem typing:
eta_train 1.06, held-out max 10.2): Chebyshev fits need the slope bound.

**Sharpness and certificates on real instances** (`an7_sharpness.py`; f = vacuum ff14SB,
envelope = measured per-torsion constants, valid on the clash-free domain: max ratio 1.0000):
* GB, A3 n=3: 0/6 sites sharp (e_i/c_i = 0.04–0.47); argmin f (all beta) != argmin E (all PPII),
  regret 1.57 kcal/mol; N_cov(0) in [94, 139] of 508.  n=4: 0/8 sharp; N_cov(0) in [447, 782] of
  3844; N_cov(2 kcal/mol) in [261, 609].  Growth x4.8 per residue (domain grows x7.6).
  n=5: argmin f = alpha-helix, argmin E = PPII, difference 0.46 kcal/mol; cover running.
  n=6: helix is the minimum of both; most single flips out of the helix clash (rigid geometry),
  so single-flip sharpness is not defined there -> added the cost-to-distance ratio lambda*.
* A3 n=4, force-field differences: ff99SB-ff14SB 8/8 sharp, 1 evaluation certifies;
  ff19SB-ff14SB 4/8 sharp, N_cov in [2, 11]; ff03-ff14SB 4/8, [2, 12]; ff15ipq-ff14SB 3/8,
  [2, 21]; OBC2-GBn2 4/8, [6, 21].  (All of 3844.)
* Exact Jensen gaps ln Z(f+g) - ln Z(f) + beta<g>_f on the grid: GB n=4: 2.56 nats, n=5: 2.30;
  the class bound sum ln cosh(beta c_i/2) is 117 and 178 nats: the real residual is nowhere
  near the worst member of its first-order class.

**Continuous single-torsion scans (ensemble C bases, 10 deg):** GB oscillation along one torsion
up to 13–16 kcal/mol (n=2), 14–24 (n=5), median 6.4–6.7; Lipschitz constants up to 9–21
kcal/mol/rad (median ~4.3); torus formula J = sum ln(sinh b_i/b_i) = 85 nats (n=2), 295 (n=5).

**Extrapolation (an6_scaling.py), coil-like site tables of f from the all-beta star
(phi: 0, 0.8, 21.6; psi: 0, 4.8, 5.2 kcal/mol):** 10 residues: 0/20 sharp; product bound
ln N_cov >= 12.0–12.5 (N >= 10^5.2–10^5.4 of 3^20 = 10^9.5); sum ln cosh = 427–476 nats.
100 residues: ln N >= 129–171 (10^56–10^74 of 10^95); sum ln cosh = 4.6e3–3.1e4 nats.

## 18:28–19:05 many-body analysis, collective sharpness, covers at n=5, report drafted

* `an10_basins.py`: reference conformations on A3.  argmin f: beta (n<=4), helix (n=5,6);
  argmin E=f+GB: PPII (n<=5), helix (n=6; PPII only 0.37 kcal/mol above, 9.27 in vacuum).
  Collective ratio lambda* = min_y (E(y)-E(x*))/d(x*,y): 0.038, 0.031, 0.020, 0.0045, 0.0026
  (n=2..6).  In the helix 6 of 10 (n=5) and 8 of 12 (n=6) torsions have no clash-free
  single-flip neighbour; the others are not sharp.  => no torsion sharp anywhere.
* `an7_sharpness.py` (fixed: memory-safe cover; an earlier version built an 832M-entry sparse
  matrix for the dense covers of the FF differences and was OOM-killed; lambda* bug at x0 fixed).
  Covers, lower/upper: GB A3 n=5: eps=0 [3042, 5357], kT [2668, 5033], 2 kcal/mol [1947, 4307] of
  28 843; GB A2 n=8: [4061, 8041] of 35 478; g_19 n=5: [2, 3]; g_03 n=5: [2, 28]; g_99 n=5: 1.
  ff99SB vs ff14SB at n=5: the minimiser CHANGES (helix -> all-beta, by 2.33 kcal/mol) although
  the residual is exactly additive with c = 0.64 kcal/mol per phi.
* `an11_manybody.py`: explicit exactly pair-additive surrogate of GB (frozen mean Born radii in
  the cross terms + linear function of the descreening sums, N+1 weights).  g - S, RMS/max
  kcal/mol: ensemble C held-out n=2..8: 0.10/0.9, 0.21/2.6, 0.30/4.1, 0.34/3.5, 0.43/5.4 (n=6),
  0.52/6.1 (n=8); all clash-free A3: 0.14/0.5, 0.27/1.0, 0.39/2.3, 0.48/4.8 (n=2..5); all A2 n=8:
  0.47/9.3.  Naive frozen radii: RMS 2.1 … 7.2 (useless) though radii fluctuate only 2–4 %.
  First attempt (self term linearised atom by atom, cross term frozen) had RMS 5 kcal/mol:
  the cross terms of bonded neighbours respond to the Born radii at first order.
* `an5_profile_transfer.py 8`: Amber-typed profile class trained at n=8: held-out 0.43/3.94;
  element-typed 1.04/5.74.  Transfers down the chain length (RMS 0.25–0.36), not up.
  Chebyshev LP with slope bound (elem types, n=5): eta_train 1.06, 1.06, 1.48, 4.0, 8.7 at
  L_s = inf, 1, 0.3, 0.1, 0.03; held-out maxima 6–21 (sampled sup norms are not bounds).
  The amber-typed LP run was killed (1101 parameters on 2500 rows: meaningless).
* `an8_scans.py`: n=8: oscillation along one torsion up to 12–20 kcal/mol, L_i up to 9–27
  kcal/mol/rad; J = 566 nats.
* `an9_torsion_refits.py`: g_99(phi) range 1.1147 kcal/mol on the circle (independent of psi to
  3e-7); g_19 range 14.1 on the torus, 5.0 on its clash-free 41 %.
* Long chains (local search, lower bounds): A2 n=12 max 19.7; A2 n=16 (9 sites) 19.2;
  A3 n=10 (8 sites) 35.2; A2 n=20 running.  The search weakens with size (few starts).
* Clash-threshold sensitivity: tau 0.6 vs 0.7: max c_i unchanged for n<=4, +8–15 % beyond;
  A3 at tau=0.8 equals A2 exactly (the phi=+60 and psi=+60 states score 0.72–0.73).
* Energy windows (A3 n=5): within 5 kcal/mol of min f: 52 conformations, g varies by 6.0;
  within 20: 5378 conformations, max c_i 14.6 (27.5 on the full domain).
* Prior art: PubMed abstracts only (GB-Neck2; ff14SB; ff19SB; Archontis–Simonson 2005
  residue-pairwise GB; Gaillard 2025; LUTE 2017).  ff14SB abstract confirms the phi-profile
  adjustment that Statement 3(a) measures.
* Report: docs/science/workstreams/SP_REPORT.md sections 1, 2, 2.B, 3, 4–7 written.

## 19:05–19:15 final checks, report complete

* Position dependence corrected in the report: on A3 the profile is a dome; on A2 the phi
  constants are a dome but the psi constants increase towards the C-terminus (largest constant
  of A2 n=9 is the LAST psi, 19.0 kcal/mol: cap against a preformed compact structure;
  dGB = +19.0 compensated by dCoulomb = -24.6).  "Distance to the nearer end" is not the
  controlling variable.
* A2 n=20 local search (6 sites, 6 starts): max 14.6 — weaker than exact n=9 (19.0): the search
  says nothing about growth at that size.  Stated as such.
* `verify_openmm_direct.py`: c_i(g_GB) on the A3 tripeptide grid computed with OpenMM's own
  CustomGBForce and a brute-force loop (no fastff, no analysis_lib) = 16.09 12.41 18.63 16.43
  15.14 11.19, 508 clash-free: identical to the pipeline.
* Envelope validity ratio = 1.0000 in all 11 an7 runs.
* Killed: amber-typed Chebyshev LP (meaningless), A2 n=8 cover at eps>0 (not needed).
* No background process left.  data/ is 161 MB, untracked.
* Not done (see report §5): side chains, relaxed geometry, PB/QM/learned residuals, upper bounds
  for continuous constants, certificates in the span format, lower bound on the distance to the
  pair-additive class.

Final deliverables: `docs/science/workstreams/SP_REPORT.md`; this directory.
