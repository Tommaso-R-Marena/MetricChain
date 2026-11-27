# Workstream R26 — NOTES (running log; adversarial review of theory §11.33 / workstream N)

Internal review by an AI agent; not external peer review.

Times are read from the clock (`date -u`) at the moment of writing each entry.

## 2026-11-26T21:50:59Z — start

- Read `docs/science/workstreams/COMMON.md` and `docs/science/workstreams/R26_brief.md` (in full).
- Created `experiments/science/ws_R26/`.
- Read-only copies at `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_4692f59/`:
  `N_REPORT.md` (1 124 lines), `THEORY_REPORT.md` (13 001 lines; I read only §11.33 and Theorem 11.56).
  NOT read (belong to other workstreams / forbidden): `R_REPORT.md`, `R_REVIEW.md`, `Z_REPORT.md`, `Z_REVIEW.md`,
  the subdirectory `read_only_after_your_own_report`.
- Machine: 4 cores, 15 GB; Python with numpy 2.5.3, scipy 1.18.1.  Rules: OMP_NUM_THREADS=1, <= 2 processes,
  <= 2 GB per process, <= 15 min per run, `python3 -B`, peak memory in the last line of every script.
- Order of work (priorities from the coordinator): Item 1 (N4 + influence of band models) > Item 2 (N12 false
  certificate, replication) > Item 3 (N1/N1') > Item 4 (Gauss space) if time remains.


## 2026-11-26T22:07:59Z — reading done

Read in full: N_REPORT.md lines 1-1124.  Read of THEORY_REPORT.md: lines 12105-12328 (section 11.33 with its
instance table and assumption paragraph) and lines 5590-5699 (Theorem 11.56 statement, proof sketch, remark on the
lowered cap).  Nothing else of the theory branch.  Quick grep of our own docs for the word "sandwich" (only to
confirm that "box class" = pointwise bounds E_lo <= E <= E_hi on the unknown energy; R24_brief.md lines 1, 59-77).

First observations (review level, before any code):

1. N4 proof is two lines and correct: V(a) = int e^{-psi(a,b)} mu(db|a) <= e^{d_o(a',a)} int e^{-psi(a',b)} mu(db|a)
   <= e^{d_o(a',a)+iota(a,a')} V(a').  Only w = e^{-psi(a',.)} (same psi, the comparison point a') is used, so the
   influence is needed only for that weight; nothing about iota is used beyond the inequality (no symmetry, no
   triangle inequality; iota = +infinity allowed on some pairs: then Xi_rho may be +infinity = no closing level).
   The exact class-relative influence sup_w ln(int w dmu_a / int w dmu_a') is automatically a quasi-metric
   (sup of sums <= sum of sups), so rho = d_o + iota obeys the triangle inequality when d_o does.
2. Lemma N.0 formula for Xi_rho has "D != X" in the sup; at q = 1 the formula gives a finite number on finite
   spaces while (TU) at q = 1 forces Xi(1) = +infinity (stated two lines above the lemma).  An implementation that
   evaluates the formula literally at q = 1 can close at level 0 with a false upper end.  Minor (to check in code).
3. For a band model of bandwidth r cut at c: mu(.|a) depends on a only through the last r outer sites, and
   dmu(.|a)/dmu(.|a') = exp(Delta)/<exp(Delta)>_{a'} with Delta = E_x(a',.) - E_x(a,.) a function of the first r
   inner sites only.  Hence iota_pt(a,a') = max Delta - ln <e^Delta>_{a'} in [0, osc Delta].  The exact value
   depends on the inner block through the law of the first r inner sites given a' (backward message) and, for a
   class, through the class projected on those sites.  So "governed by the boundary sites": TRUE for which outer
   sites matter and for the upper bound osc(Delta); FALSE for the exact value (to be shown by example).
4. Box class l <= w <= u: linear-fractional programme, optimum at a vertex w = u on a super-level set of the
   likelihood ratio, l elsewhere.  With u = e^D l: iota_box <= min(D, iota_pt), whatever the clash energy.
   And for a pure box class the fibre average V(a) lies in the computable box [int l dmu_a, int u dmu_a], so no
   influence is needed at all, and the exact tail function of the class is the cap function q(e^D - 1): nesting
   cannot beat plain sampling (to be written carefully).
5. N12 by hand: c(4,1) = ln(0.924649/0.443230) = 0.73533, k c = 11.765; V(|a|=9) = 1.204e-7, V(10) = 2.219e-6,
   V(11) = 0.2855, V(12) = 0.9753; A = 1.0746e-3; worst (TU) ratio 1.75e5 at s just above V(9) (D = {|a|>=10},
   Harper radius 2).  All consistent with the text.  Closure arithmetic by hand suggests that whether theta = 1
   gives a false certificate is close to a boundary (needs 0.264 * s_j/(e^b ell) <= 1): must be mapped by runs.
6. Hazard for us (Item 2 (iv)): a single boundary site with a RARE state and a rigid inner chain should give a
   false certificate on a nearest-neighbour chain; "the failure needs the influence to be spread" is then wrong
   at finite size / for non-uniform marginals.  To be tested.

Plan of files: r26_band.py (band models, influences), r26_alg.py (Algorithm A, own implementation),
r26_n12.py (Prop. N12 replication + controls), r26_hub.py (chain with rare boundary state),
r26_n1.py (N1/N1' stress), r26_gauss.py (Item 4 if time).

## 2026-11-26T22:21:46Z — first results

Files so far: r26_band.py (library + self-test), r26_influence.py (tables T1..T5), r26_alg.py (Algorithm A, tail
functions, checker), r26_n12.py (Proposition N12).  Logs that reached their last line: out_band_selftest_1..4.txt
(1-3 show failures of MY OWN check of the box formula, see below; 4 is the corrected one, 0 violations),
out_infl_T5_1.txt, out_alg_selftest_1.txt, out_n12_abc_1.txt, out_n12_assumed_1.txt.
out_infl_T1_1.txt did NOT reach its last line (I stopped it: the q = 4 part would have run into the time limit);
it is not cited; re-run in two parts below.

Own errors so far (to go in the report):
 E1. First check of the box-influence formula compared it with a Charnes-Cooper LP at D = 12: HiGHS' absolute
     feasibility tolerance inflates the LP optimum by up to 8e-4 when the variables are of size e^-12
     (out_band_selftest_1.txt, "violations 10").  The formula was right, the check was wrong.
 E2. Second and third check (a Dinkelbach residual with cancellation; an "optimality condition" that ignored
     configurations of mass < 1e-17) reported 143 and 171 false violations (out_band_selftest_2/3.txt).
     Final check: exhaustive over all 2^(q^r) vertex weights on the boundary layer + LP on the whole block for
     D <= 3: 984 + 48 cases, 0 violations (out_band_selftest_4.txt).

Results:
 R1. Self-test of the band library (out_band_selftest_4.txt): brute force = transfer matrices = boundary formula
     (24 random models incl. clashes, largest difference 5e-14); Lipschitz LP = closed form for Bernoulli(p)^k
     (4 cases, 2e-15); LP = recursion = closed form for the symmetric binary chain; the numbers of N_REPORT 4(f)
     reproduced: 1.525944 (p=0.3,u=1,k=6) and 1.128162 (p=0.2,u=0.5,k=6).   [replication]
 R2. T5 (out_infl_T5_1.txt): same cross-cut interaction (osc Delta = 6 kT), field on the first inner site varied:
     pointwise influence from 0.047 to 5.999; Lipschitz influence depends on the rigidity of the inner chain
     (0.89 -> 2.90 at u = 1, k = 6, p_in 0.5 -> 0.005).  So the influence is NOT a function of the cross-cut
     interaction alone; it is bounded by its oscillation.
 R3. N12 (a)-(c) (out_n12_abc_1.txt): c = 0.735326, k c = 11.7652, A = 1.074731e-3, spike share 99.9864 %,
     worst (TU) ratio 1.7474e5 at s = V(|a|=9), p(s) = 79/4096; pointwise influence 32 = kJ/2 at the threshold.
     All as in the text.   [replication]
 R4. N12 (d), assumed class (out_n12_assumed_1.txt; 7 parameter sets x theta in {20, 1} x 20 runs = 280 runs):
     INVALID in 280 of 280.  theta = 20: every run closes below the spike after 1672-2232 points, false step =
     upper tail bound, U below A by 712 (1174 for lam = 0.5); sampling certificates all true, Chernoff events all
     hold.   theta = 1: only the set with lam = 0.5 closes below the spike (7232 points, U below A by 4200).  In
     the other six sets the closure test at the first unpopulated level fails narrowly (0.264 * s_j/(e^b ell) =
     1.23 > 1), the run goes on to 2.2e5 - 1.8e6 outer points, POPULATES the spike, and the false step is then
     the LOWER tail function (the "Harper term" ell >= s_j e^-b Theta(plow) of the assumed class): L > A.
     Trace of one run: L/A = 2.37, U/A = 4.74; (TL) for the assumed class is violated by a factor up to 9.5.
     => the text's "the false step is the tail bound, and the run closes below the spike" is one of two
     mechanisms; with the lower tail function the bracket is invalid from below even when the spike is found.

## 2026-11-26T22:31:40Z — Item 1 tables and Item 2 runs (logs that reached their last line)

Influence tables (r26_influence.py; all controls 0 violations unless said):
 out_infl_T1q3_1.txt (q=3, n=10, cut 5, r=1, 10 seeds, no clash), largest / median over pairs and seeds:
   J      pt            box D=1      box D=5      box D=20      Lip u=0.5    Lip u=1      Lip u=2
   0.25   0.93/0.30     0.29/0.12    0.90/0.29    0.93/0.30     0.16/0.07    0.31/0.13    0.61/0.22
   1      4.92/1.10     0.79/0.35    3.70/1.05    4.92/1.10     0.62/0.25    1.21/0.48    2.35/0.81
   4      21.8/4.30     1.00/0.58    4.99/2.11    16.6/4.30     1.06/0.43    2.26/0.85    4.90/1.59
   8      43.7/8.82     1.00/0.61    5.00/3.36    20.0/7.30     1.00/0.37    2.01/0.86    4.10/1.90
   => pointwise ~ 5.4 J (max) / 1.1 J (median), unbounded in J; box = min(D, pt)-like, saturates at D; Lipschitz
      class saturates at about 2.3 u (max) whatever J.
 out_infl_T2_1.txt (same with clashes, each pair-state entry a clash w.p. 0.15; J = 1): largest values
   C      pt      box D=5   box D=20   Lip u=0.5   Lip u=1   Lip u=2
   none   2.90    2.58      2.90       0.58        1.15      1.94
   10     10.45   4.93      10.45      1.14        2.52      5.38
   20     20.45   4.99      19.22      1.14        2.52      5.45
   30     30.45   4.99      19.99      1.14        2.52      5.45
   => pointwise = C + O(J) (linear in the clash energy); box saturates at D; Lipschitz influence does NOT grow with
      C beyond ~10 kT: 2.5 u (it roughly doubles relative to "no clash").
 out_infl_T3_1.txt (block length k, q=3, r=1, c=4, 6 seeds): pt and box saturate by k = 3 (to 4 digits by k = 8);
   Lipschitz u=1: J=1: 0.86 (k=1) -> 1.35 (k=7), recursion bound 1.362 for k >= 8;  J=4: 1.00, 1.94, 2.43, 3.07,
   3.55 (k=5), 2.70 (k=6), 2.69 (k=7), bound 2.87 for k >= 8 (NOT monotone in k: the models are prefixes, the
   backward message changes);  J=1 with clash 20: 0.98 -> 2.00, bound 2.005.  The pairwise recursion is an upper
   bound of the LP (never below; largest excess 0.40) and is exact for q = 2.
 out_infl_T5_1.txt: same cross-cut interaction (osc 6 kT): pointwise from 0.047 to 5.999 as a field on the first
   inner site varies; Lipschitz influence 0.89 -> 2.90 as the inner chain becomes rigid.
 out_infl_T4_1.txt CRASHED (HiGHS "Status 0: Not Set" on an LP with coefficients spanning 60 decades) -> not
   cited; lp_ratio now truncates coefficients below 1e-15 of the largest and falls back to other HiGHS methods
   (out_band_selftest_5.txt: self-test still 0 violations).  T4 re-running as out_infl_T4_2.txt.  (Own error E3.)

Proposition N12 (r26_n12.py):
 out_n12_scan_1.txt (P0, 12 runs per theta, two lower tail functions):
   Harper lower function of the assumed class: theta >= 1.5: 12/12 invalid, U below A by 277..2547 (false upper
   tail bound); theta = 1: 12/12 invalid, L/A = 2.37 (false LOWER tail bound, spike populated, 2.2e5 points);
   theta <= 0.5: the run aborts with "L>U" in 12/12 (the abort rule catches the inconsistency; the returned trivial
   bracket is valid) -- "false ell" in all of them.
   Theta = id (Markov): theta >= 1.5: 12/12 invalid (same closure below the spike); theta <= 1: 72/72 VALID, with
   3.57e6 outer points (872 x the outer cube).
 out_n12_true_1.txt: true class (Harper, slope 11.765): 40/40 valid; 3 571 712 outer points in every run (872 x).
 out_n12_control_1.txt: product known part, 9 integrands in the class (cone, Harper-extremal dips, the
   log-Lipschitz majorant of the N12 landscape, flat, mixtures, random field, regularised noise), theta in {20,1},
   3 bracket placements, 10 runs each = 540 runs: 0 invalid, 0 other claim violated.  Mutations: Xi/50 and Xi/1000
   -> invalid brackets in 60 of 120 runs; K = 3 -> false sampling certificates in 5 of 60 runs: the control can fail.

Hub = a nearest-neighbour chain (r26_hub.py, out_hub_3.txt; out_hub_1/2.txt used the reference point (0;0..0) at
 which psi is minimal, which makes ell0 already within a factor 3 of A -- kept, not cited for the headline):
 chain c=4, k=16, u=1, cross coupling 14 kT, inner coupling 11 kT: pointwise influence of the boundary site 14,
 class-relative (Lipschitz) 11.45 = ln(V_1/V_0); P(rare boundary state) = pi_h:
   (A) product-class tail function: INVALID 20/20 for pi_h = 0.002 (U below A by 49-62), 0.02 (454-484), 0.2 at
       theta = 20, 5 (2081); valid 20/20 only for pi_h = 0.2 at theta = 1.   Always the upper tail bound.
   (B) envelope of Theorem N4 (u + iota at the boundary site): 0 invalid of 180; 3e3 .. 1.65e6 outer points for a
       16-point outer space.
   (C) conditioning on the boundary site: 0 invalid of 180; 1464 .. 5856 points.
   control (no coupling across the cut): 0 invalid of 180.
 => the failure does NOT need the influence to be spread: one boundary site suffices (at this size), even when
    its state is not rare (pi_h = 0.2, theta >= 5).

## 2026-11-26T22:41:32Z — own error E5 (file written outside my directory), corrected

The section above ("2026-11-26T22:31:40Z — Item 1 tables and Item 2 runs") was first written to
/home/user/MetricChain/NOTES.md, outside the directory this workstream may write in.  Cause: the command was
"cd <ws_R26> && export ... && nohup sh -c '...' &" followed by "cat >> NOTES.md": the "&" put the whole AND-list
(including the cd) into a background subshell, so the foreground shell stayed in the repository root and the
relative path NOTES.md resolved there.  The coordinator pointed it out.  Correction: the section was appended here
verbatim (the 57 lines above), and the stray file was removed by its exact name
(rm /home/user/MetricChain/NOTES.md; it was untracked: "git status --porcelain -- NOTES.md" gave "?? NOTES.md").
From now on every write to this file uses its full path.  No other file outside ws_R26 was written (checked with
"git status --porcelain" below).

## 2026-11-26T23:02:45Z — Item 3, cost table, Gauss, final reruns; report drafted

New scripts: r26_n1.py (blocks S, U, Q1), r26_cost.py, r26_gauss.py; r26_influence.py got blocks T3b, T4b.
r26_alg.py changed twice after the first N12/hub logs (checker refactored for continuous outer spaces; J takes
the larger integer when Vmax is on the level grid): therefore EVERY cited N12 / hub / N1 log was re-run with the
final code (22:53-22:57 UTC): out_band_selftest_6, out_alg_selftest_3, out_n12_abc_2, out_n12_assumed_2,
out_n12_scan_2, out_n12_true_2, out_n12_control_2, out_hub_4, out_n1_S_3, out_n1_U_2, out_n1_Q1_2 — all reached
their last line; numbers identical to the first runs (hub_4 = hub_3 and U_2 = U_1 line by line apart from times).

Results since the last entry:
 - out_n1_Q1_2.txt: Lemma N.0 literally at q = 1 (finite Xi(1) = 10.947 on Q_4): false bracket 10/10 (U = 0.358 A);
   with Xi(1) = +inf: 0/10.
 - out_n1_S_3.txt: Theorem N1, 11 adversarial integrands (atom at max, gaps, heavy lower tails, ...), sharpest
   valid tail functions, 990 runs: 0 violations of any claim; 8804 populated / 5332 negligible levels, 339 stops
   by (c0); mutations Xi/20, K=2, 5*Theta: 156 failing runs of 180.  (out_n1_S_1.txt: 18 false "level > J" flags
   on the flat integrand = my tie handling, own error E4.)
 - out_n1_U_2.txt: Theorem N1' (no cap), Gauss line L = 1.5, 2.5 and Laplace line u = 0.5, 0.8: 81 runs, 0
   violations, 32 levels left as negligible; 15 runs stopped by my 4e6-point limit (not counted).  Laplace line
   with nu1 = 1: no closing level for theta < u/(1-u).
 - out_cost_2.txt: one hot site with influence iota on the uniform cube, sorted-slope bound (E) vs product (P)
   vs conditioning (C): at theta = 1 route E falls to the atom for iota >= 0.5 (E/P = 13, 216, 4.8e6, 9e15 for
   m = 12, 20, 40, 80); C/P = 1.1 .. 11.  At equal closing level the threshold must grow by 2.9, 8.3, 164, 3e3,
   6e4 for iota = 0.5, 1, 2.5, 5, 8 (m = 20, theta = 1).  The sorted-slope bound is loose by up to 4e4 against
   the exact Lemma N.0 function of the one-hot envelope on Q_3, Q_4 -> Proposition R26.4 (below the least
   boundary-state probability the exact tail function does not contain iota).
   (out_cost_1.txt crashed on my own check: own error E8.)
 - out_gauss_1.txt: closed forms of N9 vs quadrature 3e-14; inequalities of N10(b): 0 violations; runs at L = 3:
   M_max / N10(b) bound >= 2402.
 - out_infl_T1q4_1, T1q6_1, T3b_1, T4_2, T4b_1: see report section 3.1.  T4b peak memory 880 MB; T1q6 563 s.
 - out_asym_1.txt: explicit asymmetric influence (pointwise 19.55 vs 0.62) and triangle inequality (0 violations).
 - A foreground "sleep 100" was blocked by the harness (waiting for my own background jobs); not worked around.

Report: /home/user/MetricChain/docs/science/workstreams/R26_REPORT.md (sections 0-5 written; numbers checked
against the final logs).

## 2026-11-26T23:07:22Z — hub in the theory division's own setting; report completed

 - out_n12_hubcube_1.txt (r26_n12.py hubcube, 10 seeds per cell): uniform outer cube Q_12, Harper's functions of
   slope 1, inner Q_16, residual u|b|; dependence confined to the first k0 outer sites (ln V_hub/V_rest = 15.9):
   k0 = 1: valid 80/80;  k0 = 2: invalid 20/20 at theta = 50 and 20 (A/U = 28), valid at 5 and 1;
   k0 = 3: invalid at 50, 20, 5 (53, 53, 136), valid at 1;  k0 = 4: invalid at 50, 20, 5, 1 (98, 98, 252, 556);
   k0 = 6: invalid at every theta (339 .. 1921).  260 of 400 runs invalid, always the upper tail bound.
   Trace (k0 = 2, theta = 20): ell0 = 7.4e-4 already above the bulk (1.2e-7); level 0, M = 820, N = 188 < K = 205,
   q = 0.5, Xi = 10.63, tail = 7.9e-3 <= theta e^b ell = 2.4e-2 -> closes with U = 8.6e-3 < A = 0.244.
   => "the failure needs the influence to be spread" is false in their own setting from two hub sites on.
 - out_asym_1.txt, out_infl_T3b_1.txt: see report.
 - Report sections all written and checked against the cited logs:
   /home/user/MetricChain/docs/science/workstreams/R26_REPORT.md

## 2026-11-26T23:10:00Z — final state

 - Two inline checks were saved as scripts and re-run (identical output): r26_asym.py -> out_asym_2.txt,
   r26_r264.py -> out_r264_2.txt (Proposition R26.4: below the least boundary-state probability the exact
   Lemma N.0 function of the N4 envelope is the same for iota = 3, 8, 11.45, 40 and equals the mixture bound;
   above it: 10.7, 1.6e3, 5.1e4, 1.3e17; 0 violations).
 - Report final: /home/user/MetricChain/docs/science/workstreams/R26_REPORT.md (sections 0-5; a ten-line verdict
   block at the top of section 0).  Every log cited there exists and reaches its last line (checked by a loop
   over the names in the report).
 - Findings: F1 major (N12 mechanism: two false steps), F2 major (hub remark false at finite size: chain 260/300,
   their own cube 260/400), F3 major (band models: boundary-layer reduction R26.1-R26.4; "dependence costs
   slope" is the wrong tool at bounded accuracy; conditioning), F4-F10 minor.
 - Verdicts: N4 proved as stated; N12 (a)-(c) proved as stated, (d) replicated with two corrections; N1/N1'
   proved as stated, gaps (Lemma N.0 at q = 1; constants of (R5)) closed here; N9/N10 proved as stated given the
   Gaussian isoperimetric inequality (from memory, not looked up); N11 read only.
 - Tool actions declined: one foreground "sleep 100" (blocked by the harness; not worked around).
 - No web page was opened.  No state-changing git command was run.  No subagent was used.
 - Files written outside this directory: only docs/science/workstreams/R26_REPORT.md (allowed); the stray
   /home/user/MetricChain/NOTES.md of 22:31 UTC was removed (own error E5 above).
