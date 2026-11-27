# R28 — NOTES (kept from the first minute)

Internal adversarial review by an AI agent (not external peer review).
Write area: `/home/user/MetricChain/experiments/science/ws_R28/` and
`/home/user/MetricChain/docs/science/workstreams/R28_REPORT.md` only.

Times are read from the clock (`date -u`) at the moment of writing.

## Log

* 2026-11-26T23:49Z — start.  Read `R28_brief.md` in full and `COMMON.md`.  Branch
  `research/scientific-translation`, head `eec5c16`.  `git status --short` showed two untracked
  entries that are not mine (`docs/science/workstreams/R28_brief.md`, `experiments/science/ws_R27/`).
  Created my directory.  Machine: 4 cores, 15 GB, Python 3.13.18.
* Rules I hold myself to: 3 GB address-space cap in every script; peak memory in last line;
  `OMP_NUM_THREADS=1`; at most 2 processes; no run > 10 min; `python3 -B`; fresh log names;
  prediction before each replication run; control that can fail for each check; four kinds of
  checking kept apart (review / replication / re-run / read only).
* I will NOT open parts (13)–(18) of `INFERENCE_LIMITS_ADDENDA.md`; I read lines 4159–4424 only
  (with offset/limit), and other parts only if a statement under review cites them.

## Tool actions declined

none (final; nothing was declined during the session)

## Web addresses opened (kept current; details in the search log below)

1. https://ar5iv.arxiv.org/html/1610.07277  (fetch tool; its summary of the full text)
2. https://arxiv.org/abs/1806.06064  (fetch tool; listing/abstract)
3. https://donaldlab.cs.duke.edu/Supplementary/jcb16/lute/LUTE.submit.pdf  (PDF saved by the fetch tool; text extracted with pdftotext into the session scratchpad; passage read by me)
4. https://www.biorxiv.org/content/10.1101/368522.full  (fetch tool; its summary of the full text)
5. https://cs.pwr.edu.pl/zielinski/publications/papers/fss08.pdf  (PDF; text extracted; passages read by me)
6. https://cs.pwr.edu.pl/zielinski/publications/papers/survey16.pdf  (PDF; text extracted; passages read by me)

* (time not read from the clock; between 23:49:37Z and 23:54:02Z by my shell outputs) — read (full): INFERENCE_LIMITS_ADDENDA.md lines 4159–4424 only (offset/limit read);
  SCI-REV-0025.md (all 146 lines); SCI-REV-0026.md lines 1–289 (§0–§6); SCI-MSG-0035.md lines 36–65 (§2).
  NOT yet opened: any script under review (I want my toy-chain code written from the statement first).

### First-pass review notes on Proposition A17.24 (before any code) — to be firmed up in the report

1. `ν` in (a) is never defined; it has to be the product `ν_1 ⊗ … ⊗ ν_n` (otherwise `v_s = Π v_{i,s_i}` is false).
2. (a): law of total probability on product cells — fine for a product `ν`.
3. (b): Jensen — valid for ANY probability measure on the cell; the product is needed only so that
   `⟨V_T⟩_s` depends on `s_T` alone and `v_s` factorises.
4. (c): W = Σ_T V_T^s ≤ V on the cell; W is a function of the H-coordinates; McDiarmid's MGF bound with
   `λ = −1` gives `Σ c_i²/8`.  The constant `c_i = Σ_{T∋i} o_{T,i}` is a VALID bounded-difference constant
   (osc of a sum ≤ sum of osc; sup of a sum ≤ sum of sups) but not the tight one
   (tight: sup over the window of osc_{x_i} of Σ_{T∋i} V_T^s — still a function of s on the same window).
   => Remark (1) "of order Σ_i (L_i h)²/8" with `L_i` defined through V ("If V changes by at most L_i h")
   is not what (c) delivers: (c) delivers Σ_i (Σ_{T∋i} L_{T,i} h)²/8.  Decomposition dependence.
5. Candidate counterexample to (c) WITHOUT product reference (two perfectly correlated two-point
   coordinates, W = a(x1+x2)): ln cosh(a) > a²/4.  So "needed only by the proof" (item 99 (ii)) is the
   wrong class: removal makes (c) as stated false.  To be checked numerically.
6. Hard wall / V = +∞ on part of a cell: (b) degenerates to 0; mode M repairs the upper end only.
   Item 99 (ii) "bounded oscillation — replaceable: mode M" is about the upper end only.  Check on toy.
7. Trapezoid closed cells: legitimate — equivalent to a genuine partition of an enlarged space in which
   each boundary point is split into two half-weight copies; more generally the proposition holds for
   any mixture decomposition ν_i = Σ_s v_{i,s} ν_{i,s} (cells need not be disjoint).  To be checked
   numerically (closed/trapezoid cells versus half-open cells: both must satisfy (a)–(c) exactly).
8. Measurability of inf over M-coordinates; "V bounded" does not make each V_T bounded.  Pedantic.
9. Item 99 (ii) last class: "with [bond lengths/angles] free the sites are no longer independent under
   any natural reference" — doubtful: in bond-angle-torsion coordinates the Jacobian is a product
   (from memory, to be checked numerically if time permits); what is lost with a free backbone is the
   locality of the terms, not the product reference.
10. "interpolated between 96 and 144" for 147 cells: 147 lies outside [96, 144] (width at 144 is
    0.00105 > 1e-3) — an extrapolation.  "width over J²: 0.027 …" looks like TOTAL width / J² at 48 cells
    (0.0103·8/4 = 0.0206), not per angle.  To be checked against the log.

* (time not read from the clock; before 23:56:25Z, the start stamp of toy_selftest_01.log) — wrote `r28_common.py` (3 GB cap, peak memory line), `toy_lib.py` (my own
  implementation from the statement of items 97–98; nothing of `continuous_cells.py` read yet),
  `toy_selftest.py`.
  PREDICTION (before first run of toy_selftest.py): T1–T4 zero violations; control C2 (oscillation
  × 0.3) produces per-state violations of (c) in a good fraction of models; control C3 (full
  end-point weights) breaks (a) in all 60; T5: ln cosh a > a²/4 for a ≤ 2, not at a = 4.
* (time not read from the clock; between 23:56:38Z and 23:56:52Z by the two log stamps) — `toy_selftest_01.log`: SELFTEST FAILED — MY OWN ERROR: the brute-force
  reference in `toy_lib.brute_force_check` computed `exp(-<W> + penalty)` in the linear domain and
  overflowed (13 "violations" of T1 with difference inf, a RuntimeWarning in the log).  The
  transfer-matrix code is in the log domain; the reference was not.  Fixed the reference
  (log domain); the failing log is kept under its name.  Everything else as predicted
  (T2, T3 zero violations; C2 176 hits; C3 60/60; T5 as predicted).
