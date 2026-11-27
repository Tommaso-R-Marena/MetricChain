# Workstream P5 — running notes

Started 2026-11-26 02:17 UTC.  Researcher: independent workstream P5 of the science division.
Rules: write only here and in `docs/science/workstreams/P5_REPORT.md`; no state-changing git;
at most two processes; `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`; no run longer than 20 min.

## 02:17  Start
- Read `COMMON.md`, `P5_brief.md`.  Reading `P3_REPORT.md` in full (1296 lines), then P3 code.
- Plan (order of the brief): step 1 measure cancellation by neutral groups on enumerable helix
  instances (Leu6, Leu8, Ser4–6 on the helix), orders 3–5: self / cross / sum / cross regrouped
  by neutral groups next to P3's pair-by-pair bound.  Step 2: lower bound for pair-by-pair
  bounds on an explicit family (two neutral dipoles at distance R).  Steps 3–4 only if step 1
  says the route is alive.

## 02:20–02:38  Reading; first measurements  (time stamps from `date`; an earlier version of this heading said 03:05, which was a guess and wrong)
- Read P3_REPORT in full, P3 code (p3core, mixdiff, x01_explore, gfbound, encl, t02_gf, x04_gamma, head of
  run_floor/pwmodel), addendum A17 (9)-(11).
- NOTE (rule): `encl.EnvelopeSup` writes its tables into `ws_P3/cache/` when a table is missing.  To avoid any write
  into ws_P3, `p5lib.py` redirects `encl.CACHE` to `ws_P5/cache/` (the 27 existing .npz tables were COPIED there,
  8.3 MB).  All scripts run with `python3 -B` (no bytecode written into ws_P2/ws_P3).
- Facts about the model found by probing: Leu on the helix (tau 0.60) has 2 states per site; moving atoms of a Leu
  side chain: HB2 HB3 CG HG CD1 HD1x CD2 HD2x (12 atoms; CB is fixed).  Charges: every residue is exactly neutral,
  but its fixed part (N H CA HA CB C O) has -0.1842 e and its moving part +0.1842 e: the RIGID bodies are NOT
  neutral; the peptide unit {C,O,N,H} has -0.1144 e.  Born radii at one state: 1.4-4.6 A (H 1.4-2.3, heavy 2.2-4.6):
  heterogeneous inside every group.
- Key identity used everywhere: g = sum_{p,q} W_pq, W_pq = -(kappa/2) q_p q_q M_pq, M = kernel matrix (1/f_GB off the
  diagonal, 1/B_p on it); M does not depend on the charges.
- `p5lib.py` (shared), `s1_cancel.py` (step 1).  Check inside: sum_pq W_pq = P3's G.energy at every state (4.6e-12).
- L6/H (64 states, 1.2 s) and L8/H (256 states, 7.7 s): my totals reproduce P3's Table 3.1 (order 3: 0.268 / 0.597 /
  0.684 and 1.233 / 1.260 / 1.750; order 4: 0.0607, 0.286; order 5: 0.0042, 0.0292) and P3's Gamma_3..5 (131.7, 12.88,
  0.776; 356.6, 49.3, 4.98).  0 violations of the triangle chains.
- FIRST FINDING (L6/H, L8/H), ratio to the exact sum of anchored constants of the total, orders 3/4/5:
    P3 bound            492/212/186      289/172/170
    best pair-by-pair   139/38/23        86/35/24      (sum of exact per-pair constants)
    atom x group (res.) 31/12/8.0        20/10.7/8.7   <- the level the brief's candidate route keeps signed
    atom x all          20/8.3/5.8       13/7.2/6.0
    group x group (res) 4.7/2.5/2.1      3.1/2.4/2.4
    group x all (res.)  2.35/1.6/1.3     1.75/1.45/1.5
  => signs kept on ONE side (atom x neutral group) buy only a factor 2.6-4.4 over the ideal pair-by-pair bound;
     the cancellation is between BOTH sides (residue x residue): factor 15-30.
