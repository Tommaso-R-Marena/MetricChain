# R29 — working notes (adversarial review with replication of Theorem 11.58e, theory division, export at 07cde81)

Agent: AI agent of the science division, workstream R29.  Internal review, not external peer review.
Write area: `/home/user/MetricChain/experiments/science/ws_R29/` and
`/home/user/MetricChain/docs/science/workstreams/R29_REPORT.md` only.

Kinds of checking kept apart: **review** (re-derived), **replication** (own code), **re-run** (their scripts),
**read only**.

## Tool actions declined

* 2026-11-27T00:36Z — a Bash call that began with a foreground `sleep 25` (to wait for a background run before
  polling it) was blocked by the harness ("Blocked: sleep 25 followed by: ...").  Not worked around: no chained
  shorter sleeps; from here on background runs are polled with plain short commands between other work.
  (An earlier call with `sleep 20` had been accepted.)  No result is affected.

## Own errors

(none so far)

## Log (times read from the clock, UTC; newest at the end)

* 2026-11-27T00:03:37Z — started.  Read `R29_brief.md` (128 lines) and `COMMON.md` (115 lines) in full.
  Created this directory.  Python 3.13.18, mpmath 1.3.0, numpy 2.5.3, scipy 1.18.1, sympy 1.14.0; 4 cores,
  15 GB.  Export listed (did NOT list or open `read_only_after_your_own_report/`).