* 2026-11-26T23:57:18Z — MY OWN ERROR (process): three earlier entries carried times I had estimated
  instead of reading the clock (the brief: "a time written into a file is read from the clock at that
  moment").  Replaced by what the shell outputs and log stamps bound.  From here on every time in
  this file comes from `date -u` in the same command that writes the line.
* 2026-11-26T23:57:18Z — `toy_selftest_02.log`: SELFTEST PASSED (reached its last line).  360 (model, mode)
  combinations by brute force from the definitions (closed trapezoid cells and half-open cells; all-H,
  all-M, random modes; with and without separate one-body terms): transfer matrices equal brute force
  to 4.6e-13; (a) 0 violations of 360; per-state (b), (c): 0 models with a violated state.
  Controls: oscillation × 0.3 → 176 models with a state violating (c); full end-point weights → (a)
  fails 60/60.  T5 (correlated reference): ln cosh a > a²/4 for a = 0.1 … 2 — the smallest
  counterexample to (c) without a product reference; (Σ c_i)²/8 holds.
* 2026-11-26T23:58:10Z — wrote `toy_run.py` (driver).  `continuous_cells.py` and its log still unopened.
  PREDICTION for stage A (my own random phases, seed 28; J = 2; one-body terms in the reference):
  (P1) first-order width per angle within ±25 % of the table's row 1 at every k (phases differ);
  (P2) all-H width within a factor 1.5 of row 2 at every k;
  (P3) exponents between 24 and 96 cells: −1.00 ± 0.02 and −2.10 ± 0.10;
  (P4) cells for 1e-3 nats per angle between 125 and 170, and the crossing lies ABOVE 144
       (so "interpolated between 96 and 144" would be an extrapolation);
  (P5) position of the exact value between the Jensen and the all-H end: 0.10–0.30 for k ≥ 24;
  (P6) controls: oscillation × 0.3 excludes the exact value at every k ≥ 24, and × 0.5 at none or few
       (the exact value sits below 1/4 of the way); minima-as-lower-end fails at 8 of 8;
  (P7) local search over modes at k = 3, 6 improves on the threshold rule by less than 20 %.
* 2026-11-26T23:59:26Z — `toy_stageA_seed28_01.log` (reached its last line; 56.5 s; 308 MB).  Stage A with
  MY phases (seed 28), before opening their script:
  first-order 3.296 1.944 0.962 0.4699 0.2336 0.1166 0.07773 0.03886 (table: 3.28 1.95 0.969 0.478 0.238
  0.119 0.0791 0.0396); all-H 4.734 1.274 0.2379 0.04658 0.01018 0.002373 0.00103 0.0002514 (table: 4.70
  1.27 0.239 0.0474 0.0103 0.00241 0.00105 0.000255); exponents −1.0052 and −2.1476 (text: −1.005, −2.148);
  position 0.144 (k=24) … 0.2097 (k=288) (text: 0.14 to 0.21); cells for 1e-3: 146.1 (text: 147) and the
  crossing is BEYOND 144, i.e. an extrapolation from (96,144) — P4 met.
  all-M upper end with the Jensen lower end: 1.084 (k=3), 0.6875 (k=6); best threshold rule 1.076, 0.6424;
  local search over modes 1.076, 0.6047 — the table's row 3 has 1.29 and 0.651 (their phases; to compare
  in stage B).  611 brackets, 0 exclude the exact value.
  Controls: oscillation × 0.3 excludes the exact value at k = 12…288, × 0.1 at all eight k, × 0.5 nowhere
  (so "a deliberately too small oscillation" must be below ~0.45 of the true one to be caught: the
  control is informative only for a factor well below 1/2 — to be said in the report);
  minima as a "lower end": above the exact value 8 of 8; Jensen as "upper end": below it 8 of 8.
  Predictions P1–P7: all met.
  NOW opening `continuous_cells.py` and `continuous_cells.log` (for the specification: phases, wall,
  threshold rule, auxiliary runs) — from this point my toy code is no longer blind to theirs.
* 2026-11-27T00:01:17Z — opened `continuous_cells.py` and `continuous_cells.log` (read in full).
  Specification facts NOT in the text of item 98:
  (s1) one-body terms are 1.5(1 + cos(3x + φ_i)) with RANDOM phases φ_i — the text says "1.5(1 + cos 3x)";
       with φ = 0 the three wells are centred in the three 120° cells (my stage A), with random φ they
       are not; this matters at k = 3 (my stage A mixed width 1.08 against their 1.29);
  (s2) the "smooth wall of height W between neighbours" is ONE Gaussian-like bump of width σ = 0.6 rad
       (34°) at a random point (a_i, b_i) of each neighbour pair's torus:
       W exp(−(2 − cos(x_i−a_i) − cos(x_{i+1}−b_i))/σ²); its largest slope is about W/(σ√e) ≈ 20 kT/rad
       for W = 20 — far gentler than a steric wall;
  (s3) "best choice of modes by a threshold" = best of the nine thresholds (inf, 6, 4, 3, 2, 1.5, 1, 0.5, −1)
       on cmax_i[cell] = largest all-H penalty argument the coordinate can meet;
  (s4) the 147 cells: their `k_needed` interpolates log-log between the two computed points that
       straddle the target, i.e. between 144 (1.05e-3) and 288 (2.55e-4) — the text says "interpolated
       between 96 and 144";
  (s5) "width over J²: 0.027, 0.025, 0.021, 0.015" are TOTAL widths (8 angles) over J² at 48 cells
       (log: 6.838e-03/0.25 = 2.735e-02), in a sentence about the width per angle;
  (s6) 41 partitions = 8 + 7 + 7 + 7 + 3·3 + 3 — confirmed by the log.
  Wrote `toy_stageB.py`: MY library on THEIR instance (seed 20261126, their order of draws), parsed
  comparison with all 41 rows of their log.
  PREDICTION (stage B): all 8 exact values agree to 6e-11 and all 41 rows agree — the five bracket ends to
  1e-6 (their print precision), the same best threshold and the same number of M-cells, widths per site to
  3 digits, position to 3 decimals; 0 disagreements.  Local search over modes improves their mixed width at
  k = 3 and 6 by a few per cent (less than 20 %).  Controls: Jensen-as-upper violated 41/41;
  minima-as-lower violated 41/41; oscillation × 0.1 excluded in all 41, × 0.3 in most with k ≥ 12,
  × 0.5 in few or none.
* 2026-11-27T00:03:06Z — `toy_stageB_01.log` (reached its last line; 78 s; 514 MB).  REPLICATION of item 98 with my
  code on their instance: 49 items compared (8 exact values + 41 rows; per row the five bracket ends, the best
  threshold, the number of M-cells, three widths, the position): 0 disagreements; largest |mine − theirs| over
  the 205 bracket ends 4.9e-07 (their print has six decimals).  2409 brackets (nine thresholds + local-search
  flips), 0 exclude the exact value.  Controls: Jensen-as-upper violated 41/41; minima-as-lower violated 41/41;
  all-H with oscillations × 0.1 excluded 41/41, × 0.3 34/41, × 0.5 0/41.  Prediction met in every part.
  Derived numbers from my values: exponents −1.0053, −2.1481; positions 0.1435 … 0.2092; 147.3 cells by log-log
  interpolation between 144 and 288 (147.2 by the power law through 96 and 144 — an extrapolation); 0.010342 and
  0.0096796 per angle at n = 8, 16; uniform/tilted 4.740 at 48 cells (2.19 at 3 cells … 4.95 at 144 — the
  "4.7 times" is the value at 48 cells only); wall: 80.5, 38.2, 7.65 (all-H) against 3.86, 2.26, 1.06;
  ratio 1.311 at 96.
  Findings (all minor): (m1) "interpolated between 96 and 144" is wrong (144–288); (m2) "width over J²"
  = total over 8 angles (per angle: 0.0034, 0.0032, 0.0026, 0.0018); (m3) the text omits the random phases
  of the one-body terms; (m4) the "wall" is a single smooth bump per neighbour pair; (m5) local search over
  modes beats the threshold rule by up to 10 % (case B, k = 12: 0.349 → 0.316; case A, k = 6: 0.651 → 0.620) —
  "best choice of modes by a threshold" is the best of nine thresholds, not the best assignment.