- S4/H tau .70 (2 916 states, 4.7 s), S5/H (17 496 states, 53 s): P3's Gamma reproduced (4.13, 0.0391; 8.98, 0.212,
  0.00239).  Ratios to the exact total, orders 3/4(/5):  S4: P3 58/297, pair 11.4/47, atom x group(res.) 4.5/18,
  group x group (res.) 1.6/6.9;  S5: P3 71/118/80, pair 15.6/18.6/10, ag(res.) 6.0/7.6/4.7, gg(res.) 2.1/3.1/1.9.
- s1_cancel.py rewritten with --rows a:b / --merge (split over atom rows) so that S6/H (104 976 states) runs as two
  parallel halves < 20 min each: `run_s1_S6.sh` started 02:33 (2 processes, 3 GB each).
- Thinking (while S6 runs), to be tested:
  (a) the cancellation looks INCOHERENT (statistical): pair -> atom level gains ~ sqrt(#partners in range) ~ 5-7;
      there is no small multipole parameter (group size ~ kernel range; Born radii inside a group differ by 2x).
  (b) Step 2 formalisation: M(x) does not depend on the charges => a bound that depends on the charges only through
      |q_p| ("sign-blind"; every term-by-term bound is one) must hold for every sign pattern s, hence is
      >= max_s |Delta_T g_{s o q}|.  Lower bounds on that maximum by local search over s are certified lower bounds
      for the whole class, on the real instances.
  (c) explicit family: 4 charges +-q on a regular tetrahedron of edge r with a common Born radius (two crossed
      neutral dipoles): truth = 2 kappa q^2 |Delta chi_r|, all-plus = 2 kappa q^2 |4 Delta b - 3 Delta chi_r|,
      chi_r = b - h <= (3/8) r^2 b^3  => ratio >= 4|Delta b|/|Delta chi| - 3 ~ (B/r)^2; abstract equidistant family
      with N atoms: ratio >= N |Delta b|/|Delta chi| - (N-1).
  (d) possible better route: "banded exactness" -- evaluate with signs every subset inside a window of w+1
      consecutive sites (an exact (w+1)-body banded model), bound only the NON-LOCAL threshold sets sign-blindly.
      Needs: a generalised remainder identity for down-closed families (proved on paper: threshold sets T not in D,
      T minus min T in D), and the size of sum over non-compact T of P3's chat_T.  To be measured on L8/L12/L16.

## 02:38–02:50  Step 1 complete on five instances; step 2 numerics
- S6/H (104 976 states): two halves of 345 s each + merge 61 s; P3's Gamma_4 = 0.849 reproduced.  First version of
  the s1 logs (without the cross-only regrouped rows) is SUPERSEDED: s1_cancel.py now also computes agx/ggx
  (cross part alone, regrouped), all five instances re-run (the S6 re-run started 02:49).
- Step 1 numbers (ratio to the exact sum of anchored constants of the total; orders 3/4/5):
    S6/H: P3 84/165/221, pair 17.5/16.0/13.9, atom x group(res.) 6.6/6.5/6.0, group x group(res.) 2.4/2.8/2.5.
- `s2_signblind.py` (step 2 on real instances): exact evaluation of sign-flipped systems.  Local search (1-flip
  ascent, 32 starts) for the sign pattern that maximises the mixed difference / the remainder.  Result (L6, L8):
  every bound that depends on the charges only through |q_p| is >= 79/23/17 (L6) and 48/21/15 (L8) times the true
  sum of anchored constants at orders 3/4/5, and >= 153/23/16 (L6), 72/24/38 (L8) times the true sup of the
  remainder.  Ser: 6.4/17 (S4), 8.9/7.9/4.0 (S5).  The lower bound found is within a factor 1.4-2.5 of the pair-level
  optimum, i.e. term-by-term bounds are near-optimal among sign-blind ones.  P3's Gamma is 6-20 times the lower
  bound (per-subset sums), 15-46 (remainder).
  BUG fixed on the way: the per-subset lower bound did not include the pattern found for the remainder (S4 order 4:
  "one pattern for all T" 2.52e-3 was larger than the "best per T" 2.19e-3).  Now LS_T = max of all patterns tried.
- New check of P3's theorem (it must hold for sign-flipped charges because it is sign-blind): Gamma_m >= |remainder|
  at every state for true signs, all-plus and the pattern found: L6 576, L8 2 304, S4 17 496, S5 157 464,
  S6 944 784 state checks, 0 violations.
- `s2_family.py`: explicit family (N equidistant charges, common Born radius).  (F1)-(F6) hold in 6 319 checks,
  0 violations.  With B = 0.34-0.47 nm and r = 0.123 nm: ratio 21/42/165/658 for N = 2/4/16/64 at m = 3.
  Part C (tetrahedron with OpenMM descreening integrals + T_d-symmetric uncharged shells): FIRST version had no
  bath, B = 0.17-0.20 nm, ratios only 2-19; a static symmetric bath of 38 uncharged atoms gives B = 0.35-0.47 nm and
  ratios 45 / 14 / 26 at r = 0.123 nm for m = 3/4/5.
- Dead end noted (not pursued beyond a table): "banded exactness" (candidate (d) above).  On L8/H the non-compact
  triples are NOT small: at sequence diameter 7 the exact c_T is up to 0.046 kcal/mol and P3's bound 0.7-7.9 kcal/mol
  per triple (table from out/s1_L8_H_0.60.json by diameter).  An 8-residue helix (12 A) has no "far" regime.

## 02:50–02:56  While the S6 re-run is going (no other compute): prior art, proofs, planning
- COORDINATOR'S NOTE received (via a reminder in the conversation): if the file-writing tool declines to create or
  update `docs/science/workstreams/P5_REPORT.md`, do not work around it; keep everything in NOTES.md and return the
  findings in the hand-back.  Tested at once: the Write tool CREATED the report file (header only) without objection,
  so the report is written with the normal tool as planned.  No indirect writing of that file is used anywhere.
- Prior-art queries (reading level in brackets; nothing read in full):
  1. WebSearch "group-based cutoff neutral charge groups truncation electrostatics ... Steinbach Brooks" [search
     snippets]: charge-group (neutral-group) truncation of Coulomb sums is classical; Steinbach & Brooks, J Comput Chem
     15 (1994) (crossref record 10.1002/jcc.540150702); Ni & Baumketner (PMC3204157); Kubincova, Riniker, Hunenberger,
     PCCP 2020 (d0cp03835k).  Known both to reduce cut-off artefacts and to create others.
  2. WebSearch "maximum of quadratic form over sign vectors Grothendieck cut norm Alon Naor" [search snippets]:
     max over sign vectors of a quadratic/bilinear form = cut-norm type quantity, MAX SNP-hard, SDP relaxation within a
     constant (bilinear) or O(log n) (quadratic forms on graphs, Alon-Makarychev-Makarychev-Naor).
  3. Consensus "generalized Born energy pairwise decomposition error cancellation ..." [3 abstracts]: Gaillard &
     Simonson, J Comput Chem 2014 (pairwise decomposition of MMGBSA for protein design); Gaillard, J Phys Chem B 2025
     (residue-pairwise GB, "fluctuating dielectric boundary"); Sevim et al., bioRxiv 2026 (collinearity of Coulomb and
     GB terms in MM-GBSA, R^2 >= 0.99).
  4. PubMed "fluctuating dielectric boundary generalized Born protein design": 2 hits (PMID 28749575, 41055950), not opened.
  5. WebSearch "Still Tempczyk Hawley Hendrickson 1990 ... dipole" [search snippets]: Still et al., JACS 112 (1990)
     6127; Onufriev & Sigalov 2011 (PMC3100913) on gross errors of the canonical formula; nothing found on the
     dipole limit (my (3/8)|mu|^2/B^3 expansion is derived in the report, not cited).
- Proofs written out on paper (to go into the report): Proposition 7 (sign-blind bounds: >= max over sign patterns;
  term-by-term bounds are sign-blind; P3's is term-by-term), Theorem 9 (equidistant family; 0 <= 1 - psi(u) <= 3u/8
  proved by a polynomial inequality valid for u <= 8/3, trivial beyond), Proposition 10 (remainder identity for any
  down-closed family; threshold sets).
- Why "signed at a reference" cannot be cheap (argument, to be stated as [H] with the measured numbers): the signed
  leading term of each subset T costs as many evaluations as the next ball; the remainder after ONE signed order is
  the sign-blind bound of the next order times the number of sites that can deviate, i.e. (m+1) Gamma_{m+1} ~ 0.6
  Gamma_m on the helix (Gamma ratio 5-8): no gain.
- Plan for the remaining time: (1) s1 on L12/H up to order 6 (enumerable: 4 096 states) to see truth, best
  pair-by-pair and P3 at the order P3 says is needed on the helix; (2) s3_locality.py; (3) IF time: P3's own recipe
  with SITE penalties at m = 6 on L12/L16 (P3 did not run it; its "fails on the helix" is for the constant bound).

## 02:56–03:02  More statements; runs in progress
- CORRECTION OF MY OWN READING: "every sign-blind bound >= sum over T of the best pattern per T" is true only for the
  ARCHITECTURE "sum over subsets of per-subset sign-blind bounds" (P3's Gamma_m is of that kind).  A sign-blind bound
  of the SUM needs only >= max over single patterns s of sum_T c_T(g_s).  The tables now give three lower bounds:
  (A) sum_T best pattern per T; (B) best single pattern for the sum; (C) remainder sup-norm (single pattern).
  (C), the cleanest: Leu6 153/23/16.5, Leu8 72/24/38; Ser4 4.3/19, Ser5 5.5/4.0/4.0, Ser6 8.2/6.0/3.4.
  => for Leu on the helix no sign-blind bound of the order-m remainder is within a factor ten (m = 3, 4, 5);
     for Ser on the helix the theorem does not exclude it (the pair-by-pair optimum is 10-17 times the truth there,
     P3's bound 58-300 times: the slack of P3's inequalities is the larger part).
- s3_locality.py part (a): Proposition 10 (remainder identity for a down-closed family) verified: 22 140
  (state, family) checks, 0 violations, largest deviation 7e-14; its bound with exact constants: 20 988 checks,
  0 violations, ratio bound/|remainder| in [1, 2e5].
  part (b), L8 and L12 on the helix: subsets outside a window are NOT small.  L12, order 3: the 52 triples of
  sequence diameter >= 9 have exact constants summing to 0.25 kcal/mol (max 0.016) and P3 bounds summing to 30.9
  (0.06-1.6 each); order 4, diameter >= 9: exact 0.165, P3 16.3.  "Banded exactness" is dead with sign-blind tails.
- New statement, Proposition 11 (signed reference term): sup_z |Delta_T g(z;y)| <= |d_T(y)| + sum_{j not in T}
  c^anch_{T+j}; summed: sum_T c_T <= sum_T max|d_T| + (m+1) sum_{T'} c_{T'} (order m+1).  Proof by P3's Prop. 1 at order 1
  applied to z -> Delta_T g(z; y).  It says a signed reference term costs the ball of radius m and still pays the
  sign-blind order m+1, (m+1) times: dominated by P3's recipe at order m+1.  Script: s4_refbound.py (to run).
- floor_p3copy.py = verbatim copy of ws_P3/run_floor.py + `import p5lib` (diff checked: identical up to 4 added lines).
  run_floor_helix.sh wraps it.  To be run: L12/L16 (enumerated) and L20 (not enumerated) on the helix at m = 6 with
  site penalties -- a regime P3 did not run (its "fails on the helix" is for the constant bound).
- Running since 02:57/02:59: s3_locality.py (L16 part), s1_cancel.py L12 H 0.60 6.

## 03:02–03:06  Locality dead end quantified; FIRST POSITIVE RESULT on the helix
- s3_locality.py finished (391.7 s; the L16 enumeration with P3's evaluator took 377 s of it).  L16/H order 3: all 560
  triples: exact sum of anchored constants 7.449 kcal/mol (P2's measured 7.4), P3's bound 1 819 (P3's Gamma_3).  Triples
  with first and last site >= 9 apart (280): exact 1.02, P3 123; >= 13 apart (76): 0.117 / 7.79; the 14 triples
  spanning the whole chain: exact 0.0147 (max 5.4e-3), P3 0.83.  Slow (power-law) decay: banded exactness is dead.
- `./run_floor_helix.sh L12 6 --N 20000` (P3's pipeline, verbatim copy, SITE penalties, m = 6; 27 s):
    Gamma_6 = 2.988 kcal/mol (P3's table: 2.99), gamma_i = 0.14-0.33 kcal/mol; ball of radius 5: 1 586 evaluations
    (38.7 % of 4 096); sandwich m_- <= E <= m_+ at all 4 096 states: 0 violations;
    DETERMINISTIC bracket [374.2091, 374.5277] (0.319 nats), exact ln Z(E) = 374.345343; cost number 0.200;
    Hoeffding (20 000 samples, delta 0.05): [374.3309, 374.3540] (0.023 nats); Bennett with certified b, s2: 0.193 nats.
    Mean number of sites off the anchor under pi_{m_-}: 0.61; only 10 distinct states among 20 000 samples.
  P3's own table has for the same instance and order with the CONSTANT bound: cost number 151, deterministic bracket
  10 nats.  P3 did not run site penalties on the helix beyond 8 residues.  So "the recipe fails on the helix at every
  affordable order" is a statement about the constant bound; with the floor as a function it works at 12 residues.
  The reason is not a tighter tail (the tail bound is the same sign-blind Gamma_6) but that the ensemble is nearly
  frozen at the anchor, where site penalties cost nothing.
- Started 03:05: `./run_floor_helix.sh L16 6 --N 20000` (65 536 states, enumerated).

## 03:06–03:08  Leu16 on the helix certified at order 6 with site penalties
- `./run_floor_helix.sh L16 6 --N 20000` (162 s): Gamma_6 = 8.032 kcal/mol (P3: 8.03), gamma_i = 0.21-0.73 kcal/mol
  (0.35-1.23 kT); ball of radius 5: 6 885 evaluations (10.5 % of 65 536);
    sandwich at all 65 536 states: 0 violations (m_- > E: 0; m_+ < E: 0);
    exact remainder g - I_5 g in [-1.25e-3, 1.34e-2] kcal/mol (certified bound 8.03: 600 times larger);
    DETERMINISTIC bracket [483.6408, 484.1640] (0.523 nats); exact ln Z(E) = 483.846587 -- the coordinator's value
    483.8466 (A17 (10)) reproduced by a different pipeline; cost number 0.374; the anchor is the certified minimiser;
    Hoeffding (20 000 samples, delta 0.05): [483.8328, 483.8592] (0.026 nats); Bennett (certified b = 0.76, s2 = 1.15):
    0.473 nats; mean number of sites off the anchor 0.69; 10 distinct sampled states.
  So the helix at sixteen residues IS certified by P3's recipe when the floor is a function; P3's negative statement N2
  (constant bound, e^{13.5}) does not apply to the site-penalty form, which P3 did not run beyond 8 residues.
- L16 enumeration inside the pipeline took 100 s => L20 (1 048 576 states) would take ~40 min: run with --noenum and
  compare with the coordinator's fitted-chain value 593.3030.  Started 03:07:40.
- Planned next: s2 on L12 (orders 3-6), s4_refbound, s2_family re-run (parts D, E added), then L30 --noenum.

## 03:08–03:12  Leu20 on the helix (1 048 576 assignments, NOT enumerated): certified bracket
- `./run_floor_helix.sh L20 6 --N 50000 --noenum` (252 s): Gamma_6 = 14.479 kcal/mol, gamma_i = 0.25-1.07 kcal/mol
  (0.41-1.80 kT); ball of radius 5: 21 700 evaluations (2.07 % of the domain); band w = 19 (all pairs in the band);
    DETERMINISTIC bracket [593.0653, 593.6992] (0.634 nats), no sampling;
    Hoeffding (50 000 exact samples of pi_{m_-}, delta 0.05): [593.2964, 593.3144] (0.018 nats);
    Bennett (certified b = 0.98, s2 = 1.81): 0.639 nats; ln Z of the midpoint model (not a certificate): 593.3047;
    E >= m_- at every sampled state (asserted by the pipeline); mean number of sites off the anchor 0.74; 21 distinct
    sampled states.
  The coordinator's uncertified fitted-chain estimate (A17 (10)): 593.3030 +- 0.0001 -- inside both brackets.
- P3's own helix runs (checked in ws_P3/out and its batch files): site penalties only for L8/H at m = 4, 5; constant
  bound for L8/H, L12/H at m = 3..6; nothing for L16/H.  P3's L12/H m = 6 constant: cost number 150.9, deterministic
  width 10.04 nats, same exact ln Z 374.3453434.
- Started 03:12: `./run_floor_helix.sh L30 6 --N 50000` (1.07e9 assignments; ball 174 437 evaluations).
- s1 on L12/H (orders 3-6) is still in its last step (P3's bound for each of the 2 431 subsets).

## 03:12–03:14  A run of mine was about to exceed 20 minutes: killed and split
- `s1_cancel.py L12 H 0.60 6` (started 02:59:00): exact constants done after 397 s, then P3's bound subset by subset
  for 2 431 subsets -- about 0.6 s per subset at order 6 with 240 atoms, no progress output, estimated end ~03:18-03:20,
  i.e. at the 20-minute limit.  KILLED at 03:13 (exit 144); its log is incomplete and NOT cited.
  Fix: `--p3max K` (P3's bound per subset only up to order K; above it only the closed-form sum Gamma_m, which equals
  the sum over subsets to 1e-16 on every instance where both were computed) and `run_s1_L12.sh` = two runs
  (`--rows 0:240` checkpoint, then `--merge --p3max 5`), each < 10 min.  Started 03:14.
- NOTE: my test of the new option (`s1_cancel.py L6 H 0.60 5 --p3max 4`) overwrote logs/s1_L6_H_0.60.log and
  out/s1_L6_H_0.60.json with a reduced version; `run_s1_small.sh` must be re-run before the tables are made.
- s2_signblind.py now takes the per-order sums of 'pair' and 'P3' from the s1 JSON ("sums") and tolerates missing
  per-subset P3 values; mk_tables.py likewise.

## 03:14–03:24  Leu30: the first attempt would have run ~30 min; killed and split
- `./run_floor_helix.sh L30 6 --N 50000` started 03:12:  582 atoms; the ball of radius 5 has 174 437 states at ~6 ms
  each (~17-19 min alone).  KILLED after 2 min (log renamed logs/SUPERSEDED_floor_L30_H_m6_siteres_killed.log; not
  cited).  `ball_precompute.py` evaluates the ball in parts and writes the pipeline's own cache file
  (cache/ball_L30_H_t0.60_gbn2_M5_20f5b82d67.npz: same anchor routine, same state list, same evaluator as
  run_floor.py; the pipeline reads it only if the state list is identical); `run_floor_L30.sh` = part 0, part 1, merge,
  pipeline with N = 20 000.  Part 0: 87 218 evaluations in 552.9 s (03:14:22-03:23:35).  Part 1 + merge + pipeline
  started 03:23:40.
- L12 step 1, first of two runs: DONE in 509.3 s (phase A).  Second run (merge, P3 per subset up to order 5) running.
- s2_signblind.py: new option --lsmax K (per-subset local search only up to order K), because 2 431 subsets of
  Leu12 with 64-state kernel differences would take ~15 min.
- Ranges from out/tables.md (five instances, orders 3-5): pair/(atom x group) 1.57-4.4 over the four groupings
  (2.15-4.4 for residues); (atom x group)/truth 8.0-53 (Leu), 4.5-24 (Ser); (residue x residue)/truth 1.6-6.9;
  pair/(residue x residue) 5.3-30; P3/pair 3.4-15.9; Gamma_m/true remainder sup 80-2 315.

## 03:24–03:27  Leu12 on the helix, step 1, orders 3-6 (4 096 states; two runs, 509 s + 215 s)
- 107 206 inequality checks, 0 violations.  Sums over subsets of exact anchored constants, kcal/mol (ratio to truth):
    order   truth     pair-by-pair    atom x residue   atom x all   residue x residue   P3 (Gamma_m)    true remainder
      3     3.921     310.2 (79)      73.4 (18.7)      47.1 (12.0)  11.9 (3.0)          1033.5 (264)    [-0.125, 0.779]
      4     1.065     39.86 (37)      11.94 (11.2)     7.87 (7.4)   2.70 (2.5)          188.7 (177)     [-0.174, 0.032]
      5     0.1757    3.988 (22.7)    1.430 (8.1)      0.954 (5.4)  0.401 (2.3)         26.90 (153)     [-0.0158, 0.0085]
      6     0.02199   0.3319 (15.1)   0.1325 (6.0)     0.0886 (4.0) 0.0466 (2.1)        2.988 (136)     [-0.00042, 0.0092]
  => at the order the helix needs (6): P3's bound is 9.0 times the best pair-by-pair bound and 136 times the truth;
     the one-sided signed ideal (atom x residue) is 6.0 times the truth, the pair-by-pair ideal 15 times.
     The pair-by-pair optimum falls by 7.8, 10.0, 12.0 per order; P3's bound by 5.5, 7.0, 9.0; the truth by 3.7, 6.1, 8.0.
- Started 03:26: s2_signblind.py L12 H 0.60 6 --lsmax 4 --nrand 4.

## 03:25–03:31  Sign-blind lower bounds on Leu12, orders 3-6
- First run `s2_signblind.py L12 H 0.60 6 --lsmax 4 --nrand 4` (250.9 s; SUPERSEDED by the run below, its log was
  overwritten): (C) remainder: every sign-blind bound / truth >= 51 (m=3), 34 (m=4), 20 (m=5), 3.8 (m=6).
  At order 6 the search was weak (3 candidate states, 6 starts) and the lower bound is only 3.8: with what I have,
  a sign-blind bound within a factor ten at order 6 is NOT excluded on Leu12 (the pair-by-pair optimum summed over
  subsets is 0.332 = 36 times the true remainder sup 0.0092, so the least sign-blind bound is in [3.8, 36] there).
- Second run with a stronger remainder search (`--ncand 6 --nrandrem 30`: 13 candidate states, 32 starts each),
  started 03:30.

## 03:31–03:40  Leu12 sign search (final), Proposition 11 numbers, family (final), report sections written
- Second s2 run on L12 (296.6 s; `--lsmax 4 --nrand 4 --ncand 6 --nrandrem 30`): the stronger remainder search found
  the same values: (C) >= 51 / 34 / 20 / 3.8 at m = 3 / 4 / 5 / 6.  P3's Gamma_m at every state of the sign-reversed
  systems: 49 152 state checks, 0 violations.  So: at orders 3-5 no sign-blind bound of the remainder is within a
  factor ten on Leu6, Leu8, Leu12 (16.5-153); at order 6 (Leu12) only >= 3.8 is shown and the pair-by-pair optimum is
  15 x sum of constants = 36 x remainder sup: OPEN at the order the helix needs.  (Per-subset search at orders 5, 6 of
  Leu12 not run: it would take ~15 min.)
- s4_refbound.py (62.4 s): (*) and (**) of Proposition 11: 59 084 checks, 0 violations, bound/exact in [1, 1.8e3].
  Certified version sum max|d_T| + (m+1) Gamma_{m+1} vs Gamma_m vs Gamma_{m+1} (kcal/mol):
    L6 m=3: 51.7 / 131.7 / 12.9;  m=4: 3.93 / 12.9 / 0.776;   L8 m=3: 198 / 357 / 49.3;  m=4: 25.1 / 49.3 / 4.98;
    S4 m=3: 0.227 / 4.13 / 0.0391;  S5 m=3: 0.972 / 8.98 / 0.212;  m=4: 0.0137 / 0.212 / 0.00239;
    S6 m=3: 3.59 / 17.0 / 0.849;  m=4: 0.103 / 0.849 / 0.0196.
  => 1.8-3.3 times better than Gamma_m for Leu, 4.7-18 for Ser, and always 4-6 times worse than Gamma_{m+1}, which
     needs the same evaluations.
- s2_family.py final (0.6 s): 6 811 checks, 0 violations.  Part C at r = 0.123 nm: 44.6 / 13.8 / 25.8 (m = 3/4/5).
  Part D: 240 random neutral clusters, remark's bounds hold.  Part E (two dipoles at distance R, common Born radius,
  m = 3): parallel 16, 14, 21, 29, 25, 22 at R = 0.2 ... 2.0 nm; antiparallel 108, 3851, 35, 28, 24, 22.
- run_rest.sh re-ran the four small s1 instances (L6 restored: 1.8 s; L8 12.6 s; S4 5.6 s; S5 110.0 s), then s4,
  s2_family, and is re-running s2 on the five instances.
- L30: ball part 1 done (87 219 evaluations), merge: 24 random ball states re-evaluated with P3's own evaluator,
  largest deviation 4.2e-11 kcal/mol; pipeline started 03:36:10.

## 03:40–03:47  All short runs final; Leu30 deterministic bracket
- run_rest.sh finished (03:45): s1 small instances restored, s4, s2_family, s2 on five instances re-run (5.3, 43.3,
  2.7, 43.6, 322.8 s): Table 2 identical to the earlier one (same seed, same data).
- Totals of checks.  s1: 129 804 states enumerated, 121 780 inequality checks, 0 violations.  s2: 16 296 chain checks,
  0 violations; 1 171 776 state checks of P3's Gamma_m on sign-reversed systems, 0 violations, Gamma_m/sup|rem| from
  15.2 to 2 315.  (I had written 27 114 chain checks in the report draft: wrong sum, corrected to 16 296.)
- L30 pipeline (started 03:36:10): Gamma_6 = 32.674 kcal/mol, gamma_i up to 1.594 kcal/mol (2.67 kT) [364.8 s];
  "ball values read from ball_L30_H_t0.60_gbn2_M5_20f5b82d67.npz" (the checkpointed ball was accepted: identical
  state list); 174 437 evaluations = 0.0162 % of 1.07e9;
    DETERMINISTIC bracket [866.6507, 867.3804] (0.730 nats); coordinator's fitted chain 866.9139 +- 0.00003: inside;
    midpoint model (not a certificate) 866.9151; min m_- = -516.4958, min m_+ = -516.4951 kcal/mol.
  Sampling (20 000) in progress.

## 03:47–03:53  Leu30 done; report finished; nothing left running
- L30 pipeline finished (694 s; log logs/floor_L30_H_m6_siteres.log complete): Hoeffding (20 000 samples, delta 0.05)
  [866.9000, 866.9306] (0.0306 nats); deterministic [866.6507, 867.3804]; Bennett 0.865; 0.79 sites off the anchor;
  19 distinct sampled states; E >= m_- at every sample.  Coordinator's fitted chain 866.9139: inside both brackets.
  Total for Leu30: ball 552.9 + 716.2 s, merge 10.4 s, pipeline 694 s (four runs, each < 20 min).
- Sandwich checks by enumeration inside the pipeline (L12, L16): 139 264 state checks, 0 violations; largest E - m_-
  5.12 / 12.00 kcal/mol vs certified max(m_+ - m_-) 9.45 / 22.77.
- Family, part B: (exact factor)/(bound (iii)) between 1.0 and 15.8 over the 111 cases with a positive bound.
- Coordinator's commits seen (read-only): 8ad0a24 (snapshot of my notes and scripts), 3959dce (pruned-domain note at
  the head of P3_REPORT: for Val, Leu, Ser the pruned product is the whole clash-free domain => my instances are
  unaffected; said so in the report header).
- Report `docs/science/workstreams/P5_REPORT.md` complete (written with the normal Write/Edit tool throughout; no
  indirect writing).  All "(pending)" markers gone; ranges in the text taken from out/tables.md (block `ranges`).
- Final state of processes: none of mine running (checked with ps at 03:51 and 03:52).  out/tmp/ is empty.
- Files: p5lib.py, s1_cancel.py, s2_signblind.py, s2_family.py, s3_locality.py, s4_refbound.py, ball_precompute.py,
  floor_p3copy.py (verbatim copy of P3's run_floor.py + 1 import), mk_tables.py, run_*.sh; logs/, out/, cache/.
- NOT done / open (also in the report, sections 9-10): exact enumeration of Leu20 (~40 CPU-min); per-subset sign
  search at orders 5-6 of Leu12; breakdown of P3's slack by type of pair; a compact ensemble that is not frozen
  (patterned sequence on the helix); order 7.