* 2026-11-27T00:10:25Z — reading (read only so far, nothing run):
  - THEORY_REPORT.md lines 6021–6758 (Lemma 11.58b … Theorem 11.58e, remarks, to §11.20) — read in full.
  - Z_ADDENDUM.md (532 lines) — read in full.  Z_REPORT.md (446 lines) — read in full.
  - THEORY_REPORT.md 4839–5367 (11.51–11.54: bracket procedures, R[T], Theorem 11.53, 11.53a slope map,
    11.53b) and 5510–5810 (Lemma 11.55, Theorem 11.56, Prop 11.57, Theorem 11.58) — read.
  - z6_certified_tops.py (327 lines), z7_exactness.py (158), zetalib.py (323) — read in full.
  - committed outputs out_z6_certified_u1.txt, out_z7_exactness_u1.txt — read.
  Definitions fixed for my own code (cube pair, slope u):
    p_u = 1/(1+e^u);  theta_na(e) = min{KL(rho||1/2) : KL(rho||p_u) <= e} (0 for e >= eps* = ln cosh(u/2));
    a = KL(p_u||1/2);  Lambda(v) = ln(2/(1+e^-v));  KL(rho||p_u) = KL(rho||1/2) + u rho - Lambda(u);
    J(t) = inf_e[(1-t)theta(e) + t e] = Lambda(tu) - t Lambda(u)  (re-derived: Legendre transform of KL(.||1/2));
    h = max J = KL(Lambda(u)/u || 1/2);  theta_hint(x) = KL((Lambda(u)+x)/u || 1/2);
    Sigma(B,s) = sup_e [B - (1-s)theta(e)]/e = t'(1-s)/(1-t') with J(t')/(1-t') = B/(1-s)  (re-derived);
    R[T](g) = inf_{phi,beta} sup_{gamma>=beta}[min(gamma, phi*theta((g-beta)/phi)) + (1-phi)T(gamma/(1-phi))];
    tau(T) = inf_phi sup_{gamma>=0}[min(gamma, phi a) + (1-phi) T(gamma/(1-phi))];  tau_{k+1} = tau(T_k).
  First observations on z6 (to be tested, not yet findings):
    (o1) the final "ALL CHECKS PASS" tests only `mono` (true by construction: next_top returns <= V.c) and
         `above h` (floating h from zetalib; trivially true if zetalib is missing).  The validity is by
         construction + 3 asserts/exact tests (cap <= 1, signs, top verification).  Rounding-direction
         mutations will probably NOT be caught by the script itself -> need an independent verifier.
    (o2) `assert e.a > 0, "rho must be above p_u"` does not test rho > p_u (KL > 0 on both sides); validity
         does not need it (rho is feasible for e' in the min-definition of theta_na).
    (o3) the cap line is below the MAXIMUM of the generated lines (and zero), not below one line of the stated
         form: Proposition A13 as worded ("lines that are below such lines") does not literally cover it; the
         proof of (S2) does.  Validity of the cap rests on the exact hull/vertices being right.
    (o4) printing: "%.12f" / "%.9f" round to nearest, so a printed top can be below the certified double by up
         to 5e-13 (5e-10 for the ratio).
    (o5) out_z7: (M_2 - T_2)/a = -1.98e-9 at g = 0.95 eps* (negative; A8 says T_2 <= M_2) -> check with my code
         whether that is grid error of W_2.

* 2026-11-27T00:5x — own library `r29lib.py` written (DI = my own integer interval arithmetic; CubeDI; CubeMP;
  exact hull PL; build_step/check_step with certificates).  `r29_i1_selftest.py` -> `log_i1_selftest_01.txt`:
  ALL PASS (1308 containments of mp values in DI intervals, widest 3.5e-65; hull 11096 exact comparisons;
  top_exact 200; Sigma via J vs Sigma direct agree to 3e-38); all four controls fail as they must
  (truncated series 172/200; hull without popping 1710/2000; lowered top 200/200; wrong Lambda 0.068).
  Constants reproduced: u=1: a = 0.110944071671727, h = 0.0291391385016, c_*^2 = 0.0711473217, L = 0.490034.
* re-run (their script, in place, through r29_wrap.py): `z6_certified_tops.py 1 6 400` ->
  `log_rerun_z6_u1_J6_K400.txt`: ALL CHECKS PASS, 0.9 s; nothing written into the export (checked with find -newer).
* Hand derivation (review) BEFORE running tau2 script — PREDICTION P1:
  tau_2 = min_x a*max(a, x+theta(x))/(a+x).  The closed form a^2/(a+x*) (theta(x*) = a - x*) is its value iff
  theta'(x*) >= -x*/(a+x*).  By hand at u = 10: rho* ~ 0.018, theta'(x*) ~ -0.67, x*/(a+x*) ~ 0.115 -> condition
  FAILS, so the closed form of A6a/11.58e(e) should be false for large u (true at u = 1/2, 1, 2, where I expect
  cf = direct and, at u = 1, the value 0.055517524915 of their table).  Run: r29_i1_tau2.py.
* r29_i1_tau2.py -> `log_i1_tau2_01.txt` (71 s).  OUTCOME of P1: confirmed.
  tau_2 (u=1) = 0.05551752491477794461961 = 0.50041001811299 a (their 0.055517524915 = 0.500410018 a: agrees);
  u=2: 0.505615442034 a; u=1/2: 0.500026736444 a.  Rigorous enclosures (DI) of width < 1e-67 contain the mp values;
  the condition theta'(x*) >= -x*/(a+x*) is verified RIGOROUSLY at u = 1/2, 1, 2.
  FINDING (Item 2): the closed form "for the cube tau_2 = a^2/(a+x*)" (A6a line 227; Theorem 11.58e(e)) is FALSE
  for u > u0 = 4.6535196185: there min_x a*max(a, x+theta)/(a+x) is attained beyond x* (u=5: 0.602893 a against
  the formula's 0.604053 a; u=10: 0.75971 a against 0.88596 a).  tau_2 = b_2 itself is not affected (to be
  confirmed with my envelope code at u = 5).
* PREDICTION P2 (before the first run of r29_i1_mytops.py, u=1, J=6, K=200): 0 checker violations; all 5 controls
  rejected; my c_j >= b_j(semi-analytic) with (c_j - b_j)/(b_j - h) ~ 1e-6..1e-4 (quadratic in 1/K, growing with
  the level); their committed tops (K = 3000) >= b_j as well with the excesses 3.5e-8 ... they print; my c_2
  within 1e-6 (relative) of tau_2.
* r29_i1_mytops.py 1 6 200 -> `log_i1_mytops_u1_J6_K200_01.txt` (7 s).  OUTCOME of P2: confirmed in kind; my
  sampling is worse than predicted at level 2 (only 3 sample points below the tangent point 0.041 a of level 1):
  (c_j - b_j)/(b_j - h) = 1.8e-5, 3.7e-5, 5.6e-5, 4.3e-4, 8.8e-4 at j = 2..6.  0 checker violations in 6 steps,
  841 pairs cross-checked in mp (0 violations), 5/5 controls rejected.  Semi-analytic envelope tops (mp, 30 digits):
  b_2 = 0.055517524914778 (= tau_2 closed form, all digits), b_3 = 0.040306053374704, b_4 = 0.034702356817925,
  b_5 = 0.032326518531093, b_6 = 0.031211123647228.  Their COMMITTED tops (K=3000) lie above these by
  2.7e-8, 3.0e-8, 2.7e-7, 2.7e-6, 1.1e-5 of (b_j - h): consistent with Corollary A4 (necessary condition holds).
* DI logarithm rewritten with an integer fast path (7x faster); selftest re-run -> `log_i1_selftest_02.txt`: ALL PASS.
* CubeF.Sigma switched to Newton-from-the-left; agrees with bisection (differences up to 5e-7 only at nearly
  irregular points where the map is ill-conditioned); EnvSA in doubles reproduces the mp tops b_2..b_6 to 15 digits.
* PREDICTION P3 (before r29_i1_verify_theirs.py on the UNMODIFIED z6, u=1, J=6, K=400): shadow reproduces their
  step bit for bit; 0 checker violations; their stored lines = my hull of them; least margins >= 0 ulp (e', th: >= 1
  ulp by construction of up(); slope/beta: about 2.5 ulp left of the 4 nextafter steps); tops equal to my re-run log.
* r29_i1_verify_theirs.py (their UNMODIFIED z6 imported from the export; shadow of step() + my exact checker):
  - u=1, J=6, K=400 -> `log_i1_verify_theirs_u1_J6_K400_01.txt`: P3 confirmed except one detail: least pair margins
    are 0.00 ulp, not >= 0.5: mpmath's float(mpf) TRUNCATES (round_fast = round_down), so up() = nextafter(trunc) is
    the least double above the interval end; still valid in every sign case (checked by hand).  Line margins 2.6/2.2 ulp.
  - u=1, J=80, K=3000 (their committed size) -> `log_i1_verify_theirs_u1_J80_K3000_01.txt` (255 s): 257 394 stored
    lines, 278 704 generated lines, 0 checker violations, 0 hull mismatches, least margins e' 0.00, th 0.00, slope 2.20,
    beta 1.83 ulp; 0 tops below the semi-analytic envelope tops; 0 of 80 tops differ from the committed output.
  - u=2, J=40, K=3000 -> `log_i1_verify_theirs_u2_J40_K3000_01.txt` (120 s): ALL CHECKS PASS; 0 of 40 tops differ.
* PREDICTION P5 (before r29_i1_mutations.py, u=1, J=6, K=400; 30 mutations + baseline):
  caught by the script itself (assert or CHECK FAILED): M11, M13 (assert "cap failed"), M14, M18 (gross), maybe M24;
  NOT caught by the script (ends with ALL CHECKS PASS) but rejected by my checker: M01, M03-M10, M09, M09b, M12, M15,
  M16, M17, M19, M21, M22, M23, M26, M32;  equivalent/harmless (no violation anywhere): M02, M20, M27, M28, maybe M09c.
* r29_i1_mutations.py 1 6 400 -> `log_i1_mutations_u1_J6_K400_01.txt` (74 s; mutant sources and their outputs in
  `mutants/`).  OUTCOME of P5: the direction was right, the script is even less self-checking than predicted.
  30 mutations: caught by the script itself: 2 (M11, M13: both put the cap line above 1 at the top -> assert
  "cap failed").  NOT caught by the script (it ends with "ALL CHECKS PASS") but rejected by my exact checker: 17
  (M01 M03 M04 M05 M06 M22 M23 M18 M07 M08 M09 M09b M21 M10 M12 M15 M17).  Not caught, and valid or equivalent
  on this input: 11 (M02 M32 M19 M20 M09c M14 M16 M26 M24 M27 M28).  Baseline M00: passes both.
  Wrong in P5: I expected M14, M18 (and maybe M24) to be caught by the script.  M14 (cap slope = min over vertices)
  gives a NEGATIVE slope, the hull silently drops the cap line: valid, tops 2e-3 worse.  M24 (hull pop reversed)
  leaves one line per level: valid, useless (tops ~0.965 a).  M18 (the two divergences swapped) prints
  c_2 = 0.055481623494 < tau_2 = 0.055517524915 and c_3/a = 0.360741 < tau_3/a = 0.361189 as "certified" and
  ends with "ALL CHECKS PASS" (its own comparison column (c_j - b_j)/(b_j - h) is negative: -1.4e-3, -2.5e-2,
  -4.1e-2, but that column is not part of the verdict).
  => FINDING (Item 1): the script's final verdict tests only `mono` (true by construction) and `c_j > h`; it cannot
  fail for any rounding-direction or interval error, nor for a gross error such as M18.  Validity rests on the code
  path alone.  My independent checker shows the unmutated code path is right on the committed runs.
* M19 (p_u as a double) is harmless at u = 1 only because the double happens to be below p_u; M32 (rho = 1/2 branch)
  and M16/M26 (top verification) are not exercised at this size.
* own slip: started r29_i1_verify_theirs.py with u = "1/2" (their script needs a float literal): crashed at import
  (`log_i1_verify_theirs_u0.5_J40_K3000_01.txt`, not cited); restarted with "0.5" -> `..._02.txt`.
* PREDICTION P4 (before r29_i2_tau3.py, u = 1): my R[theta](g) agrees with their 16 table values to ~1e-9 or is
  slightly BELOW (their grid zoom can only err upwards); tau_3 = a*tau_2/(a + x2*) with the sup attained at the kink
  x2*, value 0.361189 a +- 1e-6 a (theirs 0.0400717432); tau(M_2) = b_3 = 0.0403060534 to 1e-9 (their grid value
  0.363303 a is 2e-6 a high); at g = 0.95 eps*, M_2 - T_2 >= 0 (their -1.98e-9 a is grid error of their W_2);
  controls: c1 0 cases, c2 small (1e-3), c3 large.
* r29_i2_tau3.py first run (`log_i2_tau3_u1_01.txt`, killed by me, NOT cited): OWN ERROR — my minimiser of
  F(phi, beta; g) (300x300 uniform scan + nested golden sections) missed the minimum at g = 0.1, 0.9, 0.95 eps*
  (my value ABOVE theirs by 2.5e-7, 1.5e-5, 1.8e-6; any (phi, beta) is an upper bound, so the larger value is the
  wrong one): the valley near phi -> 1 is narrower than my phi grid.  At the other 13 rates mine is at or below theirs
  (down to -2.9e-6 at 0.7 eps*, -1.1e-7 at 0.03 eps*: their zoom also stalls).  Control c3 (wrong operator) did NOT
  fail: bad control (the trivial configuration phi -> 0, beta -> g still returns T(g)); replaced by a mutation that
  must undercut the hinted exponent (outer rate g/phi instead of (g - beta)/phi).  Rewriting the minimiser:
  nonuniform scan + several starts + moving zoom with exact theta.
  To examine with care: at g = 0.95 eps* their T_2 exceeds M_2 (theirs: by 2.2e-10; with MY M_2: by 4e-11).
* r29_i1_verify_theirs.py 0.5 40 3000 -> `log_i1_verify_theirs_u0.5_J40_K3000_02.txt` (122 s): ALL CHECKS PASS; 0 of
  40 tops differ from the committed output.  So all three committed z6 outputs (u = 1: 80 levels; 2, 1/2: 40 levels)
  are reproduced digit for digit AND verified by my independent exact checker (0 violations).  Not done: the
  400-level run (K = 4000) of out_z6_certified_u1_J400.txt.
* minimiser of F for R[theta]: second own attempt (moving 2-d zoom, r29rec.Rec) also stalled (above theirs by up to
  2e-6 at small g); third attempt r29rec.Rec2 (coordinates (y1, e); nested 1-d searches, full inner scan) is at or
  below their value at all 16 rates (largest mine - theirs = +1.9e-11 = their print rounding; lowest -2.9e-6 at
  0.7 eps*, -1.1e-7 at 0.03 eps*).  About 1.1 s per rate.  tau_3 script restarted -> `log_i2_tau3_u1_02.txt`.
* Item 3, review (re-derived on paper; details go to the report): Sion applies (E compact convex because W is convex
  and continuous; Phi affine in (B, s); quasi-convex and continuous in e > g because theta is convex and s <= 1); for
  one line inf_{e>g} Phi = B - Sigma(B,s) g if the tangency is at e_t >= g, and (1-s) theta(g) = B'' - Sigma(B'',s) g
  otherwise, with B'' <= B, so (B'', s) is in E because W is nondecreasing; hence
  inf_e max_E Phi = sup{B - Sigma(B, W(B)) g : Sigma finite}  (an EQUALITY), then (S1), (S2).  No gap found.
* PREDICTION P6 (before r29_i3_minimax.py): 0 violations of LHS <= RHS1 and of RHS1 <= M_{W',b'}; |LHS - RHS1| at the
  level of the golden-section accuracy (1e-10 a); control 1 (non-convex): fails in a large fraction of cases, by up
  to several 0.01 a; control 2 (two levels' gain): fails in many cases.
* r29_i3_minimax.py first run -> `log_i3_minimax_u1_01.txt` ("CHECK FAILED", NOT cited as evidence): OWN ERRORS, two:
  (1) my LHS took the infimum over phi only up to 1 - 1e-7; the infimum is often approached as phi -> 1 (e -> g), so
  LHS came out 1e-7 a too large (this is exactly why the statement carries "+ eta"); (2) my Newton slope map could
  overshoot t' >= 1 at nearly irregular points and return a huge negative slope (RHS1 = 1e9 a).  Both fixed
  (phi = 1 as an end point; Sigma returns +inf when t' reaches 1); EnvSA values unaffected (to be re-checked).
  The two controls did fail as they must in that run (non-convex: 67 of 160, up to 0.25 a; two levels for one: 428).
* r29_i3_minimax.py second run -> `log_i3_minimax_u1_02.txt` (40 "violations", NOT cited): OWN ERROR again — the phi
  grid contained 0.5 twice, so the golden-section bracket around the grid minimum was one-sided and LHS came out as
  f(0.5) = a/2 for W_1 and for the chord at small g.  Checked by hand at W_1, g = 1e-6 eps*: the true minimum over phi
  is at the crossing near phi = 0.5003 and equals RHS1 = 0.0554407.  Fixed (np.unique, wider bracket).
* r29_i2_tau3.py second run -> `log_i2_tau3_u1_02.txt` (crashed in part (3), NOT cited; parts (0)-(2) printed):
  x2* = 0.042765837436, tau_3 = a tau_2/(a + x2*) = 0.0400711983953 = 0.361183773 a (theirs 0.361189 a; their referee
  0.361184 a); checks (i), (ii) 0 violations; T_2 = M_2 at 0.95 eps* to 5e-20 in 30 digits (orbit part active), so
  their -1.98e-9 a there is grid noise ((o5) resolved).  OWN ERROR in part (3): the criterion for the grid end was
  wrong (empty index set); rewritten as a minimum over all grid ends.  Part (5) of that run may be affected by the
  Sigma overshoot bug (process started before the fix).  Re-running the whole script.
* r29_i3_minimax.py third run -> `log_i3_minimax_u1_03.txt` (16 s) — CITED.  OUTCOME of P6: confirmed.  1067 cases
  (97 convex families x 11 rates from 1e-6 eps* to 1.5 eps*): LHS <= RHS1: 0 violations, largest |LHS - RHS1| = 8.8e-13 a
  (equality, as re-derived); RHS1 <= M_{W',b'}(g): 0 violations (largest excess 3e-8 a = interpolation of W').
  Controls fail as they must: non-convex families 147 of 160 (up to 0.293 a); two envelope steps for one 635 of 1067.
* own evaluator of one level (r29level.py, from the statement of Theorem 11.56; K and m_max from qlib.level_consts
  because the quoted statement has only "K = O(...)"): 48 test levels agree with theirs to 9e-13 in ln C_max, x_out,
  ln delta', with identical J, K, r_dagger, m_max.
* PREDICTION P7 (before r29_i4_smallrates.py): (A) kappa formula = difference quotient to ~1e-5; Lemma A9 0 violations;
  A9' holds for all eta below some eta_0 (possibly for all eta < h); control fails.  (B) decay ratio of the defect
  D_k(g) tends to kappa_g (not to the proved mu_g = 1/(1+g/(48h)), which is much closer to 1); a k_2 exists for each
  rate with g k_2/h bounded; control with rate kappa_g^2 fails at every rate where enough levels are usable.
* PREDICTION P8 (before r29_i35_onelevel.py): part 1 agreement to 1e-9 with identical integer constants; part 2: no
  violation of (A)-(D) for envelope families (their own test had least slacks 13.9 / 1.2 / 25.4); for my adversarial
  families (chord, lines at the cap, two lines crossing at the top) I expect no violation either (the proofs do not
  use anything beyond admissibility), smallest slack in (C) near the allowance 1 + a d_min; all three controls fail.
* r29_i4_smallrates.py 1 400 first run -> `log_i4_smallrates_u1_K400_01.txt` (121 s; verdict "CHECK FAILED" ONLY because
  my control (B) could not fail: letting k_2 grow to KMAX/2 the too-fast rate kappa_g^2 still holds over 400 levels,
  since D_k << g at the start; OWN ERROR in the design of a control).  Control replaced (same k_2 as for the proved
  rate); re-run -> `..._02.txt`.  Numbers of the first run (unchanged by the fix): kappa formula vs difference quotient
  3e-6; Lemma A9 0 violations on 400 eta; Lemma A9' 0 violations for ALL eta in [1e-9 h, h) (no eta_0 needed for the
  cube at u = 1 on this grid); 1 - kappa(h - eta) -> sqrt(2 eta/vartheta)/h; orbit bounds 0 of 3600; control A fails (151).
  Defect decay ratio over the last 40 usable levels vs kappa_g: g = 0.02h: 0.97977..0.97995 vs 0.980202 (still
  converging); 0.05h: 0.951242..0.951257 vs 0.951251; 0.10h: 0.904882..0.904914 vs 0.904908; 0.25h: 0.7777..0.7790
  vs 0.779025; proved rates mu_g = 0.99958, 0.99896, 0.99792, 0.99482 (48h for h).  Least k_2: 10, 6, 5, 4, 2
  (g k_2/h = 0.2, 0.3, 0.5, 1.0, 2.0: bounded, as k_2 <= C_3/g requires).
* r29_i2_tau3.py third run -> `log_i2_tau3_u1_03.txt` (332 s, reached its last line) — CITED.  OUTCOME of P4:
  confirmed in kind, with one correction of THEIR number.  tau_3 = a tau_2/(a + x2*) = 0.0400711983953 = 0.361183773 a
  (x2* = 0.042765837436; checks (i), (ii): 0 violations on 158 rates; F at the minimiser agrees in 30 digits to 2e-17).
  UB_3 = 0.361184025 a is an upper bound that does not depend on the minimisation being converged (40 001 + 6000
  rates, T_2 <= F at interpolated parameters, T_2 nonincreasing and <= tau_2); b_3 - UB_3 = 2.1166e-3 a > 0.
  The addendum's 0.361189 a (0.0400717432) is ABOVE that upper bound by 5e-6 a: their zooming minimiser stalls
  (their T_2 is high by up to 2.9e-6 at the 16 table rates); their referee's 0.361184 a agrees with mine.
  tau(M_2) = b_3 to 2e-16 a (their grid value 0.363303 a is 2e-6 a high; A12(b) replicated).
  Orbit-curve lower bounds: tau_2 >= 0.398261 a, tau_3 >= 0.322565 a.
  At g >= 0.95 eps*: T_2 = M_2 (30 digits: 5e-20): where the maximising line lies on the uncapped orbit part.
* 2026-11-27T01:02Z — r29_i4_smallrates.py second run -> `log_i4_smallrates_u1_K400_02.txt` (122 s, last line reached) —
  CITED: "no violation; controls fail as they must" (5 of 5).  OUTCOME of P7: held (A9' even for all eta < h).
* r29_i35_onelevel.py 1 300 1000 3000 -> `log_i35_onelevel_u1_01.txt` (36 s, last line reached) — CITED.  OUTCOME of
  P8: held.  Part 1: 2 548 levels, mine vs theirs <= 1.24e-12, integer constants identical.  Part 2: 378 cases,
  122 472 levels: 0 violations of (A), (B), (C), (D); least slacks 7.670 / 1.222 / 15.626 nats; controls fail
  (362; 127; non-convex 6 of 24).
* 2026-11-27T01:02Z — COORDINATOR'S WIND-DOWN ORDER received (hand back within about ten minutes; start nothing
  new; write the report from what is established; mark unfinished items).  No run of mine was executing at that
  moment (both had just ended).  Started nothing after it.
  NOT FINISHED (also in the report, section 6): Item 5 (z3 re-run, `r29_i5_level_of_nest.py` written, never run);
  Item 6 numbers (`r29_i6_crossover.py` written, never run); my tops at u = 2, 1/2; the 400-level run (chunk support
  in r29_i1_verify_theirs.py written, untested); odd inputs for z6; their three reviews NOT opened (directory
  `read_only_after_your_own_report/` never listed).
* Report written: `/home/user/MetricChain/docs/science/workstreams/R29_REPORT.md`.