* 2026-11-27T00:03:59Z — read (full) `continuous_cells_real.py`, `continuous_cells_real_tables.py` (+ .log),
  the committed logs `…_L_H_144.log`, `…_VV_H_144.log`; `ws_P2/scbuild.py` and `ws_P/pepbuild.py` (the energy
  source: needed to call the builder myself).  Facts: every TORSION is a site (n = number of torsions);
  the whole energy is one term; E = groups 0–3 (ff14SB vacuum) + group 5 (GBn2 polar), divided by 0.596;
  3-cell partition = closed cells [0,120], [120,240], [240,360] with trapezoid end weights; tilted
  reference = slices through the grid minimum, remainder V = E − Σ e_i (E zero at the minimum).
  PREDICTION (re-run of their script, L H 144 and VV H 144, cache in my directory): the two logs are
  identical to the committed ones in every character except the three timing fields ("computed in N s",
  "ALL DONE N s", "peak memory N MB").
* 2026-11-27T00:06:38Z — RE-RUN (their script, cache in `ws_R28/cc_cache`, shell cap `ulimit -v 3145728`):
  `rerun_L_H_144_01.log` and `rerun_VV_H_144_01.log` reached their last lines; `diff` against the committed
  logs: only line 1 ("computed in 13 s" vs 14; 18 vs 11) and line 45 ("ALL DONE" times) differ — every number
  identical, digit for digit.  Prediction met.  No bytecode written into ws_P / ws_P2 (checked mtimes).
  Observed: `git status --short` now lists `R29_brief.md` and `ws_R29/` (another job; not mine) and no longer
  lists the R28 brief (committed by someone else meanwhile).
  Wrote `ff_grid.py` (my own grid generator through P2's builder, per force group, with geometry and
  fresh-OpenMM checks).
  PREDICTION (ff_grid.py L H 144): G1 dihedral deviation < 1e-8 deg-ish (rad 1e-8); G2 bond/angle constant;
  G3 agreement with a fresh ff14SB+GBn2 system to 1e-6 relative; G4 my grid equals their cache to 1e-9
  (same OpenMM calls underneath, different group masks → float differences ≤ 1e-9 relative);
  CA-CB-CG of the rigid leucine ≈ 109.5° (CT-CT-CT equilibrium; from memory) — i.e. NOT the ≈ 116° of
  deposited leucines (from memory), which would support "rigid ideal geometry strains the rotamers".
* 2026-11-27T00:07:33Z — `ff_grid_L_H_144_01.log` (reached its last line): G2, G3, G4 ok; **G1 FAILED — MY OWN ERROR**:
  my dihedral function had the sign of the sine reversed (it returned −θ), so the "deviation" was up to 179°.
  Fixed (hand-checked test case in the code); the failing log is kept.  The grid itself was unaffected
  (G4: my grid equals the re-run's cache to 3.6e-14 relative; GBn2 identical).  Re-running into `_02`
  (the .npz is rewritten with identical content).
* 2026-11-27T00:08:20Z — `ff_grid_L_H_144_02.log` (reached its last line; 37.5 s; 75 MB): G1 ok (3.7e-14 deg; χ1 = N-CA-CB-CG,
  χ2 = CA-CB-CG-CD1; CD2 sits at χ2 + 120.07°), G2 ok (bond, angle constant), G3 ok (builder = fresh
  ff14SB + GBn2 system to 1.5e-16; control OBC2 differs by up to 1.39 kcal/mol), G4 ok (my grid = cache of
  the re-run, 3.6e-14 relative; control: exchanged axes differ by 1.6e9).  Rigid leucine geometry:
  CA-CB-CG = CB-CG-CD = 109.50°, N-CA-CB = 109.70° — as predicted.
* 2026-11-27T00:10:42Z — wrote `ff_lib.py` (my reductions for two torsions, from the text) and `ff_reduce.py`
  (replication + parsed comparison with a log + controls C1 separable, C2 shuffled, C3).
  PREDICTION (ff_reduce.py on my L H grid against the re-run log): all compared items agree at print
  precision (0 disagreements); my higher-precision rigid offset per torsion is −0.5795 ± 0.00005 — if it
  is −0.57949…, the table's "−0.580" is a double rounding (4 decimals, then 3); C1 gives exactly zero
  coupling error; C2 (shuffled) breaks nearly every item; exhaustive search over modes at k = 3 does not
  beat the threshold rule by more than a few per cent for valine.
* 2026-11-27T00:11:25Z — REPLICATION of the reductions (my code, my grids):
  `ff_reduce_L_H_01.log` (reached last line): 165 items compared with the re-run log, 0 disagreements;
  216 brackets, 0 violated.  Leucine numbers with more digits: rigid offset per torsion −0.579521 (so
  "−0.580" is correctly rounded — my double-rounding suspicion was wrong), minimised +1.768946; TV 0.480835
  and 0.044383; rigid minimum state cell (1,0) = (180°, 60°), gap 1.55892 kT; continuous minimum
  (287.5°, 157.5°) in cell (2,1); strains 5.9079 (cell (2,1)) and 3.7869 (cell (1,0)); cell minimum of
  (1,0) is 0.56214 kT above the global minimum.  C1 (separable): zero coupling error (remainder 1e-13,
  gaps 0, populations factorise to 1e-16; the real energy: 0.187 off factorisation).  C2 (shuffled):
  135 of 165 items disagree.  C3: Jensen-as-upper violated 18/18, minima-as-lower 18/18; oscillation × 0.3
  excludes in 0/18 for leucine (its all-H end is 4e19 — this control cannot bite on L; it bites on VV).
  `ff_grid_VV_H_144_01.log` (reached last line): G1–G4 ok.
  `ff_reduce_VV_H_01.log` (reached last line): 164 items, 0 disagreements; 216 brackets, 0 violated.
  Valine, tilted reference, per torsion: Jensen gap 7.1788e-07 at k = 3; upper end above the grid 1.8418e-02
  at k = 3 and 1.6602e-05 at k = 12 — table values confirmed.  Exhaustive search over all 64 mode
  assignments at k = 3: 1.8418e-02 (the threshold rule is optimal there); local search at k = 12:
  1.4731e-05 (11 % better than the threshold rule).  C3: oscillation × 0.3 excludes the grid value in
  13/18.  C2: 155 of 164 disagree.  All predictions met except the double-rounding guess (not the case).
* 2026-11-27T00:13:12Z — wrote `ff_leucine.py` (attack on the leucine claim).  Cell minima on the 2.5° grid (helix):
  (2,1) at (287.5, 157.5) 0 kT; (1,0) at (190, 80) 0.562; (1,1) at (187.5, 135) 2.403; (2,0) at (290, 107.5) 2.927.
  PREDICTION (ff_leucine.py, helix): V0 — vacuum part alone KEEPS the claim, GBn2 alone does not show it;
  V1 — the claim (different cells) is kept for boundary shifts from −57.5° up to about +45° and is lost
  only when the cell of the rotamer 180° is stretched to contain χ1 = 287.5° (shift ≥ +47.5°);
  V2 — in the basin formulation the claim is KEPT (rigid minimum state in the basin of the (190, 80)
  minimum, not the global one); basin populations about 0.61 / 0.39;
  V3a — offsets towards the mt minimum (negative d1, d2) remove the claim, offsets towards tp keep it;
  about half of the map wrong; V3b, V3c remove it; V3d (from-memory library values): undecided,
  my guess is that it is kept with a smaller gap.
* 2026-11-27T00:14:09Z — `ff_leucine_L_H_01.log` (reached last line).  ATTACK ON THE LEUCINE CLAIM, helix, 2.5° grid:
  V0 total: claim reproduced (rigid min (180,60), gap 1.5589; continuous min (287.5,157.5)).
     **Vacuum ff14SB alone: the claim GOES AWAY** — the continuous minimum is then at (190, 80) in the cell of
     the rigid minimum; the two cell minima differ by 0.055 kT in vacuum (order reversed) against 0.562 kT with
     GBn2.  The population error stays (TV 0.467).  (Prediction V0 MISSED: I predicted vacuum keeps it.)
     Strain decomposition at the ideal rotamers relative to the continuous minimum [kT]: LJ +7.74 / +6.02,
     torsion −2.18 / −0.10, Coulomb +0.27 / −2.57, GBn2 +0.08 / +1.00 for (300,180) / (180,60): steric.
  V1 shifted boundaries: kept at 42 of 47 shifts (−57.5 … +45); lost for shifts ≥ +47.5 (the cell of 180°
     then contains χ1 = 287.5).  Prediction met.
  V2 basins of steepest descent: KEPT — rigid min state in the basin of (190, 80) (0.562 kT, population
     0.3392), global-minimum basin population 0.5514; TV between basin populations and rigid weights 0.487.
  V3a uniform offsets of the rotamer positions: **knife-edge** — wrong cell at 350 of 625 offsets in
     [−30,30]²; at d1 = 0 the table is wrong for d2 ≥ 0 and RIGHT for every d2 ≤ −2.5: a shift of the χ2
     positions by −2.5° removes the claim.  Within ±5°: wrong at 15 of 25.  TV: 0.48 at (0,0), smallest
     0.106 at (−17.5, −2.5).
  V3b slice-bottom library: min state right (by construction), TV 0.40.  V3c marginal-minimum library
     (χ1 47.5/190/287.5, χ2 80/157.5/290): right, gap 0.562, TV 0.106.
  V3d from-memory library positions: E(295,175) = 4.730, E(182.5,65) = 3.005, E(185,65) = 3.677 kT:
     claim KEPT (table prefers tp by 1.05–1.7 kT) — library values from memory, unverified.
  `ff_grid_L_E_144_01.log`, `ff_grid_L_H_win_{mt,tp,rot}_01.log`: all reached their last lines, G1–G3 ok.
* 2026-11-27T00:14:57Z — `ff_leucine_L_E_01.log` (strand; reached last line): my grid reproduces the committed strand log's
  TV 0.2746 / 0.0442, gap 32.950, continuous min (195, 82.5), same cell True.  On the strand the ideal (300,180)
  rotamer is 37.3 kT up (LJ +40.5): rigid table 1.0000 / 0.0000 against continuous 0.7254 / 0.1520.  Offsets map
  on the strand: right at (0,0), WRONG for d2 ≤ −7.5 at d1 = 0 (273 of 625 offsets wrong) — the mirror image of
  the helix: on both backbones the identity of the table's minimum state flips within a few degrees of the
  χ2 library positions.  Vacuum alone on the strand: same as total (no flip).
  PREDICTION (ff_window.py, 1° windows): minima within 1.25° of the 2.5° ones, lower by < 0.05 kT; strains
  5.9 and 3.8 change by < 0.05 kT; the sign change of E(180+d1,60+d2) − E(300+d1,180+d2) at d1 = 0 lies
  between d2 = −1 and d2 = −2.5.
* 2026-11-27T00:16:52Z — `ff_window_01.log` (reached last line).  1° windows (helix): mt minimum (287, 157), tp minimum
  (191, 81); E(tp) − E(mt) = +0.549 kT (2.5° grid: +0.562); vacuum alone −0.059 (order reversed); strains of
  the ideal rotamers 5.910 and 3.802 kT (text: 5.9, 3.8 — confirmed); slopes at the ideal rotamers
  0.29–0.51 kT per degree; thermal widths of the two wells 6–10° (std).
  **Knife edge at 1°:** E(180+d1, 60+d2) − E(300+d1, 180+d2) at d1 = 0: −1.56 (d2 = 0), −0.61 (d2 = −1),
  +0.35 (d2 = −2): the table's order of its two lowest states reverses when the χ2 positions move by
  about −1.6°; negative (the "wrong" order) at 75 of 121 offsets with |d1|, |d2| ≤ 5°.  Prediction met.
  Wrote `ff_flex.py`: the same energy with bond lengths and angles relaxed at prescribed χ (nothing in
  the logs under review measures the direction claimed in item 101 (c)).
  PREDICTION (ff_flex.py, helix): relaxation lowers the strain of both ideal rotamers substantially
  (from 5.9 / 3.8 kT to below 3 / 2 kT), the relaxed CA-CB-CG opens beyond 112°, and the relaxed minima
  move towards the ideal values — i.e. the DIRECTION "rigid geometry exaggerates the strain" will be
  confirmed; whether the relaxed two-state table still prefers (180,60): undecided (my guess: the
  preference shrinks below 1 kT or reverses).
* 2026-11-27T00:17:56Z — `ff_flex_H_01.log` (reached last line; 2.6 s).  **Bond geometry relaxed, same energy function,
  helix** (controls R1–R4 ok: restraint fidelity 0.04°, relaxation never raises the energy, frozen = builder
  energy to 0e+00, perturbed restart within 1e-3 kT):
  variant A (backbone frozen; HA, CB, side chain relax): relaxed well minima at (298.6, 177.4) and
  (178.3, 62.8) — within 3° of the IDEAL rotamers; strain of the ideal rotamers above the relaxed minima
  0.028 and 0.058 kT (rigid: 5.9 and 3.8); CA-CB-CG opens from 109.5° to 115.0–115.5°;
  relaxed two-state table E(300,180) − E(180,60) = +0.262 kT (rigid +1.559); relaxed well bottoms
  E(tp) − E(mt) = −0.292 kT (rigid +0.562): the relaxed table and the relaxed minimum AGREE (both tp).
  variant B (all atoms relax, φ ψ ω restrained): 0.021 / 0.052 kT; +0.231; −0.262; agree.
  => (i) the direction claimed in item 101 (c) is CONFIRMED by a measurement (mine; none in their logs),
  and the effect is not "exaggerated" but essentially CREATED by the rigid 109.5° geometry: the strain
  falls by two orders of magnitude; (ii) with relaxed geometry the leucine claim (table names another
  well than the minimum) GOES AWAY; (iii) the lower well of the relaxed model is tp, the one the rigid
  table named and the rigid continuous model did not.  Caveat: adiabatic (no vibrational free energy
  of the relaxed coordinates); one residue; one force field.  Prediction: direction met; the size of the
  drop (to 0.03–0.06 kT) far beyond what I predicted (< 3 / 2 kT).
* 2026-11-27T00:19:00Z — started `ff_flex.py H --map 5` (background; adiabatic relaxed map).  Wrote `ff_relaxgeom.py`:
  a RIGID-rotamer model built by rigid rotation of a geometry relaxed once (CA-CB-CG ≈ 115°) — the situation
  of a table built from deposited or minimised bond geometry.
  PREDICTION (ff_relaxgeom.py, helix): control g0 reproduces the original numbers (TV 0.4808, gap 1.559);
  with either relaxed geometry the strain of the two ideal rotamers above their cell minima falls below
  1 kT, TV(grid cells, rigid) falls below 0.15, the rigid table's minimum state is in the cell of the
  continuous minimum (claim removed), and the rigid ln Z offset per torsion becomes positive (≈ +1.5 … +1.8).
* 2026-11-27T00:22:17Z — `ff_relaxgeom_H_01.log` (reached last line; 114 s).  Rigid-rotamer model on a geometry relaxed once
  and then rotated rigidly (controls: Z-matrix extraction reproduces the builder to 3.6e-15 Å and the original
  grid to 5e-14; g0 reproduces TV 0.4808, gap 1.559, −0.5795):
  g_mt (relaxed in the mt well; CA-CB-CG 115.32°): rigid table min (300,180), gap 1.371; continuous min
     (297.5, 177.5), SAME cell; TV(rigid) 0.0684; strains 0.028 / 0.462 kT; populations grid 0.7292 / 0.2273,
     rigid 0.7976 / 0.2024; rigid ln Z offset +1.5394 per torsion.
  g_tp (relaxed in the tp well; 114.83°): rigid table min (180,60), gap 2.196; continuous min (177.5, 62.5),
     SAME cell; TV(rigid) 0.1628; strains 0.691 / 0.076; populations grid 0.1919 / 0.7371, rigid 0.1001 / 0.8999;
     offset +1.5910.
  => with realistic bond geometry the leucine claim is REMOVED (table and continuous minimum agree, TV 0.07–0.16
  instead of 0.48, ideal-rotamer strain ≤ 0.7 kT instead of 3.8–5.9).  Prediction met.
  NEW observation (not predicted): the geometry REMEMBERS its source well — the well in which the geometry was
  relaxed becomes the minimum and takes 0.73–0.74 of the weight (cell minima: the other well 0.94 kT up with
  g_mt, 1.58 kT up with g_tp; fully relaxed (adiabatic): tp lower by 0.29 kT).  A rigidly rotated deposited
  geometry is biased towards the deposited rotamer by about 1–1.5 kT here.
* 2026-11-27T00:24:22Z — Item 4.  Re-derived before opening their script: for a competitor x, min over the box of
  E'(x) − E'(x*) = E(x) − E(x*) − Σ_{entries used by exactly one of x, x*} b = Ẽ(x) − Ẽ(x*); hence (N) and (U).
  Uniform b, complete graph: a competitor differing at d of n sites uses D(d) = d(2n+1−d)/2 entries that x* does
  not (d = 1: n; increasing in d), so necessary optimality ⟺ E(x) − E(x*) ≥ 2bD(d(x)) for all x; "only if
  b ≤ gap/(2n)" is a correct NECESSARY condition whatever the second-best configuration looks like (D(d) ≥ n),
  not sufficient; it presupposes DENSE tables (every pair an entry with allowance b): in general the count is
  2(1 + degree of the flipped site).  Five numbers by hand: 0.0451/52 = 8.673e-4; 0.0243/72 = 3.375e-4;
  0.1102/72 = 1.531e-3; 0.0068/92 = 7.39e-5; 0.0039/98 = 3.98e-5 — all five as claimed.
  Per-site/well: "compare against x* alone" is sufficient, NOT necessary; exact condition = no configuration
  with x_i outside W is POSSIBLY optimal, and x is possibly optimal iff it minimises the table with its own
  entries lowered and all others raised (a vertex scenario, so vertex enumeration is exact for it too).
  Smallest example: 2 sites × 2 states, E(a,p) = 0, E(a,q) = 0.1, E(c,p) = E(c,q) = 5, b = 1 on all 8 entries:
  site 1 keeps state a in every scenario ((a,p) beats (c,p) by ≥ 1, (a,q) beats (c,q) by ≥ 0.9) while
  Ẽ(c,q) − Ẽ(a,p) = 5 − 6 < 0, and x* = (a,p) itself is not necessarily optimal.
  Then read `necessary_optimality_check.py` and its log (full).  Wrote `no_check.py` (my own; several shapes
  including sparse graphs; possibly-optimal; per-site; radius).
  PREDICTION (no_check.py): (N), (U) agree with enumeration in every model; every mutilated criterion disagrees
  somewhere; possibly-optimal criterion agrees for every configuration; per-site: "sufficient but false" 0,
  "true without sufficient" > 0, explicit example as computed by hand; S5: b* ≤ gap/(2n) always on complete
  graphs, attained in most models, strict in some; path graphs: b* exceeds gap/(2n) in most models;
  S6: 0 disagreements of 5.
* 2026-11-27T00:25:04Z — `ff_flex_H_map_01.log` (reached last line; 279 s).  Adiabatic relaxed map, 5° step, 905 points (those
  with rigid energy below 25 kT): relaxed continuous two-state split mt : tp = 0.493 : 0.507 (variant A),
  0.500 : 0.500 (variant B); relaxed ideal-rotamer two-state table 0.435 : 0.565 and 0.442 : 0.558 — an error of
  0.06 in population, against 0.617 : 0.383 (rigid continuous, same points) versus 0.174 : 0.826 (rigid table),
  an error of 0.44.  (Mask chosen from the rigid energies: a limitation of this map.)
* 2026-11-27T00:26:06Z — `no_check_01.log` (reached last line; 48.6 s; 691 MB).  REPLICATION of SCI-REV-0026 §4 with my code:
  S1 580 tiny models of 5 shapes (complete and path graphs), 91 258 880 vertex scenarios enumerated: (N) agrees
  580/580 (necessarily optimal in 179), (U) 580/580 (151); mutilated criteria disagree in 177 / 159 / 401 / 181.
  S2 possibly optimal: criterion agrees for 5430/5430 configurations.
  S3 per site and well, 2720 cases: "sufficient but false" 0; TRUE WITHOUT the sufficient condition: 49;
  the explicit 2×2 example behaves as computed by hand (site keeps its state in all 256 vertex scenarios,
  sufficient condition fails, x* not necessarily optimal).
  S4 400 larger models: where (N) holds, x* a minimiser in all 14 940 sampled scenarios; where it fails, Ẽ has
  a strictly better configuration in 151/151.
  S5 uniform b, complete graphs, 392 models: b* ≤ gap/(2n) in 392; equality in 194, strict in 198 (the binding
  competitor differs at several sites in 200); radius confirmed just below/above 784/784; D(d) = d(2n+1−d)/2
  checked n = 2..6.  Path graphs: b* EXCEEDS gap/(2n) in 245 of 293 — the count 2n is for dense tables.
  S6 five numbers: 0 disagreements (8.6731e-4, 3.3750e-4, 1.5306e-3, 7.3913e-5, 3.9796e-5).
  All predictions met.
  `ff_flex_E_01.log` (strand; reached last line): variant A strains 1.845 / 0.141 kT (rigid 35.75 / 4.39), relaxed
  table +1.902 (rigid +32.95), well bottoms −0.198 (rigid −1.588), table and minimum agree; variant B strains
  0.928 / 0.134, table +0.693, well bottoms +0.101 — table and minimum DISAGREE (a 0.1 kT near-degeneracy):
  with relaxed geometry the "other well" phenomenon survives only at the 0.1–0.7 kT level.
* 2026-11-27T00:28:30Z — RE-RUN of `necessary_optimality_check.py` (their script; `rerun_necessary_optimality_01.log`, reached last
  line): identical to the committed log except the start time and the run time.
  Wrote `check_tables.py` (my own parser of the 12 committed logs; compares every cell of the two tables of the
  addendum and of the table of SCI-REV-0025 §3 with what the logs give; recomputes the numbers quoted in the texts).
  PREDICTION: 0 differing cells in the three tables (they are generated by a script); text numbers: all consistent
  except the two already suspected — "one to three nats per torsion" (leucine is 0.58–0.62) and "about 2 nats
  per torsion" for the minimised offset (serine is 1.2).
* 2026-11-27T00:30:15Z — `check_tables_01.log` (reached last line).  READ-ONLY check against the 12 committed logs (2 of them
  identical to my re-runs): 252 table cells (addendum tables 1 and 2, SCI-REV-0025 §3 table): 0 differ.
  Text numbers recomputed from the logs — all agree; remarks: (t1) "one to three nats per torsion" (100 (i)):
  the range of |offset| is 0.580 … 3.177 (leucine 0.58–0.62 is below one); (t2) "a vibrational term of about
  2 nats per torsion" (SCI-REV-0025 point 3): minimised offsets are +1.18 … +2.28 (serine 1.18–1.21,
  leucine 1.76–1.77, valine 1.89–2.28); (t3) "kinder by a factor of about twenty": 15.5–43.8 for valine at 2.5°
  (4.6 for serine, 127 for leucine); (t4) the entry "+1.992" of VVV helix is the 3-decimal rounding of a logged
  "1.9925" — its last digit rests on digits not in the log (not re-run: 477 s); L helix "−0.580" is correct
  (my value −0.579521); (t5) item 100 (vi) cites the research log at "22:36", the entry is headed "22:35".
  Research log lines 2924–2950 and 3024–3085 read (cited by items 98 and 100 (vi)): predictions (1)–(6) are
  about valine blocks, so "met" for prediction (3) stands (valine minima 8.12, 2.67, 0.0679); for serine the
  72-cell bracket is 0.02.

## Search log (Item 5) — every query, tool and address

* 2026-11-27T00:31:14Z — PubMed tool `lookup_article_by_citation` with the six citations of item 102 (a)–(e) (journal, year, volume,
  first page, first author) → PMIDs 18293294, 22279426, 11580256, 18707538, 17154716, 19481551.
  PubMed tool `get_article_metadata` for these six PMIDs → records with abstracts.  Reading level: ABSTRACT (PubMed record).
  Outcome (item 102): (a) Georgiev, Lilien, Donald, J Comput Chem 29(10):1527-42 (2008), doi:10.1002/jcc.20909 — the quotation
  is verbatim in the abstract.  (b) Gainza, Roberts, Donald, PLoS Comput Biol 8(1):e1002335 (2012),
  doi:10.1371/journal.pcbi.1002335 — "69 protein-core redesigns", the "nearly all" sentence and "guarantees finding the optimal
  answer" verbatim; "using more rigid rotamers was never better than a continuous-rotamer model" is verbatim but the abstract's
  qualifier "at computationally feasible resolutions" is dropped.  (c) Petrella, Karplus, J Mol Biol 312(5):1161-75 (2001),
  doi:10.1006/jmbi.2001.4965 — "are largest for leucine residues" verbatim ("approximately 6 % versus 16.6 %"); the abstract
  also says on-rotamer conformations are the absolute minima of rigid-geometry CHARMM maps in 97.6 %, "generally to within
  10 degrees or less" — relevant to my finding F-L.  (d) Yanover, Schueler-Furman, Weiss, J Comput Biol 15(7):899-911 (2008),
  doi:10.1089/cmb.2007.0158 — both quotations verbatim (incl. "0:1%"), 82.6 % verbatim; also 77 % → 78 % with the softer
  repulsion and "approximately 85% of the proteins" (used in SCI-REV-0026 §3, F5): all in the abstract.
  (e) Zhang, Liu, PLoS Comput Biol 2(12):e168 (2006), doi:10.1371/journal.pcbi.0020168 and DuBay, Geissler, J Mol Biol
  391(2):484-97 (2009), doi:10.1016/j.jmb.2009.05.068 — both Monte Carlo side-chain entropies; DuBay–Geissler: backbone
  fixed, "torsional entropy" of 12 small proteins; Zhang–Liu: 675 proteins.  All bibliographic details as in item 102.
  Item 102 (f): SCI-REV-0026.md contains no occurrence of "voxel", "THY-MSG-0020", "VoxelEnclosure" or "VoxelBridge"
  (grep) — from that file alone the fairness of (f) cannot be judged.
* 2026-11-27T00:36:16Z — PubMed `search_articles`: "continuous rotamers partition function provable" (0 hits); "continuous entropy
  voxel protein design side-chain" (0); "rotamer free energy integral torsion side-chain entropy vibrational" (0);
  "continuous rotamers partition function" (2: PMID 27914058, 25846627); "continuous entropy protein design voxel" (0);
  "side-chain conformational entropy rotamer vibrational free energy" (1: PMID 8563620); "LUTE Local Unpruned Tuple
  Expansion" (1: 27681371); "Hallen MA[Author] AND (entropy OR "partition function" OR "free energy")" (4: 30368845,
  23077560, 30378699, 22821798); "minimization-aware recursive K* partition function" (1: 31855059); "BBK* branch and bound
  over K* partition function bounds" (1: 31855059); "self-consistent mean field side-chain conformational entropy rotamers"
  (3: 12441384, 8196057, 18841329).  `get_article_metadata` for 27914058, 25846627, 8563620, 27681371, 30368845, 30378699,
  31855059, 8196057, 18841329 (abstracts read).
  Web search (standard mode), query 1: continuous rotamers voxel "free energy" integral over voxel partition function provable
  bounds protein side chains "continuous entropy".  Query 2: Hallen "PLUG" "Pruning of Local Unrealistic Geometries"
  "continuous entropy" LUTE voxel free energy bioRxiv.  Query 3: "necessarily optimal" solution interval costs combinatorial
  optimization criterion scenario "upper bounds" own elements "lower bounds" others Kasperski Zieliński.
  FOUND (prior art for item 101 (b), first ingredient):
  * Hallen, Jou, Donald, LUTE, J Comput Biol 24(6):536-546 (2017), doi:10.1089/cmb.2016.0136 [record + abstract: PubMed];
    submitted manuscript dated 12 Aug 2016 (address 3) [PASSAGE read by me]: eq. (3)–(5): q = Σ_r ∫_{V(r)} exp(−E'(x)/RT) dx;
    "discrete free energy function" E(r) = −RT ln ∫_{V(r)} exp(−E'(x)/RT) dx; q = Σ_r exp(−E(r)/RT); "Alternately, if we use
    the definition Eq. (2) [the minimum over the voxel] ... gives us the approximation used in [Lilien et al., 2005] and
    [Georgiev et al., 2008] for the partition function."  => the cell-wise identity with a voxel free energy as the discrete
    energy IS IN PRINT; and the "from memory" remark of item 97 (K* uses the minimised energy of a voxel) is confirmed.
  * Hallen, PLUG, Proteins 87(1):62-73 (2019), doi:10.1002/prot.25623 [abstract: PubMed]: "When combined with the LUTE
    protein design algorithm, PLUG greatly facilitates designs that account for continuous entropy"; bioRxiv full text
    (address 4) [fetch-tool summary, not read by me verbatim]: voxel energy defined as a free energy, "computed by
    integrating the Boltzmann distribution" over a voxel by Monte Carlo integration, represented by a pairwise matrix
    LEARNED by LUTE; residuals reported; no provable bound.
  * Jou, Holt, Lowegard, Donald, MARK*, J Comput Biol 27(4):550-564 (2020), doi:10.1089/cmb.2019.0315 [abstract]: the
    K* partition function is approximated with "provable, admissible pairwise-minimized energy lower bounds".
  * Roberts, Donald, Proteins 83(6):1151-64 (2015), doi:10.1002/prot.24808 [abstract]: partitioned continuous rotamers
    (PartCR) to tighten energy bounds over voxels — for the minimum, not for a free energy.
  * Jumper, Freed, Sosnick, arXiv:1610.07277 (address 1) [fetch-tool summary]: side-chain free energy defined as
    −log ∫dχ e^{−V}; coarse states merging fine rotamers; variational/belief-propagation approximation; no bound.
  * Koehl, Delarue, J Mol Biol 239(2):249-75 (1994), doi:10.1006/jmbi.1994.1366 [abstract]: self-consistent mean field
    over rotamers with an estimate of the side-chain conformational entropy (discrete states).
  * Doig, Sternberg, Protein Sci 4(11):2247-51 (1995), doi:10.1002/pro.5560041101 [abstract]: "Changes in vibrational
    entropy appear to be negligible compared to the entropy change resulting from the loss of accessible rotamers" —
    prior statement on the "vibrational term" of item 100 (i).
  NOT FOUND in these: cell AVERAGES of the coupling as pair tables with a Jensen lower end and a bounded-difference upper
  end (a certified two-sided bracket of the continuous integral).  "Not found" in 3 web queries and 11 PubMed queries is
  not "new".
  FOUND (Item 4, "classical"): Kasperski, Zieliński, "Robust discrete optimization under discrete and interval uncertainty
  - a survey" (author's PDF, address 6; book details not verified) [PASSAGES read by me]: "the maximum regret of X equals
  f(X, S_X) − f*(S_X), where S_X is the extreme scenario under which the costs of e_i ∈ X equal c_i + d_i and the costs of
  e_i ∉ X are equal to c_i" (attributed there to their refs [41, 52]); "X is called necessarily optimal if it is optimal
  under all scenarios"; "the maximum regret of a necessarily optimal solution equals 0"; and: the optimum of the MIDPOINT
  scenario has at most twice the optimal maximum regret, which "allows us to detect efficiently a solution with the
  maximum regret equal to 0 (i.e. a necessarily optimal solution)".  Together: X necessarily optimal ⟺ X optimal under S_X —
  criterion (N) of SCI-REV-0026 §4; and if any necessarily optimal configuration exists, the minimiser of the nominal table
  is one.  Fortin, Kasperski, Zieliński, "Some methods for evaluating the optimality of elements in matroids with ill-known
  weights" (author's PDF, address 5; journal not verified) [PASSAGES read by me]: possibly / necessarily optimal ELEMENTS,
  Theorems 5 and 6 (extreme configurations, matroids); cites Yaman, Pinar, Karasan, Oper. Res. Lett. 29:31–40 (2001)
  (weak / strong edges) [reference list only; not opened].
* 2026-11-27T00:37:50Z — Web search query 4: rigorous upper and lower bounds configuration integral partition function discretization
  cells Jensen inequality lower bound "bounded differences" OR "Hoeffding" upper bound free energy  → general
  Jensen/Bogoliubov material; A. Maurer, "Thermodynamics and concentration" (arXiv:1205.1595) named in the result summary
  [search snippet only; not opened].  Query 5: verified integration rigorous enclosure multidimensional integral Boltzmann
  factor partition function interval arithmetic guaranteed error bound molecular → nothing matching (verified 1-D
  integration; a Lean package for Lennard-Jones energies) [snippets only].  Query 6: Jacobian bond-angle-torsion internal
  coordinates configuration integral "b^2 sin" product over atoms Jacobian determinant factorizes Cartesian to BAT
  coordinates → r² and sin θ factors in the volume element; Chang, Potter, Gilson, J. Phys. Chem. B 107:1048 (2003)
  named [snippets only; not opened].
  PubMed: "computational protein design side-chain conformational entropy belief propagation free energy rotamers"
  (1: 18618711); "penultimate rotamer library" (5: 10861930, …); metadata for 18618711, 10861930 [abstracts]:
  * Sciretti, Bruscolini, Pelizzola, Pretti, Jaramillo, Proteins 74(1):176-91 (2009), doi:10.1002/prot.22145: free energy
    from the partition function over rotamer states, "written in variational form in a pairwise approximation and
    minimized using the Belief Propagation algorithm" (uncertified; discrete states; a design study, cited only for the
    variational free energy).
  * Lovell, Word, Richardson, Richardson, "The penultimate rotamer library", Proteins 40(3):389-408 (2000) [abstract]:
    "All published rotamer libraries contain some rotamers that exhibit impossible internal atomic overlaps if built in
    ideal geometry with all hydrogen atoms"; remaining overlaps "can be understood in terms of bond angle distortions
    compensated by favorable interactions" — PRIOR ART for the strain of rotamers in ideal bond geometry and for its
    relief by bond angles (my measurement F-L).  The leucine library values I used in V3d ((−65, 175), (−177, 65)) and
    "CA-CB-CG ≈ 116° in deposited leucines" remain FROM MEMORY — not in this abstract.
  Search closed here (bounded): 6 web queries, 14 PubMed queries, 6 addresses opened.  Not reached: the full texts of
  the K* / BBK* / MARK* papers, of PLUG (journal version), of Gainza 2012 and Georgiev 2008; the statistical-mechanics
  literature on cell theories and variational coarse-graining (not searched beyond query 4); numerical analysis beyond
  query 5; nothing in MathSciNet/zbMATH; no citation-graph search.
  Wrote `bat_jacobian.py`.  PREDICTION: |det J| / (Π b² Π sin θ) constant to 1e-6 relative; the two controls vary by
  more than 10 %.
* 2026-11-27T00:38:58Z — `bat_jacobian_01.log` (reached last line): |det J| / (Π b² Π sin θ) constant to 2.1e-09 relative over 200
  random geometries of a 6-atom chain (controls vary by 144 % and 308 %): the Cartesian volume element IS a product
  measure in bond-angle-torsion coordinates.  Prediction met.  So "with [bond lengths, bond angles] free the sites are
  no longer independent under any natural reference" (item 99 (ii)) is wrong as a reason; what a free backbone
  destroys is the locality of the terms.
  Wrote `toy_extras.py`.  PREDICTION: X1 half-open cells give SMALLER grid widths than closed cells by factors about
  (1 − 1/m) and (1 − 1/m)² (m = grid intervals per cell): 0.8 and 0.64 at k = 288, about 1 at k = 3; 0 violations
  for both; X2 the tight constant never exceeds the stated one and gives an all-H width of 0.5–0.8 of the stated
  one for k ≥ 12; X3 with the bump height W = 20 → 2000 the Jensen gap per angle at k = 3 grows roughly in
  proportion to W while the upper end saturates.
* 2026-11-27T00:40:01Z — `toy_extras_01.log` (reached last line).  X1: half-open/closed width ratios 0.9992 | 0.9970 (k = 3) …
  0.8000 | 0.6369 (k = 288) — as predicted; 0 violations of 16: both forms are legitimate; the half-open grid partition
  UNDERSTATES oscillations (it misses one grid interval per cell), the closed trapezoid form does not.
  X2: tight constant never above the stated one (0 of 94 770 entries); all-H width with the tight constant is 0.911,
  0.792, 0.669, 0.626 of the stated one at k = 3, 6, 12, 24 (position of the exact value rises from 0.145 to 0.231 at
  k = 24).  **MY CONTROL DID NOT BITE**: "tight × 0.5 must exclude the exact value somewhere" — it excluded nowhere
  (the exact value sits at ≤ 0.231 of the tight bracket, × 0.5 leaves 0.25 of it).  A control that cannot fail at the
  factor chosen is my error; re-running with × 0.3 added (`_02`).
  X3: Jensen gap per angle at k = 3: 0.359, 0.518, 1.11, 7.71 for W = 0, 20, 200, 2000; at k = 12: 0.024, 0.033, 0.044,
  0.092; the best upper end at k = 3: 0.928, 1.08, 1.35, 2.30.  With a wall the LOWER end degrades in proportion to
  the wall's height times its share of the cell, and mode M does nothing for it.  Prediction met.
* 2026-11-27T00:41:33Z — `toy_extras_02.log` (reached last line): same numbers; the added control "tight × 0.3" excludes the exact
  value at k = 3, 12, 24 (not at 6); "tight × 0.5" nowhere.  Consequence for the text under review: the assertion
  "every bracket contains the grid value" would also pass with oscillations too small by a factor of two (× 0.5:
  0 of 41 partitions excluded in stage B) — it does not validate the H-mode constants; the agreement of two
  independent implementations to 5e-7 (stage B) does.
  Starting `ff_relaxgeom.py E` (strand) in the background.
* 2026-11-27T00:43:07Z — Review point (new): the upper end (c) is NOT a model on the interaction sets of V — exp(c_i(s)²/8) couples all
  sites of all terms containing i (3 sites on a chain; a whole neighbourhood in a dense pair model).  Cauchy–Schwarz
  with weights w_T (sum 1): (Σ_T o_T)² ≤ Σ_T o_T²/w_T keeps it a pair model at a price ≤ the number of terms at the site.
  Wrote `toy_pairwise.py`.  PREDICTION: relaxed all-H width / stated all-H width between 1.0 and 2.0 (about 1.2–1.5);
  never below the stated end; control (weights summing to 2) falls below the stated end at every k.
* 2026-11-27T00:43:41Z — `toy_pairwise_01.log` (reached last line): the pair-model relaxation of the all-H upper end costs a factor
  1.000 (k = 3) … 1.138 (k = 288) in width on the toy chain; never below the stated end; exact value inside (0 violations);
  the control (weights summing to 2) is below the stated end at all eight k (it did not exclude the exact value — the
  slack again).  Prediction met (the price is smaller than I guessed).
  `ff_relaxgeom_E_01.log` (strand; reached last line; 82 s):
  g_mt (relaxed in the mt well, χ = (291.5, 171.7), CA-CB-CG 116.27°): rigid table min (180,60), gap 4.659; continuous
     minimum (292.5, 172.5) in cell (2,1): DIFFERENT cells; TV(rigid) 0.7250; grid 0.7006 / 0.2657, rigid 0.0094 / 0.9906;
     strain of the ideal rotamers 6.239 / 0.461 kT.
  g_tp (relaxed in the tp well, 115.43°): min (180,60), gap 15.098; continuous minimum (180, 65): same cell; TV 0.1167;
     grid 0.0916 / 0.8833, rigid 0.0000 / 1.0000; strains 13.175 / 0.193.
  => **with realistic bond geometry the "other well" effect DISAPPEARS on the helix and APPEARS on the strand** (when the
  geometry comes from the mt well: TV 0.73, larger than the published 0.48).  The phenomenon is real as a family; which
  backbone / geometry / solvent term / rotamer position shows it is not stable.  The memory effect is there too: the
  well the geometry was relaxed in becomes the minimum (0.70 and 0.88 of the weight).
  Strain of the ideal rotamers, builder geometry → relaxed variants: helix (300,180): 5.91 → 0.03 (A), 0.02 (B), 0.03 /
  0.69 (rigid rotation of g_mt / g_tp); helix (180,60): 3.79 → 0.06, 0.05, 0.46 / 0.08; strand (300,180): 35.75 → 1.85,
  0.93, 6.24 / 13.18; strand (180,60): 4.39 → 0.14, 0.13, 0.46 / 0.19.  Reduced in all 16 comparisons: the DIRECTION
  of item 101 (c) is confirmed by measurement (mine).
* 2026-11-27T00:45:08Z — wrote `ff_flex_width.py` (the other half of item 101 (c): "rigid geometry makes the wells narrower").
  PREDICTION: the relaxed (adiabatic) wells of leucine on the helix are wider than the rigid ones: effective-area ratio
  relaxed/rigid between 1.3 and 3; the 5°-sub-grid control within 10 % of the 2.5° grid.
* 2026-11-27T00:46:53Z — `ff_flex_width_01.log` (reached last line): adiabatic relaxed wells of leucine on the helix against the rigid
  wells on the same points: effective area 765.8 vs 424.3 deg² (mt cell; ratio 1.80), 596.3 vs 430.8 (tp cell; 1.38)
  [variant B: 1.79, 1.36]; control: rigid 5° sub-grid / 2.5° grid = 1.075, 0.995.  So "rigid geometry makes the wells
  narrower" (item 101 (c)) is confirmed in direction by measurement (mine): by a factor 1.4–1.8 in area, i.e. 0.3–0.6
  nats per residue in the width term.  Prediction met.
  Wrote `no_midpoint.py` (the midpoint fact quoted from the survey).  PREDICTION: 0 violations of the implication and
  of the factor 2; the control fails in some models.
* 2026-11-27T00:54:00Z — `no_midpoint_01.log` (reached last line): 3 000 random pair models; a necessarily optimal configuration
  exists in 2 060; "exists but a nominal minimiser is not necessarily optimal": 0; max regret of a nominal minimiser above
  twice the smallest: 0; control (another candidate): fails in 751.  Prediction met.
  `toy_phi0_01.log` (reached last line): their instance with φ_i = 0 (as the text of item 98 reads): mixed width at
  3 cells 1.073 against 1.287 as run; at 6 cells 0.6429 against 0.6505; first-order and all-H rows within 2 %.
  Report written: `/home/user/MetricChain/docs/science/workstreams/R28_REPORT.md` (sections (0)–(7); 14 findings:
  F1–F5 major, F6–F14 minor, none critical).  Verdict table reduced to ten rows.  Numbers in the report re-read
  against the logs after writing; corrections made: CA-CB-CG range 114.8–115.6° (I had 115.0–115.5); the bias towards
  the source well 1.2–1.9 kT (I had "1 to 1.6"); grid-vs-cache agreement 7e-14 (I had 4e-14); OBC2 control 1.1–2.0
  kcal/mol; "per state" claimed only for the 360 brute-force cases; a truncated quotation of item 101 (c) completed.

## Final state

* Tool actions declined: none (no tool declined any action in this session).
* State-changing git commands run: none.  Files written: only inside `experiments/science/ws_R28/` and the report
  `docs/science/workstreams/R28_REPORT.md`; two PDFs fetched by the page tool were converted to text in the
  session scratchpad (outside the repository).
* `git status --short` at 00:54Z shows, as mine: untracked `experiments/science/ws_R28/` and
  `docs/science/workstreams/R28_REPORT.md`; NOT mine (other work going on in the same tree; I did not touch them):
  modified `docs/collaboration/SCIENCE_TO_ALL.md`, `docs/collaboration/status/science.md`,
  `docs/science/OPEN_PROBLEMS.md`; untracked `docs/collaboration/messages/science/SCI-MSG-0036.md`,
  `docs/science/SANDWICH_CERTIFICATE_FORMAT.md`, `experiments/science/sandwich_cert/`, `experiments/science/ws_R29/`.
* Subagents: none.  Longest run 279 s; largest peak memory 691 MB; at most two processes at a time.
* 2026-11-27T00:54:37Z — report re-read once more; two wordings corrected ("the example in our messages"; "no source read in full");
  header time restamped from the clock.  End of session work; hand-back follows.
